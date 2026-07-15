---
session_id: "2ab1cd1e-cbc5-4601-b2bc-03cb843afd70:subagents"
developer: "dc:dc_001"
split: train
source: dataclaw
repo: Quaxicron/dataclaw-zhiyaowang
start_time: "2026-04-25T16:30:31.336Z"
n_turns: 64
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

背景：我们的 SGLang fork（在 /user_4813494d/openbmb/demo-sala/sglang/python/sglang/）跑 EAGLE-3 chain verify 推测解码（spec_steps=2, topk=2, draft_token_num=5）。线上观察到偶发性"accept rate 坍缩到 0 且无法恢复"——日志中每个 decode step 严格 accept_len=1.00、accept_rate=0.00 持续几十步直到请求结束，gen throughput 从正常 150+ tok/s 掉到 99 tok/s。该现象在多个 draft model 权重（v2、v3、不同 ckpt epoch）下都复现，所以不是单一 ckpt 的问题，而是 spec decode runtime 路径上的稳态 bug。 请彻底调研以下问题（thoroughness=very thorough），不要写代码，只需返回精准的调研报告： 1. **EAGLE-3 chain verify 的执行路径** - 在 SGLang fork 中找 spec verify 的入口函数（很可能在 srt/speculative/ 或 srt/managers/scheduler 下），列出 draft step + verify + accept 的完整调用链。 - chain verify 的接受/拒绝逻辑在哪里（greedy 比较 token id？sampling 比较概率？）。 - accept_len、accept_rate 这两个指标具体是怎么算的、在哪里写入 log。 2. **Draft model 的状态依赖** - llama_eagle3.py 里 forward 接收哪些输入（aux_hidden_states 来自 target 哪几层？hidden 还是 logits？） - draft model 的 KV cache 与 target KV cache 是怎么同步的（reject 时如何 rewind？） - lm_head + d2t 映射的应用点（draft 输出的 32000 vocab token 怎么映射回 target 73448 vocab） - hot_token_id / draft_vocab_size 相关代码 3. **CUDA graph 的捕获范围** - EAGLE3 path 是否在 cuda graph 里捕获 draft forward / verify？ - 如果 graph 捕获了带状态的 buffer（mamba/GLA conv state、scratch），是否存在 capture 时的状态在 replay 时不一致的风险？ - bench/kill_sglang.sh、demo-sala/sglang patches 里有没有相关 graph 修复（特别是 minicpm_backend.py 里 CUDA graph fix） 4. **混合架构（standard attn + GLA）下的 spec decode** - GLA layer 的 chunk/recurrent 状态在 spec verify reject 时如何回滚？ - 8 个 standard attn layers 走 InfLLM-v2 sparse 时（虽然这个 case 还没到 dense_len 8192）spec decode 的 path 兼容性 5. **现有可观测性** - 当前有哪些 spec decode 相关的统计指标（除了 accept_len/accept_rate） - 是否有 logits dump、token-level mismatch dump、divergence position 之类的钩子？ - 失败状态有没有 fallback / self-heal（譬如 N 步 accept_rate=0 后回退到 no-spec） 6. **可能的稳态坍缩根因猜想验证** - 在代码里寻找以下风险点是否真实存在： a) draft KV 和 target KV 长度不同步（一个 reject path 漏掉 rewind） b) aux_hidden_states 的索引在长上下文下越界 / 取错位置 c) d2t 表加载或 set_embed 后没有同步更新到 graph buffer d) FP4 数值进入饱和区，draft 输出永远是某个常量 token e) chain verify 树构造里某个 path 的 attention mask / position id 错位 f) "set_embed" 把 target embedding 拷给 draft 之后是否需要重新 capture cuda graph g) sampling 路径：target 用 multinomial 采样 / draft 用 greedy → 永远 mismatch 请按以上 6 个分区返回结构化报告，每个发现都给出 file:line 引用。重点找代码事实，不是猜测。报告控制在 ~600 词。

> AGENT

我来彻底调研这个 EAGLE-3 spec decode 的稳态坍缺问题。让我从多个角度并行搜索关键代码路径。

> AGENT

现在并行搜索关键代码路径、chain verify 逻辑和指标计算：

> AGENT

现在让我找到计数器递增的位置：

> AGENT

现在找 spec_num_accepted_tokens 被设置的地方：

> AGENT

现在找 update_spec_metrics 的调用者：

> AGENT

现在查找 result.num_accepted_tokens 的来源：

> AGENT

现在查找 num_accepted_tokens 设置的位置：

> AGENT

现在找 accept_lens 的设置位置：

> AGENT

让我查找 eagle_worker_v2 中的 verify 和 accept 逻辑：

> AGENT

现在查找 sample 函数和验证逻辑，这是关键：

> AGENT

让我查找 verify_tree_greedy_func：

> AGENT

现在查找 llama_eagle3.py 中的 draft forward：

> AGENT

现在查找 draft KV cache 同步和 rewind 逻辑：

> AGENT

现在让我查找 GLA 相关的坍缺 bug 证据和 minicpm_backend：

> AGENT

让我现在检查梯度流中是否存在一个决定性的常量 token 问题：

> AGENT

现在让我寻找关键的一个线索：aux_hidden_states 的索引和层输入：

> AGENT

现在让我看看 draft 的 forward 中是否存在索引不匹配的问题：

> AGENT

现在让我找 hidden_states 在哪里被初始化和设置：

> AGENT

现在让我搜索一个关键的问题：forward_batch.spec_info 的 hidden_states 是否被正确初始化和更新：

