> DEVELOPER

我需要彻底搞清楚一个偶发的 CUDA illegal memory access crash,签名如下:

```
File "/tmp/submission_extract_1/probe-sala-full/sglang/python/sglang/srt/speculative/eagle_worker.py", line 788, in forward_batch_generation
    self.verify(batch, spec_info)
File ".../sglang/srt/speculative/eagle_worker.py", line 1846, in verify
    res: EagleVerifyOutput = spec_info.verify(
File ".../sglang/srt/speculative/eagle_info.py", line 515, in verify
    accept_index_cpu = accept_index.tolist()
torch.AcceleratorError: CUDA error: an illegal memory access was encountered
```

**背景上下文(必读才能给出有价值的分析):**

- 本地代码位置: `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/`
- 提交端代码位置: `/tmp/submission_extract_1/probe-sala-full/sglang/python/sglang/srt/speculative/`
- 这两份应当是对齐的(用户说"理论上和本地时对齐的")
- 项目背景: MiniCPM-SALA + EAGLE3 speculative + 自定义动态 spec mode (D5/D7/NO_SPEC) + per-request ngram routing (chain verify 与 EAGLE draft 混合到一个 EagleVerifyInput)
- 关键: `eagle_worker.py` 里 `_max_topk = max(d5_topk, d7_topk)`, `_max_spec_steps = max(d5_steps, d7_steps)`,cuda graph 按最大值 capture
- `_draft_ngram_route` (大约 line 1517) 实现 hit/miss 分支: hit→chain mask (`_build_ngram_chain_verify_input`), miss→EAGLE draft,两路合并成一个 `EagleVerifyInput` 交给 verify
- Hard coupling: `max_draft_tokens = min(NGRAM_MAX_DRAFT_TOKENS, dtn - 1)` (chain 长度被 D5/D7 的 dtn 卡)
- 我们已知 ngram_min_match=2 在长 context 上稳定崩,签名一模一样
- 现在 default config (MIN_MATCH=3) 在 probe-sala-full 上 ~50% 概率崩

