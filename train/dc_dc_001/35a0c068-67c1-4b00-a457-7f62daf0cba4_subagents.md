> DEVELOPER

背景：我在优化 OpenBMB/MiniCPM-SALA 的推理（仓库 /user_4813494d/openbmb），用 fork 的 SGLang。当前生产配置：EAGLE-3 chain verify，`spec_steps=2, topk=2, dtn=5`。draft model 在 `eagle/sglang_model/`（NVFP4 量化）。SGLang fork 在 `demo-sala/sglang/python/sglang/srt/`。 任务：把 EAGLE-3 在 SGLang 中的**完整推理路径**梳理一遍，目标是后续找优化点。请聚焦 thoroughness=very thorough。 具体要找的东西： 1. **入口与调度**：spec decoding 的入口（`speculative/` 目录），调度循环里 draft forward / target forward / verify 的顺序，每一步的 Python 调用栈 2. **Draft forward 路径**：draft model 怎么被调用，几步（spec_steps=2 意味着多少次 forward？），每次输入是什么，输出 token 数是多少（topk=2 怎么扩展） 3. **Target forward 路径**：target verify 时一次进来多少 token（draft tree 的叶子数？），怎么打包成 batch，attention 的 causal mask 怎么处理 tree 结构 4. **CUDA graph / piecewise 状态**：哪些步骤被 capture 了，哪些是 eager 的，graph replay 的边界在哪里 5. **同步点**：Python 层和 GPU 之间的 sync 点（`torch.cuda.synchronize`、`.item()`、`.cpu()`），特别是 spec 决策（accept 多少）需不需要 host-device 同步 请给出 file_path:line_number 引用，画一个调用顺序图（一次 spec step 内的完整事件序列）。**重点找出可能的串行瓶颈**：哪些步骤本可以并行/重叠却被串起来了。 不要写代码，不要修改任何文件。在 600 字内汇报核心发现。

> AGENT

我来梳理 SGLang 中 EAGLE-3 speculative decoding 的完整推理路径。

> AGENT

让我找 SGLang 中的 speculative decoding 路径：

> AGENT

现在让我找主调度循环和 forward 路径：

> AGENT

让我查找 server 或主循环代码：

> DEVELOPER

背景：MiniCPM-SALA 用 fork 的 SGLang 跑 EAGLE-3 spec decoding。生产配置 `spec_steps=2, topk=2, dtn=5`，目前是 **chain verify**（不是 tree verify）。SGLang fork 在 `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/`。EAGLE 相关代码主要在 `speculative/` 目录。 任务：**深度阅读 tree verify 的实现**。重点关注（thoroughness=very thorough）： 1. **Tree 结构**：tree 是怎么从 draft 输出构建的？topk=2 + spec_steps=2 形成什么形状的 tree？节点和边怎么编码？ 2. **Verification kernel**：tree verify 的核心函数在哪？是 Triton kernel、CUDA kernel 还是 Python 实现？怎么处理 tree mask（attention 时不同分支不能互相看到）？ 3. **Accept 逻辑**：怎么判断哪些 token 被接受？是按概率比较（标准 spec sampling）还是 greedy match？accept 的 token 序列怎么从 tree 里提取（最长接受路径）？ 4. **Chain vs tree 的区别**：当前生产用 chain（`spec_steps=2, topk=2` → 实际每步只取 top-1 顺序展开？还是 2×2=4 叶子？），tree 模式（如果存在）的代码路径在哪？切换的开关是什么？ 5. **Verify 的批处理细节**：一次 verify 要喂给 target 多少 token？怎么和正常 prefill / decode 共用 attention backend？sparse attention（InfLLM-v2）和 verify 怎么交互？ 6. **可能的优化点**： - tree 构建是否在 GPU 上完成，还是 CPU 来回拷贝？ - mask 是否动态生成，能否预计算 / 共用？ - accept 决策有没有 host-device sync？ - 是否有冗余 kernel launch（每个 tree 节点 launch 一次 vs 一次大 launch）？ 给出 file_path:line_number 引用。**用一段伪代码表示一次 tree verify 内部发生了什么**（从 draft 输出到 accepted token list）。 汇报核心发现，800 字内。不要写代码、不要修改文件。

> AGENT

我来深度探索 SGLang fork 中的 tree verify 实现。

> AGENT

让我先查看关键的 tree verify 相关文件：

> AGENT

现在查看 eagle_worker_v2.py 看 tree verify 的调用流程：

> AGENT

继续查看 verify 流程：

> AGENT

现在看 verify 的具体执行过程：

> DEVELOPER

背景：MiniCPM-SALA 用 fork 的 SGLang 跑 EAGLE-3 spec decoding（`spec_steps=2, topk=2, dtn=5`）。SGLang fork 在 `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/`。模型架构有 8 个 standard Attention 层 + 24 个 Lightning Attention（GLA / linear attention）层混合。EAGLE-3 相关代码在 `speculative/`。 任务：**深度分析 spec decoding 的状态管理与回滚**（thoroughness=very thorough）。spec decoding 的本质难题是：draft 写入了 N 个 token 的 KV，但 verify 后可能只 accept K<N，必须把 N-K 个未接受 token 的 KV cache "撤销"。这个回滚的实现细节往往是性能与正确性的关键。 具体要找： 1. **KV cache 在 verify 期间的写入**：target forward 进来 dtn=5 个 candidate token，KV 是不是 5 个全部写入？写到哪里？token 的 page/slot 分配在 verify 之前还是之后？ 2. **回滚机制**：accept K<5 后，怎么"撤销"未接受的 K_v / K_k 写入？ - 是物理擦除（重写指针、重置 length）还是逻辑标记？ - 涉及哪些数据结构（req_to_token、page_table、out_cache_loc 等）？ - **特别关注 Lightning Attention / GLA**：GLA 是 recurrent state（不是 KV cache），状态怎么回滚？是 checkpoint 整个 state 还是反向计算？这是混合架构 spec decoding 的特殊难点 3. **Standard attention 与 GLA 的回滚差异**：8 个 standard layer 的 KV cache 回滚 vs 24 个 GLA layer 的 state 回滚，哪边更重？哪边更容易出错？ 4. **CUDA graph 兼容性**：回滚操作是不是必须在 graph 外（动态 length）？ 5. **同步点**：回滚需要知道 accept 数量 → host-device sync 必然存在吗？放在哪里？能不能延迟？ 6. **正确性陷阱**：是否有 fork 改过的 patch 处理这个？检查 `demo-sala/sglang/python/sglang/srt/layers/attention/minicpm*` 和 GLA 相关文件 要找的文件包括但不限于：`speculative/eagle_*`、`mem_cache/`、`layers/attention/minicpm_backend.py`、`layers/attention/*gla*`、`model_executor/forward_batch_info.py`。 给出 file_path:line_number 引用。**特别强调 GLA state 回滚的实现**，这是混合架构最容易藏问题的地方。 汇报核心发现，800 字内。不要写代码、不要修改文件。