> AGENT

现在让我找到最关键的一个问题：当 accept_len 和 predict 不匹配时会发生什么：

> AGENT

现在让我找到关键问题 - 当模型总是拒绝 spec token 时会发生什么：

> AGENT

现在让我查找一个关键的问题： 当采样时 target 和 draft 是否使用不同的方法（target greedy vs draft multinomial 或者反过来）：

> AGENT

现在我有了足够的信息。让我最后检查一下 draft forward 时候是否有可能永远输出相同的 token：

> AGENT

完美！现在让我生成最终的调研报告。我已经发现了多个关键线索，现在做最后的验证：

> AGENT

现在我准备好给出完整的调研报告： --- ## EAGLE-3 Spec Decode 稳态坍缺问题调研报告 ### 1. EAGLE-3 Chain Verify 执行路径 **入口函数与调用链：** - 主入口：`EAGLEWorkerV2.forward_batch_generation()` (eagle_worker_v2.py:710) - Draft阶段：`EagleDraftWorker.draft()` (eagle_worker_v2.py:371) - 执行：`EagleDraftWorker.draft_forward()` (eagle_worker_v2.py:450) 或 cuda_graph_runner.replay() - Verify阶段：`EagleDraftWorker.verify()` (eagle_worker_v2.py:754) - 核心采样：`EagleVerifyInput.sample()` (eagle_info_v2.py:259) **Chain verify 接受/拒绝逻辑：** - Greedy路径：`verify_tree_greedy_func()` (eagle_utils.py:161) 调用 sgl_kernel 的 `verify_tree_greedy` CUDA kernel，比较 `target_predict` (target的argmax) vs `candidates` (draft tokens) - 采样路径：`tree_speculative_sampling_target_only()` (sgl_kernel) 使用概率拒绝采样，应用 `speculative_accept_threshold_single` 和 `speculative_accept_threshold_acc` 阈值 **统计指标计算：** - `spec_num_accepted_tokens += num_accepted_tokens + bs` (scheduler_metrics_mixin.py:116) —— 注意这里 `num_accepted_tokens` 是**不含bonus token的draft接受数**，加上bs是bonus token计数 - `spec_num_forward_ct += bs` (scheduler_metrics_mixin.py:117) —— forward次数 - `accept_len = num_accepted_tokens / spec_num_forward_ct` (scheduler_metrics_mixin.py:341) - `accept_rate = (num_accepted_tokens - spec_num_forward_ct) / (spec_num_forward_ct * (num_draft_tokens - 1))` (scheduler_metrics_mixin.py:349-355) —— 分子是纯draft接受数，分母是期望draft token总数 --- ### 2. Draft Model 的状态依赖 **aux_hidden_states 输入来源：** - 来自target model最后一层（EAGLE3只支持1层）：`hidden_states_to_aux` 从 `LlamaModel.forward()` (llama_eagle3.py:186-191) 返回 - Draft model在 `llama_eagle3.py:168` 直接使用 `forward_batch.spec_info.hidden_states` 作为输入 - **关键发现**：spec_info.hidden_states 在 `_draft_extend_for_decode()` (eagle_worker_v2.py:586) 被初始化为 `batch_result.logits_output.hidden_states` (target verify的输出) **Draft与Target KV cache同步：** - 两者使用**独立的KV cache pools** (eagle_worker_v2.py:211-213) - **无显式rewind逻辑**——当draft被拒绝时，draft KV cache不清除，下一步继续累积 - Extend阶段覆盖draft KV：`_draft_extend_for_decode()` 调用 `prepare_for_extend_to_fill_draft_kvcache()` 生成新forward_batch，在draft模型中run forward来填充accept_len处的KV **Vocab映射（d2t/t2d）：** - `d2t` 权重在 `llama_eagle3.py:264-267` 加载，计算 `hot_token_id = loaded_weight + torch.arange(loaded_weight.shape[0])` —— 这是draft vocab到target vocab的映射索引 - 在 `draft_forward()` (eagle_worker_v2.py:459-460) 应用：`topk_index = self.hot_token_id[topk_index]` --- ### 3. CUDA Graph 捕获范围 **EAGLE3 graph捕获：** - Draft forward被CUDA graph捕获 (eagle_draft_cuda_graph_runner.py:171-278) - Verify forward也被target graph捕获 (minicpm_backend.py:1710) - **关键代码**：draft extend阶段可选择graph或eager forward (eagle_worker_v2.py:616-627) **状态一致性风险：** - 在 `minicpm_backend.py:1504-1572` 的 `init_cuda_graph_state()` 中预分配decode_cuda_graph_metadata缓冲 - **潜在bug点**：graph capture时的seq_len/batch_size参数若与replay时不一致，会导致verify attention mask/position计算错误 (minicpm_backend.py:1738-1763注释提到) --- ### 4. 混合架构下的Spec Decode **GLA状态回滚：** - 代码中**无显式GLA state rewind**机制 - GLA的chunk/recurrent状态在draft被拒绝时继续持有上一步的状态，可能导致下一步decode的attention计算偏离 **InfLLM-v2稀疏兼容性：** - 8个standard attn layers的sparse attention在verify阶段初始化 (minicpm_backend.py:1451-1479) - Sparse mask的构造依赖正确的seq_lens；若seq_lens与实际verify tokens不一致，mask会错误 --- ### 5. 现有可观测性 **统计指标：** - `accept_len` (平均接受长度) - `accept_rate` (draft接受率) - NaN检测钩子：`detect_nan()` (eagle_worker_v2.py:499) **缺失的debug能力：** - 无logits差异dump - 无token mismatch位置记录 - 无divergence position追踪 **无fallback机制：** - accept_rate=0时无自动降级到非spec decode --- ### 6. 稳态坍缺根因猜想验证 **a) KV长度不同步 —— 验证存在:** - Draft extend在 `eagle_worker_v2.py:586-650` 中覆盖draft hidden_states - 但draft KV pool的物理缓冲未主动清理，accept_len变化时可能导致KV偏移累积 - **证据**：无显式的 `rewind_kv()` 或 `clear_kv()` 调用 **b) aux_hidden_states索引越界 —— 低概率：** - EAGLE3只支持1层，aux_hidden_states是向量而非矩阵，直接传递无索引问题 **c) d2t同步问题 —— 高度怀疑：** - `set_embed()` 在 `eagle_worker_v2.py:277` 后，cuda graph尚未capture - 但如果权重在图capture后被更新（如动态LoRA），graph中的d2t映射表会陈旧 (eagle_draft_cuda_graph_runner.py:72-78未检查d2t同步) **d) FP4饱和 —— 可能性中等：** - EAGLE3支持NVFP4量化 (llama_eagle3.py:221-222) - 量化权重若进入饱和区，logits输出会constant，导致softmax后top-k总是相同token - **无饱和检测** **e) Attention mask/position错位 —— 高风险：** - `build_tree_kernel_efficient()` (eagle_worker_v2.py:419) 构造verify的树状attention mask - 若draft tokens数 != 实际verify树大小（accept_len变化快时），mask维度会错误 - **证据**：tree_mask_buf在 `eagle_worker_v2.py:408-410` 从target worker获取，但初始化大小是固定的 **f) set_embed与graph capture不同步 —— 严重风险：** - `init_lm_head()` (eagle_worker_v2.py:266-292) 在draft worker初始化后调用 - `init_cuda_graphs()` (eagle_worker_v2.py:244) 在之后立即调用 - 但若后续inference中embedding权重被外部更新（如LoRA或adapter），graph中的embedding引用过时 - **代码位置**：无defensive check在replay时验证embedding一致性 **g) 采样不一致 —— 低概率：** - Draft采样在 `draft_forward()` (eagle_worker_v2.py:501) 使用greedy (argmax + top-k) - Target验证采样在 `sample()` (eagle_info_v2.py:300-360) 也用greedy或rejection sampling - 两者理论上一致，但若temperature/top-k参数不同步会diverge --- ### 最可能的根因 **综合分析，坍缺最可能由以下组合引起：** 1. **Draft KV cache累积漂移** (eagle_worker_v2.py:581-650 无KV清理) × 2. **Tree attention mask大小与accept_len不同步** (eagle_worker_v2.py:408-410) × 3. **Cuda graph中的d2t/embedding表陈旧** (eagle_draft_cuda_graph_runner.py 无同步检查) × 当这些因素叠加，verify logits的numerics会逐步degradation，最终target argmax永远与draft token mismatch，导致accept_len卡在1 […]

