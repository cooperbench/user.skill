[DEVELOPER]: .sessions/2026-05-21-missing-pages/H001-conversation-prompts.md 对话C

[AGENT]: 开始执行对话 C：历史分析页 UI 设计实施。先读取必读材料。

[AGENT]: 现在读取对话 B 的实施记录和 display 扩展代码。

[AGENT]: 现在读取对话 C 的关键依赖文件 — display projection、defaults、storage history API 和前端规范。

[AGENT]: 让我检查一下现有的页面和组件。

[AGENT]: 开始对话 C。先创建 session note，然后启动 Wave 1 事实收集。

[AGENT]: 启动 Wave 1 Batch 1（3 agent 并行）。

[AGENT]: Batch 1 完成。对 C4/C5 已有足够信息，只需补充 C6（主进程历史操作）。同时读 WaveformChart 确认颜色问题。

[AGENT]: Wave 1 事实收集完成。现在进入 Wave 2 设计阶段。 先做 Service Readiness Audit，检查平台 facade 和 shared composables。

[AGENT]: Wave 1 完成。进入 Wave 2 设计。先检查 CSS tokens 位置和路由配置。

[AGENT]: 所有事实收集完成。进入设计阶段。 --- ## Wave 2: 历史分析页设计 ### Service Readiness Audit | 用户操作 | Service API | 状态 | |---|---|---| | 获取可用小时 | `storageService.listHistoryHours()` | ✅ | | 加载历史数据 | `storageService.loadHistoryMaterials(ids)` | ✅ | | 查询筛选记录 | `storageService.listLocalRecords(query)` | ✅ | | 图表数量管理 | `displayService.updateChartCount(n)` | ✅ | | 单图表配置 | `displayService.updateChartConfig(id, patch)` | ✅ | | 获取图表配置 | `displayService.getPreferences().charts` | ✅ | | CSV 导出 | `storageService.createCsvFromLocalRecords(input)` | ✅ | | 文件保存对话框 | `platform.files.showSaveDialog(opts)` | ✅ | **无 service gap。** 所有操作都由已有 API 覆盖。 ### 设计决策 **DC1: 页面布局** — Mode A (master-detail)，不用 QDrawer，用 flex 布局 - 左面板 320px 固定宽：时间选择 → 数据项选择 → 导出按钮 - 右面板 flex-1：图表数量选择 → 垂直堆叠图表 **DC2: 组件拆分** (5 个新组件 + 1 composable) | 组件 | 职责 | 预估行数 | |---|---|---| | `HistoryPage.vue` | 主页面，flex 布局，编排子组件 | ~120 | | `history/HistoryTimeSelector.vue` | 预设按钮(1h/6h/12h/24h) + 自定义日期 | ~80 | | `history/HistoryDataSelector.vue` | 分组数据项 + 搜索 + 多选 | ~100 | | `history/CSVExportDialog.vue` | 导出配置弹窗 | ~100 | | `history/ChartConfigDialog.vue` | 单图表配置弹窗(选数据项 + Y轴) | ~100 | | `history/useHistoryData.ts` | 核心 composable | ~150 | **DC3: 数据流**（关键设计） ``` 用户选时间范围 → storageService.loadHistoryMaterials(hourKeys) → extractHierarchy(records) → 左面板显示分组/数据项 用户选数据项 → selectedGlobalItems (页面状态) 用户配置图表 → displayService.updateChartConfig(chartId, {selectedItems}) composable → 读 displayService.getPreferences().charts (per-chart selections) → 读 […]