> AGENT

现在让我查看 CUDA graph runner 和 tree mask 构建：

> AGENT

我来深度分析 spec decoding 的状态管理与回滚机制，重点关注 KV cache 写入、回滚策略和 GLA state 处理。

> AGENT

看一下 sample 函数和 verify_input 的定义：

> AGENT

现在找 GLA/Lightning Attention 相关文件和内存管理模块：

> AGENT

现在让我查看 tree mask 构建和 verify 准备：

> DEVELOPER

背景：在优化 OpenBMB/MiniCPM-SALA 的 EAGLE-3 spec decoding。仓库 /user_4813494d/openbmb。 任务：把项目里**所有关于 EAGLE 的文档与历史性能数据**汇总，目的是知道哪些优化已经试过、哪些是负结果、当前 accept rate 是多少、瓶颈是哪个算子。thoroughness=medium。 具体要读： 1. **`/user_4813494d/openbmb/docs/eagle/`** 整个目录，特别是 `README.md`, `training-v2.md`, `dflash.md` 2. **`/user_4813494d/openbmb/docs/runtime.md`** 里 decode 期算子优化清单和负结果合集 3. **`/user_4813494d/openbmb/eagle/README.md`** 和 `eagle/` 下任何 .md 4. **`/user_4813494d/openbmb/bench/results/`** 和 `bench/sglang_*.jsonl` 最近的性能数据，提取： - 当前 mean accept length（如果记录了） - TPOT / ITL 数值 - draft forward vs target forward 的耗时占比 5. **git log 最近 30 个 commit** 涉及 eagle / spec / draft / verify 的，提取做过什么、放弃过什么 6. **`/user_4813494d/openbmb/AGENTS.md`** 如果有 spec 相关备注 输出格式（700 字内）： - **已落地优化清单**：列出已经做的 spec decoding 改进 - **已尝试的负结果**：试过但没收益 / 反而退化的方向 - **当前已知瓶颈**：哪些算子/步骤是热点 - **当前 accept length 和 TPOT 数字** - **值得复查的 TODO / 候选项** 不要写代码、不要修改文件。给出 file_path 引用。

> AGENT

现在查看树构建的细节，看 parent 怎么编码的：

> AGENT

找到了关键文件。现在深入查看 eagle_worker_v2.py 和 spec decoding 的核心逻辑：

> AGENT

I'll help you compile all EAGLE-related documentation and performance data. Let me start by systematically exploring the directories and files you mentioned.

> AGENT

现在让我查看 verify 准备和 sample 过程中的同步点：

> AGENT

让我查看 draft_forward 返回 parent_list 的方式：

> AGENT

Now let me read the key documentation files and check for performance data:

> AGENT

现在我需要看 select_top_k_tokens 如何生成父信息：

> AGENT

Now let me read the runtime.md and check for performance data:

> AGENT

查看验证过程和回滚逻辑：

> AGENT

现在让我查看同步点和 CPU/GPU 交互：

> AGENT

现在理解了树的结构。让我查看是否有 chain vs tree 的开关：

> AGENT

Now let me check the latest performance data files and git log:

> AGENT

检查注释或代码中是否说明只使用了 greedy 而不是 topk 采样：

> AGENT

现在让我检查 draft extend 循环中的流重叠：

> AGENT

查看 verify_tree_greedy 的完整 acceptance 逻辑：

> AGENT

现在查看 eagle_info_v2.py 中的核心分配逻辑：

> AGENT

现在让我看一下 plan_stream 的实现：

> AGENT

Now let me extract performance metrics from recent benchmark files:

> AGENT

现在让我查看 draft_forward 循环中的 topk 计算和 forward 数量：

> AGENT

现在让我查看 Triton kernel 的具体调用位置和参数：

> AGENT

让我看看 CUDA graph 是否涵盖整个 draft 循环：

> AGENT

现在我需要找到 sgl_kernel 的源代码来看 verify_tree_greedy 和 build_tree_kernel_efficient 的实现：

> AGENT

Let me search for actual benchmark result numbers in the docs:

> AGENT

现在查看 GLA/Lightning Attention 状态管理：

> AGENT

Perfect! Let me also check for specific performance numbers in documentation:

> AGENT

让我查看最核心的调度循环体：

> AGENT

现在让我总结关键发现。让我再检查一下 verify tree sample 中的 GPU 同步点：

> AGENT

查看内存池与页表管理：

> AGENT

看来 sgl_kernel 可能是外部库。让我检查 jit_kernel 中是否有相关实现：

> AGENT

sgl_kernel 是通过 from sgl_kernel import 导入的外部库。让我查看一下是否有注释或其他文档说明调用的细节：

> AGENT

现在查看在生产代码中的配置：

> AGENT

现在查看 forward_batch_info 中的 seq_lens 和状态管理：

> AGENT

现在查看关键的 GLA state 管理和 verify_prefill_wrapper：

> AGENT

让我看看在注释中是否明确说明了当前是 chain verify 还是 tree verify：

> AGENT

现在让我查看树构建后的节点关系是如何从 retrive 信息中提取的：

> AGENT

现在找 GLA/hybrid_linear 的 verify 路径：

> AGENT

现在让我看看 prepare_for_v2_verify 中关于 tree mask 的部分：

> AGENT

现在让我查找 attention backend 中对 tree_mask 的处理：

> AGENT

现在找 custom_mask 在 forward 中的使用：

> AGENT

完美！找到了核心。现在查看 verify 期间如何使用这些 state：

> AGENT

