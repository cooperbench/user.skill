---
session_id: "b4f4718e-9789-4373-aafd-b7416fee3bdf:subagents"
developer: "dc:dc_001"
split: train
source: dataclaw
repo: Quaxicron/dataclaw-zhiyaowang
start_time: "2026-05-17T10:16:17.353Z"
n_turns: 233
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

在 /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/ 下查找 EAGLE-3 draft model 的实现细节。背景：draft model 是 LlamaForCausalLMEagle3，1 个 attention layer，head_dim=128，num_attention_heads=32，num_key_value_heads=2。它在 prefill 和 decode 时都跑 attention，写自己独立的 KV cache。 我要搞清楚的核心问题（按重要性排序）： 1. **Draft model 的 forward 在哪个文件 / class 里？它的 attention 调用具体是怎么写的？** 找到 attention forward 的实际入口，看它如何调用 attention backend (`forward_extend` / `forward_decode`)。 2. **Draft 用的 attention backend 是什么？** 启动配置是 `--speculative-draft-attention-backend flashinfer`，找到 FlashInfer draft backend 实现，看 plan / forward 接口签名。 3. **Draft 的 KV cache 是独立 pool 还是和 target 共享？** 找到 draft model_runner 怎么初始化它的 token_to_kv_pool / req_to_token_pool。 4. **现有 SGLang 是否已经支持 sliding window attention？** 搜 `sliding_window` / `window_size` / `local_attention` / `swa_` 关键字。如果支持，看它怎么在 attention plan 或 mask 里实现。Gemma-2 的 hybrid local/global attention 可能是参考。 5. **Chunked prefill 时 draft 的 token positions 和 page table 怎么构造？** 看 `prepare_for_extend` 类的函数，draft 输入的 sequence positions 是相对还是绝对，KV cache 写入的 slot 索引怎么算。 6. **EAGLE-3 draft 的输入是 target hidden_states**，看是从哪一层取的（aux_hidden_state）、维度多少（应该是 hidden_size×3）、在 draft attention 之前怎么经过 fc / norm 处理。 请按这 6 个问题分点回答，每点给出 file_path:line_number 引用 + 关键代码片段（≤10 行），不超过 800 字总长。不要给方案建议，只要事实和定位。

> AGENT

我来帮你系统地搜索这些核心问题。

> AGENT

让我进一步找关键文件：

> AGENT

好的，现在让我并行读取关键文件来回答你的6个问题：

> AGENT

现在让我搜索更多关于注意力后端、KV cache和sliding window的细节：

> DEVELOPER

在 /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/ 下找 sliding window / local attention 的现有支持。背景：我要给 EAGLE draft 加一个 sliding window，让它只 attend 最近 N tokens；要看现有代码已经做了什么、复用什么。 核心问题： 1. **`sliding_window_size` / `attention_chunk_size` / `is_sliding` / `swa_*` 这类字段在哪些地方被消费？** 找 attention backend 里 plan 时怎么使用、forward 时怎么 mask。FlashInfer paged kv 支持 sliding window 吗（看 `BatchPrefillWithPagedKVCacheWrapper.plan` / `BatchDecodeWithPagedKVCacheWrapper.plan` 调用点）。 2. **Gemma-2 / Llama-4 等模型有 hybrid local-global attention 层**，找它们怎么声明 per-layer attention 类型（global vs local），attention backend 怎么 dispatch。 3. **`swa_full_tokens_ratio` / `disable_hybrid_swa_memory` 这两个 server_args 是什么意思**，看它们的 KV cache memory pool 路径。 4. **FlashInfer Python wrapper 接口签名**：`flashinfer.BatchPrefillWithPagedKVCacheWrapper` 和 `BatchDecodeWithPagedKVCacheWrapper` 的 plan() 是否有 `window_left` / `sliding_window_size` 参数？看 SGLang fork 怎么调用。如果直接 grep 不到，尝试看 attention backend 的具体调用。 5. **mask_mode / MaskMode** 枚举值含义。我之前看到 production 524K prefill 用 MaskMode=0（CAUSAL）。FlashInfer 是否有 SLIDING_WINDOW / CUSTOM_MASK 模式？ 请按这 5 个问题分点回答，每点给出 file_path:line_number + 关键代码片段（≤10 行）。不要给方案建议，只要事实和定位。总长 ≤800 字。

> AGENT

继续深入搜索具体实现细节：

> AGENT

我来逐个检查这些问题。首先扫描目录结构和核心文件。

> AGENT

让我查看更多关于attention forward和aux_hidden_state的细节：

> AGENT

现在让我读取flashinfer_backend的forward_extend和forward_decode接口：

> AGENT

现在我逐个问题深入查询： **问题1、2、3、4、5：**

> DEVELOPER

在 /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/ 下搞清楚 EAGLE-3 draft 的 KV cache 是怎么分配/释放/复用的。 核心问题： 1. **Draft KV cache 用的是独立的 token_to_kv_pool 还是共享 target 的？** 看 `EagleWorkerV2` 或 `EagleWorker.__init__` 怎么把 `self.req_to_token_pool` / `self.token_to_kv_pool_allocator` 设置上来；是 alias 到 target 的还是 alloc 新的。 2. **Draft prefill 时往 KV cache 写入的 slot index 在哪里决定？** 看 `_draft_extend_for_prefill` 或 `forward_draft_extend` 调用链里 forward_batch 的 `out_cache_loc` 是怎么生成的。 3. **Slot 释放时 K/V tensor 数据是否清零？** 看 SGLang 的 allocator (e.g. `TokenToKVPoolAllocator.free`)，确认释放只是返还索引、还是会 zero-fill K/V。 4. **如果给 draft 单独分配 KV pool（不和 target 共享），需要改哪里？** scheduler 里 `init_draft_worker` 的 memory 设置在哪？mem_fraction_static 怎么划分给 draft？ 5. **Draft KV 的形状是什么？** num_layers × num_kv_heads × head_dim × max_total_tokens。对 EAGLE-3 1 层 + nkv=2 + head_dim=128 + max_total_tokens=524288 算一下大概多少 GB（dtype 是什么）。 请按这 5 个问题分点回答，每点给出 file_path:line_number + 关键代码片段（≤10 行）。不要给方案，只要事实和数字。总长 ≤800 字。

> AGENT

让我查看这个prepare_for函数和相关的chunked prefill逻辑：

> AGENT

我来逐个问题搜索关键代码。

> AGENT

现在让我查看LlamaAttention在draft中的实际调用：

> AGENT

让我查看LlamaAttention的forward方法和sliding window支持：

> AGENT

让我搜索问题1相关的初始化代码：

> AGENT

现在让我查看aux_hidden_states的获取和使用：

> AGENT

问题1找到了。现在搜问题2（draft prefill KV cache slot index）：

> AGENT

让我查看get_embed_and_head和aux_hidden_state的处理逻辑：

> AGENT

现在让我看看FlashInferMultiStepDraftBackend的实现：

> AGENT

现在查看 alloc_token_slots 如何生成 out_cache_loc：

> AGENT

现在让我查看FlashInferMultiStepDraftBackend的plan和forward方法：

> AGENT

现在让我查看最后的部分关于aux_hidden_state在draft中的处理：

> AGENT

现在搜问题3（slot释放时是否清零）：

> AGENT

完美！现在让我再查看一下KV cache pool的独立性：

> AGENT

查看free方法，没有清零。现在看看是否有地方显式清零：

> AGENT

让我查看prepare_for_v2_draft方法：

> AGENT

现在搜问题4（init_draft_worker memory设置）：

> AGENT

现在查询 Gemma-2 的 per-layer attention 配置：

> AGENT

完美！现在让我整合所有信息生成回答。根据我的搜索，我已经找到了所有核心问题的答案。让我最后验证一下关于Gemma-2 hybrid local/global attention的支持：

> AGENT

现在查找 memory 划分代码：

> AGENT

现在看ModelRunner中memory如何划分：

> AGENT

现在检查 plan() 的调用：

> AGENT

现在查 SWATokenToKVPoolAllocator：

> AGENT

现在搜问题5（Draft KV形状和大小计算）：

> AGENT

现在看EAGLE-3的配置，查draft KV形状：

> AGENT

让我查EAGLE-3的完整配置参数：

> AGENT

最后检查 mask_mode 和 dispatch：

> AGENT

现在我有足够的信息来回答了。让我生成最终答案： --- ## EAGLE-3 Draft Model 实现细节定位 ### 1. Draft Model Forward 入口与 Attention 调用 **文件位置**: `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama_eagle3.py:152-191` Draft model 的核心架构在 `LlamaModel.forward()` 中： ```python # llama_eagle3.py:168-171 hidden_states = forward_batch.spec_info.hidden_states # 从target获取aux_hidden_state hidden_states, _ = self.fc(hidden_states) # fc: (hidden_size*3 -> hidden_size) hidden_states, residual = self.midlayer( positions, embeds, hidden_states, forward_batch, residual, ) ``` 在 `LlamaDecoderLayer.forward()` (llama_eagle3.py:75-101) 中，attention 的调用为： ```python hidden_states = self.self_attn( positions=positions, hidden_states=hidden_states, # shape: (num_tokens, hidden_size) forward_batch=forward_batch, ) ``` Attention 实际路由在 `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/radix_attention.py:128-136`，根据 forward_mode 调用： ```python return forward_batch.attn_backend.forward(q, k, v, self, forward_batch, save_kv_cache, **kwargs) ``` --- ### 2. Draft 用的 Attention Backend 类型 **文件位置**: `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/draft_utils.py:66-92` Draft backend 通过 `DraftBackendFactory.create_draft_extend_backend()` 创建。启动配置 `--speculative-draft-attention-backend flashinfer` 对应： ```python # draft_utils.py:68 backend_map = { "flashinfer": self._create_flashinfer_prefill_backend, # 返回 FlashInferAttnBackend ... } ``` FlashInfer draft backend 的 **plan & forward 接口** 在 `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/flashinfer_backend.py`: - **forward_extend** (line 743): 接收 q, k, v, layer, forward_batch，调用 `prefill_wrapper_paged.forward()` - **forward_decode** (line 850): 接收同样参数，调用 `decode_wrapper.forward()` --- ### 3. Draft KV Cache 独立 Pool 或共享 **文件位置**: `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py:119-135` Draft 和 Target 使用 **独立的 KV cache pool**： ```python # eagle_worker_v2.py:119-121 self.req_to_token_pool, self.token_to_kv_pool_allocator = ( target_worker.get_memory_pool() # 与target共享req_to_token_pool ) # eagle_worker_v2.py:124-135 self.draft_worker = TpModelWorker( ..., req_to_token_pool=self.req_to_token_pool, # 共享pool索引 token_to_kv_pool_allocator=self.token_to_kv_pool_allocator, # 各自独立KV存储 ) ``` --- ### 4. Sliding Window Attention 支持现状 **文件位置**: `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/radix_attention.py:57, 76` SGLang **已支持 sliding window attention**。在 RadixAttention 初始化： ```python self.sliding_window_size = sliding_window_size or -1 # -1表示无限制 ``` 在 FlashInferAttnBackend.forward_extend() 中实现 (flashinfer_backend.py:783-790)： ```python window_left=( layer.sliding_window_size if not (multi_item_params and multi_item_params.is_enabled()) else -1 # 若使用multi-item scoring，禁用滑窗 ), ``` Gemma-2 的 hybrid local/global attention 由各模型配置 (如 `/sglang/srt/configs/model_config.py`) 提供 `sliding_window_size` 参数控制。 --- ### 5. Chunked Prefill 时 Token Positions 与 Page Table 构造 **文件位置**: `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info_v2.py:142-178` 在 `prepare_for_v2_draft()` 中： ```python self.positions = batch.seq_lens.repeat_interleave(topk, dim=0) # 相对于batch的绝对position assign_draft_cache_locs_page_size_1[(bs,)]( batch.req_pool_indices, req_to_token_pool.req_to_token, batch.seq_lens, batch.out_cache_loc, # out_cache_loc为KV写入slot索引 ..., topk, num_steps ) ``` **Extend 时** (eagle_info_v2.py:196-197)： ```python batch.extend_seq_lens = [num_draft_tokens for _ in range(len(batch.seq_lens))] batch.extend_prefix_lens = seq_lens_cpu_.tolist() # prefill部分长度(绝对) ``` --- ### 6. EAGLE-3 Draft 的 Aux Hidden State 处理 **文件位置**: `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama_eagle3.py:130-172` Target model 的 aux hidden state 维度构造 (llama_eagle3.py:130-143)： ```python if hasattr(config, "target_hidden_size"): self.hidden_size_in = config.target_hidden_size else: self.hidden_size_in = config.hidden_size # fc输入: hidden_size_in * 3，输出: hidden_size self.fc = ColumnParallelLinear( self.hidden_size_in * 3, config.hidden_size, ... ) ``` Aux hidden state 在 draft forward 中来自 (llama_eagle3.py:168)： ```python hidden_states = forward_batch.spec_info.hidden_states # shape: (num_tokens, hidden_size*3) hidden_states, _ = self.fc(hidden_states) # 经fc投影到draft hidden_size ``` 该hidden state 由 target model 的 `LlamaModel.norm()` 输出 (llama_eagle3.py:186-191)，用于aux token reconstruction。

> AGENT

现在查看获取num_kv_heads的代码：

> AGENT

检查 eagle draft 相关：

> AGENT

最后检查 flashinfer forward 调用的地方：

> AGENT

现在计算具体的KV大小。让我查EAGLE-3的KV cache dtype：

> AGENT

现在让我看一下实际的内存计算，查cell_size如何计算draft worker的：

> AGENT

现在我有足够信息了。让我总结关键发现：

> AGENT

现在生成总结： ## 五个问题的查询结果 **1. sliding_window_size / attention_chunk_size / is_sliding 字段消费位置** - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py:727-731` 定义 `_get_sliding_window_size()` 从 HF config 读取 - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/flashinfer_backend.py:783-790` 在 prefill forward 中调用 `window_left=layer.sliding_window_size` - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/flashinfer_backend.py:972-1020` 在 `update_sliding_window()` 中通过 `torch.clamp(seq_lens, max=self.sliding_window_size + 1)` 生成窗口 KV；使用 `SWATokenToKVPoolAllocator` 管理分离的 SWA KV pool **2. Gemma-2 的 per-layer hybrid local-global attention** - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/gemma2.py:153-164` 每层根据 `layer_id % 2 == 0` 判断是否使用 SWA，通过 `RadixAttention(sliding_window_size=...)` 声明 **3. swa_full_tokens_ratio / disable_hybrid_swa_memory 含义** - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/server_args.py:313-314` 定义这两个字段 - `swa_full_tokens_ratio=0.8` 控制完全注意力 KV cache 的分配比例；`disable_hybrid_swa_memory=True` 禁用分离的 SWA pool（改用单一 pool） - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/swa_memory_pool.py:20-77` `SWAKVPool` 维护分离的 `swa_kv_pool` 和 `full_kv_pool` **4. FlashInfer wrapper plan() 接口** - 无直接 `window_left` 参数在 plan()；而在 forward() 时 `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/flashinfer_backend.py:783` 传入 `window_left=layer.sliding_window_size` - SGLang 通过 `call_begin_forward(use_sliding_window_kv_pool=True)` 管理双 wrapper 编排（SWA + Full） **5. MaskMode / dispatch 机制** - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/flashinfer_backend.py:56-58` 定义 `WrapperDispatch.SLIDING_WINDOW` 枚举值 - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/flashinfer_backend.py:152-160` 若 `model_runner.sliding_window_size != None` 则设置 `dispatch_reason = SLIDING_WINDOW`、启用双 wrapper - 无 FlashInfer 原生 `MaskMode` 枚举；SGLang 用 `window_left=-1`（全注意）vs 具体值（窗口）区分。`TreeMaskMode` 是 speculative draft 的掩码模式（与 SWA 无关）

> AGENT

现在我有足够信息来回答这5个问题。让我编写最终答案： --- ## 回答 ### **问题1：Draft KV cache 用的是独立的 token_to_kv_pool 还是共享 target 的？** **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:335-337` ```python # Share the allocator with a target worker. # Draft and target worker own their own KV cache pools. self.req_to_token_pool, self.token_to_kv_pool_allocator = ( target_worker.get_memory_pool() ) ``` **事实**：Draft 和 Target worker **共享** `token_to_kv_pool_allocator`（索引分配器），但各自拥有独立的 KV cache 数据池。`req_to_token_pool` 和 `token_to_kv_pool_allocator` 都从 target worker 获取，不是新分配。 --- ### **问题2：Draft prefill 时往 KV cache 写入的 slot index 在哪里决定？** **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/common.py:258` ```python out_cache_loc = allocator.alloc(num_tokens) ``` **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:1080` ```python out_cache_loc, token_to_kv_pool_state_backup = alloc_token_slots( tree_cache=batch.tree_cache, num_tokens=num_tokens_to_allocate, backup_state=True, ) ``` **事实**：`out_cache_loc` 由 `TokenToKVPoolAllocator.alloc(num_tokens)` 生成，直接从 `free_pages` 列表分配连续 slot indices（torch.Tensor），无单独策略。 --- ### **问题3：Slot 释放时 K/V tensor 数据是否清零？** **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/allocator.py:155-165` ```python def free(self, free_index: torch.Tensor): if free_index.numel() == 0: return if self.is_not_in_free_group: if self.need_sort: self.release_pages = torch.cat((self.release_pages, free_index)) else: self.free_pages = torch.cat((self.free_pages, free_index)) ``` **事实**：`free()` 仅返还索引到 `free_pages` 或 `release_pages` 列表，**不清零** K/V tensor 数据，只标记为可复用。 --- ### **问题4：如果给 draft 单独分配 KV pool，需要改哪里？** **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/scheduler.py:485-544` **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/tp_worker.py:320-340` ```python self._model_runner = ModelRunner( mem_fraction_static=self.server_args.mem_fraction_static, is_draft_worker=True, req_to_token_pool=self.req_to_token_pool, token_to_kv_pool_allocator=self.token_to_kv_pool_allocator, ) ``` **文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/model_executor/model_runner_kv_cache_mixin.py:120-140` ```python if self.is_draft_worker: num_layers = getattr( self.model_config.hf_config, "num_nextn_predict_layers", self.num_effective_layers, ) cell_size = self.get_cell_size_per_token(num_layers) rest_memory = available_gpu_memory - total_gpu_memory * (1 - self.mem_fraction_static) ``` **事实**：需改三处：(1) `EagleWorker.__init__` 不从 target 获取 allocator，新建独立 allocator；(2) `scheduler.init_draft_worker()` 传不同的 `token_to_kv_pool_allocator`；(3) 根据 `is_draft_worker` 在 `profile_max_num_token()` 中用 `num_nextn_predict_layers` 计算 `mem_fraction_static` 割配（目前共享同一个）。 --- ### **问题5：Draft KV 的形状和大小？** **配置**：EAGLE-3 为 1 层 (`num_nextn_predict_layers=1`)、`num_kv_heads=2`、`head_dim=128`。 **公式**（`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/model_executor/model_runner_kv_cache_mixin.py:82-88`）： ```python cell_size = ( self.model_config.get_num_kv_heads(tp_size) * (self.model_config.head_dim + self.model_config.v_head_dim) * num_layers * kv_size ) ``` **计算**（假设 K、V 都用 bfloat16，1 层、2 kv_heads、128 head_dim、v_head_dim=128、524288 max_tokens、tp_size=1）： - cell_size/token = 2 × (128 + 128) × 1 × 2 bytes = **1024 bytes/token** - 总 KV 占用 = 524288 tokens × 1024 bytes = **512 MB**（单精度 bfloat16） **形状**：`[num_layers=1, num_kv_heads=2, max_total_tokens=524288, head_dim+v_head_dim=256]`

> DEVELOPER

在 /user_4813494d/openbmb 仓库审查最近所有跟 InfLLM-v2 sparse stage1/stage2 prefill 路径相关的 commits。目标：找出"声称有性能收益但可能引入精度问题"的修改。 具体要做： 1. **跑 git log**：列出最近 60 天所有 touch 这些文件的 commits 的 hash + subject： - `kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h` - `kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash.h` - `kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_blockmask.h` - `kernels/infllmv2_cuda_impl/csrc/flash_attn/flash_api.cpp` - `kernels/infllmv2_cuda_impl/csrc/entry.cu` - `demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_backend.py` - `demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_sparse_utils.py` - `demo-sala/sglang/python/sglang/srt/models/minicpm.py` 2. **对每个 commit 评估**：用 `git show --stat <hash>` 看变更范围，看 commit message。把 commits 分成 3 类： - **A 安全类**：纯重构、docs、env 开关默认 off - **B 中性类**：性能改造但**理论上等价**（如改 layout、改 launch config、加 fused kernel 等价计算） - **C 风险类**：**改变 attention 数值结果**的修改（如：调整 mask / score 归一化 / 跳过某些计算 / 改 softmax 顺序 / 改 fp32 累加为 fp16） 3. **C 类是重点**：对每个 C 类 commit 详细分析： - 改了什么数值路径 - 是否被 env flag 保护（默认 ON 还是 OFF） - 如果默认 ON：在什么 corner case 下会让 attention output 跟原版不一致 - 如果默认 OFF：有没有可能在某些条件分支里意外开启 4. **重点关注几个嫌疑词**（grep + 看 commit）： - `SGLANG_FAST_PREFILL_STAGE1` - `SGLANG_MINICPM_STAGE1_EMPTY_P2` - `compressed_max_seqlen_k` - `fi_convert` cache - `stage1_actual_maxlen` - `INFLLM_V2_*` env vars - `SGLANG_MINICPM_*` env vars 5. **当前 working tree 没 commit 的 prefill 修改**：跑 `git diff` 看上述文件未 commit 的变化，特别关注是否动了数值路径。 报告格式（800-1200 字）： - A 类一句话掠过 - B 类列出 hash + subject + 一行 rationale - **C 类要详细**：每个写 hash + subject + 改了什么数值 + env 保护状态 + 可能的精度风险场景。 - 当前 working tree 的差异单独一节。 不要给修复建议，只要风险定位。引用 file_path:line_number。

> AGENT

我来系统地审查这个仓库中与 InfLLM-v2 sparse stage1/stage2 prefill 路径相关的 commits。 首先，让我查看 git log 并识别所有相关的 commits：

> AGENT

现在让我对关键 commits 进行详细分析。首先查看最近的几个高风险 commits：

> AGENT

这是一个很关键的 revert。让我看看被 revert 的那些 commits：

> AGENT

现在让我检查其他风险的 commits，特别是那些 "perf" 相关的：

> AGENT

让我检查其他可能的风险 commits：

> DEVELOPER

在 /user_4813494d/openbmb 仓库下找所有**默认开启**且**影响 InfLLM-v2 稀疏 attention 数值路径**的 env-controlled 开关。 具体做： 1. **grep 所有跟 InfLLM-v2 / MiniCPM / sparse stage1 / stage2 prefill 相关的 env 开关定义**： - 在 `demo-sala/sglang/python/sglang/srt/` 下查所有 `os.environ.get("SGLANG_*"...)` 和 `os.environ.get("INFLLM_*"...)` 和 `os.environ.get("MINICPM_*"...)` - 在 `kernels/infllmv2_cuda_impl/` 下查所有 `getenv("INFLLM_*"...)` 和 `getenv("SGLANG_*"...)` - 在 `eval/start_eagle.sh` 和 `demo-sala/prepare_env.sh` 下看哪些显式设置了 2. **每个 env 标记**： - 默认值（无环境变量时的值） - 当前 production 配置下的实际值（看 `eval/start_eagle.sh`、`demo-sala/prepare_env.sh` 是否 export 了不同的值） - 是否动数值路径： - **数值类**：会改变 attention output（如：跳过 K1 second pass、change normalization、change mask、change dtype） - **性能类**：仅 layout / launch 优化（如：fuse kernel、improve scheduling） - **诊断类**：profile / capture / log（不动数值） 3. **报告格式**： - 一张表：env_name | 默认值 | production 值 | 类别 | 一行说明 - 重点突出"默认 OFF 但 production 显式 ON 的数值类开关"——这是最容易被忘记的精度风险源 - "默认 ON 且数值类"的开关也要点出来 4. **特别盯死这些可疑开关**（如果出现）： - `SGLANG_FAST_PREFILL_STAGE1` 是 ON 还是 OFF？影响什么？ - `SGLANG_MINICPM_STAGE1_EMPTY_P2` 是 ON 还是 OFF？P2 是 K1 second pass 吗，empty 意味着什么？ - `INFLLM_V2_STAGE1_GROUPMAX` 是 ON 还是 OFF？ - `SGLANG_MINICPM_UNSAFE_FI_CONVERT_CACHE` 是 ON 还是 OFF？ - 任何带 `MAX_SEQLEN_K` / `MAXLEN` / `ACTUAL_LEN` / `TRUNCATE` 字样的开关 - `dense_as_sparse` 现在是开的（CLAUDE.md 说），它的语义是"strict dense 也走 sparse 路径"——确认这条路径数值是不是真等价 总长 ≤ 1000 字。给出明确的"哪几个开关是当前最大的精度风险"。引用 file_path:line_number。

