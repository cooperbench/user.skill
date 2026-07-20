> DEVELOPER

.sessions/2026-05-21-missing-pages/H001-conversation-prompts.md 对话B

> DEVELOPER

.sessions/2026-05-21-missing-pages/H001-conversation-prompts.md 对话B

> TOOL

tool_use Read
id: call_940b369392dc4da2bd3ba815
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-21-missing-pages/H001-conversation-prompts.md"
}
```

> TOOL

tool_result
id: call_940b369392dc4da2bd3ba815
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

好的，这是**对话 B**。让我先读取必读材料。

> TOOL

tool_use Read
id: call_b625d66a281449daa54ef603
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-21-missing-pages/S001-research-and-planning.md"
}
```

> TOOL

tool_use Read
id: call_ed818bc5fec8413ea8b9982a
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-21-missing-pages/topic-index.md"
}
```

> TOOL

tool_result
id: call_ed818bc5fec8413ea8b9982a
```
1	# 缺失页面规划与实施
2	
3	> 状态: active | 时间跨度: 2026-05-21 ~ | 最后更新: 2026-05-24 S001 历史回溯完成
4	
5	## 进展线索
6	
7	- **S001** 调研 + 规划 (05-21 ~ 05-24)：线1 bug修复完成，三页深度调研完成，6 agent 回溯主线程 S004-S012+northbound 完成（7类决策补充），对话级 agent 策略已规划（每对话 6-9 agent 三波结构）
8	- **S002** 系统设置页 Wave 1-3 (05-24)：9 agent 事实收集完成，设计方案已出（5 分组 + 串口扩展），3 agent 自检通过（SC1 70%/SC2 100%/SC3 覆盖 #1-#9），待进入 CodeStable feat 流程
9	
10	## 已确认结论
11	
12	### 三页调研结果
13	
14	| 页面 | Feature 覆盖度 | 核心阻塞 | 工作量 |
15	|------|---------------|---------|--------|
16	| 系统设置 | 60% (7/21项) | 串口详细参数 + 跨 feature 配置归口 | 最小 |
17	| 历史分析 | 30% (数据层齐全) | display 多图表 + 元数据注册表 | 中大 |
18	| 存储管理 | 40% (不是高速存储) | 分流机制 + Platform 文件流 + 规则模型 | 最大 |
19	
20	### 共同规律
21	
22	每个页面都分两步：先扩 feature 公开 API（service readiness），再做 UI 设计。
23	
24	### 推荐执行顺序
25	
26	1. **系统设置页**（最快出活，60% 已有，主要是 API 发现和连接）
27	2. **历史分析页**（display 扩展 + storage 元数据）
28	3. **存储管理页**（涉及 main/platform/runtime，最复杂）
29	4. **task-real Phase 2**（核心已实现，只差测试收尾，可穿插）
30	5. **Northbound 框架**（可与页面并行，框架不阻塞）
31	
32	## 未决项
33	
34	- 串口详细参数（dataBits/stopBits/parity）归 connection feature 还需确认具体 API
35	- 高速存储的分流机制是否需要新 feature 还是在 runtime 层解决
36	- display 多图表扩展的设计方案（单 […]

> TOOL

tool_result
id: call_b625d66a281449daa54ef603
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

> AGENT

好的，启动**对话 B：历史分析 — display 扩展设计实施**。

**直接合同：** S001 §历史分析关键发现 + §历史分析补充
**边界护栏：** R7（多图表偏好归 display，数据归 storage）+ R4

## Phase 1: Wave 1 — 事实收集

开始 Batch 1（3 agent 并行）：B1 display types/defaults、B2 display service/selectors/composables、B3 display design 文档。

> TOOL

tool_use Agent
id: call_b2f704f2c2b646ce8940e3e6
```json
{
  "description": "B1 display types + defaults",
  "subagent_type": "Explore",
  "prompt": "只读调研，不写代码。彻底调研 rewrite/src/features/display/core/ 目录下的所有文件，重点关注：\n\n1. types.ts — 所有显示相关类型定义（TableDisplayPreference/ChartDisplayPreference/ScatterDisplayPreference 等）\n2. defaults.ts — 默认值定义\n3. 其他 core/ 下的文件\n\n产出：\n- 当前 chartSeries 的完整类型结构（字段的类型、可选性）\n- ChartDisplayPreference 的完整字段列表\n- 所有 display 相关的 type/interface 汇总\n- 多图表相关：当前是单一 chartSeries 还是已有多图表支持\n- 默认值结构\n\n请完整输出所有发现，不要省略。"
}
```

> TOOL

tool_use Agent
id: call_8cb063d23b874b65bdbb4dfb
```json
{
  "description": "B2 display service + selectors",
  "subagent_type": "Explore",
  "prompt": "只读调研，不写代码。彻底调研以下目录/文件：\n\n1. rewrite/src/features/display/services/display-service.ts — 完整 service API 签名（所有方法）\n2. rewrite/src/features/display/selectors/ — 所有 selector 文件和投影\n3. rewrite/src/features/display/composables/ — 所有 composable 文件\n4. rewrite/src/features/display/state/ — 状态管理结构\n\n产出：\n- display service 完整操作面（每个方法签名：名字、参数类型、返回类型）\n- selector 投影列表（每个 selector 名字、返回什么）\n- composable 列表和功能\n- state 结构（有哪些 slice、如何组织）\n- ingestSourceMaterial API 的完整签名和行为\n- getChartSeries 的完整签名和行为\n- updatePreferences 的完整签名和行为\n- 多图表相关：当前 API 是否支持多图表实例\n\n请完整输出所有发现，不要省略。"
}
```