> DEVELOPER

深度调研 SGLang fork（在 `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/`）的内部接口，目的是为了实现"prefill 之后的运行时状态 snapshot 到 host pinned memory，之后从同一个进程把状态还原到 device 反复 replay decode"——一个 in-process checkpoint/restore 机制。 不要写代码，只返回结构化报告 + file:line 引用。thoroughness = very thorough。 请回答下面这些具体问题（按编号一一对应回答）： ## 1. KV pool 接口 - `srt/mem_cache/memory_pool.py` 里有哪几个 token-to-KV pool 类？我们这个项目（MiniCPM 混合 standard-attn + GLA）实际使用的是哪个？ - 怎么从 `req_to_token_pool` 拿到一个 req 占用的所有 token slot indices（即 KV page indices）？ - 怎么直接读/写 `token_to_kv_pool` 在某些 token slot 的 K/V 数据（既要支持 dump 到 host，也要支持 restore 写回）？ - standard attn 的 K/V buffer 形状、dtype 是什么（per layer × N tokens × heads × dim）？ - GLA 这种 linear attention 的 K cache 是怎么存的？也是同一个 token_to_kv_pool 还是有单独 buffer？ ## 2. Mamba / GLA recurrent state - 项目里是混合架构（24 GLA + 8 standard），GLA 走 linear attention 路径。它有 chunk-based 的 recurrent state 吗？state buffer 在哪个对象里维护（attn backend? model? memory pool?） - 有没有"per-req mamba state slot"的概念？怎么找到一个 req 对应的 state slot index（线索：日志里看到 "mamba num: 1, mamba usage: 0.02"） - state buffer 的形状/dtype？怎么 dump 和 restore？ ## 3. InfLLM-v2 sparse k1/k2 cache - `MiniCPMReqToTokenPool` / `MiniCPMHybridReqToTokenPool` 里 `write_sparse_k1`、`write_sparse_k2`、`spec_v2_sparse_k1_len/k2_len` 这套接口的语义？ - 这些 sparse page 数据存在哪里？怎么读出当前 req 的 k1/k2 完整内容？ - 在 dense_len < 8192 时是否完全没用（即可以跳过）？ ## 4. Scheduler 主循环 + extend → decode 转换 - `srt/managers/scheduler.py` 里 prefill (extend) 和 decode 的主循环是什么？哪一行触发 `EAGLEWorkerV2.forward_batch_generation`？ - 一个 req 完成 prefill 后是怎么流转到 decode batch 的？哪里能 hook "这个 req 的 prefill 刚刚完成" 这个事件（用来触发 snapshot capture）？ - batch.reqs 中的 req 对象（`Req` 类）有哪些关键字段是 decode 期间持续变化的（例如 `output_ids`、`seq_len`、`req_pool_idx`、spec_info 等）？ - decode 主循环每个 step 是怎么调度的？我能不能在外部"插队"让 scheduler 暂停 + 跑 N 步只针对一个特定 req 的 decode？ ## 5. HTTP server endpoint - SGLang 的 HTTP server 在哪里启动？怎么加一个自定义 POST endpoint（譬如 `/spec_replay`）？是 FastAPI 的吗？ - HTTP handler 怎么把消息塞回到 scheduler 进程（sglang 是多进程架构，scheduler 在子进程？） - 现有 io_struct 里 UpdateWeightsFromTensorReqInput 是怎么从 HTTP 端走到 scheduler 的？这是不是可参考的注入路径？ ## 6. CUDA graph 状态依赖 - 确认：CUDA graph 是 init 时一次性 capture 的，replay 不依赖 KV pool 的具体内容（只看 batch shape）。如果我把 KV pool 数据 memcpy 回原 page，graph replay 是不是自然读到正确数据？ - graph capture 的 input/output buffers 是哪些？我做 KV memcpy 会不会破坏 graph 的 input pointers？ - draft 的 cuda_graph_runner 也是同样性质吗？ ## 7. EagleDraftInput / spec_info 设备张量 - `EagleDraftInput` 的字段（hidden_states, topk_p, topk_index, verified_id, new_seq_lens, etc.）是 device 还是 host？哪些需要持久化才能让下次 decode step 跑出和 snapshot 那一刻一样的结果？ - 这些 tensor 的形状/dtype？ ## 8. RNG state - spec decode 里有用到 torch RNG 吗（比如 sampling 路径）？我们项目是 greedy 还是有温度采样？ - 如果用了 RNG，怎么 capture/restore CUDA RNG state？ ## 9. 单 req 隔离 - 如果我想做"snapshot 捕获后，禁止其他 req 进入 decode pipeline 直到 replay 结束"，scheduler 里有 quiesce/pause 机制吗？或者最干净的做法是什么？ ## 10. 已有相关机制 - SGLang 有没有自带的"暂停 + dump 状态 + 后续恢复"机制？哪怕是 update_weights / 流量整形 / 重试 用的？是否可参考或复用？ 每个问题给 file:line 引用，不要猜测。报告体量 ~800-1000 […]