现在让我绘制调用序列图。基于我的分析，让我生成报告： --- ## EAGLE-3 在 SGLang 中的完整推理路径梳理 ### **核心调用流程** (一次 spec step 的完整序列) ``` forward_batch_generation() [line 710] ├─ draft_worker.draft() [line 742] │ ├─ prepare_for_v2_draft() [eagle_info_v2.py:142] │ │ └─ assign draft cache locs (Triton kernel, GPU) │ ├─ CUDA graph replay OR draft_forward() [line 384 or 395] │ │ └─ draft_forward() [line 450]: │ │ └─ for i in range(spec_steps) [line 476] # 循环 spec_steps=2 次 │ │ ├─ select_top_k_tokens() # 从 topk_p 展开到 topk 个 candidates │ │ └─ draft_runner.forward() # 第 i 步 forward，输入 topk tokens │ │ └─ logits_output.hidden_states, next_token_logits │ ├─ build_tree_kernel_efficient() [line 419] # 构建树状 mask 和 positions │ │ └─ 输出: tree_mask (causal + tree structure), position_buf, retrive_index │ └─ return EagleVerifyInput │ ├─ verify() [line 747] # Target verify │ ├─ prepare_for_v2_verify() [eagle_info_v2.py:214] │ │ └─ assign_extend_cache_locs() (Triton kernel, GPU) │ │ └─ graph_runner.replay_prepare() OR attn_backend.init_forward_metadata() │ ├─ [WAIT STREAM] current_stream().wait_stream(plan_stream) [line 786] <<<< SYNC │ ├─ target_worker.forward_batch_generation() [line 811] │ │ └─ 输入: (spec_steps+1)*bs tokens (draft tree leaves) │ │ └─ attention mask: tree_mask [causal + parent-child dependencies] │ │ └─ logits_output shape: (bs, spec_steps+1, vocab_size) │ │ │ ├─ sample() [eagle_info_v2.py:259] # CPU-side acceptance decision │ │ ├─ argmax(logits) → target_predict │ │ ├─ verify_tree_greedy_func() (GPU kernel) # 树状路径遍历 │ │ └─ .cpu().tolist() [line 865] <<<< SYNC (host-device) │ │ │ └─ Event().record() [line 851] # 标记 verify 完成 │ └─ draft_worker._draft_extend_for_decode() [line 749] # 为下一步准备 ├─ [WAIT STREAM] current_stream().wait_stream(plan_stream) [line 608] <<<< SYNC └─ draft_runner forward on (spec_steps+1)*bs tokens ``` --- ### **关键发现：串行瓶颈** | # | 位置 | 现象 | 影响 | |---|------|------|------| | **1** | draft_forward() [line 476-506] | 循环内顺序执行 spec_steps 次 forward，**每次依赖前一步的 hidden_states 和 logits** | 无法 pipelined；2 步 draft 需串行跑 2 个完整 forward pass | | **2** | verify() line 786-789 | `current_stream().wait_stream(plan_stream)` **强制同步**，阻断 draft extend 的 plan 工作 | 即使开启 OVERLAP_PLAN_STREAM，plan phase 的结果必须完全就绪才能 verify | | **3** | verify() line 804-808 | `.cpu()` 转移 grammar 数据到 CPU **同步点** | 如果启用 grammar，force GPU→CPU transfer | | **4** | sample() line 865-866 | `predict.cpu().tolist()` **host-device 同步** | 决定 accept_length 需要等待整个 verify forward 完成 | | **5** | draft_extend line 607-610 | draft_extend preparation 在 plan_stream，但 verify 后 `wait_stream()` **再次同步** | draft_extend 无法与 verify 并行，必须顺序执行 | --- ### **输入/输出数量分析** - **Draft forward 输入**: 第 i 步接收 `bs × topk` 个 tokens（spec_steps=2, topk=2 → 每步 2×2=4 tokens/batch） - **Draft tree 叶子数**: `bs × (1 + topk×(spec_steps-1))` = bs × (1 + […]

> AGENT

很好！现在我有足够的信息。让我做最后的验证——检查一下 tree 结构的具体大小（topk=2, spec_steps=2 → 多少个节点）：

> AGENT

Perfect! Now I have enough information. Let me compile the final report: ## EAGLE-3 Spec Decoding 优化进展总结 ### 已落地优化清单 1. **架构固化（v2→v3）** - Aux layers 重选：[1,10,22] → [4,9,24]（CE 6.51→4.61，-29%）via linear probe - NVFP4 aux_hidden 存储：2.8× 压缩，训/线精度对齐（+0.47% step-0 accuracy） - 数据规模扩展：50K→200K（云训 v3 配比：68% chinese_r1 + 6% stem_zh + 15% code + 8% codeforces + 3% reasoning） 2. **SGLang 集成（4 大修复）** — commit 8bc05a3 - GLA state rollback 统一判断（mambaish_config） - Sparse k1/k2 slot 新增 alloc 路径（verify 后手动分配） - Draft model 配置隔离（量化置 None，attention backend flashinfer） - KV cache slot 释放时序修复（verify 开头释放 draft slots） 3. **Fused Kernel 优化** - NVFP4 Scale Loader：标量广播到所有 shard（修复 qkv Inf→NaN 全链故障） - GLA Fused Kernel：24 层 1 次 launch，7.63× 加速（5.51→0.72 ms） - intermediate_ssm 直写 Triton kernel：1848 call → 0.4 ms（-99%） 4. **Tree Verify 落地** — commit 1a16b26 - Tree-aware dtn5 verify：GLA sibling 隔离，避免 c2 继承 c1 state - 回滚 Plan A 扁平版（FP32 index_select 205ms 热点，ROI 负） - 稳定方案已通过 `tests/test_simple_gla_tree_verify.py` 5. **性能优化** — docs/runtime.md §4 - RoPE F32 cast 消除（140 us/fwd，3.5× speedup） - Residual fused multiply-add（237 us/fwd，2.15× speedup） - scale_emb width 吸收（2 kernels 消除） - b12x backend 3-tier dispatch（decode GEMM -32.4%，e2e ~3%） ### 已尝试的负结果（勿重复踩坑） 详见 `/user_4813494d/openbmb/docs/runtime.md §6` — 18 项负结果： - **Stage2 FlashInfer backend 替换**：fa3/cutlass/trtllm-gen 全部 sm_120 不支持 - **spec_steps>1 chain**：draft 线性成本 ×N + accept_len plateau，净负 - **Plan A per-branch 扁平**（tree verify）：FP32 index_select 205ms 吞掉收益 - **FP8 KV cache / mamba cache quant / Radix cache**：无收益（KV 非瓶颈） - **Triton NVFP4 GEMV**：2.6× slower（809 vs 307 us/layer） - **TARGET_VERIFY replay de-Python**：target forward GPU 主导（~10ms/cycle），Python 占比极小（<5%） - **CPU 侧优化（EI_ai_tolist memcpy）**：profile 账面改进 99.8%，但 e2e **完全无感** — 原因：同步 API 里的 CPU 时间是 GPU 工作的投影，不是可优化的 CPU 工作量（教训见 §10） ### 当前已知瓶颈 **真实占比归因**（docs/runtime.md §8 + §10.B node-trace）— 584s profile 窗（S1+S8）： | 层面 | 占比 | 热点 | |---|---|---| | **GPU busy** | 82.3% | NVFP4 GEMM (10.17%) + BatchPrefill (6.42%) + index_elementwise (2.63%) | | **GPU idle** | 17.7% | 其中真 host-wait (5.5%) 分散多处，单点最大 2.1% (EV_target_forward Python) | | **CPU 侧** | — | memcpy 风暴已 revert（证伪无 ROI）；真可动的 host-wait ≈ 5.5% 且碎片化 | **核心结论**： - Workload GPU-bound，GPU kernel 优化仍第一优先级 - CPU 侧 e2e ROI 天花板 ~5.5%，任何单点 <2% - b12x GEMM (10.17%) 已优化，BatchPrefill (6.42%) / kernel fusion 可继续看 ### 当前 Accept Length 和 TPOT 数字 从多处文档交叉验证： - **当前 accept_len 基线**：1.45–1.48（cu13，对齐 cu12 ~1.50） - 来源：`/user_4813494d/openbmb/docs/cuda13-upgrade.md`、v2/v3 训练配方对标 - DFlash 决策阈值：accept_len ≤1.55 立即切 DFlash；>1.70 继续优化 EAGLE-3 - **Break-even 分析**（docs/eagle/README.md §8） - EAGLE-3 s=2, k=1, dtn=3：draft ~1.0ms + verify ~5.5ms → **break-even accept_len ≈ 1.15** - 当前 accept_len >> 1.15，稳定收益 - **Draft 成本**：~0.53 ms/replay（4.7% […]

