> DEVELOPER

通读 docs 文档和代码 多委派 subagent 旧文档、冗余文档、文档清理、合并 哪些是不存在的？ 哪些已经在生产中启用了？ 现在文档区太混乱了 请开始做这个工作

> AGENT

我来做文档清理调研。先并行委派多个 subagent 调查各主题，每个 agent 同时阅读该主题的所有文档并对比代码现状，识别幻影/陈旧/冗余文档。

> AGENT

调研完成。9 个 subagent 报告已收齐。在执行清理前，我先把发现合并成行动清单，标记每项的置信度，然后跟你确认动哪些。

> AGENT

接下来先验证几个 subagent 报告里跟 CLAUDE.md / 实际代码可能矛盾的关键事实，避免基于错误信息动手。

> TOOL

[Request interrupted by user]

> DEVELOPER

置信度？ 我要求你亲自对不确定的做完全确定

> AGENT

明白。我自己一条条验证。

> AGENT

发现关键事实矛盾。继续深挖 b12x 默认状态 + CLAUDE.md 是否本身过期：

> AGENT

事实验证完毕。把所有"置信度"问题转成"完全确定"的结论： **关键事实表（亲自验证）**： | 事项 | 真实状态 | 证据 | |---|---|---| | NVFP4 上下文 | **92160 (90K)**，非 48K | `preprocess_model.py:33` `MAX_SEQ_LENGTH=92160` | | NVFP4 校准样本数 | **90**，非 128 | `preprocess_model.py:34` `NUM_CALIBRATION_SAMPLES=90` | | → CLAUDE.md 自身过期 | "loguniform128 校准，48K 上下文" 错 | CLAUDE.md:36 / :122 | | → docs/quant/nvfp4.md 过期 | "48K" 出现 3 次 | nvfp4.md:9/18/19 | | → preprocess_model.py docstring 过期 | "128 samples...Max seq length 48K" | preprocess_model.py:5-6 | | b12x 默认状态 | **默认 OFF**（提交包/eval 脚本/代码三处一致） | prepare_env.sh:519, start_eagle.sh:53, modelopt_quant.py:295 | | → CLAUDE.md "b12x 2-tier" 表述 | 指 kernel 已 ready，但默认关 | 措辞需补 "默认 OFF（SGLANG_ENABLE_B12X=1 启用）" | | probe-sala/ 目录 | **已删**，只剩 probe-sala-s2/（authorized_keys 注入工具） | `ls probe-sala/` no such file；commit b74c10d | | DFlash best.pt | **不存在**，整个 dflash/outputs/ 缺失 | `ls dflash/outputs/` no such file | | docs/eagle/dflash.md | **已自标 deprecate**（顶部 🚨 标注，指向 ../dflash/） | head -20 已确认 | | piecewise/ 工作区 | **存在**（5 份文档，May 17） | `ls piecewise/`，commit 3c17ea3 | | prefill/ 工作区（main-test） | **存在**（experiment-log.md 95KB，May 17） | commit 141fb6d | | docs/prefill/ 不提两者 | **确认**（仅 handover.md L145 单句提及 piecewise） | grep 验证 | | .ipynb_checkpoints | **git 未追踪，已在 .gitignore**（line 29），本地有 11 个文件 | `git ls-files` 空 | | docs/eagle/d7-tune-bench-20260511.md | **被 README.md L14 索引**，是 2026-05-11 D7 调档报告 | grep 验证 | | gemm/bottleneck_cards/ | **只 2 张**，自 2026-05-12 未更新 | `ls -la` 验证 | | gemm/changelog.md 最末轮 | **R-b12x-bucket64 REJECTED**（不是死文件，活跃实验日志） | tail 验证 | 把现在的 task 重组成"文件级具体动作"，先做高置信度的 9 项。

> TOOL

[Request interrupted by user]

> DEVELOPER

先做高置信度的 9 别的就不做了？ 你在胡说八道什么

> DEVELOPER

先做高置信度的 9 别的就不做了？ 你在胡说八道什么 全部要做 而且要做好 不用和我汇报 自己去做

> DEVELOPER

先做高置信度的 9 别的就不做了？ 你在胡说八道什么 全部要做 而且要做好 不用和我汇报 自己去做 而且文档结构要合理 表述要精确 篇幅要适宜

> AGENT

现在修 preprocess_model.py docstring：

> AGENT

现在处理 changelog.md（73KB），把早期 R1-R7 归档：

> AGENT

现在重命名 bottleneck_cards：

> AGENT

现在合并 d7-tune-bench：

> AGENT

全部 11 个 phase 完成。 **结构变更总结**： - **删除**：`docs/eagle/dflash.md`（已 deprecate，内容并入 `docs/dflash/history.md` §2）、`docs/eagle/d7-tune-bench-20260511.md`（并入 `docs/eagle/training/history.md`）、全仓 `.ipynb_checkpoints/`（9 个目录） - **重命名**：`docs/gemm/bottleneck_cards/` → `bottleneck_card_samples/` + 新增 `TEMPLATE.md`（明确"仅样例，全集 54 张未补齐"） - **归档**：`docs/eagle/archive/papers-full.md`（原 papers.md 809 行）、`docs/gemm/archive/changelog-r1-r12prep.md`（原 changelog R1–R12-prep 898 行） - **精简改写**：`docs/handover.md`（190→97 行，去掉与 CLAUDE.md 重复的栈表 + 已退役 probe-sala + 已落产候选）、`docs/eagle/papers.md`（809→111 行，保留 MARS 实装+索引）、`docs/gemm/todo.md`（191→84 行，按 lock-in 状态重组）、`docs/gemm/changelog.md`（1338→450 行，只留 R-b12x 及以后） - **事实修正**：CLAUDE.md（NVFP4 48K/128 → 90K/90、`probe-sala/` → `probe-sala-s2/`、b12x 默认 OFF 补充）、`demo-sala/preprocess_model.py` docstring、`docs/quant/nvfp4.md`、`docs/decode/current.md`（b12x 真实 lock-in 状态）、`docs/gemm/marlin.md` §4（b12x 重写）、`docs/gemm/kernels-sm120.md` §1 / §7.4（去重）、`docs/platform/cu13-stack.md` §4（probe-sala 退役） - **补索引**：`docs/prefill/current.md` §5（新增 piecewise + main-test 工作区）、`docs/eagle/README.md`（D7 调档指向 training/history、300k-training-plan、papers 注释）、`docs/dflash/{current,history}.md`（best.pt 已删警示）、`docs/README.md` 快速定位扩 b12x / NVFP4 校准 / prefill 调研工作区 - **跨文件 link 修复**：归档文件的相对路径、`quant/nvfp4.md` 的 `marlin.md` 指向 总文档行数：10867 → 11289（净增 422 行，主要来自归档保留 + 工作区索引新写），但活跃主文件均显著精简，结构更清晰：每主题 README 是索引；`current.md` 是事实；`history.md` 是已枯竭路线；`archive/` 是长篇调研归档。剩 3 个 broken link 都是引用到 docs/ 外部的运行时 artifact（`/tmp` 调试脚本、`outputs/baseline/`），非文档链不修。

> DEVELOPER

做提交和推送

> AGENT

提交并推送完成。 - commit `0d3474f`：32 文件，+2447 / -2398 - 推送到 `origin/main` 成功
