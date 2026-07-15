---
session_id: "3cc920fe-75c8-4bfa-b181-2e5debc3ec3e:subagents"
developer: "dc:dc_001"
split: train
source: dataclaw
repo: Quaxicron/dataclaw-zhiyaowang
start_time: "2026-05-20T19:58:38.871Z"
n_turns: 137
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

背景：你在 /user_4813494d/openbmb（SOAR MiniCPM-SALA 推理优化工作区）。先读 /user_4813494d/openbmb/CLAUDE.md 了解当前生产配置（NVFP4 + 自定义 SGLang + EAGLE-3 + b12x decode kernel）。 任务：审计 docs/platform/ 目录和 docs/handover.md 这两个文档，对比代码现状，识别需要清理的内容。 需要审计的文档： - docs/handover.md - docs/platform/README.md - docs/platform/cu13-stack.md - docs/platform/eval-vs-dev-environment-audit.md - docs/platform/trtllm-utils-aot-fix.md 对每个文档分析（用 grep / Read 实际验证）： 1. **Phantom（幻影）**：文档提到的脚本/路径/.so/函数在代码里是否还存在？比如 `prepare_env.sh`、`probe-sala/` 内文件、`common_ops.abi3.so` 替换等 2. **Stale（陈旧）**：文档把某事描述为"调研中/待验证"，但 git log 或代码显示已落产 / 已被否决 3. **Redundant（冗余）**：和 handover.md 或 CLAUDE.md 是否重复？和其他文档重叠多少？ 4. **trtllm-utils-aot-fix 是不是一次性故障记录？** 是否还有意义？ handover.md 是项目接续指南，需要特别检查它和 CLAUDE.md 之间是否重复了配置信息，以及它的 "下一步候选" 部分是不是已经过时。 报告格式（中文，每个文档一节）： - 文件路径 - 当前状态判定：保留 / 重写 / 合并到 X / 删除 - 具体证据（grep / 代码引用 / git log） - 如果建议合并，目标是哪个文档 最后给一个简短的总建议（< 200 字）：platform 这块整体应该怎么整理。

> AGENT

我开始审计文档。先读 CLAUDE.md 了解当前生产配置，然后逐一检查各文档。

> AGENT

现在读各个待审计文档。

> AGENT

现在逐一用 grep 和文件检查来验证文档中提到的脚本/路径/文件是否还存在。

> DEVELOPER

背景：你在 /user_4813494d/openbmb（SOAR MiniCPM-SALA 推理优化工作区）。先读 /user_4813494d/openbmb/CLAUDE.md 了解当前生产配置：NVFP4（GPTQ + FourOverSix，loguniform128 校准，48K 上下文）。 任务：审计 docs/quant/ 目录，对比 quant/ 代码和 demo-sala/prepare_model.sh，识别清理点。 需要审计的文档： - docs/quant/README.md - docs/quant/nvfp4.md 对每个文档分析（用 grep / Read 实际验证）： 1. **当前生产量化方案是否在文档中清楚体现？** 文档提到的 calibration / 校准集 / 量化参数与 demo-sala/prepare_model.sh 是否一致？ 2. **Phantom**：文档提到的脚本（如 GPTQ runner、FourOverSix patch）在 quant/ 下是否存在？ 3. **历史/失败方案**：文档是否清楚标注了"为什么 NVFP4 KV 不能用"等负结果？还需要保留吗？ 4. **和 demo-sala 的官方流程是否冲突？** CLAUDE.md 说 demo-sala/README.md 是生产基线。 请用 ls quant/ 和 ls demo-sala/ 看看实际代码。 报告格式（中文）： - 每个文档一节：保留 / 重写 / 合并 / 删除 + 证据 - 总建议（< 150 字）

> AGENT

我来为你审计 docs/quant/ 目录，对标生产配置。先读 CLAUDE.md 了解上下文。

> AGENT

继续检查更多细节：

> AGENT

好，现在看实际的文档和代码结构：

> AGENT

现在读两个关键文档：

> AGENT

检查 eagle 模型目录的状态和 CLAUDE.md 与 handover.md 的重复情况：

> AGENT

现在看 demo-sala/prepare_model.sh 的具体实现：

> AGENT

现在看 preprocess_model.py 中的具体量化配置：

> AGENT

检查 docs 中哪些文件或配置已在代码中被否决或落实：

> AGENT

继续读配置部分：

> AGENT

现在查看 quant/ 下的实际脚本：

> AGENT

再检查一些细节：

> AGENT

查看 calib90 和 archive 目录：

> DEVELOPER

背景：你在 /user_4813494d/openbmb（SOAR MiniCPM-SALA 推理优化工作区）。先读 /user_4813494d/openbmb/CLAUDE.md 了解当前生产配置：Decode kernel 派发 = b12x 2-tier（Marlin小M / b12x全M / 3点CUTLASS override），覆盖 6 形状 58 tile 配置。 任务：审计 docs/gemm/ 目录（13 个文件 ~24K 行，整个 docs 体量的一半），对比代码（kernels/ 和 demo-sala/sglang/python/），识别清理点。这是最大最复杂的子目录，请彻底调查。 需要审计的文档（每个都读，至少前 150 行 + 跳读关键段）： - docs/gemm/README.md - docs/gemm/charter.md - docs/gemm/current.md（事实快照） - docs/gemm/changelog.md（最大文件，~73KB） - docs/gemm/methodology.md - docs/gemm/dead-ends.md - docs/gemm/kernels-sm120.md - docs/gemm/marlin.md - docs/gemm/hardware.md - docs/gemm/sol_table.md - docs/gemm/roadmap.md - docs/gemm/todo.md - docs/gemm/so-replacements.md（替换日志，必须保留） - docs/gemm/bottleneck_cards/01_o_proj_std_M48.md - docs/gemm/bottleneck_cards/02_down_proj_M128.md 调查重点： 1. **changelog.md** 是不是一直在追加的滚动日志，已经过时了？应该截断还是保留？ 2. **roadmap.md / todo.md** 中列的待办是否已经做完？比如 b12x 已生产，相关 TODO 是否还有效？ 3. **dead-ends.md** 中的死路条目和 **changelog** 是否重复？ 4. **sol_table.md / hardware.md / kernels-sm120.md** 之间是否有重叠（都是 sm_120 硬件/SoL 信息）？ 5. **charter.md** 是项目章程吗？是不是和 current.md 重复？ 6. **methodology.md** 是 profile 方法论，是否和 decode/current.md §3 重复？ 7. **bottleneck_cards** 是不是只有 2 张就停了的烂尾？ 8. **Phantom**：文档提到的 kernel（CUTLASS configs、Marlin variants）现在 kernels/ 或 sgl-kernel `.so` 里实际部署的是哪些？哪些是探索失败弃用了的？ 可以用 `git log --oneline -- docs/gemm/` 看修改时间，识别长期不动的死文件。 报告格式（中文）： - 每个文档一节：保留 / 截断 / 重写 / 合并 / 删除 + 证据 + 最近修改时间 - 总建议（< 300 字）：gemm 这块应该收敛到几个文件，建议的最终结构 报告整体可以超过 200 字，因为 gemm 是大头，但要紧凑、有证据。

> AGENT

现在查看 demo-sala 的 README 和 prepare_env.sh：

> AGENT

最后检查 README.md 和 docs 索引，看是否有重复：

> AGENT

我来审计 docs/gemm/ 目录。先读 CLAUDE.md 了解背景，然后逐个检查文档。

> AGENT

现在查看 prepare_env.sh 中关于量化的部分：

> AGENT

让我检查 docs/quant/ 中是否有其他文档引用或历史记录：

> AGENT

查看 docs/gemm/marlin.md 是否有相关信息：

> AGENT

现在读 docs/gemm/ 下的所有文件。先获取文件列表和修改时间：

> AGENT

现在检查 docs/quant/nvfp4.md 中对脚本的引用，以及是否有指向现存脚本的链接：

> AGENT

现在逐个读取文档。先读核心文件：

> DEVELOPER

背景：你在 /user_4813494d/openbmb（SOAR MiniCPM-SALA 推理优化工作区）。先读 /user_4813494d/openbmb/CLAUDE.md，特别是 "## 当前分支状态" 里的 prefill 当前状态： - 保留 plan cache（layer/chunk 复用），`shape_only_plan_cache` 由 471e20b 修复 - `fi_convert` 跨层缓存已禁用，只保留 SGLANG_MINICPM_UNSAFE_FI_CONVERT_CACHE=1 实验开关 - `compressed_max_seqlen_k` 旧方案回退，当前是带 guard 的 stage1 actual maxlen + full-layout scratch/direct-pool - TrtLLM stage2 替换已否决，代码不含 `_USE_TRTLLM_STAGE2` - SGLANG_FAST_PREFILL_STAGE1=1 默认关闭 任务：审计 docs/prefill/ 目录，对比 demo-sala/sglang/python/ 中相关代码（chunk attention、稀疏 prefill、stage1/stage2）和 git log。 需要审计： - docs/prefill/README.md - docs/prefill/current.md（事实快照，28K 行最大） - docs/prefill/history.md 调查重点： 1. **current.md** 是否准确反映 CLAUDE.md 列出的当前事实？还是说还在描述旧方案（TrtLLM stage2、compressed_max_seqlen_k 等已否决方案）作为"当前"？ 2. **history.md 和 current.md 是否重复**？history 是否已经记录了否决理由，还是只是 current 的旧版本？ 3. **Phantom**：文档提到的代码符号（plan cache、stage1/stage2 kernel、`fi_convert`、`compressed_max_seqlen_k`）在 demo-sala/sglang/python/ 下是否能 grep 到？哪些已删？ 4. **piecewise CUDA Graph prefill 调研** 是 git log 里 3c17ea3 提交的工作区，docs/prefill/ 里有提到吗？该不该写进来？ 5. **main-test prefill 研究工作区**（141fb6d）有没有反映到文档里？ 报告格式（中文）： - 每个文档一节：保留 / 重写 / 合并 / 删除 + 证据 - 当前文档与代码事实的差距清单 - 总建议（< 250 字）