> AGENT

完美！现在查看这个 update 函数被调用的地方：

> AGENT

现在让我验证一下 accept 逻辑是否是标准的 spec sampling（概率比较）还是 greedy：

> AGENT

现在看 KV cache 的写入和回滚逻辑：

> AGENT

现在查看整个流程如何处理 KV cache 写回：

> AGENT

让我更深入看这个 move_kv_cache 和相关的 Triton kernel：

> AGENT

完美！现在我理解全面了。让我总结一下核心发现： ## 核心发现汇报 **Tree 结构与拓扑**： - **topk=2, spec_steps=2** 配置下生成的 tree 包含：1（user_4813494d）+ 2（第1层）+ 4（第2层）= 7 个 token 节点（加上最后的 bonus token = 8 个总 verify token） - Tree 构建在 `build_tree_kernel_efficient`（/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_utils.py:47）中由 **Triton/CUDA kernel**（sgl_kernel 外部库）完成 - 节点父子关系编码：`retrive_index`（节点在 tree 中的位置）、`retrive_next_token`（子节点指针）、`retrive_next_sibling`（兄弟指针） - parent_list 在 draft_forward（行395）由 select_top_k_tokens 逐步累积，最后 cat 成统一的稀疏 tensor **Verification Kernel**： - **accept 决策是 Greedy + 概率采样混合**（eagle_info_v2.py:300）： - 当 `is_all_greedy=True` 时：调用 **`verify_tree_greedy_func`**（行303，CUDA kernel），按照 tree 叶子遍历做 greedy match - 否则：调用 **`tree_speculative_sampling_target_only`**（行345，CUDA kernel），用 rejection sampling 做概率对比 - 两个 kernel 都是 **in-place 修改** `predict`、`accept_index`、`accept_length` - Tree mask 在 triton_backend.py:596 写入 `cuda_graph_custom_mask`，用于 attention 层屏蔽跨分支的 attention **Batch Verify 的处理**： - target forward 一次喂入 **num_draft_tokens** 个 token（通常 5 个），logits shape = `(bs*num_draft_tokens, vocab_size)` - custom_mask 通过 triton_backend.py:354 传给 kernel，mask 编码三种模式（FULL_MASK / QLEN_ONLY / QLEN_ONLY_BITPACKING） - 无 host-device sync：retrive 数据全在 GPU，accept 决策直接输出到 GPU buffer **Chain vs Tree 区别**： - **代码中没有显式 chain 模式开关**，只有 tree verify 一种实现（eagle_info_v2.py 没有 chain 分支） - **生产配置 topk=2, spec_steps=2 实际产生树结构**（不是简单 chain），但如果 topk=1 退化为 chain **优化点观察**： - Tree 构建和 mask 生成都在 GPU（kernel_efficient），但 parent_list 在 CPU 端 cat（行521-525 in eagle_worker_v2.py） - Accept 输出 `accept_index` 是最长接受路径的叶子索引，`accept_length` 是深度，内部 CUDA kernel 自动遍历树返回 - 每批一次 kernel launch（`verify_tree_greedy` 或 `tree_speculative_sampling_target_only`），不是每节点一次 **伪代码流程**（draft 输出 → accepted tokens）： ``` Draft output: (bs, num_steps, topk) logits → score_list, token_list, parent_list ├─ organize_draft_results: select top-k paths ├─ build_tree_kernel_efficient(parent_list, scores): │ ├─ Encode tree structure: retrive_index, retrive_next_token, retrive_next_sibling │ ├─ Generate tree_mask (sparse, mask cross-branch attn) │ └─ Allocate position for each draft token ├─ Target verify forward with custom_mask → logits (bs*num_draft_tokens, vocab) ├─ if is_all_greedy: │ └─ verify_tree_greedy_func(tree structure, target logits) → greedy match path │ else: │ └─ tree_speculative_sampling_target_only(rejection sampling) → probabilistic accept ├─ Extract accept_length & accept_index from tree ├─ predict[accept_index[:accept_length]] = final accepted token sequence └─ Extend draft KV cache only for accepted tokens, loop back to next draft step ``` **文件引用**： - Tree 构建：/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_utils.py:47-158 - Verify kernel 调用：/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info_v2.py:259-375 - Tree mask 在 attention 中应用：/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/triton_backend.py:596, 646 - Draft 循环主逻辑：/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py:410-432, 769-846

> AGENT

现在查看 seq_lens 如何驱动回滚：

> AGENT

完美。现在让我汇总所有发现。让我最后查看一个关键的 request_keep_indices 逻辑：

> AGENT

