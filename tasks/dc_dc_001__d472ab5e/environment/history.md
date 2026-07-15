> DEVELOPER

深入仔细阅读 谅解一下我们的工作和工作内容

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /user_4813494d/.claude/projects/-user_4813494d/memory/ 2>/dev/null && echo \"---\" && ls /user_4813494d/",
  "description": "Check memory directory and home"
}
```

> TOOL

tool_result Bash
```
total 4
drwxr-xr-x 2 user_4813494d user_4813494d   10 May 26 07:56 .
drwxr-xr-x 1 user_4813494d user_4813494d 4096 May 26 07:56 ..
---
Documents
backups
codex-setup.sh
data
demo-sala-001c2ad-20260511.tar.gz
deps
models
openbmb
openbmb-backup-20260512-1937.tar.gz
project
qutlass_src
recovered-0508
research
restart-tunnel.sh
start.sh
wzy_tars
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /user_4813494d/project/ /user_4813494d/research/ /user_4813494d/Documents/ 2>/dev/null",
  "description": "List key working directories"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/Documents/:
NVIDIA Nsight Compute

/user_4813494d/project/:

/user_4813494d/research/:
ddtree
ddtree_paper.pdf
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /user_4813494d/research/ddtree/ /user_4813494d/qutlass_src/ /user_4813494d/openbmb/ /user_4813494d/models/ /user_4813494d/wzy_tars/ /user_4813494d/deps/ 2>/dev/null | head -100",
  "description": "Look at potential work directories"
}
```

> TOOL

tool_result Bash
```
/user_4813494d/deps/:
repo-cutlass
repo-deepgemm
repo-fast-hadamard-transform
repo-flash-attention
repo-flashinfer
repo-flashmla
repo-fmt
repo-mscclpp
repo-triton

/user_4813494d/models/:
openbmb

/user_4813494d/openbmb/:
AGENTS.md
CLAUDE.md
bench
bin
demo-sala
demo-sala-20260524-090426.tar.gz
dflash
docs
eagle
eval
kernels
medusa
outputs
piecewise
prefill
probe-sala-acc
probe-sala-acc-20260524-092945.tar.gz
probe-sala-acc-20260525-091526.tar.gz
probe-sala-full
probe-sala-full-20260524-153025.tar.gz
probe-sala-full-20260524-153459.tar.gz
probe-sala-full-20260525-205122.tar.gz
probe-sala-full-backup-pre-e2e3bd6-20260525-092310.tar.gz
probe-sala-quant
probe-sala-s2
quant
scale
sglang_0524_3_custom.jsonl
sglang_0524_8_custom.jsonl
sglang_0525_5_custom.jsonl
submit
tests
toolkit

/user_4813494d/qutlass_src/:
CMakeLists.txt
LICENSE
README.md
assets
benchmarks
pyproject.toml
qutlass
requirements.txt
setup.py
tests
third_party

/user_4813494d/research/ddtree/:
LICENSE
README.md
benchmark.py
ddtree.py
dflash.py
distributed.py
make_latex_table.py
model
plot_results.py
requirements.txt
run_benchmark.sh

