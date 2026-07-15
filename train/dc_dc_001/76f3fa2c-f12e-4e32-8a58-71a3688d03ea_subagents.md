> DEVELOPER

深度调查 /user_4813494d/openbmb 仓库中 EAGLE-3 推测解码相关的技术创新。

重点阅读：
1. docs/eagle/README.md - 完整阅读
2. docs/eagle/experiments-log.md - 完整阅读（rope_theta、MARS、Phased Verify 三个方向的实验日志）
3. docs/eagle/collapse-analysis.md - 完整阅读
4. docs/eagle/training-v2.md 和 training-v3.md - 关键点
5. demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py - 关键修改
6. demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py 或类似文件 - GLA fused kernel

同时 git log 查看 EAGLE 相关的提交细节：
```
git -C /user_4813494d/openbmb log --oneline | head -50
git -C /user_4813494d/openbmb show 87a8bb1 --stat
git -C /user_4813494d/openbmb show b7a839e --stat  
git -C /user_4813494d/openbmb show 8cf5f57 --stat 2>/dev/null || true
```

我需要你给出：
1. 每个技术创新点的具体内容（不是概括，是实质）
2. 每个创新的量化收益（数字）
3. 哪些是我们独有的、竞争对手大概率没有做的
4. 哪些技术方向是已验证落地 vs 仍在实验

请尽量完整，这是为了写技术博客选题用的。

> AGENT

我会系统地调查 EAGLE-3 的技术创新。我将并行阅读所有请求的文件和 git 日志。

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/README.md"
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 Speculative Decoding
2	
3	## 结论快查
4	
5	| 结论 | 权威来源 |
6	|---|---|
7	| collapse 根因：draft 训练分布盲区（long deepresearch） | [collapse-analysis.md](collapse-analysis.md) §0 |
8	| rope_theta=1M：vlong adj_al +44.9%，已部署 | [experiments-log.md](experiments-log.md) §方向一 |
9	| MARS θ=0.85：已部署（`EAGLE_MARS_THETA=0.85`） | [experiments-log.md](experiments-log.md) §方向三 |
10	| b12x：验证通过，`SGLANG_ENABLE_B12X=0` 未启用（draft graph 不兼容） | [kernels-sm120.md](../kernels-sm120.md) §7.4 |
11	| d2t 结构 miss：`<unk>`(id=0) 占 89.2%，C2 方案可治标 +23% | [collapse-analysis.md](collapse-analysis.md) §3 |
12	| Phased Verify：early exit 71.5%，实现约 200 行，CUDA graph 是风险点 | [experiments-log.md](experiments-log.md) §方向二 |
13	
14	---
15	
16	## 1. 当前状态
17	
18	- **生产配置**：`spec_steps=3, topk=2, dtn=7`，`rope_theta=1000000`，`EAGLE_MARS_THETA=0.85`
19	- **Draft model**：`eagle/sglang_model/`（v2，415 MB safetensors），纯 Marlin W4A16 推理
20	- **Target model**：`/user_4813494d/models/openbmb/MiniCPM-SALA-gptq46-calib90-90k-NVFP4`
21	- **相关文档**：
22	  - `spec v2 + overlap` 适配记录 → [spec-v2.md](spec-v2.md)
23	  - v2 训练改进细节 → [training-v2.md](training-v2.md)
24	  - v3 训练改进（probe 选层 [4,9,24] + NVFP4 存储 + 200K 数据） → [training-v3.md](training-v3.md)
25	  - 下一代候选 → [dflash.md](dflash.md)
26	  - collapse 根因实证 → [collapse-analysis.md](collapse-analysis.md)
27	  - 实验日志（rope_theta / MARS / Phased Verify）→ [experiments-log.md](experiments-log.md)
28	
29	## 2. 架构
30	
31	```
32	Eagle3Model (~437M trainable):
33	  fc:        Linear(12288 → 4096)           # 融合 3 层 aux hidden
34	  midlayer:  Eagle3DecoderLayer             # 完整 decoder layer
35	    self_attn: Eagle3Attention (GQA 32h/2kv) # Q/K input = cat(normed_embed, normed_hidden)
36	    mlp: SwiGLU (4096 → 16384 → 4096)
37	  embed_tokens: Embedding(73448, 4096) [FROZEN]
38	  lm_head:      Linear(4096 → 32000)        # 32K draft 词表 (覆盖率 99.23%)
39	```
40	
41	- **Aux layers**：v2 用 [1, 10, 22] (CE=6.51)；**v3 改为 [4, 9, 24]** (CE=4.61, -29%)，probe greedy triple search 验证，见 [training-v3.md](training-v3.md) §1
42	- **词表**：32K 子集，`d2t` 映射 draft→full vocab
43	- **Draft 推理**：~0.50 ms/step（Marlin FP4）
44	
45	## 3. 训练关键点
46	
47	### Shifted Alignment（关键对齐）
48	
49	推理时输入 `(x_{t+1}, aux[t])` → 预测 `x_{t+2}`。训练必须匹配：
50	
51	```python
52	input_ids   = token_ids[:, 1:]       # x_1..x_{S-1}
53	aux_shifted = aux_hidden[:, :-1, :]  # aux_0..aux_{S-2}
54	target      = target_logits[:, 1:]
55	```
56	
57	修复前 OOD accept rate = 8.2%，修复后 epoch 1 即达 35.5%。
58	
59	### RoPE 对齐
60	
61	训练原本无 RoPE 但推理有 → 离线 eval 虚高。已修：`_build_rope_cache(theta=10000.0)` + `apply_rotary_pos_emb`。
62	
63	### FP4_QAT (STE fake-quantize)
64	
65	训练时 forward 用 BF16，每步 `optimizer.step()` 后 project 到 FP4 grid。MLP/fc 从 NVFP4 目标模型 dequantized 权重初始化。推理时直接用 Marlin W4A16。
66	
67	## 4. SGLang 适配（4 个关键修复）
68	
69	提交 `8bc05a3`（spec v1 路径）：
70	
71	1. **GLA state rollback**：用 `mambaish_config`（含 `minicpm_hybrid_config`）统一判断
72	2. **Sparse k1/k2 slot 分配**：新增 `_alloc_sparse_for_new_positions()`，verify 后手动分配
73	3. **Draft model 配置隔离**：量化置 None + attention backend 从 minicpm_flashinfer → flashinfer
74	4. **KV cache slot 释放时序**：verify() 开头释放 draft slots，避免孤儿
75	
76	**spec v2 额外修复**（`disable_overlap_schedule=False` 路径，见 [spec-v2.md](spec-v2.md)）：
77	- `future_indices record_stream` 稳定性修复（上游 PR #18958 等价，本地已应用）
78	- sparse k1/k2 slot 的 overalloc/真实分配 时序重构
79	
80	## 5. Fused NVFP4 Scale Loader 修复
81	
82	`QKVParallelLinear.weight_loader_v2()` 加载 fused per-tensor scale 只写 `shard_id=0`，剩余 slot 为 `torch.empty` 垃圾 → `max()` 吸收 → scale 损坏 → qkv 输出 Inf → 全链 NaN → accept_len ≈ 1.03。
83	
84	**修复**：`load_fused_per_tensor_weight()` 标量广播到所有 shard。6 种配置 (flashinfer/triton × CUDA graph on/off × 新旧 ckpt) 全部零 NaN。
85	
86	## 6. Fused GLA Kernel
87	
88	**原始路径**：24 层 GLA × dtn 步 = 72 次 kernel launch。  
89	**优化**：24 层 × 1 次 launch，处理 T=dtn 并导出全部中间 state → **7.63× 加速**（microbench, 5.51 → 0.72 ms），cos_sim = 1.0。
90	
91	### intermediate_ssm 直写
92	
93	原 `ht_buf(N*H,T,K,V) → permute → intermediate_ssm.copy`（1848 call × 21us = 39.5 ms）。Triton kernel 直写 `intermediate_ssm[cache_idx,:B,:dtn]` → 0.4 ms（-99%）。cos = 1.000000, max_abs = 4.5e-8。
94	
95	## 7. GLA Tree Verify — tree-aware dtn5 verify ✅ 已落地
96	
97	### 背景
98	
99	GLA 递推 `h_t = exp(-γ)*h_{t-1} + k_t*v_t^T`。topk>1 时 flat verify `[user_4813494d, c1, c2]` 导致 c2 继承 c1 state（应从 user_4813494d 分叉）。
100	
101	### Plan A（per-branch 扁平）❌ 回滚
102	
103	重排 `[user_4813494d, c1, c2]` → `[user_4813494d, c1, user_4813494d, c2]` 做 2 个 varlen seq。离线数值正确（cos 0.996→0.9999999）。但 FP32 4D `index_select` 引入 205 ms/cycle 热点，吞掉全部收益，净 ROI 负。
104	
105	### tree-aware dtn5 verify（commit `1a16b26`）✅
106	
107	`hybrid_linear_attn_backend.py` + `eagle_worker.py` + `eagle_info.py` 联合改造，支持 tree 结构的 sibling 隔离。已落地稳定，`tests/test_simple_gla_tree_verify.py` 回归通过。
108	
109	## 8. Break-even 分析
110	
111	| 配置 | draft (ms) | verify (ms) | break-even accept_len |
112	|---|---|---|---|
113	| Medusa K=1 (truncated) | 0.39 | 6.5 | — (baseline) |
114	| EAGLE-3 s=2, k=1, dtn=3 | ~1.0 | ~5.5 | **~1.15** |
115	
116	当前 accept_len >> break-even，EAGLE-3 稳赢。
117	
118	## 9. spec_steps>1 链式 vs 树形（已决策）
119	
120	**spec_steps>1 chain 已终结**：draft forward 线性成本 ×N（每步 ~0.5 ms） + accept_len plateau → 净负。
121	
122	tree 方向（topk>1）因 dtn5 tree-aware verify 落地恢复可用，但在 GLA + dense_len 场景对比 chain 收益未彻底量化。当前生产仍用 chain（topk=1）为稳妥选择。
123	
124	## 10. 下一步优化候选
125	
126	| 方向 | 状态 | 说明 |
127	|---|---|---|
128	| response-only loss mask | TODO | 需 `build_prompts.py` 记录 assistant 段边界 |
129	| aux_layers 调优 | **DONE (v3)** | [1,10,22]→[4,9,24]，probe CE 6.51→4.61，见 [training-v3.md](training-v3.md) §1 |
130	| NVFP4 aux_hidden 存储 | **DONE (v3)** | 2.8× 压缩，step-0 acc +0.47%（train/serve 对齐），见 [training-v3.md](training-v3.md) §2 |
131	| 10× 数据规模 (200K) | **进行中 (v3)** | 148K 已上 BOS，52K topup 已切块待补采，见 [training-v3.md](training-v3.md) §3 |
132	| torch.compile midlayer | TODO | midlayer 占训练 forward 63%，compile 可省 15-20% |
133	| DFlash 评估 | backlog | 见 [dflash.md](dflash.md)；EAGLE-3 封顶后启动 |
134	
135	## 11. 已终结方向
136	
137	| 方向 | 原因 |
138	|---|---|
139	| TARGET_VERIFY replay de-Python | profile 归因确认 target forward GPU 时间（~10ms/cycle）主导，非 Python；见 `docs/runtime.md` |
140	| spec_steps>1 chain | draft 线性成本，accept_len 不涨 |
141	| Plan A per-branch 扁平 | FP32 index_select 吞掉收益 |
142	
143	## 12. 文件结构
144	
145	eagle/ 目录导航见 [`eagle/README.md`](../../eagle/README.md)。简短总览：
146	
147	```
148	eagle/
149	├── train.py  convert_to_sglang.py  eval_ood_accept.py   # 训练 / 转换 / eval
150	├── nvfp4_codec.py  start_collect.sh                     # NVFP4 lib + 采集 server
151	├── pipeline/               # build_prompts* + collect_async (+ local TODO)
152	├── probe/                  # aux layer 选择 (一次性实验)
153	├── validation/             # NVFP4 存储验证 (一次性实验)
154	├── sglang_model/           # 当前部署 draft (v2, 415 MB) ★ 不动
155	├── weights/                # 训练产出 (best.pt)
156	└── data/                   # 训练数据 (vocab_cache + train/val/val_ood)
157	
158	demo-sala/sglang/python/sglang/srt/
159	├── speculative/eagle_worker.py      # verify + draft + alloc_sparse
160	├── speculative/eagle_info.py        # verify 逻辑 + tree 构造
161	└── layers/attention/hybrid_linear_attn_backend.py  # GLA fused + direct write + tree-aware
162	```
163
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/experiments-log.md"
}
```

> TOOL

tool_result Read
```
1	# 验证实验进度日志 — 2026-04-27
2	
3	三方向验证：rope_theta / Phased Verify / STree 并行 GLA state
4	计划来源：`/user_4813494d/.claude/plans/composed-jingling-marshmallow.md`
5	
6	---
7	
8	## 方向一：rope_theta=1M 实验 — ✅ 完成（已落 production config）
9	
10	### A/B 对照结果（同环境 concurrency=9，同 9 个样本）
11	
12	| idx | 类别 | p_tok | al_base | al_1M | Δlat(s) |
13	|---|---|---|---|---|---|
14	| 32 | 长文本/deepresearch | 130308 | 1.363 | **2.174** | -1.51 |
15	| 33 | 长文本/deepresearch | 130019 | 1.309 | **2.331** | -2.63 |
16	| 34 | 长文本/deepresearch | 129033 | 1.233 | **1.978** | -1.19 |
17	| 36 | 长文本/deepresearch | 128171 | 1.405 | **2.093** | -2.23 |
18	| 38 | 长文本/deepresearch | 125646 | 1.243 | **2.156** | -2.44 |
19	| 62 | 长文本/deepresearch | 132987 | 1.253 | **2.205** | -1.36 |
20	| 1  | 编程/代码修改 | 157 | 2.356 | 1.425 | +10.83 |
21	| 5  | 编程/代码生成 | 632 | 2.698 | 2.425 | +3.21 |
22	| 7  | 编程/代码生成 | 816 | 2.465 | 2.522 | -2.32 |
23	
24	**adj_al（来自 eagle_eval_analyze.py，剔除结构 miss）：**
25	
26	| idx | adj_base | adj_1M | Δ |
27	|---|---|---|---|
28	| 34 | 1.25 | 2.05 | **+0.80** |
29	| 36 | 1.41 | 2.11 | **+0.70** |
30	| 38 | 1.29 | 2.22 | **+0.93** |
31	| 32 | 1.38 | 2.25 | **+0.87** |
32	| 62 | 1.29 | 2.44 | **+1.15** |
33	| 33 | 1.33 | 3.88 | **+2.55**（高 miss% 略噪）|
34	| 1  | 3.65 | 1.50 | -2.15 |
35	| 5  | 2.70 | 2.43 | -0.27 |
36	| 7  | 2.47 | 2.52 | +0.05 |
37	
38	### 分析结论
39	
40	- **长 deepresearch（120K–133K）**：al 提升 56%–78%，每个样本快 1–3s
41	- **短 coding（idx 1, 157 tokens）**：al 退化，慢 +10.83s
42	- **长 coding（idx 7, 816 tokens，30907 output）**：al 持平或微升，快 -2.32s
43	
44	**Benchmark critical path 分析**：Smax=64 下 duration = max latency。
45	- idx 7（30907 output tokens）是最长请求，rope_theta=1M 使其加速 -2.32s ✓
46	- idx 1（3934 output tokens）变慢 +10.83s，但在 idx 7 仍在跑时它已完成，**不影响 critical path**
47	- 净效果：benchmark duration 应有小幅改善
48	
49	**理论机制**：rope_theta=10000 在 130K 位置外推比 ~64×，导致 sin/cos phase 周期折叠，draft attention 对长距 token pair 的 score 退化。rope_theta=1M 将 period 延伸使 phase 在 130K 内不折叠，draft 在这些位置的预测恢复正常。短 coding 退化是因为 draft 权重学到的是 theta=10000 的 frequency pattern，inference 时换 theta 破坏了 0–1K 范围内的 learned attention pattern。
50	
51	**落地状态**：
52	- `demo-sala/data/eagle_draft/config.json` ← `"rope_theta": 1000000` 已写入
53	- `eagle/sglang_model/config.json` ← 同步更新
54	
55	### 全量 A/B Probe（64 样本，concurrency=64）— ✅ 完成
56	
57	**结果文件**：`outputs/eagle_accept/rope_theta_full_20260427/rope1M.jsonl` vs `theta10k.jsonl`
58	
59	| 分组 | n | al_10k | al_1M | Δal | 说明 |
60	|---|---|---|---|---|---|
61	| 长 context（p_tok>50K） | 31 | 1.395 | 2.022 | **+0.627（+44.9%）** | 近全部样本提升 |
62	| 短/中 context（p_tok≤50K）| 33 | 1.972 | 2.072 | +0.100（+5.1%） | 基本持平，轻微正向 |
63	| **全量平均** | **64** | — | — | **+0.356** | |
64	
65	- 长 context 每样本快 1.5–16s，31 个长样本中 29 个正向（2 个微负：idx 48 -0.14，idx 51 -1.04）
66	- mini_bench：S1=242.98s，S8=328.69s，Smax=604.58s（theta=1M；theta=10000 为不同样本集，不可直接对比）
67	
68	**结论：rope_theta=1M 对全量 benchmark 有实质正向影响，config 保留。**
69	
70	---
71	
72	## 方向二：Phased Verify 离线分析 — ✅ 完成
73	
74	### 结论
75	
76	| trace 来源 | 总 steps | early_exit% | 误报 | 理论 token 减少 |
77	|---|---|---|---|---|
78	| final_check_20260426 | 7205 | **71.5%** | 0 | **28.6%** |
79	| stability_rootcause_20260426 | 4936 | **68.8%** | 0 | ~27% |
80	| /tmp/eagle_trace.jsonl（full bench run） | 264728 | **48.6%** | 0 | ~19% |
81	
82	**Full bench trace 按 bucket 分解：**
83	
84	| bucket | steps | avg_al | early_exit% |
85	|---|---|---|---|
86	| short_<1K | 9498 | 1.142 | 26.5% |
87	| mid_<8K | 45950 | 1.347 | 21.8% |
88	| long_<50K | 127333 | 0.872 | **47.3%** |
89	| vlong_>=50K | 81947 | 0.400 | **68.3%** |
90	
91	- Phase-1 check（`pr[0] ∉ {dt[1], dt[2]}`）100% 准确，零误报
92	- vlong bucket（处理我们的 deepresearch 长 prompt 输出）early exit 率 **68.3%**
93	- 代码改动估计：~200 行，主要文件：
94	  - `demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py`（verify() 拆两阶段）
95	  - `demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py`（KV slot 分段分配）
96	  - `demo-sala/sglang/python/sglang/srt/speculative/eagle_utils.py`（部分树 verify）
97	- CUDA graph 适配是主要风险：TARGET_VERIFY 需 capture 两种形状（3 tokens / 2 tokens）
98	
99	**分析脚本：** `bench/phased_verify_analyze.py`
100	
101	---
102	
103	## 方向三：STree 并行 GLA state — ✅ 完成（结论：不值得改）
104	
105	### 结论
106	
107	- GLA state rollback 已正确实现（`_fused_recurrent_gla_intermediate_kernel` + `update_mamba_state_after_mtp_verify`）
108	- `_fused_recurrent_gla_intermediate_kernel` 内 `retrieve_parent_token` 实现了等效于 STree A-matrix 累乘的 tree topology state 传播
109	- kernel 串行 step loop（dtn=5 次），理论上可并行为 3 轮，但：
110	  - verify bottleneck 是 FlashInfer prefill（32 层 attention），GLA state 计算占比小
111	  - dtn=5 的串行开销微不足道
112	- **结论：不值得重写 kernel**
113	
114	---
115	
116	## 综合优先级（最终）
117	
118	| 方向 | 状态 | 实测收益 | 推荐 |
119	|---|---|---|---|
120	| rope_theta=1M | ✅ 已落地 | 长 context al +56–78%，benchmark 中性或略正 | 已完成 |
121	| Phased Verify | 技术可行 | 理论 -28.6% token 计算量，实际收益需 bench 验证 | 下一步实施 |
122	| STree 并行 GLA | 不推进 | ROI 低（bottleneck 不在 GLA state 计算）| 关闭 |
123	| **MARS（θ=0.85）** | **✅ 初步验证** | 吞吐可观测提升，eval 分数无可观测下降 | 保留，待精调 |
124	
125	---
126	
127	## 方向四：MARS（Margin-Aware Relaxed Speculative Verification）— ✅ 初步验证
128	
129	### 方法
130	
131	论文 arXiv:2601.15498（ICLR 2026）。对每个 draft token：
132	1. `v_t == top-1` → 直接接受（原有行为）
133	2. `v_t == top-2` 且 `z_(2)/z_(1) > θ` → 放宽接受（MARS 新增）
134	3. 否则拒绝
135	
136	Training-free，仅改 verify 规则，完全兼容 tree verify。
137	
138	### 论文数据
139	
140	θ=0.90（论文推荐值，扫描范围 [0.84, 0.96]）：
141	
142	| 模型 | EAGLE-3 加速 | MARS 加速 | τ 提升 |
143	|---|---|---|---|
144	| Vicuna-13B | 3.12x | 3.74x | +27.7% |
145	| Llama-3.1-8B | 3.24x | 4.00x | +37.2% |
146	| Llama-3.1-70B | 4.40x | 4.76x | +12.9% |
147	| Qwen3-8B | 2.96x | 3.23x | +18.4% |
148	
149	质量退化（θ=0.90）：BLEU 差 0.04，ROUGE-L 差 0.0008，MT-Bench 差 <0.18 分——统计噪声范围内。
150	θ < 0.88 开始有可测量退化；θ=0.5 论文未测试。
151	
152	**无理论散度保证**（论文定位为 lossy variant，以实证为依据）。
153	
154	### 本机实测结论（2026-04-27）
155	
156	**θ=0.85：吞吐可观测提升，eval 分数无可观测下降。**
157	
158	- 论文 sweep 最低至 θ=0.84，θ=0.85 为我们扩展验证的更激进点
159	- 论文预测 θ<0.88 有可测量质量退化，但在 MiniCPM-SALA 生产 eval 中**未观测到分数下降**
160	- 可能原因：NVFP4 量化后 logit ratio 分布更集中，θ=0.85 在我们的模型上仍处于安全区间
161	- **当前推荐 θ=0.85**（实测优于论文推荐的 0.9），后续需更系统 bench 确认
162	
163	### 本机工程实现
164	
165	**改动清单（2026-04-27）**：
166	
167	| 文件 | 改动 |
168	|---|---|
169	| `sgl-kernel/csrc/speculative/eagle_utils.cu` | `VerifyTreeGreedy` kernel 8→11 参数，先 exact match 后 MARS fallback |
170	| `sgl-kernel/csrc/common_extension.cc` | PyTorch op schema 11 参数（3 新参数可选） |
171	| `sgl-kernel/include/sgl_kernel_ops.h` | 同步 C++ 头 |
172	| `sgl_kernel/speculative.py`（venv） | Python wrapper 转发新参数 |
173	| `demo-sala/sglang/.../eagle_utils.py` | 加 `target_predict.contiguous()`（必须，server 中为非连续 view） |
174	| `demo-sala/sglang/.../eagle_info.py` | verify 循环 EOS 检测，红色 ANSI 日志 |
175	
176	**重要约束**：rebuild 必须用 `gptq_marlin.cu` Feb 21 版（37KB）。Apr 25 版（44KB，新增 `workspace_blocks_per_sm` 动态参数）导致 EAGLE draft graph capture 在 bs=8 挂住。已回退，备份在 `gptq_marlin.cu.apr25.bak`。
177	
178	**启动方式**：`EAGLE_MARS_THETA=0.85 bash eval/start_eagle.sh`（默认 θ=-1.0 = MARS 关闭）
179	
180	### 已验证
181	
182	- sanity test（3 cases：legacy 8-arg / MARS hit r=0.95>θ / MARS reject r=0.5<θ）全部通过
183	- server 可起，smoke test 正常（人话输出，finish_reason=stop）
184	- EOS 红色日志功能就位
185	
186	### 待完成
187	
188	- [x] e2e bench：θ=0.85 初步验证，吞吐提升 + eval 分数无下降
189	- [ ] 系统 bench：mini_bench + full bench，量化 θ=0.85 vs off 的具体数字
190	- [ ] θ 精调：扫描 θ ∈ {0.80, 0.85, 0.88, 0.90}，找 MiniCPM-SALA 上的最优点
191	- [ ] 长 context 专项（deepresearch 样本，p_tok>50K）：MARS 在 low-accept 区域应有更大收益
192	
193	---
194	
195	## 第五轮：候选方向纸面调查（4-agent 并行，2026-04-27）
196	
197	4 个 subagent 并行精读论文，覆盖 GOOSE / SMART / RACER / Cactus / BanditSpec / FASER，以确认 greedy 兼容性和 batch=1 ROI。
198	
199	### 淘汰方向
200	
201	#### ❌ SMART（arXiv:2604.09731）— batch=1 无收益，淘汰
202	
203	**结论**：SMART 的核心价值是在大 batch compute-bound 场景防止树过展开的负收益。**batch=1 baseline 2.20× vs SMART 2.17×**，与 baseline 持平甚至微负。
204	
205	我们的场景（bs=1 decode，64 并发但 spec 在 decode 路径是独立请求逐个验证）不符合 SMART 的设计假设。
206	
207	#### ❌ Cactus（arXiv:2604.04987）— T=0 greedy 不兼容，淘汰
208	
209	**结论**：Cactus 接受规则 `gamma* = min{q(n) + sqrt(2δ·q(n)·(1-q(n))), 1}`，其中 q(n) 是 target 对 draft token n 的概率。
210	
211	在 T=0 greedy 下：target argmax token n* 的 q(n*)=1，其余 q(n≠n*)=0，因此：
212	- n = n*（draft 猜对）：gamma*=min{1+0,1}=1，接受
213	- n ≠ n*（draft 猜错）：gamma*=min{0+0,1}=0，拒绝
214	
215	**退化为精确 exact-match**，与当前 `verify_tree_greedy` 行为完全等价，零额外收益。
216	
217	### 确认候选方向
218	
219	#### ✅ GOOSE — 各向异性推测树（arXiv:2604.02047, 2026.04）
220	
221	**Greedy 兼容**：设计目标就是 T=0 greedy。核心定理不依赖概率分布，只需估算每个候选来源的 acceptance rate，可从离线统计或 in-context 滑窗获取。
222	
223	**核心机制**：观察到两种 token 来源（n-gram context match vs. 统计预测）的接受率中位数差距 **6×**（范围 2–18×）。最优树应该各向异性：高接受率的 context-matched token 形成深链（spine），低接受率统计预测 token 作为宽分支。
224	
225	**实验结果**：5 个 LLM（7B–33B）比 balanced-tree baseline 提升 **12–33%**。deepresearch 长 pattern 是高接受率 n-gram 的典型场景，在我们的 workload 上预期偏高端。
226	
227	**工程成本**：
228	- PLD n-gram lookup：prefix lookup deduplication，需维护 `{ngram_key → token_id}` 的 LRU 缓存
229	- Bigram adjacency matrix：按 token 对统计条件概率，可从 eval dataset 离线预计算，约 32000×32000 稀疏矩阵（热词覆盖 99%）
230	- 树构建逻辑嵌入 draft generation 步骤，约 200–300 行 Python + 离线统计脚本
231	
232	#### ✅ RACER — AC 自动机检索树（arXiv:2604.14885, 2026.04）
233	
234	**Greedy 兼容**：论文主实验均为 T=0，AC 自动机匹配是确定性操作，完全兼容。
235	
236	**核心机制**：用 Aho-Corasick 自动机索引已生成 token 序列，快速检索当前 prefix 对应的历史续写 candidates。LRU 淘汰控制内存使用。与 logits draft tree 融合：ngram 候选走检索分支，logits 候选走标准 EAGLE draft 分支。
237	
238	**实验结果**：deepresearch 长文本 MAT（Mean Accepted Tokens）提升 **+0.5–0.76**。特别适合长重复 pattern（deepresearch 中"根据搜索结果…"类模板），是 EAGLE 的互补而非竞争。
239	
240	**工程成本**：CPU-only，不占 GPU 时间。约 **400 行 Python**，嵌入现有 draft generation 流程（`eagle_worker.py` draft 阶段前插入 AC lookup）。是候选中实现成本最低的。
241	
242	#### ✅ BanditSpec — 自适应推测步数（arXiv:2505.15141, 2026）
243	
244	**Greedy 兼容**：信号 = accept_length（整数），与概率分布无关。UCB 臂选择是纯整数运算。完全兼容 greedy。
245	
246	**核心机制**：每个请求维护独立 UCB 多臂老虎机，arms = `{dtn=3, dtn=5, dtn=7}`。每完成一个 verify step，reward = accept_length，更新对应 arm 的 UCB 统计量，下一步选择 UCB 值最大的 arm。
247	
248	**为什么对我们有效**：
249	- vlong bucket（p_tok≥50K）当前 avg_al=0.40，dtn=5 等效效率只有 **8%**（每 5 token verify 成本只换 0.4 token 进展）
250	- 若 BanditSpec 学会在 vlong 收敛到 dtn=3，效率提升到 **13%（+63% 相对）**
251	- 编程 bucket（avg_al~2.5）dtn=5 效率 50%，dtn=7 可能更好；UCB 自动发现最优
252	
253	**工程成本**：约 **100 行 Python**，`eagle_worker.py` 中增加 per-req state dict `{rid → UCBArm}`。per-req overhead 极低（一次加法+比较）。是候选中**实现成本最低**的。
254	
255	---
256	
257	## 综合优先级（更新至 2026-04-27 第五轮）
258	
259	| # | 方向 | 状态 | 实测/预估收益 | 推荐 |
260	|---|---|---|---|---|
261	| — | rope_theta=1M | ✅ 已落地 | 长 context al +44.9%（p_tok>50K）| 已完成 |
262	| — | MARS θ=0.85 | ✅ 初步验证 | 吞吐可观测提升，eval 分数无下降 | 保留，待系统 bench |
263	| — | STree 并行 GLA | ❌ 不推进 | ROI 低，bottleneck 不在 GLA state | 关闭 |
264	| — | SMART | ❌ 淘汰 | batch=1 无收益（2.17× vs baseline 2.20×）| 关闭 |
265	| — | Cactus | ❌ 淘汰 | T=0 退化为 exact-match，零额外收益 | 关闭 |
266	| 1 | **Phased Verify** | 离线分析✅，代码未改 | 理论 -28.6% verify token，vlong early-exit 68.3% | **优先实施** |
267	| 2 | **BanditSpec** | 未实施 | vlong dtn 自适应，est +20–35% mixed workload | 低成本，建议并行 |
268	| 3 | **GOOSE** | 未实施 | +12–33% vs balanced tree（deepresearch 预期上端）| 中等成本 |
269	| 4 | **RACER** | 未实施 | deepresearch MAT +0.5–0.76 | 低成本，互补 GOOSE |
270
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/collapse-analysis.md"
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 Accept-rate Collapse 根因分析
2	
3	承接 `docs/eagle/collapse-investigation.md`（"暂判 draft 训练分布问题"，§6 留三条未排除）和 `docs/eagle/eagle-accept-handover-2026-04-26.md`（"未结案"）。本文档基于 **demosala-rollback @ 9a7e04c** 上的**实证 trace** 完成最终诊断。
4	
5	---
6	
7	## 0. 结论速查（TL;DR）
8	
9	- **根因**：pre-EOS 长生成中 49% verify step `accept_len==0`。**纯 draft 能力问题**（v2 在长 context 上 top-2 漏 target argmax）+ **少量 d2t 覆盖缺陷**（英文专有名词 "War"/"Love"/"Letter" 等 target 不在 draft 词表 32K 子集）。**与 backend / KV pool / cuda graph 无关**。
10	- **d2t 结构 miss**：bench 打分场景中 10.12% output token 不在 draft hot_set，其中 89.2% 是 `<unk>`（id=0），1.4% 是 `<|im_end|>`（id=73440），均为结构原因而非 draft 能力问题。修好两者可将 aggregate al 从 1.865 提升至 2.298（+23%）。
11	- **batch-dependent drift**：相同 prompt 在 `batch_size>=2` 下输出第 8 个 generated token 就分歧。**nospec 自己也有**（与 spec / draft 完全无关），是 sglang/flashinfer 在 multi-batch 路径上的 **GPU kernel 数值非确定性**。
12	- **80-token probe 误导**：80 token 内 al≈1.74 只覆盖 step 0-59，错过 step 60+ 的 collapse 段，之前所有基于 80-token 数据的 al 优化方向均偏差。
13	
14	**已排除**：TARGET_VERIFY sparse 路径不等价、handover "hidden state 错配"论断、stale kv suffix（9a7e04c 已 zero-fill）、PLAN_CACHE 跨 mode 错乱、topk/spec_steps/v3 配置层面 fix（±5% 无一消除 collapse）。
15	
16	---
17	
18	## 1. 诊断工具
19	
20	| 文件 | 作用 |
21	|---|---|
22	| `bench/eagle_collapse_probe.py` | 长 generation probe（concurrency × trials），sglang `/generate` `temperature=0 top_k=1 ignore_eos=True`，存 output_ids + meta_info |
23	| `bench/eagle_collapse_analyze.py` | 解析 `EAGLE_TRACE_FILE` jsonl，按 rid 分组 per-step `accept_len` 序列，找连续 al=0 段 |
24	| `bench/eagle_accept_probe.py` | greedy `temperature=0, max_new_tokens=80, ignore_eos=True`，输出 `output_ids` + `meta_info.spec_accept_*` |
25	| `bench/eagle_accept_diff.py` | spec vs nospec 第一个偏离 token |
26	| `bench/eagle_eval_probe.py` | Smax=64 对齐 probe（`CONCURRENCY=64`，stream=False 抓完整 output_ids） |
27	| `bench/eagle_eval_analyze.py` | 离线算 miss / adj_al |
28	| `EAGLE_TRACE_FILE` | sglang 内置 trace（`eagle_info.py:414`），verify event 含 `dt`/`pr`/`t2i`/`t2v`/`hn`/`acc_pred`/`ot` |
29	| env 控制 | `EAGLE_TOPK / EAGLE_SPEC_STEPS / EAGLE_FORCE_NO_ACCEPT / SGLANG_MINICPM_PLAN_CACHE / SGLANG_EAGLE_STRICT_user_4813494d` |
30	
31	---
32	
33	## 2. 单 req 实证（idx 17，pre-EOS 133 步）
34	
35	`max_tokens=2000 ignore_eos=True`。整体 al=1.052，**pre-EOS 段（133 step）**：
36	
37	- al==0: **65/133 (48.9%)**, al==1: 38, al==2: 30 → al_mean=0.737
38	- 最长连续 al==0 run: **10 步**（step 75-84，中文长 deepresearch 流畅段）
39	- collapse 段散布在整个 generation，不是单一中段坍塌
40	
41	每个 al=0 step 检查 target argmax 是否在 draft 可提议子集（`hot_token_id = d2t + arange(32000)`，覆盖 32000/73448 = 43.6% target vocab）：
42	
43	| 类别 | 数量 | 触发 token 例 |
44	|---|---|---|
45	| target OUT of hot_set | **5** | 5231 "War", 10510 "Love", 30010 "Letter", 20090 "iel", 20939 "相识" |
46	| target IN hot_set, NOT in draft top-2 | **60** | 大量中文 deepresearch 续写位置（draft 训练分布盲区） |
47	
48	EOS 后段（step 133-1900，1768 步全 al==0）是 `ignore_eos=True` + `<|im_end|>=73440` 不在 hot_set 的人为现象，不是真 collapse。
49	
50	**single req trial=3 同 prompt → 1 个 sha**（完全 deterministic）。single req 上 collapse **不是随机**，是 prompt-determined。
51	
52	### target logit gap (top1-top2) 分布
53	
54	| al | n | gap p25 | p50 | p75 | mean |
55	|---|---|---|---|---|---|
56	| 0 (collapse) | 96 | 0.94 | 2.75 | 8.25 | 4.28 |
57	| 1 (健康) | 37 | 1.31 | 4.75 | 8.25 | 5.16 |
58	| 2 (满) | 28 | 2.44 | 5.06 | 9.50 | 5.83 |
59	
60	collapse 段 logit gap 比健康段**显著低**（25% step gap < 1.0），其中部分是 target 自身高熵（任何 draft 都难命中），剩余是 draft 真错。
61	
62	### v3 draft 实测：比 v2 更糟
63	
64	切 `EAGLE_DRAFT_MODEL=/user_4813494d/openbmb/eagle/sglang_model_v3` 跑 idx 17 max_tokens=800：
65	
66	| | pre-EOS al==0% | al_mean | longest run |
67	|---|---|---|---|
68	| v2 (current) | 48.9% | 0.737 | 10 |
69	| v3（aux=[4,9,24], NLL -29% per docs） | **59.6%** | **0.578** | 9 |
70	
71	v3 在 long deepresearch 上 collapse 比 v2 更频。docs 报告的 NLL -29% 不对应这个 workload。**切 v3 不修 collapse**。
72	
73	### 80-token mean al 与 long-gen al 严重分歧
74	
75	| | idx 17 80-token al | idx 17 pre-EOS 133-step al |
76	|---|---|---|
77	| 实测 | **1.74** | **0.737** |
78	
79	**80-token probe 的 al 数字**看着不错（80 token 内 al=1.74），但**只覆盖 step 0-59**，错过了 step 60+ 的 collapse 段。**之前所有 mean al 优化（topk、spec_steps、v3 切换）都是基于 80-token 数据，没看到 collapse 段，方向偏了**。
80	
81	---
82	
83	## 3. 全量 Smax=64 量化（benchmark 场景）
84	
85	前述主要基于 idx 17 single-req focused trace。本节换到**真正打分场景**复测，逐项对齐 `toolkit/bench_serving.sh` 参数：
86	
87	| 参数 | bench 打分 | 本轮 probe |
88	|---|---|---|
89	| endpoint | `/generate` | 同 |
90	| prompt | raw text（不套 chat template） | 同 |
91	| `ignore_eos` | True | 同 |
92	| `max_new_tokens` | per-sample = `len(tokenizer.encode(dataset.model_response))`（分布 9-30991, sum=417996）| 同 |
93	| concurrency | Smax = 全 64 同时下发 | 同 |
94	
95	产物：`outputs/eagle_accept/benchlike_smax_20260426_214251/benchlike_smax.jsonl`（64 条）。
96	
97	### 总量
98	
99	- **total output tokens: 416,207**（跑满 per-sample max_new，因为 ignore_eos=True）
100	- **miss（不在 draft hot_set 的 token）: 42,110 = 10.12%**
101	- **aggregate al (raw)**: 1.865
102	- **aggregate al (miss-excluded)**: 2.298（**+23%**）
103	- wallclock 767s = 12.8 min
104	
105	### miss token 高度集中在两个结构 id
106	
107	| token | id | count | 占 total miss |
108	|---|---|---|---|
109	| `<unk>` | 0 | 37,551 | **89.2%** |
110	| `<|im_end|>` | 73440 | 578 | 1.4% |
111	| 其它（英文专名 / 生僻汉字 / url 片段） | ~4,000 | ~9.4% |
112	
113	draft `d2t + arange(32000)` 覆盖 target id 范围 ~[1, 73417]；id 0 (`<unk>`) 和 id 73440 (`<|im_end|>`) **结构上**不在子集。
114	
115	**高 miss 成因**：模型真实回答结束后 `ignore_eos=True` 强迫继续生成 → 退化到 `<unk>` / `<|im_end|>` / 少数标点的循环 → 整个尾段 draft 提议不上 → al 被拉到 ~1.15。这是**bench 打分行为的人为放大**（production `ignore_eos=False`，EOS 自然终止不会出现）。
116	
117	### 高 miss 代表样本
118	
119	| idx | cat | p_tok | max_new | out_len | miss% | unique miss | al | adj_al |
120	|---|---|---|---|---|---|---|---|---|
121	| 16 | 长文本 deepresearch | 10873 | 210 | 210 | **82.9%** | **1** | 1.12 | 15.00 |
122	| 15 | 数学能力 计算 | 127 | 30990 | 30990 | **75.9%** | **4** | 1.15 | 9.26 |
123	| 14 | 文本生成 格式遵循 | 165 | 18688 | 18688 | **75.4%** | **3** | 1.16 | 9.02 |
124	| 17 | 长文本 deepresearch | 15655 | 663 | 663 | 36.3% | 3 | 1.64 | 4.04 |
125	| 1 | 编程能力 代码修改 | 157 | 3934 | 3934 | 14.0% | 5 | 2.18 | 3.13 |
126	
127	`unique`=1-5 关键：idx 16 的 174 个 miss token **全是同一个 id**（post-EOS 单 token 循环）。
128	
129	### adj_al 排名（draft 真实命中率，剔除结构 miss 后）
130	
131	**adj_al bottom（draft 真弱项，全为 p_tok>120K long deepresearch）**：
132	
133	| idx | cat | p_tok | out_len | al | adj_al |
134	|---|---|---|---|---|---|
135	| 62 | 长文本 deepresearch | 132987 | 183 | 1.24 | **1.25** |
136	| 38 | 长文本 deepresearch | 125646 | 373 | 1.24 | **1.26** |
137	| 34 | 长文本 deepresearch | 129033 | 180 | 1.26 | **1.27** |
138	| 33 | 长文本 deepresearch | 130019 | 415 | 1.27 | **1.28** |
139	| 36 | 长文本 deepresearch | 128171 | 475 | 1.28 | **1.30** |
140	
141	**adj_al top（draft 强项，编程/数学/模板化输出）**：
142	
143	| idx | cat | p_tok | out_len | al | adj_al |
144	|---|---|---|---|---|---|
145	| 5 | 编程能力 代码生成 | 632 | 8222 | 2.82 | **2.82** |
146	| 13 | 编程能力 代码生成 | 186 | 30980 | 2.78 | **2.78** |
147	| 28 | 长文本 ? | 23360 | 918 | 2.77 | **2.77** |
148	| 3 | 数学能力 数列 | 25 | 3286 | 2.72 | **2.72** |
149	| 7 | 编程能力 代码生成 | 816 | 30907 | 2.68 | **2.68** |
150	
151	### per-category 统计
152	
153	| cat1 | n | avg_out_len | miss% | 典型 al | 备注 |
154	|---|---|---|---|---|---|
155	| 编程能力 | 12 | 20930 | **0.34%** | 2.3-2.8 | draft 强项，几乎无 `<unk>` 退化段 |
156	| 长文本 | 49 | 2287 | 3.25% | 1.2-1.7 | draft 弱项（长 context 分布） |
157	| 数学能力 | 2 | 17138 | 68.6% | — | idx 15 尾段全 `<unk>` |
158	| 文本生成 | 1 | 18688 | 75.4% | — | idx 14 尾段全 `<unk>` |
159	
160	### 可修空间量化与方案对比
161	
162	bench 打分场景下，修好 `<unk>` + `<|im_end|>` 两个结构 miss 的上限收益：aggregate al 从 **1.865 → 2.298**（+23%），throughput 线性受益。**不能根治 long deepresearch 的 draft 弱项**（adj_al=1.24-1.30 独立于 `<unk>`，是训练分布问题）。
163	
164	| 方案 | 工程量 | 是否破红线 | 覆盖 | 备注 |
165	|---|---|---|---|---|
166	| C1: lm_head 扩 2 dim (32000→32002) + 微调 | 中 | **破**（动 draft ckpt）| `<unk>` + `<|im_end|>` | 只改 d2t 不工作 |
167	| **C2**: runtime post-EOS / `<unk>`-loop detect → 该 req 退 nospec | 小 | **不破** | 退化段 draft + verify dtn=5 overhead | detect 规则：最近 K=3 commit token ∈ {0, 73440} 或最近 K=5 步 al=0；false positive 几乎不可能 |
168	| C3: 接受现状 | 0 | 不破 | 0 | bench 打分场景 -23% al 是工程债 |
169	
170	> **后续更新（2026-04-27）**：rope_theta=1M 实验落地后，long context（p_tok>50K）bucket adj_al +44.9%（全量 64 样本，concurrency=64），是另一条红线内零重训收益。C2 和 rope_theta=1M 两条路可并行。详见 [`verify-experiments-log-20260427.md`](verify-experiments-log-20260427.md) §1。
171	
172	---
173	
174	## 4. Batch drift 实证
175	
176	### single req 多次 trial → deterministic
177	
178	idx 17 max_tokens=200, concurrency=1, trial=3 → **3 次同 sha**，同 al=1.724 verify_ct=116。
179	
180	### concurrency>=2 → 分歧
181	
182	idx 17 max_tokens=200，**同 prompt × N slot 并发**：
183	
184	| concurrency | unique sha | per-slot al |
185	|---|---|---|
186	| 1 | 1 | 1.724 |
187	| 2 | 2 | 1.613 / 1.739 |
188	| 4 | 4 | 1.626 / 1.667 / 1.724 / 1.639 |
189	| 8 | 6 | 1.107-1.144 (max_tokens=800) |
190	
191	**第一个分歧 token 的位置**（nospec c=4 max_tokens=800）：output token 8（即模型回答的第 8 个新生成 token）。slot 0/3 输出"这部电影"，slot 1/2 输出"我们可以"。
192	
193	### 排除假设
194	
195	| 假设 | 实测 | 结论 |
196	|---|---|---|
197	| cuda graph 引入非确定 | `--disable-cuda-graph` c=2 仍分歧 | 不只是 cuda graph |
198	| flashinfer split-KV 非确定 | `SGLANG_MINICPM_VERIFY_DISABLE_SPLIT_KV=1` c=2 仍分歧 | 不只是 split-KV |
199	| spec/draft 引入 | **nospec c=4 也产生 4 个不同 sha** | **与 spec 完全无关**，是 sglang/flashinfer multi-batch 路径自身的数值非确定 |
200	| topk/spec_steps 配置 | chain/v3/spec3/topk3 实测 mean al ±5%，无一消除 collapse 或 drift | 配置层面无 fix |
201	
202	### batch drift 与 collapse 的关系
203	
204	batch drift 让每个 slot 走不同的 generation path → 每个 slot 在不同 token 位置碰到 draft 盲区 → collapse 段触发位置/长度不同。这就是"collapse 不固定何时发生"——**抖动不是 collapse 本身随机，是 batch drift 让 prompt 路径分叉**。single req 上 collapse 是 prompt-determined（同 prompt 必然在同位置 collapse）。
205	
206	---
207	
208	## 5. 配置搜索实验（config A–E）
209	
210	### 基线数据（current best baseline）
211	
212	**default EAGLE（topk=2, spec_steps=2, dtn=5）vs 4-26 historical**：
213	
214	| idx | task | p_tok | 4-26 al | now al | 改善 |
215	|---|---|---|---|---|---|
216	| 16 | deepresearch | 10873 | 1.333 | **1.778** | +33% |
217	| 17 | deepresearch | 15655 | 1.311 | **1.739** | +33% |
218	| 49 | "?" | 64399 | 1.081 | **1.404** | +30% |
219	
220	al 30%+ 改善来自两项改动：(1) SimpleGLA direct-state decode wired，(2) `.so` 换为 `220c18cc`（draft cuda graph capture 通过）。
221	
222	**全 64 分桶 baseline（config A）**：
223	
224	| bucket | n | task | al p50 |
225	|---|---|---|---|
226	| short <1K | 14 | 代码生成/数列/计算/格式/代码修改 | **1.86-2.29** |
227	| mid 1-8K | 1 | 代码生成 | 2.424 |
228	| long 8-50K | 18 | deepresearch / "?" | 1.509-1.538 |
229	| vlong >50K | 31 | deepresearch / "?" | 1.379-1.404 |
230	
231	全 64 mean=1.566，p50=1.481，max=2.424，min=1.194。**al 与 prompt length 单调反相关**：short al ~1.86-2.42，vlong deepresearch al ~1.38。
232	
233	### config A–E 结论表格
234	
235	| config | 参数 | 全 64 mean | long 8-50K p50 | vlong p50 | 结论 |
236	|---|---|---|---|---|---|
237	| A（baseline） | topk=2, spec_steps=2, dtn=5 | **1.566** | 1.538 | 1.379 | 当前生产 |
238	| B（chain） | topk=1, spec_steps=2, dtn=3 | 1.435（**-0.13**） | 1.311（-0.093） | — | 全面差，丢弃 |
239	| C（v3 draft） | aux=[4,9,24], 200K, NLL -29% | 1.566（**±0.000**） | 1.536（-0.015） | 1.335（**-0.039**） | short +0.10 但 vlong 退，整体持平；不是 long fix |
240	| D（spec_steps=3） | topk=2, spec_steps=3, dtn=7 | 1.604（+0.038） | 1.600（+0.049） | 1.388（+0.014） | long latency +0.3%（dominated by prefill），short latency +7.2%（净 throughput -9%）；不作 default，可做长 prompt routing |
241	| E（topk=3） | topk=3, spec_steps=2, dtn=7 | — | — | — | in flight，未完成 |
242	
243	---
244	
245	## 6. 已废弃调查路径
246	
247	**从 handover 继承的错误假设**：
248	- **handover "TARGET_VERIFY 走 sparse"**：dense vs sparse logit 不影响 spec 内部 accept rate（target argmax 取自 dense forward 自己），只影响 spec output ≠ nospec output（user 不要求 bit-identical）。accept rate 已从 1.0-1.3 改善到 1.38-1.54，根因是 SimpleGLA + .so 修复，不是 TARGET_VERIFY 路径。
249	- **handover "hidden state 错配"论断**：deeper accept 时 child verify forward 输入 token = `candidates[child]` = `target_predict[parent]`（accept condition），prefix 与 commit 完全一致，hidden state 自洽。`force_no_accept=1` 长生成与 nospec 前 134 token 完全一致是旁证。handover 结论不成立。
250	
251	**strict_user_4813494d patch 机制（实测退化为 force_no_accept）**：
252	
253	在 `eagle_info.py:391-413` 加判断 `predict_2d[:, 0].ne(candidates[:, 0])` 的 strict-user_4813494d gate 完全错误：`candidates[:, 0]` 是 `verified_id`（已 commit 的最后 token），`predict[:, 0]` 是 target 的 next-token argmax，两者按设计永远不等。patch 等价于 `EAGLE_FORCE_NO_ACCEPT=1`，accept rate 全跌至 1.01-1.10（全 64 mean=1.033，p50=1.026）。已回滚。
254	
255	**其它已排除路径**：
256	- **1608d18 "stale kv suffix"**：9a7e04c 已有 `verify_kv_indices_active_pages` zero-fill 逻辑（minicpm_backend.py:2307-2316），1608d18 主要是 python loop → Triton 性能改写，语义等价，不修 collapse。
257	- **PLAN_CACHE 跨 mode 错乱**：plan_cache 只在 decode_wrapper（minicpm_attention_kernels.py:534），verify 走 prefill_wrapper 不进 plan_cache，关闭后 idx 49 仍 t=8 偏离。
258	- **topk=1/3 / spec_steps=3 / v3 draft**：mean al ±5%，long-gen collapse 频率与 default 同量级，无一消除。
259	
260	---
261	
262	## 7. 连续坍缩机制
263	
264	User 提的关键问题：target argmax 翻一下，下一步只是少 1 个 token，spec 应当能恢复——但实测 idx 17 一进入 collapse 段就**连续 10+ 步全 al=0**。
265	
266	### 先排除两个看似合理但实测不成立的 contagion
267	
268	**(a) "翻转后 KV cache 错位污染"** — 不成立。
269	- 9a7e04c 已有 `verify_kv_indices_active_pages` zero-fill 逻辑（minicpm_backend.py:2307-2316），shrink 时 suffix 清零。
270	- al=0 时 evict_mask 把未接受的 candidate 的 KV slot 加回 free pool；下次 verify 的 `kv_indptr` 是按 commit 序列重新构造的，不会读到被 evict 的 slot。
271	- spec 内部 KV 是 **commit-aligned** 的，整条 generation 上 spec 自己看到的 prefix 与 commit 序列严格一致。
272	
273	**(b) "翻转后 draft 收到的 hidden state 是错前缀的"** — 不成立。
274	- al=0 时 commit 1 token = `target_predict[user_4813494d]`；user_4813494d 位置的 hidden state 在 verify forward 中是用 `verified_id`（上一步 commit 的最后 token）作为 input 跑的，attention prefix = 真正的 commit 序列。
275	- 下一步 draft 的 hidden 输入 = 该 user_4813494d hidden（来自正确 prefix）+ token id = commit token；二者对齐。
276	- al>=1 时 deeper accept 的 hidden state 同样自洽，因为 accept 条件 `candidate(child) == target_predict(parent)` 保证 verify forward 中 child 位置的 input 等于实际 commit token。
277	
278	实测旁证：`force_no_accept=1` 长生成与 nospec 在前 134 token 完全一致——如果 spec 内部 KV/hidden 真有 contagion，长 generation 不可能与 nospec **token-level 一致**。
279	
280	### 真因：翻转把 prefix 推入 draft 训练分布的"连续盲区"
281	
282	draft 是个独立的小 model，训练分布有限。在长 deepresearch 这种语义模板上（比如"...这部电影是中国历史战争**剧情片**，改编自清末四大奇案之一的'刺马案'..."），**连续多个位置都是 draft 训练数据未充分覆盖的语境**。每个位置 draft 的 top-2 都漏掉 target argmax → 连续 al=0。
283	
284	单点"翻转"在这条机制里的角色：
285	- 某次 verify 中 target 在高熵位置（collapse 段 p50 logit gap=2.75，健康段 p50=4.75）把 argmax 选到 token A 而不是 B。
286	- 翻转后 spec 走上"以 A 为前缀"的语义路径。
287	- 如果这条路径**整段都是 draft 盲区**（draft 训练时没见过类似 prefix → next-token 的映射），则整段连续 collapse。
288	- 翻转**不是 collapse 的"病因"**，而是"路径分支器"——把 spec 引向了一条 draft 盲区路径。
289	
290	**恢复机制**：当 target commit 走到语义边界（标点 "。" / 连接词 / 数字 / 模板化短语），prefix 重新落入 draft 熟悉的分布，accept 立即恢复。collapse 段总是被低熵、模板化的 token 终结。
291	
292	### 三个实测旁证
293	
294	1. **collapse 段 target 自己也犹豫**：al=0 段 logit gap p50=2.75，健康段 p50=5.06。target 的不确定与 draft 失败强相关。
295	2. **collapse 段 target 输出仍合理**：spec 在 collapse 段 commit 的 token 与 nospec 同位置一致（前 134 token），输出文本流畅。target 没"乱"，**spec 没"卡死"**。
296	3. **跨 prompt 差异巨大**：idx 14 (165 short, 格式遵循) long-gen al=2.09 / 0 collapse；idx 17 (15K, deepresearch) al=1.05 / 多个 >=10 步 collapse；idx 56 (136K, deepresearch) al=1.88 / 3 个 >=10 步 collapse。**与 prompt 长度不单调，与 prompt 内容（draft 训练分布覆盖度）强相关**。
297	
298	---
299	
300	## 8. 修复路径
301	
302	### A. collapse（draft 能力）
303	
304	| 选项 | 工程量 | 是否破红线 | 状态 |
305	|---|---|---|---|
306	| **A1**：重训 draft（扩长 deepresearch / reasoning 训练数据） | 大 | **破** | 非本次 scope |
307	| **A2**：扩 d2t（让 hot_token_id 覆盖 73448 全 vocab，含英文专有名词 + special tokens） | 需 lm_head 同步重训 | **破** | 非本次 scope |
308	| **A3**：runtime collapse skip — 连续 K=5 步 al=0 → 该 req 暂停 spec 走纯 nospec N=20 步 → 恢复 | 中等（按 req mask batch 复杂） | **不破** | P0 提议，未实现。治标：cap collapse 段 verify dtn=5 overhead；单 req 省 ~3-4x verify forward 时间；多 req mask 复杂 |
309	| **A4**：接受现状 + 文档化（instrumentation 已落地） | 0 | 不破 | **已完成** |
310	
311	### B. 结构 miss（`<unk>` + `<|im_end|>`，bench 打分 -23% al）
312	
313	| 选项 | 工程量 | 是否破红线 | 状态 |
314	|---|---|---|---|
315	| **C2**：runtime post-EOS / `<unk>`-loop detect → 该 req 退 nospec | 小（`eagle_worker.py` 加 per-req counter） | **不破** | 推荐实施，detect 规则稳定性高 |
316	| C1: lm_head 扩 2 dim + 微调 | 中 | **破** | 非本次 scope |
317	
318	### C. batch drift（kernel 非确定）
319	
320	| 选项 | 工程量 | 状态 |
321	|---|---|---|
322	| **B1**：接 `enable_deterministic_inference` 到 minicpm_flashinfer + minicpm_attention_kernels | 大 | 实测仅给 verify_wrapper.plan 加 disable_split_kv 不够，drift 还有其它源（mamba2 GLA、sparse top-k、layer norm reduction 等）。完整接入是大工程 |
323	| **B2**：`--max-running-requests 1` | 0 | 吞吐崩，不可用 |
324	| **B3**：接受现状 + 文档化 | 0 | **已完成** |
325	
326	### 已落地的非 functional 改动
327	
328	- `eagle_info.py` 加 `_COLLAPSE_COUNTERS` instrumentation：每 req 维护 `consec_al0` 计数，到达 `EAGLE_COLLAPSE_LOG_K`（默认 10）emit `[eagle-collapse]` warning，纯监控，不改 spec 行为。
329	- `minicpm_backend.py` verify_wrapper.plan() 两处加 `disable_split_kv`，通过 `SGLANG_MINICPM_VERIFY_DISABLE_SPLIT_KV` env 控制（默认 0）。实测不消除 c=2 batch drift，留作后续 deterministic 全栈接入时复用。
330	
331	---
332	
333	## 关键代码锚点
334	
335	- `bench/data/speed_bench_cunlimited.jsonl`：64 条数据集
336	- `outputs/eagle_accept/collapse_*/`：诊断 trace（多个时间戳子目录）
337	- `outputs/eagle_accept/benchlike_smax_20260426_214251/benchlike_smax.jsonl`：Smax=64 全量 raw
338	- `/tmp/benchlike_smax_analyze2.log`：完整 adj_al rank 表
339	- `/tmp/eagle_trace.jsonl`：最新 EAGLE_TRACE_FILE 输出
340	- `demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py:414-457`：trace verify event 写入
341	- `demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_backend.py:1964-1977 / 2364-2380`：verify_wrapper.plan() 两处（capture / replay）
342	- `demo-sala/sglang/python/sglang/srt/models/llama_eagle3.py:250-253`：`hot_token_id = d2t + arange` 加载逻辑
343	- `demo-sala/data/eagle_draft/model.safetensors`：v2 draft（d2t shape=(32000,) range=[1, 41418]，hot_token_id 覆盖 32000/73448=43.6%）
344	- `eagle/sglang_model_v3/`：v3 draft（aux=[4,9,24]，long-gen collapse 反而比 v2 更糟）
345
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/training-v2.md"
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 v2 训练改进记录
2	
3	> **状态（2026-04-27）**：v2 checkpoint 已部署生产（`eagle/sglang_model/`，415MB safetensors，NVFP4 QAT）。v3 训练已有 ckpt 但在 long deepresearch 上比 v2 更差（adj_al 0.578 vs 0.737），v3 暂未部署，见 `training-v3.md`。
4	
5	2026-04-18 重新训练 draft model 的改进总集。旧 v1 配方（SkyPile/code_search_net/wikitext + SEQ_LEN 截断 + TTT 多步 eval）与线上分布严重 mismatch，v2 针对数据分布、管线效率、eval 方法论做了全面重构。
6	
7	## 1. 数据集重构
8	
9	**动机**：旧训练分布（SkyPile 中文 web + code_search_net + wikitext）与线上 bench 严重 mismatch。线上 83% 是中文长 CoT 推理，旧训练集 0% 含 `<think>` 风格。
10	
11	**v2 配比**（20,000 样本 × 2048 tok，真实代码 token ≈ 0.6%）：
12	
13	| 数据源 | 占比 | block 切法 |
14	|---|---|---|
15	| Chinese-DeepSeek-R1-Distill-110k | 60% | 按 `repo_name` 分组拼接 |
16	| stem_zh_instruction | 22% | 按学科分组 |
17	| OpenCodeReasoning (Python 全量) | 11.5% | 按 `source` 分组 |
18	| codeforces-cots py_decontam | 5.5% | 长样本直接切 |
19	| dolphin-r1 reasoning-deepseek | 1% | 长样本直接切 |
20	
21	剔除：NuminaMath（cn_k12 text 实际为英文）。
22	
23	## 2. 采集管线
24	
25	| 文件 | 作用 |
26	|---|---|
27	| `eagle/pipeline/build_prompts.py` (当前版) / 已删的 v1 | 读 5 个数据源 → 切 2048-tok block → `/tmp/eagle3_prompts*.jsonl` |
28	| 已删的 `eagle/collect_data.py`（v1） | 旧版同步采集器，v3 换成 `eagle/pipeline/collect_async.py` |
29	| `demo-sala/.../minicpm.py:94` | `_EAGLE3_TOP_K = int(env('EAGLE3_TOP_K', '256'))`，从 256 改 128 |
30	
31	**陷阱 1：chunked prefill 切分 hook**。server 默认 `chunked-prefill-size=8192`，batch 32 × 2048 = 65k tok 被切 8 chunk。hook 对每个 chunk 写一次 .pt → 一条 prompt 产生多个残片，呈 full 2048 + medium (1024-2047) + tiny (<256) 三档分布。**修法**：采集用 `--chunked-prefill-size 131072` 或 65536。v2 采集未加，事后按长度 > 1024 过滤保留 19601 条。
32	
33	**陷阱 2：val_ood `EAGLE3_MAX_TOKENS=0` 导致 OOM**。server 需降 `--mem-fraction-static 0.70 --max-running-requests 4` + `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`。
34	
35	**陷阱 3：过滤 `completion_tokens >= 2000` 错误**。bench 本身就是生产分布，不该按长度过滤。改 `> 0` 拿全 64 条。
36	
37	## 3. 训练管线优化（-39% wall clock）
38	
39	Profile 定位（离线 microbench）：
40	
41	| 项 | baseline | 优化后 | 说明 |
42	|---|---|---|---|
43	| `GRAD_CHECKPOINT` | True | **False** | bwd 286→185 ms（-35%），peak mem 11→28 GB（84 GB 余量充足） |
44	| `BATCH_SIZE` / `GRAD_ACCUM` | 2 / 4 | **8 / 1** | effective batch 保持 8 |
45	| data loading | sync | **AsyncPrefetcher** | disk I/O 完全被 GPU 覆盖，77→21 ms |
46	| **per_sample** | **279 ms** | **169 ms** | **-39%** |
47	
48	`AsyncPrefetcher` 类在 `eagle/train.py`：后台线程 + pin_memory + `non_blocking` transfer，queue_size=2。
49	
50	Forward 内部分解（BS=4 per_sample 184ms）：
51	
52	| op | 占比 | 说明 |
53	|---|---|---|
54	| midlayer (attn + MLP) | **63%** | FP4_QAT fake-quant 固有 cost，继续优化需改 `_FP4QuantSTE` |
55	| lm_head (4096→32000) | 27% | |
56	| loss + target_p | 8% | |
57	| fc / embed / mask | 2% | |
58	
59	**Profile 数据**（BS=4 grad_ckpt=False，稳态）：
60	
61	```
62	fwd= 280ms  bwd= 381ms  mem=28.6GB  per_sample=170.1ms
63	```
64	
65	BS=12 测试（peak_mem 71.6 GB，边缘 OOM + disk-bound stalls 让 per_sample 回升到 185ms），不采用。
66	
67	## 4. 对齐官方 EAGLE（超参修正）
68	
69	| 参数 | 前 | 后 | 理由 |
70	|---|---|---|---|
71	| `MAX_GRAD_NORM` | 5.0 | **1.0** | 官方默认，防 grad 爆 |
72	| `WARMUP_STEPS` | 500 | **1500** | 总 step 数 6%（前 2% 过激） |
73	| `TTT_STEPS` | 3 | 3（未改） | 推理 spec_steps=2 只用 step 0-1；step 2 做正则 |
74	
75	## 5. eval_ood 修复
76	
77	**原问题**：旧 `eval_ood` 做 step 0..2 完整 TTT + SEQ_LEN 截断 + 逐 step 加权 acc。Step 1/2 在长序列上因 RoPE 外推坍塌（>2048 tok 时 step1 acc 18%）。
78	
79	**v2 改为 step-0 only + 全长**（`eagle/train.py:eval_ood`）：
80	
81	- 只测 step 0（user_4813494d token 预测），这是线上实际用的能力
82	- 全长 val_ood，不截断到 SEQ_LEN
83	
84	**v2 新坑**：RoPE cache = `SEQ_LEN * TTT_STEPS + 8192 + 64 = 14400`，val_ood 最长 30991 tok → 越界 `vectorized_gather_kernel`。**修法**：eval_ood 内按 `rope_max` 截断样本。
85	
86	**检查点提前保存**：ckpt 从 eval_ood 之后移到之前，eval 崩不再丢整 epoch。
87	
88	旧 `weighted_acc`（truncated 2048, TTT=3）= 0.5255 → 新 step-0 acc（full length）= 0.6607。对齐线上真实使用方式。
89	
90	## 6. vocab 覆盖（32k 维持最优）
91	
92	| K | train cov | val_ood target cov | masked |
93	|---|---|---|---|
94	| 8000 | 93.94% | 91.69% | 8.31% |
95	| 16000 | 98.07% | 96.48% | 3.52% |
96	| **32000** | **99.75%** | **99.23%** | **0.77%** |
97	
98	K=16000 masked 4.6×，accept_len 上限损失不划算。
99	
100	## 7. 未做（留给下轮）
101	
102	- **response-only loss mask**：需要 `build_prompts.py` 记录 assistant 段 token 边界。当前多数数据源无结构化分隔（只 `codeforces` 有明确 messages user/assistant）。
103	- ~~**aux_layers 调优**~~ → **v3 已做**：[1,10,22]→[4,9,24]，CE 6.51→4.61，见 [training-v3.md](training-v3.md) §1。
104	- ~~**fp8 aux_hidden 压缩**~~ → **v3 改用 NVFP4**：精度对齐生产 W4A4，step-0 acc +0.47%，2.8× 压缩，见 [training-v3.md](training-v3.md) §2。
105	- **torch.compile**：midlayer 63% 占比，compile 可能省 15-20%。
106	
107	## 8. 训练重要文件
108	
109	- `eagle/train.py` — 主训练（含 AsyncPrefetcher、FP4_QAT、TTT loop）
110	- `eagle/pipeline/build_prompts.py` — 数据切块（v3 版，旧 v1 已删）
111	- `eagle/pipeline/collect_async.py` — 并发 server 请求采集（v3，替代已删的 v1 `collect_data.py`）
112	- `eagle/convert_to_sglang.py` — ckpt → `eagle/sglang_model/` 格式
113	- `eagle/sglang_model/` — 当前部署 draft（v2，415MB safetensors）
114	- `demo-sala/sglang/python/sglang/srt/models/minicpm.py:90-161` — EAGLE3_COLLECT hook
115
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/training-v3.md"
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 v3 训练改进记录
2	
3	2026-04-24 起。v2 的遗留 TODO（aux_layers 调优、fp8 压缩、数据规模）在 v3 集中打掉。
4	
5	**本机 vs 云训分叉**：本机做 smoke（小规模、v2 老配比，控制变量只验层），云训用 BOS 上的 200K 大规模跑真正的 production ckpt。两条管线**共享相同 aux_layers [4,9,24] 和 NVFP4 存储**，只有数据量和来源不同。
6	
7	## 1. aux_layers 重选（[1,10,22] → [4,9,24]）
8	
9	v2 的 [1,10,22] 是早期粗略选择，未充分验证。v3 用 linear probe 系统搜索。
10	
11	**方法**（`eagle/probe/probe_search.py`，结果 `eagle/probe/probe_results.json`）：
12	
13	- Phase 1：采集 32 层 midlayer output 在小规模 prompts 上的 hidden
14	- Phase 2：每层单独训 linear probe → NLL on held-out token，排层强度
15	- Phase 3：greedy triple search，贪心加层，fc dim 保持 `hidden_size × 3 = 12288`
16	
17	**结果**：
18	
19	| 组合 | NLL (CE) | 备注 |
20	|---|---|---|
21	| `[1, 10, 22]` (v2) | 6.51 | baseline，浅-中-深但偏前 |
22	| `[4, 9, 24]` (v3) | **4.61** | **-29% CE**，pass 后移 |
23	| best pair (9, 24) | 4.45 | 两层已接近三层 |
24	| best single (24) | 4.92 | 深层最强 |
25	
26	结论：v2 过于靠前，v3 把第一层从 1 → 4（跳过早期 embed 噪声），第二层 10 → 9（几乎不变），第三层 22 → 24（更深）。
27	
28	## 2. NVFP4 存储（aux_hidden bf16 → NVFP4 group=16）
29	
30	**动机**：10× 数据规模下 bf16 aux_hidden 存储 10 TB 打不住，磁盘和带宽都紧张。
31	
32	**方案**（`eagle/nvfp4_codec.py`）：
33	
34	- aux_hidden 每 16 维一组，bf16 group-wise scale + FP4 E2M1 codes
35	- 与生产 fc layer 的 W4A4 NVFP4 精度**完全对齐**（训出来的权重直接能用，不丢精度）
36	- 压缩比 ~**2.8×**（48 MB bf16 → 17.3 MB 压缩）
37	
38	**验证**（`eagle/validation/validate_nvfp4_storage.py`，100 步对比）：
39	
40	| 配置 | final loss | final step-0 acc |
41	|---|---|---|
42	| baseline bf16 | — | 0.1139 |
43	| NVFP4 storage | — | **0.1186** (+0.47%) |
44	
45	NVFP4 存储**略好**于 bf16——train/serve 精度对齐的小 bonus。Bit-exact round-trip vs reference 脚本也验证过。
46	
47	## 3. 数据 pipeline 分叉
48	
49	### 云训管线：BOS 200K，`aux=[4,9,24]`
50	
51	| 阶段 | 路径 | 脚本 | 状态 |
52	|---|---|---|---|
53	| 切块 | `/tmp/eagle3_prompts_200k.jsonl` | `eagle/build_prompts.py` | 148490 行（chinese_r1 84K/136K 短） |
54	| 补齐 | `/tmp/eagle3_prompts_topup.jsonl` | `eagle/build_prompts_topup.py` | 51510 行，append 后凑 200K |
55	| 采集+上传 | BOS `bos://anp3-common-model/vista/eagle3_data/v2/` | `eagle/pipeline/collect_async.py` + `eagle/start_collect.sh` | 147K 文件/1140 段/~2 TB 已上传 |
56	| 使用 | **云训机下载** | — | 本机不使用 |
57	
58	**v3 200K 配比**（扩展自 v2 老 20K 的比例，chinese_r1 从 60% 提到 68% 扩容）：
59	
60	| 源 | 数量 | 占比 |
61	|---|---|---|
62	| Chinese-DeepSeek-R1-Distill-110k | 136,000 | 68% |
63	| stem_zh_instruction | 12,000 | 6% |
64	| OpenCodeReasoning Python | 30,000 | 15% |
65	| codeforces-cots py_decontam | 16,000 | 8% |
66	| dolphin-r1 reasoning-deepseek | 6,000 | 3% |
67	
68	**为什么本机不用 BOS 数据**：
69	
70	- 下行 76 MB/s × 865 GB (50K) ≈ 3.2 h —— 跟本地重生成差不多
71	- 但 BOS 数据是扩展 68/6/15/8/3 配比，本机要做**控制变量对比 v2**需要老 60/22/11.5/5.5/1 配比（stem_zh 在 BOS 只有 12K，顶死 54K 总样本）
72	- 重新生成的成本不高（~2 h），所以本机从源头 build 更灵活
73	
74	### 本机管线：50K v2 老配比 smoke，`aux=[4,9,24]`
75	
76	目的：**严格控制变量**跟 v2 baseline ([1,10,22], 20K, 老配比) 对比 eval_ood step-0 acc，验证新层确实更好，再去云训烧大数据。
77	
78	| 阶段 | 路径 | 脚本 | 状态 |
79	|---|---|---|---|
80	| 切块 | `/tmp/eagle3_prompts_local.jsonl` | `eagle/pipeline/build_prompts_local.py` | **TODO** |
81	| 采集 | `eagle/data/train/` (NVFP4 直写本地，**不走 BOS**) | `eagle/pipeline/collect_local.py` | **TODO** |
82	| 训练 | `eagle/train.py` 加 NVFP4 dataloader | `eagle/train.py` | **TODO** |
83	
84	**配比（v2 老 20K × 2.5）**：
85	
86	| 源 | v2 占比 | 50K 数量 |
87	|---|---|---|
88	| chinese_r1 | 60% | 30,000 |
89	| stem_zh | 22% | 11,000 |
90	| open_code | 11.5% | 5,750 |
91	| codeforces | 5.5% | 2,750 |
92	| dolphin_r1 | 1% | 500 |
93	
94	**规模选择理由**：
95	
96	- 磁盘：50K × 17.3 MB ≈ 865 GB，删 v2 旧数据后 1.2 TB free 余量足
97	- 时间：本地采集 ~2 h（避开 upload 5 MB/s 瓶颈）
98	- 数据量：v2 基线的 **2.5×**，实验层选择对比有信噪比
99	
100	## 4. 已清理
101	
102	- 删 `eagle/data/{train, val, val_ood}` 976 GB（v2 bf16 旧采集）
103	- 删 `/tmp/sglang_prof_*.{sqlite,nsys-rep}` ~10 GB
104	- 磁盘：235 GB → **1.2 TB free**
105	
106	## 5. 采集管线实现细节
107	
108	### `eagle/pipeline/collect_async.py`（云训用，BOS 上传）
109	
110	- `aiohttp` 32 并发发 `/v1/completions max_tokens=1` → server hook 写 bf16 `.pt` 到 `/tmp/eagle3_collect_v2/`
111	- `ThreadPoolExecutor(8)` 实时压 NVFP4 → stage 到 `/tmp/eagle3_stage_v2/seg_NNNNN/`
112	- 2 workers 跑 `bcecmd bos cp -r seg_dir/ bos://...` 批量上传
113	- 状态文件 `/tmp/eagle3_collect_state.json` 支持断点续传
114	- BOS 侧 `detect_remote_uploaded` 启动时 ls 去重
115	
116	**v2 (α) → v3 采集期修的坑**：
117	
118	- aiohttp keep-alive 重用 stale TCP 致 batch 首 32 请求全 ECONNRESET → `TCPConnector(force_close=True)`
119	- fail 诊断条件 `(batch % 10 == 0)` 掩盖小 batch fail → 改为 per-batch 只要有 fail 就打
120	- `UPLOAD_QUEUE_LIMIT=30` bounded queue 反压 sender，防 stage dir OOM
121	
122	**已知未解决**：
123	
124	- bcecmd `bos cp -r` 对小文件目录（100 × 17 MB）吞吐仅 5 MB/s，远低于大文件单 cp 108 MB/s。疑为 bcecmd 内部对目录模式 per-file 串行；没有公开并发参数控制。绕过方案：云训机改用 BOS SDK 直写并发 put。
125	
126	### `eagle/pipeline/collect_local.py`（本机用，**待写**）
127	
128	- 复用 `collect_async.py` 的 sender + compressor
129	- **去掉 `UploadPool`**，压缩后直写 `eagle/data_v3/train/seg_NNNNN/`
130	- 训练 dataloader 兼容相同 seg 结构（`train.py` 遍历子目录 glob `*.pt`）
131	
132	## 6. 训练侧改动（TODO）
133	
134	- `eagle/train.py`：添加 `decompress_sample` 调用（`nvfp4_codec.decompress_sample`），让 dataloader 透明支持 NVFP4 格式
135	- `EAGLE3_AUX_LAYERS=4,9,24`：hook 已支持 env 驱动，无需改 fc 层尺寸（仍是 12288）
136	- eval_ood：v2 改成 step-0 full-length 模式可以沿用，不变
137	
138	## 7. 待做清单
139	
140	- [ ] `eagle/pipeline/build_prompts_local.py`：v2 老配比 × 50K
141	- [ ] `eagle/pipeline/collect_local.py`：fork `collect_async.py`，删 upload + 本地直写
142	- [ ] 本机采 50K NVFP4 (~2 h)
143	- [ ] `eagle/train.py` 加 NVFP4 dataloader
144	- [ ] 跑训练 + eval_ood，对比 v2 baseline（老层、老数据）
145	- [ ] **若新层 win** → 继续补云端 52K 凑 200K，云训 production ckpt
146	- [ ] **若新层 lose/持平** → 回溯 probe 假设，重选层组合
147	
148	## 8. 文件索引
149	
150	| 文件 | 作用 |
151	|---|---|
152	| `eagle/probe/probe_search.py` | Phase 2/3 linear probe + greedy triple search |
153	| `eagle/probe/probe_results.json` | 层 NLL + best_triple/best_pair 结果 |
154	| `eagle/nvfp4_codec.py` | NVFP4 encode/decode/compress_sample/decompress_sample |
155	| `eagle/validation/validate_nvfp4_storage.py` | bf16 vs NVFP4 存储的训练对比（bit-exact + empirically +0.47%） |
156	| `eagle/pipeline/build_prompts.py` | 200K 扩展配比（v3 云训用） |
157	| `eagle/pipeline/build_prompts_topup.py` | chinese_r1 补齐 51510（passA stride=512 + 新 seed 短 pack） |
158	| `eagle/pipeline/collect_async.py` | 云训管线：aiohttp+NVFP4+BOS 上传 |
159	| `eagle/start_collect.sh` | 数据采集 server（aux=4,9,24，chunked_prefill=131072） |
160	| `eagle/pipeline/build_prompts_local.py` | **TODO**：v2 老配比 × 50K，本机 |
161	| `eagle/pipeline/collect_local.py` | **TODO**：本机采集（no upload） |
162
```

> TOOL

tool_use Bash
```json
{
  "command": "git -C /user_4813494d/openbmb log --oneline | head -50"
}
```

> TOOL

tool_result Bash
```
87a8bb1 perf(eagle/dynamic): four small accelerations on the spec-decode hot path
61e4904 fix(metrics/demo-sala): NO_SPEC accept stats, dynamic dtn denominator, v3 draft, env align
06ed8e0 revert(eagle/dynamic): roll back mamba pool split
e291467 fix(eagle/dynamic): KV pool reclaim, per-mode mars theta, crash fixes
20cc58a perf(eagle/dynamic): kill three hot-path wastes in spec decode
b7a839e feat(eagle): dynamic spec mode (NO_SPEC / D5 / D7) by running batch size
cc9943b docs: restructure and merge eagle docs — trim stale files, consolidate surveys
4c0005c docs: multi-doc audit — correct b12x/MARS/rope_theta status and cross-link
c783ba8 docs(eagle/mars): correct theta to 0.85 (was mistakenly recorded as 0.8)
ca22a40 docs(eagle/mars): record theta=0.8 initial validation result
8f1af57 feat(eagle): implement MARS verify + sync MARS .so to demo-sala
7cf3b63 Revert "feat(eagle): two-phase TARGET_VERIFY with shared-buffer fix"
9dabf09 feat(eagle): two-phase TARGET_VERIFY with shared-buffer fix
f0e6a61 chore(demo-sala/env): align prepare_env.sh to main
a8b22ae revert(demo-sala): roll back to 9a7e04c cu13 baseline
61213bf chore(demo-sala): drop legacy duplicates, add tuning + verify helpers
0e768a3 chore(env+eval+meta): start_eagle defaults, prepare_env tweaks, CLAUDE/AGENTS align
081559b docs: marlin-tuning + collapse + training-v3 + nvfp4-kv + infllmv2 fix + upstream survey
5b1c851 chore(bench): reorganize into kernels/{minicpm,marlin,fp4,prefill,...}; add microbenches
da18187 feat(eagle): v3 training rewrite + pipeline reorganization
1608d18 fix(sgl-srt): spec-v1 correctness + profile gating + NVFP4 lm_head pipeline
5552a23 perf: tune no-spec decode kernels
22b2bf7 chore: track eagle draft weights with git-lfs
5234ff4 chore: remove accidentally committed .venv from probe-sala
e9bfcb0 feat(probe-sala): sync sglang to latest + b12x readiness check
51ca6a8 fix(demo-sala): drop stale MARLIN_DECODE_THRESHOLD, add CUTE_DSL_CACHE_DIR
d19e4f2 perf: strip dispatch trace + hot-path cleanup
b3f9687 feat(b12x): 2-tier dispatch full-M + eagle_fc shape + dispatch trace
c3effe9 docs(runtime): §10.B 深挖 — 17.7% idle 拆分，CPU 侧真实 ROI 硬顶从 9.6% 下修到 5.5%
cd480ca docs(runtime): §7/§8/§9 memcpy attribution + §10 profiling methodology
38ab07b fix: harden spec v2 overlap path
d7e5b52 probe-sala: torchao+xgrammar wheels + exit 1 also on all-pass path
ac03fe5 eval: restore live_dashboard.py — tail-f incremental predictions viewer
59c126a eagle(v2): data pipeline + training rewrite (BS=8, fresh init, 1500 warmup)
4f8fc05 bench: cu13/sm120 kernel microbenches + b12x CuTe-DSL backend exploration
9a7e04c feat(probe-sala): full cu12→cu13 upgrade pipeline + BOS wheels offline install
230b381 docs: rewrite CLAUDE.md + trim AGENTS.md + align start_eagle.sh
bf55703 docs: restructure — rename, merge, split, update
91b0dd2 chore: purge obsolete — PLAN.md, v1 draft, superpowers/, debug archives
b4d387a perf(prefill): cross-chunk plan_info reuse + smax64 bench
1f265fe perf(prefill): reuse flashinfer plan across 8 standard layers
e36cefc feat: include eagle v2 draft weights
5c5335f feat: package eagle v2 demo-sala defaults
8017c1d fix: add tree-aware eagle dtn5 verify
0845f7b fix: stabilize eagle dtn2 replay path
9c6996a docs: EAGLE-3 数据采集 v2 设计 spec
475ddd5 eval_ood: step-0 only, full-length (no SEQ_LEN truncation)
9225f46 feat: intermediate_ssm direct-write + fused sparse metadata + profiling framework
89eb9a6 feat(gla): Plan A scaffolding — per-branch tree verify buffers
6ba52a7 feat: record triton eagle path and pin current draft model
```

> TOOL

[Request interrupted by user]

> DEVELOPER

你在 /user_4813494d/openbmb 工作区，这是一个 SOAR 2026 LLM 推理优化比赛仓库，优化 MiniCPM-SALA 模型推理。请深入调查 EAGLE-3 speculative decoding 相关的所有技术工作。

重点读取以下内容：
1. docs/eagle/ 目录下所有文件（README.md, spec-v2.md, training-v2.md, training-v3.md, collapse-analysis.md, experiments-log.md, longcontext-analysis.md, spec-survey.md, dflash.md）
2. demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py
3. demo-sala/sglang/python/sglang/srt/speculative/ 下其他文件
4. demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py（或类似文件）
5. git log 中所有 eagle 相关的提交消息

请特别关注：
- Fused GLA kernel 的技术细节和性能数字
- MARS verify 是什么，theta 参数的作用
- rope_theta=1M 的效果和原理
- tree-aware dtn verify 解决了什么问题
- dynamic spec mode（NO_SPEC/D5/D7）的设计
- 训练 v2→v3 的关键改进（probe 选层、NVFP4 存储）
- collapse 分析的具体发现

请给出一份详细的技术摘要，包括具体数字和实现细节。

> AGENT

我会系统地调查 EAGLE-3 投机解码的所有技术工作。让我先并行读取所有文档和源文件。

> TOOL

tool_use Bash
```json
{
  "command": "ls /user_4813494d/openbmb/docs/eagle/",
  "description": "List eagle docs directory"
}
```

> TOOL

tool_result Bash
```
README.md
collapse-analysis.md
dflash.md
experiments-log.md
longcontext-analysis.md
spec-survey.md
spec-v2.md
training-v2.md
training-v3.md
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/",
  "description": "List speculative decoding source files"
}
```

> TOOL

tool_result Bash
```
__pycache__
base_spec_worker.py
cpp_ngram
draft_utils.py
eagle_draft_cuda_graph_runner.py
eagle_draft_extend_cuda_graph_runner.py
eagle_info.py
eagle_info_v2.py
eagle_utils.py
eagle_worker.py
eagle_worker_v2.py
medusa_worker.py
multi_layer_eagle_draft_extend_cuda_graph_runner.py
multi_layer_eagle_utils.py
multi_layer_eagle_worker.py
multi_layer_eagle_worker_v2.py
ngram_info.py
ngram_worker.py
spec_info.py
spec_mode.py
spec_utils.py
standalone_worker.py
standalone_worker_v2.py
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/ -name \"*hybrid*\" -o -name \"*gla*\" -o -name \"*linear_attn*\" 2>/dev/null",
  "description": "Find hybrid/GLA attention files"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_attn_backend.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/simple_gla_decode_kernel.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/__pycache__/hybrid_linear_attn_backend.cpython-310.pyc
```

> TOOL

tool_use Bash
```json
{
  "command": "git log --oneline --all --grep=\"eagle\" -i --since=\"2024-01-01\" | head -80",
  "description": "Get eagle-related git commits"
}
```

> TOOL

tool_result Bash
```
87a8bb1 perf(eagle/dynamic): four small accelerations on the spec-decode hot path
61e4904 fix(metrics/demo-sala): NO_SPEC accept stats, dynamic dtn denominator, v3 draft, env align
06ed8e0 revert(eagle/dynamic): roll back mamba pool split
e291467 fix(eagle/dynamic): KV pool reclaim, per-mode mars theta, crash fixes
20cc58a perf(eagle/dynamic): kill three hot-path wastes in spec decode
b7a839e feat(eagle): dynamic spec mode (NO_SPEC / D5 / D7) by running batch size
cc9943b docs: restructure and merge eagle docs — trim stale files, consolidate surveys
4c0005c docs: multi-doc audit — correct b12x/MARS/rope_theta status and cross-link
c783ba8 docs(eagle/mars): correct theta to 0.85 (was mistakenly recorded as 0.8)
ca22a40 docs(eagle/mars): record theta=0.8 initial validation result
8f1af57 feat(eagle): implement MARS verify + sync MARS .so to demo-sala
7cf3b63 Revert "feat(eagle): two-phase TARGET_VERIFY with shared-buffer fix"
9dabf09 feat(eagle): two-phase TARGET_VERIFY with shared-buffer fix
a8b22ae revert(demo-sala): roll back to 9a7e04c cu13 baseline
0e768a3 chore(env+eval+meta): start_eagle defaults, prepare_env tweaks, CLAUDE/AGENTS align
081559b docs: marlin-tuning + collapse + training-v3 + nvfp4-kv + infllmv2 fix + upstream survey
da18187 feat(eagle): v3 training rewrite + pipeline reorganization
1608d18 fix(sgl-srt): spec-v1 correctness + profile gating + NVFP4 lm_head pipeline
22b2bf7 chore: track eagle draft weights with git-lfs
51ca6a8 fix(demo-sala): drop stale MARLIN_DECODE_THRESHOLD, add CUTE_DSL_CACHE_DIR
b3f9687 feat(b12x): 2-tier dispatch full-M + eagle_fc shape + dispatch trace
cd480ca docs(runtime): §7/§8/§9 memcpy attribution + §10 profiling methodology
59c126a eagle(v2): data pipeline + training rewrite (BS=8, fresh init, 1500 warmup)
230b381 docs: rewrite CLAUDE.md + trim AGENTS.md + align start_eagle.sh
bf55703 docs: restructure — rename, merge, split, update
91b0dd2 chore: purge obsolete — PLAN.md, v1 draft, superpowers/, debug archives
e36cefc feat: include eagle v2 draft weights
5c5335f feat: package eagle v2 demo-sala defaults
8017c1d fix: add tree-aware eagle dtn5 verify
0845f7b fix: stabilize eagle dtn2 replay path
9c6996a docs: EAGLE-3 数据采集 v2 设计 spec
9225f46 feat: intermediate_ssm direct-write + fused sparse metadata + profiling framework
617d6e5 feat: record triton eagle path and pin current draft model
6ba52a7 feat: record triton eagle path and pin current draft model
f7faed5 fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards
2b36ae2 fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards
a25e93d docs: update CLAUDE.md and PLAN.md for EAGLE-3 fused GLA
462414b docs: update CLAUDE.md and PLAN.md for EAGLE-3 fused GLA
da4309b feat: EAGLE-3 speculative decoding with fused GLA kernel
0843656 feat: EAGLE-3 speculative decoding with fused GLA kernel
351e77e chore: cleanup dead files, one-off scripts, update .gitignore
3ffeed9 chore: cleanup dead files, one-off scripts, update .gitignore
60474e8 eagle: implement STE-QAT FP4 native training + NVFP4 export pipeline
1f702ee eagle: implement STE-QAT FP4 native training + NVFP4 export pipeline
1267775 eagle: add Phase 0 baselines, Phase 2 kernel benchmarks, and plan
38ce7ea eagle: add Phase 0 baselines, Phase 2 kernel benchmarks, and plan
af38f7c docs: comprehensive cleanup — update CLAUDE.md, consolidate docs, add AGENTS.md
20ea7ec docs: comprehensive cleanup — update CLAUDE.md, consolidate docs, add AGENTS.md
ab4a619 fix: EAGLE-3 MiniCPM-SALA compatibility
8bc05a3 fix: EAGLE-3 MiniCPM-SALA compatibility
c6b7991 feat: Medusa speculative decoding integration (S1 -12%, S8 -12.5%)
3de4d05 feat: Medusa speculative decoding integration (S1 -12%, S8 -12.5%)
b478fcf feat: add EAGLE-3 speculative decoding for MiniCPM-SALA
057c168 feat: add EAGLE-3 speculative decoding for MiniCPM-SALA
```

> AGENT

现在让我并行读取所有文档文件。

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/README.md"
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 Speculative Decoding
2	
3	## 结论快查
4	
5	| 结论 | 权威来源 |
6	|---|---|
7	| collapse 根因：draft 训练分布盲区（long deepresearch） | [collapse-analysis.md](collapse-analysis.md) §0 |
8	| rope_theta=1M：vlong adj_al +44.9%，已部署 | [experiments-log.md](experiments-log.md) §方向一 |
9	| MARS θ=0.85：已部署（`EAGLE_MARS_THETA=0.85`） | [experiments-log.md](experiments-log.md) §方向三 |
10	| b12x：验证通过，`SGLANG_ENABLE_B12X=0` 未启用（draft graph 不兼容） | [kernels-sm120.md](../kernels-sm120.md) §7.4 |
11	| d2t 结构 miss：`<unk>`(id=0) 占 89.2%，C2 方案可治标 +23% | [collapse-analysis.md](collapse-analysis.md) §3 |
12	| Phased Verify：early exit 71.5%，实现约 200 行，CUDA graph 是风险点 | [experiments-log.md](experiments-log.md) §方向二 |
13	
14	---
15	
16	## 1. 当前状态
17	
18	- **生产配置**：`spec_steps=3, topk=2, dtn=7`，`rope_theta=1000000`，`EAGLE_MARS_THETA=0.85`
19	- **Draft model**：`eagle/sglang_model/`（v2，415 MB safetensors），纯 Marlin W4A16 推理
20	- **Target model**：`/user_4813494d/models/openbmb/MiniCPM-SALA-gptq46-calib90-90k-NVFP4`
21	- **相关文档**：
22	  - `spec v2 + overlap` 适配记录 → [spec-v2.md](spec-v2.md)
23	  - v2 训练改进细节 → [training-v2.md](training-v2.md)
24	  - v3 训练改进（probe 选层 [4,9,24] + NVFP4 存储 + 200K 数据） → [training-v3.md](training-v3.md)
25	  - 下一代候选 → [dflash.md](dflash.md)
26	  - collapse 根因实证 → [collapse-analysis.md](collapse-analysis.md)
27	  - 实验日志（rope_theta / MARS / Phased Verify）→ [experiments-log.md](experiments-log.md)
28	
29	## 2. 架构
30	
31	```
32	Eagle3Model (~437M trainable):
33	  fc:        Linear(12288 → 4096)           # 融合 3 层 aux hidden
34	  midlayer:  Eagle3DecoderLayer             # 完整 decoder layer
35	    self_attn: Eagle3Attention (GQA 32h/2kv) # Q/K input = cat(normed_embed, normed_hidden)
36	    mlp: SwiGLU (4096 → 16384 → 4096)
37	  embed_tokens: Embedding(73448, 4096) [FROZEN]
38	  lm_head:      Linear(4096 → 32000)        # 32K draft 词表 (覆盖率 99.23%)
39	```
40	
41	- **Aux layers**：v2 用 [1, 10, 22] (CE=6.51)；**v3 改为 [4, 9, 24]** (CE=4.61, -29%)，probe greedy triple search 验证，见 [training-v3.md](training-v3.md) §1
42	- **词表**：32K 子集，`d2t` 映射 draft→full vocab
43	- **Draft 推理**：~0.50 ms/step（Marlin FP4）
44	
45	## 3. 训练关键点
46	
47	### Shifted Alignment（关键对齐）
48	
49	推理时输入 `(x_{t+1}, aux[t])` → 预测 `x_{t+2}`。训练必须匹配：
50	
51	```python
52	input_ids   = token_ids[:, 1:]       # x_1..x_{S-1}
53	aux_shifted = aux_hidden[:, :-1, :]  # aux_0..aux_{S-2}
54	target      = target_logits[:, 1:]
55	```
56	
57	修复前 OOD accept rate = 8.2%，修复后 epoch 1 即达 35.5%。
58	
59	### RoPE 对齐
60	
61	训练原本无 RoPE 但推理有 → 离线 eval 虚高。已修：`_build_rope_cache(theta=10000.0)` + `apply_rotary_pos_emb`。
62	
63	### FP4_QAT (STE fake-quantize)
64	
65	训练时 forward 用 BF16，每步 `optimizer.step()` 后 project 到 FP4 grid。MLP/fc 从 NVFP4 目标模型 dequantized 权重初始化。推理时直接用 Marlin W4A16。
66	
67	## 4. SGLang 适配（4 个关键修复）
68	
69	提交 `8bc05a3`（spec v1 路径）：
70	
71	1. **GLA state rollback**：用 `mambaish_config`（含 `minicpm_hybrid_config`）统一判断
72	2. **Sparse k1/k2 slot 分配**：新增 `_alloc_sparse_for_new_positions()`，verify 后手动分配
73	3. **Draft model 配置隔离**：量化置 None + attention backend 从 minicpm_flashinfer → flashinfer
74	4. **KV cache slot 释放时序**：verify() 开头释放 draft slots，避免孤儿
75	
76	**spec v2 额外修复**（`disable_overlap_schedule=False` 路径，见 [spec-v2.md](spec-v2.md)）：
77	- `future_indices record_stream` 稳定性修复（上游 PR #18958 等价，本地已应用）
78	- sparse k1/k2 slot 的 overalloc/真实分配 时序重构
79	
80	## 5. Fused NVFP4 Scale Loader 修复
81	
82	`QKVParallelLinear.weight_loader_v2()` 加载 fused per-tensor scale 只写 `shard_id=0`，剩余 slot 为 `torch.empty` 垃圾 → `max()` 吸收 → scale 损坏 → qkv 输出 Inf → 全链 NaN → accept_len ≈ 1.03。
83	
84	**修复**：`load_fused_per_tensor_weight()` 标量广播到所有 shard。6 种配置 (flashinfer/triton × CUDA graph on/off × 新旧 ckpt) 全部零 NaN。
85	
86	## 6. Fused GLA Kernel
87	
88	**原始路径**：24 层 GLA × dtn 步 = 72 次 kernel launch。  
89	**优化**：24 层 × 1 次 launch，处理 T=dtn 并导出全部中间 state → **7.63× 加速**（microbench, 5.51 → 0.72 ms），cos_sim = 1.0。
90	
91	### intermediate_ssm 直写
92	
93	原 `ht_buf(N*H,T,K,V) → permute → intermediate_ssm.copy`（1848 call × 21us = 39.5 ms）。Triton kernel 直写 `intermediate_ssm[cache_idx,:B,:dtn]` → 0.4 ms（-99%）。cos = 1.000000, max_abs = 4.5e-8。
94	
95	## 7. GLA Tree Verify — tree-aware dtn5 verify ✅ 已落地
96	
97	### 背景
98	
99	GLA 递推 `h_t = exp(-γ)*h_{t-1} + k_t*v_t^T`。topk>1 时 flat verify `[user_4813494d, c1, c2]` 导致 c2 继承 c1 state（应从 user_4813494d 分叉）。
100	
101	### Plan A（per-branch 扁平）❌ 回滚
102	
103	重排 `[user_4813494d, c1, c2]` → `[user_4813494d, c1, user_4813494d, c2]` 做 2 个 varlen seq。离线数值正确（cos 0.996→0.9999999）。但 FP32 4D `index_select` 引入 205 ms/cycle 热点，吞掉全部收益，净 ROI 负。
104	
105	### tree-aware dtn5 verify（commit `1a16b26`）✅
106	
107	`hybrid_linear_attn_backend.py` + `eagle_worker.py` + `eagle_info.py` 联合改造，支持 tree 结构的 sibling 隔离。已落地稳定，`tests/test_simple_gla_tree_verify.py` 回归通过。
108	
109	## 8. Break-even 分析
110	
111	| 配置 | draft (ms) | verify (ms) | break-even accept_len |
112	|---|---|---|---|
113	| Medusa K=1 (truncated) | 0.39 | 6.5 | — (baseline) |
114	| EAGLE-3 s=2, k=1, dtn=3 | ~1.0 | ~5.5 | **~1.15** |
115	
116	当前 accept_len >> break-even，EAGLE-3 稳赢。
117	
118	## 9. spec_steps>1 链式 vs 树形（已决策）
119	
120	**spec_steps>1 chain 已终结**：draft forward 线性成本 ×N（每步 ~0.5 ms） + accept_len plateau → 净负。
121	
122	tree 方向（topk>1）因 dtn5 tree-aware verify 落地恢复可用，但在 GLA + dense_len 场景对比 chain 收益未彻底量化。当前生产仍用 chain（topk=1）为稳妥选择。
123	
124	## 10. 下一步优化候选
125	
126	| 方向 | 状态 | 说明 |
127	|---|---|---|
128	| response-only loss mask | TODO | 需 `build_prompts.py` 记录 assistant 段边界 |
129	| aux_layers 调优 | **DONE (v3)** | [1,10,22]→[4,9,24]，probe CE 6.51→4.61，见 [training-v3.md](training-v3.md) §1 |
130	| NVFP4 aux_hidden 存储 | **DONE (v3)** | 2.8× 压缩，step-0 acc +0.47%（train/serve 对齐），见 [training-v3.md](training-v3.md) §2 |
131	| 10× 数据规模 (200K) | **进行中 (v3)** | 148K 已上 BOS，52K topup 已切块待补采，见 [training-v3.md](training-v3.md) §3 |
132	| torch.compile midlayer | TODO | midlayer 占训练 forward 63%，compile 可省 15-20% |
133	| DFlash 评估 | backlog | 见 [dflash.md](dflash.md)；EAGLE-3 封顶后启动 |
134	
135	## 11. 已终结方向
136	
137	| 方向 | 原因 |
138	|---|---|
139	| TARGET_VERIFY replay de-Python | profile 归因确认 target forward GPU 时间（~10ms/cycle）主导，非 Python；见 `docs/runtime.md` |
140	| spec_steps>1 chain | draft 线性成本，accept_len 不涨 |
141	| Plan A per-branch 扁平 | FP32 index_select 吞掉收益 |
142	
143	## 12. 文件结构
144	
145	eagle/ 目录导航见 [`eagle/README.md`](../../eagle/README.md)。简短总览：
146	
147	```
148	eagle/
149	├── train.py  convert_to_sglang.py  eval_ood_accept.py   # 训练 / 转换 / eval
150	├── nvfp4_codec.py  start_collect.sh                     # NVFP4 lib + 采集 server
151	├── pipeline/               # build_prompts* + collect_async (+ local TODO)
152	├── probe/                  # aux layer 选择 (一次性实验)
153	├── validation/             # NVFP4 存储验证 (一次性实验)
154	├── sglang_model/           # 当前部署 draft (v2, 415 MB) ★ 不动
155	├── weights/                # 训练产出 (best.pt)
156	└── data/                   # 训练数据 (vocab_cache + train/val/val_ood)
157	
158	demo-sala/sglang/python/sglang/srt/
159	├── speculative/eagle_worker.py      # verify + draft + alloc_sparse
160	├── speculative/eagle_info.py        # verify 逻辑 + tree 构造
161	└── layers/attention/hybrid_linear_attn_backend.py  # GLA fused + direct write + tree-aware
162	```
163
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/spec-v2.md"
}
```

> TOOL

tool_result Read
```
1	# Spec V2 Overlap 适配记录
2	
3	## 1. 目标
4	
5	本文档记录 MiniCPM-SALA 上 `spec v2 + overlap` 的真实执行路径、与 `spec v1` 的边界、已确认问题、已落地修复、以及当前不变量。
6	
7	只记录：
8	
9	- 可复现的实现方法
10	- 已验证的设计决策
11	- 明确终结的错误方向
12	
13	不记录：
14	
15	- 会快速过期的 e2e 吞吐数字
16	- 单次 bench 截图
17	
18	## 2. 启用方式
19	
20	当前 `spec v2` 通过环境变量启用：
21	
22	```bash
23	SGLANG_ENABLE_SPEC_V2=1 bash eval/start_eagle.sh
24	```
25	
26	`server_args.py` 检测到 `eagle/eagle3 + overlap` 后，会切到 `event_loop_overlap()`，并走 `EAGLEWorkerV2` 路径，而不是 `eagle_worker.py`。
27	
28	## 3. 路径总览
29	
30	`spec v2` 的关键链路如下：
31	
32	1. `scheduler.event_loop_overlap()`
33	2. `FutureMap.resolve_future()` 从 future buffer 取回下一拍 draft 输入
34	3. `EAGLEWorkerV2.forward_batch_generation()`
35	4. `draft -> verify -> next_draft_input`
36	5. `FutureMap.store_to_map_for_new_batch()` 把下一拍 future 写回 circular buffer
37	
38	与 `spec v1` 的本质区别：
39	
40	- `v1` 没有 overlap future-map
41	- `v1` 的 finish 判定、verify 后状态提交、slot 生命周期，都在单 worker 路径内闭合
42	- `v2` 把“本拍生成”和“下一拍 draft 输入准备”拆到 overlap relay 上，任何 batch/filter/future 生命周期问题都会直接放大
43	
44	## 4. 与 Spec V1 的边界
45	
46	硬约束：
47	
48	- **不要改变 `spec v1` 已验证行为**
49	- `v1` worker 语义保持不动：`eagle_worker.py`
50	- `v2` 修复只能收敛在：
51	  - `eagle_worker_v2.py`
52	  - `overlap_utils.py`
53	  - `scheduler.py` 的 `spec v2 overlap` 分支
54	  - 少量共享数据结构，但只能是对 `v1` 惰性、无行为变化的字段
55	
56	目前允许的共享层改动只有两类：
57	
58	1. **惰性元数据**
59	   - 例如 `Req.spec_v2_sparse_k1_len/spec_v2_sparse_k2_len`
60	   - 只被 `spec v2` 使用，不参与 `v1` 路径判断
61	2. **显式受 `spec v2 overlap` 调用点控制的新参数**
62	   - 例如 `ScheduleBatch.filter_batch(..., spec_info_has_been_filtered=True)`
63	   - 默认值保持原行为，`v1` 调用点不变
64	
65	## 5. 已确认的原始问题
66	
67	### 5.1 SALA 语义没有被完整搬到 V2
68	
69	`v1` 已有的 SALA 修复最初没有完整进入 `v2`：
70	
71	- GLA / mamba verify 后状态提交
72	- MiniCPM sparse k1/k2 slot 分配
73	- unfinished-only next draft 输入
74	
75	结果：
76	
77	- overlap 会把 finished 请求再带一拍
78	- sparse row 与 dense row 生命周期失配
79	- 高并发收尾阶段容易暴露 double free / leak
80	
81	### 5.2 future_indices 生命周期不安全
82	
83	`FutureMap.alloc_future_indices()` 在 schedule/default stream 上分配 `indices`，下一拍 `resolve_future()` 在 forward stream 上读取它。
84	
85	如果旧 `spec_info` Python 引用被新对象覆盖，而 `indices` 没有 `record_stream()`，PyTorch caching allocator 可能在 GPU 仍在读时提前回收这块内存。
86	
87	upstream PR：`sglang #18958`（截至 2026-04-27 尚未 merge 进 sglang main；我们本地已应用等价修复，见 §6.4）
88	
89	结论：
90	
91	- 这个 PR 对我们有意义
92	- 它不是 sparse leak 根因，但属于必须补的稳定性修复
93	
94	### 5.3 leak 根因不是 dense tail，而是 sparse tail 的“理论长度回收”
95	
96	`spec v2` 的实际行为：
97	
98	- dense overalloc 在 `prepare_for_decode()` 里统一扩出来
99	- sparse k1/k2 **不是**随 dense 一起 overalloc
100	- sparse slot 只会在 verify 后，为 accepted token 真实分配
101	
102	原错误做法：
103	
104	- finish 时按 `kv_allocated_len` 反推 sparse tail 范围
105	- 但 `req_pool_idx` 复用后，sparse row 尾部可能留着旧请求的脏页号
106	- 回收时就把这些历史页又 free 一次
107	
108	典型表现：
109	
110	- `allocator_double_free`
111	- `dup_existing=[...]`
112	- idle self-check 报 `available_size > max_total_num_tokens`
113	
114	## 6. 已落地修复
115	
116	### 6.1 verify 后 SALA hook 进入 V2
117	
118	`eagle_worker_v2.py` 现在在 verify 后显式执行：
119	
120	- mamba / GLA state 提交
121	- `_alloc_sparse_for_new_positions()`
122	
123	原则：
124	
125	- `v2` 不能再依赖“normal decode 路径会顺便补 sparse metadata”
126	- verify 后必须在 `v2` 自己的 post-verify hook 中完成状态闭合
127	
128	### 6.2 unfinished-only future relay
129	
130	`verify` 完成后，先基于 accepted token 预测哪些请求会 finish，只给 unfinished 请求保留下一拍 future。
131	
132	实现上通过：
133	
134	- `request_keep_indices`
135	- `FutureMap.active_mask_buf`
136	- `scheduler._filter_batch_for_spec_v2_overlap()`
137	
138	目标：
139	
140	- 不让 finished 请求再多跑一拍 overlap draft
141	- 不让 next draft batch 混入已经应该退出的 req
142	
143	### 6.3 sparse cleanup 改为“按真实写入边界回收”
144	
145	为每个 req 记录：
146	
147	- `spec_v2_sparse_k1_len`
148	- `spec_v2_sparse_k2_len`
149	
150	含义：
151	
152	- 这是当前请求在 `spec v2` 下**实际写到的 sparse 上界**
153	- 不是理论上“按 dense 长度应该有多少 sparse slot”
154	
155	finish / stale cleanup 只允许回收到这个上界，不得碰后面的脏尾巴。
156	
157	### 6.4 future_indices record_stream 跟进 upstream
158	
159	`FutureMap.resolve_future()` 现在对 GPU 上的 `future_indices.indices` 调用 `record_stream()`。
160	
161	这是 `sglang #18958` 的本地等价修复。
162	
163	附带收敛：
164	
165	- `active_mask` 不再每步新建临时 `torch.zeros`
166	- 直接写回 `active_mask_buf`
167	
168	### 6.5 复用 `new_seq_lens_cpu`
169	
170	`verify` 阶段本来就会算出 CPU 版的新长度。
171	
172	现在直接把它挂到 `next_draft_input.new_seq_lens_cpu`，供 scheduler 下一拍复用，避免重复做一遍 GPU -> CPU 拷贝。
173	
174	这是纯吞吐向优化，不改变语义。
175	
176	## 7. 当前不变量
177	
178	以下不变量已经在实现里固定下来：
179	
180	1. `spec v2` 的 future relay 只允许携带 unfinished 请求
181	2. sparse 回收只能基于“当前请求真实写过的 sparse 上界”
182	3. `FutureMap.resolve_future()` 取回 future 值后，如果 spec-info 已经是活跃子集，则后续 batch filter 必须以 `has_been_filtered=True` 处理
183	4. `spec v2` 对共享层的任何改动，都必须能证明 `v1` 默认调用点行为不变
184	
185	## 8. 已终结错误方向
186	
187	### 8.1 “record_batch_in_overlap 引用保活已经够了”
188	
189	不够。
190	
191	`record_batch_in_overlap()` 只是一个对象引用保活 hack，不能替代跨 stream tensor 生命周期声明。`future_indices.indices` 仍然需要 `record_stream()`。
192	
193	### 8.2 “按 dense overalloc 长度回收 sparse tail”
194	
195	错误。
196	
197	这是假设 sparse 分配和 dense 一样按理论长度连续增长，但 `spec v2` 实际不是这样工作的。
198	
199	### 8.3 “把所有共享 filter 逻辑一把改掉也没关系”
200	
201	错误。
202	
203	`v1` 已经验证过，shared `filter_batch()`、shared sparse metadata 处理如果无约束地修改，最容易把 `v1` 一起带坏。
204	
205	## 9. 当前保留的吞吐优化边界
206	
207	已经收下、风险低的优化：
208	
209	- `future_indices.indices.record_stream()`
210	- `active_mask_buf` 复用
211	- `new_seq_lens_cpu` 复用
212	- overlap filter 中 `keep_indices` device tensor 复用
213	
214	暂时**不收**的优化：
215	
216	- 把 `build_request_keep_indices_for_spec_v2()` 的 finish 判定完全搬离 CPU
217	
218	原因：
219	
220	- 这段逻辑已经碰到 `eos / stop_token_ids / stop_str / regex / grammar` 语义边界
221	- 再压缩会直接触碰正确率和 finish 语义，不属于低风险吞吐优化
222	
223	## 10. 最小验证集
224	
225	文档只记录验证方法，不记录易过期数字。
226	
227	### 单测
228	
229	```bash
230	python -m unittest demo-sala.sglang.python.sglang.test.speculative.test_eagle_worker_v2
231	```
232	
233	### 真实 smoke
234	
235	```bash
236	bash eval/start_eagle.sh
237	```
238	
239	单请求：
240	
241	```bash
242	curl -s http://127.0.0.1:30000/v1/chat/completions \
243	  -H 'Content-Type: application/json' \
244	  -d '{
245	    "model":"minicpm",
246	    "messages":[{"role":"user","content":"请用中文简短解释一下地球自转和公转的区别。"}],
247	    "max_tokens":256
248	  }'
249	```
250	
251	并发 smoke：
252	
253	- 发 3 条短中文问答
254	- 看是否全部 `200`
255	- 看服务端是否出现：
256	  - `allocator_double_free`
257	  - `memory leak detected`
258	  - `device-side assert triggered`
259	  - `Scheduler hit an exception`
260	
261	停服：
262	
263	```bash
264	bash bench/kill_sglang.sh
265	```
266	
267	## 11. 相关文件
268	
269	- `demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py`
270	- `demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py`
271	- `demo-sala/sglang/python/sglang/srt/managers/overlap_utils.py`
272	- `demo-sala/sglang/python/sglang/srt/managers/scheduler.py`
273	- `demo-sala/sglang/python/sglang/srt/managers/scheduler_output_processor_mixin.py`
274	- `demo-sala/sglang/python/sglang/srt/mem_cache/common.py`
275	- `demo-sala/sglang/python/sglang/test/speculative/test_eagle_worker_v2.py`
276
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/training-v2.md"
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 v2 训练改进记录
2	
3	> **状态（2026-04-27）**：v2 checkpoint 已部署生产（`eagle/sglang_model/`，415MB safetensors，NVFP4 QAT）。v3 训练已有 ckpt 但在 long deepresearch 上比 v2 更差（adj_al 0.578 vs 0.737），v3 暂未部署，见 `training-v3.md`。
4	
5	2026-04-18 重新训练 draft model 的改进总集。旧 v1 配方（SkyPile/code_search_net/wikitext + SEQ_LEN 截断 + TTT 多步 eval）与线上分布严重 mismatch，v2 针对数据分布、管线效率、eval 方法论做了全面重构。
6	
7	## 1. 数据集重构
8	
9	**动机**：旧训练分布（SkyPile 中文 web + code_search_net + wikitext）与线上 bench 严重 mismatch。线上 83% 是中文长 CoT 推理，旧训练集 0% 含 `<think>` 风格。
10	
11	**v2 配比**（20,000 样本 × 2048 tok，真实代码 token ≈ 0.6%）：
12	
13	| 数据源 | 占比 | block 切法 |
14	|---|---|---|
15	| Chinese-DeepSeek-R1-Distill-110k | 60% | 按 `repo_name` 分组拼接 |
16	| stem_zh_instruction | 22% | 按学科分组 |
17	| OpenCodeReasoning (Python 全量) | 11.5% | 按 `source` 分组 |
18	| codeforces-cots py_decontam | 5.5% | 长样本直接切 |
19	| dolphin-r1 reasoning-deepseek | 1% | 长样本直接切 |
20	
21	剔除：NuminaMath（cn_k12 text 实际为英文）。
22	
23	## 2. 采集管线
24	
25	| 文件 | 作用 |
26	|---|---|
27	| `eagle/pipeline/build_prompts.py` (当前版) / 已删的 v1 | 读 5 个数据源 → 切 2048-tok block → `/tmp/eagle3_prompts*.jsonl` |
28	| 已删的 `eagle/collect_data.py`（v1） | 旧版同步采集器，v3 换成 `eagle/pipeline/collect_async.py` |
29	| `demo-sala/.../minicpm.py:94` | `_EAGLE3_TOP_K = int(env('EAGLE3_TOP_K', '256'))`，从 256 改 128 |
30	
31	**陷阱 1：chunked prefill 切分 hook**。server 默认 `chunked-prefill-size=8192`，batch 32 × 2048 = 65k tok 被切 8 chunk。hook 对每个 chunk 写一次 .pt → 一条 prompt 产生多个残片，呈 full 2048 + medium (1024-2047) + tiny (<256) 三档分布。**修法**：采集用 `--chunked-prefill-size 131072` 或 65536。v2 采集未加，事后按长度 > 1024 过滤保留 19601 条。
32	
33	**陷阱 2：val_ood `EAGLE3_MAX_TOKENS=0` 导致 OOM**。server 需降 `--mem-fraction-static 0.70 --max-running-requests 4` + `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`。
34	
35	**陷阱 3：过滤 `completion_tokens >= 2000` 错误**。bench 本身就是生产分布，不该按长度过滤。改 `> 0` 拿全 64 条。
36	
37	## 3. 训练管线优化（-39% wall clock）
38	
39	Profile 定位（离线 microbench）：
40	
41	| 项 | baseline | 优化后 | 说明 |
42	|---|---|---|---|
43	| `GRAD_CHECKPOINT` | True | **False** | bwd 286→185 ms（-35%），peak mem 11→28 GB（84 GB 余量充足） |
44	| `BATCH_SIZE` / `GRAD_ACCUM` | 2 / 4 | **8 / 1** | effective batch 保持 8 |
45	| data loading | sync | **AsyncPrefetcher** | disk I/O 完全被 GPU 覆盖，77→21 ms |
46	| **per_sample** | **279 ms** | **169 ms** | **-39%** |
47	
48	`AsyncPrefetcher` 类在 `eagle/train.py`：后台线程 + pin_memory + `non_blocking` transfer，queue_size=2。
49	
50	Forward 内部分解（BS=4 per_sample 184ms）：
51	
52	| op | 占比 | 说明 |
53	|---|---|---|
54	| midlayer (attn + MLP) | **63%** | FP4_QAT fake-quant 固有 cost，继续优化需改 `_FP4QuantSTE` |
55	| lm_head (4096→32000) | 27% | |
56	| loss + target_p | 8% | |
57	| fc / embed / mask | 2% | |
58	
59	**Profile 数据**（BS=4 grad_ckpt=False，稳态）：
60	
61	```
62	fwd= 280ms  bwd= 381ms  mem=28.6GB  per_sample=170.1ms
63	```
64	
65	BS=12 测试（peak_mem 71.6 GB，边缘 OOM + disk-bound stalls 让 per_sample 回升到 185ms），不采用。
66	
67	## 4. 对齐官方 EAGLE（超参修正）
68	
69	| 参数 | 前 | 后 | 理由 |
70	|---|---|---|---|
71	| `MAX_GRAD_NORM` | 5.0 | **1.0** | 官方默认，防 grad 爆 |
72	| `WARMUP_STEPS` | 500 | **1500** | 总 step 数 6%（前 2% 过激） |
73	| `TTT_STEPS` | 3 | 3（未改） | 推理 spec_steps=2 只用 step 0-1；step 2 做正则 |
74	
75	## 5. eval_ood 修复
76	
77	**原问题**：旧 `eval_ood` 做 step 0..2 完整 TTT + SEQ_LEN 截断 + 逐 step 加权 acc。Step 1/2 在长序列上因 RoPE 外推坍塌（>2048 tok 时 step1 acc 18%）。
78	
79	**v2 改为 step-0 only + 全长**（`eagle/train.py:eval_ood`）：
80	
81	- 只测 step 0（user_4813494d token 预测），这是线上实际用的能力
82	- 全长 val_ood，不截断到 SEQ_LEN
83	
84	**v2 新坑**：RoPE cache = `SEQ_LEN * TTT_STEPS + 8192 + 64 = 14400`，val_ood 最长 30991 tok → 越界 `vectorized_gather_kernel`。**修法**：eval_ood 内按 `rope_max` 截断样本。
85	
86	**检查点提前保存**：ckpt 从 eval_ood 之后移到之前，eval 崩不再丢整 epoch。
87	
88	旧 `weighted_acc`（truncated 2048, TTT=3）= 0.5255 → 新 step-0 acc（full length）= 0.6607。对齐线上真实使用方式。
89	
90	## 6. vocab 覆盖（32k 维持最优）
91	
92	| K | train cov | val_ood target cov | masked |
93	|---|---|---|---|
94	| 8000 | 93.94% | 91.69% | 8.31% |
95	| 16000 | 98.07% | 96.48% | 3.52% |
96	| **32000** | **99.75%** | **99.23%** | **0.77%** |
97	
98	K=16000 masked 4.6×，accept_len 上限损失不划算。
99	
100	## 7. 未做（留给下轮）
101	
102	- **response-only loss mask**：需要 `build_prompts.py` 记录 assistant 段 token 边界。当前多数数据源无结构化分隔（只 `codeforces` 有明确 messages user/assistant）。
103	- ~~**aux_layers 调优**~~ → **v3 已做**：[1,10,22]→[4,9,24]，CE 6.51→4.61，见 [training-v3.md](training-v3.md) §1。
104	- ~~**fp8 aux_hidden 压缩**~~ → **v3 改用 NVFP4**：精度对齐生产 W4A4，step-0 acc +0.47%，2.8× 压缩，见 [training-v3.md](training-v3.md) §2。
105	- **torch.compile**：midlayer 63% 占比，compile 可能省 15-20%。
106	
107	## 8. 训练重要文件
108	
109	- `eagle/train.py` — 主训练（含 AsyncPrefetcher、FP4_QAT、TTT loop）
110	- `eagle/pipeline/build_prompts.py` — 数据切块（v3 版，旧 v1 已删）
111	- `eagle/pipeline/collect_async.py` — 并发 server 请求采集（v3，替代已删的 v1 `collect_data.py`）
112	- `eagle/convert_to_sglang.py` — ckpt → `eagle/sglang_model/` 格式
113	- `eagle/sglang_model/` — 当前部署 draft（v2，415MB safetensors）
114	- `demo-sala/sglang/python/sglang/srt/models/minicpm.py:90-161` — EAGLE3_COLLECT hook
115
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/training-v3.md"
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 v3 训练改进记录
2	
3	2026-04-24 起。v2 的遗留 TODO（aux_layers 调优、fp8 压缩、数据规模）在 v3 集中打掉。
4	
5	**本机 vs 云训分叉**：本机做 smoke（小规模、v2 老配比，控制变量只验层），云训用 BOS 上的 200K 大规模跑真正的 production ckpt。两条管线**共享相同 aux_layers [4,9,24] 和 NVFP4 存储**，只有数据量和来源不同。
6	
7	## 1. aux_layers 重选（[1,10,22] → [4,9,24]）
8	
9	v2 的 [1,10,22] 是早期粗略选择，未充分验证。v3 用 linear probe 系统搜索。
10	
11	**方法**（`eagle/probe/probe_search.py`，结果 `eagle/probe/probe_results.json`）：
12	
13	- Phase 1：采集 32 层 midlayer output 在小规模 prompts 上的 hidden
14	- Phase 2：每层单独训 linear probe → NLL on held-out token，排层强度
15	- Phase 3：greedy triple search，贪心加层，fc dim 保持 `hidden_size × 3 = 12288`
16	
17	**结果**：
18	
19	| 组合 | NLL (CE) | 备注 |
20	|---|---|---|
21	| `[1, 10, 22]` (v2) | 6.51 | baseline，浅-中-深但偏前 |
22	| `[4, 9, 24]` (v3) | **4.61** | **-29% CE**，pass 后移 |
23	| best pair (9, 24) | 4.45 | 两层已接近三层 |
24	| best single (24) | 4.92 | 深层最强 |
25	
26	结论：v2 过于靠前，v3 把第一层从 1 → 4（跳过早期 embed 噪声），第二层 10 → 9（几乎不变），第三层 22 → 24（更深）。
27	
28	## 2. NVFP4 存储（aux_hidden bf16 → NVFP4 group=16）
29	
30	**动机**：10× 数据规模下 bf16 aux_hidden 存储 10 TB 打不住，磁盘和带宽都紧张。
31	
32	**方案**（`eagle/nvfp4_codec.py`）：
33	
34	- aux_hidden 每 16 维一组，bf16 group-wise scale + FP4 E2M1 codes
35	- 与生产 fc layer 的 W4A4 NVFP4 精度**完全对齐**（训出来的权重直接能用，不丢精度）
36	- 压缩比 ~**2.8×**（48 MB bf16 → 17.3 MB 压缩）
37	
38	**验证**（`eagle/validation/validate_nvfp4_storage.py`，100 步对比）：
39	
40	| 配置 | final loss | final step-0 acc |
41	|---|---|---|
42	| baseline bf16 | — | 0.1139 |
43	| NVFP4 storage | — | **0.1186** (+0.47%) |
44	
45	NVFP4 存储**略好**于 bf16——train/serve 精度对齐的小 bonus。Bit-exact round-trip vs reference 脚本也验证过。
46	
47	## 3. 数据 pipeline 分叉
48	
49	### 云训管线：BOS 200K，`aux=[4,9,24]`
50	
51	| 阶段 | 路径 | 脚本 | 状态 |
52	|---|---|---|---|
53	| 切块 | `/tmp/eagle3_prompts_200k.jsonl` | `eagle/build_prompts.py` | 148490 行（chinese_r1 84K/136K 短） |
54	| 补齐 | `/tmp/eagle3_prompts_topup.jsonl` | `eagle/build_prompts_topup.py` | 51510 行，append 后凑 200K |
55	| 采集+上传 | BOS `bos://anp3-common-model/vista/eagle3_data/v2/` | `eagle/pipeline/collect_async.py` + `eagle/start_collect.sh` | 147K 文件/1140 段/~2 TB 已上传 |
56	| 使用 | **云训机下载** | — | 本机不使用 |
57	
58	**v3 200K 配比**（扩展自 v2 老 20K 的比例，chinese_r1 从 60% 提到 68% 扩容）：
59	
60	| 源 | 数量 | 占比 |
61	|---|---|---|
62	| Chinese-DeepSeek-R1-Distill-110k | 136,000 | 68% |
63	| stem_zh_instruction | 12,000 | 6% |
64	| OpenCodeReasoning Python | 30,000 | 15% |
65	| codeforces-cots py_decontam | 16,000 | 8% |
66	| dolphin-r1 reasoning-deepseek | 6,000 | 3% |
67	
68	**为什么本机不用 BOS 数据**：
69	
70	- 下行 76 MB/s × 865 GB (50K) ≈ 3.2 h —— 跟本地重生成差不多
71	- 但 BOS 数据是扩展 68/6/15/8/3 配比，本机要做**控制变量对比 v2**需要老 60/22/11.5/5.5/1 配比（stem_zh 在 BOS 只有 12K，顶死 54K 总样本）
72	- 重新生成的成本不高（~2 h），所以本机从源头 build 更灵活
73	
74	### 本机管线：50K v2 老配比 smoke，`aux=[4,9,24]`
75	
76	目的：**严格控制变量**跟 v2 baseline ([1,10,22], 20K, 老配比) 对比 eval_ood step-0 acc，验证新层确实更好，再去云训烧大数据。
77	
78	| 阶段 | 路径 | 脚本 | 状态 |
79	|---|---|---|---|
80	| 切块 | `/tmp/eagle3_prompts_local.jsonl` | `eagle/pipeline/build_prompts_local.py` | **TODO** |
81	| 采集 | `eagle/data/train/` (NVFP4 直写本地，**不走 BOS**) | `eagle/pipeline/collect_local.py` | **TODO** |
82	| 训练 | `eagle/train.py` 加 NVFP4 dataloader | `eagle/train.py` | **TODO** |
83	
84	**配比（v2 老 20K × 2.5）**：
85	
86	| 源 | v2 占比 | 50K 数量 |
87	|---|---|---|
88	| chinese_r1 | 60% | 30,000 |
89	| stem_zh | 22% | 11,000 |
90	| open_code | 11.5% | 5,750 |
91	| codeforces | 5.5% | 2,750 |
92	| dolphin_r1 | 1% | 500 |
93	
94	**规模选择理由**：
95	
96	- 磁盘：50K × 17.3 MB ≈ 865 GB，删 v2 旧数据后 1.2 TB free 余量足
97	- 时间：本地采集 ~2 h（避开 upload 5 MB/s 瓶颈）
98	- 数据量：v2 基线的 **2.5×**，实验层选择对比有信噪比
99	
100	## 4. 已清理
101	
102	- 删 `eagle/data/{train, val, val_ood}` 976 GB（v2 bf16 旧采集）
103	- 删 `/tmp/sglang_prof_*.{sqlite,nsys-rep}` ~10 GB
104	- 磁盘：235 GB → **1.2 TB free**
105	
106	## 5. 采集管线实现细节
107	
108	### `eagle/pipeline/collect_async.py`（云训用，BOS 上传）
109	
110	- `aiohttp` 32 并发发 `/v1/completions max_tokens=1` → server hook 写 bf16 `.pt` 到 `/tmp/eagle3_collect_v2/`
111	- `ThreadPoolExecutor(8)` 实时压 NVFP4 → stage 到 `/tmp/eagle3_stage_v2/seg_NNNNN/`
112	- 2 workers 跑 `bcecmd bos cp -r seg_dir/ bos://...` 批量上传
113	- 状态文件 `/tmp/eagle3_collect_state.json` 支持断点续传
114	- BOS 侧 `detect_remote_uploaded` 启动时 ls 去重
115	
116	**v2 (α) → v3 采集期修的坑**：
117	
118	- aiohttp keep-alive 重用 stale TCP 致 batch 首 32 请求全 ECONNRESET → `TCPConnector(force_close=True)`
119	- fail 诊断条件 `(batch % 10 == 0)` 掩盖小 batch fail → 改为 per-batch 只要有 fail 就打
120	- `UPLOAD_QUEUE_LIMIT=30` bounded queue 反压 sender，防 stage dir OOM
121	
122	**已知未解决**：
123	
124	- bcecmd `bos cp -r` 对小文件目录（100 × 17 MB）吞吐仅 5 MB/s，远低于大文件单 cp 108 MB/s。疑为 bcecmd 内部对目录模式 per-file 串行；没有公开并发参数控制。绕过方案：云训机改用 BOS SDK 直写并发 put。
125	
126	### `eagle/pipeline/collect_local.py`（本机用，**待写**）
127	
128	- 复用 `collect_async.py` 的 sender + compressor
129	- **去掉 `UploadPool`**，压缩后直写 `eagle/data_v3/train/seg_NNNNN/`
130	- 训练 dataloader 兼容相同 seg 结构（`train.py` 遍历子目录 glob `*.pt`）
131	
132	## 6. 训练侧改动（TODO）
133	
134	- `eagle/train.py`：添加 `decompress_sample` 调用（`nvfp4_codec.decompress_sample`），让 dataloader 透明支持 NVFP4 格式
135	- `EAGLE3_AUX_LAYERS=4,9,24`：hook 已支持 env 驱动，无需改 fc 层尺寸（仍是 12288）
136	- eval_ood：v2 改成 step-0 full-length 模式可以沿用，不变
137	
138	## 7. 待做清单
139	
140	- [ ] `eagle/pipeline/build_prompts_local.py`：v2 老配比 × 50K
141	- [ ] `eagle/pipeline/collect_local.py`：fork `collect_async.py`，删 upload + 本地直写
142	- [ ] 本机采 50K NVFP4 (~2 h)
143	- [ ] `eagle/train.py` 加 NVFP4 dataloader
144	- [ ] 跑训练 + eval_ood，对比 v2 baseline（老层、老数据）
145	- [ ] **若新层 win** → 继续补云端 52K 凑 200K，云训 production ckpt
146	- [ ] **若新层 lose/持平** → 回溯 probe 假设，重选层组合
147	
148	## 8. 文件索引
149	
150	| 文件 | 作用 |
151	|---|---|
152	| `eagle/probe/probe_search.py` | Phase 2/3 linear probe + greedy triple search |
153	| `eagle/probe/probe_results.json` | 层 NLL + best_triple/best_pair 结果 |
154	| `eagle/nvfp4_codec.py` | NVFP4 encode/decode/compress_sample/decompress_sample |
155	| `eagle/validation/validate_nvfp4_storage.py` | bf16 vs NVFP4 存储的训练对比（bit-exact + empirically +0.47%） |
156	| `eagle/pipeline/build_prompts.py` | 200K 扩展配比（v3 云训用） |
157	| `eagle/pipeline/build_prompts_topup.py` | chinese_r1 补齐 51510（passA stride=512 + 新 seed 短 pack） |
158	| `eagle/pipeline/collect_async.py` | 云训管线：aiohttp+NVFP4+BOS 上传 |
159	| `eagle/start_collect.sh` | 数据采集 server（aux=4,9,24，chunked_prefill=131072） |
160	| `eagle/pipeline/build_prompts_local.py` | **TODO**：v2 老配比 × 50K，本机 |
161	| `eagle/pipeline/collect_local.py` | **TODO**：本机采集（no upload） |
162
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/collapse-analysis.md"
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 Accept-rate Collapse 根因分析
2	
3	承接 `docs/eagle/collapse-investigation.md`（"暂判 draft 训练分布问题"，§6 留三条未排除）和 `docs/eagle/eagle-accept-handover-2026-04-26.md`（"未结案"）。本文档基于 **demosala-rollback @ 9a7e04c** 上的**实证 trace** 完成最终诊断。
4	
5	---
6	
7	## 0. 结论速查（TL;DR）
8	
9	- **根因**：pre-EOS 长生成中 49% verify step `accept_len==0`。**纯 draft 能力问题**（v2 在长 context 上 top-2 漏 target argmax）+ **少量 d2t 覆盖缺陷**（英文专有名词 "War"/"Love"/"Letter" 等 target 不在 draft 词表 32K 子集）。**与 backend / KV pool / cuda graph 无关**。
10	- **d2t 结构 miss**：bench 打分场景中 10.12% output token 不在 draft hot_set，其中 89.2% 是 `<unk>`（id=0），1.4% 是 `<|im_end|>`（id=73440），均为结构原因而非 draft 能力问题。修好两者可将 aggregate al 从 1.865 提升至 2.298（+23%）。
11	- **batch-dependent drift**：相同 prompt 在 `batch_size>=2` 下输出第 8 个 generated token 就分歧。**nospec 自己也有**（与 spec / draft 完全无关），是 sglang/flashinfer 在 multi-batch 路径上的 **GPU kernel 数值非确定性**。
12	- **80-token probe 误导**：80 token 内 al≈1.74 只覆盖 step 0-59，错过 step 60+ 的 collapse 段，之前所有基于 80-token 数据的 al 优化方向均偏差。
13	
14	**已排除**：TARGET_VERIFY sparse 路径不等价、handover "hidden state 错配"论断、stale kv suffix（9a7e04c 已 zero-fill）、PLAN_CACHE 跨 mode 错乱、topk/spec_steps/v3 配置层面 fix（±5% 无一消除 collapse）。
15	
16	---
17	
18	## 1. 诊断工具
19	
20	| 文件 | 作用 |
21	|---|---|
22	| `bench/eagle_collapse_probe.py` | 长 generation probe（concurrency × trials），sglang `/generate` `temperature=0 top_k=1 ignore_eos=True`，存 output_ids + meta_info |
23	| `bench/eagle_collapse_analyze.py` | 解析 `EAGLE_TRACE_FILE` jsonl，按 rid 分组 per-step `accept_len` 序列，找连续 al=0 段 |
24	| `bench/eagle_accept_probe.py` | greedy `temperature=0, max_new_tokens=80, ignore_eos=True`，输出 `output_ids` + `meta_info.spec_accept_*` |
25	| `bench/eagle_accept_diff.py` | spec vs nospec 第一个偏离 token |
26	| `bench/eagle_eval_probe.py` | Smax=64 对齐 probe（`CONCURRENCY=64`，stream=False 抓完整 output_ids） |
27	| `bench/eagle_eval_analyze.py` | 离线算 miss / adj_al |
28	| `EAGLE_TRACE_FILE` | sglang 内置 trace（`eagle_info.py:414`），verify event 含 `dt`/`pr`/`t2i`/`t2v`/`hn`/`acc_pred`/`ot` |
29	| env 控制 | `EAGLE_TOPK / EAGLE_SPEC_STEPS / EAGLE_FORCE_NO_ACCEPT / SGLANG_MINICPM_PLAN_CACHE / SGLANG_EAGLE_STRICT_user_4813494d` |
30	
31	---
32	
33	## 2. 单 req 实证（idx 17，pre-EOS 133 步）
34	
35	`max_tokens=2000 ignore_eos=True`。整体 al=1.052，**pre-EOS 段（133 step）**：
36	
37	- al==0: **65/133 (48.9%)**, al==1: 38, al==2: 30 → al_mean=0.737
38	- 最长连续 al==0 run: **10 步**（step 75-84，中文长 deepresearch 流畅段）
39	- collapse 段散布在整个 generation，不是单一中段坍塌
40	
41	每个 al=0 step 检查 target argmax 是否在 draft 可提议子集（`hot_token_id = d2t + arange(32000)`，覆盖 32000/73448 = 43.6% target vocab）：
42	
43	| 类别 | 数量 | 触发 token 例 |
44	|---|---|---|
45	| target OUT of hot_set | **5** | 5231 "War", 10510 "Love", 30010 "Letter", 20090 "iel", 20939 "相识" |
46	| target IN hot_set, NOT in draft top-2 | **60** | 大量中文 deepresearch 续写位置（draft 训练分布盲区） |
47	
48	EOS 后段（step 133-1900，1768 步全 al==0）是 `ignore_eos=True` + `<|im_end|>=73440` 不在 hot_set 的人为现象，不是真 collapse。
49	
50	**single req trial=3 同 prompt → 1 个 sha**（完全 deterministic）。single req 上 collapse **不是随机**，是 prompt-determined。
51	
52	### target logit gap (top1-top2) 分布
53	
54	| al | n | gap p25 | p50 | p75 | mean |
55	|---|---|---|---|---|---|
56	| 0 (collapse) | 96 | 0.94 | 2.75 | 8.25 | 4.28 |
57	| 1 (健康) | 37 | 1.31 | 4.75 | 8.25 | 5.16 |
58	| 2 (满) | 28 | 2.44 | 5.06 | 9.50 | 5.83 |
59	
60	collapse 段 logit gap 比健康段**显著低**（25% step gap < 1.0），其中部分是 target 自身高熵（任何 draft 都难命中），剩余是 draft 真错。
61	
62	### v3 draft 实测：比 v2 更糟
63	
64	切 `EAGLE_DRAFT_MODEL=/user_4813494d/openbmb/eagle/sglang_model_v3` 跑 idx 17 max_tokens=800：
65	
66	| | pre-EOS al==0% | al_mean | longest run |
67	|---|---|---|---|
68	| v2 (current) | 48.9% | 0.737 | 10 |
69	| v3（aux=[4,9,24], NLL -29% per docs） | **59.6%** | **0.578** | 9 |
70	
71	v3 在 long deepresearch 上 collapse 比 v2 更频。docs 报告的 NLL -29% 不对应这个 workload。**切 v3 不修 collapse**。
72	
73	### 80-token mean al 与 long-gen al 严重分歧
74	
75	| | idx 17 80-token al | idx 17 pre-EOS 133-step al |
76	|---|---|---|
77	| 实测 | **1.74** | **0.737** |
78	
79	**80-token probe 的 al 数字**看着不错（80 token 内 al=1.74），但**只覆盖 step 0-59**，错过了 step 60+ 的 collapse 段。**之前所有 mean al 优化（topk、spec_steps、v3 切换）都是基于 80-token 数据，没看到 collapse 段，方向偏了**。
80	
81	---
82	
83	## 3. 全量 Smax=64 量化（benchmark 场景）
84	
85	前述主要基于 idx 17 single-req focused trace。本节换到**真正打分场景**复测，逐项对齐 `toolkit/bench_serving.sh` 参数：
86	
87	| 参数 | bench 打分 | 本轮 probe |
88	|---|---|---|
89	| endpoint | `/generate` | 同 |
90	| prompt | raw text（不套 chat template） | 同 |
91	| `ignore_eos` | True | 同 |
92	| `max_new_tokens` | per-sample = `len(tokenizer.encode(dataset.model_response))`（分布 9-30991, sum=417996）| 同 |
93	| concurrency | Smax = 全 64 同时下发 | 同 |
94	
95	产物：`outputs/eagle_accept/benchlike_smax_20260426_214251/benchlike_smax.jsonl`（64 条）。
96	
97	### 总量
98	
99	- **total output tokens: 416,207**（跑满 per-sample max_new，因为 ignore_eos=True）
100	- **miss（不在 draft hot_set 的 token）: 42,110 = 10.12%**
101	- **aggregate al (raw)**: 1.865
102	- **aggregate al (miss-excluded)**: 2.298（**+23%**）
103	- wallclock 767s = 12.8 min
104	
105	### miss token 高度集中在两个结构 id
106	
107	| token | id | count | 占 total miss |
108	|---|---|---|---|
109	| `<unk>` | 0 | 37,551 | **89.2%** |
110	| `<|im_end|>` | 73440 | 578 | 1.4% |
111	| 其它（英文专名 / 生僻汉字 / url 片段） | ~4,000 | ~9.4% |
112	
113	draft `d2t + arange(32000)` 覆盖 target id 范围 ~[1, 73417]；id 0 (`<unk>`) 和 id 73440 (`<|im_end|>`) **结构上**不在子集。
114	
115	**高 miss 成因**：模型真实回答结束后 `ignore_eos=True` 强迫继续生成 → 退化到 `<unk>` / `<|im_end|>` / 少数标点的循环 → 整个尾段 draft 提议不上 → al 被拉到 ~1.15。这是**bench 打分行为的人为放大**（production `ignore_eos=False`，EOS 自然终止不会出现）。
116	
117	### 高 miss 代表样本
118	
119	| idx | cat | p_tok | max_new | out_len | miss% | unique miss | al | adj_al |
120	|---|---|---|---|---|---|---|---|---|
121	| 16 | 长文本 deepresearch | 10873 | 210 | 210 | **82.9%** | **1** | 1.12 | 15.00 |
122	| 15 | 数学能力 计算 | 127 | 30990 | 30990 | **75.9%** | **4** | 1.15 | 9.26 |
123	| 14 | 文本生成 格式遵循 | 165 | 18688 | 18688 | **75.4%** | **3** | 1.16 | 9.02 |
124	| 17 | 长文本 deepresearch | 15655 | 663 | 663 | 36.3% | 3 | 1.64 | 4.04 |
125	| 1 | 编程能力 代码修改 | 157 | 3934 | 3934 | 14.0% | 5 | 2.18 | 3.13 |
126	
127	`unique`=1-5 关键：idx 16 的 174 个 miss token **全是同一个 id**（post-EOS 单 token 循环）。
128	
129	### adj_al 排名（draft 真实命中率，剔除结构 miss 后）
130	
131	**adj_al bottom（draft 真弱项，全为 p_tok>120K long deepresearch）**：
132	
133	| idx | cat | p_tok | out_len | al | adj_al |
134	|---|---|---|---|---|---|
135	| 62 | 长文本 deepresearch | 132987 | 183 | 1.24 | **1.25** |
136	| 38 | 长文本 deepresearch | 125646 | 373 | 1.24 | **1.26** |
137	| 34 | 长文本 deepresearch | 129033 | 180 | 1.26 | **1.27** |
138	| 33 | 长文本 deepresearch | 130019 | 415 | 1.27 | **1.28** |
139	| 36 | 长文本 deepresearch | 128171 | 475 | 1.28 | **1.30** |
140	
141	**adj_al top（draft 强项，编程/数学/模板化输出）**：
142	
143	| idx | cat | p_tok | out_len | al | adj_al |
144	|---|---|---|---|---|---|
145	| 5 | 编程能力 代码生成 | 632 | 8222 | 2.82 | **2.82** |
146	| 13 | 编程能力 代码生成 | 186 | 30980 | 2.78 | **2.78** |
147	| 28 | 长文本 ? | 23360 | 918 | 2.77 | **2.77** |
148	| 3 | 数学能力 数列 | 25 | 3286 | 2.72 | **2.72** |
149	| 7 | 编程能力 代码生成 | 816 | 30907 | 2.68 | **2.68** |
150	
151	### per-category 统计
152	
153	| cat1 | n | avg_out_len | miss% | 典型 al | 备注 |
154	|---|---|---|---|---|---|
155	| 编程能力 | 12 | 20930 | **0.34%** | 2.3-2.8 | draft 强项，几乎无 `<unk>` 退化段 |
156	| 长文本 | 49 | 2287 | 3.25% | 1.2-1.7 | draft 弱项（长 context 分布） |
157	| 数学能力 | 2 | 17138 | 68.6% | — | idx 15 尾段全 `<unk>` |
158	| 文本生成 | 1 | 18688 | 75.4% | — | idx 14 尾段全 `<unk>` |
159	
160	### 可修空间量化与方案对比
161	
162	bench 打分场景下，修好 `<unk>` + `<|im_end|>` 两个结构 miss 的上限收益：aggregate al 从 **1.865 → 2.298**（+23%），throughput 线性受益。**不能根治 long deepresearch 的 draft 弱项**（adj_al=1.24-1.30 独立于 `<unk>`，是训练分布问题）。
163	
164	| 方案 | 工程量 | 是否破红线 | 覆盖 | 备注 |
165	|---|---|---|---|---|
166	| C1: lm_head 扩 2 dim (32000→32002) + 微调 | 中 | **破**（动 draft ckpt）| `<unk>` + `<|im_end|>` | 只改 d2t 不工作 |
167	| **C2**: runtime post-EOS / `<unk>`-loop detect → 该 req 退 nospec | 小 | **不破** | 退化段 draft + verify dtn=5 overhead | detect 规则：最近 K=3 commit token ∈ {0, 73440} 或最近 K=5 步 al=0；false positive 几乎不可能 |
168	| C3: 接受现状 | 0 | 不破 | 0 | bench 打分场景 -23% al 是工程债 |
169	
170	> **后续更新（2026-04-27）**：rope_theta=1M 实验落地后，long context（p_tok>50K）bucket adj_al +44.9%（全量 64 样本，concurrency=64），是另一条红线内零重训收益。C2 和 rope_theta=1M 两条路可并行。详见 [`verify-experiments-log-20260427.md`](verify-experiments-log-20260427.md) §1。
171	
172	---
173	
174	## 4. Batch drift 实证
175	
176	### single req 多次 trial → deterministic
177	
178	idx 17 max_tokens=200, concurrency=1, trial=3 → **3 次同 sha**，同 al=1.724 verify_ct=116。
179	
180	### concurrency>=2 → 分歧
181	
182	idx 17 max_tokens=200，**同 prompt × N slot 并发**：
183	
184	| concurrency | unique sha | per-slot al |
185	|---|---|---|
186	| 1 | 1 | 1.724 |
187	| 2 | 2 | 1.613 / 1.739 |
188	| 4 | 4 | 1.626 / 1.667 / 1.724 / 1.639 |
189	| 8 | 6 | 1.107-1.144 (max_tokens=800) |
190	
191	**第一个分歧 token 的位置**（nospec c=4 max_tokens=800）：output token 8（即模型回答的第 8 个新生成 token）。slot 0/3 输出"这部电影"，slot 1/2 输出"我们可以"。
192	
193	### 排除假设
194	
195	| 假设 | 实测 | 结论 |
196	|---|---|---|
197	| cuda graph 引入非确定 | `--disable-cuda-graph` c=2 仍分歧 | 不只是 cuda graph |
198	| flashinfer split-KV 非确定 | `SGLANG_MINICPM_VERIFY_DISABLE_SPLIT_KV=1` c=2 仍分歧 | 不只是 split-KV |
199	| spec/draft 引入 | **nospec c=4 也产生 4 个不同 sha** | **与 spec 完全无关**，是 sglang/flashinfer multi-batch 路径自身的数值非确定 |
200	| topk/spec_steps 配置 | chain/v3/spec3/topk3 实测 mean al ±5%，无一消除 collapse 或 drift | 配置层面无 fix |
201	
202	### batch drift 与 collapse 的关系
203	
204	batch drift 让每个 slot 走不同的 generation path → 每个 slot 在不同 token 位置碰到 draft 盲区 → collapse 段触发位置/长度不同。这就是"collapse 不固定何时发生"——**抖动不是 collapse 本身随机，是 batch drift 让 prompt 路径分叉**。single req 上 collapse 是 prompt-determined（同 prompt 必然在同位置 collapse）。
205	
206	---
207	
208	## 5. 配置搜索实验（config A–E）
209	
210	### 基线数据（current best baseline）
211	
212	**default EAGLE（topk=2, spec_steps=2, dtn=5）vs 4-26 historical**：
213	
214	| idx | task | p_tok | 4-26 al | now al | 改善 |
215	|---|---|---|---|---|---|
216	| 16 | deepresearch | 10873 | 1.333 | **1.778** | +33% |
217	| 17 | deepresearch | 15655 | 1.311 | **1.739** | +33% |
218	| 49 | "?" | 64399 | 1.081 | **1.404** | +30% |
219	
220	al 30%+ 改善来自两项改动：(1) SimpleGLA direct-state decode wired，(2) `.so` 换为 `220c18cc`（draft cuda graph capture 通过）。
221	
222	**全 64 分桶 baseline（config A）**：
223	
224	| bucket | n | task | al p50 |
225	|---|---|---|---|
226	| short <1K | 14 | 代码生成/数列/计算/格式/代码修改 | **1.86-2.29** |
227	| mid 1-8K | 1 | 代码生成 | 2.424 |
228	| long 8-50K | 18 | deepresearch / "?" | 1.509-1.538 |
229	| vlong >50K | 31 | deepresearch / "?" | 1.379-1.404 |
230	
231	全 64 mean=1.566，p50=1.481，max=2.424，min=1.194。**al 与 prompt length 单调反相关**：short al ~1.86-2.42，vlong deepresearch al ~1.38。
232	
233	### config A–E 结论表格
234	
235	| config | 参数 | 全 64 mean | long 8-50K p50 | vlong p50 | 结论 |
236	|---|---|---|---|---|---|
237	| A（baseline） | topk=2, spec_steps=2, dtn=5 | **1.566** | 1.538 | 1.379 | 当前生产 |
238	| B（chain） | topk=1, spec_steps=2, dtn=3 | 1.435（**-0.13**） | 1.311（-0.093） | — | 全面差，丢弃 |
239	| C（v3 draft） | aux=[4,9,24], 200K, NLL -29% | 1.566（**±0.000**） | 1.536（-0.015） | 1.335（**-0.039**） | short +0.10 但 vlong 退，整体持平；不是 long fix |
240	| D（spec_steps=3） | topk=2, spec_steps=3, dtn=7 | 1.604（+0.038） | 1.600（+0.049） | 1.388（+0.014） | long latency +0.3%（dominated by prefill），short latency +7.2%（净 throughput -9%）；不作 default，可做长 prompt routing |
241	| E（topk=3） | topk=3, spec_steps=2, dtn=7 | — | — | — | in flight，未完成 |
242	
243	---
244	
245	## 6. 已废弃调查路径
246	
247	**从 handover 继承的错误假设**：
248	- **handover "TARGET_VERIFY 走 sparse"**：dense vs sparse logit 不影响 spec 内部 accept rate（target argmax 取自 dense forward 自己），只影响 spec output ≠ nospec output（user 不要求 bit-identical）。accept rate 已从 1.0-1.3 改善到 1.38-1.54，根因是 SimpleGLA + .so 修复，不是 TARGET_VERIFY 路径。
249	- **handover "hidden state 错配"论断**：deeper accept 时 child verify forward 输入 token = `candidates[child]` = `target_predict[parent]`（accept condition），prefix 与 commit 完全一致，hidden state 自洽。`force_no_accept=1` 长生成与 nospec 前 134 token 完全一致是旁证。handover 结论不成立。
250	
251	**strict_user_4813494d patch 机制（实测退化为 force_no_accept）**：
252	
253	在 `eagle_info.py:391-413` 加判断 `predict_2d[:, 0].ne(candidates[:, 0])` 的 strict-user_4813494d gate 完全错误：`candidates[:, 0]` 是 `verified_id`（已 commit 的最后 token），`predict[:, 0]` 是 target 的 next-token argmax，两者按设计永远不等。patch 等价于 `EAGLE_FORCE_NO_ACCEPT=1`，accept rate 全跌至 1.01-1.10（全 64 mean=1.033，p50=1.026）。已回滚。
254	
255	**其它已排除路径**：
256	- **1608d18 "stale kv suffix"**：9a7e04c 已有 `verify_kv_indices_active_pages` zero-fill 逻辑（minicpm_backend.py:2307-2316），1608d18 主要是 python loop → Triton 性能改写，语义等价，不修 collapse。
257	- **PLAN_CACHE 跨 mode 错乱**：plan_cache 只在 decode_wrapper（minicpm_attention_kernels.py:534），verify 走 prefill_wrapper 不进 plan_cache，关闭后 idx 49 仍 t=8 偏离。
258	- **topk=1/3 / spec_steps=3 / v3 draft**：mean al ±5%，long-gen collapse 频率与 default 同量级，无一消除。
259	
260	---
261	
262	## 7. 连续坍缩机制
263	
264	User 提的关键问题：target argmax 翻一下，下一步只是少 1 个 token，spec 应当能恢复——但实测 idx 17 一进入 collapse 段就**连续 10+ 步全 al=0**。
265	
266	### 先排除两个看似合理但实测不成立的 contagion
267	
268	**(a) "翻转后 KV cache 错位污染"** — 不成立。
269	- 9a7e04c 已有 `verify_kv_indices_active_pages` zero-fill 逻辑（minicpm_backend.py:2307-2316），shrink 时 suffix 清零。
270	- al=0 时 evict_mask 把未接受的 candidate 的 KV slot 加回 free pool；下次 verify 的 `kv_indptr` 是按 commit 序列重新构造的，不会读到被 evict 的 slot。
271	- spec 内部 KV 是 **commit-aligned** 的，整条 generation 上 spec 自己看到的 prefix 与 commit 序列严格一致。
272	
273	**(b) "翻转后 draft 收到的 hidden state 是错前缀的"** — 不成立。
274	- al=0 时 commit 1 token = `target_predict[user_4813494d]`；user_4813494d 位置的 hidden state 在 verify forward 中是用 `verified_id`（上一步 commit 的最后 token）作为 input 跑的，attention prefix = 真正的 commit 序列。
275	- 下一步 draft 的 hidden 输入 = 该 user_4813494d hidden（来自正确 prefix）+ token id = commit token；二者对齐。
276	- al>=1 时 deeper accept 的 hidden state 同样自洽，因为 accept 条件 `candidate(child) == target_predict(parent)` 保证 verify forward 中 child 位置的 input 等于实际 commit token。
277	
278	实测旁证：`force_no_accept=1` 长生成与 nospec 在前 134 token 完全一致——如果 spec 内部 KV/hidden 真有 contagion，长 generation 不可能与 nospec **token-level 一致**。
279	
280	### 真因：翻转把 prefix 推入 draft 训练分布的"连续盲区"
281	
282	draft 是个独立的小 model，训练分布有限。在长 deepresearch 这种语义模板上（比如"...这部电影是中国历史战争**剧情片**，改编自清末四大奇案之一的'刺马案'..."），**连续多个位置都是 draft 训练数据未充分覆盖的语境**。每个位置 draft 的 top-2 都漏掉 target argmax → 连续 al=0。
283	
284	单点"翻转"在这条机制里的角色：
285	- 某次 verify 中 target 在高熵位置（collapse 段 p50 logit gap=2.75，健康段 p50=4.75）把 argmax 选到 token A 而不是 B。
286	- 翻转后 spec 走上"以 A 为前缀"的语义路径。
287	- 如果这条路径**整段都是 draft 盲区**（draft 训练时没见过类似 prefix → next-token 的映射），则整段连续 collapse。
288	- 翻转**不是 collapse 的"病因"**，而是"路径分支器"——把 spec 引向了一条 draft 盲区路径。
289	
290	**恢复机制**：当 target commit 走到语义边界（标点 "。" / 连接词 / 数字 / 模板化短语），prefix 重新落入 draft 熟悉的分布，accept 立即恢复。collapse 段总是被低熵、模板化的 token 终结。
291	
292	### 三个实测旁证
293	
294	1. **collapse 段 target 自己也犹豫**：al=0 段 logit gap p50=2.75，健康段 p50=5.06。target 的不确定与 draft 失败强相关。
295	2. **collapse 段 target 输出仍合理**：spec 在 collapse 段 commit 的 token 与 nospec 同位置一致（前 134 token），输出文本流畅。target 没"乱"，**spec 没"卡死"**。
296	3. **跨 prompt 差异巨大**：idx 14 (165 short, 格式遵循) long-gen al=2.09 / 0 collapse；idx 17 (15K, deepresearch) al=1.05 / 多个 >=10 步 collapse；idx 56 (136K, deepresearch) al=1.88 / 3 个 >=10 步 collapse。**与 prompt 长度不单调，与 prompt 内容（draft 训练分布覆盖度）强相关**。
297	
298	---
299	
300	## 8. 修复路径
301	
302	### A. collapse（draft 能力）
303	
304	| 选项 | 工程量 | 是否破红线 | 状态 |
305	|---|---|---|---|
306	| **A1**：重训 draft（扩长 deepresearch / reasoning 训练数据） | 大 | **破** | 非本次 scope |
307	| **A2**：扩 d2t（让 hot_token_id 覆盖 73448 全 vocab，含英文专有名词 + special tokens） | 需 lm_head 同步重训 | **破** | 非本次 scope |
308	| **A3**：runtime collapse skip — 连续 K=5 步 al=0 → 该 req 暂停 spec 走纯 nospec N=20 步 → 恢复 | 中等（按 req mask batch 复杂） | **不破** | P0 提议，未实现。治标：cap collapse 段 verify dtn=5 overhead；单 req 省 ~3-4x verify forward 时间；多 req mask 复杂 |
309	| **A4**：接受现状 + 文档化（instrumentation 已落地） | 0 | 不破 | **已完成** |
310	
311	### B. 结构 miss（`<unk>` + `<|im_end|>`，bench 打分 -23% al）
312	
313	| 选项 | 工程量 | 是否破红线 | 状态 |
314	|---|---|---|---|
315	| **C2**：runtime post-EOS / `<unk>`-loop detect → 该 req 退 nospec | 小（`eagle_worker.py` 加 per-req counter） | **不破** | 推荐实施，detect 规则稳定性高 |
316	| C1: lm_head 扩 2 dim + 微调 | 中 | **破** | 非本次 scope |
317	
318	### C. batch drift（kernel 非确定）
319	
320	| 选项 | 工程量 | 状态 |
321	|---|---|---|
322	| **B1**：接 `enable_deterministic_inference` 到 minicpm_flashinfer + minicpm_attention_kernels | 大 | 实测仅给 verify_wrapper.plan 加 disable_split_kv 不够，drift 还有其它源（mamba2 GLA、sparse top-k、layer norm reduction 等）。完整接入是大工程 |
323	| **B2**：`--max-running-requests 1` | 0 | 吞吐崩，不可用 |
324	| **B3**：接受现状 + 文档化 | 0 | **已完成** |
325	
326	### 已落地的非 functional 改动
327	
328	- `eagle_info.py` 加 `_COLLAPSE_COUNTERS` instrumentation：每 req 维护 `consec_al0` 计数，到达 `EAGLE_COLLAPSE_LOG_K`（默认 10）emit `[eagle-collapse]` warning，纯监控，不改 spec 行为。
329	- `minicpm_backend.py` verify_wrapper.plan() 两处加 `disable_split_kv`，通过 `SGLANG_MINICPM_VERIFY_DISABLE_SPLIT_KV` env 控制（默认 0）。实测不消除 c=2 batch drift，留作后续 deterministic 全栈接入时复用。
330	
331	---
332	
333	## 关键代码锚点
334	
335	- `bench/data/speed_bench_cunlimited.jsonl`：64 条数据集
336	- `outputs/eagle_accept/collapse_*/`：诊断 trace（多个时间戳子目录）
337	- `outputs/eagle_accept/benchlike_smax_20260426_214251/benchlike_smax.jsonl`：Smax=64 全量 raw
338	- `/tmp/benchlike_smax_analyze2.log`：完整 adj_al rank 表
339	- `/tmp/eagle_trace.jsonl`：最新 EAGLE_TRACE_FILE 输出
340	- `demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py:414-457`：trace verify event 写入
341	- `demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_backend.py:1964-1977 / 2364-2380`：verify_wrapper.plan() 两处（capture / replay）
342	- `demo-sala/sglang/python/sglang/srt/models/llama_eagle3.py:250-253`：`hot_token_id = d2t + arange` 加载逻辑
343	- `demo-sala/data/eagle_draft/model.safetensors`：v2 draft（d2t shape=(32000,) range=[1, 41418]，hot_token_id 覆盖 32000/73448=43.6%）
344	- `eagle/sglang_model_v3/`：v3 draft（aux=[4,9,24]，long-gen collapse 反而比 v2 更糟）
345
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/experiments-log.md"
}
```

> TOOL

tool_result Read
```
1	# 验证实验进度日志 — 2026-04-27
2	
3	三方向验证：rope_theta / Phased Verify / STree 并行 GLA state
4	计划来源：`/user_4813494d/.claude/plans/composed-jingling-marshmallow.md`
5	
6	---
7	
8	## 方向一：rope_theta=1M 实验 — ✅ 完成（已落 production config）
9	
10	### A/B 对照结果（同环境 concurrency=9，同 9 个样本）
11	
12	| idx | 类别 | p_tok | al_base | al_1M | Δlat(s) |
13	|---|---|---|---|---|---|
14	| 32 | 长文本/deepresearch | 130308 | 1.363 | **2.174** | -1.51 |
15	| 33 | 长文本/deepresearch | 130019 | 1.309 | **2.331** | -2.63 |
16	| 34 | 长文本/deepresearch | 129033 | 1.233 | **1.978** | -1.19 |
17	| 36 | 长文本/deepresearch | 128171 | 1.405 | **2.093** | -2.23 |
18	| 38 | 长文本/deepresearch | 125646 | 1.243 | **2.156** | -2.44 |
19	| 62 | 长文本/deepresearch | 132987 | 1.253 | **2.205** | -1.36 |
20	| 1  | 编程/代码修改 | 157 | 2.356 | 1.425 | +10.83 |
21	| 5  | 编程/代码生成 | 632 | 2.698 | 2.425 | +3.21 |
22	| 7  | 编程/代码生成 | 816 | 2.465 | 2.522 | -2.32 |
23	
24	**adj_al（来自 eagle_eval_analyze.py，剔除结构 miss）：**
25	
26	| idx | adj_base | adj_1M | Δ |
27	|---|---|---|---|
28	| 34 | 1.25 | 2.05 | **+0.80** |
29	| 36 | 1.41 | 2.11 | **+0.70** |
30	| 38 | 1.29 | 2.22 | **+0.93** |
31	| 32 | 1.38 | 2.25 | **+0.87** |
32	| 62 | 1.29 | 2.44 | **+1.15** |
33	| 33 | 1.33 | 3.88 | **+2.55**（高 miss% 略噪）|
34	| 1  | 3.65 | 1.50 | -2.15 |
35	| 5  | 2.70 | 2.43 | -0.27 |
36	| 7  | 2.47 | 2.52 | +0.05 |
37	
38	### 分析结论
39	
40	- **长 deepresearch（120K–133K）**：al 提升 56%–78%，每个样本快 1–3s
41	- **短 coding（idx 1, 157 tokens）**：al 退化，慢 +10.83s
42	- **长 coding（idx 7, 816 tokens，30907 output）**：al 持平或微升，快 -2.32s
43	
44	**Benchmark critical path 分析**：Smax=64 下 duration = max latency。
45	- idx 7（30907 output tokens）是最长请求，rope_theta=1M 使其加速 -2.32s ✓
46	- idx 1（3934 output tokens）变慢 +10.83s，但在 idx 7 仍在跑时它已完成，**不影响 critical path**
47	- 净效果：benchmark duration 应有小幅改善
48	
49	**理论机制**：rope_theta=10000 在 130K 位置外推比 ~64×，导致 sin/cos phase 周期折叠，draft attention 对长距 token pair 的 score 退化。rope_theta=1M 将 period 延伸使 phase 在 130K 内不折叠，draft 在这些位置的预测恢复正常。短 coding 退化是因为 draft 权重学到的是 theta=10000 的 frequency pattern，inference 时换 theta 破坏了 0–1K 范围内的 learned attention pattern。
50	
51	**落地状态**：
52	- `demo-sala/data/eagle_draft/config.json` ← `"rope_theta": 1000000` 已写入
53	- `eagle/sglang_model/config.json` ← 同步更新
54	
55	### 全量 A/B Probe（64 样本，concurrency=64）— ✅ 完成
56	
57	**结果文件**：`outputs/eagle_accept/rope_theta_full_20260427/rope1M.jsonl` vs `theta10k.jsonl`
58	
59	| 分组 | n | al_10k | al_1M | Δal | 说明 |
60	|---|---|---|---|---|---|
61	| 长 context（p_tok>50K） | 31 | 1.395 | 2.022 | **+0.627（+44.9%）** | 近全部样本提升 |
62	| 短/中 context（p_tok≤50K）| 33 | 1.972 | 2.072 | +0.100（+5.1%） | 基本持平，轻微正向 |
63	| **全量平均** | **64** | — | — | **+0.356** | |
64	
65	- 长 context 每样本快 1.5–16s，31 个长样本中 29 个正向（2 个微负：idx 48 -0.14，idx 51 -1.04）
66	- mini_bench：S1=242.98s，S8=328.69s，Smax=604.58s（theta=1M；theta=10000 为不同样本集，不可直接对比）
67	
68	**结论：rope_theta=1M 对全量 benchmark 有实质正向影响，config 保留。**
69	
70	---
71	
72	## 方向二：Phased Verify 离线分析 — ✅ 完成
73	
74	### 结论
75	
76	| trace 来源 | 总 steps | early_exit% | 误报 | 理论 token 减少 |
77	|---|---|---|---|---|
78	| final_check_20260426 | 7205 | **71.5%** | 0 | **28.6%** |
79	| stability_rootcause_20260426 | 4936 | **68.8%** | 0 | ~27% |
80	| /tmp/eagle_trace.jsonl（full bench run） | 264728 | **48.6%** | 0 | ~19% |
81	
82	**Full bench trace 按 bucket 分解：**
83	
84	| bucket | steps | avg_al | early_exit% |
85	|---|---|---|---|
86	| short_<1K | 9498 | 1.142 | 26.5% |
87	| mid_<8K | 45950 | 1.347 | 21.8% |
88	| long_<50K | 127333 | 0.872 | **47.3%** |
89	| vlong_>=50K | 81947 | 0.400 | **68.3%** |
90	
91	- Phase-1 check（`pr[0] ∉ {dt[1], dt[2]}`）100% 准确，零误报
92	- vlong bucket（处理我们的 deepresearch 长 prompt 输出）early exit 率 **68.3%**
93	- 代码改动估计：~200 行，主要文件：
94	  - `demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py`（verify() 拆两阶段）
95	  - `demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py`（KV slot 分段分配）
96	  - `demo-sala/sglang/python/sglang/srt/speculative/eagle_utils.py`（部分树 verify）
97	- CUDA graph 适配是主要风险：TARGET_VERIFY 需 capture 两种形状（3 tokens / 2 tokens）
98	
99	**分析脚本：** `bench/phased_verify_analyze.py`
100	
101	---
102	
103	## 方向三：STree 并行 GLA state — ✅ 完成（结论：不值得改）
104	
105	### 结论
106	
107	- GLA state rollback 已正确实现（`_fused_recurrent_gla_intermediate_kernel` + `update_mamba_state_after_mtp_verify`）
108	- `_fused_recurrent_gla_intermediate_kernel` 内 `retrieve_parent_token` 实现了等效于 STree A-matrix 累乘的 tree topology state 传播
109	- kernel 串行 step loop（dtn=5 次），理论上可并行为 3 轮，但：
110	  - verify bottleneck 是 FlashInfer prefill（32 层 attention），GLA state 计算占比小
111	  - dtn=5 的串行开销微不足道
112	- **结论：不值得重写 kernel**
113	
114	---
115	
116	## 综合优先级（最终）
117	
118	| 方向 | 状态 | 实测收益 | 推荐 |
119	|---|---|---|---|
120	| rope_theta=1M | ✅ 已落地 | 长 context al +56–78%，benchmark 中性或略正 | 已完成 |
121	| Phased Verify | 技术可行 | 理论 -28.6% token 计算量，实际收益需 bench 验证 | 下一步实施 |
122	| STree 并行 GLA | 不推进 | ROI 低（bottleneck 不在 GLA state 计算）| 关闭 |
123	| **MARS（θ=0.85）** | **✅ 初步验证** | 吞吐可观测提升，eval 分数无可观测下降 | 保留，待精调 |
124	
125	---
126	
127	## 方向四：MARS（Margin-Aware Relaxed Speculative Verification）— ✅ 初步验证
128	
129	### 方法
130	
131	论文 arXiv:2601.15498（ICLR 2026）。对每个 draft token：
132	1. `v_t == top-1` → 直接接受（原有行为）
133	2. `v_t == top-2` 且 `z_(2)/z_(1) > θ` → 放宽接受（MARS 新增）
134	3. 否则拒绝
135	
136	Training-free，仅改 verify 规则，完全兼容 tree verify。
137	
138	### 论文数据
139	
140	θ=0.90（论文推荐值，扫描范围 [0.84, 0.96]）：
141	
142	| 模型 | EAGLE-3 加速 | MARS 加速 | τ 提升 |
143	|---|---|---|---|
144	| Vicuna-13B | 3.12x | 3.74x | +27.7% |
145	| Llama-3.1-8B | 3.24x | 4.00x | +37.2% |
146	| Llama-3.1-70B | 4.40x | 4.76x | +12.9% |
147	| Qwen3-8B | 2.96x | 3.23x | +18.4% |
148	
149	质量退化（θ=0.90）：BLEU 差 0.04，ROUGE-L 差 0.0008，MT-Bench 差 <0.18 分——统计噪声范围内。
150	θ < 0.88 开始有可测量退化；θ=0.5 论文未测试。
151	
152	**无理论散度保证**（论文定位为 lossy variant，以实证为依据）。
153	
154	### 本机实测结论（2026-04-27）
155	
156	**θ=0.85：吞吐可观测提升，eval 分数无可观测下降。**
157	
158	- 论文 sweep 最低至 θ=0.84，θ=0.85 为我们扩展验证的更激进点
159	- 论文预测 θ<0.88 有可测量质量退化，但在 MiniCPM-SALA 生产 eval 中**未观测到分数下降**
160	- 可能原因：NVFP4 量化后 logit ratio 分布更集中，θ=0.85 在我们的模型上仍处于安全区间
161	- **当前推荐 θ=0.85**（实测优于论文推荐的 0.9），后续需更系统 bench 确认
162	
163	### 本机工程实现
164	
165	**改动清单（2026-04-27）**：
166	
167	| 文件 | 改动 |
168	|---|---|
169	| `sgl-kernel/csrc/speculative/eagle_utils.cu` | `VerifyTreeGreedy` kernel 8→11 参数，先 exact match 后 MARS fallback |
170	| `sgl-kernel/csrc/common_extension.cc` | PyTorch op schema 11 参数（3 新参数可选） |
171	| `sgl-kernel/include/sgl_kernel_ops.h` | 同步 C++ 头 |
172	| `sgl_kernel/speculative.py`（venv） | Python wrapper 转发新参数 |
173	| `demo-sala/sglang/.../eagle_utils.py` | 加 `target_predict.contiguous()`（必须，server 中为非连续 view） |
174	| `demo-sala/sglang/.../eagle_info.py` | verify 循环 EOS 检测，红色 ANSI 日志 |
175	
176	**重要约束**：rebuild 必须用 `gptq_marlin.cu` Feb 21 版（37KB）。Apr 25 版（44KB，新增 `workspace_blocks_per_sm` 动态参数）导致 EAGLE draft graph capture 在 bs=8 挂住。已回退，备份在 `gptq_marlin.cu.apr25.bak`。
177	
178	**启动方式**：`EAGLE_MARS_THETA=0.85 bash eval/start_eagle.sh`（默认 θ=-1.0 = MARS 关闭）
179	
180	### 已验证
181	
182	- sanity test（3 cases：legacy 8-arg / MARS hit r=0.95>θ / MARS reject r=0.5<θ）全部通过
183	- server 可起，smoke test 正常（人话输出，finish_reason=stop）
184	- EOS 红色日志功能就位
185	
186	### 待完成
187	
188	- [x] e2e bench：θ=0.85 初步验证，吞吐提升 + eval 分数无下降
189	- [ ] 系统 bench：mini_bench + full bench，量化 θ=0.85 vs off 的具体数字
190	- [ ] θ 精调：扫描 θ ∈ {0.80, 0.85, 0.88, 0.90}，找 MiniCPM-SALA 上的最优点
191	- [ ] 长 context 专项（deepresearch 样本，p_tok>50K）：MARS 在 low-accept 区域应有更大收益
192	
193	---
194	
195	## 第五轮：候选方向纸面调查（4-agent 并行，2026-04-27）
196	
197	4 个 subagent 并行精读论文，覆盖 GOOSE / SMART / RACER / Cactus / BanditSpec / FASER，以确认 greedy 兼容性和 batch=1 ROI。
198	
199	### 淘汰方向
200	
201	#### ❌ SMART（arXiv:2604.09731）— batch=1 无收益，淘汰
202	
203	**结论**：SMART 的核心价值是在大 batch compute-bound 场景防止树过展开的负收益。**batch=1 baseline 2.20× vs SMART 2.17×**，与 baseline 持平甚至微负。
204	
205	我们的场景（bs=1 decode，64 并发但 spec 在 decode 路径是独立请求逐个验证）不符合 SMART 的设计假设。
206	
207	#### ❌ Cactus（arXiv:2604.04987）— T=0 greedy 不兼容，淘汰
208	
209	**结论**：Cactus 接受规则 `gamma* = min{q(n) + sqrt(2δ·q(n)·(1-q(n))), 1}`，其中 q(n) 是 target 对 draft token n 的概率。
210	
211	在 T=0 greedy 下：target argmax token n* 的 q(n*)=1，其余 q(n≠n*)=0，因此：
212	- n = n*（draft 猜对）：gamma*=min{1+0,1}=1，接受
213	- n ≠ n*（draft 猜错）：gamma*=min{0+0,1}=0，拒绝
214	
215	**退化为精确 exact-match**，与当前 `verify_tree_greedy` 行为完全等价，零额外收益。
216	
217	### 确认候选方向
218	
219	#### ✅ GOOSE — 各向异性推测树（arXiv:2604.02047, 2026.04）
220	
221	**Greedy 兼容**：设计目标就是 T=0 greedy。核心定理不依赖概率分布，只需估算每个候选来源的 acceptance rate，可从离线统计或 in-context 滑窗获取。
222	
223	**核心机制**：观察到两种 token 来源（n-gram context match vs. 统计预测）的接受率中位数差距 **6×**（范围 2–18×）。最优树应该各向异性：高接受率的 context-matched token 形成深链（spine），低接受率统计预测 token 作为宽分支。
224	
225	**实验结果**：5 个 LLM（7B–33B）比 balanced-tree baseline 提升 **12–33%**。deepresearch 长 pattern 是高接受率 n-gram 的典型场景，在我们的 workload 上预期偏高端。
226	
227	**工程成本**：
228	- PLD n-gram lookup：prefix lookup deduplication，需维护 `{ngram_key → token_id}` 的 LRU 缓存
229	- Bigram adjacency matrix：按 token 对统计条件概率，可从 eval dataset 离线预计算，约 32000×32000 稀疏矩阵（热词覆盖 99%）
230	- 树构建逻辑嵌入 draft generation 步骤，约 200–300 行 Python + 离线统计脚本
231	
232	#### ✅ RACER — AC 自动机检索树（arXiv:2604.14885, 2026.04）
233	
234	**Greedy 兼容**：论文主实验均为 T=0，AC 自动机匹配是确定性操作，完全兼容。
235	
236	**核心机制**：用 Aho-Corasick 自动机索引已生成 token 序列，快速检索当前 prefix 对应的历史续写 candidates。LRU 淘汰控制内存使用。与 logits draft tree 融合：ngram 候选走检索分支，logits 候选走标准 EAGLE draft 分支。
237	
238	**实验结果**：deepresearch 长文本 MAT（Mean Accepted Tokens）提升 **+0.5–0.76**。特别适合长重复 pattern（deepresearch 中"根据搜索结果…"类模板），是 EAGLE 的互补而非竞争。
239	
240	**工程成本**：CPU-only，不占 GPU 时间。约 **400 行 Python**，嵌入现有 draft generation 流程（`eagle_worker.py` draft 阶段前插入 AC lookup）。是候选中实现成本最低的。
241	
242	#### ✅ BanditSpec — 自适应推测步数（arXiv:2505.15141, 2026）
243	
244	**Greedy 兼容**：信号 = accept_length（整数），与概率分布无关。UCB 臂选择是纯整数运算。完全兼容 greedy。
245	
246	**核心机制**：每个请求维护独立 UCB 多臂老虎机，arms = `{dtn=3, dtn=5, dtn=7}`。每完成一个 verify step，reward = accept_length，更新对应 arm 的 UCB 统计量，下一步选择 UCB 值最大的 arm。
247	
248	**为什么对我们有效**：
249	- vlong bucket（p_tok≥50K）当前 avg_al=0.40，dtn=5 等效效率只有 **8%**（每 5 token verify 成本只换 0.4 token 进展）
250	- 若 BanditSpec 学会在 vlong 收敛到 dtn=3，效率提升到 **13%（+63% 相对）**
251	- 编程 bucket（avg_al~2.5）dtn=5 效率 50%，dtn=7 可能更好；UCB 自动发现最优
252	
253	**工程成本**：约 **100 行 Python**，`eagle_worker.py` 中增加 per-req state dict `{rid → UCBArm}`。per-req overhead 极低（一次加法+比较）。是候选中**实现成本最低**的。
254	
255	---
256	
257	## 综合优先级（更新至 2026-04-27 第五轮）
258	
259	| # | 方向 | 状态 | 实测/预估收益 | 推荐 |
260	|---|---|---|---|---|
261	| — | rope_theta=1M | ✅ 已落地 | 长 context al +44.9%（p_tok>50K）| 已完成 |
262	| — | MARS θ=0.85 | ✅ 初步验证 | 吞吐可观测提升，eval 分数无下降 | 保留，待系统 bench |
263	| — | STree 并行 GLA | ❌ 不推进 | ROI 低，bottleneck 不在 GLA state | 关闭 |
264	| — | SMART | ❌ 淘汰 | batch=1 无收益（2.17× vs baseline 2.20×）| 关闭 |
265	| — | Cactus | ❌ 淘汰 | T=0 退化为 exact-match，零额外收益 | 关闭 |
266	| 1 | **Phased Verify** | 离线分析✅，代码未改 | 理论 -28.6% verify token，vlong early-exit 68.3% | **优先实施** |
267	| 2 | **BanditSpec** | 未实施 | vlong dtn 自适应，est +20–35% mixed workload | 低成本，建议并行 |
268	| 3 | **GOOSE** | 未实施 | +12–33% vs balanced tree（deepresearch 预期上端）| 中等成本 |
269	| 4 | **RACER** | 未实施 | deepresearch MAT +0.5–0.76 | 低成本，互补 GOOSE |
270
```

> DEVELOPER

你在 /user_4813494d/openbmb 工作区，这是一个 SOAR 2026 LLM 推理优化比赛仓库，优化 MiniCPM-SALA 模型推理（硬件：NVIDIA RTX 6000D, sm_120 Blackwell, 84GB VRAM）。请深入调查量化和 kernel 相关的所有技术工作。

重点读取：
1. docs/quantization.md
2. docs/kernels-sm120.md
3. docs/marlin-tuning.md
4. docs/nvfp4-kv-investigation.md
5. docs/runtime.md
6. demo-sala/sglang/python/sglang/srt/ 下与量化相关的文件（modelopt_quant.py, marlin_utils_fp4.py 等）
7. git log 中所有 b12x、marlin、NVFP4、quant 相关提交

请特别关注：
- NVFP4 KV Cache 调研结论（为什么最终放弃，具体技术障碍）
- b12x 2-tier dispatch 的设计和效果（具体形状、tile 配置、性能提升数字）
- FourOverSix 量化方案是什么
- Marlin FP4 scale bug fix 内容
- scale loader bug（QKV fused per-tensor scale 污染）的完整故事
- sm_120 上各 GEMM 库的实测性能对比
- 生产配置的最终决策及原因

请给出一份详细的技术摘要，包括具体数字、负结果和实现细节。

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/longcontext-analysis.md"
}
```

> TOOL

tool_result Read
```
1	# 长上下文推测解码（Speculative Decoding）综述
2	# —— 问题现象、学术根因与 MiniCPM-SALA 实测结合分析
3	
4	> 写作时间：2026-04-27  
5	> 适用对象：SOAR/MiniCPM-SALA EAGLE-3 推测解码优化团队  
6	> 依据：本轮多 agent 学术调研（≥14 个 subagent）+ 本仓库实测 trace（`collapse-rerun-20260426.md` §1–11）  
7	> 本文档**不**重复 `collapse-rerun-20260426.md` 的实测步骤，专注于方法论定位和文献支撑
8	
9	---
10	
11	## 0. 核心结论（先读这里）
12	
13	| 结论 | 依据来源 |
14	|---|---|
15	| EAGLE-3 在长上下文（>8K prompt tokens）下接受率显著下降是**已发表的普遍现象**，非项目特有 bug | OWL (EMNLP 2025)、LongSpec (ACL 2025)、SpecPV 实测 |
16	| 下降有**五条独立根因**，每条都有文献和实测旁证；消除任一不足以解决全部 | 见 §2 |
17	| concurrency=64 下 EAGLE-3 仍有 **1.38× throughput**（SGLang 官方 H100 实测），未进入负收益区 | EAGLE-3 NeurIPS 2025 Table 3 |
18	| 我们 workload 中 `ignore_eos=True` 造成的 post-EOS `<unk>` 循环**人为拉低 adj_al -23%**，是可治标的工程问题 | 本仓库 §11 adj_al 分析 |
19	| 治本需重训 draft（破 CLAUDE.md 红线）；红线内**最大可行单点改进**：C2 runtime post-EOS 退 nospec 检测 | §5 修复矩阵 |
20	
21	---
22	
23	## 1. 问题定义与现象定位
24	
25	### 1.1 MiniCPM-SALA 场景
26	
27	- **模型**：32 层混合（8 Attention + 24 GLA Lightning Attention），dense_len=8192，sparse 阈值后走 InfLLM-v2
28	- **Draft**：EAGLE-3，1 层 transformer，aux hidden from layers [1,10,22]，词表 32K（d2t 子集）
29	- **评分工作负载**：64 条样本，37 条长文本 deepresearch（completion 500–31K tokens），12 条编程，ignore_eos=True，concurrency=64（Smax）
30	
31	详细实测数据见 `collapse-rerun-20260426.md`（权威版本）。核心结论：超长 deepresearch（p_tok > 120K）adj_al 1.24–1.30，aggregate al 1.865 vs adj_al 2.298（+23%，差距 90%+ 来自 post-EOS `<unk>` 结构 miss）。
32	
33	---
34	
35	## 2. 五条独立根因
36	
37	以下五条根因在文献中各有独立验证，在我们的场景中可以叠加。
38	
39	### 2.1 RoPE 位置外推失效
40	
41	**机制**：EAGLE-3 draft 的 RoPE `rope_theta` 默认 10000，训练序列长度约 2048 tokens（标准 EAGLE 训练习惯）。推理时 130K prompt 使得位置编码在 >65× 倍的外推区间工作（EAGLE-3 论文训练位置上限 2048，推理位置 130K ≈ 64× 外推）。
42	
43	**文献**：
44	- **LongSpec** (ACL 2025, arXiv:2502.17421) §4.3："EAGLE drafter's position indices... up to 2048 during training vs 200K+ at inference, a 100× extrapolation"
45	- **SpecPV**（可扩展 spec 训练综述）："RoPE theta 10000 causes phase collapse beyond 8K position"
46	- **YaRN** (ICLR 2024)：NTK 插值公式，scaling_factor=s 时 theta 应调整为 `theta * s^(d/(d-2))`；s=64（130K/2K）时 theta 有效值需 ~10000 * 64^(128/126) ≈ 700K
47	
48	**我们场景**：draft config.json `rope_theta` 未设置（默认 10000），p_tok=130K 时外推比约 64×。
49	
50	**零成本验证**：在 `eagle/sglang_model/config.json` 加 `"rope_theta": 1000000`（NTK 公式对应 100× scale），重跑 idx 34/62 adj_al 比对。此改动不触碰 ckpt 权重，10 min 可出结论。（注意：如果有改动 config.json 的话则需要验证）
51	
52	### 2.2 训练位置分布偏斜
53	
54	**机制**：短序列样本数量多 → 小位置（0–2K）被过度训练，大位置（>2K）覆盖极少。draft 在大位置 token 的 next-token 预测分布受训练不足，即使 RoPE 能正确编码位置，从这些位置开始的 logit 也分布漂移。
55	
56	**文献**：
57	- **LongSpec** (ACL 2025) §4.3 图 5：draft 训练数据按位置绘制的频率直方图，2K 处陡降；Figure 5 显示 EAGLE 在 position > 2K 的 acceptance 曲线下坠
58	- LongSpec 提出 **Anchor-Offset Indices (AOI)**：前 4 个 token 锚定在 [0,1,2,3]，后续 token 的 position_ids 从随机 offset（0–30K）开始连续递增。使用 2K 长 shard 就能覆盖 30K 的位置空间，训练收敛速度 **3.93× 提升**
59	
60	**我们场景**：v2/v3 draft 训练数据集长度分布未在文档中明确，但 collapse-investigation.md §3 提及"训练数据长度分布导致 context collapse"，与此一致。
61	
62	**可行改进（Tier 2，需重训）**：在 `eagle/train.py` 的 position_ids 构建逻辑中加入 AOI：约 20 行改动，理论上不需要增加训练数据量，只需修改采样策略。
63	
64	### 2.3 Target Hidden State 分布漂移
65	
66	**机制**：EAGLE-3 draft 使用目标模型中间层的 hidden state 作为输入特征（aux_hidden from layers [1,10,22]）。在超长上下文下，attention sink（开头几个 token 的 attention score 异常大）被 InfLLM-v2 sparse 稀疏机制放大，使得中间层的 feature 分布与短上下文训练时的分布不同。Draft 的 fc 层（12288 → 4096）接收到协变量漂移的输入，输出质量下降。
67	
68	**文献**：
69	- **OWL** (EMNLP 2025, arXiv:2510.07535)：专门研究"隐状态质量下降"问题，提出 LSTM drafter 只消费最后 1 个 token 的 hidden state（避免对 prefix hidden 的依赖），在 LongSpecBench（4K–64K）上 acceptance=4.00 vs EAGLE-3 的 1.28
70	- **QuantSpec** (2025)：target SnapKV KV cache 压缩后，acceptance rate 从 89% 降至 80%（§3.1 "sparse KV affects hidden state quality fed to drafter"）
71	
72	**我们场景特有叠加**：target 在 dense_len=8192 后走 InfLLM-v2 sparse（compress_k → stage1 block_score → stage2 top-K sparse FA），而 draft 走全量 dense attention。这一不对称性独立于 §2.1、§2.2，是第三条根因。
73	
74	### 2.4 InfLLM-v2 Sparse / Draft Dense 注意力不对称
75	
76	**机制**：超过 `dense_len=8192` 后，target 的 8 个 standard attention 层走稀疏 attention（只对 top-K 个 block 做 FA），而 draft 始终是全量 dense attention（draft 只有 1 层 transformer，不支持 InfLLM-v2 sparse）。这导致：
77	1. Target 的 KV 视野（看到哪些 prefix token）与 draft 完全不同
78	2. 特别是"遗忘"了的 context block 在 target 里不影响 logit，但 draft 仍然试图 attend 到这些 block，产生系统性预测偏差
79	
80	**文献**：
81	- QuantSpec §3.1："the mismatch between compressed KV in target and full KV in draft is an independent degradation source"
82	- OWL §2 明确将此归类为独立于 RoPE extrapolation 的"attention regime mismatch"
83	
84	**我们场景**：GLA 层（24 层）本来就是 linear attention，不走 sparse；但 8 个 standard attention 层 >8192 后走 InfLLM-v2。这 8 层的稀疏化是独立的 mismatch source。
85	
86	### 2.5 Draft 训练数据领域覆盖不足
87	
88	**机制**：Draft 在特定 prompt 类型上的 top-k 预测漏掉 target argmax，不是 RoPE 或 hidden drift 问题，而是纯粹的训练分布盲区。典型表现：多跳推理链（"根据搜索结果..."引导的段落）、专有名词（历史人物、生僻词）、自我修正短语。
89	
90	**实测证据**（collapse-rerun-20260426.md §2 §10b）：
91	- idx 17 pre-EOS 段 65/133 步 al==0，其中 60 步是"target IN hot_set, NOT in draft top-2"（draft 词表覆盖到了 target token，但 draft 预测排名不够高）
92	- collapse 段 target logit gap p50=2.75（vs 健康段 5.06），说明 target 自己在这些位置高熵，但 draft 失败率更高
93	- **连续 collapse 机制**（§10b）：单次翻转把路径推入 draft 分布盲区连续段 → 整段 al==0，直到 target commit 到 draft 熟悉的语义边界（标点、模板短语）才恢复
94	
95	**文献支撑**：
96	- **OWL**：长上下文任务测试集（history, finance, law）中 EAGLE-3 acceptance 1.28，LSTM drafter acceptance 4.00，差距与 §2.1-2.4 机制叠加一致
97	- **collapse-investigation.md §6**（本仓库历史）："暂判 draft 训练分布问题"——本轮实证确认这是主因之一
98	
99	**v3 draft 的反效果**：在 idx 17 上 v3（aux=[4,9,24]，200K 数据）pre-EOS al=0.578 vs v2 0.737，long-gen collapse 更频。v3 的 NLL -29% 不对应 long deepresearch workload，说明 v3 训练数据配比也未解决这个盲区。
100	
101	---
102	
103	## 3. Batch Size / Concurrency 对 EAGLE-3 的影响
104	
105	### 3.1 官方实测数据
106	
107	来源：EAGLE-3 论文（NeurIPS 2025），SGLang + H100 + LLaMA-3.1-8B：
108	
109	| Batch size | EAGLE（旧）| EAGLE-3 |
110	|---|---|---|
111	| 2 | 1.40× | **1.81×** |
112	| 8 | 1.23× | 1.62× |
113	| 24 | **0.93×（负）** | 1.39× |
114	| 48 | 0.88× | 1.38× |
115	| 64 | 0.99× | **1.38×** |
116	
117	**关键观察**：旧 EAGLE 从 bs=24 就进入负收益；EAGLE-3 在 bs=64 仍有 1.38×，这是 SGLang 官方 H100 实测，具有代表性。
118	
119	独立评估（Liu et al. 2025b）：EAGLE speedup bs=1 时 1.73×，bs=128 时降至 1.21×，单调递减但始终正收益。
120	
121	### 3.2 我们场景的 effective batch size
122	
123	eval 脚本发起 concurrency=64 请求，但实际 effective batch size 是动态的：
124	- 短编程样本（~8K tokens completion）比 deepresearch 快得多，早退出
125	- batch 从 64 逐渐收缩，最终由极长尾（31K completion）决定 benchmark duration
126	
127	此动态 profile 下，EAGLE-3 预期收益区间为 **1.2×–1.38×**，未进入负收益。
128	
129	### 3.3 Ragged tensor 对齐开销
130	
131	batch 内每个请求接受的 draft token 数量不同（accept_length 异质）→ ragged batch 需要 padding 对齐 → overhead 随 batch 大小和接受率方差超线性增长。
132	
133	hard 样本（acceptance≈0）相当于把当前 batch step 的 spec 有效吞吐归零，因为 batch 内最短接受数决定有效进度。
134	
135	**topk 的影响**：topk=2 tree verify 生成每个请求不同形状的候选树，batch 内树形状异质性进一步放大对齐开销。理论上 topk=1（pure chain）是对 ragged 开销最友好的配置，但 EAGLE-3 论文 bs=64 对应 topk=1 情况下收益已是 1.38×，topk=2 是否更好需实测（现有数据点不足以外推）。
136	
137	---
138	
139	## 4. ignore_eos=True 对 Spec Decoding 的影响
140	
141	这是我们比赛场景特有的机制，公开文献未直接研究，以下基于原理推导和实测验证。
142	
143	### 4.1 机制
144	
145	1. **post-EOS 生成分布混乱**：模型自然结束（输出 `<|im_end|>`，id=73440）后被强制继续生成。post-EOS 的 next-token 分布接近随机或退化（重复 `<unk>` id=0、标点循环）。
146	2. **`<unk>` 和 `<|im_end|>` 均不在 draft hot_set**：`hot_token_id = d2t + arange(32000)` 覆盖 32000 个 token，但 id=0（`<unk>`）结构上不在 d2t 子集，id=73440 超出 32K 范围。post-EOS 退化段必然是 draft 结构性不可提议区域。
147	3. **每个 al==0 的 post-EOS 步仍跑完整 verify forward**：dtn=5 意味着每步 verify 相当于 5 token 的 chunked prefill。忽略 post-EOS 段全是 al==0 但 overhead 不减——这是 spec 在 post-EOS 段比 nospec 慢 3× 的原因。
148	
149	### 4.2 实测量化
150	
151	从 benchlike_smax_20260426 全 64 样本分析（§11）：
152	
153	| 样本 | 真实 completion | dataset max_new | post-EOS 估算 |
154	|---|---|---|---|
155	| idx 16 | ~30 tokens | 210 | 174 步全 `<unk>` |
156	| idx 14 | ~4K tokens | 18688 | ~14K 步退化 |
157	| idx 15 | ~5K tokens | 30990 | ~25K 步退化 |
158	
159	这三个样本的 adj_al 名义上高（9–15），但因为 out_len/vct 极小，数字不稳定。这些样本的**有效 completion 段**（pre-EOS）adj_al 正常，是 post-EOS 拖低了 raw al。
160	
161	**aggregate 效果**：
162	- raw al（含 post-EOS miss）：1.865
163	- adj_al（剔除结构不可提议步）：2.298
164	- 差距 **+23%**，主要来源于 idx 14/15 的长 post-EOS 退化段
165	
166	### 4.3 对打分的意义
167	
168	benchmark duration = 最后一个请求完成时刻。idx 14/15 的 completion 是 18K/30K tokens，post-EOS 段 spec 效率约 0.37× nospec（每步产出 1 token 但消耗 3× 时间），这些样本成为 duration 的决定因子。
169	
170	**spec 在这些样本上净负收益**，但因为这些样本数量少（2/64），整体 aggregate 结论仍是正收益。
171	
172	---
173	
174	## 5. 现有缓解方法与 2025–2026 新方案
175	
176	### 5.1 方案矩阵
177	
178	以下按技术成熟度、我们的工程可行性、以及论文支持排列：
179	
180	#### Tier 0：零成本 / 不改权重（可立即验证）
181	
182	| 方案 | 原理 | 论文来源 | 我们可行性 | 预期收益 |
183	|---|---|---|---|---|
184	| rope_theta 10000→1M | NTK 插值消除 RoPE 外推失效（§2.1）| LongSpec §4.3；YaRN ICLR 2024 | 改 config.json 1 行，不触 ckpt | 理论消除 §2.1；实测 10 min 可验 |
185	| **C2 runtime post-EOS 退 nospec**（首要推荐）| 检测最近 K=3 commit token ∈ {0, 73440} → 该 req 退 nospec | 本仓库 §11 C2 方案 | `eagle_worker.py` 加 per-req counter，约 20 行 | +23% throughput（adj_al 差距） |
186	| Entropy threshold（draft 提前终止）| 当 draft top-1 softmax < 0.15 时不展开更多 draft token | BanditSpec ICML 2025 自适应思路 | `eagle_worker.py` draft 循环内，约 10–20 行 | 降低高熵位置 draft overhead |
187	
188	#### Tier 1：代码改动，不动权重（数天工程）
189	
190	| 方案 | 原理 | 论文来源 | 备注 |
191	|---|---|---|---|
192	| seq_len > 50K 自动关 spec | 超长 context 下 spec 几乎净负收益，不如不跑 | 本仓库 §8 量化结论 | `eagle_worker.py` 加 req.prompt_len 判断，10 行；**有争议**：50K–130K 段 adj_al=1.26–1.30，关掉是否值需 A/B bench |
193	| **FASER early exit**（2026-04 最新）| per-token 在 verify 阶段提前退出，42–48% latency 减少（LongBench greedy 实测）| arXiv:2604.20503，2026-04 | 研究原型，SGLang 未集成；integrate 工程量中等 |
194	| SGLang NGRAM prompt-cache bug fix | `ngram_worker.py` 的 extend 插入被注释掉（FIXME comment），prompt token 未进 ngram cache，deepresearch 长 prompt 的 n-gram 命中为零 | 本仓库代码审计（原始 discover）| 1–2 行取消注释；但 NGRAM 整体接受率不如 EAGLE，仅作参考 |
195	| FR-Spec vocab map | 频率排序 top-32K token 替换 draft lm_head，减少 56% 计算 | FR-Spec (2025, arXiv:2502.01824) | 我们已有 d2t 子集，相当于已实现；可测试增大到 top-40K |
196	
197	#### Tier 2：需重训 draft（破 CLAUDE.md 红线）
198	
199	| 方案 | 原理 | 论文来源 | 预期收益 |
200	|---|---|---|---|
201	| **Anchor-Offset Indices (AOI)**（最推荐）| 随机 position offset 覆盖大位置区间，消除 §2.2 位置分布偏斜，2K shard 覆盖 30K 位置空间 | LongSpec ACL 2025 §4.2 | 收敛 3.93× 更快，acceptance 在 >8K 位置大幅提升 |
202	| YaRN 微调（scaling_factor=16）| 恢复 RoPE 在 130K 处的幅度，结合 §2.1 修复 | SpecPV 实测 τ=3.0–3.3 @10K–60K | 需 1 epoch fine-tune，~6K 样本，lr=2e-5 |
203	| 扩长 deepresearch 训练数据 | 直接覆盖 §2.5 的分布盲区 | training-v3.md 方向但 v3 未收效 | 需仔细配比；v3 200K 数据反效（adj_al 更差） |
204	| 扩 d2t 到全 vocab（73448）| 消除结构性不可提议（id=0/73440）+ 部分专有名词 | 本仓库 §11 分析 | 需 lm_head 同步重训（dim 从 32000 扩到 73448） |
205	
206	#### Tier 3：架构替换（长期研究）
207	
208	| 方案 | 原理 | 论文来源 | 对我们的可行性 |
209	|---|---|---|---|
210	| **OWL LSTM drafter**（最激进但最有效）| LSTM 只消费最后 1 token hidden，不依赖 prefix hidden；训练在 256 token 上，推理 64K+ 零外推问题 | OWL EMNLP 2025，arXiv:2510.07535 | 结构完全不同，需从头训；acceptance 4.00 vs EAGLE-3 1.28（LongSpecBench） |
211	| **STree for GLA**（最适配架构）| 专为 SSM/hybrid 模型设计 tree verify，用 GLA A-matrix 累乘处理 non-causal states | STree NeurIPS 2025，arXiv:2505.14969 | 直接对应 MiniCPM-SALA 的 GLA 层；tree verify 正确性保证（现有 EAGLE-3 tree verify 在 GLA 层的 state 更新语义未被 STree 严格化） |
212	| LongSpec cache-free cross-attn | Hybrid Tree Attention，sliding window self-attn + cache-free cross-attn，保持 O(1) KV | LongSpec ACL 2025 §3.3 | 需重写 draft model forward；3.26× speedup at 32K context |
213	
214	### 5.2 优先级建议（红线内，比赛场景）
215	
216	```
217	P0（立即可做）：
218	  C2 runtime post-EOS / <unk>-loop 退 nospec
219	  → 预期 +23% throughput
220	  → eagle_worker.py 约 20 行，false positive 极低
221	
222	✅ P1（已完成，2026-04-27）：
223	  rope_theta 改 config.json（不动 ckpt）
224	  → vlong bucket（p_tok>50K） adj_al +44.9%（全量 64 样本实测）
225	  → demo-sala/data/eagle_draft/config.json 已写入 "rope_theta": 1000000
226	
227	P2（A/B bench 已完成，2026-04-27）：
228	  topk 1 vs 2 → 已确认：生产使用 topk=2, spec_steps=3, dtn=7
229	  详见 verify-experiments-log-20260427.md
230	
231	P3（需重训，破红线）：
232	  AOI 训练改动 + 长 deepresearch 数据扩充
233	  → 理论修复 §2.2，是目前唯一能根治 adj_al=1.24-1.30 的红线内可讨论方向
234	```
235	
236	---
237	
238	## 6. 与本仓库实测数据的对应关系
239	
240	实测结论三点：超长 deepresearch（p_tok=120K–130K）adj_al 1.24–1.30，与文献长上下文 acceptance 崩到 ~1.2 一致；aggregate al 1.865 vs adj_al 2.298（+23%），差距来自 post-EOS `<unk>` miss；nospec c=4 也产生 4 个不同 sha，batch drift 与 spec 无关。详细数据见 `collapse-rerun-20260426.md`。
241	
242	---
243	
244	## 7. 未解与存疑
245	
246	| 问题 | 当前状态 | 所需工作 |
247	|---|---|---|
248	| ~~rope_theta=1M 是否实际改善 idx 34/62 adj_al~~ | ✅ **已验证（2026-04-27）**：vlong +44.9%，config 已部署 | `verify-experiments-log-20260427.md §1` |
249	| ~~topk=1 vs topk=2 在 bs=64 下哪个吞吐更高~~ | ✅ **已确认**：生产配置 topk=2, spec_steps=3, dtn=7 | `verify-experiments-log-20260427.md` |
250	| C2 runtime 退 nospec 在 production EOS 场景是否仍有效 | 未验证 | production 下 ignore_eos=False，模型正常 EOS 退出，C2 不触发；收益来自 bench 场景 |
251	
252	---
253	
254	## 8. 参考文献
255	
256	| 论文 | arXiv / 会议 | 核心贡献 | 与本文关联 |
257	|---|---|---|---|
258	| EAGLE-3 | NeurIPS 2025 | Feature drafter，chain/tree verify，批量 speedup | §3 batch size 数据来源 |
259	| OWL | arXiv:2510.07535，EMNLP 2025 | LSTM drafter，长上下文 acceptance 4.00 vs EAGLE-3 1.28 | §2.3 隐状态漂移；§5 Tier 3 |
260	| LongSpec | arXiv:2502.17421，ACL 2025 | Anchor-Offset Indices，cache-free cross-attn，3.26× at 32K | §2.2 位置偏斜；§5 Tier 2/3 |
261	| STree | arXiv:2505.14969，NeurIPS 2025 | SSM/hybrid 模型 tree verify | §5 Tier 3 |
262	| FASER | arXiv:2604.20503，2026-04 | Per-token early exit，42–48% latency 减少 | §5 Tier 1 |
263	| FR-Spec | arXiv:2502.01824，2025 | Frequency-ranked vocab 56% 计算减少 | §5 Tier 1 |
264	| YaRN | ICLR 2024 | NTK 插值，rope_theta 公式 | §2.1 |
265	| QuantSpec | 2025 | KV 压缩对 spec 的影响 | §2.4 |
266	| BanditSpec | ICML 2025 | 多臂老虎机自适应 spec_steps | §5 Tier 0 entropy threshold |
267	| LongBench v2 / LongSpecBench | 2024–2025 | 长上下文评测基准 | OWL 测试集来源 |
268	
269	---
270	
271	*本文档基于 2026-04-27 调研快照；spec decoding 领域进展迅速，建议 2 周后重新检索 arXiv:cs.CL 的 speculative 新 paper。*
272
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/spec-survey.md"
}
```

> TOOL

tool_result Read
```
1	# Speculative Decoding Verify 机制与线性注意力 Verify 深度调查
2	
3	> 调查时间：2026-04-27（第一轮本地代码）+ 2026-04-27（第二轮 verify 机制）+ 2026-04-27（第三轮补充）
4	> 方法：16 个 subagent 并行（本地代码分析 + Tavily + arxiv MCP 深度检索），覆盖 verify 机制创新、线性注意力/SSM verify、EAGLE 架构、长上下文分析
5	> **定位：原材料库**。记录调查发现的事实和论文内容，不做结论或行动建议。工程决策和实测数据见 [`experiments-log.md`](experiments-log.md)。
6	
7	---
8	
9	## 1. Tree Verification 创新
10	
11	### 1.1 Traversal Verification（NeurIPS 2025, arXiv:2505.12398）
12	
13	验证方向从 top-down 改为 bottom-up（叶到根），采用序列级接受概率而非逐 token 接受概率。
14	
15	核心机制：传统 top-down 中父节点拒绝则所有子节点丢弃；Traversal 中父节点只在所有子节点均被拒绝后才验证。序列级联合概率 `min(r(X1)*r(X3), 1)` 允许跨步概率补偿（vs 传统 `min(r(X1),1)*min(r(X3),1)`）。
16	
17	数值示例：`r(X1)=0.5, r(X3)=4/3` 时，Traversal P(accept)=0.667 vs 传统 0.5。
18	
19	纯算法层改动，与 FlashInfer 兼容。
20	
21	### 1.2 Dynamic Delayed Tree Expansion（arXiv:2602.16994, 2026.02）
22	
23	系统评估了 Traversal Verification vs OT-based（SpecInfer）验证策略。发现 Traversal 全面优于 OT 方法。OT 方法在树根附近获得高多 token 接受率，但收益在树深处更关键。
24	
25	提出 delayed tree expansion：先 draft 一段单路径，延迟 i.i.d. 分支点。还开发动态神经选择器（neural selector），从 draft/target 特征估计 OT 验证的 block efficiency，动态决定是否展开。
26	
27	neural selector 需轻量训练；delayed expansion 本身不需要。
28	
29	### 1.3 GOOSE — Anisotropic Speculation Trees（arXiv:2604.02047, 2026.04）
30	
31	观察到两种 training-free token 来源（n-gram 匹配 vs 统计预测）的接受率差距巨大（中位数 6x，范围 2-18x）。**核心定理**：当存在质量差距时，最优树是各向异性的——高接受率 token 形成深链（spine），低接受率 token 作为宽分支。
32	
33	构建自适应 spine tree：深层链由高接受率的 context-matched token 组成，每个节点挂宽分支作备选。5 个 LLM（7B-33B）上比 balanced-tree baseline 提升 12-33%。
34	
35	Training-free。
36	
37	### 1.4 Hierarchical Verification Tree（HVT）（arXiv:2508.03726, 2025.08）
38	
39	将 spec beam decoding的验证重构为层次化结构——优先验证高似然的 draft，提前剪枝次优候选。形式化的 verification-pruning 算法保证正确性。
40	
41	Training-free。
42	
43	### 1.5 SAGE — Entropy-Guided Adaptive Tree（arXiv:2602.00523, 2026.02）
44	
45	利用输出 entropy 作为自然置信度指标（具有跨解码步骤的强时间相关性）。高置信时构建 deep-narrow 树，低置信时构建 shallow-wide 树。
46	
47	LLaVA-OneVision-72B 达 3.36x speedup。Training-free。
48	
49	### 1.6 C2T — Classifier-Based Tree Construction（arXiv:2502.13652, 2025.02）
50	
51	训练轻量 classifier，输入特征超越传统联合概率，输出每个 draft token 的 confidence score 据此决定是否纳入候选树。比 EAGLE-2 减少 25% 候选 token 数。需训练 classifier。
52	
53	### 1.7 OPT-Tree / Sequoia
54	
55	OPT-Tree（arXiv:2406.17276, 2024.06）：动态规划搜索最大化 acceptance length 期望的最优树结构。Sequoia（arXiv:2402.12374, 2024.02）：动态规划最优树 + 硬件感知树优化器。两者均 training-free。
56	
57	---
58	
59	## 2. 接受规则创新
60	
61	### 2.1 MARS — Margin-Aware Speculative Verification（ICLR 2026, arXiv:2601.15498）
62	
63	当 target 的 top-1 和 top-2 概率接近（low-margin）时，拒绝 runner-up token 的信息增益可忽略但 rollback 成本高。MARS 从 target logits 测量 decision stability，低 margin 区域放宽验证。
64	
65	训练免费，域无关，8B-235B 一致提速。
66	
67	**算法**：对每个 draft token v_t：
68	1. Exact Match：`v_t == top-1` → 直接接受
69	2. Adaptive Relaxation：`v_t == top-2` 且 `r_t = z_(2)/z_(1) > θ` → 接受（视为 tie）
70	3. 否则拒绝
71	
72	**论文参数结论（θ 扫描 [0.84, 0.96]）**：
73	- θ=0.90 是 speedup 与 quality 的帕累托最优点
74	- θ=0.90：τ（accept length）提升 +27%，端到端加速比较 EAGLE-3 提升约 +20%；BLEU/ROUGE/MT-Bench 退化在统计噪声范围内（BLEU 差 0.04）
75	- θ < 0.88：开始出现可测量的质量退化（BLEU 约 -1 分）
76	- θ=0.5：论文未测试，预计质量退化明显
77	- **无正式散度理论保证**，论文定位为 lossy variant，以实证为依据
78	
79	**工程落地状态（2026-04-27，已上生产）**：
80	
81	MARS 实测已完成，theta=0.85 全量 64 样本生产配置已部署。详细实测数据见 [`experiments-log.md`](experiments-log.md) §方向三。
82	
83	| 修改文件 | 内容 |
84	|---|---|
85	| `sgl-kernel/csrc/speculative/eagle_utils.cu` | `VerifyTreeGreedy` kernel 8→11 参数（+`top2_token`, `top2_ratio`, `mars_theta`）；先扫描 exact match，fallback 到 MARS |
86	| `sgl-kernel/csrc/common_extension.cc` | PyTorch op schema 更新为 11 参数，3 新参数可选 |
87	| `sgl-kernel/include/sgl_kernel_ops.h` | C++ 头文件同步更新 |
88	| `sgl_kernel/speculative.py`（venv） | Python wrapper 转发 3 个新可选参数 |
89	| `demo-sala/sglang/.../eagle_utils.py` | 调用侧加 `target_predict.contiguous()`（server 中该 tensor 为非连续 view）|
90	| `demo-sala/sglang/.../eagle_info.py` | verify 循环中检测 EOS（`FINISH_MATCHED_TOKEN`），以红色 ANSI 打印到日志 |
91	
92	**已知约束**：
93	- 依赖 `gptq_marlin.cu` **Feb 21 版本**（旧稳定版，37KB）。Apr 25 版本（44KB，含 `workspace_blocks_per_sm` 动态参数）在 rebuild 后导致 EAGLE draft CUDA graph capture 在 bs=8 挂住，详见 `docs/marlin-tuning.md §25`
94	- 启动时需传 `EAGLE_MARS_THETA=0.9`（默认 θ=-1.0 = MARS 关闭，保持原有贪心行为）
95	
96	**待完成**：
97	- [x] θ=0.85 初步验证：MiniCPM-SALA 生产 eval 中吞吐可观测提升，eval 分数无可观测下降（论文预测退化但未在本模型上观测到，推测与 NVFP4 量化 logit ratio 分布有关）
98	- [ ] 系统 bench：mini_bench + full bench 量化具体加速数字
99	- [ ] θ 精调：扫描 {0.80, 0.85, 0.88, 0.90}，当前推荐 θ=0.85
100	
101	### 2.2 Cactus — Constrained Acceptance Speculative Sampling（arXiv:2604.04987, 2026.04）
102	
103	将 speculative sampling 形式化为约束优化问题：最大化 acceptance rate，约束输出分布与 target 的散度 ≤ epsilon。标准 SpS 是 epsilon=0 的特例。
104	
105	接受规则公式（KKT 条件推导）：接受概率 = `min(1, p_target(x)/p_draft(x) * g(x))`，其中 g(x) 保证 `TV(p_output, p_target) ≤ epsilon`。
106	
107	提供 principled 的 epsilon-放松框架。Training-free。
108	
109	### 2.3 DIVERSED — Dynamic Ensemble Verification（AISTATS 2026, arXiv:2604.07622）
110	
111	验证分布从 p_target 放松为 `p_verify = alpha * p_target + (1-alpha) * p_draft`。alpha 由轻量级神经网络学习（单层 FC + sigmoid）。Static Ensemble 变体固定 alpha，training-free。
112	
113	理论保证：relaxed 分布与 target 的偏差有界（TV distance 上界）。
114	
115	代码：https://github.com/comeusr/diversed
116	
117	### 2.4 SMC-SD — Sequential Monte Carlo Speculative Decoding（arXiv:2604.15672, 2026.04）
118	
119	用 importance-weighted resampling 替代 rejection sampling。维护 N 个 draft particles，每步 importance reweight 后 resample，而非拒绝截断。
120	
121	关键洞察：LLM inference 是 memory-bandwidth-bound，SMC 的额外 compute 几乎免费。保留所有 draft 信息，不截断。per-step approximation error 有界（SMC 理论）。
122	
123	Training-free。
124	
125	### 2.5 Fuzzy SD（ACL Findings 2025, arXiv:2502.20704）
126	
127	用 target 和 draft 分布的散度（KL/JS/TV）决定是否接受。Reduced 变体：先标准验证，rejected token 再做 fuzzy check。
128	
129	### 2.6 Calibrated Speculative Decoding（CSD）（arXiv:2604.13634, 2026.04）
130	
131	两个模块：(1) Online Correction Memory — 聚合历史拒绝模式做 rescue candidate；(2) Semantic Consistency Gating — 用概率比代替精确 token 匹配做验证。
132	
133	允许"语义等价但词汇不同"的 token 被接受。Training-free。
134	
135	### 2.7 Reflective Verification（arXiv:2505.18629, 2025.05）
136	
137	利用 LLM 的 reflective capacity，单次 forward pass 同时获得 p_original 和 p_reflective，融合做语义级验证。与统计验证正交，组合使用额外 5-15% speedup。Training-free。
138	
139	### 2.8 SelfJudge（arXiv:2510.02329, 2025.10）
140	
141	通过 target model 的自监督训练 judge verifier：衡量 token 替换后的 response 是否保持原意。需训练但无需人工标注。
142	
143	### 2.9 KL-Divergence Judge Training-Free（arXiv:2601.04766, 2026.01）
144	
145	理论证明 trained linear judge 学到的 criticality score 本质上编码在 draft-target KL divergence 中。提出 training-free 验证机制：高 KL = 严格验证，低 KL = 放松验证。
146	
147	### 2.10 LK Losses — Direct Acceptance Rate Optimization（arXiv:2602.23881, 2026.02）
148	
149	标准训练用 KL 散度作为 proxy，但小 draft 模型容量受限时，最小化 KL 不等于最大化 acceptance rate。提出 LK（Log-KL）损失函数族，直接优化 acceptance rate 的可微上界/下界。4 种 draft 架构、6 个 target 模型（8B-70B），acceptance rate 提升 5-15%。需替代标准 KL 蒸馏训练。
150	
151	### 2.11 Alignment-Augmented SD（arXiv:2505.13204, 2025.05）
152	
153	利用 prefill 阶段的输出分布做 alignment sampling（提供更对齐的 draft 候选）。对高质量但不对齐的 draft，引入 flexible verification：自适应概率阈值。平均 acceptance length 达 2.39，speedup 2.23x。Training-free。
154	
155	### 2.12 Global Resolution — Optimal Multi-Draft（arXiv:2511.15898, 2025.11）
156	
157	将最优传输问题从指数规模 LP 归约为 V 个变量的凸优化（V = 词表大小），利用 polymatroid 理论。n-draft 下 90% 接受率且 <100ms overhead/token。
158	
159	---
160	
161	## 3. Block / Sequence-Level Verification
162	
163	### 3.1 Block Verification（arXiv:2403.10444, 2024.03）— 奠基工作
164	
165	**核心证明**：逐 token 独立验证不是最优的。联合验证整个 block，使用 on-path 概率的联合条件。BV 在所有仅使用 on-path 概率的验证算法中最优，期望接受 token 数 >= 标准验证。额外 wall-clock 加速 1.1-1.3x。Training-free。
166	
167	### 3.2 Greedy Multi-Path Block Verification（arXiv:2602.16961, 2026.02）
168	
169	将 BV 从单路径扩展到多路径 tree。贪心选择接受概率最高的路径。比独立 token 验证和单路径 BV 均更优。Training-free。
170	
171	### 3.3 SJD-PV — Phrase Verification（arXiv:2603.06666, 2026.03）
172	
173	phrase-level 联合验证（多 token 组）。通过共现统计构建 phrase 单元，联合验证 phrase 内所有 token。
174	
175	---
176	
177	## 4. Early Exit / Multi-Stage Verify
178	
179	### 4.1 HiSpec — Hierarchical Speculative Decoding（arXiv:2510.01336, 2025.10）
180	
181	用 early-exit model 做中间验证。EE model 允许 token 在中间层提前退出，跳过后续层计算。定期将 intermediate verifier 接受的 token 对照 target 做 full verification。
182	
183	需要训练 EE model（layer dropout + early exit loss）。Average throughput 提升 1.28x，最高 2.01x。
184	
185	### 4.2 LayerSkip — Self-Speculative + Early Exit（arXiv:2404.16710, 2024.04, Meta）
186	
187	训练时用 layer dropout（浅层低、深层高）+ 所有层共享 exit loss，增强浅层 early exit 准确度。推理时浅层 exit 做 draft，剩余层做 verify。需训练。
188	
189	### 4.3 PPSD — Pipeline-Parallel Self-Speculative（arXiv:2509.19368, 2025.09）
190	
191	将模型层配置为 pipeline，early-exit（draft）计算和剩余层（verify）计算重叠。逐 token 交替 drafting 和 verification。2.01x-3.81x speedup。需训练 early-exit head。
192	
193	### 4.4 FASER — Fine-Grained Phase Management（arXiv:2604.20503, 2026.04）
194	
195	per-request 动态调整 speculative length + verification phase 内部 early pruning + 将 verification phase 拆分为 frontiers/chunks 与 draft phase 重叠执行。vLLM 中实现，throughput 提升 53%，latency 降低 1.92x。Training-free。
196	
197	### 4.5 Speculative Verification（SV）（arXiv:2509.24328, 2025.09）
198	
199	用 companion model 估计 draft-target 分布对齐度，动态调整验证长度。低准确率时缩短验证，高时延长。bs=32-80 时平均 1.4x 加速。
200	
201	### 4.6 TriSpec — Ternary Speculative Decoding（arXiv:2601.23180, 2026）
202	
203	三阶段 proxy verifier：approve（直接接受）→ uncertain（调 target 验证）→ reject。可叠加在 EAGLE-3 上。
204	
205	### 4.7 SPRINTER — Sequential Approximate Verification（arXiv:2502.04557, 2025）
206	
207	训练低复杂度 verifier 预测 draft token 是否会被 target 接受。仅当不可接受时才调 target。
208	
209	### 4.8 SpecPV — Partial Verification（arXiv:2512.02337, 2025）
210	
211	用部分 KV states 做快速验证，定期做 full verification 消除累积误差。长上下文生成上最高 6x 解码加速。
212	
213	---
214	
215	## 5. Batch / Parallel Verify
216	
217	### 5.1 MineDraft — Batch Parallel SD（arXiv:2603.18016, 2026.03）
218	
219	维护两批 request，一批 drafting 同时另一批 verification，重叠 drafting latency 与 verification。throughput 提升 75%，latency 降低 39%。已实现为 vLLM 插件。Training-free。
220	
221	### 5.2 ECHO — Elastic Speculative Decoding（arXiv:2604.09603, 2026.04）
222	
223	将 speculative execution 重定义为 budgeted scheduling problem。Sparse confidence gating 将整个 batch 作为统一 super-tree 管理，弹性分配 depth/width budget。已集成在 SGLang 中。Qwen3-235B 上最高 5.35x speedup。Training-free。
224	
225	### 5.3 Mirror-SD — 异构并行（arXiv:2510.13161, 2025.10）
226	
227	draft 和 target 在异构加速器（GPU + NPU）上并行执行。2.8x-5.8x walltime speedup，比 EAGLE-3 平均快 30%。需异构硬件。
228	
229	### 5.4 SpecFormer — 非自回归并行 draft（arXiv:2511.20340, 2025.11）
230	
231	结合单向 + 双向 attention 的 draft 架构。非自回归并行生成消除对大前缀树的依赖。需训练 SpecFormer draft model。
232	
233	---
234	
235	## 6. Verify Overhead / 量化 Verify
236	
237	### 6.1 Quasar — 量化验证（arXiv:2603.01399, 2026.03）
238	
239	对 verification phase 使用低 bit 量化。核心洞察：结构化剪枝严重损害验证准确性，但量化能高保真保留 logit 分布同时减半内存流量。与现有 drafting 策略正交。Training-free。
240	
241	### 6.2 MoE-Spec — Expert Budgeting（arXiv:2602.16052, 2026.02）
242	
243	对 MoE 模型，大 draft tree 激活大量 unique experts 增加内存压力。每层执行固定 expert capacity limit，只加载贡献最大的 experts。比 EAGLE-3 throughput 高 10-30%。Training-free。
244	
245	### 6.3 Nightjar — 自适应 Spec 开关（arXiv:2512.22420, 2025.12）
246	
247	MAB planner 动态决定是否启用 spec decoding。高负载时关闭 SD 并将 draft model offload 到 CPU，回收 GPU 内存给 KV cache。throughput 提升 27.29%，latency 降低 20.18%。Training-free。
248	
249	### 6.4 Hidden State 复用（arXiv:2602.21224, 2026.02）
250	
251	验证失败的 draft hidden states 复用。在 hidden state 层面做自回归预测，验证失败时从 hidden states 重新采样 token 而非从头 draft。最高 3.3x speedup。需训练特殊 draft model。
252	
253	### 6.5 SpeCache — Speculative KV Caching（arXiv:2503.16163, 2025）
254	
255	预测下个 token 可能访问的 KV pair，speculative fetching。低 bit KV cache copy 在 VRAM 中做重要性度量。
256	
257	### 6.6 VOCABTRIM（arXiv:2506.22694, 2025）
258	
259	Draft 时裁剪 LM head 的词汇表，减少不必要的推理开销。对大词表模型（73448）收益显著。Training-free。
260	
261	---
262	
263	## 7. SSM / Mamba + Speculative Decoding Verify
264	
265	### 7.1 SpecMamba（arXiv:2509.19873, 2025）
266	
267	**最直接相关的 SSM verify 工作**。提出 SSM hidden state backtracking 的三种方案：
268	
269	| 方案 | 策略 | 内存开销 | 计算开销 | 适用场景 |
270	|------|------|----------|----------|----------|
271	| Plan I | 存所有 draft token 的 h_t | O(spec_len * state_dim) | 无额外计算 | Draft model |
272	| Plan II | 缓存轻量激活 (A,B,Delta,X)，需时重算 | O(spec_len * activation_dim) | 重算 h_t 的 SSM 前向 | Target verify |
273	| Hybrid | Draft 用 Plan I，Target 用 Plan II | 最优 tradeoff | 最优 tradeoff | 系统级 co-design |
274	
275	FIFO-based Tree Verification with Tiling：利用 SSM 的 token 间依赖关系，按 BFS 顺序验证 tree。节点所有子节点验证完毕后即可驱逐，内存需求从 O(所有节点) 降至 O(活跃路径)。
276	
277	SSM 层无法像 attention 那样对多条候选路径并行计算，必须串行递推。
278	
279	FPGA 上 2.27x 加速。
280	
281	### 7.2 Mamba Drafters（arXiv:2506.01206, 2025, EMNLP 2025）
282	
283	用 Mamba SSM 作为外部 drafter。常数内存 draft（Mamba 的 recurrent state 大小固定）。130M Mamba drafter 在 Llama-2-70B target 上达 2.55x 加速。
284	
285	注意：这是 SSM 做 drafter（target 仍是 Transformer），与 MiniCPM-SALA 的问题方向相反（我们的 target 有 SSM 层）。
286	
287	### 7.3 Gating is Weighting（arXiv:2504.04308, 2025）
288	
289	证明多层 GLA 可实现 Weighted Preconditioned Gradient Descent (WPGD)。Gating 控制每个 token 对预测的贡献权重。
290	
291	对 verify 的含义：GLA state 回滚不只影响"记忆"，还影响模型内部的"优化状态"。如果 state 不完全正确，后续预测的质量退化可能比 Transformer 的 KV cache 不一致更严重。
292	
293	---
294	
295	## 8. Hybrid Attention + Speculative Decoding Verify
296	
297	### 8.1 Nemotron 3 Super — MTP + Hybrid Mamba-Transformer（arXiv:2604.12374, 2026, NVIDIA）
298	
299	MTP head 与主模型共享参数，通过 shared-weight formulation 递归使用。Hybrid Mamba-2 + MoE + 少量 attention 层。MTP 平均 acceptance length = 3.45（SPEED-Bench, draft length=7）。
300	
301	**未讨论** Mamba 层的 state 管理（回滚/快照）问题——推测是因为 MTP verify 时 SSM 层的 state 按正确序列自然递推，不需要显式回滚。
302	
303	### 8.2 DUET — Disaggregated Hybrid Mamba-Transformer（arXiv:2603.15530, 2026）
304	
305	Hybrid Mamba-Transformer 模型的 SSM 层在 decode 阶段是 element-wise 操作，不适合 matmul-centric 加速器。SSM decode 是 bandwidth-bound 的，verify 时串行递推 SSM 层的瓶颈是内存带宽而非计算量。
306	
307	### 8.3 Jamba / Zamba
308	
309	Jamba（arXiv:2403.19887, AI21 Labs）：交替 Transformer + Mamba 层 + MoE，52B/12B active。Zamba（arXiv:2405.16712, Zyphra）：Mamba backbone + 单一共享 attention module。两者均未涉及 speculative decoding。
310	
311	### 8.4 OWL LSTM Drafter（arXiv:2510.07535, EMNLP 2025）
312	
313	**动机**：EAGLE-3 在长上下文（LongSpecBench）acceptance=1.28，OWL LSTM drafter acceptance=4.00。差距根因：EAGLE 依赖 full-context KV cache，上下文越长 feature 越偏移；OWL 只消费 last-token hidden state，不受上下文长度影响。
314	
315	**架构**：单层 LSTM，hidden size=12288
316	
317	输入映射：
318	```
319	e_{N+1} = E(t_{N+1})
320	s^m = W^m(h_N) + alpha * e_{N+1},  m in {f,i,o,c}   // W^m ∈ R^{d_0 × d}
321	```
322	
323	LSTM 前向：
324	```
325	g^m = sigma(s^m),   m in {f,i,o}     // sigmoid 门控
326	s^c = GeLU_LN(s^c) * g^i             // GeLU + LayerNorm（非标准 tanh）
327	z   = z * g^f + s^c                   // cell state
328	h_{N+1} = GeLU_LN(z) * g^o           // 输出
329	```
330	
331	**alpha 系数**（遵循 MLP-Speculator）：`alpha_0 = 2^{-1/(2n)}`（n=tree depth），`alpha = 2*alpha_0 / ((1-alpha_0^2)*d)`
332	
333	**[SPEC] token**：额外可学习 token 增强起始步的 verifier 表示。**参数量**（Llama-3.1-8B）：4× 投影矩阵 ~201M。
334	
335	### 8.5 LongSpec Anchor-Offset Indices（arXiv:2502.17421, ICML 2025）
336	
337	**AOI 完整算法**（论文附录 G, Algorithm 1）：
338	
339	```
340	Input: 序列长度 N, 最大长度 MAX_LEN, Query states q_s
341	Output: 应用了修改后 indices 的 RoPE 结果
342	
343	1. P ← {0, 1, ..., N-1}               // 初始连续 position indices
344	2. o ← RandomInt(0, MAX_LEN - N)      // 随机 offset
345	3. P[4:] += o                         // 前 4 个 anchor 不变，后续全加 offset
346	4. return RoPE(q_s, P)
347	```
348	
349	**Anchor 数量=4 的依据**：StreamingLLM 的 attention sink 观察（前 4 个 token 聚集大量 attention weight）。
350	
351	| 目标模型 | 随机 offset 范围 |
352	|---|---|
353	| Vicuna-7B / LongChat-7B | [0, 15000] |
354	| Vicuna-13B / Llama-3.1-8B / Qwen-2.5-7B | [0, 30000] |
355	
356	**约束**：draft model RoPE base **必须**与 target 完全一致。AOI 只改 position_ids，不改 RoPE 参数。
357	
358	**AOI Ablation**：Multi-News τ: 3.20→3.36（+5%），tok/s +6-7%，训练收敛 3.93× 更快。
359	
360	**与 MiniCPM-SALA 的交互**：24 层 GLA 有 RoPE → AOI 有效；8 层 sparse attention 无 RoPE → AOI 无直接效果。draft 全层有 RoPE → AOI 完全有效。AOI 与 rope_theta=1M 互补：theta 解决旋转角周期问题，AOI 解决训练位置覆盖问题；offset 范围需根据 512K max_position 调整（论文的 [0,30K] 针对 32K 上下文）。
361	
362	### 8.6 GLA State 在推测解码中的生命周期（本地实现参考）
363	
364	**正常 Decode 路径**（`SimpleGLAAttnBackend.forward()`）：
365	
366	`simple_gla_decode_update_fwd`（`SGLANG_SIMPLE_GLA_DIRECT_DECODE=1`）：自定义 Triton kernel 直接读写 `layer_cache.temporal[state_indices]`，消除 gather+index_put 开销。核心公式：`h_t = exp(g_gamma) * h_{t-1} + k_t @ v_t^T`，`o_t = (h_t @ q_t^T) * scale`
367	
368	**TARGET_VERIFY 路径**：不直接修改 `layer_cache.temporal`，而写入 `intermediate_ssm` 缓冲区（形状 `(num_mamba_layers, pool_size+1, dtn, HV, K, V)`）。Kernel `_fused_recurrent_gla_intermediate_kernel` 在每步保存 `ht_all`，用 `retrieve_parent_token` 处理 tree sibling 隔离（等效于 STree 的 A-matrix 累乘方案）。
369	
370	**verify 后处理**（`_mamba_verify_update`）：从 `intermediate_ssm` 按 `accept_index` 选取正确步骤写回 `ssm_states`，使用 3D fancy indexing。Profile 归因下占 verify 期 index kernel 的 98.4%。
371	
372	---
373	
374	## 9. 当前代码中的 Verify 实现（本地调查补充）
375	
376	### 9.1 已有的放松接受基础设施
377	
378	`demo-sala/sglang/` 中使用 `tree_speculative_sampling_target_only`（sgl_kernel CUDA kernel），支持 `threshold_single` 和 `threshold_acc` 两个放松参数（默认 1.0 = 标准 lossless）。
379	
380	### 9.2 Phased Verify 的 GLA State 管理
381	
382	从 `eagle_worker.py` 和 `hybrid_linear_attn_backend.py` 代码可见：
383	
384	1. Phase-1 verify：`p1_gla = intermediate_ssm[:, :bs, :3].clone()`，保存 3 个 GLA intermediate state
385	2. Phase-1 结束后：将 Phase-1 的 dt1 state 写回 `ssm_states_all`，然后执行 Phase-2
386	3. Phase-2 结束后：恢复 Phase-1 的 GLA intermediate state `intermediate_ssm[:, :bs, :3] = p1_gla`，同时保存 Phase-2 的 state
387	4. 恢复生产 ssm_states：`ssm_states_all[:, mamba_indices_active] = ssm_orig_backup`
388	
389	这本质上是多阶段 state snapshot + restore 策略，对应 SpecMamba 论文的 Plan I 变体。
390	
391	### 9.3 文献中的空白
392	
393	**目前没有发现任何论文专门解决"混合 standard attention + GLA 架构的 speculative decoding verify"问题**。现有工作要么：
394	- 全 SSM（SpecMamba）：target 全部是 Mamba
395	- 全 Transformer target（Mamba Drafters）：SSM 只做 drafter
396	- MTP self-speculation（Nemotron）：不涉及外部 drafter 的 verify 回滚
397	
398	MiniCPM-SALA 的 8 层 attention + 24 层 GLA + EAGLE 外部 drafter 组合在文献中独一无二。
399	
400	---
401	
402	## 10. Draft 生成方式革新影响 Verify
403	
404	### 10.1 FastEagle — Cascaded Drafting（arXiv:2509.20416, 2025）
405	
406	非自回归级联 drafter，一次 forward 生成整个 draft。Constrained draft tree 保持无损验证成本。在 greedy 和 stochastic decoding 下一致超过 EAGLE-3。
407	
408	### 10.2 DDTree — Block Diffusion Draft Trees（arXiv:2604.12989, 2026）
409	
410	从 block diffusion drafter 的 per-position distributions 直接构建 draft tree。Best-first heap 选择最可能匹配 target 的 continuation。单次 target forward 验证整棵树。
411	
412	### 10.3 SpecForge（arXiv:2603.18567, 2026）
413	
414	SGLang 官方 EAGLE-3 训练框架。发布 SpecBundle：主流开源 LLM 的生产级 EAGLE-3 draft 模型。Qwen3-235B-A22B 训练加速 9.9x。
415	
416	### 10.4 PayPal EAGLE3 实证研究（arXiv:2604.19767, 2026）
417	
418	vLLM + EAGLE3 + 2xH100。gamma=3: 22-49% throughput 提升，18-33% 延迟降低。Acceptance rate ~35.5% (gamma=3), ~25% (gamma=5)。
419	
420	---
421	
422	## 11. Verify 后处理与 KV Cache 管理
423	
424	### 11.1 Sparse Verification（arXiv:2512.21911, 2025）
425	
426	对验证阶段做联合稀疏化（attention + FFN + MoE），减少验证计算瓶颈。Inter-draft token 和 inter-layer retrieval reuse 减少冗余计算。适用场景：长上下文和 MoE 模型。
427	
428	### 11.2 EAGLE-Pangu — 加速器安全树 SD（arXiv:2603.08088, 2026）
429	
430	将 EAGLE-3 树推测解码移植到 Ascend NPU。显式 branch/commit cache manager；加速器安全树张量化（消除负索引）；fused-kernel 兼容的 teacher 验证路径。
431	
432	### 11.3 Nightjar — 资源感知自适应（arXiv:2512.22420, 2025）
433	
434	根据请求负载动态选择最优 speculative length。MAB planner 决定何时禁用推测。高负载时验证开销变为瓶颈。
435	
436	### 11.4 SMART — System-Aware Marginal Analysis（arXiv:2604.09731, 2026）
437	
438	将树展开重形式化为硬件感知优化问题。边际收益-成本规则，仅当节点边际收益-成本比超过树级加速比时才展开。Training-free，即插即用。
439	
440	---
441	
442	## 12. 综合论文索引
443	
444	| 论文 | arXiv ID | 时间 | 改动点 | 训练需求 | 理论无损 |
445	|---|---|---|---|---|---|
446	| Traversal Verification | 2505.12398 | 2025.05 | 验证方向（叶→根） | 无 | 是 |
447	| Delayed Tree Expansion | 2602.16994 | 2026.02 | 树结构（延迟分支） | neural selector 需训练 | 是 |
448	| GOOSE Anisotropic Tree | 2604.02047 | 2026.04 | 树结构（各向异性） | 无 | 是 |
449	| HVT | 2508.03726 | 2025.08 | 层次化剪枝验证 | 无 | 是 |
450	| SAGE Entropy Tree | 2602.00523 | 2026.02 | 树结构（entropy 深宽） | 无 | 是 |
451	| C2T Classifier Tree | 2502.13652 | 2025.02 | 树构建（分类器） | 需训练 classifier | 是 |
452	| OPT-Tree | 2406.17276 | 2024.06 | 最优树（DP） | 无 | 是 |
453	| Sequoia | 2402.12374 | 2024.02 | 最优树（硬件感知） | 无 | 是 |
454	| MARS | 2601.15498 | 2026.01 | 接受规则（margin-aware） | 无 | 近似无损 |
455	| Cactus | 2604.04987 | 2026.04 | 接受规则（约束优化） | 无 | 受控偏差 |
456	| DIVERSED | 2604.07622 | 2026.04 | 接受规则（ensemble 混合） | ensemble 需训练 | 近似无损 |
457	| SMC-SD | 2604.15672 | 2026.04 | 采样方式（SMC resampling） | 无 | 近似 |
458	| Fuzzy SD | 2502.20704 | 2025.02 | 接受规则（散度阈值） | 无 | 阈值控制 |
459	| CSD Calibrated | 2604.13634 | 2026.04 | 接受规则（语义等价） | 无 | 受控偏差 |
460	| Reflective Verification | 2505.18629 | 2025.05 | 验证维度（语义+统计） | 无 | 是 |
461	| SelfJudge | 2510.02329 | 2025.10 | 验证维度（自监督 judge） | 需训练（无标注） | 受控偏差 |
462	| KL-Divergence Judge | 2601.04766 | 2026.01 | 接受规则（KL criticality） | 无 | 受控偏差 |
463	| LK Losses | 2602.23881 | 2026.02 | 训练目标（acceptance rate） | 需替代 KL 蒸馏 | N/A（训练方法） |
464	| Block Verification | 2403.10444 | 2024.03 | 验证粒度（block-level） | 无 | 是 |
465	| Multi-Path Block BV | 2602.16961 | 2026.02 | 验证粒度（tree block） | 无 | 是 |
466	| HiSpec | 2510.01336 | 2025.10 | 验证架构（intermediate verifier） | 需训练 EE model | 定期 full verify 兜底 |
467	| LayerSkip | 2404.16710 | 2024.04 | 验证架构（self-spec + EE） | 需训练 | 是 |
468	| PPSD | 2509.19368 | 2025.09 | 验证架构（pipeline overlap） | 需训练 EE head | 是 |
469	| FASER | 2604.20503 | 2026.04 | 验证调度（分块+重叠） | 无 | 是 |
470	| SV | 2509.24328 | 2025.09 | 验证长度（companion model） | 无 | 是 |
471	| TriSpec | 2601.23180 | 2026 | 验证架构（ternary proxy） | 无 | 是 |
472	| SPRINTER | 2502.04557 | 2025 | 验证架构（approximate verifier） | 需训练 verifier | 近似 |
473	| SpecPV | 2512.02337 | 2025 | 验证粒度（partial KV） | 无 | 定期 full verify |
474	| MineDraft | 2603.18016 | 2026.03 | batch 级（两批重叠） | 无 | 是 |
475	| ECHO | 2604.09603 | 2026.04 | batch 级（super-tree） | 无 | 是 |
476	| Mirror-SD | 2510.13161 | 2025.10 | 跨设备并行 | 无（需异构硬件） | 是 |
477	| SpecFormer | 2511.20340 | 2025.11 | draft 方式（非 AR） | 需训练 draft | 是 |
478	| Quasar | 2603.01399 | 2026.03 | 验证精度（量化） | 无 | 是 |
479	| MoE-Spec | 2602.16052 | 2026.02 | 验证开销（expert budget） | 无 | 是 |
480	| Nightjar | 2512.22420 | 2025.12 | 调度（自适应开关） | 无 | 是 |
481	| Hidden State 复用 | 2602.21224 | 2026.02 | 失败回收 | 需训练 draft | 是 |
482	| SpecMamba | 2509.19873 | 2025 | SSM state 回溯（三种 plan） | 无 | 是 |
483	| Mamba Drafters | 2506.01206 | 2025 | SSM 做 drafter | 需训练 Mamba drafter | 是 |
484	| Gating is Weighting | 2504.04308 | 2025 | GLA 理论（WPGD） | N/A | N/A |
485	| Nemotron 3 Super | 2604.12374 | 2026 | MTP + hybrid | 需训练 MTP head | 是 |
486	| DUET | 2603.15530 | 2026 | Disaggregated hybrid | N/A | N/A |
487	| FastEagle | 2509.20416 | 2025 | 非 AR cascaded draft | 需训练 | 是 |
488	| DDTree | 2604.12989 | 2026 | Block diffusion draft | 需训练 | 是 |
489	| SpecForge | 2603.18567 | 2026 | EAGLE-3 训练框架 | N/A | N/A |
490	| Sparse Verification | 2512.21911 | 2025 | 联合稀疏化验证 | 无 | 是 |
491	| SMART | 2604.09731 | 2026 | 树展开边际分析 | 无 | 是 |
492	| VOCABTRIM | 2506.22694 | 2025 | Draft 词表裁剪 | 无 | 是 |
493	| Alignment-Augmented SD | 2505.13204 | 2025.05 | Prefill 辅助+自适应阈值 | 无 | 是 |
494	| Global Resolution | 2511.15898 | 2025.11 | 多 draft 最优验证 | 无 | 是 |
495	| SpecGuard | 2604.15244 | 2026.04 | Step-level 验证 | 无 | 是 |
496	| EAGLE-Pangu | 2603.08088 | 2026 | NPU 移植 | 无 | 是 |
497	| OWL | 2510.07535, EMNLP 2025 | 2025.10 | LSTM drafter，长 context acceptance 4.00 vs EAGLE-3 1.28 | 需训练 | 是 |
498	| LongSpec | 2502.17421, ICML 2025 | 2025.02 | AOI 位置覆盖，Hybrid Tree Attention | 无（AOI）| 是 |
499	| SpecExtend | 2505.20776 | 2025.05 | Cross-model Retrieval，target attention score 指导 draft KV | 无 | 是 |
500	| RAPID | 2502.20330, ICML 2025 | 2025.02 | RAG drafter 缩短 context draft | 需训练 | 是 |
501	| TriForce | 2404.11912 | 2024.04 | 分层 spec decoding | 无 | 是 |
502	
503	---
504	
505	## 13. 第三轮补充调查（2026-04-27）
506	
507	### 13.1 SSM State Checkpoint/Rollback 新发现
508	
509	**Snakes and Ladders: Accelerating SSM Inference with Speculative Decoding**（arXiv:2402.00550, NeurIPS 2024 Workshop, UCLA + AWS AI）
510	
511	两种 SSM state backtracking 方法：
512	- **Activation Replay**：缓存 SSM block 的输入激活，回溯时只重跑 state update kernel 到最后验证通过的 token
513	- **Joint Attainment and Advancement**：在验证当前 draft 的同时前进一步，恢复到最后验证通过的 token 的 SSM state
514	
515	与 SpecMamba 的 Plan I/II 方案互补，但仅处理纯 SSM target。
516	
517	**STree**（arXiv:2505.14969, NeurIPS 2025）
518	
519	将 token tree 压平为单一序列 + tree mask，利用 SSM 状态转移矩阵的可加性，一次性前向计算 tree 上所有节点的输出，避免为每条路径重复展开 SSM。提出 custom tree scan kernel。明确声称适用于"hybrid SSM+Transformer"架构，但论文中的 hybrid 是指 Mamba+Attention 层交替排列的 target model，不处理外部 drafter。
520	
521	### 13.2 混合架构 + Spec Decoding 工程实践
522	
523	**SGLang MambaRadixCache + Speculative Decoding**（PyTorch Blog "Hybrid Models Meet SGLang"）
524	
525	已在 Qwen3-Next（Gated DeltaNet + Gated Attention 混合）上验证的关键设计：
526	- **双内存池设计**：Mamba pool + KV cache pool 独立管理
527	- **MambaRadixCache**：混合 radix tree，分别管理 SSM state 和 KV cache 的 prefix 匹配
528	- **State Snapshotting**：为每个 draft token 分配独立的 Mamba cache slot，解决 SSM state 不可逆问题
529	- **EAGLE-Tree with top-K > 1**：支持树形 draft + 混合架构
530	
531	**这是 MiniCPM-SALA 最直接可借鉴的工程实现**。
532	
533	**Marconi: Prefix Caching for the Era of Hybrid LLMs**（arXiv:2411.19379, MLSys 2025 Outstanding Paper Honorable Mention）
534	
535	第一个支持混合模型 prefix caching 的系统。SSM state 不可逆（只能精确匹配，不能部分重叠），采用审慎的 admission 策略——只在高复用概率时缓存 SSM state。SSM state 的 "all-or-nothing" 特性分析对理解 GLA verify 挑战很有价值。
536	
537	**Qwen3.5-27B 的 recurrent state 问题**（vLLM 论坛）
538	
539	Qwen3.5 的 conv_states 和 recurrent_states **没有 sequence_length 维度**，无法像 KV cache 那样选择性接受部分 token。如果 draft 包含 4 个 token 但 target 只接受前 2 个，系统无法恢复对应的 conv_states 和 recurrent_states。因此 Qwen3.5 目前只支持 MTP-1。
540	
541	**这正是 MiniCPM-SALA 的 GLA 层的核心挑战的直接映射**——recurrent state 是整体更新的，无法按 token 粒度截断。
542	
543	**vLLM GDN Attention Bug**（issue #38196）
544	
545	GDN（Gated DeltaNet）attention backend 在 ngram speculative decoding 产生 mixed decode + spec_decode batch 时崩溃。GDN builder 假设 num_decodes 和 num_spec_decodes 互斥，但部分拒绝时两者同时非零。
546	
547	**直接证明工业界在混合 linear attention 层的 speculative decoding 实现上存在基础性 bug**。
548	
549	### 13.3 Linear Attention + Speculative Decoding 兼容性
550	
551	**When Linear Attention Meets Autoregressive Decoding**（arXiv:2406.07368, ICML 2024, Georgia Tech + Google）
552	
553	第一个系统研究 linear attention 与 speculative decoding 的兼容性。发现：
554	- 标准 linear attention 的 causal mask 与 tree attention mask 不兼容
555	- 提出 local augmentation 技术增强 linear attention 的局部特征提取
556	- 开发 tree-based attention 与 linear attention 的无缝集成方案
557	
558	**高度相关**：论文直接解决了 linear attention 层在 tree verify 中的 causal mask 问题。
559	
560	### 13.4 Cactus 完整算法
561	
562	**Cactus**（arXiv:2604.04987, ICLR 2026 Poster）
563	
564	约束优化目标：最大化接受率，约束 KL(h || q) ≤ delta。
565	
566	最优解（Corollary 5，KL 散度 + 二阶 Taylor 近似）：
567	```
568	gamma* = min{q(n) + sqrt(2 * delta * q(n) * (1-q(n))), 1}
569	```
570	
571	q(n) 是 target model 对 draft token n 的概率。gamma* 给 draft token n 一个 "bonus probability"，bonus 最大值在 q(n)=0.5 时取得。
572	
573	delta 典型值：0.01~0.05。
574	
575	对 tree verify：理论上可以嵌入（每条边的 gamma* 不同），但论文未做 tree verify 实验。
576	
577	代码：https://github.com/MANGA-UOFA/Cactus
578	
579	### 13.5 MARS 完整算法
580	
581	**MARS**（arXiv:2601.15498, ICLR 2026）
582	
583	对每个 draft token v_t：
584	1. **Exact Match**：如果 v_t = target top-1，直接接受
585	2. **Adaptive Relaxation**：如果 v_t = target top-2 且 `r_t > theta`，接受（视为 tie）
586	3. **Rejection**：否则拒绝
587	
588	核心度量 **Logit Ratio**：`r_t = z_{(2)} / z_{(1)}`（top-2 logit / top-1 logit）
589	
590	theta **固定 0.9**，ablation 在 [0.85, 0.95] 稳定。
591	
592	实验数据：
593	
594	| Model | EAGLE-3 | MARS |
595	|-------|---------|------|
596	| Vicuna-13B | 3.12x / tau=5.64 | **3.74x / tau=7.20** |
597	| Llama-3.1-8B | 3.24x / tau=4.82 | **4.00x / tau=6.61** |
598	| Llama-3.1-70B | 4.61x / tau=5.86 | **4.76x / tau=6.53** |
599	
600	与 tree verify 兼容：每条边的验证独立应用 MARS 规则。
601	
602	代码：https://github.com/5SSjw/MARS
603	
604	### 13.6 SMC-SD 完整实现
605	
606	**SMC-SD**（arXiv:2604.15672）
607	
608	基于 SGLang fork，3 步循环：Extend → Reweight → Resample。
609	
610	ESS（Effective Sample Size）：`ESS = (sum w_n)^2 / sum w_n^2`。ESS 趋近 1 说明权重退化，需要 resample。
611	
612	粒子数 N：实验中 N=4~8。Roofline 模型分析：N 应选择使算术强度接近 GPU roofline ridge point。
613	
614	理论误差界（Theorem 3.1）：L2 bias = `O((1 + chi^2(p||q)) / N)`，L1 bias = `O(sqrt(...))`
615	
616	实验：比 optimized SD 快 2.36x，比 AR 快 5.2x，准确率在 target 3% 以内。
617	
618	代码：https://github.com/abdelfattah-lab/smcsd
619	
620	### 13.7 2026 最新论文
621	
622	**HSD: Hierarchical Speculative Decoding**（ICLR 2026 Oral）
623	
624	解决 sequence-level verification 的"联合不可解性"问题。将 resampling 组织为层次结构，在分支间重新分配概率质量。集成 EAGLE-3 获 **12% 性能提升**。Lossless。
625	
626	**SSD/Saguaro: Speculative Speculative Decoding**（ICLR 2026 Poster）
627	
628	将 draft 和 verify 阶段并行化。verify 进行时，draft model 预测 verify 结果并提前准备下一轮 speculation。比 SD baseline 快 **2x**，比 AR 快 5x。
629	
630	**LTD: Learning To Draft**（ICLR 2026 Poster）
631	
632	将 draft-verify 建模为 RL 环境，训练 co-adaptive policies 动态协调 draft 和 verify。直接优化 throughput，2.24x-4.32x 加速，**比 EAGLE-3 优 36.4%**。
633	
634	**DDTree + DFlash**（arXiv:2604.12989, 2026.04）
635	
636	从 block diffusion drafter 的 per-position 边缘分布构建 draft tree。Best-first heap 算法最大化期望接受长度。接受长度提升 **35%-63%**，峰值 8.22x 加速。已在 RTX 3090/DGX Spark 社区验证。
637	
638	**FLy: Accepting Semantically Correct Drafts Beyond Exact Match**（AMD ROCm Blog）
639	
640	Entropy-based gating + deferred window validation，允许语义正确但词汇不同的 draft 被接受。99%+ accuracy recovery。
641	
642	**RACER**（arXiv:2604.14885）
643	
644	AC 自动机 + LRU 淘汰构建 n-gram retrieval tree，与 logits tree 融合。Training-free，plug-and-play。
645	
646	**Super Apriel**（arXiv:2604.19877）
647	
648	15B supernet，每层 4 种 mixer（FA/SWA/KDA/GDN），运行时可切换。共享 checkpoint 可直接做 self-speculative decoding，无需单独 draft model。DIL/KIL 初始化方法可将 GDN/KDA 层注入已有 transformer。
649	
650	**Mamba-3**（arXiv:2603.15569, ICLR 2026 Oral）
651	
652	Trapezoidal discretization + MIMO + 复值状态更新。1.5B scale 用一半状态大小匹配 Mamba-2 perplexity。
653	
654	**ConFu: Contemplate the Future**（arXiv:2603.08899）
655	
656	通过 contemplate tokens 和 soft prompts 让 draft model 获取 target model 的"未来信号"。
657	
658	### 13.8 SGLang 工程实现细节
659	
660	**SGLang Adaptive Speculative Decoding**（已落地）：
661	- EMA 策略：每轮 verify 后读取 accepted draft length，用指数移动平均平滑
662	- 预建候选层：启动时为每个候选 tier（默认 [1,3,7]）预建 CudaGraphRunner
663	- **当前限制**：只支持 `--speculative-algorithm EAGLE` + `--speculative-eagle-topk 1`
664	
665	**Tree Verify Kernel**：
666	- Greedy 路径：`verify_tree_greedy_func()` 调用 `sgl_kernel.verify_tree_greedy` CUDA kernel
667	- Sampling 路径：`tree_speculative_sampling_target_only()` kernel
668	- **draft_probs = torch.zeros(...)**：当前代码走 target-only 验证，不使用 draft model 的概率分布
669	
670	**SGLang 最新 spec 算法扩展**：
671	- **P-EAGLE**（Issue #23171）：并行 EAGLE，一次 forward 生成所有 K 个 draft token
672	- **DDTree**（Issue #22887）：扩散 draft tree
673	- **SSD/Saguaro**（Issue #19896）：异步推测解码
674	- **Spec V2**（`SGLANG_ENABLE_SPEC_V2`）：STANDALONE draft model
675	
676	### 13.9 量化 + Spec Decoding 实践
677	
678	**QSpec**（arXiv:2410.11305, EMNLP 2025 / ICLR 2025 提交）：
679	- W4A4 做 draft（快但不准），W4A16 做 verify（准但慢），**共享权重和 KV cache**
680	- 接受率 93-95%，加速 1.64-1.80x，无质量损失
681	- **不适用 NVFP4**：需要 W4A4 kernel，sm_120 无此 kernel
682	
683	**SpecMQuant**（arXiv:2505.22179）：
684	- **4-bit 量化模型上 tree-style verify 时间开销远大于 single-token forward pass**
685	- 解决方案：层次化框架，用小模型做中间阶段将 tree drafts 转为 sequence drafts
686	- W4A16 Llama-3-70B 上 **2.78x** 加速，比 EAGLE-2 快 1.31x
687	
688	**NVFP4 target logits 精度**：
689	- NVIDIA 数据：DeepSeek-R1-0528 从 FP8 到 NVFP4 精度差 <1%（MMLU-Pro, GPQA Diamond）
690	- vLLM：MTP spec + Marlin NVFP4 路径 -22% throughput（activation distribution mismatch）
691	- 关键问题：放松验证叠加量化误差，MARS 的 logit ratio 在量化 logits 上可能更不稳定
692	
693	### 13.10 生产环境 Spec Decoding 经验
694	
695	**Acceptance Rate 与加速比**：
696	- alpha=0.6 → ~2.4x 加速
697	- alpha=0.8 → ~3.7x 加速
698	- **alpha < 0.5 时 spec decode 比 baseline 更慢**
699	
700	**Batch Size 与 Spec Decoding**：
701	- bs 1-4：GPU memory-bound，spec 有效
702	- bs 8-32：过渡区域
703	- bs 32+：compute-bound，spec 通常更慢
704	- **长上下文反转**：MagicDec 发现当 KV cache 成为瓶颈时，大 batch + 长上下文 spec 仍可 2x 加速
705	
706	**Acceptance Rate 波动**：
707	- 代码生成 alpha ~70-80%，数学推理 50-60%，开放聊天 40-60%
708	- 同一请求内位置方差极大；请求间方差大 → ragged tensor
709	- 生产部署通常比实验室数据低 40-60%
710	
711	### 13.11 文献空白确认（第三轮）
712	
713	经三轮系统性搜索，**确认不存在**专门解决"混合 standard attention + GLA/SSM target model + 外部 EAGLE drafter 的 tree verify + GLA state checkpoint/rollback"的论文。
714	
715	最接近的四个方案：
716	1. **SGLang MambaRadixCache + per-draft-token Mamba cache slot**（工程方案，Qwen3-Next 上已验证）
717	2. **STree 的累积状态转移矩阵**（理论方案，custom GLA tree scan kernel）
718	3. **Snakes & Ladders 的 Activation Replay**（baseline 方案，缓存输入激活重算）
719	4. **Qwen3.5/vLLM 的现状**（反面教训：recurrent state 无 sequence_length 维度）
720	
721	### 13.11b BanditSpec — Per-Request Adaptive Spec Steps（arXiv:2505.15141, 2026）
722	
723	**定位**：每请求独立 UCB 多臂老虎机，自适应选择最优推测步数（dtn）。
724	
725	**算法**：
726	- Arms = `{dtn=3, dtn=5, dtn=7}`，每个请求独立维护 UCB 统计量
727	- Reward = 每步 accept_length（整数，greedy 完全兼容）
728	- UCB 选择：`arm* = argmax_a (mean_a + c * sqrt(log(t) / n_a))`
729	
730	**为什么对 MiniCPM-SALA 有效**：
731	- vlong bucket（p_tok≥50K）avg_al=0.40，dtn=5 等效效率仅 8%（每 5 token verify 成本只换 0.4 token）
732	- 收敛到 dtn=3 后效率 0.40/3=13.3%（**+63% 相对提升**）
733	- 编程 bucket avg_al~2.5，dtn=7 可能更优；UCB 自动发现请求级最优
734	
735	**工程成本**：约 100 行 Python，`eagle_worker.py` 中 per-req state dict `{rid → UCBArm}`。完全不改任何 kernel。
736	
737	**论文数据（混合 workload，greedy）**：+20–35% throughput 估算（论文未细拆 per-bucket，整体 workload 含短/长混合）。
738	
739	**Greedy 兼容性**：信号 = accept_length（整数，不依赖概率分布）。完全兼容。
740	
741	---
742	
743	### 13.12 方法组合兼容性
744	
745	- **MARS + Traversal Verification**：可叠加（MARS 改单 token 判定，Traversal 改 tree 遍历策略）
746	- **MARS + Block Verification**：可叠加但需重新推导 BV 最优性
747	- **Cactus + Block Verification**：可叠加（Cactus 修改的分布 h 嵌入 BV 框架）
748	- **SMC-SD + 其他方法**：基本不兼容（不同范式：resampling vs rejection）
749	- **推荐组合**：MARS（最易）→ Traversal Verification（可叠加）→ Block Verification（lossless +5-8%）
750	
751	**T=0 Greedy 不兼容方法**（2026-04-27 确认）：
752	- **Block Verification**：需要 joint probability compensation，T=0 时 p_draft 退化为 0/1，无意义
753	- **Cactus**：`gamma*=min{q(n)+sqrt(2δq(n)(1-q(n))),1}`，T=0 时 q(n*)=1/q(n≠n*)=0 → 退化为 exact-match
754	- **SMC-SD**：importance resampling 需要 p_draft(x) 概率值
755	
756	**batch=1 低 ROI 方法**（2026-04-27 确认）：
757	- **SMART**：硬件感知边际分析，设计假设是 compute-bound large batch。batch=1 实测 2.17× vs baseline 2.20×（无收益）
758	
759	### 13.13 第三轮新增论文索引
760	
761	| 论文 | arXiv ID | 时间 | 核心发现 |
762	|---|---|---|---|
763	| Snakes and Ladders | 2402.00550 | 2024.02 | SSM Activation Replay + Joint Attainment |
764	| When Linear Attention Meets SD | 2406.07368 | 2024.06 | Linear attention causal mask 与 tree mask 不兼容 |
765	| Marconi | 2411.19379 | 2024.11 | 混合模型 prefix caching，SSM state all-or-nothing |
766	| SpecMQuant | 2505.22179 | 2025.05 | 4-bit 量化上 tree verify 开销大，需层次化框架 |
767	| HSD | ICLR 2026 Oral | 2026 | 层次化 SD，集成 EAGLE-3 +12% |
768	| SSD/Saguaro | ICLR 2026 Poster | 2026 | draft-verify 并行化，2x over SD |
769	| LTD | ICLR 2026 Poster | 2026 | RL 自适应 draft-verify，+36.4% over EAGLE-3 |
770	| DDTree+DFlash | 2604.12989 | 2026.04 | 扩散 draft tree，+35-63% acceptance |
771	| RACER | 2604.14885 | 2026 | AC 自动机 n-gram retrieval tree |
772	| BanditSpec | 2505.15141 | 2026 | Per-req UCB 自适应 dtn，greedy 兼容，est +20–35% |
773	| Super Apriel | 2604.19877 | 2026 | Supernet self-spec，4 种 mixer 可切换 |
774	| Mamba-3 | 2603.15569 | 2026 | ICLR Oral，trapezoidal discretization + MIMO |
775	| ConFu | 2603.08899 | 2026 | Contemplate tokens 获取 target 未来信号 |
776	| FLy (AMD) | AMD Blog | 2026 | Entropy gating + deferred window validation |
777	| FR-Spec | 2502.14856 | 2025 | ACL Main，高频 token 子集采样，+1.12x |
778	
779	---
780	
781	## 14. 架构背景参考
782	
783	### 14.1 EAGLE 架构演进
784	
785	| 版本 | 会议/时间 | 核心创新 |
786	|---|---|---|
787	| EAGLE-1 | ICML 2024, arXiv:2401.15077 | Feature-level autoregression，采样 feature 而非 argmax，固定 25 节点树 |
788	| EAGLE-2 | EMNLP 2024, arXiv:2406.16858 | 动态 draft tree，根据 confidence 自适应，比 v1 快 1.4× |
789	| EAGLE-3 | NeurIPS 2025, arXiv:2503.01840 | Direct token prediction，三层特征融合，TTT（Training-Time Test），8× 数据→1.4× 加速，最大 6.5× |
790	
791	**EAGLE-3 核心论文数据**（SGLang + H100 + LLaMA-3.1-8B）：
792	
793	| 方法 | Throughput (bs=1) | 加速比 |
794	|---|---|---|
795	| SGLang 无推测 | 158.34 tok/s | 1.00× |
796	| SGLang + EAGLE-2 | 244.10 tok/s | 1.54× |
797	| SGLang + EAGLE-3 | 373.25 tok/s | **2.36×** |
798	
799	### 14.2 MiniCPM 模型系列
800	
801	| 模型 | 论文/时间 | 核心特性 |
802	|---|---|---|
803	| MiniCPM | arXiv:2404.06395, 2024.4 | 1.2B/2.4B SLM，WSD 调度器，Chinchilla Optimal 数据比 |
804	| MiniCPM-3 | 2024 | 4B 参数迭代版本 |
805	| MiniCPM4 | arXiv:2506.07900, 2025.6 | InfLLM-v2 可训练稀疏注意力，BitCPM 三值量化，CPM.cu 推理框架 |
806	| MiniCPM4.1 | 2025.9 | 融合思维推理能力，EAGLE3 推测解码 3× 加速 |
807	| MiniCPM-SALA | 2026.2 | SALA 混合注意力（8 sparse + 24 GLA），HyPE，HALO 蒸馏，1M+ context |
808	
809	注：SGLang 和 vLLM 目前仅支持 MiniCPM4/4.1 的 dense attention 推理模式；sparse 推理需用 HuggingFace Transformers 或 CPM.cu。
810
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/dflash.md"
}
```

> TOOL

tool_result Read
```
1	# DFlash — 下一代 Draft 候选方案
2	
3	**定位**：不是 EAGLE 的变种，是**范式级替代**。Block diffusion 一次 forward 预测 16 token，吞吐上限远高于 EAGLE chain。作为 EAGLE-3 封顶后的**下一代 draft**。
4	
5	参考：
6	- Repo: https://github.com/z-lab/dflash
7	- Paper (预印): arxiv:2602.06036
8	- 本地 clone: `~/dflash/`
9	- 官方模型: `z-lab/Qwen3.5-4B-DFlash`（HuggingFace）
10	
11	## 1. 核心机制（纠正"K/V 共享"的误解）
12	
13	DFlash **不是**"用 target 的 K/V cache 替代 draft 的"。而是把 target 多层 hidden 作为 **cross-attention 的 context tokens**：
14	
15	```python
16	# Draft 的每层 attention layer（Qwen3DFlashAttention.forward）
17	q = self.q_proj(noise_embedding)         # query 来自 noise (mask_tokens 的 embedding)
18	k_ctx = self.k_proj(target_hidden)       # draft 自己的 k_proj 作用在 target hidden 上
19	v_ctx = self.v_proj(target_hidden)       # draft 自己的 v_proj
20	k_noise = self.k_proj(noise_embedding)
21	v_noise = self.v_proj(noise_embedding)
22	k = cat([k_ctx, k_noise], dim=1)
23	v = cat([v_ctx, v_noise], dim=1)
24	attn(q, k, v)  # noise 的 query 同时 attend 到 target ctx + noise 自身
25	```
26	
27	三种方案对照：
28	
29	| | input | 谁持有 k_proj/v_proj | 一次出几个 token |
30	|---|---|---|---|
31	| **EAGLE-3** | target hidden 3 层拼接 → `fc` → draft hidden_state | draft self-attn | 1（每 chain step） |
32	| "K/V 共享"（罕见） | 复用 target K/V cache | target | 1 |
33	| **DFlash** | target hidden 5 层拼接 + mask_token embedding | draft cross-attn（query=noise, K/V=投影后 target hidden + noise） | **16**（block_size） |
34	
35	## 2. DFlash Config（从 `z-lab/Qwen3.5-4B-DFlash` 提取）
36	
37	| 参数 | 值 |
38	|---|---|
39	| `num_hidden_layers` | **5**（EAGLE-3 只 1 层） |
40	| `hidden_size` | 2560 |
41	| `intermediate_size` | 9728 |
42	| `num_attention_heads` / `num_key_value_heads` | 32 / 8 (GQA) |
43	| `block_size` | **16** |
44	| `target_layer_ids` | **[1, 8, 15, 22, 29]**（32 层均匀 5 层） |
45	| `mask_token_id` | 248070 |
46	| `tie_word_embeddings` | True |
47	
48	## 3. 训练配方（反推，置信度高）
49	
50	**数据采集**：
51	
52	```python
53	for prompt in dataset:
54	    out = target(prompt, output_hidden_states=True)
55	    # hidden_states[0]=embed, hidden_states[k+1]=layer k 输出
56	    target_hidden = concat([hidden_states[lid + 1] for lid in target_layer_ids])
57	    save({'token_ids': out.sequences, 'target_hidden': target_hidden})
58	```
59	
60	**训练 step**（block 级 denoising CE loss）：
61	
62	```python
63	# batch: token_ids (B,T), target_hidden (B, T, 5*hidden)
64	for block_start in range(0, T - block_size, block_size):
65	    noise_tokens = tokens[:, block_start:block_start+block_size].clone()
66	    noise_tokens[:, 1:] = MASK_ID                    # pos 0 真, pos 1..15 mask
67	    noise_emb = embed(noise_tokens)
68	
69	    ctx = target_hidden_projected[:, :block_start+1, :]
70	    out = draft(noise_emb, ctx, position_ids=arange(block_start, block_start+16))
71	    logits = lm_head(out)
72	    loss = F.cross_entropy(logits[:, :-1], tokens[:, block_start+1:block_start+16])
73	```
74	
75	**超参推测**：AdamW, lr=1e-4~3e-4, betas=(0.9, 0.95), wd=0.01, cosine + linear warmup, grad_clip=1.0, bf16 native, 2-5 epochs。**没有 FP4_QAT**（DFlash 是 bf16 draft）。
76	
77	## 4. 推理流程（摘自 `dflash.model.dflash_generate`）
78	
79	```
80	1. Prefill: target(input_ids) → target_hidden[0:N] + 首 token
81	2. 每块主循环:
82	   a. block_input = [last_accepted_token, MASK*15]  (长度 16)
83	   b. noise_emb = embed(block_input)
84	   c. draft forward: query=noise_emb, context=target_hidden[0:start]
85	      → 同时输出 16 个 logits
86	   d. block_output[:, 1:] = argmax(draft_logits)
87	   e. target forward(block_output) → 16 个 posterior
88	   f. acc_len = prefix-match(block_output[1:], posterior[:-1])
89	   g. 提交 acc_len+1 个 token，target_hidden += hidden[accepted 位置]
90	   h. start += acc_len + 1
91	```
92	
93	单 forward 出 block_size=16 token（非 EAGLE chain 1 个）。bs=1 decode 吞吐大幅提升。
94	
95	## 5. GLA chain verify rollback — 现有 infra 免费支持（关键优势）
96	
97	**核心结论**：DFlash chain verify 相对 EAGLE tree verify 在 SALA 上有**结构性优势**，不需要 tree-aware kernel。
98	
99	**代码验证**（`demo-sala/.../hybrid_linear_attn_backend.py:1562`）：
100	
101	```python
102	# update_mamba_state_after_mtp_verify 核心一行
103	ssm_states[:, dst_state_indices, :] = intermediate_state_cache[
104	    :, src_state_indices, last_steps   # last_steps 是 (N,) 索引张量
105	]
106	```
107	
108	- `intermediate_state_cache` 形状 `(num_layers, req, draft_token_num, K*V)`
109	- GLA fused kernel 在 verify 时已把 h_0..h_{block_size-1} 全算好缓存
110	- Rollback = 一次 fancy-indexed scatter，`O(req_num × state_dim)`，**和 block_size 无关**
111	
112	**两阶段成本分解**：
113	
114	| Phase | 开销 | 和 block_size 关系 |
115	|---|---|---|
116	| GLA forward (compute h_0..h_15) | O(block_size) | ✅ 线性 |
117	| Rollback (scatter intermediate → committed) | O(req_num) | ❌ **无关**，block_size=16 和 =1 同成本 |
118	
119	**为什么 chain 比 tree 在 GLA 上干净**：
120	
121	- **Tree**：sibling c2 本应从 user_4813494d 分叉，GLA 递推 flat 序列让 c2 继承 c1 state → 污染。Plan A FP32 index_select 205ms net-negative，Plan C 300 行 Triton 未做。
122	- **Chain**：h_t 天然从 h_{t-1} 来，GLA 递推语义与 chain verify 语义完全一致 → **无污染，无需新 kernel**。
123	
124	这是 DFlash 在 SALA 上的关键优势：**绕过最大技术债**（GLA tree pollution），复用现有 `intermediate_ssm` + `update_mamba_state_after_mtp_verify` 完全够用。
125	
126	## 6. 移植 MiniCPM-SALA 的障碍
127	
128	**🔴 高 🟡 中 🟢 低**
129	
130	| # | 障碍 | 级别 | 解决方向 |
131	|---|---|---|---|
132	| 1 | 官方只支持 Qwen3 / LLaMA-3.1 / Kimi / gpt-oss，无 MiniCPM | 🔴 | 自写 `MiniCPMDFlashDraftModel`（照搬 Qwen3，换 MLP/attn 为 MiniCPM 结构） |
133	| 2 | SALA 24/32 层是 Lightning (GLA)，hidden 语义不同于标准 attn | 🟡 | target_layer_ids 避开 GLA 层：从 attention 层 [0,9,16,17,22,29,30,31] 选 5 个（如 [0,9,17,22,30]） |
134	| 3 | 训练配方未开源（README 承诺 "soon"） | 🟡 | 按 §3 反推自训；若 repo 放出再校准 |
135	| 4 | `mask_token_id` 要占 1 个 vocab 位（MiniCPM vocab 73448） | 🟢 | 选末端未用的 id（如 73447） |
136	| 5 | block diffusion + SALA 长序列 attention (dense_len=8192 + sparse) 交互未知 | 🟡 | 先短序列 (2K) 验证，再扩 |
137	| 6 | SGLang 需加 `--speculative-algorithm DFLASH` 的 MiniCPM 支持 | 🟡 | 可能需要 patch SGLang（DFlash 已在 sglang PR 20547） |
138	| 7 | draft 5 层 × hidden 2560 ≈ 65M params/layer，比 EAGLE 1 层重 5× | 🟡 | 先降到 2-3 层做初验 |
139	
140	## 7. 最小可行验证（MVP）
141	
142	**目标**：证明 block diffusion 在 SALA 上能收敛到 accept_len > 1.50（超过当前 EAGLE-3）。
143	
144	**数据**：
145	
146	- 用现成 `eagle/data/train/` 改造 → 额外保存 5 层 target hidden（非 3 层）
147	- hook 调整：`_EAGLE3_AUX_LAYERS = [0, 9, 17, 22, 30]`（全选 full_attention 层）
148	- 样本数减半（10k）先验证 pipeline
149	
150	**模型**：
151	
152	- `DFlashDraftModel_SALA`：2 层（先验证）× hidden=2560
153	- block_size=8（非 16）
154	- bf16 训练（非 FP4_QAT）
155	
156	**训练**：
157	
158	- 1 epoch 看 loss 曲线 + val_ood block accept-len
159	- 通过门槛：val_ood block accept-len > 2.0
160	
161	**时间预算**：3-4 天研发（代码移植 1-2 天 + 数据重采 4-6 hrs + 1 epoch 训练 ~10 hrs）。
162	
163	## 8. 激活决策树
164	
165	```
166	EAGLE-3 v2 训练结果 →
167	  ├─ accept_len > 1.70: 继续优化 EAGLE-3（response-only mask, aux_layer 调优）
168	  ├─ accept_len ∈ [1.55, 1.70]: 两轮 EAGLE-3 + 一轮 DFlash 小验证 并行
169	  └─ accept_len ≤ 1.55: 立即切 DFlash 验证（EAGLE-3 封顶）
170	```
171
```

> AGENT

我将系统地调查量化与内核相关的所有技术工作。让我先从阅读关键文档和搜索相关代码开始。

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/quantization.md"
}
```

> TOOL

tool_result Read
```
1	# 量化与 Marlin
2	
3	## 1. NVFP4 量化方案
4	
5	**算法**：GPTQ + FourOverSix（adaptive 4/6 block scale），`lm_head` Identity patch  
6	**校准**：wikitext loguniform 128 samples，8 buckets（512-64K log-uniform）  
7	**推理要求**：`--dense-as-sparse`（dense_len=0，全序列走 sparse TopK 路径）
8	
9	### 校准实验结果
10	
11	| Config | Calibration | max_length | FourOverSix | dense-as-sparse | ori_accuracy |
12	|---|---|---|---|---|---|
13	| baseline | calib90 (eval mix) | 24K | ❌ | ✅ | 80.27%（不稳定） |
14	| **chosen** | **loguniform 128 (wikitext)** | **48K** | **✅** | **✅** | **79.98%** |
15	| exp | loguniform 128 | 48K | ✅ | ❌ | 78.18% |
16	| exp | calib90 | 72K | ✅ | ✅ | 77.04%（不达标） |
17	
18	## 2. FourOverSix (4/6) 实现
19	
20	MIT-HAN Lab 方案。标准 NVFP4 固定 block scale÷6；FourOverSix 对每个 block 比较 scale=4 和 scale=6 的 MSE，选更小者。输出格式不变（4-bit FP4 权重 + FP8 block scales），zero throughput impact。
21	
22	```python
23	scale_4 = fp8(scale_6.float() * 1.5)    # scale=4: 权重映射到 [-4, 4]
24	mse_6 = sum((W_group - dequant(W_group, scale_6))^2)
25	mse_4 = sum((W_group - dequant(W_group, scale_4))^2)
26	new_scale = where(mse_4 < mse_6, scale_4, scale_6)
27	```
28	
29	实测 40-43% blocks 选 scale=4；MLP 层比 Attention 层获益更大。
30	
31	### 集成方式
32	
33	直接 patch `llmcompressor/modifiers/quantization/gptq/gptq_quantize.py`，在 observer 输出 scale 后、GPTQ 优化循环前插入 scale 选择。`prepare_env.sh` 用 `cp patches/gptq_quantize_fouroversix.py $GPTQ_TARGET` 覆盖。
34	
35	## 3. Hybrid Marlin/CUTLASS Dispatch
36	
37	Target model decode 时 M 小 → Marlin W4A16（BF16 activation）显著快于 CUTLASS W4A4。
38	
39	**当前策略**：全局阈值 `SGLANG_MARLIN_DECODE_THRESHOLD=48`。M ≤ 48 → Marlin；M > 48 → CUTLASS。
40	
41	### 实现
42	
43	- `process_weights_after_loading`：CUTLASS prep 先跑，然后 `_prepare_hybrid_marlin` 从原权重创建 Marlin 格式。两种格式共存，额外 VRAM ~4 GB。
44	- `apply()`：M ≤ threshold → Marlin；否则 → CUTLASS。CUDA graph safe。
45	
46	**b12x 2-tier dispatch**（开发完成，当前未启用）：已通过正确性验证（见 [`kernels-sm120.md §7.4`](kernels-sm120.md)），但 `SGLANG_ENABLE_B12X` 默认为 0，当前提交包不启用。启用后走 per-shape Marlin/b12x/CUTLASS 三路分流，draft model 不兼容 b12x 始终走纯 Marlin。
47	
48	### sgl-kernel 修复
49	
50	平台 sgl-kernel 0.3.20 的 `marlin_template.h` 有 FP4 scale `/2` bug（cos_sim 0.77）。修复：pre-built `common_ops.abi3.so`（SM120a）via `cp` 替换。
51	
52	### Draft Model
53	
54	Draft model 永远用**纯 Marlin（no hybrid）**，M=1-6 时 CUTLASS 比 BF16 还慢：
55	
56	| Layer | Marlin | CUTLASS | 倍率 |
57	|---|---|---|---|
58	| gate_proj (N=16384) | 16.4 us | 48 us | 2.9× |
59	| down_proj (K=16384) | 20.5 us | 154 us | 7.5× |
60	| o_proj (4096×4096) | 10.3 us | 41 us | 3.9× |
61	
62	实现：`_detect_draft_model_quantization()` 检测到 FP4 draft 时设 threshold=9999。
63	
64	## 4. Marlin 调优负结果（勿重复踩坑）
65	
66	| 方向 | 结论 | 原因 |
67	|---|---|---|
68	| pipe_stages 4→6 | gate_up +5-8%，其余 0%，e2e <0.5% | down 撞 HBM roofline；qkv/o L2 驻留变 compute-bound |
69	| `use_fp32_reduce=False` | M=4-8 退化 9-17% | dispatcher 走不同 tile |
70	| native FP4 MMA (mma.kind=nvf4) | 不可行 | PTX 要求 A+B 都必须 FP4，无 W4A16 路径 |
71	| tile/warp sweep | 无意义 | HMMA:HFMA2 = 1:11，换 tile 不改 HFMA2 数量 |
72	| gn-kernels dequant 手优化 | 无货可抄 | gn-kernels 用 native MMA，没有 dequant 代码 |
73	| QuTLASS MXFP4 | 未测 | sm_120a 原生 Blackwell FP4 MMA，环境匹配未 build |
74	
75	**Pareto 判定**：Marlin 在 sm_120 W4A16 M=1-8 decode 已近最优。继续压 kernel ROI < 2%。
76	
77	### SASS 分析（gate_up M=1）
78	
79	```
80	HMMA (tensor core):                48 条
81	HFMA2+HADD2+HMUL2 (CUDA core FP):  532 条
82	LOP3+SHF+PRMT (FP4→BF16 dequant):  454 条
83	地址计算:                           536 条
84	```
85	
86	HMMA:HFMA2 = 1:11，张量核严重空转。瓶颈是 CUDA core dequant，不是 HBM 或 tensor core。
87	
88	## 5. KV Cache 量化调研
89	
90	- **FP8 KV**（生产）：`--kv-cache-dtype fp8_e5m2`，高并发稳定收益。FlashInfer `BatchDecodeWithPagedKVCacheWrapper` 吃 fp8 buffer + kernel 内 on-the-fly dequant，省 HBM 读带宽
91	- **NVFP4 KV**：在 SALA 当前架构下**没有可落地路径**。老版本"`trtllm_batch_decode_with_kv_cache` 未传 `kv_block_scales`"的结论已过时（FlashInfer 0.6.8 已支持），真正阻塞点是 InfLLM-v2 sparse + page_size=1 的组合。完整调研（API 约束、SGLang fork latent bugs、全球 30+ 项目盘点、离线微基准数据、三条理论路径评估）见 [nvfp4-kv-investigation.md](nvfp4-kv-investigation.md)
92	- **VariableBlockSparseAttentionWrapper**（FlashInfer v0.2）：离线实测对 SALA 现有 `BatchPrefill` baseline 整体打平或略慢，内部 kernel 路径等价，不带来加速
93	
94	## 6. Health check 注意
95	
96	NVFP4 量化后模型在 mcq 强格式约束下会退化为重复 pattern，但 eval regex 仍命中 → `ori_accuracy` 看似正常实则生成垃圾。**健康检查必须用 chat 长样本，不用 mcq。**
97
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/kernels-sm120.md"
}
```

> TOOL

tool_result Read
```
1	# sm_120 NVFP4 Kernel 现状与优化空间
2	
3	## 1. 结论速览
4	
5	- **硬件上限**：sm_120 NVFP4 block-scaled MMA 真实 peak ≈ **1467 TFLOPS**（pure-MMA probe，2 block/SM 达到，实测对齐理论值 1553 TFLOPS 的 ~95%）。
6	- **生态现状**：CUTLASS / cuBLAS / cuDNN / sgl-kernel 全部实测 ~560 TFLOPS，**仅挤出 peak 的 38%**，有 **2.6× 理论空间**。
7	- **决策洼地**：不是 ISA 上限，是官方全家桶 + 社区 kernel 的共同未调优状态。autotune 可 vary 的维度比预期窄（硬件约束），但 schedule / stages / epilogue fusion 仍未开发。
8	- **Marlin 不是优化对象**：decode 热形状（gate/up/down M=1/8）已实测 82-97% L2 带宽饱和，sm_120-native W4A16 重写无可挤空间。
9	- **b12x backend（PR #3051）** 已集成并默认启用（`SGLANG_ENABLE_B12X=1`）：2-tier dispatch Marlin/b12x + 3 点 CUTLASS override，覆盖 6 个形状（5 target + eagle_fc）× 全 M 范围（58 个 tile 配置），decode GEMM 62% 走 b12x。不再依赖 `SGLANG_MARLIN_DECODE_THRESHOLD`。关键 gotcha：b12x 必须喂 `layer.weight_scale_interleaved`（post-permute TMA-swizzled 格式），不是 pre-permute padded_scales（见 §7.4）。
10	
11	## 2. MMA 指令与硬件 peak
12	
13	**PTX（CUTLASS 生成）**：
14	
15	```
16	mma.sync.aligned.kind::mxf4nvf4.block_scale.scale_vec::4X.m16n8k64
17	  .row.col.f32.e2m1.e2m1.f32.ue4m3
18	```
19	
20	- `m16n8k64`：每指令 16×8×64×2 = 16384 FLOPs
21	- 每 16 个 k 元素一个 ue4m3 scale，4 scale/tile
22	- accumulator f32
23	- **block-scaled 相对 unscaled 慢 ~3×**，是 ISA 级开销
24	
25	**pure-MMA peak**（`bench/pure_mma_peak/`）：寄存器常驻 A/B/scale，`ACC=8` 独立累加器消除依赖，`INNER=64` 循环展开。
26	
27	| blocks/SM | warps/SM | TFLOPS | cycles/MMA |
28	|---|---|---|---|
29	| 1 | 4 | 1447 | 16.1 |
30	| **2** | **8** | **1467** | 24.2 |
31	| 4 | 16 | 1423 | 134 |
32	| 8 | 32 | 1152 | 77 |
33	
34	**推算**：4 tensor partitions/SM × (1 MMA / 16 cycles) × 156 SMs × 2.43 GHz × 16384 FLOPs = **1553 TFLOPS 理论**，实测 1467 差 5–7%（时钟/同步噪声）。
35	
36	## 3. 各 GEMM 库对比（M=8192 标定点）
37	
38	| Library | 路径 | gate_proj TFLOPS | 备注 |
39	|---|---|---|---|
40	| sgl-kernel `cutlass_scaled_fp4_mm` | `Sm120` builder, tile=256×128×128 | 550 | 当前 SALA 默认 |
41	| flashinfer `mm_fp4` backend=cutlass | 同底 CUTLASS | 547 | — |
42	| flashinfer `mm_fp4` backend=cudnn | cuDNN 路径 | 551 | 和 CUTLASS 打平 |
43	| flashinfer `mm_fp4` backend=trtllm | — | 不支持 sm_120 | BackendSupportedError |
44	| flashinfer `mm_fp4` backend=cute-dsl | — | 不支持 sm_120 | 同上 |
45	| `torch._scaled_mm` (cuBLAS 13.4) | via `VEC16_UE4M3` scale mode | 553 | PyTorch 2.11 暴露 |
46	
47	**四个库一致 ~550 TFLOPS** = 生态共同的未调优状态。
48	
49	## 4. sgl-kernel 当前 dispatch
50	
51	`csrc/gemm/nvfp4_scaled_mm_kernels.cu` 只 hard-code 两个 sm_120 config：
52	
53	| 触发条件 | MmaTile (M×N×K) | Cluster | Schedule |
54	|---|---|---|---|
55	| `next_pow_2(M) ≤ 256` | 128 × 128 × 128 | 1×1×1 | Auto（实测 Cooperative, stages=3） |
56	| `M > 256` | 256 × 128 × 128 | 1×1×1 | 同上 |
57	
58	**Prefill M=8192 永远走第二个**。N 维和 K 维都从未扩过。
59	
60	### 4.1 flashinfer 0.6.8.post1 已带 sm_120 autotune 池（PR #2460）
61	
62	2026-03 合入的 [flashinfer PR #2460](https://github.com/flashinfer-ai/flashinfer/pull/2460) 把 sm_120 `mm_fp4(backend="cutlass")` 的候选 tile 从"只有 128×128×128 DP"扩到 **3 tile × 2 schedule = 6 tactic**：
63	
64	```cpp
65	// flashinfer/data/include/flashinfer/gemm/fp4_gemm_cutlass_template_sm120.h:168
66	tactic 0: 128×128×128  Auto  DP      (== 旧 fallback，tactic=-1 等价)
67	tactic 1: 128×128×128  Auto  StreamK
68	tactic 2: 128×128×256  Auto  DP
69	tactic 3: 128×128×256  Auto  StreamK
70	tactic 4: 256×128×128  Auto  DP
71	tactic 5: 256×128×128  Auto  StreamK
72	```
73	
74	PR 给的收益数字是 **M=32, N=5120, K=25600 → 1.8× on sm_120**，但只是单点。PR 未内置 autotune cache，我们必须离线 tune + 落盘复用（见 §7.1）。
75	
76	## 5. sm_120 tile 空间硬件约束
77	
78	实测编译 12 个候选，成功 5 个：
79	
80	### 成功（有效 autotune 维度）
81	`128×128×128`, `256×128×128`（sgl 默认两种）, `128×256×128`, `256×256×128`, `128×128×256`
82	
83	### 失败
84	
85	| Config | 错误 | 根因 |
86	|---|---|---|
87	| `256×128×256` / `128×256×256` / `256×256×256` | `Specialization requires Stages set to value 2 or more` | sm_120 每 SM ~100 KB smem，扣 epilogue 后装不下 2 份大 tile |
88	| `64×128×128` / `128×64×128` / `64×256×128` / `256×64×128` | `TMA requires CTA_Tile and SLayout top-level size equivalence` | CUTLASS sm_120 block-scaled TMA atom 最小 M/N = 128 |
89	| `Cluster > 1` | `no programmatic multicast on this arch` | sm_120 无 distributed shared memory（tcgen05 专属） |
90	
91	**有效 tile 空间**：`{128, 256} × {128, 256} × {128}` + `(128, 128, 256)`，Cluster 锁死 1×1×1。
92	
93	## 6. W4A4 vs W4A16：小 M 的结构性差异
94	
95	Marlin (W4A16) vs CUTLASS (W4A4)，M=1 gate_proj：
96	- Marlin: 16.5 us
97	- CUTLASS NVFP4: 48 us（3× 慢）
98	
99	**不能由 tile 大小解释**。NVFP4 W4A4 的 **activation quantize**（BF16 → FP4 + e4m3 scale）约 7.4 us 是 M=1 时**不可消除的架构级开销**：
100	
101	```
102	NVFP4 total = quantize(7.4us) + GEMM(40us) = 48us
103	即使 GEMM 降到 10us（理论最小）→ 17us ≈ 打平 Marlin
104	```
105	
106	| | Marlin | CUTLASS NVFP4 |
107	|---|---|---|
108	| 量化方案 | W4A16（激活不量化） | W4A4 |
109	| 核心指令 | BF16 MMA `m16n8k16` | FP4 block-scaled MMA `m16n8k64` |
110	| peak TFLOPS | ~400 | ~1467 |
111	| 小 M 瓶颈 | weight-bandwidth | quantize overhead + weight BW |
112	
113	**启示**：小 M 场景，NVFP4 小 tile kernel 最好情况只能打平 Marlin，不能显著超越。真想挤小 M 的话，应该写 **sm_120 原生 W4A16 kernel 替代 Marlin** —— 但 Marlin 实测已 82-97% L2 BW 饱和，无可挤空间。
114	
115	## 7. ROI 排序的优化方向
116	
117	### 7.1 flashinfer mm_fp4 离线 autotune（已落地 2026-04）
118	
119	利用 §4.1 的 6 tactic 池做**离线 tune → JSON cache → runtime load**，不在 server 启动时占 warmup 预算。
120	
121	**脚本**：`demo-sala/tune_mm_fp4_sm120.py`
122	
123	**策略（A+B 组合，消除噪声回归）**：
124	
125	- **A（profiling 加强）**：`AutoTuner.warmup=20, repeat=100`（10× flashinfer 默认 3/10）
126	- **B（per-config validate）**：对每个 (shape, M) 独立跑 baseline（tactic=-1）→ tune → bench tuned；仅当 `tuned < baseline × 0.97` 才合并进 cache，KEEP_MARGIN=3%。保证单调性——任何 cache 条目都是验证过的 ≥3% 增益，miss 走 fallback（等价 baseline）
127	
128	**覆盖 shape**（MiniCPM-SALA 所有 projection × 14 个 M bucket）：
129	
130	| 层 | N × K | M buckets |
131	|---|---|---|
132	| gate_up_proj | 32768 × 4096 | 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192 |
133	| down_proj | 4096 × 16384 | 同上 |
134	| qkv_proj | 4608 × 4096 | 同上 |
135	| o_proj | 4096 × 4096 | 同上 |
136	| lm_head | 73448 × 4096 | 同上 |
137	
138	**tune 结果**（`demo-sala/assets/mm_fp4_tune_sm120_report.json`）：
139	
140	| 层 | kept / total | 聚合 speedup（kept only） | 显著赢点 |
141	|---|---|---|---|
142	| gate_up_proj | 4 / 14 | 1.06× | 均匀弱收益 |
143	| **down_proj** | **13 / 14** | **1.27×** | **M=64 3.59×, M=128 3.55×, M=2 3.39×, M=4 3.27×** |
144	| qkv_proj | 8 / 14 | 1.07× | M=16 1.12×, M=1024 1.11× |
145	| o_proj | 11 / 14 | 1.06× | M=1024 1.12× |
146	| lm_head | 7 / 14 | 1.08× | M=8,16 各 1.11× |
147	| **总计** | **43 / 70** | — | — |
148	
149	**部署**（已生效）：
150	
151	- 产物：`demo-sala/assets/mm_fp4_tune_sm120.json`（62 entries 含 metadata）
152	- 加载点：`modelopt_quant.py` 模块导入时 `_load_fp4_autotune_cache()` 读 `SGLANG_FP4_TUNE_CACHE` 环境变量 → `AutoTuner.get().load_configs(path)`
153	- 非 tune 模式下 flashinfer `choose_one` 直接查 cache（不需要 `autotune(...)` context manager），miss → tactic=-1 fallback
154	- env 导出：`demo-sala/prepare_env.sh` Stage 5 + `eval/start_eagle.sh` 双路径同步
155	
156	**与 Marlin hybrid 的交互**：
157	down_proj 3× 级别的巨大增益集中在 M=2..256，但 `SGLANG_MARLIN_DECODE_THRESHOLD=48` 让 M≤48 走 Marlin，不过 CUTLASS。**真实吃到这批增益的场景**：EAGLE-3 verify 的 target forward（M≈256 @ bs=64 dtn=4）和 Smax 并发。小 M decode 仍走 Marlin。
158	
159	**为什么 autotune 会产生回归（已解决）**：tactic 0 和 fallback tactic=-1 是同一个 kernel，理论上 worst case 等于 baseline。第一版跑出的 qkv M=1,2 有 0.59-0.74× 回归——纯属 flashinfer 默认 `warmup=3, repeat=10` 的测量噪声，min selection 在方差带内误选次优 tactic。A+B 策略完全消除：43 个入库全部验证过，27 个被 KEEP_MARGIN 丢弃。
160	
161	### 7.2 NVFP4 tile × schedule × stages 手动编译扫描（独立方向，未展开）
162	
163	§7.1 是用 **flashinfer 已编译好的 6 个 tactic** 做选择；另一条独立路径是自己编译候选 kernel 扩展 tile 空间。
164	
165	- 5 个有效 tile（§5）× 2 schedule × 3-4 stages ≈ 30-40 候选
166	- 模板：`bench/autotune_fp4/autotune_kernel.cu`
167	- 目标：挤到 peak 50-70% = 750-1000 TFLOPS（1.3-1.8×）
168	- **状态**：未展开——§7.1 的 ROI 兑现（down_proj 3.5×）已满足短期收益需求；自编译需维护 sgl-kernel fork，维护成本高于收益
169	
170	### 7.3 Epilogue fusion（非 kernel 内部）
171	
172	- SwiGLU 融入 gate+up GEMM epilogue：省 32-128 MB 中间 activation write+read
173	- RoPE 融入 QKV GEMM epilogue
174	- 和 autotune 互补，可并行做
175	
176	### 7.4 b12x backend（全面实测 + 集成 + 生产 smoke test 通过 2026-04-22）
177	
178	**集成状态 2026-04-22**：代码开发完成，正确性验证通过（smoke test 正确答题，26 个 b12x kernel JIT 编译成功）。**当前提交包未启用**：`SGLANG_ENABLE_B12X` 默认为 0（`prepare_env.sh` 和 `start_eagle.sh` 均设 `:-0`），回滚原因是 EAGLE draft CUDA graph capture 路径不兼容 b12x。target model 走 b12x 收益已验证，draft model 始终需走纯 Marlin。
179	
180	**EAGLE draft 不兼容说明**：draft model CUDA graph capture 路径与 b12x dispatch 不兼容，draft 需保持纯 Marlin（`_detect_draft_model_quantization()` 设 threshold=9999）。若后续启用 b12x，target 路径可获 decode GEMM ~32.4% 收益，draft 路径不受影响。
181	
182	**初版集成 bug 与根因定位**（值得记录以防再踩）：
183	
184	第一版集成把 b12x 喂了 "pre-permute `padded_scales`"（即 `layer.weight_scale_interleaved` 做 TMA swizzle 之前的原始 padded 形式），基于假设"b12x 要 unswizzled 格式"。smoke test 模型答非所问（`1+1=?` 答成推理任务）——语言结构保留但分布偏移，典型权重轻微错乱症状。
185	
186	用 `bench/b12x/diag_layout_mismatch.py` 做 6 种（backend, x 格式, w scale 格式）交叉对照后定位：
187	
188	| 测试 | backend | x sf | w sf | vs 生产 CUTLASS 参考 |
189	|---|---|---|---|---|
190	| 1 | cutlass | nvfp4（bench） | **pre-permute** | cos **0.85** |
191	| 2 | cutlass | fp4（生产） | pre-permute | cos 0.85 |
192	| 3 | cutlass | fp4（生产） | **interleaved** | **参考** |
193	| 4 | b12x | nvfp4 | pre-permute（初版集成） | cos 0.85 |
194	| 5 | b12x | fp4 | pre-permute | cos 0.85 |
195	| **6** | **b12x** | **fp4** | **interleaved** | **cos 1.0 bit-identical** ✓ |
196	
197	**结论**：b12x kernel 和 mm_fp4(cutlass) 需要 **完全相同的 interleaved（TMA-swizzled）weight scale 布局**。bench `test_correctness.py` 里 `nvfp4_quantize(layout_128x4, do_shuffle=False)` 输出其实**就是 interleaved 格式**（不是我以为的"unswizzled"）；`do_shuffle=True` 才额外加一次 TMA 通道重排。生产 `layer.weight_scale_interleaved`（经过 `process_weights_after_loading` 的 permute）字节上等价于 `nvfp4_quantize(do_shuffle=False)`。
198	
199	**修复**：直接复用 `layer.weight_scale_interleaved`，删掉 `weight_scale_b12x` 占位变量，activation 用 `fp4_quantize`（production-style swizzled）而非 `nvfp4_quantize`。两者在这个布局下 kernel 输出位级相同。
200	
201	**bench 数据**（`bench/b12x/bench_full_matrix.py` + `b12x_full_matrix.json`，5 shape × 10 M × 4 backend，42 分钟 wall clock）：
202	
203	| shape | M=16 Mar/b12x | M=48 Mar/b12x | M=96 C/b12x | M=256 C/b12x | 赢 b12x 的 M 区间 |
204	|---|---|---|---|---|---|
205	| std_o (4096×4096) | 12.3 / **10.3** | 30.8 / **10.2** | 45 / **12.3** | 39 / **15.1** | **M ≥ 16** |
206	| std_qkv (4608×4096) | 12.1 / **10.3** | 27.9 / **10.3** | 44.3 / **12.3** | 42.8 / **16.4** | **M ≥ 16** |
207	| down (4096×16384) | **20.6** / 37.9 | **49.2** / 39.1 | 151 / **38.9** | 158 / **77.1** | **M ≥ 48** |
208	| gate_up (4096×32768) | **31.2** / 47.1 | 77.2 / **38.8** | 77.6 / **67.6** | 146 / **131** | **M ≥ 24** |
209	| gla_qkv (4096×12288) | **14.4** / 20.5 | **37.1** / 14.4 | 43.9 / **28.7** | 76.8 / **49.1** | **M ≥ 24** |
210	
211	**早期 bench 误判修正**（历史记录，防再踩）：
212	
213	最初用 `bench/b12x/run_b12x_vs_all.py` 得"仅 std_o + down 能用"结论，两处错：
214	1. baseline 用 sgl-kernel `cutlass_scaled_fp4_mm`，**不是生产** `flashinfer.mm_fp4(backend="cutlass")` + autotune cache。生产 std_o 小 M 反而比 sgl-kernel 慢 15–20%。
215	2. b12x 只跑默认启发式 tile，**没走 PR #3051 的 8-tactic autotune 空间**（4 tile × 2 prefetch）。tuned b12x 在 M=256 比默认快 2.75×，down 整体快 2×。
216	
217	修正后 5 shape 全部有效（上表），最终用 `bench/b12x/bench_full_matrix.py`（4 backend × 5 shape × 10 M）取证。
218	
219	**b12x 最优 tile 分布**（非单一最优）：
220	
221	| M | std_o | std_qkv | down | gate_up | gla_qkv |
222	|---|---|---|---|---|---|
223	| 24 | 64×128/pf | 64×128 | 64×64/pf | 64×128/pf | 64×128/pf |
224	| 48 | **64×64** | 64×64/pf | 64×64/pf | 64×128 | 64×128/pf |
225	| 96 | **128×64** | 64×128/pf | 64×64/pf | 64×64/pf | 64×64 |
226	| 128 | 64×128/pf | **128×64** | 64×64 | 64×64 | 64×64 |
227	| 256 | 64×128/pf | 64×128 | 64×64/pf | 64×128/pf | 64×64 |
228	
229	**关键：autotune 不是奢侈品，是必须的**。heuristic `_select_default_sm120_mma_tiler` 在 M=256 错选 128×128 导致 2.75× 速度损失；M=48 应选 64×64 但 heuristic 选 64×128；prefetch=True 是 heuristic 完全不考虑的维度。
230	
231	**正确性验证**（`bench/b12x/test_correctness.py` + `b12x_correctness.json`）：
232	- 23 配置 × 3 seed = **69 / 69 PASS**
233	- **cos_sim = 1.000000, max_abs = 0.000000**（bit-identical 不是舍入级一致，是位级一致）
234	- 原因：b12x 和 CUTLASS 都发同一条 `mma.sync.aligned.kind::mxf4nvf4.block_scale` 指令，f32 accumulator 顺序在这些 shape 上恰好等价
235	- **混用零精度代价**——模型层间 b12x/CUTLASS 切换无一致性问题
236	
237	**生产 M 直方图取证**（2026-04，`SGLANG_PROFILE_DISPATCH=1` EAGLE-3 workload，54000 次 GEMM 13.2s wall）：
238	
239	decode GEMM 时间分布（排除 M=8192 prefill）：
240	
241	| shape | decode GEMM ms | M=[24,256] 占比 | b12x 节省 | 节省 % |
242	|---|---|---|---|---|
243	| std_o | 395 | 68.5% | 195 | **49%** |
244	| std_qkv | 48 | 71.4% | 23 | 47% |
245	| down | 517 | 72.4% | 194 | **38%** |
246	| gate_up | 589 | 59.4% | 99 | 17% |
247	| gla_qkv | 202 | 63.1% | 57 | 28% |
248	| **合计** | **1750** | 66% | **567** | **32.4%** |
249	
250	**E2e 估算**：
251	- decode GEMM kernel 时间省 **32.4%**（1750 → 1183 ms/13.2s）
252	- wall clock 上限 4.3%（若 GEMM 完全在 critical path）
253	- 实际 decode 并发 ~1.3× → 真实 e2e 吞吐增益 **~3%**
254	- Prefill（M=8192）**0 收益** —— b12x 大 M 回到 128×128 = CUTLASS 同路径
255	
256	**最终 dispatch 规则（2-tier + CUTLASS override，2026-04-23）**：
257	
258	```python
259	MARLIN_UPPER = {
260	    (N=4096,  K=4096):   8,    # std_o
261	    (N=4608,  K=4096):   8,    # std_qkv
262	    (N=4096,  K=16384):  24,   # down (K 大 Marlin 带宽仍赢到 M=24)
263	    (N=32768, K=4096):   16,   # gate_up
264	    (N=12288, K=4096):   16,   # gla_qkv
265	    (N=4096,  K=12288):  16,   # eagle_fc (crossover M=24, conservative=16)
266	}
267	CUTLASS_OVERRIDE = {
268	    (4096,  16384, 512),   # down M=512:     b12x 0.91× CUTLASS
269	    (32768, 4096,  8192),  # gate_up M=8192: b12x 1.00× CUTLASS
270	    (4608,  4096,  8192),  # std_qkv M=8192: b12x 0.97× CUTLASS
271	}
272	# M ≤ MARLIN_UPPER         → Marlin (W4A16)
273	# (N,K,M_bucket) in OVERRIDE → tuned CUTLASS (W4A4)
274	# otherwise                 → b12x (W4A4, block-scaled MMA)
275	```
276	
277	2-tier 规则覆盖 6 个形状 × 全 M 范围（58 个 BEST_TILE 条目），不再使用 `B12X_UPPER` 上限。高并发时 b12x 接管 62% dispatch，override 18%（主要是 down M=512），CUTLASS prefill 19%。`SGLANG_MARLIN_DECODE_THRESHOLD` 不再需要——b12x 路径内置 per-shape Marlin 阈值并自动准备 Marlin 权重。
278	
279	### 7.5 b12x 环境要求与集成步骤
280	
281	```
282	nvidia-cutlass-dsl                 == 4.5.0.dev0
283	nvidia-cutlass-dsl-libs-base       == 4.5.0.dev0
284	nvidia-cutlass-dsl-libs-cu13       == 4.5.0.dev0   (关键！uv pip 单升 base 会漏)
285	flashinfer-python                  >= 0.6.8.post1
286	torch                              == 2.11.0+cu130
287	CUDA toolkit                       == 13.2
288	export CUTE_DSL_ARCH=sm_120a       (不带 'a' 会 ptxas 拒收 block-scaled MMA)
289	```
290	
291	**b12x 踩过的坑**（记录以防重犯）：
292	
293	1. **cutlass-dsl 4.4.2 → 4.5.0.dev0 的 NVVM lowering**：4.4.2 生成 `_mma.block_scale...` 带下划线前缀（占位符），ptxas 报 `Unexpected instruction types`。4.5.0.dev0 才发 `mma.sync.aligned...kind::mxf4nvf4.block_scale`。必须三包同步升。
294	2. **CUTE_DSL_ARCH 默认不是 sm_120a**：默认回退 `sm_120`（无 arch suffix），block-scaled MMA 需要 `sm_120a`。
295	3. **PR demo 函数 `dense_gemm()` M=1 触发 `cudaErrorIllegalInstruction`**：不用 demo，直接走生产路径 `_compile_block_scaled_gemm` + `gemm.wrapper`（参考 `flashinfer/gemm/gemm_base.py` `_b12x_gemm_fp4_runner`）。
296	4. **Monkey-patch flashinfer.cute_dsl.utils**：我们没升 flashinfer 本体，只从 PR 拉 kernel 文件，运行时注入 `sm120_make_smem_layout_sfa/sfb`。
297	
298	**集成路径**：
299	
300	1. **kernel 文件**：从 `bench/b12x/` 复制到 `demo-sala/sglang/python/sglang/srt/layers/quantization/b12x/`（`dense_blockscaled_gemm_sm120.py` + `cute_dsl_utils.py` + `__init__.py`）
301	2. **glue 模块**：`demo-sala/sglang/python/sglang/srt/layers/quantization/b12x_fp4.py`——懒加载、monkey-patch flashinfer.cute_dsl.utils、编译+缓存、`b12x_gemm_fp4(x, w, x_sf, w_sf, alpha, tile, prefetch)` API
302	3. **modelopt_quant.py dispatch**：`NvFp4LinearMethod.apply()` 加第三路
303	4. **prepare_env.sh**：`CUTE_DSL_ARCH=sm_120a`（必须带 `a`）+ 3 包 cutlass-dsl 4.5.0.dev0（环境已具备，验证 BOS 清单）+ `CUTE_DSL_CACHE_DIR=/tmp/cute_dsl_cache`
304	5. **warmup**：`--skip-server-warmup` 前按 bench 最优 tile 表预编译 5 shape × 6 M_bucket = 30 个 kernel 变体（首次 ~5–10 分钟，后续复用 `CUTE_DSL_CACHE_DIR`）
305	6. **autotune**：不需要再跑 flashinfer autotune（同 shape 区间已被 b12x 接管）；现有 `mm_fp4_tune_sm120.json` 保留用于 M > 256 的 CUTLASS 路径
306	
307	## 8. 已终结方向（不值得做）
308	
309	| 方向 | 原因 |
310	|---|---|
311	| 手写 pure NVFP4 GEMM kernel | CUTLASS 已用足 TMA + WS + Cooperative + persistent + sm_120 原生 MMA |
312	| Cluster > 1 | sm_120 无 multicast |
313	| 大 K tile (>128) 搭大 M/N tile | smem 不够 2 stage |
314	| 小 tile (<128) | TMA atom 约束 |
315	| flashinfer `trtllm` backend | sm_120 不支持（`cute-dsl` 从 PR #3051 拉 b12x kernel 后可用，见 §7.4） |
316	| sm_120-native W4A16 重写 Marlin | Marlin decode M=1/8 已达 82-97% L2 BW（gate/up/down），无可挤空间 |
317	| Marlin bandwidth 测量作为 blocker | 已测，实证 L2 饱和，终结 |
318	
319	## 9. 关键脚本与数据位置
320	
321	| 文件 | 用途 |
322	|---|---|
323	| `bench/pure_mma_peak/pure_mma.cu` + `run.py` | pure-MMA peak 测量 |
324	| `bench/bench_fp4_all_backends.py` | 全家桶 library 对比 |
325	| `bench/probe_fp4_peak.py` | CUTLASS 跨 shape 实测收敛 |
326	| `bench/bench_cublas_vs_cutlass_nvfp4.py` | cuBLAS vs CUTLASS 对照 |
327	| `bench/autotune_fp4/autotune_kernel.cu` | tile 参数化模板 |
328	| `bench/autotune_fp4/build.sh` | 候选 config 编译 |
329	| `bench/bench_marlin_bandwidth.py` | Marlin 带宽测量 |
330	| `bench/b12x/` | PR #3051 backend 完整调研 + kernel 文件（`dense_blockscaled_gemm_sm120.py` + `cute_dsl_utils.py`） |
331	| `bench/b12x/bench_full_matrix.py` | **最终 4-way bench**：tuned-flashinfer-CUTLASS / sgl-kernel-CUTLASS / b12x 8-tactic / Marlin，5 shape × 10 M |
332	| `bench/b12x/b12x_full_matrix.json` | 上述 bench 完整结果（2026-04-22 跑，42 分钟 wall） |
333	| `bench/b12x/test_correctness.py` | b12x vs CUTLASS 位级等价测试（cos_sim / max_abs / max_rel） |
334	| `bench/b12x/b12x_correctness.json` | 69/69 PASS 记录 |
335	| `bench/b12x/run_b12x_vs_all.py` | 早期 bench（**baseline 不公平，保留作历史**；权威数据用 `bench_full_matrix.json`） |
336	| `bench/b12x_vs_all.json` | 早期 bench 结果（同上，保留） |
337	| `bench/b12x_extra_shapes.json` | 早期扩展 shape 实验（结论被 `bench_full_matrix.json` 推翻） |
338	| `demo-sala/tune_mm_fp4_sm120.py` | §7.1 离线 autotune 脚本（A+B 策略） |
339	| `demo-sala/bench_downproj_marlin_vs_cutlass.py` | down_proj Marlin vs CUTLASS(tuned) A/B，验证 threshold=48 |
340	| `demo-sala/assets/mm_fp4_tune_sm120.json` | autotune cache（运行时资产） |
341	| `demo-sala/assets/mm_fp4_tune_sm120_report.json` | autotune per-entry decision log |
342
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/marlin-tuning.md"
}
```

> TOOL

tool_result Read
```
1	# Marlin / b12x 调优记录
2	
3	> 更新时间：2026-04-27
4	> 范围：MiniCPM-SALA no-spec 路径下的 NVFP4 Marlin、b12x/CUTLASS 分流、CUDA graph 内 profiling。
5	> 最高口径：涉及 decode 性能时，以 CUDA graph replay 内 kernel 时间为准；Python `apply()` 计数只能作为辅助定位。
6	
7	## 当前部署状态速览
8	
9	| 组件 | 状态 | 说明 |
10	|---|---|---|
11	| b12x 2-tier dispatch | ⚠️ 开发完成，**未启用** | `SGLANG_ENABLE_B12X=0`（默认关闭）；draft CUDA graph capture 不兼容，回滚 |
12	| sgl-kernel FP4 scale bug fix | ✅ 已部署 | `common_ops.abi3.so` pre-built 替换，scale `/2` bug（cos_sim 0.77→1.0）修复 |
13	| Marlin atomic / shape-aware tile | ✅ 已集成 | `.so` 内已包含；全局阈值 `SGLANG_MARLIN_DECODE_THRESHOLD=48` 生效 |
14	| 当前生产 dispatch | ✅ M≤48 Marlin，M>48 CUTLASS | b12x 未启用；threshold=48 全局切换 |
15	| native FP4 MMA / QuTLASS | ❌ 无法使用 | sm_120 限制（见下文负结果） |
16	
17	
18	## 1. Baseline 定义
19	
20	这里必须区分三种 baseline，不能混着说。
21	
22	| 名称 | 含义 | 当前状态 |
23	|---|---|---|
24	| B0: old Marlin baseline | 未做 atomic/shape-aware/tile 调优的老 Marlin `.so` | 还没有完成本轮公平 e2e / CUDA graph 对比 |
25	| B1: current Marlin + b12x baseline dispatch | 当前已部署 Marlin `.so`，但 `SGLANG_B12X_DISPATCH_PROFILE=baseline` 使用旧 b12x 阈值 | 已测 |
26	| B2: current Marlin + b12x tuned dispatch | 当前已部署 Marlin `.so`，`SGLANG_B12X_DISPATCH_PROFILE=tuned` 使用新 b12x/shape-aware 分流 | 已测 |
27	| B3: Marlin M=1 graph-tile candidate | 新发现的 M=1 exact-shape Marlin tile 表 | 已测，e2e 回退，默认禁用 |
28	
29	当前部署产物：
30	
31	```text
32	32d27c728ea93203236757d7534b6e68  /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/sgl_kernel/sm100/common_ops.abi3.so
33	32d27c728ea93203236757d7534b6e68  /user_4813494d/openbmb/demo-sala/common_ops.abi3.so
34	```
35	
36	注意：
37	
38	- 之前我口头说的 fresh baseline 是 B1，不是 B0。
39	- `.cu12bak` 当前 md5 是 `5b768fb3708ed2c15ffe5601db3b5f45`，它是部署过程备份，不等价于 old Marlin baseline。
40	- 78MB 的 `common_ops.abi3.so.bak` 涉及旧 cu12/旧打包，不适合直接当公平性能 baseline；若要测 B0，应从明确的 old Marlin 源码/patch 点重新 build 一个 cu13 `.so`。
41	
42	备份源码位置：
43	
44	```text
45	/user_4813494d/backups/cu12-baseline-20260420/packages/sglang-minicpm/sgl-kernel/csrc/gemm/marlin/gptq_marlin.cu
46	```
47	
48	这里的 old Marlin C++ 仍有：
49	
50	```cpp
51	bool part_use_atomic_add = use_atomic_add && div_ceil(prob_m_split, 64) * prob_n <= 2048;
52	```
53	
54	因此对 `N=4096/4608/12288/32768` 的 decode 基本禁用 atomic。当前 Marlin 的关键改动之一是把小 M decode 纳入 atomic 路径。
55	
56	## 2. 已测 e2e 结论
57	
58	约束：no-spec，只测允许的 `3*S1 8*S8 0*Smax`。
59	
60	| 对比项 | S1 | S8 | Smax |
61	|---|---:|---:|---:|
62	| B0 old Marlin cu13 `.so` + b12x tuned dispatch | `275.70s` | `293.04s` | `0.00s` |
63	| B1 current Marlin + b12x baseline dispatch | `266.44s` | `284.57s` | `0.00s` |
64	| B2 current Marlin + b12x tuned dispatch | `266.57s` | `284.37s` | `0.00s` |
65	
66	结论：
67	
68	- B1 和 B2 基本持平。
69	- 这个结果只能说明 b12x/shape-aware 分流没有兑现 e2e 提升。
70	- 它不能回答“old Marlin vs tuned Marlin 有没有提升”，因为 B1/B2 用的是同一个已部署 Marlin `.so`。
71	- B0 和 B2 的公平 no-spec e2e 对比显示：当前 Marlin 比 old Marlin 快，S1 少 `9.13s`，S8 少 `8.67s`，约 `3.0%~3.3%` duration 改善。
72	
73	B0 old Marlin 产物：
74	
75	```text
76	77a3a9fb3aad222714a43ede4776596d  /user_4813494d/openbmb/outputs/marlin_b0_20260425_101153/common_ops.old_marlin_cu13.abi3.so
77	```
78	
79	对应 B0 e2e 日志：
80	
81	```text
82	/user_4813494d/openbmb/outputs/marlin_b0_20260425_101153/b0old_mini_bench_3s1_8s8_0smax_manual_*.log
83	```
84	
85	## 3. CUDA Graph Profiling 结论
86	
87	方法：使用 SGLang profiler 捕获 `EXTEND` / `DECODE` trace，解析 kernel event，不依赖 Python 层 `apply()` 计数。
88	
89	Decode trace 结果：
90	
91	| 项 | B1 baseline dispatch | B2 tuned dispatch |
92	|---|---:|---:|
93	| DECODE total GPU kernel time | `299.306 ms` | `299.425 ms` |
94	| Marlin time | `167.053 ms` | `167.112 ms` |
95	| Marlin 占比 | `55.81%` | `55.81%` |
96	| Marlin calls | `5120` | `5120` |
97	
98	Extend trace 结果：
99	
100	| 项 | B1 baseline dispatch | B2 tuned dispatch |
101	|---|---:|---:|
102	| EXTEND total GPU kernel time | `1628.944 ms` | `1609.674 ms` |
103	| b12x/CuteDSL time | `769.847 ms` | `750.131 ms` |
104	
105	诊断：
106	
107	- tuned dispatch 在 prefill/extend 有小幅收益，约 `19.7 ms` kernel time。
108	- no-spec S1/S8 的 e2e 主体是长 decode；decode graph 内 Marlin 时间完全没变。
109	- 因此 B2 不快的直接原因是：优化发生在 prefill/dispatch，主耗时路径 decode graph Marlin 没有变化。
110	
111	B3 e2e 结果（已在 §2 汇总）：B3 直接回退，不能进入默认路径。当前已把部署 `.so` 回滚到 `32d27c728ea93203236757d7534b6e68`。源码中的 exact tile 表保留为实验项，但默认由 `SGLANG_MARLIN_M1_EXACT_TILE=0` 禁用。
112	
113	## 4. Old-Emulated Marlin 对比
114	
115	初步以 old-emulated CUDA graph microbench（强制旧 tile `{K=128,N=128,T=256,B=1}` + 关闭 atomic）先验证方向：old Marlin -> current Marlin 在 microbench 上有提升，主要来自小 M atomic。B1 -> B2 没提升，是因为 b12x tuned 没改变 decode Marlin replay。此结果由 §4.1 真正 B0 e2e 所取代。
116	
117	## 4.1 B0 old `.so` 与 Current Marlin 归因
118	
119	在 `2026-04-25` 已补做真正 B0 old-Marlin cu13 `.so`：
120	
121	```text
122	77a3a9fb3aad222714a43ede4776596d  /user_4813494d/openbmb/outputs/marlin_b0_20260425_101153/common_ops.old_marlin_cu13.abi3.so
123	```
124	
125	同机、同参数 CUDA graph microbench：
126	
127	| shape | M | B0 old `.so` | current | current no-small-atomic | old-tile + atomic | old-tile barrier |
128	|---|---:|---:|---:|---:|---:|---:|
129	| `std_o` | 1 | `10.250 us` | `8.199 us` | `10.246 us` | `8.180 us` | `10.258 us` |
130	| `std_o` | 8 | `10.244 us` | `8.194 us` | `10.250 us` | `8.183 us` | `10.249 us` |
131	| `std_qkv` | 1 | `10.242 us` | `6.298 us` | `10.244 us` | `6.314 us` | `10.241 us` |
132	| `std_qkv` | 8 | `10.240 us` | `8.182 us` | `10.251 us` | `8.181 us` | `10.232 us` |
133	| `gla_qkv` | 1 | `12.293 us` | `12.252 us` | `12.336 us` | `12.293 us` | `12.305 us` |
134	| `gla_qkv` | 8 | `12.291 us` | `12.301 us` | `14.334 us` | `12.300 us` | `12.299 us` |
135	| `gate_up` | 1 | `25.114 us` | `22.520 us` | `22.520 us` | `24.624 us` | `25.797 us` |
136	| `gate_up` | 8 | `26.622 us` | `22.560 us` | `22.587 us` | `25.917 us` | `26.617 us` |
137	| `down` | 1 | `18.428 us` | `14.323 us` | `20.603 us` | `14.441 us` | `18.434 us` |
138	| `down` | 8 | `18.435 us` | `14.353 us` | `22.274 us` | `16.374 us` | `18.449 us` |
139	
140	归因结论：
141	
142	- `std_o` / `std_qkv`：收益几乎全部来自 small-M atomic；关闭 `SGLANG_MARLIN_ATOMIC_SMALL_M` 后退回 old `.so` 水平。
143	- `down`：收益主要来自 small-M atomic，同时 tile 也有少量贡献；关闭 small-M atomic 后甚至比 old `.so` 更慢。
144	- `gate_up`：收益主要来自 shape-aware tile；关闭 small-M atomic 基本不影响，强制 old tile 会明显变慢。
145	- `gla_qkv`：当前 Marlin 对它基本没收益，且 no-small-atomic 在 M=8 上有回退风险；后续不要优先动。
146	
147	这解释了为什么 B0 -> current 有约 `3%` e2e 收益：std/down/qkv 的 atomic 和 gate_up 的 tile 共同贡献；而 B1 -> B2 不动，是因为 b12x 分流没有改变这些 decode graph Marlin replay 内核。
148	
149	## 5. b12x / Shape-Aware 做了什么
150	
151	`demo-sala/sglang/python/sglang/srt/layers/quantization/b12x_fp4.py` 当前新增了 dispatch profile：
152	
153	- `SGLANG_B12X_DISPATCH_PROFILE=baseline|tuned`
154	- baseline 复现旧阈值和旧 CUTLASS override。
155	- tuned 根据离线 b12x/CUTLASS/Marlin crossover 调整：
156	  - `std_o/std_qkv` Marlin 上界放到 `M<=32`
157	  - `down` 放到 `M<=24`
158	  - `gate_up` 保持 `M<=16`
159	  - `gla_qkv` 放到 `M<=24`
160	  - 部分大 M bucket 强制 CUTLASS，绕开 b12x 不占优的点
161	
162	同时加了 b12x 预编译缓存：
163	
164	- `SGLANG_B12X_PRECOMPILE=1`
165	- `SGLANG_B12X_PRECOMPILE_PROFILE=nospec-mini`
166	- `CUTE_DSL_CACHE_DIR=/user_4813494d/openbmb/bench/b12x/cache/cute_dsl`
167	
168	这解决的是 capture/build 抖动，不是 decode replay 热点。
169	
170	为什么没有提升：
171	
172	- no-spec decode 的有效 M 是 `1` 或 `8`。
173	- 这些 M 档位在 baseline/tuned dispatch 下都仍然走 Marlin。
174	- Python 分流只在 prefill 和 CUDA graph capture 时执行；graph replay 阶段不重新走 Python 分流。
175	- 因此 tuned dispatch 不会改变每个 decode token replay 的 Marlin kernel。
176	
177	## 6. 已排除方向
178	
179	### 6.1 Python route profiling 不能当最终依据
180	
181	`SGLANG_B12X_PROFILE` 只覆盖 `apply()` 执行阶段，decode graph replay 不走 Python，不能用它解释最终 decode 吞吐。
182	
183	### 6.2 `use_fp32_reduce=False` 没有 replay 收益
184	
185	生产 shape 上 `fp32_reduce=True/False` 的 CUDA graph replay 时间全部在约 `0.1%` 内，不能作为优化方向。decode 小 M 已走 atomic 路径，基本不触发 barrier global reduce，关 fp32 reduce 只影响极少量路径。
186	
187	## 7. 新发现：M=1 Marlin Tile 才是当前抓手
188	
189	按用户要求，重新以 CUDA graph replay 计时做 tile sweep，结果：
190	
191	| shape | M | 当前 auto | best | speedup |
192	|---|---:|---:|---:|---:|
193	| `std_o` | 1 | `8.184 us` | `k128_n256_t256_b1 = 6.265 us` | `1.306x` |
194	| `std_qkv` | 1 | `6.375 us` | `k064_n128_t128_b2 = 6.148 us` | `1.037x` |
195	| `gla_qkv` | 1 | `11.783 us` | `k064_n128_t128_b2 = 11.402 us` | `1.033x` |
196	| `gate_up` | 1 | `22.512 us` | auto | `1.000x` |
197	| `down` | 1 | `14.335 us` | `k064_n256_t256_b2 = 14.329 us` | `1.000x` |
198	| `std_o` | 8 | `8.195 us` | `k128_n128_t256_b1 = 8.187 us` | `1.001x` |
199	| `std_qkv` | 8 | `8.186 us` | `k128_n128_t256_b1 = 8.183 us` | `1.000x` |
200	| `gla_qkv` | 8 | `12.290 us` | `k128_n128_t256_b1 = 12.289 us` | `1.000x` |
201	
202	结论：
203	- S8 的 M=8 decode 基本没有 tile 空间。
204	- S1 的 M=1 decode 有真实空间，尤其 `std_o`。
205	- 下一步应该只动 M=1 exact-shape Marlin tile 表，避免影响 M=8。
206	
207	## 10. M=1 Exact Tile Per-Shape Gate
208	
209	B3 失败的直接教训是：不能用一个总开关同时打开 `std_o/std_qkv/gla_qkv` 的 M=1 exact tile。当前已把外部 sgl-kernel 源码改成 per-shape gate，默认仍关闭：
210	
211	```text
212	SGLANG_MARLIN_M1_EXACT_TILE=0
213	SGLANG_MARLIN_M1_STD_O_TILE=0
214	SGLANG_MARLIN_M1_STD_QKV_TILE=0
215	SGLANG_MARLIN_M1_GLA_QKV_TILE=0
216	```
217	
218	candidate `.so` 已备份并恢复为 stable `.so`。离线 microbench 结果：`std_o M=1` 节省约 `0.64 us/call`（按层加权约 `1.81%` M=1 Marlin 本地收益）；`std_qkv M=1` 节省约 `0.09 us/call`（层数少，权重低）；`gla_qkv M=1` 轻微回退。
219	
220	结论：
221	
222	- `std_o M=1` 是唯一还有意义的 exact-tile 候选，但收益只占 M=1 Marlin 本地约 `1.8%`。
223	- `std_qkv M=1` 层数只有 8，权重太小，单独默认打开价值很低。
224	- `gla_qkv M=1` 不再默认研究；B3 已显示它有回退风险。
225	- 在没有服务级 e2e 证据前，per-shape gate 只能保留为实验项，不能默认启用。
226	
227	## 11. Decode Kernel Hotspot After Marlin
228	
229	基于 B2 tuned S8short DECODE trace，只统计 GPU kernel event：
230	
231	| class | calls | GPU time | pct |
232	|---|---:|---:|---:|
233	| Marlin | `5120` | `167.112 ms` | `56.17%` |
234	| elementwise misc | `13752` | `24.617 ms` | `8.28%` |
235	| BF16 CUTLASS GEMM | `288` | `20.831 ms` | `7.00%` |
236	| index_put | `1333` | `16.007 ms` | `5.38%` |
237	| vectorized_gather | `768` | `13.623 ms` | `4.58%` |
238	| RMSNorm | `4384` | `9.833 ms` | `3.31%` |
239	| compress_k | `512` | `9.003 ms` | `3.03%` |
240	| topk/sort | `768` | `8.452 ms` | `2.84%` |
241	| fused recurrent GLA | `768` | `7.429 ms` | `2.50%` |
242	| attention split/paged-kv | `512` | `12.159 ms` | `4.09%` |
243	
244	宏观判断：
245	
246	- Marlin 仍是最大项，但 B0 -> current 已经拿到约 `3%` e2e；继续 exact tile 的理论收益已经很小。
247	- M=1 exact tile 的 `std_o+std_qkv` 候选只省约 `38 us/decode step`，约 `1.9%` M=1 Marlin 本地收益，折到 e2e 很可能低于 `1%`。
248	- 后续更值得看的 kernel 侧方向：
249	  - BF16 CUTLASS GEMM：大概率是 lm_head/logits 类路径，单项约 `7%` decode GPU time，但涉及精度/答案风险。
250	  - KV/cache gather + index_put：合计接近 `10%` decode GPU time，可能来自 cache/table 更新和稀疏路径元数据搬运，优化潜力比继续 Marlin tile 更高。
251	  - elementwise misc：调用多但单 kernel 小，适合找可融合链路，不适合盲写大 kernel。
252	
253	当前不做 e2e 时，下一步只能做 kernel-side/read-only 归因：定位 BF16 CUTLASS GEMM、gather/index_put 分别来自哪段 Python/CUDA graph 捕获路径，再决定是否写替换 kernel。
254	
255	## 12. compress_k Head-Parallel Rewrite
256	
257	源码归因：`compress_k` 热点来自 `minicpm_sparse_kernels.py`；原 kernel 启动 grid `(batch, chunk, head)`，但每个 head program 存在控制流冗余（history 路径只有 `head_idx==0` 处理所有 head；new chunk 路径同理）。修改后每个 `head_idx` program 只负责自己的 head，同步改了 padded / non-padded 两路，主路径是 non-padded（`split_stage1=false`）。
258	
259	CUDA graph microbench 与 PyTorch reference correctness 已验证，padded correctness smoke：`bs=1/8, k1/k2, history=64, new=1: out_diff=0.0, key_diff=0.0`。
260	
261	| case | k | old graph | new graph | speedup | correctness |
262	|---|---|---:|---:|---:|---|
263	| bs=1, history=512, new=1 | k1 32/16 | `8.228 us` | `4.129 us` | `1.99x` | 0 diff |
264	| bs=1, history=512, new=1 | k2 128/64 | `59.420 us` | `32.809 us` | `1.81x` | 0 diff |
265	| bs=8, history=512, new=1 all rows | k2 128/64 | `58.152 us` | `38.405 us` | `1.51x` | 0 diff |
266	
267	解释：history-only 路径基本不变；new chunk 有边界时收益明显（k2 约 1.5×~1.8×），因为旧实现对 `kernel_size=128` 做了冗余 mean pooling。new compressed chunk 不是每步都有（k1 约每 16 token 一次，k2 约每 64 token 一次），这项优化是”去掉尖峰成本”而非稳定节省；折到 e2e 的预期收益小于 Marlin B0→current 的 `3%`，但比继续压 M=1 Marlin tile 更确定。
268	
269	## 13. SimpleGLA Direct-State Decode
270	
271	继续沿着 decode GPU hotspot 看，`vectorized_gather` + `fused_recurrent_fwd_kernel` + `index_put` 的序列基本定位到 SimpleGLA recurrent state：
272	
273	```python
274	initial_state = layer_cache.temporal[mamba_indices, :].contiguous()
275	o, final_state = fused_recurrent_simple_gla(..., initial_state=initial_state)
276	layer_cache.temporal[mamba_indices, :] = final_state
277	```
278	
279	对应代码在 `demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py` 的 SimpleGLA decode 分支。当前模型有 24 个 `lightning-attn` 层：
280	
281	```text
282	lightning-attn layers = [1,2,3,4,5,6,7,8,10,11,12,13,14,15,18,19,20,21,23,24,25,26,27,28]
283	```
284	
285	修改：
286	
287	- 扩展 `demo-sala/sglang/python/sglang/srt/layers/attention/simple_gla_decode_kernel.py`，新增 `simple_gla_decode_update_fwd()`。
288	- 新 kernel 直接从 `temporal[state_indices]` 读 recurrent state，在 kernel 内写回更新后的 state。
289	- 同时使用 `BK=BV=128` 的 decode tile，避免 FLA 默认 `64x64` 切成 4 个 tile 后再做 `sum(0)`。
290	- 接入 no-spec decode 路径；`target_verify` / spec 路径不动。
291	- 保留关闭开关：`SGLANG_SIMPLE_GLA_DIRECT_DECODE=0`。
292	
293	CUDA graph replay 结果：
294	
295	| batch | old generic path | direct-state path | speedup | output diff | state diff |
296	|---:|---:|---:|---:|---:|---:|
297	| 1 | `14.380 us` | `6.164 us` | `2.33x` | `5.96e-08` | `0.0` |
298	| 8 | `34.860 us` | `14.366 us` | `2.43x` | `0.00390625` | `0.0` |
299	
300	解释：
301	
302	- `state diff = 0` 说明 recurrent state 更新与旧路径一致。
303	- bs=8 的 output diff 是 bf16 量级，来自 `K=128` 单 tile 与旧 `64x64` 分块后求和的累加顺序差异。
304	- 这个优化直接覆盖 trace 中的 `vectorized_gather`、`fused_recurrent_fwd_kernel`、`index_put` 三段组合，而不是只改其中一个 PyTorch indexing kernel。
305	- 这是目前比继续 Marlin M=1 tile 更高杠杆的 no-spec decode kernel 侧优化。
306	
307	状态：已做 `py_compile`、CUDA graph correctness/timing、用户手跑 no-spec e2e。
308	
309	## 14. Non-Spec E2E Result After Kernel-Side Fixes
310	
311	用户在 `2026-04-25` 手动跑了 `3*S1 8*S8 0*Smax` no-spec e2e（S1: `248.53s`，S8: `265.63s`）。
312	
313	对比本轮修改前的 tuned no-spec：
314	
315	| case | before tuned | after kernel-side | duration delta | speedup |
316	|---|---:|---:|---:|---:|
317	| S1 | `266.57s` | `248.53s` | `-18.04s / -6.77%` | `1.073x` |
318	| S8 | `284.37s` | `265.63s` | `-18.74s / -6.59%` | `1.071x` |
319	
320	对比真正 old Marlin baseline：
321	
322	| case | B0 old Marlin | after kernel-side | duration delta |
323	|---|---:|---:|---:|
324	| S1 | `275.70s` | `248.53s` | `-27.17s / -9.85%` |
325	| S8 | `293.04s` | `265.63s` | `-27.41s / -9.35%` |
326	
327	结论：
328	
329	- 当前收益不是 b12x/shape-aware dispatch 贡献的；那条此前已经证明基本持平。
330	- old Marlin -> current Marlin 约 `3%`。
331	- 本轮非 Marlin kernel-side 修改又给 no-spec e2e 带来约 `6.6%~6.8%` duration 改善（§15 已用 DECODE trace 确认来源）。
332	
333	## 15. Short DECODE Trace Confirmation
334	
335	本节只使用短 DECODE trace（CUDA graph 内 kernel 时间），不做全量 e2e。两份 trace 序列分布不一致（old tuned: ~32 steps，new direct-state: ~16 steps），采用 Marlin 调用数做 per-step 归一化。
336	
337	核心 per-step 对比：
338	
339	| class | old tuned | new direct-state | interpretation |
340	|---|---:|---:|---|
341	| Marlin | `5.2222 ms/step` | `4.8839 ms/step` | Marlin 仍是 decode graph 最大项 |
342	| `vectorized_gather` | `0.4257 ms/step` | gone from top classes | 被 direct-state 读 state 替掉 |
343	| generic `fused_recurrent_fwd_kernel` | `0.2322 ms/step` | gone | 被 SimpleGLA direct kernel 替掉 |
344	| `index_put` | `0.5002 ms/step` | `0.1066 ms/step` | recurrent state 写回大幅减少，仍有少量其他 index kernel |
345	| `_simple_gla_decode_update_kernel` | absent | `0.4672 ms/step` | 新 kernel，合并读 state、GLA recurrence、写 state |
346	| SimpleGLA state path subtotal | `1.1581 ms/step` | `0.5738 ms/step` | `-0.5843 ms/step`，约 `50%` local reduction |
347	| `compress_k_complete_kernel_new` | `0.2814 ms/step` | `0.3995 ms/step` | 这份短 trace 新 chunk 分布不同，不能从 e2e trace 证明 compress_k 收益 |
348	| attention split / paged-kv | `0.4042 ms/step` | `1.6976 ms/step` | 受序列长度 / split-kv 分布影响，不作为本轮优化归因 |
349	
350	结论：
351	
352	- 本轮 e2e 下降的主因已经在 CUDA graph trace 中确认：SimpleGLA no-spec decode 的 gather / generic recurrent / index_put 链路被替换，graph 内实测每 step 省约 `0.58 ms`。
353	- `compress_k` rewrite 的 microbench 是正收益，但短 trace 里没有形成稳定下降；原因是它只在 new compressed chunk 边界处省尖峰，是否反映到短 profile 取决于采样到的序列位置。
354	- 因此目前要把本轮收益归因到 SimpleGLA direct-state decode，而不是 b12x dispatch，也不是 Marlin tile 本身。
355	- 下一步如果继续 kernel 侧优化，应按 decode graph 排序继续打最大项：Marlin 仍是第一项，其次是 attention split / paged-kv 的长上下文分布问题；`compress_k` 只作为边界尖峰优化继续保留。
356	
357	## 16. Fixed-Input S8 Decode Trace
358	
359	采样分布：S8 sampled n=8，prompt_tokens avg=70136 min=613 max=135664，output_len=128，profile decode steps=16。
360	
361	CUDA graph 内 per-step 结果：
362	
363	| class | calls/step | ms/step |
364	|---|---:|---:|
365	| Marlin | `160.0` | `4.9032` |
366	| attention split/paged-kv | `24.0` | `1.7541` |
367	| SimpleGLA direct | `24.0` | `0.4748` |
368	| BF16/CUTLASS GEMM | `1.0` | `0.4588` |
369	| compress_k | `16.0` | `0.4037` |
370	| elementwise/reduce misc | `182.0` | `0.3674` |
371	| RMSNorm | `137.0` | `0.3025` |
372	| topk/sort | `24.0` | `0.2692` |
373	| sparse metadata | `48.0` | `0.1925` |
374	| index_put | `17.6` | `0.1098` |
375	
376	Marlin variant 分布：
377	
378	| variant | calls/step | ms/step | avg us |
379	|---|---:|---:|---:|
380	| `block=128, thread_k=4, grid=[312,1,1]` | `88` | `4.0899` | `46.476` |
381	| `block=256, thread_k=8, grid=[156,1,1]` | `72` | `0.8134` | `11.297` |
382	
383	attention split/paged-kv 进一步拆开：
384	
385	| kernel | calls/step | ms/step | avg us | source |
386	|---|---:|---:|---:|---|
387	| `flash_fwd_splitkv_stage1_kernel` | `8` | `1.4249` | `178.116` | sparse topk stage1 compressed scoring |
388	| `BatchPrefillWithPagedKVCacheKernel` | `8` | `0.3049` | `38.108` | FlashInfer stage2 sparse paged KV |
389	| `PersistentVariableLengthMergeStatesKernel` | `8` | `0.0243` | `3.036` | stage2 merge |
390	
391	关键结论：
392	
393	- fixed S8 trace 与上一轮 direct-state trace 结构一致，说明 SimpleGLA direct-state 收益不是输入偶然。
394	- decode graph 内看不到 b12x runtime kernel；b12x/shape-aware Python 分流仍不是 no-spec S1/S8 graph replay 的主杠杆。
395	- attention 第二大项不能粗暴归因为 FlashInfer paged KV wrapper。最大子项是 `infllmv2_attn_stage1` 触发的 `flash_fwd_splitkv_stage1_kernel`，也就是 sparse topk 的 stage1 scoring。
396	
397	## 17. Attention Stage1/Stage2 Negative Tests
398	
399	stage2 wrapper 结果：
400	
401	| option | result |
402	|---|---:|
403	| `use_tensor_cores=1` default | `20.84 us` |
404	| `use_tensor_cores=0` | unsupported: `Unsupported group_size: 16` |
405	| `disable_split_kv=1` | `230.45 us` |
406	| `fixed_split_size=8192` | `230.93 us` |
407	
408	解释：MiniCPM sparse stage2 每个 head group 是 `qo_heads=16, kv_heads=1`；FlashInfer non-TC wrapper 不支持 `group_size=16`；`disable_split_kv` 会把 stage2 从约 `21 us` 拉到约 `230 us`。新增的实验开关（`SGLANG_MINICPM_DECODE_TENSOR_CORES` / `_DISABLE_SPLIT_KV` / `_FIXED_SPLIT_SIZE`）默认必须保持当前行为。
409	
410	stage1 sparse topk 结果：
411	
412	| seq_len | max_context_len | baseline graph | `split_stage1` graph | topk overlap |
413	|---:|---:|---:|---:|---:|
414	| `70136` | `524288` | `144.86 us` | `159.58 us` | `0.438` |
415	| `135664` | `524288` | `230.19 us` | `251.04 us` | `0.417` |
416	| `135664` | `135664` | `217.55 us` | `239.10 us` | `0.416` |
417	| `524288` | `524288` | `828.28 us` | `855.71 us` | `0.472` |
418	
419	结论：
420	
421	- `split_stage1` 不是可上线优化：更慢，并且只用 k1 scoring，topk overlap 只有约 `0.42~0.47`，语义风险过高。
422	- max_context padding 不是主要矛盾：`135664` 场景把 `max_context_len` 从 `524288` 降到实际长度只省约 `12.6 us/call`。
423	- 下一轮 attention 侧如果要继续，必须做保持 k1+k2 scoring 语义的 stage1 fused kernel，目标是合并 `infllmv2_attn_stage1 + max_pooling_1d_varlen + topk/sort`，而不是打开已有 `fuse_topk` 或 `split_stage1`。
424	
425	## 18. Marlin Remaining Headroom
426	
427	用已有 graph tile sweep 对照 fixed S8 trace 后，Marlin 的剩余空间基本清楚：
428	
429	核心结果：
430	
431	| shape | M | auto graph | best | speedup |
432	|---|---:|---:|---:|---:|
433	| `std_o` | `1` | `8.184 us` | `6.265 us` | `1.306x` |
434	| `std_o` | `8` | `8.195 us` | `8.187 us` | `1.001x` |
435	| `std_qkv` | `1` | `6.375 us` | `6.148 us` | `1.037x` |
436	| `std_qkv` | `8` | `8.186 us` | `8.183 us` | `1.000x` |
437	| `gla_qkv` | `1` | `11.783 us` | `11.402 us` | `1.033x` |
438	| `gla_qkv` | `8` | `12.290 us` | `12.289 us` | `1.000x` |
439	| `gate_up` | `1` | `22.512 us` | `22.512 us` | `1.000x` |
440	| `gate_up` | `8` | `22.534 us` | `22.534 us` | `1.000x` |
441	| `down` | `1` | `14.335 us` | `14.329 us` | `1.000x` |
442	| `down` | `8` | `14.339 us` | `14.338 us` | `1.000x` |
443	
444	结论：
445	
446	- fixed S8 的主 decode batch 是 M=8；M=8 上 Marlin tile 已接近 sweep 最优，继续靠 tile 很难再明显降低 `4.9 ms/step`。
447	- M=1 只有 `std_o` 还有约 `1.9 us/call` 的 microbench 空间，但调用数有限，折到 no-spec e2e 大概率低于 `1%`。
448	- 因此下一轮真正高杠杆仍不是继续盲扫 Marlin tile，而是：
449	  - 保持 k1+k2 语义的 sparse stage1 fused topk；
450	  - 或回到 b12x/Marlin 重新划分，但必须先证明某些 M=8 shapes 能用 b12x 在 CUDA graph 内赢 Marlin。
451	
452	## 19. Fused TopK Consistency Gate
453	
454	用户提醒 `fused topk` 可能有 bug 后，本轮先做 correctness gate 验证：
455	
456	| case | scenario | official vs fused overlap mean | fused duplicate mean | verdict |
457	|---|---|---:|---:|---|
458	| verify `B=16,Q=5,seq=16384` | random | `0.460` | `0.033` | FAIL |
459	| S1 decode `B=3,Q=1,seq=70136` | random | `0.139` | `0.010` | FAIL |
460	| S8 decode `B=8,Q=1,seq=135664` | random | `0.168` | `0.009` | FAIL |
461	
462	定位：`compressed_attention_tilelang()` 只传 `k1` 进 fused kernel，`k2` 未参与计算，破坏官方 k1+k2 scoring 语义；`k1_ref_vs_fused` overlap 也低，说明 pooling/topk 未对齐 k1-only reference（详见 §22）。
463	
464	结论：当前 `--fuse-topk` 不能上马；已加防误用 guard（传 `--fuse-topk` 直接报错，需 `SGLANG_MINICPM_ALLOW_UNSAFE_FUSE_TOPK=1` 才能调试）。后续若继续做 fused topk，目标必须是复现 `infllmv2_attn_stage1(k1,k2) + pooling + topk` 的完整语义。
465	
466	## 20. TopK Select Candidate Held Back
467	
468	在不启用 fused topk 的前提下，曾尝试一个看似无语义风险的小优化：
469	
470	```python
471	block_score.topk(topk, dim=-1).indices.sort(-1).values
472	```
473	
474	PyTorch `topk` 默认 `sorted=True`，但后面马上按 block index 再 sort，一开始按 score 排序是浪费。改为：
475	
476	```python
477	block_score.topk(topk, dim=-1, sorted=False).indices.sort(-1).values
478	```
479	
480	CUDA graph microbench 结果（fp32 和 bf16 趋势一致）：
481	
482	| dtype | case | sorted=True | sorted=False | speedup | equal |
483	|---|---|---:|---:|---:|---|
484	| fp32 | verify `(2,80,256)` | `24.612 us` | `20.490 us` | `1.201x` | True |
485	| fp32 | S1 decode `(2,3,1096)` | `30.709 us` | `27.949 us` | `1.099x` | True |
486	| fp32 | S8 decode `(2,8,2120)` | `34.804 us` | `30.706 us` | `1.133x` | True |
487	
488	进一步在真实 stage1 score 上固定同一个 `block_score` 对比，`sorted=True/False` 输出也一致。但完整 `compressed_attention` 对拍时发现 `infllmv2_attn_stage1` 自身在 verify/S8 形状上存在 run-to-run topk 抖动，导致难以把这项变更独立证明为严格不改输出。为避免把 tie 行为变化带进主路径，生产默认仍保持 `sorted=True`，该项仅作为候选保留。
489	
490	## 21. Decode Pooling No-Zero
491	
492	`infllm_v2.max_pooling_1d_varlen()` 的 Python wrapper 先分配 `torch.zeros` 输出，再调用 CUDA kernel：
493	
494	```python
495	output = torch.zeros(num_heads, total_q, out_len, device=input.device, dtype=input.dtype)
496	C.max_pooling_1d_varlen(...)
497	```
498	
499	读 C kernel 后确认每个有效 `(head, q, out_block)` 都会被覆写；因此 decode 路径可改为 `torch.empty`，省掉输出清零。为了不改 infllm wheel，只在 `minicpm_sparse_utils.py` 增加 `_max_pooling_1d_varlen_no_zero()`，只在 `max_seqlen_q == 1` 的 decode 路径启用；prefill/verify 继续走原始 wrapper。验证结果：
500	
501	| case | zeros | empty | speedup | equal |
502	|---|---:|---:|---:|---|
503	| verify `B=16,Q=5,seq=16384` | `6.998 us` | `8.138 us` | `0.860x` | True |
504	| S1 decode `B=3,Q=1,seq=70136` | `12.402 us` | `8.158 us` | `1.520x` | True |
505	| S8 decode `B=8,Q=1,seq=135664` | `12.369 us` | `12.440 us` | `0.994x` | True |
506	
507	结论：真实 stage1 score 对拍均等（`pool equal=True, topk equal=True`）；完整 stage1 decode graph 净下降约 `1.0~1.4 us/call`（S8 135664 场景基本持平）。这是一个低风险小 patch，只覆盖 no-spec/S1/S8 decode 的 pooling 子项；折到完整 stage1 graph 后收益很小，不能替代 k1+k2 fused stage1。
508	
509	## 22. k1+k2 Stage1 Semantics
510	
511	继续读 `kernels/infllmv2_cuda_impl` 后，stage1 语义更清楚：
512	
513	- Python wrapper `infllmv2_attn_stage1(q, k, v, ...)` 里 `k` 是 `k1`，`v` 实际传的是 `k2`；它不是普通 attention 的 value 输出。
514	- C++ 入口为 `mha_varlen_fwd_stage1()`，返回的 `p` shape 是 `(num_heads_k, total_q, seqlen_k_rounded)`；MiniCPM 后续把它当作 compressed block score 输入给 pooling。
515	- CUDA kernel 分两段：
516	  - 第一段用 `gC`/`v_ptr`，也就是 `k2`，跑 coarse softmax 并得到 row max/sum；
517	  - 第二段用 `gK`/`k_ptr`，也就是 `k1`，调用 `softmax_rescale_gt()` 复用第一段的 row max/sum，再通过 `hdim16_reduce()` 写出 `k1` score。
518	
519	这解释了为什么 k1-only fused topk 和 `split_stage1=True` 都不对：官方 score 不是单独的 `softmax(q @ k1)`，而是由 `k2` coarse LSE 参与归一化后的 `k1` score。保持语义的真正融合应在 stage1 CUDA epilogue 里做（`hdim16_reduce()` 写 `p` 后直接做 block pooling/topk），而非外挂 k1-only TileLang kernel。
520	
521	## 23. Decode Replay Skip-Fill
522	
523	背景：CUDA graph replay 路径里 `compress_k1` / `compress_k2` 使用预分配 buffer。旧逻辑每个 decode step 都先把整段 replay buffer 填成 `-inf`，再由 `compress_k_complete_kernel_new` 写有效区间。profile 中表现为两批较大的 BF16 `FillFunctor` kernel。
524	
525	本轮改动：
526	
527	- `SGLANG_MINICPM_FILL_COMPRESS_BUFFERS=0` 为默认值，即跳过旧的 replay buffer fill。
528	- `SGLANG_MINICPM_FILL_COMPRESS_BUFFERS=1` 只保留为回退/调试开关。
529	- `eval/start_eagle.sh` 已显式带上该默认开关，避免生产启动路径依赖隐式默认值。
530	
531	验证方法：短输入、固定 batch，只 profile decode graph，避免 e2e 噪声。
532	
533	结果：
534	
535	| 配置 | BF16 FillFunctor calls | BF16 FillFunctor total | per decode step |
536	|---|---:|---:|---:|
537	| fill-on | `288` | `1.480 ms` | `0.0925 ms/step` |
538	| skip-fill | `256` | `0.258 ms` | `0.0161 ms/step` |
539	| 差值 | `-32` | `-1.222 ms` | `-0.0764 ms/step` |
540	
541	关键证据：
542	
543	- fill-on 多出的 `32` 次正好是 `16 decode steps * 2 buffers`。
544	- 多出的两批 kernel 分别是 `grid=[65536,1,1]` 和 `grid=[16384,1,1]`，各 `16` 次，对应 `compress_k1` / `compress_k2` 大 buffer fill。
545	- skip-fill 后剩下的 `256` 次 BF16 fill 都是 `grid=[512,1,1]` 的小 fill，不属于本次目标 buffer。
546	- decode graph 总 kernel 时间从 `155.107 ms / 16 steps` 降到 `153.462 ms / 16 steps`，净下降约 `0.103 ms/step`。
547	
548	结论：skip-fill 已在 CUDA graph decode replay 内移除目标那批 `FillFunctor<c10::BFloat16>` kernel。收益量级明确，但不是下一阶段的主杠杆。
549	
550	## 24. 下一轮高 ROI 方向
551	
552	不要继续围绕 `0.05-0.10 ms/step` 的小 kernel 做局部修剪。现有 profiling 指向一个更难但更有潜力的方向：**把 EAGLE verify 后的 GLA/Mamba state update 从 PyTorch fancy indexing 改成一个语义等价的 fused CUDA/Triton kernel**。
553	
554	已有 profile 证据见 `runtime.md §7`：
555	
556	- target verify GPU 时间主导 spec 路径，draft 只有约 `4.7%`。
557	- 一轮 trace 里两个 `at::index_elementwise_kernel` 合计 `1609 ms`，约 `77.6%` GPU time。
558	- 用 launch-time 重新归因后，`mamba_verify_update` 吃掉 `1181 ms / 98.4%` 的 index kernel 时间；之前归因到 `alloc_sparse_new_positions` 是 GPU end-time 对齐 NVTX 的污染。
559	
560	热点代码在 `hybrid_linear_attn_backend.py:update_mamba_state_after_mtp_verify()`：
561	
562	```python
563	ssm_states[:, dst_state_indices, :] = intermediate_state_cache[
564	    :, src_state_indices, last_steps
565	].to(ssm_states.dtype, copy=False)
566	
567	ssm_states[:, dst_track_indices, :] = intermediate_state_cache[
568	    :, src_track_indices, track_steps
569	].to(ssm_states.dtype, copy=False)
570	```
571	
572	难点：
573	
574	- `ssm_states` 是所有 GLA 层共享的多层 state cache，维度大，写入目标是 request cache slot。
575	- `accepted_steps` / `mamba_steps_to_track` 每轮动态变化，且必须和 verify/rollback 语义一致。
576	- 当前 PyTorch 写法会生成大量 gather + scatter index kernel；替换后必须逐项对拍 state，而不是只看输出文本。
577	
578	建议路线：
579	
580	1. 先写离线 microbench + correctness harness，固定真实形状，比较 PyTorch fancy indexing 和 fused kernel 后的 `ssm_states` bit/近似一致性。
581	2. 首版 kernel 只覆盖 SALA 当前 `conv_states is None` 的主路径：把 main scatter 和 track scatter 合并为 1 到 2 个 Triton/CUDA kernel。
582	3. 接入时加 env gate，例如 `SGLANG_MINICPM_FUSED_MAMBA_VERIFY_UPDATE=1`，先只在 EAGLE verify 路径打开。
583	4. 验证顺序：state tensor 对拍 -> no-spec/spec 小样本一致性 -> profile 中 index kernel 是否下降 -> 最后再做受限 e2e。
584	
585	这是下一轮最值得攻的点：它难度比 skip-fill / topk sorted / no-zero pooling 高很多，但 profile 中占比足够大，成功后才可能带来真正可见的吞吐改善。
586	
587	## 25. Current Marlin `.so` 与 EAGLE Draft CUDA Graph 不兼容
588	
589	> 2026-04-26 确认
590	
591	在 §4.1 中确认收益的 `32d27c728ea93203236757d7534b6e68`（current Marlin，含 small-M atomic + shape-aware tile）**会导致 EAGLE-3 draft CUDA graph capture 挂住**（37% 进度卡死）。
592	
593	时间线：
594	
595	| 时间点 | env `.so` | EAGLE draft graph |
596	|---|---|---|
597	| probe-sala/prepare_env.sh 部署后 | `220c18cc`（probe-sala，Apr 21） | 正常 |
598	| 换成 demo-sala `.so` 做 Marlin bench | `32d27c7`（demo-sala，Apr 25） | **挂住** |
599	| 恢复 `220c18cc` | `220c18cc` | 正常 |
600	
601	诊断：
602	
603	- `32d27c7` 比 `220c18cc` 大 562 KB，主要差异是 small-M atomic 路径和 shape-aware tile 表。
604	- marlin-tuning.md 所有 Marlin e2e 测试（§2, §4.1）都在 **no-spec** 下做的，从未用 EAGLE draft graph capture 验证过该 `.so`。
605	- CLAUDE.md 中 "draft CUDA graph capture 有观察到明显退化" 的根因就是这个 `.so`。
606	- `probe-sala/common_ops.abi3.so`（`220c18cc`）是目前唯一被验证可以正常 EAGLE 起服的 `.so`。
607	
608	结论：
609	
610	- **Marlin 3%（§2, §4.1）在 EAGLE 生产路径下不可用。** draft graph capture 过程中 Marlin kernel 的 atomic/tile 行为和 CUDA graph capture 有不明冲突。
611	- 当前生产部署必须使用 `220c18cc`。`demo-sala/common_ops.abi3.so` 已替换为 `220c18cc`。
612	- 如果后续要恢复 Marlin 3%，必须逐项 bisect small-M atomic vs shape-aware tile，找到和 draft graph capture 冲突的具体改动，而不是整体替换 `.so`。
613	
614	## 26. SimpleGLA Direct-State Decode 捞回与 EAGLE E2E 验证
615	
616	> 2026-04-26 从 main 捞回并验证
617	
618	§13 的 SimpleGLA direct-state decode 在 `demosala-rollback` 中被丢失（rollback 到 9a7e04c 时只有 127 行的旧 `simple_gla_decode_kernel.py`）。本轮从 main 捞回并接入生产路径。
619	
620	改动文件：
621	
622	1. `demo-sala/sglang/python/sglang/srt/layers/attention/simple_gla_decode_kernel.py` — 从 main 恢复（127 → 286 行），包含 `simple_gla_decode_update_fwd()`。
623	2. `demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py` — 三处改动：
624	   - 添加 `import simple_gla_decode_update_fwd`
625	   - `__init__` 中添加 `self._simple_gla_direct_decode` flag（读 `SGLANG_SIMPLE_GLA_DIRECT_DECODE` 环境变量，默认 `"1"` 开启）
626	   - GLA forward decode 分支：`use_direct_decode` 条件短路，直接调用 `simple_gla_decode_update_fwd()` 替代 `fused_recurrent_simple_gla` + gather/index_put 链路
627	
628	环境变量：`SGLANG_SIMPLE_GLA_DIRECT_DECODE=1`（`eval/start_eagle.sh` 已设置）。`=0` 可关闭回退到旧路径。
629	
630	离线复现（CUDA graph microbench）：
631	
632	| batch | 旧 generic (us) | 新 direct (us) | speedup | output diff | state diff |
633	|---:|---:|---:|---:|---:|---:|
634	| 1 | 14.38 | 6.16 | **2.33×** | 0.0 | 0.0 |
635	| 8 | 34.84 | 10.28 | **3.39×** | 6.1e-05 | 0.0 |
636	
637	与 §13 原始记录高度一致，bs=8 甚至优于原记录（10.28 vs 14.37 us）。
638	
639	EAGLE E2E 验证：用户确认 EAGLE-3 spec 路径起服正常、draft CUDA graph capture 通过。该优化只接入 no-spec decode 分支（`forward_mode.is_decode()` + `head_dim == 128`），不影响 target_verify / spec 路径。
640
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/nvfp4-kv-investigation.md"
}
```

> TOOL

tool_result Read
```
1	# NVFP4 KV Cache 调研（负结果合集）
2	
3	2026-04-21 的深度调研记录。**结论：NVFP4 KV 在 SALA 当前架构（InfLLM-v2 sparse + page_size=1）上没有可用落地路径；VariableBlockSparseAttentionWrapper 也不带来加速**。保留本文以防重踩。
4	
5	## 1. 出发点（被证伪的旧判断）
6	
7	生产 `--kv-cache-dtype fp8_e5m2` 已经在高并发证明稳定收益。自然想法：NVFP4 KV 理论再省 2× 带宽，是否能进一步提速。
8	
9	[`docs/quantization.md`](quantization.md) 老版本的阻塞理由是 "SGLang MHA 路径 `trtllm_batch_decode_with_kv_cache` 未传 `kv_block_scales`"。**这个结论在 FlashInfer 0.6.8 / cu13 已过时** —— API 早已支持（`flashinfer/decode.py:2260` 的 `kv_cache_sf=(k_sf, v_sf)` 参数）。真正的阻塞点不在 API，而在下文描述的**算法不兼容**。
10	
11	## 2. FlashInfer NVFP4 KV API 的真实约束
12	
13	核对 FlashInfer 0.6.8.post1 源码：
14	
15	| 路径 | backend | sm_120 支持 | page_size 限制 | 通用 sparse | 备注 |
16	|---|---|---|---|---|---|
17	| `trtllm_batch_decode_with_kv_cache` 自动派发到 `xqa` | xqa | ✅ | ∈ {16,32,64,128} | ❌ dense paged | decode.py:2431 |
18	| `trtllm_batch_decode_with_kv_cache` 自动派发到 `trtllm-gen` | trtllm-gen | ❌（仅 sm_100/103） | — | — | TRT-LLM issue #10241 确认 blocked |
19	| `flashinfer.xqa.xqa` 直调 | xqa | ✅（**NVFP4 KV only supported on SM120**，见 xqa.py:309） | ∈ {16,32,64,128} | ❌ | `k_sf_cache/v_sf_cache` 参数存在且可用 |
20	| `BatchDecodeWithPagedKVCacheWrapper` | FA2/FA3 | ✅ | page=1 OK | token-level indices | **不支持 NVFP4 KV** |
21	| `VariableBlockSparseAttentionWrapper`（v0.2+） | FA2/FA3 | ✅（FA3 可能打折） | page=1 OK | block-sparse 原生 | **不支持 NVFP4 KV**（KV dtype 只到 FP8） |
22	
23	**结论**：支持 NVFP4 KV 的 kernel（xqa, trtllm-gen）都要求 page_size ≥ 16；支持 page_size=1 / sparse 的 kernel 都不吃 NVFP4。
24	
25	### NVFP4 存储格式的真正事实
26	
27	NVFP4 (E2M1) 4-bit 值 + **E4M3FN per-16-element block scale**（不是 MXFP4 的 E8M0）。scale 的 block=16 是沿 **head_dim 方向**，**不是沿 token 方向**。所以 NVFP4 存储本身和 page_size=1 完全兼容；page_size≥16 是 xqa kernel 的 **TMA tile 约束**，不是格式约束。
28	
29	SGLang 上游 PR #10078 的 `KVFP4QuantizeUtil` 用的是 E8M0（MXFP4），**格式不对**，喂给 FlashInfer xqa 会导致精度严重退化。不能复用那条量化路径，要用 `flashinfer.nvfp4_quantize(sfLayout=layout_linear)`。
30	
31	## 3. SALA 架构与 page_size=1 的硬依赖
32	
33	`--dense-as-sparse` 启动，SALA 32 层中 8 层 standard attention **永远走 InfLLM-v2 sparse**，24 层 GLA 无 KV cache。sparse path 的 page_size=1 依赖不是历史遗留，是算法决定的：
34	
35	### 3.1 硬编码点（`demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_backend.py`）
36	
37	```python
38	# L1410 (sparse extend path)
39	assert self.page_size == 1
40	key_cache_by_head_group = key_cache.reshape(
41	    -1, self.page_size, layer.tp_k_head_num // 2, layer.head_dim
42	)
43	
44	# L1130 (sparse decode path)
45	sparse_page_table = sparse_kernel_extension.get_block_table_v2(
46	    topk_idx, page_table, ..., self.sparse_topk
47	).reshape(-1, self.num_sparse_topk_tokens)   # 96*64=6144 token slots
48	```
49	
50	### 3.2 InfLLM-v2 是 block-sparse，block_size=64
51	
52	`config.json` 的 `sparse_config`：
53	```
54	block_size = 64       # 每 sparse block 64 连续 tokens
55	topk       = 64       # 每 query 选 top-64 blocks
56	kernel_size = 32, kernel_stride = 16   # compress_k 滑窗
57	window_size = 2048, dense_len = 8192
58	```
59	
60	理论上 `block_size=64 / page_size=16 = 4`，把 page_size 升到 16 + sparse_page_table 改 page 粒度就能对齐 xqa 的 page_size 约束。但实测推进时撞到**深层 page_size=1 依赖**：
61	
62	### 3.3 page_size=16 尝试触发的 latent bugs
63	
64	推进 `--page-size 16 --kv-cache-dtype fp8_e5m2` 时依次踩坑：
65	
66	1. **server_args guard**：`speculative_eagle_topk>1 && page_size>1` 被拒，白名单不含 `minicpm_flashinfer`
67	   - 修复：`server_args.py:2180` 白名单加 `minicpm_flashinfer`（latent bug，值得保留）
68	2. **HybridLinearKVPool 透传 bug**：`enable_kv_cache_copy` 参数没传给内部 `MHATokenToKVPool`，`move_kv_cache` assert 崩
69	   - 触发条件：`eagle_info.py:520-599` 仅 `page_size>1 && topk>1` 分支走 `move_kv_cache`
70	   - 修复：`memory_pool.py:1231` 加参数；`model_runner_kv_cache_mixin.py:562` 显式传 `(speculative_algorithm is not None)`（latent bug，已保留）
71	3. **compress_k 单 token 分配崩**：InfLLM-v2 的 compress_k1/compress_k2 池每 `kernel_stride=16` 步调 `alloc_token_slots(..., 1)`，`PagedTokenToKVPoolAllocator.alloc(need_size=1)` 在 page_size=16 下返回空 tensor
72	   - 位置：`eagle_worker.py:1033` + `mem_cache/allocator.py:315`
73	   - 深度：**架构级不兼容**。compress_k pool 和 full KV pool 共享 allocator/page_size；真要修需要 compress_k 独立 allocator，是中等规模重构
74	
75	这 3 处暴露的只是前几层。推进下去还会撞更多（如 `minicpm_backend.py:1410` 的 assert 本身、InfLLM-v2 kernel 的 token-level 假设等）。
76	
77	## 4. 全球现成 NVFP4 KV kernel 盘点（30+ 项目）
78	
79	需求：NVFP4 KV + page_size=1（或 token-level sparse block_table） + sm_120。
80	
81	### 4.1 最接近但有硬伤的 3 个
82	
83	| 候选 | NVFP4 KV | sparse/page=1 | sm_120 | 硬伤 |
84	|---|---|---|---|---|
85	| FlashInfer `xqa` | ✅ | ❌（page≥16） | ✅ | `page_table` dense 线性，喂不了 InfLLM-v2 top-K block |
86	| SGLang PR #21601 | ✅（quantize 逻辑可复用） | ❌ | ✅ | 上层假定 dense MHA，未 merge |
87	| FlashInfer `VariableBlockSparseAttentionWrapper` | ❌（KV 只到 FP8） | ✅ | ⚠ FA3 on sm_120 可能打折 | 不支持 NVFP4 |
88	
89	### 4.2 查过且不适用的 20+ 项目
90	
91	- TRT-LLM xqa cubin（sm_100/103 only） / FMHA cubins（SM120/121 未 compile，issue #11799）
92	- vLLM NVFP4 KV（未实现，issue #32220） / TurboQuant PR #38479（是 MSE codebook + QJL，不是 NVFP4 格式）
93	- DeepSeek FlashMLA / DSA（FP8 KV，不是 FP4；MLA 架构）
94	- Quest / Block-Sparse-Attention / MInference / native-sparse-attention-triton / Flash-Sparse-Attention / SpargeAttn（全 bf16/FP16 KV）
95	- SageAttention3 Blackwell（diffusion 专用，无 paged KV）
96	- OpenBMB/infllmv2_cuda_impl（sm80/90 only, bf16 KV）
97	- SGLang PR #10078 / #12612 / issue #17365 / issue #19637（均未提供 sm_120 + page=1 + NVFP4 组合）
98	- LMDeploy TurboMind（int4/int8 KV only）
99	- NVFP4-on-4090-vLLM (BenChaliah)（实际 FP4 weight + FP8 KV，非 FP4 KV）
100	- Qwen3.6-NVFP4-DFlash（NVFP4 weight + DFlash，KV 仍 FP8）
101	
102	**结论**：截至 2026-04-21，全球开源范围**不存在** "NVFP4 KV + page_size=1（或 sparse block_table） + sm_120" 的成熟 kernel。SOAR 比赛还在进行中，优胜方案未公开。
103	
104	## 5. 离线微基准数据（本次工作留档）
105	
106	### 5.1 NVFP4 KV decode（xqa，dense path）— 已验证可跑
107	
108	`bench/bench_nvfp4_kv_decode.py` + `bench/bench_nvfp4_kv_official.py`（page_size=16、dense）：
109	
110	| B | L | bf16 (us) | nvfp4 (us) | ratio | K 占用 |
111	|---|---|---|---|---|---|
112	| 1 | 8192 | 12 | 13 | 1.08× | 0.28× |
113	| 8 | 2048 | 11 | 14 | 1.28× | 0.28× |
114	| 8 | 8192 | 21 | 25 | 1.20× | 0.28× |
115	| **8** | **16384** | **97** | **42** | **0.43×** 🎯 | 0.28× |
116	| 32 | 8192 | 210 | 78 | **0.37×** 🎯 | 0.28× |
117	
118	- 大 batch × 长 seq 下 NVFP4 decode 确有 2-3× 加速（HBM 带宽饱和区间）
119	- 但**此 kernel 是 dense xqa，不走 SALA sparse path**
120	- 精度 cos_sim ~0.95（纯随机输入），结构化 attention 预期更好
121	
122	### 5.2 Triton NVFP4 sparse decode（自写 naive 版）— 正确但离 roofline 50×
123	
124	`bench/bench_nvfp4_sparse_decode_triton.py`：
125	
126	- 正确性：cos_sim 0.99 稳定（全 shape）
127	- 性能：B=8 SP=4096 **700us**，对比 bf16 flashinfer ~23us（roofline 10us）→ **自写 naive Triton 离 flashinfer 30×，离 roofline 50×**
128	- 结论：手写追平 flashinfer fp8（更别说超过）需要 split-KV + TMA + tile 优化，几周级别工程，不符合比赛节奏
129	
130	### 5.3 VariableBlockSparseAttentionWrapper vs 当前 baseline
131	
132	`bench/bench_variable_block_sparse_wrapper.py`（bf16 KV，SALA shape）：
133	
134	| 配置 | VBS | BatchDecode(Q=1) | BatchPrefill | VBS/BPF |
135	|---|---|---|---|---|
136	| B=1 SEQ=8K Q=1 | 53us | 66us | 28us | 1.87× ❌ |
137	| B=1 SEQ=8K Q=5 | 73us | — | 28us | 2.63× ❌ |
138	| B=8 SEQ=8K Q=1 | 71us | 31us | 75us | 0.95× |
139	| B=8 SEQ=8K Q=5 | 137us | — | 140us | 0.97× |
140	| **B=8 SEQ=32K Q=5** | **42us** | — | **53us** | **0.80×** 🎯 |
141	| B=32 SEQ=8K Q=5 | 310us | — | 226us | 1.37× ❌ |
142	| B=64 SEQ=8K Q=1 | 432us | 761us | 457us | 0.94× |
143	
144	**结论**：VBS 相对 SALA 当前 `BatchPrefill`（spec verify 主路径）**整体打平或略慢**。仅 B=8 SEQ=32K Q=5 一个点有 20% 加速。**换 wrapper 不是加速方案**。内部两者都是 prefill kernel，kernel 路径等价；SALA 已通过手工 kv_indices 拿到了 block-sparse 语义等价，无挖掘空间。
145	
146	## 6. 三条理论路径 + 推荐
147	
148	| 路径 | 关键动作 | 工程量 | 风险 | ROI |
149	|---|---|---|---|---|
150	| A. 放弃 `--dense-as-sparse`，混合 KV | 短 seq→dense xqa+NVFP4；长 seq→sparse+FP8 | 中 | 影响长上下文精度 | 短 seq 场景有收益 |
151	| B. 自写 Triton sparse+NVFP4 kernel | 500-800 行 Triton，split-KV+TMA | 高（周级） | 难超 flashinfer FP8 | 不确定 |
152	| C. 放弃 NVFP4 KV，守 fp8 | 尝试 fp8_e4m3，优化 compress_k / top-K / Marlin dispatch | 低 | 低 | 已知瓶颈更可能 |
153	
154	**推荐**：路径 C。NVFP4 KV 理论收益（~2× 带宽）不足以值回自写 kernel 的工程投入，也不适合 SALA 的 sparse 架构。把精力投到已知瓶颈（compress_k 前导 / top-K selection / batch-aware Marlin dispatch）更务实。
155	
156	## 7. 保留的改动（latent bug 修复）
157	
158	以下修改不涉及 NVFP4，是本次顺手修的 SGLang fork 原生 bug，**保留**：
159	
160	1. `server_args.py:2180` — `minicpm_flashinfer` 加入 `speculative_eagle_topk>1 && page_size>1` 的 backend 白名单
161	2. `memory_pool.py:1231` — `HybridLinearKVPool.__init__` 接受 `enable_kv_cache_copy` 参数并透传给内部 `MHATokenToKVPool`
162	3. `model_runner_kv_cache_mixin.py:562` — 构造 `HybridLinearKVPool` 时显式 `enable_kv_cache_copy=(speculative_algorithm is not None)`
163	
164	这些修复只在 `page_size>1 + speculative` 组合下才被触发，page_size=1 生产路径无副作用。
165	
166	## 8. 参考文件
167	
168	离线验证脚本（留档）：
169	- `bench/bench_nvfp4_kv_decode.py` — NVFP4 vs bf16 decode（naive quantize）
170	- `bench/bench_nvfp4_kv_official.py` — 同上，用 `flashinfer.nvfp4_quantize` 官方 linear layout
171	- `bench/bench_nvfp4_sparse_decode_triton.py` — 自写 Triton NVFP4 sparse decode（正确性过，性能不达标）
172	- `bench/bench_variable_block_sparse_wrapper.py` — VBS vs BatchDecode/BatchPrefill 3-way 对比
173	
174	关键外部 URL：
175	- [FlashInfer xqa 源码](https://github.com/flashinfer-ai/flashinfer/blob/main/flashinfer/xqa.py)
176	- [FlashInfer sparse.py](https://github.com/flashinfer-ai/flashinfer/blob/main/flashinfer/sparse.py)
177	- [SGLang PR #21601 (NVFP4 KV for SM120)](https://github.com/sgl-project/sglang/pull/21601)（未 merge）
178	- [TRT-LLM issue #10241](https://github.com/NVIDIA/TensorRT-LLM/issues/10241)（NVFP4 KV on sm_120 blocked）
179	
180	> **关联**：InfLLM-v2 blockmask batch>1 bug 修复记录见 [`infllmv2-blockmask-fix.md`](infllmv2-blockmask-fix.md)。若方案 A（kernel 放宽 page_block_size 限制）最终落地，可重新评估 NVFP4 KV 阻塞点 §3 "page_size=1 不兼容" 是否解除。
181	- [NVIDIA NVFP4 KV cache blog](https://developer.nvidia.com/blog/optimizing-inference-for-long-context-and-large-batch-sizes-with-nvfp4-kv-cache/)
182
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/runtime.md"
}
```

> TOOL

tool_result Read
```
1	# Runtime 优化记录
2	
3	## 1. 空响应问题 ✅ 已解决
4	
5	**根因**：旧版 FlashInfer (0.5.3) 的 CUTLASS FP4 GEMM 在 SM120 上产生 NaN → logits 全 NaN → sampling 产生特殊 token → detokenizer 过滤后返回空文本。
6	
7	**解决**：升级 FlashInfer ≥0.6.7.post3 + cuDNN ≥9.15。no-spec / spec 均零空响应，`ori_accuracy=79.11%`。cu13 迁移后 FlashInfer 0.6.8.post1 + cuDNN 9.21 仍稳定。
8	
9	被误判的假设（均已排除）：GDC flag 缺失（平台已有）、Medusa 是主因（no-spec 下仍复现）、CUDA graph buffer overflow（辅助因素，非根因）。
10	
11	## 2. MiniCPM FlashInfer 稀疏路径调研
12	
13	### 背景
14	
15	长上下文样本（prompt ~130K tokens）在稀疏 decode 路径下图外 Python 开销显著。初步怀疑：`forward_decode → get_topk_for_sparse → get_block_table_v3 → FlashInfer kv_indptr/kv_indices 转换` 每 decode step 重复执行。
16	
17	### 结论
18	
19	`sparse_page_table → flashinfer` 转换**不能**提前到 replay 时做：`sparse_page_table` 是每层 `get_topk_for_sparse` 输出，层间 top-k 不同，复用一份会改变语义（验证：同 seed 请求输出 hash 改变）。
20	
21	`fused metadata copy`（`SGLANG_MINICPM_DISABLE_FUSED_META_COPY`）A/B：bs=1 长样本噪声级差异，hash 相同，无收益。
22	
23	### Metadata 冗余（`_compute_single_compression_metadata`）
24	
25	`schedule_batch.prepare_for_decode` 已在 CPU 预算 k1/k2 压缩 metadata 并通过 `forward_batch.*_cpu` 透传；CUDA graph replay 路径（`minicpm_backend.py:1961-2032`）已用 `.copy_()` 消费。Eager decode 路径未消费，形成冗余 GPU 重算。
26	
27	离线 microbench：5× 加速（240→50 us/call），bit-exact，但 e2e 无可感知收益（base 极小）。`fast_level_from_cpu` 已实装（`minicpm_sparse_utils.py`），decode 消费 `*_cpu` 字段。
28	
29	## 3. TARGET_VERIFY replay de-Python 已终结
30	
31	profile 归因（bs=7 dtn=4）：
32	
33	| Phase | 占 verify ms |
34	|---|---|
35	| eagle_verify 总 | 100% |
36	| DC_verify_ai_tolist (GPU sync) | 74% |
37	| target forward GPU | 主导 |
38	| Python control flow | < 5% |
39	
40	**结论**：target forward GPU 时间（~10ms/cycle）主导 verify 总耗时，Python 循环 + `.item()` 只占极小部分。Python 侧 de-Python 优化不具 ROI，**终结此方向**。
41	
42	## 4. 算子优化（已落地）
43	
44	| 优化 | Decode 收益 | Prefill 收益 | 说明 |
45	|---|---|---|---|
46	| RoPE F32 cast 消除 | 140 us/fwd (3.5×) | 11.2 ms/fwd (4.5×) | sgl_kernel RoPE 内部已是 F32；cos_sim=1.0 |
47	| Residual fused multiply-add | 237 us/fwd (2.15×) | 4.4 ms/fwd (5.76×) | 精度高于 F64 参考 |
48	| `scale_emb` / `width` 吸收进权重 | 2 kernels 消除 | 284 us/fwd | BF16-representable 标量，exact |
49	| In-place sigmoid×mul gate | memory pressure ↓ | — | 等价 |
50	| GLA backend cleanup | ~24 us | — | 删冗余 `.contiguous()` + cache 查询 |
51	| flashinfer mm_fp4 离线 autotune | down_proj M=64 3.59×（验证 M 段） | — | 43/70 验证过的 ≥3% 增益入 cache，miss 走 tactic=-1 fallback。详见 [kernels-sm120.md §7.1](kernels-sm120.md#71-flashinfer-mm_fp4-离线-autotune已落地-2026-04) |
52	| **b12x backend + 3-tier dispatch**（集成落地 `SGLANG_ENABLE_B12X=1` default） | decode GEMM kernel 省 32.4%（5 shape × M=24..256）→ e2e ~3% | 0（M=8192 prefill 不覆盖） | Marlin (W4A16) / b12x (W4A4) / CUTLASS (W4A4) 三档，per-shape Marlin 阈值 {8,8,24,16,16}。初版集成用 "pre-permute padded_scales" 错，生产 smoke test 精度回归；改用 `layer.weight_scale_interleaved` + `fp4_quantize` 激活 → **bit-identical vs CUTLASS**，smoke test 通过（1+1=2 正确）。详见 [kernels-sm120.md §7.4](kernels-sm120.md#74-b12x-backend) |
53	
54	（prefill 相关优化另见 [prefill.md](prefill.md)）
55	
56	## 5. stage2 extend_sparse_fa backend 替换（否）
57	
58	长 prefill 混 decode workload，profile（cuda graph 打开）拿到 `prefill_sparse_calls` 平均单次 13.26 ms / 层，内部切分：
59	
60	| 子项 | ms | 占比 |
61	|---|---|---|
62	| `fi_decode_fwd_ms`（FA kernel） | 8.12 | 61% |
63	| `fi_begin_forward_ms`（plan） | 3.19 | 24% |
64	| `fi_convert_ms`（sparse_page_table→flashinfer indices） | 1.92 | 15% |
65	
66	关键事实：stage2 实际走 **BatchDecodeWithPagedKVCacheWrapper**，不是 prefill wrapper。原因是长序列分支 `sparse_max_seq_len_q` 保持默认 1（`minicpm_sparse_utils.py:1309-1333`），触发 `is_prefill=False`；q tokens 摊平到 batch dim，每 q token 一个 "virtual batch"。production shape：`vbatch = 16 req × 512 q_tok × 2 head_group = 16384`，每 vbatch 6144 pages（96 block × 64）。
67	
68	尝试换 FlashInfer backend（`bench/bench_stage2_backends.py`，production shape 离线）：
69	
70	| backend | 结果 |
71	|---|---|
72	| fa2+TC（auto，当前生产） | 7600 μs/call |
73	| fa3 | Ninja 编译失败：fa3 源文件硬编码 sm_90，sm_120 不支持 |
74	| cutlass | `backend must be fa2 or fa3 in gen_batch_prefill_module` —— decode wrapper 拒绝 cutlass |
75	| trtllm-gen | `fmhaRunner.cuh:30 Unsupported architecture` —— sm_120 不支持 |
76	
77	FlashInfer 0.6.8.post1 在 sm_120 上 BatchDecode 只有 fa2+TC 一条路。**backend swap 不通，放弃此方向**。后续若打 stage2 须从 plan overhead / convert overhead 或改 kernel 源（triton 稀疏 decode / flashmla sparse / 虚 batch 合并近似）入手。
78	
79	## 6. 负结果（勿重复踩坑）
80	
81	| 方向 | 结论 |
82	|---|---|
83	| stage2 FlashInfer backend swap（fa3/cutlass/trtllm-gen） | sm_120 全部不支持，见 §5 |
84	| stage2 VariableBlockSparseAttentionWrapper | 4× 慢（398 vs 97 μs），`bench/bench_variable_block_sparse_wrapper.py` |
85	| EAGLE3 draft `--fuse-topk`（tilelang 融合 stage1+pool+topk） | 离线一致性崩（重复率 61%，planted-peak recall 16/160），kernel 只用 k1 且有 dup bug，`bench/bench_fuse_topk_consistency.py` |
86	| FP8 KV cache | 无收益（KV 带宽非瓶颈） |
87	| mamba cache quant (INT8/4) | 不可行（temporal state 累积误差） |
88	| Radix cache | 无收益（bench 每档清 cache） |
89	| Triton NVFP4 GEMV | 2.6× slower（809 vs 307 us/layer） |
90	| FP8 decode | 无收益（权重 1.78× 抵消带宽收益） |
91	| Full Marlin (no hybrid) | prefill 3.8× slower（M=8192） |
92	| SimpleGLA BK=128 kernel | 1.65× slower（eager 1.9× 收益是 Python overhead 假象，CUDA graph 揭真相） |
93	| Medusa K=3 | 微弱（1.543 vs 1.356 tok/step，GLA overhead 2×） |
94	| Triton `kv_indices` kernel | 0.78× slower（`.item()` 在 CPU tensor 上，无 GPU sync 可省） |
95	| `pre_quant_scale` fusion | 不值（CUDA graph 消除 launch overhead；scale 格式 opaque） |
96	| `minicpm_fi` fused metadata copy | 无收益（bs=1 长样本噪声级） |
97	| `_alloc_sparse_for_new_positions` 向量化 | 中性；保留代码，不计收益 |
98	| TARGET_VERIFY replay de-Python | target forward GPU 主导，Python 占比极小（见 §3） |
99	| BS-自适应 EAGLE no-spec 降级 | 实测无收益 |
100	| compressed_k 跨层复用 | smax=64 / 130K A/B 均噪声内，无收益 |
101	
102	## 7. target verify 真实 GPU 时间拆解（2026-04-22）
103	
104	### 问题
105	
106	b12x GEMM backend 落地后，bench 看不到预期 28% 的 e2e 提升。怀疑 target verify 里 GEMM 不是大头。Draft model 时间占比也一并查。
107	
108	### ⚠️ 结论的适用条件
109	
110	- 测试 case：prompt ~20 tokens，`max_tokens=128`，144 次并发 sweep，trace 15s — 是 **短 context 场景**
111	- 生产 `--dense-as-sparse` 下 sparse 路径 **对所有长度都激活**（`dense_len=0`），所以 sparse attn 在短 prompt 也跑，但 seq_len 远小于真实长 context（bench_serving 可到 130K）
112	- 长 context 下 index 占比可能更高或变化，**尚未用 `toolkit/eval_dataset/perf_public_set.jsonl` 的真实长 prompt 复核**
113	
114	### 测量方法
115	
116	**A. draft / target 时间占比（env-gated CUDA event timer）**
117	
118	在 `modelopt_quant.py` 加一个 `_record_replay_timing(kind, start_evt, end_evt)` 累加器，两端入口：
119	- `CudaGraphRunner.replay()`（target verify）：`self.graphs[graph_key].replay()` 前后包一对 `torch.cuda.Event`
120	- `EAGLEDraftCudaGraphRunner._replay()`（draft decode chain）：`self.graphs[self.bs].replay()` 前后包一对
121	
122	每累积到 100 对 event 触发一次 `torch.cuda.synchronize()` + `start.elapsed_time(end)` 求和，dump 到 `/tmp/replay_timing.json`。env `SGLANG_REPLAY_TIMER=1` 启用。
123	
124	启动 + 压测脚本：
125	```bash
126	SGLANG_REPLAY_TIMER=1 bash eval/start_eagle.sh &
127	# 等 Uvicorn running
128	python3 /tmp/trace_prod.py   # S1/S4/S8/S16/S32/Smax 并发 sweep，max_tokens=128
129	cat /tmp/replay_timing.json
130	```
131	
132	**B. target verify kernel 级拆解（nsys delayed capture）**
133	
134	```bash
135	nsys profile --delay=140 --duration=30 --trace=cuda --sample=none \
136	  --output=/tmp/sglang_prof --force-overwrite=true \
137	  bash eval/start_eagle.sh
138	# delay 覆盖 server 启动 + capture graph；
139	# duration 覆盖 trace_prod.py 压测窗口（~15s）
140	nsys stats --report cuda_gpu_kern_sum --format csv \
141	  --output /tmp/sglang_prof_kern /tmp/sglang_prof.nsys-rep
142	# 手动按 time_% 排序 top-30 kernel
143	```
144	
145	解析 CSV 即为每 kernel 的 total time / calls / avg us。nsys 抓的是 GPU 实际执行时间，不含 CPU-side Python 开销。
146	
147	### 结果
148	
149	**A. draft 占比 4.7%**（单并发 sweep，800 target + 800 draft replays）：
150	
151	| | calls | GPU time | avg/call | share |
152	|---|---|---|---|---|
153	| target verify (`CudaGraphRunner.replay`) | 800 | 8509 ms | 10.6 ms | **95.3%** |
154	| draft decode (`EAGLEDraftCudaGraphRunner._replay`) | 800 | 420 ms | 0.53 ms | **4.7%** |
155	
156	draft 本身 kernel 路径已合理：5 个 GEMM 里 3 个（o/gate_up/down）命中 b12x dispatch，2 个（fc/qkv_eagle）在 MARLIN_UPPER 外 M>48 会掉 cutlass —— 但 draft 天花板 4.7% × 受影响比例 16% = **最多 0.1-0.2% e2e 收益**，不值。
157	
158	**B. target 10.6 ms/replay 的 GPU 时间分布**（nsys 30s 窗口总 2073 ms GPU 活跃时间）：
159	
160	| kernel 类别 | total ms | % |
161	|---|---|---|
162	| `at::index_elementwise_kernel` (index get，60us avg × 13652 calls) | 817.7 | **39.4%** |
163	| `at::index_elementwise_kernel` (index_put，194us avg × 4079 calls) | 791.8 | **38.2%** |
164	| b12x `DenseGemmKernel` | 77.8 | 3.8% |
165	| CUTLASS `GemmUniversal` | 50.7 | 2.4% |
166	| `fused_recurrent_fwd_kernel` (GLA) | 23.8 | 1.1% |
167	| Marlin GEMM | 22.7 | 1.1% |
168	| CatArray concat / fill / rms_norm / silu / cub reduce / ... | ~288 | ~13% |
169	
170	**GEMM 全家（b12x + CUTLASS + Marlin）合计 151 ms，仅 7.3%**。我们之前花大力气调 b12x dispatch 只在优化不到 8% 的蛋糕。
171	
172	**两个 `at::index_elementwise_kernel` 实例合计 1609 ms = 77.6% GPU 时间** —— 是 Python `x[mask] = val` / `x[idx]` 这类带 bool/advanced index 的切片赋值。
173	
174	### 定位源头（已完成 — 2026-04-22 晚）
175	
176	**第四轮定位（成功）**：把 NVTX 扩到 `EAGLEWorker.forward_batch_generation` 等各模块（20+ 个 range）。结果：
177	
178	| NVTX range | get<4> 次/ms | put<4> 次/ms | 小计 ms | 占比 |
179	|---|---|---|---|---|
180	| **`alloc_sparse_new_positions`** | **3626 / 300** | **1781 / 333** | **633** | **52.8%** |
181	| `DEAD_graph_replay`（draft_extend replay 周围 eager）| 1869 / 155 | 748 / 240 | 395 | 32.9% |
182	| `EW_verify` 顶层残余 | 2339 / 52 | 129 / 0.2 | 52 | 4.3% |
183	| `EW_draft_extend_after_decode` 顶层残余 | 479 / 37 | 18 / 5.8 | 43 | 3.6% |
184	| `DEAD_prepare_extend`（prepare_extend_after_decode）| 372 / 30 | 9 / 0.5 | 31 | 2.6% |
185	| `verify_kv_evict_mask` + `vkev_*` | 1816 / 3.3 | 0 | 3.3 | 0.3% |
186	| `fwd_extend_L*` 各层 | 0 | 144 / 0.8 | 0.8 | 0.1% |
187	| 其他 | <10 ms | <10 ms | <10 | <1% |
188	
189	**总 index kernel 时间 1200 ms = 1200 / 2074 = 57.9%**（本轮 trace 短、比例与旧 trace 略差异，量级一致）。
190	
191	**第一次"锁定"（错误 — GPU end-time 归因污染）**：`eagle_worker.py:1034 _alloc_sparse_for_new_positions`
192	
193	```python
194	for i in range(bs):                                              # per-request
195	    for sl in range(max(old_sl + 1, kernel_size), new_sl + 1):   # per-new-position
196	        if (sl - kernel_size) % kernel_stride == 0:
197	            loc = alloc_token_slots(batch.tree_cache, 1)         # GPU alloc 1 slot!
198	            rtp.write_sparse_k1(
199	                (batch.req_pool_indices[i], (k1_idx, k1_idx + 1)),
200	                loc.to(torch.int32),
201	            )
202	    # k2 同理（kernel_size*4 / kernel_stride*4）
203	```
204	
205	**为什么是它**：
206	- Python 双重循环，bs × new_positions 次迭代
207	- 每次 `alloc_token_slots(1)` 读 int32 free list → **`index_kernel<4>`**（element size=4 bytes）
208	- 每次 `write_sparse_k1` 做 `req_to_sparse_k1_token[indices] = values`（`memory_pool.py:570-574`），int32 tensor 的 advanced-indexing 写 → **`index_put<4>`**
209	- spec decoding 每步接受 3-4 个 token × 8 reqs × 1009 verify 步 × 概率过 stride 阈值 → 5407 次微 op
210	- **MiniCPM-SALA 特有代码，非 sglang 原生**。EAGLE 跳过了正常 decode 的 batch alloc 路径，这里是补救；但逐 token 分配在 spec 场景下放大成了热点
211	
212	按此结论写了批量化 fix（CPU 聚合 + 一次 alloc + per-req slice 写）。smoke + 10000 次 fuzz 对照过，代码正确。但 mini_bench e2e **无感提升**。
213	
214	**第二次验证（CPU launch-time 归因 — 正确结论）**：
215	
216	改用 `CUPTI_ACTIVITY_KIND_RUNTIME.start`（kernel **CPU launch** 时间）替代 `CUPTI_ACTIVITY_KIND_KERNEL.end`（GPU 执行 end 时间）重做归因：
217	
218	| NVTX range (launch-time 归因) | get<4> 次/ms | put<4> 次/ms | 小计 ms | 占比 |
219	|---|---|---|---|---|
220	| **`mamba_verify_update`** | **9977 / 603** | **1814 / 578** | **1181** | **98.4%** |
221	| `EW_verify` 顶层残余 | 1936 / 8.8 | — | 8.8 | 0.7% |
222	| `vkev_ai_boolmask` (line 510) | 908 / 2.2 | — | 2.2 | 0.2% |
223	| `vkev_verified_id` (line 511) | 908 / 1.1 | — | 1.1 | 0.1% |
224	| `alloc_sparse_new_positions` | — | 874 / 1.2 | 1.2 | 0.1% ← **不是热点** |
225	| 其他 | ~120 | ~110 | ~1 | <0.1% |
226	
227	**真正的主源**：`hybrid_linear_attn_backend.py:1628 update_mamba_state_after_mtp_verify` — **1181ms / 98.4%**。
228	
229	**为什么之前误判（重中之重的教训）**：
230	1. `_mamba_verify_update` 在 `worker.verify()` 里 **launch** 一大波 3D fancy-index kernel 到默认 stream
231	2. 这些 kernel 在 GPU 侧排队，**执行时间远晚于 launch**（几百 us 到几 ms）
232	3. Python 继续往下走，push 下一个 NVTX：`alloc_sparse_new_positions`
233	4. 原 `_alloc_sparse_for_new_positions` 本身 CPU 循环耗时几 ms，期间 GPU 正在消化刚才 mamba 那批 kernel
234	5. nsys 归因默认用 kernel **GPU end-time** 对应 NVTX CPU 时间窗 → mamba 的 kernel 被张冠李戴到 alloc_sparse 名下
235	
236	**检验办法**：用 `correlationId JOIN CUPTI_ACTIVITY_KIND_RUNTIME` 拿 **launch 的 CPU 时间**，一目了然。
237	
238	**`update_mamba_state_after_mtp_verify` 代码本体**（`hybrid_linear_attn_backend.py:1665+`）：
239	
240	```python
241	# SALA 的 24 层 GLA 也走这里（SimpleGLAAttnBackend 继承自 MambaAttnBackendBase）
242	ssm_states[:, dst_state_indices, :] = intermediate_state_cache[
243	    :, src_state_indices, last_steps
244	].to(ssm_states.dtype, copy=False)
245	
246	if conv_states is not None:  # SALA 无 conv
247	    conv_states[:, dst_state_indices, :] = intermediate_conv_window_cache[
248	        :, src_state_indices, last_steps
249	    ].to(conv_states.dtype, copy=False)
250	
251	if mamba_track_indices is not None:  # enable_mamba_extra_buffer 时再 ×2
252	    ssm_states[:, dst_track_indices, :] = intermediate_state_cache[
253	        :, src_track_indices, track_steps
254	    ].to(ssm_states.dtype, copy=False)
255	```
256	
257	`ssm_states` shape `[layers, slots, state_dim]`；`[:, indices_1d, scalar_1d]` 属于 **3D fancy indexing** → 一次调用 1 个 `index_kernel<4>`（read）+ 1 个 `index_put<4>`（write）。1009 verify × 开启的分支数 × ≥2 读写 ≈ 10k 级别，吻合观测到的 9977 get + 1814 put（put 被 in-place scatter 合并所以少）。
258	
259	**alloc_sparse 批量化 fix 的实际影响**：
260	- CPU 端节省 ~30-50us/call Python 循环，累计 ~30ms（非关键路径，无感）
261	- GPU 端：真正 alloc_sparse 的 kernel 只有 ~1ms
262	- **保留 fix** 作为代码清理（phantom 写去除）；e2e 影响 <1%
263	- 未发布也无所谓，绝对不回滚——批量版语义等价且更干净
264	
265	### 下一步：修复候选（按实际 ROI 排序）
266	
267	> **§8 mini_bench 全景归因后的修正**：`mamba_verify_update` 真实 e2e 占比只有 **1.65%**（见下文 §8），Plan A 收益约 2%。真正的大头是 **CPU memcpy/sync 风暴（79% wall time）**，优先级反转。
268	
269	原候选列表保留作为参考：
270	1. `update_mamba_state_after_mtp_verify`（Plan A — triton 融合 scatter，预期 +2% e2e；mini_bench 下不再是第一优先级）
271	2. `DEAD_graph_replay` 395ms（launch-time 归因后可能也有污染，需重评）
272	3. `EW_verify` 顶层残余 ~9ms
273	
274	### 复现产物
275	
276	- `/tmp/sglang_prof_nvtx5.nsys-rep`·`.sqlite` — 基线 trace（未 fix + 满 NVTX）
277	- `/tmp/sglang_prof_fix.nsys-rep`·`.sqlite` — alloc_sparse fix 后（只有 alloc_sparse NVTX）
278	- `/tmp/sglang_prof_fix2.nsys-rep`·`.sqlite` — alloc_sparse fix 后 + 细粒度 `asp_k1_alloc`/`asp_k1_writes`/`asp_k2_*` NVTX
279	- `/tmp/sglang_prof_nvtx{,2,3,4}.nsys-rep` — 过程中多轮证伪
280	- `/tmp/trigger_long.py` — decode-heavy 触发脚本（8 concurrent × 24 requests × 512 max_tokens）
281	- **正确归因 SQL**（必须 join RUNTIME 拿 launch time，不可用 GPU end time）：
282	  ```sql
283	  SELECT k.demangledName, r.start AS launch_cpu, k.end-k.start AS dur
284	  FROM CUPTI_ACTIVITY_KIND_KERNEL k
285	  JOIN CUPTI_ACTIVITY_KIND_RUNTIME r ON k.correlationId = r.correlationId
286	  WHERE k.demangledName IN (...);
287	  ```
288	  Python 侧 `bisect` 把 `launch_cpu` 落入 NVTX range，再按 innermost range 归因。
289	- 代码：各文件（`eagle_worker.py`、`eagle_info.py`、`multi_layer_eagle_worker.py`、`minicpm_sparse_utils.py`、`minicpm_backend.py`）均已加 NVTX range 插桩，保留作常备诊断工具；如需启用可加 `SGLANG_NVTX_PROFILE=1` 门控。
290	
291	### 结论（修正版）
292	
293	1. **Draft 不是瓶颈**（4.7%）；kernel/quant 替换 ROI < 1%，不做
294	2. **GEMM 不是瓶颈**（7.3%）；b12x 的 28% GEMM 省 ≈ 2% e2e，已完成工作保留
295	3. **Index 操作占 57~78% 属实**，但真正主源是 **`update_mamba_state_after_mtp_verify`（1181ms / 98.4%）**，不是之前误报的 `_alloc_sparse_for_new_positions`
296	4. **`_alloc_sparse_for_new_positions` 批量化 fix** 属于代码清理/副产品，e2e 无感。已合入
297	5. **下一步**：把 `update_mamba_state_after_mtp_verify` 的 4 次 3D fancy scatter 融成一个 triton kernel（或审视 SALA 是否该走 Mamba 的 state rollback 路径）
298	
299	**教训**（重中之重）：
300	- **NVTX range + CUDA 异步的时序陷阱**：NVTX push/pop 只标 CPU 时间窗；CUDA kernel 的 GPU end-time 可能在 launch 之后几 ms。用 GPU end-time 匹配 NVTX 会严重偏移大量 kernel 的归因。**必须 join RUNTIME_API 拿 launch CPU 时间** 才是正确归因方式。
301	- 得出"是这个函数"结论前，先做 end-time vs launch-time 对比 sanity check —— 两者 top range 若差异巨大说明有时序污染
302	- CUDA graph `graphId` 列一次性排除"卡在 graph 里"的假设，比继续加 NVTX 高效
303	- 优化 GEMM backend 之前应先 kernel-level profile 确认大头（原结论仍然成立）
304	- **SALA 特有性这次表现为**：GLA 被归到 `MambaAttnBackendBase` 的 verify 后处理路径，命中 sglang 为通用 Mamba 写的 3D fancy scatter，不是 SALA 本身的 bug
305	
306	## 8. mini_bench 全景归因（2026-04-22 晚）
307	
308	### 目的
309	
310	§7 的 "98.4% / 1181ms" 是 **stress workload** 下 verify 期 **index_kernel 这一类里**的占比，**不是 e2e 占比**。mini_bench（S1=3 S8=8，贴近正式评测的 workload）重测，得到真实量级。
311	
312	### 方法
313	
314	同 §7（nsys + NVTX + launch-time 归因），但 workload 换成 mini_bench。Profile 窗 337 s（覆盖 S1 152s + S8 177s decode 全程）。
315	
316	```bash
317	# 样本
318	python3 /tmp/mini_sample.py          # 生成 /tmp/mini_s{1,8}.jsonl
319	# server 在 nsys 下启动，/start_profile(CUDA_PROFILER) → mini_bench → /stop_profile
320	bash /tmp/nsys_start_mini.sh         # EAGLE3 生产配置
321	SPEED_DATA_S1=/tmp/mini_s1.jsonl SPEED_DATA_S8=/tmp/mini_s8.jsonl \
322	  bash /user_4813494d/openbmb/toolkit/bench_serving.sh http://127.0.0.1:30000
323	# 导出 & 归因
324	nsys export --type sqlite -o /tmp/sglang_prof_mini.sqlite /tmp/sglang_prof_mini.nsys-rep
325	python3 /tmp/analyze_mini.py
326	python3 /tmp/top_hotspots.py
327	```
328	
329	### 结果 — GPU 只占 18.5%，CPU 在等
330	
331	**GPU top（337s profile 窗口占比）**：
332	
333	| kernel | calls | GPU ms | %e2e | 备注 |
334	|---|---|---|---|---|
335	| `cutlass::device_kernel`（NVFP4 GEMM） | 15,510 | 18,685 | **5.54** | b12x 已优化 |
336	| `BatchPrefillWithPagedKVCacheKernel` | 840 | 11,683 | 3.47 | flashinfer prefill |
337	| `index_elementwise_kernel` | 607k | 6,455 | 1.91 | 5.28s 归 `mamba_verify_update`，1.17s 别处 |
338	| `vectorized_elementwise_kernel` | 543k | 3,717 | 1.10 | 通用 pointwise |
339	| `flash_fwd_splitkv_stage1_kernel` | 752 | 3,248 | 0.96 | decode full-attn |
340	| `generate_draft_decode_kv_indices` | 25,654 | 1,831 | 0.54 | — |
341	| `act_and_mul_kernel` | 3,102 | 1,779 | 0.53 | — |
342	| `RMSNormKernel` | 13,066 | 1,721 | 0.51 | — |
343	
344	**GPU 总活跃 62,469 ms / 337 s = 18.5% → 其余 81.5% 是 CPU 或空转**
345	
346	### CPU top — **memcpy + sync 风暴（79%）**
347	
348	| API | calls | CPU ms | %window |
349	|---|---|---|---|
350	| **`cudaMemcpyAsync`** | **1,416,819** | **212,556** | **63.1%** |
351	| `cudaStreamSynchronize` | 631,088 | 53,818 | 16.0% |
352	| `cudaLaunchKernel` | 3,005,571 | 9,049 | 2.7% |
353	
354	- 1.4M 次 memcpy / 337s = **4,200/sec**，每 decode round 80-100 次
355	- 平均 150μs CPU / 次 —— 名字叫 Async 但实际 **同步等待**（小张量 D2H readback 典型特征）
356	- memcpy GPU 侧总共只有 864ms（0.26%），**99.6% 的 memcpy 时间花在 CPU 等**
357	
358	### `update_mamba_state_after_mtp_verify` 真实占比
359	
360	| 子 range | CPU 墙时 | GPU 时间 | %e2e |
361	|---|---|---|---|
362	| `mamba_verify_update`（顶层） | 5,405 ms | 5,577 ms | **1.65** |
363	| └ `mv_prep_indices`（Python 打掩码 + cast） | 3,552 ms | 384 ms | 1.05（CPU 主导）|
364	| └ `mv_main_ssm_scatter`（fancy gather+scatter） | 1,484 ms | 5,177 ms | 1.54（GPU 主导）|
365	| └ `mv_track_*`（interval=256，低频） | — | — | 0 触发 |
366	
367	**Plan A triton 融合 kernel 预期收益 ≈ 2% e2e**，远小于 memcpy 风暴。
368	
369	### 优先级反转
370	
371	| 方向 | 预期收益 | 复杂度 |
372	|---|---|---|
373	| **根治 memcpy/sync 风暴** | **5~15% e2e** | 高（源头排查 + 逐点治理）|
374	| Plan A mamba scatter triton | ~2% e2e | 中 |
375	| CUTLASS GEMM 再优化 | <1% | 极高 |
376	
377	**决定**：放下 Plan A，先排查 1.4M 次 memcpy 的源头分布。候选入口：scheduler loop / spec_info 构建 / forward_metadata 准备 / sample readback。
378	
379	### 复现产物
380	
381	- `/tmp/sglang_prof_mini.nsys-rep` · `.sqlite`（323 MB / 835 MB）
382	- `/tmp/mini_sample.py`·`/tmp/nsys_start_mini.sh`·`/tmp/analyze_mini.py`·`/tmp/top_hotspots.py`
383	- `hybrid_linear_attn_backend.py:update_mamba_state_after_mtp_verify` 已加 `mamba_verify_update` / `mv_prep_indices` / `mv_main_ssm_scatter` / `mv_main_conv_scatter` / `mv_track_*` NVTX（保留作常备诊断工具）
384	
385	## 9. memcpy storm 源头锁定 —— `accept_index/predict.tolist()`（2026-04-22 晚 II）
386	
387	> **⚠️ 2026-04-23 复盘**：本节的 "memcpy 优化 ROI 5-9% e2e" 估算**错了**。按 §9 方案（fuse + pinned + non-blocking + event 重叠）实际改了代码跑 profile + e2e：
388	> - profile：`EI_ai_tolist` CPU 墙时 277,581 ms → 545 ms（-99.8%）✅ 账面完美
389	> - **e2e：S8 无收益（甚至略降）** ❌
390	>
391	> 原因：`.tolist()` 的 4ms "CPU 阻塞" **是 target_forward GPU kernel 占 critical path 的 CPU 侧影像，不是独立可压的 CPU 工作**。换成 `event.synchronize()` 只是把等待从一个 API 挪到另一个 API，wall time 不变。
392	>
393	> 修复代码已 revert。方法论教训与权威出处见 **§10**。
394	> **本节的数据仍有价值**（attribution 正确、定位到 `EI_ai_tolist`），**但"打它能收 ROI" 这个结论被证伪**。
395	
396	### 关键修正：nvitop 89% 和 profile 18.5% 并不矛盾
397	
398	nsys 默认 `--cuda-graph-trace=graph` **不展开 graph 内部 kernel**，全部 KERNEL 行 `graphNodeId IS NULL`（经 SQL 验证）。
399	
400	- decode forward 全部在 CUDA graph 内 → kernel 对 profile 不可见 → 看起来 GPU 只有 4%
401	- prefill eager shape 动态，不入 graph → kernel 正常可见 → 看起来 GPU 85-90%
402	- nvitop 采样的是**任一 kernel 是否在跑**的布尔量，在 graph 内跑 kernel 时同样显示高利用率 ✅
403	
404	**decode 时真实物理图景**：
405	- GPU 89% busy（graph 里 forward pass）
406	- CPU 74% busy（**两次 graph launch 之间疯狂 memcpy**）
407	- GPU 11% idle（就是 CPU memcpy/sync 没准备好下一个 graph 的那点空窗）
408	
409	**memcpy 优化修正 ROI：5-9% e2e**（只能填 decode 的 11% idle 窗）——不是之前估的 5-15%。仍然是第一优先级。
410	
411	### Profile 2（含更多 NVTX）: mini2
412	
413	方法同 §8，但在 `eagle_worker.verify()` / `eagle_info.verify()` / `draft()` 里加了 16 个 NVTX range 细分 memcpy 来源。
414	
415	**Profile 窗口**：`/tmp/sglang_prof_mini2.nsys-rep` (488 MB)·`sqlite`(1.26 GB)，窗口 589 s，1.98M memcpy / 875k sync / 4.27M launchKernel。
416	
417	### memcpy CPU 归因（top 10）
418	
419	| NVTX range | 调用 | mc# | mc CPU | **% of all memcpy** |
420	|---|---|---|---|---|
421	| `EW_verify`（外层） | 34,644 | 1,111,236 | 282,174 ms | **87.1%** |
422	| └ `EV_verify_accept` | 34,644 | 242,536 | 278,292 ms | 85.9% |
423	| &nbsp;&nbsp;&nbsp;└ **`EI_ai_tolist`** | **34,644** | **69,288** | **277,581 ms** | **85.7%** |
424	| `EW_draft` | 34,644 | 264,262 | 14,555 ms | 4.5% |
425	| └ `ED_replay_or_forward` | 34,644 | 242,508 | 14,459 ms | 4.5% |
426	| `EW_draft_post` | 34,644 | 554,244 | 5,492 ms | 1.7% |
427	| `EV_target_forward` | 34,644 | 632,186 | 3,093 ms | 1.0% |
428	| `mamba_verify_update` | 34,645 | 103,935 | 291 ms | 0.1% |
429	
430	（`memcpy` 列的"次数"算的是**该 range 里 cudaMemcpyAsync launch 落入的次数**；同一次 `.tolist()` 内部可能触发多次 memcpy）
431	
432	**`EI_ai_tolist` 单独 85.7%**。两行代码 `eagle_info.py:462-463`：
433	
434	```python
435	accept_index_cpu = accept_index.tolist()   # (bs, spec_steps+1) int32 ≈ 96 B
436	predict_cpu = predict.tolist()              # (bs*dtn+1,)        int32 ≈ 170 B
437	```
438	
439	- 69,288 次 cudaMemcpyAsync（每 round 2 次）= 277.6 s CPU
440	- **每次平均 4 ms CPU 阻塞**
441	- 张量 <200 B，**时间完全是在等 GPU** —— `.tolist()` 强制 sync，紧邻上游就是 `target forward CUDA graph`（decode 里最长一段 GPU 工作）
442	
443	### 为什么这两行这么狠
444	
445	```
446	target_fwd(graph, ~4ms GPU)
447	    → verify_tree_greedy (tiny)
448	    → tolist()   ← CPU 硬等 target forward 跑完（~4ms × 2 次）
449	    → pyloop (~50μs Python)
450	```
451	
452	CPU 在 tolist 里什么都没做，纯阻塞。整个 decode round TPOT 才 6 ms，两次 tolist 最坏就是 8ms（实际有部分 overlap，但累计仍占 85% memcpy 时间）。
453	
454	### 修复计划
455	
456	**目标**：消除 `accept_index.tolist() + predict.tolist()` 的 CPU 阻塞。
457	
458	设计了 3 步走方案（合并 memcpy → pinned memory 异步 copy → CPU/GPU 真正并行），预期 +5-9% e2e。**实际修改后 e2e 完全无感（S8 0 收益），修复已 revert。** 原因见 §10：`.tolist()` 的 CPU 阻塞时间是 target_forward GPU kernel 在 critical path 上的 CPU 侧影像，消掉等待只是把阻塞从一个 API 挪到另一个，wall time 不变。`EI_ai_tolist` 是主源这一 attribution 结论正确，但"打它能收 ROI"被证伪。
459	
460	### 复现产物（mini2）
461	
462	- `/tmp/sglang_prof_mini2.nsys-rep` · `.sqlite`（488 MB / 1.26 GB）
463	- `/tmp/memcpy_attrib2.py` · `/tmp/memcpy_size.py` · `/tmp/reconcile_util.py`
464	- 各文件 NVTX 插桩保留作常备诊断工具（`EW_*`、`EV_*`、`EI_*` 等 range）。
465	
466	### 教训
467	
468	- **CUDA graph + nsys**：默认 `--cuda-graph-trace=graph` 不展开 graph 内部。要看 decode 内部 kernel 需 `--cuda-graph-trace=node`。否则会把 "GPU 闲"误读。
469	- **`.tolist()` 在 GPU tensor 上 = 强制 sync**，是隐藏的 CPU 阻塞点。小张量也一样贵 —— 代价全在等 GPU queue。
470	- nvitop 的 utilization 是"任一 kernel 在跑"的布尔采样，和积分 kernel 时间语义不同，两个可以同时成立。
471	
472	## 10. 性能 profiling 方法论复盘（2026-04-23）
473	
474	§9 的修复把 `EI_ai_tolist` 从 profile 的 85.7% 打到 1.2%，但 e2e **完全无感**。这是方法论错误，不是个案失败。本节把教训和权威出处钉死，避免再踩。
475	
476	### 核心陷阱：CPU 在 sync API 里的时间 ≠ CPU 工作量
477	
478	**NVIDIA CUDA C Best Practices Guide** 原话（profiling 章节）：
479	> When using CPU timers, it is critical to remember that many CUDA API functions are asynchronous. **CPU time spent in synchronization APIs (like `cudaDeviceSynchronize()`) is actually GPU work attribution, not CPU overhead.** The true critical path emerges only after accounting for this distinction.
480	
481	补充原文：
482	> `cudaMemcpyAsync()` **requires pinned host memory** [for asynchrony]. Without pinned memory backing, async transfers may not function as intended.
483	
484	**直译到我们这次**：
485	- baseline 的 `.tolist()` 等价于 `cudaMemcpyAsync(DtoH, pageable)` = 阻塞版本
486	- 那 4ms CPU 墙时 = target_forward kernel（GPU critical path）的 CPU 侧影像
487	- 消掉这段 CPU 等待 → `event.synchronize()` 上阻塞同样 4ms（或者 CPU 空转等下一段 GPU-dep 工作）
488	- **critical path 没变 → wall time 没变**
489	- profile "变好看" 只是 attribution 改了 API，不是 wall 被压缩了
490	
491	### 用 Amdahl's Law 算 ROI 天花板（也是权威要求）
492	
493	CUDA Best Practices 章节 12（Scaling）要求在优化前就用 Amdahl 算天花板：
494	
495	$$S \le \frac{1}{(1-P) + P/N} \quad ; \quad P = \text{可并行比例}, N = \text{并行度}$$
496	
497	对我们的 decode：
498	- 真实 GPU 活跃 ~89%（nvitop），CPU-侧优化对应 "(1-P) = 11%" 段
499	- CPU-侧优化 **e2e 上限 = 1/(0.89+0.11·0) = 1.12×**，**即 ≤ 11% e2e**
500	- §9 估 "5-9%" 已经吃掉 GPU idle 上限的一半 → 需要严格证明"那 11% 里有 5-9% 是 host-wait"
501	- 当时**没证明**，直接写进文档。这是方法论事故。
502	
503	### 正确的 GPU-idle breakdown：Meta HTA 的 3 分类
504	
505	Meta **Holistic Trace Analysis** (HTA) 定义的 **Idle Time Breakdown**（PyTorch 官方博客 _Trace Analysis for the Masses_ 推荐工具）：
506	
507	1. **Host wait** — GPU 闲，因为 CPU 还没 launch 下一个 kernel → 可优化，CPU 侧可收
508	2. **Kernel wait** — GPU 闲，因为在等另一个 kernel 的依赖 → 优化 stream/graph 结构
509	3. **Unknown** — 其他（OS 调度 / 驱动开销 / PCIe 等）→ 通常硬啃不动
510	
511	**只有 (1) host-wait 才是 CPU 侧优化能收的。** 我们从未测过 host-wait 占比就直接估 "5-9%"，等于空手套白狼。
512	
513	### 决策树（从今以后按这个来）
514	
515	每次 CPU 侧优化候选出来前，必须先过：
516	
517	```
518	Step 0  nsys profile  --cuda-graph-trace=node   ← 必须 node，不能 graph
519	              ↓
520	Step 1  算 GPU 实际活跃 % = Σ(kernel_duration) / profile_window
521	              ↓
522	Step 2  GPU 活跃 ≥ 90%?
523	        ├── 是 → 纯 GPU-bound。CPU 侧再好都 ≤ 10%。
524	        │        优先攻 GPU top kernels（走 b12x / CUTLASS / Marlin 路线）
525	        │
526	        └── 否 → GPU idle > 10%，拆 idle breakdown：
527	              ↓
528	        Step 3  用 HTA 或手算：host-wait / kernel-wait / unknown
529	              ↓
530	        Step 4  host-wait 占比决定 CPU 侧 ROI 天花板
531	                host-wait < 5%  → CPU 侧不做
532	                host-wait 5-15% → 可做，但先验证目标改动能挤掉 host-wait
533	                host-wait > 15% → 值得深究
534	              ↓
535	        Step 5  改完必须 e2e 再测一遍确认 host-wait 真的下去了
536	                profile "账面变好" 不算数，只认 wall time
537	```
538	
539	### 为什么 nsys "CPU API CPU 时间" 是陷阱
540	
541	nsys 的 `CUPTI_ACTIVITY_KIND_RUNTIME` 表记的是 **CPU 线程在该 API 调用里从 entry 到 return 的 wall time**：
542	- 对 `cudaMemcpyAsync(DtoH, pageable)` → 阻塞型 API → 这段 wall = 等 GPU 的时间
543	- 对 `cudaStreamSynchronize` → 显式阻塞 → 这段 wall = 等 GPU 的时间
544	- **两者 accumulate 的 "CPU 时间" 都是 GPU 时间的投影**，**不是可优化的 CPU 工作**
545	
546	把这类 "CPU time" 当 CPU 工作优化 = 优化了也没用。
547	
548	### 正确量 GPU-idle 的操作步骤
549	
550	使用 `--cuda-graph-trace=node` 导出 SQLite 后：
551	
552	```sql
553	-- profile window
554	SELECT MIN(start), MAX(end) FROM NVTX_EVENTS WHERE text LIKE '%decode%';
555	-- 或用整个 prof window
556	
557	-- GPU 活跃时间 = Σ kernel duration
558	SELECT SUM(end-start)/1e6 AS gpu_active_ms FROM CUPTI_ACTIVITY_KIND_KERNEL;
559	
560	-- GPU-idle = window - gpu_active
561	-- gpu_active / window = 真实 GPU 利用率
562	
563	-- Host-wait proxy：统计相邻两个 kernel end-to-next-start 间隙，
564	-- 该间隙内如果 CPU 正在 cudaLaunchKernel 之外的 API 里 → 潜在 host-wait
565	-- 更精确要对齐 stream 和 CPU thread timeline（HTA 做的事）
566	```
567	
568	### 对本项目的具体决策
569	
570	- `EI_ai_tolist` 修复已 revert，code 回到 baseline（仅保留 NVTX 诊断）
571	- 后续**所有 CPU 侧候选**（`EV_free_draft_kv`、`alloc_sparse_new_positions`、`mv_prep_indices` 等）在动手前**必须**先按上面决策树跑 node-trace + idle breakdown
572	- 真正可动的方向回到 **GPU critical path kernel**：
573	  - b12x（已落地，decode GEMM -32.4%）继续 tune
574	  - `BatchPrefillWithPagedKVCacheKernel` 3.47% e2e，可看
575	  - `flash_fwd_splitkv_stage1_kernel` 0.96%，小
576	  - `update_mamba_state_after_mtp_verify` 原 Plan A triton 融合 2% e2e —— 如果 host-wait 确认 <5%，这是下一个正经目标
577	
578	### 附：未来 profile 的最低配置
579	
580	```bash
581	nsys profile -t cuda,nvtx \
582	    --cuda-graph-trace=node \           # 必须 node
583	    --cuda-event-trace=false \
584	    --capture-range=cudaProfilerApi --capture-range-end=stop \
585	    -o /tmp/prof_xxx -f true --stats=false \
586	    <server-cmd>
587	```
588	
589	导出后必跑三件事：
590	1. **GPU 活跃 %** （上面 SQL）
591	2. **Idle breakdown**（host-wait vs kernel-wait vs unknown）
592	3. **Top kernels by GPU duration**（不是 launch count、不是 CPU memcpy time）
593	
594	### 权威出处
595	
596	- NVIDIA CUDA C++ Best Practices Guide · §8（Timing） · §12（Scaling）
597	- Nsight Systems User Guide · Timeline View / NVTX integration
598	- PyTorch Blog _Trace Analysis for the Masses_
599	- Meta Holistic Trace Analysis · Idle Time Breakdown
600	
601	### 教训落地（MEMO）
602	
603	- "profile 里某 API 用了 X% CPU 时间" **不是**优化目标，目标永远是 **wall time**
604	- wall time 不动的优化 = 浪费工作 + 增加代码复杂度 + 污染未来 profile
605	- 改完第一件事是 **e2e benchmark**，profile 是辅助不是结论
606	
607	### 附录：node-trace 实测基线（2026-04-23）
608	
609	按 §10 决策树要求，用 `--cuda-graph-trace=node` 重跑 mini_bench 并做 GPU union-busy + global idle breakdown，作为后续所有 CPU/GPU 优化决策的基准：
610	
611	**Profile 窗**：584 s（覆盖 S1=8 + S8=24 全程）；`/tmp/sglang_prof_node.nsys-rep`（1.35 GB）·`.sqlite`（4.1 GB）
612	
613	**Workload 类别**：
614	
615	| 指标 | 值 | 含义 |
616	|---|---|---|
617	| GPU union-busy | **82.3%** | 任意 stream 在跑 kernel 的时间占比（和 nvitop 89% 差 6 pp 来自 node-trace profile 开销） |
618	| 全局 GPU idle | 17.7% | 所有 stream 同时空闲的时间 |
619	| **host-wait** | **9.64%** of window（= 54% of idle） | 下一个 kernel 的 CPU launch 晚于 gap 起点 → 真可 CPU-侧优化 |
620	| alloc/dep | 0.11% | launch 已入队但 GPU 未起 → stream 依赖/驱动 |
621	| tiny <10μs | 5.19% | launch 开销噪声，不可优化 |
622	| unknown | 2.77% | OS/driver/PCIe，硬啃不动 |
623	
624	**关键结论**：
625	
626	1. **workload 是 GPU-bound**（82.3% busy）→ GPU kernel 优化仍是第一优先级
627	2. **CPU 侧优化 e2e 绝对天花板 = 9.6%**（host-wait 总量）。任何 CPU 侧改动不能超过这个数字
628	3. §9 估 "5-9%" 数量级猜对了，但推理错误 —— 假定 memcpy = host-wait；`EI_ai_tolist` 修复后 e2e 0 收益证明 memcpy **不是** host-wait 主源
629	4. 9.6% host-wait 分布多处、每处很小，**没有单点能吃掉 5%+**，碎片化优化的 ROI/risk 比差
630	
631	**Top GPU kernels on main stream 7**（按 GPU 时间，未来 kernel 优化候选）：
632	
633	| kernel | calls | GPU 时间 | % window |
634	|---|---|---|---|
635	| `device_kernel`（NVFP4 GEMM） | 49,665 | 59.4 s | **10.17%** |
636	| `BatchPrefillWithPagedKVCacheKernel` | 2,683 | 37.5 s | 6.42% |
637	| `index_elementwise_kernel` | 826,622 | 15.4 s | 2.63% |
638	| `vectorized_elementwise_kernel` | 788,645 | 10.9 s | 1.87% |
639	| `flash_fwd_splitkv_stage1_kernel` | 2,408 | 10.6 s | 1.81% |
640	| `act_and_mul_kernel` | 9,933 | 5.7 s | 0.97% |
641	| `RMSNormKernel` | 41,839 | 5.4 s | 0.93% |
642	| `quantize_with_block_size_tma` | 48,675 | 4.3 s | 0.74% |
643	
644	**实操建议**：
645	- **GEMM (b12x) 继续 tune**：10.17% 最大头，且已在做
646	- **BatchPrefillWithPagedKVCacheKernel**：6.42%，长 context prefill，可看
647	- **index_elementwise_kernel**：826k 次调用，2.63%，融合/消除可节省（对应 Plan A triton scatter）
648	- CPU 侧任何改动前先证明能动 host-wait 里的某一块；不能的话别动
649	
650	**复现产物**：
651	
652	```bash
653	# node-trace profile
654	bash /tmp/nsys_start_node.sh                          # server under nsys --cuda-graph-trace=node
655	# bench + /start_profile + /stop_profile 见 /tmp/run_bench_prof.sh
656	
657	# 归因
658	python3 /tmp/gpu_union_busy.py      # 全局 busy/idle
659	python3 /tmp/gpu_global_idle.py     # idle breakdown: host-wait / alloc-dep / tiny / unknown
660	python3 /tmp/gpu_idle_breakdown.py  # 单流（stream 7）级 breakdown，用来看局部 pipeline 结构
661	python3 /tmp/host_wait_refined.py   # host-wait 再拆 REAL vs FAKE(sync) + NVTX 归因
662	python3 /tmp/idle_unknown_tiny.py   # unknown 拆 launch API、tiny <10μs 直方图
663	```
664	
665	### 10.B 深挖（2026-04-23）：17.7% idle 的 "真正可动" 比例
666	
667	Table 1 初版把 unknown 记成 2.77% "OS/driver/PCIe 硬啃不动"，把 host-wait 记成 9.64% "全可 CPU 优化"。两个都太粗。深挖一轮后的更新：
668	
669	**Unknown 16.2s 其实是分类器漏判**。原脚本只关联 `cudaLaunchKernel_v7000`，但生产路径有多种 launch API：
670	
671	| 次级 launch API | 时间 | 占 unknown |
672	|---|---|---|
673	| `cudaGraphLaunch_v10000` | 9.78s | 60.4% |
674	| `cuLaunchKernelEx`（Triton） | 3.99s | 24.6% |
675	| `cudaLaunchKernelExC_v11060` | 2.43s | 15.0% |
676	
677	这些本质是 **CUDA graph 入口和 Triton kernel 边界**，不是神秘事件，也不能被 CPU 侧优化。
678	
679	**Host-wait 9.64% 再拆（`/tmp/host_wait_refined.py`）**：
680	
681	- **FAKE (sync overlap) 0.18%**（1.03s，1.8% of HW）：gap 被 cudaStreamSync / cudaEventSync / cudaMemcpy 覆盖 → CPU 在等 GPU，是 GPU 工作伪装成 host-wait，优化无效。比例小是意外：说明 §10 主段担忧的陷阱在这一次数据里不是主因（EI_ai_tolist 情形是少数集中点）
682	- **REAL 9.47%**（55.28s，98.2% of HW）：真 CPU 侧可攻击。但**必须**再剔除 inter-request bench 间隔：
683	
684	| REAL host-wait 分布 | 时间 | 占窗口 | 性质 |
685	|---|---|---|---|
686	| `(none)` NVTX — 3 个巨型 gap（4.2s + 1.0s + 1.0s）+ 17 个 ~47ms | 22.99s | **3.94%** | bench 请求间隔，生产工作流不存在 |
687	| `EV_target_forward` | 12.25s | 2.10% | target 模型 forward，Python 层间开销 |
688	| `EW_verify` | 4.48s | 0.77% | verify 阶段 Python |
689	| `EI_evict_mask` | 3.48s | 0.60% | eviction mask 构造 |
690	| `EI_ai_tolist` | 2.57s | 0.44% | `.tolist()`（§9 验证过 fix 无收益） |
691	| `EW_draft_post` | 2.32s | 0.40% | draft 后处理 |
692	| 其他 11 个 region（每个 <0.4%） | ~7.2s | ~1.2% | 分散 |
693	
694	→ **decode 内部真可攻击 host-wait ≈ 32.3s = 5.5% of window**，不是 9.6%
695	
696	**Tiny 30.3s 的几何解读**：窗口 584s 内跑了 **3240 万个 kernel**，即 **55,515 kernels/sec**。如果每个 kernel 后面有 1μs gap → 32.4s = 5.55% 窗口 ← 和 tiny 5.19% 几乎对上。88% 的 tiny gap <1μs（avg 0.56μs），这是 CUDA 自己的 launch 延迟下限，CPU 优化吃不到。要压这一块只能减少 kernel 数量（**fusion**）或扩大 CUDA graph 覆盖范围（把更多 boundary 吞进 graph）。
697	
698	**17.7% idle 最终归类**：
699	
700	| 分量 | 占窗口 | 性质 | 可攻击？ |
701	|---|---|---|---|
702	| decode 内部真 host-wait | **~5.5%** | CPU 侧 Python / dispatch 逻辑 | 可但分散，单点 ≤2.1% |
703	| inter-request bench idle | ~3.9% | bench 请求之间空档 | 否（生产不存在） |
704	| tiny <10μs launch 下限 | 5.2% | kernel 碎片化结构性 | 只能 fusion / 扩 graph |
705	| CUDA graph / Triton launch 边界 | ~2.8% | launch 入口结构性 | 否 |
706	| 真 alloc/dep + 其他 | ~0.2% | stream 依赖 | 否 |
707	
708	**最终决策（取代 §10 主段"9.6% ROI 天花板"）**：
709	
710	1. **生产工作流下 CPU 侧 ROI 硬顶 = ~5.5%**（不是 9.6%），且 **单点最大只 2.1%**（EV_target_forward）。任何 CPU 侧大改动的 ROI/risk 都不值得做
711	2. **GPU 侧方向不变**：b12x GEMM (10.17%) + BatchPrefill (6.42%) 仍是第一优先级
712	3. **次级新信号**：kernel 数量 55k/sec → **fusion 路线天然吃得到 tiny 5.2% + 部分 target_forward Python 开销**。b12x 本身是 fused NVFP4 GEMM epilogue，恰好符合这条路径；Plan A triton scatter 同理。这两条比 "优化 CPU" 更正派
713	4. §10 主段保留当警示（CPU 时间 = GPU 归因陷阱仍然存在，EI_ai_tolist 就是样本），但 ROI 数字以 **5.5%** 为准
714
```

> AGENT

现在，我将并行读取关键的源文件。

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1	import logging
2	import os
3	import time
4	from copy import copy
5	from typing import List, Optional, Tuple
6	
7	import torch
8	import torch._dynamo
9	
10	# select_top_k_tokens (spec_utils.py) is @torch.compile(dynamic=True) and gets
11	# specialized per (i, hidden_states is None, dtn, topk) combo. Dynamic spec
12	# mode (D5+D7+NO_SPEC, multiple capture_bs) easily blows past the default
13	# recompile_limit=8 → dynamo gives up and runs eager (1-4% loss/step). 32 is
14	# a safe ceiling that fits all current specializations.
15	torch._dynamo.config.recompile_limit = 32
16	
17	from sglang.srt.distributed import get_tp_group
18	from sglang.srt.hardware_backend.npu.graph_runner.eagle_draft_npu_graph_runner import (
19	    EAGLEDraftNpuGraphRunner,
20	)
21	from sglang.srt.layers.dp_attention import get_attention_tp_group
22	from sglang.srt.layers.logits_processor import LogitsProcessorOutput
23	from sglang.srt.layers.moe.utils import (
24	    speculative_moe_a2a_backend_context,
25	    speculative_moe_backend_context,
26	)
27	from sglang.srt.layers.utils.logprob import add_output_logprobs_for_spec_v1
28	from sglang.srt.managers.io_struct import UpdateWeightsFromTensorReqInput
29	from sglang.srt.managers.schedule_batch import ScheduleBatch
30	from sglang.srt.managers.scheduler import GenerationBatchResult
31	from sglang.srt.managers.tp_worker import TpModelWorker
32	from sglang.srt.mem_cache.chunk_cache import SWAChunkCache
33	from sglang.srt.mem_cache.common import (
34	    alloc_paged_token_slots_extend,
35	    alloc_token_slots,
36	    get_last_loc,
37	)
38	from sglang.srt.model_executor.forward_batch_info import (
39	    CaptureHiddenMode,
40	    ForwardBatch,
41	    ForwardMode,
42	)
43	from sglang.srt.server_args import ServerArgs
44	from sglang.srt.speculative.draft_utils import DraftBackendFactory
45	from sglang.srt.speculative.eagle_draft_cuda_graph_runner import (
46	    EAGLEDraftCudaGraphRunner,
47	)
48	from sglang.srt.speculative.eagle_draft_extend_cuda_graph_runner import (
49	    EAGLEDraftExtendCudaGraphRunner,
50	)
51	from sglang.srt.speculative.eagle_info import (
52	    _EAGLE_TRACE_PATH,
53	    _eagle_trace_emit,
54	    EagleDraftInput,
55	    EagleVerifyInput,
56	    EagleVerifyOutput,
57	)
58	from sglang.srt.speculative.eagle_utils import (
59	    build_tree_kernel_efficient,
60	    organize_draft_results,
61	)
62	from sglang.srt.speculative.spec_info import SpeculativeAlgorithm
63	from sglang.srt.speculative.spec_mode import (
64	    SpecMode,
65	    SpecModeConfig,
66	    load_config as load_spec_mode_config,
67	)
68	from sglang.srt.speculative.spec_utils import (
69	    assign_draft_cache_locs,
70	    detect_nan,
71	    draft_tp_context,
72	    fast_topk,
73	    generate_token_bitmask,
74	    get_last_loc_large_page_size_large_top_k,
75	    load_token_map,
76	    select_top_k_tokens,
77	)
78	from sglang.srt.sampling.sampling_batch_info import SamplingBatchInfo
79	from sglang.srt.utils import (
80	    MultiprocessingSerializer,
81	    empty_context,
82	    get_available_gpu_memory,
83	    is_cuda,
84	    is_npu,
85	    next_power_of_2,
86	)
87	from sglang.srt.utils.patch_torch import monkey_patch_torch_reductions
88	
89	_is_npu = is_npu()
90	
91	if is_cuda():
92	    from sgl_kernel import segment_packbits  # noqa: F401
93	
94	logger = logging.getLogger(__name__)
95	
96	
97	def _detect_draft_model_quantization(
98	    draft_model_path: Optional[str],
99	    default_quant: Optional[str],
100	) -> Optional[str]:
101	    """Return the quantization scheme to use for the EAGLE-3 draft model.
102	
103	    Detection order:
104	    1. hf_quant_config.json: {"quantization": {"quant_algo": "NVFP4", ...}}
105	       — written by convert_to_sglang.py; presence means pre-quantized NVFP4.
106	    2. config.json quantization_config.quant_algo = "NVFP4" (legacy flat format).
107	    3. config.json quantization_config.quant_type in ("nvfp4", "modelopt_fp4")
108	       (original format before fix).
109	
110	    Returns "modelopt_fp4" if NVFP4 detected, else None (BF16 legacy mode).
111	    """
112	    if draft_model_path is None:
113	        return None
114	    import json, os
115	
116	    # ── 1. hf_quant_config.json (primary, written by convert_to_sglang.py) ──
117	    hf_quant_path = os.path.join(draft_model_path, "hf_quant_config.json")
118	    if os.path.exists(hf_quant_path):
119	        try:
120	            with open(hf_quant_path) as f:
121	                hf_cfg = json.load(f)
122	            quant_algo = hf_cfg.get("quantization", {}).get("quant_algo", "").upper()
123	            if "NVFP4" in quant_algo or "FP4" in quant_algo:
124	                logger.info(
125	                    "Draft model at %s has hf_quant_config.json with %s — "
126	                    "enabling modelopt_fp4 (Marlin W4A16)",
127	                    draft_model_path, quant_algo,
128	                )
129	                return "modelopt_fp4"
130	        except Exception:
131	            pass
132	
133	    # ── 2/3. config.json quantization_config (fallback) ────────────────────
134	    config_path = os.path.join(draft_model_path, "config.json")
135	    if not os.path.exists(config_path):
136	        return None
137	    try:
138	        with open(config_path) as f:
139	            cfg = json.load(f)
140	        qcfg = cfg.get("quantization_config", {})
141	        quant_algo = qcfg.get("quant_algo", "").upper()
142	        quant_type = qcfg.get("quant_type", "").lower()
143	        if "NVFP4" in quant_algo or "FP4" in quant_algo or quant_type in ("nvfp4", "modelopt_fp4"):
144	            logger.info(
145	                "Draft model at %s has NVFP4 in config.json — enabling modelopt_fp4",
146	                draft_model_path,
147	            )
148	            return "modelopt_fp4"
149	    except Exception:
150	        pass
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/spec_mode.py"
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
45	    d5_mars_theta: float       # per-mode override; -1 means "use mars_theta"
46	    d7_mars_theta: float
47	
48	    def effective_d5_theta(self) -> float:
49	        return self.d5_mars_theta if self.d5_mars_theta >= 0.0 else self.mars_theta
50	
51	    def effective_d7_theta(self) -> float:
52	        return self.d7_mars_theta if self.d7_mars_theta >= 0.0 else self.mars_theta
53	
54	    def summary(self) -> str:
55	        if not self.enabled:
56	            return "EAGLE dynamic mode: DISABLED (static D5)"
57	        return (
58	            "EAGLE dynamic mode: ENABLED | "
59	            f"NO_SPEC bs>={self.enter_no_spec_bs} (leave<={self.leave_no_spec_bs}) | "
60	            f"D7 bs<={self.enter_d7_bs} (leave>={self.leave_d7_bs}) | "
61	            f"D5 (topk={self.d5_topk}, steps={self.d5_steps}, dtn={self.d5_dtn}, "
62	            f"theta={self.effective_d5_theta()}) | "
63	            f"D7 (topk={self.d7_topk}, steps={self.d7_steps}, dtn={self.d7_dtn}, "
64	            f"theta={self.effective_d7_theta()})"
65	        )
66	
67	
68	def _env_int(name: str, default: int) -> int:
69	    raw = os.environ.get(name)
70	    if raw is None or raw == "":
71	        return default
72	    try:
73	        return int(raw)
74	    except ValueError:
75	        logger.warning("[spec-mode] %s=%r not int, fallback %d", name, raw, default)
76	        return default
77	
78	
79	def _env_float(name: str, default: float) -> float:
80	    raw = os.environ.get(name)
81	    if raw is None or raw == "":
82	        return default
83	    try:
84	        return float(raw)
85	    except ValueError:
86	        logger.warning("[spec-mode] %s=%r not float, fallback %f", name, raw, default)
87	        return default
88	
89	
90	def load_config() -> SpecModeConfig:
91	    cfg = SpecModeConfig(
92	        enabled=os.environ.get("EAGLE_DYNAMIC_MODE", "0") == "1",
93	        enter_no_spec_bs=_env_int("EAGLE_NO_SPEC_BS", 31),
94	        leave_no_spec_bs=_env_int("EAGLE_NO_SPEC_LEAVE_BS", 28),
95	        enter_d7_bs=_env_int("EAGLE_D7_BS", 1),
96	        leave_d7_bs=_env_int("EAGLE_D7_LEAVE_BS", 3),
97	        d5_topk=_env_int("EAGLE_D5_TOPK", 2),
98	        d5_steps=_env_int("EAGLE_D5_STEPS", 2),
99	        d5_dtn=_env_int("EAGLE_D5_DTN", 5),
100	        d7_topk=_env_int("EAGLE_D7_TOPK", 2),
101	        d7_steps=_env_int("EAGLE_D7_STEPS", 3),
102	        d7_dtn=_env_int("EAGLE_D7_DTN", 7),
103	        mars_theta=_env_float("EAGLE_MARS_THETA", -1.0),
104	        # Per-mode MARS theta overrides. -1 = inherit global mars_theta.
105	        # S1 (bs=1) runs entirely in D7, so a more aggressive D7 theta can
106	        # boost S1 accept-length without affecting D5/no-spec quality.
107	        d5_mars_theta=_env_float("EAGLE_D5_MARS_THETA", -1.0),
108	        d7_mars_theta=_env_float("EAGLE_D7_MARS_THETA", -1.0),
109	    )
110	    _validate(cfg)
111	    return cfg
112	
113	
114	def _validate(cfg: SpecModeConfig) -> None:
115	    if not cfg.enabled:
116	        return
117	    if cfg.leave_no_spec_bs >= cfg.enter_no_spec_bs:
118	        logger.warning(
119	            "[spec-mode] leave_no_spec_bs(%d) >= enter_no_spec_bs(%d) disables hysteresis",
120	            cfg.leave_no_spec_bs, cfg.enter_no_spec_bs,
121	        )
122	    if cfg.leave_d7_bs <= cfg.enter_d7_bs:
123	        logger.warning(
124	            "[spec-mode] leave_d7_bs(%d) <= enter_d7_bs(%d) disables hysteresis",
125	            cfg.leave_d7_bs, cfg.enter_d7_bs,
126	        )
127	    for tag, topk, steps, dtn in (
128	        ("D5", cfg.d5_topk, cfg.d5_steps, cfg.d5_dtn),
129	        ("D7", cfg.d7_topk, cfg.d7_steps, cfg.d7_dtn),
130	    ):
131	        expected = 1 + topk * steps
132	        if dtn != expected:
133	            logger.warning(
134	                "[spec-mode] %s dtn=%d != 1+topk*steps=%d (chain verify expects equality)",
135	                tag, dtn, expected,
136	            )
137	
138	
139	class SpecModeSelector:
140	    """Pick spec mode for a decode batch based on running BS.
141	
142	    Hysteresis guards against prefill bursts re-entering NO_SPEC mid-bench;
143	    under monotonically-decreasing bs traffic, the path is effectively
144	    NO_SPEC -> MARS_D5 -> MARS_D7 with no backtracking.
145	    """
146	
147	    def __init__(self, config: SpecModeConfig):
148	        self.config = config
149	        self.current = SpecMode.MARS_D5  # initial default; first decode step overrides
150	
151	    def select(self, bs: int) -> SpecMode:
152	        cfg = self.config
153	        if not cfg.enabled:
154	            return SpecMode.MARS_D5
155	
156	        prev = self.current
157	        if prev == SpecMode.NO_SPEC:
158	            if bs <= cfg.leave_no_spec_bs:
159	                new = SpecMode.MARS_D7 if bs <= cfg.enter_d7_bs else SpecMode.MARS_D5
160	            else:
161	                new = SpecMode.NO_SPEC
162	        elif prev == SpecMode.MARS_D7:
163	            if bs >= cfg.enter_no_spec_bs:
164	                new = SpecMode.NO_SPEC
165	            elif bs >= cfg.leave_d7_bs:
166	                new = SpecMode.MARS_D5
167	            else:
168	                new = SpecMode.MARS_D7
169	        else:  # MARS_D5
170	            if bs >= cfg.enter_no_spec_bs:
171	                new = SpecMode.NO_SPEC
172	            elif bs <= cfg.enter_d7_bs:
173	                new = SpecMode.MARS_D7
174	            else:
175	                new = SpecMode.MARS_D5
176	
177	        if new != prev:
178	            logger.info("[spec-mode] %s -> %s (bs=%d)", prev.value, new.value, bs)
179	        self.current = new
180	        return new
181	
182	
183	def selector_from_env() -> SpecModeSelector:
184	    cfg = load_config()
185	    logger.info("[spec-mode] %s", cfg.summary())
186	    return SpecModeSelector(cfg)
187
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	import math
2	import os
3	from typing import Optional, Union
4	
5	import torch
6	import triton
7	import triton.language as tl
8	from einops import rearrange
9	
10	from sglang.srt.layers.attention.base_attn_backend import AttentionBackend
11	from sglang.srt.layers.attention.fla.chunk import chunk_gated_delta_rule
12	from sglang.srt.layers.attention.fla.chunk_delta_h import CHUNK_SIZE as FLA_CHUNK_SIZE
13	from sglang.srt.layers.attention.fla.fused_gdn_gating import fused_gdn_gating
14	from sglang.srt.layers.attention.fla.fused_recurrent import (
15	    fused_recurrent_gated_delta_rule_update,
16	)
17	from sglang.srt.layers.attention.fla.fused_sigmoid_gating_recurrent import (
18	    fused_sigmoid_gating_delta_rule_update,
19	)
20	from sglang.srt.layers.attention.fla.kda import (
21	    chunk_kda,
22	    fused_kda_gate,
23	    fused_recurrent_kda,
24	)
25	from sglang.srt.layers.attention.mamba.causal_conv1d_triton import (
26	    PAD_SLOT_ID,
27	    causal_conv1d_fn,
28	    causal_conv1d_update,
29	)
30	from sglang.srt.layers.attention.mamba.mamba import MambaMixer2
31	from sglang.srt.layers.attention.mamba.mamba2_metadata import (
32	    ForwardMetadata,
33	    Mamba2Metadata,
34	)
35	
36	# Import Simple GLA from fla if available
37	try:
38	    from fla.ops.simple_gla import chunk_simple_gla
39	    from fla.ops.simple_gla.fused_recurrent import fused_recurrent_simple_gla
40	    SIMPLE_GLA_AVAILABLE = True
41	except ImportError:
42	    SIMPLE_GLA_AVAILABLE = False
43	
44	from fla.ops.utils.op import exp as _fla_exp
45	
46	
47	# ── Fused recurrent kernel with intermediate state export ──────────
48	# Eliminates 3x kernel launch overhead in TARGET_VERIFY by processing
49	# all draft_token_num steps in a single kernel call while saving
50	# per-step state for verification rollback.
51	@triton.heuristics({
52	    'USE_INITIAL_STATE': lambda args: args['h0'] is not None,
53	    'IS_VARLEN': lambda args: args['cu_seqlens'] is not None,
54	})
55	@triton.jit(do_not_specialize=['B', 'T'])
56	def _fused_recurrent_gla_intermediate_kernel(
57	    q, k, v, g_gamma, o, h0,
58	    ht_all,  # (N, T_per_seq, H, K, V) — state after each step (writes via explicit strides)
59	    cu_seqlens, scale,
60	    retrieve_parent_token_ptr,
61	    B, T,
62	    q_stride_t,
63	    q_stride_h,
64	    k_stride_t,
65	    k_stride_h,
66	    v_stride_t,
67	    v_stride_h,
68	    o_stride_nk,
69	    o_stride_t,
70	    o_stride_h,
71	    h0_stride_n,
72	    h0_stride_h,
73	    ht_stride_n,
74	    ht_stride_t,
75	    ht_stride_h,
76	    stride_retrieve_parent_token_seq,
77	    stride_retrieve_parent_token_token,
78	    NP2_T: tl.constexpr,
79	    H: tl.constexpr,
80	    K: tl.constexpr,
81	    V: tl.constexpr,
82	    BK: tl.constexpr,
83	    BV: tl.constexpr,
84	    USE_INITIAL_STATE: tl.constexpr,
85	    IS_VARLEN: tl.constexpr,
86	    HAS_EAGLE_TREE_CUSTOM_ATTN_MASK: tl.constexpr,
87	):
88	    i_v, i_k, i_nh = tl.program_id(0).to(tl.int64), tl.program_id(1).to(tl.int64), tl.program_id(2).to(tl.int64)
89	    i_n, i_h = i_nh // H, i_nh % H
90	
91	    seq_len = T
92	    if IS_VARLEN:
93	        bos = tl.load(cu_seqlens + i_n).to(tl.int64)
94	        eos = tl.load(cu_seqlens + i_n + 1).to(tl.int64)
95	        seq_len = eos - bos
96	    else:
97	        bos = i_n * T
98	        eos = i_n * T + T
99	
100	    o_k = i_k * BK + tl.arange(0, BK)
```

> TOOL

tool_use Bash
```json
{
  "command": "git log --oneline --all --grep=\"eagle\" -i --since=\"2024-01-01\" --format=\"%h %s\" | head -80",
  "description": "Get eagle commits with full messages"
}
```

> TOOL

tool_result Bash
```
87a8bb1 perf(eagle/dynamic): four small accelerations on the spec-decode hot path
61e4904 fix(metrics/demo-sala): NO_SPEC accept stats, dynamic dtn denominator, v3 draft, env align
06ed8e0 revert(eagle/dynamic): roll back mamba pool split
e291467 fix(eagle/dynamic): KV pool reclaim, per-mode mars theta, crash fixes
20cc58a perf(eagle/dynamic): kill three hot-path wastes in spec decode
b7a839e feat(eagle): dynamic spec mode (NO_SPEC / D5 / D7) by running batch size
cc9943b docs: restructure and merge eagle docs — trim stale files, consolidate surveys
4c0005c docs: multi-doc audit — correct b12x/MARS/rope_theta status and cross-link
c783ba8 docs(eagle/mars): correct theta to 0.85 (was mistakenly recorded as 0.8)
ca22a40 docs(eagle/mars): record theta=0.8 initial validation result
8f1af57 feat(eagle): implement MARS verify + sync MARS .so to demo-sala
7cf3b63 Revert "feat(eagle): two-phase TARGET_VERIFY with shared-buffer fix"
9dabf09 feat(eagle): two-phase TARGET_VERIFY with shared-buffer fix
a8b22ae revert(demo-sala): roll back to 9a7e04c cu13 baseline
0e768a3 chore(env+eval+meta): start_eagle defaults, prepare_env tweaks, CLAUDE/AGENTS align
081559b docs: marlin-tuning + collapse + training-v3 + nvfp4-kv + infllmv2 fix + upstream survey
da18187 feat(eagle): v3 training rewrite + pipeline reorganization
1608d18 fix(sgl-srt): spec-v1 correctness + profile gating + NVFP4 lm_head pipeline
22b2bf7 chore: track eagle draft weights with git-lfs
51ca6a8 fix(demo-sala): drop stale MARLIN_DECODE_THRESHOLD, add CUTE_DSL_CACHE_DIR
b3f9687 feat(b12x): 2-tier dispatch full-M + eagle_fc shape + dispatch trace
cd480ca docs(runtime): §7/§8/§9 memcpy attribution + §10 profiling methodology
59c126a eagle(v2): data pipeline + training rewrite (BS=8, fresh init, 1500 warmup)
230b381 docs: rewrite CLAUDE.md + trim AGENTS.md + align start_eagle.sh
bf55703 docs: restructure — rename, merge, split, update
91b0dd2 chore: purge obsolete — PLAN.md, v1 draft, superpowers/, debug archives
e36cefc feat: include eagle v2 draft weights
5c5335f feat: package eagle v2 demo-sala defaults
8017c1d fix: add tree-aware eagle dtn5 verify
0845f7b fix: stabilize eagle dtn2 replay path
9c6996a docs: EAGLE-3 数据采集 v2 设计 spec
9225f46 feat: intermediate_ssm direct-write + fused sparse metadata + profiling framework
617d6e5 feat: record triton eagle path and pin current draft model
6ba52a7 feat: record triton eagle path and pin current draft model
f7faed5 fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards
2b36ae2 fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards
a25e93d docs: update CLAUDE.md and PLAN.md for EAGLE-3 fused GLA
462414b docs: update CLAUDE.md and PLAN.md for EAGLE-3 fused GLA
da4309b feat: EAGLE-3 speculative decoding with fused GLA kernel
0843656 feat: EAGLE-3 speculative decoding with fused GLA kernel
351e77e chore: cleanup dead files, one-off scripts, update .gitignore
3ffeed9 chore: cleanup dead files, one-off scripts, update .gitignore
60474e8 eagle: implement STE-QAT FP4 native training + NVFP4 export pipeline
1f702ee eagle: implement STE-QAT FP4 native training + NVFP4 export pipeline
1267775 eagle: add Phase 0 baselines, Phase 2 kernel benchmarks, and plan
38ce7ea eagle: add Phase 0 baselines, Phase 2 kernel benchmarks, and plan
af38f7c docs: comprehensive cleanup — update CLAUDE.md, consolidate docs, add AGENTS.md
20ea7ec docs: comprehensive cleanup — update CLAUDE.md, consolidate docs, add AGENTS.md
ab4a619 fix: EAGLE-3 MiniCPM-SALA compatibility
8bc05a3 fix: EAGLE-3 MiniCPM-SALA compatibility
c6b7991 feat: Medusa speculative decoding integration (S1 -12%, S8 -12.5%)
3de4d05 feat: Medusa speculative decoding integration (S1 -12%, S8 -12.5%)
b478fcf feat: add EAGLE-3 speculative decoding for MiniCPM-SALA
057c168 feat: add EAGLE-3 speculative decoding for MiniCPM-SALA
```

> TOOL

tool_use Bash
```json
{
  "command": "git log --oneline --all --grep=\"dynamic\" -i --since=\"2025-01-01\" --format=\"%h %s\" | head -20",
  "description": "Get dynamic spec mode commits"
}
```

> TOOL

tool_result Bash
```
87a8bb1 perf(eagle/dynamic): four small accelerations on the spec-decode hot path
61e4904 fix(metrics/demo-sala): NO_SPEC accept stats, dynamic dtn denominator, v3 draft, env align
06ed8e0 revert(eagle/dynamic): roll back mamba pool split
e291467 fix(eagle/dynamic): KV pool reclaim, per-mode mars theta, crash fixes
20cc58a perf(eagle/dynamic): kill three hot-path wastes in spec decode
b7a839e feat(eagle): dynamic spec mode (NO_SPEC / D5 / D7) by running batch size
```

> DEVELOPER

你在 /user_4813494d/openbmb 工作区，这是一个 SOAR 2026 LLM 推理优化比赛仓库，优化 MiniCPM-SALA 模型推理。请深入调查除 EAGLE speculative decoding 和量化之外的所有性能优化工作。

重点读取：
1. docs/prefill.md
2. docs/prefill-accel-phase1.md（如果存在）
3. docs/prefill-accel-survey.md（如果存在）
4. docs/runtime.md
5. docs/infllmv2-blockmask-fix.md
6. docs/cuda13-upgrade.md（关注性能影响部分）
7. bench/mini_bench.sh
8. git log 中所有 perf、prefill、runtime、infllmv2 相关提交

请特别关注：
- InfLLM-v2 稀疏注意力的实现和优化（blockmask fix 解决了什么）
- 长上下文 prefill 的热点在哪里，做了什么优化
- plan_info reuse 优化的内容
- decode 期的算子优化清单（已落地的和负结果的）
- MiniCPM-SALA 模型架构特殊性（8 standard + 24 GLA 混合）对优化的影响
- 整个工作的 end-to-end 速度收益（能找到多少数字）
- cu13 升级带来了什么性能提升

请给出详细技术摘要，包括具体数字和架构特殊性分析。

> AGENT

现在我来搜索与量化相关的源文件和 git log。

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization -name \"*.py\" | head -20",
  "description": "List quantization-related Python files"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/__init__.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/auto_round.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/awq.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/awq_triton.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/base_config.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/blockwise_int8.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/fp8.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/fp8_kernel.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/fp8_utils.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/fpgemm_fp8.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/gguf.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/gptq.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/int8_kernel.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/int8_utils.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/kv_cache.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/kvfp4_tensor.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/marlin_utils_fp8.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/moe_wna16.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/mxfp4.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/mxfp4_tensor.py
```

> TOOL

tool_use Bash
```json
{
  "command": "git log --oneline --all --grep=\"b12x\\|marlin\\|NVFP4\\|quant\\|FourOverSix\\|scale.*bug\\|kv.*cache.*fp4\\|dispatch\\|kernel\" -i | head -60",
  "description": "Search git log for quantization-related commits"
}
```

> TOOL

tool_result Bash
```
87a8bb1 perf(eagle/dynamic): four small accelerations on the spec-decode hot path
61e4904 fix(metrics/demo-sala): NO_SPEC accept stats, dynamic dtn denominator, v3 draft, env align
06ed8e0 revert(eagle/dynamic): roll back mamba pool split
e291467 fix(eagle/dynamic): KV pool reclaim, per-mode mars theta, crash fixes
20cc58a perf(eagle/dynamic): kill three hot-path wastes in spec decode
b7a839e feat(eagle): dynamic spec mode (NO_SPEC / D5 / D7) by running batch size
cc9943b docs: restructure and merge eagle docs — trim stale files, consolidate surveys
4c0005c docs: multi-doc audit — correct b12x/MARS/rope_theta status and cross-link
ca22a40 docs(eagle/mars): record theta=0.8 initial validation result
8f1af57 feat(eagle): implement MARS verify + sync MARS .so to demo-sala
f0e6a61 chore(demo-sala/env): align prepare_env.sh to main
a8b22ae revert(demo-sala): roll back to 9a7e04c cu13 baseline
61213bf chore(demo-sala): drop legacy duplicates, add tuning + verify helpers
0e768a3 chore(env+eval+meta): start_eagle defaults, prepare_env tweaks, CLAUDE/AGENTS align
081559b docs: marlin-tuning + collapse + training-v3 + nvfp4-kv + infllmv2 fix + upstream survey
5b1c851 chore(bench): reorganize into kernels/{minicpm,marlin,fp4,prefill,...}; add microbenches
da18187 feat(eagle): v3 training rewrite + pipeline reorganization
1608d18 fix(sgl-srt): spec-v1 correctness + profile gating + NVFP4 lm_head pipeline
5552a23 perf: tune no-spec decode kernels
e9bfcb0 feat(probe-sala): sync sglang to latest + b12x readiness check
51ca6a8 fix(demo-sala): drop stale MARLIN_DECODE_THRESHOLD, add CUTE_DSL_CACHE_DIR
d19e4f2 perf: strip dispatch trace + hot-path cleanup
b3f9687 feat(b12x): 2-tier dispatch full-M + eagle_fc shape + dispatch trace
c3effe9 docs(runtime): §10.B 深挖 — 17.7% idle 拆分，CPU 侧真实 ROI 硬顶从 9.6% 下修到 5.5%
d7e5b52 probe-sala: torchao+xgrammar wheels + exit 1 also on all-pass path
4f8fc05 bench: cu13/sm120 kernel microbenches + b12x CuTe-DSL backend exploration
9a7e04c feat(probe-sala): full cu12→cu13 upgrade pipeline + BOS wheels offline install
bf55703 docs: restructure — rename, merge, split, update
9225f46 feat: intermediate_ssm direct-write + fused sparse metadata + profiling framework
f7faed5 fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards
2b36ae2 fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards
da4309b feat: EAGLE-3 speculative decoding with fused GLA kernel
0843656 feat: EAGLE-3 speculative decoding with fused GLA kernel
351e77e chore: cleanup dead files, one-off scripts, update .gitignore
3ffeed9 chore: cleanup dead files, one-off scripts, update .gitignore
460f3f2 plan: update Phase 2 checklist — STE-QAT + NVFP4 export implemented
373dc6d plan: update Phase 2 checklist — STE-QAT + NVFP4 export implemented
60474e8 eagle: implement STE-QAT FP4 native training + NVFP4 export pipeline
1f702ee eagle: implement STE-QAT FP4 native training + NVFP4 export pipeline
1267775 eagle: add Phase 0 baselines, Phase 2 kernel benchmarks, and plan
38ce7ea eagle: add Phase 0 baselines, Phase 2 kernel benchmarks, and plan
af38f7c docs: comprehensive cleanup — update CLAUDE.md, consolidate docs, add AGENTS.md
20ea7ec docs: comprehensive cleanup — update CLAUDE.md, consolidate docs, add AGENTS.md
f359853 probe-sala: fix empty responses via FlashInfer/cuDNN upgrade + full self-eval config
c54c473 probe-sala: fix empty responses via FlashInfer/cuDNN upgrade + full self-eval config
ab4a619 fix: EAGLE-3 MiniCPM-SALA compatibility
8bc05a3 fix: EAGLE-3 MiniCPM-SALA compatibility
ed3ec68 clean: restore demo-sala from tarball + MedusaBlock auto-detect
c3e99f4 clean: restore demo-sala from tarball + MedusaBlock auto-detect
c6b7991 feat: Medusa speculative decoding integration (S1 -12%, S8 -12.5%)
3de4d05 feat: Medusa speculative decoding integration (S1 -12%, S8 -12.5%)
47a054c feat: Medusa speculative decoding – data collection, training pipeline, profiling
2bde847 feat: Medusa speculative decoding – data collection, training pipeline, profiling
139652c perf: GPTQ quantization + operator optimizations for inference throughput
fc3a920 perf: GPTQ quantization + operator optimizations for inference throughput
9692e9e feat: GPTQ+NVFP4 quantization pipeline (80.27% accuracy, +0.54 vs AWQ-lite)
5a32cbd feat: GPTQ+NVFP4 quantization pipeline (80.27% accuracy, +0.54 vs AWQ-lite)
f4c53be revert: remove SimpleGLA BK=128 kernel (CUDA graph 1.65x slower)
f734a5e revert: remove SimpleGLA BK=128 kernel (CUDA graph 1.65x slower)
2162051 perf: fuse residual+scale_depth into single torch.add kernel
```

> AGENT

我将系统地调查此仓库中的所有性能优化工作。我将首先探索仓库结构并同时读取关键文档。

> TOOL

tool_use Bash
```json
{
  "command": "ls /user_4813494d/openbmb/docs/",
  "description": "List docs directory"
}
```

> TOOL

tool_result Bash
```
README.md
cuda13-upgrade.md
eagle
infllmv2-blockmask-fix.md
kernels-sm120.md
marlin-tuning.md
nvfp4-kv-investigation.md
prefill-accel-phase1.md
prefill-accel-survey.md
prefill.md
quantization.md
runtime.md
sglang-upstream-survey.md
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /user_4813494d/openbmb/bench/",
  "description": "List bench directory"
}
```

> TOOL

tool_result Bash
```
README.md
__pycache__
archive
autotune_fp4
b12x
bench.py
bench_compress_k_autotune.py
bench_cublas_vs_cutlass_nvfp4.py
bench_fp4_all_backends.py
bench_fp4_cudnn_vs_cutlass.py
bench_fp4_cutlass_fine.py
bench_kernels_cu12_baseline.py
bench_kernels_cu13_baseline.py
bench_marlin_bandwidth.py
bench_marlin_vs_cutlass.py
bench_mlp_breakdown.py
bench_stage1_seqlen_k.py
build_sgl_kernel_cu13.sh
data
eagle_accept_diff.py
eagle_accept_probe.py
eagle_collapse_analyze.py
eagle_collapse_probe.py
eagle_eval_analyze.py
eagle_eval_probe.py
infllmv2
kernels
kill_sglang.sh
mars_offline.py
mini_bench.sh
ncu_target_cutlass_nvfp4.py
prefill_bench_smax64.py
probe_fp4_peak.py
profile
profile_gla_custom_kernel.py
profile_gla_verify.py
pure_mma_peak
results
rope_theta_probe.py
sglang_0425_24_custom.jsonl
sglang_0425_64_custom.jsonl
sglang_0425_8_custom.jsonl
sglang_0426_24_custom.jsonl
sglang_0426_8_custom.jsonl
sglang_0428_24_custom.jsonl
sglang_0428_8_custom.jsonl
test_fused_vs_stepbystep.py
test_hybrid_offline.py
trigger_profile.sh
trtllm_vs_fa2_prefill_sweep.json
trtllm_vs_fa2_prefill_sweep.py
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt -name \"modelopt_quant.py\" -o -name \"marlin_utils_fp4.py\" -o -name \"b12x_fp4.py\" 2>/dev/null",
  "description": "Find key quantization source files"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/marlin_utils_fp4.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/b12x_fp4.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -maxdepth 2 -type f -name \"*.md\" | sort",
  "description": "Find all markdown files"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/.ipynb_checkpoints/HANDOVER-checkpoint.md
/user_4813494d/openbmb/.ipynb_checkpoints/PLAN-checkpoint.md
/user_4813494d/openbmb/.ipynb_checkpoints/eagle3_runtime_investigation-checkpoint.md
/user_4813494d/openbmb/.ipynb_checkpoints/fix-checkpoint.md
/user_4813494d/openbmb/.pytest_cache/README.md
/user_4813494d/openbmb/AGENTS.md
/user_4813494d/openbmb/CLAUDE.md
/user_4813494d/openbmb/bench/README.md
/user_4813494d/openbmb/demo-sala/README.md
/user_4813494d/openbmb/docs/README.md
/user_4813494d/openbmb/docs/cuda13-upgrade.md
/user_4813494d/openbmb/docs/infllmv2-blockmask-fix.md
/user_4813494d/openbmb/docs/kernels-sm120.md
/user_4813494d/openbmb/docs/marlin-tuning.md
/user_4813494d/openbmb/docs/nvfp4-kv-investigation.md
/user_4813494d/openbmb/docs/prefill-accel-phase1.md
/user_4813494d/openbmb/docs/prefill-accel-survey.md
/user_4813494d/openbmb/docs/prefill.md
/user_4813494d/openbmb/docs/quantization.md
/user_4813494d/openbmb/docs/runtime.md
/user_4813494d/openbmb/docs/sglang-upstream-survey.md
/user_4813494d/openbmb/eagle/README.md
/user_4813494d/openbmb/eagle3_runtime_investigation.md
/user_4813494d/openbmb/toolkit/README.md
/user_4813494d/openbmb/toolkit/README_EN.md
```

> TOOL

tool_use Bash
```json
{
  "command": "git log --oneline -80",
  "description": "Recent git log"
}
```

> TOOL

tool_result Bash
```
87a8bb1 perf(eagle/dynamic): four small accelerations on the spec-decode hot path
61e4904 fix(metrics/demo-sala): NO_SPEC accept stats, dynamic dtn denominator, v3 draft, env align
06ed8e0 revert(eagle/dynamic): roll back mamba pool split
e291467 fix(eagle/dynamic): KV pool reclaim, per-mode mars theta, crash fixes
20cc58a perf(eagle/dynamic): kill three hot-path wastes in spec decode
b7a839e feat(eagle): dynamic spec mode (NO_SPEC / D5 / D7) by running batch size
cc9943b docs: restructure and merge eagle docs — trim stale files, consolidate surveys
4c0005c docs: multi-doc audit — correct b12x/MARS/rope_theta status and cross-link
c783ba8 docs(eagle/mars): correct theta to 0.85 (was mistakenly recorded as 0.8)
ca22a40 docs(eagle/mars): record theta=0.8 initial validation result
8f1af57 feat(eagle): implement MARS verify + sync MARS .so to demo-sala
7cf3b63 Revert "feat(eagle): two-phase TARGET_VERIFY with shared-buffer fix"
9dabf09 feat(eagle): two-phase TARGET_VERIFY with shared-buffer fix
f0e6a61 chore(demo-sala/env): align prepare_env.sh to main
a8b22ae revert(demo-sala): roll back to 9a7e04c cu13 baseline
61213bf chore(demo-sala): drop legacy duplicates, add tuning + verify helpers
0e768a3 chore(env+eval+meta): start_eagle defaults, prepare_env tweaks, CLAUDE/AGENTS align
081559b docs: marlin-tuning + collapse + training-v3 + nvfp4-kv + infllmv2 fix + upstream survey
5b1c851 chore(bench): reorganize into kernels/{minicpm,marlin,fp4,prefill,...}; add microbenches
da18187 feat(eagle): v3 training rewrite + pipeline reorganization
1608d18 fix(sgl-srt): spec-v1 correctness + profile gating + NVFP4 lm_head pipeline
5552a23 perf: tune no-spec decode kernels
22b2bf7 chore: track eagle draft weights with git-lfs
5234ff4 chore: remove accidentally committed .venv from probe-sala
e9bfcb0 feat(probe-sala): sync sglang to latest + b12x readiness check
51ca6a8 fix(demo-sala): drop stale MARLIN_DECODE_THRESHOLD, add CUTE_DSL_CACHE_DIR
d19e4f2 perf: strip dispatch trace + hot-path cleanup
b3f9687 feat(b12x): 2-tier dispatch full-M + eagle_fc shape + dispatch trace
c3effe9 docs(runtime): §10.B 深挖 — 17.7% idle 拆分，CPU 侧真实 ROI 硬顶从 9.6% 下修到 5.5%
cd480ca docs(runtime): §7/§8/§9 memcpy attribution + §10 profiling methodology
38ab07b fix: harden spec v2 overlap path
d7e5b52 probe-sala: torchao+xgrammar wheels + exit 1 also on all-pass path
ac03fe5 eval: restore live_dashboard.py — tail-f incremental predictions viewer
59c126a eagle(v2): data pipeline + training rewrite (BS=8, fresh init, 1500 warmup)
4f8fc05 bench: cu13/sm120 kernel microbenches + b12x CuTe-DSL backend exploration
9a7e04c feat(probe-sala): full cu12→cu13 upgrade pipeline + BOS wheels offline install
230b381 docs: rewrite CLAUDE.md + trim AGENTS.md + align start_eagle.sh
bf55703 docs: restructure — rename, merge, split, update
91b0dd2 chore: purge obsolete — PLAN.md, v1 draft, superpowers/, debug archives
b4d387a perf(prefill): cross-chunk plan_info reuse + smax64 bench
1f265fe perf(prefill): reuse flashinfer plan across 8 standard layers
e36cefc feat: include eagle v2 draft weights
5c5335f feat: package eagle v2 demo-sala defaults
8017c1d fix: add tree-aware eagle dtn5 verify
0845f7b fix: stabilize eagle dtn2 replay path
9c6996a docs: EAGLE-3 数据采集 v2 设计 spec
475ddd5 eval_ood: step-0 only, full-length (no SEQ_LEN truncation)
9225f46 feat: intermediate_ssm direct-write + fused sparse metadata + profiling framework
89eb9a6 feat(gla): Plan A scaffolding — per-branch tree verify buffers
6ba52a7 feat: record triton eagle path and pin current draft model
2b36ae2 fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards
462414b docs: update CLAUDE.md and PLAN.md for EAGLE-3 fused GLA
0843656 feat: EAGLE-3 speculative decoding with fused GLA kernel
3ffeed9 chore: cleanup dead files, one-off scripts, update .gitignore
dd78dae chore: rename PLANtodo.md → PLAN.md
373dc6d plan: update Phase 2 checklist — STE-QAT + NVFP4 export implemented
1f702ee eagle: implement STE-QAT FP4 native training + NVFP4 export pipeline
38ce7ea eagle: add Phase 0 baselines, Phase 2 kernel benchmarks, and plan
5dfcff9 chore: extend .gitignore for calibration data, bench results, probe artifacts
af38f7c docs: comprehensive cleanup — update CLAUDE.md, consolidate docs, add AGENTS.md
f359853 probe-sala: fix empty responses via FlashInfer/cuDNN upgrade + full self-eval config
ab4a619 fix: EAGLE-3 MiniCPM-SALA compatibility
6087c93 revert: undo fc3a920 operator optimizations for precision A/B test
f42aca0 fix: deterministic decode/verify via num_splits=1 + eager TARGET_VERIFY fallback
6484c43 clean: reset demo-sala to 5f2a290 + MedusaBlock auto-detect
ed3ec68 clean: restore demo-sala from tarball + MedusaBlock auto-detect
150119c fix: Medusa spec decode CUDA graph buffer overflow + vectorized verify
c6b7991 feat: Medusa speculative decoding integration (S1 -12%, S8 -12.5%)
47a054c feat: Medusa speculative decoding – data collection, training pipeline, profiling
b478fcf feat: add EAGLE-3 speculative decoding for MiniCPM-SALA
e8b28e1 fix: gitignore /models/ user_4813494d-only, add cutlass and sglang models ignore
139652c perf: GPTQ quantization + operator optimizations for inference throughput
9692e9e feat: GPTQ+NVFP4 quantization pipeline (80.27% accuracy, +0.54 vs AWQ-lite)
f4c53be revert: remove SimpleGLA BK=128 kernel (CUDA graph 1.65x slower)
2162051 perf: fuse residual+scale_depth into single torch.add kernel
f4bea68 perf: eliminate redundant F32 dtype cast in RoPE for all 32 layers
6cd79ae feat: hybrid Marlin/CUTLASS dispatch + 45K quant + submission cleanup
7f05a8e docs: merge 4 docs into soar-competition.md + technical-notes.md
1c18765 chore: clean up project structure, remove obsolete files, update docs
99e195e feat: NVFP4 Marlin fallback path + sgl-kernel rebuild pipeline + probe-sala
```

> AGENT

现在让我读取关键源文件的更具体部分——特别是 MARS 验证和 `eagle_info.py` 中 tree-aware verify 的部分。

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py",
  "limit": 80,
  "offset": 380
}
```

> TOOL

tool_result Read
```
380	                topk=self.topk,
381	                top2_token=top2_token,
382	                top2_ratio=top2_ratio,
383	                mars_theta=mars_theta,
384	            )
385	
386	        else:
387	            # apply temperature and get target probs
388	            expanded_temperature = torch.repeat_interleave(
389	                sampling_info.temperatures, self.draft_token_num, dim=0
390	            )  # (bs * draft_token_num, 1)
391	
392	            target_probs = F.softmax(
393	                logits_output.next_token_logits / expanded_temperature, dim=-1
394	            )  # (bs * draft_token_num, vocab_size)
395	            target_probs = top_k_renorm_prob(
396	                target_probs,
397	                torch.repeat_interleave(
398	                    sampling_info.top_ks, self.draft_token_num, dim=0
399	                ),
400	            )  # (bs * draft_token_num, vocab_size)
401	            if not torch.all(sampling_info.top_ps == 1.0):
402	                target_probs = top_p_renorm_prob(
403	                    target_probs,
404	                    torch.repeat_interleave(
405	                        sampling_info.top_ps, self.draft_token_num, dim=0
406	                    ),
407	                )
408	            target_probs = target_probs.reshape(bs, self.draft_token_num, -1)
409	
410	            draft_probs = torch.zeros(
411	                target_probs.shape, dtype=torch.float32, device=batch.device
412	            )
413	
414	            # coins for rejection sampling
415	            coins = torch.rand_like(
416	                candidates, dtype=torch.float32, device=batch.device
417	            )
418	            # coins for final sampling
419	            coins_for_final_sampling = torch.rand(
420	                (bs,), dtype=torch.float32, device=batch.device
421	            )
422	            tree_speculative_sampling_target_only(
423	                predicts=predict,  # mutable
424	                accept_index=accept_index,  # mutable
425	                accept_token_num=accept_length,  # mutable
426	                candidates=candidates,
427	                retrive_index=self.retrive_index,
428	                [REDACTED],
429	                retrive_next_sibling=self.retrive_next_sibling,
430	                uniform_samples=coins,
431	                uniform_samples_for_final_sampling=coins_for_final_sampling,
432	                target_probs=target_probs,
433	                draft_probs=draft_probs,
434	                threshold_single=get_global_server_args().speculative_accept_threshold_single,
435	                threshold_acc=get_global_server_args().speculative_accept_threshold_acc,
436	                deterministic=True,
437	            )
438	
439	        if SIMULATE_ACC_LEN > 0.0:
440	            # Do simulation
441	            accept_index = generate_simulated_accept_index(
442	                accept_index=accept_index,
443	                predict=predict,  # mutable
444	                accept_length=accept_length,  # mutable
445	                bs=bs,
446	                spec_steps=self.spec_steps,
447	            )
448	
449	        if _FORCE_NO_ACCEPT:
450	            # Profile hack: force all draft tokens rejected. Keep user_4813494d only.
451	            accept_index[:, 1:] = -1
452	            accept_length.zero_()
453	
454	        if _EAGLE_TRACE_PATH:
455	            try:
456	                dtn = self.draft_token_num
457	                _tr_logits_v = logits_output.next_token_logits.view(bs, dtn, -1).float()
458	                _tr_top2_v, _tr_top2_i = torch.topk(_tr_logits_v, 2, dim=-1)
459	                _tr_top2_v_cpu = _tr_top2_v.cpu().tolist()
```

> AGENT

现在让我并行读取所有关键文档。

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/prefill.md"
}
```

> TOOL

tool_result Read
```
1	# 长上下文 Prefill 热点图与优化记录
2	
3	**场景**：128K prompt prefill（MiniCPM-SALA-NVFP4，`--chunked-prefill-size 8192`，`--dense-as-sparse`，`minicpm_flashinfer`）
4	
5	## 1. 热点分层（Chunk 1, token=8192, 插桩稍慢但比例可信）
6	
7	在三个模块加 `_profile_begin / _profile_end`（`torch.cuda.synchronize() + time.perf_counter()`）：
8	
9	- `models/minicpm.py` — `MiniCPMDecoderLayer.forward` 按层分桶（`attn_standard_ms` / `attn_gla_ms` / `mlp_ms` / `ln_pre_ms` / `ln_post_ms` / `residual_ms`）
10	- `layers/attention/minicpm_sparse_utils.py` — `infllmv2_attn_stage1`、`max_pooling_1d_varlen`、`block_score.topk` 各一桶
11	- `layers/attention/minicpm_backend.py` — `get_compress_k_v2` / `sparse_get_topk_impl` / `attention_kernel.forward`（`extend_sparse_fa_ms`）
12	
13	触发：`SGLANG_MINICPM_PROFILE=1 SGLANG_MINICPM_PROFILE_INTERVAL=32`。
14	
15	**每层占比**（归一化）：
16	
17	| 阶段 | 占比 |
18	|---|---|
19	| **extend_sparse_fa**（8 std layer × sparse FA） | ~26% |
20	| **mlp**（32 层 MLP） | ~16% |
21	| **attn_gla**（24 层 Lightning Attention） | ~11% |
22	| attn_standard 其他（QKV/OUT proj + RoPE） | ~5% |
23	| sparse_topk 合计（stage1 + pool + topk_select） | ~5% |
24	| compress_k | <1% |
25	| ln + residual + embed + final_norm | ~2% |
26	
27	`attn_standard` 内部 sparse FA 占 73%，sparse_topk 13%，QKV/OUT proj + RoPE 14%，compress_k < 1%。
28	
29	## 2. 周期性 2× 慢 chunk — 已定位根因
30	
31	每 3 chunk 出现一次慢 chunk，`extend_sparse_fa` 和 `attn_standard` 翻一倍，差值稳定在一次 sparse FA 的时间。
32	
33	### 定位方法
34	
35	在 `FlashInferKernel.forward` 把三步独立分桶：
36	
37	- `fi_convert_ms` — `convert_sparse_page_table_to_flashinfer`
38	- `fi_begin_forward_ms` — `wrapper.begin_forward(...)`（= flashinfer `plan()`）
39	- `fi_decode_fwd_ms` — `wrapper.forward(...)`（实际 FA kernel）
40	
41	### 结论
42	
43	慢点在 `wrapper.begin_forward` → flashinfer `plan()`。每个慢 chunk 恰有一个 standard layer 的 `bf` 暴涨（`cv` / `fw` 完全不变）。慢 layer 在 {L9, L16, L17, L22, L29, L30} 间无规律轮换。
44	
45	### plan() 内部 nsys 抓取
46	
47	用 `nsys profile -t cuda,nvtx --capture-range=cudaProfilerApi` + `SGLANG_MINICPM_CUDA_PROFILER=1` + `SGLANG_MINICPM_NVTX=1`（`MiniCPMModel.forward` 加 `cudaProfilerStart/Stop` 控制窗口）：
48	
49	**Normal layer 窗口**：bf 起点 → end 之间有 ~23 ms 的 **CPU 空白**（零 kernel / API / memcpy），接着一个 256KB DtoH 把 plan 输出拷回 CPU。
50	
51	**Slow layer 窗口**：bf 起点先有一个 HtoD 异常慢（64KB 被阻塞 10× 以上），接着跑一串 GPU 辅助 kernel（normal 窗口没有，`elementwise / cumsum / reduce / scan / flatten_and_fill`），然后 ~350 ms 的 CPU 空白，最后 plan 输出 DtoH。
52	
53	### 根因
54	
55	1. **plan() baseline = 纯 CPU 时间**：不是 GPU/driver 慢，而是 flashinfer `_cached_module.plan(...)` C++ 函数在做 work-split 决策的 CPU 计算。
56	2. **慢 outlier 也是纯 CPU**：同一 CPU 计算偶尔暴涨 ~15×。开头异常慢 HtoD + plan 内额外 GPU 辅助 kernel 说明 CPU 这次走了"重计算路径"，memcpy 被什么阻塞（ioctl / allocator / page fault）。
57	3. **与 allocator 抖动无关**：nsys 窗口内无 cudaMalloc/cudaFree（只在 init 阶段），所以 buffer reuse 实验没用。
58	
59	## 3. 修复：layer 间 plan 复用（commit 259b82d）
60	
61	**观察**：同一个 forward 的 8 个 standard layer 的 KV layout 完全一致（`max_kv_len` / `bs` / `page_size` / `heads` / `dtypes` 相同），只有 `_paged_kv_indices` 内容变化。flashinfer `plan()` 的 work split 完全由前面这些量决定 → 8 层可共用一次 plan。
62	
63	**实现**（`FlashInferKernel.__init__` + `forward`）：
64	
65	- 新增 `_plan_cache_key` / `_plan_last_layer_id`
66	- 非 CUDA-graph + sparse decode wrapper 分支里，判定 `layer_id > _plan_last_layer_id` 且 cache_key 匹配 → 跳过 `wrapper.begin_forward`，直接 `wrapper._paged_kv_indices_buf = kv_indices`
67	- 失效：下一次 forward 从 L0 开始 `0 > 31 == False` 自动触发 replan
68	- env: `SGLANG_MINICPM_PLAN_CACHE=0` 可关
69	
70	**验证**：`per-chunk FA log` 显示 7/8 层 `bf=0.0 ms`，L0 正常 cache-miss replan。
71	
72	**Decode 物理隔离**：plan cache 只作用于 non-CUDA-graph + sparse decode wrapper 路径。Decode 走 CUDA graph 分支（`params.decode_wrapper is not None`），cache on/off 的 decode TPS 在噪声级别一致。
73	
74	## 4. 修复：chunk 间 plan 复用（commit e99478e）
75	
76	**动机**：layer-cache 后每 chunk L0 仍 replan（基线开销中的主要残余）。InfLLM-v2 在 seq_len 超过 topk 阈值后 `kv_indptr` / `kv_last_page_len` / `bs` / `page_size` 都固定，只有 `kv_indices` 内容随 chunk 推进变化 → 跨 chunk 也可复用。
77	
78	**实现**：cache 新增 `_plan_cached_indptr_bytes` / `_plan_cached_lpl_bytes`（CPU-side 字节副本）。layer 级判定失败（forward 边界 / L0）后做 CPU byte compare：`kv_indptr` + `kv_last_page_len` 与缓存一致 → 复用 plan；否则 replan + 刷新缓存。bs ≤ 16 时两个张量 total ≤ ~256 B，`.cpu().numpy().tobytes()` 开销可忽略。
79	
80	**验证**：多数 chunk cross-hit（cross-hit 路径 bf ~0.1 ms），仅早期 seq_len 未达 full topk 阈值的 chunk 仍 replan。
81	
82	**纯 prefill 并发 A/B**（`bench/prefill_bench_smax64.py`，64 个 smax 样本并发 `max_tokens=1`）：plan cache 在长序列并发场景稳定省下相当一部分纯 prefill 时间，`p50` / `max` latency 同步下降。
83	
84	## 5. 已撤回的尝试
85	
86	- **复用 `kv_indptr` / `kv_indices` / `kv_last_page_len` buffer**：改 `FlashInferKernel` 预分配 3 个 int32 buffer + view 复用，慢 layer 的频率 / 幅度都没变化 → 确认 stall 不是 allocator 抖动造成。
87	- **CUDA graph 包 sparse prefill 的 begin_forward + forward**：plan 是 eager mode C++，graph 捕不了。
88	
89	## 6. 仍然可挖的点
90	
91	- **L0 残留 replan**：chunk 1 因 `kv_indptr` 结构变化仍 replan。可 pad 到 full topk，或 L0 20ms 转 CUDA kernel overlap。
92	- **`plan()` 偶发 spike**：单 chunk 概率、非 layer 数线性，可能源自 flashinfer 内部 autotune 分配，待观察。
93	- **自写 sparse decode kernel 绕过 flashinfer plan()**：彻底解决但风险高，延后。
94	- **FlashPrefill α-threshold 替代固定 topk sparse**：需 accuracy 验证，当前 `topk=96=64+32 local` 固定稀疏率；α-threshold 动态稀疏率潜在收益 1.5-2×，代价是训练-推理稀疏率 mismatch 风险。
95	- **stage2 FA kernel autotune**：借 FlashPrefill 的 (Q_TILE × K_TILE) × (warps × stages) 空间重调，低风险 ~1.2×。
96	
97	## 7. profile 基础设施
98	
99	保留但默认关闭的 instrumentation（靠 env var 打开）：
100	
101	| env var | 作用 |
102	|---|---|
103	| `SGLANG_MINICPM_PROFILE=1` | 启用全部 `_profile_begin/end` 桶，打印 `[minicpm-prefill-fwd]` / `[minicpm-prefill-fa-per-layer]` |
104	| `SGLANG_MINICPM_PROFILE_INTERVAL=N` | 每 N 次 forward 打一次 |
105	| `SGLANG_MINICPM_NVTX=1` | 加 NVTX range 方便 nsys 对齐 |
106	| `SGLANG_MINICPM_CUDA_PROFILER=1` | 在 `MiniCPMModel.forward` 控制 `cudaProfilerStart/Stop` 抓窗口 trace |
107	| `SGLANG_MINICPM_PLAN_CACHE=0` | 关 plan 复用（验证退化用） |
108
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/prefill-accel-phase1.md"
}
```

> TOOL

tool_result Read
```
1	# Prefill 加速调研 Phase 1 综述
2	
3	**时间**：2026-04-28  
4	**场景**：RTX 6000D (sm_120)，MiniCPM-SALA-NVFP4，128K prompt，`--chunked-prefill-size 8192`，`--dense-as-sparse`（**必须开，否则精度问题**）
5	
6	---
7	
8	## 0. 场景约束（先读，避免走弯路）
9	
10	### 0.1 `--dense-as-sparse` 强制约束
11	
12	`--dense-as-sparse=True` 是生产必须项，不可关闭。效果：**所有 8 个 standard attention 层无论序列长度一律走 InfLLM-v2 稀疏路径**，不存在"短序列走 dense FA"的分支。
13	
14	直接推论：
15	- cuDNN SDPA、FA2 原生 dense 路径优化对我们**完全无效**（代码分支不存在）
16	- "dense attention" 方向的所有调研结论作废
17	
18	### 0.2 阶段 2 必须 profile 重跑
19	
20	现有 profiling（`docs/prefill.md §1`）在 `--dense-as-sparse` 开启状态下测量，数字可信：
21	
22	| 阶段 | 占比 | 绝对时间估算 |
23	|---|---|---|
24	| **extend_sparse_fa**（8 std layer × sparse FA stage2） | ~26% | ★ 最大单块 |
25	| **mlp**（32 层 MLP，M=8192 NVFP4 GEMM） | ~16% | |
26	| **attn_gla**（24 层 Lightning Attention） | ~11% | |
27	| attn_standard QKV/OUT proj + RoPE | ~5% | |
28	| sparse_topk（stage1 + pool + topk_select） | ~5% | |
29	| compress_k | <1% | |
30	| ln + residual + embed + final_norm | ~2% | |
31	
32	**不在热点的方向可以排除**：compress_k <1%，layernorm/residual ~2%，均不值得投入。
33	
34	### 0.3 硬件约束速查
35	
36	| 属性 | 值 |
37	|---|---|
38	| 架构 | sm_120 (Blackwell, GB202) |
39	| SMEM/SM | ~96 KB（实测，CUTLASS sm_120 限制） |
40	| TMEM | **不存在**（GB202 无，GB100 专属）|
41	| HBM BW | ~1400 GB/s |
42	| NVFP4 MMA peak | ~1467 TFLOPS |
43	| FA4 / FA3 | **不可用**（TMEM 依赖） |
44	
45	---
46	
47	## 1. 关键发现：stage2 sparse FA 是内存带宽瓶颈
48	
49	这是本轮调研最重要的发现，**决定优化策略的方向**。
50	
51	### 算术强度分析
52	
53	Stage2 sparse FA（FlashInfer FA2+TC，varlen sparse，topk=96）的算术强度：
54	
55	```
56	topk=96 KV blocks, block_size=64, head_dim=128, BF16
57	每 query block:
58	  FLOPs = 2 × 96×64 × 128 × 2(QK+AV) ≈ 3.1M FLOP
59	  Bytes = 96×64×128×2(load K) + 96×64×128×2(load V) ≈ 3.9M bytes
60	算术强度 ≈ 0.78 FLOP/byte
61	```
62	
63	**ridge point ≈ 1467T / 1400G ≈ 1048 FLOP/byte**，实际强度 0.78 << 1048。
64	
65	**结论：stage2 sparse FA 是极度内存带宽受限操作，不是 TC 利用率问题。**
66	
67	优化策略的直接推论：
68	- 提升 TC 利用率（更大 tile、StreamK、更高 TFLOPS）对 stage2 **无效**
69	- 有效方向只有两类：**减少 HBM 流量**（更少 KV blocks）或**利用 HBM 内的 skip**（跳过零权重块）
70	
71	---
72	
73	## 2. 各优化方向评估
74	
75	### P0 — BLASST / Skip Softmax（最高优先级）
76	
77	**来源**：arXiv:2512.12087，NVIDIA TRT-LLM 已集成，FlashInfer PR in review  
78	**原理**：在 sparse FA stage2 内部，QK softmax 后权重为 0 的行（已被稀疏 topk 过滤的块）跳过 AV 乘积；对内存受限 kernel 等效减少 HBM 读取量  
79	**收益**：论文报告 ~1.4-1.5× stage2 加速（70% sparsity 典型值）  
80	**stage2 占 26% → e2e prefill 潜在 +10-13%**  
81	**代价**：training-free，无精度损失，只改 kernel  
82	**可行性**：
83	- FlashInfer 0.6.8.post1 **还未合入**，需要自行移植 PR diff 或直接用 infllm_v2 未来版本
84	- 核心变化是 `advance_to_next_do_not_attend_position` 逻辑，约 100-200 行 kernel 改动
85	- infllm_v2 的 `infllmv2_attn_varlen_func` 是否已内置 BLASST 需要检查源码
86	
87	**行动**：先检查 infllm_v2 包是否已含 BLASST；若无，从 FlashInfer PR 移植 skip-softmax patch 到 `minicpm_backend.py` 的 stage2 调用路径
88	
89	---
90	
91	### P1a — topk 96→64 精度实验
92	
93	**原理**：stage2 加载的 KV 块数从 96 → 64，HBM 流量直降 33%，stage2 时间理论 -25% 至 -30%  
94	**e2e 估算**：stage2 占 26%，潜在 +7-8%  
95	**代价**：可能影响生成精度（topk=96=64+32 local，32 是 local window，64 是 retrieved；减少到 64 等于完全砍 retrieved）  
96	**正确做法**：
97	- 实际应减 retrieved 部分：`topk_retrieved = 64→32`，local window 32 保持不变
98	- 用 benchmark eval 样本（deepresearch，长 context）测 accuracy delta
99	- 若 BLEU/ROUGE 无可测量下降（<1%），可合入
100	
101	**行动**：在 `minicpm_backend.py` 加 `SGLANG_INFLLM_TOPK` env var，跑 A/B
102	
103	---
104	
105	### P1b — SageAttention3 FP4 稀疏路径
106	
107	**来源**：NeurIPS 2025，RTX 5090 (=sm_120) 实测 ~3-5× vs FA2  
108	**原理**：用 NVFP4 MMA 做 attention，将 Q/K 量化到 FP4 做 QK，保 V 精度  
109	**HuggingFace wheel**：`pip install sageattention` 提供 sm_120 预编译包  
110	**关键不确定性**：
111	1. SageAttention3 的 sm_120 API 是否支持 **varlen sparse** 模式（infllm_v2 stage2 需要 sparse page table）
112	2. FP4 attention 对长 context 精度影响——Q/K FP4 量化在稀疏 topk 路径是否会导致 attention pattern 进一步偏移
113	3. 其 benchmark 在稠密 full-attention 上测，稀疏场景性能数字未知
114	
115	**行动**：安装 sageattention，检查是否有 `varlen_sparse` API；若有，在 128K 单样本上跑 correctness + latency 对比
116	
117	---
118	
119	### P2 — FLA 0.5.0 cherry-pick（GLA 加速）
120	
121	**来源**：FLA GitHub，两个 PR  
122	**PR #469**：移除 `simple_gla` 反向中不必要的 dg 计算（训练路径），推理无影响  
123	**PR #361**：`tl.exp2` 替代 `torch.exp`（更快的 Triton 指令），影响 `chunk_simple_gla` 推理 forward  
124	**收益估算**：PR #361 → 5-10% GLA kernel 加速，GLA 占 11% → e2e **+0.5-1%**  
125	**代价**：极低——cherry-pick 2-3 行 Triton kernel 改动到 `/opt/.../fla/` 包文件  
126	**依赖**：FLA 0.4.1 → 0.5.0 变更是否有其他 breaking change 需要检查  
127	
128	**行动**：diff FLA 0.4.1 vs 0.5.0 的 `chunk_simple_gla`，仅 cherry-pick PR #361 的 exp2 改动
129	
130	---
131	
132	### P3a — CUTLASS NVFP4 tile 扫描（§7.2，MLP GEMM M=8192）
133	
134	**来源**：`docs/kernels-sm120.md §7.2`，标注"未展开"  
135	**现状**：sgl-kernel 只 hard-code 2 个 sm_120 config（§4），M=8192 永远走 `256×128×128`  
136	**有效空间**：`{128,256}×{128,256}×{128}` + `(128,128,256)`，5 个有效 tile  
137	**估算**：MLP 占 16%，tile 调优收益 2-5% → e2e **+0.3-0.8%**  
138	**代价**：需要编译候选 kernel（`bench/autotune_fp4/autotune_kernel.cu`），模板已有  
139	**注意**：autotune cache（`mm_fp4_tune_sm120.json`）覆盖 flashinfer 的 6 tactic，但 sgl-kernel 的 `cutlass_scaled_fp4_mm` 不读这个 cache——两个路径独立
140	
141	**行动**：运行 `bench/autotune_fp4/build.sh` 编译 5 tile × 2 schedule，benchmark M=8192 gate_proj / down_proj
142	
143	---
144	
145	### P3b — MInference 动态稀疏
146	
147	**来源**：Microsoft，arXiv，已开源  
148	**原理**：在 prefill 时动态决定每个 attention head 的稀疏模式（A-shape / slash / dense），比 fixed topk 更 adaptive  
149	**与 InfLLM-v2 关系**：InfLLM-v2 已经是 fixed topk 稀疏——MInference 是替换 topk 选择策略，不是替换 stage2 kernel  
150	**风险**：改动 InfLLM-v2 稀疏选择逻辑，需要重新 calibrate attention pattern，accuracy 风险高  
151	**优先级**：P3（高工程风险，收益不确定，`dense-as-sparse` 约束下 calibration 更复杂）
152	
153	---
154	
155	### ❌ 已终结方向（本轮调研新增）
156	
157	| 方向 | 根因 |
158	|---|---|
159	| cuDNN SDPA / FlashInfer FA2 dense path | `--dense-as-sparse` 强制，代码路径不存在 |
160	| FA3 / FA4 | sm_120 无 TMEM，架构不支持 |
161	| StreamK for M=8192 MLP GEMM | tiles >> 156 SMs，wave quantization loss <2%，无收益 |
162	| SnapKV / PyramidKV | 仅减少 decode KV 内存，prefill FLOPs 不变 |
163	| chunk_size > 64 for GLA | sm_120 96KB SMEM 装不下（已实测 §5 kernels-sm120） |
164	| Chunk-level pipeline overlap | 单 GPU，所有 op 串行，stage2 memory-bound 无 overlap 空间 |
165	| Triton NVFP4 GEMM | 比 CUTLASS 慢，已实测 |
166	| compress_k 优化 | 占比 <1%，不值得投入 |
167	| Prefix caching（Marconi 等） | 比赛评测场景无复用，完全无效 |
168	| b12x backend | 已废弃（draft CUDA graph 不兼容，见 `docs/eagle/README.md §1`） |
169	
170	---
171	
172	## 3. 优先级矩阵
173	
174	| 优先级 | 方向 | 预估 e2e 收益 | 工程代价 | 状态 |
175	|---|---|---|---|---|
176	| **P0** | BLASST / Skip Softmax | +10-13% | 中（kernel patch） | 待验证 |
177	| **P1a** | topk 96→64 精度实验 | +7-8% | 低（1 env var） | 待 A/B |
178	| **P1b** | SageAttention3 FP4 sparse | +5-15%（不确定） | 低（安装+测） | 需 API 验证 |
179	| **P2** | FLA 0.5.0 PR#361 cherry-pick | +0.5-1% | 极低（3 行 patch） | 待实施 |
180	| **P3a** | CUTLASS tile sweep M=8192 | +0.3-0.8% | 中（编译 + bench） | 待展开 |
181	| **P3b** | MInference 动态稀疏 | 未知 | 高 | 待调研 |
182	
183	---
184	
185	## 4. 调研空白与不确定性
186	
187	本轮调研存在以下已知盲区，Phase 2 需要补充：
188	
189	1. **infllm_v2 包内部实现**：未看 `infllmv2_attn_varlen_func` 的 C++/CUDA 源码，不确定是否已内置 BLASST 或类似 skip 逻辑。需要查包源码或 GitHub 仓库。
190	
191	2. **SageAttention3 sparse varlen API**：只知道 wheel 存在和 dense benchmark 数字，未验证 `varlen_sparse` 是否可用于我们的 page table 格式。
192	
193	3. **infllm_v2 sm_120 路径**：官方 README 仅提 SM80/SM90 优化，sm_120 是否有 regression 或有 native 路径未确认。
194	
195	4. **topk 精度 sensitivity**：减少 retrieved KV 对 deepresearch 长文本的 accuracy 影响完全未量化。这是 P1a 的最大风险。
196	
197	5. **stage1 block_score 瓶颈详查**：stage1+pool+topk 合计 ~5%，相比 stage2 26% 是次要的，但其 kernel 是否已针对 sm_120 优化未确认。
198	
199	---
200	
201	## 5. Phase 2 工作计划
202	
203	按 ROI 排序：
204	
205	1. **检查 infllm_v2 BLASST 状态** — 读源码 5 min，决定是否需要自己 patch
206	2. **SageAttention3 API 探测** — 安装 + 10 min 代码检查，确认 varlen sparse 是否可用
207	3. **topk A/B 实验** — 改 1 行 env var，跑 eval bench，定量 accuracy delta
208	4. **FLA PR#361 cherry-pick** — 低风险，可并行
209	5. **BLASST 移植**（若 infllm_v2 未内置） — 核心工程任务
210
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py",
  "limit": 120,
  "offset": 150
}
```

> TOOL

tool_result Read
```
150	        b_o = tl.sum(b_o, axis=0)
151	        tl.store(p_o, b_o.to(p_o.dtype.element_ty), mask=m_v)
152	
153	        # Store intermediate state after each step
154	        p_ht = ht_all + i_n * ht_stride_n + step * ht_stride_t + i_h * ht_stride_h + o_k[:, None] * V + o_v[None, :]
155	        tl.store(p_ht, b_h.to(p_ht.dtype.element_ty), mask=m_h)
156	
157	        p_q += q_stride_t
158	        p_k += k_stride_t
159	        p_v += v_stride_t
160	        p_o += o_stride_t
161	
162	
163	def _fused_recurrent_gla_launch(q, k, v, g_gamma, scale, initial_state, cu_seqlens,
164	                                 o_buf, ht_buf, retrieve_parent_token=None):
165	    """Launch fused recurrent GLA kernel into pre-allocated buffers.
166	
167	    All output buffers must be pre-allocated (for CUDA graph safety).
168	
169	    Args:
170	        q, k, v: (1, total_tokens, H, K/V)
171	        g_gamma: (H,) log decay
172	        scale: float
173	        initial_state: (N, H, K, V) or None
174	        cu_seqlens: (N+1,) cumulative sequence lengths
175	        o_buf: pre-allocated output buffer (NK, 1, total_tokens, H, V)
176	        ht_buf: pre-allocated state buffer (N*H, T_per_seq, K, V)
177	    """
178	    B, total_T, H, K = q.shape
179	    V = v.shape[-1]
180	    N = len(cu_seqlens) - 1
181	
182	    BK = min(triton.next_power_of_2(K), 64)
183	    BV = min(triton.next_power_of_2(V), 64)
184	    NK = triton.cdiv(K, BK)
185	    NV = triton.cdiv(V, BV)
186	    T_per_seq = total_T // N
187	
188	    if retrieve_parent_token is not None:
189	        stride_retrieve_parent_token_seq = retrieve_parent_token.stride(0)
190	        [REDACTED](1)
191	    else:
192	        stride_retrieve_parent_token_seq = 0
193	        stride_retrieve_parent_token_token = 0
194	
195	    grid = (NV, NK, N * H)
196	    _fused_recurrent_gla_intermediate_kernel[grid](
197	        q=q, k=k, v=v, g_gamma=g_gamma,
198	        o=o_buf, h0=initial_state, ht_all=ht_buf,
199	        cu_seqlens=cu_seqlens, scale=scale,
200	        retrieve_parent_token_ptr=retrieve_parent_token,
201	        T=total_T, B=B,
202	        q_stride_t=q.stride(1), q_stride_h=q.stride(2),
203	        k_stride_t=k.stride(1), k_stride_h=k.stride(2),
204	        v_stride_t=v.stride(1), v_stride_h=v.stride(2),
205	        o_stride_nk=o_buf.stride(0), o_stride_t=o_buf.stride(2), o_stride_h=o_buf.stride(3),
206	        h0_stride_n=initial_state.stride(0) if initial_state is not None else 0,
207	        h0_stride_h=initial_state.stride(1) if initial_state is not None else 0,
208	        ht_stride_n=ht_buf.stride(0), ht_stride_t=ht_buf.stride(1), ht_stride_h=ht_buf.stride(2),
209	        stride_retrieve_parent_token_seq=stride_retrieve_parent_token_seq,
210	        [REDACTED],
211	        NP2_T=triton.next_power_of_2(T_per_seq),
212	        H=H, K=K, V=V, BK=BK, BV=BV,
213	        HAS_EAGLE_TREE_CUSTOM_ATTN_MASK=retrieve_parent_token is not None,
214	    )
215	
216	
217	def _fused_recurrent_gla_with_intermediate(q, k, v, g_gamma, scale, initial_state, cu_seqlens,
218	                                            o_buf=None, ht_buf=None, retrieve_parent_token=None):
219	    """Convenience wrapper — allocates buffers if not provided (NOT CUDA graph safe)."""
220	    B, total_T, H, K = q.shape
221	    V = v.shape[-1]
222	    N = len(cu_seqlens) - 1
223	    T_per_seq = total_T // N
224	
225	    BK = min(triton.next_power_of_2(K), 64)
226	    NK = triton.cdiv(K, BK)
227	
228	    if o_buf is None:
229	        o_buf = q.new_empty(NK, *v.shape, dtype=torch.float32)
230	    if ht_buf is None:
231	        ht_buf = q.new_empty(N, T_per_seq, H, K, V, dtype=torch.float32)
232	
233	    _fused_recurrent_gla_launch(
234	        q,
235	        k,
236	        v,
237	        g_gamma,
238	        scale,
239	        initial_state,
240	        cu_seqlens,
241	        o_buf,
242	        ht_buf,
243	        [REDACTED],
244	    )
245	
246	    o = o_buf.sum(0).to(q.dtype)
247	    return o, ht_buf
248	
249	
250	def _build_retrieve_parent_token(
251	    retrieve_next_token: Optional[torch.Tensor],
252	    retrieve_next_sibling: Optional[torch.Tensor],
253	    out: Optional[torch.Tensor] = None,
254	) -> Optional[torch.Tensor]:
255	    if retrieve_next_token is None or retrieve_next_sibling is None:
256	        return out
257	
258	    bs, draft_token_num = retrieve_next_token.shape
259	    next_cpu = retrieve_next_token.cpu().tolist()
260	    sibling_cpu = retrieve_next_sibling.cpu().tolist()
261	    parent_cpu = [[0] * draft_token_num for _ in range(bs)]
262	
263	    for b in range(bs):
264	        queue = [0]
265	        seen = {0}
266	        while queue:
267	            node = queue.pop(0)
268	            child = next_cpu[b][node]
269	            while child != -1:
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/prefill-accel-survey.md"
}
```

> TOOL

tool_result Read
```
1	# Prefill 加速综合调研（Phase 1 + Phase 2）
2	
3	**更新**：2026-04-28  
4	**场景**：RTX 6000D (sm_120)，MiniCPM-SALA-NVFP4，128K prompt，`--chunked-prefill-size 8192`，`--dense-as-sparse`（必须开，否则精度问题）
5	
6	---
7	
8	## 0. 场景约束（先读）
9	
10	### 0.1 `--dense-as-sparse` 强制开启
11	
12	所有 8 个 standard attention 层无论序列长度一律走 InfLLM-v2 稀疏路径，不存在 "短序列 dense FA" 分支。`minicpm_backend.py:322` `self.dense_len = 0 if self.dense_as_sparse else hf_config.sparse_dense_len`。
13	
14	推论：cuDNN SDPA、FlashInfer FA2 dense 路径优化完全无效（代码分支不存在）。
15	
16	### 0.2 Stage2 实际调用路径（Phase 2 Agent 1 发现）
17	
18	生产 stage2 sparse FA 使用 **FlashInfer `BatchPrefillWithPagedKVCacheWrapper`**，不是 `infllmv2_attn_varlen_func`（后者只出现在 bench 脚本）。infllm_v2 只负责 stage1（`infllmv2_attn_stage1` + `max_pooling_1d_varlen`）。
19	- 来源：Phase 2 Agent 1（infllm_v2 源码精读）
20	
21	### 0.3 page_size=1 全局约束（Phase 2 Agent 13 确认）
22	
23	SGLang KV cache 全局 `page_size=1`（`prepare_env.sh` 未传 `--page-size`，`minicpm_backend.py:1410` 有 `assert self.page_size == 1`）。结果：每请求 sparse_topk=96 → kv_indices 6144 条，每条指向 1 个 token。改大 page_size 需重写 KV 分配器（`sparse_kernel_extension.so` 是预编译二进制，返回 token 级索引），短期不可行。
24	- 来源：Phase 2 Agent 13（page_size 确认）
25	
26	### 0.4 sm_120 硬件约束速查
27	
28	| 属性 | 值 |
29	|---|---|
30	| 架构 | sm_120 (Blackwell GB202，consumer，无 TMEM）|
31	| SMEM/SM | ~96-100 KB |
32	| HBM BW | **1568 GB/s (GDDR7)**（vs sm_89 960 GB/s，**1.63×**）|
33	| L2 cache | **112 MB**（vs sm_89 ~6 MB，**18.7×**）|
34	| FA4 / FA3 | **不可用**（依赖 TMEM，GB202 无）|
35	| BF16 MMA | `mma.sync` m16n8k16（非 `wgmma`，无 SMEM accumulator 直读）|
36	| TMA | 有（1-CTA，但 paged KV indirection 不兼容）|
37	| Warp Spec | 有（100KB SMEM 限制 pipeline stage 数）|
38	- 来源：Phase 2 Agent 10（Blackwell CUDA 特性）
39	
40	### 0.5 Profiling 数据（128K prompt, chunked-prefill-size=8192）
41	
42	| 阶段 | 占比 |
43	|---|---|
44	| extend_sparse_fa（8 std layer × stage2 sparse FA） | ~26% |
45	| mlp（32 层 MLP） | ~16% |
46	| attn_gla（24 层 GLA） | ~11% |
47	| attn_standard QKV/OUT + RoPE | ~5% |
48	| sparse_topk（stage1 + pool + topk_select） | ~5% |
49	| compress_k | <1% |
50	| ln + residual + embed + final_norm | ~2% |
51	- 来源：`docs/prefill.md §1`（现有 profiling）
52	
53	---
54	
55	## 1. 关键发现：stage2 sparse FA 是内存带宽瓶颈
56	
57	**算术强度分析**（topk=96, block_size=64, head_dim=128, BF16）：
58	
59	```
60	每 query block:
61	  FLOPs ≈ 2 × 96×64 × 128 × 2(QK+AV) ≈ 3.1M FLOP
62	  Bytes ≈ 96×64×128×2(K) + 96×64×128×2(V) ≈ 3.9M bytes
63	  算术强度 ≈ 0.78 FLOP/byte
64	```
65	
66	ridge point = 1467T / 1568G ≈ **935 FLOP/byte**，实际强度 0.78 ≪ 935。
67	
68	**结论：stage2 是极度内存带宽受限操作。**  
69	有效优化只有两类：**减少 HBM 流量**（更少 KV blocks）或 **skip 零权重块**（BLASST）。  
70	提升 TC 利用率（更大 tile、StreamK）对 stage2 **无效**。
71	- 来源：Phase 1 Agent 5（pipeline overlap 分析）；Phase 2 Agent 10 确认硬件带宽数据
72	
73	sm_120 的 112MB L2 cache 是天然优势：sparse FA 的热 KV blocks 大概率命中 L2，无需代码改动。
74	
75	---
76	
77	## 2. 优先级矩阵（最终）
78	
79	| 优先级 | 方向 | 预估 e2e 收益 | 工程代价 | 状态 |
80	|---|---|---|---|---|
81	| **P0** | trtllm_fmha_v2_prefill 直调（kernel swap，跳过 all-masked Q 行）| **+10%（1.67× stage2）**，与 P1a 复合可达 +17%（2.86× stage2）| 低（半天）+ accuracy A/B | **可实施但需 eval 验证**：行为变化（fa2 garbage → trt zero on all-masked rows） |
82	| ~~P0-old~~ | ~~BLASST via wrapper backend="trtllm-gen"~~ | ~~+10-13%~~ | ~~中~~ | **死**（SM120 wrapper 不支持 + skip_softmax kernel bug）|
83	| **P1a** | topk 96→64（global topk 64→32）| +7-8% | 极低（1行）| 待 A/B |
84	| **P1b** | chunked-prefill-size 8192→16384 | +5-10% | 极低（1 参数）| 待 bench |
85	| **P2a** | ENABLE_SM120=1（FlashInfer SM120 路径）| 未知（可能显著）| 极低（1 env var）| 待验证 |
86	| **P2b** | use_fp16_qk_reduction=True | 小（1-3%）| 极低 | 待验证 |
87	| **P3a** | FLA 0.5.1 升级（Blackwell crash fix）| +0.5-1.6% | 低 | 待验证兼容性 |
88	| **P3b** | RadixCache evict 增量优化（#14339）| TTFT 改善 | 低 | 待 cherry-pick |
89	| **P3c** | topk + chunk_size 联合调参 | +5-15% | 低（参数扫描）| 待 bench |
90	| **P4** | XAttention 替换 stage1 block_score | +15-25% | 中 | 待调研可行性 |
91	| **P5** | Chunked prefill KV 泄漏修复（#20476）| 稳定性 | 中 | 待验证 |
92	
93	---
94	
95	## 3. 各方向详细说明
96	
97	### P0 — BLASST / Skip-Softmax（FlashInfer trtllm-gen）
98	
99	**原理**：在 sparse FA 内部，对零贡献行跳过 AV GEMM，减少 HBM 流量。  
100	**收益**：论文报告 stage2 ~1.4-1.5×；stage2 占 26% → e2e +10-13%。  
101	**API 已就绪**：FlashInfer 0.6.8.post1 `BatchPrefillWithPagedKVCacheWrapper.run()` 和 `BatchDecodeWithPagedKVCacheWrapper.run()` 均有 `skip_softmax_threshold_scale_factor: Optional[float] = None` 参数，自 v0.6.4（PR #2477，已合并）起可用。  
102	**关键约束**：skip-softmax 仅在 `backend="trtllm-gen"` 时生效，当前用 `backend="fa2"`（`minicpm_attention_kernels.py:311`）。
103	
104	---
105	
106	#### **2026-04-28 实测调查更新**（关键转折）
107	
108	**调查结论**（离线实测 + C++ 源码精读）：
109	
110	| 子路径 | 状态 | 原因 |
111	|---|---|---|
112	| `BatchPrefillWithPagedKVCacheWrapper(backend="trtllm-gen")` wrapper | **完全死** | `flashinfer/data/include/flashinfer/trtllm/fmha/fmhaRunner.cuh:30` 硬编码 `mSM == kSM_100 \|\| mSM == kSM_103`，直接抛 `Unsupported architecture` |
113	| `flashinfer.prefill.trtllm_fmha_v2_prefill` 直调（无 skip_softmax）| **可用，1.67× 快** | JIT 生成 SM120 专用 kernel；正确性 cos=0.999995（BF16 噪声内）|
114	| `trtllm_fmha_v2_prefill` + `skip_softmax_threshold_scale_factor>0` | **死（SM120 kernel bug）** | 任何非零阈值都返回 NaN/Inf；FlashInfer issue #2555 范畴 |
115	
116	**正确性验证**（`/tmp/test_correctness_v2.py`，BS=1, Q=128, KV=256, BF16）：
117	- 正确参数：`bmm1_scale=1/sqrt(d), bmm2_scale=1.0`（C++ 内部 `scale_softmax` 硬编码 1.0）
118	- vs FA2 baseline：cos=0.999995, max_abs=0.0010
119	- 之前 cos=0.0 失败原因：scale 参数 convention 错误，**不是布局不兼容**
120	
121	**KV cache 布局兼容性**（C++ 源码 `paged_kv_cache.h` + `gmem_tile_qkv_packed.h:868-869` 精读）：
122	
123	trtllm kernel 模型：
124	- 单一 `mPoolPtr` + `mBlockOffsets[B, 2, M]`，`[b,0,m]` = K page 偏移，`[b,1,m]` = V page 偏移
125	- `mBytesPerBlock = page_size * h_kv * d * sizeof(dtype)`（半 page，仅 K 或仅 V）
126	- 物理上期望 `pool[2p] = K of page p, pool[2p+1] = V of page p`（K0/V0/K1/V1 交错）
127	
128	我们的 KV cache 是 `[total_pages, 2, page_size, num_kv, dim]` row-major，实际字节布局：
129	```
130	[K page0 | V page0 | K page1 | V page1 | ...]
131	```
132	**完全等同 trtllm 期望的交错格式**。Python wrapper 现有的 `block_tables * 2` / `* 2 + 1` 展开正确匹配我们的 mBytesPerBlock 偏移模型。`page_size=1` 让 NHD/HND 字节等价，`.transpose(-3,-2).contiguous()` 在 PS=1 下是 no-op。
133	
134	**结论：KV cache 不需要任何重组**。
135	
136	**性能实测**（Q=8192, KV=6144, H=32/2, D=128, BF16）：
137	
138	| 路径 | 时延 | 加速 |
139	|---|---|---|
140	| `fa2` (current) | 3.949 ms | 1.0× |
141	| `trtllm_fmha_v2_prefill` | 2.360 ms | **1.673×** |
142	
143	e2e 估算：stage2 占 26% × (1 − 1/1.673) ≈ **+10.4%**
144	
145	**吞吐成本分析（throughput-free 验证）**：
146	- 内存：零（KV cache 复用现有分配，无新增 buffer）
147	- 拷贝：零（layout 字节兼容，无 `.contiguous()` 强制 copy）
148	- 转换开销：`kv_indices + kv_indptr → block_tables [BS, max_pages]`，每 prefill chunk 一次，6144 entry int32 ≈ 24KB，~1µs，可忽略
149	- 精度：cos=0.999995（BF16 噪声内）
150	- **完全 throughput-free，无精度损失**
151	
152	**待解决的工程问题**（实施时）：
153	1. **API 切换**：`minicpm_attention_kernels.py:622` `wrapper.forward()` → `flashinfer.prefill.trtllm_fmha_v2_prefill()`
154	2. **block_tables 构造**：增加 `kv_indices + kv_indptr → block_tables [BS, max_pages]` vectorized 转换（CUDA graph 友好）
155	3. **CUDA graph 适配**：`trtllm_fmha_v2_prefill` 没有 wrapper 的 `plan/begin_forward` 分离 API。但 prefill 本来就不在 CUDA graph 路径（CUDA graph 仅 decode），影响小；decode 路径仍走 fa2 wrapper 不动
156	4. **skip_softmax 死路**：失去 BLASST 的额外稀疏性收益（论文 1.4-1.5× stage2），仅得 1.67× kernel 加速；SM120 kernel bug 需 FlashInfer 上游修复，短期不可行
157	
158	**修正后的预期收益**：+10% e2e prefill（throughput-free，无精度损失），原 +10-13% 是含 BLASST，现实只能拿基础 kernel swap 的份。
159	
160	**实施代价**：~半天（API swap + block_tables 转换 + smoke test + bench）。
161	
162	---
163	
164	#### **2026-04-28 第二轮深入调查：1.67× 加速来源剖析（关键风险点）**
165	
166	第一轮 bench 报告 1.67× speedup（Q=8192, KV=6144），但更广形状的 sweep 暴露异常：
167	
168	| Q | KV | speedup | cos vs fa2 |
169	|---|---|---|---|
170	| Q=KV=8192 | — | **1.01×（无加速）** | 1.000 |
171	| Q=8192, KV=6144 | Q>KV | 1.68× | 0.982 |
172	| Q=8192, KV=4096 | Q>KV | 2.89× | 0.945 |
173	| Q=8192, KV=2048 | Q>KV | 5.24× | 0.845 |
174	| Q=16384, KV=2048 | Q≫KV | 9.25× | 0.716 |
175	| Q<KV | — | 1.0× | 1.000 |
176	
177	speedup 与 cos 完美**反相关** —— 速度越快输出越偏离 fa2。
178	
179	**根因（C++ 源码 `warpspec/dma.h:356-393`）**：
180	
181	```cpp
182	int past_kv_length = actual_kv_seqlen - actual_q_seqlen;
183	int q_tile_offset = local_q_tile_offset + past_kv_length;
184	```
185	
186	trtllm 和 fa2 都用 **bottom-right 对齐的 shifted causal**（FlashAttention v2.1+ 标准，参考 [FlashMask paper arXiv:2410.01359](https://arxiv.org/html/2410.01359v1)）。当 Q>KV 时 `past_kv_length<0`：
187	- 前 `Q-KV` 个 query 行的可见 KV 集合为空（all-masked rows）
188	- fa2：在 all-masked rows 输出 garbage（norm=18.5，未定义行为残留累加器状态）
189	- trtllm：输出 0（modern FlashMask convention，"stranded queries default to 0"）
190	
191	**Per-row 验证**（`/tmp/test_per_row_correctness.py`）：
192	
193	| Q 范围 | 含义 | mean_cos vs fa2 | max_abs |
194	|---|---|---|---|
195	| Q[0..2048) | all-masked（fa2 garbage / trt zero）| **0.000** | 0.0273 |
196	| Q[2048..8192) | 正常 attention（两 kernel 一致）| **0.999999** | 0.0002 |
197	
198	差异 100% 集中在 all-masked 区域，正常计算的 5/6 query 完全 BF16 等价。
199	
200	**1.67× 加速来源拆解**（`/tmp/bench_speedup_isolation.py`）：
201	
202	| Q | KV | mask=causal | mask=padding |
203	|---|---|---|---|
204	| 8192 | 6144 | **1.68×** | 1.00× |
205	| 8192 | 4096 | **2.92×** | 1.01× |
206	| 8192 | 8192 | 1.01× | 1.01× |
207	
208	`mask=padding`（无 causal）下两 kernel 完全持平。**所有 1.67× 加速来自 trtllm 的 early-exit：跳过 all-masked Q 行的计算**。fa2 仍执行那些行（虽产生 garbage）。
209	
210	**生产场景适用性分析**：
211	
212	我们的 stage2 sparse FA：
213	- Q = chunk_size = 8192（chunked-prefill，每 chunk 处理 8192 个 token）
214	- KV = topk × block_size = 96 × 64 = 6144（sparse-selected 过去 token）
215	- **生产稳定处于 Q>KV 区间**（Q=8192, KV=6144）
216	- production code `causal=True` hardcoded（`minicpm_backend.py:1064/1344`）
217	
218	含义：production 当前每个 chunk **前 2048 个 query 拿到 fa2 的 garbage 输出**，模型经 32 层运行依然产出合理结果——已测过容忍这种 noise。改用 trtllm 后那 2048 行变成 zero，**行为更"清洁"但属于行为改变**。
219	
220	**联合 P0 + P1a 的复合效益**（`/tmp/bench_production_realistic.py`）：
221	
222	| KV size（对应 topk）| speedup | all-masked Q |
223	|---|---|---|
224	| KV=3072（topk=48）| **4.00×** | 5120 |
225	| KV=4096（topk=64）| **2.86×** | 4096 |
226	| KV=6144（topk=96）| 1.67× | 2048 |
227	| KV=8192（无 all-masked）| 1.01× | 0 |
228	
229	P0（trtllm swap）和 P1a（topk 96→64）**乘性复合**：联合可拿 stage2 2.86× → **e2e +17%**。topk 越小 trtllm 优势越大。
230	
231	batch scaling（验证非 small-batch 假阳性）：
232	
233	| BS | fa2 ms/call | trt ms/call | speedup | 8-layer e2e 节省 |
234	|---|---|---|---|---|
235	| 1 | 3.98 | 2.37 | 1.68× | 12.9 ms |
236	| 2 | 7.76 | 4.72 | 1.64× | 24.3 ms |
237	| 4 | 15.44 | 9.39 | 1.64× | 48.4 ms |
238	| 8 | 30.62 | 18.66 | 1.64× | 95.6 ms |
239	
240	加速跨 batch 稳定 1.64-1.68×，节省随 batch 线性扩。128K prefill = 16 chunks × 8 std layers × 节省 → 总节省可观。
241	
242	**部署风险评估**：
243	
244	| 风险 | 评估 |
245	|---|---|
246	| 正常 Q 行（5/6）的精度 | cos=0.999999, max_abs=0.0002（BF16 完美对齐）✓ |
247	| All-masked Q 行（1/6 = 2048 / chunk）行为改变 | fa2 garbage(norm=18.5) → trt zero。生产模型在 fa2 输出上稳定 32 层，理论上 zero 更清洁，但**未验证**模型对 zero 的反应 |
248	| skip_softmax 不可用 | SM120 kernel bug，无 BLASST 加成，仅得 kernel swap 1.67× |
249	| CUDA graph 兼容 | prefill 不在 CUDA graph 路径，影响小 |
250	
251	**最终结论**：
252	
253	1. **1.67× 加速是真实的、kernel swap 级别的、throughput-free 的优化**——但来源是 trtllm 跳过 all-masked Q 行（这些行 fa2 也算了但产出 garbage）
254	2. 仅对 Q>KV 场景有效（我们生产恰好命中）
255	3. 与 P1a topk 减少**乘性复合**，topk 64→32 后可获 2.86× stage2
256	4. **核心风险**：行为变化（fa2 garbage → trt zero）需要模型 A/B accuracy eval 验证不退化
257	5. 网搜确认 trtllm 的 zero 输出符合现代 FlashMask 标准（[arXiv:2410.01359](https://arxiv.org/html/2410.01359v1)），是更"正确"的实现
258	
259	**实施前置条件**：
260	- 部署后必须跑 deepresearch 长文本 eval，确认 BLEU/ROUGE 不下降
261	- 若退化：考虑混合方案（保留 fa2 给前 2048 Q 行，trtllm 处理后续）
262	- 备选退路：用 `causal=False` 拿 0 加速（无 all-masked rows，但语义更对）→ 需另行 A/B
263	
264	- 来源：Phase 2 Agent 1（生产路径确认）；Phase 2 Agent 6（BLASST PR 精读，PR #2477）；2026-04-28 离线实测（`/tmp/test_trtllm_sm120.py`, `/tmp/test_correctness_v2.py`, `/tmp/test_blasst_threshold.py`, `/tmp/bench_trtllm_vs_fa2.py`）；C++ 源码精读（`fmha_v2_run.cu:540-595`, `paged_kv_cache.h`, `gmem_tile_qkv_packed.h:860-870`, `dma.h:368`）
265	
266	---
267	
268	### P1a — topk 96→64（1 行代码）
269	
270	**原理**：模型配置 `hf_config.sparse_topk=64`，代码算出 `self.sparse_topk = 64 + 32(local) = 96`，stage2 KV 序列长度 `= 96×64 = 6144 tokens`。减少 global topk 64→32 → total sparse_topk 96→64 → stage2 KV 长度 **6144→4096（-33%）**。  
271	**代码**：`minicpm_backend.py:324`，一行改动：  
272	```python
273	topk = int(os.environ.get("SGLANG_INFLLM_TOPK", str(hf_config.sparse_topk)))
274	```
275	设置 `SGLANG_INFLLM_TOPK=32`，下游 buffer（sparse_page_table、kv_indices、CUDA graph buffer）全部自动适配，**无需改其他代码**。  
276	**实施**：改 1 行 + 跑 eval benchmark（deepresearch 长文本），确认 BLEU/ROUGE 无可测量下降（<1%）。  
277	**注意**：kv_indices 大小随 topk 线性缩减，同时缓解 page_size=1 带来的 kv_indices 表压力（6144→4096 条）。  
278	- 来源：Phase 2 Agent 3（minicpm_backend.py 精读，topk 计算链，行号已确认）
279	
280	---
281	
282	### P1b — chunked-prefill-size 8192→16384
283	
284	**原理**：128K prompt / 8192 = 16 次 chunk；改为 16384 → 8 次 chunk，减少约一半的 kernel launch 和调度轮次，overhead 降低 10-15%。  
285	**交互**：更大 chunk → 每 chunk 的 KV 更多 → stage1 block_score 更准确 → 可能允许更低 topk（与 P1a 联合调优空间）。  
286	**约束**：peak KV cache memory 上升，需确认 84GB VRAM 下 128K 上下文是否 OOM。  
287	**实施**：在 `SGLANG_SERVER_ARGS` 加 `--chunked-prefill-size 16384`，bench 对比。  
288	- 来源：Phase 2 Agent 7（2025-2026 sparse attention 综述）
289	
290	---
291	
292	### P2a — ENABLE_SM120=1
293	
294	**发现**：FlashInfer 内部有 FMHA_V2 SM120 专用 prefill kernel，但被 `ENABLE_SM120` 环境变量门控，且路由逻辑未修正（SM120 被降级到 generic FA2）。设置此变量可能解锁 SM120 专用路径（FlashInfer issue #2555，修复尚未合并）。  
295	**实施**：在 `prepare_env.sh` 加 `export ENABLE_SM120=1`，先发 3 条 smoke test 确认正确性，再 bench 对比。  
296	**风险**：专用路径可能有未修复的 routing bug（否则早就默认开了）。  
297	- 来源：Phase 2 Agent 8（FlashInfer 0.6.8+ API 调研）
298	
299	---
300	
301	### P2b — use_fp16_qk_reduction=True
302	
303	**发现**：`BatchPrefillWithPagedKVCacheWrapper.plan()` 支持 `use_fp16_qk_reduction=True` 参数，我们当前未使用。  
304	**效果**：加速 QK reduction 步骤，轻微精度损失（需 A/B 验证是否影响生成质量）。  
305	- 来源：Phase 2 Agent 8
306	
307	---
308	
309	### P3a — FLA 0.5.1 升级
310	
311	**核心价值（稳定性优先）**：  
312	- **PR #825（0.4.2）**：修复 Blackwell 上 Triton autotune 的 `NullAllocator` 崩溃——这是针对我们硬件的稳定性修复  
313	- **PR #798（0.5.0）**：FLA autotune cache，避免重复编译  
314	- GLA chunk_size 策略未变（仍 min(64, max(16, next_pow2(T)))）  
315	- PyTorch 2.11 满足 FLA 0.5.x 要求（≥ 2.7.0）  
316	**收益**：GLA 占 prefill 11%，预估 5-15% GLA kernel 改善 → e2e +0.5-1.6%。  
317	**附加 Triton 层面小优化**（无需升级 FLA）：调整 FLA GLA kernel 的 `num_stages`（当前硬编码 2，可试 3/4）和 `num_warps`（sm_120 有 65536 regs/SM，可试 8）——参数调优，不需重写 kernel，单独微 benchmark 确认。  
318	**警告**：`FLA_USE_FAST_OPS=1` 在 sm_120 上使 `tl.exp2` 比 `tl.exp` 慢 83%，务必保持默认关闭。  
319	- 来源：Phase 2 Agent 12（FLA 版本分析）；Phase 2 Agent Triton（Triton 3.6 实测）
320	
321	---
322	
323	### P3b — RadixCache evict 增量优化（SGLang #14339）
324	
325	**改动**：将 `RadixCache.evict()` 从每次全树遍历 O(N) 改为增量维护 `evictable_leaves` Set。  
326	**收益**：128K 上下文高并发下，eviction 7ms→0.5ms，直接影响 TTFT。  
327	**冲突风险**：低，可独立 cherry-pick（修改 `radix_cache.py` 的 4-5 个方法）。  
328	- 来源：Phase 2 Agent 9（SGLang 上游调研，PR #14339 v0.5.9）
329	
330	---
331	
332	### P3c — topk + chunked-prefill-size 联合调参
333	
334	P1a 和 P1b 存在耦合：更大 chunk → block_score 更准 → 可能允许更低 topk → peak memory 减少 → 支持更大 chunk。是二维联合优化空间，低成本（参数扫描），建议在 P1a/P1b 单独验证后做联合扫描。
335	
336	---
337	
338	### P4 — XAttention 替换 stage1 block_score
339	
340	**原理**（arXiv 2503.16428，ICML 2025，MIT Han Lab）：对每个 block 沿反对角线做 strided 采样求和，比 compress_k mean-pooling 更精准，允许在相同精度下降低 topk。代码已开源（github.com/mit-han-lab/x-attention）。  
341	**收益**：若 topk 可从 96 降至 64-72 且精度持平，stage2 减少 25-33%，e2e +15-25%。  
342	**与 P1a 关系**：P4 提供更智能的 topk 选择，P1a 是粗暴减少数量。P4 的价值在于不降低精度的前提下实现 P1a 的效果。  
343	**工程成本**：中（实现反对角线采样 kernel + 替换 stage1 block_score 逻辑）。  
344	**先做 P1a 的 accuracy A/B**：若 topk=64 精度无损，P4 的边际价值降低；若有损，P4 是替代方案。  
345	- 来源：Phase 2 Agent 7（2025-2026 综述）
346	
347	---
348	
349	### P5 — Chunked Prefill KV 泄漏修复（#20476）
350	
351	修复 streaming session 下 chunked prefill 的 KV cache 泄漏（三个 bug：多 chunked request 状态混乱、SessionSlot 锁泄露、冗余 radix tree 插入）。是稳定性修复，防止长上下文 prefill 渐进式 KV pool 缩减。回捞需验证与我们 EAGLE-3 自定义逻辑的兼容性。  
352	- 来源：Phase 2 Agent 9（SGLang 上游调研，PR #20476 v0.5.10）
353	
354	---
355	
356	## 4. 已终结方向（本次调研新增）
357	
358	| 方向 | 根因 | 来源 |
359	|---|---|---|
360	| `BatchPrefillWithPagedKVCacheWrapper(backend="trtllm-gen")` | `fmhaRunner.cuh:30` 硬编码 SM100/SM103；SM120 抛 Unsupported architecture | 2026-04-28 实测 |
361	| BLASST skip-softmax on SM120 | trtllm_fmha_v2_prefill 内 skip_softmax 任何非零阈值 NaN/Inf；SM120 kernel bug，需上游修 | 2026-04-28 实测 |
362	| KV cache 重组为交错格式（曾考虑）| **不需要**：现有 `[pages,2,page_size,nkv,dim]` 字节上已是 K0/V0/K1/V1 交错，原生匹配 trtllm pool 模型 | 2026-04-28 C++ 源码精读 |
363	| SageAttention3 | Python ≥ 3.13 硬要求（我们 3.10）；无 varlen/paged KV API | Phase 2 Agent 2 |
364	| FLA PR #361 tl.exp2 | sm_120 上 `tl.exp2` 实测比 `tl.exp` **慢 83%**（0.55×）；`tl.exp` 已是最优；`FLA_USE_FAST_OPS=1` 有害无益 | Phase 2 Agent 4 + Agent Triton |
365	| CUTLASS tile sweep（M=8192）| SM120 只有 3 个有效 tile（flashinfer 已全含）；M=8192 差距 <1%；MLP 16%×3% = 0.48% | Phase 2 Agent 5 |
366	| FA4 / FA3 | SM120 无 TMEM，官方 GitHub Issue #2307 确认不支持 | Phase 2 Agent 7 |
367	| FlashInfer 升级到 0.6.9 | attention kernel 无改动，trtllm paged attn 不稳定 | Phase 2 Agent 8 |
368	| Triton warp specialization / Gluon 重写 GLA | sm_120 显式 `warp_specialize=True` 编译崩溃（Triton 3.6 bug）；Gluon API experimental，需完全重写 kernel；bf16 GLA 不适用 tcgen05 FP4 MMA；重写后收益 <10%，GLA 仅占 11% | Phase 2 Agent Triton |
369	| FlashKDA / CUTLASS GLA kernel | SM90a only；开发成本极高 | Phase 2 Agent 12 |
370	| liger-kernel / xformers GLA | 均无 GLA 实现 | Phase 2 Agent 12 |
371	| TMA-based 自写 sparse FA | paged KV indirection 与 TMA 不兼容；sm_120 无 WGMMA；Triton sparse FA 比 FlashInfer FA2 慢 | Phase 2 Agent 10 + Agent Triton |
372	| Triton Gluon 重写 GLA | experimental API，需完全重写；`warp_specialize=True` sm_120 编译崩溃；bf16 GLA 不受益 FP4 tcgen05 | Phase 2 Agent Triton |
373	| Marconi prefix caching | 比赛评测场景无复用 | Phase 1 用户更正 |
374	| b12x backend | 已废弃（draft CUDA graph 不兼容）| `docs/eagle/README.md §1` |
375	| cuDNN SDPA / dense FA path | `--dense-as-sparse` 强制，代码路径不存在 | Phase 1 用户更正 |
376	| Cluster > 1 | SM120 无 distributed SMEM | `docs/kernels-sm120.md §5` |
377	| StreamK for M=8192 | tiles >> 156 SMs，wave loss <2% | Phase 1 Agent 3 |
378	| SnapKV / PyramidKV | 仅减少 decode KV 内存，prefill FLOPs 不变 | Phase 1 Agent 6 |
379	| compress_k 优化 | 占比 <1%，不值得 | Phase 1 profiling |
380	| chunk-level pipeline overlap | 单 GPU，stage2 memory-bound | Phase 1 Agent 5 |
381	
382	---
383	
384	## 5. 架构级已有优势（无需改代码）
385	
386	- **HBM BW 1.63×**（1568 vs 960 GB/s）：sm_120 vs sm_89
387	- **L2 cache 18.7×**（112 MB vs ~6 MB）：sparse FA 热 KV blocks 大概率命中 L2，天然降低 HBM 访问
388	- **page_size=1 部分缓解**：112MB L2 可吸收大部分 6144 条 page table lookup 的 TLB miss 代价
389	
390	---
391	
392	## 6. 调研空白
393	
394	1. ~~**trtllm-gen sm_120 兼容性**~~：**已结论**——wrapper 路径死，直调 trtllm_fmha_v2_prefill 可用 1.67×（无 skip_softmax）
395	2. **topk accuracy sensitivity**：topk=64 对 deepresearch 长文本的 BLEU/ROUGE 影响完全未量化
396	3. **chunked-prefill-size peak memory**：16384 下 128K 上下文是否 OOM
397	4. **ENABLE_SM120=1 稳定性**：路由修复未合入，behavior 未知
398	5. **Triton 3.6 sm_120 优化**：Agent 9（Triton 3.6）尚未完成
399	6. **XAttention 反对角线 kernel 开销**：实际 stage1 overhead 增加多少，net gain 未量化
400	
401	---
402	
403	## 7. Phase 2 工作计划（优先级排序）
404	
405	1. ~~**验证 trtllm-gen sm_120 兼容性**~~ → **2026-04-28 已完成**：wrapper 死，直调 1.67× 可用
406	2. **P0 实施 trtllm_fmha_v2_prefill kernel swap**（半天）→ +10% e2e，throughput-free
407	3. **topk A/B**（SGLANG_INFLLM_TOPK=32 vs default）→ P1a 精度验证
408	4. **chunked-prefill-size bench**（8192 vs 16384）→ P1b 收益量化
409	5. **ENABLE_SM120=1 smoke test** → P2a 可行性（smoke test 5 分钟）
410	6. **FLA 0.5.1 升级** → P3a（Blackwell crash fix 稳定性收益）
411	7. **RadixCache #14339 cherry-pick** → P3b（低风险）
412	8. **topk + chunk_size 联合调参** → P3c（在 1-3 完成后）
413	9. **XAttention prototype** → P4（若 P1a accuracy 有损）
414
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1	# Adapted from https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/layers/quantization/modelopt.py
2	from __future__ import annotations
3	
4	import logging
5	from enum import IntEnum
6	from typing import TYPE_CHECKING, Any, Dict, List, Optional
7	
8	import torch
9	from torch.nn.parameter import Parameter
10	
11	from sglang.srt.distributed import get_tp_group
12	from sglang.srt.distributed.device_communicators.pynccl_allocator import (
13	    use_symmetric_memory,
14	)
15	from sglang.srt.environ import envs
16	from sglang.srt.layers.dp_attention import is_allocation_symmetric
17	from sglang.srt.layers.moe import (
18	    MoeRunner,
19	    MoeRunnerBackend,
20	    MoeRunnerConfig,
21	    get_moe_runner_backend,
22	)
23	from sglang.srt.layers.moe.cutlass_moe_params import CutlassMoEParams, CutlassMoEType
24	from sglang.srt.layers.moe.moe_runner.triton import TritonMoeQuantInfo
25	from sglang.srt.layers.moe.utils import should_use_flashinfer_cutlass_moe_fp4_allgather
26	from sglang.srt.layers.parameter import ModelWeightParameter, PerTensorScaleParameter
27	from sglang.srt.layers.quantization.base_config import (
28	    FusedMoEMethodBase,
29	    LinearMethodBase,
30	    QuantizationConfig,
31	    QuantizeMethodBase,
32	)
33	from sglang.srt.layers.quantization.fp8_kernel import scaled_fp8_quant
34	from sglang.srt.layers.quantization.fp8_utils import (
35	    apply_fp8_linear,
36	    cutlass_fp8_supported,
37	    is_blackwell_supported,
38	)
39	from sglang.srt.layers.quantization.kv_cache import BaseKVCacheMethod
40	from sglang.srt.layers.quantization.unquant import UnquantizedLinearMethod
41	from sglang.srt.layers.quantization.utils import (
42	    convert_to_channelwise,
43	    is_layer_skipped,
44	    per_tensor_dequantize,
45	    prepare_static_weights_for_trtllm_fp4_moe,
46	    requantize_with_max_scale,
47	    swizzle_blockscale,
48	)
49	from sglang.srt.layers.radix_attention import RadixAttention
50	from sglang.srt.utils.common import (
51	    get_bool_env_var,
52	    is_cuda,
53	    is_sm120_supported,
54	    next_power_of_2,
55	)
56	from sglang.srt.utils.custom_op import register_custom_op
57	from sglang.srt.utils.patch_torch import register_fake_if_exists
58	
59	if TYPE_CHECKING:
60	    from sglang.srt.batch_overlap.single_batch_overlap import DownGemmOverlapArgs
61	    from sglang.srt.layers.moe.fused_moe_triton.layer import FusedMoE
62	    from sglang.srt.layers.moe.token_dispatcher import (
63	        CombineInput,
64	        StandardDispatchOutput,
65	    )
66	
67	try:
68	    if is_sm120_supported():
69	        from flashinfer import fp4_quantize
70	    else:
71	        from sgl_kernel import scaled_fp4_quant as fp4_quantize
72	
73	except ImportError:
74	    fp4_quantize = None
75	
76	try:
77	    from flashinfer import mm_fp4 as flashinfer_fp4_gemm
78	    from flashinfer import reorder_rows_for_gated_act_gemm, shuffle_matrix_sf_a
79	
80	    enable_flashinfer_fp4_gemm = True
81	except ImportError:
82	    if is_cuda():
83	        from sgl_kernel import cutlass_scaled_fp4_mm as cutlass_fp4_gemm
84	    enable_flashinfer_fp4_gemm = False
85	    reorder_rows_for_gated_act_gemm = None
86	    shuffle_matrix_a = None
87	    shuffle_matrix_sf_a = None
88	
89	try:
90	    from flashinfer.fused_moe import cutlass_fused_moe as flashinfer_cutlass_fused_moe
91	    from flashinfer.fused_moe.core import ActivationType
92	except ImportError:
93	    flashinfer_cutlass_fused_moe = None
94	
95	    # Define a minimal ActivationType enum if flashinfer is not available
96	    class ActivationType(IntEnum):
97	        Swiglu = 3
98	        Relu2 = 6
99	
100	
101	# Initialize logger for the module
102	logger = logging.getLogger(__name__)
103	
104	
105	def _sglang_fp4_gemm_fake(
106	    input: torch.Tensor,
107	    weight: torch.Tensor,
108	    input_sf: torch.Tensor,
109	    weight_sf: torch.Tensor,
110	    alpha: torch.Tensor,
111	    out_dtype: torch.dtype,
112	    out_features: int,
113	) -> torch.Tensor:
114	    M = input.shape[-2]
115	    N = int(out_features)
116	    return input.new_empty((M, N), dtype=out_dtype)
117	
118	
119	@register_custom_op(fake_impl=_sglang_fp4_gemm_fake)
120	def fp4_gemm(
121	    input: torch.Tensor,
122	    weight: torch.Tensor,
123	    input_sf: torch.Tensor,
124	    weight_sf: torch.Tensor,
125	    alpha: torch.Tensor,
126	    out_dtype: torch.dtype,
127	    out_features: int,
128	) -> torch.Tensor:
129	    backend = FLASHINFER_FP4_GEMM_BACKEND if FLASHINFER_FP4_GEMM_BACKEND else "cutlass"
130	    if enable_flashinfer_fp4_gemm:
131	        return flashinfer_fp4_gemm(
132	            input, weight, input_sf, weight_sf, alpha, out_dtype, backend=backend
133	        )
134	    else:
135	        return cutlass_fp4_gemm(input, weight, input_sf, weight_sf, alpha, out_dtype)
136	
137	
138	if is_cuda() and (not is_sm120_supported()) and (fp4_quantize is not None):
139	
140	    @register_fake_if_exists("sgl_kernel::scaled_fp4_quant")
141	    def _sgl_kernel_scaled_fp4_quant_fake(
142	        output, input, output_scale, input_global_scale
143	    ):
144	        return
145	
146	
147	CUTEDSL_MOE_SCALAR_INPUT_SCALE = get_bool_env_var(
148	    "SGLANG_CUTEDSL_MOE_SCALAR_INPUT_SCALE", "true"
149	)
150
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/runtime.md"
}
```

> TOOL

tool_result Read
```
1	# Runtime 优化记录
2	
3	## 1. 空响应问题 ✅ 已解决
4	
5	**根因**：旧版 FlashInfer (0.5.3) 的 CUTLASS FP4 GEMM 在 SM120 上产生 NaN → logits 全 NaN → sampling 产生特殊 token → detokenizer 过滤后返回空文本。
6	
7	**解决**：升级 FlashInfer ≥0.6.7.post3 + cuDNN ≥9.15。no-spec / spec 均零空响应，`ori_accuracy=79.11%`。cu13 迁移后 FlashInfer 0.6.8.post1 + cuDNN 9.21 仍稳定。
8	
9	被误判的假设（均已排除）：GDC flag 缺失（平台已有）、Medusa 是主因（no-spec 下仍复现）、CUDA graph buffer overflow（辅助因素，非根因）。
10	
11	## 2. MiniCPM FlashInfer 稀疏路径调研
12	
13	### 背景
14	
15	长上下文样本（prompt ~130K tokens）在稀疏 decode 路径下图外 Python 开销显著。初步怀疑：`forward_decode → get_topk_for_sparse → get_block_table_v3 → FlashInfer kv_indptr/kv_indices 转换` 每 decode step 重复执行。
16	
17	### 结论
18	
19	`sparse_page_table → flashinfer` 转换**不能**提前到 replay 时做：`sparse_page_table` 是每层 `get_topk_for_sparse` 输出，层间 top-k 不同，复用一份会改变语义（验证：同 seed 请求输出 hash 改变）。
20	
21	`fused metadata copy`（`SGLANG_MINICPM_DISABLE_FUSED_META_COPY`）A/B：bs=1 长样本噪声级差异，hash 相同，无收益。
22	
23	### Metadata 冗余（`_compute_single_compression_metadata`）
24	
25	`schedule_batch.prepare_for_decode` 已在 CPU 预算 k1/k2 压缩 metadata 并通过 `forward_batch.*_cpu` 透传；CUDA graph replay 路径（`minicpm_backend.py:1961-2032`）已用 `.copy_()` 消费。Eager decode 路径未消费，形成冗余 GPU 重算。
26	
27	离线 microbench：5× 加速（240→50 us/call），bit-exact，但 e2e 无可感知收益（base 极小）。`fast_level_from_cpu` 已实装（`minicpm_sparse_utils.py`），decode 消费 `*_cpu` 字段。
28	
29	## 3. TARGET_VERIFY replay de-Python 已终结
30	
31	profile 归因（bs=7 dtn=4）：
32	
33	| Phase | 占 verify ms |
34	|---|---|
35	| eagle_verify 总 | 100% |
36	| DC_verify_ai_tolist (GPU sync) | 74% |
37	| target forward GPU | 主导 |
38	| Python control flow | < 5% |
39	
40	**结论**：target forward GPU 时间（~10ms/cycle）主导 verify 总耗时，Python 循环 + `.item()` 只占极小部分。Python 侧 de-Python 优化不具 ROI，**终结此方向**。
41	
42	## 4. 算子优化（已落地）
43	
44	| 优化 | Decode 收益 | Prefill 收益 | 说明 |
45	|---|---|---|---|
46	| RoPE F32 cast 消除 | 140 us/fwd (3.5×) | 11.2 ms/fwd (4.5×) | sgl_kernel RoPE 内部已是 F32；cos_sim=1.0 |
47	| Residual fused multiply-add | 237 us/fwd (2.15×) | 4.4 ms/fwd (5.76×) | 精度高于 F64 参考 |
48	| `scale_emb` / `width` 吸收进权重 | 2 kernels 消除 | 284 us/fwd | BF16-representable 标量，exact |
49	| In-place sigmoid×mul gate | memory pressure ↓ | — | 等价 |
50	| GLA backend cleanup | ~24 us | — | 删冗余 `.contiguous()` + cache 查询 |
51	| flashinfer mm_fp4 离线 autotune | down_proj M=64 3.59×（验证 M 段） | — | 43/70 验证过的 ≥3% 增益入 cache，miss 走 tactic=-1 fallback。详见 [kernels-sm120.md §7.1](kernels-sm120.md#71-flashinfer-mm_fp4-离线-autotune已落地-2026-04) |
52	| **b12x backend + 3-tier dispatch**（集成落地 `SGLANG_ENABLE_B12X=1` default） | decode GEMM kernel 省 32.4%（5 shape × M=24..256）→ e2e ~3% | 0（M=8192 prefill 不覆盖） | Marlin (W4A16) / b12x (W4A4) / CUTLASS (W4A4) 三档，per-shape Marlin 阈值 {8,8,24,16,16}。初版集成用 "pre-permute padded_scales" 错，生产 smoke test 精度回归；改用 `layer.weight_scale_interleaved` + `fp4_quantize` 激活 → **bit-identical vs CUTLASS**，smoke test 通过（1+1=2 正确）。详见 [kernels-sm120.md §7.4](kernels-sm120.md#74-b12x-backend) |
53	
54	（prefill 相关优化另见 [prefill.md](prefill.md)）
55	
56	## 5. stage2 extend_sparse_fa backend 替换（否）
57	
58	长 prefill 混 decode workload，profile（cuda graph 打开）拿到 `prefill_sparse_calls` 平均单次 13.26 ms / 层，内部切分：
59	
60	| 子项 | ms | 占比 |
61	|---|---|---|
62	| `fi_decode_fwd_ms`（FA kernel） | 8.12 | 61% |
63	| `fi_begin_forward_ms`（plan） | 3.19 | 24% |
64	| `fi_convert_ms`（sparse_page_table→flashinfer indices） | 1.92 | 15% |
65	
66	关键事实：stage2 实际走 **BatchDecodeWithPagedKVCacheWrapper**，不是 prefill wrapper。原因是长序列分支 `sparse_max_seq_len_q` 保持默认 1（`minicpm_sparse_utils.py:1309-1333`），触发 `is_prefill=False`；q tokens 摊平到 batch dim，每 q token 一个 "virtual batch"。production shape：`vbatch = 16 req × 512 q_tok × 2 head_group = 16384`，每 vbatch 6144 pages（96 block × 64）。
67	
68	尝试换 FlashInfer backend（`bench/bench_stage2_backends.py`，production shape 离线）：
69	
70	| backend | 结果 |
71	|---|---|
72	| fa2+TC（auto，当前生产） | 7600 μs/call |
73	| fa3 | Ninja 编译失败：fa3 源文件硬编码 sm_90，sm_120 不支持 |
74	| cutlass | `backend must be fa2 or fa3 in gen_batch_prefill_module` —— decode wrapper 拒绝 cutlass |
75	| trtllm-gen | `fmhaRunner.cuh:30 Unsupported architecture` —— sm_120 不支持 |
76	
77	FlashInfer 0.6.8.post1 在 sm_120 上 BatchDecode 只有 fa2+TC 一条路。**backend swap 不通，放弃此方向**。后续若打 stage2 须从 plan overhead / convert overhead 或改 kernel 源（triton 稀疏 decode / flashmla sparse / 虚 batch 合并近似）入手。
78	
79	## 6. 负结果（勿重复踩坑）
80	
81	| 方向 | 结论 |
82	|---|---|
83	| stage2 FlashInfer backend swap（fa3/cutlass/trtllm-gen） | sm_120 全部不支持，见 §5 |
84	| stage2 VariableBlockSparseAttentionWrapper | 4× 慢（398 vs 97 μs），`bench/bench_variable_block_sparse_wrapper.py` |
85	| EAGLE3 draft `--fuse-topk`（tilelang 融合 stage1+pool+topk） | 离线一致性崩（重复率 61%，planted-peak recall 16/160），kernel 只用 k1 且有 dup bug，`bench/bench_fuse_topk_consistency.py` |
86	| FP8 KV cache | 无收益（KV 带宽非瓶颈） |
87	| mamba cache quant (INT8/4) | 不可行（temporal state 累积误差） |
88	| Radix cache | 无收益（bench 每档清 cache） |
89	| Triton NVFP4 GEMV | 2.6× slower（809 vs 307 us/layer） |
90	| FP8 decode | 无收益（权重 1.78× 抵消带宽收益） |
91	| Full Marlin (no hybrid) | prefill 3.8× slower（M=8192） |
92	| SimpleGLA BK=128 kernel | 1.65× slower（eager 1.9× 收益是 Python overhead 假象，CUDA graph 揭真相） |
93	| Medusa K=3 | 微弱（1.543 vs 1.356 tok/step，GLA overhead 2×） |
94	| Triton `kv_indices` kernel | 0.78× slower（`.item()` 在 CPU tensor 上，无 GPU sync 可省） |
95	| `pre_quant_scale` fusion | 不值（CUDA graph 消除 launch overhead；scale 格式 opaque） |
96	| `minicpm_fi` fused metadata copy | 无收益（bs=1 长样本噪声级） |
97	| `_alloc_sparse_for_new_positions` 向量化 | 中性；保留代码，不计收益 |
98	| TARGET_VERIFY replay de-Python | target forward GPU 主导，Python 占比极小（见 §3） |
99	| BS-自适应 EAGLE no-spec 降级 | 实测无收益 |
100	| compressed_k 跨层复用 | smax=64 / 130K A/B 均噪声内，无收益 |
101	
102	## 7. target verify 真实 GPU 时间拆解（2026-04-22）
103	
104	### 问题
105	
106	b12x GEMM backend 落地后，bench 看不到预期 28% 的 e2e 提升。怀疑 target verify 里 GEMM 不是大头。Draft model 时间占比也一并查。
107	
108	### ⚠️ 结论的适用条件
109	
110	- 测试 case：prompt ~20 tokens，`max_tokens=128`，144 次并发 sweep，trace 15s — 是 **短 context 场景**
111	- 生产 `--dense-as-sparse` 下 sparse 路径 **对所有长度都激活**（`dense_len=0`），所以 sparse attn 在短 prompt 也跑，但 seq_len 远小于真实长 context（bench_serving 可到 130K）
112	- 长 context 下 index 占比可能更高或变化，**尚未用 `toolkit/eval_dataset/perf_public_set.jsonl` 的真实长 prompt 复核**
113	
114	### 测量方法
115	
116	**A. draft / target 时间占比（env-gated CUDA event timer）**
117	
118	在 `modelopt_quant.py` 加一个 `_record_replay_timing(kind, start_evt, end_evt)` 累加器，两端入口：
119	- `CudaGraphRunner.replay()`（target verify）：`self.graphs[graph_key].replay()` 前后包一对 `torch.cuda.Event`
120	- `EAGLEDraftCudaGraphRunner._replay()`（draft decode chain）：`self.graphs[self.bs].replay()` 前后包一对
121	
122	每累积到 100 对 event 触发一次 `torch.cuda.synchronize()` + `start.elapsed_time(end)` 求和，dump 到 `/tmp/replay_timing.json`。env `SGLANG_REPLAY_TIMER=1` 启用。
123	
124	启动 + 压测脚本：
125	```bash
126	SGLANG_REPLAY_TIMER=1 bash eval/start_eagle.sh &
127	# 等 Uvicorn running
128	python3 /tmp/trace_prod.py   # S1/S4/S8/S16/S32/Smax 并发 sweep，max_tokens=128
129	cat /tmp/replay_timing.json
130	```
131	
132	**B. target verify kernel 级拆解（nsys delayed capture）**
133	
134	```bash
135	nsys profile --delay=140 --duration=30 --trace=cuda --sample=none \
136	  --output=/tmp/sglang_prof --force-overwrite=true \
137	  bash eval/start_eagle.sh
138	# delay 覆盖 server 启动 + capture graph；
139	# duration 覆盖 trace_prod.py 压测窗口（~15s）
140	nsys stats --report cuda_gpu_kern_sum --format csv \
141	  --output /tmp/sglang_prof_kern /tmp/sglang_prof.nsys-rep
142	# 手动按 time_% 排序 top-30 kernel
143	```
144	
145	解析 CSV 即为每 kernel 的 total time / calls / avg us。nsys 抓的是 GPU 实际执行时间，不含 CPU-side Python 开销。
146	
147	### 结果
148	
149	**A. draft 占比 4.7%**（单并发 sweep，800 target + 800 draft replays）：
150	
151	| | calls | GPU time | avg/call | share |
152	|---|---|---|---|---|
153	| target verify (`CudaGraphRunner.replay`) | 800 | 8509 ms | 10.6 ms | **95.3%** |
154	| draft decode (`EAGLEDraftCudaGraphRunner._replay`) | 800 | 420 ms | 0.53 ms | **4.7%** |
155	
156	draft 本身 kernel 路径已合理：5 个 GEMM 里 3 个（o/gate_up/down）命中 b12x dispatch，2 个（fc/qkv_eagle）在 MARLIN_UPPER 外 M>48 会掉 cutlass —— 但 draft 天花板 4.7% × 受影响比例 16% = **最多 0.1-0.2% e2e 收益**，不值。
157	
158	**B. target 10.6 ms/replay 的 GPU 时间分布**（nsys 30s 窗口总 2073 ms GPU 活跃时间）：
159	
160	| kernel 类别 | total ms | % |
161	|---|---|---|
162	| `at::index_elementwise_kernel` (index get，60us avg × 13652 calls) | 817.7 | **39.4%** |
163	| `at::index_elementwise_kernel` (index_put，194us avg × 4079 calls) | 791.8 | **38.2%** |
164	| b12x `DenseGemmKernel` | 77.8 | 3.8% |
165	| CUTLASS `GemmUniversal` | 50.7 | 2.4% |
166	| `fused_recurrent_fwd_kernel` (GLA) | 23.8 | 1.1% |
167	| Marlin GEMM | 22.7 | 1.1% |
168	| CatArray concat / fill / rms_norm / silu / cub reduce / ... | ~288 | ~13% |
169	
170	**GEMM 全家（b12x + CUTLASS + Marlin）合计 151 ms，仅 7.3%**。我们之前花大力气调 b12x dispatch 只在优化不到 8% 的蛋糕。
171	
172	**两个 `at::index_elementwise_kernel` 实例合计 1609 ms = 77.6% GPU 时间** —— 是 Python `x[mask] = val` / `x[idx]` 这类带 bool/advanced index 的切片赋值。
173	
174	### 定位源头（已完成 — 2026-04-22 晚）
175	
176	**第四轮定位（成功）**：把 NVTX 扩到 `EAGLEWorker.forward_batch_generation` 等各模块（20+ 个 range）。结果：
177	
178	| NVTX range | get<4> 次/ms | put<4> 次/ms | 小计 ms | 占比 |
179	|---|---|---|---|---|
180	| **`alloc_sparse_new_positions`** | **3626 / 300** | **1781 / 333** | **633** | **52.8%** |
181	| `DEAD_graph_replay`（draft_extend replay 周围 eager）| 1869 / 155 | 748 / 240 | 395 | 32.9% |
182	| `EW_verify` 顶层残余 | 2339 / 52 | 129 / 0.2 | 52 | 4.3% |
183	| `EW_draft_extend_after_decode` 顶层残余 | 479 / 37 | 18 / 5.8 | 43 | 3.6% |
184	| `DEAD_prepare_extend`（prepare_extend_after_decode）| 372 / 30 | 9 / 0.5 | 31 | 2.6% |
185	| `verify_kv_evict_mask` + `vkev_*` | 1816 / 3.3 | 0 | 3.3 | 0.3% |
186	| `fwd_extend_L*` 各层 | 0 | 144 / 0.8 | 0.8 | 0.1% |
187	| 其他 | <10 ms | <10 ms | <10 | <1% |
188	
189	**总 index kernel 时间 1200 ms = 1200 / 2074 = 57.9%**（本轮 trace 短、比例与旧 trace 略差异，量级一致）。
190	
191	**第一次"锁定"（错误 — GPU end-time 归因污染）**：`eagle_worker.py:1034 _alloc_sparse_for_new_positions`
192	
193	```python
194	for i in range(bs):                                              # per-request
195	    for sl in range(max(old_sl + 1, kernel_size), new_sl + 1):   # per-new-position
196	        if (sl - kernel_size) % kernel_stride == 0:
197	            loc = alloc_token_slots(batch.tree_cache, 1)         # GPU alloc 1 slot!
198	            rtp.write_sparse_k1(
199	                (batch.req_pool_indices[i], (k1_idx, k1_idx + 1)),
200	                loc.to(torch.int32),
201	            )
202	    # k2 同理（kernel_size*4 / kernel_stride*4）
203	```
204	
205	**为什么是它**：
206	- Python 双重循环，bs × new_positions 次迭代
207	- 每次 `alloc_token_slots(1)` 读 int32 free list → **`index_kernel<4>`**（element size=4 bytes）
208	- 每次 `write_sparse_k1` 做 `req_to_sparse_k1_token[indices] = values`（`memory_pool.py:570-574`），int32 tensor 的 advanced-indexing 写 → **`index_put<4>`**
209	- spec decoding 每步接受 3-4 个 token × 8 reqs × 1009 verify 步 × 概率过 stride 阈值 → 5407 次微 op
210	- **MiniCPM-SALA 特有代码，非 sglang 原生**。EAGLE 跳过了正常 decode 的 batch alloc 路径，这里是补救；但逐 token 分配在 spec 场景下放大成了热点
211	
212	按此结论写了批量化 fix（CPU 聚合 + 一次 alloc + per-req slice 写）。smoke + 10000 次 fuzz 对照过，代码正确。但 mini_bench e2e **无感提升**。
213	
214	**第二次验证（CPU launch-time 归因 — 正确结论）**：
215	
216	改用 `CUPTI_ACTIVITY_KIND_RUNTIME.start`（kernel **CPU launch** 时间）替代 `CUPTI_ACTIVITY_KIND_KERNEL.end`（GPU 执行 end 时间）重做归因：
217	
218	| NVTX range (launch-time 归因) | get<4> 次/ms | put<4> 次/ms | 小计 ms | 占比 |
219	|---|---|---|---|---|
220	| **`mamba_verify_update`** | **9977 / 603** | **1814 / 578** | **1181** | **98.4%** |
221	| `EW_verify` 顶层残余 | 1936 / 8.8 | — | 8.8 | 0.7% |
222	| `vkev_ai_boolmask` (line 510) | 908 / 2.2 | — | 2.2 | 0.2% |
223	| `vkev_verified_id` (line 511) | 908 / 1.1 | — | 1.1 | 0.1% |
224	| `alloc_sparse_new_positions` | — | 874 / 1.2 | 1.2 | 0.1% ← **不是热点** |
225	| 其他 | ~120 | ~110 | ~1 | <0.1% |
226	
227	**真正的主源**：`hybrid_linear_attn_backend.py:1628 update_mamba_state_after_mtp_verify` — **1181ms / 98.4%**。
228	
229	**为什么之前误判（重中之重的教训）**：
230	1. `_mamba_verify_update` 在 `worker.verify()` 里 **launch** 一大波 3D fancy-index kernel 到默认 stream
231	2. 这些 kernel 在 GPU 侧排队，**执行时间远晚于 launch**（几百 us 到几 ms）
232	3. Python 继续往下走，push 下一个 NVTX：`alloc_sparse_new_positions`
233	4. 原 `_alloc_sparse_for_new_positions` 本身 CPU 循环耗时几 ms，期间 GPU 正在消化刚才 mamba 那批 kernel
234	5. nsys 归因默认用 kernel **GPU end-time** 对应 NVTX CPU 时间窗 → mamba 的 kernel 被张冠李戴到 alloc_sparse 名下
235	
236	**检验办法**：用 `correlationId JOIN CUPTI_ACTIVITY_KIND_RUNTIME` 拿 **launch 的 CPU 时间**，一目了然。
237	
238	**`update_mamba_state_after_mtp_verify` 代码本体**（`hybrid_linear_attn_backend.py:1665+`）：
239	
240	```python
241	# SALA 的 24 层 GLA 也走这里（SimpleGLAAttnBackend 继承自 MambaAttnBackendBase）
242	ssm_states[:, dst_state_indices, :] = intermediate_state_cache[
243	    :, src_state_indices, last_steps
244	].to(ssm_states.dtype, copy=False)
245	
246	if conv_states is not None:  # SALA 无 conv
247	    conv_states[:, dst_state_indices, :] = intermediate_conv_window_cache[
248	        :, src_state_indices, last_steps
249	    ].to(conv_states.dtype, copy=False)
250	
251	if mamba_track_indices is not None:  # enable_mamba_extra_buffer 时再 ×2
252	    ssm_states[:, dst_track_indices, :] = intermediate_state_cache[
253	        :, src_track_indices, track_steps
254	    ].to(ssm_states.dtype, copy=False)
255	```
256	
257	`ssm_states` shape `[layers, slots, state_dim]`；`[:, indices_1d, scalar_1d]` 属于 **3D fancy indexing** → 一次调用 1 个 `index_kernel<4>`（read）+ 1 个 `index_put<4>`（write）。1009 verify × 开启的分支数 × ≥2 读写 ≈ 10k 级别，吻合观测到的 9977 get + 1814 put（put 被 in-place scatter 合并所以少）。
258	
259	**alloc_sparse 批量化 fix 的实际影响**：
260	- CPU 端节省 ~30-50us/call Python 循环，累计 ~30ms（非关键路径，无感）
261	- GPU 端：真正 alloc_sparse 的 kernel 只有 ~1ms
262	- **保留 fix** 作为代码清理（phantom 写去除）；e2e 影响 <1%
263	- 未发布也无所谓，绝对不回滚——批量版语义等价且更干净
264	
265	### 下一步：修复候选（按实际 ROI 排序）
266	
267	> **§8 mini_bench 全景归因后的修正**：`mamba_verify_update` 真实 e2e 占比只有 **1.65%**（见下文 §8），Plan A 收益约 2%。真正的大头是 **CPU memcpy/sync 风暴（79% wall time）**，优先级反转。
268	
269	原候选列表保留作为参考：
270	1. `update_mamba_state_after_mtp_verify`（Plan A — triton 融合 scatter，预期 +2% e2e；mini_bench 下不再是第一优先级）
271	2. `DEAD_graph_replay` 395ms（launch-time 归因后可能也有污染，需重评）
272	3. `EW_verify` 顶层残余 ~9ms
273	
274	### 复现产物
275	
276	- `/tmp/sglang_prof_nvtx5.nsys-rep`·`.sqlite` — 基线 trace（未 fix + 满 NVTX）
277	- `/tmp/sglang_prof_fix.nsys-rep`·`.sqlite` — alloc_sparse fix 后（只有 alloc_sparse NVTX）
278	- `/tmp/sglang_prof_fix2.nsys-rep`·`.sqlite` — alloc_sparse fix 后 + 细粒度 `asp_k1_alloc`/`asp_k1_writes`/`asp_k2_*` NVTX
279	- `/tmp/sglang_prof_nvtx{,2,3,4}.nsys-rep` — 过程中多轮证伪
280	- `/tmp/trigger_long.py` — decode-heavy 触发脚本（8 concurrent × 24 requests × 512 max_tokens）
281	- **正确归因 SQL**（必须 join RUNTIME 拿 launch time，不可用 GPU end time）：
282	  ```sql
283	  SELECT k.demangledName, r.start AS launch_cpu, k.end-k.start AS dur
284	  FROM CUPTI_ACTIVITY_KIND_KERNEL k
285	  JOIN CUPTI_ACTIVITY_KIND_RUNTIME r ON k.correlationId = r.correlationId
286	  WHERE k.demangledName IN (...);
287	  ```
288	  Python 侧 `bisect` 把 `launch_cpu` 落入 NVTX range，再按 innermost range 归因。
289	- 代码：各文件（`eagle_worker.py`、`eagle_info.py`、`multi_layer_eagle_worker.py`、`minicpm_sparse_utils.py`、`minicpm_backend.py`）均已加 NVTX range 插桩，保留作常备诊断工具；如需启用可加 `SGLANG_NVTX_PROFILE=1` 门控。
290	
291	### 结论（修正版）
292	
293	1. **Draft 不是瓶颈**（4.7%）；kernel/quant 替换 ROI < 1%，不做
294	2. **GEMM 不是瓶颈**（7.3%）；b12x 的 28% GEMM 省 ≈ 2% e2e，已完成工作保留
295	3. **Index 操作占 57~78% 属实**，但真正主源是 **`update_mamba_state_after_mtp_verify`（1181ms / 98.4%）**，不是之前误报的 `_alloc_sparse_for_new_positions`
296	4. **`_alloc_sparse_for_new_positions` 批量化 fix** 属于代码清理/副产品，e2e 无感。已合入
297	5. **下一步**：把 `update_mamba_state_after_mtp_verify` 的 4 次 3D fancy scatter 融成一个 triton kernel（或审视 SALA 是否该走 Mamba 的 state rollback 路径）
298	
299	**教训**（重中之重）：
300	- **NVTX range + CUDA 异步的时序陷阱**：NVTX push/pop 只标 CPU 时间窗；CUDA kernel 的 GPU end-time 可能在 launch 之后几 ms。用 GPU end-time 匹配 NVTX 会严重偏移大量 kernel 的归因。**必须 join RUNTIME_API 拿 launch CPU 时间** 才是正确归因方式。
301	- 得出"是这个函数"结论前，先做 end-time vs launch-time 对比 sanity check —— 两者 top range 若差异巨大说明有时序污染
302	- CUDA graph `graphId` 列一次性排除"卡在 graph 里"的假设，比继续加 NVTX 高效
303	- 优化 GEMM backend 之前应先 kernel-level profile 确认大头（原结论仍然成立）
304	- **SALA 特有性这次表现为**：GLA 被归到 `MambaAttnBackendBase` 的 verify 后处理路径，命中 sglang 为通用 Mamba 写的 3D fancy scatter，不是 SALA 本身的 bug
305	
306	## 8. mini_bench 全景归因（2026-04-22 晚）
307	
308	### 目的
309	
310	§7 的 "98.4% / 1181ms" 是 **stress workload** 下 verify 期 **index_kernel 这一类里**的占比，**不是 e2e 占比**。mini_bench（S1=3 S8=8，贴近正式评测的 workload）重测，得到真实量级。
311	
312	### 方法
313	
314	同 §7（nsys + NVTX + launch-time 归因），但 workload 换成 mini_bench。Profile 窗 337 s（覆盖 S1 152s + S8 177s decode 全程）。
315	
316	```bash
317	# 样本
318	python3 /tmp/mini_sample.py          # 生成 /tmp/mini_s{1,8}.jsonl
319	# server 在 nsys 下启动，/start_profile(CUDA_PROFILER) → mini_bench → /stop_profile
320	bash /tmp/nsys_start_mini.sh         # EAGLE3 生产配置
321	SPEED_DATA_S1=/tmp/mini_s1.jsonl SPEED_DATA_S8=/tmp/mini_s8.jsonl \
322	  bash /user_4813494d/openbmb/toolkit/bench_serving.sh http://127.0.0.1:30000
323	# 导出 & 归因
324	nsys export --type sqlite -o /tmp/sglang_prof_mini.sqlite /tmp/sglang_prof_mini.nsys-rep
325	python3 /tmp/analyze_mini.py
326	python3 /tmp/top_hotspots.py
327	```
328	
329	### 结果 — GPU 只占 18.5%，CPU 在等
330	
331	**GPU top（337s profile 窗口占比）**：
332	
333	| kernel | calls | GPU ms | %e2e | 备注 |
334	|---|---|---|---|---|
335	| `cutlass::device_kernel`（NVFP4 GEMM） | 15,510 | 18,685 | **5.54** | b12x 已优化 |
336	| `BatchPrefillWithPagedKVCacheKernel` | 840 | 11,683 | 3.47 | flashinfer prefill |
337	| `index_elementwise_kernel` | 607k | 6,455 | 1.91 | 5.28s 归 `mamba_verify_update`，1.17s 别处 |
338	| `vectorized_elementwise_kernel` | 543k | 3,717 | 1.10 | 通用 pointwise |
339	| `flash_fwd_splitkv_stage1_kernel` | 752 | 3,248 | 0.96 | decode full-attn |
340	| `generate_draft_decode_kv_indices` | 25,654 | 1,831 | 0.54 | — |
341	| `act_and_mul_kernel` | 3,102 | 1,779 | 0.53 | — |
342	| `RMSNormKernel` | 13,066 | 1,721 | 0.51 | — |
343	
344	**GPU 总活跃 62,469 ms / 337 s = 18.5% → 其余 81.5% 是 CPU 或空转**
345	
346	### CPU top — **memcpy + sync 风暴（79%）**
347	
348	| API | calls | CPU ms | %window |
349	|---|---|---|---|
350	| **`cudaMemcpyAsync`** | **1,416,819** | **212,556** | **63.1%** |
351	| `cudaStreamSynchronize` | 631,088 | 53,818 | 16.0% |
352	| `cudaLaunchKernel` | 3,005,571 | 9,049 | 2.7% |
353	
354	- 1.4M 次 memcpy / 337s = **4,200/sec**，每 decode round 80-100 次
355	- 平均 150μs CPU / 次 —— 名字叫 Async 但实际 **同步等待**（小张量 D2H readback 典型特征）
356	- memcpy GPU 侧总共只有 864ms（0.26%），**99.6% 的 memcpy 时间花在 CPU 等**
357	
358	### `update_mamba_state_after_mtp_verify` 真实占比
359	
360	| 子 range | CPU 墙时 | GPU 时间 | %e2e |
361	|---|---|---|---|
362	| `mamba_verify_update`（顶层） | 5,405 ms | 5,577 ms | **1.65** |
363	| └ `mv_prep_indices`（Python 打掩码 + cast） | 3,552 ms | 384 ms | 1.05（CPU 主导）|
364	| └ `mv_main_ssm_scatter`（fancy gather+scatter） | 1,484 ms | 5,177 ms | 1.54（GPU 主导）|
365	| └ `mv_track_*`（interval=256，低频） | — | — | 0 触发 |
366	
367	**Plan A triton 融合 kernel 预期收益 ≈ 2% e2e**，远小于 memcpy 风暴。
368	
369	### 优先级反转
370	
371	| 方向 | 预期收益 | 复杂度 |
372	|---|---|---|
373	| **根治 memcpy/sync 风暴** | **5~15% e2e** | 高（源头排查 + 逐点治理）|
374	| Plan A mamba scatter triton | ~2% e2e | 中 |
375	| CUTLASS GEMM 再优化 | <1% | 极高 |
376	
377	**决定**：放下 Plan A，先排查 1.4M 次 memcpy 的源头分布。候选入口：scheduler loop / spec_info 构建 / forward_metadata 准备 / sample readback。
378	
379	### 复现产物
380	
381	- `/tmp/sglang_prof_mini.nsys-rep` · `.sqlite`（323 MB / 835 MB）
382	- `/tmp/mini_sample.py`·`/tmp/nsys_start_mini.sh`·`/tmp/analyze_mini.py`·`/tmp/top_hotspots.py`
383	- `hybrid_linear_attn_backend.py:update_mamba_state_after_mtp_verify` 已加 `mamba_verify_update` / `mv_prep_indices` / `mv_main_ssm_scatter` / `mv_main_conv_scatter` / `mv_track_*` NVTX（保留作常备诊断工具）
384	
385	## 9. memcpy storm 源头锁定 —— `accept_index/predict.tolist()`（2026-04-22 晚 II）
386	
387	> **⚠️ 2026-04-23 复盘**：本节的 "memcpy 优化 ROI 5-9% e2e" 估算**错了**。按 §9 方案（fuse + pinned + non-blocking + event 重叠）实际改了代码跑 profile + e2e：
388	> - profile：`EI_ai_tolist` CPU 墙时 277,581 ms → 545 ms（-99.8%）✅ 账面完美
389	> - **e2e：S8 无收益（甚至略降）** ❌
390	>
391	> 原因：`.tolist()` 的 4ms "CPU 阻塞" **是 target_forward GPU kernel 占 critical path 的 CPU 侧影像，不是独立可压的 CPU 工作**。换成 `event.synchronize()` 只是把等待从一个 API 挪到另一个 API，wall time 不变。
392	>
393	> 修复代码已 revert。方法论教训与权威出处见 **§10**。
394	> **本节的数据仍有价值**（attribution 正确、定位到 `EI_ai_tolist`），**但"打它能收 ROI" 这个结论被证伪**。
395	
396	### 关键修正：nvitop 89% 和 profile 18.5% 并不矛盾
397	
398	nsys 默认 `--cuda-graph-trace=graph` **不展开 graph 内部 kernel**，全部 KERNEL 行 `graphNodeId IS NULL`（经 SQL 验证）。
399	
400	- decode forward 全部在 CUDA graph 内 → kernel 对 profile 不可见 → 看起来 GPU 只有 4%
401	- prefill eager shape 动态，不入 graph → kernel 正常可见 → 看起来 GPU 85-90%
402	- nvitop 采样的是**任一 kernel 是否在跑**的布尔量，在 graph 内跑 kernel 时同样显示高利用率 ✅
403	
404	**decode 时真实物理图景**：
405	- GPU 89% busy（graph 里 forward pass）
406	- CPU 74% busy（**两次 graph launch 之间疯狂 memcpy**）
407	- GPU 11% idle（就是 CPU memcpy/sync 没准备好下一个 graph 的那点空窗）
408	
409	**memcpy 优化修正 ROI：5-9% e2e**（只能填 decode 的 11% idle 窗）——不是之前估的 5-15%。仍然是第一优先级。
410	
411	### Profile 2（含更多 NVTX）: mini2
412	
413	方法同 §8，但在 `eagle_worker.verify()` / `eagle_info.verify()` / `draft()` 里加了 16 个 NVTX range 细分 memcpy 来源。
414	
415	**Profile 窗口**：`/tmp/sglang_prof_mini2.nsys-rep` (488 MB)·`sqlite`(1.26 GB)，窗口 589 s，1.98M memcpy / 875k sync / 4.27M launchKernel。
416	
417	### memcpy CPU 归因（top 10）
418	
419	| NVTX range | 调用 | mc# | mc CPU | **% of all memcpy** |
420	|---|---|---|---|---|
421	| `EW_verify`（外层） | 34,644 | 1,111,236 | 282,174 ms | **87.1%** |
422	| └ `EV_verify_accept` | 34,644 | 242,536 | 278,292 ms | 85.9% |
423	| &nbsp;&nbsp;&nbsp;└ **`EI_ai_tolist`** | **34,644** | **69,288** | **277,581 ms** | **85.7%** |
424	| `EW_draft` | 34,644 | 264,262 | 14,555 ms | 4.5% |
425	| └ `ED_replay_or_forward` | 34,644 | 242,508 | 14,459 ms | 4.5% |
426	| `EW_draft_post` | 34,644 | 554,244 | 5,492 ms | 1.7% |
427	| `EV_target_forward` | 34,644 | 632,186 | 3,093 ms | 1.0% |
428	| `mamba_verify_update` | 34,645 | 103,935 | 291 ms | 0.1% |
429	
430	（`memcpy` 列的"次数"算的是**该 range 里 cudaMemcpyAsync launch 落入的次数**；同一次 `.tolist()` 内部可能触发多次 memcpy）
431	
432	**`EI_ai_tolist` 单独 85.7%**。两行代码 `eagle_info.py:462-463`：
433	
434	```python
435	accept_index_cpu = accept_index.tolist()   # (bs, spec_steps+1) int32 ≈ 96 B
436	predict_cpu = predict.tolist()              # (bs*dtn+1,)        int32 ≈ 170 B
437	```
438	
439	- 69,288 次 cudaMemcpyAsync（每 round 2 次）= 277.6 s CPU
440	- **每次平均 4 ms CPU 阻塞**
441	- 张量 <200 B，**时间完全是在等 GPU** —— `.tolist()` 强制 sync，紧邻上游就是 `target forward CUDA graph`（decode 里最长一段 GPU 工作）
442	
443	### 为什么这两行这么狠
444	
445	```
446	target_fwd(graph, ~4ms GPU)
447	    → verify_tree_greedy (tiny)
448	    → tolist()   ← CPU 硬等 target forward 跑完（~4ms × 2 次）
449	    → pyloop (~50μs Python)
450	```
451	
452	CPU 在 tolist 里什么都没做，纯阻塞。整个 decode round TPOT 才 6 ms，两次 tolist 最坏就是 8ms（实际有部分 overlap，但累计仍占 85% memcpy 时间）。
453	
454	### 修复计划
455	
456	**目标**：消除 `accept_index.tolist() + predict.tolist()` 的 CPU 阻塞。
457	
458	设计了 3 步走方案（合并 memcpy → pinned memory 异步 copy → CPU/GPU 真正并行），预期 +5-9% e2e。**实际修改后 e2e 完全无感（S8 0 收益），修复已 revert。** 原因见 §10：`.tolist()` 的 CPU 阻塞时间是 target_forward GPU kernel 在 critical path 上的 CPU 侧影像，消掉等待只是把阻塞从一个 API 挪到另一个，wall time 不变。`EI_ai_tolist` 是主源这一 attribution 结论正确，但"打它能收 ROI"被证伪。
459	
460	### 复现产物（mini2）
461	
462	- `/tmp/sglang_prof_mini2.nsys-rep` · `.sqlite`（488 MB / 1.26 GB）
463	- `/tmp/memcpy_attrib2.py` · `/tmp/memcpy_size.py` · `/tmp/reconcile_util.py`
464	- 各文件 NVTX 插桩保留作常备诊断工具（`EW_*`、`EV_*`、`EI_*` 等 range）。
465	
466	### 教训
467	
468	- **CUDA graph + nsys**：默认 `--cuda-graph-trace=graph` 不展开 graph 内部。要看 decode 内部 kernel 需 `--cuda-graph-trace=node`。否则会把 "GPU 闲"误读。
469	- **`.tolist()` 在 GPU tensor 上 = 强制 sync**，是隐藏的 CPU 阻塞点。小张量也一样贵 —— 代价全在等 GPU queue。
470	- nvitop 的 utilization 是"任一 kernel 在跑"的布尔采样，和积分 kernel 时间语义不同，两个可以同时成立。
471	
472	## 10. 性能 profiling 方法论复盘（2026-04-23）
473	
474	§9 的修复把 `EI_ai_tolist` 从 profile 的 85.7% 打到 1.2%，但 e2e **完全无感**。这是方法论错误，不是个案失败。本节把教训和权威出处钉死，避免再踩。
475	
476	### 核心陷阱：CPU 在 sync API 里的时间 ≠ CPU 工作量
477	
478	**NVIDIA CUDA C Best Practices Guide** 原话（profiling 章节）：
479	> When using CPU timers, it is critical to remember that many CUDA API functions are asynchronous. **CPU time spent in synchronization APIs (like `cudaDeviceSynchronize()`) is actually GPU work attribution, not CPU overhead.** The true critical path emerges only after accounting for this distinction.
480	
481	补充原文：
482	> `cudaMemcpyAsync()` **requires pinned host memory** [for asynchrony]. Without pinned memory backing, async transfers may not function as intended.
483	
484	**直译到我们这次**：
485	- baseline 的 `.tolist()` 等价于 `cudaMemcpyAsync(DtoH, pageable)` = 阻塞版本
486	- 那 4ms CPU 墙时 = target_forward kernel（GPU critical path）的 CPU 侧影像
487	- 消掉这段 CPU 等待 → `event.synchronize()` 上阻塞同样 4ms（或者 CPU 空转等下一段 GPU-dep 工作）
488	- **critical path 没变 → wall time 没变**
489	- profile "变好看" 只是 attribution 改了 API，不是 wall 被压缩了
490	
491	### 用 Amdahl's Law 算 ROI 天花板（也是权威要求）
492	
493	CUDA Best Practices 章节 12（Scaling）要求在优化前就用 Amdahl 算天花板：
494	
495	$$S \le \frac{1}{(1-P) + P/N} \quad ; \quad P = \text{可并行比例}, N = \text{并行度}$$
496	
497	对我们的 decode：
498	- 真实 GPU 活跃 ~89%（nvitop），CPU-侧优化对应 "(1-P) = 11%" 段
499	- CPU-侧优化 **e2e 上限 = 1/(0.89+0.11·0) = 1.12×**，**即 ≤ 11% e2e**
500	- §9 估 "5-9%" 已经吃掉 GPU idle 上限的一半 → 需要严格证明"那 11% 里有 5-9% 是 host-wait"
501	- 当时**没证明**，直接写进文档。这是方法论事故。
502	
503	### 正确的 GPU-idle breakdown：Meta HTA 的 3 分类
504	
505	Meta **Holistic Trace Analysis** (HTA) 定义的 **Idle Time Breakdown**（PyTorch 官方博客 _Trace Analysis for the Masses_ 推荐工具）：
506	
507	1. **Host wait** — GPU 闲，因为 CPU 还没 launch 下一个 kernel → 可优化，CPU 侧可收
508	2. **Kernel wait** — GPU 闲，因为在等另一个 kernel 的依赖 → 优化 stream/graph 结构
509	3. **Unknown** — 其他（OS 调度 / 驱动开销 / PCIe 等）→ 通常硬啃不动
510	
511	**只有 (1) host-wait 才是 CPU 侧优化能收的。** 我们从未测过 host-wait 占比就直接估 "5-9%"，等于空手套白狼。
512	
513	### 决策树（从今以后按这个来）
514	
515	每次 CPU 侧优化候选出来前，必须先过：
516	
517	```
518	Step 0  nsys profile  --cuda-graph-trace=node   ← 必须 node，不能 graph
519	              ↓
520	Step 1  算 GPU 实际活跃 % = Σ(kernel_duration) / profile_window
521	              ↓
522	Step 2  GPU 活跃 ≥ 90%?
523	        ├── 是 → 纯 GPU-bound。CPU 侧再好都 ≤ 10%。
524	        │        优先攻 GPU top kernels（走 b12x / CUTLASS / Marlin 路线）
525	        │
526	        └── 否 → GPU idle > 10%，拆 idle breakdown：
527	              ↓
528	        Step 3  用 HTA 或手算：host-wait / kernel-wait / unknown
529	              ↓
530	        Step 4  host-wait 占比决定 CPU 侧 ROI 天花板
531	                host-wait < 5%  → CPU 侧不做
532	                host-wait 5-15% → 可做，但先验证目标改动能挤掉 host-wait
533	                host-wait > 15% → 值得深究
534	              ↓
535	        Step 5  改完必须 e2e 再测一遍确认 host-wait 真的下去了
536	                profile "账面变好" 不算数，只认 wall time
537	```
538	
539	### 为什么 nsys "CPU API CPU 时间" 是陷阱
540	
541	nsys 的 `CUPTI_ACTIVITY_KIND_RUNTIME` 表记的是 **CPU 线程在该 API 调用里从 entry 到 return 的 wall time**：
542	- 对 `cudaMemcpyAsync(DtoH, pageable)` → 阻塞型 API → 这段 wall = 等 GPU 的时间
543	- 对 `cudaStreamSynchronize` → 显式阻塞 → 这段 wall = 等 GPU 的时间
544	- **两者 accumulate 的 "CPU 时间" 都是 GPU 时间的投影**，**不是可优化的 CPU 工作**
545	
546	把这类 "CPU time" 当 CPU 工作优化 = 优化了也没用。
547	
548	### 正确量 GPU-idle 的操作步骤
549	
550	使用 `--cuda-graph-trace=node` 导出 SQLite 后：
551	
552	```sql
553	-- profile window
554	SELECT MIN(start), MAX(end) FROM NVTX_EVENTS WHERE text LIKE '%decode%';
555	-- 或用整个 prof window
556	
557	-- GPU 活跃时间 = Σ kernel duration
558	SELECT SUM(end-start)/1e6 AS gpu_active_ms FROM CUPTI_ACTIVITY_KIND_KERNEL;
559	
560	-- GPU-idle = window - gpu_active
561	-- gpu_active / window = 真实 GPU 利用率
562	
563	-- Host-wait proxy：统计相邻两个 kernel end-to-next-start 间隙，
564	-- 该间隙内如果 CPU 正在 cudaLaunchKernel 之外的 API 里 → 潜在 host-wait
565	-- 更精确要对齐 stream 和 CPU thread timeline（HTA 做的事）
566	```
567	
568	### 对本项目的具体决策
569	
570	- `EI_ai_tolist` 修复已 revert，code 回到 baseline（仅保留 NVTX 诊断）
571	- 后续**所有 CPU 侧候选**（`EV_free_draft_kv`、`alloc_sparse_new_positions`、`mv_prep_indices` 等）在动手前**必须**先按上面决策树跑 node-trace + idle breakdown
572	- 真正可动的方向回到 **GPU critical path kernel**：
573	  - b12x（已落地，decode GEMM -32.4%）继续 tune
574	  - `BatchPrefillWithPagedKVCacheKernel` 3.47% e2e，可看
575	  - `flash_fwd_splitkv_stage1_kernel` 0.96%，小
576	  - `update_mamba_state_after_mtp_verify` 原 Plan A triton 融合 2% e2e —— 如果 host-wait 确认 <5%，这是下一个正经目标
577	
578	### 附：未来 profile 的最低配置
579	
580	```bash
581	nsys profile -t cuda,nvtx \
582	    --cuda-graph-trace=node \           # 必须 node
583	    --cuda-event-trace=false \
584	    --capture-range=cudaProfilerApi --capture-range-end=stop \
585	    -o /tmp/prof_xxx -f true --stats=false \
586	    <server-cmd>
587	```
588	
589	导出后必跑三件事：
590	1. **GPU 活跃 %** （上面 SQL）
591	2. **Idle breakdown**（host-wait vs kernel-wait vs unknown）
592	3. **Top kernels by GPU duration**（不是 launch count、不是 CPU memcpy time）
593	
594	### 权威出处
595	
596	- NVIDIA CUDA C++ Best Practices Guide · §8（Timing） · §12（Scaling）
597	- Nsight Systems User Guide · Timeline View / NVTX integration
598	- PyTorch Blog _Trace Analysis for the Masses_
599	- Meta Holistic Trace Analysis · Idle Time Breakdown
600	
601	### 教训落地（MEMO）
602	
603	- "profile 里某 API 用了 X% CPU 时间" **不是**优化目标，目标永远是 **wall time**
604	- wall time 不动的优化 = 浪费工作 + 增加代码复杂度 + 污染未来 profile
605	- 改完第一件事是 **e2e benchmark**，profile 是辅助不是结论
606	
607	### 附录：node-trace 实测基线（2026-04-23）
608	
609	按 §10 决策树要求，用 `--cuda-graph-trace=node` 重跑 mini_bench 并做 GPU union-busy + global idle breakdown，作为后续所有 CPU/GPU 优化决策的基准：
610	
611	**Profile 窗**：584 s（覆盖 S1=8 + S8=24 全程）；`/tmp/sglang_prof_node.nsys-rep`（1.35 GB）·`.sqlite`（4.1 GB）
612	
613	**Workload 类别**：
614	
615	| 指标 | 值 | 含义 |
616	|---|---|---|
617	| GPU union-busy | **82.3%** | 任意 stream 在跑 kernel 的时间占比（和 nvitop 89% 差 6 pp 来自 node-trace profile 开销） |
618	| 全局 GPU idle | 17.7% | 所有 stream 同时空闲的时间 |
619	| **host-wait** | **9.64%** of window（= 54% of idle） | 下一个 kernel 的 CPU launch 晚于 gap 起点 → 真可 CPU-侧优化 |
620	| alloc/dep | 0.11% | launch 已入队但 GPU 未起 → stream 依赖/驱动 |
621	| tiny <10μs | 5.19% | launch 开销噪声，不可优化 |
622	| unknown | 2.77% | OS/driver/PCIe，硬啃不动 |
623	
624	**关键结论**：
625	
626	1. **workload 是 GPU-bound**（82.3% busy）→ GPU kernel 优化仍是第一优先级
627	2. **CPU 侧优化 e2e 绝对天花板 = 9.6%**（host-wait 总量）。任何 CPU 侧改动不能超过这个数字
628	3. §9 估 "5-9%" 数量级猜对了，但推理错误 —— 假定 memcpy = host-wait；`EI_ai_tolist` 修复后 e2e 0 收益证明 memcpy **不是** host-wait 主源
629	4. 9.6% host-wait 分布多处、每处很小，**没有单点能吃掉 5%+**，碎片化优化的 ROI/risk 比差
630	
631	**Top GPU kernels on main stream 7**（按 GPU 时间，未来 kernel 优化候选）：
632	
633	| kernel | calls | GPU 时间 | % window |
634	|---|---|---|---|
635	| `device_kernel`（NVFP4 GEMM） | 49,665 | 59.4 s | **10.17%** |
636	| `BatchPrefillWithPagedKVCacheKernel` | 2,683 | 37.5 s | 6.42% |
637	| `index_elementwise_kernel` | 826,622 | 15.4 s | 2.63% |
638	| `vectorized_elementwise_kernel` | 788,645 | 10.9 s | 1.87% |
639	| `flash_fwd_splitkv_stage1_kernel` | 2,408 | 10.6 s | 1.81% |
640	| `act_and_mul_kernel` | 9,933 | 5.7 s | 0.97% |
641	| `RMSNormKernel` | 41,839 | 5.4 s | 0.93% |
642	| `quantize_with_block_size_tma` | 48,675 | 4.3 s | 0.74% |
643	
644	**实操建议**：
645	- **GEMM (b12x) 继续 tune**：10.17% 最大头，且已在做
646	- **BatchPrefillWithPagedKVCacheKernel**：6.42%，长 context prefill，可看
647	- **index_elementwise_kernel**：826k 次调用，2.63%，融合/消除可节省（对应 Plan A triton scatter）
648	- CPU 侧任何改动前先证明能动 host-wait 里的某一块；不能的话别动
649	
650	**复现产物**：
651	
652	```bash
653	# node-trace profile
654	bash /tmp/nsys_start_node.sh                          # server under nsys --cuda-graph-trace=node
655	# bench + /start_profile + /stop_profile 见 /tmp/run_bench_prof.sh
656	
657	# 归因
658	python3 /tmp/gpu_union_busy.py      # 全局 busy/idle
659	python3 /tmp/gpu_global_idle.py     # idle breakdown: host-wait / alloc-dep / tiny / unknown
660	python3 /tmp/gpu_idle_breakdown.py  # 单流（stream 7）级 breakdown，用来看局部 pipeline 结构
661	python3 /tmp/host_wait_refined.py   # host-wait 再拆 REAL vs FAKE(sync) + NVTX 归因
662	python3 /tmp/idle_unknown_tiny.py   # unknown 拆 launch API、tiny <10μs 直方图
663	```
664	
665	### 10.B 深挖（2026-04-23）：17.7% idle 的 "真正可动" 比例
666	
667	Table 1 初版把 unknown 记成 2.77% "OS/driver/PCIe 硬啃不动"，把 host-wait 记成 9.64% "全可 CPU 优化"。两个都太粗。深挖一轮后的更新：
668	
669	**Unknown 16.2s 其实是分类器漏判**。原脚本只关联 `cudaLaunchKernel_v7000`，但生产路径有多种 launch API：
670	
671	| 次级 launch API | 时间 | 占 unknown |
672	|---|---|---|
673	| `cudaGraphLaunch_v10000` | 9.78s | 60.4% |
674	| `cuLaunchKernelEx`（Triton） | 3.99s | 24.6% |
675	| `cudaLaunchKernelExC_v11060` | 2.43s | 15.0% |
676	
677	这些本质是 **CUDA graph 入口和 Triton kernel 边界**，不是神秘事件，也不能被 CPU 侧优化。
678	
679	**Host-wait 9.64% 再拆（`/tmp/host_wait_refined.py`）**：
680	
681	- **FAKE (sync overlap) 0.18%**（1.03s，1.8% of HW）：gap 被 cudaStreamSync / cudaEventSync / cudaMemcpy 覆盖 → CPU 在等 GPU，是 GPU 工作伪装成 host-wait，优化无效。比例小是意外：说明 §10 主段担忧的陷阱在这一次数据里不是主因（EI_ai_tolist 情形是少数集中点）
682	- **REAL 9.47%**（55.28s，98.2% of HW）：真 CPU 侧可攻击。但**必须**再剔除 inter-request bench 间隔：
683	
684	| REAL host-wait 分布 | 时间 | 占窗口 | 性质 |
685	|---|---|---|---|
686	| `(none)` NVTX — 3 个巨型 gap（4.2s + 1.0s + 1.0s）+ 17 个 ~47ms | 22.99s | **3.94%** | bench 请求间隔，生产工作流不存在 |
687	| `EV_target_forward` | 12.25s | 2.10% | target 模型 forward，Python 层间开销 |
688	| `EW_verify` | 4.48s | 0.77% | verify 阶段 Python |
689	| `EI_evict_mask` | 3.48s | 0.60% | eviction mask 构造 |
690	| `EI_ai_tolist` | 2.57s | 0.44% | `.tolist()`（§9 验证过 fix 无收益） |
691	| `EW_draft_post` | 2.32s | 0.40% | draft 后处理 |
692	| 其他 11 个 region（每个 <0.4%） | ~7.2s | ~1.2% | 分散 |
693	
694	→ **decode 内部真可攻击 host-wait ≈ 32.3s = 5.5% of window**，不是 9.6%
695	
696	**Tiny 30.3s 的几何解读**：窗口 584s 内跑了 **3240 万个 kernel**，即 **55,515 kernels/sec**。如果每个 kernel 后面有 1μs gap → 32.4s = 5.55% 窗口 ← 和 tiny 5.19% 几乎对上。88% 的 tiny gap <1μs（avg 0.56μs），这是 CUDA 自己的 launch 延迟下限，CPU 优化吃不到。要压这一块只能减少 kernel 数量（**fusion**）或扩大 CUDA graph 覆盖范围（把更多 boundary 吞进 graph）。
697	
698	**17.7% idle 最终归类**：
699	
700	| 分量 | 占窗口 | 性质 | 可攻击？ |
701	|---|---|---|---|
702	| decode 内部真 host-wait | **~5.5%** | CPU 侧 Python / dispatch 逻辑 | 可但分散，单点 ≤2.1% |
703	| inter-request bench idle | ~3.9% | bench 请求之间空档 | 否（生产不存在） |
704	| tiny <10μs launch 下限 | 5.2% | kernel 碎片化结构性 | 只能 fusion / 扩 graph |
705	| CUDA graph / Triton launch 边界 | ~2.8% | launch 入口结构性 | 否 |
706	| 真 alloc/dep + 其他 | ~0.2% | stream 依赖 | 否 |
707	
708	**最终决策（取代 §10 主段"9.6% ROI 天花板"）**：
709	
710	1. **生产工作流下 CPU 侧 ROI 硬顶 = ~5.5%**（不是 9.6%），且 **单点最大只 2.1%**（EV_target_forward）。任何 CPU 侧大改动的 ROI/risk 都不值得做
711	2. **GPU 侧方向不变**：b12x GEMM (10.17%) + BatchPrefill (6.42%) 仍是第一优先级
712	3. **次级新信号**：kernel 数量 55k/sec → **fusion 路线天然吃得到 tiny 5.2% + 部分 target_forward Python 开销**。b12x 本身是 fused NVFP4 GEMM epilogue，恰好符合这条路径；Plan A triton scatter 同理。这两条比 "优化 CPU" 更正派
713	4. §10 主段保留当警示（CPU 时间 = GPU 归因陷阱仍然存在，EI_ai_tolist 就是样本），但 ROI 数字以 **5.5%** 为准
714
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/infllmv2-blockmask-fix.md"
}
```

> TOOL

tool_result Read
```
1	# infllmv2 blockmask batch>1 修复
2	
3	## 背景
4	
5	infllmv2 stage2 sparse attention 有两种实现路径：
6	
7	| 术语 | 含义 |
8	|---|---|
9	| **infllmv2 topk** | 原生 blockmask 路径：`topk_to_uint64` 生成位掩码，kernel 内 `fwdIterator::max_no_larger()` 位扫描跳块，只加载 topk 块的 K/V |
10	| **gather + dense FA** | 先按 topk 索引 gather K/V 到连续 buffer，再跑普通 dense FlashAttention |
11	| **FlashInfer paged** | 当前生产路径，用 FlashInfer paged attention 做 stage2 |
12	
13	infllmv2 topk 理论最优（省 gather 拷贝 + plan 开销），但 batch>1 时结果错误，一直未启用。
14	
15	## 根因
16	
17	`topk_to_uint64` 输出 blockmask 布局为 **head-major**：`(num_k_heads, batch, uint64_per_row)`。
18	
19	`fwdIterator` 构造函数（`flash_blockmask.h`）计算 `blockmask_ptr` 偏移时用了 **batch-major** 寻址，batch=1 时两种布局恰好等价，batch>1 时每个 batch 读到错误的掩码行。
20	
21	原始代码（简化）：
22	
23	```cpp
24	// 错误：batch-major 寻址
25	const int row_offset = batch_idx * params.num_k_heads * params.num_blocks_m;
26	blockmask_ptr = params.blockmask +
27	    head_idx * params.num_blocks_m * uint64_per_row +
28	    row_offset * uint64_per_row +
29	    loop_step_idx * uint64_per_row;
30	```
31	
32	问题点：
33	1. `batch_idx * num_k_heads` 是 batch-major，但数据是 head-major
34	2. `loop_step_idx` 偏移多余——同一 (batch, head) 的所有 Q token 共享同一行 topk 掩码
35	3. `num_blocks_m` 作为 head 维步长不正确，应该用 `batch`
36	
37	## 修复
38	
39	### 1. `flash_blockmask.h` — fwdIterator 寻址
40	
41	```cpp
42	// 修复后：head-major 寻址，与 topk_to_uint64 输出一致
43	const int num_blocks_n = params.num_blocks_n;
44	const int uint64_per_row = (num_blocks_n + 64 - 1) / 64;
45	
46	blockmask_ptr = params.blockmask +
47	    head_idx * params.b * uint64_per_row +
48	    batch_idx * uint64_per_row;
49	```
50	
51	- `params.b` = 原始 batch_size（seqlenq_ngroups_swapped 之前取值，始终正确）
52	- 去掉 `loop_step_idx` 偏移
53	
54	### 2. `flash_api.cpp` — num_k_heads 硬编码
55	
56	两处 `params.num_k_heads = 2;` 改为 `params.num_k_heads = num_heads_k;`：
57	- varlen fwd 路径（~line 708）
58	- kvcache fwd 路径（~line 1711）
59	
60	## seqlenq_ngroups_swapped 分析
61	
62	MQA/GQA decode 时（seqlen_q=1, nq=32, nk=2）触发 swapped 优化：
63	
64	- Q reshape: `(B, 1, 32, 128)` → `(B*16, 1, 2, 128)`
65	- `params.b` = B×16，`num_heads` = `num_heads_k` = 2
66	- grid: `(num_m_block, B*16, 2)`
67	- `bidb` = 0..B×16-1，`bidh` = 0..1
68	
69	blockmask 布局 `(2, B, U)` 需要从 swapped 的 `bidb` 还原原始 batch_idx：`bidb / ngroups`（ngroups=16）。但实际上 `params.b` 在 swapped 后 = B×16，所以 `head_idx * params.b * U` 的步长已经正确覆盖了所有 swapped batch 维度——同一原始 batch 的 16 个 group 都读到同一行掩码，这正是期望行为。
70	
71	**验证**：对于原始 batch=0 的 group g（swapped bidb=g），`blockmask_ptr = head_idx * B*16 * U + g * U`。同一原始 batch 的所有 group (0..15) 读到的是连续 16 行，但 blockmask 只有 B 行（不是 B*16 行）。
72	
73	**问题**：swapped 后 `params.b = B*16`，但 blockmask 只有 `(nk, B, U)` 即 B 行。需要用原始 batch_idx = `bidb / ngroups` 来索引。当前修复在 swapped 场景下仍有越界风险——需要进一步验证或在 swapped 路径做 `batch_idx / ngroups` 映射。
74	
75	## 验证结果（2026-04-23）
76	
77	### 部署陷阱：rebuild 未生效
78	
79	rebuild 后 `.so` 仅产出到 `packages/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so`（23 MB, Apr 23），但 Python 实际加载的是 venv site-packages 中的旧版（51 MB, Apr 20）。**所有前期"修复后仍失败"的结论均因此无效**——代码改动从未被执行过。
80	
81	修复方法：手动 `cp` 到 site-packages：
82	```bash
83	cp packages/infllmv2_cuda_impl/infllm_v2/C.cpython-310-x86_64-linux-gnu.so \
84	   $VIRTUAL_ENV/lib/python3.10/site-packages/infllm_v2/C.cpython-310-x86_64-linux-gnu.so
85	```
86	
87	提交包中 `demo-sala/prepare_env.sh:413-417` 也是 `.so` 直接替换模式：
88	```bash
89	cp "${SCRIPT_DIR}/prebuilt/infllm_v2_C.cpython-310-x86_64-linux-gnu.so" \
90	   "${VENV_SP}/infllm_v2/C.cpython-310-x86_64-linux-gnu.so"
91	```
92	所以最终修复需要更新 `demo-sala/prebuilt/` 中的 `.so`。
93	
94	### batch>1 正确性全部通过
95	
96	安装正确 `.so` 后：
97	
98	| 测试 | bs=1 | bs=2 | bs=4 | nq=16 swap |
99	|---|---|---|---|---|
100	| `diag_blockmask_allblocks.py`（全 block = dense） | OK cos=1.00 | OK cos=1.00 | OK cos=1.00 | OK cos=1.00 |
101	| `diag_blockmask_cross.py`（batch0=[0-5], batch1=[10-15]） | — | OK cos=1.00 | — | — |
102	| `test_infllmv2_precision.py` DECODE（BATCH=4, NQ=16, NK=1, K=4096~32768, topk=96） | OK | OK | OK | OK |
103	
104	交叉验证：batch[1] 输出与 batch[0] 的 topk ref 余弦为负（cos≈-0.1），确认 blockmask 正确选中了各自 batch 的 blocks。
105	
106	debug printf 确认 blockmask 寻址对齐：
107	```
108	fwdIter: bidb=0 bidh=0 params.b=4 offset=0  bm_val=0x...
109	fwdIter: bidb=1 bidh=0 params.b=4 offset=1  bm_val=0x...  (不同)
110	fwdIter: bidb=2 bidh=0 params.b=4 offset=2  bm_val=0x...  (不同)
111	fwdIter: bidb=3 bidh=0 params.b=4 offset=3  bm_val=0x...  (不同)
112	```
113	
114	### 仍需验证
115	
116	- nheads_k=2（GQA group=16）的生产形状：flash_api.cpp `num_k_heads` 修复在多 head 下是否正确
117	- seqlenq_ngroups_swapped 路径（nq=32 decode → swapped bidb 范围超过 blockmask batch 维）
118	- 长 seqlen_k（>65536）的 multi-uint64 寻址
119	
120	## Paged KV 对接问题
121	
122	### 核心矛盾
123	
124	生产 stage2 路径（`minicpm_backend.py:1393-1461`）：
125	1. `get_topk_for_sparse()` → topk_idx
126	2. `sparse_kernel_extension.get_block_table_v3()` → 展开到 token-level sparse_page_table
127	3. `FlashAttentionKernel.forward()` → `sgl_kernel.flash_attn.flash_attn_with_kvcache(page_table=sparse_page_table)`
128	
129	生产 KV pool 是 **page_size=1** paged（`minicpm_backend.py:1410 assert self.page_size == 1`）。
130	
131	infllmv2 kvcache 接口**支持 `block_table` + `topk_idx` 同时传入**（`infllmv2_sparse_attention.py:625,734`），但有硬约束：
132	```cpp
133	// flash_api.cpp:1619
134	TORCH_CHECK(!paged_KV || page_block_size % 256 == 0,
135	            "Paged KV cache block size must be divisible by 256");
136	```
137	
138	### 256 约束的原因
139	
140	`flash_fwd_kernel.h` 中 `compute_attn_1rowblock_splitkv`（line ~607）对 block_table 的使用假设：
141	
142	```cpp
143	// line 876-883: 一次 FA 迭代处理 kBlockN 个 K token
144	const int block_table_idx_cur = n_block * kBlockN / params.page_block_size;
145	// ...从单个 page 基址连续读 kBlockN 个 token
146	```
147	
148	一次 cp.async/gmem load 连续读 kBlockN × head_dim × sizeof(bf16) 字节。这要求 kBlockN 个 token 物理连续、落在同一个 page 内，即 `page_block_size >= kBlockN`。
149	
150	blockmask path 使用 kBlockN=64；标准 decode path kBlockN=128。256 = 128×2 是保守下限。
151	
152	page_size=1 时：kernel 从一个 token 的地址连续读 64 个 token，读到的 63 个是**其他请求或空闲 page 的物理内存**——完全错误。
153	
154	### 方案评估
155	
156	| 方案 | 描述 | 代价 | 当前状态 |
157	|---|---|---|---|
158	| A. 改 kernel 支持 page_block_size=1 | 在 splitkv kernel 里按 page 粒度查 block_table，每 token 独立寻址 | 改 flash_fwd_kernel.h ~4 处 pointer 计算 + gmem load 模式；**进行中** | 深入调研中 |
159	| B. 独立 256-aligned KV buffer | 稀疏 layer 单独维护连续 KV，额外拷贝 | ≈ 当前 gather 代价 | 无净收益 |
160	| C. 改 sglang page_size=256 | 全局改 | 影响所有 layer | 不现实 |
161	
162	**结论**：只有方案 A 能实现"省掉 gather + sparse_page_table 构造"的理论收益。
163	
164	## 编译注意
165	
166	修改 `flash_blockmask.h`（header）后必须清理 build 目录强制全量重编译：
167	
168	```bash
169	cd /opt/SGLang-MiniCPM-SALA/packages/infllmv2_cuda_impl
170	rm -rf build/
171	MAX_JOBS=2 python setup.py build_ext --inplace
172	```
173	
174	ninja 增量编译可能不追踪 header 依赖，导致 `.cu` 文件不重编译。
175	
176	**rebuild 后必须复制到 site-packages**（见"部署陷阱"小节）。
177	
178	## 状态
179	
180	- [x] 根因定位
181	- [x] 源码修改（3 处）
182	- [x] 清理重编译 + 正确安装到 site-packages
183	- [x] batch>1 正确性测试通过（nheads_k=1, K≤32768）
184	- [ ] nheads_k=2 GQA 生产形状正确性
185	- [ ] 清除 debug printf 后 clean rebuild
186	- [ ] 更新 `demo-sala/prebuilt/` .so
187	- [ ] 方案 A：kernel 放宽 page_block_size 限制
188	- [ ] 生产形状 benchmark（vs FA3 paged）
189	- [ ] 集成到 minicpm_backend.py
190	
191	> **关联**：NVFP4 KV cache 在 SALA 架构下无落地路径（InfLLM-v2 sparse + page_size=1 不兼容），调研见 [`nvfp4-kv-investigation.md`](../nvfp4-kv-investigation.md)。若方案 A 落地（page_block_size 放宽），需同步评估 NVFP4 KV 可行性。
192
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/cuda13-upgrade.md"
}
```

> TOOL

tool_result Read
```
1	# CUDA 12.8 → CUDA 13 升级调研
2	
3	本文档是基于对 `demo-sala/` 和 `demo-sala/sglang/` 源码的**亲自深入阅读**得出的升级可行性结论。不是二手总结。
4	
5	调研日期：2026-04-20。
6	
7	---
8	
9	## 1. 结论先行
10	
11	**无硬卡点，所有候选阻塞项都有源码/重编路径可解。**
12	
13	**主要收益窗口**：SM120 Blackwell 在 CUDA 13 + `compute_120f` 下的 CUTLASS NVFP4 GEMM 路径（cutlass#3096 实测 2.7× decode，M>48 prefill 预期 ≥20%）。
14	
15	**主要风险**：
16	1. tilelang 0.1.8（JIT 编译 sparse prefill kernel）在 cu13 Blackwell 下未经验证
17	2. FlashInfer wrapper 内部私有字段 `_paged_kv_indptr_buf` 等被我们直接访问，版本间重命名会崩
18	3. 量化流程 (`prepare_model.sh`) 在 cu13 + nvidia-modelopt 新版下需精度回归
19	
20	---
21	
22	## 2. 当前栈真相（而非 pyproject.toml 表面）
23	
24	| 层 | 真实运行版本 | 备注 |
25	|---|---|---|
26	| torch | 2.9.1+cu128 | `prepare_env.sh` 不重装 torch，继承平台 |
27	| flashinfer | **>=0.6.7**（prepare_env.sh:20 主动升级）| pyproject.toml 锁 0.5.3 是**假锁**，被 `uv pip install --no-deps -e` 绕过 |
28	| sgl-kernel | 0.3.20（pyproject 锁）| engine.py:794 真会断言；但 `common_ops.abi3.so` 被 demo-sala 覆写（prepare_env.sh:34）|
29	| cuDNN | >=9.15.0（主动升）| `nvidia-cudnn-cu12>=9.15.0` |
30	| CUDA toolkit | 12.9（RUNPATH 内嵌）| `common_ops.abi3.so` 编译时链的是 cu12.9 |
31	| tilelang | 0.1.8 | JIT 编译，跟随系统 nvcc |
32	| fla | 0.4.1 | flash-linear-attention，纯 Triton |
33	| sparse_kernel_extension | 0.0.0（`/opt/.../packages/sparse_kernel/`）| 有源码 `get_table_kernel.cu`，可重编 |
34	| nvidia-modelopt | 0.42.0 | `prepare_env.sh:13` |
35	| llmcompressor | [REDACTED] | 打了自定义 patch `gptq_quantize_fouroversix.py` |
36	
37	**engine.py 版本检查只在 `attention_backend == "flashinfer"` 时触发**（line 783）。我们用的是 `minicpm_flashinfer`，**flashinfer==0.5.3 这条断言永远不执行**。sgl-kernel==0.3.20 的断言（line 791）会触发，必须保留版本号。
38	
39	---
40	
41	## 3. 二进制依赖清单（cu13 下必须重编）
42	
43	### 3.1 `demo-sala/common_ops.abi3.so`（78 MB，2026-03-31 编译）
44	
45	- `ldd` 显示硬链 `libcudart.so.12`, `libcublas.so.12`, `libcublasLt.so.12`
46	- `RUNPATH`: `/usr/local/cuda-12.9/targets/x86_64-linux/lib` → 编译时的 cu12.9
47	- 598 个导出符号，涵盖 Marlin FP4 (`marlin_moe_wna16`), `gptq_shuffle`, `scaled_fp4_quant`, `top_k_renorm_prob`, `tree_speculative_sampling_target_only`, `verify_tree_greedy`, `segment_packbits` 等
48	
49	**重编路径**：sgl-kernel 源（GitHub sgl-project/sglang，csrc/gemm/marlin/）+ `demo-sala/patches/marlin_fp4_scale.patch`（57 行，修 FP4 kFE2M1f scale stride bug）→ cmake + ninja。
50	
51	**编译必须带**：`TORCH_CUDA_ARCH_LIST=12.0f`（**注意是 `120f` 不是 `120a`**，vllm#36865 陷阱：不写就套用非-SM120 Marlin 模板掉速）。
52	
53	### 3.2 `sparse_kernel_extension.so`
54	
55	- 硬链 libcudart.so.12
56	- **源码在** `/opt/SGLang-MiniCPM-SALA/packages/sparse_kernel/get_table_kernel.cu`，有 `setup.py`
57	- 被 `minicpm_backend.py:28, 1121, 1378` 用，提供 `get_block_table_v2/v3`
58	- cu13 下 `cd packages/sparse_kernel && python setup.py install` 即可
59	
60	### 3.3 FlashInfer JIT 缓存
61	
62	`prepare_env.sh:23` 清除 `~/.cache/flashinfer/` 后 `prewarm_flashinfer_fp4.py` 预编译 `fp4_gemm_cutlass_sm120`。cu13 下 JIT 会自动用新 nvcc 重编，**但 `prewarm_flashinfer_fp4.py:20` 硬写 `120a` 路径**，需改为 `120f`（cutlass#3096 修复要求）。
63	
64	### 3.4 `~/.cache/flashinfer/*/120a/cached_ops/fp4_gemm_cutlass_sm120/`
65	
66	`prepare_env.sh:47` 的 sed patch 给 `-DCUTLASS_ENABLE_GDC_FOR_SM100=1` 修 PDL race。cu13 + 新 FlashInfer 是否还需要这个 patch 要验证，0.6.x 可能已经在上游修了。
67	
68	---
69	
70	## 4. FlashInfer API 使用点精确清单
71	
72	### 4.1 稳定公共 API（版本间兼容性好）
73	
74	| 位置 | API | 风险 |
75	|---|---|---|
76	| `minicpm_backend.py:22` | `BatchDecodeWithPagedKVCacheWrapper`, `BatchPrefillWithPagedKVCacheWrapper` import | 低 |
77	| `minicpm_backend.py:1850-1858` | `BatchDecodeWithPagedKVCacheWrapper(ws, "NHD", use_cuda_graph=True, use_tensor_cores=True, paged_kv_indptr_buffer=..., paged_kv_indices_buffer=..., paged_kv_last_page_len_buffer=...)` | 低 |
78	| `minicpm_backend.py:1861-1874, 2069-2082` | `decode_wrapper.begin_forward(kv_indptr, kv_indices, kv_last_page_len, num_qo, num_kv, head_dim, page_size, q_data_type=, kv_data_type=, non_blocking=True)` | 低 |
79	| `minicpm_backend.py:1934-1942` | `BatchPrefillWithPagedKVCacheWrapper(ws, "NHD", use_cuda_graph=True, qo_indptr_buf, paged_kv_indptr_buf, paged_kv_indices_buf, paged_kv_last_page_len_buf)` | 低 |
80	| `minicpm_backend.py:1949-1962, 2349-2362` | `verify_wrapper.plan(qo_indptr, kv_indptr, kv_indices, kv_last_page_len, num_qo, num_kv, head_dim, page_size, q_data_type=, kv_data_type=, non_blocking=True, causal=True)` | 低 |
81	| `minicpm_attention_kernels.py:539-558` | `wrapper.forward(q, k, causal=, sm_scale=, window_left=, logits_soft_cap=)` | 低（0.6.7 加了 shape 校验，之前静默容忍的不匹配会报错） |
82	| `minicpm_attention_kernels.py:289-293` | `BatchPrefillWithPagedKVCacheWrapper(ws, "NHD", backend="fa2")` **显式指定 fa2** | **利好**：0.6.4 auto backend 改 FA2 对我们无影响（已显式） |
83	| `modelopt_quant.py:69` | `from flashinfer import fp4_quantize` | 低 |
84	| `modelopt_quant.py:77-78` | `from flashinfer import mm_fp4, reorder_rows_for_gated_act_gemm, shuffle_matrix_sf_a` | 低 |
85	| `modelopt_quant.py:90-91` | `from flashinfer.fused_moe import cutlass_fused_moe, ActivationType` | 中（非 MoE 模型未用到） |
86	
87	### 4.2 **风险点：私有字段访问**
88	
89	```python
90	# minicpm_attention_kernels.py:396-409
91	kv_indptr_shape = wrapper._paged_kv_indptr_buf.shape
92	kv_indices_shape = wrapper._paged_kv_indices_buf.shape
93	kv_last_page_len_shape = wrapper._paged_kv_last_page_len_buf.shape
94	# 还直接赋值使用
95	kv_indptr = wrapper._paged_kv_indptr_buf
96	kv_indices = wrapper._paged_kv_indices_buf
97	kv_last_page_len = wrapper._paged_kv_last_page_len_buf
98	```
99	
100	这三个下划线前缀字段是 FlashInfer wrapper 的**内部实现**，任何版本可以重命名。升级后必须手动验证这三个属性仍然存在且语义一致；否则要改。
101	
102	### 4.3 EAGLE draft 路径 FlashInfer 依赖
103	
104	`prepare_env.sh:63` 的 `SGLANG_SERVER_ARGS` 包含 `--speculative-draft-attention-backend flashinfer`。draft 走 stock FlashInfer 路径（非 minicpm_flashinfer），依赖：
105	
106	- `sgl_kernel.top_k_renorm_prob` (eagle_info.py:65)
107	- `sgl_kernel.tree_speculative_sampling_target_only` (eagle_info.py:67)
108	- `sgl_kernel.segment_packbits` (eagle_worker.py:78)
109	- `sgl_kernel.verify_tree_greedy` (eagle_utils.py:173)
110	- `sgl_kernel.fast_topk` (spec_utils.py:35)
111	
112	这些在 `common_ops.abi3.so` 里，重编 .so 就解决。
113	
114	---
115	
116	## 5. `kv_block_scales → kv_cache_sf` 影响
117	
118	**全项目 grep 结果：0 处使用**（`demo-sala/` 下没有任何 `kv_block_scales` 或 `kv_cache_sf` 字符串）。
119	
120	FlashInfer 0.6.8 的这个重命名**不影响本项目**。之前的判断有误，更正。
121	
122	---
123	
124	## 6. 非二进制改造清单
125	
126	### 6.1 必改（否则启动失败）
127	
128	| 文件 | 行 | 改动 |
129	|---|---|---|
130	| `demo-sala/sglang/python/pyproject.toml` | 30-31 | `flashinfer_python==0.5.3` → `>=0.6.8.post1`（但因 `--no-deps` 安装可不改，实际不生效）|
131	| `demo-sala/prepare_env.sh` | 16 | `nvidia-cudnn-cu12` → `nvidia-cudnn-cu13` |
132	| `demo-sala/prepare_env.sh` | 20 | `flashinfer-python>=0.6.7` → `>=0.6.8.post1`（建议升到最新）|
133	| `demo-sala/prepare_env.sh` | 32 | `common_ops.abi3.so` 路径仍叫 `sm100/common_ops.abi3.so`（这是 sgl-kernel 内部包目录名，与 arch 无关，不改）|
134	| `demo-sala/prewarm_flashinfer_fp4.py` | 20 | `"*/120a/cached_ops/..."` → `"*/120f/cached_ops/..."` 或 glob 模式 |
135	| `demo-sala/sglang/python/sglang/srt/utils/common.py` | 288 | `is_nvidia_cublas_cu12_version_ge_12_9` 改成 `_cu13` 或做兼容 |
136	| `server_args.py` | 4847 | `pip install nvidia-cudnn-cu12==[REDACTED]` → cu13 版本 |
137	
138	### 6.2 必验证（不改也可能跑但行为变）
139	
140	| 文件 | 点 | 验证内容 |
141	|---|---|---|
142	| `minicpm_attention_kernels.py` | 396-409 | `_paged_kv_*_buf` 私有字段仍存在 |
143	| `prepare_env.sh` | 43-48 | `CUTLASS_ENABLE_GDC_FOR_SM100=1` patch 是否还需要（0.6.x 可能上游已修） |
144	| `modelopt_quant.py` | 68-71 | `is_sm120_supported()` 返回 True 时走 `flashinfer.fp4_quantize`，cu13 下此函数路径是否仍正确（FlashInfer 0.6.x NVFP4 swizzle 变化） |
145	| `simple_gla_decode_kernel.py` | 124 | `num_warps=8` 硬写，Triton 3.x + cu13 下可能不是最优（非硬阻塞） |
146	| `minicpm_fuse_kernel.py` | 全文 | tilelang JIT 在 cu13 Blackwell 下能编译 + 正确性 |
147	
148	### 6.3 可选（拿满收益）
149	
150	- `FLASHINFER_FP4_GEMM_BACKEND` 环境变量可选 "cutlass" / "trtllm"，cu13 下 trtllm 路径在 Blackwell 上可能更快，值得 A/B
151	- GLA kernel 加 `@triton.autotune` 让它自己找 Blackwell 最优 num_warps
152	- `SGLANG_MARLIN_DECODE_THRESHOLD=48` 在 cu13 下重新 sweep（CUTLASS NVFP4 变快可能需要降低阈值让更多走 CUTLASS）
153	
154	---
155	
156	## 7. 收益/风险量化
157	
158	| 路径 | 当前 (cu12.8) | cu13 预期 | 依据 |
159	|---|---|---|---|
160	| CUTLASS NVFP4 GEMM（M>48, prefill 主导）| baseline | **+30~100%** | cutlass#3096 实测 `compute_120a` 14.6 → `compute_120f` 39.0 tok/s (2.7×)；FlashInfer 0.6.6+ 启用 SM120 编译；CUDA 13.2 cuBLASLt NVFP4 Grouped GEMM +20% |
161	| Marlin FP4 W4A16（M≤48, decode 主导）| baseline | **+0~17%** | vllm 论坛实测 SM120+cu13 NVFP4 Marlin vs AWQ Marlin +17%（同场景实测） |
162	| FlashInfer attention decode | baseline | **+0~10%** | 0.6.8 post1 发布 2 天，SM120 tile filter 改进 |
163	| Triton kernel（GLA, sparse）| baseline | **持平~±5%** | nvcc 13 PTX lowering 对 sm_120 更成熟，但硬写 num_warps=8 限制了收益 |
164	| tilelang sparse prefill | baseline | **未知** | JIT 在 cu13 Blackwell 未验证，可能崩（tilelang 0.1.8 是较早版本） |
165	
166	**mini_bench 预期**：S1=192.04s → 150-175s（-10~20%），S8=230.42s → 180-210s（-10~20%）。
167	
168	**关键保守派情景**：tilelang 0.1.8 在 cu13 下编不出来，sparse prefill 崩 → 退回 dense → S8 可能反而掉 30%+。
169	
170	---
171	
172	## 8. 执行计划（就地升级 + 全量 cu13 重编）
173	
174	**方针修正**（2026-04-20，经用户确认）：
175	- 本地即评测环境，**必须就地升级**（不开沙箱 conda env）
176	- 升级前已做**完整备份**：`/user_4813494d/backups/cu12-baseline-20260420/` + `RESTORE.sh`（6 步回滚），19GB，9 秒回滚
177	- 路径选择 **B 全量重编**（非 A 保守）：torch 2.9.1+cu128 → torch 2.11.0+cu13，所有 torch extension 重编。代价 1-2 天，换干净栈；避免 cudart 跨版本同进程共存风险
178	- **driver 不动**：当前 580.95.05 > cu13.0.0 bundle driver 580.65.06，R580 分支覆盖 cu13.x 全部
179	
180	### Stage 0 — 备份与基线（已完成 2026-04-20）
181	
182	- ✅ `/user_4813494d/backups/cu12-baseline-20260420/`：venv 11G + cuda-12.9 toolkit 7.3G + packages + flashinfer-cache + common_ops.abi3.so + sparse_kernel_extension.so + `RESTORE.sh`
183	- ✅ **cu12 kernel bench 基线**：`bench/cu12_baseline_kernels.json`（`bench/bench_kernels_cu12_baseline.py`）。4 shape × 14 M 值的 Marlin/CUTLASS 时延。关键交叉点：q/o_proj ~64、gate_proj ~48、down_proj ~128、k/v_proj 上 CUTLASS 全程领先
184	- ✅ CUDA 13.2 apt 装好（`/usr/local/cuda-13.2/`, V13.2.78，4.8G），cu12.9 保留在 `/usr/local/cuda-12/`
185	- ✅ 源：`/etc/apt/sources.list.d/cuda.list` 切清华→NVIDIA CN CDN（`developer.download.nvidia.cn`）
186	- ✅ pypi 源：清华 `mirrors.tuna.tsinghua.edu.cn/pypi/web/simple`
187	
188	### Stage 1 — cu13 编译通路门禁（已完成）
189	
190	- ✅ **1.1** `nvcc -arch=sm_120f` smoke：10 行 axpy kernel，`__CUDA_ARCH__=1200`，axpy 结果 OK（两个变体 `sm_120a`/`sm_120f` 都编得动都能跑）
191	- ✅ **1.2** cu13 wheel 可得性调研。全部依赖都有 cu13 版（见 § 9.1）
192	
193	### Stage 2 — 全量重编（✅ 完成 2026-04-20）
194	
195	| 步 | 任务 | 状态 |
196	|---|---|---|
197	| **2.1** | torch 2.11.0+cu130 + triton 3.6.0 + cudnn [REDACTED] | ✅ GPU matmul smoke 通过 |
198	| **2.2** | sparse_kernel_extension 重编 | ✅ `.cpython-310.so` 覆盖安装，3 API 导出 |
199	| **2.3** | infllm_v2 重编 | ✅ **遇坑**：bundled CUTLASS 3.6 `cuda_host_adapter.hpp` guard `MAJOR>=12 && MINOR>=5` 在 cu13.2 下失败，改 `MAJOR>=13 \|\| (MAJOR==12 && MINOR>=5)`；MAX_JOBS=4 过（cgroup 64GB 限制，>4 会被杀）|
200	| **2.4** | sgl-kernel `common_ops_sm100_build` 精准重编 | ✅ **优化**：绕过 `uv pip install`，CMake + Ninja 只 build `common_ops_sm100_build`（跳过 sm90 variant / FA3 flash_ops / flashmla_ops / spatial_ops / deep_gemm_cpp，MiniCPM 路径不用）。产出 `sm100/common_ops.abi3.so` 25MB（cu12 版 78MB，单 sm_120a gencode + `--compress-mode=size`）。依赖全走 `/user_4813494d/deps/` 本地 override（8 FetchContent + FlashMLA + 5 submodule），mscclpp python bindings `OFF` 跳过 nanobind/dlpack clone |
201	| **2.5** | FlashInfer + cuDNN cu13 | ✅ flashinfer-python 0.6.8.post1[cu13] + flashinfer-cubin 0.6.8.post1；nvidia-cudnn-cu13 9.19 active；`prepare_env.sh` cu12→cu13 包名，删除 `CUTLASS_ENABLE_GDC_FOR_SM100` sed patch（0.6.8.post1 源码已内置此 flag，line 112/180/229） |
202	| **2.6** | cu13 kernel bench diff | ✅ 见下表 |
203	
204	**`common_ops_sm100_build` 内含 sm_120a fatbin**：CMakeLists:226 `-gencode=arch=compute_120a,code=sm_120a`；`load_utils.py:63-69` 按 cc 分派（`cc==90→sm90/`，其他→`sm100/`），sm100 目录命名 ≠ sm100 arch 限制。
205	
206	**cu13 vs cu12 FP4 GEMM diff**（RTX 6000D，关键形状）：
207	
208	| 路径 | 形状 | M 范围 | Δ |
209	|------|------|--------|---|
210	| Marlin FP4 decode | gate_proj 4096×16384 | M=1-8 | **-12.5%** ✅ |
211	| Marlin FP4 decode | down_proj 16384×4096 | M=1-32 | **-11%** ✅ |
212	| Marlin FP4 decode | k_proj 4096×256 | M=1-8 | -4% |
213	| Marlin FP4 decode | q_proj 4096×4096 | 全段 | ±0.3% |
214	| CUTLASS NVFP4 | k_proj 4096×256 | M=1-2 | **-21~25%** ✅ |
215	| CUTLASS NVFP4 | 其他 | 全段 | ±2% 噪声 |
216	
217	零回归（最大负向 +8% k_proj cutlass M=64，容忍内）。Marlin decode 大 MLP 形状 10-12% 提速 = S1 decode 热路径直接受益。
218	
219	**任一步无法克服 → `bash /user_4813494d/backups/cu12-baseline-20260420/RESTORE.sh` 回滚**。
220	
221	### Stage 2 坑洞/经验集
222	
223	- **cgroup 内存 64GB**：`cat /sys/fs/cgroup/memory.max = 68719476736`。本机总内存 1.5TB 但 cgroup 受限。CUDA extension 并行编译 `MAX_JOBS` 务必 ≤4（单个 nvcc + CUTLASS 重模板可能吃 8-10GB）
224	- **CUTLASS 3.6 cu13 兼容 guard bug**：`cuda_host_adapter.hpp` 的版本 guard 是 `&&` 而不是 `MAJOR>=13 \|\|` — bundled 在 infllm_v2 里的副本必须手工修。sgl-kernel 用的是 CMake 拉的 `57e3cfb4` commit（4.x 版，已修）
225	- **本地 FetchContent repo 集合**：`/user_4813494d/deps/` 下有 repo-cutlass / repo-deepgemm / repo-fmt / repo-triton / repo-flashinfer / repo-flash-attention / repo-mscclpp / repo-fast-hadamard-transform，SHA 和 sgl-kernel CMakeLists 完全对上；以后任何 sgl-kernel 类重编优先走 `-DFETCHCONTENT_SOURCE_DIR_REPO-*` 跳 GitHub
226	
227	### Stage 3 — e2e 正确性 + 速度
228	
229	**3.1 短 chat smoke**（✅ 2026-04-20）：3 条中文请求（自我介绍 / 红黑树 / Python 去重），全部说人话，无乱码。
230	
231	**3.2 长上下文 + EAGLE-3 联合**（✅ 2026-04-20）：
232	- 任务：niah（perf_public_set idx=49）
233	- `prompt_tokens=63690`，`completion_tokens=512`，端到端 **36.01s**（~33s prefill + ~3s decode）
234	- 输出：正确抽取 4 个 magic number（roasted-online/hilarious-stot/malicious-vector/animated-diction）
235	- EAGLE 稳态 `accept_len 1.45–1.48`（对齐 cu12 基线 ~1.50），`accept_rate 0.21–0.24`
236	- decode 峰值吞吐 159.49 tok/s；无 NaN / crash / OOM
237	
238	**3.3 flashinfer cu13 + sm_120 构建验证**（✅ 2026-04-20）：
239	- 预编译 cubin **sm100f family variant**（1479 个），cu13 新特性，Blackwell 家族通用
240	- JIT 本地缓存 `~/.cache/flashinfer/0.6.8.post1/120f/cached_ops/`，gencode `compute_120a,code=sm_120a`
241	- 已 JIT 构建：`fp4_gemm_cutlass_sm120.so` / `fp4_quantization_120f.so` / `batch_prefill_..._bf16.so` / `cascade.so`
242	- 运行进程 `/proc/<pid>/maps` 确认加载 `/nvidia/cu13/lib/libcublas.so.13` / `libcudart.so.13` / `libcupti.so.13`
243	
244	**3.4 剩余**：
245	- probe-sala 全量自测（无 NaN，ori_accuracy 不退）— 待跑
246	- mini_bench S1=3 / S8=8 对比 192.04s / 230.42s 基线 — 需用户授权
247	
248	**过关阈值**：S1 或 S8 提速 ≥5% 且无正确性退化 → 提交；否则 RESTORE.sh 回滚。
249	
250	### Stage 4 — Squeeze（可选，1-2 天）
251	
252	- 扫 `SGLANG_MARLIN_DECODE_THRESHOLD` 新最优值（CUTLASS NVFP4 变快可能需降低阈值让更多走 CUTLASS）
253	- GLA kernel 加 `@triton.autotune` 让它找 Blackwell 最优 num_warps
254	- `FLASHINFER_FP4_GEMM_BACKEND=trtllm` A/B
255	- 删除不再需要的 `CUTLASS_ENABLE_GDC_FOR_SM100` patch
256	
257	---
258	
259	## 9. cu13 wheel 可得性矩阵
260	
261	### 9.1 核心栈
262	
263	| 依赖 | cu12 现装 | cu13 目标 | 源 |
264	|---|---|---|---|
265	| torch | 2.9.1+cu128 | **2.11.0+cu130** | pypi 或 pytorch.org/whl/cu130 |
266	| triton | 3.5.1 | **3.6.0** | pypi |
267	| torchvision | 0.24.1 | 0.26.0+cu130 | pypi |
268	| torchaudio | 2.9.1 | 2.11.0+cu130 | pypi |
269	| nvidia-cudnn-cu13 | — | [REDACTED]（被 torch 2.11 锁定，pypi 最新 [REDACTED]）| pypi |
270	| nvidia-cublas / cudart / cufft / cufile / curand / cusolver / cusparse / cusparselt-cu13 / nccl-cu13 / nvjitlink / nvtx / nvshmem-cu13 | 内置在 torch cu12 | 独立 pypi 包 (13.x) | pypi |
271	| cuda-toolkit wheel | — | 13.0.2 pypi 壳包（与 apt 装的 /usr/local/cuda-13.2 不同路径）| pypi |
272	| flashinfer-python / flashinfer-cubin | 0.6.7.post3 | **0.6.8.post1**（py3-none-any，JIT 吃系统 nvcc）| pypi |
273	| tilelang | 0.1.8 | 0.1.8（版本不变，JIT 吃环境 nvcc）| pypi |
274	| llguidance / xgrammar / nvidia-modelopt / llmcompressor | 现版本 | 不变（纯 py 或无 cuda 链）| pypi |
275	
276	**关键**：pypi.org 上的 `torch==2.11.0`（无 `+cu130` 后缀）会自动拉取 cu13 runtime 依赖（`nvidia-cublas==[REDACTED]` 等 16 个包）。所以**不必用 pytorch.org 慢速源**，清华 pypi 镜像直装即可。
277	
278	### 9.2 自建二进制（仓库/平台有源码）
279	
280	| 物件 | 现状 | 源码位置 |
281	|---|---|---|
282	| `demo-sala/common_ops.abi3.so` (75M) | cu12.9，含 `marlin_fp4_scale.patch`（上游未合入）| `github.com/sgl-project/sglang` tag v0.3.20 子树 + `demo-sala/patches/marlin_fp4_scale.patch` |
283	| `sgl_kernel/flash_ops.abi3.so` (336M) + `sm90/common_ops.abi3.so` (252M) | cu12 平台版 | 同上（sgl-kernel 全套）|
284	| `sparse_kernel_extension.so` (360K) | cu12.9 | `/opt/SGLang-MiniCPM-SALA/packages/sparse_kernel/`（get_table_kernel.cu, setup.py）|
285	| `infllm_v2/C.cpython-310.so` (50M) | cu12 平台版 | `/opt/SGLang-MiniCPM-SALA/packages/infllmv2_cuda_impl/` + `/user_4813494d/openbmb/kernels/infllmv2_cuda_impl/`（仓库备份）|
286	| `demo-sala/data/flashinfer_cache/fp4_gemm_cutlass_sm120.so` (997K) | cu12 JIT 预热产物 | 自动重建（删 `~/.cache/flashinfer/*/120a/...`，prepare_env.sh 改成 120f 路径）|
287	
288	### 9.3 纯 Python 物件（cu 版本无关）
289	
290	| 物件 | 说明 |
291	|---|---|
292	| `demo-sala/sglang/python/`（1083 个 .py）| custom SGLang。`uv pip install --no-deps -e`。可能有 torch 2.11 API 兼容性需验证 |
293	| `demo-sala/patches/gptq_quantize_fouroversix.py` | 覆盖 llmcompressor 的 GPTQ 量化函数 |
294	| `prepare_env.sh:42-48` sed patch | 给 FlashInfer `fp4_gemm_cutlass_sm120` JIT recipe 加 `-DCUTLASS_ENABLE_GDC_FOR_SM100=1`。cu13 下 120f 路径可能不需要此 patch，重评 |
295	| `prewarm_flashinfer_fp4.py` | 硬编码 `120a/cached_ops/` 路径 → 改 `120f` |
296	
297	---
298	
299	## 10. 已消除的虚假风险
300	
301	以下几项在初轮调研中被列为风险，经亲自读代码后确认**不是问题**：
302	
303	- ❌ `flashinfer==0.5.3` 版本锁 → 是假锁（`--no-deps` + engine.py 条件检查），实际运行 >=0.6.7
304	- ❌ `kv_block_scales → kv_cache_sf` rename → 全项目 0 处使用
305	- ❌ FlashInfer 0.6.4 auto backend 切 FA2 → 我们 `backend="fa2"` 显式指定
306	- ❌ Marlin FP4 decode cu13 下崩溃 → vllm 论坛有实测 +17% 数据
307	- ❌ nvidia-modelopt/llmcompressor/compressed-tensors 在 cu13 下不可用 → 都是纯 Python 或 torch 透传
308	
309	---
310	
311	## 11. cu13 + sm_120 NVFP4 Kernel 生态调研（2026-04-20）
312	
313	网络调研 agent 扫过 TRT-LLM / FlashInfer / CUTLASS / vLLM / SGLang / DeepGEMM / Marlin / ThunderKittens 等项目 2025-11 至 2026-04 的 release / PR / issue。**只调研不改动。**
314	
315	### 11.1 按项目可用性
316	
317	| 项目 | 最新版 | cu13 + sm_120 | 对 MiniCPM 收益 | 集成难度 |
318	|---|---|---|---|---|
319	| **FlashInfer** | **0.6.8.post1** (2026-04-18) | ✅ yes | **5-15%** prefill M>48 GEMM（已装）| 已装 |
320	| **CUTLASS** | 4.4.2 (2025-03-17) | ⚠️ partial | 3-8% prefill（升 main HEAD 有 SM120f 补丁）| 中（需重编 sgl-kernel）|
321	| **SGLang main** | issue #19637 | ✅ yes | FP4 backend dispatch + modelopt 整合 | 中（cherry-pick 到 demo-sala）|
322	| **vLLM Marlin W4A8** | PR #24722 | ✅ yes | decode M≤48 可能 >1.5×（激活 8bit 省带宽）| 高（需 W4A8 calib 流程）|
323	| **TRT-LLM** | NGC 26.02 | ❌ no | SM120 NVFP4 cubin 未发布（issue #11799、#10241、#2577）| 等上游 |
324	| **DeepGEMM** | issue #236 open | ❌ no | 无 SM120 wheel，NVFP4 未落地 | 等上游 |
325	| **ThunderKittens 2.0** | 2026-01-11 | ⚠️ B200-only | 仅测 SM100（B200），SM120 需自行 port | 高 |
326	| **NVFP4 W4A4 attention** | 未发布 | — | 未查到公开实现（全部项目只有 GEMM）| — |
327	
328	### 11.2 关键发现
329	
330	**FlashInfer 0.6.8 已 port TRT-LLM SM120/121 FP4 CUTLASS GEMM 优化**——正是绕开 issue #2577 的官方路径。我们已升级 0.6.8.post1，预期 prefill M>48 GEMM 5-15% 提升已在 Stage 2.6 kernel bench 中部分体现（CUTLASS k_proj M=1-2 -21~25%）。
331	
332	**vLLM Marlin W4A8（PR #24722）** 是 decode M≤48 的高潜力选项：激活从 16bit 降到 8bit，带宽减半。值得离线 bench 对比当前 W4A16 Marlin（MiniCPM decode 热路径）。但需要 W4A8 校准流程。
333	
334	**SGLang main 的 SM120 优化计划（issue #19637）**：默认 FP4 GEMM 切到 `flashinfer_cudnn`，引入 CUTLASS NVFP4 GEMM 改进。demo-sala 分叉自 SGLang 0.5.x，差距较大；值得 cherry-pick FP4 backend dispatch 和 modelopt 整合逻辑。
335	
336	**TRT-LLM / DeepGEMM 短期不可用**：SM120 cubin 未发布，不要投入时间。
337	
338	**NVFP4 W4A4 attention 是行业空白**：所有项目都只有 GEMM 路径，注意力仍跑 bf16/fp16。短期无可用 kernel。
339	
340	### 11.3 行动建议（ROI 排序）
341	
342	1. **已完成**：FlashInfer 0.6.8.post1 升级（Stage 2.5）
343	2. **Stage 4 候选 A**：离线 bench vLLM Marlin W4A8（PR #24722）vs 当前 W4A16 Marlin，MiniCPM decode M=1-32 各形状，目标 >1.5× 再进全量 calib
344	3. **Stage 4 候选 B**：试编 CUTLASS main HEAD（非 4.4.2 tag）带 SM120f 补丁，重测 Marlin 是否回归
345	4. **Stage 4 候选 C**：cherry-pick SGLang main 的 `FP4 backend dispatch` + ModelOpt 整合到 demo-sala
346	5. **暂缓**：TRT-LLM NVFP4、DeepGEMM、ThunderKittens（全部上游未支持 sm_120）
347	
348	### 11.4 调研参考链接
349	
350	- [FlashInfer #2577](https://github.com/flashinfer-ai/flashinfer/issues/2577) — NVFP4 SM120 broken（0.6.8 已修）
351	- [CUTLASS #3096](https://github.com/NVIDIA/cutlass/issues/3096) — SM120 compute_120f fix
352	- [TRT-LLM #11799](https://github.com/NVIDIA/TensorRT-LLM/issues/11799) — SM120/121 FMHA cubins missing
353	- [TRT-LLM #10241](https://github.com/NVIDIA/TensorRT-LLM/issues/10241) — NVFP4 KV cache SM120 缺失
354	- [SGLang #19637](https://github.com/sgl-project/sglang/issues/19637) — SM120 Performance Optimization Plan
355	- [vLLM PR #24722](https://github.com/vllm-project/vllm/pull/24722) — Marlin W4A8
356	- [vLLM forum Qwen3.5 SM120 实测](https://discuss.vllm.ai/t/sm120-rtx-pro-6000-nvfp4-moe-performance-report-qwen3-5-397b/2536)
357	- [DeepGEMM #236](https://github.com/deepseek-ai/DeepGEMM/issues/236) — SM120 request open
358	- [FlashInfer CHANGELOG](https://github.com/flashinfer-ai/flashinfer/blob/main/CHANGELOG.md)
359	- [LMSYS ModelOpt quant blog (2025-12-02)](https://www.lmsys.org/blog/2025-12-02-modelopt-quantization/)
360	- [ThunderKittens 2.0 blog (2026-02-19)](https://hazyresearch.stanford.edu/blog/2026-02-19-tk-2) — B200-only
361	
362	---
363	
364	## 12. 评测环境完整升级步骤
365	
366	**起点**：评测平台与本地开发环境等价，原装 **cu12.8** 栈（torch 2.9.1+cu128 / cudnn cu12 / cuda-12.9 apt toolkit / sgl_kernel common_ops cu12 版 78MB）。目标：**就地升级到 cu13 + sm_120f + cuDNN 9.21 + FlashInfer 0.6.8.post1**，对齐本地已验证配置。
367	
368	**方案分叉**：
369	- **12.A 全量重编方案**（开发机路径，已在本地验证）：评测环境完整重跑 Stage 2 四个 build，耗时 30-60 分钟，吃 cgroup 内存 64GB
370	- **12.B no-build 线上 .so 替换方案**（提交包推荐）：所有二进制在本地预编好打进提交包，评测环境只做 pip install + 文件拷贝，**零编译**
371	
372	### 12.1 流程表（两方案共用步骤，标注差异）
373	
374	| 步 | 目的 | 12.A 全量重编 | 12.B no-build 线上 |
375	|---|---|---|---|
376	| S0 | apt 装 cuda-13.2 toolkit | 必做（编译 + nvcc JIT 兜底）| 可选（FlashInfer cache 已预热时不需 nvcc）|
377	| S1 | `update-alternatives --set cuda` → cuda-13.2 | 必做 | 必做（若装了 S0）|
378	| S2 | **清 `/etc/ld.so.conf.d/` 中 cu12 条目 + `ldconfig`** | 必做 | 必做 |
379	| S3 | `uv pip install torch==2.11.0` 拉 cu13 runtime 全家 | 必做 | 必做 |
380	| S4 | `--force-reinstall nvidia-cudnn-cu13>=9.21` | 必做 | 必做 |
381	| S5 | 卸 `nvidia-*-cu12` pip 残留（15 包） | 必做 | 必做 |
382	| S6 | `--force-reinstall` `cusparselt/nvshmem/nccl/cudnn-cu13` 修被误删 .so | 必做 | 必做 |
383	| S7a | **重编**：sparse_kernel / infllm_v2 / sgl_kernel common_ops sm100 | 必做，~25 分钟 | **跳过** |
384	| S7b | **拷贝预编 .so**：sparse / infllm_v2 / sgl_kernel common_ops sm100 | — | **必做，<5 秒** |
385	| S8a | **prewarm FlashInfer FP4 GEMM**（JIT 编 `fp4_gemm_cutlass_sm120`）| 必做，~2 分钟 | **跳过** |
386	| S8b | **拷贝预热 FlashInfer cache**（`~/.cache/flashinfer/...`）| — | **必做** |
387	| S9 | 冒烟：短 chat + 长上下文 + `mm_fp4(cudnn)+mm_fp4(cutlass)` | 必做 | 必做 |
388	
389	**跳过原因**（S0/S8a 在 no-build 下可省）：
390	- S0 apt 装 cuda-13.2：只有 S7a/S8a 的 nvcc 编译和 FlashInfer 冷启 JIT 需要。若 S7b/S8b 文件拷全，运行期只用 `libcudart.so.13`（由 S3 带的 `nvidia-cuda-runtime-cu13` 提供），不需 `/usr/local/cuda/bin/nvcc`
391	- S8a prewarm：FlashInfer 启动时若命中 `~/.cache/flashinfer/` 已编译 op 直接加载，不再 JIT
392	
393	### 12.2 脚本化命令
394	
395	```bash
396	# ------ A. apt 默认 cuda → 13.2 ------
397	update-alternatives --set cuda /usr/local/cuda-13.2   # /etc/alternatives/cuda → cuda-13.2
398	update-alternatives --set cuda-13 /usr/local/cuda-13.2
399	# 验证
400	ls -l /usr/local/cuda                                  # → /etc/alternatives/cuda → /usr/local/cuda-13.2
401	nvcc --version | grep release                          # release 13.2
402	
403	# ------ B. 清掉 ld.so.conf.d 的 cu12 条目 ------
404	# libcudart.so.12 会被 cudnn-frontend 1.22 的 "Multiple libcudart" 检测拒绝
405	mv /etc/ld.so.conf.d/988_cuda-12.conf    /etc/ld.so.conf.d/988_cuda-12.conf.disabled
406	mv /etc/ld.so.conf.d/gds-12-9.conf       /etc/ld.so.conf.d/gds-12-9.conf.disabled
407	ldconfig
408	# 验证：只能看到 libcudart.so.13，不能有 libcudart.so.12
409	ldconfig -p | grep libcudart
410	
411	# ------ C. 升级 torch 到 2.11+cu130，附带 16 个 nvidia-*-cu13 ------
412	# 清华 pypi 镜像自动把 cu13 runtime 拉下来
413	export PIP_INDEX_URL=https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
414	# 或腾讯：https://mirrors.cloud.tencent.com/pypi/simple
415	uv pip install --upgrade torch==2.11.0 torchvision torchaudio triton
416	uv pip install --upgrade flashinfer-python==0.6.8.post1 flashinfer-cubin==0.6.8.post1
417	
418	# ------ D. 强制 cuDNN 9.21（unlock mm_fp4 cudnn backend） ------
419	uv pip install --force-reinstall --no-deps "nvidia-cudnn-cu13>=9.21"
420	# 验证：cuDNN [REDACTED]
421	python3 -c "import ctypes; h=ctypes.CDLL('libcudnn.so.9'); fn=h.cudnnGetVersion; fn.restype=ctypes.c_size_t; print('cudnn:', fn())"
422	
423	# ------ E. 卸 cu12 pip 残留（15 个包） ------
424	uv pip uninstall \
425	    nvidia-cublas-cu12 nvidia-cuda-cupti-cu12 nvidia-cuda-nvrtc-cu12 \
426	    nvidia-cuda-runtime-cu12 nvidia-cudnn-cu12 nvidia-cufft-cu12 \
427	    nvidia-cufile-cu12 nvidia-curand-cu12 nvidia-cusolver-cu12 \
428	    nvidia-cusparse-cu12 nvidia-cusparselt-cu12 nvidia-nccl-cu12 \
429	    nvidia-nvjitlink-cu12 nvidia-nvshmem-cu12 nvidia-nvtx-cu12
430	
431	# ------ F. 修复共享目录被误删的 cu13 .so ------
432	# cusparselt/nvshmem/nccl/cudnn 的 cu12/cu13 包装到同一 site-packages/nvidia/<name>/lib/
433	# 卸 cu12 会删实体 .so，必须 force-reinstall cu13 恢复
434	uv pip install --force-reinstall --no-deps \
435	    "nvidia-cusparselt-cu13>=0.9.0" \
436	    "nvidia-nvshmem-cu13>=3.6.5" \
437	    "nvidia-nccl-cu13>=2.30.3" \
438	    "nvidia-cudnn-cu13>=[REDACTED]"
439	
440	# ------ G. 重编三个本地二进制 ------
441	# G1. sparse_kernel_extension
442	cd /opt/SGLang-MiniCPM-SALA/packages/sparse_kernel && python setup.py build_ext --inplace
443	cp *.so /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/
444	
445	# G2. infllm_v2（CUTLASS guard patch 必做）
446	cd /opt/SGLang-MiniCPM-SALA/packages/infllmv2_cuda_impl
447	sed -i 's@#if (CUDA_VERSION_MAJOR >= 12) && (CUDA_VERSION_MINOR >= 5)@#if (CUDA_VERSION_MAJOR >= 13) || ((CUDA_VERSION_MAJOR == 12) && (CUDA_VERSION_MINOR >= 5))@' \
448	    include/cutlass/cuda_host_adapter.hpp
449	MAX_JOBS=4 python setup.py build_ext --inplace   # cgroup 64GB，>4 会 OOM
450	
451	# G3. sgl_kernel common_ops sm100（绕 uv pip install）
452	# 预置本地 deps：/user_4813494d/deps/{cutlass,flashinfer,flash-attention,...} 对应 CMakeLists FetchContent SHA
453	cd /user_4813494d/deps/sgl-kernel-build    # 或仓库 kernels/sgl_kernel/
454	cmake -S . -B build -G Ninja \
455	    -DSGL_KERNEL_ENABLE_SM90=OFF \
456	    -DSGL_KERNEL_ENABLE_FA3=OFF \
457	    -DSGL_KERNEL_ENABLE_FLASHMLA=OFF \
458	    -DSGL_KERNEL_ENABLE_SPATIAL=OFF \
459	    -DSGL_KERNEL_ENABLE_DEEPGEMM=OFF \
460	    -DSGL_KERNEL_ENABLE_MSCCLPP_PY=OFF \
461	    -DFETCHCONTENT_SOURCE_DIR_REPO-CUTLASS=/user_4813494d/deps/repo-cutlass \
462	    -DFETCHCONTENT_SOURCE_DIR_REPO-FLASHINFER=/user_4813494d/deps/repo-flashinfer
463	ninja -C build common_ops_sm100_build -j 4
464	cp build/common_ops.abi3.so \
465	   /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/sgl_kernel/sm100/
466	
467	# ------ H. 清 FlashInfer JIT 缓存的 120a（cu12 产物） ------
468	rm -rf ~/.cache/flashinfer/*/120a/
469	# 下次进程启动会按 120f 重建（sm100f family cubin 优先；sm_120a 特化 op JIT）
470	
471	# ------ I. 冒烟 ------
472	# I1. 短 chat
473	bash /tmp/start_sglang_cu13.sh &
474	sleep 60; until curl -sf http://127.0.0.1:30000/v1/models; do sleep 2; done
475	curl -sf -X POST http://127.0.0.1:30000/v1/chat/completions -H "Content-Type: application/json" \
476	    -d '{"model":"minicpm","messages":[{"role":"user","content":"你好"}],"max_tokens":50}' \
477	    | python3 -c 'import json,sys; print(json.load(sys.stdin)["choices"][0]["message"]["content"])'
478	
479	# I2. mm_fp4 两个 backend
480	python3 -c "
481	import torch, flashinfer.gemm as G
482	from sgl_kernel import scaled_fp4_quant as q
483	a = torch.randn(64, 4096, dtype=torch.bfloat16, device='cuda')
484	b = torch.randn(4096, 4096, dtype=torch.bfloat16, device='cuda')
485	ia = torch.tensor(1.0, dtype=torch.float32, device='cuda')
486	aq, asc = q(a, ia); bq, bsc = q(b, ia)
487	alpha = torch.tensor(1.0, dtype=torch.float32, device='cuda')
488	for be in ['cutlass', 'cudnn']:
489	    out = G.mm_fp4(aq, bq.T, asc, bsc.T, alpha=alpha, out_dtype=torch.bfloat16, backend=be)
490	    torch.cuda.synchronize()
491	    print(be, out.shape, out.dtype)
492	"
493	
494	# I3. 端到端 bench（需授权）
495	bash bench/mini_bench.sh
496	```
497	
498	### 12.3 新发现（2026-04-21，本章追加动因）
499	
500	1. **cudnn-frontend 1.22 同时检测到 libcudart.so.12 和 .so.13 会硬拒**
501	   - 触发点：`mm_fp4(backend='cudnn')` → `cudnn/_compiled_module.so` 内部 dlopen + detect + raise
502	   - 症状：`RuntimeError: Multiple libcudart libraries found: libcudart.so.12 and libcudart.so.13`
503	   - 根因：apt cuda-12.9 toolkit 的 `/etc/ld.so.conf.d/988_cuda-12.conf` 把 cu12 cudart 放进 ldconfig cache
504	   - **修法**：改名 .disabled + `ldconfig`（不需要 apt purge 12.9）
505	   - 一旦清理，`ldconfig -p | grep libcudart` 只剩 .so.13，问题消失
506	
507	2. **cuDNN 9.19 → 9.21 是 sm_120 FP4 必需**
508	   - flashinfer/gemm/gemm_base.py 的 `build_cudnn_gemm_fp4_graph_override_shape` 硬编码 `backend_version >= 92100`
509	   - 9.19 下 `mm_fp4(cudnn)` 会报 "No valid engine configs for smVersion:1200"
510	   - torch 2.11 默认锁 9.19，必须 `--force-reinstall --no-deps "nvidia-cudnn-cu13>=9.21"`
511	
512	3. **共享目录包的卸载陷阱**
513	   - `nvidia-cudnn-cu12` 和 `nvidia-cudnn-cu13` 都装到 `site-packages/nvidia/cudnn/lib/`
514	   - 同样适用 cusparselt / nvshmem / nccl
515	   - 卸 cu12 会**直接删 .so 文件**（即便 cu13 还在），必须 force-reinstall cu13 恢复
516	
517	### 12.4 prepare_env.sh 需追加的动作
518	
519	本仓库 `demo-sala/prepare_env.sh` 当前是 cu12→cu13 包名替换级别。为评测环境一次通过，应追加：
520	
521	- 步骤 B（ld.so.conf 清理）— **必做**，否则 cudnn backend 永远不可用
522	- 步骤 D（cudnn 9.21 强制）
523	- 步骤 F（共享目录 force-reinstall）
524	
525	详见 § 12（本章）。
526	
527	---
528	
529	## 13. probe-sala 平台提交包（cu13 全量鉴权下载版本）
530	
531	`probe-sala/prepare_env.sh` 是针对评测平台的**一次性、无 fallback、BOS 鉴权下发**的完整 cu13 安装流水线。与 `demo-sala/prepare_env.sh`（增量升级）路径分离，专门用于**平台环境复现本地已验证栈**。
532	
533	### 13.1 四个关键设计
534	
535	1. **BOS 鉴权下载**（替代 pypi / pytorch.org 兜底）
536	   - AK 尾字母 `u` 不可省（`ALTAKeWYPVdISZK7DE1E2e32eu`）
537	   - 走 bcecmd 官方工具，credentials / config 两个文件，`[Defaults]` 段（大写 `Ak` / `Sk`）
538	   - 显式 `--conf-path ${BCE_CONF}` 传入，避开评测机 `~` 不一致
539	   - 92 个 wheel 一次性拉全（2.8 GB），缺任何一个就 `exit 1`，不走远程兜底
540	
541	2. **cu12 彻底清理**（apt resolver 走不通时）
542	   - `dpkg --purge --force-all` 绕过依赖，分 2 round（避免孤儿）
543	   - 连带删 `/usr/local/cuda-12*`, `/lib/x86_64-linux-gnu/libcudnn*.so.9*`, `/etc/ld.so.conf.d/988_cuda-12.conf`
544	   - `ldconfig -p | grep libcudart.so.12` 必须为空，否则 cudnn-frontend dlopen 会 raise
545	
546	3. **flashinfer AOT skip JIT**（评测机无需 nvcc）
547	   - 把 prebuilt `*.so` 复制到 `site-packages/flashinfer/data/aot/<name>/<name>.so`
548	   - flashinfer `JitSpec.__init__` 检测到 aot_path 存在 → `is_aot=True` → `build_and_load` 直接 `self.load(self.aot_path)`，不调 ninja
549	   - 评测环境完全不需 `CUDA_HOME` / `nvcc`，即使 apt 不装 cuda-13.2 也能运行
550	
551	4. **失败强制终止评测**（kill 平台 shell）
552	   - 检测 sourced / executed 两模式：`[ "${BASH_SOURCE[0]}" != "${0}" ]` 真 → `KILL_TARGET=$$`（sourced，直接是平台 shell），否则 `$PPID`
553	   - `die()` 发 ABORTED 邮件后 `kill -TERM ${KILL_TARGET}` → `sleep 2` → `kill -KILL`
554	   - 不能包外层 `( ... exit )` subshell，只杀 subshell 会漏过 outer platform shell
555	
556	### 13.2 Stage 顺序（强依赖链）
557	
558	| Stage | 动作 | 失败动作 |
559	|---|---|---|
560	| 0 | apt cn 镜像，unset pip index | email, 不终止 |
561	| 0.5 | BOS 拉 92 wheel → `wheels/` | `die` |
562	| 1 | cu12 purge + ldconfig 校验 | `die` |
563	| 2A | pip 卸 torch + cu12 卫星包 | 容忍 |
564	| 2A.run | cu13 runtime（cublas/cudart/cupti/nvrtc/cufft/...）→ cuDNN/NCCL/cusparselt/nvshmem | `die` |
565	| 2B | torch 2.11.0+cu130 三件套 + triton + 纯 py deps | `die` |
566	| 2C | flashinfer + 量化 + transformers | `die` |
567	| 2D | sglang server + IPC | `die` |
568	| 2E | editable sglang | `die` |
569	| 2F | `/etc/ld.so.conf.d/99_pip_nvidia_cu13.conf` + `ldconfig` | `die` |
570	| 3 | 复制 prebuilt .so（common_ops / sparse_kernel / infllm_v2） + 填充 flashinfer AOT 目录 | `die` |
571	| 4 | `verify_env.py` 11 项深度自检 | `die` |
572	| 5 | 环境 rollup 邮件（含 `nvidia-smi` / pip list / verify log） | 容忍 |
573	| 6 | 启动 BF16 server（no-spec, no-quant, 最小冒烟） | 容忍 |
574	| 7 | sleep 120 + chat probe，回传响应 | 容忍 |
575	
576	### 13.3 `verify_env.py` 11 项检查（最后把关）
577	
578	| # | 检查 | 失败含义 |
579	|---|---|---|
580	| C1 | `libcudart.so.13` 存在且无 `libcudart.so.12` 进 ldconfig | cu12 purge 残留 |
581	| C2 | pip cuDNN 9.21+（不是系统 apt） | mm_fp4 cudnn backend 不可用 |
582	| C3 | `cudnn-frontend.backend_version() >= 92100` | 系统 apt `libcudnn9-cuda-12` 在 shadow pip cu13 |
583	| C4 | torch 版本 `2.11.0+cu130` + `cuda.is_available()` + cc `(12, 0)` | torch 升级失败 |
584	| C4b | `uv pip list` 无 `-cu12` 包 | pip 层 cu12 残留 |
585	| C5 | sgl_kernel Marlin FP4 符号可导入 | common_ops.abi3.so 不匹配 torch 2.11 |
586	| C6 | sparse_kernel_extension API `get_block_table_v2/v3` | prebuilt .so 损坏 |
587	| C7 | `infllm_v2.C` 可 import | prebuilt .so 损坏 |
588	| C8 | `flashinfer.mm_fp4(..., backend='cutlass')` smoke | AOT 目录填充失败或 libcudart 解析失败 |
589	| C9 | `flashinfer.mm_fp4(..., backend='cudnn')` smoke | cuDNN 9.21 未装 / libcudart 冲突 |
590	| C10 | `import sglang` from custom editable path | Stage 2E 未生效 |
591	| C11 | `~/.cache/flashinfer/.../cached_ops/` 必备 op 全有 | cache 未正确拷贝 |
592	
593	### 13.4 交付清单（tar 内容）
594	
595	```
596	probe-sala/
597	├── prepare_env.sh             # 563 行主流水
598	├── verify_env.py              # 11 项深度自检
599	├── prepare_model.sh           # 故意 exit 1（probe 设计）
600	├── probe_email.py             # 分阶段邮件回传
601	├── bcecmd                     # 16 MB Go binary
602	├── wheels_requirements.txt    # 92 个严格 pin
603	├── download_wheels.sh         # 本地一次性下载脚本（给你用）
604	├── wheels/                    # 92 whl + 3 torch whl（平台 BOS 下发）
605	├── prebuilt/                  # common_ops / sparse_kernel / infllm_v2 / flashinfer_cache
606	├── patches/gptq_quantize_fouroversix.py
607	├── sglang/python/             # editable custom SGLang
608	└── common_ops.abi3.so         # 已 replace 过 Marlin FP4 scale bug 的版本
609	```
610	
611	最终 tar ~109 MB（不含 wheels/ 的 2.8 GB 由 BOS 下载触达）。
612	
613	### 13.5 已踩坑清单
614	
615	| 坑 | 表现 | 修法 |
616	|---|---|---|
617	| pip resolver 下 torch 2.10 CPU + 2.11 CPU 双版本 | `uv pip install` 悄悄降级 | 严格 `==` pin + `--no-deps` + `--no-index --find-links wheels/` |
618	| bcecmd "Session Token not valid" | `Sts` 行残留 | 删 `~/.go-bcecli/credentials` `Sts = bj` 那行 |
619	| bcecmd "Access Denied" | AK 少尾字母 `u` | 完整 `ALTAKeWYPVdISZK7DE1E2e32eu` |
620	| apt purge 0 removed | `libcublas-12-9 depends on cuda-toolkit-12-9-config-common` | `dpkg --purge --force-all` |
621	| verify C8 `nvcc: not found` | prebuilt `fp4_gemm_cutlass_sm120.so` 没 RPATH，JIT 触发 ninja | AOT 目录机制 skip JIT |
622	| die 后评测继续 | 外层 subshell `(exit)` 只杀 subshell | `kill -TERM $$/$PPID` with mode detection |
623	
624	---
625	
626	## 14. 关键参考链接
627	
628	- cutlass#3096：https://github.com/NVIDIA/cutlass/issues/3096 （SM120 NVFP4 MoE fix with `compute_120f`）
629	- vllm#36865：https://github.com/vllm-project/vllm/issues/36865 （cu13 源码编译未指定 `120a/120f` 掉速陷阱）
630	- flashinfer#2577：https://github.com/flashinfer-ai/flashinfer/issues/2577 （SM120 NVFP4 mm_fp4 broken in cu12，cu13 修复）
631	- vllm forum 2525：https://discuss.vllm.ai/t/sm120-rtx-pro-4000-6-5x-throughput-gain-and-v0-18-1-regression-findings/2525 （SM120 NVFP4 Marlin +17% 实测）
632	- CUDA 13.2 Release Notes：https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html
633	- zenn RTX5090 cu13 trap：https://zenn.dev/toki_mwc/articles/rtx5090-blackwell-cuda-toolkit-trap-llama-cpp （llama.cpp MMQ 在 cu13.1 崩溃的反面教材，Marlin 无此问题）
634
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/bench/mini_bench.sh"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env bash
2	set -euo pipefail
3	# =============================================================
4	# mini_bench.sh — 快速速度验证（全量 bench 的 ~25%）
5	#
6	# 用法:
7	#   bash bench/mini_bench.sh [API_BASE] [N_S1] [N_S8] [N_SMAX]
8	#
9	# 默认值:
10	#   API_BASE = http://127.0.0.1:30000
11	#   N_S1=3  N_S8=8  N_SMAX=16
12	#
13	# S8=8 恰好一个满批，能体现并发压力；Smax=16 覆盖长尾。
14	# 数据集嵌套关系: S1(8) ⊆ S8(24) ⊆ Smax(64)，每档样本唯一。
15	# 本脚本取各档前 N 条，保留与全量相同的长尾特性。
16	# =============================================================
17	
18	API_BASE="${1:-http://127.0.0.1:30000}"
19	N_S1="${2:-0}"
20	N_S8="${3:-0}"
21	N_SMAX="${4:-64}"
22	
23	BENCH_DIR="$(cd "$(dirname "$0")" && pwd)"
24	DATA_DIR="${BENCH_DIR}/data"
25	TOOLKIT_BENCH="${BENCH_DIR}/../toolkit/bench_serving.sh"
26	
27	echo "=========================================================="
28	echo "  mini_bench  S1=${N_S1}  S8=${N_S8}  Smax=${N_SMAX}"
29	echo "  API: ${API_BASE}"
30	echo "=========================================================="
31	
32	# 分层抽样到 /tmp（按 prompt_tokens 分布均匀取样，避免前段全是短请求）
33	S1_MINI="/tmp/mini_s1.jsonl"
34	S8_MINI="/tmp/mini_s8.jsonl"
35	SMAX_MINI="/tmp/mini_smax.jsonl"
36	
37	python3 - <<PY
38	import json, random
39	
40	SEED = 42
41	
42	def stratified_sample(src, dst, n):
43	    if n <= 0:
44	        open(dst, 'w').close()  # empty file
45	        return
46	    rng = random.Random(SEED)
47	    items = [json.loads(l) for l in open(src)]
48	    items.sort(key=lambda x: x['prompt_tokens'])
49	    step = len(items) / n
50	    sampled = [rng.choice(items[int(i*step):int((i+1)*step) or len(items)]) for i in range(n)]
51	    with open(dst, 'w') as f:
52	        for it in sampled:
53	            f.write(json.dumps(it, ensure_ascii=False) + '\n')
54	    pts = [it['prompt_tokens'] for it in sampled]
55	    print(f"  {dst}: n={n}, prompt avg={sum(pts)//n}, min={min(pts)}, max={max(pts)}")
56	
57	stratified_sample("${DATA_DIR}/speed_bench_c1.jsonl",         "${S1_MINI}",   ${N_S1})
58	stratified_sample("${DATA_DIR}/speed_bench_c8.jsonl",         "${S8_MINI}",   ${N_S8})
59	stratified_sample("${DATA_DIR}/speed_bench_cunlimited.jsonl", "${SMAX_MINI}", ${N_SMAX})
60	PY
61	
62	echo "  抽样完成: S1=${N_S1}条  S8=${N_S8}条  Smax=${N_SMAX}条"
63	echo ""
64	
65	SPEED_DATA_S1="${S1_MINI}" \
66	SPEED_DATA_S8="${S8_MINI}" \
67	SPEED_DATA_SMAX="${SMAX_MINI}" \
68	bash "${TOOLKIT_BENCH}" "${API_BASE}"
69
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"MARS\\|mars_theta\\|top2_ratio\\|[REDACTED] | head -30",
  "description": "Find MARS-related lines in eagle_info.py"
}
```

> TOOL

tool_result Bash
```
25:# MARS verify (arXiv:2601.15498): theta < 0 disables, default. Recommended 0.9.
26:_MARS_THETA = float(os.environ.get("EAGLE_MARS_THETA", "-1.0"))
103:    # Per-mode MARS verify theta. Negative = disabled (standard greedy verify).
104:    # Set by EAGLEWorker._apply_spec_config from EAGLE_D{5,7}_MARS_THETA env so
107:    mars_theta: float = -1.0
347:            # MARS (Margin-Aware Speculative verification, arXiv:2601.15498):
349:            # Enabled when EAGLE_MARS_THETA >= 0; default disabled (-1.0) keeps standard SD.
351:            # for dynamic D5/D7 modes). Fall back to module-level _MARS_THETA
354:            inst_theta = getattr(self, "mars_theta", -1.0)
355:            mars_theta = float(inst_theta) if inst_theta >= 0.0 else float(_MARS_THETA)
356:            if mars_theta >= 0.0:
359:                top2_token = top2.indices[..., 1].reshape(bs, self.draft_token_num).contiguous()
362:                # ratio = z2/z1 only when z1 > 0; else -1.0 (never triggers MARS)
364:                top2_ratio = ratio.reshape(bs, self.draft_token_num).contiguous().float()
368:                top2_token = None
369:                top2_ratio = None
381:                top2_token=top2_token,
382:                top2_ratio=top2_ratio,
383:                mars_theta=mars_theta,
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/b12x_fp4.py",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1	"""b12x NVFP4 GEMM integration for sm_120 MiniCPM-SALA.
2	
3	Wraps flashinfer PR #3051 Sm120BlockScaledDenseGemmKernel. Provides:
4	- lazy import (server doesn't crash if cutlass-dsl / flashinfer missing)
5	- monkey-patch of flashinfer.cute_dsl.utils with two sm120 helpers
6	- kernel compile + cache per (M_bucket, N, K, tile, use_prefetch)
7	- shape-aware optimal tile lookup derived from bench_full_matrix.json (2026-04-22)
8	- b12x_gemm_fp4() API consumed by modelopt_quant.py dispatch
9	
10	Activation requires env `CUTE_DSL_ARCH=sm_120a` (PTXAS rejects block-scaled MMA
11	without the `a` suffix). If env missing or deps missing, b12x_available()
12	returns False and modelopt_quant falls back to existing Marlin/CUTLASS hybrid.
13	"""
14	from __future__ import annotations
15	
16	import logging
17	import os
18	import threading
19	from pathlib import Path
20	from typing import Optional, Tuple
21	
22	import torch
23	
24	logger = logging.getLogger(__name__)
25	
26	# --- lazy module-level state ---
27	_INIT_LOCK = threading.Lock()
28	_INITIALIZED = False
29	_AVAILABLE = False
30	_KERNEL_CACHE: dict = {}
31	_COMPILE_LOCK = threading.Lock()
32	
33	# Exposed for testing
34	_CUTE_DSL_ARCH = os.environ.get("CUTE_DSL_ARCH", "")
35	
36	
37	# --- shape dispatch profile ---
38	
39	# Baseline is the pre-2026-04-25 b12x/Marlin split. It is kept behind an env
40	# switch so e2e comparisons can run from the same Python/CUDA artifact.
41	BASELINE_MARLIN_UPPER: dict[Tuple[int, int], int] = {
42	    (4096,   4096):   8,
43	    (4608,   4096):   8,
44	    (4096,   16384):  24,
45	    (32768,  4096):   16,
46	    (12288,  4096):   16,
47	    (4096,   12288):  16,
48	}
49	
50	BASELINE_CUTLASS_OVERRIDE: frozenset[Tuple[int, int, int]] = frozenset({
51	    (4096,  16384, 512),
52	    (32768, 4096,  8192),
53	    (4608,  4096,  8192),
54	})
55	
56	# Tuned profile, refreshed by bench_nospec_crossover.py on 2026-04-25 with
57	# activation quantization cost included.
58	TUNED_MARLIN_UPPER: dict[Tuple[int, int], int] = {
59	    (4096,   4096):   32,     # std_o
60	    (4608,   4096):   32,     # std_qkv
61	    (4096,   16384):  24,     # down
62	    (32768,  4096):   16,     # gate_up
63	    (12288,  4096):   24,     # gla_qkv
64	    (4096,   12288):  16,     # eagle_fc
65	}
66	
67	TUNED_CUTLASS_OVERRIDE: frozenset[Tuple[int, int, int]] = frozenset({
68	    (4096,  4096,  8192),  # std_o large tails/full chunk
69	    (4096,  16384, 512),   # down M=512
70	    (4096,  16384, 2048),  # down M=2048
71	    (4096,  16384, 4096),  # down M=2526/4096
72	    (12288, 4096,  2048),  # gla_qkv M=2048
73	    (32768, 4096,  8192),  # gate_up M=8192
74	    (4608,  4096,  8192),  # std_qkv M=8192
75	})
76	
77	
78	def _select_dispatch_profile() -> tuple[str, dict[Tuple[int, int], int], frozenset[Tuple[int, int, int]]]:
79	    profile = os.environ.get("SGLANG_B12X_DISPATCH_PROFILE", "tuned").strip().lower()
80	    if profile == "baseline":
81	        return profile, BASELINE_MARLIN_UPPER, BASELINE_CUTLASS_OVERRIDE
82	    if profile != "tuned":
83	        logger.warning("[b12x] unknown dispatch profile %r; using tuned", profile)
84	    return "tuned", TUNED_MARLIN_UPPER, TUNED_CUTLASS_OVERRIDE
85	
86	
87	_DISPATCH_PROFILE, MARLIN_UPPER, CUTLASS_OVERRIDE = _select_dispatch_profile()
88	
89	
90	def _try_initialize() -> bool:
91	    """One-time initialization: env check + monkey-patch + kernel import.
92	
93	    Returns True if b12x can be used, False otherwise. Safe to call multiple
94	    times; actual init runs only once.
95	    """
96	    global _INITIALIZED, _AVAILABLE
97	    if _INITIALIZED:
98	        return _AVAILABLE
99	    with _INIT_LOCK:
100	        if _INITIALIZED:
101	            return _AVAILABLE
102	        _INITIALIZED = True
103	
104	        if _CUTE_DSL_ARCH != "sm_120a":
105	            logger.info(
106	                "[b12x] disabled: CUTE_DSL_ARCH=%r (need 'sm_120a'). "
107	                "Set env and restart to enable.",
108	                _CUTE_DSL_ARCH,
109	            )
110	            return False
111	
112	        try:
113	            # Monkey-patch sm120 helpers (PR #3051 adds these; vanilla 0.6.8.post1
114	            # doesn't have them, so inject at runtime from bundled b12x/ package).
115	            from .b12x import cute_dsl_utils as _new_helpers
116	            import flashinfer.cute_dsl.utils as _fu
117	            _fu.sm120_make_smem_layout_sfa = _new_helpers.sm120_make_smem_layout_sfa
118	            _fu.sm120_make_smem_layout_sfb = _new_helpers.sm120_make_smem_layout_sfb
119	
120	            # Import the block-scaled kernel (pulled from PR #3051)
121	            from .b12x.dense_blockscaled_gemm_sm120 import (
122	                Sm120BlockScaledDenseGemmKernel,  # noqa: F401
123	            )
124	
125	            import cutlass  # noqa: F401
126	            import cutlass.cute as cute  # noqa: F401
127	            from cutlass.cute.runtime import make_ptr  # noqa: F401
128	            from flashinfer.cute_dsl.utils import get_max_active_clusters  # noqa: F401
129	        except Exception as e:
130	            logger.warning("[b12x] disabled: dependency import failed: %s", e)
131	            return False
132	
133	        _AVAILABLE = True
134	        logger.info(
135	            "[b12x] ready: sm_120a kernel enabled; profile=%s "
136	            "known_shapes=%d cutlass_overrides=%d",
137	            _DISPATCH_PROFILE,
138	            len(MARLIN_UPPER),
139	            len(CUTLASS_OVERRIDE),
140	        )
141	        return True
142	
143	
144	_PRECOMPILED = False
145	_PRECOMPILE_LOCK = threading.Lock()
146	
147	
148	def ensure_precompiled() -> None:
149	    """Precompile selected b12x kernels for the active dispatch profile.
150
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/marlin_utils_fp4.py",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	# SPDX-License-Identifier: Apache-2.0
2	# Adapted from https://github.com/sgl-project/sglang/pull/19652
3	
4	"""NVFP4 Marlin fallback: run FP4-quantized models on non-Blackwell GPUs via Marlin kernel."""
5	
6	import logging
7	from typing import Optional
8	
9	import torch
10	
11	from sglang.srt.layers.quantization.marlin_utils import (
12	    USE_FP32_REDUCE_DEFAULT,
13	    marlin_make_workspace,
14	    marlin_permute_bias,
15	    marlin_permute_scales,
16	    should_use_atomic_add_reduce,
17	)
18	from sglang.srt.layers.quantization.utils import get_scalar_types
19	from sglang.srt.utils import get_device_capability, is_blackwell_supported, is_cuda
20	
21	_is_cuda = is_cuda()
22	if _is_cuda:
23	    from sgl_kernel import gptq_marlin_gemm, gptq_marlin_repack
24	
25	ScalarType, scalar_types = get_scalar_types()
26	
27	logger = logging.getLogger(__name__)
28	
29	# NVFP4 always uses group_size=16
30	FP4_MARLIN_GROUP_SIZE = 16
31	
32	
33	def is_fp4_marlin_supported() -> bool:
34	    """当前 GPU 是否支持 FP4 Marlin fallback (CUDA SM >= 75)。"""
35	    if not _is_cuda:
36	        return False
37	    if torch.version.hip is not None:
38	        return False
39	    major, minor = get_device_capability()
40	    if major is None or minor is None:
41	        return False
42	    return (major * 10 + minor) >= 75
43	
44	
45	def should_use_fp4_marlin_fallback() -> bool:
46	    """非 Blackwell（或强制）且 SM >= 75 时返回 True。"""
47	    import os
48	    force = os.environ.get("SGLANG_FORCE_NVFP4_MARLIN", "0") == "1"
49	    return (force or not is_blackwell_supported()) and is_fp4_marlin_supported()
50	
51	
52	def nvfp4_marlin_process_scales(marlin_scales: torch.Tensor) -> torch.Tensor:
53	    """将 NVFP4 scales 从 FP8-S1E4M3 转换为 Marlin 所需的 FP8-S0E5M3 格式。"""
54	    marlin_scales = marlin_scales.to(torch.half)
55	
56	    if not (marlin_scales >= 0).all():
57	        logger.warning_once(
58	            "NVFP4 Marlin 要求 scales >= 0，但检测到负 scale，精度可能下降。"
59	        )
60	
61	    # 重排列：[0,1,2,3] -> [0,2,1,3]（每组4个，交换1和2）
62	    marlin_scales = marlin_scales.view(-1, 4)[:, [0, 2, 1, 3]].view(
63	        marlin_scales.size(0), -1
64	    )
65	
66	    # 转换 exponent bias：FP16 exponent bias=15，FP8-S0E5M3 bias=16，差值=1
67	    # 乘以 2^7 后以 int16 左移1位，再视作 float8_e4m3fn
68	    marlin_scales = (marlin_scales * (2**7)).view(torch.int16) << 1
69	    marlin_scales = marlin_scales.view(torch.float8_e4m3fn)
70	    marlin_scales = marlin_scales[:, 1::2].contiguous()
71	
72	    return marlin_scales
73	
74	
75	def nvfp4_marlin_process_global_scale(global_scale: torch.Tensor) -> torch.Tensor:
76	    """预调整 global scale 的 exponent bias 供 Marlin kernel 使用。"""
77	    assert global_scale.dtype in [torch.half, torch.bfloat16], (
78	        f"global_scale dtype 必须是 half 或 bfloat16，实际为 {global_scale.dtype}"
79	    )
80	    fp4_exponent = 2
81	    target_exponent = 5 if global_scale.dtype == torch.half else 8
82	    exponent_bias = 2 ** (target_exponent - 1) - 2 ** (fp4_exponent - 1)
83	    return global_scale * (2.0 ** (exponent_bias - 7))
84	
85	
86	def apply_fp4_marlin_linear(
87	    input: torch.Tensor,
88	    weight: torch.Tensor,
89	    weight_scale: torch.Tensor,
90	    weight_global_scale: Optional[torch.Tensor],
91	    workspace: torch.Tensor,
92	    size_n: int,
93	    size_k: int,
94	    bias: Optional[torch.Tensor] = None,
95	    use_fp32_reduce: bool = USE_FP32_REDUCE_DEFAULT,
96	) -> torch.Tensor:
97	    """通过 Marlin kernel 执行 FP4 量化 linear（非 Blackwell fallback）。"""
98	    reshaped_x = input.reshape(-1, input.shape[-1])
99	    out_shape = input.shape[:-1] + (size_n,)
100
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"tree_aware\\|tree_verify\\|retrieve_parent\\|intermediate_ssm\\|fused_recurrent_gla\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py | head -30",
  "description": "Find tree-aware verify and GLA kernel references"
}
```

> TOOL

tool_result Bash
```
56:def _fused_recurrent_gla_intermediate_kernel(
60:    retrieve_parent_token_ptr,
76:    stride_retrieve_parent_token_seq,
77:    stride_retrieve_parent_token_token,
121:        retrieve_parent_token_base = (
122:            retrieve_parent_token_ptr
123:            + (i_n * stride_retrieve_parent_token_seq)
124:            + token_indices * stride_retrieve_parent_token_token
126:        parent_idx_tokens = tl.load(retrieve_parent_token_base, mask=mask_retrieve)
163:def _fused_recurrent_gla_launch(q, k, v, g_gamma, scale, initial_state, cu_seqlens,
164:                                 o_buf, ht_buf, retrieve_parent_token=None):
188:    if retrieve_parent_token is not None:
189:        stride_retrieve_parent_token_seq = retrieve_parent_token.stride(0)
190:        [REDACTED](1)
192:        stride_retrieve_parent_token_seq = 0
193:        stride_retrieve_parent_token_token = 0
196:    _fused_recurrent_gla_intermediate_kernel[grid](
200:        retrieve_parent_token_ptr=retrieve_parent_token,
209:        stride_retrieve_parent_token_seq=stride_retrieve_parent_token_seq,
210:        [REDACTED],
213:        HAS_EAGLE_TREE_CUSTOM_ATTN_MASK=retrieve_parent_token is not None,
217:def _fused_recurrent_gla_with_intermediate(q, k, v, g_gamma, scale, initial_state, cu_seqlens,
218:                                            o_buf=None, ht_buf=None, retrieve_parent_token=None):
233:    _fused_recurrent_gla_launch(
243:        [REDACTED],
250:def _build_retrieve_parent_token(
469:        self.retrieve_parent_token_list_by_dtn: dict = {}
475:        self.retrieve_parent_token_list = []
485:        retrieve_parent_token = None
515:                        [REDACTED](retrieve_next_token)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py",
  "limit": 200,
  "offset": 150
}
```

> TOOL

tool_result Read
```
150	
151	# TODO make it true by default when the DeepEP PR is merged
152	MOE_NVFP4_DISPATCH = envs.SGLANG_MOE_NVFP4_DISPATCH.get()
153	FLASHINFER_FP4_GEMM_BACKEND = envs.SGLANG_FLASHINFER_FP4_GEMM_BACKEND.get()
154	
155	# Hybrid Marlin decode threshold: M <= threshold uses Marlin FP4 GEMV,
156	# M > threshold uses CUTLASS NVFP4 W4A4. Set via env var, 0 = disabled.
157	import os as _os
158	_MARLIN_HYBRID_THRESHOLD = int(_os.environ.get("SGLANG_MARLIN_DECODE_THRESHOLD", "0"))
159	
160	# Supported activation schemes for the current configuration
161	ACTIVATION_SCHEMES = ["static"]
162	
163	ACT_STR_TO_TYPE_MAP = {
164	    "silu": ActivationType.Swiglu,  # This is the default
165	    "relu2": ActivationType.Relu2,
166	}
167	
168	
169	class ModelOptQuantConfig(QuantizationConfig):
170	    def __init__(
171	        self,
172	        kv_cache_quant_algo: Optional[str],
173	        exclude_modules: Optional[List[str]],
174	        packed_modules_mapping: Optional[Dict[str, List[str]]],
175	    ):
176	        super().__init__()
177	        self.packed_modules_mapping = packed_modules_mapping
178	        self.exclude_modules = exclude_modules or []
179	        self.kv_cache_quant_algo = kv_cache_quant_algo
180	
181	    def _get_quant_method(
182	        self,
183	        layer: torch.nn.Module,
184	        prefix: str,
185	        *,
186	        Linear: type[LinearMethodBase],
187	        Moe: type[FusedMoEMethodBase],
188	    ) -> Optional[QuantizeMethodBase]:
189	        from sglang.srt.layers.linear import LinearBase
190	        from sglang.srt.layers.moe.fused_moe_triton import FusedMoE
191	
192	        if isinstance(layer, LinearBase):
193	            if is_layer_skipped(
194	                prefix, self.exclude_modules, self.packed_modules_mapping
195	            ) or self.is_layer_excluded(prefix):
196	                return UnquantizedLinearMethod()
197	            return Linear(self)
198	        elif self.kv_cache_quant_algo and isinstance(layer, RadixAttention):
199	            return ModelOptFp8KVCacheMethod(self)
200	        elif isinstance(layer, FusedMoE):
201	            return Moe(self)
202	        return None
203	
204	    @classmethod
205	    def get_config_filenames(cls) -> List[str]:
206	        return ["hf_quant_config.json"]
207	
208	    def get_scaled_act_names(self) -> List[str]:
209	        return []
210	
211	
212	class ModelOptFp8Config(ModelOptQuantConfig):
213	    """Configuration for ModelOpt FP8 quantization, including serialization and compatibility checks."""
214	
215	    def __init__(
216	        self,
217	        is_checkpoint_fp8_serialized: bool = False,
218	        kv_cache_quant_method: Optional[str] = None,
219	        exclude_modules: Optional[List[str]] = None,
220	        packed_modules_mapping: Optional[Dict[str, List[str]]] = None,
221	    ) -> None:
222	        """
223	        Args:
224	            is_checkpoint_fp8_serialized (bool): Indicates if the checkpoint uses serialized FP8 format.
225	        """
226	        super().__init__(kv_cache_quant_method, exclude_modules, packed_modules_mapping)
227	        self.is_checkpoint_fp8_serialized = is_checkpoint_fp8_serialized
228	        if is_checkpoint_fp8_serialized:
229	            logger.warning(
230	                "Detected ModelOpt FP8 checkpoint. The format is experimental and subject to change."
231	            )
232	
233	    @classmethod
234	    def override_quantization_method(cls, hf_quant_config, user_quant):
235	        """Override quantization method based on the model's config."""
236	        return cls._modelopt_override_quantization_method(hf_quant_config, user_quant)
237	
238	    @classmethod
239	    def get_name(cls) -> str:
240	        return "modelopt_fp8"
241	
242	    @classmethod
243	    def get_supported_act_dtypes(cls) -> List[torch.dtype]:
244	        return [torch.bfloat16, torch.half]
245	
246	    @classmethod
247	    def get_min_capability(cls) -> int:
248	        return 89  # Minimum hardware capability (e.g., Hopper GPUs).
249	
250	    @classmethod
251	    def from_config(cls, config: Dict[str, Any]) -> ModelOptFp8Config:
252	        # Handle two different config formats:
253	        # 1. hf_quant_config.json format: {"quantization": {"quant_algo": "FP8", ...}}
254	        # 2. config.json quantization_config format: {"quant_algo": "FP8", ...}
255	        # In future modelopt will deprecate hf_quant_config.json, and only keep config.json.
256	        # For legacy reasons, we keep hf_quant_config.json for now.
257	
258	        # Initialize variables
259	        kv_cache_quant_method = None
260	        exclude_modules = None
261	
262	        # Try flat format first (config.json quantization_config - preferred format)
263	        quant_method = config.get("quant_algo")
264	        if quant_method is not None:
265	            # Flat format (config.json quantization_config)
266	            # For kv_cache, check if kv_cache_scheme exists and extract algo
267	            kv_cache_scheme = config.get("kv_cache_scheme")
268	            if (
269	                kv_cache_scheme
270	                and kv_cache_scheme.get("type") == "float"
271	                and kv_cache_scheme.get("num_bits") == 8
272	            ):
273	                kv_cache_quant_method = "FP8"
274	
275	            # Map 'ignore' field to 'exclude_modules'
276	            exclude_modules = config.get("ignore")
277	        else:
278	            # Fall back to nested format (hf_quant_config.json - legacy format)
279	            try:
280	                quantization_section = cls.get_from_keys(config, ["quantization"])
281	                quant_method = quantization_section.get("quant_algo")
282	                kv_cache_quant_method = quantization_section.get("kv_cache_quant_algo")
283	                exclude_modules = quantization_section.get("exclude_modules")
284	            except ValueError:
285	                raise ValueError(
286	                    "Cannot find 'quant_algo' in the model's quantization config. "
287	                    "Expected either flat format (config.json) or nested format (hf_quant_config.json)."
288	                )
289	        if quant_method is None:
290	            raise ValueError(
291	                "Cannot find 'quant_algo' in the model's quantization config. "
292	            )
293	        if "FP8" not in quant_method:
294	            raise ValueError(
295	                "ModelOptFp8Config only supports static FP8 quantization in SGLang. "
296	                "For FP4 quantization, use ModelOptFp4Config. "
297	                "Check the quantization config for your model's configuration."
298	            )
299	
300	        return cls(
301	            is_checkpoint_fp8_serialized=True,
302	            kv_cache_quant_method=kv_cache_quant_method,
303	            exclude_modules=exclude_modules,
304	            packed_modules_mapping=config.get("packed_modules_mapping"),
305	        )
306	
307	    def is_layer_excluded(self, prefix: str) -> bool:
308	        if len(self.exclude_modules) == 0:
309	            return False
310	        return any(
311	            module in prefix
312	            or (
313	                prefix.startswith("language_model.")
314	                and module in prefix.removeprefix("language_model.")
315	            )
316	            for module in self.exclude_modules
317	        )
318	
319	    def get_quant_method(
320	        self, layer: torch.nn.Module, prefix: str
321	    ) -> Optional[QuantizeMethodBase]:
322	        return self._get_quant_method(
323	            layer, prefix, Linear=ModelOptFp8LinearMethod, Moe=ModelOptFp8MoEMethod
324	        )
325	
326	
327	class ModelOptFp8LinearMethod(LinearMethodBase):
328	    """Linear method for ModelOpt static FP8 quantization.
329	
330	    Supports loading FP8 checkpoints with static weight and activation scales.
331	    Future support may include dynamic scales.
332	
333	    **Limitations**:
334	    1. Only supports per-tensor quantization due to `torch._scaled_mm` limitations.
335	    2. Only supports the `float8_e4m3fn` data type.
336	
337	    Args:
338	        quant_config (ModelOptFp8Config): The ModelOpt quantization configuration.
339	    """
340	
341	    def __init__(self, quant_config: ModelOptFp8Config):
342	        super().__init__()
343	        self.quant_config = quant_config
344	        self.cutlass_fp8_supported = cutlass_fp8_supported()
345	
346	    def create_weights(
347	        self,
348	        layer: torch.nn.Module,
349	        input_size_per_partition: int,
```

> TOOL

tool_use Bash
```json
{
  "command": "git log --oneline -5 --format=\"%h %s%n%b\" 87a8bb1 61e4904 06ed8e0 e291467 20cc58a b7a839e 2>/dev/null | head -60",
  "description": "Get dynamic spec mode commit messages"
}
```

> TOOL

tool_result Bash
```
87a8bb1 perf(eagle/dynamic): four small accelerations on the spec-decode hot path
Each fix is independent and offline-validated; smoketested across bs=1/8/16/32/36
plus repeated NO_SPEC <-> D5 <-> D7 transitions (zero flush warnings, coherent
output). No e2e bench yet — these are the "small but perceivable" wins.

#1 NO_SPEC lazy draft KV catch-up
  Skip the per-step [REDACTED] that ran purely
  to keep draft KV lock-step with target. Stash (target_hidden, next_token_id)
  per Req on pending_no_spec_{hidden,token_ids} during the streak; on the
  first non-NO_SPEC step, _flush_no_spec_pending replays the K stashed
  positions in ONE multi-token DRAFT_EXTEND. Filter/merge/finished cleanup
  are free since pending lives on the Req.
  Subtle bits handled:
    * Stale spec_info.topk_p tripping EagleDraftInput.filter_batch when a req
      finishes mid-streak — null out spec_info fields at end of each NO_SPEC
      step so filter routes through the topk_p=None branch.
    * Multi-token flush needs (bs*K,) out_cache_loc; the last NO_SPEC step
      only left (bs,). Gather kv slots from req_to_token_pool.req_to_token at
      [seq_len-K..seq_len) per req.
    * The draft_extend cuda graph runner's buffers are sized for
      bs * (steps+1) tokens (the 1-token-per-req post-prefill shape); flush's
      bs*K tokens overflow. Add num_tokens check to can_run so flush falls
      back to eager. Capture path unchanged.
    * Mid-streak EXTEND (mixed prefill+decode) drops pending with a warning;
      affected reqs see one D5/D7 step with degraded accept rate. Rare in
      practice; logged for diagnosis.

#2 _apply_spec_config early-return on unchanged mode
  D5 -> D5 is the steady-state hot path; the legacy "no early-return" comment
  was scoped to startup only. Cache _applied_spec_mode, return immediately
  when mode matches. MARS theta moves off a module-level _MARS_THETA write
  onto an EagleVerifyInput.mars_theta field plumbed via draft() — eagle_info
  reads from spec_info first, falls back to module global for legacy callers.
  ~0.2 us/step saved; dependability win is bigger.

#3 FlashInfer verify plan() takes CPU inputs
  plan() unconditionally does qo_indptr.to("cpu") + paged_kv_indptr.to("cpu")
  + paged_kv_last_page_len.to("cpu"), three D2H syncs per replay (~26 us
  total at any bs). Pre-build pinned-memory CPU twins of qo_indptr per dtn
  alongside the GPU bank; pass the CPU versions of qo_indptr / kv_indptr /
  kv_last_page_len directly. plan()'s internal _paged_kv_indptr_buf.copy_
  becomes an async H2D into the same registered GPU buffer — semantically
  identical, three D2H syncs gone. Capture path untouched (one-time cost).

#4 _alloc_sparse_for_new_positions: bulk plan + scatter
  Replaced the bs * range(...) Python double-loop + per-position
  alloc_token_slots(1) + advanced-index write with:
    * a fast Python pre-check (~3-5 us) that bails when no req crosses any
      kernel_size / kernel_stride boundary this step (the common case at
      kernel_stride=16 vs accept_len=1-3),
    * numpy planning for the rare crossing steps,
    * a single bulk alloc_token_slots(M) + single advanced-index scatter per
      tier, preserving the legacy "+1 padding" overlap semantic via an
      explicit pad-write at col j_max+1.
  Slot IDs renumber (legacy interleaved k1/k2 per-req; bulk groups all k1
  then all k2) — no semantic effect, the offline test verifies structural
  pattern equivalence (same nonzero cols, same intra-row slot-equivalence
  classes). Microbench: M=0 step 2->1 us, one-cross 230->58 us (4x),
  multi-cross bs=32 step 3.7 ms->60 us (62x).
```

> TOOL

tool_use Bash
```json
{
  "command": "git log --oneline --all --grep=\"scale.*loader\\|fused.*scale\\|auxiliary.*scale\\|QKV.*fused\\|per-tensor.*scale\" -i | head -20",
  "description": "Search for scale loader bug related commits"
}
```

> TOOL

tool_result Bash
```
f7faed5 fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards
2b36ae2 fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards
```

> TOOL

tool_use Bash
```json
{
  "command": "git log --oneline --all --grep=\"FourOverSix\\|fouroversix\\|4/6\\|scale_4\\|scale_6\" -i | head -10",
  "description": "Search for FourOverSix related commits"
}
```

> TOOL

tool_result Bash
```
9225f46 feat: intermediate_ssm direct-write + fused sparse metadata + profiling framework
af38f7c docs: comprehensive cleanup — update CLAUDE.md, consolidate docs, add AGENTS.md
20ea7ec docs: comprehensive cleanup — update CLAUDE.md, consolidate docs, add AGENTS.md
f359853 probe-sala: fix empty responses via FlashInfer/cuDNN upgrade + full self-eval config
c54c473 probe-sala: fix empty responses via FlashInfer/cuDNN upgrade + full self-eval config
```

> AGENT

现在，我来获取 git 日志中关于性能优化的详细提交，并阅读更多文档。

> TOOL

tool_use Bash
```json
{
  "command": "git log --oneline --all --grep=\"perf\\|prefill\\|runtime\\|infllmv2\\|plan_info\\|plan cache\\|RoPE\\|residual\\|scale_emb\\|b12x\\|dispatch\\|marlin\\|operator\\|kernel\\|decode\\|GPTQ\\|NVFP4\\|quant\" --since=\"2026-03-01\" | head -60",
  "description": "Find performance-related commits"
}
```

> TOOL

tool_result Bash
```
87a8bb1 perf(eagle/dynamic): four small accelerations on the spec-decode hot path
06ed8e0 revert(eagle/dynamic): roll back mamba pool split
e291467 fix(eagle/dynamic): KV pool reclaim, per-mode mars theta, crash fixes
20cc58a perf(eagle/dynamic): kill three hot-path wastes in spec decode
b7a839e feat(eagle): dynamic spec mode (NO_SPEC / D5 / D7) by running batch size
cc9943b docs: restructure and merge eagle docs — trim stale files, consolidate surveys
4c0005c docs: multi-doc audit — correct b12x/MARS/rope_theta status and cross-link
ca22a40 docs(eagle/mars): record theta=0.8 initial validation result
8f1af57 feat(eagle): implement MARS verify + sync MARS .so to demo-sala
9dabf09 feat(eagle): two-phase TARGET_VERIFY with shared-buffer fix
f0e6a61 chore(demo-sala/env): align prepare_env.sh to main
a8b22ae revert(demo-sala): roll back to 9a7e04c cu13 baseline
61213bf chore(demo-sala): drop legacy duplicates, add tuning + verify helpers
0e768a3 chore(env+eval+meta): start_eagle defaults, prepare_env tweaks, CLAUDE/AGENTS align
081559b docs: marlin-tuning + collapse + training-v3 + nvfp4-kv + infllmv2 fix + upstream survey
5b1c851 chore(bench): reorganize into kernels/{minicpm,marlin,fp4,prefill,...}; add microbenches
da18187 feat(eagle): v3 training rewrite + pipeline reorganization
1608d18 fix(sgl-srt): spec-v1 correctness + profile gating + NVFP4 lm_head pipeline
5552a23 perf: tune no-spec decode kernels
e9bfcb0 feat(probe-sala): sync sglang to latest + b12x readiness check
51ca6a8 fix(demo-sala): drop stale MARLIN_DECODE_THRESHOLD, add CUTE_DSL_CACHE_DIR
d19e4f2 perf: strip dispatch trace + hot-path cleanup
b3f9687 feat(b12x): 2-tier dispatch full-M + eagle_fc shape + dispatch trace
c3effe9 docs(runtime): §10.B 深挖 — 17.7% idle 拆分，CPU 侧真实 ROI 硬顶从 9.6% 下修到 5.5%
cd480ca docs(runtime): §7/§8/§9 memcpy attribution + §10 profiling methodology
d7e5b52 probe-sala: torchao+xgrammar wheels + exit 1 also on all-pass path
4f8fc05 bench: cu13/sm120 kernel microbenches + b12x CuTe-DSL backend exploration
9a7e04c feat(probe-sala): full cu12→cu13 upgrade pipeline + BOS wheels offline install
230b381 docs: rewrite CLAUDE.md + trim AGENTS.md + align start_eagle.sh
bf55703 docs: restructure — rename, merge, split, update
b4d387a perf(prefill): cross-chunk plan_info reuse + smax64 bench
1f265fe perf(prefill): reuse flashinfer plan across 8 standard layers
475ddd5 eval_ood: step-0 only, full-length (no SEQ_LEN truncation)
9225f46 feat: intermediate_ssm direct-write + fused sparse metadata + profiling framework
f7faed5 fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards
2b36ae2 fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards
da4309b feat: EAGLE-3 speculative decoding with fused GLA kernel
0843656 feat: EAGLE-3 speculative decoding with fused GLA kernel
351e77e chore: cleanup dead files, one-off scripts, update .gitignore
3ffeed9 chore: cleanup dead files, one-off scripts, update .gitignore
460f3f2 plan: update Phase 2 checklist — STE-QAT + NVFP4 export implemented
373dc6d plan: update Phase 2 checklist — STE-QAT + NVFP4 export implemented
60474e8 eagle: implement STE-QAT FP4 native training + NVFP4 export pipeline
1f702ee eagle: implement STE-QAT FP4 native training + NVFP4 export pipeline
1267775 eagle: add Phase 0 baselines, Phase 2 kernel benchmarks, and plan
38ce7ea eagle: add Phase 0 baselines, Phase 2 kernel benchmarks, and plan
f359853 probe-sala: fix empty responses via FlashInfer/cuDNN upgrade + full self-eval config
c54c473 probe-sala: fix empty responses via FlashInfer/cuDNN upgrade + full self-eval config
ab4a619 fix: EAGLE-3 MiniCPM-SALA compatibility
8bc05a3 fix: EAGLE-3 MiniCPM-SALA compatibility
6087c93 revert: undo fc3a920 operator optimizations for precision A/B test
fbf2704 revert: undo fc3a920 operator optimizations for precision A/B test
f42aca0 fix: deterministic decode/verify via num_splits=1 + eager TARGET_VERIFY fallback
409ff84 fix: deterministic decode/verify via num_splits=1 + eager TARGET_VERIFY fallback
ed3ec68 clean: restore demo-sala from tarball + MedusaBlock auto-detect
c3e99f4 clean: restore demo-sala from tarball + MedusaBlock auto-detect
150119c fix: Medusa spec decode CUDA graph buffer overflow + vectorized verify
5f2a290 fix: Medusa spec decode CUDA graph buffer overflow + vectorized verify
c6b7991 feat: Medusa speculative decoding integration (S1 -12%, S8 -12.5%)
3de4d05 feat: Medusa speculative decoding integration (S1 -12%, S8 -12.5%)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/kernels-sm120.md"
}
```

> TOOL

tool_result Read
```
1	# sm_120 NVFP4 Kernel 现状与优化空间
2	
3	## 1. 结论速览
4	
5	- **硬件上限**：sm_120 NVFP4 block-scaled MMA 真实 peak ≈ **1467 TFLOPS**（pure-MMA probe，2 block/SM 达到，实测对齐理论值 1553 TFLOPS 的 ~95%）。
6	- **生态现状**：CUTLASS / cuBLAS / cuDNN / sgl-kernel 全部实测 ~560 TFLOPS，**仅挤出 peak 的 38%**，有 **2.6× 理论空间**。
7	- **决策洼地**：不是 ISA 上限，是官方全家桶 + 社区 kernel 的共同未调优状态。autotune 可 vary 的维度比预期窄（硬件约束），但 schedule / stages / epilogue fusion 仍未开发。
8	- **Marlin 不是优化对象**：decode 热形状（gate/up/down M=1/8）已实测 82-97% L2 带宽饱和，sm_120-native W4A16 重写无可挤空间。
9	- **b12x backend（PR #3051）** 已集成并默认启用（`SGLANG_ENABLE_B12X=1`）：2-tier dispatch Marlin/b12x + 3 点 CUTLASS override，覆盖 6 个形状（5 target + eagle_fc）× 全 M 范围（58 个 tile 配置），decode GEMM 62% 走 b12x。不再依赖 `SGLANG_MARLIN_DECODE_THRESHOLD`。关键 gotcha：b12x 必须喂 `layer.weight_scale_interleaved`（post-permute TMA-swizzled 格式），不是 pre-permute padded_scales（见 §7.4）。
10	
11	## 2. MMA 指令与硬件 peak
12	
13	**PTX（CUTLASS 生成）**：
14	
15	```
16	mma.sync.aligned.kind::mxf4nvf4.block_scale.scale_vec::4X.m16n8k64
17	  .row.col.f32.e2m1.e2m1.f32.ue4m3
18	```
19	
20	- `m16n8k64`：每指令 16×8×64×2 = 16384 FLOPs
21	- 每 16 个 k 元素一个 ue4m3 scale，4 scale/tile
22	- accumulator f32
23	- **block-scaled 相对 unscaled 慢 ~3×**，是 ISA 级开销
24	
25	**pure-MMA peak**（`bench/pure_mma_peak/`）：寄存器常驻 A/B/scale，`ACC=8` 独立累加器消除依赖，`INNER=64` 循环展开。
26	
27	| blocks/SM | warps/SM | TFLOPS | cycles/MMA |
28	|---|---|---|---|
29	| 1 | 4 | 1447 | 16.1 |
30	| **2** | **8** | **1467** | 24.2 |
31	| 4 | 16 | 1423 | 134 |
32	| 8 | 32 | 1152 | 77 |
33	
34	**推算**：4 tensor partitions/SM × (1 MMA / 16 cycles) × 156 SMs × 2.43 GHz × 16384 FLOPs = **1553 TFLOPS 理论**，实测 1467 差 5–7%（时钟/同步噪声）。
35	
36	## 3. 各 GEMM 库对比（M=8192 标定点）
37	
38	| Library | 路径 | gate_proj TFLOPS | 备注 |
39	|---|---|---|---|
40	| sgl-kernel `cutlass_scaled_fp4_mm` | `Sm120` builder, tile=256×128×128 | 550 | 当前 SALA 默认 |
41	| flashinfer `mm_fp4` backend=cutlass | 同底 CUTLASS | 547 | — |
42	| flashinfer `mm_fp4` backend=cudnn | cuDNN 路径 | 551 | 和 CUTLASS 打平 |
43	| flashinfer `mm_fp4` backend=trtllm | — | 不支持 sm_120 | BackendSupportedError |
44	| flashinfer `mm_fp4` backend=cute-dsl | — | 不支持 sm_120 | 同上 |
45	| `torch._scaled_mm` (cuBLAS 13.4) | via `VEC16_UE4M3` scale mode | 553 | PyTorch 2.11 暴露 |
46	
47	**四个库一致 ~550 TFLOPS** = 生态共同的未调优状态。
48	
49	## 4. sgl-kernel 当前 dispatch
50	
51	`csrc/gemm/nvfp4_scaled_mm_kernels.cu` 只 hard-code 两个 sm_120 config：
52	
53	| 触发条件 | MmaTile (M×N×K) | Cluster | Schedule |
54	|---|---|---|---|
55	| `next_pow_2(M) ≤ 256` | 128 × 128 × 128 | 1×1×1 | Auto（实测 Cooperative, stages=3） |
56	| `M > 256` | 256 × 128 × 128 | 1×1×1 | 同上 |
57	
58	**Prefill M=8192 永远走第二个**。N 维和 K 维都从未扩过。
59	
60	### 4.1 flashinfer 0.6.8.post1 已带 sm_120 autotune 池（PR #2460）
61	
62	2026-03 合入的 [flashinfer PR #2460](https://github.com/flashinfer-ai/flashinfer/pull/2460) 把 sm_120 `mm_fp4(backend="cutlass")` 的候选 tile 从"只有 128×128×128 DP"扩到 **3 tile × 2 schedule = 6 tactic**：
63	
64	```cpp
65	// flashinfer/data/include/flashinfer/gemm/fp4_gemm_cutlass_template_sm120.h:168
66	tactic 0: 128×128×128  Auto  DP      (== 旧 fallback，tactic=-1 等价)
67	tactic 1: 128×128×128  Auto  StreamK
68	tactic 2: 128×128×256  Auto  DP
69	tactic 3: 128×128×256  Auto  StreamK
70	tactic 4: 256×128×128  Auto  DP
71	tactic 5: 256×128×128  Auto  StreamK
72	```
73	
74	PR 给的收益数字是 **M=32, N=5120, K=25600 → 1.8× on sm_120**，但只是单点。PR 未内置 autotune cache，我们必须离线 tune + 落盘复用（见 §7.1）。
75	
76	## 5. sm_120 tile 空间硬件约束
77	
78	实测编译 12 个候选，成功 5 个：
79	
80	### 成功（有效 autotune 维度）
81	`128×128×128`, `256×128×128`（sgl 默认两种）, `128×256×128`, `256×256×128`, `128×128×256`
82	
83	### 失败
84	
85	| Config | 错误 | 根因 |
86	|---|---|---|
87	| `256×128×256` / `128×256×256` / `256×256×256` | `Specialization requires Stages set to value 2 or more` | sm_120 每 SM ~100 KB smem，扣 epilogue 后装不下 2 份大 tile |
88	| `64×128×128` / `128×64×128` / `64×256×128` / `256×64×128` | `TMA requires CTA_Tile and SLayout top-level size equivalence` | CUTLASS sm_120 block-scaled TMA atom 最小 M/N = 128 |
89	| `Cluster > 1` | `no programmatic multicast on this arch` | sm_120 无 distributed shared memory（tcgen05 专属） |
90	
91	**有效 tile 空间**：`{128, 256} × {128, 256} × {128}` + `(128, 128, 256)`，Cluster 锁死 1×1×1。
92	
93	## 6. W4A4 vs W4A16：小 M 的结构性差异
94	
95	Marlin (W4A16) vs CUTLASS (W4A4)，M=1 gate_proj：
96	- Marlin: 16.5 us
97	- CUTLASS NVFP4: 48 us（3× 慢）
98	
99	**不能由 tile 大小解释**。NVFP4 W4A4 的 **activation quantize**（BF16 → FP4 + e4m3 scale）约 7.4 us 是 M=1 时**不可消除的架构级开销**：
100	
101	```
102	NVFP4 total = quantize(7.4us) + GEMM(40us) = 48us
103	即使 GEMM 降到 10us（理论最小）→ 17us ≈ 打平 Marlin
104	```
105	
106	| | Marlin | CUTLASS NVFP4 |
107	|---|---|---|
108	| 量化方案 | W4A16（激活不量化） | W4A4 |
109	| 核心指令 | BF16 MMA `m16n8k16` | FP4 block-scaled MMA `m16n8k64` |
110	| peak TFLOPS | ~400 | ~1467 |
111	| 小 M 瓶颈 | weight-bandwidth | quantize overhead + weight BW |
112	
113	**启示**：小 M 场景，NVFP4 小 tile kernel 最好情况只能打平 Marlin，不能显著超越。真想挤小 M 的话，应该写 **sm_120 原生 W4A16 kernel 替代 Marlin** —— 但 Marlin 实测已 82-97% L2 BW 饱和，无可挤空间。
114	
115	## 7. ROI 排序的优化方向
116	
117	### 7.1 flashinfer mm_fp4 离线 autotune（已落地 2026-04）
118	
119	利用 §4.1 的 6 tactic 池做**离线 tune → JSON cache → runtime load**，不在 server 启动时占 warmup 预算。
120	
121	**脚本**：`demo-sala/tune_mm_fp4_sm120.py`
122	
123	**策略（A+B 组合，消除噪声回归）**：
124	
125	- **A（profiling 加强）**：`AutoTuner.warmup=20, repeat=100`（10× flashinfer 默认 3/10）
126	- **B（per-config validate）**：对每个 (shape, M) 独立跑 baseline（tactic=-1）→ tune → bench tuned；仅当 `tuned < baseline × 0.97` 才合并进 cache，KEEP_MARGIN=3%。保证单调性——任何 cache 条目都是验证过的 ≥3% 增益，miss 走 fallback（等价 baseline）
127	
128	**覆盖 shape**（MiniCPM-SALA 所有 projection × 14 个 M bucket）：
129	
130	| 层 | N × K | M buckets |
131	|---|---|---|
132	| gate_up_proj | 32768 × 4096 | 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192 |
133	| down_proj | 4096 × 16384 | 同上 |
134	| qkv_proj | 4608 × 4096 | 同上 |
135	| o_proj | 4096 × 4096 | 同上 |
136	| lm_head | 73448 × 4096 | 同上 |
137	
138	**tune 结果**（`demo-sala/assets/mm_fp4_tune_sm120_report.json`）：
139	
140	| 层 | kept / total | 聚合 speedup（kept only） | 显著赢点 |
141	|---|---|---|---|
142	| gate_up_proj | 4 / 14 | 1.06× | 均匀弱收益 |
143	| **down_proj** | **13 / 14** | **1.27×** | **M=64 3.59×, M=128 3.55×, M=2 3.39×, M=4 3.27×** |
144	| qkv_proj | 8 / 14 | 1.07× | M=16 1.12×, M=1024 1.11× |
145	| o_proj | 11 / 14 | 1.06× | M=1024 1.12× |
146	| lm_head | 7 / 14 | 1.08× | M=8,16 各 1.11× |
147	| **总计** | **43 / 70** | — | — |
148	
149	**部署**（已生效）：
150	
151	- 产物：`demo-sala/assets/mm_fp4_tune_sm120.json`（62 entries 含 metadata）
152	- 加载点：`modelopt_quant.py` 模块导入时 `_load_fp4_autotune_cache()` 读 `SGLANG_FP4_TUNE_CACHE` 环境变量 → `AutoTuner.get().load_configs(path)`
153	- 非 tune 模式下 flashinfer `choose_one` 直接查 cache（不需要 `autotune(...)` context manager），miss → tactic=-1 fallback
154	- env 导出：`demo-sala/prepare_env.sh` Stage 5 + `eval/start_eagle.sh` 双路径同步
155	
156	**与 Marlin hybrid 的交互**：
157	down_proj 3× 级别的巨大增益集中在 M=2..256，但 `SGLANG_MARLIN_DECODE_THRESHOLD=48` 让 M≤48 走 Marlin，不过 CUTLASS。**真实吃到这批增益的场景**：EAGLE-3 verify 的 target forward（M≈256 @ bs=64 dtn=4）和 Smax 并发。小 M decode 仍走 Marlin。
158	
159	**为什么 autotune 会产生回归（已解决）**：tactic 0 和 fallback tactic=-1 是同一个 kernel，理论上 worst case 等于 baseline。第一版跑出的 qkv M=1,2 有 0.59-0.74× 回归——纯属 flashinfer 默认 `warmup=3, repeat=10` 的测量噪声，min selection 在方差带内误选次优 tactic。A+B 策略完全消除：43 个入库全部验证过，27 个被 KEEP_MARGIN 丢弃。
160	
161	### 7.2 NVFP4 tile × schedule × stages 手动编译扫描（独立方向，未展开）
162	
163	§7.1 是用 **flashinfer 已编译好的 6 个 tactic** 做选择；另一条独立路径是自己编译候选 kernel 扩展 tile 空间。
164	
165	- 5 个有效 tile（§5）× 2 schedule × 3-4 stages ≈ 30-40 候选
166	- 模板：`bench/autotune_fp4/autotune_kernel.cu`
167	- 目标：挤到 peak 50-70% = 750-1000 TFLOPS（1.3-1.8×）
168	- **状态**：未展开——§7.1 的 ROI 兑现（down_proj 3.5×）已满足短期收益需求；自编译需维护 sgl-kernel fork，维护成本高于收益
169	
170	### 7.3 Epilogue fusion（非 kernel 内部）
171	
172	- SwiGLU 融入 gate+up GEMM epilogue：省 32-128 MB 中间 activation write+read
173	- RoPE 融入 QKV GEMM epilogue
174	- 和 autotune 互补，可并行做
175	
176	### 7.4 b12x backend（全面实测 + 集成 + 生产 smoke test 通过 2026-04-22）
177	
178	**集成状态 2026-04-22**：代码开发完成，正确性验证通过（smoke test 正确答题，26 个 b12x kernel JIT 编译成功）。**当前提交包未启用**：`SGLANG_ENABLE_B12X` 默认为 0（`prepare_env.sh` 和 `start_eagle.sh` 均设 `:-0`），回滚原因是 EAGLE draft CUDA graph capture 路径不兼容 b12x。target model 走 b12x 收益已验证，draft model 始终需走纯 Marlin。
179	
180	**EAGLE draft 不兼容说明**：draft model CUDA graph capture 路径与 b12x dispatch 不兼容，draft 需保持纯 Marlin（`_detect_draft_model_quantization()` 设 threshold=9999）。若后续启用 b12x，target 路径可获 decode GEMM ~32.4% 收益，draft 路径不受影响。
181	
182	**初版集成 bug 与根因定位**（值得记录以防再踩）：
183	
184	第一版集成把 b12x 喂了 "pre-permute `padded_scales`"（即 `layer.weight_scale_interleaved` 做 TMA swizzle 之前的原始 padded 形式），基于假设"b12x 要 unswizzled 格式"。smoke test 模型答非所问（`1+1=?` 答成推理任务）——语言结构保留但分布偏移，典型权重轻微错乱症状。
185	
186	用 `bench/b12x/diag_layout_mismatch.py` 做 6 种（backend, x 格式, w scale 格式）交叉对照后定位：
187	
188	| 测试 | backend | x sf | w sf | vs 生产 CUTLASS 参考 |
189	|---|---|---|---|---|
190	| 1 | cutlass | nvfp4（bench） | **pre-permute** | cos **0.85** |
191	| 2 | cutlass | fp4（生产） | pre-permute | cos 0.85 |
192	| 3 | cutlass | fp4（生产） | **interleaved** | **参考** |
193	| 4 | b12x | nvfp4 | pre-permute（初版集成） | cos 0.85 |
194	| 5 | b12x | fp4 | pre-permute | cos 0.85 |
195	| **6** | **b12x** | **fp4** | **interleaved** | **cos 1.0 bit-identical** ✓ |
196	
197	**结论**：b12x kernel 和 mm_fp4(cutlass) 需要 **完全相同的 interleaved（TMA-swizzled）weight scale 布局**。bench `test_correctness.py` 里 `nvfp4_quantize(layout_128x4, do_shuffle=False)` 输出其实**就是 interleaved 格式**（不是我以为的"unswizzled"）；`do_shuffle=True` 才额外加一次 TMA 通道重排。生产 `layer.weight_scale_interleaved`（经过 `process_weights_after_loading` 的 permute）字节上等价于 `nvfp4_quantize(do_shuffle=False)`。
198	
199	**修复**：直接复用 `layer.weight_scale_interleaved`，删掉 `weight_scale_b12x` 占位变量，activation 用 `fp4_quantize`（production-style swizzled）而非 `nvfp4_quantize`。两者在这个布局下 kernel 输出位级相同。
200	
201	**bench 数据**（`bench/b12x/bench_full_matrix.py` + `b12x_full_matrix.json`，5 shape × 10 M × 4 backend，42 分钟 wall clock）：
202	
203	| shape | M=16 Mar/b12x | M=48 Mar/b12x | M=96 C/b12x | M=256 C/b12x | 赢 b12x 的 M 区间 |
204	|---|---|---|---|---|---|
205	| std_o (4096×4096) | 12.3 / **10.3** | 30.8 / **10.2** | 45 / **12.3** | 39 / **15.1** | **M ≥ 16** |
206	| std_qkv (4608×4096) | 12.1 / **10.3** | 27.9 / **10.3** | 44.3 / **12.3** | 42.8 / **16.4** | **M ≥ 16** |
207	| down (4096×16384) | **20.6** / 37.9 | **49.2** / 39.1 | 151 / **38.9** | 158 / **77.1** | **M ≥ 48** |
208	| gate_up (4096×32768) | **31.2** / 47.1 | 77.2 / **38.8** | 77.6 / **67.6** | 146 / **131** | **M ≥ 24** |
209	| gla_qkv (4096×12288) | **14.4** / 20.5 | **37.1** / 14.4 | 43.9 / **28.7** | 76.8 / **49.1** | **M ≥ 24** |
210	
211	**早期 bench 误判修正**（历史记录，防再踩）：
212	
213	最初用 `bench/b12x/run_b12x_vs_all.py` 得"仅 std_o + down 能用"结论，两处错：
214	1. baseline 用 sgl-kernel `cutlass_scaled_fp4_mm`，**不是生产** `flashinfer.mm_fp4(backend="cutlass")` + autotune cache。生产 std_o 小 M 反而比 sgl-kernel 慢 15–20%。
215	2. b12x 只跑默认启发式 tile，**没走 PR #3051 的 8-tactic autotune 空间**（4 tile × 2 prefetch）。tuned b12x 在 M=256 比默认快 2.75×，down 整体快 2×。
216	
217	修正后 5 shape 全部有效（上表），最终用 `bench/b12x/bench_full_matrix.py`（4 backend × 5 shape × 10 M）取证。
218	
219	**b12x 最优 tile 分布**（非单一最优）：
220	
221	| M | std_o | std_qkv | down | gate_up | gla_qkv |
222	|---|---|---|---|---|---|
223	| 24 | 64×128/pf | 64×128 | 64×64/pf | 64×128/pf | 64×128/pf |
224	| 48 | **64×64** | 64×64/pf | 64×64/pf | 64×128 | 64×128/pf |
225	| 96 | **128×64** | 64×128/pf | 64×64/pf | 64×64/pf | 64×64 |
226	| 128 | 64×128/pf | **128×64** | 64×64 | 64×64 | 64×64 |
227	| 256 | 64×128/pf | 64×128 | 64×64/pf | 64×128/pf | 64×64 |
228	
229	**关键：autotune 不是奢侈品，是必须的**。heuristic `_select_default_sm120_mma_tiler` 在 M=256 错选 128×128 导致 2.75× 速度损失；M=48 应选 64×64 但 heuristic 选 64×128；prefetch=True 是 heuristic 完全不考虑的维度。
230	
231	**正确性验证**（`bench/b12x/test_correctness.py` + `b12x_correctness.json`）：
232	- 23 配置 × 3 seed = **69 / 69 PASS**
233	- **cos_sim = 1.000000, max_abs = 0.000000**（bit-identical 不是舍入级一致，是位级一致）
234	- 原因：b12x 和 CUTLASS 都发同一条 `mma.sync.aligned.kind::mxf4nvf4.block_scale` 指令，f32 accumulator 顺序在这些 shape 上恰好等价
235	- **混用零精度代价**——模型层间 b12x/CUTLASS 切换无一致性问题
236	
237	**生产 M 直方图取证**（2026-04，`SGLANG_PROFILE_DISPATCH=1` EAGLE-3 workload，54000 次 GEMM 13.2s wall）：
238	
239	decode GEMM 时间分布（排除 M=8192 prefill）：
240	
241	| shape | decode GEMM ms | M=[24,256] 占比 | b12x 节省 | 节省 % |
242	|---|---|---|---|---|
243	| std_o | 395 | 68.5% | 195 | **49%** |
244	| std_qkv | 48 | 71.4% | 23 | 47% |
245	| down | 517 | 72.4% | 194 | **38%** |
246	| gate_up | 589 | 59.4% | 99 | 17% |
247	| gla_qkv | 202 | 63.1% | 57 | 28% |
248	| **合计** | **1750** | 66% | **567** | **32.4%** |
249	
250	**E2e 估算**：
251	- decode GEMM kernel 时间省 **32.4%**（1750 → 1183 ms/13.2s）
252	- wall clock 上限 4.3%（若 GEMM 完全在 critical path）
253	- 实际 decode 并发 ~1.3× → 真实 e2e 吞吐增益 **~3%**
254	- Prefill（M=8192）**0 收益** —— b12x 大 M 回到 128×128 = CUTLASS 同路径
255	
256	**最终 dispatch 规则（2-tier + CUTLASS override，2026-04-23）**：
257	
258	```python
259	MARLIN_UPPER = {
260	    (N=4096,  K=4096):   8,    # std_o
261	    (N=4608,  K=4096):   8,    # std_qkv
262	    (N=4096,  K=16384):  24,   # down (K 大 Marlin 带宽仍赢到 M=24)
263	    (N=32768, K=4096):   16,   # gate_up
264	    (N=12288, K=4096):   16,   # gla_qkv
265	    (N=4096,  K=12288):  16,   # eagle_fc (crossover M=24, conservative=16)
266	}
267	CUTLASS_OVERRIDE = {
268	    (4096,  16384, 512),   # down M=512:     b12x 0.91× CUTLASS
269	    (32768, 4096,  8192),  # gate_up M=8192: b12x 1.00× CUTLASS
270	    (4608,  4096,  8192),  # std_qkv M=8192: b12x 0.97× CUTLASS
271	}
272	# M ≤ MARLIN_UPPER         → Marlin (W4A16)
273	# (N,K,M_bucket) in OVERRIDE → tuned CUTLASS (W4A4)
274	# otherwise                 → b12x (W4A4, block-scaled MMA)
275	```
276	
277	2-tier 规则覆盖 6 个形状 × 全 M 范围（58 个 BEST_TILE 条目），不再使用 `B12X_UPPER` 上限。高并发时 b12x 接管 62% dispatch，override 18%（主要是 down M=512），CUTLASS prefill 19%。`SGLANG_MARLIN_DECODE_THRESHOLD` 不再需要——b12x 路径内置 per-shape Marlin 阈值并自动准备 Marlin 权重。
278	
279	### 7.5 b12x 环境要求与集成步骤
280	
281	```
282	nvidia-cutlass-dsl                 == 4.5.0.dev0
283	nvidia-cutlass-dsl-libs-base       == 4.5.0.dev0
284	nvidia-cutlass-dsl-libs-cu13       == 4.5.0.dev0   (关键！uv pip 单升 base 会漏)
285	flashinfer-python                  >= 0.6.8.post1
286	torch                              == 2.11.0+cu130
287	CUDA toolkit                       == 13.2
288	export CUTE_DSL_ARCH=sm_120a       (不带 'a' 会 ptxas 拒收 block-scaled MMA)
289	```
290	
291	**b12x 踩过的坑**（记录以防重犯）：
292	
293	1. **cutlass-dsl 4.4.2 → 4.5.0.dev0 的 NVVM lowering**：4.4.2 生成 `_mma.block_scale...` 带下划线前缀（占位符），ptxas 报 `Unexpected instruction types`。4.5.0.dev0 才发 `mma.sync.aligned...kind::mxf4nvf4.block_scale`。必须三包同步升。
294	2. **CUTE_DSL_ARCH 默认不是 sm_120a**：默认回退 `sm_120`（无 arch suffix），block-scaled MMA 需要 `sm_120a`。
295	3. **PR demo 函数 `dense_gemm()` M=1 触发 `cudaErrorIllegalInstruction`**：不用 demo，直接走生产路径 `_compile_block_scaled_gemm` + `gemm.wrapper`（参考 `flashinfer/gemm/gemm_base.py` `_b12x_gemm_fp4_runner`）。
296	4. **Monkey-patch flashinfer.cute_dsl.utils**：我们没升 flashinfer 本体，只从 PR 拉 kernel 文件，运行时注入 `sm120_make_smem_layout_sfa/sfb`。
297	
298	**集成路径**：
299	
300	1. **kernel 文件**：从 `bench/b12x/` 复制到 `demo-sala/sglang/python/sglang/srt/layers/quantization/b12x/`（`dense_blockscaled_gemm_sm120.py` + `cute_dsl_utils.py` + `__init__.py`）
301	2. **glue 模块**：`demo-sala/sglang/python/sglang/srt/layers/quantization/b12x_fp4.py`——懒加载、monkey-patch flashinfer.cute_dsl.utils、编译+缓存、`b12x_gemm_fp4(x, w, x_sf, w_sf, alpha, tile, prefetch)` API
302	3. **modelopt_quant.py dispatch**：`NvFp4LinearMethod.apply()` 加第三路
303	4. **prepare_env.sh**：`CUTE_DSL_ARCH=sm_120a`（必须带 `a`）+ 3 包 cutlass-dsl 4.5.0.dev0（环境已具备，验证 BOS 清单）+ `CUTE_DSL_CACHE_DIR=/tmp/cute_dsl_cache`
304	5. **warmup**：`--skip-server-warmup` 前按 bench 最优 tile 表预编译 5 shape × 6 M_bucket = 30 个 kernel 变体（首次 ~5–10 分钟，后续复用 `CUTE_DSL_CACHE_DIR`）
305	6. **autotune**：不需要再跑 flashinfer autotune（同 shape 区间已被 b12x 接管）；现有 `mm_fp4_tune_sm120.json` 保留用于 M > 256 的 CUTLASS 路径
306	
307	## 8. 已终结方向（不值得做）
308	
309	| 方向 | 原因 |
310	|---|---|
311	| 手写 pure NVFP4 GEMM kernel | CUTLASS 已用足 TMA + WS + Cooperative + persistent + sm_120 原生 MMA |
312	| Cluster > 1 | sm_120 无 multicast |
313	| 大 K tile (>128) 搭大 M/N tile | smem 不够 2 stage |
314	| 小 tile (<128) | TMA atom 约束 |
315	| flashinfer `trtllm` backend | sm_120 不支持（`cute-dsl` 从 PR #3051 拉 b12x kernel 后可用，见 §7.4） |
316	| sm_120-native W4A16 重写 Marlin | Marlin decode M=1/8 已达 82-97% L2 BW（gate/up/down），无可挤空间 |
317	| Marlin bandwidth 测量作为 blocker | 已测，实证 L2 饱和，终结 |
318	
319	## 9. 关键脚本与数据位置
320	
321	| 文件 | 用途 |
322	|---|---|
323	| `bench/pure_mma_peak/pure_mma.cu` + `run.py` | pure-MMA peak 测量 |
324	| `bench/bench_fp4_all_backends.py` | 全家桶 library 对比 |
325	| `bench/probe_fp4_peak.py` | CUTLASS 跨 shape 实测收敛 |
326	| `bench/bench_cublas_vs_cutlass_nvfp4.py` | cuBLAS vs CUTLASS 对照 |
327	| `bench/autotune_fp4/autotune_kernel.cu` | tile 参数化模板 |
328	| `bench/autotune_fp4/build.sh` | 候选 config 编译 |
329	| `bench/bench_marlin_bandwidth.py` | Marlin 带宽测量 |
330	| `bench/b12x/` | PR #3051 backend 完整调研 + kernel 文件（`dense_blockscaled_gemm_sm120.py` + `cute_dsl_utils.py`） |
331	| `bench/b12x/bench_full_matrix.py` | **最终 4-way bench**：tuned-flashinfer-CUTLASS / sgl-kernel-CUTLASS / b12x 8-tactic / Marlin，5 shape × 10 M |
332	| `bench/b12x/b12x_full_matrix.json` | 上述 bench 完整结果（2026-04-22 跑，42 分钟 wall） |
333	| `bench/b12x/test_correctness.py` | b12x vs CUTLASS 位级等价测试（cos_sim / max_abs / max_rel） |
334	| `bench/b12x/b12x_correctness.json` | 69/69 PASS 记录 |
335	| `bench/b12x/run_b12x_vs_all.py` | 早期 bench（**baseline 不公平，保留作历史**；权威数据用 `bench_full_matrix.json`） |
336	| `bench/b12x_vs_all.json` | 早期 bench 结果（同上，保留） |
337	| `bench/b12x_extra_shapes.json` | 早期扩展 shape 实验（结论被 `bench_full_matrix.json` 推翻） |
338	| `demo-sala/tune_mm_fp4_sm120.py` | §7.1 离线 autotune 脚本（A+B 策略） |
339	| `demo-sala/bench_downproj_marlin_vs_cutlass.py` | down_proj Marlin vs CUTLASS(tuned) A/B，验证 threshold=48 |
340	| `demo-sala/assets/mm_fp4_tune_sm120.json` | autotune cache（运行时资产） |
341	| `demo-sala/assets/mm_fp4_tune_sm120_report.json` | autotune per-entry decision log |
342
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/marlin-tuning.md"
}
```

> TOOL

tool_result Read
```
1	# Marlin / b12x 调优记录
2	
3	> 更新时间：2026-04-27
4	> 范围：MiniCPM-SALA no-spec 路径下的 NVFP4 Marlin、b12x/CUTLASS 分流、CUDA graph 内 profiling。
5	> 最高口径：涉及 decode 性能时，以 CUDA graph replay 内 kernel 时间为准；Python `apply()` 计数只能作为辅助定位。
6	
7	## 当前部署状态速览
8	
9	| 组件 | 状态 | 说明 |
10	|---|---|---|
11	| b12x 2-tier dispatch | ⚠️ 开发完成，**未启用** | `SGLANG_ENABLE_B12X=0`（默认关闭）；draft CUDA graph capture 不兼容，回滚 |
12	| sgl-kernel FP4 scale bug fix | ✅ 已部署 | `common_ops.abi3.so` pre-built 替换，scale `/2` bug（cos_sim 0.77→1.0）修复 |
13	| Marlin atomic / shape-aware tile | ✅ 已集成 | `.so` 内已包含；全局阈值 `SGLANG_MARLIN_DECODE_THRESHOLD=48` 生效 |
14	| 当前生产 dispatch | ✅ M≤48 Marlin，M>48 CUTLASS | b12x 未启用；threshold=48 全局切换 |
15	| native FP4 MMA / QuTLASS | ❌ 无法使用 | sm_120 限制（见下文负结果） |
16	
17	
18	## 1. Baseline 定义
19	
20	这里必须区分三种 baseline，不能混着说。
21	
22	| 名称 | 含义 | 当前状态 |
23	|---|---|---|
24	| B0: old Marlin baseline | 未做 atomic/shape-aware/tile 调优的老 Marlin `.so` | 还没有完成本轮公平 e2e / CUDA graph 对比 |
25	| B1: current Marlin + b12x baseline dispatch | 当前已部署 Marlin `.so`，但 `SGLANG_B12X_DISPATCH_PROFILE=baseline` 使用旧 b12x 阈值 | 已测 |
26	| B2: current Marlin + b12x tuned dispatch | 当前已部署 Marlin `.so`，`SGLANG_B12X_DISPATCH_PROFILE=tuned` 使用新 b12x/shape-aware 分流 | 已测 |
27	| B3: Marlin M=1 graph-tile candidate | 新发现的 M=1 exact-shape Marlin tile 表 | 已测，e2e 回退，默认禁用 |
28	
29	当前部署产物：
30	
31	```text
32	32d27c728ea93203236757d7534b6e68  /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/sgl_kernel/sm100/common_ops.abi3.so
33	32d27c728ea93203236757d7534b6e68  /user_4813494d/openbmb/demo-sala/common_ops.abi3.so
34	```
35	
36	注意：
37	
38	- 之前我口头说的 fresh baseline 是 B1，不是 B0。
39	- `.cu12bak` 当前 md5 是 `5b768fb3708ed2c15ffe5601db3b5f45`，它是部署过程备份，不等价于 old Marlin baseline。
40	- 78MB 的 `common_ops.abi3.so.bak` 涉及旧 cu12/旧打包，不适合直接当公平性能 baseline；若要测 B0，应从明确的 old Marlin 源码/patch 点重新 build 一个 cu13 `.so`。
41	
42	备份源码位置：
43	
44	```text
45	/user_4813494d/backups/cu12-baseline-20260420/packages/sglang-minicpm/sgl-kernel/csrc/gemm/marlin/gptq_marlin.cu
46	```
47	
48	这里的 old Marlin C++ 仍有：
49	
50	```cpp
51	bool part_use_atomic_add = use_atomic_add && div_ceil(prob_m_split, 64) * prob_n <= 2048;
52	```
53	
54	因此对 `N=4096/4608/12288/32768` 的 decode 基本禁用 atomic。当前 Marlin 的关键改动之一是把小 M decode 纳入 atomic 路径。
55	
56	## 2. 已测 e2e 结论
57	
58	约束：no-spec，只测允许的 `3*S1 8*S8 0*Smax`。
59	
60	| 对比项 | S1 | S8 | Smax |
61	|---|---:|---:|---:|
62	| B0 old Marlin cu13 `.so` + b12x tuned dispatch | `275.70s` | `293.04s` | `0.00s` |
63	| B1 current Marlin + b12x baseline dispatch | `266.44s` | `284.57s` | `0.00s` |
64	| B2 current Marlin + b12x tuned dispatch | `266.57s` | `284.37s` | `0.00s` |
65	
66	结论：
67	
68	- B1 和 B2 基本持平。
69	- 这个结果只能说明 b12x/shape-aware 分流没有兑现 e2e 提升。
70	- 它不能回答“old Marlin vs tuned Marlin 有没有提升”，因为 B1/B2 用的是同一个已部署 Marlin `.so`。
71	- B0 和 B2 的公平 no-spec e2e 对比显示：当前 Marlin 比 old Marlin 快，S1 少 `9.13s`，S8 少 `8.67s`，约 `3.0%~3.3%` duration 改善。
72	
73	B0 old Marlin 产物：
74	
75	```text
76	77a3a9fb3aad222714a43ede4776596d  /user_4813494d/openbmb/outputs/marlin_b0_20260425_101153/common_ops.old_marlin_cu13.abi3.so
77	```
78	
79	对应 B0 e2e 日志：
80	
81	```text
82	/user_4813494d/openbmb/outputs/marlin_b0_20260425_101153/b0old_mini_bench_3s1_8s8_0smax_manual_*.log
83	```
84	
85	## 3. CUDA Graph Profiling 结论
86	
87	方法：使用 SGLang profiler 捕获 `EXTEND` / `DECODE` trace，解析 kernel event，不依赖 Python 层 `apply()` 计数。
88	
89	Decode trace 结果：
90	
91	| 项 | B1 baseline dispatch | B2 tuned dispatch |
92	|---|---:|---:|
93	| DECODE total GPU kernel time | `299.306 ms` | `299.425 ms` |
94	| Marlin time | `167.053 ms` | `167.112 ms` |
95	| Marlin 占比 | `55.81%` | `55.81%` |
96	| Marlin calls | `5120` | `5120` |
97	
98	Extend trace 结果：
99	
100	| 项 | B1 baseline dispatch | B2 tuned dispatch |
101	|---|---:|---:|
102	| EXTEND total GPU kernel time | `1628.944 ms` | `1609.674 ms` |
103	| b12x/CuteDSL time | `769.847 ms` | `750.131 ms` |
104	
105	诊断：
106	
107	- tuned dispatch 在 prefill/extend 有小幅收益，约 `19.7 ms` kernel time。
108	- no-spec S1/S8 的 e2e 主体是长 decode；decode graph 内 Marlin 时间完全没变。
109	- 因此 B2 不快的直接原因是：优化发生在 prefill/dispatch，主耗时路径 decode graph Marlin 没有变化。
110	
111	B3 e2e 结果（已在 §2 汇总）：B3 直接回退，不能进入默认路径。当前已把部署 `.so` 回滚到 `32d27c728ea93203236757d7534b6e68`。源码中的 exact tile 表保留为实验项，但默认由 `SGLANG_MARLIN_M1_EXACT_TILE=0` 禁用。
112	
113	## 4. Old-Emulated Marlin 对比
114	
115	初步以 old-emulated CUDA graph microbench（强制旧 tile `{K=128,N=128,T=256,B=1}` + 关闭 atomic）先验证方向：old Marlin -> current Marlin 在 microbench 上有提升，主要来自小 M atomic。B1 -> B2 没提升，是因为 b12x tuned 没改变 decode Marlin replay。此结果由 §4.1 真正 B0 e2e 所取代。
116	
117	## 4.1 B0 old `.so` 与 Current Marlin 归因
118	
119	在 `2026-04-25` 已补做真正 B0 old-Marlin cu13 `.so`：
120	
121	```text
122	77a3a9fb3aad222714a43ede4776596d  /user_4813494d/openbmb/outputs/marlin_b0_20260425_101153/common_ops.old_marlin_cu13.abi3.so
123	```
124	
125	同机、同参数 CUDA graph microbench：
126	
127	| shape | M | B0 old `.so` | current | current no-small-atomic | old-tile + atomic | old-tile barrier |
128	|---|---:|---:|---:|---:|---:|---:|
129	| `std_o` | 1 | `10.250 us` | `8.199 us` | `10.246 us` | `8.180 us` | `10.258 us` |
130	| `std_o` | 8 | `10.244 us` | `8.194 us` | `10.250 us` | `8.183 us` | `10.249 us` |
131	| `std_qkv` | 1 | `10.242 us` | `6.298 us` | `10.244 us` | `6.314 us` | `10.241 us` |
132	| `std_qkv` | 8 | `10.240 us` | `8.182 us` | `10.251 us` | `8.181 us` | `10.232 us` |
133	| `gla_qkv` | 1 | `12.293 us` | `12.252 us` | `12.336 us` | `12.293 us` | `12.305 us` |
134	| `gla_qkv` | 8 | `12.291 us` | `12.301 us` | `14.334 us` | `12.300 us` | `12.299 us` |
135	| `gate_up` | 1 | `25.114 us` | `22.520 us` | `22.520 us` | `24.624 us` | `25.797 us` |
136	| `gate_up` | 8 | `26.622 us` | `22.560 us` | `22.587 us` | `25.917 us` | `26.617 us` |
137	| `down` | 1 | `18.428 us` | `14.323 us` | `20.603 us` | `14.441 us` | `18.434 us` |
138	| `down` | 8 | `18.435 us` | `14.353 us` | `22.274 us` | `16.374 us` | `18.449 us` |
139	
140	归因结论：
141	
142	- `std_o` / `std_qkv`：收益几乎全部来自 small-M atomic；关闭 `SGLANG_MARLIN_ATOMIC_SMALL_M` 后退回 old `.so` 水平。
143	- `down`：收益主要来自 small-M atomic，同时 tile 也有少量贡献；关闭 small-M atomic 后甚至比 old `.so` 更慢。
144	- `gate_up`：收益主要来自 shape-aware tile；关闭 small-M atomic 基本不影响，强制 old tile 会明显变慢。
145	- `gla_qkv`：当前 Marlin 对它基本没收益，且 no-small-atomic 在 M=8 上有回退风险；后续不要优先动。
146	
147	这解释了为什么 B0 -> current 有约 `3%` e2e 收益：std/down/qkv 的 atomic 和 gate_up 的 tile 共同贡献；而 B1 -> B2 不动，是因为 b12x 分流没有改变这些 decode graph Marlin replay 内核。
148	
149	## 5. b12x / Shape-Aware 做了什么
150	
151	`demo-sala/sglang/python/sglang/srt/layers/quantization/b12x_fp4.py` 当前新增了 dispatch profile：
152	
153	- `SGLANG_B12X_DISPATCH_PROFILE=baseline|tuned`
154	- baseline 复现旧阈值和旧 CUTLASS override。
155	- tuned 根据离线 b12x/CUTLASS/Marlin crossover 调整：
156	  - `std_o/std_qkv` Marlin 上界放到 `M<=32`
157	  - `down` 放到 `M<=24`
158	  - `gate_up` 保持 `M<=16`
159	  - `gla_qkv` 放到 `M<=24`
160	  - 部分大 M bucket 强制 CUTLASS，绕开 b12x 不占优的点
161	
162	同时加了 b12x 预编译缓存：
163	
164	- `SGLANG_B12X_PRECOMPILE=1`
165	- `SGLANG_B12X_PRECOMPILE_PROFILE=nospec-mini`
166	- `CUTE_DSL_CACHE_DIR=/user_4813494d/openbmb/bench/b12x/cache/cute_dsl`
167	
168	这解决的是 capture/build 抖动，不是 decode replay 热点。
169	
170	为什么没有提升：
171	
172	- no-spec decode 的有效 M 是 `1` 或 `8`。
173	- 这些 M 档位在 baseline/tuned dispatch 下都仍然走 Marlin。
174	- Python 分流只在 prefill 和 CUDA graph capture 时执行；graph replay 阶段不重新走 Python 分流。
175	- 因此 tuned dispatch 不会改变每个 decode token replay 的 Marlin kernel。
176	
177	## 6. 已排除方向
178	
179	### 6.1 Python route profiling 不能当最终依据
180	
181	`SGLANG_B12X_PROFILE` 只覆盖 `apply()` 执行阶段，decode graph replay 不走 Python，不能用它解释最终 decode 吞吐。
182	
183	### 6.2 `use_fp32_reduce=False` 没有 replay 收益
184	
185	生产 shape 上 `fp32_reduce=True/False` 的 CUDA graph replay 时间全部在约 `0.1%` 内，不能作为优化方向。decode 小 M 已走 atomic 路径，基本不触发 barrier global reduce，关 fp32 reduce 只影响极少量路径。
186	
187	## 7. 新发现：M=1 Marlin Tile 才是当前抓手
188	
189	按用户要求，重新以 CUDA graph replay 计时做 tile sweep，结果：
190	
191	| shape | M | 当前 auto | best | speedup |
192	|---|---:|---:|---:|---:|
193	| `std_o` | 1 | `8.184 us` | `k128_n256_t256_b1 = 6.265 us` | `1.306x` |
194	| `std_qkv` | 1 | `6.375 us` | `k064_n128_t128_b2 = 6.148 us` | `1.037x` |
195	| `gla_qkv` | 1 | `11.783 us` | `k064_n128_t128_b2 = 11.402 us` | `1.033x` |
196	| `gate_up` | 1 | `22.512 us` | auto | `1.000x` |
197	| `down` | 1 | `14.335 us` | `k064_n256_t256_b2 = 14.329 us` | `1.000x` |
198	| `std_o` | 8 | `8.195 us` | `k128_n128_t256_b1 = 8.187 us` | `1.001x` |
199	| `std_qkv` | 8 | `8.186 us` | `k128_n128_t256_b1 = 8.183 us` | `1.000x` |
200	| `gla_qkv` | 8 | `12.290 us` | `k128_n128_t256_b1 = 12.289 us` | `1.000x` |
201	
202	结论：
203	- S8 的 M=8 decode 基本没有 tile 空间。
204	- S1 的 M=1 decode 有真实空间，尤其 `std_o`。
205	- 下一步应该只动 M=1 exact-shape Marlin tile 表，避免影响 M=8。
206	
207	## 10. M=1 Exact Tile Per-Shape Gate
208	
209	B3 失败的直接教训是：不能用一个总开关同时打开 `std_o/std_qkv/gla_qkv` 的 M=1 exact tile。当前已把外部 sgl-kernel 源码改成 per-shape gate，默认仍关闭：
210	
211	```text
212	SGLANG_MARLIN_M1_EXACT_TILE=0
213	SGLANG_MARLIN_M1_STD_O_TILE=0
214	SGLANG_MARLIN_M1_STD_QKV_TILE=0
215	SGLANG_MARLIN_M1_GLA_QKV_TILE=0
216	```
217	
218	candidate `.so` 已备份并恢复为 stable `.so`。离线 microbench 结果：`std_o M=1` 节省约 `0.64 us/call`（按层加权约 `1.81%` M=1 Marlin 本地收益）；`std_qkv M=1` 节省约 `0.09 us/call`（层数少，权重低）；`gla_qkv M=1` 轻微回退。
219	
220	结论：
221	
222	- `std_o M=1` 是唯一还有意义的 exact-tile 候选，但收益只占 M=1 Marlin 本地约 `1.8%`。
223	- `std_qkv M=1` 层数只有 8，权重太小，单独默认打开价值很低。
224	- `gla_qkv M=1` 不再默认研究；B3 已显示它有回退风险。
225	- 在没有服务级 e2e 证据前，per-shape gate 只能保留为实验项，不能默认启用。
226	
227	## 11. Decode Kernel Hotspot After Marlin
228	
229	基于 B2 tuned S8short DECODE trace，只统计 GPU kernel event：
230	
231	| class | calls | GPU time | pct |
232	|---|---:|---:|---:|
233	| Marlin | `5120` | `167.112 ms` | `56.17%` |
234	| elementwise misc | `13752` | `24.617 ms` | `8.28%` |
235	| BF16 CUTLASS GEMM | `288` | `20.831 ms` | `7.00%` |
236	| index_put | `1333` | `16.007 ms` | `5.38%` |
237	| vectorized_gather | `768` | `13.623 ms` | `4.58%` |
238	| RMSNorm | `4384` | `9.833 ms` | `3.31%` |
239	| compress_k | `512` | `9.003 ms` | `3.03%` |
240	| topk/sort | `768` | `8.452 ms` | `2.84%` |
241	| fused recurrent GLA | `768` | `7.429 ms` | `2.50%` |
242	| attention split/paged-kv | `512` | `12.159 ms` | `4.09%` |
243	
244	宏观判断：
245	
246	- Marlin 仍是最大项，但 B0 -> current 已经拿到约 `3%` e2e；继续 exact tile 的理论收益已经很小。
247	- M=1 exact tile 的 `std_o+std_qkv` 候选只省约 `38 us/decode step`，约 `1.9%` M=1 Marlin 本地收益，折到 e2e 很可能低于 `1%`。
248	- 后续更值得看的 kernel 侧方向：
249	  - BF16 CUTLASS GEMM：大概率是 lm_head/logits 类路径，单项约 `7%` decode GPU time，但涉及精度/答案风险。
250	  - KV/cache gather + index_put：合计接近 `10%` decode GPU time，可能来自 cache/table 更新和稀疏路径元数据搬运，优化潜力比继续 Marlin tile 更高。
251	  - elementwise misc：调用多但单 kernel 小，适合找可融合链路，不适合盲写大 kernel。
252	
253	当前不做 e2e 时，下一步只能做 kernel-side/read-only 归因：定位 BF16 CUTLASS GEMM、gather/index_put 分别来自哪段 Python/CUDA graph 捕获路径，再决定是否写替换 kernel。
254	
255	## 12. compress_k Head-Parallel Rewrite
256	
257	源码归因：`compress_k` 热点来自 `minicpm_sparse_kernels.py`；原 kernel 启动 grid `(batch, chunk, head)`，但每个 head program 存在控制流冗余（history 路径只有 `head_idx==0` 处理所有 head；new chunk 路径同理）。修改后每个 `head_idx` program 只负责自己的 head，同步改了 padded / non-padded 两路，主路径是 non-padded（`split_stage1=false`）。
258	
259	CUDA graph microbench 与 PyTorch reference correctness 已验证，padded correctness smoke：`bs=1/8, k1/k2, history=64, new=1: out_diff=0.0, key_diff=0.0`。
260	
261	| case | k | old graph | new graph | speedup | correctness |
262	|---|---|---:|---:|---:|---|
263	| bs=1, history=512, new=1 | k1 32/16 | `8.228 us` | `4.129 us` | `1.99x` | 0 diff |
264	| bs=1, history=512, new=1 | k2 128/64 | `59.420 us` | `32.809 us` | `1.81x` | 0 diff |
265	| bs=8, history=512, new=1 all rows | k2 128/64 | `58.152 us` | `38.405 us` | `1.51x` | 0 diff |
266	
267	解释：history-only 路径基本不变；new chunk 有边界时收益明显（k2 约 1.5×~1.8×），因为旧实现对 `kernel_size=128` 做了冗余 mean pooling。new compressed chunk 不是每步都有（k1 约每 16 token 一次，k2 约每 64 token 一次），这项优化是”去掉尖峰成本”而非稳定节省；折到 e2e 的预期收益小于 Marlin B0→current 的 `3%`，但比继续压 M=1 Marlin tile 更确定。
268	
269	## 13. SimpleGLA Direct-State Decode
270	
271	继续沿着 decode GPU hotspot 看，`vectorized_gather` + `fused_recurrent_fwd_kernel` + `index_put` 的序列基本定位到 SimpleGLA recurrent state：
272	
273	```python
274	initial_state = layer_cache.temporal[mamba_indices, :].contiguous()
275	o, final_state = fused_recurrent_simple_gla(..., initial_state=initial_state)
276	layer_cache.temporal[mamba_indices, :] = final_state
277	```
278	
279	对应代码在 `demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py` 的 SimpleGLA decode 分支。当前模型有 24 个 `lightning-attn` 层：
280	
281	```text
282	lightning-attn layers = [1,2,3,4,5,6,7,8,10,11,12,13,14,15,18,19,20,21,23,24,25,26,27,28]
283	```
284	
285	修改：
286	
287	- 扩展 `demo-sala/sglang/python/sglang/srt/layers/attention/simple_gla_decode_kernel.py`，新增 `simple_gla_decode_update_fwd()`。
288	- 新 kernel 直接从 `temporal[state_indices]` 读 recurrent state，在 kernel 内写回更新后的 state。
289	- 同时使用 `BK=BV=128` 的 decode tile，避免 FLA 默认 `64x64` 切成 4 个 tile 后再做 `sum(0)`。
290	- 接入 no-spec decode 路径；`target_verify` / spec 路径不动。
291	- 保留关闭开关：`SGLANG_SIMPLE_GLA_DIRECT_DECODE=0`。
292	
293	CUDA graph replay 结果：
294	
295	| batch | old generic path | direct-state path | speedup | output diff | state diff |
296	|---:|---:|---:|---:|---:|---:|
297	| 1 | `14.380 us` | `6.164 us` | `2.33x` | `5.96e-08` | `0.0` |
298	| 8 | `34.860 us` | `14.366 us` | `2.43x` | `0.00390625` | `0.0` |
299	
300	解释：
301	
302	- `state diff = 0` 说明 recurrent state 更新与旧路径一致。
303	- bs=8 的 output diff 是 bf16 量级，来自 `K=128` 单 tile 与旧 `64x64` 分块后求和的累加顺序差异。
304	- 这个优化直接覆盖 trace 中的 `vectorized_gather`、`fused_recurrent_fwd_kernel`、`index_put` 三段组合，而不是只改其中一个 PyTorch indexing kernel。
305	- 这是目前比继续 Marlin M=1 tile 更高杠杆的 no-spec decode kernel 侧优化。
306	
307	状态：已做 `py_compile`、CUDA graph correctness/timing、用户手跑 no-spec e2e。
308	
309	## 14. Non-Spec E2E Result After Kernel-Side Fixes
310	
311	用户在 `2026-04-25` 手动跑了 `3*S1 8*S8 0*Smax` no-spec e2e（S1: `248.53s`，S8: `265.63s`）。
312	
313	对比本轮修改前的 tuned no-spec：
314	
315	| case | before tuned | after kernel-side | duration delta | speedup |
316	|---|---:|---:|---:|---:|
317	| S1 | `266.57s` | `248.53s` | `-18.04s / -6.77%` | `1.073x` |
318	| S8 | `284.37s` | `265.63s` | `-18.74s / -6.59%` | `1.071x` |
319	
320	对比真正 old Marlin baseline：
321	
322	| case | B0 old Marlin | after kernel-side | duration delta |
323	|---|---:|---:|---:|
324	| S1 | `275.70s` | `248.53s` | `-27.17s / -9.85%` |
325	| S8 | `293.04s` | `265.63s` | `-27.41s / -9.35%` |
326	
327	结论：
328	
329	- 当前收益不是 b12x/shape-aware dispatch 贡献的；那条此前已经证明基本持平。
330	- old Marlin -> current Marlin 约 `3%`。
331	- 本轮非 Marlin kernel-side 修改又给 no-spec e2e 带来约 `6.6%~6.8%` duration 改善（§15 已用 DECODE trace 确认来源）。
332	
333	## 15. Short DECODE Trace Confirmation
334	
335	本节只使用短 DECODE trace（CUDA graph 内 kernel 时间），不做全量 e2e。两份 trace 序列分布不一致（old tuned: ~32 steps，new direct-state: ~16 steps），采用 Marlin 调用数做 per-step 归一化。
336	
337	核心 per-step 对比：
338	
339	| class | old tuned | new direct-state | interpretation |
340	|---|---:|---:|---|
341	| Marlin | `5.2222 ms/step` | `4.8839 ms/step` | Marlin 仍是 decode graph 最大项 |
342	| `vectorized_gather` | `0.4257 ms/step` | gone from top classes | 被 direct-state 读 state 替掉 |
343	| generic `fused_recurrent_fwd_kernel` | `0.2322 ms/step` | gone | 被 SimpleGLA direct kernel 替掉 |
344	| `index_put` | `0.5002 ms/step` | `0.1066 ms/step` | recurrent state 写回大幅减少，仍有少量其他 index kernel |
345	| `_simple_gla_decode_update_kernel` | absent | `0.4672 ms/step` | 新 kernel，合并读 state、GLA recurrence、写 state |
346	| SimpleGLA state path subtotal | `1.1581 ms/step` | `0.5738 ms/step` | `-0.5843 ms/step`，约 `50%` local reduction |
347	| `compress_k_complete_kernel_new` | `0.2814 ms/step` | `0.3995 ms/step` | 这份短 trace 新 chunk 分布不同，不能从 e2e trace 证明 compress_k 收益 |
348	| attention split / paged-kv | `0.4042 ms/step` | `1.6976 ms/step` | 受序列长度 / split-kv 分布影响，不作为本轮优化归因 |
349	
350	结论：
351	
352	- 本轮 e2e 下降的主因已经在 CUDA graph trace 中确认：SimpleGLA no-spec decode 的 gather / generic recurrent / index_put 链路被替换，graph 内实测每 step 省约 `0.58 ms`。
353	- `compress_k` rewrite 的 microbench 是正收益，但短 trace 里没有形成稳定下降；原因是它只在 new compressed chunk 边界处省尖峰，是否反映到短 profile 取决于采样到的序列位置。
354	- 因此目前要把本轮收益归因到 SimpleGLA direct-state decode，而不是 b12x dispatch，也不是 Marlin tile 本身。
355	- 下一步如果继续 kernel 侧优化，应按 decode graph 排序继续打最大项：Marlin 仍是第一项，其次是 attention split / paged-kv 的长上下文分布问题；`compress_k` 只作为边界尖峰优化继续保留。
356	
357	## 16. Fixed-Input S8 Decode Trace
358	
359	采样分布：S8 sampled n=8，prompt_tokens avg=70136 min=613 max=135664，output_len=128，profile decode steps=16。
360	
361	CUDA graph 内 per-step 结果：
362	
363	| class | calls/step | ms/step |
364	|---|---:|---:|
365	| Marlin | `160.0` | `4.9032` |
366	| attention split/paged-kv | `24.0` | `1.7541` |
367	| SimpleGLA direct | `24.0` | `0.4748` |
368	| BF16/CUTLASS GEMM | `1.0` | `0.4588` |
369	| compress_k | `16.0` | `0.4037` |
370	| elementwise/reduce misc | `182.0` | `0.3674` |
371	| RMSNorm | `137.0` | `0.3025` |
372	| topk/sort | `24.0` | `0.2692` |
373	| sparse metadata | `48.0` | `0.1925` |
374	| index_put | `17.6` | `0.1098` |
375	
376	Marlin variant 分布：
377	
378	| variant | calls/step | ms/step | avg us |
379	|---|---:|---:|---:|
380	| `block=128, thread_k=4, grid=[312,1,1]` | `88` | `4.0899` | `46.476` |
381	| `block=256, thread_k=8, grid=[156,1,1]` | `72` | `0.8134` | `11.297` |
382	
383	attention split/paged-kv 进一步拆开：
384	
385	| kernel | calls/step | ms/step | avg us | source |
386	|---|---:|---:|---:|---|
387	| `flash_fwd_splitkv_stage1_kernel` | `8` | `1.4249` | `178.116` | sparse topk stage1 compressed scoring |
388	| `BatchPrefillWithPagedKVCacheKernel` | `8` | `0.3049` | `38.108` | FlashInfer stage2 sparse paged KV |
389	| `PersistentVariableLengthMergeStatesKernel` | `8` | `0.0243` | `3.036` | stage2 merge |
390	
391	关键结论：
392	
393	- fixed S8 trace 与上一轮 direct-state trace 结构一致，说明 SimpleGLA direct-state 收益不是输入偶然。
394	- decode graph 内看不到 b12x runtime kernel；b12x/shape-aware Python 分流仍不是 no-spec S1/S8 graph replay 的主杠杆。
395	- attention 第二大项不能粗暴归因为 FlashInfer paged KV wrapper。最大子项是 `infllmv2_attn_stage1` 触发的 `flash_fwd_splitkv_stage1_kernel`，也就是 sparse topk 的 stage1 scoring。
396	
397	## 17. Attention Stage1/Stage2 Negative Tests
398	
399	stage2 wrapper 结果：
400	
401	| option | result |
402	|---|---:|
403	| `use_tensor_cores=1` default | `20.84 us` |
404	| `use_tensor_cores=0` | unsupported: `Unsupported group_size: 16` |
405	| `disable_split_kv=1` | `230.45 us` |
406	| `fixed_split_size=8192` | `230.93 us` |
407	
408	解释：MiniCPM sparse stage2 每个 head group 是 `qo_heads=16, kv_heads=1`；FlashInfer non-TC wrapper 不支持 `group_size=16`；`disable_split_kv` 会把 stage2 从约 `21 us` 拉到约 `230 us`。新增的实验开关（`SGLANG_MINICPM_DECODE_TENSOR_CORES` / `_DISABLE_SPLIT_KV` / `_FIXED_SPLIT_SIZE`）默认必须保持当前行为。
409	
410	stage1 sparse topk 结果：
411	
412	| seq_len | max_context_len | baseline graph | `split_stage1` graph | topk overlap |
413	|---:|---:|---:|---:|---:|
414	| `70136` | `524288` | `144.86 us` | `159.58 us` | `0.438` |
415	| `135664` | `524288` | `230.19 us` | `251.04 us` | `0.417` |
416	| `135664` | `135664` | `217.55 us` | `239.10 us` | `0.416` |
417	| `524288` | `524288` | `828.28 us` | `855.71 us` | `0.472` |
418	
419	结论：
420	
421	- `split_stage1` 不是可上线优化：更慢，并且只用 k1 scoring，topk overlap 只有约 `0.42~0.47`，语义风险过高。
422	- max_context padding 不是主要矛盾：`135664` 场景把 `max_context_len` 从 `524288` 降到实际长度只省约 `12.6 us/call`。
423	- 下一轮 attention 侧如果要继续，必须做保持 k1+k2 scoring 语义的 stage1 fused kernel，目标是合并 `infllmv2_attn_stage1 + max_pooling_1d_varlen + topk/sort`，而不是打开已有 `fuse_topk` 或 `split_stage1`。
424	
425	## 18. Marlin Remaining Headroom
426	
427	用已有 graph tile sweep 对照 fixed S8 trace 后，Marlin 的剩余空间基本清楚：
428	
429	核心结果：
430	
431	| shape | M | auto graph | best | speedup |
432	|---|---:|---:|---:|---:|
433	| `std_o` | `1` | `8.184 us` | `6.265 us` | `1.306x` |
434	| `std_o` | `8` | `8.195 us` | `8.187 us` | `1.001x` |
435	| `std_qkv` | `1` | `6.375 us` | `6.148 us` | `1.037x` |
436	| `std_qkv` | `8` | `8.186 us` | `8.183 us` | `1.000x` |
437	| `gla_qkv` | `1` | `11.783 us` | `11.402 us` | `1.033x` |
438	| `gla_qkv` | `8` | `12.290 us` | `12.289 us` | `1.000x` |
439	| `gate_up` | `1` | `22.512 us` | `22.512 us` | `1.000x` |
440	| `gate_up` | `8` | `22.534 us` | `22.534 us` | `1.000x` |
441	| `down` | `1` | `14.335 us` | `14.329 us` | `1.000x` |
442	| `down` | `8` | `14.339 us` | `14.338 us` | `1.000x` |
443	
444	结论：
445	
446	- fixed S8 的主 decode batch 是 M=8；M=8 上 Marlin tile 已接近 sweep 最优，继续靠 tile 很难再明显降低 `4.9 ms/step`。
447	- M=1 只有 `std_o` 还有约 `1.9 us/call` 的 microbench 空间，但调用数有限，折到 no-spec e2e 大概率低于 `1%`。
448	- 因此下一轮真正高杠杆仍不是继续盲扫 Marlin tile，而是：
449	  - 保持 k1+k2 语义的 sparse stage1 fused topk；
450	  - 或回到 b12x/Marlin 重新划分，但必须先证明某些 M=8 shapes 能用 b12x 在 CUDA graph 内赢 Marlin。
451	
452	## 19. Fused TopK Consistency Gate
453	
454	用户提醒 `fused topk` 可能有 bug 后，本轮先做 correctness gate 验证：
455	
456	| case | scenario | official vs fused overlap mean | fused duplicate mean | verdict |
457	|---|---|---:|---:|---|
458	| verify `B=16,Q=5,seq=16384` | random | `0.460` | `0.033` | FAIL |
459	| S1 decode `B=3,Q=1,seq=70136` | random | `0.139` | `0.010` | FAIL |
460	| S8 decode `B=8,Q=1,seq=135664` | random | `0.168` | `0.009` | FAIL |
461	
462	定位：`compressed_attention_tilelang()` 只传 `k1` 进 fused kernel，`k2` 未参与计算，破坏官方 k1+k2 scoring 语义；`k1_ref_vs_fused` overlap 也低，说明 pooling/topk 未对齐 k1-only reference（详见 §22）。
463	
464	结论：当前 `--fuse-topk` 不能上马；已加防误用 guard（传 `--fuse-topk` 直接报错，需 `SGLANG_MINICPM_ALLOW_UNSAFE_FUSE_TOPK=1` 才能调试）。后续若继续做 fused topk，目标必须是复现 `infllmv2_attn_stage1(k1,k2) + pooling + topk` 的完整语义。
465	
466	## 20. TopK Select Candidate Held Back
467	
468	在不启用 fused topk 的前提下，曾尝试一个看似无语义风险的小优化：
469	
470	```python
471	block_score.topk(topk, dim=-1).indices.sort(-1).values
472	```
473	
474	PyTorch `topk` 默认 `sorted=True`，但后面马上按 block index 再 sort，一开始按 score 排序是浪费。改为：
475	
476	```python
477	block_score.topk(topk, dim=-1, sorted=False).indices.sort(-1).values
478	```
479	
480	CUDA graph microbench 结果（fp32 和 bf16 趋势一致）：
481	
482	| dtype | case | sorted=True | sorted=False | speedup | equal |
483	|---|---|---:|---:|---:|---|
484	| fp32 | verify `(2,80,256)` | `24.612 us` | `20.490 us` | `1.201x` | True |
485	| fp32 | S1 decode `(2,3,1096)` | `30.709 us` | `27.949 us` | `1.099x` | True |
486	| fp32 | S8 decode `(2,8,2120)` | `34.804 us` | `30.706 us` | `1.133x` | True |
487	
488	进一步在真实 stage1 score 上固定同一个 `block_score` 对比，`sorted=True/False` 输出也一致。但完整 `compressed_attention` 对拍时发现 `infllmv2_attn_stage1` 自身在 verify/S8 形状上存在 run-to-run topk 抖动，导致难以把这项变更独立证明为严格不改输出。为避免把 tie 行为变化带进主路径，生产默认仍保持 `sorted=True`，该项仅作为候选保留。
489	
490	## 21. Decode Pooling No-Zero
491	
492	`infllm_v2.max_pooling_1d_varlen()` 的 Python wrapper 先分配 `torch.zeros` 输出，再调用 CUDA kernel：
493	
494	```python
495	output = torch.zeros(num_heads, total_q, out_len, device=input.device, dtype=input.dtype)
496	C.max_pooling_1d_varlen(...)
497	```
498	
499	读 C kernel 后确认每个有效 `(head, q, out_block)` 都会被覆写；因此 decode 路径可改为 `torch.empty`，省掉输出清零。为了不改 infllm wheel，只在 `minicpm_sparse_utils.py` 增加 `_max_pooling_1d_varlen_no_zero()`，只在 `max_seqlen_q == 1` 的 decode 路径启用；prefill/verify 继续走原始 wrapper。验证结果：
500	
501	| case | zeros | empty | speedup | equal |
502	|---|---:|---:|---:|---|
503	| verify `B=16,Q=5,seq=16384` | `6.998 us` | `8.138 us` | `0.860x` | True |
504	| S1 decode `B=3,Q=1,seq=70136` | `12.402 us` | `8.158 us` | `1.520x` | True |
505	| S8 decode `B=8,Q=1,seq=135664` | `12.369 us` | `12.440 us` | `0.994x` | True |
506	
507	结论：真实 stage1 score 对拍均等（`pool equal=True, topk equal=True`）；完整 stage1 decode graph 净下降约 `1.0~1.4 us/call`（S8 135664 场景基本持平）。这是一个低风险小 patch，只覆盖 no-spec/S1/S8 decode 的 pooling 子项；折到完整 stage1 graph 后收益很小，不能替代 k1+k2 fused stage1。
508	
509	## 22. k1+k2 Stage1 Semantics
510	
511	继续读 `kernels/infllmv2_cuda_impl` 后，stage1 语义更清楚：
512	
513	- Python wrapper `infllmv2_attn_stage1(q, k, v, ...)` 里 `k` 是 `k1`，`v` 实际传的是 `k2`；它不是普通 attention 的 value 输出。
514	- C++ 入口为 `mha_varlen_fwd_stage1()`，返回的 `p` shape 是 `(num_heads_k, total_q, seqlen_k_rounded)`；MiniCPM 后续把它当作 compressed block score 输入给 pooling。
515	- CUDA kernel 分两段：
516	  - 第一段用 `gC`/`v_ptr`，也就是 `k2`，跑 coarse softmax 并得到 row max/sum；
517	  - 第二段用 `gK`/`k_ptr`，也就是 `k1`，调用 `softmax_rescale_gt()` 复用第一段的 row max/sum，再通过 `hdim16_reduce()` 写出 `k1` score。
518	
519	这解释了为什么 k1-only fused topk 和 `split_stage1=True` 都不对：官方 score 不是单独的 `softmax(q @ k1)`，而是由 `k2` coarse LSE 参与归一化后的 `k1` score。保持语义的真正融合应在 stage1 CUDA epilogue 里做（`hdim16_reduce()` 写 `p` 后直接做 block pooling/topk），而非外挂 k1-only TileLang kernel。
520	
521	## 23. Decode Replay Skip-Fill
522	
523	背景：CUDA graph replay 路径里 `compress_k1` / `compress_k2` 使用预分配 buffer。旧逻辑每个 decode step 都先把整段 replay buffer 填成 `-inf`，再由 `compress_k_complete_kernel_new` 写有效区间。profile 中表现为两批较大的 BF16 `FillFunctor` kernel。
524	
525	本轮改动：
526	
527	- `SGLANG_MINICPM_FILL_COMPRESS_BUFFERS=0` 为默认值，即跳过旧的 replay buffer fill。
528	- `SGLANG_MINICPM_FILL_COMPRESS_BUFFERS=1` 只保留为回退/调试开关。
529	- `eval/start_eagle.sh` 已显式带上该默认开关，避免生产启动路径依赖隐式默认值。
530	
531	验证方法：短输入、固定 batch，只 profile decode graph，避免 e2e 噪声。
532	
533	结果：
534	
535	| 配置 | BF16 FillFunctor calls | BF16 FillFunctor total | per decode step |
536	|---|---:|---:|---:|
537	| fill-on | `288` | `1.480 ms` | `0.0925 ms/step` |
538	| skip-fill | `256` | `0.258 ms` | `0.0161 ms/step` |
539	| 差值 | `-32` | `-1.222 ms` | `-0.0764 ms/step` |
540	
541	关键证据：
542	
543	- fill-on 多出的 `32` 次正好是 `16 decode steps * 2 buffers`。
544	- 多出的两批 kernel 分别是 `grid=[65536,1,1]` 和 `grid=[16384,1,1]`，各 `16` 次，对应 `compress_k1` / `compress_k2` 大 buffer fill。
545	- skip-fill 后剩下的 `256` 次 BF16 fill 都是 `grid=[512,1,1]` 的小 fill，不属于本次目标 buffer。
546	- decode graph 总 kernel 时间从 `155.107 ms / 16 steps` 降到 `153.462 ms / 16 steps`，净下降约 `0.103 ms/step`。
547	
548	结论：skip-fill 已在 CUDA graph decode replay 内移除目标那批 `FillFunctor<c10::BFloat16>` kernel。收益量级明确，但不是下一阶段的主杠杆。
549	
550	## 24. 下一轮高 ROI 方向
551	
552	不要继续围绕 `0.05-0.10 ms/step` 的小 kernel 做局部修剪。现有 profiling 指向一个更难但更有潜力的方向：**把 EAGLE verify 后的 GLA/Mamba state update 从 PyTorch fancy indexing 改成一个语义等价的 fused CUDA/Triton kernel**。
553	
554	已有 profile 证据见 `runtime.md §7`：
555	
556	- target verify GPU 时间主导 spec 路径，draft 只有约 `4.7%`。
557	- 一轮 trace 里两个 `at::index_elementwise_kernel` 合计 `1609 ms`，约 `77.6%` GPU time。
558	- 用 launch-time 重新归因后，`mamba_verify_update` 吃掉 `1181 ms / 98.4%` 的 index kernel 时间；之前归因到 `alloc_sparse_new_positions` 是 GPU end-time 对齐 NVTX 的污染。
559	
560	热点代码在 `hybrid_linear_attn_backend.py:update_mamba_state_after_mtp_verify()`：
561	
562	```python
563	ssm_states[:, dst_state_indices, :] = intermediate_state_cache[
564	    :, src_state_indices, last_steps
565	].to(ssm_states.dtype, copy=False)
566	
567	ssm_states[:, dst_track_indices, :] = intermediate_state_cache[
568	    :, src_track_indices, track_steps
569	].to(ssm_states.dtype, copy=False)
570	```
571	
572	难点：
573	
574	- `ssm_states` 是所有 GLA 层共享的多层 state cache，维度大，写入目标是 request cache slot。
575	- `accepted_steps` / `mamba_steps_to_track` 每轮动态变化，且必须和 verify/rollback 语义一致。
576	- 当前 PyTorch 写法会生成大量 gather + scatter index kernel；替换后必须逐项对拍 state，而不是只看输出文本。
577	
578	建议路线：
579	
580	1. 先写离线 microbench + correctness harness，固定真实形状，比较 PyTorch fancy indexing 和 fused kernel 后的 `ssm_states` bit/近似一致性。
581	2. 首版 kernel 只覆盖 SALA 当前 `conv_states is None` 的主路径：把 main scatter 和 track scatter 合并为 1 到 2 个 Triton/CUDA kernel。
582	3. 接入时加 env gate，例如 `SGLANG_MINICPM_FUSED_MAMBA_VERIFY_UPDATE=1`，先只在 EAGLE verify 路径打开。
583	4. 验证顺序：state tensor 对拍 -> no-spec/spec 小样本一致性 -> profile 中 index kernel 是否下降 -> 最后再做受限 e2e。
584	
585	这是下一轮最值得攻的点：它难度比 skip-fill / topk sorted / no-zero pooling 高很多，但 profile 中占比足够大，成功后才可能带来真正可见的吞吐改善。
586	
587	## 25. Current Marlin `.so` 与 EAGLE Draft CUDA Graph 不兼容
588	
589	> 2026-04-26 确认
590	
591	在 §4.1 中确认收益的 `32d27c728ea93203236757d7534b6e68`（current Marlin，含 small-M atomic + shape-aware tile）**会导致 EAGLE-3 draft CUDA graph capture 挂住**（37% 进度卡死）。
592	
593	时间线：
594	
595	| 时间点 | env `.so` | EAGLE draft graph |
596	|---|---|---|
597	| probe-sala/prepare_env.sh 部署后 | `220c18cc`（probe-sala，Apr 21） | 正常 |
598	| 换成 demo-sala `.so` 做 Marlin bench | `32d27c7`（demo-sala，Apr 25） | **挂住** |
599	| 恢复 `220c18cc` | `220c18cc` | 正常 |
600	
601	诊断：
602	
603	- `32d27c7` 比 `220c18cc` 大 562 KB，主要差异是 small-M atomic 路径和 shape-aware tile 表。
604	- marlin-tuning.md 所有 Marlin e2e 测试（§2, §4.1）都在 **no-spec** 下做的，从未用 EAGLE draft graph capture 验证过该 `.so`。
605	- CLAUDE.md 中 "draft CUDA graph capture 有观察到明显退化" 的根因就是这个 `.so`。
606	- `probe-sala/common_ops.abi3.so`（`220c18cc`）是目前唯一被验证可以正常 EAGLE 起服的 `.so`。
607	
608	结论：
609	
610	- **Marlin 3%（§2, §4.1）在 EAGLE 生产路径下不可用。** draft graph capture 过程中 Marlin kernel 的 atomic/tile 行为和 CUDA graph capture 有不明冲突。
611	- 当前生产部署必须使用 `220c18cc`。`demo-sala/common_ops.abi3.so` 已替换为 `220c18cc`。
612	- 如果后续要恢复 Marlin 3%，必须逐项 bisect small-M atomic vs shape-aware tile，找到和 draft graph capture 冲突的具体改动，而不是整体替换 `.so`。
613	
614	## 26. SimpleGLA Direct-State Decode 捞回与 EAGLE E2E 验证
615	
616	> 2026-04-26 从 main 捞回并验证
617	
618	§13 的 SimpleGLA direct-state decode 在 `demosala-rollback` 中被丢失（rollback 到 9a7e04c 时只有 127 行的旧 `simple_gla_decode_kernel.py`）。本轮从 main 捞回并接入生产路径。
619	
620	改动文件：
621	
622	1. `demo-sala/sglang/python/sglang/srt/layers/attention/simple_gla_decode_kernel.py` — 从 main 恢复（127 → 286 行），包含 `simple_gla_decode_update_fwd()`。
623	2. `demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py` — 三处改动：
624	   - 添加 `import simple_gla_decode_update_fwd`
625	   - `__init__` 中添加 `self._simple_gla_direct_decode` flag（读 `SGLANG_SIMPLE_GLA_DIRECT_DECODE` 环境变量，默认 `"1"` 开启）
626	   - GLA forward decode 分支：`use_direct_decode` 条件短路，直接调用 `simple_gla_decode_update_fwd()` 替代 `fused_recurrent_simple_gla` + gather/index_put 链路
627	
628	环境变量：`SGLANG_SIMPLE_GLA_DIRECT_DECODE=1`（`eval/start_eagle.sh` 已设置）。`=0` 可关闭回退到旧路径。
629	
630	离线复现（CUDA graph microbench）：
631	
632	| batch | 旧 generic (us) | 新 direct (us) | speedup | output diff | state diff |
633	|---:|---:|---:|---:|---:|---:|
634	| 1 | 14.38 | 6.16 | **2.33×** | 0.0 | 0.0 |
635	| 8 | 34.84 | 10.28 | **3.39×** | 6.1e-05 | 0.0 |
636	
637	与 §13 原始记录高度一致，bs=8 甚至优于原记录（10.28 vs 14.37 us）。
638	
639	EAGLE E2E 验证：用户确认 EAGLE-3 spec 路径起服正常、draft CUDA graph capture 通过。该优化只接入 no-spec decode 分支（`forward_mode.is_decode()` + `head_dim == 128`），不影响 target_verify / spec 路径。
640
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/quantization.md"
}
```

> TOOL

tool_result Read
```
1	# 量化与 Marlin
2	
3	## 1. NVFP4 量化方案
4	
5	**算法**：GPTQ + FourOverSix（adaptive 4/6 block scale），`lm_head` Identity patch  
6	**校准**：wikitext loguniform 128 samples，8 buckets（512-64K log-uniform）  
7	**推理要求**：`--dense-as-sparse`（dense_len=0，全序列走 sparse TopK 路径）
8	
9	### 校准实验结果
10	
11	| Config | Calibration | max_length | FourOverSix | dense-as-sparse | ori_accuracy |
12	|---|---|---|---|---|---|
13	| baseline | calib90 (eval mix) | 24K | ❌ | ✅ | 80.27%（不稳定） |
14	| **chosen** | **loguniform 128 (wikitext)** | **48K** | **✅** | **✅** | **79.98%** |
15	| exp | loguniform 128 | 48K | ✅ | ❌ | 78.18% |
16	| exp | calib90 | 72K | ✅ | ✅ | 77.04%（不达标） |
17	
18	## 2. FourOverSix (4/6) 实现
19	
20	MIT-HAN Lab 方案。标准 NVFP4 固定 block scale÷6；FourOverSix 对每个 block 比较 scale=4 和 scale=6 的 MSE，选更小者。输出格式不变（4-bit FP4 权重 + FP8 block scales），zero throughput impact。
21	
22	```python
23	scale_4 = fp8(scale_6.float() * 1.5)    # scale=4: 权重映射到 [-4, 4]
24	mse_6 = sum((W_group - dequant(W_group, scale_6))^2)
25	mse_4 = sum((W_group - dequant(W_group, scale_4))^2)
26	new_scale = where(mse_4 < mse_6, scale_4, scale_6)
27	```
28	
29	实测 40-43% blocks 选 scale=4；MLP 层比 Attention 层获益更大。
30	
31	### 集成方式
32	
33	直接 patch `llmcompressor/modifiers/quantization/gptq/gptq_quantize.py`，在 observer 输出 scale 后、GPTQ 优化循环前插入 scale 选择。`prepare_env.sh` 用 `cp patches/gptq_quantize_fouroversix.py $GPTQ_TARGET` 覆盖。
34	
35	## 3. Hybrid Marlin/CUTLASS Dispatch
36	
37	Target model decode 时 M 小 → Marlin W4A16（BF16 activation）显著快于 CUTLASS W4A4。
38	
39	**当前策略**：全局阈值 `SGLANG_MARLIN_DECODE_THRESHOLD=48`。M ≤ 48 → Marlin；M > 48 → CUTLASS。
40	
41	### 实现
42	
43	- `process_weights_after_loading`：CUTLASS prep 先跑，然后 `_prepare_hybrid_marlin` 从原权重创建 Marlin 格式。两种格式共存，额外 VRAM ~4 GB。
44	- `apply()`：M ≤ threshold → Marlin；否则 → CUTLASS。CUDA graph safe。
45	
46	**b12x 2-tier dispatch**（开发完成，当前未启用）：已通过正确性验证（见 [`kernels-sm120.md §7.4`](kernels-sm120.md)），但 `SGLANG_ENABLE_B12X` 默认为 0，当前提交包不启用。启用后走 per-shape Marlin/b12x/CUTLASS 三路分流，draft model 不兼容 b12x 始终走纯 Marlin。
47	
48	### sgl-kernel 修复
49	
50	平台 sgl-kernel 0.3.20 的 `marlin_template.h` 有 FP4 scale `/2` bug（cos_sim 0.77）。修复：pre-built `common_ops.abi3.so`（SM120a）via `cp` 替换。
51	
52	### Draft Model
53	
54	Draft model 永远用**纯 Marlin（no hybrid）**，M=1-6 时 CUTLASS 比 BF16 还慢：
55	
56	| Layer | Marlin | CUTLASS | 倍率 |
57	|---|---|---|---|
58	| gate_proj (N=16384) | 16.4 us | 48 us | 2.9× |
59	| down_proj (K=16384) | 20.5 us | 154 us | 7.5× |
60	| o_proj (4096×4096) | 10.3 us | 41 us | 3.9× |
61	
62	实现：`_detect_draft_model_quantization()` 检测到 FP4 draft 时设 threshold=9999。
63	
64	## 4. Marlin 调优负结果（勿重复踩坑）
65	
66	| 方向 | 结论 | 原因 |
67	|---|---|---|
68	| pipe_stages 4→6 | gate_up +5-8%，其余 0%，e2e <0.5% | down 撞 HBM roofline；qkv/o L2 驻留变 compute-bound |
69	| `use_fp32_reduce=False` | M=4-8 退化 9-17% | dispatcher 走不同 tile |
70	| native FP4 MMA (mma.kind=nvf4) | 不可行 | PTX 要求 A+B 都必须 FP4，无 W4A16 路径 |
71	| tile/warp sweep | 无意义 | HMMA:HFMA2 = 1:11，换 tile 不改 HFMA2 数量 |
72	| gn-kernels dequant 手优化 | 无货可抄 | gn-kernels 用 native MMA，没有 dequant 代码 |
73	| QuTLASS MXFP4 | 未测 | sm_120a 原生 Blackwell FP4 MMA，环境匹配未 build |
74	
75	**Pareto 判定**：Marlin 在 sm_120 W4A16 M=1-8 decode 已近最优。继续压 kernel ROI < 2%。
76	
77	### SASS 分析（gate_up M=1）
78	
79	```
80	HMMA (tensor core):                48 条
81	HFMA2+HADD2+HMUL2 (CUDA core FP):  532 条
82	LOP3+SHF+PRMT (FP4→BF16 dequant):  454 条
83	地址计算:                           536 条
84	```
85	
86	HMMA:HFMA2 = 1:11，张量核严重空转。瓶颈是 CUDA core dequant，不是 HBM 或 tensor core。
87	
88	## 5. KV Cache 量化调研
89	
90	- **FP8 KV**（生产）：`--kv-cache-dtype fp8_e5m2`，高并发稳定收益。FlashInfer `BatchDecodeWithPagedKVCacheWrapper` 吃 fp8 buffer + kernel 内 on-the-fly dequant，省 HBM 读带宽
91	- **NVFP4 KV**：在 SALA 当前架构下**没有可落地路径**。老版本"`trtllm_batch_decode_with_kv_cache` 未传 `kv_block_scales`"的结论已过时（FlashInfer 0.6.8 已支持），真正阻塞点是 InfLLM-v2 sparse + page_size=1 的组合。完整调研（API 约束、SGLang fork latent bugs、全球 30+ 项目盘点、离线微基准数据、三条理论路径评估）见 [nvfp4-kv-investigation.md](nvfp4-kv-investigation.md)
92	- **VariableBlockSparseAttentionWrapper**（FlashInfer v0.2）：离线实测对 SALA 现有 `BatchPrefill` baseline 整体打平或略慢，内部 kernel 路径等价，不带来加速
93	
94	## 6. Health check 注意
95	
96	NVFP4 量化后模型在 mcq 强格式约束下会退化为重复 pattern，但 eval regex 仍命中 → `ori_accuracy` 看似正常实则生成垃圾。**健康检查必须用 chat 长样本，不用 mcq。**
97
```

> AGENT

让我从关键源文件中获取更多细节，包括 MARS kernel 的实现和 `eagle_worker` 的动态模式逻辑。

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"NO_SPEC\\|_apply_spec_config\\|SpecMode\\|spec_mode\\|dynamic_mode\\|no_spec\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py | head -40",
  "description": "Find dynamic spec mode lines in eagle_worker.py"
}
```

> TOOL

tool_result Bash
```
12:# mode (D5+D7+NO_SPEC, multiple capture_bs) easily blows past the default
63:from sglang.srt.speculative.spec_mode import (
64:    SpecMode,
65:    SpecModeConfig,
66:    load_config as load_spec_mode_config,
310:        self.spec_mode_config: SpecModeConfig = load_spec_mode_config()
311:        if self.spec_mode_config.enabled:
313:                self.spec_mode_config.d5_steps, self.spec_mode_config.d7_steps
316:                self.spec_mode_config.d5_topk, self.spec_mode_config.d7_topk
342:        # Per-mode swap still happens in _apply_spec_config for the live
344:        if not self.spec_mode_config.enabled:
349:        self._prev_spec_mode: Optional[SpecMode] = None
350:        # Tracks the mode actually applied by _apply_spec_config so we can
354:        self._applied_spec_mode: Optional[SpecMode] = None
388:        With ``spec_mode_config.enabled``, captures one runner per active spec
394:        self.cuda_graph_runner = None  # active runner; mutated by _apply_spec_config
408:        if self.spec_mode_config.enabled:
409:            cfg = self.spec_mode_config
537:            self._prev_spec_mode = None
545:            mode = getattr(batch, "_spec_mode", None)
547:            if mode == SpecMode.NO_SPEC:
548:                self._prev_spec_mode = mode
549:                return self._forward_no_spec(batch)
554:                self._apply_spec_config(mode)
555:            self._prev_spec_mode = mode
579:            # by _apply_spec_config to D5/D7's dtn (or unchanged for static
590:    def _apply_spec_config(self, mode: SpecMode) -> None:
597:        cfg = self.spec_mode_config
600:        if mode == SpecMode.MARS_D5:
604:        elif mode == SpecMode.MARS_D7:
609:            return  # NO_SPEC handled separately
612:        # decode steps once the bs settles. _applied_spec_mode is None on the
615:        if self._applied_spec_mode == mode:
631:        self._applied_spec_mode = mode
633:    def _forward_no_spec(self, batch: ScheduleBatch) -> GenerationBatchResult:
651:        batch.prepare_for_decode(force_no_spec=True)
```

> TOOL

tool_use Bash
```json
{
  "command": "git show f7faed5 --stat && echo \"=== COMMIT MSG ===\" && git log -1 --format=\"%B\" f7faed5",
  "description": "Read the scale loader bug fix commit"
}
```

> TOOL

tool_result Bash
```
commit f7faed59005e86342e39e7fc41c54f1a6e2a9017
Author: SOAR User <[REDACTED]>
Date:   Wed Apr 15 13:25:08 2026 +0000

    fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards
    
    user_4813494d cause: QKVParallelLinear and MergedColumnParallelLinear loaded fused
    per-tensor scales (weight_scale_2, input_scale) into shard_id=0 only,
    leaving remaining slots as torch.empty garbage. Post-load max() absorbed
    the undefined data, corrupting qkv_proj scale and producing Inf/NaN.
    
    Fix: PerTensorScaleParameter.load_fused_per_tensor_weight() broadcasts
    scalar scales to all logical shards, and loads full vectors element-wise.
    Both old (scalar) and new (vector) checkpoint formats are supported.
    
    Also: respect explicit --speculative-draft-attention-backend flag instead
    of always overriding to flashinfer when target uses minicpm_flashinfer.
    
    Verified: flashinfer+graph ON accept_len=1.50 stable, zero NaN across
    all backend/graph combinations (6-config matrix regression).
    
    Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

 .../sglang/python/sglang/srt/layers/linear.py      |   9 +-
 .../sglang/python/sglang/srt/layers/parameter.py   |  24 ++
 .../python/sglang/srt/speculative/eagle_info.py    |   1 +
 .../python/sglang/srt/speculative/eagle_worker.py  |   5 +-
 docs/eagle3-draft-nan-handover.md                  | 467 +++++++++++++++++++++
 tests/test_eagle_fused_scale_loader.py             | 125 ++++++
 6 files changed, 623 insertions(+), 8 deletions(-)
=== COMMIT MSG ===
fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards

user_4813494d cause: QKVParallelLinear and MergedColumnParallelLinear loaded fused
per-tensor scales (weight_scale_2, input_scale) into shard_id=0 only,
leaving remaining slots as torch.empty garbage. Post-load max() absorbed
the undefined data, corrupting qkv_proj scale and producing Inf/NaN.

Fix: PerTensorScaleParameter.load_fused_per_tensor_weight() broadcasts
scalar scales to all logical shards, and loads full vectors element-wise.
Both old (scalar) and new (vector) checkpoint formats are supported.

Also: respect explicit --speculative-draft-attention-backend flag instead
of always overriding to flashinfer when target uses minicpm_flashinfer.

Verified: flashinfer+graph ON accept_len=1.50 stable, zero NaN across
all backend/graph combinations (6-config matrix regression).

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"verify_tree_greedy\\|MARS\\|top2_ratio\\|top2_token\\|mars_theta\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_utils.py | head -20",
  "description": "Find MARS verify in eagle_utils.py"
}
```

> TOOL

tool_result Bash
```
161:def verify_tree_greedy_func(
171:    top2_token: Optional[torch.Tensor] = None,
172:    top2_ratio: Optional[torch.Tensor] = None,
173:    mars_theta: float = -1.0,
176:        from sgl_kernel import verify_tree_greedy
178:        verify_tree_greedy(
187:            top2_token=top2_token,
188:            top2_ratio=top2_ratio,
189:            mars_theta=mars_theta,
193:        from sgl_kernel_npu.sample.verify_tree_greedy import verify_tree_greedy
195:        verify_tree_greedy(
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "limit": 120,
  "offset": 150
}
```

> TOOL

tool_result Read
```
150	        pass
151	    return None
152	
153	
154	class EAGLEWorker(TpModelWorker):
155	
156	    def __init__(
157	        self,
158	        server_args: ServerArgs,
159	        gpu_id: int,
160	        tp_rank: int,
161	        dp_rank: Optional[int],
162	        moe_ep_rank: int,
163	        nccl_port: int,
164	        target_worker: TpModelWorker,
165	    ):
166	        # Parse arguments
167	        self.server_args = server_args
168	        self.topk = server_args.speculative_eagle_topk
169	        self.speculative_num_steps = server_args.speculative_num_steps
170	        self.speculative_num_draft_tokens = server_args.speculative_num_draft_tokens
171	        self.enable_nan_detection = server_args.enable_nan_detection
172	        self.gpu_id = gpu_id
173	        self.device = server_args.device
174	        self.target_worker = target_worker
175	        self.page_size = server_args.page_size
176	        self.speculative_algorithm = SpeculativeAlgorithm.from_string(
177	            server_args.speculative_algorithm
178	        )
179	
180	        # Override the context length of the draft model to be the same as the target model.
181	        server_args.context_length = target_worker.model_runner.model_config.context_len
182	
183	        # Do not capture cuda graph in `super().__init__()`
184	        # It will be captured later.
185	        backup_disable_cuda_graph = server_args.disable_cuda_graph
186	        server_args.disable_cuda_graph = True
187	        # EAGLE_DRAFT_KV_BF16=1 keeps draft KV pool in BF16 even when target uses
188	        # fp8_e4m3 KV cache. Target's pool/backend are already initialized with
189	        # the original server_args.kv_cache_dtype before this point; we only
190	        # tweak the value seen by the draft ModelRunner inside super().__init__().
191	        backup_kv_cache_dtype = server_args.kv_cache_dtype
192	        force_draft_bf16_kv = (
193	            os.environ.get("EAGLE_DRAFT_KV_BF16", "0") == "1"
194	            and backup_kv_cache_dtype not in (None, "auto", "bf16", "bfloat16")
195	        )
196	        if force_draft_bf16_kv:
197	            server_args.kv_cache_dtype = "bfloat16"
198	            logger.info(
199	                "EAGLE_DRAFT_KV_BF16=1: draft KV cache forced to bfloat16 "
200	                "(target stays %s)",
201	                backup_kv_cache_dtype,
202	            )
203	        # Determine draft model quantization.
204	        # If the draft model's config.json has quantization_config.quant_type="nvfp4",
205	        # it was trained with FP4_QAT and packed in NVFP4 format — keep modelopt_fp4.
206	        # Otherwise use None (BF16 mode, legacy behaviour).
207	        backup_draft_quant = server_args.speculative_draft_model_quantization
208	        draft_model_path = server_args.speculative_draft_model_path
209	        draft_quant = _detect_draft_model_quantization(draft_model_path, backup_draft_quant)
210	        server_args.speculative_draft_model_quantization = draft_quant
211	        # Draft model (Llama architecture) should use standard flashinfer, not minicpm_flashinfer
212	        backup_draft_attn = server_args.speculative_draft_attention_backend
213	        if (
214	            server_args.attention_backend == "minicpm_flashinfer"
215	            and backup_draft_attn in (None, "minicpm_flashinfer")
216	        ):
217	            server_args.speculative_draft_attention_backend = "flashinfer"
218	        # Share the allocator with a target worker.
219	        # Draft and target worker own their own KV cache pools.
220	        self.req_to_token_pool, self.token_to_kv_pool_allocator = (
221	            target_worker.get_memory_pool()
222	        )
223	
224	        # Load hot token ids
225	        if self.speculative_algorithm.is_eagle3():
226	            if server_args.speculative_token_map is not None:
227	                logger.warning(
228	                    "Speculative token map specified, but EAGLE3 models already have this. Ignoring the specified token map."
229	                )
230	            self.hot_token_id = None
231	        elif server_args.speculative_token_map is not None:
232	            self.hot_token_id = load_token_map(server_args.speculative_token_map)
233	            server_args.json_model_override_args = (
234	                f'{{"hot_vocab_size": {len(self.hot_token_id)}}}'
235	            )
236	        else:
237	            self.hot_token_id = None
238	
239	        # Init draft worker
240	        if server_args.enable_dp_attention and self.speculative_algorithm.is_eagle3():
241	            ctx = draft_tp_context(get_attention_tp_group())
242	        else:
243	            ctx = empty_context()
244	        with (
245	            ctx
246	        ), speculative_moe_backend_context(), speculative_moe_a2a_backend_context():
247	            super().__init__(
248	                server_args=server_args,
249	                gpu_id=gpu_id,
250	                tp_rank=tp_rank,
251	                pp_rank=0,  # FIXME
252	                dp_rank=dp_rank,
253	                moe_ep_rank=moe_ep_rank,
254	                nccl_port=nccl_port,
255	                is_draft_worker=True,
256	                req_to_token_pool=self.req_to_token_pool,
257	                token_to_kv_pool_allocator=self.token_to_kv_pool_allocator,
258	            )
259	
260	        if force_draft_bf16_kv:
261	            server_args.kv_cache_dtype = backup_kv_cache_dtype
262	
263	        embed, head = self.target_worker.model_runner.model.get_embed_and_head()
264	
265	        if self.speculative_algorithm.is_eagle3():
266	            # most cases EAGLE3 models don't share lm_head
267	            # but some models (e.g. nvidia/gpt-oss-120b-Eagle3) shares
268	            if (
269	                hasattr(self.draft_model_runner.model, "load_lm_head_from_target")
```

> TOOL

tool_use Bash
```json
{
  "command": "git log --oneline --all | grep -i \"marlin\\|fp4.*scale\\|scale.*bug\\|sgl-kernel\\|common_ops\\|sgl-kernel\" | head -20",
  "description": "Search for Marlin/sgl-kernel fix commits"
}
```

> TOOL

tool_result Bash
```
081559b docs: marlin-tuning + collapse + training-v3 + nvfp4-kv + infllmv2 fix + upstream survey
5b1c851 chore(bench): reorganize into kernels/{minicpm,marlin,fp4,prefill,...}; add microbenches
51ca6a8 fix(demo-sala): drop stale MARLIN_DECODE_THRESHOLD, add CUTE_DSL_CACHE_DIR
f7faed5 fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards
2b36ae2 fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards
6cd79ae feat: hybrid Marlin/CUTLASS dispatch + 45K quant + submission cleanup
f2e843d feat: hybrid Marlin/CUTLASS dispatch + 45K quant + submission cleanup
99e195e feat: NVFP4 Marlin fallback path + sgl-kernel rebuild pipeline + probe-sala
ae7c1d6 feat: NVFP4 Marlin fallback path + sgl-kernel rebuild pipeline + probe-sala
64f262d feat: W4A16 Marlin decode path — NVFP4→GPTQ conversion, dtype fix, bench tooling
372b695 feat: W4A16 Marlin decode path — NVFP4→GPTQ conversion, dtype fix, bench tooling
```

> TOOL

tool_use Bash
```json
{
  "command": "wc -l /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py",
  "description": "Count lines in key files"
}
```

> TOOL

tool_result Bash
```
1610 /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py
  1142 /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py
  2164 /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py
  4916 total
```

> TOOL

tool_use Bash
```json
{
  "command": "git log --oneline --all | grep -i \"b12x\\|2-tier\\|dispatch\\|marlin.*threshold\" | head -20",
  "description": "Search for b12x dispatch commits"
}
```

> TOOL

tool_result Bash
```
4c0005c docs: multi-doc audit — correct b12x/MARS/rope_theta status and cross-link
e9bfcb0 feat(probe-sala): sync sglang to latest + b12x readiness check
51ca6a8 fix(demo-sala): drop stale MARLIN_DECODE_THRESHOLD, add CUTE_DSL_CACHE_DIR
d19e4f2 perf: strip dispatch trace + hot-path cleanup
b3f9687 feat(b12x): 2-tier dispatch full-M + eagle_fc shape + dispatch trace
4f8fc05 bench: cu13/sm120 kernel microbenches + b12x CuTe-DSL backend exploration
6cd79ae feat: hybrid Marlin/CUTLASS dispatch + 45K quant + submission cleanup
f2e843d feat: hybrid Marlin/CUTLASS dispatch + 45K quant + submission cleanup
```

> AGENT

好的，我现在来查看更具体的 `git commits` 以及其他关键文件。

> TOOL

tool_use Bash
```json
{
  "command": "git log --format=\"%h %s\" --grep=\"perf\\|prefill\\|runtime\\|infllmv2\\|plan_info\\|plan cache\\|RoPE\\|residual\\|scale_emb\\|b12x\\|dispatch\\|marlin\\|operator\\|kernel\\|decode\\|GPTQ\\|NVFP4\\|quant\\|simple_gla\\|compress_k\\|Medusa\\|EAGLE-3\" 139652c..HEAD --reverse | head -40",
  "description": "Ordered performance commit history"
}
```

> TOOL

tool_result Bash
```
b478fcf feat: add EAGLE-3 speculative decoding for MiniCPM-SALA
47a054c feat: Medusa speculative decoding – data collection, training pipeline, profiling
c6b7991 feat: Medusa speculative decoding integration (S1 -12%, S8 -12.5%)
150119c fix: Medusa spec decode CUDA graph buffer overflow + vectorized verify
ed3ec68 clean: restore demo-sala from tarball + MedusaBlock auto-detect
6484c43 clean: reset demo-sala to 5f2a290 + MedusaBlock auto-detect
f42aca0 fix: deterministic decode/verify via num_splits=1 + eager TARGET_VERIFY fallback
6087c93 revert: undo fc3a920 operator optimizations for precision A/B test
ab4a619 fix: EAGLE-3 MiniCPM-SALA compatibility
f359853 probe-sala: fix empty responses via FlashInfer/cuDNN upgrade + full self-eval config
af38f7c docs: comprehensive cleanup — update CLAUDE.md, consolidate docs, add AGENTS.md
38ce7ea eagle: add Phase 0 baselines, Phase 2 kernel benchmarks, and plan
1f702ee eagle: implement STE-QAT FP4 native training + NVFP4 export pipeline
373dc6d plan: update Phase 2 checklist — STE-QAT + NVFP4 export implemented
3ffeed9 chore: cleanup dead files, one-off scripts, update .gitignore
0843656 feat: EAGLE-3 speculative decoding with fused GLA kernel
462414b docs: update CLAUDE.md and PLAN.md for EAGLE-3 fused GLA
2b36ae2 fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards
9225f46 feat: intermediate_ssm direct-write + fused sparse metadata + profiling framework
475ddd5 eval_ood: step-0 only, full-length (no SEQ_LEN truncation)
9c6996a docs: EAGLE-3 数据采集 v2 设计 spec
1f265fe perf(prefill): reuse flashinfer plan across 8 standard layers
b4d387a perf(prefill): cross-chunk plan_info reuse + smax64 bench
bf55703 docs: restructure — rename, merge, split, update
230b381 docs: rewrite CLAUDE.md + trim AGENTS.md + align start_eagle.sh
9a7e04c feat(probe-sala): full cu12→cu13 upgrade pipeline + BOS wheels offline install
4f8fc05 bench: cu13/sm120 kernel microbenches + b12x CuTe-DSL backend exploration
d7e5b52 probe-sala: torchao+xgrammar wheels + exit 1 also on all-pass path
cd480ca docs(runtime): §7/§8/§9 memcpy attribution + §10 profiling methodology
c3effe9 docs(runtime): §10.B 深挖 — 17.7% idle 拆分，CPU 侧真实 ROI 硬顶从 9.6% 下修到 5.5%
b3f9687 feat(b12x): 2-tier dispatch full-M + eagle_fc shape + dispatch trace
d19e4f2 perf: strip dispatch trace + hot-path cleanup
51ca6a8 fix(demo-sala): drop stale MARLIN_DECODE_THRESHOLD, add CUTE_DSL_CACHE_DIR
e9bfcb0 feat(probe-sala): sync sglang to latest + b12x readiness check
5552a23 perf: tune no-spec decode kernels
1608d18 fix(sgl-srt): spec-v1 correctness + profile gating + NVFP4 lm_head pipeline
da18187 feat(eagle): v3 training rewrite + pipeline reorganization
5b1c851 chore(bench): reorganize into kernels/{minicpm,marlin,fp4,prefill,...}; add microbenches
081559b docs: marlin-tuning + collapse + training-v3 + nvfp4-kv + infllmv2 fix + upstream survey
0e768a3 chore(env+eval+meta): start_eagle defaults, prepare_env tweaks, CLAUDE/AGENTS align
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle3_runtime_investigation.md",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 Runtime Investigation
2	
3	This document is based on code only. I did not use `docs/*` as a source of truth.
4	
5	Scope:
6	- `eval/start_eagle.sh`
7	- `demo-sala/sglang/python/sglang/srt/speculative/*`
8	- `demo-sala/sglang/python/sglang/srt/layers/attention/*`
9	- `demo-sala/sglang/python/sglang/srt/model_executor/*`
10	- `demo-sala/sglang/python/sglang/srt/managers/*`
11	
12	## Current path in code
13	
14	The active EAGLE-3 server entrypoint is `eval/start_eagle.sh`. The current default shape is:
15	- `spec_steps=1`
16	- `topk=2`
17	- `dtn=3`
18	- `attention-backend=minicpm_flashinfer`
19	- `speculative-draft-attention-backend=triton`
20	- `max-running-requests=64`
21	
22	Source:
23	- `eval/start_eagle.sh:10-37`
24	
25	The decode loop on the current v1 path is:
26	1. `ScheduleBatch.prepare_for_decode()` early-returns for speculative decode.
27	2. `EAGLEWorker.forward_batch_generation()` runs `draft()`.
28	3. `EAGLEWorker.verify()` runs target `TARGET_VERIFY`.
29	4. `EAGLEWorker.forward_draft_extend_after_decode()` fills the draft KV cache for the next round.
30	
31	Source:
32	- `demo-sala/sglang/python/sglang/srt/managers/schedule_batch.py:1938-1951`
33	- `demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:364-391`
34	- `demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:595-670`
35	- `demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:754-853`
36	- `demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:1027-1109`
37	
38	For EAGLE/EAGLE3, target CUDA graph capture is not normal decode. `CudaGraphRunner` captures `ForwardMode.TARGET_VERIFY` with `num_tokens_per_bs = speculative_num_draft_tokens`.
39	
40	Source:
41	- `demo-sala/sglang/python/sglang/srt/model_executor/cuda_graph_runner.py:250-286`
42	
43	## Two corrections from code that change the framing
44	
45	### 1. The current MiniCPM TARGET_VERIFY path is not using the generic tree-mask interface
46	
47	Generic FlashInfer-style backends call `spec_info.generate_attn_arg_prefill(...)`, which builds `kv_indices`, `qo_indptr`, and `custom_mask`.
48	
49	Source:
50	- `demo-sala/sglang/python/sglang/srt/layers/attention/flashinfer_backend.py:1339-1436`
51	- `demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py:158-211`
52	
53	The current `minicpm_flashinfer` TARGET_VERIFY path does not call that interface. Instead it:
54	- creates a `BatchPrefillWithPagedKVCacheWrapper`
55	- updates `verify_kv_indptr` / `verify_kv_indices`
56	- calls `verify_wrapper.forward(...)`
57	- passes no `custom_mask`
58	
59	Source:
60	- `demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_backend.py:1766-1830`
61	- `demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_backend.py:973-1014`
62	- `demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_backend.py:2037-2105`
63	
64	So the current tree-awareness problem is broader than "GLA only". On the current backend, standard attention in `minicpm_backend.py` also does not consume the generic `custom_mask` path.
65	
66	### 2. The spec-v2 "fill verify buffers after draft" hook is not actually wired through the current backend chain
67	
68	`eagle_worker_v2.py` is written to use:
69	- `attn_backend.get_verify_buffers_to_fill_after_draft()`
70	- `attn_backend.update_verify_buffers_to_fill_after_draft(...)`
71	
72	Source:
73	- `demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py:311-334`
74	- `demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py:681-695`
75	
76	But the base attention backend default is a no-op:
77	- returns `[None, None]`
78	- requires subclasses to override update behavior
79	
80	Source:
81	- `demo-sala/sglang/python/sglang/srt/layers/attention/base_attn_backend.py:57-75`
82	
83	The current `HybridAttnBackend` does not forward these methods to child backends.
84	
85	Source:
86	- `demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_attn_backend.py:1-137`
87	
88	The current `minicpm_backend.py` also does not override them.
89	
90	This means spec-v2 already has the API shape, but on the current target backend path those hooks are effectively inert.
91	
92	## Investigation of the 6 directions
93	
94	## 1. TARGET_VERIFY replay de-`plan()` and remove CPU-side `kv_indices` packing
95	
96	### What the code does today
97	
98	During CUDA-graph capture, MiniCPM allocates:
99	- `verify_qo_indptr`
100	- `verify_kv_indptr`
```

> AGENT

我现在来阅读 `eagle_worker.py` 的 `_apply_spec_config` 和 `_forward_no_spec` 部分，以及动态模式的调度器集成。

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "limit": 120,
  "offset": 530
}
```

> TOOL

tool_result Read
```
530	            )
531	            with self.draft_tp_context(
532	                self.draft_model_runner.tp_group
533	            ), speculative_moe_backend_context(), speculative_moe_a2a_backend_context():
534	                self.forward_draft_extend(
535	                    batch, logits_output.hidden_states, next_token_ids, seq_lens_cpu
536	                )
537	            self._prev_spec_mode = None
538	            return GenerationBatchResult(
539	                logits_output=logits_output,
540	                next_token_ids=next_token_ids,
541	                num_accepted_tokens=0,
542	                can_run_cuda_graph=False,
543	            )
544	        else:
545	            mode = getattr(batch, "_spec_mode", None)
546	
547	            if mode == SpecMode.NO_SPEC:
548	                self._prev_spec_mode = mode
549	                return self._forward_no_spec(batch)
550	
551	            # Spec mode (D5/D7 or legacy fixed config). Apply per-mode params
552	            # before the draft/verify path consumes self.* / server_args.*.
553	            if mode is not None:
554	                self._apply_spec_config(mode)
555	            self._prev_spec_mode = mode
556	
557	            with self.draft_tp_context(
558	                self.draft_model_runner.tp_group
559	            ), speculative_moe_backend_context(), speculative_moe_a2a_backend_context():
560	                spec_info = self.draft(batch)
561	            logits_output, verify_output, model_worker_batch, can_run_cuda_graph = (
562	                self.verify(batch, spec_info)
563	            )
564	
565	            with self.draft_tp_context(
566	                self.draft_model_runner.tp_group
567	            ), speculative_moe_backend_context(), speculative_moe_a2a_backend_context():
568	                # NOTE: We should use `check_forward_draft_extend_after_decode`
569	                # when DP attention is enabled, but it is slow. Skip it for now.
570	                if (
571	                    self.server_args.enable_dp_attention
572	                    or batch.spec_info.verified_id.shape[0] > 0
573	                ):
574	                    # decode is not finished
575	                    self.forward_draft_extend_after_decode(batch)
576	
577	            # Tell metrics layer the actual per-req draft capacity for this
578	            # step. self.speculative_num_draft_tokens has already been swapped
579	            # by _apply_spec_config to D5/D7's dtn (or unchanged for static
580	            # spec). Subtracting 1 strips the user_4813494d token to get pure draft.
581	            return GenerationBatchResult(
582	                logits_output=logits_output,
583	                next_token_ids=verify_output.verified_id,
584	                num_accepted_tokens=sum(verify_output.accept_length_per_req_cpu),
585	                accept_length_per_req_cpu=verify_output.accept_length_per_req_cpu,
586	                can_run_cuda_graph=can_run_cuda_graph,
587	                max_draft_per_req=max(self.speculative_num_draft_tokens - 1, 0),
588	            )
589	
590	    def _apply_spec_config(self, mode: SpecMode) -> None:
591	        """Switch worker spec config (topk / steps / dtn) and active draft graph.
592	
593	        No-op if dynamic mode disabled or mode is the same as last applied. The
594	        draft attn_backend is shared across modes (sized to ``_max_spec_steps``
595	        at init); only the cuda-graph runner buffers differ.
596	        """
597	        cfg = self.spec_mode_config
598	        if not cfg.enabled:
599	            return
600	        if mode == SpecMode.MARS_D5:
601	            new_topk, new_steps, new_dtn = cfg.d5_topk, cfg.d5_steps, cfg.d5_dtn
602	            new_runner = self.cuda_graph_runner_d5
603	            new_theta = cfg.effective_d5_theta()
604	        elif mode == SpecMode.MARS_D7:
605	            new_topk, new_steps, new_dtn = cfg.d7_topk, cfg.d7_steps, cfg.d7_dtn
606	            new_runner = self.cuda_graph_runner_d7
607	            new_theta = cfg.effective_d7_theta()
608	        else:
609	            return  # NO_SPEC handled separately
610	
611	        # Steady-state fast path: D5 -> D5 / D7 -> D7 are the vast majority of
612	        # decode steps once the bs settles. _applied_spec_mode is None on the
613	        # very first call (forces full re-bind so cuda_graph_runner is correct
614	        # even if self.* defaults already match the requested mode).
615	        if self._applied_spec_mode == mode:
616	            return
617	
618	        self.topk = new_topk
619	        self.speculative_num_steps = new_steps
620	        self.speculative_num_draft_tokens = new_dtn
621	        self.server_args.speculative_eagle_topk = new_topk
622	        self.server_args.speculative_num_steps = new_steps
623	        self.server_args.speculative_num_draft_tokens = new_dtn
624	        self.cuda_graph_runner = new_runner
625	
626	        # Per-mode MARS theta. eagle_info reads from EagleVerifyInput.mars_theta
627	        # (plumbed via draft() at construction time) so we just stash the value
628	        # on self here. D7 (typically bs=1, S1) can run a more aggressive theta
629	        # than D5 without affecting D5 quality. -1 disables MARS for that mode.
630	        self._active_mars_theta = float(new_theta)
631	        self._applied_spec_mode = mode
632	
633	    def _forward_no_spec(self, batch: ScheduleBatch) -> GenerationBatchResult:
634	        """Run target_worker direct decode and refresh draft KV with one token.
635	
636	        Skips draft/verify entirely. Then runs a single 1-token DRAFT_EXTEND so
637	        the draft KV / GLA state advance lock-step with target — this lets us
638	        switch back to MARS_D5/D7 on the next step without any cold-start gap.
639	        """
640	        # Scheduler's prepare_for_decode() early-returned because spec is
641	        # enabled — that meant EAGLE.draft() was expected to allocate the KV
642	        # slots. We're skipping draft, so run the full non-spec body now to
643	        # allocate (bs,) dense KV slots, advance seq_lens, set input_ids.
644	        # Clear any stale spec_info.positions BEFORE building model_worker_batch:
645	        # the previous step's prepare_extend_after_decode left positions sized
646	        # to the prior bs. ForwardBatch.init_new copies spec_info.positions
647	        # verbatim when set, so a stale length crashes target's input_buffers
648	        # at copy time.
649	        if isinstance(batch.spec_info, EagleDraftInput):
```

> TOOL

tool_use Bash
```json
{
  "command": "git log -1 --format=\"%B\" b3f9687",
  "description": "Read b12x 2-tier dispatch commit message"
}
```

> TOOL

tool_result Bash
```
feat(b12x): 2-tier dispatch full-M + eagle_fc shape + dispatch trace

- Expand b12x from B12X_UPPER=256 to full M range with 3 CUTLASS
  override points (down M=512, gate_up M=8192, std_qkv M=8192)
- Add eagle_fc (4096×12288) shape: MARLIN_UPPER=16, 10 tile configs;
  b12x 3-6× faster than CUTLASS at small M, draft model fc layer
  now routes through b12x instead of legacy CUTLASS
- 58 BEST_TILE entries across 6 shapes (5 target + 1 eagle_fc)
- Precompile all kernels at startup (ensure_precompiled in
  process_weights_after_loading), eliminates JIT during requests
- Prepare Marlin weights when b12x enabled (not just when
  SGLANG_MARLIN_DECODE_THRESHOLD>0), fixes AttributeError on
  weight_marlin
- Remove SGLANG_MARLIN_DECODE_THRESHOLD from start_eagle.sh
  (b12x has per-shape thresholds built-in)
- Add dispatch trace instrumentation: per-(tag, N, K, M) counters,
  periodic log + auto-dump to /tmp/dispatch_trace.json
- Bench data: 62% b12x, 18% override_cutlass, 19% cutlass prefill,
  0.7% b12x_marlin, 0.07% legacy_marlin (draft only)

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/nvfp4-kv-investigation.md",
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	# NVFP4 KV Cache 调研（负结果合集）
2	
3	2026-04-21 的深度调研记录。**结论：NVFP4 KV 在 SALA 当前架构（InfLLM-v2 sparse + page_size=1）上没有可用落地路径；VariableBlockSparseAttentionWrapper 也不带来加速**。保留本文以防重踩。
4	
5	## 1. 出发点（被证伪的旧判断）
6	
7	生产 `--kv-cache-dtype fp8_e5m2` 已经在高并发证明稳定收益。自然想法：NVFP4 KV 理论再省 2× 带宽，是否能进一步提速。
8	
9	[`docs/quantization.md`](quantization.md) 老版本的阻塞理由是 "SGLang MHA 路径 `trtllm_batch_decode_with_kv_cache` 未传 `kv_block_scales`"。**这个结论在 FlashInfer 0.6.8 / cu13 已过时** —— API 早已支持（`flashinfer/decode.py:2260` 的 `kv_cache_sf=(k_sf, v_sf)` 参数）。真正的阻塞点不在 API，而在下文描述的**算法不兼容**。
10	
11	## 2. FlashInfer NVFP4 KV API 的真实约束
12	
13	核对 FlashInfer 0.6.8.post1 源码：
14	
15	| 路径 | backend | sm_120 支持 | page_size 限制 | 通用 sparse | 备注 |
16	|---|---|---|---|---|---|
17	| `trtllm_batch_decode_with_kv_cache` 自动派发到 `xqa` | xqa | ✅ | ∈ {16,32,64,128} | ❌ dense paged | decode.py:2431 |
18	| `trtllm_batch_decode_with_kv_cache` 自动派发到 `trtllm-gen` | trtllm-gen | ❌（仅 sm_100/103） | — | — | TRT-LLM issue #10241 确认 blocked |
19	| `flashinfer.xqa.xqa` 直调 | xqa | ✅（**NVFP4 KV only supported on SM120**，见 xqa.py:309） | ∈ {16,32,64,128} | ❌ | `k_sf_cache/v_sf_cache` 参数存在且可用 |
20	| `BatchDecodeWithPagedKVCacheWrapper` | FA2/FA3 | ✅ | page=1 OK | token-level indices | **不支持 NVFP4 KV** |
21	| `VariableBlockSparseAttentionWrapper`（v0.2+） | FA2/FA3 | ✅（FA3 可能打折） | page=1 OK | block-sparse 原生 | **不支持 NVFP4 KV**（KV dtype 只到 FP8） |
22	
23	**结论**：支持 NVFP4 KV 的 kernel（xqa, trtllm-gen）都要求 page_size ≥ 16；支持 page_size=1 / sparse 的 kernel 都不吃 NVFP4。
24	
25	### NVFP4 存储格式的真正事实
26	
27	NVFP4 (E2M1) 4-bit 值 + **E4M3FN per-16-element block scale**（不是 MXFP4 的 E8M0）。scale 的 block=16 是沿 **head_dim 方向**，**不是沿 token 方向**。所以 NVFP4 存储本身和 page_size=1 完全兼容；page_size≥16 是 xqa kernel 的 **TMA tile 约束**，不是格式约束。
28	
29	SGLang 上游 PR #10078 的 `KVFP4QuantizeUtil` 用的是 E8M0（MXFP4），**格式不对**，喂给 FlashInfer xqa 会导致精度严重退化。不能复用那条量化路径，要用 `flashinfer.nvfp4_quantize(sfLayout=layout_linear)`。
30	
31	## 3. SALA 架构与 page_size=1 的硬依赖
32	
33	`--dense-as-sparse` 启动，SALA 32 层中 8 层 standard attention **永远走 InfLLM-v2 sparse**，24 层 GLA 无 KV cache。sparse path 的 page_size=1 依赖不是历史遗留，是算法决定的：
34	
35	### 3.1 硬编码点（`demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_backend.py`）
36	
37	```python
38	# L1410 (sparse extend path)
39	assert self.page_size == 1
40	key_cache_by_head_group = key_cache.reshape(
41	    -1, self.page_size, layer.tp_k_head_num // 2, layer.head_dim
42	)
43	
44	# L1130 (sparse decode path)
45	sparse_page_table = sparse_kernel_extension.get_block_table_v2(
46	    topk_idx, page_table, ..., self.sparse_topk
47	).reshape(-1, self.num_sparse_topk_tokens)   # 96*64=6144 token slots
48	```
49	
50	### 3.2 InfLLM-v2 是 block-sparse，block_size=64
51	
52	`config.json` 的 `sparse_config`：
53	```
54	block_size = 64       # 每 sparse block 64 连续 tokens
55	topk       = 64       # 每 query 选 top-64 blocks
56	kernel_size = 32, kernel_stride = 16   # compress_k 滑窗
57	window_size = 2048, dense_len = 8192
58	```
59	
60	理论上 `block_size=64 / page_size=16 = 4`，把 page_size 升到 16 + sparse_page_table 改 page 粒度就能对齐 xqa 的 page_size 约束。但实测推进时撞到**深层 page_size=1 依赖**：
61	
62	### 3.3 page_size=16 尝试触发的 latent bugs
63	
64	推进 `--page-size 16 --kv-cache-dtype fp8_e5m2` 时依次踩坑：
65	
66	1. **server_args guard**：`speculative_eagle_topk>1 && page_size>1` 被拒，白名单不含 `minicpm_flashinfer`
67	   - 修复：`server_args.py:2180` 白名单加 `minicpm_flashinfer`（latent bug，值得保留）
68	2. **HybridLinearKVPool 透传 bug**：`enable_kv_cache_copy` 参数没传给内部 `MHATokenToKVPool`，`move_kv_cache` assert 崩
69	   - 触发条件：`eagle_info.py:520-599` 仅 `page_size>1 && topk>1` 分支走 `move_kv_cache`
70	   - 修复：`memory_pool.py:1231` 加参数；`model_runner_kv_cache_mixin.py:562` 显式传 `(speculative_algorithm is not None)`（latent bug，已保留）
71	3. **compress_k 单 token 分配崩**：InfLLM-v2 的 compress_k1/compress_k2 池每 `kernel_stride=16` 步调 `alloc_token_slots(..., 1)`，`PagedTokenToKVPoolAllocator.alloc(need_size=1)` 在 page_size=16 下返回空 tensor
72	   - 位置：`eagle_worker.py:1033` + `mem_cache/allocator.py:315`
73	   - 深度：**架构级不兼容**。compress_k pool 和 full KV pool 共享 allocator/page_size；真要修需要 compress_k 独立 allocator，是中等规模重构
74	
75	这 3 处暴露的只是前几层。推进下去还会撞更多（如 `minicpm_backend.py:1410` 的 assert 本身、InfLLM-v2 kernel 的 token-level 假设等）。
76	
77	## 4. 全球现成 NVFP4 KV kernel 盘点（30+ 项目）
78	
79	需求：NVFP4 KV + page_size=1（或 token-level sparse block_table） + sm_120。
80
```

> TOOL

tool_use Bash
```json
{
  "command": "git log -1 --format=\"%B\" 6cd79ae",
  "description": "Read hybrid Marlin/CUTLASS dispatch commit"
}
```

> TOOL

tool_result Bash
```
feat: hybrid Marlin/CUTLASS dispatch + 45K quant + submission cleanup

- Implement hybrid decode: M<=threshold→Marlin W4A16, M>threshold→CUTLASS W4A4
- Add SGLANG_MARLIN_DECODE_THRESHOLD env var (replaces SGLANG_FORCE_NVFP4_MARLIN)
- Reduce quant context 48K→45K, set both PYTORCH_ALLOC_CONF variants for OOM fix
- Remove sgl-kernel-deps from submission (989MB→44MB tarball)
- Add offline hybrid consistency test + Marlin vs CUTLASS benchmark
- Clean up prepare_env/model scripts, update CLAUDE.md

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"_spec_mode\\|spec_mode_selector\\|NO_SPEC\\|SpecMode\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/managers/scheduler.py | head -20",
  "description": "Find dynamic mode integration in scheduler"
}
```

> TOOL

tool_result Bash
```
169:from sglang.srt.speculative.spec_mode import SpecMode, selector_from_env
816:        self._spec_mode_selector = selector_from_env()
2275:            batch._spec_mode = self._spec_mode_selector.select(batch.batch_size())
2277:            batch._spec_mode = None
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py",
  "limit": 200,
  "offset": 350
}
```

> TOOL

tool_result Read
```
350	        output_partition_sizes: List[int],
351	        params_dtype: torch.dtype,
352	        **extra_weight_attrs,
353	    ) -> None:
354	        """Creates and registers weights, weight scales, and input scales for FP8 quantization."""
355	        output_size_per_partition = sum(output_partition_sizes)
356	        weight_loader = extra_weight_attrs.get("weight_loader")
357	        weight_dtype = (
358	            torch.float8_e4m3fn
359	            if self.quant_config.is_checkpoint_fp8_serialized
360	            else params_dtype
361	        )
362	
363	        # Set layer attributes
364	        layer.logical_widths = output_partition_sizes
365	        layer.input_size_per_partition = input_size_per_partition
366	        layer.output_size_per_partition = output_size_per_partition
367	
368	        # Register weight
369	        layer.register_parameter(
370	            "weight",
371	            ModelWeightParameter(
372	                data=torch.empty(
373	                    output_size_per_partition,
374	                    input_size_per_partition,
375	                    dtype=weight_dtype,
376	                ),
377	                input_dim=1,
378	                output_dim=0,
379	                weight_loader=weight_loader,
380	            ),
381	        )
382	
383	        if self.quant_config.is_checkpoint_fp8_serialized:
384	            # Register weight and input scales
385	            for scale_name in ["weight_scale", "input_scale"]:
386	                layer.register_parameter(
387	                    scale_name,
388	                    PerTensorScaleParameter(
389	                        data=torch.full(
390	                            (len(output_partition_sizes),),
391	                            torch.finfo(torch.float32).min,
392	                            dtype=torch.float32,
393	                        ),
394	                        weight_loader=weight_loader,
395	                    ),
396	                )
397	
398	    def process_weights_after_loading(self, layer: torch.nn.Module) -> None:
399	        """Requantizes weights after loading using the maximum scale."""
400	        max_w_scale, quantized_weight = requantize_with_max_scale(
401	            layer.weight, layer.weight_scale, layer.logical_widths
402	        )
403	        layer.weight = Parameter(quantized_weight.t(), requires_grad=False)
404	        # cutlass sgl-kernel only supports per-channel scale
405	        if self.cutlass_fp8_supported:
406	            max_w_scale = convert_to_channelwise(max_w_scale, layer.logical_widths)
407	        layer.weight_scale = Parameter(max_w_scale, requires_grad=False)
408	        layer.input_scale = Parameter(layer.input_scale.max(), requires_grad=False)
409	
410	    def apply(
411	        self,
412	        layer: torch.nn.Module,
413	        x: torch.Tensor,
414	        bias: Optional[torch.Tensor] = None,
415	    ) -> torch.Tensor:
416	        """Applies FP8 linear transformation."""
417	        return apply_fp8_linear(
418	            input=x,
419	            weight=layer.weight,
420	            weight_scale=layer.weight_scale,
421	            input_scale=layer.input_scale,
422	            bias=bias,
423	            cutlass_fp8_supported=self.cutlass_fp8_supported,
424	        )
425	
426	
427	class ModelOptFp8KVCacheMethod(BaseKVCacheMethod):
428	    """
429	    Handles loading FP8 kv-cache scaling factors from modelopt quantized checkpoints.
430	    """
431	
432	    def __init__(self, quant_config: ModelOptFp8Config):
433	        super().__init__(quant_config)
434	
435	
436	class ModelOptFp8MoEMethod(FusedMoEMethodBase):
437	    """MoE method for ModelOpt FP8.
438	    Supports loading FP8 checkpoints with static weight scale and activation scale.
439	
440	    Args:
441	        quant_config: The ModelOpt quantization config.
442	    """
443	
444	    def __init__(self, quant_config: ModelOptFp8Config):
445	        self.quant_config = quant_config
446	        self.cutlass_fp8_supported = cutlass_fp8_supported()
447	
448	    def create_weights(
449	        self,
450	        layer: torch.nn.Module,
451	        num_experts: int,
452	        hidden_size: int,
453	        intermediate_size_per_partition: int,
454	        params_dtype: torch.dtype,
455	        **extra_weight_attrs,
456	    ):
457	        from sglang.srt.layers.moe.fused_moe_triton import FusedMoeWeightScaleSupported
458	
459	        # Use FP8 dtype if checkpoint is serialized, otherwise use the default dtype
460	        weight_dtype = (
461	            torch.float8_e4m3fn
462	            if self.quant_config.is_checkpoint_fp8_serialized
463	            else params_dtype
464	        )
465	        weight_loader = extra_weight_attrs.get("weight_loader")
466	        num_shards = 2 if layer.moe_runner_config.is_gated else 1
467	        intermediate_size = num_shards * intermediate_size_per_partition
468	        w13_weight = ModelWeightParameter(
469	            data=torch.empty(
470	                num_experts,
471	                intermediate_size,
472	                hidden_size,
473	                dtype=weight_dtype,
474	            ),
475	            input_dim=2,
476	            output_dim=1,
477	            weight_loader=weight_loader,
478	        )
479	        layer.register_parameter("w13_weight", w13_weight)
480	
481	        w2_weight = ModelWeightParameter(
482	            data=torch.empty(
483	                num_experts,
484	                hidden_size,
485	                intermediate_size_per_partition,
486	                dtype=weight_dtype,
487	            ),
488	            input_dim=2,
489	            output_dim=1,
490	            weight_loader=weight_loader,
491	        )
492	        layer.register_parameter("w2_weight", w2_weight)
493	
494	        if self.quant_config.is_checkpoint_fp8_serialized:
495	            # WEIGHT SCALES - Per-tensor scaling for ModelOpts
496	            # Allocate 2 scales for w1 and w3 respectively.
497	            # They will be combined to a single scale after weight loading.
498	            w13_scale_shape = (num_experts, num_shards)
499	            w13_weight_scale = PerTensorScaleParameter(
500	                data=torch.full(
501	                    w13_scale_shape,
502	                    torch.finfo(torch.float32).min,
503	                    dtype=torch.float32,
504	                ),
505	                weight_loader=weight_loader,
506	            )
507	            w2_weight_scale = PerTensorScaleParameter(
508	                data=torch.full(
509	                    (num_experts,), torch.finfo(torch.float32).min, dtype=torch.float32
510	                ),
511	                weight_loader=weight_loader,
512	            )
513	            layer.register_parameter("w13_weight_scale", w13_weight_scale)
514	            layer.register_parameter("w2_weight_scale", w2_weight_scale)
515	
516	            # Set weight loader attributes for scales
517	            extra_weight_attrs.update(
518	                {"quant_method": FusedMoeWeightScaleSupported.TENSOR.value}
519	            )
520	
521	            # INPUT SCALES - Per-tensor scaling for ModelOpt
522	            w13_input_scale = PerTensorScaleParameter(
523	                data=torch.full((num_experts,), 1.0, dtype=torch.float32),
524	                weight_loader=weight_loader,
525	            )
526	            w2_input_scale = PerTensorScaleParameter(
527	                data=torch.full((num_experts,), 1.0, dtype=torch.float32),
528	                weight_loader=weight_loader,
529	            )
530	            layer.register_parameter("w13_input_scale", w13_input_scale)
531	            layer.register_parameter("w2_input_scale", w2_input_scale)
532	
533	    def process_weights_after_loading(self, layer: torch.nn.Module) -> None:
534	        """Process FP8 MoE weights after loading from serialized checkpoint.
535	
536	        Only supports pre-quantized checkpoints with FP8 weights and scales.
537	        """
538	
539	        layer.w13_weight = Parameter(layer.w13_weight.data, requires_grad=False)
540	        layer.w2_weight = Parameter(layer.w2_weight.data, requires_grad=False)
541	
542	        # Handle scale parameters
543	        if hasattr(layer, "w13_weight_scale") and layer.w13_weight_scale is not None:
544	            # Fp8 moe kernel needs single weight scale for w13 per expert.
545	            # We take the max of the w1 and w3 scales then dequant and requant each expert.
546	            if layer.w13_weight_scale.dim() == 2:  # Shape: (num_experts, 2)
547	                # Get the maximum scale across w1 and w3 for each expert
548	                max_w13_scales = layer.w13_weight_scale.max(dim=1).values
549
```

> AGENT

现在我来查看具体的性能优化提交，以获取更多数据。

> TOOL

tool_use Bash
```json
{
  "command": "git log --format=\"%h %ad %s\" --date=short 139652c..HEAD | grep -i \"perf\\|RoPE\\|residual\\|scale_emb\\|GPTQ\\|operator\\|b12x\\|dispatch\\|Medusa\\|plan\"",
  "description": "Key perf commits with dates"
}
```

> TOOL

tool_result Bash
```
87a8bb1 2026-04-28 perf(eagle/dynamic): four small accelerations on the spec-decode hot path
20cc58a 2026-04-28 perf(eagle/dynamic): kill three hot-path wastes in spec decode
4c0005c 2026-04-27 docs: multi-doc audit — correct b12x/MARS/rope_theta status and cross-link
5552a23 2026-04-25 perf: tune no-spec decode kernels
e9bfcb0 2026-04-23 feat(probe-sala): sync sglang to latest + b12x readiness check
d19e4f2 2026-04-23 perf: strip dispatch trace + hot-path cleanup
b3f9687 2026-04-23 feat(b12x): 2-tier dispatch full-M + eagle_fc shape + dispatch trace
4f8fc05 2026-04-21 bench: cu13/sm120 kernel microbenches + b12x CuTe-DSL backend exploration
91b0dd2 2026-04-21 chore: purge obsolete — PLAN.md, v1 draft, superpowers/, debug archives
b4d387a 2026-04-20 perf(prefill): cross-chunk plan_info reuse + smax64 bench
1f265fe 2026-04-20 perf(prefill): reuse flashinfer plan across 8 standard layers
89eb9a6 2026-04-17 feat(gla): Plan A scaffolding — per-branch tree verify buffers
462414b 2026-04-15 docs: update CLAUDE.md and PLAN.md for EAGLE-3 fused GLA
dd78dae 2026-04-14 chore: rename PLANtodo.md → PLAN.md
373dc6d 2026-04-14 plan: update Phase 2 checklist — STE-QAT + NVFP4 export implemented
38ce7ea 2026-04-14 eagle: add Phase 0 baselines, Phase 2 kernel benchmarks, and plan
6087c93 2026-04-08 revert: undo fc3a920 operator optimizations for precision A/B test
6484c43 2026-04-07 clean: reset demo-sala to 5f2a290 + MedusaBlock auto-detect
ed3ec68 2026-04-07 clean: restore demo-sala from tarball + MedusaBlock auto-detect
150119c 2026-04-04 fix: Medusa spec decode CUDA graph buffer overflow + vectorized verify
c6b7991 2026-04-04 feat: Medusa speculative decoding integration (S1 -12%, S8 -12.5%)
47a054c 2026-04-04 feat: Medusa speculative decoding – data collection, training pipeline, profiling
```

> AGENT

现在我来阅读 `modelopt_quant.py` 的 NVFP4 部分，其中包含 dispatch 逻辑。

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"class NvFp4\\|class ModelOptFp4\\|MARLIN_DECODE_THRESHOLD\\|b12x\\|_detect_draft\\|_prepare_hybrid_marlin\\|def apply\\|weight_scale_interleaved\\|dense_as_sparse\\|FourOverSix\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py | head -40",
  "description": "Find key NVFP4 dispatch code locations"
}
```

> TOOL

tool_result Bash
```
158:_MARLIN_HYBRID_THRESHOLD = int(_os.environ.get("SGLANG_MARLIN_DECODE_THRESHOLD", "0"))
410:    def apply(
709:    def apply(
864:class ModelOptFp4Config(ModelOptQuantConfig):
1073:class ModelOptFp4LinearMethod(LinearMethodBase):
1230:            layer.weight_scale_interleaved = Parameter(scale, requires_grad=False)
1256:        layer.weight_scale_interleaved = Parameter(padded_scales, requires_grad=False)
1261:            self._prepare_hybrid_marlin(layer)
1265:    def _prepare_hybrid_marlin(layer):
1313:    def apply(
1369:        w_scale_interleaved = layer.weight_scale_interleaved
1372:            w_scale_interleaved = layer.weight_scale_interleaved.T
1783:    def apply(
1884:    def apply_without_routing_weights(
```

> TOOL

tool_use Bash
```json
{
  "command": "git show 1f265fe --stat && echo \"===\" && git show b4d387a --stat && echo \"===\" && git show 139652c --stat",
  "description": "Show stat for key perf commits"
}
```

> TOOL

tool_result Bash
```
commit 1f265fe90bf1acf42ccfb6a921708440f2107010
Author: SOAR User <[REDACTED]>
Date:   Mon Apr 20 12:27:11 2026 +0000

    perf(prefill): reuse flashinfer plan across 8 standard layers
    
    128K prompt prefill 端到端 14.6s → 10.3s (-28%). 根因定位：flashinfer
    BatchDecodeWithPagedKVCacheWrapper.plan() 每次调用在 CPU 侧耗 ~23ms 做
    work-split 决策（nsys 确认与 GPU 状态无关，纯 CPU gap），16 chunk × 8
    std layer × 23ms ≈ 2.9s baseline + 偶发 350ms spike ~2.8s。
    
    同一 forward 内 8 个 standard layer 的 plan 输入（bs / indptr 值 /
    last_page_len / heads / dtypes）完全相同，只有 kv_indices 内容变化，因此
    layer_id > last 时可跳过 begin_forward，直接复用 wrapper 内部 _plan_info /
    _cached_module，只覆写 _paged_kv_indices_buf。下一次 forward 从 L0
    (0 > 31 == False) 自动触发 replan，跨 forward 无残留。
    
    只作用于 non-CUDA-graph + is_prefill=False 的 sparse decode wrapper 路径，
    decode CUDA graph 路径物理隔离；cache on/off decode TPS 噪声级一致。
    env SGLANG_MINICPM_PLAN_CACHE=0 可关。
    
    同时加入 NVTX range + cudaProfilerStart/Stop 窗口、sparse 阶段细分
    profile bucket、per-layer FA 时序打印，用于后续热点分析。文档见
    docs/PREFILL-HOTMAP.md。

 .../layers/attention/minicpm_attention_kernels.py  | 104 ++++++++--
 .../sglang/srt/layers/attention/minicpm_backend.py |  76 ++++++-
 .../srt/layers/attention/minicpm_sparse_utils.py   |  22 ++-
 .../sglang/python/sglang/srt/models/minicpm.py     | 106 +++++++++-
 docs/PREFILL-HOTMAP.md                             | 219 +++++++++++++++++++++
 5 files changed, 507 insertions(+), 20 deletions(-)
===
commit b4d387a6bfaf2e96f192d892b7b4d485ff5930d4
Author: SOAR User <[REDACTED]>
Date:   Mon Apr 20 12:56:07 2026 +0000

    perf(prefill): cross-chunk plan_info reuse + smax64 bench
    
    - layer-level plan cache 之外，在 L0 路径加 kv_indptr / kv_last_page_len 的 CPU byte-compare，
      当结构 chunk 间不变时跨 chunk 复用 plan（~14/16 chunk cross-hit）。
    - 新增 bench/prefill_bench_smax64.py：64 smax 样本纯 prefill（max_tokens=1）A/B 对照。
    - 实测 cache on vs off：416.29s → 290.23s（-30.3% e2e，p50 60s → 42s）。
    
    Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>

 bench/prefill_bench_smax64.py                      | 102 +++++++++++++++++++++
 .../layers/attention/minicpm_attention_kernels.py  |  37 +++++++-
 docs/PREFILL-HOTMAP.md                             |  32 ++++++-
 3 files changed, 166 insertions(+), 5 deletions(-)
===
commit 139652cdbd0526a599bfb78ca88511a64d4e3b16
Author: SOAR User <[REDACTED]>
Date:   Fri Apr 3 15:42:24 2026 +0000

    perf: GPTQ quantization + operator optimizations for inference throughput
    
    Quantization: replace AWQ-lite with GPTQ+NVFP4 via llmcompressor
    - Hessian-based optimal weight rounding, calibrated on 90 mcq/niah/qa samples (24K max_length)
    - Output converted to modelopt format for hybrid Marlin/CUTLASS serving
    - Accuracy: 80.27% (vs AWQ-lite 79.73%, +0.54%)
    - prepare_env.sh installs llmcompressor; preprocess_model.py fully rewritten
    
    Operator optimizations in minicpm.py:
    - Absorb scale_emb (×12) into embed_tokens.weight and scale_width (÷16) into
      lm_head.weight at load time, eliminating 2 elementwise kernels per forward
    - In-place output gate: o.mul_(z.sigmoid_()) replaces o * F.sigmoid(z) across
      32 layers, removing intermediate tensor allocations
    - Remove redundant no-op reshape in Lightning mixer
    
    GLA backend cleanup in hybrid_linear_attn_backend.py:
    - Remove redundant .contiguous() (advanced indexing returns contiguous)
    - Cache layer_cache lookup to avoid double dict.get + mamba2_layer_cache call
    - Hoist error check to deduplicate RuntimeError code
    
    Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

 CLAUDE.md                                          |  20 +-
 bench/mini_bench.sh                                |   4 +-
 demo-sala/prepare_env.sh                           |   4 +-
 demo-sala/prepare_model.sh                         |   6 +-
 demo-sala/preprocess_model.py                      | 533 ++++++++-------------
 .../layers/attention/hybrid_linear_attn_backend.py |  45 +-
 .../sglang/python/sglang/srt/models/minicpm.py     |  26 +-
 eval/start_public_eval_server.sh                   |   2 +-
 8 files changed, 263 insertions(+), 377 deletions(-)
```

> AGENT

现在我已掌握足够信息，可以提供一份全面的技术摘要。让我再核实一个关于 MARS CUDA kernel 的细节。

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"MARS\\|mars_theta\\|top2_ratio\\|top2_token\\|logit_ratio\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py | head -30",
  "description": "Get MARS implementation details in eagle_info"
}
```

> TOOL

tool_result Bash
```
25:# MARS verify (arXiv:2601.15498): theta < 0 disables, default. Recommended 0.9.
26:_MARS_THETA = float(os.environ.get("EAGLE_MARS_THETA", "-1.0"))
103:    # Per-mode MARS verify theta. Negative = disabled (standard greedy verify).
104:    # Set by EAGLEWorker._apply_spec_config from EAGLE_D{5,7}_MARS_THETA env so
107:    mars_theta: float = -1.0
347:            # MARS (Margin-Aware Speculative verification, arXiv:2601.15498):
349:            # Enabled when EAGLE_MARS_THETA >= 0; default disabled (-1.0) keeps standard SD.
351:            # for dynamic D5/D7 modes). Fall back to module-level _MARS_THETA
354:            inst_theta = getattr(self, "mars_theta", -1.0)
355:            mars_theta = float(inst_theta) if inst_theta >= 0.0 else float(_MARS_THETA)
356:            if mars_theta >= 0.0:
359:                top2_token = top2.indices[..., 1].reshape(bs, self.draft_token_num).contiguous()
362:                # ratio = z2/z1 only when z1 > 0; else -1.0 (never triggers MARS)
364:                top2_ratio = ratio.reshape(bs, self.draft_token_num).contiguous().float()
368:                top2_token = None
369:                top2_ratio = None
381:                top2_token=top2_token,
382:                top2_ratio=top2_ratio,
383:                mars_theta=mars_theta,
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py",
  "limit": 40,
  "offset": 345
}
```

> TOOL

tool_result Read
```
345	        if is_all_greedy or not TREE_SPEC_KERNEL_AVAILABLE:
346	          with torch.profiler.record_function("verify_tree_greedy"):
347	            # MARS (Margin-Aware Speculative verification, arXiv:2601.15498):
348	            # accept draft if it == argmax (top-1) OR (it == top-2 AND z2/z1 > theta).
349	            # Enabled when EAGLE_MARS_THETA >= 0; default disabled (-1.0) keeps standard SD.
350	            # Prefer per-instance theta (set by EAGLEWorker._apply_spec_config
351	            # for dynamic D5/D7 modes). Fall back to module-level _MARS_THETA
352	            # only when caller didn't plumb it (legacy single-mode workers /
353	            # idle EagleVerifyInput from cuda_graph_runner.get_spec_info).
354	            inst_theta = getattr(self, "mars_theta", -1.0)
355	            mars_theta = float(inst_theta) if inst_theta >= 0.0 else float(_MARS_THETA)
356	            if mars_theta >= 0.0:
357	                top2 = torch.topk(logits_output.next_token_logits, 2, dim=-1)
358	                target_predict = top2.indices[..., 0].reshape(bs, self.draft_token_num)
359	                top2_token = top2.indices[..., 1].reshape(bs, self.draft_token_num).contiguous()
360	                z1 = top2.values[..., 0]
361	                z2 = top2.values[..., 1]
362	                # ratio = z2/z1 only when z1 > 0; else -1.0 (never triggers MARS)
363	                ratio = torch.where(z1 > 0, z2 / z1, torch.full_like(z2, -1.0))
364	                top2_ratio = ratio.reshape(bs, self.draft_token_num).contiguous().float()
365	            else:
366	                target_predict = torch.argmax(logits_output.next_token_logits, dim=-1)
367	                target_predict = target_predict.reshape(bs, self.draft_token_num)
368	                top2_token = None
369	                top2_ratio = None
370	
371	            predict, accept_index, accept_length = verify_tree_greedy_func(
372	                predicts=predict,  # mutable
373	                accept_index=accept_index,  # mutable
374	                accept_token_num=accept_length,  # mutable
375	                candidates=candidates,
376	                retrive_index=self.retrive_index,
377	                [REDACTED],
378	                retrive_next_sibling=self.retrive_next_sibling,
379	                target_predict=target_predict,
380	                topk=self.topk,
381	                top2_token=top2_token,
382	                top2_ratio=top2_ratio,
383	                mars_theta=mars_theta,
384	            )
```

> TOOL

tool_use Bash
```json
{
  "command": "git show 2162051 --stat && echo \"===\" && git show f4bea68 --stat && echo \"===\" && git show 6cd79ae --stat",
  "description": "Show stat for operator optimization commits"
}
```

> TOOL

tool_result Bash
```
commit 2162051053144610d8f9de6a71737142f8cea7aa
Author: SOAR User <[REDACTED]>
Date:   Tue Mar 31 20:31:54 2026 +0000

    perf: fuse residual+scale_depth into single torch.add kernel
    
    Replace `residual + hidden_states * (scale_depth / sqrt(N))` with
    `torch.add(residual, hidden_states, alpha=precomputed_scale)`.
    
    Eliminates 64 redundant mul kernels per forward (2 per layer × 32).
    Fused path is strictly more precise vs F64 ground truth.
    
    Offline verified: 32-layer cos_sim >= 0.99998, CUDA graph compatible.
    Decode M=1: 237us/fwd saved. Prefill M=4096: 4.4ms/fwd saved.
    
    Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

 CLAUDE.md                                            | 14 +++++++++++++-
 demo-sala/sglang/python/sglang/srt/models/minicpm.py |  9 +++------
 2 files changed, 16 insertions(+), 7 deletions(-)
===
commit f4bea68f5e8de25b305bcb52dec57cf5dac1ac61
Author: SOAR User <[REDACTED]>
Date:   Tue Mar 31 20:05:35 2026 +0000

    perf: eliminate redundant F32 dtype cast in RoPE for all 32 layers
    
    sgl_kernel's apply_rope_with_cos_sin_cache_inplace already computes
    in F32 internally regardless of input dtype. The outer .float() and
    .to(bf16) casts were pure memory bandwidth waste.
    
    Offline verified: cos_sim=1.0, max_diff=0 across all seq lengths and
    position ranges. Dot product consistency preserved exactly.
    
    Benchmarked savings (24 Lightning + 8 Standard Attention layers):
    - Decode M=1 (CUDA graph): 140us/forward (3.5x per-layer speedup)
    - Prefill M=8192: 11.2ms/forward (4.5x per-layer speedup)
    
    Also fix .gitignore: /models/ instead of models/ to avoid ignoring
    demo-sala/sglang/srt/models/ subdirectory.
    
    Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

 .gitignore                                         |   4 +-
 CLAUDE.md                                          |   9 +-
 .../sglang/python/sglang/srt/models/minicpm.py     | 669 +++++++++++++++++++++
 3 files changed, 679 insertions(+), 3 deletions(-)
===
commit 6cd79ae131f522e35741bb2dd947d9b0d74dc7c6
Author: SOAR User <[REDACTED]>
Date:   Tue Mar 31 19:16:39 2026 +0000

    feat: hybrid Marlin/CUTLASS dispatch + 45K quant + submission cleanup
    
    - Implement hybrid decode: M<=threshold→Marlin W4A16, M>threshold→CUTLASS W4A4
    - Add SGLANG_MARLIN_DECODE_THRESHOLD env var (replaces SGLANG_FORCE_NVFP4_MARLIN)
    - Reduce quant context 48K→45K, set both PYTORCH_ALLOC_CONF variants for OOM fix
    - Remove sgl-kernel-deps from submission (989MB→44MB tarball)
    - Add offline hybrid consistency test + Marlin vs CUTLASS benchmark
    - Clean up prepare_env/model scripts, update CLAUDE.md
    
    Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

 CLAUDE.md                                          |  78 ++++---
 bench/bench_marlin_vs_cutlass.py                   | 211 +++++++++++++++++
 bench/mini_bench.sh                                |   4 +-
 bench/sglang_0331_16_custom.jsonl                  |   2 +
 bench/sglang_0331_3_custom.jsonl                   |   1 +
 bench/sglang_0331_64_custom.jsonl                  |   4 +
 bench/sglang_0331_8_custom.jsonl                   |   2 +
 bench/test_hybrid_offline.py                       | 254 +++++++++++++++++++++
 demo-sala/prepare_env.sh                           |  71 +-----
 demo-sala/prepare_model.sh                         |  72 +-----
 .../srt/layers/quantization/modelopt_quant.py      | 192 ++++++----------
 eval/start_public_eval_server.sh                   |  14 +-
 probe-sala/prepare_env.sh                          |  67 +-----
 probe-sala/prepare_model.sh                        |   2 +-
 14 files changed, 621 insertions(+), 353 deletions(-)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py",
  "limit": 200,
  "offset": 1073
}
```

> TOOL

tool_result Read
```
1073	class ModelOptFp4LinearMethod(LinearMethodBase):
1074	    """Linear method for NVFP4.
1075	    Supports loading NVFP4 checkpoints with the following structure:
1076	
1077	    |Tensor Name           | datatype      |  shape      |
1078	    |----------------------------------------------------|
1079	    |input_scale           | torch.float32 | scalar      |
1080	    |weight                | NVFP4(SE2M1)  | [1, X, y/2] |
1081	    |weight_scale          | FP8-E4M3      | [X, Y]      |
1082	    |weight_scale_2        | torch.float32 | scalar      |
1083	
1084	    The weights are quantized per block of 16 elements.
1085	    Args: quant_config: The ModelOpt quantization config.
1086	    """
1087	
1088	    def __init__(self, quant_config: ModelOptFp4Config):
1089	        self.quant_config = quant_config
1090	
1091	    def create_weights(
1092	        self,
1093	        layer: torch.nn.Module,
1094	        input_size_per_partition: int,
1095	        output_partition_sizes: List[int],
1096	        input_size: int,
1097	        output_size: int,
1098	        params_dtype: torch.dtype,
1099	        **extra_weight_attrs,
1100	    ):
1101	        del input_size, output_size
1102	        if not self.quant_config.is_checkpoint_nvfp4_serialized:
1103	            raise ValueError(
1104	                "NVFP4 quantization was selected, "
1105	                " dynamic quantization is not supported."
1106	            )
1107	
1108	        output_size_per_partition = sum(output_partition_sizes)
1109	        weight_loader = extra_weight_attrs.get("weight_loader")
1110	
1111	        layer.logical_widths = output_partition_sizes
1112	
1113	        layer.input_size_per_partition = input_size_per_partition
1114	        layer.output_size_per_partition = output_size_per_partition
1115	        if input_size_per_partition % 16 != 0:
1116	            raise ValueError(
1117	                "Unsupported model when in features size is " "not multiple of 16"
1118	            )
1119	
1120	        weight_dtype = (
1121	            torch.float8_e4m3fn
1122	            if self.quant_config.is_checkpoint_nvfp4_serialized
1123	            else params_dtype
1124	        )
1125	
1126	        weight = ModelWeightParameter(
1127	            data=torch.empty(
1128	                # 2 fp4 data is packed in one uint8 in the input dimension
1129	                output_size_per_partition,
1130	                input_size_per_partition // 2,
1131	                dtype=torch.uint8,
1132	            ),
1133	            input_dim=1,
1134	            output_dim=0,
1135	            weight_loader=weight_loader,
1136	        )
1137	        layer.register_parameter("weight", weight)
1138	
1139	        input_scale = PerTensorScaleParameter(
1140	            data=torch.empty(len(output_partition_sizes), dtype=torch.float32),
1141	            weight_loader=weight_loader,
1142	        )
1143	
1144	        layer.register_parameter("input_scale", input_scale)
1145	
1146	        weight_scale_2 = PerTensorScaleParameter(
1147	            data=torch.empty(len(output_partition_sizes), dtype=torch.float32),
1148	            weight_loader=weight_loader,
1149	        )
1150	        layer.register_parameter("weight_scale_2", weight_scale_2)
1151	
1152	        weight_scale = ModelWeightParameter(
1153	            data=torch.empty(
1154	                output_size_per_partition,
1155	                input_size_per_partition // self.quant_config.group_size,
1156	                dtype=weight_dtype,
1157	            ),
1158	            input_dim=1,
1159	            output_dim=0,
1160	            weight_loader=weight_loader,
1161	        )
1162	
1163	        layer.register_parameter("weight_scale", weight_scale)
1164	
1165	        # AWQ checkpoints may include per-channel pre_quant_scale for input smoothing.
1166	        if self.quant_config.has_pre_quant_scale:
1167	            pre_quant_scale = ModelWeightParameter(
1168	                data=torch.ones(input_size_per_partition, dtype=torch.float32),
1169	                input_dim=0,
1170	                output_dim=None,
1171	                weight_loader=weight_loader,
1172	            )
1173	            layer.register_parameter("pre_quant_scale", pre_quant_scale)
1174	
1175	    def process_weights_after_loading(self, layer: torch.nn.Module) -> None:
1176	        input_scale_2 = layer.input_scale.max().to(torch.float32)
1177	        weight_scale_2 = layer.weight_scale_2.max().to(torch.float32)
1178	        layer.input_scale = Parameter(input_scale_2, requires_grad=False)
1179	        layer.weight_scale_2 = Parameter(weight_scale_2, requires_grad=False)
1180	
1181	        # Finalize AWQ pre_quant_scale: move to CUDA and cast to bf16 so that
1182	        # x * pre_quant_scale stays in bf16 without an extra .to() in apply().
1183	        if hasattr(layer, "pre_quant_scale"):
1184	            layer.pre_quant_scale = Parameter(
1185	                layer.pre_quant_scale.data.to(
1186	                    device="cuda", dtype=torch.bfloat16
1187	                ),
1188	                requires_grad=False,
1189	            )
1190	        layer.alpha = Parameter(
1191	            layer.input_scale * layer.weight_scale_2, requires_grad=False
1192	        )
1193	        layer.input_scale_inv = Parameter(
1194	            (1 / input_scale_2).to(torch.float32), requires_grad=False
1195	        )
1196	
1197	        # Full Marlin FP4 fallback for non-Blackwell GPUs (SM < 100 but SM >= 75)
1198	        from sglang.srt.layers.quantization.marlin_utils_fp4 import (
1199	            is_fp4_marlin_supported,
1200	            prepare_fp4_layer_for_marlin,
1201	            should_use_fp4_marlin_fallback,
1202	        )
1203	        if should_use_fp4_marlin_fallback() and _MARLIN_HYBRID_THRESHOLD <= 0:
1204	            prepare_fp4_layer_for_marlin(
1205	                layer,
1206	                weight_attr="weight",
1207	                weight_scale_attr="weight_scale",
1208	                weight_global_scale_attr="weight_scale_2",
1209	            )
1210	            layer._use_fp4_marlin = True
1211	            return
1212	
1213	        if FLASHINFER_FP4_GEMM_BACKEND == "trtllm":
1214	            # FlashInfer TRTLLM FP4 GEMM requires a different weight layout.
1215	            # FlashInfer provides nvfp4_quantize to quantize + shuffle the
1216	            # layout but we use our own quantization so we have to call
1217	            # shuffles ourselves.
1218	            from flashinfer import shuffle_matrix_a, shuffle_matrix_sf_a
1219	
1220	            weight = layer.weight
1221	            scale = layer.weight_scale
1222	            epilogue_tile_m = 128
1223	            weight = shuffle_matrix_a(weight.view(torch.uint8), epilogue_tile_m)
1224	            scale = (
1225	                shuffle_matrix_sf_a(scale.view(torch.uint8), epilogue_tile_m)
1226	                .reshape(scale.shape)
1227	                .view(torch.float8_e4m3fn)
1228	            )
1229	
1230	            layer.weight_scale_interleaved = Parameter(scale, requires_grad=False)
1231	            layer.weight = Parameter(weight, requires_grad=False)
1232	            return
1233	        # Pad and blockwise interleave weight_scale
1234	        scales = layer.weight_scale
1235	        scale_ndim = scales.ndim
1236	        if scale_ndim == 2:
1237	            scales = scales.unsqueeze(0)
1238	        assert scales.ndim == 3
1239	        B, M, K = scales.shape
1240	        round_up_multiple = lambda x, m: (x + m - 1) // m * m
1241	        M_padded = round_up_multiple(M, 128)
1242	        K_padded = round_up_multiple(K, 4)
1243	        padded_scales = torch.zeros((B, M_padded, K_padded), dtype=scales.dtype)
1244	        padded_scales[:B, :M, :K] = scales
1245	        batches, rows, cols = padded_scales.shape
1246	        assert rows % 128 == 0
1247	        assert cols % 4 == 0
1248	        padded_scales = padded_scales.reshape(batches, rows // 128, 4, 32, cols // 4, 4)
1249	        padded_scales = padded_scales.permute((0, 1, 4, 3, 2, 5))
1250	        padded_scales = padded_scales.contiguous().cuda()
1251	        padded_scales = (
1252	            padded_scales.reshape(M_padded, K_padded)
1253	            if scale_ndim == 2
1254	            else padded_scales.reshape(B, M_padded, K_padded)
1255	        )
1256	        layer.weight_scale_interleaved = Parameter(padded_scales, requires_grad=False)
1257	
1258	        # Hybrid Marlin: prepare Marlin FP4 weights alongside CUTLASS
1259	        # Original weight/weight_scale are still intact after CUTLASS prep above
1260	        if _MARLIN_HYBRID_THRESHOLD > 0 and is_fp4_marlin_supported():
1261	            self._prepare_hybrid_marlin(layer)
1262	            layer._hybrid_marlin_threshold = _MARLIN_HYBRID_THRESHOLD
1263	
1264	    @staticmethod
1265	    def _prepare_hybrid_marlin(layer):
1266	        """Prepare Marlin FP4 (float4_e2m1f) weights for decode acceleration.
1267	
1268	        Stores repacked weights in separate attributes (weight_marlin, etc.)
1269	        so the original NVFP4 weights remain available for the CUTLASS path.
1270	        """
1271	        from sgl_kernel import gptq_marlin_repack
1272	        from sglang.srt.layers.quantization.marlin_utils import (
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py",
  "limit": 200,
  "offset": 1273
}
```

> TOOL

tool_result Read
```
1273	            marlin_make_workspace,
1274	            marlin_permute_scales,
1275	        )
1276	        from sglang.srt.layers.quantization.marlin_utils_fp4 import (
1277	            FP4_MARLIN_GROUP_SIZE,
1278	            nvfp4_marlin_process_global_scale,
1279	            nvfp4_marlin_process_scales,
1280	        )
1281	
1282	        part_size_n = layer.output_size_per_partition
1283	        part_size_k = layer.input_size_per_partition
1284	        param_dtype = layer.params_dtype  # match model dtype (bfloat16)
1285	        device = layer.weight.device
1286	
1287	        # Weight repack: NVFP4 (N, K/2) uint8 → Marlin tile (K/8, N) int32
1288	        perm = torch.empty(0, dtype=torch.int, device=device)
1289	        qweight = layer.weight.data.view(torch.int32).T.contiguous()
1290	        marlin_qweight = gptq_marlin_repack(qweight, perm, part_size_k, part_size_n, 4)
1291	        del qweight
1292	        layer.weight_marlin = Parameter(marlin_qweight, requires_grad=False)
1293	
1294	        # Scale: transpose → permute → FP8-S0E5M3 (halved)
1295	        weight_scale = layer.weight_scale.data.T.contiguous().to(param_dtype)
1296	        weight_scale = marlin_permute_scales(
1297	            weight_scale, part_size_k, part_size_n, FP4_MARLIN_GROUP_SIZE
1298	        )
1299	        weight_scale = nvfp4_marlin_process_scales(weight_scale)
1300	        layer.weight_scale_marlin = Parameter(weight_scale, requires_grad=False)
1301	
1302	        # Global scale: adjust exponent bias for Marlin kernel
1303	        global_scale = layer.weight_scale_2.data.to(param_dtype)
1304	        global_scale = nvfp4_marlin_process_global_scale(global_scale)
1305	        layer.weight_global_scale_marlin = Parameter(global_scale, requires_grad=False)
1306	
1307	        layer.marlin_workspace = marlin_make_workspace(device)
1308	        logger.info(
1309	            "Hybrid Marlin: prepared %s (N=%d, K=%d), threshold=%d",
1310	            "layer", part_size_n, part_size_k, _MARLIN_HYBRID_THRESHOLD,
1311	        )
1312	
1313	    def apply(
1314	        self,
1315	        layer: torch.nn.Module,
1316	        x: torch.Tensor,
1317	        bias: Optional[torch.Tensor] = None,
1318	    ) -> torch.Tensor:
1319	        output_dtype = x.dtype
1320	        x_m, _ = x.shape
1321	        output_shape = list(x.shape[:-1]) + [layer.output_size_per_partition]
1322	
1323	        # Full Marlin FP4 fallback (non-Blackwell, SM >= 75, no hybrid)
1324	        if getattr(layer, "_use_fp4_marlin", False):
1325	            from sglang.srt.layers.quantization.marlin_utils_fp4 import (
1326	                apply_fp4_marlin_linear,
1327	            )
1328	            x_in = x
1329	            if hasattr(layer, "pre_quant_scale"):
1330	                x_in = x * layer.pre_quant_scale
1331	            return apply_fp4_marlin_linear(
1332	                input=x_in,
1333	                weight=layer.weight,
1334	                weight_scale=layer.weight_scale,
1335	                weight_global_scale=layer.weight_scale_2,
1336	                workspace=layer.marlin_workspace,
1337	                size_n=layer.output_size_per_partition,
1338	                size_k=layer.input_size_per_partition,
1339	                bias=bias,
1340	            )
1341	
1342	        # Hybrid Marlin decode path: M <= threshold → Marlin FP4 (W4A16)
1343	        threshold = getattr(layer, "_hybrid_marlin_threshold", 0)
1344	        if threshold > 0 and x_m <= threshold:
1345	            from sglang.srt.layers.quantization.marlin_utils_fp4 import (
1346	                apply_fp4_marlin_linear,
1347	            )
1348	            x_in = x
1349	            if hasattr(layer, "pre_quant_scale"):
1350	                x_in = x * layer.pre_quant_scale
1351	            return apply_fp4_marlin_linear(
1352	                input=x_in,
1353	                weight=layer.weight_marlin,
1354	                weight_scale=layer.weight_scale_marlin,
1355	                weight_global_scale=layer.weight_global_scale_marlin,
1356	                workspace=layer.marlin_workspace,
1357	                size_n=layer.output_size_per_partition,
1358	                size_k=layer.input_size_per_partition,
1359	                bias=bias,
1360	            )
1361	
1362	        # NVFP4 CUTLASS path (prefill, or decode when hybrid disabled)
1363	        w_n, _ = layer.weight.shape
1364	        if hasattr(layer, "pre_quant_scale"):
1365	            x = x * layer.pre_quant_scale
1366	        x_fp4, x_scale_interleaved = fp4_quantize(x, layer.input_scale_inv)
1367	
1368	        w = layer.weight
1369	        w_scale_interleaved = layer.weight_scale_interleaved
1370	        if enable_flashinfer_fp4_gemm:
1371	            w = layer.weight.T
1372	            w_scale_interleaved = layer.weight_scale_interleaved.T
1373	        out = fp4_gemm(
1374	            x_fp4,
1375	            w,
1376	            x_scale_interleaved,
1377	            w_scale_interleaved,
1378	            layer.alpha,
1379	            output_dtype,
1380	            w_n,
1381	        )
1382	        if bias is not None:
1383	            out = out + bias
1384	        return out.view(*output_shape)
1385	
1386	
1387	class ModelOptNvFp4FusedMoEMethod(FusedMoEMethodBase):
1388	    """
1389	       MoE Method for FP4 Quantization with Blockscales and PerTensorScales
1390	    Args:
1391	        quant_config: NVFP4 Quant Config
1392	    """
1393	
1394	    def __init__(self, quant_config: ModelOptFp4Config):
1395	        self.quant_config = quant_config
1396	        if not is_blackwell_supported():
1397	            raise ValueError(
1398	                "Current platform does not support NVFP4"
1399	                " quantization. Please use Blackwell and"
1400	                " above."
1401	            )
1402	        self.enable_flashinfer_trtllm_moe = (
1403	            get_moe_runner_backend().is_flashinfer_trtllm()
1404	        )
1405	        self._cache_permute_indices = {}
1406	
1407	    @property
1408	    def enable_flashinfer_cutlass_moe(self) -> bool:
1409	        from sglang.srt.layers.moe import get_moe_runner_backend
1410	
1411	        """Access the global enable_flashinfer_cutlass_moe setting."""
1412	        return get_moe_runner_backend().is_flashinfer_cutlass()
1413	
1414	    @property
1415	    def enable_flashinfer_cutedsl_moe(self) -> bool:
1416	        from sglang.srt.layers.moe import get_moe_runner_backend
1417	
1418	        """Access the global enable_flashinfer_cutedsl_moe setting."""
1419	        return get_moe_runner_backend().is_flashinfer_cutedsl()
1420	
1421	    def create_weights(
1422	        self,
1423	        layer: torch.nn.Module,
1424	        num_experts: int,
1425	        hidden_size: int,
1426	        intermediate_size_per_partition: int,
1427	        params_dtype: torch.dtype,
1428	        **extra_weight_attrs,
1429	    ):
1430	        if not self.quant_config.is_checkpoint_nvfp4_serialized:
1431	            raise ValueError(
1432	                "NVFP4 quantization was selected, "
1433	                " dynamic quantization is not supported."
1434	            )
1435	
1436	        # TODO(ch-wan): check if this is needed
1437	        layer.intermediate_size_per_partition = intermediate_size_per_partition
1438	        layer.params_dtype = params_dtype
1439	        layer.quant_config = self.quant_config
1440	
1441	        weight_dtype = torch.uint8
1442	        weight_scale_dtype = torch.float8_e4m3fn
1443	        weight_loader = extra_weight_attrs.get("weight_loader")
1444	        # GEMM 1
1445	        num_shards = 2 if layer.moe_runner_config.is_gated else 1
1446	
1447	        w13_weight = ModelWeightParameter(
1448	            data=torch.empty(
1449	                layer.num_local_experts,
1450	                num_shards * intermediate_size_per_partition,
1451	                # 2 fp4 items are packed in the input dimension
1452	                hidden_size // 2,
1453	                dtype=weight_dtype,
1454	            ),
1455	            input_dim=1,
1456	            output_dim=2,
1457	            weight_loader=weight_loader,
1458	        )
1459	        layer.register_parameter("w13_weight", w13_weight)
1460	
1461	        # GEMM 2
1462	        w2_weight = ModelWeightParameter(
1463	            data=torch.empty(
1464	                layer.num_local_experts,
1465	                hidden_size,
1466	                # 2 fp4 items are packed in the input dimension
1467	                intermediate_size_per_partition // 2,
1468	                dtype=weight_dtype,
1469	            ),
1470	            input_dim=1,
1471	            output_dim=2,
1472	            weight_loader=weight_loader,
```

> AGENT

现在我来查看一下 Medusa 提交的性能数据以及 CLAUDE.md 文件，以获取整体上下文。

> TOOL

tool_use Bash
```json
{
  "command": "git show c6b7991 --format=\"%B\" | head -20",
  "description": "Medusa commit message"
}
```

> TOOL

tool_result Bash
```
feat: Medusa speculative decoding integration (S1 -12%, S8 -12.5%)

Medusa uses K=3 parallel ResBlock heads on target hidden states to draft
tokens, verified in a single batched TARGET_VERIFY forward pass.
Achieves peak 208 tok/s (vs 111 baseline), limited by draft model quality
(avg accept_len ~1.7, accept_rate ~42%).

Core implementation:
- medusa_worker.py: draft, verify, GLA rollback, sparse k1/k2 alloc
- MedusaVerifyInput in eagle_info.py for TARGET_VERIFY batch setup
- MEDUSA enum + is_medusa() in spec_info.py
- Server args: dtn=K+1, disable overlap, reserved mem handling
- Scheduler: Medusa output processing, filter_batch fix

CUDA graph compatibility:
- SimpleGLA: pre-allocated step buffers in init_cuda_graph_state
- FlashInfer: prefill wrapper with use_cuda_graph=True, full-size
  kv_indices buffer to handle any sequence length at replay
- CaptureHiddenMode.LAST for draft head hidden states
```

> TOOL

tool_use Bash
```json
{
  "command": "git show 5552a23 --format=\"%B\" | head -20",
  "description": "Tune no-spec decode kernels commit"
}
```

> TOOL

tool_result Bash
```
perf: tune no-spec decode kernels


diff --git a/bench/b12x/bench_nospec_crossover.py b/bench/b12x/bench_nospec_crossover.py
new file mode 100755
index 0000000..6d323fc
--- /dev/null
+++ b/bench/b12x/bench_nospec_crossover.py
@@ -0,0 +1,473 @@
+#!/usr/bin/env python3
+"""No-spec MiniCPM-SALA FP4 dispatch crossover bench.
+
+This is intentionally production-shaped instead of a pure GEMM microbench:
+
+* Marlin is timed as W4A16 with bf16 activation input.
+* b12x and CUTLASS are timed as activation-quantize + W4A4 GEMM, matching
+  ModelOptNvFp4LinearMethod.apply().
+* The M grid includes no-spec decode M values plus chunked-prefill buckets and
+  tails from the allowed mini bench mix: 3*S1, 8*S8, 0*Smax.
+
```

> TOOL

tool_use Bash
```json
{
  "command": "git show 20cc58a --format=\"%B\" | head -30",
  "description": "Kill hot-path wastes commit"
}
```

> TOOL

tool_result Bash
```
perf(eagle/dynamic): kill three hot-path wastes in spec decode

Three independent fixes on the spec-decode hot path. Each is a
strict improvement (helps both EAGLE_DYNAMIC_MODE=0 and =1), no
behavioural change beyond removing redundant work.

#1 minicpm_backend: stop rebuilding verify_qo_indptr per step
  Replay was running torch.arange + copy_ to rewrite the qo_indptr
  buffer every TARGET_VERIFY step (8 standard-attn layers share one
  metadata, so 1 GPU kernel + alloc per step). Pre-build a per-dtn
  bank of indptr buffers in init_cuda_graph_state and just pick the
  matching one — zero hot-path arange / copy_. Same change in
  capture for symmetry.

#2 cuda_graph_runner: collapse double _get_graph_key in replay
  replay_prepare and replay each called _get_graph_key, which does
  attribute chain access + f-string + dict lookup. Cache the graph
  kind ("default" / "decode" / "d5") on self in replay_prepare;
  replay rebuilds the key from self.bs + cached kind. Affects every
  cuda graph replay path (decode, medusa, EAGLE static, EAGLE dynamic).

#3 eagle_worker: lazy draft KV catch-up across NO_SPEC runs
  NO_SPEC was paying a [REDACTED] per
  step purely to keep draft KV in sync — but draft KV is never read
  while NO_SPEC stays active, so each of those prefills was waste
  (estimated 0.3-1ms/step at bs=58). Now NO_SPEC parks (token, last
  hidden) on self._no_spec_pending keyed by req.rid; the first
  MARS_D5/D7 step after NO_SPEC ends triggers _flush_no_spec_pending,
  which builds one multi-token DRAFT_EXTEND covering all accumulated
  tokens. Filter / merge are handled implicitly by keying on rid.
```

> AGENT

现在让我更详细地检查 scale loader bug commit 和 Marlin FP4 scale bug fix。

> TOOL

tool_use Bash
```json
{
  "command": "git show f7faed5 --stat -p -- \"*.py\" | head -200",
  "description": "Read the scale loader bug fix diff"
}
```

> TOOL

tool_result Bash
```
commit f7faed59005e86342e39e7fc41c54f1a6e2a9017
Author: SOAR User <[REDACTED]>
Date:   Wed Apr 15 13:25:08 2026 +0000

    fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards
    
    user_4813494d cause: QKVParallelLinear and MergedColumnParallelLinear loaded fused
    per-tensor scales (weight_scale_2, input_scale) into shard_id=0 only,
    leaving remaining slots as torch.empty garbage. Post-load max() absorbed
    the undefined data, corrupting qkv_proj scale and producing Inf/NaN.
    
    Fix: PerTensorScaleParameter.load_fused_per_tensor_weight() broadcasts
    scalar scales to all logical shards, and loads full vectors element-wise.
    Both old (scalar) and new (vector) checkpoint formats are supported.
    
    Also: respect explicit --speculative-draft-attention-backend flag instead
    of always overriding to flashinfer when target uses minicpm_flashinfer.
    
    Verified: flashinfer+graph ON accept_len=1.50 stable, zero NaN across
    all backend/graph combinations (6-config matrix regression).
    
    Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
---
 .../sglang/python/sglang/srt/layers/linear.py      |   9 +-
 .../sglang/python/sglang/srt/layers/parameter.py   |  24 ++++
 .../python/sglang/srt/speculative/eagle_info.py    |   1 +
 .../python/sglang/srt/speculative/eagle_worker.py  |   5 +-
 tests/test_eagle_fused_scale_loader.py             | 125 +++++++++++++++++++++
 5 files changed, 156 insertions(+), 8 deletions(-)

diff --git a/demo-sala/sglang/python/sglang/srt/layers/linear.py b/demo-sala/sglang/python/sglang/srt/layers/linear.py
index 428f3a2..e538787 100644
--- a/demo-sala/sglang/python/sglang/srt/layers/linear.py
+++ b/demo-sala/sglang/python/sglang/srt/layers/linear.py
@@ -730,12 +730,7 @@ class MergedColumnParallelLinear(ColumnParallelLinear):
     ):
         if loaded_shard_id is None:
             if isinstance(param, PerTensorScaleParameter):
-                param.load_merged_column_weight(
-                    loaded_weight=loaded_weight,
-                    shard_id=0,
-                    tp_rank=self.tp_rank,
-                    tp_size=self.tp_size,
-                )
+                param.load_fused_per_tensor_weight(loaded_weight=loaded_weight)
                 return
             elif type(param) in (RowvLLMParameter, BasevLLMParameter):
                 param.load_merged_column_weight(
@@ -972,7 +967,7 @@ class QKVParallelLinear(ColumnParallelLinear):
     ):
         if loaded_shard_id is None:  # special case for certain models
             if isinstance(param, PerTensorScaleParameter):
-                param.load_qkv_weight(loaded_weight=loaded_weight, shard_id=0)
+                param.load_fused_per_tensor_weight(loaded_weight=loaded_weight)
                 return
             elif type(param) in (RowvLLMParameter, BasevLLMParameter):
                 param.load_qkv_weight(loaded_weight=loaded_weight)
diff --git a/demo-sala/sglang/python/sglang/srt/layers/parameter.py b/demo-sala/sglang/python/sglang/srt/layers/parameter.py
index 3cc1d23..9028ca3 100644
--- a/demo-sala/sglang/python/sglang/srt/layers/parameter.py
+++ b/demo-sala/sglang/python/sglang/srt/layers/parameter.py
@@ -368,6 +368,30 @@ class PerTensorScaleParameter(BasevLLMParameter):
         kwargs.pop("use_presharded_weights", None)
         super().load_row_parallel_weight(*args, **kwargs)
 
+    def load_fused_per_tensor_weight(self, loaded_weight: torch.Tensor):
+        """Load a fused per-tensor scale blob.
+
+        Fused QKV / gate_up checkpoints may serialize auxiliary scales either as:
+        - a scalar to be shared by every logical shard, or
+        - a full vector with one entry per logical shard.
+
+        Older EAGLE3 exporters emitted a scalar for fused NVFP4 qkv/gate_up. If we
+        only write shard 0, the remaining slots keep torch.empty garbage and later
+        post-load max() will absorb that undefined data.
+        """
+
+        param_data = self.data
+        loaded_flat = loaded_weight.reshape(-1)
+        if loaded_flat.numel() == 1:
+            param_data.copy_(loaded_flat.expand_as(param_data))
+            return
+
+        assert loaded_flat.numel() == param_data.numel(), (
+            f"Expected fused per-tensor scale with {param_data.numel()} values, "
+            f"got {loaded_flat.numel()}"
+        )
+        param_data.copy_(loaded_flat.view_as(param_data))
+
     def _load_into_shard_id(
         self, loaded_weight: torch.Tensor, shard_id: Union[str, int], **kwargs
     ):
diff --git a/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py b/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py
index 161d603..06e812d 100644
--- a/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py
+++ b/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py
@@ -310,6 +310,7 @@ class EagleVerifyInput(SpecInput, EagleVerifyInputV2Mixin):
         if is_all_greedy or not TREE_SPEC_KERNEL_AVAILABLE:
             target_predict = torch.argmax(logits_output.next_token_logits, dim=-1)
             target_predict = target_predict.reshape(bs, self.draft_token_num)
+
             predict, accept_index, accept_length = verify_tree_greedy_func(
                 predicts=predict,  # mutable
                 accept_index=accept_index,  # mutable
diff --git a/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py b/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py
index 53afd72..da7ee3b 100644
--- a/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py
+++ b/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py
@@ -176,7 +176,10 @@ class EAGLEWorker(TpModelWorker):
         server_args.speculative_draft_model_quantization = draft_quant
         # Draft model (Llama architecture) should use standard flashinfer, not minicpm_flashinfer
         backup_draft_attn = server_args.speculative_draft_attention_backend
-        if server_args.attention_backend == "minicpm_flashinfer":
+        if (
+            server_args.attention_backend == "minicpm_flashinfer"
+            and backup_draft_attn in (None, "minicpm_flashinfer")
+        ):
             server_args.speculative_draft_attention_backend = "flashinfer"
         # Share the allocator with a target worker.
         # Draft and target worker own their own KV cache pools.
diff --git a/tests/test_eagle_fused_scale_loader.py b/tests/test_eagle_fused_scale_loader.py
new file mode 100644
index 0000000..1ecb203
--- /dev/null
+++ b/tests/test_eagle_fused_scale_loader.py
@@ -0,0 +1,125 @@
+#!/usr/bin/env python3
+"""Offline regression tests for fused NVFP4 auxiliary-scale loading."""
+
+import ast
+import importlib.util
+import sys
+import unittest
+from pathlib import Path
+
+import torch
+
+REPO_user_4813494d = Path("/user_4813494d/openbmb")
+SGLANG_PYTHON = REPO_user_4813494d / "demo-sala/sglang/python"
+LINEAR_PY = SGLANG_PYTHON / "sglang/srt/layers/linear.py"
+CONVERT_PY = REPO_user_4813494d / "eagle/convert_to_sglang.py"
+
+sys.path.insert(0, str(SGLANG_PYTHON))
+
+from sglang.srt.layers.parameter import PerTensorScaleParameter  # noqa: E402
+
+
+def _dummy_weight_loader(*args, **kwargs):
+    return None
+
+
+def _make_scale_param(size: int) -> PerTensorScaleParameter:
+    return PerTensorScaleParameter(
+        data=torch.empty(size, dtype=torch.float32),
+        weight_loader=_dummy_weight_loader,
+    )
+
+
+def _load_convert_module():
+    spec = importlib.util.spec_from_file_location("eagle_convert_to_sglang", CONVERT_PY)
+    module = importlib.util.module_from_spec(spec)
+    assert spec.loader is not None
+    spec.loader.exec_module(module)
+    return module
+
+
+def _method_calls_attr(module_path: Path, class_name: str, method_name: str, attr: str) -> bool:
+    tree = ast.parse(module_path.read_text())
+    for node in tree.body:
+        if isinstance(node, ast.ClassDef) and node.name == class_name:
+            for item in node.body:
+                if isinstance(item, ast.FunctionDef) and item.name == method_name:
+                    for subnode in ast.walk(item):
+                        if not isinstance(subnode, ast.Call):
+                            continue
+                        func = subnode.func
+                        if isinstance(func, ast.Attribute) and func.attr == attr:
+                            return True
+    return False
+
+
+class EagleFusedScaleLoaderTest(unittest.TestCase):
+    def test_scalar_broadcasts_to_all_qkv_scale_slots(self):
+        param = _make_scale_param(3)
+
+        param.load_fused_per_tensor_weight(torch.tensor(2.5))
+
+        self.assertTrue(torch.equal(param.data, torch.tensor([2.5, 2.5, 2.5])))
+
+    def test_scalar_broadcasts_to_all_gate_up_scale_slots(self):
+        param = _make_scale_param(2)
+
+        param.load_fused_per_tensor_weight(torch.tensor(1.25))
+
+        self.assertTrue(torch.equal(param.data, torch.tensor([1.25, 1.25])))
+
+    def test_full_scale_vector_is_loaded_verbatim(self):
+        param = _make_scale_param(3)
+        scale_vec = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float32)
+
```

> TOOL

tool_use Bash
```json
{
  "command": "git show 87a8bb1 --format=\"%B\" | head -40",
  "description": "Four small accelerations commit"
}
```

> TOOL

tool_result Bash
```
perf(eagle/dynamic): four small accelerations on the spec-decode hot path

Each fix is independent and offline-validated; smoketested across bs=1/8/16/32/36
plus repeated NO_SPEC <-> D5 <-> D7 transitions (zero flush warnings, coherent
output). No e2e bench yet — these are the "small but perceivable" wins.

#1 NO_SPEC lazy draft KV catch-up
  Skip the per-step [REDACTED] that ran purely
  to keep draft KV lock-step with target. Stash (target_hidden, next_token_id)
  per Req on pending_no_spec_{hidden,token_ids} during the streak; on the
  first non-NO_SPEC step, _flush_no_spec_pending replays the K stashed
  positions in ONE multi-token DRAFT_EXTEND. Filter/merge/finished cleanup
  are free since pending lives on the Req.
  Subtle bits handled:
    * Stale spec_info.topk_p tripping EagleDraftInput.filter_batch when a req
      finishes mid-streak — null out spec_info fields at end of each NO_SPEC
      step so filter routes through the topk_p=None branch.
    * Multi-token flush needs (bs*K,) out_cache_loc; the last NO_SPEC step
      only left (bs,). Gather kv slots from req_to_token_pool.req_to_token at
      [seq_len-K..seq_len) per req.
    * The draft_extend cuda graph runner's buffers are sized for
      bs * (steps+1) tokens (the 1-token-per-req post-prefill shape); flush's
      bs*K tokens overflow. Add num_tokens check to can_run so flush falls
      back to eager. Capture path unchanged.
    * Mid-streak EXTEND (mixed prefill+decode) drops pending with a warning;
      affected reqs see one D5/D7 step with degraded accept rate. Rare in
      practice; logged for diagnosis.

#2 _apply_spec_config early-return on unchanged mode
  D5 -> D5 is the steady-state hot path; the legacy "no early-return" comment
  was scoped to startup only. Cache _applied_spec_mode, return immediately
  when mode matches. MARS theta moves off a module-level _MARS_THETA write
  onto an EagleVerifyInput.mars_theta field plumbed via draft() — eagle_info
  reads from spec_info first, falls back to module global for legacy callers.
  ~0.2 us/step saved; dependability win is bigger.

#3 FlashInfer verify plan() takes CPU inputs
  plan() unconditionally does qo_indptr.to("cpu") + paged_kv_indptr.to("cpu")
  + paged_kv_last_page_len.to("cpu"), three D2H syncs per replay (~26 us
  total at any bs). Pre-build pinned-memory CPU twins of qo_indptr per dtn
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -rn \"scale.*bug\\|scale.*/2\\|cos_sim.*0.77\\|FP4.*scale.*fix\\|marlin_template\\|common_ops\" /user_4813494d/openbmb/docs/ 2>/dev/null | head -20",
  "description": "Search for Marlin FP4 scale bug references"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/docs/quantization.md:50:平台 sgl-kernel 0.3.20 的 `marlin_template.h` 有 FP4 scale `/2` bug（cos_sim 0.77）。修复：pre-built `common_ops.abi3.so`（SM120a）via `cp` 替换。
/user_4813494d/openbmb/docs/quantization.md:91:- **NVFP4 KV**：在 SALA 当前架构下**没有可落地路径**。老版本"`trtllm_batch_decode_with_kv_cache` 未传 `kv_block_scales`"的结论已过时（FlashInfer 0.6.8 已支持），真正阻塞点是 InfLLM-v2 sparse + page_size=1 的组合。完整调研（API 约束、SGLang fork latent bugs、全球 30+ 项目盘点、离线微基准数据、三条理论路径评估）见 [nvfp4-kv-investigation.md](nvfp4-kv-investigation.md)
/user_4813494d/openbmb/docs/prefill-accel-survey.md:114:| `trtllm_fmha_v2_prefill` + `skip_softmax_threshold_scale_factor>0` | **死（SM120 kernel bug）** | 任何非零阈值都返回 NaN/Inf；FlashInfer issue #2555 范畴 |
/user_4813494d/openbmb/docs/marlin-tuning.md:12:| sgl-kernel FP4 scale bug fix | ✅ 已部署 | `common_ops.abi3.so` pre-built 替换，scale `/2` bug（cos_sim 0.77→1.0）修复 |
/user_4813494d/openbmb/docs/marlin-tuning.md:32:32d27c728ea93203236757d7534b6e68  /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/sgl_kernel/sm100/common_ops.abi3.so
/user_4813494d/openbmb/docs/marlin-tuning.md:33:32d27c728ea93203236757d7534b6e68  /user_4813494d/openbmb/demo-sala/common_ops.abi3.so
/user_4813494d/openbmb/docs/marlin-tuning.md:40:- 78MB 的 `common_ops.abi3.so.bak` 涉及旧 cu12/旧打包，不适合直接当公平性能 baseline；若要测 B0，应从明确的 old Marlin 源码/patch 点重新 build 一个 cu13 `.so`。
/user_4813494d/openbmb/docs/marlin-tuning.md:76:77a3a9fb3aad222714a43ede4776596d  /user_4813494d/openbmb/outputs/marlin_b0_20260425_101153/common_ops.old_marlin_cu13.abi3.so
/user_4813494d/openbmb/docs/marlin-tuning.md:122:77a3a9fb3aad222714a43ede4776596d  /user_4813494d/openbmb/outputs/marlin_b0_20260425_101153/common_ops.old_marlin_cu13.abi3.so
/user_4813494d/openbmb/docs/marlin-tuning.md:606:- `probe-sala/common_ops.abi3.so`（`220c18cc`）是目前唯一被验证可以正常 EAGLE 起服的 `.so`。
/user_4813494d/openbmb/docs/marlin-tuning.md:611:- 当前生产部署必须使用 `220c18cc`。`demo-sala/common_ops.abi3.so` 已替换为 `220c18cc`。
/user_4813494d/openbmb/docs/cuda13-upgrade.md:28:| sgl-kernel | 0.3.20（pyproject 锁）| engine.py:794 真会断言；但 `common_ops.abi3.so` 被 demo-sala 覆写（prepare_env.sh:34）|
/user_4813494d/openbmb/docs/cuda13-upgrade.md:30:| CUDA toolkit | 12.9（RUNPATH 内嵌）| `common_ops.abi3.so` 编译时链的是 cu12.9 |
/user_4813494d/openbmb/docs/cuda13-upgrade.md:43:### 3.1 `demo-sala/common_ops.abi3.so`（78 MB，2026-03-31 编译）
/user_4813494d/openbmb/docs/cuda13-upgrade.md:49:**重编路径**：sgl-kernel 源（GitHub sgl-project/sglang，csrc/gemm/marlin/）+ `demo-sala/patches/marlin_fp4_scale.patch`（57 行，修 FP4 kFE2M1f scale stride bug）→ cmake + ninja。
/user_4813494d/openbmb/docs/cuda13-upgrade.md:112:这些在 `common_ops.abi3.so` 里，重编 .so 就解决。
/user_4813494d/openbmb/docs/cuda13-upgrade.md:133:| `demo-sala/prepare_env.sh` | 32 | `common_ops.abi3.so` 路径仍叫 `sm100/common_ops.abi3.so`（这是 sgl-kernel 内部包目录名，与 arch 无关，不改）|
/user_4813494d/openbmb/docs/cuda13-upgrade.md:182:- ✅ `/user_4813494d/backups/cu12-baseline-20260420/`：venv 11G + cuda-12.9 toolkit 7.3G + packages + flashinfer-cache + common_ops.abi3.so + sparse_kernel_extension.so + `RESTORE.sh`
/user_4813494d/openbmb/docs/cuda13-upgrade.md:200:| **2.4** | sgl-kernel `common_ops_sm100_build` 精准重编 | ✅ **优化**：绕过 `uv pip install`，CMake + Ninja 只 build `common_ops_sm100_build`（跳过 sm90 variant / FA3 flash_ops / flashmla_ops / spatial_ops / deep_gemm_cpp，MiniCPM 路径不用）。产出 `sm100/common_ops.abi3.so` 25MB（cu12 版 78MB，单 sm_120a gencode + `--compress-mode=size`）。依赖全走 `/user_4813494d/deps/` 本地 override（8 FetchContent + FlashMLA + 5 submodule），mscclpp python bindings `OFF` 跳过 nanobind/dlpack clone |
/user_4813494d/openbmb/docs/cuda13-upgrade.md:204:**`common_ops_sm100_build` 内含 sm_120a fatbin**：CMakeLists:226 `-gencode=arch=compute_120a,code=sm_120a`；`load_utils.py:63-69` 按 cc 分派（`cc==90→sm90/`，其他→`sm100/`），sm100 目录命名 ≠ sm100 arch 限制。
```

> TOOL

tool_use Bash
```json
{
  "command": "git show 9225f46 --format=\"%B\" | head -30",
  "description": "intermediate_ssm direct-write commit"
}
```

> TOOL

tool_result Bash
```
feat: intermediate_ssm direct-write + fused sparse metadata + profiling framework

工作树积累的 EAGLE-3 / FlashInfer 稀疏路径优化一并落盘。核心是 3 个运行时
改动 + 1 套 profiling 基建，docs 同步重组。

核心优化
---------

1. intermediate_ssm 直写（hybrid_linear_attn_backend.py, Phase 3.2.1）
   - GLA kernel 输出布局从 (N*H, T, K, V) 改为 (N, T, H, K, V)，独立 stride
     (ht_stride_n + ht_stride_h)，消除 view + permute(0,2,1,3,4) 中转
   - ht_buf 直接 alias 到 intermediate_ssm[cache_idx, :bs, :dtn] slice，
     kernel 写入即终态
   - direct_copy 39.5ms → 0.4ms（-99%），profile wall -8.9%（bs=4）
   - extend 路径用 extend_prefix_lens_cpu 镜像判断，消掉 per-layer GPU sync

2. Fused sparse metadata copy（minicpm_backend.py）
   - k1/k2 共 16 个 metadata 字段从 16 个独立 GPU tensor + 16 次 .copy_()
     合并成 1 个 fused GPU buffer + 配对 pinned-memory CPU buffer + offset 字典
   - 单次 pinned H2D 搬运替代 16 次 per-field copy
   - A/B 开关：SGLANG_MINICPM_DISABLE_FUSED_META_COPY=1 退回原 per-field 路径
   - _sparse_meta_field_specs 表驱动，replay_prepare 按 spec 统一 scatter

3. using_preconverted FlashInfer 稀疏转换（minicpm_attention_kernels.py）
   - 上游（backend replay）已预转换 sparse_page_table → kv_indptr/indices 时，
     FlashInferKernel 跳过重复转换
   - 原 wrapper._paged_kv_* 路径保留为 fallback
   - 修注释所指 head-group split bug（forward_decode 先做 head_num//2 切分，
     这里不能再用 self.num_qo_heads / num_kv_heads，改成从 q.shape / k_cache.shape
     取实际 per-sequence head counts）
```

> TOOL

tool_use Bash
```json
{
  "command": "git log --oneline --all | grep -i \"FP4.*scale\\|scale.*patch\\|marlin.*patch\\|sgl-kernel\" | head -10",
  "description": "Search for Marlin FP4 scale bug patch commits"
}
```

> TOOL

tool_result Bash
```
f7faed5 fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards
2b36ae2 fix: EAGLE-3 fused NVFP4 auxiliary scale loader — broadcast scalar to all shards
6cd79ae feat: hybrid Marlin/CUTLASS dispatch + 45K quant + submission cleanup
f2e843d feat: hybrid Marlin/CUTLASS dispatch + 45K quant + submission cleanup
99e195e feat: NVFP4 Marlin fallback path + sgl-kernel rebuild pipeline + probe-sala
ae7c1d6 feat: NVFP4 Marlin fallback path + sgl-kernel rebuild pipeline + probe-sala
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -name \"marlin_fp4_scale.patch\" -o -name \"*fp4*scale*patch*\" 2>/dev/null | head -5",
  "description": "Find the FP4 scale patch file"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -name \"*.patch\" 2>/dev/null | head -10",
  "description": "Find patch files"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -path \"*/patches/*\" -type f 2>/dev/null | head -10",
  "description": "Find files in patches directory"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/probe-sala/patches/gptq_quantize_fouroversix.py
/user_4813494d/openbmb/demo-sala/patches/gptq_quantize_fouroversix.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/patches/gptq_quantize_fouroversix.py",
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	import math
2	import os
3	from copy import copy
4	
5	import torch
6	import transformers
7	from compressed_tensors.quantization import (
8	    ActivationOrdering,
9	    QuantizationArgs,
10	    QuantizationStrategy,
11	    QuantizationType,
12	    fake_quantize,
13	)
14	from compressed_tensors.quantization.quant_args import FP4_E2M1_DATA
15	from compressed_tensors.utils import update_offload_parameter
16	from loguru import logger
17	
18	from llmcompressor.modifiers.utils import SPARSITY_THRESHOLD
19	from llmcompressor.observers.base import Observer
20	from llmcompressor.pytorch.utils.helpers import tensor_sparsity
21	
22	GPTQ_PRECISION = torch.float32
23	FOUROVERSIX_ENABLED = os.environ.get("FOUROVERSIX", "1") == "1"
24	
25	__all__ = ["make_empty_hessian", "accumulate_hessian", "quantize_weight"]
26	
27	
28	def _fouroversix_scale_select(
29	    W: torch.Tensor,
30	    scale: torch.Tensor,
31	    quant_args: QuantizationArgs,
32	    global_scale: torch.Tensor,
33	) -> torch.Tensor:
34	    """
35	    Four Over Six adaptive block scale selection (arXiv:2512.02010).
36	
37	    For each group of weights, compare MSE with scale=6 (standard NVFP4)
38	    vs scale=4 (scale * 1.5). Pick whichever gives lower reconstruction
39	    error, accounting for FP8 scale quantization.
40	
41	    Called after observer computes standard scale=6, before GPTQ loop.
42	    GPTQ then optimizes rounding for the selected scale per group.
43	    """
44	    group_size = quant_args.group_size
45	    num_rows, num_cols = W.shape
46	
47	    if num_cols % group_size != 0:
48	        return scale
49	
50	    num_groups = num_cols // group_size
51	
52	    # Reshape weights into groups: [rows, groups, group_size]
53	    W_groups = W.reshape(num_rows, num_groups, group_size)
54	
55	    # Current scale=6 (already global_scale * amax/6, FP8-rounded)
56	    scale_6 = scale  # [rows, groups], dtype=float8_e4m3fn or float32
57	
58	    # Alternative scale=4: multiply by 1.5, re-round to FP8
59	    scale_4_f32 = scale_6.float() * 1.5
60	    scale_4 = scale_4_f32.to(torch.float8_e4m3fn)
61	
62	    # Effective per-group scale (undo global_scale)
63	    gs = global_scale.float()
64	    eff_6 = scale_6.float() / gs  # [rows, groups]
65	    eff_4 = scale_4.float() / gs
66	
67	    # Fake-quantize with scale=6
68	    scaled_6 = W_groups / eff_6.unsqueeze(-1)
69	    q_6 = FP4_E2M1_DATA.cast_to_fp4(scaled_6.clamp(-6.0, 6.0).clone())
70	    deq_6 = q_6 * eff_6.unsqueeze(-1)
71	    mse_6 = ((W_groups - deq_6) ** 2).sum(dim=-1)
72	
73	    # Fake-quantize with scale=4
74	    scaled_4 = W_groups / eff_4.unsqueeze(-1)
75	    q_4 = FP4_E2M1_DATA.cast_to_fp4(scaled_4.clamp(-6.0, 6.0).clone())
76	    deq_4 = q_4 * eff_4.unsqueeze(-1)
77	    mse_4 = ((W_groups - deq_4) ** 2).sum(dim=-1)
78	
79	    # Per-group selection (torch.where doesn't support FP8 promotion, work in float32)
80	    use_4 = mse_4 < mse_6
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/b12x -type f 2>/dev/null",
  "description": "List b12x kernel files"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/b12x/__init__.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/b12x/cute_dsl_utils.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/quantization/b12x/dense_blockscaled_gemm_sm120.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/patches/gptq_quantize_fouroversix.py",
  "limit": 30,
  "offset": 80
}
```

> TOOL

tool_result Read
```
80	    use_4 = mse_4 < mse_6
81	    new_scale = torch.where(use_4, scale_4.float(), scale_6.float()).to(scale.dtype)
82	
83	    pct = use_4.float().mean().item() * 100
84	    improved = (mse_6[use_4] - mse_4[use_4]).sum().item() if use_4.any() else 0
85	    logger.info(
86	        f"FourOverSix: {pct:.1f}% blocks selected scale=4 "
87	        f"(MSE reduction: {improved:.6f})"
88	    )
89	
90	    return new_scale
91	
92	
93	def make_empty_hessian(
94	    module: torch.nn.Module, device: torch.device | None = None
95	) -> torch.Tensor:
96	    weight = module.weight
97	    num_columns = weight.shape[1]
98	    device = device if device is not None else weight.device
99	    return torch.zeros((num_columns, num_columns), device=device, dtype=GPTQ_PRECISION)
100	
101	
102	def accumulate_hessian(
103	    inp: torch.Tensor,
104	    module: torch.nn.Module,
105	    H: torch.Tensor | None,
106	    num_samples: torch.Tensor,
107	) -> tuple[torch.Tensor, torch.Tensor]:
108	    inp = inp.to(device=H.device)
109	    if len(inp.shape) == 2:
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/cuda13-upgrade.md",
  "limit": 60
}
```

> TOOL

tool_result Read
```
1	# CUDA 12.8 → CUDA 13 升级调研
2	
3	本文档是基于对 `demo-sala/` 和 `demo-sala/sglang/` 源码的**亲自深入阅读**得出的升级可行性结论。不是二手总结。
4	
5	调研日期：2026-04-20。
6	
7	---
8	
9	## 1. 结论先行
10	
11	**无硬卡点，所有候选阻塞项都有源码/重编路径可解。**
12	
13	**主要收益窗口**：SM120 Blackwell 在 CUDA 13 + `compute_120f` 下的 CUTLASS NVFP4 GEMM 路径（cutlass#3096 实测 2.7× decode，M>48 prefill 预期 ≥20%）。
14	
15	**主要风险**：
16	1. tilelang 0.1.8（JIT 编译 sparse prefill kernel）在 cu13 Blackwell 下未经验证
17	2. FlashInfer wrapper 内部私有字段 `_paged_kv_indptr_buf` 等被我们直接访问，版本间重命名会崩
18	3. 量化流程 (`prepare_model.sh`) 在 cu13 + nvidia-modelopt 新版下需精度回归
19	
20	---
21	
22	## 2. 当前栈真相（而非 pyproject.toml 表面）
23	
24	| 层 | 真实运行版本 | 备注 |
25	|---|---|---|
26	| torch | 2.9.1+cu128 | `prepare_env.sh` 不重装 torch，继承平台 |
27	| flashinfer | **>=0.6.7**（prepare_env.sh:20 主动升级）| pyproject.toml 锁 0.5.3 是**假锁**，被 `uv pip install --no-deps -e` 绕过 |
28	| sgl-kernel | 0.3.20（pyproject 锁）| engine.py:794 真会断言；但 `common_ops.abi3.so` 被 demo-sala 覆写（prepare_env.sh:34）|
29	| cuDNN | >=9.15.0（主动升）| `nvidia-cudnn-cu12>=9.15.0` |
30	| CUDA toolkit | 12.9（RUNPATH 内嵌）| `common_ops.abi3.so` 编译时链的是 cu12.9 |
31	| tilelang | 0.1.8 | JIT 编译，跟随系统 nvcc |
32	| fla | 0.4.1 | flash-linear-attention，纯 Triton |
33	| sparse_kernel_extension | 0.0.0（`/opt/.../packages/sparse_kernel/`）| 有源码 `get_table_kernel.cu`，可重编 |
34	| nvidia-modelopt | 0.42.0 | `prepare_env.sh:13` |
35	| llmcompressor | [REDACTED] | 打了自定义 patch `gptq_quantize_fouroversix.py` |
36	
37	**engine.py 版本检查只在 `attention_backend == "flashinfer"` 时触发**（line 783）。我们用的是 `minicpm_flashinfer`，**flashinfer==0.5.3 这条断言永远不执行**。sgl-kernel==0.3.20 的断言（line 791）会触发，必须保留版本号。
38	
39	---
40	
41	## 3. 二进制依赖清单（cu13 下必须重编）
42	
43	### 3.1 `demo-sala/common_ops.abi3.so`（78 MB，2026-03-31 编译）
44	
45	- `ldd` 显示硬链 `libcudart.so.12`, `libcublas.so.12`, `libcublasLt.so.12`
46	- `RUNPATH`: `/usr/local/cuda-12.9/targets/x86_64-linux/lib` → 编译时的 cu12.9
47	- 598 个导出符号，涵盖 Marlin FP4 (`marlin_moe_wna16`), `gptq_shuffle`, `scaled_fp4_quant`, `top_k_renorm_prob`, `tree_speculative_sampling_target_only`, `verify_tree_greedy`, `segment_packbits` 等
48	
49	**重编路径**：sgl-kernel 源（GitHub sgl-project/sglang，csrc/gemm/marlin/）+ `demo-sala/patches/marlin_fp4_scale.patch`（57 行，修 FP4 kFE2M1f scale stride bug）→ cmake + ninja。
50	
51	**编译必须带**：`TORCH_CUDA_ARCH_LIST=12.0f`（**注意是 `120f` 不是 `120a`**，vllm#36865 陷阱：不写就套用非-SM120 Marlin 模板掉速）。
52	
53	### 3.2 `sparse_kernel_extension.so`
54	
55	- 硬链 libcudart.so.12
56	- **源码在** `/opt/SGLang-MiniCPM-SALA/packages/sparse_kernel/get_table_kernel.cu`，有 `setup.py`
57	- 被 `minicpm_backend.py:28, 1121, 1378` 用，提供 `get_block_table_v2/v3`
58	- cu13 下 `cd packages/sparse_kernel && python setup.py install` 即可
59	
60	### 3.3 FlashInfer JIT 缓存
```

> AGENT

---

# EAGLE-3 Speculative Decoding 技术全貌 -- 详细摘要

以下是对 SOAR 2026 比赛中 MiniCPM-SALA 模型 EAGLE-3 投机解码全部技术工作的系统性总结，涵盖所有文档和核心实现。

---

## 一、架构概览

**生产配置**: `spec_steps=3, topk=2, dtn=7`, `rope_theta=1000000`, `EAGLE_MARS_THETA=0.85`

**Eagle3Model** (~437M trainable):
- `fc`: Linear(12288 -> 4096), 融合 3 层 aux hidden
- `midlayer`: Eagle3DecoderLayer (1 层完整 decoder)
  - `self_attn`: Eagle3Attention (GQA 32h/2kv), Q/K input = cat(normed_embed, normed_hidden)
  - `mlp`: SwiGLU (4096 -> 16384 -> 4096)
- `embed_tokens`: Embedding(73448, 4096) [FROZEN]
- `lm_head`: Linear(4096 -> 32000), 32K draft 词表 (覆盖率 99.23%)

**推理性能**: Draft ~0.50 ms/step (Marlin FP4); d2t 映射 draft->full vocab, hot_token_id 覆盖 32000/73448 = 43.6%

---

## 二、Fused GLA Kernel -- 技术细节与性能

**问题**: 原始路径需 24 层 GLA x dtn 步 = 72 次 kernel launch。

**优化方案**: 24 层 x 1 次 launch, 处理 T=dtn 并导出全部中间 state。

**性能数字**:
- **7.63x 加速** (microbench: 5.51 ms -> 0.72 ms)
- cos_sim = 1.0, 数值等价

**intermediate_ssm 直写**:
- 原: `ht_buf(N*H,T,K,V) -> permute -> intermediate_ssm.copy` (1848 call x 21us = 39.5 ms)
- 新: Triton kernel 直写 `intermediate_ssm[cache_idx,:B,:dtn]`
- 结果: 0.4 ms (**-99%**), cos = 1.000000, max_abs = 4.5e-8

**核心 Triton kernel**: `_fused_recurrent_gla_intermediate_kernel` (文件: `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py` 行 56-155)
- GLA 递推: `h_t = exp(-gamma) * h_{t-1} + k_t * v_t^T`
- 每 step 存 intermediate state 到 `ht_all` (形状 `(N, T_per_seq, H, K, V)`)
- 支持 `retrieve_parent_token` 实现树感知状态传播 (等效于 STree 的 A-matrix 累乘)

---

## 三、MARS Verify -- 机制与 Theta 参数

**论文**: arXiv:2601.15498 (ICLR 2026)

**核心算法**: 对每个 draft token v_t:
1. **Exact Match**: `v_t == top-1` -> 直接接受
2. **Adaptive Relaxation**: `v_t == top-2` 且 `r_t = z_(2)/z_(1) > theta` -> 接受(视为 tie)
3. 否则拒绝

**theta 参数的作用**:
- `r_t` = target top-2 logit / top-1 logit (logit ratio)
- 当 `r_t > theta` 时, 表示 top-1 和 top-2 的 logit 值非常接近(target 自身也在"犹豫"), 此时接受 top-2 token 的信息损失可忽略
- theta 越低, 放宽程度越大, 接受率越高, 但质量风险也越高

**论文数据** (theta=0.90):
- Vicuna-13B: 3.12x -> 3.74x (+27.7% tau)
- Llama-3.1-8B: 3.24x -> 4.00x (+37.2% tau)
- theta < 0.88 开始有可测量质量退化

**本机实测**: theta=0.85 (比论文推荐更激进)
- 吞吐可观测提升, eval 分数无可观测下降
- 推测原因: NVFP4 量化后 logit ratio 分布更集中, theta=0.85 在该模型上仍处于安全区间
- **当前生产值**: `EAGLE_MARS_THETA=0.85`

**实现** (关键文件):
- `sgl-kernel/csrc/speculative/eagle_utils.cu`: `VerifyTreeGreedy` kernel 8->11 参数, 先 exact match 后 MARS fallback
- `eagle_info.py` 行 347-384: 计算 `top2_ratio = z2/z1`, 传入 CUDA kernel
- CUDA kernel 内逻辑: 先扫 exact match, fallback 到 MARS (draft_token == top2_token && top2_ratio > mars_theta)

---

## 四、rope_theta=1M -- 效果与原理

**原理**:
- RoPE theta=10000 在 130K 位置外推比约 64x, sin/cos phase 周期折叠, draft attention 对长距 token pair 的 score 退化
- rope_theta=1M 将 period 延伸, phase 在 130K 内不折叠
- 依据 YaRN (ICLR 2024) NTK 插值公式: s=64 时 theta 有效值需 ~700K; 1M 覆盖此范围

**实测效果** (全量 64 样本, concurrency=64):

| 分组 | n | al_10k | al_1M | delta |
|---|---|---|---|---|
| 长 context (p_tok>50K) | 31 | 1.395 | 2.022 | **+0.627 (+44.9%)** |
| 短/中 context (p_tok<=50K) | 33 | 1.972 | 2.072 | +0.100 (+5.1%) |

长 deepresearch 样本:
- idx 32: al 1.363 -> 2.174 (lat -1.51s)
- idx 33: al 1.309 -> 2.331 (lat -2.63s)
- idx 62: al 1.253 -> 2.205 (lat -1.36s)

短 coding 反向:
- idx 1 (157 tok): al 2.356 -> 1.425 (lat +10.83s), 但不影响 benchmark critical path

**落地状态**: `config.json` 中 `"rope_theta": 1000000` 已写入, 无需重训

---

## 五、Tree-aware dtn5 Verify -- 解决什么问题

**问题**: GLA 递推 `h_t = exp(-gamma)*h_{t-1} + k_t*v_t^T`。topk>1 时 flat verify `[user_4813494d, c1, c2]` 导致 c2 继承 c1 state(应从 user_4813494d 分叉) -> sibling 污染。

**Plan A (per-branch 扁平)**: 重排为 `[user_4813494d, c1, user_4813494d, c2]` 做 2 个 varlen seq。数值正确(cos 0.996->0.9999999), 但 FP32 4D `index_select` 引入 205 ms/cycle 热点, **净 ROI 负**, 已回滚。

**Tree-aware dtn5 verify (commit 8017c1d)**: 
- `hybrid_linear_attn_backend.py` + `eagle_worker.py` + `eagle_info.py` 联合改造
- Triton kernel `_fused_recurrent_gla_intermediate_kernel` 内通过 `retrieve_parent_token` 实现树拓扑状态传播
- `_build_retrieve_parent_token()` 函数 (hybrid_linear_attn_backend.py 行 250+) 从 `retrieve_next_token` / `retrieve_next_sibling` 构建 parent 索引矩阵
- kernel 内: 每步加载 `parent_idx_tokens = tl.load(retrieve_parent_token_base)`, 从正确的 parent state 恢复, 而非从线性前一步
- 这等效于 STree 的 A-matrix 累乘方案, 但在单次 kernel launch 内完成

**结果**: sibling 隔离正确, 已落地稳定, `tests/test_simple_gla_tree_verify.py` 回归通过

---

## 六、Dynamic Spec Mode (NO_SPEC/D5/D7)

**设计动机**: 不同 batch size 下 spec decode 效率不同:
- 大 batch (bs>=31): spec 净负收益(verify overhead > draft 加速)
- 中 batch: D5 (dtn=5) 是 sweet spot
- 小 batch (bs<=1): D7 (dtn=7) 更激进, 单请求吞吐最大化

**三种模式** (文件: `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/spec_mode.py`):

| 模式 | 条件 | topk | steps | dtn | 默认 MARS theta |
|---|---|---|---|---|---|
| NO_SPEC | bs >= 31 | - | - | - | - |
| MARS_D5 | 默认 | 2 | 2 | 5 | 继承全局 |
| MARS_D7 | bs <= 1 | 2 | 3 | 7 | 继承全局(可独立设) |

**迟滞设计**: enter/leave 阈值分开, 防止 prefill burst 翻转
- NO_SPEC: enter_bs=31, leave_bs=28
- D7: enter_bs=1, leave_bs=3
- Bench 流量 bs 单调递减, 路径实质上是单向: NO_SPEC -> D5 -> D7

**env 控制**:
- `EAGLE_DYNAMIC_MODE=1` 启用
- `EAGLE_NO_SPEC_BS=31`, `EAGLE_D7_BS=1`
- `EAGLE_D5_MARS_THETA`, `EAGLE_D7_MARS_THETA` 独立设置每模式 theta

**实现** (文件: `eagle_worker.py`):
- `_apply_spec_config(mode)`: 运行时切换 topk/steps/dtn/ cuda_graph_runner/mars_theta
- `_forward_no_spec(batch)`: 直接 target decode, 跳过 draft/verify, 但仍推进 draft KV 以避免冷启动
- 稳态 D5->D5 / D7->D7 快路径 early-return, 避免重复参数绑定
- `torch._dynamo.config.recompile_limit = 32` 防止多模式多 capture_bs 下 dynamo 放弃编译

**4 项热路径加速** (commit 87a8bb1):
1. NO_SPEC lazy draft KV catch-up: 不再每步 [REDACTED], 而是暂存 pending, 回 D5/D7 时一次性 multi-token flush
2. `_apply_spec_config` early-return: D5->D5 快路径 ~0.2 us/step
3. FlashInfer verify plan() CPU 输入: 消除 3 次 D2H sync (~26 us)
4. `_alloc_sparse_for_new_positions` bulk plan: bs=32 时 3.7ms -> 60us (62x)

---

## 七、训练 v2 -> v3 关键改进

### v2 (2026-04-18, 已部署生产)

**数据重构**: 从 SkyPile/code_search_net/wikitext (与线上 mismatch) 换为:
- Chinese-DeepSeek-R1-Distill-110k 60%, stem_zh 22%, OpenCodeReasoning 11.5%, codeforces 5.5%, dolphin-r1 1%
- 20,000 样本 x 2048 tok

**训练管线优化 -39% wall clock**:
- GRAD_CHECKPOINT: True -> False (bwd 286->185ms, peak mem 11->28GB)
- BS=2/4 -> BS=8/1 (effective batch 保持 8)
- AsyncPrefetcher: disk I/O 完全被 GPU 覆盖

**关键修复**: 
- Shifted Alignment: 修复后 OOD accept rate 8.2% -> 35.5%
- RoPE 对齐: 训练加 `_build_rope_cache(theta=10000.0)`
- eval_ood 改为 step-0 only + 全长 (old weighted_acc=0.5255 -> new step-0 acc=0.6607)
- 超参: MAX_GRAD_NORM 5.0->1.0, WARMUP 500->1500

### v3 (2026-04-24, 训练完成但未部署)

**1. Probe 选层 [1,10,22] -> [4,9,24]**
- Phase 2: 每层单独训 linear probe -> NLL 排序
- Phase 3: greedy triple search
- CE: 6.51 -> 4.61 (**-29%**)
- 关键发现: 深层(24)最强(single CE=4.92), 第一层从 1->4 跳过早期 embed 噪声

**2. NVFP4 存储**
- aux_hidden bf16 -> NVFP4 group=16 (与生产 fc layer W4A4 精度对齐)
- 压缩比 ~2.8x (48 MB bf16 -> 17.3 MB)
- step-0 acc: 0.1139 -> **0.1186 (+0.47%)** (NVFP4 反而略好, 因 train/serve 精度对齐)
- 文件: `eagle/nvfp4_codec.py`

**3. 数据规模 20K -> 200K**
- BOS 云训管线: 148K 已上传, 52K 待补采
- 采集: `collect_async.py` (aiohttp 32并发 + ThreadPool 8 压缩 + bcecmd BOS 上传)

**v3 未部署原因**: 在 long deepresearch 上 **比 v2 更差** (idx 17 pre-EOS al=0.578 vs v2 0.737, collapse 更频), v3 的 NLL -29% 不对应 long deepresearch workload

---

## 八、Collapse 分析 -- 具体发现

**根因**: pre-EOS 长生成中 49% verify step `accept_len==0`。纯 draft 能力问题 + 少量 d2t 覆盖缺陷。**与 backend/KV pool/cuda graph 无关**。

**关键数字** (idx 17, pre-EOS 133 步):
- al==0: 65/133 (48.9%), al==1: 38, al==2: 30
- 最长连续 al==0: 10 步 (step 75-84)
- al=0 段 logit gap p50=2.75 vs 健康段 5.06

**d2t 结构 miss** (Smax=64 全量):
- miss = 42,110/416,207 = 10.12%
- `<unk>` (id=0): 37,551 = 89.2% of miss
- `<|im_end|>` (id=73440): 578 = 1.4% of miss
- 剔除结构 miss 后 adj_al: 1.865 -> 2.298 (**+23%**)

**80-token probe 误导**: 80 token 内 al=1.74, 但只覆盖 step 0-59, 错过 step 60+ collapse 段 (al=0.737)。之前所有基于 80-token 的优化方向均偏差。

**连续 collapse 机制**:
1. 单次翻转把 prefix 推入 draft 训练分布的"连续盲区"
2. 连续多个位置 draft top-2 都漏 target argmax
3. 直到 target commit 到语义边界(标点/模板短语), prefix 重新落入 draft 熟悉分布, accept 恢复

**v3 反效果**: aux=[4,9,24], 200K 数据, NLL -29% -- 但 long-gen collapse 反而比 v2 更频 (al=0.578 vs 0.737)

**batch drift**: concurrency>=2 时, output 第 8 个 generated token 就分歧。**nospec 自己也有** (与 spec/draft 完全无关), 是 sglang/flashinfer multi-batch 路径的 GPU kernel 数值非确定性。

**与 prompt 长度的关系**: al 与 prompt 长度单调反相关 (short al~1.86-2.42, vlong al~1.38), 但 **与 prompt 内容(训练分布覆盖度)强相关**。编程类 adj_al=2.3-2.8, 长文本 deepresearch adj_al=1.24-1.30。

---

## 九、五条独立长上下文根因 (学术综述)

1. **RoPE 位置外推失效**: theta=10000 在 130K 处外推 64x, phase 周期折叠 (LongSpec ACL 2025, YaRN ICLR 2024)
2. **训练位置分布偏斜**: 短序列过度训练, 大位置覆盖极少 (LongSpec 提出 AOI: Anchor-Offset Indices)
3. **Target Hidden State 分布漂移**: attention sink + InfLLM-v2 sparse 放大 feature 偏移 (OWL EMNLP 2025)
4. **InfLLM-v2 Sparse / Draft Dense 注意力不对称**: 8 层 standard attention >8192 走 sparse, draft 全量 dense (QuantSpec)
5. **Draft 训练数据领域覆盖不足**: 纯训练分布盲区 (v3 200K 数据也未解决)

---

## 十、SGLang 适配 (4+5 关键修复)

**v1 路径** (commit 8bc05a3):
1. GLA state rollback: 用 `mambaish_config` 统一判断
2. Sparse k1/k2 slot 分配: `_alloc_sparse_for_new_positions()`
3. Draft 配置隔离: 量化置 None + attention backend 从 minicpm_flashinfer -> flashinfer
4. KV cache slot 释放时序: verify() 开头释放 draft slots

**v2 额外修复** (spec-v2 overlap 路径):
5. future_indices record_stream (等价 upstream PR #18958)
6. sparse 回收改为"按真实写入边界回收"
7. unfinished-only future relay
8. Fused NVFP4 Scale Loader 修复: `load_fused_per_tensor_weight()` 标量广播到所有 shard (6 种配置零 NaN)

---

## 十一、已确认的候选优化方向 (优先级排序)

| # | 方向 | 状态 | 收益 |
|---|---|---|---|
| - | rope_theta=1M | **已落地** | vlong adj_al +44.9% |
| - | MARS theta=0.85 | **已部署** | 吞吐提升, eval 无退化 |
| - | dynamic spec mode | **已部署** | 大 bs 避免负收益, 小 bs 激进 dtn |
| 1 | Phased Verify | 离线分析完成 | vlong early-exit 68.3%, -28.6% verify token |
| 2 | BanditSpec | 未实施 | per-req UCB 自适应 dtn, est +20-35% |
| 3 | GOOSE | 未实施 | 各向异性树, +12-33% vs balanced tree |
| 4 | RACER | 未实施 | AC 自动机 n-gram retrieval, MAT +0.5-0.76 |
| backlog | DFlash | 下一代候选 | block diffusion 一次 forward 16 token |

**已淘汰**: SMART (batch=1 无收益), Cactus (T=0 退化为 exact-match), STree 并行 GLA (bottleneck 不在 GLA state), Plan A per-branch 扁平 (FP32 index_select 净负)

---

## 十二、关键文件索引

| 文件 | 作用 |
|---|---|
| `/user_4813494d/openbmb/docs/eagle/README.md` | 架构总览 + 全局状态 |
| `/user_4813494d/openbmb/docs/eagle/collapse-analysis.md` | collapse 根因实证 |
| `/user_4813494d/openbmb/docs/eagle/experiments-log.md` | rope_theta/MARS/Phased Verify 实测数据 |
| `/user_4813494d/openbmb/docs/eagle/training-v2.md` | v2 训练改进 |
| `/user_4813494d/openbmb/docs/eagle/training-v3.md` | v3 probe 选层 + NVFP4 存储 |
| `/user_4813494d/openbmb/docs/eagle/spec-survey.md` | 50+ 篇论文系统综述 |
| `/user_4813494d/openbmb/docs/eagle/longcontext-analysis.md` | 五条长上下文根因 |
| `/user_4813494d/openbmb/docs/eagle/spec-v2.md` | spec v2 overlap 适配 |
| `/user_4813494d/openbmb/docs/eagle/dflash.md` | 下一代 DFlash 候选 |
| `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py` | verify + draft + dynamic mode + NO_SPEC |
| `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py` | verify 逻辑 + MARS + tree 构造 |
| `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/spec_mode.py` | NO_SPEC/D5/D7 模式定义 + selector |
| `/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/layers/attention/hybrid_linear_attn_backend.py` | GLA fused kernel + tree-aware verify + intermediate_ssm |

> AGENT

我现在对所有技术细节有了透彻的理解。接下来，我将整理并呈现全面的摘要。

---

## 量化与 Kernel 技术工作深度摘要

### 一、NVFP4 量化方案

**算法**: GPTQ + FourOverSix (自适应 4/6 block scale)，`lm_head` Identity patch。校准使用 wikitext loguniform 128 samples，8 buckets（512-64K log-uniform），max_length=48K。推理要求 `--dense-as-sparse`（dense_len=0，全序列走 sparse TopK 路径）。

**校准实验结果**:

| Config | Calibration | max_length | FourOverSix | dense-as-sparse | ori_accuracy |
|---|---|---|---|---|---|
| baseline | calib90 | 24K | off | on | 80.27%（不稳定） |
| **chosen** | **loguniform 128** | **48K** | **on** | **on** | **79.98%** |
| exp | loguniform 128 | 48K | on | off | 78.18% |
| exp | calib90 | 72K | on | on | 77.04% |

**健康检查警告**: NVFP4 量化后模型在 mcq 强格式约束下会退化为重复 pattern，但 eval regex 仍命中，ori_accuracy 看似正常实则生成垃圾。健康检查必须用 chat 长样本，不用 mcq。

---

### 二、FourOverSix (4/6) 量化方案

**来源**: MIT-HAN Lab 方案 (arXiv:2512.02010)。

**原理**: 标准 NVFP4 固定 block scale/6；FourOverSix 对每个 block 比较 scale=4 和 scale=6 的 MSE，选更小者。输出格式不变（4-bit FP4 权重 + FP8 block scales），zero throughput impact。

**核心算法**:
```python
scale_4 = fp8(scale_6.float() * 1.5)    # scale=4: 权重映射到 [-4, 4]
mse_6 = sum((W_group - dequant(W_group, scale_6))^2)
mse_4 = sum((W_group - dequant(W_group, scale_4))^2)
new_scale = where(mse_4 < mse_6, scale_4, scale_6)
```

**实测**: 40-43% 的 blocks 选 scale=4；MLP 层比 Attention 层获益更大。

**集成**: 直接 patch `llmcompressor/modifiers/quantization/gptq/gptq_quantize.py`，在 observer 输出 scale 后、GPTQ 优化循环前插入 scale 选择。通过 `FOUROVERSIX` 环境变量控制（默认 `"1"`）。代码位于 `/user_4813494d/openbmb/demo-sala/patches/gptq_quantize_fouroversix.py`。

---

### 三、Marlin FP4 Scale Bug Fix

**问题**: 平台 sgl-kernel 0.3.20 的 `marlin_template.h` 有 FP4 scale `/2` bug，导致 Marlin FP4 输出的 cos_sim 仅为 0.77。

**修复**: Pre-built `common_ops.abi3.so`（SM120a）via `cp` 替换。修复后 cos_sim 0.77 -> 1.0。重编路径使用 sgl-kernel 源码 + `demo-sala/patches/marlin_fp4_scale.patch`（57 行），编译必须带 `TORCH_CUDA_ARCH_LIST=12.0f`（不是 `120a`，vllm#36865 陷阱）。

**当前部署的 `.so` md5**: `32d27c728ea93203236757d7534b6e68`（含 small-M atomic + shape-aware tile 改进，但**EAGLE draft CUDA graph capture 不兼容**）。

**EAGLE 不兼容问题**: `32d27c7` 比 probe-sala 的 `220c18cc` 大 562 KB，会导致 EAGLE-3 draft CUDA graph capture 挂住（37% 进度卡死）。根因是 small-M atomic/tile 行为和 CUDA graph capture 有不明冲突。当前生产必须用 `220c18cc`（probe-sala 版本）。Marlin 3% 的 e2e 收益在 EAGLE 生产路径下不可用。

---

### 四、Scale Loader Bug（QKV Fused Per-Tensor Scale 污染）

**完整故事**:

**根因**: `QKVParallelLinear` 和 `MergedColumnParallelLinear` 在加载 fused per-tensor scales（`weight_scale_2`, `input_scale`）时，只写入了 `shard_id=0`，其余 slot 保留为 `torch.empty` 垃圾数据。后续 `process_weights_after_loading` 中的 `max()` 吸收了未初始化数据，导致 `qkv_proj` scale 被污染，产生 Inf/NaN。

**修复** (commit `f7faed5`): 新增 `PerTensorScaleParameter.load_fused_per_tensor_weight()` 方法，将标量 scale 广播到所有 logical shard，对向量格式则逐元素加载。两种 checkpoint 格式（标量和向量）都支持。

**验证**: flashinfer + graph ON, accept_len=1.50 稳定，6-config 矩阵回归中 zero NaN。

---

### 五、b12x 2-Tier Dispatch 设计与效果

**设计**: 3 路 GEMM 分流 — Marlin (W4A16) / b12x (W4A4 block-scaled MMA) / CUTLASS (W4A4)。per-shape Marlin 阈值：

```python
MARLIN_UPPER = {
    (N=4096,  K=4096):   8,    # std_o
    (N=4608,  K=4096):   8,    # std_qkv
    (N=4096,  K=16384):  24,   # down (K大 Marlin 带宽仍赢到 M=24)
    (N=32768, K=4096):   16,   # gate_up
    (N=12288, K=4096):   16,   # gla_qkv
    (N=4096,  K=12288):  16,   # eagle_fc
}
CUTLASS_OVERRIDE = {
    (4096, 16384, 512),   # down M=512
    (32768, 4096, 8192),  # gate_up M=8192
    (4608, 4096, 8192),   # std_qkv M=8192
}
```

**b12x 最优 tile 分布**（非单一最优，autotune 是必须的）:

| M | std_o | std_qkv | down | gate_up | gla_qkv |
|---|---|---|---|---|---|
| 24 | 64x128/pf | 64x128 | 64x64/pf | 64x128/pf | 64x128/pf |
| 48 | **64x64** | 64x64/pf | 64x64/pf | 64x128 | 64x128/pf |
| 96 | **128x64** | 64x128/pf | 64x64/pf | 64x64/pf | 64x64 |
| 128 | 64x128/pf | **128x64** | 64x64 | 64x64 | 64x64 |
| 256 | 64x128/pf | 64x128 | 64x64/pf | 64x128/pf | 64x64 |

**性能数据** (5 shape x 10 M x 4 backend, 42 min wall clock):

| shape | M=16 Mar/b12x | M=48 Mar/b12x | M=96 C/b12x | M=256 C/b12x | 赢 b12x M 区间 |
|---|---|---|---|---|---|
| std_o (4096x4096) | 12.3/**10.3** | 30.8/**10.2** | 45/**12.3** | 39/**15.1** | M >= 16 |
| down (4096x16384) | **20.6**/37.9 | **49.2**/39.1 | 151/**38.9** | 158/**77.1** | M >= 48 |
| gate_up (4096x32768) | **31.2**/47.1 | 77.2/**38.8** | 77.6/**67.6** | 146/**131** | M >= 24 |

**生产 M 直方图**（54000 次 GEMM, 13.2s wall）: decode GEMM 62% 走 b12x, 18% CUTLASS override, 19% prefill CUTLASS。decode GEMM kernel 时间省 32.4%（1750 -> 1183 ms/13.2s），e2e 估算约 3%。

**正确性**: 23 配置 x 3 seed = 69/69 PASS，cos_sim = 1.000000, max_abs = 0.000000（位级一致）。

**初版集成 bug**: 第一版把 b12x 喂了 "pre-permute padded_scales"（假设 b12x 要 unswizzled 格式），smoke test 模型答非所问。6 种交叉对照定位后确认 b12x 和 CUTLASS 需要**完全相同的 interleaved (TMA-swizzled) weight scale 布局**，修复：直接复用 `layer.weight_scale_interleaved`。

**当前状态**: 开发完成、正确性验证通过，**但未启用**。`SGLANG_ENABLE_B12X` 默认为 0。回滚原因是 EAGLE draft CUDA graph capture 路径不兼容 b12x。Draft model 始终需走纯 Marlin。

---

### 六、NVFP4 KV Cache 调研结论

**最终结论**: NVFP4 KV 在 SALA 当前架构下**没有可落地路径**。

**技术障碍（层层递进）**:

1. **API 层面**（旧结论，已过时）: 老版本 `trtllm_batch_decode_with_kv_cache` 未传 `kv_block_scales`。FlashInfer 0.6.8 已支持。

2. **Kernel 层面（真正阻塞）**: 支持 NVFP4 KV 的 kernel（xqa, trtllm-gen）都要求 `page_size >= 16`；支持 `page_size=1` / sparse 的 kernel 都不吃 NVFP4。

3. **架构层面（根本矛盾）**: SALA 的 InfLLM-v2 sparse 路径硬编码 `page_size=1`（`minicpm_backend.py:1410 assert self.page_size == 1`）。尝试 `page_size=16` 时连续踩坑：
   - `server_args` guard 拒 `speculative_eagle_topk>1 && page_size>1`
   - `HybridLinearKVPool` 透传 bug（`enable_kv_cache_copy` 未传）
   - **compress_k 单 token 分配崩**：架构级不兼容，compress_k pool 和 full KV pool 共享 allocator/page_size，需要独立 allocator 中等规模重构

4. **全球生态**: 30+ 项目盘点，不存在 "NVFP4 KV + page_size=1 + sm_120" 的成熟 kernel。

**离线微基准**:
- xqa dense path: 大 batch x 长 seq 下 NVFP4 确有 2-3x 加速（B=32 L=8192: 210us -> 78us），但不走 sparse path
- 自写 Triton sparse decode: 正确但离 roofline 50x（B=8 SP=4096 = 700us vs flashinfer 23us）
- VariableBlockSparseAttentionWrapper: vs BatchPrefill 整体打平或略慢

**最终推荐**: 路径 C（放弃 NVFP4 KV，守 FP8），保留的 latent bug 修复: `server_args.py` 白名单、`memory_pool.py` 透传参数、`model_runner_kv_cache_mixin.py` 显式传参。

---

### 七、sm_120 各 GEMM 库实测性能对比

**硬件 peak**: sm_120 NVFP4 block-scaled MMA 真实 peak 约 1467 TFLOPS（2 block/SM，实测对齐理论 1553 TFLOPS 的约 95%）。

**M=8192 标定点**:

| Library | 路径 | gate_proj TFLOPS | 备注 |
|---|---|---|---|
| sgl-kernel `cutlass_scaled_fp4_mm` | Sm120 builder | 550 | 当前默认 |
| flashinfer `mm_fp4` backend=cutlass | 同底 CUTLASS | 547 | |
| flashinfer `mm_fp4` backend=cudnn | cuDNN | 551 | 打平 |
| flashinfer `mm_fp4` backend=trtllm | - | 不支持 | BackendSupportedError |
| `torch._scaled_mm` (cuBLAS 13.4) | VEC16_UE4M3 | 553 | PyTorch 2.11 |

**四个库一致约 550 TFLOPS** = 生态共同的未调优状态，仅挤出 peak 的 38%。

**有效 tile 空间**: `{128, 256} x {128, 256} x {128}` + `(128, 128, 256)`，Cluster 锁死 1x1x1。大 K tile + 大 M/N tile 因 smem 不够 2 stage 失败；小 tile (<128) 因 TMA atom 约束失败。

**flashinfer 离线 autotune** (已落地): 利用 6 tactic 池做离线 tune + JSON cache，43/70 入库（验证过 >=3% 增益）。down_proj 最大收益 M=64 3.59x, M=128 3.55x, M=2 3.39x。

---

### 八、Marlin 调优负结果

| 方向 | 结论 | 原因 |
|---|---|---|
| pipe_stages 4->6 | gate_up +5-8%，其余 0%，e2e <0.5% | down 撞 HBM roofline |
| `use_fp32_reduce=False` | M=4-8 退化 9-17% | dispatcher 走不同 tile |
| native FP4 MMA (nvf4) | 不可行 | PTX 要求 A+B 都 FP4，无 W4A16 路径 |
| tile/warp sweep | 无意义 | HMMA:HFMA2 = 1:11，换 tile 不改 HFMA2 数量 |
| sm_120 原生 W4A16 重写 | 无空间 | Marlin decode M=1/8 已达 82-97% L2 BW 饱和 |

**SASS 分析（gate_up M=1）**: HMMA 48 条 vs HFMA2+HADD2+HMUL2 532 条 vs LOP3+SHF+PRMT 454 条。瓶颈是 CUDA core dequant，不是 HBM 或 tensor core。

---

### 九、生产配置最终决策

**当前生产 dispatch**: `SGLANG_MARLIN_DECODE_THRESHOLD=48`，M <= 48 走 Marlin，M > 48 走 CUTLASS。b12x 未启用（默认 `SGLANG_ENABLE_B12X=0`）。

**KV Cache**: `--kv-cache-dtype fp8_e5m2`（生产），高并发稳定收益。NVFP4 KV 放弃。

**Draft model**: 永远用纯 Marlin（no hybrid），`_detect_draft_model_quantization()` 检测到 FP4 draft 时设 threshold=9999。Draft M=1-6 时 CUTLASS 比 BF16 还慢 2.9-7.5x。

**生产 `.so`**: `220c18cc`（probe-sala 版本），是唯一被验证可正常 EAGLE 起服的版本。`32d27c7`（含 Marlin 3% e2e 收益）导致 draft graph capture 挂住。

**No-spec e2e 结果** (最终):
- Old Marlin baseline -> current (kernel-side fixes): S1 -27.17s (-9.85%), S8 -27.41s (-9.35%)
- 其中 Marlin small-M atomic + shape-aware tile 约 3%
- SimpleGLA direct-state decode 约 6.6-6.8%（主要收益来源：gather + generic recurrent + index_put 链路被替换，bs=1 2.33x, bs=8 2.43-3.39x）
- compress_k head-parallel rewrite: k2 1.5-1.8x（尖峰消除）
- Decode replay skip-fill: -0.0764 ms/step

**GPU idle 分析最终结论**: GPU union-busy 82.3%，真可攻击的 host-wait 约 5.5% of window（不是之前误估的 9.6%），单点最大只 2.1%。CPU 侧大改 ROI/risk 不值得。

**下一轮高 ROI 方向**: EAGLE verify 后的 GLA/Mamba state update 融合 CUDA/Triton kernel（当前 `update_mamba_state_after_mtp_verify` 占 98.4% 的 index kernel 时间，但真实 e2e 只有 1.65%），以及保持 k1+k2 语义的 sparse stage1 fused topk。

**关键方法论教训**:
1. NVTX + CUDA 异步时序陷阱: NVTX 标 CPU 时间窗，CUDA kernel GPU end-time 可能延后几 ms，用 GPU end-time 匹配 NVTX 会严重偏移归因。必须 join RUNTIME_API 拿 launch CPU 时间。
2. `.tolist()` 在 GPU tensor 上 = 强制 sync，CPU 阻塞时间实际是 GPU critical path 的投影，消掉等待只是把阻塞从一 API 挪到另一 API，wall time 不变。
3. Profile "账面变好" 不算数，只认 wall time / e2e。

> AGENT

现在我已经从所有文档中获取了全面的信息。让我来整理最终的技术总结。

---

# MiniCPM-SALA 推理优化技术详细摘要（除 EAGLE speculative decoding 和量化之外）

## 一、MiniCPM-SALA 模型架构特殊性

MiniCPM-SALA 是混合注意力架构：**8 层标准注意力 + 24 层 GLA（Lightning Attention/简单 GLA）**，共 32 层。这一混合结构对优化的影响贯穿所有方向：

- 8 层标准注意力必须走 InfLLM-v2 稀疏路径（`--dense-as-sparse` 强制，因精度问题不可关闭），不存在"短序列走密集 FA"分支
- 24 层 GLA 无 KV cache，但需 recurrent state（ssm_states）管理，spec 解码的 verify 后状态更新链路极重
- GLA 被归到 sglang 的 `MambaAttnBackendBase` 类体系，命中了为通用 Mamba 写的 3D 花式散点操作，是 SALA 特有的性能陷阱
- `config.sparse_config`：block_size=64，topk=64(+32 local)=96，kernel_size=32/128，stride=16/64，window_size=2048
- 全局 `page_size=1`（`minicpm_backend.py:1410 assert`），由 InfLLM-v2 token-level sparse 索引决定，不可改

## 二、InfLLM-v2 稀疏注意力的实现与优化

### 2.1 blockmask 修复（`docs/infllmv2-blockmask-fix.md`）

**问题**：InfLLM-v2 原生 blockmask 路径（topk_to_uint64 位掩码 + fwdIterator 跳块）在 batch>1 时结果错误，导致一直无法启用。

**根因**：`topk_to_uint64` 输出 head-major 布局 `(num_k_heads, batch, uint64_per_row)`，但 `fwdIterator` 构造函数用 batch-major 寻址。batch=1 时两种布局等价，batch>1 时读到错误掩码行。

**修复**（3 处源码改动）：
1. `flash_blockmask.h` fwdIterator 寻址改为 head-major：`head_idx * params.b * uint64_per_row + batch_idx * uint64_per_row`
2. 去掉多余的 `loop_step_idx` 偏移（同一 batch/head 的所有 Q token 共享同一行 topk 掩码）
3. `flash_api.cpp` 两处 `num_k_heads` 硬编码 2 改为 `num_heads_k`

**验证**：batch=1/2/4 + nq=16 swap 全部通过，cos=1.00。部署陷阱：rebuild 后 `.so` 仅产出在 `packages/` 目录，Python 实际加载 venv site-packages 中的旧版，需手动 `cp`。

**当前阻塞**：生产路径用的是 FlashInfer paged attention，infllmv2 原生路径未集成。核心矛盾是 paged KV page_size=1 与 infllmv2 kernel 的 `page_block_size % 256 == 0` 硬约束不兼容（一次 cp.async 连续读 64 个 token 要求物理连续）。方案 A（改 kernel 放宽 page_block_size）仍在调研。

### 2.2 稀疏 stage1/stage2 架构

**Stage1**：`infllmv2_attn_stage1` + `max_pooling_1d_varlen` + `block_score.topk`。注意 k1/k2 语义：`infllmv2_attn_stage1` 的 `v` 参数实际传的是 `k2`，内部先跑 `k2` 粗略 softmax 得到 `row max/sum`，再用 `k1` 调用 `softmax_rescale_gt()` + `hdim16_reduce()` 输出 score。因此 k1-only 的 fused topk 全部不正确。

**Stage2**：生产走 FlashInfer `BatchDecodeWithPagedKVCacheWrapper`（不是 `BatchPrefillWithPagedKVCacheWrapper`），因为长序列分支 `sparse_max_seq_len_q` 默认 1，触发 `is_prefill=False`，q tokens 摊平到 batch 维。

## 三、长上下文 Prefill 热点与优化

### 3.1 Prefill 热点分层（128K prompt, chunked-prefill-size=8192）

| 阶段 | 占比 | 说明 |
|---|---|---|
| **extend_sparse_fa**（8 std layer x stage2 sparse FA） | ~26% | 最大单块 |
| **mlp**（32 层 MLP，M=8192 NVFP4 GEMM） | ~16% | |
| **attn_gla**（24 层 Lightning Attention） | ~11% | |
| attn_standard QKV/OUT proj + RoPE | ~5% | |
| sparse_topk（stage1 + pool + topk_select） | ~5% | |
| compress_k | <1% | |
| ln + residual + embed + final_norm | ~2% | |

### 3.2 周期性 2x 慢 chunk — plan() 根因

每 3 个 chunk 出现一次慢 chunk，`extend_sparse_fa` 翻倍。通过 nsys 精确定位：慢点在 `wrapper.begin_forward()` 即 flashinfer `plan()` 的纯 CPU 计算（work-split 决策），耗时约 23ms，偶发 spike 至约 350ms。慢 chunk 中有异常慢的 HtoD + plan 内额外 GPU 辅助 kernel，说明走了"重计算路径"。

### 3.3 plan_info reuse 优化（两步递进）

**Step 1: 层间 plan 复用**（commit `1f265fe`，2026-04-20）

观察：同一 forward 的 8 个标准层 KV layout 完全一致（`max_kv_len/bs/page_size/heads/dtypes` 相同），只有 `_paged_kv_indices` 变化。plan() 的 work split 完全由前面这些量决定。

实现：`FlashInferKernel.__init__` + `forward` 新增 `_plan_cache_key` / `_plan_last_layer_id`，非 CUDA-graph + 稀疏解码 wrapper 分支判定 `layer_id > _plan_last_layer_id` 且 cache_key 匹配则跳过 `begin_forward`，只覆写 `_paged_kv_indices_buf`。下一次 forward 从 L0 开始自动触发重新规划。

**收益：128K prefill 14.6s -> 10.3s（-28%）**。7/8 层 `bf=0.0 ms`。

**Step 2: 跨 chunk plan 复用**（commit `b4d387a`，2026-04-20）

动机：层缓存后每 chunk L0 仍重新规划。InfLLM-v2 在 `seq_len` 超过 `topk` 阈值后 `kv_indptr/kv_last_page_len/bs/page_size` 都固定，只有 `kv_indices` 内容变化。

实现：缓存新增 `_plan_cached_indptr_bytes` / `_plan_cached_lpl_bytes`（CPU-side 字节副本），层级判定失败后做 CPU 字节比较，匹配则复用。

**收益：64 smax 样本纯 prefill 416.29s -> 290.23s（-30.3% e2e，p50 60s -> 42s）**。

两步合计 prefill 加速显著，但 decode 走 CUDA graph 分支，`cache on/off` 解码 `TPS` 噪声级一致。

### 3.4 Stage2 sparse FA 是内存带宽瓶颈

算术强度分析（topk=96, block_size=64, head_dim=128, BF16）：
- 每次查询块：FLOPs 约为 3.1M，字节约为 3.9M
- 算术强度 约为 0.78 FLOP/byte
- `ridge point` 约为 935 FLOP/byte（sm_120 1568 GB/s HBM）
- 结论：**极度内存带宽受限**，提升 `TC utilization` 无效，有效方向只有减少 HBM 流量或利用 `skip`

### 3.5 trtllm_fmha_v2_prefill kernel swap（未合入，Phase 2 调研）

发现 `flashinfer.prefill.trtllm_fmha_v2_prefill` 直调（无 `skip_softmax`）在 SM120 上可用，`Q=8192, KV=6144` 场景 **1.67x 快于** `fa2`。但加速来源是跳过全掩码 Q 行（`fa2` 也算了但产出垃圾，`trtllm` 输出零）。与 P1a topk 96->64 **乘性复合**：`topk=64` 时 stage2 可达 2.86x -> **e2e +17%**。核心风险是行为变化（`fa2` 垃圾 -> `trtllm` 零），需 `accuracy A/B` 验证。

### 3.6 Prefill 已终结方向

- `cuDNN SDPA / dense FA path`：`--dense-as-sparse` 强制，代码分支不存在
- FA3/FA4：sm_120 无 `TMEM`
- `SageAttention3`：需 Python>=3.13（我们 3.10），无 `varlen/paged KV API`
- FLA `tl.exp2`：sm_120 实测比 `tl.exp` 慢 83%
- CUTLASS tile sweep M=8192：SM120 只有 3 个有效 `tile`，差距<1%
- `compress_k` 优化：占比<1%

## 四、Decode 期算子优化清单

### 4.1 已落地的优化

| 优化 | 解码收益 | Prefill 收益 | 详细说明 |
|---|---|---|---|
| **RoPE F32 cast 消除**（`f4bea68`） | 140 us/fwd (3.5x) | 11.2 ms/fwd (4.5x) | `sgl_kernel RoPE` 内部已是 F32；cos_sim=1.0 |
| **Residual fused multiply-add**（`2162051`） | 237 us/fwd (2.15x) | 4.4 ms/fwd (5.76x) | `torch.add(residual, hidden, alpha=precomputed_scale)`，精度高于 F64 参考 |
| **scale_emb / width 吸收进权重**（`139652c`） | 2 kernels 消除 | 284 us/fwd | `BF16-representable` 标量，`exact` |
| **In-place sigmoid x mul gate**（`139652c`） | memory pressure 降低 | - | 等价 |
| **GLA backend cleanup**（`139652c`） | 约为 24 us | - | 删冗余 `.contiguous()` + `cache` 查询 |
| **Flashinfer mm_fp4 离线 autotune** | down_proj M=64 3.59x | - | 43/70 验证过 >=3% 增益入 `cache`，`miss` 走 `fallback` |
| **Marlin small-M atomic + shape-aware tile** | no-spec e2e 约 3% | - | `B0 old Marlin` -> `current`：S1 -9.13s, S8 -8.67s |
| **SimpleGLA direct-state decode** | `bs=1` 2.33x, `bs=8` 2.43x | - | 自定义 kernel 替换 `fused_recurrent_simple_gla` + `gather/index_put` 链路 |
| **compress_k head-parallel rewrite** | `k2 bs=1` 1.81x | - | 消除旧 kernel 冗余 `mean pooling`，去尖峰 |
| **Decode replay skip-fill** | -0.103 ms/step | - | 跳过 `compress_k` buffer 每步 `-inf fill` |
| **Hybrid Marlin/CUTLASS dispatch** | M<=48 Marlin, M>48 CUTLASS | - | 全局 `SGLANG_MARLIN_DECODE_THRESHOLD=48` |

### 4.2 SimpleGLA Direct-State Decode — 当前最大杠杆的 kernel 侧优化

（`marlin-tuning.md` 13/26，2026-04-26 捞回验证）

24 层 GLA 的解码旧路径：
```python
initial_state = layer_cache.temporal[mamba_indices, :].contiguous()
o, final_state = fused_recurrent_simple_gla(..., initial_state=initial_state)
layer_cache.temporal[mamba_indices, :] = final_state
```
对应 `vectorized_gather` + `fused_recurrent_fwd_kernel` + `index_put` 三段组合。

新 kernel `simple_gla_decode_update_fwd()`：直接从 `temporal[state_indices]` 读 recurrent state，在 kernel 内写回更新后的 state，使用 BK=BV=128 decode tile。

**CUDA graph replay**：bs=1 14.38->6.16 us (2.33x)，bs=8 34.84->10.28 us (3.39x)，state diff=0.0。

**no-spec e2e**：S1 266.57s->248.53s (-6.77%)，S8 284.37s->265.63s (-6.59%)。这是当前最实质性的 decode 算子优化。

### 4.3 b12x 2-tier dispatch（开发完成，当前未启用）

`SGLANG_ENABLE_B12X=1` 默认为 0。原因：EAGLE draft CUDA graph capture 不兼容 b12x（`marlin-tuning.md` 25 确认 current Marlin `.so` 会导致 EAGLE-3 draft graph capture 挂住）。

离线数据：decode GEMM kernel 省 32.4%（5 shape x M=24..256），但 e2e 约 3%。b12x 和 CUTLASS 位级等价（69/69 PASS, cos=1.000000）。且 b12x/Marlin `crossover` 不影响 `decode graph replay` 的 Marlin kernel（Python 分流只在 `prefill` 和 `capture` 时执行）。

### 4.4 Medusa speculative decoding（已废弃）

commit `c6b7991`：S1 -12%，S8 -12.5%。但 `accept_len` 约 1.7、`accept_rate` 约 42%，被 EAGLE-3 替代。

### 4.5 EAGLE dynamic mode 优化（最新）

commit `20cc58a` + `87a8bb1`（2026-04-28）：
1. NO_SPEC lazy draft KV catch-up：跳过每步 1-token `forward_draft_extend_after_decode`，累积后一次性 `flush`
2. `verify_qo_indptr` 预建 per-dtn bank：零热路径 `arange/copy_`
3. `_get_graph_key` 双调用折叠：缓存 graph kind
4. `_apply_spec_config` 未变模式 early-return
5. FlashInfer `verify plan()` 改用 `pinned-memory CPU inputs`，省 3 次 D2H sync 约 26 us/replay

## 五、负结果清单（避免重复踩坑）

| 方向 | 结论 |
|---|---|
| `stage2 FlashInfer backend swap`（fa3/cutlass/trtllm-gen） | sm_120 全部不支持 |
| `VariableBlockSparseAttentionWrapper` | 4x 慢 |
| EAGLE3 `--fuse-topk`（`tilelang` 融合 stage1+pool+topk） | 一致性崩（只用 k1，`dup bug`） |
| FP8 KV cache | 无收益（KV 带宽非瓶颈） |
| NVFP4 KV cache | InfLLM-v2 sparse + `page_size=1` 不兼容 |
| `mamba cache quant` (INT8/4) | temporal state 累积误差 |
| Triton NVFP4 GEMV | 2.6x `slower` |
| Full Marlin (no hybrid) | prefill 3.8x `slower`（M=8192） |
| SimpleGLA BK=128 kernel | 1.65x `slower`（CUDA graph 揭真相） |
| Medusa K=3 | 微弱（GLA overhead 2x） |
| Triton `kv_indices` kernel | 0.78x `slower` |
| `pre_quant_scale` fusion | 不值（CUDA graph 消除 launch overhead） |
| `minicpm_fi` fused metadata copy | 无收益（bs=1 长样本噪声级） |
| `_alloc_sparse_for_new_positions` 向量化 | 中性 |
| TARGET_VERIFY replay de-Python | target forward GPU 主导，Python<5% |
| `compressed_k` 跨层复用 | 噪声内 |
| `EI_ai_tolist` 消除 | `.tolist()` 的 CPU 阻塞是 target_forward GPU kernel 的 CPU 侧影像，`wall time` 不变 |
| `split_stage1` | 更慢 + topk overlap 只有 0.42-0.47 |
| topk sorted=False | microbench 1.2x 但 `run-to-run topk` 抖动 |
| decode pooling no-zero | S1 1.52x 但 S8 基本持平 |
| M=1 Marlin exact tile | `std_o` 1.3x microbench 但 e2e<1%，且与 EAGLE draft graph capture 不兼容 |

## 六、End-to-End 速度收益数字汇总

| 优化 | 场景 | 收益 |
|---|---|---|
| `plan_info` 层间复用 | 128K prefill | 14.6s -> 10.3s（-28%） |
| `plan_info` 跨 chunk 复用 | 64 smax 纯 prefill | 416.29s -> 290.23s（-30.3%，p50 60s->42s） |
| `RoPE F32 cast` 消除 | decode M=1 | 140 us/fwd (3.5x) |
| `Residual fused multiply-add` | decode M=1 | 237 us/fwd (2.15x) |
| Marlin `small-M atomic` + `tile` | no-spec `mini_bench` | S1 -9.13s, S8 -8.67s（约为 3%） |
| `SimpleGLA direct-state decode` | no-spec `mini_bench` | S1 -18.04s（-6.77%），S8 -18.74s（-6.59%） |
| `B0 old Marlin` -> `after kernel-side` | no-spec `mini_bench` | S1 -27.17s（-9.85%），S8 -27.41s（-9.35%） |
| Medusa spec（已废弃） | S1/S8 | S1 -12%，S8 -12.5% |
| `intermediate_ssm direct-write` | `bs=4 profile` | `direct_copy` 39.5ms->0.4ms（-99%），`profile wall` -8.9% |
| `b12x` dispatch（未启用） | decode GEMM `offline` | -32.4% kernel time，e2e 约为 3% |
| `compress_k head-parallel` | CUDA graph | `k2 bs=1` 1.81x，`k1 bs=1` 1.99x |
| `SimpleGLA direct decode` CUDA graph | `bs=1` / `bs=8` | 2.33x / 2.43x |

## 七、CUDA 13 升级的性能影响

### 7.1 升级内容

`torch` 2.9.1+`cu128` -> 2.11.0+`cu130`，`FlashInfer` 0.6.7 -> 0.6.8.`post1`[`cu13`]，`cuDNN` 9.15 -> 9.21，全部 `CUDA extension` 重编（`sgl-kernel` / `infllm_v2` / `sparse_kernel`）。

### 7.2 Kernel 级 diff

| 路径 | 形状 | M 范围 | 约为 |
|---|---|---|---|
| `Marlin FP4 decode` | `gate_proj` 4096x16384 | M=1-8 | **-12.5%** |
| `Marlin FP4 decode` | `down_proj` 16384x4096 | M=1-32 | **-11%** |
| `Marlin FP4 decode` | `k_proj` 4096x256 | M=1-8 | -4% |
| `CUTLASS NVFP4` | `k_proj` 4096x256 | M=1-2 | **-21~25%** |
| `CUTLASS NVFP4` | 其他 | 全段 | 约为 2% 噪声 |

零回归。Marlin decode 大 MLP 形状 10-12% 提速 = S1 decode 热路径直接受益。

### 7.3 E2e 验证

长上下文（63K prompt + 512 tokens）端到端 36.01s，EAGLE `accept_len` 1.45-1.48（对齐 `cu12` 约 1.50），decode 峰值 159.49 `tok/s`。正确性通过。

### 7.4 预期 vs 实际

文档预测 `mini_bench` S1 192.04s -> 150-175s（-10~20%），S8 230.42s -> 180-210s（-10~20%）。`FlashInfer` 0.6.8 已 `port TRT-LLM SM120/121 FP4 CUTLASS GEMM` 优化，`prefill M>48 GEMM` 5-15% 提升已在 `kernel bench` 部分体现。

### 7.5 关键坑洞

- `cudnn-frontend 1.22` 同时检测到 `libcudart.so.12` 和 `.so.13` 会硬拒 -> 需清 `/etc/ld.so.conf.d/` 中 `cu12` 条目 + `ldconfig`
- `cuDNN` 9.19 -> 9.21 是 `sm_120 FP4` 必需（`mm_fp4(cudnn)` 需 `backend_version >= 92100`）
- 卸 `cu12 pip` 包会删共享目录 `.so` -> 必须 `force-reinstall cu13` 恢复
- `CUTLASS 3.6 cuda_host_adapter.hpp` 版本 `guard bug`：需改 `MAJOR>=13 ||`

## 八、Runtime profiling 方法论关键教训

1. **GPU end-time vs CPU launch-time 归因**：NVTX `push/pop` 只标 CPU 时间窗，CUDA kernel 的 GPU end-time 可能在 launch 之后数 ms。用 GPU end-time 匹配 NVTX 会严重偏移大量 kernel 的归因。`update_mamba_state_after_mtp_verify` 最初被误报为 `_alloc_sparse_for_new_positions`，正确做法是 `JOIN CUPTI_ACTIVITY_KIND_RUNTIME` 拿 launch CPU 时间。

2. **CPU 在 sync API 里的时间 != CPU 工作量**：`.tolist()` 的 4ms CPU 阻塞是 target_forward GPU kernel 的 CPU 侧影像，消掉等待只是把阻塞从一个 API 挪到另一个，`wall time` 不变。

3. **`nsys --cuda-graph-trace=graph` 不展开 graph 内部**：decode forward 全在 CUDA graph 内，默认模式下 kernel 对 profile 不可见 -> 误读为"GPU 4%"。必须用 `--cuda-graph-trace=node`。

4. **17.7% idle 最终归类**：`host-wait` 约为 5.5%（不含 `bench` 间 idle），`single-point` 最大 2.1%（EV_target_forward）。CPU 侧优化 e2e 硬顶约为 5.5%。

5. **GPU union-busy 82.3%** -> workload 是 GPU-bound，GPU kernel 优化仍是第一优先级。Top GPU kernels：NVFP4 GEMM 10.17%，BatchPrefill 6.42%，index_elementwise 2.63%。

> DEVELOPER

请帮我核实以下两篇论文的技术细节，用于撰写技术博客，需要确保原理描述准确。

**论文一：FourOverSix**
- arXiv: 2512.02010
- 声称是 MIT-HAN Lab 的工作
- 核心思路：对每个 NVFP4 量化 block，比较 scale=4 和 scale=6 的 MSE，选更小者
- 请访问 https://arxiv.org/abs/2512.02010 确认：
  1. 论文标题、作者、机构
  2. FourOverSix 算法的准确描述（scale=4 vs scale=6 的具体含义）
  3. NVFP4 格式中 scale 参数的作用（scale÷6 还是别的？）
  4. 论文报告的性能数字

**论文二：Medusa**
- 声称是 Tianle Cai et al., ICML 2024
- 核心：多个预测头附加在 LLM 最后一层，ResBlock + LM Head 结构
- 请访问 https://arxiv.org/abs/2401.10774 确认：
  1. 论文标题、作者、venue
  2. Medusa head 的准确架构（ResBlock 具体结构）
  3. verify 机制（tree attention 的工作方式）
  4. 与 standard speculative decoding 的核心区别

请直接访问 arxiv 页面获取准确信息，给出验证结论。

> AGENT

我将同时访问两篇 arXiv 论文以核实技术细节。

> TOOL

tool_use mcp__exa__web_fetch_exa
```json
{
  "maxCharacters": 15000,
  "urls": [
    "https://arxiv.org/abs/2512.02010",
    "https://arxiv.org/abs/2401.10774"
  ]
}
```

> TOOL

tool_result mcp__exa__web_fetch_exa
```
<persisted-output>
Output too large (85.9KB). Full output saved to: /user_4813494d/.claude/projects/-user_4813494d-openbmb/76f3fa2c-f12e-4e32-8a58-71a3688d03ea/tool-results/call_c422462b7fe94f74a6748e63.json

Preview (first 2KB):
[
  {
    "type": "text",
    "text": "# [2512.02010] Four Over Six: More Accurate NVFP4 Quantization with Adaptive Block Scaling\nURL: https://arxiv.org/abs/2512.02010\nPublished: 2025-12-01\n\n[2512.02010] Four Over Six: More Accurate NVFP4 Quantization with Adaptive Block Scaling\n\n# Computer Science > Computation and Language\n\narXiv:2512.02010 (cs)\n\n[Submitted on 1 Dec 2025 (v1), last revised 22 Jan 2026 (this version, v3)]\n\n# Title:Four Over Six: More Accurate NVFP4 Quantization with Adaptive Block Scaling\n\nView PDF HTML (experimental)\n\n> Abstract:As large language models have grown larger, interest has grown in low-precision numerical formats such as NVFP4 as a way to improve speed and reduce memory usage. However, quantizing models to NVFP4 remains difficult as the lack of precision generally degrades model performance. In this work, we address this issue with Four Over Six (4/6), a modification to the block-scaled NVFP4 quantization algorithm that yields reduced quantization error. Unlike integer formats, floating point formats have non-uniform step sizes which create larger quantization error on larger values. 4/6 takes advantage of this by adaptively scaling some blocks to smaller FP4 values, making the distribution of representable values more uniform and reducing quantization error for near-maximal values. We show that 4/6 can be implemented efficiently on NVIDIA Blackwell GPUs, resulting in performance gains during both pre-training and inference with minimal computational overhead. In pre-training experiments with the Nemotron 3 Nano 30B-A3B model architecture, we find that 4/6 brings training loss closer to BF16 compared to models trained with current state-of-the-art NVFP4 training recipes. Our code is available at this http URL.\n\narXiv-issued DOI via DataCite\n\n| Comments: |\n| --- |\n| Subjects: | Computation and Language (cs.CL); Machine Learning (cs.LG) |\n| Cite as: | arXiv:2512.02010 [cs.CL] |\n| (or arXiv:2512.02010v3 [cs.CL] for
...
</persisted-output>
```

> AGENT

让我阅读完整的抓取结果，以便更详细地获取这两篇论文的信息。

> TOOL

tool_use Bash
```json
{
  "command": "cat /user_4813494d/.claude/projects/-user_4813494d-openbmb/76f3fa2c-f12e-4e32-8a58-71a3688d03ea/tool-results/call_c422462b7fe94f74a6748e63.json | python3 -c \"import json,sys; data=json.load(sys.stdin); print(data[0]['text'][:8000])\"",
  "description": "Read FourOverSix paper content from fetched results"
}
```

> TOOL

tool_result Bash
```
# [2512.02010] Four Over Six: More Accurate NVFP4 Quantization with Adaptive Block Scaling
URL: https://arxiv.org/abs/2512.02010
Published: 2025-12-01

[2512.02010] Four Over Six: More Accurate NVFP4 Quantization with Adaptive Block Scaling

# Computer Science > Computation and Language

arXiv:2512.02010 (cs)

[Submitted on 1 Dec 2025 (v1), last revised 22 Jan 2026 (this version, v3)]

# Title:Four Over Six: More Accurate NVFP4 Quantization with Adaptive Block Scaling

View PDF HTML (experimental)

> Abstract:As large language models have grown larger, interest has grown in low-precision numerical formats such as NVFP4 as a way to improve speed and reduce memory usage. However, quantizing models to NVFP4 remains difficult as the lack of precision generally degrades model performance. In this work, we address this issue with Four Over Six (4/6), a modification to the block-scaled NVFP4 quantization algorithm that yields reduced quantization error. Unlike integer formats, floating point formats have non-uniform step sizes which create larger quantization error on larger values. 4/6 takes advantage of this by adaptively scaling some blocks to smaller FP4 values, making the distribution of representable values more uniform and reducing quantization error for near-maximal values. We show that 4/6 can be implemented efficiently on NVIDIA Blackwell GPUs, resulting in performance gains during both pre-training and inference with minimal computational overhead. In pre-training experiments with the Nemotron 3 Nano 30B-A3B model architecture, we find that 4/6 brings training loss closer to BF16 compared to models trained with current state-of-the-art NVFP4 training recipes. Our code is available at this http URL.

arXiv-issued DOI via DataCite

| Comments: |
| --- |
| Subjects: | Computation and Language (cs.CL); Machine Learning (cs.LG) |
| Cite as: | arXiv:2512.02010 [cs.CL] |
| (or arXiv:2512.02010v3 [cs.CL] for this version) |

## Submission history

From: Jack Cook [view email] [v1] Mon, 1 Dec 2025 18:59:45 UTC (1,697 KB) [v2] Wed, 3 Dec 2025 17:24:59 UTC (1,695 KB) [v3] Thu, 22 Jan 2026 18:49:14 UTC (704 KB)

Full-text links:

## Access Paper:

Current browse context:

cs.CL

< prev| next >

Change to browse by:

### References & Citations

- Google Scholar
- Semantic Scholar

export BibTeX citation

### Bookmark

Bibliographic Tools

# Bibliographic and Citation Tools

Bibliographic Explorer Toggle

Bibliographic Explorer (What is the Explorer?)

Connected Papers Toggle

Connected Papers (What is Connected Papers?)

Litmaps Toggle

Litmaps (What is Litmaps?)

scite.ai Toggle

scite Smart Citations (What are Smart Citations?)

Code, Data, Media

# Code, Data and Media Associated with this Article

alphaXiv Toggle

alphaXiv (What is alphaXiv?)

Links to Code Toggle

CatalyzeX Code Finder for Papers (What is CatalyzeX?)

DagsHub Toggle

DagsHub (What is DagsHub?)

GotitPub Toggle

Gotit.pub (What is GotitPub?)

Huggingface Toggle

Hugging Face (What is Huggingface?)

ScienceCast Toggle

ScienceCast (What is ScienceCast?)

Demos

# Demos

Replicate Toggle

Replicate (What is Replicate?)

Spaces Toggle

Hugging Face Spaces (What is Spaces?)

Spaces Toggle

TXYZ.AI (What is TXYZ.AI?)

Related Papers

# Recommenders and Search Tools

Link to Influence Flower

Influence Flower (What are Influence Flowers?)

Core recommender toggle

CORE Recommender (What is CORE?)

- Author
- Venue
- Institution
- Topic

About arXivLabs

# arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? Learn more about arXivLabs.

# Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads
URL: https://arxiv.org/abs/2401.10774

Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads

# Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads

Tianle Cai Yuhong Li Zhengyang Geng Hongwu Peng Jason D. Lee Deming Chen Tri Dao

###### Abstract

Large Language Models (LLMs) employ auto-regressive decoding that requires sequential computation, with each step reliant on the previous one’s output. This creates a bottleneck as each step necessitates moving the full model parameters from High-Bandwidth Memory (HBM) to the accelerator’s cache. While methods such as speculative decoding have been suggested to address this issue, their implementation is impeded by the challenges associated with acquiring and maintaining a separate draft model. In this paper, we present Medusa, an efficient method that augments LLM inference by adding extra decoding heads to predict multiple subsequent tokens in parallel. Using a tree-based attention mechanism, Medusa constructs multiple candidate continuations and verifies them simultaneously in each decoding step. By leveraging parallel processing, Medusa substantially reduces the number of decoding steps required. We present two levels of fine-tuning procedures for Medusa to meet the needs of different use cases: Medusa-1: Medusa is directly fine-tuned on top of a frozen backbone LLM, enabling lossless inference acceleration. Medusa-2: Medusa is fine-tuned together with the backbone LLM, enabling better prediction accuracy of Medusa heads and higher speedup but needing a special training recipe that preserves the model’s capabilities. Moreover, we propose several extensions that improve or expand the utility of Medusa, including a self-distillation to handle situations where no training data is available and a typical acceptance scheme to boost the acceptance rate while maintaining generation quality. We evaluate Medusa on models of various sizes and training procedures. Our experiments demonstrate that Medusa-1 can achieve over 2.2 $\times$ speedup without compromising generation quality, while Medusa-2 further improves the speedup to 2.3-2.8 $\times$ .

Machine Learning, ICML

## 1 Introduction

The recent advancements in Large Language Models (LLMs) have demonstrated that the quality of language generation significantly improves with an increase in model size, reaching billions of parameters (Brown et al., 2020; Chowdhery et al., 2022; Zhang et al., 2022; Hoffmann et al., 2022; OpenAI, 2023; Google, 2023; Touvron et al., 2023). However, this growth has led to an increase in inference latency, which poses a significant challenge in practical applications. From a system perspective, LLM inference is predominantly memory-bandwidth-bound (Shazeer, 2019; Kim et al., 2023), with the main latency bottleneck stemming from accelerators’ memory bandwidth rather than arithmetic computations. This bottleneck is inherent to the sequential nature of auto-regressive decoding, where each forward pass requires transferring the complete model parameters from High-Bandwidth Memory (HBM) to the accelerator’s cache. This process, which generates only a single token, underutilizes the arithmetic computation potential of modern accelerators, leading to inefficiency.

To address this, one approach to speed up LLM inference involves increasing the arithmetic intensity (the ratio of total floating-point operations (FLOPs) to total data movement) of the decoding process and reducing the number of decoding steps. In line with this idea, speculative decoding has been proposed (Leviathan et al., 2022; Chen et al., 2023; Xia et al., 2023; Miao et al., 2023). This method uses a smaller draft model to generate a token sequence, which is then refined by the original, larger model for acceptable continuation. However, obtaining an appropriate draft model remains challenging, and it’s even harder
```

> TOOL

tool_use Bash
```json
{
  "command": "cat /user_4813494d/.claude/projects/-user_4813494d-openbmb/76f3fa2c-f12e-4e32-8a58-71a3688d03ea/tool-results/call_c422462b7fe94f74a6748e63.json | python3 -c \"import json,sys; data=json.load(sys.stdin); print(data[0]['text'][8000:20000])\"",
  "description": "Read FourOverSix paper content continued"
}
```

> TOOL

tool_result Bash
```
to integrate the draft model into a distributed system (Chen et al., 2023).

Instead of using a separate draft model to sequentially generate candidate outputs, in this paper, we revisit and refine the concept of using multiple decoding heads on top of the backbone model to expedite inference (Stern et al., 2018). We find that when applied effectively, this technique can overcome the challenges of speculative decoding, allowing for seamless integration into existing LLM systems. Specifically, we introduce Medusa, a method that enhances LLM inference by integrating additional decoding heads to concurrently predict multiple tokens. These heads are fine-tuned in a parameter-efficient manner and can be added to any existing model. With no requirement for a draft model, Medusa offers easy integration into current LLM systems, including those in distributed environments, ensuring a user-friendly experience.

We further enhance Medusa with two key insights. Firstly, the current approach of generating a single candidate continuation at each decoding step leads to inefficient use of computational resources. To address this, we propose generating multiple candidate continuations using the Medusa heads and verifying them concurrently through a simple adjustment to the attention mask. Secondly, we can reuse the rejection sampling scheme as used in speculative decoding (Leviathan et al., 2022; Chen et al., 2023) to generate consistent responses with the same distribution as the original model. However, it cannot further enhance the acceleration rate. Alternatively, we introduce a typical acceptance scheme that selects reasonable candidates from the Medusa head outputs. We use temperature as a threshold to manage deviation from the original model’s predictions, providing an efficient alternative to the rejection sampling method. Our results suggest that the proposed typical acceptance scheme can accelerate the decoding speed further while maintaining a similar generation quality.

To equip LLMs with predictive Medusa heads, we propose two distinct fine-tuning procedures tailored to various scenarios. For situations with limited computational resources or when the objective is to incorporate Medusa into an existing model without affecting its performance, we recommend Medusa-1. This method requires minimal memory and can be further optimized with quantization techniques akin to those in QLoRA (Dettmers et al., 2023), without compromising the generation quality due to the fixed backbone model. However, in Medusa-1, the full potential of the backbone model is not utilized. We can further fine-tune it to enhance the prediction accuracy of Medusa heads, which can directly lead to a greater speedup. Therefore, we introduce Medusa-2, which is suitable for scenarios with ample computational resources or for direct Supervised Fine-Tuning (SFT) from a base model. The key to Medusa-2 is a training protocol that enables joint training of the Medusa heads and the backbone model without compromising the model’s next-token prediction capability and output quality. We propose different strategies for obtaining the training datasets depending on the model’s training recipe and dataset availability. When the model is fine-tuned on a public dataset, it can be directly used for Medusa. If the dataset is unavailable or the model underwent a Reinforcement Learning with Human Feedback (RLHF) (Ouyang et al., 2022) process, we suggest a self-distillation approach to generate a training dataset for the Medusa heads.

Our experiments primarily focus on scenarios with a batch size of one, which is representative of the use case where LLMs are locally hosted for personal use. We test Medusa on models of varying sizes and training settings, including Vicuna-7B, 13B (trained with a public dataset), Vicuna-33B (Chiang et al., 2023) (trained with a private dataset111Upon contacting the authors, this version is experimental and used some different data than Vicuna 7B and 13B.), and Zephyr-7B (trained with both supervised fine-tuning and alignment). Medusa can achieve a speedup of 2.3 to 2.8 times across different prompt types without compromising on the quality of generation.

Figure 1: Medusa introduces multiple heads on top of the last hidden states of the LLM, enabling the prediction of several subsequent tokens in parallel (Section 2.1.1). During inference, each head generates multiple top predictions for its designated position. These predictions are assembled into candidates, which are processed in parallel using a tree-based attention mechanism (Section 2.1.2). The final step is to verify the candidates and accept a continuation. Besides the standard rejection sampling scheme, a typical acceptance scheme (Section 2.3.1) can also be used here to select reasonable continuations, and the longest accepted candidate prefix will be used for the next decoding phase.

## 2 Methodology

Medusa follows the same framework as speculative decoding, where each decoding step primarily consists of three substeps: (1) generating candidates, (2) processing candidates, and (3) accepting candidates. For Medusa, (1) is achieved by Medusa heads, (2) is realized by tree attention, and since Medusa heads are on top of the original model, the logits calculated in (2) can be used for substep (1) for the next decoding step. The final step (3) can be realized by either rejection sampling (Leviathan et al., 2022; Chen et al., 2023) or typical acceptance (Section 2.3.1). The overall pipeline is illustrated in Figure 1.

In this section, we first introduce the key components of Medusa, including Medusa heads, and tree attention. Then, we present two levels of fine-tuning procedures for Medusa to meet the needs of different use cases. Finally, we propose two extensions to Medusa, including self-distillation and typical acceptance, to handle situations where no training data is available for Medusa and to improve the efficiency of the decoding process, respectively.

### 2.1 Key Components

#### 2.1.1 Medusa Heads

In speculative decoding, subsequent tokens are predicted by an auxiliary draft model. This draft model must be small yet effective enough to generate continuations that the original model will accept. Fulfilling these requirements is a challenging task, and existing approaches (Spector & Re, 2023; Miao et al., 2023) often resort to separately pre-training a smaller model. This pre-training process demands substantial additional computational resources. For example, in (Miao et al., 2023), a reported 275 NVIDIA A100 GPU hours were used. Additionally, separate pre-training can potentially create a distribution shift between the draft model and the original model, leading to continuations that the original model may not favor. Chen et al. (2023) have also highlighted the complexities of serving multiple models in a distributed environment.

To streamline and democratize the acceleration of LLM inference, we take inspiration from Stern et al. (2018), which utilizes parallel decoding for tasks such as machine translation and image super-resolution. Medusa heads are additional decoding heads appended to the last hidden states of the original model. Specifically, given the original model’s last hidden states $h_{t}$ at position $t$ , we add $K$ decoding heads to $h_{t}$ . The $k$ -th head is used to predict the token in the $(t+k+1)$ -th position of the next tokens (the original language model head is used to predict the $(t+1)$ -th position). The prediction of the $k$ -th head is denoted as $p_{t}^{(k)}$ , representing a distribution over the vocabulary, while the prediction of the original model is denoted as $p_{t}^{(0)}$ . Following the approach of Stern et al. (2018), we utilize a single layer of feed-forward network with a residual connection for each head. We find that this simple design is sufficient to achieve satisfactory performance. The definition of the $k$ -th head is outlined as:

| $\displaystyle p_{t}^{(k)}=\text{softmax}\left(W_{2}^{(k)}\cdot\left(\text{SiLU% }(W_{1}^{(k)}\cdot h_{t})+h_{t}\right)\right),$ |
| --- |
| $\displaystyle\text{where }W_{2}^{(k)}\in\mathbb{R}^{d\times V},W_{1}^{(k)}\in% \mathbb{R}^{d\times d}.$ |

$d$ is the output dimension of the LLM’s last hidden layer and $V$ is the vocabulary size. We initialize $W_{2}^{(k)}$ identically to the original language model head, and $W_{1}^{(k)}$ to zero. This aligns the initial prediction of Medusa heads with that of the original model. The SiLU activation function (Elfwing et al., 2017) is employed following the Llama models (Touvron et al., 2023).

Unlike a draft model, Medusa heads are trained in conjunction with the original backbone model, which can remain frozen during training (Medusa-1) or be trained together (Medusa-2). This method allows for fine-tuning large models even on a single GPU, taking advantage of the powerful base model’s learned representations. Furthermore, it ensures that the distribution of the Medusa heads aligns with that of the original model, thereby mitigating the distribution shift problem. Additionally, since the new heads consist of just a single layer akin to the original language model head, Medusa does not add complexity to the serving system design and is friendly to distributed settings. We will discuss the training recipe for Medusa heads in Section 2.2.

#### 2.1.2 Tree Attention

Through Medusa heads, we obtain probability predictions for the subsequent $K+1$ tokens. These predictions enable us to create length- $K+1$ continuations as candidates. While the speculative decoding studies (Leviathan et al., 2022; Chen et al., 2023) suggest sampling a single continuation as the candidate, leveraging multiple candidates during decoding can enhance the expected acceptance length within a decoding step. Nevertheless, more candidates can also raise computational demands. To strike a balance, we employ a tree-structured attention mechanism to process multiple candidates concurrently.

Figure 2: We demonstrates the use of tree attention to process multiple candidates concurrently. As exemplified, the top-2 predictions from the first Medusa head and the top-3 from the second result in a total of $2\times 3=6$ candidates. Each of these candidates corresponds to a distinct branch within the tree structure. To guarantee that each token only accesses its predecessors, we devise an attention mask that exclusively permits attention flow from the current token back to its antecedent tokens. The positional indices for positional encoding are adjusted in line with this structure.

This attention mechanism diverges from the traditional causal attention paradigm. Within this framework, only tokens from the same continuation are regarded as historical data. Drawing inspiration from the concept of embedding graph structures into attention as proposed in the graph neural network domain (Ying et al., 2021), we incorporate the tree structure into our attention mask, visualized in Figure 2. Remarkably, similar ideas have also been explored in independent works like Miao et al. (2023); Spector & Re (2023), where they follow a bottom-up approach and construct the tree by merging multiple candidates generated by a draft model. In our method, we instead take a top-down approach to build the tree thanks to the structure of candidates generated by Medusa heads. For a given $k$ -th head, its top- $s_{k}$ predictions serve as the basis for candidate formation, where $s_{k}$ is a designated hyperparameter. These candidates are established by determining the Cartesian product of the top- $s_{k}$ predictions from each head. For instance, in Figure 2, with $s_{1}=2$ and $s_{2}=3$ , each first head prediction can be succeeded by any prediction from the second head. This leads to a tree structure where $s_{k}$ branches exist at the $k$ -th level (considering a virtual user_4813494d as the $0$ -level, in practice, this $0$ -level is for the prediction of the language mod
```

> TOOL

tool_use Bash
```json
{
  "command": "cat /user_4813494d/.claude/projects/-user_4813494d-openbmb/76f3fa2c-f12e-4e32-8a58-71a3688d03ea/tool-results/call_c422462b7fe94f74a6748e63.json | python3 -c \"import json,sys; data=json.load(sys.stdin); print(data[1]['text'][:8000])\"",
  "description": "Read Medusa paper content from fetched results"
}
```

> TOOL

tool_result Bash
```
Exit code 1
Traceback (most recent call last):
  File "<string>", line 1, in <module>
IndexError: list index out of range
```

> TOOL

tool_use Bash
```json
{
  "command": "cat /user_4813494d/.claude/projects/-user_4813494d-openbmb/76f3fa2c-f12e-4e32-8a58-71a3688d03ea/tool-results/call_c422462b7fe94f74a6748e63.json | python3 -c \"import json,sys; data=json.load(sys.stdin); print(data[1]['text'][8000:20000])\"",
  "description": "Read Medusa paper content continued"
}
```

> TOOL

tool_result Bash
```
<tool_use_error>Cancelled: parallel tool call Bash(cat /user_4813494d/.claude/projects/-user_4813494d-openbmb…) errored</tool_use_error>
```

> AGENT

让我获取FourOverSix论文的PDF以了解更多细节，并继续阅读Medusa论文。

> TOOL

tool_use mcp__exa__web_fetch_exa
```json
{
  "maxCharacters": 20000,
  "urls": [
    "https://arxiv.org/html/2512.02010"
  ]
}
```

> TOOL

tool_result mcp__exa__web_fetch_exa
```
<persisted-output>
Output too large (62KB). Full output saved to: /user_4813494d/.claude/projects/-user_4813494d-openbmb/76f3fa2c-f12e-4e32-8a58-71a3688d03ea/tool-results/call_f8d4fe184a8f48cab0dc99a4.json

Preview (first 2KB):
[
  {
    "type": "text",
    "text": "# Four Over Six: More Accurate NVFP4 Quantization with Adaptive Block Scaling\nURL: https://arxiv.org/html/2512.02010\n\nFour Over Six: More Accurate NVFP4 Quantization with Adaptive Block Scaling \n\n# Four Over Six: More Accurate NVFP4 Quantization with Adaptive Block Scaling\n\nJack Cook 1 Junxian Guo1 Guangxuan Xiao1 Yujun Lin2 Song Han1,2 https://github.com/mit-han-lab/fouroversix 1Massachusetts Institute of Technology, 2NVIDIA. Correspondence to: Jack Cook, Song Han \n\n###### Abstract\n\nAs large language models have grown larger, interest has grown in low-precision numerical formats such as NVFP4 as a way to improve speed and reduce memory usage. However, quantizing models to NVFP4 remains difficult as the lack of precision generally degrades model performance. In this work, we address this issue with Four Over Six (4/6), a modification to the block-scaled NVFP4 quantization algorithm that yields reduced quantization error. Unlike integer formats, floating point formats have non-uniform step sizes which create larger quantization error on larger values. 4/6 takes advantage of this by adaptively scaling some blocks to smaller FP4 values, making the distribution of representable values more uniform and reducing quantization error for near-maximal values. We show that 4/6 can be implemented efficiently on NVIDIA Blackwell GPUs, resulting in performance gains during both pre-training and inference with minimal computational overhead. In pre-training experiments with the Nemotron 3 Nano 30B-A3B model architecture, we find that 4/6 brings training loss closer to BF16 compared to models trained with current state-of-the-art NVFP4 training recipes.\n\n## 1 Introduction\n\nLarge language models (LLMs) have grown increasingly capable as a direct result of increases to their sizes and the speeds at which they can be trained. As a result, creating methods that enable the training of larger LLMs has been a driving question behind ma
...
</persisted-output>
```

> TOOL

tool_use Bash
```json
{
  "command": "cat /user_4813494d/.claude/projects/-user_4813494d-openbmb/76f3fa2c-f12e-4e32-8a58-71a3688d03ea/tool-results/call_c422462b7fe94f74a6748e63.json | python3 -c \"import json,sys; data=json.load(sys.stdin); text=data[1]['text']; start=text.find('2.1.2 Tree Attention'); print(text[start:start+8000])\"",
  "description": "Read Medusa tree attention section"
}
```

> TOOL

tool_result Bash
```
Exit code 1
Traceback (most recent call last):
  File "<string>", line 1, in <module>
IndexError: list index out of range
```

> TOOL

tool_use Bash
```json
{
  "command": "cat /user_4813494d/.claude/projects/-user_4813494d-openbmb/76f3fa2c-f12e-4e32-8a58-71a3688d03ea/tool-results/call_f8d4fe184a8f48cab0dc99a4.json | python3 -c \"import json,sys; data=json.load(sys.stdin); text=data[0]['text']; print(text[2000:12000])\"",
  "description": "Read FourOverSix HTML paper - authors and intro"
}
```

> TOOL

tool_result Bash
```
ears. An example of this can be seen in numerical precision: it used to be standard to train models using FP32, then FP16 Micikevicius et al. (2018), and now it is standard to keep most or all parameters in BF16 Kalamkar et al. (2019). Some works have successfully trained LLMs while keeping some parameters in FP8, but this remains an active area of study DeepSeek-AI et al. (2025); Meta AI (2025); Mishra et al. (2025).

Going beyond FP8, some works have begun to study the feasibility of training LLMs with FP4 Castro et al. (2025); Chmiel et al. (2025); Tseng et al. (2025); NVIDIA et al. (2025a). However, end-to-end training with FP4 remains difficult, as FP4 is a very coarse datatype that only has 16 values: ±{0,0.5,1,1.5,2,3,4,6}\pm\{0,0.5,1,1.5,2,3,4,6\}. To make up for this lack of precision, block-scaled FP4 formats such as MXFP4 Rouhani et al. (2023) and NVFP4 NVIDIA et al. (2025a) have recently become more popular. Rather than simply quantizing all values in a tensor to the range of FP4 from −6-6 to 66, block-scaled formats allow one FP8 scale factor to be stored for every mm values, 32 and 16 for MXFP4 and NVFP4 respectively, enabling a much larger range of values to be represented across an entire tensor.

Even with this change, using NVFP4 for training remains challenging: the only hardware accelerators that currently support NVFP4, NVIDIA Blackwell GPUs, require that both operands of any matrix multiplication are quantized to NVFP4. As a result, for efficient model training, weights, activations, and gradients must all be quantized to NVFP4. In theory, this should deliver two key benefits: speed improvements due to the 4-6x faster matrix multiplication operations compared to BF16 NVIDIA et al. (2025a), and a natively quantized NVFP4 model. In practice, however, current state-of-the-art NVFP4 training recipes require operations that introduce more computational overhead and fail to deliver a natively quantized model. These include the random Hadamard transform (RHT), stochastic rounding (SR), keeping some layers in high precision, and “healing” the model by switching to high precision weights, activations, and gradients near the end of training Chmiel et al. (2025); NVIDIA et al. (2025a); Wang et al. (2025); Castro et al. (2025). Furthermore, this added overhead must be carefully managed: if too much overhead is introduced, it becomes faster to train models using more accurate FP8 formats. To make NVFP4 training viable, more lightweight operations that improve numerical accuracy are necessary.

(a) Quantization error relative to the largest value in a block of values quantized to NVFP4 when the largest value in the block is scaled to six.

(b) Quantization error relative to the largest value in the block when the block’s largest value is instead scaled to four.

Figure 1: In standard NVFP4 quantization (left), using the full range of FP4 values from 0 to 6 means that it is impossible to represent values between 66.6% and 100% of the magnitude of the largest value in a block. By instead scaling some blocks to a maximum value of 4, it becomes possible to represent values that are 75% of the largest value in a block, reducing worst-case quantization error for large values.

| [10, 20, 30, 40] |
| --- |
| NVFP4 (M=6M=6) | 6.5 ×\times [1.5, 3, 4, 6] |
| Mean Squared Error | 4.33 |
| NVFP4 (M=4M=4) | 10 ×\times [1, 2, 3, 4] |
| Mean Squared Error | 0 |

Table 1: NVFP4 quantization using Equation˜3 with the block’s largest value scaled to M=4M=4 and M=6M=6. Blocks such as this one, often those with values close to 75% of the block’s largest value, may be represented with less error when scaled to 4. See Table˜2 for details.

In this work, we introduce Four Over Six (4/6), a change to the NVFP4 block-scaled quantization algorithm that improves its representation of near-maximal values in each block. During quantization, it is standard to scale high-precision values to the full range of values that can be represented by the low-precision numerical format Nagel et al. (2021). However, when this is done with FP4, this results in large amounts of quantization error for near-maximal values (Figure˜1(a)). If values are instead scaled to the range (−4,4)(-4,4), the distribution of representable values becomes more uniform, reducing worst-case quantization error (Figure˜1(b)). An example can be seen in Table˜1. When the values [10, 20, 30, 40] are quantized to NVFP4, 30 is scaled to 306.5=4.62\frac{30}{6.5}=4.62, and then rounded down to 4, the nearest FP4 value, introducing a relative error of 13.4%. If this block is instead scaled such that the largest value is 4, 30 would instead be scaled to 3010=3\frac{30}{10}=3, which can be represented in FP4 with no error.

We find that for many blocks in weight, gradient, and activation tensors during both pre-training and post-training quantization (PTQ), scaling to 4 rather than 6 introduces less error, leading to more accurate models. Crucially, we find that this can be implemented efficiently in an online fashion, adding less than 15% overhead to the NVFP4 quantization operation. During pre-training, we find that 4/6 improves the performance of current state-of-the-art NVFP4 pre-training recipes, bringing loss closer to high-precision baselines. Furthermore, when used during post-training quantization, we find that 4/6 can often improve the accuracy of existing methods such as GPTQ Frantar et al. (2023), AWQ Lin et al. (2024), and SmoothQuant Xiao et al. (2024a). We additionally release quantization and matrix multiplication kernels on GitHub.

## 2 Problems with NVFP4 Quantization

### 2.1 NVFP4 Overview

NVFP4 is a block-scaled quantization format that stores values in FP4 E2M1, with an FP8 E4M3 scale factor Δi\Delta_{i} for every 16 values, and a tensor-wide FP32 scale factor α\alpha. This can be expressed as follows, where 𝐗\mathbf{X} is the high-precision tensor, 𝐗¯\mathbf{\bar{X}} is its quantized representation, MFP4M^{\text{FP4}} and MFP8M^{\text{FP8}} are the largest values that can be represented in FP4 and FP8 E4M3, 6 and 448 respectively, and ⌈⋅⌋\lceil\cdot\rfloor is the rounding function.111FP32 and FP8 casting operations are not described mathematically for brevity. Sample calculations can be found in lines 1-4 of Table 2.

| αFP32\displaystyle\alpha^{\text{FP32}} | =max​(|𝐗|)MFP4×MFP8\displaystyle=\frac{\text{max}(|\mathbf{X}|)}{M^{\text{FP4}}\times M^{\text{FP8}}} | (1) |
| --- | --- | --- |
| ΔiFP8\displaystyle\Delta^{\text{FP8}}_{i} | =max​(|𝐗16​i​…​16​(i+1)|)α​MFP4\displaystyle=\frac{\text{max}(|\mathbf{X}_{16i...16(i+1)}|)}{\alpha M^{\text{FP4}}} | (2) |
| 𝐗¯FP4\displaystyle\mathbf{\bar{X}}^{\text{FP4}} | ={12⌈2​𝐗α​Δ⌋,|𝐗α​Δ|<2⌈𝐗α​Δ⌋,|𝐗α​Δ|<42⌈𝐗2​α​Δ⌋,|𝐗α​Δ|≤6\displaystyle=\begin{cases}\frac{1}{2}\lceil\frac{2\mathbf{X}}{\alpha\Delta}\rfloor,&|\frac{\mathbf{X}}{\alpha\Delta}|<2\\ \lceil\frac{\mathbf{X}}{\alpha\Delta}\rfloor,&|\frac{\mathbf{X}}{\alpha\Delta}|<4\\ 2\lceil\frac{\mathbf{X}}{2\alpha\Delta}\rfloor,&|\frac{\mathbf{X}}{\alpha\Delta}|\leq 6\end{cases} | (3) |

Unlike integer formats, floating point formats such as FP4 have dynamic step sizes: 0.5 between 0 and 2, 1 between 2 and 4, and 2 between 4 and 6, as shown in Figure˜1(a). This enables them to represent a wider range of values, making them better at representing weights, activations, and gradients Chen et al. (2025); Liu et al. (2023). For example, the range of representable values, which is the largest value divided by the smallest positive value, for FP4 is 12 (60.5\frac{6}{0.5}), compared to just 7 (71\frac{7}{1}) for INT4.

Note that Equations˜2 and 3 involve casting values to specific numerical precisions. These are required to benefit from hardware support, but they are also where quantization error is introduced, as information is lost when rounding to the nearest representable values. In summary, there are two sources of error in NVFP4 quantization:

1.

FP8 block-level scale factors: Each scale factor contains some quantization error due to the limited precision offered by E4M3. If a scale factor is rounded up or down from its high-precision counterpart, it affects all of the values in its block.

2.

FP4 values: Individual values may be rounded up or down to one of the eight possible FP4 values shown in Figure˜1(a).

1. 7 Conclusion

### 2.2 NVFP4 Error Comes From Rounding Near-Maximal Values

To better understand the effects of NVFP4 quantization on LLM performance, it would be helpful to understand the downstream effects of each type of NVFP4 quantization error. In Figure˜2(a), we show how the performance of Llama-3.1-8B is affected when quantized to NVFP4, and when each type of error is mitigated by keeping either scale factors or values in high precision. Following from standard practice with PTQ, we keep sensitive layers and operations, including embedding layers, the LM head, and Attention calculations in high precision. We find that error from scale factors has a minimal effect on model performance, and that NVFP4 performance degradation can be entirely attributed to error introduced by casting values to FP4. When this source of error is mitigated, downstream performance recovers completely.

(a) Scale Factor Quantization Error has Minimal Effects on Performance. NVFP4 quantization alongside simulated versions of NVFP4 where either values (𝐗¯\mathbf{\bar{X}}) or scale factors (Δ\Delta) are kept in high precision (HP). Error from scale factors contributes relatively little to performance loss, but if values are stored in high precision, performance can recover completely.

(b) NVFP4 Error Comes from Rounding Near-Maximal Values. Simulated quantization where only values with a magnitude ≥x\geq x are quantized to NVFP4. x=0x=0, where all values are kept in high precision, is equivalent to BF16, and x=6x=6 is equivalent to NVFP4. The steeper slope x=5x=5 indicates that error on values quantized around 5, where FP4 has no representable values, are primarily responsible for NVF
```

> TOOL

tool_use Bash
```json
{
  "command": "cat /user_4813494d/.claude/projects/-user_4813494d-openbmb/76f3fa2c-f12e-4e32-8a58-71a3688d03ea/tool-results/call_f8d4fe184a8f48cab0dc99a4.json | python3 -c \"import json,sys; data=json.load(sys.stdin); text=data[0]['text']; print(text[12000:24000])\"",
  "description": "Read FourOverSix HTML paper - method section"
}
```

> TOOL

tool_result Bash
```
P4’s poor performance.

Figure 2: Simulated NVFP4 quantization with Llama-3.1-8B evaluated on WikiText-2 word perplexity. To improve NVFP4 performance, we find that we should focus on improving the representation of specific values in each block.

Next, we simulate how model performance is affected when only some values are casted to FP4. Specifically, we only cast scaled values to FP4 if their absolute value is above a threshold α\alpha, measure downstream model performance, and plot our results in Figure˜2(b). We find that performance degrades steadily up until values greater than 4 are quantized, and then rapidly degrades after that, indicating that error due to rounding values around 5 is most responsible for performance degradation. Smaller spikes can also be observed at scaled values around 2.5 and 3.5. This finding aligns with Figure˜1(a), which shows that these three values suffer from large amounts of error once quantized to FP4.

This has a large impact on model training: in order to benefit from hardware support, all operands of an NVFP4 matrix multiplication must be quantized to NVFP4. In Figure˜3, we show the computational flow of an NVFP4 linear layer, in which weights, activations, and gradients during training are all quantized to NVFP4 before being used. Following from recent work on training with FP4 NVIDIA et al. (2025a); Chmiel et al. (2025); Tseng et al. (2025); Castro et al. (2025), we perform stochastic rounding on gradients to reduce quantization bias, and we perform a random Hadamard transform on the inputs to the weight gradient calculation NVIDIA et al. (2025a). Our experiments above indicate that near-maximal values are responsible for performance degradation during post-training quantization, but it is likely that this explains much of the performance loss during training as well.

Figure 3: Computational flow of an NVFP4 quantized linear layer trained with Four Over Six. All matrix multiplications (FPROP, DGRAD, WGRAD) are performed in NVFP4, while model weights are stored in FP32, and activations and gradients are stored in BF16. Q(4/6) denotes our method where blocks are scaled to either 4 or 6 based on the distribution of values. SR denotes Stochastic Rounding, and RHT denotes Random Hadamard Transform. Blue paths represent FP32 data flow; orange paths represent BF16; green paths represent NVFP4.

## 3 Adaptive Block Scaling with Four Over Six

In the previous section, we found that in NVFP4 quantization, scaled values around 5 in weights and activations are responsible for a large portion of the performance degradation in quantized models, since these values cannot be represented accurately by FP4. To improve the representation of these values, in this section we introduce Four Over Six (4/6), a method for improving the representation of these near-maximal values in NVFP4 blocks.

Rather than scaling all blocks by the same value MFP4M^{\text{FP4}} as is done in Equation˜3, we find that changing this scale for some blocks can improve their representation of near-maximal values. This value dictates the range to which values are quantized to: by setting it to 6, values are spread out over the range of all FP4 values from -6 to 6. However, we find that for some blocks, it is better to instead set this value to 4, spreading out values over the range of -4 to 4. By giving up the ability to represent -6 and 6, we allow NVFP4 to represent near-maximal values more accurately. For example, when scaling to 6, the quantized value 4 represents 66.6% of the block’s maximum value, and no values can be represented between 66.6% and 100%. When a block is instead scaled to 4, the quantized value 3 represents 75% of the block’s maximum value, offering a better ability to represent values in some blocks, such as the samples shown in Table˜2. Other possible scales, such as 2 or 3, only offer subsets of values that can be represented with 4 or 6.

| Pseudocode | 𝐗\mathbf{X} = [10, 20, 30, 40] | 𝐗\mathbf{X} = [15, 30, 120, 180] |
| --- | --- | --- |
| 1 | Δ(6)\Delta^{(6)} = max(|𝐗||\mathbf{X}|) ÷\div 6 | 6.67 | 30 |
| 2 | Δ(6)\Delta^{(6)} = fp8_e4m3(Δ(6)\Delta^{(6)}) | 6.5 | 30 |
| 3 | 𝐗¯i(6)\mathbf{\bar{X}}_{i}^{(6)} = 𝐗i\mathbf{X}_{i} ÷\div Δ(6)\Delta^{(6)} | [1.54, 3.08, 4.62, 6.15] | [0.5, 1, 4, 6] |
| 4 | 𝐗¯i(6)\mathbf{\bar{X}}_{i}^{(6)} = fp4_e2m1(𝐗¯i(6)\mathbf{\bar{X}}_{i}^{(6)}) | [1.5, 3, 4, 6] | [0.5, 1, 4, 6] |
| 5 | 𝐃i(6)\mathbf{D}_{i}^{(6)} = 𝐗¯i(6)\mathbf{\bar{X}}_{i}^{(6)} ×\times Δ(6)\Delta^{(6)} | [9.75, 19.5, 26, 39] | [15, 30, 120, 180] |
| 6 | E(6)\text{E}^{(6)} = 1n​∑in(𝐃i(6)−𝐗i)2\frac{1}{n}\sum_{i}^{n}(\mathbf{D}_{i}^{(6)}-\mathbf{X}_{i})^{2} | 4.33 | 0 |
| 7 | Δ(4)\Delta^{(4)} = max(|𝐗||\mathbf{X}|) ÷\div 4 | 10 | 45 |
| 8 | Δ(4)\Delta^{(4)} = fp8_e4m3(Δ(4)\Delta^{(4)}) | 10 | 44 |
| 9 | 𝐗¯i(4)\mathbf{\bar{X}}_{i}^{(4)} = 𝐗i\mathbf{X}_{i} ÷\div Δ(4)\Delta^{(4)} | [1, 2, 3, 4] | [0.34, 0.68, 2.73, 4.09] |
| 10 | 𝐗¯i(4)\mathbf{\bar{X}}_{i}^{(4)} = fp4_e2m1(𝐗¯i(4)\mathbf{\bar{X}}_{i}^{(4)}) | [1, 2, 3, 4] | [0.5, 0.5, 3, 4] |
| 11 | 𝐃i(4)\mathbf{D}_{i}^{(4)} = 𝐗¯i(4)\mathbf{\bar{X}}_{i}^{(4)} ×\times Δ(4)\Delta^{(4)} | [10, 20, 30, 40] | [22, 22, 136, 176] |
| 12 | E(4)\text{E}^{(4)} = 1n​∑in(𝐃i(4)−𝐗i)2\frac{1}{n}\sum_{i}^{n}(\mathbf{D}_{i}^{(4)}-\mathbf{X}_{i})^{2} | 0 | 96.25 |
| 13 | Δ\Delta = Δ(4)\Delta^{(4)} if E(4)\text{E}^{(4)} < E(6)\text{E}^{(6)} else Δ(6)\Delta^{(6)} | 10 | 30 |
| 14 | 𝐗¯i\mathbf{\bar{X}}_{i} = 𝐗¯i(4)\mathbf{\bar{X}}_{i}^{(4)} if E(4)\text{E}^{(4)} < E(6)\text{E}^{(6)} else 𝐗¯i(6)\mathbf{\bar{X}}_{i}^{(6)} | [1, 2, 3, 4] | [0.5, 1, 4, 6] |

Table 2: We highlight how for these two sample blocks, our procedure may choose to scale the block using either 4 or 6. The standard NVFP4 quantization algorithm ends on line 4, returning Δ(6)\Delta^{(6)} and 𝐗¯(6)\mathbf{\bar{X}}^{(6)}. Operations that introduce error, and values that suffer from this error, are highlighted in orange.

### 3.1 Scale Selection Rules

| Llama 3 | Qwen 3 |
| --- | --- |
| 1B | 8B | 70B | 1.7B | 8B | 32B |
| BF16 | 11.98 | 7.54 | 2.86 | 21.06 | 12.22 | 9.34 |
| MXFP4 | 17.67 | 9.66 | 5.53 | 26.95 | 14.08 | 11.92 |
| NVFP4 (M=6) | 14.27 | 8.43 | 4.00 | 23.06 | 12.68 | 9.85 |
| NVFP4 (M=4) | 14.75 | 8.63 | 4.48 | 24.43 | 12.98 | 10.57 |

Table 3: Scaling Blocks to 4 Is Not Always Better. WikiText-2 word perplexity for models quantized with W4A4 PTQ. MXFP4 and baseline NVFP4 quantization (M=6M=6) suffer from performance degradation. Scaling all blocks with M=4M=4 further degrades overall performance.

| WikiText-2 Word PPL | C4 Word PPL |
| --- | --- |
| Llama 3 | Qwen 3 | Llama 3 | Qwen 3 |
| 1B | 8B | 70B | 1.7B | 8B | 32B | 1B | 8B | 70B | 1.7B | 8B | 32B |
| BF16 | 11.98 | 7.54 | 2.86 | 21.06 | 12.22 | 9.34 | 28.54 | 18.08 | 12.52 | 58.76 | 36.35 | 26.12 |
| RTN | 14.27 | 8.43 | 4.00 | 23.06 | 12.68 | 9.85 | 36.19 | 20.83 | 14.16 | 65.54 | 37.91 | 27.54 |
| + 4/6 (MSE) | 13.84 | 8.30 | 3.83 | 23.60 | 12.56 | 9.84 | 35.09 | 20.48 | 13.95 | 66.32 | 37.32 | 27.67 |
| + 4/6 (L1) | 13.94 | 8.33 | 3.86 | 23.45 | 12.63 | 9.82 | 35.32 | 20.56 | 13.94 | 66.41 | 37.53 | 27.56 |
| + 4/6 (Abs-Max) | 14.06 | 8.36 | 4.39 | 23.32 | 12.86 | 9.97 | 35.43 | 20.68 | 14.31 | 65.39 | 37.93 | 28.21 |

Table 4: Selecting Block Scales Using MSE Works Best Overall. After a block is quantized to NVFP4 with N=4N=4 and N=6N=6, there are several ways to pick which quantized version is better. We find that using mean squared quantization error generally works best.

Scaling blocks to 4 can reduce quantization error on some blocks, but not on all blocks. This is demonstrated by Table˜2, in which one block is better represented when scaled to 6, and another block is better represented when scaled to 4. In Table˜3, we evaluate several Llama Grattafiori et al. (2024) and Qwen Yang et al. (2025) models when quantized to NVFP4 with a block scale of 4, and with the standard block scale of 6. We find that despite its ability to represent large values more accurately, scaling all blocks to 4 results in worse performance than scaling all blocks to 6 as is done in standard NVFP4 quantization, likely due to the significantly larger range of values that can be expressed with a scale of 6 (60.5\frac{6}{0.5} vs. 40.5\frac{4}{0.5}, a 50% increase). Instead, blocks need to be scaled adaptively.

We find that it is difficult to identify which scale is best without access to a block’s quantized values. To implement Four Over Six, we quantize each block twice: once with a scale of 6, and again with a scale of 4, and then compare the quantized values 𝐗¯(4)\bar{\mathbf{X}}^{(4)} and 𝐗¯(6)\bar{\mathbf{X}}^{(6)} to the original values 𝐗\mathbf{X}. With access to these values, we implement three different scale selection rules: selecting the quantized values with the smallest maximum error (i.e., maxi⁡(𝐗¯i(4)−𝐗i)\max_{i}(\mathbf{\bar{X}}^{(4)}_{i}-\mathbf{X}_{i}) vs. maxi⁡(𝐗¯i(6)−𝐗i)\max_{i}(\mathbf{\bar{X}}^{(6)}_{i}-\mathbf{X}_{i})), with the lower L1 norm of errors, and with the lower mean squared error (MSE). In Table˜4, we show the effects of these three rules on model performance. We find that each rule sometimes outperforms standard NVFP4 quantization, but that selecting a block’s scale based on quantization MSE works best in most cases. In the remainder of this work, we adopt the MSE scale selection rule.

Finally, we make one modification to the computation of the tensor scale α\alpha (Equation˜1) when quantizing to NVFP4 with 4/6. When MFP4×MFP8M^{\text{FP4}}\times M^{\text{FP8}} is used to compute the tensor scale, it ensures that all quantized values will be less than 6×4486\times 448. However, this makes it impossible to select a scale of 4 for the blocks that contain a tensor’s largest values, because the block’s scale would need to be 448×64=672448\times\frac{6}{4}=672, which would overflow since 448 is the maximum value that can be represented by E4M3. As a result, when computing the tensor scale, we replace MFP8M^{\text{FP8}} to 256 in Equation˜1, since 256 is the largest E4M3 that can be multiplied by 64\frac{6}{4} and represented without error in E4M3, as 384.

### 3.2 Implementation

We find that Four Over Six can be implemented efficiently using PTX instructions supported by NVIDIA Blackwell GPUs. Specifically, we use the cvt family of instructions to perform quantization into the packed FP4 format, and then also dequantization from FP4 to FP16, which is needed to calculate error as is done in lines 6 and 12 of Table˜2. To maintain high performance, we implement Four Over Six in a CUDA kernel where all quantized values, dequantized values, and errors are kept in the register file. As a result, we observe that the overhead introduced by Four Over Six is under 15%, and we expect that we will be able to reduce this overhead further with more optimization.

## 4 Evaluation

In this section, we evaluate how Four Over Six affects the performance of models quantized to NVFP4 during pre-training and post-training quantization. We find that the addition of Four Over Six leads to improved performance during pre-training, and improves downstream performance of already-trained Llama Grattafiori et al. (2024) and Qwen Yang et al. (2025) models on a wide variety of tasks.

### 4.1 Pre-Training

Figure 4: Four Over Six Can Improve NVFP4 Performance During Pre-Training. Training loss curves comparing BF16, NVFP4, and NVFP4 with 4/6 for our Mixture-of-Experts hybrid Mamba-Transformer model architecture. Adding 4/6 keeps NVFP4 training loss closer to BF16.

Figure˜4 shows our main results when 4/6 is applied during pre-training. We find that compared to the current state-of-the-art NVFP4 training recipe NVIDIA et al. (2025a), 4/6 brings training loss 22.3% closer to BF16 performance for our model architecture and training setup. We adopt the Nemotron 3 Nano architecture NVIDIA (2025), which has 52 blocks: 6 Self-Attention Vaswani et al. (2023), 23 Mixture-of-Experts (MoE) NVIDIA et al. (2025c), a
```

> TOOL

tool_use Bash
```json
{
  "command": "cat /user_4813494d/.claude/projects/-user_4813494d-openbmb/76f3fa2c-f12e-4e32-8a58-71a3688d03ea/tool-results/call_f8d4fe184a8f48cab0dc99a4.json | python3 -c \"import json,sys; data=json.load(sys.stdin); text=data[0]['text']; print(text[24000:40000])\"",
  "description": "Read FourOverSix HTML paper - experiments and results"
}
```

> TOOL

tool_result Bash
```
nd 23 Mamba-2 Dao and Gu (2024) blocks. The model has 30 billion total parameters, 3 billion of which are active at a time. The model’s hidden dimension is 2688, and the Grouped-Query Attention layers have 32 query heads and 2 key-value heads. MoE blocks have 128 experts, 6 of which are activated per forward pass, and 2 of which are shared, use squared ReLU activations, and have a hidden size of 1856.

We train our models on a high-quality curated and synthetic data distribution of 1 trillion tokens based on NVIDIA et al. (2025b) using the AdamW optimizer Loshchilov and Hutter (2019) with β1=0.9\beta_{1}=0.9, β2=0.95\beta_{2}=0.95, weight decay of 0.10.1, gradient clipping at 1.01.0, a sequence length of 8192, and a global batch size of 3072. We use a WSD schedule with a constant learning rate of 10−310^{-3} which decays to 10−510^{-5} over the last 20% of training. Models are trained using 384 B200 180GB GPUs.

Following from the current state-of-the-art NVFP4 pre-training recipe NVIDIA et al. (2025a), we perform stochastic rounding on gradients, apply a random Hadamard transform to both inputs of the weight gradient calculation, and perform 2D block quantization on weight matrices, as outlined in Figure˜3. When performing stochastic rounding, we follow the same procedure as for non-stochastic rounding, which involves quantizing stochastically using scales of 4 and 6 and selecting the result with less error. All NVFP4 matrix multiplications accumulate in FP32 and output in BF16, and model weights are stored in FP32. Following from NVIDIA et al. (2025a), Attention components, the output projection head, normalization layers, and non-linearities are kept in high precision, either BF16 or FP32. We also keep the output projection layer of Mamba-2 blocks in MXFP8.

### 4.2 Post-Training Quantization

We also evaluate the ability of 4/6 to improve NVFP4 post-training quantization (PTQ) accuracy. While 4/6 can be used on its own, 4/6 is a general method that modifies the underlying NVFP4 quantization algorithm, allowing it to be easily combined with existing PTQ methods such as GPTQ Frantar et al. (2023), AWQ Lin et al. (2024), and SmoothQuant Xiao et al. (2024a). When evaluating Llama 3 and Qwen3 models on WikiText-2 and C4 word perplexity, we find that 4/6 improves performance in the vast majority of cases, as shown in Table˜5. When combined with AWQ and SmoothQuant, 4/6 improves performance on these metrics for all models tested, bringing word perplexity 19.9% and 5.3% closer to BF16 model performance respectively. We find that 4/6 reduces the performance of models quantized with GPTQ, increasing the gap between NVFP4 and BF16 word perplexity by an average of 34.6%. AWQ with 4/6 performs best overall, with an average WikiText-2 word perplexity of 11.58 and an average C4 word perplexity of 32.36 across all models.

To evaluate GPTQ, we use the FP-Quant implementation available on GitHub Egiazarian et al. (2025) and load quantized models with either the built-in FP4 linear layers or our version which performs quantization with 4/6. Modifying the GPTQ optimization process in a way that incorporates Four Over Six is likely to deliver performance improvements in future work. To evaluate AWQ and SmoothQuant, we substitute our linear layer during optimization, enabling these algorithms to make more accurate measurements of the effects of outlier smoothing and clipping. Results using GPTQ for Llama-3.1-70B are omitted due to memory constraints, and results for SmoothQuant for Llama-3.1-70B and Qwen3-32B are omitted due to time and resource constraints.

While perplexity is often considered a more stable metric for evaluating quantized models Dettmers and Zettlemoyer (2023), we also evaluate these quantized models on several downstream tasks including BoolQ Clark et al. (2019), ARC-Easy and ARC-Challenge Clark et al. (2018), and HellaSwag Zellers et al. (2019). Following standard practice, we report normalized accuracy for ARC-Easy, ARC-Challenge, and HellaSwag in order to reduce differences due to tokenization when comparing across different models. We find that 4/6 improves performance across most PTQ methods and tasks, with average task performance improved in nearly all cases, as shown in Table˜6 for Llama 3 models and Table˜7 for Qwen3 models.

| WikiText-2 Word PPL (↓\downarrow) | C4 Word PPL (↓\downarrow) |
| --- | --- |
| Llama 3 | Qwen 3 | Llama 3 | Qwen 3 |
| 1B | 8B | 70B | 1.7B | 8B | 32B | 1B | 8B | 70B | 1.7B | 8B | 32B |
| BF16 | 11.98 | 7.54 | 2.86 | 21.06 | 12.22 | 9.34 | 28.54 | 18.08 | 12.52 | 58.76 | 36.35 | 26.12 |
| RTN | 14.27 | 8.43 | 4.00 | 23.06 | 12.68 | 9.85 | 36.19 | 20.83 | 14.16 | 65.54 | 37.91 | 27.54 |
| + 4/6 | 13.84 | 8.30 | 3.83 | 23.60 | 12.56 | 9.84 | 35.09 | 20.48 | 13.95 | 66.32 | 37.32 | 27.67 |
| GPTQ | 13.73 | 8.33 | – | 21.48 | 12.50 | 9.67 | 35.65 | 20.98 | – | 63.33 | 37.14 | 27.17 |
| + 4/6 | 13.67 | 8.30 | – | 22.70 | 12.65 | 9.66 | 35.55 | 20.89 | – | 63.81 | 37.25 | 27.09 |
| AWQ | 14.04 | 8.33 | 3.86 | 22.20 | 12.68 | 9.69 | 35.56 | 20.69 | 13.58 | 62.50 | 37.51 | 27.09 |
| + 4/6 | 13.67 | 8.24 | 3.71 | 21.67 | 12.57 | 9.64 | 34.55 | 20.34 | 13.41 | 61.78 | 37.14 | 26.95 |
| SmoothQuant | 14.17 | 8.38 | 3.86 | 21.99 | 12.64 | 9.65 | 35.61 | 20.80 | – | 62.33 | 37.67 | – |
| + 4/6 | 14.03 | 8.32 | 3.80 | 21.97 | 12.62 | 9.63 | 35.20 | 20.61 | – | 62.19 | 37.62 | – |

Table 5: 4/6 Can Improve the Performance of Existing PTQ Methods. We find that 4/6 uniformly improves perplexity metrics when combined with AWQ and SmoothQuant, and can also improve the performance of RTN (round-to-nearest) quantization and GPTQ in most cases.

| BoolQ (↑\uparrow) | Arc-E (↑\uparrow) | Arc-C (↑\uparrow) | HellaSwag (↑\uparrow) | Average (↑\uparrow) |
| --- | --- | --- | --- | --- |
| 1B | 8B | 1B | 8B | 1B | 8B | 1B | 8B | 1B | 8B |
| BF16 | 63.7 | 83.2 | 61.8 | 82.5 | 37.0 | 55.0 | 64.3 | 79.3 | 56.7 | 75.0 |
| RTN | 58.6 | 80.2 | 57.3 | 77.5 | 34.3 | 52.5 | 60.0 | 77.7 | 52.3 | 72.0 |
| + 4/6 | 57.7 | 80.9 | 56.9 | 80.2 | 33.0 | 52.6 | 60.0 | 78.0 | 51.9 | 72.2 |
| GPTQ | 61.1 | 80.3 | 57.3 | 78.3 | 33.1 | 53.9 | 60.6 | 77.0 | 53.0 | 72.4 |
| + 4/6 | 60.2 | 81.4 | 57.5 | 78.7 | 33.8 | 53.0 | 60.7 | 77.4 | 53.1 | 72.6 |
| AWQ | 59.8 | 81.3 | 58.0 | 78.4 | 34.2 | 51.7 | 60.9 | 77.5 | 53.2 | 72.2 |
| + 4/6 | 61.0 | 80.4 | 58.8 | 80.2 | 35.5 | 53.6 | 61.2 | 78.2 | 54.1 | 73.1 |
| SmoothQuant | 61.1 | 81.1 | 57.4 | 77.6 | 35.5 | 52.7 | 60.7 | 77.6 | 53.7 | 72.3 |
| + 4/6 | 61.6 | 80.4 | 58.0 | 78.6 | 35.6 | 52.2 | 61.6 | 80.4 | 54.2 | 72.9 |

Table 6: Downstream task performance of Llama-3.2-1B and Llama-3.1-8B when quantized using various PTQ methods and 4/6. 4/6 improves average task performance in nearly all cases.

| BoolQ (↑\uparrow) | Arc-E (↑\uparrow) | Arc-C (↑\uparrow) | HellaSwag (↑\uparrow) | Average (↑\uparrow) |
| --- | --- | --- | --- | --- |
| 1.7B | 8B | 1.7B | 8B | 1.7B | 8B | 1.7B | 8B | 1.7B | 8B |
| BF16 | 77.6 | 86.6 | 70.2 | 80.9 | 43.0 | 56.7 | 60.4 | 74.9 | 62.8 | 74.8 |
| RTN | 73.1 | 85.5 | 59.9 | 78.6 | 35.3 | 54.1 | 58.0 | 73.2 | 56.6 | 72.3 |
| + 4/6 | 76.3 | 85.8 | 66.3 | 78.5 | 38.7 | 53.7 | 58.0 | 73.7 | 59.8 | 72.9 |
| GPTQ | 74.6 | 86.4 | 60.9 | 79.8 | 36.3 | 54.3 | 57.2 | 73.2 | 57.3 | 73.4 |
| + 4/6 | 73.8 | 86.5 | 59.8 | 80.8 | 37.3 | 54.9 | 57.1 | 73.2 | 57.0 | 73.9 |
| AWQ | 72.8 | 86.5 | 58.0 | 78.4 | 36.3 | 55.2 | 57.8 | 73.6 | 56.2 | 73.4 |
| + 4/6 | 75.9 | 86.5 | 63.8 | 78.1 | 39.2 | 55.8 | 57.9 | 73.6 | 59.2 | 73.5 |
| SmoothQuant | 74.8 | 86.4 | 61.2 | 78.1 | 37.2 | 55.2 | 57.8 | 73.3 | 57.8 | 73.2 |
| + 4/6 | 74.5 | 85.9 | 61.7 | 78.4 | 40.4 | 54.8 | 57.9 | 73.5 | 58.6 | 73.2 |

Table 7: Downstream task performance of Qwen3-1.7B and Qwen3-8B when quantized using various PTQ methods and 4/6. 4/6 improves or matches average task performance in nearly all cases.

## 5 Discussion

### 5.1 Outliers

Modern training techniques often aim to mitigate outliers in weights and activations, since they can often degrade model performance, introduce instability during training, and make models harder to compress An et al. (2025); Xiao et al. (2024b); Bondarenko et al. (2023); Nrusimha et al. (2024). However, by introducing a separate scale factor for every mm values, block-scaled floating point formats such as MXFP4 (m=32m=32) and NVFP4 (m=16m=16) are able to represent outliers with almost no error. As a result, most of the quantization error in these formats comes from near-maximal values, as demonstrated in Section˜2.2. While we are able to adapt NVFP4 to represent these values with less error, some models with very few outliers may benefit further from formats with even more uniform quantization error, such as INT4 Chen et al. (2025). However, NVFP4, especially once combined with 4/6, has empirically proven better at quantizing models in most real-world cases.

### 5.2 Limitations

While Four Over Six could theoretically be applied to other block-scaled low-precision FP4 formats, we focus on NVFP4 in this work because Four Over Six would not work with MXFP4. Note that the ability to scale blocks to either 4 or 6 requires a minimum amount of precision to be present in scale factors: a block scaled to 4 requires a scale factor that is 50% larger than a block scaled to 6. This is possible to represent with FP8 E4M3, the numerical format used by NVFP4 to represent scale factors. However, this is not possible in MXFP4 Rouhani et al. (2023) scale factors, which are saved in FP8 E8M0, a format in which each representable value is a factor of 2 away from the previous or next representable value. Future block-scaled floating point formats may benefit from 4/6-style Adaptive Block Scaling, however the benefits fade quickly as the precision used to store values increases.

## 6 Related Work

Quantization has seen widespread adoption in LLMs due to its ability to reduce model size and accelerate inference Han et al. (2016). Most methods aim to mitigate outliers in order to reduce the dynamic range of tensors that need to be quantized. This is often done with per-channel smoothing factors Lin et al. (2024); Xiao et al. (2024a), second-order information Frantar et al. (2023), or rotations Liu et al. (2025); Ashkboos et al. (2024). Most of these works were developed with older numerical formats in mind, such as INT4, which no longer has dedicated support on newer NVIDIA GPUs.

Block-scaled quantization formats have grown in popularity due to the increased precision they provide. For example, the smallest nonzero value that can be represented in FP4 is 0.5, and the largest is 6, meaning a tensor quantized to FP4 should ideally have a dynamic range of 12, far too small for many practical applications. Block-scaled formats such as MXFP4 Rouhani et al. (2023) and NVFP4 NVIDIA et al. (2025a), on the other hand, store a higher-precision scaling factor alongside blocks of FP4 values, allowing for different blocks in the same tensor to have vastly different scales. In the case of MXFP4, every 32 FP4 values are accompanied by an 8-bit E8M0 scaling factor, and in the case of NVFP4, every 16 FP4 values are accompanied by an 8-bit E4M3 scaling factor. Crucially, both of these methods have dedicated hardware support in the most recently-released NVIDIA Blackwell GPUs, offering up to 2x speed improvements over FP8 inputs, and 4x speed improvements over BF16/FP16 inputs on NVIDIA B200 GPUs. However, despite the benefits these formats provide, maintaining model performance after quantization remains challenging.

Low-precision training with MXFP4 and NVFP4 remains a largely unsolved problem. In theory, FP4 training should provide two primary benefits: improved training speed, and a natively-quantized FP4 model. In practice, achieving these goals is difficult. Many works use stochastic rounding, the random Hadamard transform, or both to mitigate the effects of outliers Tseng et al. (2025); NVIDIA et al. (2025a); Castro et al. (2025); Wang et al. (2025). However, each of these operations, in addition to the process of computing scale factors, adds computational overhead. If the overhead becomes too large, training with block-scaled FP4 formats becomes pointless, as FP8 formats are generally far more accurate and are only 2x slower on NVIDIA B200 GPUs. Furthermore, many FP4 training works require “healing” the model by training in high-precision for some time afterward, adding to the time cost, and resulting in a high-precision model Chmiel et al. (2025); NVIDIA et al. (2025a).

Post-training quantization with MXFP4 and NVFP4 is easier, since models can be calibrated offline to recover accuracy. SpinQuant Liu et al. (2025) and QuaRot Ashkboos et al. (2024) rotate model weights to make them easier to quantize. AWQ Lin et al. (2024), GPTQ Frantar et al. (2023), SmoothQuant Xiao et al. (2024a), and SVDQuant Li et al. (2025) rely on offline calibration. However, quantizing to MXFP4 and NVFP4 with these methods still generally fails to recover full high-precision performance, as shown in Table˜3.

## 7 Conclusion

In this work, we introduced Four Over Six, a change to the NVFP4 quantization algorithm that improves quantization accuracy while introducing minimal overhead. We find that 4/6 improves pre-training performance compared to existing state-of-the-art NVFP4 pre-training recipes, bringing performance closer to high-precision baselines. When added to existing PTQ methods, we find that 4/6 leads to broad performance improvements across a variety of tasks. We hope this work inspires future work in NVFP4 quantization.

## Acknowledgments and Disclosure of Funding

We thank Modal and NVIDIA for access to the HGX-B200 and NVL-72 nodes needed to run our experiments. This research is partially supported by Amazon, Hyundai Motor Company, the MIT AI Hardware Program, the MIT-IBM Watson AI Lab, the National Science Foundation, and the National Science Foundation Graduate Research Fellowship under Grant No. 2141064. Any opinion, findings, and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation.

## References

- [1] Y. An, X. Zhao, T. Yu, M. Tang, and J. Wang (2025-02) Systematic Outliers in Large Language Models. arXiv. Note: arXiv:2502.06415 [cs] External Links: Link, Document Cited by:§5.1.
- [2] S. Ashkboos, A. Mohtashami, M. L. Croci, B. Li, P. Cameron, M. Jaggi, D. Alistarh, T. Hoefler, and J. Hensman (2024-10) QuaRot: Outlier-Free 4-Bit Inference in Rotated LLMs. arXiv. Note: arXiv:2404.00456 [cs] External Links: Link, Document Cited by:§6,§6.
- [3] Y. Bondarenko, M. Nagel, and T. Blankevoort (2023-11) Quantizable Transformers: Removing Outliers by Helping Attention Heads Do Nothing. arXiv. Note: arXiv:2306.12929 [cs] External Links: Link, Document Cited by:§5.1.
- [4] R. L. Castro, A. Panferov, S. Tabesh, O. Sieberling, J. Chen, M. Nikdan, S. Ashkboos, and D. Alistarh (2025-05) Quartet: Native FP4 Training Can Be Optimal for Large Language Models. arXiv. Note: arXiv:2505.14669 [cs] External Links: Link, Document Cited by:§1,§1,§2.2,§6.
- [5] M. Chen, M. Wu, H. Jin, Z. Yuan, J. Liu, C. Zhang, Y. Li, J. Huang, J. Ma, Z. Xue, Z. Liu, X. Bin, and P. Luo (2025-10) INT v.s. FP: A Comprehensive Study of Fine-Grained Low-bit Quantization Formats. arXiv. Note: arXiv:2510.25602 [cs] External Links: Link, Document Cited by:§2.1,§5.1.
- [6] B. Chmiel, M. Fishman, R. Banner, and D. Soudry (2025-08) FP4 All the Way: Fully Quantized Training of LLMs. arXiv. Note: arXiv:2505.19115 [cs] External Links: Link, Document Cited by:§1,§1,§2.2,§6.
- [7] C. Clark, K. Lee, M. Chang, T. Kwiatkowski, M. Collins, and K. Toutanova (2019-05) BoolQ: Exploring the Surprising Difficulty of Natural Yes/No Questions. arXiv. Note: arXiv:1905.10044 [cs] External Links: Link, Document Cited by:§4.2.
- [8] P. Clark, I. Cowhey, O. Etzioni, T. Khot, A. Sabharwal, C. Schoenick, and O. Tafjord (2018-03) Think you have
```

> AGENT

现在我来获取更详细的 Medusa 论文内容，特别是关于验证/比较部分。

> TOOL

tool_use mcp__exa__web_fetch_exa
```json
{
  "maxCharacters": 20000,
  "urls": [
    "https://arxiv.org/html/2401.10774"
  ]
}
```

> TOOL

tool_result mcp__exa__web_fetch_exa
```
<persisted-output>
Output too large (81.8KB). Full output saved to: /user_4813494d/.claude/projects/-user_4813494d-openbmb/76f3fa2c-f12e-4e32-8a58-71a3688d03ea/tool-results/call_d163831f1190412983839df9.json

Preview (first 2KB):
[
  {
    "type": "text",
    "text": "# Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads\nURL: https://arxiv.org/html/2401.10774\n\nMedusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads\n\n# Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads\n\nTianle Cai Yuhong Li Zhengyang Geng Hongwu Peng Jason D. Lee Deming Chen Tri Dao\n\n###### Abstract\n\nLarge Language Models (LLMs) employ auto-regressive decoding that requires sequential computation, with each step reliant on the previous one’s output. This creates a bottleneck as each step necessitates moving the full model parameters from High-Bandwidth Memory (HBM) to the accelerator’s cache. While methods such as speculative decoding have been suggested to address this issue, their implementation is impeded by the challenges associated with acquiring and maintaining a separate draft model. In this paper, we present Medusa, an efficient method that augments LLM inference by adding extra decoding heads to predict multiple subsequent tokens in parallel. Using a tree-based attention mechanism, Medusa constructs multiple candidate continuations and verifies them simultaneously in each decoding step. By leveraging parallel processing, Medusa substantially reduces the number of decoding steps required. We present two levels of fine-tuning procedures for Medusa to meet the needs of different use cases: Medusa-1: Medusa is directly fine-tuned on top of a frozen backbone LLM, enabling lossless inference acceleration. Medusa-2: Medusa is fine-tuned together with the backbone LLM, enabling better prediction accuracy of Medusa heads and higher speedup but needing a special training recipe that preserves the model’s capabilities. Moreover, we propose several extensions that improve or expand the utility of Medusa, including a self-distillation to handle situations where no training data is available and a typical acceptance scheme to boost the a
...
</persisted-output>
```

> TOOL

tool_use Bash
```json
{
  "command": "cat /user_4813494d/.claude/projects/-user_4813494d-openbmb/76f3fa2c-f12e-4e32-8a58-71a3688d03ea/tool-results/call_d163831f1190412983839df9.json | python3 -c \"import json,sys; data=json.load(sys.stdin); text=data[0]['text']; idx=text.find('2.3'); print(text[idx:idx+10000])\"",
  "description": "Read Medusa verification and typical acceptance section"
}
```

> TOOL

tool_result Bash
```
2.3-2.8 $\times$ .

Machine Learning, ICML

## 1 Introduction

The recent advancements in Large Language Models (LLMs) have demonstrated that the quality of language generation significantly improves with an increase in model size, reaching billions of parameters (Brown et al., 2020; Chowdhery et al., 2022; Zhang et al., 2022; Hoffmann et al., 2022; OpenAI, 2023; Google, 2023; Touvron et al., 2023). However, this growth has led to an increase in inference latency, which poses a significant challenge in practical applications. From a system perspective, LLM inference is predominantly memory-bandwidth-bound (Shazeer, 2019; Kim et al., 2023), with the main latency bottleneck stemming from accelerators’ memory bandwidth rather than arithmetic computations. This bottleneck is inherent to the sequential nature of auto-regressive decoding, where each forward pass requires transferring the complete model parameters from High-Bandwidth Memory (HBM) to the accelerator’s cache. This process, which generates only a single token, underutilizes the arithmetic computation potential of modern accelerators, leading to inefficiency.

To address this, one approach to speed up LLM inference involves increasing the arithmetic intensity (the ratio of total floating-point operations (FLOPs) to total data movement) of the decoding process and reducing the number of decoding steps. In line with this idea, speculative decoding has been proposed (Leviathan et al., 2022; Chen et al., 2023; Xia et al., 2023; Miao et al., 2023). This method uses a smaller draft model to generate a token sequence, which is then refined by the original, larger model for acceptable continuation. However, obtaining an appropriate draft model remains challenging, and it’s even harder to integrate the draft model into a distributed system (Chen et al., 2023).

Instead of using a separate draft model to sequentially generate candidate outputs, in this paper, we revisit and refine the concept of using multiple decoding heads on top of the backbone model to expedite inference (Stern et al., 2018). We find that when applied effectively, this technique can overcome the challenges of speculative decoding, allowing for seamless integration into existing LLM systems. Specifically, we introduce Medusa, a method that enhances LLM inference by integrating additional decoding heads to concurrently predict multiple tokens. These heads are fine-tuned in a parameter-efficient manner and can be added to any existing model. With no requirement for a draft model, Medusa offers easy integration into current LLM systems, including those in distributed environments, ensuring a user-friendly experience.

We further enhance Medusa with two key insights. Firstly, the current approach of generating a single candidate continuation at each decoding step leads to inefficient use of computational resources. To address this, we propose generating multiple candidate continuations using the Medusa heads and verifying them concurrently through a simple adjustment to the attention mask. Secondly, we can reuse the rejection sampling scheme as used in speculative decoding (Leviathan et al., 2022; Chen et al., 2023) to generate consistent responses with the same distribution as the original model. However, it cannot further enhance the acceleration rate. Alternatively, we introduce a typical acceptance scheme that selects reasonable candidates from the Medusa head outputs. We use temperature as a threshold to manage deviation from the original model’s predictions, providing an efficient alternative to the rejection sampling method. Our results suggest that the proposed typical acceptance scheme can accelerate the decoding speed further while maintaining a similar generation quality.

To equip LLMs with predictive Medusa heads, we propose two distinct fine-tuning procedures tailored to various scenarios. For situations with limited computational resources or when the objective is to incorporate Medusa into an existing model without affecting its performance, we recommend Medusa-1. This method requires minimal memory and can be further optimized with quantization techniques akin to those in QLoRA (Dettmers et al., 2023), without compromising the generation quality due to the fixed backbone model. However, in Medusa-1, the full potential of the backbone model is not utilized. We can further fine-tune it to enhance the prediction accuracy of Medusa heads, which can directly lead to a greater speedup. Therefore, we introduce Medusa-2, which is suitable for scenarios with ample computational resources or for direct Supervised Fine-Tuning (SFT) from a base model. The key to Medusa-2 is a training protocol that enables joint training of the Medusa heads and the backbone model without compromising the model’s next-token prediction capability and output quality. We propose different strategies for obtaining the training datasets depending on the model’s training recipe and dataset availability. When the model is fine-tuned on a public dataset, it can be directly used for Medusa. If the dataset is unavailable or the model underwent a Reinforcement Learning with Human Feedback (RLHF) (Ouyang et al., 2022) process, we suggest a self-distillation approach to generate a training dataset for the Medusa heads.

Our experiments primarily focus on scenarios with a batch size of one, which is representative of the use case where LLMs are locally hosted for personal use. We test Medusa on models of varying sizes and training settings, including Vicuna-7B, 13B (trained with a public dataset), Vicuna-33B (Chiang et al., 2023) (trained with a private dataset111Upon contacting the authors, this version is experimental and used some different data than Vicuna 7B and 13B.), and Zephyr-7B (trained with both supervised fine-tuning and alignment). Medusa can achieve a speedup of 2.3 to 2.8 times across different prompt types without compromising on the quality of generation.

Figure 1: Medusa introduces multiple heads on top of the last hidden states of the LLM, enabling the prediction of several subsequent tokens in parallel (Section 2.1.1). During inference, each head generates multiple top predictions for its designated position. These predictions are assembled into candidates, which are processed in parallel using a tree-based attention mechanism (Section 2.1.2). The final step is to verify the candidates and accept a continuation. Besides the standard rejection sampling scheme, a typical acceptance scheme (Section 2.3.1) can also be used here to select reasonable continuations, and the longest accepted candidate prefix will be used for the next decoding phase.

## 2 Methodology

Medusa follows the same framework as speculative decoding, where each decoding step primarily consists of three substeps: (1) generating candidates, (2) processing candidates, and (3) accepting candidates. For Medusa, (1) is achieved by Medusa heads, (2) is realized by tree attention, and since Medusa heads are on top of the original model, the logits calculated in (2) can be used for substep (1) for the next decoding step. The final step (3) can be realized by either rejection sampling (Leviathan et al., 2022; Chen et al., 2023) or typical acceptance (Section 2.3.1). The overall pipeline is illustrated in Figure 1.

In this section, we first introduce the key components of Medusa, including Medusa heads, and tree attention. Then, we present two levels of fine-tuning procedures for Medusa to meet the needs of different use cases. Finally, we propose two extensions to Medusa, including self-distillation and typical acceptance, to handle situations where no training data is available for Medusa and to improve the efficiency of the decoding process, respectively.

### 2.1 Key Components

#### 2.1.1 Medusa Heads

In speculative decoding, subsequent tokens are predicted by an auxiliary draft model. This draft model must be small yet effective enough to generate continuations that the original model will accept. Fulfilling these requirements is a challenging task, and existing approaches (Spector & Re, 2023; Miao et al., 2023) often resort to separately pre-training a smaller model. This pre-training process demands substantial additional computational resources. For example, in (Miao et al., 2023), a reported 275 NVIDIA A100 GPU hours were used. Additionally, separate pre-training can potentially create a distribution shift between the draft model and the original model, leading to continuations that the original model may not favor. Chen et al. (2023) have also highlighted the complexities of serving multiple models in a distributed environment.

To streamline and democratize the acceleration of LLM inference, we take inspiration from Stern et al. (2018), which utilizes parallel decoding for tasks such as machine translation and image super-resolution. Medusa heads are additional decoding heads appended to the last hidden states of the original model. Specifically, given the original model’s last hidden states $h_{t}$ at position $t$ , we add $K$ decoding heads to $h_{t}$ . The $k$ -th head is used to predict the token in the $(t+k+1)$ -th position of the next tokens (the original language model head is used to predict the $(t+1)$ -th position). The prediction of the $k$ -th head is denoted as $p_{t}^{(k)}$ , representing a distribution over the vocabulary, while the prediction of the original model is denoted as $p_{t}^{(0)}$ . Following the approach of Stern et al. (2018), we utilize a single layer of feed-forward network with a residual connection for each head. We find that this simple design is sufficient to achieve satisfactory performance. The definition of the $k$ -th head is outlined as:

| $\displaystyle p_{t}^{(k)}=\text{softmax}\left(W_{2}^{(k)}\cdot\left(\text{SiLU% }(W_{1}^{(k)}\cdot h_{t})+h_{t}\right)\right),$ |
| --- |
| $\displaystyle\text{where }W_{2}^{(k)}\in\mathbb{R}^{d\times V},W_{1}^{(k)}\in% \mathbb{R}^{d\times d}.$ |

$d$ is
```

> TOOL

tool_use Bash
```json
{
  "command": "cat /user_4813494d/.claude/projects/-user_4813494d-openbmb/76f3fa2c-f12e-4e32-8a58-71a3688d03ea/tool-results/call_d163831f1190412983839df9.json | python3 -c \"import json,sys; data=json.load(sys.stdin); text=data[0]['text']; idx=text.find('speculative decoding'); print('SPECULATIVE DECODING COMPARISON:'); print(text[idx:idx+5000])\"",
  "description": "Read Medusa comparison with speculative decoding"
}
```

> TOOL

tool_result Bash
```
SPECULATIVE DECODING COMPARISON:
speculative decoding have been suggested to address this issue, their implementation is impeded by the challenges associated with acquiring and maintaining a separate draft model. In this paper, we present Medusa, an efficient method that augments LLM inference by adding extra decoding heads to predict multiple subsequent tokens in parallel. Using a tree-based attention mechanism, Medusa constructs multiple candidate continuations and verifies them simultaneously in each decoding step. By leveraging parallel processing, Medusa substantially reduces the number of decoding steps required. We present two levels of fine-tuning procedures for Medusa to meet the needs of different use cases: Medusa-1: Medusa is directly fine-tuned on top of a frozen backbone LLM, enabling lossless inference acceleration. Medusa-2: Medusa is fine-tuned together with the backbone LLM, enabling better prediction accuracy of Medusa heads and higher speedup but needing a special training recipe that preserves the model’s capabilities. Moreover, we propose several extensions that improve or expand the utility of Medusa, including a self-distillation to handle situations where no training data is available and a typical acceptance scheme to boost the acceptance rate while maintaining generation quality. We evaluate Medusa on models of various sizes and training procedures. Our experiments demonstrate that Medusa-1 can achieve over 2.2 $\times$ speedup without compromising generation quality, while Medusa-2 further improves the speedup to 2.3-2.8 $\times$ .

Machine Learning, ICML

## 1 Introduction

The recent advancements in Large Language Models (LLMs) have demonstrated that the quality of language generation significantly improves with an increase in model size, reaching billions of parameters (Brown et al., 2020; Chowdhery et al., 2022; Zhang et al., 2022; Hoffmann et al., 2022; OpenAI, 2023; Google, 2023; Touvron et al., 2023). However, this growth has led to an increase in inference latency, which poses a significant challenge in practical applications. From a system perspective, LLM inference is predominantly memory-bandwidth-bound (Shazeer, 2019; Kim et al., 2023), with the main latency bottleneck stemming from accelerators’ memory bandwidth rather than arithmetic computations. This bottleneck is inherent to the sequential nature of auto-regressive decoding, where each forward pass requires transferring the complete model parameters from High-Bandwidth Memory (HBM) to the accelerator’s cache. This process, which generates only a single token, underutilizes the arithmetic computation potential of modern accelerators, leading to inefficiency.

To address this, one approach to speed up LLM inference involves increasing the arithmetic intensity (the ratio of total floating-point operations (FLOPs) to total data movement) of the decoding process and reducing the number of decoding steps. In line with this idea, speculative decoding has been proposed (Leviathan et al., 2022; Chen et al., 2023; Xia et al., 2023; Miao et al., 2023). This method uses a smaller draft model to generate a token sequence, which is then refined by the original, larger model for acceptable continuation. However, obtaining an appropriate draft model remains challenging, and it’s even harder to integrate the draft model into a distributed system (Chen et al., 2023).

Instead of using a separate draft model to sequentially generate candidate outputs, in this paper, we revisit and refine the concept of using multiple decoding heads on top of the backbone model to expedite inference (Stern et al., 2018). We find that when applied effectively, this technique can overcome the challenges of speculative decoding, allowing for seamless integration into existing LLM systems. Specifically, we introduce Medusa, a method that enhances LLM inference by integrating additional decoding heads to concurrently predict multiple tokens. These heads are fine-tuned in a parameter-efficient manner and can be added to any existing model. With no requirement for a draft model, Medusa offers easy integration into current LLM systems, including those in distributed environments, ensuring a user-friendly experience.

We further enhance Medusa with two key insights. Firstly, the current approach of generating a single candidate continuation at each decoding step leads to inefficient use of computational resources. To address this, we propose generating multiple candidate continuations using the Medusa heads and verifying them concurrently through a simple adjustment to the attention mask. Secondly, we can reuse the rejection sampling scheme as used in speculative decoding (Leviathan et al., 2022; Chen et al., 2023) to generate consistent responses with the same distribution as the original model. However, it cannot further enhance the acceleration rate. Alternatively, we introduce a typical acceptance scheme that selects reasonable candidates from the Medusa head outputs. We use temperature
```

> TOOL

tool_use Bash
```json
{
  "command": "cat /user_4813494d/.claude/projects/-user_4813494d-openbmb/76f3fa2c-f12e-4e32-8a58-71a3688d03ea/tool-results/call_d163831f1190412983839df9.json | python3 -c \"import json,sys; data=json.load(sys.stdin); text=data[0]['text']; idx=text.find('Typical Acceptance'); print(text[idx:idx+6000])\"",
  "description": "Read Medusa typical acceptance scheme details"
}
```

> TOOL

tool_result Bash
```
Typical Acceptance

In speculative decoding papers (Leviathan et al., 2022; Chen et al., 2023), authors employ rejection sampling to yield diverse outputs that align with the distribution of the original model. However, subsequent implementations (Joao Gante, 2023; Spector & Re, 2023) reveal that this sampling strategy results in diminished efficiency as the sampling temperature increases. Intuitively, this can be comprehended in the extreme instance where the draft model is the same as the original one: Using greedy decoding, all output of the draft model will be accepted, therefore maximizing the efficiency. Conversely, rejection sampling introduces extra overhead, as the draft model and the original model are sampled independently. Even if their distributions align perfectly, the output of the draft model may still be rejected.

However, in real-world scenarios, sampling from language models is often employed to generate diverse responses, and the temperature parameter is used merely to modulate the “creativity” of the response. Therefore, higher temperatures should result in more opportunities for the original model to accept the draft model’s output. We ascertain that it is typically unnecessary to match the distribution of the original model. Thus, we propose employing a typical acceptance scheme to select plausible candidates rather than using rejection sampling. This approach draws inspiration from truncation sampling studies (Hewitt et al., 2022) (refer to Appendix A for an in-depth explanation). Our objective is to choose candidates that are typical, meaning they are not exceedingly improbable to be produced by the original model. We use the prediction probability from the original model as a natural gauge for this and establish a threshold based on the prediction distribution to determine acceptance. Specifically, given $x_{1},x_{2},\cdots,x_{n}$ as context, when evaluating the candidate sequence $(x_{n+1},x_{n+2},\cdots,x_{n+K+1})$ (composed by top predictions of the original language model head and Medusa heads), we consider the condition

| $\displaystyle p_{\text{original}}(x_{n+k}|x_{1},x_{2},\cdots,x_{n+k-1})>$ |
| --- |
| $\displaystyle\min\left(\epsilon,\delta\exp\left(-H(p_{\text{original}}(\cdot|x% _{1},x_{2},\cdots,x_{n+k-1}))\right)\right),$ |

where $H(\cdot)$ denotes the entropy function, and $\epsilon,\delta$ are the hard threshold and the entropy-dependent threshold respectively. This criterion is adapted from Hewitt et al. (2022) and rests on two observations: (1) tokens with relatively high probability are meaningful, and (2) when the distribution’s entropy is high, various continuations may be deemed reasonable. During decoding, every candidate is evaluated using this criterion, and a prefix of the candidate is accepted if it satisfies the condition. To guarantee the generation of at least one token at each step, we apply greedy decoding for the first token and unconditionally accept it while employing typical acceptance for subsequent tokens. The final prediction for the current step is determined by the longest accepted prefix among all candidates.

Examining this scheme leads to several insights. Firstly, when the temperature is set to $0$ , it reverts to greedy decoding, as only the most probable token possesses non-zero probability. As the temperature surpasses $0$ , the outcome of greedy decoding will consistently be accepted with appropriate $\epsilon,\delta$ , since those tokens have the maximum probability, yielding maximal speedup. Likewise, in general scenarios, an increased temperature will correspondingly result in longer accepted sequences, as corroborated by our experimental findings.

Empirically, we verify that typical acceptance can achieve a better speedup while maintaining a similar generation quality as shown in Figure 5.

#### 2.3.2 Self-Distillation

In Section 2.2, we assume the existence of a training dataset that matches the target model’s output distribution. However, this is not always the case. For example, the model owners may only release the model without the training data, or the model may have gone through a Reinforcement Learning with Human Feedback (RLHF) procedure, which makes the output distribution of the model different from the training dataset. To tackle this issue, we propose an automated self-distillation pipeline to use the model itself to generate the training dataset for Medusa heads, which matches the output distribution of the model.

The dataset generation process is straightforward. We first take a public seed dataset from a domain similar to the target model; for example, using the ShareGPT (ShareGPT, 2023) dataset for chat models. Then, we simply take the prompts from the dataset and ask the model to reply to the prompts. In order to obtain multi-turn conversation samples, we can sequentially feed the prompts from the seed dataset to the model. Or, for models like Zephyr 7B (Tunstall et al., 2023), which are trained on both roles of the conversation, they have the ability to self-talk, and we can simply feed the first prompt and let the model generate multiple rounds of conversation.

For Medusa-1, this dataset is sufficient for training Medusa heads. However, for Medusa-2, we observe that solely using this dataset for training the backbone and Medusa heads usually leads to a lower generation quality. In fact, even without training Medusa heads, training the backbone model with this dataset will lead to performance degradation. This suggests that we also need to use the original model’s probability prediction instead of using the ground truth token as the label for the backbone model, similar to classic knowledge distillation works (Kim & Rush, 2016). Concretely, the loss for the backbone model is:

| $\displaystyle\mathcal{L}_{\text{LM-distill}}=KL(p_{\text{original},t}^{(0)}||p% _{t}^{(0)}),$ |
| --- |

where $p_{\text{original},t}^{(0)}$ denotes the probability distribution of the original model’s predi
```

> TOOL

tool_use Bash
```json
{
  "command": "cat /user_4813494d/.claude/projects/-user_4813494d-openbmb/76f3fa2c-f12e-4e32-8a58-71a3688d03ea/tool-results/call_d163831f1190412983839df9.json | python3 -c \"import json,sys; data=json.load(sys.stdin); text=data[0]['text']; idx=text.find('Experiment'); print(text[idx:idx+8000])\"",
  "description": "Read Medusa experiment results"
}
```

> TOOL

tool_result Bash
```
Experiments

In this section, we present experiments to demonstrate the effectiveness of Medusa under different settings. First, we evaluate Medusa on the Vicuna-7B and 13B models (Chiang et al., 2023) to show the performance of Medusa-1 and Medusa-2. Then, we assess our method using the Vicuna-33B and Zephyr-7B models to demonstrate self-distillation’s viability in scenarios where direct access to the fine-tuning recipe is unavailable, as with Vicuna-33B, and in models like Zephyr-7B that employ Reinforcement Learning from Human Feedback (RLHF). The evaluation is conducted on MT-Bench (Zheng et al., 2023), a multi-turn, conversational-format benchmark. Detailed settings can be found in Appendix B.

### 3.1 Case Study: Medusa-1 v.s. Medusa-2 on Vicuna 7B and 13B

Experimental Setup. We use the Vicuna model class (Chiang et al., 2023), which encompasses chat models of varying sizes (7B, 13B, 33B) that are fine-tuned from the Llama model (Touvron et al., 2023). Among them, the 7B and 13B models are trained on the ShareGPT (ShareGPT, 2023) dataset, while the 33B model is an experimental model and is trained on a private dataset. In this section, we use the ShareGPT dataset to train the Medusa heads on the 7B and 13B models for $2$ epochs. We use the v1.5 version of Vicuna models, which are fine-tuned from Llama-2 models with sequence length 4096.

Results. We collect the results and show them in Fig. 3. The baseline is the default Huggingface implementation. In Fig. 3(a), we can see that for the 7B models, Medusa-1 and Medusa-2 configurations lead to a significant increase in speed, measuring in tokens processed per second. Medusa-1 shows a 2.18 $\times$ speedup, while Medusa-2 further improves this to a 2.83 $\times$ . When applied to the larger 13B model, Medusa-1 results in a 2.33 $\times$ speed increase, while Medusa-2 maintains a similar performance gain of 2.83 $\times$ over the baseline. We also plot the speedup per category for Medusa-2 Vicuna-7B model. We observe that the coding category benefits from a 3.29 $\times$ speedup, suggesting that Medusa is particularly effective for tasks in this domain. This points to a significant potential for optimizing coding LLMs, which are widely used in software development and other programming-related tasks. The “Extraction” category shows the highest speedup at 3.62 $\times$ , indicating that this task is highly optimized by the Medusa. Overall, the results suggest that the Medusa significantly enhances inference speed across different model sizes and tasks.

### 3.2 Case Study: Training with Self-Distillation on Vicuna-33B and Zephyr-7B

Experimental Setup. In this case study, we focus on the cases where self-distillation is needed. We use the Vicuna-33B model (Chiang et al., 2023) and the Zephyr-7B model (Tunstall et al., 2023) as examples. Following the procedure described in Section 2.3.2, we first generate the datasets with some seed prompts. We use ShareGPT (ShareGPT, 2023) and UltraChat (Ding et al., 2023) as the seed datasets and collect a dataset at about $100k$ samples for both cases. Interestingly, we find that the Zephyr model can continue to generate multiple rounds of conversation with a single prompt, which makes it easy to collect a large dataset. For Vicuna-33B, we generate the multi-turn conversations by iteratively feeding the prompts from each multi-turn seed conversation using random sampling with temperature 0.3. Both models are trained with sequence length $2048$ and batch size $128$ .

Table 1: Comparison of various Medusa-2 models. The first section reports the details of Medusa-2, including accelerate rate, overhead, and quality that denoted the average scores on the MT-Bench compared to the original models. The second section lists the speedup ( $S$ ) of SpecDecoding and Medusa, respectively.

| Model Name | Vicuna-7B | Zephyr-7B | Vicuna-13B | Vicuna-33B |
| --- | --- | --- | --- | --- |
| Acc. rate | 3.47 | 3.14 | 3.51 | 3.01 |
| Overhead | 1.22 | 1.18 | 1.23 | 1.27 |
| Quality | 6.18 (+0.01) | 7.25 (-0.07) | 6.43 (-0.14) | 7.18 (+0.05) |
| $S_{\textnormal{SpecDecoding}}$ | 1.47 | - | 1.56 | 1.60 |
| $S_{\textsc{Medusa}}$ | 2.83 | 2.66 | 2.83 | 2.35 |

Figure 4: Effectiveness of numbers of candidate tokens for decoding introduced by trees (default number of candidate token for decoding is 1 when using KV cache). Left: The acceleration rate for randomly sampled dense tree settings (blue dots) and optimized sparse tree settings (red stars). Right: The speed (tokens/s) for both settings. The trend lines indicate that while the acceleration rate remains relatively stable for sparse trees, there is a notable decrease in speed as the candidate tokens increases.

(a)

(b)

Results. Table 1 complements these findings by comparing various Medusa-2 models in terms of their acceleration rate, overhead, and quality on MT-Bench with GPT-4 acting as the evaluator to assign performance scores ranging from 0 to 10. We report the quality differences of Medusa compared to the original model. Notably, while the Medusa-2 Vicuna-33B model shows a lower acceleration rate, it maintains a comparable quality. We hypothesize that this is due to a mismatch between the hidden training dataset and the dataset we used for self-distillation. Hence, the model’s generation quality can be well aligned by self-distillation while Medusa heads learn distribution from the self-distillation that potentially shifts from the training set. In our study, we also applied speculative decoding (Chen et al., 2023; Leviathan et al., 2022) to the Vicuna lineup using open-source draft models (details can be found in Appendix D).

These results underscore the complex interplay between speed and performance when scaling up model sizes and applying self-distillation techniques. The findings also highlight the potential of the Medusa-2 configuration to boost efficiency in processing while carefully preserving the quality of the model’s outputs, suggesting a promising direction for co-optimizing LLMs with Medusa heads.

### 3.3 Ablation Study

#### 3.3.1 Configuration of Tree Attention

The study of tree attention is conducted on the writing and roleplay categories from the MT-Bench dataset using Medusa-2 Vicuna-7B. We target to depict tree attention’s motivation and its performance.

Fig. 4(a) compares the acceleration rate of randomly sampled dense tree configurations (Section. 2.1.2, depicted by blue dots) against optimized sparse tree settings (Section. 2.3.3, shown with red stars). The sparse tree configuration with 64 nodes shows a better acceleration rate than the dense tree settings with 256 nodes. The decline in speed in Fig. 4(b) is attributed to the increased overhead introduced by the compute-bound. While a more complex tree can improve acceleration, it does so at the cost of speed due to intensive matrix multiplications for linear layers and self-attention. The acceleration rate increase follows a logarithmic trend and slows down when the tree size grows as shown in Fig. 4(a). However, the initial gains are substantial, allowing Medusa to achieve significant speedups. If the acceleration increase is less than the overhead, it will slow down overall performance. For detailed study, please refer to Appendix G.

Figure 5: Performance comparison of Medusa using proposed typical sampling. The model is fully fine-tuned from Vicuna-7B. The plot illustrates the acceleration rate and average scores on the writing and roleplay (MT-Bench) with a fixed temperature of 0.7 for 3 different settings: greedy sampling and random sampling (RS) plotted as the star and the dot, and typical sampling curves under different thresholds.

#### 3.3.2 Thresholds of Typical Acceptance

The thresholds of typical acceptance are studied on the writing and roleplay categories from the MT-Bench dataset (Zheng et al., 2023) using Medusa-2 Vicuna 7B. Utilizing the Vicuna 7B model, we aligned our methodology with the approach delineated by (Hewitt et a
```

> AGENT

我现在已经获取了关于这两篇论文的全面信息。让我来整理验证结果。

---

## 论文一：FourOverSix -- 验证报告

### 1. 论文标题、作者、机构

- **标题**: Four Over Six: More Accurate NVFP4 Quantization with Adaptive Block Scaling
- **作者**: Jack Cook, Junxian Guo, Guangxuan Xiao, Yujun Lin, Song Han
- **机构**: 1Massachusetts Institute of Technology (MIT), 2NVIDIA
- **通信作者**: Jack Cook, Song Han
- **代码**: https://github.com/mit-han-lab/fouroversix

**关于"MIT-HAN Lab"的声明**: 基本正确。论文明确标注第一单位为 MIT，Song Han 为通信作者之一，且代码仓库位于 mit-han-lab 组织下。但需注意，这是一篇 MIT 与 NVIDIA 的**联合工作**，Yujun Lin 的单位是 NVIDIA，不能简单说是纯 MIT-HAN Lab 的工作。

### 2. FourOverSix 算法的准确描述

**用户描述的"scale=4 和 scale=6 的 MSE 比较选更小者"基本正确，但需要澄清"scale"的具体含义。**

准确机制如下：

- **NVFP4 格式**使用 FP4 E2M1，其可表示值为 {0, 0.5, 1, 1.5, 2, 3, 4, 6}（正数部分），最大值为 6。标准 NVFP4 量化时，每个 block 的值会被归一化到 FP4 的完整范围（-6 到 6），即 `M=6`。
- **"scale=4 vs scale=6"的含义**: 这里的 4 和 6 **不是 scale factor 本身**，而是**归一化范围的上界 M**。当 M=6 时，block 的最大值被映射到 FP4 的最大值 6；当 M=4 时，block 的最大值被映射到 FP4 值 4（放弃了 4 和 6 之间的表示范围）。
- **为什么 M=4 有时更好**: 当 block 缩放到 M=6 时，FP4 值 4 代表 block 最大值的 66.6%（4/6），而 4 到 6 之间没有可表示的值，导致近最大值（66.6%~100% 范围）无法精确表示。当 M=4 时，FP4 值 3 代表 75%（3/4），填补了这一"盲区"，减少了对近最大值的量化误差。
- **选择规则**: 对每个 block 分别用 M=6 和 M=4 量化一次，计算两种方案的反量化值与原始值的 MSE，选 MSE 更小者。论文也测试了 L1 范数和 Abs-Max 规则，发现 MSE 在大多数情况下最优。

**纠正用户描述**: 不是"scale=4 vs scale=6"——更准确的说法是"**归一化上界 M=4 vs M=6**"。Scale factor (Delta) 会根据 M 的选择自动调整。

### 3. NVFP4 格式中 scale 参数的作用

NVFP4 使用**两级缩放**：

- **Tensor-wide FP32 scale** `alpha`: `alpha = max(|X|) / (M_FP4 * M_FP8)`，其中 `M_FP4=6`, `M_FP8=448`
- **Block-level FP8 E4M3 scale** `Delta_i`: `Delta_i = max(|X_{16i...16(i+1)}|) / (alpha * M_FP4)`，每 16 个值共享一个

量化公式为分段舍入（Equation 3），取决于 `|X/(alpha*Delta)|` 的范围：
- < 2: 步长 0.5
- < 4: 步长 1
- <= 6: 步长 2

**4/6 对 scale 的影响**: 当选择 M=4 时，block 的 scale factor Delta 会相应增大（因为 Delta = max(|X_block|) / (alpha * 4) 而非 / (alpha * 6)）。此外，论文修改了 tensor scale alpha 的计算，将 M_FP8 替换为 256（而非 448），以确保 M=4 的 block scale 在 FP8 E4M3 中可表示（因为 256 * 6/4 = 384，不会溢出 E4M3 的最大值 448）。

**所以用户说的"scale/6"不准确**。正确理解是：scale factor 的分母中 M_FP4 从 6 变为 4，这使得 scale factor 变大（约 1.5 倍），从而将同样的值映射到 FP4 更小的范围，获得更密集的表示。

### 4. 论文报告的性能数字

**Pre-training**:
- 4/6 使 NVFP4 训练损失向 BF16 **靠近了 22.3%**
- 模型架构: Nemotron 3 Nano 30B-A3B（混合 Mamba-Transformer MoE 架构）
- 训练规模: 1T tokens，384 个 B200 GPU

**Post-Training Quantization (PTQ)**:
- **+ AWQ + 4/6**: WikiText-2 平均 perplexity 11.58，C4 平均 perplexity 32.36（所有测试模型中最佳）
- **+ AWQ + 4/6**: Perplexity 比 BF16 差距缩小 **19.9%**；+ SmoothQuant + 4/6 缩小 **5.3%**
- **+ GPTQ + 4/6**: 反而使 NVFP4 与 BF16 的差距平均**扩大了 34.6%**（论文明确指出 GPTQ+4/6 效果不佳）
- 下游任务（BoolQ, ARC, HellaSwag）上，4/6 在绝大多数情况下提升平均性能

**实现开销**: 4/6 在 CUDA kernel 中实现，所有中间值保持在寄存器文件中，开销**低于 15%**。

---

## 论文二：Medusa -- 验证报告

### 1. 论文标题、作者、Venue

- **标题**: Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads
- **作者**: Tianle Cai, Yuhong Li, Zhengyang Geng, Hongwu Peng, Jason D. Lee, Deming Chen, Tri Dao
- **Venue**: arXiv 标注为 "Machine Learning, ICML"，即 **ICML 2024**

**验证**: 用户声称"Tianle Cai et al., ICML 2024"——**正确**。

### 2. Medusa Head 的准确架构

用户描述的"ResBlock + LM Head 结构"**基本正确但需要更精确**。

准确公式：

```
p_t^(k) = softmax( W2^(k) * ( SiLU(W1^(k) * h_t) + h_t ) )
```

其中：
- `W1^(k) ∈ R^{d×d}`: 单层前馈网络（一个线性层）
- `W2^(k) ∈ R^{d×V}`: 输出投影到词表大小（类似于 LM Head）
- **残差连接**: `SiLU(W1^(k) * h_t) + h_t`，这就是用户所说的"ResBlock"
- **SiLU 激活函数**: 跟随 Llama 模型的选择
- **初始化**: W2^(k) 初始化为与原始 LM Head 相同的权重，W1^(k) 初始化为零。这使得 Medusa head 初始预测与原始模型一致。

所以"ResBlock"的具体结构是：**单层线性变换 + SiLU 激活 + 残差连接**，然后再接一个线性层投影到词表并 softmax。**不是传统意义上的多层 ResBlock**，而是极其轻量的单层结构。

第 k 个 head 预测位置 t+k+1 处的 token（原始 LM head 预测 t+1，Medusa heads 补充预测后续位置）。

### 3. Verify 机制 -- Tree Attention 的工作方式

**核心流程**:

1. **生成候选**: 每个 Medusa head 产生 top-s_k 个预测。K 个 head 的候选通过**笛卡尔积**组合成多条候选序列。例如 s_1=2, s_2=3 产生 2x3=6 条候选。
2. **Tree Attention 处理**: 所有候选序列在**一次前向传播**中并行处理，通过修改 attention mask 实现。Tree mask 确保每个 token 只能 attend 到其前驱节点（同一候选分支中的历史 token），而非传统因果 mask 的所有前序 token。
3. **位置编码调整**: 位置索引根据树结构调整，而非简单的顺序位置。
4. **验证**: 每个候选被评估，接受最长满足条件的候选前缀。

**Rejection Sampling vs Typical Acceptance**:
- **Rejection sampling**（来自 speculative decoding）：可以保证输出分布与原始模型一致，但在高温采样时效率下降。
- **Typical acceptance**（Medusa 提出）：给定候选 token x_{n+k}，如果 `p_original(x_{n+k}|context) > min(epsilon, delta * exp(-H(p_original)))` 则接受，其中 H 是熵函数。即只要原始模型认为该 token "足够合理"（概率超过阈值）就接受，不需要完全匹配分布。第一token 无条件接受（greedy），后续 token 使用典型接受。**温度越高，接受率越高，加速越快**。

### 4. 与 Standard Speculative Decoding 的核心区别

| 维度 | Speculative Decoding | Medusa |
|------|---------------------|--------|
| **候选生成方式** | 使用独立的**小型 draft model 串行生成**多个 token | 在原模型上附加 **多个 head 并行预测**多个位置 |
| **额外模型** | 需要获取/训练一个合适的 draft model | **不需要**额外模型，head 直接附加在 backbone 上 |
| **分布偏移** | draft model 与原始模型可能有分布偏移 | Medusa heads 基于 backbone 的隐藏状态训练，**天然对齐** |
| **分布式部署** | 需要同时服务两个模型，系统复杂 | 单模型，**易于分布式部署** |
| **候选构建** | 单条候选序列 | **多条候选并行**（tree attention），通过笛卡尔积构建候选树 |
| **验证方式** | Rejection sampling（保证分布一致） | Rejection sampling 或 **Typical acceptance**（更高效但不严格匹配分布） |
| **训练开销** | Draft model 可能需要 275 A100 GPU 小时预训练 | 参数高效微调，单 GPU 可完成 |
| **加速比** | SpecDecoding 在 Vicuna 系列约 1.47-1.60x | **Medusa-2 达到 2.35-2.83x** |

**最核心的区别**: Speculative decoding 用一个**独立的小模型串行预测**，Medusa 用**同一模型的多个 head 并行预测**，省去了独立 draft model 的获取、训练和部署成本，同时通过 tree attention 实现多条候选的并行验证。

---

## 总结：用户描述中需要修正的要点

1. **FourOverSix 机构**: 基本正确但不够精确——这是 MIT + NVIDIA 联合工作，非纯 MIT-HAN Lab。
2. **"scale=4 vs scale=6"**: 含义不是 "scale factor 等于 4 或 6"，而是**归一化范围上界 M=4 vs M=6**。Scale factor (Delta) 会根据 M 自动调整，M=4 时 Delta 更大（约为 M=6 时的 1.5 倍）。
3. **"scale/6"的说法**: 不准确。NVFP4 的量化分母是 `alpha * Delta`，其中 Delta 的计算公式为 `max(|X_block|) / (alpha * M_FP4)`。4/6 改变的是 M_FP4 从 6 到 4，而非直接对 scale 做除法。
4. **Medusa "ResBlock"**: 不是传统多层 ResBlock，而是**单层线性变换 + SiLU + 残差连接**，极其轻量。公式为 `softmax(W2 * (SiLU(W1 * h) + h))`。
5. **Medusa 与 speculative decoding的核心区别**: 最关键的不是"多 head vs 单 draft model"这么简单，而是 Medusa **不需要独立 draft model**、**head 与 backbone 天然对齐**、**通过 tree attention 并行验证多条候选**、以及**typical acceptance 机制**提供了比 rejection sampling 更高效的替代方案。
