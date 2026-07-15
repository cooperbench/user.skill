> DEVELOPER

.sessions/2026-05-21-missing-pages/H001-conversation-prompts.md 对话DP

> TOOL

tool_use Read
id: call_caca4b24620d4032ae0c3228
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-21-missing-pages/H001-conversation-prompts.md"
}
```

> TOOL

tool_use Read
id: call_fd4dd21a247b43a49239f908
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-21-missing-pages/topic-index.md"
}
```

> TOOL

tool_result
id: call_fd4dd21a247b43a49239f908
```
1	# 缺失页面规划与实施
2	
3	> 状态: active | 时间跨度: 2026-05-21 ~ | 最后更新: 2026-05-25 S004 历史分析页 UI 实施完成
4	
5	## 进展线索
6	
7	- **S001** 调研 + 规划 (05-21 ~ 05-24)：线1 bug修复完成，三页深度调研完成，6 agent 回溯主线程 S004-S012+northbound 完成（7类决策补充），对话级 agent 策略已规划（每对话 6-9 agent 三波结构）
8	- **S002** 系统设置页 Wave 1-3 (05-24)：9 agent 事实收集完成，设计方案已出（5 分组 + 串口扩展），3 agent 自检通过（SC1 70%/SC2 100%/SC3 覆盖 #1-#9），待进入 CodeStable feat 流程
9	- **S003** 对话 B display 扩展 (05-25)：9 agent 事实收集→设计→3 agent 自检→14 文件实施→42 问题全量扫描→27 项修复（含 historyBuffer 幽灵边界清除）→build+lint+1216 tests 通过，待提交
10	- **S004** 对话 C 历史分析页 UI (05-25)：Wave 1 事实收集→Wave 2 设计(6项决策+无 service gap)→Wave 3 自检(18/18 覆盖)→10 文件实施(composable+4 组件+token 迁移+路由)→build+lint+1259 tests 通过
11	
12	## 已确认结论
13	
14	### 三页调研结果
15	
16	| 页面 | Feature 覆盖度 | 核心阻塞 | 工作量 |
17	|------|---------------|---------|--------|
18	| 系统设置 | 60% (7/21项) | 串口详细参数 + 跨 feature 配置归口 | 最小 |
19	| 历史分析 | 30% (数据层齐全) | display 多图表 + 元数据注册表 | 中大 |
20	| 存储管理 | 40% (不是高速存储) | 分流机制 + Platform 文件流 + 规则模型 | 最大 |
21	
22	### 共同规律
23	
24	每个页面都分两步：先扩 feature 公开 API（service readiness），再做 UI 设计。
25	
26	### 推荐执行顺序
27	
28	1. **系统设置页**（最快出活，60% 已有，主要是 API 发现和连接） […]

> TOOL

tool_result
id: call_caca4b24620d4032ae0c3228
```
1	# Handoff: 各对话短提示词
2	
3	> 来源: S001 | 交接目标: 给用户开新对话时粘贴
4	> 文件名: H001-conversation-prompts.md
5	
6	## 已完成边界
7	
8	S001 调研完成，6 agent 历史回溯完成，7 类决策补充写入，对话 A~F + task-real + northbound 全部规划完毕。对话 A 已完成并验证提示词缺陷，已修正。
9	
10	## 不要做什么
11	
12	- 不要跳过 Wave 1 直接设计
13	- 不要在 Wave 2 未完成时派 Wave 3
14	- 不要跳过必读文档（frontend conventions / checklist / quickref）
15	- 不要把 northbound/report/file delivery 和页面混在一起
16	- 不要自编审查/自检方法 — CLAUDE.md 已有完整框架，必须引用
17	- 不要闷头跑自检 — 自检方案先说出来等用户确认再执行
18	
19	## 必读
20	
21	1. `.sessions/2026-05-21-missing-pages/S001-research-and-planning.md` — 完整 agent 策略
22	2. `.sessions/2026-05-21-missing-pages/topic-index.md` — 专题总览
23	
24	## 对话 A 经验教训
25	
26	对话 A 实际执行中发现提示词存在以下缺陷，已在本版修正：
27	
28	1. **只写了 Wave 1/2/3，没提 CodeStable 流程** → 现在明确要求按 cs-feat-design → impl → accept 走
29	2. **没指定自检方法** → 现在引用 CLAUDE.md 的完整审查框架
30	3. **没强调实施前必读规范** → 现在列为硬门槛
31	4. **没要求自检前先说方案** → 现在明确要求
32	
33	## 通用流程指令（所有 Lane B/C 对话适用）
34	
35	以下指令适用于所有页面对话（B/C/D/E/F/Northbound），直接附加在提示词中：
36	
37	```
38	## 流程（必须严格按顺序）
39	
40	### Phase 1: 事实收集（Wave 1）
41	- 按 S001 对应对话的 Wave 1 派 agent（6-9 个，每批 ≤3 并发）
42	- 全部完成后汇总事实，先写入 session note 或设计文档
43	
44	### Phase 2: 设计（cs-feat-design）
45	- 汇总 Wave 1 事实，产出设计文档 + checklist
46 […]

> AGENT

好，对话 DP 是实时显示页 UX 重做。我先读取必读文档和事实材料。

> TOOL

tool_use Read
id: call_f2da52f7d0414d5687f9a12d
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-21-missing-pages/S001-research-and-planning.md"
}
```