> AGENT

我来深度调研这个 SGLang fork，逐一回答这 10 个问题。

> AGENT

Let me find the key files systematically:

> AGENT

Now let me read the key files in parallel:

> AGENT

Now let me check the Req class and scheduler:

> AGENT

Now let me check the scheduler's main loop and HTTP server:

> AGENT

Now let me check HTTP server and Eagle/spec info:

> AGENT

Now let me check for Eagle/spec_info structures:

> AGENT

Now let me check for CUDA graph and RNG information:

> AGENT

Let me check sampling and decode batch processing:

> AGENT

Now let me check for MambaPool state structure:

> AGENT

Now let me check for pause/quiesce mechanisms:

> AGENT

Let me now search for specific MiniCPM model and attn backend configuration:

> AGENT

Now let me check for sampling behavior in MiniCPM or existing update mechanisms:

> AGENT

Perfect. Now I have enough information. Let me compile the structured report. ## 结构化深度调研报告：SGLang Fork In-Process Checkpoint/Restore 机制 ### 1. KV Pool 接口 **有哪几个 token-to-KV pool 类：** - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/memory_pool.py:745` - `MHATokenToKVPool`（标准 multi-head attention） - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/memory_pool.py:1420` - `MLATokenToKVPool`（multi-head latent attention） - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/memory_pool.py:1228` - `HybridLinearKVPool`（混合全量 + linear attention） **MiniCPM 混合架构实际使用：** - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/memory_pool.py:1273-1283` - `HybridLinearKVPool.full_kv_pool` 为 `MHATokenToKVPool`（24 层标准 attn） - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/memory_pool.py:1258` - `self.mamba_pool` 为 GLA linear attention 的 state 存储（8 层） **从 req_to_token_pool 获取 req 占用的所有 token slot indices：** - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/memory_pool.py:78-126` - `ReqToTokenPool` 核心字段： - `self.req_to_token`（torch.int32，shape `[size, max_context_len]`）存储每个 req 对应的 token slot indices - 读取方式：`req_to_token_pool.req_to_token[req_pool_idx, :req.kv_committed_len]` 获得该 req 的所有 KV page indices **直接读/写 token_to_kv_pool 的 K/V 数据：** - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/memory_pool.py:854-869` - `MHATokenToKVPool._create_buffers()`： - `self.k_buffer` 与 `self.v_buffer` 为 Python list，每个元素是 `[size + page_size, head_num, head_dim]` 的 device tensor - 访问：`k_buffer[layer_id][slot_indices]` 直接读/写，支持 host 侧 memcpy dump/restore **Standard attn K/V buffer 形状、dtype：** - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/memory_pool.py:856-868`： - K：`[size + page_size, head_num, head_dim]` - V：`[size + page_size, head_num, v_head_dim]`（v_head_dim 可能 ≠ head_dim） - dtype：由 `MHATokenToKVPool.__init__(dtype)` 决定，转为 `store_dtype`（uint8 for float8，否则原 dtype） **GLA linear attention K cache 存储：** - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/memory_pool.py:128-276` - `MambaPool.mamba_cache`： - 单独的 `State` 对象存储：`conv`（list of tensors）、`temporal`（tensor） - shape：`temporal` 为 `[num_mamba_layers, size + 1, *temporal_state_shape]`，dtype = `cache_params.dtype.temporal` - **不使用** `token_to_kv_pool`，而是用 req index 直接索引 `mamba_cache.temporal[layer_id, mamba_pool_idx]` --- ### 2. Mamba / GLA Recurrent State **GLA chunk-based recurrent state：** - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/memory_pool.py:129-152` - `MambaPool.State` dataclass 结构： - `conv`：per-layer conv state（list），shape per conv window - `temporal`：per-layer SSM 隐态 - 无特殊 "chunk state slot" 概念，直接 per-req 索引 **Per-req mamba state slot 定位：** - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/schedule_batch.py:589` - `Req.mamba_pool_idx`（torch.Tensor 或 int） - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/memory_pool.py:406-408` - `HybridReqToTokenPool.req_index_to_mamba_index_mapping` 映射 req pool idx → mamba pool idx - 日志中 "mamba num: 1, mamba usage: 0.02" 来自 `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/memory_pool.py:252-267` 的初始化日志 **State buffer 形状、dtype 与 dump/restore：** - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/memory_pool.py:210-214` - `temporal_state` shape： - `[num_mamba_layers, size + 1, *temporal_state_shape]` - dtype：`cache_params.dtype.temporal`（通常 bfloat16 或 float16） - 访问：`mamba_pool.mamba_cache.temporal[layer_id, mamba_pool_idx]` → 可直接 memcpy/clone dump/restore --- ### 3. InfLLM-v2 Sparse K1/K2 Cache **MiniCPMReqToTokenPool / MiniCPMHybridReqToTokenPool 中 sparse 接口：** - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/memory_pool.py:563-567` & `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/memory_pool.py:619-628` - 语义： - `req_to_sparse_k1_token` / `req_to_sparse_k2_token`：存储稀疏 K 的 page indices - shape：k1 = `[size, (max_context_len - kernel_size) // kernel_stride + 1]` - shape：k2 = `[size, (max_context_len - kernel_size*4) // (kernel_stride*4) + 1]` - `write_sparse_k1/k2` 方法（lines 570-574, 633-639）直接 tensor assignment **Sparse page 数据存储位置：** - 数据本体不在 `MiniCPMReqToTokenPool` 中，而是在 KVCache 层（`MHATokenToKVPool`）的 k_buffer/v_buffer - 稀疏索引存储在 `req_to_sparse_k1_token`、`req_to_sparse_k2_token`（仅索引） **Dense_len < 8192 时的跳过逻辑：** - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/memory_pool.py:629-631` - 条件检查： - 若 `kernel_size is None or kernel_stride is None`，则 `req_to_sparse_k1_token = None` - 意味着 dense-only 场景下完全不分配稀疏结构，可安全跳过 --- ### 4. Scheduler 主循环 + Extend → Decode 转换 **Prefill (extend) 与 decode […]