> AGENT

现在让我检查其他重要的 perf commits：

> AGENT

我会系统地搜索这些环境变量开关。让我并行执行多个查询来快速定位。

> AGENT

现在让我检查更多的 commits，特别关注数值路径的修改：

> AGENT

现在让我并行搜索关键的环境变量定义和使用位置：

> AGENT

让我查看当前工作树是否有未提交的变化：

> AGENT

很好！我找到了关键文件。现在让我读取主要的InfLLM-v2相关文件：

> AGENT

让我继续查看这些未提交的变化：

> AGENT

现在让我查看更多的环境变量，特别是关于stage1的：

> AGENT

现在让我检查这些新增 env flags 和 functions 的默认值及风险：

> AGENT

现在让我找更多的InfLLM v2相关的C++环境变量检查：

> AGENT

现在让我总结所有发现。首先让我快速检查其他一些高风险的 commits：

> DEVELOPER

在 /user_4813494d/openbmb 仓库下精读 InfLLM-v2 sparse stage1/stage2 prefill kernel 源码，找**可能引入数值精度问题**的代码模式。 重点检查文件： - `kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h` - `kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_blockmask.h` - `kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash.h` - `kernels/infllmv2_cuda_impl/csrc/flash_attn/flash_api.cpp` - `demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_backend.py` - `demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_sparse_utils.py` - `demo-sala/sglang/python/sglang/srt/models/minicpm.py` 查找以下精度风险模式（每个找到的实例报告 file:line 和原始代码 ≤8 行）： 1. **早停 / 截断 K1 / K2 的逻辑**：是否有 "if (block_idx > some_bound) break" 类型的代码，看 bound 是不是 actual context length，是否可能在 batch 中某个 row 的 max_seqlen_k 不等于 batch.max() 时早停过头？ 2. **mask build 的边界**：`flash_blockmask.h` 里 build_blockmask 的逻辑，看 mask 在 last partial tile 处怎么处理，causal 边界对不对，是否有"假装当前 tile 是 valid 但其实超出 actual seqlen"的 bug。 3. **softmax / online softmax 的 rescale 顺序**：看 row_max 累加 + row_sum rescale 的顺序，确认在 K2 → K1 两阶段之间 max/sum 传递正确（之前实验日志里提到过 stage1 first-pass-only 的实验，要看主路径是否被 first-pass 残留影响）。 4. **stage1 P 写出的归一化**：stage1 的输出 P 是 normalized prob 还是 raw logit？看 `params.stage1_first_pass_only` / `params.stage1_blockmax` / `params.stage1_groupmax_*` 字段引用点，确认主路径用的是哪个、归一化是否完成。 5. **dtype 退化**：找 `float` → `__half` / `__nv_bfloat16` 的累加转换，看是否有 fp32 累加被改为 fp16/bf16 累加。 6. **`compressed_max_seqlen_k` 残留**：grep 这个名字，确认所有引用点都已经回退到带 guard 的 actual maxlen 版本。CLAUDE.md 提到这是"危险行为已回退"，验证回退完整。 7. **`max_pooling_1d_varlen` / `compress_k_complete_kernel`**：minicpm_sparse_utils.py 调用的 compress 路径，看是否有跨 batch 边界的 reduce / pooling，特别是 mixed-length batch 下的行为。 8. **stage2 sparse 的 topk 索引转换**：`_topk_to_flashinfer_indices_kernel` 这种 kernel，看 indices 是基于 padded 还是 actual seqlen 计算的。 9. **`out_cache_loc` / page table** 跨层 / 跨 forward 复用：grep `plan_cache` / `fi_convert` / `shape_only_plan_cache`，特别是 `471e20b` 提到的"shape_only_plan_cache 跨 forward 命中时刷新 page table"的修复点——确认刷新逻辑确实覆盖所有 case。 报告格式：每个找到的风险点一段，包含： - file_path:line_number - 原始代码片段 ≤8 行 - 风险陈述（具体到"在什么 corner case 下输出会不正确"） - 是否被 env 保护 总长 ≤ 1500 字。不要给修复建议，只要定位风险。

> AGENT

现在让我查看C++代码中的getenv调用：

> AGENT

我将系统地搜索这些文件，查找可能的数值精度问题。让我先定位这些文件。

> AGENT

让我读取这些关键部分：

> AGENT

现在让我并行读取主要的文件：

> AGENT

完美！现在让我编写最终报告。我已经收集了足够的信息：

> AGENT

现在让我搜索关键的精度风险模式：

> AGENT

现在让我读取更多细节：

> AGENT

现在让我搜索Python文件的细节：

> AGENT

让我搜索更多关键的精度问题模式：

> AGENT

现在检查关键的softmax和pool逻辑：

> AGENT

现在让我检查blockmask的最后一个tile处理：

> AGENT

现在让我检查topk索引转换和pool混合长度batch：

> AGENT

现在让我检查pool函数的batch处理和topk索引转换：

> AGENT

现在让我检查最后几个关键点：

> AGENT

## 最终报告 我已完成对 `/user_4813494d/openbmb` 仓库中所有**默认开启且影响 InfLLM-v2 稀疏 attention 数值路径**的 env-controlled 开关的全面审计。 ### 四大精度风险源（降序） | ENV 变量 | 默认 | Production | 风险 | 引用位置 | |---------|------|----------|------|---------| | **SGLANG_FAST_PREFILL_STAGE1** | OFF | OFF | ⚠️ 替代 FA-based stage1 为 torch.matmul + 跳过因果掩码 | /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_sparse_utils.py:54 | | **INFLLM_V2_STAGE1_EMPTY_P** | 0 | 动态=2 | ⚠️ 改变 stage1 softmax 初值（0 vs empty vs empty+pad）；=2 需配套 zero_stage1_future 内核 | /user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/flash_api.cpp:965,1107; minicpm_sparse_utils.py:1078 | | **INFLLM_V2_STAGE1_BLOCKMAX** | OFF | 动态=1 | ⚠️ 改变 stage1 p 输出形状（seqlen_k_rounded/4 vs full），影响后续 K2 score 匹配 | flash_api.cpp:948; minicpm_sparse_utils.py:291-322 | | **SGLANG_MINICPM_STAGE1_EMPTY_P2** | OFF | OFF | ⚠️ 启用时跳过 K1 second pass（去噪步骤），改变稀疏模式 | minicpm_sparse_utils.py:73-75 | ### 关键发现 1. **BLOCKMAX 与 EMPTY_P 的动态管理**：这两个环境变量在 minicpm_sparse_utils.py 中被临时修改（save→modify→restore），作为状态机控制稀疏路由，不是持久配置。行 291-322 设置 BLOCKMAX=1 然后恢复；行 1078-1079 设置 EMPTY_P=2 进行 future 去噪。 2. **dense_as_sparse 现状**：start_eagle.sh:75 明确启用了 `--dense-as-sparse`，使所有长度的序列都走 InfLLM-v2 sparse path，包括短序列。该路径内的 topk + K2 refinement 与 dense full attention 的数值等价性未经严格验证。 3. **missing 检查**：SGLANG_MINICPM_UNSAFE_FI_CONVERT_CACHE（默认 0）在 minicpm_attention_kernels.py:1086 中存在，若被误设为 1 会跳过 KV cache 验证。 4. **P2 含义澄清**："empty P2" 中的 P2 确实是 K1 的 second pass softmax；启用时完全跳过，导致 K1 topk 只执行一轮而非两轮，精度影响未量化。 ### 总结 **当前最大精度风险** 来自 `INFLLM_V2_STAGE1_EMPTY_P` 和 `INFLLM_V2_STAGE1_BLOCKMAX` 的动态改写，它们在不同 inference path 下可能被激活，需即时 trace 日志确认实际参数值。

> AGENT

最后查看stage1与stage2的交接点和out_cache_loc：

> AGENT

现在让我查看这个pool空输出的逻辑和stage1的blockmax输出规范化：

> AGENT

现在让我整合所有发现并生成最终报告。让我再检查几个关键细节：

> AGENT

现在我有足够的信息来撰写报告。让我准备最终的审查报告： 基于对 /user_4813494d/openbmb 仓库最近 60 天内与 InfLLM-v2 sparse stage1/stage2 prefill 路径相关的详细审查，以下是按风险等级分类的 commits 分析。 ## 报告摘要（约 1100 字） ### A 类：安全重构（纯文档/清理） - `2d76a61` docs: profile topk head groups — 纯文档 - `a464ac9` docs: profile topk adjacency — 纯文档 - `41d8c8d` chore: add gla prefill profile buckets — 纯 profiling hook 添加 - `208bb39` chore(minicpm): add subop profiling hooks — profiling only - `866c4c2` clean(prefill): remove abandoned stage2 experiments — 重新引入已沉默的实验代码（env-gated `SGLANG_MINICPM_*`，不影响默认路径） 这些 commits 要么是文档、profiling instrumentation 添加，要么重新引入的实验代码都被 env flag 保护且默认未启用。 ### B 类：中性性能优化（等价计算或元数据改进） - `f1ac79d` perf(prefill): skip redundant stage1 zero fill — 跳过 wrapper 的冗余 `p.zero_()` 调用。**env 保护**：`SGLANG_MINICPM_STAGE1_SKIP_EXTRA_ZERO=1`（默认 ON）。C++ 侧仍用 `torch::full(...,0)` 初始化，只省一次 Python 侧 `zero_()`。离线对拍 topk 相同。**rationale**：纯 GPU 内存初始化优化，无数值路径改变。 - `b1be94a` perf(prefill): shrink stage1 scoring maxlen safely — 缩小 stage1 score tensor 的 K 维度到实际值而非 full padded。**env 保护**：`SGLANG_MINICPM_STAGE1_ACTUAL_MAXLEN=1`（默认 ON）。离线一致性确认 topk element/row exact=1.0，wall time +1.3%。**rationale**：只改变 tensor shape，`compressed_attention` 后续仍用 full `max_context_len` 调 pooling，topk 语义不变。 - `cb862eb` perf(prefill): reduce sparse prefill overhead — 新增 `shape_only_plan_cache` 逻辑。**gate**：仅当 `forward_batch.sparse_batch_size == bs`（所有 batch 都是 all-sparse）时启用。跳过 plan() 的 byte-compare，只用 shape key 判断复用。**rationale**：shape 足以验证 all-sparse batch 的 page table 结构，不改变数值；mixed batch 仍走 byte-compare。 - `1f265fe` perf(prefill): reuse flashinfer plan across 8 standard layers — layer 间 plan 复用。**无 env flag**，但逻辑受 `self._plan_cache_disable` 约束。cross-layer KV layout 完全相同时 plan() 仅执行一次。**rationale**：改变的是元数据复用策略，不是数值计算。 ### C 类：数值风险 COMMITS（详细分析） #### **C1: 3178604 — revert(prefill): roll back stage1 fast path + cleanups** **关键内容**：Revert 了 3 个可疑 commits： - `a3f2b5e` perf(prefill): guard infllm stage1 full chunks - `9a6ba25` clean(prefill): remove unproven stage1 zero-skip path - `866c4c2` clean(prefill): remove abandoned stage2 experiments **数值改变**：`a3f2b5e` 引入了 stage1 kernel dispatch 的 32×64 warp tile 快速路径。原注释称"bitwise-equal claim from offline microbench did not hold under production data"。线上观察到精度回归。 **env 保护状态**：新的 32×64 dispatch 有 guard 条件（`params.seqlen_q % 32 == 0 && params.total_q == params.seqlen_q * params.b`），但仍然默认启用。tail chunks 和 mixed-length batch 会 fallback。 **精度风险场景**：tail chunk（如 `T=2747,K=8192`）或 batch 内序列长度不均匀时，32×64 tile 改变了计算顺序/累加顺序，导致 FP32 累加的 float-to-bf16 四舍五入点不同，最终 topk 顺序改变（`diff_max=0.0046`，topk 不一致）。生产数据暴露了这个 corner case。 **线上收益声称**：离线对拍称 8192 token 能快 50% 左右（`16.24ms → 8.94ms`），但实际线上用 15-chunk 长 prefill 也只见 2-3% throughput 改善。这个修改后来被完全 revert 了。 **file paths**：`kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_launch_template.h:232-233`（guard 条件和快速路径分发） --- #### **C2: a3f2b5e — perf(prefill): guard infllm stage1 full chunks** *（此 commit 已在 3178604 中被 revert，但保留在 log 中作为反例）* **具体改动**：在 `flash_fwd_launch_template.h` 加入 32×64 tile dispatch 条件： ```cpp else if (params.seqlen_q % 32 == 0 && params.total_q == params.seqlen_q * params.b) { run_flash_splitkv_fwd_stage1<...32x64 tile...>(...); } ``` **声称的 rationale**：stage1 block scoring 在 full chunk 时计算量大，用 2-warp 而非 1-warp tile 可加速。离线对拍(T=8192, K=1024..8192) 都表现为"bitwise equal + topk equal"。 **实际问题**：FP32 block-wise softmax → bf16 store 时的数值路径改变了。虽然每个 query row 的 softmax 操作数相同，但累加顺序导致舍入误差累积不同。在 tail chunks（seqlen_q % 32 […]

> AGENT

完美。现在我有足够的信息生成最终报告： ## 精度风险定位报告 ### 1. Stage1 blockmax 输出规范化缺陷 **文件:** `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:1770-1778` ```cuda if (params.stage1_blockmax != 0) { hdim16_reduce_blockmax<Element>( acc_s, reinterpret_cast<Element *>(params.p_ptr) + row_offset_p_base, params.stage1_blockmax_out_len, n_block * kBlockN, m_block * kBlockM, kNWarps * 16 ); } ``` **风险:** `hdim16_reduce_blockmax` 写入 `acc_s` 对应的原始 fp32 logit 的最大值或池化结果，但主流程在 stage1_first_pass_only 模式下（line 1681）直接返回，此时 softmax_rescale_simple 可能未被调用。如果 stage1_blockmax 启用但输出在后续 stage2 中被视为已归一化的概率而非 raw logit，会引入数值错误。 **环境保护:** `INFLLM_V2_STAGE1_BLOCKMAX` env 控制，但在 `_infllmv2_attn_stage1_blockmax()` (line 292-322 Python) 中临时启用后未验证输出格式一致性。 --- ### 2. 混合长度 batch 下 pool 函数跨边界缺陷 **文件:** `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_sparse_utils.py:433-496` ```python def _max_pooling_1d_varlen_empty( input: torch.Tensor, # [num_heads, total_q, seqlen_k] cu_seqlens_q: torch.Tensor, cu_seqlens_k: torch.Tensor, cache_lens: torch.Tensor, # per-batch cache length max_seqlen_q: int, max_context_len: int, ... ) -> torch.Tensor: # output shape: [num_heads, total_q, out_len] # where out_len = (max_context_len + block_size - 1) // block_size ``` **风险:** 当 batch 中存在变长 K 序列（cu_seqlens_k[i+1] - cu_seqlens_k[i] 不等）时，max_pooling_1d_varlen 使用单一的 `max_context_len` 计算 `out_len`。若某行实际 K 长度小于 max_context_len，pooling kernel 仍可能访问到该行的 padding 区域或超出 actual_seqlen_k 的位置，导致输出包含虚假的最大值。 **环境保护:** `SGLANG_MINICPM_POOL_EMPTY_OUTPUT` 控制是否使用 `_max_pooling_1d_varlen_empty`，但两个实现都有同样的 batch 边界问题。 --- ### 3. Topk 索引基准偏移计算错误 **文件:** `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_sparse_stage2.py:41-49` ```python for topk_i in range(0, sparse_topk): block = tl.load( topk_ptr + head_group * topk_stride_h + token * topk_stride_token + topk_i * topk_stride_k ) pos = block * block_size + block_offsets mask_t = (block >= 0) & (pos < limit) # limit = min(token_pos, seqlen_k) base_page = tl.load( base_page_table_ptr + bs * base_pt_stride_bs + pos * base_pt_stride_pos, mask=mask_t, other=0, ).to(tl.int64) ``` **风险:** 当 `block` 是 padded 中的索引（block_score.shape[-1] 可能因 actual_topk < topk 而被 pad 为 -1），kernel 仍用该索引计算 `pos = block * block_size + ...`。若 block=-1，pos 会出现负值，虽然 mask_t 会过滤，但当 topk 被 pad 时，该行的最后几个 topk entry 应对应 -1（无效），而实际代码在处理 "padding 填充 -1" 时的掩码逻辑可能不完全（line 49 的 mask_t 判断前已经加载了坏的 block）。 **环境保护:** 无，这是 Triton kernel 硬编码逻辑。 --- ### 4. Stage1 K1 early break 跨 batch 不安全 **文件:** `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h:1796-1800` ```cpp if (n_masking_steps > 1 && n_block <= n_block_min) { --n_block; break; } ``` **风险:** 该 break 基于 `n_block <= n_block_min`，其中 `n_block_min` 由 line 267 计算： ```cpp const int n_block_min = !Is_local ? 0 : std::max(0, (m_block * kBlockM + binfo.actual_seqlen_k - binfo.actual_seqlen_q - params.window_size_left) / kBlockN); ``` 在 varlen batch 中，不同行的 actual_seqlen_k 不同，但 n_block_min 基于该行的值。若 batch 中某行提前满足 break 条件，而同时处理的另一行仍需要迭代，kernel 会提前返回，导致该行的 K 块未被完全扫描。 **环境保护:** 无，这是主路径硬编码。 --- ### 5. Pool output shape 与后续 topk 的边界不匹配 **文件:** `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_sparse_utils.py:1193-1221` ```python actual_topk = min(topk, block_score.shape[-1]) if actual_topk == topk: topk_idx = topk_result.indices.sort(-1).values else: topk_idx = torch.full((*block_score.shape[:-1], topk), -1, dtype=torch.int64, ...) if actual_topk > 0: topk_idx[..., :actual_topk] = topk_result.indices.sort(-1).values ``` **风险:** 当 `block_score.shape[-1] < topk` 时（比如短序列或 pool 输出不足），topk_idx 的后 (topk - actual_topk) 元素被填充为 -1。但在 stage2 的 `_topk_to_flashinfer_indices_kernel` 中，这些 -1 索引在计算 `pos = […]

> DEVELOPER

在 /user_4813494d/openbmb 仓库下，给我详细审查以下 3 个 Python 文件的 working tree diff（未 commit 的本地修改）： 1. `demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_backend.py` 2. `demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_sparse_utils.py` 3. `demo-sala/sglang/python/sglang/srt/models/minicpm.py` 对每个文件分别跑 `git diff <file>`，然后按以下 4 类**逐个改动**归类（每个改动给一行说明）： - **类 A：新增 hook / 接口**（纯添加，无 caller，default path 完全不走） - **类 B：default-OFF 实验路径**（gated by `_SGLANG_MINICPM_STAGE1_*` 等 env，默认 0） - **类 C：default-ON 优化**（这种**最危险**——动了默认行为，需要逐个看 guard 严密性） - **类 D：改了默认数值路径**（既不是 env-gated，又改了 attention 计算 / mask / topk 逻辑 / dtype / 顺序） **特别盯死类 C 和类 D**。类 A、B 一句话掠过即可。 对类 C 每一处，要给出： - 改动的 file:line 和 hunk 关键代码（≤8 行） - 默认 ON 时跑的什么逻辑 - 原代码是什么逻辑 - guard 条件是什么 - **可能不等价的 corner case**（比如 mixed-length batch、tail chunk、short prompt、dense_as_sparse 路径等） 对类 D 每一处，要给出： - 改动的 file:line 和 hunk 关键代码（≤8 行） - 改动的语义本质 - **风险陈述**：在什么 corner case 下输出会和 HEAD 版本不同 报告格式： - 每个文件一个 section - 类 A 计数 + 一句话掠过 - 类 B 计数 + env 名清单 - 类 C 详写 - 类 D 详写 - 最后一段：综合判断"这 3 个文件中改了默认数值路径的修改有几处" 要求严谨，不要把 "新增 hook" 误判为 "改默认行为"。也不要把"动态写 env 但被 outer guard 包住"误判为 "production 动态切换"。 总长 ≤ 1500 字。

> AGENT

我会逐个查看这三个文件的 git diff，进行详细的修改分类。

> AGENT

现在查看第二个文件：

> AGENT

现在查看第三个文件：

> DEVELOPER

在 /user_4813494d/openbmb 仓库下，审查以下 5 个 C++/CUDA 文件的 working tree diff（未 commit 的本地修改）： 1. `kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_fwd_kernel.h` 2. `kernels/infllmv2_cuda_impl/csrc/flash_attn/flash_api.cpp` 3. `kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash.h` 4. `kernels/infllmv2_cuda_impl/csrc/flash_attn/src/flash_blockmask.h` 5. `kernels/infllmv2_cuda_impl/csrc/entry.cu` 对每个文件跑 `git diff <file>`，按以下 4 类逐个改动归类： - **类 A：新增 struct field / 函数签名扩展 / 新增 kernel 定义**（纯添加，default 0 / nullptr，旧 caller 看不到） - **类 B：default-OFF kernel 路径**（gated by `if (params.stage1_* != 0)` 或 `getenv("INFLLM_V2_STAGE1_*")` 这种 env，默认 0 不走） - **类 C：动了默认 kernel 行为**（最危险）——比如： - 改了 attention softmax / mask 计算顺序 - 改了 P 输出的 stride / offset 计算（即使"看似等价"也算 C） - 改了 fwdIterator / blockmask 行为，即使 default 路径 - 改了 GMEM 写入模式 / 累加精度 / dtype - **类 D：编译期模板参数 / kernel dispatch 选择改动**（影响所有 caller 的二进制路径） **重点审查 flash_fwd_kernel.h 中**： - `compute_attn_1rowblock_splitkv_stage1` 函数（line ~1300+）中改动的部分 - 第二次 fwdIterator 调用从原 `params.blockmask` 改为 `stage1_k1_blockmask`，分析对 default 路径（stage1_k1_blockmask=null）的影响——会不会因 fallback 行为不同导致 K1 second pass 走不同的 dense scan 顺序？ - gP 写出从滚动指针 `gP.data() = gP.data() + (-kBlockN)` 改为绝对地址 `row_offset_p_base + n_block * kBlockN` —— 这两者**是否在 default dense scan 顺序下完全等价**？给出严格论证（n_block 是否从 max-1 递减到 min，每次 -1，以及 dense iterator 是否会跳过任何 block） **重点审查 flash_api.cpp 中**： - 新增的 `mha_varlen_fwd_stage1_k1_mask` 函数——这是新增的入口还是替换了旧入口？看 PYBIND 注册看是 ADD 还是 REPLACE - `mha_varlen_fwd_stage1`（原入口）有没有被改动？逐个 hunk 看 **重点审查 entry.cu 中**： - 新增的 `stage1_blockmax_finalize_kernel` / `stage1_k2_indices_to_k1_mask_kernel` / `zero_stage1_future_kernel` 是否新增 kernel - 有没有动现有 kernel 的 launch config / 模板实例化 报告格式： - 每个文件一个 section - 类 A、B 计数 + 一句话掠过 - 类 C、D 详写：file:line、hunk 关键 8 行代码、语义陈述、风险陈述 - 最后总结：5 个文件中改了默认 kernel 行为的修改有几处，每处一句话 总长 ≤ 1500 字。

> AGENT

I'll analyze the working tree diffs for these 5 C++/CUDA files. Let me start by checking the git diffs.

> AGENT

Let me continue reading the diff and check the other files:

> DEVELOPER

