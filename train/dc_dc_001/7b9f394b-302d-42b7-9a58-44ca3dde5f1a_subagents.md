> DEVELOPER

深入调查 Eagle-3 (EAGLE-3) speculative decoding 的架构设计和改进点。需要做两件事： 1. **本地代码调查**：仔细阅读 /user_4813494d/openbmb 仓库中所有 Eagle 相关代码和文档，重点关注： - demo-sala/sglang/python/sglang/srt/speculative/ 目录下所有文件 - docs/eagle/ 目录下所有文档 - eagle/ 目录下的训练和数据管线 - 当前生产配置：spec_steps=2, topk=2, dtn=5 - draft model 的架构（eagle_draft/config.json） - tree verify 的实现细节 - CUDA graph capture 对 spec 的支持 2. **在线调研**：搜索 Eagle-3 / EAGLE speculative decoding 的最新论文和实现，重点关注： - EAGLE-3 vs EAGLE-2 vs EAGLE-1 的核心区别 - tree structure / draft chain 的设计改进 - fused GLA 在 draft model 中的应用 - acceptance rate 优化的最新方法 - SGLang 对 EAGLE 的适配细节 输出要求：用简体中文，详细列出发现，按"本地代码发现"和"在线调研发现"分别组织。每个发现点要包含具体文件路径和行号（本地）或来源链接（在线）。

> AGENT

我开始对 Eagle-3 speculative decoding 进行全面调查，同时进行本地代码阅读和在线调研。 先并行读取本地关键文件和启动在线搜索。

> DEVELOPER

深入调查 EAGLE speculative decoding 在长上下文场景下 accept rate 坍缩（collapse）的问题。需要做两件事： 1. **本地代码调查**： - 仔细阅读 /user_4813494d/openbmb/docs/eagle/collapse-investigation.md 全文 - 阅读 /user_4813494d/openbmb/docs/eagle/ 目录下所有相关文档 - 查看 eagle_info.py 中的 collapse 监控代码（_COLLAPSE_COUNTERS, _COLLAPSE_LOG_K） - 查看 eagle_worker.py 中的 verify 逻辑 - 查看当前 phased verify 的实现（_verify_phased 方法） - 查看 eval/ 目录下的评测脚本，了解 accept rate 是怎么测量的 - 查看 bench/ 目录下的 benchmark 配置 2. **在线调研**：搜索以下主题： - speculative decoding long context acceptance rate degradation - draft model distribution shift in long sequences - tree speculative decoding acceptance rate optimization - EAGLE speculative decoding collapse / failure modes - 最新的 accept rate 改进方法（如 adaptive draft, context-aware draft, etc.） - GLA / linear attention 在长上下文下对 spec decoding 的影响 输出要求：用简体中文，详细列出发现。特别关注： - 坍缩的根因分析 - 已尝试的解决方案及效果 - 业界最新的解决方案 - 对当前 spec_steps=2, topk=2 配置的建议

> AGENT

我开始全面调查 EAGLE speculative decoding 在长上下文下 accept rate 坍缩的问题。先从本地代码和文档入手。

> AGENT

现在开始深入读取本地核心代码文件。

> AGENT

现在继续阅读其他相关文档和代码。

> DEVELOPER

深入调查 GLA (Gated Linear Attention) 混合线性注意力机制在推测解码 (speculative decoding) 中的交互问题。需要做两件事： 1. **本地代码调查**： - 阅读 /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/ 目录下所有相关文件 - 特别关注 hybrid_linear_attn_backend.py, minicpm_backend.py, simple_gla_decode_kernel.py - 查看 MiniCPM-SALA 的 32 层混合架构（8 standard + 24 GLA layers） - 查看 CUDA graph runner 中对 verify 模式的处理 - 查看 dense_len=8192 和 InfLLM-v2 稀疏注意力的实现 - 查看 simple_gla_decode_kernel.py 中新增的 _simple_gla_decode_update_kernel - 查看 phased verify 对 GLA state 的影响（Phase-2 GLA initial state 使用 pre-draft production state 的 approximation） - 查看 model_runner.py 中 forward_decode 的 dispatch 逻辑 2. **在线调研**：搜索以下主题： - Gated Linear Attention (GLA) speculative decoding compatibility - linear attention state management during speculative decoding - MiniCPM linear attention hybrid architecture - RetNet / GLA / TransNormerLLM speculative decoding challenges - stateful attention kernels + speculative decoding interaction - Triton kernel optimization for GLA decode - FlashInfer + linear attention integration - 2024-2025 最新关于混合注意力 + spec decoding 的论文 输出要求：用简体中文，详细列出发现。特别关注： - GLA state 更新在 spec verify 时的正确性风险 - 新增 _simple_gla_decode_update_kernel 的设计意图 - phased verify 的 GLA state approximation 是否可接受 - 业界对 stateful attention + spec decoding 的最新解决方案

> AGENT

继续读取更多关键文件。

> AGENT

有很多相关文档。让我继续读取更多关键文件。

> AGENT

我来深入调查 GLA 混合线性注意力机制在推测解码中的交互问题。先从本地代码阅读开始。

> AGENT

现在读取更多关键文件和在线调研 EAGLE-3 论文核心区别。

> AGENT

继续读取剩余的相关文档。

> AGENT

本地代码和文档已全部阅读完毕。现在进行在线调研。

> DEVELOPER

深入调查 SGLang 框架在 speculative decoding 方面的最新进展和优化。需要做两件事： 1. **本地代码调查**： - 阅读 /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/ 目录下所有文件 - 特别关注 eagle_worker.py 的完整实现（包括 _verify_phased 方法） - 查看 cuda_graph_runner.py 中对 spec decode 的 CUDA graph 支持 - 查看 model_runner.py 中对 speculative 模式的 dispatch - 查看 minicpm_backend.py 中对 TARGET_VERIFY 的处理 - 查看 docs/runtime.md 和 docs/eagle/ 目录下的性能优化记录 - 查看 bench/ 目录下的 benchmark 配置和结果 2. **在线调研**：搜索以下主题： - SGLang speculative decoding latest improvements 2024-2025 - SGLang EAGLE integration - speculative decoding CUDA graph capture optimization - SGLang speculative decoding performance benchmarks - tree verification vs chain verification speculative decoding - Medusa vs EAGLE vs other spec decoding methods comparison 2025 - speculative decoding for quantized models (NVFP4, GPTQ) - spec decoding + KV cache management optimization - 量化模型 (FP4/INT4) 对 speculative decoding accuracy 的影响 输出要求：用简体中文，详细列出发现。特别关注： - SGLang 上游对 EAGLE 的最新改进 - CUDA graph capture 在 spec decode 中的最新优化方法 - 量化模型 spec decoding 的挑战和解决方案 - 对当前配置（NVFP4 + EAGLE-3 + spec_steps=2/topk=2）的改进建议

> AGENT

继续读取更多关键文件。

> AGENT

minicpm_backend.py 太大了，我分段读取关键部分。

> AGENT

我来进行全面的本地代码调查和在线调研。先并行启动多个方向的调查。

> AGENT

最后再读取几个重要文件完成调查。

> AGENT

现在并行读取关键文件。

> AGENT

继续读取关键文件。

> AGENT

注意到一个关键细节：生产部署的 `sglang_model/config.json` 已经用 `rope_theta=1000000`，但 `eagle_aux_hidden_state_layer_ids` 仍是 `[1, 10, 22]`（v2 层）。而 `demo-sala/data/eagle_draft/config.json` 也是 `[1, 10, 22]`。让我确认当前启动配置。

> AGENT

现在让我查看 model_runner.py 中的 forward_decode dispatch 逻辑。

> AGENT

现在读取更多关键文件和启动在线调研。

> AGENT

现在让我查看 MambaPool 中的 SpeculativeState 和 intermediate_ssm 的内存分配。

> AGENT

现在进行在线调研部分。

> DEVELOPER

纯在线论文调研，不读本地代码。用简体中文回复。 深入搜索以下主题的最新论文和技术报告（2024-2026），每个主题至少找到3-5篇相关论文，给出论文标题、作者、时间、核心贡献、arxiv链接： 1. **EAGLE / EAGLE-2 / EAGLE-3 speculative decoding** - 搜索 "EAGLE speculative decoding" "EAGLE-3" "EAGLE-2" - 各版本的核心区别是什么？draft model架构、tree structure、verify机制分别怎么改的？ 2. **Speculative decoding acceptance rate optimization** - 搜索 "speculative decoding acceptance rate" "speculative decoding adaptive draft" - 最新的 accept rate 提升方法：adaptive draft length, context-aware drafting, reward-guided spec等 3. **Tree/chain speculative decoding最新进展** - 搜索 "tree speculative decoding" "chain verification speculative" "speculative decoding tree structure optimization" - 2024-2025年最新的tree spec decoding方法，与EAGLE的对比 4. **Speculative decoding for quantized models** - 搜索 "speculative decoding quantized model" "FP4 speculative decoding" "GPTQ speculative decoding" - 量化对draft model精度的影响，量化模型spec decoding的特殊挑战 5. **Medusa / SpecInfer / other speculative methods vs EAGLE** - 搜索对比类论文 对每篇论文，给出：标题、arxiv ID、核心idea一句话、与当前项目（MiniCPM-SALA + EAGLE-3 + NVFP4）的关联度评估。

> AGENT

我来对这5个主题进行系统性的在线论文调研。

> DEVELOPER

纯在线论文调研，不读本地代码。用简体中文回复。 深入搜索以下主题的最新论文和技术报告（2024-2026），每个主题至少找到3-5篇相关论文： 1. **长上下文下speculative decoding accept rate退化** - 搜索 "long context speculative decoding" "speculative decoding long sequence acceptance rate" - 为什么长上下文下accept rate会退化？根因分析 - 业界提出的解决方案 2. **Draft model distribution shift** - 搜索 "draft model distribution shift" "speculative decoding distribution mismatch" - draft model和target model在长序列上的分布偏差 - 上下文长度增加时draft model的预测质量如何变化 3. **Context-aware / adaptive speculative decoding** - 搜索 "adaptive speculative decoding" "context-aware draft model" - 根据当前context动态调整draft策略的方法 - 动态调整spec steps、topk、draft length的方法 4. **Speculative decoding with stateful attention (GLA/linear attention)** - 搜索 "linear attention speculative decoding" "GLA speculative decoding" "stateful attention draft model" - 线性注意力/状态化注意力在spec decoding中的特殊挑战 - state rollback / state consistency 问题 5. **Accept rate collapse / failure modes in speculative decoding** - 搜索 "speculative decoding failure" "speculative decoding collapse" "accept rate zero" - spec decoding的典型失败模式 - 如何检测和恢复 对每篇论文，给出：标题、arxiv ID、核心idea一句话、与当前问题（MiniCPM-SALA EAGLE-3 长上下文accept rate偶发坍缩）的关联度评估。

> AGENT

现在读取更多关键文件来完善调查。

> AGENT

我将对这五个主题进行系统性文献调研。先并行搜索所有主题。

> AGENT

第五个搜索额度用完了，让我用其他方式继续搜索 Medusa/SpecInfer 对比类论文，以及补充更多细节。

> DEVELOPER

纯在线论文调研，不读本地代码。用简体中文回复。 深入搜索以下主题的最新论文和技术报告（2024-2026），每个主题至少找到3-5篇相关论文： 1. **Gated Linear Attention (GLA) 最新进展** - 搜索 "Gated Linear Attention" "GLA attention mechanism" - GLA的架构演进、训练技巧、推理优化 - GLA与标准attention的混合架构设计 2. **Linear attention + speculative decoding交互** - 搜索 "linear attention speculative decoding" "recurrent state speculative decoding" - 线性注意力/循环状态在spec decode verify时的state管理问题 - state rollback机制、KV cache与recurrent state的协调 3. **Hybrid attention architecture (混合注意力架构)** - 搜索 "hybrid attention architecture" "mix standard linear attention" "Jamba Mamba attention hybrid" - 2024-2025年混合架构的最新设计：哪些层用standard、哪些用linear - 混合架构对推理速度和准确率的影响 - MiniCPM的8 standard + 24 GLA设计在业界的位置 4. **Triton kernel优化 for linear attention decode** - 搜索 "Triton kernel linear attention" "GLA Triton kernel optimization" "linear attention decode kernel" - 最新的Triton kernel优化技术 - state update kernel的设计（incremental vs full recomputation） - warp配置、shared memory优化 5. **MiniCPM / MiniCPM-SALA 相关论文** - 搜索 "MiniCPM" "MiniCPM-SALA" "MiniCPM3" "OpenBMB MiniCPM" - MiniCPM系列的技术演进 - SALA架构的设计论文 6. **FlashInfer + linear attention integration** - 搜索 "FlashInfer" "FlashInfer linear attention" "FlashInfer speculative decoding" - FlashInfer对speculative decoding的支持 - FlashInfer对混合注意力后端的支持 对每篇论文，给出：标题、arxiv ID、核心idea一句话、与当前项目（MiniCPM-SALA 32层混合 + EAGLE-3 spec + simple_gla_decode_kernel）的关联度评估。

> AGENT

Tavily搜索配额已耗尽，让我切换到其他搜索方式继续调研。

> AGENT

我将对这6个主题进行全面的在线论文调研。让我并行搜索所有主题。

> AGENT

Tavily 额度已用尽。让我用已有的搜索结果，结合额外的 Google Scholar 搜索来补充。

> AGENT

Tavily配额用尽，让我用arxiv API直接搜索。

> AGENT

Tavily 搜索配额已用尽。让我尝试用 `tavily_research` 工具进行深度研究，它的配额可能是独立的。

> AGENT

Tavily 的所有端点都超配额了。让我尝试通过 crawl 和 extract 工具直接访问 arxiv 和相关页面来搜索论文。

> AGENT

所有 Tavily 工具均超配额。让我尝试用 Google Scholar 和 Semantic Scholar 的 API 来搜索论文。

> AGENT

arxiv API似乎不可用，让我换用Semantic Scholar API。

> AGENT

Semantic Scholar 限流了。让我等待一下再分批请求。

> AGENT

现在我已经完成了所有本地代码文档阅读和在线调研。下面整理完整的调查报告。 --- # EAGLE Speculative Decoding 长上下文 Accept Rate 坍缩深度调查报告 ## 一、坍缩现象总结 ### 1.1 核心表现 线上偶发：单个请求在长生成中段，`accept_len` 严格落到 1.0（spec_steps + tree 全废，只剩 bonus user_4813494d token），且持续 N 步不恢复。吞吐从 ~200 tok/s 跌到 99 tok/s。 ### 1.2 量化数据 | 场景 | accept_len | |---|---| | 编程样本 adj_al | 2.3-2.8 | | 短 deepresearch adj_al | 1.5-2.0 | | 超长 deepresearch（p_tok > 120K）adj_al | **1.24-1.30** | | idx 17（15K prompt）pre-EOS 段 al | 0.737（al==0 占 48.9%）| | aggregate al（raw，含结构 miss）| 1.865 | | aggregate al（miss-excluded adj_al）| **2.298（+23%）** | --- ## 二、根因分析（五条独立根因，已实证确认） ### 根因 1：RoPE 位置外推失效（已解决） **机制**：Draft 模型 `rope_theta` 默认 10000，训练序列约 2048 tokens。推理时 130K prompt 使得位置编码在 ~64x 外推区间工作，sin/cos phase 周期折叠，draft attention 对长距 token pair 的 score 退化。 **实证**：已通过 `rope_theta=1000000` 验证修复，长 deepresearch（120K-133K）al 提升 56%-78%，全量 64 样本长 context 组 al 从 1.395 涨到 2.022（+44.9%）。**已落地到 production config。** **代价**：短 coding（idx 1, 157 tokens）al 从 2.356 降到 1.425，但不影响 benchmark critical path。 ### 根因 2：训练位置分布偏斜 **机制**：短序列样本多 -> 小位置（0-2K）被过度训练，大位置（>2K）覆盖极少。Draft 在大位置 token 的 next-token 预测分布受训练不足。 **文献支撑**：LongSpec (ACL 2025, arXiv:2502.17421) 图 5 显示 EAGLE 在 position > 2K 的 acceptance 曲线下坠；提出 Anchor-Offset Indices (AOI)，前 4 个 token 锚定在 [0,1,2,3]，后续 position_ids 从随机 offset（0-30K）开始连续递增，训练收敛速度 3.93x 提升。 **当前状态**：v2/v3 draft 训练数据集长度分布未专门处理此问题。需重训 draft 才能根治（破红线）。 ### 根因 3：Target Hidden State 分布漂移 **机制**：EAGLE-3 draft 使用目标模型中间层 hidden state 作为输入特征（aux_hidden）。超长上下文下，attention sink 被 InfLLM-v2 sparse 稀疏机制放大，中间层 feature 分布与短上下文训练时不同。Draft 的 fc 层（12288 -> 4096）接收到协变量漂移的输入。 **文献支撑**：OWL (EMNLP 2025, arXiv:2510.07535) 专门研究此问题，提出 LSTM drafter 只消费最后 1 个 token 的 hidden state，LongSpecBench 上 acceptance=4.00 vs EAGLE-3 的 1.28。 ### 根因 4：InfLLM-v2 Sparse / Draft Dense 注意力不对称 **机制**：超过 dense_len=8192 后，target 的 8 个 standard attention 层走稀疏 attention（只对 top-K 个 block 做 FA），而 draft 始终是全量 dense attention。Target 的 KV 视野与 draft 完全不同，产生系统性预测偏差。 **文献支撑**：QuantSpec (2025) 3.1 节："the mismatch between compressed KV in target and full KV in draft is an independent degradation source"；OWL 2 节将此归类为独立于 RoPE extrapolation 的 "attention regime mismatch"。 **当前状态**：这是 MiniCPM-SALA 混合架构（8 Attention + 24 GLA）特有的问题。GLA 层本身就是 linear attention 不走 sparse，但 8 个 standard attention 层 >8192 后走 InfLLM-v2。未修。 ### 根因 5：Draft 训练数据领域覆盖不足（已实证确认的主因） **机制**：Draft 在特定 prompt 类型上的 top-k 预测漏掉 target argmax。不是 RoPE 或 hidden drift 问题，而是纯粹的训练分布盲区。 **实证数据**： - idx 17 pre-EOS 段 65/133 步 al==0，其中 60 步是 "target IN hot_set, NOT in draft top-2"（draft 词表覆盖到了 target token，但 draft 预测排名不够高） - collapse 段 target logit gap p50=2.75（vs 健康段 5.06），说明 target 自己在高熵位置，但 draft 失败率更高 - **连续 collapse 机制**：单点翻转把路径推入 draft 分布盲区连续段 -> 整段 al==0，直到 target commit 到 draft 熟悉的语义边界才恢复 - v3 draft 在 long deepresearch 上反而比 v2 更糟（idx 17 long-gen al=0.578 vs v2 0.737） **已排除的虚假根因**： - CUDA graph / FP4 量化（toggle 实验无法消除 collapse） - […]

> AGENT

现在我有足够的信息来输出完整的调查报告了。 --- # EAGLE-3 Speculative Decoding 深度调查报告 ## 一、本地代码发现 ### 1. Draft Model 架构 **文件**: `/user_4813494d/openbmb/demo-sala/data/eagle_draft/config.json`（行 1-30） 当前生产 draft model 架构为 `LlamaForCausalLMEagle3`，核心参数： - **1 层 Transformer decoder**（`num_hidden_layers: 1`） - `hidden_size=4096`, `intermediate_size=16384`, GQA 32h/2kv, `head_dim=128` - `vocab_size=73448`（target 全词表），`draft_vocab_size=32000`（draft 子词表，覆盖率 99.23%） - `scale_emb=12`（embedding 缩放因子） - `rope_theta=1000000`（已从默认 10000 升级，verify-experiments-log 确认对长 context 有 +56-78% al 提升） - `eagle_config.use_aux_hidden_state=true`, `eagle_aux_hidden_state_layer_ids=[1, 10, 22]` **架构全貌**（`docs/eagle/README.md` 行 16-28）： ``` Eagle3Model (~437M trainable): fc: Linear(12288 → 4096) # 融合 3 层 aux hidden midlayer: Eagle3DecoderLayer # 完整 decoder layer self_attn: Eagle3Attention (GQA 32h/2kv) mlp: SwiGLU (4096 → 16384 → 4096) embed_tokens: Embedding(73448, 4096) [FROZEN] lm_head: Linear(4096 → 32000) # 32K draft 词表 ``` fc 层将 3 层 aux hidden（`hidden_size × 3 = 12288`）映射到 draft 的 `hidden_size=4096`。self_attn 的 Q/K 输入为 `cat(normed_embed, normed_hidden)`。 ### 2. 当前生产配置 **文件**: `/user_4813494d/openbmb/eval/start_eagle.sh`（行 24-66） - `spec_steps=2`, `topk=2`, `dtn=5`（`dtn = 1 + topk * spec_steps`） - 注释说 `topk=1, dtn=3`，但实际默认 `TOPK=2`——注释和代码不一致，当前生产是 **topk=2 tree verify** - `speculative-algorithm EAGLE3` - draft model 路径: `/user_4813494d/openbmb/demo-sala/data/eagle_draft`（v2, 415 MB safetensors） - target model: NVFP4 量化（`modelopt_fp4`） - `SGLANG_ENABLE_SPEC_V2=0`（使用 v1 EAGLEWorker，不用 overlap v2） - Draft 专用 `flashinfer` attention backend（不从 target 的 `minicpm_flashinfer` 继承） ### 3. EAGLE Worker 两套实现 **V1（生产路径）**: `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py` - 类 `EAGLEWorker(TpModelWorker)`，行 145-1400 - 完整 decode 流程: `forward_batch_generation()` → `draft()` → `verify()` → `forward_draft_extend_after_decode()` - 包含 MiniCPM-SALA 专属修复： - `_alloc_sparse_for_new_positions()`（行 1174-1228）：verify 后手动分配 InfLLM-v2 sparse k1/k2 slots - `_mamba_verify_update()`（行 909-1010）：GLA/mamba state rollback，使用 `update_mamba_state_after_mtp_verify` - Phased verify 实现 `_verify_phased()`（行 1011-1172）：两阶段 TARGET_VERIFY，Phase-1 3 token + Phase-2 2 token，可 early exit - Draft model 量化自动检测 `_detect_draft_model_quantization()`（行 88-142），支持 NVFP4 pre-quantized draft - KV cache slot 释放时序修复：verify() 开头释放 draft slots（行 805-806） **V2（overlap 路径）**: `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py` - 类 `EAGLEWorkerV2(BaseSpecWorker)` + `EagleDraftWorker(BaseDraftWorker)` - 拆分为 draft worker 和 verify worker，支持 overlap scheduling - 通过 `SGLANG_ENABLE_SPEC_V2=1` 启用 - 当前生产**未启用** v2（start_eagle.sh 行 49 显式设 `SGLANG_ENABLE_SPEC_V2=0`） ### 4. Tree Verify 核心实现 **文件**: `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py` **EagleVerifyInput**（行 82-723）: - `retrive_index`, `retrive_next_token`, `retrive_next_sibling`：tree 结构索引，由 `sgl_build_tree_kernel_efficient` CUDA kernel 生成 - `verify()` 方法（行 244-723）：核心 verify 逻辑 - Greedy 路径：`verify_tree_greedy_func()`（sgl_kernel CUDA kernel） - Sampling 路径：`tree_speculative_sampling_target_only()`（sgl_kernel CUDA kernel） - 包含 Collapse 监控：连续 K=10 步 `accept_len==0` 时 log warning（行 511-529） - EAGLE trace 输出：`EAGLE_TRACE_FILE` 环境变量控制的 per-step trace（行 423-466） - KV cache 回收：page_size=1 直接 free；topk>1 + page_size>1 需要移动 accepted token 到连续位置 **EagleDraftInput**（行 727-1030）: - `topk_p`, `topk_index`, `hidden_states`：draft 模型输出 - `prepare_extend_after_decode()`：构建 draft extend 的输入（行 809-879） - EAGLE-3 的 `capture_hidden_mode` 设为 `LAST`（只需最后一层 hidden state 做下次 draft 输入） ### 5. Tree 构造算法 **文件**: `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_utils.py` - `build_tree_kernel_efficient()`（行 47-158）：调用 `sgl_build_tree_kernel_efficient` CUDA kernel - 输入：`parent_list`, `top_scores_index`, `draft_tokens`, `seq_lens` - 输出：`tree_mask`, `positions`, `retrive_index`, `retrive_next_token`, `retrive_next_sibling` - 支持 `TreeMaskMode`：`FULL_MASK`（完整 tree mask）、`QLEN_ONLY`（只存 query 部分）、`QLEN_ONLY_BITPACKING`（bit-packed） - `organize_draft_results()`（行 […]

> AGENT

找到了一批论文。让我继续搜索更多相关主题。

> AGENT

Semantic Scholar 恢复了。现在让我分批搜索所有6个主题。

> AGENT

现在我已经收集了足够的信息，可以进行综合分析了。 --- # SGLang Speculative Decoding 深度调查报告 ## 一、本地代码调查 ### 1.1 Speculative 目录结构 `demo-sala/sglang/python/sglang/srt/speculative/` 下共 21 个 Python 文件，总计约 10,249 行代码。核心组件： | 文件 | 行数 | 职责 | |---|---|---| | `eagle_worker.py` | 1416 | V1 EAGLE Worker 主控，含 draft/verify/_verify_phased/alloc_sparse | | `eagle_worker_v2.py` | 838 | V2 overlap-schedule 版 EAGLE Worker | | `eagle_info.py` | 1104 | EagleDraftInput/EagleVerifyInput/EagleVerifyOutput 数据结构 + verify 逻辑 | | `eagle_info_v2.py` | 489 | V2 版 spec_info mixin | | `eagle_utils.py` | 199 | build_tree_kernel_efficient + verify_tree_greedy_func | | `eagle_draft_cuda_graph_runner.py` | 396 | Draft decode 的 CUDA graph capture/replay | | `eagle_draft_extend_cuda_graph_runner.py` | 498 | Draft extend 的 CUDA graph capture/replay | | `spec_utils.py` | 744 | Triton kernel + 通用 spec 工具函数 | | `multi_layer_eagle_worker.py` | 752 | 多层 EAGLE Worker | | `medusa_worker.py` | 697 | Medusa K-head spec worker | ### 1.2 eagle_worker.py 核心流程 **forward_batch_generation** 是入口，分两个路径： - **Extend 路径**：先跑 target forward（CaptureHiddenMode.FULL），再跑 draft extend - **Decode 路径**：先 draft（生成候选树），再 verify（target 单次前向验证），最后 draft_extend_after_decode **_verify_phased 方法**（env-gated，`EAGLE_PHASED_VERIFY=1`）：两阶段 TARGET_VERIFY： - Phase-1: 3-token forward [dt0,dt1,dt2] - Early-exit 检测：若 `pr[0]` 不在 {dt1,dt2} 则跳过 Phase-2 - Phase-2: 2-token forward [dt3,dt4]（仅当 Phase-1 有匹配时） - 离线 trace 分析：full bench 下 early_exit 率 48.6%，vlong bucket（>=50K prompt）达 68.3% **关键适配**： - Draft model 量化自动检测（`_detect_draft_model_quantization`）：扫描 hf_quant_config.json / config.json 的 NVFP4 标记 - Draft attention backend 隔离：minicpm_flashinfer -> flashinfer - GLA tree-aware verify：通过 `update_mamba_state_after_mtp_verify` 做 GLA state rollback - `_alloc_sparse_for_new_positions`：为 InfLLM-v2 sparse k1/k2 分配 slot（EAGLE 跳过了正常 decode 的 batch alloc 路径） ### 1.3 CUDA Graph 在 Spec Decode 中的架构 三套独立的 CUDA graph runner： 1. **EAGLEDraftCudaGraphRunner**：Draft decode 阶段。`num_tokens_per_bs = topk`，每个 batch size capture 一个 graph。支持 padding 到更大 bs。内部 replay `eagle_worker.draft_forward`。 2. **EAGLEDraftExtendCudaGraphRunner**：Draft extend 阶段。`num_tokens_per_bs = spec_steps + 1`。支持 EAGLE-3 的 aux hidden state（3x hidden_size）。内部 replay `model_runner.model.forward` + softmax + fast_topk。 3. **目标 CudaGraphRunner**（cuda_graph_runner.py）：Target verify 阶段。Phased verify 模式下需 capture 两种形状（3 tokens/req 和 2 tokens/req），这是主要风险点。 **内存池共享问题**（已知 bug #22930）：Draft 和 target 共享 `get_global_graph_memory_pool()`，当 target 使用 KVTC 时 draft graph capture 会覆盖 target 的 pool 地址。修复方案：draft capture 完成后重跑一次 target graph capture（+0.6s 启动开销）。 ### 1.4 minicpm_backend.py 中 TARGET_VERIFY 处理 - `MiniCPMBackendMetadata` 包含 `verify_prefill_wrapper` 字段，用于 TARGET_VERIFY 时使用 FlashInfer prefill wrapper（CUDA graph 兼容） - Sparse attention 路径在 TARGET_VERIFY 下也走 InfLLM-v2 sparse，但需手动调用 `_alloc_sparse_for_new_positions` 分配 k1/k2 slot - verify 后需调用 `update_mamba_state_after_mtp_verify` 做 GLA state 更新（经 profiling 确认占 1.65% e2e 时间，98.4% 的 index kernel 时间来自此函数的 3D fancy scatter） ### 1.5 性能优化记录摘要 **docs/runtime.md 核心结论**： - **Draft 不是瓶颈**（4.7% GPU 时间，0.53 ms/call） - **GEMM 不是大头**（7.3% GPU 时间）；b12x 28% GEMM 省 = 2% e2e - **Target verify GPU 时间 10.6 ms/call**，占 95.3% - **Index 操作**（`update_mamba_state_after_mtp_verify` […]

