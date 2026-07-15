---
session_id: "50240ede-2a4b-4d4b-b1db-2d885fdca440:subagents"
developer: "dc:dc_001"
split: train
source: dataclaw
repo: Quaxicron/dataclaw-zhiyaowang
start_time: "2026-04-13T03:53:01.531Z"
n_turns: 56
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

I'm investigating an "empty response" problem in a MiniCPM-SALA inference server. I need to understand the current state of evidence and code paths. Please do the following (thoroughness: very thorough): 1. Read the probe artifacts that exist: - Check if these files exist: /user_4813494d/no-spec/summary.json, /user_4813494d/no-spec/server_log.txt - If summary.json exists, read it - If server_log.txt exists, read just the first 100 and last 100 lines 2. Search for the FP4 backend switch code: - In demo-sala/sglang/python/sglang/srt/environ.py - find SGLANG_FLASHINFER_FP4_GEMM_BACKEND - In demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py - find where backend="cudnn" or backend="cutlass" is used 3. Check current FlashInfer version: - Run: python3 -c "import flashinfer; print(flashinfer.__version__)" - Run: python3 -c "import torch; print(torch.backends.cudnn.version())" 4. Search for any empty-response-related debug logging already in the codebase: - Grep for "empty" or "empty_response" or "prediction" in probe-sala/ and demo-sala/sglang/ 5. Look at the persistent bad case - search for sample 85 patterns: - Check if there's any eval dataset file that would have sample index 85 - Look at toolkit/eval_dataset/ for the eval data format 6. Check the predictions artifacts: - ls -la /user_4813494d/predictions.jsonl*.gz /user_4813494d/no-spec/*.gz 2>/dev/null Report everything you find concisely.

> AGENT

I'll systematically investigate this MiniCPM-SALA inference server issue. Let me start by checking the probe artifacts and then move through each investigation point.

> AGENT

Now let me read the summary and log files:

> DEVELOPER

I'm investigating "empty responses" from an NVFP4-quantized MiniCPM-SALA model served through SGLang. The handover doc says empty responses persist even without speculative decoding. Please do the following (thoroughness: very thorough): 1. Read the eval script to understand how responses are collected and what "empty" means: - toolkit/eval_model.py (or similar eval scripts in toolkit/) - Look for how predictions are saved, how empty is detected 2. Read the SGLang detokenizer / output processing path: - Search in demo-sala/sglang/python/sglang/ for detokenizer, output processing, response building - Look for any place where output text could become empty despite having completion_tokens > 0 3. Read the modelopt_quant.py apply() method to understand the FP4 forward pass: - demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py - Focus on the CUTLASS path and any potential numerical issues 4. Search for any NaN/inf handling or detection in the serving path: - Grep for "nan", "inf", "isnan", "isinf" in demo-sala/sglang/ 5. Look at the MiniCPM model forward pass: - demo-sala/sglang/python/sglang/srt/models/minicpm.py - Look for anything that could produce garbled tokens under long-context FP4 6. Check if there's any token validation or filtering that could cause visible output to be empty: - Search for "skip_special_tokens", "spaces_between_special_tokens", or token filtering Report all findings concisely, focusing on any path where valid token IDs could produce empty text output.

> AGENT

Now let me read the last 100 lines of the server log:

> TOOL

[Request interrupted by user]

> TOOL

[Request interrupted by user]

> DEVELOPER

You are reviewing a bug fix in the probe-sala SGLang fork. The bug was: NaN detection code in `logits_processor.py` calls `.tolist()` (GPU→CPU sync) which crashes during CUDA graph capture with "operation not permitted when stream is capturing". The fix applied: added `if torch.cuda.is_current_stream_capturing(): return None` at the top of `_build_probe_nan_customized_info()` in logits_processor.py. Additionally, `cuda_graph_runner.py` replay() was modified to call `_build_probe_nan_customized_info()` AFTER replay (outside the graph), so NaN detection still happens at inference time. Your job: do a THOROUGH review of ALL paths where this could still fail. Specifically: 1. Read `/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/layers/logits_processor.py` — check ALL calls to `_build_probe_nan_customized_info` and `_per_seq_has_nan`. Are there any other D2H sync operations (`.item()`, `.tolist()`, `.cpu()`, `print()` of tensors, etc.) that could also crash during CUDA graph capture? 2. Read `/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/model_executor/cuda_graph_runner.py` — check the replay() method. Does it correctly call `_build_probe_nan_customized_info` AFTER the graph replay completes? Is there any path where customized_info could be lost or the NaN check could run during capture? 3. Search for any OTHER files in `/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/` that reference `customized_info`, `_per_seq_has_nan`, or `_build_probe_nan_customized_info` — are there other callers that might have the same CUDA graph capture problem? 4. Check if `torch.cuda.is_current_stream_capturing()` is the right API for PyTorch 2.9.1. Some older versions used different names. 5. Think about edge cases: - What happens during the CUDA graph capture warm-up run (the run_once before actual capture)? - What happens if capture fails partway — does the NaN code get called during error handling? - In the replay() path in cuda_graph_runner.py, is `self.raw_num_token` correctly set? Could trimmed_hidden be wrong shape? Report ALL findings — safe paths, unsafe paths, and any remaining risks. Be specific with file paths and line numbers.

> AGENT

I'll do a thorough review of all the paths. Let me start by reading the key files.

> AGENT

Now let me read the cuda_graph_runner.py file, focusing on the replay method and capture.

> AGENT

Good. Now let me search for other callers and check capture paths.

> AGENT

Now let me check the capture path to see if `LogitsProcessor.forward()` is called during capture.

> AGENT

Now let me check the `_capture_graph` method to see when the actual capture happens.

> AGENT

Now let me verify the `torch.cuda.is_current_stream_capturing()` API availability.

> AGENT

Good. Let me also check if there are any other `.item()`, `.tolist()`, `.cpu()` calls inside the logits_processor forward path that could crash during capture.

> AGENT

Lines 377 and 384 have `.item()` calls but they're in the `compute_logprobs_for_multi_item_scoring` path which is only called for prefill-only requests, never during CUDA graph capture (decode-only). Now let me check the warm-up run path more carefully. The warm-up runs happen at lines 797-800 (two `run_once()` calls BEFORE graph capture). These are normal forward passes, so `_build_probe_nan_customized_info` will execute normally with `.tolist()`. The actual capture happens inside `_capture_graph` (line 806-808), where the graph context manager wraps `run_once()`. During that call, `is_current_stream_capturing()` will be True, so `_build_probe_nan_customized_info` returns None. That's correct. Let me verify one more thing - the output_buffers stored during capture.

> TOOL

[Request interrupted by user]

> DEVELOPER

## Task Thoroughly review the probe-sala NaN detection code to determine whether the CUDA graph capture crash is fully fixed, and whether any similar issues remain. ## Background The probe-sala package adds NaN detection to SGLang's inference pipeline to diagnose empty responses. The NaN detection calls `torch.isnan(...).any(dim=1).tolist()` which does a GPU→CPU sync (D2H transfer). This crashes during CUDA graph **capture** because `.tolist()` is forbidden when a stream is capturing. The crash was: ``` torch.AcceleratorError: CUDA error: operation not permitted when stream is capturing ``` at `logits_processor.py:71` inside `_per_seq_has_nan()`. ### The fix applied In `_build_probe_nan_customized_info()` in `logits_processor.py`, a guard was added: ```python if torch.cuda.is_current_stream_capturing(): return None ``` Additionally, in `cuda_graph_runner.py`, the `replay()` method was modified to call `_build_probe_nan_customized_info()` AFTER replay (outside capture), so NaN detection still happens during inference. ## What to review 1. **Read these files thoroughly:** - `/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/layers/logits_processor.py` — the NaN detection functions and ALL places `_build_probe_nan_customized_info` is called - `/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/model_executor/cuda_graph_runner.py` — the `replay()` method and `capture_one_batch_size()` method - `/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/managers/scheduler_output_processor_mixin.py` — `maybe_collect_customized_info()` and how customized_info flows - `/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/entrypoints/openai/serving_chat.py` — `_record_empty_response_debug()` 2. **Check for these specific issues:** a. Does the `is_current_stream_capturing()` guard fully prevent D2H sync during capture? Are there any other code paths that could still trigger `.tolist()`, `.item()`, or `.cpu()` during capture? b. In `replay()`, is `_build_probe_nan_customized_info` called AFTER `graph.replay()` completes, so it's outside the captured graph? Or is there a risk it runs during replay of a captured graph? c. During normal (non-CUDA-graph) forward passes, does NaN detection still work correctly? d. Are there any other `.tolist()`, `.item()`, or CPU sync operations in the customized_info pipeline that could crash during CUDA graph capture? Check the full chain: logits_processor → scheduler_output_processor_mixin → tokenizer_manager → serving_chat. e. Is there a risk that `customized_info=None` (returned during capture) propagates downstream and causes a KeyError or AttributeError? f. In `capture_one_batch_size()`, the forward function is called during capture. Does it also call `_build_probe_nan_customized_info` via the model's `forward()`? If so, does the guard protect it? 3. **Report format:** - List each potential issue found (or confirm it's safe) - For each issue, cite the exact file and line number - Rate overall confidence that the fix is complete: HIGH / MEDIUM / LOW - If any issues found, provide the exact code changes needed

> AGENT

I'll read all four files thoroughly to review the NaN detection code and CUDA graph interaction.

> AGENT

Let me search for the relevant functions and read targeted sections.

> AGENT

Now let me check the downstream handling of `customized_info=None` and the `_record_empty_response_debug` function.

> AGENT

Now let me check if `capture_one_batch_size` calls the forward function and whether it goes through `logits_processor.forward()`.

> AGENT

Now I have the full picture. Let me verify one more thing -- inside `_capture_graph`, the `run_once` function is called which invokes `forward()`, which goes through the model and eventually hits `logits_processor.forward()`. During capture, `torch.cuda.is_current_stream_capturing()` returns True, so the guard should trigger. Let me also check if there are any other `.tolist()`, `.item()`, or `.cpu()` calls in the customized_info flow.

> AGENT

I now have a complete picture. Here is my analysis: --- ## 审查结果 ### 1a. `is_current_stream_capturing()` 守卫是否完全阻止了capture期间的D2H同步？ **安全。** `_build_probe_nan_customized_info()` 第79行的守卫在 `_per_seq_has_nan()` 被调用之前就返回了 `None`。这意味着 `.tolist()`（第71行）和 `.item()`（第69行）都不会在capture期间执行。`_per_seq_has_nan` 本身没有独立的调用路径——它只被 `_build_probe_nan_customized_info` 调用。 ### 1b. `replay()` 中的 `_build_probe_nan_customized_info` 是否在 `graph.replay()` 之后调用？ **安全。** 在 `cuda_graph_runner.py` 第951行，`self.graphs[graph_key].replay()` 执行完毕后，第967行才调用 `_build_probe_nan_customized_info()`。`graph.replay()` 是同步提交图到GPU流的操作，之后不再处于capturing状态。`_build_probe_nan_customized_info` 读取的是 output buffer 中的数据（第962-968行的 `trimmed_hidden` 和 `next_token_logits`），这些是graph replay写入的GPU tensor，`.tolist()` 会触发正常的GPU同步读取，不在capture上下文中。 ### 1c. 非CUDA graph正常forward pass是否仍正常工作？ **安全。** `logits_processor.py` 中有两处直接调用 `_build_probe_nan_customized_info`（第630行和第705行），都在 `LogitsProcessor.forward()` 的正常返回路径中。非CUDA graph模式下 `is_current_stream_capturing()` 返回 False，守卫不触发，NaN检测正常执行。 ### 1d. customized_info管道中是否有其他可能在CUDA graph capture期间触发GPU→CPU同步的操作？ **安全。** 完整链路： - `logits_processor.py` → 返回 `LogitsProcessorOutput.customized_info`（已是Python dict/list，无tensor） - `scheduler_output_processor_mixin.py` 第77-83行 → 只做 dict/list 的Python操作，无tensor操作 - `serving_chat.py` 第142-161行 → 只做 `meta_info.get()` 和Python的 `any()` 操作，无tensor操作 在capture期间 `customized_info=None`，`maybe_collect_customized_info`（第77行）的 `is not None` 检查会跳过，不会进入dict遍历。 ### 1e. `customized_info=None` 是否会导致下游 KeyError 或 AttributeError？ **安全。** - `scheduler_output_processor_mixin.py` 第77行：`logits_output.customized_info is not None` 守卫，None时直接跳过。 - `serving_chat.py` 第142-143行：使用 `meta_info.get("probe_hidden_has_nan")` 访问，键不存在时返回 `None`。 - 第158-161行使用 `if hidden_has_nan` / `if logits_has_nan` 守卫，None时返回安全的默认值（`None` 和 `False`）。 ### 1f. `capture_one_batch_size()` 中forward函数是否也调用了 `_build_probe_nan_customized_info`？ **安全。** `capture_one_batch_size()` 第797-800行在capture前先warmup执行 `run_once()` 两次（此时不在capture中），然后第806行通过 `_capture_graph()` 在capture流上再次调用 `run_once()`。在capture流上执行时，`forward()` → 模型forward → `LogitsProcessor.forward()` → `_build_probe_nan_customized_info()`。此时 `torch.cuda.is_current_stream_capturing()` 返回 True，守卫触发，返回 None，不执行任何D2H同步。capture期间 `customized_info=None` 被存入 output buffer 的 `LogitsProcessorOutput` 中，但这个值在 `replay()` 时被丢弃——`replay()` 第967行重新调用 `_build_probe_nan_customized_info` 从实际输出tensor中构建新的customized_info。 --- ## 总结 **整体信心：HIGH（高）** 修复是完整的，没有发现遗留问题： 1. `is_current_stream_capturing()` 守卫正确阻止了capture期间的所有D2H同步操作 2. `replay()` 在graph replay完成后才执行NaN检测，时序正确 3. `customized_info=None` 在整个下游管道中都被安全处理，不会导致异常 4. 没有其他绕过守卫的代码路径 唯一值得注意的非问题点：在 `replay()` 中调用 `_build_probe_nan_customized_info` 会对每次decode步骤引入一个额外的GPU→CPU同步（`.tolist()`），但这是设计预期的诊断功能开销，且在probe-sala（诊断包）而非demo-sala（提交包）中。

> DEVELOPER

I need a thorough audit of the project at /user_4813494d/openbmb. This is a SOAR competition workspace for optimizing MiniCPM-SALA model inference. The project has grown organically and the user says directories, docs, and memory are messy/outdated. Do a comprehensive inventory: 1. **Directory audit**: List every top-level directory and significant subdirectory. For each, determine: - What it contains (brief) - Is it actively used or stale/abandoned? - Are there duplicate files across directories? - Are there large files that shouldn't be in git? 2. **Untracked files audit**: Run `git status` and categorize ALL untracked files as: - Should be committed (active code/config) - Should be gitignored (data, logs, artifacts, weights) - Should be deleted (abandoned experiments, dead code) 3. **Documentation audit**: Read ALL docs in /user_4813494d/openbmb/docs/ and check: - Is the content still accurate? - Is it redundant with CLAUDE.md? - Should it be kept, updated, or deleted? 4. **Cross-directory duplication**: Check for files that exist in both demo-sala/ and probe-sala/ (especially sglang/ subdirectory). Are they in sync or diverged? Which is the source of truth? 5. **Read CLAUDE.md thoroughly** and flag: - Outdated information - Missing information about recent changes (FlashInfer upgrade, empty response fix, probe system) - Contradictions 6. **Read /user_4813494d/.claude/projects/-user_4813494d-openbmb/memory/MEMORY.md** and ALL memory files it references. For each memory: - Is it still accurate? - Is it outdated or superseded by current state? - Does it contain information that's already in CLAUDE.md (redundant)? Report in structured format with specific recommendations. Be thorough — read every file you reference, don't guess.

> AGENT

I'll conduct a comprehensive audit of the project. Let me start by gathering information across multiple dimensions in parallel.

> AGENT

Now let me read all the documentation files, memory files, and explore the directory structure in parallel.

> AGENT

Now let me read all the memory files, explore subdirectories, and check for cross-directory duplication.

> AGENT

Now let me read all the memory files and check for key divergences between demo-sala and probe-sala.

> AGENT

Now let me check for large files, the .gitignore, key size comparisons between demo-sala and probe-sala, and the remaining directories.

> AGENT

Now let me check the git log and some final comparisons.

> AGENT

Let me check a few remaining things to complete the audit.

> AGENT

I now have comprehensive data. Here is the full audit report. --- ## COMPREHENSIVE PROJECT AUDIT: /user_4813494d/openbmb --- ### 1. DIRECTORY AUDIT #### Top-level items | Path | Type | Contents | Status | Notes | |------|------|----------|--------|-------| | `CLAUDE.md` | File | Primary project guidance doc for Claude Code | **Active** | Needs updates (see section 5) | | `AGENTS.md` | File | Repository navigation guide for agents | **Active, untracked** | Comprehensive and accurate; should be committed | | `HANDOVER.md` | File | Empty response investigation handover (Apr 12) | **Partially stale, untracked** | Superseded by `docs/empty-response-investigation-handover-20260413.md` and the resolution in memory. Two competing handover docs exist | | `demo-sala/` | Dir | Official competition submission package | **Active, source of truth** | Core submission path | | `probe-sala/` | Dir | Platform debugging probe package | **Active** | SGLang fork is a copy from demo-sala, but has diverged (see section 4) | | `probe-env-diff/` | Dir | Minimal environment diff probe (4 files) | **Active but niche, untracked** | Small utility, 78 MB .so duplicate | | `probe-so-test/` | Dir | Minimal .so replacement test probe (4 files) | **Active but niche, untracked** | Small utility, 78 MB .so duplicate | | `probe-sala-no-spec-debug.tar.gz` | File | Archived no-spec debug probe (92 MB) | **Stale** | Historical artifact; should be gitignored or deleted | | `eagle/` | Dir | EAGLE-3 data collection, training, eval, model conversion | **Active research** | 475 GB training data, 30 GB weights locally. EAGLE-3 was ultimately a negative result | | `medusa/` | Dir | Medusa speculative decoding training/eval | **Active** | Current production spec decode method | | `eval/` | Dir | Local evaluation scripts | **Active** | Contains 21 MB niah_qa_60.jsonl and other data files that should be gitignored | | `bench/` | Dir | Benchmarking scripts and results | **Active** | 8 untracked result .jsonl files | | `quant/` | Dir | Quantization experiment scripts | **Active** | Contains `calib90/train.json` (10 MB), multiple experiment variants | | `kernels/` | Dir | CUDA kernel experiments and InfLLM-v2 source | **Mostly archived** | `experiments/` is archived per CLAUDE.md | | `toolkit/` | Dir | Official evaluation tools | **Active, read-only** | Should never be modified | | `tests/` | Dir | Regression tests (1 file) | **Active, untracked** | Only `test_medusa_dual_graph.py` | | `outputs/` | Dir | Runtime output artifacts (484 MB, ~40 […]

> DEVELOPER

## Task Carefully review ALL differences between the probe-sala and demo-sala submission packages to determine if the demo-sala package is safe to submit to the platform. The probe-sala package just scored >80% accuracy with zero empty responses on the platform. ## Context - `demo-sala/` is the official submission package - `probe-sala/` is a platform diagnostic probe that just passed with flying colors (>80%, zero empty responses) - The user wants to submit demo-sala and needs to be sure it won't regress ## What to do ### 1. Compare prepare_env.sh Read both files completely: - `/user_4813494d/openbmb/demo-sala/prepare_env.sh` - `/user_4813494d/openbmb/probe-sala/prepare_env.sh` Check: Are FlashInfer/cuDNN upgrades present in both? Are all env vars (MARLIN_DECODE_THRESHOLD, MEDUSA_BS_THRESHOLD, CUBLAS_WORKSPACE_CONFIG, SGLANG_SERVER_ARGS) identical? Any steps in probe that are missing from demo or vice versa? ### 2. Compare prepare_model.sh Read both and check for differences that could affect quantization. ### 3. Compare preprocess_model.py Read both and check: same calibration data? same NUM_CALIBRATION_SAMPLES? same MAX_SEQ_LENGTH? same GPTQ config? ### 4. Compare sglang code differences Run `diff -rq` on the sglang directories, then for EACH differing file, read the actual diff and classify it as: - (A) Probe-only diagnostic code (NaN detection, debug logging) — safe to omit from demo - (B) Demo-only feature code (EAGLE-3 support, etc.) — safe to keep in demo, won't affect Medusa path - (C) **CRITICAL** — a difference that could cause demo to fail, crash, or produce empty responses where probe succeeded ### 5. Compare data files Check that demo-sala has all the data files it needs (calibration data, medusa weights, etc.) ### 6. Check for anything in probe-sala that was critical to its success but is MISSING from demo-sala This is the most important check. The probe scored >80% with zero empty responses. If demo-sala is missing something that probe had, the submission could fail. ## Report format - For each difference found, classify as (A), (B), or (C) - List any (C) critical issues with exact file paths and what needs to change - Give a final GO / NO-GO recommendation for demo-sala submission - If NO-GO, list exactly what needs to be fixed

> AGENT

I'll systematically compare the two submission packages. Let me start by reading the key files in parallel.

> AGENT

Good, I have the core files. Now let me diff the sglang directories and check data files.

> AGENT

Now let me filter out the .pyc files and get only actual source differences in sglang.

> AGENT

Good. Now let me diff each of the 8 differing sglang source files.

> AGENT

Now let me look at the critical chunk_cache.py difference in more detail and the EAGLE worker differences that are relevant to understanding the behavior.

> AGENT

Now let me check the EAGLE worker more carefully -- particularly the `restore_state` and `_alloc_sparse` differences, as these are not probe diagnostics but behavioral changes.

> AGENT

Now let me check if the demo-sala uses EAGLE at all or only Medusa. Let me verify the Medusa worker is identical in both packages.

> AGENT

Good - medusa_worker.py, attention layers, and quantization layers are identical. Now let me also check the key model config and other shared files.

> AGENT

Let me now verify the data files are the same content-wise where they overlap, and check the probe's calibration data file.

> AGENT

Now let me verify the patches/gptq_quantize_fouroversix.py is identical.

> AGENT

Now let me look at the minicpm.py difference more carefully -- specifically the EAGLE-3 aux hidden states.

> AGENT

Now let me check the set_eagle3_layers_to_capture difference.

> AGENT

Let me now check the model_runner.py set_eagle3_layers_to_capture call difference.

> AGENT

Now let me verify the `mambaish_config` vs `hybrid_gdn_config` difference in eagle_worker.py. This is a check in EAGLE's `_prepare_for_verify` and could be structurally important.

> AGENT

Let me check if `mambaish_config` exists on the model runner.

> AGENT

Good - `mambaish_config` is the current unified property in both packages. The probe's eagle_worker.py still uses the old `hybrid_gdn_config`/`mamba2_config` attributes -- that's the older code. The demo's eagle_worker.py has been updated to use the unified `mambaish_config`. This is a demo improvement. Let me now verify the EAGLE path is never activated during Medusa operation.

> AGENT

The EAGLE worker is only instantiated when `--speculative-algorithm EAGLE` is used. Since both demo and probe use `--speculative-algorithm MEDUSA`, the eagle_worker.py differences don't affect the Medusa path. Let me verify this by checking how the spec worker is selected.

> AGENT

Good. Now let me verify the `schedule_batch.py` is the same in both packages, as it's listed in the git status as modified.

> AGENT

Now let me check the cuda_graph_runner.py difference more carefully. This is a key file.

> AGENT

Let me also check whether there's a `tbo_plugin` difference.

> AGENT

Both have the tbo_plugin, just at slightly different line numbers due to code ordering. The full diff showed the only real difference is passing `eagle_aux_hidden_state_layer_ids` vs not passing it to `set_eagle3_layers_to_capture`. Let me verify the full diff one more time.

> AGENT

Now I have a comprehensive picture. Let me compile the full analysis. Here is the complete comparison analysis: --- ## 1. prepare_env.sh 对比 **差异分类: (A) 仅探针诊断代码** 两个文件核心功能步骤完全一致: - SGLang editable install 相同 - nvidia-modelopt==0.42.0 + llmcompressor==[REDACTED] 相同 - cuDNN 升级 `>=9.15.0` 相同 - FlashInfer 升级 `>=0.6.7` 相同，JIT 缓存清理相同 - FourOverSix 补丁相同 - common_ops.abi3.so 替换相同 (md5 一致: `4f9ce8823ad4...`) - SM120 GDC flag 补丁逻辑相同 - prewarm_flashinfer_fp4.py 相同 (md5 一致: `564fb2ce5...`) - **关键环境变量完全一致**: - `SGLANG_SERVER_ARGS` 内容一致 (Medusa K=1, mem-fraction-static 0.80, max-running-requests 64 等) - `SGLANG_MARLIN_DECODE_THRESHOLD=48` 一致 - `SGLANG_MEDUSA_BS_THRESHOLD=16` 一致 - `CUBLAS_WORKSPACE_CONFIG=":4096:8"` 一致 probe 额外包含: - 邮件报告 (`probe_email.py`) - FlashInfer 状态诊断 (`probe_flashinfer_state.py`) - 这些仅为诊断工具，不影响推理行为 ## 2. prepare_model.sh 对比 **差异分类: (A) 仅探针诊断代码** demo: 直接调用 `preprocess_model.py "$@"` probe: 调用 `preprocess_model.py --input "$INPUT" --output "$OUTPUT"`，加 tee 日志、状态采集、邮件报告、运行 `probe_eval.py`，最后 `exit 1` (探针不计分) 核心量化调用一致。 ## 3. preprocess_model.py 对比 **差异分类: 重要但无影响 -- 量化参数不同，但 demo 使用的是经过验证的更优配置** | 参数 | demo-sala | probe-sala | |------|-----------|------------| | MAX_SEQ_LENGTH | 49152 (48K) | 92160 (90K) | | NUM_CALIBRATION_SAMPLES | 128 | 90 | | 校准数据 | calib_wikitext_loguniform_128.jsonl | calib90_train.jsonl | **这不是问题。** demo 使用的是 CLAUDE.md 中记录的"chosen"配置 (loguniform128/48K/FourOverSix, 79.98%)。probe 使用的是 calib90/90K 配置。两种配置都能通过精度门槛 (77.6%)。demo 的配置是经过本地验证更稳定的选择。 两者的 phase2_convert (tensor format conversion, lm_head restoration, config patching) 完全相同。 ## 4. sglang 代码差异 (8 个文件) ### 4a. serving_chat.py **分类: (A) 仅探针诊断代码** probe 额外有 `_record_empty_response_debug()` 方法，当检测到空响应时写入调试 JSON。demo 无此代码。不影响功能。 ### 4b. logits_processor.py **分类: (A) 仅探针诊断代码** probe 额外有 `_per_seq_has_nan()` 和 `_build_probe_nan_customized_info()` 函数，在 sampling 时收集 NaN 检测信息。demo 无此代码。不影响 sampling 逻辑本身。 ### 4c. scheduler_metrics_mixin.py **分类: (B) demo 改进代码** demo 修正了 acceptance rate 计算: 减去了 confirmed tokens 的基数 (`pure_draft_accepted = self.spec_num_accepted_tokens - self.spec_num_forward_ct`)。这只影响 metrics 日志显示，不影响推理行为。 ### 4d. chunk_cache.py **分类: (B) demo 新增的 EAGLE 相关防御代码** demo 在 `cache_finished_req` 中跳过 all-zero 的 sparse indices 释放 (`k1_indices = k1_indices[k1_indices > 0]`)。这是 EAGLE speculative decoding 的防御性代码，在 Medusa 路径下不会触发问题（Medusa 正常分配 sparse slots）。安全保留。 ### 4e. cuda_graph_runner.py **分类: (A)+(B)** - probe: import `_build_probe_nan_customized_info` 并在 CUDA graph replay 时收集 NaN 信息 -- (A) 诊断代码 - demo: `set_eagle3_layers_to_capture(self.model_runner.eagle_aux_hidden_state_layer_ids)` 传递 layer IDs -- (B) EAGLE-3 改进 EAGLE-3 代码路径仅在 `spec_algorithm.is_eagle3()` 时激活，Medusa 模式下不会执行。 ### 4f. model_runner.py **分类: (B) demo 改进代码** demo: `set_eagle3_layers_to_capture(self.eagle_aux_hidden_state_layer_ids)` 传递 layer IDs probe: `set_eagle3_layers_to_capture()` 不传 同上，仅 EAGLE-3 路径，Medusa 模式不执行。 ### 4g. minicpm.py **分类: (B) demo 改进代码** demo: `aux_hidden_states.append(hidden_states)` (不加 residual) probe: `aux_hidden_states.append(hidden_states + residual ...)` 这是 EAGLE-3 训练数据对齐的修复。`layers_to_capture` 默认为空集 `set()`，只有 EAGLE-3 调用 `set_eagle3_layers_to_capture()` 才会激活。Medusa 不会触发此代码路径。 ### 4h. eagle_worker.py **分类: (B) demo 多处 EAGLE-3 改进** 主要差异: 1. draft model 量化/attention backend 配置修复 (demo 新增) 2. `restore_state` 删除 + 注释 (demo: 不调用，避免 double-free) 3. draft KV cache 主动释放 (demo 新增 `batch.tree_cache.token_to_kv_pool_allocator.free`) 4. `mambaish_config` 统一属性 (demo) vs `hybrid_gdn_config`/`mamba2_config` 分别检查 […]