完美了。现在让我汇总和撰写深度分析报告： ## 核心发现：MiniCPM-SALA Spec Decoding 状态管理与回滚机制深度分析 ### 1. **KV Cache 写入与分配时机** **关键文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info_v2.py` (lines 142-178, 180-210, 414-446) **发现**： - **Draft 阶段**：`assign_draft_cache_locs_page_size_1` (line 54-78) 在 draft forward **之前** 一次性为全 dtn=5 个 candidate token 分配 page/slot。这些位置记录在 `batch.out_cache_loc` 中（line 155-169）。 - **Verify 阶段**：`assign_extend_cache_locs_func` (line 225-233) 在 verify forward **之前** 重新扫一遍 `req_to_token` 页表，为接受的 token "复制" KV 物理位置到目标 KV cache。这是一个 **选择性复制**，仅复制 accept_length 个 token。 - **关键点**：两个阶段都是预分配（BEFORE forward），而非动态分配。这使 CUDA graph 兼容性成立。 ### 2. **回滚机制：逻辑标记 vs 物理擦除** **关键文件**：`eagle_worker_v2.py` (lines 847-898), `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/memory_pool.py` (lines 1035-1083) **发现**： - **标准 Attention 的 KV 回滚**：NOT 物理擦除。新的 `seq_lens += accept_length` (line 847) 仅更新长度指针。未被接受的 N-K 个 token 的 KV 数据物理上仍在内存中，但因为 `seq_lens` 不会再读它们，形成 **逻辑垃圾**。 - **页表更新**：`move_kv_cache()` (memory_pool.py:1035) 通过 Triton kernel `copy_all_layer_kv_cache_tiled` 仅拷贝 `tgt_cache_loc[accept_index]` 指向的 K、V，覆盖式地将接受的 token KV 移到目标池。未被接受的数据从不被触及。 ### 3. **GLA/Lightning Attention 的状态回滚——混合架构的关键难点** **关键文件**：`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py` (lines 50-165, 1631-1710), `eagle_worker_v2.py` (lines 900-939) **发现**： - **GLA 是 recurrent state**（不是 KV cache），需要特殊处理。24 个 GLA 层的状态是 `h_t = [B, H, K, V]` recurrent state，每一步都会变化。 - **Checkpoint 策略**：核心创新在 `_fused_recurrent_gla_intermediate_kernel` (line 59-164)，它在单个 kernel 调用内处理全 dtn=5 步，**同时 CHECKPOINT 每一步之后的 h_t**（line 156-158）到 `ht_all[step]` 缓冲。这样 verify 后无需回滚，只需 **按 accept_length 索引选中对应步的 h_t** 复制回主 state 缓冲。 - **Verify 后的 Scatter**：`update_mamba_state_after_mtp_verify()` (line 1631-1710) 在 verify 完成后执行。它查询 `intermediate_ssm[src_idx, last_steps]`（line 1672-1674）取出对应的 h_t，用 torch scatter 写回主 `ssm_states[:, dst_indices]`。这是 **per-step state 的索引选择**，而非动态长度重置。 - **无需反向计算**：GLA 不像 RNN 需要反向展开。checkpoint 的 h_t 直接就是正确答案，accept_length 就决定了取哪一步。 ### 4. **Standard vs GLA 回滚的复杂度差异** - **Standard Attention**（8层）：KV cache 回滚仅需更新 `seq_lens` 指针 + 有选择地拷贝 accept_index 的数据。纯内存指针操作，无计算。 - **GLA**（24层）：需要 per-step state checkpoint（增加内存4倍~5倍），verify 后通过 scatter 与 mask 操作恢复状态。**复杂度更高但更安全**：state 在 checkpoint 中，不存在部分覆盖问题。 - **易错点**：若 GLA checkpoint buffer 大小错误或索引计算有误，会导致 state 混乱（跨请求 contamination）。当前代码通过 `valid_mask` 和 `src_state_indices` 的对齐防护。 ### 5. **Host-Device Sync 点与延迟性** **关键发现**： - `accept_length` 在 verify 的 sample 阶段（line 844）由 logits sampling 产生，必须从 GPU 回读到 CPU（用于 `build_request_keep_indices_for_spec_v2` 的列表构造）。 - Sync 点位置：line 851 `verify_done.record()` 之后立即返回 `GenerationBatchResult`，包含了 `accept_lens`。**延迟机制**：实际 GLA state scatter 在 `_run_sala_post_verify_hooks()` 里（line 934-939），不在 verify 函数内。这样 verify forward 的 GPU 计算与 state 更新并不同步。 - **无法完全延迟**：因为下一轮 draft 需要正确的 state 初值，所以 GLA state 更新必须在下个 draft 的 forward_metadata init 之前完成（隐含的 sync 屏障）。 ### 6. **CUDA Graph 兼容性** **关键文件**：`eagle_draft_cuda_graph_runner.py`, `eagle_draft_extend_cuda_graph_runner.py` **发现**： - **Draft CUDA graph**：可以捕获，因为 dtn=5 是固定的、cache 位置预分配。 - **Verify forward 内部**：不进 graph（`can_run_cuda_graph` 判断于 line 245-250 只针对 forward 本身）。Verify 前的 metadata 准备（line 776-800）、后的 state 更新（line 934-939）都在动态代码路径。 - **原因**：verify 的 logit sample 输出（accept_length）在运行时才确定，无法固定 graph。GLA state scatter 的 mask 也动态。 ### 7. **正确性陷阱与 Fork 改进** **特别关注**： - `_run_sala_post_verify_hooks()` (line 900-939)：这是 fork 相对于原始 SGLang 的 **关键 patch**。它在 verify 完成后立即处理两件事：(1) GLA state 回滚（update_mamba_state_after_mtp_verify），(2) 稀疏 k1 层的 slot 分配（_alloc_sparse_for_new_positions）。 - **MiniCPM 稀疏模式**：line 957-1001 处理 MiniCPM 特有的稀疏 attention（kernel_size、kernel_stride）。verify 后要为新增 token 分配稀疏页。这是 **标准 SGLang 没有的**。 - **缺陷风险**：若 `request_keep_indices` 处理错误（line 863-870），可能导致 finished request 的 state 被错误地保留或转移到其他 request。 ### […]

> DEVELOPER