/user_4813494d/wzy_tars/:
demo-sala_d7_6_13_20260511.tar.gz
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/CLAUDE.md"
}
```

> TOOL

tool_result Read
```
1	# CLAUDE.md
2	
3	## 身份
4	
5	你是 AI 助手，不是人类工程师。你的效率比人类高很多——不要拿人类的工时尺度（"这要好几天"、"engineering 量大"）来套自己的工作量。
6	
7	## 语言
8	
9	**始终使用简体中文回复。严禁使用韩语、日语或其他语言。**
10	
11	## 项目定位
12	
13	SOAR 比赛工作区，优化 **OpenBMB/MiniCPM-SALA** 的推理。最终在官方云环境打分。
14	
15	**基座模型不可替换**，改动只能落在：量化方案、SGLang fork、推测解码 draft、kernel、平台部署脚本。
16	
17	## 模型架构
18	
19	- **32 layers 混合**：8 standard Attention（layer id = 0, 9, 16, 17, 22, 29, 30, 31）+ 24 Lightning Attention（GLA）
20	- `hidden_size=4096`，`intermediate_size=16384`，`nq/nkv=32/2`，`head_dim=128`
21	- `vocab_size=73448`，`max_position_embeddings=524288`（512K）
22	- **InfLLM-v2 路径**：**生产配置默认 `--dense-as-sparse`**（`server_args.py:570` 默认 True，`minicpm_backend.py:418` 把 `dense_len` 强制覆盖为 0），所有 8 层 standard Attention **无论 prefill 长度一律走 sparse 路径**（compress_k → stage1 block_score → stage2 top-K sparse FA）；hf config 默认 `sparse_dense_len=8192` 已不再生效。`--dense-as-sparse` 关闭后才会按长度阈值切换 dense/sparse，但这条路径不是生产，会带来精度问题（见 [`docs/quant/nvfp4.md`](docs/quant/nvfp4.md)）
23	
24	## 运行栈
25	
26	**硬件**：NVIDIA RTX 6000D（sm_120, Blackwell, 84 GB VRAM）
27	
28	| 组件 | 版本 |
29	|---|---|
30	| Python | 3.10.19（venv 预激活，`VIRTUAL_ENV=/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env`） |
31	| PyTorch | 2.11.0+cu130 |
32	| CUDA toolkit | 13.2 |
33	| cuDNN | [REDACTED]（sm_120 FP4 cudnn backend 硬要求） |
34	| FlashInfer | 0.6.8.post1[cu13] |
35	| sgl-kernel | 0.3.20 + 本仓库 `common_ops.abi3.so` 替换（Marlin FP4 scale bug fix） |
36	| Triton | 3.6.0 |
37	
38	## 当前生产配置
39	
40	- **量化**：NVFP4（GPTQ + FourOverSix，wikitext loguniform 90 样本校准，90K 上下文 `MAX_SEQ_LENGTH=92160`）
41	- **Decode […]

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/AGENTS.md"
}
```

> TOOL

tool_result Read
```
1	# Repository Guidelines
2	
3	> 项目总览 + 框架介绍见 [`CLAUDE.md`](CLAUDE.md)。本文档偏"协作者 onboarding"，涵盖路径分工、定制点、测试验收。
4	
5	## 1. 仓库定位
6	
7	这个仓库不是单一应用，而是围绕 SOAR / MiniCPM-SALA 推理优化比赛组织的工作区。三条活跃主线：
8	
9	- `demo-sala/` — **正式提交包**，平台真正消费
10	- `probe-sala/` — cu13 鉴权下发的平台诊断探针（BOS + 邮件回传 + 11 项 verify）
11	- 仓库根下 `eval/` / `bench/` / `eagle/` / `medusa/` / `quant/` / `kernels/` — 本地实验、精度排查、性能验证、草稿模型训练、CUDA kernel 研究
12	
13	## 2. 主线真实状态
14	
15	### 2.1 `demo-sala/` 提交路径
16	
17	- `demo-sala/prepare_env.sh`
18	  - `uv pip install --no-deps -e demo-sala/sglang/python` 装自定义 SGLang
19	  - `nvidia-modelopt==0.42.0` + `llmcompressor==[REDACTED]` + `nvidia-cudnn-cu13>=9.15` + `flashinfer-python[cu13]>=0.6.8.post1`
20	  - `demo-sala/patches/gptq_quantize_fouroversix.py` 覆盖 llmcompressor GPTQ 逻辑
21	  - 替换 `sgl_kernel/sm100/common_ops.abi3.so`（Marlin FP4 scale bug fix）
22	  - 导出 `SGLANG_SERVER_ARGS`（`modelopt_fp4` + `dense-as-sparse` + EAGLE3 chain verify）+ `SGLANG_MARLIN_DECODE_THRESHOLD=48` + `SGLANG_MINICPM_PLAN_CACHE=1`
23	- `demo-sala/prepare_model.sh` / `preprocess_model.py`
24	  - GPTQ + NVFP4 + FourOverSix
25	  - 校准集 `demo-sala/data/calib_wikitext_loguniform_128.jsonl`（48K 上下文）
26	  - 导出 llmcompressor → SGLang `modelopt_fp4` 可加载格式，恢复 `sparse_config` / `max_position_embeddings` / `lm_head`
27	
28	### 2.2 `probe-sala/` 平台诊断探针
29	
30	`probe-sala/` 功能类似 `demo-sala/`，但专为**平台差异定位**设计：
31	
32	- `prepare_env.sh`（563 行）— BOS 鉴权下发 92 个 pin wheel，cu12 purge via `dpkg --force-all`，flashinfer AOT 目录填充 skip JIT，失败 `kill -TERM` 强制终止评测
33	- `verify_env.py` — 11 项环境深度自检（libcudart 唯一、cuDNN 9.21、cudnn-frontend backend、torch 2.11+cu130、无 cu12 残留、sgl_kernel […]