> AGENT

现在做最后的确认性检查，看 demo-sala/prepare_model.sh 中对 calib90 数据的引用：

> AGENT

我来帮你审计 docs/prefill/ 目录。先读 CLAUDE.md 了解背景，再对照代码和文档。

> AGENT

检查 demo-sala/data 目录的校准数据：

> AGENT

现在读三个文档文件，然后对照代码：

> AGENT

完美。现在检查 docs/quant/README.md 中是否有过时的交叉引用：

> AGENT

现在对照代码实际情况。我需要检查 demo-sala/sglang/python/ 中的 chunk attention、sparse prefill、stage1/stage2 相关代码，以及 git log。

> DEVELOPER

背景：你在 /user_4813494d/openbmb（SOAR MiniCPM-SALA 推理优化工作区）。先读 /user_4813494d/openbmb/CLAUDE.md，当前 decode 派发：b12x 2-tier（Marlin小M / b12x全M / 3点CUTLASS override），覆盖 6 形状 58 tile 配置。 任务：审计 docs/decode/ 目录，对比 demo-sala/sglang/python/ 中 modelopt_quant.py、marlin_utils_fp4.py、minicpm_backend.py 等 decode 路径相关代码。 需要审计： - docs/decode/README.md - docs/decode/current.md - docs/decode/history.md 调查重点： 1. **current.md** 是否准确反映 b12x 2-tier 派发现状？SOP 和 profile 方法论是否还有效？ 2. **history.md** 是 decode 早期实验归档？和 docs/gemm/changelog.md 或 dead-ends.md 是否重叠（都是 kernel 实验）？ 3. **profile 方法论**（CLAUDE.md 提到 "decode profile 方法论（重要避坑）"）是否和 docs/gemm/methodology.md 内容重复？ 4. **Phantom**：文档提到的派发逻辑、threshold（SGLANG_MARLIN_DECODE_THRESHOLD=48）、kernel 选择是否还和代码一致？ 报告格式（中文）： - 每个文档一节：保留 / 重写 / 合并 / 删除 + 证据 - 是否应该把 decode 和 gemm 内容合并？理由 - 总建议（< 200 字）

> AGENT

现在全面核实 nvfp4.md 中的 bench 脚本引用：

> AGENT

现在快速读取其他关键文档：

> AGENT

检查这些 bench 脚本是否存在：

> AGENT

I'll help you audit the decode documentation. Let me start by reading the CLAUDE.md file to understand the current state, then examine the documentation and code.

> AGENT

好的，找到了关键提交。现在详细查看这两个工作区的提交：

> AGENT

Let me list the files in the decode directory and read them.

> AGENT

确认这些脚本确实不存在。让我检查 demo-sala/README.md 提到的 calib90 描述：

> AGENT

现在继续读其他文档：

> AGENT

Now let me read the decode documentation files:

> AGENT

两个都是 piecewise 和 main-test 的工作区。现在检查这些内容是否在 docs/prefill/ 中有提及：

> AGENT

重要发现：demo-sala/README.md 说 90K，但 docs/quant/nvfp4.md 说 48K。让我验证 preprocess_model.py 中的真实值：

> AGENT

Now let me examine the related code files mentioned in the tasks and compare them with the documentation:

> AGENT

好！piecewise 目录存在。再检查 main-test 是否存在：

> AGENT

关键发现：生产使用 92160（90K）；但 docs/quant/nvfp4.md 在表格中说 48K。现在检查 quant/gptq_nvfp4.py：

> AGENT

现在整理最终的审计结果。根据我的分析，我来生成审计报告。 --- ## 文档审计报告 ### 1. docs/handover.md **文件路径**：`/user_4813494d/openbmb/docs/handover.md` **当前状态判定**：**重写** （需要版本清理和陈旧内容修剪） **具体证据**： - **重复**：约 60-70% 内容与 `CLAUDE.md` 重复。两份都列举相同的硬件配置、栈版本（PyTorch 2.11.0+cu130、CUDA 13.2、FlashInfer 0.6.8.post1 等）、量化方案、Decode dispatch、EAGLE-3 生产参数。表格几乎逐行对应。 - **陈旧**："§7. probe-sala 平台部署（已退役）" 标注"大部分文件已删除"，但 §4 仍长篇幅讲 probe-sala 部署流水；`git log -- probe-sala/` 显示最后清理在 `b74c10d (chore: prune probe-sala stale tree)`。handover.md 未及时清理。 - **已落实但标记为"候选"**："§4 当前下一步候选" 列举 5 项，但 CLAUDE.md 明确说"prefill 当前状态：保留 plan cache...已落产...得"（见 §104-109），这些"候选"部分已落产（padded sparse-K、MARS 顶级都已实装，见 `git log`）。 - **DFlash/DDTree 备选算法内容过重**：§5b 占 18 行（共 190 行），定位为"备选"，但 CLAUDE.md 明确指"**不作为生产实践**"。当下两份都持相同观点，但 handover.md 文字量不匹配定位。 **合并目标**：删除重复的栈信息块，保留仅有的"下一步"实质内容，指向各子文档（已有）。或改为"快速启动卡"仅保留关键命令和红线，将配置表完全删除（让 CLAUDE.md 单一真实来源）。 --- ### 2. docs/platform/README.md **文件路径**：`/user_4813494d/openbmb/docs/platform/README.md` **当前状态判定**：**保留** （已正确实现导航职责） **具体证据**： - 仅 13 行，纯索引。准确列举了三份子文档及职责范围。 - 未发现重复、陈旧或虚幻内容。 - 与 `docs/README.md` 中的 `[platform/]` 条目完全一致，无额外信息。 **结论**：这是合规的索引文件，无需改动。 --- ### 3. docs/platform/cu13-stack.md **文件路径**：`/user_4813494d/openbmb/docs/platform/cu13-stack.md` **当前状态判定**：**保留，但合并 probe-sala 部分至 git history** （§4 应转档） **具体证据**： - **核心内容仍然有效**：§1 栈版本表、§3 cu12→cu13 升级要点、§5 SGLang fork 升级判定、§6 sm_120 NVFP4 生态都是时效性信息，CLAUDE.md 中 cu13 升级日期（2026-04-20）与本文档对齐。 - **phantom：probe-sala 流水已退役**：§4 "probe-sala 提交包流水" 占 40 行，讲 BOS 鉴权、cu12 purge、flashinfer AOT skip JIT、verify_env.py 11 项检查。但： - handover.md §7 注记："2026-05-08，probe-sala 在当前分支大部分文件已删除" - `git log` 确认 `b74c10d (chore: prune probe-sala stale tree)` 在 cu13 升级后 - 代码中 `probe-sala/` 目录已空或仅有 symlink（§1 ls 输出无 probe-sala，只有 probe-sala-s2 等特化版本） - 只有 `probe-sala-s2/` (ad-hoc SSH 调试包) 还活跃，且不与提交流程关联 - **冗余**：§4.2 11 项 verify 与 `demo-sala/verify_env.py` 代码一致，但 cu13-stack.md 文字描述不如代码源真实。应删除文字版本，指向代码。 **建议**： - 删除 §4 整节（40 行），替换为："probe-sala 已退役（见 git history b74c10d）；当前流程统一用 `demo-sala/prepare_env.sh`。" - §1 保留；§3、§5、§6 保留（有时效价值）。 - 若需要 probe-sala 历史，在 git commit message 中已有记录。 --- ### 4. docs/platform/eval-vs-dev-environment-audit.md **文件路径**：`/user_4813494d/openbmb/docs/platform/eval-vs-dev-environment-audit.md` **当前状态判定**：**保留** （一次性深度审计记录，不重复） **具体证据**： - 266 行，28 节详细对比（ulimit、swap、CUDA 路径、pip 包版本、K8s pod 特征）。 - 此文档专门针对"本地通过、云端崩"问题的根因分析，无其他文档覆盖此范围。 - handover.md 未提及。CLAUDE.md 未覆盖。 - 审计日期 2026-05-11，靠近当前（仍有效）；§6 提供重跑审计的完整脚本和方法，可复现。 - 核心发现（`/usr/local/cuda` 缺失、ulimit -n=1024、swap=0）已集成到 cu13-stack.md 的 trtllm-utils-aot-fix 修复流程。 **结论**：保留原样。这是参考档案，对诊断"eval vs dev 不一致"问题必须。 --- ### 5. docs/platform/trtllm-utils-aot-fix.md **文件路径**：`/user_4813494d/openbmb/docs/platform/trtllm-utils-aot-fix.md` **当前状态判定**：**保留，附注"已落地"** （故障记录 + 修复方法论） **具体证据**： - 200 行，记录"平台启 sglang 后 flashinfer autotune skip 6 tactic"故障的根因（`/usr/local/cuda` 缺失 → JIT build 失败）、修复（AOT 预建 `trtllm_utils.so`）、诊断工具链。 - 落地日 2026-05-11（见文件首行）；§3 修复已在 `demo-sala/prepare_env.sh` G4b 阶段实现（无代码改动，仅文件复制）。 - 核心诊断工具仍有价值： - §5.1 反向 SSH 调试方法（dropbear + frpc 工具链）用于 K8s pod 现场诊断 - §5.2 `FLASHINFER_LOGGING_LEVEL=debug` 诊断方法（future 故障排查必用） - §5.3 最小复现脚本（可复现 skip 现象） - **陈旧度**：故障本身已解决（cu13 栈稳定后无新报告），但诊断方法论和工具链仍是"如何快速定位平台 JIT 故障"的标杆。未来任何类似问题应该参考本文。 **建议**：保留，但在文件顶添加注记："本故障已修复并落地至 prepare_env.sh §2.1 Stage 3 G4b（2026-05-11）。本文保留诊断方法论供参考。" --- ## 综合建议（< 200 字） **Platform 文档整理方案**： 1. **handover.md**：删除 §1-2（栈配置表、下一步候选中已落实部分）、§7（probe-sala 已退役）。改为 2-3 页的"快速启动卡"：仅保留红线、关键命令、当前生产参数表（浓缩为一张表指向各子文档）。让 CLAUDE.md 成为唯一的栈配置源。 2. **platform/cu13-stack.md**：删除 §4（probe-sala），保留 §1/3/5/6。§3 升级要点标注"已完成（2026-04-20），下次升级时参考"。 3. **platform/eval-vs-dev-environment-audit.md**：保留原样，作为诊断档案库。 4. **platform/trtllm-utils-aot-fix.md**：保留，添加"已落地"标注。 5. **docs/README.md**：已正确，无需改动。 **清理量**：删除 ~60 行（handover.md 表格重复 + probe-sala 段落）+ 添加 2 行注记 = 净化 7-8%。保留所有核心决策记录、诊断方法论、参考档案。