> AGENT

让我继续补充关键论文的详细信息。

> AGENT

Semantic Scholar有速率限制。让我用更宽泛的关键词搜索，并获取摘要。

> AGENT

又限流了。让我用更长的间隔分批请求。

> AGENT

让我尝试用arxiv的直接搜索页面，以及使用不同的策略来获取论文信息。

> AGENT

找到了关键论文。继续搜索更多主题。

> AGENT

Semantic Scholar 持续限流。让我换用直接爬取 arxiv 搜索页面的方式。

> AGENT

非常好，找到了大量相关论文。让我继续搜索更多关键主题，并获取已找到论文的详细摘要。

> AGENT

现在让我查看 Together AI 关于混合模型推测解码的关键工作。

> AGENT

现在我已经收集了足够的信息。让我整合所有搜索结果，撰写完整的调研报告。 --- # Speculative Decoding 最新论文调研报告（2024-2026） --- ## 1. EAGLE / EAGLE-2 / EAGLE-3 Speculative Decoding ### 1.1 EAGLE-1: Speculative Sampling Requires Rethinking Feature Uncertainty | 字段 | 内容 | |---|---| | **标题** | EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty | | **arxiv ID** | 2401.15077 | | **作者** | Yuhui Li, Fengxuan Li, Tianle Cai, Hao Zhang, Ziteng Sun 等 | | **时间** | 2024年1月 (ICML 2024) | | **核心idea** | 在target model的次顶层特征(feature)层面做自回归draft，而非token层面；通过建模feature的不确定性（采样而非取argmax）来提升accept rate | | **与项目关联度** | **极高** -- 项目当前EAGLE-3 draft的架构根基；feature-level autoregression是v1的核心创新 | **关键设计**： - Draft model仅1层transformer decoder，输入target model次顶层hidden state - 采样feature而非确定性预测，解决feature不确定性被忽略的问题 - 使用固定的25节点heuristic draft tree ### 1.2 EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees | 字段 | 内容 | |---|---| | **标题** | EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees | | **arxiv ID** | 2406.16858 | | **作者** | Yuhui Li, Tianle Cai, Ziteng Sun 等 | | **时间** | 2024年6月 (EMNLP 2024) | | **核心idea** | 将固定draft tree改为动态draft tree，根据draft model的confidence自适应调整tree结构，高置信度位置扩展更多分支 | | **与项目关联度** | **极高** -- 当前项目`spec_steps=2, topk=2`的chain verify就是EAGLE-2动态树的简化版；tree结构优化是提升accept rate的关键方向 | **关键改进（vs EAGLE-1）**： - EAGLE-1用固定25节点树 -> EAGLE-2用动态树，每步根据draft confidence决定广度和深度 - 高confidence token处扩展子树，低confidence处剪枝 - 比EAGLE-1快1.4x（13B模型） ### 1.3 EAGLE-3: Scaling up Inference Acceleration via Training-Time Test | 字段 | 内容 | |---|---| | **标题** | EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test | | **arxiv ID** | 2503.01840 | | **作者** | Yuhui Li, Ziteng Sun, Tianle Cai 等 | | **时间** | 2025年3月 (NeurIPS 2025) | | **核心idea** | 放弃feature prediction改为direct token prediction；用多层特征融合（低/中/高层语义）替代仅依赖顶层feature；引入training-time test机制让draft model在训练时模拟推理 | | **与项目关联度** | **极高** -- 项目正在使用的核心方法；多层特征融合直接适用于MiniCPM-SALA的32层混合架构 | **关键改进（vs EAGLE-2）**： - EAGLE-1/2在feature level做自回归 -> EAGLE-3改为direct token prediction - 仅用顶层hidden state -> 融合低/中/高三层feature（语法 + 语义 + 概率分布） - 发现scaling data对EAGLE-1/2提升有限（受feature prediction天花板约束），EAGLE-3打破此限制 - 速度提升：比vanilla decoding快5.6x（13B），比EAGLE-1快1.8x - SGLang框架中batch=64时吞吐提升1.38x **三个版本核心区别总结**： | 维度 | EAGLE-1 | EAGLE-2 | EAGLE-3 | |---|---|---|---| | Draft架构 | Feature-level AR | Feature-level AR | Direct token prediction | | 输入特征 | 次顶层hidden state | 次顶层hidden state | 多层feature fusion（低/中/高） | | Tree结构 | 固定25节点heuristic | 动态树（confidence-adaptive） | 继承EAGLE-2动态树 | | Verify机制 | Speculative sampling | Speculative sampling | Speculative sampling | | 训练方法 | 标准训练 | 标准训练 | Training-time test（推理时模拟） | | 速度提升 | 4x vs vanilla | 1.4x vs EAGLE-1 | 1.4x vs EAGLE-2 | ### 1.4 P-EAGLE: Parallel Speculative Decoding (AWS/vLLM) | 字段 | 内容 | |---|---| | **标题** | P-EAGLE: Faster LLM Inference with Parallel Speculative Decoding in vLLM | | **arxiv ID** | 暂无独立arxiv（AWS ML […]

> AGENT

Arxiv API 也限流了。让我等待然后逐个请求，使用更大的间隔。

> AGENT

arxiv API 也在限流。让我改用另一个策略——直接用已知的 arxiv ID 来获取论文详情，同时尝试 Semantic Scholar 的单篇论文查询（限流可能只针对搜索端点）。

> AGENT

找到了 MiniCPM-SALA 的论文。让我继续搜索其他主题。

> AGENT

现在我已经收集了足够的信息。让我综合本地代码和在线调研的发现，撰写详细报告。 --- # GLA 混合线性注意力与推测解码交互问题深度调查报告 ## 一、架构总览 MiniCPM-SALA 采用 32 层混合架构： - **8 层 Standard Attention**（layer id = 0, 9, 16, 17, 22, 29, 30, 31）：使用 FlashInfer/FA3 + InfLLM-v2 稀疏注意力（序列超过 dense_len=8192 时触发） - **24 层 Lightning Attention (GLA)**（其余层）：使用 SimpleGLA 后端，基于 ALiBi 斜率的固定 decay，无卷积 推测解码配置为 EAGLE-3 chain verify：`spec_steps=2, topk=2, dtn=5`，即每个请求 5 个 draft token（树结构：根 + 2 个子节点各延伸 2 步）。 ## 二、GLA State 在推测解码中的生命周期 ### 2.1 正常 Decode 路径 在 `SimpleGLAAttnBackend.forward()` 中（`hybrid_linear_attn_backend.py:1952-2104`），decode 路径有两个分支： 1. **`simple_gla_decode_update_fwd`**（默认路径，`SGLANG_SIMPLE_GLA_DIRECT_DECODE=1`）：自定义 Triton kernel，直接在 kernel 内读写 `layer_cache.temporal[state_indices]`，无需外部的 `contiguous()` gather + index_put 回写。仅支持 K=V=128，FP32 state。 2. **FLA 原生 `fused_recurrent_simple_gla`**：需要先 `state[indices].contiguous()` 读取，再 `state[indices] = final_state` 写回。 两者的核心状态更新公式相同： ``` h_t = exp(g_gamma) * h_{t-1} + k_t @ v_t^T o_t = (h_t @ q_t^T) * scale ``` 其中 `g_gamma` 是 ALiBi 斜率（负值），per-head 常量。 ### 2.2 TARGET_VERIFY 路径 — 中间状态缓存机制 这是 GLA 与推测解码交互的核心。代码路径在 `SimpleGLAAttnBackend.forward()` 第 2002-2046 行。 **关键设计**：verify 时不直接修改 `layer_cache.temporal`，而是将每一步的中间状态写入 `intermediate_ssm` 缓冲区。 ```python # hybrid_linear_attn_backend.py:2008-2014 spec_cache = self.req_to_token_pool.mamba_pool.get_speculative_mamba2_params_all_layers() intermediate_ssm = spec_cache.intermediate_ssm ht_buf = intermediate_ssm[cache_idx, :batch_size, :draft_token_num] ``` `intermediate_ssm` 的形状为 `(num_mamba_layers, pool_size+1, speculative_num_draft_tokens, HV, K, V)`，在 `MambaPool.__init__` 中预分配（`memory_pool.py:218-229`）。 核心 kernel `_fused_recurrent_gla_intermediate_kernel`（第 60-164 行）在每一步 step 后都保存 `ht_all`： ```python # 第 158 行 tl.store(p_ht, b_h.to(p_ht.dtype.element_ty), mask=m_h) ``` **树验证支持**：当 `topk > 1` 时，kernel 支持 `retrieve_parent_token`，根据树结构回溯到正确的父节点状态： ```python # 第 122-145 行 if HAS_EAGLE_TREE_CUSTOM_ATTN_MASK and step != 0: parent_step_idx = tl.sum(tl.where(token_indices == step, parent_idx_tokens, 0)) p_parent_ht = ht_all + ... + parent_step_idx * ht_stride_t + ... b_h = tl.load(p_parent_ht, ...) ``` 这意味着树结构中的每个节点不是简单的线性递推，而是从其父节点的中间状态恢复，避免了兄弟分支之间的"污染"。 ### 2.3 Verify 后的状态回写 — `update_mamba_state_after_mtp_verify` 在 `HybridLinearAttnBackend.update_mamba_state_after_mtp_verify()`（第 1632-1700 行）中，根据接受步数从 `intermediate_ssm` 中选择正确的状态写回 `layer_cache.temporal`： ```python ssm_states[:, dst_state_indices, :] = intermediate_state_cache[ :, src_state_indices, last_steps ].to(ssm_states.dtype, copy=False) ``` 这确保了被拒绝的 draft token 的状态更新不会污染生产状态。 ## 三、正确性风险分析 ### 3.1 GLA State 回滚的正确性 — 已实现，但需关注边界 **当前实现是安全的**：verify 阶段不修改 `temporal` state，所有中间状态写入独立的 `intermediate_ssm` 缓冲区。verify 结束后，`update_mamba_state_after_mtp_verify` 根据接受的步数从中间状态中选取正确的历史状态写回。 **潜在风险点**： 1. **`disable_state_update=True` 的 GDN 后端路径**（第 1349-1364 行）：GDN 后端在 verify 时使用 `fused_recurrent_gated_delta_rule_update` 并设置 `disable_state_update=True`，这意味着 kernel 不写入 `ssm_states`。但 SimpleGLA 后端的实现方式不同——它根本不传 `initial_state_source=ssm_states` 给 kernel，而是用 `initial_state = layer_cache.temporal[mamba_indices, :].contiguous()` 做只读读取。这两种方式等效，都是安全的。 2. **`intermediate_ssm` 数据竞争**：`_fused_recurrent_gla_intermediate_kernel` 中，树结构节点回溯父节点时通过 `tl.load(p_parent_ht, ...)` 读取同一个 `ht_buf` 中其他 step 已写入的状态。由于 Triton kernel 是同一个 grid 内顺序执行（每个 program 处理一个 (n, h) 对），**同一个 sequence 内的 step 是串行的**，所以不存在数据竞争。但如果不同 sequence 的 program 并行度导致某些 sequence 的 step 先执行，也不会有问题，因为每个 sequence 只读自己 `i_n` 的数据。 3. **`_build_retrieve_parent_token` 的正确性**：该函数（第 254-291 行）通过 BFS 从 `retrieve_next_token` 和 `retrieve_next_sibling` 构建父节点映射。需要确保 EAGLE 树的 sibling chain 结构在所有情况下都能正确解析。特别是当某个分支的 `next_sibling` 链较长时，BFS 的遍历顺序必须一致。 ### 3.2 Phased Verify 的 GLA State Approximation — 可接受但非完美 在 `_verify_phased()`（`eagle_worker.py:1011-1172`）中，两阶段 verify 的实现有一个明确的注释（第 1027-1032 行）： > "Phase-2 GLA initial state uses pre-draft production state (approximation acceptable for long sequences; state drift from 2 tokens is negligible)" 具体问题：Phase-2 的 2 个 token（dt3, dt4）的 GLA forward 从 `seq_lens + 3` […]

> AGENT

arxiv API也限速了。让我用Semantic Scholar继续，间隔更长时间。

> AGENT

让我使用串行方式，每个请求之间增加间隔来避免限流。

> AGENT

让我换一种方式来获取论文摘要，直接抓取arxiv HTML页面。

> AGENT

找到了大量相关论文。让我逐个获取这些关键论文的详情，然后继续搜索其他主题。

> AGENT

部分论文因太新而没有 S2 记录。让我直接从 arxiv 抓取摘要。

> AGENT

非常好，核心论文都找到了。让我继续搜索其他主题的论文。

> AGENT

很多结果不太相关。让我用更精确的搜索来找混合注意力架构和 speculative decoding 的论文。

> AGENT

arxiv搜索"speculative"太宽泛了。让我用更精确的方式搜索剩余主题，并获取一些重要论文的全文内容。

> AGENT

搜索结果不太相关。让我更精确地搜索GLA/状态化注意力相关的推测解码挑战。

> AGENT

EAGLE-3搜索结果太泛。基于已有知识，EAGLE-3的arxiv ID是2406.16858的后续工作。让我尝试已知的一些ID。

> AGENT

现在我已经收集了足够的论文信息。让我整理最终报告。

> AGENT

现在我已经收集了所有五个主题的论文数据。以下是完整的调研报告。 --- ## 主题1：长上下文下 Speculative Decoding Accept Rate 退化 ### 1.1 OWL: Overcoming Window Length-Dependence in Speculative Decoding for Long-Context Inputs - **Arxiv ID**: 2510.07535 (2025-10) - **核心idea**: 发现EAGLE-3在长上下文下acceptance length仅1.28（几乎无加速，甚至0.81x减速），提出LSTM drafter仅依赖last-token state以消除上下文长度依赖，加[SPEC] token增强verifier表示 - **与当前问题关联度**: **极高** -- 直接证明EAGLE-3在长上下文下严重退化，给出根因：EAGLE系列draft模型依赖KV cache的full-context attention，上下文越长draft模型的feature越偏移，导致draft-target分布mismatch急剧增大 ### 1.2 LongSpec: Long-Context Lossless Speculative Decoding with Efficient Drafting and Verification - **Arxiv ID**: 2502.17421 (2025-02, ICML 2025) - **核心idea**: 系统性归纳长上下文spec decoding三大挑战：(1) draft模型KV cache内存暴增；(2) 短上下文训练-长上下文推理的位置分布偏移(position distribution shift)；(3) 长序列tree attention效率低下。提出sliding-window+cross-attention的constant-size KV draft模型和anchor-offset position indices - **与当前问题关联度**: **极高** -- 对"为什么长上下文退化"给出最系统的分析，特别是**position distribution shift**理论：RoPE位置编码在训练时见过的位置范围与推理时不一致，导致attention分布偏移，直接损害draft质量 ### 1.3 SpecExtend: A Drop-in Enhancement for Speculative Decoding of Long Sequences - **Arxiv ID**: 2505.20776 (2025-05) - **核心idea**: 无需重新训练的即插即用方案。发现draft accuracy下降的两大根因：(1) KV cache加载开销使verify变慢；(2) **draft模型容量有限，无法在长上下文下保持与target一致的attention**。提出Cross-model Retrieval：用target模型的attention score动态选择draft模型应关注的KV条目 - **与当前问题关联度**: **高** -- 直接分析"smaller draft model在长上下文下的信息瓶颈"问题，Cross-model Retrieval思路可启发MiniCPM-SALA中GLA层的context selection ### 1.4 RAPID: Long-Context Inference with Retrieval-Augmented Speculative Decoding - **Arxiv ID**: 2502.20330 (2025-02, ICML 2025) - **核心idea**: 用RAG drafter在缩短的检索context上draft，避免长KV cache瓶颈。同一个量级甚至更大的模型也可作为RAG drafter。acceptance rate随context增长而下降，但RAPID在32K以上仍维持加速 - **与当前问题关联度**: **高** -- 提供了"缩短draft context"的解决思路，对MiniCPM-SALA混合架构的GLA层有参考价值 ### 1.5 TriForce: Lossless Acceleration of Long Sequence Generation with Hierarchical Speculative Decoding - **Arxiv ID**: 2404.11912 (2024-04) - **核心idea**: 分层speculative decoding：第一层用稀疏KV cache做draft，第二层用全量KV cache验证。KV cache线性增长是长序列decode的核心瓶颈 - **与当前问题关联度**: **中高** -- 层次化KV cache思路与MiniCPM-SALA的dense_len=8192后的稀疏attention架构天然契合 ### 1.6 MagicDec: Breaking the Latency-Throughput Tradeoff for Long Context Generation with Speculative Decoding - **Arxiv ID**: 2408.11049 (2024-08) - **核心idea**: 证明speculative decoding在大batch+长上下文下仍有效，因为长KV cache使decode重新变为memory-bound。但acceptance rate会随context增长而下降 - **与当前问题关联度**: **中** -- 提供了长上下文下spec decoding是否有效的理论框架，但对acceptance rate退化的根因分析较浅 --- ## 主题2：Draft Model Distribution Shift ### 2.1 LongSpec (同1.2) - **关键发现**: **Position distribution shift** -- draft模型在训练时使用短序列位置编码，推理时遇到未见过的长位置，RoPE的position index分布偏移导致attention pattern畸变。论文给出理论upper bound：DE = log(1 + d_V * exp(B)) * TV(p_sliding, p_full) - **与当前问题关联度**: **极高** -- MiniCPM-SALA使用RoPE + GLA混合，GLA层虽然无显式位置编码，但standard attention层的position shift同样会影响EAGLE-3的feature input ### 2.2 OWL (同1.1) - **关键发现**: EAGLE系列依赖full KV cache做draft，上下文越长draft model的hidden state越偏离训练分布。OWL用LSTM drafter仅依赖last-token state，完全消除对context长度的依赖 - **与当前问题关联度**: **极高** -- 直接解释了EAGLE-3在MiniCPM-SALA上的退化机制：EAGLE-3使用target model的feature层做autoregression，feature本身受长上下文影响 ### 2.3 SpecExtend (同1.3) - **关键发现**: draft模型的**limited capacity**导致它在长上下文下无法维持与target一致的attention distribution。越长的context意味着越多需要"记住"的信息，但小模型容量不够 - **与当前问题关联度**: **高** -- 容量瓶颈问题在MiniCPM-SALA上可能更严重，因为target是混合架构（8 standard + 24 GLA），而draft模型是标准transformer ### 2.4 QuantSpec: Self-Speculative Decoding with Hierarchical Quantized KV Cache - **Arxiv ID**: 2502.10424 (2025-02) - **核心idea**: 用量化KV cache做draft，全精度KV cache做verify。低精度KV cache引入的分布偏移直接影响draft acceptance rate - **与当前问题关联度**: **中** -- 量化引入的distribution shift与长上下文的shift叠加，可能是MiniCPM-SALA NVFP4量化+长上下文双重要素的根因 ### 2.5 Acceptance Dynamics Across Cognitive Domains in Speculative Decoding - **Arxiv ID**: 2604.14682 (2026-04) - **核心idea**: 系统研究不同认知领域（代码生成、数学推理、逻辑推理、聊天）对acceptance rate的影响。发现**task type是比tree depth更强的acceptance预测因子**。只有chat domain的expected accepted length > 1.0。entropy-acceptance相关性始终为负但较弱 - **与当前问题关联度**: **中高** -- 提供了acceptance rate退化的另一维分析：不同任务类型下draft-target分布偏差程度不同，推理型任务偏差最大，这与MiniCPM-SALA评测时观察到的偶发坍缩一致 --- ## 主题3：Context-Aware / Adaptive Speculative Decoding ### 3.1 EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees - **Arxiv ID**: 2406.16858 (2024-06) - **核心idea**: 发现draft token的acceptance rate不仅依赖位置，还**context-dependent**。提出根据当前context动态调整draft tree结构 - **与当前问题关联度**: **极高** -- 是EAGLE-3的直接前身，EAGLE-3继承了dynamic tree但未解决长上下文下的context adaptation问题 ### 3.2 TALON: Confidence-Aware Speculative Decoding with Adaptive Token Trees - **Arxiv ID**: 2601.07353 (2026-01) - **核心idea**: […]

> AGENT

现在我已经收集了足够多的论文信息。让我再搜索几个关键遗漏领域。

> TOOL

[Request interrupted by user]

> DEVELOPER

纯学术深度调研，用简体中文回复。不读本地代码。 聚焦 LongSpec (arXiv:2502.17421, ACL 2025) 的 Anchor-Offset Indices (AOI) 训练策略，深挖以下问题： 1. **AOI 的完整算法**： - 具体的 position_ids 构建流程是什么？ - anchor tokens 数量为什么选 4？是否可调？ - offset 的采样范围是多少？论文说"random offset"，具体是什么分布？均匀？对数？ - 训练和推理时 position_ids 的差异如何处理？ - RoPE 的 theta 如何配合 AOI？是否需要修改？ 2. **AOI 对 EAGLE-3 draft model 的影响**： - AOI 是只改 position_ids 还是也需要改 attention pattern？ - EAGLE-3 的 Training-Time Test (TTT) 与 AOI 是否兼容？TTT 本身已有多步自回归，AOI 的 position 在多步中如何递增？ - AOI 是否改变了 draft model 的 KV cache 大小？ 3. **实验数据深度**： - LongSpec 在不同 context length（4K, 16K, 64K, 128K）下的 acceptance length 是多少？ - AOI 相比无 AOI 的 acceptance 提升百分比分别是多少？ - 与 rope_theta scaling（如 1M）对比，AOI 的额外收益是多少？ 4. **适配 MiniCPM-SALA 的关键问题**： - MiniCPM-SALA 有 24 层 GLA（linear attention，无显式 RoPE），AOI 只影响 8 层 standard attention - 这种混合架构下 AOI 的效果是否打折？ - draft model 是标准 transformer（1 层 decoder），AOI 对 draft model 的 position encoding 影响是什么？ - 当前项目已用 rope_theta=1M，AOI 是否能与 rope_theta=1M 叠加？ 5. **LongSpec 的 Hybrid Tree Attention 实现细节**： - 具体的两阶段 attention 计算流程 - 与 FlashInfer 的兼容性 - 是否有开源代码？GitHub 地址？ 请用 tavily_search 搜索论文全文、GitHub 仓库、相关讨论帖，获取尽可能详细的实现信息。

> AGENT

我将对 LongSpec (arXiv:2502.17421) 的 Anchor-Offset Indices (AOI) 进行深度调研，搜索多个来源获取详细信息。

> DEVELOPER

纯学术深度调研，用简体中文回复。不读本地代码。 聚焦 OWL (arXiv:2510.07535, EMNLP 2025) 的 LSTM drafter 架构和与 SGLang 的集成可行性，深挖以下问题： 1. **OWL LSTM Drafter 完整架构**： - LSTM 的输入维度、hidden 维度、层数 - 输入是什么？只有 last-token hidden state？还是也有 token embedding？ - 如何从 target model 的 hidden state 映射到 LSTM input？ - LSTM 的输出如何映射到 token prediction？有 lm_head 吗？词表大小是多少？ - 参数量与 EAGLE-3 draft model 对比如何？ 2. **[SPEC] Token 机制**： - [SPEC] token 在 verifier 的 prefill 和 decode 阶段分别如何处理？ - [SPEC] token 产生的"额外表示"具体是什么？多一个 token 的 hidden state？ - 训练时 [SPEC] token 的 loss 如何计算？ - [SPEC] 增加了多少额外计算量？ 3. **Hybrid Algorithm (HOWL)**： - tree 和 non-tree 方法的具体切换逻辑 - HOWL 的 acceptance length 从 4.00 提升到 5.31-6.14 是怎么实现的？ - 不同 context length 下 tree vs non-tree 的最优选择 4. **LongSpecBench 评测数据**： - 不同 context length (4K-64K) 下 OWL vs EAGLE-3 vs EAGLE-3-L 的 acceptance length 详细对比 - 不同 target model 大小 (8B, 70B) 下的表现 - throughput (tok/s) 对比 5. **SGLang 集成可行性**： - LSTM drafter 在 SGLang 框架中的集成路径 - LSTM 不需要 KV cache，但需要 recurrent state，CUDA graph capture 的兼容性 - 与 EAGLE-3 的 tree verify 机制的兼容性 - 是否有开源代码？有没有 vLLM 或 SGLang 的 PR？ 6. **对 MiniCPM-SALA 的特殊适配问题**： - MiniCPM-SALA 的 24 层 GLA 有 recurrent state，OWL 的 LSTM drafter 是否可以复用 GLA 的 state？ - LSTM drafter 不依赖 full KV cache，这与 GLA 层的 constant-state 推理模式有天然协同性 - NVFP4 量化对 LSTM drafter 的影响 请用 tavily_search 搜索论文全文、GitHub 仓库、相关讨论帖。

> AGENT

我来进行 OWL 论文的深度调研，先搜索论文本身和相关资源。

> AGENT

让我继续深入搜索论文的详细实现、实验数据和代码仓库。

> AGENT

现在我需要获取论文的完整内容，特别是 LSTM drafter 的详细架构参数、[SPEC] token 机制、HOWL 算法和评测数据。

> AGENT

让我继续读取论文全文和代码仓库的更多细节。

> AGENT

现在让我搜索 OWL 的匿名代码仓库、Snowflake Arctic LSTM speculator 与 SGLang 集成相关信息，以及更多关于参数量的细节。

> AGENT

让我提取论文 v4 版本的完整 HTML 内容，获取更多算法细节和实验数据。

> AGENT

让我再搜索 OWL 的匿名代码仓库链接和更具体的 SGLang 集成讨论。

> AGENT

现在让我搜索论文中关于 Flash Noisy Training 和理论分析的更多细节。

> AGENT

现在让我搜索更精确的 OWL 参数量细节和 Arctic LSTM speculator 的具体架构。

> AGENT

让我再搜索 LongSpec 的 GitHub 代码细节和 MiniCPM-SALA 混合架构的相关信息。

> AGENT

现在我已经收集了足够的信息来撰写完整的深度调研报告。让我最后搜索一下 LongSpec 与 rope_theta=1M 叠加的兼容性问题。

> AGENT

