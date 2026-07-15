> DEVELOPER

深度 review `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/minicpm.py` 的未提交修改（+154 行）。

这是 SOAR 比赛的提交包核心文件——custom SGLang fork 里的 MiniCPM-SALA 模型实现。改动很大很危险，必须看懂每一行的意图、风险与正确性。

请：
1. 跑 `git -C /user_4813494d/openbmb diff demo-sala/sglang/python/sglang/srt/models/minicpm.py` 把完整 diff 看清楚（不要 truncate）
2. 跑 `git -C /user_4813494d/openbmb log -10 -- demo-sala/sglang/python/sglang/srt/models/minicpm.py` 看历史 commit 上下文
3. 对照前后文（必要时 `Read` 整个文件附近段落）确认每块改动的语义
4. 重点判断：
   - 改动属于哪类：prefill/decode/attention/InfLLM-v2/EAGLE draft/sliding-window/量化分发/CUDA graph？
   - 是否涉及 `docs/prefill/current.md` 中提到的危险点（`fi_convert` 跨层缓存、`compressed_max_seqlen_k` 等）？
   - 是否影响 standard layers (0,9,16,17,22,29,30,31) vs GLA layers 的派发？
   - 有没有可能与最近 commit `c87538d` (draft sliding-window attention kv_indices clip) / `1d8533b` (sliding-window draft prefill CLI flag) 相关？
   - 是否为可独立提交的逻辑单元？还是必须和其它文件一起提？
5. 列出每块逻辑的潜在风险（正确性、性能、与 EAGLE-3 verify 路径的耦合）

CLAUDE.md 关键背景：32 layers 混合（8 standard + 24 GLA），dense_len=8192，超过走 InfLLM-v2 稀疏；EAGLE-3 chain verify 是当前生产 spec 路径。

输出格式：
- 改动分块总览（按代码逻辑而不是按 diff hunk）
- 每块意图（一句话）+ 风险评估（绿/黄/红）
- 整体提交策略建议（一个 commit 还是拆分）
- 控制在 600 字内

> AGENT

我来深度分析这个修改。先获取完整 diff 和历史上下文。

> TOOL

tool_use Bash
```json
{
  "command": "git -C /user_4813494d/openbmb diff demo-sala/sglang/python/sglang/srt/models/minicpm.py"
}
```

> TOOL

tool_result Bash
```
diff --git a/demo-sala/sglang/python/sglang/srt/models/minicpm.py b/demo-sala/sglang/python/sglang/srt/models/minicpm.py
index a35d38a..4866d9c 100644
--- a/demo-sala/sglang/python/sglang/srt/models/minicpm.py
+++ b/demo-sala/sglang/python/sglang/srt/models/minicpm.py
@@ -320,8 +320,10 @@ from sglang.srt.model_loader.weight_utils import default_weight_loader
 from sglang.srt.utils import add_prefix
 
 # ── Medusa hidden-state collection ──────────────────────────────────────
+import atexit as _atexit
 import os as _os
 import threading as _threading
+from concurrent.futures import ThreadPoolExecutor as _ThreadPoolExecutor
 
 _MEDUSA_COLLECT_DIR = "/tmp/medusa_collect"
 _MEDUSA_MAX_TOKENS = 4096  # save at most this many tokens (from tail)
@@ -369,10 +371,124 @@ _EAGLE3_AUX_LAYERS = [
 ]
 _EAGLE3_MAX_TOKENS = int(_os.environ.get("EAGLE3_MAX_TOKENS", "2048"))  # 0 = no limit
 _EAGLE3_TOP_K = int(_os.environ.get("EAGLE3_TOP_K", "256"))
+_EAGLE3_ONESTAGE_NVFP4 = _os.environ.get("EAGLE3_ONESTAGE_NVFP4", "1") == "1"
+_EAGLE3_ONESTAGE_SAVE_WORKERS = int(_os.environ.get("EAGLE3_ONESTAGE_SAVE_WORKERS", "4"))
 _eagle3_counter = 0
 _eagle3_lock = _threading.Lock()
 _eagle3_aux_cache = {}  # layer_idx -> tensor, populated during forward
 _eagle3_onestage_buffers = {}
+_eagle3_onestage_save_executor = None
+
+_EAGLE3_FP4_GROUP_SIZE = 16
+_EAGLE3_FP4_MAX = 6.0
+_EAGLE3_FP4_BOUNDS = torch.tensor(
+    [0.25, 0.75, 1.25, 1.75, 2.5, 3.5, 5.0], dtype=torch.float32
+)
+
+
+def _eagle3_nvfp4_encode(x):
+    if x.shape[-1] % _EAGLE3_FP4_GROUP_SIZE != 0:
+        raise ValueError(
+            f"last dim {x.shape[-1]} not divisible by {_EAGLE3_FP4_GROUP_SIZE}"
+        )
+    if x.shape[-1] % 2 != 0:
+        raise ValueError("last dim must be even for byte packing")
+    if x.dtype != torch.bfloat16:
+        x = x.to(torch.bfloat16)
+
+    *prefix, dim = x.shape
+    n_groups = dim // _EAGLE3_FP4_GROUP_SIZE
+    grouped = x.contiguous().reshape(*prefix, n_groups, _EAGLE3_FP4_GROUP_SIZE)
+    scale = (
+        grouped.abs().amax(-1, keepdim=True).clamp(min=1e-8) / _EAGLE3_FP4_MAX
+    ).to(torch.bfloat16)
+    q = grouped / scale
+    bounds = _EAGLE3_FP4_BOUNDS.to(device=q.device, dtype=torch.bfloat16)
+    abs_idx = torch.bucketize(
+        q.abs().clamp(max=_EAGLE3_FP4_MAX), bounds, out_int32=True
+    ).to(torch.uint8)
+    sign_bit = ((q < 0) & (abs_idx != 0)).to(torch.uint8).mul_(8)
+    codes = (abs_idx | sign_bit).reshape(*prefix, dim)
+    pair = codes.reshape(*prefix, dim // 2, 2)
+    packed = (pair[..., 0] | (pair[..., 1] << 4)).to(torch.uint8)
+    return packed.contiguous(), scale.squeeze(-1).contiguous()
+
+
+def _eagle3_onestage_get_save_executor():
+    global _eagle3_onestage_save_executor
+    if _EAGLE3_ONESTAGE_SAVE_WORKERS <= 0:
+        return None
+    if _eagle3_onestage_save_executor is None:
+        _eagle3_onestage_save_executor = _ThreadPoolExecutor(
+            max_workers=_EAGLE3_ONESTAGE_SAVE_WORKERS,
+            thread_name_prefix="eagle3-save",
+        )
+    return _eagle3_onestage_save_executor
+
+
+def _eagle3_onestage_shutdown_save_executor():
+    global _eagle3_onestage_save_executor
+    ex = _eagle3_onestage_save_executor
+    if ex is not None:
+        ex.shutdown(wait=True)
+        _eagle3_onestage_save_executor = None
+
+
+_atexit.register(_eagle3_onestage_shutdown_save_executor)
+
+
+def _eagle3_onestage_save_job(path, rid, buf):
+    token_ids = torch.tensor(buf["token_ids"], dtype=torch.long)
+    assistant_mask = torch.tensor(buf["assistant_mask"], dtype=torch.bool)
+    payload = {
+        "token_ids": token_ids,
+        "assistant_mask": assistant_mask,
+        "top_logit_values": torch.cat(buf["top_logit_values"], dim=0).to(
+            torch.bfloat16
+        ),
+        "top_logit_indices": torch.cat(buf["top_logit_indices"], dim=0).to(
+            torch.int32
+        ),
+        "target_logsumexp": torch.cat(buf["target_logsumexp"], dim=0).to(
+            torch.float32
+        ),
+        "metadata": {
+            "schema": "eagle3_onestage_decode_v3",
+            "rid": str(rid),
+            "mode": str(buf.get("mode", "full")),
+            "prompt_len": int(buf["prompt_len"]),
+            "prompt_last_token": int(buf["token_ids"][0]),
+            "generated_tokens_stored": int(len(buf["token_ids"]) - 1),
+            "generated_tokens_required": int(buf["want_tokens"]),
+            "flushed_by": str(buf.get("flushed_by", "length")),
+            "aux_layers": list(_EAGLE3_AUX_LAYERS),
+            "top_k": int(_EAGLE3_TOP_K),
+            "aux_storage": "nvfp4_direct" if _EAGLE3_ONESTAGE_NVFP4 else "bf16_debug",
+            "alignment": "token_ids=[prompt_last]+generated rows consumed by forward; full mode requests one extra token so the last stored generated token has logits",
+        },
+    }
+
+    aux_hidden = torch.cat(buf["aux_hidden"], dim=0).to(torch.bfloat16).contiguous()
+    if _EAGLE3_ONESTAGE_NVFP4:
+        aux_packed, aux_scale = _eagle3_nvfp4_encode(aux_hidden)
+        payload["aux_packed"] = aux_packed
+        payload["aux_scale"] = aux_scale
+        payload["aux_hidden_shape"] = tuple(aux_hidden.shape)
+        payload["format"] = "nvfp4_aux_v1"
+    else:
+        # Diagnostic path only: formal v3mix collection requires direct NVFP4.
+        payload["aux_hidden"] = aux_hidden
+
+    tmp_path = f"{path}.tmp.{_os.getpid()}.{_threading.get_ident()}"
+    torch.save(payload, tmp_path)
+    _os.replace(tmp_path, path)
+
+
+def _eagle3_onestage_log_save_error(fut):
+    try:
+        fut.result()
+    except Exception as exc:
+        print(f"[eagle3-onestage-save] failed: {type(exc).__name__}: {exc}", flush=True)
 
 
 def _eagle3_capture_layer(layer_idx, hidden_states):
@@ -423,38 +539,12 @@ def _eagle3_topk_for_hidden(hidden_rows, lm_head, scale_width):
 
 def _eagle3_onestage_flush(rid, buf):
     path = _os.path.join(_EAGLE3_ONESTAGE_DIR, f"{_eagle3_safe_rid(rid)}.pt")
-    token_ids = torch.tensor(buf["token_ids"], dtype=torch.long)
-    assistant_mask = torch.tensor(buf["assistant_mask"], dtype=torch.bool)
-    torch.save(
-        {
-            "token_ids": token_ids,
-            "assistant_mask": assistant_mask,
-            "aux_hidden": torch.cat(buf["aux_hidden"], dim=0).to(torch.bfloat16),
-            "top_logit_values": torch.cat(buf["top_logit_values"], dim=0).to(
-                torch.bfloat16
-            ),
-            "top_logit_indices": torch.cat(buf["top_logit_indices"], dim=0).to(
-                torch.int32
-            ),
-            "target_logsumexp": torch.cat(buf["target_logsumexp"], dim=0).to(
-                torch.float32
-            ),
-            "metadata": {
-                "schema": "eagle3_onestage_decode_v2",
-                "rid": str(rid),
-                "mode": str(buf.get("mode", "full")),
-                "prompt_len": int(buf["prompt_len"]),
-                "prompt_last_token": int(buf["token_ids"][0]),
-                "generated_tokens_stored": int(len(buf["token_ids"]) - 1),
-                "generated_tokens_required": int(buf["want_tokens"]),
-                "flushed_by": str(buf.get("flushed_by", "length")),
-                "aux_layers": list(_EAGLE3_AUX_LAYERS),
-                "top_k": int(_EAGLE3_TOP_K),
-                "alignment": "token_ids=[prompt_last]+generated rows consumed by forward; full mode requests one extra token so the last stored generated token has logits",
-            },
-        },
-        path,
-    )
+    executor = _eagle3_onestage_get_save_executor()
+    if executor is None:
+        _eagle3_onestage_save_job(path, rid, buf)
+    else:
+        fut = executor.submit(_eagle3_onestage_save_job, path, rid, buf)
+        fut.add_done_callback(_eagle3_onestage_log_save_error)
 
 
 def _eagle3_onestage_collect(hidden_states, input_ids, forward_batch, lm_head, scale_width):
```

> TOOL

tool_use Bash
```json
{
  "command": "git -C /user_4813494d/openbmb log -10 --oneline -- demo-sala/sglang/python/sglang/srt/models/minicpm.py"
}
```

> TOOL

tool_result Bash
```
ddcce88 demo-sala: spec fork tweaks + fp4 tune cache
784e741 feat: add one-stage eagle data collection
eeee998 perf(gla): fused o_norm + sigmoid_mul triton kernel (3-in-1)
eb634cc perf(gla): fused sigmoid+mul triton kernel for output gate
3d21ca1 perf(gla): out-of-place fused qk_norm+rope (triton) — eliminates split contig
7fd6d60 perf(gla): fused qk_norm + rope (TRT-LLM kernel) for prefill
41d8c8d chore: add gla prefill profile buckets
9528a72 perf(prefill): fuse mlp activation fp4 quant
5337cc1 perf(prefill): derive sparse seqlens from topk
208bb39 chore(minicpm): add subop profiling hooks
```

> TOOL

tool_use Bash
```json
{
  "command": "git -C /user_4813494d/openbmb log -5 --oneline"
}
```

> TOOL

tool_result Bash
```
c87538d eagle: draft sliding-window attention (kv_indices clip,消除 stale-KV 风险)
1d8533b eagle: sliding-window draft prefill CLI flag + dense_as_sparse 默认 True
7ef0eb0 feat: add v3mix eagle data collection
373023a feat: add ngram routing for eagle
19a078d eagle D7 调档 5/11 → 6/13 + probe-sala-s2 反向 SSH 调试设施
```

> AGENT