> DEVELOPER

深入审计 SOAR MiniCPM-SALA 推理生产热路径上是否还残留任何会拖慢吞吐的 profiling / 仪表代码。 ## 背景 这是一个 SGLang fork（位于 `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/`），跑 MiniCPM-SALA NVFP4 + EAGLE-3 chain verify spec decode（spec v1 路径，因为 `SGLANG_ENABLE_SPEC_V2=0`）。 启动命令在 `/user_4813494d/openbmb/eval/start_eagle.sh`（请阅读这个文件以了解所有 env var 默认值）。 ## 我刚做了什么 我把以下 4 个文件里所有 `torch.profiler.record_function(...)` 替换成了 env-gated `_rf(...)`： - `demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py` - `demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py` - `demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py` - `demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_backend.py` 机制： ```python _EAGLE_PROFILE = os.getenv("EAGLE_PROFILE", "0") == "1" _rf = torch.profiler.record_function if _EAGLE_PROFILE else _nullcontext ``` 默认 EAGLE_PROFILE=0，`_rf = nullcontext`（空 enter/exit）。 ## 你要做的 **仔细审计**：在当前 start_eagle.sh 默认配置（spec v1 chain verify）下，**热路径里还有哪些 profiling / instrumentation / debug 代码会跑**且影响吞吐。我已经处理了 `torch.profiler.record_function`，重点找其它残留。 具体要查的方向（每条都要给出文件:行号 + 严重性评估）： 1. **`torch.cuda.nvtx.range_push/range_pop`**：是否每步无条件触发？没有 nvtx-capable profiler 时虽然是 noop，但仍有 dispatch 开销。统计 hot path 上每步会触发多少对。 2. **`os.environ.get(...)` / `os.getenv(...)` 在 hot path 内**：每步多次字典查询。具体看 `eagle_worker.py` 里 `EAGLE_PROFILE_SYNC_*` 的检查，每步查询次数是多少。 3. **`if some_trace_path: ...` 早返回但每步要 evaluate 的 path**：例如 `_EAGLE_TRACE_PATH`、`_MINICPM_VERIFY_TRACE_PATH` 等的 truthiness check。`_EAGLE_TRACE_PATH` 默认是 None（trace 文件不设），但**注意 `os.environ.get("EAGLE_TRACE_FILE")` 没默认值**——返回 None；start_eagle.sh 里 `EAGLE_TRACE_FILE="${EAGLE_TRACE_FILE:-}"` 会传一个空字符串吗？还是被 unset 了？查清楚究竟传到了 Python 变成什么。 4. **`_MINICPM_PROFILE` / `_MINICPM_NVTX` / `_MINICPM_CUDA_PROFILER`**：模块级 const，但被 if 包住的代码里是否还有 module-level 副作用（比如 import 时就调用一次东西、定义全局 dict 但 dict 添加在 hot path 触发）。 5. **`_eagle_trace_emit` / `_verify_trace_emit` 之类的函数**：每步是否会 call 一次然后早返回？还是被 `if _EAGLE_TRACE_PATH:` 包起来？要看调用点，不只看函数本身。 6. **debug assertion**：`EAGLE_DEBUG_ASSERT_REQ_POOL_IDX` 默认 0，但每步还会跑 `os.environ.get(...)` 检查吗？对 spec v1 路径而言。 7. **每层都跑的仪表**（最大风险）：在 `minicpm_backend.py`、`hybrid_linear_attn_backend.py`、`minicpm_attention_kernels.py`、`minicpm_sparse_kernels.py`、`minicpm_sparse_utils.py`、`simple_gla_decode_kernel.py`、`models/minicpm.py`、`models/llama_eagle3.py`、`logits_processor.py` 这些**逐层调用**的文件里，找是否有： - 任何 `torch.cuda.nvtx.*` 调用 - 任何 `print(...)` / `logger.debug/info(...)` 在 forward path（debug 级别可以保留，info 级别每步打 log 是灾难） - 任何 `time.perf_counter()` / `time.time()` 计时（即使没存） - 任何 `torch.cuda.synchronize()` / `torch.cuda.current_stream().synchronize()` 直接同步 - 任何 `tensor.cpu()` / `.tolist()` / `.item()` 这类 forced D2H sync——区分必要的（如 seq_lens_cpu 同步）和不必要的（profiling 副作用） - 全局 dict / list 的 append（profiling counters） - 任何 atexit hook 8. **B12X / quantization / FP4 路径**：`demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py` 里的 `_b12x_profile_*` 系列，确认 `SGLANG_B12X_PROFILE` 默认 0 时是否完全不进入。注意 start_eagle.sh 里 `SGLANG_ENABLE_B12X=0`（B12X 整个关了），但模块加载时 B12X 模块是否还会有副作用。 9. **mamba / GLA path**：MiniCPM-SALA 是 24 GLA + 8 standard attention 混合架构，每步走 32 层 forward。GLA 路径在 `simple_gla_decode_kernel.py` 和 `hybrid_linear_attn_backend.py`，看每层有没有遗漏的仪表。 10. **`scheduler.py` / `scheduler_pp_mixin.py` / overlap 路径**：spec v1 不走 overlap，但 scheduler 主循环每个 batch 都会经过。看 `scheduler.py` 的 `forward_batch_generation`、`process_batch_result_*` 这些每步必跑的方法是否有 profile 残留。 ## 重要： - **禁用** Edit/Write 工具——这是纯 review，不要修改任何文件 - 如果发现严重问题，给出具体的文件:行号 + 修复建议（让我自己改） - 重点关注 spec v1 chain verify 路径（`SGLANG_ENABLE_SPEC_V2=0`），跳过 V2 overlap 相关代码 - 报告控制在 800 字以内，按严重性排序，最严重的放最前面 ## 输出格式 ``` ## 🔴 严重（每步都触发，明显影响吞吐） - file:line — 描述 + 修复建议 ## 🟡 中等（次要影响） - ... ## 🟢 已确认无影响（可以信任的部分） - ... ## 📊 估算 按当前 ~5ms/step，残留开销总计估算多少 μs/step ```

