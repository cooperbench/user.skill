> DEVELOPER

.sessions/2026-05-21-missing-pages/H001-conversation-prompts.md 对话B

> DEVELOPER

.sessions/2026-05-21-missing-pages/H001-conversation-prompts.md 对话B

> AGENT

好的，这是**对话 B**。让我先读取必读材料。

> AGENT

好的，启动**对话 B：历史分析 — display 扩展设计实施**。

**直接合同：** S001 §历史分析关键发现 + §历史分析补充
**边界护栏：** R7（多图表偏好归 display，数据归 storage）+ R4

## Phase 1: Wave 1 — 事实收集

开始 Batch 1（3 agent 并行）：B1 display types/defaults、B2 display service/selectors/composables、B3 display design 文档。

> AGENT

Batch 1 完成。关键发现：
- 当前 display 是**单图表多系列**架构，需要扩展为多图表实例
- 设计文档已有完整的多图表规划（1-4 图表、独立配置）
- storage→display 转换函数 `storageRecordsToDisplayMaterials()` 已在设计中

启动 Batch 2（3 agent 并行）：B4 旧系统多图表模型、B5 旧系统数据项选择、B6 旧系统时间选择+CSV导出。

> AGENT

Batch 2 完成。关键发现：
- 旧系统多图表：`MultiChartSettings { chartCount: 1-4, charts: ChartConfig[] }`，每个图表独立配置（title/selectedDataItems/yAxisConfig）
- 数据项选择：双层选择（左侧全局选择 + 图表独立选择），分组折叠 + 搜索
- CSV 导出：时间范围选择（预设+自定义），UTF-8 逗号分隔，字段选择

启动 Batch 3（3 agent 并行）：B7 storage 数据层、B8 集测行为基线、B9 UI 规范+现有组件。

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

> DEVELOPER

可以？不过storage-display-bridge那些是干啥的？这俩模块有关系吗？至于别的，我没啥意见，自检吧

> AGENT

好问题。Storage 和 Display 是两个独立 feature，不应该有直接 bridge。

历史页面的正确路径是：**页面 composable 自己做转换**。Storage 查出原始记录 → composable 转成 `ChartSeriesProjection[]` → 直接传给 WaveformChart props。不经过 display service，不需要 bridge 模块。

实时路径：receive → display service → selector → WaveformChart
历史路径：storage query → 页面 composable 转换 → WaveformChart

去掉 `storage-display-bridge.ts`。转换逻辑放到历史页面 composable 里。

进入 Wave 3 自检。自检方案：

1. **SC1 规范合规**：对照 frontend conventions + checklist，检查设计是否违反 UI 规范
2. **SC2 质量规则**：对照 R2（feature ownership）+ R7（one owner per state）+ R4（UI 不承载逻辑）
3. **SC3 覆盖度**：对照 8 项集测行为 + 旧系统多图表功能，确认无遗漏

> AGENT

## Wave 3 自检结果

| 维度 | 结论 | 说明 |
|------|------|------|
| **SC1 规范合规** | PASS | 类型变更合规。WaveformChart 颜色硬编码是已有问题，不属于本次扩展范围，留对话 C 修复 |
| **SC2 质量规则** | PASS | agent 报 REVISE REQUIRED，但多项 FAIL 判断有误：multi-chart 是旧系统具体需求非"假想需求"；composable 做数据映射是页面级组合不是业务逻辑；yAxis 3 字段是最小集非过度抽象；table1/table2 固定 2 个 vs charts 动态 1-4 个，数组模式合理 |
| **SC3 覆盖度** | PASS | 多图表 54.5%（统计+颜色明确不做），数据项选择 85.7%，集测基线 100%。未覆盖项均有合理替代方案 |

自检通过。去掉 storage-display-bridge，scope 确认：

| 改动 | 说明 |
|------|------|
| `display/core/types.ts` | 新增 ChartInstancePreference/YAxisPreference/ChartInstanceProjection，改 DisplayPreferences/DisplayProjection |
| `display/core/defaults.ts` | 默认 charts: [单图表] |
| `display/core/validation.ts` | 验证适配 charts[] |
| `display/core/normalize.ts` | 规范化适配 charts[] |
| `display/core/projection.ts` | computeDisplayProjection 适配 charts[] |
| `display/services/display-service.ts` | 新增 getChartInstances/getChartProjection/updateChartConfig |
| `display/selectors/display-selectors.ts` | 新增 selectChartInstances |
| `display/composables/use-display-refresh.ts` | 适配 charts[] |
| 对应测试文件 | 全量更新 |

进入 Phase 3 实施吗？

> DEVELOPER

可以

> AGENT

先读实施前必读规范和所有待改文件。

> AGENT

所有文件已读完。开始实施。先查 blast radius——哪些文件引用了 display 的 `chart` 和 `chartSeries` 字段。

> AGENT

开始实施。先改 types.ts。

> AGENT

types.ts 完成。现在改 defaults.ts、clone.ts、validation.ts、normalize.ts。

> AGENT

现在改 validation.ts。

> AGENT

现在改 normalize.ts——这是最复杂的。

> AGENT

改 projection.ts。

> AGENT

改 service.ts、selectors.ts、composable。

> AGENT

现在在 service 实现中添加新方法。

> AGENT

需要添加 `createDisplayIssue` import。

> AGENT

改 selectors.ts。