> TOOL

tool_use Read
id: call_82cbaa1e04e0470abef8c7b6
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/rewrite/src/pages/DisplayPage.vue"
}
```

> TOOL

tool_use Glob
id: call_b619d419f7264d9590b89f18
```json
{
  "pattern": "src/components/display/**/*"
}
```

> TOOL

tool_result
id: call_f2da52f7d0414d5687f9a12d
```
1	# [S001] 调研 + 规划
2	
3	> 2026-05-21 | 规划 | 进行中
4	
5	## 目标
6	
7	线1 bug修复 + 三个缺失页面深度调研 + 规划后续实施路径
8	
9	## 记录
10	
11	### 线1 Bug 修复（已完成）
12	
13	3 个 bug 全部修复，1178/1178 tests passed + 0 lint errors：
14	- BF1: settleResolvers 改 Set<() => void> 支持多等待者
15	- BF2: runExecutionLoop finally 兜底 resolveSettle
16	- BF3: helpers.ts 补 storageService mock
17	
18	### 线2 分析（已完成）
19	
20	3 个高级分析 agent 并行完成：
21	- task-real Phase 2：核心已实现，只差测试收尾（~1天）
22	- 缺失页面：设置 60% / 存储 40% / 历史 30%
23	- Northbound：4 接口缺失，框架可先搭，等甲方 schema
24	
25	### 深度调研（已完成）
26	
27	3 个深度调研 agent 并行完成，6 个维度 × 3 页面 = 18 组调研结果。
28	
29	#### 存储管理关键发现
30	
31	storage-local-baseline **不是**高速存储，只覆盖本地材料管理。旧系统高速存储是三层架构：
32	1. UI 配置层（已部分覆盖）
33	2. 主进程文件操作层（完全缺失：流式写入、文件轮转）
34	3. 网络热路径分流层（完全缺失：`networkHandlers.ts:505-517` 等价物）
35	
36	P0 阻塞项：
37	- Runtime 分流机制（需在 connection/network 添加热路径钩子）
38	- Platform 文件流支持（writeStream、checkFileSize、rotateFile）
39	- 高速存储规则模型（FrameHeaderRule 类型 + 匹配逻辑）
40	
41	#### 历史分析关键发现
42	
43	Storage 数据操作已齐全（query/load/CSV/cleanup），但 UI 层缺失严重：
44	- display feature 的 chartSeries 是单一数组，不支持多图表实例（1-4个）
45	- 缺数据项元数据注册表（label、dataType、groupId）
46	- 缺 Y 轴配置、颜色管理、加载进度反馈、统计计算
47	
48	P0 阻塞项：
49	- display 多图表实例管理
50	- 数据项元数据注册表
51	
52 […]

> TOOL

