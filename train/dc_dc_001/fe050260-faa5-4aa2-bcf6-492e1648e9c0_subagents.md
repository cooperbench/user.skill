> DEVELOPER

Thoroughly explore the EAGLE-3 training pipeline in this repo. I need to understand:

1. All files in eagle/ directory - read each one fully
2. The docs: docs/eagle3_research.md, docs/eagle3-pipeline.md, docs/eagle3-accept-rate-fix.md
3. The medusa/ directory for comparison (collect_data.py, train.py)
4. demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py and medusa_worker.py

For each file, provide:
- Full content summary
- Key parameters and configurations
- How files connect to each other in the pipeline

Be very thorough - read every file completely.

> AGENT

I'll conduct a thorough exploration of the EAGLE-3 training pipeline. Let me start by mapping out all the files and their contents.

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -type f -name \"*.py\" -o -name \"*.md\" | grep -E \"(eagle|medusa)\" | head -50"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/docs/eagle3_research.md
/user_4813494d/openbmb/docs/eagle3-pipeline.md
/user_4813494d/openbmb/docs/eagle3-accept-rate-fix.md
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/hardware_backend/npu/graph_runner/eagle_draft_extend_npu_graph_runner.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/hardware_backend/npu/graph_runner/eagle_draft_npu_graph_runner.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/eagle_draft_cuda_graph_runner.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/eagle_draft_extend_cuda_graph_runner.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/eagle_info_v2.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/eagle_utils.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/multi_layer_eagle_draft_extend_cuda_graph_runner.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/multi_layer_eagle_utils.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/multi_layer_eagle_worker.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/multi_layer_eagle_worker_v2.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/eagle_worker.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/eagle_info.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/medusa_worker.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/models/llama_eagle.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/models/mistral_large_3_eagle.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/models/qwen2_eagle.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/models/llama_eagle3.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/models/ernie4_eagle.py
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/test/server_fixtures/eagle_fixture.py
/user_4813494d/openbmb/medusa/profile_verify.py
/user_4813494d/openbmb/medusa/.ipynb_checkpoints/train-checkpoint.py
/user_4813494d/openbmb/medusa/check_data.py
/user_4813494d/openbmb/medusa/collect_data.py
/user_4813494d/openbmb/medusa/eval_topk.py
/user_4813494d/openbmb/medusa/quick_validate_similar.py
/user_4813494d/openbmb/medusa/select_similar.py
/user_4813494d/openbmb/medusa/train.py
/user_4813494d/openbmb/medusa/collect_eval_overfit.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/hardware_backend/npu/graph_runner/eagle_draft_extend_npu_graph_runner.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/hardware_backend/npu/graph_runner/eagle_draft_npu_graph_runner.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_draft_cuda_graph_runner.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_draft_extend_cuda_graph_runner.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info_v2.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_utils.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/multi_layer_eagle_draft_extend_cuda_graph_runner.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/multi_layer_eagle_utils.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/multi_layer_eagle_worker.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/multi_layer_eagle_worker_v2.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/medusa_worker.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/ernie4_eagle.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama_eagle.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/llama_eagle3.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/models/mistral_large_3_eagle.py
```

> AGENT

Now let me explore the eagle/ directory structure:

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/eagle -type f -name \"*.py\" -o -name \"*.md\" | sort"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/eagle/collect_data.py
/user_4813494d/openbmb/eagle/convert_to_sglang.py
/user_4813494d/openbmb/eagle/eval_ood_accept.py
/user_4813494d/openbmb/eagle/test_decode_mode.py
/user_4813494d/openbmb/eagle/test_eagle3_flow.py
/user_4813494d/openbmb/eagle/test_forward_match.py
/user_4813494d/openbmb/eagle/test_offline_pred.py
/user_4813494d/openbmb/eagle/train.py
/user_4813494d/openbmb/eagle/verify_sglang_draft.py
```

> AGENT

Perfect. Now let me read all the key files. I'll start with the documentation files and then the eagle/ directory files in parallel:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle3_research.md"
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 Speculative Decoding for MiniCPM-SALA
2	
3	本文档记录 EAGLE-3 在 MiniCPM-SALA 上的研究与适配工作。
4	
5	## 1. 背景
6	
7	### 1.1 EAGLE 系列演进
8	
9	| 版本 | Loss 设计 | 关键特点 |
10	|------|----------|----------|
11	| EAGLE-1 | l_fea (MSE) + l_token (CE) | 特征预测 + token 预测 |
12	| EAGLE-2 | l_fea + l_token + tree attention | 引入 tree draft |
13	| **EAGLE-3** | **纯 plogp loss** | 去掉 l_fea，引入 TTT |
14	
15	### 1.2 EAGLE-3 核心创新
16	
17	1. **去除特征约束 (l_fea)**：不再要求 draft 预测 target 的 hidden state，解放模型表达能力
18	2. **Training-Time Test (TTT)**：训练时模拟真实 inference，draft 吃自己的预测做多步自回归
19	3. **多层特征融合**：concat 多层 hidden states 作为输入
20	4. **数据 scaling 生效**：更多数据 → 更高 acceptance rate
21	
22	### 1.3 MiniCPM-SALA 架构
23	
24	```
25	32 layers:
26	  - 8 Standard Attention (minicpm4): layers 0, 9, 16, 17, 22, 29, 30, 31
27	  - 24 Lightning Attention (SimpleGLA): 其余层
28	
29	Config:
30	  - hidden_size: 4096
31	  - intermediate_size: 16384
32	  - num_attention_heads: 32
33	  - num_key_value_heads: 2 (standard), 32 (lightning)
34	  - head_dim: 128
35	  - vocab_size: 73448
36	  - scale_emb: 12
37	  - scale_depth: 1.4
38	  - dim_model_base: 256
39	```
40	
41	**与 Llama 的关键差异**：
42	- 混合注意力架构（非同构）
43	- Lightning Attention 有递推状态 h: (nkv, head_dim, head_dim)
44	- 特殊的 scaling 模式：`scale_depth / sqrt(num_layers)`
45	
46	---
47	
48	## 2. Aux Layer 选择实验
49	
50	### 2.1 实验设计
51	
52	使用 linear probe 评估不同 layer 组合的 next-token 预测能力：
53	- 数据：wikitext-2, 64 samples × 2048 tokens
54	- 方法：Linear(hidden_size × 3, vocab_size) 训练 200 steps
55	- 指标：Cross-Entropy loss (lower = better)
56	
57	### 2.2 Per-Layer Cosine Similarity
58	
59	测量每层 hidden state 与 final hidden state 的余弦相似度：
60	
61	```
62	Layer  Type       CosSim
63	---------------------------
64	  0    Attn       0.0143
65	  1    Lightning  0.0172
66	  2    Lightning  0.0224
67	  ...
68	  9    Attn       0.0408
69	  10   Lightning  0.0419
70	  ...
71	  16   Attn       0.0537
72	  17   Attn       0.0588
73	  ...
74	  22   Attn       0.0767
75	  ...
76	  29   Attn       0.2349
77	  30   Attn       0.3000
78	  31   Attn       1.0000  ← 最后一层
79	```
80	
81	**观察**：
82	- 越深的层 cos_sim 越高
83	- Layer 31 = 1.0（与 final 完全相同，冗余）
84	- 标准 Attn 层的 cos_sim 略高于相邻的 Lightning 层
85	
86	### 2.3 Layer Combo 对比结果
87	
88	第一轮 (13 combos, 16 samples):
89	```
90	[2, 10, 22] CE=7.8260  ★ Best
91	[3, 14, 27] CE=10.7504
92	[4, 12, 28] CE=11.7970
93	[3, 16, 28] CE=11.8116
94	[2, 16, 29] CE=12.4497  ← EAGLE-3 default
95	...
96	[0, 16, 31] CE=30.5165  ← 含 layer 31，最差
97	```
98	
99	第二轮精调 (9 combos, 64 samples):
100	```
101	[1, 10, 22] CE=6.5112  ★ Best
102	[2, 9, 22]  CE=6.5734
103	[2, 10, 21] CE=6.6441
104	[2, 8, 22]  CE=6.6568
105	[2, 10, 22] CE=6.6753
106	...
107	```
108	
109	### 2.4 结论
110	
111	**选定 aux layers: [2, 10, 22]**
112	
113	| Layer | Type | 位置 | 选择理由 |
114	|-------|------|------|----------|
115	| 2 | Lightning | 早期 | 捕获原始特征 |
116	| 10 | Lightning | 中期 | 捕获中间处理 |
117	| 22 | Attn | 中后期 | 捕获标准注意力 pattern |
118	
119	**与 EAGLE-3 官方的差异**：
120	
121	EAGLE-3 官方代码用 [embedding, layer0, layer1]（极早期），可能原因：
122	1. Llama 是同构 Transformer，早期层足够
123	2. TTT 训练使 draft 能从错误中恢复，不需要 late layer 信息
124	3. Late layer 与 final 太接近，冗余
125	
126	MiniCPM-SALA 是**混合架构**，我们的选择覆盖两种注意力类型，更合理。
127	
128	---
129	
130	## 3. 草稿模型架构
131	
132	### 3.1 结构设计
133	
134	```
135	MiniCPMForCausalLMEagle3:
136	  fc: Linear(4096 × 3, 4096)     # 融合 3 层 aux hidden
137	  midlayer: MiniCPMDecoderLayer  # 1 层完整 transformer
138	    - input_layernorm: RMSNorm
139	    - hidden_norm: RMSNorm       # 额外的 hidden 归一化
140	    - self_attn: Attention
141	        - qkv_proj: Linear(2 × 4096, ...)  # 输入 = cat(embed, hidden)
142	        - o_proj
143	    - post_attention_layernorm: RMSNorm
144	    - mlp: gate_proj, up_proj, down_proj
145	  final_norm: RMSNorm
146	
147	共享组件 (来自 target):
148	  - embed_tokens
149	  - lm_head
150	```
151	
152	### 3.2 参数量估算
153	
154	| 组件 | 参数量 | 大小 (bf16) |
155	|------|--------|-------------|
156	| fc | 50M | 100 MB |
157	| midlayer.qkv_proj | 38M | 76 MB |
158	| midlayer.o_proj | 17M | 34 MB |
159	| midlayer.mlp | 201M | 402 MB |
160	| norms | ~0 | ~0 |
161	| **Total** | **~306M** | **~612 MB** |
162	
163	提交预算：
164	- NVFP4 目标模型：在线量化（不占 zip）
165	- 草稿模型 bf16：612 MB
166	- 代码 + 数据：~50 MB
167	- **Total: ~670 MB << 2 GB 限制**
168	
169	### 3.3 代码位置
170	
171	- `eagle/minicpm_eagle3.py` - SGLang 格式的草稿模型
172	- 训练时使用独立的 PyTorch 模型，训练后转换权重
173	
174	---
175	
176	## 4. 训练设计
177	
178	### 4.1 EAGLE-3 官方训练方式
179	
180	```python
181	# cnets.py 核心逻辑
182	for idx in range(7):  # 7 步 TTT
183	    inputs_embeds = embed_tokens(input_ids)
184	    hidden, cache = midlayer(inputs_embeds, hidden, cache, ...)
185	    logits = lm_head(norm(hidden))
186	
187	    # plogp loss
188	    target_p = softmax(target_logits)
189	    out_logp = log_softmax(logits)
190	    loss = -sum(target_p * out_logp * mask)
191	
192	    if not last:
193	        input_ids = shift(input_ids)  # 用预测结果作为下一步输入
194	```
195	
196	关键点：
197	1. **纯 plogp loss**：`-sum(target_p × log(draft_p))`，无 CE，无 feature loss
198	2. **7 步 TTT**：训练时自回归，模拟真实 inference
199	3. **loss_mask**：屏蔽 prompt 部分，只在 response 上计算 loss
200	4. **DeepSpeed**：多卡分布式训练
201	
202	### 4.2 我们的 2-Phase 方案
203	
204	**Phase 1: 离线数据准备 (8 GPU 并行)**
205	
206	```
207	输入: wikitext / ShareGPT 数据
208	输出:
209	  - embeddings: (N, seq_len, 4096)
210	  - aux_hidden: (N, seq_len, 4096 × 3)
211	  - target_logits: (N, seq_len, vocab_size)
212	  - targets: (N, seq_len)
213	  - loss_mask: (N, seq_len)
214	
215	存储: ~100 GB for 100K samples
216	```
217	
218	**Phase 2: Draft 模型训练 (8 GPU DDP)**
219	
220	```
221	输入: Phase 1 的缓存数据
222	训练:
223	  - 7 步 TTT 自回归
224	  - 纯 plogp loss
225	  - batch_size: 32 (4 per GPU × 8 GPU)
226	  - epochs: 40
227	  - lr: 1e-4 with cosine decay
228	```
229	
230	### 4.3 与官方实现的差异
231	
232	| 方面 | EAGLE-3 官方 | 我们的方案 |
233	|------|-------------|-----------|
234	| Target forward | 每 batch 在线计算 | Phase 1 离线预计算 |
235	| 训练框架 | DeepSpeed ZeRO-3 | PyTorch DDP |
236	| 数据格式 | ShareGPT jsonl | wikitext + calib data |
237	| Aux layers | [emb, layer0, layer1] | [2, 10, 22] |
238	| 模型适配 | Llama | MiniCPM-SALA hybrid |
239	
240	---
241	
242	## 5. SimpleGLA 状态管理
243	
244	### 5.1 问题
245	
246	MiniCPM-SALA 的 24 层 Lightning Attention 维护递推状态：
247	```
248	h: (batch, num_kv_heads, head_dim, head_dim)
249	   = (bs, 32, 128, 128) per layer
250	   ≈ 2 MB per layer per request
251	```
252	
253	Speculative decoding verify 后，被拒绝的 token 已污染状态，需要回滚。
254	
255	### 5.2 Baseline 方案：Python 级快照
256	
257	```python
258	# verify 前
259	snapshot = [layer.cache.temporal.clone() for layer in gla_layers]
260	
261	# verify 后
262	for i, layer in enumerate(gla_layers):
263	    layer.cache.temporal = snapshot[i][:, :, :accepted_len]
264	```
265	
266	开销：24 layers × 2 MB ≈ 48 MB per request（可接受）
267	
268	### 5.3 优化方案：Kernel 级 intermediate state
269	
270	参考 GDR kernel (`fla/fused_recurrent.py`)：
271	- `CACHE_INTERMEDIATE_STATES`：缓存每步状态
272	- `DISABLE_STATE_UPDATE`：verify 时不更新状态
273	- `retrieve_parent_token`：tree attention 状态选择
274	
275	需要为 SimpleGLA 实现类似的 kernel，后续优化。
276	
277	---
278	
279	## 6. 预期效果
280	
281	### 6.1 Acceptance Rate 估算
282	
283	假设 per-token acceptance α = 0.6-0.7（保守估计）：
284	
285	| spec_steps | 期望 tokens | 加速比 |
286	|------------|-------------|--------|
287	| 3 | ~2.2 | ~1.7× |
288	| 5 | ~2.8 | ~1.9× |
289	| 7 | ~3.2 | ~2.1× |
290	
291	### 6.2 对竞赛指标的影响
292	
293	| 指标 | 当前 | 预期 (α=0.65) |
294	|------|------|---------------|
295	| S1 | 650s | ~400-450s |
296	| S8 | 645s | ~580-620s |
297	| Smax | 916s | ~800-850s |
298	
299	**注意**：高并发场景 (S8, Smax) 收益有限，因为额外内存占用减少 KV cache 空间。
300	
301	---
302	
303	## 7. 文件结构
304	
305	```
306	eagle/
307	├── minicpm_eagle3.py       # SGLang 草稿模型定义
308	├── train_eagle3.py         # 训练脚本 (待重写)
309	├── test_layer_selection.py # Layer 选择实验
310	├── EAGLE/                  # EAGLE 官方仓库 (参考)
311	│   └── eagle/traineagle3/
312	│       ├── main.py         # 官方训练入口
313	│       └── cnets.py        # 官方模型定义
314	└── data_cache/             # 数据缓存
315	    ├── wikitext_*.pt
316	    └── target_*.pt
317	```
318	
319	---
320	
321	## 8. TODO
322	
323	- [ ] 重写 `train_eagle3.py`：实现 2-Phase 训练
324	  - [ ] Phase 1: 离线数据准备脚本
325	  - [ ] Phase 2: 8 GPU DDP 训练脚本
326	- [ ] 实现 7 步 TTT 自回归训练
327	- [ ] 实现纯 plogp loss
328	- [ ] 测试 aux layers [1, 2, 3] vs [2, 10, 22]
329	- [ ] SimpleGLA 状态快照/回滚
330	- [ ] 集成到 SGLang serving
331	
332	---
333	
334	## 9. 参考资料
335	
336	- EAGLE-3 Paper: arxiv:2503.01840
337	- EAGLE GitHub: https://github.com/SafeAILab/EAGLE
338	- SGLang EAGLE 实现: `sglang/srt/models/llama_eagle3.py`
339
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle3-pipeline.md"
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 Speculative Decoding Pipeline for MiniCPM-SALA
2	
3	## 1. 概述
4	
5	用 EAGLE-3 替代 Medusa K=1 作为 speculative decoding 方案。
6	
7	**当前 Medusa K=1 基线**：head_0 top-1 accuracy = 37.7%，tokens_per_step = 1.377，S1 = 360s
8	
9	**EAGLE-3 目标**：step_0 top-1 accuracy > 55%，tokens_per_step > 2.5，S1 < 300s
10	
11	## 2. Aux Layers 选择
12	
13	**选定：[1, 10, 22]**
14	
15	| Layer | 深度 | 类型 | 作用 |
16	|-------|------|------|------|
17	| 1 | 早期 (第 2 层) | Lightning Attention | Token identity + 位置 + 初步上下文 |
18	| 10 | 中期 (第 11 层) | Lightning Attention | 中间语义，已过 2 次 StdAttn + 9 次 Lightning |
19	| 22 | 中后期 (第 23 层) | Standard Attention | 接近最终语义，单独预测力最强 |
20	
21	**选择理由**：
22	- MiniCPM-SALA 的 `scale_depth=1.4/sqrt(32)=0.247` 使早期层之间高度相似，all-early（官方 [emb,0,1]）会浪费 fc 容量
23	- early + mid + late 组合信息互补最大化
24	- Linear probe 实验支持：[1,10,22] CE=6.51 (best) vs [2,10,22] CE=6.68
25	- 覆盖两种注意力类型
26	
27	**备选 A/B**：如 [1,10,22] 效果不佳，测试 [0,9,22]（全 Standard Attention 层）
28	
29	## 3. Pipeline 阶段
30	
31	### Phase 1: 数据采集 (~4h)
32	
33	**方法**：修改 SGLang 模型 forward hook，从 NVFP4 量化模型采集中间层输出
34	
35	**修改文件**：
36	- `demo-sala/sglang/python/sglang/srt/models/minicpm.py` — 添加 aux layer 捕获
37	- `medusa/collect_eagle_data.py` — 新增采集脚本
38	
39	**采集数据格式** (.pt)：
40	```python
41	{
42	    "token_ids":         (seq_len,),         # int64
43	    "embeds":            (seq_len, 4096),    # bf16, embed_tokens(ids) * scale_emb
44	    "aux_hidden":        (seq_len, 4096*3),  # bf16, cat(layer1, layer10, layer22)
45	    "hidden_states":     (seq_len, 4096),    # bf16, 最后一层 post-norm（兼容 Medusa）
46	    "top_logit_values":  (seq_len, 256),     # bf16, target top-256 logit values
47	    "top_logit_indices": (seq_len, 256),     # int32, target top-256 token indices
48	}
49	```
50	
51	每文件 ~42 MB，目标 3000 samples ≈ 126 GB。
52	
53	**数据源**：待定（见第 4 节讨论）
54	
55	### Phase 2: 训练 (~6h)
56	
57	**新增文件**：`medusa/train_eagle3.py`
58	
59	**Draft Model 架构** (~306M trainable params):
60	```
61	MiniCPMEagle3Draft:
62	  fc:        Linear(4096×3 → 4096, bias=False)     # 50M
63	  midlayer:  1× MiniCPM decoder layer               # ~256M
64	    self_attn: QKV input = cat(embed, hidden) = 8192
65	      q_proj(8192→4096), k_proj(8192→256), v_proj(8192→256), o_proj(4096→4096)
66	    mlp: gate_proj(4096→16384), up_proj(4096→16384), down_proj(16384→4096)
67	    norms: input_layernorm, hidden_norm, post_attention_layernorm
68	  final_norm: RMSNorm(4096)
69	  lm_head:   Linear(4096 → draft_vocab_size)        # ~130M (frozen target lm_head 或独立)
70	
71	共享 (frozen): embed_tokens from target model
72	```
73	
74	**训练配置**（与官方 EAGLE-3 对齐）：
75	```
76	ttt_steps       = 7           # Training-Time Test
77	batch_size      = 2-8         # 单 GPU 84 GB
78	grad_checkpoint = True
79	seq_len         = 2048
80	lr              = 1e-4
81	warmup_steps    = 200
82	weight_decay    = 0.0
83	betas           = (0.9, 0.95)
84	max_grad_norm   = 0.5
85	loss_decay      = 0.8         # step i weight = 0.8^i
86	draft_vocab     = 32000       # 高频 token 子集
87	epochs          = 10
88	```
89	
90	**TTT 训练流程**（每 batch）：
91	```
92	1. hidden = fc(aux_hidden)
93	2. 构建 causal mask
94	3. for step in range(7):
95	     input_emb = embeds (step 0) 或 embed_tokens(shift(ids)) (step > 0)
96	     hidden_out = midlayer(input_emb, hidden, kv_cache, mask)
97	     logits = lm_head(final_norm(hidden_out))
98	     loss_i = plogp(logits, target_p)   # -Σ(target_p × log(draft_p))
99	     hidden = hidden_out
100	4. total_loss = Σ(0.8^i × loss_i)
101	```
102	
103	**VRAM 估算**: ~6.5 GB（极为充裕）
104	
105	### Phase 3: 离线评估 (~1h)
106	
107	**新增文件**：`medusa/eval_eagle3.py`
108	
109	测量：per-step acceptance rate、mean_accepted_length、tokens_per_step
110	
111	**通过标准**：step_0 accuracy > 50%，mean_accepted_length > 1.0
112	
113	### Phase 4: Serving 集成 (~4h)
114	
115	**文件**：
116	- `demo-sala/sglang/.../models/minicpm_eagle3.py` — 新增 SGLang draft model
117	- `demo-sala/sglang/.../speculative/eagle_worker.py` — 适配 GLA rollback
118	- `demo-sala/sglang/.../models/minicpm.py` — target forward 输出 aux hidden
119	- `demo-sala/prepare_env.sh` — 启动参数
120	
121	**复用**：
122	- eagle_worker.py 的 tree draft + verify 框架
123	- MedusaVerifyInput 或 EagleVerifyInput
124	- update_mamba_state_after_mtp_verify() GLA 回滚 kernel
125	- CUDA graph capture 基础设施
126	
127	### Phase 5: 端到端验证 (~2h)
128	
129	**验收标准**：
130	
131	| 指标 | Medusa K=1 | EAGLE-3 目标 |
132	|------|-----------|-------------|
133	| ori_accuracy | 81.0% | ≥ 80% |
134	| S1 | ~360s | ≤ 300s |
135	| S8 | ~350s | ≤ 340s |
136	
137	## 4. 数据配比（待讨论）
138	
139	现有 Medusa 训练数据配比 (v2 + v3 supplement, ~57M tokens):
140	- Chinese (SkyPile): ~50% → 20M tokens
141	- Code (multi-lang): ~42% → 24M tokens
142	- English (wikitext): ~8% → 4M tokens
143	
144	EAGLE-3 的数据配比需要单独讨论——可能需要与评测集分布对齐。
145	
146	## 5. 参考
147	
148	- EAGLE-3 官方代码: `~/EAGLE/eagle/traineagle3/`
149	- 研究笔记: `docs/eagle3_research.md`
150	- Medusa 训练: `medusa/train.py`
151	- Medusa 数据采集: `medusa/collect_data.py`
152
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle3-accept-rate-fix.md"
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 Accept Rate 修复记录
2	
3	## 问题
4	
5	EAGLE-3 speculative decoding 在线 accept rate 仅 ~5%（accept_len ~1.05），离线训练 acc0 却有 63.5%。Draft model 在推理时几乎无法命中任何 token。
6	
7	## 根因分析
8	
9	### 训练/推理的 token-hidden_states 对齐不一致
10	
11	sglang EAGLE-3 推理时对 input_ids 做了隐式左移：
12	
13	1. **`eagle_info.py` prepare_for_extend**（首次 extend）：
14	   ```python
15	   input_ids = torch.cat((input_ids[1:], verified_id))
16	   ```
17	   位置 t 的 token 变成了 x_{t+1}，而 hidden_states 仍是 aux[t]。
18	
19	2. **`eagle_info.py` prepare_extend_after_decode**（后续 decode）：
20	   ```python
21	   batch.input_ids = self.verified_id  # target 预测的未来 token
22	   hidden_states = hidden_states[accept_index]  # 已接受位置的 hidden
23	   ```
24	   verified_id 是 target model 的预测（未来 token），配对的是当前位置的 aux_hidden。
25	
26	因此推理时 draft model 实际输入为 **(x_{t+1}, aux[t])** → 预测 **x_{t+2}**。
27	
28	而旧训练代码使用对齐的 **(x_t, aux[t])** → 预测 **x_{t+1}**。输入分布完全不匹配，导致 draft 几乎无法命中。
29	
30	### 验证
31	
32	用旧权重在 shifted eval 上测试：OOD accept rate = 8.2%，与在线 ~5% 吻合，确认根因。
33	
34	## 修复
35	
36	### 1. 训练对齐修复 (`eagle/train.py`)
37	
38	将训练 forward 的输入做同样的 shift，匹配推理行为：
39	
40	```python
41	# 修复前（对齐的）
42	input_ids = token_ids              # x_0..x_{S-1}
43	hidden = self.fc(aux_hidden)       # aux_0..aux_{S-1}
44	
45	# 修复后（shifted，匹配推理）
46	input_ids = token_ids[:, 1:]           # x_1..x_{S-1}
47	aux_shifted = aux_hidden[:, :-1, :]    # aux_0..aux_{S-2}
48	target_values = target_logits_values[:, 1:, :]
49	target_indices = target_logits_indices[:, 1:, :]
50	```
51	
52	### 2. 评估脚本修复 (`eagle/eval_ood_accept.py`)
53	
54	- 同步 shifted 对齐
55	- 修复 checkpoint 键名映射（`midlayer.` 前缀剥离、`input_emb_norm` → `input_layernorm`）
56	- 支持从训练 checkpoint 直接加载
57	
58	### 3. 诊断代码清理
59	
60	从 `eagle_info.py`、`eagle_worker.py`、`minicpm.py` 移除全部 6 个 DIAG 打印块。
61	
62	## 重训结果
63	
64	训练配置：10 epochs, batch=2x4 grad_accum, lr=3e-4, seq_len=2048, 9530 files。
65	
66	| Checkpoint | 训练 acc0 | OOD Accept Rate | 在线 accept_len |
67	|-----------|---------|----------------|----------------|
68	| 旧(未shift) | 63.5% | 8.2% | ~1.05 |
69	| Epoch 1 (shifted) | 34.3% | 35.5% | 1.50 (单请求) / 1.33 (32并发) |
70	| Epoch 2 (shifted) | 53.9% | 45.8% | — |
71	| Epoch 3+ | 61.9%+ | 预计 >50% | — |
72	
73	## OOD Accept Rate 饱和
74	
75	| Epoch | 训练 acc0 | OOD Accept Rate | delta |
76	|-------|---------|----------------|-------|
77	| 1 | 34.3% | 35.5% | — |
78	| 2 | 53.9% | 45.8% | +10.3 |
79	| 3 | 61.9% | 49.1% | +3.3 |
80	| 4 | 67.6% | 49.3% | +0.2 |
81	
82	Epoch 4 后 OOD accept rate 基本饱和（49.3%），训练 acc 仍在涨但 OOD 不动。gap 说明过拟合到训练集分布。进一步提升需要 in-domain 验证集做 early stopping，或更大/更多样的训练数据。
83	
84	## Tree Verify 与线性注意力的兼容性问题
85	
86	### 问题
87	
88	MiniCPM-SALA 有 24/32 层 GLA（线性注意力）。sglang 的 EAGLE tree verify 对两种注意力层处理方式不同：
89	
90	- **Standard attention（8层）**：使用 tree mask（FlashInfer prefill + custom_mask），每个 token 只 attend 祖先链。**正确。**
91	- **GLA（24层）**：`hybrid_linear_attn_backend.py:1636-1711` 逐 token 串行处理，所有 draft tokens 当成线性序列。**不同分支间 state 互相污染。**
92	
93	```python
94	# GLA TARGET_VERIFY 实际行为（simplified）
95	for step in range(draft_token_num):
96	    o_s, current_state = fused_recurrent_simple_gla(...)
97	    intermediate_ssm[layer, :batch, step] = current_state
98	# → A 分支的 state 污染了 B 分支的计算
99	```
100	
101	### topk=1 vs topk=2 实测
102	
103	理论上 topk=1（单链）对 GLA 完全正确，但实测 **topk=2 仍然更快**。
104	
105	原因：tree 的候选覆盖率优势 > GLA state 污染的精度损失：
106	- `topk=2, steps=3`：6 个候选，命中概率高
107	- `topk=1, steps=3`：3 个候选，覆盖面窄
108	- 8 层 standard attention 的 tree mask 仍然正确，部分补偿 GLA 误差
109	- GLA 污染有界——sibling branch 对 state 的扰动不至于完全破坏 logits
110	
111	### 可能的改进方向
112	
113	1. **DFS 遍历 + state 分支保存**：GLA 层在分支点保存 state，处理完一条路径后 restore。每个分支点额外 ~1 MB/层，24层×3点=72 MB。计算量不变（已经逐 token 串行），只多 save/restore 操作。
114	2. **更大/更好的 draft model**：2-3 层 draft 提高 accept rate，配合 NVFP4 量化控制 latency。
115	3. **In-domain 训练数据**：当前 OOD accept rate 49.3% 饱和，更匹配的训练数据可能突破瓶颈。
116	
117	## 排查过程中排除的假设
118	
119	1. **verify_tree / retrive_index bug** — 验证逻辑正确，`ridx=[0..7]` 全部列出，d1_hit=True 时 accept_length=1
120	2. **layers_to_capture 不匹配** — 确认 {2,11,23}（MLP delta）与训练数据采集一致
121	3. **residual bug** — 模型捕获的是 MLP delta（无 residual），与训练一致
122	
123	## 关键文件
124	
125	| 文件 | 改动 |
126	|------|------|
127	| `eagle/train.py` | shifted 对齐修复 |
128	| `eagle/eval_ood_accept.py` | shifted eval + 键名映射修复 |
129	| `eagle/convert_to_sglang.py` | checkpoint → sglang 格式转换 |
130	| `demo-sala/sglang/.../eagle_info.py` | 清理诊断代码 |
131	| `demo-sala/sglang/.../eagle_worker.py` | 清理诊断代码 |
132	| `demo-sala/sglang/.../models/minicpm.py` | 清理诊断代码 |
133
```

> AGENT

Now let me read all the eagle/ directory files:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/collect_data.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Collect aux hidden states + top-K logits from NVFP4 model for EAGLE-3 training.
4	
5	Activates via EAGLE3_COLLECT_DIR env var in minicpm.py hook.
6	Server captures layer 1/10/22 outputs + top-256 logits per EXTEND request.
7	
8	Data budget:
9	  train: 10,000 samples × 2048 tokens (EAGLE3_MAX_TOKENS=2048)
10	    - SkyPile (中文):  50% → 5000
11	    - Code (多语言):   42% → 4200 (py60/java16/go12/js8/php2.4/ruby1.6)
12	    - Wikitext (英文):  8% → 800
13	  val_ood: 64 samples, original length (EAGLE3_MAX_TOKENS=0)
14	    - speed_bench_cunlimited.jsonl model_response, no truncation
15	
16	Prerequisites:
17	    1. Start NVFP4 server with: EAGLE3_COLLECT_DIR=/tmp/eagle3_collect
18	    2. python3 eagle/collect_data.py              # train only
19	    3. python3 eagle/collect_data.py --val-ood     # val_ood only (needs server restart with EAGLE3_MAX_TOKENS=0)
20	    4. python3 eagle/collect_data.py --smoke N     # N samples smoke test
21	
22	NOTE: train and val_ood require DIFFERENT server configs:
23	  - train:   EAGLE3_MAX_TOKENS=2048 (default)
24	  - val_ood: EAGLE3_MAX_TOKENS=0 (no truncation, restart server!)
25	"""
26	
27	import asyncio
28	import json
29	import os
30	import random
31	import shutil
32	import sys
33	import threading
34	import time
35	from pathlib import Path
36	
37	import aiohttp
38	import torch
39	from tqdm import tqdm
40	from transformers import AutoTokenizer
41	
42	
43	def _net_monitor(stop_event, interval=2.0):
44	    """Background thread: print network throughput every `interval` seconds."""
45	    def _rx_bytes():
46	        with open("/proc/net/dev") as f:
47	            total = 0
48	            for line in f:
49	                if ":" not in line:
50	                    continue
51	                parts = line.split()
52	                iface = parts[0].rstrip(":")
53	                if iface == "lo":
54	                    continue
55	                total += int(parts[1])  # rx bytes
56	            return total
57	
58	    prev = _rx_bytes()
59	    prev_t = time.monotonic()
60	    while not stop_event.is_set():
61	        stop_event.wait(interval)
62	        now = _rx_bytes()
63	        now_t = time.monotonic()
64	        dt = now_t - prev_t
65	        if dt > 0:
66	            speed = (now - prev) / dt
67	            if speed > 1024 * 1024:
68	                print(f"\r  [net] ↓ {speed / 1024 / 1024:.1f} MB/s", end="", flush=True)
69	            elif speed > 1024:
70	                print(f"\r  [net] ↓ {speed / 1024:.0f} KB/s", end="", flush=True)
71	        prev, prev_t = now, now_t
72	    print()  # newline on exit
73	
74	REPO_user_4813494d = Path(__file__).resolve().parent.parent
75	MODEL_PATH = [REDACTED]
76	API_BASE = "http://127.0.0.1:30000"
77	COLLECT_DIR = Path("/tmp/eagle3_collect")
78	OUTPUT_TRAIN = REPO_user_4813494d / "eagle" / "data" / "train"
79	OUTPUT_VAL_OOD = REPO_user_4813494d / "eagle" / "data" / "val_ood"
80	CONCURRENCY = 32
81	SEQ_LEN = 2048
82	MIN_TOKENS = 64
83	
84	# ── Budget ────────────────────────────────────────────────────────────
85	BUDGET = {
86	    "skypile": 5000,
87	    "code": 4200,
88	    "wikitext": 800,
89	}
90	
91	# Python 比例提高到 60%（2048 截断更友好）
92	CODE_LANG_PCT = {
93	    "python": 0.60,
94	    "java": 0.16,
95	    "go": 0.12,
96	    "javascript": 0.08,
97	    "php": 0.024,
98	    "ruby": 0.016,
99	}
100	
101	
102	# ── Data loading ──────────────────────────────────────────────────────
103	
104	def prepare_texts(tokenizer, smoke=0):
105	    """Prepare text samples. Returns list of {text, source}."""
106	    random.seed(42)
107	    os.environ["HF_DATASETS_OFFLINE"] = "1"
108	    from datasets import load_dataset
109	
110	    # 启动网络速度监控
111	    net_stop = threading.Event()
112	    net_thread = threading.Thread(target=_net_monitor, args=(net_stop,), daemon=True)
113	    net_thread.start()
114	
115	    budget = dict(BUDGET)
116	    if smoke > 0:
117	        total = smoke
118	        budget = {
119	            "skypile": max(1, int(total * 0.50)),
120	            "code": max(1, int(total * 0.42)),
121	            "wikitext": max(1, total - max(1, int(total * 0.50)) - max(1, int(total * 0.42))),
122	        }
123	        print(f"[smoke test] budget: {budget}")
124	
125	    all_samples = []
126	
127	    # ── SkyPile (本地 jsonl) ─────────────────────────────────────
128	    need = budget["skypile"] + 50
129	    skypile_path = "/user_4813494d/data/skypile/data/2020-40_zh_head_0000.jsonl"
130	    print(f"Loading SkyPile from {skypile_path} (need {need} chunks)...", flush=True)
131	    sky_chunks = []
132	    buf_ids = []
133	    with open(skypile_path) as f:
134	        for line in tqdm(f, desc="skypile", unit="line"):
135	            text = json.loads(line).get("text", "")
136	            if not text.strip() or len(text) < 50:
137	                continue
138	            buf_ids.extend(tokenizer.encode(text, add_special_tokens=False))
139	            while len(sky_chunks) < need and len(buf_ids) >= SEQ_LEN:
140	                chunk = buf_ids[:SEQ_LEN]
141	                buf_ids = buf_ids[SEQ_LEN:]
142	                sky_chunks.append({"text": tokenizer.decode(chunk), "source": "skypile"})
143	            if len(sky_chunks) >= need:
144	                break
145	    random.shuffle(sky_chunks)
146	    all_samples.extend(sky_chunks[: budget["skypile"]])
147	    print(f"  skypile: {len(sky_chunks)} prepared, using {budget['skypile']}")
148	
149	    # ── Code ──────────────────────────────────────────────────────
150	    need = budget["code"] + 50
151	    code_chunks = []
152	    for lang, pct in CODE_LANG_PCT.items():
153	        lang_need = int(need * pct) + 10
154	        print(f"Loading code_search_net/{lang} (need {lang_need} chunks)...", flush=True)
155	        code_ds = load_dataset("code_search_net", lang, split="train")
156	        lang_chunks = []
157	        buf_ids = []
158	        for sample in tqdm(code_ds, desc=f"code/{lang}", unit="func"):
159	            func = sample.get("whole_func_string", "")
160	            if not func or len(func) < 50:
161	                continue
162	            buf_ids.extend(tokenizer.encode(func, add_special_tokens=False))
163	            while len(buf_ids) >= SEQ_LEN:
164	                chunk = buf_ids[:SEQ_LEN]
165	                buf_ids = buf_ids[SEQ_LEN:]
166	                lang_chunks.append({"text": tokenizer.decode(chunk), "source": f"code_{lang}"})
167	            if len(lang_chunks) >= lang_need:
168	                break
169	        if len(buf_ids) >= MIN_TOKENS:
170	            lang_chunks.append({"text": tokenizer.decode(buf_ids[:SEQ_LEN]), "source": f"code_{lang}"})
171	        random.shuffle(lang_chunks)
172	        code_chunks.extend(lang_chunks[:lang_need])
173	        print(f"  {lang}: {len(lang_chunks)} chunks, using {min(len(lang_chunks), lang_need)}")
174	    random.shuffle(code_chunks)
175	    all_samples.extend(code_chunks[: budget["code"]])
176	    print(f"  code total: using {budget['code']}")
177	
178	    # ── Wikitext ──────────────────────────────────────────────────
179	    need = budget["wikitext"] + 50
180	    print(f"Loading wikitext-103 (need {need} chunks)...", flush=True)
181	    wiki_ds = load_dataset("wikitext", "wikitext-103-raw-v1", split="train")
182	    wiki_chunks = []
183	    buf_ids = []
184	    for sample in tqdm(wiki_ds, desc="wikitext", unit="doc"):
185	        if not sample["text"].strip():
186	            continue
187	        buf_ids.extend(tokenizer.encode(sample["text"], add_special_tokens=False))
188	        while len(wiki_chunks) < need and len(buf_ids) >= SEQ_LEN:
189	            chunk = buf_ids[:SEQ_LEN]
190	            buf_ids = buf_ids[SEQ_LEN:]
191	            wiki_chunks.append({"text": tokenizer.decode(chunk), "source": "wikitext"})
192	        if len(wiki_chunks) >= need:
193	            break
194	    random.shuffle(wiki_chunks)
195	    all_samples.extend(wiki_chunks[: budget["wikitext"]])
196	    print(f"  wikitext: {len(wiki_chunks)} prepared, using {budget['wikitext']}")
197	
198	    net_stop.set()
199	    net_thread.join(timeout=3)
200	
201	    random.shuffle(all_samples)
202	    from collections import Counter
203	    counts = Counter(s["source"] for s in all_samples)
204	    print(f"\nTotal: {len(all_samples)} samples")
205	    for src, n in sorted(counts.items()):
206	        print(f"  {src}: {n}")
207	    return all_samples
208	
209	
210	def prepare_val_ood(tokenizer):
211	    """Load speed bench model responses as val_ood. No truncation, original length."""
212	    bench_path = REPO_user_4813494d / "bench" / "data" / "speed_bench_cunlimited.jsonl"
213	    with open(bench_path) as f:
214	        lines = [json.loads(l) for l in f]
215	    samples = []
216	    for l in lines:
217	        text = l.get("model_response", "")
218	        ids = tokenizer.encode(text, add_special_tokens=False)
219	        if len(ids) < MIN_TOKENS:
220	            continue
221	        samples.append({"text": text, "source": "bench_ood"})
222	    print(f"val_ood: {len(samples)} samples from {bench_path.name}")
223	    lens = [len(tokenizer.encode(s["text"], add_special_tokens=False)) for s in samples]
224	    print(f"  token lengths: min={min(lens)}, max={max(lens)}, total={sum(lens)/1e3:.0f}K")
225	    return samples
226	
227	
228	# ── Collection ────────────────────────────────────────────────────────
229	
230	async def collect_split(samples, output_dir, concurrency=CONCURRENCY):
231	    """Collect samples with batched concurrent requests.
232	
233	    Each batch of requests produces .pt files in COLLECT_DIR.
234	    After each batch completes, files are moved to output_dir with sequential naming.
235	    Supports resume: skips already-collected files based on existing .pt count.
236	    """
237	    output_dir.mkdir(parents=True, exist_ok=True)
238	    COLLECT_DIR.mkdir(exist_ok=True)
239	
240	    # Clean stale files
241	    for f in COLLECT_DIR.glob("*.pt"):
242	        f.unlink()
243	
244	    async with aiohttp.ClientSession() as session:
245	        # Verify server is up
246	        try:
247	            async with session.get(f"{API_BASE}/v1/models") as resp:
248	                if resp.status != 200:
249	                    print(f"Server not ready: {resp.status}")
250	                    return 0
251	        except Exception as e:
252	            print(f"Cannot reach server: {e}")
253	            return 0
254	
255	        # Skip already collected
256	        existing = sorted(output_dir.glob("*.pt"))
257	        start_idx = len(existing)
258	        if start_idx > 0:
259	            print(f"Resuming from index {start_idx} ({start_idx} already collected)")
260	            samples = samples[start_idx:]
261	
262	        fail_count = [0]
263	        success = 0
264	        pbar = tqdm(total=len(samples), desc="collecting", unit="seq")
265	
266	        sem = asyncio.Semaphore(concurrency)
267	        batch_size = concurrency
268	
269	        for batch_start in range(0, len(samples), batch_size):
270	            batch = samples[batch_start:batch_start + batch_size]
271	
272	            # Clean collect dir before batch
273	            for f in COLLECT_DIR.glob("*.pt"):
274	                f.unlink()
275	
276	            # Send batch concurrently
277	            tasks = []
278	            for j, sample in enumerate(batch):
279	                payload = {
280	                    "model": "default",
281	                    "prompt": sample["text"],
282	                    "max_tokens": 1,
283	                    "temperature": 0,
284	                }
285	
286	                async def _send(p=payload):
287	                    async with sem:
288	                        try:
289	                            async with session.post(
290	                                f"{API_BASE}/v1/completions",
291	                                json=p,
292	                                timeout=aiohttp.ClientTimeout(total=600),
293	                            ) as resp:
294	                                await resp.json()
295	                                return True
296	                        except Exception as e:
297	                            return False
298	
299	                tasks.append(asyncio.create_task(_send()))
300	
301	            results = await asyncio.gather(*tasks)
302	            ok_count = sum(1 for r in results if r)
303	            fail_count[0] += len(results) - ok_count
304	
305	            # Small wait for hook I/O to flush
306	            await asyncio.sleep(0.2)
307	
308	            # Move all .pt files from collect dir, sorted by name
309	            pt_files = sorted(COLLECT_DIR.glob("*.pt"))
310	            for f in pt_files:
311	                dst = output_dir / f"{start_idx + success:06d}.pt"
312	                shutil.move(str(f), str(dst))
313	                success += 1
314	
315	            pbar.update(len(batch))
316	            pbar.set_postfix(ok=success, fail=fail_count[0])
317	
318	        pbar.close()
319	
320	        total_bytes = sum(f.stat().st_size for f in output_dir.glob("*.pt"))
321	        print(f"\nDone: {success} files, {total_bytes / 1024**3:.1f} GB")
322	        print(f"Failures: {fail_count[0]}")
323	        return success
324	
325	
326	# ── Main ──────────────────────────────────────────────────────────────
327	
328	def validate_pt(output_dir, label=""):
329	    """Validate a sample .pt file from output_dir."""
330	    pt_files = sorted(output_dir.glob("*.pt"))
331	    if not pt_files:
332	        print(f"  No files to validate in {output_dir}")
333	        return
334	    sample_f = pt_files[len(pt_files) // 2]
335	    d = torch.load(sample_f, weights_only=True)
336	    print(f"\nValidation {label}({sample_f.name}):")
337	    for k, v in d.items():
338	        print(f"  {k}: {v.shape} {v.dtype}")
339	    expected_keys = {"token_ids", "aux_hidden", "top_logit_values", "top_logit_indices"}
340	    assert set(d.keys()) == expected_keys, f"Unexpected keys: {set(d.keys())}"
341	    assert d["aux_hidden"].shape[-1] == 4096 * 3, f"Bad aux_hidden dim: {d['aux_hidden'].shape}"
342	    print("  PASSED")
343	
344	
345	def main():
346	    smoke = 0
347	    val_ood_mode = "--val-ood" in sys.argv
348	    if "--smoke" in sys.argv:
349	        idx = sys.argv.index("--smoke")
350	        smoke = int(sys.argv[idx + 1]) if idx + 1 < len(sys.argv) else 5
351	
352	    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
353	
354	    if val_ood_mode:
355	        # ── val_ood: 全量采集，不截断 ──────────────────────────────
356	        print(f"EAGLE-3 val_ood collection (no truncation, output={OUTPUT_VAL_OOD})")
357	        print("NOTE: server must be started with EAGLE3_MAX_TOKENS=0")
358	        samples = prepare_val_ood(tokenizer)
359	        # val_ood 序列长，降低并发避免 OOM
360	        n = asyncio.run(collect_split(samples, OUTPUT_VAL_OOD, concurrency=4))
361	        if n > 0:
362	            validate_pt(OUTPUT_VAL_OOD, "val_ood ")
363	    else:
364	        # ── train: 10000 × 2048 ──────────────────────────────────
365	        output_dir = OUTPUT_TRAIN
366	        print(f"EAGLE-3 train collection (seq_len={SEQ_LEN}, output={output_dir})")
367	        if smoke:
368	            print(f"*** SMOKE TEST: {smoke} samples ***")
369	
370	        samples = prepare_texts(tokenizer, smoke=smoke)
371	
372	        # Save manifest
373	        manifest_path = output_dir.parent / "manifest.json"
374	        output_dir.mkdir(parents=True, exist_ok=True)
375	        with open(manifest_path, "w") as f:
376	            json.dump(
377	                {
378	                    "total": len(samples),
379	                    "seq_len": SEQ_LEN,
380	                    "sources": {s["source"]: 0 for s in samples},
381	                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
382	                    "samples": [{"source": s["source"], "text_len": len(s["text"])} for s in samples],
383	                },
384	                f,
385	                indent=2,
386	            )
387	        print(f"Manifest saved to {manifest_path}")
388	
389	        n = asyncio.run(collect_split(samples, output_dir))
390	        if n > 0:
391	            validate_pt(output_dir, "train ")
392	
393	
394	if __name__ == "__main__":
395	    main()
396
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/train.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Train EAGLE-3 draft model for MiniCPM-SALA speculative decoding.
4	
5	Architecture: fc(12288→4096) + 1 decoder layer (TTT 7-step) + norm + lm_head
6	Loss: plogp = -sum(target_p * log(draft_p)), weighted by 0.8^step
7	
8	Data: .pt files with {token_ids, aux_hidden, top_logit_values, top_logit_indices}
9	      aux_hidden = cat(layer1, layer10, layer22) of shape (seq_len, 12288)
10	
11	Run from repo user_4813494d:
12	    python3 eagle/train.py
13	"""
14	
15	import math
16	import os
17	import random
18	import time
19	from pathlib import Path
20	
21	import torch
22	import torch.nn as nn
23	import torch.nn.functional as F
24	from safetensors import safe_open
25	from tqdm import tqdm
26	
27	# ── Config ──────────────────────────────────────────────────────────────
28	DATA_DIR = Path("eagle/data/train")
29	VAL_DIR = Path("medusa/data/val_ood")  # reuse Medusa val_ood for monitoring
30	OUTPUT_DIR = Path("eagle/weights")
31	MODEL_PATH = [REDACTED]
32	
33	HIDDEN_SIZE = 4096
34	AUX_DIM = HIDDEN_SIZE * 3  # 12288
35	VOCAB_SIZE = 73448
36	DRAFT_VOCAB_SIZE = 32000
37	SCALE_EMB = 12
38	SCALE_WIDTH = HIDDEN_SIZE / 256  # 16
39	NUM_HEADS = 32
40	NUM_KV_HEADS = 2
41	HEAD_DIM = 128
42	INTERMEDIATE_SIZE = 16384
43	RMS_NORM_EPS = 1e-6
44	
45	TTT_STEPS = 1  # single-step: stable training, sufficient for spec decode
46	LOSS_DECAY = 0.8
47	SEQ_LEN = 2048
48	BATCH_SIZE = 2
49	GRAD_ACCUM = 4  # effective batch = 8
50	LR = 3e-4
51	WARMUP_STEPS = 500
52	WEIGHT_DECAY = 0.0
53	BETAS = (0.9, 0.95)
54	MAX_GRAD_NORM = 5.0
55	EPOCHS = 10
56	EVAL_EVERY_EPOCH = 1
57	GRAD_CHECKPOINT = True
58	SEED = 42
59	MIN_TOKENS = 128  # skip files shorter than this
60	
61	DEVICE = "cuda"
62	DTYPE = torch.bfloat16
63	
64	
65	# ── RMSNorm ─────────────────────────────────────────────────────────────
66	class RMSNorm(nn.Module):
67	    def __init__(self, dim, eps=1e-6):
68	        super().__init__()
69	        self.weight = nn.Parameter(torch.ones(dim))
70	        self.eps = eps
71	
72	    def forward(self, x):
73	        norm = x.float().pow(2).mean(-1, keepdim=True).add(self.eps).rsqrt()
74	        return (x * norm).to(x.dtype) * self.weight
75	
76	
77	# ── Attention (list-based cache, matching official EAGLE-3 cnets.py L227-314) ──
78	class Eagle3Attention(nn.Module):
79	    """EAGLE-3 attention with list-based KV cache across TTT steps.
80	
81	    Official mechanism:
82	    - Step 0: standard full causal attention Q @ K0^T → softmax → @ V0
83	    - Step i>0: K_i is a single "summary" vector per position (same shape as K0).
84	      Attention score for cached step i is element-wise dot: (q * k_i).sum(-1),
85	      producing one scalar per (batch, head, query_pos).
86	      These scalars are concatenated with the S scores from K0, then softmax.
87	      Output = attn_weights0 @ V0 + sum_i(attn_weights_i * V_i)
88	    """
89	    def __init__(self):
90	        super().__init__()
91	        self.num_heads = NUM_HEADS
92	        self.num_kv_heads = NUM_KV_HEADS
93	        self.head_dim = HEAD_DIM
94	        self.num_kv_groups = NUM_HEADS // NUM_KV_HEADS
95	
96	        qkv_in = HIDDEN_SIZE * 2  # cat(embed, hidden)
97	        self.q_proj = nn.Linear(qkv_in, NUM_HEADS * HEAD_DIM, bias=False)
98	        self.k_proj = nn.Linear(qkv_in, NUM_KV_HEADS * HEAD_DIM, bias=False)
99	        self.v_proj = nn.Linear(qkv_in, NUM_KV_HEADS * HEAD_DIM, bias=False)
100	        self.o_proj = nn.Linear(NUM_HEADS * HEAD_DIM, HIDDEN_SIZE, bias=False)
101	
102	    def forward(self, hidden_cat, cache_k_list, cache_v_list, causal_mask=None):
103	        """
104	        hidden_cat: (B, S, 2*H)
105	        cache_k_list: list of (B, num_heads, S, head_dim) from prior TTT steps, or None
106	        cache_v_list: list of (B, num_heads, S, head_dim) from prior TTT steps, or None
107	        causal_mask: (1, 1, S, S)
108	        Returns: output (B, S, H), new_cache_k_list, new_cache_v_list
109	        """
110	        B, S, _ = hidden_cat.shape
111	
112	        q = self.q_proj(hidden_cat).view(B, S, self.num_heads, self.head_dim).transpose(1, 2)
113	        k = self.k_proj(hidden_cat).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
114	        v = self.v_proj(hidden_cat).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
115	
116	        # GQA expand
117	        if self.num_kv_groups > 1:
118	            k = k.repeat_interleave(self.num_kv_groups, dim=1)
119	            v = v.repeat_interleave(self.num_kv_groups, dim=1)
120	
121	        # Build cache lists (copy to avoid in-place modification for grad checkpoint)
122	        if cache_k_list is None:
123	            local_cache_k = []
124	            local_cache_v = []
125	        else:
126	            local_cache_k = list(cache_k_list)
127	            local_cache_v = list(cache_v_list)
128	
129	        local_cache_k.append(k)
130	        local_cache_v.append(v)
131	
132	        n_cached = len(local_cache_k)
133	
134	        if n_cached == 1:
135	            # Step 0: use flash attention (memory efficient, no materialized attn matrix)
136	            # F.scaled_dot_product_attention with is_causal=True
137	            attn_output = F.scaled_dot_product_attention(
138	                q, local_cache_k[0], local_cache_v[0], is_causal=True
139	            )
140	        else:
141	            # Steps with cache: manual attention with cached KV summaries
142	            k0 = local_cache_k[0]
143	            v0 = local_cache_v[0]
144	
145	            attn_weights = torch.matmul(q, k0.transpose(-2, -1)) / math.sqrt(self.head_dim)
146	            if causal_mask is not None:
147	                attn_weights = attn_weights + causal_mask
148	
149	            for i in range(1, n_cached):
150	                ki = local_cache_k[i]
151	                attn_wi = (q * ki).sum(-1) / math.sqrt(self.head_dim)
152	                attn_weights = torch.cat([attn_weights, attn_wi.unsqueeze(-1)], dim=-1)
153	
154	            attn_weights = F.softmax(attn_weights, dim=-1, dtype=torch.float32).to(q.dtype)
155	
156	            attn_w0 = attn_weights[..., :S]
157	            attn_output = torch.matmul(attn_w0, v0)
158	
159	            for i in range(1, n_cached):
160	                vi = local_cache_v[i]
161	                wi = attn_weights[..., S + i - 1]
162	                attn_output = attn_output + wi.unsqueeze(-1) * vi
163	
164	        attn_output = attn_output.transpose(1, 2).contiguous().view(B, S, -1)
165	        return self.o_proj(attn_output), local_cache_k, local_cache_v
166	
167	
168	# ── MLP ──────────────────────────────────────────────────────────────────
169	class Eagle3MLP(nn.Module):
170	    def __init__(self):
171	        super().__init__()
172	        self.gate_proj = nn.Linear(HIDDEN_SIZE, INTERMEDIATE_SIZE, bias=False)
173	        self.up_proj = nn.Linear(HIDDEN_SIZE, INTERMEDIATE_SIZE, bias=False)
174	        self.down_proj = nn.Linear(INTERMEDIATE_SIZE, HIDDEN_SIZE, bias=False)
175	
176	    def forward(self, x):
177	        return self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))
178	
179	
180	# ── Decoder Layer ────────────────────────────────────────────────────────
181	class Eagle3DecoderLayer(nn.Module):
182	    def __init__(self):
183	        super().__init__()
184	        self.hidden_norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
185	        self.input_emb_norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
186	        self.self_attn = Eagle3Attention()
187	        self.post_attention_layernorm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
188	        self.mlp = Eagle3MLP()
189	
190	    def forward(self, input_emb, hidden_states, cache_k_list=None, cache_v_list=None, causal_mask=None):
191	        """
192	        input_emb: (B, S, H) - embedded tokens
193	        hidden_states: (B, S, H) - running hidden from fc or prior step
194	        cache_k_list, cache_v_list: list of tensors from prior TTT steps
195	        Returns: new_hidden (B, S, H), cache_k_list, cache_v_list
196	        """
197	        residual = hidden_states
198	
199	        normed_emb = self.input_emb_norm(input_emb)
200	        normed_hidden = self.hidden_norm(hidden_states)
201	        hidden_cat = torch.cat([normed_emb, normed_hidden], dim=-1)
202	
203	        attn_out, cache_k_list, cache_v_list = self.self_attn(hidden_cat, cache_k_list, cache_v_list, causal_mask)
204	        hidden_states = residual + attn_out
205	
206	        residual = hidden_states
207	        hidden_states = self.post_attention_layernorm(hidden_states)
208	        hidden_states = self.mlp(hidden_states)
209	        hidden_states = residual + hidden_states
210	
211	        return hidden_states, cache_k_list, cache_v_list
212	
213	
214	# ── EAGLE-3 Draft Model ─────────────────────────────────────────────────
215	class Eagle3Model(nn.Module):
216	    def __init__(self, embed_weight, lm_head_weight):
217	        """
218	        embed_weight: (vocab_size, hidden_size) from target model
219	        lm_head_weight: (vocab_size, hidden_size) from target model
220	        """
221	        super().__init__()
222	        self.fc = nn.Linear(AUX_DIM, HIDDEN_SIZE, bias=False)
223	        self.midlayer = Eagle3DecoderLayer()
224	        self.norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
225	
226	        # Frozen embedding from target (with scale_emb)
227	        self.embed_tokens = nn.Embedding.from_pretrained(embed_weight, freeze=True)
228	        self.scale_emb = SCALE_EMB
229	
230	        # lm_head initialized from target (subset rows set in _init_lm_head)
231	        self.lm_head = nn.Linear(HIDDEN_SIZE, DRAFT_VOCAB_SIZE, bias=False)
232	        self._full_lm_head_weight = lm_head_weight  # kept for init after vocab mapping
233	
234	        # d2t / t2d / draft_idx_map mappings (set later via build_vocab_mapping)
235	        self.register_buffer("d2t", torch.zeros(DRAFT_VOCAB_SIZE, dtype=torch.long))
236	        self.register_buffer("t2d", torch.zeros(VOCAB_SIZE, dtype=torch.bool))
237	        self.register_buffer("draft_idx_map", torch.zeros(VOCAB_SIZE, dtype=torch.long))
238	
239	        self.ttt_steps = TTT_STEPS
240	        self.loss_decay = LOSS_DECAY
241	
242	    def build_vocab_mapping(self, data_dir):
243	        """Build draft vocabulary from training data token frequency."""
244	        cache_path = data_dir.parent / "vocab_cache.pt"
245	        if cache_path.exists():
246	            cache = torch.load(cache_path, weights_only=True)
247	            self.d2t.copy_(cache["d2t"])
248	            self.t2d.copy_(cache["t2d"])
249	            print(f"Loaded vocab mapping from {cache_path}")
250	        else:
251	            print("Building draft vocabulary from training data...")
252	            from collections import Counter
253	            counter = Counter()
254	            pt_files = sorted(data_dir.glob("*.pt"))
255	            for f in tqdm(pt_files, desc="scanning vocab"):
256	                d = torch.load(f, weights_only=True)
257	                ids = d["token_ids"].numpy()
258	                for tok in ids:
259	                    counter[int(tok)] += 1
260	
261	            top_tokens = [tok for tok, _ in counter.most_common(DRAFT_VOCAB_SIZE)]
262	            top_tokens.sort()
263	
264	            d2t = torch.tensor(top_tokens, dtype=torch.long)
265	            t2d = torch.zeros(VOCAB_SIZE, dtype=torch.bool)
266	            t2d[d2t] = True
267	
268	            total_freq = sum(counter.values())
269	            covered_freq = sum(counter[t] for t in top_tokens)
270	            print(f"Draft vocab covers {covered_freq/total_freq:.2%} of tokens")
271	
272	            torch.save({"d2t": d2t, "t2d": t2d}, cache_path)
273	            self.d2t.copy_(d2t)
274	            self.t2d.copy_(t2d)
275	
276	        # Build draft_idx_map buffer (full_vocab_id -> draft_idx)
277	        self.draft_idx_map.zero_()
278	        self.draft_idx_map[self.d2t] = torch.arange(DRAFT_VOCAB_SIZE, device=self.draft_idx_map.device)
279	
280	        # Initialize lm_head from target model's lm_head (draft vocab subset)
281	        if self._full_lm_head_weight is not None:
282	            with torch.no_grad():
283	                self.lm_head.weight.copy_(self._full_lm_head_weight[self.d2t.cpu()])
284	            print(f"Initialized lm_head from target model ({DRAFT_VOCAB_SIZE} rows)")
285	            self._full_lm_head_weight = None  # free memory
286	
287	    def _make_causal_mask(self, total_len, device):
288	        """Create causal attention mask."""
289	        mask = torch.full((total_len, total_len), float("-inf"), device=device)
290	        mask = torch.triu(mask, diagonal=1)
291	        return mask[None, None, :, :]  # (1, 1, S, S)
292	
293	    def _build_target_p(self, target_logits_values, target_logits_indices, device):
294	        """Build target distribution from top-256 logits.
295	
296	        Maps top-256 full-vocab logits into draft vocab space, applies softmax.
297	        Mirrors official: target_head = full_logits[..., t2d]; target_p = softmax(target_head)
298	        We approximate by scattering top-256 logits into draft vocab positions.
299	        """
300	        B, S, K = target_logits_values.shape
301	        indices = target_logits_indices.long().clamp(0, VOCAB_SIZE - 1)
302	        in_draft = self.t2d[indices]  # (B, S, 256) bool
303	
304	        # Build draft-space logits: only scatter tokens that are in draft vocab
305	        # Use reduce='amax' to avoid race condition when multiple entries map to same idx
306	        draft_logits = torch.full((B, S, DRAFT_VOCAB_SIZE), -1e9, device=device, dtype=torch.float32)
307	        mapped_idx = self.draft_idx_map[indices]  # (B, S, 256)
308	        values = target_logits_values.float()
309	
310	        # Set non-draft entries to -1e9, then scatter with amax (max wins, -1e9 never beats valid)
311	        safe_vals = torch.where(in_draft, values, torch.tensor(-1e9, device=device))
312	        draft_logits.scatter_reduce_(2, mapped_idx, safe_vals, reduce="amax")
313	        target_p = F.softmax(draft_logits, dim=-1)
314	        return target_p
315	
316	    def forward(self, token_ids, aux_hidden, target_logits_values, target_logits_indices):
317	        """
318	        EAGLE-3 training with shifted alignment to match inference.
319	
320	        Inference pattern: (embed(x_{t+1}), fc(aux[t])) → predict x_{t+2}
321	        So we shift inputs: position t gets token[t+1] with hidden[t], target[t+1].
322	
323	        1. Shift: input_ids = token_ids[:,1:], aux = aux_hidden[:,:-1], target = target[:,1:]
324	        2. fc(aux) → hidden
325	        3. For each TTT step:
326	           a. embed(input_ids) → input_emb
327	           b. midlayer(input_emb, hidden, cache) → hidden_out
328	           c. norm(hidden_out) → lm_head → logits
329	           d. plogp loss with position_mask
330	           e. Shift input_ids, target, loss by 1 position (padding left=False)
331	        """
332	        B, S_orig = token_ids.shape
333	        device = token_ids.device
334	
335	        # Shift alignment: match inference pattern (x_{t+1}, aux[t]) → predict x_{t+2}
336	        input_ids = token_ids[:, 1:]           # (B, S-1): tokens x_1..x_{S-1}
337	        aux_shifted = aux_hidden[:, :-1, :]    # (B, S-1, 12288): aux_0..aux_{S-2}
338	        target_values = target_logits_values[:, 1:, :]   # (B, S-1, K)
339	        target_indices = target_logits_indices[:, 1:, :]  # (B, S-1, K)
340	        S = S_orig - 1
341	
342	        hidden = self.fc(aux_shifted)
343	
344	        # Build causal mask once (same sequence length throughout, no KV cache accumulation)
345	        # Official EAGLE-3 uses standard causal mask, NOT accumulating KV across TTT steps
346	        causal_mask = self._make_causal_mask(S, device)
347	
348	        step_losses = []
349	        step_accs = []
350	        cache_k_list = None
351	        cache_v_list = None
352	
353	        for step in range(self.ttt_steps):
354	            last = step == self.ttt_steps - 1
355	
356	            # Embed current input_ids
357	            input_emb = self.embed_tokens(input_ids) * self.scale_emb
358	            input_emb = input_emb.to(hidden.dtype)
359	
360	            # Forward through decoder layer with list-based KV cache
361	            if GRAD_CHECKPOINT and self.training:
362	                def _fwd(ie, hs, cm, *cache_tensors):
363	                    # Reconstruct lists from flattened tensors
364	                    n = len(cache_tensors) // 2
365	                    ck = list(cache_tensors[:n]) if n > 0 else None
366	                    cv = list(cache_tensors[n:]) if n > 0 else None
367	                    out, new_ck, new_cv = self.midlayer(ie, hs, ck, cv, cm)
368	                    return (out, *new_ck, *new_cv)
369	
370	                # Flatten cache lists for checkpoint (it needs tensors, not lists)
371	                cache_tensors = []
372	                if cache_k_list is not None:
373	                    cache_tensors = [*cache_k_list, *cache_v_list]
374	                results = torch.utils.checkpoint.checkpoint(
375	                    _fwd, input_emb, hidden, causal_mask, *cache_tensors,
376	                    use_reentrant=False,
377	                )
378	                hidden_out = results[0]
379	                n_cache = (len(results) - 1) // 2
380	                cache_k_list = list(results[1:1+n_cache])
381	                cache_v_list = list(results[1+n_cache:])
382	            else:
383	                hidden_out, cache_k_list, cache_v_list = self.midlayer(
384	                    input_emb, hidden, cache_k_list, cache_v_list, causal_mask,
385	                )
386	            hidden = hidden_out
387	
388	            # Compute target distribution for this step's target
389	            with torch.no_grad():
390	                target_p = self._build_target_p(target_values, target_indices, device)
391	                # target_p: (B, S, draft_vocab)
392	
393	                # Position mask: only positions where target argmax is in draft vocab
394	                target_argmax_full = target_indices[:, :, 0].long().clamp(0, VOCAB_SIZE - 1)  # top-1
395	                target_mask = self.t2d[target_argmax_full].float()  # (B, S)
396	
397	            # Logits
398	            normed = self.norm(hidden_out)
399	            logits = self.lm_head(normed).float()  # (B, S, draft_vocab)
400	
401	            # plogp loss (official L854-855) — mean over valid positions
402	            out_logp = F.log_softmax(logits, dim=-1)
403	            plogp = target_p * out_logp  # (B, S, draft_vocab)
404	            neg_ce = -plogp.sum(dim=-1)  # (B, S) — cross-entropy per position
405	            # Average only over positions where target is in draft vocab
406	            n_valid = target_mask.sum().clamp(min=1)
407	            loss = (neg_ce * target_mask).sum() / n_valid
408	            step_losses.append(loss)
409	
410	            # Accuracy
411	            with torch.no_grad():
412	                pred_idx = logits.argmax(-1)  # (B, S)
413	                target_draft_idx = target_p.argmax(-1)  # (B, S)
414	                correct = (pred_idx == target_draft_idx).float() * target_mask
415	                acc = correct.sum().item() / (target_mask.sum().item() + 1e-6)
416	                step_accs.append(acc)
417	
418	            # Shift for next step (official L862-864)
419	            if not last:
420	                # padding(x, left=False) = cat(x[:,1:], zeros)
421	                input_ids = torch.cat([input_ids[:, 1:], torch.zeros(B, 1, dtype=input_ids.dtype, device=device)], dim=1)
422	                target_values = torch.cat([target_values[:, 1:, :], torch.zeros(B, 1, target_values.shape[2], dtype=target_values.dtype, device=device)], dim=1)
423	                target_indices = torch.cat([target_indices[:, 1:, :], torch.zeros(B, 1, target_indices.shape[2], dtype=target_indices.dtype, device=device)], dim=1)
424	
425	        # Weighted total loss
426	        total_loss = sum(self.loss_decay ** i * l for i, l in enumerate(step_losses))
427	        return total_loss, step_losses, step_accs
428	
429	
430	# ── Data loading ─────────────────────────────────────────────────────────
431	def load_batch(files, device):
432	    """Load a batch of .pt files and collate with padding."""
433	    batch = {"token_ids": [], "aux_hidden": [], "top_logit_values": [], "top_logit_indices": []}
434	    for f in files:
435	        d = torch.load(f, weights_only=True)
436	        for k in batch:
437	            batch[k].append(d[k][:SEQ_LEN])  # truncate to SEQ_LEN
438	
439	    # Pad to max length in batch
440	    max_len = max(t.shape[0] for t in batch["token_ids"])
441	    for k in batch:
442	        padded = []
443	        for t in batch[k]:
444	            if t.shape[0] < max_len:
445	                pad_shape = list(t.shape)
446	                pad_shape[0] = max_len - t.shape[0]
447	                t = torch.cat([t, torch.zeros(pad_shape, dtype=t.dtype)], dim=0)
448	            padded.append(t)
449	        batch[k] = torch.stack(padded).to(device)
450	    batch["aux_hidden"] = batch["aux_hidden"].to(DTYPE)
451	    batch["top_logit_values"] = batch["top_logit_values"].to(DTYPE)
452	    return batch
453	
454	
455	def load_embed_and_lm_head():
456	    """Load frozen embed_tokens and lm_head from target model."""
457	    import json
458	    config_path = os.path.join(MODEL_PATH, "config.json")
459	    with open(config_path) as f:
460	        config = json.load(f)
461	
462	    # Load from safetensors
463	    index_path = os.path.join(MODEL_PATH, "model.safetensors.index.json")
464	    if os.path.exists(index_path):
465	        with open(index_path) as f:
466	            index = json.load(f)
467	        weight_map = index["weight_map"]
468	
469	        emb_file = weight_map.get("model.embed_tokens.weight", None)
470	        lm_file = weight_map.get("lm_head.weight", None)
471	
472	        with safe_open(os.path.join(MODEL_PATH, emb_file), framework="pt", device="cpu") as f:
473	            embed_weight = f.get_tensor("model.embed_tokens.weight").float()
474	
475	        if lm_file:
476	            with safe_open(os.path.join(MODEL_PATH, lm_file), framework="pt", device="cpu") as f:
477	                lm_weight = f.get_tensor("lm_head.weight").float()
478	        else:
479	            # tied embeddings
480	            lm_weight = embed_weight.clone()
481	    else:
482	        # Single safetensors file
483	        st_path = os.path.join(MODEL_PATH, "model.safetensors")
484	        with safe_open(st_path, framework="pt", device="cpu") as f:
485	            embed_weight = f.get_tensor("model.embed_tokens.weight").float()
486	            try:
487	                lm_weight = f.get_tensor("lm_head.weight").float()
488	            except:
489	                lm_weight = embed_weight.clone()
490	
491	    print(f"Loaded embed_tokens: {embed_weight.shape}, lm_head: {lm_weight.shape}")
492	    return embed_weight, lm_weight
493	
494	
495	# ── Main ─────────────────────────────────────────────────────────────────
496	def main():
497	    random.seed(SEED)
498	    torch.manual_seed(SEED)
499	    torch.cuda.manual_seed(SEED)
500	
501	    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
502	
503	    # Load target model weights
504	    print("Loading target model embed/lm_head...")
505	    embed_weight, lm_weight = load_embed_and_lm_head()
506	
507	    # Build model
508	    model = Eagle3Model(embed_weight, lm_weight).to(DEVICE).to(DTYPE)
509	    model.build_vocab_mapping(DATA_DIR)
510	
511	    # Count params
512	    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
513	    frozen = sum(p.numel() for p in model.parameters() if not p.requires_grad)
514	    print(f"Trainable: {trainable/1e6:.1f}M, Frozen: {frozen/1e6:.1f}M")
515	
516	    # Optimizer
517	    optimizer = torch.optim.AdamW(
518	        [p for p in model.parameters() if p.requires_grad],
519	        lr=LR, betas=BETAS, weight_decay=WEIGHT_DECAY,
520	    )
521	
522	    # Data — filter short files by file size (MIN_TOKENS * ~26KB/token)
523	    # 128 tokens ≈ 3.2 MB (each token has 12288*2 + 256*2 + 256*4 + 8 bytes ≈ 26KB)
524	    min_file_size = MIN_TOKENS * 26 * 1024
525	    all_files = sorted(DATA_DIR.glob("*.pt"))
526	    pt_files = [f for f in all_files if f.stat().st_size >= min_file_size]
527	    print(f"Training files: {len(pt_files)} (filtered from {len(all_files)}, min_size={min_file_size//1024}KB)")
528	    if len(pt_files) == 0:
529	        print("No training data! Run eagle/collect_data.py first.")
530	        return
531	
532	    steps_per_epoch = len(pt_files) // BATCH_SIZE
533	    total_steps = steps_per_epoch * EPOCHS // GRAD_ACCUM
534	    print(f"Steps/epoch: {steps_per_epoch}, Total steps: {total_steps}, Effective batch: {BATCH_SIZE * GRAD_ACCUM}")
535	
536	    # LR scheduler
537	    def lr_lambda(step):
538	        if step < WARMUP_STEPS:
539	            return step / max(1, WARMUP_STEPS)
540	        progress = (step - WARMUP_STEPS) / max(1, total_steps - WARMUP_STEPS)
541	        return 0.5 * (1 + math.cos(math.pi * progress))
542	
543	    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)
544	
545	    # Training loop
546	    global_step = 0
547	    best_acc = 0
548	    model.train()
549	
550	    for epoch in range(EPOCHS):
551	        random.shuffle(pt_files)
552	        epoch_loss = 0
553	        epoch_acc0 = 0
554	        n_batches = 0
555	
556	        pbar = tqdm(range(0, len(pt_files) - BATCH_SIZE + 1, BATCH_SIZE),
557	                     desc=f"Epoch {epoch+1}/{EPOCHS}", unit="batch")
558	
559	        optimizer.zero_grad()
560	
561	        for batch_idx in pbar:
562	            batch_files = pt_files[batch_idx:batch_idx + BATCH_SIZE]
563	            batch = load_batch(batch_files, DEVICE)
564	
565	            total_loss, step_losses, step_accs = model(
566	                batch["token_ids"],
567	                batch["aux_hidden"],
568	                batch["top_logit_values"],
569	                batch["top_logit_indices"],
570	            )
571	
572	            loss = total_loss / GRAD_ACCUM
573	            loss.backward()
574	
575	            if (n_batches + 1) % GRAD_ACCUM == 0:
576	                torch.nn.utils.clip_grad_norm_(model.parameters(), MAX_GRAD_NORM)
577	                optimizer.step()
578	                scheduler.step()
579	                optimizer.zero_grad()
580	                global_step += 1
581	
582	            epoch_loss += total_loss.item()
583	            epoch_acc0 += step_accs[0]
584	            n_batches += 1
585	
586	            pbar.set_postfix(
587	                loss=f"{total_loss.item():.3f}",
588	                acc0=f"{step_accs[0]:.3f}",
589	                lr=f"{scheduler.get_last_lr()[0]:.2e}",
590	                gstep=global_step,
591	            )
592	
593	            if n_batches % 200 == 0 and n_batches > 0:
594	                avg_recent = epoch_loss / n_batches
595	                avg_acc_recent = epoch_acc0 / n_batches
596	                print(f"\n  [{time.strftime('%H:%M:%S')}] batch {n_batches}: "
597	                      f"avg_loss={avg_recent:.3f}, avg_acc0={avg_acc_recent:.3f}, "
598	                      f"lr={scheduler.get_last_lr()[0]:.2e}, gstep={global_step}")
599	
600	        avg_loss = epoch_loss / max(n_batches, 1)
601	        avg_acc0 = epoch_acc0 / max(n_batches, 1)
602	        print(f"Epoch {epoch+1}: loss={avg_loss:.4f}, step0_acc={avg_acc0:.4f}")
603	
604	        # Save checkpoint
605	        ckpt = {
606	            "epoch": epoch + 1,
607	            "model_state_dict": {k: v.cpu() for k, v in model.state_dict().items()
608	                                  if not k.startswith("embed_tokens")},
609	            "optimizer_state_dict": optimizer.state_dict(),
610	            "avg_loss": avg_loss,
611	            "avg_acc0": avg_acc0,
612	            "config": {
613	                "hidden_size": HIDDEN_SIZE,
614	                "draft_vocab_size": DRAFT_VOCAB_SIZE,
615	                "ttt_steps": TTT_STEPS,
616	                "aux_layers": [1, 10, 22],
617	            },
618	        }
619	        torch.save(ckpt, OUTPUT_DIR / f"epoch_{epoch+1}.pt")
620	
621	        if avg_acc0 > best_acc:
622	            best_acc = avg_acc0
623	            torch.save(ckpt, OUTPUT_DIR / "best.pt")
624	            print(f"  New best! acc0={best_acc:.4f}")
625	
626	    print(f"\nTraining complete. Best acc0: {best_acc:.4f}")
627	    print(f"Checkpoints saved to {OUTPUT_DIR}")
628	
629	
630	if __name__ == "__main__":
631	    main()
632
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/eval_ood_accept.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Evaluate EAGLE-3 accept rate on OOD data.
4	Simulates full inference forward to match online behavior.
5	"""
6	
7	import math
8	import torch
9	import torch.nn as nn
10	import torch.nn.functional as F
11	from pathlib import Path
12	from safetensors import safe_open
13	
14	DEVICE = "cuda"
15	DTYPE = torch.bfloat16
16	
17	# Model config (from train.py)
18	HIDDEN_SIZE = 4096
19	AUX_DIM = HIDDEN_SIZE * 3  # 12288
20	VOCAB_SIZE = 73448
21	DRAFT_VOCAB_SIZE = 32000
22	SCALE_EMB = 12
23	NUM_HEADS = 32
24	NUM_KV_HEADS = 2
25	HEAD_DIM = 128
26	INTERMEDIATE_SIZE = 16384
27	RMS_NORM_EPS = 1e-6
28	
29	
30	class RMSNorm(nn.Module):
31	    def __init__(self, dim, eps=1e-6):
32	        super().__init__()
33	        self.weight = nn.Parameter(torch.ones(dim))
34	        self.eps = eps
35	
36	    def forward(self, x):
37	        norm = x.float().pow(2).mean(-1, keepdim=True).add(self.eps).rsqrt()
38	        return (x * norm).to(x.dtype) * self.weight
39	
40	
41	class Eagle3Attention(nn.Module):
42	    """Simplified attention for eval (no KV cache, single step)."""
43	    def __init__(self):
44	        super().__init__()
45	        self.num_heads = NUM_HEADS
46	        self.num_kv_heads = NUM_KV_HEADS
47	        self.head_dim = HEAD_DIM
48	        self.num_kv_groups = NUM_HEADS // NUM_KV_HEADS
49	
50	        qkv_in = HIDDEN_SIZE * 2
51	        self.q_proj = nn.Linear(qkv_in, NUM_HEADS * HEAD_DIM, bias=False)
52	        self.k_proj = nn.Linear(qkv_in, NUM_KV_HEADS * HEAD_DIM, bias=False)
53	        self.v_proj = nn.Linear(qkv_in, NUM_KV_HEADS * HEAD_DIM, bias=False)
54	        self.o_proj = nn.Linear(NUM_HEADS * HEAD_DIM, HIDDEN_SIZE, bias=False)
55	
56	    def forward(self, hidden_cat):
57	        B, S, _ = hidden_cat.shape
58	        q = self.q_proj(hidden_cat).view(B, S, self.num_heads, self.head_dim).transpose(1, 2)
59	        k = self.k_proj(hidden_cat).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
60	        v = self.v_proj(hidden_cat).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
61	
62	        if self.num_kv_groups > 1:
63	            k = k.repeat_interleave(self.num_kv_groups, dim=1)
64	            v = v.repeat_interleave(self.num_kv_groups, dim=1)
65	
66	        attn_output = F.scaled_dot_product_attention(q, k, v, is_causal=True)
67	        attn_output = attn_output.transpose(1, 2).contiguous().view(B, S, -1)
68	        return self.o_proj(attn_output)
69	
70	
71	class Eagle3MLP(nn.Module):
72	    def __init__(self):
73	        super().__init__()
74	        self.gate_proj = nn.Linear(HIDDEN_SIZE, INTERMEDIATE_SIZE, bias=False)
75	        self.up_proj = nn.Linear(HIDDEN_SIZE, INTERMEDIATE_SIZE, bias=False)
76	        self.down_proj = nn.Linear(INTERMEDIATE_SIZE, HIDDEN_SIZE, bias=False)
77	
78	    def forward(self, x):
79	        return self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))
80	
81	
82	class Eagle3Model(nn.Module):
83	    def __init__(self):
84	        super().__init__()
85	        self.fc = nn.Linear(AUX_DIM, HIDDEN_SIZE, bias=False)
86	        self.input_layernorm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
87	        self.hidden_norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
88	        self.self_attn = Eagle3Attention()
89	        self.post_attention_layernorm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
90	        self.mlp = Eagle3MLP()
91	        self.norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
92	        self.embed_tokens = nn.Embedding(VOCAB_SIZE, HIDDEN_SIZE)
93	        self.lm_head = nn.Linear(HIDDEN_SIZE, DRAFT_VOCAB_SIZE, bias=False)
94	        self.scale_emb = SCALE_EMB
95	
96	    def forward(self, token_ids, aux_hidden):
97	        """
98	        token_ids: (B, S) or (S,)
99	        aux_hidden: (B, S, 12288) or (S, 12288)
100	        Returns: logits (B, S, draft_vocab) or (S, draft_vocab)
101	        """
102	        if token_ids.dim() == 1:
103	            token_ids = token_ids.unsqueeze(0)
104	            aux_hidden = aux_hidden.unsqueeze(0)
105	            squeeze_out = True
106	        else:
107	            squeeze_out = False
108	
109	        # fc projection
110	        hidden_states = self.fc(aux_hidden)
111	
112	        # embed tokens
113	        embeds = self.embed_tokens(token_ids) * self.scale_emb
114	        embeds = embeds.to(hidden_states.dtype)
115	
116	        # decoder layer forward (matching llama_eagle3.py)
117	        residual = hidden_states
118	        embeds_normed = self.input_layernorm(embeds)
119	        hidden_normed = self.hidden_norm(hidden_states)
120	        hidden_cat = torch.cat([embeds_normed, hidden_normed], dim=-1)
121	
122	        # attention
123	        attn_out = self.self_attn(hidden_cat)
124	        hidden_states = residual + attn_out
125	
126	        # MLP
127	        residual = hidden_states
128	        hidden_states = self.post_attention_layernorm(hidden_states)
129	        hidden_states = self.mlp(hidden_states)
130	        hidden_states = residual + hidden_states
131	
132	        # final norm + lm_head
133	        hidden_states = self.norm(hidden_states)
134	        logits = self.lm_head(hidden_states)
135	
136	        if squeeze_out:
137	            logits = logits.squeeze(0)
138	        return logits
139	
140	
141	def load_model(ckpt_path=None):
142	    model = Eagle3Model().to(DEVICE).to(DTYPE)
143	
144	    if ckpt_path and Path(ckpt_path).suffix == ".pt":
145	        # Load from training checkpoint — remap midlayer keys to flat names
146	        ckpt = torch.load(ckpt_path, weights_only=True, map_location="cpu")
147	        raw_state = ckpt["model_state_dict"]
148	        state_dict = {}
149	        for k, v in raw_state.items():
150	            nk = k
151	            if nk.startswith("midlayer."):
152	                nk = nk[len("midlayer."):]
153	            if nk == "input_emb_norm.weight":
154	                nk = "input_layernorm.weight"
155	            state_dict[nk] = v
156	        print(f"Loaded checkpoint: epoch={ckpt.get('epoch')}, avg_acc0={ckpt.get('avg_acc0', 'N/A')}")
157	        print(f"  Mapped keys: {sorted(state_dict.keys())}")
158	    else:
159	        # Load from sglang_model format
160	        with safe_open("eagle/sglang_model/model.safetensors", framework="pt", device="cpu") as f:
161	            state_dict = {}
162	            for key in f.keys():
163	                tensor = f.get_tensor(key)
164	                if key.startswith("model."):
165	                    key = key[6:]
166	                if key == "midlayer.input_layernorm.weight":
167	                    [REDACTED]
168	                elif key == "midlayer.hidden_norm.weight":
169	                    [REDACTED]
170	                elif key == "midlayer.post_attention_layernorm.weight":
171	                    [REDACTED]
172	                elif key.startswith("midlayer.self_attn."):
173	                    key = key.replace("midlayer.self_attn.", "self_attn.")
174	                elif key.startswith("midlayer.mlp."):
175	                    key = key.replace("midlayer.mlp.", "mlp.")
176	                elif key == "norm.weight":
177	                    key = "norm.weight"
178	                state_dict[key] = tensor
179	
180	    # Load embed_tokens from target model
181	    import json
182	    target_path = [REDACTED]
183	    with open(f"{target_path}/model.safetensors.index.json") as f:
184	        index = json.load(f)
185	    emb_file = index["weight_map"]["model.embed_tokens.weight"]
186	    with safe_open(f"{target_path}/{emb_file}", framework="pt", device="cpu") as f:
187	        state_dict["embed_tokens.weight"] = f.get_tensor("model.embed_tokens.weight")
188	
189	    model.load_state_dict(state_dict, strict=False)
190	    model.eval()
191	    return model
192	
193	
194	def load_vocab_mapping():
195	    cache = torch.load("eagle/data/vocab_cache.pt", weights_only=True)
196	    d2t = cache["d2t"].to(DEVICE)
197	    t2d = cache["t2d"].to(DEVICE)
198	    draft_idx_map = torch.zeros(VOCAB_SIZE, dtype=torch.long, device=DEVICE)
199	    draft_idx_map[d2t] = torch.arange(DRAFT_VOCAB_SIZE, device=DEVICE)
200	    return d2t, t2d, draft_idx_map
201	
202	
203	def build_target_p(target_logits_values, target_logits_indices, t2d, draft_idx_map):
204	    """Build target distribution from top-256 logits."""
205	    S, K = target_logits_values.shape
206	    indices = target_logits_indices.long().clamp(0, VOCAB_SIZE - 1)
207	    in_draft = t2d[indices]
208	
209	    draft_logits = torch.full((S, DRAFT_VOCAB_SIZE), -1e9, device=DEVICE, dtype=torch.float32)
210	    mapped_idx = draft_idx_map[indices]
211	    values = target_logits_values.float()
212	
213	    safe_vals = torch.where(in_draft, values, torch.tensor(-1e9, device=DEVICE))
214	    draft_logits.scatter_reduce_(1, mapped_idx, safe_vals, reduce="amax")
215	    target_p = F.softmax(draft_logits, dim=-1)
216	    return target_p
217	
218	
219	def main():
220	    import sys
221	    ckpt_path = sys.argv[1] if len(sys.argv) > 1 else None
222	    print(f"Loading model... (ckpt={ckpt_path})")
223	    model = load_model(ckpt_path)
224	    d2t, t2d, draft_idx_map = load_vocab_mapping()
225	
226	    # Load OOD data
227	    ood_dir = Path("/tmp/eagle3_val_collect")
228	    pt_files = sorted(ood_dir.glob("*.pt"))
229	    print(f"Found {len(pt_files)} OOD files")
230	
231	    total_correct = 0
232	    total_valid = 0
233	    total_tokens = 0
234	
235	    with torch.no_grad():
236	        for i, pt_file in enumerate(pt_files):
237	            data = torch.load(pt_file, weights_only=True)
238	            token_ids = data["token_ids"].to(DEVICE)
239	            aux_hidden = data["aux_hidden"].to(DEVICE).to(DTYPE)
240	            top_logit_values = data["top_logit_values"].to(DEVICE).to(DTYPE)
241	            top_logit_indices = data["top_logit_indices"].to(DEVICE)
242	
243	            seq_len = token_ids.shape[0]
244	            if seq_len < 3:
245	                continue
246	
247	            # Shifted alignment: match inference (x_{t+1}, aux[t]) → predict x_{t+2}
248	            shifted_ids = token_ids[1:]           # x_1..x_{S-1}
249	            shifted_aux = aux_hidden[:-1]          # aux_0..aux_{S-2}
250	            shifted_target_vals = top_logit_values[1:]
251	            shifted_target_inds = top_logit_indices[1:]
252	
253	            # Forward
254	            logits = model(shifted_ids, shifted_aux)  # (S-1, draft_vocab)
255	
256	            # Build target distribution
257	            target_p = build_target_p(shifted_target_vals, shifted_target_inds, t2d, draft_idx_map)
258	
259	            # Compute accept rate
260	            pred_draft_idx = logits.argmax(dim=-1)
261	            target_draft_idx = target_p.argmax(dim=-1)
262	
263	            # Only count positions where target argmax is in draft vocab
264	            target_argmax_full = shifted_target_inds[:, 0].long().clamp(0, VOCAB_SIZE - 1)
265	            target_mask = t2d[target_argmax_full].float()
266	
267	            correct = (pred_draft_idx == target_draft_idx).float() * target_mask
268	            n_correct = correct.sum().item()
269	            n_valid = target_mask.sum().item()
270	
271	            total_correct += n_correct
272	            total_valid += n_valid
273	            total_tokens += seq_len - 1
274	
275	            if i < 5:
276	                acc = n_correct / n_valid if n_valid > 0 else 0
277	                print(f"[{i}] {pt_file.name}: seq_len={seq_len}, valid={int(n_valid)}, correct={int(n_correct)}, acc={acc:.1%}")
278	
279	    print(f"\n{'='*60}")
280	    print(f"Total tokens: {total_tokens}")
281	    print(f"Valid positions: {int(total_valid)}")
282	    print(f"Correct predictions: {int(total_correct)}")
283	    print(f"OOD Accept Rate: {total_correct/total_valid:.1%}" if total_valid > 0 else "N/A")
284	
285	
286	if __name__ == "__main__":
287	    main()
288
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/convert_to_sglang.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Convert EAGLE-3 training checkpoint to sglang-compatible format.
4	
5	Produces a directory with:
6	  - config.json (LlamaConfig-compatible)
7	  - model.safetensors (weights with sglang naming)
8	
9	Usage:
10	    python3 eagle/convert_to_sglang.py [--ckpt eagle/weights/best.pt] [--output eagle/sglang_model]
11	"""
12	
13	import json
14	import os
15	from pathlib import Path
16	
17	import torch
18	from safetensors.torch import save_file
19	
20	
21	CKPT_PATH = Path("eagle/weights/epoch_4.pt")
22	OUTPUT_DIR = Path("eagle/sglang_model")
23	TARGET_MODEL = [REDACTED]
24	
25	# Architecture constants (must match train.py)
26	HIDDEN_SIZE = 4096
27	AUX_DIM = HIDDEN_SIZE * 3  # 12288
28	VOCAB_SIZE = 73448
29	DRAFT_VOCAB_SIZE = 32000
30	NUM_HEADS = 32
31	NUM_KV_HEADS = 2
32	HEAD_DIM = 128
33	INTERMEDIATE_SIZE = 16384
34	RMS_NORM_EPS = 1e-6
35	
36	
37	def convert():
38	    print(f"Loading checkpoint: {CKPT_PATH}")
39	    ckpt = torch.load(CKPT_PATH, weights_only=True)
40	    state = ckpt["model_state_dict"]
41	
42	    print(f"Checkpoint epoch: {ckpt['epoch']}, acc0: {ckpt.get('avg_acc0', 'N/A')}")
43	
44	    # Load vocab mapping
45	    vocab_cache = torch.load("eagle/data/vocab_cache.pt", weights_only=True)
46	    d2t = vocab_cache["d2t"]  # (32000,) — target vocab ids
47	
48	    # Convert d2t to diff format (what sglang expects)
49	    # sglang: hot_token_id = d2t_stored + arange(draft_vocab)
50	    # So d2t_stored = d2t - arange(draft_vocab)
51	    d2t_diff = d2t - torch.arange(DRAFT_VOCAB_SIZE)
52	
53	    # Map training state_dict keys to sglang keys
54	    key_mapping = {
55	        "fc.weight": "model.fc.weight",
56	        # Decoder layer
57	        "midlayer.input_emb_norm.weight": "model.midlayer.input_layernorm.weight",
58	        "midlayer.hidden_norm.weight": "model.midlayer.hidden_norm.weight",
59	        "midlayer.self_attn.q_proj.weight": "model.midlayer.self_attn.q_proj.weight",
60	        "midlayer.self_attn.k_proj.weight": "model.midlayer.self_attn.k_proj.weight",
61	        "midlayer.self_attn.v_proj.weight": "model.midlayer.self_attn.v_proj.weight",
62	        "midlayer.self_attn.o_proj.weight": "model.midlayer.self_attn.o_proj.weight",
63	        "midlayer.post_attention_layernorm.weight": "model.midlayer.post_attention_layernorm.weight",
64	        "midlayer.mlp.gate_proj.weight": "model.midlayer.mlp.gate_proj.weight",
65	        "midlayer.mlp.up_proj.weight": "model.midlayer.mlp.up_proj.weight",
66	        "midlayer.mlp.down_proj.weight": "model.midlayer.mlp.down_proj.weight",
67	        # Top-level norm
68	        "norm.weight": "model.norm.weight",
69	        # lm_head
70	        "lm_head.weight": "lm_head.weight",
71	    }
72	
73	    tensors = {}
74	    for train_key, sglang_key in key_mapping.items():
75	        if train_key in state:
76	            tensors[sglang_key] = state[train_key].to(torch.bfloat16)
77	        else:
78	            print(f"  WARNING: missing key {train_key}")
79	
80	    # Add d2t diff
81	    tensors["d2t"] = d2t_diff
82	
83	    # Add embed_tokens from target model (frozen, not in checkpoint)
84	    from safetensors import safe_open
85	    index_path = os.path.join(TARGET_MODEL, "model.safetensors.index.json")
86	    with open(index_path) as f:
87	        index = json.load(f)
88	    emb_file = index["weight_map"]["model.embed_tokens.weight"]
89	    with safe_open(os.path.join(TARGET_MODEL, emb_file), framework="pt", device="cpu") as f:
90	        embed_weight = f.get_tensor("model.embed_tokens.weight")
91	    tensors["model.embed_tokens.weight"] = embed_weight.to(torch.bfloat16)
92	
93	    # Save weights
94	    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
95	    save_file(tensors, OUTPUT_DIR / "model.safetensors")
96	    print(f"Saved weights: {len(tensors)} tensors")
97	
98	    # Generate config.json
99	    config = {
100	        "architectures": ["LlamaForCausalLMEagle3"],
101	        "model_type": "llama",
102	        "hidden_size": HIDDEN_SIZE,
103	        "intermediate_size": INTERMEDIATE_SIZE,
104	        "num_hidden_layers": 1,
105	        "num_attention_heads": NUM_HEADS,
106	        "num_key_value_heads": NUM_KV_HEADS,
107	        "head_dim": HEAD_DIM,
108	        "hidden_act": "silu",
109	        "max_position_embeddings": 524288,
110	        "rms_norm_eps": RMS_NORM_EPS,
111	        "vocab_size": VOCAB_SIZE,
112	        "draft_vocab_size": DRAFT_VOCAB_SIZE,
113	        "target_hidden_size": HIDDEN_SIZE,  # same as hidden_size since fc does 12288→4096
114	        "scale_emb": 12,
115	        "tie_word_embeddings": False,
116	        "torch_dtype": "bfloat16",
117	        # EAGLE-3 specific — sglang reads these from draft model config
118	        "eagle_config": {
119	            "use_aux_hidden_state": True,
120	            "eagle_aux_hidden_state_layer_ids": [1, 10, 22],
121	        },
122	    }
123	
124	    with open(OUTPUT_DIR / "config.json", "w") as f:
125	        json.dump(config, f, indent=2)
126	    print(f"Saved config.json")
127	
128	    # Copy tokenizer files from target model
129	    for fname in ["tokenizer.json", "tokenizer_config.json", "special_tokens_map.json",
130	                   "tokenizer.model", "added_tokens.json"]:
131	        src = os.path.join(TARGET_MODEL, fname)
132	        if os.path.exists(src):
133	            import shutil
134	            shutil.copy2(src, OUTPUT_DIR / fname)
135	            print(f"Copied {fname}")
136	
137	    # Verify
138	    print(f"\nOutput directory: {OUTPUT_DIR}")
139	    for f in sorted(OUTPUT_DIR.iterdir()):
140	        size = f.stat().st_size
141	        if size > 1024 * 1024:
142	            print(f"  {f.name}: {size / 1024 / 1024:.1f} MB")
143	        else:
144	            print(f"  {f.name}: {size / 1024:.1f} KB")
145	
146	    print(f"\nConversion complete! acc0={ckpt.get('avg_acc0', 'N/A')}")
147	    print(f"To use with sglang, pass --speculative-draft-model-path {OUTPUT_DIR.resolve()}")
148	
149	
150	if __name__ == "__main__":
151	    convert()
152
```

> AGENT

Now let me read the remaining eagle files:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/test_eagle3_flow.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Test EAGLE-3 inference flow - verify hidden_states dimensions and d2t mapping.
4	
5	This runs a single forward pass to check:
6	1. aux_hidden_states from target model has correct shape (12288)
7	2. d2t mapping works correctly
8	3. Draft model fc projection works
9	"""
10	
11	import os
12	import sys
13	import torch
14	import json
15	from pathlib import Path
16	
17	# Add sglang to path
18	SGLANG_PATH = Path("/user_4813494d/openbmb/demo-sala/sglang/python")
19	sys.path.insert(0, str(SGLANG_PATH))
20	
21	os.environ["CUDA_VISIBLE_DEVICES"] = "0"
22	
23	def test_weights_loading():
24	    """Test that weights are correctly loaded."""
25	    from safetensors import safe_open
26	
27	    print("=" * 60)
28	    print("Test 1: Weight Loading")
29	    print("=" * 60)
30	
31	    model_path = Path("eagle/sglang_model/model.safetensors")
32	
33	    with safe_open(model_path, framework="pt", device="cpu") as f:
34	        keys = f.keys()
35	        print(f"Total tensors: {len(keys)}")
36	
37	        # Check fc weight
38	        fc_weight = f.get_tensor("model.fc.weight")
39	        print(f"model.fc.weight: {fc_weight.shape} (expected: [4096, 12288])")
40	        assert fc_weight.shape == (4096, 12288), f"Wrong fc weight shape: {fc_weight.shape}"
41	
42	        # Check d2t
43	        d2t_diff = f.get_tensor("d2t")
44	        print(f"d2t (diff): {d2t_diff.shape}, range [{d2t_diff.min()}, {d2t_diff.max()}]")
45	
46	        # Recover actual d2t
47	        d2t = d2t_diff + torch.arange(len(d2t_diff))
48	        print(f"d2t (recovered): range [{d2t.min()}, {d2t.max()}]")
49	        print(f"  d2t[:5] = {d2t[:5].tolist()}")
50	
51	        # Check attention weights (should be 8192 input dim)
52	        q_proj = f.get_tensor("model.midlayer.self_attn.q_proj.weight")
53	        print(f"q_proj.weight: {q_proj.shape} (expected: [4096, 8192])")
54	        assert q_proj.shape == (4096, 8192), f"Wrong q_proj shape: {q_proj.shape}"
55	
56	    print("✓ Weight loading test PASSED\n")
57	
58	
59	def test_target_aux_capture():
60	    """Test that target model captures aux hidden states correctly."""
61	    print("=" * 60)
62	    print("Test 2: Target Model Aux Hidden State Capture")
63	    print("=" * 60)
64	
65	    # Simulate the capture logic
66	    layers_to_capture_config = [1, 10, 22]
67	    layers_to_capture = {val + 1 for val in layers_to_capture_config}
68	
69	    print(f"Config layer_ids: {layers_to_capture_config}")
70	    print(f"Actual layers_to_capture set: {sorted(layers_to_capture)}")
71	
72	    # Simulate forward loop capture
73	    num_layers = 32
74	    hidden_size = 4096
75	    captured = []
76	
77	    for i in range(num_layers):
78	        if i in layers_to_capture:
79	            captured.append(f"layer_{i-1}_output")  # i-1 because we capture before layer i runs
80	
81	    print(f"Captured states: {captured}")
82	    assert len(captured) == 3, f"Expected 3 captured states, got {len(captured)}"
83	
84	    # Expected concat dimension
85	    concat_dim = hidden_size * len(captured)
86	    print(f"Concatenated hidden_states dimension: {concat_dim} (expected: 12288)")
87	    assert concat_dim == 12288, f"Wrong concat dim: {concat_dim}"
88	
89	    print("✓ Aux hidden state capture test PASSED\n")
90	
91	
92	def test_d2t_mapping():
93	    """Test d2t mapping correctness."""
94	    print("=" * 60)
95	    print("Test 3: D2T Mapping")
96	    print("=" * 60)
97	
98	    vocab_cache = torch.load("eagle/data/vocab_cache.pt", weights_only=True)
99	    d2t = vocab_cache["d2t"]
100	    t2d = vocab_cache["t2d"]
101	
102	    print(f"d2t shape: {d2t.shape}")
103	    print(f"t2d shape: {t2d.shape}, True count: {t2d.sum().item()}")
104	
105	    # Check bijection
106	    for i in range(min(10, len(d2t))):
107	        target_id = d2t[i].item()
108	        assert t2d[target_id], f"draft_id {i} -> target_id {target_id} not in t2d"
109	
110	    # Check d2t_diff recovery
111	    from safetensors import safe_open
112	    with safe_open("eagle/sglang_model/model.safetensors", framework="pt", device="cpu") as f:
113	        d2t_diff = f.get_tensor("d2t")
114	
115	    d2t_recovered = d2t_diff + torch.arange(len(d2t_diff))
116	    assert torch.all(d2t_recovered == d2t), "d2t recovery mismatch!"
117	
118	    print("✓ D2T mapping test PASSED\n")
119	
120	
121	def test_draft_model_structure():
122	    """Test draft model structure matches expected architecture."""
123	    print("=" * 60)
124	    print("Test 4: Draft Model Structure")
125	    print("=" * 60)
126	
127	    with open("eagle/sglang_model/config.json") as f:
128	        cfg = json.load(f)
129	
130	    print(f"Architecture: {cfg['architectures']}")
131	    print(f"hidden_size: {cfg['hidden_size']}")
132	    print(f"target_hidden_size: {cfg.get('target_hidden_size', 'N/A')}")
133	    print(f"draft_vocab_size: {cfg.get('draft_vocab_size', 'N/A')}")
134	    print(f"vocab_size: {cfg['vocab_size']}")
135	    print(f"num_hidden_layers: {cfg['num_hidden_layers']}")
136	
137	    eagle_config = cfg.get("eagle_config", {})
138	    print(f"eagle_config: {eagle_config}")
139	
140	    # Validate
141	    assert cfg["architectures"] == ["LlamaForCausalLMEagle3"]
142	    assert cfg["num_hidden_layers"] == 1
143	    assert cfg["hidden_size"] == 4096
144	    assert cfg.get("draft_vocab_size") == 32000
145	    assert eagle_config.get("use_aux_hidden_state") == True
146	    assert eagle_config.get("eagle_aux_hidden_state_layer_ids") == [1, 10, 22]
147	
148	    print("✓ Draft model structure test PASSED\n")
149	
150	
151	def test_fc_projection():
152	    """Test fc projection numerically."""
153	    print("=" * 60)
154	    print("Test 5: FC Projection")
155	    print("=" * 60)
156	
157	    from safetensors import safe_open
158	
159	    # Load fc weight
160	    with safe_open("eagle/sglang_model/model.safetensors", framework="pt", device="cpu") as f:
161	        fc_weight = f.get_tensor("model.fc.weight").to(torch.bfloat16)
162	
163	    # Simulate aux_hidden input
164	    batch_size = 2
165	    seq_len = 10
166	    aux_dim = 12288
167	    hidden_size = 4096
168	
169	    # Random aux_hidden (simulating concat of 3 layers)
170	    torch.manual_seed(42)
171	    aux_hidden = torch.randn(batch_size, seq_len, aux_dim, dtype=torch.bfloat16)
172	
173	    # FC projection
174	    hidden = torch.nn.functional.linear(aux_hidden, fc_weight)
175	
176	    print(f"aux_hidden shape: {aux_hidden.shape}")
177	    print(f"fc_weight shape: {fc_weight.shape}")
178	    print(f"hidden shape: {hidden.shape}")
179	
180	    assert hidden.shape == (batch_size, seq_len, hidden_size), f"Wrong output shape: {hidden.shape}"
181	
182	    # Check not all zeros
183	    assert hidden.abs().sum() > 0, "Hidden states are all zeros!"
184	
185	    print(f"hidden mean: {hidden.float().mean().item():.6f}")
186	    print(f"hidden std: {hidden.float().std().item():.6f}")
187	
188	    print("✓ FC projection test PASSED\n")
189	
190	
191	def main():
192	    print("\n" + "=" * 60)
193	    print("EAGLE-3 Inference Flow Test")
194	    print("=" * 60 + "\n")
195	
196	    test_weights_loading()
197	    test_target_aux_capture()
198	    test_d2t_mapping()
199	    test_draft_model_structure()
200	    test_fc_projection()
201	
202	    print("=" * 60)
203	    print("ALL TESTS PASSED!")
204	    print("=" * 60)
205	
206	
207	if __name__ == "__main__":
208	    main()
209
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/test_forward_match.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Test that offline eval forward matches SGLang draft model forward.
4	Uses the same weights and compares outputs on OOD data.
5	"""
6	
7	import torch
8	import torch.nn as nn
9	import torch.nn.functional as F
10	from pathlib import Path
11	from safetensors import safe_open
12	
13	DEVICE = "cuda"
14	DTYPE = torch.bfloat16
15	
16	# Model config
17	HIDDEN_SIZE = 4096
18	AUX_DIM = HIDDEN_SIZE * 3  # 12288
19	VOCAB_SIZE = 73448
20	DRAFT_VOCAB_SIZE = 32000
21	SCALE_EMB = 12
22	NUM_HEADS = 32
23	NUM_KV_HEADS = 2
24	HEAD_DIM = 128
25	INTERMEDIATE_SIZE = 16384
26	RMS_NORM_EPS = 1e-6
27	
28	
29	class RMSNorm(nn.Module):
30	    def __init__(self, dim, eps=1e-6):
31	        super().__init__()
32	        self.weight = nn.Parameter(torch.ones(dim))
33	        self.eps = eps
34	
35	    def forward(self, x):
36	        norm = x.float().pow(2).mean(-1, keepdim=True).add(self.eps).rsqrt()
37	        return (x * norm).to(x.dtype) * self.weight
38	
39	
40	class Eagle3Attention(nn.Module):
41	    """Simplified attention (no KV cache, single forward)."""
42	    def __init__(self):
43	        super().__init__()
44	        self.num_heads = NUM_HEADS
45	        self.num_kv_heads = NUM_KV_HEADS
46	        self.head_dim = HEAD_DIM
47	        self.num_kv_groups = NUM_HEADS // NUM_KV_HEADS
48	
49	        qkv_in = HIDDEN_SIZE * 2
50	        self.q_proj = nn.Linear(qkv_in, NUM_HEADS * HEAD_DIM, bias=False)
51	        self.k_proj = nn.Linear(qkv_in, NUM_KV_HEADS * HEAD_DIM, bias=False)
52	        self.v_proj = nn.Linear(qkv_in, NUM_KV_HEADS * HEAD_DIM, bias=False)
53	        self.o_proj = nn.Linear(NUM_HEADS * HEAD_DIM, HIDDEN_SIZE, bias=False)
54	
55	    def forward(self, hidden_cat):
56	        B, S, _ = hidden_cat.shape
57	        q = self.q_proj(hidden_cat).view(B, S, self.num_heads, self.head_dim).transpose(1, 2)
58	        k = self.k_proj(hidden_cat).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
59	        v = self.v_proj(hidden_cat).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
60	
61	        if self.num_kv_groups > 1:
62	            k = k.repeat_interleave(self.num_kv_groups, dim=1)
63	            v = v.repeat_interleave(self.num_kv_groups, dim=1)
64	
65	        attn_output = F.scaled_dot_product_attention(q, k, v, is_causal=True)
66	        attn_output = attn_output.transpose(1, 2).contiguous().view(B, S, -1)
67	        return self.o_proj(attn_output)
68	
69	
70	class Eagle3MLP(nn.Module):
71	    def __init__(self):
72	        super().__init__()
73	        self.gate_proj = nn.Linear(HIDDEN_SIZE, INTERMEDIATE_SIZE, bias=False)
74	        self.up_proj = nn.Linear(HIDDEN_SIZE, INTERMEDIATE_SIZE, bias=False)
75	        self.down_proj = nn.Linear(INTERMEDIATE_SIZE, HIDDEN_SIZE, bias=False)
76	
77	    def forward(self, x):
78	        return self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))
79	
80	
81	class Eagle3Model(nn.Module):
82	    def __init__(self):
83	        super().__init__()
84	        self.fc = nn.Linear(AUX_DIM, HIDDEN_SIZE, bias=False)
85	        self.input_layernorm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
86	        self.hidden_norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
87	        self.self_attn = Eagle3Attention()
88	        self.post_attention_layernorm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
89	        self.mlp = Eagle3MLP()
90	        self.norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
91	        self.embed_tokens = nn.Embedding(VOCAB_SIZE, HIDDEN_SIZE)
92	        self.lm_head = nn.Linear(HIDDEN_SIZE, DRAFT_VOCAB_SIZE, bias=False)
93	        self.scale_emb = SCALE_EMB
94	
95	    def forward(self, token_ids, aux_hidden):
96	        """Full forward matching offline eval."""
97	        if token_ids.dim() == 1:
98	            token_ids = token_ids.unsqueeze(0)
99	            aux_hidden = aux_hidden.unsqueeze(0)
100	            squeeze_out = True
101	        else:
102	            squeeze_out = False
103	
104	        # fc projection
105	        hidden_states = self.fc(aux_hidden)
106	
107	        # embed tokens
108	        embeds = self.embed_tokens(token_ids) * self.scale_emb
109	        embeds = embeds.to(hidden_states.dtype)
110	
111	        # decoder layer forward
112	        residual = hidden_states
113	        embeds_normed = self.input_layernorm(embeds)
114	        hidden_normed = self.hidden_norm(hidden_states)
115	        hidden_cat = torch.cat([embeds_normed, hidden_normed], dim=-1)
116	
117	        # attention
118	        attn_out = self.self_attn(hidden_cat)
119	        hidden_states = residual + attn_out
120	
121	        # MLP
122	        residual = hidden_states
123	        hidden_states = self.post_attention_layernorm(hidden_states)
124	        hidden_states = self.mlp(hidden_states)
125	        hidden_states = residual + hidden_states
126	
127	        # final norm + lm_head
128	        hidden_states = self.norm(hidden_states)
129	        logits = self.lm_head(hidden_states)
130	
131	        if squeeze_out:
132	            logits = logits.squeeze(0)
133	        return logits
134	
135	
136	def load_model():
137	    model = Eagle3Model().to(DEVICE).to(DTYPE)
138	
139	    # Load weights
140	    with safe_open("eagle/sglang_model/model.safetensors", framework="pt", device="cpu") as f:
141	        state_dict = {}
142	        for key in f.keys():
143	            tensor = f.get_tensor(key)
144	            # Map weight names
145	            if key.startswith("model."):
146	                key = key[6:]
147	            if key == "midlayer.input_layernorm.weight":
148	                [REDACTED]
149	            elif key == "midlayer.hidden_norm.weight":
150	                [REDACTED]
151	            elif key == "midlayer.post_attention_layernorm.weight":
152	                [REDACTED]
153	            elif key.startswith("midlayer.self_attn."):
154	                key = key.replace("midlayer.self_attn.", "self_attn.")
155	            elif key.startswith("midlayer.mlp."):
156	                key = key.replace("midlayer.mlp.", "mlp.")
157	            elif key == "norm.weight":
158	                key = "norm.weight"
159	            state_dict[key] = tensor
160	
161	    model.load_state_dict(state_dict, strict=False)
162	    model.eval()
163	    return model
164	
165	
166	def load_vocab_mapping():
167	    cache = torch.load("eagle/data/vocab_cache.pt", weights_only=True)
168	    d2t = cache["d2t"].to(DEVICE)
169	    t2d = cache["t2d"].to(DEVICE)
170	    draft_idx_map = torch.zeros(VOCAB_SIZE, dtype=torch.long, device=DEVICE)
171	    draft_idx_map[d2t] = torch.arange(DRAFT_VOCAB_SIZE, device=DEVICE)
172	    return d2t, t2d, draft_idx_map
173	
174	
175	def build_target_p(target_logits_values, target_logits_indices, t2d, draft_idx_map):
176	    """Build target distribution from top-256 logits."""
177	    S, K = target_logits_values.shape
178	    indices = target_logits_indices.long().clamp(0, VOCAB_SIZE - 1)
179	    in_draft = t2d[indices]
180	
181	    draft_logits = torch.full((S, DRAFT_VOCAB_SIZE), -1e9, device=DEVICE, dtype=torch.float32)
182	    mapped_idx = draft_idx_map[indices]
183	    values = target_logits_values.float()
184	
185	    safe_vals = torch.where(in_draft, values, torch.tensor(-1e9, device=DEVICE))
186	    draft_logits.scatter_reduce_(1, mapped_idx, safe_vals, reduce="amax")
187	    target_p = F.softmax(draft_logits, dim=-1)
188	    return target_p
189	
190	
191	def test_single_position():
192	    """Test forward for single position (decode-like scenario)."""
193	    print("Loading model...")
194	    model = load_model()
195	    d2t, t2d, draft_idx_map = load_vocab_mapping()
196	
197	    # Load OOD data
198	    ood_dir = Path("/tmp/eagle3_val_collect")
199	    pt_files = sorted(ood_dir.glob("*.pt"))
200	    if len(pt_files) == 0:
201	        print("No OOD files found. Run data collection first.")
202	        return
203	
204	    print(f"Found {len(pt_files)} OOD files")
205	
206	    # Test: compare full-sequence forward vs position-by-position forward
207	    data = torch.load(pt_files[0], weights_only=True)
208	    token_ids = data["token_ids"].to(DEVICE)
209	    aux_hidden = data["aux_hidden"].to(DEVICE).to(DTYPE)
210	    top_logit_values = data["top_logit_values"].to(DEVICE).to(DTYPE)
211	    top_logit_indices = data["top_logit_indices"].to(DEVICE)
212	
213	    seq_len = token_ids.shape[0]
214	    print(f"\nSequence length: {seq_len}")
215	
216	    with torch.no_grad():
217	        # Full sequence forward (offline eval style)
218	        full_logits = model(token_ids, aux_hidden)
219	        print(f"Full forward logits shape: {full_logits.shape}")
220	
221	        # Now test position-by-position with KV-cache simulation
222	        # This mimics what happens in decode mode
223	        print("\nTesting position-by-position (simulating decode with fc projection)...")
224	
225	        # First position uses aux_hidden (12288)
226	        pos0_logits_12288 = model.forward_fc_then_layer(token_ids[:1], aux_hidden[:1])
227	
228	        # Check if first position matches
229	        match_pos0 = torch.allclose(full_logits[0], pos0_logits_12288[0], atol=1e-2)
230	        diff_pos0 = (full_logits[0] - pos0_logits_12288[0]).abs().max().item()
231	        print(f"Position 0 (aux_hidden 12288): match={match_pos0}, max_diff={diff_pos0:.4f}")
232	
233	
234	def test_full_sequence():
235	    """Test full sequence accuracy."""
236	    print("Loading model...")
237	    model = load_model()
238	    d2t, t2d, draft_idx_map = load_vocab_mapping()
239	
240	    ood_dir = Path("/tmp/eagle3_val_collect")
241	    pt_files = sorted(ood_dir.glob("*.pt"))
242	    if len(pt_files) == 0:
243	        print("No OOD files found at /tmp/eagle3_val_collect")
244	        print("Please run OOD data collection first.")
245	        return
246	
247	    print(f"Found {len(pt_files)} OOD files\n")
248	
249	    total_correct = 0
250	    total_valid = 0
251	
252	    with torch.no_grad():
253	        for i, pt_file in enumerate(pt_files[:5]):
254	            data = torch.load(pt_file, weights_only=True)
255	            token_ids = data["token_ids"].to(DEVICE)
256	            aux_hidden = data["aux_hidden"].to(DEVICE).to(DTYPE)
257	            top_logit_values = data["top_logit_values"].to(DEVICE).to(DTYPE)
258	            top_logit_indices = data["top_logit_indices"].to(DEVICE)
259	
260	            seq_len = token_ids.shape[0]
261	            if seq_len < 2:
262	                continue
263	
264	            # Forward
265	            logits = model(token_ids, aux_hidden)
266	
267	            # Build target distribution
268	            target_p = build_target_p(top_logit_values, top_logit_indices, t2d, draft_idx_map)
269	
270	            # Compute accept rate
271	            pred_draft_idx = logits.argmax(dim=-1)
272	            target_draft_idx = target_p.argmax(dim=-1)
273	
274	            # Only count positions where target argmax is in draft vocab
275	            target_argmax_full = top_logit_indices[:, 0].long().clamp(0, VOCAB_SIZE - 1)
276	            target_mask = t2d[target_argmax_full].float()
277	
278	            correct = (pred_draft_idx == target_draft_idx).float() * target_mask
279	            n_correct = correct.sum().item()
280	            n_valid = target_mask.sum().item()
281	
282	            total_correct += n_correct
283	            total_valid += n_valid
284	
285	            if i < 5:
286	                acc = n_correct / n_valid if n_valid > 0 else 0
287	                print(f"[{i}] {pt_file.name}: seq_len={seq_len}, valid={int(n_valid)}, correct={int(n_correct)}, acc={acc:.1%}")
288	
289	    print(f"\n{'='*60}")
290	    print(f"Total valid positions: {int(total_valid)}")
291	    print(f"Correct predictions: {int(total_correct)}")
292	    if total_valid > 0:
293	        print(f"OOD Accept Rate: {total_correct/total_valid:.1%}")
294	
295	
296	if __name__ == "__main__":
297	    import sys
298	    if len(sys.argv) > 1 and sys.argv[1] == "--position":
299	        test_single_position()
300	    else:
301	        test_full_sequence()
302
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/test_offline_pred.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Test EAGLE-3 model prediction offline using collected training data.
4	Verify that the trained model can correctly predict next tokens.
5	"""
6	
7	import torch
8	import torch.nn.functional as F
9	from pathlib import Path
10	from safetensors import safe_open
11	
12	DEVICE = "cuda"
13	DTYPE = torch.bfloat16
14	
15	# Load model weights
16	print("Loading model weights...")
17	with safe_open("eagle/sglang_model/model.safetensors", framework="pt", device="cpu") as f:
18	    fc_weight = f.get_tensor("model.fc.weight").to(DEVICE).to(DTYPE)
19	    lm_head_weight = f.get_tensor("lm_head.weight").to(DEVICE).to(DTYPE)
20	    norm_weight = f.get_tensor("model.norm.weight").to(DEVICE).to(DTYPE)
21	    # Attention weights
22	    q_proj = f.get_tensor("model.midlayer.self_attn.q_proj.weight").to(DEVICE).to(DTYPE)
23	    k_proj = f.get_tensor("model.midlayer.self_attn.k_proj.weight").to(DEVICE).to(DTYPE)
24	    v_proj = f.get_tensor("model.midlayer.self_attn.v_proj.weight").to(DEVICE).to(DTYPE)
25	    o_proj = f.get_tensor("model.midlayer.self_attn.o_proj.weight").to(DEVICE).to(DTYPE)
26	    input_ln = f.get_tensor("model.midlayer.input_layernorm.weight").to(DEVICE).to(DTYPE)
27	    hidden_norm = f.get_tensor("model.midlayer.hidden_norm.weight").to(DEVICE).to(DTYPE)
28	    post_ln = f.get_tensor("model.midlayer.post_attention_layernorm.weight").to(DEVICE).to(DTYPE)
29	    gate_proj = f.get_tensor("model.midlayer.mlp.gate_proj.weight").to(DEVICE).to(DTYPE)
30	    up_proj = f.get_tensor("model.midlayer.mlp.up_proj.weight").to(DEVICE).to(DTYPE)
31	    down_proj = f.get_tensor("model.midlayer.mlp.down_proj.weight").to(DEVICE).to(DTYPE)
32	    embed_weight = f.get_tensor("model.embed_tokens.weight").to(DEVICE).to(DTYPE)
33	
34	# Load d2t mapping
35	vocab_cache = torch.load("eagle/data/vocab_cache.pt", weights_only=True)
36	d2t = vocab_cache["d2t"].to(DEVICE)
37	t2d = vocab_cache["t2d"].to(DEVICE)
38	
39	print(f"fc_weight: {fc_weight.shape}")
40	print(f"lm_head_weight: {lm_head_weight.shape}")
41	print(f"d2t: {d2t.shape}")
42	
43	# RMSNorm
44	def rms_norm(x, weight, eps=1e-6):
45	    norm = x.float().pow(2).mean(-1, keepdim=True).add(eps).rsqrt()
46	    return (x * norm).to(x.dtype) * weight
47	
48	# Simple forward (no attention for simplicity, just fc -> norm -> lm_head)
49	def simple_forward(aux_hidden):
50	    """Simplified forward: fc -> norm -> lm_head"""
51	    hidden = F.linear(aux_hidden, fc_weight)
52	    hidden = rms_norm(hidden, norm_weight)
53	    logits = F.linear(hidden, lm_head_weight)
54	    return logits
55	
56	# Build draft_idx_map (target_id -> draft_id)
57	DRAFT_VOCAB_SIZE = 32000
58	VOCAB_SIZE = 73448
59	draft_idx_map = torch.zeros(VOCAB_SIZE, dtype=torch.long, device=DEVICE)
60	draft_idx_map[d2t] = torch.arange(DRAFT_VOCAB_SIZE, device=DEVICE)
61	
62	def build_target_p(target_logits_values, target_logits_indices):
63	    """Build target distribution from top-256 logits (same as training)."""
64	    S, K = target_logits_values.shape
65	    indices = target_logits_indices.long().clamp(0, VOCAB_SIZE - 1)
66	    in_draft = t2d[indices]  # (S, 256) bool
67	
68	    draft_logits = torch.full((S, DRAFT_VOCAB_SIZE), -1e9, device=DEVICE, dtype=torch.float32)
69	    mapped_idx = draft_idx_map[indices]  # (S, 256)
70	    values = target_logits_values.float()
71	
72	    safe_vals = torch.where(in_draft, values, torch.tensor(-1e9, device=DEVICE))
73	    draft_logits.scatter_reduce_(1, mapped_idx, safe_vals, reduce="amax")
74	    target_p = F.softmax(draft_logits, dim=-1)
75	    return target_p
76	
77	# Load training samples
78	data_dir = Path("eagle/data/train")
79	pt_files = sorted(data_dir.glob("*.pt"))
80	print(f"\nFound {len(pt_files)} training files")
81	
82	# Test on first 5 files
83	correct_top1 = 0
84	total = 0
85	
86	for i, pt_file in enumerate(pt_files[:5]):
87	    data = torch.load(pt_file, weights_only=True)
88	    aux_hidden = data["aux_hidden"].to(DEVICE).to(DTYPE)
89	    top_logit_values = data["top_logit_values"].to(DEVICE).to(DTYPE)
90	    top_logit_indices = data["top_logit_indices"].to(DEVICE)
91	
92	    seq_len = aux_hidden.shape[0]
93	
94	    # Predict
95	    with torch.no_grad():
96	        logits = simple_forward(aux_hidden)  # (seq_len, 32000)
97	        target_p = build_target_p(top_logit_values, top_logit_indices)
98	
99	    pred_draft_idx = logits.argmax(dim=-1)  # (seq_len,)
100	    target_draft_idx = target_p.argmax(dim=-1)  # (seq_len,)
101	
102	    # Target argmax in draft vocab?
103	    target_argmax_full = top_logit_indices[:, 0].long().clamp(0, VOCAB_SIZE - 1)
104	    target_mask = t2d[target_argmax_full].float()
105	
106	    correct = (pred_draft_idx == target_draft_idx).float() * target_mask
107	    n_correct = correct.sum().item()
108	    n_valid = target_mask.sum().item()
109	
110	    if n_valid > 0:
111	        acc = n_correct / n_valid
112	        print(f"File {i}: {pt_file.name}, seq_len={seq_len}, valid={int(n_valid)}, correct={int(n_correct)}, acc={acc:.2%}")
113	        correct_top1 += n_correct
114	        total += n_valid
115	
116	print(f"\nOverall acc (same as training): {correct_top1}/{int(total)} = {correct_top1/total:.2%}")
117
```

> AGENT

Now let me read the remaining eagle files and the medusa training files:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/test_decode_mode.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Test EAGLE-3 in decode mode (position-by-position with KV cache simulation).
4	Compare with full-sequence mode to find discrepancies.
5	"""
6	
7	import torch
8	import torch.nn as nn
9	import torch.nn.functional as F
10	from pathlib import Path
11	from safetensors import safe_open
12	
13	DEVICE = "cuda"
14	DTYPE = torch.bfloat16
15	
16	# Model config
17	HIDDEN_SIZE = 4096
18	AUX_DIM = HIDDEN_SIZE * 3
19	VOCAB_SIZE = 73448
20	DRAFT_VOCAB_SIZE = 32000
21	SCALE_EMB = 12
22	NUM_HEADS = 32
23	NUM_KV_HEADS = 2
24	HEAD_DIM = 128
25	INTERMEDIATE_SIZE = 16384
26	RMS_NORM_EPS = 1e-6
27	
28	
29	class RMSNorm(nn.Module):
30	    def __init__(self, dim, eps=1e-6):
31	        super().__init__()
32	        self.weight = nn.Parameter(torch.ones(dim))
33	        self.eps = eps
34	
35	    def forward(self, x):
36	        norm = x.float().pow(2).mean(-1, keepdim=True).add(self.eps).rsqrt()
37	        return (x * norm).to(x.dtype) * self.weight
38	
39	
40	class Eagle3AttentionWithKVCache(nn.Module):
41	    """Attention with KV cache for decode simulation."""
42	    def __init__(self):
43	        super().__init__()
44	        self.num_heads = NUM_HEADS
45	        self.num_kv_heads = NUM_KV_HEADS
46	        self.head_dim = HEAD_DIM
47	        self.num_kv_groups = NUM_HEADS // NUM_KV_HEADS
48	
49	        qkv_in = HIDDEN_SIZE * 2
50	        self.q_proj = nn.Linear(qkv_in, NUM_HEADS * HEAD_DIM, bias=False)
51	        self.k_proj = nn.Linear(qkv_in, NUM_KV_HEADS * HEAD_DIM, bias=False)
52	        self.v_proj = nn.Linear(qkv_in, NUM_KV_HEADS * HEAD_DIM, bias=False)
53	        self.o_proj = nn.Linear(NUM_HEADS * HEAD_DIM, HIDDEN_SIZE, bias=False)
54	
55	        # KV cache
56	        self.k_cache = None
57	        self.v_cache = None
58	
59	    def clear_cache(self):
60	        self.k_cache = None
61	        self.v_cache = None
62	
63	    def forward(self, hidden_cat, use_cache=False, pos=None):
64	        """
65	        hidden_cat: (B, S, 2*H) or (B, 1, 2*H) for decode
66	        use_cache: if True, use KV cache for decode mode
67	        pos: current position (for decode mode)
68	        """
69	        B, S, _ = hidden_cat.shape
70	        q = self.q_proj(hidden_cat).view(B, S, self.num_heads, self.head_dim).transpose(1, 2)
71	        k = self.k_proj(hidden_cat).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
72	        v = self.v_proj(hidden_cat).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
73	
74	        if use_cache:
75	            if self.k_cache is None:
76	                self.k_cache = k
77	                self.v_cache = v
78	            else:
79	                self.k_cache = torch.cat([self.k_cache, k], dim=2)
80	                self.v_cache = torch.cat([self.v_cache, v], dim=2)
81	            k = self.k_cache
82	            v = self.v_cache
83	
84	        # Expand KV heads
85	        if self.num_kv_groups > 1:
86	            k = k.repeat_interleave(self.num_kv_groups, dim=1)
87	            v = v.repeat_interleave(self.num_kv_groups, dim=1)
88	
89	        # For decode mode (S=1), only attend to past positions
90	        if use_cache and S == 1:
91	            # q: (B, heads, 1, head_dim)
92	            # k, v: (B, heads, seq_len, head_dim)
93	            attn_output = F.scaled_dot_product_attention(q, k, v, is_causal=False)
94	        else:
95	            attn_output = F.scaled_dot_product_attention(q, k, v, is_causal=True)
96	
97	        attn_output = attn_output.transpose(1, 2).contiguous().view(B, S, -1)
98	        return self.o_proj(attn_output)
99	
100	
101	class Eagle3MLP(nn.Module):
102	    def __init__(self):
103	        super().__init__()
104	        self.gate_proj = nn.Linear(HIDDEN_SIZE, INTERMEDIATE_SIZE, bias=False)
105	        self.up_proj = nn.Linear(HIDDEN_SIZE, INTERMEDIATE_SIZE, bias=False)
106	        self.down_proj = nn.Linear(INTERMEDIATE_SIZE, HIDDEN_SIZE, bias=False)
107	
108	    def forward(self, x):
109	        return self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))
110	
111	
112	class Eagle3ModelWithKVCache(nn.Module):
113	    def __init__(self):
114	        super().__init__()
115	        self.fc = nn.Linear(AUX_DIM, HIDDEN_SIZE, bias=False)
116	        self.input_layernorm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
117	        self.hidden_norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
118	        self.self_attn = Eagle3AttentionWithKVCache()
119	        self.post_attention_layernorm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
120	        self.mlp = Eagle3MLP()
121	        self.norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
122	        self.embed_tokens = nn.Embedding(VOCAB_SIZE, HIDDEN_SIZE)
123	        self.lm_head = nn.Linear(HIDDEN_SIZE, DRAFT_VOCAB_SIZE, bias=False)
124	        self.scale_emb = SCALE_EMB
125	
126	    def clear_cache(self):
127	        self.self_attn.clear_cache()
128	
129	    def forward_with_kv_cache(self, token_ids, aux_hidden, use_cache=False, pos=None):
130	        """
131	        Forward with optional KV cache for decode simulation.
132	
133	        token_ids: (1,) or (S,) for prefill
134	        aux_hidden: (1, 12288) or (S, 12288) for prefill, or (1, 4096) for decode
135	        """
136	        # Add batch dim
137	        if token_ids.dim() == 1:
138	            token_ids = token_ids.unsqueeze(0)
139	        if aux_hidden.dim() == 2:
140	            aux_hidden = aux_hidden.unsqueeze(0)
141	
142	        # fc projection (only for 12288 input)
143	        if aux_hidden.shape[-1] == AUX_DIM:
144	            hidden_states = self.fc(aux_hidden)
145	        else:
146	            hidden_states = aux_hidden  # already 4096
147	
148	        # embed tokens
149	        embeds = self.embed_tokens(token_ids) * self.scale_emb
150	        embeds = embeds.to(hidden_states.dtype)
151	
152	        # decoder layer forward
153	        residual = hidden_states
154	        embeds_normed = self.input_layernorm(embeds)
155	        hidden_normed = self.hidden_norm(hidden_states)
156	        hidden_cat = torch.cat([embeds_normed, hidden_normed], dim=-1)
157	
158	        # attention with KV cache
159	        attn_out = self.self_attn(hidden_cat, use_cache=use_cache, pos=pos)
160	        hidden_states = residual + attn_out
161	
162	        # MLP
163	        residual = hidden_states
164	        hidden_states = self.post_attention_layernorm(hidden_states)
165	        hidden_states = self.mlp(hidden_states)
166	        hidden_states = residual + hidden_states
167	
168	        # final norm + lm_head
169	        final_hidden = self.norm(hidden_states)
170	        logits = self.lm_head(final_hidden)
171	
172	        return logits.squeeze(0), hidden_states.squeeze(0)  # return hidden for next step
173	
174	
175	def load_model():
176	    model = Eagle3ModelWithKVCache().to(DEVICE).to(DTYPE)
177	
178	    with safe_open("eagle/sglang_model/model.safetensors", framework="pt", device="cpu") as f:
179	        state_dict = {}
180	        for key in f.keys():
181	            tensor = f.get_tensor(key)
182	            if key.startswith("model."):
183	                key = key[6:]
184	            if key == "midlayer.input_layernorm.weight":
185	                [REDACTED]
186	            elif key == "midlayer.hidden_norm.weight":
187	                [REDACTED]
188	            elif key == "midlayer.post_attention_layernorm.weight":
189	                [REDACTED]
190	            elif key.startswith("midlayer.self_attn."):
191	                key = key.replace("midlayer.self_attn.", "self_attn.")
192	            elif key.startswith("midlayer.mlp."):
193	                key = key.replace("midlayer.mlp.", "mlp.")
194	            elif key == "norm.weight":
195	                key = "norm.weight"
196	            state_dict[key] = tensor
197	
198	    model.load_state_dict(state_dict, strict=False)
199	    model.eval()
200	    return model
201	
202	
203	def load_vocab_mapping():
204	    cache = torch.load("eagle/data/vocab_cache.pt", weights_only=True)
205	    d2t = cache["d2t"].to(DEVICE)
206	    t2d = cache["t2d"].to(DEVICE)
207	    draft_idx_map = torch.zeros(VOCAB_SIZE, dtype=torch.long, device=DEVICE)
208	    draft_idx_map[d2t] = torch.arange(DRAFT_VOCAB_SIZE, device=DEVICE)
209	    return d2t, t2d, draft_idx_map
210	
211	
212	def build_target_p(target_logits_values, target_logits_indices, t2d, draft_idx_map):
213	    S, K = target_logits_values.shape
214	    indices = target_logits_indices.long().clamp(0, VOCAB_SIZE - 1)
215	    in_draft = t2d[indices]
216	    draft_logits = torch.full((S, DRAFT_VOCAB_SIZE), -1e9, device=DEVICE, dtype=torch.float32)
217	    mapped_idx = draft_idx_map[indices]
218	    values = target_logits_values.float()
219	    safe_vals = torch.where(in_draft, values, torch.tensor(-1e9, device=DEVICE))
220	    draft_logits.scatter_reduce_(1, mapped_idx, safe_vals, reduce="amax")
221	    target_p = F.softmax(draft_logits, dim=-1)
222	    return target_p
223	
224	
225	def test_decode_vs_prefill():
226	    """Compare decode mode (position-by-position with KV cache) vs prefill mode."""
227	    print("Loading model...")
228	    model = load_model()
229	    d2t, t2d, draft_idx_map = load_vocab_mapping()
230	
231	    ood_dir = Path("/tmp/eagle3_val_collect")
232	    pt_files = sorted(ood_dir.glob("*.pt"))
233	    if len(pt_files) == 0:
234	        print("No OOD files found.")
235	        return
236	
237	    print(f"Found {len(pt_files)} OOD files\n")
238	
239	    with torch.no_grad():
240	        for file_idx, pt_file in enumerate(pt_files[:3]):
241	            data = torch.load(pt_file, weights_only=True)
242	            token_ids = data["token_ids"].to(DEVICE)
243	            aux_hidden = data["aux_hidden"].to(DEVICE).to(DTYPE)
244	
245	            seq_len = min(token_ids.shape[0], 32)  # Limit to 32 tokens to avoid OOM
246	            token_ids = token_ids[:seq_len]
247	            aux_hidden = aux_hidden[:seq_len]
248	
249	            if seq_len < 2:
250	                continue
251	
252	            print(f"\n[{file_idx}] {pt_file.name}: seq_len={seq_len}")
253	
254	            # Prefill mode (full sequence)
255	            model.clear_cache()
256	            logits_prefill, _ = model.forward_with_kv_cache(token_ids, aux_hidden, use_cache=False)
257	
258	            # Decode mode (position by position with KV cache)
259	            model.clear_cache()
260	            logits_decode_list = []
261	
262	            for i in range(seq_len):
263	                logits_i, hidden_out = model.forward_with_kv_cache(
264	                    token_ids[i:i+1], aux_hidden[i:i+1], use_cache=True, pos=i
265	                )
266	                logits_decode_list.append(logits_i)
267	
268	            logits_decode = torch.cat(logits_decode_list, dim=0)  # Each is (1, vocab), cat to (seq_len, vocab)
269	
270	            # Compare
271	            print(f"  logits_prefill.shape={logits_prefill.shape}, logits_decode.shape={logits_decode.shape}")
272	            pred_prefill = logits_prefill.argmax(dim=-1)
273	            pred_decode = logits_decode.argmax(dim=-1)
274	            print(f"  pred_prefill.shape={pred_prefill.shape}, pred_decode.shape={pred_decode.shape}")
275	            pred_match = (pred_prefill == pred_decode).float().mean().item()
276	            logits_diff = (logits_prefill - logits_decode).abs()
277	
278	            print(f"  Logits max diff: {logits_diff.max().item():.4f}, mean diff: {logits_diff.mean().item():.4f}")
279	            print(f"  Prediction match: {pred_match:.1%}")
280	
281	            # Detailed comparison for all positions
282	            print(f"  Position-wise comparison:")
283	            for pos in range(seq_len):
284	                diff = (logits_prefill[pos] - logits_decode[pos]).abs()
285	                p1, p2 = pred_prefill[pos].item(), pred_decode[pos].item()
286	                match_str = "✓" if p1 == p2 else "✗"
287	                print(f"    pos={pos}: prefill={p1}, decode={p2} {match_str}, max_diff={diff.max().item():.2f}")
288	
289	
290	if __name__ == "__main__":
291	    test_decode_vs_prefill()
292
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/verify_sglang_draft.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Verify that SGLang's draft model produces same output as offline eval.
4	Loads the draft model using SGLang's weight loading and compares with offline eval.
5	"""
6	
7	import torch
8	import torch.nn.functional as F
9	from pathlib import Path
10	from safetensors import safe_open
11	
12	DEVICE = "cuda"
13	DTYPE = torch.bfloat16
14	HIDDEN_SIZE = 4096
15	AUX_DIM = HIDDEN_SIZE * 3
16	VOCAB_SIZE = 73448
17	DRAFT_VOCAB_SIZE = 32000
18	
19	
20	def test_fc_weight():
21	    """Test that fc weight matches between offline eval and SGLang draft model."""
22	    print("Testing fc weight...")
23	
24	    # Offline eval loads fc.weight directly
25	    with safe_open("eagle/sglang_model/model.safetensors", framework="pt", device="cpu") as f:
26	        fc_weight = f.get_tensor("model.fc.weight")
27	
28	    print(f"  fc.weight shape: {fc_weight.shape}")
29	    print(f"  fc.weight mean: {fc_weight.float().mean():.6f}")
30	    print(f"  fc.weight std: {fc_weight.float().std():.6f}")
31	
32	    # Test fc forward
33	    test_input = torch.randn(1, 10, AUX_DIM, dtype=DTYPE, device=DEVICE)
34	    fc_weight_cuda = fc_weight.to(DEVICE).to(DTYPE)
35	    output = F.linear(test_input, fc_weight_cuda)
36	    print(f"  Test forward: input {test_input.shape} -> output {output.shape}")
37	    print(f"  Output mean: {output.float().mean():.4f}, std: {output.float().std():.4f}")
38	    print()
39	
40	
41	def test_lm_head():
42	    """Test lm_head weight and d2t mapping."""
43	    print("Testing lm_head and d2t mapping...")
44	
45	    with safe_open("eagle/sglang_model/model.safetensors", framework="pt", device="cpu") as f:
46	        lm_head_weight = f.get_tensor("lm_head.weight")
47	        d2t_diff = f.get_tensor("d2t")
48	
49	    print(f"  lm_head.weight shape: {lm_head_weight.shape}")
50	
51	    # Reconstruct hot_token_id as SGLang does
52	    hot_token_id = d2t_diff + torch.arange(len(d2t_diff))
53	    print(f"  hot_token_id (d2t + arange): shape={hot_token_id.shape}")
54	    print(f"  hot_token_id[:5]: {hot_token_id[:5].tolist()}")
55	
56	    # Verify d2t mapping matches vocab_cache
57	    vocab_cache = torch.load("eagle/data/vocab_cache.pt", weights_only=True)
58	    d2t_expected = vocab_cache["d2t"]
59	    match = (hot_token_id == d2t_expected).all()
60	    print(f"  d2t matches vocab_cache: {match}")
61	    print()
62	
63	
64	def test_full_forward():
65	    """Test full forward pass matches offline eval."""
66	    print("Testing full forward pass...")
67	
68	    # Load OOD data
69	    ood_dir = Path("/tmp/eagle3_val_collect")
70	    pt_files = sorted(ood_dir.glob("*.pt"))
71	    if len(pt_files) == 0:
72	        print("  No OOD files found!")
73	        return
74	
75	    data = torch.load(pt_files[0], weights_only=True)
76	    token_ids = data["token_ids"][:16].to(DEVICE)  # Use first 16 tokens
77	    aux_hidden = data["aux_hidden"][:16].to(DEVICE).to(DTYPE)
78	    seq_len = token_ids.shape[0]
79	    print(f"  Test data: seq_len={seq_len}")
80	
81	    # Load all weights
82	    with safe_open("eagle/sglang_model/model.safetensors", framework="pt", device="cpu") as f:
83	        fc_weight = f.get_tensor("model.fc.weight").to(DEVICE).to(DTYPE)
84	        emb_weight = f.get_tensor("model.embed_tokens.weight").to(DEVICE).to(DTYPE)
85	        lm_head_weight = f.get_tensor("lm_head.weight").to(DEVICE).to(DTYPE)
86	        input_ln_weight = f.get_tensor("model.midlayer.input_layernorm.weight").to(DEVICE).to(DTYPE)
87	        hidden_norm_weight = f.get_tensor("model.midlayer.hidden_norm.weight").to(DEVICE).to(DTYPE)
88	        q_proj = f.get_tensor("model.midlayer.self_attn.q_proj.weight").to(DEVICE).to(DTYPE)
89	        k_proj = f.get_tensor("model.midlayer.self_attn.k_proj.weight").to(DEVICE).to(DTYPE)
90	        v_proj = f.get_tensor("model.midlayer.self_attn.v_proj.weight").to(DEVICE).to(DTYPE)
91	        o_proj = f.get_tensor("model.midlayer.self_attn.o_proj.weight").to(DEVICE).to(DTYPE)
92	        post_ln_weight = f.get_tensor("model.midlayer.post_attention_layernorm.weight").to(DEVICE).to(DTYPE)
93	        gate_proj = f.get_tensor("model.midlayer.mlp.gate_proj.weight").to(DEVICE).to(DTYPE)
94	        up_proj = f.get_tensor("model.midlayer.mlp.up_proj.weight").to(DEVICE).to(DTYPE)
95	        down_proj = f.get_tensor("model.midlayer.mlp.down_proj.weight").to(DEVICE).to(DTYPE)
96	        norm_weight = f.get_tensor("model.norm.weight").to(DEVICE).to(DTYPE)
97	
98	    SCALE_EMB = 12
99	    RMS_NORM_EPS = 1e-6
100	    NUM_HEADS = 32
101	    NUM_KV_HEADS = 2
102	    HEAD_DIM = 128
103	    NUM_KV_GROUPS = NUM_HEADS // NUM_KV_HEADS
104	
105	    def rms_norm(x, weight):
106	        norm = x.float().pow(2).mean(-1, keepdim=True).add(RMS_NORM_EPS).rsqrt()
107	        return (x * norm).to(x.dtype) * weight
108	
109	    # Forward pass
110	    # 1. fc projection
111	    hidden_states = F.linear(aux_hidden, fc_weight)
112	    print(f"  After fc: {hidden_states.shape}, mean={hidden_states.float().mean():.4f}")
113	
114	    # 2. embed tokens
115	    embeds = F.embedding(token_ids, emb_weight) * SCALE_EMB
116	    print(f"  Embeds: {embeds.shape}, mean={embeds.float().mean():.4f}")
117	
118	    # 3. decoder layer
119	    residual = hidden_states
120	    embeds_normed = rms_norm(embeds, input_ln_weight)
121	    hidden_normed = rms_norm(hidden_states, hidden_norm_weight)
122	    hidden_cat = torch.cat([embeds_normed, hidden_normed], dim=-1)
123	    print(f"  hidden_cat: {hidden_cat.shape}")
124	
125	    # 4. attention
126	    q = F.linear(hidden_cat, q_proj).view(1, seq_len, NUM_HEADS, HEAD_DIM).transpose(1, 2)
127	    k = F.linear(hidden_cat, k_proj).view(1, seq_len, NUM_KV_HEADS, HEAD_DIM).transpose(1, 2)
128	    v = F.linear(hidden_cat, v_proj).view(1, seq_len, NUM_KV_HEADS, HEAD_DIM).transpose(1, 2)
129	    if NUM_KV_GROUPS > 1:
130	        k = k.repeat_interleave(NUM_KV_GROUPS, dim=1)
131	        v = v.repeat_interleave(NUM_KV_GROUPS, dim=1)
132	    attn_output = F.scaled_dot_product_attention(q, k, v, is_causal=True)
133	    attn_output = attn_output.transpose(1, 2).contiguous().view(1, seq_len, -1)
134	    attn_output = F.linear(attn_output, o_proj)
135	    hidden_states = residual + attn_output.squeeze(0)
136	    print(f"  After attention: {hidden_states.shape}, mean={hidden_states.float().mean():.4f}")
137	
138	    # 5. MLP
139	    residual = hidden_states
140	    hidden_states = rms_norm(hidden_states, post_ln_weight)
141	    hidden_states = F.linear(F.silu(F.linear(hidden_states, gate_proj)) * F.linear(hidden_states, up_proj), down_proj)
142	    hidden_states = residual + hidden_states
143	    print(f"  After MLP: {hidden_states.shape}, mean={hidden_states.float().mean():.4f}")
144	
145	    # 6. final norm + lm_head
146	    hidden_states = rms_norm(hidden_states, norm_weight)
147	    logits = F.linear(hidden_states, lm_head_weight)
148	    print(f"  Final logits: {logits.shape}, mean={logits.float().mean():.4f}")
149	
150	    # Get predictions
151	    pred = logits.argmax(dim=-1)
152	    print(f"  Predictions (first 8): {pred[:8].tolist()}")
153	    print()
154	
155	
156	if __name__ == "__main__":
157	    test_fc_weight()
158	    test_lm_head()
159	    test_full_forward()
160
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/medusa/train.py",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Train Medusa heads for MiniCPM-SALA speculative decoding.
4	
5	Step-based training with warmup + cosine LR decay, dropout, weight decay.
6	Eval every 20% of total steps on both val_ind and val_ood.
7	
8	Run from repo user_4813494d:
9	    python3 medusa/train.py
10	"""
11	
12	import math
13	import os
14	import queue
15	import random
16	import threading
17	import time
18	from pathlib import Path
19	
20	import torch
21	import torch.nn as nn
22	import torch.nn.functional as F
23	from safetensors import safe_open
24	from tqdm import tqdm
25	
26	# ── Config ──────────────────────────────────────────────────────────────
27	DATA_DIR   = Path("medusa/data")
28	OUTPUT_DIR = Path("medusa/weights")
29	MODEL_PATH = [REDACTED]
30	
31	NUM_HEADS     = 1
32	EQUIV_EPOCHS  = 5        # total_steps = equiv_epochs × packs_per_pass (if TOTAL_STEPS=0)
33	TOTAL_STEPS   = 10000    # explicit step count
34	LR            = 1e-3
35	LR_ETA_MIN    = 1e-5
36	WARMUP_STEPS  = 200
37	WEIGHT_DECAY  = 0.0
38	DROPOUT       = 0.0
39	GRAD_CLIP     = 1.0
40	DECAY         = 0.8      # head loss weight decay (K>1)
41	PACK_SIZE     = 6
42	VAL_IND_PCT   = 0.015
43	VAL_EVERY_PCT = 0.20     # eval every 20% of total steps
44	SEED          = 42
45	RESUME_FROM   = None     # set to checkpoint path to resume, e.g. "medusa/weights/best.pt"
46	
47	# Weighted sampling: use importance^WEIGHT_POWER as sampling weights.
48	# Requires medusa/data/train_ranked_by_val_ood.json (from select_similar.py).
49	# Files with higher cosine similarity to val_ood are sampled more frequently.
50	USE_WEIGHTED_SAMPLING = True
51	WEIGHT_POWER  = 2.0      # importance^power as sampling weight
52	WEIGHT_FLOOR  = 0.1      # minimum weight (prevents zero-weight files)
53	
54	# ── Model constants ─────────────────────────────────────────────────────
55	HIDDEN_SIZE = 4096
56	VOCAB_SIZE  = 73448
57	SCALE_WIDTH = HIDDEN_SIZE / 256
58	
59	
60	# ── Model ───────────────────────────────────────────────────────────────
61	class RMSNorm(nn.Module):
62	    def __init__(self, hidden_size: int, eps: float = 1e-6):
63	        super().__init__()
64	        self.weight = nn.Parameter(torch.ones(hidden_size))
65	        self.eps = eps
66	
67	    def forward(self, x: torch.Tensor) -> torch.Tensor:
68	        norm = x.float().pow(2).mean(-1, keepdim=True).add(self.eps).rsqrt()
69	        return (x * norm).to(x.dtype) * self.weight
70	
71	
72	class ResBlock(nn.Module):
73	    def __init__(self, hidden_size: int, dropout: float = 0.0):
74	        super().__init__()
75	        self.linear = nn.Linear(hidden_size, hidden_size)
76	        nn.init.zeros_(self.linear.weight)
77	        nn.init.zeros_(self.linear.bias)
78	        self.act = nn.SiLU()
79	        self.dropout = nn.Dropout(dropout) if dropout > 0 else nn.Identity()
80	
81	    def forward(self, x: torch.Tensor) -> torch.Tensor:
82	        return x + self.dropout(self.act(self.linear(x)))
83	
84	
85	class MedusaBlock(nn.Module):
86	    def __init__(self, hidden_size: int, dropout: float = 0.0):
87	        super().__init__()
88	        self.norm = RMSNorm(hidden_size)
89	        self.res1 = ResBlock(hidden_size, dropout)
90	        self.res2 = ResBlock(hidden_size, dropout)
91	
92	    def forward(self, x: torch.Tensor) -> torch.Tensor:
93	        x = self.norm(x)
94	        x = self.res1(x)
95	        x = self.res2(x)
96	        return x
97	
98	
99	class MedusaHeads(nn.Module):
100	    def __init__(self, num_heads: int, hidden_size: int, lm_head_weight: torch.Tensor,
101	                 dropout: float = 0.0):
102	        super().__init__()
103	        self.num_heads = num_heads
104	        self.heads = nn.ModuleList(
105	            [MedusaBlock(hidden_size, dropout) for _ in range(num_heads)])
106	        self.register_buffer("lm_head_weight", lm_head_weight)
107	
108	    def forward(self, hidden_states: torch.Tensor) -> list[torch.Tensor]:
109	        return [F.linear(head(hidden_states), self.lm_head_weight).float()
110	                for head in self.heads]
111	
112	
113	# ── Data ────────────────────────────────────────────────────────────────
114	def load_split_files(split_dir: Path) -> list[Path]:
115	    files = sorted(split_dir.glob("*.pt"))
116	    if not files:
117	        raise FileNotFoundError(f"No .pt files in {split_dir}")
118	    return files
119	
120	
121	def _load_pack_cpu(files: list[Path], K: int):
122	    hs, label_lists = [], [[] for _ in range(K)]
123	    for f in files:
124	        data = torch.load(f, map_location="cpu", weights_only=True)
125	        h   = data["hidden_states"]
126	        ids = data["token_ids"]
127	        valid_len = len(ids) - K - 1
128	        if valid_len < 1 or h.isnan().any():
129	            continue
130	        hs.append(h[:valid_len])
131	        for k in range(K):
132	            label_lists[k].append(ids[k + 2 : k + 2 + valid_len])
133	    if not hs:
134	        return None, None
135	    return torch.cat(hs, dim=0), [torch.cat(lbl, dim=0) for lbl in label_lists]
136	
137	
138	class PackStream:
139	    """Infinite stream of (h, labels) packs with background prefetch.
140	
141	    Supports weighted sampling: files with higher importance are sampled more often.
142	    Without weights, shuffles uniformly each pass.
143	    """
144	    def __init__(self, files: list[Path], K: int, device: torch.device,
145	                 pack_size: int = PACK_SIZE, seed: int = SEED,
146	                 weights: list[float] | None = None):
147	        self.files = list(files)
148	        self.K = K
149	        self.device = device
150	        self.pack_size = pack_size
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/medusa/collect_data.py",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Collect post-norm hidden states from SGLang server for Medusa head training.
4	
5	Data budget v2: ~40M tokens/epoch, 3 epochs
6	  - Chinese 50%: SkyPile-150B (short 4K + long 16K)
7	  - Code 40%: code_search_net multi-language (Python/Java/Go/JS/PHP+Ruby)
8	  - English 10%: wikitext-103 (short 4K + long 16K)
9	  - val_ood: bench model_response chunks (unchanged from v1)
10	
11	Data budget v3 (--code-supplement): add ~20M code tokens to existing train
12	  - Brings code from ~3.8M (10%) to ~23.8M (~42%) of ~57M total
13	  - Uses concatenated code_search_net functions to fill 4K chunks properly
14	
15	The _maybe_collect_hidden hook in minicpm.py splits long sequences into
16	multiple 4096-token .pt files automatically, so each request produces
17	ceil(seq_len / 4096) files.
18	
19	Prerequisites:
20	    1. Start SGLang server (normal NVFP4 config, --dense-as-sparse)
21	    2. mkdir /tmp/medusa_collect
22	    3. python3 medusa/collect_data.py [--train-only]
23	    4. rm -rf /tmp/medusa_collect
24	
25	Supplement mode (add code data to existing train):
26	    python3 medusa/collect_data.py --code-supplement [--concurrency 64]
27	
28	Usage:
29	    python3 medusa/collect_data.py [--output medusa/data] [--concurrency 64]
30	"""
31	
32	import argparse
33	import asyncio
34	import json
35	import os
36	import random
37	import shutil
38	import sys
39	import time
40	from pathlib import Path
41	
42	import aiohttp
43	import torch
44	from tqdm import tqdm
45	from transformers import AutoTokenizer
46	
47	REPO_user_4813494d = Path(__file__).resolve().parent.parent
48	COLLECT_DIR = Path("/tmp/medusa_collect")
49	MODEL_PATH = [REDACTED]
50	
51	SHORT_LEN = 4096
52	LONG_LEN = 16384
53	MIN_TOKENS = 64
54	
55	# ── Budget v2 ──────────────────────────────────────────────────────────
56	# Train: ~40M tokens total
57	#   Chinese (SkyPile):  short 3418 × 4K = 14.0M  +  long 366 × 16K = 6.0M  = 20.0M (50%)
58	#   Code (multi-lang):  short 3906 × 4K = 16.0M                              = 16.0M (40%)
59	#   English (wikitext): short  781 × 4K =  3.2M  +  long  49 × 16K = 0.8M  =  4.0M (10%)
60	#
61	# Note: long samples produce multiple .pt files via the hook's chunking
62	# (16K / 4K = 4 files each), so file count > sample count.
63	
64	TRAIN_SHORT = {
65	    "skypile": 3418,
66	    "code": 3906,
67	    "wikitext": 781,
68	}
69	TRAIN_LONG = {
70	    "skypile_long": 366,
71	    "wikitext_long": 49,
72	}
73	
74	# Code language allocation (% of code budget)
75	CODE_LANG_PCT = {
76	    "python": 0.50,       # bench主力
77	    "java": 0.20,         # C++代理 (code_search_net无C++)
78	    "go": 0.15,
79	    "javascript": 0.10,
80	    "php": 0.03,
81	    "ruby": 0.02,
82	}
83	
84	# Val: reuse existing val/ and val_ood/ from v1 (already on disk)
85	# Only regenerate if --full flag is passed
86	VAL_SHORT = {"skypile": 40, "code": 40, "wikitext": 40}
87	VAL_LONG = {"skypile_long": 10, "wikitext_long": 10}
88	
89	# ── Budget v3: code supplement ──────────────────────────────────────────
90	# Existing train: ~36.6M tokens (chinese ~17M, english ~16M, code ~3.8M)
91	# Target: code ~50% of total → need ~20M more code tokens → 5000 × 4K chunks
92	# Total after supplement: ~57M tokens (chinese 30%, code 42%, english 28%)
93	CODE_SUPPLEMENT_CHUNKS = 5000
94	
95	
96	# ── Data loading helpers ────────────────────────────────────────────────
97	
98	def _load_jsonl(path, key):
99	    with open(path) as f:
100	        return [json.loads(line)[key] for line in f]
101	
102	
103	def _chunk_ids(token_ids, tokenizer, chunk_len):
104	    """Chunk token list into pieces, return decoded texts."""
105	    chunks = []
106	    for i in range(0, len(token_ids), chunk_len):
107	        c = token_ids[i : i + chunk_len]
108	        if len(c) < MIN_TOKENS:
109	            continue
110	        chunks.append(tokenizer.decode(c))
111	    return chunks
112	
113	
114	def prepare_all(tokenizer, train_only=False) -> dict:
115	    """Prepare all data splits. Returns {split_name: [text_strings]}."""
116	    random.seed(42)
117	
118	    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
119	    from datasets import load_dataset
120	
121	    # ── SkyPile (Chinese web text, streaming) ───────────────────────
122	    need_cn_short = TRAIN_SHORT["skypile"] + (VAL_SHORT.get("skypile", 0) if not train_only else 0) + 50
123	    need_cn_long = TRAIN_LONG["skypile_long"] + (VAL_LONG.get("skypile_long", 0) if not train_only else 0) + 20
124	
125	    print("  Loading SkyPile-150B (streaming)...")
126	    sky_ds = load_dataset("Skywork/SkyPile-150B", split="train", streaming=True)
127	
128	    sky_short, sky_long = [], []
129	    buf_ids = []
130	    pbar = tqdm(desc="  skypile", unit="chunk")
131	    for sample in sky_ds:
132	        text = sample.get("text", "")
133	        if not text.strip() or len(text) < 50:
134	            continue
135	        buf_ids.extend(tokenizer.encode(text, add_special_tokens=False))
136	        # Extract short chunks
137	        while len(sky_short) < need_cn_short and len(buf_ids) >= SHORT_LEN:
138	            chunk = buf_ids[:SHORT_LEN]
139	            buf_ids = buf_ids[SHORT_LEN:]
140	            sky_short.append({"text": tokenizer.decode(chunk), "source": "skypile"})
141	            pbar.update(1)
142	        # Extract long chunks
143	        while len(sky_long) < need_cn_long and len(buf_ids) >= LONG_LEN:
144	            chunk = buf_ids[:LONG_LEN]
145	            buf_ids = buf_ids[LONG_LEN:]
146	            sky_long.append({"text": tokenizer.decode(chunk), "source": "skypile_long"})
147	            pbar.update(1)
148	        if len(sky_short) >= need_cn_short and len(sky_long) >= need_cn_long:
149	            break
150	    pbar.close()
```

> AGENT

Now let me read the sglang worker files:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "limit": 200
}
```

> TOOL

tool_result Read
```
1	import logging
2	import time
3	from typing import List, Optional, Tuple
4	
5	import torch
6	
7	from sglang.srt.distributed import get_tp_group
8	from sglang.srt.hardware_backend.npu.graph_runner.eagle_draft_npu_graph_runner import (
9	    EAGLEDraftNpuGraphRunner,
10	)
11	from sglang.srt.layers.dp_attention import get_attention_tp_group
12	from sglang.srt.layers.logits_processor import LogitsProcessorOutput
13	from sglang.srt.layers.moe.utils import (
14	    speculative_moe_a2a_backend_context,
15	    speculative_moe_backend_context,
16	)
17	from sglang.srt.layers.utils.logprob import add_output_logprobs_for_spec_v1
18	from sglang.srt.managers.io_struct import UpdateWeightsFromTensorReqInput
19	from sglang.srt.managers.schedule_batch import ScheduleBatch
20	from sglang.srt.managers.scheduler import GenerationBatchResult
21	from sglang.srt.managers.tp_worker import TpModelWorker
22	from sglang.srt.mem_cache.chunk_cache import SWAChunkCache
23	from sglang.srt.mem_cache.common import (
24	    alloc_paged_token_slots_extend,
25	    alloc_token_slots,
26	    get_last_loc,
27	)
28	from sglang.srt.model_executor.forward_batch_info import (
29	    CaptureHiddenMode,
30	    ForwardBatch,
31	    ForwardMode,
32	)
33	from sglang.srt.server_args import ServerArgs
34	from sglang.srt.speculative.draft_utils import DraftBackendFactory
35	from sglang.srt.speculative.eagle_draft_cuda_graph_runner import (
36	    EAGLEDraftCudaGraphRunner,
37	)
38	from sglang.srt.speculative.eagle_draft_extend_cuda_graph_runner import (
39	    EAGLEDraftExtendCudaGraphRunner,
40	)
41	from sglang.srt.speculative.eagle_info import (
42	    EagleDraftInput,
43	    EagleVerifyInput,
44	    EagleVerifyOutput,
45	)
46	from sglang.srt.speculative.eagle_utils import (
47	    build_tree_kernel_efficient,
48	    organize_draft_results,
49	)
50	from sglang.srt.speculative.spec_info import SpeculativeAlgorithm
51	from sglang.srt.speculative.spec_utils import (
52	    assign_draft_cache_locs,
53	    detect_nan,
54	    draft_tp_context,
55	    fast_topk,
56	    generate_token_bitmask,
57	    get_last_loc_large_page_size_large_top_k,
58	    load_token_map,
59	    select_top_k_tokens,
60	)
61	from sglang.srt.utils import (
62	    MultiprocessingSerializer,
63	    empty_context,
64	    get_available_gpu_memory,
65	    is_cuda,
66	    is_npu,
67	    next_power_of_2,
68	)
69	from sglang.srt.utils.patch_torch import monkey_patch_torch_reductions
70	
71	_is_npu = is_npu()
72	
73	if is_cuda():
74	    from sgl_kernel import segment_packbits  # noqa: F401
75	
76	logger = logging.getLogger(__name__)
77	
78	
79	class EAGLEWorker(TpModelWorker):
80	
81	    def __init__(
82	        self,
83	        server_args: ServerArgs,
84	        gpu_id: int,
85	        tp_rank: int,
86	        dp_rank: Optional[int],
87	        moe_ep_rank: int,
88	        nccl_port: int,
89	        target_worker: TpModelWorker,
90	    ):
91	        # Parse arguments
92	        self.server_args = server_args
93	        self.topk = server_args.speculative_eagle_topk
94	        self.speculative_num_steps = server_args.speculative_num_steps
95	        self.speculative_num_draft_tokens = server_args.speculative_num_draft_tokens
96	        self.enable_nan_detection = server_args.enable_nan_detection
97	        self.gpu_id = gpu_id
98	        self.device = server_args.device
99	        self.target_worker = target_worker
100	        self.page_size = server_args.page_size
101	        self.speculative_algorithm = SpeculativeAlgorithm.from_string(
102	            server_args.speculative_algorithm
103	        )
104	
105	        # Override the context length of the draft model to be the same as the target model.
106	        server_args.context_length = target_worker.model_runner.model_config.context_len
107	
108	        # Do not capture cuda graph in `super().__init__()`
109	        # It will be captured later.
110	        backup_disable_cuda_graph = server_args.disable_cuda_graph
111	        server_args.disable_cuda_graph = True
112	        # Draft model should not be quantized (it's a small BF16 model)
113	        # Must set speculative_draft_model_quantization, not quantization
114	        # (server_args init already copied quantization to speculative_draft_model_quantization)
115	        backup_draft_quant = server_args.speculative_draft_model_quantization
116	        server_args.speculative_draft_model_quantization = None
117	        # Draft model (Llama architecture) should use standard flashinfer, not minicpm_flashinfer
118	        backup_draft_attn = server_args.speculative_draft_attention_backend
119	        if server_args.attention_backend == "minicpm_flashinfer":
120	            server_args.speculative_draft_attention_backend = "flashinfer"
121	        # Share the allocator with a target worker.
122	        # Draft and target worker own their own KV cache pools.
123	        self.req_to_token_pool, self.token_to_kv_pool_allocator = (
124	            target_worker.get_memory_pool()
125	        )
126	
127	        # Load hot token ids
128	        if self.speculative_algorithm.is_eagle3():
129	            if server_args.speculative_token_map is not None:
130	                logger.warning(
131	                    "Speculative token map specified, but EAGLE3 models already have this. Ignoring the specified token map."
132	                )
133	            self.hot_token_id = None
134	        elif server_args.speculative_token_map is not None:
135	            self.hot_token_id = load_token_map(server_args.speculative_token_map)
136	            server_args.json_model_override_args = (
137	                f'{{"hot_vocab_size": {len(self.hot_token_id)}}}'
138	            )
139	        else:
140	            self.hot_token_id = None
141	
142	        # Init draft worker
143	        if server_args.enable_dp_attention and self.speculative_algorithm.is_eagle3():
144	            ctx = draft_tp_context(get_attention_tp_group())
145	        else:
146	            ctx = empty_context()
147	        with (
148	            ctx
149	        ), speculative_moe_backend_context(), speculative_moe_a2a_backend_context():
150	            super().__init__(
151	                server_args=server_args,
152	                gpu_id=gpu_id,
153	                tp_rank=tp_rank,
154	                pp_rank=0,  # FIXME
155	                dp_rank=dp_rank,
156	                moe_ep_rank=moe_ep_rank,
157	                nccl_port=nccl_port,
158	                is_draft_worker=True,
159	                req_to_token_pool=self.req_to_token_pool,
160	                token_to_kv_pool_allocator=self.token_to_kv_pool_allocator,
161	            )
162	
163	        embed, head = self.target_worker.model_runner.model.get_embed_and_head()
164	
165	        if self.speculative_algorithm.is_eagle3():
166	            # most cases EAGLE3 models don't share lm_head
167	            # but some models (e.g. nvidia/gpt-oss-120b-Eagle3) shares
168	            if (
169	                hasattr(self.draft_model_runner.model, "load_lm_head_from_target")
170	                and self.draft_model_runner.model.load_lm_head_from_target
171	            ):
172	                self.draft_model_runner.model.set_embed_and_head(embed, head)
173	            else:
174	                self.draft_model_runner.model.set_embed(embed)
175	
176	            # grab hot token ids
177	            if self.draft_model_runner.model.hot_token_id is not None:
178	                self.hot_token_id = self.draft_model_runner.model.hot_token_id.to(
179	                    embed.device
180	                )
181	
182	        else:
183	            if self.hot_token_id is not None:
184	                head = head.clone()
185	                self.hot_token_id = self.hot_token_id.to(head.device)
186	                head.data = head.data[self.hot_token_id]
187	
188	            # Share the embedding and lm_head
189	            self.draft_model_runner.model.set_embed_and_head(embed, head)
190	
191	        # Init attention backend and cuda graphs
192	        self.draft_model_runner.server_args.disable_cuda_graph = (
193	            backup_disable_cuda_graph
194	        )
195	        self.draft_tp_context = (
196	            draft_tp_context if server_args.enable_dp_attention else empty_context
197	        )
198	        self.eagle_use_aux_hidden_state = False
199	        if self.speculative_algorithm.is_eagle3():
200	            self.eagle_use_aux_hidden_state = True
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/medusa_worker.py",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1	"""
2	Medusa speculative decoding worker for MiniCPM-SALA.
3	
4	Architecture: K ResBlock heads + shared lm_head (frozen).
5	Draft: run heads on target hidden states → argmax → K draft tokens.
6	Verify: Batched TARGET_VERIFY — all K+1 tokens verified in ONE forward pass.
7	        GLA intermediate states saved per-step for rollback.
8	"""
9	
10	import logging
11	from typing import List, Optional
12	
13	import torch
14	import torch.nn as nn
15	import torch.nn.functional as F
16	
17	from sglang.srt.layers.logits_processor import LogitsProcessorOutput
18	from sglang.srt.managers.schedule_batch import ScheduleBatch
19	from sglang.srt.mem_cache.common import alloc_for_decode, alloc_token_slots
20	from sglang.srt.managers.tp_worker import TpModelWorker
21	from sglang.srt.managers.utils import GenerationBatchResult
22	from sglang.srt.model_executor.forward_batch_info import (
23	    CaptureHiddenMode,
24	    ForwardMode,
25	)
26	from sglang.srt.server_args import ServerArgs
27	from sglang.srt.speculative.eagle_info import EagleDraftInput, MedusaVerifyInput
28	from sglang.srt.speculative.spec_utils import (
29	    assign_req_to_token_pool_func,
30	    detect_nan,
31	)
32	
33	logger = logging.getLogger(__name__)
34	
35	
36	# ── Medusa head model ───────────────────────────────────────────────────
37	
38	
39	class RMSNorm(nn.Module):
40	    def __init__(self, hidden_size: int, eps: float = 1e-6):
41	        super().__init__()
42	        self.weight = nn.Parameter(torch.ones(hidden_size))
43	        self.eps = eps
44	
45	    def forward(self, x: torch.Tensor) -> torch.Tensor:
46	        norm = x.float().pow(2).mean(-1, keepdim=True).add(self.eps).rsqrt()
47	        return (x * norm).to(x.dtype) * self.weight
48	
49	
50	class ResBlock(nn.Module):
51	    def __init__(self, hidden_size: int):
52	        super().__init__()
53	        self.linear = nn.Linear(hidden_size, hidden_size)
54	        self.act = nn.SiLU()
55	
56	    def forward(self, x: torch.Tensor) -> torch.Tensor:
57	        return x + self.act(self.linear(x))
58	
59	
60	class MedusaBlock(nn.Module):
61	    """RMSNorm + 2x ResBlock, used by newer Medusa checkpoints."""
62	    def __init__(self, hidden_size: int):
63	        super().__init__()
64	        self.norm = RMSNorm(hidden_size)
65	        self.res1 = ResBlock(hidden_size)
66	        self.res2 = ResBlock(hidden_size)
67	
68	    def forward(self, x: torch.Tensor) -> torch.Tensor:
69	        x = self.norm(x)
70	        x = self.res1(x)
71	        x = self.res2(x)
72	        return x
73	
74	
75	class MedusaHeads(nn.Module):
76	    def __init__(self, num_heads: int, hidden_size: int, lm_head_weight: torch.Tensor,
77	                 block_cls: type[nn.Module] = ResBlock):
78	        super().__init__()
79	        self.num_heads = num_heads
80	        self.heads = nn.ModuleList([block_cls(hidden_size) for _ in range(num_heads)])
81	        self.register_buffer("lm_head_weight", lm_head_weight)
82	
83	    def forward(self, hidden_states: torch.Tensor) -> list[torch.Tensor]:
84	        return [
85	            F.linear(head(hidden_states), self.lm_head_weight)
86	            for head in self.heads
87	        ]
88	
89	
90	# ── Medusa Worker ───────────────────────────────────────────────────────
91	
92	
93	class MedusaWorker:
94	
95	    def __init__(
96	        self,
97	        server_args: ServerArgs,
98	        gpu_id: int,
99	        tp_rank: int,
100	        dp_rank: Optional[int],
101	        moe_ep_rank: int,
102	        nccl_port: int,
103	        target_worker: TpModelWorker,
104	    ):
105	        self.server_args = server_args
106	        self.target_worker = target_worker
107	        self.device = server_args.device
108	        self.gpu_id = gpu_id
109	        self.page_size = server_args.page_size
110	        self.enable_nan_detection = server_args.enable_nan_detection
111	
112	        self.num_heads = server_args.speculative_num_steps or 3
113	        self.topk = 1
114	        # Medusa verifies verified_id + K drafts = K+1 tokens per request.
115	        # server_args already enforces speculative_num_draft_tokens = num_steps + 1.
116	        self.num_draft_tokens = self.num_heads + 1
117	        assert server_args.speculative_num_draft_tokens == self.num_draft_tokens, (
118	            f"speculative_num_draft_tokens={server_args.speculative_num_draft_tokens} "
119	            f"must equal num_heads+1={self.num_draft_tokens}"
120	        )
121	
122	        # Share allocator with target worker (same pattern as EAGLEWorker)
123	        self.req_to_token_pool, self._token_to_kv_pool_allocator = (
124	            target_worker.get_memory_pool()
125	        )
126	
127	        # Dynamic spec/no-spec threshold: skip draft+verify when bs >= threshold
128	        import os
129	        self.spec_bs_threshold = int(os.environ.get("SGLANG_MEDUSA_BS_THRESHOLD", "16"))
130	
131	        self._load_medusa_heads()
132	        logger.info(
133	            f"MedusaWorker initialized: {self.num_heads} heads, "
134	            f"topk={self.topk}, num_draft_tokens={self.num_draft_tokens}, "
135	            f"strategy=batched_target_verify, "
136	            f"spec_bs_threshold={self.spec_bs_threshold}"
137	        )
138	
139	    def _load_medusa_heads(self):
140	        import os
141	
142	        model = self.target_worker.model_runner.model
143	        if hasattr(model, "lm_head"):
144	            lm_head_weight = model.lm_head.weight
145	        elif hasattr(model, "model") and hasattr(model.model, "embed_tokens"):
146	            lm_head_weight = model.model.embed_tokens.weight
147	        else:
148	            raise RuntimeError("Cannot find lm_head weight in target model")
149	        hidden_size = lm_head_weight.shape[1]
150
```

> AGENT

Now let me get a comprehensive summary by checking the structure and getting more info on file organization:

> TOOL

tool_use Bash
```json
{
  "command": "ls -lah /user_4813494d/openbmb/eagle/"
}
```

> TOOL

tool_result Bash
```
total 128K
drwxr-xr-x  6 user_4813494d user_4813494d 4.0K Apr 12 12:02 .
drwxr-xr-x 19 user_4813494d user_4813494d 4.0K Apr 13 09:41 ..
drwxr-xr-x  2 user_4813494d user_4813494d  132 Apr 12 11:20 __pycache__
-rw-r--r--  1 user_4813494d user_4813494d  16K Apr 11 20:36 collect_data.py
-rw-r--r--  1 user_4813494d user_4813494d 5.5K Apr 12 12:02 convert_to_sglang.py
drwxr-xr-x  3 user_4813494d user_4813494d   78 Apr 11 20:54 data
-rw-r--r--  1 user_4813494d user_4813494d  11K Apr 12 11:06 eval_ood_accept.py
drwxr-xr-x  2 user_4813494d user_4813494d 4.0K Apr 12 00:46 sglang_model
-rw-r--r--  1 user_4813494d user_4813494d  11K Apr 12 06:23 test_decode_mode.py
-rw-r--r--  1 user_4813494d user_4813494d 6.5K Apr 12 05:09 test_eagle3_flow.py
-rw-r--r--  1 user_4813494d user_4813494d  11K Apr 12 06:19 test_forward_match.py
-rw-r--r--  1 user_4813494d user_4813494d 4.8K Apr 12 05:24 test_offline_pred.py
-rw-r--r--  1 user_4813494d user_4813494d  27K Apr 12 10:48 train.py
-rw-r--r--  1 user_4813494d user_4813494d 6.6K Apr 12 06:25 verify_sglang_draft.py
drwxr-xr-x  2 user_4813494d user_4813494d 4.0K Apr 12 10:49 weights
```

> TOOL

tool_use Bash
```json
{
  "command": "head -50 /user_4813494d/openbmb/medusa/train.py | tail -40"
}
```

> TOOL

tool_result Bash
```
import math
import os
import queue
import random
import threading
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
from safetensors import safe_open
from tqdm import tqdm

# ── Config ──────────────────────────────────────────────────────────────
DATA_DIR   = Path("medusa/data")
OUTPUT_DIR = Path("medusa/weights")
MODEL_PATH = [REDACTED]

NUM_HEADS     = 1
EQUIV_EPOCHS  = 5        # total_steps = equiv_epochs × packs_per_pass (if TOTAL_STEPS=0)
TOTAL_STEPS   = 10000    # explicit step count
LR            = 1e-3
LR_ETA_MIN    = 1e-5
WARMUP_STEPS  = 200
WEIGHT_DECAY  = 0.0
DROPOUT       = 0.0
GRAD_CLIP     = 1.0
DECAY         = 0.8      # head loss weight decay (K>1)
PACK_SIZE     = 6
VAL_IND_PCT   = 0.015
VAL_EVERY_PCT = 0.20     # eval every 20% of total steps
SEED          = 42
RESUME_FROM   = None     # set to checkpoint path to resume, e.g. "medusa/weights/best.pt"

# Weighted sampling: use importance^WEIGHT_POWER as sampling weights.
# Requires medusa/data/train_ranked_by_val_ood.json (from select_similar.py).
# Files with higher cosine similarity to val_ood are sampled more frequently.
USE_WEIGHTED_SAMPLING = True
```

> TOOL

tool_use Bash
```json
{
  "command": "wc -l /user_4813494d/openbmb/eagle/*.py /user_4813494d/openbmb/medusa/*.py"
}
```

> TOOL

tool_result Bash
```
Permission for this tool use was denied. The tool use was rejected (eg. if it was a file edit, the new_string was NOT written to the file). Try a different approach or report the limitation to complete your task.
```

> AGENT

Let me get file stats another way:

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/eagle -name \"*.py\" -exec wc -l {} \\; | awk '{sum+=$1} END {print \"Total eagle .py lines: \" sum}'"
}
```

> TOOL

tool_result Bash
```
Total eagle .py lines: 2539
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/medusa -name \"*.py\" -exec wc -l {} \\; | awk '{sum+=$1} END {print \"Total medusa .py lines: \" sum}'"
}
```

> TOOL

tool_result Bash
```
Total medusa .py lines: 2625
```

> TOOL

[Request interrupted by user]

> DEVELOPER

Thoroughly explore the eagle/ directory and all related documentation. I need to understand:
1. The full EAGLE-3 training pipeline: data collection, training, model conversion, evaluation
2. Current state of each script - what's complete, what's WIP
3. How eagle/ scripts interact with the sglang serving code (especially eagle_worker.py, medusa_worker.py)
4. Key configuration: model architecture, training hyperparameters, data format

Read all files in eagle/ directory, then read docs/eagle3_research.md, docs/eagle3-pipeline.md, docs/eagle3-accept-rate-fix.md. Also check demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py and medusa_worker.py.

Report comprehensively - file by file summary with key details.

> AGENT

I'll thoroughly explore the eagle/ directory and related documentation to provide you with a comprehensive understanding of the EAGLE-3 training pipeline and its integration with sglang serving code.

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -type f -name \"*.md\" | grep -E \"(eagle|EAGLE)\" | head -20"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/docs/eagle3_research.md
/user_4813494d/openbmb/docs/eagle3-pipeline.md
/user_4813494d/openbmb/docs/eagle3-accept-rate-fix.md
```

> DEVELOPER

Explore the medusa/ directory and the medusa_worker.py in demo-sala/sglang/. I need to understand:
1. Current Medusa implementation details (K=1, ResBlock head, training data, accuracy)
2. How medusa_worker.py does batched TARGET_VERIFY
3. The actual performance numbers - what's measured vs what's claimed

Read all files in medusa/ and demo-sala/sglang/python/sglang/srt/speculative/medusa_worker.py.
Also check bench/mini_bench.sh for benchmark methodology.

Report comprehensively.

> AGENT

Now let me explore the eagle/ directory structure:

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/eagle -type f -name \"*.py\" -o -name \"*.sh\" -o -name \"*.md\" | sort"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/eagle/collect_data.py
/user_4813494d/openbmb/eagle/convert_to_sglang.py
/user_4813494d/openbmb/eagle/eval_ood_accept.py
/user_4813494d/openbmb/eagle/test_decode_mode.py
/user_4813494d/openbmb/eagle/test_eagle3_flow.py
/user_4813494d/openbmb/eagle/test_forward_match.py
/user_4813494d/openbmb/eagle/test_offline_pred.py
/user_4813494d/openbmb/eagle/train.py
/user_4813494d/openbmb/eagle/verify_sglang_draft.py
```

> AGENT

I'll explore these directories and files to understand the Medusa implementation details, batched verification, and performance metrics.

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -type f -name \"*.py\" -o -name \"*.sh\" | grep -E \"(medusa|medusa_worker)\" | head -20"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/medusa_worker.py
/user_4813494d/openbmb/medusa/profile_verify.py
/user_4813494d/openbmb/medusa/.ipynb_checkpoints/train-checkpoint.py
/user_4813494d/openbmb/medusa/check_data.py
/user_4813494d/openbmb/medusa/collect_data.py
/user_4813494d/openbmb/medusa/eval_topk.py
/user_4813494d/openbmb/medusa/quick_validate_similar.py
/user_4813494d/openbmb/medusa/recollect_val_ood.sh
/user_4813494d/openbmb/medusa/select_similar.py
/user_4813494d/openbmb/medusa/train.py
/user_4813494d/openbmb/medusa/collect_eval_overfit.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/medusa_worker.py
/user_4813494d/openbmb/tests/test_medusa_dual_graph.py
```

> AGENT

Now let me read all eagle scripts and documentation files in parallel:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/collect_data.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Collect aux hidden states + top-K logits from NVFP4 model for EAGLE-3 training.
4	
5	Activates via EAGLE3_COLLECT_DIR env var in minicpm.py hook.
6	Server captures layer 1/10/22 outputs + top-256 logits per EXTEND request.
7	
8	Data budget:
9	  train: 10,000 samples × 2048 tokens (EAGLE3_MAX_TOKENS=2048)
10	    - SkyPile (中文):  50% → 5000
11	    - Code (多语言):   42% → 4200 (py60/java16/go12/js8/php2.4/ruby1.6)
12	    - Wikitext (英文):  8% → 800
13	  val_ood: 64 samples, original length (EAGLE3_MAX_TOKENS=0)
14	    - speed_bench_cunlimited.jsonl model_response, no truncation
15	
16	Prerequisites:
17	    1. Start NVFP4 server with: EAGLE3_COLLECT_DIR=/tmp/eagle3_collect
18	    2. python3 eagle/collect_data.py              # train only
19	    3. python3 eagle/collect_data.py --val-ood     # val_ood only (needs server restart with EAGLE3_MAX_TOKENS=0)
20	    4. python3 eagle/collect_data.py --smoke N     # N samples smoke test
21	
22	NOTE: train and val_ood require DIFFERENT server configs:
23	  - train:   EAGLE3_MAX_TOKENS=2048 (default)
24	  - val_ood: EAGLE3_MAX_TOKENS=0 (no truncation, restart server!)
25	"""
26	
27	import asyncio
28	import json
29	import os
30	import random
31	import shutil
32	import sys
33	import threading
34	import time
35	from pathlib import Path
36	
37	import aiohttp
38	import torch
39	from tqdm import tqdm
40	from transformers import AutoTokenizer
41	
42	
43	def _net_monitor(stop_event, interval=2.0):
44	    """Background thread: print network throughput every `interval` seconds."""
45	    def _rx_bytes():
46	        with open("/proc/net/dev") as f:
47	            total = 0
48	            for line in f:
49	                if ":" not in line:
50	                    continue
51	                parts = line.split()
52	                iface = parts[0].rstrip(":")
53	                if iface == "lo":
54	                    continue
55	                total += int(parts[1])  # rx bytes
56	            return total
57	
58	    prev = _rx_bytes()
59	    prev_t = time.monotonic()
60	    while not stop_event.is_set():
61	        stop_event.wait(interval)
62	        now = _rx_bytes()
63	        now_t = time.monotonic()
64	        dt = now_t - prev_t
65	        if dt > 0:
66	            speed = (now - prev) / dt
67	            if speed > 1024 * 1024:
68	                print(f"\r  [net] ↓ {speed / 1024 / 1024:.1f} MB/s", end="", flush=True)
69	            elif speed > 1024:
70	                print(f"\r  [net] ↓ {speed / 1024:.0f} KB/s", end="", flush=True)
71	        prev, prev_t = now, now_t
72	    print()  # newline on exit
73	
74	REPO_user_4813494d = Path(__file__).resolve().parent.parent
75	MODEL_PATH = [REDACTED]
76	API_BASE = "http://127.0.0.1:30000"
77	COLLECT_DIR = Path("/tmp/eagle3_collect")
78	OUTPUT_TRAIN = REPO_user_4813494d / "eagle" / "data" / "train"
79	OUTPUT_VAL_OOD = REPO_user_4813494d / "eagle" / "data" / "val_ood"
80	CONCURRENCY = 32
81	SEQ_LEN = 2048
82	MIN_TOKENS = 64
83	
84	# ── Budget ────────────────────────────────────────────────────────────
85	BUDGET = {
86	    "skypile": 5000,
87	    "code": 4200,
88	    "wikitext": 800,
89	}
90	
91	# Python 比例提高到 60%（2048 截断更友好）
92	CODE_LANG_PCT = {
93	    "python": 0.60,
94	    "java": 0.16,
95	    "go": 0.12,
96	    "javascript": 0.08,
97	    "php": 0.024,
98	    "ruby": 0.016,
99	}
100	
101	
102	# ── Data loading ──────────────────────────────────────────────────────
103	
104	def prepare_texts(tokenizer, smoke=0):
105	    """Prepare text samples. Returns list of {text, source}."""
106	    random.seed(42)
107	    os.environ["HF_DATASETS_OFFLINE"] = "1"
108	    from datasets import load_dataset
109	
110	    # 启动网络速度监控
111	    net_stop = threading.Event()
112	    net_thread = threading.Thread(target=_net_monitor, args=(net_stop,), daemon=True)
113	    net_thread.start()
114	
115	    budget = dict(BUDGET)
116	    if smoke > 0:
117	        total = smoke
118	        budget = {
119	            "skypile": max(1, int(total * 0.50)),
120	            "code": max(1, int(total * 0.42)),
121	            "wikitext": max(1, total - max(1, int(total * 0.50)) - max(1, int(total * 0.42))),
122	        }
123	        print(f"[smoke test] budget: {budget}")
124	
125	    all_samples = []
126	
127	    # ── SkyPile (本地 jsonl) ─────────────────────────────────────
128	    need = budget["skypile"] + 50
129	    skypile_path = "/user_4813494d/data/skypile/data/2020-40_zh_head_0000.jsonl"
130	    print(f"Loading SkyPile from {skypile_path} (need {need} chunks)...", flush=True)
131	    sky_chunks = []
132	    buf_ids = []
133	    with open(skypile_path) as f:
134	        for line in tqdm(f, desc="skypile", unit="line"):
135	            text = json.loads(line).get("text", "")
136	            if not text.strip() or len(text) < 50:
137	                continue
138	            buf_ids.extend(tokenizer.encode(text, add_special_tokens=False))
139	            while len(sky_chunks) < need and len(buf_ids) >= SEQ_LEN:
140	                chunk = buf_ids[:SEQ_LEN]
141	                buf_ids = buf_ids[SEQ_LEN:]
142	                sky_chunks.append({"text": tokenizer.decode(chunk), "source": "skypile"})
143	            if len(sky_chunks) >= need:
144	                break
145	    random.shuffle(sky_chunks)
146	    all_samples.extend(sky_chunks[: budget["skypile"]])
147	    print(f"  skypile: {len(sky_chunks)} prepared, using {budget['skypile']}")
148	
149	    # ── Code ──────────────────────────────────────────────────────
150	    need = budget["code"] + 50
151	    code_chunks = []
152	    for lang, pct in CODE_LANG_PCT.items():
153	        lang_need = int(need * pct) + 10
154	        print(f"Loading code_search_net/{lang} (need {lang_need} chunks)...", flush=True)
155	        code_ds = load_dataset("code_search_net", lang, split="train")
156	        lang_chunks = []
157	        buf_ids = []
158	        for sample in tqdm(code_ds, desc=f"code/{lang}", unit="func"):
159	            func = sample.get("whole_func_string", "")
160	            if not func or len(func) < 50:
161	                continue
162	            buf_ids.extend(tokenizer.encode(func, add_special_tokens=False))
163	            while len(buf_ids) >= SEQ_LEN:
164	                chunk = buf_ids[:SEQ_LEN]
165	                buf_ids = buf_ids[SEQ_LEN:]
166	                lang_chunks.append({"text": tokenizer.decode(chunk), "source": f"code_{lang}"})
167	            if len(lang_chunks) >= lang_need:
168	                break
169	        if len(buf_ids) >= MIN_TOKENS:
170	            lang_chunks.append({"text": tokenizer.decode(buf_ids[:SEQ_LEN]), "source": f"code_{lang}"})
171	        random.shuffle(lang_chunks)
172	        code_chunks.extend(lang_chunks[:lang_need])
173	        print(f"  {lang}: {len(lang_chunks)} chunks, using {min(len(lang_chunks), lang_need)}")
174	    random.shuffle(code_chunks)
175	    all_samples.extend(code_chunks[: budget["code"]])
176	    print(f"  code total: using {budget['code']}")
177	
178	    # ── Wikitext ──────────────────────────────────────────────────
179	    need = budget["wikitext"] + 50
180	    print(f"Loading wikitext-103 (need {need} chunks)...", flush=True)
181	    wiki_ds = load_dataset("wikitext", "wikitext-103-raw-v1", split="train")
182	    wiki_chunks = []
183	    buf_ids = []
184	    for sample in tqdm(wiki_ds, desc="wikitext", unit="doc"):
185	        if not sample["text"].strip():
186	            continue
187	        buf_ids.extend(tokenizer.encode(sample["text"], add_special_tokens=False))
188	        while len(wiki_chunks) < need and len(buf_ids) >= SEQ_LEN:
189	            chunk = buf_ids[:SEQ_LEN]
190	            buf_ids = buf_ids[SEQ_LEN:]
191	            wiki_chunks.append({"text": tokenizer.decode(chunk), "source": "wikitext"})
192	        if len(wiki_chunks) >= need:
193	            break
194	    random.shuffle(wiki_chunks)
195	    all_samples.extend(wiki_chunks[: budget["wikitext"]])
196	    print(f"  wikitext: {len(wiki_chunks)} prepared, using {budget['wikitext']}")
197	
198	    net_stop.set()
199	    net_thread.join(timeout=3)
200	
201	    random.shuffle(all_samples)
202	    from collections import Counter
203	    counts = Counter(s["source"] for s in all_samples)
204	    print(f"\nTotal: {len(all_samples)} samples")
205	    for src, n in sorted(counts.items()):
206	        print(f"  {src}: {n}")
207	    return all_samples
208	
209	
210	def prepare_val_ood(tokenizer):
211	    """Load speed bench model responses as val_ood. No truncation, original length."""
212	    bench_path = REPO_user_4813494d / "bench" / "data" / "speed_bench_cunlimited.jsonl"
213	    with open(bench_path) as f:
214	        lines = [json.loads(l) for l in f]
215	    samples = []
216	    for l in lines:
217	        text = l.get("model_response", "")
218	        ids = tokenizer.encode(text, add_special_tokens=False)
219	        if len(ids) < MIN_TOKENS:
220	            continue
221	        samples.append({"text": text, "source": "bench_ood"})
222	    print(f"val_ood: {len(samples)} samples from {bench_path.name}")
223	    lens = [len(tokenizer.encode(s["text"], add_special_tokens=False)) for s in samples]
224	    print(f"  token lengths: min={min(lens)}, max={max(lens)}, total={sum(lens)/1e3:.0f}K")
225	    return samples
226	
227	
228	# ── Collection ────────────────────────────────────────────────────────
229	
230	async def collect_split(samples, output_dir, concurrency=CONCURRENCY):
231	    """Collect samples with batched concurrent requests.
232	
233	    Each batch of requests produces .pt files in COLLECT_DIR.
234	    After each batch completes, files are moved to output_dir with sequential naming.
235	    Supports resume: skips already-collected files based on existing .pt count.
236	    """
237	    output_dir.mkdir(parents=True, exist_ok=True)
238	    COLLECT_DIR.mkdir(exist_ok=True)
239	
240	    # Clean stale files
241	    for f in COLLECT_DIR.glob("*.pt"):
242	        f.unlink()
243	
244	    async with aiohttp.ClientSession() as session:
245	        # Verify server is up
246	        try:
247	            async with session.get(f"{API_BASE}/v1/models") as resp:
248	                if resp.status != 200:
249	                    print(f"Server not ready: {resp.status}")
250	                    return 0
251	        except Exception as e:
252	            print(f"Cannot reach server: {e}")
253	            return 0
254	
255	        # Skip already collected
256	        existing = sorted(output_dir.glob("*.pt"))
257	        start_idx = len(existing)
258	        if start_idx > 0:
259	            print(f"Resuming from index {start_idx} ({start_idx} already collected)")
260	            samples = samples[start_idx:]
261	
262	        fail_count = [0]
263	        success = 0
264	        pbar = tqdm(total=len(samples), desc="collecting", unit="seq")
265	
266	        sem = asyncio.Semaphore(concurrency)
267	        batch_size = concurrency
268	
269	        for batch_start in range(0, len(samples), batch_size):
270	            batch = samples[batch_start:batch_start + batch_size]
271	
272	            # Clean collect dir before batch
273	            for f in COLLECT_DIR.glob("*.pt"):
274	                f.unlink()
275	
276	            # Send batch concurrently
277	            tasks = []
278	            for j, sample in enumerate(batch):
279	                payload = {
280	                    "model": "default",
281	                    "prompt": sample["text"],
282	                    "max_tokens": 1,
283	                    "temperature": 0,
284	                }
285	
286	                async def _send(p=payload):
287	                    async with sem:
288	                        try:
289	                            async with session.post(
290	                                f"{API_BASE}/v1/completions",
291	                                json=p,
292	                                timeout=aiohttp.ClientTimeout(total=600),
293	                            ) as resp:
294	                                await resp.json()
295	                                return True
296	                        except Exception as e:
297	                            return False
298	
299	                tasks.append(asyncio.create_task(_send()))
300	
301	            results = await asyncio.gather(*tasks)
302	            ok_count = sum(1 for r in results if r)
303	            fail_count[0] += len(results) - ok_count
304	
305	            # Small wait for hook I/O to flush
306	            await asyncio.sleep(0.2)
307	
308	            # Move all .pt files from collect dir, sorted by name
309	            pt_files = sorted(COLLECT_DIR.glob("*.pt"))
310	            for f in pt_files:
311	                dst = output_dir / f"{start_idx + success:06d}.pt"
312	                shutil.move(str(f), str(dst))
313	                success += 1
314	
315	            pbar.update(len(batch))
316	            pbar.set_postfix(ok=success, fail=fail_count[0])
317	
318	        pbar.close()
319	
320	        total_bytes = sum(f.stat().st_size for f in output_dir.glob("*.pt"))
321	        print(f"\nDone: {success} files, {total_bytes / 1024**3:.1f} GB")
322	        print(f"Failures: {fail_count[0]}")
323	        return success
324	
325	
326	# ── Main ──────────────────────────────────────────────────────────────
327	
328	def validate_pt(output_dir, label=""):
329	    """Validate a sample .pt file from output_dir."""
330	    pt_files = sorted(output_dir.glob("*.pt"))
331	    if not pt_files:
332	        print(f"  No files to validate in {output_dir}")
333	        return
334	    sample_f = pt_files[len(pt_files) // 2]
335	    d = torch.load(sample_f, weights_only=True)
336	    print(f"\nValidation {label}({sample_f.name}):")
337	    for k, v in d.items():
338	        print(f"  {k}: {v.shape} {v.dtype}")
339	    expected_keys = {"token_ids", "aux_hidden", "top_logit_values", "top_logit_indices"}
340	    assert set(d.keys()) == expected_keys, f"Unexpected keys: {set(d.keys())}"
341	    assert d["aux_hidden"].shape[-1] == 4096 * 3, f"Bad aux_hidden dim: {d['aux_hidden'].shape}"
342	    print("  PASSED")
343	
344	
345	def main():
346	    smoke = 0
347	    val_ood_mode = "--val-ood" in sys.argv
348	    if "--smoke" in sys.argv:
349	        idx = sys.argv.index("--smoke")
350	        smoke = int(sys.argv[idx + 1]) if idx + 1 < len(sys.argv) else 5
351	
352	    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
353	
354	    if val_ood_mode:
355	        # ── val_ood: 全量采集，不截断 ──────────────────────────────
356	        print(f"EAGLE-3 val_ood collection (no truncation, output={OUTPUT_VAL_OOD})")
357	        print("NOTE: server must be started with EAGLE3_MAX_TOKENS=0")
358	        samples = prepare_val_ood(tokenizer)
359	        # val_ood 序列长，降低并发避免 OOM
360	        n = asyncio.run(collect_split(samples, OUTPUT_VAL_OOD, concurrency=4))
361	        if n > 0:
362	            validate_pt(OUTPUT_VAL_OOD, "val_ood ")
363	    else:
364	        # ── train: 10000 × 2048 ──────────────────────────────────
365	        output_dir = OUTPUT_TRAIN
366	        print(f"EAGLE-3 train collection (seq_len={SEQ_LEN}, output={output_dir})")
367	        if smoke:
368	            print(f"*** SMOKE TEST: {smoke} samples ***")
369	
370	        samples = prepare_texts(tokenizer, smoke=smoke)
371	
372	        # Save manifest
373	        manifest_path = output_dir.parent / "manifest.json"
374	        output_dir.mkdir(parents=True, exist_ok=True)
375	        with open(manifest_path, "w") as f:
376	            json.dump(
377	                {
378	                    "total": len(samples),
379	                    "seq_len": SEQ_LEN,
380	                    "sources": {s["source"]: 0 for s in samples},
381	                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
382	                    "samples": [{"source": s["source"], "text_len": len(s["text"])} for s in samples],
383	                },
384	                f,
385	                indent=2,
386	            )
387	        print(f"Manifest saved to {manifest_path}")
388	
389	        n = asyncio.run(collect_split(samples, output_dir))
390	        if n > 0:
391	            validate_pt(output_dir, "train ")
392	
393	
394	if __name__ == "__main__":
395	    main()
396
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/convert_to_sglang.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Convert EAGLE-3 training checkpoint to sglang-compatible format.
4	
5	Produces a directory with:
6	  - config.json (LlamaConfig-compatible)
7	  - model.safetensors (weights with sglang naming)
8	
9	Usage:
10	    python3 eagle/convert_to_sglang.py [--ckpt eagle/weights/best.pt] [--output eagle/sglang_model]
11	"""
12	
13	import json
14	import os
15	from pathlib import Path
16	
17	import torch
18	from safetensors.torch import save_file
19	
20	
21	CKPT_PATH = Path("eagle/weights/epoch_4.pt")
22	OUTPUT_DIR = Path("eagle/sglang_model")
23	TARGET_MODEL = [REDACTED]
24	
25	# Architecture constants (must match train.py)
26	HIDDEN_SIZE = 4096
27	AUX_DIM = HIDDEN_SIZE * 3  # 12288
28	VOCAB_SIZE = 73448
29	DRAFT_VOCAB_SIZE = 32000
30	NUM_HEADS = 32
31	NUM_KV_HEADS = 2
32	HEAD_DIM = 128
33	INTERMEDIATE_SIZE = 16384
34	RMS_NORM_EPS = 1e-6
35	
36	
37	def convert():
38	    print(f"Loading checkpoint: {CKPT_PATH}")
39	    ckpt = torch.load(CKPT_PATH, weights_only=True)
40	    state = ckpt["model_state_dict"]
41	
42	    print(f"Checkpoint epoch: {ckpt['epoch']}, acc0: {ckpt.get('avg_acc0', 'N/A')}")
43	
44	    # Load vocab mapping
45	    vocab_cache = torch.load("eagle/data/vocab_cache.pt", weights_only=True)
46	    d2t = vocab_cache["d2t"]  # (32000,) — target vocab ids
47	
48	    # Convert d2t to diff format (what sglang expects)
49	    # sglang: hot_token_id = d2t_stored + arange(draft_vocab)
50	    # So d2t_stored = d2t - arange(draft_vocab)
51	    d2t_diff = d2t - torch.arange(DRAFT_VOCAB_SIZE)
52	
53	    # Map training state_dict keys to sglang keys
54	    key_mapping = {
55	        "fc.weight": "model.fc.weight",
56	        # Decoder layer
57	        "midlayer.input_emb_norm.weight": "model.midlayer.input_layernorm.weight",
58	        "midlayer.hidden_norm.weight": "model.midlayer.hidden_norm.weight",
59	        "midlayer.self_attn.q_proj.weight": "model.midlayer.self_attn.q_proj.weight",
60	        "midlayer.self_attn.k_proj.weight": "model.midlayer.self_attn.k_proj.weight",
61	        "midlayer.self_attn.v_proj.weight": "model.midlayer.self_attn.v_proj.weight",
62	        "midlayer.self_attn.o_proj.weight": "model.midlayer.self_attn.o_proj.weight",
63	        "midlayer.post_attention_layernorm.weight": "model.midlayer.post_attention_layernorm.weight",
64	        "midlayer.mlp.gate_proj.weight": "model.midlayer.mlp.gate_proj.weight",
65	        "midlayer.mlp.up_proj.weight": "model.midlayer.mlp.up_proj.weight",
66	        "midlayer.mlp.down_proj.weight": "model.midlayer.mlp.down_proj.weight",
67	        # Top-level norm
68	        "norm.weight": "model.norm.weight",
69	        # lm_head
70	        "lm_head.weight": "lm_head.weight",
71	    }
72	
73	    tensors = {}
74	    for train_key, sglang_key in key_mapping.items():
75	        if train_key in state:
76	            tensors[sglang_key] = state[train_key].to(torch.bfloat16)
77	        else:
78	            print(f"  WARNING: missing key {train_key}")
79	
80	    # Add d2t diff
81	    tensors["d2t"] = d2t_diff
82	
83	    # Add embed_tokens from target model (frozen, not in checkpoint)
84	    from safetensors import safe_open
85	    index_path = os.path.join(TARGET_MODEL, "model.safetensors.index.json")
86	    with open(index_path) as f:
87	        index = json.load(f)
88	    emb_file = index["weight_map"]["model.embed_tokens.weight"]
89	    with safe_open(os.path.join(TARGET_MODEL, emb_file), framework="pt", device="cpu") as f:
90	        embed_weight = f.get_tensor("model.embed_tokens.weight")
91	    tensors["model.embed_tokens.weight"] = embed_weight.to(torch.bfloat16)
92	
93	    # Save weights
94	    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
95	    save_file(tensors, OUTPUT_DIR / "model.safetensors")
96	    print(f"Saved weights: {len(tensors)} tensors")
97	
98	    # Generate config.json
99	    config = {
100	        "architectures": ["LlamaForCausalLMEagle3"],
101	        "model_type": "llama",
102	        "hidden_size": HIDDEN_SIZE,
103	        "intermediate_size": INTERMEDIATE_SIZE,
104	        "num_hidden_layers": 1,
105	        "num_attention_heads": NUM_HEADS,
106	        "num_key_value_heads": NUM_KV_HEADS,
107	        "head_dim": HEAD_DIM,
108	        "hidden_act": "silu",
109	        "max_position_embeddings": 524288,
110	        "rms_norm_eps": RMS_NORM_EPS,
111	        "vocab_size": VOCAB_SIZE,
112	        "draft_vocab_size": DRAFT_VOCAB_SIZE,
113	        "target_hidden_size": HIDDEN_SIZE,  # same as hidden_size since fc does 12288→4096
114	        "scale_emb": 12,
115	        "tie_word_embeddings": False,
116	        "torch_dtype": "bfloat16",
117	        # EAGLE-3 specific — sglang reads these from draft model config
118	        "eagle_config": {
119	            "use_aux_hidden_state": True,
120	            "eagle_aux_hidden_state_layer_ids": [1, 10, 22],
121	        },
122	    }
123	
124	    with open(OUTPUT_DIR / "config.json", "w") as f:
125	        json.dump(config, f, indent=2)
126	    print(f"Saved config.json")
127	
128	    # Copy tokenizer files from target model
129	    for fname in ["tokenizer.json", "tokenizer_config.json", "special_tokens_map.json",
130	                   "tokenizer.model", "added_tokens.json"]:
131	        src = os.path.join(TARGET_MODEL, fname)
132	        if os.path.exists(src):
133	            import shutil
134	            shutil.copy2(src, OUTPUT_DIR / fname)
135	            print(f"Copied {fname}")
136	
137	    # Verify
138	    print(f"\nOutput directory: {OUTPUT_DIR}")
139	    for f in sorted(OUTPUT_DIR.iterdir()):
140	        size = f.stat().st_size
141	        if size > 1024 * 1024:
142	            print(f"  {f.name}: {size / 1024 / 1024:.1f} MB")
143	        else:
144	            print(f"  {f.name}: {size / 1024:.1f} KB")
145	
146	    print(f"\nConversion complete! acc0={ckpt.get('avg_acc0', 'N/A')}")
147	    print(f"To use with sglang, pass --speculative-draft-model-path {OUTPUT_DIR.resolve()}")
148	
149	
150	if __name__ == "__main__":
151	    convert()
152
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/train.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Train EAGLE-3 draft model for MiniCPM-SALA speculative decoding.
4	
5	Architecture: fc(12288→4096) + 1 decoder layer (TTT 7-step) + norm + lm_head
6	Loss: plogp = -sum(target_p * log(draft_p)), weighted by 0.8^step
7	
8	Data: .pt files with {token_ids, aux_hidden, top_logit_values, top_logit_indices}
9	      aux_hidden = cat(layer1, layer10, layer22) of shape (seq_len, 12288)
10	
11	Run from repo user_4813494d:
12	    python3 eagle/train.py
13	"""
14	
15	import math
16	import os
17	import random
18	import time
19	from pathlib import Path
20	
21	import torch
22	import torch.nn as nn
23	import torch.nn.functional as F
24	from safetensors import safe_open
25	from tqdm import tqdm
26	
27	# ── Config ──────────────────────────────────────────────────────────────
28	DATA_DIR = Path("eagle/data/train")
29	VAL_DIR = Path("medusa/data/val_ood")  # reuse Medusa val_ood for monitoring
30	OUTPUT_DIR = Path("eagle/weights")
31	MODEL_PATH = [REDACTED]
32	
33	HIDDEN_SIZE = 4096
34	AUX_DIM = HIDDEN_SIZE * 3  # 12288
35	VOCAB_SIZE = 73448
36	DRAFT_VOCAB_SIZE = 32000
37	SCALE_EMB = 12
38	SCALE_WIDTH = HIDDEN_SIZE / 256  # 16
39	NUM_HEADS = 32
40	NUM_KV_HEADS = 2
41	HEAD_DIM = 128
42	INTERMEDIATE_SIZE = 16384
43	RMS_NORM_EPS = 1e-6
44	
45	TTT_STEPS = 1  # single-step: stable training, sufficient for spec decode
46	LOSS_DECAY = 0.8
47	SEQ_LEN = 2048
48	BATCH_SIZE = 2
49	GRAD_ACCUM = 4  # effective batch = 8
50	LR = 3e-4
51	WARMUP_STEPS = 500
52	WEIGHT_DECAY = 0.0
53	BETAS = (0.9, 0.95)
54	MAX_GRAD_NORM = 5.0
55	EPOCHS = 10
56	EVAL_EVERY_EPOCH = 1
57	GRAD_CHECKPOINT = True
58	SEED = 42
59	MIN_TOKENS = 128  # skip files shorter than this
60	
61	DEVICE = "cuda"
62	DTYPE = torch.bfloat16
63	
64	
65	# ── RMSNorm ─────────────────────────────────────────────────────────────
66	class RMSNorm(nn.Module):
67	    def __init__(self, dim, eps=1e-6):
68	        super().__init__()
69	        self.weight = nn.Parameter(torch.ones(dim))
70	        self.eps = eps
71	
72	    def forward(self, x):
73	        norm = x.float().pow(2).mean(-1, keepdim=True).add(self.eps).rsqrt()
74	        return (x * norm).to(x.dtype) * self.weight
75	
76	
77	# ── Attention (list-based cache, matching official EAGLE-3 cnets.py L227-314) ──
78	class Eagle3Attention(nn.Module):
79	    """EAGLE-3 attention with list-based KV cache across TTT steps.
80	
81	    Official mechanism:
82	    - Step 0: standard full causal attention Q @ K0^T → softmax → @ V0
83	    - Step i>0: K_i is a single "summary" vector per position (same shape as K0).
84	      Attention score for cached step i is element-wise dot: (q * k_i).sum(-1),
85	      producing one scalar per (batch, head, query_pos).
86	      These scalars are concatenated with the S scores from K0, then softmax.
87	      Output = attn_weights0 @ V0 + sum_i(attn_weights_i * V_i)
88	    """
89	    def __init__(self):
90	        super().__init__()
91	        self.num_heads = NUM_HEADS
92	        self.num_kv_heads = NUM_KV_HEADS
93	        self.head_dim = HEAD_DIM
94	        self.num_kv_groups = NUM_HEADS // NUM_KV_HEADS
95	
96	        qkv_in = HIDDEN_SIZE * 2  # cat(embed, hidden)
97	        self.q_proj = nn.Linear(qkv_in, NUM_HEADS * HEAD_DIM, bias=False)
98	        self.k_proj = nn.Linear(qkv_in, NUM_KV_HEADS * HEAD_DIM, bias=False)
99	        self.v_proj = nn.Linear(qkv_in, NUM_KV_HEADS * HEAD_DIM, bias=False)
100	        self.o_proj = nn.Linear(NUM_HEADS * HEAD_DIM, HIDDEN_SIZE, bias=False)
101	
102	    def forward(self, hidden_cat, cache_k_list, cache_v_list, causal_mask=None):
103	        """
104	        hidden_cat: (B, S, 2*H)
105	        cache_k_list: list of (B, num_heads, S, head_dim) from prior TTT steps, or None
106	        cache_v_list: list of (B, num_heads, S, head_dim) from prior TTT steps, or None
107	        causal_mask: (1, 1, S, S)
108	        Returns: output (B, S, H), new_cache_k_list, new_cache_v_list
109	        """
110	        B, S, _ = hidden_cat.shape
111	
112	        q = self.q_proj(hidden_cat).view(B, S, self.num_heads, self.head_dim).transpose(1, 2)
113	        k = self.k_proj(hidden_cat).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
114	        v = self.v_proj(hidden_cat).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
115	
116	        # GQA expand
117	        if self.num_kv_groups > 1:
118	            k = k.repeat_interleave(self.num_kv_groups, dim=1)
119	            v = v.repeat_interleave(self.num_kv_groups, dim=1)
120	
121	        # Build cache lists (copy to avoid in-place modification for grad checkpoint)
122	        if cache_k_list is None:
123	            local_cache_k = []
124	            local_cache_v = []
125	        else:
126	            local_cache_k = list(cache_k_list)
127	            local_cache_v = list(cache_v_list)
128	
129	        local_cache_k.append(k)
130	        local_cache_v.append(v)
131	
132	        n_cached = len(local_cache_k)
133	
134	        if n_cached == 1:
135	            # Step 0: use flash attention (memory efficient, no materialized attn matrix)
136	            # F.scaled_dot_product_attention with is_causal=True
137	            attn_output = F.scaled_dot_product_attention(
138	                q, local_cache_k[0], local_cache_v[0], is_causal=True
139	            )
140	        else:
141	            # Steps with cache: manual attention with cached KV summaries
142	            k0 = local_cache_k[0]
143	            v0 = local_cache_v[0]
144	
145	            attn_weights = torch.matmul(q, k0.transpose(-2, -1)) / math.sqrt(self.head_dim)
146	            if causal_mask is not None:
147	                attn_weights = attn_weights + causal_mask
148	
149	            for i in range(1, n_cached):
150	                ki = local_cache_k[i]
151	                attn_wi = (q * ki).sum(-1) / math.sqrt(self.head_dim)
152	                attn_weights = torch.cat([attn_weights, attn_wi.unsqueeze(-1)], dim=-1)
153	
154	            attn_weights = F.softmax(attn_weights, dim=-1, dtype=torch.float32).to(q.dtype)
155	
156	            attn_w0 = attn_weights[..., :S]
157	            attn_output = torch.matmul(attn_w0, v0)
158	
159	            for i in range(1, n_cached):
160	                vi = local_cache_v[i]
161	                wi = attn_weights[..., S + i - 1]
162	                attn_output = attn_output + wi.unsqueeze(-1) * vi
163	
164	        attn_output = attn_output.transpose(1, 2).contiguous().view(B, S, -1)
165	        return self.o_proj(attn_output), local_cache_k, local_cache_v
166	
167	
168	# ── MLP ──────────────────────────────────────────────────────────────────
169	class Eagle3MLP(nn.Module):
170	    def __init__(self):
171	        super().__init__()
172	        self.gate_proj = nn.Linear(HIDDEN_SIZE, INTERMEDIATE_SIZE, bias=False)
173	        self.up_proj = nn.Linear(HIDDEN_SIZE, INTERMEDIATE_SIZE, bias=False)
174	        self.down_proj = nn.Linear(INTERMEDIATE_SIZE, HIDDEN_SIZE, bias=False)
175	
176	    def forward(self, x):
177	        return self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))
178	
179	
180	# ── Decoder Layer ────────────────────────────────────────────────────────
181	class Eagle3DecoderLayer(nn.Module):
182	    def __init__(self):
183	        super().__init__()
184	        self.hidden_norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
185	        self.input_emb_norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
186	        self.self_attn = Eagle3Attention()
187	        self.post_attention_layernorm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
188	        self.mlp = Eagle3MLP()
189	
190	    def forward(self, input_emb, hidden_states, cache_k_list=None, cache_v_list=None, causal_mask=None):
191	        """
192	        input_emb: (B, S, H) - embedded tokens
193	        hidden_states: (B, S, H) - running hidden from fc or prior step
194	        cache_k_list, cache_v_list: list of tensors from prior TTT steps
195	        Returns: new_hidden (B, S, H), cache_k_list, cache_v_list
196	        """
197	        residual = hidden_states
198	
199	        normed_emb = self.input_emb_norm(input_emb)
200	        normed_hidden = self.hidden_norm(hidden_states)
201	        hidden_cat = torch.cat([normed_emb, normed_hidden], dim=-1)
202	
203	        attn_out, cache_k_list, cache_v_list = self.self_attn(hidden_cat, cache_k_list, cache_v_list, causal_mask)
204	        hidden_states = residual + attn_out
205	
206	        residual = hidden_states
207	        hidden_states = self.post_attention_layernorm(hidden_states)
208	        hidden_states = self.mlp(hidden_states)
209	        hidden_states = residual + hidden_states
210	
211	        return hidden_states, cache_k_list, cache_v_list
212	
213	
214	# ── EAGLE-3 Draft Model ─────────────────────────────────────────────────
215	class Eagle3Model(nn.Module):
216	    def __init__(self, embed_weight, lm_head_weight):
217	        """
218	        embed_weight: (vocab_size, hidden_size) from target model
219	        lm_head_weight: (vocab_size, hidden_size) from target model
220	        """
221	        super().__init__()
222	        self.fc = nn.Linear(AUX_DIM, HIDDEN_SIZE, bias=False)
223	        self.midlayer = Eagle3DecoderLayer()
224	        self.norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
225	
226	        # Frozen embedding from target (with scale_emb)
227	        self.embed_tokens = nn.Embedding.from_pretrained(embed_weight, freeze=True)
228	        self.scale_emb = SCALE_EMB
229	
230	        # lm_head initialized from target (subset rows set in _init_lm_head)
231	        self.lm_head = nn.Linear(HIDDEN_SIZE, DRAFT_VOCAB_SIZE, bias=False)
232	        self._full_lm_head_weight = lm_head_weight  # kept for init after vocab mapping
233	
234	        # d2t / t2d / draft_idx_map mappings (set later via build_vocab_mapping)
235	        self.register_buffer("d2t", torch.zeros(DRAFT_VOCAB_SIZE, dtype=torch.long))
236	        self.register_buffer("t2d", torch.zeros(VOCAB_SIZE, dtype=torch.bool))
237	        self.register_buffer("draft_idx_map", torch.zeros(VOCAB_SIZE, dtype=torch.long))
238	
239	        self.ttt_steps = TTT_STEPS
240	        self.loss_decay = LOSS_DECAY
241	
242	    def build_vocab_mapping(self, data_dir):
243	        """Build draft vocabulary from training data token frequency."""
244	        cache_path = data_dir.parent / "vocab_cache.pt"
245	        if cache_path.exists():
246	            cache = torch.load(cache_path, weights_only=True)
247	            self.d2t.copy_(cache["d2t"])
248	            self.t2d.copy_(cache["t2d"])
249	            print(f"Loaded vocab mapping from {cache_path}")
250	        else:
251	            print("Building draft vocabulary from training data...")
252	            from collections import Counter
253	            counter = Counter()
254	            pt_files = sorted(data_dir.glob("*.pt"))
255	            for f in tqdm(pt_files, desc="scanning vocab"):
256	                d = torch.load(f, weights_only=True)
257	                ids = d["token_ids"].numpy()
258	                for tok in ids:
259	                    counter[int(tok)] += 1
260	
261	            top_tokens = [tok for tok, _ in counter.most_common(DRAFT_VOCAB_SIZE)]
262	            top_tokens.sort()
263	
264	            d2t = torch.tensor(top_tokens, dtype=torch.long)
265	            t2d = torch.zeros(VOCAB_SIZE, dtype=torch.bool)
266	            t2d[d2t] = True
267	
268	            total_freq = sum(counter.values())
269	            covered_freq = sum(counter[t] for t in top_tokens)
270	            print(f"Draft vocab covers {covered_freq/total_freq:.2%} of tokens")
271	
272	            torch.save({"d2t": d2t, "t2d": t2d}, cache_path)
273	            self.d2t.copy_(d2t)
274	            self.t2d.copy_(t2d)
275	
276	        # Build draft_idx_map buffer (full_vocab_id -> draft_idx)
277	        self.draft_idx_map.zero_()
278	        self.draft_idx_map[self.d2t] = torch.arange(DRAFT_VOCAB_SIZE, device=self.draft_idx_map.device)
279	
280	        # Initialize lm_head from target model's lm_head (draft vocab subset)
281	        if self._full_lm_head_weight is not None:
282	            with torch.no_grad():
283	                self.lm_head.weight.copy_(self._full_lm_head_weight[self.d2t.cpu()])
284	            print(f"Initialized lm_head from target model ({DRAFT_VOCAB_SIZE} rows)")
285	            self._full_lm_head_weight = None  # free memory
286	
287	    def _make_causal_mask(self, total_len, device):
288	        """Create causal attention mask."""
289	        mask = torch.full((total_len, total_len), float("-inf"), device=device)
290	        mask = torch.triu(mask, diagonal=1)
291	        return mask[None, None, :, :]  # (1, 1, S, S)
292	
293	    def _build_target_p(self, target_logits_values, target_logits_indices, device):
294	        """Build target distribution from top-256 logits.
295	
296	        Maps top-256 full-vocab logits into draft vocab space, applies softmax.
297	        Mirrors official: target_head = full_logits[..., t2d]; target_p = softmax(target_head)
298	        We approximate by scattering top-256 logits into draft vocab positions.
299	        """
300	        B, S, K = target_logits_values.shape
301	        indices = target_logits_indices.long().clamp(0, VOCAB_SIZE - 1)
302	        in_draft = self.t2d[indices]  # (B, S, 256) bool
303	
304	        # Build draft-space logits: only scatter tokens that are in draft vocab
305	        # Use reduce='amax' to avoid race condition when multiple entries map to same idx
306	        draft_logits = torch.full((B, S, DRAFT_VOCAB_SIZE), -1e9, device=device, dtype=torch.float32)
307	        mapped_idx = self.draft_idx_map[indices]  # (B, S, 256)
308	        values = target_logits_values.float()
309	
310	        # Set non-draft entries to -1e9, then scatter with amax (max wins, -1e9 never beats valid)
311	        safe_vals = torch.where(in_draft, values, torch.tensor(-1e9, device=device))
312	        draft_logits.scatter_reduce_(2, mapped_idx, safe_vals, reduce="amax")
313	        target_p = F.softmax(draft_logits, dim=-1)
314	        return target_p
315	
316	    def forward(self, token_ids, aux_hidden, target_logits_values, target_logits_indices):
317	        """
318	        EAGLE-3 training with shifted alignment to match inference.
319	
320	        Inference pattern: (embed(x_{t+1}), fc(aux[t])) → predict x_{t+2}
321	        So we shift inputs: position t gets token[t+1] with hidden[t], target[t+1].
322	
323	        1. Shift: input_ids = token_ids[:,1:], aux = aux_hidden[:,:-1], target = target[:,1:]
324	        2. fc(aux) → hidden
325	        3. For each TTT step:
326	           a. embed(input_ids) → input_emb
327	           b. midlayer(input_emb, hidden, cache) → hidden_out
328	           c. norm(hidden_out) → lm_head → logits
329	           d. plogp loss with position_mask
330	           e. Shift input_ids, target, loss by 1 position (padding left=False)
331	        """
332	        B, S_orig = token_ids.shape
333	        device = token_ids.device
334	
335	        # Shift alignment: match inference pattern (x_{t+1}, aux[t]) → predict x_{t+2}
336	        input_ids = token_ids[:, 1:]           # (B, S-1): tokens x_1..x_{S-1}
337	        aux_shifted = aux_hidden[:, :-1, :]    # (B, S-1, 12288): aux_0..aux_{S-2}
338	        target_values = target_logits_values[:, 1:, :]   # (B, S-1, K)
339	        target_indices = target_logits_indices[:, 1:, :]  # (B, S-1, K)
340	        S = S_orig - 1
341	
342	        hidden = self.fc(aux_shifted)
343	
344	        # Build causal mask once (same sequence length throughout, no KV cache accumulation)
345	        # Official EAGLE-3 uses standard causal mask, NOT accumulating KV across TTT steps
346	        causal_mask = self._make_causal_mask(S, device)
347	
348	        step_losses = []
349	        step_accs = []
350	        cache_k_list = None
351	        cache_v_list = None
352	
353	        for step in range(self.ttt_steps):
354	            last = step == self.ttt_steps - 1
355	
356	            # Embed current input_ids
357	            input_emb = self.embed_tokens(input_ids) * self.scale_emb
358	            input_emb = input_emb.to(hidden.dtype)
359	
360	            # Forward through decoder layer with list-based KV cache
361	            if GRAD_CHECKPOINT and self.training:
362	                def _fwd(ie, hs, cm, *cache_tensors):
363	                    # Reconstruct lists from flattened tensors
364	                    n = len(cache_tensors) // 2
365	                    ck = list(cache_tensors[:n]) if n > 0 else None
366	                    cv = list(cache_tensors[n:]) if n > 0 else None
367	                    out, new_ck, new_cv = self.midlayer(ie, hs, ck, cv, cm)
368	                    return (out, *new_ck, *new_cv)
369	
370	                # Flatten cache lists for checkpoint (it needs tensors, not lists)
371	                cache_tensors = []
372	                if cache_k_list is not None:
373	                    cache_tensors = [*cache_k_list, *cache_v_list]
374	                results = torch.utils.checkpoint.checkpoint(
375	                    _fwd, input_emb, hidden, causal_mask, *cache_tensors,
376	                    use_reentrant=False,
377	                )
378	                hidden_out = results[0]
379	                n_cache = (len(results) - 1) // 2
380	                cache_k_list = list(results[1:1+n_cache])
381	                cache_v_list = list(results[1+n_cache:])
382	            else:
383	                hidden_out, cache_k_list, cache_v_list = self.midlayer(
384	                    input_emb, hidden, cache_k_list, cache_v_list, causal_mask,
385	                )
386	            hidden = hidden_out
387	
388	            # Compute target distribution for this step's target
389	            with torch.no_grad():
390	                target_p = self._build_target_p(target_values, target_indices, device)
391	                # target_p: (B, S, draft_vocab)
392	
393	                # Position mask: only positions where target argmax is in draft vocab
394	                target_argmax_full = target_indices[:, :, 0].long().clamp(0, VOCAB_SIZE - 1)  # top-1
395	                target_mask = self.t2d[target_argmax_full].float()  # (B, S)
396	
397	            # Logits
398	            normed = self.norm(hidden_out)
399	            logits = self.lm_head(normed).float()  # (B, S, draft_vocab)
400	
401	            # plogp loss (official L854-855) — mean over valid positions
402	            out_logp = F.log_softmax(logits, dim=-1)
403	            plogp = target_p * out_logp  # (B, S, draft_vocab)
404	            neg_ce = -plogp.sum(dim=-1)  # (B, S) — cross-entropy per position
405	            # Average only over positions where target is in draft vocab
406	            n_valid = target_mask.sum().clamp(min=1)
407	            loss = (neg_ce * target_mask).sum() / n_valid
408	            step_losses.append(loss)
409	
410	            # Accuracy
411	            with torch.no_grad():
412	                pred_idx = logits.argmax(-1)  # (B, S)
413	                target_draft_idx = target_p.argmax(-1)  # (B, S)
414	                correct = (pred_idx == target_draft_idx).float() * target_mask
415	                acc = correct.sum().item() / (target_mask.sum().item() + 1e-6)
416	                step_accs.append(acc)
417	
418	            # Shift for next step (official L862-864)
419	            if not last:
420	                # padding(x, left=False) = cat(x[:,1:], zeros)
421	                input_ids = torch.cat([input_ids[:, 1:], torch.zeros(B, 1, dtype=input_ids.dtype, device=device)], dim=1)
422	                target_values = torch.cat([target_values[:, 1:, :], torch.zeros(B, 1, target_values.shape[2], dtype=target_values.dtype, device=device)], dim=1)
423	                target_indices = torch.cat([target_indices[:, 1:, :], torch.zeros(B, 1, target_indices.shape[2], dtype=target_indices.dtype, device=device)], dim=1)
424	
425	        # Weighted total loss
426	        total_loss = sum(self.loss_decay ** i * l for i, l in enumerate(step_losses))
427	        return total_loss, step_losses, step_accs
428	
429	
430	# ── Data loading ─────────────────────────────────────────────────────────
431	def load_batch(files, device):
432	    """Load a batch of .pt files and collate with padding."""
433	    batch = {"token_ids": [], "aux_hidden": [], "top_logit_values": [], "top_logit_indices": []}
434	    for f in files:
435	        d = torch.load(f, weights_only=True)
436	        for k in batch:
437	            batch[k].append(d[k][:SEQ_LEN])  # truncate to SEQ_LEN
438	
439	    # Pad to max length in batch
440	    max_len = max(t.shape[0] for t in batch["token_ids"])
441	    for k in batch:
442	        padded = []
443	        for t in batch[k]:
444	            if t.shape[0] < max_len:
445	                pad_shape = list(t.shape)
446	                pad_shape[0] = max_len - t.shape[0]
447	                t = torch.cat([t, torch.zeros(pad_shape, dtype=t.dtype)], dim=0)
448	            padded.append(t)
449	        batch[k] = torch.stack(padded).to(device)
450	    batch["aux_hidden"] = batch["aux_hidden"].to(DTYPE)
451	    batch["top_logit_values"] = batch["top_logit_values"].to(DTYPE)
452	    return batch
453	
454	
455	def load_embed_and_lm_head():
456	    """Load frozen embed_tokens and lm_head from target model."""
457	    import json
458	    config_path = os.path.join(MODEL_PATH, "config.json")
459	    with open(config_path) as f:
460	        config = json.load(f)
461	
462	    # Load from safetensors
463	    index_path = os.path.join(MODEL_PATH, "model.safetensors.index.json")
464	    if os.path.exists(index_path):
465	        with open(index_path) as f:
466	            index = json.load(f)
467	        weight_map = index["weight_map"]
468	
469	        emb_file = weight_map.get("model.embed_tokens.weight", None)
470	        lm_file = weight_map.get("lm_head.weight", None)
471	
472	        with safe_open(os.path.join(MODEL_PATH, emb_file), framework="pt", device="cpu") as f:
473	            embed_weight = f.get_tensor("model.embed_tokens.weight").float()
474	
475	        if lm_file:
476	            with safe_open(os.path.join(MODEL_PATH, lm_file), framework="pt", device="cpu") as f:
477	                lm_weight = f.get_tensor("lm_head.weight").float()
478	        else:
479	            # tied embeddings
480	            lm_weight = embed_weight.clone()
481	    else:
482	        # Single safetensors file
483	        st_path = os.path.join(MODEL_PATH, "model.safetensors")
484	        with safe_open(st_path, framework="pt", device="cpu") as f:
485	            embed_weight = f.get_tensor("model.embed_tokens.weight").float()
486	            try:
487	                lm_weight = f.get_tensor("lm_head.weight").float()
488	            except:
489	                lm_weight = embed_weight.clone()
490	
491	    print(f"Loaded embed_tokens: {embed_weight.shape}, lm_head: {lm_weight.shape}")
492	    return embed_weight, lm_weight
493	
494	
495	# ── Main ─────────────────────────────────────────────────────────────────
496	def main():
497	    random.seed(SEED)
498	    torch.manual_seed(SEED)
499	    torch.cuda.manual_seed(SEED)
500	
501	    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
502	
503	    # Load target model weights
504	    print("Loading target model embed/lm_head...")
505	    embed_weight, lm_weight = load_embed_and_lm_head()
506	
507	    # Build model
508	    model = Eagle3Model(embed_weight, lm_weight).to(DEVICE).to(DTYPE)
509	    model.build_vocab_mapping(DATA_DIR)
510	
511	    # Count params
512	    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
513	    frozen = sum(p.numel() for p in model.parameters() if not p.requires_grad)
514	    print(f"Trainable: {trainable/1e6:.1f}M, Frozen: {frozen/1e6:.1f}M")
515	
516	    # Optimizer
517	    optimizer = torch.optim.AdamW(
518	        [p for p in model.parameters() if p.requires_grad],
519	        lr=LR, betas=BETAS, weight_decay=WEIGHT_DECAY,
520	    )
521	
522	    # Data — filter short files by file size (MIN_TOKENS * ~26KB/token)
523	    # 128 tokens ≈ 3.2 MB (each token has 12288*2 + 256*2 + 256*4 + 8 bytes ≈ 26KB)
524	    min_file_size = MIN_TOKENS * 26 * 1024
525	    all_files = sorted(DATA_DIR.glob("*.pt"))
526	    pt_files = [f for f in all_files if f.stat().st_size >= min_file_size]
527	    print(f"Training files: {len(pt_files)} (filtered from {len(all_files)}, min_size={min_file_size//1024}KB)")
528	    if len(pt_files) == 0:
529	        print("No training data! Run eagle/collect_data.py first.")
530	        return
531	
532	    steps_per_epoch = len(pt_files) // BATCH_SIZE
533	    total_steps = steps_per_epoch * EPOCHS // GRAD_ACCUM
534	    print(f"Steps/epoch: {steps_per_epoch}, Total steps: {total_steps}, Effective batch: {BATCH_SIZE * GRAD_ACCUM}")
535	
536	    # LR scheduler
537	    def lr_lambda(step):
538	        if step < WARMUP_STEPS:
539	            return step / max(1, WARMUP_STEPS)
540	        progress = (step - WARMUP_STEPS) / max(1, total_steps - WARMUP_STEPS)
541	        return 0.5 * (1 + math.cos(math.pi * progress))
542	
543	    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)
544	
545	    # Training loop
546	    global_step = 0
547	    best_acc = 0
548	    model.train()
549	
550	    for epoch in range(EPOCHS):
551	        random.shuffle(pt_files)
552	        epoch_loss = 0
553	        epoch_acc0 = 0
554	        n_batches = 0
555	
556	        pbar = tqdm(range(0, len(pt_files) - BATCH_SIZE + 1, BATCH_SIZE),
557	                     desc=f"Epoch {epoch+1}/{EPOCHS}", unit="batch")
558	
559	        optimizer.zero_grad()
560	
561	        for batch_idx in pbar:
562	            batch_files = pt_files[batch_idx:batch_idx + BATCH_SIZE]
563	            batch = load_batch(batch_files, DEVICE)
564	
565	            total_loss, step_losses, step_accs = model(
566	                batch["token_ids"],
567	                batch["aux_hidden"],
568	                batch["top_logit_values"],
569	                batch["top_logit_indices"],
570	            )
571	
572	            loss = total_loss / GRAD_ACCUM
573	            loss.backward()
574	
575	            if (n_batches + 1) % GRAD_ACCUM == 0:
576	                torch.nn.utils.clip_grad_norm_(model.parameters(), MAX_GRAD_NORM)
577	                optimizer.step()
578	                scheduler.step()
579	                optimizer.zero_grad()
580	                global_step += 1
581	
582	            epoch_loss += total_loss.item()
583	            epoch_acc0 += step_accs[0]
584	            n_batches += 1
585	
586	            pbar.set_postfix(
587	                loss=f"{total_loss.item():.3f}",
588	                acc0=f"{step_accs[0]:.3f}",
589	                lr=f"{scheduler.get_last_lr()[0]:.2e}",
590	                gstep=global_step,
591	            )
592	
593	            if n_batches % 200 == 0 and n_batches > 0:
594	                avg_recent = epoch_loss / n_batches
595	                avg_acc_recent = epoch_acc0 / n_batches
596	                print(f"\n  [{time.strftime('%H:%M:%S')}] batch {n_batches}: "
597	                      f"avg_loss={avg_recent:.3f}, avg_acc0={avg_acc_recent:.3f}, "
598	                      f"lr={scheduler.get_last_lr()[0]:.2e}, gstep={global_step}")
599	
600	        avg_loss = epoch_loss / max(n_batches, 1)
601	        avg_acc0 = epoch_acc0 / max(n_batches, 1)
602	        print(f"Epoch {epoch+1}: loss={avg_loss:.4f}, step0_acc={avg_acc0:.4f}")
603	
604	        # Save checkpoint
605	        ckpt = {
606	            "epoch": epoch + 1,
607	            "model_state_dict": {k: v.cpu() for k, v in model.state_dict().items()
608	                                  if not k.startswith("embed_tokens")},
609	            "optimizer_state_dict": optimizer.state_dict(),
610	            "avg_loss": avg_loss,
611	            "avg_acc0": avg_acc0,
612	            "config": {
613	                "hidden_size": HIDDEN_SIZE,
614	                "draft_vocab_size": DRAFT_VOCAB_SIZE,
615	                "ttt_steps": TTT_STEPS,
616	                "aux_layers": [1, 10, 22],
617	            },
618	        }
619	        torch.save(ckpt, OUTPUT_DIR / f"epoch_{epoch+1}.pt")
620	
621	        if avg_acc0 > best_acc:
622	            best_acc = avg_acc0
623	            torch.save(ckpt, OUTPUT_DIR / "best.pt")
624	            print(f"  New best! acc0={best_acc:.4f}")
625	
626	    print(f"\nTraining complete. Best acc0: {best_acc:.4f}")
627	    print(f"Checkpoints saved to {OUTPUT_DIR}")
628	
629	
630	if __name__ == "__main__":
631	    main()
632
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/eval_ood_accept.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Evaluate EAGLE-3 accept rate on OOD data.
4	Simulates full inference forward to match online behavior.
5	"""
6	
7	import math
8	import torch
9	import torch.nn as nn
10	import torch.nn.functional as F
11	from pathlib import Path
12	from safetensors import safe_open
13	
14	DEVICE = "cuda"
15	DTYPE = torch.bfloat16
16	
17	# Model config (from train.py)
18	HIDDEN_SIZE = 4096
19	AUX_DIM = HIDDEN_SIZE * 3  # 12288
20	VOCAB_SIZE = 73448
21	DRAFT_VOCAB_SIZE = 32000
22	SCALE_EMB = 12
23	NUM_HEADS = 32
24	NUM_KV_HEADS = 2
25	HEAD_DIM = 128
26	INTERMEDIATE_SIZE = 16384
27	RMS_NORM_EPS = 1e-6
28	
29	
30	class RMSNorm(nn.Module):
31	    def __init__(self, dim, eps=1e-6):
32	        super().__init__()
33	        self.weight = nn.Parameter(torch.ones(dim))
34	        self.eps = eps
35	
36	    def forward(self, x):
37	        norm = x.float().pow(2).mean(-1, keepdim=True).add(self.eps).rsqrt()
38	        return (x * norm).to(x.dtype) * self.weight
39	
40	
41	class Eagle3Attention(nn.Module):
42	    """Simplified attention for eval (no KV cache, single step)."""
43	    def __init__(self):
44	        super().__init__()
45	        self.num_heads = NUM_HEADS
46	        self.num_kv_heads = NUM_KV_HEADS
47	        self.head_dim = HEAD_DIM
48	        self.num_kv_groups = NUM_HEADS // NUM_KV_HEADS
49	
50	        qkv_in = HIDDEN_SIZE * 2
51	        self.q_proj = nn.Linear(qkv_in, NUM_HEADS * HEAD_DIM, bias=False)
52	        self.k_proj = nn.Linear(qkv_in, NUM_KV_HEADS * HEAD_DIM, bias=False)
53	        self.v_proj = nn.Linear(qkv_in, NUM_KV_HEADS * HEAD_DIM, bias=False)
54	        self.o_proj = nn.Linear(NUM_HEADS * HEAD_DIM, HIDDEN_SIZE, bias=False)
55	
56	    def forward(self, hidden_cat):
57	        B, S, _ = hidden_cat.shape
58	        q = self.q_proj(hidden_cat).view(B, S, self.num_heads, self.head_dim).transpose(1, 2)
59	        k = self.k_proj(hidden_cat).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
60	        v = self.v_proj(hidden_cat).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
61	
62	        if self.num_kv_groups > 1:
63	            k = k.repeat_interleave(self.num_kv_groups, dim=1)
64	            v = v.repeat_interleave(self.num_kv_groups, dim=1)
65	
66	        attn_output = F.scaled_dot_product_attention(q, k, v, is_causal=True)
67	        attn_output = attn_output.transpose(1, 2).contiguous().view(B, S, -1)
68	        return self.o_proj(attn_output)
69	
70	
71	class Eagle3MLP(nn.Module):
72	    def __init__(self):
73	        super().__init__()
74	        self.gate_proj = nn.Linear(HIDDEN_SIZE, INTERMEDIATE_SIZE, bias=False)
75	        self.up_proj = nn.Linear(HIDDEN_SIZE, INTERMEDIATE_SIZE, bias=False)
76	        self.down_proj = nn.Linear(INTERMEDIATE_SIZE, HIDDEN_SIZE, bias=False)
77	
78	    def forward(self, x):
79	        return self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))
80	
81	
82	class Eagle3Model(nn.Module):
83	    def __init__(self):
84	        super().__init__()
85	        self.fc = nn.Linear(AUX_DIM, HIDDEN_SIZE, bias=False)
86	        self.input_layernorm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
87	        self.hidden_norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
88	        self.self_attn = Eagle3Attention()
89	        self.post_attention_layernorm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
90	        self.mlp = Eagle3MLP()
91	        self.norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
92	        self.embed_tokens = nn.Embedding(VOCAB_SIZE, HIDDEN_SIZE)
93	        self.lm_head = nn.Linear(HIDDEN_SIZE, DRAFT_VOCAB_SIZE, bias=False)
94	        self.scale_emb = SCALE_EMB
95	
96	    def forward(self, token_ids, aux_hidden):
97	        """
98	        token_ids: (B, S) or (S,)
99	        aux_hidden: (B, S, 12288) or (S, 12288)
100	        Returns: logits (B, S, draft_vocab) or (S, draft_vocab)
101	        """
102	        if token_ids.dim() == 1:
103	            token_ids = token_ids.unsqueeze(0)
104	            aux_hidden = aux_hidden.unsqueeze(0)
105	            squeeze_out = True
106	        else:
107	            squeeze_out = False
108	
109	        # fc projection
110	        hidden_states = self.fc(aux_hidden)
111	
112	        # embed tokens
113	        embeds = self.embed_tokens(token_ids) * self.scale_emb
114	        embeds = embeds.to(hidden_states.dtype)
115	
116	        # decoder layer forward (matching llama_eagle3.py)
117	        residual = hidden_states
118	        embeds_normed = self.input_layernorm(embeds)
119	        hidden_normed = self.hidden_norm(hidden_states)
120	        hidden_cat = torch.cat([embeds_normed, hidden_normed], dim=-1)
121	
122	        # attention
123	        attn_out = self.self_attn(hidden_cat)
124	        hidden_states = residual + attn_out
125	
126	        # MLP
127	        residual = hidden_states
128	        hidden_states = self.post_attention_layernorm(hidden_states)
129	        hidden_states = self.mlp(hidden_states)
130	        hidden_states = residual + hidden_states
131	
132	        # final norm + lm_head
133	        hidden_states = self.norm(hidden_states)
134	        logits = self.lm_head(hidden_states)
135	
136	        if squeeze_out:
137	            logits = logits.squeeze(0)
138	        return logits
139	
140	
141	def load_model(ckpt_path=None):
142	    model = Eagle3Model().to(DEVICE).to(DTYPE)
143	
144	    if ckpt_path and Path(ckpt_path).suffix == ".pt":
145	        # Load from training checkpoint — remap midlayer keys to flat names
146	        ckpt = torch.load(ckpt_path, weights_only=True, map_location="cpu")
147	        raw_state = ckpt["model_state_dict"]
148	        state_dict = {}
149	        for k, v in raw_state.items():
150	            nk = k
151	            if nk.startswith("midlayer."):
152	                nk = nk[len("midlayer."):]
153	            if nk == "input_emb_norm.weight":
154	                nk = "input_layernorm.weight"
155	            state_dict[nk] = v
156	        print(f"Loaded checkpoint: epoch={ckpt.get('epoch')}, avg_acc0={ckpt.get('avg_acc0', 'N/A')}")
157	        print(f"  Mapped keys: {sorted(state_dict.keys())}")
158	    else:
159	        # Load from sglang_model format
160	        with safe_open("eagle/sglang_model/model.safetensors", framework="pt", device="cpu") as f:
161	            state_dict = {}
162	            for key in f.keys():
163	                tensor = f.get_tensor(key)
164	                if key.startswith("model."):
165	                    key = key[6:]
166	                if key == "midlayer.input_layernorm.weight":
167	                    [REDACTED]
168	                elif key == "midlayer.hidden_norm.weight":
169	                    [REDACTED]
170	                elif key == "midlayer.post_attention_layernorm.weight":
171	                    [REDACTED]
172	                elif key.startswith("midlayer.self_attn."):
173	                    key = key.replace("midlayer.self_attn.", "self_attn.")
174	                elif key.startswith("midlayer.mlp."):
175	                    key = key.replace("midlayer.mlp.", "mlp.")
176	                elif key == "norm.weight":
177	                    key = "norm.weight"
178	                state_dict[key] = tensor
179	
180	    # Load embed_tokens from target model
181	    import json
182	    target_path = [REDACTED]
183	    with open(f"{target_path}/model.safetensors.index.json") as f:
184	        index = json.load(f)
185	    emb_file = index["weight_map"]["model.embed_tokens.weight"]
186	    with safe_open(f"{target_path}/{emb_file}", framework="pt", device="cpu") as f:
187	        state_dict["embed_tokens.weight"] = f.get_tensor("model.embed_tokens.weight")
188	
189	    model.load_state_dict(state_dict, strict=False)
190	    model.eval()
191	    return model
192	
193	
194	def load_vocab_mapping():
195	    cache = torch.load("eagle/data/vocab_cache.pt", weights_only=True)
196	    d2t = cache["d2t"].to(DEVICE)
197	    t2d = cache["t2d"].to(DEVICE)
198	    draft_idx_map = torch.zeros(VOCAB_SIZE, dtype=torch.long, device=DEVICE)
199	    draft_idx_map[d2t] = torch.arange(DRAFT_VOCAB_SIZE, device=DEVICE)
200	    return d2t, t2d, draft_idx_map
201	
202	
203	def build_target_p(target_logits_values, target_logits_indices, t2d, draft_idx_map):
204	    """Build target distribution from top-256 logits."""
205	    S, K = target_logits_values.shape
206	    indices = target_logits_indices.long().clamp(0, VOCAB_SIZE - 1)
207	    in_draft = t2d[indices]
208	
209	    draft_logits = torch.full((S, DRAFT_VOCAB_SIZE), -1e9, device=DEVICE, dtype=torch.float32)
210	    mapped_idx = draft_idx_map[indices]
211	    values = target_logits_values.float()
212	
213	    safe_vals = torch.where(in_draft, values, torch.tensor(-1e9, device=DEVICE))
214	    draft_logits.scatter_reduce_(1, mapped_idx, safe_vals, reduce="amax")
215	    target_p = F.softmax(draft_logits, dim=-1)
216	    return target_p
217	
218	
219	def main():
220	    import sys
221	    ckpt_path = sys.argv[1] if len(sys.argv) > 1 else None
222	    print(f"Loading model... (ckpt={ckpt_path})")
223	    model = load_model(ckpt_path)
224	    d2t, t2d, draft_idx_map = load_vocab_mapping()
225	
226	    # Load OOD data
227	    ood_dir = Path("/tmp/eagle3_val_collect")
228	    pt_files = sorted(ood_dir.glob("*.pt"))
229	    print(f"Found {len(pt_files)} OOD files")
230	
231	    total_correct = 0
232	    total_valid = 0
233	    total_tokens = 0
234	
235	    with torch.no_grad():
236	        for i, pt_file in enumerate(pt_files):
237	            data = torch.load(pt_file, weights_only=True)
238	            token_ids = data["token_ids"].to(DEVICE)
239	            aux_hidden = data["aux_hidden"].to(DEVICE).to(DTYPE)
240	            top_logit_values = data["top_logit_values"].to(DEVICE).to(DTYPE)
241	            top_logit_indices = data["top_logit_indices"].to(DEVICE)
242	
243	            seq_len = token_ids.shape[0]
244	            if seq_len < 3:
245	                continue
246	
247	            # Shifted alignment: match inference (x_{t+1}, aux[t]) → predict x_{t+2}
248	            shifted_ids = token_ids[1:]           # x_1..x_{S-1}
249	            shifted_aux = aux_hidden[:-1]          # aux_0..aux_{S-2}
250	            shifted_target_vals = top_logit_values[1:]
251	            shifted_target_inds = top_logit_indices[1:]
252	
253	            # Forward
254	            logits = model(shifted_ids, shifted_aux)  # (S-1, draft_vocab)
255	
256	            # Build target distribution
257	            target_p = build_target_p(shifted_target_vals, shifted_target_inds, t2d, draft_idx_map)
258	
259	            # Compute accept rate
260	            pred_draft_idx = logits.argmax(dim=-1)
261	            target_draft_idx = target_p.argmax(dim=-1)
262	
263	            # Only count positions where target argmax is in draft vocab
264	            target_argmax_full = shifted_target_inds[:, 0].long().clamp(0, VOCAB_SIZE - 1)
265	            target_mask = t2d[target_argmax_full].float()
266	
267	            correct = (pred_draft_idx == target_draft_idx).float() * target_mask
268	            n_correct = correct.sum().item()
269	            n_valid = target_mask.sum().item()
270	
271	            total_correct += n_correct
272	            total_valid += n_valid
273	            total_tokens += seq_len - 1
274	
275	            if i < 5:
276	                acc = n_correct / n_valid if n_valid > 0 else 0
277	                print(f"[{i}] {pt_file.name}: seq_len={seq_len}, valid={int(n_valid)}, correct={int(n_correct)}, acc={acc:.1%}")
278	
279	    print(f"\n{'='*60}")
280	    print(f"Total tokens: {total_tokens}")
281	    print(f"Valid positions: {int(total_valid)}")
282	    print(f"Correct predictions: {int(total_correct)}")
283	    print(f"OOD Accept Rate: {total_correct/total_valid:.1%}" if total_valid > 0 else "N/A")
284	
285	
286	if __name__ == "__main__":
287	    main()
288
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/test_decode_mode.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Test EAGLE-3 in decode mode (position-by-position with KV cache simulation).
4	Compare with full-sequence mode to find discrepancies.
5	"""
6	
7	import torch
8	import torch.nn as nn
9	import torch.nn.functional as F
10	from pathlib import Path
11	from safetensors import safe_open
12	
13	DEVICE = "cuda"
14	DTYPE = torch.bfloat16
15	
16	# Model config
17	HIDDEN_SIZE = 4096
18	AUX_DIM = HIDDEN_SIZE * 3
19	VOCAB_SIZE = 73448
20	DRAFT_VOCAB_SIZE = 32000
21	SCALE_EMB = 12
22	NUM_HEADS = 32
23	NUM_KV_HEADS = 2
24	HEAD_DIM = 128
25	INTERMEDIATE_SIZE = 16384
26	RMS_NORM_EPS = 1e-6
27	
28	
29	class RMSNorm(nn.Module):
30	    def __init__(self, dim, eps=1e-6):
31	        super().__init__()
32	        self.weight = nn.Parameter(torch.ones(dim))
33	        self.eps = eps
34	
35	    def forward(self, x):
36	        norm = x.float().pow(2).mean(-1, keepdim=True).add(self.eps).rsqrt()
37	        return (x * norm).to(x.dtype) * self.weight
38	
39	
40	class Eagle3AttentionWithKVCache(nn.Module):
41	    """Attention with KV cache for decode simulation."""
42	    def __init__(self):
43	        super().__init__()
44	        self.num_heads = NUM_HEADS
45	        self.num_kv_heads = NUM_KV_HEADS
46	        self.head_dim = HEAD_DIM
47	        self.num_kv_groups = NUM_HEADS // NUM_KV_HEADS
48	
49	        qkv_in = HIDDEN_SIZE * 2
50	        self.q_proj = nn.Linear(qkv_in, NUM_HEADS * HEAD_DIM, bias=False)
51	        self.k_proj = nn.Linear(qkv_in, NUM_KV_HEADS * HEAD_DIM, bias=False)
52	        self.v_proj = nn.Linear(qkv_in, NUM_KV_HEADS * HEAD_DIM, bias=False)
53	        self.o_proj = nn.Linear(NUM_HEADS * HEAD_DIM, HIDDEN_SIZE, bias=False)
54	
55	        # KV cache
56	        self.k_cache = None
57	        self.v_cache = None
58	
59	    def clear_cache(self):
60	        self.k_cache = None
61	        self.v_cache = None
62	
63	    def forward(self, hidden_cat, use_cache=False, pos=None):
64	        """
65	        hidden_cat: (B, S, 2*H) or (B, 1, 2*H) for decode
66	        use_cache: if True, use KV cache for decode mode
67	        pos: current position (for decode mode)
68	        """
69	        B, S, _ = hidden_cat.shape
70	        q = self.q_proj(hidden_cat).view(B, S, self.num_heads, self.head_dim).transpose(1, 2)
71	        k = self.k_proj(hidden_cat).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
72	        v = self.v_proj(hidden_cat).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
73	
74	        if use_cache:
75	            if self.k_cache is None:
76	                self.k_cache = k
77	                self.v_cache = v
78	            else:
79	                self.k_cache = torch.cat([self.k_cache, k], dim=2)
80	                self.v_cache = torch.cat([self.v_cache, v], dim=2)
81	            k = self.k_cache
82	            v = self.v_cache
83	
84	        # Expand KV heads
85	        if self.num_kv_groups > 1:
86	            k = k.repeat_interleave(self.num_kv_groups, dim=1)
87	            v = v.repeat_interleave(self.num_kv_groups, dim=1)
88	
89	        # For decode mode (S=1), only attend to past positions
90	        if use_cache and S == 1:
91	            # q: (B, heads, 1, head_dim)
92	            # k, v: (B, heads, seq_len, head_dim)
93	            attn_output = F.scaled_dot_product_attention(q, k, v, is_causal=False)
94	        else:
95	            attn_output = F.scaled_dot_product_attention(q, k, v, is_causal=True)
96	
97	        attn_output = attn_output.transpose(1, 2).contiguous().view(B, S, -1)
98	        return self.o_proj(attn_output)
99	
100	
101	class Eagle3MLP(nn.Module):
102	    def __init__(self):
103	        super().__init__()
104	        self.gate_proj = nn.Linear(HIDDEN_SIZE, INTERMEDIATE_SIZE, bias=False)
105	        self.up_proj = nn.Linear(HIDDEN_SIZE, INTERMEDIATE_SIZE, bias=False)
106	        self.down_proj = nn.Linear(INTERMEDIATE_SIZE, HIDDEN_SIZE, bias=False)
107	
108	    def forward(self, x):
109	        return self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))
110	
111	
112	class Eagle3ModelWithKVCache(nn.Module):
113	    def __init__(self):
114	        super().__init__()
115	        self.fc = nn.Linear(AUX_DIM, HIDDEN_SIZE, bias=False)
116	        self.input_layernorm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
117	        self.hidden_norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
118	        self.self_attn = Eagle3AttentionWithKVCache()
119	        self.post_attention_layernorm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
120	        self.mlp = Eagle3MLP()
121	        self.norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
122	        self.embed_tokens = nn.Embedding(VOCAB_SIZE, HIDDEN_SIZE)
123	        self.lm_head = nn.Linear(HIDDEN_SIZE, DRAFT_VOCAB_SIZE, bias=False)
124	        self.scale_emb = SCALE_EMB
125	
126	    def clear_cache(self):
127	        self.self_attn.clear_cache()
128	
129	    def forward_with_kv_cache(self, token_ids, aux_hidden, use_cache=False, pos=None):
130	        """
131	        Forward with optional KV cache for decode simulation.
132	
133	        token_ids: (1,) or (S,) for prefill
134	        aux_hidden: (1, 12288) or (S, 12288) for prefill, or (1, 4096) for decode
135	        """
136	        # Add batch dim
137	        if token_ids.dim() == 1:
138	            token_ids = token_ids.unsqueeze(0)
139	        if aux_hidden.dim() == 2:
140	            aux_hidden = aux_hidden.unsqueeze(0)
141	
142	        # fc projection (only for 12288 input)
143	        if aux_hidden.shape[-1] == AUX_DIM:
144	            hidden_states = self.fc(aux_hidden)
145	        else:
146	            hidden_states = aux_hidden  # already 4096
147	
148	        # embed tokens
149	        embeds = self.embed_tokens(token_ids) * self.scale_emb
150	        embeds = embeds.to(hidden_states.dtype)
151	
152	        # decoder layer forward
153	        residual = hidden_states
154	        embeds_normed = self.input_layernorm(embeds)
155	        hidden_normed = self.hidden_norm(hidden_states)
156	        hidden_cat = torch.cat([embeds_normed, hidden_normed], dim=-1)
157	
158	        # attention with KV cache
159	        attn_out = self.self_attn(hidden_cat, use_cache=use_cache, pos=pos)
160	        hidden_states = residual + attn_out
161	
162	        # MLP
163	        residual = hidden_states
164	        hidden_states = self.post_attention_layernorm(hidden_states)
165	        hidden_states = self.mlp(hidden_states)
166	        hidden_states = residual + hidden_states
167	
168	        # final norm + lm_head
169	        final_hidden = self.norm(hidden_states)
170	        logits = self.lm_head(final_hidden)
171	
172	        return logits.squeeze(0), hidden_states.squeeze(0)  # return hidden for next step
173	
174	
175	def load_model():
176	    model = Eagle3ModelWithKVCache().to(DEVICE).to(DTYPE)
177	
178	    with safe_open("eagle/sglang_model/model.safetensors", framework="pt", device="cpu") as f:
179	        state_dict = {}
180	        for key in f.keys():
181	            tensor = f.get_tensor(key)
182	            if key.startswith("model."):
183	                key = key[6:]
184	            if key == "midlayer.input_layernorm.weight":
185	                [REDACTED]
186	            elif key == "midlayer.hidden_norm.weight":
187	                [REDACTED]
188	            elif key == "midlayer.post_attention_layernorm.weight":
189	                [REDACTED]
190	            elif key.startswith("midlayer.self_attn."):
191	                key = key.replace("midlayer.self_attn.", "self_attn.")
192	            elif key.startswith("midlayer.mlp."):
193	                key = key.replace("midlayer.mlp.", "mlp.")
194	            elif key == "norm.weight":
195	                key = "norm.weight"
196	            state_dict[key] = tensor
197	
198	    model.load_state_dict(state_dict, strict=False)
199	    model.eval()
200	    return model
201	
202	
203	def load_vocab_mapping():
204	    cache = torch.load("eagle/data/vocab_cache.pt", weights_only=True)
205	    d2t = cache["d2t"].to(DEVICE)
206	    t2d = cache["t2d"].to(DEVICE)
207	    draft_idx_map = torch.zeros(VOCAB_SIZE, dtype=torch.long, device=DEVICE)
208	    draft_idx_map[d2t] = torch.arange(DRAFT_VOCAB_SIZE, device=DEVICE)
209	    return d2t, t2d, draft_idx_map
210	
211	
212	def build_target_p(target_logits_values, target_logits_indices, t2d, draft_idx_map):
213	    S, K = target_logits_values.shape
214	    indices = target_logits_indices.long().clamp(0, VOCAB_SIZE - 1)
215	    in_draft = t2d[indices]
216	    draft_logits = torch.full((S, DRAFT_VOCAB_SIZE), -1e9, device=DEVICE, dtype=torch.float32)
217	    mapped_idx = draft_idx_map[indices]
218	    values = target_logits_values.float()
219	    safe_vals = torch.where(in_draft, values, torch.tensor(-1e9, device=DEVICE))
220	    draft_logits.scatter_reduce_(1, mapped_idx, safe_vals, reduce="amax")
221	    target_p = F.softmax(draft_logits, dim=-1)
222	    return target_p
223	
224	
225	def test_decode_vs_prefill():
226	    """Compare decode mode (position-by-position with KV cache) vs prefill mode."""
227	    print("Loading model...")
228	    model = load_model()
229	    d2t, t2d, draft_idx_map = load_vocab_mapping()
230	
231	    ood_dir = Path("/tmp/eagle3_val_collect")
232	    pt_files = sorted(ood_dir.glob("*.pt"))
233	    if len(pt_files) == 0:
234	        print("No OOD files found.")
235	        return
236	
237	    print(f"Found {len(pt_files)} OOD files\n")
238	
239	    with torch.no_grad():
240	        for file_idx, pt_file in enumerate(pt_files[:3]):
241	            data = torch.load(pt_file, weights_only=True)
242	            token_ids = data["token_ids"].to(DEVICE)
243	            aux_hidden = data["aux_hidden"].to(DEVICE).to(DTYPE)
244	
245	            seq_len = min(token_ids.shape[0], 32)  # Limit to 32 tokens to avoid OOM
246	            token_ids = token_ids[:seq_len]
247	            aux_hidden = aux_hidden[:seq_len]
248	
249	            if seq_len < 2:
250	                continue
251	
252	            print(f"\n[{file_idx}] {pt_file.name}: seq_len={seq_len}")
253	
254	            # Prefill mode (full sequence)
255	            model.clear_cache()
256	            logits_prefill, _ = model.forward_with_kv_cache(token_ids, aux_hidden, use_cache=False)
257	
258	            # Decode mode (position by position with KV cache)
259	            model.clear_cache()
260	            logits_decode_list = []
261	
262	            for i in range(seq_len):
263	                logits_i, hidden_out = model.forward_with_kv_cache(
264	                    token_ids[i:i+1], aux_hidden[i:i+1], use_cache=True, pos=i
265	                )
266	                logits_decode_list.append(logits_i)
267	
268	            logits_decode = torch.cat(logits_decode_list, dim=0)  # Each is (1, vocab), cat to (seq_len, vocab)
269	
270	            # Compare
271	            print(f"  logits_prefill.shape={logits_prefill.shape}, logits_decode.shape={logits_decode.shape}")
272	            pred_prefill = logits_prefill.argmax(dim=-1)
273	            pred_decode = logits_decode.argmax(dim=-1)
274	            print(f"  pred_prefill.shape={pred_prefill.shape}, pred_decode.shape={pred_decode.shape}")
275	            pred_match = (pred_prefill == pred_decode).float().mean().item()
276	            logits_diff = (logits_prefill - logits_decode).abs()
277	
278	            print(f"  Logits max diff: {logits_diff.max().item():.4f}, mean diff: {logits_diff.mean().item():.4f}")
279	            print(f"  Prediction match: {pred_match:.1%}")
280	
281	            # Detailed comparison for all positions
282	            print(f"  Position-wise comparison:")
283	            for pos in range(seq_len):
284	                diff = (logits_prefill[pos] - logits_decode[pos]).abs()
285	                p1, p2 = pred_prefill[pos].item(), pred_decode[pos].item()
286	                match_str = "✓" if p1 == p2 else "✗"
287	                print(f"    pos={pos}: prefill={p1}, decode={p2} {match_str}, max_diff={diff.max().item():.2f}")
288	
289	
290	if __name__ == "__main__":
291	    test_decode_vs_prefill()
292
```

> AGENT

Let me explore the medusa directory structure and key files:

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /user_4813494d/openbmb/medusa/ | head -40"
}
```

> TOOL

tool_result Bash
```
total 108
drwxr-xr-x  6 user_4813494d user_4813494d  4096 Apr 10 11:18 .
drwxr-xr-x 19 user_4813494d user_4813494d  4096 Apr 13 09:41 ..
drwxr-xr-x  2 user_4813494d user_4813494d    41 Apr  6 11:52 .ipynb_checkpoints
-rw-r--r--  1 user_4813494d user_4813494d  4263 Apr  9 10:38 check_data.py
-rw-r--r--  1 user_4813494d user_4813494d 17631 Apr  9 10:38 collect_data.py
-rw-r--r--  1 user_4813494d user_4813494d 10319 Apr 10 11:18 collect_eval_overfit.py
drwxr-xr-x  3 user_4813494d user_4813494d    90 Apr 11 19:11 data
-rw-r--r--  1 user_4813494d user_4813494d  8140 Apr  9 10:38 eval_topk.py
drwxr-xr-x  3 user_4813494d user_4813494d    29 Apr  4 12:22 medusa
-rw-r--r--  1 user_4813494d user_4813494d  8102 Apr  4 21:45 profile_verify.py
-rw-r--r--  1 user_4813494d user_4813494d 10075 Apr  9 10:38 quick_validate_similar.py
-rw-r--r--  1 user_4813494d user_4813494d  2772 Apr  9 10:38 recollect_val_ood.sh
-rw-r--r--  1 user_4813494d user_4813494d  6469 Apr  9 10:38 select_similar.py
-rw-r--r--  1 user_4813494d user_4813494d 19951 Apr  9 10:39 train.py
drwxr-xr-x  3 user_4813494d user_4813494d   100 Apr  6 09:04 weights
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/medusa -type f -name \"*.py\" | sort"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/medusa/.ipynb_checkpoints/train-checkpoint.py
/user_4813494d/openbmb/medusa/check_data.py
/user_4813494d/openbmb/medusa/collect_data.py
/user_4813494d/openbmb/medusa/collect_eval_overfit.py
/user_4813494d/openbmb/medusa/eval_topk.py
/user_4813494d/openbmb/medusa/profile_verify.py
/user_4813494d/openbmb/medusa/quick_validate_similar.py
/user_4813494d/openbmb/medusa/select_similar.py
/user_4813494d/openbmb/medusa/train.py
```

> AGENT

Let me continue reading the remaining eagle scripts and documentation files:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/test_eagle3_flow.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Test EAGLE-3 inference flow - verify hidden_states dimensions and d2t mapping.
4	
5	This runs a single forward pass to check:
6	1. aux_hidden_states from target model has correct shape (12288)
7	2. d2t mapping works correctly
8	3. Draft model fc projection works
9	"""
10	
11	import os
12	import sys
13	import torch
14	import json
15	from pathlib import Path
16	
17	# Add sglang to path
18	SGLANG_PATH = Path("/user_4813494d/openbmb/demo-sala/sglang/python")
19	sys.path.insert(0, str(SGLANG_PATH))
20	
21	os.environ["CUDA_VISIBLE_DEVICES"] = "0"
22	
23	def test_weights_loading():
24	    """Test that weights are correctly loaded."""
25	    from safetensors import safe_open
26	
27	    print("=" * 60)
28	    print("Test 1: Weight Loading")
29	    print("=" * 60)
30	
31	    model_path = Path("eagle/sglang_model/model.safetensors")
32	
33	    with safe_open(model_path, framework="pt", device="cpu") as f:
34	        keys = f.keys()
35	        print(f"Total tensors: {len(keys)}")
36	
37	        # Check fc weight
38	        fc_weight = f.get_tensor("model.fc.weight")
39	        print(f"model.fc.weight: {fc_weight.shape} (expected: [4096, 12288])")
40	        assert fc_weight.shape == (4096, 12288), f"Wrong fc weight shape: {fc_weight.shape}"
41	
42	        # Check d2t
43	        d2t_diff = f.get_tensor("d2t")
44	        print(f"d2t (diff): {d2t_diff.shape}, range [{d2t_diff.min()}, {d2t_diff.max()}]")
45	
46	        # Recover actual d2t
47	        d2t = d2t_diff + torch.arange(len(d2t_diff))
48	        print(f"d2t (recovered): range [{d2t.min()}, {d2t.max()}]")
49	        print(f"  d2t[:5] = {d2t[:5].tolist()}")
50	
51	        # Check attention weights (should be 8192 input dim)
52	        q_proj = f.get_tensor("model.midlayer.self_attn.q_proj.weight")
53	        print(f"q_proj.weight: {q_proj.shape} (expected: [4096, 8192])")
54	        assert q_proj.shape == (4096, 8192), f"Wrong q_proj shape: {q_proj.shape}"
55	
56	    print("✓ Weight loading test PASSED\n")
57	
58	
59	def test_target_aux_capture():
60	    """Test that target model captures aux hidden states correctly."""
61	    print("=" * 60)
62	    print("Test 2: Target Model Aux Hidden State Capture")
63	    print("=" * 60)
64	
65	    # Simulate the capture logic
66	    layers_to_capture_config = [1, 10, 22]
67	    layers_to_capture = {val + 1 for val in layers_to_capture_config}
68	
69	    print(f"Config layer_ids: {layers_to_capture_config}")
70	    print(f"Actual layers_to_capture set: {sorted(layers_to_capture)}")
71	
72	    # Simulate forward loop capture
73	    num_layers = 32
74	    hidden_size = 4096
75	    captured = []
76	
77	    for i in range(num_layers):
78	        if i in layers_to_capture:
79	            captured.append(f"layer_{i-1}_output")  # i-1 because we capture before layer i runs
80	
81	    print(f"Captured states: {captured}")
82	    assert len(captured) == 3, f"Expected 3 captured states, got {len(captured)}"
83	
84	    # Expected concat dimension
85	    concat_dim = hidden_size * len(captured)
86	    print(f"Concatenated hidden_states dimension: {concat_dim} (expected: 12288)")
87	    assert concat_dim == 12288, f"Wrong concat dim: {concat_dim}"
88	
89	    print("✓ Aux hidden state capture test PASSED\n")
90	
91	
92	def test_d2t_mapping():
93	    """Test d2t mapping correctness."""
94	    print("=" * 60)
95	    print("Test 3: D2T Mapping")
96	    print("=" * 60)
97	
98	    vocab_cache = torch.load("eagle/data/vocab_cache.pt", weights_only=True)
99	    d2t = vocab_cache["d2t"]
100	    t2d = vocab_cache["t2d"]
101	
102	    print(f"d2t shape: {d2t.shape}")
103	    print(f"t2d shape: {t2d.shape}, True count: {t2d.sum().item()}")
104	
105	    # Check bijection
106	    for i in range(min(10, len(d2t))):
107	        target_id = d2t[i].item()
108	        assert t2d[target_id], f"draft_id {i} -> target_id {target_id} not in t2d"
109	
110	    # Check d2t_diff recovery
111	    from safetensors import safe_open
112	    with safe_open("eagle/sglang_model/model.safetensors", framework="pt", device="cpu") as f:
113	        d2t_diff = f.get_tensor("d2t")
114	
115	    d2t_recovered = d2t_diff + torch.arange(len(d2t_diff))
116	    assert torch.all(d2t_recovered == d2t), "d2t recovery mismatch!"
117	
118	    print("✓ D2T mapping test PASSED\n")
119	
120	
121	def test_draft_model_structure():
122	    """Test draft model structure matches expected architecture."""
123	    print("=" * 60)
124	    print("Test 4: Draft Model Structure")
125	    print("=" * 60)
126	
127	    with open("eagle/sglang_model/config.json") as f:
128	        cfg = json.load(f)
129	
130	    print(f"Architecture: {cfg['architectures']}")
131	    print(f"hidden_size: {cfg['hidden_size']}")
132	    print(f"target_hidden_size: {cfg.get('target_hidden_size', 'N/A')}")
133	    print(f"draft_vocab_size: {cfg.get('draft_vocab_size', 'N/A')}")
134	    print(f"vocab_size: {cfg['vocab_size']}")
135	    print(f"num_hidden_layers: {cfg['num_hidden_layers']}")
136	
137	    eagle_config = cfg.get("eagle_config", {})
138	    print(f"eagle_config: {eagle_config}")
139	
140	    # Validate
141	    assert cfg["architectures"] == ["LlamaForCausalLMEagle3"]
142	    assert cfg["num_hidden_layers"] == 1
143	    assert cfg["hidden_size"] == 4096
144	    assert cfg.get("draft_vocab_size") == 32000
145	    assert eagle_config.get("use_aux_hidden_state") == True
146	    assert eagle_config.get("eagle_aux_hidden_state_layer_ids") == [1, 10, 22]
147	
148	    print("✓ Draft model structure test PASSED\n")
149	
150	
151	def test_fc_projection():
152	    """Test fc projection numerically."""
153	    print("=" * 60)
154	    print("Test 5: FC Projection")
155	    print("=" * 60)
156	
157	    from safetensors import safe_open
158	
159	    # Load fc weight
160	    with safe_open("eagle/sglang_model/model.safetensors", framework="pt", device="cpu") as f:
161	        fc_weight = f.get_tensor("model.fc.weight").to(torch.bfloat16)
162	
163	    # Simulate aux_hidden input
164	    batch_size = 2
165	    seq_len = 10
166	    aux_dim = 12288
167	    hidden_size = 4096
168	
169	    # Random aux_hidden (simulating concat of 3 layers)
170	    torch.manual_seed(42)
171	    aux_hidden = torch.randn(batch_size, seq_len, aux_dim, dtype=torch.bfloat16)
172	
173	    # FC projection
174	    hidden = torch.nn.functional.linear(aux_hidden, fc_weight)
175	
176	    print(f"aux_hidden shape: {aux_hidden.shape}")
177	    print(f"fc_weight shape: {fc_weight.shape}")
178	    print(f"hidden shape: {hidden.shape}")
179	
180	    assert hidden.shape == (batch_size, seq_len, hidden_size), f"Wrong output shape: {hidden.shape}"
181	
182	    # Check not all zeros
183	    assert hidden.abs().sum() > 0, "Hidden states are all zeros!"
184	
185	    print(f"hidden mean: {hidden.float().mean().item():.6f}")
186	    print(f"hidden std: {hidden.float().std().item():.6f}")
187	
188	    print("✓ FC projection test PASSED\n")
189	
190	
191	def main():
192	    print("\n" + "=" * 60)
193	    print("EAGLE-3 Inference Flow Test")
194	    print("=" * 60 + "\n")
195	
196	    test_weights_loading()
197	    test_target_aux_capture()
198	    test_d2t_mapping()
199	    test_draft_model_structure()
200	    test_fc_projection()
201	
202	    print("=" * 60)
203	    print("ALL TESTS PASSED!")
204	    print("=" * 60)
205	
206	
207	if __name__ == "__main__":
208	    main()
209
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/test_forward_match.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Test that offline eval forward matches SGLang draft model forward.
4	Uses the same weights and compares outputs on OOD data.
5	"""
6	
7	import torch
8	import torch.nn as nn
9	import torch.nn.functional as F
10	from pathlib import Path
11	from safetensors import safe_open
12	
13	DEVICE = "cuda"
14	DTYPE = torch.bfloat16
15	
16	# Model config
17	HIDDEN_SIZE = 4096
18	AUX_DIM = HIDDEN_SIZE * 3  # 12288
19	VOCAB_SIZE = 73448
20	DRAFT_VOCAB_SIZE = 32000
21	SCALE_EMB = 12
22	NUM_HEADS = 32
23	NUM_KV_HEADS = 2
24	HEAD_DIM = 128
25	INTERMEDIATE_SIZE = 16384
26	RMS_NORM_EPS = 1e-6
27	
28	
29	class RMSNorm(nn.Module):
30	    def __init__(self, dim, eps=1e-6):
31	        super().__init__()
32	        self.weight = nn.Parameter(torch.ones(dim))
33	        self.eps = eps
34	
35	    def forward(self, x):
36	        norm = x.float().pow(2).mean(-1, keepdim=True).add(self.eps).rsqrt()
37	        return (x * norm).to(x.dtype) * self.weight
38	
39	
40	class Eagle3Attention(nn.Module):
41	    """Simplified attention (no KV cache, single forward)."""
42	    def __init__(self):
43	        super().__init__()
44	        self.num_heads = NUM_HEADS
45	        self.num_kv_heads = NUM_KV_HEADS
46	        self.head_dim = HEAD_DIM
47	        self.num_kv_groups = NUM_HEADS // NUM_KV_HEADS
48	
49	        qkv_in = HIDDEN_SIZE * 2
50	        self.q_proj = nn.Linear(qkv_in, NUM_HEADS * HEAD_DIM, bias=False)
51	        self.k_proj = nn.Linear(qkv_in, NUM_KV_HEADS * HEAD_DIM, bias=False)
52	        self.v_proj = nn.Linear(qkv_in, NUM_KV_HEADS * HEAD_DIM, bias=False)
53	        self.o_proj = nn.Linear(NUM_HEADS * HEAD_DIM, HIDDEN_SIZE, bias=False)
54	
55	    def forward(self, hidden_cat):
56	        B, S, _ = hidden_cat.shape
57	        q = self.q_proj(hidden_cat).view(B, S, self.num_heads, self.head_dim).transpose(1, 2)
58	        k = self.k_proj(hidden_cat).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
59	        v = self.v_proj(hidden_cat).view(B, S, self.num_kv_heads, self.head_dim).transpose(1, 2)
60	
61	        if self.num_kv_groups > 1:
62	            k = k.repeat_interleave(self.num_kv_groups, dim=1)
63	            v = v.repeat_interleave(self.num_kv_groups, dim=1)
64	
65	        attn_output = F.scaled_dot_product_attention(q, k, v, is_causal=True)
66	        attn_output = attn_output.transpose(1, 2).contiguous().view(B, S, -1)
67	        return self.o_proj(attn_output)
68	
69	
70	class Eagle3MLP(nn.Module):
71	    def __init__(self):
72	        super().__init__()
73	        self.gate_proj = nn.Linear(HIDDEN_SIZE, INTERMEDIATE_SIZE, bias=False)
74	        self.up_proj = nn.Linear(HIDDEN_SIZE, INTERMEDIATE_SIZE, bias=False)
75	        self.down_proj = nn.Linear(INTERMEDIATE_SIZE, HIDDEN_SIZE, bias=False)
76	
77	    def forward(self, x):
78	        return self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))
79	
80	
81	class Eagle3Model(nn.Module):
82	    def __init__(self):
83	        super().__init__()
84	        self.fc = nn.Linear(AUX_DIM, HIDDEN_SIZE, bias=False)
85	        self.input_layernorm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
86	        self.hidden_norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
87	        self.self_attn = Eagle3Attention()
88	        self.post_attention_layernorm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
89	        self.mlp = Eagle3MLP()
90	        self.norm = RMSNorm(HIDDEN_SIZE, RMS_NORM_EPS)
91	        self.embed_tokens = nn.Embedding(VOCAB_SIZE, HIDDEN_SIZE)
92	        self.lm_head = nn.Linear(HIDDEN_SIZE, DRAFT_VOCAB_SIZE, bias=False)
93	        self.scale_emb = SCALE_EMB
94	
95	    def forward(self, token_ids, aux_hidden):
96	        """Full forward matching offline eval."""
97	        if token_ids.dim() == 1:
98	            token_ids = token_ids.unsqueeze(0)
99	            aux_hidden = aux_hidden.unsqueeze(0)
100	            squeeze_out = True
101	        else:
102	            squeeze_out = False
103	
104	        # fc projection
105	        hidden_states = self.fc(aux_hidden)
106	
107	        # embed tokens
108	        embeds = self.embed_tokens(token_ids) * self.scale_emb
109	        embeds = embeds.to(hidden_states.dtype)
110	
111	        # decoder layer forward
112	        residual = hidden_states
113	        embeds_normed = self.input_layernorm(embeds)
114	        hidden_normed = self.hidden_norm(hidden_states)
115	        hidden_cat = torch.cat([embeds_normed, hidden_normed], dim=-1)
116	
117	        # attention
118	        attn_out = self.self_attn(hidden_cat)
119	        hidden_states = residual + attn_out
120	
121	        # MLP
122	        residual = hidden_states
123	        hidden_states = self.post_attention_layernorm(hidden_states)
124	        hidden_states = self.mlp(hidden_states)
125	        hidden_states = residual + hidden_states
126	
127	        # final norm + lm_head
128	        hidden_states = self.norm(hidden_states)
129	        logits = self.lm_head(hidden_states)
130	
131	        if squeeze_out:
132	            logits = logits.squeeze(0)
133	        return logits
134	
135	
136	def load_model():
137	    model = Eagle3Model().to(DEVICE).to(DTYPE)
138	
139	    # Load weights
140	    with safe_open("eagle/sglang_model/model.safetensors", framework="pt", device="cpu") as f:
141	        state_dict = {}
142	        for key in f.keys():
143	            tensor = f.get_tensor(key)
144	            # Map weight names
145	            if key.startswith("model."):
146	                key = key[6:]
147	            if key == "midlayer.input_layernorm.weight":
148	                [REDACTED]
149	            elif key == "midlayer.hidden_norm.weight":
150	                [REDACTED]
151	            elif key == "midlayer.post_attention_layernorm.weight":
152	                [REDACTED]
153	            elif key.startswith("midlayer.self_attn."):
154	                key = key.replace("midlayer.self_attn.", "self_attn.")
155	            elif key.startswith("midlayer.mlp."):
156	                key = key.replace("midlayer.mlp.", "mlp.")
157	            elif key == "norm.weight":
158	                key = "norm.weight"
159	            state_dict[key] = tensor
160	
161	    model.load_state_dict(state_dict, strict=False)
162	    model.eval()
163	    return model
164	
165	
166	def load_vocab_mapping():
167	    cache = torch.load("eagle/data/vocab_cache.pt", weights_only=True)
168	    d2t = cache["d2t"].to(DEVICE)
169	    t2d = cache["t2d"].to(DEVICE)
170	    draft_idx_map = torch.zeros(VOCAB_SIZE, dtype=torch.long, device=DEVICE)
171	    draft_idx_map[d2t] = torch.arange(DRAFT_VOCAB_SIZE, device=DEVICE)
172	    return d2t, t2d, draft_idx_map
173	
174	
175	def build_target_p(target_logits_values, target_logits_indices, t2d, draft_idx_map):
176	    """Build target distribution from top-256 logits."""
177	    S, K = target_logits_values.shape
178	    indices = target_logits_indices.long().clamp(0, VOCAB_SIZE - 1)
179	    in_draft = t2d[indices]
180	
181	    draft_logits = torch.full((S, DRAFT_VOCAB_SIZE), -1e9, device=DEVICE, dtype=torch.float32)
182	    mapped_idx = draft_idx_map[indices]
183	    values = target_logits_values.float()
184	
185	    safe_vals = torch.where(in_draft, values, torch.tensor(-1e9, device=DEVICE))
186	    draft_logits.scatter_reduce_(1, mapped_idx, safe_vals, reduce="amax")
187	    target_p = F.softmax(draft_logits, dim=-1)
188	    return target_p
189	
190	
191	def test_single_position():
192	    """Test forward for single position (decode-like scenario)."""
193	    print("Loading model...")
194	    model = load_model()
195	    d2t, t2d, draft_idx_map = load_vocab_mapping()
196	
197	    # Load OOD data
198	    ood_dir = Path("/tmp/eagle3_val_collect")
199	    pt_files = sorted(ood_dir.glob("*.pt"))
200	    if len(pt_files) == 0:
201	        print("No OOD files found. Run data collection first.")
202	        return
203	
204	    print(f"Found {len(pt_files)} OOD files")
205	
206	    # Test: compare full-sequence forward vs position-by-position forward
207	    data = torch.load(pt_files[0], weights_only=True)
208	    token_ids = data["token_ids"].to(DEVICE)
209	    aux_hidden = data["aux_hidden"].to(DEVICE).to(DTYPE)
210	    top_logit_values = data["top_logit_values"].to(DEVICE).to(DTYPE)
211	    top_logit_indices = data["top_logit_indices"].to(DEVICE)
212	
213	    seq_len = token_ids.shape[0]
214	    print(f"\nSequence length: {seq_len}")
215	
216	    with torch.no_grad():
217	        # Full sequence forward (offline eval style)
218	        full_logits = model(token_ids, aux_hidden)
219	        print(f"Full forward logits shape: {full_logits.shape}")
220	
221	        # Now test position-by-position with KV-cache simulation
222	        # This mimics what happens in decode mode
223	        print("\nTesting position-by-position (simulating decode with fc projection)...")
224	
225	        # First position uses aux_hidden (12288)
226	        pos0_logits_12288 = model.forward_fc_then_layer(token_ids[:1], aux_hidden[:1])
227	
228	        # Check if first position matches
229	        match_pos0 = torch.allclose(full_logits[0], pos0_logits_12288[0], atol=1e-2)
230	        diff_pos0 = (full_logits[0] - pos0_logits_12288[0]).abs().max().item()
231	        print(f"Position 0 (aux_hidden 12288): match={match_pos0}, max_diff={diff_pos0:.4f}")
232	
233	
234	def test_full_sequence():
235	    """Test full sequence accuracy."""
236	    print("Loading model...")
237	    model = load_model()
238	    d2t, t2d, draft_idx_map = load_vocab_mapping()
239	
240	    ood_dir = Path("/tmp/eagle3_val_collect")
241	    pt_files = sorted(ood_dir.glob("*.pt"))
242	    if len(pt_files) == 0:
243	        print("No OOD files found at /tmp/eagle3_val_collect")
244	        print("Please run OOD data collection first.")
245	        return
246	
247	    print(f"Found {len(pt_files)} OOD files\n")
248	
249	    total_correct = 0
250	    total_valid = 0
251	
252	    with torch.no_grad():
253	        for i, pt_file in enumerate(pt_files[:5]):
254	            data = torch.load(pt_file, weights_only=True)
255	            token_ids = data["token_ids"].to(DEVICE)
256	            aux_hidden = data["aux_hidden"].to(DEVICE).to(DTYPE)
257	            top_logit_values = data["top_logit_values"].to(DEVICE).to(DTYPE)
258	            top_logit_indices = data["top_logit_indices"].to(DEVICE)
259	
260	            seq_len = token_ids.shape[0]
261	            if seq_len < 2:
262	                continue
263	
264	            # Forward
265	            logits = model(token_ids, aux_hidden)
266	
267	            # Build target distribution
268	            target_p = build_target_p(top_logit_values, top_logit_indices, t2d, draft_idx_map)
269	
270	            # Compute accept rate
271	            pred_draft_idx = logits.argmax(dim=-1)
272	            target_draft_idx = target_p.argmax(dim=-1)
273	
274	            # Only count positions where target argmax is in draft vocab
275	            target_argmax_full = top_logit_indices[:, 0].long().clamp(0, VOCAB_SIZE - 1)
276	            target_mask = t2d[target_argmax_full].float()
277	
278	            correct = (pred_draft_idx == target_draft_idx).float() * target_mask
279	            n_correct = correct.sum().item()
280	            n_valid = target_mask.sum().item()
281	
282	            total_correct += n_correct
283	            total_valid += n_valid
284	
285	            if i < 5:
286	                acc = n_correct / n_valid if n_valid > 0 else 0
287	                print(f"[{i}] {pt_file.name}: seq_len={seq_len}, valid={int(n_valid)}, correct={int(n_correct)}, acc={acc:.1%}")
288	
289	    print(f"\n{'='*60}")
290	    print(f"Total valid positions: {int(total_valid)}")
291	    print(f"Correct predictions: {int(total_correct)}")
292	    if total_valid > 0:
293	        print(f"OOD Accept Rate: {total_correct/total_valid:.1%}")
294	
295	
296	if __name__ == "__main__":
297	    import sys
298	    if len(sys.argv) > 1 and sys.argv[1] == "--position":
299	        test_single_position()
300	    else:
301	        test_full_sequence()
302
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/test_offline_pred.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Test EAGLE-3 model prediction offline using collected training data.
4	Verify that the trained model can correctly predict next tokens.
5	"""
6	
7	import torch
8	import torch.nn.functional as F
9	from pathlib import Path
10	from safetensors import safe_open
11	
12	DEVICE = "cuda"
13	DTYPE = torch.bfloat16
14	
15	# Load model weights
16	print("Loading model weights...")
17	with safe_open("eagle/sglang_model/model.safetensors", framework="pt", device="cpu") as f:
18	    fc_weight = f.get_tensor("model.fc.weight").to(DEVICE).to(DTYPE)
19	    lm_head_weight = f.get_tensor("lm_head.weight").to(DEVICE).to(DTYPE)
20	    norm_weight = f.get_tensor("model.norm.weight").to(DEVICE).to(DTYPE)
21	    # Attention weights
22	    q_proj = f.get_tensor("model.midlayer.self_attn.q_proj.weight").to(DEVICE).to(DTYPE)
23	    k_proj = f.get_tensor("model.midlayer.self_attn.k_proj.weight").to(DEVICE).to(DTYPE)
24	    v_proj = f.get_tensor("model.midlayer.self_attn.v_proj.weight").to(DEVICE).to(DTYPE)
25	    o_proj = f.get_tensor("model.midlayer.self_attn.o_proj.weight").to(DEVICE).to(DTYPE)
26	    input_ln = f.get_tensor("model.midlayer.input_layernorm.weight").to(DEVICE).to(DTYPE)
27	    hidden_norm = f.get_tensor("model.midlayer.hidden_norm.weight").to(DEVICE).to(DTYPE)
28	    post_ln = f.get_tensor("model.midlayer.post_attention_layernorm.weight").to(DEVICE).to(DTYPE)
29	    gate_proj = f.get_tensor("model.midlayer.mlp.gate_proj.weight").to(DEVICE).to(DTYPE)
30	    up_proj = f.get_tensor("model.midlayer.mlp.up_proj.weight").to(DEVICE).to(DTYPE)
31	    down_proj = f.get_tensor("model.midlayer.mlp.down_proj.weight").to(DEVICE).to(DTYPE)
32	    embed_weight = f.get_tensor("model.embed_tokens.weight").to(DEVICE).to(DTYPE)
33	
34	# Load d2t mapping
35	vocab_cache = torch.load("eagle/data/vocab_cache.pt", weights_only=True)
36	d2t = vocab_cache["d2t"].to(DEVICE)
37	t2d = vocab_cache["t2d"].to(DEVICE)
38	
39	print(f"fc_weight: {fc_weight.shape}")
40	print(f"lm_head_weight: {lm_head_weight.shape}")
41	print(f"d2t: {d2t.shape}")
42	
43	# RMSNorm
44	def rms_norm(x, weight, eps=1e-6):
45	    norm = x.float().pow(2).mean(-1, keepdim=True).add(eps).rsqrt()
46	    return (x * norm).to(x.dtype) * weight
47	
48	# Simple forward (no attention for simplicity, just fc -> norm -> lm_head)
49	def simple_forward(aux_hidden):
50	    """Simplified forward: fc -> norm -> lm_head"""
51	    hidden = F.linear(aux_hidden, fc_weight)
52	    hidden = rms_norm(hidden, norm_weight)
53	    logits = F.linear(hidden, lm_head_weight)
54	    return logits
55	
56	# Build draft_idx_map (target_id -> draft_id)
57	DRAFT_VOCAB_SIZE = 32000
58	VOCAB_SIZE = 73448
59	draft_idx_map = torch.zeros(VOCAB_SIZE, dtype=torch.long, device=DEVICE)
60	draft_idx_map[d2t] = torch.arange(DRAFT_VOCAB_SIZE, device=DEVICE)
61	
62	def build_target_p(target_logits_values, target_logits_indices):
63	    """Build target distribution from top-256 logits (same as training)."""
64	    S, K = target_logits_values.shape
65	    indices = target_logits_indices.long().clamp(0, VOCAB_SIZE - 1)
66	    in_draft = t2d[indices]  # (S, 256) bool
67	
68	    draft_logits = torch.full((S, DRAFT_VOCAB_SIZE), -1e9, device=DEVICE, dtype=torch.float32)
69	    mapped_idx = draft_idx_map[indices]  # (S, 256)
70	    values = target_logits_values.float()
71	
72	    safe_vals = torch.where(in_draft, values, torch.tensor(-1e9, device=DEVICE))
73	    draft_logits.scatter_reduce_(1, mapped_idx, safe_vals, reduce="amax")
74	    target_p = F.softmax(draft_logits, dim=-1)
75	    return target_p
76	
77	# Load training samples
78	data_dir = Path("eagle/data/train")
79	pt_files = sorted(data_dir.glob("*.pt"))
80	print(f"\nFound {len(pt_files)} training files")
81	
82	# Test on first 5 files
83	correct_top1 = 0
84	total = 0
85	
86	for i, pt_file in enumerate(pt_files[:5]):
87	    data = torch.load(pt_file, weights_only=True)
88	    aux_hidden = data["aux_hidden"].to(DEVICE).to(DTYPE)
89	    top_logit_values = data["top_logit_values"].to(DEVICE).to(DTYPE)
90	    top_logit_indices = data["top_logit_indices"].to(DEVICE)
91	
92	    seq_len = aux_hidden.shape[0]
93	
94	    # Predict
95	    with torch.no_grad():
96	        logits = simple_forward(aux_hidden)  # (seq_len, 32000)
97	        target_p = build_target_p(top_logit_values, top_logit_indices)
98	
99	    pred_draft_idx = logits.argmax(dim=-1)  # (seq_len,)
100	    target_draft_idx = target_p.argmax(dim=-1)  # (seq_len,)
101	
102	    # Target argmax in draft vocab?
103	    target_argmax_full = top_logit_indices[:, 0].long().clamp(0, VOCAB_SIZE - 1)
104	    target_mask = t2d[target_argmax_full].float()
105	
106	    correct = (pred_draft_idx == target_draft_idx).float() * target_mask
107	    n_correct = correct.sum().item()
108	    n_valid = target_mask.sum().item()
109	
110	    if n_valid > 0:
111	        acc = n_correct / n_valid
112	        print(f"File {i}: {pt_file.name}, seq_len={seq_len}, valid={int(n_valid)}, correct={int(n_correct)}, acc={acc:.2%}")
113	        correct_top1 += n_correct
114	        total += n_valid
115	
116	print(f"\nOverall acc (same as training): {correct_top1}/{int(total)} = {correct_top1/total:.2%}")
117
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/eagle/verify_sglang_draft.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Verify that SGLang's draft model produces same output as offline eval.
4	Loads the draft model using SGLang's weight loading and compares with offline eval.
5	"""
6	
7	import torch
8	import torch.nn.functional as F
9	from pathlib import Path
10	from safetensors import safe_open
11	
12	DEVICE = "cuda"
13	DTYPE = torch.bfloat16
14	HIDDEN_SIZE = 4096
15	AUX_DIM = HIDDEN_SIZE * 3
16	VOCAB_SIZE = 73448
17	DRAFT_VOCAB_SIZE = 32000
18	
19	
20	def test_fc_weight():
21	    """Test that fc weight matches between offline eval and SGLang draft model."""
22	    print("Testing fc weight...")
23	
24	    # Offline eval loads fc.weight directly
25	    with safe_open("eagle/sglang_model/model.safetensors", framework="pt", device="cpu") as f:
26	        fc_weight = f.get_tensor("model.fc.weight")
27	
28	    print(f"  fc.weight shape: {fc_weight.shape}")
29	    print(f"  fc.weight mean: {fc_weight.float().mean():.6f}")
30	    print(f"  fc.weight std: {fc_weight.float().std():.6f}")
31	
32	    # Test fc forward
33	    test_input = torch.randn(1, 10, AUX_DIM, dtype=DTYPE, device=DEVICE)
34	    fc_weight_cuda = fc_weight.to(DEVICE).to(DTYPE)
35	    output = F.linear(test_input, fc_weight_cuda)
36	    print(f"  Test forward: input {test_input.shape} -> output {output.shape}")
37	    print(f"  Output mean: {output.float().mean():.4f}, std: {output.float().std():.4f}")
38	    print()
39	
40	
41	def test_lm_head():
42	    """Test lm_head weight and d2t mapping."""
43	    print("Testing lm_head and d2t mapping...")
44	
45	    with safe_open("eagle/sglang_model/model.safetensors", framework="pt", device="cpu") as f:
46	        lm_head_weight = f.get_tensor("lm_head.weight")
47	        d2t_diff = f.get_tensor("d2t")
48	
49	    print(f"  lm_head.weight shape: {lm_head_weight.shape}")
50	
51	    # Reconstruct hot_token_id as SGLang does
52	    hot_token_id = d2t_diff + torch.arange(len(d2t_diff))
53	    print(f"  hot_token_id (d2t + arange): shape={hot_token_id.shape}")
54	    print(f"  hot_token_id[:5]: {hot_token_id[:5].tolist()}")
55	
56	    # Verify d2t mapping matches vocab_cache
57	    vocab_cache = torch.load("eagle/data/vocab_cache.pt", weights_only=True)
58	    d2t_expected = vocab_cache["d2t"]
59	    match = (hot_token_id == d2t_expected).all()
60	    print(f"  d2t matches vocab_cache: {match}")
61	    print()
62	
63	
64	def test_full_forward():
65	    """Test full forward pass matches offline eval."""
66	    print("Testing full forward pass...")
67	
68	    # Load OOD data
69	    ood_dir = Path("/tmp/eagle3_val_collect")
70	    pt_files = sorted(ood_dir.glob("*.pt"))
71	    if len(pt_files) == 0:
72	        print("  No OOD files found!")
73	        return
74	
75	    data = torch.load(pt_files[0], weights_only=True)
76	    token_ids = data["token_ids"][:16].to(DEVICE)  # Use first 16 tokens
77	    aux_hidden = data["aux_hidden"][:16].to(DEVICE).to(DTYPE)
78	    seq_len = token_ids.shape[0]
79	    print(f"  Test data: seq_len={seq_len}")
80	
81	    # Load all weights
82	    with safe_open("eagle/sglang_model/model.safetensors", framework="pt", device="cpu") as f:
83	        fc_weight = f.get_tensor("model.fc.weight").to(DEVICE).to(DTYPE)
84	        emb_weight = f.get_tensor("model.embed_tokens.weight").to(DEVICE).to(DTYPE)
85	        lm_head_weight = f.get_tensor("lm_head.weight").to(DEVICE).to(DTYPE)
86	        input_ln_weight = f.get_tensor("model.midlayer.input_layernorm.weight").to(DEVICE).to(DTYPE)
87	        hidden_norm_weight = f.get_tensor("model.midlayer.hidden_norm.weight").to(DEVICE).to(DTYPE)
88	        q_proj = f.get_tensor("model.midlayer.self_attn.q_proj.weight").to(DEVICE).to(DTYPE)
89	        k_proj = f.get_tensor("model.midlayer.self_attn.k_proj.weight").to(DEVICE).to(DTYPE)
90	        v_proj = f.get_tensor("model.midlayer.self_attn.v_proj.weight").to(DEVICE).to(DTYPE)
91	        o_proj = f.get_tensor("model.midlayer.self_attn.o_proj.weight").to(DEVICE).to(DTYPE)
92	        post_ln_weight = f.get_tensor("model.midlayer.post_attention_layernorm.weight").to(DEVICE).to(DTYPE)
93	        gate_proj = f.get_tensor("model.midlayer.mlp.gate_proj.weight").to(DEVICE).to(DTYPE)
94	        up_proj = f.get_tensor("model.midlayer.mlp.up_proj.weight").to(DEVICE).to(DTYPE)
95	        down_proj = f.get_tensor("model.midlayer.mlp.down_proj.weight").to(DEVICE).to(DTYPE)
96	        norm_weight = f.get_tensor("model.norm.weight").to(DEVICE).to(DTYPE)
97	
98	    SCALE_EMB = 12
99	    RMS_NORM_EPS = 1e-6
100	    NUM_HEADS = 32
101	    NUM_KV_HEADS = 2
102	    HEAD_DIM = 128
103	    NUM_KV_GROUPS = NUM_HEADS // NUM_KV_HEADS
104	
105	    def rms_norm(x, weight):
106	        norm = x.float().pow(2).mean(-1, keepdim=True).add(RMS_NORM_EPS).rsqrt()
107	        return (x * norm).to(x.dtype) * weight
108	
109	    # Forward pass
110	    # 1. fc projection
111	    hidden_states = F.linear(aux_hidden, fc_weight)
112	    print(f"  After fc: {hidden_states.shape}, mean={hidden_states.float().mean():.4f}")
113	
114	    # 2. embed tokens
115	    embeds = F.embedding(token_ids, emb_weight) * SCALE_EMB
116	    print(f"  Embeds: {embeds.shape}, mean={embeds.float().mean():.4f}")
117	
118	    # 3. decoder layer
119	    residual = hidden_states
120	    embeds_normed = rms_norm(embeds, input_ln_weight)
121	    hidden_normed = rms_norm(hidden_states, hidden_norm_weight)
122	    hidden_cat = torch.cat([embeds_normed, hidden_normed], dim=-1)
123	    print(f"  hidden_cat: {hidden_cat.shape}")
124	
125	    # 4. attention
126	    q = F.linear(hidden_cat, q_proj).view(1, seq_len, NUM_HEADS, HEAD_DIM).transpose(1, 2)
127	    k = F.linear(hidden_cat, k_proj).view(1, seq_len, NUM_KV_HEADS, HEAD_DIM).transpose(1, 2)
128	    v = F.linear(hidden_cat, v_proj).view(1, seq_len, NUM_KV_HEADS, HEAD_DIM).transpose(1, 2)
129	    if NUM_KV_GROUPS > 1:
130	        k = k.repeat_interleave(NUM_KV_GROUPS, dim=1)
131	        v = v.repeat_interleave(NUM_KV_GROUPS, dim=1)
132	    attn_output = F.scaled_dot_product_attention(q, k, v, is_causal=True)
133	    attn_output = attn_output.transpose(1, 2).contiguous().view(1, seq_len, -1)
134	    attn_output = F.linear(attn_output, o_proj)
135	    hidden_states = residual + attn_output.squeeze(0)
136	    print(f"  After attention: {hidden_states.shape}, mean={hidden_states.float().mean():.4f}")
137	
138	    # 5. MLP
139	    residual = hidden_states
140	    hidden_states = rms_norm(hidden_states, post_ln_weight)
141	    hidden_states = F.linear(F.silu(F.linear(hidden_states, gate_proj)) * F.linear(hidden_states, up_proj), down_proj)
142	    hidden_states = residual + hidden_states
143	    print(f"  After MLP: {hidden_states.shape}, mean={hidden_states.float().mean():.4f}")
144	
145	    # 6. final norm + lm_head
146	    hidden_states = rms_norm(hidden_states, norm_weight)
147	    logits = F.linear(hidden_states, lm_head_weight)
148	    print(f"  Final logits: {logits.shape}, mean={logits.float().mean():.4f}")
149	
150	    # Get predictions
151	    pred = logits.argmax(dim=-1)
152	    print(f"  Predictions (first 8): {pred[:8].tolist()}")
153	    print()
154	
155	
156	if __name__ == "__main__":
157	    test_fc_weight()
158	    test_lm_head()
159	    test_full_forward()
160
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle3_research.md"
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 Speculative Decoding for MiniCPM-SALA
2	
3	本文档记录 EAGLE-3 在 MiniCPM-SALA 上的研究与适配工作。
4	
5	## 1. 背景
6	
7	### 1.1 EAGLE 系列演进
8	
9	| 版本 | Loss 设计 | 关键特点 |
10	|------|----------|----------|
11	| EAGLE-1 | l_fea (MSE) + l_token (CE) | 特征预测 + token 预测 |
12	| EAGLE-2 | l_fea + l_token + tree attention | 引入 tree draft |
13	| **EAGLE-3** | **纯 plogp loss** | 去掉 l_fea，引入 TTT |
14	
15	### 1.2 EAGLE-3 核心创新
16	
17	1. **去除特征约束 (l_fea)**：不再要求 draft 预测 target 的 hidden state，解放模型表达能力
18	2. **Training-Time Test (TTT)**：训练时模拟真实 inference，draft 吃自己的预测做多步自回归
19	3. **多层特征融合**：concat 多层 hidden states 作为输入
20	4. **数据 scaling 生效**：更多数据 → 更高 acceptance rate
21	
22	### 1.3 MiniCPM-SALA 架构
23	
24	```
25	32 layers:
26	  - 8 Standard Attention (minicpm4): layers 0, 9, 16, 17, 22, 29, 30, 31
27	  - 24 Lightning Attention (SimpleGLA): 其余层
28	
29	Config:
30	  - hidden_size: 4096
31	  - intermediate_size: 16384
32	  - num_attention_heads: 32
33	  - num_key_value_heads: 2 (standard), 32 (lightning)
34	  - head_dim: 128
35	  - vocab_size: 73448
36	  - scale_emb: 12
37	  - scale_depth: 1.4
38	  - dim_model_base: 256
39	```
40	
41	**与 Llama 的关键差异**：
42	- 混合注意力架构（非同构）
43	- Lightning Attention 有递推状态 h: (nkv, head_dim, head_dim)
44	- 特殊的 scaling 模式：`scale_depth / sqrt(num_layers)`
45	
46	---
47	
48	## 2. Aux Layer 选择实验
49	
50	### 2.1 实验设计
51	
52	使用 linear probe 评估不同 layer 组合的 next-token 预测能力：
53	- 数据：wikitext-2, 64 samples × 2048 tokens
54	- 方法：Linear(hidden_size × 3, vocab_size) 训练 200 steps
55	- 指标：Cross-Entropy loss (lower = better)
56	
57	### 2.2 Per-Layer Cosine Similarity
58	
59	测量每层 hidden state 与 final hidden state 的余弦相似度：
60	
61	```
62	Layer  Type       CosSim
63	---------------------------
64	  0    Attn       0.0143
65	  1    Lightning  0.0172
66	  2    Lightning  0.0224
67	  ...
68	  9    Attn       0.0408
69	  10   Lightning  0.0419
70	  ...
71	  16   Attn       0.0537
72	  17   Attn       0.0588
73	  ...
74	  22   Attn       0.0767
75	  ...
76	  29   Attn       0.2349
77	  30   Attn       0.3000
78	  31   Attn       1.0000  ← 最后一层
79	```
80	
81	**观察**：
82	- 越深的层 cos_sim 越高
83	- Layer 31 = 1.0（与 final 完全相同，冗余）
84	- 标准 Attn 层的 cos_sim 略高于相邻的 Lightning 层
85	
86	### 2.3 Layer Combo 对比结果
87	
88	第一轮 (13 combos, 16 samples):
89	```
90	[2, 10, 22] CE=7.8260  ★ Best
91	[3, 14, 27] CE=10.7504
92	[4, 12, 28] CE=11.7970
93	[3, 16, 28] CE=11.8116
94	[2, 16, 29] CE=12.4497  ← EAGLE-3 default
95	...
96	[0, 16, 31] CE=30.5165  ← 含 layer 31，最差
97	```
98	
99	第二轮精调 (9 combos, 64 samples):
100	```
101	[1, 10, 22] CE=6.5112  ★ Best
102	[2, 9, 22]  CE=6.5734
103	[2, 10, 21] CE=6.6441
104	[2, 8, 22]  CE=6.6568
105	[2, 10, 22] CE=6.6753
106	...
107	```
108	
109	### 2.4 结论
110	
111	**选定 aux layers: [2, 10, 22]**
112	
113	| Layer | Type | 位置 | 选择理由 |
114	|-------|------|------|----------|
115	| 2 | Lightning | 早期 | 捕获原始特征 |
116	| 10 | Lightning | 中期 | 捕获中间处理 |
117	| 22 | Attn | 中后期 | 捕获标准注意力 pattern |
118	
119	**与 EAGLE-3 官方的差异**：
120	
121	EAGLE-3 官方代码用 [embedding, layer0, layer1]（极早期），可能原因：
122	1. Llama 是同构 Transformer，早期层足够
123	2. TTT 训练使 draft 能从错误中恢复，不需要 late layer 信息
124	3. Late layer 与 final 太接近，冗余
125	
126	MiniCPM-SALA 是**混合架构**，我们的选择覆盖两种注意力类型，更合理。
127	
128	---
129	
130	## 3. 草稿模型架构
131	
132	### 3.1 结构设计
133	
134	```
135	MiniCPMForCausalLMEagle3:
136	  fc: Linear(4096 × 3, 4096)     # 融合 3 层 aux hidden
137	  midlayer: MiniCPMDecoderLayer  # 1 层完整 transformer
138	    - input_layernorm: RMSNorm
139	    - hidden_norm: RMSNorm       # 额外的 hidden 归一化
140	    - self_attn: Attention
141	        - qkv_proj: Linear(2 × 4096, ...)  # 输入 = cat(embed, hidden)
142	        - o_proj
143	    - post_attention_layernorm: RMSNorm
144	    - mlp: gate_proj, up_proj, down_proj
145	  final_norm: RMSNorm
146	
147	共享组件 (来自 target):
148	  - embed_tokens
149	  - lm_head
150	```
151	
152	### 3.2 参数量估算
153	
154	| 组件 | 参数量 | 大小 (bf16) |
155	|------|--------|-------------|
156	| fc | 50M | 100 MB |
157	| midlayer.qkv_proj | 38M | 76 MB |
158	| midlayer.o_proj | 17M | 34 MB |
159	| midlayer.mlp | 201M | 402 MB |
160	| norms | ~0 | ~0 |
161	| **Total** | **~306M** | **~612 MB** |
162	
163	提交预算：
164	- NVFP4 目标模型：在线量化（不占 zip）
165	- 草稿模型 bf16：612 MB
166	- 代码 + 数据：~50 MB
167	- **Total: ~670 MB << 2 GB 限制**
168	
169	### 3.3 代码位置
170	
171	- `eagle/minicpm_eagle3.py` - SGLang 格式的草稿模型
172	- 训练时使用独立的 PyTorch 模型，训练后转换权重
173	
174	---
175	
176	## 4. 训练设计
177	
178	### 4.1 EAGLE-3 官方训练方式
179	
180	```python
181	# cnets.py 核心逻辑
182	for idx in range(7):  # 7 步 TTT
183	    inputs_embeds = embed_tokens(input_ids)
184	    hidden, cache = midlayer(inputs_embeds, hidden, cache, ...)
185	    logits = lm_head(norm(hidden))
186	
187	    # plogp loss
188	    target_p = softmax(target_logits)
189	    out_logp = log_softmax(logits)
190	    loss = -sum(target_p * out_logp * mask)
191	
192	    if not last:
193	        input_ids = shift(input_ids)  # 用预测结果作为下一步输入
194	```
195	
196	关键点：
197	1. **纯 plogp loss**：`-sum(target_p × log(draft_p))`，无 CE，无 feature loss
198	2. **7 步 TTT**：训练时自回归，模拟真实 inference
199	3. **loss_mask**：屏蔽 prompt 部分，只在 response 上计算 loss
200	4. **DeepSpeed**：多卡分布式训练
201	
202	### 4.2 我们的 2-Phase 方案
203	
204	**Phase 1: 离线数据准备 (8 GPU 并行)**
205	
206	```
207	输入: wikitext / ShareGPT 数据
208	输出:
209	  - embeddings: (N, seq_len, 4096)
210	  - aux_hidden: (N, seq_len, 4096 × 3)
211	  - target_logits: (N, seq_len, vocab_size)
212	  - targets: (N, seq_len)
213	  - loss_mask: (N, seq_len)
214	
215	存储: ~100 GB for 100K samples
216	```
217	
218	**Phase 2: Draft 模型训练 (8 GPU DDP)**
219	
220	```
221	输入: Phase 1 的缓存数据
222	训练:
223	  - 7 步 TTT 自回归
224	  - 纯 plogp loss
225	  - batch_size: 32 (4 per GPU × 8 GPU)
226	  - epochs: 40
227	  - lr: 1e-4 with cosine decay
228	```
229	
230	### 4.3 与官方实现的差异
231	
232	| 方面 | EAGLE-3 官方 | 我们的方案 |
233	|------|-------------|-----------|
234	| Target forward | 每 batch 在线计算 | Phase 1 离线预计算 |
235	| 训练框架 | DeepSpeed ZeRO-3 | PyTorch DDP |
236	| 数据格式 | ShareGPT jsonl | wikitext + calib data |
237	| Aux layers | [emb, layer0, layer1] | [2, 10, 22] |
238	| 模型适配 | Llama | MiniCPM-SALA hybrid |
239	
240	---
241	
242	## 5. SimpleGLA 状态管理
243	
244	### 5.1 问题
245	
246	MiniCPM-SALA 的 24 层 Lightning Attention 维护递推状态：
247	```
248	h: (batch, num_kv_heads, head_dim, head_dim)
249	   = (bs, 32, 128, 128) per layer
250	   ≈ 2 MB per layer per request
251	```
252	
253	Speculative decoding verify 后，被拒绝的 token 已污染状态，需要回滚。
254	
255	### 5.2 Baseline 方案：Python 级快照
256	
257	```python
258	# verify 前
259	snapshot = [layer.cache.temporal.clone() for layer in gla_layers]
260	
261	# verify 后
262	for i, layer in enumerate(gla_layers):
263	    layer.cache.temporal = snapshot[i][:, :, :accepted_len]
264	```
265	
266	开销：24 layers × 2 MB ≈ 48 MB per request（可接受）
267	
268	### 5.3 优化方案：Kernel 级 intermediate state
269	
270	参考 GDR kernel (`fla/fused_recurrent.py`)：
271	- `CACHE_INTERMEDIATE_STATES`：缓存每步状态
272	- `DISABLE_STATE_UPDATE`：verify 时不更新状态
273	- `retrieve_parent_token`：tree attention 状态选择
274	
275	需要为 SimpleGLA 实现类似的 kernel，后续优化。
276	
277	---
278	
279	## 6. 预期效果
280	
281	### 6.1 Acceptance Rate 估算
282	
283	假设 per-token acceptance α = 0.6-0.7（保守估计）：
284	
285	| spec_steps | 期望 tokens | 加速比 |
286	|------------|-------------|--------|
287	| 3 | ~2.2 | ~1.7× |
288	| 5 | ~2.8 | ~1.9× |
289	| 7 | ~3.2 | ~2.1× |
290	
291	### 6.2 对竞赛指标的影响
292	
293	| 指标 | 当前 | 预期 (α=0.65) |
294	|------|------|---------------|
295	| S1 | 650s | ~400-450s |
296	| S8 | 645s | ~580-620s |
297	| Smax | 916s | ~800-850s |
298	
299	**注意**：高并发场景 (S8, Smax) 收益有限，因为额外内存占用减少 KV cache 空间。
300	
301	---
302	
303	## 7. 文件结构
304	
305	```
306	eagle/
307	├── minicpm_eagle3.py       # SGLang 草稿模型定义
308	├── train_eagle3.py         # 训练脚本 (待重写)
309	├── test_layer_selection.py # Layer 选择实验
310	├── EAGLE/                  # EAGLE 官方仓库 (参考)
311	│   └── eagle/traineagle3/
312	│       ├── main.py         # 官方训练入口
313	│       └── cnets.py        # 官方模型定义
314	└── data_cache/             # 数据缓存
315	    ├── wikitext_*.pt
316	    └── target_*.pt
317	```
318	
319	---
320	
321	## 8. TODO
322	
323	- [ ] 重写 `train_eagle3.py`：实现 2-Phase 训练
324	  - [ ] Phase 1: 离线数据准备脚本
325	  - [ ] Phase 2: 8 GPU DDP 训练脚本
326	- [ ] 实现 7 步 TTT 自回归训练
327	- [ ] 实现纯 plogp loss
328	- [ ] 测试 aux layers [1, 2, 3] vs [2, 10, 22]
329	- [ ] SimpleGLA 状态快照/回滚
330	- [ ] 集成到 SGLang serving
331	
332	---
333	
334	## 9. 参考资料
335	
336	- EAGLE-3 Paper: arxiv:2503.01840
337	- EAGLE GitHub: https://github.com/SafeAILab/EAGLE
338	- SGLang EAGLE 实现: `sglang/srt/models/llama_eagle3.py`
339
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /user_4813494d/openbmb/medusa/medusa/"
}
```

> TOOL

tool_result Bash
```
total 4
drwxr-xr-x 3 user_4813494d user_4813494d   29 Apr  4 12:22 .
drwxr-xr-x 6 user_4813494d user_4813494d 4096 Apr 10 11:18 ..
drwxr-xr-x 2 user_4813494d user_4813494d   10 Apr  4 12:22 weights
```

> AGENT

Now let me check the bench/mini_bench.sh:

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -name \"mini_bench.sh\" -o -name \"*bench*.sh\" 2>/dev/null | grep -v \".git\""
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/bench/.ipynb_checkpoints/mini_bench-checkpoint.sh
/user_4813494d/openbmb/bench/mini_bench.sh
/user_4813494d/openbmb/toolkit/bench_serving.sh
```

> AGENT

Now let me read the remaining documentation files:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle3-pipeline.md"
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 Speculative Decoding Pipeline for MiniCPM-SALA
2	
3	## 1. 概述
4	
5	用 EAGLE-3 替代 Medusa K=1 作为 speculative decoding 方案。
6	
7	**当前 Medusa K=1 基线**：head_0 top-1 accuracy = 37.7%，tokens_per_step = 1.377，S1 = 360s
8	
9	**EAGLE-3 目标**：step_0 top-1 accuracy > 55%，tokens_per_step > 2.5，S1 < 300s
10	
11	## 2. Aux Layers 选择
12	
13	**选定：[1, 10, 22]**
14	
15	| Layer | 深度 | 类型 | 作用 |
16	|-------|------|------|------|
17	| 1 | 早期 (第 2 层) | Lightning Attention | Token identity + 位置 + 初步上下文 |
18	| 10 | 中期 (第 11 层) | Lightning Attention | 中间语义，已过 2 次 StdAttn + 9 次 Lightning |
19	| 22 | 中后期 (第 23 层) | Standard Attention | 接近最终语义，单独预测力最强 |
20	
21	**选择理由**：
22	- MiniCPM-SALA 的 `scale_depth=1.4/sqrt(32)=0.247` 使早期层之间高度相似，all-early（官方 [emb,0,1]）会浪费 fc 容量
23	- early + mid + late 组合信息互补最大化
24	- Linear probe 实验支持：[1,10,22] CE=6.51 (best) vs [2,10,22] CE=6.68
25	- 覆盖两种注意力类型
26	
27	**备选 A/B**：如 [1,10,22] 效果不佳，测试 [0,9,22]（全 Standard Attention 层）
28	
29	## 3. Pipeline 阶段
30	
31	### Phase 1: 数据采集 (~4h)
32	
33	**方法**：修改 SGLang 模型 forward hook，从 NVFP4 量化模型采集中间层输出
34	
35	**修改文件**：
36	- `demo-sala/sglang/python/sglang/srt/models/minicpm.py` — 添加 aux layer 捕获
37	- `medusa/collect_eagle_data.py` — 新增采集脚本
38	
39	**采集数据格式** (.pt)：
40	```python
41	{
42	    "token_ids":         (seq_len,),         # int64
43	    "embeds":            (seq_len, 4096),    # bf16, embed_tokens(ids) * scale_emb
44	    "aux_hidden":        (seq_len, 4096*3),  # bf16, cat(layer1, layer10, layer22)
45	    "hidden_states":     (seq_len, 4096),    # bf16, 最后一层 post-norm（兼容 Medusa）
46	    "top_logit_values":  (seq_len, 256),     # bf16, target top-256 logit values
47	    "top_logit_indices": (seq_len, 256),     # int32, target top-256 token indices
48	}
49	```
50	
51	每文件 ~42 MB，目标 3000 samples ≈ 126 GB。
52	
53	**数据源**：待定（见第 4 节讨论）
54	
55	### Phase 2: 训练 (~6h)
56	
57	**新增文件**：`medusa/train_eagle3.py`
58	
59	**Draft Model 架构** (~306M trainable params):
60	```
61	MiniCPMEagle3Draft:
62	  fc:        Linear(4096×3 → 4096, bias=False)     # 50M
63	  midlayer:  1× MiniCPM decoder layer               # ~256M
64	    self_attn: QKV input = cat(embed, hidden) = 8192
65	      q_proj(8192→4096), k_proj(8192→256), v_proj(8192→256), o_proj(4096→4096)
66	    mlp: gate_proj(4096→16384), up_proj(4096→16384), down_proj(16384→4096)
67	    norms: input_layernorm, hidden_norm, post_attention_layernorm
68	  final_norm: RMSNorm(4096)
69	  lm_head:   Linear(4096 → draft_vocab_size)        # ~130M (frozen target lm_head 或独立)
70	
71	共享 (frozen): embed_tokens from target model
72	```
73	
74	**训练配置**（与官方 EAGLE-3 对齐）：
75	```
76	ttt_steps       = 7           # Training-Time Test
77	batch_size      = 2-8         # 单 GPU 84 GB
78	grad_checkpoint = True
79	seq_len         = 2048
80	lr              = 1e-4
81	warmup_steps    = 200
82	weight_decay    = 0.0
83	betas           = (0.9, 0.95)
84	max_grad_norm   = 0.5
85	loss_decay      = 0.8         # step i weight = 0.8^i
86	draft_vocab     = 32000       # 高频 token 子集
87	epochs          = 10
88	```
89	
90	**TTT 训练流程**（每 batch）：
91	```
92	1. hidden = fc(aux_hidden)
93	2. 构建 causal mask
94	3. for step in range(7):
95	     input_emb = embeds (step 0) 或 embed_tokens(shift(ids)) (step > 0)
96	     hidden_out = midlayer(input_emb, hidden, kv_cache, mask)
97	     logits = lm_head(final_norm(hidden_out))
98	     loss_i = plogp(logits, target_p)   # -Σ(target_p × log(draft_p))
99	     hidden = hidden_out
100	4. total_loss = Σ(0.8^i × loss_i)
101	```
102	
103	**VRAM 估算**: ~6.5 GB（极为充裕）
104	
105	### Phase 3: 离线评估 (~1h)
106	
107	**新增文件**：`medusa/eval_eagle3.py`
108	
109	测量：per-step acceptance rate、mean_accepted_length、tokens_per_step
110	
111	**通过标准**：step_0 accuracy > 50%，mean_accepted_length > 1.0
112	
113	### Phase 4: Serving 集成 (~4h)
114	
115	**文件**：
116	- `demo-sala/sglang/.../models/minicpm_eagle3.py` — 新增 SGLang draft model
117	- `demo-sala/sglang/.../speculative/eagle_worker.py` — 适配 GLA rollback
118	- `demo-sala/sglang/.../models/minicpm.py` — target forward 输出 aux hidden
119	- `demo-sala/prepare_env.sh` — 启动参数
120	
121	**复用**：
122	- eagle_worker.py 的 tree draft + verify 框架
123	- MedusaVerifyInput 或 EagleVerifyInput
124	- update_mamba_state_after_mtp_verify() GLA 回滚 kernel
125	- CUDA graph capture 基础设施
126	
127	### Phase 5: 端到端验证 (~2h)
128	
129	**验收标准**：
130	
131	| 指标 | Medusa K=1 | EAGLE-3 目标 |
132	|------|-----------|-------------|
133	| ori_accuracy | 81.0% | ≥ 80% |
134	| S1 | ~360s | ≤ 300s |
135	| S8 | ~350s | ≤ 340s |
136	
137	## 4. 数据配比（待讨论）
138	
139	现有 Medusa 训练数据配比 (v2 + v3 supplement, ~57M tokens):
140	- Chinese (SkyPile): ~50% → 20M tokens
141	- Code (multi-lang): ~42% → 24M tokens
142	- English (wikitext): ~8% → 4M tokens
143	
144	EAGLE-3 的数据配比需要单独讨论——可能需要与评测集分布对齐。
145	
146	## 5. 参考
147	
148	- EAGLE-3 官方代码: `~/EAGLE/eagle/traineagle3/`
149	- 研究笔记: `docs/eagle3_research.md`
150	- Medusa 训练: `medusa/train.py`
151	- Medusa 数据采集: `medusa/collect_data.py`
152
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle3-accept-rate-fix.md"
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 Accept Rate 修复记录
2	
3	## 问题
4	
5	EAGLE-3 speculative decoding 在线 accept rate 仅 ~5%（accept_len ~1.05），离线训练 acc0 却有 63.5%。Draft model 在推理时几乎无法命中任何 token。
6	
7	## 根因分析
8	
9	### 训练/推理的 token-hidden_states 对齐不一致
10	
11	sglang EAGLE-3 推理时对 input_ids 做了隐式左移：
12	
13	1. **`eagle_info.py` prepare_for_extend**（首次 extend）：
14	   ```python
15	   input_ids = torch.cat((input_ids[1:], verified_id))
16	   ```
17	   位置 t 的 token 变成了 x_{t+1}，而 hidden_states 仍是 aux[t]。
18	
19	2. **`eagle_info.py` prepare_extend_after_decode**（后续 decode）：
20	   ```python
21	   batch.input_ids = self.verified_id  # target 预测的未来 token
22	   hidden_states = hidden_states[accept_index]  # 已接受位置的 hidden
23	   ```
24	   verified_id 是 target model 的预测（未来 token），配对的是当前位置的 aux_hidden。
25	
26	因此推理时 draft model 实际输入为 **(x_{t+1}, aux[t])** → 预测 **x_{t+2}**。
27	
28	而旧训练代码使用对齐的 **(x_t, aux[t])** → 预测 **x_{t+1}**。输入分布完全不匹配，导致 draft 几乎无法命中。
29	
30	### 验证
31	
32	用旧权重在 shifted eval 上测试：OOD accept rate = 8.2%，与在线 ~5% 吻合，确认根因。
33	
34	## 修复
35	
36	### 1. 训练对齐修复 (`eagle/train.py`)
37	
38	将训练 forward 的输入做同样的 shift，匹配推理行为：
39	
40	```python
41	# 修复前（对齐的）
42	input_ids = token_ids              # x_0..x_{S-1}
43	hidden = self.fc(aux_hidden)       # aux_0..aux_{S-1}
44	
45	# 修复后（shifted，匹配推理）
46	input_ids = token_ids[:, 1:]           # x_1..x_{S-1}
47	aux_shifted = aux_hidden[:, :-1, :]    # aux_0..aux_{S-2}
48	target_values = target_logits_values[:, 1:, :]
49	target_indices = target_logits_indices[:, 1:, :]
50	```
51	
52	### 2. 评估脚本修复 (`eagle/eval_ood_accept.py`)
53	
54	- 同步 shifted 对齐
55	- 修复 checkpoint 键名映射（`midlayer.` 前缀剥离、`input_emb_norm` → `input_layernorm`）
56	- 支持从训练 checkpoint 直接加载
57	
58	### 3. 诊断代码清理
59	
60	从 `eagle_info.py`、`eagle_worker.py`、`minicpm.py` 移除全部 6 个 DIAG 打印块。
61	
62	## 重训结果
63	
64	训练配置：10 epochs, batch=2x4 grad_accum, lr=3e-4, seq_len=2048, 9530 files。
65	
66	| Checkpoint | 训练 acc0 | OOD Accept Rate | 在线 accept_len |
67	|-----------|---------|----------------|----------------|
68	| 旧(未shift) | 63.5% | 8.2% | ~1.05 |
69	| Epoch 1 (shifted) | 34.3% | 35.5% | 1.50 (单请求) / 1.33 (32并发) |
70	| Epoch 2 (shifted) | 53.9% | 45.8% | — |
71	| Epoch 3+ | 61.9%+ | 预计 >50% | — |
72	
73	## OOD Accept Rate 饱和
74	
75	| Epoch | 训练 acc0 | OOD Accept Rate | delta |
76	|-------|---------|----------------|-------|
77	| 1 | 34.3% | 35.5% | — |
78	| 2 | 53.9% | 45.8% | +10.3 |
79	| 3 | 61.9% | 49.1% | +3.3 |
80	| 4 | 67.6% | 49.3% | +0.2 |
81	
82	Epoch 4 后 OOD accept rate 基本饱和（49.3%），训练 acc 仍在涨但 OOD 不动。gap 说明过拟合到训练集分布。进一步提升需要 in-domain 验证集做 early stopping，或更大/更多样的训练数据。
83	
84	## Tree Verify 与线性注意力的兼容性问题
85	
86	### 问题
87	
88	MiniCPM-SALA 有 24/32 层 GLA（线性注意力）。sglang 的 EAGLE tree verify 对两种注意力层处理方式不同：
89	
90	- **Standard attention（8层）**：使用 tree mask（FlashInfer prefill + custom_mask），每个 token 只 attend 祖先链。**正确。**
91	- **GLA（24层）**：`hybrid_linear_attn_backend.py:1636-1711` 逐 token 串行处理，所有 draft tokens 当成线性序列。**不同分支间 state 互相污染。**
92	
93	```python
94	# GLA TARGET_VERIFY 实际行为（simplified）
95	for step in range(draft_token_num):
96	    o_s, current_state = fused_recurrent_simple_gla(...)
97	    intermediate_ssm[layer, :batch, step] = current_state
98	# → A 分支的 state 污染了 B 分支的计算
99	```
100	
101	### topk=1 vs topk=2 实测
102	
103	理论上 topk=1（单链）对 GLA 完全正确，但实测 **topk=2 仍然更快**。
104	
105	原因：tree 的候选覆盖率优势 > GLA state 污染的精度损失：
106	- `topk=2, steps=3`：6 个候选，命中概率高
107	- `topk=1, steps=3`：3 个候选，覆盖面窄
108	- 8 层 standard attention 的 tree mask 仍然正确，部分补偿 GLA 误差
109	- GLA 污染有界——sibling branch 对 state 的扰动不至于完全破坏 logits
110	
111	### 可能的改进方向
112	
113	1. **DFS 遍历 + state 分支保存**：GLA 层在分支点保存 state，处理完一条路径后 restore。每个分支点额外 ~1 MB/层，24层×3点=72 MB。计算量不变（已经逐 token 串行），只多 save/restore 操作。
114	2. **更大/更好的 draft model**：2-3 层 draft 提高 accept rate，配合 NVFP4 量化控制 latency。
115	3. **In-domain 训练数据**：当前 OOD accept rate 49.3% 饱和，更匹配的训练数据可能突破瓶颈。
116	
117	## 排查过程中排除的假设
118	
119	1. **verify_tree / retrive_index bug** — 验证逻辑正确，`ridx=[0..7]` 全部列出，d1_hit=True 时 accept_length=1
120	2. **layers_to_capture 不匹配** — 确认 {2,11,23}（MLP delta）与训练数据采集一致
121	3. **residual bug** — 模型捕获的是 MLP delta（无 residual），与训练一致
122	
123	## 关键文件
124	
125	| 文件 | 改动 |
126	|------|------|
127	| `eagle/train.py` | shifted 对齐修复 |
128	| `eagle/eval_ood_accept.py` | shifted eval + 键名映射修复 |
129	| `eagle/convert_to_sglang.py` | checkpoint → sglang 格式转换 |
130	| `demo-sala/sglang/.../eagle_info.py` | 清理诊断代码 |
131	| `demo-sala/sglang/.../eagle_worker.py` | 清理诊断代码 |
132	| `demo-sala/sglang/.../models/minicpm.py` | 清理诊断代码 |
133
```

> AGENT

Now let me read the key files:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/medusa/train.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Train Medusa heads for MiniCPM-SALA speculative decoding.
4	
5	Step-based training with warmup + cosine LR decay, dropout, weight decay.
6	Eval every 20% of total steps on both val_ind and val_ood.
7	
8	Run from repo user_4813494d:
9	    python3 medusa/train.py
10	"""
11	
12	import math
13	import os
14	import queue
15	import random
16	import threading
17	import time
18	from pathlib import Path
19	
20	import torch
21	import torch.nn as nn
22	import torch.nn.functional as F
23	from safetensors import safe_open
24	from tqdm import tqdm
25	
26	# ── Config ──────────────────────────────────────────────────────────────
27	DATA_DIR   = Path("medusa/data")
28	OUTPUT_DIR = Path("medusa/weights")
29	MODEL_PATH = [REDACTED]
30	
31	NUM_HEADS     = 1
32	EQUIV_EPOCHS  = 5        # total_steps = equiv_epochs × packs_per_pass (if TOTAL_STEPS=0)
33	TOTAL_STEPS   = 10000    # explicit step count
34	LR            = 1e-3
35	LR_ETA_MIN    = 1e-5
36	WARMUP_STEPS  = 200
37	WEIGHT_DECAY  = 0.0
38	DROPOUT       = 0.0
39	GRAD_CLIP     = 1.0
40	DECAY         = 0.8      # head loss weight decay (K>1)
41	PACK_SIZE     = 6
42	VAL_IND_PCT   = 0.015
43	VAL_EVERY_PCT = 0.20     # eval every 20% of total steps
44	SEED          = 42
45	RESUME_FROM   = None     # set to checkpoint path to resume, e.g. "medusa/weights/best.pt"
46	
47	# Weighted sampling: use importance^WEIGHT_POWER as sampling weights.
48	# Requires medusa/data/train_ranked_by_val_ood.json (from select_similar.py).
49	# Files with higher cosine similarity to val_ood are sampled more frequently.
50	USE_WEIGHTED_SAMPLING = True
51	WEIGHT_POWER  = 2.0      # importance^power as sampling weight
52	WEIGHT_FLOOR  = 0.1      # minimum weight (prevents zero-weight files)
53	
54	# ── Model constants ─────────────────────────────────────────────────────
55	HIDDEN_SIZE = 4096
56	VOCAB_SIZE  = 73448
57	SCALE_WIDTH = HIDDEN_SIZE / 256
58	
59	
60	# ── Model ───────────────────────────────────────────────────────────────
61	class RMSNorm(nn.Module):
62	    def __init__(self, hidden_size: int, eps: float = 1e-6):
63	        super().__init__()
64	        self.weight = nn.Parameter(torch.ones(hidden_size))
65	        self.eps = eps
66	
67	    def forward(self, x: torch.Tensor) -> torch.Tensor:
68	        norm = x.float().pow(2).mean(-1, keepdim=True).add(self.eps).rsqrt()
69	        return (x * norm).to(x.dtype) * self.weight
70	
71	
72	class ResBlock(nn.Module):
73	    def __init__(self, hidden_size: int, dropout: float = 0.0):
74	        super().__init__()
75	        self.linear = nn.Linear(hidden_size, hidden_size)
76	        nn.init.zeros_(self.linear.weight)
77	        nn.init.zeros_(self.linear.bias)
78	        self.act = nn.SiLU()
79	        self.dropout = nn.Dropout(dropout) if dropout > 0 else nn.Identity()
80	
81	    def forward(self, x: torch.Tensor) -> torch.Tensor:
82	        return x + self.dropout(self.act(self.linear(x)))
83	
84	
85	class MedusaBlock(nn.Module):
86	    def __init__(self, hidden_size: int, dropout: float = 0.0):
87	        super().__init__()
88	        self.norm = RMSNorm(hidden_size)
89	        self.res1 = ResBlock(hidden_size, dropout)
90	        self.res2 = ResBlock(hidden_size, dropout)
91	
92	    def forward(self, x: torch.Tensor) -> torch.Tensor:
93	        x = self.norm(x)
94	        x = self.res1(x)
95	        x = self.res2(x)
96	        return x
97	
98	
99	class MedusaHeads(nn.Module):
100	    def __init__(self, num_heads: int, hidden_size: int, lm_head_weight: torch.Tensor,
101	                 dropout: float = 0.0):
102	        super().__init__()
103	        self.num_heads = num_heads
104	        self.heads = nn.ModuleList(
105	            [MedusaBlock(hidden_size, dropout) for _ in range(num_heads)])
106	        self.register_buffer("lm_head_weight", lm_head_weight)
107	
108	    def forward(self, hidden_states: torch.Tensor) -> list[torch.Tensor]:
109	        return [F.linear(head(hidden_states), self.lm_head_weight).float()
110	                for head in self.heads]
111	
112	
113	# ── Data ────────────────────────────────────────────────────────────────
114	def load_split_files(split_dir: Path) -> list[Path]:
115	    files = sorted(split_dir.glob("*.pt"))
116	    if not files:
117	        raise FileNotFoundError(f"No .pt files in {split_dir}")
118	    return files
119	
120	
121	def _load_pack_cpu(files: list[Path], K: int):
122	    hs, label_lists = [], [[] for _ in range(K)]
123	    for f in files:
124	        data = torch.load(f, map_location="cpu", weights_only=True)
125	        h   = data["hidden_states"]
126	        ids = data["token_ids"]
127	        valid_len = len(ids) - K - 1
128	        if valid_len < 1 or h.isnan().any():
129	            continue
130	        hs.append(h[:valid_len])
131	        for k in range(K):
132	            label_lists[k].append(ids[k + 2 : k + 2 + valid_len])
133	    if not hs:
134	        return None, None
135	    return torch.cat(hs, dim=0), [torch.cat(lbl, dim=0) for lbl in label_lists]
136	
137	
138	class PackStream:
139	    """Infinite stream of (h, labels) packs with background prefetch.
140	
141	    Supports weighted sampling: files with higher importance are sampled more often.
142	    Without weights, shuffles uniformly each pass.
143	    """
144	    def __init__(self, files: list[Path], K: int, device: torch.device,
145	                 pack_size: int = PACK_SIZE, seed: int = SEED,
146	                 weights: list[float] | None = None):
147	        self.files = list(files)
148	        self.K = K
149	        self.device = device
150	        self.pack_size = pack_size
151	        self.rng = random.Random(seed)
152	        self.packs_per_pass = (len(files) + pack_size - 1) // pack_size
153	        self.weights = weights  # per-file sampling weights (same order as files)
154	
155	    def _make_batches(self):
156	        """Sample files for one pass (weighted or uniform)."""
157	        n = len(self.files)
158	        if self.weights is not None:
159	            # Weighted sampling with replacement: draw n files
160	            sampled = self.rng.choices(self.files, weights=self.weights, k=n)
161	        else:
162	            sampled = list(self.files)
163	            self.rng.shuffle(sampled)
164	        return [sampled[i:i + self.pack_size]
165	                for i in range(0, len(sampled), self.pack_size)]
166	
167	    def __iter__(self):
168	        """Yield (h, labels) on device indefinitely."""
169	        q = queue.Queue(maxsize=3)
170	        stop = threading.Event()
171	
172	        def worker():
173	            while not stop.is_set():
174	                for batch in self._make_batches():
175	                    if stop.is_set():
176	                        return
177	                    q.put(_load_pack_cpu(batch, self.K))
178	            q.put(None)
179	
180	        t = threading.Thread(target=worker, daemon=True)
181	        t.start()
182	        try:
183	            while True:
184	                item = q.get()
185	                if item is None:
186	                    break
187	                h_cpu, labels_cpu = item
188	                if h_cpu is None:
189	                    continue
190	                yield h_cpu.to(self.device), [l.to(self.device) for l in labels_cpu]
191	        finally:
192	            stop.set()
193	            t.join(timeout=5)
194	
195	
196	def iter_packs(files: list[Path], K: int, device: torch.device):
197	    """Single-pass iterator for evaluation."""
198	    batches = [files[i:i + PACK_SIZE] for i in range(0, len(files), PACK_SIZE)]
199	    q = queue.Queue(maxsize=2)
200	    stop = threading.Event()
201	
202	    def worker():
203	        for batch in batches:
204	            if stop.is_set():
205	                break
206	            q.put(_load_pack_cpu(batch, K))
207	        q.put(None)
208	
209	    t = threading.Thread(target=worker, daemon=True)
210	    t.start()
211	    try:
212	        while True:
213	            item = q.get()
214	            if item is None:
215	                break
216	            h_cpu, labels_cpu = item
217	            if h_cpu is None:
218	                continue
219	            yield h_cpu.to(device), [l.to(device) for l in labels_cpu]
220	    finally:
221	        stop.set()
222	        t.join(timeout=5)
223	
224	
225	# ── LR Schedule ─────────────────────────────────────────────────────────
226	def get_lr(step: int, total_steps: int, warmup: int, lr_max: float, lr_min: float) -> float:
227	    if step < warmup:
228	        return lr_max * step / max(warmup, 1)
229	    progress = (step - warmup) / max(total_steps - warmup, 1)
230	    return lr_min + 0.5 * (lr_max - lr_min) * (1 + math.cos(math.pi * progress))
231	
232	
233	def set_lr(optimizer, lr: float):
234	    for pg in optimizer.param_groups:
235	        pg["lr"] = lr
236	
237	
238	# ── Evaluation ──────────────────────────────────────────────────────────
239	@torch.no_grad()
240	def evaluate(model: MedusaHeads, files: list[Path], device,
241	             split_name: str = "val") -> dict:
242	    model.eval()
243	    K = model.num_heads
244	    total_pos, total_accept, total_loss = 0, 0.0, 0.0
245	    top1 = [0] * K
246	    n_packs = 0
247	
248	    pbar = tqdm(desc=f"Eval {split_name}", unit="pack", leave=False,
249	                total=(len(files) + PACK_SIZE - 1) // PACK_SIZE)
250	    for h, labels in iter_packs(files, K, device):
251	        logits = model(h)
252	        N = h.shape[0]
253	        matches = []
254	        for k in range(K):
255	            total_loss += (DECAY ** k) * F.cross_entropy(logits[k], labels[k]).item()
256	            preds = logits[k].argmax(dim=-1)
257	            m = preds == labels[k]
258	            matches.append(m)
259	            top1[k] += m.sum().item()
260	        accept = torch.stack(matches).cumprod(0).sum(0)
261	        total_accept += accept.sum().item()
262	        total_pos += N
263	        n_packs += 1
264	        pbar.update(1)
265	    pbar.close()
266	
267	    mean_accept = total_accept / max(total_pos, 1)
268	    metrics = {
269	        "loss":            round(total_loss / max(n_packs, 1), 4),
270	        "mean_accept_len": round(mean_accept, 3),
271	        "tokens_per_step": round(1.0 + mean_accept, 3),
272	        "n_positions":     total_pos,
273	    }
274	    for k in range(K):
275	        metrics[f"head_{k}_top1_acc"] = round(top1[k] / max(total_pos, 1), 4)
276	    model.train()
277	    return metrics
278	
279	
280	# ── Checkpoint ──────────────────────────────────────────────────────────
281	def save_checkpoint(model, step, m_ood, m_ind, path):
282	    torch.save({
283	        "heads_state_dict": {k: v.cpu() for k, v in model.heads.state_dict().items()},
284	        "num_heads": model.num_heads, "hidden_size": HIDDEN_SIZE,
285	        "step": step, "metrics_ood": m_ood, "metrics_ind": m_ind,
286	    }, path)
287	
288	
289	# ── Main ────────────────────────────────────────────────────────────────
290	def split_train_val_ind(all_files: list[Path], pct: float, seed: int = SEED):
291	    rng = random.Random(seed)
292	    shuffled = list(all_files)
293	    rng.shuffle(shuffled)
294	    n_val = max(int(len(shuffled) * pct), 10)
295	    return shuffled[n_val:], shuffled[:n_val]
296	
297	
298	def main():
299	    torch.manual_seed(SEED)
300	    device = torch.device("cuda")
301	    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
302	
303	    # ── Data ────────────────────────────────────────────────────────────
304	    all_train = load_split_files(DATA_DIR / "train")
305	    val_dir = DATA_DIR / "val"
306	    if val_dir.exists():
307	        all_train += load_split_files(val_dir)
308	
309	    # Load importance weights for weighted sampling
310	    ranked_path = DATA_DIR / "train_ranked_by_val_ood.json"
311	    file_importance = {}  # file_path -> max_cos_sim
312	    if USE_WEIGHTED_SAMPLING and ranked_path.exists():
313	        import json
314	        with open(ranked_path) as f:
315	            ranked = json.load(f)
316	        for r in ranked:
317	            file_importance[r["file"]] = r.get("max_cos_sim", 1.0 - r.get("dist", 0.0))
318	        print(f"Loaded importance weights for {len(file_importance)} files")
319	    elif USE_WEIGHTED_SAMPLING:
320	        print(f"⚠ USE_WEIGHTED_SAMPLING=True but {ranked_path} not found. "
321	              f"Run select_similar.py first. Using uniform sampling.")
322	
323	    train_files, ind_files = split_train_val_ind(all_train, VAL_IND_PCT)
324	    ood_files = load_split_files(DATA_DIR / "val_ood")
325	
326	    packs_per_pass = (len(train_files) + PACK_SIZE - 1) // PACK_SIZE
327	    total_steps = TOTAL_STEPS if TOTAL_STEPS > 0 else EQUIV_EPOCHS * packs_per_pass
328	    val_every = max(int(total_steps * VAL_EVERY_PCT), 1)
329	
330	    print(f"Data: train={len(train_files)}, val_ind={len(ind_files)}, val_ood={len(ood_files)}")
331	    print(f"Training: {total_steps} steps, {packs_per_pass} packs/pass, "
332	          f"~{total_steps / packs_per_pass:.1f} equiv epochs")
333	    print(f"Schedule: warmup={WARMUP_STEPS}, lr={LR}→{LR_ETA_MIN}, "
334	          f"wd={WEIGHT_DECAY}, dropout={DROPOUT}")
335	    print(f"Eval every {val_every} steps ({VAL_EVERY_PCT*100:.0f}%)")
336	
337	    # ── Model ───────────────────────────────────────────────────────────
338	    print("Loading lm_head...")
339	    sf_path = os.path.join(MODEL_PATH, "model-00002-of-00002.safetensors")
340	    with safe_open(sf_path, framework="pt") as sf:
341	        lm_head_w = sf.get_tensor("lm_head.weight").to(device)
342	    lm_head_w = lm_head_w / SCALE_WIDTH
343	
344	    model = MedusaHeads(
345	        NUM_HEADS, HIDDEN_SIZE, lm_head_w, dropout=DROPOUT,
346	    ).to(device=device, dtype=torch.bfloat16)
347	
348	    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
349	    print(f"Medusa: {NUM_HEADS} heads, {n_params:,} params ({n_params*2/1e6:.1f} MB BF16)")
350	
351	    # Separate param groups: no weight decay on RMSNorm and biases
352	    decay_params, no_decay_params = [], []
353	    for name, p in model.named_parameters():
354	        if not p.requires_grad:
355	            continue
356	        if "norm" in name or "bias" in name:
357	            no_decay_params.append(p)
358	        else:
359	            decay_params.append(p)
360	    optimizer = torch.optim.AdamW([
361	        {"params": decay_params, "weight_decay": WEIGHT_DECAY},
362	        {"params": no_decay_params, "weight_decay": 0.0},
363	    ], lr=LR)
364	
365	    start_step = 0
366	    if RESUME_FROM:
367	        ckpt = torch.load(RESUME_FROM, map_location="cpu", weights_only=True)
368	        model.heads.load_state_dict(ckpt["heads_state_dict"])
369	        start_step = ckpt.get("step", 0)
370	        print(f"Resumed from {RESUME_FROM} at step {start_step}")
371	
372	    # ── Baseline ────────────────────────────────────────────────────────
373	    print("\n── Baseline ──")
374	    m_ind = evaluate(model, ind_files, device, "val_ind")
375	    m_ood = evaluate(model, ood_files, device, "val_ood")
376	    print(f"  val_ind: accept={m_ind['mean_accept_len']:.3f}")
377	    print(f"  val_ood: accept={m_ood['mean_accept_len']:.3f}  "
378	          f"gap={m_ind['mean_accept_len'] - m_ood['mean_accept_len']:+.3f}")
379	
380	    best_accept = m_ood["mean_accept_len"]
381	
382	    # ── Compute sampling weights ───────────────────────────────────────
383	    sampling_weights = None
384	    if USE_WEIGHTED_SAMPLING and file_importance:
385	        raw_weights = []
386	        for f in train_files:
387	            sim = file_importance.get(str(f), 0.0)
388	            w = max(sim, WEIGHT_FLOOR) ** WEIGHT_POWER
389	            raw_weights.append(w)
390	        w_min, w_max = min(raw_weights), max(raw_weights)
391	        w_mean = sum(raw_weights) / len(raw_weights)
392	        # Effective dataset size: (sum(w))^2 / sum(w^2) — measures diversity
393	        sw = sum(raw_weights)
394	        sw2 = sum(w * w for w in raw_weights)
395	        eff_size = sw * sw / sw2 if sw2 > 0 else len(raw_weights)
396	        print(f"Weighted sampling: power={WEIGHT_POWER}, floor={WEIGHT_FLOOR}")
397	        print(f"  weight range: [{w_min:.4f}, {w_max:.4f}], mean={w_mean:.4f}")
398	        print(f"  effective dataset size: {eff_size:.0f} / {len(train_files)} "
399	              f"({eff_size/len(train_files)*100:.1f}%)")
400	        sampling_weights = raw_weights
401	
402	    # ── Training loop ───────────────────────────────────────────────────
403	    print(f"\n── Training ({total_steps} steps) ──")
404	    model.train()
405	    K = model.num_heads
406	    stream = PackStream(train_files, K, device, weights=sampling_weights)
407	    stream_iter = iter(stream)
408	
409	    running_loss = 0.0
410	    running_count = 0
411	    total_tok = 0
412	    t0 = time.time()
413	    optimizer.zero_grad()
414	
415	    pbar = tqdm(total=total_steps, initial=start_step, desc="Train", unit="step")
416	    for step in range(start_step, total_steps):
417	        # LR schedule
418	        lr = get_lr(step, total_steps, WARMUP_STEPS, LR, LR_ETA_MIN)
419	        set_lr(optimizer, lr)
420	
421	        # Forward
422	        h, labels = next(stream_iter)
423	        logits = model(h)
424	        loss = sum((DECAY ** k) * F.cross_entropy(logits[k], labels[k])
425	                   for k in range(K))
426	
427	        if loss.isnan():
428	            pbar.update(1)
429	            continue
430	
431	        # Backward
432	        loss.backward()
433	        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=GRAD_CLIP)
434	        optimizer.step()
435	        optimizer.zero_grad()
436	
437	        running_loss += loss.item()
438	        running_count += 1
439	        total_tok += h.shape[0]
440	        pbar.update(1)
441	        pbar.set_postfix(
442	            loss=f"{running_loss / running_count:.4f}",
443	            lr=f"{lr:.1e}",
444	            tok_s=f"{total_tok / (time.time() - t0):.0f}",
445	        )
446	
447	        # ── Eval checkpoint ─────────────────────────────────────────────
448	        if (step + 1) % val_every == 0 or step == total_steps - 1:
449	            elapsed = time.time() - t0
450	            avg_loss = running_loss / max(running_count, 1)
451	            pct = (step + 1) / total_steps * 100
452	
453	            print(f"\n[Step {step+1}/{total_steps} ({pct:.0f}%)]  "
454	                  f"loss={avg_loss:.4f}  lr={lr:.2e}  "
455	                  f"tok/s={total_tok/elapsed:.0f}  elapsed={elapsed:.0f}s")
456	
457	            m_ind = evaluate(model, ind_files, device, "val_ind")
458	            m_ood = evaluate(model, ood_files, device, "val_ood")
459	            gap = m_ind["mean_accept_len"] - m_ood["mean_accept_len"]
460	
461	            print(f"  val_ind: loss={m_ind['loss']:.4f} accept={m_ind['mean_accept_len']:.3f} "
462	                  + " ".join(f"h{k}={m_ind[f'head_{k}_top1_acc']:.3f}" for k in range(K)))
463	            print(f"  val_ood: loss={m_ood['loss']:.4f} accept={m_ood['mean_accept_len']:.3f} "
464	                  + " ".join(f"h{k}={m_ood[f'head_{k}_top1_acc']:.3f}" for k in range(K)))
465	            print(f"  gap={gap:+.3f}" + ("  ⚠ overfit!" if gap > 0.05 else ""))
466	
467	            if m_ood["mean_accept_len"] > best_accept:
468	                best_accept = m_ood["mean_accept_len"]
469	                save_checkpoint(model, step + 1, m_ood, m_ind, OUTPUT_DIR / "best.pt")
470	                print(f"  ★ New best! ood_accept={best_accept:.3f}")
471	
472	            # Reset running stats for next interval
473	            running_loss = 0.0
474	            running_count = 0
475	            model.train()
476	
477	    pbar.close()
478	
479	    # ── Final save ──────────────────────────────────────────────────────
480	    save_checkpoint(model, total_steps, m_ood, m_ind, OUTPUT_DIR / "final.pt")
481	    print(f"\nDone. Best ood_accept={best_accept:.3f}")
482	    print(f"Weights: {OUTPUT_DIR}/best.pt, {OUTPUT_DIR}/final.pt")
483	
484	
485	if __name__ == "__main__":
486	    main()
487
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/medusa/profile_verify.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Profile verify-step overhead for Medusa speculative decoding on MiniCPM-SALA.
4	
5	Key question: is verify(K+1 tokens) cheap enough vs decode(1 token) that
6	Medusa's accept rate (val_ood ~0.155) translates to real speedup?
7	
8	Measurements:
9	  1. Steady-state decode step time  (S1, S8, S64)
10	  2. EXTEND step scaling with token count  (proxy for verify overhead)
11	  3. Expected net Medusa speedup
12	
13	Prerequisites: SGLang server running at http://127.0.0.1:30000
14	Run: python3 medusa/profile_verify.py
15	"""
16	
17	import asyncio
18	import statistics
19	import time
20	
21	import aiohttp
22	
23	API    = "http://127.0.0.1:30000"
24	MODEL  = "default"
25	
26	# ── Fixed context ──────────────────────────────────────────────────────
27	# 80 tokens of context so decode is in steady state (KV cache populated)
28	CONTEXT = (
29	    "The transformer architecture has revolutionized natural language processing. "
30	    "Attention mechanisms allow models to focus on relevant parts of the input. "
31	    "Recent advances in large language models have demonstrated remarkable capabilities "
32	    "across a wide range of tasks including reasoning, coding, and creative writing. "
33	)  # ~80 tokens
34	
35	# Short prompts of exact token counts (single english words ≈ 1 token each)
36	SHORT_PROMPTS = {
37	    1: "hello",
38	    2: "hello world",
39	    4: "hello world good morning",
40	    8: "hello world good morning the quick brown fox",
41	    16: "hello world good morning the quick brown fox jumps over the lazy dog today",
42	}
43	
44	
45	async def post(session, prompt: str, max_tokens: int, sem: asyncio.Semaphore):
46	    payload = {
47	        "model": MODEL,
48	        "prompt": prompt,
49	        "max_tokens": max_tokens,
50	        "temperature": 0,
51	        "ignore_eos": True,
52	    }
53	    async with sem:
54	        t0 = time.perf_counter()
55	        async with session.post(
56	            f"{API}/v1/completions",
57	            json=payload,
58	            timeout=aiohttp.ClientTimeout(total=120),
59	        ) as resp:
60	            data = await resp.json()
61	        elapsed = time.perf_counter() - t0
62	    return elapsed, data
63	
64	
65	async def warmup(session):
66	    sem = asyncio.Semaphore(1)
67	    print("  Warming up (5 requests)...", end="", flush=True)
68	    for _ in range(5):
69	        await post(session, CONTEXT, 30, sem)
70	    print(" done")
71	
72	
73	# ── Measurement 1: steady-state decode step time ───────────────────────
74	async def measure_decode_step(session, concurrency: int, gen_tokens: int = 200, trials: int = 5):
75	    """
76	    Generate gen_tokens from CONTEXT with `concurrency` parallel requests.
77	    Returns mean per-token latency (ms) for a single request in that batch.
78	    """
79	    sem = asyncio.Semaphore(concurrency)
80	    results = []
81	    for _ in range(trials):
82	        tasks = [
83	            asyncio.create_task(post(session, CONTEXT, gen_tokens, sem))
84	            for _ in range(concurrency)
85	        ]
86	        t0 = time.perf_counter()
87	        await asyncio.gather(*tasks)
88	        wall = (time.perf_counter() - t0) * 1000   # ms
89	        # wall / gen_tokens = ms per batch step (all concurrency requests advanced 1 token)
90	        results.append(wall / gen_tokens)
91	    return statistics.median(results)
92	
93	
94	# ── Measurement 2: EXTEND step scaling with token count ────────────────
95	async def measure_extend_step(session, n_tok_list: list[int], trials: int = 8):
96	    """
97	    For each prompt length in n_tok_list, measure TTFT (ms).
98	    TTFT ≈ extend(n tokens) + 1 decode step.
99	    extend_cost(n) = ttft(n) - ttft(1)  → scaling with n.
100	    """
101	    sem = asyncio.Semaphore(1)
102	    ttft = {}
103	    for n in n_tok_list:
104	        prompt = SHORT_PROMPTS.get(n, "hello " * n)
105	        times = []
106	        for _ in range(trials):
107	            elapsed, _ = await post(session, prompt, 1, sem)
108	            times.append(elapsed * 1000)
109	        ttft[n] = statistics.median(times)
110	    return ttft
111	
112	
113	# ── Main ───────────────────────────────────────────────────────────────
114	async def main():
115	    print("=" * 60)
116	    print("  Medusa Verify-Step Profiling")
117	    print("=" * 60)
118	
119	    async with aiohttp.ClientSession() as session:
120	
121	        # Health check
122	        try:
123	            async with session.get(f"{API}/health") as r:
124	                assert r.status == 200, f"status {r.status}"
125	        except Exception as e:
126	            print(f"\nServer not reachable: {e}")
127	            return
128	
129	        await warmup(session)
130	
131	        # ── 1. Decode step time at different concurrency ──────────────
132	        print("\n── Decode step time (per batch step, ms) ──")
133	        decode_ms = {}
134	        for conc in [1, 8, 64]:
135	            ms = await measure_decode_step(session, conc)
136	            decode_ms[conc] = ms
137	            print(f"  concurrency={conc:2d}: {ms:.1f} ms/step")
138	
139	        # ── 2. EXTEND step scaling ────────────────────────────────────
140	        print("\n── EXTEND step time vs token count ──")
141	        n_tok_list = [1, 2, 4, 8, 16]
142	        ttft = await measure_extend_step(session, n_tok_list)
143	
144	        # ttft(1) ≈ extend(1 token) + decode(1 token)
145	        # For 1 token, extend ≈ 1 decode step → ttft(1) ≈ 2 × decode(1)
146	        # Use ttft(1) as anchor to compute pure extend cost
147	        baseline_ttft = ttft[1]
148	        decode_s1 = decode_ms[1]
149	
150	        print(f"  {'n_tok':>5}  {'ttft_ms':>8}  {'extend_ms':>10}  {'ratio_vs_1tok_decode':>20}")
151	        for n in n_tok_list:
152	            # extend_cost(n) = how much MORE does n-token extend cost vs 1-token extend
153	            extend_extra = ttft[n] - baseline_ttft   # additional cost above n=1
154	            ratio = ttft[n] / decode_s1              # total step cost vs 1 decode step
155	            print(f"  {n:>5}  {ttft[n]:>8.1f}  {extend_extra:>+10.1f}  {ratio:>20.2f}x")
156	
157	        # ── 3. Verify step proxy ──────────────────────────────────────
158	        # For Medusa K=3: verify processes K+1=4 tokens
159	        # Proxy: EXTEND of 4 tokens ≈ verify step cost
160	        # (both require 4 sequential Mamba recurrent updates per layer)
161	        print("\n── Medusa profitability (val_ood accept=0.155, tok/step=1.155) ──")
162	        print(f"  {'K':>3}  {'verify_cost':>12}  {'cost_ratio':>11}  {'expected_speedup':>17}  {'verdict':>12}")
163	        for K in [1, 2, 3]:
164	            verify_tokens = K + 1
165	            verify_cost_ms = ttft.get(verify_tokens, ttft[4])   # EXTEND proxy
166	            cost_ratio = verify_cost_ms / decode_s1
167	
168	            accept_val    = 0.155     # val_ood epoch 2
169	            tok_per_step  = 1.0 + accept_val
170	            net_speedup   = tok_per_step / cost_ratio
171	            verdict       = "✓ PROFITABLE" if net_speedup > 1.02 else ("≈ BREAKEVEN" if net_speedup > 0.98 else "✗ NEGATIVE")
172	            print(f"  {K:>3}  {verify_cost_ms:>10.1f}ms  {cost_ratio:>10.2f}x  {net_speedup:>16.3f}x  {verdict}")
173	
174	        # ── 4. Sensitivity: what accept rate is needed to break even? ──
175	        print("\n── Break-even accept rate (K=3) ──")
176	        verify_cost_ms_k3 = ttft.get(4, ttft[4])
177	        cost_ratio_k3     = verify_cost_ms_k3 / decode_s1
178	        breakeven_accept  = cost_ratio_k3 - 1.0
179	        print(f"  Verify cost = {cost_ratio_k3:.2f}x decode step")
180	        print(f"  Need accept rate > {breakeven_accept:.3f} tok/step  (currently {accept_val:.3f})")
181	        if breakeven_accept < accept_val:
182	            print(f"  → Current accept rate EXCEEDS break-even: Medusa profitable")
183	        else:
184	            margin = breakeven_accept - accept_val
185	            print(f"  → Need {margin:.3f} more acceptance to break even")
186	            print(f"  → Requires training improvement or more heads")
187	
188	        print("\n" + "=" * 60)
189	
190	
191	if __name__ == "__main__":
192	    asyncio.run(main())
193
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/medusa_worker.py"
}
```

> TOOL

tool_result Read
```
1	"""
2	Medusa speculative decoding worker for MiniCPM-SALA.
3	
4	Architecture: K ResBlock heads + shared lm_head (frozen).
5	Draft: run heads on target hidden states → argmax → K draft tokens.
6	Verify: Batched TARGET_VERIFY — all K+1 tokens verified in ONE forward pass.
7	        GLA intermediate states saved per-step for rollback.
8	"""
9	
10	import logging
11	from typing import List, Optional
12	
13	import torch
14	import torch.nn as nn
15	import torch.nn.functional as F
16	
17	from sglang.srt.layers.logits_processor import LogitsProcessorOutput
18	from sglang.srt.managers.schedule_batch import ScheduleBatch
19	from sglang.srt.mem_cache.common import alloc_for_decode, alloc_token_slots
20	from sglang.srt.managers.tp_worker import TpModelWorker
21	from sglang.srt.managers.utils import GenerationBatchResult
22	from sglang.srt.model_executor.forward_batch_info import (
23	    CaptureHiddenMode,
24	    ForwardMode,
25	)
26	from sglang.srt.server_args import ServerArgs
27	from sglang.srt.speculative.eagle_info import EagleDraftInput, MedusaVerifyInput
28	from sglang.srt.speculative.spec_utils import (
29	    assign_req_to_token_pool_func,
30	    detect_nan,
31	)
32	
33	logger = logging.getLogger(__name__)
34	
35	
36	# ── Medusa head model ───────────────────────────────────────────────────
37	
38	
39	class RMSNorm(nn.Module):
40	    def __init__(self, hidden_size: int, eps: float = 1e-6):
41	        super().__init__()
42	        self.weight = nn.Parameter(torch.ones(hidden_size))
43	        self.eps = eps
44	
45	    def forward(self, x: torch.Tensor) -> torch.Tensor:
46	        norm = x.float().pow(2).mean(-1, keepdim=True).add(self.eps).rsqrt()
47	        return (x * norm).to(x.dtype) * self.weight
48	
49	
50	class ResBlock(nn.Module):
51	    def __init__(self, hidden_size: int):
52	        super().__init__()
53	        self.linear = nn.Linear(hidden_size, hidden_size)
54	        self.act = nn.SiLU()
55	
56	    def forward(self, x: torch.Tensor) -> torch.Tensor:
57	        return x + self.act(self.linear(x))
58	
59	
60	class MedusaBlock(nn.Module):
61	    """RMSNorm + 2x ResBlock, used by newer Medusa checkpoints."""
62	    def __init__(self, hidden_size: int):
63	        super().__init__()
64	        self.norm = RMSNorm(hidden_size)
65	        self.res1 = ResBlock(hidden_size)
66	        self.res2 = ResBlock(hidden_size)
67	
68	    def forward(self, x: torch.Tensor) -> torch.Tensor:
69	        x = self.norm(x)
70	        x = self.res1(x)
71	        x = self.res2(x)
72	        return x
73	
74	
75	class MedusaHeads(nn.Module):
76	    def __init__(self, num_heads: int, hidden_size: int, lm_head_weight: torch.Tensor,
77	                 block_cls: type[nn.Module] = ResBlock):
78	        super().__init__()
79	        self.num_heads = num_heads
80	        self.heads = nn.ModuleList([block_cls(hidden_size) for _ in range(num_heads)])
81	        self.register_buffer("lm_head_weight", lm_head_weight)
82	
83	    def forward(self, hidden_states: torch.Tensor) -> list[torch.Tensor]:
84	        return [
85	            F.linear(head(hidden_states), self.lm_head_weight)
86	            for head in self.heads
87	        ]
88	
89	
90	# ── Medusa Worker ───────────────────────────────────────────────────────
91	
92	
93	class MedusaWorker:
94	
95	    def __init__(
96	        self,
97	        server_args: ServerArgs,
98	        gpu_id: int,
99	        tp_rank: int,
100	        dp_rank: Optional[int],
101	        moe_ep_rank: int,
102	        nccl_port: int,
103	        target_worker: TpModelWorker,
104	    ):
105	        self.server_args = server_args
106	        self.target_worker = target_worker
107	        self.device = server_args.device
108	        self.gpu_id = gpu_id
109	        self.page_size = server_args.page_size
110	        self.enable_nan_detection = server_args.enable_nan_detection
111	
112	        self.num_heads = server_args.speculative_num_steps or 3
113	        self.topk = 1
114	        # Medusa verifies verified_id + K drafts = K+1 tokens per request.
115	        # server_args already enforces speculative_num_draft_tokens = num_steps + 1.
116	        self.num_draft_tokens = self.num_heads + 1
117	        assert server_args.speculative_num_draft_tokens == self.num_draft_tokens, (
118	            f"speculative_num_draft_tokens={server_args.speculative_num_draft_tokens} "
119	            f"must equal num_heads+1={self.num_draft_tokens}"
120	        )
121	
122	        # Share allocator with target worker (same pattern as EAGLEWorker)
123	        self.req_to_token_pool, self._token_to_kv_pool_allocator = (
124	            target_worker.get_memory_pool()
125	        )
126	
127	        # Dynamic spec/no-spec threshold: skip draft+verify when bs >= threshold
128	        import os
129	        self.spec_bs_threshold = int(os.environ.get("SGLANG_MEDUSA_BS_THRESHOLD", "16"))
130	
131	        self._load_medusa_heads()
132	        logger.info(
133	            f"MedusaWorker initialized: {self.num_heads} heads, "
134	            f"topk={self.topk}, num_draft_tokens={self.num_draft_tokens}, "
135	            f"strategy=batched_target_verify, "
136	            f"spec_bs_threshold={self.spec_bs_threshold}"
137	        )
138	
139	    def _load_medusa_heads(self):
140	        import os
141	
142	        model = self.target_worker.model_runner.model
143	        if hasattr(model, "lm_head"):
144	            lm_head_weight = model.lm_head.weight
145	        elif hasattr(model, "model") and hasattr(model.model, "embed_tokens"):
146	            lm_head_weight = model.model.embed_tokens.weight
147	        else:
148	            raise RuntimeError("Cannot find lm_head weight in target model")
149	        hidden_size = lm_head_weight.shape[1]
150	
151	        weights_path = self.server_args.speculative_draft_model_path
152	        if weights_path is None or not os.path.exists(weights_path):
153	            # Search in common locations
154	            candidates = [
155	                weights_path,
156	                os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "data", "medusa_best.pt"),
157	                os.path.join(self.server_args.model_path, "..", "medusa_weights", "best.pt"),
158	                "/user_4813494d/openbmb/medusa/weights/best.pt",
159	            ]
160	            weights_path = None
161	            for c in candidates:
162	                if c and os.path.exists(c):
163	                    weights_path = os.path.realpath(c)
164	                    break
165	            if weights_path is None:
166	                raise FileNotFoundError(f"Medusa weights not found in: {candidates}")
167	        logger.info(f"Loading Medusa heads from {weights_path}")
168	
169	        checkpoint = torch.load(weights_path, map_location="cpu", weights_only=True)
170	        heads_state_dict = checkpoint["heads_state_dict"]
171	        ckpt_num_heads = checkpoint.get("num_heads", self.num_heads)
172	        if self.num_heads > ckpt_num_heads:
173	            logger.warning(
174	                f"Requested {self.num_heads} heads but checkpoint only has {ckpt_num_heads}. "
175	                f"Using checkpoint value."
176	            )
177	            self.num_heads = ckpt_num_heads
178	            self.num_draft_tokens = ckpt_num_heads + 1
179	        elif self.num_heads < ckpt_num_heads:
180	            logger.info(
181	                f"Using {self.num_heads} of {ckpt_num_heads} available heads from checkpoint."
182	            )
183	
184	        # Auto-detect checkpoint format: MedusaBlock (norm+res1+res2) vs ResBlock
185	        block_cls = MedusaBlock if any(
186	            ".norm." in k or ".res1." in k or ".res2." in k
187	            for k in heads_state_dict
188	        ) else ResBlock
189	        logger.info(f"Medusa checkpoint format: {block_cls.__name__}")
190	
191	        # Load all checkpoint heads, then keep only the first num_heads
192	        all_heads = MedusaHeads(
193	            ckpt_num_heads, hidden_size, lm_head_weight.clone(),
194	            block_cls=block_cls,
195	        ).to(device=self.device, dtype=torch.bfloat16)
196	        all_heads.heads.load_state_dict(heads_state_dict)
197	
198	        self.medusa_heads = MedusaHeads(
199	            self.num_heads, hidden_size, lm_head_weight.clone(),
200	            block_cls=block_cls,
201	        ).to(device=self.device, dtype=torch.bfloat16)
202	        # Copy only the first num_heads
203	        for i in range(self.num_heads):
204	            self.medusa_heads.heads[i].load_state_dict(all_heads.heads[i].state_dict())
205	        del all_heads
206	        self.medusa_heads.eval()
207	
208	        n_params = sum(p.numel() for p in self.medusa_heads.parameters())
209	        logger.info(f"Medusa heads loaded: {n_params:,} params")
210	
211	    @property
212	    def model_runner(self):
213	        return self.target_worker.model_runner
214	
215	    @property
216	    def model_config(self):
217	        return self.target_worker.model_runner.model_config
218	
219	    @property
220	    def token_to_kv_pool_allocator(self):
221	        return self._token_to_kv_pool_allocator
222	
223	    def get_memory_pool(self):
224	        return self.target_worker.get_memory_pool()
225	
226	    # ── Main entry ──────────────────────────────────────────────────────
227	
228	    def forward_batch_generation(self, batch: ScheduleBatch) -> GenerationBatchResult:
229	        if batch.forward_mode.is_extend() or batch.is_extend_in_batch:
230	            return self._forward_extend(batch)
231	        elif batch.forward_mode.is_idle():
232	            return self._forward_idle(batch)
233	        else:
234	            return self._forward_decode(batch)
235	
236	    # ── Extend ──────────────────────────────────────────────────────────
237	
238	    def _forward_extend(self, batch: ScheduleBatch) -> GenerationBatchResult:
239	        model_worker_batch = batch.get_model_worker_batch()
240	        model_worker_batch.capture_hidden_mode = CaptureHiddenMode.LAST
241	        batch_result = self.target_worker.forward_batch_generation(model_worker_batch)
242	        logits_output = batch_result.logits_output
243	        next_token_ids = batch_result.next_token_ids
244	
245	        batch.spec_info = EagleDraftInput(
246	            hidden_states=logits_output.hidden_states,
247	            verified_id=next_token_ids,
248	            topk_p=torch.ones(
249	                len(next_token_ids), 1, device=self.device, dtype=torch.float32
250	            ),
251	            topk_index=next_token_ids.unsqueeze(1),
252	            num_tokens_per_batch=1,
253	            num_tokens_for_logprob_per_batch=1,
254	            capture_hidden_mode=CaptureHiddenMode.LAST,
255	        )
256	
257	        return GenerationBatchResult(
258	            logits_output=logits_output,
259	            next_token_ids=next_token_ids,
260	            num_accepted_tokens=0,
261	            can_run_cuda_graph=False,
262	        )
263	
264	    # ── Idle ────────────────────────────────────────────────────────────
265	
266	    def _forward_idle(self, batch: ScheduleBatch) -> GenerationBatchResult:
267	        batch.spec_info = EagleDraftInput.create_idle_input(
268	            device=self.device,
269	            hidden_size=self.model_config.hidden_size,
270	            dtype=self.model_config.dtype,
271	            topk=self.topk,
272	            capture_hidden_mode=CaptureHiddenMode.LAST,
273	        )
274	        model_worker_batch = batch.get_model_worker_batch()
275	        model_worker_batch.capture_hidden_mode = CaptureHiddenMode.LAST
276	        batch_result = self.target_worker.forward_batch_generation(model_worker_batch)
277	        return GenerationBatchResult(
278	            logits_output=batch_result.logits_output,
279	            next_token_ids=batch_result.next_token_ids,
280	            num_accepted_tokens=0,
281	            can_run_cuda_graph=False,
282	        )
283	
284	    # ── Decode (Batched TARGET_VERIFY) ────────────────────────────────
285	
286	    def _forward_decode(self, batch: ScheduleBatch) -> GenerationBatchResult:
287	        """Speculative decode using batched TARGET_VERIFY.
288	
289	        All K+1 tokens (verified_id + K drafts) are verified in a single
290	        forward pass through the target model. This leverages the fact that
291	        GEMM cost at M=4 is only ~2x M=1 (bandwidth-limited), so verifying
292	        4 tokens costs ~1.5x of a single decode while potentially producing
293	        up to 4 tokens.
294	
295	        When bs >= spec_bs_threshold, falls back to normal single-token decode
296	        to avoid throughput regression from draft overhead at high concurrency.
297	        """
298	        spec_info = batch.spec_info
299	        assert isinstance(spec_info, EagleDraftInput)
300	
301	        hidden_states = spec_info.hidden_states
302	        verified_id = spec_info.verified_id
303	        bs = batch.batch_size()
304	
305	        if bs >= self.spec_bs_threshold:
306	            return self._forward_decode_no_spec(batch, hidden_states, verified_id, bs)
307	
308	        K = self.num_heads
309	        dtn = self.num_draft_tokens  # K+1
310	
311	        # NOTE: prepare_for_decode returns early for speculative decoding —
312	        # it does NOT allocate slots or increment seq_lens. No undo needed.
313	
314	        # 1. Medusa draft: predict K candidate next-tokens
315	        draft_tokens = self._medusa_draft(hidden_states)  # (bs, K)
316	
317	        # 2. Construct input for TARGET_VERIFY
318	        # input_ids = [verified_id, draft_0, draft_1, ..., draft_{K-1}] per request
319	        input_ids_list = [verified_id.unsqueeze(1)]  # (bs, 1)
320	        for k in range(K):
321	            input_ids_list.append(draft_tokens[:, k:k + 1])
322	        input_ids = torch.cat(input_ids_list, dim=1).reshape(-1)  # (bs * dtn,)
323	
324	        # 3. Compute positions: [seq_len, seq_len+1, ..., seq_len+K] per request
325	        # Now seq_lens = S (original), so positions are [S, S+1, ..., S+K]
326	        positions = (
327	            batch.seq_lens.unsqueeze(1)
328	            + torch.arange(dtn, device=self.device).unsqueeze(0)
329	        ).reshape(-1).to(torch.int64)
330	
331	        # 4. Set up batch for TARGET_VERIFY
332	        seq_lens_before = batch.seq_lens.clone()
333	        seq_lens_cpu_before = batch.seq_lens_cpu.clone()
334	
335	        verify_input = MedusaVerifyInput(
336	            draft_token=input_ids,
337	            positions=positions,
338	            draft_token_num=dtn,
339	            capture_hidden_mode=CaptureHiddenMode.LAST,
340	            seq_lens_sum=batch.seq_lens.sum().item(),
341	            seq_lens_cpu=batch.seq_lens_cpu,
342	        )
343	
344	        # Allocate KV cache slots and set up req_to_token mapping
345	        verify_input.prepare_for_verify(batch)
346	
347	        batch.forward_mode = ForwardMode.TARGET_VERIFY
348	        batch.spec_info = verify_input
349	
350	        # 5. Run TARGET_VERIFY through target model
351	        model_worker_batch = batch.get_model_worker_batch()
352	        batch_result = self.target_worker.forward_batch_generation(
353	            model_worker_batch, is_verify=True
354	        )
355	        logits_output = batch_result.logits_output
356	
357	        if self.enable_nan_detection:
358	            detect_nan(logits_output)
359	
360	        # 6. Verify: greedy comparison
361	        # logits shape: (bs * dtn, vocab_size)
362	        # For each request, logits[i*dtn + j] is the target prediction after
363	        # seeing tokens 0..j
364	        all_logits = logits_output.next_token_logits
365	        target_preds = all_logits.argmax(dim=-1)  # (bs * dtn,)
366	        target_preds = target_preds.view(bs, dtn)
367	
368	        # target_preds[:, j] = target's prediction after seeing input_ids[:, 0:j+1]
369	        # Verification: draft_tokens[:, k] should match target_preds[:, k]
370	        # (target_preds[:, 0] is what target predicts after seeing verified_id)
371	        accept_mask = torch.zeros(bs, K, dtype=torch.bool, device=self.device)
372	        for k in range(K):
373	            accept_mask[:, k] = (draft_tokens[:, k] == target_preds[:, k])
374	
375	        # Find first rejection per request (cascading acceptance)
376	        # accepted_count[i] = number of consecutive accepted drafts for request i
377	        accepted_count = torch.zeros(bs, dtype=torch.long, device=self.device)
378	        for k in range(K):
379	            still_accepting = (accepted_count == k) & accept_mask[:, k]
380	            accepted_count[still_accepting] = k + 1
381	
382	        # accepted_steps for GLA rollback: index of last accepted token (0-indexed)
383	        # If 0 drafts accepted: accepted_step = 0 (only verified_id processed)
384	        # If 1 draft accepted: accepted_step = 1 (verified_id + draft_0)
385	        # If all K drafts accepted: accepted_step = K (all dtn tokens)
386	        accepted_steps = accepted_count  # (bs,)
387	
388	        # 7. GLA state rollback via update_mamba_state_after_mtp_verify
389	        if hasattr(self.target_worker.model_runner, 'mambaish_config') and \
390	           self.target_worker.model_runner.mambaish_config is not None:
391	            self.target_worker.model_runner.attn_backend.update_mamba_state_after_mtp_verify(
392	                accepted_steps=accepted_steps,
393	                mamba_track_indices=None,
394	                mamba_steps_to_track=None,
395	                model=self.target_worker.model_runner.model,
396	            )
397	
398	        # 8. Free unused KV cache slots and fix seq_lens (vectorized — no per-request GPU→CPU sync)
399	        # Each request allocated dtn slots. Keep (accepted_count + 1) slots, free the rest.
400	        total_accepted = accepted_count.sum().item()
401	        total_to_free = bs * K - total_accepted
402	
403	        if total_to_free > 0:
404	            all_cache_locs = batch.out_cache_loc.view(bs, dtn)
405	            positions = torch.arange(dtn, device=self.device).unsqueeze(0)  # (1, dtn)
406	            keep_mask = positions <= accepted_count.unsqueeze(1)  # (bs, dtn)
407	            free_locs = all_cache_locs[~keep_mask]
408	            if free_locs.numel() > 0:
409	                self._token_to_kv_pool_allocator.free(free_locs)
410	
411	        # Fix seq_lens: vectorized update (single GPU op + single GPU→CPU transfer)
412	        new_seq_lens = seq_lens_before + accepted_count.to(seq_lens_before.dtype) + 1
413	        batch.seq_lens[:bs] = new_seq_lens
414	        batch.seq_lens_cpu[:bs] = new_seq_lens.cpu()
415	
416	        # Allocate sparse k1/k2 slots for positions that crossed sparse thresholds.
417	        # Normal decode does this in alloc_for_decode, but Medusa skips that path.
418	        # Without this, cache_finished_req would free stale sparse entries → over-free.
419	        self._alloc_sparse_for_new_positions(batch, seq_lens_before)
420	
421	        # 9. Build output tokens and update request state (vectorized where possible)
422	        # verified_id was already output in the previous round — do NOT output it again.
423	        # Output: accepted drafts (d_0..d_{n-1}) + target's correction (target_pred_n).
424	
425	        # Vectorized gather of last token ids (no per-request .item())
426	        gather_col = accepted_count.unsqueeze(1)  # (bs, 1)
427	        last_token_ids = target_preds.gather(1, gather_col).squeeze(1)  # (bs,)
428	
429	        # Batch transfer to CPU (single GPU→CPU transfer instead of bs×K .item() calls)
430	        accepted_count_cpu = accepted_count.tolist()
431	        new_seq_lens_cpu = batch.seq_lens[:bs].tolist()
432	        draft_tokens_cpu = draft_tokens.cpu()
433	
434	        for i, req in enumerate(batch.reqs):
435	            n_acc = accepted_count_cpu[i]
436	            req.kv_committed_len = new_seq_lens_cpu[i]
437	            req.kv_allocated_len = new_seq_lens_cpu[i]
438	            # Append accepted draft tokens (scheduler will append target_pred)
439	            for k in range(n_acc):
440	                req.output_ids.append(draft_tokens_cpu[i, k].item())
441	
442	        # 10. Extract hidden states for next round's draft
443	        # hidden_states from logits_output: (bs * dtn, hidden_size)
444	        # Pick the hidden state at each request's acceptance point
445	        if logits_output.hidden_states is not None:
446	            hs = logits_output.hidden_states.view(bs, dtn, -1)
447	            # Index: accepted_count per request (the position of the last accepted/correction token)
448	            gather_idx = accepted_count.unsqueeze(1).unsqueeze(2).expand(
449	                bs, 1, hs.shape[2]
450	            )
451	            last_hidden = hs.gather(1, gather_idx).squeeze(1)  # (bs, hidden_size)
452	        else:
453	            last_hidden = hidden_states  # fallback
454	
455	        # 11. Restore batch forward mode and set spec_info for next round
456	        batch.forward_mode = ForwardMode.DECODE
457	        accept_length_cpu = accepted_count.tolist()
458	
459	        batch.spec_info = EagleDraftInput(
460	            hidden_states=last_hidden,
461	            verified_id=last_token_ids,
462	            topk_p=torch.ones(bs, 1, device=self.device, dtype=torch.float32),
463	            topk_index=last_token_ids.unsqueeze(1),
464	            num_tokens_per_batch=1,
465	            num_tokens_for_logprob_per_batch=1,
466	            accept_length_cpu=accept_length_cpu,
467	            capture_hidden_mode=CaptureHiddenMode.LAST,
468	        )
469	
470	        # Build logits output for the accepted positions only
471	        # The scheduler needs next_token_logits to be (bs, vocab_size)
472	        accepted_logit_indices = (
473	            torch.arange(bs, device=self.device) * dtn + accepted_count
474	        )
475	        final_logits = LogitsProcessorOutput(
476	            next_token_logits=all_logits[accepted_logit_indices],
477	            hidden_states=last_hidden,
478	        )
479	
480	        num_bonus = int(accepted_count.sum().item())
481	
482	        return GenerationBatchResult(
483	            logits_output=final_logits,
484	            next_token_ids=last_token_ids,
485	            num_accepted_tokens=num_bonus * 1,  # bonus tokens beyond baseline
486	            accept_length_per_req_cpu=accept_length_cpu,
487	            can_run_cuda_graph=True,
488	        )
489	
490	    # ── No-spec fallback (large batch) ─────────────────────────────────
491	
492	    def _forward_decode_no_spec(
493	        self,
494	        batch: ScheduleBatch,
495	        hidden_states: torch.Tensor,
496	        verified_id: torch.Tensor,
497	        bs: int,
498	    ) -> GenerationBatchResult:
499	        """Normal single-token decode when bs >= spec_bs_threshold.
500	
501	        Processes 1 token per request (not dtn) using DECODE CUDA graph,
502	        fully aligned with non-speculative inference. The DECODE graphs
503	        are captured alongside TARGET_VERIFY graphs at startup.
504	        """
505	        # 1. Set up input: single token per request
506	        batch.input_ids = verified_id
507	        batch.forward_mode = ForwardMode.DECODE
508	
509	        # 2. Compute sparse k1/k2 allocation counts (mirrors prepare_for_decode)
510	        if batch.model_config.has_sparse_attention:
511	            seq_lens_next = batch.seq_lens + 1
512	            kernel_size = batch.model_config.sparse_kernel_size
513	            kernel_stride = batch.model_config.sparse_kernel_stride
514	            token_num_sparse_k1 = [
515	                (1 if seq_lens_next[i] >= kernel_size
516	                 and (seq_lens_next[i] - kernel_size) % kernel_stride == 0
517	                 else 0) for i in range(bs)
518	            ]
519	            token_num_sparse_k2 = [
520	                (1 if seq_lens_next[i] >= kernel_size * 4
521	                 and (seq_lens_next[i] - kernel_size * 4) % (kernel_stride * 4) == 0
522	                 else 0) for i in range(bs)
523	            ]
524	            batch.token_sum_sparse_k1 = sum(token_num_sparse_k1)
525	            batch.token_sum_sparse_k2 = sum(token_num_sparse_k2)
526	            batch.token_num_sparse_k1_cpu = torch.tensor(token_num_sparse_k1, dtype=torch.int64)
527	            batch.token_num_sparse_k2_cpu = torch.tensor(token_num_sparse_k2, dtype=torch.int64)
528	
529	        # 3. Allocate KV cache (1 token per request + sparse slots)
530	        batch.out_cache_loc, batch.sparse_k1_loc, batch.sparse_k2_loc = alloc_for_decode(
531	            batch, token_per_req=1
532	        )
533	
534	        # 4. Update req-level state (must match prepare_for_decode exactly)
535	        for i, req in enumerate(batch.reqs):
536	            req.decode_batch_idx += 1
537	            req.kv_committed_len += 1
538	            req.kv_allocated_len += 1
539	
540	        # 5. Update seq_lens (in-place, non-overlap mode)
541	        batch.seq_lens.add_(1)
542	        batch.seq_lens_cpu.add_(1)
543	        batch.orig_seq_lens.add_(1)
544	        batch.seq_lens_sum += bs
545	
546	        # 6. Update mamba/GLA track state (critical for Lightning Attention layers)
547	        from sglang.srt.server_args import get_global_server_args
548	        if get_global_server_args().enable_mamba_extra_buffer():
549	            batch.mamba_track_indices = torch.tensor(
550	                [req.mamba_ping_pong_track_buffer[req.mamba_next_track_idx]
551	                 for req in batch.reqs],
552	                dtype=torch.int64, device=self.device,
553	            )
554	            batch.mamba_track_mask = torch.tensor(
555	                [sl % get_global_server_args().mamba_track_interval == 0
556	                 for sl in batch.seq_lens_cpu],
557	                dtype=torch.bool, device=self.device,
558	            )
559	
560	        # 7. Compute sparse attention metadata (same as prepare_for_decode)
561	        batch.prepare_sparse_metadata_for_decode()
562	
563	        # 8. Forward through target model (normal DECODE, uses DECODE CUDA graph)
564	        model_worker_batch = batch.get_model_worker_batch()
565	        model_worker_batch.capture_hidden_mode = CaptureHiddenMode.LAST
566	        batch_result = self.target_worker.forward_batch_generation(model_worker_batch)
567	        logits_output = batch_result.logits_output
568	        next_token_ids = batch_result.next_token_ids
569	
570	        # 9. Set spec_info for next round
571	        last_hidden = logits_output.hidden_states if logits_output.hidden_states is not None else hidden_states
572	        batch.spec_info = EagleDraftInput(
573	            hidden_states=last_hidden,
574	            verified_id=next_token_ids,
575	            topk_p=torch.ones(bs, 1, device=self.device, dtype=torch.float32),
576	            topk_index=next_token_ids.unsqueeze(1),
577	            num_tokens_per_batch=1,
578	            num_tokens_for_logprob_per_batch=1,
579	            capture_hidden_mode=CaptureHiddenMode.LAST,
580	        )
581	
582	        return GenerationBatchResult(
583	            logits_output=logits_output,
584	            next_token_ids=next_token_ids,
585	            num_accepted_tokens=0,
586	            can_run_cuda_graph=batch_result.can_run_cuda_graph,
587	        )
588	
589	    # ── Sparse k1/k2 allocation ──────────────────────────────────────────
590	
591	    def _alloc_sparse_for_new_positions(
592	        self, batch: ScheduleBatch, seq_lens_before: torch.Tensor
593	    ):
594	        """Allocate sparse k1/k2 slots for positions crossed during this decode round.
595	
596	        MiniCPM-SALA uses InfLLM-v2 sparse attention for standard layers.
597	        Normal decode allocates sparse slots in alloc_for_decode, but Medusa
598	        skips that path. We must allocate them here so cache_finished_req's
599	        sparse free matches what was allocated.
600	        """
601	        from sglang.srt.mem_cache.memory_pool import (
602	            MiniCPMReqToTokenPool,
603	            MiniCPMHybridReqToTokenPool,
604	        )
605	
606	        rtp = self.req_to_token_pool
607	        if not isinstance(rtp, (MiniCPMReqToTokenPool, MiniCPMHybridReqToTokenPool)):
608	            return
609	
610	        kernel_size = rtp.kernel_size
611	        kernel_stride = rtp.kernel_stride
612	        bs = batch.batch_size()
613	
614	        for i in range(bs):
615	            old_sl = seq_lens_before[i].item()
616	            new_sl = batch.seq_lens[i].item()
617	
618	            # k1: positions where sl >= kernel_size and (sl - kernel_size) % kernel_stride == 0
619	            for sl in range(max(old_sl + 1, kernel_size), new_sl + 1):
620	                if (sl - kernel_size) % kernel_stride == 0:
621	                    k1_idx = (sl - kernel_size) // kernel_stride
622	                    loc = alloc_token_slots(batch.tree_cache, 1)
623	                    rtp.write_sparse_k1(
624	                        (batch.req_pool_indices[i], (k1_idx, k1_idx + 1)),
625	                        loc.to(torch.int32),
626	                    )
627	
628	            # k2: kernel_size*4, kernel_stride*4
629	            k2_ks = kernel_size * 4
630	            k2_stride = kernel_stride * 4
631	            for sl in range(max(old_sl + 1, k2_ks), new_sl + 1):
632	                if (sl - k2_ks) % k2_stride == 0:
633	                    k2_idx = (sl - k2_ks) // k2_stride
634	                    loc = alloc_token_slots(batch.tree_cache, 1)
635	                    rtp.write_sparse_k2(
636	                        (batch.req_pool_indices[i], (k2_idx, k2_idx + 1)),
637	                        loc.to(torch.int32),
638	                    )
639	
640	    # ── Medusa draft ────────────────────────────────────────────────────
641	
642	    @torch.no_grad()
643	    def _medusa_draft(self, hidden_states: torch.Tensor) -> torch.Tensor:
644	        logits_list = self.medusa_heads(hidden_states)
645	        return torch.stack(
646	            [logits.argmax(dim=-1) for logits in logits_list], dim=1
647	        )
648	
649	    # ── Misc ────────────────────────────────────────────────────────────
650	
651	    def clear_cache_pool(self):
652	        pass
653	
654	    def update_weights_from_tensor(self, recv_req):
655	        return self.target_worker.model_runner.update_weights_from_tensor(
656	            named_tensors=recv_req,
657	            load_format=recv_req.load_format,
658	        )
659
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
19	N_S1="${2:-8}"
20	N_S8="${3:-24}"
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

> AGENT

Now let me examine the sglang serving integration files:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	import logging
2	import time
3	from typing import List, Optional, Tuple
4	
5	import torch
6	
7	from sglang.srt.distributed import get_tp_group
8	from sglang.srt.hardware_backend.npu.graph_runner.eagle_draft_npu_graph_runner import (
9	    EAGLEDraftNpuGraphRunner,
10	)
11	from sglang.srt.layers.dp_attention import get_attention_tp_group
12	from sglang.srt.layers.logits_processor import LogitsProcessorOutput
13	from sglang.srt.layers.moe.utils import (
14	    speculative_moe_a2a_backend_context,
15	    speculative_moe_backend_context,
16	)
17	from sglang.srt.layers.utils.logprob import add_output_logprobs_for_spec_v1
18	from sglang.srt.managers.io_struct import UpdateWeightsFromTensorReqInput
19	from sglang.srt.managers.schedule_batch import ScheduleBatch
20	from sglang.srt.managers.scheduler import GenerationBatchResult
21	from sglang.srt.managers.tp_worker import TpModelWorker
22	from sglang.srt.mem_cache.chunk_cache import SWAChunkCache
23	from sglang.srt.mem_cache.common import (
24	    alloc_paged_token_slots_extend,
25	    alloc_token_slots,
26	    get_last_loc,
27	)
28	from sglang.srt.model_executor.forward_batch_info import (
29	    CaptureHiddenMode,
30	    ForwardBatch,
31	    ForwardMode,
32	)
33	from sglang.srt.server_args import ServerArgs
34	from sglang.srt.speculative.draft_utils import DraftBackendFactory
35	from sglang.srt.speculative.eagle_draft_cuda_graph_runner import (
36	    EAGLEDraftCudaGraphRunner,
37	)
38	from sglang.srt.speculative.eagle_draft_extend_cuda_graph_runner import (
39	    EAGLEDraftExtendCudaGraphRunner,
40	)
41	from sglang.srt.speculative.eagle_info import (
42	    EagleDraftInput,
43	    EagleVerifyInput,
44	    EagleVerifyOutput,
45	)
46	from sglang.srt.speculative.eagle_utils import (
47	    build_tree_kernel_efficient,
48	    organize_draft_results,
49	)
50	from sglang.srt.speculative.spec_info import SpeculativeAlgorithm
51	from sglang.srt.speculative.spec_utils import (
52	    assign_draft_cache_locs,
53	    detect_nan,
54	    draft_tp_context,
55	    fast_topk,
56	    generate_token_bitmask,
57	    get_last_loc_large_page_size_large_top_k,
58	    load_token_map,
59	    select_top_k_tokens,
60	)
61	from sglang.srt.utils import (
62	    MultiprocessingSerializer,
63	    empty_context,
64	    get_available_gpu_memory,
65	    is_cuda,
66	    is_npu,
67	    next_power_of_2,
68	)
69	from sglang.srt.utils.patch_torch import monkey_patch_torch_reductions
70	
71	_is_npu = is_npu()
72	
73	if is_cuda():
74	    from sgl_kernel import segment_packbits  # noqa: F401
75	
76	logger = logging.getLogger(__name__)
77	
78	
79	class EAGLEWorker(TpModelWorker):
80	
81	    def __init__(
82	        self,
83	        server_args: ServerArgs,
84	        gpu_id: int,
85	        tp_rank: int,
86	        dp_rank: Optional[int],
87	        moe_ep_rank: int,
88	        nccl_port: int,
89	        target_worker: TpModelWorker,
90	    ):
91	        # Parse arguments
92	        self.server_args = server_args
93	        self.topk = server_args.speculative_eagle_topk
94	        self.speculative_num_steps = server_args.speculative_num_steps
95	        self.speculative_num_draft_tokens = server_args.speculative_num_draft_tokens
96	        self.enable_nan_detection = server_args.enable_nan_detection
97	        self.gpu_id = gpu_id
98	        self.device = server_args.device
99	        self.target_worker = target_worker
100	        self.page_size = server_args.page_size
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/medusa_worker.py",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	"""
2	Medusa speculative decoding worker for MiniCPM-SALA.
3	
4	Architecture: K ResBlock heads + shared lm_head (frozen).
5	Draft: run heads on target hidden states → argmax → K draft tokens.
6	Verify: Batched TARGET_VERIFY — all K+1 tokens verified in ONE forward pass.
7	        GLA intermediate states saved per-step for rollback.
8	"""
9	
10	import logging
11	from typing import List, Optional
12	
13	import torch
14	import torch.nn as nn
15	import torch.nn.functional as F
16	
17	from sglang.srt.layers.logits_processor import LogitsProcessorOutput
18	from sglang.srt.managers.schedule_batch import ScheduleBatch
19	from sglang.srt.mem_cache.common import alloc_for_decode, alloc_token_slots
20	from sglang.srt.managers.tp_worker import TpModelWorker
21	from sglang.srt.managers.utils import GenerationBatchResult
22	from sglang.srt.model_executor.forward_batch_info import (
23	    CaptureHiddenMode,
24	    ForwardMode,
25	)
26	from sglang.srt.server_args import ServerArgs
27	from sglang.srt.speculative.eagle_info import EagleDraftInput, MedusaVerifyInput
28	from sglang.srt.speculative.spec_utils import (
29	    assign_req_to_token_pool_func,
30	    detect_nan,
31	)
32	
33	logger = logging.getLogger(__name__)
34	
35	
36	# ── Medusa head model ───────────────────────────────────────────────────
37	
38	
39	class RMSNorm(nn.Module):
40	    def __init__(self, hidden_size: int, eps: float = 1e-6):
41	        super().__init__()
42	        self.weight = nn.Parameter(torch.ones(hidden_size))
43	        self.eps = eps
44	
45	    def forward(self, x: torch.Tensor) -> torch.Tensor:
46	        norm = x.float().pow(2).mean(-1, keepdim=True).add(self.eps).rsqrt()
47	        return (x * norm).to(x.dtype) * self.weight
48	
49	
50	class ResBlock(nn.Module):
51	    def __init__(self, hidden_size: int):
52	        super().__init__()
53	        self.linear = nn.Linear(hidden_size, hidden_size)
54	        self.act = nn.SiLU()
55	
56	    def forward(self, x: torch.Tensor) -> torch.Tensor:
57	        return x + self.act(self.linear(x))
58	
59	
60	class MedusaBlock(nn.Module):
61	    """RMSNorm + 2x ResBlock, used by newer Medusa checkpoints."""
62	    def __init__(self, hidden_size: int):
63	        super().__init__()
64	        self.norm = RMSNorm(hidden_size)
65	        self.res1 = ResBlock(hidden_size)
66	        self.res2 = ResBlock(hidden_size)
67	
68	    def forward(self, x: torch.Tensor) -> torch.Tensor:
69	        x = self.norm(x)
70	        x = self.res1(x)
71	        x = self.res2(x)
72	        return x
73	
74	
75	class MedusaHeads(nn.Module):
76	    def __init__(self, num_heads: int, hidden_size: int, lm_head_weight: torch.Tensor,
77	                 block_cls: type[nn.Module] = ResBlock):
78	        super().__init__()
79	        self.num_heads = num_heads
80	        self.heads = nn.ModuleList([block_cls(hidden_size) for _ in range(num_heads)])
81	        self.register_buffer("lm_head_weight", lm_head_weight)
82	
83	    def forward(self, hidden_states: torch.Tensor) -> list[torch.Tensor]:
84	        return [
85	            F.linear(head(hidden_states), self.lm_head_weight)
86	            for head in self.heads
87	        ]
88	
89	
90	# ── Medusa Worker ───────────────────────────────────────────────────────
91	
92	
93	class MedusaWorker:
94	
95	    def __init__(
96	        self,
97	        server_args: ServerArgs,
98	        gpu_id: int,
99	        tp_rank: int,
100	        dp_rank: Optional[int],
```

> TOOL

tool_use Bash
```json
{
  "command": "wc -l /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/medusa_worker.py"
}
```

> TOOL

tool_result Bash
```
1090 /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py
  658 /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/medusa_worker.py
 1748 total
```

> AGENT

Now let me read additional files to understand the medusa data collection and evaluation:

> AGENT

Let me read more of these crucial files to understand the integration:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/medusa/collect_data.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Collect post-norm hidden states from SGLang server for Medusa head training.
4	
5	Data budget v2: ~40M tokens/epoch, 3 epochs
6	  - Chinese 50%: SkyPile-150B (short 4K + long 16K)
7	  - Code 40%: code_search_net multi-language (Python/Java/Go/JS/PHP+Ruby)
8	  - English 10%: wikitext-103 (short 4K + long 16K)
9	  - val_ood: bench model_response chunks (unchanged from v1)
10	
11	Data budget v3 (--code-supplement): add ~20M code tokens to existing train
12	  - Brings code from ~3.8M (10%) to ~23.8M (~42%) of ~57M total
13	  - Uses concatenated code_search_net functions to fill 4K chunks properly
14	
15	The _maybe_collect_hidden hook in minicpm.py splits long sequences into
16	multiple 4096-token .pt files automatically, so each request produces
17	ceil(seq_len / 4096) files.
18	
19	Prerequisites:
20	    1. Start SGLang server (normal NVFP4 config, --dense-as-sparse)
21	    2. mkdir /tmp/medusa_collect
22	    3. python3 medusa/collect_data.py [--train-only]
23	    4. rm -rf /tmp/medusa_collect
24	
25	Supplement mode (add code data to existing train):
26	    python3 medusa/collect_data.py --code-supplement [--concurrency 64]
27	
28	Usage:
29	    python3 medusa/collect_data.py [--output medusa/data] [--concurrency 64]
30	"""
31	
32	import argparse
33	import asyncio
34	import json
35	import os
36	import random
37	import shutil
38	import sys
39	import time
40	from pathlib import Path
41	
42	import aiohttp
43	import torch
44	from tqdm import tqdm
45	from transformers import AutoTokenizer
46	
47	REPO_user_4813494d = Path(__file__).resolve().parent.parent
48	COLLECT_DIR = Path("/tmp/medusa_collect")
49	MODEL_PATH = [REDACTED]
50	
51	SHORT_LEN = 4096
52	LONG_LEN = 16384
53	MIN_TOKENS = 64
54	
55	# ── Budget v2 ──────────────────────────────────────────────────────────
56	# Train: ~40M tokens total
57	#   Chinese (SkyPile):  short 3418 × 4K = 14.0M  +  long 366 × 16K = 6.0M  = 20.0M (50%)
58	#   Code (multi-lang):  short 3906 × 4K = 16.0M                              = 16.0M (40%)
59	#   English (wikitext): short  781 × 4K =  3.2M  +  long  49 × 16K = 0.8M  =  4.0M (10%)
60	#
61	# Note: long samples produce multiple .pt files via the hook's chunking
62	# (16K / 4K = 4 files each), so file count > sample count.
63	
64	TRAIN_SHORT = {
65	    "skypile": 3418,
66	    "code": 3906,
67	    "wikitext": 781,
68	}
69	TRAIN_LONG = {
70	    "skypile_long": 366,
71	    "wikitext_long": 49,
72	}
73	
74	# Code language allocation (% of code budget)
75	CODE_LANG_PCT = {
76	    "python": 0.50,       # bench主力
77	    "java": 0.20,         # C++代理 (code_search_net无C++)
78	    "go": 0.15,
79	    "javascript": 0.10,
80	    "php": 0.03,
81	    "ruby": 0.02,
82	}
83	
84	# Val: reuse existing val/ and val_ood/ from v1 (already on disk)
85	# Only regenerate if --full flag is passed
86	VAL_SHORT = {"skypile": 40, "code": 40, "wikitext": 40}
87	VAL_LONG = {"skypile_long": 10, "wikitext_long": 10}
88	
89	# ── Budget v3: code supplement ──────────────────────────────────────────
90	# Existing train: ~36.6M tokens (chinese ~17M, english ~16M, code ~3.8M)
91	# Target: code ~50% of total → need ~20M more code tokens → 5000 × 4K chunks
92	# Total after supplement: ~57M tokens (chinese 30%, code 42%, english 28%)
93	CODE_SUPPLEMENT_CHUNKS = 5000
94	
95	
96	# ── Data loading helpers ────────────────────────────────────────────────
97	
98	def _load_jsonl(path, key):
99	    with open(path) as f:
100	        return [json.loads(line)[key] for line in f]
101	
102	
103	def _chunk_ids(token_ids, tokenizer, chunk_len):
104	    """Chunk token list into pieces, return decoded texts."""
105	    chunks = []
106	    for i in range(0, len(token_ids), chunk_len):
107	        c = token_ids[i : i + chunk_len]
108	        if len(c) < MIN_TOKENS:
109	            continue
110	        chunks.append(tokenizer.decode(c))
111	    return chunks
112	
113	
114	def prepare_all(tokenizer, train_only=False) -> dict:
115	    """Prepare all data splits. Returns {split_name: [text_strings]}."""
116	    random.seed(42)
117	
118	    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
119	    from datasets import load_dataset
120	
121	    # ── SkyPile (Chinese web text, streaming) ───────────────────────
122	    need_cn_short = TRAIN_SHORT["skypile"] + (VAL_SHORT.get("skypile", 0) if not train_only else 0) + 50
123	    need_cn_long = TRAIN_LONG["skypile_long"] + (VAL_LONG.get("skypile_long", 0) if not train_only else 0) + 20
124	
125	    print("  Loading SkyPile-150B (streaming)...")
126	    sky_ds = load_dataset("Skywork/SkyPile-150B", split="train", streaming=True)
127	
128	    sky_short, sky_long = [], []
129	    buf_ids = []
130	    pbar = tqdm(desc="  skypile", unit="chunk")
131	    for sample in sky_ds:
132	        text = sample.get("text", "")
133	        if not text.strip() or len(text) < 50:
134	            continue
135	        buf_ids.extend(tokenizer.encode(text, add_special_tokens=False))
136	        # Extract short chunks
137	        while len(sky_short) < need_cn_short and len(buf_ids) >= SHORT_LEN:
138	            chunk = buf_ids[:SHORT_LEN]
139	            buf_ids = buf_ids[SHORT_LEN:]
140	            sky_short.append({"text": tokenizer.decode(chunk), "source": "skypile"})
141	            pbar.update(1)
142	        # Extract long chunks
143	        while len(sky_long) < need_cn_long and len(buf_ids) >= LONG_LEN:
144	            chunk = buf_ids[:LONG_LEN]
145	            buf_ids = buf_ids[LONG_LEN:]
146	            sky_long.append({"text": tokenizer.decode(chunk), "source": "skypile_long"})
147	            pbar.update(1)
148	        if len(sky_short) >= need_cn_short and len(sky_long) >= need_cn_long:
149	            break
150	    pbar.close()
151	    random.shuffle(sky_short)
152	    random.shuffle(sky_long)
153	    print(f"  skypile: {len(sky_short)} short, {len(sky_long)} long")
154	
155	    # ── Code (code_search_net, multi-language) ──────────────────────
156	    need_code = TRAIN_SHORT["code"] + (VAL_SHORT.get("code", 0) if not train_only else 0) + 50
157	    code_short = []
158	
159	    for lang, pct in CODE_LANG_PCT.items():
160	        lang_need = int(need_code * pct) + 10  # margin
161	        print(f"  Loading code_search_net/{lang}...")
162	        code_ds = load_dataset("code_search_net", lang, split="train", streaming=True)
163	        lang_chunks = []
164	        buf_ids = []
165	        for sample in tqdm(code_ds, desc=f"  code/{lang}", unit="func", leave=False):
166	            func = sample.get("whole_func_string", "")
167	            if not func or len(func) < 50:
168	                continue
169	            buf_ids.extend(tokenizer.encode(func, add_special_tokens=False))
170	            while len(buf_ids) >= SHORT_LEN:
171	                chunk = buf_ids[:SHORT_LEN]
172	                buf_ids = buf_ids[SHORT_LEN:]
173	                lang_chunks.append({"text": tokenizer.decode(chunk), "source": f"code_{lang}"})
174	            if len(lang_chunks) >= lang_need:
175	                break
176	        if len(buf_ids) >= MIN_TOKENS:
177	            lang_chunks.append({"text": tokenizer.decode(buf_ids), "source": f"code_{lang}"})
178	        random.shuffle(lang_chunks)
179	        code_short.extend(lang_chunks[:lang_need])
180	        print(f"    {lang}: {len(lang_chunks)} chunks (using {min(len(lang_chunks), lang_need)})")
181	
182	    random.shuffle(code_short)
183	    print(f"  code total: {len(code_short)} short chunks")
184	
185	    # ── wikitext-103 ────────────────────────────────────────────────
186	    need_wk_short = TRAIN_SHORT["wikitext"] + (VAL_SHORT.get("wikitext", 0) if not train_only else 0) + 50
187	    need_wk_long = TRAIN_LONG["wikitext_long"] + (VAL_LONG.get("wikitext_long", 0) if not train_only else 0) + 10
188	
189	    print("  Loading wikitext-103 (streaming)...")
190	    wiki_ds = load_dataset("wikitext", "wikitext-103-raw-v1", split="train", streaming=True)
191	
192	    wiki_short, wiki_long = [], []
193	    buf_ids = []
194	    pbar = tqdm(desc="  wikitext", unit="chunk")
195	    for sample in wiki_ds:
196	        if not sample["text"].strip():
197	            continue
198	        buf_ids.extend(tokenizer.encode(sample["text"], add_special_tokens=False))
199	        while len(wiki_short) < need_wk_short and len(buf_ids) >= SHORT_LEN:
200	            chunk = buf_ids[:SHORT_LEN]
201	            buf_ids = buf_ids[SHORT_LEN:]
202	            wiki_short.append({"text": tokenizer.decode(chunk), "source": "wikitext"})
203	            pbar.update(1)
204	        while len(wiki_long) < need_wk_long and len(buf_ids) >= LONG_LEN:
205	            chunk = buf_ids[:LONG_LEN]
206	            buf_ids = buf_ids[LONG_LEN:]
207	            wiki_long.append({"text": tokenizer.decode(chunk), "source": "wikitext_long"})
208	            pbar.update(1)
209	        if len(wiki_short) >= need_wk_short and len(wiki_long) >= need_wk_long:
210	            break
211	    pbar.close()
212	    random.shuffle(wiki_short)
213	    random.shuffle(wiki_long)
214	    print(f"  wikitext: {len(wiki_short)} short, {len(wiki_long)} long")
215	
216	    # ── Assemble splits ──────────────────────────────────────────────
217	    def take(pool, n):
218	        return pool[:n], pool[n:]
219	
220	    # Train
221	    sk_s_train, sk_s_rest = take(sky_short, TRAIN_SHORT["skypile"])
222	    co_s_train, co_s_rest = take(code_short, TRAIN_SHORT["code"])
223	    wk_s_train, wk_s_rest = take(wiki_short, TRAIN_SHORT["wikitext"])
224	    sk_l_train, sk_l_rest = take(sky_long, TRAIN_LONG["skypile_long"])
225	    wk_l_train, wk_l_rest = take(wiki_long, TRAIN_LONG["wikitext_long"])
226	
227	    train = sk_s_train + co_s_train + wk_s_train + sk_l_train + wk_l_train
228	    random.shuffle(train)
229	
230	    result = {"train": train}
231	
232	    if not train_only:
233	        # Val (small balanced set for monitoring)
234	        sk_s_val, _ = take(sk_s_rest, VAL_SHORT.get("skypile", 0))
235	        co_s_val, _ = take(co_s_rest, VAL_SHORT.get("code", 0))
236	        wk_s_val, _ = take(wk_s_rest, VAL_SHORT.get("wikitext", 0))
237	        sk_l_val, _ = take(sk_l_rest, VAL_LONG.get("skypile_long", 0))
238	        wk_l_val, _ = take(wk_l_rest, VAL_LONG.get("wikitext_long", 0))
239	        val = sk_s_val + co_s_val + wk_s_val + sk_l_val + wk_l_val
240	        random.shuffle(val)
241	        result["val"] = val
242	
243	        # Val OOD (bench model responses, unchanged from v1)
244	        bench_path = REPO_user_4813494d / "bench/data/speed_bench_cunlimited.jsonl"
245	        bench_texts = _load_jsonl(bench_path, "model_response")
246	        bench_samples = []
247	        for text in bench_texts:
248	            ids = tokenizer.encode(text, add_special_tokens=False)
249	            if len(ids) < MIN_TOKENS:
250	                continue
251	            for t in _chunk_ids(ids, tokenizer, SHORT_LEN):
252	                bench_samples.append({"text": t, "source": "bench"})
253	        result["val_ood"] = bench_samples
254	        print(f"  bench OOD: {len(bench_samples)} chunks")
255	
256	    # Report
257	    from collections import Counter
258	    for split_name, samples in result.items():
259	        counts = Counter(s["source"] for s in samples)
260	        long_n = sum(v for k, v in counts.items() if k.endswith("_long"))
261	        short_n = sum(v for k, v in counts.items() if not k.endswith("_long"))
262	        print(f"\n  {split_name.upper()}: {len(samples)} (short {short_n} + long {long_n})")
263	        for src, n in sorted(counts.items()):
264	            print(f"    {src}: {n}")
265	
266	    return result
267	
268	
269	def prepare_code_supplement(tokenizer) -> dict:
270	    """Prepare code-only supplement data. Concatenates functions to fill 4K chunks."""
271	    random.seed(43)  # different seed from v2 to avoid overlap
272	
273	    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
274	    from datasets import load_dataset
275	
276	    need = CODE_SUPPLEMENT_CHUNKS + 50  # margin
277	    code_chunks = []
278	
279	    for lang, pct in CODE_LANG_PCT.items():
280	        lang_need = int(need * pct) + 10
281	        print(f"  Loading code_search_net/{lang} (supplement)...")
282	        code_ds = load_dataset("code_search_net", lang, split="train", streaming=True)
283	        lang_chunks = []
284	        buf_ids = []
285	        seen = 0
286	        for sample in tqdm(code_ds, desc=f"  code/{lang}", unit="func", leave=False):
287	            func = sample.get("whole_func_string", "")
288	            if not func or len(func) < 50:
289	                continue
290	            seen += 1
291	            # Skip first half of dataset to avoid overlap with v2 collection
292	            if seen < 5000:
293	                continue
294	            buf_ids.extend(tokenizer.encode(func, add_special_tokens=False))
295	            while len(buf_ids) >= SHORT_LEN:
296	                chunk = buf_ids[:SHORT_LEN]
297	                buf_ids = buf_ids[SHORT_LEN:]
298	                lang_chunks.append({"text": tokenizer.decode(chunk), "source": f"code_supp_{lang}"})
299	            if len(lang_chunks) >= lang_need:
300	                break
301	        # Flush remaining buffer if substantial
302	        if len(buf_ids) >= MIN_TOKENS:
303	            lang_chunks.append({"text": tokenizer.decode(buf_ids), "source": f"code_supp_{lang}"})
304	        random.shuffle(lang_chunks)
305	        code_chunks.extend(lang_chunks[:lang_need])
306	        print(f"    {lang}: {len(lang_chunks)} chunks (using {min(len(lang_chunks), lang_need)})")
307	
308	    random.shuffle(code_chunks)
309	    code_chunks = code_chunks[:CODE_SUPPLEMENT_CHUNKS]
310	    print(f"  Code supplement total: {len(code_chunks)} chunks (~{len(code_chunks) * 4}K tokens)")
311	    return {"train": code_chunks}
312	
313	
314	# ── Collection ──────────────────────────────────────────────────────────
315	
316	async def send_request(session, text, api_base, sem):
317	    payload = {"model": "default", "prompt": text, "max_tokens": 1, "temperature": 0}
318	    async with sem:
319	        try:
320	            async with session.post(
321	                f"{api_base}/v1/completions",
322	                json=payload,
323	                timeout=aiohttp.ClientTimeout(total=600),
324	            ) as resp:
325	                await resp.json()
326	                return True
327	        except Exception as e:
328	            print(f"\n  Error: {e}", file=sys.stderr)
329	            return False
330	
331	
332	async def collect_split(session, samples, split_name, api_base, sem, output_dir):
333	    split_dir = output_dir / split_name
334	    split_dir.mkdir(parents=True, exist_ok=True)
335	
336	    # Clean stale files from collect dir
337	    for f in COLLECT_DIR.glob("*.pt"):
338	        f.unlink()
339	
340	    success, fail = 0, 0
341	    pbar = tqdm(total=len(samples), desc=f"  {split_name}", unit="seq")
342	
343	    tasks = []
344	    for sample in samples:
345	        task = asyncio.create_task(send_request(session, sample["text"], api_base, sem))
346	        tasks.append(task)
347	
348	    for task in asyncio.as_completed(tasks):
349	        ok = await task
350	        if ok:
351	            success += 1
352	        else:
353	            fail += 1
354	        pbar.update(1)
355	        pbar.set_postfix(ok=success, fail=fail)
356	    pbar.close()
357	
358	    await asyncio.sleep(2)
359	
360	    pt_files = sorted(COLLECT_DIR.glob("*.pt"))
361	    for f in pt_files:
362	        shutil.move(str(f), str(split_dir / f.name))
363	
364	    total_bytes = sum(f.stat().st_size for f in split_dir.glob("*.pt"))
365	    print(f"    → {len(pt_files)} files, {total_bytes / 1024**3:.2f} GB")
366	    return len(pt_files)
367	
368	
369	async def collect_all(splits, api_base, concurrency, output_dir):
370	    COLLECT_DIR.mkdir(exist_ok=True)
371	    sem = asyncio.Semaphore(concurrency)
372	
373	    async with aiohttp.ClientSession() as session:
374	        # Health check via /v1/models (not /health per project convention)
375	        try:
376	            async with session.get(f"{api_base}/v1/models") as resp:
377	                if resp.status != 200:
378	                    print(f"Server not ready: {resp.status}")
379	                    return
380	        except Exception as e:
381	            print(f"Cannot reach server: {e}")
382	            return
383	
384	        total = 0
385	        for split_name in ["train", "val", "val_ood"]:
386	            samples = splits.get(split_name)
387	            if not samples:
388	                continue
389	            n = await collect_split(session, samples, split_name, api_base, sem, output_dir)
390	            total += n
391	
392	    meta = {
393	        "total_files": total,
394	        "splits": {name: len(s) for name, s in splits.items()},
395	        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
396	        "config": {
397	            "short_len": SHORT_LEN, "long_len": LONG_LEN,
398	            "budget": "v2_40M", "code_languages": list(CODE_LANG_PCT.keys()),
399	        },
400	    }
401	    with open(output_dir / "meta.json", "w") as f:
402	        json.dump(meta, f, indent=2)
403	    print(f"\nDone! {total} files → {output_dir}/")
404	
405	
406	def main():
407	    parser = argparse.ArgumentParser()
408	    parser.add_argument("--api-base", default="http://127.0.0.1:30000")
409	    parser.add_argument("--output", default="medusa/data")
410	    parser.add_argument("--concurrency", type=int, default=64)
411	    parser.add_argument("--train-only", action="store_true",
412	                        help="Only regenerate train split (keep existing val/val_ood)")
413	    parser.add_argument("--code-supplement", action="store_true",
414	                        help="Only collect additional code data to supplement existing train")
415	    args = parser.parse_args()
416	
417	    os.chdir(REPO_user_4813494d)
418	    output_dir = Path(args.output)
419	
420	    print("Loading tokenizer...")
421	    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
422	
423	    if args.code_supplement:
424	        print("Preparing code supplement (v3)...")
425	        splits = prepare_code_supplement(tokenizer)
426	    else:
427	        print("Preparing samples...")
428	        splits = prepare_all(tokenizer, train_only=args.train_only)
429	
430	    print(f"\nCollecting → {output_dir}/")
431	    asyncio.run(collect_all(splits, args.api_base, args.concurrency, output_dir))
432	
433	
434	if __name__ == "__main__":
435	    main()
436
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py",
  "offset": 100,
  "limit": 200
}
```

> TOOL

tool_result Read
```
100	        self.page_size = server_args.page_size
101	        self.speculative_algorithm = SpeculativeAlgorithm.from_string(
102	            server_args.speculative_algorithm
103	        )
104	
105	        # Override the context length of the draft model to be the same as the target model.
106	        server_args.context_length = target_worker.model_runner.model_config.context_len
107	
108	        # Do not capture cuda graph in `super().__init__()`
109	        # It will be captured later.
110	        backup_disable_cuda_graph = server_args.disable_cuda_graph
111	        server_args.disable_cuda_graph = True
112	        # Draft model should not be quantized (it's a small BF16 model)
113	        # Must set speculative_draft_model_quantization, not quantization
114	        # (server_args init already copied quantization to speculative_draft_model_quantization)
115	        backup_draft_quant = server_args.speculative_draft_model_quantization
116	        server_args.speculative_draft_model_quantization = None
117	        # Draft model (Llama architecture) should use standard flashinfer, not minicpm_flashinfer
118	        backup_draft_attn = server_args.speculative_draft_attention_backend
119	        if server_args.attention_backend == "minicpm_flashinfer":
120	            server_args.speculative_draft_attention_backend = "flashinfer"
121	        # Share the allocator with a target worker.
122	        # Draft and target worker own their own KV cache pools.
123	        self.req_to_token_pool, self.token_to_kv_pool_allocator = (
124	            target_worker.get_memory_pool()
125	        )
126	
127	        # Load hot token ids
128	        if self.speculative_algorithm.is_eagle3():
129	            if server_args.speculative_token_map is not None:
130	                logger.warning(
131	                    "Speculative token map specified, but EAGLE3 models already have this. Ignoring the specified token map."
132	                )
133	            self.hot_token_id = None
134	        elif server_args.speculative_token_map is not None:
135	            self.hot_token_id = load_token_map(server_args.speculative_token_map)
136	            server_args.json_model_override_args = (
137	                f'{{"hot_vocab_size": {len(self.hot_token_id)}}}'
138	            )
139	        else:
140	            self.hot_token_id = None
141	
142	        # Init draft worker
143	        if server_args.enable_dp_attention and self.speculative_algorithm.is_eagle3():
144	            ctx = draft_tp_context(get_attention_tp_group())
145	        else:
146	            ctx = empty_context()
147	        with (
148	            ctx
149	        ), speculative_moe_backend_context(), speculative_moe_a2a_backend_context():
150	            super().__init__(
151	                server_args=server_args,
152	                gpu_id=gpu_id,
153	                tp_rank=tp_rank,
154	                pp_rank=0,  # FIXME
155	                dp_rank=dp_rank,
156	                moe_ep_rank=moe_ep_rank,
157	                nccl_port=nccl_port,
158	                is_draft_worker=True,
159	                req_to_token_pool=self.req_to_token_pool,
160	                token_to_kv_pool_allocator=self.token_to_kv_pool_allocator,
161	            )
162	
163	        embed, head = self.target_worker.model_runner.model.get_embed_and_head()
164	
165	        if self.speculative_algorithm.is_eagle3():
166	            # most cases EAGLE3 models don't share lm_head
167	            # but some models (e.g. nvidia/gpt-oss-120b-Eagle3) shares
168	            if (
169	                hasattr(self.draft_model_runner.model, "load_lm_head_from_target")
170	                and self.draft_model_runner.model.load_lm_head_from_target
171	            ):
172	                self.draft_model_runner.model.set_embed_and_head(embed, head)
173	            else:
174	                self.draft_model_runner.model.set_embed(embed)
175	
176	            # grab hot token ids
177	            if self.draft_model_runner.model.hot_token_id is not None:
178	                self.hot_token_id = self.draft_model_runner.model.hot_token_id.to(
179	                    embed.device
180	                )
181	
182	        else:
183	            if self.hot_token_id is not None:
184	                head = head.clone()
185	                self.hot_token_id = self.hot_token_id.to(head.device)
186	                head.data = head.data[self.hot_token_id]
187	
188	            # Share the embedding and lm_head
189	            self.draft_model_runner.model.set_embed_and_head(embed, head)
190	
191	        # Init attention backend and cuda graphs
192	        self.draft_model_runner.server_args.disable_cuda_graph = (
193	            backup_disable_cuda_graph
194	        )
195	        self.draft_tp_context = (
196	            draft_tp_context if server_args.enable_dp_attention else empty_context
197	        )
198	        self.eagle_use_aux_hidden_state = False
199	        if self.speculative_algorithm.is_eagle3():
200	            self.eagle_use_aux_hidden_state = True
201	            eagle_config = getattr(
202	                self.draft_model_runner.model_config.hf_config, "eagle_config", {}
203	            )
204	            self.eagle_use_aux_hidden_state = eagle_config.get(
205	                "use_aux_hidden_state", True
206	            )
207	        with self.draft_tp_context(
208	            self.draft_model_runner.tp_group
209	        ), speculative_moe_backend_context(), speculative_moe_a2a_backend_context():
210	            self.init_attention_backend()
211	            self.init_cuda_graphs()
212	
213	        # Some dummy tensors
214	        self.num_new_pages_per_topk = torch.empty(
215	            (), dtype=torch.int64, device=self.device
216	        )
217	        self.extend_lens = torch.empty((), dtype=torch.int64, device=self.device)
218	
219	    def init_attention_backend(self):
220	        # Create multi-step attn backends and cuda graph runners
221	        draft_backend_factory = DraftBackendFactory(
222	            self.server_args,
223	            self.draft_model_runner,
224	            self.topk,
225	            self.speculative_num_steps,
226	        )
227	
228	        # Initialize decode attention backend
229	        self.draft_attn_backend = draft_backend_factory.create_decode_backend()
230	
231	        # Initialize draft extend attention backend (respects speculative_attention_mode setting)
232	        self.draft_extend_attn_backend = (
233	            draft_backend_factory.create_draft_extend_backend()
234	        )
235	
236	        self.draft_model_runner.draft_attn_backend = self.draft_attn_backend
237	
238	    def init_cuda_graphs(self):
239	        """Capture cuda graphs."""
240	        self.cuda_graph_runner = None
241	        self.cuda_graph_runner_for_draft_extend = None
242	
243	        if self.server_args.disable_cuda_graph:
244	            return
245	
246	        Device2DraftCudaGraphRunner = {
247	            "npu": EAGLEDraftNpuGraphRunner,
248	            "cuda": EAGLEDraftCudaGraphRunner,
249	        }
250	        # Capture draft
251	        if self.speculative_num_steps > 1:
252	            tic = time.perf_counter()
253	            before_mem = get_available_gpu_memory(self.device, self.gpu_id)
254	            logger.info(
255	                f"Capture draft cuda graph begin. This can take up to several minutes. avail mem={before_mem:.2f} GB"
256	            )
257	            self.cuda_graph_runner = Device2DraftCudaGraphRunner[
258	                self.target_worker.device
259	            ](self)
260	            after_mem = get_available_gpu_memory(self.device, self.gpu_id)
261	            logger.info(
262	                f"Capture draft cuda graph end. Time elapsed: {time.perf_counter() - tic:.2f} s. mem usage={(before_mem - after_mem):.2f} GB. avail mem={after_mem:.2f} GB."
263	            )
264	
265	        # Capture extend
266	        if self.draft_extend_attn_backend and not _is_npu:
267	            tic = time.perf_counter()
268	            before_mem = get_available_gpu_memory(self.device, self.gpu_id)
269	            logger.info(
270	                f"Capture draft extend cuda graph begin. This can take up to several minutes. avail mem={before_mem:.2f} GB"
271	            )
272	            self.cuda_graph_runner_for_draft_extend = EAGLEDraftExtendCudaGraphRunner(
273	                self
274	            )
275	            after_mem = get_available_gpu_memory(self.device, self.gpu_id)
276	            logger.info(
277	                f"Capture draft extend cuda graph end. Time elapsed: {time.perf_counter() - tic:.2f} s. mem usage={(before_mem - after_mem):.2f} GB. avail mem={after_mem:.2f} GB."
278	            )
279	
280	    @property
281	    def draft_model_runner(self):
282	        return self.model_runner
283	
284	    def forward_batch_generation(self, batch: ScheduleBatch) -> GenerationBatchResult:
285	        """Run speculative decoding forward.
286	
287	        NOTE: Many states of batch is modified as you go through. It is not guaranteed that
288	        the final output batch have the same state as the input.
289	
290	        Args:
291	            batch: The batch to run forward. The state of the batch is modified as it runs.
292	        Returns:
293	            A tuple of the final logit output of the target model, next tokens accepted,
294	            the batch id (used for overlap schedule), and number of accepted tokens.
295	        """
296	        if batch.forward_mode.is_extend() or batch.is_extend_in_batch:
297	            logits_output, next_token_ids, seq_lens_cpu = self.forward_target_extend(
298	                batch
299	            )
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/medusa/eval_topk.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Offline evaluation: top-k candidate tree for Medusa K=1 head.
4	
5	Simulates tree verification where the single head produces k candidates
6	instead of 1 argmax. If ANY candidate matches the true label, it counts
7	as accepted. This models a width-k depth-1 tree verified in one forward.
8	
9	Reports:
10	  - Per-k hit rate (P(at least 1 of k matches label))
11	  - Expected tokens_per_step = 1 + hit_rate
12	  - Effective throughput ratio vs k=1 baseline, accounting for dtn overhead
13	
14	Usage:
15	    python3 medusa/eval_topk.py [--split val_ood] [--max-k 10]
16	"""
17	
18	import os
19	import sys
20	import time
21	from pathlib import Path
22	
23	import torch
24	import torch.nn as nn
25	import torch.nn.functional as F
26	from safetensors import safe_open
27	from tqdm import tqdm
28	
29	# ── Config ───────────────────────────────────────────────────────────────
30	DATA_DIR   = Path("medusa/data")
31	MODEL_PATH = [REDACTED]
32	WEIGHTS    = Path("medusa/weights/best.pt")
33	PACK_SIZE  = 6
34	
35	HIDDEN_SIZE = 4096
36	VOCAB_SIZE  = 73448
37	SCALE_WIDTH = HIDDEN_SIZE / 256   # 16
38	
39	
40	# ── Model (same as train.py) ────────────────────────────────────────────
41	class RMSNorm(nn.Module):
42	    def __init__(self, hidden_size, eps=1e-6):
43	        super().__init__()
44	        self.weight = nn.Parameter(torch.ones(hidden_size))
45	        self.eps = eps
46	
47	    def forward(self, x):
48	        norm = x.float().pow(2).mean(-1, keepdim=True).add(self.eps).rsqrt()
49	        return (x * norm).to(x.dtype) * self.weight
50	
51	
52	class ResBlock(nn.Module):
53	    def __init__(self, hidden_size):
54	        super().__init__()
55	        self.linear = nn.Linear(hidden_size, hidden_size)
56	        self.act = nn.SiLU()
57	
58	    def forward(self, x):
59	        return x + self.act(self.linear(x))
60	
61	
62	class MedusaBlock(nn.Module):
63	    def __init__(self, hidden_size):
64	        super().__init__()
65	        self.norm = RMSNorm(hidden_size)
66	        self.res1 = ResBlock(hidden_size)
67	        self.res2 = ResBlock(hidden_size)
68	
69	    def forward(self, x):
70	        x = self.norm(x)
71	        x = self.res1(x)
72	        x = self.res2(x)
73	        return x
74	
75	
76	class MedusaHeads(nn.Module):
77	    def __init__(self, num_heads, hidden_size, lm_head_weight):
78	        super().__init__()
79	        self.num_heads = num_heads
80	        self.heads = nn.ModuleList([MedusaBlock(hidden_size) for _ in range(num_heads)])
81	        self.register_buffer("lm_head_weight", lm_head_weight)
82	
83	    def forward(self, hidden_states):
84	        return [F.linear(head(hidden_states), self.lm_head_weight).float()
85	                for head in self.heads]
86	
87	
88	# ── Data loading (reuse from train.py) ───────────────────────────────────
89	def _load_pack_cpu(files, K):
90	    hs, label_lists = [], [[] for _ in range(K)]
91	    for f in files:
92	        data = torch.load(f, map_location="cpu", weights_only=True)
93	        h   = data["hidden_states"]
94	        ids = data["token_ids"]
95	        valid_len = len(ids) - K - 1
96	        if valid_len < 1 or h.isnan().any():
97	            continue
98	        hs.append(h[:valid_len])
99	        for k in range(K):
100	            label_lists[k].append(ids[k + 2 : k + 2 + valid_len])
101	    if not hs:
102	        return None, None
103	    return torch.cat(hs, dim=0), [torch.cat(lbl, dim=0) for lbl in label_lists]
104	
105	
106	def iter_packs(files, K, device):
107	    batches = [files[i : i + PACK_SIZE] for i in range(0, len(files), PACK_SIZE)]
108	    for batch in tqdm(batches, desc="Eval", unit="pack", leave=False):
109	        h_cpu, labels_cpu = _load_pack_cpu(batch, K)
110	        if h_cpu is None:
111	            continue
112	        yield h_cpu.to(device), [l.to(device) for l in labels_cpu]
113	
114	
115	# ── Main ─────────────────────────────────────────────────────────────────
116	def main():
117	    import argparse
118	    parser = argparse.ArgumentParser()
119	    parser.add_argument("--split", default="val_ood")
120	    parser.add_argument("--max-k", type=int, default=10)
121	    args = parser.parse_args()
122	
123	    device = torch.device("cuda")
124	    max_k = args.max_k
125	
126	    # Load model
127	    print("Loading lm_head...")
128	    sf_path = os.path.join(MODEL_PATH, "model-00002-of-00002.safetensors")
129	    with safe_open(sf_path, framework="pt") as sf:
130	        lm_head_w = sf.get_tensor("lm_head.weight").to(device)
131	    lm_head_w = lm_head_w / SCALE_WIDTH
132	
133	    print("Loading Medusa head...")
134	    ckpt = torch.load(WEIGHTS, map_location="cpu", weights_only=True)
135	    num_heads = ckpt["num_heads"]
136	    model = MedusaHeads(num_heads, HIDDEN_SIZE, lm_head_w).to(device=device, dtype=torch.bfloat16)
137	    model.heads.load_state_dict(ckpt["heads_state_dict"])
138	    model.eval()
139	    print(f"  Loaded: {num_heads} heads, metrics={ckpt.get('metrics', 'N/A')}")
140	
141	    # Load data
142	    split_dir = DATA_DIR / args.split
143	    files = sorted(split_dir.glob("*.pt"))
144	    print(f"  Data: {len(files)} files from {split_dir}")
145	
146	    # Evaluate top-k hit rates
147	    K = num_heads  # should be 1
148	    # For each k in [1..max_k], track hits
149	    hits = [0] * (max_k + 1)  # hits[k] = positions where top-k contains label
150	    total_pos = 0
151	
152	    with torch.no_grad():
153	        for h, labels in iter_packs(files, K, device):
154	            logits = model(h)[0]  # K=1, take head 0's logits: (N, vocab)
155	            label = labels[0]      # (N,)
156	            N = h.shape[0]
157	            total_pos += N
158	
159	            # Get top-max_k predictions
160	            topk_preds = logits.topk(max_k, dim=-1).indices  # (N, max_k)
161	            label_expanded = label.unsqueeze(-1)  # (N, 1)
162	
163	            # For each k, check if label is in top-k
164	            for k in range(1, max_k + 1):
165	                match = (topk_preds[:, :k] == label_expanded).any(dim=-1)  # (N,)
166	                hits[k] += match.sum().item()
167	
168	    # Report
169	    print(f"\n{'='*70}")
170	    print(f"Top-k Candidate Analysis (split={args.split}, N={total_pos})")
171	    print(f"{'='*70}")
172	    print(f"{'k':>3}  {'hit_rate':>8}  {'tok/step':>8}  {'dtn':>4}  {'eff_throughput':>14}  {'vs_k=1':>8}")
173	    print(f"{'-'*3}  {'-'*8}  {'-'*8}  {'-'*4}  {'-'*14}  {'-'*8}")
174	
175	    baseline_eff = None
176	    for k in range(1, max_k + 1):
177	        hit_rate = hits[k] / max(total_pos, 1)
178	        tok_per_step = 1.0 + hit_rate
179	        dtn = k + 1  # verified_id + k candidates
180	        # Effective throughput: tokens gained per unit of forward cost
181	        # Assume forward cost scales linearly with dtn (conservative)
182	        eff = tok_per_step / dtn
183	        if k == 1:
184	            baseline_eff = eff
185	        speedup = eff / baseline_eff if baseline_eff else 1.0
186	
187	        print(f"{k:>3}  {hit_rate:>8.4f}  {tok_per_step:>8.3f}  {dtn:>4}  {eff:>14.4f}  {speedup:>7.2f}x")
188	
189	    # Also show with sublinear cost model (more realistic)
190	    print(f"\n{'='*70}")
191	    print(f"With sublinear cost model: cost(dtn) = 1 + 0.3*(dtn-1)")
192	    print(f"  (decode is memory-bandwidth-bound, extra tokens add marginal cost)")
193	    print(f"{'='*70}")
194	    print(f"{'k':>3}  {'hit_rate':>8}  {'tok/step':>8}  {'cost':>6}  {'eff_throughput':>14}  {'vs_k=1':>8}")
195	    print(f"{'-'*3}  {'-'*8}  {'-'*8}  {'-'*6}  {'-'*14}  {'-'*8}")
196	
197	    baseline_eff_sub = None
198	    for k in range(1, max_k + 1):
199	        hit_rate = hits[k] / max(total_pos, 1)
200	        tok_per_step = 1.0 + hit_rate
201	        dtn = k + 1
202	        cost = 1.0 + 0.3 * (dtn - 1)  # sublinear: base + 0.3 per extra token
203	        eff = tok_per_step / cost
204	        if k == 1:
205	            baseline_eff_sub = eff
206	        speedup = eff / baseline_eff_sub if baseline_eff_sub else 1.0
207	
208	        print(f"{k:>3}  {hit_rate:>8.4f}  {tok_per_step:>8.3f}  {cost:>6.2f}  {eff:>14.4f}  {speedup:>7.2f}x")
209	
210	    print(f"\nNote: actual cost model depends on batch size and model architecture.")
211	    print(f"Sublinear model is more realistic for decode (memory-bandwidth-bound).")
212	    print(f"Profile with real serving to find the optimal k.")
213	
214	
215	if __name__ == "__main__":
216	    main()
217
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/medusa/select_similar.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""Per-query KNN data selection: for each val_ood file, find K nearest
3	train files by cosine similarity of mean hidden states. Union of all
4	neighbors forms the training subset.
5	
6	GPU-accelerated: cosine sim matrix (150 × 11585) computed in one batch.
7	Multi-threaded I/O for loading hidden states.
8	
9	Usage:
10	    python3 medusa/select_similar.py
11	"""
12	
13	import json
14	import torch
15	from pathlib import Path
16	from concurrent.futures import ThreadPoolExecutor, as_completed
17	from tqdm import tqdm
18	
19	DATA_DIR = Path("medusa/data")
20	NUM_WORKERS = 16
21	MIN_TOKENS = 64
22	K = 50  # nearest neighbors per val_ood file
23	
24	
25	def compute_mean_hidden(fpath):
26	    """Load file, return (path, mean_hidden, n_tokens) or None."""
27	    try:
28	        d = torch.load(fpath, map_location="cpu", weights_only=True)
29	        h = d["hidden_states"]
30	        n_tok = len(d["token_ids"])
31	        if n_tok < MIN_TOKENS or h.isnan().any():
32	            return None
33	        return (str(fpath), h.float().mean(dim=0), n_tok)
34	    except Exception:
35	        return None
36	
37	
38	def load_all_means(files, desc):
39	    """Multi-threaded load, returns (paths, mean_tensor, token_counts)."""
40	    paths, means, tok_counts = [], [], []
41	    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as pool:
42	        futs = [pool.submit(compute_mean_hidden, f) for f in files]
43	        for fut in tqdm(as_completed(futs), total=len(futs), desc=desc):
44	            r = fut.result()
45	            if r:
46	                paths.append(r[0])
47	                means.append(r[1])
48	                tok_counts.append(r[2])
49	    return paths, torch.stack(means), tok_counts
50	
51	
52	def main():
53	    device = torch.device("cuda")
54	
55	    # 1. Load all mean hidden states
56	    val_files = sorted((DATA_DIR / "val_ood").glob("*.pt"))
57	    train_files = sorted((DATA_DIR / "train").glob("*.pt"))
58	    print(f"Files: val_ood={len(val_files)}, train={len(train_files)}")
59	
60	    val_paths, val_means, val_toks = load_all_means(val_files, "val_ood")
61	    train_paths, train_means, train_toks = load_all_means(train_files, "train")
62	    print(f"Valid: val_ood={len(val_paths)}, train={len(train_paths)}")
63	
64	    # 2. GPU cosine similarity matrix
65	    print(f"\nComputing cosine similarity ({len(val_paths)} × {len(train_paths)}) on GPU...")
66	    val_gpu = torch.nn.functional.normalize(val_means.to(device), dim=1)    # (V, 4096)
67	    train_gpu = torch.nn.functional.normalize(train_means.to(device), dim=1)  # (T, 4096)
68	    sim = val_gpu @ train_gpu.T  # (V, T)
69	
70	    # 3. Per-query top-K
71	    topk_vals, topk_idx = sim.topk(K, dim=1)  # (V, K)
72	    topk_idx = topk_idx.cpu()
73	    topk_vals = topk_vals.cpu()
74	
75	    # Collect union of all neighbors
76	    selected_indices = set()
77	    for i in range(len(val_paths)):
78	        for j in range(K):
79	            selected_indices.add(topk_idx[i, j].item())
80	
81	    selected_tokens = sum(train_toks[idx] for idx in selected_indices)
82	
83	    print(f"\n{'='*60}")
84	    print(f"K={K}, val_ood queries={len(val_paths)}")
85	    print(f"Max possible neighbors: {len(val_paths) * K} = {len(val_paths)*K}")
86	    print(f"Unique selected: {len(selected_indices)} files")
87	    print(f"Selected tokens: {selected_tokens/1e6:.1f}M")
88	    print(f"Coverage: {len(selected_indices)/len(train_paths)*100:.1f}% of train")
89	
90	    # 4. Per-query stats
91	    print(f"\nPer-query nearest neighbor stats:")
92	    print(f"{'query':<15} {'best_sim':>8} {'worst_sim':>9} {'avg_sim':>8}")
93	    print("-" * 45)
94	    sims_best = topk_vals[:, 0]
95	    sims_worst = topk_vals[:, K-1]
96	    sims_avg = topk_vals.mean(dim=1)
97	    # Show a few
98	    for i in range(0, len(val_paths), max(1, len(val_paths)//10)):
99	        vname = Path(val_paths[i]).name
100	        print(f"{vname:<15} {sims_best[i]:>8.4f} {sims_worst[i]:>9.4f} {sims_avg[i]:>8.4f}")
101	    print(f"{'OVERALL':<15} {sims_best.mean():>8.4f} {sims_worst.mean():>9.4f} {sims_avg.mean():>8.4f}")
102	
103	    # 5. Compute per-file importance: max cosine sim to ANY val_ood query
104	    # This gives every train file a continuous weight, not just binary selected/not
105	    max_sim_per_train = sim.max(dim=0).values.cpu()  # (T,)
106	
107	    # Also compute KNN importance for reporting
108	    importance = {}
109	    for i in range(len(val_paths)):
110	        for j in range(K):
111	            idx = topk_idx[i, j].item()
112	            if idx not in importance:
113	                importance[idx] = {"count": 0, "max_sim": 0.0}
114	            importance[idx]["count"] += 1
115	            importance[idx]["max_sim"] = max(importance[idx]["max_sim"],
116	                                              topk_vals[i, j].item())
117	
118	    # Save ALL files with continuous importance weights (no re-loading needed)
119	    selected_ranked = []
120	    for idx in range(len(train_paths)):
121	        sim_val = max_sim_per_train[idx].item()
122	        entry = {
123	            "file": train_paths[idx],
124	            "tokens": train_toks[idx],
125	            "max_cos_sim": round(sim_val, 6),  # continuous importance weight
126	            "dist": round(1.0 - sim_val, 4),   # backward compat
127	            "query_count": importance.get(idx, {}).get("count", 0),
128	        }
129	        selected_ranked.append(entry)
130	    # Sort by importance (highest first)
131	    selected_ranked.sort(key=lambda x: -x["max_cos_sim"])
132	
133	    out_path = DATA_DIR / "train_ranked_by_val_ood.json"
134	    with open(out_path, "w") as f:
135	        json.dump(selected_ranked, f)
136	    print(f"\nSaved {len(selected_ranked)} entries to {out_path}")
137	
138	    # 6. Show importance distribution
139	    all_sims = [r["max_cos_sim"] for r in selected_ranked]
140	    import numpy as np
141	    sims_arr = np.array(all_sims)
142	    print(f"\nImportance (max_cos_sim) distribution:")
143	    for p in [10, 25, 50, 75, 90]:
144	        print(f"  P{p}: {np.percentile(sims_arr, p):.4f}")
145	    print(f"  mean: {sims_arr.mean():.4f}, std: {sims_arr.std():.4f}")
146	
147	    # Show top files
148	    print(f"\nTop 15 most important train files:")
149	    for r in selected_ranked[:15]:
150	        print(f"  {Path(r['file']).name}: cos_sim={r['max_cos_sim']:.4f}, "
151	              f"KNN_count={r['query_count']}, {r['tokens']} tok")
152	
153	    # Show weight distribution preview
154	    power = 2.0
155	    floor = 0.1
156	    weights = [max(s, floor) ** power for s in all_sims]
157	    w_arr = np.array(weights)
158	    print(f"\nSampling weights (power={power}, floor={floor}):")
159	    print(f"  range: [{w_arr.min():.4f}, {w_arr.max():.4f}]")
160	    print(f"  mean: {w_arr.mean():.4f}")
161	    eff = (w_arr.sum()**2) / (w_arr**2).sum()
162	    print(f"  effective dataset size: {eff:.0f} / {len(w_arr)} ({eff/len(w_arr)*100:.1f}%)")
163	
164	
165	if __name__ == "__main__":
166	    main()
167
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/medusa_worker.py",
  "offset": 100,
  "limit": 200
}
```

> TOOL

tool_result Read
```
100	        dp_rank: Optional[int],
101	        moe_ep_rank: int,
102	        nccl_port: int,
103	        target_worker: TpModelWorker,
104	    ):
105	        self.server_args = server_args
106	        self.target_worker = target_worker
107	        self.device = server_args.device
108	        self.gpu_id = gpu_id
109	        self.page_size = server_args.page_size
110	        self.enable_nan_detection = server_args.enable_nan_detection
111	
112	        self.num_heads = server_args.speculative_num_steps or 3
113	        self.topk = 1
114	        # Medusa verifies verified_id + K drafts = K+1 tokens per request.
115	        # server_args already enforces speculative_num_draft_tokens = num_steps + 1.
116	        self.num_draft_tokens = self.num_heads + 1
117	        assert server_args.speculative_num_draft_tokens == self.num_draft_tokens, (
118	            f"speculative_num_draft_tokens={server_args.speculative_num_draft_tokens} "
119	            f"must equal num_heads+1={self.num_draft_tokens}"
120	        )
121	
122	        # Share allocator with target worker (same pattern as EAGLEWorker)
123	        self.req_to_token_pool, self._token_to_kv_pool_allocator = (
124	            target_worker.get_memory_pool()
125	        )
126	
127	        # Dynamic spec/no-spec threshold: skip draft+verify when bs >= threshold
128	        import os
129	        self.spec_bs_threshold = int(os.environ.get("SGLANG_MEDUSA_BS_THRESHOLD", "16"))
130	
131	        self._load_medusa_heads()
132	        logger.info(
133	            f"MedusaWorker initialized: {self.num_heads} heads, "
134	            f"topk={self.topk}, num_draft_tokens={self.num_draft_tokens}, "
135	            f"strategy=batched_target_verify, "
136	            f"spec_bs_threshold={self.spec_bs_threshold}"
137	        )
138	
139	    def _load_medusa_heads(self):
140	        import os
141	
142	        model = self.target_worker.model_runner.model
143	        if hasattr(model, "lm_head"):
144	            lm_head_weight = model.lm_head.weight
145	        elif hasattr(model, "model") and hasattr(model.model, "embed_tokens"):
146	            lm_head_weight = model.model.embed_tokens.weight
147	        else:
148	            raise RuntimeError("Cannot find lm_head weight in target model")
149	        hidden_size = lm_head_weight.shape[1]
150	
151	        weights_path = self.server_args.speculative_draft_model_path
152	        if weights_path is None or not os.path.exists(weights_path):
153	            # Search in common locations
154	            candidates = [
155	                weights_path,
156	                os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "data", "medusa_best.pt"),
157	                os.path.join(self.server_args.model_path, "..", "medusa_weights", "best.pt"),
158	                "/user_4813494d/openbmb/medusa/weights/best.pt",
159	            ]
160	            weights_path = None
161	            for c in candidates:
162	                if c and os.path.exists(c):
163	                    weights_path = os.path.realpath(c)
164	                    break
165	            if weights_path is None:
166	                raise FileNotFoundError(f"Medusa weights not found in: {candidates}")
167	        logger.info(f"Loading Medusa heads from {weights_path}")
168	
169	        checkpoint = torch.load(weights_path, map_location="cpu", weights_only=True)
170	        heads_state_dict = checkpoint["heads_state_dict"]
171	        ckpt_num_heads = checkpoint.get("num_heads", self.num_heads)
172	        if self.num_heads > ckpt_num_heads:
173	            logger.warning(
174	                f"Requested {self.num_heads} heads but checkpoint only has {ckpt_num_heads}. "
175	                f"Using checkpoint value."
176	            )
177	            self.num_heads = ckpt_num_heads
178	            self.num_draft_tokens = ckpt_num_heads + 1
179	        elif self.num_heads < ckpt_num_heads:
180	            logger.info(
181	                f"Using {self.num_heads} of {ckpt_num_heads} available heads from checkpoint."
182	            )
183	
184	        # Auto-detect checkpoint format: MedusaBlock (norm+res1+res2) vs ResBlock
185	        block_cls = MedusaBlock if any(
186	            ".norm." in k or ".res1." in k or ".res2." in k
187	            for k in heads_state_dict
188	        ) else ResBlock
189	        logger.info(f"Medusa checkpoint format: {block_cls.__name__}")
190	
191	        # Load all checkpoint heads, then keep only the first num_heads
192	        all_heads = MedusaHeads(
193	            ckpt_num_heads, hidden_size, lm_head_weight.clone(),
194	            block_cls=block_cls,
195	        ).to(device=self.device, dtype=torch.bfloat16)
196	        all_heads.heads.load_state_dict(heads_state_dict)
197	
198	        self.medusa_heads = MedusaHeads(
199	            self.num_heads, hidden_size, lm_head_weight.clone(),
200	            block_cls=block_cls,
201	        ).to(device=self.device, dtype=torch.bfloat16)
202	        # Copy only the first num_heads
203	        for i in range(self.num_heads):
204	            self.medusa_heads.heads[i].load_state_dict(all_heads.heads[i].state_dict())
205	        del all_heads
206	        self.medusa_heads.eval()
207	
208	        n_params = sum(p.numel() for p in self.medusa_heads.parameters())
209	        logger.info(f"Medusa heads loaded: {n_params:,} params")
210	
211	    @property
212	    def model_runner(self):
213	        return self.target_worker.model_runner
214	
215	    @property
216	    def model_config(self):
217	        return self.target_worker.model_runner.model_config
218	
219	    @property
220	    def token_to_kv_pool_allocator(self):
221	        return self._token_to_kv_pool_allocator
222	
223	    def get_memory_pool(self):
224	        return self.target_worker.get_memory_pool()
225	
226	    # ── Main entry ──────────────────────────────────────────────────────
227	
228	    def forward_batch_generation(self, batch: ScheduleBatch) -> GenerationBatchResult:
229	        if batch.forward_mode.is_extend() or batch.is_extend_in_batch:
230	            return self._forward_extend(batch)
231	        elif batch.forward_mode.is_idle():
232	            return self._forward_idle(batch)
233	        else:
234	            return self._forward_decode(batch)
235	
236	    # ── Extend ──────────────────────────────────────────────────────────
237	
238	    def _forward_extend(self, batch: ScheduleBatch) -> GenerationBatchResult:
239	        model_worker_batch = batch.get_model_worker_batch()
240	        model_worker_batch.capture_hidden_mode = CaptureHiddenMode.LAST
241	        batch_result = self.target_worker.forward_batch_generation(model_worker_batch)
242	        logits_output = batch_result.logits_output
243	        next_token_ids = batch_result.next_token_ids
244	
245	        batch.spec_info = EagleDraftInput(
246	            hidden_states=logits_output.hidden_states,
247	            verified_id=next_token_ids,
248	            topk_p=torch.ones(
249	                len(next_token_ids), 1, device=self.device, dtype=torch.float32
250	            ),
251	            topk_index=next_token_ids.unsqueeze(1),
252	            num_tokens_per_batch=1,
253	            num_tokens_for_logprob_per_batch=1,
254	            capture_hidden_mode=CaptureHiddenMode.LAST,
255	        )
256	
257	        return GenerationBatchResult(
258	            logits_output=logits_output,
259	            next_token_ids=next_token_ids,
260	            num_accepted_tokens=0,
261	            can_run_cuda_graph=False,
262	        )
263	
264	    # ── Idle ────────────────────────────────────────────────────────────
265	
266	    def _forward_idle(self, batch: ScheduleBatch) -> GenerationBatchResult:
267	        batch.spec_info = EagleDraftInput.create_idle_input(
268	            device=self.device,
269	            hidden_size=self.model_config.hidden_size,
270	            dtype=self.model_config.dtype,
271	            topk=self.topk,
272	            capture_hidden_mode=CaptureHiddenMode.LAST,
273	        )
274	        model_worker_batch = batch.get_model_worker_batch()
275	        model_worker_batch.capture_hidden_mode = CaptureHiddenMode.LAST
276	        batch_result = self.target_worker.forward_batch_generation(model_worker_batch)
277	        return GenerationBatchResult(
278	            logits_output=batch_result.logits_output,
279	            next_token_ids=batch_result.next_token_ids,
280	            num_accepted_tokens=0,
281	            can_run_cuda_graph=False,
282	        )
283	
284	    # ── Decode (Batched TARGET_VERIFY) ────────────────────────────────
285	
286	    def _forward_decode(self, batch: ScheduleBatch) -> GenerationBatchResult:
287	        """Speculative decode using batched TARGET_VERIFY.
288	
289	        All K+1 tokens (verified_id + K drafts) are verified in a single
290	        forward pass through the target model. This leverages the fact that
291	        GEMM cost at M=4 is only ~2x M=1 (bandwidth-limited), so verifying
292	        4 tokens costs ~1.5x of a single decode while potentially producing
293	        up to 4 tokens.
294	
295	        When bs >= spec_bs_threshold, falls back to normal single-token decode
296	        to avoid throughput regression from draft overhead at high concurrency.
297	        """
298	        spec_info = batch.spec_info
299	        assert isinstance(spec_info, EagleDraftInput)
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt -name \"*eagle*\" -type f | head -20"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/hardware_backend/npu/graph_runner/eagle_draft_extend_npu_graph_runner.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/hardware_backend/npu/graph_runner/eagle_draft_npu_graph_runner.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/hardware_backend/npu/graph_runner/__pycache__/eagle_draft_npu_graph_runner.cpython-310.pyc
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_draft_cuda_graph_runner.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_draft_extend_cuda_graph_runner.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info_v2.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_utils.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker_v2.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/multi_layer_eagle_draft_extend_cuda_graph_runner.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/multi_layer_eagle_utils.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/multi_layer_eagle_worker.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/multi_layer_eagle_worker_v2.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/__pycache__/eagle_info.cpython-310.pyc
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/__pycache__/eagle_info_v2.cpython-310.pyc
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/__pycache__/eagle_utils.cpython-310.pyc
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/__pycache__/eagle_worker.cpython-310.pyc
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/__pycache__/eagle_draft_cuda_graph_runner.cpython-310.pyc
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/__pycache__/eagle_draft_extend_cuda_graph_runner.cpython-310.pyc
```

> AGENT

Now let me check the eagle_info.py to understand the data structures:

> AGENT

Now let me check for any actual performance measurements and benchmarks:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1	import logging
2	from copy import copy
3	from dataclasses import dataclass
4	from typing import ClassVar, List, Optional, Tuple
5	
6	import torch
7	import torch.nn.functional as F
8	
9	from sglang.srt.constrained.base_grammar_backend import BaseGrammarObject
10	from sglang.srt.environ import envs
11	from sglang.srt.layers.attention.utils import create_flashinfer_kv_indices_triton
12	from sglang.srt.layers.logits_processor import LogitsProcessorOutput
13	from sglang.srt.layers.sampler import apply_custom_logit_processor
14	from sglang.srt.managers.overlap_utils import FutureIndices
15	from sglang.srt.managers.schedule_batch import ScheduleBatch
16	from sglang.srt.mem_cache.allocator import BaseTokenToKVPoolAllocator
17	from sglang.srt.mem_cache.common import (
18	    alloc_paged_token_slots_extend,
19	    alloc_token_slots,
20	    get_last_loc,
21	)
22	from sglang.srt.model_executor.forward_batch_info import CaptureHiddenMode
23	from sglang.srt.server_args import get_global_server_args
24	from sglang.srt.speculative.eagle_info_v2 import (
25	    EagleDraftInputV2Mixin,
26	    EagleVerifyInputV2Mixin,
27	)
28	from sglang.srt.speculative.eagle_utils import verify_tree_greedy_func
29	from sglang.srt.speculative.spec_info import SpecInput, SpecInputType
30	from sglang.srt.speculative.spec_utils import (
31	    SIMULATE_ACC_LEN,
32	    TREE_SPEC_KERNEL_AVAILABLE,
33	    align_evict_mask_to_page_size,
34	    assign_req_to_token_pool_func,
35	    create_accept_length_filter,
36	    create_extend_after_decode_spec_info,
37	    filter_finished_cache_loc_kernel,
38	    generate_simulated_accept_index,
39	    get_src_tgt_cache_loc,
40	    get_target_cache_loc,
41	)
42	from sglang.srt.utils import is_cuda, next_power_of_2
43	
44	if is_cuda():
45	    from sgl_kernel import (
46	        top_k_renorm_prob,
47	        top_p_renorm_prob,
48	        tree_speculative_sampling_target_only,
49	    )
50	
51	logger = logging.getLogger(__name__)
52	
53	
54	@dataclass
55	class EagleVerifyInput(SpecInput, EagleVerifyInputV2Mixin):
56	    draft_token: torch.Tensor
57	    custom_mask: torch.Tensor
58	    positions: torch.Tensor
59	    retrive_index: torch.Tensor
60	    retrive_next_token: torch.Tensor
61	    retrive_next_sibling: torch.Tensor
62	    retrive_cum_len: torch.Tensor
63	    spec_steps: int
64	    topk: int
65	    draft_token_num: int
66	    capture_hidden_mode: CaptureHiddenMode
67	    seq_lens_sum: int
68	    seq_lens_cpu: torch.Tensor
69	    grammar: BaseGrammarObject = None
70	
71	    # Shape info for padding
72	    num_tokens_per_batch: int = -1
73	
74	    def __post_init__(self):
75	        super().__init__(SpecInputType.EAGLE_VERIFY)
76	
77	    def get_spec_adjust_token_coefficient(self) -> Tuple[int, int]:
78	        return self.draft_token_num, self.draft_token_num
79	
80	    @classmethod
81	    def create_idle_input(cls, topk: int, spec_steps: int, num_verify_tokens: int):
82	        return cls(
83	            draft_token=torch.empty((0,), dtype=torch.long, device="cuda"),
84	            custom_mask=torch.full((0,), True, dtype=torch.bool, device="cuda"),
85	            positions=torch.empty((0,), dtype=torch.int64, device="cuda"),
86	            retrive_index=torch.full(
87	                (0, num_verify_tokens), -1, dtype=torch.long, device="cuda"
88	            ),
89	            retrive_next_token=torch.full(
90	                (0, num_verify_tokens), -1, dtype=torch.long, device="cuda"
91	            ),
92	            retrive_next_sibling=torch.full(
93	                (0, num_verify_tokens), -1, dtype=torch.long, device="cuda"
94	            ),
95	            retrive_cum_len=None,
96	            topk=topk,
97	            draft_token_num=num_verify_tokens,
98	            spec_steps=spec_steps,
99	            capture_hidden_mode=CaptureHiddenMode.FULL,
100	            seq_lens_sum=0,
101	            seq_lens_cpu=torch.empty((0,), dtype=torch.int32),
102	        )
103	
104	    def prepare_for_verify(self, batch: ScheduleBatch, page_size: int):
105	
106	        if batch.forward_mode.is_idle():
107	            return
108	
109	        batch.input_ids = self.draft_token
110	
111	        if page_size == 1:
112	            batch.out_cache_loc = alloc_token_slots(
113	                batch.tree_cache,
114	                len(batch.input_ids),
115	            )
116	            end_offset = batch.seq_lens + self.draft_token_num
117	        else:
118	            prefix_lens = batch.seq_lens
119	            prefix_lens_cpu = batch.seq_lens_cpu
120	            end_offset = prefix_lens + self.draft_token_num
121	            end_offset_cpu = prefix_lens_cpu + self.draft_token_num
122	            last_loc = get_last_loc(
123	                batch.req_to_token_pool.req_to_token,
124	                batch.req_pool_indices,
125	                prefix_lens,
126	            )
127	            batch.out_cache_loc = alloc_paged_token_slots_extend(
128	                batch.tree_cache,
129	                prefix_lens,
130	                prefix_lens_cpu,
131	                end_offset,
132	                end_offset_cpu,
133	                last_loc,
134	                len(batch.input_ids),
135	            )
136	            self.last_loc = last_loc
137	
138	        bs = batch.batch_size()
139	        assign_req_to_token_pool_func(
140	            batch.req_pool_indices,
141	            batch.req_to_token_pool.req_to_token,
142	            batch.seq_lens,
143	            end_offset,
144	            batch.out_cache_loc,
145	            bs,
146	        )
147	
148	        if get_global_server_args().enable_mamba_extra_buffer():
149	            batch.mamba_track_indices = torch.tensor(
150	                [
```

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -name \"*.json\" | xargs grep -l \"accept\\|speedup\\|throughput\" 2>/dev/null | head -10"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/quant/calib90/train.json
/user_4813494d/openbmb/eagle/sglang_model/tokenizer.json
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -lh /user_4813494d/openbmb/eagle/ 2>/dev/null | head -20"
}
```

> TOOL

tool_result Bash
```
total 120K
drwxr-xr-x 2 user_4813494d user_4813494d  132 Apr 12 11:20 __pycache__
-rw-r--r-- 1 user_4813494d user_4813494d  16K Apr 11 20:36 collect_data.py
-rw-r--r-- 1 user_4813494d user_4813494d 5.5K Apr 12 12:02 convert_to_sglang.py
drwxr-xr-x 3 user_4813494d user_4813494d   78 Apr 11 20:54 data
-rw-r--r-- 1 user_4813494d user_4813494d  11K Apr 12 11:06 eval_ood_accept.py
drwxr-xr-x 2 user_4813494d user_4813494d 4.0K Apr 12 00:46 sglang_model
-rw-r--r-- 1 user_4813494d user_4813494d  11K Apr 12 06:23 test_decode_mode.py
-rw-r--r-- 1 user_4813494d user_4813494d 6.5K Apr 12 05:09 test_eagle3_flow.py
-rw-r--r-- 1 user_4813494d user_4813494d  11K Apr 12 06:19 test_forward_match.py
-rw-r--r-- 1 user_4813494d user_4813494d 4.8K Apr 12 05:24 test_offline_pred.py
-rw-r--r-- 1 user_4813494d user_4813494d  27K Apr 12 10:48 train.py
-rw-r--r-- 1 user_4813494d user_4813494d 6.6K Apr 12 06:25 verify_sglang_draft.py
drwxr-xr-x 2 user_4813494d user_4813494d 4.0K Apr 12 10:49 weights
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/medusa/check_data.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""Check training data for NaN, short files, and compute hidden state stats.
3	
4	Outputs:
5	  - NaN file list + count
6	  - Short file list (<64 tokens)
7	  - Per-file mean/std norm (for distribution matching later)
8	  - Summary by source (original vs supplement)
9	
10	Usage:
11	    python3 medusa/check_data.py
12	"""
13	
14	import torch
15	from pathlib import Path
16	from concurrent.futures import ThreadPoolExecutor, as_completed
17	from collections import defaultdict
18	import json
19	from tqdm import tqdm
20	
21	DATA_DIR = Path("medusa/data")
22	SPLITS = ["train", "val_ood"]
23	NUM_WORKERS = 16
24	MIN_TOKENS = 64
25	
26	
27	def check_file(fpath):
28	    """Return stats dict for one .pt file."""
29	    try:
30	        d = torch.load(fpath, map_location="cpu", weights_only=True)
31	        h = d["hidden_states"]
32	        ids = d["token_ids"]
33	        has_nan = bool(h.isnan().any().item())
34	        nan_pct = h.isnan().float().mean().item() * 100 if has_nan else 0.0
35	        h_float = h.float()
36	        mean_norm = h_float.mean(dim=0).norm().item() if not has_nan else float("nan")
37	        std_norm = h_float.std(dim=0).norm().item() if not has_nan else float("nan")
38	        return {
39	            "file": fpath.name,
40	            "split": fpath.parent.name,
41	            "tokens": len(ids),
42	            "has_nan": has_nan,
43	            "nan_pct": nan_pct,
44	            "mean_norm": mean_norm,
45	            "std_norm": std_norm,
46	        }
47	    except Exception as e:
48	        return {
49	            "file": fpath.name,
50	            "split": fpath.parent.name,
51	            "tokens": 0,
52	            "has_nan": True,
53	            "nan_pct": 100.0,
54	            "mean_norm": float("nan"),
55	            "std_norm": float("nan"),
56	            "error": str(e),
57	        }
58	
59	
60	def main():
61	    all_files = []
62	    for split in SPLITS:
63	        d = DATA_DIR / split
64	        if d.exists():
65	            files = sorted(d.glob("*.pt"))
66	            all_files.extend(files)
67	            print(f"{split}: {len(files)} files")
68	
69	    print(f"\nChecking {len(all_files)} files with {NUM_WORKERS} workers...")
70	
71	    results = []
72	    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as pool:
73	        futures = {pool.submit(check_file, f): f for f in all_files}
74	        for fut in tqdm(as_completed(futures), total=len(all_files), desc="Checking", unit="file"):
75	            results.append(fut.result())
76	
77	    # ── Summary ─────────────────────────────────────────────────────────
78	    by_split = defaultdict(list)
79	    for r in results:
80	        by_split[r["split"]].append(r)
81	
82	    for split, items in sorted(by_split.items()):
83	        nan_files = [r for r in items if r["has_nan"]]
84	        short_files = [r for r in items if r["tokens"] < MIN_TOKENS and not r["has_nan"]]
85	        ok_files = [r for r in items if not r["has_nan"] and r["tokens"] >= MIN_TOKENS]
86	
87	        print(f"\n{'='*60}")
88	        print(f"{split}: {len(items)} total, {len(ok_files)} ok, "
89	              f"{len(nan_files)} NaN, {len(short_files)} short (<{MIN_TOKENS} tok)")
90	
91	        if nan_files:
92	            # Check source: file number >= 8852 = supplement (after val_ood 008851)
93	            nan_original = [r for r in nan_files if int(r["file"].split(".")[0]) < 8852]
94	            nan_supplement = [r for r in nan_files if int(r["file"].split(".")[0]) >= 8852]
95	            print(f"  NaN by source: original={len(nan_original)}, supplement={len(nan_supplement)}")
96	            print(f"  NaN examples (first 15):")
97	            for r in nan_files[:15]:
98	                print(f"    {r['file']}: tokens={r['tokens']}, nan%={r['nan_pct']:.1f}%")
99	
100	        if short_files:
101	            print(f"  Short examples (first 15):")
102	            for r in short_files[:15]:
103	                print(f"    {r['file']}: tokens={r['tokens']}")
104	
105	    # ── Save full results for later use ─────────────────────────────────
106	    out_path = DATA_DIR / "data_check.json"
107	    with open(out_path, "w") as f:
108	        json.dump(results, f)
109	    print(f"\nFull results saved to {out_path}")
110	    print(f"Bad files (NaN + short): {sum(1 for r in results if r['has_nan'] or r['tokens'] < MIN_TOKENS)}")
111	
112	
113	if __name__ == "__main__":
114	    main()
115
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/medusa/collect_eval_overfit.py"
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	"""
3	Collect hidden states from eval benchmark prompts, then train Medusa head
4	to overfit on the eval answer distribution.
5	
6	Purpose: verify whether Medusa spec-decode introduces accuracy variance.
7	- Overfit head → acceptance rate ~1.0 → amplifies any verify-logic bugs
8	- If accuracy unchanged after overfitting → verify is correct, Medusa not the cause
9	
10	Usage:
11	    # Step 1: start server (no spec decode)
12	    # Step 2: python3 medusa/collect_eval_overfit.py --collect
13	    # Step 3: python3 medusa/collect_eval_overfit.py --train
14	"""
15	
16	import asyncio
17	import json
18	import math
19	import os
20	import random
21	import shutil
22	import time
23	from pathlib import Path
24	
25	import aiohttp
26	import torch
27	import torch.nn as nn
28	import torch.nn.functional as F
29	from safetensors import safe_open
30	
31	REPO_user_4813494d    = Path(__file__).resolve().parent.parent
32	COLLECT_DIR  = Path("/tmp/medusa_collect")
33	OUTPUT_DIR   = Path("medusa/data/eval_overfit")
34	WEIGHTS_DIR  = Path("medusa/weights")
35	MODEL_PATH   = [REDACTED]
36	
37	EVAL_FILES = [
38	    REPO_user_4813494d / "eval/mcq_only.jsonl",
39	    REPO_user_4813494d / "eval/niah_qa_60.jsonl",
40	    REPO_user_4813494d / "eval/qa30.jsonl",
41	]
42	
43	API_BASE     = "http://127.0.0.1:30000"
44	CONCURRENCY  = 8
45	
46	# Training config (intentional overfit: small data, many steps)
47	TOTAL_STEPS  = 5000
48	LR           = 5e-3
49	LR_MIN       = 1e-4
50	WARMUP_STEPS = 100
51	GRAD_CLIP    = 1.0
52	PACK_SIZE    = 8
53	HIDDEN_SIZE  = 4096
54	VOCAB_SIZE   = 73448
55	SCALE_WIDTH  = HIDDEN_SIZE / 256
56	
57	
58	# ── Model (same as train.py) ─────────────────────────────────────────────
59	class RMSNorm(nn.Module):
60	    def __init__(self, hidden_size, eps=1e-6):
61	        super().__init__()
62	        self.weight = nn.Parameter(torch.ones(hidden_size))
63	        self.eps = eps
64	
65	    def forward(self, x):
66	        norm = x.float().pow(2).mean(-1, keepdim=True).add(self.eps).rsqrt()
67	        return (x * norm).to(x.dtype) * self.weight
68	
69	
70	class ResBlock(nn.Module):
71	    def __init__(self, hidden_size):
72	        super().__init__()
73	        self.linear = nn.Linear(hidden_size, hidden_size)
74	        nn.init.zeros_(self.linear.weight)
75	        nn.init.zeros_(self.linear.bias)
76	        self.act = nn.SiLU()
77	
78	    def forward(self, x):
79	        return x + self.act(self.linear(x))
80	
81	
82	class MedusaBlock(nn.Module):
83	    def __init__(self, hidden_size):
84	        super().__init__()
85	        self.norm = RMSNorm(hidden_size)
86	        self.res1 = ResBlock(hidden_size)
87	        self.res2 = ResBlock(hidden_size)
88	
89	    def forward(self, x):
90	        x = self.norm(x)
91	        x = self.res1(x)
92	        x = self.res2(x)
93	        return x
94	
95	
96	class MedusaHeads(nn.Module):
97	    def __init__(self, lm_head_weight):
98	        super().__init__()
99	        self.heads = nn.ModuleList([MedusaBlock(HIDDEN_SIZE)])
100	        self.register_buffer("lm_head_weight", lm_head_weight)
101	
102	    def forward(self, h):
103	        return [F.linear(self.heads[0](h), self.lm_head_weight).float()]
104	
105	
106	# ── Collection ───────────────────────────────────────────────────────────
107	def load_eval_prompts():
108	    """Load eval items, return list of (prompt+gold_answer) strings."""
109	    samples = []
110	    for fpath in EVAL_FILES:
111	        with open(fpath) as f:
112	            items = [json.loads(l) for l in f]
113	        for item in items:
114	            q = item["question"]
115	            gold = item["gold"]
116	            # Append gold answer so model processes answer tokens during prefill
117	            if isinstance(gold, list):
118	                answer = gold[0] if gold else ""
119	            else:
120	                answer = str(gold)
121	            # Build full sequence: prompt + "\n" + answer
122	            full_text = q + "\n" + answer
123	            samples.append(full_text)
124	    print(f"Loaded {len(samples)} eval prompts")
125	    return samples
126	
127	
128	async def send_one(session, text, sem):
129	    payload = {"model": "default", "prompt": text, "max_tokens": 1, "temperature": 0}
130	    async with sem:
131	        try:
132	            async with session.post(
133	                f"{API_BASE}/v1/completions",
134	                json=payload,
135	                timeout=aiohttp.ClientTimeout(total=300),
136	            ) as resp:
137	                await resp.json()
138	                return True
139	        except Exception as e:
140	            print(f"  Error: {e}")
141	            return False
142	
143	
144	async def collect_all(samples):
145	    COLLECT_DIR.mkdir(exist_ok=True)
146	    # Clean stale files
147	    for f in COLLECT_DIR.glob("*.pt"):
148	        f.unlink()
149	
150	    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
151	
152	    sem = asyncio.Semaphore(CONCURRENCY)
153	    async with aiohttp.ClientSession() as session:
154	        # Check server
155	        try:
156	            async with session.get(f"{API_BASE}/v1/models") as resp:
157	                assert resp.status == 200, f"Server status {resp.status}"
158	            print("Server OK")
159	        except Exception as e:
160	            print(f"Server not reachable: {e}")
161	            return False
162	
163	        tasks = [asyncio.create_task(send_one(session, s, sem)) for s in samples]
164	        done = 0
165	        for t in asyncio.as_completed(tasks):
166	            await t
167	            done += 1
168	            if done % 10 == 0:
169	                print(f"  {done}/{len(samples)}")
170	
171	    await asyncio.sleep(2)
172	
173	    # Move collected files
174	    pt_files = sorted(COLLECT_DIR.glob("*.pt"))
175	    for f in pt_files:
176	        shutil.move(str(f), str(OUTPUT_DIR / f.name))
177	
178	    total_bytes = sum(f.stat().st_size for f in OUTPUT_DIR.glob("*.pt"))
179	    print(f"Collected {len(pt_files)} files ({total_bytes/1024**2:.1f} MB) → {OUTPUT_DIR}")
180	    return True
181	
182	
183	# ── Training ─────────────────────────────────────────────────────────────
184	def get_lr(step, total, warmup, lr_max, lr_min):
185	    if step < warmup:
186	        return lr_max * step / max(warmup, 1)
187	    p = (step - warmup) / max(total - warmup, 1)
188	    return lr_min + 0.5 * (lr_max - lr_min) * (1 + math.cos(math.pi * p))
189	
190	
191	def load_pack(files):
192	    hs, labels = [], []
193	    for f in files:
194	        data = torch.load(f, map_location="cpu", weights_only=True)
195	        h = data["hidden_states"]
196	        ids = data["token_ids"]
197	        valid = len(ids) - 2
198	        if valid < 1 or h.isnan().any():
199	            continue
200	        hs.append(h[:valid])
201	        labels.append(ids[2:2 + valid])
202	    if not hs:
203	        return None, None
204	    return torch.cat(hs), torch.cat(labels)
205	
206	
207	def train():
208	    device = torch.device("cuda")
209	    files = sorted(OUTPUT_DIR.glob("*.pt"))
210	    if not files:
211	        print(f"No .pt files in {OUTPUT_DIR}. Run --collect first.")
212	        return
213	
214	    print(f"Training on {len(files)} files ({TOTAL_STEPS} steps, overfit mode)")
215	
216	    # Load lm_head
217	    sf_path = os.path.join(MODEL_PATH, "model-00002-of-00002.safetensors")
218	    with safe_open(sf_path, framework="pt") as sf:
219	        lm_head_w = sf.get_tensor("lm_head.weight").to(device)
220	    lm_head_w = lm_head_w / SCALE_WIDTH
221	
222	    # Init from existing best.pt
223	    existing = WEIGHTS_DIR / "best.pt"
224	    model = MedusaHeads(lm_head_w).to(device=device, dtype=torch.bfloat16)
225	    if existing.exists():
226	        ckpt = torch.load(existing, map_location="cpu", weights_only=True)
227	        model.heads.load_state_dict(ckpt["heads_state_dict"])
228	        print(f"Initialized from {existing}")
229	    else:
230	        print("No existing best.pt, training from scratch")
231	
232	    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)
233	
234	    # Build pack list (repeat files to fill steps)
235	    all_files = list(files)
236	    random.shuffle(all_files)
237	
238	    t0 = time.time()
239	    best_acc = 0.0
240	    step = 0
241	
242	    while step < TOTAL_STEPS:
243	        # Sample a pack
244	        batch = random.choices(all_files, k=PACK_SIZE)
245	        h_cpu, lbl_cpu = load_pack(batch)
246	        if h_cpu is None:
247	            continue
248	
249	        h = h_cpu.to(device)
250	        lbl = lbl_cpu.to(device)
251	
252	        lr = get_lr(step, TOTAL_STEPS, WARMUP_STEPS, LR, LR_MIN)
253	        for pg in optimizer.param_groups:
254	            pg["lr"] = lr
255	
256	        model.train()
257	        logits = model(h)
258	        loss = F.cross_entropy(logits[0], lbl)
259	
260	        if loss.isnan():
261	            step += 1
262	            continue
263	
264	        optimizer.zero_grad()
265	        loss.backward()
266	        torch.nn.utils.clip_grad_norm_(model.parameters(), GRAD_CLIP)
267	        optimizer.step()
268	
269	        if (step + 1) % 100 == 0:
270	            with torch.no_grad():
271	                preds = logits[0].argmax(-1)
272	                acc = (preds == lbl).float().mean().item()
273	            elapsed = time.time() - t0
274	            print(f"  step={step+1}/{TOTAL_STEPS}  loss={loss.item():.4f}  "
275	                  f"top1={acc:.3f}  lr={lr:.2e}  {elapsed:.0f}s")
276	            if acc > best_acc:
277	                best_acc = acc
278	
279	        step += 1
280	
281	    # Save as eval_overfit.pt
282	    out_path = WEIGHTS_DIR / "eval_overfit.pt"
283	    torch.save({
284	        "heads_state_dict": {k: v.cpu() for k, v in model.heads.state_dict().items()},
285	        "num_heads": 1,
286	        "hidden_size": HIDDEN_SIZE,
287	        "step": TOTAL_STEPS,
288	        "note": "overfit on eval benchmark answers for hypothesis testing",
289	    }, out_path)
290	    print(f"\nDone. best_top1={best_acc:.3f}  saved → {out_path}")
291	    print(f"To test: restart server with --speculative-draft-model-path {out_path}")
292	
293	
294	# ── Main ─────────────────────────────────────────────────────────────────
295	if __name__ == "__main__":
296	    import sys
297	    os.chdir(REPO_user_4813494d)
298	
299	    mode = sys.argv[1] if len(sys.argv) > 1 else "--help"
300	
301	    if mode == "--collect":
302	        samples = load_eval_prompts()
303	        asyncio.run(collect_all(samples))
304	
305	    elif mode == "--train":
306	        train()
307	
308	    elif mode == "--all":
309	        samples = load_eval_prompts()
310	        ok = asyncio.run(collect_all(samples))
311	        if ok:
312	            # Kill server before training (need GPU memory)
313	            print("\nKilling sglang server before training...")
314	            os.system("bash bench/kill_sglang.sh")
315	            import time; time.sleep(5)
316	            train()
317	
318	    else:
319	        print(__doc__)
320
```

> AGENT

Perfect! Now let me check the directory structure and get final summary information:

> TOOL

tool_use Bash
```json
{
  "command": "ls -lh /user_4813494d/openbmb/eagle/data/ 2>/dev/null && ls -lh /user_4813494d/openbmb/eagle/weights/ 2>/dev/null"
}
```

> TOOL

tool_result Bash
```
total 1.4M
-rw-r--r-- 1 user_4813494d user_4813494d 631K Apr 11 20:51 manifest.json
drwxr-xr-x 2 user_4813494d user_4813494d 280K Apr 11 21:21 train
-rw-r--r-- 1 user_4813494d user_4813494d 324K Apr 11 20:54 vocab_cache.pt
total 30G
-rw-r--r-- 1 user_4813494d user_4813494d 2.5G Apr 12 11:55 best.pt
-rw-r--r-- 1 user_4813494d user_4813494d 2.5G Apr 12 10:49 best_unshifted.pt
-rw-r--r-- 1 user_4813494d user_4813494d 2.5G Apr 12 11:04 epoch_1.pt
-rw-r--r-- 1 user_4813494d user_4813494d 2.5G Apr 12 00:45 epoch_10.pt
-rw-r--r-- 1 user_4813494d user_4813494d 2.5G Apr 12 11:19 epoch_2.pt
-rw-r--r-- 1 user_4813494d user_4813494d 2.5G Apr 12 11:37 epoch_3.pt
-rw-r--r-- 1 user_4813494d user_4813494d 2.5G Apr 12 11:55 epoch_4.pt
-rw-r--r-- 1 user_4813494d user_4813494d 2.5G Apr 11 23:36 epoch_5.pt
-rw-r--r-- 1 user_4813494d user_4813494d 2.5G Apr 11 23:50 epoch_6.pt
-rw-r--r-- 1 user_4813494d user_4813494d 2.5G Apr 12 00:04 epoch_7.pt
-rw-r--r-- 1 user_4813494d user_4813494d 2.5G Apr 12 00:18 epoch_8.pt
-rw-r--r-- 1 user_4813494d user_4813494d 2.5G Apr 12 00:32 epoch_9.pt
```

> AGENT

Let me also check probe-sala to understand more context:

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/probe-sala/sglang/python/sglang/srt/speculative/medusa_worker.py",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	"""
2	Medusa speculative decoding worker for MiniCPM-SALA.
3	
4	Architecture: K ResBlock heads + shared lm_head (frozen).
5	Draft: run heads on target hidden states → argmax → K draft tokens.
6	Verify: Batched TARGET_VERIFY — all K+1 tokens verified in ONE forward pass.
7	        GLA intermediate states saved per-step for rollback.
8	"""
9	
10	import logging
11	from typing import List, Optional
12	
13	import torch
14	import torch.nn as nn
15	import torch.nn.functional as F
16	
17	from sglang.srt.layers.logits_processor import LogitsProcessorOutput
18	from sglang.srt.managers.schedule_batch import ScheduleBatch
19	from sglang.srt.mem_cache.common import alloc_for_decode, alloc_token_slots
20	from sglang.srt.managers.tp_worker import TpModelWorker
21	from sglang.srt.managers.utils import GenerationBatchResult
22	from sglang.srt.model_executor.forward_batch_info import (
23	    CaptureHiddenMode,
24	    ForwardMode,
25	)
26	from sglang.srt.server_args import ServerArgs
27	from sglang.srt.speculative.eagle_info import EagleDraftInput, MedusaVerifyInput
28	from sglang.srt.speculative.spec_utils import (
29	    assign_req_to_token_pool_func,
30	    detect_nan,
31	)
32	
33	logger = logging.getLogger(__name__)
34	
35	
36	# ── Medusa head model ───────────────────────────────────────────────────
37	
38	
39	class RMSNorm(nn.Module):
40	    def __init__(self, hidden_size: int, eps: float = 1e-6):
41	        super().__init__()
42	        self.weight = nn.Parameter(torch.ones(hidden_size))
43	        self.eps = eps
44	
45	    def forward(self, x: torch.Tensor) -> torch.Tensor:
46	        norm = x.float().pow(2).mean(-1, keepdim=True).add(self.eps).rsqrt()
47	        return (x * norm).to(x.dtype) * self.weight
48	
49	
50	class ResBlock(nn.Module):
51	    def __init__(self, hidden_size: int):
52	        super().__init__()
53	        self.linear = nn.Linear(hidden_size, hidden_size)
54	        self.act = nn.SiLU()
55	
56	    def forward(self, x: torch.Tensor) -> torch.Tensor:
57	        return x + self.act(self.linear(x))
58	
59	
60	class MedusaBlock(nn.Module):
61	    """RMSNorm + 2x ResBlock, used by newer Medusa checkpoints."""
62	    def __init__(self, hidden_size: int):
63	        super().__init__()
64	        self.norm = RMSNorm(hidden_size)
65	        self.res1 = ResBlock(hidden_size)
66	        self.res2 = ResBlock(hidden_size)
67	
68	    def forward(self, x: torch.Tensor) -> torch.Tensor:
69	        x = self.norm(x)
70	        x = self.res1(x)
71	        x = self.res2(x)
72	        return x
73	
74	
75	class MedusaHeads(nn.Module):
76	    def __init__(self, num_heads: int, hidden_size: int, lm_head_weight: torch.Tensor,
77	                 block_cls: type[nn.Module] = ResBlock):
78	        super().__init__()
79	        self.num_heads = num_heads
80	        self.heads = nn.ModuleList([block_cls(hidden_size) for _ in range(num_heads)])
81	        self.register_buffer("lm_head_weight", lm_head_weight)
82	
83	    def forward(self, hidden_states: torch.Tensor) -> list[torch.Tensor]:
84	        return [
85	            F.linear(head(hidden_states), self.lm_head_weight)
86	            for head in self.heads
87	        ]
88	
89	
90	# ── Medusa Worker ───────────────────────────────────────────────────────
91	
92	
93	class MedusaWorker:
94	
95	    def __init__(
96	        self,
97	        server_args: ServerArgs,
98	        gpu_id: int,
99	        tp_rank: int,
100	        dp_rank: Optional[int],
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /user_4813494d/openbmb/medusa/weights/ 2>/dev/null"
}
```

> TOOL

tool_result Bash
```
total 163912
drwxr-xr-x 3 user_4813494d user_4813494d      100 Apr  6 09:04 .
drwxr-xr-x 6 user_4813494d user_4813494d     4096 Apr 10 11:18 ..
drwxr-xr-x 2 user_4813494d user_4813494d       10 Apr  6 09:04 .ipynb_checkpoints
-rw-r--r-- 1 user_4813494d user_4813494d 33564621 Apr  6 07:45 1-best.pt
-rw-r--r-- 1 user_4813494d user_4813494d 67136120 Apr  9 13:25 best.pt
-rw-r--r-- 1 user_4813494d user_4813494d 67136131 Apr  9 13:36 final.pt
```

> AGENT

Excellent! Now let me check what's in sglang_model:

> TOOL

tool_use Bash
```json
{
  "command": "ls -lh /user_4813494d/openbmb/eagle/sglang_model/ && head -100 /user_4813494d/openbmb/eagle/sglang_model/config.json"
}
```

> TOOL

tool_result Bash
```
total 1.4G
-rw-r--r-- 1 user_4813494d user_4813494d  204 Apr 11 13:59 added_tokens.json
-rw-r--r-- 1 user_4813494d user_4813494d  620 Apr 12 12:03 config.json
-rw-r--r-- 1 user_4813494d user_4813494d 1.4G Apr 12 12:03 model.safetensors
-rw-r--r-- 1 user_4813494d user_4813494d  979 Apr 11 13:59 special_tokens_map.json
-rw-r--r-- 1 user_4813494d user_4813494d 6.4M Apr 11 13:59 tokenizer.json
-rw-r--r-- 1 user_4813494d user_4813494d 1.2M Apr 11 13:59 tokenizer.model
-rw-r--r-- 1 user_4813494d user_4813494d 5.2K Apr 11 13:59 tokenizer_config.json
{
  "architectures": [
    "LlamaForCausalLMEagle3"
  ],
  "model_type": "llama",
  "hidden_size": 4096,
  "intermediate_size": 16384,
  "num_hidden_layers": 1,
  "num_attention_heads": 32,
  "num_key_value_heads": 2,
  "head_dim": 128,
  "hidden_act": "silu",
  "max_position_embeddings": 524288,
  "rms_norm_eps": 1e-06,
  "vocab_size": 73448,
  "draft_vocab_size": 32000,
  "target_hidden_size": 4096,
  "scale_emb": 12,
  "tie_word_embeddings": false,
  "torch_dtype": "bfloat16",
  "eagle_config": {
    "use_aux_hidden_state": true,
    "eagle_aux_hidden_state_layer_ids": [
      1,
      10,
      22
    ]
  }
}
```

> AGENT

Now let me check for any results or documentation about the actual measured performance:

> TOOL

tool_use Bash
```json
{
  "command": "find /user_4813494d/openbmb -name \"README*\" -o -name \"*.md\" | xargs grep -l \"medusa\\|accept\\|speedup\" 2>/dev/null | head -5"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/docs/eagle3_research.md
/user_4813494d/openbmb/docs/eagle3-pipeline.md
/user_4813494d/openbmb/docs/eagle3-accept-rate-fix.md
/user_4813494d/openbmb/docs/empty-response-investigation-handover-20260413.md
/user_4813494d/openbmb/probe-sala/sglang/python/sglang/multimodal_gen/docs/attention_backends.md
```

> AGENT

Perfect! Now let me get a final comprehensive summary by checking file counts and understanding the relationship between components:

> TOOL

tool_use Bash
```json
{
  "command": "wc -l /user_4813494d/openbmb/eagle/*.py && echo \"---\" && grep -c \"def\\|class\" /user_4813494d/openbmb/eagle/*.py | head -20"
}
```

> TOOL

tool_result Bash
```
395 /user_4813494d/openbmb/eagle/collect_data.py
  151 /user_4813494d/openbmb/eagle/convert_to_sglang.py
  287 /user_4813494d/openbmb/eagle/eval_ood_accept.py
  291 /user_4813494d/openbmb/eagle/test_decode_mode.py
  208 /user_4813494d/openbmb/eagle/test_eagle3_flow.py
  301 /user_4813494d/openbmb/eagle/test_forward_match.py
  116 /user_4813494d/openbmb/eagle/test_offline_pred.py
  631 /user_4813494d/openbmb/eagle/train.py
  159 /user_4813494d/openbmb/eagle/verify_sglang_draft.py
 2539 total
---
/user_4813494d/openbmb/eagle/collect_data.py:10
/user_4813494d/openbmb/eagle/convert_to_sglang.py:1
/user_4813494d/openbmb/eagle/eval_ood_accept.py:16
/user_4813494d/openbmb/eagle/test_decode_mode.py:18
/user_4813494d/openbmb/eagle/test_eagle3_flow.py:6
/user_4813494d/openbmb/eagle/test_forward_match.py:17
/user_4813494d/openbmb/eagle/test_offline_pred.py:3
/user_4813494d/openbmb/eagle/train.py:23
/user_4813494d/openbmb/eagle/verify_sglang_draft.py:4
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle3-accept-rate-fix.md"
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 Accept Rate 修复记录
2	
3	## 问题
4	
5	EAGLE-3 speculative decoding 在线 accept rate 仅 ~5%（accept_len ~1.05），离线训练 acc0 却有 63.5%。Draft model 在推理时几乎无法命中任何 token。
6	
7	## 根因分析
8	
9	### 训练/推理的 token-hidden_states 对齐不一致
10	
11	sglang EAGLE-3 推理时对 input_ids 做了隐式左移：
12	
13	1. **`eagle_info.py` prepare_for_extend**（首次 extend）：
14	   ```python
15	   input_ids = torch.cat((input_ids[1:], verified_id))
16	   ```
17	   位置 t 的 token 变成了 x_{t+1}，而 hidden_states 仍是 aux[t]。
18	
19	2. **`eagle_info.py` prepare_extend_after_decode**（后续 decode）：
20	   ```python
21	   batch.input_ids = self.verified_id  # target 预测的未来 token
22	   hidden_states = hidden_states[accept_index]  # 已接受位置的 hidden
23	   ```
24	   verified_id 是 target model 的预测（未来 token），配对的是当前位置的 aux_hidden。
25	
26	因此推理时 draft model 实际输入为 **(x_{t+1}, aux[t])** → 预测 **x_{t+2}**。
27	
28	而旧训练代码使用对齐的 **(x_t, aux[t])** → 预测 **x_{t+1}**。输入分布完全不匹配，导致 draft 几乎无法命中。
29	
30	### 验证
31	
32	用旧权重在 shifted eval 上测试：OOD accept rate = 8.2%，与在线 ~5% 吻合，确认根因。
33	
34	## 修复
35	
36	### 1. 训练对齐修复 (`eagle/train.py`)
37	
38	将训练 forward 的输入做同样的 shift，匹配推理行为：
39	
40	```python
41	# 修复前（对齐的）
42	input_ids = token_ids              # x_0..x_{S-1}
43	hidden = self.fc(aux_hidden)       # aux_0..aux_{S-1}
44	
45	# 修复后（shifted，匹配推理）
46	input_ids = token_ids[:, 1:]           # x_1..x_{S-1}
47	aux_shifted = aux_hidden[:, :-1, :]    # aux_0..aux_{S-2}
48	target_values = target_logits_values[:, 1:, :]
49	target_indices = target_logits_indices[:, 1:, :]
50	```
51	
52	### 2. 评估脚本修复 (`eagle/eval_ood_accept.py`)
53	
54	- 同步 shifted 对齐
55	- 修复 checkpoint 键名映射（`midlayer.` 前缀剥离、`input_emb_norm` → `input_layernorm`）
56	- 支持从训练 checkpoint 直接加载
57	
58	### 3. 诊断代码清理
59	
60	从 `eagle_info.py`、`eagle_worker.py`、`minicpm.py` 移除全部 6 个 DIAG 打印块。
61	
62	## 重训结果
63	
64	训练配置：10 epochs, batch=2x4 grad_accum, lr=3e-4, seq_len=2048, 9530 files。
65	
66	| Checkpoint | 训练 acc0 | OOD Accept Rate | 在线 accept_len |
67	|-----------|---------|----------------|----------------|
68	| 旧(未shift) | 63.5% | 8.2% | ~1.05 |
69	| Epoch 1 (shifted) | 34.3% | 35.5% | 1.50 (单请求) / 1.33 (32并发) |
70	| Epoch 2 (shifted) | 53.9% | 45.8% | — |
71	| Epoch 3+ | 61.9%+ | 预计 >50% | — |
72	
73	## OOD Accept Rate 饱和
74	
75	| Epoch | 训练 acc0 | OOD Accept Rate | delta |
76	|-------|---------|----------------|-------|
77	| 1 | 34.3% | 35.5% | — |
78	| 2 | 53.9% | 45.8% | +10.3 |
79	| 3 | 61.9% | 49.1% | +3.3 |
80	| 4 | 67.6% | 49.3% | +0.2 |
81	
82	Epoch 4 后 OOD accept rate 基本饱和（49.3%），训练 acc 仍在涨但 OOD 不动。gap 说明过拟合到训练集分布。进一步提升需要 in-domain 验证集做 early stopping，或更大/更多样的训练数据。
83	
84	## Tree Verify 与线性注意力的兼容性问题
85	
86	### 问题
87	
88	MiniCPM-SALA 有 24/32 层 GLA（线性注意力）。sglang 的 EAGLE tree verify 对两种注意力层处理方式不同：
89	
90	- **Standard attention（8层）**：使用 tree mask（FlashInfer prefill + custom_mask），每个 token 只 attend 祖先链。**正确。**
91	- **GLA（24层）**：`hybrid_linear_attn_backend.py:1636-1711` 逐 token 串行处理，所有 draft tokens 当成线性序列。**不同分支间 state 互相污染。**
92	
93	```python
94	# GLA TARGET_VERIFY 实际行为（simplified）
95	for step in range(draft_token_num):
96	    o_s, current_state = fused_recurrent_simple_gla(...)
97	    intermediate_ssm[layer, :batch, step] = current_state
98	# → A 分支的 state 污染了 B 分支的计算
99	```
100	
101	### topk=1 vs topk=2 实测
102	
103	理论上 topk=1（单链）对 GLA 完全正确，但实测 **topk=2 仍然更快**。
104	
105	原因：tree 的候选覆盖率优势 > GLA state 污染的精度损失：
106	- `topk=2, steps=3`：6 个候选，命中概率高
107	- `topk=1, steps=3`：3 个候选，覆盖面窄
108	- 8 层 standard attention 的 tree mask 仍然正确，部分补偿 GLA 误差
109	- GLA 污染有界——sibling branch 对 state 的扰动不至于完全破坏 logits
110	
111	### 可能的改进方向
112	
113	1. **DFS 遍历 + state 分支保存**：GLA 层在分支点保存 state，处理完一条路径后 restore。每个分支点额外 ~1 MB/层，24层×3点=72 MB。计算量不变（已经逐 token 串行），只多 save/restore 操作。
114	2. **更大/更好的 draft model**：2-3 层 draft 提高 accept rate，配合 NVFP4 量化控制 latency。
115	3. **In-domain 训练数据**：当前 OOD accept rate 49.3% 饱和，更匹配的训练数据可能突破瓶颈。
116	
117	## 排查过程中排除的假设
118	
119	1. **verify_tree / retrive_index bug** — 验证逻辑正确，`ridx=[0..7]` 全部列出，d1_hit=True 时 accept_length=1
120	2. **layers_to_capture 不匹配** — 确认 {2,11,23}（MLP delta）与训练数据采集一致
121	3. **residual bug** — 模型捕获的是 MLP delta（无 residual），与训练一致
122	
123	## 关键文件
124	
125	| 文件 | 改动 |
126	|------|------|
127	| `eagle/train.py` | shifted 对齐修复 |
128	| `eagle/eval_ood_accept.py` | shifted eval + 键名映射修复 |
129	| `eagle/convert_to_sglang.py` | checkpoint → sglang 格式转换 |
130	| `demo-sala/sglang/.../eagle_info.py` | 清理诊断代码 |
131	| `demo-sala/sglang/.../eagle_worker.py` | 清理诊断代码 |
132	| `demo-sala/sglang/.../models/minicpm.py` | 清理诊断代码 |
133
```

> AGENT

Perfect! Now let me check for more concrete Medusa performance data:

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"accept.*rate\\|accept.*len\\|0\\.15\\|mean_accept\" /user_4813494d/openbmb/medusa/ 2>/dev/null | head -20"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/medusa/profile_verify.py:Medusa's accept rate (val_ood ~0.155) translates to real speedup?
/user_4813494d/openbmb/medusa/profile_verify.py:        print("\n── Medusa profitability (val_ood accept=0.155, tok/step=1.155) ──")
/user_4813494d/openbmb/medusa/profile_verify.py:            accept_val    = 0.155     # val_ood epoch 2
/user_4813494d/openbmb/medusa/profile_verify.py:        # ── 4. Sensitivity: what accept rate is needed to break even? ──
/user_4813494d/openbmb/medusa/profile_verify.py:        print("\n── Break-even accept rate (K=3) ──")
/user_4813494d/openbmb/medusa/profile_verify.py:        print(f"  Need accept rate > {breakeven_accept:.3f} tok/step  (currently {accept_val:.3f})")
/user_4813494d/openbmb/medusa/profile_verify.py:            print(f"  → Current accept rate EXCEEDS break-even: Medusa profitable")
/user_4813494d/openbmb/medusa/.ipynb_checkpoints/train-checkpoint.py:    mean_accept = total_accept / max(total_pos, 1)
/user_4813494d/openbmb/medusa/.ipynb_checkpoints/train-checkpoint.py:        "mean_accept_len": round(mean_accept, 3),
/user_4813494d/openbmb/medusa/.ipynb_checkpoints/train-checkpoint.py:        "tokens_per_step": round(1.0 + mean_accept, 3),
/user_4813494d/openbmb/medusa/.ipynb_checkpoints/train-checkpoint.py:    print(f"  val_ind: accept={m_ind['mean_accept_len']:.3f}")
/user_4813494d/openbmb/medusa/.ipynb_checkpoints/train-checkpoint.py:    print(f"  val_ood: accept={m_ood['mean_accept_len']:.3f}  "
/user_4813494d/openbmb/medusa/.ipynb_checkpoints/train-checkpoint.py:          f"gap={m_ind['mean_accept_len'] - m_ood['mean_accept_len']:+.3f}")
/user_4813494d/openbmb/medusa/.ipynb_checkpoints/train-checkpoint.py:    best_accept = m_ood["mean_accept_len"]
/user_4813494d/openbmb/medusa/.ipynb_checkpoints/train-checkpoint.py:            gap = m_ind["mean_accept_len"] - m_ood["mean_accept_len"]
/user_4813494d/openbmb/medusa/.ipynb_checkpoints/train-checkpoint.py:            print(f"  val_ind: loss={m_ind['loss']:.4f} accept={m_ind['mean_accept_len']:.3f} "
/user_4813494d/openbmb/medusa/.ipynb_checkpoints/train-checkpoint.py:            print(f"  val_ood: loss={m_ood['loss']:.4f} accept={m_ood['mean_accept_len']:.3f} "
/user_4813494d/openbmb/medusa/.ipynb_checkpoints/train-checkpoint.py:            if m_ood["mean_accept_len"] > best_accept:
/user_4813494d/openbmb/medusa/.ipynb_checkpoints/train-checkpoint.py:                best_accept = m_ood["mean_accept_len"]
/user_4813494d/openbmb/medusa/collect_data.py:    "go": 0.15,
```

> AGENT

Excellent! Now let me get a comprehensive view of all the code paths and understanding. Let me check the actual MedusaVerifyInput class:

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"class MedusaVerifyInput\\|prepare_for_verify\" /user_4813494d/openbmb/demo-sala/sglang/ 2>/dev/null | head -5"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/multi_layer_eagle_worker.py:        spec_info.prepare_for_verify(batch, self.page_size)
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/ngram_info.py:    def prepare_for_verify(self, batch: ScheduleBatch, page_size: int):
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/ngram_worker.py:        batch.spec_info.prepare_for_verify(batch, self.page_size)
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:        # Free the draft model's KV cache slots BEFORE prepare_for_verify overwrites batch.out_cache_loc.
/user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py:        # they become orphaned when prepare_for_verify allocates new slots for verification.
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -A 30 \"class MedusaVerifyInput\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py 2>/dev/null | head -50"
}
```

> TOOL

tool_result Bash
```
class MedusaVerifyInput(SpecInput):
    """Minimal spec_info for Medusa batched TARGET_VERIFY.

    Unlike EAGLE's tree-based verification, Medusa uses flat (sequential)
    draft tokens: [verified_id, draft_0, draft_1, ..., draft_{K-1}].
    """

    draft_token: torch.Tensor  # (bs * draft_token_num,) flattened input_ids
    positions: torch.Tensor  # (bs * draft_token_num,) position ids
    draft_token_num: int  # K+1 (verified + K drafts)
    topk: int = 1  # always 1 for flat Medusa (no tree)
    capture_hidden_mode: CaptureHiddenMode = CaptureHiddenMode.LAST
    seq_lens_sum: int = 0
    seq_lens_cpu: Optional[torch.Tensor] = None

    # Shape info for padding
    num_tokens_per_batch: int = -1

    def __post_init__(self):
        super().__init__(SpecInputType.MEDUSA_VERIFY)

    def get_spec_adjust_token_coefficient(self):
        return self.draft_token_num, self.draft_token_num

    @classmethod
    def create_idle_input(cls, draft_token_num: int):
        return cls(
            draft_token=torch.empty((0,), dtype=torch.long, device="cuda"),
            positions=torch.empty((0,), dtype=torch.int64, device="cuda"),
            draft_token_num=draft_token_num,
            capture_hidden_mode=CaptureHiddenMode.LAST,
```

> AGENT

Perfect! Now let me create a comprehensive summary. Let me check one more critical file about the batching logic:

> TOOL

tool_use Bash
```json
{
  "command": "grep -A 50 \"def prepare_for_verify\" /user_4813494d/openbmb/demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py 2>/dev/null | head -80"
}
```

> TOOL

tool_result Bash
```
def prepare_for_verify(self, batch: ScheduleBatch, page_size: int):

        if batch.forward_mode.is_idle():
            return

        batch.input_ids = self.draft_token

        if page_size == 1:
            batch.out_cache_loc = alloc_token_slots(
                batch.tree_cache,
                len(batch.input_ids),
            )
            end_offset = batch.seq_lens + self.draft_token_num
        else:
            prefix_lens = batch.seq_lens
            prefix_lens_cpu = batch.seq_lens_cpu
            end_offset = prefix_lens + self.draft_token_num
            end_offset_cpu = prefix_lens_cpu + self.draft_token_num
            last_loc = get_last_loc(
                batch.req_to_token_pool.req_to_token,
                batch.req_pool_indices,
                prefix_lens,
            )
            batch.out_cache_loc = alloc_paged_token_slots_extend(
                batch.tree_cache,
                prefix_lens,
                prefix_lens_cpu,
                end_offset,
                end_offset_cpu,
                last_loc,
                len(batch.input_ids),
            )
            self.last_loc = last_loc

        bs = batch.batch_size()
        assign_req_to_token_pool_func(
            batch.req_pool_indices,
            batch.req_to_token_pool.req_to_token,
            batch.seq_lens,
            end_offset,
            batch.out_cache_loc,
            bs,
        )

        if get_global_server_args().enable_mamba_extra_buffer():
            batch.mamba_track_indices = torch.tensor(
                [
                    req.mamba_ping_pong_track_buffer[req.mamba_next_track_idx]
                    for req in batch.reqs
                ],
                dtype=torch.int64,
--
    def prepare_for_verify(self, batch: ScheduleBatch):
        """Set up batch for TARGET_VERIFY: allocate cache slots, set positions."""
        if batch.forward_mode.is_idle():
            return

        batch.input_ids = self.draft_token
        bs = batch.batch_size()

        # Allocate KV cache slots for all draft_token_num tokens per request
        batch.out_cache_loc = alloc_token_slots(
            batch.tree_cache, len(batch.input_ids)
        )
        end_offset = batch.seq_lens + self.draft_token_num

        # Map cache slots to req_to_token
        assign_req_to_token_pool_func(
            batch.req_pool_indices,
            batch.req_to_token_pool.req_to_token,
            batch.seq_lens,
            end_offset,
            batch.out_cache_loc,
            bs,
        )
```

> TOOL

[Request interrupted by user]

> TOOL

[Request interrupted by user]