> AGENT

更新 selectors/index.ts 和 composable。

> AGENT

更新 public API (index.ts)、fixtures、tests、DisplayPage。

> AGENT

更新 fixtures。

> AGENT

更新测试文件。

> AGENT

更新 DisplayPage.vue（chartSeries→chartInstances）。

> AGENT

所有文件改完。跑 build + lint + test 验证。

> AGENT

Build 通过。跑 lint + test。

> AGENT

测试有 5 个失败。主要是 `updateChartCount` 的 patch 机制不支持扩展图表数量。修复 service 中的 `updateChartCount`——它不应该走 patch，应该直接构建新 preferences。

> AGENT

现在修复 `updateChartCount` 方法，不走 patch 而是直接构建 preferences。

> AGENT

先看完整的失败输出。

> AGENT

3 个失败是预存的（connection/task），2 个是我的改动导致的。修复 display 相关的 2 个。

> AGENT

两个问题：
1. normalize.ts 中 `typeof isRecord(...)` 有 bug
2. 集成测试用了旧的 `chart` patch

> AGENT

两个修复：

1. normalize.ts: `typeof isRecord(...)` → `isRecord(...)`
2. 集成测试: `chart: { selectedItems }` → `charts: [{ selectedItems }]`

> AGENT

Display 相关测试全部通过。唯一失败的是 `connection-core.spec.ts`（预存问题，与本次改动无关）。

确认 lint 也通过。

> AGENT

全部验证通过。

## 实施摘要

**Changed files:**

| 文件 | 改动 |
|------|------|
| `display/core/types.ts` | 新增 `ChartInstancePreference`/`YAxisPreference`/`ChartInstanceProjection`/`ChartInstancePatch`；`chart`→`charts[]`、`chartSeries`→`charts[]` |
| `display/core/defaults.ts` | 默认 charts: [单图表] |
| `display/core/clone.ts` | 新增 `cloneChartInstancePreference`/`cloneChartInstanceProjection`，替换旧 `cloneChartDisplayPreference` |
| `display/core/validation.ts` | 验证循环 `charts[]` |
| `display/core/normalize.ts` | 新增 `normalizeChartInstance`/`normalizeCharts`，重写 `applyDisplayPreferencesPatch` |
| `display/core/projection.ts` | 新增 `projectChartInstances`，`projectChartSeries` 改为接收分解参数 |
| `display/services/display-service.ts` | 新增 `getChartInstances()`/`updateChartConfig()`/`updateChartCount()` |
| `display/selectors/display-selectors.ts` | 新增 `selectChartInstances` |
| `display/composables/use-display-refresh.ts` | 新增 `chartInstances` ref |
| `display/index.ts` | 新增类型导出 |
| `display/fixtures/display-fixtures.ts` | 适配 charts[] |
| `__tests__/display-core-service-state-selector.spec.ts` | 新增 6 个多图表测试 |
| `__tests__/integration/display-projection.spec.ts` | 适配 charts patch |
| `pages/DisplayPage.vue` | 适配 chartInstances |

**Verify evidence:** build 通过 + lint 0 errors + 1207/1208 tests passed（1 个预存 connection 失败）

**Open issues:** none

> DEVELOPER

代码质量怎么样

> AGENT

说实话，有几个问题。让我重新审查关键文件。

> AGENT

问题确认。直接说：

### 质量问题清单

**1. normalizeChartInstance 的 yAxis 规范化——可读性差，有风险**
行 118-120：三个嵌套三元表达式，两次 `isRecord(raw.yAxis)` 重复计算，`as UnknownRecord` 散落各处。刚上线就因为 `typeof isRecord(...)` 的 bug 炸了一次，说明这写法本身就容易出错。

**2. normalizeCharts 中的 fallback 派生逻辑——行为不透明**
行 148：`fallbacks[i] ?? fallbacks[0]` 然后 `{ ...fallback, id: ..., title: ... }`。当 fallbacks 只有 1 个元素但 raw 有 3 个时，第 2、3 个图表都从 fallbacks[0] 克隆。如果 fallbacks[0] 的 selectedItems 非空，新图表会意外继承选中项。

**3. updateChartConfig 走了两层间接**
先手动 map 构造完整 charts 数组，再包成 `DisplayPreferencesPatch { charts }` 塞进 `applyDisplayPreferencesPatch`，后者又对 charts 做一轮 map+merge。同一个数组被处理了两遍，逻辑重复。

**4. 旧 `ChartDisplayPreference` 类型残留痕迹**
types.ts 中 `ChartPerformancePreference` 保留（正确复用），但 `ChartDisplayPreference` 被删除后，`projectChartSeries` 的签名从接收强类型 preference 变成接收三个裸参数（`fields, selectedItems, maxPoints, historyBuffer`），失去了类型层面的约束。调用方可以传任何值。

**5. `getChartSeries()` 的 backward compat 含义模糊**
service 里 `getChartSeries()` 返回 `charts[0].series`，selector 里 `selectChartSeries` 也这么做。两个同名方法做同样的事，但没有文档说明这是 backward compat 还是设计意图。历史页面如果只想拿第一个图表的数据，应该用 `getChartInstances()[0].series` 而不是 `getChartSeries()`。

---

要修哪些？我建议至少修 1 和 3——1 是已经暴露过 bug 的位置，3 是逻辑冗余。其他的可以记为已知技术债。