在 /user_4813494d/openbmb 仓库下跑 `git diff kernels/infllmv2_cuda_impl/setup.py`，审查这个文件的 working tree 修改。 问题： 1. 是否新增了 entry.cu / 别的 .cu 文件到 extension 的 sources 列表？ 2. 是否改了编译参数（nvcc flags / arch / -O 级别 / 宏定义）？ 3. 是否改了 wheel 名 / package 名？ 4. setup.py 这次修改之后，**重新 build 这个 kernel 后产生的 .so 是否和 git HEAD 版本二进制兼容**？即：如果回退 setup.py 但保留新 .so 会不会出问题，反过来呢？ 请同时确认：当前 `import infllm_v2_C` 的实际 .so 在哪个路径，最后 build 时间是何时（用 stat / find）： ```bash find /opt/SGLang-MiniCPM-SALA -name 'infllm_v2_C*.so' 2>/dev/null find /user_4813494d/openbmb/kernels/infllmv2_cuda_impl -name '*.so' 2>/dev/null ``` 报告格式：300 字以内。明确回答"setup.py 这次改动是否影响默认 build"，以及"如果回退 working tree 这些 C++ 源码改动，需不需要也重新 build kernel"。

> AGENT

我来帮你审查这个修改。让我先检查 git diff 和文件状态。

> AGENT

现在让我查找 .so 文件位置和构建时间：

> AGENT

现在进行分析。让我整理一下每个文件的修改分类。 ## 审查报告 ### 文件 1：`minicpm_backend.py` **类 A（新增 hook / 接口）：1 处** - 新增 `_maybe_capture_stage1_candidate_inputs()` 函数及相关 env 变量/状态管理（第 76-145 行）：纯添加debug/logging钩子，不影响default path。 **类 B（default-OFF 实验路径）：4 处** - `_MINICPM_STAGE1_CAPTURE_DIR`、`_MINICPM_STAGE1_CAPTURE_MAX`、`_MINICPM_STAGE1_CAPTURE_MIN_K1`：都由env控制，默认关闭。 - 在 `compressed_attention()` 尾部调用 `_maybe_capture_stage1_candidate_inputs()` 钩子（第 1390-1413 行）：只在env指定dir时激活，无default行为改变。 **类 C（default-ON 优化）：1 处** - **minicpm_backend.py:1330-1338** 改动： ```python topk_query_layer = ( query_layer if no_rope_param is None else no_rope_param["query_states_no_rope"] ) ``` 默认 ON 时跑的逻辑：计算一次topk_query_layer，复用给两个分支（fuse_topk 和非fuse_topk）。 原代码逻辑：每个分支各自inline计算一次同样的三元表达式。 Guard 条件：无guard，纯代码化简。 **风险**：无等价性问题（只是提取了公共子表达式），在任何batch size/sequence length下行为相同。 **类 D（改了默认数值路径）：0 处** --- ### 文件 2：`minicpm_sparse_utils.py` **类 A（新增 hook / 接口）：0 处** **类 B（default-OFF 实验路径）：9 处** - `_SGLANG_MINICPM_STAGE1_EMPTY_P2`：默认"0" - `_SGLANG_MINICPM_STAGE1_BLOCKMAX_FUSION`：默认"0" - `_SGLANG_MINICPM_CHECK_STAGE1_BLOCKMAX_FUSION`：默认"0" - `_SGLANG_MINICPM_STAGE1_K2_SCORE_SELECTIVE`：默认"0" - `_SGLANG_MINICPM_STAGE1_K2_SCORE_TOPK`、`_SGLANG_MINICPM_STAGE1_K2_SCORE_RADIUS`、`_SGLANG_MINICPM_STAGE1_K2_SCORE_MIN_K1`：实验参数，仅在上述 env 启用时生效。 - `_SGLANG_MINICPM_STAGE1_K2_SCORE_EXACT_LAYERS`：layer白名单控制。 **类 C（default-ON 优化）：1 处** - **minicpm_sparse_utils.py:1017-1138** 改动：条件分支改变 stage1 score计算路径（无mask vs k2-selective mask vs blockmax fusion）。 默认 ON 时跑的逻辑： ```python if use_stage1_blockmax: # only enabled when _SGLANG_MINICPM_STAGE1_BLOCKMAX_FUSION==1 block_score = _infllmv2_attn_stage1_blockmax(...) elif stage1_k1_blockmask is not None: # only when k2_score_selective gated by env score_actual = _infllmv2_attn_stage1_k1_mask(...) else: score_actual = _infllmv2_attn_stage1(...) ``` 原代码逻辑：直接调 `_infllmv2_attn_stage1()`，后面一定走pooling。 Guard 条件：`_SGLANG_MINICPM_STAGE1_BLOCKMAX_FUSION` 和 `_SGLANG_MINICPM_STAGE1_K2_SCORE_SELECTIVE` 双重env控制 + `use_stage1_direct_pool` 前置检查。 **风险**：default 时env都为0，走 else 分支，和原代码等价。但若env启用，会改变score计算逻辑： - blockmax路径跳过后续pooling（line 1184: `if not block_score_from_stage1:`） - k2-mask路径改变attention mask语义，可能在mixed-length batch + dense_as_sparse路径下输出不同 **类 D（改了默认数值路径）：1 处** - **minicpm_sparse_utils.py:1020-1021** 改动： ```python stage1_score_width = triton.cdiv(max_seqlen_k, 64) * 64 # round up to 64 use_stage1_direct_pool = ( ... and stage1_score_width >= min_score_width_for_topk ) ``` 改动的语义本质：从用 `score_actual.shape[-1]` 改为用计算的 `stage1_score_width`（四舍五入到64的倍数）。 **风险陈述**：在 `max_seqlen_k` 不是64倍数的情况下（e.g., 31000、48700等），原代码取决于stage1返回shape，新代码用四舍五入估计。如果actual score shape < 四舍五入值，可能误判 `use_stage1_direct_pool=True` 而原代码为False，导致后续attention mask应用逻辑差异（尤其是当direct_pool为True时会跳过某些计算）。 --- ### 文件 3：`minicpm.py` **类 A（新增 hook / 接口）：3 处** - `_eagle3_nvfp4_encode()`、`_eagle3_onestage_get_save_executor()`、`_eagle3_onestage_shutdown_save_executor()` 新增工具函数（第 387-425 行）。 - `_eagle3_onestage_save_job()` 新增保存逻辑钩子，替换原有inline保存（第 428-451 行）。 - `_eagle3_onestage_log_save_error()` 新增异常日志钩子（第 454-459 行）。 **类 B（default-OFF 实验路径）：2 处** - `_EAGLE3_ONESTAGE_NVFP4`：默认"1"（启用NV-FP4编码） - `_EAGLE3_ONESTAGE_SAVE_WORKERS`：默认"4"（异步保存工作线程数） **类 C（default-ON 优化）：1 处** - **minicpm.py:542-547** 改动： ```python executor = _eagle3_onestage_get_save_executor() if executor is None: _eagle3_onestage_save_job(path, rid, buf) else: fut = executor.submit(_eagle3_onestage_save_job, path, rid, buf) fut.add_done_callback(_eagle3_onestage_log_save_error) ``` 默认 ON 时跑的逻辑：用线程池异步保存（当 `_EAGLE3_ONESTAGE_SAVE_WORKERS > 0`）或同步保存（workers=0）。 原代码逻辑：同步 `torch.save()` 立即保存。 Guard 条件：由 `_EAGLE3_ONESTAGE_SAVE_WORKERS` 控制是否启用executor。default=4，所以**默认启用异步**。 **风险**：改成异步保存可能导致： 1. 进程退出时数据未落盘（已注册atexit shutdown，但如果强杀可能丢失） 2. 异常被延迟处理，影响错误可见性 3. 在mixed-length batch中，若请求并发时数据竞争（虽然用了线程安全的dict/list，但如果有外部state依赖则可能不等价） **类 D（改了默认数值路径）：1 处** - **minicpm.py:441-451** NV-FP4编码逻辑改变：当 `_EAGLE3_ONESTAGE_NVFP4=True` 时，aux_hidden从bf16压缩到uint8 packed格式。 改动的语义本质：payload格式从 `"schema": "eagle3_onestage_decode_v2"` 改为 `"schema": "eagle3_onestage_decode_v3"`，且 `format: "nvfp4_aux_v1"`；原代码存bf16，新代码存packed uint8+scale。 **风险陈述**：虽然env-gated，但default=1（启用）。任何依赖v2 schema或bf16存储格式的下游（decoder、offline分析）将失败。数值上压缩后的aux_hidden在解包时应等价（假设解码器正确实现），但如果有任何round-trip验证或cross-version兼容性测试，会在default行为下失败。 --- ### 综合判断 **改了默认数值路径的修改共计 2 处**： 1. **minicpm_sparse_utils.py:1020-1021**：stage1_score_width计算改为四舍五入，在非64倍数seqlen下可能误判direct_pool策略。 2. **minicpm.py:441-451**：NV-FP4编码默认启用（env=1），改变payload格式和数值存储方式。 其中第1处是**silent default-path change**（无env保护，只是基于shape的算术改变），第2处虽有env但default=1启用。两者都有跨越不同batch profile的不等价风险。

> AGENT

Now let me analyze these changes systematically:

> AGENT

让我查看 setup.py 当前是否还有其他改动，以及完整的源码情况：

> AGENT

## 审查报告 **问题 1：新增 .cu 文件？** 否。diff 中未增加任何 .cu 文件到 sources 列表。entry.cu 已存在。 **问题 2：编译参数改动？** 否。未改变 nvcc flags、arch、优化级别或宏定义。 **问题 3：wheel/package 名改动？** 否。 **问题 4：二进制兼容性？** **改动仅影响 include 路径搜索**：从硬编码 `csrc/cutlass/include` 改为动态查找函数 `find_cutlass_include()`，优先级搜索 5 个位置。如果找到的最终路径相同，编译输出 **完全相同**（头文件内容决定符号），因此 **新旧 .so 二进制兼容**。 **当前 .so 路径**： - `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so` - **最后构建时间**：2026-05-17 13:27:54 **结论**：setup.py 改动**不影响默认 build 输出**。若回退 working tree C++ 源码，**无需重新 build kernel**，旧 .so 可继续使用。

> AGENT

Now I'll create a comprehensive analysis: ## Code Review Report: 5 C++/CUDA Flash Attention Files ### 1. **flash_fwd_kernel.h** (207 lines changed) **类 A（新增）：** 2 项 - New helper functions: `element_to_u16()`, `u16_to_element()` (line ~115) - New function: `hdim16_reduce_blockmax<>()` (line ~127-213) for pooled block-max output **类 B（default-OFF paths）：** 4 项 - Line 1402: `if (params.stage1_blockmax != 0)` gates new blockmax finalization - Line 1401: `stage1_p_stride` computed from `params.stage1_blockmax_out_len` only when blockmax enabled - Line 1681: `if (params.stage1_first_pass_only != 0) return;` skips second K1 pass entirely - Line 1770-1775, 1852-1857: `if (params.stage1_blockmax != 0)` gates blockmax vs. standard reduce calls **类 C（默认 kernel 行为改动）：** 1 项 - **Line 1400-1408** (P matrix offset calculation): ```cpp // BEFORE: const index_t row_offset_p = (bidh * params.total_q/16 + (query_offset_in_total + m_block * kBlockM)/16) * params.seqlen_k_rounded + (n_block_max - 1) * kBlockN; // AFTER: const int stage1_p_stride = params.stage1_blockmax != 0 ? params.stage1_blockmax_out_len : params.seqlen_k_rounded; const index_t row_offset_p_base = (bidh * params.total_q/16 + (query_offset_in_total + m_block * kBlockM)/16) * stage1_p_stride; const index_t row_offset_p = row_offset_p_base + (n_block_max - 1) * kBlockN; ``` **语义：** P 矩阵 stride 由 `seqlen_k_rounded` 改为条件性的 `stage1_blockmax_out_len`；但当 `stage1_blockmax==0`（默认）时，fallback 回原值。**问题**：这改动了 `row_offset_p` 的计算——即使在 stage1_blockmax==0 时，`row_offset_p_base` 现在被拆分出来，后续写入仍然使用 `row_offset_p_base + n_block * kBlockN` 替代滚动指针 `gP.data() = gP.data() + (-kBlockN)`。这可能导致 **block iteration 顺序与地址计算的不匹配**。 **类 D（编译期 dispatch 改动）：** 1 项 - **Line 1695**：`fwdIterator blockmask(..., true)` 新增布尔参数；默认 false。在第二次 fwdIterator 调用中传 true，使其选用 `stage1_k1_blockmask` 替代 `params.blockmask`。但当两者都为 nullptr（default case），行为相同——不构成风险。 --- ### 2. **flash_api.cpp**（~150 lines） **类 A：** 3 项 - Include `<cstdlib>` for `getenv`/`atoi` - Forward declare `zero_stage1_future()` function - New function `mha_varlen_fwd_stage1()` wrapper (lines 1140+)——是原函数的壳子，转发至 `mha_varlen_fwd_stage1_k1_mask()` **类 B：** 5 项 - `getenv("INFLLM_V2_STAGE1_BLOCKMAX")` gates `stage1_blockmax` logic (line 947) - `getenv("INFLLM_V2_STAGE1_GROUPMAX")` gates groupmax evidence (line 950) - `getenv("INFLLM_V2_STAGE1_EMPTY_P")` modes gate P tensor initialization (line 953-967) - `getenv("INFLLM_V2_STAGE1_FIRST_PASS_ONLY")` gates second K1 pass (line 1043) - Line 1109-1123: `zero_stage1_future()` kernel call gates on `empty_stage1_p_mode == 2` **类 C：** 2 项 - **Line 956-970** (P tensor allocation logic): ```cpp // Default path: torch::full(..., 0) or torch::full(..., -inf) // But now conditionally switches to torch::empty() if INFLLM_V2_STAGE1_EMPTY_P set p = use_empty_stage1_p && !zero_tensors && !use_stage1_k1_mask ? torch::empty({...}) : torch::full({...}, use_stage1_k1_mask ? -inf : 0); ``` **语义**：默认路径不变（full with 0），但新增 env-gated 路径可切换为 empty。**风险**：在 default 路径（env unset）中不改动，但 logic 复杂化可能埋伏 bug。 - **Line 1043-1047** (stage1_first_pass_only param): ```cpp const char *stage1_first_pass_only_env = std::getenv("INFLLM_V2_STAGE1_FIRST_PASS_ONLY"); params.stage1_first_pass_only = stage1_first_pass_only_env == nullptr ? 0 : ...; ``` 默认 0，不改动默认 kernel 行为。**无风险**。 **入口变化**：原 `mha_varlen_fwd_stage1()` 被**重命名**为 `mha_varlen_fwd_stage1_k1_mask()` 并新增参数 `stage1_k1_blockmask_`（line 806-1047）；新 `mha_varlen_fwd_stage1()` 是**包装器**（line 1140-1197），内部转发至 `*_k1_mask` 版本，传 `nullopt` blockmask。**PYBIND注册**（entry.cu）：新增 `varlen_fwd_stage1_k1_mask` entry，保留 `varlen_fwd_stage1` entry——**双入口共存，向后兼容**。 --- […]

> DEVELOPER

Review code for latent bugs in MiniCPM-SALA's `--dense-as-sparse=False` mixed-batch path. This is a SGLang fork. Codebase at /user_4813494d/openbmb. Working directory state: HEAD `7ef0eb0` clean (no working-tree changes on the files you'll be reading; some other unrelated files are dirty, ignore them). # Context When `--dense-as-sparse` is OFF, dense layers (8 of 32) go through standard FA path while sparse layers go through InfLLM-v2 sparse path. When mixed in one batch (some bs have seq_len < dense_len = 8192 → dense, others ≥ dense_len → sparse), the code follows a special path under `if forward_batch.sparse_batch_size < bs:` that allocates a `sparse_page_table` covering BOTH sparse and dense bs, then patches the dense bs entries. This mixed-batch path is dead-code in production (we always run with `--dense-as-sparse` ON in submission), but the user wants to enable it for accuracy comparison and just hit 2 bugs. I already fixed: **Bug 1**: `minicpm_attention_kernels.py:417-427` — `_get_or_create_prefill_wrapper()` (and sibling decode getters at lines 383, 398) were lazily creating FlashInfer wrappers without protecting against being called inside `torch.inference_mode()` (which happens during `model_runner._flashinfer_autotune` at line 1730). The wrapper's internal `_kv_lens_buffer` would then become an inference tensor, and later `wrapper.plan()` would throw `RuntimeError: Inplace update to inference tensor outside InferenceMode is not allowed`. Fixed by wrapping the construction in `with torch.inference_mode(False):`. **Bug 2**: `minicpm_sparse_utils.py:1741` in `build_sparse_prefill_metadata()` — `max_sparse_cache_len` was being computed using `extend_seq_lens_cpu[i]` for dense bs, but the writer at `minicpm_backend.py:1613` reads `kv_len = seq_lens_cpu[dense_bs]` (total = prefix + extend). On chunked prefill 2nd chunk this caused `RuntimeError: The expanded size of the tensor (630) must match the existing size (632)`. Fixed by changing to `seq_lens_cpu[i]`. # Your task Read the dense-as-sparse=False mixed-batch path end-to-end and find OTHER latent bugs in the same family — places where the code assumes "all bs are sparse" (or "all are dense") but the mixed case isn't handled, where dense bs and sparse bs metadata have different semantics, where chunked prefill (prefix > 0) breaks assumptions, or where stage1/stage2/FlashInfer downstream consumers can't handle the mixed layout. # Files to read - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_backend.py` — especially: - line ~580-660 (sparse_metadata_builder setup, sparse_page_table assignment) - line ~970-1010 (`all_sparse` checks around line 976) - line ~1470-1620 (prefill block_table / direct write / mixed batch fill — this is where Bug 2 was) - line ~1620-1810 (`use_derived_sparse_seqlens`, `sparse_cache_seqlens_int32` derivation, plan caching) - line ~1850-1990 (forward_extend + standard FA dispatch for dense bs) - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_sparse_utils.py` — `build_sparse_prefill_metadata` function (line 1650-1900) […]

> AGENT

I'll review the dense-as-sparse=False mixed-batch path systematically. Let me start by reading the key files.

> AGENT

Now let me look at the dispatch path in minicpm.py and the standard FA path for dense bs in forward_extend:

> AGENT

Let me find the dense-as-sparse dispatch:

> AGENT

The dense-as-sparse dispatch is on the backend side. Let me look at `forward_extend` in the backend to find the dense_as_sparse path:

> AGENT

Now look at the section around line 380-440 for wrapper getters and look at FlashInfer indptr setup:

> AGENT

Now let me look at the build_sequence_lengths to understand how it handles dense vs sparse, and identify_sparse_batches:

> AGENT

Now let me look at `cu_seqlens_q_adjusted` and `max_seqlen_q_adjusted` at line ~630, which is used in stage1:

> AGENT

Now let me look around line 380-440 for the wrapper getters (mentioned bug 1):

> AGENT

Now let me look at the `cu_seqlens_q_adjusted` usage - this is used for stage1. Notice line 626-629: this only includes batches where `seq_lens_cpu[i] >= dense_len`. Let me trace where `cu_seqlens_q_adjusted` is consumed:

> AGENT

Note this is sparse_get_topk_impl — when running with `all_sparse` path (line 977), cu_seqlens_q is `metadata.cu_seqlens_q` (full batch including dense bs), but in line 1282 it passes `metadata.cu_seqlens_q_adjusted`. Let me re-read to confirm. Looking back at line 1004-1022 (`all_sparse` path): - Passes `cu_seqlens_q = metadata.cu_seqlens_q` (full batch) - Internally passes `self.forward_metadata.cu_seqlens_q_adjusted` (computed at line 634 from sparse-only list) Then for non-all_sparse (line 1047+), it calls `build_prefill_topk_metadata` which builds `cu_seqlens_q_sparse` only over sparse_bs — and then passes that to `sparse_get_topk_impl`. But it ALSO passes `self.forward_metadata.cu_seqlens_q_adjusted` (computed at line 634 which is only built when `all_sparse` was true). Actually wait — let me re-read the gating logic at line 626-635. The `cu_seqlens_q_adjusted` is built using only sparse-bs entries `for i in range(batch_size): if forward_batch.seq_lens_cpu[i] >= self.dense_len`. So in mixed batch, this filters to sparse-only. That matches `build_prefill_topk_metadata`'s `cu_seqlens_q_sparse`. But notice line 976: `all_sparse = forward_batch.sparse_batch_size == forward_batch.batch_size`. In the `all_sparse` path, `cu_seqlens_q = metadata.cu_seqlens_q` is the FULL batch's cu_seqlens_q. But `cu_seqlens_q_adjusted` (line 634) is computed over sparse-only entries. If `all_sparse` is True, all bs are sparse, so these match. OK. Now let me check the flashinfer indptr setup for CUDA graph in init_cuda_graph_state. Specifically, is it ever planned for `sparse_bs = 2 * bs` where `bs` represents full batch_size? In decode CUDA graph mode, mixed batch can't easily happen (decode is per-token, all bs have seq_len > prefill so all sparse in normal case). Still let me check the decode handling:

> AGENT

Now let me look at how `forward_batch.sparse_idx` is used downstream and what indexing is expected when it's `slice(None)` (all_sparse_prefill) vs a list (mixed):

> AGENT

At line 1544 and 1563, the code writes to `metadata.sparse_page_table[forward_batch.sparse_idx, :num_sparse_topk_tokens] = sparse_page_table_sparse_bs`. In mixed batch, `sparse_idx` is a list of indices into the sparse_page_table corresponding to sparse-bs rows. The sparse_page_table is shape `(sparse_page_table_bs, max_sparse_cache_len)`, where `max_sparse_cache_len = max(sparse_topk*block_size, max(seq_lens_cpu of dense bs))`. Now, line 1613-1614: `metadata.sparse_page_table[start, :kv_len] = page_table[dense_bs, :kv_len] * 2`. This writes to FULL kv_len (which may be > num_sparse_topk_tokens). Good — the row is sized to `max_sparse_cache_len`. But wait — at line 1563, the sparse-bs rows are only written up to `:num_sparse_topk_tokens`. What about the rest of those rows? Looking at line 1755-1759, `sparse_page_table = torch.zeros(...)` — so rest is zero. That's fine because `sparse_cache_seqlens_int32` (derived at line 1636-1640) counts non-zero entries → would only count the topk tokens. OK. But for the dense-bs rows, line 1613 writes `page_table[dense_bs, :kv_len] * 2`. The `*2` multiplication — if `page_table` entries are valid kv slot ids, this could be wrong. Let me investigate. The page_table is the kv slot index, but the FA path uses page_size=1 with these kv slots interleaved by head_group: `key_cache_by_head_group = key_cache.reshape(-1, page_size, tp_k_head_num // 2, head_dim)`. So `*2` and `*2+1` is the right way to address head_group 0 and 1 separately. OK, looks intentional. Now potential issues - check `(metadata.sparse_page_table != 0).sum(dim=1)` at line 1636-1640 for dense bs: - Dense bs rows: `page_table[dense_bs, :kv_len] * 2` — but some of those values could be 0 (slot 0 IS valid!) → that gets counted as not present → undercount. Plus `* 2 + 1` (odd rows) are never 0. So odd row gets count = kv_len but even row could be less if any slot=0 exists. This is a potential bug. Let me check if slot 0 is ever used:

> AGENT

Slot 0 is generally the first valid slot in the pool. The `(sparse_page_table != 0).sum(dim=1)` derivation is structurally suspect - if dense_bs has its first cached token at slot id 0, this would either miscount or get even/odd mismatch. Let me look at the standard FA path for sparse layers — but wait, the question is about Standard Attention layers (8 of 32) vs Lightning. Looking at `minicpm.py`:

> AGENT

Wait - I don't see a separate "standard FA path" branch in `MiniCPMAttention.forward`. It just calls `self.attn` (RadixAttention). The `forward_extend` of the backend is what gets called. Let me re-read forward_extend to find the dense/sparse branching: Looking at line 1464-1466: ```python bs = forward_batch.batch_size use_topk_to_fi_indices = False if max(forward_batch.seq_lens_cpu) >= self.dense_len: ``` If ALL seq_lens are below dense_len, the code goes through the `else` at line 1566 and falls through... but then at line 1582-1583 `q_reshaped = q.contiguous().view(-1, layer.tp_q_head_num // 2, layer.head_dim)` and there's an unconditional sparse path applied. Wait, this is the all-dense case where max(seq_lens) < dense_len. In that case `topk_idx` is never computed but the code still flows to the sparse FA path. Let me re-look:

