> DEVELOPER

深度调查 /user_4813494d/openbmb 仓库中 EAGLE-3 推测解码相关的技术创新。 重点阅读： 1. docs/eagle/README.md - 完整阅读 2. docs/eagle/experiments-log.md - 完整阅读（rope_theta、MARS、Phased Verify 三个方向的实验日志） 3. docs/eagle/collapse-analysis.md - 完整阅读 4. docs/eagle/training-v2.md 和 training-v3.md - 关键点 5. demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py - 关键修改 6. demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py 或类似文件 - GLA fused kernel 同时 git log 查看 EAGLE 相关的提交细节： ``` git -C /user_4813494d/openbmb log --oneline | head -50 git -C /user_4813494d/openbmb show 87a8bb1 --stat git -C /user_4813494d/openbmb show b7a839e --stat git -C /user_4813494d/openbmb show 8cf5f57 --stat 2>/dev/null || true ``` 我需要你给出： 1. 每个技术创新点的具体内容（不是概括，是实质） 2. 每个创新的量化收益（数字） 3. 哪些是我们独有的、竞争对手大概率没有做的 4. 哪些技术方向是已验证落地 vs 仍在实验 请尽量完整，这是为了写技术博客选题用的。

> AGENT

我会系统地调查 EAGLE-3 的技术创新。我将并行阅读所有请求的文件和 git 日志。

> TOOL

[Request interrupted by user]

> DEVELOPER

你在 /user_4813494d/openbmb 工作区，这是一个 SOAR 2026 LLM 推理优化比赛仓库，优化 MiniCPM-SALA 模型推理。请深入调查 EAGLE-3 speculative decoding 相关的所有技术工作。 重点读取以下内容： 1. docs/eagle/ 目录下所有文件（README.md, spec-v2.md, training-v2.md, training-v3.md, collapse-analysis.md, experiments-log.md, longcontext-analysis.md, spec-survey.md, dflash.md） 2. demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py 3. demo-sala/sglang/python/sglang/srt/speculative/ 下其他文件 4. demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py（或类似文件） 5. git log 中所有 eagle 相关的提交消息 请特别关注： - Fused GLA kernel 的技术细节和性能数字 - MARS verify 是什么，theta 参数的作用 - rope_theta=1M 的效果和原理 - tree-aware dtn verify 解决了什么问题 - dynamic spec mode（NO_SPEC/D5/D7）的设计 - 训练 v2→v3 的关键改进（probe 选层、NVFP4 存储） - collapse 分析的具体发现 请给出一份详细的技术摘要，包括具体数字和实现细节。

> AGENT

我会系统地调查 EAGLE-3 投机解码的所有技术工作。让我先并行读取所有文档和源文件。

> AGENT

现在让我并行读取所有文档文件。

> DEVELOPER

你在 /user_4813494d/openbmb 工作区，这是一个 SOAR 2026 LLM 推理优化比赛仓库，优化 MiniCPM-SALA 模型推理（硬件：NVIDIA RTX 6000D, sm_120 Blackwell, 84GB VRAM）。请深入调查量化和 kernel 相关的所有技术工作。 重点读取： 1. docs/quantization.md 2. docs/kernels-sm120.md 3. docs/marlin-tuning.md 4. docs/nvfp4-kv-investigation.md 5. docs/runtime.md 6. demo-sala/sglang/python/sglang/srt/ 下与量化相关的文件（modelopt_quant.py, marlin_utils_fp4.py 等） 7. git log 中所有 b12x、marlin、NVFP4、quant 相关提交 请特别关注： - NVFP4 KV Cache 调研结论（为什么最终放弃，具体技术障碍） - b12x 2-tier dispatch 的设计和效果（具体形状、tile 配置、性能提升数字） - FourOverSix 量化方案是什么 - Marlin FP4 scale bug fix 内容 - scale loader bug（QKV fused per-tensor scale 污染）的完整故事 - sm_120 上各 GEMM 库的实测性能对比 - 生产配置的最终决策及原因 请给出一份详细的技术摘要，包括具体数字、负结果和实现细节。

> AGENT

我将系统地调查量化与内核相关的所有技术工作。让我先从阅读关键文档和搜索相关代码开始。

> AGENT