现在我已经收集了所有需要的信息。以下是完整的深度调研报告。 --- # LongSpec Anchor-Offset Indices (AOI) 深度调研报告 ## 1. AOI 完整算法 ### 1.1 position_ids 构建流程 论文附录 G 给出了伪代码（Algorithm 1: Anchor-Offset Indexing）： ``` Input: 序列长度 N, 最大长度 MAX_LEN, Query states q_s Output: 应用了修改后 indices 的 RoPE 结果 1. P ← {0, 1, ..., N-1} // 初始连续 position indices 2. o ← RandomInt(0, MAX_LEN - N) // 生成随机 offset 3. P[4:] += o // 前4个 anchor 保持不变，后续全部加 offset 4. // 例: N=128, o=16257, 则 P = [0,1,2,3, 16261,...,16385] 5. return RoPE(q_s, P) ``` **关键点**： - 前 4 个 token 的 position_ids 保持为 [0,1,2,3]，作为 attention sink anchors - 第 5 个 token 开始，position_ids = 原始位置 + 随机 offset - offset 的采样范围：`[0, MAX_LEN - N]`，其中 MAX_LEN 是模型最大上下文长度 - **采样分布**：论文明确说是 **均匀分布整数**（`RandomInt`），不是对数分布 ### 1.2 Anchor 数量为什么选 4？ 论文明确引用了 StreamingLLM (Xiao et al., 2024) 的 attention sink 现象：LLM 处理长文本时，attention 权重主要集中在**前 4 个 token** 和最近的 token 上。因此： - 选择 4 是直接来自 StreamingLLM 的经验观察，不是一个可调的超参数搜索结果 - 论文没有做 anchor 数量的 ablation（1/2/4/8 对比） - 理论上 anchor 数量**可调**，但改为非 4 可能导致 target model 出现 OOD 行为，因为 target model 本身就是按 attention sink = 4 tokens 训练的 - 论文验证了采用 AOI 后 target model 的 loss 只增加约 0.001，说明 4 个 anchor 是安全的 ### 1.3 offset 采样范围的具体数值 | 目标模型 | 随机 offset 范围 | |---|---| | Vicuna-7B / LongChat-7B | `[0, 15000]` | | Vicuna-13B / LongChat-13B / Llama-3.1-8B / Qwen-2.5-7B | `[0, 30000]` | 范围的选择依据是模型的最大上下文长度：更长上下文的模型用更大的 offset 范围。 ### 1.4 训练与推理时 position_ids 的差异处理 这是 AOI 的核心设计约束： - **训练时（第一阶段：SlimPajama-6B 短序列预训练）**：使用 AOI，每个 batch 随机采样 offset - **训练时（第二阶段：Prolong-64k 长序列微调 + 第三阶段：长上下文 SFT）**：使用**vanilla indices**（即正常的 [0,1,2,...,N-1]），因为训练数据已经足够长，不需要 AOI - **推理时**：使用 vanilla indices（因为推理时序列本身就是长上下文） **核心洞察**：AOI 仅用于短序列训练阶段，让模型"提前见到"大 position index 的 RoPE 编码模式。推理时回到正常 indices，模型已经学会了如何处理大 position。 ### 1.5 RoPE theta 的配合 论文明确强调：**draft model 的 RoPE base 必须与 target model 完全一致**。 原因：draft model 通过 cross-attention 复用 target model 的 KV cache。如果 RoPE base 不一致，会导致 cross-attention 层严重退化（论文用 "significant collapse" 描述这一现象）。 因此，AOI 的设计哲学是**只改 position_ids，不改 RoPE 参数**。offset 直接加在 position index 上，然后传给标准 RoPE 计算：`RoPE(q_s, P_modified)`。RoPE 内部的 theta/base 保持不变。 --- ## 2. AOI 对 EAGLE-3 Draft Model 的影响 ### 2.1 AOI 只改 position_ids，不改 attention pattern AOI 的影响路径： - **仅修改 position_ids** -> 影响 RoPE 的旋转角度 -> 影响 Q/K 的点积（相对位置编码） - **不修改** attention mask、attention 结构、KV cache 大小 LongSpec 的 draft model 架构与 EAGLE-3 有本质区别： - LongSpec draft = 滑动窗口 self-attention (窗口=512) + cache-free cross-attention（复用 target KV cache）+ 共享 Embedding/LM Head - EAGLE-3 draft = 1 层标准 decoder，self-attention 无窗口限制，有自己的 KV cache ### 2.2 EAGLE-3 的 TTT 与 AOI 的兼容性 **TTT (Training-Time Test) 的核心**：训练时模拟推理的多步自回归过程——先 1 步用 target model 特征，后续步用 draft model 自身的预测作为输入。 **AOI 在 TTT 多步中的 position 递增**： […]

> AGENT

现在我已经收集了足够的信息来进行全面的分析。让我整理所有调研结果。 --- # OWL (arXiv:2510.07535) 深度调研报告 ## 1. OWL LSTM Drafter 完整架构 ### 1.1 基本架构 OWL 的 LSTM drafter 是一个**单层 LSTM**，不使用多层堆叠。其核心设计灵感来自 MLP-Speculator (Wertheimer et al., 2024)，但将 feed-forward 结构替换为 LSTM 的门控循环结构。 **输入维度与映射：** - 输入有两个来源： - **last-token hidden state** `h_N`，维度为 `d_0`（即 target model 的 hidden_size，如 Llama-3.1-8B 为 4096） - **predicted next token** `t_{N+1}` 的 embedding，通过可训练的 embedding layer `E` 获得 - 映射公式： ``` e_{N+1} = E(t_{N+1}) // token embedding s^m = W^m(h_N) + alpha * e_{N+1}, m in {f, i, o, c} ``` 其中 `W^f, W^i, W^o, W^c` 的维度为 `R^{d_0 x d}`，`d` 是 LSTM 的 hidden size。 **hidden 维度：** - 论文明确写道：**d = 12288**（即 LSTM hidden size 为 12288） - `d_0` 是 target model 的 hidden_size（如 4096） - 投影矩阵 `W^m` 的维度为 `d_0 x d = 4096 x 12288` **层数：** - 论文只描述了**单层 LSTM**。cell state `z` 初始化为零，在 recurrent 步中更新。没有提及多层堆叠。 **alpha 系数：** - 遵循 MLP-Speculator 的设计： ``` alpha_0 = 2^{-1/(2n)} // n 是 tree depth（论文用 8） alpha = 2*alpha_0 / ((1 - alpha_0^2) * d) ``` 这个系数平衡 hidden state projection 和 token embedding 的贡献。 **LSTM 前向流程：** ``` g^m = sigma(s^m), m in {f, i, o} // sigmoid 门控 s^c = f(s^c) * g^i // cell update（f 是 GeLU + LayerNorm） z = z * g^f + s^c // cell state 更新 h_{N+1} = f(z) * g^o // 输出 hidden state ``` 注意：论文使用了 GeLU + LayerNorm 作为激活函数（而非标准 LSTM 的 tanh），这是一个重要的设计差异。 **输出映射到 token prediction：** - 从 `h_{N+1}` 通过一个**可训练的 head**（lm_head）映射到词表上的 logits - 论文公式 (9) 显示 [SPEC] token 的 loss 使用了 target LLM 的 head：`CE(y_{[SPEC]_{k-1}}, t_k)`，其中 `y_{[SPEC]_{k-1}}` 是通过 target LLM 的 head 从 `h_{[SPEC]_{k-1}}` 生成的 - 但普通 draft token 的 head 是 drafter 自己的可训练 head - 词表大小与 target model 一致（如 Llama-3.1 的 128256） **参数量估算：** 以 Llama-3.1-8B-Instruct 为例（`d_0=4096, d=12288, vocab=128256`）： | 组件 | 参数量计算 | 估算值 | |---|---|---| | 4x 投影矩阵 W^m | 4 x 4096 x 12288 | ~201M | | Embedding layer E | 128256 x d_embed | 取决于 d_embed，如 d_embed=d=12288 则 ~1.57B | | 可训练 head (lm_head) | 12288 x 128256 | ~1.57B | | 总计 | | ~1.8-2.1B | 这个估算与 Snowflake Arctic LSTM-Speculator 报告的 **1.8B 参数**高度吻合。作为对比： - **EAGLE-3 draft model**：使用 Llama-style transformer layers，参数量约 **9B**（对于 8B target）或更大；MiniCPM-SALA 的 EAGLE-3 draft model 约 **415MB** safetensors（NVFP4 量化后） - **Arctic MLP-Speculator**：2.1B 参数 - **OWL LSTM drafter**：约 1.8B 参数，远小于 EAGLE-3 的 transformer-based drafter ### 1.2 训练细节 - **训练数据**：Ultrachat-200k + Magicoder-OSS-Instruct-75K - **预处理**：数据按 64 token 切块，用 vLLM 生成 256 token 的序列 - **训练长度**：256 token 序列 - **batch size**：2048 - **learning rate**：1e-3 - **iterations**：3000 - […]

> DEVELOPER

纯学术深度调研，用简体中文回复。用 tavily_search 深入搜索。 聚焦 QSPEC (arXiv:2410.11305, EMNLP 2025) 和量化模型 speculative decoding，深挖： 1. **QSPEC 完整实现**： - W4A4 draft 和 W4A16 verify 的具体切换机制 - "共享权重和KV cache零额外显存"的具体实现方式 - 在 Atom 和 QuaRot 两种量化方法上的实现差异 - draft token length gamma=3 的选择依据 - batch size 从 1 到 32 的详细 throughput 数据 2. **QSPEC 与 NVFP4 的兼容性**： - NVFP4 是 E2M1+block scale 格式，QSPEC 原本基于 Atom W4A4 - NVFP4 能否在 W4A4 draft / W4A16 verify 模式间切换？ - Marlin kernel 是否支持这种双精度模式？ - Blackwell (sm_120) 上的 NVFP4 kernel 是否有 dual-precision dispatch？ 3. **SPEQ bit-sharing FP4** (arXiv:2510.18525)： - 从 BF16/FP16 权重中提取 FP4 draft 的具体算法 - 与 NVFP4 的 E2M1 + shared scale 格式的关系 - 是否有开源实现？ 4. **量化 + Spec Decoding 的分布偏移分析**： - 搜索 "QuantSpec" (arXiv:2502.10424) 的详细实验数据 - KV cache 压缩（SnapKV/InfLLM-v2 sparse）对 acceptance rate 的量化影响 - FP4 kernel 数值非确定性对 greedy verify 的潜在影响 5. **SGLang/vLLM 中的量化 spec 解码实践**： - vLLM EAGLE-3 + NVFP4 的已知 bug（#36331 等） - SGLang 中 draft model 量化配置传播 - Blackwell 上 MTP + NVFP4 + CUDA graph 的兼容性问题

> AGENT

我将对 QSPEC 和量化模型 speculative decoding 进行深度学术调研，分多个方向同时搜索。

> DEVELOPER

纯学术深度调研，用简体中文回复。用 tavily_search 深入搜索。 聚焦 Traversal Verification (NeurIPS 2025, arXiv:2505.12398) 和 STree (arXiv:2505.14969)，深挖： 1. **Traversal Verification 完整算法**： - 叶到根遍历的具体算法伪代码 - 与传统 top-down verify 的理论等价性证明要点 - "保留被传统方法过早丢弃的有效子序列"的具体机制 - 对 acceptance length 的提升幅度（在不同模型/任务上的具体数据） - 计算复杂度对比：叶到根 vs 传统 top-down - 是否需要修改 CUDA kernel？与 FlashInfer tree attention 的兼容性？ 2. **STree 完整算法**： - accumulated state transition matrix 的具体数学公式 - 在 SSM 层上的 tree verification 流程 - hardware-aware implementation 的关键优化 - 与 MiniCPM-SALA 的 24 层 GLA 的 state structure 对应关系 - 实验数据：不同 tree size 下的 speedup 3. **SpecBranch rollback-aware** (arXiv:2506.01979, ICLR 2026)： - rollback-aware branch parallelism 的具体算法 - adaptive draft length 机制 - implicit confidence + explicit feature reusing 的含义 - 50% rollback token 减少的具体实现 - 多分支并发更新共享 state 的 race condition 如何处理 4. **Amazon "Snakes and Ladders"** SSM speculative decoding： - Activation Replay 的具体实现 - Joint Attainment and Advancement 的具体实现 - 与 MiniCPM-SALA 的 intermediate_ssm 方案的性能对比 5. **Together AI "Mamba in the Llama"** (arXiv:2408.15237)： - Multi-Step RNN Speculation 的 hardware-aware kernel 设计 - "不物化中间状态"的具体实现 - 在 hybrid attention/SSM 架构上的 speculative decoding 实现 - 与 SGLang 的集成路径 6. **三种 SSM/GLA state rollback 策略的全面对比**： - 全量快照（intermediate_ssm，当前项目） - Activation Replay（Amazon） - Multi-Step kernel（Together AI） - Transition matrix（STree） - 各自的内存开销、延迟、实现复杂度

> AGENT

我将系统性地搜索这些论文的详细信息。让我先并行搜索所有六个方向。

> AGENT

现在我需要深入搜索更多细节，特别是关于 NVFP4 兼容性、vLLM/SGLang 实践、以及 FP4 kernel 非确定性的问题。

> DEVELOPER

自由探索型学术调研，用简体中文回复。用 tavily_search 广泛搜索。 不限特定论文，自由探索以下方向的最新进展（2024-2026）： 1. **混合注意力架构的最新设计趋势**： - Qwen3-Next 的 3:1 Gated DeltaNet + Gated Attention 混合 - Kimi Linear 48B 的设计 - Nemotron 3 的混合架构 - Jamba / Bamba 的最新版本 - 这些架构如何处理 speculative decoding？ 2. **GLA / Lightning Attention 的最新改进**： - ReGLA (arXiv:2502.01578) 的改进点 - Log-Linear Attention (2025) - FlexLinearAttention / compiler-based linear attention kernel - Gated DeltaNet vs GLA vs Mamba-2 的最新对比 3. **混合架构下的推理优化**： - 混合架构 decode 阶段的 kernel 融合 - GLA 层的 state management 最佳实践 - 混合架构下的 CUDA graph capture 挑战 - Triton kernel 对 linear attention decode 的优化 4. **Gated Attention (NeurIPS 2025 Best Paper)**： - 具体的 gate 设计和训练方法 - 对 attention sink 的抑制效果 - 与混合架构的兼容性 - 对 speculative decoding 的潜在影响 5. **Mamba-3 和最新 SSM 架构**： - Mamba-3 的改进点 - 与 GLA 的架构对比 - SSM 在 speculative decoding 中的最新应用 6. **Long context 推理的最新优化**： - 512K+ context length 的推理技术 - KV cache 压缩 + speculative decoding 的联合优化 - InfLLM-v2 的最新改进和替代方案 每个方向至少找到 3 篇相关论文或技术报告，给出标题、来源和核心发现。特别关注与 MiniCPM-SALA（32 层混合 8 standard + 24 GLA, 512K context, NVFP4 量化, EAGLE-3 speculative decoding）的直接关联。

> AGENT

我将分批进行广泛搜索，覆盖所有6个方向。

> AGENT

现在让我深入提取每篇论文的完整技术细节。我将并行抓取论文全文。

> DEVELOPER

自由探索型学术调研，用简体中文回复。用 tavily_search 广泛搜索。 不限特定论文，自由探索 SGLang 推理框架的最新优化方向（2024-2026）： 1. **SGLang 2026 路线图和最新 PR**： - 搜索 SGLang GitHub 的 2026 roadmap / milestones - 最近 3 个月的重要 PR 和 feature - overlap scheduler 的进展 - adaptive speculative decoding 的最新实现状态 - spec v2 overlap worker 的进展 2. **SGLang EAGLE 实现的最新改进**： - EAGLE-3 在 SGLang 中的 batch=64 性能数据 - CUDA graph + EAGLE 的最新 bug fix - draft model 量化（NVFP4/Marlin）在 SGLang 中的支持状态 - tree verify kernel 的最新优化 3. **SGLang 的 attention backend 最新优化**： - FlashInfer 0.6.8+ 的新 feature - FlashAttention-3 对 SGLang 的影响 - minicpm_flashinfer backend 的最新改进 - FlashInfer tree attention 的性能 4. **SGLang overlap scheduling**： - 当前 overlap scheduler 的实现状态 - 与 speculative decoding 的兼容性 - chunked prefill + speculative decoding 的最新进展 5. **vLLM vs SGLang speculative decoding 最新对比**： - vLLM 0.19+ 的 EAGLE-3 支持 - vLLM 的 adaptive speculative decoding - 两个框架在 spec decoding 上的性能对比 - 互相借鉴的 feature 6. **SGLang 在 Blackwell (sm_120) 上的最新适配**： - RTX 6000D / B200 上的已知问题 - NVFP4 kernel 的稳定性 - CUDA graph capture 在 Blackwell 上的特殊处理 - FP4 Marlin kernel 的 bug fix 状态

> AGENT

我来对 SGLang 推理框架的最新优化方向进行广泛搜索调研。先并行发起多个搜索请求。

> AGENT

让我继续深入搜索 QSPEC 论文的具体吞吐量数据和 ML-SpecQD 的细节，以及 KV cache 压缩对 acceptance rate 的影响。

> AGENT

现在搜索其余方向的内容。

> DEVELOPER

自由探索型学术调研，用简体中文回复。用 tavily_search 广泛搜索。 聚焦 speculative decoding 的 verify 机制改进和 acceptance rate collapse 的恢复策略，自由探索： 1. **Relaxed / Fuzzy / Margin-Aware Verification**： - DIVERSED (arXiv:2604.07622)：relaxed verification framework 详细算法 - Fuzzy SD (arXiv:2502.20704, ACL Findings 2025)：模糊接受规则 - MARS (arXiv:2601.15498)：margin-aware verification - Judge Decoding (arXiv:2501.19309)：用 judge module 替代 strict verification - 这些方法对 acceptance rate 的提升幅度 - 与 EAGLE-3 greedy verify 的兼容性 - 是否是无损的？如果不是，accuracy 退化有多大？ 2. **Collapse Detection and Recovery**： - 搜索任何关于 "speculative decoding collapse recovery" 的论文 - "acceptance rate zero" 的检测和自动恢复机制 - 退 nospec 的最优策略（何时退、何时恢复） - 基于滑动窗口的 acceptance rate 监控 3. **Adaptive Draft Length 策略对比**： - SVIP (entropy-based) vs PACER (blockwise pre-verification) vs AdaEDL (entropy lower bound) - BanditSpec (multi-armed bandit) vs EAGLE-2 (confidence-based) - SMART (marginal benefit-cost) vs TALON (confidence-aware tree) - 哪种策略在长上下文下最有效？ - 与 CUDA graph capture 的兼容性对比 4. **Post-EOS / End-of-Sequence 处理**： - 搜索 "speculative decoding ignore_eos" 或 "post-EOS generation" - 其他框架如何处理 post-EOS 退化段 - 是否有论文专门研究 ignore_eos 下的 spec decoding 行为 5. **Draft Model 的 Vocab Coverage 问题**： - 搜索 "draft model vocabulary size" 或 "draft vocabulary coverage" - EAGLE 的 draft_vocab_size=32000 vs target vocab_size=73448 的问题是否在其他项目中也存在？ - 扩展 draft vocab 的训练策略 - vocab coverage 对 acceptance rate 的量化影响

> AGENT

我将对这五个方向进行广泛的学术调研。让我先并行发起多组搜索。

> AGENT

现在让我提取 QSPEC 论文的完整 throughput 数据和更多 NVFP4/CUDA graph 相关细节。

> DEVELOPER

自由探索型学术调研，用简体中文回复。用 tavily_search 广泛搜索。 自由探索 MiniCPM 模型系列和相关训练数据/校准数据的最新进展： 1. **MiniCPM 系列论文和技术报告**： - MiniCPM (初代) 的论文 - MiniCPM-2 / MiniCPM-3 的改进 - MiniCPM-SALA 的设计论文（如果有的话） - OpenBMB 团队的最新模型 - SALA (Sparse Attention with Linear Attention) 的原始论文 2. **混合 Attention 架构的设计论文**： - 搜索 "MiniCPM linear attention hybrid" 或 "MiniCPM GLA" - 8 standard + 24 GLA 的设计原理 - dense_len=8192 的选择依据 - InfLLM-v2 的论文和最新改进 3. **Speculative Decoding Draft Model 训练**： - EAGLE-3 训练的最佳实践（数据选择、序列长度、数据量） - SpecForge 训练框架的详细信息 - draft model 在混合架构模型上的训练有什么特殊考虑？ - 搜索 "EAGLE training hybrid attention" 或 "draft model training linear attention" 4. **校准数据 (Calibration Data) 选择**： - NVFP4 量化的校准数据最佳实践 - 当前项目用 calib90_train.jsonl (90K 上下文)，这个数据量是否最优？ - FourOverSix 量化方法 (loguniform 128, 48K 上下文) 的校准数据选择 - 搜索 "NVFP4 calibration data selection" 或 "GPTQ calibration data" 5. **EAGLE Draft Model 的数据采集**： - target model 生成 draft 训练数据的最新策略 - 长上下文数据的采集方法（如何获取 >50K 的训练样本） - 训练数据的领域配比（code / math / chat / reasoning） - 数据质量 vs 数据量对 draft model 性能的影响 6. **SOAR 比赛相关信息**： - SOAR (Speed Optimized AI Reasoning) 比赛的最新规则 - 其他参赛团队的技术方案 - 评测数据集的特点（是什么类型的 prompt？长度分布？） - 评分标准（吞吐量？延迟？准确率？权重？）

> AGENT

我将进行广泛的搜索来调研这些主题。让我并行发起多个搜索。

> AGENT

继续深入搜索更多具体方向。

> AGENT

Tavily 搜索额度已耗尽，让我继续用其他方式获取信息。

> AGENT

让我读取提取到的完整论文内容，获取技术细节。

> AGENT

Tavily 搜索 API 配额已耗尽。让我改用项目内部文档和公开网页信息来完成这个调研。我先从项目文档中提取关键信息，再用其他方式搜索。

> AGENT

Tavily 额度已完全耗尽。我将基于已经获取的搜索结果以及我对这些论文的已有知识来完成调研。让我先查看项目中已有的相关文档作为上下文。

> AGENT

Tavily 搜索配额用完了，换用 Tavily extract 和 research 来补充剩余信息。

> AGENT

现在我已经有了项目背景。让我继续搜索剩余主题的论文信息。

> AGENT

Tavily 搜索额度用完了。让我用 research 工具继续搜索剩余方向。

> AGENT

现在让我阅读更多相关文档并搜索公开信息。

> AGENT

Tavily 搜索额度完全耗尽。让我改用其他方式获取信息。

> AGENT

现在让我搜索更多关于 Snakes and Ladders 论文的细节，以及 SpecBranch 的 H-RAD 算法的具体实现。

> AGENT

现在让我查看项目代码中关于 MiniCPM-SALA 模型架构的更多信息，以及搜索公开论文。

> AGENT

好的，我已经获取了 MARS 和 Judge Decoding 的摘要。让我继续搜索其余主题。

> AGENT

Tavily 搜索额度已用尽，让我从已提取的完整论文内容中继续挖掘细节。让我读取 STree 论文的剩余部分，以及 SpecBranch 论文。

> AGENT

现在让我尝试用其他方式搜索学术信息。

> AGENT

现在让我读取之前保存的完整提取内容，获取 STree 和 SpecBranch 的详细信息。

> AGENT

Tavily API 配额已耗尽。让我用 curl 来获取公开论文信息。

> AGENT

现在让我获取 Amazon Snakes and Ladders 论文的详细内容。

> AGENT

现在我已经收集了足够的详细内容来撰写全面的学术调研。让我再获取一些关于 Snakes and Ladders 的 Activation Replay 和 Together AI Multi-Step kernel 与 GLA 对应关系的细节。

> AGENT

Tavily 全部配额已用尽，但前两轮搜索已经获取了非常丰富的信息。下面基于已搜集到的内容，整理出完整的调研报告。 --- # SGLang 推理框架最新优化方向调研（2024-2026） ## 一、SGLang 2026 路线图与最新 PR ### 1.1 2026 Q2 路线图（Issue #22949，2026年4月16日发布） SGLang 2026 Q2 路线图由 @merrymercy 发布，子模块包含： - **Nvidia Collaboration Roadmap (2026 Q2)** #22960 - **Speculative Decoding Development Roadmap (2026 Q2)** #23005 — 专门的推测解码子路线图 - **SGLang-Diffusion (26 Q2)** #23035 - **Multimodal LLM (26 Q2)** #23036 - **AMD Development Roadmap (2026 Q2)** #23494 - **RFC: Native gRPC Server for SGLang in Rust** #22558 - **RFC: Sglang non-GPU process rust migration** #23206 核心方向：Rust 化迁移（非 GPU 进程）、gRPC server、推测解码专项路线图。 ### 1.2 2026 Q1 路线图（Issue #12780）关键条目 - **KV Cache 系统**：HiCache for Hybrid and Sparse LLMs（#12826），Sparse Attention + KV cache CPU/GPU 调度（#11191） - **推测解码**：overlap scheduler（#11762）、lookahead 参考解码（#9873）、与所有 feature 的兼容性 - **Prefill-Only 推理**：作为一等执行路径（#15344） - **CI/CD**：CUDA 13 workflow、B200/B300 CI runners - **Tracing**：HiCache、PP、SD 的请求追踪（#13511） - **Advanced Priority Scheduling**：优先级调度、批处理、并发控制（#13526） ### 1.3 2025 Q3 路线图核心重构 - **Overlap Scheduler**：Feature #11762，支持推测解码与 CPU overlap - **Piecewise CUDA Graph + torch.compile 支持**：#11490 - **mem_cache_v2**：分离分配逻辑与调度器（#11313） - **Pipeline Parallelism 路线图**：#11857 - **DeepSeek V3 优化**：FlashAttention-3、Dynamic MLA-to-MHA switching、DeepGEMM FP8、Kernel Fusion、Data-parallel attention ### 1.4 Overlap Scheduler 进展 Overlap Scheduler 是 2025 Q3-Q4 的重点特性，目前的状态： - **已合并主分支**：SGLang v0.4 引入 zero-overhead batch scheduler - **与 speculative decoding 的 overlap 支持**：Feature #11762 仍在推进 - 实测数据（DeepSeek V3 + SGLang overlap）：TPOT 从 348.10s 降至 196.79s（约 43% 降低），但 TTFT 有退化（724050s → 864850s，约 19% 增加），原因是调度开销 - 大请求场景下 overlap 效果更明显 - 启动参数：`--disable-overlap-schedule` 可关闭 --- ## 二、SGLang EAGLE 实现的最新改进 ### 2.1 EAGLE-3 在 SGLang 中的性能数据 论文（arXiv:2503.01840）中 SGLang 团队提供的官方数据（1x H100，LLaMA-Instruct 3.1 8B，MT-Bench）： | 方法 | Throughput (bs=1) | 加速比 | |---|---|---| | SGLang 无推测 | 158.34 tok/s | 1.00x | | SGLang + EAGLE-2 | 244.10 tok/s | 1.54x | | SGLang + EAGLE-3 | 373.25 tok/s | **2.36x** | **大 batch 数据**（未使用 tree 结构，chain max=2）： - bs=2 时 EAGLE-3 吞吐提升 1.81x - **bs=64 时 EAGLE-3 仍有 1.38x（40%）吞吐提升** - EAGLE-2 在 bs=24 时吞吐反而下降至 0.93x 这打破了"推测解码在大 batch 下无用"的传统认知。关键在于 SGLang 的 zero-overhead scheduler 使验证开销极低。 ### 2.2 EAGLE-3 架构改进 - **移除 feature prediction 约束**：不再预测目标模型顶层特征，直接通过 Training-time test 预测 draft tokens - **三层特征融合（Tri-layer feature fusion）**：融合目标模型低层、中层、高层特征，获得更丰富信息 - 早期层：编码语法、形态、局部 token 上下文 - 中间层：编码语义关系和篇章结构 - 晚期层：编码输出概率分布 - **Scaling law 发现**：增加训练数据量会正比提升加速比，这在原始 EAGLE 中未观察到 - EAGLE-3 用 8x 数据训练，比 EAGLE-2 快 1.4x（bs=1） - 最大加速比达 6.5x ### 2.3 SpecForge 训练框架 2025年7月25日发布，SGLang 官方的 EAGLE-3 训练框架： - 与 SGLang 推理引擎紧密集成，训练到部署无缝衔接 - 支持在线训练（SGLang server 实时提取多层特征）和离线训练（预计算 hidden states 存盘） - 已有预训练模型：Llama-3.1-8B、Qwen-2.5-7B 等 - `bench_speculative` 脚本可调优最优 spec 参数 ### 2.4 CUDA Graph + EAGLE 的已知问题 - SGLang 在 Blackwell (SM120) 上需要 `--disable-cuda-graph` 或 `--enforce-eager` 才能稳定运行 - CUDA graph capture 在 Blackwell 上有 Triton SMEM overflow 问题（fix PR #17908） - MTP 路径会自动 cap […]