tool_result
id: call_82cbaa1e04e0470abef8c7b6
```
1	<script setup lang="ts">
2	import { onMounted, ref, shallowRef } from 'vue';
3	import { useRewriteRuntime } from '@/app/rewriteRuntime';
4	import { usePolling } from '@/shared/composables';
5	import DataTable from '@/widgets/DataTable.vue';
6	import StatusBadge from '@/widgets/StatusBadge.vue';
7	import ScatterChart from '@/widgets/ScatterChart.vue';
8	import WaveformChart from '@/widgets/WaveformChart.vue';
9	import { useDisplayRefresh } from '@/features/display/composables';
10	import { receiveLifecycleMap } from '@/features/receive/components/receiveStatusMap';
11	import { fieldValueColumns, recentInputColumns, frameStatsColumns } from '@/features/display/components/display-columns';
12	import type { ReceiveCounterSnapshot, ReceiveLifecycleStatus, ReceiveFieldValueSnapshot, ReceiveRecentInputSnapshot, ReceiveFrameStatisticsSnapshot } from '@/features/receive';
13	
14	// ===== Service references =====
15	const runtime = useRewriteRuntime();
16	const receiveService = runtime.features.receiveService;
17	const displayService = runtime.features.displayService;
18	const displayRefresh = useDisplayRefresh(displayService);
19	
20	// ===== Business data =====
21	const lifecycle = ref<ReceiveLifecycleStatus>('idle');
22	const counters = ref<ReceiveCounterSnapshot>({
23	  batchCount: 0, byteCount: 0, matchedCount: 0, unmatchedCount: 0,
24	  configErrorCount: 0, parseErrorCount: 0, inputErrorCount: 0, staleInputCount: 0,
25	});
26	
27	// ===== Derived data (shallowRef per P2/P4) =====
28	const fieldValues = shallowRef<ReceiveFieldValueSnapshot[]>([]);
29	const recentInputs = shallowRef<ReceiveRecentInputSnapshot[]>([]);
30	const frameStats = shallowRef<ReceiveFrameStatisticsSnapshot[]>([]);
31	
32	// ===== UI state =====
33	const activeTab = ref('overview');
34	const matchRate = ref('--');
35	
36	// ===== Polling =====
37	function […]

> TOOL

tool_result
id: call_b619d419f7264d9590b89f18
```
No files found
```

> AGENT

旧系统 display 组件路径不同。让我查找旧系统相关文件。

> TOOL

tool_use Glob
id: call_2b882ef0ec5141e1a3654d89
```json
{
  "pattern": "src/**/dataDisplay*"
}
```

> TOOL

tool_use Glob
id: call_92e394bbca9c46b0a9be8ad9
```json
{
  "pattern": "src/**/DisplayPage*"
}
```

> TOOL

tool_use Glob
id: call_36f8603d069d4b87a88dac79
```json
{
  "pattern": "src/components/display*/**/*"
}
```

> TOOL

tool_use Grep
id: call_5133a3aca4b042ea8109aa37
```json
{
  "pattern": "dataDisplay",
  "glob": "src/**/*.{vue,ts}",
  "head_limit": 20
}
```

> TOOL

tool_result
id: call_5133a3aca4b042ea8109aa37
```
Found 9 files
src/stores/frames/receiveFramesStore.ts
src/layouts/useAppLifecycle.ts
src/stores/frames/dataDisplayStore.ts
src/components/frames/receive/DataDisplay/DataTable.vue
src/components/frames/receive/DataDisplay/DataDisplayContainer.vue
src/components/frames/receive/DataDisplay/ScatterPlotConfigDialog.vue
src/components/common/UniversalChart.vue
src/components/frames/receive/FrameStatsPanel.vue
src/components/frames/receive/DataDisplay/RecordingControls.vue
```

> TOOL

tool_result
id: call_92e394bbca9c46b0a9be8ad9
```
No files found
```

> TOOL

tool_result
id: call_36f8603d069d4b87a88dac79
```
No files found
```

> TOOL

tool_result
id: call_2b882ef0ec5141e1a3654d89
```
src/types/frames/dataDisplay.ts
src/stores/frames/dataDisplayStore.ts
```

> TOOL

tool_use Read
id: call_d0b68aa20dab4656abc1aff6
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/src/stores/frames/dataDisplayStore.ts"
}
```

> TOOL

tool_use Glob
id: call_3300def8cba24e33a287ee9f
```json
{
  "pattern": "src/components/frames/receive/DataDisplay/**/*"
}
```

> TOOL