现在，我将并行读取关键的源文件。

> DEVELOPER

你在 /user_4813494d/openbmb 工作区，这是一个 SOAR 2026 LLM 推理优化比赛仓库，优化 MiniCPM-SALA 模型推理。请深入调查除 EAGLE speculative decoding 和量化之外的所有性能优化工作。 重点读取： 1. docs/prefill.md 2. docs/prefill-accel-phase1.md（如果存在） 3. docs/prefill-accel-survey.md（如果存在） 4. docs/runtime.md 5. docs/infllmv2-blockmask-fix.md 6. docs/cuda13-upgrade.md（关注性能影响部分） 7. bench/mini_bench.sh 8. git log 中所有 perf、prefill、runtime、infllmv2 相关提交 请特别关注： - InfLLM-v2 稀疏注意力的实现和优化（blockmask fix 解决了什么） - 长上下文 prefill 的热点在哪里，做了什么优化 - plan_info reuse 优化的内容 - decode 期的算子优化清单（已落地的和负结果的） - MiniCPM-SALA 模型架构特殊性（8 standard + 24 GLA 混合）对优化的影响 - 整个工作的 end-to-end 速度收益（能找到多少数字） - cu13 升级带来了什么性能提升 请给出详细技术摘要，包括具体数字和架构特殊性分析。

> AGENT

现在我来搜索与量化相关的源文件和 git log。

> AGENT

我将系统地调查此仓库中的所有性能优化工作。我将首先探索仓库结构并同时读取关键文档。

> AGENT

现在让我读取关键源文件的更具体部分——特别是 MARS 验证和 `eagle_info.py` 中 tree-aware verify 的部分。

> AGENT

现在让我并行读取所有关键文档。

> AGENT

现在，我来获取 git 日志中关于性能优化的详细提交，并阅读更多文档。

> AGENT

让我从关键源文件中获取更多细节，包括 MARS kernel 的实现和 `eagle_worker` 的动态模式逻辑。

> AGENT

好的，我现在来查看更具体的 `git commits` 以及其他关键文件。

> AGENT

我现在来阅读 `eagle_worker.py` 的 `_apply_spec_config` 和 `_forward_no_spec` 部分，以及动态模式的调度器集成。

> AGENT

现在我来查看具体的性能优化提交，以获取更多数据。

> AGENT

现在我来阅读 `modelopt_quant.py` 的 NVFP4 部分，其中包含 dispatch 逻辑。

> AGENT

现在我已掌握足够信息，可以提供一份全面的技术摘要。让我再核实一个关于 MARS CUDA kernel 的细节。

> AGENT

现在我来查看一下 Medusa 提交的性能数据以及 CLAUDE.md 文件，以获取整体上下文。

> AGENT

现在让我更详细地检查 scale loader bug commit 和 Marlin FP4 scale bug fix。

> AGENT