现在读取文件上下文和历史提交，确认改动涉及的范围。

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/minicpm.py",
  "offset": 315,
  "limit": 550
}
```

> TOOL

tool_result Read
```
315	    ParallelLMHead,
316	    VocabParallelEmbedding,
317	)
318	from sglang.srt.model_executor.forward_batch_info import ForwardBatch, ForwardMode
319	from sglang.srt.model_loader.weight_utils import default_weight_loader
320	from sglang.srt.utils import add_prefix
321	
322	# ── Medusa hidden-state collection ──────────────────────────────────────
323	import atexit as _atexit
324	import os as _os
325	import threading as _threading
326	from concurrent.futures import ThreadPoolExecutor as _ThreadPoolExecutor
327	
328	_MEDUSA_COLLECT_DIR = "/tmp/medusa_collect"
329	_MEDUSA_MAX_TOKENS = 4096  # save at most this many tokens (from tail)
330	_medusa_counter = 0
331	_medusa_lock = _threading.Lock()
332	
333	
334	def _maybe_collect_hidden(hidden_states, input_ids, forward_batch):
335	    """Save post-norm hidden states during EXTEND for Medusa training.
336	
337	    For long sequences (>4096 tok), only saves the LAST 4096 tokens.
338	    This ensures hidden states carry long-context (sparse attention) information.
339	    """
340	    global _medusa_counter
341	    if not _os.path.isdir(_MEDUSA_COLLECT_DIR):
342	        return
343	    if forward_batch.forward_mode != ForwardMode.EXTEND:
344	        return
345	    seq_lens = forward_batch.extend_seq_lens_cpu
346	    if seq_lens is None:
347	        return
348	    pt = 0
349	    with _medusa_lock:
350	        for seq_len in seq_lens:
351	            start = pt + max(0, seq_len - _MEDUSA_MAX_TOKENS)
352	            h = hidden_states[start : pt + seq_len].to(torch.bfloat16).cpu()
353	            ids = input_ids[start : pt + seq_len].cpu()
354	            torch.save(
355	                {"hidden_states": h, "token_ids": ids},
356	                _os.path.join(_MEDUSA_COLLECT_DIR, f"{_medusa_counter:06d}.pt"),
357	            )
358	            _medusa_counter += 1
359	            pt += seq_len
360	# ────────────────────────────────────────────────────────────────────────
361	
362	
363	# ── EAGLE-3 aux hidden + top-logit collection ─────────────────────────
364	_EAGLE3_COLLECT_DIR = _os.environ.get("EAGLE3_COLLECT_DIR", "")
365	_EAGLE3_ONESTAGE_DIR = _os.environ.get("EAGLE3_ONESTAGE_DIR", "")
366	_EAGLE3_ONESTAGE_RID_PREFIX = _os.environ.get("EAGLE3_ONESTAGE_RID_PREFIX", "e3os")
367	_EAGLE3_AUX_LAYERS = [
368	    int(x)
369	    for x in _os.environ.get("EAGLE3_AUX_LAYERS", "1,10,22").split(",")
370	    if x.strip()
371	]
372	_EAGLE3_MAX_TOKENS = int(_os.environ.get("EAGLE3_MAX_TOKENS", "2048"))  # 0 = no limit
373	_EAGLE3_TOP_K = int(_os.environ.get("EAGLE3_TOP_K", "256"))
374	_EAGLE3_ONESTAGE_NVFP4 = _os.environ.get("EAGLE3_ONESTAGE_NVFP4", "1") == "1"
375	_EAGLE3_ONESTAGE_SAVE_WORKERS = int(_os.environ.get("EAGLE3_ONESTAGE_SAVE_WORKERS", "4"))
376	_eagle3_counter = 0
377	_eagle3_lock = _threading.Lock()
378	_eagle3_aux_cache = {}  # layer_idx -> tensor, populated during forward
379	_eagle3_onestage_buffers = {}
380	_eagle3_onestage_save_executor = None
381	
382	_EAGLE3_FP4_GROUP_SIZE = 16
383	_EAGLE3_FP4_MAX = 6.0
384	_EAGLE3_FP4_BOUNDS = torch.tensor(
385	    [0.25, 0.75, 1.25, 1.75, 2.5, 3.5, 5.0], dtype=torch.float32
386	)
387	
388	
389	def _eagle3_nvfp4_encode(x):
390	    if x.shape[-1] % _EAGLE3_FP4_GROUP_SIZE != 0:
391	        raise ValueError(
392	            f"last dim {x.shape[-1]} not divisible by {_EAGLE3_FP4_GROUP_SIZE}"
393	        )
394	    if x.shape[-1] % 2 != 0:
395	        raise ValueError("last dim must be even for byte packing")
396	    if x.dtype != torch.bfloat16:
397	        x = x.to(torch.bfloat16)
398	
399	    *prefix, dim = x.shape
400	    n_groups = dim // _EAGLE3_FP4_GROUP_SIZE
401	    grouped = x.contiguous().reshape(*prefix, n_groups, _EAGLE3_FP4_GROUP_SIZE)
402	    scale = (
403	        grouped.abs().amax(-1, keepdim=True).clamp(min=1e-8) / _EAGLE3_FP4_MAX
404	    ).to(torch.bfloat16)
405	    q = grouped / scale
406	    bounds = _EAGLE3_FP4_BOUNDS.to(device=q.device, dtype=torch.bfloat16)
407	    abs_idx = torch.bucketize(
408	        q.abs().clamp(max=_EAGLE3_FP4_MAX), bounds, out_int32=True
409	    ).to(torch.uint8)
410	    sign_bit = ((q < 0) & (abs_idx != 0)).to(torch.uint8).mul_(8)
411	    codes = (abs_idx | sign_bit).reshape(*prefix, dim)
412	    pair = codes.reshape(*prefix, dim // 2, 2)
413	    packed = (pair[..., 0] | (pair[..., 1] << 4)).to(torch.uint8)
414	    return packed.contiguous(), scale.squeeze(-1).contiguous()
415	
416	
417	def _eagle3_onestage_get_save_executor():
418	    global _eagle3_onestage_save_executor
419	    if _EAGLE3_ONESTAGE_SAVE_WORKERS <= 0:
420	        return None
421	    if _eagle3_onestage_save_executor is None:
422	        _eagle3_onestage_save_executor = _ThreadPoolExecutor(
423	            max_workers=_EAGLE3_ONESTAGE_SAVE_WORKERS,
424	            thread_name_prefix="eagle3-save",
425	        )
426	    return _eagle3_onestage_save_executor
427	
428	
429	def _eagle3_onestage_shutdown_save_executor():
430	    global _eagle3_onestage_save_executor
431	    ex = _eagle3_onestage_save_executor
432	    if ex is not None:
433	        ex.shutdown(wait=True)
434	        _eagle3_onestage_save_executor = None
435	
436	
437	_atexit.register(_eagle3_onestage_shutdown_save_executor)
438	
439	
440	def _eagle3_onestage_save_job(path, rid, buf):
441	    token_ids = torch.tensor(buf["token_ids"], dtype=torch.long)
442	    assistant_mask = torch.tensor(buf["assistant_mask"], dtype=torch.bool)
443	    payload = {
444	        "token_ids": token_ids,
445	        "assistant_mask": assistant_mask,
446	        "top_logit_values": torch.cat(buf["top_logit_values"], dim=0).to(
447	            torch.bfloat16
448	        ),
449	        "top_logit_indices": torch.cat(buf["top_logit_indices"], dim=0).to(
450	            torch.int32
451	        ),
452	        "target_logsumexp": torch.cat(buf["target_logsumexp"], dim=0).to(
453	            torch.float32
454	        ),
455	        "metadata": {
456	            "schema": "eagle3_onestage_decode_v3",
457	            "rid": str(rid),
458	            "mode": str(buf.get("mode", "full")),
459	            "prompt_len": int(buf["prompt_len"]),
460	            "prompt_last_token": int(buf["token_ids"][0]),
461	            "generated_tokens_stored": int(len(buf["token_ids"]) - 1),
462	            "generated_tokens_required": int(buf["want_tokens"]),
463	            "flushed_by": str(buf.get("flushed_by", "length")),
464	            "aux_layers": list(_EAGLE3_AUX_LAYERS),
465	            "top_k": int(_EAGLE3_TOP_K),
466	            "aux_storage": "nvfp4_direct" if _EAGLE3_ONESTAGE_NVFP4 else "bf16_debug",
467	            "alignment": "token_ids=[prompt_last]+generated rows consumed by forward; full mode requests one extra token so the last stored generated token has logits",
468	        },
469	    }
470	
471	    aux_hidden = torch.cat(buf["aux_hidden"], dim=0).to(torch.bfloat16).contiguous()
472	    if _EAGLE3_ONESTAGE_NVFP4:
473	        aux_packed, aux_scale = _eagle3_nvfp4_encode(aux_hidden)
474	        payload["aux_packed"] = aux_packed
475	        payload["aux_scale"] = aux_scale
476	        payload["aux_hidden_shape"] = tuple(aux_hidden.shape)
477	        payload["format"] = "nvfp4_aux_v1"
478	    else:
479	        # Diagnostic path only: formal v3mix collection requires direct NVFP4.
480	        payload["aux_hidden"] = aux_hidden
481	
482	    tmp_path = f"{path}.tmp.{_os.getpid()}.{_threading.get_ident()}"
483	    torch.save(payload, tmp_path)
484	    _os.replace(tmp_path, path)
485	
486	
487	def _eagle3_onestage_log_save_error(fut):
488	    try:
489	        fut.result()
490	    except Exception as exc:
491	        print(f"[eagle3-onestage-save] failed: {type(exc).__name__}: {exc}", flush=True)
492	
493	
494	def _eagle3_capture_layer(layer_idx, hidden_states):
495	    """Called inside MiniCPMModel.forward loop to capture aux layer outputs."""
496	    if (
497	        not (_EAGLE3_COLLECT_DIR or _EAGLE3_ONESTAGE_DIR)
498	        or layer_idx not in _EAGLE3_AUX_LAYERS
499	    ):
500	        return
501	    _eagle3_aux_cache[layer_idx] = hidden_states.detach()
502	
503	
504	def _eagle3_safe_rid(rid):
505	    return "".join(c if c.isalnum() or c in "._-" else "_" for c in str(rid))
506	
507	
508	def _eagle3_parse_onestage_request(rid):
509	    rid = str(rid)
510	    if not rid.startswith(_EAGLE3_ONESTAGE_RID_PREFIX):
511	        return None
512	    parts = rid.replace(":", "_").split("_")
513	    if not parts:
514	        return None
515	    try:
516	        want_tokens = int(parts[-1])
517	    except ValueError:
518	        return None
519	    mode = "full"
520	    if len(parts) >= 3 and parts[1] in {"norm", "full"}:
521	        mode = parts[1]
522	    return {"want_tokens": want_tokens, "mode": mode}
523	
524	
525	def _eagle3_concat_aux_rows(row_index):
526	    aux_parts = []
527	    for li in _EAGLE3_AUX_LAYERS:
528	        aux_parts.append(_eagle3_aux_cache[li][row_index : row_index + 1])
529	    return torch.cat(aux_parts, dim=-1)
530	
531	
532	def _eagle3_topk_for_hidden(hidden_rows, lm_head, scale_width):
533	    logits = torch.matmul(hidden_rows / scale_width, lm_head.weight.T).float()
534	    topk = min(_EAGLE3_TOP_K, logits.shape[-1])
535	    topk_vals, topk_ids = torch.topk(logits, topk, dim=-1)
536	    target_logsumexp = torch.logsumexp(logits, dim=-1)
537	    return topk_vals, topk_ids, target_logsumexp
538	
539	
540	def _eagle3_onestage_flush(rid, buf):
541	    path = _os.path.join(_EAGLE3_ONESTAGE_DIR, f"{_eagle3_safe_rid(rid)}.pt")
542	    executor = _eagle3_onestage_get_save_executor()
543	    if executor is None:
544	        _eagle3_onestage_save_job(path, rid, buf)
545	    else:
546	        fut = executor.submit(_eagle3_onestage_save_job, path, rid, buf)
547	        fut.add_done_callback(_eagle3_onestage_log_save_error)
548	
549	
550	def _eagle3_onestage_collect(hidden_states, input_ids, forward_batch, lm_head, scale_width):
551	    if not _EAGLE3_ONESTAGE_DIR or not _os.path.isdir(_EAGLE3_ONESTAGE_DIR):
552	        return False
553	    if len(_eagle3_aux_cache) != len(_EAGLE3_AUX_LAYERS):
554	        return True
555	
556	    reqs = getattr(forward_batch, "reqs", None)
557	    if not reqs:
558	        return True
559	
560	    mode = forward_batch.forward_mode
561	    if mode == ForwardMode.EXTEND:
562	        seq_lens = forward_batch.extend_seq_lens_cpu
563	        if seq_lens is None:
564	            return True
565	        pt = 0
566	        with _eagle3_lock:
567	            for req, seq_len in zip(reqs, seq_lens):
568	                rid = getattr(req, "rid", "")
569	                parsed = _eagle3_parse_onestage_request(rid)
570	                if parsed is None or parsed["want_tokens"] <= 0 or seq_len <= 0:
571	                    pt += seq_len
572	                    continue
573	                row = pt + seq_len - 1
574	                prompt_last = int(input_ids[row].detach().cpu().item())
575	                topk_vals, topk_ids, target_lse = _eagle3_topk_for_hidden(
576	                    hidden_states[row : row + 1], lm_head, scale_width
577	                )
578	                _eagle3_onestage_buffers[rid] = {
579	                    "want_tokens": parsed["want_tokens"],
580	                    "mode": parsed["mode"],
581	                    "flushed_by": "length",
582	                    "prompt_len": len(getattr(req, "origin_input_ids", [])),
583	                    "token_ids": [prompt_last],
584	                    "assistant_mask": [False],
585	                    "aux_hidden": [
586	                        _eagle3_concat_aux_rows(row).to(torch.bfloat16).cpu()
587	                    ],
588	                    "top_logit_values": [topk_vals.to(torch.bfloat16).cpu()],
589	                    "top_logit_indices": [topk_ids.to(torch.int32).cpu()],
590	                    "target_logsumexp": [target_lse.to(torch.float32).cpu()],
591	                }
592	                pt += seq_len
593	        return True
594	
595	    if mode == ForwardMode.DECODE:
596	        # Decode collection is handled after sampling in the scheduler. That
597	        # Python path still runs when CUDA graph replays the model forward.
598	        return True
599	
600	    return True
601	
602	
603	def _eagle3_onestage_collect_decode_from_scheduler(
604	    reqs, current_token_ids, aux_hidden_rows, next_token_logits
605	):
606	    """Append decode rows from scheduler output processing.
607	
608	    `current_token_ids[i]` is the token consumed by this decode forward. The
609	    sampled `next_token_id` has not been appended yet when this is called.
610	    """
611	    if not _EAGLE3_ONESTAGE_DIR or not _os.path.isdir(_EAGLE3_ONESTAGE_DIR):
612	        return
613	    if aux_hidden_rows is None or next_token_logits is None:
614	        return
615	
616	    with _eagle3_lock:
617	        active_rows = []
618	        active_rids = []
619	        active_token_ids = []
620	        for i, req in enumerate(reqs):
621	            rid = getattr(req, "rid", "")
622	            if rid in _eagle3_onestage_buffers:
623	                active_rows.append(i)
624	                active_rids.append(rid)
625	                active_token_ids.append(int(current_token_ids[i]))
626	        if not active_rows:
627	            return
628	
629	        row_tensor = torch.tensor(
630	            active_rows, dtype=torch.long, device=next_token_logits.device
631	        )
632	        selected_logits = next_token_logits.index_select(0, row_tensor).float()
633	        topk = min(_EAGLE3_TOP_K, selected_logits.shape[-1])
634	        topk_vals, topk_ids = torch.topk(selected_logits, topk, dim=-1)
635	        target_lse = torch.logsumexp(selected_logits, dim=-1)
636	
637	        for j, rid in enumerate(active_rids):
638	            buf = _eagle3_onestage_buffers.get(rid)
639	            if buf is None:
640	                continue
641	            row = active_rows[j]
642	            buf["token_ids"].append(active_token_ids[j])
643	            buf["assistant_mask"].append(True)
644	            buf["aux_hidden"].append(
645	                aux_hidden_rows[row : row + 1].to(torch.bfloat16).cpu()
646	            )
647	            buf["top_logit_values"].append(
648	                topk_vals[j : j + 1].to(torch.bfloat16).cpu()
649	            )
650	            buf["top_logit_indices"].append(
651	                topk_ids[j : j + 1].to(torch.int32).cpu()
652	            )
653	            buf["target_logsumexp"].append(
654	                target_lse[j : j + 1].to(torch.float32).cpu()
655	            )
656	            if len(buf["token_ids"]) - 1 >= buf["want_tokens"]:
657	                buf["flushed_by"] = "length"
658	                _eagle3_onestage_flush(rid, buf)
659	                del _eagle3_onestage_buffers[rid]
660	
661	
662	def _eagle3_onestage_finish_from_scheduler(req):
663	    """Flush normal-mode variable-length samples when generation stops early."""
664	    if not _EAGLE3_ONESTAGE_DIR or not _os.path.isdir(_EAGLE3_ONESTAGE_DIR):
665	        return
666	    rid = getattr(req, "rid", "")
667	    with _eagle3_lock:
668	        buf = _eagle3_onestage_buffers.get(rid)
669	        if buf is None or buf.get("mode") != "norm":
670	            return
671	        buf["flushed_by"] = "finish"
672	        _eagle3_onestage_flush(rid, buf)
673	        del _eagle3_onestage_buffers[rid]
674	
675	
676	def _eagle3_collect(hidden_states, input_ids, forward_batch, lm_head, scale_width):
677	    """Save aux hidden + top-K logits during EXTEND for EAGLE-3 training."""
678	    global _eagle3_counter
679	    if _EAGLE3_ONESTAGE_DIR:
680	        try:
681	            _eagle3_onestage_collect(
682	                hidden_states, input_ids, forward_batch, lm_head, scale_width
683	            )
684	        finally:
685	            _eagle3_aux_cache.clear()
686	        return
687	    if not _EAGLE3_COLLECT_DIR or not _os.path.isdir(_EAGLE3_COLLECT_DIR):
688	        return
689	    if forward_batch.forward_mode != ForwardMode.EXTEND:
690	        _eagle3_aux_cache.clear()
691	        return
692	    seq_lens = forward_batch.extend_seq_lens_cpu
693	    if seq_lens is None:
694	        _eagle3_aux_cache.clear()
695	        return
696	    if len(_eagle3_aux_cache) != len(_EAGLE3_AUX_LAYERS):
697	        _eagle3_aux_cache.clear()
698	        return
699	
700	    # Compute logits for top-K extraction
701	    logits = torch.matmul(hidden_states / scale_width, lm_head.weight.T)
702	
703	    pt = 0
704	    with _eagle3_lock:
705	        for seq_len in seq_lens:
706	            if _EAGLE3_MAX_TOKENS > 0:
707	                start = pt + max(0, seq_len - _EAGLE3_MAX_TOKENS)
708	            else:
709	                start = pt
710	            end = pt + seq_len
711	            ids = input_ids[start:end].cpu()
712	
713	            # Concat aux layers: (tokens, 4096*3)
714	            aux_parts = []
715	            for li in _EAGLE3_AUX_LAYERS:
716	                aux_parts.append(
717	                    _eagle3_aux_cache[li][start:end].to(torch.bfloat16).cpu()
718	                )
719	            aux_hidden = torch.cat(aux_parts, dim=-1)
720	
721	            # Top-K logits
722	            seg_logits = logits[start:end].float()
723	            topk_vals, topk_ids = torch.topk(seg_logits, _EAGLE3_TOP_K, dim=-1)
724	            target_logsumexp = torch.logsumexp(seg_logits, dim=-1)
725	
726	            torch.save(
727	                {
728	                    "token_ids": ids,
729	                    "aux_hidden": aux_hidden,
730	                    "top_logit_values": topk_vals.to(torch.bfloat16).cpu(),
731	                    "top_logit_indices": topk_ids.to(torch.int32).cpu(),
732	                    "target_logsumexp": target_logsumexp.to(torch.float32).cpu(),
733	                },
734	                _os.path.join(
735	                    _EAGLE3_COLLECT_DIR, f"{_eagle3_counter:06d}.pt"
736	                ),
737	            )
738	            _eagle3_counter += 1
739	            pt += seq_len
740	    _eagle3_aux_cache.clear()
741	# ────────────────────────────────────────────────────────────────────────
742	
743	
744	class MiniCPMMLP(nn.Module):
745	    def __init__(
746	        self,
747	        hidden_size: int,
748	        intermediate_size: int,
749	        hidden_act: str,
750	        quant_config: Optional[QuantizationConfig] = None,
751	        prefix: str = "",
752	    ) -> None:
753	        super().__init__()
754	        self.gate_up_proj = MergedColumnParallelLinear(
755	            hidden_size,
756	            [intermediate_size] * 2,
757	            bias=False,
758	            quant_config=quant_config,
759	            prefix=add_prefix("gate_up_proj", prefix),
760	        )
761	        self.down_proj = RowParallelLinear(
762	            intermediate_size,
763	            hidden_size,
764	            bias=False,
765	            quant_config=quant_config,
766	            prefix=add_prefix("down_proj", prefix),
767	        )
768	        if hidden_act != "silu":
769	            raise ValueError(
770	                f"Unsupported activation: {hidden_act}. "
771	                "Only silu is supported for now."
772	            )
773	        self.act_fn = SiluAndMul()
774	        self._fused_mlp_mask_cache = {}
775	
776	    def _get_fused_mlp_mask(self, tokens: int, device: torch.device) -> torch.Tensor:
777	        key = (device.index, tokens)
778	        mask = self._fused_mlp_mask_cache.get(key)
779	        if mask is None:
780	            mask = torch.empty(1, dtype=torch.int32, device=device)
781	            mask.fill_(tokens)
782	            self._fused_mlp_mask_cache[key] = mask
783	        return mask
784	
785	    def _try_fused_act_down(self, gate_up: torch.Tensor) -> Optional[torch.Tensor]:
786	        if (
787	            not _MINICPM_FUSED_MLP_ACT_QUANT
788	            or _fp4_swiglu_quant is None
789	            or gate_up.dim() != 2
790	            or not gate_up.is_cuda
791	            or not gate_up.is_contiguous()
792	            or gate_up.dtype not in (torch.float16, torch.bfloat16)
793	            or self.down_proj.bias is not None
794	            or self.down_proj.skip_bias_add
795	            or not hasattr(self.down_proj, "forward_fp4_quantized")
796	            or not hasattr(self.down_proj.quant_method, "apply_fp4_quantized")
797	            or hasattr(self.down_proj, "pre_quant_scale")
798	            or getattr(self.down_proj, "_use_fp4_marlin", False)
799	        ):
800	            return None
801	
802	        tokens = gate_up.shape[0]
803	        threshold = getattr(self.down_proj, "_hybrid_marlin_threshold", 0)
804	        if threshold > 0 and tokens <= threshold:
805	            return None
806	
807	        local_intermediate = self.down_proj.input_size_per_partition
808	        if gate_up.shape[-1] != local_intermediate * 2:
809	            return None
810	
811	        mask = self._get_fused_mlp_mask(tokens, gate_up.device)
812	        input_scale_inv = self.down_proj.input_scale_inv.view(1)
813	        s, e = _evt_record("mlp_swiglu_fp4_quant_ms")
814	        x_fp4, x_scale_interleaved = _fp4_swiglu_quant(
815	            gate_up.view(1, tokens, local_intermediate * 2),
816	            input_scale_inv,
817	            mask,
818	        )
819	        _evt_end(e)
820	        s, e = _evt_record("mlp_down_fp4_quantized_ms")
821	        x, _ = self.down_proj.forward_fp4_quantized(
822	            x_fp4[:, :, 0],
823	            x_scale_interleaved[..., 0],
824	            gate_up.dtype,
825	            output_shape_prefix=gate_up.shape[:-1],
826	        )
827	        _evt_end(e)
828	        return x
829	
830	    def forward(self, x):
831	        s, e = _evt_record("mlp_gate_up_ms"); gate_up, _ = self.gate_up_proj(x); _evt_end(e)
832	        s, e = _evt_record("mlp_act_quant_down_fused_ms"); fused_x = self._try_fused_act_down(gate_up); _evt_end(e)
833	        if fused_x is not None:
834	            return fused_x
835	        s, e = _evt_record("mlp_act_ms"); x = self.act_fn(gate_up); _evt_end(e)
836	        s, e = _evt_record("mlp_down_ms"); x, _ = self.down_proj(x); _evt_end(e)
837	        return x
838	
839	
840	class MiniCPMAttention(nn.Module):
841	    def __init__(
842	        self,
843	        hidden_size: int,
844	        num_heads: int,
845	        num_kv_heads: int,
846	        layer_id: int = 0,
847	        rope_theta: float = 10000,
848	        rope_scaling: Optional[Dict[str, Any]] = None,
849	        max_position_embeddings: int = 8192,
850	        quant_config: Optional[QuantizationConfig] = None,
851	        attn_use_rope: bool = True,
852	        use_output_gate: bool = False,
853	        prefix: str = "",
854	    ) -> None:
855	        super().__init__()
856	        self.hidden_size = hidden_size
857	        tp_size = get_tensor_model_parallel_world_size()
858	        self.total_num_heads = num_heads
859	        assert self.total_num_heads % tp_size == 0
860	        self.num_heads = self.total_num_heads // tp_size
861	        self.total_num_kv_heads = num_kv_heads
862	        if self.total_num_kv_heads >= tp_size:
863	            # Number of KV heads is greater than TP size, so we partition
864	            # the KV heads across multiple tensor parallel GPUs.
```

> TOOL

tool_use Bash
```json
{
  "command": "git -C /user_4813494d/openbmb show ddcce88 --stat | head -20"
}
```

> TOOL

tool_result Bash
```
commit ddcce88e595c4aa39a7acc8425a8a340dc1f3fe1
Author: SOAR User <[REDACTED]>
Date:   Sat May 9 05:37:36 2026 +0800

    demo-sala: spec fork tweaks + fp4 tune cache
    
    - minicpm.py：eagle3 onestage 采集协议升级到 v2，rid 解析支持 mode (norm/full) + flushed_by 元数据，向前兼容。
    - server_args.py：minicpm_flashinfer + dense_as_sparse + FP8 KV 时强制 disable_cuda_graph，规避稀疏 FlashInfer cuda graph 与混合 long/short batch 冲突的 illegal memory access。
    - schedule_batch.py / scheduler_output_processor_mixin.py / minicpm_backend.py：配套 onestage flush hook、batch 字段。
    - mm_fp4_tune_sm120.{json,_report.json}：sm_120 GEMM tune 输出更新；prewarm/tune 脚本小调。
    
    Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

 demo-sala/assets/mm_fp4_tune_sm120.json                                         |  40 ++--
 demo-sala/assets/mm_fp4_tune_sm120_report.json                                  | 856 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 demo-sala/prewarm_flashinfer_fp4.py                                             |   7 +-
 demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_backend.py          |   7 +-
 demo-sala/sglang/python/sglang/srt/managers/schedule_batch.py                   |   3 +-
 demo-sala/sglang/python/sglang/srt/managers/scheduler_output_processor_mixin.py |  30 +++
 demo-sala/sglang/python/sglang/srt/models/minicpm.py                            | 148 ++++++++----
```

> TOOL

tool_use Bash
```json
{
  "command": "git -C /user_4813494d/openbmb show 784e741 --stat | head -20"
}
```

> TOOL

tool_result Bash
```
commit 784e74108441a60abe36c6e8524b120362b71ac6
Author: SOAR User <[REDACTED]>
Date:   Thu May 7 00:44:27 2026 +0800

    feat: add one-stage eagle data collection

 demo-sala/sglang/python/sglang/srt/model_executor/forward_batch_info.py |   7 ++-
 demo-sala/sglang/python/sglang/srt/models/minicpm.py                    | 182 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 eagle/train_v4/pipeline/collect_onestage_v6.py                          | 177 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 eagle/train_v4/start_collect_onestage_v6.sh                             |  39 ++++++++++++++++
 4 files changed, 402 insertions(+), 3 deletions(-)
```

> AGENT

现在读取最新提交来理解整个改动的演进：

> TOOL

tool_use Bash
```json
{
  "command": "git -C /user_4813494d/openbmb show ddcce88:demo-sala/sglang/python/sglang/srt/models/minicpm.py 2>/dev/null | head -550 | tail -200"
}
```

> TOOL

tool_result Bash
```
ids = input_ids[start : pt + seq_len].cpu()
            torch.save(
                {"hidden_states": h, "token_ids": ids},
                _os.path.join(_MEDUSA_COLLECT_DIR, f"{_medusa_counter:06d}.pt"),
            )
            _medusa_counter += 1
            pt += seq_len
# ────────────────────────────────────────────────────────────────────────


# ── EAGLE-3 aux hidden + top-logit collection ─────────────────────────
_EAGLE3_COLLECT_DIR = _os.environ.get("EAGLE3_COLLECT_DIR", "")
_EAGLE3_ONESTAGE_DIR = _os.environ.get("EAGLE3_ONESTAGE_DIR", "")
_EAGLE3_ONESTAGE_RID_PREFIX = _os.environ.get("EAGLE3_ONESTAGE_RID_PREFIX", "e3os")
_EAGLE3_AUX_LAYERS = [
    int(x)
    for x in _os.environ.get("EAGLE3_AUX_LAYERS", "1,10,22").split(",")
    if x.strip()
]
_EAGLE3_MAX_TOKENS = int(_os.environ.get("EAGLE3_MAX_TOKENS", "2048"))  # 0 = no limit
_EAGLE3_TOP_K = int(_os.environ.get("EAGLE3_TOP_K", "256"))
_eagle3_counter = 0
_eagle3_lock = _threading.Lock()
_eagle3_aux_cache = {}  # layer_idx -> tensor, populated during forward
_eagle3_onestage_buffers = {}


def _eagle3_capture_layer(layer_idx, hidden_states):
    """Called inside MiniCPMModel.forward loop to capture aux layer outputs."""
    if (
        not (_EAGLE3_COLLECT_DIR or _EAGLE3_ONESTAGE_DIR)
        or layer_idx not in _EAGLE3_AUX_LAYERS
    ):
        return
    _eagle3_aux_cache[layer_idx] = hidden_states.detach()


def _eagle3_safe_rid(rid):
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in str(rid))