> TOOL

tool_use Bash
```json
{
  "command": "ls /user_4813494d/openbmb/docs/ 2>/dev/null && echo \"---\" && ls /user_4813494d/openbmb/docs/handover* 2>/dev/null",
  "description": "List docs structure"
}
```

> TOOL

tool_result Bash
```
README.md
blog
candidates.md
decode
dflash
eagle
gemm
handover.md
ngram
platform
prefill
quant
---
/user_4813494d/openbmb/docs/handover.md
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/handover.md",
  "limit": 120
}
```

> TOOL

tool_result Read
```
1	# 全栈接续指南
2	
3	下一个 session 接续工作时优先读这份。链接到事实文档；不要把瞬时 bench 数字写进来。
4	
5	工作目录：`/user_4813494d/openbmb`；提交根目录：`demo-sala/`；custom SGLang 在 `demo-sala/sglang/python/`。
6	
7	> **红线、栈版本、运维规则、Monitor 规范**：全部在 [`/user_4813494d/openbmb/CLAUDE.md`](../CLAUDE.md)。本文档只
8	> 列接续工作必读的状态与路径，不重复 CLAUDE.md 内容。
9	
10	## 1. 当前生产配置（一行一个，指针为主）
11	
12	| 维度 | 来源 |
13	|---|---|
14	| 硬件 / 栈版本 | [CLAUDE.md §运行栈](../CLAUDE.md#运行栈) |
15	| 量化（NVFP4，GPTQ + FourOverSix，wikitext 90 样本，`MAX_SEQ_LENGTH=92160`） | [quant/nvfp4.md](quant/nvfp4.md) |
16	| Decode dispatch（生产默认全 Marlin；`SGLANG_ENABLE_B12X=1` 启用 b12x 2-tier） | [gemm/marlin.md](gemm/marlin.md)、[decode/current.md](decode/current.md) |
17	| Spec（EAGLE-3 chain，默认 `spec_steps=5 topk=2 dtn=11`，dynamic NO_SPEC/D5/D7） | [eagle/README.md](eagle/README.md) |
18	| Draft（`demo-sala/data/eagle_draft/`，来源 `draft_main` step 6250 / `v3mix_300k_s6250_ind672`） | [eagle/README.md](eagle/README.md) |
19	| ngram routing（提交包默认开启） | [ngram/routing.md](ngram/routing.md) |
20	| MARS verify（D5 θ=0.85，D7 θ=0.5） | [eagle/experiments.md](eagle/experiments.md) §3 |
21	| DFlash + DDTree（**非生产**，备选 spec 算法） | [dflash/](dflash/) |
22	
23	`.so` 替换日志见 [gemm/so-replacements.md](gemm/so-replacements.md)（替换 `.so` 前先备份，CLAUDE.md 硬规则）。
24	
25	## 2. 关键命令
26	
27	```bash
28	bash eval/start_eagle.sh                       # 起 EAGLE-3 生产 server
29	bash bench/kill_sglang.sh                      # 唯一允许的停服方式
30	bash bench/mini_bench.sh                       # 速度速查
31	bash toolkit/bench_serving.sh http://127.0.0.1:30000   # 完整 bench
32	```
33	
34	## 3. Prefill 接续
35	
36	事实来源：[prefill/current.md](prefill/current.md)。
37	
38	- 当前 stage2 sparse FA 走 FlashInfer `BatchPrefillWithPagedKVCacheWrapper`；`--dense-as-sparse` 强制
39	  开启，page_size=1 是算法决定（compress_k 独立 allocator 是中等重构）。
40	- 已落地：layer/chunk plan cache + cross-forward buffer […]

> AGENT

我已经深入阅读了 `/user_4813494d/openbmb/` 工作区的 CLAUDE.md、AGENTS.md 和 docs/handover.md。以下是对你工作的理解：

## 项目定位
**SOAR 比赛工作区** — 优化 OpenBMB/MiniCPM-SALA 推理性能，最终在官方云环境打分。基座模型不可换，改动只能落在：量化、SGLang fork、推测解码 draft、kernel、平台部署脚本。

## 模型架构要点
- 32 层混合：8 standard Attention（layer 0/9/16/17/22/29/30/31）+ 24 Lightning Attention (GLA)
- `hidden=4096`, `intermediate=16384`, `nq/nkv=32/2`, `head_dim=128`，512K 上下文
- **生产默认 `--dense-as-sparse`**，所有 standard Attention 走 sparse 路径（compress_k → stage1 → stage2 top-K FA）

## 运行栈
- 硬件：RTX 6000D（sm_120 Blackwell, 84GB）
- PyTorch 2.11.0+cu130 / CUDA 13.2 / cuDNN 9.21 / FlashInfer 0.6.8.post1[cu13] / Triton 3.6.0
- venv 预激活在 `/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env`

## 当前生产配置
- **量化**：NVFP4（GPTQ + FourOverSix，wikitext 90 样本，`MAX_SEQ_LENGTH=92160`）
- **Decode**：Marlin 全 M（生产默认）；b12x 2-tier 已 lock-in 但默认关闭
- **推测解码**：EAGLE-3 chain verify，`spec_steps=5, topk=2, dtn=11`，dynamic NO_SPEC/D5/D7 切换
- **Draft**：`demo-sala/data/eagle_draft/`（来源 `draft_main` step 6250 / `v3mix_300k_s6250_ind672`）

## 三条主线
| 路径 | 用途 |
|---|---|
| `demo-sala/` | **正式提交包**（平台真正消费），≤2GB |
| `probe-sala-s2/` | 反向 SSH 调试 sidecar（authorized_keys + dropbear/frpc） |
| `eagle/` / `bench/` / `eval/` / `quant/` / `kernels/` | 研发、训练、bench、kernel 实验 |

## 关键红线（已记在脑里）
- **始终简体中文回复**
- **杀 sglang 只用** `bash bench/kill_sglang.sh`（禁 `pkill -f sglang`，会杀系统进程）
- **始终 `uv pip install`**，永不 `pip install`
- 替换 `.so` 必须先备份到 `outputs/so_backups/...` + 写 `docs/gemm/so-replacements.md`
- SGLang 参数连字符风格（`--dense-as-sparse`）
- 不用 argparse，脚本硬编码
- 性能改动先 profile 证明 >1.5× 收益再 e2e bench
- DFlash / DDTree 是**探索路线，非生产**，提交包仍走 EAGLE-3
- 同时只能跑一个 GPU 任务
- Monitor 用 `grep -m1 PATTERN`，pattern […]

> TOOL

tool_use Write
```json
{
  "file_path": "/user_4813494d/.claude/projects/-user_4813494d/memory/MEMORY.md",
  "content": "- [Project: OpenBMB MiniCPM-SALA SOAR](project_openbmb_sala.md) — SOAR 比赛工作区，优化 MiniCPM-SALA 推理，工作目录 /user_4813494d/openbmb\n- [User: SOAR contestant](user_role.md) — 比赛选手，工作集中在量化/SGLang fork/spec decoding/kernel\n- [Feedback: Chinese only](feedback_language.md) — 始终简体中文回复，严禁韩日等其他语言\n- [Feedback: Project ops rules](feedback_openbmb_ops.md) — kill_sglang.sh 唯一停服方式、uv pip、no argparse 等硬规则\n- [Reference: openbmb docs](reference_openbmb_docs.md) — 项目文档位置和入口（CLAUDE.md / AGENTS.md / docs/handover.md）\n"
}
```

> TOOL

tool_result Write
```
File created successfully at: /user_4813494d/.claude/projects/-user_4813494d/memory/MEMORY.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
```json
{
  "file_path": "/user_4813494d/.claude/projects/-user_4813494d/memory/project_openbmb_sala.md",
  "content": "---\nname: project_openbmb_sala\ndescription: SOAR 比赛工作区 /user_4813494d/openbmb，优化 OpenBMB/MiniCPM-SALA 推理，最终在官方云环境打分\nmetadata:\n  type: project\n---\n\n**项目**：SOAR 比赛 — 优化 OpenBMB/MiniCPM-SALA 推理性能，平台云环境打分。基座模型不可换，改动只能落在：量化方案、SGLang fork、推测解码 draft、kernel、平台部署脚本。\n\n**Why**：比赛性质，最终以平台跑分定胜负；提交包 ≤ 2GB。\n\n**How to apply**：\n- 工作目录 `/user_4813494d/openbmb`，提交根 `demo-sala/`，custom SGLang 在 `demo-sala/sglang/python/`\n- 三条主线：`demo-sala/`（正式提交）/ `probe-sala-s2/`（反向 SSH 调试 sidecar）/ `eagle/`+`bench/`+`eval/`（研发实验）\n- 任何\"在本地能跑\"不代表\"提交包能跑\"——必须验 `demo-sala/` 路径\n\n**模型架构**：MiniCPM-SALA，32 层混合（8 standard Attention layer 0/9/16/17/22/29/30/31 + 24 Lightning Attention/GLA），hidden=4096，intermediate=16384，nq/nkv=32/2，head_dim=128，512K 上下文。\n\n**生产配置**：\n- 硬件 RTX 6000D（sm_120 Blackwell, 84GB），PyTorch 2.11.0+cu130 / CUDA 13.2 / cuDNN 9.21 / FlashInfer 0.6.8.post1[cu13]\n- 量化 NVFP4（GPTQ + FourOverSix，wikitext loguniform 90 样本，MAX_SEQ_LENGTH=92160）\n- Decode：Marlin 全 M（b12x 2-tier 已 lock-in 但默认关）\n- Spec：EAGLE-3 chain verify，spec_steps=5/topk=2/dtn=11，dynamic NO_SPEC/D5/D7\n- Draft：`demo-sala/data/eagle_draft/`（来源 `draft_main` step 6250 / `v3mix_300k_s6250_ind672`）\n- Prefill 全 8 层 standard Attention 走 sparse（`--dense-as-sparse` 强开）\n\n**注意**：DFlash + DDTree 是探索路线，**非生产**，提交包仍走 EAGLE-3。相关索引文档参见 [[reference_openbmb_docs]]。\n"
}
```