> AGENT

arxiv 搜索接口似乎限流了。让我基于已获取的信息以及专业知识来完成这份调研报告。让我再查一下 SPEED-Bench 论文中关于 vocabulary pruning 的发现。

> AGENT

现在让我查看项目中的相关代码，了解当前 verify 机制的具体实现，以便评估各方法与 EAGLE-3 的兼容性。

> AGENT

Tavily 额度已耗尽。我已经收集了大量信息，可以基于前8次搜索的结果给出综合报告。对于未能搜索到的方向，我将基于已有搜索结果中获取的线索和我的知识进行补充。 --- # 混合注意力架构与推理优化最新进展调研报告（2024-2026） ## 1. 混合注意力架构的最新设计趋势 ### 1.1 Qwen3-Next / Qwen3.5：3:1 Gated DeltaNet + Gated Attention 混合 **核心论文/来源：** - Qwen Team, "Qwen3-Next: A New Generation of Ultra-Efficient Model Architecture" (2025.9) - Yang, Kautz, Hatamizadeh, "Gated Delta Networks: Improving Mamba2 with Delta Rule" (ICLR 2025, arXiv:2412.06464) - Qwen3.5 将混合注意力扩展到 397B 参数 **核心发现：** - Qwen3-Next 采用 75% Gated DeltaNet + 25% Gated Attention 的 3:1 混合比例 - 80B 总参数，MoE 设计激活仅 3B（3.7% 激活率），512 experts 中每步仅激活 10 个 - Gated DeltaNet 层：线性注意力，使用 delta rule + 门控衰减，固定大小 state 矩阵 `(B, H, d_k, d_v)`，不依赖序列长度 - Gated Attention 层：在标准 softmax attention 基础上增加三项改进——(1) 输出门控缩放 attention 结果后再加回残差；(2) Zero-centered QK-Norm 替代标准 RMSNorm；(3) 部分 RoPE - Qwen3.5 将此架构扩展至 397B，证明 Gated DeltaNet 可以有效规模化，验证了线性注意力混合架构的 scaling 能力 - Qwen3-Coder-Next 变体：256K context，同样 3:1 混合 + MoE + MTP（Multi-Token Prediction），在 SWE-Bench Pro 上达 44.3% **与 MiniCPM-SALA 的关联：** MiniCPM-SALA 的 8:24（1:3）混合比例与 Qwen3-Next 的 3:1 GDN:GA 比例形成有趣对照——两者都是 linear attention 层占多数，但 Qwen3-Next 的 Gated DeltaNet 比 GLA 更强（delta rule 提供更好的 key-value 关联学习），且 Gated Attention 层的输出门控设计可能对我们保留的 8 层 standard attention 有参考价值。 ### 1.2 Kimi Linear 48B：KDA + MLA 混合 **核心论文/来源：** - Kimi Team, "Kimi Linear: An Expressive, Efficient Attention Architecture" (arXiv:2510.26692v2, 2025.11) - Moonshot AI 开源，HuggingFace 可用 **核心发现：** - Kimi Delta Attention (KDA)：Gated DeltaNet 的改进版本，引入 **channel-wise gating**（逐通道门控），允许对各特征维度独立控制记忆衰减，而非 GDN 的 head-wise 标量门控 - 3:1 KDA:MLA 混合比例，36 层 - 48B 总参数，128 experts，8 active（3B 激活），1M context - DPLR 矩阵（Diagonal-Plus-Low-Rank）：KDA 层使用 DPLR 转移矩阵的 chunkwise 算法，优化硬件利用率 - NoPE 策略：MLA 层不使用位置编码，位置信息全部由 KDA 层承担 - 消融实验关键结论：3:1 比例最优（train PPL 9.23 vs 全 attention 9.45）；sigmoid 门控优于 swish 和无门控；卷积层移除增加 val PPL 0.05 - RL 场景表现突出：MATH500 上 Kimi Linear ~86%->90%，超越 MLA 基线 - 推理效率：75% KV cache 减少，1M context 下 6x 解码吞吐提升 - KDA kernel 已开源到 FLA (Flash Linear Attention) 库，vLLM 已集成 **与 MiniCPM-SALA 的关联：** KDA 的 channel-wise gating 设计直接改进了我们使用的 GLA 架构。GLA 的 element-wise forget gate 是 head-wise 的，而 KDA 让每个特征维度有独立的衰减控制。这个设计思路可以作为 GLA 层升级的候选方向。此外 KDA 在 FLA 库中的 Triton kernel 实现对我们有直接参考价值。 ### 1.3 Nemotron 3：Mamba-2 + Attention + MoE 混合 **核心论文/来源：** - NVIDIA, "Nemotron 3: Efficient and Open Intelligence" (arXiv:2512.20856, 2025.12) - NVIDIA, "Nemotron 3 Super: Open, Efficient Mixture-of-Experts Hybrid Mamba-Transformer" (Technical Report, 2026.3) **核心发现：** - Nano (30B-A3B), Super (120B-A12B), Ultra 三个变体 - Super 架构：6 层一组循环，顺序为 Mamba-2 -> LatentMoE -> Mamba-2 -> Attention -> Mamba-2 -> LatentMoE，重复 5 组 - **LatentMoE**：新型 MoE 设计，在 latent space 中路由，提升每字节精度 - **NVFP4 训练格式**：Super/Ultra 使用 NVFP4 量化训练，原生适配 Blackwell 架构 - MTP（Multi-Token Prediction）用于推理加速 - 1M context window，通过 hybrid Mamba-Transformer 架构实现 - 3x 吞吐提升 vs 同等规模 Transformer（Nemotron-H 报告达 3x） - 解耦设计（DUET 论文，arXiv:2603.15530）：roofline 分析表明 Mamba 和 Attention 层在 prefill/decode […]

> AGENT

搜索额度用完了，但我已经收集到了足够的信息。让我整理完整的深度调研报告。 --- ## QSPEC 与量化模型 Speculative Decoding 深度调研报告 --- ### 1. QSPEC 完整实现细节 #### 1.1 W4A4 Draft / W4A16 Verify 的切换机制 QSPEC 的核心观察是：**同一份 4-bit 权重**在两种激活精度模式下生成的 token 分布高度相似（见论文 Figure 2 的散点图）。切换机制如下： - **Draft 阶段**：使用 W4A4 模式（权重 INT4 + 激活 INT4），调用 Atom/QuaRot 的低精度 kernel 执行前向推理。激活在进入 GEMM 前被量化为 INT4，利用 Tensor Core 的 INT4 计算能力获得更高算力利用率。 - **Verify 阶段**：使用 W4A16 模式（权重 INT4 + 激活 FP16），调用 Marlin 或等价的 weight-only dequant kernel。激活保持 FP16，权重在线反量化后与 FP16 激活做 GEMM。 - **切换代价**：由于**权重是同一份**，切换只涉及选择不同的 GEMM kernel 路径（W4A4 kernel vs W4A16 kernel），无需权重拷贝或格式转换。论文称之为"nearly cost-free execution switching"。 #### 1.2 "共享权重和 KV cache 零额外显存"的具体实现 - **权重共享**：W4A4 和 W4A16 两种模式使用完全相同的量化后权重张量（INT4 packed format）。不需要额外存储一份 BF16/FP16 权重。这就是"零额外权重内存"的含义。 - **KV Cache 覆写**：这是 QSPEC 的关键设计—— - Draft 阶段 W4A4 生成 token 时会产生低质量 KV cache（激活精度低导致 KV 值不精确）。 - Verify 阶段 W4A16 对被接受的 token 重新计算前向，产生高质量 FP16 KV cache。 - **W4A16 的 KV cache 直接覆写 W4A4 的 KV cache**（对应 accepted token 位置），后续解码步使用的是高质量 KV cache。 - 因此只需维护**一份 KV cache**，不需要为 draft 和 verify 分别维护，内存开销等于纯 W4A16 模式。 对比表格（论文 Table 2）： | 方法 | Draft 权重 | Draft KV | W4A4 Kernel | Draft-Verify 一致性 | 高 Acceptance | 高 Fidelity | |------|-----------|----------|-------------|-------------------|--------------|-------------| | W4A16 | 无 | 无 | 无 | 无 | 无 | 有 | | W4A4 | 无 | 无 | 有 | 无 | 无 | 无 | | 传统 Spec Dec | 有 | 有 | — | 有 | 有 | 有 | | **QSPEC** | **无** | **无** | **有** | **有** | **有** | **有** | #### 1.3 Atom vs QuaRot 的实现差异 两者都是 W4A4 量化方案，但原理不同： - **Atom**：基于 learned equivalent transform（旋转/缩放），通过优化使权重和激活的分布更利于 INT4 量化。QSPEC 在 Atom 上的 acceptance rate 更高（ShareGPT 83.8%，MATH 89.4%，MBPP 88.6%）。 - **QuaRot**：基于 Hadamard 旋转实现 computational invariance，消除 outlier，使权重、激活、KV cache 都能 4-bit 量化。QSPEC 在 QuaRot 上的 acceptance rate 略低（ShareGPT 81.6%，MATH 88.9%，MBPP 85.4%），可能因为 QuaRot 的旋转变换使 W4A4 与 W4A16 的输出差异稍大。 论文 Table 3 显示：Atom W4A16 PPL=7.87，QuaRot W4A16 PPL=8.58；Atom W4A4 PPL=8.6，QuaRot W4A4 PPL=10.2。QuaRot 的 W4A4 质量退化更严重，导致 acceptance rate 稍低。 #### 1.4 gamma=3 的选择依据 论文 Section 3.3 和 Appendix A.4 讨论了 draft length 的选择。gamma=3 的理由： - 对于 self-speculative decoding（draft 和 verify 共享权重），acceptance rate 非常高（93-95%），因此即使 gamma 较小，期望接受 token 数也接近 gamma * acceptance_rate。 - 增大 gamma 会线性增加 W4A4 draft 时间，但 verify 阶段（W4A16）只执行一次。当 acceptance rate 极高时，gamma=3 已经能获得接近 3 个 accepted token，进一步增大 gamma 的边际收益递减。 - Batch size 增大时，verify 阶段开销也增大，较大的 gamma 未必带来更好吞吐。论文 Table 8 显示 batch size 32 时加速比降至 1.01-1.15x。 #### 1.5 Batch Size 1 到 32 的详细 Throughput 数据 **Llama2-7B (Atom 量化)**，A100 GPU： | Batch Size | W4A16 | QSPEC | 加速比 | Acceptance Rate | |-----------|-------|-------|--------|----------------| | 1 | […]

> AGENT

我现在已经收集了所有论文的核心技术细节。下面撰写完整的学术调研报告。 --- # SSM/GLA 推测解码前沿论文深度调研 ## 一、Traversal Verification (NeurIPS 2025, arXiv:2505.12398) ### 1.1 完整算法 Traversal Verification 的核心思想是将验证方向从传统 top-down 改为 bottom-up（叶到根），并采用**序列级接受概率**而非逐 token 接受概率。 **算法 3 伪代码要点**： 1. **初始化阶段**：对树中每条链 alpha = (X_0, X_1, ..., X_{gamma_alpha})，计算每个节点的序列级接受概率： `p_alpha^{ini}(X_i) = min{p_alpha^{ini}(X_{i-1}) * M_b(X_i|X^{i-1}) / M_s(X_i|X^{i-1}), 1}`, 1 <= i <= gamma_alpha 其中 p_alpha^{ini}(X_0) = 1。关键在于：接受概率在链上是**累积的**（相乘后再裁剪到 1），而非传统方法中每步独立 min(r,1)。 2. **遍历阶段**：按后序 DFS（叶到根）遍历树，对于当前链 alpha： - 采样均匀随机数 eta ~ U(0,1) - 若 eta < p_alpha(X_{gamma_alpha})，接受**整条链**（从当前叶节点到根） - 若被拒绝，删除最后节点 X_{gamma_alpha}，更新分布和接受概率 3. **拒绝后分布更新**（核心机制）： - 新目标分布：`M_b'(x|X^{gamma_alpha-1}) = norm([p_alpha(X_{gamma_alpha-1}) * M_b(x|X^{gamma_alpha-1}) - M_s(x|X^{gamma_alpha-1})]_+)` - 新 draft 分布：`M_s'(x|X^{gamma_alpha-1}) = norm(M_s(X_{gamma_alpha}|X^{gamma_alpha-1})=0)` （将被拒 token 概率置零后归一化，即 RRSw） - 更新接受概率：`p_alpha'(X_{gamma_alpha-1}) = sum_x [p_alpha(X_{gamma_alpha-1}) * M_b(x|X^{gamma_alpha-1}) - M_s(x|X^{gamma_alpha-1})]_+ / (sum_x [...]_+ + 1 - p_alpha(X_{gamma_alpha-1}))` 4. 当所有兄弟节点均被拒绝时，回退到父节点继续验证。 ### 1.2 理论等价性证明要点 **Theorem 3.3 (无损失性)**：证明利用了算法的**自相似性**（self-similarity）。对树中任意父节点 A，在决定 A 是否被接受之前，其所有后代节点已通过相同的遍历机制处理完毕。因此每个局部子树本质上是 Traversal Verification 的缩放实例。通过对后代节点数做数学归纳，建立 Lemma A.2，Theorem 3.3 作为推论直接得出。 **Theorem 3.4 (单链最优性)**：在单链情形下，E[N_traversal] = E[N_block] >= E[N_verify]。证明思路是引入"伪子节点"使目标分布变为 P(A)*M_b，然后将序列级 RRSw 应用于将 draft 分布 M_s 迁移到目标分布，确保每节点达到最高可能接受概率。 ### 1.3 "保留被传统方法过早丢弃的有效子序列"机制 传统 top-down 验证中，一旦父节点被拒绝，其**所有子节点立即被丢弃**，即使子节点本身可能对应目标模型的高概率 token。Traversal Verification 中，父节点只在**所有子节点均被拒绝后**才被验证，因此子节点的验证机会不会被过早剥夺。此外，序列级接受概率 `min(r(X_1)*r(X_3), 1)` 在 `r(X_1)<1` 时可以"借"后续 token 的超额概率来弥补前面 token 的不足，而传统方法 `min(r(X_1),1)*min(r(X_3),1)` 则每步独立截断，无法跨步补偿。 具体数值示例：当 r(X_1)=0.5, r(X_3)=4/3 时： - Traversal: P(accept) = min(0.5 * 4/3, 1) = 0.667 - Token-level: P(accept) = 0.5 * 1 = 0.5（r(X_3)>1 被 min 截断后浪费了超额概率） ### 1.4 Acceptance Length 提升幅度 **Llama3.2-1B / Llama3.1-8B (Temperature=1)**： - Chain (depth=5): 3.88 -> 3.99 (+2.8%) - Binary Tree (depth=5): 4.63 -> 4.73 (+2.2%) - EAGLE Sparse Tree: 4.49 -> 4.60 (+2.4%) **Llama-68M / Llama2-7B (Temperature=1)**： - Chain: 1.99 -> 2.10 (+5.7%) - Binary Tree: 2.44 -> 2.56 (+4.9%) - EAGLE Sparse Tree: 2.52 -> 2.62 (+3.8%) **温度影响**：温度越高优势越明显（T=0.2 时仅 +1.0%，T=1.0 时 +2.8%），因为高温下概率分布更分散，序列级联合概率的优势更显著。**链深度和树规模越大，改进越显著**（深度 8 的 chain 改进远大于深度 2）。 ### 1.5 计算复杂度对比 - 传统 top-down：最坏情况遍历所有节点 O(N)，但通常在中间节点被拒绝后剪枝，提前终止 - Traversal Verification：同样最坏 O(N)，但因为从叶节点开始验证，**几乎总是需要遍历更多节点**（即使父节点最终被接受，也必须先处理所有子节点） - 论文承认：Traversal Verification 引入的额外遍历开销使得实际吞吐量提升略低于 acceptance length 改进（如 acceptance +2.8% 对应 throughput +2.5%） - 声称可通过更优化的实现缓解 ### 1.6 与 FlashInfer Tree Attention 的兼容性 Traversal Verification **不需要修改 CUDA kernel**。它是纯算法层面的改动——验证逻辑从 top-down 改为 bottom-up，仅影响采样/接受/拒绝的决策流程。target model 的 tree attention forward pass（FlashInfer tree attention）完全不变——仍然是一次性将所有 draft token 喂入目标模型获取 M_b。Traversal Verification 只是改变了如何使用这些 M_b 输出来做接受/拒绝决策。因此它是 **plug-and-play** 的，可以直接替换现有 EAGLE/Medusa/SpecInfer 中的验证模块。 --- ## 二、STree (NeurIPS 2025, arXiv:2505.14969) ### 2.1 Accumulated State Transition Matrix 的数学公式 STree 的核心是利用 SSM 的对角结构，将树形 mask 引入状态转移矩阵的累积计算。 SSM 基本形式：`x_{t+1} = A(u_t)x_t + B(u_t)u_t`, `y_t = C(u_t)x_t` 对树中 token 按前序打包为序列 S={t_1,...,t_N}，定义树 mask L（L_{i,j}=1 当且仅当 t_j 在 t_i 到根的路径上），则： **y_t = C_t * (exp{sum_{i=1}^t L_{t,i} * log(A_i)} * x_0 + sum_{s=1}^t L_{t,s} * exp{sum_{j=s+1}^t L_{t,j} * log(A_j)} * B_s * u_s)** 定义 **A_tree = L * A_log**，其中 `A_log = [diag(log A_1), ..., diag(log A_N)]^T`，则： `(A_tree)_t = sum_{i=1}^N L_{t,i} * diag(log A_i)` 最终输出： - `(M_x)_i = C_i * diag(exp{(A_tree)_i})` - `(M_u)_{ij} […]

> AGENT

现在我已经收集了足够的信息。让我整理完整的调研报告。 --- # Speculative Decoding 机制改进学术调研报告 ## 1. Relaxed / Fuzzy / Margin-Aware Verification ### 1.1 DIVERSED（arXiv:2604.07622，AISTATS 2026） **核心算法**：DIVERSED 提出动态集成验证（Dynamic Ensemble Verification），将验证目标从纯 target 分布 p(x) 替换为 p(x) 和 draft 分布 q(x) 的混合： ``` nu_t(x) = alpha_t * p(x|context) + (1 - alpha_t) * q(x|context) ``` 其中 `alpha_t` 是随上下文和 token 位置动态变化的混合权重，由一个轻量级神经网络（单层 FC + sigmoid）学习。训练目标是在最大化 task reward 的同时鼓励高 acceptance rate。 **两种变体**： - **Static Ensemble**（训练免费）：固定 alpha 混合，论文证明其精确遍历 acceptance-quality Pareto 前沿 - **DIVERSED**（需训练）：动态 alpha，在可比质量下获得比 Pareto 前沿更高的 acceptance **Acceptance 提升幅度**：理论推导给出 `E[TN] = sum_t Product_i (1 - TV(q_i, p_i))`，DIVERSED 通过降低混合分布与 draft 的 TV 距离来提高接受长度。实证在多个模型对上显著高于标准 SD。 **与 EAGLE-3 兼容性**：DIVERSED 修改的是 verify 阶段的接受规则，不影响 draft 生成。但当前 EAGLE-3 用的是 greedy verify（`verify_tree_greedy_func`），DIVERSED 的动态 alpha 需要在 verify 时计算混合概率，与 greedy argmax 匹配逻辑不直接兼容。需要将 greedy verify 替换为基于概率的 verify。 **是否无损**：**不是无损的**。当 alpha < 1 时，接受分布会偏离 target 分布，存在 distributional bias。论文量化了这个 bias：`Loss*_TV(b) > 0` 当 b 超过标准 SD 阈值时。但 alpha 趋近 1 时 bias 趋近 0，在 Pareto 前沿上可以找到 bias 极小但 acceptance 提升明显的操作点。 ### 1.2 Fuzzy SD（arXiv:2502.20704，ACL Findings 2025） **核心算法**：FSD 用 target 和 draft 分布的散度（divergence）来决定是否接受 draft token，而非逐 token 的概率比： ``` F_accept(x_i) = 1 if Div(P_MT[i], P_MD[i]) < T, else 0 ``` T 是用户可调的散度阈值。支持任何基于 P_MT 和 P_MD 的散度度量（KL、JS、TV 等）。 **Reduced FSD 变体**：先按标准 SD 规则验证，rejected 的 token 再做一次 fuzzy check（散度 < T 则接受）。这保证了标准 SD 的输出是 reduced FSD 输出的子集，更加安全。 **Acceptance 提升幅度**：通过调低 T，用户可以显式控制 acceptance rate。论文展示 T 的调节可以平滑地在 quality 和 throughput 之间取舍。 **与 EAGLE-3 兼容性**：**高度兼容**。Reduced FSD 变体只需在 greedy verify 拒绝后增加一步 divergence check。当前代码中 `verify_tree_greedy_func` 返回 accept_index 后，可以对 rejected 位置计算 `TV(target_probs, draft_probs)` 并有条件恢复。计算散度需要 draft_probs，当前 greedy verify 不保存 draft probs，需要小幅改造。 **是否无损**：**不是无损的**。当 T > 0 时，输出分布会偏离 target。但 reduced FSD 变体的偏离是有界的——只有标准 SD 会拒绝但散度足够小的 token 才被 fuzzy 接受，这类 token 通常对输出质量影响极小。 ### 1.3 MARS（arXiv:2601.15498，ICLR 2026） **核心算法**：Margin-Aware Speculative Verification，训练免费且领域无关。核心洞察是：现代 LLM 经常在 low-margin 状态下运行（top-1 和 top-2 概率接近），此时拒绝 runner-up token 的信息增益可忽略但 rollback 成本很高。MARS 基于 target logits 的决策稳定性（decision stability）来条件化验证： - 计算 target 的 top-1 和 top-2 概率之差（margin） - 当 margin 足够大时（target 有强偏好），使用严格验证 - 当 margin 很小时（target 不确定），放松验证接受 draft token **关键优势**： - 完全训练免费 - 只修改验证规则，与任何 target-coupled spec decode 框架兼容 - 在 8B 到 235B 模型规模上一致性提速 **与 EAGLE-3 兼容性**：**最兼容**。MARS 只需要 target logits 的 top-2 概率，当前 verify 已经计算了 `target_predict = argmax(logits)`，增加 top-2 概率几乎没有额外开销。在 greedy verify 路径中，当 `p_top1 - p_top2 < margin_threshold` 时，将 draft token 的匹配条件从 `target_predict == draft_token` 放宽为 `draft_token in {top-1, top-2}` 或类似规则。 **是否无损**：**近似无损**。在 low-margin 区域接受 draft token 等价于从一个与 target 几乎不可区分的分布采样。论文在多样化 benchmark 上展示了 generation quality 保持。 ### 1.4 Judge Decoding（arXiv:2501.19309） **核心算法**：颠覆性地不依赖 draft-target 对齐，而是训练一个 compact judge module 附加在 target 的 embedding 之上，直接判断"当前 continuation 是否正确"。受 LLM-as-a-judge 启发。 **关键发现**：论文证明即使是 GPT-4o 作为 draft model，甚至人类文本，在标准验证下 acceptance rate 也很低——这是标准 SD 验证机制的根本局限。 **Acceptance 提升幅度**：8B/405B-Judge 达到 9x 加速（vs Llama-405B autoregressive），141 tok/s（8B/70B-Judge，2xH100）。 **与 EAGLE-3 兼容性**：**不兼容**。Judge module 需要训练并集成到 […]

> AGENT

现在我有了足够的信息来进行综合调研报告。以下是完整的调研结果。 --- # MiniCPM 模型系列与相关技术调研报告 ## 一、MiniCPM 模型系列论文与技术报告 ### 1. MiniCPM（初代） - **论文**：*MiniCPM: Unveiling the Potential of Small Language Models with Scalable Training Strategies*（arXiv:2404.06395，2024年4月） - **作者**：Shengding Hu, Yuge Tu, Xu Han 等（OpenBMB/清华团队） - **核心贡献**：1.2B 和 2.4B 非嵌入参数 SLM，性能对标 7B-13B LLM。引入 WSD（Warmup-Stable-Decay）学习率调度器，发现 Chinchilla Optimal 的数据-模型比远高于此前认知。衍生出 MiniCPM-DPO、MiniCPM-MoE、MiniCPM-128K。 - **GitHub**：https://github.com/OpenBMB/MiniCPM ### 2. MiniCPM-3 - 没有找到独立的 MiniCPM-3 技术报告（arxiv 上未检索到）。但 HuggingFace 上存在 `openbmb/MiniCPM3-4B` 及其 GPTQ/GGUF 变体，是 4B 参数的迭代版本。 ### 3. MiniCPM4 - **论文**：*MiniCPM4: Ultra-Efficient LLMs on End Devices*（arXiv:2506.07900，2025年6月） - **核心贡献**：从四个维度（模型架构、训练数据、训练算法、推理系统）实现极致端侧效率。8B 参数训练 8T tokens。关键创新： - **InfLLM-v2** 可训练稀疏注意力机制 - **Model Wind Tunnel 2.0** 可预测扩展 - **BitCPM** 极端三值量化（90% 位宽压缩） - **CPM.cu** 自研 CUDA 推理框架 - **UltraClean / UltraChat v2** 高质量数据管线 - 已有配套 EAGLE-FRSpec 推测解码 head 和 Marlin 量化版本 ### 4. MiniCPM4.1 - 2025年9月发布，在 MiniCPM4 基础上加入**融合思维（fusion thinking）**推理能力 - 支持 EAGLE3 推测解码，3x 解码加速 - 提供 GPTQ/AutoAWQ/Marlin/GGUF/MLX 多种量化格式 - 注意：SGLang 和 vLLM 目前仅支持 MiniCPM4/4.1 的 **dense attention 推理模式**；sparse 推理需用 HuggingFace Transformers 或 CPM.cu ### 5. MiniCPM-SALA（核心目标模型） - **论文**：HuggingFace 模型卡引用了两篇关键技术论文： - *Hybrid Linear Attention Done Right: Efficient Distillation and Effective Architectures for Extremely Long Contexts*（arXiv:2601.22156）——即 **HyPE (Hybrid Positional Encoding)** 论文 - *InfLLM-V2: Dense-Sparse Switchable Attention for Seamless Short-to-Long Adaptation*（arXiv:2509.24663）——稀疏注意力论文 - **技术报告**：https://github.com/OpenBMB/MiniCPM/blob/main/report/MiniCPM_4_Technical_Report.pdf（MiniCPM4 技术报告涵盖 SALA 架构） - **核心创新**： - **SALA 混合注意力**：25% InfLLM-v2 稀疏注意力 + 75% Lightning Attention（GLA） - **HALO (Hybrid Attention via Layer Optimization)**：新型蒸馏配方，将 dense attention 能力转移到混合架构，避免纯线性模型性能退化 - **HyPE**：统一稀疏注意力和线性注意力的位置编码 - **Transformer-to-Hybrid 继续训练**：在预训练权重上做架构转换，训练预算仅为从头训练的约 25% - **百万 token 上下文**：在 NVIDIA RTX 5090/A6000D 上支持 1M+ token 推理 - 比 Qwen3-8B 快 3.5x（256K 序列长度，A6000D） - **发布时间**：2026年2月11日 --- ## 二、混合 Attention 架构设计原理 ### 1. GLA (Gated Linear Attention) - **论文**：*Gated Linear Attention Transformers with Hardware-Efficient Training*（arXiv:2312.06635） - GLA 是 Lightning Attention 的一种变体，递推公式 `h_t = exp(-gamma) * h_{t-1} + k_t * v_t^T` - 核心优势：O(1) KV cache 增长，适合超长序列；用门控机制替代 softmax 的信息筛选 ### 2. 8 Standard + 24 GLA 的设计原理 - 根据项目文档和 config.json 中的 `mixer_types` 字段： - Layer 0, 9, 16, 17, 22, 29, 30, 31 为 `minicpm4`（标准稀疏注意力，即 InfLLM-v2） - 其余 24 层为 `lightning-attn`（GLA） - **设计理念**： - 8 层 standard attention 保证高保真长上下文建模（InfLLM-v2 的 top-K 稀疏块选择） - 24 层 GLA 提供全局高效线性注意力，O(N) 复杂度 - HALO 蒸馏策略确保架构转换后性能不退化 ### 3. dense_len=8192 的选择依据 - `sparse_config` 中 `dense_len=8192`：序列长度低于此值时走全量 dense attention，超过后切换到稀疏 attention - 选择 8192 的理由（从 MiniCPM4 的文档推断）： - 8K 以下稀疏化收益有限（topk=64 block 中大部分块都会被选中） - 8K 以上稀疏化收益显著，计算量降至 <5% token 参与 attention - 与 `block_size=64`、`topk=64`、`window_size=2048` 参数协同 ### 4. InfLLM-v2 - **论文**：*InfLLM-V2: Dense-Sparse Switchable Attention for Seamless Short-to-Long Adaptation*（arXiv:2509.24663） - 核心机制： - `compress_k`：用 kernel_size=32, stride=16 的滑窗压缩 KV - `stage1`：block_score 计算各 block 相关性 - `stage2`：top-K sparse FlashAttention - 支持 dense-sparse 无缝切换（短序列 dense，长序列 sparse） - 训练成本：仅需 5B 长文本 token 即可训练出稀疏注意力模型 --- ## 三、EAGLE-3 Speculative Decoding […]