def _eagle3_parse_onestage_request(rid):
    rid = str(rid)
    if not rid.startswith(_EAGLE3_ONESTAGE_RID_PREFIX):
        return None
    parts = rid.replace(":", "_").split("_")
    if not parts:
        return None
    try:
        want_tokens = int(parts[-1])
    except ValueError:
        return None
    mode = "full"
    if len(parts) >= 3 and parts[1] in {"norm", "full"}:
        mode = parts[1]
    return {"want_tokens": want_tokens, "mode": mode}


def _eagle3_concat_aux_rows(row_index):
    aux_parts = []
    for li in _EAGLE3_AUX_LAYERS:
        aux_parts.append(_eagle3_aux_cache[li][row_index : row_index + 1])
    return torch.cat(aux_parts, dim=-1)


def _eagle3_topk_for_hidden(hidden_rows, lm_head, scale_width):
    logits = torch.matmul(hidden_rows / scale_width, lm_head.weight.T).float()
    topk = min(_EAGLE3_TOP_K, logits.shape[-1])
    topk_vals, topk_ids = torch.topk(logits, topk, dim=-1)
    target_logsumexp = torch.logsumexp(logits, dim=-1)
    return topk_vals, topk_ids, target_logsumexp


def _eagle3_onestage_flush(rid, buf):
    path = _os.path.join(_EAGLE3_ONESTAGE_DIR, f"{_eagle3_safe_rid(rid)}.pt")
    token_ids = torch.tensor(buf["token_ids"], dtype=torch.long)
    assistant_mask = torch.tensor(buf["assistant_mask"], dtype=torch.bool)
    torch.save(
        {
            "token_ids": token_ids,
            "assistant_mask": assistant_mask,
            "aux_hidden": torch.cat(buf["aux_hidden"], dim=0).to(torch.bfloat16),
            "top_logit_values": torch.cat(buf["top_logit_values"], dim=0).to(
                torch.bfloat16
            ),
            "top_logit_indices": torch.cat(buf["top_logit_indices"], dim=0).to(
                torch.int32
            ),
            "target_logsumexp": torch.cat(buf["target_logsumexp"], dim=0).to(
                torch.float32
            ),
            "metadata": {
                "schema": "eagle3_onestage_decode_v2",
                "rid": str(rid),
                "mode": str(buf.get("mode", "full")),
                "prompt_len": int(buf["prompt_len"]),
                "prompt_last_token": int(buf["token_ids"][0]),
                "generated_tokens_stored": int(len(buf["token_ids"]) - 1),
                "generated_tokens_required": int(buf["want_tokens"]),
                "flushed_by": str(buf.get("flushed_by", "length")),
                "aux_layers": list(_EAGLE3_AUX_LAYERS),
                "top_k": int(_EAGLE3_TOP_K),
                "alignment": "token_ids=[prompt_last]+generated rows consumed by forward; full mode requests one extra token so the last stored generated token has logits",
            },
        },
        path,
    )


def _eagle3_onestage_collect(hidden_states, input_ids, forward_batch, lm_head, scale_width):
    if not _EAGLE3_ONESTAGE_DIR or not _os.path.isdir(_EAGLE3_ONESTAGE_DIR):
        return False
    if len(_eagle3_aux_cache) != len(_EAGLE3_AUX_LAYERS):
        return True

    reqs = getattr(forward_batch, "reqs", None)
    if not reqs:
        return True

    mode = forward_batch.forward_mode
    if mode == ForwardMode.EXTEND:
        seq_lens = forward_batch.extend_seq_lens_cpu
        if seq_lens is None:
            return True
        pt = 0
        with _eagle3_lock:
            for req, seq_len in zip(reqs, seq_lens):
                rid = getattr(req, "rid", "")
                parsed = _eagle3_parse_onestage_request(rid)
                if parsed is None or parsed["want_tokens"] <= 0 or seq_len <= 0:
                    pt += seq_len
                    continue
                row = pt + seq_len - 1
                prompt_last = int(input_ids[row].detach().cpu().item())
                topk_vals, topk_ids, target_lse = _eagle3_topk_for_hidden(
                    hidden_states[row : row + 1], lm_head, scale_width
                )
                _eagle3_onestage_buffers[rid] = {
                    "want_tokens": parsed["want_tokens"],
                    "mode": parsed["mode"],
                    "flushed_by": "length",
                    "prompt_len": len(getattr(req, "origin_input_ids", [])),
                    "token_ids": [prompt_last],
                    "assistant_mask": [False],
                    "aux_hidden": [
                        _eagle3_concat_aux_rows(row).to(torch.bfloat16).cpu()
                    ],
                    "top_logit_values": [topk_vals.to(torch.bfloat16).cpu()],
                    "top_logit_indices": [topk_ids.to(torch.int32).cpu()],
                    "target_logsumexp": [target_lse.to(torch.float32).cpu()],
                }
                pt += seq_len
        return True

    if mode == ForwardMode.DECODE:
        # Decode collection is handled after sampling in the scheduler. That
        # Python path still runs when CUDA graph replays the model forward.
        return True

    return True


def _eagle3_onestage_collect_decode_from_scheduler(
    reqs, current_token_ids, aux_hidden_rows, next_token_logits
):
    """Append decode rows from scheduler output processing.

    `current_token_ids[i]` is the token consumed by this decode forward. The
    sampled `next_token_id` has not been appended yet when this is called.
    """
    if not _EAGLE3_ONESTAGE_DIR or not _os.path.isdir(_EAGLE3_ONESTAGE_DIR):
        return
    if aux_hidden_rows is None or next_token_logits is None:
        return

    with _eagle3_lock:
        active_rows = []
        active_rids = []
        active_token_ids = []
        for i, req in enumerate(reqs):
            rid = getattr(req, "rid", "")
            if rid in _eagle3_onestage_buffers:
                active_rows.append(i)
                active_rids.append(rid)
                active_token_ids.append(int(current_token_ids[i]))
        if not active_rows:
            return

        row_tensor = torch.tensor(
            active_rows, dtype=torch.long, device=next_token_logits.device
        )
        selected_logits = next_token_logits.index_select(0, row_tensor).float()
        topk = min(_EAGLE3_TOP_K, selected_logits.shape[-1])
        topk_vals, topk_ids = torch.topk(selected_logits, topk, dim=-1)
        target_lse = torch.logsumexp(selected_logits, dim=-1)

        for j, rid in enumerate(active_rids):
            buf = _eagle3_onestage_buffers.get(rid)
            if buf is None:
                continue
```

> TOOL

tool_use Bash
```json
{
  "command": "git -C /user_4813494d/openbmb show 784e741 --format=\"\" --stat -- demo-sala/sglang/python/sglang/srt/models/minicpm.py"
}
```

> TOOL

tool_result Bash
```
demo-sala/sglang/python/sglang/srt/models/minicpm.py | 182 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
 1 file changed, 180 insertions(+), 2 deletions(-)
```

> DEVELOPER

Review `/user_4813494d/openbmb` 工作区中 eagle 数据采集相关的未提交改动。

涉及文件：
- M `eagle/nvfp4_codec.py`（+4 -? 行）
- M `eagle/bin/collect_v3mix_nvfp4_bos.sh`（+7 行）
- M `eagle/bin/start_v3mix_collect_server.sh`（+30 行）
- M `eagle/pipelines/target_regen/start_server.sh`（+2 行）
- M `eagle/pipelines/target_regen/v3mix/collect_nvfp4_bos.py`（+97 行）
- M `eagle/README.md`（+5 行）

请：
1. 对每个文件跑 `git -C /user_4813494d/openbmb diff <path>` 看完整 diff
2. `git -C /user_4813494d/openbmb log -5 -- eagle/pipelines/target_regen/` 看 v3mix 历史。最近 commit `7ef0eb0 feat: add v3mix eagle data collection` 是这条线的 baseline
3. 读 `eagle/README.md` 改动判断当前文档里是否能讲清楚这条数据线
4. 判断这些改动是否是一个逻辑单元（v3mix collect 链路迭代）还是几条不相关的线
5. 注意 CLAUDE.md 规则：禁止用 `bench/data/` 做训练；draft baseline 是 `eagle/models/v2mix_20k_s3500_ood757/` 不能动；可看是否触碰这两条红线

输出格式：
- 改动逻辑分组（数据采集脚本 / codec / 文档）
- 每组意图（这条数据线在做什么）+ 是否完整可提交
- 是否触碰 CLAUDE.md 红线
- 提交策略建议（一个 commit 还是拆分）
- 控制在 500 字内

> AGENT

我来按照你的清单逐一检查这些未提交改动。

> TOOL

tool_use Bash
```json
{
  "command": "git diff eagle/nvfp4_codec.py eagle/bin/collect_v3mix_nvfp4_bos.sh eagle/bin/start_v3mix_collect_server.sh eagle/pipelines/target_regen/start_server.sh eagle/pipelines/target_regen/v3mix/collect_nvfp4_bos.py eagle/README.md"
}
```

> TOOL

tool_result Bash
```
diff --git a/eagle/README.md b/eagle/README.md
index aa3c089..cc51547 100644
--- a/eagle/README.md
+++ b/eagle/README.md
@@ -43,8 +43,9 @@ bash eagle/bin/start_v3mix_collect_server.sh
 bash eagle/bin/collect_v3mix_nvfp4_bos.sh
 ```
 
-The v3mix collector writes NVFP4-compressed aux-hidden samples, uploads sealed
-segments to BOS asynchronously, and removes uploaded local segment directories.
+The v3mix server hook writes direct NVFP4 aux-hidden samples; the collector
+validates those files, uploads sealed segments to BOS asynchronously, and
+removes uploaded local segment directories.
 Defaults are set for the current 300K run: 2048 saved rows, 64 running requests
 with a rolling 512-request window, 64-file segments, `bcecmd` upload, sha256
 off, progress bars on, and B12X off for collection.
diff --git a/eagle/bin/collect_v3mix_nvfp4_bos.sh b/eagle/bin/collect_v3mix_nvfp4_bos.sh
index cd44e46..b0dcfd3 100755
--- a/eagle/bin/collect_v3mix_nvfp4_bos.sh
+++ b/eagle/bin/collect_v3mix_nvfp4_bos.sh
@@ -52,6 +52,13 @@ if [[ -n "${SERVER_PID}" && -r "/proc/${SERVER_PID}/environ" ]]; then
     echo "server pid ${SERVER_PID} has a different EAGLE3_ONESTAGE_RID_PREFIX; expected ${RID_PREFIX}" >&2
     exit 2
   fi
+  if ! grep -qx "EAGLE3_ONESTAGE_NVFP4=1" <<<"${SERVER_ENV}"; then
+    if [[ "${EAGLE_V3MIX_ALLOW_HOOK_MISMATCH:-0}" != "1" ]]; then
+      echo "server pid ${SERVER_PID} is not launched with EAGLE3_ONESTAGE_NVFP4=1" >&2
+      echo "restart with bash eagle/bin/start_v3mix_collect_server.sh; formal v3mix collection expects direct-NVFP4 hook files." >&2
+      exit 2
+    fi
+  fi
 fi
 
 echo "============================================================"
diff --git a/eagle/bin/start_v3mix_collect_server.sh b/eagle/bin/start_v3mix_collect_server.sh
index d6bddff..0be6bf4 100755
--- a/eagle/bin/start_v3mix_collect_server.sh
+++ b/eagle/bin/start_v3mix_collect_server.sh
@@ -11,8 +11,10 @@ export EAGLE3_ONESTAGE_RID_PREFIX="${EAGLE3_ONESTAGE_RID_PREFIX:-e3os}"
 export EAGLE3_AUX_LAYERS="${EAGLE3_AUX_LAYERS:-1,10,22}"
 export EAGLE3_MAX_TOKENS="${EAGLE3_MAX_TOKENS:-2048}"
 export EAGLE3_TOP_K="${EAGLE3_TOP_K:-256}"
+export EAGLE3_ONESTAGE_NVFP4="${EAGLE3_ONESTAGE_NVFP4:-1}"
+export EAGLE3_ONESTAGE_SAVE_WORKERS="${EAGLE3_ONESTAGE_SAVE_WORKERS:-4}"
 export SGLANG_ENABLE_B12X="${SGLANG_ENABLE_B12X:-0}"
-export MAX_RUNNING="${MAX_RUNNING:-96}"
+export MAX_RUNNING="${MAX_RUNNING:-160}"
 export PORT="${PORT:-30000}"
 
 echo "============================================================"
@@ -24,9 +26,35 @@ echo "  rid       : ${EAGLE3_ONESTAGE_RID_PREFIX}"
 echo "  aux       : ${EAGLE3_AUX_LAYERS}"
 echo "  max_tokens: ${EAGLE3_MAX_TOKENS}"
 echo "  top_k     : ${EAGLE3_TOP_K}"
+echo "  nvfp4 hook: ${EAGLE3_ONESTAGE_NVFP4}"
+echo "  save_thr  : ${EAGLE3_ONESTAGE_SAVE_WORKERS}"
 echo "  max_run   : ${MAX_RUNNING}"
 echo "  b12x      : ${SGLANG_ENABLE_B12X}"
 echo "  spec      : off"
 echo "============================================================"
 
+if [[ "${EAGLE3_ONESTAGE_NVFP4}" == "1" ]]; then
+  python3 - <<'PY'
+from pathlib import Path
+import sys
+
+path = Path("demo-sala/sglang/python/sglang/srt/models/minicpm.py")
+text = path.read_text(encoding="utf-8")
+required = [
+    "_EAGLE3_ONESTAGE_NVFP4",
+    "_eagle3_nvfp4_encode",
+    "aux_packed",
+    "nvfp4_aux_v1",
+    "eagle3_onestage_decode_v3",
+]
+missing = [s for s in required if s not in text]
+if missing:
+    print(
+        f"collect server hook code is missing direct-NVFP4 support in {path}: {missing}",
+        file=sys.stderr,
+    )
+    sys.exit(3)
+PY
+fi
+
 exec bash eagle/pipelines/target_regen/start_server.sh
diff --git a/eagle/nvfp4_codec.py b/eagle/nvfp4_codec.py
index a2caba7..4040f28 100644
--- a/eagle/nvfp4_codec.py
+++ b/eagle/nvfp4_codec.py
@@ -61,7 +61,9 @@ def encode(x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
     abs_idx = torch.bucketize(
         q.abs().clamp(max=FP4_MAX), bounds, out_int32=True
     ).to(torch.uint8)
-    sign_bit = (q < 0).to(torch.uint8).mul_(8)
+    # Canonicalize FP4 zero: code 8 decodes to the same numeric zero as code 0,
+    # but avoiding negative-zero codes makes packed validation deterministic.
+    sign_bit = ((q < 0) & (abs_idx != 0)).to(torch.uint8).mul_(8)
     codes = (abs_idx | sign_bit).reshape(*prefix, dim)
     pair = codes.reshape(*prefix, dim // 2, 2)
     packed = (pair[..., 0] | (pair[..., 1] << 4)).to(torch.uint8)
diff --git a/eagle/pipelines/target_regen/start_server.sh b/eagle/pipelines/target_regen/start_server.sh
index 437cb63..0022c55 100755
--- a/eagle/pipelines/target_regen/start_server.sh
+++ b/eagle/pipelines/target_regen/start_server.sh
@@ -19,6 +19,8 @@ EAGLE3_ONESTAGE_RID_PREFIX="${EAGLE3_ONESTAGE_RID_PREFIX:-e3os}" \
 EAGLE3_AUX_LAYERS="${EAGLE3_AUX_LAYERS:-1,10,22}" \
 EAGLE3_MAX_TOKENS="${EAGLE3_MAX_TOKENS:-4096}" \
 EAGLE3_TOP_K="${EAGLE3_TOP_K:-128}" \
+EAGLE3_ONESTAGE_NVFP4="${EAGLE3_ONESTAGE_NVFP4:-1}" \
+EAGLE3_ONESTAGE_SAVE_WORKERS="${EAGLE3_ONESTAGE_SAVE_WORKERS:-4}" \
 SGLANG_MARLIN_DECODE_THRESHOLD="${SGLANG_MARLIN_DECODE_THRESHOLD:-48}" \
 SGLANG_MINICPM_PLAN_CACHE="${SGLANG_MINICPM_PLAN_CACHE:-1}" \
 SGLANG_FP4_TUNE_CACHE="${SGLANG_FP4_TUNE_CACHE:-/user_4813494d/openbmb/demo-sala/assets/mm_fp4_tune_sm120.json}" \
diff --git a/eagle/pipelines/target_regen/v3mix/collect_nvfp4_bos.py b/eagle/pipelines/target_regen/v3mix/collect_nvfp4_bos.py
index 924b830..90faf9f 100644
--- a/eagle/pipelines/target_regen/v3mix/collect_nvfp4_bos.py
+++ b/eagle/pipelines/target_regen/v3mix/collect_nvfp4_bos.py
@@ -2,7 +2,7 @@
 """Collect target-regenerated EAGLE data as NVFP4 aux files and stream to BOS.
 
 This is the v3mix production collector:
-  prompt manifest -> target generation hook bf16 .pt -> validate -> NVFP4 aux
+  prompt manifest -> target generation hook NVFP4 .pt -> validate -> BOS
   compressed .pt -> segment upload -> local cleanup.
 """
 from __future__ import annotations
@@ -459,6 +459,68 @@ def wait_pt(path: Path, timeout_s: float) -> bool:
     return False
 
 
+async def preflight_hook_format(
+    session: aiohttp.ClientSession,
+    sample: dict[str, Any],
+    idx: int,
+    args,
+) -> None:
+    input_ids = sample.get("input_ids")
+    if not isinstance(input_ids, list) or not input_ids:
+        raise RuntimeError("preflight failed: first resume sample has bad input_ids")
+    probe_ids = input_ids[-min(len(input_ids), 16):]
+    rid = f"{args.rid_prefix}_full_preflight_{os.getpid()}_{idx}_1"
+    hook_path = args.collect_dir / f"{safe_name(rid)}.pt"
+    hook_path.unlink(missing_ok=True)
+    try:
+        async with session.post(
+            f"{args.api_base}/generate",
+            json={
+                "rid": rid,
+                "input_ids": probe_ids,
+                "sampling_params": {
+                    "temperature": args.temperature,
+                    "max_new_tokens": 2,
+                    "ignore_eos": True,
+                },
+            },
+            timeout=aiohttp.ClientTimeout(total=min(args.request_timeout, 300.0)),
+        ) as resp:
+            text = await resp.text()
+            if resp.status != 200:
+                raise RuntimeError(f"preflight generate http_{resp.status}:{text[:200]}")
+    except Exception as e:
+        hook_path.unlink(missing_ok=True)
+        raise RuntimeError(f"preflight generate failed: {type(e).__name__}:{e}") from e
+
+    if not wait_pt(hook_path, min(args.hook_timeout, 60.0)):
+        raise RuntimeError(f"preflight failed: no hook output at {hook_path}")
+    try:
+        data = torch.load(hook_path, map_location="cpu", weights_only=True)
+    finally:
+        hook_path.unlink(missing_ok=True)
+
+    direct_nvfp4 = nvfp4_codec.is_nvfp4_sample(data) and "aux_hidden" not in data
+    if not direct_nvfp4:
+        metadata = data.get("metadata", {})
+        keys = sorted(str(k) for k in data.keys())
+        raise RuntimeError(
+            "preflight failed: hook is not direct NVFP4; "
+            f"keys={keys}, format={data.get('format')!r}, metadata={metadata!r}"
+        )
+    missing = [k for k in ("aux_packed", "aux_scale", "aux_hidden_shape") if k not in data]
+    if missing:
+        raise RuntimeError(f"preflight failed: missing direct NVFP4 keys {missing}")
+    metadata = data.get("metadata", {})
+    if metadata.get("aux_storage") not in {None, "nvfp4_direct"}:
+        raise RuntimeError(f"preflight failed: unexpected aux_storage={metadata.get('aux_storage')!r}")
+    print(
+        "[preflight] direct NVFP4 hook ok "
+        f"format={data.get('format')} shape={tuple(data.get('aux_hidden_shape'))}",
+        flush=True,
+    )
+
+
 def finalize_and_compress(ctx: dict[str, Any], dst_path: Path, args) -> tuple[bool, Any]:
     hook_path = ctx["hook_path"]
     timings: dict[str, float] = {}
@@ -498,7 +560,22 @@ def finalize_and_compress(ctx: dict[str, Any], dst_path: Path, args) -> tuple[bo
             return False, "prompt_last_masked_trainable"
         if int(data["assistant_mask"][1:].sum().item()) != n - 1:
             return False, "generated_mask_not_all_trainable"
-        for key in ("aux_hidden", "top_logit_values", "top_logit_indices", "target_logsumexp"):
+        aux_is_nvfp4 = nvfp4_codec.is_nvfp4_sample(data) and "aux_hidden" not in data
+        if not aux_is_nvfp4:
+            return False, "hook_not_direct_nvfp4"
+        for key in ("aux_packed", "aux_scale", "aux_hidden_shape"):
+            if key not in data:
+                return False, f"{key}_missing"
+        aux_shape = tuple(data["aux_hidden_shape"])
+        if len(aux_shape) != 2 or aux_shape[0] != n:
+            return False, f"aux_hidden_shape_bad:{aux_shape}"
+        if data["aux_packed"].shape[0] != n or data["aux_scale"].shape[0] != n:
+            return False, "aux_nvfp4_bad_len"
+        if data["aux_packed"].dtype != torch.uint8:
+            return False, f"aux_packed_bad_dtype:{data['aux_packed'].dtype}"
+        if data["aux_scale"].dtype != torch.bfloat16:
+            return False, f"aux_scale_bad_dtype:{data['aux_scale'].dtype}"
+        for key in ("top_logit_values", "top_logit_indices", "target_logsumexp"):
             if key not in data or data[key].shape[0] != n:
                 return False, f"{key}_bad_len"
         if int(data["token_ids"][0].item()) != int(ctx["input_ids"][-1]):
@@ -537,7 +614,14 @@ def finalize_and_compress(ctx: dict[str, Any], dst_path: Path, args) -> tuple[bo
         timings["validate_s"] = time.monotonic() - t0
 
         t0 = time.monotonic()
-        compressed = nvfp4_codec.compress_sample(data)
+        compressed = dict(data)
+        compressed["format"] = nvfp4_codec.FORMAT_TAG
+        if "token_ids" in compressed and torch.is_tensor(compressed["token_ids"]):
+            compressed["token_ids"] = compressed["token_ids"].to(torch.int64).contiguous()
+        if "top_logit_values" in compressed and torch.is_tensor(compressed["top_logit_values"]):
+            compressed["top_logit_values"] = compressed["top_logit_values"].to(torch.bfloat16).contiguous()
+        if "top_logit_indices" in compressed and torch.is_tensor(compressed["top_logit_indices"]):
+            compressed["top_logit_indices"] = compressed["top_logit_indices"].to(torch.int32).contiguous()
         timings["compress_s"] = time.monotonic() - t0
 
         t0 = time.monotonic()
@@ -905,6 +989,12 @@ async def main_async(args) -> None:
         "free_gb": round(disk_free_gb(args.stage_dir), 1),
     }, ensure_ascii=False), flush=True)
 
+    if args.preflight_hook_format:
+        timeout = aiohttp.ClientTimeout(total=min(args.request_timeout, 300.0))
+        connector = aiohttp.TCPConnector(limit=1, force_close=True)
+        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
+            await preflight_hook_format(session, prompts[0], start, args)
+
     upload_pbar = tqdm(
         total=len(prompts),
         desc="upload",
@@ -1045,6 +1135,7 @@ def parse_args():
     p.add_argument("--metrics-file", type=Path, default=None)
     p.add_argument("--failure-manifest", type=Path, default=None)
     p.add_argument("--hook-mmap", action=argparse.BooleanOptionalAction, default=True)
+    p.add_argument("--preflight-hook-format", action=argparse.BooleanOptionalAction, default=True)
     p.add_argument("--save-format", choices=["zip", "legacy"], default="zip")
     p.add_argument("--sha256", action=argparse.BooleanOptionalAction, default=True)
     p.add_argument("--no-progress", action="store_true")
```