--- # EAGLE-3 Speculative Decoding 技术全貌 -- 详细摘要 以下是对 SOAR 2026 比赛中 MiniCPM-SALA 模型 EAGLE-3 投机解码全部技术工作的系统性总结，涵盖所有文档和核心实现。 --- ## 一、架构概览 **生产配置**: `spec_steps=3, topk=2, dtn=7`, `rope_theta=1000000`, `EAGLE_MARS_THETA=0.85` **Eagle3Model** (~437M trainable): - `fc`: Linear(12288 -> 4096), 融合 3 层 aux hidden - `midlayer`: Eagle3DecoderLayer (1 层完整 decoder) - `self_attn`: Eagle3Attention (GQA 32h/2kv), Q/K input = cat(normed_embed, normed_hidden) - `mlp`: SwiGLU (4096 -> 16384 -> 4096) - `embed_tokens`: Embedding(73448, 4096) [FROZEN] - `lm_head`: Linear(4096 -> 32000), 32K draft 词表 (覆盖率 99.23%) **推理性能**: Draft ~0.50 ms/step (Marlin FP4); d2t 映射 draft->full vocab, hot_token_id 覆盖 32000/73448 = 43.6% --- ## 二、Fused GLA Kernel -- 技术细节与性能 **问题**: 原始路径需 24 层 GLA x dtn 步 = 72 次 kernel launch。 **优化方案**: 24 层 x 1 次 launch, 处理 T=dtn 并导出全部中间 state。 **性能数字**: - **7.63x 加速** (microbench: 5.51 ms -> 0.72 ms) - cos_sim = 1.0, 数值等价 **intermediate_ssm 直写**: - 原: `ht_buf(N*H,T,K,V) -> permute -> intermediate_ssm.copy` (1848 call x 21us = 39.5 ms) - 新: Triton kernel 直写 `intermediate_ssm[cache_idx,:B,:dtn]` - 结果: 0.4 ms (**-99%**), cos = 1.000000, max_abs = 4.5e-8 **核心 Triton kernel**: `_fused_recurrent_gla_intermediate_kernel` (文件: `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py` 行 56-155) - GLA 递推: `h_t = exp(-gamma) * h_{t-1} + k_t * v_t^T` - 每 step 存 intermediate state 到 `ht_all` (形状 `(N, T_per_seq, H, K, V)`) - 支持 `retrieve_parent_token` 实现树感知状态传播 (等效于 STree 的 A-matrix 累乘) --- ## 三、MARS Verify -- 机制与 Theta 参数 **论文**: arXiv:2601.15498 (ICLR 2026) **核心算法**: 对每个 draft token v_t: 1. **Exact Match**: `v_t == top-1` -> 直接接受 2. **Adaptive Relaxation**: `v_t == top-2` 且 `r_t = z_(2)/z_(1) > theta` -> 接受(视为 tie) 3. 否则拒绝 **theta 参数的作用**: - `r_t` = target top-2 logit / top-1 logit (logit ratio) - 当 `r_t > theta` 时, 表示 top-1 和 top-2 的 logit 值非常接近(target 自身也在"犹豫"), 此时接受 top-2 token 的信息损失可忽略 - theta 越低, 放宽程度越大, 接受率越高, 但质量风险也越高 **论文数据** (theta=0.90): - Vicuna-13B: 3.12x -> 3.74x (+27.7% tau) - Llama-3.1-8B: 3.24x -> 4.00x (+37.2% tau) - theta < 0.88 开始有可测量质量退化 **本机实测**: theta=0.85 (比论文推荐更激进) - 吞吐可观测提升, eval 分数无可观测下降 - 推测原因: NVFP4 量化后 logit ratio 分布更集中, theta=0.85 在该模型上仍处于安全区间 - **当前生产值**: `EAGLE_MARS_THETA=0.85` **实现** (关键文件): - `sgl-kernel/csrc/speculative/eagle_utils.cu`: `VerifyTreeGreedy` kernel 8->11 参数, 先 exact match 后 MARS fallback - `eagle_info.py` 行 347-384: 计算 `top2_ratio = z2/z1`, 传入 CUDA kernel - CUDA kernel 内逻辑: 先扫 exact match, fallback 到 MARS (draft_token == top2_token && top2_ratio > mars_theta) --- ## 四、rope_theta=1M -- 效果与原理 **原理**: - RoPE theta=10000 在 130K 位置外推比约 64x, sin/cos phase 周期折叠, draft attention 对长距 token pair 的 score 退化 - […]

> AGENT