> DEVELOPER

你是一个学术论文深度调研专家。请对以下主题做非常深入的论文调研，使用 Tavily 搜索工具广泛检索。 ## 主题：线性注意力 / SSM / 状态模型 的推测解码验证机制 背景：我们有一个 MiniCPM-SALA 模型，32层混合架构：8层 standard attention + 24层 GLA (Gated Linear Attention / Lightning Attention)。使用 EAGLE-3 推测解码。GLA 层有递推状态 h_t = exp(-γ)*h_{t-1} + k_t*v_t^T，verify 时需要处理状态回滚和树验证。 已知相关论文：STree (NeurIPS 2025, arXiv:2505.14969) — SSM tree verify。 请深入调研以下方向： 1. **STree 的完整算法细节**：STree 如何处理 SSM/Mamba 的 tree verify？A-matrix 累乘的具体公式？与 EAGLE tree verify 的本质区别？性能数据？ 2. **Mamba/SSM 推测解码**：所有关于 Mamba 系列模型做推测解码的论文，包括 Mamba-2、Jamba 等混合架构的 spec decode 方案 3. **Linear attention 的推测解码**：GLA、RetNet、RWKV、DeltaNet 等线性注意力模型如何做 spec decode？状态回滚机制？ 4. **State rollback in speculative decoding**：所有关于循环状态模型（RNN/SSM/linear attention）在 spec decode 中状态管理的论文 5. **Hybrid model speculative decoding**：混合架构（attention + SSM/linear）的 spec decode 验证有什么特殊挑战？已有哪些解决方案？ 6. **ReGLA / Retention speculative decoding**：ReGLA 的完整算法，以及任何 retention 模型的 spec decode 方案 每个论文请提供： - 完整标题、arXiv ID、会议/时间 - 核心算法的详细描述（不是一句话概括） - 与 MiniCPM-SALA 的 GLA 24 层混合架构的关联 - 如果有代码，给出 GitHub 地址 请尽量多搜索，每个方向至少搜索 2-3 次，用不同的关键词组合。

> DEVELOPER

你是一个学术论文深度调研专家。请对以下主题做非常深入的论文调研，使用 Tavily 搜索工具广泛检索。 ## 主题：推测解码验证（verify）算法的最新进展（2025-2026） 背景：我们已经了解了 MARS、Fuzzy SD、DIVERSED、Traversal Verification、SVIP、FASER 等论文。现在需要找到更多、更新的验证算法改进论文。 请深入调研以下方向： 1. **Tree verification 算法**： - 所有关于 tree-structured speculative decoding 验证算法的论文 - tree 的形状优化（如何构建更好的 draft tree） - tree verify 的数学保证（无损性证明） - 除了 EAGLE 的 greedy verify 外还有什么 verify 算法？ 2. **概率匹配验证**： - speculative sampling 的精确算法及其变体 - 温度采样 vs greedy 验证的理论差异 - 多 token 联合接受概率（joint acceptance probability）的最新理论 - rejection sampling 在 spec decode 中的变体 3. **Early exit / adaptive verification**： - 验证过程中的提前退出机制 - per-layer early exit 在 spec decode 中的应用 - confidence-based verification 4. **Batched verification**： - 多请求 batch 下的验证算法优化 - ragged batch tree verify - FlashInfer / vLLM / SGLang 的 tree verify 实现对比 5. **2025-2026 新论文**： - 搜索 arXiv 上 2025 年下半年到 2026 年的 spec decoding 新论文 - 特别关注 ICLR 2026、NeurIPS 2025、ICML 2025 的相关接收论文 - 搜索关键词：speculative decoding verification, tree verification, acceptance rate, draft verification 6. **Verification for quantized models**： - 量化模型（W4A16, FP4, INT4）的 spec decode 验证有什么特殊问题？ - 量化误差如何影响接受率？ - 除了 QSPEC 外还有什么方案？ 每个论文请提供：完整标题、arXiv ID、会议/时间、核心算法详细描述、与 EAGLE-3 的兼容性分析。 请大量搜索，每个方向至少搜索 3 次，用不同关键词。特别关注最新的 2025-2026 论文。

> DEVELOPER

你是一个学术论文深度调研专家。请对以下主题做非常深入的论文调研，使用 Tavily 搜索工具广泛检索。 ## 主题：GLA / Linear Attention 状态管理 + 推测解码的交互问题 背景：MiniCPM-SALA 有 24 层 GLA (Gated Linear Attention)，状态公式 h_t = exp(-γ)*h_{t-1} + k_t*v_t^T。在 EAGLE-3 推测解码中： - verify 时不直接修改 temporal state，而是写入 intermediate_ssm 缓冲区 - verify 结束后通过 update_mamba_state_after_mtp_verify 做 rollback - 树验证时通过 retrieve_parent_token 回溯到正确父节点状态 - Phased Verify Phase-2 使用 Phase-1 最终 state 作为起点（非精确回溯） 已知代码中的问题： - mamba_verify_update 占用 verify 期 index kernel 的 98.4%（3D fancy scatter） - Phased Verify 的 GLA state 近似可能在长 context 下产生累积误差 - InfLLM-v2 sparse k1/k2 分配在 verify 后需要补偿 请深入调研以下方向： 1. **Linear attention state checkpointing for speculative decoding**： - 如何高效地保存和恢复 linear attention 的递推状态？ - 有没有避免 3D fancy scatter 的方案？ - Triton kernel 融合 scatter 的相关工作 2. **Tree verification in stateful models**： - 树形 draft tree 在有递推状态的模型中如何正确验证？ - 状态分支（state branching）的数学正确性 - STree 以外还有没有处理 SSM/linear attention tree verify 的方案？ 3. **State approximation in multi-phase verification**： - 分阶段验证时，后续阶段使用前一阶段最终状态作为起点的误差分析 - 有没有理论分析这种近似对接受率的影响？ - 增量状态更新 vs 全量回滚的 trade-off 4. **InfLLM / sparse attention + speculative decoding**： - 稀疏注意力模型做 spec decode 时的特殊挑战 - KV cache 压缩对 spec decode verify 的影响 - block-level sparse attention 与 tree verify 的交互 5. **Flash Linear Attention (FLA) library**： - FLA 库对 speculative decoding 的支持 - FLA 中的 tree verify 实现 - GLA / DeltaNet / KDA 在 FLA 中的推理优化 6. **Mamba-2 speculative decoding implementation details**： - SGLang / vLLM 中 Mamba-2 的 spec decode 实现 - Mamba 状态的 verify 后处理 - 与我们的 GLA verify 后处理的异同 请大量搜索，使用关键词如：linear attention speculative decoding, GLA state management, SSM verify, mamba speculative decoding, flash linear attention tree verify, state rollback speculative 等。

> DEVELOPER

你是一个学术论文深度调研专家。请对以下主题做非常深入的论文调研，使用 Tavily 搜索工具广泛检索。 ## 主题：推测解码 Tree Verify 的数学理论与实现细节 背景：EAGLE-3 使用 tree verify（topk=2, dtn=5），verify_tree_greedy_func 做贪婪匹配。已知 Traversal Verification 提出了 bottom-up 序列级接受概率。需要更深入了解 tree verify 的数学基础和工程实现。 请深入调研以下方向： 1. **Tree verify 的无损性理论**： - Leviathan et al. 2023 (speculative sampling) 的原始证明 - 多 token tree 验证的无损性如何证明？ - 不同的采样/验证策略（greedy vs sampling vs top-k）的无损性条件 - 概率匹配在 tree verify 中的精确数学 2. **Draft tree 构建优化**： - EAGLE-2 的动态树构建算法细节 - 最优 draft tree 形状的理论分析（什么形状的树能最大化期望接受长度？） - 树的深度 vs 广度的 trade-off（spec_steps vs topk） - 自适应树构建（根据 draft confidence 动态调整） 3. **Verification + Sampling 的交互**： - temperature > 0 时的验证算法 - top-p / top-k sampling 与 speculative decoding 验证的兼容性 - repetition penalty / frequency penalty 在 spec decode 中的处理 - 结构化输出（JSON mode / grammar）与 spec decode 验证 4. **Medusa / multi-head verification**： - Medusa 的验证算法与 EAGLE tree verify 的数学对比 - multi-token prediction (MTP) 验证算法 - 并行 head vs 树形验证的理论效率对比 5. **FlashInfer tree attention 实现**： - FlashInfer 的 BatchDecodeWithPagedKVCacheWrapper 对 tree verify 的支持 - tree mask 的实现细节 - FlashInfer vs custom Triton kernel 的 tree attention 性能对比 6. **数学分析工具**： - 期望接受长度 E[AL] 的精确计算公式 - 不同 tree 形状下的 E[AL] 分析 - 接受率的理论上界（给定 draft-target KL 散度时） 搜索关键词：tree verification speculative decoding, lossless speculative sampling proof, draft tree optimization, EAGLE tree verify algorithm, FlashInfer tree attention, expected acceptance length, speculative sampling temperature, Medusa verification algorithm 等。 请大量搜索，每个方向至少搜索 2-3 次。

> DEVELOPER

你是一个学术论文和开源代码调研专家。请对以下主题做非常深入的调研，使用 Tavily 搜索和 Web 搜索工具。 ## 主题：SGLang / vLLM / TRT-LLM 的推测解码实现对比 背景：我们使用 SGLang 的 EAGLE-3 推测解码实现，包括 V1 EAGLEWorker 和 V2 overlap-schedule 版本。需要了解其他框架的实现方式，特别是 verify 阶段和状态管理的差异。 请深入调研以下方向： 1. **SGLang EAGLE 实现的最新进展**： - 搜索 SGLang GitHub 上的 speculative decoding PR 和 issue - spec v2 (overlap) 的完整实现细节 - 2026 Q2 Speculative Decoding Roadmap (#23005) 的具体内容 - HiCache for hybrid models (#12826) 的进展 - CUDA graph + spec decode 的最新修复 2. **vLLM speculative decoding 实现**： - vLLM 的 EAGLE 实现与 SGLang 的差异 - vLLM 的 Mamba/SSM spec decode 实现 - vLLM 的 tree verify 实现 - vLLM 的 RejectionSampler 和 speculative decoding 的验证流程 3. **TensorRT-LLM speculative decoding**： - TRT-LLM 的 EAGLE/medusa 实现 - TRT-LLM 的 tree verify kernel - TRT-LLM 与 SGLang/vLLM 的 verify 性能对比 4. **框架间的 verify 算法差异**： - 各框架的 tree verify 算法实现差异 - 各框架对 Mamba/SSM state 的 verify 后处理 - 各框架的 CUDA graph + spec decode 支持 5. **Speculative decoding benchmark**： - 各框架在相同模型上的 spec decode 性能对比 - EAGLE-3 在不同框架上的吞吐差异 - Blackwell (sm_120) 上的 spec decode 兼容性 6. **开源 spec decode 训练框架**： - SpecForge (SGLang) 的最新进展 - 其他 EAGLE/medusa 训练框架 - draft model 训练的最佳实践 请搜索 GitHub issues/PRs、arXiv 论文、技术博客等。每个方向至少搜索 2-3 次。

> DEVELOPER

你是一个学术论文深度调研专家。请对以下主题做非常深入的论文调研，使用 Tavily 搜索工具广泛检索。 ## 主题：推测解码接受率（acceptance rate）的理论分析与优化 背景：EAGLE-3 在长上下文下 acceptance rate 下降（adj_al 从 2.3 降到 1.24）。需要理解接受率的理论基础和优化方法。 请深入调研以下方向： 1. **接受率的精确数学公式**： - speculative sampling 的接受概率公式：p_accept = min(1, p_target(x)/p_draft(x)) - 期望接受长度 E[AL] 的精确公式（chain 和 tree 两种） - 接受率与 KL 散度的关系 - 多步接受概率的累积公式 2. **接受率的理论上界**： - 给定 draft-target 分布距离时，接受率的上界是多少？ - 不同验证策略（greedy vs sampling vs tree）的接受率上界 - 信息论视角：接受率与互信息的关系 3. **Long-context acceptance rate degradation 的理论分析**： - 为什么长上下文下接受率会系统性下降？有没有理论解释？ - position encoding 对接受率的影响（RoPE 外推 → attention score 偏移 → draft 质量下降 → 接受率下降） - 上下文长度 vs 接受率的定量关系 4. **Draft-target distribution mismatch 分析**： - 如何度量 draft 和 target 分布的匹配度？ - KL 散度、总变差距离、Wasserstein 距离与接受率的关系 - 量化（W4A16, FP4）对 draft-target 匹配度的影响 5. **接受率优化的理论方法**： - 降低 draft-target 分布距离的理论方法 - Draft model capacity 与接受率的关系（多大的 draft model 才够？） - 温度/采样策略对接受率的影响 6. **Recent theoretical papers (2025-2026)**： - 搜索最新的 speculative decoding 理论分析论文 - ICLR 2026 / NeurIPS 2025 / ICML 2025 中的 spec decoding 理论论文 - 搜索关键词：speculative decoding theory, acceptance rate analysis, draft model optimality, speculative sampling optimality 请大量搜索，每个方向至少搜索 2-3 次，用不同关键词组合。特别关注理论性强的论文（有定理和证明的）。

> AGENT

API Error: 503 当前分组 default 下对于模型 claude-sonnet-4-6 无可用渠道 (request id: 2026042720571066722520109805175). This is a server-side issue, usually temporary — try again in a moment. If it persists, check status.claude.com.

> DEVELOPER

你是一个学术论文深度调研专家。请对以下主题做非常深入的论文调研，使用 Tavily 搜索工具广泛检索。 ## 主题：线性注意力 / SSM / 状态模型 的推测解码验证机制 背景：我们有一个 MiniCPM-SALA 模型，32层混合架构：8层 standard attention + 24层 GLA (Gated Linear Attention / Lightning Attention)。使用 EAGLE-3 推测解码。GLA 层有递推状态 h_t = exp(-γ)*h_{t-1} + k_t*v_t^T，verify 时需要处理状态回滚和树验证。 已知相关论文：STree (NeurIPS 2025, arXiv:2505.14969) — SSM tree verify。 请深入调研以下方向： 1. **STree 的完整算法细节**：STree 如何处理 SSM/Mamba 的 tree verify？A-matrix 累乘的具体公式？与 EAGLE tree verify 的本质区别？性能数据？ 2. **Mamba/SSM 推测解码**：所有关于 Mamba 系列模型做推测解码的论文，包括 Mamba-2、Jamba 等混合架构的 spec decode 方案 3. **Linear attention 的推测解码**：GLA、RetNet、RWKV、DeltaNet 等线性注意力模型如何做 spec decode？状态回滚机制？ 4. **State rollback in speculative decoding**：所有关于循环状态模型（RNN/SSM/linear attention）在 spec decode 中状态管理的论文 5. **Hybrid model speculative decoding**：混合架构（attention + SSM/linear）的 spec decode 验证有什么特殊挑战？已有哪些解决方案？ 6. **ReGLA / Retention speculative decoding**：ReGLA 的完整算法，以及任何 retention 模型的 spec decode 方案 每个论文请提供： - 完整标题、arXiv ID、会议/时间 - 核心算法的详细描述（不是一句话概括） - 与 MiniCPM-SALA 的 GLA 24 层混合架构的关联 - 如果有代码，给出 GitHub 地址 请尽量多搜索，每个方向至少搜索 2-3 次，用不同的关键词组合。

> AGENT

我将对这个主题进行深入的论文调研。让我从多个方向并行搜索开始。

> AGENT

API Error: 503 当前分组 default 下对于模型 claude-sonnet-4-6 无可用渠道 (request id: 2026042720573386795237861091103). This is a server-side issue, usually temporary — try again in a moment. If it persists, check status.claude.com.

> AGENT

Tavily 搜索配额已用尽。让我尝试使用 Tavily 的研究工具和其他可用方式继续调研。

> AGENT

Tavily 的所有工具都超出了配额限制。让我尝试用其他方式获取论文信息。

> DEVELOPER

你是一个学术论文深度调研专家。请对以下主题做非常深入的论文调研，使用 Tavily 搜索工具广泛检索。 ## 主题：推测解码验证（verify）算法的最新进展（2025-2026） 背景：我们已经了解了 MARS、Fuzzy SD、DIVERSED、Traversal Verification、SVIP、FASER 等论文。现在需要找到更多、更新的验证算法改进论文。 请深入调研以下方向： 1. **Tree verification 算法**： - 所有关于 tree-structured speculative decoding 验证算法的论文 - tree 的形状优化（如何构建更好的 draft tree） - tree verify 的数学保证（无损性证明） - 除了 EAGLE 的 greedy verify 外还有什么 verify 算法？ 2. **概率匹配验证**： - speculative sampling 的精确算法及其变体 - 温度采样 vs greedy 验证的理论差异 - 多 token 联合接受概率（joint acceptance probability）的最新理论 - rejection sampling 在 spec decode 中的变体 3. **Early exit / adaptive verification**： - 验证过程中的提前退出机制 - per-layer early exit 在 spec decode 中的应用 - confidence-based verification 4. **Batched verification**： - 多请求 batch 下的验证算法优化 - ragged batch tree verify - FlashInfer / vLLM / SGLang 的 tree verify 实现对比 5. **2025-2026 新论文**： - 搜索 arXiv 上 2025 年下半年到 2026 年的 spec decoding 新论文 - 特别关注 ICLR 2026、NeurIPS 2025、ICML 2025 的相关接收论文 - 搜索关键词：speculative decoding verification, tree verification, acceptance rate, draft verification 6. **Verification for quantized models**： - 量化模型（W4A16, FP4, INT4）的 spec decode 验证有什么特殊问题？ - 量化误差如何影响接受率？ - 除了 QSPEC 外还有什么方案？ 每个论文请提供：完整标题、arXiv ID、会议/时间、核心算法详细描述、与 EAGLE-3 的兼容性分析。 请大量搜索，每个方向至少搜索 3 次，用不同关键词。特别关注最新的 2025-2026 论文。

> AGENT

我将对推测解码验证算法的最新进展进行系统性深度调研。每个方向我会使用不同关键词多次搜索，确保覆盖面广。 先从最核心的方向开始——tree verification 算法和 2025-2026 新论文。

> AGENT

API Error: 503 当前分组 default 下对于模型 claude-sonnet-4-6 无可用渠道 (request id: 2026042720575692722747317109118). This is a server-side issue, usually temporary — try again in a moment. If it persists, check status.claude.com.

> AGENT

Tavily 搜索 API 额度已用尽。让我尝试使用 Tavily 的 research 工具，以及通过其他方式获取信息。

> AGENT

API Error: 503 当前分组 default 下对于模型 claude-sonnet-4-6 无可用渠道 (request id: 2026042720580921475310529982170). This is a server-side issue, usually temporary — try again in a moment. If it persists, check status.claude.com.

> AGENT

Tavily API 额度完全用尽。让我尝试通过 web crawl 直接抓取 arXiv 和相关学术资源。

> AGENT

API Error: 503 当前分组 default 下对于模型 claude-sonnet-4-6 无可用渠道 (request id: 2026042720581168784306174018610). This is a server-side issue, usually temporary — try again in a moment. If it persists, check status.claude.com.

> AGENT

Tavily 的所有工具都已达到额度上限。让我改用 Bash 工具直接通过 curl 抓取 arXiv API 和网页来获取论文信息。

> AGENT

arXiv API 似乎没有响应。让我试试其他方式。

> AGENT

API Error: 503 当前分组 default 下对于模型 claude-sonnet-4-6 无可用渠道 (request id: 2026042720583124835750953997124). This is a server-side issue, usually temporary — try again in a moment. If it persists, check status.claude.com.

> DEVELOPER

你是一个学术论文深度调研专家。请对以下主题做非常深入的论文调研，使用 Tavily 搜索工具广泛检索。 ## 主题：线性注意力 / SSM / 状态模型 的推测解码验证机制 背景：MiniCPM-SALA 模型，32层混合架构：8层 standard attention + 24层 GLA (Gated Linear Attention / Lightning Attention)。EAGLE-3 推测解码。GLA 层有递推状态 h_t = exp(-γ)*h_{t-1} + k_t*v_t^T，verify 时需要处理状态回滚和树验证。 已知：STree (NeurIPS 2025, arXiv:2505.14969) — SSM tree verify。 请深入调研： 1. **STree 完整算法**：如何处理 SSM/Mamba 的 tree verify？A-matrix 累乘的具体公式？与 EAGLE tree verify 的本质区别？性能数据？ 2. **Mamba/SSM 推测解码**：Mamba-2、Jamba 等混合架构的 spec decode 方案 3. **Linear attention 推测解码**：GLA、RetNet、RWKV、DeltaNet 等线性注意力模型如何做 spec decode？状态回滚机制？ 4. **State rollback in speculative decoding**：循环状态模型（RNN/SSM/linear attention）在 spec decode 中状态管理的论文 5. **Hybrid model speculative decoding**：混合架构（attention + SSM/linear）的 spec decode 验证特殊挑战？已有解决方案？ 6. **ReGLA / Retention speculative decoding**：ReGLA 完整算法，retention 模型的 spec decode 方案 每个论文：完整标题、arXiv ID、会议/时间、核心算法详细描述、与 MiniCPM-SALA GLA 24 层混合架构的关联、GitHub 地址（如有）。每个方向至少搜索 2-3 次，用不同关键词。

> AGENT

我将开始对线性注意力/SSM/状态模型的推测解码验证机制进行深度论文调研。每个方向我会用不同关键词多次搜索。

> AGENT

arXiv API 的 OR 搜索把结果搞乱了，关键词被拆分了。我需要用更精确的引号搜索。让我尝试多种精确搜索。

> AGENT

Tavily search 配额已用尽。我换用 Tavily extract 和 research 工具来获取信息。

> AGENT

Tavily 全部 API 配额已耗尽。让我尝试用 extract 直接从 arXiv 页面获取论文信息。

> AGENT

Tavily 所有 API 都已超限。让我用 Bash 的 curl 直接从 arXiv 和学术搜索获取论文信息。

> AGENT

有结果了。让我提取论文标题和ID。

> AGENT

成功获取了 STree 论文的基本信息。让我继续获取更多论文。

> AGENT

Semantic Scholar 也被限流了。让我尝试直接从 arXiv 和其他来源获取论文内容。

> AGENT

很好，获得了大量结果。让我继续搜索更多方向。

> DEVELOPER

深度调研 Traversal Verification 论文（NeurIPS 2025, arXiv:2505.12398）与线性注意力/SSM模型推测解码verify的结合。 需要调研的内容： 1. Traversal Verification 的完整算法细节（bottom-up DFS验证、序列级接受概率计算、拒绝后分布更新公式） 2. 论文中是否在SSM/线性注意力模型（如Mamba、GLA、RetNet）上做过实验？如果有，数据是什么？ 3. 线性注意力模型的state递推特性（h_t = decay * h_{t-1} + k_t * v_t^T）如何影响Traversal Verification的state回滚？与传统softmax attention的KV cache回滚有何本质区别？ 4. Traversal Verification在tree verify场景下对GLA层的intermediate_ssm缓冲区有什么新要求？ 5. 论文的代码是否开源？如果有，核心数据结构是什么？ 使用Tavily搜索，关键词：Traversal Verification speculative decoding, bottom-up verification SSM, leaf-to-user_4813494d verify Mamba, arXiv:2505.12398 code implementation 报告要求：只记录调查发现的事实和论文内容，不做结论或行动建议。用简体中文。

> DEVELOPER

深度调研 STree 论文（NeurIPS 2025, arXiv:2505.14969）的完整实现细节，特别关注其与GLA/线性注意力模型verify的结合。 需要调研的内容： 1. STree的完整算法：如何用SSM的A-matrix累乘处理tree verify中的non-causal states？给出公式和推导 2. STree如何处理GLA类型的递推state（h_t = exp(-gamma) * h_{t-1} + k_t * v_t^T）在tree branching时的正确回滚？ 3. STree与EAGLE-3 tree verify的GLA state处理（intermediate_ssm + retrieve_parent_token）有什么本质区别？ 4. STree的实验数据：在哪些模型上测试了？acceptance length提升多少？是否有Mamba/GLA模型的数据？ 5. STree的开源代码：GitHub地址、核心kernel实现、与vLLM/SGLang的集成状态 6. STree对MiniCPM-SALA这种混合架构（8层sparse attention + 24层GLA）有什么特殊处理或建议？ 使用Tavily搜索，关键词：STree speculative decoding SSM, arXiv:2505.14969 tree verification linear attention, STree Mamba GLA state rollback, STree code GitHub 报告要求：只记录调查发现的事实和论文内容，不做结论或行动建议。用简体中文。

> AGENT

arXiv ID 不对应正确论文。让我用更精确的方式搜索。

> AGENT

非常好！让我继续搜索更多具体方向的关键论文。

> AGENT

找到了关键论文。让我继续深入搜索更多相关论文，并获取已找到论文的详细信息。

> AGENT

很好！现在让我获取几篇最重要的核心论文的详细摘要。

> AGENT

很好，找到了一些相关论文。让我继续深入搜索更多方向。

> AGENT

让我修复 Python 脚本的语法错误并重试。

> TOOL

[Request interrupted by user]

> TOOL

[Request interrupted by user]

> TOOL

[Request interrupted by user for tool use]

> TOOL

[Request interrupted by user for tool use]

> TOOL

[Request interrupted by user for tool use]

> DEVELOPER