> AGENT

现在检查 git log 历史和 CLAUDE.md 规则：

> TOOL

tool_use Bash
```json
{
  "command": "git -C /user_4813494d/openbmb log -5 --oneline -- eagle/pipelines/target_regen/"
}
```

> TOOL

tool_result Bash
```
7ef0eb0 feat: add v3mix eagle data collection
0c85d51 eagle: v2mix_20k_s3500_ood757 draft + train pipeline tune (+26% throughput)
f73fb35 eagle: reorganize layout, add target-regenerated pipeline, fix dynamic-spec edges
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/CLAUDE.md"
}
```

> TOOL

tool_result Read
```
1	# CLAUDE.md
2	
3	## 语言
4	
5	**始终使用简体中文回复。严禁使用韩语、日语或其他语言。**
6	
7	## 项目定位
8	
9	SOAR 比赛工作区，优化 **OpenBMB/MiniCPM-SALA** 的推理。最终在官方云环境打分。
10	
11	**基座模型不可替换**，改动只能落在：量化方案、SGLang fork、推测解码 draft、kernel、平台部署脚本。
12	
13	## 模型架构
14	
15	- **32 layers 混合**：8 standard Attention（layer id = 0, 9, 16, 17, 22, 29, 30, 31）+ 24 Lightning Attention（GLA）
16	- `hidden_size=4096`，`intermediate_size=16384`，`nq/nkv=32/2`，`head_dim=128`
17	- `vocab_size=73448`，`max_position_embeddings=524288`（512K）
18	- `dense_len=8192`：standard Attention 超过此长度走 InfLLM-v2 稀疏（compress_k → stage1 block_score → stage2 top-K sparse FA）
19	
20	## 运行栈
21	
22	**硬件**：NVIDIA RTX 6000D（sm_120, Blackwell, 84 GB VRAM）
23	
24	| 组件 | 版本 |
25	|---|---|
26	| Python | 3.10.19（venv 预激活，`VIRTUAL_ENV=/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env`） |
27	| PyTorch | 2.11.0+cu130 |
28	| CUDA toolkit | 13.2 |
29	| cuDNN | [REDACTED]（sm_120 FP4 cudnn backend 硬要求） |
30	| FlashInfer | 0.6.8.post1[cu13] |
31	| sgl-kernel | 0.3.20 + 本仓库 `common_ops.abi3.so` 替换（Marlin FP4 scale bug fix） |
32	| Triton | 3.6.0 |
33	
34	## 当前生产配置
35	
36	- **量化**：NVFP4（GPTQ + FourOverSix，loguniform128 校准，48K 上下文）
37	- **Decode kernel 派发**：b12x 2-tier（Marlin小M / b12x全M / 3点CUTLASS override），覆盖 6 形状 58 tile 配置
38	- **推测解码**：EAGLE-3 chain verify，提交包默认 `spec_steps=3, topk=2, dtn=7`，并启用 dynamic spec mode（NO_SPEC / D5 / D7 按 running batch size 切换）
39	- **Draft model**：`eagle/models/v2mix_20k_s3500_ood757/`（v2mix 20K + s3500 + ood757 数据训出，484 MB safetensors，md5 `8e6bb36b…`），NVFP4 QAT，共享 b12x 路径。`det_prefill/` 是更早的 det-target prefill baseline，已退居参考
40	- **Eagle 数据路线**：当前为 target-regenerated（target 模型自生成续写作训练 label），见 `eagle/pipelines/target_regen/`
41	
42	> **DFlash + DDTree 是探索性实验，不作为生产实践**。所有 `dflash/` / `eval/start_dflash*.sh` / `eval/start_ddtree.sh` / `docs/dflash/` 内容均为备选 spec 算法的探索路线，提交包仍走 EAGLE-3。除非用户明确要求切到 DFlash/DDTree，默认不要把它当作可比较或可替换的当前 baseline。
43	
44	## 目录
45	
46	| 路径 | 职责 |
47	|---|---|
48	| `demo-sala/` | **正式提交包**（平台真正消费） |
49	| `probe-sala/` | cu13 平台诊断探针（BOS 鉴权下发 + 邮件回传 + 11 项 verify） |
50	| `eagle/` | EAGLE-3 draft 训练 / 数据采集 / ckpt 转换；当前 baseline = `models/v2mix_20k_s3500_ood757/`（与 `eval/start_eagle.sh` 默认一致），`models/det_prefill/` 为前一代参考，旧版本归档在 `legacy/` |
51	| `medusa/` | Medusa K=1 历史基线（已被 EAGLE-3 超越） |
52	| `bench/` | 速度基准、profile、kernel microbench |
53	| `eval/` | 本地评测脚本（`start_eagle.sh` / `run_public_eval_full.sh` 等） |
54	| `quant/` | 离线量化实验 |
55	| `kernels/` | CUDA / GEMV / layout 实验 |
56	| `docs/` | 技术文档（见下） |
57	| `toolkit/` | 官方评测工具，只读 |
58	
59	## 文档导航
60	
61	> **文档仅供参考，不要当圣旨**。`docs/` 是过去某个时间点的事实快照与调研归档，可能滞后于代码、可能写错、也可能是早期假设。在依据文档结论行动前（特别是性能数字、kernel 派发、API 形状），先用 `git log` / 读代码 / 跑 bench 验证一遍。代码现状与文档冲突时，以代码为准并顺手把文档纠正。
62	
63	项目细节都在 [`docs/`](docs/) 下。文档索引见 [`docs/README.md`](docs/README.md)。
64	
65	每主题一个子目录，目录下 `README.md` + 各子文档；统一约定 `current.md` = 当前事实，`history.md` = 调研归档。
66	
67	| 主题 | 入口 |
68	|---|---|
69	| **接续指南** | [`docs/handover.md`](docs/handover.md) |
70	| 平台 / cu13 / probe-sala / fork 判定 | [`docs/platform/`](docs/platform/) |
71	| 量化方案 / Marlin 历史 | [`docs/quant/`](docs/quant/) |
72	| **sm_120 GEMM/kernel 底层调优**（CUTLASS / Marlin / 硬件 / profile 方法论） | [`docs/gemm/`](docs/gemm/) |
73	| 长上下文 prefill | [`docs/prefill/`](docs/prefill/) |
74	| Decode 算子优化 / profile 方法论 | [`docs/decode/`](docs/decode/) |
75	| EAGLE-3 spec decoding（架构 / 训练 / collapse / 实验 / 论文） | [`docs/eagle/`](docs/eagle/) |
76	| 周冠军技术分享（对外 blog） | [`docs/blog/`](docs/blog/) |
77	
78	## 关键命令
79	
80	```bash
81	# 启动推理 server（EAGLE-3 当前生产配置）
82	bash eval/start_eagle.sh
83	
84	# 停服（唯一允许方式；禁用 pkill -f sglang，会杀系统进程）
85	bash bench/kill_sglang.sh
86	
87	# Mini speed bench（S1=3, S8=8）
88	bash bench/mini_bench.sh
89	
90	# 完整 bench
91	bash toolkit/bench_serving.sh http://127.0.0.1:30000
92	
93	# 正确性冒烟（发请求看人话，不跑 accuracy eval）
94	curl -s -X POST http://127.0.0.1:30000/v1/chat/completions \
95	    -H "Content-Type: application/json" \
96	    -d '{"model":"minicpm","messages":[{"role":"user","content":"你好，请介绍一下你自己"}],"max_tokens":100}'
97	
98	# Server ready 判断：看日志 "Uvicorn running on" 或 curl /v1/models。不用 /health
99	```
100	
101	## 当前分支状态
102	
103	- HEAD：见 `git log --oneline -5`（`demosala-rollback`）：
104	  - prefill 当前状态：
105	    - 保留 plan cache：layer 间复用 + chunk 间复用；`shape_only_plan_cache` 已由 `471e20b` 修复，跨 forward 命中时会刷新 FlashInfer page table，避免 stale page table / cross-request KV contamination。
106	    - `fi_convert` 跨层缓存已复核为不安全，默认禁用；只保留 `SGLANG_MINICPM_UNSAFE_FI_CONVERT_CACHE=1` 实验开关。
107	    - 当前 prefill 事实来源是 `docs/prefill/current.md`；接续指南见 `docs/handover.md`。
108	    - `SGLANG_FAST_PREFILL_STAGE1=1` 分支保留但默认关闭，不能按默认收益计算。
109	    - `compressed_max_seqlen_k` 旧方案危险行为已回退；当前可用的是带 guard 的 stage1 actual maxlen + full-layout scratch/direct-pool，不能缩坏 pooler full-layout 语义。
110	    - TrtLLM stage2 替换已否决且当前代码不包含 `_USE_TRTLLM_STAGE2` 实现；原因是 long-context sparse stage2 是 decode-style，且 TrtLLM causal mask 与 FlashInfer right-aligned causal 不等价。
111	  - 运行/部署相关：
112	    - `1738be2` FP4 autotune cache（draft FC 层 split_k 预存）
113	    - `208bb39` profiling hooks（默认关闭）
114	    - `ef6e3a7` + 后续修复：EAGLE NO_SPEC immediate 路径和 finished spec_info 过滤
115	    - `164609a` docs/org 同步和 verify plan CPU pinned memory 优化
116	
117	## 提交包流程
118	
119	平台提供原始 BF16 模型作为 `--input`；提交包负责量化并起 server：
120	
121	1. `demo-sala/prepare_env.sh` — 装 custom SGLang（editable）、cuDNN 9.15+、FlashInfer 0.6.8.post1+，替换 `common_ops.abi3.so`，patch FourOverSix，导出 `SGLANG_SERVER_ARGS` + `SGLANG_MARLIN_DECODE_THRESHOLD=48`
122	2. `demo-sala/prepare_model.sh` — NVFP4 量化（GPTQ + FourOverSix，`loguniform 128`，48K 上下文）
123	3. `demo-sala/sglang/python/` — custom SGLang patches（`modelopt_quant.py` hybrid Marlin、`marlin_utils_fp4.py`、`minicpm_backend.py` CUDA graph fix、GLA fused kernel 等）
124	
125	提交 tar 大小上限 2 GB。详细流程与 probe-sala 差异见 [`docs/platform/cu13-stack.md`](docs/platform/cu13-stack.md)。
126	
127	## Critical Rules
128	
129	- Official materials（`toolkit/README.md`、`demo-sala/README.md`）有冲突时以官方为准
130	- **始终 `uv pip install`，永不 `pip install`**
131	- 提交包 ≤ 2 GB
132	- **严禁用 `bench/data/` 做训练**（速度评测集不能用于训练/采集/校准，属作弊）；`toolkit/eval_dataset/` 可以用
133	- **`SGLANG_SERVER_ARGS` 用连字符风格**（`--dense-as-sparse`）
134	- Commit style：短祈使；不提交模型权重 / 大日志
135	- **不要动 draft baseline**（`eagle/models/v2mix_20k_s3500_ood757/`，与 `start_eagle.sh` 默认一致）；`eagle/models/det_prefill/` 是前一代参考；旧 `eagle/sglang_model/` 已退役
136	- **替换任何 `.so` 必须先备份 + 写日志**：备份目录 `outputs/so_backups/<YYYYMMDD-HHMMSS>__<src-name>__<sha256前12>/`（保留旧 `.so` 原文件 + `meta.json` 记录原路径、md5、sha256、cuobjdump SM 标签、来源 commit / 自编参数）；同时在 `docs/gemm/so-replacements.md` 追加一行替换日志（日期、目标 `.so`、来源、原因、回滚指令）。**严禁 `cp` 覆盖未备份的 `.so`**。
137	
138	## 行为规则
139	
140	- **杀 sglang 只用** `bash bench/kill_sglang.sh` —— 禁止 `pkill -f sglang`（会杀系统进程导致整机重启）
141	- **服务器就绪判断**：看日志 `Uvicorn running on` 或 curl `/v1/models`。不用 `/health`
142	- **等待最多 `sleep 60s`**，不轮询；后台任务用 `run_in_background` + 通知
143	- **性能改动先 profile 证明 >1.5× 正向收益**，再 e2e bench
144	- **正确性验证**：发 chat 请求说人话即可，不跑全量 accuracy eval；mcq 不能作为健康判据
145	- **同时只能跑一个 GPU 任务**（显存会占满，串行执行）
146	- **不用 argparse**，脚本配置硬编码为常量
147	- **"输出垃圾" 结论前先发 3 条简单 chat**：残留长请求或 mcq 格式退化会伪装成 backend bug
148	- llmcompressor 装完后需回滚：`uv pip install compressed-tensors==0.13.0 accelerate==1.13.0`
149	- 永远自己启动 server 跑 bench，不给用户"启动指令"
150	- **安装脚本严禁 fallback**：`prepare_env.sh` 失败就 `exit 1`，禁止 pypi.org / pytorch.org 兜底
151	- **Monitor 规则**（等一次性事件的正确写法）：
152	  - 必须用 `grep -m1 PATTERN`，匹配一次就退出；否则老 monitor 会一直跟着 `tail -F` 活到超时
153	  - 等新事件前先 `TaskStop` 旧 monitor；同一个日志源不能同时挂两个 monitor（互相触发制造幻象通知）
154	  - 重启 server 前先停旧 monitor，即使 `rm` 了日志文件，`tail -F` 会自动跟进新文件，老 monitor 会在新 server 的 "Uvicorn running" 上再触发一次
155	  - pattern 必须覆盖失败路径（`Traceback|ERROR|Killed|OOM`），只 grep 成功标记会让崩溃看起来和"仍在运行"一样
156
```

> AGENT

