[DEVELOPER]: .sessions/2026-05-21-missing-pages/H001-conversation-prompts.md 对话A

[AGENT]: 好的，开始对话 A：系统设置页。先读取直接合同和边界护栏材料。

[AGENT]: 已读完 S001 和 topic-index。开始对话 A：系统设置页。 **直接合同：** S001 §系统设置关键发现 + §系统设置补充 **边界护栏：** R14（services and wiring explicit）+ R7（one owner per state）+ CLAUDE.md 配置归口 按 Wave 1/2/3 执行。先启动 Batch 1 — 3 个 agent 并行收集事实。

[AGENT]: Wave 1 第一批已启动（A1 设置类型默认值、A2 服务/状态/选择器、A3 旧系统配置存储）。等待结果返回后启动第二批。

[AGENT]: A2 已返回。Settings feature 当前 3 个 scope、7 个字段、9 个 selector，确认 7/21 覆盖。等待 A1、A3 完成。

[AGENT]: A1 也已返回。Settings 类型体系完整，14 项 gap 分属 connection/display/status/command-ingress 等 feature。等 A3 回来就启动第二批。

[AGENT]: Batch 1 全部返回。旧系统 17 个主配置项（~50+ 字段）分布在 8 个 store。现在启动 Batch 2 — 3 agent 并行查 connection/display/status/command-ingress 的配置 API。

[AGENT]: Batch 2 已启动（A4 连接配置 API、A5 显示/状态配置 API、A6 命令入口 SCOE 配置）。等待返回后启动 Batch 3。

[AGENT]: A4 返回。连接功能缺失 7 个串口配置字段（dataBits/stopBits/parity/flowControl/bufferSize/timeout），持久化已接入。等 A5、A6。

[AGENT]: A6 返回。SCOE 配置 API 已暴露（类型+验证完整），但持久化是 TODO 占位、高亮配置缺失。等 A5。

[AGENT]: A5 返回。显示偏好 API 完整，状态指示灯 API 完整（阈值替代值映射），两者都缺持久化。第二批全部完成，启动第三批。

[AGENT]: 第三批已启动（A7 持久化机制、A8 集测行为基线、A9 UI 规范速查）。等待全部返回后进入 Wave 2 设计阶段。

[AGENT]: A9 返回。UI 规范要点已收集：Mode C 布局、QForm+Quasar 组件、语义 class、useAsyncAction/useNotify 必用、300 行拆分。等 A7、A8。

[AGENT]: A8 返回。21 项设置行为覆盖度：8 已覆盖(38%)、9 部分覆盖(43%)、3 未覆盖(14%)、1 无法判断(5%)。等最后一个 A7。

[AGENT]: **Wave 1 全部完成。** 9 个 agent 事实已收集。进入 Wave 2 设计阶段。 --- ## Wave 2：系统设置页设计 ### 事实汇总 | 维度 | 发现 | |------|------| | Settings feature | 7 字段 / 3 scope / 完整 service+selector | | 旧系统 | 17 主配置项，8 个 store，~50+ 字段 | | 21 项行为 | 8 已覆盖(38%)、9 部分覆盖(43%)、3 未覆盖(14%) | | Connection | 缺 7 个串口参数字段，持久化已接入 | | Display/Status | API 完整，持久化未接入 | | SCOE | 类型+验证完整，持久化是 TODO 占位 | | 持久化现状 | 仅 frame/connection/settings 3 个 feature 已持久化，启动只恢复 frames | ### Gap 分析 **本对话必须解决（设置页前置）：** | Gap | 类型 | 工作量 | |-----|------|--------| | 串口详细参数 (dataBits/stopBits/parity/flowControl) | 扩展 connection types | 小 | | display/status 持久化未接入 | 持久化 wiring | 中 | | 设置页 UI | 新页面 | 中 | **依赖其他对话（不阻塞设置页基本结构）：** | Gap | 依赖 | |-----|------| | 多图表配置 | 对话 B (display 扩展) | | 高速存储配置 | 对话 D (存储管理) | | SCOE 持久化补全 | 独立工作 | | 多帧发送策略 | send/task feature | ### 设计方案 **页面结构（Mode C：单列居中，max-width 1120px）：** | 分组 | 配置来源 | 本对话实施 | |------|---------|-----------| | 应用 (Application) | settings feature (7项) | 完整实施 | | 连接 (Connection) | connection feature (串口默认参数) | 完整实施 | | 显示 (Display) | display feature | 预留分组，等对话 B | […]