tool_result
id: call_d0b68aa20dab4656abc1aff6
```
1	/**
2	 * 数据显示状态管理Store
3	 */
4	
5	import { defineStore } from 'pinia';
6	import { ref, computed } from 'vue';
7	import type {
8	  TableConfig,
9	  DisplaySettings,
10	  DataRecord,
11	  RecordingStatus,
12	  TableRowData,
13	} from '../../types/frames/dataDisplay';
14	import type { HourlyDataFile, HistoryDataRecord } from '../../types/storage/historyData';
15	import { useReceiveFramesStore } from './receiveFramesStore';
16	import { useSettingsStore } from '../settingsStore';
17	import { useTimerManager } from '../../composables/common/useTimerManager';
18	import { convertToHex } from '../../utils/frames/hexCovertUtils';
19	import { getHourKey, isNewHour } from '../../utils/common/dateUtils';
20	import { historyDataAPI } from '../../api/common';
21	import { useStorage } from '@vueuse/core';
22	import type { TimerConfig } from '../../types/common/timerManager';
23	
24	// 导入星座图配置类型
25	export interface ConstellationConfig {
26	  bitWidth: number;
27	  sampleCount: number;
28	  pointSize?: number;
29	
30	  // 数据源配置
31	  iDataSource?: {
32	    frameId: string;
33	    fieldId: string;
34	  };
35	  qDataSource?: {
36	    frameId: string;
37	    fieldId: string;
38	  };
39	
40	  // 刷新间隔（毫秒）
41	  refreshInterval?: number;
42	}
43	
44	export const useDataDisplayStore = defineStore('dataDisplay', () => {
45	  const settingsStore = useSettingsStore();
46	
47	  // 定时器管理器
48	  const timerManager = useTimerManager();
49	
50	  // 循环缓冲区类，用于高效的数据存储和清理
51	  class CircularBuffer<T> {
52	    private buffer: […]

> TOOL

tool_result
id: call_3300def8cba24e33a287ee9f
```
src/components/frames/receive/DataDisplay/RecordingControls.vue
src/components/frames/receive/DataDisplay/TableControls.vue
src/components/frames/receive/DataDisplay/DisplayModeToggle.vue
src/components/frames/receive/DataDisplay/ScatterPlotConfigDialog.vue
src/components/frames/receive/DataDisplay/OrderControls.vue
src/components/frames/receive/DataDisplay/DataDisplayContainer.vue
src/components/frames/receive/DataDisplay/DataTable.vue
src/components/frames/receive/DataDisplay/SpecialConstellationChart.vue
```

> AGENT

让我继续读取旧系统 UI 组件和新系统 display feature。

> TOOL

tool_use Read
id: call_be79828d12fe4e00993094f0
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/src/components/frames/receive/DataDisplay/DataDisplayContainer.vue"
}
```

> TOOL

tool_use Agent
id: call_bb22fce173f3449493454940
```json
{
  "description": "Read display feature code",
  "prompt": "Read and summarize the following files in the new rewrite display feature. Report the full API surface (types, service methods, selectors, composables):\n\n1. rewrite/src/features/display/core/types.ts\n2. rewrite/src/features/display/core/defaults.ts\n3. rewrite/src/features/display/services/display-service.ts\n4. rewrite/src/features/display/selectors/ (all files)\n5. rewrite/src/features/display/composables/ (all files)\n6. rewrite/src/features/display/index.ts (public API)\n\nFor each file, report:\n- Key types and their fields\n- Service method signatures (name, params, return type)\n- Selector signatures and what they project\n- Composable signatures and what they provide\n\nAlso check if there's a display adapter or state directory.\n\nKeep the report structured and concise. Focus on the API surface, not implementation details.",
  "subagent_type": "Explore"
}
```

> TOOL

tool_use Agent
id: call_36a23c24a58e4ff989105196
```json
{
  "description": "Read old display UI components",
  "prompt": "Read and summarize the following old system display UI components. Focus on extracting the UX patterns, interactions, and component structure:\n\n1. src/components/frames/receive/DataDisplay/DataDisplayContainer.vue - main container\n2. src/components/frames/receive/DataDisplay/DataTable.vue - data table\n3. src/components/frames/receive/DataDisplay/TableControls.vue - table controls\n4. src/components/frames/receive/DataDisplay/DisplayModeToggle.vue - display mode toggle\n5. src/components/frames/receive/DataDisplay/RecordingControls.vue - recording controls\n6. src/components/frames/receive/DataDisplay/ScatterPlotConfigDialog.vue - scatter plot config\n7. src/components/frames/receive/DataDisplay/OrderControls.vue - order controls\n8. src/components/frames/receive/DataDisplay/SpecialConstellationChart.vue - constellation chart\n\nFor each component, report:\n- What it renders (layout, sections)\n- User interactions (clicks, selections, toggles)\n- Props and events\n- How it connects to the dataDisplayStore\n\nThen provide a summary of the overall UX pattern:\n- How dual panels work\n- How display mode switching works (table/chart/constellation)\n- How chart configuration works\n- How recording works\n- How group/field selection works",
  "subagent_type": "Explore"
}
```