**触发场景(从最近一次 crash log 提取):**
1. 单请求长 context (前面 Decode batch #running-req=1 多次,accept len 14~15,几乎到 dtn=15 上限,即 D7+ngram chain hit 满 chain)
2. 之后 Smax workload 涌入(96 个新 prefill batches 连续 prefill,8192 chunked-prefill)
3. 期间 schedule 切换 D7 → D5 → 可能 NO_SPEC
4. verify() 在 `accept_index.tolist()` 处 CUDA illegal memory access

**任务:**

仔细深入阅读以下文件,不要只看 grep 摘要,要看实际代码逻辑:

1. `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py` 的 `EagleVerifyInput.verify` 方法(line 515 周围 ±100行) […]

> AGENT

I'll conduct a systematic deep-dive analysis of this CUDA illegal memory access crash. Let me start by reading the critical files to understand the data flow.

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py",
  "offset": 400,
  "limit": 250
}
```

> TOOL

tool_result Read
```
400	            # apply temperature and get target probs
401	            expanded_temperature = torch.repeat_interleave(
402	                sampling_info.temperatures, self.draft_token_num, dim=0
403	            )  # (bs * draft_token_num, 1)
404	
405	            target_probs = F.softmax(
406	                logits_output.next_token_logits / expanded_temperature, dim=-1
407	            )  # (bs * draft_token_num, vocab_size)
408	            target_probs = top_k_renorm_prob(
409	                target_probs,
410	                torch.repeat_interleave(
411	                    sampling_info.top_ks, self.draft_token_num, dim=0
412	                ),
413	            )  # (bs * draft_token_num, vocab_size)
414	            if not torch.all(sampling_info.top_ps == 1.0):
415	                target_probs = top_p_renorm_prob(
416	                    target_probs,
417	                    torch.repeat_interleave(
418	                        sampling_info.top_ps, self.draft_token_num, dim=0
419	                    ),
420	                )
421	            target_probs = target_probs.reshape(bs, self.draft_token_num, -1)
422	
423	            draft_probs = torch.zeros(
424	                target_probs.shape, dtype=torch.float32, device=batch.device
425	            )
426	
427	            # coins for rejection sampling
428	            coins = torch.rand_like(
429	                candidates, dtype=torch.float32, device=batch.device
430	            )
431	            # coins for final sampling
432	            coins_for_final_sampling = torch.rand(
433	                (bs,), dtype=torch.float32, device=batch.device
434	            )
435	            tree_speculative_sampling_target_only(
436	                predicts=predict,  # mutable
437	                accept_index=accept_index,  # mutable
438	                accept_token_num=accept_length,  # mutable
439	                candidates=candidates,
440	                retrive_index=self.retrive_index,
441	                [REDACTED],
442	                retrive_next_sibling=self.retrive_next_sibling,
443	                uniform_samples=coins,
444	                uniform_samples_for_final_sampling=coins_for_final_sampling,
445	                target_probs=target_probs,
446	                draft_probs=draft_probs,
447	                threshold_single=get_global_server_args().speculative_accept_threshold_single,
448	                threshold_acc=get_global_server_args().speculative_accept_threshold_acc,
449	                deterministic=True,
450	            )
451	
452	        if SIMULATE_ACC_LEN > 0.0:
453	            # Do simulation
454	            accept_index = generate_simulated_accept_index(
455	                accept_index=accept_index,
456	                predict=predict,  # mutable
457	                accept_length=accept_length,  # mutable
458	                bs=bs, […]

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "offset": 1800,
  "limit": 100
}
```

> TOOL

tool_result Read
```
1800	            )
1801	            assert model_worker_batch.capture_hidden_mode == spec_info.capture_hidden_mode
1802	
1803	        if batch.has_grammar:
1804	            retrieve_next_token_cpu = spec_info.retrive_next_token.cpu()
1805	            retrieve_next_sibling_cpu = spec_info.retrive_next_sibling.cpu()
1806	            draft_tokens_cpu = spec_info.draft_token.view(
1807	                spec_info.retrive_next_token.shape
1808	            ).cpu()
1809	
1810	        # Forward
1811	        with _profile_region("EW_target_verify_forward"):
1812	            batch_result = self.target_worker.forward_batch_generation(
1813	                model_worker_batch, is_verify=True
1814	            )
1815	        logits_output, can_run_cuda_graph = (
1816	            batch_result.logits_output,
1817	            batch_result.can_run_cuda_graph,
1818	        )
1819	        _ngram_debug_cuda_sync("target_verify_forward")
1820	
1821	        vocab_mask = None
1822	        if batch.has_grammar:
1823	            # Generate the logit mask for structured output.
1824	            # Overlap the CPU operations for bitmask generation with the forward pass.
1825	            vocab_mask = generate_token_bitmask(
1826	                batch.reqs,
1827	                spec_info,
1828	                retrieve_next_token_cpu,
1829	                retrieve_next_sibling_cpu,
1830	                draft_tokens_cpu,
1831	                batch.sampling_info.vocab_size,
1832	            )
1833	
1834	            if vocab_mask is not None:
1835	                assert spec_info.grammar is not None
1836	                vocab_mask = vocab_mask.to(spec_info.retrive_next_token.device)
1837	                # NOTE (sk): otherwise, this vocab mask will be the one from the previous extend stage
1838	                # and will be applied to produce wrong results
1839	                batch.sampling_info.vocab_mask = None
1840	
1841	        if self.enable_nan_detection:
1842	            detect_nan(logits_output)
1843	
1844	        spec_info.hidden_states = logits_output.hidden_states
1845	        with _profile_region("EW_verify_post_accept"):
1846	            res: EagleVerifyOutput = spec_info.verify(
1847	                batch,
1848	                logits_output,
1849	                self.token_to_kv_pool_allocator,
1850	                self.page_size,
1851	                vocab_mask,
1852	            )
1853	        _ngram_debug_cuda_sync("verify_accept_and_kv")
1854	
1855	        # Post process based on verified outputs.
1856	        # Pick […]

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "offset": 1500,
  "limit": 150
}
```

> TOOL

tool_result Read
```
1500	        return EagleVerifyInput(
1501	            draft_token=draft_tokens,
1502	            custom_mask=tree_mask,
1503	            positions=positions,
1504	            retrive_index=retrive_index,
1505	            [REDACTED],
1506	            retrive_next_sibling=retrive_next_sibling,
1507	            retrive_cum_len=None,
1508	            spec_steps=max(self.speculative_num_steps, dtn - 1),
1509	            topk=self.topk,
1510	            draft_token_num=dtn,
1511	            capture_hidden_mode=CaptureHiddenMode.FULL,
1512	            seq_lens_sum=seq_lens_sum,
1513	            seq_lens_cpu=seq_lens_cpu,
1514	            mars_theta=self._active_mars_theta,
1515	        )
1516	
1517	    def _draft_ngram_route(self, batch: ScheduleBatch) -> Optional[EagleVerifyInput]:
1518	        dtn = self.speculative_num_draft_tokens
1519	        max_draft_tokens = min(self.ngram_route_max_draft_tokens, dtn - 1)
1520	        if max_draft_tokens <= 0:
1521	            return None
1522	
1523	        ngram_drafts = [
1524	            self._lookup_req_ngram_draft(req, max_draft_tokens)
1525	            for req in batch.reqs
1526	        ]
1527	        hit_indices = [i for i, draft in enumerate(ngram_drafts) if draft]
1528	        if not hit_indices:
1529	            return None
1530	
1531	        bs = len(batch.reqs)
1532	        hit_index_set = set(hit_indices)
1533	        miss_indices = [i for i in range(bs) if i not in hit_index_set]
1534	        miss_spec_info = None
1535	        miss_batch = None
1536	        if miss_indices:
1537	            miss_batch = self._make_ngram_route_subbatch(batch, miss_indices)
1538	            miss_spec_info = self._draft_eagle_verify_input(miss_batch)
1539	            _ngram_debug_cuda_sync("route_miss_eagle_draft")
1540	            batch.out_cache_loc = miss_batch.out_cache_loc
1541	        else:
1542	            batch.out_cache_loc = None
1543	
1544	        self._ngram_route_step_ct += bs
1545	        self._ngram_route_hit_ct += len(hit_indices)
1546	        if len(hit_indices) == bs:
1547	            self._ngram_route_all_hit_ct += 1
1548	        elif hit_indices:
1549	            self._ngram_route_mixed_ct += 1
1550	        if (
1551	            self._ngram_route_log_every > 0
1552	            and self._ngram_route_step_ct >= self._ngram_route_log_every
1553	        ):
1554	            logger.info(
1555	                "[eagle-ngram-route] req_steps=%d hit_req_steps=%d "
1556 […]

> AGENT

Now let me read the critical sections around accept_index computation and the ngram chain verify building:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py",
  "offset": 1,
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	import json
2	import logging
3	import os
4	import threading
5	from copy import copy
6	from dataclasses import dataclass
7	from typing import ClassVar, List, Optional, Tuple
8	
9	import torch
10	import torch.nn.functional as F
11	
12	
13	_EAGLE_TRACE_PATH = os.environ.get("EAGLE_TRACE_FILE")
14	_EAGLE_TRACE_FD = None
15	_EAGLE_TRACE_LOCK = threading.Lock()
16	
17	# Collapse instrumentation: per-rid consecutive al==0 counter. When a request
18	# stays in al==0 for >= EAGLE_COLLAPSE_LOG_K consecutive verify steps, log a
19	# warning. Pure visibility — does NOT alter spec behavior. Use to monitor
20	# collapse frequency on production traffic. Default K=10 so noise stays low.
21	_COLLAPSE_COUNTERS: dict = {}
22	_COLLAPSE_LOG_K = int(os.environ.get("EAGLE_COLLAPSE_LOG_K", "10"))
23	_COLLAPSE_LOG_LOCK = threading.Lock()
24	_FORCE_NO_ACCEPT = os.environ.get("EAGLE_FORCE_NO_ACCEPT", "0") == "1"
25	_FUSE_VERIFY_ACCEPT_COMPACT = (
26	    os.environ.get("SGLANG_EAGLE_FUSE_VERIFY_ACCEPT_COMPACT", "1") == "1"
27	)
28	_FUSE_VERIFY_FREE_SLOTS = (
29	    os.environ.get("SGLANG_EAGLE_FUSE_VERIFY_FREE_SLOTS", "1") == "1"
30	)
31	_DRAFT_EXTEND_CPU_INDPTR = (
32	    os.environ.get("SGLANG_EAGLE_DRAFT_EXTEND_CPU_INDPTR", "1") == "1"
33	)
34	# MARS verify (arXiv:2601.15498): theta < 0 disables, default. Recommended 0.9.
35	_MARS_THETA = float(os.environ.get("EAGLE_MARS_THETA", "-1.0"))
36	
37	
38	def _eagle_trace_emit(rec: dict):
39	    global _EAGLE_TRACE_FD
40	    if not _EAGLE_TRACE_PATH:
41	        return
42	    with _EAGLE_TRACE_LOCK:
43	        if _EAGLE_TRACE_FD […]

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py",
  "offset": 100,
  "limit": 150
}
```

> TOOL

tool_result Read
```
100	    retrive_index: torch.Tensor
101	    retrive_next_token: torch.Tensor
102	    retrive_next_sibling: torch.Tensor
103	    retrive_cum_len: torch.Tensor
104	    spec_steps: int
105	    topk: int
106	    draft_token_num: int
107	    capture_hidden_mode: CaptureHiddenMode
108	    seq_lens_sum: int
109	    seq_lens_cpu: torch.Tensor
110	    grammar: BaseGrammarObject = None
111	
112	    # Shape info for padding
113	    num_tokens_per_batch: int = -1
114	    # Per-mode MARS verify theta. Negative = use module-level _MARS_THETA
115	    # fallback; MARS is disabled only when the effective theta is negative.
116	    # Set by EAGLEWorker._apply_spec_config from EAGLE_D{5,7}_MARS_THETA env so
117	    # D5/D7 can run different thresholds without a module-level global write.
118	    mars_theta: float = -1.0
119	
120	    def __post_init__(self):
121	        super().__init__(SpecInputType.EAGLE_VERIFY)
122	
123	    def get_spec_adjust_token_coefficient(self) -> Tuple[int, int]:
124	        return self.draft_token_num, self.draft_token_num
125	
126	    @classmethod
127	    def create_idle_input(cls, topk: int, spec_steps: int, num_verify_tokens: int):
128	        return cls(
129	            draft_token=torch.empty((0,), dtype=torch.long, device="cuda"),
130	            custom_mask=torch.full((0,), True, dtype=torch.bool, device="cuda"),
131	            positions=torch.empty((0,), dtype=torch.int64, device="cuda"),
132	            retrive_index=torch.full(
133	                (0, num_verify_tokens), -1, dtype=torch.long, device="cuda"
134	            ),
135	            retrive_next_token=torch.full(
136	                (0, num_verify_tokens), -1, dtype=torch.long, device="cuda"
137	            ),
138	            retrive_next_sibling=torch.full(
139	                (0, num_verify_tokens), -1, dtype=torch.long, device="cuda"
140	            ),
141	            retrive_cum_len=None,
142	            topk=topk,
143	            draft_token_num=num_verify_tokens,
144	            spec_steps=spec_steps,
145	            capture_hidden_mode=CaptureHiddenMode.FULL,
146	            seq_lens_sum=0,
147	            seq_lens_cpu=torch.empty((0,), dtype=torch.int32),
148	        )
149	
150	    def prepare_for_verify(self, batch: ScheduleBatch, page_size: int): […]

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "offset": 1390,
  "limit": 200
}
```

> TOOL

tool_result Read
```
1390	        self,
1391	        tree_mask: torch.Tensor,
1392	        offset: int,
1393	        seq_len: int,
1394	        dtn: int,
1395	        chain_len: int,
1396	    ) -> None:
1397	        row_width = seq_len + dtn
1398	        tree_mask[offset : offset + dtn * row_width].fill_(True)
1399	        for q in range(dtn):
1400	            tree_start = offset + q * row_width + seq_len
1401	            tree_mask[tree_start : tree_start + dtn].fill_(False)
1402	            visible_to = min(q, chain_len)
1403	            tree_mask[tree_start : tree_start + visible_to + 1].fill_(True)
1404	
1405	    def _build_ngram_chain_verify_input(
1406	        self,
1407	        batch: ScheduleBatch,
1408	        ngram_drafts: List[Optional[List[int]]],
1409	        miss_indices: List[int],
1410	        miss_spec_info: Optional[EagleVerifyInput],
1411	    ) -> EagleVerifyInput:
1412	        bs = len(batch.reqs)
1413	        dtn = self.speculative_num_draft_tokens
1414	        device = batch.seq_lens.device
1415	        seq_lens_cpu = batch.seq_lens_cpu
1416	        seq_lens_sum = int(seq_lens_cpu.sum().item())
1417	
1418	        draft_tokens = torch.empty((bs * dtn,), dtype=torch.long, device=device)
1419	        positions = torch.empty((bs * dtn,), dtype=torch.long, device=device)
1420	        retrive_index = torch.empty((bs, dtn), dtype=torch.long, device=device)
1421	        retrive_next_token = torch.full((bs, dtn), -1, dtype=torch.long, device=device)
1422	        retrive_next_sibling = torch.full((bs, dtn), -1, dtype=torch.long, device=device)
1423	        tree_mask = torch.empty(
1424	            (seq_lens_sum * dtn + dtn * dtn * bs,),
1425	            dtype=torch.bool,
1426	            device=device,
1427	        )
1428	
1429	        draft_view = draft_tokens.view(bs, dtn)
1430	        pos_view = positions.view(bs, dtn)
1431	        verified_id_cpu = [
1432	            int(req.output_ids[-1] if req.output_ids else req.origin_input_ids[-1])
1433	            for req in batch.reqs […]

> AGENT

Now let me read the `_lookup_req_ngram_draft` and `_mask_row_offset` methods:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "offset": 1270,
  "limit": 150
}
```

> TOOL

tool_result Read
```
1270	            or cached_origin_len != origin_len
1271	            or cached_output_len < 0
1272	            or cached_output_len > output_len
1273	        ):
1274	            cached = "".join(
1275	                chr(int(x) + _NGRAM_TOKEN_BASE)
1276	                for x in (req.origin_input_ids + req.output_ids)
1277	            )
1278	            req._eagle_ngram_origin_len = origin_len
1279	            req._eagle_ngram_output_len = output_len
1280	            req._eagle_ngram_token_str = cached
1281	            return cached
1282	
1283	        if cached_output_len < output_len:
1284	            cached += "".join(
1285	                chr(int(x) + _NGRAM_TOKEN_BASE)
1286	                for x in req.output_ids[cached_output_len:]
1287	            )
1288	            req._eagle_ngram_output_len = output_len
1289	            req._eagle_ngram_token_str = cached
1290	        return cached
1291	
1292	    def _lookup_req_ngram_draft(self, req, max_draft_tokens: int):
1293	        if max_draft_tokens <= 0:
1294	            return None
1295	        token_str = self._get_req_ngram_str(req)
1296	        total_len = len(token_str)
1297	        if total_len < self.ngram_route_min_match:
1298	            return None
1299	
1300	        max_match = min(self.ngram_route_max_match, total_len)
1301	        for n in range(max_match, self.ngram_route_min_match - 1, -1):
1302	            query_start = total_len - n
1303	            pos = token_str.rfind(token_str[query_start:total_len], 0, query_start)
1304	            if pos < 0:
1305	                continue
1306	            draft_start = pos + n
1307	            available = total_len - draft_start
1308	            if available <= 0:
1309	                continue
1310	            draft_chars = token_str[
1311	                draft_start : draft_start + min(max_draft_tokens, available)
1312	            ]
1313	            if draft_chars:
1314	                return [ord(ch) - _NGRAM_TOKEN_BASE for ch in draft_chars]
1315	        return None
1316	
1317	    def _make_ngram_route_subbatch(self, […]

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "offset": 1350,
  "limit": 80
}
```

> TOOL

tool_result Read
```
1350	            "hidden_states",
1351	            "verified_id",
1352	            "accept_length",
1353	            "seq_lens_for_draft_extend",
1354	            "req_pool_indices_for_draft_extend",
1355	        ):
1356	            value = getattr(spec_info, name, None)
1357	            if isinstance(value, torch.Tensor) and value.shape[:1] == (len(batch.reqs),):
1358	                setattr(sub_spec_info, name, value[index_device])
1359	        if isinstance(spec_info.seq_lens_for_draft_extend_cpu, torch.Tensor) and (
1360	            spec_info.seq_lens_for_draft_extend_cpu.shape[:1] == (len(batch.reqs),)
1361	        ):
1362	            sub_spec_info.seq_lens_for_draft_extend_cpu = (
1363	                spec_info.seq_lens_for_draft_extend_cpu[indices]
1364	            )
1365	        if (
1366	            spec_info.accept_length_cpu is not None
1367	            and len(spec_info.accept_length_cpu) == len(batch.reqs)
1368	        ):
1369	            sub_spec_info.accept_length_cpu = [
1370	                spec_info.accept_length_cpu[i] for i in indices
1371	            ]
1372	        if (
1373	            spec_info.request_keep_indices is not None
1374	            and len(spec_info.request_keep_indices) == len(batch.reqs)
1375	        ):
1376	            sub_spec_info.request_keep_indices = [
1377	                spec_info.request_keep_indices[i] for i in indices
1378	            ]
1379	        sub.spec_info = sub_spec_info
1380	        return sub
1381	
1382	    def _mask_row_offset(self, seq_lens_cpu: torch.Tensor, row: int, dtn: int) -> int:
1383	        if row == 0:
1384	            prefix = 0
1385	        else:
1386	            prefix = int(seq_lens_cpu[:row].sum().item())
1387	        return prefix * dtn + row * dtn * dtn
1388	
1389	    def _fill_ngram_chain_mask_row(
1390	        self,
1391	        tree_mask: torch.Tensor,
1392	        offset: int,
1393	        seq_len: int,
1394	        dtn: int,
1395	        chain_len: int,
1396	    ) -> None:
1397	        row_width = seq_len + dtn
1398	        tree_mask[offset : offset + dtn * row_width].fill_(True)
1399	        for q in range(dtn):
1400	            tree_start = offset […]

