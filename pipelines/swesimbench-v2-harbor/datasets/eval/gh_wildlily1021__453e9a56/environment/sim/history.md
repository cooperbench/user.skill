[DEVELOPER]: .sessions/2026-05-21-missing-pages/H001-conversation-prompts.md 对话DP

[AGENT]: 好，对话 DP 是实时显示页 UX 重做。我先读取必读文档和事实材料。

[AGENT]: 旧系统 display 组件路径不同。让我查找旧系统相关文件。

[AGENT]: 让我继续读取旧系统 UI 组件和新系统 display feature。

[AGENT]: 事实收集进展顺利。继续读取必读规范和 receive feature API。

[AGENT]: Wave 1 事实收集完成。汇总关键发现。 --- ## Wave 1 事实汇总 ### 新系统 DisplayPage 现状（277 行，旧系统 ~15%） - 统计栏 + 两 tab（数据总览 / 可视化） - 总览：字段值表 + 帧匹配统计表 + 最近输入表 - 可视化：单波形图 + 单星座图 - 数据来源：receive service 直接查 + displayRefresh composable 取图表 ### Display Feature 已有 API（不改，只做 UI 层） display service 已具备完整能力，但当前页面几乎没用到： | 能力 | API | 当前页面使用 | |------|-----|------------| | 双面板偏好 | `preferences.table1 / table2` | ❌ 未用 | | 三种显示模式 | `DisplayMode = 'table' \| 'chart' \| 'special'` | ❌ 硬编码 tab | | 分组选择 | `selectedGroupId` | ❌ 未暴露 | | 多图表实例 | `ChartInstanceProjection[]`（1-4） | ⚠️ 只取 [0] | | Y 轴配置 | `YAxisPreference { autoScale, min, max }` | ❌ 未暴露 | | 星座图 | `ScatterProjection + ScatterDisplayPreference` | ⚠️ 有组件无配置 | | 图表性能 | `ChartPerformancePreference { maxPoints, refreshIntervalMs }` | ❌ 未暴露 | | 刷新 composable | `useDisplayRefresh(service)` | ✅ 在用 | ### 旧系统 UX 核心（需要还原的） 1. **双面板**：左右两个独立面板，各有独立配置 2. **三种模式切换**：表格 / 折线图 / 星座图，每面板独立 3. **分组选择器**：每面板独立选数据分组 4. **图表配置弹窗**：字段选择 + Y 轴 + 性能 5. **星座图配置弹窗**：I/Q 数据源 + 位宽 + 采样数 6. **底部状态栏**：面板状态 + 更新间隔 7. **录制控制**：开始/停止 + 录制时长 + 记录数 ### 不在 scope 的（H001 边界） - **录制控制**：不在 display feature，属 settings/storage 层，需要 feature API 扩展 - **字段排序/收藏**：属 receive feature，不改 […]