你是推测解码（speculative decoding）验证（verify）机制的学术调研专家。请用 Tavily 进行深度文献检索，聚焦以下方向： **核心问题**：speculative decoding 中 verify 阶段的前沿创新，特别是 2025-2026 年的最新工作。 **调研方向**： 1. **Tree verification 创新**：除了 EAGLE 的 top-down greedy verify，还有哪些 tree verify 方式？包括但不限于： - Bottom-up / leaf-to-user_4813494d verify（Traversal Verification 之外还有没有？） - 并行 verify 多个 draft token 的新算法 - Tree 结构与 verify 策略的联合优化 - 搜索 "tree verification speculative decoding 2025 2026" 2. **Acceptance rate 优化算法**：verify 阶段不改变 draft model，只改接受规则： - Margin-aware / confidence-aware verify（MARS 之外） - Distribution-aware verify（Fuzzy SD / DIVERSED 之外） - 搜索 "acceptance rate optimization speculative decoding verify 2025 2026" - 搜索 "relaxed verification speculative decoding" - 搜索 "speculative decoding acceptance length improvement" 3. **Early exit verify**：verify 过程中提前退出，减少计算 - 搜索 "early exit speculative decoding verify 2025 2026" - 搜索 "FASER speculative decoding early exit" - 搜索 "progressive verification speculative decoding" 4. **Batched / parallel verify**：多个请求或多个 draft tree 并行验证 - 搜索 "batched verification speculative decoding" - 搜索 "parallel speculative decoding verification" 5. **Verify 计算 overhead 优化**： - 搜索 "speculative decoding verification overhead reduction" - 搜索 "speculative decoding verify latency optimization" 对每篇找到的论文，请记录： - 完整标题和 arXiv ID - 发表会议/时间 - 核心算法（具体公式/伪代码） - 与标准 EAGLE verify 的关键区别 - 实验数据（acceptance length 提升、throughput 提升） - 是否需要重新训练 draft model 请用 mcp__tavily__tavily_search 工具进行搜索，每个方向至少 2-3 次搜索，确保广度。搜索 query 要具体，包含年份限制。

> TOOL

[Request interrupted by user]

> DEVELOPER

你是推测解码（speculative decoding）验证（verify）机制的学术调研专家。请用 Tavily 进行深度文献检索，聚焦以下方向： **核心问题**：speculative decoding 中 verify 阶段的前沿创新，特别是 2025-2026 年的最新工作。 **调研方向**： 1. **Tree verification 创新**：除了 EAGLE 的 top-down greedy verify，还有哪些 tree verify 方式？ - 搜索 "tree verification speculative decoding 2025 2026" - 搜索 "bottom-up verification speculative decoding" - 搜索 "speculative decoding tree structure optimization 2025" 2. **Acceptance rate 优化算法**：verify 阶段不改 draft model，只改接受规则 - 搜索 "acceptance rate optimization speculative decoding verify 2025 2026" - 搜索 "relaxed verification speculative decoding" - 搜索 "margin aware speculative verification 2025 2026" - 搜索 "speculative decoding acceptance length improvement algorithm" 3. **Early exit verify** - 搜索 "early exit speculative decoding verify 2025 2026" - 搜索 "FASER speculative decoding early exit" - 搜索 "progressive verification speculative decoding" 4. **Batched / parallel verify** - 搜索 "batched verification speculative decoding" - 搜索 "parallel speculative decoding verification tree" 5. **Verify overhead 优化** - 搜索 "speculative decoding verification overhead reduction" - 搜索 "speculative decoding verify latency optimization 2025" 对每篇找到的论文，请记录：完整标题、arXiv ID、发表会议/时间、核心算法（具体公式/伪代码）、与标准 EAGLE verify 的关键区别、实验数据（acceptance length 提升、throughput 提升）、是否需要重新训练 draft model。 请用 mcp__tavily__tavily_search 工具搜索，每个方向至少 2-3 次搜索。搜索 query 要具体，包含年份限制。

> DEVELOPER

你是线性注意力（linear attention）和 SSM（state space model）推测解码验证的学术调研专家。请用 Tavily 进行深度文献检索。 **核心问题**：当 target model 使用线性注意力（GLA/Lightning Attention/Mamba/RetNet）或混合架构时，speculative decoding 的 verify 阶段有什么特殊的挑战和创新方案？ **背景**：MiniCPM-SALA 使用 8 层 standard attention + 24 层 GLA (Lightning Attention) 的混合架构。GLA 层有 temporal state（递推 h_t = exp(-γ)*h_{t-1} + k_t*v_t^T），verify 时需要处理 state 回滚/快照/恢复。 **调研方向**： 1. **SSM/Mamba + speculative decoding** - 搜索 "Mamba speculative decoding verification 2025 2026" - 搜索 "SSM state management speculative decoding" - 搜索 "state space model speculative decoding verify state rollback" - 搜索 "Mamba model speculative decoding acceptance rate" 2. **GLA / Linear Attention + speculative decoding** - 搜索 "gated linear attention speculative decoding 2025" - 搜索 "linear attention speculative decoding verification" - 搜索 "lightning attention speculative decoding" - 搜索 "recurrent attention speculative decoding verify" 3. **Hybrid attention + speculative decoding** - 搜索 "hybrid attention speculative decoding 2025 2026" - 搜索 "mixed attention speculative decoding verification" - 搜索 "sparse attention speculative decoding verify" 4. **SSM state management during verify** - 搜索 "SSM hidden state rollback speculative decoding" - 搜索 "Mamba state snapshot verification" - 搜索 "recurrent state checkpoint speculative decoding" - 搜索 "STree SSM tree verification" 5. **RetNet / RWKV + speculative decoding** - 搜索 "RetNet speculative decoding" - 搜索 "RWKV speculative decoding verification" - 搜索 "recurrent language model speculative decoding" 对每篇找到的论文，请记录：完整标题、arXiv ID、发表会议/时间、核心算法（特别是如何处理 SSM/线性注意力的 state 管理）、与 EAGLE verify 的关键区别、实验数据、是否需要重新训练。

> DEVELOPER

你是推测解码验证算法的学术调研专家，专注 verify 阶段的接受规则和分布匹配创新。请用 Tavily 进行深度文献检索。 **核心问题**：speculative decoding verify 时，如何设计更好的接受规则（acceptance rule）来提高 acceptance length，同时保证输出分布质量？ **调研方向**： 1. **Distribution matching verify** - 搜索 "speculative decoding distribution matching verification 2025 2026" - 搜索 "KL divergence speculative decoding acceptance" - 搜索 "distribution aware speculative decoding verify" - 搜索 "speculative decoding optimal acceptance rule" 2. **Relaxed / approximate verify** - 搜索 "relaxed speculative decoding verification 2025" - 搜索 "approximate verification speculative decoding" - 搜索 "lossy speculative decoding acceptance" - 搜索 "speculative decoding quality throughput tradeoff verification" 3. **Confidence-based verify** - 搜索 "confidence based speculative decoding verification 2025 2026" - 搜索 "entropy based speculative decoding draft termination" - 搜索 "speculative decoding adaptive verification" - 搜索 "SVIP speculative decoding entropy" 4. **Multi-token / sequence-level verify** - 搜索 "sequence level acceptance speculative decoding" - 搜索 "multi-token verification speculative decoding 2025" - 搜索 "joint acceptance speculative decoding tree" - 搜索 "block verification speculative decoding" 5. **Verify for quantized models** - 搜索 "quantized model speculative decoding verification 2025" - 搜索 "NVFP4 speculative decoding verify" - 搜索 "weight-only quantization speculative decoding acceptance" - 搜索 "speculative decoding mixed precision verify" 6. **Recent arXiv surveys / position papers** - 搜索 "speculative decoding survey 2025 2026" - 搜索 "speculative decoding verification taxonomy" - 搜索 "speculative decoding open problems 2026" 对每篇论文记录：完整标题、arXiv ID、核心算法（具体到公式级别）、与标准 speculative sampling (Leviathan et al. 2023, Chen et al. 2023) 的关键区别、实验数据、是否需要训练、适用条件。

> DEVELOPER

你是 EAGLE 推测解码的学术调研专家，专注 EAGLE 系列 verify 机制的最新变体和改进。请用 Tavily 进行深度文献检索。 **核心问题**：EAGLE-1/2/3 的 verify 机制（top-down greedy + tree attention）有哪些最新的改进和变体？ **调研方向**： 1. **EAGLE verify 最新改进** - 搜索 "EAGLE speculative decoding verification improvement 2025 2026" - 搜索 "EAGLE-3 verify optimization" - 搜索 "EAGLE tree verification acceptance improvement" - 搜索 "EAGLE speculative decoding long context verify" 2. **Draft tree 结构与 verify 联合优化** - 搜索 "draft tree structure optimization speculative decoding 2025" - 搜索 "speculative decoding tree topology verification" - 搜索 "adaptive draft tree speculative decoding" - 搜索 "speculative decoding tree width depth tradeoff" 3. **Medusa / multi-head verify 对比** - 搜索 "Medusa speculative decoding verification 2025" - 搜索 "multi-token prediction verification speculative decoding" - 搜索 "speculative decoding multi-head vs tree verification" 4. **Speculative decoding + CUDA graph / inference system** - 搜索 "speculative decoding CUDA graph verification 2025 2026" - 搜索 "speculative decoding verify kernel optimization" - 搜索 "speculative decoding verify memory optimization" 5. **EAGLE 在 SGLang/vLLM 中的最新实现** - 搜索 "SGLang EAGLE verification implementation 2025 2026" - 搜索 "vLLM speculative decoding verify 2025" - 搜索 "speculative decoding verify flashinfer tree attention" 6. **Verify 后处理优化** - 搜索 "speculative decoding verify post processing KV cache" - 搜索 "speculative decoding verify state update optimization" - 搜索 "speculative decoding accepted tokens KV cache management" 对每篇论文记录：完整标题、arXiv ID、核心算法、与 EAGLE 标准 verify 的关键区别、实验数据、系统实现细节。

> TOOL

[Request interrupted by user]

> TOOL

[Request interrupted by user]

> TOOL

[Request interrupted by user]

> TOOL

[Request interrupted by user]

> DEVELOPER

你是推测解码（speculative decoding）验证（verify）机制的学术调研专家。请用 Tavily 进行深度文献检索，聚焦 verify 阶段的前沿创新（2025-2026 年）。 **调研方向**： 1. **Tree verification 创新** - 搜索 "tree verification speculative decoding 2025 2026" - 搜索 "bottom-up verification speculative decoding" - 搜索 "speculative decoding tree structure optimization 2025" 2. **Acceptance rate 优化算法**（只改接受规则，不改 draft model） - 搜索 "acceptance rate optimization speculative decoding verify 2025 2026" - 搜索 "relaxed verification speculative decoding" - 搜索 "margin aware speculative verification 2025 2026" - 搜索 "speculative decoding acceptance length improvement algorithm" 3. **Early exit verify** - 搜索 "early exit speculative decoding verify 2025 2026" - 搜索 "FASER speculative decoding early exit" - 搜索 "progressive verification speculative decoding" 4. **Batched / parallel verify** - 搜索 "batched verification speculative decoding" - 搜索 "parallel speculative decoding verification tree" 5. **Verify overhead 优化** - 搜索 "speculative decoding verification overhead reduction 2025" - 搜索 "speculative decoding verify latency optimization 2025" 对每篇论文记录：完整标题、arXiv ID、发表会议/时间、核心算法（具体公式/伪代码）、与标准 EAGLE verify 的关键区别、实验数据、是否需要重新训练。每个方向至少 2-3 次搜索。

> AGENT

我将按照五个方向进行系统性文献检索，每个方向进行多次搜索。 **方向1: Tree Verification 创新**

> DEVELOPER

你是线性注意力（linear attention）和 SSM 推测解码验证的学术调研专家。请用 Tavily 进行深度文献检索。 **核心问题**：当 target model 使用线性注意力（GLA/Lightning Attention/Mamba/RetNet）或混合架构时，speculative decoding 的 verify 阶段有什么特殊挑战和创新方案？ **背景**：MiniCPM-SALA 使用 8 层 standard attention + 24 层 GLA (Lightning Attention) 混合架构。GLA 层有 temporal state（递推 h_t = exp(-γ)*h_{t-1} + k_t*v_t^T），verify 时需要处理 state 回滚/快照/恢复。 **调研方向**： 1. **SSM/Mamba + speculative decoding** - 搜索 "Mamba speculative decoding verification 2025 2026" - 搜索 "SSM state management speculative decoding" - 搜索 "state space model speculative decoding verify state rollback" - 搜索 "Mamba model speculative decoding acceptance rate" 2. **GLA / Linear Attention + speculative decoding** - 搜索 "gated linear attention speculative decoding 2025" - 搜索 "linear attention speculative decoding verification" - 搜索 "lightning attention speculative decoding" - 搜索 "recurrent attention speculative decoding verify" 3. **Hybrid attention + speculative decoding** - 搜索 "hybrid attention speculative decoding 2025 2026" - 搜索 "mixed attention speculative decoding verification" - 搜索 "sparse attention speculative decoding verify mismatch" 4. **SSM state management during verify** - 搜索 "SSM hidden state rollback speculative decoding" - 搜索 "Mamba state snapshot verification" - 搜索 "STree SSM tree verification" - 搜索 "recurrent state checkpoint speculative decoding" 5. **RetNet / RWKV + speculative decoding** - 搜索 "RetNet speculative decoding" - 搜索 "RWKV speculative decoding verification" - 搜索 "recurrent language model speculative decoding 2025" 对每篇论文记录：完整标题、arXiv ID、核心算法（特别是 SSM/线性注意力 state 管理）、与 EAGLE verify 的关键区别、实验数据、是否需要训练。

> AGENT

Tavily 搜索 API 额度已耗尽。我换用 Tavily 的 research 和 extract 工具来继续调研。

> AGENT

我来进行系统性深度文献检索，覆盖你指定的5个调研方向。先并行发起多组搜索。

> DEVELOPER

你是推测解码验证算法的学术调研专家，专注 verify 阶段的接受规则和分布匹配创新。请用 Tavily 进行深度文献检索。 **核心问题**：speculative decoding verify 时，如何设计更好的接受规则（acceptance rule）来提高 acceptance length，同时保证输出分布质量？ **调研方向**： 1. **Distribution matching verify** - 搜索 "speculative decoding distribution matching verification 2025 2026" - 搜索 "KL divergence speculative decoding acceptance" - 搜索 "distribution aware speculative decoding verify" - 搜索 "speculative decoding optimal acceptance rule" 2. **Relaxed / approximate verify** - 搜索 "relaxed speculative decoding verification 2025" - 搜索 "approximate verification speculative decoding" - 搜索 "lossy speculative decoding acceptance" - 搜索 "speculative decoding quality throughput tradeoff verification" 3. **Confidence-based verify** - 搜索 "confidence based speculative decoding verification 2025 2026" - 搜索 "entropy based speculative decoding draft termination" - 搜索 "SVIP speculative decoding entropy" - 搜索 "speculative decoding adaptive verification confidence" 4. **Multi-token / sequence-level verify** - 搜索 "sequence level acceptance speculative decoding" - 搜索 "multi-token verification speculative decoding 2025" - 搜索 "joint acceptance speculative decoding tree" - 搜索 "block verification speculative decoding" 5. **Verify for quantized models** - 搜索 "quantized model speculative decoding verification 2025" - 搜索 "NVFP4 speculative decoding verify" - 搜索 "weight-only quantization speculative decoding acceptance" - 搜索 "speculative decoding mixed precision verify" 6. **Recent surveys** - 搜索 "speculative decoding survey 2025 2026" - 搜索 "speculative decoding verification taxonomy" - 搜索 "speculative decoding open problems 2026" 对每篇论文记录：完整标题、arXiv ID、核心算法（具体到公式级别）、与标准 speculative sampling (Leviathan et al. 2023, Chen et al. 2023) 的关键区别、实验数据、是否需要训练、适用条件。

> AGENT

Tavily 的所有工具（search、research、extract、crawl、map）均已超配额限制。让我尝试通过其他途径获取信息。

> AGENT

我将对推测解码验证算法进行全面深度调研。让我按照六个方向并行搜索。

> AGENT

Tavily 搜索配额已耗尽。让我改用 `tavily_research` 工具进行深度调研，这个工具可能有独立的配额。

> DEVELOPER

你是 EAGLE 推测解码的学术调研专家，专注 EAGLE 系列 verify 机制的最新变体、系统实现和后处理优化。请用 Tavily 进行深度文献检索。 **核心问题**：EAGLE-1/2/3 的 verify 机制（top-down greedy + tree attention）有哪些最新改进变体？系统层面如何优化 verify？ **调研方向**： 1. **EAGLE verify 最新改进** - 搜索 "EAGLE speculative decoding verification improvement 2025 2026" - 搜索 "EAGLE-3 verify optimization" - 搜索 "EAGLE tree verification acceptance improvement" - 搜索 "EAGLE speculative decoding long context verify" 2. **Draft tree 结构与 verify 联合优化** - 搜索 "draft tree structure optimization speculative decoding 2025" - 搜索 "speculative decoding tree topology verification" - 搜索 "adaptive draft tree speculative decoding" - 搜索 "speculative decoding tree width depth tradeoff" 3. **Speculative decoding + CUDA graph / inference system** - 搜索 "speculative decoding CUDA graph verification 2025 2026" - 搜索 "speculative decoding verify kernel optimization" - 搜索 "speculative decoding verify memory optimization" 4. **EAGLE 在 SGLang/vLLM 中的最新实现** - 搜索 "SGLang EAGLE verification implementation 2025 2026" - 搜索 "vLLM speculative decoding verify 2025" - 搜索 "speculative decoding verify flashinfer tree attention" 5. **Verify 后处理优化** - 搜索 "speculative decoding verify post processing KV cache" - 搜索 "speculative decoding verify state update optimization" - 搜索 "speculative decoding accepted tokens KV cache management" 6. **Medusa / multi-head verify 对比** - 搜索 "Medusa speculative decoding verification 2025" - 搜索 "multi-token prediction verification speculative decoding" - 搜索 "speculative decoding multi-head vs tree verification comparison" 对每篇论文记录：完整标题、arXiv ID、核心算法、与 EAGLE 标准 verify 的关键区别、实验数据、系统实现细节。

> AGENT

Tavily 全部 API 配额已耗尽。让我尝试通过其他方式获取文献信息——用 Tavily 的 extract 工具直接抓取 arXiv 搜索结果页面，以及用 crawl 工具来获取信息。

> AGENT

HTML 太长了，我需要更高效地提取论文标题和 arXiv ID。让我用更好的方法解析。

> AGENT

我来进行系统性的深度文献检索，覆盖所有6个调研方向。让我并行发起多组搜索。

> AGENT

Tavily search API 配额已用尽。让我尝试使用 Tavily 的 research 工具，以及通过 web crawl/extract 方式获取信息。

> AGENT

Tavily 全部 API 都已达配额限制。让我尝试通过直接抓取 arXiv 和关键论文页面来获取信息。

> AGENT

所有 Tavily API 工具的配额都已耗尽。让我改用 Bash 工具通过 `curl` 直接访问 arXiv API 来进行文献检索，这不需要 Tavily 配额。

> AGENT

Tavily 搜索配额已用尽。让我尝试使用 Tavily 的 research 和 extract 功能，以及直接爬取相关学术论文页面。

> AGENT

Tavily research 也超出配额。让我尝试 extract 功能直接抓取已知的 arXiv 论文页面。

> AGENT

所有 Tavily API 端点均已超配额。让我使用 Bash 工具通过 curl 直接访问 arXiv 和 Semantic Scholar 来进行文献检索。

> AGENT

找到了大量论文 ID。现在让我获取这些论文的标题和摘要信息，重点关注 2025-2026 年的论文。

> AGENT

Tavily 的所有功能（search / research / extract / crawl / map）都已超出配额限制。让我用 Bash 直接通过 curl 抓取 arXiv 和 Semantic Scholar 的 API 来完成调研。

> AGENT

arXiv API 可能被阻断了。让我尝试其他方法。

> AGENT

Semantic Scholar 也被限速了。让我间隔后逐个查询，同时尝试 arXiv API。

> AGENT

HTTPS 可用。让我用 HTTPS 来查询。

> AGENT

Semantic Scholar 也限速了。让我间隔后重试，同时尝试 arXiv API。

> AGENT

现在我需要获取这些论文的详细信息。让我使用 arXiv API 来批量获取标题和摘要。

> AGENT

arXiv 需要用 HTTPS。让我修正。

> AGENT

arXiv API 的通用关键词搜索返回了太多不相关的结果。让我使用更精确的搜索词，特别是针对 NLP/ML 领域的论文。

> AGENT

好，arXiv API 可用。让我并行搜索多个方向。

> AGENT

很好，arXiv API 可用。已经发现了多篇关键论文。让我继续搜索更多方向。

> AGENT

很好，找到了一些相关论文。让我继续搜索更多特定方向的论文。

> AGENT

非常好，已经获得了大量结果。让我继续搜索更多方向，并获取关键论文的详细内容。

> AGENT

非常好，已发现大量相关论文。让我继续搜索更多方向并获取关键论文的详细内容。

> AGENT

arXiv API 的 XML 解析没有正确提取 title。让我修正解析方式。

> AGENT

有些请求失败了，可能是因为 arXiv API 的请求频率限制。让我稍微等待后分批查询。

> AGENT

这个方法可行。让我批量获取所有论文的标题。

> AGENT

arXiv API 开始限速了。让我改用 Semantic Scholar API（间隔调用）来获取更多论文，然后抓取关键论文的详细内容。

> AGENT

arXiv API 限速了。让我等更长时间再继续查询。

> AGENT

arXiv API 似乎在限流。让我尝试 Semantic Scholar（间隔后）和直接抓取关键论文的 HTML 页面。

> AGENT

现在让我获取更多关键论文的详细信息。

> AGENT

Semantic Scholar 再次限速了。让我直接从 arXiv 获取关键论文的 PDF 摘要内容。

> AGENT

API 再次限速了。让我直接用 arXiv ID 来获取之前发现的几篇关键论文的详细信息，同时也用 Semantic Scholar API 来搜索更多相关文献。

> AGENT

已经找到了关键的 SpecMamba 和 Mamba Drafters 论文。让我继续搜索更多相关论文。

> AGENT

Semantic Scholar 恢复了。让我读取完整结果并继续搜索更多方向。

> AGENT

让我获取更多关键论文的详细信息。

> AGENT

很好，获得了大量结果。让我继续搜索剩余方向，并抓取几篇核心论文的详细内容。

> AGENT

很好，现在我已经获得了所有论文标题。让我筛选出与 verify 阶段创新最直接相关的论文，获取它们的摘要和详细信息。

> AGENT

arXiv API 也被限速了。让我改用 Semantic Scholar 并使用更温和的请求频率。

> AGENT

Semantic Scholar 似乎又在限流了。让我尝试直接用 curl 抓取关键论文的 arXiv HTML 页面。

> AGENT

两个 API 都被限速了。让我尝试直接从 arXiv HTML 页面获取论文信息。

> AGENT

很好，成功获取了关键论文。继续获取更多论文。

> AGENT

现在让我获取更多关键论文的摘要信息。

> AGENT

现在我已经收集了大量论文信息。让我再获取几篇特别关键论文的更多细节。

> AGENT

现在让我搜索更多专门关于 SSM/线性注意力推测解码 verify 阶段的核心论文。

> AGENT

arXiv ID 没有对上正确的论文。让我查找正确的 GLA 和 Lightning Attention 论文 ID。

> AGENT

现在让我获取一些原始 EAGLE 论文和关键的系统实现论文。

> AGENT

现在我已经收集了足够的信息来撰写一份全面的调研报告。让我最后补充几篇特别关键的论文。

> AGENT

现在让我获取更多论文详情，包括一些更早期的关键奠基工作。

> AGENT

让我再搜索几个重要方向的关键论文。

> AGENT

非常好，我现在对代码库中的 GLA 状态管理有了清晰的理解。让我再搜索一些关键论文。

> AGENT

项目内已有一份详尽的调查文档。让我继续获取尚未覆盖的论文的详细信息。

> AGENT

通用搜索词结果太杂。让我搜索一些我知道存在的关键论文。

> AGENT

现在让我获取更多关键的最新论文。

> AGENT

现在我已经收集了足够的论文数据。让我再获取几篇重要的缺失论文，然后整理完整报告。

> AGENT

发现了一篇非常重要的论文 Cactus（Constrained Acceptance Speculative Sampling）。让我获取更多细节。

> AGENT

非常好，已经获取了 SpecMamba 的核心内容。现在让我获取 Mamba Drafters 的完整摘要和更多论文。

> AGENT

现在让我再搜索一些更特定方向的论文，特别是关于量化模型和分布匹配的。

> AGENT

我现在已经收集了足够全面的信息。以下是完整的调研报告。 --- # 推测解码 Verify 阶段前沿创新调研报告（2025-2026） ## 方向一：Tree Verification 创新 ### 1. Traversal Verification（叶到根验证） - **论文**：Traversal Verification for Speculative Tree Decoding - **arXiv**：2505.12398（2025年5月） - **核心算法**：颠覆传统 top-down 逐层验证，改为 **leaf-to-user_4813494d 遍历**。对每个叶节点，验证从该节点到根的完整 token 序列（而非单个 token），保留那些"父节点被拒但子序列仍有效"的路径。关键洞察：传统验证中一旦父节点被拒则丢弃整棵子树，但子节点序列的联合概率可能与 target 分布一致。 - **与 EAGLE 的关键区别**：EAGLE 采用 top-down 逐层 rejection sampling，父节点失败则整棵子树作废；Traversal Verification 保留被传统方法过早丢弃的有效子序列。 - **理论保证**：证明遍历验证输出的概率分布与 target model 完全一致（lossless）。 - **实验数据**：在多个 LLM 和任务上一致提升 acceptance length 和 throughput。 - **是否需要重新训练**：否，纯验证算法改动。 ### 2. Dynamic Delayed Tree Expansion（延迟树扩展） - **论文**：Dynamic Delayed Tree Expansion For Improved Multi-Path Speculative Decoding - **arXiv**：2602.16994（2026年2月） - **核心算法**：系统评估了 Traversal Verification vs OT-based（SpecInfer）等验证策略，发现 Traversal Verification 全面优于 OT 方法。关键洞察：OT 方法在树根附近获得高多 token 接受率，但多 token 收益在树深处更关键（draft-target 分布在深层更发散）。因此提出 **delayed tree expansion**：先 draft 一段单路径，延迟 i.i.d. 分支点。还开发了 **动态神经选择器**（neural selector），从 draft/target 特征估计 OT 验证的 block efficiency，动态决定是否展开。 - **与 EAGLE 的关键区别**：EAGLE 的树结构固定（static tree 或基于概率的动态 top-k）；delayed expansion 推迟分支，让单路径更深后再展开。 - **实验数据**：OT-based 方法（SpecInfer）配合 neural selector 首次超越 Traversal Verification，平均吞吐量高 5%。 - **是否需要重新训练**：neural selector 需要轻量训练；delayed expansion 本身不需要。 ### 3. C2T（Classifier-Based Tree Construction） - **论文**：C2T: A Classifier-Based Tree Construction Method in Speculative Decoding - **arXiv**：2502.13652（2025年2月） - **核心算法**：训练一个轻量 **classifier**，输入特征超越传统联合概率（加入额外特征变量），输出每个 draft token 的 confidence score，据此决定是否纳入候选树。本质是用分类器做 tree pruning。 - **与 EAGLE 的关键区别**：EAGLE-2/3 用 draft model 的 top-k 概率做树结构选择；C2T 用专门训练的分类器做更精准的剪枝。 - **实验数据**：比 EAGLE-2 减少 25% 候选 token 数，同时维持或提升 acceptance length。 - **是否需要重新训练**：是，需要训练 classifier（轻量）。 ### 4. GOOSE（Anisotropic Speculation Trees） - **论文**：Goose: Anisotropic Speculation Trees for Training-Free Speculative Decoding - **arXiv**：2604.02047（2026年4月） - **核心算法**：观察到两种 training-free token 来源（n-gram 匹配 vs 统计预测）的接受率差距巨大（中位数 6x，范围 2-18x）。**核心定理**：当存在质量差距时，最优树是**各向异性的**——高接受率 token 形成深链（spine），低接受率 token 作为宽分支。构建自适应 **spine tree**：深层链由高接受率的 context-matched token 组成，每个节点挂宽分支作为备选。 - **与 EAGLE 的关键区别**：EAGLE 的树是平衡/均匀的；GOOSE 打破深度限制，构建不对称的 spine tree。 - **实验数据**：5 个 LLM（7B-33B）5 个 benchmark 上 1.9-4.3x lossless speedup，比 balanced-tree baseline 提升 12-33%。 - **是否需要重新训练**：否，training-free。 ### 5. Hierarchical Verification Tree（HVT） - **论文**：Hierarchical Verification of Speculative Beams for Accelerating LLM Inference - **arXiv**：2508.03726（2025年8月） - **核心算法**：将 spec beam decoding的验证重构为层次化结构——优先验证高似然的 draft，**提前剪枝**次优候选。开发形式化的 verification-pruning 算法保证正确性。 - **与 EAGLE 的关键区别**：EAGLE 扁平验证所有候选；HVT 按似然排序，分层剪枝，减少无效验证计算。 - **实验数据**：在多数据集和模型上一致优于现有 spec decoding 方案，显著减少推理时间和能耗。 - **是否需要重新训练**：否。 ### 6. SAGE（Entropy-Guided Adaptive Tree） - **论文**：SAGE: Accelerating Vision-Language Models via Entropy-Guided Adaptive Speculative Decoding - **arXiv**：2602.00523（2026年2月） - **核心算法**：利用输出 **entropy** 作为自然置信度指标（具有跨解码步骤的强时间相关性）。高置信时构建 deep-narrow 树（最大化推测深度），低置信时构建 shallow-wide 树（多样化探索）。 - **与 EAGLE 的关键区别**：EAGLE 树结构静态或仅基于 draft 概率；SAGE 基于实时 entropy 动态调整树的深宽比。 - **实验数据**：LLaVA-OneVision-72B 达 3.36x speedup，Qwen2.5-VL-72B 达 3.18x。 - **是否需要重新训练**：否。 ### 7. OPT-Tree / Sequoia（动态规划最优树） - **论文**：OPT-Tree（2406.17276, 2024年6月）；Sequoia（2402.12374, 2024年2月） - **核心算法**：OPT-Tree 搜索最大化 acceptance length 期望的最优树结构；Sequoia 用动态规划找最优树 + 硬件感知树优化器。 - **与 EAGLE 的关键区别**：数学最优树结构 vs 启发式固定结构。 - **是否需要重新训练**：否。 --- ## 方向二：Acceptance Rate 优化算法（只改接受规则） ### 1. MARS：Margin-Aware Speculative Verification - **论文**：MARS: Unleashing the Power of Speculative Decoding via Margin-Aware Verification - **arXiv**：2601.15498（2026年1月） - **核心算法**：当 target model 对 top candidates 只有 **weak preference**（低 margin）时，严格拒绝 runner-up tokens 的信息增益可忽略，但 rollback 代价巨大。MARS 从 target logits 直接测量 **decision stability**（决策稳定性），仅在严格验证收益微小时放宽拒绝。形式化：若 `max(p_target) - […]