> TOOL

tool_result Write
```
File created successfully at: /user_4813494d/.claude/projects/-user_4813494d/memory/project_openbmb_sala.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
```json
{
  "file_path": "/user_4813494d/.claude/projects/-user_4813494d/memory/user_role.md",
  "content": "---\nname: user_role\ndescription: 用户是 SOAR 比赛选手，工作集中在 MiniCPM-SALA 推理优化（量化/SGLang fork/spec decoding/CUDA kernel）\nmetadata:\n  type: user\n---\n\n用户是 **SOAR 比赛选手**，深度参与 [[project_openbmb_sala]]。\n\n**技术领域**：\n- 推理引擎 / SGLang fork\n- 量化（NVFP4、GPTQ、FourOverSix、Marlin、CUTLASS）\n- 推测解码（EAGLE-3、Medusa、DFlash/DDTree 备选）\n- CUDA kernel 调优 / sm_120 Blackwell 硬件\n- FlashInfer / cudnn / Triton\n\n**邮箱**：[REDACTED]\n\n**协作偏好**：技术对话非常底层（kernel BW 利用率、sparse FA 路径、CUDA graph、plan cache），可以直接讨论 commit hash、API 形状、寄存器布局等具体细节，无需 hand-holding。\n"
}
```

> TOOL

tool_result Write
```
File created successfully at: /user_4813494d/.claude/projects/-user_4813494d/memory/user_role.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
```json
{
  "file_path": "/user_4813494d/.claude/projects/-user_4813494d/memory/feedback_language.md",
  "content": "---\nname: feedback_language\ndescription: 始终使用简体中文回复，严禁韩日英等其他语言\nmetadata:\n  type: feedback\n---\n\n**始终使用简体中文回复**。严禁使用韩语、日语等其他语言。\n\n**Why**：[[project_openbmb_sala]] 的 CLAUDE.md 顶部硬规则，用户母语为中文。技术术语保留英文（如 NVFP4、Marlin、FlashInfer、EAGLE-3）。\n\n**How to apply**：任何回复（包括 commit message 之外的解释、计划、总结）默认中文；引用代码标识符、文件路径、命令、英文技术名词保留原文。\n"
}
```

