[DEVELOPER]: .sessions/2026-05-21-missing-pages/H001-conversation-prompts.md 对话D

[AGENT]: 文件已读取。以下是**对话 D**的完整提示词（第 118-133 行）： --- ## 对话 D：存储管理 — feature 设计 ``` Lane B/C | 存储管理高速存储 feature 设计（只设计不实施） 先读 .sessions/2026-05-21-missing-pages/S001-research-and-planning.md §存储管理补充 + §对话 D 再读 .sessions/2026-05-21-missing-pages/topic-index.md 目标：设计高速存储三层架构 — 规则模型 + 分流机制 + Platform 文件流。产出设计文档 + checklist，不写代码 直接合同：S001 §存储管理关键发现 + §存储管理补充 边界护栏：R5 + R6 + CLAUDE.md main 不承载业务逻辑 按 H001 §通用流程指令执行（Phase 1-2，不进 Phase 3 实施设计文档 + checklist 产出 + 自检通过即可。 Wave 1 按 S001 §对话 D 派 9 agent。 ``` --- **对话 D 关键信息：** - **Lane**: B/C（需要设计闭环，可能跨模块） - **只设计不实施** — 产出设计文档 + checklist 即可 - **目标**: 高速存储三层架构（规则模型 + 分流机制 + Platform 文件流） - **Wave 1**: 需派 9 agent 收集事实 - **直接合同**: S001 的存储管理关键发现和补充 - **边界护栏**: R5 + R6 + main 不承载业务逻辑 要现在开始执行对话 D 吗？

[DEVELOPER]: 好

[AGENT]: 开始执行对话 D。先读必读文档。

[AGENT]: 已读完必读文档。开始对话 D 执行。 **Direct contract:** S001 §存储管理关键发现 + §存储管理补充 **Boundary guards:** R5 + R6 + CLAUDE.md main 不承载业务逻辑 **目标:** 设计高速存储三层架构（规则模型 + 分流机制 + Platform 文件流），只产出设计文档 + checklist，不写代码 先创建任务追踪，再派 Wave 1 Batch 1。

[AGENT]: 开始 Wave 1 Batch 1 — 派 3 个 agent 并行收集旧系统事实。

[AGENT]: Batch 1 完成。关键发现： - **单规则系统**：旧系统只支持 1 条 FrameHeaderRule，新系统需支持多规则 - **短路分流**：网络数据在主进程被拦截，匹配规则后直接写文件，不发渲染进程 - **文件流+轮转**：WriteStream 追加写入，size 触发轮转，保留 N 个最新文件 - **数据格式**：Uint8Array → 大写 hex string，每帧一行 开始 Batch 2。

[AGENT]: Batch 2 完成。关键发现： - **Connection 分流钩子位置明确**：`drainAdapterEvents()` 返回后、状态更新前，是最佳分流点 - **Platform 缺文件流**：只有 readTextFile/writeTextFile，缺少 createWriteStream/rotation/checkFileSize - **storage-local-baseline 是 JSON 持久化**：与高速存储的流式二进制写入完全不同，但类型和模式可复用 开始 Batch 3。