> TOOL

tool_result
id: call_be79828d12fe4e00993094f0
```
1	<script setup lang="ts">
2	import { ref, computed } from 'vue';
3	import DataTable from './DataTable.vue';
4	import UniversalChart from '../../../common/UniversalChart.vue';
5	import SpecialConstellationChart from './SpecialConstellationChart.vue';
6	import ScatterPlotConfigDialog from './ScatterPlotConfigDialog.vue';
7	import TableControls from './TableControls.vue';
8	import DisplayModeToggle from './DisplayModeToggle.vue';
9	import RecordingControls from './RecordingControls.vue';
10	import UniversalChartSettingsDialog from '../../../common/UniversalChartSettingsDialog.vue';
11	import { useDataDisplayStore } from '../../../../stores/frames/dataDisplayStore';
12	import { useReceiveFramesStore } from '../../../../stores/frames/receiveFramesStore';
13	import { useLocalStorage } from '@vueuse/core';
14	import type { YAxisConfig, PerformanceConfig } from '../../../../types/storage/historyData';
15	
16	// Store
17	const dataDisplayStore = useDataDisplayStore();
18	const receiveFramesStore = useReceiveFramesStore();
19	
20	// 对话框状态
21	const table1SettingsDialog = ref(false);
22	const table2SettingsDialog = ref(false);
23	
24	// 性能配置持久化存储 - 优化默认值提高实时图表性能
25	const performanceConfig = useLocalStorage<PerformanceConfig>('chart-performance-config', {
26	  maxDataPoints: 500, // 减少数据点提高性能
27	  updateInterval: 1000, // 保持1秒更新间隔
28	  enableIncrementalUpdate: true, // 启用增量更新
29	  enableSampling: true, // 启用抽样减少数据量
30	  samplingInterval: 2, // 每2个点取1个
31	});
32	
33	// 普通图表设置对话框触发
34	
35	// 处理表格1图表设置点击
36	const handleTable1ChartSettings = () => {
37	  table1SettingsDialog.value = true;
38	};
39	
40	// 处理表格2图表设置点击
41	const handleTable2ChartSettings = () => {
42	  table2SettingsDialog.value = true;
43	};
44	
45	// UI显示用的数据项接口
46	interface UIDataItem {
47 […]

> TOOL

tool_result
id: call_36a23c24a58e4ff989105196
```
## Summary of Old System Display UI Components

Based on my analysis of the 8 UI components, here's a comprehensive summary of the UX patterns and component structure:

---

## Individual Component Analysis

### 1. DataDisplayContainer.vue (Main Container)
**What it renders:**
- Dual panel layout with two side-by-side panels (table1 and table2)
- Each panel has a header with display mode toggle, settings button, and group selector
- Main content area switches between table/special chart/regular chart
- Bottom status bar showing panel states and recording controls

**User interactions:**
- Switch display modes for each panel independently
- Open settings dialogs for chart/scatter configuration
- Select data groups for each panel
- Clear chart history
- Start/stop recording

**Props & events:**
- No props (uses stores directly)
- Emits to store methods for all state updates

**Store connections:**
- `dataDisplayStore` - Main store for all display state
- `receiveFramesStore` - Source of frame/field data
- Manages both table1 and table2 configurations

---

### 2. DataTable.vue (Data Table)
**What it renders:**
- Quasar table with fixed columns (index, label, value, hex, favorite, actions)
- Sticky header, alternating row colors
- Empty state and loading states
- Virtual scrolling […]

> TOOL