> TOOL

tool_result Write
```
File created successfully at: /user_4813494d/.claude/projects/-user_4813494d/memory/feedback_language.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
```json
{
  "file_path": "/user_4813494d/.claude/projects/-user_4813494d/memory/feedback_openbmb_ops.md",
  "content": "---\nname: feedback_openbmb_ops\ndescription: openbmb 工作区的硬性操作规则（停服、安装、so 替换、profile、monitor 等）\nmetadata:\n  type: feedback\n---\n\n[[project_openbmb_sala]] 的硬规则（来自 CLAUDE.md / AGENTS.md），违反会出事：\n\n**停服**：只用 `bash bench/kill_sglang.sh`。**严禁** `pkill -f sglang` / `kill -9` —— 会杀系统进程导致整机重启。\n\n**包管理**：始终 `uv pip install`，永不 `pip install`。`prepare_env.sh` 失败 `exit 1`，禁止 pypi.org / pytorch.org 兜底。llmcompressor 装完后回滚 `compressed-tensors==0.13.0 accelerate==1.13.0`。\n\n**`.so` 替换**：必须先备份到 `outputs/so_backups/<YYYYMMDD-HHMMSS>__<src-name>__<sha256前12>/`（含 meta.json：原路径、md5、sha256、cuobjdump SM、来源 commit），同时在 `docs/gemm/so-replacements.md` 追加一行。**严禁 cp 覆盖未备份的 .so**。\n\n**SGLang 参数**：连字符风格（`--dense-as-sparse`），不是下划线。\n\n**脚本风格**：不用 argparse，配置硬编码为常量。Shell 用 `#!/usr/bin/env bash` + `set -euo pipefail`（source 的脚本例外）。\n\n**性能 / 验证**：\n- 性能改动先 profile 证明 >1.5× 收益，再 e2e bench\n- 单看 tok/s 没意义，必须连同 `ori_accuracy`\n- 正确性冒烟用 chat 请求（说人话即可），不用 mcq、不跑全量 accuracy eval、不用 `/health`\n- Server ready 判断：日志 `Uvicorn running on` 或 curl `/v1/models`\n- \"输出垃圾\"结论前先发 3 条简单 chat（残留长请求或 mcq 退化会伪装成 bug）\n\n**GPU 任务串行**：同时只能跑一个（显存占满）。永远自己启动 server 跑 bench，不给用户\"启动指令\"。\n\n**Monitor**：\n- 必须 `grep -m1 PATTERN` 一次匹配退出\n- 等新事件前 `TaskStop` 旧 monitor\n- 重启 server 前先停旧 monitor（`tail -F` 会跟新文件）\n- pattern 必须覆盖失败路径（`Traceback|ERROR|Killed|OOM`）\n\n**等待**：最多 `sleep 60s` 不轮询；后台任务用 `run_in_background` + 通知。\n\n**禁止预判**：不要估算工作量/工时；不要预判 ROI 当拒绝理由——让 wall 数字说话。\n\n**数据红线**：严禁用 `bench/data/` 做训练/采集/校准（速度评测集，会算作弊）；`toolkit/eval_dataset/` 可以。\n\n**提交**：≤2GB；不提交模型权重/大日志/outputs/；commit message 短祈使（`feat:` / `fix:` / `clean:` / `chore:` / `docs:` / `perf:`）。\n\n**不要随意动当前提交 draft**（`demo-sala/data/eagle_draft/`）；DFlash/DDTree 是探索路线，默认不当作可替换 baseline。\n"
}
```

> TOOL

tool_result Write
```
File created successfully at: /user_4813494d/.claude/projects/-user_4813494d/memory/feedback_openbmb_ops.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
```json
{
  "file_path": "/user_4813494d/.claude/projects/-user_4813494d/memory/reference_openbmb_docs.md",
  "content": "---\nname: reference_openbmb_docs\ndescription: openbmb 工作区的关键文档入口（CLAUDE.md / AGENTS.md / docs/handover.md / 各子主题）\nmetadata:\n  type: reference\n---\n\n[[project_openbmb_sala]] 文档入口：\n\n**根级**：\n- `/user_4813494d/openbmb/CLAUDE.md` — 项目总览、硬规则、栈版本、关键命令\n- `/user_4813494d/openbmb/AGENTS.md` — onboarding，路径分工、定制点、测试验收\n- `/user_4813494d/openbmb/docs/handover.md` — **接续指南**，下个 session 优先读这份\n- `/user_4813494d/openbmb/docs/README.md` — 文档索引\n\n**docs/ 子主题**（统一约定 `current.md` = 当前事实，`history.md` = 调研归档）：\n| 主题 | 路径 |\n|---|---|\n| 平台 / cu13 栈 | `docs/platform/` |\n| 量化 / NVFP4 / FourOverSix | `docs/quant/`（重点 `nvfp4.md`） |\n| sm_120 GEMM / Marlin / kernel 调优 | `docs/gemm/`（`marlin.md`, `so-replacements.md`, `methodology.md`） |\n| 长上下文 prefill | `docs/prefill/` |\n| Decode 派发 / profile | `docs/decode/` |\n| EAGLE-3 spec decoding | `docs/eagle/`（`README.md`, `experiments.md`, `collapse.md`, `large-batch.md`, `main-runbook.md`, `training/pipeline.md`） |\n| ngram routing | `docs/ngram/` |\n| DFlash + DDTree（非生产） | `docs/dflash/` |\n| 周冠军技术分享 blog | `docs/blog/` |\n\n**重要警告**（CLAUDE.md 原文）：文档可能滞后于代码、可能写错。**代码现状与文档冲突时以代码为准**；用 `git log` / 读代码 / 跑 bench 验证后再行动，顺手把文档纠正。\n\n**外部资源**：\n- demo-sala 历史快照 tar：`/user_4813494d/openbmb/*.tar.gz` 与 `/user_4813494d/wzy_tars/`\n- 当前 target model：`/user_4813494d/models/openbmb/MiniCPM-SALA-gptq46-calib90-90k-NVFP4`\n- venv：`/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env`\n- deps repos（cutlass、deepgemm、fast-hadamard-transform、flash-attention、flashinfer、flashmla、mscclpp、triton）：`/user_4813494d/deps/`\n"
}
```

> TOOL

tool_result Write
```
File created successfully at: /user_4813494d/.claude/projects/-user_4813494d/memory/reference_openbmb_docs.md (file state is current in your context — no need to Read it back)
```

> AGENT

理解完毕，关键信息已存到 memory（5 个文件：项目、用户、中文反馈、运维规则、文档索引），下次 session 接续不用重读。

需要我现在动手做什么具体任务？比如：
- 看 `docs/handover.md` 提到的某个接续点（prefill MLP epilogue / b12x 启用 / EAGLE 训练）
- 跑 mini_bench 看当前性能
- 排查某个具体问题