背景：MiniCPM-SALA fork 的 SGLang 在 `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/`。混合架构 8 SA + 24 GLA。EAGLE-3 spec decoding 生产配置 `spec_steps=2, topk=2, dtn=5`。 任务：**深度调研一项优化的可行性**——融合 `update_mamba_state_after_mtp_verify` 中的 4 次 fancy scatter 操作。约束：**只读代码、不跑、不改**。最终给出"能否做、怎么做、风险在哪、ROI 估计"。thoroughness=very thorough。 必读位置： - `demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py:1631-1710`（update_mamba_state_after_mtp_verify 主体） - 同文件里 GLA fused kernel `_fused_recurrent_gla_intermediate_kernel`（约 line 50-165），看 `intermediate_ssm` / `ht_all` 的生产端 - `demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py` 里调用该函数的位置（在 `_run_sala_post_verify_hooks` 内，约 line 900-940） - `demo-sala/sglang/python/sglang/srt/speculative/eagle_info_v2.py` 里 accept_length / accept_index 的生成（约 line 259-375） - 相关测试：`demo-sala/sglang/python/tests/` 里有没有覆盖这个函数的（`grep -r mamba_state_after_mtp` 之类） 具体调研项（每条都要回答）： 1. **数据流精确画像** - 4 个 scatter / index_copy_ 各自的 (源 tensor, 目的 tensor, 索引, 形状) 是什么？ - `intermediate_ssm` shape = [dtn=5, batch, num_heads, K, V]？确认每一维含义 - `ssm_states` shape 和 layout - 索引 `src_idx`（哪个 batch 的哪个分支胜出）、`last_steps`（accept_length-1）、`dst_indices`（写到主 state 的哪行）从哪来、谁产生、是不是 GPU tensor 2. **accept_length 动态性** - accept_length 在 batch 内 per-request 是否不同？ - 这意味着 scatter 的索引 tensor 在每次 verify 后形状是否变化？ - 是否有 host-device sync 触发？(.item / .cpu / .tolist) 3. **CUDA graph 兼容性** - 这个函数现在是不是在 graph 内？看 eagle_worker_v2.py 上下文 - 如果不在 graph 内：原因是 accept_length 动态？还是其他？ - 融合后的 Triton kernel 能不能进 graph？ 4. **正确性陷阱** - GLA sibling 隔离（commit 1a16b26 提到）和 scatter 的关系——4 个 scatter 里有没有专门处理 sibling 状态？ - finished request 的 state 处理（valid_mask / request_keep_indices） - per-request accept_length 不齐时 scatter 的语义 5. **融合方案设计** - 能否一个 Triton kernel：每个 program 处理 (batch, head) 一个 tile，从 `intermediate_ssm[last_step, src_idx, head]` 读 K×V 元素，写到 `ssm_states[dst_idx, head]` - block 维度怎么切？K=128, V=128, head=2（nkv），batch ≤ 64 - 是否需要先用一个小的 prologue kernel 把 src_idx / last_steps / dst_indices / valid_mask 压成单个索引张量，再交给 main kernel - 如果 4 次 scatter 实际是 4 个不同语义的操作（不是同 source/dest 的同类操作），那"融合"是否还成立？ 6. **ROI 量化** - 当前 4 次 scatter 大概多少 µs？（看 docs/runtime.md / bench/profile/ 里有没有 profile 数据） - docs/runtime.md 写的"预期 2% e2e"出处和依据 - 离线测试方法：能否写一个独立的 unit script 喂模拟数据测延迟，无需启 server 7. **替代方案对比** - 现状是 torch native scatter，PyTorch 是否本身就在底层用了多 stream / fused kernel？ - 是否有现成的 sgl_kernel 或 flashinfer 函数能直接套用？ 8. **文档与 commit 历史** - `git log --oneline -- hybrid_linear_attn_backend.py` 最近 10 个，找相关改动背景 - `docs/runtime.md` 里这一项的具体描述、约束、是否有失败前置 输出格式（1200 字内）： - **数据流图**（一段伪代码描述当前 4 次 scatter） - **可行性结论**：能融合 / 不能融合 / 部分能 - **风险清单**（按严重程度排序） - **离线验证方案**（具体到几个测试文件、测什么 invariant） - **工程量估计**（小时） - **ROI 复核**（基于实际看到的数据） 不要写代码、不要修改文件、不要启动 server。只读 + 思考 + 报告。务必给出 file_path:line_number 引用。

> AGENT

我来深度调研这项优化的可行性。按照必读位置逐个探索数据流、动态性、CUDA graph 兼容性、风险和ROI。

> AGENT

现在读取eagle_worker_v2调用位置和eagle_info_v2的accept_length生成：

> AGENT

读取eagle_worker_v2的调用上下文和eagle_info_v2的accept_length细节：

> AGENT

现在读取完整的update函数（第1710行后）、查看其他辅助细节和profile数据：

> AGENT

读取runtime.md查看性能数据和2%预期的出处：

> AGENT

现在收集数据张量形状信息和具体的scatter操作：

> AGENT

现在查找与intermediate_ssm的相关定义和shape信息：

> AGENT

查找MambaCaches类定义：

> AGENT

很好。现在查找GLA sibling隔离相关的实现（commit 1a16b26）：

> DEVELOPER

背景：MiniCPM-SALA fork 的 SGLang 在 `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/`。EAGLE-3 spec decoding 生产配置 `spec_steps=2, topk=2, dtn=5`。当前 draft forward 的 spec_steps=2 步是顺序执行的，每个 step 是独立的 CUDA graph replay。 任务：**深度调研一项优化的可行性**——把整个 draft 阶段（2 步 draft loop + tree build + verify metadata init）capture 进单个大 CUDA graph。约束：**只读代码、不跑、不改**。最终给出"能否做、怎么做、风险在哪、ROI 估计"。thoroughness=very thorough。 必读位置： - `demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py`： - draft_forward 主体（约 line 410-510） - 整个 forward_batch_generation（约 line 700-870） - _draft_extend / verify / _run_sala_post_verify_hooks - `demo-sala/sglang/python/sglang/srt/speculative/eagle_draft_cuda_graph_runner.py` 整文件（draft graph capture 边界） - `demo-sala/sglang/python/sglang/srt/speculative/eagle_draft_extend_cuda_graph_runner.py` 整文件 - `demo-sala/sglang/python/sglang/srt/speculative/eagle_utils.py` 里 `select_top_k_tokens` 实现 + `build_tree_kernel_efficient` - `demo-sala/sglang/python/sglang/srt/speculative/eagle_info_v2.py:142-260` (prepare_for_v2_draft / prepare_for_v2_verify) - 上游 sgl_kernel 的 top-k 实现（grep "top_k_softmax" 或 "fast_topk"） - `demo-sala/sglang/python/sglang/srt/cuda_graph_runner.py` 看 capture 模板 - `demo-sala/sglang/python/sglang/srt/server_args.py` 看 spec_steps/topk/dtn 是从哪传进来的 具体调研项（每条都要回答）： 1. **当前 graph 边界精确画像** - draft 阶段每步是单独 CUDA graph 还是整个 draft_forward 是一个 graph？ - 看 `eagle_draft_cuda_graph_runner.py` 的 capture 函数，replay() 一次覆盖多少工作？ - 2 个 spec_step 之间的 Python 代码（select_top_k_tokens、attention metadata 更新等）有没有 GPU 工作？这些在 graph 外吗？ - tree build (build_tree_kernel_efficient) 现在在 graph 内还是外？ 2. **`wait_stream(plan_stream)` 的真实语义** - eagle_worker_v2.py:786 这个 wait_stream 卡的是什么 stream？为什么需要？ - plan_stream 上跑的是什么工作（attention backend 的 plan） - 如果整个 draft + verify init capture 进单图，plan 工作能否一并塞进图里？还是 plan 本身有 host-side 工作（比如 metadata 计算） 3. **常量化前提** - spec_steps、topk、num_draft_tokens (dtn) 在生产配置确实是常量，但 batch_size 不是。capture 是按 (batch_size) 一组一组 capture 的（标准 SGLang 做法）？ - 如果 batch_size 也按 padding bucket capture，有几个 bucket？是否会爆显存？ - graph 池子大小现在是多少（mem 占用） 4. **select_top_k_tokens 的 graph 兼容性** - 这个函数是 Python 还是 kernel？读它实现 - 调用了什么 GPU op（topk、softmax、scatter）？这些 op 的输出形状是 data-dependent 还是固定？ - 有没有 host-device sync 在里面（.item / .cpu / control flow on tensor value） 5. **multi-step graph capture 的已知做法** - SGLang 上游有没有"循环展开成单图"的先例？grep "torch.cuda.graph" / "make_graphed_callables" - 业界做法：torch 的 conditional graph、stream-with-graph、multi-stream graph capture——哪个适用 - mega-graph 一旦 batch_size 变化，重建成本是多少？ 6. **launch overhead 实测占比** - 当前 docs/runtime.md §10 提到 5.2% 是 <10μs 的 tiny gap。这 5.2% 全在 spec 路径上，还是只是 spec 路径的一部分？ - 已知 draft forward ~0.5ms + verify ~10.6ms，draft 的 launch overhead 在其中是多少？ - mega-graph 砍掉的 wait_stream 那一次，时间占比多少？ 7. **风险清单** - select_top_k_tokens 如果用了 graph-unsafe op（torch.unique、bool tensor indexing 等），怎么办 - tree build 里 parent_list cat 在 CPU——这个 graph 外的 CPU 工作能不能搬到 GPU - mega-graph 模式下，错误诊断变难（一个 graph 出错很难定位到哪个 op） - 内存占用：graph 池子 × bucket 数 8. **离线验证方案** - 能不能在不启 server 的前提下，构造一个 mock batch，capture 当前的 draft graph 看看 capture 能不能成功 - 如果尝试把 select_top_k_tokens 塞进 capture 区，预期会在哪个 op 上 fail（torch 的 graph capture 报错信息） 9. **工程量估计** - mega-graph 涉及修哪些文件、多大 patch 量 - 是否要改 sgl_kernel 上游 10. **ROI 复核** - 假设最大节省 = (spec_steps-1) × per-iter Python overhead + plan_stream sync - 给出乐观 / 保守两个估计（占 e2e %） 输出格式（1200 字内）： - **当前调用栈与 graph 边界图** - **可行性结论**：完全可行 / 部分可行 / 不可行 - **风险清单**（按严重程度排序） - **离线验证方案**（具体到能跑的最小 reproducer） - […]