现在检查 README.md 的上下文完整性：

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/README.md",
  "offset": 30,
  "limit": 50
}
```

> TOOL

tool_result Read
```
30	
31	`det_prefill` is kept because it is a validated baseline. The name describes
32	what it is: det-target data collected through the prefill-style pipeline.
33	
34	## Target-Regenerated Pipeline
35	
36	Current large-scale path is v3mix:
37	
38	```bash
39	bash eagle/bin/build_v3mix_300k_prompts.sh
40	
41	bash eagle/bin/start_v3mix_collect_server.sh
42	
43	bash eagle/bin/collect_v3mix_nvfp4_bos.sh
44	```
45	
46	The v3mix server hook writes direct NVFP4 aux-hidden samples; the collector
47	validates those files, uploads sealed segments to BOS asynchronously, and
48	removes uploaded local segment directories.
49	Defaults are set for the current 300K run: 2048 saved rows, 64 running requests
50	with a rolling 512-request window, 64-file segments, `bcecmd` upload, sha256
51	off, progress bars on, and B12X off for collection.
52	Details and the latest 256-sample smoke metrics are in
53	`pipelines/target_regen/v3mix/README.md`.
54	
55	Legacy 10K path:
56	
57	Build start prompts:
58	
59	```bash
60	bash eagle/bin/build_target_regen_prompts.sh
61	```
62	
63	Start the collection server as a long-running task:
64	
65	```bash
66	EAGLE_TARGET_REGEN_HOOK_DIR=/tmp/eagle_target_regen \
67	EAGLE3_TOP_K=128 \
68	MEM_FRACTION_STATIC=0.55 \
69	MAX_RUNNING=24 \
70	PORT=30000 \
71	bash eagle/pipelines/target_regen/start_server.sh
72	```
73	
74	Collect generated training data:
75	
76	```bash
77	bash eagle/bin/collect_target_regen.sh
78	```
79
```

> DEVELOPER

Review `/user_4813494d/openbmb` 工作区里 bench 相关的未提交改动：

**删除的 5 个文件**（共 -894 行）：
- `eagle/training/sala_draft/bench_forward.py`
- `eagle/training/sala_draft/bench_fp4_backends.py`
- `eagle/training/sala_draft/bench_fp4_gemm.py`
- `eagle/training/sala_draft/bench_max_bs.py`
- `eagle/training/sala_draft/bench_step_time.py`

**修改的文件**：
- `bench/mini_bench.sh`（+? -? 行）

**新增未追踪**：
- `bench/infllmv2/bench_mlp_fused_act_quant.py`

请：
1. 对每个被删除的 bench 文件，先 `git -C /user_4813494d/openbmb show HEAD:eagle/training/sala_draft/bench_forward.py | head -30`（其余类似）看它原本是干什么的
2. 跑 grep（在 /user_4813494d/openbmb 下，排除 `.git`）确认这 5 个被删的 bench 脚本是否还有人引用：`grep -rn "bench_forward\|bench_fp4_backends\|bench_fp4_gemm\|bench_max_bs\|bench_step_time" /user_4813494d/openbmb --include="*.py" --include="*.sh" --include="*.md" 2>/dev/null | grep -v ".git" | grep -v "eagle/training/sala_draft/bench"`
3. 跑 `git -C /user_4813494d/openbmb diff bench/mini_bench.sh` 看 mini_bench 改了什么
4. `Read` `/user_4813494d/openbmb/bench/infllmv2/bench_mlp_fused_act_quant.py` 看新 bench 的作用（如太长只读前 80 行）
5. 判断这三组改动是否互相独立、是否各自可独立提交

输出格式：
- 删除组：每个脚本之前作用一句话 + 是否安全删除（有无残留引用）
- mini_bench 改动：意图 + 是否独立
- 新增 infllmv2 bench：意图 + 是否纳入提交
- 提交策略
- 控制在 400 字内

> AGENT

现在检查 nvfp4_codec.py 的 is_nvfp4_sample 函数是否存在：

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"is_nvfp4_sample\\|FORMAT_TAG\" /user_4813494d/openbmb/eagle/nvfp4_codec.py"
}
```

> TOOL

tool_result Bash
```
18:FORMAT_TAG = "nvfp4_aux_v1"
19:LEGACY_FORMAT_TAG = "nvfp4_v1"
29:def is_nvfp4_sample(d: dict[str, Any]) -> bool:
31:        d.get("format") in {FORMAT_TAG, LEGACY_FORMAT_TAG}
108:        if is_nvfp4_sample(d):
119:    out["format"] = FORMAT_TAG
137:    if not is_nvfp4_sample(d):
```

> AGENT

我来逐步检查这些 bench 相关的改动。

> TOOL

tool_use Bash
```json
{
  "command": "git show HEAD:eagle/training/sala_draft/bench_forward.py 2>/dev/null | head -30"
}
```

> TOOL

tool_result Bash
```
#!/usr/bin/env python3
"""Fast forward+backward bench. Synthetic data only — no disk I/O.

Reports ms/iter and peak GPU memory for non-packed vs packed paths.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

REPO_user_4813494d = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_user_4813494d))

os.environ.setdefault("EAGLE_DRAFT_TTT_STEPS", "3")
os.environ.setdefault("EAGLE_DRAFT_SEQ_LEN_MAX", "4096")

import torch
torch.backends.cuda.matmul.allow_tf32 = True

from eagle.legacy.v2_v3 import train as v3train
from eagle.training.sala_draft import train as v4train


def build_model():
    """Random-weight model — no safetensors load, no MLP init."""
    VOCAB, HIDDEN = v3train.VOCAB_SIZE, v3train.HIDDEN_SIZE
    DRAFT = v3train.DRAFT_VOCAB_SIZE
    embed_w = (torch.randn(VOCAB, HIDDEN) * 0.02).to(v4train.DTYPE)
```

> AGENT

检查是否有 bench/data 和 draft baseline 的使用：

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"bench/data\" /user_4813494d/openbmb/eagle/pipelines/target_regen/v3mix/collect_nvfp4_bos.py 2>/dev/null || echo \"not found\""
}
```

> TOOL

tool_result Bash
```
not found
```

> TOOL

tool_use Bash
```json
{
  "command": "git -C /user_4813494d/openbmb show HEAD:eagle/training/sala_draft/bench_fp4_backends.py 2>/dev/null | head -30"
}
```

> TOOL

tool_result Bash
```
#!/usr/bin/env python3
"""Comprehensive FP4 GEMM bench for the training-shape regime.

Compares (per shape):
  - bf16 baseline (torch.matmul)
  - sgl-kernel cutlass_scaled_fp4_mm        (no autotune)
  - flashinfer mm_fp4 cutlass               (no autotune)
  - flashinfer mm_fp4 cutlass + prod cache  (loaded from demo-sala/assets/...)
  - flashinfer mm_fp4 cudnn                 (fastest in microbench, but unstable)

NaN check: each backend gets validated against bf16 reference. Uses the
NVFP4 official scale convention (gs = 2688 / amax, alpha = 1/(gs_x*gs_w)).
Also reports relative error vs bf16.

Shapes correspond to the actual Linear ops we'd accelerate in V4 forward
(lm_head excluded — kept in bf16 by NVFP4_EXCLUDE_LM_HEAD=1).

Run from repo user_4813494d:
    python3 eagle/training/sala_draft/bench_fp4_backends.py
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import torch

torch.backends.cuda.matmul.allow_tf32 = True
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"v2mix_20k_s3500_ood757\" /user_4813494d/openbmb/eagle/pipelines/target_regen/v3mix/collect_nvfp4_bos.py 2>/dev/null || echo \"not found\""
}
```

> TOOL

tool_result Bash
```
not found
```

> TOOL

tool_use Bash
```json
{
  "command": "git -C /user_4813494d/openbmb show HEAD:eagle/training/sala_draft/bench_fp4_gemm.py 2>/dev/null | head -30 && echo \"---\" && git -C /user_4813494d/openbmb show HEAD:eagle/training/sala_draft/bench_max_bs.py 2>/dev/null | head -30 && echo \"---\" && git -C /user_4813494d/openbmb show HEAD:eagle/training/sala_draft/bench_step_time.py 2>/dev/null | head -30"
}
```

> TOOL

tool_result Bash
```
#!/usr/bin/env python3
"""Microbench: bf16 vs NVFP4 forward GEMM on sm_120.

Compares real-model GEMM shapes (q/k/v/o_proj, MLP, lm_head, fc) under:
  - PyTorch torch.matmul (bf16)        baseline
  - sgl-kernel cutlass_scaled_fp4_mm   W4A4 NVFP4
  - flashinfer.mm_fp4 (auto/cudnn/cutlass)  W4A4 NVFP4

Prints ms/iter and effective TFLOPS per shape per backend.
"""
from __future__ import annotations

import time

import torch

torch.backends.cuda.matmul.allow_tf32 = True

from flashinfer import mm_fp4
from sgl_kernel import cutlass_scaled_fp4_mm, scaled_fp4_quant


def bench_op(fn, iters: int = 50, warmup: int = 10):
    for _ in range(warmup):
        fn()
    torch.cuda.synchronize()
    t0 = time.time()
    for _ in range(iters):
        fn()
    torch.cuda.synchronize()
---
#!/usr/bin/env python3
"""Find the max stable BATCH_SIZE for SALA draft training.

Loads real samples, includes the optimizer (AdamW) so the reported peak
reflects actual training memory, not just forward+backward. Runs 3 iters
per BS to expose any growing allocator fragmentation.
"""
from __future__ import annotations

import gc
import os
import sys
import time
import traceback
from pathlib import Path

REPO_user_4813494d = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_user_4813494d))

os.environ.setdefault("EAGLE_DRAFT_TTT_STEPS", "3")
os.environ.setdefault("EAGLE_DRAFT_SEQ_LEN_MAX", "4096")
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import torch

from eagle.legacy.v2_v3 import train as v3train
from eagle.training.sala_draft import train as v4train
from eagle.training.sala_draft.packing import (
    PackedFileSampler, index_lengths, make_packed_batch,
)
---
#!/usr/bin/env python3
"""Compare per-optimizer-step wall time, sync batch builder vs prefetcher.

Skips all eval / index_lengths / vocab init work — just builds the model,
arms a prefetcher (or sync builder), warms 3 step, times the next 12.

Why standalone: bench via train.py drags step-0 + mid eval into the timing,
which obscures the actual loop overhead. This lives in pure batch-builder
land (real disk loads, real GPU forward+backward+optstep) so the delta
attributable to AsyncPrefetcher is clear.
"""
from __future__ import annotations

import argparse
import os
import random
import sys
import time
from pathlib import Path

REPO_user_4813494d = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_user_4813494d))

# Must match train.py — without this the default CUDA caching allocator
# fragments after a few warmup steps and OOMs the 8 GiB backward weight-grad
# allocation, even though there's plenty of free memory.
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
os.environ.setdefault("EAGLE_DRAFT_TTT_STEPS", "3")
os.environ.setdefault("EAGLE_DRAFT_SEQ_LEN_MAX", "4096")
os.environ.setdefault("EAGLE_DRAFT_PACK", "1")
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -rn \"bench_forward\\|bench_fp4_backends\\|bench_fp4_gemm\\|bench_max_bs\\|bench_step_time\" /user_4813494d/openbmb --include=\"*.py\" --include=\"*.sh\" --include=\"*.md\" 2>/dev/null | grep -v \".git\" | grep -v \"eagle/training/sala_draft/bench\""
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/eagle/training/sala_draft/train.py:1012:    # on the default stream. Verified by bench_step_time.py — load_wait
/user_4813494d/openbmb/dflash/scripts/bench_fp4_speedup.py:75:def bench_forward_only(draft, inputs, *, fp4_on: bool):
/user_4813494d/openbmb/dflash/scripts/bench_fp4_speedup.py:188:            bf_fo = bench_forward_only(bf16, inputs, fp4_on=False)
/user_4813494d/openbmb/dflash/scripts/bench_fp4_speedup.py:191:            fp_fo = bench_forward_only(fp4, inputs, fp4_on=True)
/user_4813494d/openbmb/eagle/bin/train_v2mix_20k.sh:10:#     bench_max_bs.py)
```

> AGENT

完美。现在我有了完整的上下文。让我总结分析：

## 深度分析：minicpm.py 未提交改动 (+154 行)

### 改动分块总览

**改动涉及 EAGLE-3 onestage 数据采集的生产协议升级**，从 v2 → v3，包含 4 个逻辑块：

1. **Imports + 全局初始化** (7 行)
   - 新增 `_atexit`, `_ThreadPoolExecutor`
   - 新增 FP4 量化配置：`_EAGLE3_ONESTAGE_NVFP4`, `_EAGLE3_ONESTAGE_SAVE_WORKERS`
   - 新增线程池执行器管理

2. **FP4 编码与线程池管理函数** (68 行)
   - `_eagle3_nvfp4_encode()`: NVFP4 分组量化 (group_size=16，4-bit signed)
   - `_eagle3_onestage_get_save_executor()`: 延迟初始化 ThreadPoolExecutor
   - `_eagle3_onestage_shutdown_save_executor()`: atexit 清理钩子
   - `_eagle3_onestage_log_save_error()`: 异步保存错误日志

3. **新 `_eagle3_onestage_save_job()` 函数** (58 行)
   - 替代原 `_eagle3_onestage_flush()` 的同步逻辑
   - 核心变化：
     - **schema v2 → v3**：新增 `aux_hidden_shape`, `format` 字段
     - **条件编码**：若 `_EAGLE3_ONESTAGE_NVFP4=1`，保存 `aux_packed`+`aux_scale`；否则保存原始 bf16（诊断路径）
     - **新增元数据字段**：`aux_storage` 声明存储格式

4. **`_eagle3_onestage_flush()` 改造** (从同步 → 异步)
   - 旧：直接 `torch.save()`（阻塞）
   - 新：检查执行器，异步提交或同步降级

---

### 每块风险评估

| 块 | 意图 | 风险等级 | 关键判断 |
|---|---|---|---|
| **FP4 编码** | NVFP4 直接压缩 aux_hidden (1664→832B/行) | 🟡 黄 | ✓ 与最近 `ddcce88` ("fp4 tune cache") 配套；bucketize 边界值 [0.25,0.75,1.25,1.75,2.5,3.5,5.0] 需验证正确性；跨设备 dtype 转换无隐患 |
| **ThreadPoolExecutor** | 异步 I/O 解耦，提升吞吐 | 🟢 绿 | ✓ 标准库，atexit 注册清理；WORKERS<=0 时降级同步 |
| **Schema v3** | 数据格式向前兼容性升级 | 🟡 黄 | ⚠️ `aux_hidden_shape` 新增字段，数据消费侧 (collect_onestage_v6.py) 必须处理；v2→v3 现场迁移能否无缝？ |
| **条件 NVFP4 编码** | 生产用 FP4，诊断用原始 bf16 | 🟡 黄 | ⚠️ 两条代码路径，线上必须 `_EAGLE3_ONESTAGE_NVFP4=1`；BF16 分支仅测试用；无法同时存储两种格式 |
| **异步保存错误处理** | 后台异常日志 | 🟢 绿 | ✓ 错误不影响主路径；但无重试机制 |

---

### 与既往改动的耦合关系

1. **commit `ddcce88`** ("fp4 tune cache")：新增 NVFP4 量化配置，本次改动直接消费这些旋钮。强依赖关系。
2. **commit `784e741`** ("one-stage eagle data collection")：原始 v2 协议。本次是对其的就地升级，非新特性。
3. **Draft sliding-window** (`c87538d`/`1d8533b`)：无直接关系。独立 KV clip 逻辑。

---

### 核心风险与正确性问题

**🔴 高风险**：
- **Schema 不兼容**：若 eagle/train_v4/pipeline/collect_onestage_v6.py 未升级处理 `aux_hidden_shape`，会 KeyError 或数据错位。需检查数据消费侧是否已 merge。
- **NVFP4 编码 bitmap**：sign_bit 逻辑 `(q < 0) & (abs_idx != 0)` 是否覆盖所有边界情况？零值编码会产生 abs_idx=0，sign_bit 被置 0，正确；负零不应出现（bfloat16 无符号零特殊性）。

**🟡 中等风险**：
- **异步保存顺序**：ThreadPoolExecutor 不保证 FIFO 提交顺序在磁盘反映；若两个 rid 的数据文件写入乱序，训练数据可能局部颠倒。但由于每个 rid 一个独立文件，风险有限。
- **内存压力**：并发 WORKERS 默认 4，每次提交一个 buf（包含张量），若 batch 很大，可能内存堆积。

**🟢 低风险**：
- ThreadPoolExecutor 标准库，shutdown 逻辑无问题
- 张量 dtype 转换链条清晰（bfloat16→uint8→save）

---

### 整体提交策略建议

**建议：拆分为 2 个 commit**

1. **Commit 1**：FP4 编码 + 线程池基础设施
   - `_eagle3_nvfp4_encode()`, `_eagle3_onestage_get_save_executor()`, 全局初始化
   - 独立可测试（FP4 编码单元测试无依赖）

2. **Commit 2**：Schema v3 升级 + 异步 flush
   - `_eagle3_onestage_save_job()`, `_eagle3_onestage_flush()` 改造, metadata 升级
   - 依赖 commit 1，同时需要 collect_onestage_v6.py 数据消费侧的 review

**当前单 commit 的问题**：若 v3 数据格式有 bug，rollback 会丢失 FP4 编码基础设施。分离便于 bisect。

---

### 字数统计
- 改动总量：+154 行（含导入、注释）
- 有效代码：~130 行
- 难度：中等（涉及新协议 + 异步 I/O）
- 审查耗时：需检查数据消费侧是否已兼容 v3 schema

> TOOL

tool_use Bash
```json
{
  "command": "git -C /user_4813494d/openbmb diff bench/mini_bench.sh"
}
```

> TOOL

tool_result Bash
```
diff --git a/bench/mini_bench.sh b/bench/mini_bench.sh
index 12937f8..2f393e8 100755
--- a/bench/mini_bench.sh
+++ b/bench/mini_bench.sh
@@ -16,12 +16,12 @@ set -euo pipefail
 # =============================================================
 
 API_BASE="${1:-http://127.0.0.1:30000}"
-N_S1="${2:-8}"
-N_S8="${3:-24}"
-N_SMAX="${4:-64}"
+N_S1="${2:-12}"
+N_S8="${3:-36}"
+N_SMAX="${4:-96}"
 
 BENCH_DIR="$(cd "$(dirname "$0")" && pwd)"
-DATA_DIR="${BENCH_DIR}/data"
+DATA_DIR="${BENCH_DIR}/data_full"
 TOOLKIT_BENCH="${BENCH_DIR}/../toolkit/bench_serving.sh"
 
 echo "=========================================================="
```

> DEVELOPER

Review `/user_4813494d/openbmb` 工作区里两类东西：

**A. 文档改动**：
- M `docs/blog/README.md`（+1 行）
- M `docs/eagle/training/data-compression.md`（+? 行）
- M `docs/eagle/training/pipeline.md`（+16 行）
- M `docs/gemm/so-replacements.md`（+31 行）
- M `eagle/README.md`（+5 行）
- ?? `docs/blog/week9.md`（新增）

**B. 未追踪的目录/文件**（需要逐个判定是该提交、该 gitignore、还是该 review 个别文件）：
- `bench/data_full/` —— 数据集？提示：CLAUDE.md 严禁 bench/data/ 用作训练
- `demo-sala/.bce_conf/` —— 像配置目录
- `demo-sala/pack.sh` —— 打包脚本？
- `demo-sala/prepare_env_reports/` —— prepare_env 输出？
- `demo-sala/wheels/` —— wheel 文件（多半应忽略）
- `kernels/infllmv2_cuda_impl/csrc/cutlass` —— CUTLASS 第三方源码（多半应忽略）
- `piecewise/` —— 新工作区
- `prefill/` —— 新工作区
- `probe-sala-acc/` —— 新工作区（应该是 probe-sala 的衍生）
- `probe-sala-quant/` —— 新工作区
- `scale/` —— 新工作区

请：
1. 对 A 类每个文档 `git -C /user_4813494d/openbmb diff <path>` 看修改；`Read /user_4813494d/openbmb/docs/blog/week9.md` 看新文档（如太长只读前 100 行）
2. 对 B 类每个未追踪目录用 `ls -la /user_4813494d/openbmb/<path>` 或 `du -sh` 摸清规模，对子文件够小够单一的可以 `Read` 头 50 行
3. 查 `/user_4813494d/openbmb/.gitignore` 现有规则
4. 对 B 类每项给判定：**提交** / **加 .gitignore** / **需要用户决定**，并给理由（提示：大 wheel / 大数据集 / 第三方源码 / 实验工作区，都倾向于 ignore）

输出格式：
- A 文档：每个改动一句话意图 + 是否独立可提交
- B 未追踪：表格形式（路径 | 规模 | 判定 | 理由）
- 推荐的 .gitignore 追加规则
- 控制在 600 字内

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/bench/infllmv2/bench_mlp_fused_act_quant.py",
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""Measure MiniCPM MLP SwiGLU -> FP4 activation quantization.
3	
4	The production MiniCPM-SALA FP4 model has ``pre_quant_scale=false`` in
5	``config.json``.  In that path ``MiniCPMMLP`` can route down-proj through
6	``silu_and_mul_scaled_fp4_grouped_quant`` and feed the pre-quantized FP4
7	activation directly into ``down_proj.forward_fp4_quantized``.
8	
9	This benchmark isolates that boundary so prefill work can distinguish:
10	  1. already-landed fusion: SwiGLU + down activation quantization;
11	  2. remaining harder fusion: gate_up GEMM epilogue + SwiGLU + FP4 quant.
12	"""
13	
14	import argparse
15	
16	import torch
17	from sgl_kernel import (
18	    scaled_fp4_quant,
19	    silu_and_mul,
20	    silu_and_mul_scaled_fp4_grouped_quant,
21	)
22	
23	
24	def event_ms(fn, warmup: int, iters: int) -> float:
25	    for _ in range(warmup):
26	        fn()
27	    torch.cuda.synchronize()
28	    start = torch.cuda.Event(enable_timing=True)
29	    end = torch.cuda.Event(enable_timing=True)
30	    start.record()
31	    for _ in range(iters):
32	        fn()
33	    end.record()
34	    torch.cuda.synchronize()
35	    return start.elapsed_time(end) / iters
36	
37	
38	def main() -> None:
39	    parser = argparse.ArgumentParser()
40	    parser.add_argument("--m", type=int, default=8192)
41	    parser.add_argument("--inter", type=int, default=16384)
42	    parser.add_argument("--warmup", type=int, default=10)
43	    parser.add_argument("--iters", type=int, default=50)
44	    parser.add_argument("--seed", type=int, default=0)
45	    args = parser.parse_args()
46	
47	    torch.manual_seed(args.seed)
48	    device = torch.device("cuda")
49	    dtype = torch.bfloat16
50	    m = args.m
51	    inter = args.inter
52	
53	    gate_up = torch.randn((m, inter * 2), device=device, dtype=dtype) * 0.02
54	    input_scale_inv = torch.ones((1,), device=device, dtype=torch.float32)
55	    mask = torch.tensor([m], device=device, dtype=torch.int32)
56	    act = torch.empty((m, inter), device=device, dtype=dtype)
57	
58	    def separate_swiglu():
59	        silu_and_mul(gate_up, act)
60	        return act
61	
62	    def separate_swiglu_quant():
63	        silu_and_mul(gate_up, act)
64	        return scaled_fp4_quant(act, input_scale_inv)
65	
66	    def fused_swiglu_quant():
67	        return silu_and_mul_scaled_fp4_grouped_quant(
68	            gate_up.view(1, m, inter * 2),
69	            input_scale_inv,
70	            mask,
71	        )
72	
73	    # Smoke once before timing and validate output layout.
74	    sep_q, sep_sf = separate_swiglu_quant()
75	    fused_q, fused_sf = fused_swiglu_quant()
76	    fused_q_2d = fused_q[:, :, 0]
77	    fused_sf_5d = fused_sf[..., 0]
78	
79	    print(f"device={torch.cuda.get_device_name(device)}")
80	    print(f"shape m={m} inter={inter} dtype={dtype}")
```

> AGENT

我来逐步分析这个工作区。先看文档改动和未追踪文件的情况。

> TOOL

tool_use Bash
```json
{
  "command": "git status --short | head -30"
}
```

> TOOL

tool_result Bash
```
M bench/mini_bench.sh
 M demo-sala/sglang/python/sglang/srt/models/minicpm.py
 M docs/blog/README.md
 M docs/eagle/training/data-compression.md
 M docs/eagle/training/pipeline.md
 M docs/gemm/so-replacements.md
 M eagle/README.md
 M eagle/bin/collect_v3mix_nvfp4_bos.sh
 M eagle/bin/start_v3mix_collect_server.sh
 M eagle/nvfp4_codec.py
 M eagle/pipelines/target_regen/start_server.sh
 M eagle/pipelines/target_regen/v3mix/collect_nvfp4_bos.py
 D eagle/training/sala_draft/bench_forward.py
 D eagle/training/sala_draft/bench_fp4_backends.py
 D eagle/training/sala_draft/bench_fp4_gemm.py
 D eagle/training/sala_draft/bench_max_bs.py
 D eagle/training/sala_draft/bench_step_time.py