> TOOL

tool_use Agent
id: call_dad7ca705f0d4396af83a234
```json
{
  "description": "B3 display design docs",
  "subagent_type": "Explore",
  "prompt": "只读调研，不写代码。搜索并读取所有 display 相关的设计文档：\n\n1. codestable/features/rewrite-display/ 目录下的所有文件\n2. codestable/features/ 目录下任何包含 \"display\" 或 \"chart\" 的文件\n3. codestable/ 下其他位置可能涉及 display 的设计文档（搜索 display/chart 关键词）\n\n产出：\n- display 设计意图和目标\n- 已知扩展点和待办项\n- 多图表相关的设计决策\n- 与其他 feature 的交互契约\n- 任何关于 history/历史分析 的设计说明\n\n如果没有找到相关文档，明确说明。请完整输出所有发现。"
}
```

> TOOL

tool_result
id: call_b2f704f2c2b646ce8940e3e6
```
Based on my thorough investigation of the `rewrite/src/features/display/core/` directory, here is my comprehensive report:

---

## **Display Feature Core Types & Structure - Complete Investigation Report**

### **1. ChartSeries 完整类型结构**

**`ChartSeriesProjection` 接口定义：**
```typescript
interface ChartSeriesProjection {
  readonly fieldId: string;           // 字段唯一标识符
  readonly fieldName: string;          // 字段显示名称
  readonly points: readonly ChartPoint[];  // 数据点数组
}
```

**`ChartPoint` 接口定义：**
```typescript
interface ChartPoint {
  readonly timestamp: string;  // ISO时间戳
  readonly value: number;      // 数值
}
```

**字段特性：**
- 所有字段都是 `readonly`（不可变）
- `points` 是只读数组，包含时间序列数据
- `fieldId` 用于标识数据源（格式：`"groupId:dataItemId"`）
- `fieldName` 提供人类可读的字段名称

---

### **2. ChartDisplayPreference 完整字段列表**

**`ChartDisplayPreference` 接口定义：**
```typescript
interface ChartDisplayPreference {
  readonly selectedItems: readonly string[];  // 选中的字段ID列表
  readonly performance: ChartPerformancePreference;
}
```

**`ChartPerformancePreference` 契约定义：**
```typescript
interface ChartPerformancePreference {
  readonly maxPoints: number;           // 最大数据点数量
  readonly refreshIntervalMs: number;   // 刷新间隔（毫秒）
}
```

**字段特性：**
- `selectedItems`: 字符串数组，存储要显示的字段标识符
- `performance`: 嵌套对象，控制图表性能相关参数
- 所有字段都是 `readonly`

---

### **3. 所有 Display 相关 Type/Interface 汇总**

#### **3.1 基础类型**
```typescript
type DisplayMode = 'table' | 'chart' | 'special';
```

#### **3.2 偏好设置类型**

**TableDisplayPreference：**
```typescript
interface TableDisplayPreference {
  readonly displayMode: DisplayMode;
  readonly selectedGroupId: string;
  readonly selectedItems: readonly string[];
}
```

**ChartDisplayPreference：**
```typescript
interface ChartDisplayPreference {
  readonly selectedItems: readonly string[];
  readonly performance: ChartPerformancePreference;
}
```

**ScatterDisplayPreference：**
```typescript
interface ScatterDisplayPreference {
  readonly […]

> TOOL

tool_result
id: call_dad7ca705f0d4396af83a234
```
Based on my comprehensive search and analysis of the codebase, I've found extensive display-related design documentation. Let me provide you with a complete report of all findings:

## Display 设计文档调研报告

### 1. 发现的设计文档

我在 `codestable/features/rewrite-display/` 目录下找到了完整的 display 设计文档体系：

#### 核心设计文档
- **rewrite-display-design.md** - Display feature 核心设计文档
- **rewrite-display-checklist.yaml** - 实施检查清单
- **display-identity-brainstorm.md** - 数据身份标识统一讨论
- **rewrite-display-ui-brainstorm.md** - UI 页面层头脑风暴
- **rewrite-display-ui-design.md** - UI 页面层设计文档

### 2. Display 设计意图和目标

#### 核心职责
Display feature 的明确职责边界：
- **展示偏好语义**：table/chart/special/history display preference 语义
- **展示配置校验/规范化**：配置规范化结果、UI-safe display config snapshot
- **投影计算**：表格/图表/星座图 display projection
- **UI-safe snapshot**：实时/历史展示快照和展示刷新策略
- **transient display buffers**：为图表、表格服务的短生命周期 buffer

#### 明确不拥有的职责
- receive parse truth、connection transport truth
- status health summary、settings persisted truth
- storage/history persistence truth
- task lifecycle、result/report/northbound 语义

### 3. 已知扩展点和待办项

#### 关键扩展点
1. **多图表支持**：支持 1-4 个图表的布局配置
2. **三种显示模式**：table / chart / special (星座图)
3. **双面板布局**：table1 和 table2 独立配置
4. **实时刷新策略**：单一 rAF 循环统一刷新（替代多层定时器）
5. **历史分析**：HistoryPage 独立页面，支持历史数据查询和多图展示

#### 核心待办项
从 checklist 中识别的关键待办项：
- DISP-IMPL-001: 建立 display core 纯 TypeScript 规则
- DISP-IMPL-002: 建立 display service/state/selector
- DISP-IMPL-003: 收口 settings -> display 偏好边界
- DISP-IMPL-004: 收口 receive/frame -> display source 边界
- DISP-IMPL-005: 收口 storage/history -> display 边界
- DISP-TEST-001: 沉淀 display fixtures 和 oracle
- DISP-UI-001: 保留 display […]

> TOOL

tool_result
id: call_8cb063d23b874b65bdbb4dfb
```
Perfect! Now I have a complete understanding of the display feature. Let me compile a comprehensive report of my findings.

## Display Feature 完整调研报告

### 1. Display Service 完整操作面

**DisplayService 接口** (`/mnt/d/code/frontend/dongfanghong/rewrite/src/features/display/services/display-service.ts`)

#### Reader 方法 (只读操作)
- **getSnapshot()**: `ReadonlyDisplaySnapshot`
  - 返回当前完整状态的只读快照
  
- **getPreferences()**: `ReadonlyDisplayPreferences`
  - 返回当前用户偏好的只读副本
  
- **getTable1Rows()**: `TableRowProjection[]`
  - 返回表格1的行投影数据（已过滤和选择）
  
- **getTable2Rows()**: `TableRowProjection[]`
  - 返回表格2的行投影数据（已过滤和选择）
  
- **getChartSeries()**: `ChartSeriesProjection[]`
  - 返回图表系列投影数据（包含历史点）
  
- **getScatterProjection()**: `ScatterProjection`
  - 返回散点图投影数据（I/Q数据）
  
- **getAvailability()**: `DisplaySourceAvailability`
  - 返回数据源可用性状态

#### Writer 方法 (写操作)
- **updatePreferences(patch: DisplayPreferencesPatch)**: `DisplayOperationResult`
  - 更新用户偏好设置
  - 参数：偏好的部分更新对象
  - 返回：操作结果（包含成功状态、问题列表、新快照）
  
- **ingestSourceMaterial(material: DisplaySourceMaterial)**: `DisplayOperationResult`
  - 摄入源数据材料
  - 参数：包含字段和可用性的源数据
  - 返回：操作结果
  - **行为**：
    - 如果提供 `fields`，更新内部字段缓冲区
    - 如果提供 `availability`，更新可用性状态
    - 重新计算投影
  
- **clearProjection()**: `DisplayOperationResult`
  - 清空投影数据（保留偏好设置）
  - 返回：操作结果
  - **行为**：清空字段缓冲区和图表历史，保留偏好设置
  
- **reset()**: `DisplayOperationResult`
  - 重置到默认状态
  - 返回：操作结果
  - **行为**：清空所有数据，恢复默认偏好设置

### 2. Selector 投影列表

**所有 Selector** (`/mnt/d/code/frontend/dongfanghong/rewrite/src/features/display/selectors/display-selectors.ts`)

- **selectDisplaySnapshot(source)**: `DisplaySnapshot`
  - 返回完整快照的深拷贝
  
- **selectPreferences(source)**: `ReadonlyDisplayPreferences`
  - 返回偏好设置的深拷贝
  
- **selectTable1Rows(source)**: `TableRowProjection[]`
  - 返回表格1行投影的浅拷贝数组
  
- **selectTable2Rows(source)**: `TableRowProjection[]`
  - 返回表格2行投影的浅拷贝数组
  
- **selectChartSeries(source)**: `ChartSeriesProjection[]`
  - 返回图表系列投影，包含深拷贝的点数据
  
- **selectScatterProjection(source)**: `ScatterProjection`
  - 返回散点图投影，包含深拷贝的点数据
  
- **selectAvailability(source)**: `DisplaySourceAvailability`
  - 返回数据源可用性状态的浅拷贝

### 3. Composable 列表和功能

**useDisplayRefresh** (`/mnt/d/code/frontend/dongfanghong/rewrite/src/features/display/composables/use-display-refresh.ts`)

**参数**：
- `service: DisplayService` - 显示服务实例
- `cadenceMs: number = 200` - 刷新间隔（毫秒）

**返回值**：`DisplayRefreshState & { start: () => void; stop: () => void }` […]

> AGENT

Batch 1 完成。关键发现：
- 当前 display 是**单图表多系列**架构，需要扩展为多图表实例
- 设计文档已有完整的多图表规划（1-4 图表、独立配置）
- storage→display 转换函数 `storageRecordsToDisplayMaterials()` 已在设计中

启动 Batch 2（3 agent 并行）：B4 旧系统多图表模型、B5 旧系统数据项选择、B6 旧系统时间选择+CSV导出。

> TOOL

tool_use Agent
id: call_e2312a7fef994b4cb7d8a8ca
```json
{
  "description": "B4 old system multi-chart model",
  "prompt": "只读调研，不写代码。彻底调研旧系统多图表模型：\n\n1. `src/stores/historyAnalysis.ts` — 重点关注：\n   - 行 45-55：图表配置结构（chartCount/charts[]）\n   - 行 109-153：图表数据计算逻辑\n   - 行 280-362：图表操作方法\n\n产出：\n- 多图表类型完整结构（chartCount 怎么控制、charts[] 每个元素有什么字段）\n- 每个图表的配置项（title/dataItems/yAxis 等）\n- 图表数量变更时的行为（增加/减少图表）\n- 图表配置操作方法签名和行为\n- 数据如何分配到多个图表\n\n请完整输出所有发现，不要省略字段。",
  "subagent_type": "Explore"
}
```

> TOOL

tool_use Agent
id: call_9372b9d6428a4202a36d7ef7
```json
{
  "description": "B5 old system data item selection",
  "prompt": "只读调研，不写代码。彻底调研旧系统数据项选择模型：\n\n1. `src/stores/historyAnalysis.ts` — 重点关注行 232-278：数据项选择\n2. `src/components/storage/HistoryDataSelector.vue` — 数据项选择器组件\n\n产出：\n- 分组/数据项元数据结构（groupId/groupName/dataItemId/dataItemName/dataType 等）\n- 选择操作方法（全选、取消、按组选择等）\n- 数据项与图表的关联方式\n- 搜索/过滤功能\n- HistoryDataSelector 组件的 props/events/交互模式\n\n请完整输出所有发现。",
  "subagent_type": "Explore"
}
```

> TOOL

tool_use Agent
id: call_78f33f8529fe49c7937e4b05
```json
{
  "description": "B6 old system time + CSV export",
  "prompt": "只读调研，不写代码。彻底调研旧系统时间选择和 CSV 导出功能：\n\n1. `src/components/storage/HistoryTimeSelector.vue` — 时间选择器\n2. `src/components/storage/CSVExportDialog.vue` — CSV 导出对话框\n3. `src/stores/historyAnalysis.ts` — 行 364-386：导出逻辑\n\n产出：\n- 时间选择交互模式（日期选择、时间范围、快捷选项）\n- CSV 导出配置项（文件名、分隔符、编码、字段选择等）\n- 导出操作流程（选择范围 → 预览 → 导出）\n- 数据格式化规则（时间格式、数字格式、空值处理）\n\n请完整输出所有发现。",
  "subagent_type": "Explore"
}
```

> TOOL

tool_result
id: call_e2312a7fef994b4cb7d8a8ca
```
基于彻底调研，现在我可以完整输出旧系统多图表模型的完整发现：

## 旧系统多图表模型完整调研报告

### 1. 多图表类型完整结构

#### 核心数据结构
**位置**: `/mnt/d/code/frontend/dongfanghong/src/stores/historyAnalysis.ts` (行 45-55)

```typescript
// 多图表配置（持久化存储）
const multiChartSettings = useStorage<MultiChartSettings>('historyAnalysis_chartSettings', {
  chartCount: 1,
  charts: [
    {
      id: 1,
      title: '图表1',
      selectedDataItems: [],
    },
  ],
});
```

**类型定义** (位置: `/mnt/d/code/frontend/dongfanghong/src/types/storage/historyData.ts`):

```typescript
// 多图表设置接口
interface MultiChartSettings {
  chartCount: number;        // 图表数量 (1-4)
  charts: ChartConfig[];     // 图表配置列表
}

// 图表配置接口
interface ChartConfig {
  id: number;                // 图表ID (从1开始)
  title: string;             // 图表标题
  selectedDataItems: Array<{
    groupId: number;         // 分组ID
    dataItemId: number;      // 数据项ID  
    label: string;           // 显示标签
    color: string;           // 线条颜色
  }>;
  yAxisConfig?: YAxisConfig; // Y轴配置 (可选)
}

// Y轴配置接口
interface YAxisConfig {
  autoScale: boolean;        // 是否自动缩放
  min?: number;              // 最小值 (手动模式)
  max?: number;              // 最大值 (手动模式)
  enableStatistics?: boolean;        // 是否启用统计计算
  statisticsItems?: number[];        // 参与统计计算的数据项ID列表
  statisticsTimeWindow?: number;     // 统计计算时间窗口（秒），默认60秒
}
```

#### chartCount 控制机制
- **取值范围**: 1-4 个图表
- **控制方式**: 通过UI按钮选择 1/2/3/4，调用 `updateChartCount(count)` 方法
- **持久化**: 使用 `useStorage` 存储在 localStorage，键名为 `'historyAnalysis_chartSettings'`
- **默认值**: chartCount = 1，包含一个空图表配置

### 2. 每个图表的配置项详解

#### 2.1 基础配置项
```typescript
{
  id: number;           // 图表唯一标识，从1开始递增
  title: string;        // 图表显示标题，如 "图表1"、"图表2"
  selectedDataItems: Array<{
    groupId: number;       // 数据所属分组ID
    dataItemId: number;    // 数据项ID
    label: string;         // 显示标签，格式 "组名 - 数据项名"
    color: string;         // 线条颜色，十六进制颜色码
  }>;
}
```

#### 2.2 Y轴配置项 (yAxisConfig […]

> TOOL

tool_result
id: call_78f33f8529fe49c7937e4b05
```
基于我对代码的彻底调研，现在我可以提供完整的分析报告。让我整理所有发现：

## 旧系统时间选择和CSV导出功能完整调研报告

### 1. 时间选择交互模式 (`HistoryTimeSelector.vue`)

#### 1.1 日期选择
- **分离式输入控件**：日期和时间分别使用独立的输入框
  - `startDate` / `endDate`：HTML5 `type="date"` 输入框
  - `startTime` / `endTime`：HTML5 `type="time"` 输入框
- **日期范围限制**：基于实际可用数据 (`availableDateRange.min/max`)
- **时区处理**：使用本地时间避免时区问题

#### 1.2 时间范围
- **最大跨度限制**：30天（硬编码验证）
- **实时验证**：
  - 开始时间必须早于结束时间
  - 防抖处理（1秒）避免频繁更新
- **双向同步**：输入框变更自动更新Store，Store变更自动同步到输入框

#### 1.3 快捷选项
```javascript
const presetRanges = [
  { label: '最近1小时', hours: 1 },
  { label: '最近6小时', hours: 6 },
  { label: '最近12小时', hours: 12 },
  { label: '最近24小时', hours: 24 },
];
```
- 一键设置时间范围
- 按钮显示简化标签（去除"最近"前缀）
- 自动同步输入框显示

### 2. CSV导出配置项 (`CSVExportDialog.vue`)

#### 2.1 文件配置
- **文件名**：
  - 默认值：`history_data`
  - 自动生成建议文件名：`history_data_YYYYMMDD_HHMMSS`
  - 手动编辑支持
  
- **输出路径选项**：
  - **预设路径**：使用 `settings.csvDefaultOutputPath`（默认空值时显示 `data/exports/csv`）
  - **手动选择**：触发系统保存对话框

#### 2.2 内容配置
```javascript
// 基本选项
const includeHeaders = ref(true);      // 包含表头
const includeTimestamp = ref(true);    // 包含时间戳
const usePresetPath = ref(true);       // 使用预设路径

// 时间格式选项
const dateFormatOptions = [
  { label: 'YYYY-MM-DD HH:mm:ss', value: 'YYYY-MM-DD HH:mm:ss' },
  { label: 'YYYY/MM/DD HH:mm:ss', value: 'YYYY/MM/DD HH:mm:ss' },
  { label: 'MM/DD/YYYY HH:mm:ss', value: 'MM/DD/YYYY HH:mm:ss' },
  { label: 'DD.MM.YYYY HH:mm:ss', value: 'DD.MM.YYYY HH:mm:ss' },
  { label: 'ISO 8601', value: 'ISO' },
  { label: 'Unix 时间戳', value: 'UNIX' },
];
```

#### 2.3 字段选择
- 基于 `dataItemSelections`（数据项选择状态）
- 显示选中数据项的标签（分组名 - 数据项名）
- 预览选中的数据项列表

#### […]

> TOOL

tool_result
id: call_9372b9d6428a4202a36d7ef7
```
基于我的彻底调研，现在可以提供完整的发现报告。

## 旧系统数据项选择模型调研报告

### 1. 分组/数据项元数据结构

#### 核心类型定义
```typescript
// 数据项元数据
interface DataItemMetadata {
  id: number;              // 数据项ID
  label: string;           // 数据项标签
  dataType: FieldType;     // 数据类型（uint8, int8, uint16, float等）
  groupId: number;         // 所属分组ID
  index: number;           // 在data数组中的索引位置
}

// 分组元数据
interface GroupMetadata {
  id: number;              // 分组ID
  label: string;           // 分组标签
  dataItems: DataItemMetadata[];  // 数据项列表
}

// 数据项选择状态
interface DataItemSelection {
  groupId: number;         // 分组ID
  dataItemId: number;      // 数据项ID
  selected: boolean;       // 是否选中
  visible: boolean;        // 是否可见（用于搜索过滤）
}

// 图表数据项配置
interface ChartDataItem {
  groupId: number;         // 分组ID
  dataItemId: number;      // 数据项ID
  label: string;           // 显示标签
  color: string;           // 线条颜色
}
```

#### 数据类型选项
系统支持11种数据类型：
- **整数类型**: `uint8`, `int8`, `uint16`, `int16`, `uint32`, `int32`, `uint64`, `int64`
- **浮点类型**: `float`, `double`
- **其他类型**: `bytes`

### 2. 选择操作方法

#### Store中的核心方法 (`historyAnalysis.ts` 第232-278行)

```typescript
// 初始化数据项选择状态
initDataItemSelections(): void
// 从loadedMetadata构建初始选择状态，默认全部未选中

// 更新单个数据项选择状态
updateDataItemSelection(groupId: number, dataItemId: number, selected: boolean): void

// 分组级别的选择操作
toggleGroupSelection(groupId: number, selected: boolean): void
// true: 全选分组内所有项
// false: 取消分组内所有项

// 清空所有选择
clearAllSelections(): void
```

#### 组件中的UI操作方法 (`HistoryDataSelector.vue`)

```typescript
// 切换单个数据项
toggleDataItemSelection(groupId: number, dataItemId: number): void

// 切换分组选择（智能判断全选/取消）
toggleGroupSelection(groupId: number): void
// 如果已全选则取消，否则全选

// 批量操作
selectAllVisible(): void        // 全选所有搜索过滤后的项
clearAllSelections(): void      // 清空所有选择

// 展开状态管理
toggleGroupExpanded(groupId: number): void
``` […]

> AGENT

Batch 2 完成。关键发现：
- 旧系统多图表：`MultiChartSettings { chartCount: 1-4, charts: ChartConfig[] }`，每个图表独立配置（title/selectedDataItems/yAxisConfig）
- 数据项选择：双层选择（左侧全局选择 + 图表独立选择），分组折叠 + 搜索
- CSV 导出：时间范围选择（预设+自定义），UTF-8 逗号分隔，字段选择

启动 Batch 3（3 agent 并行）：B7 storage 数据层、B8 集测行为基线、B9 UI 规范+现有组件。

> TOOL

tool_use Agent
id: call_2a0f53d9feec4b90b1214737
```json
{
  "description": "B7 storage data layer for history",
  "prompt": "只读调研，不写代码。彻底调研 storage 数据层对历史分析的支撑：\n\n1. rewrite/src/features/storage-local-baseline/core/types.ts — 完整类型定义\n2. rewrite/src/features/storage-local-baseline/core/history.ts — 历史数据操作\n3. rewrite/src/features/storage-local-baseline/services/storage-local-service.ts — service API\n\n产出：\n- storage 完整类型结构（StorageLocalRecord 等）\n- 历史数据相关 API 签名（query/append/list/cleanup/CSV 等）\n- storage 的 groupId/dataItemId 模型 vs display 的 frameId/fieldId 模型\n- identity 映射需求（channel+key → frameId+fieldId）\n- 哪些历史分析需求已被 storage API 覆盖\n- 哪些还缺失\n\n请完整输出所有发现。",
  "subagent_type": "Explore"
}
```

> TOOL

tool_use Agent
id: call_ad393df6afba40b58ae26f94
```json
{
  "description": "B8 integration test baseline history",
  "prompt": "只读调研，不写代码。读取集测行为基线中历史/CSV 相关的行为定义：\n\n1. .sessions/2026-05-19-integration-testing/S004-legacy-observable-behaviors.md — 找到 §2.9（历史/CSV 8 项行为）\n\n产出：\n- 8 项行为的完整列表（编号、行为描述）\n- 每项行为逐一标注新系统覆盖情况（已覆盖/部分覆盖/未覆盖）\n- 覆盖 gap 分析\n\n请完整输出所有发现。",
  "subagent_type": "Explore"
}
```

> TOOL

tool_use Agent
id: call_d4a50da2b777460ebfc40cc0
```json
{
  "description": "B9 UI conventions + chart widgets",
  "prompt": "只读调研，不写代码。调研 UI 规范和现有图表组件：\n\n1. codestable/quality/rewrite-frontend-conventions.md — 前端 UI 规范要点（表格、表单、弹窗、布局、颜色）\n2. codestable/reference/rewrite-frontend-quickref.md — 前端速查卡（shared/ API 索引 + 语义 class + 高频违规清单 + 新页面检查清单）\n3. rewrite/src/widgets/WaveformChart.vue — 波形图组件\n4. rewrite/src/widgets/ScatterChart.vue — 星座图组件（如存在）\n\n产出：\n- 图表组件的 props/events/slots（完整签名）\n- 图表组件可复用能力评估\n- UI 规范中与历史分析页相关的要点（布局模式、颜色 token、表格规范）\n- 速查卡中的新页面检查清单\n- 高频违规清单\n\n请完整输出所有发现。",
  "subagent_type": "Explore"
}
```

> TOOL

tool_result
id: call_d4a50da2b777460ebfc40cc0
```
## UI 规范和图表组件调研报告

---

### 一、图表组件完整签名

#### 1. WaveformChart.vue（波形图）

**路径**: `/mnt/d/code/frontend/dongfanghong/rewrite/src/widgets/WaveformChart.vue`

```typescript
interface ChartSeriesProjection {
  fieldName: string;
  points: Array<{ timestamp: string; value: number }>;
}

interface WaveformChartProps {
  series: ChartSeriesProjection[];  // 多系列波形数据
  loading?: boolean;                // 加载状态
  height?: string;                  // 图表高度，默认 '300px'
}
```

**Props**:
- `series` — 多系列波形数据，每个系列包含字段名和点数组
- `loading` — 可选，加载状态标识
- `height` — 可选，图表高度（默认 '300px'）

**Events**: 无

**Slots**: 无

**特性**:
- 使用 ECharts LineChart
- 内置 dataZoom 缩放
- 自动图例（series > 1 时显示）
- 固定色板循环
- ResizeObserver 自适应

---

#### 2. ScatterChart.vue（星座图）

**路径**: `/mnt/d/code/frontend/dongfanghong/rewrite/src/widgets/ScatterChart.vue`

```typescript
interface ScatterProjection {
  points: Array<{ i: number; q: number }>;
}

interface ScatterChartProps {
  data: ScatterProjection;          // IQ 星座点数据
  loading?: boolean;                // 加载状态
  height?: string;                  // 图表高度，默认 '300px'
}
```

**Props**:
- `data` — IQ 星座点数据数组
- `loading` — 可选，加载状态标识
- `height` — 可选，图表高度（默认 '300px'）

**Events**: 无

**Slots**: 无

**特性**:
- 使用 ECharts ScatterChart
- 内置 tooltip 显示 I/Q 值（4 位小数）
- 固定蓝色点（`#1f6feb`）
- 虚线网格
- ResizeObserver 自适应

---

### 二、图表组件可复用能力评估

| 维度 | WaveformChart | ScatterChart | 评价 |
|------|--------------|--------------|------|
| **通用性** | 中 | 低 | Waveform 支持多系列泛化，Scatter 硬编码 IQ 语义 |
| **配置灵活性** | 低 | 低 | 颜色、符号大小、网格等均硬编码 |
| **事件扩展** | 无 | 无 […]

> TOOL

tool_result
id: call_2a0f53d9feec4b90b1214737
```
基于对代码的全面调研，现在让我输出完整的分析报告：

## Storage 数据层历史分析支撑调研报告

### 1. Storage 完整类型结构

#### 核心类型定义 (`rewrite/src/features/storage-local-baseline/core/types.ts`)

**StorageLocalRecord** - 本地记录基础类型：
```typescript
interface StorageLocalRecord {
  readonly id: string;              // 记录唯一标识
  readonly capturedAt: string;      // 捕获时间 (ISO 8601格式)
  readonly source: StorageLocalRecordSource; // 来源：'local' | 'legacy' | 'manual'
  readonly channel: string;         // 通道标识 (对应 receive.source.sourceId)
  readonly fields: readonly StorageRecordField[]; // 字段数组
  readonly note?: string;           // 可选备注
}

interface StorageRecordField {
  readonly key: string;             // 字段键名 (对应 frame.fieldName)
  readonly value: StorageRecordFieldValue; // 字段值：string | number | boolean | null
  readonly unit?: string;           // 可选单位
}
```

**StorageHistoryMaterial** - 历史材料容器：
```typescript
interface StorageHistoryMaterial {
  readonly hourKey: string;         // 小时键：YYYY-MM-DDTHH
  readonly source: StorageLocalRecordSource;
  readonly records: readonly StorageLocalRecord[];
}
```

**StorageCsvMaterial** - CSV 导出材料：
```typescript
interface StorageCsvMaterial {
  readonly id: string;              // CSV文件ID
  readonly name: string;            // CSV文件名
  readonly generatedAt: string;     // 生成时间
  readonly columns: readonly StorageCsvColumn[]; // 列定义
  readonly recordCount: number;     // 记录数量
  readonly content: string;         // CSV内容字符串
}

interface StorageCsvColumn {
  readonly key: string;             // 列键名 (对应 field.key)
  readonly label: string;           // 列显示名称
}
```

**状态快照** (`rewrite/src/features/storage-local-baseline/state/storage-state.ts`)：
```typescript
interface StorageStateSnapshot {
  readonly records: readonly ReadonlyStorageLocalRecord[];        // 当前加载的记录
  readonly historyMaterials: readonly ReadonlyStorageHistoryMaterial[]; // 历史材料
  readonly csvMaterials: readonly ReadonlyStorageCsvMaterial[];   // CSV材料
  readonly legacyMaterials: readonly ReadonlyStorageLegacyJsonMaterial[]; // 旧材料
  readonly lastIssue?: […]

> TOOL

tool_result
id: call_ad393df6afba40b58ae26f94
```
基于我对旧系统行为定义和新系统代码的调研，现在让我整理完整的历史/CSV行为覆盖分析报告：

## 集测行为基线调研报告：历史/CSV 相关行为

### 1. 8 项历史/CSV 行为完整列表

根据 `.sessions/2026-05-19-integration-testing/S004-legacy-observable-behaviors.md` §2.9（存储/历史/高速存储）以及 `S004-agent5-storage-history-csv.md` 的详细分析，历史/CSV 相关的核心行为如下：

#### **1.1 历史数据存储行为（6 项）**

**H-01：JSON 文件按小时存储历史数据**
- 行为描述：历史数据存储为 JSON 文件，路径 `{userDataPath}/data/history-statistics/{hourKey}.json`，hourKey 格式 `YYYY-MM-DD-HH`（如 `2026-05-19-14`），支持 gzip 压缩（`.json.gz`）
- 代码位置：`src-electron/main/ipc/historyDataHandlers.ts:34-52`
- 新系统对应：storage feature
- Oracle 评估：代码完整，行为明确

**H-02：HourlyDataFile 结构（分组元数据+时间序列）**
- 行为描述：每个小时文件包含 `metadata`（版本、小时键、分组元数据、记录数、时间戳）和 `records`（时间序列记录数组）
- 代码位置：`src/types/storage/historyData.ts:8-40`
- 新系统对应：storage feature
- Oracle 评估：代码完整

**H-03：增量追加记录到小时文件**
- 行为描述：支持通过 `appendBatchRecords` 增量追加记录到已有小时文件，更新 `updatedAt` 时间戳
- 代码位置：`src-electron/main/ipc/historyDataHandlers.ts:102-157`
- 新系统对应：storage feature 写入 API
- Oracle 评估：代码完整

**H-04：定时收集（1s）+ 定期持久化（5min）+ 小时边界切换**
- 行为描述：数据收集定时器（1s）、历史数据保存定时器（5min）、小时边界自动切换、停止记录时保存未保存数据
- 代码位置：`src/stores/frames/dataDisplayStore.ts:554-630`
- 新系统对应：receive-real + storage feature 协作
- Oracle 评估：代码完整

**H-05：自动开始记录（可配置）**
- 行为描述：应用启动时如果 `settingsStore.autoStartRecording` 为 true（默认 true），自动调用 `dataDisplayStore.startRecording()`
- 代码位置：`src/layouts/useAppLifecycle.ts:65-68`
- 新系统对应：app lifecycle + receive feature
- Oracle 评估：代码完整

**H-06：循环缓冲区 + 动态容量 + 时间过期清理**
- 行为描述：循环缓冲区按 groupId 索引，容量根据活跃图表数动态调整（0 图表=1000，1 图表=5000，2 图表=3000），每 10 秒检查，每小时移除超过 `maxHistoryHours`（默认 24 小时）的旧记录
- 代码位置：`src/stores/frames/dataDisplayStore.ts:51-115, 247-274`
- 新系统对应：storage + visualization feature
- Oracle 评估：代码完整，性能优化策略清晰

#### **1.2 CSV 导出行为（2 项）**

**C-01：CSV 导出配置（文件名/时间范围/数据项选择/表头/时间戳/预设路径）**
- 行为描述：CSV 导出通过 `CSVExportDialog` 组件触发，支持配置文件名、时间范围、选中数据项、包含表头、包含时间戳、预设路径、6 种时间格式选项
- 代码位置：`src/components/storage/CSVExportDialog.vue:1-401`、`src/types/storage/historyData.ts:115-131`
- 新系统对应：storage feature 导出 + UI 页面
- Oracle 评估：代码完整，UI 交互完整

**C-02：CSV 格式：逗号分隔、UTF-8、{group}_{item} 表头、ISO 时间戳**
- 行为描述：分隔符为逗号，编码为 UTF-8，表头格式为 `timestamp` 或 `{groupLabel}_{dataItemLabel}`，时间戳格式为 `YYYY-MM-DD HH:MM:SS`，每行按选中数据项的 metadata index 取值
- 代码位置：`src-electron/main/ipc/historyDataHandlers.ts:305-474`
- 新系统对应：storage feature 导出
- Oracle 评估：代码完整，格式逻辑清晰

---

### 2. 新系统覆盖情况分析

#### **2.1 已覆盖行为（4 项）**

✅ **H-05：自动开始记录** - **已覆盖**
- […]

> AGENT

## Wave 1 全部完成（9/9 agent）

### 事实汇总

| 维度 | 关键发现 |
|------|---------|
| Display 类型 | **单图表架构**：`chartSeries: ChartSeriesProjection[]`、`preferences.chart` 是单一对象，无多图表支持 |
| Display 设计文档 | 已有完整多图表设计规划：1-4 图表、独立配置、QBtnToggle、ChartWidget 纯 props |
| 旧系统多图表 | `MultiChartSettings { chartCount: 1-4, charts: ChartConfig[] }`，每个图表独立 selectedDataItems + yAxisConfig |
| 旧系统数据项 | 双层选择（全局选择 + 图表独立选择），分组折叠 + 搜索，11 种数据类型 |
| Storage 数据层 | API 覆盖 ~70% 历史分析需求，**关键缺失**：channel+key → frameId+fieldId 映射层 |
| 集测基线 | 8 项行为：4 已覆盖、2 部分覆盖、2 未覆盖（循环缓冲区、CSV UI） |
| UI 组件 | WaveformChart/ScatterChart 可直接复用，语义 class 体系完备 |

---

## Wave 2: 设计

### 核心设计决策

**DC1: 多图表类型扩展**

```
当前：preferences.chart: ChartDisplayPreference (单一)
     projection.chartSeries: ChartSeriesProjection[] (单一图表的多系列)

目标：preferences.charts: ChartInstancePreference[] (1-4 个)
     projection.charts: ChartInstanceProjection[] (1-4 个投影)
```

这是对 display feature 的**类型级扩展**。DisplayPage 当前是 skeleton，改 type 不会破坏已有功能。

**DC2: 元数据注册表归属**

- 数据项元数据来自 frame 定义（receive/frame feature 的 public API）
- display feature 消费 frame 定义的 `frameId + fieldId + fieldName`
- 不在 display 或 storage 中新建"元数据注册表"——复用 frame 定义的公共读取模型
- 历史页选择器通过 frame feature 的 selector 获取可用数据项列表

**DC3: Storage→Display 转换层**

- 新建 `storage-display-bridge.ts`（纯函数）
- `storageRecordsToDisplayMaterials(records, frameDefinitions) → DisplaySourceMaterial`
- 映射：channel → frameId（通过 frame 定义查找）、field.key → fieldId

**DC4: Y轴配置归属 display preferences**

- 每个 ChartInstancePreference 包含可选 yAxisConfig
- 统计功能（mean/RMSE）在 UI 组件 computed 中计算，不占 display state

**DC5: 颜色策略**

- 固定 6 色 CSS token，确定性分配（按 fieldId hash） […]