> AGENT

现在检查当前测试覆盖情况和数据流：

> AGENT

我将系统地调研这个 CUDA graph mega-graph 优化的可行性。让我从关键文件逐一分析。

> AGENT

让我继续读取关键文件：

> AGENT

现在查看accepted_steps和索引的动态性：

> AGENT

继续深入分析关键函数和流程：

> AGENT

现在查看CUDA graph兼容性背景：

> AGENT

现在查看验证中是否使用graph：

> AGENT

现在看看verify 中target forward是否用graph：

> AGENT

现在收集关于可能融合的索引信息和形状：

> AGENT

现在让我查看 `build_tree_kernel_efficient` 的完整实现和底层性质：

> AGENT

查看形状信息和维度的完整映射：

> AGENT

现在让我分析图流传播和内存占用情况：

> AGENT

现在让我总结关键发现并验证一些细节：

> AGENT

现在我有了足够的信息。让我进行最终的深度分析并生成报告。 --- ## **深度调研报告：EAGLE-3 Draft 阶段 Mega-CUDA-Graph 融合可行性** ### **1. 当前 Graph 边界精确画像** **关键发现：** - **Draft 阶段当前分离为 2 个独立 CUDA Graph**（`eagle_draft_cuda_graph_runner.py:319-396`）： - **Graph1：draft_forward()** （`eagle_worker_v2.py:450-527`） - 包含：forward_batch.input_ids → logits → topk sampling - 通过 `self.cuda_graph_runner.replay(forward_batch)` 一次性执行整个 draft_forward - 循环展开：2 个 spec_step 的 forward 内部已展开在单图内（`for i in range(self.speculative_num_steps)`） - **每个 step 间是否有 Python gap**：有，`select_top_k_tokens`（line 477-479）在图外执行 - **Graph2（可选）：draft_extend** （`eagle_draft_extend_cuda_graph_runner.py:235-372`） - 用于 KV cache 填充，与 draft_forward 分离 - **Graph 外的 Python 工作**（不在 CUDA graph 内）： - `select_top_k_tokens()`（`spec_utils.py:467-514`）： - 调用 `fast_topk()` **核心 GPU op**（来自 `sgl_kernel`） - 但**外层逻辑是 Python**：`torch.gather()`、`torch.mul()`、tensor slicing - **初步评估**：这些 op 本身是图兼容的，但 `scores` 的 reshape 操作需检查 - `build_tree_kernel_efficient()`（`eagle_utils.py:47-158`）： - 调用**单个底层 CUDA kernel**（`sgl_build_tree_kernel_efficient`，来自 `sgl_kernel`） - **关键**：前后有 `torch.cat()` 和 `torch.full()` —— **这些在 Python 中执行**（line 61, 79-102, 107-119） - 前置的 `parent_list = torch.cat(parents_list[:-1], dim=1)`（`eagle_worker_v2.py:522`）是**CPU/Python 级操作** - **Plan stream 的工作内容**（`eagle_worker_v2.py:70-78, 598-610, 775-800`）： - 在 `plan_stream` 上运行 `prepare_for_extend_to_fill_draft_kvcache()` 和 `prepare_for_v2_verify()` - 包含：attention backend plan 计算（metadata initialization） - 默认关闭（`SGLANG_ENABLE_OVERLAP_PLAN_STREAM=False`），仅在启用重叠时存在 `wait_stream` 同步点 --- ### **2. `wait_stream(plan_stream)` 的真实语义** **代码位置**：`eagle_worker_v2.py:786-787` ```python torch.get_device_module(self.device).current_stream().wait_stream(self.plan_stream) ``` **流程**： - `plan_stream` 在**独立 CUDA stream** 上运行 attention backend 的 metadata 初始化 - `prepare_for_v2_verify()` 中涉及： - `assign_extend_cache_locs_func()` —— **GPU kernel** - `target_worker.model_runner.graph_runner.replay_prepare()`（可选）—— **GPU 工作** - `attn_backend.init_forward_metadata()` —— **可能有 GPU op**（backend-dependent） - **wait_stream 的作用**：主流等待 plan_stream 完成，确保 metadata 在 verify forward 前就绪 - **能否融合入 mega-graph**： - 如果 plan stream 上只有**纯 GPU kernel**（无 host-side control flow），**能融合** - 但 `replay_prepare()` 涉及**attention backend plan 逻辑**，后者可能含有 host-side 元数据计算 —— **风险区** --- ### **3. 常量化前提与图池管理** **确认**（`server_args.py:423-425, 2065-2081`）： - `spec_steps=2, topk=2, dtn=5` **确实是常量**，在生产启动时固定 - `batch_size` **不是常量**，按 padding bucket capture（标准 SGLang 做法） **Graph 池子大小**： - `eagle_draft_cuda_graph_runner.py:65` 获取 `capture_bs`（多个 bucket） - 按 batch_size padding 捕获，每个 bucket 一个 graph 实例 - `eagle_draft_cuda_graph_runner.py:46` `self.graphs = {}`：bucket_size → graph 映射 - **内存占用估计**： - 单个 draft graph：~200-400 MB（含所有 layer 的 graph pool） - 假设 4-6 个 bucket（典型配置）：**~1.2-2.4 GB** - Mega-graph（融合所有阶段）：**+50-100% 内存**（需存储更多 placeholder tensors） --- ### **4. `select_top_k_tokens` 的 Graph 兼容性** **实现分析**（`spec_utils.py:467-514`）： ```python def select_top_k_tokens(i, topk_p, topk_index, hidden_states, scores, topk): if i == 0: input_ids = topk_index.flatten() hidden_states = hidden_states.repeat_interleave(topk, dim=0) # ✓ Graph-safe scores = topk_p tree_info = (topk_p.unsqueeze(1), topk_index, ...) # ✓ Graph-safe else: expand_scores = torch.mul(scores.unsqueeze(2), topk_p.reshape(...)) # ✓ Graph-safe topk_cs_p, topk_cs_index = fast_topk(...) # ✓ 底层 CUDA kernel，graph-safe input_ids = torch.gather(topk_index, index=topk_cs_index, dim=1).flatten() # ✓ 形状固定 selected_input_index = topk_cs_index.flatten() // topk + ... # ✓ Graph-safe hidden_states = hidden_states[selected_input_index, :] # ⚠️ 动态索引 ``` **关键风险**： - `hidden_states[selected_input_index, :]`（line 506）：**动态索引** - 在 CUDA graph capture 中，这类操作**可能失败**（取决于 PyTorch 版本和 index tensor 是否在 graph 外计算） - **预期错误**：`RuntimeError: Can't capture tensor indexing ... because index tensor is not captured` --- ### **5. Multi-step Graph Capture […]