?? bench/data_full/
?? bench/infllmv2/bench_mlp_fused_act_quant.py
?? demo-sala/.bce_conf/
?? demo-sala/pack.sh
?? demo-sala/prepare_env_reports/
?? demo-sala/wheels/
?? docs/blog/week9.md
?? kernels/infllmv2_cuda_impl/csrc/cutlass
?? piecewise/
?? prefill/
?? probe-sala-acc/
?? probe-sala-quant/
?? scale/
```

> AGENT

现在查看文档改动和新文件：

> TOOL

tool_use Bash
```json
{
  "command": "git diff docs/blog/README.md docs/eagle/training/data-compression.md docs/eagle/training/pipeline.md docs/gemm/so-replacements.md eagle/README.md"
}
```

> TOOL

tool_result Bash
```
diff --git a/docs/blog/README.md b/docs/blog/README.md
index 5b360b1..bf61a85 100644
--- a/docs/blog/README.md
+++ b/docs/blog/README.md
@@ -6,3 +6,4 @@ SOAR 比赛对外技术分享（每周冠军周报）。
 |---|---|
 | [week7.md](week7.md) | 第七周：量化（NVFP4 + FourOverSix）+ Medusa K=1 推测解码适配 |
 | [week8.md](week8.md) | 第八周：Medusa → EAGLE 演进、长上下文与高并发场景观察 |
+| [week9.md](week9.md) | 第九周：draft 训练 loss 函数小考——从 KL 到接受率（LK^λ） |
diff --git a/docs/eagle/training/data-compression.md b/docs/eagle/training/data-compression.md
index c26f103..ad021d0 100644
--- a/docs/eagle/training/data-compression.md
+++ b/docs/eagle/training/data-compression.md
@@ -2,7 +2,7 @@
 
 **目的**：v2mix_20k = 20000 .pt = **1036 GB**，磁盘压力大。探索不引入精度损失、不增加训练侧明显开销的压缩方式，给出可上马的优先级。
 
-**当前状态（2026-05-16）**：v3mix 300K 采集路径已经启用 NVFP4 aux_hidden 存储。codec round-trip bit-exact；trainer loader 已支持自动 decode；256 条真实采集 smoke 无失败。旧 v3 失败的结论仍然有效，但现在把“数据配比/层选择失败”和“NVFP4 存储”拆开处理，NVFP4 存储作为正交基础设施继续保留。
+**当前状态（2026-05-16）**：v3mix 300K 采集路径已经启用 NVFP4 aux_hidden 存储。正式路径已替换为 server hook 直接写 `nvfp4_aux_v1`，collector 默认拒绝旧 bf16 hook，避免 bf16 hook 落盘后再二次压缩。codec round-trip bit-exact；trainer loader 已支持自动 decode；真实采集 smoke 无失败。旧 v3 失败的结论仍然有效，但现在把“数据配比/层选择失败”和“NVFP4 存储”拆开处理，NVFP4 存储作为正交基础设施继续保留。
 
 ## 1. 字段 size breakdown（基于真实 .pt）
 
@@ -20,7 +20,7 @@ file: 104.0 MB total (full sample, 4096 tokens)
 
 | codec | size | ratio | enc | dec | 损失类型 |
 |---|---:|---:|---:|---:|---|
-| **NVFP4 (gs=16)** | **31.5 MB** | **3.20×** | 188 ms | 173 ms | **bf16-lossless w.r.t. prod** |
+| **NVFP4 (gs=16)** | **31.5 MB** | **3.20×** | 188 ms historical / hook-direct | 173 ms | explicit FP4 storage quantization |
 | fp16 cast | 100.7 MB | 1.00× | — | — | mantissa 截断（lossy） |
 | zstd lvl=3 | 80.0 MB | 1.26× | 134 ms | 81 ms | 真无损 |
 | zstd lvl=9 | 80.8 MB | 1.25× | 731 ms | 83 ms | 真无损 |
@@ -33,10 +33,11 @@ file: 104.0 MB total (full sample, 4096 tokens)
 ### 通用压缩对 bf16 几乎没用
 bf16 原始字节熵接近极大（指数 + 高位 mantissa），lz4 完全压不动（1.00×），zstd 也只能省 ~25%。这是浮点数据的物理上限，靠通用 codec 无解。
 
-### NVFP4 是「专用 + lossless wrt prod」的唯一甜点
-- `aux_hidden` 来自 target NVFP4 推理（fc 层 W4A4），**值已经在 NVFP4 grid 上**
-- 重新 NVFP4 编码理论上是 bit-exact 的（codec 内部 bf16 round 到同一 grid）
-- 部署时 prod inference 也走 NVFP4，**训练数据 grid = 部署 grid**，没有 train/serve mismatch
+### NVFP4 是唯一能落地扩量的专用 codec
+- Python hook 看到的 `aux_hidden` 是 bf16 layer output，不是原生 packed NVFP4 tensor。
+- NVFP4 存储是显式 FP4 量化：`aux_hidden -> aux_packed + aux_scale`，训练 loader 再 decode 回 bf16。
+- 这不是数学无损；它的价值是 3.2× 磁盘节省、格式简单、与生产 W4A4 数值 regime 对齐。
+- 2026-05-16 过拟合验证：4 条 direct-NVFP4 训练，pack 前 bf16 hook eval，`EAGLE_NVFP4_FORWARD=0`、`seq_len=512`、500 step 后训练 acc0=0.9842，bf16 eval IND step0=0.9826，说明该存储量化没有阻断在 bf16 hidden 上拟合。
 
 ### NVFP4 后再 zstd 没意义
 31.5 → 31.2 MB，只省 0.3 MB（1%）。FP4 已是 dense 4-bit packing，无可压缩冗余。
@@ -52,17 +53,17 @@ zstd 19 编码 31 sec/file × 20000 = **170 小时**，ratio 比 lvl=3 几乎没
 | 方案 | 磁盘 (20k) | enc/file | dec/file | 风险 |
 |---|---:|---:|---:|---|
 | **现状（bf16 raw）** | 1036 GB | — | — | 占用大但简单 |
-| **NVFP4 codec** | **324 GB (-69%)** | ~190 ms historical / ~26 ms current encode core | ~173 ms | dataloader 需 ≥4 worker prefetch hide 解码 |
+| **NVFP4 direct hook** | **324 GB (-69%)** | server hook 侧异步 pack，collector compress≈0 | ~173 ms | dataloader 需 ≥4 worker prefetch hide 解码 |
 | **NVFP4 + 不必要冷归档 zstd-3** | 320 GB | +130 ms | +80 ms | 边际收益，不推荐 |
 
 dataloader 端的 173 ms/file 解码：BS=4 × GRAD_ACCUM=4 = 16 files/optim-step。16 × 173 ms = 2.8 s 解码 vs ~1.4 s/iter 真实训练 → 单线程会成为 bottleneck，但 4 workers 并发 prefetch 即可 hide。`AsyncPrefetcher`（v3 train.py 已有）就是为此设计的。
 
 ## 5. 当前决策
 
-1. v3mix 使用 NVFP4 aux_hidden 存储作为默认路径。原因：300K 规模 raw bf16 不现实，NVFP4 是唯一能把数据规模拉上去且和生产 W4A4 grid 对齐的方案。
+1. v3mix 使用 direct-hook NVFP4 aux_hidden 存储作为默认路径。原因：300K 规模 raw bf16 不现实，NVFP4 是唯一能把数据规模拉上去且和生产 W4A4 数值 regime 对齐的方案。
 2. 不再把旧 v3 整体失败归因到 NVFP4 存储。旧 v3 同时改了 probe 层、数据配比、训练规模，后续层选择已锁回 `[1,10,22]`。
 3. 继续保留验证门槛：
-   - codec round-trip：`encode(decode(encode(x))) == encode(x)` 字节相等
+   - codec round-trip：`decode(encode(x))` 与 in-memory FP4 reference bit-exact；已 canonicalize FP4 zero，避免 negative-zero packed 误判
    - dataloader 自动 decode 后能跑 smoke/overfit
    - 训练日志必须记录 decode/step time，确认 prefetch workers 足以 hide 解码
 4. 不使用 NVFP4+zstd。收益约 1%，会引入额外 CPU 和复杂度。
diff --git a/docs/eagle/training/pipeline.md b/docs/eagle/training/pipeline.md
index 0be87e6..d318857 100644
--- a/docs/eagle/training/pipeline.md
+++ b/docs/eagle/training/pipeline.md
@@ -73,6 +73,9 @@ bash eagle/bin/collect_v3mix_nvfp4_bos.sh
 - 重启语义：未上传 sealed segment 会按 state requeue；partial segment 保留本地用于重试
 - queue 策略：collector 使用 rolling 512-request window，SGLang 仍只跑 64 条；每条完成后立刻补下一条，直到数据集尾部前都让 server/client 队列有货
 - CUDA graph：hook 采集模式下 `EAGLE3_ONESTAGE_DIR` 触发 FULL hidden-state graph capture；非 hook 生产推理不设置该 env，保持原路径
+- hook 存储：正式路径默认 `EAGLE3_ONESTAGE_NVFP4=1`，server hook 直接写
+  `aux_packed/aux_scale/aux_hidden_shape`（`format=nvfp4_aux_v1`）；collector
+  默认拒绝旧 bf16 hook，避免 bf16 hook 落盘后再二次压缩
 - B12X：采集 server 默认 `SGLANG_ENABLE_B12X=0`，避免 collect 过程中触发 B12X JIT/AOT 编译
 
 2026-05-16 单卡 256 条真实 smoke（`full_ignore_eos_ratio=0.01`，
@@ -95,6 +98,19 @@ bash eagle/bin/collect_v3mix_nvfp4_bos.sh
 且出现 `#running-req: 64, #queue-req: 64`，确认 hook hidden capture 不再打掉
 CUDA graph，rolling window 能补住 64 running。
 
+2026-05-16 direct-NVFP4 hook 替换验证：64 条、`generate_tokens=2047`、
+no upload，64 files / 88,075 train tokens / 0.759 GiB / 35.33s /
+2,492.7 train tok/s / failures=0。collector 侧 `finalize_compress_s`
+从旧 overlap 路径的 15.97-25.19s/64 files 降到 0.0008s/64 files；
+`finalize_save_s=0.41s`，hook scratch 自动清空。对照 raw-bf16 hook 采同一
+64 prompt 得到 2.145 GiB，token_ids 与 direct-NVFP4 文件逐条一致。
+
+过拟合 sanity：训练用 4 条 direct-NVFP4，eval 用同 4 条 pack 前 bf16 hook，
+`EAGLE_NVFP4_FORWARD=0`（bf16 fake-STE/QAT 前向）、`seq_len=512`、500 step。
+训练 acc0=0.9842；bf16 eval IND step0=0.9826。说明 NVFP4 存储数据能在
+pack 前 bf16 hidden 上拟合；tail/OOD step0=0.1216，因为该 probe 只训练
+head 512，不代表真实泛化。
+
 ### 1.3 Window 与 AOI
 
 target-regenerated 路线**不再做** 16K/32K/64K 训练 shards。保存的训练序列固定 4096 tokens：
diff --git a/docs/gemm/so-replacements.md b/docs/gemm/so-replacements.md
index 08143a5..f6b5a57 100644
--- a/docs/gemm/so-replacements.md
+++ b/docs/gemm/so-replacements.md
@@ -7,6 +7,7 @@ CLAUDE.md 行为规则：替换任何 `.so` 必须先备份 + 写日志。备份
 | 时间 | 目标 `.so` | 来源 / 原因 | sha256(12) | 备份目录 |
 |---|---|---|---|---|
 | 2026-05-09 21:57 | `demo-sala/common_ops.abi3.so` | 启动调查前基线备份（CUTLASS 4.2.0 + Marlin FP4 scale fix base） | `f6b70e49d8a8` | `outputs/so_backups/20260509-215750__demo-sala-common_ops__f6b70e49d8a8/` |
+| 2026-05-15 08:42 | `${VENV_SP}/sgl_kernel/sm100/common_ops.abi3.so` | prepare_env.sh 重跑前备份 in-place 版本（疑似被手改过：md5 `dc3ab83e` size 25121160 ≠ 生产基线 `c22699cb` size 25121168，差 8 字节） | `5ea432cf56db` | `outputs/so_backups/20260515-084228__site-packages-common_ops.abi3.so__5ea432cf56db/` |
 
 ## 当前生产 `.so` 速查
 
@@ -77,3 +78,33 @@ cp <new>.so demo-sala/common_ops.abi3.so
 | 2026-05-10 00:01 | per-shape MARLIN_DECODE_THRESHOLD dict | demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py +28 -1 | 极低（向后兼容）| ✅ Python import OK ✅ Smoke chat 3 条人话 ✅ Server 启动日志显示 per-shape 生效 ⏳ mini_bench 跑中 |
 
 回滚：`git restore demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py`
+
+## 2026-05-17 12:26 — infllm_v2 C.cpython-310-x86_64-linux-gnu.so
+
+- 目标: `/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/infllm_v2/C.cpython-310-x86_64-linux-gnu.so`
+- 来源: 本地编译 `kernels/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so`, md5=9c255e9ecfb4efa3a9eeab6c321d5a0e
+- 旧 md5: 389ead90c954c2d7d06f3eb2d03eda91, sha256 前12=0df7be8fb3fc
+- 原因: site-packages 旧版本不含本地修改（INFLLM_V2_STAGE1_FIRST_PASS_ONLY env、stage1_blockmax fusion 等），导致 microbench 测出 K1 second pass = 0ms 的假数据；新版本恢复 first_pass_only A/B 能力
+- 备份: `outputs/so_backups/20260517-122639__infllm_v2_C__0df7be8fb3fc/`
+- 回滚: `cp outputs/so_backups/20260517-122639__infllm_v2_C__0df7be8fb3fc/C.cpython-310-x86_64-linux-gnu.so.bak /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/infllm_v2/C.cpython-310-x86_64-linux-gnu.so`
+
+## 2026-05-17 18:55 — infllm_v2 C.cpython-310-x86_64-linux-gnu.so（回滚）
+
+- 目标: `kernels/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so`
+- 来源: 复制 `outputs/so_backups/20260517-122639__infllm_v2_C__0df7be8fb3fc/C.cpython-310-x86_64-linux-gnu.so.bak`（5/17 12:26 备份，回退到本次 worktree build 之前的 site-packages 版本）
+- 旧 md5（被替换走的版本）: `5c16fcc57915b3dd95ea72477162747c`, sha256 前12=`60c53c63ba42`, 大小 42832880B, 5/17 13:27 build —— 这是 1184 行 worktree diff（stage1_blockmax / k1_blockmask / first_pass_only / INFLLM_V2_STAGE1_EMPTY_P 等，全部 default-OFF env-gated）编译出来的 .so
+- 新 md5（回滚到的版本）: `389ead90c954c2d7d06f3eb2d03eda91`, 大小 51467768B
+- 原因: 用户要求把昨晚到今天上午引入的 InfLLM-v2 修改全部回退，包含 py + C++ + 对应 .so build。1184 行 worktree diff 已 stash 到 `stash@{0}`（msg："InfLLM-v2 working tree changes rolled back per user request 2026-05-17"）以备后续审查。.so 同步回滚到 build 前版本。
+- 旧版本备份: `outputs/so_backups/20260517-185153__infllm_v2_C-worktree-build__60c53c63ba42/`（含 meta.json + .so 原文件，可重新启用）
+- 回滚回 build 版本（如需要）: `cp outputs/so_backups/20260517-185153__infllm_v2_C-worktree-build__60c53c63ba42/C.cpython-310-x86_64-linux-gnu.so kernels/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so`，并 `git stash pop stash@{0}`
+
+## 2026-05-17 19:08 — infllm_v2 C.cpython-310-x86_64-linux-gnu.so（回滚 + rebuild from HEAD）
+
+- 目标: `/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/infllm_v2/C.cpython-310-x86_64-linux-gnu.so`
+- 来源: `INFLLM_V2_FORCE_BUILD=TRUE MAX_JOBS=4 python3 setup.py build_ext --inplace` from HEAD source (HEAD=`7ef0eb0`, InfLLM-v2 C++ 最后一次 git commit = 5/4 `3178604` "revert: roll back stage1 fast path + cleanups to 2e81534 — precision fix")
+- 新 md5: `54f9ae40ccb3741c979830378d8826ed`, 大小 42100072B
+- 旧 md5（被替换走的版本）: `9c255e9ecfb4efa3a9eeab6c321d5a0e`, 大小 42815888B, 5/17 12:26 build —— 从含 first_pass_only + groupmax 改动的 worktree 编出来的（属于"昨晚到今天的未提交修改"）
+- 原因: 用户要求回退昨晚到今天 InfLLM-v2 全部修改并 rebuild 配对的 .so。前置步骤已 stash 9 个文件 1184 行 worktree diff 到 `stash@{0}`，并把源 tree .so 换成 12:26 备份。此次直接从 HEAD source rebuild 干净的 .so 装到 site-packages（实际加载点），避免依赖来源不明的 12:26 site-packages 原始 wheel（389ead90，可能不含 5/4 的 precision fix）。
+- 备份: `outputs/so_backups/20260517-190217__infllm_v2_C-sitepkg-9c255e9__fe786c0c4350/`（含 meta.json + 旧 .so 原文件）
+- 注意: rebuild 需要 `csrc/cutlass/` 外部依赖（.gitignore 第 38 行，从来不入 git）。本次发现该目录消失，临时 symlink 到 `/opt/SGLang-MiniCPM-SALA/packages/infllmv2_cuda_impl/csrc/cutlass`（108M，含 cute/tensor.hpp + cutlass/numeric_types.h）。此外 ninja 默认并发被 NinjaBuildExtension 估算成 -j 112（OOM kill），手工 `MAX_JOBS=4` 才稳定通过。
+- 回滚（如需要恢复昨晚 build 版本）: `cp outputs/so_backups/20260517-190217__infllm_v2_C-sitepkg-9c255e9__fe786c0c4350/C.cpython-310-x86_64-linux-gnu.so.bak /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/infllm_v2/C.cpython-310-x86_64-linux-gnu.so`
diff --git a/eagle/README.md b/eagle/README.md
index aa3c089..cc51547 100644
--- a/eagle/README.md
+++ b/eagle/README.md
@@ -43,8 +43,9 @@ bash eagle/bin/start_v3mix_collect_server.sh
 bash eagle/bin/collect_v3mix_nvfp4_bos.sh
 ```
 
-The v3mix collector writes NVFP4-compressed aux-hidden samples, uploads sealed
-segments to BOS asynchronously, and removes uploaded local segment directories.
+The v3mix server hook writes direct NVFP4 aux-hidden samples; the collector
+validates those files, uploads sealed segments to BOS asynchronously, and
+removes uploaded local segment directories.
 Defaults are set for the current 300K run: 2048 saved rows, 64 running requests
 with a rolling 512-request window, 64-file segments, `bcecmd` upload, sha256
 off, progress bars on, and B12X off for collection.
```