我现在对所有技术细节有了透彻的理解。接下来，我将整理并呈现全面的摘要。 --- ## 量化与 Kernel 技术工作深度摘要 ### 一、NVFP4 量化方案 **算法**: GPTQ + FourOverSix (自适应 4/6 block scale)，`lm_head` Identity patch。校准使用 wikitext loguniform 128 samples，8 buckets（512-64K log-uniform），max_length=48K。推理要求 `--dense-as-sparse`（dense_len=0，全序列走 sparse TopK 路径）。 **校准实验结果**: | Config | Calibration | max_length | FourOverSix | dense-as-sparse | ori_accuracy | |---|---|---|---|---|---| | baseline | calib90 | 24K | off | on | 80.27%（不稳定） | | **chosen** | **loguniform 128** | **48K** | **on** | **on** | **79.98%** | | exp | loguniform 128 | 48K | on | off | 78.18% | | exp | calib90 | 72K | on | on | 77.04% | **健康检查警告**: NVFP4 量化后模型在 mcq 强格式约束下会退化为重复 pattern，但 eval regex 仍命中，ori_accuracy 看似正常实则生成垃圾。健康检查必须用 chat 长样本，不用 mcq。 --- ### 二、FourOverSix (4/6) 量化方案 **来源**: MIT-HAN Lab 方案 (arXiv:2512.02010)。 **原理**: 标准 NVFP4 固定 block scale/6；FourOverSix 对每个 block 比较 scale=4 和 scale=6 的 MSE，选更小者。输出格式不变（4-bit FP4 权重 + FP8 block scales），zero throughput impact。 **核心算法**: ```python scale_4 = fp8(scale_6.float() * 1.5) # scale=4: 权重映射到 [-4, 4] mse_6 = sum((W_group - dequant(W_group, scale_6))^2) mse_4 = sum((W_group - dequant(W_group, scale_4))^2) new_scale = where(mse_4 < mse_6, scale_4, scale_6) ``` **实测**: 40-43% 的 blocks 选 scale=4；MLP 层比 Attention 层获益更大。 **集成**: 直接 patch `llmcompressor/modifiers/quantization/gptq/gptq_quantize.py`，在 observer 输出 scale 后、GPTQ 优化循环前插入 scale 选择。通过 `FOUROVERSIX` 环境变量控制（默认 `"1"`）。代码位于 `/user_4813494d/openbmb/demo-sala/patches/gptq_quantize_fouroversix.py`。 --- ### 三、Marlin FP4 Scale Bug Fix **问题**: 平台 sgl-kernel 0.3.20 的 `marlin_template.h` 有 FP4 scale `/2` bug，导致 Marlin FP4 输出的 cos_sim 仅为 0.77。 **修复**: Pre-built `common_ops.abi3.so`（SM120a）via `cp` 替换。修复后 cos_sim 0.77 -> 1.0。重编路径使用 sgl-kernel 源码 + `demo-sala/patches/marlin_fp4_scale.patch`（57 行），编译必须带 `TORCH_CUDA_ARCH_LIST=12.0f`（不是 `120a`，vllm#36865 陷阱）。 **当前部署的 `.so` md5**: `32d27c728ea93203236757d7534b6e68`（含 small-M atomic + shape-aware tile 改进，但**EAGLE draft CUDA graph capture 不兼容**）。 **EAGLE 不兼容问题**: `32d27c7` 比 probe-sala 的 `220c18cc` 大 562 KB，会导致 EAGLE-3 draft CUDA graph capture 挂住（37% 进度卡死）。根因是 small-M atomic/tile 行为和 CUDA graph capture 有不明冲突。当前生产必须用 `220c18cc`（probe-sala 版本）。Marlin 3% 的 e2e 收益在 EAGLE 生产路径下不可用。 --- ### 四、Scale Loader Bug（QKV Fused Per-Tensor Scale 污染） **完整故事**: **根因**: `QKVParallelLinear` 和 `MergedColumnParallelLinear` 在加载 fused per-tensor scales（`weight_scale_2`, `input_scale`）时，只写入了 `shard_id=0`，其余 slot 保留为 `torch.empty` 垃圾数据。后续 `process_weights_after_loading` 中的 `max()` 吸收了未初始化数据，导致 `qkv_proj` scale 被污染，产生 Inf/NaN。 **修复** (commit `f7faed5`): 新增 `PerTensorScaleParameter.load_fused_per_tensor_weight()` 方法，将标量 scale 广播到所有 logical shard，对向量格式则逐元素加载。两种 checkpoint 格式（标量和向量）都支持。 **验证**: flashinfer + graph ON, accept_len=1.50 稳定，6-config 矩阵回归中 zero NaN。 --- ### 五、b12x 2-Tier Dispatch 设计与效果 **设计**: 3 路 GEMM 分流 — Marlin (W4A16) / b12x (W4A4 block-scaled MMA) / CUTLASS (W4A4)。per-shape Marlin 阈值： ```python MARLIN_UPPER = { (N=4096, K=4096): 8, # std_o (N=4608, K=4096): 8, # std_qkv (N=4096, K=16384): 24, # down (K大 Marlin 带宽仍赢到 M=24) (N=32768, K=4096): 16, # gate_up (N=12288, K=4096): 16, # gla_qkv (N=4096, K=12288): […]

> AGENT