> AGENT

现在生成最终报告。我已经收集了足够的数据来进行深度分析。让我整理一下关键发现： ## **深度调研报告：`update_mamba_state_after_mtp_verify` 中 4 次 Fancy Scatter 融合的可行性** --- ### **1. 数据流精确画像** **四个 scatter 操作的完整映射** `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py:1665-1712` ``` 操作1 (line 1672-1674) — main_ssm_scatter: 源: intermediate_state_cache[2:, src_idx, last_steps] 形状 [layers, src_N, dtn=5, HV, K, V] → gather [layers, src_N, dtn=5, HV, K, V] 选择 [:, src_indices, last_steps]（advanced indexing） 目的: ssm_states[:, dst_state_indices, :] 形状 [layers, slots, HV, K, V] 索引: src_state_indices, last_steps, dst_state_indices（均 [N_valid]） 语义: 从 intermediate_cache 的某个时步提取，复制到主 SSM 状态池的目标行 操作2 (line 1680-1682) — main_conv_scatter: 条件: if conv_states is not None（SALA 无 conv，不执行） 结构: 同操作1，但针对 conv_window_cache 操作3 (line 1701-1703) — track_ssm_scatter: 条件: if mamba_track_indices is not None（enable_mamba_extra_buffer，低频） 源: intermediate_state_cache[:, src_track_indices, track_steps] 目的: ssm_states[:, dst_track_indices, :] 索引: src_track_indices, track_steps, dst_track_indices（均 [M_track] ⊂ [N]） 语义: interval 采样，保存中间检查点 操作4 (line 1709-1711) — track_conv_scatter: 条件: if conv_states is not None and mamba_track_indices is not None 结构: 同操作3 ``` **形状确认**（来自 `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/mem_cache/memory_pool.py:218-228`）： | 张量 | 形状 | 维度含义 | |---|---|---| | `intermediate_state_cache` | `[num_layers, spec_state_size+1, dtn, HV, K, V]` | layers=32 SA+8 GLA; spec_state_size=batch_sz（≤64）; dtn=5（spec_steps=2, topk=2, dtn=5）; HV=2（GLA nkv_heads）; K=128; V=128 | | `ssm_states` | `[num_layers, slots, HV, K, V]` | slots=cache pool 大小（~4096 从内存预算推） | | `src_state_indices` | `[N_valid]` | N_valid=batch 内 accepted_steps≥0 的数量，per-request 不齐（关键） | | `last_steps` | `[N_valid]` | `accepted_steps[valid_mask]`，值域 [0, dtn-1] | | `dst_state_indices` | `[N_valid]` | `state_indices_tensor[valid_mask]`，从 forward_metadata 来（mamba_cache_indices） | **索引来源追踪**（`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py:909, 934-939`）： ``` accepted_steps = accept_length.to(torch.int64) - 1 # GPU tensor，per-request 动态 ↑ 来自 eagle_info.sample()，由 verify_tree_greedy_func / tree_speculative_sampling_target_only 产生 ↑ 每次 verify 后形状相同（bs,），但值域变化 state_indices_tensor = forward_metadata.mamba_cache_indices[:batch_sz] # GPU int32 ↑ 在 prefill/decode 时预分配，该 request 对应的主状态池行号 valid_mask = accepted_steps >= 0 # bool mask，排除 finished request（-1） src_state_indices = intermediate_state_indices[valid_mask] # 0..batch_sz-1 的 subset dst_state_indices = state_indices_tensor[valid_mask] ``` **GPU tensor 确认**：所有索引及 `accepted_steps` 都在 GPU 上（`.to(torch.int64)` 明确），无 `.item()` / `.cpu()` 触发 host-device sync。 --- ### **2. Accept_length 动态性与索引形状变化** **per-request 不齐**（`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info_v2.py:297, 374-375`）： ```python accept_length = torch.empty((bs,), dtype=torch.int32, device=device) # 经过 verify_tree_greedy_func / tree_speculative_sampling_target_only 填充 # 每个 request 的 accept_length[i] ∈ [1, spec_steps+1]，取决于树验证结果 accept_length.add_(1) # 加 bonus token ``` **动态性分析**： - ✅ accept_length 在 **batch 内 per-request 不同**（树分支选择不同） - ✅ 这直接导致 `last_steps = accepted_steps[valid_mask]` 的值分布变化 - ❌ **但索引 tensor 形状不变**：`valid_mask` shape = (bs,)，`src/dst/last_steps` shape = (N_valid,) ⊆ (bs,)，N_valid 由 accepted_steps≥0 动态决定但不跨越图边界 - ❌ **无 host-device sync**：所有索引操作在 GPU 上，验证后无 `.item()` 等同步（`eagle_worker.py:909` 直接用 GPU tensor） **scatter 操作的 GPU 动态性**： - fancy indexing `ssm_states[:, indices_variable, :]` 其中 `indices_variable` 在每次 verify 后值变但大小 ≤ bs - PyTorch 处理这类 advanced index 生成一个 3D `index_kernel<4>`（read）+ `index_put<4>`（write） - 无条件分支逻辑（掩码形式）在 CUDA kernel 侧展开，不需 host 端循环 --- ### **3. CUDA Graph 兼容性** **Target verify forward 在 graph 外**（`/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py:811-816`）： […]
