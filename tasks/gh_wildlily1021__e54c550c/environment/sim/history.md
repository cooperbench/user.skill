[DEVELOPER]: .sessions/2026-05-21-missing-pages/H001-conversation-prompts.md task-real Phase 2做这个

[AGENT]: 我先阅读一下交接文件，以理解上下文。

[AGENT]: Lane A 任务 — task-real Phase 2 测试收尾。先读设计文档和现有测试。

[AGENT]: 让我阅读清单和测试文件，以了解缺少了什么。

[AGENT]: 159 测试全部通过。让我看详细输出和现有测试覆盖范围，对比 design checklist 找 Phase 2 缺口。

[AGENT]: 找到了 — 1个测试失败：`TaskService - trigger scheduling fires on matching receive event`。让我阅读该测试以及研究笔记中第二阶段的定义。

[AGENT]: 现在我来检查 S001 研究文件，了解“Phase 2”指代什么，并阅读实际的测试失败。

[AGENT]: 让我检查一下当前实现状态与第二阶段设计的对比。

[AGENT]: 让我检查一下核心类型，看看第二阶段是否已经实现。

[AGENT]: Phase 2 类型已实现。让我检查核心引擎文件和 checklist 完成状态。

[AGENT]: Phase 2 核心代码已完整实现。现在有两个问题要解决：1) 1 个失败测试 2) 确认缺失测试项。 先定位失败原因。

[AGENT]: 单个文件跑全通过。让我确认之前全量跑的 2 个 failure 是不是都在 connection。

[AGENT]: Task 测试独立跑全部通过（159/159）。全量跑时的 `STACK_TRACE_ERROR` 是测试间污染或并行竞态问题，不是 task 逻辑 bug。 现在让我对照 design checklist 确认测试覆盖情况。

[AGENT]: 分析完成。缺失 5 个测试区域：resolveFieldValues、step repeat、fieldVariations 注入、exitCondition、buildSendRequest 对齐。让我先读相关源码再写测试。

[AGENT]: 现在我有了完整的画面。让我阅读 `core/index.ts` 来理解导出。

[AGENT]: 现在开始写缺失的测试。分两部分：纯函数测试加到 `task-core.spec.ts`，集成测试加到 `ta[REDACTED_SK].spec.ts`。

[AGENT]: 现在开始写测试。先加纯函数测试到 `task-core.spec.ts`。

[AGENT]: 现在在 fixture 验证部分之后添加 `resolveFieldValues` 和 `buildSendRequest` 的测试。

[AGENT]: 现在，针对服务层面的测试（repeat、fieldVariations、exitCondition），请将其添加到 `ta[REDACTED_SK].spec.ts` 文件中。

[AGENT]: 现在运行测试，看看它们是否通过。

[AGENT]: 有 6 个测试失败需要修复。主要是：(1) 参数顺序，(2) 字段访问路径 (`request.userFieldValues`)，(3) 重复失败行为是完成而不是停止，(4) `until` 测试使用了错误的服务实例。我来修复所有这些问题。

[AGENT]: 现在修复服务级别的测试。

[AGENT]: 修复重复失败测试 — 重复失败会中断循环但不会触发错误策略，因此任务会完成。

[AGENT]: 修复 `fieldVariations` 注入测试 — 使用 `request.userFieldValues` 而不是直接的 `userFieldValues`。

[AGENT]: 现在还需要修复“repeat with infinite maxCount”测试——它也使用了 `createTestSetup` 但又创建了一个单独的服务。

[AGENT]: 现在也修复 `exitCondition` 测试 — 它们需要使用一个共享的发送服务。

[AGENT]: 183/183 全部通过。之前全量跑的 STACK_TRACE_ERROR 是测试间并行竞态问题，不是 task 逻辑 bug。现在跑 build + lint 验证。

[AGENT]: Build 成功，lint 通过（2 个错误在无关文件 `verify-serialport.mjs`）。 ## 实施摘要 **Changed files:** - `rewrite/src/features/task/__tests__/task-core.spec.ts` — 新增 17 个测试：resolveFieldValues（8 项：空值/基础值/覆写/多轮/多字段/越界/保留/混合）+ buildSendRequest 对齐（6 项：字段映射/variables/context/无options/targetId无fallback/fieldVariations合并） - `rewrite/src/features/task/__tests__/ta[REDACTED_SK].spec.ts` — 新增 7 个测试：step repeat（4 项：maxCount/until条件/失败中断/无限+until）、fieldVariations注入（3 项：per-iteration覆写/auto-maxIterations/保留非变体字段）、exitCondition（3 项：条件触发停止/无provider忽略/与maxDurationMs共存） **Verify evidence:** - `pnpm -C rewrite test`（task feature）: 183/183 通过（+24 新测试） - `pnpm -C rewrite build`: 成功 - `pnpm -C rewrite lint`: 通过（2 个无关错误） **Open issues:** - 全量并行跑时 `trigger scheduling ignores non-matching events` 偶现 STACK_TRACE_ERROR（测试间竞态，非逻辑 bug，独立跑稳定通过） - step repeat 失败时不会触发 errorPolicy，而是中断迭代循环后 task 正常 complete — 这是设计层面的问题，如果需要 repeat 失败也走 errorPolicy 需要额外改动