> AGENT

现在我已经收集了大量关键论文的详细信息。让我再搜索几个关键遗漏的论文，然后整理完整的调研报告。

> AGENT

现在让我获取最后几篇重要的论文，并整理已有信息。

> AGENT

现在我已经收集了足够全面的论文数据。让我整理成结构化的调研报告。 --- # EAGLE 推测解码 Verify 机制深度文献调研报告 ## 一、EAGLE 系列 Verify 机制演进 ### 1. EAGLE-1 (ICML 2024, arXiv:2401.15077) - **核心**：Feature-level autoregression，在 second-to-top-layer 特征空间做自回归，采样 feature 而非 argmax - **Verify**：标准 top-down greedy token-level rejection sampling，固定 25 节点静态 draft tree - **局限**：静态树假设 acceptance rate 仅与位置有关；feature prediction 约束限制了 scaling ### 2. EAGLE-2 (EMNLP 2024, arXiv:2406.16858) - **核心改进**：Context-aware 动态 draft tree - **关键洞察**：draft model 是 well-calibrated 的——draft 的 confidence score 近似 acceptance rate - **Verify**：仍是 top-down rejection sampling，但树结构根据 confidence 动态调整 - **效果**：3.05x-4.26x 加速，比 EAGLE-1 快 20%-40% ### 3. EAGLE-3 (NeurIPS 2025, arXiv:2503.01840) - **核心改进**：放弃 feature prediction，改为 direct token prediction；三层特征融合（低/中/高层语义）；Training-Time Test (TTT) 模拟推理时多步自回归 - **Verify**：仍用 top-down rejection sampling + tree attention - **效果**：SGLang + H100 + LLaMA-3.1-8B 上 2.36x 加速；bs=64 时 1.38x（vs EAGLE-1 的 0.99x 负加速） - **Scaling law**：8x 数据 → 1.4x 加速 --- ## 二、Verify 机制改进变体（按策略分类） ### A. 验证方向改进：Bottom-Up / Traversal **1. Traversal Verification** (NeurIPS 2025, arXiv:2505.12398) - **核心算法**：验证方向从 top-down 改为 bottom-up（叶到根），采用序列级接受概率而非逐 token 接受概率 - **关键区别**：传统 top-down 中父节点拒绝则所有子节点丢弃；Traversal 中父节点只在所有子节点均被拒绝后才验证，子节点验证机会不被过早剥夺 - **序列级补偿**：`min(r(X1)*r(X3), 1)` vs 传统 `min(r(X1),1)*min(r(X3),1)`，允许跨步概率补偿 - **数值示例**：`r(X1)=0.5, r(X3)=4/3` 时，Traversal P(accept)=0.667 vs 传统 0.5 - **实验数据**：EAGLE Sparse Tree 上 acceptance length 4.49→4.60 (+2.4%)；温度越高优势越明显 - **实现**：纯算法层改动，与 FlashInfer 兼容，不需要修改 CUDA kernel **2. Hierarchical Speculative Decoding (HSD)** (arXiv:2601.05724, 2026) - **核心**：Provable lossless 序列级验证，通过平衡 excess 和 deficient probability mass 克服联合不可解性 - **效果**：在多个模型和 benchmark 上一致提升 acceptance rate **3. Hierarchical Verification Tree (HVT)** (arXiv:2508.03726, 2025) - **核心**：对 speculative beams 做层次化验证，优先验证高似然 draft，及早剪枝次优候选 - **效果**：无需重训练/架构修改即可集成；多个数据集上一致优于现有方法 ### B. 放松验证严格性 **4. MARS: Margin-Aware Speculative Verification** (ICLR 2026, arXiv:2601.15498) - **核心洞察**：现代 LLM 在 low-margin 状态（top-1 和 top-2 概率接近）下，拒绝 runner-up token 的信息增益可忽略但 rollback 成本高 - **算法**：计算 target top-1 和 top-2 概率之差 (margin)；margin 大时严格验证；margin 小时放松接受 draft token - **特性**：训练免费；域无关；与任何 target-coupled spec decode 兼容；8B-235B 一致提速 **5. Fuzzy Speculative Decoding (FSD)** (ACL Findings 2025, arXiv:2502.20704) - **算法**：用 target 和 draft 分布的散度 (KL/JS/TV) 决定是否接受，阈值可调 - **效果**：5+ tok/s 加速换约 2% absolute accuracy 下降；调参可完全匹配 SD accuracy - **Reduced FSD 变体**：先标准验证，rejected token 再做 fuzzy check **6. DIVERSED: Dynamic Ensemble Verification** (AISTATS 2026, arXiv:2604.07622) - **算法**：验证目标替换为 draft 和 target 分布的加权混合：`nu_t(x) = alpha_t * p(x) + (1-alpha_t) * q(x)` - **alpha_t** 由轻量级神经网络学习（单层 FC + sigmoid）；Static Ensemble 变体固定 alpha，训练免费 - **理论基础**：提供理论证明保证生成质量 **7. Calibrated Speculative Decoding (CSD)** (arXiv:2604.13634, 2026) - **核心**："Frequency-Guided Candidate Selection + Probability-Guarded Acceptance" - **两个模块**：Online Correction Memory（聚合历史拒绝模式做 rescue candidate）；Semantic Consistency Gating（用概率比代替精确 token 匹配做验证） - **效果**：峰值 2.33x throughput 加速 **8. Cactus: Constrained Acceptance Speculative Sampling** (arXiv:2604.04987, 2026) - **核心**：将 speculative sampling 形式化为约束优化问题 - **效果**：保证与 verifier 分布的可控偏离，同时提升 acceptance rate **9. Think Before You Accept: Reflective Verification** (arXiv:2505.18629, 2025) - **核心**：利用 LLM 自身的反思能力做语义级验证 - **方法**：prompt-based probing 获取原始和 reflective 输出，并行语义评估 […]

> AGENT

现在让我查看一下已有的 EAGLE 推测解码实现代码，了解当前验证算法的具体实现，以便更好地将调研结果与项目关联。

> AGENT

现在我已经收集了足够的文献信息。让我最后搜索一两篇关键遗漏的论文，然后整理完整报告。

> AGENT

很好，现在我有了足够的信息来整理完整的调研报告。让我查看 `threshold_single` 和 `threshold_acc` 的语义。

> AGENT

我已经收集了足够的文献数据。现在让我整合所有发现，形成完整的调研报告。 --- # 线性注意力 / SSM 混合架构推测解码验证（Verify）阶段：挑战与创新方案调研报告 ## 一、核心挑战总览 当 target model 使用线性注意力（GLA/Lightning Attention）或 SSM（Mamba）时，speculative decoding 的 verify 阶段面临 Transformer 所没有的三大特殊挑战： 1. **隐藏状态回溯困难（Hidden State Backtracking）**：SSM/线性注意力的递推更新 `h_t = f(h_{t-1}, x_t)` 丢弃了之前的 hidden state。当 draft token 被拒绝时，必须回滚到最后一个被接受的 token 的状态，但该状态已不可逆地被覆盖。 2. **树形并行验证不兼容（Tree Verification Incompatibility）**：标准 Transformer verify 时可以用 tree attention 并行验证多条 draft 路径。但 SSM 层必须**按 token 顺序串行递推**，无法像 attention 那样对多条候选路径并行计算。 3. **混合架构的状态不一致性**：当模型混合 standard attention + SSM/线性注意力层时，verify 阶段需要同时管理 KV cache（attention 层）和 recurrent state（SSM/GLA 层），两者在 draft/verify 过程中的快照/恢复策略完全不同。 --- ## 二、逐方向论文详析 ### 方向 1：SSM/Mamba + Speculative Decoding #### 论文 1：SpecMamba: Accelerating Mamba Inference on FPGA with Speculative Decoding - **arXiv ID**: 2509.19873 (2025) - **核心算法 -- Memory-Aware Hybrid Backtracking**： - **Plan I（存全部状态）**：将所有 draft token 的 hidden state h_1~h_4 存到 off-chip 内存。优点：load 时可与 weight transfer overlap，draft 阶段零额外延迟。缺点：target model 并行 verify 时需要存多个 hidden state，通信开销过大。 - **Plan II（缓存轻量 activation 重算）**：仅缓存 SSM 的中间激活 (A, B, Delta, X)，需要时重新计算 hidden state。优点：target verify 阶段因 linear layer 只需执行一次而 SSM 串行递推时，重算避免了大量存储。缺点：draft 阶段引入冗余计算。 - **Hybrid 策略**：draft model 用 Plan I（off-chip 存储 hidden state），target model 用 Plan II（on-chip 缓存 activation）。这样 draft 阶段零额外延迟，target verify 阶段通信开销低。 - **核心算法 -- FIFO-based Tree Verification with Tiling**： - 利用 SSM 的 token 间依赖关系，按广度优先遍历（BFS）顺序验证 tree。一旦某节点的所有子节点验证完毕，该节点的状态即可驱逐（evict），从而将 SSM tree verify 的内存需求从 O(所有节点) 降至 O(活跃路径)。 - **与 EAGLE verify 的关键区别**：EAGLE 用 tree attention 并行验证多条路径（一次 forward），SpecMamba 的 SSM 层**必须串行递推**，无法并行化 verify 的 SSM 部分，只能用 FIFO + eviction 策略优化访存。 - **实验数据**：FPGA 上 2.27x 加速 vs GPU baseline，5.41x 能效提升。 - **是否需要训练**：否，纯系统/算法层面优化。 #### 论文 2：Mamba Drafters for Speculative Decoding - **arXiv ID**: 2506.01206 (2025, EMNLP 2025) - **核心算法**：用 Mamba SSM 作为**外部 drafter**（而非 self-speculation），利用 SSM 的线性复杂度和常数大小 recurrent state 实现： - **常数内存 draft**：Mamba 的 recurrent state 大小固定，不随序列长度增长。对比 Transformer drafter 的 KV cache 随输入长度线性增长。 - **高吞吐 draft**：Mamba drafter 比 Transformer drafter 快得多，因为无需维护 KV cache。 - **Tree-drafting 算法**：扩展了 Mamba 的 tree 搜索能力，生成更优的候选序列以提高 accept length。 - **与 EAGLE verify 的关键区别**：Mamba 作为 drafter 而非 target。target 仍是标准 Transformer，所以 verify 阶段**不需要处理 SSM state 回滚**。这正好是 MiniCPM-SALA 的**反方向**问题——我们是 target 有 SSM 层。 - **实验数据**：130M Mamba drafter 在 Llama-2-70B target 上达到 2.55x 加速；acceptance rate 与 Transformer drafter 相当但吞吐更高。 - **是否需要训练**：需要训练 Mamba drafter（但只需训练 drafter，不需要改 target）。 #### 论文 3：MambaByte: Token-free Selective State Space Model - **arXiv ID**: 2401.13660 (2024) - **核心算法**：MambaByte 适配了 speculative decoding 用于 byte-level 模型，采用"tokenized drafting + byte-level verification"策略。利用 Mamba 的固定大小状态实现 2.6x 推理加速。 - **与 EAGLE verify 的关键区别**：同样是用 SSM 作为 draft model，verify 在 target 端。 - **是否需要训练**：需要训练 MambaByte 模型。 #### 论文 4：DYNAMAX: Dynamic Computing for Transformers and Mamba Based Architectures - **arXiv ID**: 2504.20922 (2025) - **核心算法**：将 Early Exit (EE) 机制集成到 Mamba 架构，并利用 Mamba 作为 EE 分类器。不是 speculative decoding，但提出了 Mamba 在 decoder-only 架构中的动态计算方案。 - […]

> AGENT

现在我已经掌握了足够的信息，可以撰写完整的调研报告了。 --- # 推测解码验证算法深度调研报告 ## 一、背景：标准 Speculative Sampling 回顾 **Leviathan et al. 2023 (arXiv:2302.01318)** 和 **Chen et al. 2023 (arXiv:2305.09781)** 提出的标准接受规则： - **逐 token 独立验证**：对 draft token x_i，接受概率 = min(1, p_target(x_i) / p_draft(x_i)) - **拒绝后残差采样**：从 max(0, p_target - p_draft) 分布采样修正 token - **保证**：输出分布与 target 模型严格一致（lossless） - **核心局限**：(1) 逐 token 验证不是最优的（忽略 token 间联合概率）；(2) draft-target 任何分歧都导致截断，acceptance rate 上限受限于分布匹配质量 **当前项目的实现**：`demo-sala/sglang/` 中使用 `tree_speculative_sampling_target_only`（sgl_kernel CUDA kernel），支持 `threshold_single` 和 `threshold_acc` 两个放松参数（默认 1.0 = 标准 lossless），即已有放松接受的基础设施。 --- ## 二、Distribution Matching Verify ### 2.1 LK Losses: Direct Acceptance Rate Optimization (arXiv:2602.23881, 2026.02) - **核心发现**：标准训练用 KL 散度作为 proxy 目标，但小 draft 模型容量有限，收敛到 suboptimal 解时，最小化 KL 不等于最大化 acceptance rate - **算法**：提出 LK（Log-KL）损失函数族，直接优化 acceptance rate： - 标准接受率 = E_x~p_target[min(1, p_draft(x)/p_target(x))]，这本身不可微 - LK 损失将其转化为可微上界/下界 - 具体形式：L_LK = -E_x~p_target[log(min(1, p_draft(x)/p_target(x)))] 的变体 - **与标准 SD 区别**：不改验证算法，而是改 draft 训练目标，使 draft 分布在 acceptance rate 意义上更匹配 target - **需要训练**：是（替代标准 KL 蒸馏） - **实验**：4 种 draft 架构、6 个 target 模型（8B-70B），acceptance rate 提升 5-15% ### 2.2 Revisiting Judge Decoding via Training-Free Distributional Divergence (arXiv:2601.04766, 2026.01) - **核心发现**：Judge Decoding 中通过监督学习获得的 "criticality" 分数，本质上与 KL 散度编码相同信息 - **算法**： - 理论证明：线性 judge 的打分 = f(KL(p_target || p_draft))，依赖相同的 logit 原语 - 提出 training-free 验证机制：直接用 KL 散度作为 token "criticality" 度量 - 高 KL = 高 criticality = 严格验证；低 KL = 低 criticality = 放松验证 - **与标准 SD 区别**：引入 token-level criticality 分层验证，而非统一严格/放松 - **需要训练**：否 - **实验**：reasoning 和 coding benchmark 上匹配或超越复杂训练 judge ### 2.3 AdaSPEC: Selective Knowledge Distillation (arXiv:2510.19779, 2025.10) - **算法**：选择性知识蒸馏，按 context 动态调整 KD 强度 - **与本项目相关度**：中等（改训练而非验证） --- ## 三、Relaxed / Approximate Verify（最核心突破方向） ### 3.1 DIVERSED: Dynamic Ensemble Verification (arXiv:2604.07622, 2026.04) -- **最高相关性** - **核心算法**：将验证分布从 p_target 放松为 p_verify = alpha * p_target + (1-alpha) * p_draft 的加权集成 - alpha 是 task-dependent 和 context-dependent 的动态权重 - 通过轻量级 ensemble-based verifier 学习 alpha - **接受规则**：将标准 min(1, p_target(x)/p_draft(x)) 替换为 min(1, p_verify(x)/p_draft(x)) - 由于 p_verify 包含 p_draft 成分，接受概率天然更高 - **理论保证**：证明 relaxed 分布与 target 分布的偏差有界（TV distance 上界） - **与标准 SD 区别**：验证器不是纯粹 target，而是 draft-target 的混合分布 - **需要训练**：是（学习 alpha，但开销小） - **实验**：比标准 SD 显著提升推理效率 - **代码**：https://github.com/comeusr/diversed ### 3.2 Cactus: Constrained Acceptance Speculative Sampling (arXiv:2604.04987, 2026.04) -- **最高相关性** - **核心创新**：从约束优化视角形式化 speculative sampling - 目标：最大化 acceptance rate - 约束：输出分布与 target 的散度 <= epsilon - **算法**： - 标准 SpS 是 epsilon=0 的特例 - 允许受控的分布偏移（类似 temperature/top-k 调整） - 解约束优化得到最优接受规则 - **接受规则公式**（推导自 KKT 条件）： - 接受概率 = min(1, p_target(x)/p_draft(x) * g(x))，其中 g(x) 是拉格朗日乘子的函数 - g(x) 的设计保证 TV(p_output, p_target) <= epsilon - **与标准 SD 区别**：提供 principled 的 epsilon-放松框架，不是 heuristic - **需要训练**：否 - **适用条件**：任何 draft-target 配对，epsilon 是用户可调 knob ### 3.3 SMC-SD: Sequential Monte Carlo Speculative Decoding (arXiv:2604.15672, 2026.04) -- **高相关性** - **核心创新**：用 importance-weighted […]

> DEVELOPER

你是推测解码中 SSM/线性注意力 state 管理的专家调研员。请同时使用 Tavily 搜索和 arxiv MCP server 工具进行深度文献检索。 **核心问题**：当 target model 包含 SSM/线性注意力（Mamba/GLA/RetNet）层时，speculative decoding verify 阶段的 state 回滚/快照/恢复有哪些方案？这是文献中的空白区域，需要极深入的挖掘。 **调研方法**： 1. 先用 arxiv MCP server 的 search_papers 和 semantic_search 搜索以下关键词 2. 再用 Tavily 补充搜索博客/代码/讨论等非论文资源 3. 对找到的关键论文，用 download_paper + read_paper 获取完整算法细节 **arxiv 搜索关键词**： - "speculative decoding mamba state" - "speculative decoding linear attention verification" - "SSM state rollback speculative" - "recurrent state checkpoint speculative decoding" - "Mamba inference speculative" - "gated linear attention speculative" - "hybrid attention speculative decoding state" - "MiniCPM speculative decoding" - "state space model verification speculative" - "temporal state management speculative decoding" **Tavily 搜索**： - "Mamba speculative decoding state management 2025 2026" - "GLA linear attention speculative decoding verify state" - "speculative decoding hybrid attention state rollback" - "SpecMamba SSM verification algorithm" - "STree SSM tree verification algorithm details" **特别关注**： 1. SpecMamba (arXiv:2509.19873) 的完整算法细节——用 download_paper 获取 2. STree (arXiv:2505.14969) 的完整算法——用 download_paper 获取 3. 任何涉及 Mamba/Jamba/Zamba + speculative decoding 的论文 4. 任何涉及 GLA/Lightning Attention + speculative decoding 的论文 5. FLA (Flash Linear Attention) 库中的 speculative decoding 相关实现 对每篇论文提供：完整标题、arXiv ID、核心算法（公式级别）、SSM/线性注意力 state 如何在 verify 时管理、实验数据。

> AGENT

我将系统地进行这个深度调研。先并行启动 arxiv 搜索和 Tavily 搜索，然后对关键论文下载全文细读。 **第一轮：arxiv 关键词搜索（并行）**

> DEVELOPER

你是推测解码 verification 算法的专家调研员。请同时使用 Tavily 搜索和 arxiv MCP server 工具进行深度文献检索。 **核心问题**：Block Verification 和 Sequence-Level Verification 的具体算法细节是什么？这是被证明"逐 token 独立验证不是最优的"之后的突破方向，需要精确的数学公式和实现细节。 **调研方法**： 1. 用 arxiv MCP server 的 search_papers 搜索 2. 对关键论文用 download_paper + read_paper 获取完整内容 3. 用 Tavily 补充搜索代码实现和博客解读 **arxiv 搜索关键词**： - "block verification speculative decoding" - "sequence level acceptance speculative decoding" - "joint verification speculative decoding" - "optimal transport speculative decoding verification" - "SpecInfer tree verification algorithm" - "multi-token verification speculative decoding" **必须深入阅读的论文**（用 download_paper 获取完整内容）： 1. Block Verification (arXiv:2403.10444) — 证明逐 token 非最优的奠基工作 2. Greedy Multi-Path Block Verification (arXiv:2602.16961) — 多路径扩展 3. Traversal Verification (arXiv:2505.12398) — 叶到根验证的完整伪代码 4. SpecInfer (arXiv:2305.09781 或相关) — OT-based 验证的完整算法 5. Global Resolution (arXiv:2511.15898) — 多 draft 最优验证 **需要提取的具体信息**： - 每篇论文的完整验证算法伪代码 - 接受概率的精确数学公式 - 理论最优性证明的核心思路 - 与标准 rejection sampling 的数学关系 - 计算复杂度分析 - 在 tree 结构下的具体执行流程 - 如何处理 rejection 后的修正采样 **Tavily 补充搜索**： - "speculative decoding block verification implementation details 2025" - "speculative decoding sequence level acceptance formula" - "SpecInfer tree verification algorithm pseudocode"

> AGENT

我将系统性地搜索和阅读推测解码验证算法的关键论文。先并行启动 arxiv 搜索和 Tavily 搜索。

> DEVELOPER

你是推测解码验证算法的专家调研员。请同时使用 Tavily 搜索和 arxiv MCP server 工具进行深度文献检索。 **核心问题**：放松验证（relaxed verification）的具体算法细节。包括 Cactus 的约束优化框架、SMC-SD 的 importance resampling、DIVERSED 的 ensemble 混合验证。需要精确的数学公式和实现路径。 **调研方法**： 1. 用 arxiv MCP server 搜索和下载论文 2. 用 Tavily 补充搜索代码和讨论 **必须深入阅读的论文**（用 download_paper + read_paper 获取）： 1. Cactus (arXiv:2604.04987) — 约束优化形式的接受规则，精确的 KKT 推导 2. SMC-SD (arXiv:2604.15672) — Sequential Monte Carlo 替代 rejection sampling 3. DIVERSED (arXiv:2604.07622) — Ensemble 验证的完整算法 4. MARS (arXiv:2601.15498) — Margin-aware 验证的完整公式 5. LK Losses (arXiv:2602.23881) — 直接优化 acceptance rate 的损失函数 **arxiv 搜索关键词**： - "relaxed speculative decoding verification 2025 2026" - "constrained acceptance speculative sampling" - "sequential monte carlo speculative decoding" - "margin aware verification speculative" - "acceptance rate optimization speculative decoding" - "lossy speculative decoding controlled divergence" **需要提取的具体信息**： - Cactus 的约束优化形式化（目标函数、约束条件、KKT 条件推导、接受规则 g(x) 的显式形式） - SMC-SD 的 particle filter 流程（初始化、权重更新、resampling 策略、近似误差界） - DIVERSED 的 alpha 学习算法（训练目标、网络结构、static vs dynamic 的差异） - MARS 的 margin 阈值选择（理论推导、自适应设置） - LK Losses 的损失函数族定义（上界/下界形式、与 acceptance rate 的数学关系） - 每种方法的输出分布偏差的定量界（TV distance / KL bound） - 与标准 speculative sampling (Leviathan 2023) 的公式级对比 - 代码实现路径（是否开源、关键代码行数估计） **Tavily 补充搜索**： - "Cactus constrained acceptance speculative decoding code implementation" - "SMC-SD sequential monte carlo speculative decoding algorithm" - "DIVERSED dynamic ensemble verification open source code"

> AGENT

我将同时启动 arxiv 搜索和 Tavily 搜索，并行进行文献检索。

> TOOL

[Request interrupted by user for tool use]

> TOOL

[Request interrupted by user for tool use]

> TOOL

[Request interrupted by user]

> DEVELOPER

你是推测解码与线性注意力混合架构的学术调研专家。你的任务是补充之前调查的文献空白。 **已知空白**：目前没有论文专门解决"混合 standard attention + GLA/SSM 架构 + 外部 drafter 的 speculative decoding verify"问题。现有工作要么全 SSM target，要么全 Transformer target。 **调研方向**（请用 mcp__tavily__tavily_search 和 arxiv MCP server 工具交替搜索）： 1. **SSM state checkpoint/rollback 最新工作** - 搜索 "SSM state checkpoint speculative decoding 2025 2026" - 搜索 "Mamba hidden state rollback inference" - 搜索 "recurrent model state management inference optimization 2026" - 在 arxiv 搜索 "speculative decoding Mamba state" 2. **Hybrid model inference optimization** - 搜索 "hybrid Mamba transformer inference optimization 2025 2026" - 搜索 "mixed attention model speculative decoding state" - 搜索 "linear attention decode state management speculative" - 在 arxiv 搜索 "hybrid attention speculative decoding verify" 3. **KV cache + recurrent state 联合管理** - 搜索 "KV cache recurrent state joint management speculative decoding" - 搜索 "speculative decoding verify state snapshot restore" - 搜索 "tree verification recurrent model state management" 4. **GLA / Lightning Attention 特有问题** - 搜索 "gated linear attention verify speculative decoding" - 搜索 "GLA temporal state rollback" - 搜索 "lightning attention inference speculative" - 在 arxiv 搜索 "linear attention speculative decoding verification" 5. **MiniCPM / OpenBMB 相关最新工作** - 搜索 "MiniCPM speculative decoding 2025 2026" - 搜索 "OpenBMB MiniCPM4 inference acceleration" - 搜索 "InfLLM speculative decoding" - 在 arxiv 搜索 "MiniCPM4 EAGLE speculative" 对每篇论文记录：完整标题、arXiv ID、核心算法、与 MiniCPM-SALA 混合架构 verify 的关系。