tool_result
id: call_bb22fce173f3449493454940
```
# Display Feature API Surface Report

## Overview
The display feature is located at `/rewrite/src/features/display/` and provides table, chart, and scatter visualization capabilities with a clean separation between preferences, projections, and source material ingestion.

---

## Core Types (`core/types.ts`)

### Display Modes
- **DisplayMode**: `'table' | 'chart' | 'special'`

### Preference Types
- **TableDisplayPreference**: `{ displayMode, selectedGroupId, selectedItems }`
- **ChartPerformancePreference**: `{ maxPoints, refreshIntervalMs }`
- **YAxisPreference**: `{ autoScale, min?, max? }`
- **ChartInstancePreference**: `{ id, title, selectedItems, yAxis, performance }`
- **ScatterSourceBinding**: `{ groupId, dataItemId }`
- **ScatterDisplayPreference**: `{ iSource, qSource, sampleCount, bitWidth, refreshIntervalMs }`
- **DisplayPreferences**: `{ table1, table2, charts, scatter, refreshCadenceMs }`

### Source Material Types
- **DisplayFieldMaterial**: `{ groupId, dataItemId, fieldName, value, displayValue, updatedAt? }`
- **DisplaySourceAvailability**: `{ available, reason? }`
- **DisplaySourceMaterial**: `{ fields?, availability? }`

### Projection Types (UI-safe read models)
- **TableRowProjection**: `{ groupId, dataItemId, fieldName, value, displayValue, updatedAt? }`
- **ChartPoint**: `{ timestamp, value }`
- **ChartSeriesProjection**: `{ fieldId, fieldName, points }`
- **ScatterPoint**: `{ i, q }`
- **ScatterProjection**: `{ points, sampleCount }`
- **ChartInstanceProjection**: `{ id, series }`
- **DisplayProjection**: `{ table1Rows, table2Rows, charts, scatter }`

### Core Snapshot Type
- **DisplaySnapshot**: `{ schemaVersion, preferences, projection, […]

> AGENT

事实收集进展顺利。继续读取必读规范和 receive feature API。

> TOOL

tool_use Read
id: call_74bc1eb4b9434871b519684e
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/quality/rewrite-frontend-conventions.md"
}
```

> TOOL

tool_use Read
id: call_03966b45edda4a5084431e8f
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/reference/rewrite-frontend-quickref.md"
}
```

> TOOL

tool_use Agent
id: call_7a227fe865bb4967a3622e01
```json
{
  "description": "Read receive feature public API",
  "prompt": "Read and summarize the receive feature's public API that DisplayPage consumes. Focus on:\n\n1. rewrite/src/features/receive/index.ts - what's exported\n2. The receive service methods that DisplayPage currently uses:\n   - getUiSnapshot()\n   - listFieldValues()\n   - listRecentInputs()\n   - listFrameStats()\n3. The receive lifecycle map: receiveLifecycleMap\n\nReport the full type signatures and what data they return.",
  "subagent_type": "Explore"
}
```

> TOOL