> TOOL

tool_use bash
```json
{
  "command": "grep -n \"_mask_row_offset\\|_lookup_req_ngram_draft\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py | head -20"
}
```

> TOOL

tool_result bash
```
<tool_use_error>Error: No such tool available: bash</tool_use_error>
```

> AGENT

Let me search for the accept_index computation in the tree_speculative_sampling kernel call:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py",
  "offset": 270,
  "limit": 200
}
```

> TOOL

tool_result Read
```
270	        vocab_mask: Optional[torch.Tensor] = None,  # For grammar
271	    ) -> torch.Tensor:
272	        """
273	        Verify and find accepted tokens based on logits output and batch
274	        (which contains spec decoding information).
275	
276	        WARNING: This API in-place modifies the states of logits_output
277	
278	        This API updates values inside logits_output based on the accepted
279	        tokens. I.e., logits_output.next_token_logits only contains
280	        accepted token logits.
281	        """
282	        if batch.forward_mode.is_idle():
283	            return EagleVerifyOutput(
284	                draft_input=EagleDraftInput.create_idle_input(
285	                    device=batch.device,
286	                    hidden_size=batch.model_config.hidden_size,
287	                    dtype=batch.model_config.dtype,
288	                    topk=self.topk,
289	                    capture_hidden_mode=CaptureHiddenMode.LAST,
290	                ),
291	                logits_output=logits_output,
292	                verified_id=torch.empty(0, dtype=torch.long, device=batch.device),
293	                accept_length_per_req_cpu=[],
294	                accepted_indices=torch.full(
295	                    (0, self.spec_steps + 1),
296	                    -1,
297	                    dtype=torch.int32,
298	                    device=batch.device,
299	                ),
300	            )
301	
302	        bs = self.retrive_index.shape[0]
303	        candidates = self.draft_token.reshape(bs, self.draft_token_num)
304	        sampling_info = batch.sampling_info
305	
306	        predict_shape = list(logits_output.next_token_logits.shape)[:-1]
307	        predict_shape[-1] += 1
308	        predict = torch.empty(predict_shape, dtype=torch.int32, device=batch.device)
309	        accept_index = torch.full(
310	            (bs, self.spec_steps + 1), -1, dtype=torch.int32, device=batch.device
311	        )
312	        accept_length = torch.empty((bs,), dtype=torch.int32, device=batch.device)
313	
314	        if bs != len(sampling_info):
315	            sampling_info = copy.deepcopy(sampling_info)
316	            # NOTE: retrive_index are the indices of the requests that are kept.
317	            sampling_info.filter_batch(self.retrive_index.tolist(), self.retrive_index)
318	
319	        # Apply the custom logit processors if registered […]

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py",
  "offset": 250,
  "limit": 120
}
```

> TOOL

tool_result Read
```
250	                [
251	                    self.custom_mask,
252	                    torch.full(
253	                        (mask_numel - self.custom_mask.numel(),),
254	                        True,
255	                        dtype=torch.bool,
256	                        device=device,
257	                    ),
258	                ],
259	                dim=0,
260	            )
261	
262	        return kv_indices, cum_kv_seq_len, qo_indptr, self.custom_mask
263	
264	    def verify(
265	        self,
266	        batch: ScheduleBatch,
267	        logits_output: LogitsProcessorOutput,
268	        token_to_kv_pool_allocator: BaseTokenToKVPoolAllocator,
269	        page_size: int,
270	        vocab_mask: Optional[torch.Tensor] = None,  # For grammar
271	    ) -> torch.Tensor:
272	        """
273	        Verify and find accepted tokens based on logits output and batch
274	        (which contains spec decoding information).
275	
276	        WARNING: This API in-place modifies the states of logits_output
277	
278	        This API updates values inside logits_output based on the accepted
279	        tokens. I.e., logits_output.next_token_logits only contains
280	        accepted token logits.
281	        """
282	        if batch.forward_mode.is_idle():
283	            return EagleVerifyOutput(
284	                draft_input=EagleDraftInput.create_idle_input(
285	                    device=batch.device,
286	                    hidden_size=batch.model_config.hidden_size,
287	                    dtype=batch.model_config.dtype,
288	                    topk=self.topk,
289	                    capture_hidden_mode=CaptureHiddenMode.LAST,
290	                ),
291	                logits_output=logits_output,
292	                verified_id=torch.empty(0, dtype=torch.long, device=batch.device),
293	                accept_length_per_req_cpu=[],
294	                accepted_indices=torch.full(
295	                    (0, self.spec_steps + 1),
296	                    -1,
297	                    dtype=torch.int32,
298	                    device=batch.device,
299	                ),
300	            )
301	
302	        bs = self.retrive_index.shape[0]
303	        candidates = self.draft_token.reshape(bs, self.draft_token_num)
304	        sampling_info = batch.sampling_info
305	
306	        predict_shape = list(logits_output.next_token_logits.shape)[:-1]
307	        predict_shape[-1] += 1
308	        predict = torch.empty(predict_shape, dtype=torch.int32, device=batch.device)
309	        accept_index = torch.full(
310	            (bs, self.spec_steps […]

> AGENT

Now let me check how the dynamic spec mode (D5/D7/NO_SPEC) impacts shape consistency:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/spec_mode.py",
  "offset": 1,
  "limit": 150
}
```

> TOOL

tool_result Read
```
1	"""Dynamic speculative-decoding mode selection for MiniCPM-SALA.
2	
3	Picks one of three modes per decode step based on the running batch size:
4	
5	    NO_SPEC      : bs >= EAGLE_NO_SPEC_BS         (target_worker direct decode)
6	    MARS_D5      : default spec config            (chain verify, dtn=5 by default)
7	    MARS_D7      : bs <= EAGLE_D7_BS              (chain verify, dtn=7 by default)
8	
9	Hysteresis (separate enter/leave thresholds) prevents prefill bursts from
10	flipping NO_SPEC mid-bench. Bench traffic is monotonically decreasing on bs,
11	so transitions are essentially one-way: NO_SPEC -> MARS_D5 -> MARS_D7.
12	
13	All thresholds and per-mode spec parameters are env-driven so we can sweep
14	without rebuilding. Enable with EAGLE_DYNAMIC_MODE=1.
15	"""
16	
17	import enum
18	import logging
19	import os
20	from dataclasses import dataclass
21	
22	logger = logging.getLogger(__name__)
23	
24	
25	class SpecMode(enum.Enum):
26	    NO_SPEC = "no_spec"
27	    MARS_D5 = "mars_d5"
28	    MARS_D7 = "mars_d7"
29	
30	
31	@dataclass(frozen=True)
32	class SpecModeConfig:
33	    enabled: bool
34	    enter_no_spec_bs: int
35	    leave_no_spec_bs: int
36	    enter_d7_bs: int
37	    leave_d7_bs: int
38	    d5_topk: int
39	    d5_steps: int
40	    d5_dtn: int
41	    d7_topk: int
42	    d7_steps: int
43	    d7_dtn: int
44	    mars_theta: float          # global fallback (legacy EAGLE_MARS_THETA)
45	    d5_mars_theta: float […]

> TOOL

tool_use bash
```json
{
  "command": "find /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative -name \"*.py\" -type f | head -15"
}
```

> TOOL

tool_result bash
```
<tool_use_error>Error: No such tool available: bash</tool_use_error>
```

> AGENT

Let me search for the critical invariant about tree_mask size calculation and how it could overflow:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "offset": 1410,
  "limit": 100
}
```

> TOOL

tool_result Read
```
1410	        miss_spec_info: Optional[EagleVerifyInput],
1411	    ) -> EagleVerifyInput:
1412	        bs = len(batch.reqs)
1413	        dtn = self.speculative_num_draft_tokens
1414	        device = batch.seq_lens.device
1415	        seq_lens_cpu = batch.seq_lens_cpu
1416	        seq_lens_sum = int(seq_lens_cpu.sum().item())
1417	
1418	        draft_tokens = torch.empty((bs * dtn,), dtype=torch.long, device=device)
1419	        positions = torch.empty((bs * dtn,), dtype=torch.long, device=device)
1420	        retrive_index = torch.empty((bs, dtn), dtype=torch.long, device=device)
1421	        retrive_next_token = torch.full((bs, dtn), -1, dtype=torch.long, device=device)
1422	        retrive_next_sibling = torch.full((bs, dtn), -1, dtype=torch.long, device=device)
1423	        tree_mask = torch.empty(
1424	            (seq_lens_sum * dtn + dtn * dtn * bs,),
1425	            dtype=torch.bool,
1426	            device=device,
1427	        )
1428	
1429	        draft_view = draft_tokens.view(bs, dtn)
1430	        pos_view = positions.view(bs, dtn)
1431	        verified_id_cpu = [
1432	            int(req.output_ids[-1] if req.output_ids else req.origin_input_ids[-1])
1433	            for req in batch.reqs
1434	        ]
1435	
1436	        miss_row_by_index = {idx: row for row, idx in enumerate(miss_indices)}
1437	        miss_draft_view = (
1438	            miss_spec_info.draft_token.view(len(miss_indices), dtn)
1439	            if miss_spec_info is not None
1440	            else None
1441	        )
1442	        miss_pos_view = (
1443	            miss_spec_info.positions.view(len(miss_indices), dtn)
1444	            if miss_spec_info is not None
1445	            else None
1446	        )
1447	
1448	        for i in range(bs):
1449	            full_offset = self._mask_row_offset(seq_lens_cpu, i, dtn)
1450	            row_len = int(seq_lens_cpu[i].item()) + dtn
1451	            if i in miss_row_by_index:
1452	                miss_row = miss_row_by_index[i]
1453	                draft_view[i].copy_(miss_draft_view[miss_row])
1454	                pos_view[i].copy_(miss_pos_view[miss_row])
1455	                delta = (i […]

> AGENT

Perfect! Now I've found a critical insight. Let me trace through the logic and verify my hypothesis by checking the initialization of EAGLE worker parameters:

> TOOL

tool_use bash
```json
{
  "command": "grep -n \"speculative_num_draft_tokens\\|_max_topk\\|_max_spec_steps\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py | head -30"
}
```

> TOOL

tool_result bash
```
<tool_use_error>Error: No such tool available: bash</tool_use_error>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "offset": 1,
  "limit": 120
}
```

> TOOL

tool_result Read
```
1	import logging
2	import os
3	import time
4	from contextlib import nullcontext
5	from copy import copy
6	from typing import List, Optional, Tuple
7	
8	import torch
9	import torch._dynamo
10	import triton
11	import triton.language as tl
12	
13	# select_top_k_tokens (spec_utils.py) is @torch.compile(dynamic=True) and gets
14	# specialized per (i, hidden_states is None, dtn, topk) combo. Dynamic spec
15	# mode (D5+D7+NO_SPEC, multiple capture_bs) easily blows past the default
16	# recompile_limit=8 → dynamo gives up and runs eager (1-4% loss/step). 32 is
17	# a safe ceiling that fits all current specializations.
18	torch._dynamo.config.recompile_limit = 32
19	
20	_EAGLE_PROFILE_RECORD = os.getenv("EAGLE_PROFILE_RECORD", "0") == "1"
21	_FUSE_MAMBA_VERIFY_METADATA = (
22	    os.getenv("SGLANG_EAGLE_FUSE_MAMBA_VERIFY_METADATA", "1") == "1"
23	)
24	_NO_SPEC_ASYNC_NEXT_TOKEN_CPU = (
25	    os.getenv("SGLANG_EAGLE_NO_SPEC_ASYNC_NEXT_TOKEN_CPU", "1") == "1"
26	)
27	_NGRAM_TOKEN_BASE = 0x10000
28	_NGRAM_DEBUG_SYNC = os.getenv("SGLANG_EAGLE_NGRAM_DEBUG_SYNC", "0") == "1"
29	
30	
31	def _profile_region(name: str):
32	    return torch.profiler.record_function(name) if _EAGLE_PROFILE_RECORD else nullcontext()
33	
34	
35	def _env_int(name: str, default: int) -> int:
36	    raw = os.getenv(name)
37	    if raw is None or raw == "":
38	        return default
39	    try:
40	        return int(raw)
41	    except ValueError:
42	        logger.warning("%s=%r is not an int; using […]

> AGENT

Let me search for the EAGLEWorker __init__ method:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "offset": 700,
  "limit": 300
}
```

> TOOL

tool_result Read
```
700	        else:
701	            # Legacy single-runner path (preserves pre-dynamic behaviour).
702	            if self.speculative_num_steps > 1:
703	                tic = time.perf_counter()
704	                before_mem = get_available_gpu_memory(self.device, self.gpu_id)
705	                logger.info(
706	                    f"Capture draft cuda graph begin. This can take up to several minutes. avail mem={before_mem:.2f} GB"
707	                )
708	                self.cuda_graph_runner = Runner(self)
709	                after_mem = get_available_gpu_memory(self.device, self.gpu_id)
710	                logger.info(
711	                    f"Capture draft cuda graph end. Time elapsed: {time.perf_counter() - tic:.2f} s. mem usage={(before_mem - after_mem):.2f} GB. avail mem={after_mem:.2f} GB."
712	                )
713	
714	        # Capture extend
715	        if self.draft_extend_attn_backend and not _is_npu:
716	            tic = time.perf_counter()
717	            before_mem = get_available_gpu_memory(self.device, self.gpu_id)
718	            logger.info(
719	                f"Capture draft extend cuda graph begin. This can take up to several minutes. avail mem={before_mem:.2f} GB"
720	            )
721	            self.cuda_graph_runner_for_draft_extend = EAGLEDraftExtendCudaGraphRunner(
722	                self
723	            )
724	            after_mem = get_available_gpu_memory(self.device, self.gpu_id)
725	            logger.info(
726	                f"Capture draft extend cuda graph end. Time elapsed: {time.perf_counter() - tic:.2f} s. mem usage={(before_mem - after_mem):.2f} GB. avail mem={after_mem:.2f} GB."
727	            )
728	
729	    @property
730	    def draft_model_runner(self):
731	        return self.model_runner
732	
733	    def forward_batch_generation(self, batch: ScheduleBatch) -> GenerationBatchResult:
734	        """Run speculative decoding forward.
735	
736	        NOTE: Many states of batch is modified as you go through. It is not guaranteed that
737 […]

> AGENT

Now let me find where _max_topk and _max_spec_steps are set:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "offset": 550,
  "limit": 200
}
```

> TOOL

tool_result Read
```
550	            ).create_decode_backend()
551	            self.draft_attn_backend_d7 = DraftBackendFactory(
552	                self.server_args,
553	                self.draft_model_runner,
554	                cfg.d7_topk,
555	                cfg.d7_steps,
556	            ).create_decode_backend()
557	            self.draft_attn_backend = self.draft_attn_backend_d5
558	            draft_extend_factory = DraftBackendFactory(
559	                self.server_args,
560	                self.draft_model_runner,
561	                self._max_topk,
562	                self._max_spec_steps,
563	            )
564	        else:
565	            draft_backend_factory = DraftBackendFactory(
566	                self.server_args,
567	                self.draft_model_runner,
568	                self.topk,
569	                self.speculative_num_steps,
570	            )
571	            self.draft_attn_backend_d5 = None
572	            self.draft_attn_backend_d7 = None
573	            self.draft_attn_backend = draft_backend_factory.create_decode_backend()
574	            draft_extend_factory = draft_backend_factory
575	
576	        # Initialize draft extend attention backend (respects speculative_attention_mode setting)
577	        self.draft_extend_attn_backend = (
578	            draft_extend_factory.create_draft_extend_backend()
579	        )
580	
581	        self.draft_model_runner.draft_attn_backend = self.draft_attn_backend
582	
583	    def init_cuda_graphs(self):
584	        """Capture cuda graphs.
585	
586	        With ``spec_mode_config.enabled``, captures one runner per active spec
587	        mode (D5 + D7). Each runner owns its own input buffers (sized to its
588	        own ``topk * spec_steps``); the underlying draft attn_backend is shared
589	        and ``init_cuda_graph_state`` is invoked exactly once on the largest
590	        runner so its buffer pool covers both modes.
591	        """
592	        self.cuda_graph_runner = None  # active runner; mutated by _apply_spec_config
593	        self.cuda_graph_runner_d5 = None
594	        self.cuda_graph_runner_d7 = None
595	        self.cuda_graph_runner_for_draft_extend = None
596	
597	        if self.server_args.disable_cuda_graph:
598	            return
599	
600	        Device2DraftCudaGraphRunner = {
601	            "npu": EAGLEDraftNpuGraphRunner,
602	            "cuda": EAGLEDraftCudaGraphRunner,
603	        }
604 […]

> AGENT

Now let me find where _max_topk and _max_spec_steps are initialized:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "offset": 440,
  "limit": 130
}
```

> TOOL

tool_result Read
```
440	            self._max_topk = max(
441	                self.spec_mode_config.d5_topk, self.spec_mode_config.d7_topk
442	            )
443	            # Force attention-backend factory to size for the largest mode.
444	            backup_steps = self.speculative_num_steps
445	            backup_topk = self.topk
446	            self.speculative_num_steps = self._max_spec_steps
447	            self.topk = self._max_topk
448	        else:
449	            self._max_spec_steps = self.speculative_num_steps
450	            self._max_topk = self.topk
451	            backup_steps = self.speculative_num_steps
452	            backup_topk = self.topk
453	
454	        self.ngram_route_enabled = (
455	            os.getenv("SGLANG_EAGLE_NGRAM_ROUTE", "0") == "1"
456	        )
457	        self.ngram_route_min_match = _env_int("SGLANG_EAGLE_NGRAM_MIN_MATCH", 5)
458	        self.ngram_route_max_match = _env_int("SGLANG_EAGLE_NGRAM_MAX_MATCH", 12)
459	        self.ngram_route_max_draft_tokens = _env_int(
460	            "SGLANG_EAGLE_NGRAM_MAX_DRAFT_TOKENS", 15
461	        )
462	        self._ngram_route_step_ct = 0
463	        self._ngram_route_hit_ct = 0
464	        self._ngram_route_mixed_ct = 0
465	        self._ngram_route_all_hit_ct = 0
466	        self._ngram_route_log_every = _env_int(
467	            "SGLANG_EAGLE_NGRAM_LOG_EVERY", 1000
468	        )
469	        self.max_draft_extend_tokens_per_bs = self.speculative_num_steps + 1
470	        if self.ngram_route_enabled:
471	            if self.spec_mode_config.enabled:
472	                self.max_draft_extend_tokens_per_bs = max(
473	                    self.max_draft_extend_tokens_per_bs,
474	                    self.spec_mode_config.d5_dtn,
475	                    self.spec_mode_config.d7_dtn,
476	                )
477	            self.max_draft_extend_tokens_per_bs = max(
478	                self.max_draft_extend_tokens_per_bs,
479	                min(
480	                    self.ngram_route_max_draft_tokens + 1,
481	                    max(
482	                        self.speculative_num_draft_tokens,
483	                        getattr(self.spec_mode_config, "d5_dtn", 0),
484	                        getattr(self.spec_mode_config, "d7_dtn", 0),
485	                    ),
486	                ),
487	            )
488	            if self._ngram_route_log_every > 0:
489	                logger.info(
490	                    "[eagle-ngram-route] enabled: k=%d..%d K<=%d "
491	                    "draft_extend_graph_tokens_per_bs=%d",
492	                    self.ngram_route_min_match,
493	                    self.ngram_route_max_match,
494	                    self.ngram_route_max_draft_tokens,
495	                    self.max_draft_extend_tokens_per_bs,
496	                )
497	
498	        with self.draft_tp_context(
499	            self.draft_model_runner.tp_group
500	        ), […]

> AGENT

Perfect! Now I have a complete picture. Let me create a comprehensive analysis document:

---

## 深度分析：CUDA Illegal Memory Access user_4813494d Cause

基于代码精读，我已锁定问题的关键数据流和候选 user_4813494d cause。

### §1 数据流：accept_index 生成与 Sync 点

**accept_index 生成链路：**

1. **初始化** (eagle_info.py:309-311)
   - Shape: `(bs, spec_steps+1)` ← 由 `self.spec_steps` 决定
   - 分配为 `-1` 填充，int32 device tensor

2. **Kernel 计算** (eagle_info.py:359-450)
   - 调用 `verify_tree_greedy_func()` 或 `tree_speculative_sampling_target_only()`
   - 这些是 sgl_kernel 中的 CUDA kernel，**in-place 修改 accept_index 和 predict**
   - Kernel 遍历树结构 (retrive_index / retrive_next_token / retrive_next_sibling) 填充 accept_index[i, j] 的值

3. **CPU Sync 点** (eagle_info.py:514-515)
   ```python
   with torch.profiler.record_function("DC_verify_ai_tolist"):
       accept_index_cpu = accept_index.tolist()  # ← CRASH HERE
   ```
   - `.tolist()` 触发强制 device→host sync
   - **这是 CUDA 端任何未同步异步操作暴露的唯一地点**

### §2 候选 user_4813494d Cause 按可能性排序

#### **(a) Ngram chain mask 越界写入 [高概率]**

**现象：** 在 `_build_ngram_chain_verify_input` (line 1405-1515) 中，tree_mask 分配大小为：
```python
tree_mask = torch.empty(
    (seq_lens_sum * dtn + dtn * dtn * bs,),  # line 1423-1424
    dtype=torch.bool,
    device=device,
)
```

**问题点 1：mask offset 计算 (line 1382-1387)**
```python
def _mask_row_offset(self, seq_lens_cpu: torch.Tensor, row: int, dtn: int) -> int:
    if row == 0:
        prefix = 0
    else:
        prefix = int(seq_lens_cpu[:row].sum().item())
    return prefix * dtn + row * dtn * dtn  # ← 线性加上树部分
```

假设：`seq_lens_sum=200K, dtn=15, bs=32`
- tree_mask 总大小 = `200K*15 + 15*15*32` = `3,007,200` […]