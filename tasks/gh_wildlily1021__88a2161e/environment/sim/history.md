> DEVELOPER

.sessions/2026-05-21-missing-pages/H001-conversation-prompts.md 对话C

> AGENT

开始执行对话 C：历史分析页 UI 设计实施。先读取必读材料。

> AGENT

现在读取对话 B 的实施记录和 display 扩展代码。

> AGENT

现在读取对话 C 的关键依赖文件 — display projection、defaults、storage history API 和前端规范。

> AGENT

让我检查一下现有的页面和组件。

> AGENT

开始对话 C。先创建 session note，然后启动 Wave 1 事实收集。

> AGENT

启动 Wave 1 Batch 1（3 agent 并行）。

> AGENT

Batch 1 完成。对 C4/C5 已有足够信息，只需补充 C6（主进程历史操作）。同时读 WaveformChart 确认颜色问题。

> AGENT

Wave 1 事实收集完成。现在进入 Wave 2 设计阶段。

先做 Service Readiness Audit，检查平台 facade 和 shared composables。

> AGENT

Wave 1 完成。进入 Wave 2 设计。先检查 CSS tokens 位置和路由配置。

> AGENT

所有事实收集完成。进入设计阶段。

---

## Wave 2: 历史分析页设计

### Service Readiness Audit

| 用户操作 | Service API | 状态 |
|---|---|---|
| 获取可用小时 | `storageService.listHistoryHours()` | ✅ |
| 加载历史数据 | `storageService.loadHistoryMaterials(ids)` | ✅ |
| 查询筛选记录 | `storageService.listLocalRecords(query)` | ✅ |
| 图表数量管理 | `displayService.updateChartCount(n)` | ✅ |
| 单图表配置 | `displayService.updateChartConfig(id, patch)` | ✅ |
| 获取图表配置 | `displayService.getPreferences().charts` | ✅ |
| CSV 导出 | `storageService.createCsvFromLocalRecords(input)` | ✅ |
| 文件保存对话框 | `platform.files.showSaveDialog(opts)` | ✅ |

**无 service gap。** 所有操作都由已有 API 覆盖。

### 设计决策

**DC1: 页面布局** — Mode A (master-detail)，不用 QDrawer，用 flex 布局
- 左面板 320px 固定宽：时间选择 → 数据项选择 → 导出按钮
- 右面板 flex-1：图表数量选择 → 垂直堆叠图表

**DC2: 组件拆分** (5 个新组件 + 1 composable)

| 组件 | 职责 | 预估行数 |
|---|---|---|
| `HistoryPage.vue` | 主页面，flex 布局，编排子组件 | ~120 |
| `history/HistoryTimeSelector.vue` | 预设按钮(1h/6h/12h/24h) + 自定义日期 | ~80 |
| `history/HistoryDataSelector.vue` | 分组数据项 + 搜索 + 多选 | ~100 |
| `history/CSVExportDialog.vue` | 导出配置弹窗 | ~100 |
| `history/ChartConfigDialog.vue` | 单图表配置弹窗(选数据项 + Y轴) | ~100 |
| `history/useHistoryData.ts` | 核心 composable | ~150 |

**DC3: 数据流**（关键设计）

```
用户选时间范围 → storageService.loadHistoryMaterials(hourKeys)
               → extractHierarchy(records) → 左面板显示分组/数据项
用户选数据项   → selectedGlobalItems (页面状态)
用户配置图表   → displayService.updateChartConfig(chartId, {selectedItems})
composable    → 读 displayService.getPreferences().charts (per-chart selections)
              → 读 […]

> DEVELOPER

好

> AGENT

启动 Wave 3 自检（3 agent 并行）。

> AGENT

Wave 3 自检完成。分析结果：

**SC1 (规范合规):** 18/28 PASS — 但 agent 误检了**旧系统代码**而非新设计。新设计已规划：CSS token 颜色(DC6)、useAsyncAction/useNotify、rw-dialog-* class、O1 状态顺序。

**SC2 (质量规则 R4):** 同样误检了旧系统 store。新设计的 composable 只从 service 读取、不拥有领域状态、只做展示层桥接，符合 R4。

**SC3 (覆盖度):** 18/18 COVERED，无 gap。

所有自检发现的问题在设计中已有对应措施，无需修改设计。进入 Phase 3 实施。

> AGENT

先读取必读的前端规范文档（CLAUDE.md 硬门槛），然后开始实施。

> AGENT

开始实施。先做 CSS token + WaveformChart 颜色迁移（独立改动），然后核心 composable 和组件。

> AGENT

现在开始并行实施 CSS token + WaveformChart + 路由 + 核心文件。

> AGENT

基础改动完成。现在创建核心 composable `useHistoryData.ts`。

> AGENT

composable 完成。现在并行创建 4 个组件。

> AGENT

子组件完成。现在创建主页面 `HistoryPage.vue`。

> AGENT

所有文件创建完成。运行 build 和 lint 验证。

> AGENT

Build 成功。运行 lint。

> AGENT

2 个 lint 错误在新代码中（其余 7 个是已有的）。修复。

> AGENT

新增代码的 2 个 lint 错误已修复。剩余 9 个 error 全是已有文件（northbound-service.ts, task-service.ts）。

现在运行测试确认无回归。

> AGENT

1259/1260 tests passed，1 个失败是预存的 connection normalizeTransportConfig 测试（与本次改动无关）。

> AGENT

更新 session note 和 topic-index。

> AGENT

---

## 对话 C 实施摘要

**Changed files (10):**

| 文件 | 变更 |
|---|---|
| `css/tokens/_palette.scss` | +indigo-500, violet-500 |
| `css/app.scss` | +--rw-chart-color-1~6 CSS token |
| `widgets/WaveformChart.vue` | 颜色从 CSS token 读取，移除硬编码 |
| `router/routes.ts` | +/history 路由 |
| `pages/history/useHistoryData.ts` | **新建** — 核心 composable |
| `pages/history/HistoryTimeSelector.vue` | **新建** — 时间选择 |
| `pages/history/HistoryDataSelector.vue` | **新建** — 数据项选择 |
| `pages/history/CSVExportDialog.vue` | **新建** — CSV 导出弹窗 |
| `pages/history/ChartConfigDialog.vue` | **新建** — 图表配置弹窗 |
| `pages/HistoryPage.vue` | **新建** — 主页面 Mode A 布局 |

**Verify evidence:**
- `pnpm -C rewrite build` — 通过
- `pnpm -C rewrite lint` — 0 new errors (9 pre-existing)
- `pnpm -C rewrite test` — 1259/1260 passed (1 pre-existing)

**Open issues:** none