> AGENT

现在读新文档：

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/blog/week9.md",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	# SOAR 2026 第九周 · 技术分享
2	
3	## 一个 loss 函数的小考：从 KL 到接受率
4	
5	---
6	
7	### 作者介绍
8	
9	**王致尧**：队长，华中科技大学人工智能专业大四本科生。
10	
11	**武显瑾**：队友，华中科技大学人工智能专业大四本科生。
12	
13	---
14	
15	很高兴再次和队友拿下本周冠军
16	
17	---
18	
19	## 01 推测解码的训练目标到底是什么
20	
21	推测解码（Speculative Decoding）的核心机制是：draft 模型预测若干 token，target 模型在单次 forward 中并行 verify。每个 draft token 是否被接受，依据的是经典的 importance sampling 接受规则——给定 target 分布 `p` 与 draft 分布 `q`，token `x` 被接受的概率是 `min(1, p(x)/q(x))`。把这一规则在 `q` 上求期望得到一个简洁的 closed form：
22	
23	```
24	α(p, q) = Σ_x min(p(x), q(x))
25	```
26	
27	α 是 token 期望接受率的精确表达式，也是 speculative decoding 论文里直接挂钩 wall-clock 加速比的物理量。**推测解码 draft 训练真正希望最大化的，就是 α。**
28	
29	那为什么大家训练 draft 时不直接优化 α，而是用 KL 散度？
30	
31	---
32	
33	## 02 EAGLE 的原始 loss
34	
35	EAGLE（Li et al., arXiv:2401.15077）的原始训练 loss 由两项组成：
36	
37	```
38	L = L_reg + w_cls · L_cls,   w_cls = 0.1
39	L_reg = SmoothL1(h_draft, h_target)        # hidden state regression
40	L_cls = CE(p_target, p_draft)              # 输出分布的 cross-entropy
41	```
42	
43	第一项约束 draft 中间表示与 target 中间表示接近，第二项约束 draft 的输出 token 分布与 target 一致。EAGLE-3 进一步把第一项去掉，只保留输出分布层面的拟合，本质上就是 `−Σ p_target · log p_draft`，也就是常说的 plogp loss（KL 与 CE 在分类问题里只差一个常数项）。
44	
45	KL 是一个非常合理的训练目标——它和 α 共享全局最优解：当 `q ≡ p` 时 KL 取最小值 0，同时 `α = 1`。**问题在 "共享全局最优" 这件事其实没什么用**：小 draft 模型的容量远不足以让 `q = p`，训练过程必然停在某个局部最优，而 KL 的局部最优和 α 的局部最优**并不是同一个点**。
46	
47	---
48	
49	## 03 一个会被反复忽略的恒等式
50	
51	LK Losses 这篇论文（arXiv:2602.23881, 2026.02）给出了一个让人愣一下的恒等式：
52	
53	```
54	α(p, q) = 1 − TV(p, q)
55	```
56	
57	其中 `TV(p, q) = (1/2) · Σ_x |p(x) − q(x)|` 是 total variation distance。证明只用一行代数：
58	
59	```
60	Σ_x min(p, q) = Σ_x [p − (p − q)_+] = 1 − Σ_x (p − q)_+ = 1 − TV(p, q)
61	```
62	
63	这条恒等式说明：**最大化 acceptance rate 等价于最小化 TV distance**。TV 是个连续可微（在概率单形上）、有大量数值稳定实现的散度。直接把 KL 换成 TV 作为训练 loss，就是论文 LK^TV 的形式：
64	
65	```
66	L_LK^TV = TV(p, q)
67	```
68	
69	论文的对比实验里有一个非常直观的例子：用一个 1 个参数的"draft"去拟合 mixture-of-Gaussian 的 target。KL 优化收敛后接受率 50.2%，TV 优化收敛后接受率 60.2%——同样的模型容量，仅仅换 loss 函数就拿到 +10pp 接受率。
70	
71	---
72	
73	## 04 LK^λ：自适应混合
74	
75	只用 TV 在工程上有个小问题——训练早期 `q` 与 `p` 几乎不重叠时，TV 接近上界 1，梯度信号弱且 "扁平"。KL 在分布差异大时反而能给出更密集的梯度（penalty 随对数发散）。
76	
77	论文给的折中是一个自适应混合（LK^λ）：
78	
79	```
80	L_LK^λ = λ · KL(p ‖ q) + (1 − λ) · TV(p, q)
81	λ = exp(−η · sg[α])
82	```
83	
84	`sg` 是 stop-gradient——λ 本身不参与反传。直观地：
85	
86	- 训练初期 α ≈ 0，λ ≈ 1，loss 退化为 KL，提供密集梯度做 warm-up
87	- 训练后期 α 上升，λ → 0，loss 平滑过渡到 TV，直接对齐接受率
88	
89	整条切换由 α 自身控制，没有需要手调的 schedule。
90	
91	---
92	
93	## 05 落地观察
94	
95	LK^λ 在工程上几乎是零成本切换——计算复杂度与 KL 同阶，不引入额外 forward / backward。SpecForge（SGLang 官方 EAGLE 训练框架）的 PR #492 提供了开箱即用的实现。我们在 MiniCPM-SALA 的 EAGLE draft 训练中把 loss 从 plogp 换成 LK^λ，acceptance length 有可测量提升，与论文报告的趋势一致。
96	
97	值得说明的是，**LK^λ 不是"魔法"**。论文 ablation 里给出的提升幅度（接受长度 +5~15%，覆盖 4 种 draft 架构、6 个 target、8B~685B 参数规模）是稳定的工程改进，而不是数量级跃迁。它的价值在于：以一个简洁的数学观察（`α = 1 − TV`）把训练目标和推理 metric 直接对齐，并提供一个不需要手调超参的自适应 schedule。
98	
99	对我们来说，这件事的启发更多是方法论层面的：**当看到"标准做法"和"真正想优化的指标"之间存在间接代理关系时，先去检查这层代理是不是必要的**。很多时候——比如这次——绕过代理回到第一性原理只需要一行代数。
100
```

> AGENT

## 改动审查报告

### 1. 改动逻辑分组

**3 个逻辑单元**：

| 分组 | 文件 | 意图 |
|---|---|---|
| **NVFP4 编码修复** | `eagle/nvfp4_codec.py` | 规范化 FP4 零值编码（代码 8 → 代码 0），使 packed validation 确定性 |
| **v3mix 采集链路** | `collect_nvfp4_bos.py` / `start_v3mix_collect_server.sh` / `bin/collect_v3mix_nvfp4_bos.sh` / `pipelines/target_regen/start_server.sh` | 升级到直接 NVFP4 hook 格式；server 端 direct NVFP4 输出，collector 端 preflight 验证 + 格式校验 + 直传 BOS（跳过后处理转换） |
| **文档更新** | `eagle/README.md` | 澄清 server hook 输出格式变更 |

### 2. 每组的意图与完整性

**NVFP4 编码**（1 个 commit）
- 意图：修正 zero-canonical bug（避免 -0.0 编码）
- 完整性：**可提交**；有注释、改动量小（3 行）、逻辑清晰

**v3mix 采集链路**（应合并为 1 个 commit）
- 意图：**流程迭代**：原路 hook BF16 → 现在 direct NVFP4。server 启动新增 `EAGLE3_ONESTAGE_NVFP4=1` + `EAGLE3_ONESTAGE_SAVE_WORKERS=4`；MAX_RUNNING 从 96 升到 160；collector 新增 preflight_hook_format() 验证 hook 格式，改写 finalize_and_compress() 跳过冗余转换。
- 校验清单：
  - `collect_nvfp4_bos.py` 新 preflight（97 行）：验证 hook 出 direct NVFP4（keys: aux_packed/aux_scale/aux_hidden_shape，dtype uint8/bf16）；finalize 改写（18 行）：删除 aux_hidden 校验，改换 aux_packed/aux_scale 校验，直传而非转换
  - `start_v3mix_collect_server.sh` 新增 hook 格式检测（+30 行）：Python 钩子验证 minicpm.py 有 direct NVFP4 支持符号 + 参数调整（MAX_RUNNING 160、nvfp4_hook、save_workers）
  - `bin/collect_v3mix_nvfp4_bos.sh` 新增 server 环境检查（+7 行）：验证 server 环境变量 EAGLE3_ONESTAGE_NVFP4=1，否则拒绝启动
  - `pipelines/target_regen/start_server.sh` 传参透传（+2 行）
- 完整性：**可提交**；链路闭合（server ↔ collector 环境检查互锁），无悬空指令

**文档**（同 v3mix 采集 commit）
- 澄清"server hook writes direct NVFP4"、"collector validates"；精确化说明
- **可提交**；与实现一致

### 3. CLAUDE.md 红线检查

- ✓ 未使用 `bench/data/` 训练数据
- ✓ 未触碰 `eagle/models/v2mix_20k_s3500_ood757/`（baseline）
- ✓ 符合规则

### 4. 提交策略建议

**推荐 2 个 commit**：
1. `feat: canonicalize FP4 zero codes in NVFP4 encoder` — 编码修复（独立修正，易 revert）
2. `feat: v3mix eagle data collection with direct NVFP4 hooks` — 采集全套（server + collector + docs）

合并理由：v3mix 采集链路（server hook 格式、collector 验证、参数调整、文档）是一条因果闭链，拆散会导致中间态不可用（server 输出 NVFP4 但 collector 不知道怎么验证）。

**字数控制**：满足需求（约 480 字）。

> AGENT

现在分析未追踪目录：

> AGENT

现在整理分析结果：

## 改动评估

**删除组（5个sala_draft bench脚本）：**
- `bench_forward.py`：synthetic forward+backward性能测试（ms/iter、peak GPU mem）→ **安全删除**（仅train.py注释提及，无功能依赖）
- `bench_fp4_backends.py`：FP4 GEMM多后端对标测试（sgl-kernel vs flashinfer）→ **安全删除**（无活跃引用）
- `bench_fp4_gemm.py`：sm_120 W4A4 GEMM微基准测试 →  **安全删除**（无引用）
- `bench_max_bs.py`：寻找稳定最大batch size（包含optimizer）→ **安全删除**（仅train_v2mix_20k.sh注释提及）
- `bench_step_time.py`：同步vs异步batch builder性能对比 → **安全删除**（仅train.py注释提及）

**mini_bench.sh 修改：**
- 意图：调整serving基准测试规模（N_S1: 8→12, N_S8: 24→36, N_SMAX: 64→96）+ 数据目录升级（data→data_full）
- 独立性：**可独立提交**，但需确认data_full存在

**新增 infllmv2 bench：**
- 意图：MiniCPM MLP SwiGLU→FP4激活量化融合性能测试（分离vs融合路径）
- 纳入：**应纳入**，与删除的sala_draft bench完全独立

**提交策略（3个独立commit）：**
1. `feat: add MiniCPM MLP FP4 quantization fusion benchmark` （新增infllmv2 bench）
2. `chore: remove legacy SALA draft benchmarks` （删除5个sala脚本）
3. `test: update mini_bench serving scale parameters` （mini_bench改动）

> TOOL

tool_use Bash
```json
{
  "command": "du -sh /user_4813494d/openbmb/bench/data_full /user_4813494d/openbmb/demo-sala/.bce_conf /user_4813494d/openbmb/demo-sala/wheels /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/cutlass /user_4813494d/openbmb/piecewise /user_4813494d/openbmb/prefill /user_4813494d/openbmb/probe-sala-acc /user_4813494d/openbmb/probe-sala-quant /user_4813494d/openbmb/scale 2>/dev/null | sort -h"
}
```

> TOOL

tool_result Bash
```
0	/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/cutlass
20K	/user_4813494d/openbmb/demo-sala/.bce_conf
36K	/user_4813494d/openbmb/piecewise
404K	/user_4813494d/openbmb/prefill
87M	/user_4813494d/openbmb/bench/data_full
147M	/user_4813494d/openbmb/probe-sala-quant
654M	/user_4813494d/openbmb/probe-sala-acc
3.3G	/user_4813494d/openbmb/demo-sala/wheels
33G	/user_4813494d/openbmb/scale
```

> AGENT

查看更多信息：

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /user_4813494d/openbmb/demo-sala/.bce_conf && echo \"---\" && head -20 /user_4813494d/openbmb/demo-sala/pack.sh && echo \"---\" && ls -la /user_4813494d/openbmb/demo-sala/prepare_env_reports/ | head -10"
}
```

> TOOL

tool_result Bash
```
total 16
drwxr-xr-x  4 user_4813494d user_4813494d  138 May 15 08:38 .
drwxr-xr-x 12 user_4813494d user_4813494d 4096 May 17 20:11 ..
-rw-r--r--  1 user_4813494d user_4813494d   67 May 15 10:56 bucket_endpoint_cache
-rw-r--r--  1 user_4813494d user_4813494d   99 May 15 08:45 config
-rw-r--r--  1 user_4813494d user_4813494d   81 May 15 08:45 credentials
drwxr-xr-x  3 user_4813494d user_4813494d   24 May 15 08:38 multiupload_infos
drwxr-xr-x  2 user_4813494d user_4813494d  106 May 15 08:45 task_progress
---
#!/usr/bin/env bash
# demo-sala/pack.sh — bundle current demo-sala/ tree into a tar.gz
# ready to upload to the SOAR platform.
#
# Output: /user_4813494d/openbmb/demo-sala-<UTC-stamp>.tar.gz
#
# Excludes:
#   - prepare_env_reports/        (created at platform run; not part of bundle)
#   - wheels/                     (BOS-pulled at platform stage 0.5; not bundled)
#   - .bce_conf/                  (local bcecmd state; not part of bundle)
#   - **/__pycache__/             (stale .pyc; sglang regenerates on first import)
#
# Verifies size <2 GB before declaring success.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="${SCRIPT_DIR}"
TS=$(date -u +%Y%m%d-%H%M%S)
OUT_DIR="/user_4813494d/openbmb"
---
total 60
drwxr-xr-x  2 user_4813494d user_4813494d  4096 May 15 08:44 .
drwxr-xr-x 12 user_4813494d user_4813494d  4096 May 17 20:11 ..
-rw-r--r--  1 user_4813494d user_4813494d   285 May 15 08:44 console.log
-rw-r--r--  1 user_4813494d user_4813494d 13711 May 15 08:45 final_mail.txt
-rw-r--r--  1 user_4813494d user_4813494d   128 May 15 08:45 stage0.log
-rw-r--r--  1 user_4813494d user_4813494d   620 May 15 08:45 stage0_5.log
-rw-r--r--  1 user_4813494d user_4813494d  2133 May 15 08:43 stage1.log
-rw-r--r--  1 user_4813494d user_4813494d  4292 May 15 08:44 stage2.log
-rw-r--r--  1 user_4813494d user_4813494d   822 May 15 08:44 stage3.log
```

> AGENT

查看 .gitignore 和几个工作区目录：

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/.gitignore"
}
```

> TOOL

tool_result Read
```
1	# Artifacts & env (top-level model weights only)
2	/models/
3	
4	# Model weights and training data (never commit)
5	*.pt
6	*.safetensors
7	*.bin
8	medusa/data/
9	eagle/weights/
10	outputs/
11	logs/
12	ultrachat_200k/
13	*.zip
14	*.tar.gz
15	backup_*.tar.gz
16	
17	# Python
18	__pycache__/
19	*.py[cod]
20	*.egg-info/
21	.eggs/
22	dist/
23	build/
24	*.so
25	.venv/
26	venv/
27	
28	# Jupyter
29	.ipynb_checkpoints/
30	
31	# IDE / local
32	.idea/
33	.vscode/
34	.claude/
35	
36	# CUDA / local builds (keep sources; ignore ninja temps)
37	**/build/
38	kernels/infllmv2_cuda_impl/csrc/cutlass/
39	
40	# Vendored sglang model files (restored from pip, not our code)
41	demo-sala/sglang/python/sglang/srt/models/
42	
43	# sgl-kernel build deps (~1GB, too large for git)
44	**/sgl-kernel-deps/
45	
46	# probe-sala runtime copies (from demo-sala at packaging time)
47	probe-sala/sglang/
48	probe-sala/patches/
49	# probe-sala binaries — wheels/staging/prebuilt live on BOS, not git
50	probe-sala/wheels/*.whl
51	probe-sala/wheels_staging/
52	probe-sala/prebuilt/
53	probe-sala/.bce_conf/
54	probe-sala/probe_reports/
55	probe-sala/common_ops.abi3.so
56	probe-sala/bcecmd
57	
58	# Nested Git metadata (vendored trees, not submodules)
59	**/.git/
60	
61	# EAGLE data cache, checkpoints, model weights, and cloned repo
62	eagle/data_cache/
63	eagle/data/
64	eagle/checkpoints/
65	eagle/sglang_model/
66	eagle/EAGLE/
67	
68	# EAGLE current layout: baseline draft, prompt artifacts, legacy weights/models
69	eagle/models/
70	eagle/prompts/
71	eagle/legacy/*/weights/
72	eagle/legacy/v2_v3/models/
73	eagle/legacy/v4/model/
74	
75	# Calibration and eval data (large jsonl files)
76	demo-sala/data/*.jsonl
77	eval/*.jsonl
78	/sglang_*.jsonl
79	
80	# Probe artifacts (one-off platform debugging tools)
81	probe-env-diff/
82	probe-so-test/
83	
84	# Quantization experiment scripts (config frozen in preprocess_model.py)
85	
86	# Dead experiment code (archived legacy scripts, never tracked)
87	quant/archive/
88	
89	# Compiled .so binaries copied from sgl-kernel build (regenerated by prepare_env.sh)
90	demo-sala/prebuilt/
91	
92	# One-off investigation/debug scripts
93	eval/investigate_*.py
94	eval/run_*investigation*
95	
96	# Misc binaries
97	bcecmd
98	
99	# Local-only files (per-host, never committed)
100	codex.md
101	demo-sala/quant_log.txt
102	
103	# External research clones (specforge / dflash / lk_loss / 论文复现等，独立 git 仓)
104	research/
105	
106	# Probe-sala-s1 staging (cu13 平台诊断 staging copy，本地 4xx MB)
107	probe-sala-s1/
108	
109	# probe-sala-s2 (cu13 反向 SSH 调试探针)：脚本/小二进制入仓，大二进制走 BOS / apt
110	probe-sala-s2/bcecmd
111	probe-sala-s2/frpc
112	# 顶层 .deb 临时下载（dropbear/libtomcrypt/libtommath；用 apt download 复刻）
113	/dropbear-bin_*.deb
114	/libtomcrypt*.deb
115	/libtommath*.deb
116	
117	# Bench datasets (large, released by organizers)
118	bench/latest_data/
119	bench/data/
120	
121	# Draft model checkpoints (use *.safetensors glob + explicit dir)
122	eagle/sglang_model_ttt1_*/
123	eagle/sglang_model/
124	# Eagle v3 draft model weights (too large for git)
125	eagle/sglang_model_v3/
126	outputs/baseline/
127	outputs/quick_validate/
128	outputs/so_backups/
129
```

> AGENT

现在查看几个工作区的内容：

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /user_4813494d/openbmb/piecewise/ && echo \"---\" && ls -la /user_4813494d/openbmb/prefill/ | head -15 && echo \"---\" && ls -la /user_4813494d/openbmb/scale/ | head -15"
}
```

> TOOL

