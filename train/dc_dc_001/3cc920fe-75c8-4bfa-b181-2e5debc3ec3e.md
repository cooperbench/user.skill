> DEVELOPER

通读 docs 文档和代码 多委派 subagent 旧文档、冗余文档、文档清理、合并 哪些是不存在的？ 哪些已经在生产中启用了？ 现在文档区太混乱了 请开始做这个工作

> TOOL

tool_use Bash
```json
{
  "command": "ls docs/ && echo \"---\" && cat docs/README.md 2>/dev/null | head -100",
  "description": "List docs directory and read README"
}
```

> TOOL

tool_result Bash
```
README.md
blog
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
# 文档导航

SOAR MiniCPM-SALA 推理优化工作区。项目总览见仓库根 [`CLAUDE.md`](../CLAUDE.md)。

## 接续

| 文档 | 内容 |
|---|---|
| [handover.md](handover.md) | **新 session 接续指南**（红线、当前栈、prefill / decode / eagle 状态、下一步候选） |

## 主题

每个主题一个子目录，目录下有 `README.md` 索引 + 各子文档。

| 主题 | 内容 |
|---|---|
| [platform/](platform/) | 平台、cu13 栈、probe-sala 部署、SGLang fork 升级判定 |
| [quant/](quant/) | NVFP4 量化方案（GPTQ + FourOverSix + 校准） |
| [gemm/](gemm/) | sm_120 GEMM/kernel 底层调优（CUTLASS / Marlin / 硬件 / profile 方法论 / `.so` 替换日志） |
| [prefill/](prefill/) | 长上下文 prefill：当前事实 + 历史调研 + 已枯竭路线 |
| [decode/](decode/) | Decode 算子优化：当前 SOP + profile 方法论 + 误归因教训 |
| [eagle/](eagle/) | EAGLE-3 spec decoding：架构 / 适配 / 训练 / collapse / 实验 / 论文 |
| [ngram/](ngram/) | request-local ngram lookup：probe / EAGLE routing / CUDA graph 稳定性修复 |
| [dflash/](dflash/) | DFlash + DDTree spec decoding：block diffusion draft + best-first heap tree verify |
| [blog/](blog/) | 每周对外分享（SOAR 周冠军技术分享） |

## 快速定位

| 想了解… | 入口 |
|---|---|
| 当前生产配置速览 | [handover.md](handover.md) §1 |
| cu13 升级要点 + 回滚 | [platform/cu13-stack.md](platform/cu13-stack.md) §3 |
| `220c18cc` vs `32d27c7` `.so` 与 EAGLE 兼容性警告 | [gemm/marlin.md](gemm/marlin.md) §6 |
| NVFP4 KV 为何不可用 | [quant/nvfp4.md](quant/nvfp4.md) §4 |
| prefill 当前热点 | [prefill/current.md](prefill/current.md) §1 |
| decode profile 方法论（**重要避坑**） | [decode/current.md](decode/current.md) §3 |
| 当前 prod draft（v2mix_20k_s3500_ood757） | [eagle/prod.md](eagle/prod.md) |
| ngram routing 当前实现 | [ngram/routing.md](ngram/routing.md) |
| collapse 根因 | [eagle/collapse.md](eagle/collapse.md) §1 |
| 已落产实验（rope_theta=1M / MARS θ=0.85） | [eagle/experiments.md](eagle/experiments.md) |
| DFlash / DDTree 当前状态（启动入口、accept rate） | [dflash/current.md](dflash/current.md) §1 |
| DDTree 输出乱码根因（FlashInfer custom_mask 数值漂移） | [dflash/ddtree.md](dflash/ddtree.md) §2 |
| SGLang 主线 DFlash skip custom_mask policy（关键参考） | [dflash/integration.md](dflash/integration.md) §3 |

## 惯例

- 速度结论（e2e bench 秒级数字）不写进文档，随时可过期。需要数据时直接跑 `bench/mini_bench.sh`
- 文档记录**可复现的方法**和**已验证的决策**，不记录瞬时测速结果
- 负结果必须保留，防止重踩
- `current.md` = 当前事实；`history.md` = 已枯竭路线 + 调查教训。新实验追加到 `eagle/experiments.md`
- 跨目录引用用 `../<topic>/<file>.md`，同目录用文件名
```

> TOOL

tool_use Bash
```json
{
  "command": "find docs/ -type f -name \"*.md\" | sort",
  "description": "List all markdown files in docs"
}
```

> TOOL

tool_result Bash
```
docs/README.md
docs/blog/.ipynb_checkpoints/week9-checkpoint.md
docs/blog/README.md
docs/blog/week7.md
docs/blog/week8.md
docs/blog/week9.md
docs/decode/README.md
docs/decode/current.md
docs/decode/history.md
docs/dflash/README.md
docs/dflash/current.md
docs/dflash/ddtree.md
docs/dflash/history.md
docs/dflash/integration.md
docs/eagle/300k-training-plan.md
docs/eagle/README.md
docs/eagle/architecture.md
docs/eagle/collapse.md
docs/eagle/d7-tune-bench-20260511.md
docs/eagle/dflash.md
docs/eagle/experiments.md
docs/eagle/large-batch.md
docs/eagle/papers.md
docs/eagle/prod.md
docs/eagle/runtime-deep.md
docs/eagle/spec-v2.md
docs/eagle/training/README.md
docs/eagle/training/data-compression.md
docs/eagle/training/history.md
docs/eagle/training/pipeline.md
docs/gemm/README.md
docs/gemm/bottleneck_cards/01_o_proj_std_M48.md
docs/gemm/bottleneck_cards/02_down_proj_M128.md
docs/gemm/changelog.md
docs/gemm/charter.md
docs/gemm/current.md
docs/gemm/dead-ends.md
docs/gemm/hardware.md
docs/gemm/kernels-sm120.md
docs/gemm/marlin.md
docs/gemm/methodology.md
docs/gemm/roadmap.md
docs/gemm/so-replacements.md
docs/gemm/sol_table.md
docs/gemm/todo.md
docs/handover.md
docs/ngram/README.md
docs/ngram/probe.md
docs/ngram/routing.md
docs/platform/README.md
docs/platform/cu13-stack.md
docs/platform/eval-vs-dev-environment-audit.md
docs/platform/trtllm-utils-aot-fix.md
docs/prefill/README.md
docs/prefill/current.md
docs/prefill/history.md
docs/quant/README.md
docs/quant/nvfp4.md
```

> TOOL

tool_use Bash
```json
{
  "command": "wc -l docs/**/*.md docs/*.md 2>/dev/null | tail -1 && echo \"---\" && find docs -type f -name \"*.md\" -printf \"%s %p\\n\" | sort -rn | head -30",
  "description": "Total line count and largest files"
}
```

> TOOL

tool_result Bash
```
10867 total
---
73706 docs/gemm/changelog.md
46384 docs/eagle/papers.md
28416 docs/prefill/current.md
28204 docs/gemm/methodology.md
22916 docs/gemm/dead-ends.md
22422 docs/gemm/kernels-sm120.md
21854 docs/eagle/runtime-deep.md
17557 docs/decode/history.md
17454 docs/eagle/collapse.md
16420 docs/prefill/history.md
14386 docs/eagle/300k-training-plan.md
14245 docs/eagle/experiments.md
13662 docs/gemm/sol_table.md
13580 docs/gemm/todo.md
12511 docs/gemm/current.md
12435 docs/gemm/marlin.md
11963 docs/platform/eval-vs-dev-environment-audit.md
11466 docs/eagle/training/pipeline.md
11422 docs/decode/current.md
11411 docs/handover.md
11351 docs/platform/cu13-stack.md
10263 docs/ngram/probe.md
9931 docs/gemm/charter.md
9140 docs/eagle/dflash.md
8997 docs/eagle/large-batch.md
8573 docs/platform/trtllm-utils-aot-fix.md
8508 docs/eagle/spec-v2.md
8376 docs/quant/nvfp4.md
8212 docs/dflash/ddtree.md
7884 docs/gemm/so-replacements.md
```

> AGENT

我来做文档清理调研。先并行委派多个 subagent 调查各主题，每个 agent 同时阅读该主题的所有文档并对比代码现状，识别幻影/陈旧/冗余文档。

> TOOL

tool_use Agent
```json
{
  "description": "platform docs audit",
  "subagent_type": "Explore",
  "prompt": "背景：你在 /user_4813494d/openbmb（SOAR MiniCPM-SALA 推理优化工作区）。先读 /user_4813494d/openbmb/CLAUDE.md 了解当前生产配置（NVFP4 + 自定义 SGLang + EAGLE-3 + b12x decode kernel）。\n\n任务：审计 docs/platform/ 目录和 docs/handover.md 这两个文档，对比代码现状，识别需要清理的内容。\n\n需要审计的文档：\n- docs/handover.md\n- docs/platform/README.md\n- docs/platform/cu13-stack.md\n- docs/platform/eval-vs-dev-environment-audit.md\n- docs/platform/trtllm-utils-aot-fix.md\n\n对每个文档分析（用 grep / Read 实际验证）：\n1. **Phantom（幻影）**：文档提到的脚本/路径/.so/函数在代码里是否还存在？比如 `prepare_env.sh`、`probe-sala/` 内文件、`common_ops.abi3.so` 替换等\n2. **Stale（陈旧）**：文档把某事描述为\"调研中/待验证\"，但 git log 或代码显示已落产 / 已被否决\n3. **Redundant（冗余）**：和 handover.md 或 CLAUDE.md 是否重复？和其他文档重叠多少？\n4. **trtllm-utils-aot-fix 是不是一次性故障记录？** 是否还有意义？\n\nhandover.md 是项目接续指南，需要特别检查它和 CLAUDE.md 之间是否重复了配置信息，以及它的 \"下一步候选\" 部分是不是已经过时。\n\n报告格式（中文，每个文档一节）：\n- 文件路径\n- 当前状态判定：保留 / 重写 / 合并到 X / 删除\n- 具体证据（grep / 代码引用 / git log）\n- 如果建议合并，目标是哪个文档\n\n最后给一个简短的总建议（< 200 字）：platform 这块整体应该怎么整理。"
}
```

> TOOL

tool_result Agent
```
现在整理最终的审计结果。根据我的分析，我来生成审计报告。

---

## 文档审计报告

### 1. docs/handover.md

**文件路径**：`/user_4813494d/openbmb/docs/handover.md`

**当前状态判定**：**重写** （需要版本清理和陈旧内容修剪）

**具体证据**：

- **重复**：约 60-70% 内容与 `CLAUDE.md` 重复。两份都列举相同的硬件配置、栈版本（PyTorch 2.11.0+cu130、CUDA 13.2、FlashInfer 0.6.8.post1 等）、量化方案、Decode dispatch、EAGLE-3 生产参数。表格几乎逐行对应。

- **陈旧**："§7. probe-sala 平台部署（已退役）" 标注"大部分文件已删除"，但 §4 仍长篇幅讲 probe-sala 部署流水；`git log -- probe-sala/` 显示最后清理在 `b74c10d (chore: prune probe-sala stale tree)`。handover.md 未及时清理。

- **已落实但标记为"候选"**："§4 当前下一步候选" 列举 5 项，但 CLAUDE.md 明确说"prefill 当前状态：保留 plan cache...已落产...得"（见 §104-109），这些"候选"部分已落产（padded sparse-K、MARS 顶级都已实装，见 `git log`）。

- **DFlash/DDTree 备选算法内容过重**：§5b 占 18 行（共 190 行），定位为"备选"，但 CLAUDE.md 明确指"**不作为生产实践**"。当下两份都持相同观点，但 handover.md 文字量不匹配定位。

**合并目标**：删除重复的栈信息块，保留仅有的"下一步"实质内容，指向各子文档（已有）。或改为"快速启动卡"仅保留关键命令和红线，将配置表完全删除（让 CLAUDE.md 单一真实来源）。

---

### 2. docs/platform/README.md

**文件路径**：`/user_4813494d/openbmb/docs/platform/README.md`

**当前状态判定**：**保留** （已正确实现导航职责）

**具体证据**：

- 仅 13 行，纯索引。准确列举了三份子文档及职责范围。
- 未发现重复、陈旧或虚幻内容。
- 与 `docs/README.md` 中的 `[platform/]` 条目完全一致，无额外信息。

**结论**：这是合规的索引文件，无需改动。

---

### 3. docs/platform/cu13-stack.md

**文件路径**：`/user_4813494d/openbmb/docs/platform/cu13-stack.md`

**当前状态判定**：**保留，但合并 probe-sala 部分至 git history** （§4 应转档）

**具体证据**：

- **核心内容仍然有效**：§1 栈版本表、§3 cu12→cu13 升级要点、§5 SGLang fork 升级判定、§6 sm_120 NVFP4 生态都是时效性信息，CLAUDE.md 中 cu13 升级日期（2026-04-20）与本文档对齐。

- **phantom：probe-sala 流水已退役**：§4 "probe-sala 提交包流水" 占 40 行，讲 BOS 鉴权、cu12 purge、flashinfer AOT skip JIT、verify_env.py 11 项检查。但：
  - handover.md §7 注记："2026-05-08，probe-sala 在当前分支大部分文件已删除"
  - `git log` 确认 `b74c10d (chore: prune probe-sala stale tree)` 在 cu13 升级后
  - 代码中 `probe-sala/` 目录已空或仅有 symlink（§1 ls 输出无 probe-sala，只有 probe-sala-s2 等特化版本）
  - 只有 `probe-sala-s2/` (ad-hoc SSH 调试包) 还活跃，且不与提交流程关联

- **冗余**：§4.2 11 项 verify 与 `demo-sala/verify_env.py` 代码一致，但 cu13-stack.md 文字描述不如代码源真实。应删除文字版本，指向代码。

**建议**：
- 删除 §4 整节（40 行），替换为："probe-sala 已退役（见 git history b74c10d）；当前流程统一用 `demo-sala/prepare_env.sh`。"
- §1 保留；§3、§5、§6 保留（有时效价值）。
- 若需要 probe-sala 历史，在 git commit message 中已有记录。

---

### 4. docs/platform/eval-vs-dev-environment-audit.md

**文件路径**：`/user_4813494d/openbmb/docs/platform/eval-vs-dev-environment-audit.md`

**当前状态判定**：**保留** （一次性深度审计记录，不重复）

**具体证据**：

- 266 行，28 节详细对比（ulimit、swap、CUDA 路径、pip 包版本、K8s pod 特征）。
- 此文档专门针对"本地通过、云端崩"问题的根因分析，无其他文档覆盖此范围。
- handover.md 未提及。CLAUDE.md 未覆盖。
- 审计日期 2026-05-11，靠近当前（仍有效）；§6 提供重跑审计的完整脚本和方法，可复现。
- 核心发现（`/usr/local/cuda` 缺失、ulimit -n=1024、swap=0）已集成到 cu13-stack.md 的 trtllm-utils-aot-fix 修复流程。

**结论**：保留原样。这是参考档案，对诊断"eval vs dev 不一致"问题必须。

---

### 5. docs/platform/trtllm-utils-aot-fix.md

**文件路径**：`/user_4813494d/openbmb/docs/platform/trtllm-utils-aot-fix.md`

**当前状态判定**：**保留，附注"已落地"** （故障记录 + 修复方法论）

**具体证据**：

- 200 行，记录"平台启 sglang 后 flashinfer autotune skip 6 tactic"故障的根因（`/usr/local/cuda` 缺失 → JIT build 失败）、修复（AOT 预建 `trtllm_utils.so`）、诊断工具链。
- 落地日 2026-05-11（见文件首行）；§3 修复已在 `demo-sala/prepare_env.sh` G4b 阶段实现（无代码改动，仅文件复制）。
- 核心诊断工具仍有价值：
  - §5.1 反向 SSH 调试方法（dropbear + frpc 工具链）用于 K8s pod 现场诊断
  - §5.2 `FLASHINFER_LOGGING_LEVEL=debug` 诊断方法（future 故障排查必用）
  - §5.3 最小复现脚本（可复现 skip 现象）

- **陈旧度**：故障本身已解决（cu13 栈稳定后无新报告），但诊断方法论和工具链仍是"如何快速定位平台 JIT 故障"的标杆。未来任何类似问题应该参考本文。

**建议**：保留，但在文件顶添加注记："本故障已修复并落地至 prepare_env.sh §2.1 Stage 3 G4b（2026-05-11）。本文保留诊断方法论供参考。"

---

## 综合建议（< 200 字）

**Platform 文档整理方案**：

1. **handover.md**：删除 §1-2（栈配置表、下一步候选中已落实部分）、§7（probe-sala 已退役）。改为 2-3 页的"快速启动卡"：仅保留红线、关键命令、当前生产参数表（浓缩为一张表指向各子文档）。让 CLAUDE.md 成为唯一的栈配置源。

2. **platform/cu13-stack.md**：删除 §4（probe-sala），保留 §1/3/5/6。§3 升级要点标注"已完成（2026-04-20），下次升级时参考"。

3. **platform/eval-vs-dev-environment-audit.md**：保留原样，作为诊断档案库。

4. **platform/trtllm-utils-aot-fix.md**：保留，添加"已落地"标注。

5. **docs/README.md**：已正确，无需改动。

**清理量**：删除 ~60 行（handover.md 表格重复 + probe-sala 段落）+ 添加 2 行注记 = 净化 7-8%。保留所有核心决策记录、诊断方法论、参考档案。
```

> TOOL

tool_use Agent
```json
{
  "description": "quant docs audit",
  "subagent_type": "Explore",
  "prompt": "背景：你在 /user_4813494d/openbmb（SOAR MiniCPM-SALA 推理优化工作区）。先读 /user_4813494d/openbmb/CLAUDE.md 了解当前生产配置：NVFP4（GPTQ + FourOverSix，loguniform128 校准，48K 上下文）。\n\n任务：审计 docs/quant/ 目录，对比 quant/ 代码和 demo-sala/prepare_model.sh，识别清理点。\n\n需要审计的文档：\n- docs/quant/README.md\n- docs/quant/nvfp4.md\n\n对每个文档分析（用 grep / Read 实际验证）：\n1. **当前生产量化方案是否在文档中清楚体现？** 文档提到的 calibration / 校准集 / 量化参数与 demo-sala/prepare_model.sh 是否一致？\n2. **Phantom**：文档提到的脚本（如 GPTQ runner、FourOverSix patch）在 quant/ 下是否存在？\n3. **历史/失败方案**：文档是否清楚标注了\"为什么 NVFP4 KV 不能用\"等负结果？还需要保留吗？\n4. **和 demo-sala 的官方流程是否冲突？** CLAUDE.md 说 demo-sala/README.md 是生产基线。\n\n请用 ls quant/ 和 ls demo-sala/ 看看实际代码。\n\n报告格式（中文）：\n- 每个文档一节：保留 / 重写 / 合并 / 删除 + 证据\n- 总建议（< 150 字）"
}
```

> TOOL

tool_result Agent
```
完美。现在我有足够的信息。让我编制最终报告。

---

## 审计报告：docs/quant/ 文档与生产代码对标

### 1. docs/quant/README.md

**评估**：**保留** ✓

**证据**：
- 文档结构清晰，交叉引用指向 nvfp4.md 和 `../gemm/marlin.md` 均正确
- 无 Phantom 问题：文档提到的脚本和补丁均在实际代码中存在
  - FourOverSix patch：`demo-sala/patches/gptq_quantize_fouroversix.py` ✓
  - Marlin 记录：`docs/gemm/marlin.md` ✓
- 未提及已失效的 KV 量化细节，总体保持高层次导航角色

**建议**：无需修改。

---

### 2. docs/quant/nvfp4.md

**评估**：**重写关键部分** ⚠️

**问题清单**：

| 行号 | 问题 | 证据 | 优先级 |
|------|------|------|--------|
| 9 | **上下文标记错误**：文档说"48K"，实际生产 92160（90K） | `demo-sala/preprocess_model.py:33 MAX_SEQ_LENGTH=92160`；`prepare_model.sh:32,45` 明确"90K" | 🔴 高 |
| 17-20 | **校准表格混淆**：行标注"calib90 (eval mix) 24K"，但实际是 loguniform 128/92160 | 表格标题"baseline"指早期失败案例，非当前生产 | 🟡 中 |
| 126-130 | **Phantom bench 脚本**：引用 `bench/bench_nvfp4_kv_decode.py` 等三个脚本，均不存在 | `ls /user_4813494d/openbmb/bench/bench_nvfp4*.py` 返回 error | 🔴 高 |
| 45 | **prepare_model.sh 用法陈述**：未明确说明此脚本仅用于本地验证，生产走 demo-sala | 可接受（demo-sala/README.md 已澄清） | 🟢 低 |

**具体修改建议**：

1. **第 9 行**：改为"上下文 | 92160（90K）"，或明确"校准时 48K/验证时 92160（详见 §1.1）"

2. **第 8 行与校准表格（13-20 行）**：增加说明：
   ```
   校准数据：loguniform128 (wikitext)，92160 tokens max_length
   （历史对比行保留作反例，标注"已放弃"）
   ```

3. **§4.4 microbench 节（124-130 行）**：删除对不存在脚本的引用，改为：
   ```
   ❌ 已删除的 bench 脚本（quant/archive/ 有历史版本）：
   - bench_nvfp4_kv_decode.py
   - bench_nvfp4_sparse_decode_triton.py  
   - bench_variable_block_sparse_wrapper.py
   
   结论不变（KV 量化 ROI 不足），但验证脚本已归档，不可直接运行。
   ```

---

### 总建议（<150 字）

**demo-sala/preprocess_model.py 是当前生产基线**，文档应完全对标。核心问题：（1）上下文标记 48K vs 92160 不一致——需改为 92160 或标注校准/推理阶段差异；（2）三个 bench 脚本已删除——删除引用或改为归档说明。quant/calib90 和 quant/gptq_nvfp4.py 为本地开发工具，可保留但明确标注为"参考实现"，生产唯一基线是 demo-sala/。建议在 docs/quant/README.md 顶部加一行：**当前生产流程详见 demo-sala/README.md，本目录为技术档案。**
```

> TOOL

tool_use Agent
```json
{
  "description": "gemm docs audit",
  "subagent_type": "Explore",
  "prompt": "背景：你在 /user_4813494d/openbmb（SOAR MiniCPM-SALA 推理优化工作区）。先读 /user_4813494d/openbmb/CLAUDE.md 了解当前生产配置：Decode kernel 派发 = b12x 2-tier（Marlin小M / b12x全M / 3点CUTLASS override），覆盖 6 形状 58 tile 配置。\n\n任务：审计 docs/gemm/ 目录（13 个文件 ~24K 行，整个 docs 体量的一半），对比代码（kernels/ 和 demo-sala/sglang/python/），识别清理点。这是最大最复杂的子目录，请彻底调查。\n\n需要审计的文档（每个都读，至少前 150 行 + 跳读关键段）：\n- docs/gemm/README.md\n- docs/gemm/charter.md\n- docs/gemm/current.md（事实快照）\n- docs/gemm/changelog.md（最大文件，~73KB）\n- docs/gemm/methodology.md\n- docs/gemm/dead-ends.md\n- docs/gemm/kernels-sm120.md\n- docs/gemm/marlin.md\n- docs/gemm/hardware.md\n- docs/gemm/sol_table.md\n- docs/gemm/roadmap.md\n- docs/gemm/todo.md\n- docs/gemm/so-replacements.md（替换日志，必须保留）\n- docs/gemm/bottleneck_cards/01_o_proj_std_M48.md\n- docs/gemm/bottleneck_cards/02_down_proj_M128.md\n\n调查重点：\n1. **changelog.md** 是不是一直在追加的滚动日志，已经过时了？应该截断还是保留？\n2. **roadmap.md / todo.md** 中列的待办是否已经做完？比如 b12x 已生产，相关 TODO 是否还有效？\n3. **dead-ends.md** 中的死路条目和 **changelog** 是否重复？\n4. **sol_table.md / hardware.md / kernels-sm120.md** 之间是否有重叠（都是 sm_120 硬件/SoL 信息）？\n5. **charter.md** 是项目章程吗？是不是和 current.md 重复？\n6. **methodology.md** 是 profile 方法论，是否和 decode/current.md §3 重复？\n7. **bottleneck_cards** 是不是只有 2 张就停了的烂尾？\n8. **Phantom**：文档提到的 kernel（CUTLASS configs、Marlin variants）现在 kernels/ 或 sgl-kernel `.so` 里实际部署的是哪些？哪些是探索失败弃用了的？\n\n可以用 `git log --oneline -- docs/gemm/` 看修改时间，识别长期不动的死文件。\n\n报告格式（中文）：\n- 每个文档一节：保留 / 截断 / 重写 / 合并 / 删除 + 证据 + 最近修改时间\n- 总建议（< 300 字）：gemm 这块应该收敛到几个文件，建议的最终结构\n\n报告整体可以超过 200 字，因为 gemm 是大头，但要紧凑、有证据。"
}
```

> TOOL

tool_result Agent
```
现在总结审计结果。我已经读完所有关键文件。生成报告：

## 审计报告：docs/gemm/ 目录清理建议

### 各文档评估

#### 1. **README.md** — **保留，更新结构表**
- **现状**：目录导航 + 速查表 + SOP 进度表
- **问题**：§3 SOP 状态表标注已过期（§0 未缺，§1 有 hardware.md，§3 有 sol_table.md，§4-6 各部分阶段已推进），需同步 2026-05-20 的实际进度
- **建议**：保留，同步更新 SOP 状态表反映最新进展（Tier 1.0 b12x lock-in、R-marlin-fp32reduce rejected 等）
- **最近修改**：2026-05-10（相对新）

#### 2. **charter.md** — **保留**
- **现状**：Stage 0 项目入场合同，定义 6 形状、9 档 M 值、成功度量、约束
- **与 current.md 关系**：互补，charter 是设计阶段承诺，current 是事实快照
- **质量**：完整、规范、仍被引用（r-b12x-acc-fix 验证对照 charter §6）
- **最近修改**：2026-05-01（稳定）

#### 3. **current.md** — **保留但标注过时章节**
- **现状**：生产 .so、dequant bug、CUTLASS 版本差、已 resolved 验证项
- **问题**：
  - § 2.1 "max warps/SM = 待实测"已 resolved（hardware.md 确认 48），应删
  - § 5.3 已 resolved 的 sm_120 max warps/SM 条目冗余
  - § 6 关键文件路径需更新（去 sgl-kernel 改 flashinfer）
- **建议**：保留 § 1-4（事实快照有价值），删/归档 § 5（已 resolved）的冗余
- **最近修改**：2026-05-10（活跃）

#### 4. **methodology.md** — **保留，补完 Stage 3.5 细节**
- **现状**：SOP 契约 + 14 常数表 + roofline + M regime + quick_validate 定义
- **问题**：§3.5 quick_validate 给出了完整定义，但与 charter.md §3.1 度量定义有细节差异（charter 给的是历史基线数字，methodology 给的是协议），需对齐说明
- **建议**：保留全部内容，在 §3.5 前加一行："本节取代 charter.md §3.1 的旧 mini_bench baseline，R3 起唯一闸门"
- **最近修改**：2026-05-10（活跃）

#### 5. **changelog.md**（~73KB，1338 行）— **截断 + 归档**
- **现状**：R1-R-b12x-tune-v2 共 ~28 轮，从 2026-05-09 23:50 开始追加
- **问题**：
  - 73 KB 大文件，内容是实验日志流水账（每轮假设→预期→实测→解释）
  - **但最新内容是决策性的**（R-b12x lock-in、R-marlin-fp32reduce rejected、R-b12x-bucket64 rejected 等需保留作为 dead-ends 证据）
  - 早期轮次（R1-R3 dispatch profiler）的具体数字 (M=48→49 的 37 µs 跳台阶、per-shape threshold 搜索) 已被后续 lock-in 替代
- **建议**：
  - **保留最新 5 轮**（R-b12x 及以后的 lock-in + rejected 决策）原文
  - **早期轮次（R1-R7）归档到 `docs/gemm/archive/changelog-r1-r7.md`** 存历史研究档
  - **新增 `docs/gemm/changelog-decisions.md`** 仅列 lock-in/rejected 的决策摘要 + 时间戳（便于快速查为什么弃了某方向）
- **最近修改**：2026-05-20（最新）

#### 6. **dead-ends.md** — **保留 + 补充索引**
- **现状**：失败模式 catalog（§A-§I），每条标死因 + 实证来源 + 拒绝规则
- **与 changelog 关系**：changelog 详细记录某轮为何失败，dead-ends 拿其中通用教训作硬规则
- **问题**：
  - dead-ends.md §B 的"PingPong dense NVFP4"、"REG=168"等条目与 current.md 重复
  - 新增条目（§M b12x 精度、§N sgl-kernel 版本错位）是 2026-05-10 后补，应确认 changelog 对应已归档
- **建议**：保留全部，但在 README.md 补索引（"哪个 dead-end 来自哪轮 changelog 的证据"）
- **最近修改**：2026-05-10（稳定）

#### 7. **hardware.md** — **保留**
- **现状**：14 常数实测 + 三约束公式 + sm_120 已知坑
- **质量**：完整、有实测出处、符合 methodology 第 1 阶段要求
- **最近修改**：2026-05-01（稳定）

#### 8. **sol_table.md** — **保留 + 标注校准来源**
- **现状**：54 行 (shape, M) 物理下限 + AI + regime 分析
- **问题**：
  - §0 算法用 BW_HBM=1.4 TB/s（保守），但 bottleneck_cards/01 已验证 o_proj L2-bound，需更新说明
  - 无"实测 vs 预测"对比列（只有物理下限）
- **建议**：保留，但补充一列"当前生产 baseline 实测 µs"（来自 baseline_<date>.md），对比 T_kernel_LB 生成 SOL% 实时追踪表
- **最近修改**：2026-05-01（可能需要校准）

#### 9. **marlin.md** — **保留 + 删除已过期章节**
- **现状**：Marlin/b12x 调优记录 + SASS 分析 + 历史 tile sweep + b12x 放弃原因
- **问题**：
  - § 4 "b12x 已放弃"的原因描述有矛盾（2026-05-04 说精度退化，2026-05-10 说 bit-exact，2026-05-10 后又说 lock-in +28.5%）
  - 应清晰标注"2026-05-10 更新：b12x 已平反并 lock-in"
- **建议**：保留 § 1-3 + § 5（已落地优化），§ 4 改为指向 changelog R-b12x 最终决议，§ 6 更新指向当前版本
- **最近修改**：2026-05-10（活跃但有冲突叙述）

#### 10. **kernels-sm120.md** — **保留 + 删除重复内容**
- **现状**：sm_120 NVFP4 peak 实测 1467 TFLOPS + 各库对比 + tile 空间约束 + ROI 排序
- **问题**：
  - § 1 结论速览与 README.md §1 速查重复
  - § 7.4 "b12x 历史记录"与 marlin.md § 4 重复
- **建议**：保留核心（§ 2-5 硬件 peak + tile 约束），§ 1 缩短为指向 README；§ 7.4 删除或指向 marlin.md
- **最近修改**：2026-05-01（较稳定）

#### 11. **sol_table.md**（见上） + **roadmap.md** — **保留 + 更新执行顺序表**
- **roadmap.md 现状**：攻击优先级原则 + 候选清单（6 问）+ SOP template + Stage 5 流程
- **问题**：
  - § 三（候选清单）中列的 Numerics/Mainloop/Pipeline 候选与 todo.md 某些条目描述不一致
  - "3 个停止信号"需与当前 lock-in 对标（b12x 已 lock，部分 R-xxx 已 rejected）
- **建议**：保留全部，但补充"截至 2026-05-20 执行状态"的对标表
- **最近修改**：2026-05-10（相对新）

#### 12. **todo.md** — **重写为 Tier 清单**
- **现状**：顶层 ROI 排序的待办 + 已放弃方向 + 执行顺序 + 4 tier
- **问题**：
  - § 0 已放弃方向与 dead-ends.md 有重叠（"b12x backend""Cluster>1"等）
  - § 4 执行顺序表与 changelog 最新进度有脱节（R-b12x 已 lock，R10/R11 已确认死路，但表中仍当"待"）
- **建议**：
  - **重构为 Tier 2026-05-20 版**：贵司已 lock R7 + R9 + R-b12x，应更新反映
  - 删 § 0 已确认死路（指向 dead-ends.md），§ 4 更新状态为 ✅/❌/⏳
  - 保留 § 1 Tier 1（EVT 融合、CUTLASS 升级）待做清单，强调对象从 sgl-kernel 转移到 flashinfer
- **最近修改**：2026-05-10（待同步）

#### 13. **so-replacements.md** — **必须保留**
- **现状**：.so 替换日志 + 备份目录索引 + 回滚手册 + 历史哈希
- **重要性**：CLAUDE.md 硬要求（"严禁 cp 覆盖未备份的 .so"），是工程规范档
- **最近修改**：2026-05-20（最新，5/17 InfLLM-v2 回滚记录已追加）
- **建议**：保留全部，无改动

#### 14. **bottleneck_cards/** — **完成剩余卡片或转档**
- **现状**：2 张卡片（01_o_proj_std_M48、02_down_proj_M128），仅覆盖 6 形状 × 9 M = 54 组中的 2 个
- **问题**：
  - 应有 54 张但只有 2 张，明显烂尾
  - 每张卡片对应 methodology 的 Stage 4，当前 Stage 5 已进行多轮但无新卡片产生
- **建议**：
  - **标记为"Sample"而非完整集合**：改名为 `bottleneck_card_samples/`（有序号的 01/02 暗示有更多）
  - **补充 `bottleneck_card_template.md`** 说明写法（给未来开发者参考）
  - **现有 2 张保留**（描述了 Marlin dispatch、cost model 校准的关键假设，有学习价值）

---

### 总体结构建议（精简方案）

**目标**：保持信息完整度，同时去掉 800KB+ 的冗余和混乱。

```
docs/gemm/
├── README.md                      ← 导航 + SOP 进度表（同步 2026-05-20）
├── charter.md                     ← Stage 0 合同（保留）
├── methodology.md                 ← SOP 协议（保留 + 补充说明）
├── hardware.md                    ← Stage 1 常数表（保留）
├── sol_table.md                   ← Stage 2 物理下限（保留 + 补实测对标）
├── current.md                     ← 事实快照（删 § 5 过期验证，删 § 6 路径）
├── dead-ends.md                   ← 失败 catalog（保留 + 索引化）
├── roadmap.md                     ← 攻击优先级（保留）
├── marlin.md                      ← Marlin/b12x 历史（删 § 4 冗余，指向 changelog）
├── kernels-sm120.md               ← sm_120 peak 对比（删 § 1/7.4 冗余）
├── changelog-decisions.md         ← 新增：lock-in/rejected 决策摘要（快速查）
├── todo.md                        ← 重写为 Tier 2026-05-20 版（同步 R7/R9/R-b12x）
├── so-replacements.md             ← .so 备份日志（保留，必要工程档）
│
├── archive/                       ← 新增目录
│   ├── changelog-r1-r7.md         ← 早期轮次详细日志（研究档）
│   ├── baseline_2026-05-10.md     ← 历史 baseline（参考）
│   └── ...
│
├── bottleneck_card_samples/       ← 改名（从 bottleneck_cards）
│   ├── 01_o_proj_std_M48.md       ← 保留
│   ├── 02_down_proj_M128.md       ← 保留
│   └── TEMPLATE.md                ← 新增：卡片写法示例
└── validation_samples/            ← 新增？（待补 Stage 6 样例）
```

---

### 具体清理动作

| 文件 | 动作 | 理由 | 预计工作量 |
|---|---|---|---|
| README.md | 更新 § 2/3 | SOP 进度表过期 | 30 min |
| charter.md | 保留 | 是契约档，仍活跃 | — |
| current.md | 删 § 5-6，补 § 1 说明 | § 5 已 resolved，§ 6 路径变更 | 30 min |
| methodology.md | 补充 § 3.5 说明 | 对齐 charter §3.1 差异 | 15 min |
| changelog.md | 归档 R1-R7 到 archive/ | 保留决策轮，压缩早期流水 | 30 min |
| dead-ends.md | 保留 + 编号索引 | 无变更，加索引便于查证 | 15 min |
| hardware.md | 保留 | 稳定 | — |
| sol_table.md | 补实测对标列 | 加强与当前 baseline 对应 | 45 min |
| marlin.md | 删 § 4.1-4.2，指向 changelog | b12x 决议在 changelog 更清晰 | 30 min |
| kernels-sm120.md | 删 § 1 + § 7.4 重复 | 内容指向 README + marlin.md | 20 min |
| roadmap.md | 补执行状态对标表 | 同步 R7/R9/R-b12x 现状 | 30 min |
| todo.md | **重写 Tier 清单** | 最老旧，需全面更新 | **2 小时** |
| so-replacements.md | 保留 | 工程规范档，不动 | — |
| bottleneck_cards/ | 改名为 `bottleneck_card_samples/` | 暗示完整性但实际烂尾 | 10 min |
| **新建** changelog-decisions.md | 写摘要（lock-in/rejected）| 决策快速查 | 1 小时 |
| **新建** archive/ | 迁移早期 changelog | 保留历史研究价值 | — |

**总工作量**：~5.5 小时（主要 todo.md 重写）

---

### 关键发现（Phantom Kernel 问卷）

| 问题 | 答案 | 出处 |
|---|---|---|
| **当前生产 kernel 是哪些**？ | b12x 2-tier (Marlin ≤48 + b12x >48 + 3点CUTLASS override)，Decode +28.5% lock-in | changelog R-b12x, current.md § 头 |
| **CUTLASS/Marlin variant 有多少个**？ | Marlin: sgl-kernel 内 67 个（cubin #39）+ b12x 新增；CUTLASS: 5 有效 tile × 2 schedule × 2 kernel （dense Coop + grouped Pingpong） = 20+ variant | kernels-sm120.md § 5 |
| **dead kernel 有多少个**？ | 163 个（sm_100 tcgen05/UMMA 52 + sm_90 WGMMA 111），在 .so 占体积但 sm_120 调用即崩 | current.md § 2.4 |
| **是否有精度问题的 kernel**？ | **是**：dequant_fp8_scales 小 global_scale 下 BF16 widening underflow（vLLM PR #34577 型），已部分 backport 但 C++ 端未修 | current.md § 3.2, dead-ends.md § G |
| **哪些是探索失败弃用的**？ | Marlin small-M atomic + shape-aware tile (`32d27c7`，与 EAGLE 不兼容）、b12x bucket=64 override（full eval -1.06pp）、flashinfer CUTLASS 4.4.2→4.5.0（高风险） | changelog R-b12x-tune/bucket64, todo.md § 1.2 |

---

### 最终建议（< 300 字总结）

**gemm 这块应该收敛到 6 核心文档 + 1 决策档**：

1. **不动**：charter（契约） → hardware → sol_table（3 阶段基础档）
2. **轻调**：current（删过期章节） → marlin（删冗余指向） → methodology（补说明）
3. **重写**：todo.md（按 Tier 和 lock-in 状态重新组织）
4. **新增**：changelog-decisions.md（快速查 lock-in/rejected 原因）
5. **归档**：changelog R1-R7（73KB 流水账→10KB 摘要）到 archive/
6. **工程档保留**：so-replacements.md（必要工程规范）

**当前 docs/gemm 瘦身后约 200KB → 80KB**（去掉 changelog 重复、over-documented Stage 4 卡片、各库对比章节）。**保留完整的思想链条和决策轨迹，去掉冗余详细数字**。核心 value 是"为什么做"和"为什么不做"，而非每轮的绝对数字。
```

> TOOL

tool_use Agent
```json
{
  "description": "prefill docs audit",
  "subagent_type": "Explore",
  "prompt": "背景：你在 /user_4813494d/openbmb（SOAR MiniCPM-SALA 推理优化工作区）。先读 /user_4813494d/openbmb/CLAUDE.md，特别是 \"## 当前分支状态\" 里的 prefill 当前状态：\n- 保留 plan cache（layer/chunk 复用），`shape_only_plan_cache` 由 471e20b 修复\n- `fi_convert` 跨层缓存已禁用，只保留 SGLANG_MINICPM_UNSAFE_FI_CONVERT_CACHE=1 实验开关\n- `compressed_max_seqlen_k` 旧方案回退，当前是带 guard 的 stage1 actual maxlen + full-layout scratch/direct-pool\n- TrtLLM stage2 替换已否决，代码不含 `_USE_TRTLLM_STAGE2`\n- SGLANG_FAST_PREFILL_STAGE1=1 默认关闭\n\n任务：审计 docs/prefill/ 目录，对比 demo-sala/sglang/python/ 中相关代码（chunk attention、稀疏 prefill、stage1/stage2）和 git log。\n\n需要审计：\n- docs/prefill/README.md\n- docs/prefill/current.md（事实快照，28K 行最大）\n- docs/prefill/history.md\n\n调查重点：\n1. **current.md** 是否准确反映 CLAUDE.md 列出的当前事实？还是说还在描述旧方案（TrtLLM stage2、compressed_max_seqlen_k 等已否决方案）作为\"当前\"？\n2. **history.md 和 current.md 是否重复**？history 是否已经记录了否决理由，还是只是 current 的旧版本？\n3. **Phantom**：文档提到的代码符号（plan cache、stage1/stage2 kernel、`fi_convert`、`compressed_max_seqlen_k`）在 demo-sala/sglang/python/ 下是否能 grep 到？哪些已删？\n4. **piecewise CUDA Graph prefill 调研** 是 git log 里 3c17ea3 提交的工作区，docs/prefill/ 里有提到吗？该不该写进来？\n5. **main-test prefill 研究工作区**（141fb6d）有没有反映到文档里？\n\n报告格式（中文）：\n- 每个文档一节：保留 / 重写 / 合并 / 删除 + 证据\n- 当前文档与代码事实的差距清单\n- 总建议（< 250 字）"
}
```

> TOOL

tool_result Agent
```
现在我有了足够的信息。让我生成最终审计报告。

---

## 审计报告：docs/prefill/ 文档对比代码现状

### 1. **README.md** — 保留（索引准确）

**现状**：2 个文档索引（current.md 和 history.md）。
**审计结果**：索引准确，符合实际内容。
**建议**：保留，但应补充说明 piecewise/ 和 prefill/ 两个工作区的定位。

---

### 2. **current.md** — 重写（内容滞后，缺关键工作区）

**事实差距清单**：

| 问题 | 证据 | 影响 |
|---|---|---|
| **缺失 piecewise CUDA Graph 工作区** | commit 3c17ea3（2026-05-20）已在 repo 根目录 piecewise/ 完成 5 份文档，评估结论：收益 < 0.3% wall。current.md 完全无提及。 | 接续者无法了解该调研路线的 go/no-go 决策依据。 |
| **缺失 main-test 工作区** | commit 141fb6d（2026-05-20）完成，包含 stage1/stage2/MLP/GLA 的 bounding conclusion（wall=54.97s @ 524K）、15 份实验脚本。current.md 只列数字，无工作区参考。 | 读者误以为 current.md 的性能数字是最新优化下限，实际还有其他调研维度。 |
| **§3.14 "stage1 mask/dtype 快捷路径"过时** | 该节引用 "早期 `q=8192,1.7ms` microbench"，但 main-test/experiment-log.md 明确标记 adjusted-q 形态才是真实 prod 生产形态（131072）。current.md 没引述这个更正。 | 维护者可能试图优化错的 baseline。 |
| **stage1 profile 数据来源不明** | current.md §1 "stage1_score 74ms/chunk"，但 history.md §2.3 的 nsys 真实 profile 显示 "stage1 splitkv 总占 0.16% wall（3.2ms）"，矛盾。来源应该是 main-test 的 "stage1-profile.md"，未标注。 | 混淆宏观 profile 口径（含 host overhead）vs 纯 kernel 时间。 |

**关键缺陷**：

- **3.2 TrtLLM stage2 替换**：current.md 说"已否决"，但 history.md §1 提供了 accuracy 风险的详细（Q>KV 场景下跳过 all-masked 行，speedup 完全来自这部分）。现版本 current.md 缺少这个风险说明。
- **3.4 compressed_max_seqlen_k**："旧方案危险行为已回退"，但代码仍在用（minicpm_backend.py 行 109 等处赋值 `compressed_max_seqlen_k=max(k1_lens[sparse_bs])`）。current.md 没说明当前如何 guard 这个危险行为。
- **3.14 阶段 3：stage1 trait sweep 已枯竭**：history.md §2 证据来自 nsys 硬件 profile（stage1 仅 0.16% wall），但 main-test 的 stage1-profile.md 与 stage1-groupmax-design.md 对 stage1 成本分解更细致。current.md 没引这两份。

**建议**：
- 补充 **§3.25 Piecewise CUDA Graph prefill**：引述 `piecewise/` 工作区结论（< 0.3% wall，3 hard blocker）。
- 补充 **§3.26 main-test 工作区与 bounding 分析**：cross-ref 至 `prefill/roadmap.md`，说明 stage1/stage2/MLP/GLA 各模块已 bounding 结论。
- 更新 **§3.14**：改为引述 main-test 的 "adjusted-q 131072" 真实 prod 形态，撤回"早期 microbench"假设。
- 更新 **§3.4**：说明 `compressed_max_seqlen_k` 当前是用 `metadata.k1.max_seq_len`（来自 stage1 actual k1）还是自己传的，guard 条件何在。

---

### 3. **history.md** — 合并（部分内容应迁入 current.md）

**现状**：17K 文档，包含：
- §1 trtllm_fmha_v2_prefill（2026-05-09 已废弃，含详细 accuracy 风险）
- §2 nsys 硬件 profile（2026-05-03，破除宏观结论）
- §4 已终结方向总表（23 项）
- §5 infllmv2 blockmask batch>1 修复（已落地）
- §6 infllmv2 paged KV 256 约束（方案 A 进行中）

**审计结果**：

| 部分 | 评价 |
|---|---|
| §1 trtllm_v2_prefill | **应迁入 current.md §3.2**：当前 current.md §3.2 说明太简，缺乏 speedup 来源（Q>KV all-masked 行）和 accuracy 风险的细节。建议折叠到 current.md，避免阅读割裂。 |
| §2 nsys profile | **可保留在 history**：是 2026-05-03 的深度审计，已支撑 current.md 各否决理由。作为"历史调研"存档合理。 |
| §4 已终结方向表 | **部分应整并到 current.md §3**：当前 current.md 23 项否决，history.md §4 也列 23 项，两份重复。应选一份为"canonical"。 |
| §5-6 infllmv2 修复 | **已在 current.md 落地**：§2.11 提到 stage1 guard，§3 中 compressed_max_seqlen_k 也与这相关。history 中细节可保留（§5.1 根因、§5.5 仍需验证），但应明确"已落地 prebuilt/.so"。 |

**建议**：
- 将 history.md §1（trtllm 详细）补充进 current.md §3.2，当前版本太言简意赅。
- 消除 history.md §4 与 current.md §3 的重复：统一为单一列表，在各小节展开（不重复列表头）。
- 保留 history.md 作为"调研过程与已验证的底线"存档，但在 README.md 中明确其定位为"深度技术审计而非当前事实"。

---

### 4. 代码现状 vs 文档对齐情况

**已确认代码符号现存**（所有 current.md 提及的 env var 都在 demo-sala/sglang/python/ 中找到）：
- `SGLANG_MINICPM_PLAN_CACHE`、`SGLANG_MINICPM_CROSS_FORWARD_BUFFER_REFRESH` ✓
- `SGLANG_MINICPM_STAGE1_ACTUAL_MAXLEN` ✓
- `SGLANG_MINICPM_FUSED_GLA_QK_NORM_ROPE_OOP` ✓（默认开启）

**已删除的代码符号**（§3 提及但代码无踪）：
- `_USE_TRTLLM_STAGE2` ✗ 不存在（正确，已否决）
- `SGLANG_FAST_PREFILL_STAGE1` ✗ 未找到（已关闭）

**现存但文档说明不足**：
- `compressed_max_seqlen_k`：现在用的是 `metadata.k1.max_seq_len`（来自 stage1 actual K1 长度），但代码中仍有 fallback 到 `self.forward_metadata.k1.max_seq_len`。current.md 说"旧方案已回退"，实际是"用 stage1 actual maxlen 代替 compressed 精度"，没说明清楚。

---

## 总建议（250字内）

**优先级**：

1. **current.md 补充 piecewise + main-test 工作区**（1 天）：
   - 加 §4 "后续调研方向" 部分，引述 piecewise/ 和 prefill/ 的 go/no-go 决策。
   - 标记性能数字的 profile 来源（main-test vs 官方 bench）。

2. **合并 history 与 current 的重复**（1 天）：
   - 将 history.md §1 trtllm 详细补进 current.md §3.2。
   - 消除 §3-§4 的已终结方向重复列表。

3. **澄清 stage1 cost 分析**（0.5 天）：
   - current.md §1 "stage1_score 74ms/chunk" 改为"宏观口径含 host overhead"，纯 kernel ~3.2ms（来自 history §2.3）。
   - cross-ref main-test 的 stage1-profile.md 供细致调研。

**核心风险**：current.md §3 的 23 项否决理由大多成立，但缺少最近两个工作区（piecewise、main-test）的 bounding 证据，阅读者误以为某些方向仍有余地（实际已 sealed）。
```

> TOOL

tool_use Agent
```json
{
  "description": "decode docs audit",
  "subagent_type": "Explore",
  "prompt": "背景：你在 /user_4813494d/openbmb（SOAR MiniCPM-SALA 推理优化工作区）。先读 /user_4813494d/openbmb/CLAUDE.md，当前 decode 派发：b12x 2-tier（Marlin小M / b12x全M / 3点CUTLASS override），覆盖 6 形状 58 tile 配置。\n\n任务：审计 docs/decode/ 目录，对比 demo-sala/sglang/python/ 中 modelopt_quant.py、marlin_utils_fp4.py、minicpm_backend.py 等 decode 路径相关代码。\n\n需要审计：\n- docs/decode/README.md\n- docs/decode/current.md\n- docs/decode/history.md\n\n调查重点：\n1. **current.md** 是否准确反映 b12x 2-tier 派发现状？SOP 和 profile 方法论是否还有效？\n2. **history.md** 是 decode 早期实验归档？和 docs/gemm/changelog.md 或 dead-ends.md 是否重叠（都是 kernel 实验）？\n3. **profile 方法论**（CLAUDE.md 提到 \"decode profile 方法论（重要避坑）\"）是否和 docs/gemm/methodology.md 内容重复？\n4. **Phantom**：文档提到的派发逻辑、threshold（SGLANG_MARLIN_DECODE_THRESHOLD=48）、kernel 选择是否还和代码一致？\n\n报告格式（中文）：\n- 每个文档一节：保留 / 重写 / 合并 / 删除 + 证据\n- 是否应该把 decode 和 gemm 内容合并？理由\n- 总建议（< 200 字）"
}
```

> TOOL

tool_result Agent
```
Perfect! Now I have all the information I need to write the audit report. Let me compile the findings:

## 审计报告：docs/decode/ 目录与代码一致性

### 1. docs/decode/README.md

**建议：保留，微调内容指针**

当前内容（13 行）仅列表索引，基本无误。但 `"当前 Phantom 写去除"` 的参考被删掉了——history.md §5.3 仅提一句 `phantom 写去除`（未展开），README 应不提此实现细节。

**证据**：
- history.md:116 提 `phantom 写去除` 但无定义（指 `alloc_sparse` 批量化 fix）
- 当前代码（modelopt_quant.py）无 `_phantom_*` 标记，说明已落地清理

**更新建议**：删掉 README 中对已落地细节的参考，改为对 current/history 的纯转向。

---

### 2. docs/decode/current.md

**建议：部分需重写（关键派发逻辑已变更）**

#### 2.1 **b12x 2-tier 派发状态已过时**

- **文档说（p.37）**：`"b12x 2-tier dispatch ⚠️ 开发完成 + AOT cache 已生成，默认 SGLANG_ENABLE_B12X=0"`
- **代码现状（2026-05-10 commit 679017f）**：b12x 已重启为生产 target dispatch
  - Decode single +28.5%、bs=8-24 +6-12%
  - Stage A bit-exact 通过（max_diff=0, cos_sim=1.0）
  - **需确认** prepare_env.sh 是否已改 default=1，但目前仍是 default=0（line 519）

#### 2.2 **Hybrid Marlin threshold 描述准确但不够深**

- current.md 仅说明派发规则但未引 SGLANG_MARLIN_DECODE_THRESHOLD=48 源头
- 缺 **methodology.md §3 M regime** 的物理依据（weight-bound→transition boundary）
- **代码验证**（modelopt_quant.py line 184-210）：
  - ✅ global threshold = 48（与文档一致）
  - ✅ per-shape override dict 已实装（空集合，§5b 已撤销）
  - ✅ `_should_use_marlin_override()` 守卫存在

**问题**：current.md 把 threshold 当编码细节，未关联硬件 AI regime 边界理论。新读者无法判断为什么是 48。

#### 2.3 **Profile 方法论重复度高**

- current.md §3（279 行 profile 方法论）与 gemm/methodology.md（586 行）有 **45% 重叠**
  - nsys `--cuda-graph-trace=node` 说法相同
  - idle breakdown 三分类相同
  - NVTX 归因陷阱相同（§3.3 ↔ gemm/methodology §8）

**问题**：两份文档各说一遍相同的"CPU sync 时间 ≠ CPU 工作"教训，后来者无法判断是否同一套理论还是独立发现。

---

### 3. docs/decode/history.md

**建议：合并到 gemm/dead-ends.md 或 gemm/changelog.md**

#### 3.1 **kernel 调优失败归档**

history.md §1-4 是 decode 早期问题：
- 空响应（根因 FlashInfer 版本）
- sparse_page_table 跨层复用不可行
- Metadata 冗余（已修）
- stage2 backend 替换（FlashInfer sm_120 只有 fa2 路）

**这些与 gemm/dead-ends.md §B/C（PingPong dense path、spill 优化、RTX PRO ncu）属同类**：硬件/框架约束导致路线终结。

#### 3.2 **Profile 误归因事故（§5-8）**

- 事故 1：`alloc_sparse_new_positions` 虚惊（§5）
- 事故 2：`EI_ai_tolist` profile 假象（§7-8）
- **根本原因**：CUDA API profile 归因陷阱（CPU sync time 是 GPU work 投影）

**问题**：§8 "性能 profiling 方法论复盘" 是**通用软件 profiling 常识**，不是 decode 专有。§8.4 引用的 NVIDIA CUDA Best Practices Guide §8 同样适用于 gemm/prefill 调优。

**对标**：gemm/methodology.md §8 也讲 Amdahl 算和 idle breakdown，但用的是 roofline + 硬件常数表；decode/history.md §8 是"踩坑教训"风格。两套理论不矛盾但体系不同。

#### 3.3 **已枯竭路线（§9-10）**

- § 9：FP8 KV、Triton NVFP4、Medusa、mamba cache quant 等 **decode 侧已放弃方向**
- **与 gemm/dead-ends.md 区别**：
  - gemm/dead-ends 列的是**硬件/架构约束**（sm_120 无 WGMMA / TMEM）
  - history.md §9 列的是**性能尝试失败**（"跑了发现没收益"）

**判定**：§9 属 **decode 私有负结果档案**，不应并入 gemm；§10 的一些条目（e.g., "FP8 decode 无收益" L289）可作为 gemm roofline 验证案例。

---

### 4. 关键不一致点（代码 vs 文档）

| 项 | 文档说法 | 代码现状 | 影响 |
|---|---|---|---|
| **b12x default 状态** | `SGLANG_ENABLE_B12X=0`（默认关） | prepare_env.sh line 519 仍 default=0 | ⚠️ 高优先级：代码有 b12x target dispatch (commit 679017f) 但未开启 |
| **marlin_upper 各形状** | 仅提全局 48 | modelopt_quant.py line 195-202 有 dict 全 48 | ✅ 一致；但应引 R3 回退 note |
| **threshold=48 依据** | 未给出 | gemm/methodology.md §3 有"weight-bound→transition boundary" 证明 | ❌ current.md 应交叉引用 |
| **profile 方法论** | current.md §3 详述 | gemm/methodology.md §3.5-§8 重述 | ⚠️ 重复度 45%，应 DRY（Don't Repeat Yourself） |
| **Phantom** | history.md:116 一笔带过 | 代码已清理，无残留 | ✅ 可，但 README 不应提 |

---

### 5. 是否应合并 decode 和 gemm 文档？

**建议：不合并，但要增强交叉引用**

**理由**：

| 维度 | decode | gemm | 可否合并 |
|---|---|---|---|
| **核心职责** | 算子融合 + profile 方法论 | kernel 底层 (CUTLASS/Marlin) 调优 | ❌ 不同层级 |
| **受众** | Server 推理工程师（看 token/s） | Kernel 开发者（看 SOL%） | ❌ 关注点不同 |
| **失败模式** | profile 陷阱、算子融合 ROI | 硬件约束、编译器行为 | ⚠️ 有共同教训但背景差 |
| **方法论体系** | "踩坑后悔"式 narrative | "第一性原理 + SOP 契约"式 | ❌ 文风不同 |
| **更新频率** | 快（配置变化 / env gate 多） | 慢（kernel 本身变化少） | ❌ 发布节奏不同 |

**实际行动**：
1. ✅ 保留 decode/current.md 的派发逻辑 + profile SOP
2. ✅ 将 decode/history.md §1-4（"框架约束导致路线终结"）迁移到 gemm/dead-ends.md 作为补充案例
3. ✅ 将 decode/history.md §8（"Amdahl + idle breakdown 方法论"）合并为 gemm/methodology.md §9（跨 kernel/decode 通用 profiling 纪律）
4. ❌ **不合并** decode/current.md 和 gemm/current.md（层级/受众差异）

---

### 6. 总建议（<200 字）

| 文档 | 行动 | 优先级 |
|---|---|---|
| **current.md** | 重写 §1.0（b12x 状态）+ 补充 threshold=48 物理依据链接到 gemm/methodology §3 | 🔴 高 |
| **history.md** | (1) 迁 §1-4 到 gemm/dead-ends.md；(2) 合并 §8 到 gemm/methodology.md；(3) 保留 §5-7 作 decode 私有负结果档案 | 🟡 中 |
| **README.md** | 删掉"phantom"参考，纯转向 current/history | 🟢 低 |
| **跨引用** | current.md §2.2 加脚注 → gemm/methodology.md §3（M regime 边界）；history.md 各失败点加 §出处标记 | 🟡 中 |

**核心问题**：b12x target dispatch 已重启（commit 679017f），但文档和 prepare_env.sh default 未同步。需即刻验证生产线是否应改 `SGLANG_ENABLE_B12X=1`；若是，则 current.md 整体需重写。
```

> TOOL

tool_use Agent
```json
{
  "description": "eagle docs audit",
  "subagent_type": "Explore",
  "prompt": "背景：你在 /user_4813494d/openbmb（SOAR MiniCPM-SALA 推理优化工作区）。先读 /user_4813494d/openbmb/CLAUDE.md，当前 EAGLE-3 配置：\n- 提交包 spec_steps=3 topk=2 dtn=7\n- Dynamic spec mode（NO_SPEC / D5 / D7 按 running batch size 切换）\n- Draft model: `eagle/models/v2mix_20k_s3500_ood757/`（v2mix 20K + s3500 + ood757，NVFP4 QAT）\n- Eagle 数据路线：target-regenerated（target 自生成续写作训练 label），`eagle/pipelines/target_regen/`\n- `eagle/models/det_prefill/` 是更早的 det-target prefill baseline，已退居参考\n- DFlash/DDTree 是探索性实验，不作为生产\n\n任务：审计 docs/eagle/ 目录（13 个文件，是除 gemm 外的第二大主题），对比 eagle/ 代码（models、pipelines、training scripts）。\n\n需要审计：\n- docs/eagle/README.md\n- docs/eagle/prod.md（生产 draft 事实）\n- docs/eagle/architecture.md\n- docs/eagle/collapse.md（17K 行）\n- docs/eagle/runtime-deep.md（21K 行）\n- docs/eagle/papers.md（46K 行最大）\n- docs/eagle/spec-v2.md\n- docs/eagle/experiments.md（14K 行）\n- docs/eagle/large-batch.md\n- docs/eagle/300k-training-plan.md\n- docs/eagle/d7-tune-bench-20260511.md（日期戳，明显是日志）\n- docs/eagle/dflash.md（在 eagle 下又有 dflash？）\n- docs/eagle/training/README.md\n- docs/eagle/training/pipeline.md\n- docs/eagle/training/data-compression.md\n- docs/eagle/training/history.md\n\n调查重点：\n1. **papers.md 46K 是不是论文摘记堆？** 还有保留价值吗，还是应该归档？\n2. **d7-tune-bench-20260511.md** 显然是日期戳，是一次 tune 的产物吗？应该归档还是删除？\n3. **300k-training-plan.md** 这个计划是否已经执行（看 eagle/pipelines 和 eagle/models）？\n4. **eagle/dflash.md** 和 docs/dflash/ 重复吗？为什么 eagle 子目录下有一份？\n5. **collapse.md** 17K 是 collapse 根因分析，还有现实意义吗？还是说当前 v2mix_20k_s3500_ood757 已经解决了 collapse？\n6. **runtime-deep.md** 21K 是运行时深挖，和 spec-v2.md / large-batch.md 有重叠吗？\n7. **experiments.md** 是连续追加的实验记录，最新的实验状态如何？\n8. **training/history.md vs training/pipeline.md vs training/data-compression.md** 之间什么关系？\n9. **prod.md** 是否准确反映当前 `v2mix_20k_s3500_ood757`？\n10. **Phantom**：文档提到的脚本（pipelines/target_regen/、训练 launcher、ckpt 转换 scripts）在 eagle/ 下是否还存在？哪些路径已经改名/删除？\n\n可以用 `git log --oneline -- docs/eagle/` 看修改时间。\n\n报告格式（中文）：\n- 每个文档一节：保留 / 截断 / 重写 / 合并 / 删除 + 证据\n- 总建议（< 350 字）：eagle 这块应该如何收敛文件结构"
}
```

> TOOL

tool_result Agent
```
Excellent! Now I have comprehensive information. Let me generate the audit report:

---

## 审计报告：docs/eagle/ 文档集合（16 个文件，3742 行）

### 文件级审计

#### 1. **README.md**（52 行）✅ **保留**
- **现状**：索引文档，列举 13 个主题文档 + 生产配置速览 + 当前数据路线
- **准确性**：高。当前事实与 CLAUDE.md 同步（`v2mix_20k_s3500_ood757`、dynamic spec mode、`spec_steps=3, topk=2, dtn=7`）
- **证据**：最新两次更新 commit `2c62397`（v3mix）和 `7ef0eb0`（v3mix collection）都同步了索引
- **建议**：保留。这是门户，聚合性文档。每次主题有重大变更时同步索引即可

#### 2. **prod.md**（132 行）✅ **保留 + 微调**
- **现状**：v2mix_20k_s3500_ood757 生产事实记录（OOD0=0.7571、cosine LR、sequence packing）
- **准确性**：高。与代码一致（参数对齐验证：ttt_steps=3、aux_layers=[1,10,22]、rope_theta=144000、draft_vocab=32000）
- **局限**：只记录了 v2mix_20k，对 v3mix_300K 采集进展（已在 `7ef0eb0` 上线）无记录
- **建议**：当前 prod 保留。如果 v3mix_300K 训练完成落地，新建 `prod-v3mix-300k.md` 并更新索引；不合并，保持历史记录

#### 3. **d7-tune-bench-20260511.md**（95 行）⚠️ **截断为实验笔记**
- **现状**：日期戳文件，记录 2026-05-11 D7 调档实测（steps 5→6, dtn 11→13）
- **性质**：快照报告，不是长期事实（已融入 CLAUDE.md 生产配置，评测机 probe-sala-s2 反向 SSH 也已提及）
- **价值**：反向 SSH 设施细节（frpc + dropbear）和调档过程有重要诊断价值
- **问题**：
  - 标题带日期戳，易被误认为旧数据；实际配置至今沿用（已 lock-in）
  - 与 `experiments.md` 职责重叠（都是验证实验日志）
- **建议**：**保留但重命名为 `experiments-d7-tune-20260511.md`**，归并到 `training/history.md` 的时间线（s5→s6 调档是 v2mix 后续的一次 tuning，不是新 draft 版本）；关键「反向 SSH 设施」迁移到 `docs/platform/` 下（`cu13-platform-debugging.md`）

#### 4. **collapse.md**（292 行）✅ **保留**
- **现状**：EAGLE-3 accept-rate collapse 根因诊断（长上下文、draft 能力缺陷、d2t 结构 miss）+ 学术文献支撑
- **现实意义**：高度相关
  - `rope_theta=1M` 修复已部署（vlong context +44.9% adj_al，见 `experiments.md` §1）
  - d2t miss（`<unk>`=89.2%）仍是性能短板，所有 draft 设计都要对齐
  - long context collapse 是已发表的普遍现象（OWL/EMNLP 2025、LongSpec/ACL 2025），非 EAGLE 特有
- **风险**：17K 行看似大，但内容无重叠，需要保留作为长上下文 spec decoding 的设计参考
- **建议**：保留。补充一句「当前 v2mix_20k_s3500_ood757 已应用 rope_theta=1M 与 MARS θ=0.85 双重修复」

#### 5. **runtime-deep.md**（581 行）✅ **保留 + 明确职责边界**
- **现状**：代码级深读（基于 `eagle_worker.py`、`minicpm_backend.py` 等源码），覆盖 TARGET_VERIFY 流程、CUDA graph capture、tree-aware GLA verify
- **质量**：高。英文、严谨、逐行引用源码位置（e.g. `demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py:158-211`）
- **职责冲突**：与 `spec-v2.md`、`architecture.md` 有交叉
  - `runtime-deep.md` 关注"当前代码如何实现"（事实陈述）
  - `spec-v2.md` 关注"v1 vs v2 边界、已解决/待解决问题"（决策记录）
  - `architecture.md` 关注"draft 模型架构、SGLang 适配的 4 个关键修复"（设计概览）
- **建议**：保留。但在 README.md 索引中明确标注"源码级深读，适合核心贡献者"；与 `spec-v2.md` 的重叠部分（GLA tree verify）在 `spec-v2.md` 中加交叉引用

#### 6. **papers.md**（809 行）⚠️ **截断为学术参考库**
- **现状**：60+ 篇论文精要库（verify 机制创新、接受规则、线性注意力、长上下文）+ MARS 完整落地细节
- **量化**：809 行中，论文摘记 ~400 行，MARS 实装细节（5 个文件、11 参数）~100 行，其余为结构和交叉引用
- **价值**：
  - **高价值部分**：MARS θ=0.85 实装规范（已部署）、论文参数扫描结论（θ=0.90 vs θ=0.85 trade-off）
  - **参考价值**：下一代 draft 设计（tree/SSM/sparse-KV 方案综述）
  - **低价值部分**：纯论文摘记（§1.1-§1.7），可归档
- **问题**：
  - 充当了"待决策的学术方案库"（大 batch 缩水见 `large-batch.md` §3，重复）
  - 论文标题 + 核心数字跨越多个章节，难以快速检索
- **建议**：**截断为 150 行核心参考**
  - 保留：MARS 实装细节（完整复现）、当前生产验证规则的论文证据
  - 删除：纯摘记的 tree/verify 创新（已在 `architecture.md` 和 `large-batch.md` 总结）
  - 迁移：下一代方案综述（Sequoia、SpecFormer、P-EAGLE）→ `large-batch.md §3.2-§3.3`

#### 7. **experiments.md**（269 行）✅ **保留**
- **现状**：验证实验进度日志（rope_theta=1M / Phased Verify / GLA state 并行），3 个方向已完成
- **准确性**：高。数据精确（rope_theta=1M 长 context +44.9% adj_al 已落地）
- **职责**：与 README.md 中的"结论快查"表格一致；反向引用关系清晰
- **风险**：方向二（Phased Verify）和方向三（GLA state 并行）虽然完成离线分析，但代码实装仍未合并（代码注释"留作下次"）
- **建议**：保留。补充一行注记「Phased Verify 和 GLA state 并行分析完成，代码实装已 deferred；当前生产路径仅落地 rope_theta=1M 和 MARS θ=0.85」

#### 8. **spec-v2.md**（275 行）✅ **保留**
- **现状**：Spec V2 overlap 适配记录（目标 / 启用方式 / 路径总览 / v1 边界 / 原始问题 + 修复）
- **关键**：§5 已确认的原始问题（GLA/sparse k1k2/finished req 过滤）明确了 v2 的风险，有助于未来 spec v2 维护
- **非冗余**：本文档是决策记录（"为什么做这些改动"），`runtime-deep.md` 是实现记录（"代码怎么做的"）
- **建议**：保留。标注"v2 overlap 为高级特性，当前 prod 未启用（SGLANG_ENABLE_SPEC_V2=0）"

#### 9. **architecture.md**（132 行）✅ **保留**
- **现状**：draft 模型架构（437M 参数、fc 融合、aux_layers=[1,10,22]）+ 4 个关键 SGLang 适配修复 + Fused GLA kernel（7.63× 加速）
- **准确性**：高。与代码一致（commit `8bc05a3` spec v1 路径）
- **综合价值**：新人入门必读
- **建议**：保留

#### 10. **large-batch.md**（128 行）✅ **保留**
- **现状**：大 batch spec 增益缩水的 6 个机制（roofline、KV BW、straggler、draft overhead、tree mask、量化）+ SALA 架构事实 + 学术方案 40+ 篇
- **核心**：当前 dynamic spec mode（bs≥31 → NO_SPEC）的决策依据完整记录
- **综合性**：本文档是对 `spec-v2.md`（算法）和 `runtime-deep.md`（代码）的性能透视
- **建议**：保留。补充一行「当前生产采用 dynamic spec mode 规避大 batch 缩水」

#### 11. **dflash.md**（187 行）⚠️ **删除**
- **现状**：早期调研笔记（§1-§8），已于 2026-05-09 deprecate
- **事实**：
  - 文件开头已标记"🚨 文档已 deprecate"，指向 `../dflash/` 当前事实
  - `docs/dflash/` 目录已规范化建立（current.md / integration.md / ddtree.md / history.md）
  - commit `528332b`（2026-05-12）"按规范新建 docs/dflash/ 主题，归并 eagle/dflash.md" 表明归并已完成
- **遗留**：本文件仅作"历史档案"保留 §1-§8，但无人维护、无交叉引用、占用 187 行
- **建议**：**删除**。若需保留调研历史，应迁移到 `docs/dflash/history.md` 中；当前 `docs/eagle/` 下无实质用途

---

### 训练子目录 (`training/`) 审计

#### 12. **training/README.md**（14 行）✅ **保留**
- 索引页面，指向 3 个关键主题

#### 13. **training/pipeline.md**（247 行）✅ **保留**
- **现状**：训练流水线规范（target-regenerated 数据路线、v3mix_300K 采集、NVFP4 forward GEMM、真 4-bit 落地）
- **最新**：commit `2c62397` 更新了 v3mix server hook 直写 NVFP4（已上线）
- **准确性**：高。采集 smoke 数据（256 条）、overlap 性能对比、graph/window 验证均已实测
- **建议**：保留

#### 14. **training/history.md**（140 行）✅ **保留 + 整理**
- **现状**：v2 → v3（否决）→ v4 → det_prefill → v2mix_20k 的时间线
- **问题**：
  - 最后一个版本是 v2mix_20k（2026-05-07），之后的 v3mix_300K（2026-05-16 onwards）未记录
  - D7 调档（2026-05-11）的历史地位未明确（是 v2mix_20k 的后续 tuning，还是新版本？）
- **建议**：保留 + 补充 v3mix_300K 时间线（占位待填，当前仅在 `pipeline.md` 中零散出现）；D7 调档作为 v2mix_20k 的"post-launch tuning"附在后面

#### 15. **training/data-compression.md**（83 行）✅ **保留**
- **现状**：NVFP4 codec 实测（3.2× 压缩比）、通用 zstd 对 bf16 无效、当前决策（v3mix 采用 direct hook NVFP4）
- **准确性**：高。4 条 overfit 验证已完成（2026-05-16）
- **建议**：保留

---

### 总体文档健康度评分

| 维度 | 评分 | 备注 |
|---|---|---|
| 索引完整性 | 9/10 | README.md 覆盖 13 主题，微调：补充 v3mix_300K 现状 |
| 事实准确性 | 9/10 | 大部分文档与代码同步；少数（d7-tune）需明确标记为"历史快照"而非"当前状态" |
| 重复率 | 7/10 | papers.md / large-batch.md / runtime-deep.md 论文摘记重合；dflash.md 完全 deprecated |
| 可维护性 | 6/10 | 缺少"文档更新 SOP"和"版本对应关系"；v3mix_300K 进展散落在 pipeline.md 各处 |
| 新手友好度 | 8/10 | README.md 快查表很好；runtime-deep.md 应标注"高级" |

---

### 建议总结（< 350 字）

**eagle/ 文档收敛方案**：

1. **保留核心文档**（11 个）：README、prod、collapse、runtime-deep、experiments、spec-v2、architecture、large-batch、training/{README,pipeline,history,data-compression}。这些为决策记录、设计参考或常用查询。

2. **截断 papers.md**：从 809 行 → 150 行。保留 MARS 实装细节和关键学术证据；论文摘记（60+ 篇）迁移到 large-batch.md §3 的学术方案综述，实现单一信息源。

3. **重命名 d7-tune-bench-20260511.md**：→ `experiments-d7-tuning-20260511.md`，归并到 training/history.md。关键"反向 SSH 调试设施"迁出到 `docs/platform/cu13-debug-sandbox.md`。

4. **更新 training/history.md**：补充 v3mix_300K（2026-05-16 onwards）的时间线框架；明确 D7 调档为 v2mix_20k 的 post-launch 性能 tuning，非新版本。

5. **补充跨文档标记**：在 README.md 索引中注记"源码深读"（runtime-deep）、"决策记录"（spec-v2）、"性能分析"（large-batch）的用途，便于读者快速定位。

**预期效果**：文档规模 3742 行 → ~3200 行；重复消减 40%；版本追踪清晰。
```

> TOOL

tool_use Agent
```json
{
  "description": "ngram docs audit",
  "subagent_type": "Explore",
  "prompt": "背景：你在 /user_4813494d/openbmb（SOAR MiniCPM-SALA 推理优化工作区）。先读 /user_4813494d/openbmb/CLAUDE.md。CLAUDE.md 主索引提到 ngram 是 \"request-local ngram lookup：probe / EAGLE routing / CUDA graph 稳定性修复\"。\n\n任务：审计 docs/ngram/ 目录，对比代码现状。\n\n需要审计：\n- docs/ngram/README.md\n- docs/ngram/probe.md\n- docs/ngram/routing.md\n\n调查重点：\n1. **ngram 当前是不是生产功能？** 还是探索路线？grep \"ngram\" 在 demo-sala/sglang/python/ 看是否有实际代码。\n2. **probe vs routing** 是两个独立特性还是同一个？文档里关系如何？\n3. **CUDA graph 稳定性修复** 是不是已经合并到 EAGLE 路径里了？\n4. **eagle/start_eagle.sh 默认是否启用 ngram**？看一下脚本。\n5. **Phantom**：文档提到的代码符号在代码里是否存在？\n\n报告格式（中文）：\n- 每个文档一节：保留 / 合并 / 删除 + 证据\n- ngram 整体定位：生产 / 探索 / 已弃用？\n- 总建议（< 200 字）"
}
```

> TOOL

tool_result Agent
```
Perfect! Now I have all the information needed. Let me compile my audit report.

---

## ngram 文档审计报告

### 1. docs/ngram/README.md
**决策**: **保留** ✓

**证据**:
- 文档准确描述了两个子文档的职责划分
- `routing.md` 对应 runtime 实现（已在代码中验证）
- `probe.md` 对应实现前离线调研（已有完整 probe 脚本）
- 文档简洁，作为目录索引是必要的

---

### 2. docs/ngram/probe.md
**决策**: **保留** ✓

**证据**:
- 标题明确注明"调研归档（2026-05-15）"，定位清晰
- 所有 probe 脚本存在且可用：
  - `/user_4813494d/openbmb/bench/ngram_probe_char.py`（字符级初步）
  - `/user_4813494d/openbmb/bench/ngram_probe_token.py`（token 级 sweep）
  - `/user_4813494d/openbmb/bench/ngram_probe_inspect.py`（sample 检查）
  - `/user_4813494d/openbmb/bench/ngram_probe_trace.py`（step trace）
- 数据集存在：`bench/data/speed_bench_cunlimited.jsonl`
- Tokenizer 存在：`demo-sala/data/eagle_draft/`
- 提及的代码符号准确存在：
  - `NGRAMWorker` 在 `ngram_worker.py:24` ✓
  - `NgramCache` 在 `ngram_worker.py:14` ✓
  - `ngram_worker.py:50` 的 `self.ngram_cache` ✓
  - `ngram_worker.py:199-211` 的 `_update_ngram_cache` 逻辑准确 ✓

---

### 3. docs/ngram/routing.md
**决策**: **保留，补充细微更新** 

**证据与现状对齐**:

#### 3.1 实现路径（所有文件存在且已合并）✓
- `demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py`
  - `_get_req_ngram_str()` L1207 ✓
  - `_lookup_req_ngram_draft()` L1238 ✓
  - `_make_ngram_route_subbatch()` L1263 ✓
  - `_build_ngram_chain_verify_input()` L1351 ✓
  - `_draft_ngram_route()` L1463 ✓
  - `draft()` 入口 L1520 已实现路由逻辑 ✓

- `eagle_draft_cuda_graph_runner.py` L20 有 `_NGRAM_DEBUG_SYNC` ✓
- `eagle_draft_extend_cuda_graph_runner.py` 已更新支持 ngram 深度 ✓
- `hybrid_linear_attn_backend.py` 已存在 ✓

#### 3.2 CUDA Graph 稳定性修复已实现 ✓
- **D5/D7 分离后端**（文档 L77-81 所述）：
  - `eagle_worker.py:543-559` 创建 `draft_attn_backend_d5` 和 `draft_attn_backend_d7`
  - `eagle_worker.py:583-584` 维护 `cuda_graph_runner_d5` 和 `cuda_graph_runner_d7`
  - `eagle_worker.py:625-683` 分别 capture D5/D7 CUDA graph
  - `eagle_worker.py:825-851` 在 `_apply_spec_config()` 中切 runner

- **ngram 路由下 miss sub-batch 支持任意 batch size**（L82）：
  - `_draft_ngram_route()` 构造 miss_batch，传给 `_draft_eagle_verify_input(miss_batch)`
  - draft graph capture 全整数 bs=1..max_bs ✓

- **draft extend graph token budget 扩展**（L83）：
  - `eagle_worker.py:449-475` 配置 `max_draft_extend_tokens_per_bs` 扩到 ngram 最大接受深度 ✓

#### 3.3 默认配置（eval/start_eagle.sh + demo-sala/prepare_env.sh）✓
- `SGLANG_EAGLE_NGRAM_ROUTE=1` 默认开启：
  - `eval/start_eagle.sh:70` ✓
  - `demo-sala/prepare_env.sh:546` ✓
- `SGLANG_EAGLE_NGRAM_LOG_EVERY=0` 默认关闭日志：
  - `eval/start_eagle.sh:71` ✓
  - `demo-sala/prepare_env.sh:547` ✓
- ngram 配置 (k=5..12, K=15)：
  - `eval/start_eagle.sh:72-74` ✓
  - `demo-sala/prepare_env.sh:548-550` ✓

#### 3.4 验证记录（稳定性测试）✓
- 编译验证命令有效（文件都存在）
- 稳定性测试参数正确
- **重要**: 文档提到的 `success=64/64` 结果仍是当时的快照，非当前实时状态，但验证方法仍可复现

#### 3.5 轻微不一致
- 文档 L47 提到 "主要文件"，实际上关键文件在 `demo-sala/sglang/` 下是正确的，但没有提 `ngram_worker.py`（已被新的 routing 替代，不是接入点，正确）

---

### 4. ngram 整体定位
**生产功能** ✓

**证据**:
- `routing.md` 标题："Runtime 集成"，不是"探索"或"历史"
- 已合并入主线（commit `373023a`，May 15 22:44）
- **生产默认开启**：
  - `eval/start_eagle.sh:70` `SGLANG_EAGLE_NGRAM_ROUTE="${SGLANG_EAGLE_NGRAM_ROUTE:-1}"`（默认值为 1）
  - `demo-sala/prepare_env.sh:546` 同样默认 1
  - 这是提交包（demo-sala）的配置来源
- 代码集成点：`eagle_worker.py:1520` 的 `draft()` 方法是热路径，ngram 在此前置拦截
- CUDA graph 稳定性已修复（D5/D7 分离）

---

### 5. 关键问题回答

| 问题 | 回答 | 证据 |
|------|------|------|
| **ngram 当前是生产功能吗？** | 是 | 默认开启，已合并，docs 标注为"runtime 集成" |
| **probe vs routing 关系?** | 两个阶段 | probe = 实现前离线调研；routing = 工程实现 |
| **CUDA graph 稳定性修复合并了吗?** | 是 | D5/D7 分离后端已在 eagle_worker.py L543-683 |
| **start_eagle.sh 默认开启吗?** | 是 | L70 `=${SGLANG_EAGLE_NGRAM_ROUTE:-1}` |
| **Phantom 代码符号?** | 无 | probe.md/routing.md 未提及；decode/history.md 只提 "phantom 写去除" 为代码清理 |

---

## 总建议（150 字）

**保留全部三个文档**。ngram routing 已是生产功能（默认开启），文档职责划分清晰：
- **README.md** 作为索引必要
- **probe.md** 记录实现前的关键调研数据和假设，是技术决策的依据
- **routing.md** 记录工程实现、CUDA 稳定性修复和验证方法

三份文档事实准确、代码符号校验无误。建议在 `routing.md` 脚注补注"验证结果为 2026-05-15 快照，当前性能数据需自行跑 bench"。
```

> TOOL

tool_use Agent
```json
{
  "description": "dflash docs audit",
  "subagent_type": "Explore",
  "prompt": "背景：你在 /user_4813494d/openbmb（SOAR MiniCPM-SALA 推理优化工作区）。先读 /user_4813494d/openbmb/CLAUDE.md。\n\nCLAUDE.md 明确说：**DFlash + DDTree 是探索性实验，不作为生产实践**。所有 `dflash/` / `eval/start_dflash*.sh` / `eval/start_ddtree.sh` / `docs/dflash/` 内容均为备选 spec 算法的探索路线，提交包仍走 EAGLE-3。\n\n任务：审计 docs/dflash/ 目录 + docs/eagle/dflash.md（eagle 目录下还有一份 dflash 文档），对比代码现状，判断是否还有保留价值。\n\n需要审计：\n- docs/dflash/README.md\n- docs/dflash/current.md\n- docs/dflash/ddtree.md\n- docs/dflash/history.md\n- docs/dflash/integration.md\n- docs/eagle/dflash.md\n\n调查重点：\n1. **dflash/ 代码目录现在还存在并维护吗？** ls /user_4813494d/openbmb/dflash/ 看看\n2. **eval/start_dflash*.sh** 和 **eval/start_ddtree.sh** 还存在吗？\n3. **当前 DFlash 探索是活跃的还是已经搁置？** git log --oneline -- docs/dflash/ 看一下最近修改时间\n4. **docs/eagle/dflash.md vs docs/dflash/*** 重复程度？为什么要在两个地方都有？\n5. **integration.md（SGLang 主线 DFlash skip custom_mask policy）** 是关键参考，是否还需要保留？\n6. **ddtree.md（输出乱码根因）** 是一次性 debug 记录还是有长期价值？\n\nCLAUDE.md 已经明确 DFlash/DDTree 是探索性，所以这块文档可能是大量探索归档。问题是：\n- 探索停了吗？还是仍在继续？\n- 如果停了，是否应该集中放到一个 archive 文档里？\n- 如果还在继续，文档结构合理吗？\n\n报告格式（中文）：\n- 每个文档一节：保留 / 归档 / 合并 / 删除 + 证据\n- DFlash 整体定位判断（基于 git log 和代码）\n- 总建议（< 250 字）"
}
```

> TOOL

tool_result Agent
```
完美。现在我有了足够的信息来做出审计结论。让我生成最终报告。

---

## 审计报告：docs/dflash/ + docs/eagle/dflash.md

### 整体定位判断

**DFlash/DDTree 是活跃的、已部分落地的探索算法**：
- 代码现状：`dflash/` 目录存在，含 32 个 .py 文件（训练 pipeline 完整）；eval 脚本齐全（`eval/start_dflash.sh`, `eval/start_dflash_single.sh`, `eval/start_ddtree.sh`）
- 时间轴：最近提交在 2026-05-09（仅 12 天前），共 6 个关键 commit（`012df6e` FULL_CTX 修复、`1915caf` DDTree 接入、`968a0f0` 功能正确、`2cb8592` worker 接入）
- CLAUDE.md 明确态度：「**不作为生产实践**，备选 spec 算法」；用户决策「先接 SGLang 再说，完成 dflash + ddtree 全套」
- **关键事实**：训练 checkpoint `best.pt` 在文档中多处引用（4.3 GB），但**实际磁盘不存在**（`/user_4813494d/openbmb/dflash/outputs/train/` 目录不存在）

---

### 各文档逐项评审

| 文档 | 保留价值 | 建议 | 证据 |
|---|---|---|---|
| **docs/dflash/README.md** | ✓ 保留 | **现状维持** | 目录索引清晰，指向 4 个子文档；启动入口 3 个脚本对应当前代码分支 |
| **docs/dflash/current.md** | ⭐ 核心 | **主文档，常更新** | 当前事实源（accept rate 1.15→1.62、DDTree 1.82-1.93），与 commit `012df6e` / `2c2713e` 直接对应；需补填 throughput 实测（已声明需跑 `mini_bench.sh`） |
| **docs/dflash/integration.md** | ⭐ 核心 | **保留，关键参考** | SGLang 主线 `_DFLASH_VERIFY_SKIP_CUSTOM_MASK_BACKENDS` 策略的唯一文档来源；minicpm_backend tree-mask 扩展说明；DDTree custom_mask 必要性的关键论证 |
| **docs/dflash/ddtree.md** | ⭐ 核心 | **保留，debug 档案** | FlashInfer sm_120 数值漂移根因（L31 8.5% drift）的唯一深度分析；manual SDPA workaround 的完整说明；4 个调试 env 变量文档化 |
| **docs/dflash/history.md** | ✓ 有价值 | **归档化，附注过期** | 6 个决策点完整记录（aux_layers=[1,10,22]、FP4QAT 选择性、chain vs tree、pos1=0.466）；多轮调试过程（DDTree 输出乱码 7 步隔离）；已枯竭路线清单（缩 budget / disable_split_kv / collapse 禁止）；**已部分过期**（ckpt `best.pt` 路径指向不存在目录，pos1 数字静态） |
| **docs/eagle/dflash.md** | ⭐ 有价值 | **改标题，保留归档** | §1-§8 的早期调研内容（DFlash 机制、训练反推、GLA chain 优势、移植障碍清单）；header 已标注 deprecate（重定向到 `../dflash/`）；但内容不应删除（§5 GLA chain verify 无污染论证独有、§7 MVP 验证框架仍适用） |

---

### 关键发现

**⚠️ 问题 1：training checkpoint 悬浮**
- 文档 4 处引用 `dflash/outputs/train/best.pt` 和 4.3 GB 大小
- 实际盘上**不存在**（目录 `/user_4813494d/openbmb/dflash/outputs/` 缺失）
- `eval/start_dflash*.sh` 默认指向此路径，脚本会失败
- **需要澄清**：ckpt 是离线保存还是 git-lfs / 外部存储？若永久缺失，文档需改为 placeholder

**⚠️ 问题 2：两地文档重复与版本混乱**
- `docs/eagle/dflash.md` 有 §1-§8 完整内容，但被 `docs/dflash/` 新建主题"归并"了
- 新文档分散到 current.md / integration.md / ddtree.md / history.md
- 早期调研 §1-§4（机制、数据配方、推理流程）**并未完全重现**在新目录中
  - 例：§3 的 "anchor 采样 + 并行 block forward" 在新文档中无具体描述
  - 例：§7 的 MVP 验证框架（5 层 → 2 层、block_size=8、accept_len > 2.0 门槛）没有保留

**✓ 优势：规范化内容结构**
- `current.md` / `history.md` 的约定（当前事实 vs 已枯竭路线）遵守了 CLAUDE.md 惯例
- 决策追溯链完整（时间线表、用户原话、commit hash、教训总结）

---

### 总建议（中文，< 250 字）

**保留全部，分层调整**：

1. **即时修复**：
   - `docs/dflash/history.md` / `current.md` 补注「`best.pt` 路径待确认」，或改为 `{DFLASH_CKPT}` placeholder
   - `docs/eagle/dflash.md` 顶部的 deprecate 标注下加一行「关键内容已分散到 ../dflash/；本文保留 §5 GLA chain 论证和 §7 MVP 框架供参考」

2. **保留核心 4 文**：
   - `current.md` — 当前吞吐 / accept_len 的唯一事实源
   - `integration.md` — SGLang 主线 skip-mask 策略的唯一详解
   - `ddtree.md` — FlashInfer 数值漂移根因的深度分析（稀有档案）
   - `history.md` — 决策链条 + 已枯竭路线（防止重踩）

3. **docs/eagle/dflash.md 转为存档标记**：不删除，但标注「历史调研，关键洞察见 ../dflash/ 下各文，本文供机制理解和 MVP 框架参考」

**理由**：DFlash 是活跃的本周 commit，非搁置探索；文档是仅有的决策与 debug 记录；checkpoint 缺失是部署问题而非文档问题。
```

> TOOL

tool_use Agent
```json
{
  "description": "blog docs audit",
  "subagent_type": "Explore",
  "prompt": "背景：你在 /user_4813494d/openbmb（SOAR MiniCPM-SALA 推理优化工作区）。CLAUDE.md 提到 docs/blog/ 是 \"周冠军技术分享（对外 blog）\"。\n\n任务：快速审计 docs/blog/ 目录，识别垃圾文件和清理点。\n\n需要审计：\n- docs/blog/README.md\n- docs/blog/week7.md\n- docs/blog/week8.md\n- docs/blog/week9.md\n- docs/blog/.ipynb_checkpoints/week9-checkpoint.md（这个看起来是 jupyter checkpoint 垃圾）\n\n调查重点：\n1. **.ipynb_checkpoints/** 是 jupyter 自动生成的临时目录，应该被 .gitignore，是不是垃圾？\n2. blog/week*.md 是对外发表的吗？还是草稿？看 git log --oneline -- docs/blog/\n3. 内容是否还有保留意义？\n\n报告格式（中文，简短，< 150 字）。"
}
```

> TOOL

tool_result Agent
```
完成审计。以下是报告：

---

## docs/blog/ 审计报告

**垃圾文件确认：**
1. **`.ipynb_checkpoints/week9-checkpoint.md`** — 确实是垃圾。`.gitignore` 已列入规则，但该目录仍被追踪。Jupyter 自动生成的临时文件，应删除。

**blog 文件性质：**
- **week7/8/9.md 是对外发表文档**，非草稿。README.md 明确标题"对外技术分享"，git log 显示规范提交（4 次）。
- 内容：量化、推测解码、EAGLE 适配、loss 函数——SOAR 比赛周冠军技术总结。

**保留意义：**
- ✓ 高价值：深度技术分享，适合开源项目 blog。
- ✓ 维护状态：week7-9 完整，README 索引清晰。

**清理建议：删除 `.ipynb_checkpoints/` 目录。其他文件完整且有价值。**
```

> TOOL

tool_use ToolSearch
```json
{
  "query": "select:TaskCreate,TaskUpdate,TaskList",
  "max_results": 3
}
```

> TOOL

tool_result ToolSearch
```
null
```

> AGENT

调研完成。9 个 subagent 报告已收齐。在执行清理前，我先把发现合并成行动清单，标记每项的置信度，然后跟你确认动哪些。

> TOOL

tool_use TaskCreate
```json
{
  "subject": "Audit synthesis: present consolidated cleanup plan",
  "description": "合并 9 个 subagent 报告，按置信度分级展示清理方案，请用户确认范围",
  "activeForm": "Synthesizing audit findings"
}
```

> TOOL

tool_result TaskCreate
```
Task #1 created successfully: Audit synthesis: present consolidated cleanup plan
```

> TOOL

tool_use TaskCreate
```json
{
  "subject": "Verify uncertain claims before destructive ops",
  "description": "subagent 报告中存在与 CLAUDE.md 冲突的事实（如 NVFP4 上下文 48K vs 92160、b12x default 状态等），先验证再动手",
  "activeForm": "Verifying contested claims"
}
```

> TOOL

tool_result TaskCreate
```
Task #2 created successfully: Verify uncertain claims before destructive ops
```

> TOOL

tool_use TaskCreate
```json
{
  "subject": "Tier-A cleanup: delete clear junk and deprecated files",
  "description": "删除明确死文件：docs/blog/.ipynb_checkpoints/、docs/eagle/dflash.md (已 deprecate，内容已迁 docs/dflash/)",
  "activeForm": "Executing Tier-A deletes"
}
```

> TOOL

tool_result TaskCreate
```
Task #3 created successfully: Tier-A cleanup: delete clear junk and deprecated files
```

> TOOL

tool_use TaskCreate
```json
{
  "subject": "Tier-B cleanup: rename / move one-off log files",
  "description": "d7-tune-bench-20260511.md 归并到 training/history.md 或 experiments.md；bottleneck_cards/ 可重命名暗示烂尾",
  "activeForm": "Executing Tier-B reorganization"
}
```

> TOOL

tool_result TaskCreate
```
Task #4 created successfully: Tier-B cleanup: rename / move one-off log files
```

> TOOL

tool_use TaskCreate
```json
{
  "subject": "Tier-C cleanup: truncate / split oversized files",
  "description": "gemm/changelog.md (73KB) 拆 archive、papers.md (46KB) 截断为核心参考",
  "activeForm": "Splitting oversized docs"
}
```

> TOOL

tool_result TaskCreate
```
Task #5 created successfully: Tier-C cleanup: truncate / split oversized files
```

> TOOL

tool_use TaskCreate
```json
{
  "subject": "Tier-D cleanup: rewrite/sync outdated current.md files",
  "description": "prefill/current.md 补 piecewise + main-test 工作区；decode/current.md 同步 b12x；handover.md 去除与 CLAUDE.md 重复的栈信息",
  "activeForm": "Rewriting outdated current docs"
}
```

> TOOL

tool_result TaskCreate
```
Task #6 created successfully: Tier-D cleanup: rewrite/sync outdated current.md files
```

> AGENT

接下来先验证几个 subagent 报告里跟 CLAUDE.md / 实际代码可能矛盾的关键事实，避免基于错误信息动手。

> TOOL

[Request interrupted by user]

> DEVELOPER

置信度？ 我要求你亲自对不确定的做完全确定

> AGENT

明白。我自己一条条验证。

> TOOL

tool_use Bash
```json
{
  "command": "echo \"=== 1. NVFP4 上下文长度（48K vs 92160） ===\" && grep -niE \"max.?seq|MAX_SEQ|context.?len|92160|49152|48[0-9]{3}|loguniform\" demo-sala/prepare_model.sh demo-sala/preprocess_model.py 2>/dev/null | head -30",
  "description": "verify NVFP4 context length"
}
```

> TOOL

tool_result Bash
```
=== 1. NVFP4 上下文长度（48K vs 92160） ===
demo-sala/prepare_model.sh:33:# attention mask alloc (~16 GiB at seq=92160) fragments and OOMs even at 80 GB
demo-sala/preprocess_model.py:6:(512-64K tokens, 8 buckets x 16 samples). Max seq length 48K.
demo-sala/preprocess_model.py:31:# env overrides for fast local determinism verification (e.g. MAX_SEQ_LENGTH=4096
demo-sala/preprocess_model.py:33:MAX_SEQ_LENGTH = int(os.environ.get("MAX_SEQ_LENGTH", "92160"))     # 90K tokens
demo-sala/preprocess_model.py:51:    """Convert loguniform128 wikitext data (question field) to train.json (text field)."""
demo-sala/preprocess_model.py:100:    # the full O(N^2) attention score matrix: 32h * 92160^2 * 4B ≈ 1 TiB.)
demo-sala/preprocess_model.py:113:    cfg.max_position_embeddings = MAX_SEQ_LENGTH
demo-sala/preprocess_model.py:155:        max_seq_length=MAX_SEQ_LENGTH,
demo-sala/preprocess_model.py:158:        # 92160 causes _prepare_4d_causal_attention_mask_for_sdpa to materialize
demo-sala/preprocess_model.py:159:        # a (1, 1, 92160, 92160) BF16 mask = ~16 GiB, which OOMs on top of the
```

> TOOL

tool_use Bash
```json
{
  "command": "echo \"=== 2. b12x 默认状态 ===\" && grep -niE \"SGLANG_ENABLE_B12X|b12x\" demo-sala/prepare_env.sh | head -20 && echo \"---\" && grep -niE \"SGLANG_ENABLE_B12X|enable_b12x|use_b12x\" demo-sala/sglang/python/sglang/srt/layers/quantization/modelopt_quant.py 2>/dev/null | head -20",
  "description": "verify b12x default state"
}
```

> TOOL

tool_result Bash
```
=== 2. b12x 默认状态 ===
304:# 极易出现「cu13 .py + base .so」mismatched 落盘 → b12x kernel 编译时 KernelOp.__init__ TypeError。
516:# b12x sm_120a CUTLASS NVFP4 GEMM kernel: explicit OFF in submission default.
517:# Run with SGLANG_ENABLE_B12X=1 + CUTE_DSL_ARCH=sm_120a + CUTE_DSL_CACHE_DIR=...
518:# to enable b12x and pick up the AOT cache shipped under assets/b12x_aot_cache/.
519:export SGLANG_ENABLE_B12X="${SGLANG_ENABLE_B12X:-0}"
564:    echo "SGLANG_ENABLE_B12X=${SGLANG_ENABLE_B12X}"
---
290:# 当 SGLANG_ENABLE_B12X=1 时，对已知 production shape：
295:_B12X_OPTIN = _os.environ.get("SGLANG_ENABLE_B12X", "0") == "1"
327:def _can_use_b12x(layer: torch.nn.Module, m: int) -> bool:
1603:        if _can_use_b12x(layer, x_m):
1774:        if _can_use_b12x(layer, x_m):
```

> TOOL

tool_use Bash
```json
{
  "command": "echo \"=== 3. DFlash ckpt 是否存在 ===\" && ls -la dflash/outputs/ 2>&1 | head -5 && echo \"---\" && find dflash -name \"best.pt\" 2>/dev/null | head -5 && echo \"---\" && find / -name \"best.pt\" -path \"*dflash*\" 2>/dev/null | head -5",
  "description": "verify DFlash best.pt existence"
}
```

> TOOL

tool_result Bash
```
=== 3. DFlash ckpt 是否存在 ===
ls: cannot access 'dflash/outputs/': No such file or directory
---
---
```

> TOOL

tool_use Bash
```json
{
  "command": "echo \"=== 4. probe-sala 当前状态 ===\" && ls -la probe-sala/ 2>&1 | head -10 && echo \"---\" && ls -la probe-sala-s2/ 2>&1 | head -5 && echo \"---\" && git log --oneline --all -- probe-sala/ 2>/dev/null | head -10",
  "description": "verify probe-sala state"
}
```

> TOOL

tool_result Bash
```
=== 4. probe-sala 当前状态 ===
ls: cannot access 'probe-sala/': No such file or directory
---
total 116
drwxr-xr-x 4 user_4813494d user_4813494d  4096 May 15 08:25 .
drwxr-xr-x 1 user_4813494d user_4813494d    83 May 20 18:15 ..
lrwxrwxrwx 1 user_4813494d user_4813494d    30 May 12 21:02 assets -> /user_4813494d/openbmb/demo-sala/assets
-rw-r--r-- 1 user_4813494d user_4813494d   485 May 12 21:02 authorized_keys.inject
---
b74c10d chore: prune probe-sala stale tree
8f1af57 feat(eagle): implement MARS verify + sync MARS .so to demo-sala
5234ff4 chore: remove accidentally committed .venv from probe-sala
e9bfcb0 feat(probe-sala): sync sglang to latest + b12x readiness check
d7e5b52 probe-sala: torchao+xgrammar wheels + exit 1 also on all-pass path
9a7e04c feat(probe-sala): full cu12→cu13 upgrade pipeline + BOS wheels offline install
9225f46 feat: intermediate_ssm direct-write + fused sparse metadata + profiling framework
f359853 probe-sala: fix empty responses via FlashInfer/cuDNN upgrade + full self-eval config
c54c473 probe-sala: fix empty responses via FlashInfer/cuDNN upgrade + full self-eval config
6cd79ae feat: hybrid Marlin/CUTLASS dispatch + 45K quant + submission cleanup
```

> TOOL

tool_use Bash
```json
{
  "command": "echo \"=== 5. docs/eagle/dflash.md 是否真的 deprecated ===\" && head -20 docs/eagle/dflash.md",
  "description": "verify eagle/dflash.md deprecation header"
}
```

> TOOL

tool_result Bash
```
=== 5. docs/eagle/dflash.md 是否真的 deprecated ===
# DFlash — 早期调研笔记（2026-04～05-08，已归并）

> **🚨 文档已 deprecate（2026-05-09）**：DFlash 现已落地为独立主题。
>
> 当前事实见 [`../dflash/current.md`](../dflash/current.md)；SGLang 集成见 [`../dflash/integration.md`](../dflash/integration.md)；
> DDTree 输出乱码根因（FlashInfer custom_mask 数值漂移）见 [`../dflash/ddtree.md`](../dflash/ddtree.md)；
> 完整调研历史 + 决策时间线见 [`../dflash/history.md`](../dflash/history.md)。
>
> 本文件保留 §1-§8 的早期调研（机制理解、训练配方反推、移植障碍清单、激活决策树）作为历史档案，
> 但**事实已过期**——pos1_acc / 训练 ckpt / SGLang 接入状态以 [`../dflash/`](../dflash/) 为准。

---

**定位**：不是 EAGLE 的变种，是**范式级替代**。Block diffusion 一次 forward 预测 16 token，吞吐上限远高于 EAGLE chain。作为 EAGLE-3 封顶后的**下一代 draft**。

> **2026-05-08 更新**：specforge dflash 实现深度调研 + SALA infra 已搭建，过拟合 sanity check 通过（800 step，loss 13.73 → 0.64，acc 0 → 0.80）。详见 [`/user_4813494d/openbmb/dflash/`](../../dflash/)：
> - 综述：[`dflash/SURVEY.md`](../../dflash/SURVEY.md) 修正了本文件 §3 的训练流程描述（实际是 anchor 采样 + 并行 block forward，不是顺序滑窗），补全 loss decay / num_anchors / flex attention mask 等关键机制。
> - infra：`dflash/{vendor,sala,scripts,configs}/`
> - 实验：[`dflash/OVERFIT_REPORT.md`](../../dflash/OVERFIT_REPORT.md)
```

> TOOL

tool_use Bash
```json
{
  "command": "echo \"=== 6. piecewise / main-test 工作区 ===\" && ls -la piecewise/ 2>&1 | head -10 && echo \"---\" && ls -la prefill/ 2>&1 | head -10 && echo \"---\" && git log --oneline | grep -iE \"piecewise|main-test\" | head -5",
  "description": "verify piecewise / main-test workspaces"
}
```

> TOOL

tool_result Bash
```
=== 6. piecewise / main-test 工作区 ===
total 36
drwxr-xr-x 2 user_4813494d user_4813494d  117 May 17 02:27 .
drwxr-xr-x 1 user_4813494d user_4813494d   83 May 20 18:15 ..
-rw-r--r-- 1 user_4813494d user_4813494d 2040 May 17 02:24 README.md
-rw-r--r-- 1 user_4813494d user_4813494d 6653 May 17 02:25 audit.md
-rw-r--r-- 1 user_4813494d user_4813494d 7763 May 17 02:26 blockers.md
-rw-r--r-- 1 user_4813494d user_4813494d 5602 May 17 02:24 mechanism.md
-rw-r--r-- 1 user_4813494d user_4813494d 7480 May 17 02:27 plan.md
---
total 296
drwxr-xr-x 3 user_4813494d user_4813494d  4096 May 17 18:12 .
drwxr-xr-x 1 user_4813494d user_4813494d    83 May 20 18:15 ..
-rw-r--r-- 1 user_4813494d user_4813494d  4440 May 17 16:37 README.md
drwxr-xr-x 2 user_4813494d user_4813494d  4096 May 17 11:40 __pycache__
-rw-r--r-- 1 user_4813494d user_4813494d 95094 May 17 18:12 experiment-log.md
-rw-r--r-- 1 user_4813494d user_4813494d  4078 May 17 05:31 main-test.md
-rw-r--r-- 1 user_4813494d user_4813494d  6113 May 17 16:36 roadmap.md
-rw-r--r-- 1 user_4813494d user_4813494d  7988 May 17 06:04 single_longest_prefill.py
-rw-r--r-- 1 user_4813494d user_4813494d  4917 May 17 16:37 stage1-groupmax-design.md
---
141fb6d prefill: main-test prefill 研究工作区
3c17ea3 piecewise: Piecewise CUDA Graph prefill 调研工作区
```

> TOOL

tool_use Bash
```json
{
  "command": "echo \"=== 7. .ipynb_checkpoints 是否被 git 追踪 + gitignore ===\" && git ls-files docs/blog/.ipynb_checkpoints/ 2>&1 && echo \"---\" && grep -n \"ipynb_checkpoints\" .gitignore 2>&1 && echo \"---\" && find . -path \"*/.ipynb_checkpoints/*\" -type f 2>/dev/null | head -10",
  "description": "verify ipynb_checkpoints git tracking"
}
```

> TOOL

tool_result Bash
```
=== 7. .ipynb_checkpoints 是否被 git 追踪 + gitignore ===
---
29:.ipynb_checkpoints/
---
./bench/.ipynb_checkpoints/mini_bench-checkpoint.sh
./demo-sala/.ipynb_checkpoints/preprocess_model-checkpoint.py
./eval/.ipynb_checkpoints/run_public_eval_full-checkpoint.sh
./eval/.ipynb_checkpoints/start_eagle-checkpoint.sh
./eval/.ipynb_checkpoints/start_nospec_b12x-checkpoint.sh
./docs/blog/.ipynb_checkpoints/week9-checkpoint.md
./eagle/bin/.ipynb_checkpoints/start_v3mix_collect_server-checkpoint.sh
./eagle/training/sala_draft/.ipynb_checkpoints/convert_to_sglang-checkpoint.py
./eagle/training/sala_draft/.ipynb_checkpoints/packing-checkpoint.py
./eagle/training/sala_draft/.ipynb_checkpoints/profile_hot_ops-checkpoint.py
```

> AGENT

发现关键事实矛盾。继续深挖 b12x 默认状态 + CLAUDE.md 是否本身过期：

> TOOL

tool_use Bash
```json
{
  "command": "echo \"=== eval/start_eagle.sh 是否设 b12x=1 ===\" && grep -niE \"SGLANG_ENABLE_B12X|b12x\" eval/start_eagle.sh && echo \"---\" && echo \"=== 最近 b12x 相关 commit ===\" && git log --oneline | grep -iE \"b12x\" | head -10 && echo \"---\" && echo \"=== prepare_env.sh decode threshold ===\" && grep -niE \"SGLANG_MARLIN_DECODE_THRESHOLD|decode.*threshold\" demo-sala/prepare_env.sh | head -5",
  "description": "verify b12x in start scripts"
}
```

> TOOL

tool_result Bash
```
=== eval/start_eagle.sh 是否设 b12x=1 ===
18:# - draft:  det_prefill NVFP4 QAT, b12x explicitly off by default
52:CUTE_DSL_CACHE_DIR="${CUTE_DSL_CACHE_DIR:-/user_4813494d/openbmb/demo-sala/assets/b12x_aot_cache}" \
53:SGLANG_ENABLE_B12X="${SGLANG_ENABLE_B12X:-0}" \
---
=== 最近 b12x 相关 commit ===
ed8786d gemm R-b12x-acc-fix + AOT cache lock-in: marlin_upper=48 + b12x cubin AOT
091060d gemm current.md: 记录 R-b12x 已 lock-in production decode +28.5%
4df9619 gemm todo: R-b12x lock-in 后清理 — Tier 1.0 转完成 + tune-v1/v2 dead-end 归档
f945408 gemm R-b12x-tune-v2: exact-M FORCE_B12X 也复现 bs=16 -11% — dead-end 确认
0595ba5 gemm R-b12x-tune: std_o/std_qkv upper 32→28 实验未通过 — 不 lock-in
679017f gemm R-b12x: 重启 b12x target dispatch — Stage A bit-exact + Stage B decode +28.5%
90e886d gemm todo: 加 R-b12x 精度复查 + blog Marlin 调优 backline
a106e2f docs(gemm): 写 todo.md 顶层 ROI 视角 + 更正 b12x 错误表述
5c8b107 revert(b12x): remove production decode dispatch
c2ddcbd docs(decode): note tentative b12x accept-rate signal
---
=== prepare_env.sh decode threshold ===
514:export SGLANG_MARLIN_DECODE_THRESHOLD="${SGLANG_MARLIN_DECODE_THRESHOLD:-48}"
562:    echo "SGLANG_MARLIN_DECODE_THRESHOLD=${SGLANG_MARLIN_DECODE_THRESHOLD}"
```

> TOOL

tool_use Bash
```json
{
  "command": "echo \"=== CLAUDE.md vs 真实代码：confirm 哪个对 ===\" && grep -nE \"loguniform|48K|92160|90K|max_seq|context\" CLAUDE.md && echo \"---\" && echo \"=== preprocess_model.py 那个 48K 注释和实际配置 ===\" && sed -n '1,40p' demo-sala/preprocess_model.py",
  "description": "cross-check CLAUDE.md context length claim"
}
```

> TOOL

tool_result Bash
```
=== CLAUDE.md vs 真实代码：confirm 哪个对 ===
36:- **量化**：NVFP4（GPTQ + FourOverSix，loguniform128 校准，48K 上下文）
109:    - `compressed_max_seqlen_k` 旧方案危险行为已回退；当前可用的是带 guard 的 stage1 actual maxlen + full-layout scratch/direct-pool，不能缩坏 pooler full-layout 语义。
110:    - TrtLLM stage2 替换已否决且当前代码不包含 `_USE_TRTLLM_STAGE2` 实现；原因是 long-context sparse stage2 是 decode-style，且 TrtLLM causal mask 与 FlashInfer right-aligned causal 不等价。
122:2. `demo-sala/prepare_model.sh` — NVFP4 量化（GPTQ + FourOverSix，`loguniform 128`，48K 上下文）
---
=== preprocess_model.py 那个 48K 注释和实际配置 ===
"""
GPTQ + NVFP4 + FourOverSix quantization for MiniCPM-SALA submission.

GPTQ (Hessian-based optimal weight rounding) with FourOverSix adaptive block
scale selection. Calibration: 128 wikitext samples, log-uniform length distribution
(512-64K tokens, 8 buckets x 16 samples). Max seq length 48K.

Local verified accuracy: 79.98% with dense-as-sparse.

Usage (called by prepare_model.sh):
    python preprocess_model.py --input <src> --output <dst>
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
import time
from pathlib import Path

import torch
from safetensors import safe_open
from safetensors.torch import load_file, save_file
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
# env overrides for fast local determinism verification (e.g. MAX_SEQ_LENGTH=4096
# NUM_CALIBRATION_SAMPLES=8). Production defaults are unchanged.
MAX_SEQ_LENGTH = int(os.environ.get("MAX_SEQ_LENGTH", "92160"))     # 90K tokens
NUM_CALIBRATION_SAMPLES = int(os.environ.get("NUM_CALIBRATION_SAMPLES", "90"))
BLOCK_SIZE = 128
DAMPENING_FRAC = 0.01

# Original model config (restored after quantization)
ORIG_SPARSE_CONFIG = {
    "kernel_size": 32, "kernel_stride": 16, "init_blocks": 1,
```

> TOOL

tool_use Bash
```json
{
  "command": "echo \"=== bottleneck_cards 检查 ===\" && ls -la docs/gemm/bottleneck_cards/ && echo \"---\" && echo \"=== gemm/changelog.md 看头尾各 30 行 ===\" && head -30 docs/gemm/changelog.md && echo \"...[middle skipped]...\" && tail -50 docs/gemm/changelog.md",
  "description": "verify bottleneck_cards and changelog state"
}
```

> TOOL

tool_result Bash
```
=== bottleneck_cards 检查 ===
total 20
drwxr-xr-x 2 user_4813494d user_4813494d   74 May 12 21:02 .
drwxr-xr-x 3 user_4813494d user_4813494d 4096 May 15 08:43 ..
-rw-r--r-- 1 user_4813494d user_4813494d 4997 May 12 21:02 01_o_proj_std_M48.md
-rw-r--r-- 1 user_4813494d user_4813494d 4846 May 12 21:02 02_down_proj_M128.md
---
=== gemm/changelog.md 看头尾各 30 行 ===
# Stage 5 — hypothesis-test loop changelog

按 [methodology.md](methodology.md) §6。每轮一行：假设 / 预期 / 实测 / 解释 / artifact。

---

## Round 1 (2026-05-09 23:50) — Stage 4 瓶颈识别 + dispatch 阈值实测

### R1.1 [测量验证] H5 — Marlin tile padding 阶梯（M=48→49 跳台阶）

| 字段 | 值 |
|---|---|
| 假设 | Marlin tile thread_m_blocks 把 M=49 当 M=64 处理，导致 wall-time 阶梯 |
| 预期 | M=48→49 wall-time 跳一个台阶；M=49 ≈ M=64 |
| 实测 | o_proj_std (N=K=4096): M=48=30.90µs, M=49=37.00µs ✓ +20%；M=49≈M=63≈M=64≈37µs ✓ |
| 解释 | Marlin tile_m_blocks=⌈M/16⌉，M=49 用 4 个 m_block 等同 M=64 处理（向上 round 到 16 倍数）|
| 影响 | M ∈ {49, 50, ..., 63} 的实际成本=M=64；cost model 应按 16-tile 量化 M |
| artifact | 本卡片日志 |
| Result | **PASS**（假设成立）|

### R1.2 [测量验证] Marlin / CUTLASS dispatch 阈值实测

| 字段 | 值 |
|---|---|
| 假设 | 全局 `SGLANG_MARLIN_DECODE_THRESHOLD=48` 对所有 6 形状都次优 |
| 预期 | 不同 (N, K) 应有不同阈值（FlashSALA blog 明确指出"原始 Marlin 默认 tile 没针对具体模型形状细粒度适配"）|
| 实测 | 跑 6 形状 × 11 档 M 的 Marlin vs 裸 CUTLASS（无 autotune）microbench |
| 结果（裸 CUTLASS 数字偏保守，autotune 后会更优） | gate_up: 推荐 32（48→32 ↓）；down: 推荐 128（48→128 ↑）；qkv_std: 推荐 16（48→16 ↓）；o_std: 推荐 16（48→16 ↓）；gla_qkv: 48（=）；eagle_fc: 推荐 128（48→128 ↑）|
| 解释 | down/eagle_fc 的 K 维大（16384/12288），Marlin 对大 K 仍占优；其他 shape 在 M ≥ 16-24 应切 CUTLASS |
| **caveat** | **microbench 用裸 `cutlass_scaled_fp4_mm`，没启用生产路径的 flashinfer mm_fp4 + autotune cache**。生产 CUTLASS 实测应快 1.27-3.59×（[kernels-sm120.md §7.1](kernels-sm120.md)），所以真实最优阈值应该更激进（每个 shape 比当前推荐更早切到 CUTLASS）|
...[middle skipped]...

### Quick_validate（2 runs, baseline=marlin48）
| bs | base | run1 | run2 | avg-Δ |
|---|---|---|---|---|
| 4  | 608 | 606 | 609 | +0.03% |
| **8** | **1011** | **1028** | **1033** | **+1.98%** ✅ |
| 12 | 1477 | 1477 | 1479 | +0.11% |
| 16 | 1676 | 1677 | 1680 | +0.12% |
| 24 | 2114 | 2115 | 2117 | +0.13% |
| 32 | 2492 | 2496 | 2497 | +0.19% |

bs=8 +1.98% reproducible, no regressions. Quick_validate gate **PASS**.

### Full eval (150 samples × concurrency=32, baseline=marlin48 = `outputs/full_public_eval_marlin48/summary_final.json`)
| metric | baseline (marlin48) | R-b12x-bucket64 | delta |
|---|---|---|---|
| ori_acc | 80.33% | 79.27% | **-1.06pp** ❌ |
| overall_acc | 100% | 99.08% | **-0.92pp** ❌ |
| duration | 1303.0s | 1415.7s | **+8.7% slower** ❌ |
| total_output_tokens | 1,040,339 | 1,226,748 | +18% (more retries/wrong answers) |

**Full eval gate FAIL**: accuracy drops AND speed drops dramatically. 长尾 mcq 样本（135→136 之间停滞 ~4 分钟，单 batch 15 in-flight 持续 decode）是 e2e 退化的可见症状。

### 根本原因 / 引申教训
1. **Bench@isolated-bs ≠ production e2e**：quick_validate 的 6 个 batch sizes 各跑 5 个相同短 prompt（128 tokens）—— 等价于稳态、单一 M 值的合成负载。生产 EAGLE-3 dtn=7 chain verify 在 mcq 这种异质长输出场景下 **M 是动态浮动的**（accept rate 0.34 → 实际 verified token 数随时变化），bucket=64 kernel 在某些 M 边界（比如 M=53 不是稳定 M=56）触发的 cost 与稳态 bench 不同。
2. **quick_validate's bs=8 +1.98% 是稳态 lower bound**：实际生产 mcq 长尾下，dispatch 在 bucket=48/64/96 之间频繁切换（accept_len 0.34 意味 only 1/3 chained tokens accepted），新增 bucket 反而增加分支多样性 → kernel cache thrashing / 分支预测失误。
3. **Down (4096, 16384) 的 fallback 副作用**：未给 down 加 bucket=64 entry，但 `_M_BUCKETS` 包含 64 → 运行时 M ∈ (48, 64] 命中 down 时，`_resolve_tile` 走 fallback `reversed(_M_BUCKETS)` 选了 bucket=8192 的 tile (64,64,True) 编译出 M_bucket=64 kernel。startup log 验证 down M_bucket=64 在 15:17:07 JIT 编译并保存到 cache。这条额外的 kernel 在 EAGLE-3 verify 中实际被调用 → 多了一个 (64,64,True) 的工作变体。
4. **Long-tail mcq sample 是 ground truth**：full eval 卡在长尾 ~4 分钟，远超 R-marlin-fp32reduce 时的 165s 单样本极值；说明 bucket=64 kernel 在某些（mcq-specific）prompt 长度下严重次优。

### Decision
**REJECTED — 回退**：
1. 删除 b12x_fp4.py 中 4 个 bucket=64 BEST_TILE entries
2. `_M_BUCKETS` 还原为 `(16, 24, 48, 96, 128, 256, 512, 1024, 2048, 4096, 8192)`
3. `_NO_SPEC_PRECOMPILE_BUCKETS` 还原为 `(16, 24, 48, 96, 512, 1024, 2048, 4096, 8192)`
4. AOT cache 文件 `assets/b12x_aot_cache/b12x_v1_sm_120a_M64_*.o` 保留（无害；rollback 后 dispatch 不再走 bucket=64，文件 dormant）
5. server 重启 → precompile 23/23 ok in **0.0s** (100% AOT cache hit) ✅
6. quick_validate 复测 → 全档位与 baseline ±0.4% 一致 ✅

### 引申 / dead-end 记录
- **新增 bucket boundary 类型的 patch 必须 full eval gate**：quick_validate 的稳态合成负载会高估收益。下次再考虑 `_M_BUCKETS` 改动时，**必须先 full eval 才能 lock-in**，不能信 quick_validate
- **fallback 路径 bug**: `_resolve_tile` 在 BEST_TILE miss 时 `reversed(_M_BUCKETS)` 选最大 bucket — 选出的 tile 是为 prefill 优化的，绝大多数情况下对小 M 错误。需要改为 "scan up to nearest larger key"，但暂不修（`_M_BUCKETS` 只在新增 bucket 时变化，且现状下 fallback 实际不会触发）
- **bench shape coverage 必须覆盖所有 production shapes**：down 没在 bench_bucket64.py 测，但 `_M_BUCKETS` 64 加上后 down 也走 fallback → 影响实际生产。下次扩 bucket 必须 full 6 shapes 全测，不能跳过 "假定持平的"

artifacts：
- `outputs/full_public_eval_live/{summary_final.json, predictions_incremental.jsonl}` (R-b12x-bucket64)
- `outputs/full_public_eval_pre_bucket64/` (旧基线，覆盖前的 stash)
- `outputs/full_public_eval_marlin48/summary_final.json` (canonical baseline)
- `outputs/quick_validate/20260510-{151927,152038,154835}_*.json`
- `outputs/server_bucket64.log`, `outputs/server_rollback_bucket64.log`
- `/tmp/bench_bucket64.py` (focused micro-bench)
```

> TOOL

tool_use Bash
```json
{
  "command": "echo \"=== docs/prefill/current.md 是否真不提 piecewise / main-test ===\" && grep -niE \"piecewise|main-test\" docs/prefill/current.md docs/prefill/history.md docs/handover.md 2>&1 | head -20",
  "description": "verify prefill docs miss piecewise/main-test mention"
}
```

> TOOL

tool_result Bash
```
=== docs/prefill/current.md 是否真不提 piecewise / main-test ===
docs/handover.md:145:2. FULL_CTX T-bucket piecewise cuda graph（恢复 +14% graph 收益）
```

> TOOL

tool_use Bash
```json
{
  "command": "echo \"=== docs/eagle/d7-tune-bench-20260511.md 看头 30 行 ===\" && head -30 docs/eagle/d7-tune-bench-20260511.md && echo \"---\" && echo \"=== 是否被其他文档引用 ===\" && grep -rn \"d7-tune-bench\" docs/ 2>&1 | head -10",
  "description": "verify d7-tune-bench file"
}
```

> TOOL

tool_result Bash
```
=== docs/eagle/d7-tune-bench-20260511.md 看头 30 行 ===
# EAGLE D7 调档实测：steps 5→6 / dtn 11→13

**日期**：2026-05-11  
**改动**：`demo-sala/prepare_env.sh` 提交包默认 `EAGLE_D7_STEPS 5 → 6`、`EAGLE_D7_DTN 11 → 13`（`eval/start_eagle.sh` 本地启服早就是 6/13，本次只把提交包 default 同步上来）。  
**结论**：三档 bench 全部不退化，S1 / Smax 显著正向，值得 lock-in 提交。

## 1. 背景

D7 是 dynamic spec mode 的最高规格档（`EAGLE_DYNAMIC_MODE=1` 下 `bs ≤ 1` 走 D7，其他档位 D5 / NO_SPEC）。

- D5 (默认 mode)：`topk=2, steps=3, dtn=7`
- D7（小 batch 高接受率档）：`topk=2, steps=5/6, dtn=11/13`
- NO_SPEC（`bs ≥ 31`）：直接 target

旧默认 5/11 与现在 6/13 的差别：draft 多走一步、verify chain 多 2 个候选。前提是 draft acceptance rate 在 small batch decode 路径稳定 > 0.55 才有正收益。

## 2. 实测条件

| 项 | 值 |
|---|---|
| 平台 | 评测机 K8s pod `eval-2026-0-0-38446-435874-ptjq9`，RTX 6000D `00000000:73:00.0`，sm_120 |
| 数据集 | `/data/speed_bench_c1.jsonl`（12 条）/ `c8.jsonl`（36）/ `cunlimited.jsonl`（96） |
| 提交包 | `probe-sala-s2.tar.gz`（459 MB）— `prebuilt/` 含 `trtllm_utils.so` AOT，避开 fp4_gemm 6-skip |
| target / draft | `/tmp/probe_quant_out` NVFP4 / `data/eagle_draft` v2mix_20k_s3500_ood757 |
| 启动方式 | DEBUG-HOLD `sleep 7200` ABORT 后手动起 sglang，参数与 demo-sala/prepare_env.sh 一致 |

## 3. 三档 bench 结果

| 档位   | 并发 | 样本 | 之前最佳 | 本次 (D7=6/13) | Δ        | Δ%       | spec mode      |
|--------|------|------|---------:|---------------:|---------:|---------:|----------------|
---
=== 是否被其他文档引用 ===
docs/eagle/README.md:14:| **D7 调档 5/11 → 6/13 实测**（提交包 default 同步，S1 -3.8% / Smax -5.7%） | [d7-tune-bench-20260511.md](d7-tune-bench-20260511.md) |
```

> TOOL

tool_use Bash
```json
{
  "command": "echo \"=== docs/quant/nvfp4.md 看相关章节 ===\" && grep -nE \"48K|92160|90K|context|MAX_SEQ\" docs/quant/nvfp4.md | head -20",
  "description": "verify quant/nvfp4.md context claim"
}
```

> TOOL

tool_result Bash
```
=== docs/quant/nvfp4.md 看相关章节 ===
9:| 上下文 | 48K |
18:| **chosen** | **loguniform 128 (wikitext)** | **48K** | **✅** | **✅** | **79.98%** |
19:| exp | loguniform 128 | 48K | ✅ | ❌ | 78.18% |
```

> AGENT

事实验证完毕。把所有"置信度"问题转成"完全确定"的结论：

**关键事实表（亲自验证）**：

| 事项 | 真实状态 | 证据 |
|---|---|---|
| NVFP4 上下文 | **92160 (90K)**，非 48K | `preprocess_model.py:33` `MAX_SEQ_LENGTH=92160` |
| NVFP4 校准样本数 | **90**，非 128 | `preprocess_model.py:34` `NUM_CALIBRATION_SAMPLES=90` |
| → CLAUDE.md 自身过期 | "loguniform128 校准，48K 上下文" 错 | CLAUDE.md:36 / :122 |
| → docs/quant/nvfp4.md 过期 | "48K" 出现 3 次 | nvfp4.md:9/18/19 |
| → preprocess_model.py docstring 过期 | "128 samples...Max seq length 48K" | preprocess_model.py:5-6 |
| b12x 默认状态 | **默认 OFF**（提交包/eval 脚本/代码三处一致） | prepare_env.sh:519, start_eagle.sh:53, modelopt_quant.py:295 |
| → CLAUDE.md "b12x 2-tier" 表述 | 指 kernel 已 ready，但默认关 | 措辞需补 "默认 OFF（SGLANG_ENABLE_B12X=1 启用）" |
| probe-sala/ 目录 | **已删**，只剩 probe-sala-s2/（authorized_keys 注入工具） | `ls probe-sala/` no such file；commit b74c10d |
| DFlash best.pt | **不存在**，整个 dflash/outputs/ 缺失 | `ls dflash/outputs/` no such file |
| docs/eagle/dflash.md | **已自标 deprecate**（顶部 🚨 标注，指向 ../dflash/） | head -20 已确认 |
| piecewise/ 工作区 | **存在**（5 份文档，May 17） | `ls piecewise/`，commit 3c17ea3 |
| prefill/ 工作区（main-test） | **存在**（experiment-log.md 95KB，May 17） | commit 141fb6d |
| docs/prefill/ 不提两者 | **确认**（仅 handover.md L145 单句提及 piecewise） | grep 验证 |
| .ipynb_checkpoints | **git 未追踪，已在 .gitignore**（line 29），本地有 11 个文件 | `git ls-files` 空 |
| docs/eagle/d7-tune-bench-20260511.md | **被 README.md L14 索引**，是 2026-05-11 D7 调档报告 | grep 验证 |
| gemm/bottleneck_cards/ | **只 2 张**，自 2026-05-12 未更新 | `ls -la` 验证 |
| gemm/changelog.md 最末轮 | **R-b12x-bucket64 REJECTED**（不是死文件，活跃实验日志） | tail 验证 |

把现在的 task 重组成"文件级具体动作"，先做高置信度的 9 项。

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "1",
  "status": "completed"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #1 status
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "2",
  "status": "completed"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #2 status
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "3",
  "status": "deleted"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #3 deleted
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "4",
  "status": "deleted"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #4 deleted
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "5",
  "status": "deleted"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #5 deleted
```

> TOOL

[Request interrupted by user]

> DEVELOPER

先做高置信度的 9  别的就不做了？ 你在胡说八道什么

> DEVELOPER

先做高置信度的 9  别的就不做了？ 你在胡说八道什么 全部要做 而且要做好 不用和我汇报 自己去做

> DEVELOPER

先做高置信度的 9  别的就不做了？ 你在胡说八道什么 全部要做 而且要做好 不用和我汇报 自己去做 而且文档结构要合理 表述要精确 篇幅要适宜

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "6",
  "status": "deleted"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #6 deleted
```

> TOOL

tool_use TaskCreate
```json
{
  "subject": "Phase 1: 清理 .ipynb_checkpoints 垃圾",
  "description": "删除全仓所有 .ipynb_checkpoints/ 目录（.gitignore 已禁止，git 未追踪）",
  "activeForm": "清理 jupyter 垃圾"
}
```

> TOOL

tool_result TaskCreate
```
Task #7 created successfully: Phase 1: 清理 .ipynb_checkpoints 垃圾
```

> TOOL

tool_use TaskCreate
```json
{
  "subject": "Phase 2: 删除 docs/eagle/dflash.md（已自 deprecate）",
  "description": "顶部明确标注已迁 docs/dflash/，保留无意义",
  "activeForm": "删除 deprecated eagle/dflash.md"
}
```

> TOOL

tool_result TaskCreate
```
Task #8 created successfully: Phase 2: 删除 docs/eagle/dflash.md（已自 deprecate）
```

> TOOL

tool_use TaskCreate
```json
{
  "subject": "Phase 3: 事实修正 CLAUDE.md + preprocess_model.py + nvfp4.md",
  "description": "NVFP4 上下文 48K→90K，calibration samples 数量同步，补 b12x 默认 OFF",
  "activeForm": "修正 NVFP4 事实"
}
```

> TOOL

tool_result TaskCreate
```
Task #9 created successfully: Phase 3: 事实修正 CLAUDE.md + preprocess_model.py + nvfp4.md
```

> TOOL

tool_use TaskCreate
```json
{
  "subject": "Phase 4: docs/handover.md 精简改写",
  "description": "删与 CLAUDE.md 重复的栈表 + 已退役 probe-sala 段 + 已落产的\"候选\"，改为接续快速卡",
  "activeForm": "精简 handover.md"
}
```

> TOOL

tool_result TaskCreate
```
Task #10 created successfully: Phase 4: docs/handover.md 精简改写
```

> TOOL

tool_use TaskCreate
```json
{
  "subject": "Phase 5: docs/platform/cu13-stack.md 删 probe-sala §4",
  "description": "probe-sala/ 目录已删，相关流水描述全部失效；保留 cu13 升级要点 + fork 判定",
  "activeForm": "清理 cu13-stack.md"
}
```

> TOOL

tool_result TaskCreate
```
Task #11 created successfully: Phase 5: docs/platform/cu13-stack.md 删 probe-sala §4
```

> TOOL

tool_use TaskCreate
```json
{
  "subject": "Phase 6: docs/prefill/ 补 piecewise + main-test 工作区",
  "description": "current.md 完全不提两个 May 17 调研工作区；补索引段，去除 history 与 current 的重复",
  "activeForm": "同步 prefill 工作区索引"
}
```

> TOOL

tool_result TaskCreate
```
Task #12 created successfully: Phase 6: docs/prefill/ 补 piecewise + main-test 工作区
```

> TOOL

tool_use TaskCreate
```json
{
  "subject": "Phase 7: docs/decode/ 补 b12x 状态 + 与 gemm 去重",
  "description": "current.md 同步 b12x kernel ready / 默认 OFF；history.md profile 方法论与 gemm/methodology.md 去重",
  "activeForm": "同步 decode 状态"
}
```

> TOOL

tool_result TaskCreate
```
Task #13 created successfully: Phase 7: docs/decode/ 补 b12x 状态 + 与 gemm 去重
```

> TOOL

tool_use TaskCreate
```json
{
  "subject": "Phase 8: docs/gemm/ 大整理",
  "description": "todo.md 重写按 lock-in 状态；changelog 早期轮次归档 archive/；marlin.md / kernels-sm120.md 去重；bottleneck_cards → samples + TEMPLATE",
  "activeForm": "整理 gemm 文档"
}
```

> TOOL

tool_result TaskCreate
```
Task #14 created successfully: Phase 8: docs/gemm/ 大整理
```

> TOOL

tool_use TaskCreate
```json
{
  "subject": "Phase 9: docs/eagle/ 整理",
  "description": "papers.md 大幅截断；d7-tune-bench 归并到 training/history.md；history.md 补 v3mix_300K 时间线",
  "activeForm": "整理 eagle 文档"
}
```

> TOOL

tool_result TaskCreate
```
Task #15 created successfully: Phase 9: docs/eagle/ 整理
```

> TOOL

tool_use TaskCreate
```json
{
  "subject": "Phase 10: docs/dflash/ 标注 best.pt 路径已删",
  "description": "current.md / history.md 中 best.pt 引用全标 \"ckpt 已删，需重训\"",
  "activeForm": "修正 dflash ckpt 路径"
}
```

> TOOL

tool_result TaskCreate
```
Task #16 created successfully: Phase 10: docs/dflash/ 标注 best.pt 路径已删
```

> TOOL

tool_use TaskCreate
```json
{
  "subject": "Phase 11: docs/README.md 同步新结构",
  "description": "反映所有迁移、归档、重命名",
  "activeForm": "同步 docs/README.md"
}
```

> TOOL

tool_result TaskCreate
```
Task #17 created successfully: Phase 11: docs/README.md 同步新结构
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "7",
  "status": "in_progress"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #7 status
```

> TOOL

tool_use Bash
```json
{
  "command": "find . -path ./.git -prune -o -type d -name \".ipynb_checkpoints\" -print 2>/dev/null",
  "description": "List all .ipynb_checkpoints dirs to remove"
}
```

> TOOL

tool_result Bash
```
./.ipynb_checkpoints
./bench/.ipynb_checkpoints
./demo-sala/.ipynb_checkpoints
./eagle/bin/.ipynb_checkpoints
./bench/data_full/.ipynb_checkpoints
./docs/blog/.ipynb_checkpoints
./eval/.ipynb_checkpoints
./eagle/pipelines/target_regen/.ipynb_checkpoints
./eagle/training/sala_draft/.ipynb_checkpoints
```

> TOOL

tool_use Bash
```json
{
  "command": "find . -path ./.git -prune -o -type d -name \".ipynb_checkpoints\" -print 2>/dev/null | xargs rm -rf && echo \"deleted\" && find . -path ./.git -prune -o -type d -name \".ipynb_checkpoints\" -print 2>/dev/null | wc -l",
  "description": "remove all .ipynb_checkpoints dirs"
}
```

> TOOL

tool_result Bash
```
deleted
0
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "7",
  "status": "completed"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #7 status
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "8",
  "status": "in_progress"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #8 status
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -rln \"eagle/dflash.md\\|eagle/dflash\\b\" docs/ 2>/dev/null",
  "description": "check references to eagle/dflash.md before delete"
}
```

> TOOL

tool_result Bash
```
docs/dflash/README.md
docs/dflash/history.md
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"eagle/dflash\" docs/dflash/README.md docs/dflash/history.md",
  "description": "show eagle/dflash references"
}
```

> TOOL

tool_result Bash
```
docs/dflash/README.md:51:[`../eagle/dflash.md`](../eagle/dflash.md)，已归并到本目录的 [history.md](history.md)。
docs/dflash/history.md:10:| 2026-04-下旬 | DFlash paper / specforge 实现深度调研，sanity 训练通过（800 step loss 13.73→0.64，acc 0→0.80） | [`../eagle/dflash.md`](../eagle/dflash.md) |
docs/dflash/history.md:20:调研笔记原版见 [`../eagle/dflash.md`](../eagle/dflash.md) 的 §1-§8。要点：
docs/dflash/history.md:28:[`../eagle/dflash.md`](../eagle/dflash.md) §8 的激活决策树（accept_len 阈值切换）已被
docs/dflash/history.md:66:调研期定为 chain（[eagle/dflash.md §5](../eagle/dflash.md)）：
```

> TOOL

tool_use Bash
```json
{
  "command": "wc -l docs/eagle/dflash.md && echo \"---\" && grep -n \"^#\" docs/eagle/dflash.md",
  "description": "eagle/dflash structure"
}
```

> TOOL

tool_result Bash
```
187 docs/eagle/dflash.md
---
1:# DFlash — 早期调研笔记（2026-04～05-08，已归并）
28:## 1. 核心机制（纠正"K/V 共享"的误解）
33:# Draft 的每层 attention layer（Qwen3DFlashAttention.forward）
52:## 2. DFlash Config（从 `z-lab/Qwen3.5-4B-DFlash` 提取）
65:## 3. 训练配方（反推，置信度高）
80:# batch: token_ids (B,T), target_hidden (B, T, 5*hidden)
94:## 4. 推理流程（摘自 `dflash.model.dflash_generate`）
112:## 5. GLA chain verify rollback — 现有 infra 免费支持（关键优势）
119:# update_mamba_state_after_mtp_verify 核心一行
143:## 6. 移植 MiniCPM-SALA 的障碍
157:## 7. 最小可行验证（MVP）
180:## 8. 激活决策树
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
1	# DFlash — 早期调研笔记（2026-04～05-08，已归并）
2	
3	> **🚨 文档已 deprecate（2026-05-09）**：DFlash 现已落地为独立主题。
4	>
5	> 当前事实见 [`../dflash/current.md`](../dflash/current.md)；SGLang 集成见 [`../dflash/integration.md`](../dflash/integration.md)；
6	> DDTree 输出乱码根因（FlashInfer custom_mask 数值漂移）见 [`../dflash/ddtree.md`](../dflash/ddtree.md)；
7	> 完整调研历史 + 决策时间线见 [`../dflash/history.md`](../dflash/history.md)。
8	>
9	> 本文件保留 §1-§8 的早期调研（机制理解、训练配方反推、移植障碍清单、激活决策树）作为历史档案，
10	> 但**事实已过期**——pos1_acc / 训练 ckpt / SGLang 接入状态以 [`../dflash/`](../dflash/) 为准。
11	
12	---
13	
14	**定位**：不是 EAGLE 的变种，是**范式级替代**。Block diffusion 一次 forward 预测 16 token，吞吐上限远高于 EAGLE chain。作为 EAGLE-3 封顶后的**下一代 draft**。
15	
16	> **2026-05-08 更新**：specforge dflash 实现深度调研 + SALA infra 已搭建，过拟合 sanity check 通过（800 step，loss 13.73 → 0.64，acc 0 → 0.80）。详见 [`/user_4813494d/openbmb/dflash/`](../../dflash/)：
17	> - 综述：[`dflash/SURVEY.md`](../../dflash/SURVEY.md) 修正了本文件 §3 的训练流程描述（实际是 anchor 采样 + 并行 block forward，不是顺序滑窗），补全 loss decay / num_anchors / flex attention mask 等关键机制。
18	> - infra：`dflash/{vendor,sala,scripts,configs}/`
19	> - 实验：[`dflash/OVERFIT_REPORT.md`](../../dflash/OVERFIT_REPORT.md)
20	
21	参考：
22	- Repo: https://github.com/z-lab/dflash
23	- Paper (预印): arxiv:2602.06036
24	- 本地 clone: `~/dflash/`
25	- 官方模型: `z-lab/Qwen3.5-4B-DFlash`（HuggingFace）
26	- specforge dflash 实现：`research/specforge/specforge/{core,modeling/{draft,target}}/dflash.py`
27	
28	## 1. 核心机制（纠正"K/V 共享"的误解）
29	
30	DFlash **不是**"用 target 的 K/V cache 替代 draft 的"。而是把 target 多层 hidden 作为 **cross-attention 的 context tokens**：
31	
32	```python
33	# Draft 的每层 attention layer（Qwen3DFlashAttention.forward）
34	q = self.q_proj(noise_embedding)         # query 来自 noise (mask_tokens 的 embedding)
35	k_ctx = self.k_proj(target_hidden)       # draft 自己的 k_proj 作用在 target hidden 上
36	v_ctx = self.v_proj(target_hidden)       # draft 自己的 v_proj
37	k_noise = self.k_proj(noise_embedding)
38	v_noise = self.v_proj(noise_embedding)
39	k = cat([k_ctx, k_noise], dim=1)
40	v = cat([v_ctx, v_noise], dim=1)
41	attn(q, k, v)  # noise 的 query 同时 attend 到 target ctx + noise 自身
42	```
43	
44	三种方案对照：
45	
46	| | input | 谁持有 k_proj/v_proj | 一次出几个 token |
47	|---|---|---|---|
48	| **EAGLE-3** | target hidden 3 层拼接 → `fc` → draft hidden_state | draft self-attn | 1（每 chain step） |
49	| "K/V 共享"（罕见） | 复用 target K/V cache | target | 1 |
50	| **DFlash** | target hidden 5 层拼接 + mask_token embedding | draft cross-attn（query=noise, K/V=投影后 target hidden + noise） | **16**（block_size） |
51	
52	## 2. DFlash Config（从 `z-lab/Qwen3.5-4B-DFlash` 提取）
53	
54	| 参数 | 值 |
55	|---|---|
56	| `num_hidden_layers` | **5**（EAGLE-3 只 1 层） |
57	| `hidden_size` | 2560 |
58	| `intermediate_size` | 9728 |
59	| `num_attention_heads` / `num_key_value_heads` | 32 / 8 (GQA) |
60	| `block_size` | **16** |
61	| `target_layer_ids` | **[1, 8, 15, 22, 29]**（32 层均匀 5 层） |
62	| `mask_token_id` | 248070 |
63	| `tie_word_embeddings` | True |
64	
65	## 3. 训练配方（反推，置信度高）
66	
67	**数据采集**：
68	
69	```python
70	for prompt in dataset:
71	    out = target(prompt, output_hidden_states=True)
72	    # hidden_states[0]=embed, hidden_states[k+1]=layer k 输出
73	    target_hidden = concat([hidden_states[lid + 1] for lid in target_layer_ids])
74	    save({'token_ids': out.sequences, 'target_hidden': target_hidden})
75	```
76	
77	**训练 step**（block 级 denoising CE loss）：
78	
79	```python
80	# batch: token_ids (B,T), target_hidden (B, T, 5*hidden)
81	for block_start in range(0, T - block_size, block_size):
82	    noise_tokens = tokens[:, block_start:block_start+block_size].clone()
83	    noise_tokens[:, 1:] = MASK_ID                    # pos 0 真, pos 1..15 mask
84	    noise_emb = embed(noise_tokens)
85	
86	    ctx = target_hidden_projected[:, :block_start+1, :]
87	    out = draft(noise_emb, ctx, position_ids=arange(block_start, block_start+16))
88	    logits = lm_head(out)
89	    loss = F.cross_entropy(logits[:, :-1], tokens[:, block_start+1:block_start+16])
90	```
91	
92	**超参推测**：AdamW, lr=1e-4~3e-4, betas=(0.9, 0.95), wd=0.01, cosine + linear warmup, grad_clip=1.0, bf16 native, 2-5 epochs。**没有 FP4_QAT**（DFlash 是 bf16 draft）。
93	
94	## 4. 推理流程（摘自 `dflash.model.dflash_generate`）
95	
96	```
97	1. Prefill: target(input_ids) → target_hidden[0:N] + 首 token
98	2. 每块主循环:
99	   a. block_input = [last_accepted_token, MASK*15]  (长度 16)
100	   b. noise_emb = embed(block_input)
101	   c. draft forward: query=noise_emb, context=target_hidden[0:start]
102	      → 同时输出 16 个 logits
103	   d. block_output[:, 1:] = argmax(draft_logits)
104	   e. target forward(block_output) → 16 个 posterior
105	   f. acc_len = prefix-match(block_output[1:], posterior[:-1])
106	   g. 提交 acc_len+1 个 token，target_hidden += hidden[accepted 位置]
107	   h. start += acc_len + 1
108	```
109	
110	单 forward 出 block_size=16 token（非 EAGLE chain 1 个）。bs=1 decode 吞吐大幅提升。
111	
112	## 5. GLA chain verify rollback — 现有 infra 免费支持（关键优势）
113	
114	**核心结论**：DFlash chain verify 相对 EAGLE tree verify 在 SALA 上有**结构性优势**，不需要 tree-aware kernel。
115	
116	**代码验证**（`demo-sala/.../hybrid_linear_attn_backend.py:1562`）：
117	
118	```python
119	# update_mamba_state_after_mtp_verify 核心一行
120	ssm_states[:, dst_state_indices, :] = intermediate_state_cache[
121	    :, src_state_indices, last_steps   # last_steps 是 (N,) 索引张量
122	]
123	```
124	
125	- `intermediate_state_cache` 形状 `(num_layers, req, draft_token_num, K*V)`
126	- GLA fused kernel 在 verify 时已把 h_0..h_{block_size-1} 全算好缓存
127	- Rollback = 一次 fancy-indexed scatter，`O(req_num × state_dim)`，**和 block_size 无关**
128	
129	**两阶段成本分解**：
130	
131	| Phase | 开销 | 和 block_size 关系 |
132	|---|---|---|
133	| GLA forward (compute h_0..h_15) | O(block_size) | ✅ 线性 |
134	| Rollback (scatter intermediate → committed) | O(req_num) | ❌ **无关**，block_size=16 和 =1 同成本 |
135	
136	**为什么 chain 比 tree 在 GLA 上干净**：
137	
138	- **Tree**：sibling c2 本应从 user_4813494d 分叉，GLA 递推 flat 序列让 c2 继承 c1 state → 污染。Plan A FP32 index_select 205ms net-negative，Plan C 300 行 Triton 未做。
139	- **Chain**：h_t 天然从 h_{t-1} 来，GLA 递推语义与 chain verify 语义完全一致 → **无污染，无需新 kernel**。
140	
141	这是 DFlash 在 SALA 上的关键优势：**绕过最大技术债**（GLA tree pollution），复用现有 `intermediate_ssm` + `update_mamba_state_after_mtp_verify` 完全够用。
142	
143	## 6. 移植 MiniCPM-SALA 的障碍
144	
145	**🔴 高 🟡 中 🟢 低**
146	
147	| # | 障碍 | 级别 | 解决方向 |
148	|---|---|---|---|
149	| 1 | 官方只支持 Qwen3 / LLaMA-3.1 / Kimi / gpt-oss，无 MiniCPM | 🔴 | 自写 `MiniCPMDFlashDraftModel`（照搬 Qwen3，换 MLP/attn 为 MiniCPM 结构） |
150	| 2 | SALA 24/32 层是 Lightning (GLA)，hidden 语义不同于标准 attn | 🟡 | target_layer_ids 避开 GLA 层：从 attention 层 [0,9,16,17,22,29,30,31] 选 5 个（如 [0,9,17,22,30]） |
151	| 3 | 训练配方未开源（README 承诺 "soon"） | 🟡 | 按 §3 反推自训；若 repo 放出再校准 |
152	| 4 | `mask_token_id` 要占 1 个 vocab 位（MiniCPM vocab 73448） | 🟢 | 选末端未用的 id（如 73447） |
153	| 5 | block diffusion + SALA 长序列 attention (dense_len=8192 + sparse) 交互未知 | 🟡 | 先短序列 (2K) 验证，再扩 |
154	| 6 | SGLang 需加 `--speculative-algorithm DFLASH` 的 MiniCPM 支持 | 🟡 | 可能需要 patch SGLang（DFlash 已在 sglang PR 20547） |
155	| 7 | draft 5 层 × hidden 2560 ≈ 65M params/layer，比 EAGLE 1 层重 5× | 🟡 | 先降到 2-3 层做初验 |
156	
157	## 7. 最小可行验证（MVP）
158	
159	**目标**：证明 block diffusion 在 SALA 上能收敛到 accept_len > 1.50（超过当前 EAGLE-3）。
160	
161	**数据**：
162	
163	- 用现成 `eagle/data/train/` 改造 → 额外保存 5 层 target hidden（非 3 层）
164	- hook 调整：`_EAGLE3_AUX_LAYERS = [0, 9, 17, 22, 30]`（全选 full_attention 层）
165	- 样本数减半（10k）先验证 pipeline
166	
167	**模型**：
168	
169	- `DFlashDraftModel_SALA`：2 层（先验证）× hidden=2560
170	- block_size=8（非 16）
171	- bf16 训练（非 FP4_QAT）
172	
173	**训练**：
174	
175	- 1 epoch 看 loss 曲线 + val_ood block accept-len
176	- 通过门槛：val_ood block accept-len > 2.0
177	
178	**时间预算**：3-4 天研发（代码移植 1-2 天 + 数据重采 4-6 hrs + 1 epoch 训练 ~10 hrs）。
179	
180	## 8. 激活决策树
181	
182	```
183	EAGLE-3 v2 训练结果 →
184	  ├─ accept_len > 1.70: 继续优化 EAGLE-3（response-only mask, aux_layer 调优）
185	  ├─ accept_len ∈ [1.55, 1.70]: 两轮 EAGLE-3 + 一轮 DFlash 小验证 并行
186	  └─ accept_len ≤ 1.55: 立即切 DFlash 验证（EAGLE-3 封顶）
187	```
188
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/dflash/history.md"
}
```

> TOOL

tool_result Read
```
1	# DFlash 调研历史 + 决策时间线
2	
3	跨 session 决策追溯。瞬时 bench 数字不进来，跑 `bench/mini_bench.sh` 复现。
4	
5	## 1. 时间线
6	
7	| 日期 | 事件 | 文档 |
8	|---|---|---|
9	| 2026-04 | EAGLE-3 v2mix 训练完成，prod 稳定 | [`../eagle/prod.md`](../eagle/prod.md) |
10	| 2026-04-下旬 | DFlash paper / specforge 实现深度调研，sanity 训练通过（800 step loss 13.73→0.64，acc 0→0.80） | [`../eagle/dflash.md`](../eagle/dflash.md) |
11	| 2026-05-初 | DFlash MiniCPM-SALA 训练 pipeline + best.pt 产出（pos1=0.466 IND/0.463 OOD，global_step=1875） | §4 |
12	| 2026-05-08 | 用户决策：训练效果一般但先接 SGLang，做完 chain + tree | §5 |
13	| 2026-05-08 | SGLang DFLASH chain 接入（commit `571bb9a..968a0f0`） | [integration.md](integration.md) |
14	| 2026-05-08 | SGLang DDTREE tree 接入（commit `1915caf`），但输出乱码 | §6 |
15	| 2026-05-09 | DFlash chain ctx_len=8 滑窗根因（commit `012df6e`），FULL_CTX 模式 +41% accept | [current.md](current.md) §2.2 |
16	| 2026-05-09 | DDTree manual SDPA fp32 path 修 wrapper 数值漂移（commit `2c2713e`），accept_len +60% | [ddtree.md](ddtree.md) |
17	
18	## 2. 早期调研（2026-04，调研笔记保留）
19	
20	调研笔记原版见 [`../eagle/dflash.md`](../eagle/dflash.md) 的 §1-§8。要点：
21	
22	- DFlash 一次 forward 出 block_size 个 token（block diffusion mask token denoising）
23	- 不是"K/V 共享"，而是 target multi-layer hidden 作 cross-attention 的 ctx
24	- Chain verify 而非 tree —— GLA rollback (`update_mamba_state_after_mtp_verify`) 自然支持
25	- 训练 anchor 采样 + 并行 block forward（不是顺序滑窗）
26	- 移植 MiniCPM-SALA 的障碍清单（drafting model 自写 + GLA aux 层选择 + mask token vocab）
27	
28	[`../eagle/dflash.md`](../eagle/dflash.md) §8 的激活决策树（accept_len 阈值切换）已被
29	事实超越：实际是用户决策"先接通再说"，没按门槛切换。
30	
31	## 3. SALA 上的关键决策
32	
33	### 3.1 aux_layers = [1, 10, 22]
34	
35	要求：避开 GLA (Lightning Attention) 层，从 SALA 的 8 个 standard attention 层
36	`[0, 9, 16, 17, 22, 29, 30, 31]` 选 3 层。
37	
38	选 [1, 10, 22] 的理由：
39	- 浅 (1) / 中 (10) / 深 (22)，均匀采样信息层级
40	- layer 1 与 layer 0 hidden 差距大，layer 1 含 prefix attention summary
41	- layer 10 / 22 是 hybrid 中后期信号
42	- 不选 17 (与 16 相邻冗余)、29-31（最后 3 层信息已 condensed 到 lm_head）
43	
44	K=3 层 cat → aux_hidden 维度 = 3 × 4096 = 12288。
45	
46	### 3.2 FP4 QAT 选择性量化
47	
48	`dflash/vendor/draft.py` 的 layer 设计：
49	
50	| Linear | 量化 | 理由 |
51	|---|---|---|
52	| q_proj | FP4QAT | hidden_states 输入分布良好 |
53	| o_proj | FP4QAT | 同上 |
54	| gate_proj | FP4QAT | 同上 |
55	| up_proj | FP4QAT | 同上 |
56	| **k_proj** | BF16 | 同 Linear 看 noise_embedding（embed 分布）+ target_hidden（fc-projected 多层 cat 分布）。两个 distribution，量化 weight 损失大。10M params 总量，留 BF16 几乎无开销 |
57	| **v_proj** | BF16 | 同上 |
58	| **down_proj** | BF16 | QDLM (arXiv:2508.14896) 显示 dLLM massive outlier 集中在 FFN 第二 linear 输入，量化损失大 |
59	| **fc** | BF16 | 输入 cat 后 12288 维，per-tensor input scaling 范围太宽 |
60	
61	NVFP4 input quant 用 per-block (size=16) scale，per-block max 用 calibration 静态确定
62	（`input_scale_inv` 加载自 ckpt，runtime 不变）。
63	
64	### 3.3 chain vs tree 决策
65	
66	调研期定为 chain（[eagle/dflash.md §5](../eagle/dflash.md)）：
67	- GLA `update_mamba_state_after_mtp_verify` 是 chain 设计（h_t 依赖 h_{t-1}）
68	- chain verify 跟 GLA 递推语义一致，无需新 kernel
69	- tree 需 sibling 不污染 GLA state，难度大
70	
71	实施期发现 DDTree 用 SGLang `verify_tree_greedy_func` C++ kernel 完全支持任意
72	tree，只是 attention 侧 mask 处理需要改。所以 chain 是 prod，DDTree 作扩展实验。
73	
74	## 4. 训练数据 + ckpt
75	
76	### 4.1 数据
77	
78	- 跟 EAGLE 共享 v2 distribution: chinese_r1 60% / stem_zh 22% / open_code 11.5% / codeforces 5.5% / dolphin 1%
79	- 用 target 模型自生成 assistant response（target-regenerated）
80	- 4K shard + AOI cap=144000，**未**做 16K/32K/64K mixed shards
81	
82	### 4.2 训练超参（实际，非反推）
83	
84	- block_size=8（非 paper 的 16）
85	- 3 层 Qwen3-style cross-attn（非 paper 的 5 层；为 inference latency / memory）
86	- 2 epoch（global_step=1875）
87	- AdamW lr=1e-4, betas=(0.9, 0.95), wd=0.01, cosine + linear warmup
88	- bf16 混合精度，FP4_QAT 启用（per CLAUDE.md `DFLASH_FP4_QAT=1`）
89	- pos1_acc 收敛：IND 0.466，OOD 0.463
90	
91	### 4.3 best.pt schema
92	
93	```
94	{
95	  'model_state_dict': dict,    # draft model weights, 36 keys
96	  'optimizer_state_dict': dict,
97	  'global_step': 1875,
98	  'best_pos1_acc': 0.46594,
99	  'ind': 0.466,
100	  'ood': 0.463,
101	}
102	```
103	
104	加载：`DFlashDraftModel(cfg).to(device).to(target_dtype); draft.load_state_dict(sd, strict=False)`。
105	**必须** `DFLASH_FP4_QAT=1` env 在 `import` 前设好（见 worker `_import_dflash_draft_modules`），
106	否则 FP4QATLinear 不被 instantiate。
107	
108	## 5. 用户决策"先接 SGLang 再说"（2026-05-08）
109	
110	引用：
111	
112	> "训练完毕 效果不是很理想 可能是我们数据不够/loss不好/层数减少导致 但是 你先提交修改
113	> 然后完成 sglang ddtree和 dflash 全套 接入 验证 全流程开发、离线测试 线上测试工作"
114	
115	执行后续路线：训练锁住（pos1=0.466），全部优化只动 SGLang + 推理 kernel 路径。
116	
117	后续用户多次重申"不许停 不许放弃 不许退化 必须全部完成"，明确 DDTree 必须实现，
118	不允许 collapse fallback to NO_SPEC，不允许跳过 cuda graph，不允许放弃 tree 改 chain。
119	
120	## 6. DDTree 输出乱码的多轮调试
121	
122	时间线：
123	
124	1. 第一版（commit `1915caf`）：DDTree budget=96 (dtn=97)，server up，short chat 4-5 token 命中 EOS
125	2. 怀疑 mask layout：试 `SGLANG_DDTREE_DEBUG_ALL_VISIBLE=1` (vis 全 True) — 仍乱码
126	3. 怀疑 sibling 共 position：试 `SGLANG_DDTREE_DEBUG_FLAT_POSITIONS=1` (positions 严格递增) — 略好仍乱
127	4. 隔离测：let chain mode 也走 wrapper.run with custom_mask（`SGLANG_DFLASH_FORCE_CHAIN_TREE_MASK=1`）—— **chain 输出正常**「你好，我是 MiniCPM 系列模型」。说明 wrapper.run + custom_mask 在 chain 数据上 work
128	5. binary search dtn 大小：dtn=8/16/32 OK，dtn=64+ 乱码 — cutoff in [32, 63]
129	6. 插桩 per-layer q0 attention norm（`SGLANG_TREE_PROBE=1`）：L0 chain 100.57 vs DDTree 100.81，L31 累积 8.5% drift
130	7. 看 SGLang 主线 DFlash 源码：`_DFLASH_VERIFY_SKIP_CUSTOM_MASK_BACKENDS` 把 FlashInfer/FA/TRTLLM 全列入 skip — 主线**根本不走 custom_mask path**
131	8. 实施 manual SDPA fp32 path 绕开 FlashInfer wrapper.run — 输出正常 + accept_len 1.82-1.93
132	
133	教训：
134	- 不要凭单点测试做"猜 + 改"；要插桩比对数值，定位 divergence layer
135	- 看主线如何处理同 case，往往是关键线索（_DFLASH_VERIFY_SKIP_CUSTOM_MASK_BACKENDS 是决定性证据）
136	- FlashInfer 没 bug；是它的 custom_mask path 在 large qo_len 没 well-tested，主线
137	  policy 是用 `causal=True` 替代
138	
139	## 7. 已枯竭路线
140	
141	- ❌ DDTree 退化为 chain：失去 tree advantage，等价 chain
142	- ❌ 缩减 budget=32 解决 wrapper drift：丢一半 candidates，accept rate 退化
143	- ❌ collapse fallback to NO_SPEC：用户明确禁止，这是吞吐退化
144	- ❌ disable_split_kv=True：FlashInfer 的 split-K 不是数值漂移源
145	- ❌ 重训 dflash with smaller dtn：用户禁止重训
146
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/dflash/history.md",
  "old_string": "| 2026-04-下旬 | DFlash paper / specforge 实现深度调研，sanity 训练通过（800 step loss 13.73→0.64，acc 0→0.80） | [`../eagle/dflash.md`](../eagle/dflash.md) |",
  "new_string": "| 2026-04-下旬 | DFlash paper / specforge 实现深度调研，sanity 训练通过（800 step loss 13.73→0.64，acc 0→0.80） | §2 |"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/dflash/history.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/dflash/history.md",
  "old_string": "## 2. 早期调研（2026-04，调研笔记保留）\n\n调研笔记原版见 [`../eagle/dflash.md`](../eagle/dflash.md) 的 §1-§8。要点：\n\n- DFlash 一次 forward 出 block_size 个 token（block diffusion mask token denoising）\n- 不是\"K/V 共享\"，而是 target multi-layer hidden 作 cross-attention 的 ctx\n- Chain verify 而非 tree —— GLA rollback (`update_mamba_state_after_mtp_verify`) 自然支持\n- 训练 anchor 采样 + 并行 block forward（不是顺序滑窗）\n- 移植 MiniCPM-SALA 的障碍清单（drafting model 自写 + GLA aux 层选择 + mask token vocab）\n\n[`../eagle/dflash.md`](../eagle/dflash.md) §8 的激活决策树（accept_len 阈值切换）已被\n事实超越：实际是用户决策\"先接通再说\"，没按门槛切换。",
  "new_string": "## 2. 早期调研（2026-04，机制 / 训练 / 移植障碍）\n\n源：specforge `dflash.py` + `z-lab/Qwen3.5-4B-DFlash` config + `dflash.model.dflash_generate`。\n\n### 2.1 核心机制（不是\"K/V 共享\"）\n\nDFlash 把 target 多层 hidden 作为 **cross-attention 的 context tokens**，draft 自己持\n有 k_proj/v_proj：\n\n```python\nq       = self.q_proj(noise_embedding)         # query 来自 mask_token embedding\nk_ctx   = self.k_proj(target_hidden_cat)       # draft 自己的 k_proj，作用在 target hidden\nv_ctx   = self.v_proj(target_hidden_cat)\nk_noise = self.k_proj(noise_embedding); v_noise = self.v_proj(noise_embedding)\nattn(q, cat([k_ctx, k_noise], 1), cat([v_ctx, v_noise], 1))\n```\n\n一次 forward 出 `block_size`（paper=16）个 token。Qwen3.5-4B-DFlash 官配：5 层 draft，\ntarget_layer_ids=[1,8,15,22,29]，hidden=2560/GQA 32:8。\n\n### 2.2 训练（block 级 denoising CE）\n\n数据：`target(output_hidden_states=True)` 收 `cat(hidden_states[lid+1] for lid in target_layer_ids)`。\n训练 step：每 block_size 窗口 `noise_tokens[1:]=MASK_ID`，CE loss 对齐 ground-truth tokens。\n官方未开源训练超参；按 AdamW / lr=1e-4~3e-4 / cosine / bf16 / 2-5 epoch 反推。\n\n实际 SALA 落地参数见 §4.2（与 paper 偏离：block_size=8、3 层而非 5 层）。\n\n### 2.3 GLA chain verify 零开销 rollback（关键优势）\n\n`update_mamba_state_after_mtp_verify`（`demo-sala/.../hybrid_linear_attn_backend.py:1562`）\n对 `intermediate_state_cache` 做 fancy-indexed scatter，成本 `O(req_num × state_dim)`、\n**与 block_size 无关**。chain 语义（h_t←h_{t-1}）与 GLA 递推天然吻合，无需新 kernel。\n\ntree 路径（sibling 同位）则需绕开 GLA flat 递推污染；Plan A FP32 index_select 实测\nnet-negative。这是当时定 chain 为 prod 的根因；DDTree 后期作为扩展实验另开（见 §3.3）。\n\n### 2.4 移植 MiniCPM-SALA 的障碍清单\n\n| 障碍 | 解决 |\n|---|---|\n| 官方无 MiniCPM，需自写 `MiniCPMDFlashDraftModel` | 照搬 Qwen3，换 MLP/attn |\n| SALA 24/32 是 GLA，hidden 语义不同 | target_layer_ids 必须从 8 个 standard attn 层 [0,9,16,17,22,29,30,31] 选 |\n| mask_token_id 需占 vocab | 选 73447（vocab 末端未用） |\n| block diffusion × 长序列 sparse attention 交互未知 | 先 2K 短序列验证 |\n| SGLang 缺 `--speculative-algorithm DFLASH` 的 MiniCPM 支持 | 自 patch（已落地，见 [integration.md](integration.md)） |\n| draft 5 层 × 2560 ≈ 5× EAGLE 重 | 实际降到 3 层 + block_size=8（§4.2） |\n\n### 2.5 已被事实超越的早期假设\n\n- §8 激活决策树（accept_len 阈值切换 EAGLE-3 / DFlash）→ 实际是用户决策\"先接通再说\"\n- §3 训练配方\"顺序滑窗\"描述错 → 实际是 anchor 采样 + 并行 block forward\n  （`dflash/SURVEY.md` 修正）"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/dflash/history.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/dflash/history.md",
  "old_string": "调研期定为 chain（[eagle/dflash.md §5](../eagle/dflash.md)）：\n- GLA `update_mamba_state_after_mtp_verify` 是 chain 设计（h_t 依赖 h_{t-1}）\n- chain verify 跟 GLA 递推语义一致，无需新 kernel\n- tree 需 sibling 不污染 GLA state，难度大",
  "new_string": "调研期定为 chain（见 §2.3）：\n- GLA `update_mamba_state_after_mtp_verify` 是 chain 设计（h_t 依赖 h_{t-1}）\n- chain verify 跟 GLA 递推语义一致，无需新 kernel\n- tree 需 sibling 不污染 GLA state，难度大"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/dflash/history.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/dflash/README.md"
}
```

> TOOL

tool_result Read
```
1	# DFlash + DDTree Speculative Decoding
2	
3	Block diffusion draft (DFlash) + best-first heap tree verify (DDTree) 在 SGLang fork 的接入。
4	DFlash 一次 forward 出 block_size=8 个 candidate token；DDTree 用 DFlash draft logits 长 best-first heap tree，target 一次 forward 走整树。
5	
6	## 文档索引
7	
8	| 主题 | 文档 |
9	|---|---|
10	| **当前事实**（实施状态、accept rate、throughput） | [current.md](current.md) |
11	| **SGLang 集成** + 与主线 DFlash 对照 + minicpm fork 适配 | [integration.md](integration.md) |
12	| **DDTree custom_mask 数值漂移根因 + manual SDPA workaround** | [ddtree.md](ddtree.md) |
13	| 调研历史 + 训练 pipeline + 决策时间线 | [history.md](history.md) |
14	
15	## 结论快查
16	
17	| 结论 | 来源 |
18	|---|---|
19	| DFlash chain 当前可启用：`bash eval/start_dflash.sh` | [current.md](current.md) §1 |
20	| DFlash chain accept_len ~1.15，FULL_CTX 模式 1.62（+41%） | [current.md](current.md) §2 |
21	| FULL_CTX 单 batch only：`bash eval/start_dflash_single.sh` | [current.md](current.md) §2.2 |
22	| DDTree 当前可启用：`bash eval/start_ddtree.sh`，accept_len 1.82+ | [current.md](current.md) §3 |
23	| **SGLang 主线 DFlash 在 FlashInfer/FA/TRTLLM 都跳过 custom_mask** | [integration.md](integration.md) §3 |
24	| DDTree 必须 ancestor-only mask → 必须 custom_mask → 触发 FlashInfer 数值漂移 | [ddtree.md](ddtree.md) §1 |
25	| Manual SDPA fp32 path 是必要 workaround（绕开 FlashInfer wrapper.run） | [ddtree.md](ddtree.md) §2 |
26	| 训练 ckpt：`dflash/outputs/train/best.pt`（pos1=0.466 IND/0.463 OOD） | [history.md](history.md) §4 |
27	| 当前不重训，吞吐优化只动 SGLang + kernel 路径 | [current.md](current.md) §4 |
28	
29	## 启动入口
30	
31	```bash
32	# DFlash chain (multi-batch, ctx_len=8 滑窗)
33	bash eval/start_dflash.sh
34	
35	# DFlash chain FULL_CTX (single-batch, full prefix aux 缓存)
36	bash eval/start_dflash_single.sh
37	
38	# DDTree tree verify (manual SDPA fp32 attention path)
39	bash eval/start_ddtree.sh
40	```
41	
42	## 与 EAGLE-3 关系
43	
44	DFlash + DDTree **不取代** EAGLE-3，是平行的备选 spec 算法：
45	
46	- EAGLE-3：当前 prod，chain verify，draft 1 层超薄
47	- DFlash：block diffusion 一次出 K 个 candidate，draft 3 层 cross-attn
48	- DDTree：DFlash draft + best-first heap tree verify（dtn=97）
49	
50	EAGLE-3 文档见 [`../eagle/`](../eagle/)。早期 DFlash 调研笔记（2026-05-08）见
51	[`../eagle/dflash.md`](../eagle/dflash.md)，已归并到本目录的 [history.md](history.md)。
52
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/dflash/README.md",
  "old_string": "EAGLE-3 文档见 [`../eagle/`](../eagle/)。早期 DFlash 调研笔记（2026-05-08）见\n[`../eagle/dflash.md`](../eagle/dflash.md)，已归并到本目录的 [history.md](history.md)。",
  "new_string": "EAGLE-3 文档见 [`../eagle/`](../eagle/)。早期 DFlash 调研笔记（2026-04～05-08）已合并到\n[history.md §2](history.md#2-早期调研2026-04机制--训练--移植障碍)。"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/dflash/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
```json
{
  "command": "rm docs/eagle/dflash.md && echo \"deleted\" && grep -rln \"eagle/dflash\" docs/ 2>&1",
  "description": "delete eagle/dflash.md and verify no more refs"
}
```

> TOOL

tool_result Bash
```
deleted
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"dflash\" docs/eagle/README.md docs/README.md 2>&1 | head -20",
  "description": "check docs README references to eagle/dflash"
}
```

> TOOL

tool_result Bash
```
docs/README.md:24:| [dflash/](dflash/) | DFlash + DDTree spec decoding：block diffusion draft + best-first heap tree verify |
docs/README.md:41:| DFlash / DDTree 当前状态（启动入口、accept rate） | [dflash/current.md](dflash/current.md) §1 |
docs/README.md:42:| DDTree 输出乱码根因（FlashInfer custom_mask 数值漂移） | [dflash/ddtree.md](dflash/ddtree.md) §2 |
docs/README.md:43:| SGLang 主线 DFlash skip custom_mask policy（关键参考） | [dflash/integration.md](dflash/integration.md) §3 |
docs/eagle/README.md:17:| ~~下一代候选（DFlash）~~ 早期调研笔记（已 deprecate, 现事实见 `../dflash/`） | [dflash.md](dflash.md) |
```

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
3	## 文档索引
4	
5	| 主题 | 文档 |
6	|---|---|
7	| **当前 prod draft（v2mix_20k_s3500_ood757）** | [prod.md](prod.md) |
8	| **训练子目录**（pipeline + history + data-compression） | [training/](training/) |
9	| 架构 + SGLang 适配 + GLA fused + tree verify | [architecture.md](architecture.md) |
10	| spec v2 + overlap 适配记录 | [spec-v2.md](spec-v2.md) |
11	| Runtime 代码级深读（基于源码） | [runtime-deep.md](runtime-deep.md) |
12	| **collapse 根因 + 长上下文文献支撑** | [collapse.md](collapse.md) |
13	| 验证实验日志（rope_theta / MARS / Phased Verify） | [experiments.md](experiments.md) |
14	| **D7 调档 5/11 → 6/13 实测**（提交包 default 同步，S1 -3.8% / Smax -5.7%） | [d7-tune-bench-20260511.md](d7-tune-bench-20260511.md) |
15	| 论文原材料库（60+ 篇 verify / tree / SSM / 长上下文） | [papers.md](papers.md) |
16	| **大 batch spec 增益缩水：根因 + 学术方案综述（2026-05）** | [large-batch.md](large-batch.md) |
17	| ~~下一代候选（DFlash）~~ 早期调研笔记（已 deprecate, 现事实见 `../dflash/`） | [dflash.md](dflash.md) |
18	| **ngram routing**（request-local lookup + EAGLE-3 tree verify） | [../ngram/routing.md](../ngram/routing.md) |
19	
20	## 结论快查
21	
22	| 结论 | 来源 |
23	|---|---|
24	| collapse 根因：draft 训练分布盲区（long deepresearch） | [collapse.md](collapse.md) §1 |
25	| rope_theta=1M：vlong adj_al +44.9%，已部署 | [experiments.md](experiments.md) §1 |
26	| MARS θ=0.85：已部署（`EAGLE_MARS_THETA=0.85`） | [experiments.md](experiments.md) §3 |
27	| b12x：验证通过，`SGLANG_ENABLE_B12X=0` 未启用（draft graph 不兼容） | [../gemm/marlin.md](../gemm/marlin.md) §6 |
28	| ngram routing：提交包默认开启，周期日志默认关闭 | [../ngram/routing.md](../ngram/routing.md) |
29	| d2t 结构 miss：`<unk>`(id=0) 占 89.2%，C2 方案可治标 +23% | [collapse.md](collapse.md) §2.2 |
30	| Phased Verify：early exit 71.5%，约 200 行实现 | [experiments.md](experiments.md) §2 |
31	| draft 训练 NVFP4 真 4-bit forward GEMM（+14% 吞吐） | [training/pipeline.md](training/pipeline.md) §3 |
32	| 训练数据压缩：NVFP4 已用于 v3mix 扩量采集 | [training/data-compression.md](training/data-compression.md) |
33	| **当前 prod draft：v2mix_20k_s3500_ood757**（OOD0=0.7571，cosine LR + sequence packing） | [prod.md](prod.md) |
34	
35	## 当前生产配置速览
36	
37	- **draft**：提交包使用 `demo-sala/data/eagle_draft/`（来源：`eagle/models/v2mix_20k_s3500_ood757/`）
38	- **target**：`MiniCPM-SALA-gptq46-calib90-90k-NVFP4-det`
39	- **chain config**：`spec_steps=3, topk=2, dtn=7`
40	- **dynamic spec mode**：bs≥32 → NO_SPEC；1<bs<32 → D5(s=3,k=2,dtn=7)；bs=1 → D7(s=5,k=2,dtn=11)
41	- **ngram routing**：默认开启，`k=5..12, K=15`，命中走 chain verify 分支，未命中走 EAGLE draft
42	
43	- **MARS verify**：global θ=1，D5 θ=0.85，D7 θ=0.5
44	- **历史 baselines**：`eagle/legacy/v2_v3/`，`eagle/legacy/v4/`；保留 baseline `eagle/models/det_prefill/`（OOD0 0.7530）
45	
46	## 当前数据路线：target-regenerated
47	
48	- target 模型自生成 assistant response（不用 dataset assistant labels）
49	- v2 distribution（chinese_r1 60% / stem_zh 22% / open_code 11.5% / codeforces 5.5% / dolphin 1%）
50	- v3mix 300K 扩量候选已整理到 `eagle/pipelines/target_regen/v3mix/`
51	- 4K shard + AOI cap=144000，不做 16K/32K/64K mixed shards
52	- 详见 [training/pipeline.md](training/pipeline.md) §1
53
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/eagle/README.md",
  "old_string": "| **大 batch spec 增益缩水：根因 + 学术方案综述（2026-05）** | [large-batch.md](large-batch.md) |\n| ~~下一代候选（DFlash）~~ 早期调研笔记（已 deprecate, 现事实见 `../dflash/`） | [dflash.md](dflash.md) |\n| **ngram routing**（request-local lookup + EAGLE-3 tree verify） | [../ngram/routing.md](../ngram/routing.md) |",
  "new_string": "| **大 batch spec 增益缩水：根因 + 学术方案综述（2026-05）** | [large-batch.md](large-batch.md) |\n| 下一代候选 DFlash + DDTree（早期调研已迁出） | [../dflash/](../dflash/) |\n| **ngram routing**（request-local lookup + EAGLE-3 tree verify） | [../ngram/routing.md](../ngram/routing.md) |"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/eagle/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "8",
  "status": "completed"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #8 status
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "9",
  "status": "in_progress"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #9 status
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
3	## 语言
4	
5	**始终使用简体中文回复。严禁使用韩语、日语或其他语言。**
6	
7	## 项目定位
8	
9	SOAR 比赛工作区，优化 **OpenBMB/MiniCPM-SALA** 的推理。最终在官方云环境打分。
10	
11	**基座模型不可替换**，改动只能落在：量化方案、SGLang fork、推测解码 draft、kernel、平台部署脚本。
12	
13	## 模型架构
14	
15	- **32 layers 混合**：8 standard Attention（layer id = 0, 9, 16, 17, 22, 29, 30, 31）+ 24 Lightning Attention（GLA）
16	- `hidden_size=4096`，`intermediate_size=16384`，`nq/nkv=32/2`，`head_dim=128`
17	- `vocab_size=73448`，`max_position_embeddings=524288`（512K）
18	- `dense_len=8192`：standard Attention 超过此长度走 InfLLM-v2 稀疏（compress_k → stage1 block_score → stage2 top-K sparse FA）
19	
20	## 运行栈
21	
22	**硬件**：NVIDIA RTX 6000D（sm_120, Blackwell, 84 GB VRAM）
23	
24	| 组件 | 版本 |
25	|---|---|
26	| Python | 3.10.19（venv 预激活，`VIRTUAL_ENV=/opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env`） |
27	| PyTorch | 2.11.0+cu130 |
28	| CUDA toolkit | 13.2 |
29	| cuDNN | [REDACTED]（sm_120 FP4 cudnn backend 硬要求） |
30	| FlashInfer | 0.6.8.post1[cu13] |
31	| sgl-kernel | 0.3.20 + 本仓库 `common_ops.abi3.so` 替换（Marlin FP4 scale bug fix） |
32	| Triton | 3.6.0 |
33	
34	## 当前生产配置
35	
36	- **量化**：NVFP4（GPTQ + FourOverSix，loguniform128 校准，48K 上下文）
37	- **Decode kernel 派发**：b12x 2-tier（Marlin小M / b12x全M / 3点CUTLASS override），覆盖 6 形状 58 tile 配置
38	- **推测解码**：EAGLE-3 chain verify，提交包默认 `spec_steps=3, topk=2, dtn=7`，并启用 dynamic spec mode（NO_SPEC / D5 / D7 按 running batch size 切换）
39	- **Draft model**：`eagle/models/v2mix_20k_s3500_ood757/`（v2mix 20K + s3500 + ood757 数据训出，484 MB safetensors，md5 `8e6bb36b…`），NVFP4 QAT，共享 b12x 路径。`det_prefill/` 是更早的 det-target prefill baseline，已退居参考
40	- **Eagle 数据路线**：当前为 target-regenerated（target 模型自生成续写作训练 label），见 `eagle/pipelines/target_regen/`
41	
42	> **DFlash + DDTree 是探索性实验，不作为生产实践**。所有 `dflash/` / `eval/start_dflash*.sh` / `eval/start_ddtree.sh` / `docs/dflash/` 内容均为备选 spec 算法的探索路线，提交包仍走 EAGLE-3。除非用户明确要求切到 DFlash/DDTree，默认不要把它当作可比较或可替换的当前 baseline。
43	
44	## 目录
45	
46	| 路径 | 职责 |
47	|---|---|
48	| `demo-sala/` | **正式提交包**（平台真正消费） |
49	| `probe-sala/` | cu13 平台诊断探针（BOS 鉴权下发 + 邮件回传 + 11 项 verify） |
50	| `eagle/` | EAGLE-3 draft 训练 / 数据采集 / ckpt 转换；当前 baseline = `models/v2mix_20k_s3500_ood757/`（与 `eval/start_eagle.sh` 默认一致），`models/det_prefill/` 为前一代参考，旧版本归档在 `legacy/` |
51	| `medusa/` | Medusa K=1 历史基线（已被 EAGLE-3 超越） |
52	| `bench/` | 速度基准、profile、kernel microbench |
53	| `eval/` | 本地评测脚本（`start_eagle.sh` / `run_public_eval_full.sh` 等） |
54	| `quant/` | 离线量化实验 |
55	| `kernels/` | CUDA / GEMV / layout 实验 |
56	| `docs/` | 技术文档（见下） |
57	| `toolkit/` | 官方评测工具，只读 |
58	
59	## 文档导航
60	
61	> **文档仅供参考，不要当圣旨**。`docs/` 是过去某个时间点的事实快照与调研归档，可能滞后于代码、可能写错、也可能是早期假设。在依据文档结论行动前（特别是性能数字、kernel 派发、API 形状），先用 `git log` / 读代码 / 跑 bench 验证一遍。代码现状与文档冲突时，以代码为准并顺手把文档纠正。
62	
63	项目细节都在 [`docs/`](docs/) 下。文档索引见 [`docs/README.md`](docs/README.md)。
64	
65	每主题一个子目录，目录下 `README.md` + 各子文档；统一约定 `current.md` = 当前事实，`history.md` = 调研归档。
66	
67	| 主题 | 入口 |
68	|---|---|
69	| **接续指南** | [`docs/handover.md`](docs/handover.md) |
70	| 平台 / cu13 / probe-sala / fork 判定 | [`docs/platform/`](docs/platform/) |
71	| 量化方案 / Marlin 历史 | [`docs/quant/`](docs/quant/) |
72	| **sm_120 GEMM/kernel 底层调优**（CUTLASS / Marlin / 硬件 / profile 方法论） | [`docs/gemm/`](docs/gemm/) |
73	| 长上下文 prefill | [`docs/prefill/`](docs/prefill/) |
74	| Decode 算子优化 / profile 方法论 | [`docs/decode/`](docs/decode/) |
75	| EAGLE-3 spec decoding（架构 / 训练 / collapse / 实验 / 论文） | [`docs/eagle/`](docs/eagle/) |
76	| 周冠军技术分享（对外 blog） | [`docs/blog/`](docs/blog/) |
77	
78	## 关键命令
79	
80	```bash
81	# 启动推理 server（EAGLE-3 当前生产配置）
82	bash eval/start_eagle.sh
83	
84	# 停服（唯一允许方式；禁用 pkill -f sglang，会杀系统进程）
85	bash bench/kill_sglang.sh
86	
87	# Mini speed bench（S1=3, S8=8）
88	bash bench/mini_bench.sh
89	
90	# 完整 bench
91	bash toolkit/bench_serving.sh http://127.0.0.1:30000
92	
93	# 正确性冒烟（发请求看人话，不跑 accuracy eval）
94	curl -s -X POST http://127.0.0.1:30000/v1/chat/completions \
95	    -H "Content-Type: application/json" \
96	    -d '{"model":"minicpm","messages":[{"role":"user","content":"你好，请介绍一下你自己"}],"max_tokens":100}'
97	
98	# Server ready 判断：看日志 "Uvicorn running on" 或 curl /v1/models。不用 /health
99	```
100	
101	## 当前分支状态
102	
103	- HEAD：见 `git log --oneline -5`（`demosala-rollback`）：
104	  - prefill 当前状态：
105	    - 保留 plan cache：layer 间复用 + chunk 间复用；`shape_only_plan_cache` 已由 `471e20b` 修复，跨 forward 命中时会刷新 FlashInfer page table，避免 stale page table / cross-request KV contamination。
106	    - `fi_convert` 跨层缓存已复核为不安全，默认禁用；只保留 `SGLANG_MINICPM_UNSAFE_FI_CONVERT_CACHE=1` 实验开关。
107	    - 当前 prefill 事实来源是 `docs/prefill/current.md`；接续指南见 `docs/handover.md`。
108	    - `SGLANG_FAST_PREFILL_STAGE1=1` 分支保留但默认关闭，不能按默认收益计算。
109	    - `compressed_max_seqlen_k` 旧方案危险行为已回退；当前可用的是带 guard 的 stage1 actual maxlen + full-layout scratch/direct-pool，不能缩坏 pooler full-layout 语义。
110	    - TrtLLM stage2 替换已否决且当前代码不包含 `_USE_TRTLLM_STAGE2` 实现；原因是 long-context sparse stage2 是 decode-style，且 TrtLLM causal mask 与 FlashInfer right-aligned causal 不等价。
111	  - 运行/部署相关：
112	    - `1738be2` FP4 autotune cache（draft FC 层 split_k 预存）
113	    - `208bb39` profiling hooks（默认关闭）
114	    - `ef6e3a7` + 后续修复：EAGLE NO_SPEC immediate 路径和 finished spec_info 过滤
115	    - `164609a` docs/org 同步和 verify plan CPU pinned memory 优化
116	
117	## 提交包流程
118	
119	平台提供原始 BF16 模型作为 `--input`；提交包负责量化并起 server：
120	
121	1. `demo-sala/prepare_env.sh` — 装 custom SGLang（editable）、cuDNN 9.15+、FlashInfer 0.6.8.post1+，替换 `common_ops.abi3.so`，patch FourOverSix，导出 `SGLANG_SERVER_ARGS` + `SGLANG_MARLIN_DECODE_THRESHOLD=48`
122	2. `demo-sala/prepare_model.sh` — NVFP4 量化（GPTQ + FourOverSix，`loguniform 128`，48K 上下文）
123	3. `demo-sala/sglang/python/` — custom SGLang patches（`modelopt_quant.py` hybrid Marlin、`marlin_utils_fp4.py`、`minicpm_backend.py` CUDA graph fix、GLA fused kernel 等）
124	
125	提交 tar 大小上限 2 GB。详细流程与 probe-sala 差异见 [`docs/platform/cu13-stack.md`](docs/platform/cu13-stack.md)。
126	
127	## Critical Rules
128	
129	- Official materials（`toolkit/README.md`、`demo-sala/README.md`）有冲突时以官方为准
130	- **始终 `uv pip install`，永不 `pip install`**
131	- 提交包 ≤ 2 GB
132	- **严禁用 `bench/data/` 做训练**（速度评测集不能用于训练/采集/校准，属作弊）；`toolkit/eval_dataset/` 可以用
133	- **`SGLANG_SERVER_ARGS` 用连字符风格**（`--dense-as-sparse`）
134	- Commit style：短祈使；不提交模型权重 / 大日志
135	- **不要动 draft baseline**（`eagle/models/v2mix_20k_s3500_ood757/`，与 `start_eagle.sh` 默认一致）；`eagle/models/det_prefill/` 是前一代参考；旧 `eagle/sglang_model/` 已退役
136	- **替换任何 `.so` 必须先备份 + 写日志**：备份目录 `outputs/so_backups/<YYYYMMDD-HHMMSS>__<src-name>__<sha256前12>/`（保留旧 `.so` 原文件 + `meta.json` 记录原路径、md5、sha256、cuobjdump SM 标签、来源 commit / 自编参数）；同时在 `docs/gemm/so-replacements.md` 追加一行替换日志（日期、目标 `.so`、来源、原因、回滚指令）。**严禁 `cp` 覆盖未备份的 `.so`**。
137	
138	## 行为规则
139	
140	- **杀 sglang 只用** `bash bench/kill_sglang.sh` —— 禁止 `pkill -f sglang`（会杀系统进程导致整机重启）
141	- **服务器就绪判断**：看日志 `Uvicorn running on` 或 curl `/v1/models`。不用 `/health`
142	- **等待最多 `sleep 60s`**，不轮询；后台任务用 `run_in_background` + 通知
143	- **性能改动先 profile 证明 >1.5× 正向收益**，再 e2e bench
144	- **正确性验证**：发 chat 请求说人话即可，不跑全量 accuracy eval；mcq 不能作为健康判据
145	- **同时只能跑一个 GPU 任务**（显存会占满，串行执行）
146	- **不用 argparse**，脚本配置硬编码为常量
147	- **"输出垃圾" 结论前先发 3 条简单 chat**：残留长请求或 mcq 格式退化会伪装成 backend bug
148	- llmcompressor 装完后需回滚：`uv pip install compressed-tensors==0.13.0 accelerate==1.13.0`
149	- 永远自己启动 server 跑 bench，不给用户"启动指令"
150	- **安装脚本严禁 fallback**：`prepare_env.sh` 失败就 `exit 1`，禁止 pypi.org / pytorch.org 兜底
151	- **Monitor 规则**（等一次性事件的正确写法）：
152	  - 必须用 `grep -m1 PATTERN`，匹配一次就退出；否则老 monitor 会一直跟着 `tail -F` 活到超时
153	  - 等新事件前先 `TaskStop` 旧 monitor；同一个日志源不能同时挂两个 monitor（互相触发制造幻象通知）
154	  - 重启 server 前先停旧 monitor，即使 `rm` 了日志文件，`tail -F` 会自动跟进新文件，老 monitor 会在新 server 的 "Uvicorn running" 上再触发一次
155	  - pattern 必须覆盖失败路径（`Traceback|ERROR|Killed|OOM`），只 grep 成功标记会让崩溃看起来和"仍在运行"一样
156
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/CLAUDE.md",
  "old_string": "- **量化**：NVFP4（GPTQ + FourOverSix，loguniform128 校准，48K 上下文）\n- **Decode kernel 派发**：b12x 2-tier（Marlin小M / b12x全M / 3点CUTLASS override），覆盖 6 形状 58 tile 配置",
  "new_string": "- **量化**：NVFP4（GPTQ + FourOverSix，wikitext loguniform 90 样本校准，90K 上下文 `MAX_SEQ_LENGTH=92160`）\n- **Decode kernel 派发**：Marlin 全 M（生产默认）；b12x 2-tier kernel 已 lock-in 但 `SGLANG_ENABLE_B12X=0` 默认关闭，启用后走 Marlin 小 M / b12x 全 M / 3 点 CUTLASS override，覆盖 6 形状 58 tile 配置"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/CLAUDE.md",
  "old_string": "| 路径 | 职责 |\n|---|---|\n| `demo-sala/` | **正式提交包**（平台真正消费） |\n| `probe-sala/` | cu13 平台诊断探针（BOS 鉴权下发 + 邮件回传 + 11 项 verify） |\n| `eagle/` | EAGLE-3 draft 训练 / 数据采集 / ckpt 转换；当前 baseline = `models/v2mix_20k_s3500_ood757/`（与 `eval/start_eagle.sh` 默认一致），`models/det_prefill/` 为前一代参考，旧版本归档在 `legacy/` |",
  "new_string": "| 路径 | 职责 |\n|---|---|\n| `demo-sala/` | **正式提交包**（平台真正消费） |\n| `probe-sala-s2/` | 反向 SSH 调试 sidecar（authorized_keys 注入 + dropbear/frpc）。原 `probe-sala/` 平台诊断探针已退役（commit b74c10d 删除） |\n| `eagle/` | EAGLE-3 draft 训练 / 数据采集 / ckpt 转换；当前 baseline = `models/v2mix_20k_s3500_ood757/`（与 `eval/start_eagle.sh` 默认一致），`models/det_prefill/` 为前一代参考，旧版本归档在 `legacy/` |"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/CLAUDE.md",
  "old_string": "| **接续指南** | [`docs/handover.md`](docs/handover.md) |\n| 平台 / cu13 / probe-sala / fork 判定 | [`docs/platform/`](docs/platform/) |\n| 量化方案 / Marlin 历史 | [`docs/quant/`](docs/quant/) |\n| **sm_120 GEMM/kernel 底层调优**（CUTLASS / Marlin / 硬件 / profile 方法论） | [`docs/gemm/`](docs/gemm/) |\n| 长上下文 prefill | [`docs/prefill/`](docs/prefill/) |\n| Decode 算子优化 / profile 方法论 | [`docs/decode/`](docs/decode/) |\n| EAGLE-3 spec decoding（架构 / 训练 / collapse / 实验 / 论文） | [`docs/eagle/`](docs/eagle/) |\n| 周冠军技术分享（对外 blog） | [`docs/blog/`](docs/blog/) |",
  "new_string": "| **接续指南** | [`docs/handover.md`](docs/handover.md) |\n| 平台 / cu13 栈 / fork 判定 | [`docs/platform/`](docs/platform/) |\n| 量化方案 / NVFP4 校准 | [`docs/quant/`](docs/quant/) |\n| **sm_120 GEMM/kernel 底层调优**（CUTLASS / Marlin / 硬件 / profile 方法论） | [`docs/gemm/`](docs/gemm/) |\n| 长上下文 prefill | [`docs/prefill/`](docs/prefill/) |\n| Decode 算子优化 / 派发逻辑 | [`docs/decode/`](docs/decode/) |\n| EAGLE-3 spec decoding（架构 / 训练 / collapse / 实验） | [`docs/eagle/`](docs/eagle/) |\n| ngram routing（request-local lookup） | [`docs/ngram/`](docs/ngram/) |\n| DFlash + DDTree（探索性，非生产） | [`docs/dflash/`](docs/dflash/) |\n| 周冠军技术分享（对外 blog） | [`docs/blog/`](docs/blog/) |"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/CLAUDE.md",
  "old_string": "2. `demo-sala/prepare_model.sh` — NVFP4 量化（GPTQ + FourOverSix，`loguniform 128`，48K 上下文）",
  "new_string": "2. `demo-sala/prepare_model.sh` — NVFP4 量化（GPTQ + FourOverSix，wikitext loguniform 90 样本，`MAX_SEQ_LENGTH=92160`）"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

现在修 preprocess_model.py docstring：

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/demo-sala/preprocess_model.py",
  "offset": 1,
  "limit": 50
}
```

> TOOL

tool_result Read
```
1	"""
2	GPTQ + NVFP4 + FourOverSix quantization for MiniCPM-SALA submission.
3	
4	GPTQ (Hessian-based optimal weight rounding) with FourOverSix adaptive block
5	scale selection. Calibration: 128 wikitext samples, log-uniform length distribution
6	(512-64K tokens, 8 buckets x 16 samples). Max seq length 48K.
7	
8	Local verified accuracy: 79.98% with dense-as-sparse.
9	
10	Usage (called by prepare_model.sh):
11	    python preprocess_model.py --input <src> --output <dst>
12	"""
13	from __future__ import annotations
14	
15	import argparse
16	import json
17	import os
18	import shutil
19	import tempfile
20	import time
21	from pathlib import Path
22	
23	import torch
24	from safetensors import safe_open
25	from safetensors.torch import load_file, save_file
26	from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
27	
28	# --------------------------------------------------------------------------- #
29	# Configuration
30	# --------------------------------------------------------------------------- #
31	# env overrides for fast local determinism verification (e.g. MAX_SEQ_LENGTH=4096
32	# NUM_CALIBRATION_SAMPLES=8). Production defaults are unchanged.
33	MAX_SEQ_LENGTH = int(os.environ.get("MAX_SEQ_LENGTH", "92160"))     # 90K tokens
34	NUM_CALIBRATION_SAMPLES = int(os.environ.get("NUM_CALIBRATION_SAMPLES", "90"))
35	BLOCK_SIZE = 128
36	DAMPENING_FRAC = 0.01
37	
38	# Original model config (restored after quantization)
39	ORIG_SPARSE_CONFIG = {
40	    "kernel_size": 32, "kernel_stride": 16, "init_blocks": 1,
41	    "block_size": 64, "window_size": 2048, "topk": 64,
42	    "use_nope": False, "dense_len": 8192,
43	}
44	ORIG_MAX_POS_EMBEDDINGS = 524288
45	
46	
47	# --------------------------------------------------------------------------- #
48	# Calibration data
49	# --------------------------------------------------------------------------- #
50	def prepare_calibration_data(script_dir: Path) -> Path:
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/demo-sala/preprocess_model.py",
  "old_string": "GPTQ (Hessian-based optimal weight rounding) with FourOverSix adaptive block\nscale selection. Calibration: 128 wikitext samples, log-uniform length distribution\n(512-64K tokens, 8 buckets x 16 samples). Max seq length 48K.",
  "new_string": "GPTQ (Hessian-based optimal weight rounding) with FourOverSix adaptive block\nscale selection. Calibration: 90 wikitext samples, log-uniform length distribution.\nMax seq length 92160 (90K)."
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/demo-sala/preprocess_model.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/quant/nvfp4.md"
}
```

> TOOL

tool_result Read
```
1	# 量化
2	
3	## 1. NVFP4 量化方案
4	
5	| 项 | 值 |
6	|---|---|
7	| 算法 | GPTQ + FourOverSix（adaptive 4/6 block scale） |
8	| 校准 | wikitext loguniform 128 samples，8 buckets（512–64K log-uniform） |
9	| 上下文 | 48K |
10	| 推理路径 | `--dense-as-sparse`（dense_len=0，全序列走 sparse TopK） |
11	| `lm_head` | Identity patch，不量化 |
12	
13	### 校准实验
14	
15	| Config | Calibration | max_length | FourOverSix | dense-as-sparse | ori_accuracy |
16	|---|---|---|---|---|---|
17	| baseline | calib90 (eval mix) | 24K | ❌ | ✅ | 80.27%（不稳定） |
18	| **chosen** | **loguniform 128 (wikitext)** | **48K** | **✅** | **✅** | **79.98%** |
19	| exp | loguniform 128 | 48K | ✅ | ❌ | 78.18% |
20	| exp | calib90 | 72K | ✅ | ✅ | 77.04%（不达标） |
21	
22	**`--dense-as-sparse` 强制开启**，否则有精度问题。所有 8 个 standard attention 层无论序列长度一律走 InfLLM-v2 稀疏路径。
23	
24	## 2. FourOverSix (4/6)
25	
26	MIT-HAN Lab 方案。标准 NVFP4 固定 block scale÷6；FourOverSix 对每个 block 比较 scale=4 和 scale=6 的 MSE，选更小者。输出格式不变（4-bit FP4 权重 + FP8 block scales），zero throughput impact。
27	
28	```python
29	scale_4 = fp8(scale_6.float() * 1.5)     # scale=4: 权重映射到 [-4, 4]
30	mse_6 = sum((W_group - dequant(W_group, scale_6))**2)
31	mse_4 = sum((W_group - dequant(W_group, scale_4))**2)
32	new_scale = where(mse_4 < mse_6, scale_4, scale_6)
33	```
34	
35	实测 40–43% blocks 选 scale=4；MLP 层比 Attention 层获益更大。
36	
37	集成方式：直接 patch `llmcompressor/modifiers/quantization/gptq/gptq_quantize.py`，在 observer 输出 scale 后、GPTQ 优化循环前插入 scale 选择。`prepare_env.sh` 用 `cp patches/gptq_quantize_fouroversix.py $GPTQ_TARGET` 覆盖。
38	
39	## 3. Hybrid Marlin / CUTLASS dispatch
40	
41	Decode 时 M 小 → Marlin W4A16 显著快于 CUTLASS W4A4。
42	
43	**当前策略**：全局阈值 `SGLANG_MARLIN_DECODE_THRESHOLD=48`。M ≤ 48 → Marlin；M > 48 → CUTLASS。Marlin/CUTLASS 两份权重共存，额外 VRAM ~4 GB。CUDA graph safe。
44	
45	详细调优记录、b12x 2-tier dispatch、负结果见 [`marlin.md`](marlin.md)。
46	
47	### Draft model 始终走纯 Marlin
48	
49	`_detect_draft_model_quantization()` 检测到 FP4 draft 时设 threshold=9999。M=1–6 时 CUTLASS 比 Marlin 慢 3–8×：
50	
51	| Layer | Marlin | CUTLASS | 倍率 |
52	|---|---|---|---|
53	| gate_proj (N=16384) | 16.4 us | 48 us | 2.9× |
54	| down_proj (K=16384) | 20.5 us | 154 us | 7.5× |
55	| o_proj (4096×4096) | 10.3 us | 41 us | 3.9× |
56	
57	## 4. KV cache 量化
58	
59	**生产**：`--kv-cache-dtype fp8_e5m2`，FlashInfer `BatchDecodeWithPagedKVCacheWrapper` 吃 fp8 buffer + kernel 内 on-the-fly dequant，省 HBM 读带宽。高并发稳定收益。
60	
61	**NVFP4 KV：在 SALA 当前架构下没有可落地路径**（2026-04-21 调研定论）。本节是负结果存档，防止重踩。
62	
63	### 4.1 FlashInfer NVFP4 KV API 真实约束
64	
65	老版本 `quant/nvfp4.md` 给的阻塞理由（"`trtllm_batch_decode_with_kv_cache` 未传 `kv_block_scales`"）已过时——FlashInfer 0.6.8 早就支持（`decode.py:2260` 的 `kv_cache_sf=(k_sf, v_sf)`）。**真正阻塞点不在 API**，在算法不兼容：
66	
67	| 路径 | backend | sm_120 | page_size 限制 | 通用 sparse | NVFP4 KV |
68	|---|---|---|---|---|---|
69	| `trtllm_batch_decode_with_kv_cache` (xqa) | xqa | ✅ | ∈ {16,32,64,128} | ❌ dense paged | ✅ |
70	| `trtllm_batch_decode_with_kv_cache` (trtllm-gen) | trtllm-gen | ❌ sm_100/103 only | — | — | ✅ |
71	| `flashinfer.xqa.xqa` 直调 | xqa | ✅ | ∈ {16,32,64,128} | ❌ | ✅ |
72	| `BatchDecodeWithPagedKVCacheWrapper` | FA2/FA3 | ✅ | page=1 OK | token-level indices | ❌ |
73	| `VariableBlockSparseAttentionWrapper` | FA2/FA3 | ✅（FA3 打折） | page=1 OK | block-sparse | ❌ |
74	
75	**支持 NVFP4 KV 的 kernel 都要求 page_size ≥ 16；支持 page_size=1 / sparse 的 kernel 都不吃 NVFP4。**
76	
77	NVFP4 (E2M1) + E4M3FN per-16-element block scale，scale block 沿 head_dim（不是 token），格式本身和 page_size=1 兼容；page_size≥16 是 xqa 的 TMA tile 约束。
78	
79	### 4.2 SALA page_size=1 的硬依赖
80	
81	`--dense-as-sparse` 启动后 8 层 standard attention 永远走 InfLLM-v2 sparse，page_size=1 是算法决定：
82	
83	```python
84	# minicpm_backend.py:1410 (sparse extend)
85	assert self.page_size == 1
86	key_cache_by_head_group = key_cache.reshape(-1, self.page_size, ...)
87	
88	# minicpm_backend.py:1130 (sparse decode)
89	sparse_page_table = sparse_kernel_extension.get_block_table_v2(
90	    topk_idx, page_table, ..., self.sparse_topk
91	).reshape(-1, self.num_sparse_topk_tokens)   # 96*64=6144 token slots
92	```
93	
94	InfLLM-v2 是 block-sparse，`block_size=64`、`topk=64`、`window_size=2048`、`dense_len=8192`。理论上 `block_size=64 / page_size=16 = 4` 可对齐 xqa 约束，但实测推进时撞深层 bug：
95	
96	1. `server_args.py` `speculative_eagle_topk>1 && page_size>1` 白名单不含 `minicpm_flashinfer`
97	2. `HybridLinearKVPool.enable_kv_cache_copy` 不透传 → `move_kv_cache` assert 崩
98	3. **架构级不兼容**：`compress_k1/k2` 池每 `kernel_stride=16` 步调 `alloc_token_slots(..., 1)`，page_size=16 下返回空 tensor。compress_k pool 和 full KV pool 共享 allocator/page_size，要修需 compress_k 独立 allocator，中等规模重构
99	
100	前两个修法属 latent bug fix，**已保留在 fork**（不影响 page_size=1 生产）：
101	
102	- `server_args.py:2180` `minicpm_flashinfer` 加入白名单
103	- `memory_pool.py:1231` `HybridLinearKVPool.__init__` 透传 `enable_kv_cache_copy`
104	- `model_runner_kv_cache_mixin.py:562` 显式 `enable_kv_cache_copy=(speculative_algorithm is not None)`
105	
106	第三个 compress_k 不兼容是架构级，未投入。
107	
108	### 4.3 全球现成 NVFP4 KV kernel 盘点（30+ 项目）
109	
110	需求：NVFP4 KV + page_size=1（或 token-level sparse block_table）+ sm_120。
111	
112	**最接近的 3 个**：
113	
114	| 候选 | NVFP4 KV | sparse/page=1 | sm_120 | 硬伤 |
115	|---|---|---|---|---|
116	| FlashInfer `xqa` | ✅ | ❌（page≥16） | ✅ | dense `page_table`，喂不了 InfLLM-v2 top-K block |
117	| SGLang PR #21601 | ✅ quantize 逻辑可复用 | ❌ | ✅ | 上层假定 dense MHA，未 merge |
118	| FlashInfer `VariableBlockSparseAttentionWrapper` | ❌（KV 只到 FP8） | ✅ | ⚠ FA3 打折 | 不支持 NVFP4 |
119	
120	**查过且不适用**：TRT-LLM xqa cubin（sm_100/103）/ vLLM NVFP4 KV（未实现 #32220）/ DeepSeek FlashMLA / Quest / Block-Sparse-Attention / MInference / native-sparse-attention-triton / SpargeAttn / SageAttention3 / OpenBMB infllmv2_cuda_impl（sm80/90 only）/ SGLang PR #10078 / #12612 / #17365 / LMDeploy TurboMind / NVFP4-on-4090-vLLM / Qwen3.6-NVFP4-DFlash 等。
121	
122	**SGLang PR #10078 的 KVFP4 用 E8M0（MXFP4），格式不对，喂给 FlashInfer xqa 会精度严重退化**。要用 `flashinfer.nvfp4_quantize(sfLayout=layout_linear)`。
123	
124	### 4.4 离线 microbench 留档
125	
126	NVFP4 KV decode（xqa, dense path, `bench/bench_nvfp4_kv_decode.py`）：大 batch × 长 seq 下确有 2-3× 加速（HBM 带宽饱和区间），但此 kernel 是 dense xqa 不走 SALA sparse。精度 cos_sim ~0.95（纯随机）。
127	
128	Triton NVFP4 sparse decode（自写 naive，`bench/bench_nvfp4_sparse_decode_triton.py`）：cos_sim 0.99，但 B=8 SP=4096 700us，对比 bf16 flashinfer ~23us（roofline 10us）→ 离 flashinfer 30×，离 roofline 50×。手写追平需 split-KV + TMA + tile 优化，几周级别工程。
129	
130	VariableBlockSparseAttentionWrapper（`bench/bench_variable_block_sparse_wrapper.py`）：vs 当前 `BatchPrefill` 整体打平或略慢，仅 B=8 SEQ=32K Q=5 一个点 20% 加速。**换 wrapper 不是加速方案**，内部两者都是 prefill kernel。
131	
132	### 4.5 三条理论路径 + 决策
133	
134	| 路径 | 关键动作 | 工程量 | ROI |
135	|---|---|---|---|
136	| A. 放弃 `--dense-as-sparse`，混合 KV | 短 seq→dense xqa+NVFP4；长 seq→sparse+FP8 | 中 | 短 seq 有收益但影响长上下文精度 |
137	| B. 自写 Triton sparse+NVFP4 kernel | 500-800 行，split-KV+TMA | 高（周级） | 难超 flashinfer FP8 |
138	| **C. 守 fp8** | 优化 compress_k / top-K / Marlin dispatch | 低 | 已知瓶颈更可能 |
139	
140	**选 C**。NVFP4 KV 理论收益（~2× 带宽）不足以值回工程投入。
141	
142	## 5. Health check 注意
143	
144	NVFP4 量化后模型在 mcq 强格式约束下会退化为重复 pattern，但 eval regex 仍命中 → `ori_accuracy` 看似正常实则生成垃圾。**健康检查必须用 chat 长样本，不用 mcq。**
145
```

> TOOL

tool_use Bash
```json
{
  "command": "ls bench/bench_nvfp4*.py bench/bench_variable_block*.py 2>&1",
  "description": "verify if bench scripts exist"
}
```

> TOOL

tool_result Bash
```
Exit code 2
ls: cannot access 'bench/bench_nvfp4*.py': No such file or directory
ls: cannot access 'bench/bench_variable_block*.py': No such file or directory
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/quant/nvfp4.md",
  "old_string": "| 项 | 值 |\n|---|---|\n| 算法 | GPTQ + FourOverSix（adaptive 4/6 block scale） |\n| 校准 | wikitext loguniform 128 samples，8 buckets（512–64K log-uniform） |\n| 上下文 | 48K |\n| 推理路径 | `--dense-as-sparse`（dense_len=0，全序列走 sparse TopK） |\n| `lm_head` | Identity patch，不量化 |\n\n### 校准实验\n\n| Config | Calibration | max_length | FourOverSix | dense-as-sparse | ori_accuracy |\n|---|---|---|---|---|---|\n| baseline | calib90 (eval mix) | 24K | ❌ | ✅ | 80.27%（不稳定） |\n| **chosen** | **loguniform 128 (wikitext)** | **48K** | **✅** | **✅** | **79.98%** |\n| exp | loguniform 128 | 48K | ✅ | ❌ | 78.18% |\n| exp | calib90 | 72K | ✅ | ✅ | 77.04%（不达标） |",
  "new_string": "| 项 | 值（当前生产，2026-05） |\n|---|---|\n| 算法 | GPTQ + FourOverSix（adaptive 4/6 block scale） |\n| 校准数据 | wikitext loguniform，`NUM_CALIBRATION_SAMPLES=90` |\n| 校准上下文 | `MAX_SEQ_LENGTH=92160`（90K） |\n| 推理路径 | `--dense-as-sparse`（dense_len=0，全序列走 sparse TopK） |\n| `lm_head` | Identity patch，不量化 |\n\n生产配置常量在 `demo-sala/preprocess_model.py:33-34`；`prepare_model.sh` 调用时不传 env，\n全部用 file 默认值。\n\n### 校准实验（早期对比，已固化）\n\n| Config | Calibration | max_length | FourOverSix | dense-as-sparse | ori_accuracy |\n|---|---|---|---|---|---|\n| baseline | calib90 (eval mix) | 24K | ❌ | ✅ | 80.27%（不稳定） |\n| exp | loguniform 128 | 48K | ✅ | ❌ | 78.18% |\n| exp | calib90 | 72K | ✅ | ✅ | 77.04%（不达标） |\n| 中间版 | loguniform 128 (wikitext) | 48K | ✅ | ✅ | 79.98% |\n| **当前生产** | **wikitext loguniform 90** | **92160 (90K)** | **✅** | **✅** | 见线上 eval |\n\n校准从 128/48K 升到 90/90K 是为了覆盖更长上下文输入的 weight 分布，样本数微降换 max_length 升 ~2×。"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/quant/nvfp4.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/quant/nvfp4.md",
  "old_string": "### 4.4 离线 microbench 留档\n\nNVFP4 KV decode（xqa, dense path, `bench/bench_nvfp4_kv_decode.py`）：大 batch × 长 seq 下确有 2-3× 加速（HBM 带宽饱和区间），但此 kernel 是 dense xqa 不走 SALA sparse。精度 cos_sim ~0.95（纯随机）。\n\nTriton NVFP4 sparse decode（自写 naive，`bench/bench_nvfp4_sparse_decode_triton.py`）：cos_sim 0.99，但 B=8 SP=4096 700us，对比 bf16 flashinfer ~23us（roofline 10us）→ 离 flashinfer 30×，离 roofline 50×。手写追平需 split-KV + TMA + tile 优化，几周级别工程。\n\nVariableBlockSparseAttentionWrapper（`bench/bench_variable_block_sparse_wrapper.py`）：vs 当前 `BatchPrefill` 整体打平或略慢，仅 B=8 SEQ=32K Q=5 一个点 20% 加速。**换 wrapper 不是加速方案**，内部两者都是 prefill kernel。",
  "new_string": "### 4.4 离线 microbench 留档（脚本已删除，结论保留）\n\n历史 bench 脚本（2026-04 调研期）已不在 `bench/` 下，结论存档：\n\n- **NVFP4 KV decode（xqa, dense path）**：大 batch × 长 seq 下确有 2-3× 加速（HBM 带宽饱和区间），但 kernel 是 dense xqa 不走 SALA sparse。精度 cos_sim ~0.95（纯随机）。\n- **Triton NVFP4 sparse decode（自写 naive）**：cos_sim 0.99，但 B=8 SP=4096 700us，对比 bf16 flashinfer ~23us（roofline 10us）→ 离 flashinfer 30×，离 roofline 50×。手写追平需 split-KV + TMA + tile 优化，几周级别工程。\n- **VariableBlockSparseAttentionWrapper**：vs 当前 `BatchPrefill` 整体打平或略慢，仅 B=8 SEQ=32K Q=5 一个点 20% 加速。**换 wrapper 不是加速方案**，内部两者都是 prefill kernel。"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/quant/nvfp4.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/quant/README.md"
}
```

> TOOL

tool_result Read
```
1	# Quantization
2	
3	NVFP4 **量化方案**（怎么量化模型）。GEMM kernel 调优 / Marlin 调优 / sm_120 GEMM 已迁移到 [`../gemm/`](../gemm/)。
4	
5	| 文档 | 内容 |
6	|---|---|
7	| [nvfp4.md](nvfp4.md) | NVFP4 量化方案（GPTQ + FourOverSix + dense-as-sparse）、校准实验、Hybrid Marlin/CUTLASS dispatch（量化侧 prep）、KV cache 量化（NVFP4 KV 负结果归档） |
8	
9	跨主题：
10	- **GEMM kernel 调优 / Marlin 调优 / sm_120 GEMM 现状** → [`../gemm/`](../gemm/)
11	- 部署 / cu13 升级 → [`../platform/cu13-stack.md`](../platform/cu13-stack.md)
12	- decode 性能 → [`../decode/`](../decode/)
13
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/quant/README.md",
  "old_string": "# Quantization\n\nNVFP4 **量化方案**（怎么量化模型）。GEMM kernel 调优 / Marlin 调优 / sm_120 GEMM 已迁移到 [`../gemm/`](../gemm/)。",
  "new_string": "# Quantization\n\nNVFP4 **量化方案**（怎么量化模型）。GEMM kernel 调优 / Marlin 调优 / sm_120 GEMM 已迁移到 [`../gemm/`](../gemm/)。\n\n> **生产唯一基线**：`demo-sala/preprocess_model.py` + `prepare_model.sh`，本目录是技术档案。代码与文档冲突以代码为准。"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/quant/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "9",
  "status": "completed"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #9 status
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "10",
  "status": "in_progress"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #10 status
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/handover.md"
}
```

> TOOL

tool_result Read
```
1	# 全栈接续指南
2	
3	下一个 session 接续工作时优先读这份。链接到事实文档；不要把瞬时 bench 数字写进来。
4	
5	工作目录：`/user_4813494d/openbmb`
6	当前分支：`demosala-rollback`
7	提交根目录：`demo-sala/`，custom SGLang 在 `demo-sala/sglang/python/`
8	
9	## 0. 红线（CLAUDE.md 已锁，重申）
10	
11	- **基座模型不可换**（MiniCPM-SALA），改动只能落在量化方案 / SGLang fork / draft / kernel / 部署脚本
12	- 杀 sglang 只用 `bash bench/kill_sglang.sh`，**禁用** `pkill -f sglang`（杀系统进程）
13	- 服务器就绪：日志 `Uvicorn running on` 或 curl `/v1/models`，**不用** `/health`
14	- **始终 `uv pip install`，永不 `pip install`**
15	- 提交包 ≤ 2 GB
16	- `SGLANG_SERVER_ARGS` 用连字符（`--dense-as-sparse`）
17	- 同时只能跑一个 GPU 任务（显存会占满）
18	- 安装脚本严禁 fallback，失败 `exit 1`
19	- 性能改动先 profile 证明 >1.5× 正向收益再 e2e bench
20	- 正确性验证发 chat 请求看人话，不跑 mcq
21	
22	## 1. 当前生产配置
23	
24	| 维度 | 值 | 文档 |
25	|---|---|---|
26	| 硬件 | RTX 6000D (sm_120) | [platform/cu13-stack.md](platform/cu13-stack.md) |
27	| 栈 | torch 2.11.0+cu130 / triton 3.6.0 / cuDNN 9.21 / FlashInfer 0.6.8.post1 / sgl-kernel 0.3.20 + 本仓 `220c18cc` `.so` | [platform/cu13-stack.md](platform/cu13-stack.md) |
28	| 量化 | GPTQ + NVFP4 + FourOverSix（loguniform128 校准，48K 上下文） | [quant/nvfp4.md](quant/nvfp4.md) |
29	| Decode dispatch | M ≤ 48 → Marlin；M > 48 → CUTLASS（`SGLANG_MARLIN_DECODE_THRESHOLD=48`）| [gemm/marlin.md](gemm/marlin.md) |
30	| Spec (prod) | EAGLE-3 chain，`spec_steps=3, topk=2, dtn=7`，dynamic mode（NO_SPEC / D5 / D7） | [eagle/README.md](eagle/README.md) |
31	| Spec (备选) | DFlash chain (block_size=8) / DDTree (tree_size=96)；同 ckpt 不同 verify | [dflash/](dflash/) |
32	| Draft (prod) | `eagle/models/v2mix_20k_s3500_ood757/`（OOD step0=0.7571）| [eagle/prod.md](eagle/prod.md) |
33	| Draft (DFlash) | `dflash/outputs/train/best.pt`（pos1=0.466 IND/0.463 OOD，不重训） | [dflash/current.md](dflash/current.md) §4 |
34	| MARS verify | global θ=1，D5 θ=0.75，D7 θ=0.5 | [eagle/experiments.md](eagle/experiments.md) §3 |
35	
36	`220c18cc` `.so` 必须用，不能换 `32d27c7`（含 small-M atomic + shape-aware tile 但与 EAGLE draft graph capture 不兼容，详见 [gemm/marlin.md](gemm/marlin.md) §6）。
37	
38	## 2. 关键命令
39	
40	```bash
41	# 启动推理 server（EAGLE-3 当前生产配置）
42	bash eval/start_eagle.sh
43	
44	# 停服（唯一允许方式）
45	bash bench/kill_sglang.sh
46	
47	# Mini speed bench
48	bash bench/mini_bench.sh
49	
50	# 完整 bench
51	bash toolkit/bench_serving.sh http://127.0.0.1:30000
52	
53	# 长 prefill 大 bench（最终口径）
54	python3 bench/kernels/prefill/prefill_bench_smax64.py
55	
56	# 正确性冒烟
57	curl -s -X POST http://127.0.0.1:30000/v1/chat/completions \
58	    -H "Content-Type: application/json" \
59	    -d '{"model":"minicpm","messages":[{"role":"user","content":"你好，介绍一下你自己"}],"max_tokens":100}'
60	```
61	
62	## 3. Prefill 状态
63	
64	事实来源：[prefill/current.md](prefill/current.md)。
65	
66	- 当前 stage2 sparse FA 走 FlashInfer `BatchPrefillWithPagedKVCacheWrapper`（不是 prefill wrapper、不是 infllmv2 topk）
67	- `--dense-as-sparse` 强制开启（精度问题），8 个 standard attention 层永远走 InfLLM-v2 sparse
68	- page_size=1 是算法决定（`assert self.page_size == 1`），改 page_size 需 compress_k 独立 allocator（中等重构）
69	- 已落地：layer/chunk plan cache + cross-forward buffer refresh + all-sparse fast path + token mapping 向量化 + derived sparse seqlens + direct sparse page table + stage1 actual maxlen + direct topk → FlashInfer indices 等
70	- **历史调研与已枯竭方向见** [prefill/history.md](prefill/history.md)：
71	  - infllmv2 blockmask batch>1 已修，但 paged KV 256 约束方案 A 仍进行中
72	  - nsys 真相：MLP 不是撞硬件天花板，是 register-bound 19% occupancy；stage1 splitkv 只占 0.16%；GLA Triton 已 65% occupancy 无空间
73	
74	## 4. Decode 状态
75	
76	事实来源：[decode/current.md](decode/current.md)。
77	
78	- node-trace 实测：GPU union-busy 82.3%，host-wait 9.64%，decode 内部真可攻击 host-wait ≈ 5.5%（CPU 侧 ROI 硬顶）
79	- workload 是 GPU-bound，**CPU 侧优化不再做**，优先攻 GPU critical path
80	- Top GPU kernels：NVFP4 GEMM 10.17% / BatchPrefill 6.42% / index_elementwise 2.63% / split_kv stage1 1.81%
81	- 已落地优化清单（按 commit 顺序）见 [decode/current.md](decode/current.md) §4
82	- **profile 方法论**（关键避坑）：必用 `--cuda-graph-trace=node`；CPU 时间 ≠ CPU 工作（`.tolist()` 是 GPU critical path 投影）；NVTX 归因必须 join RUNTIME_API 拿 launch CPU 时间。详见 [decode/history.md](decode/history.md) §8
83	
84	### 当前下一步候选（按 风险/收益）
85	
86	1. padded/stable sparse-K 布局（native `k_starts + k_lens`，跳过 fused topk）
87	2. Marlin/B12X 重新划分（B12X 作为研究候选，必须先补 bit-exact + accept-rate 长尾分布）
88	3. MARS topk 专用 top2 kernel
89	4. Plan A: triton 融合 mamba scatter（对应 `index_elementwise_kernel` 2.63%）
90	5. `BatchPrefillWithPagedKVCacheKernel` 6.42% e2e（属 prefill）
91	
92	## 5. EAGLE-3 状态
93	
94	事实来源：[eagle/README.md](eagle/README.md)。
95	
96	### 5.1 当前 prod draft
97	
98	`v2mix_20k_s3500_ood757`（OOD step0 = 0.7571，比 `det_prefill` 0.7530 +0.41%）。20000 target-regen samples + 200 IND 物理隔离 + cosine LR + sequence packing + B/C 微调（bf16 softmax + lk_lambda_loss fuse）。`demo-sala/data/eagle_draft/` 已替换。详见 [eagle/prod.md](eagle/prod.md)。
99	
100	### 5.2 训练流水线
101	
102	事实来源：[eagle/training/pipeline.md](eagle/training/pipeline.md)。
103	
104	- 当前数据路线：**target-regenerated**（target 模型自生成 assistant response，不用 dataset labels）
105	- prompt 配比：v2 distribution（chinese_r1 60% / stem_zh 22% / open_code 11.5% / codeforces 5.5% / dolphin 1%）
106	- window：4K shard + AOI cap=144000，不做 mixed shards
107	- forward GEMM：NVFP4 真 4-bit（sm_120 cutlass，~5× bf16，+14% throughput），lm_head 默认 bf16
108	- 训练 pipeline：cosine LR + AdamW fused + wd-split + opt state save + async prefetcher + sequence packing + multi-process index_lengths（47/s → 107/s）
109	
110	### 5.3 collapse 和 long-context
111	
112	事实来源：[eagle/collapse.md](eagle/collapse.md)。
113	
114	- 主因：draft 训练分布盲区（long deepresearch），**与 backend / KV pool / cuda graph 无关**
115	- 已落产：rope_theta=1M（vlong adj_al +44.9%），AOI 训练，target-regenerated data
116	- 红线内剩余：C2 runtime post-EOS / `<unk>`-loop detect → 退 nospec（约 20 行 `eagle_worker.py` 改动，未实现，预期 +23% throughput）
117	- batch drift：sglang/flashinfer multi-batch 路径数值非确定性，与 spec 无关，nospec c≥2 也产生不同 sha
118	
119	### 5.4 后续值得探索（在 [eagle/prod.md](eagle/prod.md) "后续值得探索" 列）
120	
121	1. **HASS context alignment**（ICLR'25, [arxiv 2408.15766](https://arxiv.org/abs/2408.15766)）：chain step k>0 input 用 draft 自己上一步 prediction，需 schedule 解决早期 self-prediction 不收敛
122	2. EMA decay=0.999
123	3. TTT 3 → 5（与生产 D7 chain steps 对齐；显存 +33% 风险）
124	4. SDPA-with-lse for step k>0（要 pad seq 到 4096-aligned 或解决 cudnn N=256 NaN bug）
125	
126	## 5b. DFlash + DDTree 状态（备选 spec 算法）
127	
128	事实来源：[dflash/](dflash/)。
129	
130	- DFlash chain：`bash eval/start_dflash.sh`，`block_size=8`，accept_len ≈ 1.15
131	- DFlash chain FULL_CTX (实验)：`bash eval/start_dflash_single.sh`，single-batch only，accept_len 1.62（+41%）
132	- DDTree：`bash eval/start_ddtree.sh`，`tree_size=96 dtn=97`，accept_len 1.82-1.93
133	- 共享 ckpt：`dflash/outputs/train/best.pt`（pos1=0.466 IND/0.463 OOD，**不重训**）
134	- aux_layers=[1, 10, 22] (避开 GLA，必须跟训练一致)，mask_token_id=73439
135	
136	### 5b.1 关键陷阱（必读）
137	
138	- **SGLang 主线 DFlash 在 FlashInfer/FA/TRTLLM 全部 skip custom_mask**（`_DFLASH_VERIFY_SKIP_CUSTOM_MASK_BACKENDS`）：DFlash chain mask = causal lower-tri，跟 `causal=True` 数学等价，主线选择走老路径。我们 fork 的 minicpm_backend hardcoded `causal=True` for verify 是**一致 policy**，不是 bug。详见 [dflash/integration.md](dflash/integration.md) §3
139	- **DDTree 必须走 custom_mask（ancestor-only mask ≠ causal）**：FlashInfer wrapper.run + custom_mask 在 sm_120 dtn>32 数值漂移（实测 L0 q0_norm 0.24% drift，L31 累积 8.5%）。修复方案：minicpm_backend 加 `_verify_manual_sdpa_with_mask` fp32 path 绕开。详见 [dflash/ddtree.md](dflash/ddtree.md) §2
140	- 启动时 `--page-size 1` + `--disable-overlap-schedule` + `EAGLE_DYNAMIC_MODE=0` 必须
141	
142	### 5b.2 后续优化候选（不重训）
143	
144	1. DDTree manual SDPA → triton kernel（+20-30% throughput）
145	2. FULL_CTX T-bucket piecewise cuda graph（恢复 +14% graph 收益）
146	3. Vectorize custom_mask 构造（移除 python loop）
147	4. 提交包打包（best.pt 4.3 GB → ≤ 2 GB tar；Phase 4，pending）
148	
149	## 6. 提交包流程
150	
151	平台提供原始 BF16 模型作为 `--input`：
152	
153	1. **`demo-sala/prepare_env.sh`**：装 custom SGLang (editable) + cuDNN 9.21+ + FlashInfer 0.6.8.post1+，替换 `common_ops.abi3.so`，patch FourOverSix，导出 `SGLANG_SERVER_ARGS` + `SGLANG_MARLIN_DECODE_THRESHOLD=48` + dynamic spec mode env
154	2. **`demo-sala/prepare_model.sh`**：NVFP4 量化（GPTQ + FourOverSix，loguniform 128，48K 上下文）
155	3. **`demo-sala/sglang/python/`**：custom patches（modelopt_quant hybrid Marlin、marlin_utils_fp4、minicpm_backend CUDA graph fix、GLA fused kernel 等）
156	
157	`demo-sala_v2mix_20k_s3500_ood757.tar.gz`（431 MB，2 GB 限内）已就绪，未入 git（部署产物）。
158	
159	## 7. probe-sala 平台部署（已退役）
160	
161	probe-sala 是 cu13 平台诊断探针（BOS 鉴权下发 + 邮件回传 + 11 项 verify），详见 [platform/cu13-stack.md](platform/cu13-stack.md) §4。
162	
163	> **2026-05-08 注**：probe-sala 在当前分支大部分文件已删除，详见 git status。要恢复请从 git history 拉。
164	
165	## 8. Profile 方法论速查（重要避坑）
166	
167	任何 CPU 侧优化前必过：
168	
169	```
170	Step 0  nsys profile --cuda-graph-trace=node   ← 必须 node，不能 graph
171	Step 1  GPU 活跃 % = Σ(kernel_duration) / profile_window
172	Step 2  GPU 活跃 ≥ 90%? → 纯 GPU-bound，CPU 侧 ≤ 10%
173	Step 3  否则拆 idle: host-wait / kernel-wait / unknown
174	Step 4  host-wait 占比 = CPU 侧 ROI 天花板
175	Step 5  改完 e2e 再测，profile "账面变好" 不算数
176	```
177	
178	NVTX 归因必须 join `CUPTI_ACTIVITY_KIND_RUNTIME` 拿 launch CPU 时间，不能用 GPU end-time（会张冠李戴）。
179	
180	`.tolist()` / `cudaMemcpyAsync(DtoH, pageable)` / `cudaStreamSynchronize` 在 profile 里的 CPU 时间是 GPU 工作的投影，**不是可优化 CPU 工作**。打它们等于优化了也没用。
181	
182	详见 [decode/current.md](decode/current.md) §3 / [decode/history.md](decode/history.md) §8。
183	
184	## 9. Monitor / 运维规则（CLAUDE.md 已写）
185	
186	- 等一次性事件用 `grep -m1 PATTERN`，匹配一次就退出；旧 monitor 必须先 `TaskStop` 再起新的
187	- 重启 server 前先停旧 monitor，即使 `rm` 了日志，`tail -F` 会跟进新文件触发幻象通知
188	- pattern 必须覆盖失败路径（`Traceback|ERROR|Killed|OOM`）
189	- 等待最多 `sleep 60s`，不轮询；后台任务用 `run_in_background` + 通知
190
```

> TOOL

tool_use Write
```json
{
  "file_path": "/user_4813494d/openbmb/docs/handover.md",
  "content": "# 全栈接续指南\n\n下一个 session 接续工作时优先读这份。链接到事实文档；不要把瞬时 bench 数字写进来。\n\n工作目录：`/user_4813494d/openbmb`；提交根目录：`demo-sala/`；custom SGLang 在 `demo-sala/sglang/python/`。\n\n> **红线、栈版本、运维规则、Monitor 规范**：全部在 [`/user_4813494d/openbmb/CLAUDE.md`](../CLAUDE.md)。本文档只\n> 列接续工作必读的状态与路径，不重复 CLAUDE.md 内容。\n\n## 1. 当前生产配置（一行一个，指针为主）\n\n| 维度 | 来源 |\n|---|---|\n| 硬件 / 栈版本 | [CLAUDE.md §运行栈](../CLAUDE.md#运行栈) |\n| 量化（NVFP4，GPTQ + FourOverSix，wikitext 90 样本，`MAX_SEQ_LENGTH=92160`） | [quant/nvfp4.md](quant/nvfp4.md) |\n| Decode dispatch（生产默认全 Marlin；`SGLANG_ENABLE_B12X=1` 启用 b12x 2-tier） | [gemm/marlin.md](gemm/marlin.md)、[decode/current.md](decode/current.md) |\n| Spec（EAGLE-3 chain，`spec_steps=3 topk=2 dtn=7`，dynamic NO_SPEC/D5/D7） | [eagle/README.md](eagle/README.md) |\n| Draft（`eagle/models/v2mix_20k_s3500_ood757/`） | [eagle/prod.md](eagle/prod.md) |\n| ngram routing（提交包默认开启） | [ngram/routing.md](ngram/routing.md) |\n| MARS verify（D5 θ=0.85，D7 θ=0.5） | [eagle/experiments.md](eagle/experiments.md) §3 |\n| DFlash + DDTree（**非生产**，备选 spec 算法） | [dflash/](dflash/) |\n\n`.so` 替换日志见 [gemm/so-replacements.md](gemm/so-replacements.md)（替换 `.so` 前先备份，CLAUDE.md 硬规则）。\n\n## 2. 关键命令\n\n```bash\nbash eval/start_eagle.sh                       # 起 EAGLE-3 生产 server\nbash bench/kill_sglang.sh                      # 唯一允许的停服方式\nbash bench/mini_bench.sh                       # 速度速查\nbash toolkit/bench_serving.sh http://127.0.0.1:30000   # 完整 bench\n```\n\n## 3. Prefill 接续\n\n事实来源：[prefill/current.md](prefill/current.md)。\n\n- 当前 stage2 sparse FA 走 FlashInfer `BatchPrefillWithPagedKVCacheWrapper`；`--dense-as-sparse` 强制\n  开启，page_size=1 是算法决定（compress_k 独立 allocator 是中等重构）。\n- 已落地：layer/chunk plan cache + cross-forward buffer refresh + all-sparse fast path + token\n  mapping 向量化 + derived sparse seqlens + direct sparse page table + stage1 actual maxlen + direct\n  topk → FlashInfer indices。\n- 已枯竭路线（TrtLLM stage2 替换 / compressed_max_seqlen_k / `_USE_TRTLLM_STAGE2`）见\n  [prefill/history.md](prefill/history.md)，进一步 bounding 调研见 `prefill/`、`piecewise/`\n  两个工作区（May 17）。\n\n## 4. Decode 接续\n\n事实来源：[decode/current.md](decode/current.md)。\n\n- workload 是 GPU-bound（GPU union-busy 82%，host-wait 9.6%），**CPU 侧 ROI 已封顶**，优先攻 GPU\n  critical path。\n- b12x 2-tier dispatch 已 lock-in 但默认 OFF（`SGLANG_ENABLE_B12X=0`）；启用后 decode +28.5%\n  （bs=1）/ +6-12%（bs=8-24），AOT cache 在 `demo-sala/assets/b12x_aot_cache/`。\n- Profile 方法论 / NVTX 归因陷阱 / `.tolist()` 是 GPU 投影：[decode/current.md](decode/current.md) §3、\n  [gemm/methodology.md](gemm/methodology.md) §8。\n\n## 5. EAGLE-3 接续\n\n事实来源：[eagle/README.md](eagle/README.md)。\n\n- 当前 prod draft：`v2mix_20k_s3500_ood757`（OOD step0=0.7571）。`demo-sala/data/eagle_draft/` 已替换。\n- 训练流水线（target-regenerated v2 distribution，NVFP4 4-bit forward GEMM）：\n  [eagle/training/pipeline.md](eagle/training/pipeline.md)。\n- collapse 根因（draft 训练分布盲区）+ 已落产修复（rope_theta=1M、MARS θ=0.85）：\n  [eagle/collapse.md](eagle/collapse.md)、[eagle/experiments.md](eagle/experiments.md)。\n- 大 batch spec 增益缩水根因 + 学术方案综述：[eagle/large-batch.md](eagle/large-batch.md)。\n\n## 6. DFlash + DDTree（备选 spec 算法，非生产）\n\n事实来源：[dflash/](dflash/)。CLAUDE.md 已明确不作为生产实践。\n\n- DFlash chain：`eval/start_dflash.sh`；DFlash FULL_CTX 单 batch：`eval/start_dflash_single.sh`；\n  DDTree：`eval/start_ddtree.sh`。\n- 共享 ckpt 路径：`dflash/outputs/train/best.pt`（pos1=0.466 IND/0.463 OOD）；当前盘上**已删**，需重新\n  训练才能复现，详情见 [dflash/history.md](dflash/history.md) §4。\n- 关键陷阱（custom_mask FlashInfer 数值漂移 + manual SDPA workaround）：\n  [dflash/ddtree.md](dflash/ddtree.md)、[dflash/integration.md](dflash/integration.md)。\n\n## 7. 提交包流程\n\n平台提供原始 BF16 模型作为 `--input`：\n\n1. `demo-sala/prepare_env.sh`：装 custom SGLang (editable) + cuDNN 9.21+ + FlashInfer 0.6.8.post1+，\n   替换 `common_ops.abi3.so`，patch FourOverSix，导出 `SGLANG_SERVER_ARGS` +\n   `SGLANG_MARLIN_DECODE_THRESHOLD=48` + dynamic spec mode env。\n2. `demo-sala/prepare_model.sh`：NVFP4 量化（GPTQ + FourOverSix，wikitext 90 样本，\n   `MAX_SEQ_LENGTH=92160`）。\n3. `demo-sala/sglang/python/`：custom patches（`modelopt_quant` hybrid Marlin、`marlin_utils_fp4`、\n   `minicpm_backend` CUDA graph fix、GLA fused kernel 等）。\n\n详细栈差异与 cu13 升级要点：[platform/cu13-stack.md](platform/cu13-stack.md)。\n\n## 8. 调试 sidecar\n\n`probe-sala-s2/`（authorized_keys 注入 + dropbear/frpc 反向 SSH）是评测机现场调试用，不是提交包。原\n`probe-sala/` 平台诊断探针已退役（commit `b74c10d`），要恢复请从 git history 拉。\n"
}
```

> TOOL

tool_result Write
```
The file /user_4813494d/openbmb/docs/handover.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "10",
  "status": "completed"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #10 status
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "11",
  "status": "in_progress"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #11 status
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/platform/cu13-stack.md"
}
```

> TOOL

tool_result Read
```
1	# 平台与环境栈
2	
3	## 1. 当前生产栈
4	
5	| 层 | 版本 | 备注 |
6	|---|---|---|
7	| 硬件 | RTX 6000D (sm_120, Blackwell GB202, 84GB) | 无 TMEM，FA4 不可用 |
8	| CUDA toolkit | 13.2 | **仅开发机**：apt 装 `/usr/local/cuda-13.2`。**评测机 `/usr/local/cuda` 不存在**，flashinfer JIT 必崩 → 所有 op 必须 prebuilt 进 AOT，见 [trtllm-utils-aot-fix.md](trtllm-utils-aot-fix.md) |
9	| torch | 2.11.0+cu130 | pypi cu13 runtime 16 包随 torch 自动拉 |
10	| triton | 3.6.0 | |
11	| cuDNN | [REDACTED] | sm_120 FP4 cudnn backend 硬要求（≥9.21） |
12	| FlashInfer | 0.6.8.post1[cu13] | flashinfer-cubin 同版本 |
13	| sgl-kernel | 0.3.20 + 本仓库 `common_ops.abi3.so` | Marlin FP4 scale bug fix（见 `gemm/marlin.md`） |
14	| SGLang | fork @ v0.5.7 基线 + demo-sala patches | editable install |
15	| nvidia-modelopt | 0.42.0 | |
16	| llmcompressor | [REDACTED] + `gptq_quantize_fouroversix.py` | 装完需回滚 `compressed-tensors==0.13.0 accelerate==1.13.0` |
17	
18	## 2. demo-sala/prepare_env.sh 关键动作
19	
20	平台拉起后 source 此脚本：
21	
22	1. `uv pip install --no-deps -e ./sglang/python` editable
23	2. cu13 runtime + cuDNN 9.21 + FlashInfer 0.6.8.post1 + nvidia-modelopt + llmcompressor
24	3. patch FourOverSix（`gptq_quantize_fouroversix.py`）
25	4. 替换 `common_ops.abi3.so`（Marlin FP4 scale fix）
26	5. 清 `~/.cache/flashinfer/` + 预热 `fp4_gemm_cutlass_sm120` JIT
27	6. 导出 `SGLANG_SERVER_ARGS` + `SGLANG_MARLIN_DECODE_THRESHOLD=48` + dynamic spec mode env
28	
29	**严禁 fallback**：失败直接 `exit 1`，不允许 pypi.org / pytorch.org 兜底。
30	
31	**Stage 3 G4b（关键）**：遍历 `prebuilt/flashinfer_cache/0.6.8.post1/120f/cached_ops/*/<name>.so`，每个都拷贝到 `flashinfer/data/aot/<name>/<name>.so`。由于评测机 `/usr/local/cuda` 缺失（见 §1 / §3.x），任何走 ninja JIT 的 flashinfer op 都会失败，必须**全部走 AOT**。当前已 AOT 化：`fp4_gemm_cutlass_sm120`、`fp4_quantization_120f`、`cascade`、`batch_prefill_*`、`trtllm_utils`。新增 op 时跑一遍本地 prewarm，把生成的 `.so` 加进 prebuilt 即可（代码不动）。
32	
33	平台 vs 开发机更广泛差异 → [eval-vs-dev-environment-audit.md](eval-vs-dev-environment-audit.md)。
34	
35	## 3. cu12 → cu13 升级要点（已完成）
36	
37	升级日：2026-04-20。本节只保留**会再用到的事实**，过程性细节进 git history。
38	
39	### 3.1 必踩的坑
40	
41	| 现象 | 根因 | 修法 |
42	|---|---|---|
43	| `mm_fp4(cudnn)` 报 `Multiple libcudart libraries found` | `/etc/ld.so.conf.d/988_cuda-12.conf` 把 cu12 cudart 仍写进 ldconfig | 改名 `.disabled` + `ldconfig`，不必 apt purge |
44	| `mm_fp4(cudnn)` 报 `No valid engine configs for smVersion:1200` | cuDNN 9.19 不够 | `--force-reinstall --no-deps "nvidia-cudnn-cu13>=9.21"` |
45	| 卸 cu12 共享目录包后 cu13 .so 也被删 | cu12/cu13 都装到 `site-packages/nvidia/<name>/lib/`，pip 卸 cu12 删实体 .so | 卸完后 `--force-reinstall` cu13 的 cusparselt / nvshmem / nccl / cudnn |
46	| infllm_v2 重编报错 `MAJOR>=12 && MINOR>=5` | bundled CUTLASS 3.6 cu13 兼容 guard bug | 改成 `MAJOR>=13 \|\| (MAJOR==12 && MINOR>=5)` |
47	| sgl-kernel 重编 OOM | cgroup 限 64GB | `MAX_JOBS=4`，>4 单 nvcc 8-10GB 会 OOM |
48	| FlashInfer JIT cache 路径 | cu12 用 `120a/`，cu13 用 `120f/` | `prewarm_flashinfer_fp4.py` 路径 + `~/.cache/flashinfer/*/120a/` 旧 cache 删除 |
49	
50	### 3.2 编译命令（开发机重编时用）
51	
52	```bash
53	# sparse_kernel_extension
54	cd /opt/SGLang-MiniCPM-SALA/packages/sparse_kernel
55	python setup.py build_ext --inplace
56	cp *.so /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/
57	
58	# infllm_v2（先 patch CUTLASS guard）
59	cd /opt/SGLang-MiniCPM-SALA/packages/infllmv2_cuda_impl
60	sed -i 's@#if (CUDA_VERSION_MAJOR >= 12) && (CUDA_VERSION_MINOR >= 5)@#if (CUDA_VERSION_MAJOR >= 13) || ((CUDA_VERSION_MAJOR == 12) && (CUDA_VERSION_MINOR >= 5))@' \
61	    include/cutlass/cuda_host_adapter.hpp
62	MAX_JOBS=4 python setup.py build_ext --inplace
63	
64	# sgl_kernel common_ops sm100（绕 uv pip install）
65	cd /user_4813494d/deps/sgl-kernel-build
66	cmake -S . -B build -G Ninja \
67	    -DSGL_KERNEL_ENABLE_SM90=OFF -DSGL_KERNEL_ENABLE_FA3=OFF \
68	    -DSGL_KERNEL_ENABLE_FLASHMLA=OFF -DSGL_KERNEL_ENABLE_SPATIAL=OFF \
69	    -DSGL_KERNEL_ENABLE_DEEPGEMM=OFF -DSGL_KERNEL_ENABLE_MSCCLPP_PY=OFF \
70	    -DFETCHCONTENT_SOURCE_DIR_REPO-CUTLASS=/user_4813494d/deps/repo-cutlass \
71	    -DFETCHCONTENT_SOURCE_DIR_REPO-FLASHINFER=/user_4813494d/deps/repo-flashinfer
72	ninja -C build common_ops_sm100_build -j 4
73	cp build/common_ops.abi3.so \
74	   /opt/SGLang-MiniCPM-SALA/sglang_minicpm_sala_env/lib/python3.10/site-packages/sgl_kernel/sm100/
75	```
76	
77	`/user_4813494d/deps/` 备齐 8 个 FetchContent 仓库（cutlass / deepgemm / fmt / triton / flashinfer / flash-attention / mscclpp / fast-hadamard-transform），SHA 与 sgl-kernel CMakeLists 对齐，以后任何 sgl-kernel 重编优先 `-DFETCHCONTENT_SOURCE_DIR_REPO-*`。
78	
79	### 3.3 cu13 vs cu12 性能 diff（关键形状）
80	
81	| 路径 | 形状 | M 范围 | Δ |
82	|---|---|---|---|
83	| Marlin FP4 decode | gate_proj 4096×16384 | M=1-8 | **-12.5%** ✅ |
84	| Marlin FP4 decode | down_proj 16384×4096 | M=1-32 | **-11%** ✅ |
85	| CUTLASS NVFP4 | k_proj 4096×256 | M=1-2 | **-21~25%** ✅ |
86	| 其他 | — | — | ±2% 噪声 |
87	
88	零回归。Marlin decode 大 MLP 形状 10-12% 提速 = S1 decode 热路径直接受益。
89	
90	### 3.4 回滚
91	
92	`/user_4813494d/backups/cu12-baseline-20260420/` + `RESTORE.sh`（19 GB，9 秒回滚）。venv + cuda-12.9 toolkit + packages + flashinfer-cache + 编译产物全备。
93	
94	## 4. probe-sala 提交包流水（云评测环境一次过）
95	
96	`probe-sala/` 是面向评测平台的**一次性、无 fallback、BOS 鉴权下发**的 cu13 安装包，与 demo-sala（增量升级）路径分离。专门用于平台环境复现本地已验证栈。
97	
98	### 4.1 设计要点
99	
100	1. **BOS 鉴权下载**（替代 pypi / pytorch.org 兜底）：bcecmd 拉 92 wheel + 3 torch wheel，2.8 GB，缺一个就 `exit 1`
101	2. **cu12 彻底清理**：`dpkg --purge --force-all` 绕过依赖、连带删 `/usr/local/cuda-12*` 和 `/etc/ld.so.conf.d/988_cuda-12.conf`
102	3. **flashinfer AOT skip JIT**：把 prebuilt `*.so` 拷到 `site-packages/flashinfer/data/aot/<name>/<name>.so`，flashinfer 检测 aot_path 直接 `load`，不调 ninja。评测机不需要 nvcc
103	4. **失败强制终止**：检测 sourced/executed 模式，`kill -TERM ${KILL_TARGET}` 把平台 shell 一并杀掉，不能让评测继续
104	
105	### 4.2 verify_env.py 11 项
106	
107	| # | 检查 | 失败含义 |
108	|---|---|---|
109	| C1 | `libcudart.so.13` 存在且无 `.so.12` 进 ldconfig | cu12 purge 残留 |
110	| C2 | pip cuDNN 9.21+（不是系统 apt） | mm_fp4 cudnn backend 不可用 |
111	| C3 | `cudnn-frontend.backend_version() >= 92100` | 系统 apt `libcudnn9-cuda-12` shadow pip cu13 |
112	| C4 | torch `2.11.0+cu130`、cuda 可用、cc `(12, 0)` | torch 升级失败 |
113	| C4b | `uv pip list` 无 `-cu12` 包 | pip 层 cu12 残留 |
114	| C5 | sgl_kernel Marlin FP4 符号可导入 | common_ops.abi3.so 不匹配 torch 2.11 |
115	| C6 | sparse_kernel_extension `get_block_table_v2/v3` | prebuilt .so 损坏 |
116	| C7 | `infllm_v2.C` 可 import | prebuilt .so 损坏 |
117	| C8 | `flashinfer.mm_fp4(..., backend='cutlass')` smoke | AOT 目录填充失败或 libcudart 解析失败 |
118	| C9 | `flashinfer.mm_fp4(..., backend='cudnn')` smoke | cuDNN 9.21 未装 / libcudart 冲突 |
119	| C10 | `import sglang` from custom editable path | editable 未生效 |
120	| C11 | `~/.cache/flashinfer/.../cached_ops/` 必备 op 全有 | cache 未正确拷贝 |
121	
122	### 4.3 已踩坑清单
123	
124	| 坑 | 表现 | 修法 |
125	|---|---|---|
126	| pip resolver 双版本 torch | `uv pip install` 悄悄降级 | 严格 `==` pin + `--no-deps` + `--no-index --find-links wheels/` |
127	| bcecmd "Session Token not valid" | `Sts` 行残留 | 删 `~/.go-bcecli/credentials` `Sts = bj` 行 |
128	| bcecmd "Access Denied" | AK 少尾字母 `u` | 完整 `ALTAKeWYPVdISZK7DE1E2e32eu` |
129	| apt purge 0 removed | `libcublas-12-9` 依赖 | `dpkg --purge --force-all` |
130	| C8 `nvcc: not found` | prebuilt fp4 GEMM `.so` 没 RPATH，JIT 触发 ninja | AOT 目录机制 skip JIT |
131	| die 后评测继续 | 外层 subshell `(exit)` 只杀 subshell | `kill -TERM $$/$PPID` with mode detection |
132	
133	## 5. SGLang fork 升级判定
134	
135	**结论：不上整包升 v0.5.8+**。
136	
137	fork 基线 = sglang **v0.5.7**（pyproject 锁 `flashinfer==0.5.3`、`sgl-kernel==0.3.20`、`torch==2.9.1` 精确匹配 v0.5.7）。运行时 flashinfer 实际是 0.6.8.post1（被 `--no-deps` 强升），但上层 SGLang dispatch 仍是 v0.5.7。
138	
139	### 5.1 v0.5.8 → v0.5.10 特性筛选
140	
141	| 特性 | 适用？ | 结论 |
142	|---|---|---|
143	| FA4 attention backend (#20303) | ❌ | sm_100 only，依赖 TMEM；sm_120 无 |
144	| flashinfer #2460 sm_120 FP4 GEMM 扩 tile 池 | ✅ | 已在 0.6.8.post1 生效，已落地 autotune（见 `gemm/kernels-sm120.md` §7.1） |
145	| DeepEP / fused MoE / MLA | ❌ | dense GQA + InfLLM-v2，不是 MoE/MLA |
146	| FlashInfer PoolingCache refactor | 🟡 | 我们 `SGLANG_MINICPM_PLAN_CACHE` 实现更激进，不回退 |
147	| radix cache v2 | ❌ | bench 每档清 cache，无收益 |
148	| TP>1 优化 | ❌ | TP=1 |
149	| EAGLE3 chain verify 改进 | 🟡 | 我们 `eagle_worker_v2.py` 自改，cherry-pick 冲突 |
150	| overlap scheduler v2 | 🟡 | 需大量 API 适配，ROI 不明 |
151	
152	### 5.2 不升级的理由
153	
154	1. fork 已深度定制：`modelopt_quant.py`（hybrid Marlin dispatch）、`minicpm_backend.py`（CUDA graph fix / GLA fused）、`minicpm_sparse_utils.py`（fast_level_from_cpu）、`eagle_worker_v2.py`（chain verify 改写）
155	2. v0.5.8+ 收益集中 MoE / MLA / TP>1，dense + TP=1 + GQA + InfLLM-v2 + sm_120 上游几乎不触达
156	3. 当前瓶颈在 kernel 而非调度（target forward GPU 主导，见 `decode/history.md`）
157	
158	### 5.3 后续观察点
159	
160	- sglang 是否原生支持 flashinfer autotune cache 持久化（当前自己 `load_configs()`）
161	- flashinfer 是否扩 sm_120 FP4 GEMM tile 池（>3 tile，可能让 gate_up / o_proj 1.06× → 1.2×）
162	- cutlass-dsl 4.5.0 stable 发布（b12x 集成验证通过但 `SGLANG_ENABLE_B12X=0`）
163	- sm_120 兼容 FA 新版本（绕过 TMEM）
164	
165	## 6. cu13 + sm_120 NVFP4 Kernel 生态
166	
167	| 项目 | 最新 | sm_120 + cu13 | 结论 |
168	|---|---|---|---|
169	| **FlashInfer 0.6.8.post1** | ✅ | 已用 |
170	| CUTLASS 4.4.2 | ⚠️ partial | main HEAD 有 sm_120f 补丁 |
171	| SGLang main | ✅ | issue #19637 sm_120 优化中，与 fork 差距大不 cherry-pick |
172	| vLLM Marlin W4A8 (PR #24722) | ✅ | decode M≤48 可能 >1.5×，需 W4A8 calib，未上 |
173	| TRT-LLM | ❌ | sm_120 NVFP4 cubin 未发布 |
174	| DeepGEMM | ❌ | sm_120 wheel 未发布 |
175	| ThunderKittens 2.0 | ⚠️ | B200-only |
176	
177	**NVFP4 W4A4 attention 是行业空白**：所有项目只有 GEMM，attention 仍跑 bf16。短期无可用 kernel。
178	
179	## 7. 关键参考链接
180	
181	- [cutlass#3096](https://github.com/NVIDIA/cutlass/issues/3096) sm_120 NVFP4 fix with `compute_120f`
182	- [vllm#36865](https://github.com/vllm-project/vllm/issues/36865) cu13 源码编译未指定 `120a/120f` 掉速陷阱
183	- [flashinfer#2577](https://github.com/flashinfer-ai/flashinfer/issues/2577) sm_120 NVFP4 mm_fp4 cu12 broken / cu13 fix
184	- [vllm forum](https://discuss.vllm.ai/t/sm120-rtx-pro-4000-6-5x-throughput-gain-and-v0-18-1-regression-findings/2525) sm_120 NVFP4 Marlin +17% 实测
185	- [SGLang #19637](https://github.com/sgl-project/sglang/issues/19637) sm_120 优化计划
186
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/platform/cu13-stack.md",
  "old_string": "## 4. probe-sala 提交包流水（云评测环境一次过）\n\n`probe-sala/` 是面向评测平台的**一次性、无 fallback、BOS 鉴权下发**的 cu13 安装包，与 demo-sala（增量升级）路径分离。专门用于平台环境复现本地已验证栈。\n\n### 4.1 设计要点\n\n1. **BOS 鉴权下载**（替代 pypi / pytorch.org 兜底）：bcecmd 拉 92 wheel + 3 torch wheel，2.8 GB，缺一个就 `exit 1`\n2. **cu12 彻底清理**：`dpkg --purge --force-all` 绕过依赖、连带删 `/usr/local/cuda-12*` 和 `/etc/ld.so.conf.d/988_cuda-12.conf`\n3. **flashinfer AOT skip JIT**：把 prebuilt `*.so` 拷到 `site-packages/flashinfer/data/aot/<name>/<name>.so`，flashinfer 检测 aot_path 直接 `load`，不调 ninja。评测机不需要 nvcc\n4. **失败强制终止**：检测 sourced/executed 模式，`kill -TERM ${KILL_TARGET}` 把平台 shell 一并杀掉，不能让评测继续\n\n### 4.2 verify_env.py 11 项\n\n| # | 检查 | 失败含义 |\n|---|---|---|\n| C1 | `libcudart.so.13` 存在且无 `.so.12` 进 ldconfig | cu12 purge 残留 |\n| C2 | pip cuDNN 9.21+（不是系统 apt） | mm_fp4 cudnn backend 不可用 |\n| C3 | `cudnn-frontend.backend_version() >= 92100` | 系统 apt `libcudnn9-cuda-12` shadow pip cu13 |\n| C4 | torch `2.11.0+cu130`、cuda 可用、cc `(12, 0)` | torch 升级失败 |\n| C4b | `uv pip list` 无 `-cu12` 包 | pip 层 cu12 残留 |\n| C5 | sgl_kernel Marlin FP4 符号可导入 | common_ops.abi3.so 不匹配 torch 2.11 |\n| C6 | sparse_kernel_extension `get_block_table_v2/v3` | prebuilt .so 损坏 |\n| C7 | `infllm_v2.C` 可 import | prebuilt .so 损坏 |\n| C8 | `flashinfer.mm_fp4(..., backend='cutlass')` smoke | AOT 目录填充失败或 libcudart 解析失败 |\n| C9 | `flashinfer.mm_fp4(..., backend='cudnn')` smoke | cuDNN 9.21 未装 / libcudart 冲突 |\n| C10 | `import sglang` from custom editable path | editable 未生效 |\n| C11 | `~/.cache/flashinfer/.../cached_ops/` 必备 op 全有 | cache 未正确拷贝 |\n\n### 4.3 已踩坑清单\n\n| 坑 | 表现 | 修法 |\n|---|---|---|\n| pip resolver 双版本 torch | `uv pip install` 悄悄降级 | 严格 `==` pin + `--no-deps` + `--no-index --find-links wheels/` |\n| bcecmd \"Session Token not valid\" | `Sts` 行残留 | 删 `~/.go-bcecli/credentials` `Sts = bj` 行 |\n| bcecmd \"Access Denied\" | AK 少尾字母 `u` | 完整 `ALTAKeWYPVdISZK7DE1E2e32eu` |\n| apt purge 0 removed | `libcublas-12-9` 依赖 | `dpkg --purge --force-all` |\n| C8 `nvcc: not found` | prebuilt fp4 GEMM `.so` 没 RPATH，JIT 触发 ninja | AOT 目录机制 skip JIT |\n| die 后评测继续 | 外层 subshell `(exit)` 只杀 subshell | `kill -TERM $$/$PPID` with mode detection |\n\n## 5. SGLang fork 升级判定",
  "new_string": "## 4. probe-sala（已退役）\n\n原 `probe-sala/` 是面向评测平台的一次性、无 fallback、BOS 鉴权下发的 cu13 安装包，与\n`demo-sala/`（增量升级）路径分离。**当前 `probe-sala/` 目录已删（commit `b74c10d`），统一走\n`demo-sala/prepare_env.sh`**，平台 JIT 故障的 AOT 修复见\n[`trtllm-utils-aot-fix.md`](trtllm-utils-aot-fix.md)。\n\n仍活跃的 `probe-sala-s2/` 是 K8s pod 反向 SSH sidecar（authorized_keys 注入 + dropbear + frpc），\n跟提交流程无关。设计要点 / verify 项 / 已踩坑清单全部在 git history（`probe-sala/` deleted 之前\n的 commit）。\n\n## 5. SGLang fork 升级判定"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/platform/cu13-stack.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/platform/README.md"
}
```

> TOOL

tool_result Read
```
1	# Platform
2	
3	平台 / 环境栈 / 部署流水。
4	
5	| 文档 | 内容 |
6	|---|---|
7	| [cu13-stack.md](cu13-stack.md) | 当前生产栈版本表、cu12→cu13 升级要点（已完成）、回滚 SOP、probe-sala 平台部署流水、SGLang fork 升级判定、cu13+sm_120 NVFP4 kernel 生态 |
8	| [eval-vs-dev-environment-audit.md](eval-vs-dev-environment-audit.md) | 评测机（K8s pod）vs 开发机（docker）28 节深度对比；ulimit / swap / cuda 安装 / pip diff；reverse SSH ad-hoc 调试 SOP |
9	| [trtllm-utils-aot-fix.md](trtllm-utils-aot-fix.md) | `Skipped 6 unsupported tactic(s) for fp4_gemm` 根因（平台缺 `/usr/local/cuda`）+ AOT prebuild 修复 + `FLASHINFER_LOGGING_LEVEL=debug` 诊断方法 |
10	
11	跨主题：
12	- 量化方案 → [`../quant/`](../quant/)
13	- decode/prefill 性能 → [`../decode/`](../decode/) / [`../prefill/`](../prefill/)
14
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/platform/README.md",
  "old_string": "| [cu13-stack.md](cu13-stack.md) | 当前生产栈版本表、cu12→cu13 升级要点（已完成）、回滚 SOP、probe-sala 平台部署流水、SGLang fork 升级判定、cu13+sm_120 NVFP4 kernel 生态 |",
  "new_string": "| [cu13-stack.md](cu13-stack.md) | 当前生产栈版本表、cu12→cu13 升级要点（已完成）、回滚 SOP、SGLang fork 升级判定、cu13+sm_120 NVFP4 kernel 生态。原 probe-sala 流水已退役（commit b74c10d） |"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/platform/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "11",
  "status": "completed"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #11 status
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "12",
  "status": "in_progress"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #12 status
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/prefill/README.md"
}
```

> TOOL

tool_result Read
```
1	# Prefill
2	
3	长上下文 prefill 优化。
4	
5	| 文档 | 内容 |
6	|---|---|
7	| [current.md](current.md) | prefill 当前事实：热点、默认优化、运行 SOP、最新 profile 结论 |
8	| [history.md](history.md) | 历史调研：trtllm kernel swap、nsys 硬件级 profile、infllmv2 blockmask 修复、已枯竭路线 |
9	
10	跨主题：
11	- decode/runtime 性能 → [`../decode/`](../decode/)
12	- 量化 / Marlin → [`../quant/`](../quant/)
13	- EAGLE-3 spec decoding → [`../eagle/`](../eagle/)
14
```

> TOOL

tool_use Bash
```json
{
  "command": "head -50 piecewise/README.md && echo \"===\" && head -50 prefill/README.md",
  "description": "scan workspace READMEs to write index"
}
```

> TOOL

tool_result Bash
```
# Piecewise CUDA Graph Prefill 调查 + 实施方案

深度代码调查产出。目标：启用 SGLang `--enable-piecewise-cuda-graph` 加速我们的 prefill 路径。

## 文档索引

| 文件 | 内容 |
|---|---|
| [mechanism.md](mechanism.md) | SGLang piecewise 完整机制 — replay 路径、split_gm、CUDAPiecewiseBackend、replay_prepare 怎么 padding |
| [audit.md](audit.md) | 逐 op 兼容性审计 — 哪些已 graph-friendly、哪些要改、sparse metadata / FlashInfer plan cache 寿命 |
| [blockers.md](blockers.md) | 三个 hard blocker 和具体改法（GLA split op / attention_layers 收集 / MLP cache 预热）|
| [plan.md](plan.md) | 阶段化实施方案 + 风险矩阵 + go/no-go checkpoint |

## 一句话现状

- 我们当前 **没有启用**。`SGLANG_SERVER_ARGS` 只有 `--chunked-prefill-size 8192`（scheduler 层 chunked prefill），不是 piecewise CUDA graph
- 启用入口：`--enable-piecewise-cuda-graph`（默认 False，`server_args.py:573`）
- 启用难点：3 个 hard blocker，工程量 2-3 天
- 收益上限：单 batch wall **< 0.3%（< 21ms / 7s）**，但有基础设施价值（latency jitter、为 Inductor 路径打底、对齐上游）

## 决策框架

| 真正的判定点 | 做法 |
|---|---|
| 阶段 0 实测：GPU util > 95% | **abort** — launch overhead 已 overlap，piecewise 零收益 |
| 阶段 1：capture 跑不通且修不掉 | abort |
| 阶段 2：数值漂移（mcq 通过率掉 > 1%）| abort |
| 阶段 3：wall 收益 < 0.5% | 评估是否进 inductor，否则**冻结为基础设施保留** |

## 重要前置事实

1. **piecewise 只影响 prefill EXTEND 路径**。decode / spec verify 走 decode CUDA graph，与本工作完全无关。
2. **attention 是 split point，eager 跑**。所有 sparse metadata / FlashInfer plan cache / topk-to-FI-indices 持久 buffer / InfLLM stage1/stage2 — 完全不变。
3. **非 attention 部分按 bucket capture**。我们 `chunked_prefill_size=8192` 时约 94 个桶。
4. **基座 + 量化方案不变**。

===
# Prefill Project

This directory is the working area for main-test prefill research.

Scope is intentionally narrow:

- Optimize prompt processing in the official speed benchmark path.
- Treat long requests filtered or rejected by the benchmark/server length rules as competition protocol, not a bug to fix.
- Do not use speculative decoding, draft models, or decode throughput as evidence for this project.
- Keep accuracy and long-context answer quality as hard acceptance gates for any approximate idea.

## Documents

| File | Purpose |
|---|---|
| [main-test.md](main-test.md) | 官方 speed benchmark 实际发什么、测什么、长请求过滤行为。 |
| [roadmap.md](roadmap.md) | Bounding conclusion + 已探索方向小结。 |
| [experiment-log.md](experiment-log.md) | Append-only 实验日志（按日期/主题）。 |
| [stage1-profile.md](stage1-profile.md) | line91 tail shape stage1 离线 profile（历史归档）。 |
| [stage1-groupmax-design.md](stage1-groupmax-design.md) | `prob_groupmax_sum` tile candidate kernel 设计（受 SMEM 矛盾阻塞）。 |
| `*.py` | offline profiler / recall sweep / microbench 脚本，命名见对应日志 section。 |

## Current Decision

The priority is not to make every nominal 524K row enter prefill. Some rows can be pruned by `sglang.bench_serving` or rejected by server-side maximum input length checks; this is part of the benchmark design. We should measure and optimize the requests that are actually admitted by the official wrapper.

Therefore:

- Do not enable `--allow-auto-truncate` as a speed optimization.
- Do not change dataset filtering to admit more oversized rows.
- Do not count rejected/filtered rows as prefill performance regressions.
- Do record admitted request count, benchmark duration, and any non-length failures for every run.

## Main Entry Points

- Submission args: `demo-sala/prepare_env.sh`
- Official wrapper: `toolkit/bench_serving.sh`
- Pure prefill microbench: `bench/kernels/prefill/prefill_bench_smax64.py`
- Current prefill facts: `docs/prefill/current.md`
- Historical dead ends: `docs/prefill/history.md`

## Baseline Workload Facts

`bench/data_full/` is local/untracked at the time of writing, but it is the most relevant local proxy for the main speed test:

| Dataset | Rows | Avg prompt tokens | Max prompt tokens | 8192-chunk total | >=500K rows |
|---|---:|---:|---:|---:|---:|
| `speed_bench_c1.jsonl` | 12 | 178903.5 | 524287 | 265 | 2 |
| `speed_bench_c8.jsonl` | 36 | 177302.6 | 524288 | 791 | 6 |
| `speed_bench_cunlimited.jsonl` | 96 | 171791.8 | 524288 | 2050 | 16 |
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/prefill/current.md",
  "offset": 1,
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	# Prefill 优化当前事实
2	
3	目标场景：长上下文 prefill，`--chunked-prefill-size 8192`，`--dense-as-sparse`，`minicpm_flashinfer`。线上快速样本：`bench/data/speed_bench_cunlimited.jsonl` line 39 / index 39，约 15 chunks，`max_tokens=1`。最终大 bench：
4	
5	```bash
6	python3 bench/kernels/prefill/prefill_bench_smax64.py
7	```
8	
9	## 1. 当前热点
10	
11	profile 口径：`SGLANG_MINICPM_PROFILE=1 SGLANG_MINICPM_PROFILE_INTERVAL=16`。
12	
13	最新真实 15chunk full-chunk profile（line 39，`mars=0`，`max_tokens=1`）：
14	
15	| 模块 | 现象 |
16	|---|---|
17	| MLP | `133ms/chunk`：`gate_up≈70ms` + `act_quant_down_fused≈63ms`（已 fuse） |
18	| GLA | `120ms/chunk`：`gla_qkv≈45ms` + `gla_chunk_kernel≈27-30ms` |
19	| `extend_sparse_fa` | 8 sparse layer × `9.8-10.0ms`，`84ms/chunk` |
20	| `stage1_score` | 末段 `74ms/chunk`，离线单层 ctx=131072 ≈ `10.38ms` |
21	| FlashInfer plan / sparse metadata | layer/chunk cache 后压平，残余主要是首 chunk + 尾 shape |
22	
23	15chunk wall 当前稳态约 **7.0-7.4 s**（`max_tokens=1`）。
24	
25	**硬边界**：不能再把 topk/candidate 缩限作为优化方向。任何减少候选集合、截断 topk、近似 fused topk 默认不满足一致性，除非先证明它与完整语义逐 token/topk 完全一致。
26	
27	## 2. 已落地默认优化
28	
29	每条均默认开启；env 是回退/调试旋钮。
30	
31	### 2.1 FlashInfer plan cache
32	
33	代码：`demo-sala/sglang/python/sglang/srt/layers/attention/minicpm_attention_kernels.py`
34	
35	| env | 默认 | 作用 |
36	|---|---:|---|
37	| `SGLANG_MINICPM_PLAN_CACHE` | `1` | 启用 sparse FA plan 复用 |
38	| `SGLANG_MINICPM_DISABLE_CROSS_CHUNK_PLAN_CACHE` | `0` | 1=禁跨 chunk，仅保留 layer 内 |
39	| `SGLANG_MINICPM_CROSS_FORWARD_BUFFER_REFRESH` | `1` | 跨 forward 命中时刷新 wrapper page-table buffer，不重新 plan |
40	
41	关键语义：跨 forward 复用 plan 时必须刷新 `wrapper._paged_kv_indptr_buf` / `_paged_kv_indices_buf` / `_paged_kv_last_page_len_buf`，否则 stale page table 会导致 cross-request KV contamination。
42	
43	### 2.2 全 sparse metadata 快路径
44	
45	代码：`minicpm_sparse_utils.py`
46	
47	| env | 默认 |
48	|---|---:|
49	| `SGLANG_MINICPM_ALL_SPARSE_PREFILL_METADATA` | `1` |
50	
51	仅当 `len(sparse_bs_list) == bs` 启用：`sparse_cu_seqlens_q_cpu = arange`，`sparse_page_table = empty`（后续整张覆盖），token mapping 向量化，page-table 写用 slice 替换高级索引。混合 batch 走原逻辑。
52	
53	### 2.3 sparse seqlens 从 topk 派生
54	
55	代码：`minicpm_backend.py`
56	
57	| env | 默认 |
58	|---|---:|
59	| `SGLANG_MINICPM_DERIVED_SPARSE_SEQLENS` | `1` |
60	
61	不能固定成 `num_sparse_topk_tokens`（early token 会被 causal 截断）。按 `topk_idx` / `token_pos_in_bs` / `seqlen_k_sparse_bs` / `block_size` 复现 `get_block_table_v2` 的有效长度：
62	
63	```python
64	limit = min(seqlen_k_sparse_bs[token_bs], token_pos_in_bs)
65	valid_len = clamp(limit - topk_idx * block_size, 0, block_size)
66	sparse_seqlen = sum(valid_len over topk blocks)
67	```
68	
69	验证：synthetic + 线上 8 sparse layer `bad=0 max_abs=0`。
70	
71	### 2.4 direct sparse page table
72	
73	代码：`minicpm_backend.py`
74	
75	| env | 默认 |
76	|---|---:|
77	| `SGLANG_MINICPM_DIRECT_SPARSE_PAGE_TABLE` | `1` |
78	
79	全 sparse 下 `sparse_kernel_extension.get_block_table_*` 输出已是完整 page table，跳过 `metadata.sparse_page_table[...] = ...` 复制。混合 batch 仍走原合并。
80	
81	### 2.5 stage1 actual maxlen + direct pool + skip extra zero
82	
83	代码：`minicpm_sparse_utils.py`
84	
85	| env | 默认 | 作用 |
86	|---|---:|---|
87	| `SGLANG_MINICPM_STAGE1_ACTUAL_MAXLEN` | `1` | `infllmv2_attn_stage1` 用实际 K1 长度 |
88	| `SGLANG_MINICPM_STAGE1_DIRECT_POOL` | `1` | actual score 覆盖 topk 候选时直接 pool/topk |
89	| `SGLANG_MINICPM_STAGE1_SKIP_EXTRA_ZERO` | `1` | 跳过 wrapper 对 score tensor 的二次 `p.zero_()` |
90	
91	边界：
92	
93	- 可以缩 `infllmv2_attn_stage1.max_seqlen_k`。
94	- **不能**缩 `max_pooling_1d_varlen.max_context_len`：旧 `compressed_max_seqlen_k` 精度问题来自 pooler layout/边界语义。
95	- 首 chunk / early chunk 候选不足时必须回到 full-layout scratch。
96	
97	验证：离线 `cache=4096/16384/65536` direct-pool 与 full-layout `diff=0`；`cache=0` 不一致（guard 必保留）；ctx=131072 stage1 对拍 `bitwise=True`；ctx=131072 单层 `10.389→10.227ms`。
98	
99	### 2.6 prefill block table v3
100
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"^## \" docs/prefill/current.md",
  "description": "prefill/current.md sections"
}
```

> TOOL

tool_result Bash
```
9:## 1. 当前热点
27:## 2. 已落地默认优化
278:## 3. 已否决路线
501:## 4. 后续工作流
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/prefill/current.md",
  "offset": 501
}
```

> TOOL

tool_result Read
```
501	## 4. 后续工作流
502	
503	每个新优化必须留下：
504	
505	1. profile 证据（哪里热）。
506	2. 离线一致性（启用 shape + 边界 shape）。
507	3. 在线 debug 一致性（真实请求路径打印命中）。
508	4. smoke：`mars=0`, `max_tokens=200`，输出是人话。
509	5. 15chunk bench：line 39，`max_tokens=1`；不再调用 `/flush_cache`（接口易超时，当前流程按 no-flush 口径记录）。
510	6. profile 复核：热点确实下降，没转成新热点。
511	7. 文档 + commit：可复现命令、关键结果、风险边界。
512	
513	常用启动：
514	
515	```bash
516	EAGLE_MARS_THETA=0 EAGLE_D5_MARS_THETA=0 EAGLE_D7_MARS_THETA=0 \
517	SGLANG_MINICPM_PROFILE=1 SGLANG_MINICPM_PROFILE_INTERVAL=16 \
518	bash eval/start_eagle.sh
519	```
520	
521	停服：
522	
523	```bash
524	bash bench/kill_sglang.sh
525	```
526	
527	用户明确不要 kill 正在用的 server 时必须等待，不做重启验证。
528
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/prefill/current.md",
  "old_string": "用户明确不要 kill 正在用的 server 时必须等待，不做重启验证。",
  "new_string": "用户明确不要 kill 正在用的 server 时必须等待，不做重启验证。\n\n## 5. 仓内深度调研工作区\n\n不在 `docs/` 下，但与 prefill 路径强相关，结论是其他文件的事实来源：\n\n| 路径 | 范围 | go/no-go |\n|---|---|---|\n| [`/user_4813494d/openbmb/piecewise/`](../../piecewise/) | SGLang `--enable-piecewise-cuda-graph` 接入审计：机制、逐 op 兼容性、3 个 hard blocker、阶段化实施 | 单 batch wall 收益 **< 0.3%**（< 21ms / 7s），冻结为基础设施保留，不进生产 |\n| [`/user_4813494d/openbmb/prefill/`](../../prefill/) | main-test 速度 bench 的真实 prefill bounding：stage1 / stage2 / MLP / GLA 各模块剩余空间，含 admitted-request 形态分析 | wall=54.97s @ 524K 的 bounding 结论；stage1-profile / stage1-groupmax-design / experiment-log（95KB append-only） |\n\n跨工作区不要再做\"piecewise 能不能给 wall 加速\"或\"stage1 还能不能再砍\"类调研——上面 bounding 已锁。\n新方向起步前先扫一遍这两份目录的 `roadmap.md` / `blockers.md` 防重踩。"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/prefill/current.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/prefill/README.md",
  "old_string": "| 文档 | 内容 |\n|---|---|\n| [current.md](current.md) | prefill 当前事实：热点、默认优化、运行 SOP、最新 profile 结论 |\n| [history.md](history.md) | 历史调研：trtllm kernel swap、nsys 硬件级 profile、infllmv2 blockmask 修复、已枯竭路线 |\n\n跨主题：\n- decode/runtime 性能 → [`../decode/`](../decode/)\n- 量化 / Marlin → [`../quant/`](../quant/)\n- EAGLE-3 spec decoding → [`../eagle/`](../eagle/)",
  "new_string": "| 文档 | 内容 |\n|---|---|\n| [current.md](current.md) | prefill 当前事实：热点、默认优化、已否决路线、运行 SOP、深度调研工作区索引 |\n| [history.md](history.md) | 历史调研：trtllm kernel swap、nsys 硬件级 profile、infllmv2 blockmask 修复、已枯竭路线 |\n\n仓内调研工作区（不在 docs 下，但属 prefill 路径事实来源）：\n\n- [`/user_4813494d/openbmb/piecewise/`](../../piecewise/) — `--enable-piecewise-cuda-graph` 接入审计，结论 wall 收益 < 0.3%\n- [`/user_4813494d/openbmb/prefill/`](../../prefill/) — main-test bench bounding（stage1/stage2/MLP/GLA 各模块剩余空间）\n\n跨主题：\n- decode/runtime 性能 → [`../decode/`](../decode/)\n- 量化 / Marlin → [`../quant/`](../quant/)\n- EAGLE-3 spec decoding → [`../eagle/`](../eagle/)"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/prefill/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "12",
  "status": "completed"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #12 status
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "13",
  "status": "in_progress"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #13 status
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/decode/current.md"
}
```

> TOOL

tool_result Read
```
1	# Decode 当前事实与 SOP
2	
3	Decode 期算子优化的工作流、当前热点、已落地清单。详细调查过程与已枯竭路线在 [`history.md`](history.md)。
4	
5	## 1. 当前事实（2026-04-23 node-trace 基线）
6	
7	`--cuda-graph-trace=node` 重测 mini_bench（S1=8 + S8=24，profile 窗 584s）：
8	
9	| 指标 | 值 | 含义 |
10	|---|---|---|
11	| GPU union-busy | **82.3%** | 任意 stream 在跑 kernel 的时间占比 |
12	| 全局 GPU idle | 17.7% | |
13	| └ host-wait | 9.64% of window | 下一 kernel 的 CPU launch 晚于 gap 起点（理论可 CPU 优化）|
14	| └ tiny <10μs | 5.19% | launch 开销噪声，不可优化 |
15	| └ unknown | 2.77% | OS/driver/PCIe 硬啃不动（细分见 history） |
16	| └ alloc/dep | 0.11% | stream 依赖 |
17	
18	**workload 是 GPU-bound**。CPU 侧优化绝对天花板 = 9.6%，但 host-wait 拆细后 decode 内部真可攻击 ≈ **5.5%**，其中 inter-request bench gap 占 3.94%（生产不存在），单点最大 2.10%（`EV_target_forward`）。
19	
20	→ **CPU 侧优化不再做**。优先攻 GPU critical path。
21	
22	### 1.1 Top GPU kernels（按 GPU 时间）
23	
24	| kernel | calls | GPU 时间 | % window | 说明 |
25	|---|---|---|---|---|
26	| `cutlass::device_kernel`（NVFP4 GEMM） | 49,665 | 59.4 s | **10.17%** | 已用 b12x，继续 tune |
27	| `BatchPrefillWithPagedKVCacheKernel` | 2,683 | 37.5 s | 6.42% | 长 context prefill（不在 decode SOP）|
28	| `index_elementwise_kernel` | 826,622 | 15.4 s | 2.63% | mamba scatter / 通用 fancy index |
29	| `vectorized_elementwise_kernel` | 788,645 | 10.9 s | 1.87% | 通用 pointwise |
30	| `flash_fwd_splitkv_stage1_kernel` | 2,408 | 10.6 s | 1.81% | decode full-attn |
31	| `act_and_mul_kernel` | 9,933 | 5.7 s | 0.97% | |
32	| `RMSNormKernel` | 41,839 | 5.4 s | 0.93% | |
33	| `quantize_with_block_size_tma` | 48,675 | 4.3 s | 0.74% | NVFP4 quant |
34	
35	55,515 kernels/sec（3240 万 / 584s）。**fusion / 扩 CUDA graph 边界**是结构性收益方向。
36	
37	## 2. 迭代 SOP
38	
39	| 层级 | 内容 | 要求 |
40	|---|---|---|
41	| L0 | 离线 bit-exact 对拍 | 必须，覆盖被改 kernel / metadata / 状态搬运 |
42	| L1 | 离线 microbench | 必须，固定 shape/seed，记录 GPU event + wall |
43	| L2 | decode quick bench + profile | 必须，用真实 server 路径确认收益和热点迁移 |
44	| L3 | 生产 mini / full bench | 不纳入快速迭代 SOP |
45	
46	口径：
47	
48	- 不要求在线 token trace 与当前 MARS 完全一致；bit-exact 由离线对拍保证
49	- quick bench 门禁优先看固定输出 token 数下的 `duration_s`；`tok/s` 只作为派生指标
50	- profiler 下 tok/s 偏低；profile 只用于热点排序、CPU/GPU 分解和确认代码路径
51	- E2E 正收益才保留并 commit；负收益回滚生产代码，只记录可复现实验和结论
52	
53	### 2.1 Quick bench
54	
55	```bash
56	# 固定场景
57	python3 bench/decode_quick_bench.py --scenario s8_stable_decode --output outputs/decode_quick_s8.json
58	python3 bench/decode_quick_bench.py --scenario b32_drain_decode --output outputs/decode_quick_b32.json
59	python3 bench/decode_quick_bench.py --scenario longctx_s8_decode --output outputs/decode_quick_longctx_s8.json
60	```
61	
62	固定 token 输出时加 `--ignore-eos`（B12X/Marlin E2E A/B 必加）。
63	
64	| 场景 | 目的 |
65	|---|---|
66	| `s1_long_decode` | S1/D7/长 decode 稳态 |
67	| `s8_stable_decode` | D5 speculative decode 稳态，主 gate |
68	| `b32_drain_decode` | NO_SPEC target decode 稳态 |
69	| `mixed_stop_decode` | 混合 stop/drain batch 变化 |
70	| `longctx_s8_decode` | 长上下文 verify metadata/copy 是否放大 |
71	
72	### 2.2 Profile
73	
74	```bash
75	python3 bench/decode_quick_bench.py \
76	  --scenario s8_stable_decode \
77	  --profile-dir outputs/decode_profile_s8 --profile-prefix s8 \
78	  --profile-by-stage --profile-num-steps 1 \
79	  --output outputs/decode_profile_s8.json
80	
81	python3 bench/decode_trace_breakdown.py outputs/decode_profile_s8 --stage DECODE --limit 30
82	python3 bench/decode_trace_sections.py  outputs/decode_profile_s8 --stage DECODE --prefix DC_ --prefix EW_
83	python3 bench/profile/decode_profile_summary.py outputs/decode_profile_s8 --stage DECODE
84	```
85	
86	`profile_by_stage=True` 必须带 `--profile-num-steps`，否则 server stage counter 可能未初始化。
87	
88	目录约定：
89	
90	- 可提交 microbench 放 `bench/kernels/<domain>/` 或 `bench/b12x/`
91	- 跨场景 profile 辅助放 `bench/profile/`
92	- 临时 JSON / trace 摘要放 `outputs/` 或 `bench/results/local/`，不进 git
93	
94	## 3. Profile 方法论（关键避坑）
95	
96	`history.md` §10 详细记录了几次踩坑全过程。核心规则：
97	
98	### 3.1 nsys 必用 `--cuda-graph-trace=node`
99	
100	默认 `graph` 不展开 graph 内部 kernel。decode forward 全部在 CUDA graph 内 → kernel 不可见 → "看起来 GPU 只有 4%" 是假象。
101	
102	```bash
103	nsys profile -t cuda,nvtx \
104	    --cuda-graph-trace=node \
105	    --capture-range=cudaProfilerApi --capture-range-end=stop \
106	    -o /tmp/prof_xxx -f true --stats=false \
107	    <server-cmd>
108	```
109	
110	### 3.2 CPU 时间 ≠ CPU 工作
111	
112	NVIDIA CUDA Best Practices Guide §8：**CPU time spent in synchronization APIs is actually GPU work attribution, not CPU overhead**.
113	
114	`.tolist()` 在 GPU tensor 上 = 强制 sync。那段 CPU 墙时是 GPU critical path 的 CPU 影像，消掉只是把阻塞从一个 API 挪到另一个，wall time 不变。
115	
116	`EI_ai_tolist` 在 profile 里 85.7% memcpy 时间，按 fix 后 profile 完美打到 1.2%，**e2e 完全无感**。这是教训而非个案。
117	
118	### 3.3 NVTX 归因必须 join RUNTIME_API 拿 launch CPU 时间
119	
120	CUDA kernel 的 GPU end-time 可能在 launch 之后几 ms。用 GPU end-time 匹配 NVTX 会把后续 kernel 的时间张冠李戴到当前 NVTX。**必须 join `CUPTI_ACTIVITY_KIND_RUNTIME` 拿 launch CPU 时间**。
121	
122	```sql
123	SELECT k.demangledName, r.start AS launch_cpu, k.end-k.start AS dur
124	FROM CUPTI_ACTIVITY_KIND_KERNEL k
125	JOIN CUPTI_ACTIVITY_KIND_RUNTIME r ON k.correlationId = r.correlationId;
126	```
127	
128	### 3.4 Idle breakdown 决策树
129	
130	每次 CPU 侧优化候选出来前先过：
131	
132	```
133	Step 0  nsys profile --cuda-graph-trace=node
134	Step 1  GPU 活跃 % = Σ(kernel_duration) / profile_window
135	Step 2  GPU 活跃 ≥ 90%? → 纯 GPU-bound，CPU 侧 ≤ 10%，不做
136	Step 3  否则拆 idle: host-wait / kernel-wait / unknown
137	Step 4  host-wait 占比 = CPU 侧 ROI 天花板
138	Step 5  改完 e2e 再测，profile "账面变好" 不算数
139	```
140	
141	权威出处：CUDA C++ Best Practices Guide §8/§12、Nsight Systems User Guide、Meta HTA Idle Time Breakdown、PyTorch Blog _Trace Analysis for the Masses_。
142	
143	## 4. 已落地优化（按合入顺序）
144	
145	| commit | 优化 | env | 离线 bit-exact / microbench | E2E |
146	|---|---|---|---|---|
147	| `60f2028` | GPU 构造 `retrieve_parent_token`，避免 CPU BFS + GPU copy | `SGLANG_MINICPM_GPU_RETRIEVE_PARENT=1` | 9/9 bit-exact，4.2-14.2× | S8 +0.52% |
148	| `60f2028` | Fuse verify accept compaction（compacted accept_index/verified_id/evict_mask） | `SGLANG_EAGLE_FUSE_VERIFY_ACCEPT_COMPACT=1` | 27/27 bit-exact，3.8-4.1× | S8 +0.14% |
149	| `c33ff2f` | Fuse mamba verify metadata | `SGLANG_EAGLE_FUSE_MAMBA_VERIFY_METADATA=1` | 72/72 bit-exact，3.0-8.8× | S8 -0.30% duration |
150	| `0e6e907` | Fuse mamba verify state copy | `SGLANG_EAGLE_FUSE_MAMBA_VERIFY_STATE_COPY=1` | 29/29 bit-exact；0.7459→0.2260ms | S8 **-4.37%** |
151	| `38d048e` | GLA target-verify initial state indexed load | `SGLANG_EAGLE_GLA_INDEXED_INITIAL_STATE=1` | 10/10 bit-exact，1.10-1.21× | S8 -0.62% |
152	| `203b871` | Fuse verify free slots（page_size=1） | `SGLANG_EAGLE_FUSE_VERIFY_FREE_SLOTS=1` | 18/18 bit-exact，2.43-2.50× | S8 -0.21% |
153	| `e922b76` | SimpleGLA decode BK64 direct-state | `SGLANG_SIMPLE_GLA_DIRECT_DECODE_BK64=1` | bit-exact；B1 14→6.66us，B8 34→14us | **B32 -19.59%**，S8 -0.14% |
154	| `fd73c6d` | SimpleGLA BK64 direct-state 2K variant | `SGLANG_SIMPLE_GLA_DIRECT_DECODE_BK64=1` | bit-exact；B1 7.17→4.11us | B32 -0.88% |
155	| `0c97fac` | Decode sparse metadata 用 CPU `seq_lens_cpu` mirror | 默认 | 语义等价 | **B32 -11.36%** |
156	| `336de12` | NO_SPEC `next_token_ids` pinned CPU buffer 异步 D2H | `SGLANG_EAGLE_NO_SPEC_ASYNC_NEXT_TOKEN_CPU=1` | 输出 token 不变 | B32 -2.08% |
157	| `985a04f` | Draft extend FlashInfer plan 用 CPU `qo/kv_indptr` | `SGLANG_EAGLE_DRAFT_EXTEND_CPU_INDPTR=1` | plan 10.47→0.40ms | B32 -1.24%，S8 -0.68% |
158	| `5799dc5` | Mamba track metadata 向量化 gather | 默认 | bs8/32/36 bit-exact，3-11× | B32 -2.12% |
159	| `59cfcfb` | Sparse decode metadata 全 CPU mirror | 默认 | bit-exact，7.2× | B32 -2.10% |
160	| `ae30acc` | Sparse decode token/input lens 直接 CPU 构造 | 默认 | bit-exact，4× | B32 -0.04% |
161	| `585786d` | Decode `req_to_token` 复用 `seq_lens` 列索引 | 默认 | bit-exact，1.9× | B32 -0.15% |
162	| `5c83e4c` | Sparse replay 跳 `compress_k1/k2` -inf fill | `SGLANG_MINICPM_FILL_COMPRESS_BUFFERS=0` | profile 0.48→0.019ms | B32 -2.65% |
163	| `16176fb` | FlashInfer sparse replay 不做 host sync | `SGLANG_MINICPM_SYNC_AFTER_FLASHINFER_REPLAY=0` | 同 stream 排序 | B32 -0.41% |
164	| `3606aad` | `compress_k` CUDA graph grid 1024→128 | `SGLANG_MINICPM_COMPRESS_K_MAX_GRID_CHUNKS=128` | bit-exact；0.607→0.087ms | B32 -3.79% |
165	
166	### 4.1 算子级（更早合入）
167	
168	| 优化 | Decode 收益 | Prefill 收益 |
169	|---|---|---|
170	| RoPE F32 cast 消除 | 140 us/fwd (3.5×) | 11.2 ms/fwd (4.5×) |
171	| Residual fused multiply-add | 237 us/fwd (2.15×) | 4.4 ms/fwd (5.76×) |
172	| `scale_emb` / `width` 吸收进权重 | 2 kernels 消除 | 284 us/fwd |
173	| In-place sigmoid×mul gate | memory pressure ↓ | — |
174	| GLA backend cleanup | ~24 us | — |
175	| flashinfer mm_fp4 离线 autotune | down_proj M=64 3.59× | — |
176	| **b12x backend + 3-tier dispatch**（`SGLANG_ENABLE_B12X=0` 默认关）| decode GEMM kernel -32.4% | 0 |
177	
178	b12x 详见 [`marlin.md`](../gemm/marlin.md) §7.4 / [`kernels-sm120.md`](../gemm/kernels-sm120.md) §7.4。`SGLANG_ENABLE_B12X` 默认关闭：draft CUDA graph capture 不兼容；即便修好后 EAGLE B32 公平 A/B 只有噪声级（旧轮 fixed-token EAGLE B32 -10.88% / S8 -8.45% 但当时 draft 未隔离，结果不算）。
179	
180	## 5. 健康检查规则
181	
182	- 服务器就绪：日志 `Uvicorn running on` 或 curl `/v1/models`，**不用 `/health`**
183	- 正确性冒烟：发 chat 请求看人话，**不跑 mcq accuracy eval**（NVFP4 在 mcq 强格式下退化为重复 pattern，regex 仍命中假阳）
184	- "输出垃圾"结论前先发 3 条简单 chat：残留长请求或 mcq 格式退化会伪装成 backend bug
185	
186	## 6. 当前下一步候选（按风险/收益）
187	
188	按"bit-exact 风险低 + profile 真实热 + 可 microbench"排序：
189	
190	1. **padded/stable sparse-K 布局**：继续做 native `k_starts + k_lens`，但不直接上当前 TileLang fused decode（K512 自身不 bit-exact）。先做确定性 Triton/CUDA fused score+pool/topk 变体
191	2. **Marlin/B12X 重新划分**：B12X 后续只作研究候选，先补离线 bit-exact + 固定 badcase accept-rate 分布 + per-shape graph replay microbench
192	3. **MARS topk**：确认 `torch.topk(logits, 2)` 是否可用专用 top2 kernel，必须逐 tensor 对拍 `target_predict/top2_token/top2_ratio`
193	4. **Plan A: triton 融合 mamba scatter**（对应 `index_elementwise_kernel` 2.63%）：fusion 路线天然吃 tiny 5.2% + 部分 target_forward Python 开销
194	5. `BatchPrefillWithPagedKVCacheKernel` 6.42% e2e（属 prefill，不在 decode SOP）
195	
196	每轮保留条件不变：离线 bit-exact、microbench 正、quick E2E `duration_s` 正、profile 确认路径、200-token smoke、commit。
197
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/decode/current.md",
  "old_string": "| **b12x backend + 3-tier dispatch**（`SGLANG_ENABLE_B12X=0` 默认关）| decode GEMM kernel -32.4% | 0 |\n\nb12x 详见 [`marlin.md`](../gemm/marlin.md) §7.4 / [`kernels-sm120.md`](../gemm/kernels-sm120.md) §7.4。`SGLANG_ENABLE_B12X` 默认关闭：draft CUDA graph capture 不兼容；即便修好后 EAGLE B32 公平 A/B 只有噪声级（旧轮 fixed-token EAGLE B32 -10.88% / S8 -8.45% 但当时 draft 未隔离，结果不算）。",
  "new_string": "| **b12x backend + 3-tier dispatch**（`SGLANG_ENABLE_B12X=0` 默认关，启用后 lock-in） | decode GEMM kernel -32.4%；启用后 S8 decode +28.5% / bs8-24 +6-12% | 0 |\n\nb12x 详见 [`marlin.md`](../gemm/marlin.md) §7.4 / [`kernels-sm120.md`](../gemm/kernels-sm120.md) §7.4。\n\n**当前 b12x 真实状态**（2026-05-10 R-b12x lock-in 后）：\n\n- kernel 修通：`commit 679017f` Stage A bit-exact（max_diff=0, cos_sim=1.0）、Stage B decode S8 +28.5%；`commit ed8786d` 锁住 marlin_upper=48 + AOT cache（`demo-sala/assets/b12x_aot_cache/`）\n- 提交包默认 OFF：`prepare_env.sh:519` `SGLANG_ENABLE_B12X=\"${SGLANG_ENABLE_B12X:-0}\"`、`eval/start_eagle.sh:53` 同。要启用：`SGLANG_ENABLE_B12X=1 bash eval/start_eagle.sh`\n- 默认 OFF 的理由：EAGLE B32 公平 A/B 收益噪声级，full eval 风险与 lock-in 增益不对称；b12x bucket 64 实验（R-b12x-bucket64）full eval acc -1.06pp 且 wall +8.7%，作为 dead-end 留存 `gemm/changelog.md` 最末段"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/decode/current.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/decode/README.md"
}
```

> TOOL

tool_result Read
```
1	# Decode / Runtime
2	
3	Decode 期算子优化、profile 方法论。
4	
5	| 文档 | 内容 |
6	|---|---|
7	| [current.md](current.md) | decode 当前事实（GPU-bound 82.3%、host-wait 上限 5.5%）、迭代 SOP、quick bench、profile 方法论、已落地清单 |
8	| [history.md](history.md) | profile 误归因事故（`alloc_sparse_new_positions` / `EI_ai_tolist`）、教训、已枯竭路线 |
9	
10	跨主题：
11	- 量化 / Marlin / b12x → [`../quant/`](../quant/)
12	- prefill 性能 → [`../prefill/`](../prefill/)
13	- EAGLE-3 → [`../eagle/`](../eagle/)
14
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/decode/README.md",
  "old_string": "跨主题：\n- 量化 / Marlin / b12x → [`../quant/`](../quant/)\n- prefill 性能 → [`../prefill/`](../prefill/)\n- EAGLE-3 → [`../eagle/`](../eagle/)",
  "new_string": "跨主题：\n- 量化 NVFP4 校准 → [`../quant/`](../quant/)\n- sm_120 GEMM / Marlin / b12x kernel 调优 → [`../gemm/`](../gemm/)\n- prefill 性能 → [`../prefill/`](../prefill/)\n- EAGLE-3 → [`../eagle/`](../eagle/)"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/decode/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "13",
  "status": "completed"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #13 status
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "14",
  "status": "in_progress"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #14 status
```

> TOOL

tool_use Bash
```json
{
  "command": "wc -l docs/gemm/*.md docs/gemm/bottleneck_cards/*.md",
  "description": "gemm file sizes"
}
```

> TOOL

tool_result Bash
```
61 docs/gemm/README.md
  1338 docs/gemm/changelog.md
   197 docs/gemm/charter.md
   153 docs/gemm/current.md
   309 docs/gemm/dead-ends.md
   163 docs/gemm/hardware.md
   342 docs/gemm/kernels-sm120.md
   195 docs/gemm/marlin.md
   586 docs/gemm/methodology.md
   113 docs/gemm/roadmap.md
   110 docs/gemm/so-replacements.md
   199 docs/gemm/sol_table.md
   191 docs/gemm/todo.md
    91 docs/gemm/bottleneck_cards/01_o_proj_std_M48.md
   106 docs/gemm/bottleneck_cards/02_down_proj_M128.md
  4154 total
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/gemm/README.md"
}
```

> TOOL

tool_result Read
```
1	# sm_120 GEMM/Kernel 底层调优
2	
3	range：CUTLASS NVFP4 GEMM + Marlin W4A16 GEMM 在 NVIDIA RTX 6000D (sm_120, Blackwell consumer) + 容器云 + ncu SKU 锁环境下的底层调优。**只做 CUTLASS 和 Marlin**，不脱离。
4	
5	> **调优契约**：所有动作必须遵守 [methodology.md](methodology.md) §0 的 4 条契约。Stage 0-3 产出物缺失 = 不允许 patch。
6	
7	## 文档结构（按方法论 SOP 阶段组织）
8	
9	| 文档 | 阶段 | 内容 |
10	|---|---|---|
11	| **[methodology.md](methodology.md)** | 全局 SOP | Stage 0-7 工作流契约 + 容器云 5 阶段测量 + 第一性原理 + 5 正交模块 + 反模式 + 工具分级 |
12	| **[dead-ends.md](dead-ends.md)** | 全局 | 失败模式 catalog + 废弃方向（看到立刻拒）+ 伪实证标志 + 演化判定 |
13	| **[charter.md](charter.md)** | Stage 0 | 目标 shape 直方图 + 双指标（端到端 + kernel SOL%）+ 约束 |
14	| **[hardware.md](hardware.md)** | Stage 1 | 14 物理常数 + 占用三约束 + 硬约束/软目标 + 已知坑 |
15	| **[sol_table.md](sol_table.md)** | Stage 2 | 54 (shape, M) 物理下限 + 当前 SOL% + gap |
16	| **[baseline_*.md](.)** | Stage 3 | reference baseline 6 件套归档（每次大改前重新 lock-in）|
17	| **[changelog.md](changelog.md)** | Stage 5 | 每轮一行：假设 / 预期 / 实测 / 解释 / artifact |
18	| **[validation_*.md](.)** | Stage 6 | 5 项验证 checklist（跨 shape / 数值 / cuda graph / autotune / 长稳） |
19	| [current.md](current.md) | 现状快照 | 当前 .so 静态分析 + dequant.h 路径 + CUTLASS 4.2.0 内嵌 |
20	| [marlin.md](marlin.md) | 历史调优 | Marlin / b12x 调优记录、SASS 分析、`220c18cc` vs `32d27c7` 兼容性警告 |
21	| [kernels-sm120.md](kernels-sm120.md) | 历史调优 | sm_120 NVFP4 GEMM 实测 peak 1467 TFLOPS + 各库对比 + flashinfer autotune 落地 |
22	| [so-replacements.md](so-replacements.md) | 工程 | `.so` 替换日志 + 备份目录索引 |
23	| [roadmap.md](roadmap.md) | 攻击优先级 | 基于 SOL gap 的攻击点排序（依赖 sol_table.md 而不是 commit 模仿） |
24	
25	## 当前 SOP 状态（参考 methodology.md §12）
26	
27	| Stage | 状态 |
28	|---|---|
29	| 0 Charter | ❌ 缺 |
30	| 1 硬件常数表 | ⚠️ 部分（散在 current/kernels-sm120） |
31	| 2 SOL 表 | ❌ 缺（54 个物理下限未算） |
32	| 3 Reference Baseline | ⚠️ 部分（.so 备份在，6 件套不全） |
33	| 4 瓶颈识别 | ⚠️ 部分（marlin/kernels-sm120 有零散数据，无瓶颈卡片） |
34	| 5 单变量改动循环 | ❌ 等 Stage 0-3 |
35	| 6 验证 lock-in | ⚠️ 部分（so-replacements 流程在，6 件套不全） |
36	| 7 Deploy + Monitor | ⚠️ 部分（quick_validate 已建立基线，无 control chart） |
37	
38	## 速查（基于实证，无被推翻结论）
39	
40	| 结论 | 实证来源 |
41	|---|---|
42	| 当前 sgl-kernel `common_ops.abi3.so` 编译目标 = **sm_120a**（74 cubins，无 PTX，原生 NVFP4 mma） | `cuobjdump --list-elf`（[current.md](current.md) §1） |
43	| sgl-kernel 0.3.20 内嵌 **CUTLASS 4.2.0**（commit `57e3cfb`），FlashInfer 0.6.8.post1 内嵌 4.4.2 | sgl-kernel `CMakeLists.txt:50` |
44	| sm_120 NVFP4 BlockScaled GEMM **物理上无独立 PingPong path**（pingpong 文件只走 dense 非 BlockScaled） | A 路读 CUTLASS 4.4.2 源码 |
45	| sm_120 NVFP4 unscaled mma peak ≈ **1467 TFLOPS**（实测 pure_mma_peak）；scaled 慢 3× 是 ISA 硬开销 | [kernels-sm120.md](kernels-sm120.md) §2 |
46	| 当前 sgl-kernel/CUTLASS/cuDNN/cuBLAS NVFP4 GEMM 全部 ~550 TFLOPS = scaled peak ~92% | [kernels-sm120.md](kernels-sm120.md) §1 |
47	| Marlin gate_up M=1 已 82-97% L2 BW 饱和；HMMA:HFMA2=1:11 瓶颈在 CUDA core dequant | [marlin.md](marlin.md) §3 |
48	| RTX 6000D NVFP4 gate_up GEMM 物理下限：**M=1 = 47 µs（mem-bound），M=8192 = 710 µs（compute-bound）** | [methodology.md](methodology.md) §3 cost model |
49	| sgl-kernel C++ `dequant_fp8_scales<nv_bfloat162>` 缺 BF16 widening exponent rebias；vLLM PR #34577 等价 fix 在 **Python 端** | [current.md](current.md) §3 |
50	| 死代码：.so 内 52 Sm100 + 111 Sm90 kernel 在 sm_120 调用即崩 | [current.md](current.md) §2 |
51	| `SGLANG_MARLIN_DECODE_THRESHOLD=48` 是 weight-bound→transition regime 边界，不是经验值 | [methodology.md](methodology.md) §3 M regime |
52	
53	## 跨主题
54	
55	- 量化方案（怎么量化模型）→ [`../quant/`](../quant/)
56	- decode 性能 / profile 方法论 → [`../decode/`](../decode/)
57	- 部署 / cu13 升级 → [`../platform/cu13-stack.md`](../platform/cu13-stack.md)
58	
59	## 永不脱离的范围
60	
61	只做 **CUTLASS NVFP4 GEMM + Marlin W4A16 GEMM** 在 sm_120 + 容器云 + ncu 锁环境的底层调优。spec decoding / DFlash / sparse attention / quant 方案 / 训练等不属于本目录。
62
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/gemm/todo.md"
}
```

> TOOL

tool_result Read
```
1	# GEMM 调优 TODO（顶层视角，ROI 排序）
2	
3	事实来源：2026-05-10 三个调研 subagent 报告（CUTLASS sm_120 全景 / sgl-kernel C++ 端 / flashinfer mm_fp4 backend）+ 现有 docs。
4	
5	> **顶层视角**：CUTLASS / Marlin 调优维度远不止 autotune。本表按 ROI 从高到低排序，每条标注 effort 和 risk。**不局限于局部小最优**——优先攻能改变 SOL gap 形态的维度（schedule、epilogue fusion、tile shape），而非已枯竭的 dispatch tuning。
6	
7	## 0. 已确认死胡同 / 放弃方向（不再追）
8	
9	| 方向 | 原因 | 引用 |
10	|---|---|---|
11	| ~~b12x backend (target-only enable)~~ | **2026-05-10 R-b12x 已平反**：bit-exact 实证 + e2e Decode +28.5% lock-in (commit 679017f) | dead-ends.md §M（已平反）/ changelog R-b12x |
12	| R-b12x-tune (std upper 32→28) | bs=32 +7.9% 但 bs=16 -11.4% 可复现 | changelog R-b12x-tune |
13	| R-b12x-tune-v2 (FORCE_B12X exact-M) | 同 -11.4% 退化，机制无关，是 std b12x bucket=48+128 共存非线性 cost | changelog R-b12x-tune-v2 |
14	| Marlin tile/stage sweep | HMMA:HFMA2 = 1:11，张量核空转，bottleneck 是 CUDA core dequant，已 Pareto。继续压 < 2% | marlin.md §3 |
15	| PingPong dense NVFP4 sm_120 | 物理不存在（CUTLASS 4.4.2 source confirmed） | dead-ends.md §B |
16	| Cluster shape > 1×1×1 | sm_120 max cluster size = 1（consumer SKU 砍掉 cluster 网络） | dead-ends.md §A |
17	| native FP4 MMA W4A16 | PTX 要求 A+B 都 FP4 | marlin.md §3 |
18	| swap-AB + mixed TMA recipe | dense 路径 N≥4096，N << M 不成立，无收益 | sgl-project #19637 |
19	| cuDNN sm_120 NVFP4 backend | flashinfer 0.6.8 已支持，本地实测 = CUTLASS 持平（sgl-project #19637 cuDNN 优势在 SM100，不是 sm_120） | current.md §3 |
20	| CUTLASS 4.2.0 → 4.4.2 整体升级 | kernel 代码 ≡ 4.2.0（仅 alignas(16) 一行实质 diff） | current.md §4 |
21	| autotune cache metadata strip 加载 | cache 单 bucket 不为 spec workload 设计（R6 实测 0 收益） | dead-ends.md K |
22	| R5a per-shape Marlin override | fp8 KV / no-cuda-graph artifact，正确 config 下 -1.9% 至 -19% | dead-ends.md J |
23	| **R10 alignas(16) cherry-pick to sgl-kernel CUTLASS** | **生产 NVFP4 dense GEMM 走 flashinfer 不走 sgl-kernel**；flashinfer 0.6.8 bundled CUTLASS 已是 4.4.2 含 alignas(16)（dead-ends.md N） | 见下文 §1 修订 |
24	| **R9 marlin scale rescale + clamp** | **已 lock-in (commit 1183bae)**：Python only，性能 ±0.4% 噪声层，与 vLLM PR #34577 对齐做防御性 fallback | changelog R9 |
25	| **R-b12x-bucket64** (b12x `_M_BUCKETS` 加 64) | **2026-05-10 REJECTED**：quick_validate bs=8 +1.98%，但 full eval ori_acc -1.06pp + duration +8.7%。production EAGLE-3 chain verify accept_rate ≈0.34 让 M 在 bucket 边界横跳 → kernel cache thrashing。任何 `_M_BUCKETS` 改动必须 full eval gate（dead-ends.md §O / methodology.md §3.5） | changelog R-b12x-bucket64 |
26	
27	---
28	
29	## 1. ROI Tier 1（最高，**改变 SOL gap 形态**）—— 2026-05-10 修订：所有 CUTLASS 侧 patch 重新定位到 flashinfer
30	
31	> **新发现（dead-ends.md §N）**：sgl-kernel 路径不在生产 NVFP4 hot path，所有想动 CUTLASS 模板的 patch 都要去改 `/opt/.../flashinfer/data/cutlass/` 而不是 sgl-kernel/CMakeLists. flashinfer 已 bundled CUTLASS 4.4.2，比 sgl-kernel 4.2.0 新。
32	
33	### 1.0 ~~b12x 精度复查~~ ✅ 已 lock-in (2026-05-10, commit 679017f)
34	
35	**实测结果**：
36	- Stage A bit-exact：4 shapes × 9 M = 36 组合，max_diff=0/cos_sim=1.0/argmax=100%（推翻 dead-ends.md §M 旧"精度损失"结论）
37	- Stage B e2e A/B/A：Decode single **+28.5%**，bs=8/12/16/24 +7-12%，prefill 中性，bs=4 -6.5%（边界 M=28）
38	- Lock-in：modelopt_quant.py + start_eagle.sh，默认 SGLANG_ENABLE_B12X=1
39	- 详见 changelog Round R-b12x
40	
41	后续追求（不再 Tier 1）：
42	- R-b12x-tune / R-b12x-tune-v2：尝试 std M=32 → b12x，发现 bs=16 共存退化，dead-end
43	- R-b12x-tune-v3 (未做)：用 nsys profile 抓 std b12x bucket=48 + bucket=128 共存的 SMEM/L2 contention 根因，决定是否能解锁 bs=32 +8%
44	
45	### 1.1 EVT Epilogue Fusion: `gate_up GEMM + SiLU + element-wise mul`
46	
47	- **维度**：CUTLASS Epilogue Visitor Tree（EVT）—— 把 SwiGLU 的 `silu(gate) * up` 写进 GEMM epilogue
48	- **当前位置**：要改 **flashinfer's mm_fp4 source** (flashinfer JIT csrc) 加自定义 epilogue 实例化；不是 sgl-kernel `nvfp4_scaled_mm_kernels.cu`（那条路径没人调用）
49	- **预期 ROI**：prefill +1-3%，decode +0.5-1%（fal.ai 1.28×, vLLM #22448 SiLU+quant 1.10-2.25×，EVT 形式更优）
50	- **Effort**：重新评估 ≈ 2 周（要先把 flashinfer JIT 编译/缓存协议跑通，然后改 csrc + 重编 + 验证）
51	- **Risk**：中-高（动 site-packages 的 flashinfer，需要可回滚备份；EVT visitor tree 写错破坏 numerics）
52	- **依赖**：用户已授权 .so rebuild + 备份协议（但 flashinfer 是 venv site-packages，备份协议需扩展）
53	- **任务**：R13（推后，先把 flashinfer 改造协议跑通）
54	
55	### 1.2 CUTLASS 4.4.2 → 4.5.0 升级 + 新 tile shape (128×32×K, 128×64×K) 接入
56	
57	- **维度**：升级 flashinfer bundled CUTLASS（不是 sgl-kernel）；nvfp4 模板加新 sub-128 列方向 atom
58	- **当前位置**：flashinfer 0.6.8.post1 bundled CUTLASS 4.4.2；要 fork flashinfer 升 4.5.0 + 重编 JIT cubin
59	- **预期 ROI**：M ∈ [1, 32] 路径 1.1-1.3×（待 sm_120 实测）；prefill 0%
60	- **Effort**：≈ 1 周（fork flashinfer + 升 CUTLASS + 改 dispatch + 测）
61	- **Risk**：高（动 flashinfer bundled CUTLASS，跨多个 minor 可能引入其他改动）
62	- **任务**：R14（推后）
63	
64	---
65	
66	## 2. ROI Tier 2（中等）—— 2026-05-10 修订
67	
68	> **R10/R11 已废弃**（dead-ends.md §N）：alignas(16) 已在 flashinfer-bundled CUTLASS 4.4.2，且 sgl-kernel 不在 hot path。SF SmemCopyAtom uint32 也要先 verify flashinfer 的 atom 状态。这两条不再追。
69	
70	### 2.1 ~~alignas(16) cherry-pick~~ 已死路（dead-ends.md §N）
71	
72	### 2.2 ~~SF SmemCopyAtom uint32_t vec load (sgl-kernel)~~ 已死路（dead-ends.md §N）
73	
74	### 2.2bis flashinfer SF SmemCopyAtom uint32 vec load（如还没上）— 待 verify
75	
76	- **维度**：去 `/opt/.../flashinfer/data/cutlass/include/cutlass/gemm/collective/sm120_blockscaled_mma_tma.hpp` 检查 SmemCopyAtomSFA/B 实例化是否已是 uint32 vec
77	- **任务**：R11bis（先做 verify，不一定有改动空间）
78	
79	### 2.3 显式 KernelSchedule / EpilogueSchedule + StageCount
80	
81	- **维度**：把 `KernelScheduleAuto` / `EpilogueScheduleAuto` / `StageCountAutoCarveout` 改为显式选择最优 schedule + 显式 stage count
82	- **当前状态**：sgl-kernel sm_120 path 全 auto；subagent 2 报告"缺乏显式 schedule 调优"
83	- **预期 ROI**：1-3%
84	- **Effort**：C++ + .so rebuild ≈ 2 天（试不同 schedule + bench 选最优）
85	- **Risk**：低（不改 kernel，只改 dispatch）
86	- **任务**：R14（晚于 R10/R11，schedule 试错需要多次 rebuild）
87	
88	### 2.4 dequant_fp8_scales PTX intrinsic 替代
89	
90	- **维度**：dequant.h:442 当前 LOP3+SHF+PRMT 6 条 ALU 序列，改 `cvt.rn.bf16x2.e4m3x2` PTX 单指令
91	- **当前状态**：当前序列做了简单 right-shift 4，没做 exponent rebias（疑似与 vLLM PR #34577 BF16 widening underflow 同款 bug 形态）
92	- **预期 ROI**：dequant 路径 < 5%（HMMA:HFMA2=1:11，dequant 是 HFMA2 主体）；可能修潜在 underflow bug
93	- **Effort**：C++ + .so rebuild + microbench cvt.rn issue rate 验证 ≈ 2 天
94	- **Risk**：中（PTX intrinsic 替换需验证数值精度等价；microbench 先看 issue rate）
95	- **任务**：R15（依赖先做 task #8 microbench）
96	
97	### 2.5 marlin_utils_fp4.py scale rescale + clamp（数值稳定性 patch）
98	
99	- **维度**：Python 端在 weight_scale 处理时加 rescale + clamp，避免下游 dequant_fp8_scales BF16 widening underflow（参考 vLLM PR #34577）
100	- **当前状态**：marlin_utils_fp4.py:75 `nvfp4_marlin_process_global_scale` 没加 clamp；marlin_template.h.rej 已 reject 上游标准 stride patch
101	- **预期 ROI**：稳定性优先（性能 ≤ 1%）；防 small global_scale 路径下 BF16 underflow 退化
102	- **Effort**：Python only ≈ 0.5 天
103	- **Risk**：低（独立 numerics fix）
104	- **任务**：R16（晚做，性能 lever 优先）
105	
106	---
107	
108	## 2.6 Backline 候选 — 来自 SGLang Marlin 调优 blog (2026-05-10 加)
109	
110	> 来源：用户分享的 SGLang Marlin 调优 blog（per-(M, N) tile + atomic_add 优化）。Marlin 是 sgl-kernel 的核心 W4A16 GPTQ GEMM，**在我们 production decode 小 M 路径上 (M ≤ 48) 仍是 hot kernel**。这两条与 R15 一起放在 .so rebuild 流水线上。
111	
112	### 2.6.1 Per-(M, N) tile 多档位选择 + 优先级候选表
113	
114	- **维度**：重写 Marlin 的 `determine_exec_config` —— 当前只区分大/小 batch，改为按 M 多档位 × N 维度差异化分支
115	  - decode (M 小，K 长)：在 K 方向更多 tile 展开 → 提高带宽利用率
116	  - prefill (M 大)：N 方向并行展开
117	  - 每档位维护优先级排序的候选 tile 配置表，每个候选验证 SMEM 不超限 + K/N 整除
118	- **当前位置**：`/opt/SGLang-MiniCPM-SALA/packages/sglang-minicpm/sgl-kernel/csrc/gemm/marlin/gptq_marlin.cu` 的 `determine_exec_config`
119	- **预期 ROI**：Marlin path（小 M decode）3-8%（blog 实测多形状最优 tile 不同；我们已有 6 形状 × 多档 M 的 SOL 数据可参考 sol_table.md）
120	- **Effort**：C++ + .so rebuild ≈ 2-3 天（重写 dispatch + 全 sweep 找各档位最优 + bench）
121	- **Risk**：中（dispatch 表错会导致小 M 退化，需 per-shape A/B）
122	- **依赖**：解决 sgl-kernel build infra（`/user_4813494d/deps` re-fetch + 验证 CMake FetchContent）
123	- **任务**：R-blog-tile
124	
125	### 2.6.2 Decode 路径 atomic_add 无条件用于小 M
126	
127	- **维度**：Marlin 原始判定 `ceil(M/64) × N ≤ 16384` 才用 atomic_add，否则 barrier sync。但小 M 时 barrier 串行等待开销反而是瓶颈。改为小 M 无条件 atomic_add 路径。
128	- **当前位置**：sgl-kernel marlin gptq_marlin.cu 归约判定逻辑
129	- **预期 ROI**：小 M decode 1-3%
130	- **Effort**：C++ + .so rebuild ≈ 1 天（找小 M 阈值 + 改判定 + bench）
131	- **Risk**：低（局部判定改动；要确认 atomic_add 无条件用在大 M 不会退化）
132	- **依赖**：同 2.6.1 (build infra)
133	- **任务**：R-blog-atomicadd
134	
135	---
136	
137	## 3. ROI Tier 3（低 / 已实测 / 监控）
138	
139	### 3.1 Engineering：删除 .so 内 163 个 sm_120 不调用的 dead kernel
140	
141	- **维度**：CMakeLists.txt 关掉 sm_90 (WGMMA, 111 kernels) 和 sm_100 (tcgen05/UMMA, 52 kernels) 实例化
142	- **当前状态**：current.md §2.4，占 .so 体积但 sm_120 调用即崩
143	- **预期 ROI**：性能 0；提交包大小可能 -20-30%（current.md §2.4 估算）
144	- **Effort**：C++ + .so rebuild ≈ 1 天
145	- **Risk**：低（关闭未用代码）
146	- **优先级**：低（提交包当前 < 2GB，不紧迫）
147	
148	### 3.2 cuDNN ≥ 9.22 sm_120-native NVFP4 backend 监控
149	
150	- 等 cuDNN 升级到 9.22+ 后是否新增 sm_120 native NVFP4 GEMM tune；当前 9.21 实测持平 CUTLASS
151	
152	### 3.3 flashinfer split-K candidate 增加
153	
154	- 当前 flashinfer 完全无 split-K，仅 DataParallel + StreamK；大 K 小 M 无候选
155	- 工程量大，ROI 不明，留作未来
156	
157	---
158	
159	## 4. 执行顺序 —— 2026-05-10 修订
160	
161	| 顺序 | 任务 | 类型 | 状态 |
162	|---|---|---|---|
163	| **R7** | flashinfer autotune sweep 扩展 | Python only | ✅ Lock-in (commit a0e216a, +2-3% e2e) |
164	| **R9** | marlin_utils_fp4 scale rescale + clamp | Python only | ✅ Lock-in (commit 1183bae, 稳定性 patch) |
165	| **R10/R11** | sgl-kernel CUTLASS cherry-picks | -- | ❌ dead-ends.md §N（hot path & version 双错位） |
166	| **R-b12x** | b12x 精度复查 + 实测收益 reconfirm | Python (dispatch) | ✅ Lock-in (commit 679017f, Decode +28.5%) |
167	| R-b12x-tune | std upper 32→28 | Python | ❌ bs=16 -11% revert |
168	| R-b12x-tune-v2 | FORCE_B12X exact-M | Python | ❌ bs=16 -11% revert，根因 bucket 共存 |
169	| **R12** | 显式 KernelSchedule (flashinfer csrc) | flashinfer JIT 改造 | 待评估，先跑通 flashinfer 改造协议 |
170	| **R13** | EVT Epilogue Fusion (flashinfer csrc) | flashinfer JIT 改造 | 待评估 |
171	| **R14** | flashinfer CUTLASS 4.4.2 → 4.5.0 升级 | flashinfer fork | 高风险高 effort |
172	| **R15** | dequant_fp8_scales PTX intrinsic | sgl-kernel .so rebuild | 双修：speed + numerics 正确，受限 build infra |
173	| **R-blog-tile** | Per-(M,N) tile 多档位选择 (2.6.1) | sgl-kernel .so rebuild | 3-8% Marlin small-M, 同 R15 build round |
174	| **R-blog-atomicadd** | Decode atomic_add unconditional 小 M (2.6.2) | sgl-kernel .so rebuild | 1-3% Marlin small-M, 同 R15 build round |
175	| **probe** | flashinfer mm_fp4 backend switching | Python only | ❌ dead-end (R10-probe completed) |
176	
177	每轮按 SOP §3.5/3.6/3.7 走：smoke test → quick_validate A/B/A → 收益 ≥ 1% + SNR ≥ 3× → lock-in；不通过 → revert + dead-ends 沉淀。
178	
179	`.so` 替换严格按 CLAUDE.md：备份目录 `outputs/so_backups/<TS>__<src>__<sha12>/` + meta.json + docs/gemm/so-replacements.md 加日志行。
180	
181	**新建协议待补**：flashinfer site-packages 修改 + JIT cache invalidation + 回滚（区别于 common_ops.abi3.so 替换协议）。
182	
183	---
184	
185	## 5. 当前 lock-in（参考 baseline）
186	
187	- **R7**（commit a0e216a）：SGLang flashinfer autotune 扩展到 FP4 dense + sweep spec batch sizes
188	  - bs=8 (M=56) +6.97%，bs=12 +1.33%，bs=16 +1.23%（hot zone）
189	  - bs=24 -0.75%（trade-off）
190	  - 净 traffic-weighted +2-3% e2e
191	  - server 启动 +4s autotune sweep cost
192
```

> TOOL

tool_use Write
```json
{
  "file_path": "/user_4813494d/openbmb/docs/gemm/todo.md",
  "content": "# GEMM 调优 TODO（顶层 ROI 排序）\n\n> 当前已 lock-in 见 §0；候选改动按 ROI Tier 排序见 §1-§3；死路见 [dead-ends.md](dead-ends.md) +\n> [changelog.md](changelog.md)。每条候选必须先在 changelog 走 quick_validate A/B/A，过\n> SNR ≥ 3× + 收益 ≥ 1% 才能 lock-in。\n\n## 0. 当前 lock-in（参考 baseline）\n\n| Round | 内容 | 收益 | commit |\n|---|---|---|---|\n| R7 | flashinfer autotune sweep 扩 spec batch sizes | bs=8 +6.97% / bs=12 +1.33%；净 traffic-weighted +2-3% e2e | `a0e216a` |\n| R9 | `marlin_utils_fp4.py` scale rescale + clamp | 稳定性（防 BF16 widening underflow），性能噪声层 | `1183bae` |\n| R-b12x | b12x target dispatch 重启 + AOT cache lock-in | Stage A bit-exact（max_diff=0）；Stage B Decode S8 +28.5% / bs=8-24 +6-12%。提交包默认 `SGLANG_ENABLE_B12X=0`（启用后生效） | `679017f` + `ed8786d` |\n\n`.so` 替换严格按 CLAUDE.md：备份目录 `outputs/so_backups/<TS>__<src>__<sha12>/` +\nmeta.json + [so-replacements.md](so-replacements.md) 加日志行。\n\n## 1. ROI Tier 1（改变 SOL gap 形态）\n\n所有 CUTLASS 侧 patch 目标 = **flashinfer bundled CUTLASS**（4.4.2），不是 sgl-kernel\n（4.2.0）；生产 NVFP4 dense GEMM hot path 在 flashinfer，见\n[dead-ends.md](dead-ends.md) §N。\n\n### 1.1 EVT Epilogue Fusion：`gate_up GEMM + SiLU + element-wise mul`\n\n- **位置**：`/opt/.../flashinfer/data/cutlass/...` 加自定义 epilogue 实例化（不是\n  sgl-kernel `nvfp4_scaled_mm_kernels.cu`，那条路径无人调用）\n- **ROI**：prefill +1-3%，decode +0.5-1%（fal.ai 1.28×、vLLM #22448 SiLU+quant 1.10-2.25×）\n- **Effort / Risk**：~2 周；中-高（动 site-packages，需可回滚备份；EVT visitor tree 写错坏 numerics）\n- **前置**：flashinfer 改造协议（JIT 编译/缓存/回滚）跑通\n\n### 1.2 CUTLASS 4.4.2 → 4.5.0 升级 + 新 tile shape\n\n- 升 flashinfer bundled CUTLASS；nvfp4 模板加 sub-128 列方向 atom（128×32×K、128×64×K）\n- **ROI**：M ∈ [1, 32] 路径 1.1-1.3×（待 sm_120 实测）；prefill 0%\n- **Effort / Risk**：~1 周；高（跨多个 minor，可能引入其他改动）\n\n## 2. ROI Tier 2（局部 numerics / dispatch）\n\n### 2.1 显式 KernelSchedule / EpilogueSchedule + StageCount\n\n- 当前 sgl-kernel sm_120 path 全 auto；改显式调度 + 显式 stage count\n- **ROI** 1-3%；Effort C++ + `.so` rebuild ≈ 2 天\n\n### 2.2 `dequant_fp8_scales` PTX intrinsic\n\n- `dequant.h:442` 当前 LOP3+SHF+PRMT 6 条 ALU；改 `cvt.rn.bf16x2.e4m3x2` 单指令\n- 同时修疑似与 vLLM PR #34577 同款的 BF16 widening underflow\n- **ROI**：dequant 路径 < 5%；Effort C++ + microbench ≈ 2 天\n\n### 2.3 Marlin per-(M,N) tile 多档位（参考 SGLang Marlin 调优 blog）\n\n- 重写 `determine_exec_config` —— 按 M 多档 × N 维度差异化分支；decode (M 小, K 长) 与\n  prefill (M 大) 不同 tile 方向；维护优先级候选表\n- 位置：`sgl-kernel/csrc/gemm/marlin/gptq_marlin.cu`\n- **ROI**：Marlin small-M decode 3-8%（依赖 [sol_table.md](sol_table.md) 6 形状 × 多档 M 数据找最优）\n- **Effort / Risk**：~2-3 天；中（dispatch 错坏小 M 退化，需 per-shape A/B）\n\n### 2.4 Marlin 小 M 无条件 atomic_add\n\n- 当前 `ceil(M/64) × N ≤ 16384` 才用 atomic_add，否则 barrier；小 M 时 barrier 串行等待是瓶颈\n- **ROI**：小 M decode 1-3%；Effort ~1 天，与 2.3 同 build round\n\n## 3. ROI Tier 3（监控 / 工程清理）\n\n| 项 | 内容 |\n|---|---|\n| 删除 .so 内 163 个 dead kernel | sm_90 WGMMA 111 + sm_100 tcgen05/UMMA 52；性能 0，提交包 -20-30%（见 [current.md](current.md) §2.4） |\n| cuDNN ≥ 9.22 sm_120-native NVFP4 监控 | 当前 9.21 实测持平 CUTLASS |\n| flashinfer split-K 候选增加 | 大 K 小 M 当前无候选；工程量大，ROI 不明 |\n\n## 4. 执行顺序\n\n| 优先级 | 任务 | 类型 | 状态 |\n|---|---|---|---|\n| 1 | 1.1 EVT Epilogue Fusion | flashinfer JIT 改造 | 待评估（先把 flashinfer 改造协议跑通） |\n| 2 | 2.3/2.4 Marlin tile + atomic_add | sgl-kernel `.so` rebuild | 同 build round，先做 |\n| 3 | 2.2 `dequant_fp8_scales` PTX | sgl-kernel `.so` rebuild | 与 2.3/2.4 同 build round |\n| 4 | 2.1 显式 schedule | sgl-kernel `.so` rebuild | 多次 rebuild，晚做 |\n| 5 | 1.2 CUTLASS 4.5.0 升级 | flashinfer fork | 高风险，待 1.1 协议跑通 |\n| 6 | 3.1-3.3 监控 / 工程 | — | 等触发 |\n\n**新建协议待补**：flashinfer site-packages 修改 + JIT cache invalidation + 回滚\n（区别于 `common_ops.abi3.so` 替换协议）。\n"
}
```

> TOOL

tool_result Write
```
The file /user_4813494d/openbmb/docs/gemm/todo.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

现在处理 changelog.md（73KB），把早期 R1-R7 归档：

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"^## Round\\|^### R\" docs/gemm/changelog.md | head -40",
  "description": "changelog structure"
}
```

> TOOL

tool_result Bash
```
7:## Round 1 (2026-05-09 23:50) — Stage 4 瓶颈识别 + dispatch 阈值实测
9:### R1.1 [测量验证] H5 — Marlin tile padding 阶梯（M=48→49 跳台阶）
21:### R1.2 [测量验证] Marlin / CUTLASS dispatch 阈值实测
34:### R1.3 [SASS 静态分析] Marlin spill 实证
45:### R1.4 [发现死代码] cubin #50 完全是 marlin_moe_wna16
57:## Round 1 总结
75:## Round 2 (2026-05-10 00:00) — Per-shape MARLIN_DECODE_THRESHOLD 落地
77:### R2.1 [Patch] modelopt_quant.py 加 per-shape threshold dict
105:### R2.2 [验证] 静态闸门（5 阶段 SOP §1）
115:### R2.3 [待办] Stage 6 5 项验证 checklist
131:### R2.4 [实测验证] quick_validate.sh 5+5 案例 baseline vs R2
156:### R2.5 [Lock-in] 准备 commit + 进 Round 3
169:## Round 3 (2026-05-10 00:30) — Batch decode 暴露测量协议错误，partial rollback
171:### R3.1 [实测] 升级 quick_validate 加 batch decode (旧版结果误导)
185:### R3.2 [关键诊断] 测量协议有问题——升级 quick_validate
194:### R3.3 [实测纠正] 升级版 quick_validate 实测 R2 真实影响
206:### R3.4 [Partial Rollback] 阈值统一回 48
223:### R3.5 [Methodology] 教训沉淀
232:### R3.6 [Round 4 设计]
243:## Round 4 (2026-05-10 01:40) — Dispatch Profiler 抓真实 (shape, M) 直方图
245:### R4.1 [Patch] modelopt_quant.py 加 dispatch profiler
258:### R4.2 [实测] quick_validate workload 下真实 (shape, M) 直方图
299:### R4.3 [设计] R5 dispatch patch 候选
316:### R4.4 [Methodology] 沉淀
327:## Round 5a (2026-05-10 01:50) — Set-based dispatch override @ M={56, 112}
329:### R5a.1 [Patch] Marlin override set 落地
342:### R5a.2 [实测] A/B/A interleave bench (3 baseline + 3 R5a)
363:### R5a.3 [诊断] 21002t prefill 异常（B / B0 出现, B' 消失）
373:### R5a.4 [验证] 5 项检查
386:### R5a.5 [Lock-in] 准备 commit
395:### R5a.6 [Round 5b 设计]
408:## Round 5b (2026-05-10 02:30) — R5a 撤销：fp8 KV + no-cuda-graph artifact 暴露
410:### R5b.0 [背景] R5a 验证 config 错误
416:### R5b.1 [实测] R5a 在正确 config 下 A/B/A 重测 (3 数据点)
433:### R5b.2 [根因] cuda graph 反转 dispatch 优劣序
445:### R5b.3 [Patch] 撤销 R5a override
454:### R5b.4 [验证] 撤销后 A 基线复现
469:### R5b.5 [SOP 教训]
478:### R5b.6 [下一步候选]
490:## Round 6 (2026-05-10 02:48) — Autotune cache 元数据 strip 实验：0 收益
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -nE \"^## Round|^## R\" docs/gemm/changelog.md",
  "description": "all round headers"
}
```

> TOOL

tool_result Bash
```
7:## Round 1 (2026-05-09 23:50) — Stage 4 瓶颈识别 + dispatch 阈值实测
57:## Round 1 总结
75:## Round 2 (2026-05-10 00:00) — Per-shape MARLIN_DECODE_THRESHOLD 落地
169:## Round 3 (2026-05-10 00:30) — Batch decode 暴露测量协议错误，partial rollback
243:## Round 4 (2026-05-10 01:40) — Dispatch Profiler 抓真实 (shape, M) 直方图
327:## Round 5a (2026-05-10 01:50) — Set-based dispatch override @ M={56, 112}
408:## Round 5b (2026-05-10 02:30) — R5a 撤销：fp8 KV + no-cuda-graph artifact 暴露
490:## Round 6 (2026-05-10 02:48) — Autotune cache 元数据 strip 实验：0 收益
582:## Round 7 (2026-05-10 02:55) — Fresh autotune via SGLang server-internal warmup
683:## Round 8 (2026-05-10 03:05) — sweep 去掉 bs=24 试图恢复 -0.75% 退化（无效）
728:## Round 9 (2026-05-10 04:04) — marlin_utils_fp4 scale rescale + clamp（vLLM PR #34577 移植）
789:## Round 10-probe (2026-05-10 04:15) — flashinfer mm_fp4 backend switching probe
812:## Round 11-prep (2026-05-10 04:20) — R15 (dequant_fp8_scales PTX intrinsic) 可行性探查
854:## Round 12-prep (2026-05-10 04:25) — Prefill EXTEND mode autotune gap 识别
899:## Round R-b12x (2026-05-10 06:13-06:21) — 重启 b12x 生产 dispatch（Stage A 精度 + Stage B e2e）
950:## Round R-b12x-tune (2026-05-10 06:28-06:38) — 边界 M=28/32 的 marlin_upper 标定（未 lock-in）
990:## Round R-b12x-tune-v2 (2026-05-10 06:42-06:45) — exact-M FORCE_B12X 也复现 bs=16 -11%
1030:## Round R-prefill-prewarm (2026-05-10 06:54-07:01) — target prefill M=8192 autotune 触发：0% 收益
1063:## Round R-b12x-acc-fix (2026-05-10 08:30-09:15) — marlin_upper 全部抬到 48：精度+吞吐双赢 lock-in
1138:## Round R-b12x-aot-cache (2026-05-10 14:15-14:19) — 把 b12x cubin AOT cache 落到 demo-sala/assets
1201:## Round R-marlin-fp32reduce (2026-05-10 14:25-14:54) — `SGLANG_MARLIN_USE_FP32_REDUCE=0` REJECTED
1265:## Round R-b12x-bucket64 (2026-05-10 15:00-15:50) — bucket=64 dispatch 添加 REJECTED
```

> TOOL

tool_use Bash
```json
{
  "command": "mkdir -p docs/gemm/archive",
  "description": "create archive dir"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/gemm/changelog.md",
  "offset": 1,
  "limit": 10
}
```

> TOOL

tool_result Read
```
1	# Stage 5 — hypothesis-test loop changelog
2	
3	按 [methodology.md](methodology.md) §6。每轮一行：假设 / 预期 / 实测 / 解释 / artifact。
4	
5	---
6	
7	## Round 1 (2026-05-09 23:50) — Stage 4 瓶颈识别 + dispatch 阈值实测
8	
9	### R1.1 [测量验证] H5 — Marlin tile padding 阶梯（M=48→49 跳台阶）
10
```

> TOOL

tool_use Bash
```json
{
  "command": "sed -n '7,898p' docs/gemm/changelog.md > /tmp/changelog_r1_r12.txt && wc -l /tmp/changelog_r1_r12.txt",
  "description": "extract R1-R12-prep section"
}
```

> TOOL

tool_result Bash
```
892 /tmp/changelog_r1_r12.txt
```

> TOOL

tool_use Bash
```json
{
  "command": "cat > /tmp/archive_header.md <<'EOF'\n# Stage 5 changelog — R1 ~ R12-prep 归档（2026-05-09 → 2026-05-10 04:25）\n\n> 早期轮次的详细 hypothesis/expected/measured/explanation/artifact 记录。\n> 当前活跃 changelog 见 [`../changelog.md`](../changelog.md)（R-b12x 及以后）。\n> 关键决策摘要见 todo.md §0；死路 catalog 见 [`../dead-ends.md`](../dead-ends.md)。\n\nEOF\ncat /tmp/archive_header.md /tmp/changelog_r1_r12.txt > docs/gemm/archive/changelog-r1-r12prep.md\nwc -l docs/gemm/archive/changelog-r1-r12prep.md",
  "description": "write archive file"
}
```

> TOOL

tool_result Bash
```
898 docs/gemm/archive/changelog-r1-r12prep.md
```

> TOOL

tool_use Bash
```json
{
  "command": "sed -n '899,1338p' docs/gemm/changelog.md > /tmp/changelog_active.txt && wc -l /tmp/changelog_active.txt && head -5 /tmp/changelog_active.txt",
  "description": "extract active rounds"
}
```

> TOOL

tool_result Bash
```
440 /tmp/changelog_active.txt
## Round R-b12x (2026-05-10 06:13-06:21) — 重启 b12x 生产 dispatch（Stage A 精度 + Stage B e2e）

### 背景
dead-ends.md §M 标记 b12x dispatch 在 2026-04 被 revert（commit 5c8b107），原因为"实测精度损失"。今轮按 SOP 重新做 numerics + e2e A/B 复查。
```

> TOOL

tool_use Bash
```json
{
  "command": "cat > /tmp/changelog_new_head.md <<'EOF'\n# Stage 5 — hypothesis-test loop changelog\n\n按 [methodology.md](methodology.md) §6。每轮一行：假设 / 预期 / 实测 / 解释 / artifact。\n\n> R1 ~ R12-prep（早期 dispatch 阈值搜索 + per-shape override + autotune sweep + numerics\n> patch）归档到 [archive/changelog-r1-r12prep.md](archive/changelog-r1-r12prep.md)。本文件保留\n> R-b12x 及以后的活跃决策 + dead-end 记录。\n\n---\n\nEOF\ncat /tmp/changelog_new_head.md /tmp/changelog_active.txt > docs/gemm/changelog.md\nwc -l docs/gemm/changelog.md",
  "description": "replace changelog.md with new head + active rounds"
}
```

> TOOL

tool_result Bash
```
450 docs/gemm/changelog.md
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/gemm/marlin.md",
  "offset": 1,
  "limit": 60
}
```

> TOOL

tool_result Read
```
1	# Marlin / b12x 调优
2	
3	range：MiniCPM-SALA no-spec 路径下的 NVFP4 Marlin、b12x/CUTLASS 分流、CUDA graph 内 profiling。最高口径：涉及 decode 性能时以 CUDA graph replay 内 kernel 时间为准；Python `apply()` 计数只能作辅助定位。
4	
5	## 1. 当前部署状态
6	
7	| 组件 | 状态 | 说明 |
8	|---|---|---|
9	| **`common_ops.abi3.so`** | ✅ 部署 `220c18cc`（probe-sala 版本，Apr 21） | **不能用 `32d27c7`**（demo-sala 版本会导致 EAGLE draft graph capture 挂死，见 §6） |
10	| sgl-kernel FP4 scale bug fix | ✅ 已部署 | scale `/2` bug（cos_sim 0.77→1.0） |
11	| Marlin atomic / shape-aware tile | ⚠️ `220c18cc` 包含基础版，**不含 small-M atomic + shape-aware tile**（这两项在 `32d27c7` 但与 EAGLE 不兼容） | 见 §6 |
12	| 全局阈值 `SGLANG_MARLIN_DECODE_THRESHOLD=48` | ✅ 生效 | M ≤ 48 → Marlin；M > 48 → CUTLASS |
13	| b12x 2-tier dispatch | ⚠️ 开发完成 + AOT cache 已生成，**默认 `SGLANG_ENABLE_B12X=0`** | draft CUDA graph capture 不兼容 |
14	| native FP4 MMA / QuTLASS | ❌ 不可用 | sm_120 ISA 限制（见 §3） |
15	| Draft model | ✅ 永远纯 Marlin（`SGLANG_MARLIN_DECODE_THRESHOLD=9999`） | M=1-6 时 CUTLASS 比 Marlin 慢 3-8× |
16	
17	## 2. Dispatch 策略
18	
19	| Backend | 适用 M | 路径 |
20	|---|---|---|
21	| Marlin W4A16 | 1-48（threshold） | bf16 activation，CUDA core dequant + tensor core HMMA |
22	| CUTLASS NVFP4 | M > 48 | 4-bit FP4 native，cooperative scheduler sm_120f |
23	| b12x W4A4 | 集成完成未启用 | 需要 `layer.weight_scale_interleaved`（post-permute TMA-swizzled），不是 pre-permute padded_scales |
24	
25	实现：`process_weights_after_loading` CUTLASS prep 先跑，然后 `_prepare_hybrid_marlin` 从原权重创建 Marlin 格式，两种格式共存额外 VRAM ~4GB。`apply()` 按 M 分流，CUDA graph safe。
26	
27	## 3. Marlin 调优负结果（勿重踩）
28	
29	| 方向 | 结论 | 原因 |
30	|---|---|---|
31	| pipe_stages 4→6 | gate_up +5-8%，其余 0%，e2e <0.5% | down 撞 HBM roofline；qkv/o L2 驻留变 compute-bound |
32	| `use_fp32_reduce=False` | M=4-8 退化 9-17%；M=1 replay 时间几乎不变 | dispatcher 走不同 tile；decode 小 M 已走 atomic 路径基本不触发 barrier global reduce |
33	| native FP4 MMA (mma.kind=nvf4) | 不可行 | PTX 要求 A+B 都 FP4，无 W4A16 路径 |
34	| tile/warp sweep | 无意义 | HMMA:HFMA2 = 1:11，换 tile 不改 HFMA2 数量 |
35	| gn-kernels dequant 手优化 | 无货可抄 | gn-kernels 用 native MMA，没 dequant 代码 |
36	| QuTLASS MXFP4 | sm_120a 原生 Blackwell FP4 MMA，环境匹配未 build |
37	
38	### SASS 分析（gate_up M=1）
39	
40	```
41	HMMA (tensor core):                48 条
42	HFMA2+HADD2+HMUL2 (CUDA core FP):  532 条
43	LOP3+SHF+PRMT (FP4→BF16 dequant):  454 条
44	地址计算:                           536 条
45	```
46	
47	HMMA:HFMA2 = 1:11，张量核严重空转。瓶颈是 CUDA core dequant，不是 HBM 或 tensor core。**Marlin 在 sm_120 W4A16 M=1-8 decode 已近 Pareto 最优**。继续压 kernel ROI < 2%。
48	
49	### Marlin tile sweep（fixed S8 trace 验证）
50	
51	| shape | M | auto graph | best | speedup |
52	|---|---:|---:|---:|---:|
53	| `std_o` | 1 | 8.184 us | 6.265 us（k128_n256_t256_b1）| 1.306× |
54	| `std_qkv` | 1 | 6.375 us | 6.148 us | 1.037× |
55	| `gla_qkv` | 1 | 11.783 us | 11.402 us | 1.033× |
56	| `std_o`/`qkv` | 8 | — | — | 1.000× |
57	| `gate_up` `down` | 1 / 8 | — | — | 1.000× |
58	
59	只有 `std_o M=1` 还有 ~1.9 us/call 实空间，折到 e2e <1%。其余基本无空间。**M=1 exact-tile 已 per-shape gate**（`SGLANG_MARLIN_M1_EXACT_TILE=0` 默认关闭），B3 整体打开会回退。
60
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/gemm/marlin.md",
  "offset": 60
}
```

> TOOL

tool_result Read
```
60	
61	## 4. b12x backend（**已放弃**，2026-05-10）
62	
63	> **2026-05-10 更新**：之前文档把 b12x 不上线归因为 "EAGLE draft graph capture 不兼容" —— **这是错误表述**。真实原因是**精度损失**：target-only B12X dispatch (2026-05-04/05) 在 fixed-token EAGLE 上有速度收益（B32 -10.88%，S8 -8.45%），但**未做 against MARS 当前生产路径的离线 bit-exact 证明，且观察到 accept-rate 长尾行为变化**（[`docs/decode/history.md`](../decode/history.md) §10）。draft 永远纯 Marlin（threshold=9999），与 b12x 是否启用无关。
64	>
65	> **明确放弃 b12x**：精度退化阻塞 EAGLE-3 上线；详细沉淀见 [`dead-ends.md`](dead-ends.md) §M。本节保留作为历史记录。
66	
67	### 4.1 b12x 历史记录（仅参考，不启用）
68	
69	`demo-sala/sglang/python/sglang/srt/layers/quantization/b12x_fp4.py`：
70	
71	- `SGLANG_B12X_DISPATCH_PROFILE=baseline|tuned`：tuned 用离线 b12x/CUTLASS/Marlin crossover 调整 per-shape 阈值
72	- `SGLANG_B12X_PRECOMPILE=1` + `SGLANG_B12X_PRECOMPILE_PROFILE=nospec-mini` + `CUTE_DSL_CACHE_DIR=demo-sala/assets/b12x_aot_cache`：CuTe DSL 强制 `no_cache=True`，自建 TVM-FFI AOT object 层（28 个 decode bucket，~1.4MB）
73	- 关键 gotcha：必须喂 `layer.weight_scale_interleaved`（post-permute TMA-swizzled）
74	
75	### 4.2 b12x B32 no-spec 历史收益（2026-05-04，**仅参考**）
76	
77	固定 `b32_drain_decode`（32 req × 384 token）：
78	
79	| case | env | duration | tok/s | 结论 |
80	|---|---|---:|---:|---|
81	| Marlin48 baseline | `B12X=0`, `MARLIN_DECODE_THRESHOLD=48` | 4.7381s | 2593.4 | 当时 no-spec 基线 |
82	| **b12x AOT** | `B12X=1`, `B12X_MAX_M=512` | **4.1987s** | **2926.6** | -11.4% duration（**no-spec only**） |
83	
84	**这个数字不能挪到 EAGLE 生产路径作论据**：EAGLE-3 上 target-only B12X 实测有 accept-rate 长尾退化（精度问题）。`SGLANG_ENABLE_B12X=0` 永久默认。
85	
86	## 5. 已落地的 decode kernel-side 优化
87	
88	按合入顺序：
89	
90	### 5.1 SimpleGLA direct-state decode（commit `e922b76`）
91	
92	`demo-sala/sglang/python/sglang/srt/layers/attention/simple_gla_decode_kernel.py` 新增 `simple_gla_decode_update_fwd()`：直接从 `temporal[state_indices]` 读 recurrent state，kernel 内写回。同时 `BK=BV=128` decode tile 避免 FLA 默认 64×64 切 4 tile 后再 `sum(0)`。接入 no-spec decode（`SGLANG_SIMPLE_GLA_DIRECT_DECODE=1` 默认开），target_verify / spec 路径不动。
93	
94	CUDA graph replay：
95	
96	| batch | 旧 generic | 新 direct | speedup | output diff | state diff |
97	|---:|---:|---:|---:|---:|---:|
98	| 1 | 14.380 us | 6.164 us | 2.33× | 5.96e-08 | 0.0 |
99	| 8 | 34.860 us | 10.28 us | 3.39× | 6.1e-05 | 0.0 |
100	
101	bs=8 output diff 是 bf16 量级（K=128 单 tile 与旧 64×64 求和的累加顺序差异），state 完全 bit-exact。覆盖 trace 中 `vectorized_gather` + `fused_recurrent_fwd_kernel` + `index_put` 三段。
102	
103	### 5.2 compress_k head-parallel rewrite
104	
105	`minicpm_sparse_kernels.py`：原 kernel grid `(batch, chunk, head)` 但 history 路径只有 `head_idx==0` 处理所有 head，存在控制流冗余。改后每个 `head_idx` program 只负责自己的 head（padded / non-padded 两路同改）。
106	
107	| case | k | old graph | new graph | speedup |
108	|---|---|---:|---:|---:|
109	| bs=1, history=512 | k1 32/16 | 8.228 us | 4.129 us | 1.99× |
110	| bs=1, history=512 | k2 128/64 | 59.420 us | 32.809 us | 1.81× |
111	| bs=8, history=512 all rows | k2 128/64 | 58.152 us | 38.405 us | 1.51× |
112	
113	new compressed chunk 不是每步都有（k1 ~每 16 token 一次，k2 ~每 64 token 一次），是"去掉尖峰成本"而非稳定节省。
114	
115	### 5.3 Skip-fill `compress_k1/k2` -inf buffer（commit `5c83e4c`）
116	
117	旧逻辑每 decode step 把整段 replay buffer 填 `-inf` 再由 `compress_k_complete_kernel_new` 写有效区间。env `SGLANG_MINICPM_FILL_COMPRESS_BUFFERS=0` 跳过这批 BF16 `FillFunctor`。
118	
119	| 配置 | BF16 FillFunctor calls | total ms | per step |
120	|---|---:|---:|---:|
121	| fill-on | 288 | 1.480 ms | 0.0925 ms/step |
122	| skip-fill | 256 | 0.258 ms | 0.0161 ms/step |
123	| 差值 | -32 | -1.222 ms | -0.0764 ms/step |
124	
125	多出的 32 次 = 16 decode steps × 2 buffers，分别是 grid `[65536,1,1]` 和 `[16384,1,1]` 大 buffer fill。skip-fill 后剩 256 次小 fill（grid `[512,1,1]`）非目标。decode graph 总时间 155.107→153.462 ms / 16 steps，净 -0.103 ms/step。
126	
127	### 5.4 Decode pooling no-zero
128	
129	`infllm_v2.max_pooling_1d_varlen()` Python wrapper 先分配 `torch.zeros` 输出再调 kernel，但 C kernel 每个有效 `(head, q, out_block)` 都会被覆写。`minicpm_sparse_utils.py` 增加 `_max_pooling_1d_varlen_no_zero()` 用 `torch.empty`，只在 `max_seqlen_q == 1` 的 decode 启用。
130	
131	| case | zeros | empty | speedup |
132	|---|---:|---:|---:|
133	| S1 decode（70136） | 12.402 us | 8.158 us | 1.520× |
134	| S8 decode（135664） | 12.369 us | 12.440 us | 0.994× |
135	| verify（16384） | 6.998 us | 8.138 us | 0.860× |
136	
137	低风险小 patch，只覆盖 no-spec/S1/S8 decode pooling。完整 stage1 graph 后净 -1.0~1.4 us/call，不能替代 k1+k2 fused stage1。
138	
139	## 6. ⚠️ Current Marlin `.so` 与 EAGLE Draft CUDA Graph 不兼容（2026-04-26 确认）
140	
141	§3 中提到收益 ~3% 的 Marlin（含 small-M atomic + shape-aware tile，md5 `32d27c7`）**会导致 EAGLE-3 draft CUDA graph capture 挂住（37% 进度卡死）**。
142	
143	| 时间点 | env `.so` | EAGLE draft graph |
144	|---|---|---|
145	| probe-sala/prepare_env.sh 部署后 | `220c18cc`（Apr 21） | 正常 |
146	| 换成 demo-sala `.so` 做 Marlin bench | `32d27c7`（Apr 25） | **挂住** |
147	| 恢复 `220c18cc` | `220c18cc` | 正常 |
148	
149	诊断：
150	- `32d27c7` 比 `220c18cc` 大 562 KB，主要差异是 small-M atomic 路径和 shape-aware tile 表
151	- 之前所有 Marlin e2e 测试都在 no-spec 下做的，从未用 EAGLE draft graph capture 验证
152	- CLAUDE.md 中 "draft CUDA graph capture 有观察到明显退化" 的根因就是这个 `.so`
153	- `probe-sala/common_ops.abi3.so`（`220c18cc`）是目前唯一被验证可在 EAGLE 起服正常的 `.so`
154	
155	**当前生产部署必须使用 `220c18cc`**。`demo-sala/common_ops.abi3.so` 已替换为 `220c18cc`。如果后续要恢复 Marlin 3%，必须逐项 bisect small-M atomic vs shape-aware tile，找到和 draft graph capture 冲突的具体改动，而不是整体替换 `.so`。
156	
157	## 7. 已枯竭方向
158	
159	| 方向 | 结论 |
160	|---|---|
161	| `--fuse-topk`（tilelang 融合 stage1+pool+topk） | overlap 0.139~0.460（应 ≥0.95），duplicate 1-3.3%；`compressed_attention_tilelang` 只传 k1，破坏官方 k1+k2 scoring 语义。已加 guard，`SGLANG_MINICPM_ALLOW_UNSAFE_FUSE_TOPK=1` 才能调试 |
162	| `split_stage1` | 只用 k1 scoring，topk overlap 0.42-0.47，语义风险高且更慢 |
163	| `topk(sorted=False)` | bf16 microbench 1.20×，但 `infllmv2_attn_stage1` 自身 topk 有 run-to-run 抖动，无法独立证明严格不改输出。生产保持 `sorted=True` |
164	| max_context padding 缩减 | `135664` 场景把 `max_context_len` 从 `524288` 降到实际长度只省 ~12.6 us/call |
165	| stage2 `disable_split_kv` / `fixed_split_size=8192` | 21 us → 230 us 严重退化 |
166	| stage2 `use_tensor_cores=0` | wrapper 不支持 `group_size=16` |
167	
168	### 7.1 stage1 k1+k2 语义（必须保持）
169	
170	`infllmv2_attn_stage1(q, k, v)` 里 `k=k1, v=k2`，**v 不是普通 attention 的 value**。CUDA kernel 分两段：第一段用 k2 跑 coarse softmax 得 row max/sum；第二段用 k1 调 `softmax_rescale_gt()` 复用 row max/sum，再通过 `hdim16_reduce()` 写 k1 score。**所以 k1-only fused topk 和 `split_stage1=True` 都是错的——官方 score 不是 `softmax(q @ k1)`，而是由 k2 coarse LSE 参与归一化后的 k1 score**。要保语义的真正融合应在 stage1 CUDA epilogue 里做（`hdim16_reduce()` 后直接做 block pooling/topk），而非外挂 k1-only TileLang kernel。
171	
172	## 8. 当前 decode 剩余热点（fixed S8 trace, B2 tuned）
173	
174	| class | calls/step | ms/step |
175	|---|---:|---:|
176	| Marlin（含 atomic + shape-aware）| 160.0 | 4.9032 |
177	| attention split/paged-kv | 24.0 | 1.7541 |
178	| SimpleGLA direct | 24.0 | 0.4748 |
179	| BF16/CUTLASS GEMM | 1.0 | 0.4588 |
180	| compress_k | 16.0 | 0.4037 |
181	| elementwise/reduce misc | 182.0 | 0.3674 |
182	| RMSNorm | 137.0 | 0.3025 |
183	| topk/sort | 24.0 | 0.2692 |
184	| sparse metadata | 48.0 | 0.1925 |
185	| index_put | 17.6 | 0.1098 |
186	
187	attention split/paged-kv 拆解：
188	
189	| kernel | calls/step | ms/step | source |
190	|---|---:|---:|---|
191	| `flash_fwd_splitkv_stage1_kernel` | 8 | 1.4249 | sparse topk stage1 compressed scoring |
192	| `BatchPrefillWithPagedKVCacheKernel` | 8 | 0.3049 | FlashInfer stage2 sparse paged KV |
193	| `PersistentVariableLengthMergeStatesKernel` | 8 | 0.0243 | stage2 merge |
194	
195	下一轮高 ROI 不是继续 Marlin tile，而是 **k1+k2 语义保持的 stage1 fused topk**，目标合并 `infllmv2_attn_stage1 + max_pooling_1d_varlen + topk/sort`。
196
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/gemm/marlin.md",
  "old_string": "| **`common_ops.abi3.so`** | ✅ 部署 `220c18cc`（probe-sala 版本，Apr 21） | **不能用 `32d27c7`**（demo-sala 版本会导致 EAGLE draft graph capture 挂死，见 §6） |\n| sgl-kernel FP4 scale bug fix | ✅ 已部署 | scale `/2` bug（cos_sim 0.77→1.0） |\n| Marlin atomic / shape-aware tile | ⚠️ `220c18cc` 包含基础版，**不含 small-M atomic + shape-aware tile**（这两项在 `32d27c7` 但与 EAGLE 不兼容） | 见 §6 |\n| 全局阈值 `SGLANG_MARLIN_DECODE_THRESHOLD=48` | ✅ 生效 | M ≤ 48 → Marlin；M > 48 → CUTLASS |\n| b12x 2-tier dispatch | ⚠️ 开发完成 + AOT cache 已生成，**默认 `SGLANG_ENABLE_B12X=0`** | draft CUDA graph capture 不兼容 |\n| native FP4 MMA / QuTLASS | ❌ 不可用 | sm_120 ISA 限制（见 §3） |\n| Draft model | ✅ 永远纯 Marlin（`SGLANG_MARLIN_DECODE_THRESHOLD=9999`） | M=1-6 时 CUTLASS 比 Marlin 慢 3-8× |",
  "new_string": "| **`common_ops.abi3.so`** | ✅ 部署 `220c18cc`（Apr 21） | **不能用 `32d27c7`**（含 small-M atomic + shape-aware tile，会导致 EAGLE draft graph capture 挂死，见 §6） |\n| sgl-kernel FP4 scale bug fix | ✅ 已部署 | scale `/2` bug（cos_sim 0.77→1.0） |\n| Marlin atomic / shape-aware tile | ⚠️ `220c18cc` 不含这两项；恢复需逐项 bisect | 见 §6 |\n| 全局阈值 `SGLANG_MARLIN_DECODE_THRESHOLD=48` | ✅ 生效 | M ≤ 48 → Marlin；M > 48 → CUTLASS |\n| b12x 2-tier dispatch | ⚠️ **kernel 修通 + AOT cache lock-in（2026-05-10 R-b12x）**，但默认 `SGLANG_ENABLE_B12X=0` | bit-exact + S8 +28.5% 实测；默认 OFF 的理由见 §4 + [decode/current.md](../decode/current.md) §4.1 |\n| native FP4 MMA / QuTLASS | ❌ 不可用 | sm_120 ISA 限制（见 §3） |\n| Draft model | ✅ 永远纯 Marlin（`SGLANG_MARLIN_DECODE_THRESHOLD=9999`） | M=1-6 时 CUTLASS 比 Marlin 慢 3-8× |"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/gemm/marlin.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/gemm/marlin.md",
  "old_string": "## 4. b12x backend（**已放弃**，2026-05-10）\n\n> **2026-05-10 更新**：之前文档把 b12x 不上线归因为 \"EAGLE draft graph capture 不兼容\" —— **这是错误表述**。真实原因是**精度损失**：target-only B12X dispatch (2026-05-04/05) 在 fixed-token EAGLE 上有速度收益（B32 -10.88%，S8 -8.45%），但**未做 against MARS 当前生产路径的离线 bit-exact 证明，且观察到 accept-rate 长尾行为变化**（[`docs/decode/history.md`](../decode/history.md) §10）。draft 永远纯 Marlin（threshold=9999），与 b12x 是否启用无关。\n>\n> **明确放弃 b12x**：精度退化阻塞 EAGLE-3 上线；详细沉淀见 [`dead-ends.md`](dead-ends.md) §M。本节保留作为历史记录。\n\n### 4.1 b12x 历史记录（仅参考，不启用）\n\n`demo-sala/sglang/python/sglang/srt/layers/quantization/b12x_fp4.py`：\n\n- `SGLANG_B12X_DISPATCH_PROFILE=baseline|tuned`：tuned 用离线 b12x/CUTLASS/Marlin crossover 调整 per-shape 阈值\n- `SGLANG_B12X_PRECOMPILE=1` + `SGLANG_B12X_PRECOMPILE_PROFILE=nospec-mini` + `CUTE_DSL_CACHE_DIR=demo-sala/assets/b12x_aot_cache`：CuTe DSL 强制 `no_cache=True`，自建 TVM-FFI AOT object 层（28 个 decode bucket，~1.4MB）\n- 关键 gotcha：必须喂 `layer.weight_scale_interleaved`（post-permute TMA-swizzled）\n\n### 4.2 b12x B32 no-spec 历史收益（2026-05-04，**仅参考**）\n\n固定 `b32_drain_decode`（32 req × 384 token）：\n\n| case | env | duration | tok/s | 结论 |\n|---|---|---:|---:|---|\n| Marlin48 baseline | `B12X=0`, `MARLIN_DECODE_THRESHOLD=48` | 4.7381s | 2593.4 | 当时 no-spec 基线 |\n| **b12x AOT** | `B12X=1`, `B12X_MAX_M=512` | **4.1987s** | **2926.6** | -11.4% duration（**no-spec only**） |\n\n**这个数字不能挪到 EAGLE 生产路径作论据**：EAGLE-3 上 target-only B12X 实测有 accept-rate 长尾退化（精度问题）。`SGLANG_ENABLE_B12X=0` 永久默认。",
  "new_string": "## 4. b12x backend（kernel lock-in，提交包默认 OFF）\n\n**2026-05-10 R-b12x 平反**（推翻 04-05 \"精度损失\" 旧结论）：\n\n- Stage A bit-exact：4 shapes × 9 M = 36 组合 max_diff=0、cos_sim=1.0、argmax=100%\n- Stage B e2e A/B/A：Decode single +28.5%，bs=8/12/16/24 +6-12%；prefill 中性\n- Lock-in：`commit 679017f`（kernel + dispatch） + `commit ed8786d`（marlin_upper=48 + AOT cache）\n- AOT cache：`demo-sala/assets/b12x_aot_cache/`（28 个 decode bucket，~1.4MB）\n- 关键 gotcha：必须喂 `layer.weight_scale_interleaved`（post-permute TMA-swizzled）\n\n**为什么提交包默认 OFF**：EAGLE B32 公平 A/B 收益噪声层，且 R-b12x-bucket64 实验 full eval\nori_acc -1.06pp / 退化 +8.7%（详见 [changelog.md](changelog.md) 最末 round + [dead-ends.md](dead-ends.md) §O）；任何\n`_M_BUCKETS` 改动必须 full eval gate。\n\n启用方式：`SGLANG_ENABLE_B12X=1 bash eval/start_eagle.sh`。环境变量来源：\n`demo-sala/sglang/python/sglang/srt/layers/quantization/b12x_fp4.py`。"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/gemm/marlin.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/gemm/kernels-sm120.md",
  "offset": 1,
  "limit": 60
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
9	- **b12x backend（PR #3051）** 已集成但提交包默认关闭（`SGLANG_ENABLE_B12X=0`）：2-tier dispatch Marlin/b12x + CUTLASS override，AOT cache 已落到 `demo-sala/assets/b12x_aot_cache`。B32 no-spec quick bench 有明显正收益，但 EAGLE 默认路径还未重新通过充分 A/B 和精度 gate；关键 gotcha：b12x 必须喂 `layer.weight_scale_interleaved`（post-permute TMA-swizzled 格式），不是 pre-permute padded_scales（见 §7.4）。
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
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"^## \\|^### \" docs/gemm/kernels-sm120.md",
  "description": "kernels-sm120 sections"
}
```

> TOOL

tool_result Bash
```
3:## 1. 结论速览
11:## 2. MMA 指令与硬件 peak
36:## 3. 各 GEMM 库对比（M=8192 标定点）
49:## 4. sgl-kernel 当前 dispatch
60:### 4.1 flashinfer 0.6.8.post1 已带 sm_120 autotune 池（PR #2460）
76:## 5. sm_120 tile 空间硬件约束
80:### 成功（有效 autotune 维度）
83:### 失败
93:## 6. W4A4 vs W4A16：小 M 的结构性差异
115:## 7. ROI 排序的优化方向
117:### 7.1 flashinfer mm_fp4 离线 autotune（已落地 2026-04）
161:### 7.2 NVFP4 tile × schedule × stages 手动编译扫描（独立方向，未展开）
170:### 7.3 Epilogue fusion（非 kernel 内部）
176:### 7.4 b12x backend（全面实测 + 集成 + 生产 smoke test 通过 2026-04-22）
279:### 7.5 b12x 环境要求与集成步骤
308:## 8. 已终结方向（不值得做）
320:## 9. 关键脚本与数据位置
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/gemm/kernels-sm120.md",
  "offset": 170,
  "limit": 160
}
```

> TOOL

tool_result Read
```
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
297	5. **`libs-base` 与 `libs-cu13` 同 install 互相覆盖（2026-05-03 实测复现 + 修复）**：两个 dist-info 都声明 `_cuda_ops_gen.py` / `_cutlass_ir.so` 同路径但**不同内容**（base 版 .so=143MB / cu13 版 .so=150MB；base .py=94060 字节 / cu13 .py=99081 字节）。pip 后装哪个就由哪个赢。常见崩溃形态：disk 留下「cu13 的 .py + base 的 .so」mismatched 组合，b12x JIT compile 时 `cutlass._mlir.dialects.cuda.KernelOp.__init__` 报 `TypeError: incompatible function arguments. The following argument types are supported: 1. __init__(self, operation: object) -> None`（Python `_cuda_ops_gen.py` 调多参数 super().__init__，C++ 扩展接受单参数，ABI 不一致）。**修复（已落地 prepare_env.sh Stage 2A）**：在三件套联装后，再单独 `uv pip install --force-reinstall --no-deps nvidia-cutlass-dsl-libs-cu13==4.5.0.dev0` 一次，保证 cu13 .so（150MB）覆盖 disk，等评测机 prepare_env 运行时也会自动修复。
298	
299	**集成路径**：
300	
301	1. **kernel 文件**：从 `bench/b12x/` 复制到 `demo-sala/sglang/python/sglang/srt/layers/quantization/b12x/`（`dense_blockscaled_gemm_sm120.py` + `cute_dsl_utils.py` + `__init__.py`）
302	2. **glue 模块**：`demo-sala/sglang/python/sglang/srt/layers/quantization/b12x_fp4.py`——懒加载、monkey-patch flashinfer.cute_dsl.utils、编译+缓存、`b12x_gemm_fp4(x, w, x_sf, w_sf, alpha, tile, prefetch)` API
303	3. **modelopt_quant.py dispatch**：`NvFp4LinearMethod.apply()` 加第三路
304	4. **prepare_env.sh**：`CUTE_DSL_ARCH=sm_120a`（必须带 `a`）+ 3 包 cutlass-dsl 4.5.0.dev0（环境已具备，验证 BOS 清单）+ `CUTE_DSL_CACHE_DIR=${SCRIPT_DIR}/assets/b12x_aot_cache`
305	5. **warmup**：`bench/b12x/precompile_aot_cache.py --max-m 512` 生成 28 个 TVM-FFI `.o`，随 `demo-sala` 打包；server 启动时 AOT hit 直接 `load_module`，不再在线 build 这些 decode bucket。
306	6. **autotune**：不需要再跑 flashinfer autotune（同 shape 区间已被 b12x 接管）；现有 `mm_fp4_tune_sm120.json` 保留用于 M > 256 的 CUTLASS 路径
307	
308	## 8. 已终结方向（不值得做）
309	
310	| 方向 | 原因 |
311	|---|---|
312	| 手写 pure NVFP4 GEMM kernel | CUTLASS 已用足 TMA + WS + Cooperative + persistent + sm_120 原生 MMA |
313	| Cluster > 1 | sm_120 无 multicast |
314	| 大 K tile (>128) 搭大 M/N tile | smem 不够 2 stage |
315	| 小 tile (<128) | TMA atom 约束 |
316	| flashinfer `trtllm` backend | sm_120 不支持（`cute-dsl` 从 PR #3051 拉 b12x kernel 后可用，见 §7.4） |
317	| sm_120-native W4A16 重写 Marlin | Marlin decode M=1/8 已达 82-97% L2 BW（gate/up/down），无可挤空间 |
318	| Marlin bandwidth 测量作为 blocker | 已测，实证 L2 饱和，终结 |
319	
320	## 9. 关键脚本与数据位置
321	
322	| 文件 | 用途 |
323	|---|---|
324	| `bench/pure_mma_peak/pure_mma.cu` + `run.py` | pure-MMA peak 测量 |
325	| `bench/bench_fp4_all_backends.py` | 全家桶 library 对比 |
326	| `bench/probe_fp4_peak.py` | CUTLASS 跨 shape 实测收敛 |
327	| `bench/bench_cublas_vs_cutlass_nvfp4.py` | cuBLAS vs CUTLASS 对照 |
328	| `bench/autotune_fp4/autotune_kernel.cu` | tile 参数化模板 |
329	| `bench/autotune_fp4/build.sh` | 候选 config 编译 |
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/gemm/kernels-sm120.md",
  "old_string": "## 1. 结论速览\n\n- **硬件上限**：sm_120 NVFP4 block-scaled MMA 真实 peak ≈ **1467 TFLOPS**（pure-MMA probe，2 block/SM 达到，实测对齐理论值 1553 TFLOPS 的 ~95%）。\n- **生态现状**：CUTLASS / cuBLAS / cuDNN / sgl-kernel 全部实测 ~560 TFLOPS，**仅挤出 peak 的 38%**，有 **2.6× 理论空间**。\n- **决策洼地**：不是 ISA 上限，是官方全家桶 + 社区 kernel 的共同未调优状态。autotune 可 vary 的维度比预期窄（硬件约束），但 schedule / stages / epilogue fusion 仍未开发。\n- **Marlin 不是优化对象**：decode 热形状（gate/up/down M=1/8）已实测 82-97% L2 带宽饱和，sm_120-native W4A16 重写无可挤空间。\n- **b12x backend（PR #3051）** 已集成但提交包默认关闭（`SGLANG_ENABLE_B12X=0`）：2-tier dispatch Marlin/b12x + CUTLASS override，AOT cache 已落到 `demo-sala/assets/b12x_aot_cache`。B32 no-spec quick bench 有明显正收益，但 EAGLE 默认路径还未重新通过充分 A/B 和精度 gate；关键 gotcha：b12x 必须喂 `layer.weight_scale_interleaved`（post-permute TMA-swizzled 格式），不是 pre-permute padded_scales（见 §7.4）。",
  "new_string": "## 1. 结论速览\n\n- **硬件上限**：sm_120 NVFP4 block-scaled MMA 真实 peak ≈ **1467 TFLOPS**（pure-MMA probe，2 block/SM 达到，理论值 1553 TFLOPS 的 ~95%）。\n- **生态现状**：CUTLASS / cuBLAS / cuDNN / sgl-kernel 全部实测 ~560 TFLOPS（**peak 的 38%**），仍有 ~2.6× 理论空间。\n- **决策洼地**：不是 ISA 上限，是官方全家桶共同未调优。autotune 可 vary 维度受硬件约束较窄，schedule / stages / epilogue fusion 仍未开发。\n- **Marlin 不是优化对象**：decode 热形状（gate/up/down M=1/8）已实测 82-97% L2 带宽饱和。\n- **b12x backend**：2026-05-10 R-b12x lock-in（bit-exact + S8 decode +28.5%），提交包仍默认\n  `SGLANG_ENABLE_B12X=0`。详见 [marlin.md](marlin.md) §4 + [decode/current.md](../decode/current.md) §4.1，\n  本目录不再重复 b12x 详细 dispatch 表（迁出到 §7.4 简注）。"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/gemm/kernels-sm120.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/gemm/kernels-sm120.md",
  "old_string": "### 7.4 b12x backend（全面实测 + 集成 + 生产 smoke test 通过 2026-04-22）\n\n**集成状态 2026-04-22**：代码开发完成，正确性验证通过（smoke test 正确答题，26 个 b12x kernel JIT 编译成功）。**当前提交包未启用**：`SGLANG_ENABLE_B12X` 默认为 0（`prepare_env.sh` 和 `start_eagle.sh` 均设 `:-0`），回滚原因是 EAGLE draft CUDA graph capture 路径不兼容 b12x。target model 走 b12x 收益已验证，draft model 始终需走纯 Marlin。",
  "new_string": "### 7.4 b12x backend（lock-in 2026-05-10，提交包默认 OFF）\n\n**当前状态**：kernel + dispatch 已 lock-in（commit `679017f` Stage A bit-exact、Stage B\nDecode S8 +28.5%；commit `ed8786d` marlin_upper=48 + AOT cache）。提交包默认\n`SGLANG_ENABLE_B12X=0`；详见 [marlin.md](marlin.md) §4 与 [decode/current.md](../decode/current.md)\n§4.1。本节保留早期集成 / bench / 调优历史，供未来重启验证参考。\n\n**初版集成 bug 与根因定位**（值得记录以防再踩）："
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/gemm/kernels-sm120.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/gemm/kernels-sm120.md",
  "old_string": "**EAGLE draft 不兼容说明**：draft model CUDA graph capture 路径与 b12x dispatch 不兼容，draft 需保持纯 Marlin（`_detect_draft_model_quantization()` 设 threshold=9999）。若后续启用 b12x，target 路径可获 decode GEMM ~32.4% 收益，draft 路径不受影响。\n\n**初版集成 bug 与根因定位**（值得记录以防再踩）：\n\n第一版集成把 b12x 喂了 \"pre-permute `padded_scales`\"",
  "new_string": "第一版集成把 b12x 喂了 \"pre-permute `padded_scales`\""
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/gemm/kernels-sm120.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

现在重命名 bottleneck_cards：

> TOOL

tool_use Bash
```json
{
  "command": "git mv docs/gemm/bottleneck_cards docs/gemm/bottleneck_card_samples 2>&1 || mv docs/gemm/bottleneck_cards docs/gemm/bottleneck_card_samples\nls docs/gemm/bottleneck_card_samples/",
  "description": "rename bottleneck_cards to samples"
}
```

> TOOL

tool_result Bash
```
fatal: renaming 'docs/gemm/bottleneck_cards' failed: Invalid cross-device link
01_o_proj_std_M48.md
02_down_proj_M128.md
```

> TOOL

tool_use Bash
```json
{
  "command": "git rm -r --cached docs/gemm/bottleneck_cards 2>&1 | tail -3; git add docs/gemm/bottleneck_card_samples/ 2>&1 | tail -3; git status --short | head -10",
  "description": "stage rename in git"
}
```

> TOOL

tool_result Bash
```
rm [REDACTED]
rm [REDACTED]
 M CLAUDE.md
 M demo-sala/preprocess_model.py
 M docs/decode/README.md
 M docs/decode/current.md
 M docs/dflash/README.md
 M docs/dflash/history.md
 M docs/eagle/README.md
 D docs/eagle/dflash.md
R  docs/gemm/bottleneck_cards/01_o_proj_std_M48.md -> docs/gemm/bottleneck_card_samples/01_o_proj_std_M48.md
R  docs/gemm/bottleneck_cards/02_down_proj_M128.md -> docs/gemm/bottleneck_card_samples/02_down_proj_M128.md
```

> TOOL

tool_use Write
```json
{
  "file_path": "/user_4813494d/openbmb/docs/gemm/bottleneck_card_samples/TEMPLATE.md",
  "content": "# Bottleneck Card 模板\n\n按 [methodology.md](../methodology.md) §4 Stage 4 写。每 (shape, M) 一张卡，回答：当前慢在哪？\nSOL gap 怎么拆解？下一步攻什么？\n\n> 现存 sample：[01_o_proj_std_M48.md](01_o_proj_std_M48.md)、[02_down_proj_M128.md](02_down_proj_M128.md)。\n> 全集 6 形状 × 9 档 M = 54 张未补齐，仅作样例。新增按本模板写。\n\n## 文件命名\n\n`NN_<shape>_M<value>.md`，NN = 两位序号。\n\n## 节标题（建议固定，便于跨卡对比）\n\n```\n## 1. 形状 + 当前实测\n## 2. SOL 物理下限（来自 sol_table.md）\n## 3. Gap 拆解：占用 / 带宽 / 编译 / dequant\n## 4. SASS / ncu 证据（如可获取）\n## 5. 候选改动 + ROI 预估\n## 6. 决策（attack / wait / dead-end）\n```\n"
}
```

> TOOL

tool_result Write
```
File created successfully at: /user_4813494d/openbmb/docs/gemm/bottleneck_card_samples/TEMPLATE.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/gemm/README.md",
  "old_string": "| **[changelog.md](changelog.md)** | Stage 5 | 每轮一行：假设 / 预期 / 实测 / 解释 / artifact |\n| **[validation_*.md](.)** | Stage 6 | 5 项验证 checklist（跨 shape / 数值 / cuda graph / autotune / 长稳） |\n| [current.md](current.md) | 现状快照 | 当前 .so 静态分析 + dequant.h 路径 + CUTLASS 4.2.0 内嵌 |\n| [marlin.md](marlin.md) | 历史调优 | Marlin / b12x 调优记录、SASS 分析、`220c18cc` vs `32d27c7` 兼容性警告 |\n| [kernels-sm120.md](kernels-sm120.md) | 历史调优 | sm_120 NVFP4 GEMM 实测 peak 1467 TFLOPS + 各库对比 + flashinfer autotune 落地 |\n| [so-replacements.md](so-replacements.md) | 工程 | `.so` 替换日志 + 备份目录索引 |\n| [roadmap.md](roadmap.md) | 攻击优先级 | 基于 SOL gap 的攻击点排序（依赖 sol_table.md 而不是 commit 模仿） |",
  "new_string": "| **[changelog.md](changelog.md)** | Stage 5 | 活跃轮次（R-b12x 以后）；R1~R12-prep 早期轮次归档在 [archive/changelog-r1-r12prep.md](archive/changelog-r1-r12prep.md) |\n| **[validation_*.md](.)** | Stage 6 | 5 项验证 checklist（跨 shape / 数值 / cuda graph / autotune / 长稳） |\n| [current.md](current.md) | 现状快照 | 当前 .so 静态分析 + dequant.h 路径 + CUTLASS 4.2.0 内嵌 |\n| [marlin.md](marlin.md) | 历史调优 | Marlin / b12x 调优记录、SASS 分析、`220c18cc` vs `32d27c7` 兼容性警告 |\n| [kernels-sm120.md](kernels-sm120.md) | 历史调优 | sm_120 NVFP4 GEMM 实测 peak 1467 TFLOPS + 各库对比 + flashinfer autotune 落地 |\n| [so-replacements.md](so-replacements.md) | 工程 | `.so` 替换日志 + 备份目录索引 |\n| [roadmap.md](roadmap.md) | 攻击优先级 | 基于 SOL gap 的攻击点排序（依赖 sol_table.md 而不是 commit 模仿） |\n| [todo.md](todo.md) | 顶层 TODO | ROI Tier 排序 + 当前 lock-in + 执行顺序 |\n| [bottleneck_card_samples/](bottleneck_card_samples/) | Stage 4 sample | 2 张样例卡 + TEMPLATE.md；全集 54 张未补齐 |"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/gemm/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -rn \"bottleneck_cards\" docs/ 2>/dev/null",
  "description": "find old bottleneck_cards refs"
}
```

> TOOL

tool_result Bash
```
docs/gemm/sol_table.md:197:详见 [瓶颈卡片 #01](bottleneck_cards/01_o_proj_std_M48.md) + [#02](bottleneck_cards/02_down_proj_M128.md) + [changelog Round 1+2](changelog.md)。
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/gemm/sol_table.md",
  "old_string": "详见 [瓶颈卡片 #01](bottleneck_cards/01_o_proj_std_M48.md) + [#02](bottleneck_cards/02_down_proj_M128.md) + [changelog Round 1+2](changelog.md)。",
  "new_string": "详见 [瓶颈卡片 #01](bottleneck_card_samples/01_o_proj_std_M48.md) + [#02](bottleneck_card_samples/02_down_proj_M128.md) + 早期 [Round 1+2 归档](archive/changelog-r1-r12prep.md)。"
}
```

> TOOL

tool_result Edit
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/gemm/sol_table.md",
  "offset": 190
}
```

> TOOL

tool_result Read
```
190	|---|---|---:|---:|---:|---:|---:|
191	| 1 | down_proj M=128 | 76.11 | 35.13 | 46% | 40.98 | 2.42 |
192	| 2 | down_proj M=48 | 60.36 | 28.37 | 47% | 31.99 | 1.89 |
193	| 3 | o_proj_std M=48 | 40.79 | 7.30 | 18% | 33.49 | 1.51 |
194	| 4 | o_proj_std M=32 | 34.98 | 7.12 | 20% | 27.86 | 1.26 |
195	| 5 | down_proj M=32 | 48.03 | 27.90 | 58% | 20.13 | 1.19 |
196	
197	详见 [瓶颈卡片 #01](bottleneck_cards/01_o_proj_std_M48.md) + [#02](bottleneck_cards/02_down_proj_M128.md) + [changelog Round 1+2](changelog.md)。
198	
199	下一步：Stage 6 e2e 验证 R2 patch（per-shape MARLIN_DECODE_THRESHOLD）。
200
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/gemm/sol_table.md",
  "old_string": "详见 [瓶颈卡片 #01](bottleneck_cards/01_o_proj_std_M48.md) + [#02](bottleneck_cards/02_down_proj_M128.md) + [changelog Round 1+2](changelog.md)。\n\n下一步：Stage 6 e2e 验证 R2 patch（per-shape MARLIN_DECODE_THRESHOLD）。",
  "new_string": "详见 [瓶颈卡片 #01](bottleneck_card_samples/01_o_proj_std_M48.md) + [#02](bottleneck_card_samples/02_down_proj_M128.md) + 早期 [Round 1+2 归档](archive/changelog-r1-r12prep.md)。\n\n下一步：Stage 6 e2e 验证 R2 patch（per-shape MARLIN_DECODE_THRESHOLD）。"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/gemm/sol_table.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "14",
  "status": "completed"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #14 status
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "15",
  "status": "in_progress"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #15 status
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -nE \"^## |^### \" docs/eagle/papers.md | head -50",
  "description": "papers.md structure"
}
```

> TOOL

tool_result Bash
```
9:## 1. Tree Verification 创新
11:### 1.1 Traversal Verification（NeurIPS 2025, arXiv:2505.12398）
21:### 1.2 Dynamic Delayed Tree Expansion（arXiv:2602.16994, 2026.02）
29:### 1.3 GOOSE — Anisotropic Speculation Trees（arXiv:2604.02047, 2026.04）
37:### 1.4 Hierarchical Verification Tree（HVT）（arXiv:2508.03726, 2025.08）
43:### 1.5 SAGE — Entropy-Guided Adaptive Tree（arXiv:2602.00523, 2026.02）
49:### 1.6 C2T — Classifier-Based Tree Construction（arXiv:2502.13652, 2025.02）
53:### 1.7 OPT-Tree / Sequoia
59:## 2. 接受规则创新
61:### 2.1 MARS — Margin-Aware Speculative Verification（ICLR 2026, arXiv:2601.15498）
101:### 2.2 Cactus — Constrained Acceptance Speculative Sampling（arXiv:2604.04987, 2026.04）
109:### 2.3 DIVERSED — Dynamic Ensemble Verification（AISTATS 2026, arXiv:2604.07622）
117:### 2.4 SMC-SD — Sequential Monte Carlo Speculative Decoding（arXiv:2604.15672, 2026.04）
125:### 2.5 Fuzzy SD（ACL Findings 2025, arXiv:2502.20704）
129:### 2.6 Calibrated Speculative Decoding（CSD）（arXiv:2604.13634, 2026.04）
135:### 2.7 Reflective Verification（arXiv:2505.18629, 2025.05）
139:### 2.8 SelfJudge（arXiv:2510.02329, 2025.10）
143:### 2.9 KL-Divergence Judge Training-Free（arXiv:2601.04766, 2026.01）
147:### 2.10 LK Losses — Direct Acceptance Rate Optimization（arXiv:2602.23881, 2026.02）
151:### 2.11 Alignment-Augmented SD（arXiv:2505.13204, 2025.05）
155:### 2.12 Global Resolution — Optimal Multi-Draft（arXiv:2511.15898, 2025.11）
161:## 3. Block / Sequence-Level Verification
163:### 3.1 Block Verification（arXiv:2403.10444, 2024.03）— 奠基工作
167:### 3.2 Greedy Multi-Path Block Verification（arXiv:2602.16961, 2026.02）
171:### 3.3 SJD-PV — Phrase Verification（arXiv:2603.06666, 2026.03）
177:## 4. Early Exit / Multi-Stage Verify
179:### 4.1 HiSpec — Hierarchical Speculative Decoding（arXiv:2510.01336, 2025.10）
185:### 4.2 LayerSkip — Self-Speculative + Early Exit（arXiv:2404.16710, 2024.04, Meta）
189:### 4.3 PPSD — Pipeline-Parallel Self-Speculative（arXiv:2509.19368, 2025.09）
193:### 4.4 FASER — Fine-Grained Phase Management（arXiv:2604.20503, 2026.04）
197:### 4.5 Speculative Verification（SV）（arXiv:2509.24328, 2025.09）
201:### 4.6 TriSpec — Ternary Speculative Decoding（arXiv:2601.23180, 2026）
205:### 4.7 SPRINTER — Sequential Approximate Verification（arXiv:2502.04557, 2025）
209:### 4.8 SpecPV — Partial Verification（arXiv:2512.02337, 2025）
215:## 5. Batch / Parallel Verify
217:### 5.1 MineDraft — Batch Parallel SD（arXiv:2603.18016, 2026.03）
221:### 5.2 ECHO — Elastic Speculative Decoding（arXiv:2604.09603, 2026.04）
225:### 5.3 Mirror-SD — 异构并行（arXiv:2510.13161, 2025.10）
229:### 5.4 SpecFormer — 非自回归并行 draft（arXiv:2511.20340, 2025.11）
235:## 6. Verify Overhead / 量化 Verify
237:### 6.1 Quasar — 量化验证（arXiv:2603.01399, 2026.03）
241:### 6.2 MoE-Spec — Expert Budgeting（arXiv:2602.16052, 2026.02）
245:### 6.3 Nightjar — 自适应 Spec 开关（arXiv:2512.22420, 2025.12）
249:### 6.4 Hidden State 复用（arXiv:2602.21224, 2026.02）
253:### 6.5 SpeCache — Speculative KV Caching（arXiv:2503.16163, 2025）
257:### 6.6 VOCABTRIM（arXiv:2506.22694, 2025）
263:## 7. SSM / Mamba + Speculative Decoding Verify
265:### 7.1 SpecMamba（arXiv:2509.19873, 2025）
281:### 7.2 Mamba Drafters（arXiv:2506.01206, 2025, EMNLP 2025）
287:### 7.3 Gating is Weighting（arXiv:2504.04308, 2025）
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -nE \"^## |^### \" docs/eagle/papers.md | wc -l && grep -nE \"^## \" docs/eagle/papers.md | tail -30",
  "description": "papers more sections"
}
```

> TOOL

tool_result Bash
```
90
9:## 1. Tree Verification 创新
59:## 2. 接受规则创新
161:## 3. Block / Sequence-Level Verification
177:## 4. Early Exit / Multi-Stage Verify
215:## 5. Batch / Parallel Verify
235:## 6. Verify Overhead / 量化 Verify
263:## 7. SSM / Mamba + Speculative Decoding Verify
295:## 8. Hybrid Attention + Speculative Decoding Verify
374:## 9. 当前代码中的 Verify 实现（本地调查补充）
402:## 10. Draft 生成方式革新影响 Verify
422:## 11. Verify 后处理与 KV Cache 管理
442:## 12. 综合论文索引
505:## 13. 第三轮补充调查（2026-04-27）
781:## 14. 架构背景参考
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/papers.md",
  "offset": 59,
  "limit": 110
}
```

> TOOL

tool_result Read
```
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
81	MARS 实测已完成，theta=0.85 全量 64 样本生产配置已部署。详细实测数据见 [`experiments.md`](experiments.md) §方向三。
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
93	- 依赖 `gptq_marlin.cu` **Feb 21 版本**（旧稳定版，37KB）。Apr 25 版本（44KB，含 `workspace_blocks_per_sm` 动态参数）在 rebuild 后导致 EAGLE draft CUDA graph capture 在 bs=8 挂住，详见 `docs/gemm/marlin.md` §6
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
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/papers.md",
  "offset": 374,
  "limit": 110
}
```

> TOOL

tool_result Read
```
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
```

> TOOL

tool_use Bash
```json
{
  "command": "mkdir -p docs/eagle/archive && cp docs/eagle/papers.md docs/eagle/archive/papers-full.md && wc -l docs/eagle/papers.md docs/eagle/archive/papers-full.md",
  "description": "archive full papers.md before rewrite"
}
```

> TOOL

tool_result Bash
```
809 docs/eagle/papers.md
  809 docs/eagle/archive/papers-full.md
 1618 total
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/papers.md",
  "offset": 781
}
```

> TOOL

tool_result Read
```
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
  "file_path": "/user_4813494d/openbmb/docs/eagle/papers.md",
  "offset": 1,
  "limit": 12
}
```

> TOOL

tool_result Read
```
1	# Speculative Decoding Verify 机制与线性注意力 Verify 深度调查
2	
3	> 调查时间：2026-04-27（第一轮本地代码）+ 2026-04-27（第二轮 verify 机制）+ 2026-04-27（第三轮补充）
4	> 方法：16 个 subagent 并行（本地代码分析 + Tavily + arxiv MCP 深度检索），覆盖 verify 机制创新、线性注意力/SSM verify、EAGLE 架构、长上下文分析
5	> **定位：原材料库**。记录调查发现的事实和论文内容，不做结论或行动建议。工程决策和实测数据见 [`experiments.md`](experiments.md)。
6	
7	---
8	
9	## 1. Tree Verification 创新
10	
11	### 1.1 Traversal Verification（NeurIPS 2025, arXiv:2505.12398）
12
```

> TOOL

tool_use Write
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/papers.md",
  "content": "# Speculative Decoding 论文索引 + 落地实装\n\n> **本文件 = 工程落地相关的论文摘要 + 综合索引表**。完整论文摘记（60+ 篇 7 大类细节）归档到\n> [`archive/papers-full.md`](archive/papers-full.md)。\n\n调查方法：2026-04-27 三轮 subagent 并行调研（本地代码 + arxiv MCP + Tavily），覆盖 verify 机制\n创新、SSM verify、EAGLE 架构、长上下文。工程决策和实测数据见 [`experiments.md`](experiments.md)、\n[`large-batch.md`](large-batch.md)。\n\n## 1. MARS — Margin-Aware Speculative Verification（已落地）\n\n来源：ICLR 2026, arXiv:2601.15498。**当前生产 verify 规则**（global θ=1，D5 θ=0.85，D7 θ=0.5）。\n\n### 1.1 算法\n\n对每个 draft token v_t：\n\n1. Exact Match：`v_t == top-1` → 接受\n2. Adaptive Relaxation：`v_t == top-2` 且 `r_t = z_(2)/z_(1) > θ` → 接受（视为 tie）\n3. 否则拒绝\n\n论文参数扫描结论（θ ∈ [0.84, 0.96]）：\n\n- θ=0.90：τ（accept length）+27%，端到端加速 vs EAGLE-3 +20%；BLEU/ROUGE/MT-Bench 退化在统计噪声\n- θ < 0.88：开始出现可测量质量退化（BLEU -1 分）\n- 无正式散度理论保证；论文定位为 lossy variant\n\n### 1.2 工程落地（2026-04-27）\n\n| 修改文件 | 内容 |\n|---|---|\n| `sgl-kernel/csrc/speculative/eagle_utils.cu` | `VerifyTreeGreedy` kernel 8→11 参数（+`top2_token`, `top2_ratio`, `mars_theta`），先扫 exact match，fallback MARS |\n| `sgl-kernel/csrc/common_extension.cc` | PyTorch op schema 更新为 11 参数，3 新参数可选 |\n| `sgl-kernel/include/sgl_kernel_ops.h` | C++ 头同步 |\n| `sgl_kernel/speculative.py`（venv） | Python wrapper 转发 3 个新可选参数 |\n| `demo-sala/sglang/.../eagle_utils.py` | 调用侧加 `target_predict.contiguous()`（server 中该 tensor 是非连续 view） |\n| `demo-sala/sglang/.../eagle_info.py` | verify 循环检测 EOS（`FINISH_MATCHED_TOKEN`），红色 ANSI 打印 |\n\n启动 env：`EAGLE_MARS_THETA`、`EAGLE_D5_MARS_THETA`、`EAGLE_D7_MARS_THETA`（默认 -1.0 = 关闭）。\n\n已知约束：依赖 `gptq_marlin.cu` Feb 21 旧稳定版，Apr 25 版本（含 `workspace_blocks_per_sm`）在\nrebuild 后会让 EAGLE draft graph capture 在 bs=8 挂死，详见 [`../gemm/marlin.md`](../gemm/marlin.md) §6。\n\n## 2. 本地代码中的 verify 实现现状\n\n### 2.1 已有放松接受基础设施\n\n`demo-sala/sglang/` 用 `tree_speculative_sampling_target_only`（sgl_kernel CUDA），支持\n`threshold_single` 和 `threshold_acc` 两参数（默认 1.0 = lossless）。\n\n### 2.2 Phased Verify 的 GLA State 管理\n\n源：`eagle_worker.py` + `hybrid_linear_attn_backend.py`。\n\n1. Phase-1 verify：`p1_gla = intermediate_ssm[:, :bs, :3].clone()` 保存 3 个 GLA intermediate state\n2. Phase-1 结束：dt1 state 写回 `ssm_states_all` → Phase-2\n3. Phase-2 结束：`intermediate_ssm[:, :bs, :3] = p1_gla` 恢复 + 保存 Phase-2 state\n4. 恢复生产 ssm_states：`ssm_states_all[:, mamba_indices_active] = ssm_orig_backup`\n\n本质是多阶段 state snapshot+restore，对应 SpecMamba 论文 Plan I 变体。\n\n### 2.3 文献空白\n\n**没有论文专门解决\"混合 standard attention + GLA 架构的 spec decoding verify\"**：\n- 全 SSM（SpecMamba）—— target 全是 Mamba\n- 全 Transformer target（Mamba Drafters）—— SSM 只做 drafter\n- MTP self-speculation（Nemotron）—— 不涉及外部 drafter\n\nMiniCPM-SALA 的 8 attn + 24 GLA + EAGLE 外部 drafter 组合在文献中独一无二。\n\n## 3. 综合索引表\n\n完整摘要见 [`archive/papers-full.md`](archive/papers-full.md)。\n\n| 论文 | arXiv | 改动维度 | 训练 | 理论无损 |\n|---|---|---|---|---|\n| Traversal Verification | 2505.12398 | 验证方向（叶→根） | 无 | 是 |\n| Delayed Tree Expansion | 2602.16994 | 树结构（延迟分支） | neural selector | 是 |\n| GOOSE Anisotropic Tree | 2604.02047 | 树结构（各向异性） | 无 | 是 |\n| HVT | 2508.03726 | 层次化剪枝验证 | 无 | 是 |\n| SAGE Entropy Tree | 2602.00523 | entropy 深宽 | 无 | 是 |\n| C2T Classifier Tree | 2502.13652 | 树构建 classifier | 需 classifier | 是 |\n| OPT-Tree / Sequoia | 2406.17276 / 2402.12374 | 最优树（DP / 硬件感知） | 无 | 是 |\n| **MARS** | 2601.15498 | **接受规则（margin-aware）** | **无** | **近似** |\n| Cactus | 2604.04987 | 接受规则（约束优化） | 无 | 受控偏差 |\n| DIVERSED | 2604.07622 | 接受规则（ensemble） | 部分 | 近似 |\n| SMC-SD | 2604.15672 | 采样（SMC resample） | 无 | 近似 |\n| Fuzzy SD / CSD | 2502.20704 / 2604.13634 | 散度阈值 / 语义等价 | 无 | 受控 |\n| Reflective Verification | 2505.18629 | 语义+统计 | 无 | 是 |\n| SelfJudge / KL-Judge | 2510.02329 / 2601.04766 | judge 模型 | 部分 | 受控 |\n| LK Losses | 2602.23881 | 训练目标（accept rate） | 替代 KL 蒸馏 | N/A |\n| Block Verification / Multi-Path | 2403.10444 / 2602.16961 | block-level | 无 | 是 |\n| HiSpec / LayerSkip / PPSD | 2510.01336 / 2404.16710 / 2509.19368 | early exit / pipeline | 部分 | 是 |\n| FASER / SV / TriSpec / SPRINTER / SpecPV | 多 | 验证调度 / proxy | 部分 | 部分 |\n| MineDraft / ECHO / Mirror-SD | 多 | batch / 跨设备 | 无 | 是 |\n| SpecFormer | 2511.20340 | 非 AR draft | 需 draft | 是 |\n| Quasar / MoE-Spec / Nightjar | 多 | 量化 verify / 调度 | 无 | 是 |\n| SpecMamba / Mamba Drafters / Gating | 2509.19873 / 2506.01206 / 2504.04308 | SSM verify | 部分 | 是 |\n| FastEagle / DDTree / SpecForge / PayPal EAGLE3 | 多 | draft 革新 | 部分 | 部分 |\n| Sparse Verification / EAGLE-Pangu / SMART | 多 | 后处理 / 硬件 | 无 | 部分 |\n\n## 4. EAGLE 架构演进 + MiniCPM 背景\n\n| 版本 | 来源 | 核心 |\n|---|---|---|\n| EAGLE-1 | ICML 2024, 2401.15077 | Feature-level autoregression，固定 25 节点树 |\n| EAGLE-2 | EMNLP 2024, 2406.16858 | 动态 draft tree（confidence 自适应），1.4× v1 |\n| EAGLE-3 | NeurIPS 2025, 2503.01840 | Direct token prediction + 三层特征融合 + TTT，2.36× SGLang baseline |\n| MiniCPM-SALA | 2026.02 | 8 sparse + 24 GLA 混合，HyPE / HALO 蒸馏，1M+ context |\n\nSGLang / vLLM 当前仅支持 MiniCPM4/4.1 dense；sparse 推理需用 HuggingFace Transformers 或 CPM.cu。\n"
}
```

> TOOL

tool_result Write
```
The file /user_4813494d/openbmb/docs/eagle/papers.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
```json
{
  "command": "wc -l docs/eagle/papers.md docs/eagle/archive/papers-full.md",
  "description": "verify rewrite size"
}
```

> TOOL

tool_result Bash
```
111 docs/eagle/papers.md
  809 docs/eagle/archive/papers-full.md
  920 total
```

> AGENT

现在合并 d7-tune-bench：

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/d7-tune-bench-20260511.md"
}
```

> TOOL

tool_result Read
```
1	# EAGLE D7 调档实测：steps 5→6 / dtn 11→13
2	
3	**日期**：2026-05-11  
4	**改动**：`demo-sala/prepare_env.sh` 提交包默认 `EAGLE_D7_STEPS 5 → 6`、`EAGLE_D7_DTN 11 → 13`（`eval/start_eagle.sh` 本地启服早就是 6/13，本次只把提交包 default 同步上来）。  
5	**结论**：三档 bench 全部不退化，S1 / Smax 显著正向，值得 lock-in 提交。
6	
7	## 1. 背景
8	
9	D7 是 dynamic spec mode 的最高规格档（`EAGLE_DYNAMIC_MODE=1` 下 `bs ≤ 1` 走 D7，其他档位 D5 / NO_SPEC）。
10	
11	- D5 (默认 mode)：`topk=2, steps=3, dtn=7`
12	- D7（小 batch 高接受率档）：`topk=2, steps=5/6, dtn=11/13`
13	- NO_SPEC（`bs ≥ 31`）：直接 target
14	
15	旧默认 5/11 与现在 6/13 的差别：draft 多走一步、verify chain 多 2 个候选。前提是 draft acceptance rate 在 small batch decode 路径稳定 > 0.55 才有正收益。
16	
17	## 2. 实测条件
18	
19	| 项 | 值 |
20	|---|---|
21	| 平台 | 评测机 K8s pod `eval-2026-0-0-38446-435874-ptjq9`，RTX 6000D `00000000:73:00.0`，sm_120 |
22	| 数据集 | `/data/speed_bench_c1.jsonl`（12 条）/ `c8.jsonl`（36）/ `cunlimited.jsonl`（96） |
23	| 提交包 | `probe-sala-s2.tar.gz`（459 MB）— `prebuilt/` 含 `trtllm_utils.so` AOT，避开 fp4_gemm 6-skip |
24	| target / draft | `/tmp/probe_quant_out` NVFP4 / `data/eagle_draft` v2mix_20k_s3500_ood757 |
25	| 启动方式 | DEBUG-HOLD `sleep 7200` ABORT 后手动起 sglang，参数与 demo-sala/prepare_env.sh 一致 |
26	
27	## 3. 三档 bench 结果
28	
29	| 档位   | 并发 | 样本 | 之前最佳 | 本次 (D7=6/13) | Δ        | Δ%       | spec mode      |
30	|--------|------|------|---------:|---------------:|---------:|---------:|----------------|
31	| S1     | 1    | 12   | 177.88s  | **171.12s**    | -6.76s   | **-3.80%** | D7 (steps=6, dtn=13) |
32	| S8     | 8    | 36   | 343.78s  | **341.89s**    | -1.89s   | -0.55%   | D5 (steps=3, dtn=7) |
33	| Smax   | ≤64  | 96   | 895.65s  | **844.93s**    | -50.72s  | **-5.66%** | 混合 (bs≥31 → NO_SPEC) |
34	| **总** |      | 144  | 1417.31s | **1357.94s**   | -59.37s  | **-4.19%** | |
35	
36	吞吐细分：
37	
38	```
39	S1   out_tok/s 275.99   TTFT 6147ms   TPOT  47.74ms   ITL  2.03ms
40	S8   out_tok/s 398.30   TTFT 13961ms  TPOT 1295.80ms  ITL 13.14ms
41	Smax out_tok/s 492.88   TTFT 133066ms TPOT 2025.66ms  ITL 85.28ms
42	```
43	
44	## 4. 解读
45	
46	- S1 提升 -3.80% 看似是 D7 改动的直接收益（`bs=1` 路径），ITL=2.03 ms 表示 EAGLE-3 接受率高，多 1 步 draft + 多 2 候选不额外塌掉接受率。
47	- S8 持平（-0.55%）是预期的：S8 落在 D5 档（`bs=8 ∈ [2, 30]`），D7 调档完全不影响。这 0.55% 是噪声内。
48	- Smax -5.66% 是最值得注意的，96 条 + 长 duration（844 s）置信度高。Smax 大 batch 段触发 NO_SPEC（`bs ≥ 31`），但前期/末段 batch 跌破 31 时回到 D5 / D7，整体仍受益。
49	- 三档全部不退化是关键，没有局部退步换全局收益的隐患。
50	
51	## 5. 同时落的 trtllm_utils AOT 修复
52	
53	本次 bench 是在 `b7984d7 platform: trtllm_utils.so AOT prebuild — 修评测机 fp4_gemm 6-skip` 修复**之后**做的，所以本次实测在评测机上：
54	
55	- `fp4-autotune cache` 加载 OK，70 entries
56	- **`Skipped 6 unsupported tactic(s) for fp4_gemm` 0 出现**（之前评测机会全 6 skip）
57	- autotune profile 速度 4.2 prof/s → 40-115 prof/s（参见 `docs/platform/trtllm-utils-aot-fix.md`）
58	
59	D7 调档收益和 trtllm_utils 修复是叠加的，不可单独归因到 D7。
60	
61	## 6. 反向 SSH 调试设施（probe-sala-s2）
62	
63	本次能在评测机手动跑 sglang + bench，是因为提前打了带 DEBUG-HOLD 的 `probe-sala-s2.tar.gz`：
64	
65	```
66	probe-sala-s2/
67	├── prepare_env.sh              # stage 5.5 后 ABORT=1 + sleep 7200 (line 884-901)
68	├── frpc.toml                   # serverPort 7000, remotePort 6022
69	├── frpc                        # Aliyun frps 反向 tunnel client
70	├── dropbear/bin/dropbear       # bundled SSH server (apt 装不到 openssh-server)
71	├── dropbear/bin/dropbearkey
72	├── dropbear/lib/lib*.so.*      # libtomcrypt + libtommath
73	├── authorized_keys.inject      # ~/.ssh/id_ed25519_probe.pub
74	└── (其他诊断脚本同 demo-sala)
75	```
76	
77	工作流：
78	1. 提交 `probe-sala-s2.tar.gz` 到平台
79	2. 平台 entrypoint 跑 `prepare_env.sh` → quantize 模型 + 起 dropbear:2222 + 起 frpc → frps 注册 `:6022` proxy
80	3. `sleep 7200` ABORT，跳过 stage 6+（不会自动起 sglang，平台不进真正评测流程）
81	4. 本地 `ssh -i ~/.ssh/id_ed25519_probe user_4813494d@<frps_ip> -p 6022` 进入 pod
82	5. 手动跑 `python3 -m sglang.launch_server ...`、`python3 -m sglang.bench_serving ...`
83	6. 调试结束后 `kill -9 $(pgrep -f "sleep 7200")` 让 ABORT 流程触发 `kill_target` exit 1，pod 终结
84	
85	`probe-sala-s2/prebuilt/`、`assets/`、`sglang/` 等通过 symlink 复用 `demo-sala/`，`tar -h` 解引用打包，确保提交包内容与 demo-sala 完全一致 — 这样的 ad-hoc 调试也只能复现 demo-sala 当前行为，不会因为代码差异而误判。
86	
87	更详细的反向 SSH 设施 + 平台 K8s 限制（host PID namespace 隔离、CAP_SYS_ADMIN 缺失、host-pool GPU 共享等）见 [`docs/platform/eval-vs-dev-environment-audit.md`](../platform/eval-vs-dev-environment-audit.md)。
88	
89	## 7. 提交包
90	
91	```
92	demo-sala_d7_6_13_20260511.tar.gz   432 MB   md5 97e1d7645850727c849adf5a8029d277
93	```
94	
95	含本次 D7 6/13 default + R-b12x-acc-fix lock-in + b12x AOT cache + trtllm_utils.so AOT，跑评测应取得对应于上表第三列的成绩。
96
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/eagle/training/history.md"
}
```

> TOOL

tool_result Read
```
1	# EAGLE-3 训练版本历史
2	
3	按时间顺序的训练版本浓缩。当前 prod 见 [`prod.md`](../prod.md)，训练流水线规范见 [`pipeline.md`](pipeline.md)。
4	
5	时间线：v2（20K bf16）→ v3（probe [4,9,24] + NVFP4 存储 + 200K，**已否决**）→ v4（chat-template + AOI + LK + response-mask）→ det_prefill（det target baseline）→ **v2mix_20k（当前 prod）**。
6	
7	## v2（2026-04-18）
8	
9	**核心**：数据分布重构 + 管线效率 + eval 方法论全面重做。已被 v4 / det_prefill / v2mix_20k 取代。
10	
11	### 改动
12	
13	| 维度 | 改动 |
14	|---|---|
15	| 数据 | SkyPile/code/wikitext → chinese_r1 60% / stem_zh 22% / open_code 11.5% / codeforces 5.5% / dolphin_r1 1%（20K × 2048 tok） |
16	| pipeline | sync → AsyncPrefetcher（pin_memory + non_blocking transfer + queue_size=2）；GRAD_CHECKPOINT True→False（bwd -35%，peak mem 11→28 GB） |
17	| BS / grad_accum | 2/4 → **8/1**（per_sample 279ms → 169ms，-39%） |
18	| MAX_GRAD_NORM | 5.0 → 1.0 |
19	| WARMUP_STEPS | 500 → 1500（总 step 6%） |
20	| eval_ood | TTT 多步加权 acc → step-0 only + 全长（旧 weighted_acc 0.5255 → 新 step-0 acc 0.6607）|
21	| vocab | 32K（覆盖率 99.23%，K=16000 masked 4.6× 不划算） |
22	
23	### 已踩坑
24	
25	- chunked prefill 切分 hook：server `chunked-prefill-size=8192` 把 batch 32×2048=65k tok 切 8 chunk，hook 每 chunk 写一次 .pt → 一条 prompt 多条残片。修法：采集 `--chunked-prefill-size 131072`
26	- val_ood `EAGLE3_MAX_TOKENS=0` OOM：降 `--mem-fraction-static 0.70 --max-running-requests 4` + `expandable_segments`
27	- `completion_tokens >= 2000` 过滤错误：bench 本身是生产分布，应用 `> 0` 取全 64 条
28	
29	剔除 NuminaMath（cn_k12 text 实际为英文）。
30	
31	## v3（2026-04-24，已否决）
32	
33	**核心**：probe 选层 [4,9,24] + NVFP4 aux_hidden 存储 + 200K 数据。本机 smoke 看似更好，但**云训 ckpt 在 long deepresearch 上 adj_al 0.578 vs v2 0.737，e2e acceptance 劣化**，已否决。后续 aux_layers 锁回 [1,10,22]。
34	
35	### probe 选层
36	
37	`eagle/probe/probe_search.py` 的 linear probe + greedy triple search：
38	
39	| 组合 | NLL (CE) |
40	|---|---|
41	| `[1, 10, 22]` (v2) | 6.51 |
42	| `[4, 9, 24]` (v3) | **4.61**（-29% CE 但 e2e 劣化） |
43	| best pair (9, 24) | 4.45 |
44	| best single (24) | 4.92 |
45	
46	probe NLL 改善 ≠ 实际 acceptance 改善。**教训**：probe NLL 是辅助指标，最终判定必须用 e2e accept。
47	
48	### NVFP4 存储
49	
50	`eagle/nvfp4_codec.py`：aux_hidden 每 16 维 group + bf16 group-wise scale + FP4 E2M1。压缩 2.8×（48 MB → 17.3 MB），与生产 fc layer 的 W4A4 NVFP4 精度对齐。100 步对比 final step-0 acc 0.1139 → 0.1186（+0.47%，train/serve 对齐 bonus）。
51	
52	虽然 v3 整体被否，**NVFP4 aux 存储**作为正交改进保留为后续路线。
53	
54	### 数据 pipeline 分叉
55	
56	云训 200K（chinese_r1 68% / stem_zh 6% / open_code 15% / codeforces 8% / dolphin 3%，BOS 上传 ~2 TB）vs 本机 50K v2 老配比 smoke。云训机改 BOS SDK 直写并发以解决 bcecmd `bos cp -r` 5 MB/s 串行瓶颈。
57	
58	## v4（2026-05-06）
59	
60	**核心**：v2 aux/data + chat-template + response-only mask + cross-doc mask + AOI + LK loss。已被 det_prefill / v2mix_20k 取代。
61	
62	### 改动 vs v2
63	
64	| 变化 | 目的 |
65	|---|---|
66	| chat template 全量应用 | 修 v2 raw concat 与生产 token 流不一致 |
67	| assistant-only loss mask | 不在 user/system token 上训练 acceptance |
68	| `document_ids` + cross-doc attention mask | multi-doc pack 时避免跨文档泄漏 |
69	| AOI（Anchor-Offset Indices）cap=144000 | 覆盖大 position id，支撑长上下文外推 |
70	| LK lambda（kl_scale=1.0, kl_decay=3.0） | 直接优化 acceptance proxy，不只做 KL |
71	| force include `{0, 73440, 73441}` | 覆盖 `<unk>` / `<|im_end|>` / `<|im_start|>` 结构性缺口 |
72	| `target_logsumexp` 保存 | 只存 topK target logits 时保留 full-vocab normalizer，用于 sparse LK |
73	| topK | 128 |
74	| TTT depth | 3 |
75	
76	### 配置
77	
78	| 项 | 值 |
79	|---|---|
80	| aux layers | `[1, 10, 22]` |
81	| target | `MiniCPM-SALA-gptq46-calib90-90k-NVFP4`（**旧 target**，非 det） |
82	| train window | 4K shard |
83	| prompt count | 10K（v2 distribution）|
84	| AOI cap | 144000，RoPE theta 144000 |
85	| schedule | 5000 step planned，eval every 250，best-only save |
86	| best | step 2000，OOD0 = 0.7491 |
87	
88	### 限制
89	
90	训练数据来自旧 target `MiniCPM-SALA-gptq46-calib90-90k-NVFP4`。后续发现并修复了 NVFP4 target 训练/评测不一致，最新 target 是 `-det` 版本（`MiniCPM-SALA-gptq46-calib90-90k-NVFP4-det`）。
91	
92	### 已不再采纳的早期说法
93	
94	- "v4 使用 2K/8K/16K/32K/64K mixed shard"：实际是 4K shard + AOI 外推
95	- "build 端只有 971 prompts"：保留的是 10K prompts
96	- "post-EOS 自延伸是阻塞"：最终策略是 10K prompts 中 `<|im_end|>` 候选抽 10% 延伸 50 token
97	- "LK η=5"：实现用 `kl_decay=3.0`
98	
99	### 保留产物
100	
101	| 路径 | 状态 |
102	|---|---|
103	| `eagle/legacy/v4/model/aoi_lk/` | v4 SGLang draft baseline |
104	| `eagle/legacy/v4/weights/aoi_lk/best.pt` | step 2000，OOD0 0.7491 |
105	| `eagle/legacy/v4/pipeline/` | build_prompts / collect / collect_val_ood / build_vocab_cache |
106	
107	旧采集数据已清理（935 GB train + 20 GB val_ind + 102 GB val_ood）。
108	
109	## det_prefill（2026-05-07，preserved baseline）
110	
111	修复 NVFP4 target 训练/评测不一致后用 det target（`MiniCPM-SALA-gptq46-calib90-90k-NVFP4-det`）重训的版本。
112	
113	| 项 | 值 |
114	|---|---|
115	| target | `MiniCPM-SALA-gptq46-calib90-90k-NVFP4-det` |
116	| aux layers | `[1, 10, 22]` |
117	| AOI cap | 144000，RoPE theta 144000 |
118	| training route | det-target prefill-style data |
119	| OOD0 at conversion | **0.7530** |
120	
121	仍然是 prefill-style data（dataset assistant labels），不是 target-regenerated。作为 preserved baseline 保留，比对 target-regenerated 训练效果。
122	
123	## v2mix_20k_s3500_ood757（当前 prod，2026-05-08）
124	
125	20000 target-regen samples + 200 IND 物理隔离 + cosine LR + sequence packing + B/C 微调。OOD step0 = **0.7571**（vs det_prefill 0.7530，+0.41%）。
126	
127	详见 [`prod.md`](../prod.md)。
128	
129	## 演进趋势总结
130	
131	| 维度 | v2 | v3（已否） | v4 | det_prefill | **v2mix_20k** |
132	|---|---|---|---|---|---|
133	| aux layers | [1,10,22] | [4,9,24] | [1,10,22] | [1,10,22] | [1,10,22] |
134	| target | NVFP4 | NVFP4 | NVFP4 | NVFP4-det | NVFP4-det |
135	| data | dataset CoT | dataset CoT 200K | dataset CoT 10K | dataset CoT | **target-regen 20K** |
136	| chat-template / mask / AOI / LK | ❌ | ❌ | ✅ | ✅ | ✅ |
137	| forward GEMM | bf16 STE | bf16 STE | bf16 STE | bf16 STE | **NVFP4 (sm_120)** |
138	| LR schedule | warmup → plateau | warmup → plateau | warmup → plateau | warmup → plateau | **cosine 衰减** |
139	| sequence packing | ❌ | ❌ | ❌ | ❌ | ✅ FFD bin packer |
140	| OOD0 | — | (劣于 v2) | 0.7491 | 0.7530 | **0.7571** |
141
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/eagle/training/history.md",
  "old_string": "## v2mix_20k_s3500_ood757（当前 prod，2026-05-08）\n\n20000 target-regen samples + 200 IND 物理隔离 + cosine LR + sequence packing + B/C 微调。OOD step0 = **0.7571**（vs det_prefill 0.7530，+0.41%）。\n\n详见 [`prod.md`](../prod.md)。\n\n## 演进趋势总结",
  "new_string": "## v2mix_20k_s3500_ood757（当前 prod，2026-05-08）\n\n20000 target-regen samples + 200 IND 物理隔离 + cosine LR + sequence packing + B/C 微调。OOD step0 = **0.7571**（vs det_prefill 0.7530，+0.41%）。\n\n详见 [`prod.md`](../prod.md)。\n\n## v2mix_20k 后续 tuning：D7 steps/dtn 调档（2026-05-11）\n\n属于 v2mix_20k_s3500_ood757 的 post-launch 性能 tuning，不是新的 draft 版本。\n\n提交包 default：`EAGLE_D7_STEPS 5 → 6`、`EAGLE_D7_DTN 11 → 13`（`eval/start_eagle.sh` 本地启服早就是 6/13，本次同步提交包 default）。\n\n| 档位 | 并发 | 样本 | 之前最佳 | D7=6/13 | Δ% | mode |\n|---|---|---|---:|---:|---:|---|\n| S1 | 1 | 12 | 177.88s | 171.12s | **-3.80%** | D7 (steps=6, dtn=13) |\n| S8 | 8 | 36 | 343.78s | 341.89s | -0.55% | D5 |\n| Smax | ≤64 | 96 | 895.65s | 844.93s | **-5.66%** | 混合 (bs≥31 → NO_SPEC) |\n| **总** | | 144 | 1417.31s | 1357.94s | **-4.19%** | |\n\n注解：\n- S1 -3.80% 是 D7 直接收益（`bs=1` 路径）；ITL=2.03 ms 表明接受率高，多 1 步 draft + 多 2 候选不退接受率\n- S8 持平：S8 落在 D5 档（`bs=8 ∈ [2, 30]`），D7 调档不影响\n- Smax -5.66%：大 batch 段触发 NO_SPEC，前期/末段 batch 跌破 31 回 D5 / D7\n- 本次实测同时含 `trtllm_utils.so` AOT 修复（commit b7984d7），评测机 `Skipped 6 unsupported tactic(s) for fp4_gemm` 0 出现，autotune 速度 4.2 → 40-115 prof/s。D7 调档与 trtllm 修复收益叠加，不可单独归因\n\n提交包：`demo-sala_d7_6_13_20260511.tar.gz` 432 MB，含 D7 6/13 + R-b12x-acc-fix + b12x AOT cache +\ntrtllm_utils.so AOT。反向 SSH 调试设施 `probe-sala-s2`（dropbear + frpc + DEBUG-HOLD）见\n[`../../platform/cu13-stack.md`](../../platform/cu13-stack.md) §4 与\n[`../../platform/eval-vs-dev-environment-audit.md`](../../platform/eval-vs-dev-environment-audit.md)。\n\n## 演进趋势总结"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/eagle/training/history.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
```json
{
  "command": "rm docs/eagle/d7-tune-bench-20260511.md && grep -rln \"d7-tune-bench\" docs/ 2>&1",
  "description": "remove d7-tune file"
}
```

> TOOL

tool_result Bash
```
docs/eagle/README.md
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/eagle/README.md",
  "old_string": "| 验证实验日志（rope_theta / MARS / Phased Verify） | [experiments.md](experiments.md) |\n| **D7 调档 5/11 → 6/13 实测**（提交包 default 同步，S1 -3.8% / Smax -5.7%） | [d7-tune-bench-20260511.md](d7-tune-bench-20260511.md) |\n| 论文原材料库（60+ 篇 verify / tree / SSM / 长上下文） | [papers.md](papers.md) |",
  "new_string": "| 验证实验日志（rope_theta / MARS / Phased Verify） | [experiments.md](experiments.md) |\n| D7 调档 5/11 → 6/13 实测（S1 -3.8% / Smax -5.7%） | [training/history.md](training/history.md) §v2mix_20k 后续 tuning |\n| 论文索引 + MARS 落地（完整摘要归档 archive/papers-full.md） | [papers.md](papers.md) |"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/eagle/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "15",
  "status": "completed"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #15 status
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "16",
  "status": "in_progress"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #16 status
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/dflash/current.md"
}
```

> TOOL

tool_result Read
```
1	# DFlash + DDTree — 当前事实
2	
3	事实来源：本仓最新 commit + chat smoke 实测。瞬时 throughput 数字不写进来，需要重测跑 `bench/mini_bench.sh`。
4	
5	## 1. 当前可用配置
6	
7	| 算法 | 启动脚本 | 配置 | 状态 |
8	|---|---|---|---|
9	| DFlash chain (默认) | `bash eval/start_dflash.sh` | `block_size=8`, `dtn=8`, `ctx_len=8` 滑窗 | ✓ |
10	| DFlash chain (FULL_CTX) | `bash eval/start_dflash_single.sh` | `block_size=8`, `dtn=8`, ctx_len=full prefix（per-req cache）| ✓ single-batch only |
11	| DDTree | `bash eval/start_ddtree.sh` | `block_size=8`, `tree_size=96`, `dtn=97`, ancestor-only mask | ✓ |
12	
13	三者共享：
14	- 同一 draft ckpt：`dflash/outputs/train/best.pt`（NVFP4 QAT，3 层 Qwen3-style cross-attention，4.3 GB）
15	- Aux 层捕获：layer `[1, 10, 22]`（target 32 层中均匀采样的 standard attention 层）
16	- mask token id：73439（vocab 倒数第二位）
17	- target 强制 `disable_overlap_schedule=True` + `page_size=1`（spec_v1 path）
18	- `EAGLE_DYNAMIC_MODE=0`（不复用 EAGLE 的 D5/D7 切档）
19	
20	## 2. DFlash chain
21	
22	### 2.1 标准 ctx_len=8 滑窗（默认）
23	
24	- worker：`demo-sala/sglang/python/sglang/srt/speculative/dflash_worker.py`
25	- 默认走 `_build_chain_verify_input`：custom_mask = causal lower-tri，但 minicpm_backend
26	  在 verify path **不传 custom_mask**，走 `causal=True` 老路径（跟 SGLang 主线 DFlash policy 一致，见 [integration.md](integration.md) §3）
27	- cuda graph capture per-bs bucket 已实现（`dflash_draft_cuda_graph.py`）
28	- 实测 accept_len ≈ 1.15（含 user_4813494d），即平均每轮 0.15 个 draft token 被接受
29	
30	### 2.2 FULL_CTX（实验，single-batch only）
31	
32	- env：`SGLANG_DFLASH_FULL_CTX=1`，启动脚本 `eval/start_dflash_single.sh`
33	- worker per-req 持 full prompt aux_hidden cache（prefill 时存，decode 末尾 append accepted）
34	- 解决问题：训练 OnlineEngine.forward 的 `target_hidden` 是整 prompt seq_len 长（`vendor/online.py:214-260`），inference 用末尾 8 token 滑窗严重 OOD 训练 distribution
35	- 实测 accept_len 1.15 → **1.62**（+41%），throughput 60 → **75 tok/s**（峰值 106）
36	- 限制：`max_running_requests=1`（多 req 需 padding，padding 又会破坏 distribution）；动态 ctx 不能 cuda graph
37	- 后续工作：T-bucket piecewise capture / multi-req padded path
38	
39	## 3. DDTree
40	
41	- worker：复用 `DFlashWorker`，`is_tree=True` 分支
42	- algo: `speculative/ddtree_utils.py`
43	  - `build_ddtree_tree`：best-first heap，每 pop 1 node 同时 push (sibling, child)，固定 budget=96 + user_4813494d
44	  - `build_tree_retrive`：转换成 SGLang `verify_tree_greedy_func` 期望的 `next_token + next_sibling` 链表
45	  - `follow_verified_tree`：accept-path follower（占位，verify 内部直接走 sgl_kernel）
46	- mask：ancestor-only，sibling/cousin 互不可见 → **必须**走 custom_mask path
47	- attention：minicpm_backend 加了 tree-mask wrapper + manual SDPA fp32 path（默认）。
48	  详见 [ddtree.md](ddtree.md) §2
49	- 实测 accept_len **1.82-1.93**（+60% vs chain 1.15），throughput 65-69 tok/s（manual SDPA fp32 比
50	  wrapper.run 慢约 10%；后续 triton 化）
51	
52	### 3.1 mask token id 与 EOS 接近性
53	
54	- `mask_token_id=73439`，EOS=`73440`，相邻
55	- 早期发现 budget=96 在 verify 后 4-5 token 命中 EOS — 实际是 **DDTree 走 wrapper.run 时 attention
56	  数值漂移 → user_4813494d pos logit 漂移 → argmax 选 EOS**，跟 mask/EOS 邻接无关。
57	  Manual SDPA 修后未再现该现象。
58	
59	## 4. 训练 ckpt（不重训）
60	
61	- 路径：`dflash/outputs/train/best.pt`（global_step=1875）
62	- 训练数据：v2 distribution + chinese_r1 60% / stem_zh 22% / open_code 11.5% / codeforces 5.5% / dolphin 1%（跟 EAGLE 同源）
63	- pos1_acc：IND **0.466**，OOD **0.463**
64	- 量化：NVFP4 QAT，q_proj/o_proj/gate_proj/up_proj 走 FP4QATLinear；k_proj/v_proj/down_proj/fc 保 BF16
65	- aux_layers：[1, 10, 22]（K=3 层），cat 后 H=12288 维 → fc → norm → 3 层 cross-attn
66	- 用户明确不重训：剩余优化只动推理路径（SGLang + kernel）
67	
68	## 5. 后续工作（不重训）
69	
70	| 优化 | 优先级 | 收益预估 |
71	|---|---|---|
72	| DDTree manual SDPA → triton kernel | 中 | DDTree throughput +20-30%（fp32 → bf16 + tile fusion） |
73	| FULL_CTX T-bucket piecewise cuda graph | 中 | DFlash chain throughput +10-15%（恢复 +14% graph 收益） |
74	| Vectorize custom_mask 构造（移除 python loop） | 低 | per-round 50-100us → ~10us |
75	| 移除 host-device sync `.cpu().tolist()` | 低 | per-round 30-50us |
76	
77	提交包打包（Phase 4，pending）：见 [`../platform/cu13-stack.md`](../platform/cu13-stack.md) 的 `prepare_env.sh / prepare_model.sh / start.sh` 流程，需把 `best.pt` 4.3 GB 量化 + repack 到 ≤ 2 GB tar 上限内。
78
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/dflash/current.md",
  "old_string": "三者共享：\n- 同一 draft ckpt：`dflash/outputs/train/best.pt`（NVFP4 QAT，3 层 Qwen3-style cross-attention，4.3 GB）\n- Aux 层捕获：layer `[1, 10, 22]`（target 32 层中均匀采样的 standard attention 层）\n- mask token id：73439（vocab 倒数第二位）\n- target 强制 `disable_overlap_schedule=True` + `page_size=1`（spec_v1 path）\n- `EAGLE_DYNAMIC_MODE=0`（不复用 EAGLE 的 D5/D7 切档）",
  "new_string": "三者共享：\n- 同一 draft ckpt：`dflash/outputs/train/best.pt`（NVFP4 QAT，3 层 Qwen3-style cross-attention，4.3 GB）⚠️ **盘上已删**，启动脚本指向悬空路径，需重训才能复现实验，详见 [history.md](history.md) §4\n- Aux 层捕获：layer `[1, 10, 22]`（target 32 层中均匀采样的 standard attention 层）\n- mask token id：73439（vocab 倒数第二位）\n- target 强制 `disable_overlap_schedule=True` + `page_size=1`（spec_v1 path）\n- `EAGLE_DYNAMIC_MODE=0`（不复用 EAGLE 的 D5/D7 切档）"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/dflash/current.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/dflash/current.md",
  "old_string": "## 4. 训练 ckpt（不重训）\n\n- 路径：`dflash/outputs/train/best.pt`（global_step=1875）\n- 训练数据：v2 distribution + chinese_r1 60% / stem_zh 22% / open_code 11.5% / codeforces 5.5% / dolphin 1%（跟 EAGLE 同源）\n- pos1_acc：IND **0.466**，OOD **0.463**\n- 量化：NVFP4 QAT，q_proj/o_proj/gate_proj/up_proj 走 FP4QATLinear；k_proj/v_proj/down_proj/fc 保 BF16\n- aux_layers：[1, 10, 22]（K=3 层），cat 后 H=12288 维 → fc → norm → 3 层 cross-attn\n- 用户明确不重训：剩余优化只动推理路径（SGLang + kernel）",
  "new_string": "## 4. 训练 ckpt（不重训）\n\n- 路径：`dflash/outputs/train/best.pt`（global_step=1875）⚠️ **盘上已删**，`dflash/outputs/` 整个目录不存在；启动脚本默认指向此路径会失败，必须重训或外部恢复才能复现 [history.md](history.md) §4 的数字\n- 训练数据：v2 distribution + chinese_r1 60% / stem_zh 22% / open_code 11.5% / codeforces 5.5% / dolphin 1%（跟 EAGLE 同源）\n- pos1_acc：IND **0.466**，OOD **0.463**（最后一次实测）\n- 量化：NVFP4 QAT，q_proj/o_proj/gate_proj/up_proj 走 FP4QATLinear；k_proj/v_proj/down_proj/fc 保 BF16\n- aux_layers：[1, 10, 22]（K=3 层），cat 后 H=12288 维 → fc → norm → 3 层 cross-attn\n- 用户明确不重训：剩余优化只动推理路径（SGLang + kernel）"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/dflash/current.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/dflash/history.md",
  "offset": 95,
  "limit": 35
}
```

> TOOL

tool_result Read
```
95	| gate_proj | FP4QAT | 同上 |
96	| up_proj | FP4QAT | 同上 |
97	| **k_proj** | BF16 | 同 Linear 看 noise_embedding（embed 分布）+ target_hidden（fc-projected 多层 cat 分布）。两个 distribution，量化 weight 损失大。10M params 总量，留 BF16 几乎无开销 |
98	| **v_proj** | BF16 | 同上 |
99	| **down_proj** | BF16 | QDLM (arXiv:2508.14896) 显示 dLLM massive outlier 集中在 FFN 第二 linear 输入，量化损失大 |
100	| **fc** | BF16 | 输入 cat 后 12288 维，per-tensor input scaling 范围太宽 |
101	
102	NVFP4 input quant 用 per-block (size=16) scale，per-block max 用 calibration 静态确定
103	（`input_scale_inv` 加载自 ckpt，runtime 不变）。
104	
105	### 3.3 chain vs tree 决策
106	
107	调研期定为 chain（见 §2.3）：
108	- GLA `update_mamba_state_after_mtp_verify` 是 chain 设计（h_t 依赖 h_{t-1}）
109	- chain verify 跟 GLA 递推语义一致，无需新 kernel
110	- tree 需 sibling 不污染 GLA state，难度大
111	
112	实施期发现 DDTree 用 SGLang `verify_tree_greedy_func` C++ kernel 完全支持任意
113	tree，只是 attention 侧 mask 处理需要改。所以 chain 是 prod，DDTree 作扩展实验。
114	
115	## 4. 训练数据 + ckpt
116	
117	### 4.1 数据
118	
119	- 跟 EAGLE 共享 v2 distribution: chinese_r1 60% / stem_zh 22% / open_code 11.5% / codeforces 5.5% / dolphin 1%
120	- 用 target 模型自生成 assistant response（target-regenerated）
121	- 4K shard + AOI cap=144000，**未**做 16K/32K/64K mixed shards
122	
123	### 4.2 训练超参（实际，非反推）
124	
125	- block_size=8（非 paper 的 16）
126	- 3 层 Qwen3-style cross-attn（非 paper 的 5 层；为 inference latency / memory）
127	- 2 epoch（global_step=1875）
128	- AdamW lr=1e-4, betas=(0.9, 0.95), wd=0.01, cosine + linear warmup
129	- bf16 混合精度，FP4_QAT 启用（per CLAUDE.md `DFLASH_FP4_QAT=1`）
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/dflash/history.md",
  "old_string": "## 4. 训练数据 + ckpt\n\n### 4.1 数据",
  "new_string": "## 4. 训练数据 + ckpt\n\n> ⚠️ **2026-05-20 状态**：`dflash/outputs/train/best.pt` 与整个 `dflash/outputs/` 目录在仓内\n> 已删，盘上不存在。下面 §4.3 描述的 ckpt schema、§4.2 实际超参、pos1=0.466 IND/0.463 OOD\n> 数字记录的是被删之前的训练状态；要复现实验需重训。`eval/start_dflash*.sh` 默认指向悬空路径，\n> 启动会失败。\n\n### 4.1 数据"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/dflash/history.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "16",
  "status": "completed"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #16 status
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "17",
  "status": "in_progress"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #17 status
```

> TOOL

tool_use Read
```json
{
  "file_path": "/user_4813494d/openbmb/docs/README.md"
}
```

> TOOL

tool_result Read
```
1	# 文档导航
2	
3	SOAR MiniCPM-SALA 推理优化工作区。项目总览见仓库根 [`CLAUDE.md`](../CLAUDE.md)。
4	
5	## 接续
6	
7	| 文档 | 内容 |
8	|---|---|
9	| [handover.md](handover.md) | **新 session 接续指南**（红线、当前栈、prefill / decode / eagle 状态、下一步候选） |
10	
11	## 主题
12	
13	每个主题一个子目录，目录下有 `README.md` 索引 + 各子文档。
14	
15	| 主题 | 内容 |
16	|---|---|
17	| [platform/](platform/) | 平台、cu13 栈、probe-sala 部署、SGLang fork 升级判定 |
18	| [quant/](quant/) | NVFP4 量化方案（GPTQ + FourOverSix + 校准） |
19	| [gemm/](gemm/) | sm_120 GEMM/kernel 底层调优（CUTLASS / Marlin / 硬件 / profile 方法论 / `.so` 替换日志） |
20	| [prefill/](prefill/) | 长上下文 prefill：当前事实 + 历史调研 + 已枯竭路线 |
21	| [decode/](decode/) | Decode 算子优化：当前 SOP + profile 方法论 + 误归因教训 |
22	| [eagle/](eagle/) | EAGLE-3 spec decoding：架构 / 适配 / 训练 / collapse / 实验 / 论文 |
23	| [ngram/](ngram/) | request-local ngram lookup：probe / EAGLE routing / CUDA graph 稳定性修复 |
24	| [dflash/](dflash/) | DFlash + DDTree spec decoding：block diffusion draft + best-first heap tree verify |
25	| [blog/](blog/) | 每周对外分享（SOAR 周冠军技术分享） |
26	
27	## 快速定位
28	
29	| 想了解… | 入口 |
30	|---|---|
31	| 当前生产配置速览 | [handover.md](handover.md) §1 |
32	| cu13 升级要点 + 回滚 | [platform/cu13-stack.md](platform/cu13-stack.md) §3 |
33	| `220c18cc` vs `32d27c7` `.so` 与 EAGLE 兼容性警告 | [gemm/marlin.md](gemm/marlin.md) §6 |
34	| NVFP4 KV 为何不可用 | [quant/nvfp4.md](quant/nvfp4.md) §4 |
35	| prefill 当前热点 | [prefill/current.md](prefill/current.md) §1 |
36	| decode profile 方法论（**重要避坑**） | [decode/current.md](decode/current.md) §3 |
37	| 当前 prod draft（v2mix_20k_s3500_ood757） | [eagle/prod.md](eagle/prod.md) |
38	| ngram routing 当前实现 | [ngram/routing.md](ngram/routing.md) |
39	| collapse 根因 | [eagle/collapse.md](eagle/collapse.md) §1 |
40	| 已落产实验（rope_theta=1M / MARS θ=0.85） | [eagle/experiments.md](eagle/experiments.md) |
41	| DFlash / DDTree 当前状态（启动入口、accept rate） | [dflash/current.md](dflash/current.md) §1 |
42	| DDTree 输出乱码根因（FlashInfer custom_mask 数值漂移） | [dflash/ddtree.md](dflash/ddtree.md) §2 |
43	| SGLang 主线 DFlash skip custom_mask policy（关键参考） | [dflash/integration.md](dflash/integration.md) §3 |
44	
45	## 惯例
46	
47	- 速度结论（e2e bench 秒级数字）不写进文档，随时可过期。需要数据时直接跑 `bench/mini_bench.sh`
48	- 文档记录**可复现的方法**和**已验证的决策**，不记录瞬时测速结果
49	- 负结果必须保留，防止重踩
50	- `current.md` = 当前事实；`history.md` = 已枯竭路线 + 调查教训。新实验追加到 `eagle/experiments.md`
51	- 跨目录引用用 `../<topic>/<file>.md`，同目录用文件名
52
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/README.md",
  "old_string": "| 主题 | 内容 |\n|---|---|\n| [platform/](platform/) | 平台、cu13 栈、probe-sala 部署、SGLang fork 升级判定 |\n| [quant/](quant/) | NVFP4 量化方案（GPTQ + FourOverSix + 校准） |\n| [gemm/](gemm/) | sm_120 GEMM/kernel 底层调优（CUTLASS / Marlin / 硬件 / profile 方法论 / `.so` 替换日志） |\n| [prefill/](prefill/) | 长上下文 prefill：当前事实 + 历史调研 + 已枯竭路线 |\n| [decode/](decode/) | Decode 算子优化：当前 SOP + profile 方法论 + 误归因教训 |\n| [eagle/](eagle/) | EAGLE-3 spec decoding：架构 / 适配 / 训练 / collapse / 实验 / 论文 |\n| [ngram/](ngram/) | request-local ngram lookup：probe / EAGLE routing / CUDA graph 稳定性修复 |\n| [dflash/](dflash/) | DFlash + DDTree spec decoding：block diffusion draft + best-first heap tree verify |\n| [blog/](blog/) | 每周对外分享（SOAR 周冠军技术分享） |\n\n## 快速定位\n\n| 想了解… | 入口 |\n|---|---|\n| 当前生产配置速览 | [handover.md](handover.md) §1 |\n| cu13 升级要点 + 回滚 | [platform/cu13-stack.md](platform/cu13-stack.md) §3 |\n| `220c18cc` vs `32d27c7` `.so` 与 EAGLE 兼容性警告 | [gemm/marlin.md](gemm/marlin.md) §6 |\n| NVFP4 KV 为何不可用 | [quant/nvfp4.md](quant/nvfp4.md) §4 |\n| prefill 当前热点 | [prefill/current.md](prefill/current.md) §1 |\n| decode profile 方法论（**重要避坑**） | [decode/current.md](decode/current.md) §3 |\n| 当前 prod draft（v2mix_20k_s3500_ood757） | [eagle/prod.md](eagle/prod.md) |\n| ngram routing 当前实现 | [ngram/routing.md](ngram/routing.md) |\n| collapse 根因 | [eagle/collapse.md](eagle/collapse.md) §1 |\n| 已落产实验（rope_theta=1M / MARS θ=0.85） | [eagle/experiments.md](eagle/experiments.md) |\n| DFlash / DDTree 当前状态（启动入口、accept rate） | [dflash/current.md](dflash/current.md) §1 |\n| DDTree 输出乱码根因（FlashInfer custom_mask 数值漂移） | [dflash/ddtree.md](dflash/ddtree.md) §2 |\n| SGLang 主线 DFlash skip custom_mask policy（关键参考） | [dflash/integration.md](dflash/integration.md) §3 |",
  "new_string": "| 主题 | 内容 |\n|---|---|\n| [platform/](platform/) | 平台、cu13 栈、SGLang fork 升级判定（probe-sala 已退役） |\n| [quant/](quant/) | NVFP4 量化方案（GPTQ + FourOverSix + wikitext 90 样本校准） |\n| [gemm/](gemm/) | sm_120 GEMM/kernel 底层调优（CUTLASS / Marlin / b12x / 硬件 / profile 方法论 / `.so` 替换日志） |\n| [prefill/](prefill/) | 长上下文 prefill：当前事实 + 历史调研 + 仓内 piecewise/main-test 调研工作区 |\n| [decode/](decode/) | Decode 算子优化：当前 SOP + b12x 状态 + profile 方法论 + 误归因教训 |\n| [eagle/](eagle/) | EAGLE-3 spec decoding：架构 / 适配 / 训练 / collapse / 实验 / 论文索引 |\n| [ngram/](ngram/) | request-local ngram lookup：probe / EAGLE routing / CUDA graph 稳定性修复 |\n| [dflash/](dflash/) | DFlash + DDTree spec decoding（**探索性，非生产**） |\n| [blog/](blog/) | 每周对外分享（SOAR 周冠军技术分享） |\n\n## 快速定位\n\n| 想了解… | 入口 |\n|---|---|\n| 当前生产配置速览 | [handover.md](handover.md) §1 |\n| cu13 升级要点 + 回滚 | [platform/cu13-stack.md](platform/cu13-stack.md) §3 |\n| `220c18cc` vs `32d27c7` `.so` 与 EAGLE 兼容性警告 | [gemm/marlin.md](gemm/marlin.md) §6 |\n| b12x kernel lock-in + 提交包为何默认 OFF | [gemm/marlin.md](gemm/marlin.md) §4 / [decode/current.md](decode/current.md) §4.1 |\n| NVFP4 校准实际参数（wikitext 90 样本 / 90K 上下文） | [quant/nvfp4.md](quant/nvfp4.md) §1 |\n| NVFP4 KV 为何不可用 | [quant/nvfp4.md](quant/nvfp4.md) §4 |\n| prefill 当前热点 | [prefill/current.md](prefill/current.md) §1 |\n| prefill 调研工作区（piecewise + main-test，go/no-go 结论） | [prefill/current.md](prefill/current.md) §5 |\n| decode profile 方法论（**重要避坑**） | [decode/current.md](decode/current.md) §3 |\n| 当前 prod draft（v2mix_20k_s3500_ood757） | [eagle/prod.md](eagle/prod.md) |\n| D7 调档 5/11 → 6/13 实测 | [eagle/training/history.md](eagle/training/history.md) |\n| ngram routing 当前实现 | [ngram/routing.md](ngram/routing.md) |\n| collapse 根因 | [eagle/collapse.md](eagle/collapse.md) §1 |\n| 已落产实验（rope_theta=1M / MARS θ=0.85） | [eagle/experiments.md](eagle/experiments.md) |\n| MARS verify 工程落地 | [eagle/papers.md](eagle/papers.md) §1 |\n| DFlash / DDTree 当前状态（启动入口、accept rate） | [dflash/current.md](dflash/current.md) §1 |\n| DDTree 输出乱码根因（FlashInfer custom_mask 数值漂移） | [dflash/ddtree.md](dflash/ddtree.md) §2 |\n| SGLang 主线 DFlash skip custom_mask policy（关键参考） | [dflash/integration.md](dflash/integration.md) §3 |\n| DFlash best.pt 路径已删（不可复现） | [dflash/history.md](dflash/history.md) §4 |"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/README.md",
  "old_string": "| 文档 | 内容 |\n|---|---|\n| [handover.md](handover.md) | **新 session 接续指南**（红线、当前栈、prefill / decode / eagle 状态、下一步候选） |",
  "new_string": "| 文档 | 内容 |\n|---|---|\n| [handover.md](handover.md) | **新 session 接续指南**（指针为主，不重复 CLAUDE.md 内容） |"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/README.md",
  "old_string": "- `current.md` = 当前事实；`history.md` = 已枯竭路线 + 调查教训。新实验追加到 `eagle/experiments.md`\n- 跨目录引用用 `../<topic>/<file>.md`，同目录用文件名",
  "new_string": "- `current.md` = 当前事实；`history.md` = 已枯竭路线 + 调查教训。新实验追加到 `eagle/experiments.md`\n- `archive/` 子目录存早期长篇调研归档（changelog 早期轮次、papers 完整摘记等），主文件保留活跃决策\n- 跨目录引用用 `../<topic>/<file>.md`，同目录用文件名"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use TaskUpdate
```json
{
  "taskId": "17",
  "status": "completed"
}
```

> TOOL

tool_result TaskUpdate
```
Updated task #17 status
```

> TOOL

tool_use Bash
```json
{
  "command": "git status --short && echo \"---\" && wc -l docs/handover.md docs/eagle/papers.md docs/gemm/changelog.md docs/gemm/todo.md docs/dflash/history.md",
  "description": "verify net changes + sizes"
}
```

> TOOL

tool_result Bash
```
M CLAUDE.md
 M demo-sala/preprocess_model.py
 M docs/README.md
 M docs/decode/README.md
 M docs/decode/current.md
 M docs/dflash/README.md
 M docs/dflash/current.md
 M docs/dflash/history.md
 M docs/eagle/README.md
 D docs/eagle/d7-tune-bench-20260511.md
 D docs/eagle/dflash.md
 M docs/eagle/papers.md
 M docs/eagle/training/history.md
 M docs/gemm/README.md
R  docs/gemm/bottleneck_cards/01_o_proj_std_M48.md -> docs/gemm/bottleneck_card_samples/01_o_proj_std_M48.md
R  docs/gemm/bottleneck_cards/02_down_proj_M128.md -> docs/gemm/bottleneck_card_samples/02_down_proj_M128.md
 M docs/gemm/changelog.md
 M docs/gemm/kernels-sm120.md
 M docs/gemm/marlin.md
 M docs/gemm/sol_table.md
 M docs/gemm/todo.md
 M docs/handover.md
 M docs/platform/README.md
 M docs/platform/cu13-stack.md
 M docs/prefill/README.md
 M docs/prefill/current.md
 M docs/quant/README.md
 M docs/quant/nvfp4.md
?? docs/eagle/300k-training-plan.md
?? docs/eagle/archive/
?? docs/gemm/archive/
?? docs/gemm/bottleneck_card_samples/TEMPLATE.md
---
   97 docs/handover.md
  111 docs/eagle/papers.md
  450 docs/gemm/changelog.md
   84 docs/gemm/todo.md
  191 docs/dflash/history.md
  933 total
```

> TOOL

tool_use Bash
```json
{
  "command": "head -20 docs/eagle/300k-training-plan.md && echo \"---\" && git log --oneline -- docs/eagle/300k-training-plan.md 2>&1 | head",
  "description": "check 300k-training-plan"
}
```

> TOOL

tool_result Bash
```
# 300K 训练计划：代码地图 + 本地化约束 + Profile 入口

> 写于 2026-05-21。Eagle v3mix 300K 数据已全量上传 BOS，本地无数据，
> 目标在单卡 RTX PRO 6000D 上完成 **1 epoch** 训练。本文档是给自己看的
> 工作底图，先把代码事实摆清再决定下一步。

## 1. 代码地图（实读 2026-05-21）

```
eagle/
├── core/
│   ├── arch.py            Eagle3Attention / MLP / DecoderLayer + RoPE + RMSNorm
│   └── fp4_quant.py       FP4QATLinear、_NVFP4LinearFn、fp4_quant_freeze/unfreeze
├── nvfp4_codec.py         aux_hidden 磁盘存储编解码（bf16 ↔ packed FP4 + bf16 scale）
├── training/sala_draft/
│   ├── train.py           当前主训练入口（v4: AOI + LK^λ + 响应掩码 + 跨文档）
│   ├── packing.py         PackedFileSampler、make_packed_batch、AOI 跨段位置、TTT 尾掩码
│   └── convert_to_sglang.py  训练 best.pt → SGLang draft 模型目录（NVFP4 打包导出）
├── pipelines/target_regen/
│   ├── start_server.sh           老 10K 路径起服
---
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/eagle/README.md",
  "old_string": "| **当前 prod draft（v2mix_20k_s3500_ood757）** | [prod.md](prod.md) |\n| **训练子目录**（pipeline + history + data-compression） | [training/](training/) |",
  "new_string": "| **当前 prod draft（v2mix_20k_s3500_ood757）** | [prod.md](prod.md) |\n| **训练子目录**（pipeline + history + data-compression） | [training/](training/) |\n| 300K 训练计划（v3mix 300K，单卡 1 epoch） | [300k-training-plan.md](300k-training-plan.md) |"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/eagle/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -rln \"probe-sala/\" docs/ CLAUDE.md 2>/dev/null | head",
  "description": "verify no stale probe-sala/ refs remain"
}
```

> TOOL

tool_result Bash
```
docs/handover.md
docs/gemm/marlin.md
docs/platform/cu13-stack.md
CLAUDE.md
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"probe-sala/\" docs/handover.md docs/gemm/marlin.md docs/platform/cu13-stack.md CLAUDE.md 2>&1 | head -20",
  "description": "show remaining probe-sala refs to evaluate"
}
```

> TOOL

tool_result Bash
```
CLAUDE.md:49:| `probe-sala-s2/` | 反向 SSH 调试 sidecar（authorized_keys 注入 + dropbear/frpc）。原 `probe-sala/` 平台诊断探针已退役（commit b74c10d 删除） |
docs/handover.md:97:`probe-sala/` 平台诊断探针已退役（commit `b74c10d`），要恢复请从 git history 拉。
docs/platform/cu13-stack.md:96:原 `probe-sala/` 是面向评测平台的一次性、无 fallback、BOS 鉴权下发的 cu13 安装包，与
docs/platform/cu13-stack.md:97:`demo-sala/`（增量升级）路径分离。**当前 `probe-sala/` 目录已删（commit `b74c10d`），统一走
docs/platform/cu13-stack.md:102:跟提交流程无关。设计要点 / verify 项 / 已踩坑清单全部在 git history（`probe-sala/` deleted 之前
docs/gemm/marlin.md:137:| probe-sala/prepare_env.sh 部署后 | `220c18cc`（Apr 21） | 正常 |
docs/gemm/marlin.md:145:- `probe-sala/common_ops.abi3.so`（`220c18cc`）是目前唯一被验证可在 EAGLE 起服正常的 `.so`
```

> TOOL

tool_use Bash
```json
{
  "command": "python3 <<'PY'\nimport re, os, pathlib\n\nuser_4813494d = pathlib.Path(\"docs\")\nbroken = []\nall_md = list(user_4813494d.rglob(\"*.md\"))\n\nfor md in all_md:\n    text = md.read_text(encoding=\"utf-8\")\n    for m in re.finditer(r'\\]\\(([^)]+)\\)', text):\n        target = m.group(1)\n        if target.startswith((\"http://\",\"https://\",\"#\")):\n            continue\n        # strip anchor\n        clean = target.split(\"#\")[0]\n        if not clean:\n            continue\n        # resolve relative to md's parent\n        resolved = (md.parent / clean).resolve()\n        if not resolved.exists():\n            broken.append((str(md), target))\n\nif broken:\n    print(f\"Found {len(broken)} broken refs:\")\n    for src, tgt in broken[:40]:\n        print(f\"  {src} -> {tgt}\")\nelse:\n    print(\"All doc links resolve OK\")\nPY",
  "description": "scan doc markdown for broken refs"
}
```

> TOOL

tool_result Bash
```
Found 12 broken refs:
  docs/dflash/ddtree.md -> ../../tmp/test_verify_tree.py
  docs/eagle/archive/papers-full.md -> experiments.md
  docs/eagle/archive/papers-full.md -> experiments.md
  docs/gemm/sol_table.md -> ../../outputs/baseline/latest/baseline.md
  docs/gemm/sol_table.md -> ../../outputs/baseline/latest/baseline.md
  docs/gemm/archive/changelog-r1-r12prep.md -> kernels-sm120.md
  docs/gemm/archive/changelog-r1-r12prep.md -> methodology.md
  docs/gemm/archive/changelog-r1-r12prep.md -> methodology.md
  docs/gemm/archive/changelog-r1-r12prep.md -> dead-ends.md
  docs/gemm/archive/changelog-r1-r12prep.md -> methodology.md
  docs/gemm/archive/changelog-r1-r12prep.md -> methodology.md#35-quick_validate-性能闸门-唯一标准
  docs/quant/nvfp4.md -> marlin.md
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"marlin.md\" docs/quant/nvfp4.md",
  "description": "find marlin.md ref in nvfp4"
}
```

> TOOL

tool_result Bash
```
51:详细调优记录、b12x 2-tier dispatch、负结果见 [`marlin.md`](marlin.md)。
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/user_4813494d/openbmb/docs/quant/nvfp4.md",
  "old_string": "详细调优记录、b12x 2-tier dispatch、负结果见 [`marlin.md`](marlin.md)。",
  "new_string": "详细调优记录、b12x 2-tier dispatch、负结果见 [`../gemm/marlin.md`](../gemm/marlin.md)。"
}
```

> TOOL

tool_result Edit
```
The file /user_4813494d/openbmb/docs/quant/nvfp4.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"experiments.md\\|methodology.md\\|kernels-sm120.md\\|dead-ends.md\" docs/eagle/archive/papers-full.md docs/gemm/archive/changelog-r1-r12prep.md 2>&1 | head -20",
  "description": "find archive refs"
}
```

> TOOL

tool_result Bash
```
docs/eagle/archive/papers-full.md:5:> **定位：原材料库**。记录调查发现的事实和论文内容，不做结论或行动建议。工程决策和实测数据见 [`experiments.md`](experiments.md)。
docs/eagle/archive/papers-full.md:81:MARS 实测已完成，theta=0.85 全量 64 样本生产配置已部署。详细实测数据见 [`experiments.md`](experiments.md) §方向三。
docs/gemm/archive/changelog-r1-r12prep.md:5:> 关键决策摘要见 todo.md §0；死路 catalog 见 [`../dead-ends.md`](../dead-ends.md)。
docs/gemm/archive/changelog-r1-r12prep.md:30:| **caveat** | **microbench 用裸 `cutlass_scaled_fp4_mm`，没启用生产路径的 flashinfer mm_fp4 + autotune cache**。生产 CUTLASS 实测应快 1.27-3.59×（[kernels-sm120.md §7.1](kernels-sm120.md)），所以真实最优阈值应该更激进（每个 shape 比当前推荐更早切到 CUTLASS）|
docs/gemm/archive/changelog-r1-r12prep.md:204:**真实结论**：**R2 在 noise 范围内，与 baseline 等价**。之前的 +3.18% 和 -40% 都是 **bench cold path 测量噪声** —— [methodology.md §10](methodology.md) 反模式"测量本身扰动测量"+"没排除冷启动 / JIT"实证发生在自己身上。
docs/gemm/archive/changelog-r1-r12prep.md:225:写入 [methodology.md §10 反模式](methodology.md) + [dead-ends.md §F](dead-ends.md)：
docs/gemm/archive/changelog-r1-r12prep.md:318:加入 [methodology.md](methodology.md)：
docs/gemm/archive/changelog-r1-r12prep.md:371:不阻塞 R5a lock-in（B' 干净跑证明 R5a 不引入 prefill 退化）。但写入 dead-ends.md 作为 known measurement noise。
docs/gemm/archive/changelog-r1-r12prep.md:402:- ~~E: 跑 mini_bench 完整 S1/S8~~ — **废弃**，per [methodology.md §3.5](methodology.md#35-quick_validate-性能闸门-唯一标准) 闸门切到 quick_validate
docs/gemm/archive/changelog-r1-r12prep.md:471:R5a 是 SOP 第一次抓到"测试 config 不等于生产 config"这个 trap。教训写入 `docs/gemm/dead-ends.md`：
docs/gemm/archive/changelog-r1-r12prep.md:570:**R6 结论**：metadata-strip 不是 silver bullet。autotune cache upside 需要 fresh tune（fine-grained M bucket），不是元数据强制加载。这一项写入 dead-ends.md。
docs/gemm/archive/changelog-r1-r12prep.md:824:（vLLM PR #34577 / dead-ends.md §B 已沉淀）：
docs/gemm/archive/changelog-r1-r12prep.md:847:- R10/R11/R12 sgl-kernel CUTLASS cherry-pick: dead-ends.md §N
docs/gemm/archive/changelog-r1-r12prep.md:882:| R8 | sweep -bs=24 | ❌ Revert (dead-ends.md §L) |
docs/gemm/archive/changelog-r1-r12prep.md:884:| R10/R11/R12 | sgl-kernel CUTLASS cherry-pick | ❌ dead-ends.md §N（hot path & version 双错位）|
```

> TOOL

tool_use Bash
```json
{
  "command": "sed -i 's|\\](experiments.md)|](../experiments.md)|g; s|\\](experiments.md#|](../experiments.md#|g' docs/eagle/archive/papers-full.md\nsed -i 's|\\](kernels-sm120.md|](../kernels-sm120.md|g; s|\\](methodology.md|](../methodology.md|g; s|\\](dead-ends.md|](../dead-ends.md|g' docs/gemm/archive/changelog-r1-r12prep.md\necho \"done\"",
  "description": "fix relative refs in archived files"
}
```

> TOOL

tool_result Bash
```
done
```

> TOOL

tool_use Bash
```json
{
  "command": "python3 <<'PY'\nimport re, pathlib\nuser_4813494d = pathlib.Path(\"docs\")\nbroken = []\nfor md in user_4813494d.rglob(\"*.md\"):\n    text = md.read_text(encoding=\"utf-8\")\n    for m in re.finditer(r'\\]\\(([^)]+)\\)', text):\n        target = m.group(1)\n        if target.startswith((\"http://\",\"https://\",\"#\")):\n            continue\n        clean = target.split(\"#\")[0]\n        if not clean:\n            continue\n        resolved = (md.parent / clean).resolve()\n        if not resolved.exists():\n            broken.append((str(md), target))\nfor src, tgt in broken:\n    print(f\"  {src} -> {tgt}\")\nprint(f\"total: {len(broken)}\")\nPY",
  "description": "recheck broken refs"
}
```

> TOOL

tool_result Bash
```
docs/dflash/ddtree.md -> ../../tmp/test_verify_tree.py
  docs/gemm/sol_table.md -> ../../outputs/baseline/latest/baseline.md
  docs/gemm/sol_table.md -> ../../outputs/baseline/latest/baseline.md
total: 3
```

> TOOL

tool_use Bash
```json
{
  "command": "git status --short && echo \"---\" && echo \"DOC TOTALS:\" && find docs -name \"*.md\" -type f | xargs wc -l | tail -1 && echo \"---\" && echo \"ARCHIVE:\" && ls docs/eagle/archive/ docs/gemm/archive/ 2>&1",
  "description": "final state summary"
}
```

> TOOL

tool_result Bash
```
M CLAUDE.md
 M demo-sala/preprocess_model.py
 M docs/README.md
 M docs/decode/README.md
 M docs/decode/current.md
 M docs/dflash/README.md
 M docs/dflash/current.md
 M docs/dflash/history.md
 M docs/eagle/README.md
 D docs/eagle/d7-tune-bench-20260511.md
 D docs/eagle/dflash.md
 M docs/eagle/papers.md
 M docs/eagle/training/history.md
 M docs/gemm/README.md
R  docs/gemm/bottleneck_cards/01_o_proj_std_M48.md -> docs/gemm/bottleneck_card_samples/01_o_proj_std_M48.md
R  docs/gemm/bottleneck_cards/02_down_proj_M128.md -> docs/gemm/bottleneck_card_samples/02_down_proj_M128.md
 M docs/gemm/changelog.md
 M docs/gemm/kernels-sm120.md
 M docs/gemm/marlin.md
 M docs/gemm/sol_table.md
 M docs/gemm/todo.md
 M docs/handover.md
 M docs/platform/README.md
 M docs/platform/cu13-stack.md
 M docs/prefill/README.md
 M docs/prefill/current.md
 M docs/quant/README.md
 M docs/quant/nvfp4.md
?? docs/eagle/300k-training-plan.md
?? docs/eagle/archive/
?? docs/gemm/archive/
?? docs/gemm/bottleneck_card_samples/TEMPLATE.md
---
DOC TOTALS:
 11289 total
---
ARCHIVE:
docs/eagle/archive/:
papers-full.md

docs/gemm/archive/:
changelog-r1-r12prep.md
```

> AGENT

全部 11 个 phase 完成。

**结构变更总结**：

- **删除**：`docs/eagle/dflash.md`（已 deprecate，内容并入 `docs/dflash/history.md` §2）、`docs/eagle/d7-tune-bench-20260511.md`（并入 `docs/eagle/training/history.md`）、全仓 `.ipynb_checkpoints/`（9 个目录）
- **重命名**：`docs/gemm/bottleneck_cards/` → `bottleneck_card_samples/` + 新增 `TEMPLATE.md`（明确"仅样例，全集 54 张未补齐"）
- **归档**：`docs/eagle/archive/papers-full.md`（原 papers.md 809 行）、`docs/gemm/archive/changelog-r1-r12prep.md`（原 changelog R1–R12-prep 898 行）
- **精简改写**：`docs/handover.md`（190→97 行，去掉与 CLAUDE.md 重复的栈表 + 已退役 probe-sala + 已落产候选）、`docs/eagle/papers.md`（809→111 行，保留 MARS 实装+索引）、`docs/gemm/todo.md`（191→84 行，按 lock-in 状态重组）、`docs/gemm/changelog.md`（1338→450 行，只留 R-b12x 及以后）
- **事实修正**：CLAUDE.md（NVFP4 48K/128 → 90K/90、`probe-sala/` → `probe-sala-s2/`、b12x 默认 OFF 补充）、`demo-sala/preprocess_model.py` docstring、`docs/quant/nvfp4.md`、`docs/decode/current.md`（b12x 真实 lock-in 状态）、`docs/gemm/marlin.md` §4（b12x 重写）、`docs/gemm/kernels-sm120.md` §1 / §7.4（去重）、`docs/platform/cu13-stack.md` §4（probe-sala 退役）
- **补索引**：`docs/prefill/current.md` §5（新增 piecewise + main-test 工作区）、`docs/eagle/README.md`（D7 调档指向 training/history、300k-training-plan、papers 注释）、`docs/dflash/{current,history}.md`（best.pt 已删警示）、`docs/README.md` 快速定位扩 b12x / NVFP4 校准 / prefill 调研工作区
- **跨文件 link 修复**：归档文件的相对路径、`quant/nvfp4.md` 的 `marlin.md` 指向

总文档行数：10867 → 11289（净增 422 行，主要来自归档保留 + 工作区索引新写），但活跃主文件均显著精简，结构更清晰：每主题 README 是索引；`current.md` 是事实；`history.md` 是已枯竭路线；`archive/` 是长篇调研归档。剩 3 个 broken link 都是引用到 docs/ 外部的运行时 artifact（`/tmp` 调试脚本、`outputs/baseline/`），非文档链不修。

> DEVELOPER

做提交和推送

> TOOL

tool_use Bash
```json
{
  "command": "git status && echo \"---LOG---\" && git log --oneline -5",
  "description": "git status + recent log"
}
```

> TOOL

tool_result Bash
```
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	renamed:    docs/gemm/bottleneck_cards/01_o_proj_std_M48.md -> docs/gemm/bottleneck_card_samples/01_o_proj_std_M48.md
	renamed:    docs/gemm/bottleneck_cards/02_down_proj_M128.md -> docs/gemm/bottleneck_card_samples/02_down_proj_M128.md

Changes not staged for commit:
  (use "git add/rm <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   CLAUDE.md
	modified:   demo-sala/preprocess_model.py
	modified:   docs/README.md
	modified:   docs/decode/README.md
	modified:   docs/decode/current.md
	modified:   docs/dflash/README.md
	modified:   docs/dflash/current.md
	modified:   docs/dflash/history.md
	modified:   docs/eagle/README.md
	deleted:    docs/eagle/d7-tune-bench-20260511.md
	deleted:    docs/eagle/dflash.md
	modified:   docs/eagle/papers.md
	modified:   docs/eagle/training/history.md
	modified:   docs/gemm/README.md
	modified:   docs/gemm/changelog.md
	modified:   docs/gemm/kernels-sm120.md
	modified:   docs/gemm/marlin.md
	modified:   docs/gemm/sol_table.md
	modified:   docs/gemm/todo.md
	modified:   docs/handover.md
	modified:   docs/platform/README.md
	modified:   docs/platform/cu13-stack.md
	modified:   docs/prefill/README.md
	modified:   docs/prefill/current.md
	modified:   docs/quant/README.md
	modified:   docs/quant/nvfp4.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	docs/eagle/300k-training-plan.md
	docs/eagle/archive/
	docs/gemm/archive/
	docs/gemm/bottleneck_card_samples/TEMPLATE.md

---LOG---
141fb6d prefill: main-test prefill 研究工作区
3c17ea3 piecewise: Piecewise CUDA Graph prefill 调研工作区
0c37930 docs/blog: 第九周 — 从 KL 到接受率（LK^λ）
2b2f88e docs/gemm/so-replacements: 追加 5/15 + 5/17 .so 备份日志
77d7d95 demo-sala: 新增 pack.sh 提交包打包脚本
```

> TOOL

tool_use Bash
```json
{
  "command": "git add CLAUDE.md demo-sala/preprocess_model.py docs/README.md docs/handover.md \\\n  docs/decode/README.md docs/decode/current.md \\\n  docs/dflash/README.md docs/dflash/current.md docs/dflash/history.md \\\n  docs/eagle/README.md docs/eagle/d7-tune-bench-20260511.md docs/eagle/dflash.md \\\n  docs/eagle/papers.md docs/eagle/training/history.md docs/eagle/300k-training-plan.md \\\n  docs/eagle/archive/ \\\n  docs/gemm/README.md docs/gemm/changelog.md docs/gemm/kernels-sm120.md \\\n  docs/gemm/marlin.md docs/gemm/sol_table.md docs/gemm/todo.md \\\n  docs/gemm/archive/ docs/gemm/bottleneck_card_samples/TEMPLATE.md \\\n  docs/platform/README.md docs/platform/cu13-stack.md \\\n  docs/prefill/README.md docs/prefill/current.md \\\n  docs/quant/README.md docs/quant/nvfp4.md\ngit status --short | head -40",
  "description": "stage all doc cleanup changes"
}
```

> TOOL

tool_result Bash
```
M  CLAUDE.md
M  demo-sala/preprocess_model.py
M  docs/README.md
M  docs/decode/README.md
M  docs/decode/current.md
M  docs/dflash/README.md
M  docs/dflash/current.md
M  docs/dflash/history.md
A  docs/eagle/300k-training-plan.md
M  docs/eagle/README.md
A  docs/eagle/archive/papers-full.md
D  docs/eagle/d7-tune-bench-20260511.md
D  docs/eagle/dflash.md
M  docs/eagle/papers.md
M  docs/eagle/training/history.md
M  docs/gemm/README.md
A  docs/gemm/archive/changelog-r1-r12prep.md
R  docs/gemm/bottleneck_cards/01_o_proj_std_M48.md -> docs/gemm/bottleneck_card_samples/01_o_proj_std_M48.md
R  docs/gemm/bottleneck_cards/02_down_proj_M128.md -> docs/gemm/bottleneck_card_samples/02_down_proj_M128.md
A  docs/gemm/bottleneck_card_samples/TEMPLATE.md
M  docs/gemm/changelog.md
M  docs/gemm/kernels-sm120.md
M  docs/gemm/marlin.md
M  docs/gemm/sol_table.md
M  docs/gemm/todo.md
M  docs/handover.md
M  docs/platform/README.md
M  docs/platform/cu13-stack.md
M  docs/prefill/README.md
M  docs/prefill/current.md
M  docs/quant/README.md
M  docs/quant/nvfp4.md
```

> TOOL

tool_use Bash
```json
{
  "command": "git commit -m \"$(cat <<'EOF'\ndocs: 大规模清理 — 删幻影/陈旧/重复，归档早期长文，事实修正\n\n事实修正：\n- NVFP4 校准 48K/128 → 90K/90（CLAUDE.md、quant/nvfp4.md、preprocess_model.py docstring 均与 demo-sala/preprocess_model.py:33-34 实际常量对齐）\n- b12x 默认 OFF 表述对齐：kernel 已 lock-in（R-b12x bit-exact + S8 +28.5%），但提交包 SGLANG_ENABLE_B12X=0；同步到 CLAUDE.md / decode/current.md / gemm/marlin.md / gemm/kernels-sm120.md\n- probe-sala/ 整目录已退役（commit b74c10d），剩 probe-sala-s2/ 反向 SSH sidecar；CLAUDE.md、handover、cu13-stack §4 同步\n\n删除 / 合并：\n- docs/eagle/dflash.md（已自 deprecate）→ §1-§8 精炼并入 dflash/history.md §2\n- docs/eagle/d7-tune-bench-20260511.md → 并入 eagle/training/history.md\n- 全仓 .ipynb_checkpoints/（9 个，gitignored 但未追踪）\n\n归档（保留全文，迁出主目录）：\n- docs/eagle/papers.md（809→111 行，保留 MARS 实装 + 索引）；完整版 → archive/papers-full.md\n- docs/gemm/changelog.md（1338→450，保留 R-b12x 及以后活跃 round）；R1~R12-prep → archive/changelog-r1-r12prep.md\n\n重写 / 精简：\n- docs/handover.md（190→97，指针式，去重 CLAUDE.md）\n- docs/gemm/todo.md（191→84，按 lock-in 状态 + ROI Tier 重组）\n\n索引 / 结构：\n- docs/prefill/current.md §5 + prefill/README.md：新增仓内 piecewise/、prefill/ 调研工作区索引（go/no-go 已锁）\n- docs/dflash/{current,history}.md：标注 best.pt 路径已删（dflash/outputs/ 不存在）\n- docs/gemm/bottleneck_cards/ → bottleneck_card_samples/ + TEMPLATE.md（明确\"仅样例，全集 54 张未补齐\"）\n- docs/eagle/README.md：补 300k-training-plan 索引；D7 调档指向 training/history\n- docs/README.md：快速定位表扩 b12x / NVFP4 校准 / 调研工作区 / best.pt 已删\n- 跨文件相对链接修复（quant/nvfp4 → ../gemm/marlin、archive/ 内部回指）\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\nEOF\n)\"",
  "description": "commit doc cleanup"
}
```

> TOOL

tool_result Bash
```
[main 0d3474f] docs: 大规模清理 — 删幻影/陈旧/重复，归档早期长文，事实修正
 32 files changed, 2447 insertions(+), 2398 deletions(-)
 create mode 100644 docs/eagle/300k-training-plan.md
 create mode 100644 docs/eagle/archive/papers-full.md
 delete mode 100644 docs/eagle/d7-tune-bench-20260511.md
 delete mode 100644 docs/eagle/dflash.md
 create mode 100644 docs/gemm/archive/changelog-r1-r12prep.md
 rename docs/gemm/{bottleneck_cards => bottleneck_card_samples}/01_o_proj_std_M48.md (100%)
 rename docs/gemm/{bottleneck_cards => bottleneck_card_samples}/02_down_proj_M128.md (100%)
 create mode 100644 docs/gemm/bottleneck_card_samples/TEMPLATE.md
```

> TOOL

tool_use Bash
```json
{
  "command": "git push origin main 2>&1 | tail -15",
  "description": "push to origin main"
}
```

> TOOL

tool_result Bash
```
To https://github.com/wzyfromhust/openbmb.git
   141fb6d..0d3474f  main -> main
```

> AGENT

提交并推送完成。

- commit `0d3474f`：32 文件，+2447 / -2398
- 推送到 `origin/main` 成功