现在我已经从所有文档中获取了全面的信息。让我来整理最终的技术总结。 --- # MiniCPM-SALA 推理优化技术详细摘要（除 EAGLE speculative decoding 和量化之外） ## 一、MiniCPM-SALA 模型架构特殊性 MiniCPM-SALA 是混合注意力架构：**8 层标准注意力 + 24 层 GLA（Lightning Attention/简单 GLA）**，共 32 层。这一混合结构对优化的影响贯穿所有方向： - 8 层标准注意力必须走 InfLLM-v2 稀疏路径（`--dense-as-sparse` 强制，因精度问题不可关闭），不存在"短序列走密集 FA"分支 - 24 层 GLA 无 KV cache，但需 recurrent state（ssm_states）管理，spec 解码的 verify 后状态更新链路极重 - GLA 被归到 sglang 的 `MambaAttnBackendBase` 类体系，命中了为通用 Mamba 写的 3D 花式散点操作，是 SALA 特有的性能陷阱 - `config.sparse_config`：block_size=64，topk=64(+32 local)=96，kernel_size=32/128，stride=16/64，window_size=2048 - 全局 `page_size=1`（`minicpm_backend.py:1410 assert`），由 InfLLM-v2 token-level sparse 索引决定，不可改 ## 二、InfLLM-v2 稀疏注意力的实现与优化 ### 2.1 blockmask 修复（`docs/infllmv2-blockmask-fix.md`） **问题**：InfLLM-v2 原生 blockmask 路径（topk_to_uint64 位掩码 + fwdIterator 跳块）在 batch>1 时结果错误，导致一直无法启用。 **根因**：`topk_to_uint64` 输出 head-major 布局 `(num_k_heads, batch, uint64_per_row)`，但 `fwdIterator` 构造函数用 batch-major 寻址。batch=1 时两种布局等价，batch>1 时读到错误掩码行。 **修复**（3 处源码改动）： 1. `flash_blockmask.h` fwdIterator 寻址改为 head-major：`head_idx * params.b * uint64_per_row + batch_idx * uint64_per_row` 2. 去掉多余的 `loop_step_idx` 偏移（同一 batch/head 的所有 Q token 共享同一行 topk 掩码） 3. `flash_api.cpp` 两处 `num_k_heads` 硬编码 2 改为 `num_heads_k` **验证**：batch=1/2/4 + nq=16 swap 全部通过，cos=1.00。部署陷阱：rebuild 后 `.so` 仅产出在 `packages/` 目录，Python 实际加载 venv site-packages 中的旧版，需手动 `cp`。 **当前阻塞**：生产路径用的是 FlashInfer paged attention，infllmv2 原生路径未集成。核心矛盾是 paged KV page_size=1 与 infllmv2 kernel 的 `page_block_size % 256 == 0` 硬约束不兼容（一次 cp.async 连续读 64 个 token 要求物理连续）。方案 A（改 kernel 放宽 page_block_size）仍在调研。 ### 2.2 稀疏 stage1/stage2 架构 **Stage1**：`infllmv2_attn_stage1` + `max_pooling_1d_varlen` + `block_score.topk`。注意 k1/k2 语义：`infllmv2_attn_stage1` 的 `v` 参数实际传的是 `k2`，内部先跑 `k2` 粗略 softmax 得到 `row max/sum`，再用 `k1` 调用 `softmax_rescale_gt()` + `hdim16_reduce()` 输出 score。因此 k1-only 的 fused topk 全部不正确。 **Stage2**：生产走 FlashInfer `BatchDecodeWithPagedKVCacheWrapper`（不是 `BatchPrefillWithPagedKVCacheWrapper`），因为长序列分支 `sparse_max_seq_len_q` 默认 1，触发 `is_prefill=False`，q tokens 摊平到 batch 维。 ## 三、长上下文 Prefill 热点与优化 ### 3.1 Prefill 热点分层（128K prompt, chunked-prefill-size=8192） | 阶段 | 占比 | 说明 | |---|---|---| | **extend_sparse_fa**（8 std layer x stage2 sparse FA） | ~26% | 最大单块 | | **mlp**（32 层 MLP，M=8192 NVFP4 GEMM） | ~16% | | | **attn_gla**（24 层 Lightning Attention） | ~11% | | | attn_standard QKV/OUT proj + RoPE | ~5% | | | sparse_topk（stage1 + pool + topk_select） | ~5% | | | compress_k | <1% | | | ln + residual + embed + final_norm | ~2% | | ### 3.2 周期性 2x 慢 chunk — plan() 根因 每 3 个 chunk 出现一次慢 chunk，`extend_sparse_fa` 翻倍。通过 nsys 精确定位：慢点在 `wrapper.begin_forward()` 即 flashinfer `plan()` 的纯 CPU 计算（work-split 决策），耗时约 23ms，偶发 spike 至约 350ms。慢 chunk 中有异常慢的 HtoD + plan 内额外 GPU 辅助 kernel，说明走了"重计算路径"。 ### 3.3 plan_info reuse 优化（两步递进） **Step 1: 层间 plan 复用**（commit `1f265fe`，2026-04-20） 观察：同一 forward 的 8 个标准层 KV layout 完全一致（`max_kv_len/bs/page_size/heads/dtypes` 相同），只有 `_paged_kv_indices` 变化。plan() 的 work split 完全由前面这些量决定。 实现：`FlashInferKernel.__init__` + `forward` 新增 `_plan_cache_key` / `_plan_last_layer_id`，非 CUDA-graph + 稀疏解码 wrapper 分支判定 `layer_id > _plan_last_layer_id` 且 cache_key 匹配则跳过 `begin_forward`，只覆写 `_paged_kv_indices_buf`。下一次 forward 从 L0 开始自动触发重新规划。 **收益：128K prefill 14.6s -> […]