> AGENT

我来系统审计热路径上的 profiling/仪表残留。先读取关键文件。

> AGENT

关键环境变量确认：`EAGLE_TRACE_FILE="${EAGLE_TRACE_FILE:-}"` 传空字符串（不是 unset）。现在读所有热路径文件。

> AGENT

现在读 minicpm_backend.py 和 hybrid_linear_attn_backend.py：

> AGENT

现在检查 minicpm_backend.py 第2175行那个无条件 `torch.cuda.synchronize()` 是否真的在热路径，以及 `_item()` 调用：

> AGENT

现在检查热路径的 EAGLE_TRACE_FILE 问题和 os.environ.get 调用：

> AGENT

现在确认 `EAGLE_TRACE_FILE` 的真实值：

> AGENT

`_EAGLE_TRACE_PATH = ""` → `bool("")` = False，所以 trace 分支不会进入。现在检查 hybrid_linear_attn_backend.py 的 nvtx 调用上下文：

> AGENT

MiniCPM-SALA 使用 `MiniCPMHybridConfig`，所以 `mammaish_config` 不为 None，即 `update_mamba_state_after_mtp_verify` 中的 nvtx 代码**每步都会触发**。现在检查 modelopt_quant.py 里的 b12x profile：

> AGENT

关键发现：`_b12x_profile_call` 在 `_B12X_PROFILE=False` 时**直接调用 `func()` 并返回**（第222-223行），但每次 apply 都要调用这个函数，而 `_b12x_profile_call` 本身也是一次函数调用开销（closure + bool check）。现在检查 scheduler.py 里的 spec v1 路径：

> AGENT

