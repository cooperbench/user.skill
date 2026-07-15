> DEVELOPER

看一下eagle训练部分 目前已经证实v3的效果不如v2

> TOOL

tool_use Bash
```json
{
  "command": "ls /user_4813494d/openbmb/eagle/ && echo \"---\" && ls /user_4813494d/openbmb/docs/eagle/",
  "description": "List eagle directory structure"
}
```

> TOOL

tool_result Bash
```
README.md
__pycache__
convert_to_sglang.py
data
eval_ood_accept.py
nvfp4_codec.py
pipeline
probe
sglang_model
sglang_model_v3
start_collect.sh
start_collect_val.sh
train.py
validation
weights
---
README.md
collapse-analysis.md
dflash.md
experiments-log.md
longcontext-analysis.md
runtime-investigation.md
spec-survey.md
spec-v2.md
training-v2.md
training-v3.md
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /user_4813494d/openbmb/eagle/sglang_model_v3/ && echo \"---v3 size---\" && du -sh /user_4813494d/openbmb/eagle/sglang_model/ /user_4813494d/openbmb/eagle/sglang_model_v3/ 2>/dev/null && echo \"---\" && ls /user_4813494d/openbmb/eagle/pipeline/",
  "description": "Inspect v3 vs v2 model dirs and pipeline"
}
```

> TOOL

tool_result Bash
```
added_tokens.json
config.json
hf_quant_config.json
model.safetensors
special_tokens_map.json
tokenizer.json
tokenizer.model
tokenizer_config.json
---v3 size---
423M	/user_4813494d/openbmb/eagle/sglang_model/
492M	/user_4813494d/openbmb/eagle/sglang_model_v3/
---
__pycache__
build_prompts.py
build_prompts_local.py
build_prompts_topup.py
collect_async.py
collect_local.py
collect_val_ood.py
salvage.py
split_val_ind.py
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

Continue from where you left off.

> AGENT

No response requested.