> DEVELOPER

请帮我核实以下两篇论文的技术细节，用于撰写技术博客，需要确保原理描述准确。 **论文一：FourOverSix** - arXiv: 2512.02010 - 声称是 MIT-HAN Lab 的工作 - 核心思路：对每个 NVFP4 量化 block，比较 scale=4 和 scale=6 的 MSE，选更小者 - 请访问 https://arxiv.org/abs/2512.02010 确认： 1. 论文标题、作者、机构 2. FourOverSix 算法的准确描述（scale=4 vs scale=6 的具体含义） 3. NVFP4 格式中 scale 参数的作用（scale÷6 还是别的？） 4. 论文报告的性能数字 **论文二：Medusa** - 声称是 Tianle Cai et al., ICML 2024 - 核心：多个预测头附加在 LLM 最后一层，ResBlock + LM Head 结构 - 请访问 https://arxiv.org/abs/2401.10774 确认： 1. 论文标题、作者、venue 2. Medusa head 的准确架构（ResBlock 具体结构） 3. verify 机制（tree attention 的工作方式） 4. 与 standard speculative decoding 的核心区别 请直接访问 arxiv 页面获取准确信息，给出验证结论。

> AGENT

我将同时访问两篇 arXiv 论文以核实技术细节。

> AGENT

让我阅读完整的抓取结果，以便更详细地获取这两篇论文的信息。

> AGENT

让我获取FourOverSix论文的PDF以了解更多细节，并继续阅读Medusa论文。

> AGENT

现在我来获取更详细的 Medusa 论文内容，特别是关于验证/比较部分。

> AGENT