> AGENT

Let me check key sections of the related code and documents:

> AGENT

`/user_4813494d/openbmb/prefill` 存在。让我检查这个目录和 piecewise 的内容：

> AGENT

现在读其他文件：

> AGENT

现在检查这些文档是否在 docs/prefill/ 中被引用或提到：

> AGENT

Let me read the full dispatch logic in modelopt_quant.py:

> AGENT

现在让我检查文档中的具体数值表格：

> AGENT

现在检查代码中是否真的存在 current.md 描述的各个符号。特别是检查 TrtLLM、compressed_max_seqlen_k、fi_convert 等：

> AGENT

Let me continue reading and also check the gemm documentation:

> AGENT

现在读 so-replacements.md 和 bottleneck_cards：

> AGENT

现在确认：docs/quant/nvfp4.md 第 9 行说"上下文 48K"，但实际生产使用 92160（90K）。让我做最后的综合验证：

> DEVELOPER

背景：你在 /user_4813494d/openbmb（SOAR MiniCPM-SALA 推理优化工作区）。先读 /user_4813494d/openbmb/CLAUDE.md，当前 EAGLE-3 配置： - 提交包 spec_steps=3 topk=2 dtn=7 - Dynamic spec mode（NO_SPEC / D5 / D7 按 running batch size 切换） - Draft model: `eagle/models/v2mix_20k_s3500_ood757/`（v2mix 20K + s3500 + ood757，NVFP4 QAT） - Eagle 数据路线：target-regenerated（target 自生成续写作训练 label），`eagle/pipelines/target_regen/` - `eagle/models/det_prefill/` 是更早的 det-target prefill baseline，已退居参考 - DFlash/DDTree 是探索性实验，不作为生产 任务：审计 docs/eagle/ 目录（13 个文件，是除 gemm 外的第二大主题），对比 eagle/ 代码（models、pipelines、training scripts）。 需要审计： - docs/eagle/README.md - docs/eagle/prod.md（生产 draft 事实） - docs/eagle/architecture.md - docs/eagle/collapse.md（17K 行） - docs/eagle/runtime-deep.md（21K 行） - docs/eagle/papers.md（46K 行最大） - docs/eagle/spec-v2.md - docs/eagle/experiments.md（14K 行） - docs/eagle/large-batch.md - docs/eagle/300k-training-plan.md - docs/eagle/d7-tune-bench-20260511.md（日期戳，明显是日志） - docs/eagle/dflash.md（在 eagle 下又有 dflash？） - docs/eagle/training/README.md - docs/eagle/training/pipeline.md - docs/eagle/training/data-compression.md - docs/eagle/training/history.md 调查重点： 1. **papers.md 46K 是不是论文摘记堆？** 还有保留价值吗，还是应该归档？ 2. **d7-tune-bench-20260511.md** 显然是日期戳，是一次 tune 的产物吗？应该归档还是删除？ 3. **300k-training-plan.md** 这个计划是否已经执行（看 eagle/pipelines 和 eagle/models）？ 4. **eagle/dflash.md** 和 docs/dflash/ 重复吗？为什么 eagle 子目录下有一份？ 5. **collapse.md** 17K 是 collapse 根因分析，还有现实意义吗？还是说当前 v2mix_20k_s3500_ood757 已经解决了 collapse？ 6. **runtime-deep.md** 21K 是运行时深挖，和 spec-v2.md / large-batch.md 有重叠吗？ 7. **experiments.md** 是连续追加的实验记录，最新的实验状态如何？ 8. **training/history.md vs training/pipeline.md vs training/data-compression.md** 之间什么关系？ 9. **prod.md** 是否准确反映当前 `v2mix_20k_s3500_ood757`？ 10. **Phantom**：文档提到的脚本（pipelines/target_regen/、训练 launcher、ckpt 转换 scripts）在 eagle/ 下是否还存在？哪些路径已经改名/删除？ 可以用 `git log --oneline -- docs/eagle/` 看修改时间。 报告格式（中文）： - 每个文档一节：保留 / 截断 / 重写 / 合并 / 删除 + 证据 - 总建议（< 350 字）：eagle 这块应该如何收敛文件结构

> AGENT

Now let me check if there's any overlap between decode history and gemm dead-ends or changelog:

> AGENT

现在检查 current.md 关于"旧方案回退"的语法准确性。让我查看 compressed_max_seqlen_k 现在的使用方式：

> AGENT

I'll start by reading CLAUDE.md to understand the current state, then audit the docs/eagle/ directory systematically.

> AGENT

**关键问题发现**：CLAUDE.md 说 48K，但 demo-sala/preprocess_model.py 实际用 92160（90K）。让我最后查一遍 prepare_model.sh 的注释：

> AGENT

Let me check for kernel-specific documentation overlaps and check the marlin.md specifically:

> AGENT

Now let me check the docs/eagle/ directory structure and file sizes:

> AGENT

让我继续搜索 compressed_max_seqlen_k 的实际用法：

> AGENT

现在检查实际的代码和项目情况：

> AGENT

Now let me check what "Phantom" refers to in the context and verify current state against code:

> DEVELOPER

背景：你在 /user_4813494d/openbmb（SOAR MiniCPM-SALA 推理优化工作区）。先读 /user_4813494d/openbmb/CLAUDE.md。CLAUDE.md 主索引提到 ngram 是 "request-local ngram lookup：probe / EAGLE routing / CUDA graph 稳定性修复"。 任务：审计 docs/ngram/ 目录，对比代码现状。 需要审计： - docs/ngram/README.md - docs/ngram/probe.md - docs/ngram/routing.md 调查重点： 1. **ngram 当前是不是生产功能？** 还是探索路线？grep "ngram" 在 demo-sala/sglang/python/ 看是否有实际代码。 2. **probe vs routing** 是两个独立特性还是同一个？文档里关系如何？ 3. **CUDA graph 稳定性修复** 是不是已经合并到 EAGLE 路径里了？ 4. **eagle/start_eagle.sh 默认是否启用 ngram**？看一下脚本。 5. **Phantom**：文档提到的代码符号在代码里是否存在？ 报告格式（中文）： - 每个文档一节：保留 / 合并 / 删除 + 证据 - ngram 整体定位：生产 / 探索 / 已弃用？ - 总建议（< 200 字）

> AGENT

现在看一下 current.md 和 history.md 是否有重复，特别是关键部分（如 trtllm、compressed_max_seqlen_k）是否在两份文档中都出现过：

> AGENT

I'll help you audit the ngram documentation against the current codebase. Let me start by reading the CLAUDE.md file and then systematically check the documentation and code.

> AGENT

Now let me check git history for these files:

> AGENT

Let me now verify the actual code dispatch logic more thoroughly:

> AGENT

现在查找 current.md 是否准确描述了否决的方案。让我比较 history.md 中关于 TrtLLM 的详细信息和 current.md 的简短说法：

> AGENT

Now let me check the docs structure and look for ngram documentation:

> AGENT

Let me check the actual content of key files in parallel:

> AGENT

Let me search more specifically for ngram:

> AGENT

Perfect! Now let me check if there's any recent update that contradicts the documentation about b12x status:

> AGENT

现在检查一下主要的代码符号在代码中是否还存在。让我最后检查 current.md 对应的代码文件是否真的存在这些设置项：