tool_result
id: call_03966b45edda4a5084431e8f
```
1	---
2	doc_type: reference
3	type: rewrite-frontend-quickref
4	status: active
5	date: 2026-05-14
6	summary: 前端速查卡——写新页面/新组件前花 30 秒扫一遍。含 shared/ 完整 API 索引 + 规范红线 + 新页面检查清单。
7	tags:
8	  - rewrite
9	  - frontend
10	  - quickref
11	---
12	
13	# Rewrite 前端速查卡
14	
15	> 写新页面/新组件前先看。详细规则见 `rewrite-frontend-conventions.md`。
16	> shared/ 所有 API 从 `@/shared` 或 `@/shared/composables` 导入。shared 不 import 任何 feature。
17	
18	## composables — 页面必用
19	
20	| composable | 用途 | 替代什么 |
21	|-----------|------|----------|
22	| `useAsyncAction()` | 异步操作防重 + 自动错误通知 | 手写 operatingIds + try/finally |
23	| `usePolling(fn, ms)` | rAF 轮询 + 自动清理 | 手写 rAF / disposed / 节流 |
24	| `useNotify()` | 统一消息通知 | 散落 `$q.notify()` |
25	| `useStableKeys(prefix?)` | v-for 稳定 key 生成 | index key |
26	
27	```typescript
28	const { execute, isOperating } = useAsyncAction()          // execute: 加锁→执行→解锁→失败 notify
29	const { start, stop } = usePolling(() => refresh(), 1000)  // 自动 onUnmounted 清理
30	const notify = useNotify()                                  // success / error / info / warning
31	const { keys, syncKeys } = useStableKeys('step')            // keys.value[i] 始终稳定
32	```
33	
34	## utils/ — 纯工具函数
35	
36 […]

> TOOL

tool_result
id: call_74bc1eb4b9434871b519684e
```
1	---
2	doc_type: quality
3	type: rewrite-frontend-conventions
4	status: draft
5	date: 2026-05-11
6	summary: 前端 UI 规范，讨论/设计/实施时参照。每条规则一句话 + 简短原因 + 一个示例。
7	tags:
8	  - rewrite
9	  - frontend
10	  - conventions
11	  - quasar
12	  - performance
13	---
14	
15	# Rewrite 前端 UI 规范
16	
17	样式 token 规则和 UnoCSS 结构性布局职责划分见 CLAUDE.md "目录与职责"，token 定义见 `rewrite/src/css/tokens/`，本文不重复。代码质量规则见 `rewrite-quality-rules.md`。自检 checklist 见 `rewrite-frontend-checklist.md`。
18	
19	---
20	
21	## 1. Quasar 组件使用
22	
23	### Q1. UI 需求优先从 Quasar 内建方案解决
24	
25	不引入第三方 UI 库（ag-Grid、Lucide、vue-sonner 等）。
26	
27	```typescript
28	// ❌ 第三方 toast
29	import { toast } from 'vue-sonner'; toast.success('ok');
30	// ❌ 第三方图标
31	import { Trash2 } from 'lucide-vue-next';
32	
33	// ✅ Quasar 内建
34	$q.notify({ type: 'positive', message: 'ok' });
35	<q-icon name="o_delete" />
36	```
37	
38	### Q2. Quasar prop 控制视觉行为，不用 CSS 覆盖
39	
40	```vue
41	<!-- ❌ -->
42	<q-input style="padding: 4px; height: 32px;" />
43	<q-btn style="box-shadow: none; background: transparent;" />
44	
45	<!-- ✅ -->
46	<q-input dense />
47	<q-btn flat color="primary" />
48	```
49	
50	### Q3. 颜色使用 Quasar brand prop，不硬编码
51	
52	```vue
53	<!-- ❌ -->
54	<q-btn […]

> TOOL

tool_result
id: call_7a227fe865bb4967a3622e01
```
Perfect! Now I have all the information needed. Let me provide a comprehensive summary:

## Receive Feature Public API Summary

### 1. Main Export (`rewrite/src/features/receive/index.ts`)

The receive feature exports:

**Types:**
- All core types from `./core` (ReceiveUiSnapshot, ReceiveFieldValueSnapshot, etc.)
- Service types: `CreateReceiveServiceOptions`, `ReceiveInputEvent`, `ReceiveInputSource`, `ReceiveReader`, `ReceiveService`, `ReceiveServiceOutcome`
- Selector query types: `ReceiveFieldValueQuery`, `ReceiveFrameStatsQuery`, `ReceiveRecentInputQuery`

**Functions:**
- `createReceiveReader()` - Creates a read-only receive reader
- `createReceiveService()` - Creates the main receive service
- Selectors: `selectReceiveCounters()`, `selectReceiveEvents()`, `selectReceiveFieldValues()`, `selectReceiveFrameStats()`, `selectReceiveRecentInputs()`, `selectReceiveSnapshot()`, `selectReceiveSourceStats()`, `selectReceiveUiSnapshot()`

### 2. Receive Service Methods Used by DisplayPage

#### **`getUiSnapshot(): ReceiveUiSnapshot`**
Returns UI-focused snapshot containing:
```typescript
interface ReceiveUiSnapshot {
  readonly lifecycle: ReceiveLifecycleStatus;        // 'idle' | 'ready' | 'receiving' | 'error'
  readonly referenceVersion: number;
  readonly counters: ReceiveCounterSnapshot;
  readonly currentFrame?: ReceiveMatchedFrameSummary;
  readonly frameStats: readonly ReceiveFrameStatisticsSnapshot[];
  readonly fieldValues: readonly ReceiveFieldValueSnapshot[];
  readonly recentInputs: readonly ReceiveRecentInputSnapshot[];
  readonly lastIssue?: ReceiveIssue;
}
```