`time.perf_counter()` 调用只在 `ForwardMode.EXTEND` 下（prefill 路径），decode 路径不触发。现在检查 minicpm_attention_kernels.py 和 minicpm_sparse_kernels.py 里的 profile 代码：

> AGENT

关键发现：`_profile_begin()` 在第461、474、526、640、654行**每步每层都在调用**。来看它是否是热路径问题：

> AGENT

`_profile_begin()` 调用了 `_profile_can_sync()` 再调用 `time.perf_counter()`，但关键在于 `_profile_can_sync()` 里面有 `if not _MINICPM_PROFILE: return False`，默认 False，所以 `_profile_begin()` 不会 synchronize，但**仍然会调用 `time.perf_counter()`**。这是真实开销。现在确认：

> AGENT

`_profile_can_sync()` 默认返回 False（`_MINICPM_PROFILE=0`），但 `_profile_begin()` 仍然调用 `time.perf_counter()` 并返回。然后 `_profile_end()` 在第67行立即 return（`if not _MINICPM_PROFILE: return`）。 所以热路径上 `_profile_begin()` 每次仍然执行： 1. 函数调用 `_profile_can_sync()` → False 2. `time.perf_counter()` 调用（不可省略） 每 step 被调用多少次？我来数： - minicpm_attention_kernels.py 在 decode mode 下：每个 std-attention 层（8层）每步 forward 被调用 ≥2次（_conv_start + _begin_start + _dec_start） - minicpm_backend.py 中也有 `_profile_begin()` 现在查调用次数和 minicpm_backend.py 的 `synchronize` 是否真的在热路径：

> AGENT

现在确认 minicpm_backend.py 的 decode 热路径中 `_profile_begin` 调用：

> AGENT

关键：在 decode 时，标准 attention 层每层有 3 个 `_profile_begin()` 调用（行1441, 1453, 1521），加上来自 minicpm_attention_kernels.py 的调用。`_profile_end` 虽然在 `_MINICPM_PROFILE=False` 时立即返回，但 `_profile_begin()` 每次仍会调用 `time.perf_counter()`。 现在确认 minicpm_backend.py line 2175 的 `torch.cuda.synchronize()` 触发条件： 这是在 `else` 分支（即 `_MINICPM_PROFILE=False` 时），位于 `if self.attention_kernel_type == "flashinfer":` 块内，即**每步 decode CUDA graph replay 都触发**。这是最严重的问题。 现在检查 EAGLE_FORCE_NO_ACCEPT 和其他 os.environ.get 调用：

> AGENT

现在统计热路径上 `os.environ.get()` 每步的调用次数：

> AGENT

minicpm.py 的两个 `synchronize()` 在 `set_embed_and_head/set_embed` 中，只在初始化时调用，不在热路径。现在检查 `_mm_profile_begin()` 是否也有类似问题：

> AGENT

这是每层 forward 都调用 6 次 `_profile_begin()` / `_profile_end()` 的地方。在 32 层模型中，每步触发 32×6 = 192 次（每次都调用 `time.perf_counter()`）。现在检查 llama_eagle3.py：

> AGENT

现在数出每步热路径的 `nvtx.range_push/pop` 总调用数：

> AGENT

现在确认 minicpm_backend.py 中 `synchronize()` 的具体上下文（line 2175 是 decode replay 热路径中的 else 分支）：

> AGENT

这是最严重问题：当 `_MINICPM_PROFILE=False` 时，`begin_forward` 之后会 **无条件 `torch.cuda.synchronize()`**，每步一次。这注释上写 `non_blocking=True`，但之后立刻同步，把异步优势全消掉了。 现在确认这个函数是否每步 decode 都调用到，是哪个方法：

> AGENT