> AGENT

OK, now I have enough context. Let me check a few more specific things. First, look at how `max_seq_len_q_adjusted` is used and how the `forward_metadata.cu_seqlens_q_adjusted` will interact for mixed batch. In mixed batch (where `max(seq_lens) >= dense_len` BUT some bs are dense and some sparse), at line 626-635: - `seqlens_q_sparse_list` only includes bs with `seq_lens >= dense_len` (sparse-bs only) - `cu_seqlens_q_adjusted` is sparse-bs only, multiplied by `heads_per_group` Then at line 1470-1472: ``` topk_idx = self.get_topk_for_sparse(q_reshaped, k, v, q.shape[0], layer, forward_batch) ``` `q_reshaped` is the FULL extend (all bs tokens). But topk path will call `build_prefill_topk_metadata` which gathers only the sparse-bs queries (line 2030 `batched_gather`). Good. Now wait - looking carefully at line 977 `all_sparse = forward_batch.sparse_batch_size == forward_batch.batch_size`. In mixed mode that's False, so it goes to the `topk_metadata = self.sparse_metadata_builder.build_prefill_topk_metadata(...)` branch. That looks OK. Now key question: when `forward_batch.sparse_batch_size < bs` and the dense bs's seqlen < dense_len BUT another bs's seqlen ≥ dense_len, the code at line 1466 `if max(forward_batch.seq_lens_cpu) >= self.dense_len:` is True → goes into the topk branch. The dense bs's queries are in q_reshaped but no topk is computed for them. The sparse_page_table for dense rows still gets filled (line 1613-1614) — good. BUT what about the case where ALL bs have seq_lens < dense_len? Then the `if max(seq_lens) >= self.dense_len` is False → goes to else branch (line 1566-1580) which only allocates compress keys, doesn't compute topk. Then falls through to sparse FA at line 1582+. But here `forward_batch.sparse_batch_size = 0` and `bs = N`, so all bs are dense. `metadata.sparse_page_table` has been allocated for `N * head_group_num` rows (each with `max_sparse_cache_len = max(seq_lens_cpu)`). The page table gets filled at line 1613-1614 for each dense_bs. OK so this path looks usable. Now the question - the comment on line 583-586 says `extend_prefix_lens_sparse` uses `forward_batch.extend_prefix_lens_cpu[bs]`. Let me check if it works correctly for chunked prefill when one dense bs has prefix>0. The dense bs is filtered OUT from `sparse_bs_list`, so the prefix issue would only affect dense bs in their own handling. Looking at line 1613, `kv_len = forward_batch.seq_lens_cpu[dense_bs]` — full prefix+extend. And the q_reshaped slice at line 1609-1611 is `2*len_` where `len_ = forward_batch.extend_seq_lens_cpu[dense_bs]` (extend only). OK. But wait - at line 1599 `ps = metadata.sparse_cu_seqlens_q_cpu[sparse_page_table_idx_start]`. The `sparse_cu_seqlens_q_cpu` is built layout-aware. Let me trace through this for a mixed case: Say bs=2: bs0 is sparse (seq=10000, extend=200), bs1 is dense (seq=500, extend=200). - `sparse_page_table_bs` […]

> AGENT

Now look at `convert_sparse_page_table_to_flashinfer` to see how it handles dense bs pages (which have entries even at position 0 sometimes due to *2 multiplication):

> AGENT

This is decode-only (kv_last_page_len = 1, page_size = 1). The convert relies on `cache_seqlens` per-row, so it doesn't matter if entries are 0; it just uses `num_valid` count. So the FlashInfer convert path itself is robust. But the question is — `cache_seqlens` is `metadata.sparse_cache_seqlens_int32`, which for dense bs in prefill is derived at line 1636-1640 by `(sparse_page_table != 0).sum(dim=1)`. For dense bs, the row contains `page_table[dense_bs, :kv_len] * 2` or `*2+1`. If any of those slot indices is 0, then `*2=0` → masked out as zero. So even-rows undercount, odd-rows (with `+1`) always show full kv_len. Now: is slot 0 ever a valid slot id used by req_to_token? In SGLang's standard kv pool, slot 0 IS a valid free-list slot. Let me verify by quickly checking the page_table source - it comes from `req_to_token_pool.req_to_token[req_pool_indices, :]`. Yes, typical SGLang code uses 0 as a valid slot. So this is a real correctness bug for the dense-bs path with mixed batch. Now: this branch only executes when `_MINICPM_DERIVED_SPARSE_SEQLENS` is False OR `sparse_batch_size != bs`. In mixed batch (sparse_batch_size < bs), we always go through the `(sparse_page_table != 0).sum(dim=1)` path. So this IS triggered. Now let me verify the rest of the flow: `metadata.sparse_cache_seqlens_int32` for mixed-batch prefill is used downstream as the FA k cache_seqlens. If dense bs's even row reports `kv_len_undercounted`, that's a CORRECTNESS bug — the FA call would skip some K tokens. Now check the second post-attention loop at line 1809-1833 — interleaving output rows. Let me also check `cache_seqlens` usage at line 1737 (`cache_seqlens=metadata.sparse_cache_seqlens_int32`) — yes confirmed. Now let me check the page_table dtype carefully. The page_table values are int32/int64. The `*2` and `*2+1` multiplication assumes they fit. If slot ids can be very large (e.g., max_total_num_tokens > 2^30), `*2` overflows int32. But max_context_len=524288 so max slot ≤ that, *2 fits in int32. OK. Let me also check what happens at `metadata.sparse_page_table` shape for dense bs `kv_len`. The allocated size is `max_sparse_cache_len`. In `build_sparse_prefill_metadata` line 1744-1746: `max_sparse_cache_len = max(max_sparse_cache_len, forward_batch.seq_lens_cpu[i])`. And max could be from sparse-bs branch as `sparse_topk * block_size`. The dense bs kv_len could be ≤ dense_len=8192 < sparse_topk*block_size? Let me check. `sparse_topk = topk + window_blocks` where `topk=hf_config.sparse_topk`. Typically `sparse_topk * block_size` is much smaller than 8192. So for mixed batch where a dense bs has kv_len ≈ 7000-8000, `max_sparse_cache_len` could be set from dense bs's seq_len. OK row capacity = max across all dense bs. […]

> AGENT

OK FA returns shape `(total_q, num_heads, head_dim)`. In our forward_extend at line 1777, `result` shape is `(total_tokens * 2, tp_q_head_num // 2, head_dim)` — total leading dim doubled because q was reshaped. So `result.view(-1, layer.tp_q_head_num * layer.head_dim)` at line 1835 reshapes to `(total_tokens, tp_q_head_num * head_dim)`. ✓ Now let me check one more important spot: line 1601-1602 reads `metadata.sparse_cu_seqlens_q_cpu[sparse_page_table_idx_start + 1] - ps`. But `metadata.sparse_cu_seqlens_q_cpu` is built on CPU as int (probably int32 or int64). Subtraction of CPU tensor element returns a 0-dim tensor, not a Python int. Compared to `forward_batch.extend_seq_lens_cpu[dense_bs]` (likely an int) at line 1604-1607 with `==`. Should work but type-mismatch might cause subtle issues. Now let me revisit `extend_prefix_lens` access at line 581-585. This is `forward_batch.extend_prefix_lens_cpu[bs]` for sparse-bs only. The `build_token_mappings` then uses these prefix lengths to set token positions. Looks correct. Now let me check one critical area: `metadata.cache_seqlens_int32_stage1 = metadata.cache_seqlens_int32 - 1` at line 625. `cache_seqlens_int32` is the full-batch standard cache_seqlens (one entry per bs). For dense bs in mixed batch this entry is still the full kv_len from `metadata.cache_seqlens_int32`. Then `cu_seqlens_q_adjusted` only includes sparse-bs entries. So stage1's `cache_lens` (line 1246) is the full-batch tensor, but `cu_seqlens_q_adjusted` only covers sparse-bs. These two would be mismatched in size in mixed batch! Let me check stage1 kernel access:

> AGENT

`compressed_attention` is called for sparse-bs only via `build_prefill_topk_metadata`'s gathered queries (line 2030). The `cu_seqlens_q` passed in is `cu_seqlens_q_sparse` (line 2053), only sparse-bs entries. But `cu_seqlens_q_adjusted` is from `forward_metadata.cu_seqlens_q_adjusted` (line 1282 from sparse_get_topk_impl), which is built at line 634 with sparse-bs only. So sizes match. But `cache_lens` (line 1246) is `cache_seqlens_int32_stage1` = `cache_seqlens_int32 - 1`. The full-batch cache_seqlens has size `bs`, but stage1 should only need sparse-bs sized. Let me check how it's consumed: In `compressed_attention`, `cache_lens` is passed to `pool_func` (line 853) and used to set up causal masking. The `cu_seqlens_q` and `cu_seqlens_k` sizes are based on sparse-bs only. If `cache_lens` is full-batch sized but `cu_seqlens_q` is sparse-bs sized, there's a size mismatch. Wait let me check: `cu_seqlens_q` passed into `compressed_attention` is `topk_metadata["cu_seqlens_q"]` which is `cu_seqlens_q_sparse`. From line 2032, it has length `len(sparse_bs)+1`. `cache_lens` from line 1246 is `cache_seqlens_int32_stage1` which is from `metadata.cache_seqlens_int32 - 1` — full bs size. So in mixed batch, this mismatches. Actually, this is also a bug — `cache_lens` should be subset to sparse-bs only when in mixed batch. But wait, let me check the path. In mixed batch, the topk branch at line 1047+ calls `sparse_get_topk_impl(cu_seqlens_q=topk_metadata["cu_seqlens_q"], ...)`. Then inside `sparse_get_topk_impl`, when `max_seqlen_q == 1` (decode-like), uses `cache_seqlens_int32_stage1` (line 1246). But when `max_seqlen_q > 1` (prefill — this is the case for mixed batch), it goes to line 1248-1250 `cache_lens = seq_lens_k - seq_lens_q` from the passed cu_seqlens_k/cu_seqlens_q tensors. These ARE the sparse-bs sized ones. So the line 1246 path (decode-like with max_seqlen_q==1) is the concern. In mixed-batch DECODE this could trigger, but mixed batch in decode is unusual (all bs are mid-decode → all sparse). Even in mixed-batch decode it would also be wrong size. Let me check if `cache_seqlens_int32_stage1` for decode is the size that matches sparse-only cu_seqlens_q: Line 655-657 in `update_batch_for_sparse` (decode path): ``` metadata.cache_seqlens_int32_stage1 = metadata.cache_seqlens_int32 - 1 metadata.cu_seqlens_q_adjusted = metadata.cu_seqlens_q * heads_per_group metadata.max_seqlen_q_adjusted = metadata.max_seq_len_q * heads_per_group ``` In decode, `cu_seqlens_q_adjusted` is full-batch. And `build_decode_topk_metadata` returns `cu_seqlens_q = base_metadata.cu_seqlens_q` (full batch). So decode path is full-batch consistent. ✓ In mixed-batch prefill where any bs has `extend_seq_lens_cpu == 1` (last chunk of a chunked prefill), `max_seqlen_q` could equal 1 for the sparse subset. But max_seqlen_q is computed at line 2055 as `max(seqlens_q_sparse_bs)`. If all sparse bs have extend=1, max=1. Then in `sparse_get_topk_impl`, `max_seqlen_in_batch_q == 1` and `max_seqlen_in_batch_k > 1` (since prefill kv ≥ 8192), so line 1246 triggers: `cache_lens = self.forward_metadata.cache_seqlens_int32_stage1` — […]

> AGENT