[AGENT]: Wave 1 全部完成（9/9 agent）。汇总关键事实，进入 Wave 2 设计。 ## Wave 1 关键事实汇总 | 维度 | 发现 | |------|------| | 旧系统模型 | 单规则(1条 FrameHeaderRule)，单连接，hex 模式匹配，WriteStream 追加写入 | | 旧系统分流 | networkHandlers:505-517 短路——匹配后直接写文件、不发渲染进程 | | 新系统连接层 | drainAdapterEvents() 是唯一数据汇聚点，事件先入 buffer 再由 renderer 拉取 | | Platform 缺口 | 无 createWriteStream / checkFileSize / ensureDir / listFiles / deleteFile | | storage-local | JSON 持久化 + Material bucket 模式，与流式写入完全不同，类型可复用 | | R5/R6 约束 | main 可做文件 I/O + 高频缓冲/批处理/分流，**不可做**业务规则/协议语义 | | 16 项行为基线 | 6 项 baseline 已覆盖，6 项需高速存储 feature（STO-009~014），4 项部分覆盖 | ## 核心设计决策（9 项，需确认） **D1: Feature 归属** — 新建 `features/storage-highspeed/`，不扩 storage-local-baseline - 理由：数据模型（流式 vs Material）、生命周期（常驻活跃 vs 批量操作）、平台集成方式完全不同 **D2: 匹配位置** — 字节匹配在 main process，规则管理在 renderer - 理由：分流必须在 IPC 之前完成，否则所有数据都会穿越到 renderer，失去分流意义 - R5 允许 main 做"高频数据缓冲、批处理、**分流**"；匹配算法是纯函数（可独立测试），不属于"业务运算/协议语义" - 边界：renderer 拥有"配什么规则、何时启用"的业务决策权；main 只执行"对给定字节和已注册模式做前缀比较" **D3: 分流插入点** — transport handler 内，数据入 event buffer 之前 - 理由：匹配数据不入 buffer，零 renderer 开销，无需改 routing-tick **D4: Platform API 设计** — 粗粒度 typed API，不暴露单文件操作 - `activateFilter(rules + fileConfig)` / `deactivateFilter()` / `getStats()` / `resetStats()` / `updateConfig()` - 理由：R6 禁止散落小 IPC；renderer 不需要也不应控制文件级操作 **D5: 文件格式** — 与旧系统相同（每帧一行大写 hex string） - 理由：向后兼容、人类可读、简单；未来可加二进制格式优化 **D6: 统计模式** — main 维护计数器，renderer 定时轮询（1s） - 理由：高频更新不应逐次跨 IPC **D7: 持久化** — 配置和规则由 renderer feature 通过现有持久化机制保存；统计数据运行时态 - 理由：配置是领域状态，归 feature service **D8: 多规则支持** — 支持多条规则，每条绑定不同 connectionId - 旧系统只支持 […]

[DEVELOPER]: 自检一下

[AGENT]: 派 3 个自检 agent 并行。

[AGENT]: 3 个自检 agent 完成。SC2 提到 `receive/core/frame-matcher.ts` 可能可复用，先验证这个关键事实。

[AGENT]: 验证完毕。`receive/core/frame-matcher.ts` 是协议识别（用 startIndex/endIndex + 多算子匹配帧定义），与高速存储的帧头前缀匹配（byte prefix comparison）是**不同层次的操作**，不构成重复。SC2 这个发现是误判。 --- ## 自检综合结论 ### 有效发现（需修正） | # | 来源 | 问题 | 修正方向 | |---|------|------|---------| | 1 | SC2 | **适配器层过度抽象** — Platform facade 已是边界，adapter 只有一份实现，方法直接透传 | 去掉适配器层，service 直接调用 platform facade，用 facade test double 做测试 | | 2 | SC2 | **D8 多规则无证据** — 旧系统单规则+多 pattern 已够用，多规则无实际需求驱动 | 改为单规则 + 多 headerPattern（与旧系统一致），多规则留 future | | 3 | SC1/SC2 | **分流短路未注册边界例外** — 高速存储短路正常 receive/display/trigger 链 | 设计文档中显式注册为 runtime 边界例外 | | 4 | SC3 | **STO-003/015/016 遗漏** — 定时持久化、日级清理、gzip 压缩未覆盖 | STO-003 归 runtime 层，STO-015/016 显式标记为 deferred | | 5 | SC2 | **config 单源真相关** — renderer 和 main 两处存配置 | 明确：renderer 唯一拥有 config + rules；main 只接收编译后的 active rules，不存 config | | 6 | SC2 | **createStorageHighspeedReader 可能多余** — 高速存储无只读消费者 | 去掉 reader，service 本身暴露 getSnapshot | ### SC1 误判（无需修正） | 判定 | 实际情况 | |------|---------| | Feature 应放 storage 子目录 | `features/storage-highspeed/` 与 `storage-local-baseline` 并列是正确的，两者数据模型/生命周期/平台集成完全不同 | | R5 违反（匹配在 main） | R5 明文允许 main 做"高频数据缓冲、批处理、**分流**"；业务决策（配什么规则、何时启用）在 renderer，main 只做 byte prefix comparison 执行。需注册为显式边界例外，不是违规 | | 5 层结构缺失 | 设计已含 core/service/adapter/state/selectors，SC1 误读 | ### SC2 误判 | 判定 | 实际情况 | |------|---------| | 与 receive/core/frame-matcher.ts 重复 | receive 的 matcher 做协议识别（startIndex/endIndex + eq/neq/gt 等 10 种算子），高速存储做数据路由（byte […]