#### **`listFieldValues(query?: ReceiveFieldValueQuery): ReceiveFieldValueSnapshot[]`**
Returns field values with optional filtering:
```typescript
interface ReceiveFieldValueQuery {
  readonly frameId?: string;
  readonly fieldId?: string;
}

interface ReceiveFieldValueSnapshot {
  readonly frameId: string;
  readonly frameName: string;
  readonly fieldId: string;
  readonly fieldName: string;
  readonly dataType: FrameDataType;
  readonly offset: number;
  readonly length: number;
  readonly rawHex: string;
  readonly value: ReceiveParsedFieldPrimitive;  // number | string | null
  readonly […]

> AGENT

Wave 1 事实收集完成。汇总关键发现。

---

## Wave 1 事实汇总

### 新系统 DisplayPage 现状（277 行，旧系统 ~15%）

- 统计栏 + 两 tab（数据总览 / 可视化）
- 总览：字段值表 + 帧匹配统计表 + 最近输入表
- 可视化：单波形图 + 单星座图
- 数据来源：receive service 直接查 + displayRefresh composable 取图表

### Display Feature 已有 API（不改，只做 UI 层）

display service 已具备完整能力，但当前页面几乎没用到：

| 能力 | API | 当前页面使用 |
|------|-----|------------|
| 双面板偏好 | `preferences.table1 / table2` | ❌ 未用 |
| 三种显示模式 | `DisplayMode = 'table' \| 'chart' \| 'special'` | ❌ 硬编码 tab |
| 分组选择 | `selectedGroupId` | ❌ 未暴露 |
| 多图表实例 | `ChartInstanceProjection[]`（1-4） | ⚠️ 只取 [0] |
| Y 轴配置 | `YAxisPreference { autoScale, min, max }` | ❌ 未暴露 |
| 星座图 | `ScatterProjection + ScatterDisplayPreference` | ⚠️ 有组件无配置 |
| 图表性能 | `ChartPerformancePreference { maxPoints, refreshIntervalMs }` | ❌ 未暴露 |
| 刷新 composable | `useDisplayRefresh(service)` | ✅ 在用 |

### 旧系统 UX 核心（需要还原的）

1. **双面板**：左右两个独立面板，各有独立配置
2. **三种模式切换**：表格 / 折线图 / 星座图，每面板独立
3. **分组选择器**：每面板独立选数据分组
4. **图表配置弹窗**：字段选择 + Y 轴 + 性能
5. **星座图配置弹窗**：I/Q 数据源 + 位宽 + 采样数
6. **底部状态栏**：面板状态 + 更新间隔
7. **录制控制**：开始/停止 + 录制时长 + 记录数

### 不在 scope 的（H001 边界）

- **录制控制**：不在 display feature，属 settings/storage 层，需要 feature API 扩展
- **字段排序/收藏**：属 receive feature，不改 […]

> DEVELOPER

纳入。不过这个不算单独storage吗？字段排序有就行。收藏扔了吧，用不上。

> AGENT

明白。录制确实是存储的活——composable 在页面层协调 display（取什么）+ storage（存什么）+ receive（数据源）。字段排序用 display preference 的 selectedItems 顺序即可。

有一个实际限制需要确认：

**Display feature 只有单个 scatter 配置**（`ScatterDisplayPreference`），不是双份。所以：
- 两面板可独立选 table/chart
- constellation 模式同时只能一个面板用（切另一个面板自动回 table/chart）

实际使用中很少需要双星座图，这个限制应该可接受。

如果没有异议我直接进设计 + 实施。整体方案：

| 项目 | 方案 |
|------|------|
| **布局** | 双面板并排，底部状态栏 |
| **面板组件** | `DisplayPanel.vue`，`panelId` prop，复用×2 |
| **三模式** | 每面板独立切换，mode→条件渲染 |
| **分组选择** | 面板 header 下拉，数据源 receive groups |
| **图表配置** | `ChartConfigDialog.vue`：字段多选 + Y轴 + 性能 |
| **星座配置** | `ScatterConfigDialog.vue`：I/Q源 + 参数 |
| **字段排序** | table 模式每行 up/down，改 selectedItems 顺序 |
| **录制** | `useDataRecording` composable 协调 receive+storage |
| **统计栏** | 保留当前 stats bar（receive counters） |
| **Feature API** | 不改 |

**新增/重写文件**：
- `DisplayPage.vue` — 完全重写
- `DisplayPanel.vue` — 新增
- `ChartConfigDialog.vue` — 新增
- `ScatterConfigDialog.vue` — 新增
- `useDataRecording.ts` — 新增 composable

**复用已有**：DataTable、WaveformChart、ScatterChart、StatusBadge、useDisplayRefresh、usePolling、useAsyncAction