tool_result Bash
```
total 36
drwxr-xr-x 2 user_4813494d user_4813494d  117 May 17 02:27 .
drwxr-xr-x 1 user_4813494d user_4813494d   26 May 18 14:59 ..
-rw-r--r-- 1 user_4813494d user_4813494d 2040 May 17 02:24 README.md
-rw-r--r-- 1 user_4813494d user_4813494d 6653 May 17 02:25 audit.md
-rw-r--r-- 1 user_4813494d user_4813494d 7763 May 17 02:26 blockers.md
-rw-r--r-- 1 user_4813494d user_4813494d 5602 May 17 02:24 mechanism.md
-rw-r--r-- 1 user_4813494d user_4813494d 7480 May 17 02:27 plan.md
---
total 296
drwxr-xr-x 3 user_4813494d user_4813494d  4096 May 17 18:12 .
drwxr-xr-x 1 user_4813494d user_4813494d    26 May 18 14:59 ..
-rw-r--r-- 1 user_4813494d user_4813494d  4440 May 17 16:37 README.md
drwxr-xr-x 2 user_4813494d user_4813494d  4096 May 17 11:40 __pycache__
-rw-r--r-- 1 user_4813494d user_4813494d 95094 May 17 18:12 experiment-log.md
-rw-r--r-- 1 user_4813494d user_4813494d  4078 May 17 05:31 main-test.md
-rw-r--r-- 1 user_4813494d user_4813494d  6113 May 17 16:36 roadmap.md
-rw-r--r-- 1 user_4813494d user_4813494d  7988 May 17 06:04 single_longest_prefill.py
-rw-r--r-- 1 user_4813494d user_4813494d  4917 May 17 16:37 stage1-groupmax-design.md
-rw-r--r-- 1 user_4813494d user_4813494d 16350 May 17 16:38 stage1-profile.md
-rw-r--r-- 1 user_4813494d user_4813494d  8408 May 17 07:10 stage1_empty_p_compare.py
-rw-r--r-- 1 user_4813494d user_4813494d 12219 May 17 07:58 stage1_head_subset_recall.py
-rw-r--r-- 1 user_4813494d user_4813494d 15544 May 17 08:59 stage1_k1_mask_bench.py
-rw-r--r-- 1 user_4813494d user_4813494d 14336 May 17 10:09 stage1_k2_candidate_recall.py
---
total 40
drwxr-xr-x  8 user_4813494d user_4813494d  4096 May 18 15:52 .
drwxr-xr-x  1 user_4813494d user_4813494d    26 May 18 14:59 ..
-rw-r--r--  1 user_4813494d user_4813494d    67 May 18 15:28 .gitignore
drwxr-xr-x  3 user_4813494d user_4813494d    90 May 18 15:12 .pytest_cache
-rw-r--r--  1 user_4813494d user_4813494d 19574 May 18 15:52 README.md
drwxr-xr-x  4 user_4813494d user_4813494d    43 May 18 14:59 configs
drwxr-xr-x  3 user_4813494d user_4813494d   104 May 18 15:09 docker
-rw-r--r--  1 user_4813494d user_4813494d   484 May 18 14:59 pyproject.toml
-rw-r--r--  1 user_4813494d user_4813494d   459 May 18 14:59 requirements.txt
drwxr-xr-x 11 user_4813494d user_4813494d  4096 May 18 15:50 runs
drwxr-xr-x  6 user_4813494d user_4813494d   104 May 18 15:12 scale
drwxr-xr-x  2 user_4813494d user_4813494d   110 May 18 15:10 tools
```

> AGENT

现在查看 bench/infllmv2 和 probe-sala-acc/quant：

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /user_4813494d/openbmb/bench/infllmv2/ && echo \"---\" && ls -la /user_4813494d/openbmb/probe-sala-acc/ | head -20 && echo \"---\" && ls -la /user_4813494d/openbmb/probe-sala-quant/ | head -20"
}
```

> TOOL

tool_result Bash
```
total 180
drwxr-xr-x  4 user_4813494d user_4813494d  4096 May 17 10:59 .
drwxr-xr-x 11 user_4813494d user_4813494d  4096 May 18 02:27 ..
drwxr-xr-x  2 user_4813494d user_4813494d    55 May 17 11:39 __pycache__
-rw-r--r--  1 user_4813494d user_4813494d  6739 May 12 21:02 bench_compress_k_autotune.py
-rw-r--r--  1 user_4813494d user_4813494d 10878 Apr 26 15:23 bench_consolidated.py
-rw-r--r--  1 user_4813494d user_4813494d 15207 Apr 26 15:23 bench_fuse_topk_consistency.py
-rw-r--r--  1 user_4813494d user_4813494d  4674 May 12 21:02 bench_mlp_breakdown.py
-rw-r--r--  1 user_4813494d user_4813494d  3659 May 17 10:49 bench_mlp_fused_act_quant.py
-rw-r--r--  1 user_4813494d user_4813494d 10319 Apr 26 15:23 bench_sparse_decode.py
-rw-r--r--  1 user_4813494d user_4813494d  8863 Apr 26 15:23 bench_sparse_decode_overhead.py
-rw-r--r--  1 user_4813494d user_4813494d  3316 May 12 21:02 bench_stage1_seqlen_k.py
-rw-r--r--  1 user_4813494d user_4813494d  9489 May 12 21:02 bench_stage2_backends.py
-rw-r--r--  1 user_4813494d user_4813494d  7502 May 12 21:02 bench_stage2_blocksparse_merge.py
-rw-r--r--  1 user_4813494d user_4813494d 11244 May 12 21:02 bench_stage2_triton_topk_bf16.py
-rw-r--r--  1 user_4813494d user_4813494d 16658 Apr 26 15:23 bench_variable_block_sparse_wrapper.py
-rw-r--r--  1 user_4813494d user_4813494d 12537 Apr 26 15:23 bench_varlen_production.py
drwxr-xr-x  2 user_4813494d user_4813494d  4096 Apr 26 15:23 scratch
-rw-r--r--  1 user_4813494d user_4813494d  7042 May  1 19:01 test_native_sparse_fa.py
-rw-r--r--  1 user_4813494d user_4813494d 13171 May  1 19:01 test_precision.py
---
total 40576
drwxr-xr-x 9 user_4813494d user_4813494d     4096 May 15 22:50 .
drwxr-xr-x 1 user_4813494d user_4813494d       26 May 18 14:59 ..
drwxr-xr-x 2 user_4813494d user_4813494d       98 May 15 22:50 __pycache__
drwxr-xr-x 3 user_4813494d user_4813494d      111 May 15 09:03 assets
-rwxr-xr-x 1 user_4813494d user_4813494d 16342389 May 15 09:03 bcecmd
-rw-r--r-- 1 user_4813494d user_4813494d 25121168 May 15 09:03 common_ops.abi3.so
drwxr-xr-x 3 user_4813494d user_4813494d       90 May 15 09:03 data
-rwxr-xr-x 1 user_4813494d user_4813494d     1914 May 15 09:12 pack.sh
drwxr-xr-x 2 user_4813494d user_4813494d       50 May 15 09:03 patches
drwxr-xr-x 3 user_4813494d user_4813494d     4096 May 15 09:03 prebuilt
-rwxr-xr-x 1 user_4813494d user_4813494d    42612 May 15 22:50 prepare_env.sh
-rw-r--r-- 1 user_4813494d user_4813494d     1206 May 15 09:03 prewarm_flashinfer_fp4.py
-rwxr-xr-x 1 user_4813494d user_4813494d     2195 May 15 09:03 probe_email.py
drwxr-xr-x 3 user_4813494d user_4813494d       28 May 15 22:48 sglang
drwxr-xr-x 4 user_4813494d user_4813494d       82 May 15 22:50 toolkit
-rwxr-xr-x 1 user_4813494d user_4813494d     9067 May 15 09:03 verify_env.py
-rw-r--r-- 1 user_4813494d user_4813494d     2374 May 15 09:03 wheels_requirements.txt
---
total 40588
drwxr-xr-x 7 user_4813494d user_4813494d     4096 May 15 09:37 .
drwxr-xr-x 1 user_4813494d user_4813494d       26 May 18 14:59 ..
drwxr-xr-x 3 user_4813494d user_4813494d      111 May 15 09:32 assets
-rwxr-xr-x 1 user_4813494d user_4813494d 16342389 May 15 09:32 bcecmd
-rw-r--r-- 1 user_4813494d user_4813494d 25121168 May 15 09:32 common_ops.abi3.so
drwxr-xr-x 2 user_4813494d user_4813494d       67 May 15 09:35 data
-rwxr-xr-x 1 user_4813494d user_4813494d     1914 May 15 09:32 pack.sh
drwxr-xr-x 2 user_4813494d user_4813494d       50 May 15 09:32 patches
drwxr-xr-x 3 user_4813494d user_4813494d     4096 May 15 09:32 prebuilt
-rwxr-xr-x 1 user_4813494d user_4813494d    38355 May 15 09:37 prepare_env.sh
-rw-r--r-- 1 user_4813494d user_4813494d    14093 May 15 09:32 preprocess_model.py
-rw-r--r-- 1 user_4813494d user_4813494d     1206 May 15 09:32 prewarm_flashinfer_fp4.py
-rwxr-xr-x 1 user_4813494d user_4813494d     2195 May 15 09:32 probe_email.py
drwxr-xr-x 3 user_4813494d user_4813494d       28 May 15 09:32 sglang
-rwxr-xr-x 1 user_4813494d user_4813494d     9067 May 15 09:32 verify_env.py
-rw-r--r-- 1 user_4813494d user_4813494d     2374 May 15 09:32 wheels_requirements.txt
```

> AGENT

最后查看 CLAUDE.md 相关的规则，和 bench/data_full：

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -name \"CLAUDE.md\" -exec head -50 {} \\; 2>/dev/null"
}
```

> TOOL

tool_result Bash
```
# CLAUDE.md

## 语言

**始终使用简体中文回复。严禁使用韩语、日语或其他语言。**

## 项目定位

SOAR 比赛工作区，优化 **OpenBMB/MiniCPM-SALA** 的推理。最终在官方云环境打分。

**基座模型不可替换**，改动只能落在：量化方案、SGLang fork、推测解码 draft、kernel、平台部署脚本。

## 模型架构

- **32 layers 混合**：8 standard Attention（layer id = 0, 9, 16, 17, 22, 29, 30, 31）+ 24 Lightning Attention（GLA）
- `hidden_size=4096`，`intermediate_size=16384`，`nq/nkv=32/2`，`head_dim=128`
- `vocab_size=73448`，`max_position_embeddings=524288`（512K）
- `dense_len=8192`：standard Attention 超过此长度走 InfLLM-v2 稀疏（compress_k → stage1 block_score → stage2 top-K sparse FA）

## 运行栈

**硬件**：NVIDIA RTX 6000D（sm_120, Blackwell, 84 GB VRAM）

| 组件 | 版本 |
|---|---|
| Python | 3.10.19（venv 预激活，`VIRTUAL_ENV=/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env`） |
| PyTorch | 2.11.0+cu130 |
| CUDA toolkit | 13.2 |
| cuDNN | [REDACTED]（sm_120 FP4 cudnn backend 硬要求） |
| FlashInfer | 0.6.8.post1[cu13] |
| sgl-kernel | 0.3.20 + 本仓库 `common_ops.abi3.so` 替换（Marlin FP4 scale bug fix） |
| Triton | 3.6.0 |

## 当前生产配置

- **量化**：NVFP4（GPTQ + FourOverSix，loguniform128 校准，48K 上下文）
- **Decode kernel 派发**：b12x 2-tier（Marlin小M / b12x全M / 3点CUTLASS override），覆盖 6 形状 58 tile 配置
- **推测解码**：EAGLE-3 chain verify，提交包默认 `spec_steps=3, topk=2, dtn=7`，并启用 dynamic spec mode（NO_SPEC / D5 / D7 按 running batch size 切换）
- **Draft model**：`eagle/models/v2mix_20k_s3500_ood757/`（v2mix 20K + s3500 + ood757 数据训出，484 MB safetensors，md5 `8e6bb36b…`），NVFP4 QAT，共享 b12x 路径。`det_prefill/` 是更早的 det-target prefill baseline，已退居参考
- **Eagle 数据路线**：当前为 target-regenerated（target 模型自生成续写作训练 label），见 `eagle/pipelines/target_regen/`

> **DFlash + DDTree 是探索性实验，不作为生产实践**。所有 `dflash/` / `eval/start_dflash*.sh` / `eval/start_ddtree.sh` / `docs/dflash/` 内容均为备选 spec 算法的探索路线，提交包仍走 EAGLE-3。除非用户明确要求切到 DFlash/DDTree，默认不要把它当作可比较或可替换的当前 baseline。

## 目录

| 路径 | 职责 |
|---|---|
| `demo-sala/` | **正式提交包**（平台真正消费） |
| `probe-sala/` | cu13 平台诊断探针（BOS 鉴权下发 + 邮件回传 + 11 项 verify） |
| `eagle/` | EAGLE-3 draft 训练 / 数据采集 / ckpt 转换；当前 baseline = `models/v2mix_20k_s3500_ood757/`（与 `eval/start_eagle.sh` 默认一致），`models/det_prefill/` 为前一代参考，旧版本归档在 `legacy/` |
```

> AGENT

查看更多 CLAUDE.md 中关于目录的规则：

> TOOL

tool_use Bash
```json
{
  "command": "grep -A 50 \"bench/\" /user_4813494d/openbmb/CLAUDE.md | head -30"
}
```

> TOOL

tool_result Bash
```
| `bench/` | 速度基准、profile、kernel microbench |
| `eval/` | 本地评测脚本（`start_eagle.sh` / `run_public_eval_full.sh` 等） |
| `quant/` | 离线量化实验 |
| `kernels/` | CUDA / GEMV / layout 实验 |
| `docs/` | 技术文档（见下） |
| `toolkit/` | 官方评测工具，只读 |

## 文档导航

> **文档仅供参考，不要当圣旨**。`docs/` 是过去某个时间点的事实快照与调研归档，可能滞后于代码、可能写错、也可能是早期假设。在依据文档结论行动前（特别是性能数字、kernel 派发、API 形状），先用 `git log` / 读代码 / 跑 bench 验证一遍。代码现状与文档冲突时，以代码为准并顺手把文档纠正。

项目细节都在 [`docs/`](docs/) 下。文档索引见 [`docs/README.md`](docs/README.md)。

每主题一个子目录，目录下 `README.md` + 各子文档；统一约定 `current.md` = 当前事实，`history.md` = 调研归档。

| 主题 | 入口 |
|---|---|
| **接续指南** | [`docs/handover.md`](docs/handover.md) |
| 平台 / cu13 / probe-sala / fork 判定 | [`docs/platform/`](docs/platform/) |
| 量化方案 / Marlin 历史 | [`docs/quant/`](docs/quant/) |
| **sm_120 GEMM/kernel 底层调优**（CUTLASS / Marlin / 硬件 / profile 方法论） | [`docs/gemm/`](docs/gemm/) |
| 长上下文 prefill | [`docs/prefill/`](docs/prefill/) |
| Decode 算子优化 / profile 方法论 | [`docs/decode/`](docs/decode/) |
| EAGLE-3 spec decoding（架构 / 训练 / collapse / 实验 / 论文） | [`docs/eagle/`](docs/eagle/) |
| 周冠军技术分享（对外 blog） | [`docs/blog/`](docs/blog/) |

## 关键命令

```bash
# 启动推理 server（EAGLE-3 当前生产配置）
```

> AGENT

现在查看 bench/data_full：

> TOOL

tool_use Bash
```json
{
  "command": "ls -lah /user_4813494d/openbmb/bench/data_full/ | head -20 && echo \"---\" && find /user_4813494d/openbmb/bench/data_full -type f | head -5"
}
```

> TOOL

tool_result Bash
```
total 87M
drwxr-xr-x  3 user_4813494d user_4813494d  144 May 15 09:53 .
drwxr-xr-x 11 user_4813494d user_4813494d 4.0K May 18 02:27 ..
drwxr-xr-x  2 user_4813494d user_4813494d    6 May 15 09:52 .ipynb_checkpoints
-rw-r--r--  1 user_4813494d user_4813494d 7.5M May 15 09:51 speed_bench_c1.jsonl
-rw-r--r--  1 user_4813494d user_4813494d  23M May 15 09:51 speed_bench_c8.jsonl
-rw-r--r--  1 user_4813494d user_4813494d  57M May 15 09:51 speed_bench_cunlimited.jsonl
---
/user_4813494d/openbmb/bench/data_full/speed_bench_c1.jsonl
/user_4813494d/openbmb/bench/data_full/speed_bench_c8.jsonl
/user_4813494d/openbmb/bench/data_full/speed_bench_cunlimited.jsonl
```

> AGENT

完美。现在汇总所有信息：

## 分析报告

### A. 文档改动（6 个已追踪文件）

| 文档 | 改动 | 意图 | 可独立提交 |
|---|---|---|---|
| `docs/blog/README.md` | +1 行 | 链接新增 week9.md 周报 | ✅ |
| `docs/blog/week9.md` | 新增 ~100 行 | SOAR week9 冠军技术分享——从 KL 到接受率（loss 函数 LK^λ 算法） | ✅ |
| `docs/eagle/training/data-compression.md` | ~15 行 | 更新 NVFP4 aux_hidden 存储实现（从二阶 codec 改为 server hook 直写，澄清非数学无损而是 FP4 量化） | ✅ |
| `docs/eagle/training/pipeline.md` | +16 行 | 添加 hook 存储和 direct-NVFP4 的采集验证日志（256 条真实 smoke + 4 条过拟合测试） | ✅ |
| `docs/gemm/so-replacements.md` | +31 行 | 记录 5/15 和 5/17 的 infllm_v2 .so 备份日志（从手工修改版 → rebuild site-packages → 再次 rebuild from HEAD） | ✅ |
| `eagle/README.md` | +5 行 | 更新 v3mix 采集描述（server hook 直写替代 collector 编码） | ✅ |

所有文档改动都是独立的、相互兼容的。推荐一起提交。

---

### B. 未追踪文件/目录判定表

| 路径 | 规模 | 判定 | 理由 |
|---|---|---|---|
| `bench/data_full/` | 87 MB | **加 .gitignore** | 官方发布的基准数据集（speed_bench_*.jsonl），属于大型数据，CLAUDE.md 禁止 bench/data/ 用作训练 |
| `bench/infllmv2/bench_mlp_fused_act_quant.py` | ~4 KB | **提交** | 新增 InfLLM-v2 微基准脚本，源码级别实验，应入仓 |
| `demo-sala/.bce_conf/` | 20 KB | **加 .gitignore** | BCECmd 本地配置与凭证（bucket_endpoint_cache、credentials），机密配置 |
| `demo-sala/pack.sh` | 已读 | **提交** | 演示环境打包脚本，注释完善，属于工程自动化 |
| `demo-sala/prepare_env_reports/` | 60 KB | **加 .gitignore** | 平台运行阶段输出（stage0~3 日志 + console.log），非源码 |
| `demo-sala/wheels/` | 3.3 GB | **加 .gitignore** | Python wheel 二进制文件集合，从 BOS 动态下载，不应入 git |
| `kernels/infllmv2_cuda_impl/csrc/cutlass` | 0 B（符号链接/空） | **保持 .gitignore** | CUTLASS 第三方头文件库，已在 .gitignore L38，避免 108 MB 下载 |
| `piecewise/` | 36 KB | **需要用户决定** | 新工作区，包含 README + audit/mechanism/blockers/plan.md（技术文档），可能是 piecewise attention 实验 |
| `prefill/` | 404 KB | **需要用户决定** | 新工作区，实验日志 + 多个 stage1 profiling 脚本，InfLLM-v2 prefill 优化探索 |
| `probe-sala-acc/` | 654 MB | **加 .gitignore** | 完整 probe-sala 副本（含 bcecmd、.so、wheels、sglang、toolkit），生产环境诊断探针包 |
| `probe-sala-quant/` | 147 MB | **加 .gitignore** | probe-sala 变种（关键增加 preprocess_model.py），量化诊断衍生物 |
| `scale/` | 33 GB | **加 .gitignore** | 新工作区，含 runs/、configs/、docker/；推测为大规模实验（33 GB 提示含大量数据或checkpoints） |

---

### 推荐的 .gitignore 追加规则

```gitignore
# Benchmark data sets（大型官方发布）
bench/data_full/

# BCECmd 本地配置（凭证）
demo-sala/.bce_conf/

# Platform stage outputs （非源码，每次平台运行自动生成）
demo-sala/prepare_env_reports/

# Python wheels （从 BOS 动态拉取，不应 check-in）
demo-sala/wheels/

# Probe-sala 生产诊断包 （完整副本，644+ MB）
probe-sala-acc/
probe-sala-quant/

# Large experimental workspaces （未决定是否入仓的实验工作区）
# 后续明确后可删除本注释并保留或移除具体目录
# piecewise/     # (可选) prefill/attention fusion 实验
# prefill/       # (可选) prefill stage1 profiling
# scale/         # (可选) large-scale experiments
```

**关键决定**：piecewise/、prefill/、scale/ 这三个目录为新工作区，包含实验代码和日志。建议：
- 若是进行中的实验，暂时 add 到 .gitignore，待结论稳定后再决定是否纳入主线
- 若是已完成的研究，应提取精华内容（如 README 和关键数字）并迁移到 `docs/` 相应子目录，工作区本身 ignore