我现在已经获取了关于这两篇论文的全面信息。让我来整理验证结果。 --- ## 论文一：FourOverSix -- 验证报告 ### 1. 论文标题、作者、机构 - **标题**: Four Over Six: More Accurate NVFP4 Quantization with Adaptive Block Scaling - **作者**: Jack Cook, Junxian Guo, Guangxuan Xiao, Yujun Lin, Song Han - **机构**: 1Massachusetts Institute of Technology (MIT), 2NVIDIA - **通信作者**: Jack Cook, Song Han - **代码**: https://github.com/mit-han-lab/fouroversix **关于"MIT-HAN Lab"的声明**: 基本正确。论文明确标注第一单位为 MIT，Song Han 为通信作者之一，且代码仓库位于 mit-han-lab 组织下。但需注意，这是一篇 MIT 与 NVIDIA 的**联合工作**，Yujun Lin 的单位是 NVIDIA，不能简单说是纯 MIT-HAN Lab 的工作。 ### 2. FourOverSix 算法的准确描述 **用户描述的"scale=4 和 scale=6 的 MSE 比较选更小者"基本正确，但需要澄清"scale"的具体含义。** 准确机制如下： - **NVFP4 格式**使用 FP4 E2M1，其可表示值为 {0, 0.5, 1, 1.5, 2, 3, 4, 6}（正数部分），最大值为 6。标准 NVFP4 量化时，每个 block 的值会被归一化到 FP4 的完整范围（-6 到 6），即 `M=6`。 - **"scale=4 vs scale=6"的含义**: 这里的 4 和 6 **不是 scale factor 本身**，而是**归一化范围的上界 M**。当 M=6 时，block 的最大值被映射到 FP4 的最大值 6；当 M=4 时，block 的最大值被映射到 FP4 值 4（放弃了 4 和 6 之间的表示范围）。 - **为什么 M=4 有时更好**: 当 block 缩放到 M=6 时，FP4 值 4 代表 block 最大值的 66.6%（4/6），而 4 到 6 之间没有可表示的值，导致近最大值（66.6%~100% 范围）无法精确表示。当 M=4 时，FP4 值 3 代表 75%（3/4），填补了这一"盲区"，减少了对近最大值的量化误差。 - **选择规则**: 对每个 block 分别用 M=6 和 M=4 量化一次，计算两种方案的反量化值与原始值的 MSE，选 MSE 更小者。论文也测试了 L1 范数和 Abs-Max 规则，发现 MSE 在大多数情况下最优。 **纠正用户描述**: 不是"scale=4 vs scale=6"——更准确的说法是"**归一化上界 M=4 vs M=6**"。Scale factor (Delta) 会根据 M 的选择自动调整。 ### 3. NVFP4 格式中 scale 参数的作用 NVFP4 使用**两级缩放**： - **Tensor-wide FP32 scale** `alpha`: `alpha = max(|X|) / (M_FP4 * M_FP8)`，其中 `M_FP4=6`, `M_FP8=448` - **Block-level FP8 E4M3 scale** `Delta_i`: `Delta_i = max(|X_{16i...16(i+1)}|) / (alpha * M_FP4)`，每 16 个值共享一个 量化公式为分段舍入（Equation 3），取决于 `|X/(alpha*Delta)|` 的范围： - < 2: 步长 0.5 - < 4: 步长 1 - <= 6: 步长 2 **4/6 对 scale 的影响**: 当选择 M=4 时，block 的 scale factor Delta 会相应增大（因为 Delta = max(|X_block|) / (alpha * 4) 而非 / (alpha * 6)）。此外，论文修改了 tensor scale alpha 的计算，将 M_FP8 替换为 256（而非 448），以确保 M=4 的 block scale 在 FP8 E4M3 中可表示（因为 256 * 6/4 = 384，不会溢出 E4M3 的最大值 448）。 **所以用户说的"scale/6"不准确**。正确理解是：scale factor 的分母中 M_FP4 从 6 变为 4，这使得 scale factor 变大（约 1.5 倍），从而将同样的值映射到 FP4 更小的范围，获得更密集的表示。 ### 4. 论文报告的性能数字 **Pre-training**: - 4/6 使 NVFP4 训练损失向 BF16 **靠近了 22.3%** - 模型架构: Nemotron 3 Nano 30B-A3B（混合 Mamba-Transformer MoE 架构） - 训练规模: 1T tokens，384 个 B200 GPU **Post-Training Quantization (PTQ)**: - **+ AWQ + 4/6**: WikiText-2 平均 perplexity 11.58，C4 平均 perplexity 32.36（所有测试模型中最佳） - **+ AWQ + 4/6**: Perplexity 比 BF16 差距缩小 **19.9%**；+ SmoothQuant + 4/6 缩小 **5.3%** - **+ GPTQ + 4/6**: 反而使 NVFP4 与 BF16 的差距平均**扩大了 34.6%**（论文明确指出 GPTQ+4/6 效果不佳） - 下游任务（BoolQ, ARC, HellaSwag）上，4/6 在绝大多数情况下提升平均性能 **实现开销**: 4/6 在 CUDA kernel 中实现，所有中间值保持在寄存器文件中，开销**低于 15%**。 --- ## 论文二：Medusa -- 验证报告 ### 1. 论文标题、作者、Venue - **标题**: […]