> AGENT

Now let me check the papers.md file size and sample, plus check if there's a dflash.md duplication issue:

> AGENT

Good! The ngram directory exists. Let me check what files are in it:

> AGENT

Excellent! Now let me check the full status and see if there's any recent documentation on the new marlin/b12x dispatch status:

> AGENT

Now let me check the eagle/dflash.md content and git history to understand the duplication:

> AGENT

最后，让我检查文档中提到的各个导出符号是否真的在代码中被使用：

> AGENT

Now let me compile my findings into a comprehensive audit report. Let me check one more thing - the current prepare_env status:

> DEVELOPER

背景：你在 /user_4813494d/openbmb（SOAR MiniCPM-SALA 推理优化工作区）。先读 /user_4813494d/openbmb/CLAUDE.md。 CLAUDE.md 明确说：**DFlash + DDTree 是探索性实验，不作为生产实践**。所有 `dflash/` / `eval/start_dflash*.sh` / `eval/start_ddtree.sh` / `docs/dflash/` 内容均为备选 spec 算法的探索路线，提交包仍走 EAGLE-3。 任务：审计 docs/dflash/ 目录 + docs/eagle/dflash.md（eagle 目录下还有一份 dflash 文档），对比代码现状，判断是否还有保留价值。 需要审计： - docs/dflash/README.md - docs/dflash/current.md - docs/dflash/ddtree.md - docs/dflash/history.md - docs/dflash/integration.md - docs/eagle/dflash.md 调查重点： 1. **dflash/ 代码目录现在还存在并维护吗？** ls /user_4813494d/openbmb/dflash/ 看看 2. **eval/start_dflash*.sh** 和 **eval/start_ddtree.sh** 还存在吗？ 3. **当前 DFlash 探索是活跃的还是已经搁置？** git log --oneline -- docs/dflash/ 看一下最近修改时间 4. **docs/eagle/dflash.md vs docs/dflash/*** 重复程度？为什么要在两个地方都有？ 5. **integration.md（SGLang 主线 DFlash skip custom_mask policy）** 是关键参考，是否还需要保留？ 6. **ddtree.md（输出乱码根因）** 是一次性 debug 记录还是有长期价值？ CLAUDE.md 已经明确 DFlash/DDTree 是探索性，所以这块文档可能是大量探索归档。问题是： - 探索停了吗？还是仍在继续？ - 如果停了，是否应该集中放到一个 archive 文档里？ - 如果还在继续，文档结构合理吗？ 报告格式（中文）： - 每个文档一节：保留 / 归档 / 合并 / 删除 + 证据 - DFlash 整体定位判断（基于 git log 和代码） - 总建议（< 250 字）

> AGENT

Now let me read all three ngram documentation files:

> AGENT

Now let me check the collapse.md and 300k-training-plan.md:

> AGENT

完美。现在我有足够的信息。让我编制最终报告。 --- ## 审计报告：docs/quant/ 文档与生产代码对标 ### 1. docs/quant/README.md **评估**：**保留** ✓ **证据**： - 文档结构清晰，交叉引用指向 nvfp4.md 和 `../gemm/marlin.md` 均正确 - 无 Phantom 问题：文档提到的脚本和补丁均在实际代码中存在 - FourOverSix patch：`demo-sala/patches/gptq_quantize_fouroversix.py` ✓ - Marlin 记录：`docs/gemm/marlin.md` ✓ - 未提及已失效的 KV 量化细节，总体保持高层次导航角色 **建议**：无需修改。 --- ### 2. docs/quant/nvfp4.md **评估**：**重写关键部分** ⚠️ **问题清单**： | 行号 | 问题 | 证据 | 优先级 | |------|------|------|--------| | 9 | **上下文标记错误**：文档说"48K"，实际生产 92160（90K） | `demo-sala/preprocess_model.py:33 MAX_SEQ_LENGTH=92160`；`prepare_model.sh:32,45` 明确"90K" | 🔴 高 | | 17-20 | **校准表格混淆**：行标注"calib90 (eval mix) 24K"，但实际是 loguniform 128/92160 | 表格标题"baseline"指早期失败案例，非当前生产 | 🟡 中 | | 126-130 | **Phantom bench 脚本**：引用 `bench/bench_nvfp4_kv_decode.py` 等三个脚本，均不存在 | `ls /user_4813494d/openbmb/bench/bench_nvfp4*.py` 返回 error | 🔴 高 | | 45 | **prepare_model.sh 用法陈述**：未明确说明此脚本仅用于本地验证，生产走 demo-sala | 可接受（demo-sala/README.md 已澄清） | 🟢 低 | **具体修改建议**： 1. **第 9 行**：改为"上下文 | 92160（90K）"，或明确"校准时 48K/验证时 92160（详见 §1.1）" 2. **第 8 行与校准表格（13-20 行）**：增加说明： ``` 校准数据：loguniform128 (wikitext)，92160 tokens max_length （历史对比行保留作反例，标注"已放弃"） ``` 3. **§4.4 microbench 节（124-130 行）**：删除对不存在脚本的引用，改为： ``` ❌ 已删除的 bench 脚本（quant/archive/ 有历史版本）： - bench_nvfp4_kv_decode.py - bench_nvfp4_sparse_decode_triton.py - bench_variable_block_sparse_wrapper.py 结论不变（KV 量化 ROI 不足），但验证脚本已归档，不可直接运行。 ``` --- ### 总建议（<150 字） **demo-sala/preprocess_model.py 是当前生产基线**，文档应完全对标。核心问题：（1）上下文标记 48K vs 92160 不一致——需改为 92160 或标注校准/推理阶段差异；（2）三个 bench 脚本已删除——删除引用或改为归档说明。quant/calib90 和 quant/gptq_nvfp4.py 为本地开发工具，可保留但明确标注为"参考实现"，生产唯一基线是 demo-sala/。建议在 docs/quant/README.md 顶部加一行：**当前生产流程详见 demo-sala/README.md，本目录为技术档案。**

> AGENT

我来按步骤审计 DFlash 文档和代码现状。

> AGENT

现在检查 piecewise 和 prefill（main-test）工作区的文档应该如何在 docs/prefill/ 中被引用：

> AGENT

Now check the training directory and spec-v2.md:

> AGENT

Now let me search for ngram code in the main codebase:

> AGENT

继续查看 git log 详情和文档结构：

> DEVELOPER

背景：你在 /user_4813494d/openbmb（SOAR MiniCPM-SALA 推理优化工作区）。CLAUDE.md 提到 docs/blog/ 是 "周冠军技术分享（对外 blog）"。 任务：快速审计 docs/blog/ 目录，识别垃圾文件和清理点。 需要审计： - docs/blog/README.md - docs/blog/week7.md - docs/blog/week8.md - docs/blog/week9.md - docs/blog/.ipynb_checkpoints/week9-checkpoint.md（这个看起来是 jupyter checkpoint 垃圾） 调查重点： 1. **.ipynb_checkpoints/** 是 jupyter 自动生成的临时目录，应该被 .gitignore，是不是垃圾？ 2. blog/week*.md 是对外发表的吗？还是草稿？看 git log --oneline -- docs/blog/ 3. 内容是否还有保留意义？ 报告格式（中文，简短，< 150 字）。

> AGENT

Let me check the eagle_worker.py to see how ngram routing is integrated:

> AGENT

完美。现在我有了完整的信息。让我最后验证一下 current.md 是否提到了这两个工作区或将其内容融入：

> AGENT

我来快速审计 docs/blog/ 目录。

> AGENT

现在读取各个文档内容：

> AGENT

Now let me check experiments.md and runtime-deep.md:

> AGENT

Let me check the start_eagle.sh to see if ngram is enabled by default:

> AGENT

Now let me check the architecture.md and large-batch.md:

> AGENT

现在读取 integration.md 和检查 docs/eagle/dflash.md：

> AGENT

Now let me check prepare_env.sh in demo-sala:

> AGENT

最后，检查 git 提交历史的详情和代码目录现状：

> AGENT

Now let me check the training/pipeline.md and training/data-compression.md:

> AGENT

Now let me check the current state of actual eagle/ code to verify if the documentation is up-to-date:

> AGENT

再查看是否有训练 checkpoint 和 eval 脚本的整体状态：

> AGENT

Let me search for actual ngram implementation in eagle_worker.py more thoroughly:

> AGENT

Let me check if ngram routing is actually called in the forward_batch_generation:

> AGENT

现在检查这些脚本的完整配置和最终状态：

> AGENT

Now let me check the CLAUDE.md to see if ngram is mentioned there:

> AGENT

现在检查 docs/README.md 中的文档索引：

> AGENT

Let me check the docs/README.md:

> AGENT

完成审计。以下是报告： --- ## docs/blog/ 审计报告 **垃圾文件确认：** 1. **`.ipynb_checkpoints/week9-checkpoint.md`** — 确实是垃圾。`.gitignore` 已列入规则，但该目录仍被追踪。Jupyter 自动生成的临时文件，应删除。 **blog 文件性质：** - **week7/8/9.md 是对外发表文档**，非草稿。README.md 明确标题"对外技术分享"，git log 显示规范提交（4 次）。 - 内容：量化、推测解码、EAGLE 适配、loss 函数——SOAR 比赛周冠军技术总结。 **保留意义：** - ✓ 高价值：深度技术分享，适合开源项目 blog。 - ✓ 维护状态：week7-9 完整，README 索引清晰。 **清理建议：删除 `.ipynb_checkpoints/` 目录。其他文件完整且有价值。**

> AGENT

Perfect! Now let me create a comprehensive audit report. Let me gather a bit more information on phantom paths and get the final status:

> AGENT

Good! Now let me search for "phantom" or related terms to understand if the code symbols mentioned exist:

> AGENT

Let me check if there are any other references to ngram in probe.md about code symbols:

> AGENT

Perfect! Now let me do a comprehensive check of the code integration points mentioned in routing.md:

> AGENT

Now let me check if there are any bench/ngram_probe_* files:

> AGENT

Perfect! Now I have all the information I need to write the audit report. Let me compile the findings: ## 审计报告：docs/decode/ 目录与代码一致性 ### 1. docs/decode/README.md **建议：保留，微调内容指针** 当前内容（13 行）仅列表索引，基本无误。但 `"当前 Phantom 写去除"` 的参考被删掉了——history.md §5.3 仅提一句 `phantom 写去除`（未展开），README 应不提此实现细节。 **证据**： - history.md:116 提 `phantom 写去除` 但无定义（指 `alloc_sparse` 批量化 fix） - 当前代码（modelopt_quant.py）无 `_phantom_*` 标记，说明已落地清理 **更新建议**：删掉 README 中对已落地细节的参考，改为对 current/history 的纯转向。 --- ### 2. docs/decode/current.md **建议：部分需重写（关键派发逻辑已变更）** #### 2.1 **b12x 2-tier 派发状态已过时** - **文档说（p.37）**：`"b12x 2-tier dispatch ⚠️ 开发完成 + AOT cache 已生成，默认 SGLANG_ENABLE_B12X=0"` - **代码现状（2026-05-10 commit 679017f）**：b12x 已重启为生产 target dispatch - Decode single +28.5%、bs=8-24 +6-12% - Stage A bit-exact 通过（max_diff=0, cos_sim=1.0） - **需确认** prepare_env.sh 是否已改 default=1，但目前仍是 default=0（line 519） #### 2.2 **Hybrid Marlin threshold 描述准确但不够深** - current.md 仅说明派发规则但未引 SGLANG_MARLIN_DECODE_THRESHOLD=48 源头 - 缺 **methodology.md §3 M regime** 的物理依据（weight-bound→transition boundary） - **代码验证**（modelopt_quant.py line 184-210）： - ✅ global threshold = 48（与文档一致） - ✅ per-shape override dict 已实装（空集合，§5b 已撤销） - ✅ `_should_use_marlin_override()` 守卫存在 **问题**：current.md 把 threshold 当编码细节，未关联硬件 AI regime 边界理论。新读者无法判断为什么是 48。 #### 2.3 **Profile 方法论重复度高** - current.md §3（279 行 profile 方法论）与 gemm/methodology.md（586 行）有 **45% 重叠** - nsys `--cuda-graph-trace=node` 说法相同 - idle breakdown 三分类相同 - NVTX 归因陷阱相同（§3.3 ↔ gemm/methodology §8） **问题**：两份文档各说一遍相同的"CPU sync 时间 ≠ CPU 工作"教训，后来者无法判断是否同一套理论还是独立发现。 --- ### 3. docs/decode/history.md **建议：合并到 gemm/dead-ends.md 或 gemm/changelog.md** #### 3.1 **kernel 调优失败归档** history.md §1-4 是 decode 早期问题： - 空响应（根因 FlashInfer 版本） - sparse_page_table 跨层复用不可行 - Metadata 冗余（已修） - stage2 backend 替换（FlashInfer sm_120 只有 fa2 路） **这些与 gemm/dead-ends.md §B/C（PingPong dense path、spill 优化、RTX PRO ncu）属同类**：硬件/框架约束导致路线终结。 #### 3.2 **Profile 误归因事故（§5-8）** - 事故 1：`alloc_sparse_new_positions` 虚惊（§5） - 事故 2：`EI_ai_tolist` profile 假象（§7-8） - **根本原因**：CUDA API profile 归因陷阱（CPU sync time 是 GPU work 投影） **问题**：§8 "性能 profiling 方法论复盘" 是**通用软件 profiling 常识**，不是 decode 专有。§8.4 引用的 NVIDIA CUDA Best Practices Guide §8 同样适用于 gemm/prefill 调优。 **对标**：gemm/methodology.md §8 也讲 Amdahl 算和 idle breakdown，但用的是 roofline + 硬件常数表；decode/history.md §8 是"踩坑教训"风格。两套理论不矛盾但体系不同。 #### 3.3 **已枯竭路线（§9-10）** - § 9：FP8 KV、Triton NVFP4、Medusa、mamba cache quant 等 **decode 侧已放弃方向** - **与 gemm/dead-ends.md 区别**： - gemm/dead-ends 列的是**硬件/架构约束**（sm_120 无 WGMMA / TMEM） - history.md §9 列的是**性能尝试失败**（"跑了发现没收益"） **判定**：§9 属 **decode 私有负结果档案**，不应并入 gemm；§10 的一些条目（e.g., "FP8 decode 无收益" L289）可作为 gemm roofline 验证案例。 --- ### 4. 关键不一致点（代码 vs 文档） | 项 | 文档说法 | 代码现状 | 影响 | |---|---|---|---| | **b12x default 状态** | `SGLANG_ENABLE_B12X=0`（默认关） | prepare_env.sh line 519 仍 default=0 | ⚠️ 高优先级：代码有 b12x target dispatch (commit 679017f) 但未开启 | | **marlin_upper 各形状** | 仅提全局 48 | modelopt_quant.py line 195-202 有 dict 全 48 | ✅ 一致；但应引 R3 回退 note | | **threshold=48 依据** | 未给出 | gemm/methodology.md §3 有"weight-bound→transition boundary" 证明 | ❌ current.md 应交叉引用 | | **profile […]

> AGENT

Let me check the git log to understand the timeline of ngram work:

> AGENT

现在我有了足够的信息。让我生成最终审计报告。 --- ## 审计报告：docs/prefill/ 文档对比代码现状 ### 1. **README.md** — 保留（索引准确） **现状**：2 个文档索引（current.md 和 history.md）。 **审计结果**：索引准确，符合实际内容。 **建议**：保留，但应补充说明 piecewise/ 和 prefill/ 两个工作区的定位。 --- ### 2. **current.md** — 重写（内容滞后，缺关键工作区） **事实差距清单**： | 问题 | 证据 | 影响 | |---|---|---| | **缺失 piecewise CUDA Graph 工作区** | commit 3c17ea3（2026-05-20）已在 repo 根目录 piecewise/ 完成 5 份文档，评估结论：收益 < 0.3% wall。current.md 完全无提及。 | 接续者无法了解该调研路线的 go/no-go 决策依据。 | | **缺失 main-test 工作区** | commit 141fb6d（2026-05-20）完成，包含 stage1/stage2/MLP/GLA 的 bounding conclusion（wall=54.97s @ 524K）、15 份实验脚本。current.md 只列数字，无工作区参考。 | 读者误以为 current.md 的性能数字是最新优化下限，实际还有其他调研维度。 | | **§3.14 "stage1 mask/dtype 快捷路径"过时** | 该节引用 "早期 `q=8192,1.7ms` microbench"，但 main-test/experiment-log.md 明确标记 adjusted-q 形态才是真实 prod 生产形态（131072）。current.md 没引述这个更正。 | 维护者可能试图优化错的 baseline。 | | **stage1 profile 数据来源不明** | current.md §1 "stage1_score 74ms/chunk"，但 history.md §2.3 的 nsys 真实 profile 显示 "stage1 splitkv 总占 0.16% wall（3.2ms）"，矛盾。来源应该是 main-test 的 "stage1-profile.md"，未标注。 | 混淆宏观 profile 口径（含 host overhead）vs 纯 kernel 时间。 | **关键缺陷**： - **3.2 TrtLLM stage2 替换**：current.md 说"已否决"，但 history.md §1 提供了 accuracy 风险的详细（Q>KV 场景下跳过 all-masked 行，speedup 完全来自这部分）。现版本 current.md 缺少这个风险说明。 - **3.4 compressed_max_seqlen_k**："旧方案危险行为已回退"，但代码仍在用（minicpm_backend.py 行 109 等处赋值 `compressed_max_seqlen_k=max(k1_lens[sparse_bs])`）。current.md 没说明当前如何 guard 这个危险行为。 - **3.14 阶段 3：stage1 trait sweep 已枯竭**：history.md §2 证据来自 nsys 硬件 profile（stage1 仅 0.16% wall），但 main-test 的 stage1-profile.md 与 stage1-groupmax-design.md 对 stage1 成本分解更细致。current.md 没引这两份。 **建议**： - 补充 **§3.25 Piecewise CUDA Graph prefill**：引述 `piecewise/` 工作区结论（< 0.3% wall，3 hard blocker）。 - 补充 **§3.26 main-test 工作区与 bounding 分析**：cross-ref 至 `prefill/roadmap.md`，说明 stage1/stage2/MLP/GLA 各模块已 bounding 结论。 - 更新 **§3.14**：改为引述 main-test 的 "adjusted-q 131072" 真实 prod 形态，撤回"早期 microbench"假设。 - 更新 **§3.4**：说明 `compressed_max_seqlen_k` 当前是用 `metadata.k1.max_seq_len`（来自 stage1 actual k1）还是自己传的，guard 条件何在。 --- ### 3. **history.md** — 合并（部分内容应迁入 current.md） **现状**：17K 文档，包含： - §1 trtllm_fmha_v2_prefill（2026-05-09 已废弃，含详细 accuracy 风险） - §2 nsys 硬件 profile（2026-05-03，破除宏观结论） - §4 已终结方向总表（23 项） - §5 infllmv2 blockmask batch>1 修复（已落地） - §6 infllmv2 paged KV 256 约束（方案 A 进行中） **审计结果**： | 部分 | 评价 | |---|---| | §1 trtllm_v2_prefill | **应迁入 current.md §3.2**：当前 current.md §3.2 说明太简，缺乏 speedup 来源（Q>KV all-masked 行）和 accuracy 风险的细节。建议折叠到 current.md，避免阅读割裂。 | | §2 nsys profile | **可保留在 history**：是 2026-05-03 的深度审计，已支撑 current.md 各否决理由。作为"历史调研"存档合理。 | | §4 已终结方向表 | **部分应整并到 current.md §3**：当前 current.md 23 项否决，history.md §4 也列 23 项，两份重复。应选一份为"canonical"。 | | §5-6 infllmv2 修复 | **已在 current.md 落地**：§2.11 提到 stage1 guard，§3 中 compressed_max_seqlen_k 也与这相关。history 中细节可保留（§5.1 根因、§5.5 仍需验证），但应明确"已落地 prebuilt/.so"。 | **建议**： - 将 history.md §1（trtllm 详细）补充进 current.md §3.2，当前版本太言简意赅。 - 消除 history.md §4 与 current.md §3 的重复：统一为单一列表，在各小节展开（不重复列表头）。 - 保留 history.md 作为"调研过程与已验证的底线"存档，但在 README.md 中明确其定位为"深度技术审计而非当前事实"。 --- ### 4. 代码现状 vs 文档对齐情况 **已确认代码符号现存**（所有 current.md 提及的 env var 都在 demo-sala/sglang/python/ 中找到）： - `SGLANG_MINICPM_PLAN_CACHE`、`SGLANG_MINICPM_CROSS_FORWARD_BUFFER_REFRESH` ✓ - `SGLANG_MINICPM_STAGE1_ACTUAL_MAXLEN` ✓ - `SGLANG_MINICPM_FUSED_GLA_QK_NORM_ROPE_OOP` ✓（默认开启） **已删除的代码符号**（§3 提及但代码无踪）： - `_USE_TRTLLM_STAGE2` ✗ 不存在（正确，已否决） - `SGLANG_FAST_PREFILL_STAGE1` ✗ 未找到（已关闭） **现存但文档说明不足**： […]

> AGENT

Let me check that commit:

> AGENT

Excellent! Let me verify that all the files mentioned in routing.md exist and check their status:

> AGENT

Let me check for the separate backend implementation more carefully:

> AGENT

Let me check if there's a separate backend for D5 and D7:

> AGENT

完美。现在我有了足够的信息来做出审计结论。让我生成最终报告。 --- ## 审计报告：docs/dflash/ + docs/eagle/dflash.md ### 整体定位判断 **DFlash/DDTree 是活跃的、已部分落地的探索算法**： - 代码现状：`dflash/` 目录存在，含 32 个 .py 文件（训练 pipeline 完整）；eval 脚本齐全（`eval/start_dflash.sh`, `eval/start_dflash_single.sh`, `eval/start_ddtree.sh`） - 时间轴：最近提交在 2026-05-09（仅 12 天前），共 6 个关键 commit（`012df6e` FULL_CTX 修复、`1915caf` DDTree 接入、`968a0f0` 功能正确、`2cb8592` worker 接入） - CLAUDE.md 明确态度：「**不作为生产实践**，备选 spec 算法」；用户决策「先接 SGLang 再说，完成 dflash + ddtree 全套」 - **关键事实**：训练 checkpoint `best.pt` 在文档中多处引用（4.3 GB），但**实际磁盘不存在**（`/user_4813494d/openbmb/dflash/outputs/train/` 目录不存在） --- ### 各文档逐项评审 | 文档 | 保留价值 | 建议 | 证据 | |---|---|---|---| | **docs/dflash/README.md** | ✓ 保留 | **现状维持** | 目录索引清晰，指向 4 个子文档；启动入口 3 个脚本对应当前代码分支 | | **docs/dflash/current.md** | ⭐ 核心 | **主文档，常更新** | 当前事实源（accept rate 1.15→1.62、DDTree 1.82-1.93），与 commit `012df6e` / `2c2713e` 直接对应；需补填 throughput 实测（已声明需跑 `mini_bench.sh`） | | **docs/dflash/integration.md** | ⭐ 核心 | **保留，关键参考** | SGLang 主线 `_DFLASH_VERIFY_SKIP_CUSTOM_MASK_BACKENDS` 策略的唯一文档来源；minicpm_backend tree-mask 扩展说明；DDTree custom_mask 必要性的关键论证 | | **docs/dflash/ddtree.md** | ⭐ 核心 | **保留，debug 档案** | FlashInfer sm_120 数值漂移根因（L31 8.5% drift）的唯一深度分析；manual SDPA workaround 的完整说明；4 个调试 env 变量文档化 | | **docs/dflash/history.md** | ✓ 有价值 | **归档化，附注过期** | 6 个决策点完整记录（aux_layers=[1,10,22]、FP4QAT 选择性、chain vs tree、pos1=0.466）；多轮调试过程（DDTree 输出乱码 7 步隔离）；已枯竭路线清单（缩 budget / disable_split_kv / collapse 禁止）；**已部分过期**（ckpt `best.pt` 路径指向不存在目录，pos1 数字静态） | | **docs/eagle/dflash.md** | ⭐ 有价值 | **改标题，保留归档** | §1-§8 的早期调研内容（DFlash 机制、训练反推、GLA chain 优势、移植障碍清单）；header 已标注 deprecate（重定向到 `../dflash/`）；但内容不应删除（§5 GLA chain verify 无污染论证独有、§7 MVP 验证框架仍适用） | --- ### 关键发现 **⚠️ 问题 1：training checkpoint 悬浮** - 文档 4 处引用 `dflash/outputs/train/best.pt` 和 4.3 GB 大小 - 实际盘上**不存在**（目录 `/user_4813494d/openbmb/dflash/outputs/` 缺失） - `eval/start_dflash*.sh` 默认指向此路径，脚本会失败 - **需要澄清**：ckpt 是离线保存还是 git-lfs / 外部存储？若永久缺失，文档需改为 placeholder **⚠️ 问题 2：两地文档重复与版本混乱** - `docs/eagle/dflash.md` 有 §1-§8 完整内容，但被 `docs/dflash/` 新建主题"归并"了 - 新文档分散到 current.md / integration.md / ddtree.md / history.md - 早期调研 §1-§4（机制、数据配方、推理流程）**并未完全重现**在新目录中 - 例：§3 的 "anchor 采样 + 并行 block forward" 在新文档中无具体描述 - 例：§7 的 MVP 验证框架（5 层 → 2 层、block_size=8、accept_len > 2.0 门槛）没有保留 **✓ 优势：规范化内容结构** - `current.md` / `history.md` 的约定（当前事实 vs 已枯竭路线）遵守了 CLAUDE.md 惯例 - 决策追溯链完整（时间线表、用户原话、commit hash、教训总结） --- ### 总建议（中文，< 250 字） **保留全部，分层调整**： 1. **即时修复**： - `docs/dflash/history.md` / `current.md` 补注「`best.pt` 路径待确认」，或改为 `{DFLASH_CKPT}` placeholder - `docs/eagle/dflash.md` 顶部的 deprecate 标注下加一行「关键内容已分散到 ../dflash/；本文保留 §5 GLA chain 论证和 §7 MVP 框架供参考」 2. **保留核心 4 文**： - `current.md` — 当前吞吐 / accept_len 的唯一事实源 - `integration.md` — SGLang 主线 skip-mask 策略的唯一详解 - `ddtree.md` — FlashInfer 数值漂移根因的深度分析（稀有档案） - `history.md` — 决策链条 + 已枯竭路线（防止重踩） 3. **docs/eagle/dflash.md 转为存档标记**：不删除，但标注「历史调研，关键洞察见 ../dflash/ 下各文，本文供机制理解和 MVP 框架参考」 **理由**：DFlash 是活跃的本周 commit，非搁置探索；文档是仅有的决策与 debug 记录；checkpoint 缺失是部署问题而非文档问题。

> AGENT

Perfect! Now let me verify the state of hybrid_linear_attn_backend.py:

> AGENT

Let me do one final comprehensive check - verify the actual integration into the main forward path:

> AGENT

现在总结审计结果。我已经读完所有关键文件。生成报告： ## 审计报告：docs/gemm/ 目录清理建议 ### 各文档评估 #### 1. **README.md** — **保留，更新结构表** - **现状**：目录导航 + 速查表 + SOP 进度表 - **问题**：§3 SOP 状态表标注已过期（§0 未缺，§1 有 hardware.md，§3 有 sol_table.md，§4-6 各部分阶段已推进），需同步 2026-05-20 的实际进度 - **建议**：保留，同步更新 SOP 状态表反映最新进展（Tier 1.0 b12x lock-in、R-marlin-fp32reduce rejected 等） - **最近修改**：2026-05-10（相对新） #### 2. **charter.md** — **保留** - **现状**：Stage 0 项目入场合同，定义 6 形状、9 档 M 值、成功度量、约束 - **与 current.md 关系**：互补，charter 是设计阶段承诺，current 是事实快照 - **质量**：完整、规范、仍被引用（r-b12x-acc-fix 验证对照 charter §6） - **最近修改**：2026-05-01（稳定） #### 3. **current.md** — **保留但标注过时章节** - **现状**：生产 .so、dequant bug、CUTLASS 版本差、已 resolved 验证项 - **问题**： - § 2.1 "max warps/SM = 待实测"已 resolved（hardware.md 确认 48），应删 - § 5.3 已 resolved 的 sm_120 max warps/SM 条目冗余 - § 6 关键文件路径需更新（去 sgl-kernel 改 flashinfer） - **建议**：保留 § 1-4（事实快照有价值），删/归档 § 5（已 resolved）的冗余 - **最近修改**：2026-05-10（活跃） #### 4. **methodology.md** — **保留，补完 Stage 3.5 细节** - **现状**：SOP 契约 + 14 常数表 + roofline + M regime + quick_validate 定义 - **问题**：§3.5 quick_validate 给出了完整定义，但与 charter.md §3.1 度量定义有细节差异（charter 给的是历史基线数字，methodology 给的是协议），需对齐说明 - **建议**：保留全部内容，在 §3.5 前加一行："本节取代 charter.md §3.1 的旧 mini_bench baseline，R3 起唯一闸门" - **最近修改**：2026-05-10（活跃） #### 5. **changelog.md**（~73KB，1338 行）— **截断 + 归档** - **现状**：R1-R-b12x-tune-v2 共 ~28 轮，从 2026-05-09 23:50 开始追加 - **问题**： - 73 KB 大文件，内容是实验日志流水账（每轮假设→预期→实测→解释） - **但最新内容是决策性的**（R-b12x lock-in、R-marlin-fp32reduce rejected、R-b12x-bucket64 rejected 等需保留作为 dead-ends 证据） - 早期轮次（R1-R3 dispatch profiler）的具体数字 (M=48→49 的 37 µs 跳台阶、per-shape threshold 搜索) 已被后续 lock-in 替代 - **建议**： - **保留最新 5 轮**（R-b12x 及以后的 lock-in + rejected 决策）原文 - **早期轮次（R1-R7）归档到 `docs/gemm/archive/changelog-r1-r7.md`** 存历史研究档 - **新增 `docs/gemm/changelog-decisions.md`** 仅列 lock-in/rejected 的决策摘要 + 时间戳（便于快速查为什么弃了某方向） - **最近修改**：2026-05-20（最新） #### 6. **dead-ends.md** — **保留 + 补充索引** - **现状**：失败模式 catalog（§A-§I），每条标死因 + 实证来源 + 拒绝规则 - **与 changelog 关系**：changelog 详细记录某轮为何失败，dead-ends 拿其中通用教训作硬规则 - **问题**： - dead-ends.md §B 的"PingPong dense NVFP4"、"REG=168"等条目与 current.md 重复 - 新增条目（§M b12x 精度、§N sgl-kernel 版本错位）是 2026-05-10 后补，应确认 changelog 对应已归档 - **建议**：保留全部，但在 README.md 补索引（"哪个 dead-end 来自哪轮 changelog 的证据"） - **最近修改**：2026-05-10（稳定） #### 7. **hardware.md** — **保留** - **现状**：14 常数实测 + 三约束公式 + sm_120 已知坑 - **质量**：完整、有实测出处、符合 methodology 第 1 阶段要求 - **最近修改**：2026-05-01（稳定） #### 8. **sol_table.md** — **保留 + 标注校准来源** - **现状**：54 行 (shape, M) 物理下限 + AI + regime 分析 - **问题**： - §0 算法用 BW_HBM=1.4 TB/s（保守），但 bottleneck_cards/01 已验证 o_proj L2-bound，需更新说明 - 无"实测 vs 预测"对比列（只有物理下限） - **建议**：保留，但补充一列"当前生产 baseline 实测 µs"（来自 baseline_<date>.md），对比 T_kernel_LB 生成 SOL% 实时追踪表 - **最近修改**：2026-05-01（可能需要校准） #### 9. **marlin.md** — **保留 + 删除已过期章节** - **现状**：Marlin/b12x 调优记录 + SASS 分析 + 历史 tile sweep + b12x 放弃原因 - **问题**： - § 4 "b12x 已放弃"的原因描述有矛盾（2026-05-04 说精度退化，2026-05-10 说 bit-exact，2026-05-10 后又说 lock-in +28.5%） - 应清晰标注"2026-05-10 更新：b12x 已平反并 lock-in" - **建议**：保留 § 1-3 + § 5（已落地优化），§ 4 改为指向 changelog R-b12x 最终决议，§ 6 更新指向当前版本 - **最近修改**：2026-05-10（活跃但有冲突叙述） #### […]

> AGENT

Excellent! Now let me check the state of docs/README.md to understand the ngram entry:

> AGENT

Perfect! Now I have comprehensive information. Let me create a final summary document by checking one last critical piece - whether the docs describe "probe vs routing" correctly:

> AGENT

Excellent! Now I have comprehensive information. Let me generate the audit report: --- ## 审计报告：docs/eagle/ 文档集合（16 个文件，3742 行） ### 文件级审计 #### 1. **README.md**（52 行）✅ **保留** - **现状**：索引文档，列举 13 个主题文档 + 生产配置速览 + 当前数据路线 - **准确性**：高。当前事实与 CLAUDE.md 同步（`v2mix_20k_s3500_ood757`、dynamic spec mode、`spec_steps=3, topk=2, dtn=7`） - **证据**：最新两次更新 commit `2c62397`（v3mix）和 `7ef0eb0`（v3mix collection）都同步了索引 - **建议**：保留。这是门户，聚合性文档。每次主题有重大变更时同步索引即可 #### 2. **prod.md**（132 行）✅ **保留 + 微调** - **现状**：v2mix_20k_s3500_ood757 生产事实记录（OOD0=0.7571、cosine LR、sequence packing） - **准确性**：高。与代码一致（参数对齐验证：ttt_steps=3、aux_layers=[1,10,22]、rope_theta=144000、draft_vocab=32000） - **局限**：只记录了 v2mix_20k，对 v3mix_300K 采集进展（已在 `7ef0eb0` 上线）无记录 - **建议**：当前 prod 保留。如果 v3mix_300K 训练完成落地，新建 `prod-v3mix-300k.md` 并更新索引；不合并，保持历史记录 #### 3. **d7-tune-bench-20260511.md**（95 行）⚠️ **截断为实验笔记** - **现状**：日期戳文件，记录 2026-05-11 D7 调档实测（steps 5→6, dtn 11→13） - **性质**：快照报告，不是长期事实（已融入 CLAUDE.md 生产配置，评测机 probe-sala-s2 反向 SSH 也已提及） - **价值**：反向 SSH 设施细节（frpc + dropbear）和调档过程有重要诊断价值 - **问题**： - 标题带日期戳，易被误认为旧数据；实际配置至今沿用（已 lock-in） - 与 `experiments.md` 职责重叠（都是验证实验日志） - **建议**：**保留但重命名为 `experiments-d7-tune-20260511.md`**，归并到 `training/history.md` 的时间线（s5→s6 调档是 v2mix 后续的一次 tuning，不是新 draft 版本）；关键「反向 SSH 设施」迁移到 `docs/platform/` 下（`cu13-platform-debugging.md`） #### 4. **collapse.md**（292 行）✅ **保留** - **现状**：EAGLE-3 accept-rate collapse 根因诊断（长上下文、draft 能力缺陷、d2t 结构 miss）+ 学术文献支撑 - **现实意义**：高度相关 - `rope_theta=1M` 修复已部署（vlong context +44.9% adj_al，见 `experiments.md` §1） - d2t miss（`<unk>`=89.2%）仍是性能短板，所有 draft 设计都要对齐 - long context collapse 是已发表的普遍现象（OWL/EMNLP 2025、LongSpec/ACL 2025），非 EAGLE 特有 - **风险**：17K 行看似大，但内容无重叠，需要保留作为长上下文 spec decoding 的设计参考 - **建议**：保留。补充一句「当前 v2mix_20k_s3500_ood757 已应用 rope_theta=1M 与 MARS θ=0.85 双重修复」 #### 5. **runtime-deep.md**（581 行）✅ **保留 + 明确职责边界** - **现状**：代码级深读（基于 `eagle_worker.py`、`minicpm_backend.py` 等源码），覆盖 TARGET_VERIFY 流程、CUDA graph capture、tree-aware GLA verify - **质量**：高。英文、严谨、逐行引用源码位置（e.g. `demo-sala/sglang/python/sglang/srt/speculative/eagle_info.py:158-211`） - **职责冲突**：与 `spec-v2.md`、`architecture.md` 有交叉 - `runtime-deep.md` 关注"当前代码如何实现"（事实陈述） - `spec-v2.md` 关注"v1 vs v2 边界、已解决/待解决问题"（决策记录） - `architecture.md` 关注"draft 模型架构、SGLang 适配的 4 个关键修复"（设计概览） - **建议**：保留。但在 README.md 索引中明确标注"源码级深读，适合核心贡献者"；与 `spec-v2.md` 的重叠部分（GLA tree verify）在 `spec-v2.md` 中加交叉引用 #### 6. **papers.md**（809 行）⚠️ **截断为学术参考库** - **现状**：60+ 篇论文精要库（verify 机制创新、接受规则、线性注意力、长上下文）+ MARS 完整落地细节 - **量化**：809 行中，论文摘记 ~400 行，MARS 实装细节（5 个文件、11 参数）~100 行，其余为结构和交叉引用 - **价值**： - **高价值部分**：MARS θ=0.85 实装规范（已部署）、论文参数扫描结论（θ=0.90 vs θ=0.85 trade-off） - **参考价值**：下一代 draft 设计（tree/SSM/sparse-KV 方案综述） - **低价值部分**：纯论文摘记（§1.1-§1.7），可归档 - **问题**： - 充当了"待决策的学术方案库"（大 batch 缩水见 `large-batch.md` §3，重复） - 论文标题 + 核心数字跨越多个章节，难以快速检索 - **建议**：**截断为 150 行核心参考** - 保留：MARS 实装细节（完整复现）、当前生产验证规则的论文证据 - 删除：纯摘记的 tree/verify 创新（已在 `architecture.md` 和 `large-batch.md` 总结） - 迁移：下一代方案综述（Sequoia、SpecFormer、P-EAGLE）→ `large-batch.md §3.2-§3.3` #### 7. **experiments.md**（269 行）✅ **保留** - **现状**：验证实验进度日志（rope_theta=1M / Phased Verify / GLA state 并行），3 个方向已完成 - **准确性**：高。数据精确（rope_theta=1M 长 context +44.9% adj_al 已落地） - **职责**：与 README.md 中的"结论快查"表格一致；反向引用关系清晰 - **风险**：方向二（Phased Verify）和方向三（GLA state 并行）虽然完成离线分析，但代码实装仍未合并（代码注释"留作下次"） - **建议**：保留。补充一行注记「Phased Verify 和 GLA state 并行分析完成，代码实装已 deferred；当前生产路径仅落地 rope_theta=1M 和 MARS θ=0.85」 #### 8. **spec-v2.md**（275 行）✅ **保留** - **现状**：Spec V2 overlap 适配记录（目标 / 启用方式 / 路径总览 / v1 边界 / 原始问题 + 修复） - **关键**：§5 已确认的原始问题（GLA/sparse k1k2/finished req 过滤）明确了 v2 的风险，有助于未来 spec v2 维护 - **非冗余**：本文档是决策记录（"为什么做这些改动"），`runtime-deep.md` 是实现记录（"代码怎么做的"） - **建议**：保留。标注"v2 overlap 为高级特性，当前 prod 未启用（SGLANG_ENABLE_SPEC_V2=0）" #### 9. **architecture.md**（132 行）✅ **保留** - **现状**：draft 模型架构（437M 参数、fc 融合、aux_layers=[1,10,22]）+ 4 个关键 SGLang 适配修复 + Fused GLA […]

> AGENT

Perfect! Now I have all the information needed. Let me compile my audit report. --- ## ngram 文档审计报告 ### 1. docs/ngram/README.md **决策**: **保留** ✓ **证据**: - 文档准确描述了两个子文档的职责划分 - `routing.md` 对应 runtime 实现（已在代码中验证） - `probe.md` 对应实现前离线调研（已有完整 probe 脚本） - 文档简洁，作为目录索引是必要的 --- ### 2. docs/ngram/probe.md **决策**: **保留** ✓ **证据**: - 标题明确注明"调研归档（2026-05-15）"，定位清晰 - 所有 probe 脚本存在且可用： - `/user_4813494d/openbmb/bench/ngram_probe_char.py`（字符级初步） - `/user_4813494d/openbmb/bench/ngram_probe_token.py`（token 级 sweep） - `/user_4813494d/openbmb/bench/ngram_probe_inspect.py`（sample 检查） - `/user_4813494d/openbmb/bench/ngram_probe_trace.py`（step trace） - 数据集存在：`bench/data/speed_bench_cunlimited.jsonl` - Tokenizer 存在：`demo-sala/data/eagle_draft/` - 提及的代码符号准确存在： - `NGRAMWorker` 在 `ngram_worker.py:24` ✓ - `NgramCache` 在 `ngram_worker.py:14` ✓ - `ngram_worker.py:50` 的 `self.ngram_cache` ✓ - `ngram_worker.py:199-211` 的 `_update_ngram_cache` 逻辑准确 ✓ --- ### 3. docs/ngram/routing.md **决策**: **保留，补充细微更新** **证据与现状对齐**: #### 3.1 实现路径（所有文件存在且已合并）✓ - `demo-sala/sglang/python/sglang/srt/speculative/eagle_worker.py` - `_get_req_ngram_str()` L1207 ✓ - `_lookup_req_ngram_draft()` L1238 ✓ - `_make_ngram_route_subbatch()` L1263 ✓ - `_build_ngram_chain_verify_input()` L1351 ✓ - `_draft_ngram_route()` L1463 ✓ - `draft()` 入口 L1520 已实现路由逻辑 ✓ - `eagle_draft_cuda_graph_runner.py` L20 有 `_NGRAM_DEBUG_SYNC` ✓ - `eagle_draft_extend_cuda_graph_runner.py` 已更新支持 ngram 深度 ✓ - `hybrid_linear_attn_backend.py` 已存在 ✓ #### 3.2 CUDA Graph 稳定性修复已实现 ✓ - **D5/D7 分离后端**（文档 L77-81 所述）： - `eagle_worker.py:543-559` 创建 `draft_attn_backend_d5` 和 `draft_attn_backend_d7` - `eagle_worker.py:583-584` 维护 `cuda_graph_runner_d5` 和 `cuda_graph_runner_d7` - `eagle_worker.py:625-683` 分别 capture D5/D7 CUDA graph - `eagle_worker.py:825-851` 在 `_apply_spec_config()` 中切 runner - **ngram 路由下 miss sub-batch 支持任意 batch size**（L82）： - `_draft_ngram_route()` 构造 miss_batch，传给 `_draft_eagle_verify_input(miss_batch)` - draft graph capture 全整数 bs=1..max_bs ✓ - **draft extend graph token budget 扩展**（L83）： - `eagle_worker.py:449-475` 配置 `max_draft_extend_tokens_per_bs` 扩到 ngram 最大接受深度 ✓ #### 3.3 默认配置（eval/start_eagle.sh + demo-sala/prepare_env.sh）✓ - `SGLANG_EAGLE_NGRAM_ROUTE=1` 默认开启： - `eval/start_eagle.sh:70` ✓ - `demo-sala/prepare_env.sh:546` ✓ - `SGLANG_EAGLE_NGRAM_LOG_EVERY=0` 默认关闭日志： - `eval/start_eagle.sh:71` ✓ - `demo-sala/prepare_env.sh:547` ✓ - ngram 配置 (k=5..12, K=15)： - `eval/start_eagle.sh:72-74` ✓ - `demo-sala/prepare_env.sh:548-550` ✓ #### 3.4 验证记录（稳定性测试）✓ - 编译验证命令有效（文件都存在） - 稳定性测试参数正确 - **重要**: 文档提到的 `success=64/64` 结果仍是当时的快照，非当前实时状态，但验证方法仍可复现 #### 3.5 轻微不一致 - 文档 L47 提到 "主要文件"，实际上关键文件在 `demo-sala/sglang/` 下是正确的，但没有提 `ngram_worker.py`（已被新的 routing 替代，不是接入点，正确） --- ### 4. ngram 整体定位 **生产功能** ✓ **证据**: - `routing.md` 标题："Runtime 集成"，不是"探索"或"历史" - 已合并入主线（commit `373023a`，May 15 22:44） - **生产默认开启**： - `eval/start_eagle.sh:70` `SGLANG_EAGLE_NGRAM_ROUTE="${SGLANG_EAGLE_NGRAM_ROUTE:-1}"`（默认值为 1） - `demo-sala/prepare_env.sh:546` 同样默认 1 - 这是提交包（demo-sala）的配置来源 - 代码集成点：`eagle_worker.py:1520` 的 `draft()` 方法是热路径，ngram 在此前置拦截 - CUDA graph 稳定性已修复（D5/D7 分离） --- ### 5. 关键问题回答 | 问题 | 回答 | 证据 | |------|------|------| | **ngram 当前是生产功能吗？** | 是 | 默认开启，已合并，docs 标注为"runtime 集成" | | **probe vs routing 关系?** | 两个阶段 | probe = 实现前离线调研；routing = 工程实现 | | **CUDA graph 稳定性修复合并了吗?** | 是 | D5/D7 分离后端已在 eagle_worker.py L543-683 | | **start_eagle.sh 默认开启吗?** | 是 | L70 `=${SGLANG_EAGLE_NGRAM_ROUTE:-1}` | | **Phantom 代码符号?** | 无 | probe.md/routing.md 未提及；decode/history.md 只提 "phantom 写去除" 为代码清理 | --- ## 总建议（150 字） **保留全部三个文档**。ngram routing 已是生产功能（默认开启），文档职责划分清晰： - **README.md** 作为索引必要 - **probe.md** 记录实现前的关键调研数据和假设，是技术决策的依据 […]