> AGENT

我将系统性地搜索这五个方向的文献。让我先并行发起第一批搜索。

> DEVELOPER

你是推测解码验证算法的实现细节专家。之前的调查发现了三篇最重要的接受规则创新论文（Cactus、MARS、SMC-SD），现在需要深挖它们的具体实现细节和实验数据。 **请用 mcp__tavily__tavily_search 和 arxiv MCP server 工具搜索**： 1. **Cactus（arXiv:2604.04987）实现细节** - 搜索 "Cactus constrained acceptance speculative sampling implementation" - 搜索 "Cactus speculative decoding epsilon constrained divergence" - 在 arxiv 搜索 "2604.04987" - 重点：epsilon 参数如何设置？TV distance 上界的具体公式？对 tree verify 是否适用？ 2. **MARS（arXiv:2601.15498）实现细节** - 搜索 "MARS margin aware speculative verification algorithm details" - 搜索 "MARS speculative decoding implementation margin threshold" - 在 arxiv 搜索 "2601.15498" - 重点：margin_threshold 的具体计算方式？对 greedy verify vs sampling verify 分别怎么改？在 tree verify 中如何应用？ 3. **SMC-SD（arXiv:2604.15672）实现细节** - 搜索 "SMC-SD sequential Monte Carlo speculative decoding implementation" - 搜索 "particle resampling speculative decoding inference" - 在 arxiv 搜索 "2604.15672" - 重点：粒子数 N 如何选择？与 tree verify 的兼容性？memory overhead？ 4. **Block Verification 与 tree verify 的结合** - 搜索 "block verification tree speculative decoding combination" - 搜索 "joint token verification tree attention speculative" - 重点：BV 如何在 EAGLE 的 tree attention 框架中实现？需要改 FlashInfer kernel 吗？ 5. **放松验证在量化模型上的效果** - 搜索 "relaxed verification quantized model speculative decoding" - 搜索 "NVFP4 speculative decoding acceptance rate" - 搜索 "FP4 quantization speculative decoding verify" - 重点：量化模型的 target logits 精度对 margin/KL/divergence 计算的影响 6. **这些方法的组合兼容性** - 搜索 "combining speculative decoding verification methods 2025 2026" - 搜索 "MARS traversal verification combination" - 重点：MARS + Traversal Verification 是否可叠加？Cactus + Block Verification？ 对每篇论文，请尽量找到具体的算法伪代码、公式、超参数设置、实验对比数据。

> AGENT

我来系统地搜索这些推测解码验证算法的实现细节。让我并行发起多组搜索。

> DEVELOPER

你是推测解码领域最新论文的追踪专家。之前的调查覆盖到 2026 年 4 月的工作，现在需要搜索 2026 年 4-5 月的最新论文。 **请用 mcp__tavily__tavily_search 和 arxiv MCP server 工具搜索**： 1. **2026 最新 speculative decoding 论文** - 搜索 "speculative decoding 2026 new method" (限制最近1个月) - 搜索 "speculative decoding April 2026 arxiv" - 搜索 "speculative decoding verification 2026 recent" - 在 arxiv 搜索 "speculative decoding 2026" - 在 arxiv 搜索 "speculative verification 2026" 2. **2026 最新 tree verify / acceptance rate** - 搜索 "tree verification speculative decoding 2026 new" - 搜索 "acceptance rate optimization speculative decoding 2026" - 搜索 "draft tree optimization 2026 arxiv" - 在 arxiv 搜索 "draft tree speculative 2026" 3. **2026 最新 SSM / Mamba inference** - 搜索 "Mamba inference acceleration 2026" - 搜索 "SSM speculative decoding 2026 new" - 搜索 "hybrid Mamba transformer inference 2026" - 在 arxiv 搜索 "Mamba speculative 2026" 4. **2026 最新 linear attention / GLA** - 搜索 "linear attention inference optimization 2026" - 搜索 "gated linear attention acceleration 2026" - 搜索 "recurrent attention speculative decoding 2026" - 在 arxiv 搜索 "linear attention speculative 2026" 5. **ICML / NeurIPS 2026 投稿** - 搜索 "ICML 2026 speculative decoding" - 搜索 "NeurIPS 2026 speculative decoding submission" - 在 arxiv 搜索 "speculative decoding ICML 2026" 6. **SOAR 竞赛 / LLM inference optimization 竞赛** - 搜索 "SOAR LLM inference competition 2026" - 搜索 "LLM inference optimization competition speculative decoding" - 搜索 "MiniCPM SALA optimization 2026" 对每篇论文记录：完整标题、arXiv ID、发表时间、核心创新、与 verify 机制的关系。

> AGENT

我将系统性地搜索 2026 年 4-5 月推测解码领域的最新论文。让我并行发起多个搜索。

> AGENT

很好，第一批搜索已经获得了大量关键信息。让我继续搜索剩余的方向。

> DEVELOPER

你是推测解码 verify 机制工程实践的调研专家。之前调查了大量学术论文，现在需要关注实际系统中的工程实现和部署经验。 **请用 mcp__tavily__tavily_search 和 arxiv MCP server 工具搜索**： 1. **SGLang speculative decoding 最新实现** - 搜索 "SGLang speculative decoding implementation 2026" - 搜索 "SGLang EAGLE verify optimization PR" - 搜索 "site:github.com sglang speculative decoding verify" - 重点：SGLang 的 tree verify 实现细节、FlashInfer tree attention 调用方式 2. **vLLM speculative decoding verify 实现** - 搜索 "vLLM speculative decoding verification implementation 2025 2026" - 搜索 "vLLM EAGLE verify acceptance optimization" - 重点：vLLM 与 SGLang 在 verify 实现上的差异 3. **FlashInfer tree attention 最新状态** - 搜索 "FlashInfer tree attention speculative decoding 2026" - 搜索 "flashinfer batch decode tree verify kernel" - 重点：tree attention kernel 对不同 tree shape 的支持、memory layout 4. **CUDA graph + speculative decoding 实践** - 搜索 "CUDA graph speculative decoding Blackwell 2026" - 搜索 "CUDA graph tree verify speculative decoding" - 搜索 "SM120 speculative decoding CUDA graph" - 重点：Blackwell 上 CUDA graph capture 的已知问题、workaround 5. **NVFP4 量化 + speculative decoding 实践** - 搜索 "NVFP4 speculative decoding verify accuracy" - 搜索 "weight only quantization speculative decoding logits quality" - 搜索 "FP4 GPTQ speculative decoding acceptance rate" - 重点：量化 target 的 logits 精度对 verify acceptance 的影响 6. **生产环境 spec decoding 调优经验** - 搜索 "speculative decoding production deployment tuning 2025 2026" - 搜索 "speculative decoding batch size tradeoff production" - 搜索 "speculative decoding latency throughput optimization serving" - 重点：实际部署中的 acceptance rate 波动、A/B 测试结果 对每项发现记录：来源（论文/GitHub issue/博客）、具体实现细节、与 MiniCPM-SALA 的适用性。

> AGENT

我将按照你的要求，分六个方向进行系统搜索。让我并行发起所有搜索请求。

> AGENT

继续搜索更多方向的论文。

> AGENT

好的，让我继续深入搜索更多具体细节，特别是论文的 HTML 全文、算法伪代码和实验数据。

> AGENT

非常好，发现了MiniCPM4的关键信息。让我继续搜索更多细节，特别是MiniCPM4论文的完整信息和arXiv ID，以及STree和Snakes & Ladders的更多细节。

> AGENT

现在继续搜索剩余的主题方向。

> AGENT

现在让我提取论文的详细内容，特别是算法伪代码和公式。

> AGENT

发现了非常重要的内容。让我继续搜索几个关键的缺失论文和信息。

> AGENT

现在搜索最后两个方向。

> AGENT

非常好，我已经收集到了大量关键信息。特别重要的发现是 vLLM 论坛上关于 Qwen3.5 混合线性注意力模型推测解码的精确问题--这正是 MiniCPM-SALA 面临的核心挑战。让我再做最后一轮搜索来补充几个关键论文的 arXiv ID。

> AGENT

现在让我搜索剩余的几个方向，以及获取一些论文的更详细信息。

> AGENT

现在让我查看项目中当前的 EAGLE worker 和 verify 实现，以便将搜索结果与项目实际情况关联。

> AGENT

现在让我搜索更多关于 Cactus 的核心公式、Block Verification 与 tree verify 的结合，以及量化模型上的效果。

> AGENT

现在我已经收集了足够的信息。让我查看项目中 verify 的关键实现。

> AGENT

现在我已经收集了充分的信息，可以给出完整的调研报告了。 --- ## 混合标准注意力 + GLA/SSM 架构 + 外部 drafter 推测解码验证：文献调研报告 ### 空白确认 经过系统性搜索，**确认不存在专门解决"混合 standard attention + GLA/SSM 架构 + 外部 drafter 的 speculative decoding verify"问题的论文**。现有工作覆盖了以下子问题，但没有一个在统一框架内解决 MiniCPM-SALA 所面对的全部挑战： 1. SSM/Mamba-only 的 state rollback 2. 纯 SSM 或纯 Transformer hybrid 的 tree verify 3. 混合模型的 prefix caching（KV cache + recurrent state 联合管理） 4. 混合模型的 MTP 内嵌式推测解码 但 **SSM state checkpoint/rollback + external drafter + standard attention KV cache 的联合 verify** 这一组合尚未被任何论文直接解决。 --- ### 方向 1：SSM State Checkpoint/Rollback **1. Snakes and Ladders: Accelerating SSM Inference with Speculative Decoding** - arXiv: 2402.00550（NeurIPS 2024 Workshop） - 作者: Yangchao Wu, Yonatan Dukler, Matthew Trager, Alessandro Achille, Wei Xia, Stefano Soatto (UCLA, AWS AI) - 核心算法: 两种 SSM state backtracking 方法： - **Activation Replay**: 缓存 SSM block 的输入激活，回溯时只重跑 state update kernel 到最后验证通过的 token - **Joint Attainment and Advancement**: 在验证当前 draft 的同时前进一步，恢复到最后验证通过的 token 的 SSM state - 与 MiniCPM-SALA 的关系: **直接相关但仅处理纯 SSM target**。Activation Replay 思路可借鉴到 GLA 层的 state 回退，但需要适配 GLA 的 gating 机制（S_t = G_t * S_{t-1} + k_t v_t^T），且未涉及 standard attention 层的 KV cache 联合回退。 **2. STree: Speculative Tree Decoding for Hybrid State-Space Models** - arXiv: 2505.14969（NeurIPS 2025） - 作者: Yangchao Wu 等 - 核心算法: 将 token tree 压平为单一序列 + tree mask，利用 SSM 状态转移矩阵的可加性，一次性前向计算 tree 上所有节点的输出，避免为每条路径重复展开 SSM。提出 custom tree scan kernel。 - 与 MiniCPM-SALA 的关系: **最接近的工作**。明确声称适用于"hybrid SSM+Transformer"架构，但论文中的 hybrid 是指 Mamba+Attention 层交替排列，target model 本身就是 SSM。它不处理 **外部 drafter** 的场景（如 EAGLE），而是假设 target model 自身是 SSM/hybrid，用 target 的 SSM 层做 verify。对 MiniCPM-SALA 的启示：tree mask + 累积状态转移矩阵的思路可用于 GLA 层的 tree verify，但需要解决 EAGLE drafter 产生的 draft token tree 与 GLA state 的交互问题。 **3. Speculative Speculative Decoding (Saguaro)** - arXiv: 2603.03251（ICLR 2026 Poster） - 作者: Tanishq Kumar, Tri Dao, Avner May - 核心算法: 异步推测解码——draft model 在 verification 进行时预测可能的验证结果并提前准备下一轮 speculation，消除 drafting 延迟。与 EAGLE-3 兼容。 - 与 MiniCPM-SALA 的关系: 不直接解决 SSM state 问题，但其异步流水线思路可减少 GLA state rollback 的开销窗口。 --- ### 方向 2：Hybrid Model Inference Optimization **4. SGLang Hybrid Models: MambaRadixCache + Speculative Decoding** - 来源: PyTorch Blog "Hybrid Models Meet SGLang: More than Full Attention" - 核心机制: - **双内存池设计**: Mamba pool + KV cache pool 独立管理 - **MambaRadixCache**: 混合 radix tree，分别管理 SSM state 和 KV cache 的 prefix 匹配 - **State Snapshotting**: 为每个 draft token 分配独立的 Mamba cache slot，解决 SSM state 不可逆问题 - **EAGLE-Tree with top-K > 1**: 支持树形 draft + 混合架构 - 与 MiniCPM-SALA 的关系: **最直接可借鉴的工程实现**。SGLang 已在 Qwen3-Next（Gated DeltaNet + Gated Attention 混合）上验证了 EAGLE tree verify + 混合架构的可行性。关键设计是"每个 draft token 独立 Mamba cache slot"，这正是解决 GLA state rollback 的实用方案。MiniCPM-SALA 的当前 SGLang fork 可参考此实现。 **5. Marconi: Prefix […]

> AGENT

现在让我获取更多关于 Cactus 核心公式和 "Speculative Decoding Meets Quantization" 的关键发现。

> AGENT

现在我已经收集了足够的信息。让我整理完整的调查报告。 --- ## 2026 年 4-5 月推测解码最新论文追踪报告 --- ### 一、2026 最新 Speculative Decoding 论文 **1. DDTree: Accelerating Speculative Decoding with Block Diffusion Draft Trees** - **arXiv ID**: 2604.12989 - **发表时间**: 2026-04-14 - **核心创新**: 从 block diffusion drafter (DFlash) 的单次前向传播中提取 per-position 边缘分布，构建 draft tree。使用 best-first heap 算法，在固定节点预算下可证明最优地最大化期望接受长度。Tree verification 使用 ancestor-only attention masking 在单次 target model 前向传播中完成。Lossless 保分布。 - **与 verify 机制关系**: 直接改进 tree verify——从 DFlash 只验证单条轨迹升级为验证整棵树，接受长度提升 35%-63%，峰值 8.22x 加速。**对当前项目影响极大**：DDTree+DFlash 组合已在 DGX Spark/RTX 3090 上被社区验证，是 EAGLE-3 的强力竞争者。 **2. HSD: Overcoming Joint Intractability with Lossless Hierarchical Speculative Decoding** - **arXiv ID**: (ICLR 2026 Oral, 具体编号待确认) - **发表时间**: ICLR 2026 (2026-04-25 oral) - **核心创新**: 解决 sequence-level verification 的"联合不可解性"问题，将 resampling 组织为层次结构，在分支间重新分配概率质量，使更多 token 被一次接受。理论证明 lossless，集成到 EAGLE-3 上获得 12% 性能提升。 - **与 verify 机制关系**: 直接改进 verify 步骤——从 token-wise/blockwise verification 到 hierarchical verification，比两者都优。 **3. Speculative Speculative Decoding (SSD / Saguaro)** - **arXiv ID**: (ICLR 2026 Poster) - **发表时间**: ICLR 2026 (2026-04-24 poster) - **核心创新**: 将 speculative decoding 自身的 draft 和 verify 阶段并行化。在 verify 进行时，draft model 预测 verify 结果并提前准备下一轮 speculation。若预测正确则省去 drafting 开销。实现 Saguaro 算法，比优化 SD baseline 快 2x，比 AR 快 5x。 - **与 verify 机制关系**: 从根本上消除 verify-draft 串行依赖，将 verify 和 next-draft 重叠。 **4. LTD: Learning To Draft - Adaptive Speculative Decoding with Reinforcement Learning** - **arXiv ID**: (ICLR 2026 Poster) - **发表时间**: ICLR 2026 (2026-04-25 poster) - **核心创新**: 将 draft-verify 周期建模为 RL 环境，训练两个 co-adaptive policies 动态协调 draft 和 verify 阶段。直接优化 throughput 而非代理指标（如 acceptance length），2.24x-4.32x 加速，比 EAGLE-3 优 36.4%。 - **与 verify 机制关系**: 动态调整 verify 时间分配，而非静态方案。 **5. HiSpec: Hierarchical Speculative Decoding for LLMs** - **arXiv ID**: (ICLR 2026 submission) - **核心创新**: 复用 higher intermediate layers 作为 lightweight verifiers 提前拒绝 draft tokens，减少 verification 瓶颈。Training-free，throughput 提升 1.28x-2.01x。 - **与 verify 机制关系**: 三层验证结构（draft → intermediate verifier → target），提前过滤低质 draft。 **6. ConFu: Contemplate the Future for Better Speculative Sampling** - **arXiv ID**: 2603.08899 (v3) - **核心创新**: 通过 contemplate tokens 和 soft prompts 让 draft model 获取 target model 的"未来信号"，动态 contemplate token 机制基于 MoE 架构。减少 rejection rate，提升 throughput。 - **与 verify 机制关系**: 间接改进——通过提升 draft 质量减少 verify 阶段的 rejection。 **7. RACER: Retrieval-Augmented Contextual Rapid Speculative Decoding** - **arXiv ID**: 2604.14885 - **核心创新**: Training-free，统一 retrieval-based 和 logits-based 信号。用 AC 自动机 + LRU 淘汰构建 n-gram retrieval tree，与 logits tree 融合。Plug-and-play。 - **与 verify 机制关系**: 通过丰富 draft 候选提升接受率，不改变 verify 机制本身。 **8. MARS: Margin-Aware Verification for Speculative Decoding** - **arXiv ID**: 2601.15498 (v2) - **核心创新**: Margin-aware verification——在 verify 时利用 margin 信息做更智能的接受/拒绝决策。 - **与 verify 机制关系**: 直接改进 verify 算法。 **9. DIVERSED: Relaxed Speculative Decoding via Dynamic Ensemble Verification** - **arXiv ID**: […]

> AGENT

现在让我获取 Cactus 论文的核心公式部分和 Traversal Verification 的内容。

> AGENT

我已经有了足够的上下文来撰写完整的调研报告。以下是系统性的总结。 --- ## 推测解码 Verify 机制工程实践调研报告 ### 一、SGLang Speculative Decoding 最新实现 **来源：SGLang GitHub Issue #22949/#23005/#23705、SGLang 官方文档、sgl-project/sglang 代码仓库** **1. SGLang 2026 Q2 Spec 解码路线图** SGLang 正式公布了 2026 Q2 推测解码开发路线图（Issue #23005），PoC 为 @Qiaolin-Yu 和 @hnyls2002。核心目标： - **通用推测算法抽象**：支持更多 spec 算法（当前支持 EAGLE/EAGLE3/DFLASH/STANDALONE/NGRAM） - **通用推测 graph 准备和初始化抽象** - **自适应推测配置**：根据不同请求和 batch size 动态调整参数 **2. SGLang Adaptive Speculative Decoding（已落地）** 这是与 MiniCPM-SALA 最直接相关的新特性。SGLang 已正式支持自适应推测解码（文档地址：`sgl-project.github.io/advanced_features/adaptive_speculative_decoding.html`）： - **EMA 策略**：每轮 verify 后读取每个请求的 accepted draft length，计算 batch 平均，用指数移动平均平滑 - **预建候选层**：启动时为每个候选 tier（默认 `[1,3,7]`）预建一套 CudaGraphRunner 和 backend state，运行时切换只是引用替换，不需要在线 graph recapture - **保守决策逻辑**：warmup_batches 跳过前几批、update_interval 避免每批都切换、down/up_hysteresis 减少振荡 - **当前限制**：只支持 `--speculative-algorithm EAGLE` + `--speculative-eagle-topk 1` **3. SGLang Tree Verify 实现细节** 从项目代码（`eagle_info.py:244`）可以看到 verify 流程： - **Greedy 路径**：`verify_tree_greedy_func()` 调用 `sgl_kernel.verify_tree_greedy` CUDA kernel，使用 `retrive_index/retrive_next_token/retrive_next_sibling` 三数组表示树结构，在 GPU 上并行遍历 tree 节点做贪心比较 - **Sampling 路径**：`tree_speculative_sampling_target_only()` kernel，执行标准 rejection sampling：对每个 draft token 计算 `min(1, p_target/p_draft)` 接受概率，用 uniform coin 决定是否接受 - **Draft probs 设为零**：当前代码中 `draft_probs = torch.zeros(...)`，说明走的是 target-only 验证（不使用 draft model 的概率分布），这与 EAGLE-3 的设计一致——draft model 的 logits 质量不足以用于 rejection sampling，简化为贪心/近似验证 **4. SGLang 最新 spec 算法扩展** - **P-EAGLE**（Issue #23171）：并行 EAGLE，所有 K 个 draft token 在一次 drafter forward 中生成，消除自回归 drafter 瓶颈。vLLM 已有 PR (#32887)，SGLang 正在跟进 - **DDTree**（Issue #22887）：扩散 draft tree，利用 DFlash drafter 的逐位置预测构建分支树 - **SSD/Saguaro**（ICLR 2026）：异步推测解码，draft model 预测 verification 结果并提前准备下一轮 draft，消除 drafting 延迟。SGLang 有人提议支持（Issue #19896） - **Spec V2**（`SGLANG_ENABLE_SPEC_V2`）：支持 STANDALONE draft model（独立小模型），不同于 EAGLE 的共享嵌入方式 **与 MiniCPM-SALA 适用性**：当前项目使用 EAGLE-3 chain verify（spec_steps=2, topk=2, dtn=5）。自适应推测解码可以直接启用（但需要 topk=1 限制解除后的适配）。tree verify 的 target-only 路径与当前 NVFP4 target 的 logits 精度约束一致。 --- ### 二、vLLM Speculative Decoding Verify 实现 **来源：vLLM 官方文档、vLLM Forums、Snowflake Arctic Inference 博客、AWS P-EAGLE 博客** **1. vLLM 与 SGLang 在 verify 实现上的关键差异** | 维度 | SGLang | vLLM | |------|--------|------| | **Verify 核心** | `sgl_kernel` 自定义 CUDA kernel（`verify_tree_greedy`, `tree_speculative_sampling_target_only`） | 早期版本用 Python 循环 + rejection sampling；V1 版本用 TensorRT-LLM 风格的 SpecMetadata + CUDA graph | | **Tree attention** | FlashInfer BSR mask + `plan/run` 调度 | FlashInfer 或 FlashAttention V2/V3；V0 版本缺少 tree decode 支持，V1 正在添加 | | **EAGLE 接受率** | 实测更接近论文数据 | vLLM 论坛用户报告 EAGLE 接受率仅 7.7%（Issue #9565），官方承认 vLLM EAGLE speedup 低于参考实现 | | **Batch spec** | 当前主要优化低 batch 场景 | V1 版本 speculative decoding 在高 concurrency 下比 baseline 还慢，已在 V1 中被弃用（Batch Speculative Decoding Done Right 论文指出） | **2. Snowflake Arctic Inference 的 vLLM 优化** - **Greedy verification 替代 rejection sampling**：将 verifier 延迟从 ~1.34ms 降到 ~0.38ms（3.5x 加速） - **CUDA graph 捕获整个 spec 推理循环**：减少 kernel launch overhead - **MLP speculator 优化**：Logits(Sharded) -> Topk(Sharded) -> AllGather -> TopK(Global)，延迟从 ~1.47ms/token 降到 ~0.47ms/token **3. P-EAGLE 在 vLLM 的实现**（AWS 博客） - 并行 drafting：一次 forward 生成所有 K 个 draft token - KV cache slot mapping：被拒绝的 token 映射到 `PADDING_SLOT_ID (-1)` 防止错误写入 - CUDA graph […]

> AGENT

现在我已经收集了所有需要的关键信息。让我整理成完整的报告。 --- ## 推测解码验证算法深挖报告 ### 一、Cactus（arXiv:2604.04987，ICLR 2026 Poster） **核心思想**：将 speculative sampling 重新形式化为约束优化问题 -- 在保证与 verifier 分布 q 的散度不超过 epsilon 的前提下，最大化接受率。 **关键公式**： 1. **优化目标**（公式3-5）：对每步 t，设 draft token 为 n，优化参数 h： - `max_h min{h_n / p(n|x_{<t}), 1}` -- 最大化接受率 - s.t. `h \in Simplex` -- h 是合法分布 - s.t. `D_f(h || q(·|x_{<t})) <= delta` -- 与 verifier 分布的 f-divergence 不超过 delta 2. **Theorem 2 最优解**（公式6-7）： - `h_i = gamma*` if i=n, `h_i = (1-gamma*) / (1-q(n)) * q(i)` otherwise - gamma* 是方程 `delta = q(n)*f(gamma/q(n)) + (1-q(n))*f((1-gamma)/(1-q(n)))` 在 [q(n), +inf) 上的根，clamp 到 [q(n), 1] 3. **Theorem 3 保证**：整体算法分布 h_alg 与 q 的 f-divergence 也受 delta 控制。 4. **Cactus 实用解（Corollary 5，KL 散度）**：使用 KL 散度 + 二阶 Taylor 近似得到闭式解： - `gamma* = min{q(n) + sqrt(2 * delta * q(n) * (1-q(n))), 1}` - 即给 draft token n 一个 "bonus probability"，bonus 最大值在 q(n)=0.5 时取得 - **Corollary 6**：当 gamma* <= 0.5 时（verifier 不太确定），近似解严格满足 KL 约束 **epsilon/delta 设置**： - delta 是唯一的超参数，控制 KL(h || q) 的上界 - delta 越大接受率越高，但输出分布偏离越远 - 实验中测试了 delta 从 0 到 0.1 的范围 - 典型值：delta=0.01~0.05 区间在准确率和速度间取得好平衡 **对 tree verify 的适用性**： - Cactus 修改的是接受率函数 phi 和恢复分布 g，理论上可以嵌入任何 verify 框架（chain 或 tree） - 但 tree verify 中每条路径的 gamma* 不同（依赖 draft token n），需要在 tree attention 的每条边独立计算 - 论文实验主要在 chain SpS 上验证，未专门做 tree verify 实验 **代码**：https://github.com/MANGA-UOFA/Cactus --- ### 二、MARS（arXiv:2601.15498） **核心思想**：利用 target model 的 logit margin（top-1 与 top-2 的 logit 差）来判断 "决策稳定性"，在低 margin 区域放宽验证。 **关键算法（3.4节）**： 对每个 draft token v_t： 1. **Exact Match**：如果 v_t = v^(1)（target 的 top-1），直接接受 2. **Adaptive Relaxation**：如果 v_t = v^(2)（target 的 top-2）且 r_t > theta，接受（视为 tie） 3. **Rejection**：否则拒绝，回退到 target 的 top-1 **核心度量 -- Logit Ratio**（公式4-6）： - `r_t = z_{t,(2)} / z_{t,(1)}` -- top-2 logit 除以 top-1 logit - 等价于自适应 margin 约束：`Delta_t < (1-theta) * z_{t,(1)}` - **关键性质**：所需 margin 与 top logit 大小线性缩放，避免概率阈值在高 logit 区域过度估计置信度 **超参数 theta**： - **固定值 theta=0.9**，在所有实验中使用 - Ablation 显示 theta 在 [0.85, 0.95] 范围内稳定 - r_t > 0.9 意味着 top-2 logit 达到 top-1 的 90%，即 margin 极小 **对 greedy vs sampling verify**： - **Greedy（T=0）**：原本严格 exact match；MARS 额外允许 top-2 通过（当 r_t > theta 时） - **Sampling（T>0）**：在标准拒绝采样基础上，当 v_t 是 top-2 且 r_t > theta 时，视为 "tie" 不拒绝 - Appendix B 给出了 greedy 结果，MARS 一致优于 EAGLE-3 **在 tree verify 中的应用**： - MARS 只修改 accept/reject 决策，与 draft 结构解耦 - 可以直接应用于 tree attention 框架 -- 每条边的验证独立应用 MARS 规则 - Section 4.5 验证了 "Framework-Decoupled Verification"：将 MARS 嵌入 Standard Speculative Decoding 也有效 **实验数据**： | Model | Method | Mean Speedup | Mean tau | |-------|--------|-------------|---------| | V 13B | EAGLE-3 […]