这是 `init_forward_metadata_replay` 函数，每步 CUDA graph replay 时调用一次。注释第4步也写明了 "Synchronize GPU"。这是有意为之还是可以优化？ 来看注释："to ensure updates complete before graph replay"——这是正确的技术理由，但有意义的问题是：`begin_forward` 已经用 `non_blocking=True`，所以这里的 sync 是为了确保 flashinfer wrapper 的 CPU-side metadata 写入完成。但这个 sync 是每 step 一次的真实 overhead。 现在汇总估算： - `torch.cuda.synchronize()` 在 decode 路径（minicpm_backend.py:2175）：每步 ~1-3ms（强制 CPU-GPU 同步） - nvtx push/pop（eagle_worker.py ~35 对 + eagle_info.py ~12 对 + hybrid:15 对）：没有 profiler 时 NVTX 是 noop，但通过 `torch.cuda.nvtx` dispatch 有轻微开销 ~几百 ns - `os.environ.get()` 调用（每步 7+6=13 次）：每次字典查找 ~200-500ns，总计 ~3-7µs - `_profile_begin()` 调用（minicpm.py 每层6次×32层=192次 + minicpm_backend.py decode 每层3次×8层=24次 + attention_kernels.py 3次×8层=24次）：总计 ~240次 `time.perf_counter()` 调用，每次约 50-100ns，总计 ~12-24µs - `_b12x_profile_call` wrapper（每个 linear forward 调用，每层每 forward ~4次 GEMM，32+draft层，spec v1 总 ~96+ 次）：每次只是一个 bool check + function call，约 100ns，总计 ~10µs --- 以下是审计结论： --- ## 严重（每步都触发，明显影响吞吐） **`minicpm_backend.py:2175` — 无条件 `torch.cuda.synchronize()` 在 decode CUDA graph replay 热路径** 函数 `init_forward_metadata_replay`（每步 decode 必调），在 `_MINICPM_PROFILE=False` 时走 `else` 分支，对 FlashInfer `begin_forward(non_blocking=True)` 之后立即调用 `torch.cuda.synchronize()`。注释写"Synchronize GPU to ensure updates complete before graph replay"，但 synchronize 会把 CPU 阻塞到 GPU 清空队列，代价在 1-3ms/step 量级（取决于 GPU pipeline depth）。 修复建议：删除 `else: torch.cuda.synchronize()` 这一行。`begin_forward` 内部已经 non-blocking 安排，CUDA graph replay 本身会等前序操作。如果确实需要同步（怀疑是历史上调试留下的），改为 `torch.cuda.current_stream().synchronize()` 或用 CUDA Event 等待更细粒度。 --- ## 中等（次要影响，累积不可忽视） **`minicpm.py:615-645` 每层 6 次 `_profile_begin()` 调用 → 32 层 × 6 = 192 次 `time.perf_counter()`/step（target model）+ draft model 同比** `_profile_begin()` 在 `_MINICPM_PROFILE=False` 时不 synchronize，但仍然无条件调用 `time.perf_counter()` 并返回浮点数。`_profile_end` 在第一行 `if not _MINICPM_PROFILE: return` 提前退出，但 `_profile_begin` 没有对应的 early exit。每次 `time.perf_counter()` 约 50-100ns，32层×6 + draft模型一层×6 ≈ 198次调用 ≈ ~10-20µs/step CPU overhead。 修复建议：在 `_profile_begin()` 加一行 `if not _MINICPM_PROFILE: return 0.0`（放在第一行）。这会把 ~200 次函数调用从 `time.perf_counter()` 降为直接 return。 具体位置： - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_attention_kernels.py:60-63` - `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_backend.py:164-167`（两处各有相同定义，需同步修改） **`eagle_worker.py` + `eagle_info.py` — 无条件 nvtx push/pop（35+12 对 = 47 对/step）** 在 `forward_batch_generation` → `draft()` → `verify()` 热路径上，nvtx 调用没有任何 guard。没有 nsys 时这些调用是 CUVIDEXT noop，但仍需经过 `torch.cuda.nvtx.range_push` dispatch（Python → C → driver），每对约 200-500ns，47对 ≈ ~10-25µs/step。`hybrid_linear_attn_backend.py` 里 `update_mamba_state_after_mtp_verify` 的 11 对 nvtx 每步也会触发（MiniCPM-SALA `mambaish_config` 非 None）。 修复建议：用模块级常量 guard，例如： ```python _NVTX = os.getenv("EAGLE_NVTX", "0") == "1" _nvtx_push = torch.cuda.nvtx.range_push if _NVTX else lambda x: None _nvtx_pop = torch.cuda.nvtx.range_pop if _NVTX else lambda: None ``` 将 `eagle_worker.py`、`eagle_info.py`、`hybrid_linear_attn_backend.py` 中所有裸 nvtx 调用替换为 `_nvtx_push`/`_nvtx_pop`。 **`eagle_worker.py:662-663,871-872,1284-1285` + `eagle_info.py:422-423,476` — 每步 7 次 `os.environ.get()` 调用** `EAGLE_PROFILE_SYNC_STAGES`、`EAGLE_PROFILE_SYNC_AFTER_DRAFT`、`EAGLE_PROFILE_SYNC_AFTER_TARGET_FORWARD`、`EAGLE_PROFILE_SYNC_AFTER_DRAFT_EXTEND`、`EAGLE_PROFILE_SYNC_AFTER_VERIFY_KERNEL`、`EAGLE_PROFILE_SYNC_BEFORE_VERIFY_LIST`、`EAGLE_FORCE_NO_ACCEPT` 每步都要查 dict（CPython `os.environ` 是一个 Mapping over `os._Environ`，每次都走 C extension）。 `start_eagle.sh` 中 `EAGLE_FORCE_NO_ACCEPT="${EAGLE_FORCE_NO_ACCEPT:-0}"` 设为 `"0"`；其余 `EAGLE_PROFILE_SYNC_*` 变量都没有设置（unset）。 `eagle_info.py:17` 的 `_EAGLE_TRACE_PATH = os.environ.get("EAGLE_TRACE_FILE")` 模块加载时执行一次，`EAGLE_TRACE_FILE=""` → `_EAGLE_TRACE_PATH = ""`，`bool("") = False`，所以所有 `if _EAGLE_TRACE_PATH:` 分支不进入（正确，无问题）。 修复建议：把上面 7 个 sync-flag 变量都提升为模块级常量（模仿 `_EAGLE_TRACE_PATH` 的写法）： ```python _EAGLE_PROFILE_SYNC_STAGES = os.getenv("EAGLE_PROFILE_SYNC_STAGES", "0") == "1" _EAGLE_PROFILE_SYNC_AFTER_DRAFT = os.getenv("EAGLE_PROFILE_SYNC_AFTER_DRAFT", "0") == "1" # ... 等 ``` 然后在热路径中改为 `if _EAGLE_PROFILE_SYNC_STAGES or _EAGLE_PROFILE_SYNC_AFTER_DRAFT:`。 --- ## 已确认无影响 - `_EAGLE_TRACE_PATH`：`start_eagle.sh` 中 `EAGLE_TRACE_FILE=""` 导致 Python 端 `""` → falsy，所有 trace emit 分支均不进入 - `_EAGLE_PROFILE`（record_function）：已替换为 `_nullcontext` - […]