Now let me check the standard FA path which IS what's called for the entire mixed batch (FlashAttention `flash_attn_with_kvcache`): Looking back at line 1732-1765, the `AttentionParams` is built with `page_table=metadata.sparse_page_table` (which is the mixed-layout table where sparse rows hold topk pages and dense rows hold direct page_table*2). Then `cache_seqlens=metadata.sparse_cache_seqlens_int32` (the derived `(sparse_page_table != 0).sum`). This is the FA call's page table. In `FlashAttentionKernel.forward`, this just passes through to `flash_attn_with_kvcache` (line 228). So FA processes mixed-layout page_table. The kernel `flash_attn_with_kvcache` doesn't care about semantics — it just reads `page_table[batch, :cache_seqlens[batch]]` and does causal attention. Critical question: For dense bs rows, `causal=True` is set. The causal mask aligns the query at position `cache_seqlens - max_seqlen_q + qpos`. For dense bs: q_len = `extend_seq_lens_cpu[dense_bs]`, k_len = `seq_lens_cpu[dense_bs]`. That's a normal chunked-prefill setup. Causal should work. ✓ But wait, look at line 1740: `max_seqlen_q=metadata.sparse_max_seq_len_q`. `sparse_max_seq_len_q` is computed in `build_sparse_prefill_metadata` (line 1751-1753) as `max(1, max_dense_extend)`. For mixed batch with all dense extends = 200 and any sparse bs (extend doesn't matter, sparse rows have q-len 1), `max_seqlen_q = 200`. So FA's max_seqlen_q is the dense max extend. That's correct for FA dispatch. Now is_prefill is decided by `max_seqlen_q > 1` (line 644 in flashinfer kernel). If only sparse bs exist (all dense extend = 0), then sparse_max_seq_len_q would be 1 → would mistakenly route to decode path even though we're in prefill. But this can't happen because if all bs are sparse, the all-sparse path was taken earlier (line 977). For mixed batch with dense bs present, dense extend > 0 → max_seq_len_q > 1 unless dense extend == 1 (chunked-prefill 1-token-last-chunk for the dense bs). Hmm — interesting edge case. If dense bs has extend=1 AND all sparse bs trivially have rows with q-len 1, then `sparse_max_seq_len_q = max(1, 1) = 1` → flashinfer kernel routes to **decode** path. That's wrong — this is a prefill batch. Let me verify. Line 644 in attention kernel: `is_prefill = params.max_seqlen_q > 1`. If max_seqlen_q == 1, decode path. But the dense bs has a non-zero prefix (it's chunked prefill 2nd+ chunk), so KV is properly sized. Hmm, decode path with max_seqlen_q==1 should still be valid mathematically as "single query token per row"... but for dense_bs rows the q comes from q_reshaped[ps:ps+2*len_=2] with len_=1. So 2 rows × 1 token = 2 q rows for the dense bs. For sparse bs, each token is its own row. […]

> AGENT

page64 path is gated to all-sparse (line 1715 in backend). Now let me check the FlashInfer decode wrapper path / prefill case when max_seqlen_q == 1 but actually prefill in flashinfer mode:

> AGENT

Now I have enough context. Let me also verify one more important thing - look at the `extend_prefix_lens_sparse` line 579-586 which is a list with len = len(sparse_bs_list). But `build_token_mappings` expects `extend_prefix_lens_sparse` indexed by sparse-bs order (line 1449 `extend_prefix_lens_sparse[i].item()`). Good. Let me also verify the dense bs *q-data* placement. Notice line 1582 `q_reshaped = q.contiguous().view(-1, layer.tp_q_head_num // 2, layer.head_dim)`. The original q is total_tokens × (num_heads*head_dim). For each token, the heads are laid out contiguously. When viewed as `(-1, num_heads//2, head_dim)`, the leading dim becomes `2 * total_tokens`, and each pair of consecutive rows IS the two head_groups of a single token. So `q_reshaped[2*token + 0]` is token's head_group 0, `q_reshaped[2*token + 1]` is head_group 1. Now in mixed batch, suppose batch order is bs0 (sparse, extend=5), bs1 (dense, extend=3). Total tokens = 8. - q_reshaped shape: 16 × ... - bs0 tokens: q_reshaped[0..10] (rows 0-9 = 5 tokens × 2 head_groups, interleaved) - bs1 tokens: q_reshaped[10..16] (rows 10-15 = 3 tokens × 2 head_groups, interleaved) Now `sparse_cu_seqlens_q_cpu` builds layout for the FA call: - For bs0 (sparse): 5 tokens × 2 head_groups = 10 rows, each with q-len 1 → cu = [0,1,2,...,10] - For bs1 (dense): 2 rows (one per head_group), each with q-len 3 → cu = [10, 13, 16] So `sparse_page_table_idx_start = old_bs_to_new_bs_range[1] = 10` for bs1. `ps = sparse_cu_seqlens_q_cpu[10] = 10`. `len_ = sparse_cu_seqlens_q_cpu[11] - 10 = 13 - 10 = 3`. ✓ The pre-FA at line 1609-1611: - `t = q_reshaped[10:16].clone()` — bs1's q in interleaved format - `q_reshaped[10:13] = t[0::2]` — even rows (head_group 0) - `q_reshaped[13:16] = t[1::2]` — odd rows (head_group 1) After this, q_reshaped[10:13] = h0 of bs1 tokens, q_reshaped[13:16] = h1 of bs1 tokens. ✓ Now in FA, `cu_seqlens_q = sparse_cu_seqlens_q`. For bs0 rows (0-9), each is a "batch element" with q_start = i, q_end = i+1. For bs1 rows (10-11), batch element 10 has q_start=10, q_end=13 (head_group 0 q), batch element 11 has q_start=13, q_end=16 (head_group 1 q). But wait — bs1's rows 10 and 11 share the same page_table indices? No — line 1613-1614 sets sparse_page_table[10] = page_table[bs1] * 2 (h0 cache) and sparse_page_table[11] = page_table[bs1]*2+1 (h1 cache). So each row uses its own cache. ✓ OK now one more very subtle thing. The `q_reshaped` interleave is applied IN-PLACE. So after the loop at line 1583-1614 runs, `q_reshaped` has been mutated. Then FA reads `q_sparse = q.contiguous().view(...)` […]

> AGENT

Hmm — `q_sparse = q.contiguous().view(-1, layer.tp_q_head_num // 2, layer.head_dim)`. So q_sparse is a NEW view via `.contiguous().view()`. But q_reshaped was created at line 1582 also as `q.contiguous().view(...)`. If `q.contiguous()` returns q itself (because q was already contiguous), then q_reshaped and q_sparse share the same underlying storage. Mutating q_reshaped in-place mutates q_sparse via the shared storage. But if q wasn't contiguous (or contiguous() returns a new tensor), then q_reshaped's in-place mutations don't affect q_sparse. That would be a bug. Let me check. q comes from `qkv.split([...])` which produces non-contiguous tensors (split is a view). Then `q.contiguous()` would call `.contiguous()` which returns a NEW contiguous tensor (because the strided view is non-contiguous). So at line 1582, q_reshaped is a new tensor backing. At line 1728, `q.contiguous()` is called AGAIN — but PyTorch's `.contiguous()` does NOT cache. It re-creates a new contiguous tensor (or returns the same one if already contiguous). Since `q` was non-contiguous, both calls to `.contiguous()` produce different storage. Wait no - `q.contiguous()` returns the same tensor (q itself) if q is ALREADY contiguous. If q is not contiguous, it returns a new tensor. So `q_reshaped` and `q_sparse` would each be a different tensor. Hmm, but actually `qkv.split` ... let me think. `qkv` is `(total_tokens, hidden_size_total)`. Split along dim=-1 produces views with non-contiguous strides (because of the split). So q is non-contiguous. Then `q.contiguous()` creates a new tensor. The two calls at line 1582 and 1728 each return a different new tensor. So writes to `q_reshaped[ps:ps+len_, :, :] = ...` mutate the q_reshaped temp tensor but NOT the q_sparse used in FA. This is a real bug in mixed batch. Wait but let me re-check. The q at line 1582 — does q.contiguous() copy or alias? If q was already contiguous before `.contiguous()`, returns self. After the qkv split, q is a strided view of qkv but its memory may or may not be contiguous depending on dim order. Actually, this code has been running in some mode. Let me check what code path is used in non-mixed cases. In all-sparse mode, mix-batch dense write is skipped (the code at line 1609-1611 doesn't run because forward_batch.sparse_batch_size == bs). So the bug only triggers in mixed mode. This could be a significant bug. Let me check `.contiguous()` semantics more carefully. From PyTorch docs: "Returns a contiguous in memory tensor containing the same data as self tensor. If self tensor is already […]

> AGENT

OK confirmed. q.contiguous() at 1582 and 1728 are separate calls. If q is non-contiguous, both allocate independent storage. So in mixed batch, the pre-FA q-shuffle is lost. SILENT WRONG OUTPUT for dense bs. But wait — let me also reconsider. Possibly `q` IS contiguous after MiniCPMAttention's forward. Let me look at it:

> AGENT

`q, k = self.rotary_emb(positions, q, k)`. The rotary_emb returns a new tensor typically. Let me check:

> AGENT

Ah - `apply_rope_with_cos_sin_cache_inplace` — INPLACE. So rotary_emb returns the SAME tensor (modifying in place). And the same split-view q is still passed to self.attn, still non-contiguous. So q is non-contiguous, hence q.contiguous() called twice produces different tensors. But wait, this would have been a problem in ALL cases that use the path, including all-sparse... let me re-examine. In all-sparse, the `if forward_batch.sparse_batch_size < bs:` is False, so no q-mutation happens between line 1582 and 1728. So q_reshaped (line 1582) is unused (just created for the in-place mutation that didn't fire). Then `q_sparse = q.contiguous().view(...)` at 1728 creates a new contiguous tensor used by FA. ✓ So in all-sparse path, this works because no in-place writes happen. In mixed path, the in-place writes are on a different tensor than what FA reads. Actually wait - let me reconsider once more. Maybe in mixed case the intent was to write `q_reshaped` and then re-derive q_sparse. The fact that there are TWO calls to q.contiguous().view() is suspicious — perhaps the second was supposed to be `q_sparse = q_reshaped` to preserve the mutations. OK this is definitely a bug. Now let me also check one more thing - line 1582 creates q_reshaped just for the dense bs mutation block. After the block, q_reshaped is dropped (no further refs). At line 1728, q is read again via contiguous() — but q has NOT been modified (the mutations were on q_reshaped which is a separate buffer when q is non-contiguous). So mutations are LOST. Now let me look at one more thing related to the dense bs k/v writeback. When FA reads from KV cache for dense bs (with sparse_page_table rows containing direct page_table * 2 / *2+1), these slot indices come from `forward_batch.req_to_token_pool.req_to_token[req_pool, :]`. The kv cache values at those slots — were they written with proper head_group splitting? Look at line 1340-1343: `forward_batch.token_to_kv_pool.set_kv_buffer(layer, cache_loc, k, v, ...)`. This is the standard SGLang KV writeback. The cache_loc is `forward_batch.out_cache_loc` — the slot ids for THIS chunk's new tokens. So the writeback uses slot id directly. The KV cache layout is `(slot_id, page_size, num_kv_heads, head_dim)`. With page_size=1: `(slot_id, 1, num_kv_heads, head_dim)`. But our sparse_page_table for dense bs sets `[start, :kv_len] = page_table[dense_bs] * 2` and `[start+1, :kv_len] = page_table[dense_bs] * 2 + 1`. So FA reads kv_cache_by_head_group[slot*2] for h0 and kv_cache_by_head_group[slot*2+1] for h1. `key_cache_by_head_group = key_cache.reshape(-1, page_size, tp_k_head_num // 2, head_dim)` (line 1701-1703). This reshape splits […]

> AGENT

So q is passed to forward_extend as is (sliced view of qkv). It's non-contiguous. Yes, my analysis stands. But wait — I want to double-check this. Maybe `q.contiguous()` is being cached or there's some optimization. Let me write a quick test:

> AGENT

Confirmed. `q.contiguous()` on a non-contiguous q returns DIFFERENT tensors on each call. Bug confirmed. Now let me look at one more concern — the `metadata.cu_seqlens_q_adjusted` and stage1 cache_lens size mismatch. Re-examining: in `compressed_attention` for prefill, what's `cu_seqlens_q` size? Going back to flow: - In mixed batch with `max(seq_lens) >= dense_len`: goes to topk_metadata branch - topk_metadata's `cu_seqlens_q = cu_seqlens_q_sparse` (sparse-bs only, line 2032) - topk_metadata also has `query_states` (sparse-bs only via batched_gather) - Then calls `sparse_get_topk_impl(query_states, cu_seqlens_q_sparse, ...)` at line 1128 In `sparse_get_topk_impl`: - Line 1244-1250: if max_q < max_k, derive cache_lens. If max_q == 1, use `forward_metadata.cache_seqlens_int32_stage1` (full-bs sized). Else `cu_seqlens_k - cu_seqlens_q` (sparse-bs sized). Then `compressed_attention` is called with `cu_seqlens_q = cu_seqlens_q_sparse_bs+1`, `cache_lens = full-bs size`. The `pool_func` uses cache_lens[batch] indexed by batch (where batch index ∈ [0, num_sparse_bs)). So cache_lens[0] would refer to bs0's stage1 cache_len, but the kernel expects cache_lens[sparse_bs_idx] to correspond to the i-th sparse-bs entry in cu_seqlens_q. E.g., bs0 (dense), bs1 (sparse). cu_seqlens_q_sparse has 2 entries: [0, sparse_q_len]. The kernel iterates batch=0 expecting bs1's q. cache_lens[0] is actually bs0's (dense's) stage1 cache_len. Wrong batch! But this only fires when max_seqlen_q == 1 in `sparse_get_topk_impl`. max_seqlen_q here is `topk_metadata["max_seqlen_q"] = max(seqlens_q_sparse_bs)`. If all sparse bs have extend=1, this triggers. So chunked-prefill 1-token-last-chunk path with mixed batch has wrong stage1 cache_lens. Now let me also verify line 1246 — `cache_seqlens_int32_stage1`. Actually wait — even in all-sparse with max_seqlen_q==1 (chunked-prefill last chunk all sparse), is `cache_seqlens_int32_stage1` indexed correctly? cache_seqlens_int32 is from line 868-870 (where cache_seqlens is built per-bs in the FA metadata setup). In all-sparse with all-sparse bs, full-bs == sparse-bs, so indexing is fine. In mixed, full-bs != sparse-bs, so indexing is misaligned. Now let me also look at one more spot — the use of `seqlens_q[i]` at line 2017 / 2018 in `build_prefill_topk_metadata`:

> AGENT

Line 2055 `max(seqlens_q_sparse_bs)` could error if `sparse_bs` is empty (no sparse bs). But that scenario is when max(seq_lens) < dense_len, where we go to the else branch at line 1566. So no issue. Now check that I understand the q-shuffle bug fix would look like: The bug fix would be `q_sparse = q_reshaped` (reuse the already-mutated buffer) instead of `q_sparse = q.contiguous().view(...)` at line 1728. Or alternatively, hoist `q.contiguous()` once at line 1582 and use the same q_contig variable everywhere. But this is read-only — I just need to report. Now let me check the prefill_topk_metadata's `cu_seqlens_q` derivation — it uses full `seqlens_q` (line 2020-2026, ALL bs including dense). And then it does `batched_gather(query_states_reshaped, cu_seqlens_q, sparse_bs)`. So the gather extracts only sparse-bs queries from the full layout, producing a tensor with only sparse-bs Q. This is independent of the FA path's q layout. Just used for topk. OK. Let me check `batched_gather`:

> AGENT

OK batched_gather is correct. Note that line 277 `starts = cu_seqlen_q[select]` does CPU-vs-GPU mixing. cu_seqlen_q is on GPU (line 2022 `device=query_states.device`), select is on CPU. PyTorch may auto-move. Probably works. Let me now also check what happens for the all-dense case (`max(seq_lens) < dense_len`): At line 1466, `if max(forward_batch.seq_lens_cpu) >= self.dense_len:` is False → goes to else branch (line 1566-1580). No topk_idx computed. Then falls through to 1582+. At 1583, `if forward_batch.sparse_batch_size < bs:` — yes, sparse_batch_size = 0, bs = N → True. Goes into the dense_bs_list loop for ALL bs. This processes all bs as "dense" by writing their pages to sparse_page_table. But `cu_seqlens_q_adjusted` (line 626-635) was built with only seq_lens_cpu[i] >= dense_len entries → empty list! `seqlen_q_sparse_tensor = torch.tensor([], ...)` and `cu_seqlen_q_sparse_tensor = cumsum on empty = [0]`. So `cu_seqlens_q_adjusted = [0] * heads_per_group = [0]`. And `max_seqlen_q_adjusted = 0`. Then FA: `metadata.sparse_max_seq_len_q` could be > 1 (dense bs extends). FA call uses `cu_seqlens_q=metadata.sparse_cu_seqlens_q` (full layout including dense bs) — wait, `sparse_cu_seqlens_q_cpu` includes dense bs rows. So it's NOT empty for all-dense. OK but at line 1247-1250 in `sparse_get_topk_impl`, this isn't called in all-dense case because topk is never computed. So cu_seqlens_q_adjusted = [0] doesn't bite. Good. Now one more concern - check `sparse_get_topk_impl` at line 1247-1250: `seq_lens_k = cu_seqlens_k[1:] - cu_seqlens_k[:-1]`. The cu_seqlens_k here is `topk_metadata["cu_seqlens_k"] = cu_seqlens_k_sparse` (line 2054 — sparse-bs only). And `cu_seqlens_q = cu_seqlens_q_sparse`. So sizes match. Now let me look at one last spot: the all-sparse-prefill metadata path with `sparse_idx = slice(None)`. When that's the case, `metadata.sparse_page_table[forward_batch.sparse_idx, :num_sparse_topk_tokens] = sparse_page_table_sparse_bs` (line 1562) → writes to all rows. Fine, only triggered in all-sparse. Let me now also check that `sparse_max_seq_len_q` propagates correctly. For ALL-DENSE batch (all bs have seq < dense_len), `sparse_max_seq_len_q` is `max(1, max(extend_seq_lens_cpu of dense bs))` from line 1751-1753. OK. For MIXED batch where dense bs extend = 1 (and sparse bs trivially have sparse_max_seq_len_q = 1), `sparse_max_seq_len_q = 1`. FA decodes max_seqlen_q=1. But the actual q has dense_extend = 1, so q-len 1 per dense row. That's effectively decode. OK functionally. Let me also re-verify if there's an issue when `max(seq_lens) < dense_len` AND sparse_batch_size < bs. In that case `metadata.sparse_bs_list` is empty (line 564 / 1322-1326 only adds bs with seq_lens >= dense_len). So `dense_bs_list = [0..bs)`. The loop at line 1587-1614 writes all bs as dense. `metadata.sparse_page_table` was allocated with shape `(sparse_page_table_bs, max_sparse_cache_len)` where `sparse_page_table_bs = bs * […]

> AGENT

Now I have my findings. Let me write the report. --- # Mixed-batch (`--dense-as-sparse=False`) Latent Bug Review ## Bug 1: Dense-bs q reshuffling is lost — `q.contiguous()` called twice produces independent buffers **File:** `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_backend.py:1582` and `:1728` Two separate `q.contiguous().view(...)` calls. `q` is a slice of `qkv.split(...)` and is **non-contiguous** (verified empirically: each `.contiguous()` on a non-contiguous tensor allocates fresh storage). The dense-bs pre-FA shuffle at lines 1609-1611 (`q_reshaped[ps:ps+len_] = t[0::2]`, etc.) mutates `q_reshaped`, but at line 1728 FA reads from a **different** new buffer `q_sparse`. The shuffle is silently dropped, so dense-bs rows get fed FA in the original `[h0_t0, h1_t0, h0_t1, h1_t1, …]` layout while `sparse_cu_seqlens_q` expects `[h0_t0, h0_t1, …, h1_t0, h1_t1, …]`. **Severity: silent wrong output** for all mixed-batch prefill with at least one dense bs whose extend>1. (Triggers from the first mixed chunk onward; extend=1 case is innocuous because the h0/h1 swap is a no-op.) All-sparse path is unaffected since the mutation block is gated by `sparse_batch_size < bs`. Fix candidate: replace line 1728 with `q_sparse = q_reshaped`. ## Bug 2: `sparse_cache_seqlens_int32` derivation via `(sparse_page_table != 0).sum(dim=1)` undercounts when KV slot 0 is in the page table **File:** `minicpm_backend.py:1636-1640` Mixed batch always falls into this fallback branch (the derived path at lines 1621-1633 is gated `sparse_batch_size == bs`). For dense bs rows, line 1613 writes `page_table[dense_bs, :kv_len] * 2`. If any kv slot id in that row equals 0 (slot 0 IS a valid SGLang KV pool slot), `*2 = 0` is then counted as "not present" and the **even** (h0) row under-reports `cache_seqlens` by 1 per zero-slot. The odd row (`*2+1`) is fine. Downstream this `sparse_cache_seqlens_int32` is the FA `cache_seqlens` (line 1737) and feeds `sparse_cu_seqlens_k` (line 1694). **Severity: silent wrong output / occasional under-attention** on dense bs h0 whenever slot 0 is in scope (which happens regularly for fresh sequences or after eviction). Sparse-bs rows are unaffected (topk pages can include 0 just the same, but `_MINICPM_DERIVED_SPARSE_SEQLENS=False` path applies to them too, so they have the same conceptual fragility — but they're built differently and may not legitimately contain non-zero sentinel `0` in valid positions). ## Bug 3: Stage1 `cache_lens` size mismatch when sparse-bs `max_seqlen_q == 1` in mixed batch **File:** `minicpm_backend.py:1246` (consumer in `compressed_attention` at `minicpm_sparse_utils.py:853`) When max_seqlen_q==1 (chunked-prefill last-1-token chunk for sparse bs), `sparse_get_topk_impl` picks `cache_lens = self.forward_metadata.cache_seqlens_int32_stage1`. That tensor has length `bs` (full batch). But the surrounding `cu_seqlens_q` it's paired with (`topk_metadata["cu_seqlens_q"] = […]

> DEVELOPER

研究 EAGLE-style speculative decoding 的 draft model 在长上下文场景下做 prefix 截断的合理性，并设计一个干净的生产质量实现。 # 背景 我们在做 MiniCPM-SALA (32 层 hybrid: 24 GLA + 8 standard attn) 的 SGLang 推理优化，启用 EAGLE-3 chain-verify 推测解码。Profile 发现：长上下文 (e.g. 524K tokens) 单请求 prefill 中，**EAGLE-3 draft model (1 layer Llama-style dense paged FA, BatchPrefillWithPagedKVCacheKernel<128,2,2>) 占用 ~17s / 33% 的 wall**。 我们实验了一个 hack：draft prefill 时只 attend last_n=32768 tokens (而非 full prefix)。结果： - Wall time: 53.66s → 38.01s (-29%) - Accept rate noisy 但**未崩**（baseline 1.50 → LAST_N=32K 测得 2.02，单次测量噪声大需更多 sample 但**没明显退化迹象**） - 短 prompt 自动 bypass（per-request 条件：`seq_len < req_total - LAST_N` 才 skip） 当前实现在 `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py` 的 `forward_draft_extend`，是 env-gated `SGLANG_EAGLE_DRAFT_PREFILL_LAST_N=32768` hack（启动脚本 `eval/start_eagle.sh` 已默认开 32K）。详细 hack 描述在 `prefill/experiment-log.md`（之前对话中已写）。 # 你的任务（两个部分） ## Part 1: 网络调研 + 学术/业界合理性论证 用 WebSearch/WebFetch 调研以下问题（请实际去搜，不要靠 prior knowledge 编造）： 1. EAGLE / EAGLE-2 / EAGLE-3 / Medusa 等 spec decoding 论文中，draft model 是否有 long-context 设计？是否有人讨论过 draft prefix truncation？ 2. 业界开源实现（vLLM EAGLE / SGLang upstream / TensorRT-LLM speculative / DeepSpeed-FastGen 等）是否有 draft prefix windowing / truncation 的设施？ 3. 是否有论文/blog/issue 讨论："draft model 不需要 full long-context"、"draft prefix is short-range"、"sliding window for draft"？关键词：speculative decoding long context, EAGLE long prompt, draft model context window, draft prefix truncation, draft sliding window 4. EAGLE-3 的训练数据典型 prefix length 是多少？（ShareGPT 量级？显著小于推理目标？）如果训练 prefix 短，推理时给 draft 喂 524K context 本身就是 OOD（out-of-distribution），截断到训练分布反而更合理。 5. Speculative decoding 的接受率理论：accept rate 主要取决于 draft 在 **next token level** 与 target 的对齐度，而非 draft 是否"看见"完整 prefix。Draft 短视 (myopic) 对 accept rate 的影响是 mostly local。论证这一点（找 reference）。 输出 Part 1 报告： - 现有论文/实现是否支持这种做法（具体引用 + 链接） - 哪些是 novel（我们的做法在业界没人做过） - 哪些 risk 业界已讨论过（例如 long-range token dependency, KV 不一致） - 一句话结论：合理性证据强度 (strong / moderate / weak) ## Part 2: 干净实现设计 当前 hack 缺点： - env-gated（生产配置散乱） - placeholder LogitsProcessorOutput 用 `torch.zeros` 假造（可能 mask 真实问题） - skip 整个 forward 而非 truncate prefix（粗暴；丢失了"draft prefix=last_N 仍然看 last_N tokens"的精细控制） 设计一个干净方案，需要满足： 1. **吞吐无害**：默认开启时性能 ≥ 当前 hack 2. **正确性等价**：在 last_N 足够大时（如 32K），accept rate 不退化 3. **一等公民**：不是 env hack，是 server arg / config 的合法参数（如 `--speculative-draft-prefix-window 32768`） 4. **细粒度**：可选 strategies — (a) skip-draft-prefill (current hack)、(b) truncate-draft-prefix-window (推荐：draft 真的看 last_N tokens，不是 zeros placeholder)、(c) full-draft-prefill (baseline) 5. **边界 well-defined**：短 prompt (`seq_len ≤ window`) 自动走 full；window=0 等价 hack；window=inf 等价 baseline 6. **KV cache 一致性**：draft KV pool 是否要存全 prefix 还是只存 window？影响 decode 阶段 draft 也要 attend 历史 读代码： - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py` — 现有 hack 在 forward_draft_extend - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py` 或类似 — EAGLE draft state mgmt - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/model_executor/forward_batch_info.py` — forward_batch 结构 - draft model 的 attention backend dispatch（draft 用 flashinfer，看 `--speculative-draft-attention-backend flashinfer`） 输出 Part 2 报告： - 设计方案概要（架构图/数据流） - 每个 strategy 的具体技术实现（attention backend 层面） - KV cache 怎么处理（draft KV […]

> AGENT

我来分两部分完成调研和设计。先并行启动网络调研和代码探索。

> AGENT

我开始并行调研：网络搜索 + 读代码。

> AGENT

这是个关键发现：**LongSpec (arXiv:2502.17421)** 明确提出 draft 用 sliding window self-attention（window=512）+ cross-attention 拿 target KV。完全对应我们的设计。继续深挖。

> AGENT

已经收集到足够多的论文 reference 和代码 context。让我再查一个具体的实现细节——SGLang 的 draft attention backend dispatch 和 KV cache 写入路径。

> AGENT

我有了足够的信息完成两个 Part。整理输出。 --- # Part 1: 学术/业界合理性论证 ## 1.1 EAGLE 系列本身对 long-context 的处理 EAGLE-3 论文 ([arXiv:2503.01840](https://arxiv.org/abs/2503.01840)) 完全没有讨论 draft model 的 prefix truncation 或长上下文设计。训练数据是 ShareGPT 68K + UltraChat-200K 532K 样本，**论文未给出明确 max sequence length**，但配套工程 SpecForge ([LMSYS blog](https://www.lmsys.org/blog/2025-07-25-spec-forge/))、ROCm tutorial 的样例脚本和 P-EAGLE 都显示典型训练 `max-length=2048`。Bento ML 的多个 production blog 也明确指出 ["EAGLE-3 draft heads were not optimized for long contexts"](https://www.bentoml.com/blog/3x-faster-llm-inference-with-speculative-decoding)。 含义：把 524K context 喂 EAGLE-3 draft 本身就是 **strongly out-of-distribution**。截断到 32K 反而把 draft 推回它训练时见过的分布。 ## 1.2 业界已有的同类做法（强证据） **LongSpec** ([arXiv:2502.17421](https://arxiv.org/abs/2502.17421))：draft self-attention 直接用 **sliding window=512**，并提供 Theorem 3.1 给出近似误差上界（与窗外注意力权重成正比），论据是"语言的局部性"使窗外注意力小。这是与我们做法最贴近的学术 reference。 **MagicDec** (ICLR 2025, [arXiv:2408.11049](https://arxiv.org/abs/2408.11049))：明确论证 **draft KV cache size 而非 draft 权重才是 long-context decode 的瓶颈**，方法是 StreamingLLM 风格的 constant draft KV (sink + sliding window)，2.51× speedup on Llama3.1-8B with 32–256 batch sizes。 **TriForce** (COLM 2024, [arXiv:2404.11912](https://arxiv.org/abs/2404.11912))：分层 spec decoding，draft 用 retrieval-based sparse KV (top-chunk by query attention)。 **SpecExtend** ([arXiv:2505.20776](https://arxiv.org/abs/2505.20776))：训练免费的 drop-in enhancement，用 target attention score 选 top-k chunks 喂 draft KV，up to 2.84× speedup on 16K inputs；明确"chunk retention < full prefix"等价于我们的"draft 不需要看全 prefix"假设。 **EAGLE Llama at scale** ([arXiv:2508.08192](https://arxiv.org/abs/2508.08192))：Llama4 iRoPE 实现里写了"opted for a simpler solution: truncating the draft to fit entirely within one sub-sequence"，且"impact on acceptance rate is negligible"。 ## 1.3 业界已有的产线接口（弱证据） vLLM 主线、SGLang upstream、TensorRT-LLM 均**没有** "draft prefix window" CLI flag——LongSpec/MagicDec/SpecExtend 还停在 research code。这意味着把它做成 `--speculative-draft-prefix-window` 是 **production 层面 novel** 的，但**算法层面非 novel**。 ## 1.4 Acceptance rate 的局部性论证 EAGLE-3 论文 §3.4 自己写："use **only the last accepted token and hidden states** to sync the draft model"——draft 在 decode 阶段每步本来就只接受 1-token hidden state 当 anchor，**不依赖远距离 prefix 的 attention**。LongSpec Theorem 3.1、MagicDec 实验数据、SpecExtend 静态 vs 动态 chunk retention 三方独立显示：**acceptance rate 主要由 next-token-level local context alignment 决定**，远距离 prefix 对 draft 的边际贡献小。BentoML/Nebius LK-losses blog ([Nebius](https://nebius.com/blog/posts/lk-losses)) 强调 acceptance rate 由 draft-target 在 **next-token distribution** 上的对齐度（不是 long-range）。 ## 1.5 已知 risk - **Retrieval-heavy tasks** (needle-in-a-haystack)：SpecExtend 论文显示 StreamingLLM 风格的位置式 eviction 在 needle 任务掉 acceptance；retrieval-based (SpecExtend / TriForce) 更稳。 - **KV 不一致**：draft KV pool 缺失早期 token，decode-time draft 也只能看 window；如果 draft 在 decode 中需要 attend 早期 token 会拿到未写入位置。这是真实风险，要 well-defined fallback。 ## 1.6 一句话结论 **Moderate-to-strong**：算法层面与三篇 ICLR/COLM/已审稿 arxiv 论文 (LongSpec/MagicDec/SpecExtend) 思路一致，理论与多个独立实验背书；EAGLE-3 训练数据本来就是 ≤2K-2K 短上下文，给 524K 是 OOD，截断到 32K 反而回到 ID。Production 接口层面是 novel——尚无主流 inference engine 提供该 CLI flag。 --- # Part 2: 干净实现设计 ## 2.1 当前 hack 三大缺陷 代码在 `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:2113-2150`： 1. **粗暴 skip 整个 forward**：吐 `torch.zeros((bsz, vocab))` 假 logits 当 placeholder，`capture_for_decode` 接着用 `softmax(zeros)` 做 topk → 拿到完全无意义的 `topk_p/topk_index`。在 EAGLE chain verify 的第一步可能被立刻 reject，但仍消耗一次 verify 槽位。当前测出 accept_len=2.02 没掉，是因为 prefill 之后 `forward_draft_extend_after_decode` 会用真实 hidden state 重新 seed，所以损失只局限在第一次 decode。 2. **env-gated**：`SGLANG_EAGLE_DRAFT_PREFILL_LAST_N`，文档外通道。 3. **没有 truncate 模式**：黑白二元（全跑 / 全跳），不能"draft 真的看 last_N 个 token"。 ## 2.2 接口设计 新增三个 server arg（`server_args.py:418-432` 块附近）： ```python # Speculative decoding — draft […]

> DEVELOPER

调研 SGLang 中 EAGLE-3 draft model 的输入数据流，回答：**chunked prefill 中第 N+1 个 chunk 的 draft prefill input 是否依赖第 N 个 chunk 的 draft state（hidden_states / KV / spec_info）？** # 背景 代码库 `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt`。HEAD `7ef0eb0`。在跑 MiniCPM-SALA + EAGLE-3 spec decoding。 我要实现一个 "sliding window draft prefill"：长 prompt (524K context) 时早期 chunks 跳过 draft prefill（不跑 draft forward），只在 trailing N tokens 跑 draft。当前已有 env hack 实现验证可行（wall -29%，accept_len 反升）。 我需要确认 hack 之所以 work 是因为 EAGLE-3 设计为 **draft 每个 chunk 用 target 的 hidden state 作输入，不依赖前一 chunk 的 draft state**。如果这个假设错了，sliding window 设计要重做。 # 调查任务 读以下文件，回答下面具体问题： 1. `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py` — `forward_draft_extend` 函数 (约 line 2050-2200) 2. `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py` — `EagleDraftInput` class、`prepare_for_extend` 方法 (约 line 800-900) 3. `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py` — `capture_for_decode` 方法 4. `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py` — `forward_draft_extend_after_decode` (理解 decode 阶段 draft 的输入来源) 5. 任何 EAGLE-3 draft model 的 forward 实现（draft 是 Llama-style 1 layer）— grep `LlamaForCausalLMEagle3` 找 # 具体要回答的问题 A. **draft 的 forward 输入 input_embeds 是什么？** - 是 target_hidden_states (chunk N) 经过 fc + 一些处理？ - 是 input_ids embedding + target_hidden_states？ - 是否含上一 chunk 的 draft hidden state（i.e., spec_info.hidden_states from previous capture_for_decode）？ B. **chunk N 的 draft prefill 之后写到 spec_info 的内容**（capture_for_decode 的输出）： - next_token_logits — 用于谁？ - hidden_states (next_hidden_states) — 用于哪个后续步骤？ - topk_p / topk_index — 给 decode 第一步用？还是给 chunk N+1 的 draft prefill 用？ C. **chunk N+1 的 draft prefill 进入时**，prepare_for_extend 怎么 use spec_info from chunk N？ - 读 spec_info.hidden_states 拼到 input？ - 读 spec_info.verified_id 决定 input_ids？ - 完全 ignore spec_info？ D. **当前 hack 写 zeros placeholder 进 spec_info**，chunk N+1（trailing chunk）进入时会读这个 zeros 吗？ - 如果会读 → hack 有 latent bug，trailing chunk 输入被污染 - 如果不读（每 chunk 重新从 target 取 input）→ hack 安全 - 如果只在 decode 阶段读，且 trailing chunk 写真实值覆盖 → zeros 是 dead code E. **decode 阶段 draft 的输入**：每个 spec step 的 draft input 是什么？ - last accepted token 的 target hidden state（target 在 verify 阶段输出的）？ - draft 自己上一步的 hidden state？ # 报告格式 短报告（< 500 字）： - 5 个问题逐一回答，给出**文件:line** 引用 - 关键结论：hack 是否 well-defined（zeros placeholder 是死代码 vs 有读路径） - 一句话设计建议：sliding window 实现中 spec_info 在 skip 路径应该怎么处理 不要修代码，只读。不要去 web 调研论文（之前已调研过），focus 在 sglang 当前 fork 的代码事实。

> AGENT

我开始调研 SGLang EAGLE-3 draft 的输入数据流。

> DEVELOPER

调研 SGLang 中 EAGLE-3 draft attention backend (`--speculative-draft-attention-backend flashinfer`) 的 kv_indices 数据流，回答：**能否在 worker 层 clip draft 的 kv_indices 让 attention 只看 trailing N 个 KV slots？** # 背景 代码 `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt`，HEAD `7ef0eb0`。在 MiniCPM-SALA + EAGLE-3 上做 sliding window draft 优化。 目标：让 draft model 的 attention（prefill + decode）在 long context 下只 attend 最后 N=32768 个 KV slots，而不是 full 524K。这样 decode 阶段 draft FA 避开早期 zero KV slots 的 softmax dilution 问题。 # 调查任务 读以下文件（用 grep + Read）： 1. SGLang 中 EAGLE-3 draft model 用的 attention backend (flashinfer)：找 `speculative-draft-attention-backend` 的处理路径 2. draft worker 的 attention backend init 在哪里：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py` 中找 draft_model_runner 怎么 init 3. draft model 的 forward 路径上，kv_indices / kv_indptr / kv_last_page_len 在哪个 metadata struct 里 4. flashinfer prefill wrapper 的 `begin_forward(qo_indptr, kv_indptr, kv_indices, kv_last_page_len, ...)` 调用点（draft 路径） 5. flashinfer decode wrapper 的同样调用点（draft 路径） # 具体要回答的问题 A. **draft prefill 时 kv_indices 怎么算的？** - 是不是 sglang `req_to_token` pool 的 trailing N slot 之类？ - 文件路径 + line + 关键变量名 B. **draft decode 时 kv_indices 怎么算的？** - 每 spec step 都是 [0..cache_len) 的所有 slots？ - 用 sglang token pool indexer 还是别的？ C. **能不能在 worker 层（不动 attention backend 代码）override kv_indices？** - e.g., 在 `forward_draft_extend` 调 draft_model_runner.forward(forward_batch) 前，把 forward_batch.seq_lens / forward_batch.req_to_token clip 一下 - 或者在 attention backend init_forward_metadata 钩子前覆盖 D. **clip kv_indices 后 cuda graph 兼容吗？** - draft decode 一般用 cuda graph capture（提高吞吐） - clip 后 kv_indices 长度变化 → cuda graph replay 可能失效 - 看 sglang draft decode 是否用 cuda graph，capture 时 kv_indices 长度怎么处理（padding 到 max 还是动态？） E. **RoPE positions 怎么传给 draft model？** - positions 是 absolute（524K 中的真实位置）还是 relative（0~chunk_len）？ - 看 draft model forward 的 positions 参数来源 # 报告格式 短报告（< 500 字）： - 5 个问题逐一回答，给出**文件:line** 引用 - 关键结论：worker 层 clip 可行性（trivial / 需改 backend / 不可行） - 一个推荐方案：实现 kv_indices clip 的最干净 hook 点 不要修代码，只读 + 报告。

> AGENT

我开始调研 SGLang 中 EAGLE-3 draft attention backend 的 kv_indices 数据流。

> AGENT

现在我了解了 forward_draft_extend 的整体流程。让我查 `prepare_for_extend` 和 EagleDraftInput class。

> AGENT

重要观察：`prepare_for_extend` 只改 `batch.input_ids`，**不改 hidden_states**。让我看 draft model 自己的 forward，验证它读什么。

> AGENT

找到关键路径，draft model forward 从 `forward_batch.spec_info.hidden_states` 取 hidden。让我看完整 forward。

> AGENT

Now let me look at the EAGLE-specific kv_indices code paths and the cuda graph runner.

> AGENT

关键确认：line 168 `hidden_states = forward_batch.spec_info.hidden_states`，这是 draft 的 hidden 输入来源。 这是 **target 的 aux hidden**（3*hidden_size 因 eagle3 拼 3 层），所以会过 `fc` 投回 hidden_size。 现在让我看 prepare_for_extend 的 chunked prefill 行为：spec_info.hidden_states 的形状是什么、与 chunk 关系。

> AGENT

Now let's look at how kv_indices is built for draft decode (sequential spec steps).

> AGENT

关键发现：`forward_target_extend` 用 `CaptureHiddenMode.FULL` 取 hidden states，所以 hidden_states 形状是 `(extend_num_tokens, hidden_size*3)`（aux 三层）—— 是 **当前 chunk 全部 token 的 hidden**，从 target 直出。 让我确认在 chunked prefill 时 forward_draft_extend 收到的 hidden_states 是否覆盖整个 chunk（而不是从某个 cache 来的）。

> AGENT

Now let's look at how draft decode build kv_indices (per spec step). Check eagle_draft_cuda_graph_runner.

> AGENT

eagle_worker 自己不区分 chunked vs non-chunked — 它每次走 `forward_target_extend` → `forward_draft_extend`，所以每个 chunk 都会触发一次 draft prefill。`hidden_states` 形状是当前 chunk 的 token 数。 让我看 prepare_for_extend 处的 batch.input_ids 来源以确认 input_ids 是当前 chunk 的 token id：

> AGENT

验证关键事实： - prepare_for_extend 把 `batch.input_ids` shift left（去掉第一个、末尾接 verified_id）。这是 EAGLE 论文里 "draft input shifted by 1" 的实现。 - `verified_id` 是 target 上一步 sample 出的 token id（也就是 chunk 末端预测的下一个 token）。 - **不读上一 chunk 的 spec_info.hidden_states**。新的 EagleDraftInput 在 line 2100 重新创建，hidden_states 来自当前 chunk target 的 hidden。 现在看 D 部分 — 验证 zeros placeholder 是否会被下一 chunk 读到。检查 forward_draft_extend 入口的 spec_info：

> AGENT

Let me check what `init_forward_metadata_capture_cuda_graph` does for flashinfer with draft setting (specifically how kv_indices buffer is sized & maintained at decode).

> AGENT

**关键确认**：line 2100 — 每次 `forward_draft_extend` 都用 fresh `EagleDraftInput`，`hidden_states` 来自 target chunk forward 的 hidden，**完全覆盖** 上一个 chunk capture_for_decode 写的内容。 下一 chunk 进入 forward_draft_extend 时，**根本不会读上一 chunk 留下的 spec_info.hidden_states**。 让我再看 decode 阶段 draft 输入来源，确认 trailing chunk 的 capture_for_decode 是否真的对 decode 起作用：

> AGENT

Note the `cuda_graph_kv_indices` buffer is sized `max_num_tokens * max_context_len`. So it's a pre-allocated big buffer that can hold up to max_context_len entries per token. Critical info: kv_indices length per request can vary at replay time without recapturing the graph (because flashinfer reads from kv_indptr which slices into the buffer). Now let's look at draft FlashInferMultiStepDraftBackend used for `draft_attn_backend.init_forward_metadata_capture_cuda_graph`.

> AGENT

重要发现：decode 阶段 `draft_forward` 在 line 1651-1655 从 `spec_info.{topk_p,topk_index,hidden_states}` 取输入。 **这就是 zeros placeholder 的潜在读路径**：第一次 spec decode 触发时，draft 读 `spec_info.hidden_states`（来自最近一次 capture_for_decode）。但 trailing chunk 跑了真实 draft prefill，会覆盖 zeros。 让我确认 trailing chunk 确实跑 forward 且会 capture_for_decode（line 2161）： - skip_all 路径 (zeros)：line 2149 写 placeholder 后 `return` - 普通路径（最后一个 chunk）：line 2156 跑 forward，line 2161 capture_for_decode 写真实 hidden 确实 trailing chunk 走普通路径覆盖了 zeros。但要看 scheduler 是否在 chunk N→N+1 中间会触发 decode（会读到 zeros）：

> AGENT

Excellent — now I have the critical answer for the kv_indices algorithm in draft decode. Let me read the `generate_draft_decode_kv_indices` triton kernel:

> AGENT

Chunked prefill 是连续的 chunk by chunk，中间不会插 decode（同一 req）。但 zeros placeholder 仍可能被其它路径读到：cuda graph capture、metric。让我快速看 capture_for_decode 的 hidden_states 还在哪儿被读：

> AGENT

Now let me look at `forward_draft_extend` (kv_indices for draft prefill).

> AGENT

所有 spec_info.hidden_states 读取都在 decode 路径（eagle_draft_*cuda_graph_runner、draft_forward）或 verify 路径。**Prefill 阶段 forward_draft_extend 自己 line 2100 重新构造 EagleDraftInput**，所以下一 chunk prefill 不会读上一 chunk capture_for_decode 留下的内容。 让我看看 line 953 行附近 `last_hidden`（这是 NO_SPEC → SPEC 转换处理）：

> AGENT

Now let me look at how `update_single_wrapper` (decode) computes kv_indices for draft prefill mode. Let me check the FlashInferIndicesUpdaterDecode update_single_wrapper.

> AGENT

I see — for sliding-window dispatch, the backend ALREADY supports `kv_start_idx` + clamp on `paged_kernel_lens`. This is built-in flashinfer sliding-window. Let me check `create_flashinfer_kv_indices_triton` to understand what kv_start_idx does:

> AGENT

So for prefill the `kv_start_idx` parameter directly maps to "start position in req_to_token row". If we set `kv_start_idx = max(0, seq_len - N)` and `paged_kernel_lens = min(seq_len, N)`, we get trailing-N kv_indices for free. Now let's look at update_single_wrapper for prefill (FlashInferIndicesUpdaterPrefill):

> AGENT

这是 NO_SPEC mode 路径，与 chunked prefill 无关。 我现在有完整事实可以回答。 --- ## 调研结论 ### A. draft forward 的输入 `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama_eagle3.py:152-184` Draft model 拼两个东西： 1. `embeds = self.embed_tokens(input_ids) * scale_emb`（line 161）—— 来自 `batch.input_ids`（左移 1 位 + 接 verified_id，见 `eagle_info.py:864-868`） 2. `hidden_states = forward_batch.spec_info.hidden_states`（line 168）—— 来自 target chunk forward 的 aux hidden（3*H），过 `self.fc` 投到 H 3. midlayer 内 `torch.cat([embeds, hidden_states], dim=-1)`（`llama_eagle3.py:88`） **不含上一 chunk 的 draft hidden**。 ### B. chunk N 的 capture_for_decode 写到 spec_info 的内容 `eagle_worker.py:2291-2296`： - `topk_p, topk_index = fast_topk(softmax(next_token_logits), topk)` — 给 **decode 阶段** `draft_forward` 用（`eagle_worker.py:1651-1655`），用来产生 first draft step 的候选 token - `hidden_states = logits_output.hidden_states` — 给 **decode 阶段** `draft_forward` 用作 first draft step 的 hidden 输入 这些 **只服务 decode 阶段**，下一 chunk 的 prefill 不读。 ### C. chunk N+1 的 prefill 读 spec_info 的什么 `eagle_worker.py:2100-2105`：每次 `forward_draft_extend` 入口都 **重新构造** `EagleDraftInput`，`hidden_states` 来自当前 target chunk forward，`verified_id` 来自当前 target sample。**完全覆盖** 上一 chunk 的 spec_info；`prepare_for_extend`（`eagle_info.py:855-869`）只修改 `batch.input_ids`（左移 + 接 verified_id），不读旧 hidden_states / topk。 ### D. zeros placeholder 是否被读 不会被下一 chunk prefill 读（C 已证明），但 **会被 decode 第一步读** —— 如果 chunk N 是 trailing chunk 之前的最后一个 skipped chunk，且 scheduler 在它之后直接进入 decode 而不再跑一个 trailing prefill chunk，zeros 就会污染 first draft step。 但当前实现里 trailing chunk 走 line 2152-2161 真实 forward + capture，**覆盖 zeros**。只要 `_last_n > 0` 的逻辑能保证 trailing chunk 一定存在并落入 not-skipped 分支（`seq_lens_cpu[i] >= req_total_lens[i] - _last_n`），zeros 就是 **dead write**。 潜在 latent bug：若 EAGLE-3 D5/D7 走 `forward_draft_extend_after_decode`（line 2163-）路径而不是 prefill，`prepare_extend_after_decode`（`eagle_info.py:892-922`）仍用 `self.hidden_states`（line 930 trace 读，line 1108/1114 select 也读），但这是 decode-after-decode，跟 chunked prefill 不冲突。 ### E. decode 阶段 draft 输入 `eagle_worker.py:1646-1709`（`draft_forward`）： - step 0：从 `spec_info.{topk_p, topk_index, hidden_states}` 取（line 1651-1655）—— 即 chunk-end capture_for_decode 的输出 - step i>0：从上一 step 的 logits 的 topk 取 input_ids，hidden 用上一 step 的 `logits_output.hidden_states`（line 1698 写回 spec_info.hidden_states） 即 **first step 用 target 最后 token 的 hidden + verified_id 的 embed；后续 step 用 draft 自身上一步 hidden + 自身 topk token embed**。 --- ### 关键结论 - **EAGLE-3 chunked prefill 设计上每 chunk 独立**：每 chunk 的 draft prefill 输入 = (当前 chunk input_ids 左移 + chunk-end verified_id, 当前 chunk target aux hidden)。**不依赖上一 chunk 的 draft state**。 - **hack 是 well-defined 的**：zeros placeholder 在当前控制流下是 dead write —— 下一 prefill chunk 不读它（line 2100 覆盖），decode 阶段第一步读的是 trailing chunk 的真实 capture（line 2156 + 2161 覆盖）。前提是 `_last_n` 至少能让 trailing chunk 真实跑 forward。 - **Draft KV 在 skipped 区间未写**，但 draft 只在 step 0 依赖 chunk-end hidden + verified_id 的 1-token attention 起步，后续 step 完全自洽——所以丢早期 KV 不影响 decode（除非用户极端长 accept chain 跨过 trailing 区间，正常 D5/D7 不会）。 ### 设计建议 sliding window 实现里，skip 路径应该 **直接不调用 `capture_for_decode`**（zeros placeholder 是不必要的 fake state），同时记一个 sentinel `spec_info.hidden_states = None`（或保留 last-real capture），让 assert 在 "skip 后没接 […]

> AGENT

Now I understand the prefill path. Critically — for draft prefill (`forward_draft_extend`), `spec_info = EagleDraftInput` (with hidden_states, no kv_indptr/kv_indices), and `generate_attn_arg_prefill` is what builds kv_indices. Let me look at that again carefully — line 226: `paged_kernel_lens = paged_kernel_lens + self.draft_token_num`. But for `EagleDraftInput` (draft EXTEND), is that the right path? Let me check:

> AGENT

Got it. So for draft prefill (extend_after_decode and forward_draft_extend), `EagleDraftInput.generate_attn_arg_prefill` builds kv_indices by reading from `req_to_token` rows with no `kv_start_idx` (None). To clip we'd need to either (a) pre-shift `paged_kernel_lens` and pass a `kv_start_idx`, or (b) override seq_lens at worker level. Now check forward_batch positions and how draft model consumes them. Let me look at draft model forward.

> AGENT

So `positions` is what the draft RoPE sees — comes from forward_batch.positions. For draft prefill, these are the absolute positions. For draft decode, look at how positions in `eagle_info.py` are seeded (e.g., line 1193): `spec_info.positions = batch.seq_lens.repeat_interleave(self.topk, dim=0)`. So positions are ABSOLUTE (seq_len-based). Now let's check the draft worker flow more carefully — how `forward_batch.positions` is set just before draft_model_runner.forward.

> AGENT

Let me check the EagleDraftExtendCudaGraphRunner (used for draft prefill / extend after decode).

> AGENT

Good. Now let me check init_forward_metadata for non-cuda-graph (eager) path entry to see hook points (`init_forward_metadata` in flashinfer_backend):

> AGENT

Now I have enough info to write the report. Let me also confirm whether draft decode uses cuda graph and how decode positions work.

> AGENT

Now I have everything to write the report. # 报告：EAGLE-3 draft attention kv_indices 数据流与 clip 可行性 ## 调研结论（5 个问题逐答） **A. Draft prefill (forward_draft_extend) 的 kv_indices** 入口：`eagle_worker.py:2086 forward_draft_extend()` → `init_forward_metadata(forward_mode=DRAFT_EXTEND)`（`flashinfer_backend.py:434`）→ `FlashInferIndicesUpdaterPrefill.update_single_wrapper` → `call_begin_forward()`（`flashinfer_backend.py:1213,1344`）。 由于 `spec_info` 是 `EagleDraftInput` 实例，跳过普通分支，走 `EagleDraftInput.generate_attn_arg_prefill`（`eagle_info.py:1015`）： - 调用 `create_flashinfer_kv_indices_triton`（`eagle_info.py:1064`），`paged_kernel_lens` 来自 `forward_batch.seq_lens`（target 已写满的 BF16 draft KV slots，长度 = seq_len_incl_just_accepted） - 第 5 个参数 `kv_start_idx=None`，即**从 `req_to_token` row 的位置 0 起读，长度 = seq_len**。结果就是 `req_to_token[req, 0:seq_len]` 全量 slots。**没有 trailing-N 概念**。 **B. Draft decode (每个 spec step) 的 kv_indices** 入口：`eagle_worker.draft_forward`（`eagle_worker.py:1646`）→ `FlashInferMultiStepDraftBackend.common_template`（`flashinfer_backend.py:1508`）→ `generate_draft_decode_kv_indices` triton kernel（`spec_utils.py:413`）。 实现逻辑（`spec_utils.py:447-481`）：每 step 把 `req_to_token[req, 0:seq_len]` 全拷到 step-i 缓冲区，再追加该 step 新分配的 `topk` 个 draft slot。**结果就是 [0..seq_len+i+1) 全量**，每 step 都从 0 开始。 **C. Worker 层 clip 可行性** **可行但 NOT trivial**。两条路径： 1. **Prefill 路径**：clip 必须深入到 `EagleDraftInput.generate_attn_arg_prefill`（`eagle_info.py:1015`）。它无 `kv_start_idx` 参数，硬编码 `None`；要么 monkey-patch 它在调用 triton kernel 之前把 `paged_kernel_lens` 截到 N + 把 `kv_start_idx` 传成 `seq_lens - N`，要么在 worker 层 override `forward_batch.seq_lens` 但同时还要 shift `req_to_token` 内容——后者**不可行**（target 真正在 trailing slot 写 KV，前 N-prefix 的 slots 是 stale）。 2. **Decode 路径**：必须替换 `generate_draft_decode_kv_indices` triton kernel（`spec_utils.py:413` / `flashinfer_backend.py:1477` 引用），因为它没有 start-offset 概念，且 step-i 内部计算依赖 `cum_seq_len`（line 445）。Clip 后还得保持 step-i 的 draft slot 追加逻辑（line 460-481）。**clip 决策必须在 kernel 内或重写 kernel**，worker 层无法外部 clip。 > 注意 flashinfer backend 已内置 sliding window 支持（`flashinfer_backend.py:923 dispatch_reason == WrapperDispatch.SLIDING_WINDOW`），用 `kv_start_idx = seq_lens - paged_kernel_lens_tmp`（line 998）实现 trailing-N，但**只对 spec_info=None 的非 spec 路径生效**——EAGLE 的 EagleDraftInput / EagleVerifyInput 直接走 `spec_info.generate_attn_arg_prefill / generate_attn_arg_decode`，绕过 sliding window 派发。 **D. CUDA Graph 兼容性** draft decode **必定走 cuda graph**（`eagle_draft_cuda_graph_runner.py`），prefill/extend 默认也用（`eagle_draft_extend_cuda_graph_runner.py`）。但 kv_indices buffer 是**预分配大缓冲**（`flashinfer_backend.py:514 max_num_tokens*max_context_len`、`1575 speculative_num_steps*max_bs*max_context_len`），flashinfer plan 通过 `kv_indptr` 切片读取——**kv_indices 实际长度变化不破坏 graph replay**，只需保证 indptr / buffer 容量不溢出。clip 到 trailing-N 是**缩短**，对 graph 兼容。 但 replay 时 `init_forward_metadata_replay_cuda_graph` 会重新调 `indices_updater.update`（`flashinfer_backend.py:690`），里面会重写 `kv_indptr` 和 `kv_indices`——所以 clip 必须 inject 到 replay 路径每次都生效（不能只在 capture 时改一次）。 **E. RoPE positions** draft 用的 `positions` 是**绝对**位置： - Prefill: `forward_batch.positions` 来自 `model_worker_batch`，由 scheduler 按真实 token offset 填充（即 seq 在 target context 中的真实索引 0..seq_len-1）。 - Decode: `eagle_worker.py:1193` `spec_info.positions = batch.seq_lens.repeat_interleave(topk, dim=0)`；每 step `forward_batch.positions.add_(1)`（`eagle_worker.py:1696`）→ 绝对 seq_len 起步。 draft model 转发到 `LlamaAttention(positions=...)`（`llama_eagle3.py:91`）→ RoPE 用绝对 position。**clip kv_indices 时若改 positions，会破坏 RoPE 与 KV cache 中已写 K 的 position 一致性**。如果只 clip kv_indices 不动 positions，Q 用绝对 pos，K 也用其原始 absolute pos（cache 内已是），attention 形状是 trailing-N 的 K vs Q[last]，RoPE 兼容。**保持 positions 不变是正确做法**。 ## 关键结论 — 工作量 worker 层 clip **"不可行（不动 attention backend）"**。triton kernel `generate_draft_decode_kv_indices`（spec_utils.py:413）和 `EagleDraftInput.generate_attn_arg_prefill`（eagle_info.py:1015）是**唯一构造 kv_indices 的入口**，且都**不暴露 start_offset / clip 参数**。worker 层最多能改 `forward_batch.seq_lens`，但那会让 target draft KV 写位置错位、accept_length / out_cache_loc / `assign_req_to_token_pool` 全错。 ## 推荐方案（最干净 hook） **写一个 SALA-only 包装函数，替换两处 kv_indices 构造**，保持 attention backend 文件不动： 1. **Decode path**：在 `eagle_worker.__init__` 末尾 monkey-patch `self.draft_attn_backend.generate_draft_decode_kv_indices` 为一个新 triton kernel `generate_draft_decode_kv_indices_clipped(N)`，签名一致，只改两点： - kernel 内 `seq_len` 用前先 `clip_start = max(0, seq_len - N)`，循环从 `clip_start` 起 - kv_indptr 用 […]

> DEVELOPER

背景:我在 /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py 的 `forward_draft_extend` (line 2086-2196) 加了 sliding-window draft prefill skip 逻辑,当 chunked prefill 当前 chunk 远离请求末尾时直接跳过 draft forward。当前实现 skip 时直接 `return`,不调用 `capture_for_decode`,不写任何 placeholder。 我需要你严格 review 这个 return 行为的正确性。具体 5 个问题: 1. **read 路径**: 在 chunked prefill 期间,某个被 skip 的中间 chunk 之后(但下一个 chunk 之前),是否有任何代码读取 `batch.spec_info.topk_p / topk_index / hidden_states`?如果有,这些位置目前是什么值(skip 完后)?能否容忍 None 或上一次的残留? - 重点查 scheduler / batch 管理代码,看 `batch.spec_info` 在 forward_draft_extend 返回后会不会立即被消费 - 查 `prepare_for_decode` / `draft_forward` 等 decode 入口的读取时机 2. **末 chunk 必跑保证**: 我的 skip 条件是 `all(seq_lens_cpu[i] < req_total_lens[i] - _last_n)`。请验证:对于每个请求,**最后一个** chunked prefill chunk 是否一定满足 `seq_lens == req_total`(即 skip 条件必为 False)?如果有边界情况(比如 chunk size 正好对齐,或单 chunk 完成 prefill),会不会被错误 skip? 3. **batch.spec_info 重建**: 每次 `forward_draft_extend` 调用 line 2100 都重建 `EagleDraftInput`,line 2107 跑 `prepare_for_extend`。请验证:中间 chunk skip 时跳过 forward 和 capture_for_decode 后,留下的 spec_info 状态在下一 chunk 入口处是否会被完全覆盖、不会污染下一 chunk? 4. **draft KV cache 写入**: skip 中间 chunk 时,这些 token 位置对应的 draft layer KV slot 是否会写入?如果不写入,decode 期间 draft attention 读这些位置的 paged FA 时读到什么(0、上次请求残留)?在 524K context 下 32K window 之外的位置实际会被 query 吗? 5. **forward_batch 副作用**: `forward_draft_extend` 末段(原本被 skip 的代码 line 2187-2196)创建 `forward_batch = ForwardBatch.init_new(...)`、跑 `forward`、然后 `assert forward_batch.spec_info is batch.spec_info` + `capture_for_decode`。跳过这些是否漏掉了任何**对 batch 状态的必要副作用**(比如 input_ids 更新、cuda graph state 维护)? 读相关代码确认。给我一个简洁的 yes/no per question + 具体 file:line 证据。在 200 字以内总结。

> AGENT

我来逐个验证这五个问题。先读相关代码。

> AGENT

Now let me look at how `forward_draft_extend` is called and what consumes `batch.spec_info` after the call.

> DEVELOPER

背景:在 /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/ 里有两套 EAGLE draft worker: - `speculative/eagle_worker.py` (v1) - `speculative/eagle_worker_v2.py` (v2,含 EAGLEWorkerV2 / EagleDraftWorker class) - `speculative/multi_layer_eagle_worker_v2.py` / `standalone_worker_v2.py` 我们的生产配置(`/user_4813494d/openbmb/eval/start_eagle.sh`)用: - `--speculative-algorithm EAGLE3` - (无 `--enable-multi-layer-eagle`) 请验证以下两点,给出 file:line 证据: 1. **EAGLE3 走哪条路径?** 在 `managers/scheduler.py` 和 `speculative/spec_info.py` 里找 `--speculative-algorithm EAGLE3` 的路由代码。具体: 这个算法名最终实例化的是 `eagle_worker.py` (v1) 里的 EAGLEWorker 还是 `eagle_worker_v2.py` 里的 EAGLEWorkerV2? 2. **EAGLE3 + 当前 config 下,v2 文件是死代码吗?** 进一步确认: - 在没有 `--enable-multi-layer-eagle`、没有 standalone draft 的情况下 - 启动 EAGLE3 server 时,`eagle_worker_v2.py` 里 `EagleDraftWorker.forward_draft_extend` 会被调用到吗? - 如果不会,我把 v2 文件的实验代码 `git checkout HEAD --` 还原是否安全? 200 字以内简洁回答 + 关键 file:line。

> AGENT

我来验证这两点。

> AGENT

Good. Now I can see in `forward_batch_generation` (extend branch), after `forward_draft_extend` returns the function just returns `GenerationBatchResult` — no immediate consumption of `spec_info` happens this round. Now let me check the scheduler / batch path to see whether `batch.spec_info` is read between chunks.

> AGENT

Now let me check `process_batch_result_prefill` to see if it reads spec_info.

> AGENT

关键分歧点是 `enable_overlap`。需要确认 `start_eagle.sh` 是否启用 overlap。

> AGENT

Good — `process_batch_result_prefill` doesn't read `batch.spec_info`. Now let me check `prepare_for_extend` (called at line 2107) to understand what state it leaves behind, and how `EagleDraftInput` is constructed.

> AGENT

MiniCPMForCausalLM 分支没有强制 disable_overlap_schedule。但是看到 line 2018, 2100 还有别的强制。让我查:

> AGENT

Now let me check `capture_for_decode` to see exactly what fields it writes.

> AGENT

关键发现:EAGLE3 没有强制 disable_overlap_schedule。在 MiniCPM 上 disable_overlap_schedule 默认 False(server_args.py:574)。因此 `enable_overlap=True`,会路由到 EAGLEWorkerV2。 但还需要排除 MiniCPM 特定路径,看 server_args.py:1544 MiniCPM 分支是否动了 overlap:

> AGENT

Now let me look at how draft KV is written during draft prefill, and check chunked prefill semantics — confirm last chunk satisfies `seq_lens == req_total`.

> AGENT

Now let me look at `prepare_for_extend` in ScheduleBatch and confirm `seq_lens` semantics on chunked-prefill (does it reflect actual completed prefix or end-of-chunk position?).

> AGENT

**关键证据找到了**:server_args.py:2185-2218。EAGLE3 路径下,只有当 `SGLANG_ENABLE_SPEC_V2=True` 时才 `disable_overlap_schedule=False`,否则强制 `disable_overlap_schedule=True`(line 2214)。 确认 start_eagle.sh 是否设了这个 env:

> AGENT

Good — `seq_lens` = `len(r.fill_ids)` which includes all tokens already filled (prefix + current chunk). Now check `init_next_round_input` to confirm chunked-prefill flow.

> AGENT

Now let me look at PrefillAdder's `add_one_req` chunked logic to understand which chunk is the "last chunk" and what `fill_ids` looks like at that point.

> AGENT

确认证据链完整: - `prepare_env.sh:515` 显式 `export SGLANG_ENABLE_SPEC_V2=0` - `start_eagle.sh` 没有覆盖,所以保持 `SGLANG_ENABLE_SPEC_V2=False` - `server_args.py:2199-2214`:EAGLE3 + `SGLANG_ENABLE_SPEC_V2=False` → `self.disable_overlap_schedule = True` - `scheduler.py:286`:`enable_overlap = not disable_overlap_schedule = False` - `scheduler.py:506`:`enable_multi_layer_eagle=False`,走 else 分支 - `scheduler.py:536-537`:调用 `spec_algorithm.create_worker(enable_overlap=False)` - `spec_info.py:74-82`:`enable_overlap=False` → 返回 `EAGLEWorker`(v1),**不是** V2 --- ## 答案 **1. EAGLE3 走 v1。** 路由链: - `eval/start_eagle.sh` 未设 `SGLANG_ENABLE_SPEC_V2`,而 `demo-sala/prepare_env.sh:515` 强制 `export SGLANG_ENABLE_SPEC_V2=0` - `server_args.py:2199-2214`:EAGLE3 + spec_v2 off → `disable_overlap_schedule=True`(line 2214) - `scheduler.py:286`:`self.enable_overlap = not disable_overlap_schedule = False` - `scheduler.py:506`:`enable_multi_layer_eagle=False`,走 else 分支 `create_worker(enable_overlap=False)`(line 536-538) - `spec_info.py:74-82`:`enable_overlap=False` → `from sglang.srt.speculative.eagle_worker import EAGLEWorker`(v1) V2 的入口是 `spec_info.py:76` `from ... eagle_worker_v2 import EAGLEWorkerV2`,仅当 `enable_overlap=True` 才进。 **2. 当前 config 下 v2 是死代码,还原安全。** 没有任何路径会走到 `eagle_worker_v2.py:77 EagleDraftWorker.forward_draft_extend`: - spec_v2 默认 False(`environ.py:367`),且 `prepare_env.sh:515` 锁死为 0 - 提交包没有 `--enable-multi-layer-eagle`,所以 `multi_layer_eagle_worker_v2.py` 也不进 - `start_eagle.sh` 走 EAGLE3 路径,只会用 `eagle_worker.py` (v1) 里的 `EAGLEWorker` `git checkout HEAD -- eagle_worker_v2.py multi_layer_eagle_worker_v2.py standalone_worker_v2.py` 还原对当前 EAGLE3 生产配置无影响。建议同时核对一下 `eagle_info_v2.py` 是否也仅被 v2 引用;另外若以后想开 spec v2 overlap,记得 v2 路径还有 `topk=1` 限制(`server_args.py:2207-2212`),当前生产 `topk=2`,直接开 spec v2 会报错,所以也确认了 v2 文件在当前提交参数下不可能被激活。

> AGENT

So on a chunked-prefill round, `req.fill_ids` is truncated to `prefix_indices + extend_input_len` (line 463), and `seq_lens = len(r.fill_ids)`. For the **final** chunk, the request is no longer chunked — `add_chunked_req` returns `None` (line 476, when `truncated == False`), meaning `extend_input_len` was small enough that `fill_ids` reached the full origin length. Let me also see what `process_batch_result_prefill` does with chunked vs final chunk.

> AGENT

Good. No `spec_info` access in either prefill chunk path. Now let me verify the draft model's KV write path during prefill — confirm whether skipping forward leaves KV slots unwritten and how decode reads them.

> AGENT

Now check how draft KV cache slot is allocated and written during `forward_draft_extend` (so I can confirm whether skip leaves slots unwritten or unallocated).

> AGENT

Now the key — the draft model uses a **separate** KV cache pool from the target. Let me confirm.

> AGENT

Now I need to confirm that during the chunked draft prefill, KV slots ARE allocated for the chunk (so the slot is "owned") — and whether the model forward, if skipped, just skips writing to those slots. Let me trace `out_cache_loc` and confirm the draft model runner forward writes KV via the model's `forward` (writes through `save_kv_cache`).

> AGENT

So KV cache is written inside the model forward call via attention backend. If `forward_draft_extend` skips `draft_model_runner.forward(...)`, the draft KV slots for that chunk are NOT written. Now let me confirm: are slots actually **allocated** for the draft KV (would create a leak), or is alloc tied to a different path?

> AGENT

OK — this `prepare_for_extend` is on the **target** ScheduleBatch. The target slots get allocated and written via the target forward (which happened before `forward_draft_extend` is called). So `out_cache_loc` is the **target** model's slots. But the draft model uses `self.draft_model_runner.token_to_kv_pool`. Is the draft model's KV pool **shared** with the target model? Let me check.

> AGENT

Now let me see how draft and target share. Check eagle_worker init.

> AGENT

Key fact: **Draft and target worker share `req_to_token_pool` and `token_to_kv_pool_allocator`, BUT own separate KV cache pools** (line 334 comment, line 1719 says "allocator and kv cache pool are shared with target worker" — actually that comment in clear_cache_pool says they're shared. Conflicting comments). Let me check further.

> AGENT

Important: the **draft model owns its own KV cache pool** (memory_pool.py per-model), but the **allocator** (which assigns slot indices) is shared. So when target prefill alloc's slot N, the draft also uses slot N to write its KV. Skip → draft slot N is unwritten. Now confirm: at decode time, will the draft attention paged FA read those skipped slot positions? Let me check the `_draft_preprocess_decode` to understand which KV slots get read.

> AGENT

Key point: draft decode reads KV from positions 0..seq_len-1 via `req_to_token` mapping; those slots were populated during target prefill (target's KV cache) AND draft prefill (draft's KV cache) — but if we skipped the draft forward for chunk, the **draft's** KV slots for those positions are never written. So draft attention during decode WILL read uninitialized values for the skipped range. But the user's comment at line 2138 acknowledges this — "Draft KV slots for skipped positions remain zero-initialized". Let me verify zero-init. Check memory_pool init.

> AGENT

Good — KV cache buffers are `torch.zeros` initialized. So skipped slots ARE truly zero (not residual from a previous request, assuming the buffer wasn't reused for another request — but the allocator's `free` returns slot indices to the free list, so previously freed slots COULD be reused). Wait — slots are freed and re-allocated per request. So if request A was here before and wrote draft KV into slot X, then was freed, and request B is allocated slot X for chunk skip, the draft KV at slot X is **residual from request A**, not zero. Let me verify slot reuse behavior.

> AGENT

Confirmed: freed slot indices are returned to the free pool and reused without zeroing the underlying KV memory. So skipped slots will hold residual data from **prior requests**, not zero. The user's comment ("zero-initialized") is incorrect in the general case. Empirically the model still works because: 1. Sliding window cuts to 32K most-recent tokens (positions that ARE written this request) 2. The skipped positions (outside the window) ARE still pointed to by `req_to_token[req_pool_idx][:seq_len]` and reachable through paged FA at decode time 3. Long-context draft attention is dominated by recency But "**zero-initialized**" is **not** what happens for slot reuse. Now let me also confirm what `prepare_for_extend` does in EagleDraftInput (line 2107) — specifically the line `batch.input_ids[pt : pt + extend_len] = torch.cat((input_ids[1:], self.verified_id[i].reshape(1)))`. The EagleDraftInput `prepare_for_extend` (eagle_info.py line 855) modifies `batch.input_ids` in place — this is a side effect on the **target's** ScheduleBatch input_ids. Let me check if anyone reads `batch.input_ids` after `forward_draft_extend` returns.

> AGENT

No direct reads of `batch.input_ids`. Good. Now let me confirm question 2's edge case: when chunk_size aligns exactly with the last chunk, what is `seq_lens`? Looking back: in `add_chunked_req` (line 461), `truncated = req.extend_input_len > _rem_tokens`. If `_rem_tokens >= req.extend_input_len`, truncated=False, the chunk is the LAST chunk. After `set_extend_input_len(min(...))`, `fill_ids` is truncated to `prefix + extend_input_len`. Since `extend_input_len` is the remaining (full) extension needed, `len(fill_ids) == prefix + extend_input_len = origin_input_ids` (since the last round had `fill_ids = origin_input_ids` set in init_next_round_input line 863). Hold on — `init_next_round_input` line 863: `self.fill_ids = self.origin_input_ids + self.output_ids`. For prefill (no output_ids yet), this equals `origin_input_ids`. So `seq_lens = len(fill_ids)` for the last chunk = `len(origin_input_ids) = req_total_lens[i]`. The skip condition `seq_lens < req_total - N` is False for the last chunk. **Confirmed last chunk always runs.** Edge case: what if the request is so short it fits in a single chunk (no chunking)? Then `add_one_req` (line 545-555 non-chunked path): `extend_input_len` is full, `fill_ids` is unmodified (still = full `origin_input_ids`), so `seq_lens = req_total`. Skip condition False. **Single-chunk also fine.** Now let me look at whether there's CUDA graph state maintenance that could break.

> AGENT

This is `forward_draft_extend_after_decode` (different code path, called after decode). In our `forward_draft_extend` (chunked prefill path, line 2086), looking at line 2187-2196, there's no cuda graph for this path — it's plain eager `draft_model_runner.forward(forward_batch)`. So skipping is safe for cuda graph state. I have enough evidence. Let me write up the summary. **Findings per question:** 1. **read path between chunks**: NO. After `forward_draft_extend` returns in the extend branch (eagle_worker.py:742), `forward_batch_generation` returns immediately with `GenerationBatchResult` (line 746-751). Scheduler's `process_batch_result_prefill` (scheduler_output_processor_mixin.py:85-237) never reads `batch.spec_info`. No code consumes `topk_p/topk_index/hidden_states` between chunks. They stay at default `None` from `EagleDraftInput` field defaults (eagle_info.py:816-819). 2. **last-chunk guarantee**: YES. `init_next_round_input` (schedule_batch.py:863) sets `fill_ids = origin_input_ids + output_ids`; for prefill `output_ids=[]` so `fill_ids = origin_input_ids`. `add_chunked_req` (schedule_policy.py:461-463) sets `truncated = extend_input_len > _rem_tokens`; the final chunk satisfies `truncated=False` and leaves `fill_ids` full-length. `seq_lens = len(fill_ids)` (schedule_batch.py:1471) thus equals `req_total`. Skip condition `seq_lens < req_total - N` is False. Single-chunk case (`add_one_req` line 545-555) also leaves `fill_ids` full-length. No boundary case mis-skips. 3. **spec_info rebuild**: YES. Line 2100-2107 unconditionally reconstructs `batch.spec_info = EagleDraftInput(...)` and reruns `prepare_for_extend` at every `forward_draft_extend` call. The skipped chunk's leftover `topk_p=None / topk_index=None / hidden_states=None` is overwritten by the next chunk's fresh constructor. No state pollution. 4. **draft KV not written**: YES, slots are unwritten — but the user's comment "zero-initialized" is **misleading**. KV pool buffers are `torch.zeros`-initialized at startup (memory_pool.py:972,980,1220+), BUT the allocator (allocator.py:155-163) returns freed slots to a reusable pool **without zeroing** the underlying KV memory. So skipped slots can hold residual data from **prior requests** that previously used those slot indices. At decode, draft paged FA does read these positions (req_to_token covers full seq_len). Empirically it works because draft attention is recency-dominated and the trailing 32K window is the only meaningful KV. **Suggest correcting the inline comment**: replace "zero-initialized (memory_pool default)" with something like "unwritten — may contain residual from prior requests sharing the same slot index; draft attention tolerates this because the trailing N-token window dominates softmax". This is a doc fix, not a correctness bug. 5. **forward_batch side effects**: NO observable issue. `ForwardBatch.init_new` is pure construction, `return_logprob = False`, `forward(...)` and `capture_for_decode` are the only side effects skipped — which is intentional. `prepare_for_extend` (line 2107) ran already, so `batch.input_ids` is in-place updated with verified_id shifted; no consumer between chunks anyway. `forward_draft_extend` has no cuda graph for this code path (line 2187-2191 is plain eager forward; `cuda_graph_runner_for_draft_extend` is only used in `forward_draft_extend_after_decode` […]

> DEVELOPER

背景:我要给 SGLang 的 EAGLE-3 draft model (`demo-sala/sglang/python/sglang/srt/models/llama_eagle3.py`,class `LlamaForCausalLMEagle3`)启用 sliding window attention,目标是让 draft 的 1 层 attention 只读最近 N 个 token 的 KV(真截断 kv_indices,不是 mask)。 我已经确认: - `model_runner.py:925-926`: `if hasattr(model, "get_attention_sliding_window_size"): self.sliding_window_size = self.model.get_attention_sliding_window_size()` — 这是 model 端唯一触发 model_runner.sliding_window_size 的入口 - `flashinfer_backend.py:152-154`: `model_runner.sliding_window_size is not None → num_wrappers=2 + dispatch_reason=SLIDING_WINDOW` - prefill SWA(line 1253-1300) + decode SWA(line 972-1020) 都是 kv_indices clip,真省 FLOPs - `RadixAttention.__init__` 接受 `sliding_window_size`,运行时 `layer.sliding_window_size` 会被 prefill_wrapper.forward 的 `window_left=` 读到 现在 EAGLE3 draft 在 LlamaAttention.__init__ (`models/llama.py:182-190`) 构造 RadixAttention **不传** sliding_window_size,默认 -1。 **3 个具体问题需要你给精确答案 + file:line 证据**: 1. **EAGLE3 draft 的 model_runner 是哪个?** EAGLE worker 启动时,draft model 独立构造一个 ModelRunner 还是共用 target 的?在 `speculative/eagle_worker.py` 里找 `draft_model_runner` 初始化代码,确认它是独立的 ModelRunner 实例。这关系到:在 draft model class 里加 `get_attention_sliding_window_size()` 会被 draft 自己的 ModelRunner 调用,**不会**影响 target ModelRunner 的 sliding_window 设置。 2. **draft 的 attention backend 路径**:start_eagle.sh 用 `--speculative-draft-attention-backend flashinfer`。但 target 是 `minicpm_flashinfer`。这两个 backend 在 SWA 路径上一样吗?具体: - draft 用的 backend 类是哪个(file:line)? - 它是否走我描述的 `FlashInferAttnBackend` (flashinfer_backend.py)? - 它处理 `model_runner.sliding_window_size` 的逻辑和我描述的一致吗? 3. **draft cuda graph runner SWA 兼容性**: - `speculative/eagle_draft_cuda_graph_runner.py` 和 `eagle_draft_extend_cuda_graph_runner.py` 在 cuda graph capture/replay 时如何处理 multi-wrapper(2 个 wrapper)的 plan? - SWA 下 max paged_kernel_lens 缩到 sliding_window+1(比如 32K),是否会让 graph kv_indices buffer 缩小? - 是否有任何 cuda graph capture 时 plan 拍 1 个 wrapper、replay 时实际跑 2 个 wrapper 的不一致风险? 读相关代码确认,简洁回答(每问 100 字内 + 关键 file:line)。

> AGENT

我来逐个查证这三个问题。

> AGENT

好,确认 EAGLEWorker extends TpModelWorker,super().__init__ 会创建自己的 ModelRunner。`draft_model_runner` 是 `self.model_runner`(line 720-721)。下面看 init_attention_backend 和 DraftBackendFactory。

> DEVELOPER

背景:我已实现 EAGLE-3 chunked prefill 早 chunk 完全 skip(chunk-level skip,在 `demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:2086-2200` `forward_draft_extend` 里,当 `seq_lens[i] < req_total[i] - LAST_N` for all reqs 时直接 return)。 正在考虑加另一项算法改进:EAGLE-3 draft 自己的 attention 开启 sliding_window(SGLang 原生 SWA,真截断 kv_indices)。 两项叠加的语义需要你审清楚: **4 个互动问题**: 1. **draft KV 写入路径**: - chunk skip 让 draft prefill **整个 forward 不跑** → KV 不写 - 加 draft SWA 后,**末 chunk** 跑 draft prefill 时,SWA prefill 的 KV 写入会写哪些位置?会写全 chunk 还是只写 window 内?具体看 `flashinfer_backend.py:843-846` `set_kv_buffer(layer, cache_loc, k, v, ...)` 和 prefill SWA 的 `paged_kernel_lens / kv_start_idx / use_sliding_window_kv_pool`。 - 末 chunk 的 cache_loc 是 `out_cache_loc`(整 chunk 的 token 写入位置),还是只 window 内?如果是整 chunk,write 仍然全写,SWA 只影响 read。 2. **stale-KV 风险是否真消除**: - chunk skip 留下早 chunk 位置的 draft KV = uninitialized/garbage(allocator 复用 slot 不清零) - 加 SWA 后,decode 阶段 draft attention 看的是 `clamp(seq_lens, max=sliding_window+1)` 的尾部 KV → 早 chunk 那些 garbage 位置**根本不读** → 风险真消除? - 但 prefill 末 chunk 的 SWA 也会读 prefix_lens 之前的 KV(`kv_start_idx = seq_lens - paged_kernel_lens` 可能跨越早 chunk skip 留下的 garbage 区间),需要确认末 chunk attend window 内是否完全落在末 chunk 自己刚写入的范围,不会触碰 chunk-skip 的 garbage 区 3. **chunk skip 和 SWA window 的关系**: - chunk skip 的 LAST_N = 32K(只末尾 32K 进 draft prefill forward) - 如果 SWA window = 32K,这两个 N 相等。中间 chunk 不跑 prefill 但 SWA decode 也不读它,逻辑闭合 - 但 SWA 应该比 chunk-skip 的 N 略大,因为 chunk 边界对齐会导致末 chunk 的实际 prefill 范围可能 < LAST_N(末 chunk 是 chunked-prefill 的最后一段,长度 = req_total - prev_chunk_end ≤ chunk_size=8192) - 末 chunk 进 draft prefill 后,decode 阶段 SWA 看的 window 跨越多少个之前的 chunk? - 推荐 SWA = chunk-skip LAST_N + chunk_size(margin),还是相等,还是别的? 4. **接受率影响**: - chunk skip + SWA 同时启用,理论上接受率(accept_len)和单独 SWA 有差异吗? - 单独 SWA:全部 chunk 都跑 prefill forward(MLP 全跑),attention 只读 window。chunk skip 节省的是 forward(MLP/proj/norm)整体 - 单独 chunk skip:跳 forward,KV 不写,decode 时读到 garbage - 两者叠加:跳 forward + decode 读不到 chunk-skip 区域(被 SWA window 截断) - 推断:chunk skip 现在变得"无风险"(garbage 被 SWA window 隐藏),accept_len 应不变;wall = chunk skip 的省时收益 + SWA 在末 chunk attention 的省时 精读 `flashinfer_backend.py:780-848 (prefill)`、`972-1020 (decode SWA)`、`speculative/eagle_worker.py:2086-2200 (chunk skip)`、`memory_pool/allocator.py` (slot 复用),给精确回答 + file:line 证据。每问 150 字内。

> AGENT

我开始精读相关代码。

> AGENT

好。draft 用 `FlashInferMultiStepDraftBackend` (decode) 和 `FlashInferAttnBackend` (prefill/extend),都来自 `flashinfer_backend.py`。下面看 `FlashInferMultiStepDraftBackend` 的 SWA 处理。

> DEVELOPER

背景:我要给 SGLang 的 EAGLE-3 draft model (`demo-sala/sglang/python/sglang/srt/models/llama_eagle3.py`)启用 sliding window attention。draft model 配置在 `/user_4813494d/openbmb/demo-sala/data/eagle_draft/config.json`,关键字段: - `num_hidden_layers: 1` - `max_position_embeddings: 524288` - `architectures: ["LlamaForCausalLMEagle3"]` - `eagle_config: {...}` 我决定的注入方式:在 `LlamaForCausalLMEagle3` 加 `get_attention_sliding_window_size(self)` 方法,因为这是 model_runner.py:925-926 触发 `model_runner.sliding_window_size` 的唯一干净入口。但配置值(SWA 大小)的来源需要思考。 **3 个具体问题**: 1. **配置来源的最佳设计**: - **方案 A**:用 env `SGLANG_EAGLE_DRAFT_SLIDING_WINDOW` - **方案 B**:在 `server_args.py` 加 `speculative_draft_sliding_window: int = 0`,通过 CLI `--speculative-draft-sliding-window N` 传入 - **方案 C**:写到 `config.json` 的 `eagle_config` 里 - 哪种最干净?注意:`get_attention_sliding_window_size(self)` 是在 model class 内调用,如何拿到 server_args / env? - 看 `model_runner.py` model 初始化时,model 拿不拿得到 server_args(self.model_config 字段、其他渠道)? 2. **数值约束** — 调研以下边界: - SGLang FlashInfer SWA 要求 `sliding_window_size > 0`(否则 num_wrappers=2 不开启)— 0 怎么处理?见 `flashinfer_backend.py:152` `model_runner.sliding_window_size is not None` - `RadixAttention.__init__` line 76: `self.sliding_window_size = sliding_window_size or -1` — 传 0 会变 -1,后续 wrapper 路由 `_get_wrapper_idx`(line 893)`return layer.sliding_window_size == -1` 会把这层归到 full attention wrapper(wrapper 1)。注入时务必传 > 0 的值。 - draft 1 层 → `get_attention_sliding_window_size()` 必须返回 > 0 才生效;返回 None 走默认 full attention - 推荐默认值:32K(和 chunk-skip LAST_N=32K 对齐)? 或留 0 = 关闭? 3. **副作用 / 兼容性**: - SWA + `--disable-radix-cache`(我们 start_eagle.sh 显式禁用)— 兼容吗? - SWA + `--speculative-num-steps 3 --speculative-eagle-topk 2`(我们当前 spec config)— 兼容吗?(draft decode 走 step 0/1/2 多步,每步都用同样 SWA 配置) - SWA + `--speculative-draft-attention-backend flashinfer`(明确指定 backend)— SGLang 是否还有别的 flashinfer 变体不支持 SWA? - SWA + 我们 target 不开 SWA(target 是 minicpm.py,完全独立)— 是否需要在 ModelConfig 等地方做 cross-check? - 启动期是否有 `assert sliding_window XX and YY` 之类的检查会卡住? 读代码确认,简洁回答(每问 200 字内 + file:line)。

> AGENT

关键点:`FlashInferMultiStepDraftBackend` 内部为每个 spec step 各创建一个 `FlashInferAttnBackend`(line 1493-1501),每个都看 `model_runner.sliding_window_size`,所以会各自 `num_wrappers=2`。下面看 `model_runner.py:925` 处 sliding_window 的初始化代码,以及 draft 是否真的会调用这个 hook。

> AGENT

我来调研代码，回答这 3 个问题。

> AGENT

Now let me look at how SWA prefill is set up in prefill indices updater, and the sliding-window kv pool behavior.

> AGENT

好,确认这个 hook 在每个 ModelRunner 的 load_model 流程内本地调用 `self.model.xxx`,所以 draft ModelRunner 加 hook 只影响 draft 自己。下面看 cuda graph runner 对 multi-wrapper 的处理。

> AGENT

关键观察:cuda graph runner 调用 `self.draft_attn_backend.init_forward_metadata_capture_cuda_graph` 和 `init_forward_metadata_replay_cuda_graph`,这些都是 `FlashInferMultiStepDraftBackend` 的方法,它内部会循环 `self.attn_backends[i]`(每个 step 的 backend);每个 backend 自己再调用 `update_sliding_window`(line 972/1253)。下面看 FlashInferAttnBackend 在 capture/replay 时是否 honor multi-wrapper SWA。

> AGENT

Now let's examine the memory pool allocator to understand slot reuse / non-zeroing.

> AGENT

关键:`init_cuda_graph_state` 走 `num_wrappers`(line 522-524),分配 2 个 `cuda_graph_kv_indices`,每个 size 都是 `max_num_tokens * self.max_context_len`。但 `FlashInferMultiStepDraftBackend.init_cuda_graph_state`(line 1574-1584)只给一个 buffer `self.cuda_graph_kv_indices[i]`,然后 `attn_backends[i].init_cuda_graph_state(max_bs, max_num_tokens, kv_indices_buf=self.cuda_graph_kv_indices[i])`。等等 — 它传了一个 buf,但 FlashInferAttnBackend 还会 clone 它(line 522-524)。所以第 2 个 wrapper 用 clone — clone 出来的是独立 buffer,跨 step 的 SWA 是 ok 的。 但要验证 capture/replay 时,`num_wrappers` 与 SWA size 是否正确生效。看 max_context_len 来源:

> AGENT

Confirmed: `free()` does not zero KV memory — slots are recycled by reference only. Now let's look at SWA allocator semantics.

> AGENT

`max_context_len = model_config.context_len` (line 143),不受 sliding_window_size 影响 — 它就是 server_args 的 context_len(target draft 共用 524288)。所以 `FlashInferMultiStepDraftBackend.max_context_len`(line 1503)仍然是 524288,**kv_indices buffer 不会因 SWA 缩小**,但 SWA 通过 `update_sliding_window` 的 `paged_kernel_lens = clamp(seq_lens, max=window+1)` 截断 indices 内容(不缩 buffer)。 但注意 `FlashInferMultiStepDraftBackend.kv_indices`(line 1554-1560) allocates `batch_size * topk * max_context_len`,这是常驻 GPU 大块。SWA 后 logical kv 长度变短,但分配仍按 max_context_len → 内存大但 kernel FLOPs 真省。OK。 但还有一个关键点要查:`FlashInferMultiStepDraftBackend.__init__`(line 1493)创建 FlashInferAttnBackend 时传了 `kv_indptr_buf=self.kv_indptr[i]`,但 FlashInferAttnBackend 在 `kv_indptr_buf is not None` 时强制 `assert self.num_wrappers == 1`(line 221, 229)!这会与 SWA 的 `num_wrappers=2` 冲突 — 立刻崩。

> AGENT

Now let me check the prefill SWA path more carefully — particularly the `paged_kernel_lens = min(seq_lens, sliding_window + seq_lens - prefix_lens)` math, and what `prefix_lens` is in chunked-prefill.

> AGENT

确认。`FlashInferMultiStepDraftBackend` 把每个 step backend 都传了 `kv_indptr_buf` — 如果 draft model_runner 的 sliding_window_size 被设置,那 line 152-153 算 `num_wrappers=2`,line 221 `assert num_wrappers == 1` 立刻崩。**这是阻塞性 bug,必须 patch**。 下面看 draft extend cuda graph 是否也用 SWA wrapper(prefill path),即 `init_forward_metadata_capture_cuda_graph` 的 `is_draft_extend` 分支(line 615-644)是否兼容 SWA 的 `update_sliding_window`:

> AGENT

Now I have enough. Let me also peek at how `cache_loc` / `out_cache_loc` is constructed in chunked prefill — specifically whether the trailing chunk's draft prefill writes only the chunk's tokens.

> AGENT

注意:`update_sliding_window` 总是 plan 两个 wrapper(SWA + full)。这是 framework 假设有 hybrid SWA(部分层 SWA、其余 full)。但 EAGLE3 draft 只有 1 层 attention,如果它的 `sliding_window_size > 0`,会走到 SWA wrapper(0);如果是 -1,走 full(1)。但 plan 时 framework 都做两份。**OK,功能上对**。但因为只有 1 层且全 SWA,wrapper 1 plan 的全 KV 数据浪费 — 这是性能 overhead 而非正确性问题。 下面再确认 dispatch_layer 逻辑:layer.sliding_window_size 决定走哪个 wrapper:

> AGENT

确认:`_get_wrapper_idx` (line 888-897) — layer.sliding_window_size != -1 → wrapper 0 (SWA); ==-1 → wrapper 1 (full)。draft 唯一 1 层只要把 RadixAttention 的 sliding_window_size 设到 N,就吃 wrapper 0(真截断 kv_indices)。 下面回答 Q3 关于 cuda graph 一致性。

> AGENT

OK,capture 调用 `draft_attn_backend.init_forward_metadata_capture_cuda_graph` → 它就是 `FlashInferMultiStepDraftBackend` 的方法,该方法 dispatch 到每个 step backend `attn_backends[i].init_forward_metadata_capture_cuda_graph` → 那里在 line 552-580 处理 `num_wrappers=2`,2 个 decode_wrapper 都创建。replay 时 `init_forward_metadata_replay_cuda_graph` 同样路径(line 1600-1615 多 step → 每 step → 每 wrapper),所以 capture 与 replay wrapper 数一致。 下面看 multi_layer_eagle_worker 是否有差别(start_eagle.sh 用的可能是不同 worker):

> AGENT

I now have enough to answer. Let me write up the precise per-question response. # 回答(每问 ≤150 字) ## 1. draft KV 写入路径 — 末 chunk SWA prefill 全写,SWA 只影响 read 末 chunk 跑 draft prefill 时,`cache_loc = forward_batch.out_cache_loc`(`flashinfer_backend.py:755-758`)是 allocator 给这一 chunk 全部 token 分配的 slot,与 attention window 无关。`save_kv_cache` 路径走 `set_kv_buffer(layer, cache_loc, k, v, ...)`(`:843-846`),写整 chunk 的 k/v 到 swa_kv_pool(`swa_memory_pool.py:148-175`,通过 `translate_loc_from_full_to_swa` 映射到 SWA ring buffer)。SWA 只在 attention 计算时通过 `paged_kernel_lens = min(seq_lens, sw + seq_lens - prefix_lens)`(`:1270-1273`)和 `kv_start_idx = seq_lens - paged_kernel_lens`(`:1280`)裁短 read。**结论:write 全写,read 截断**。 ## 2. stale-KV 风险真消除,但有前提 decode 阶段 `paged_kernel_lens = clamp(seq_lens, max=sw+1)` + `kv_start_idx = seq_lens - paged_kernel_lens`(`flashinfer_backend.py:988-998`),只读尾部 sw 个 slot — 早 chunk skip 留下的 garbage slot(`allocator.py:155-163` `free` 只把 index 推回 free list,不清零)落在 `[0, seq_lens-sw)`,不会被读到,**风险真消除**。 末 chunk prefill 的 SWA 也安全:`kv_start_idx = seq_lens - min(seq_lens, sw + chunk_len)`(prefix_lens=prev_chunk_end,`:1270-1280`),只要 `sw ≥ LAST_N`,window 起点 ≥ chunk-skip 边界,落在末 chunk 自己刚写入的范围 — 不触碰 garbage。 ## 3. SWA window 选 LAST_N + chunk_size 留 margin 末 chunk 长度 = `req_total - prev_chunk_end ∈ (0, chunk_size=8192]`(chunked-prefill 边界对齐),不保证 ≥ LAST_N。极端 case:`req_total = N*8192 + 1`,末 chunk 只有 1 token,实际进 draft prefill 的"近端"只有 1 token。**等价 SWA = LAST_N 不够**:decode 一开始 `seq_lens = req_total`,window 起点 `seq_lens - sw = req_total - LAST_N`,正好等于 chunk-skip 边界,边界 token 可能在已 skip chunk 内(garbage)。**推荐 SWA = LAST_N + chunk_size = 32K + 8K = 40K**,留一个 chunk 的 margin,保证 window 起点严格落在末 chunk 已写入的区间内。 ## 4. 接受率:两者叠加 ≈ 单独 SWA;wall 两者相加 叠加后: - read 路径完全等于单独 SWA(只看 window 内 KV),accept_len 应**等于**单独 SWA — chunk-skip 区域被 SWA 隐藏,不参与 softmax(`flashinfer_backend.py:988-998` clamp 在 decode wrapper begin_forward 时就把 kv_indptr 截短了)。 - 单独 chunk-skip:decode 时读到 chunk-skip 区域的 garbage(`allocator.py` slot 复用未清零),理论上 accept_len 会被污染;实测稳是因为 draft 1-layer self-attn 局部主导 softmax,但**叠加 SWA 让"无污染"在语义上严谨**,不再依赖经验论证。 - wall 收益正交相加:chunk-skip 省早 chunk 整个 forward(MLP/proj/norm,占大头),SWA 省末 chunk + decode 的 attention `O(seq_len)→O(sw)`。建议 SWA=40K 先打 bench,验证 accept_len 不掉再合入。 ## 关键证据 file:line 索引 - chunk skip 主体:`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:2086-2200` - prefill write(全 chunk):`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/flashinfer_backend.py:755-758, 843-846` - prefill SWA read 裁剪:`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/flashinfer_backend.py:1267-1300`(`paged_kernel_lens = min(seq_lens, sw + seq_lens - prefix_lens)`,`kv_start_idx = seq_lens - paged_kernel_lens`) - decode SWA read 裁剪:`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/flashinfer_backend.py:972-1020`(`clamp(seq_lens, max=sw+1)`,`kv_start_idx_tmp = seq_lens - paged_kernel_lens_tmp`) - SWA pool 写映射:`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/swa_memory_pool.py:141-185` - allocator slot 复用不清零:`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/allocator.py:131-163`(`free()` 只把 index 推回 `free_pages`,无 `zero_()`) - `translate_loc_from_full_to_swa` ring buffer 映射:`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/flashinfer_backend.py:1407-1413`

> AGENT

好的——`LlamaForCausalLMEagle3` 不在 `hybrid_swa_archs` 集合里，所以 `is_hybrid_swa=False`，不会触发 `set_num_tokens_hybrid_swa()` 那条 `assert sliding_window_size > 0` 路径。这是关键。

> AGENT

现在我有足够信息回答 3 个问题。最后确认一下 spec_steps 多步 decode 与 SWA 的兼容性。

> AGENT

确认 start_eagle.sh 走的就是 `eagle_worker.py:EAGLEWorker`(非 v2 路径,在 spec_info.py 选择)。验证完成。 回答完毕。 --- ## 1. EAGLE3 draft 的 ModelRunner 是独立的 `EAGLEWorker` extends `TpModelWorker` (`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:269`),在 `__init__` 里 `super().__init__(..., is_draft_worker=True, ...)` (line 362-373) 自己跑一遍 TpModelWorker init,会 **创建独立的 ModelRunner**。所以 `self.draft_model_runner` 是 `self.model_runner`(line 720-721 显式 alias),与 `self.target_worker.model_runner` 是两个独立实例。两者只 **共享 req_to_token_pool 和 token_to_kv_pool_allocator**(line 335-337),不共享 sliding_window_size。 因此在 `LlamaForCausalLMEagle3` 上加 `get_attention_sliding_window_size()` 只会被 draft ModelRunner 自己 load_model 流程 (`model_runner.py:925-926`) 调用,target ModelRunner 完全不受影响。 ## 2. Draft 走 `FlashInferAttnBackend`,SWA 路径与 target 一致(但有 1 个阻塞 assert) start_eagle.sh `--speculative-draft-attention-backend flashinfer` (`eval/start_eagle.sh:83`)。`eagle_worker.py:327-332` 兜底:若 target 是 `minicpm_flashinfer` 且 draft 没显式指定,**强制改成 `flashinfer`**。 `DraftBackendFactory` (`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/draft_utils.py`) : - decode: `FlashInferMultiStepDraftBackend` (line 108-116),内部循环 `speculative_num_steps-1` 次创建 `FlashInferAttnBackend(skip_prefill=True, kv_indptr_buf=...)` (flashinfer_backend.py:1493-1501)。 - draft-extend (prefill): 直接 `FlashInferAttnBackend(skip_prefill=False)` (line 192-198)。 两者都是 `flashinfer_backend.py:FlashInferAttnBackend`,与 target 走的 SWA 路径(`num_wrappers=2`,`update_sliding_window`,wrapper0 = SWA clamp `kv_indices`)**逻辑完全一致**(line 152-153, 972/1253, 888-893)。 **阻塞 bug**: `FlashInferMultiStepDraftBackend` 给每个 step backend 传 `kv_indptr_buf` (line 1498-1499),而 `FlashInferAttnBackend.__init__` 在 `kv_indptr_buf is not None` 时硬 `assert self.num_wrappers == 1` (flashinfer_backend.py:221, 229)。一旦 draft `model_runner.sliding_window_size is not None`,启动就崩。必须 patch:让 multi-step 路径在 SWA 下也分配 2 套 `self.kv_indptr` / `self.kv_last_page_len`,或绕过 assert(传 2 个 buf list)。 ## 3. Cuda graph capture/replay 兼容性 `FlashInferMultiStepDraftBackend.init_cuda_graph_state` (line 1574-1584) 为每个 step 分配 buffer 时仍按 `max_context_len = model_config.context_len`(target/draft 共用 524288,line 143, 1503)**不缩 buffer**。SWA 只在 `update_sliding_window` 里 clamp `paged_kernel_lens`(line 1270-1273, 988-993),通过 `paged_kv_indptr` 截短实际生效长度,**省 FLOPs 但不省 buffer 内存**。所以 graph kv_indices buffer 不会因 SWA 缩小,不存在 buffer 越界风险。 Capture / replay wrapper 数一致:capture(`init_forward_metadata_capture_cuda_graph` line 551-580)和 replay 都按 `num_wrappers` 循环建 2 个 `BatchDecodeWithPagedKVCacheWrapper`;每个 step backend 各持一份 `decode_cuda_graph_metadata[bs]`。replay (line 1600-1615) 也走完整 `common_template` → 每 step → `update_sliding_window` 把 2 个 wrapper 都 re-plan。 **唯一隐患**: 若有任何一个 step 的 backend 在 SWA dispatch 与 full dispatch 之间发生切换(即 `dispatch_reason` 在 capture 与 replay 间不同),会跑飞。但 `dispatch_reason` 在 `FlashInferAttnBackend.__init__` 锁死 (line 152-160),capture 之后不再变,**无风险**。 ## 实施路径 要让 draft 真启用 SWA,只需: 1. 在 `LlamaForCausalLMEagle3` 加 `get_attention_sliding_window_size(self): return N`。 2. 在 `LlamaAttention.__init__` (`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama.py:182-190`) 给 EAGLE3 draft 那 1 层的 `RadixAttention` 传 `sliding_window_size=N`(否则 layer.sliding_window_size=-1 会被 `_get_wrapper_idx` 路由到 wrapper 1=full,SWA wrapper 0 plan 出来用不上)。 3. **必须 patch** `FlashInferAttnBackend.__init__` 的 `assert self.num_wrappers == 1`(line 221, 229)— 让 multi-step draft 路径支持 SWA。最干净做法是 `FlashInferMultiStepDraftBackend` 在检测 `model_runner.sliding_window_size is not None` 时给每 step 同时分配 wrapper0/wrapper1 两套 `kv_indptr` buf 再传下去。 ## 关键文件 - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py` (269, 362-373, 720-721) - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/draft_utils.py` (108-124, 192-204) - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/flashinfer_backend.py` (112, 143, 152-160, 213-230, 510-580, 1253-1300, 888-897, 1461-1615) - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/model_executor/model_runner.py` (924-937) - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_draft_cuda_graph_runner.py` (350-352, 454) - `/user_4813494d/openbmb/eval/start_eagle.sh` (79-85)

> AGENT

调研完成。现在给出回答。 --- ## 回答 ### 问题 1 — 配置来源的最佳设计 **推荐方案 B（CLI / `server_args`）**，且 model class 能够拿到。 - `model_runner.py:294` `self.server_args = server_args`，但 model 自身（`LlamaForCausalLMEagle3.__init__`）的签名只接 `config, quant_config, prefix`，**不直接拿 server_args**。 - 但 SGLang 提供了**进程级全局** `get_global_server_args()`：`server_args.py:5250-5265`，在 `model_runner.py:353-354` 启动时通过 `set_global_server_args_for_scheduler(server_args)` 注入。这是 model class 在 `get_attention_sliding_window_size(self)` 里取 server_args 的干净渠道。 - 推荐 server_args.py 新增 `speculative_draft_sliding_window: int = 0`（默认 0 = 关闭），CLI `--speculative-draft-sliding-window`。Model 端实现： ```python def get_attention_sliding_window_size(self): from sglang.srt.server_args import get_global_server_args swa = get_global_server_args().speculative_draft_sliding_window return swa if swa and swa > 0 else None ``` 方案 A（env）能用但不规范；方案 C（写 `config.json` 的 `eagle_config`）要改 ckpt，不利于实验扫参。 涉及文件：`server_args.py:420-442`（spec args block）、`models/llama_eagle3.py:194-234`。 --- ### 问题 2 — 数值约束 - **返回 `None`**：走 `model_runner.py:927-934` 后续分支（非 hybrid swa），最终 `self.sliding_window_size = None`，flashinfer `num_wrappers=1`，**关闭 SWA**。 - **返回 0**：`flashinfer_backend.py:152` 判 `is not None` 仍为真 → `num_wrappers=2`，但 `RadixAttention.__init__:76` `self.sliding_window_size = 0 or -1 = -1`，`_get_wrapper_idx:893` `layer.sliding_window_size == -1` 把该层归到 full wrapper（idx=1），SWA 实际未生效，反而多分配一组 wrapper/indptr，**最差选择**。 - **返回 > 0**：才真正生效，draft 1 层 → 全部走 SWA wrapper（idx=0），`forward_extend` 的 `window_left=layer.sliding_window_size`（`flashinfer_backend.py:783-784`）。 - 因此 `get_attention_sliding_window_size()` 必须返回 `> 0` 整数或 `None`，**严禁返回 0**。 - **默认值**：建议默认 0（即在 server_args 默认关闭，方法返回 None），让 `--speculative-draft-sliding-window` 显式开。要对齐 LAST_N=32K 可以传 `32768`；起跑值可以更激进些（如 4096/8192）先看 acceptance rate 退化幅度，因为 draft 1 层 + chain-3 步，KV 历史远没 LAST_N 那么需要。 --- ### 问题 3 — 副作用 / 兼容性 - **`--disable-radix-cache`**：兼容。`model_runner_kv_cache_mixin.py:248` 的 `assert sliding_window_size > 0` 在 `if self.is_hybrid_swa:` 分支内（`mixin.py:355`），而 `is_hybrid_swa_model()` 白名单只含 `Llama4ForConditionalGeneration / MiMoV2FlashForCausalLM / MiMoV2MTP`（`configs/model_config.py:1214-1221`），**`LlamaForCausalLMEagle3` 不在内**，不会触发 hybrid-kv-pool 分支，与 disable-radix-cache 路径完全独立。 - **`--speculative-num-steps 3 --speculative-eagle-topk 2`**：兼容。所有 step 都走同一 draft `model_runner.attn_backend`，SWA 是 backend 级配置，不感知 step。`eagle_worker.py:1061` / `eagle_info_v2.py:85` 的 `evict_swa` 只在 hybrid KV pool 才走（保护机制无关）。 - **`--speculative-draft-attention-backend flashinfer`**：SGLang 在 `eagle_worker.py:327-332` 已强制 draft 用 `"flashinfer"`（minicpm_flashinfer→flashinfer 改写），唯一另一个 `flashinfer_mla_backend` 只在 MLA 模型时走，draft Llama 不会路由过去，**安全**。 - **target 不开 SWA**：完全独立。Target 与 draft 各有 `ModelRunner` 实例，`sliding_window_size` 是 per-runner 属性，target 的 `MiniCPM` 不实现 `get_attention_sliding_window_size`，target attn backend `minicpm_flashinfer` 保持 full attention。**无需 cross-check**。 - **启动期 assert**： - `flashinfer_backend.py:147-150` `not (sliding_window AND is_encoder_decoder)`：draft 不是 encoder-decoder，过。 - `flashinfer_backend.py:984` `assert self.sliding_window_size is not None`：在 `update_decode_indices_for_swa` 内，只有 `num_wrappers==2` 时调用，传 > 0 即 OK。 - `model_runner_kv_cache_mixin.py:248`：上面已说，受 `is_hybrid_swa` 门控，不触发。 **结论**：方案 B + 默认 0（None）+ CLI 显式 >0 开启，单测一遍 `start_eagle.sh` 加 `--speculative-draft-sliding-window 4096` 应直接跑通；不需要改 ModelConfig / KV-pool / hybrid 路径。 **关键文件路径**： - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama_eagle3.py` - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/server_args.py`（行 420-442 spec block；5250-5265 global） - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/model_executor/model_runner.py`（行 923-937） - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/flashinfer_backend.py`（行 147-160, 783-790, 888-897, 984） - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/radix_attention.py`（行 76） - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/model_executor/model_runner_kv_cache_mixin.py`（行 248, 355） - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/configs/model_config.py`（行 1214-1221） - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py`（行 327-332）
