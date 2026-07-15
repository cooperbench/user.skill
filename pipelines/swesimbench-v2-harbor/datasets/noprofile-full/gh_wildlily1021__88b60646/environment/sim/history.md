[DEVELOPER]: .sessions/2026-05-21-missing-pages/H001-conversation-prompts.md 做这个

[AGENT]: 我先读取 handoff 文件以了解上下文。

[AGENT]: 根据 topic-index，H001 中已完成的有：A、B、C、D、E、task-real Phase 2、Northbound。下一个待执行的是 **对话 DP：DisplayPage UX 重做实施**（S007 设计已完成）。 开始读取设计文档和必读文件。

[AGENT]: 现在正在读取必读的前端规范和其余的代码文件。

[AGENT]: 让我阅读更多文件以了解全貌——展示功能的公开 API、分组结构和运行时绑定。

[AGENT]: 我来检查一下用于录音功能的存储导出，然后开始实现。

[AGENT]: 好的，我已经掌握了所有需要的 API 信息。现在我将创建任务并开始实施。

[AGENT]: 正在并行创建 DisplayPanel.vue、ChartConfigDialog.vue、ScatterConfigDialog.vue 和 display-columns.ts。

[AGENT]: 正在将 `panelTableColumns` 添加到 `display-columns.ts` 并重写 `DisplayPage.vue`。

[AGENT]: 现在正在重写 DisplayPage.vue — 核心更改：双面板布局、底部带录制功能的条形图、移除概览标签页。

[AGENT]: 正在运行构建和代码检查进行验证。

[AGENT]: 构建成功。正在运行 lint。

[AGENT]: Lint 通过（退出码 0，所有问题都在已构建的 dist 文件中，而不是源代码中）。正在运行测试。

[AGENT]: 1350 通过，1 失败 — 失败的测试是一个预先存在的连接问题 (`stopBits` test from S002, 已在 topic-index 中注明). 我的改动没有引入新的失败。

[AGENT]: 实施完成。 **Changed files:** - `rewrite/src/pages/DisplayPage.vue` — 完整重写：双面板布局 + 统计栏 + 底部录制控制栏 + 图表/星座配置对话框集成。移除 overview tab。 - `rewrite/src/features/display/components/DisplayPanel.vue` — 新建，纯展示面板组件（模式切换 + 分组下拉 + 表格/波形/星座三模式） - `rewrite/src/features/display/components/ChartConfigDialog.vue` — 新建，图表字段选择 + Y轴 + 性能配置 - `rewrite/src/features/display/components/ScatterConfigDialog.vue` — 新建，I/Q 数据源 + 位宽/采样数配置 - `rewrite/src/features/display/components/display-columns.ts` — 追加 `panelTableColumns` **Verify evidence:** - `pnpm build` — 成功 - `pnpm lint` — 通过（exit 0，issues 均在 dist 编译产物） - `vitest run` — 1350 pass / 1 fail（connection stopBits 是 S002 遗留问题，非本次引入） **Open issues:** - connection-core stopBits 测试失败（S002 遗留，topic-index 已记录） - 图表高度使用 `height="100%"` 依赖 flex 布局正确传高，需在运行时验证 - Y-axis 配置已保存到 preference 但 WaveformChart 尚未消费该配置