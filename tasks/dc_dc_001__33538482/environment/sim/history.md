> DEVELOPER

我需要彻底搞清楚一个偶发的 CUDA illegal memory access crash,签名如下: ``` File "/tmp/submission_extract_1/probe-sala-full/sglang/python/sglang/srt/speculative/eagle_worker.py", line 788, in forward_batch_generation self.verify(batch, spec_info) File ".../sglang/srt/speculative/eagle_worker.py", line 1846, in verify res: EagleVerifyOutput = spec_info.verify( File ".../sglang/srt/speculative/eagle_info.py", line 515, in verify accept_index_cpu = accept_index.tolist() torch.AcceleratorError: CUDA error: an illegal memory access was encountered ``` **背景上下文(必读才能给出有价值的分析):** - 本地代码位置: `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/` - 提交端代码位置: `/tmp/submission_extract_1/probe-sala-full/sglang/python/sglang/srt/speculative/` - 这两份应当是对齐的(用户说"理论上和本地时对齐的") - 项目背景: MiniCPM-SALA + EAGLE3 speculative + 自定义动态 spec mode (D5/D7/NO_SPEC) + per-request ngram routing (chain verify 与 EAGLE draft 混合到一个 EagleVerifyInput) - 关键: `eagle_worker.py` 里 `_max_topk = max(d5_topk, d7_topk)`, `_max_spec_steps = max(d5_steps, d7_steps)`,cuda graph 按最大值 capture - `_draft_ngram_route` (大约 line 1517) 实现 hit/miss 分支: hit→chain mask (`_build_ngram_chain_verify_input`), miss→EAGLE draft,两路合并成一个 `EagleVerifyInput` 交给 verify - Hard coupling: `max_draft_tokens = min(NGRAM_MAX_DRAFT_TOKENS, dtn - 1)` (chain 长度被 D5/D7 的 dtn 卡) - 我们已知 ngram_min_match=2 在长 context 上稳定崩,签名一模一样 - 现在 default config (MIN_MATCH=3) 在 probe-sala-full 上 ~50% 概率崩 **触发场景(从最近一次 crash log 提取):** 1. 单请求长 context (前面 Decode batch #running-req=1 多次,accept len 14~15,几乎到 dtn=15 上限,即 D7+ngram chain hit 满 chain) 2. 之后 Smax workload 涌入(96 个新 prefill batches 连续 prefill,8192 chunked-prefill) 3. 期间 schedule 切换 D7 → D5 → 可能 NO_SPEC 4. verify() 在 `accept_index.tolist()` 处 CUDA illegal memory access **任务:** 仔细深入阅读以下文件,不要只看 grep 摘要,要看实际代码逻辑: 1. `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py` 的 `EagleVerifyInput.verify` 方法(line 515 周围 ±100行) […]

> AGENT

I'll conduct a systematic deep-dive analysis of this CUDA illegal memory access crash. Let me start by reading the critical files to understand the data flow.

> AGENT

Now let me read the critical sections around accept_index computation and the ngram chain verify building:

> AGENT

Now let me read the `_lookup_req_ngram_draft` and `_mask_row_offset` methods:

> AGENT

Let me search for the accept_index computation in the tree_speculative_sampling kernel call:

> AGENT

Now let me check how the dynamic spec mode (D5/D7/NO_SPEC) impacts shape consistency:

> AGENT

Let me search for the critical invariant about tree_mask size calculation and how it could overflow:

> AGENT

Perfect! Now I've found a critical insight. Let me trace through the logic and verify my hypothesis by checking the initialization of EAGLE worker parameters:

> AGENT

Let me search for the EAGLEWorker __init__ method:

> AGENT

Now let me find where _max_topk and _max_spec_steps are set:

> AGENT

Now let me find where _max_topk and _max_spec_steps are initialized:

> AGENT

Perfect! Now I have a complete picture. Let me create a comprehensive analysis document: --- ## 深度分析：CUDA Illegal Memory Access user_4813494d Cause 基于代码精读，我已锁定问题的关键数据流和候选 user_4813494d cause。 ### §1 数据流：accept_index 生成与 Sync 点 **accept_index 生成链路：** 1. **初始化** (eagle_info.py:309-311) - Shape: `(bs, spec_steps+1)` ← 由 `self.spec_steps` 决定 - 分配为 `-1` 填充，int32 device tensor 2. **Kernel 计算** (eagle_info.py:359-450) - 调用 `verify_tree_greedy_func()` 或 `tree_speculative_sampling_target_only()` - 这些是 sgl_kernel 中的 CUDA kernel，**in-place 修改 accept_index 和 predict** - Kernel 遍历树结构 (retrive_index / retrive_next_token / retrive_next_sibling) 填充 accept_index[i, j] 的值 3. **CPU Sync 点** (eagle_info.py:514-515) ```python with torch.profiler.record_function("DC_verify_ai_tolist"): accept_index_cpu = accept_index.tolist() # ← CRASH HERE ``` - `.tolist()` 触发强制 device→host sync - **这是 CUDA 端任何未同步异步操作暴露的唯一地点** ### §2 候选 user_4813494d Cause 按可能性排序 #### **(a) Ngram chain mask 越界写入 [高概率]** **现象：** 在 `_build_ngram_chain_verify_input` (line 1405-1515) 中，tree_mask 分配大小为： ```python tree_mask = torch.empty( (seq_lens_sum * dtn + dtn * dtn * bs,), # line 1423-1424 dtype=torch.bool, device=device, ) ``` **问题点 1：mask offset 计算 (line 1382-1387)** ```python def _mask_row_offset(self, seq_lens_cpu: torch.Tensor, row: int, dtn: int) -> int: if row == 0: prefix = 0 else: prefix = int(seq_lens_cpu[:row].sum().item()) return prefix * dtn + row * dtn * dtn # ← 线性加上树部分 ``` 假设：`seq_lens_sum=200K, dtn=15, bs=32` - tree_mask 总大小 = `200K*15 + 15*15*32` = `3,007,200` […]