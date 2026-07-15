> DEVELOPER

.sessions/2026-05-21-missing-pages/H001-conversation-prompts.md Northbound 框架，讨论这个？.sessions\2026-05-18-northbound-integration\topic-index.md得看

> DEVELOPER

.sessions/2026-05-21-missing-pages/H001-conversation-prompts.md Northbound 框架，讨论这个？.sessions\2026-05-18-northbound-integration\topic-index.md得看 @.agent/skills/cs-brainstorm/SKILL.md

> AGENT

先读你提到的两份文件，了解上下文。

> AGENT

好，我看到了完整上下文。按 brainstorm 流程先做分诊前检查——扫一下仓库里 northbound 相关的已有工件和 feature。

> AGENT

检查完成，汇总发现：

**已有工件：**
- `.sessions/2026-05-18-northbound-integration/` — S001 闭环分析已完成，7 条架构决策已锁定，代码验证已做
- `.sessions/2026-05-21-missing-pages/` — S001 里已规划了 Northbound 并行对话的 Wave 1-3 策略（6 agent + 3 自检），H001 有现成提示词
- `codestable/` 下无 northbound feature 目录，无 design/brainstorm 文件

**已锁定决策（S001）：**
- testCase = task 映射
- HTTPS server 在 main，业务在 renderer
- northbound 独立 feature，不合并 command-ingress
- 翻译层（inbound/outbound）在 feature 内
- result 不改，northbound 自己接线 onSettled

**未决项（6 条）：** HTTPS 库选型、taskId↔instanceId 映射、sessionId 生命周期、G2 step 名称映射、G5 getTestCaseAll 格式、TLS 配置

---

**分诊判断：** 这块方向和架构已经 S001 一轮完整分析锁定了，6 个 MVP 接口清晰，"不做"清单有。剩余未决项是设计阶段要拍的技术选型和细节，不是方向性问题。

我判 **case 1——已经够清楚**。H001 提示词里 Wave 1-3 策略、直接合同、边界护栏都现成了。直接进 `cs-feat-design` 更省事，brainstorm 对这块没增量。

要不要直接跳到 design？还是你觉得有什么点还没想透想先聊？

> DEVELOPER

我记得之前有对应design，不过它很老了，得大改？

> AGENT

找到了。你说的"对应 design"应该是这份：

**`codestable/compound/2026-04-28-northbound-overlap-and-gap-map.md`**（4月28日）

这不是一份 feature design——是甲方对接前的 **gap 分析 + overlap 矩阵**。253 行，覆盖面很全：
- 甲方 31 接口的 overlap/gap 分类
- false equivalence 清单（send≠setTestTask、history≠TestReport、target≠deviceId）
- 12 条可自主决策 + 13 条待问甲方

**但它和当前状态有三层脱节：**

| 维度 | gap map（4/28） | 当前（5/18 S001 之后） |
|------|---------|---------|
| 决策层 | "待问甲方"占多数 | 7 条架构决策已锁定，2 条甲方已回复 |
| 映射层 | task/case 关系还在讨论 | testCase=task 已确认，executionPlan 处理方案已定 |
| MVP 范围 | 31 接口全覆盖 | 收窄到 6 个 MVP 接口，"不做"清单明确 |

**结论：gap map 不需要"大改"——它作为边界参考仍然准确（false equivalence 那些不会过时），但不可能从它改出一份 feature design。** northbound feature design 得从零写，直接合同是 5/18 S001 的 7 条决策 + 6 个 MVP 接口。

所以回到分诊：这块确实是 **case 1**——方向、架构、范围、上游依赖全锁了，缺的就是一份 `codestable/features/rewrite-northbound/northbound-design.md`。

直接 `cs-feat-design` 开干？还是你觉得有哪个点还没定想先聊？

> DEVELOPER

codestable\features\rewrite-command-ingress\command-ingress-brainstorm.md这个？应该有些相关的

> AGENT

找到了，确实高度相关。command-ingress brainstorm（5月9日）覆盖了新甲方 HTTPS 接口——但后来被 5/18 的 northbound 决策推翻了。

关键点：

**command-ingress brainstorm 原本的定位：**
- 统一外部命令入站 feature，同时处理 SCOE TCP + 新甲方 HTTPS
- 决策 9："新甲方 HTTPS 先做 stub，`canHandle()` 返回 false，不实现协议细节"
- 有完整的 ProtocolAdapter 接口 + TransportEventConsumer 消费者链模式

**5/18 northbound S001 推翻的决策：**
- northbound 做独立 feature，**不合并到 command-ingress**
- HTTPS server 在 main process，业务在 renderer
- 翻译层（inbound/outbound）在 northbound 内部

**现在的状态：**

| 方面 | command-ingress brainstorm | 需要怎么变 |
|------|--------------------------|-----------|
| 甲方 HTTPS 部分 | stub，留在 command-ingress | 拆出去给 northbound |
| TransportEventConsumer 模式 | 设计完整，可用 | northbound 的 HTTPS server 不走 transport event 流（甲方主动推我们），消费模式不同 |
| SCOE 部分 | 完整设计 | 不受影响，留给 command-ingress |
| TaskDefinition 翻译模式 | send+wait 映射 | northbound 的 setTestTask 也翻译成 TaskDefinition，模式可复用 |

所以不是"大改"——是 **command-ingress 里的甲方 HTTPS stub 要拆出来，变成独立的 northbound feature**。但两条入站路径的协议层差异不小：SCOE 是字节流协议识别（consumer 链），甲方是 HTTPS server 收 JSON（完全不同的入站模式）。

这改变分诊判断吗？我觉得不改变——方向仍然清楚，只是多了一个上游参考材料。还是 case 1，你有想法要补充吗？

> DEVELOPER

让子agent看看目前状况。想一想怎么搞合适。

> AGENT

探索完成，汇总一下现状和想法。

## 现状一句话

**内部引擎全通，northbound 层零代码。** command-ingress 的 SCOE → TaskDefinition 翻译模式可直接复用。

## 具体缺失

| 层 | 缺什么 | 改动量 |
|---|--------|--------|
| **platform facade** | HTTPS server + HTTPS client + FTP | 新增 ~3 个 facade，main process 加 IPC |
| **task service** | step 完成事件 hook（msgReport 需要） | task-iteration-loops.ts 加回调参数，~20 行 |
| **result wiring** | onSettled → collectResult 自动接线 | runtime 加几行编排 |
| **northbound feature** | 整个 feature 不存在——inbound translator、outbound translator、session 管理、heartbeat、getSubSysState | 从零建 |
| **preload bridge** | 暴露 HTTPS/FTP 相关 IPC | 扩展现有 preload |

## 怎么搞

我判断还是 **Lane B 单 feature**——和 command-ingress 同样规模。理由：

1. 外部表面是一个 feature（甲方 HTTPS 闭环），不像 receive-real 那样有 5 个子 feature
2. platform/main 改动是基础设施扩展，服务于这个 feature，不算跨 feature 编排
3. command-ingress 已验证了 consumer chain + translator + TaskDefinition 翻译这条路径

**但 H001 提示词里的 Wave 1-3 策略需要更新**——那份是基于 5/21 的认知写的，没考虑到：
- command-ingress 已完整实现，可直接参考其 translator 模式
- result 已有被动 API，只需要接线
- step event hook 是前置依赖，得先确认 task 那边怎么加

建议的推进顺序：
1. **先让 task 加 step 完成回调**（最小改动，独立可验证）
2. **建 northbound feature 骨架 + platform 扩展**（HTTPS server/client facade）
3. **实现 inbound translator**（setTestTask → TaskDefinition，参考 command-ingress 的翻译模式）
4. **实现 outbound translator + 接线**（onSettled → result → 翻译 → POST）
5. **heartbeat + getSubSysState**（简单 handler）

你觉得这个路子对不对？对的话直接进 `cs-feat-design`。

> DEVELOPER

可以？不过http的不能放在这吧？各级封装要足够好，这样后面改动才不会改一点就要改一堆文件

> AGENT

对，你说得对。HTTPS server/client 是平台能力，不是 northbound 业务——和 TCP/UDP/Serial 一样，应该归 platform facade + main process。

层级应该是：

```
main process    → HTTPS server (接收) + HTTPS client (发送) + FTP client
preload         → 暴露 IPC bridge
platform facade → 封装为类型安全的 API（和 transport/file 同级）
northbound      → 只消费 platform facade，不碰 HTTP 细节
```

这样 HTTPS 库换掉（Fastify→Express / 原生 Node）、TLS 配置变、端口变，都只动 platform + main，northbound 不受影响。

那推进拆成两块：

1. **platform HTTPS facade**（独立小任务，Lane A 级别）—— main process 加 HTTP handler + preload 暴露 + platform facade 封装
2. **northbound feature**（Lane B）—— 建好后消费 platform facade

这两块可以先 design 再 impl，也可以 platform 先快速落地再搞 northbound。你倾向哪种节奏？

> DEVELOPER

甲方接口相关我不希望主进程那边也要改。应该不会吧？你没打算把甲方接口写进主进程吧？

> DEVELOPER

甲方接口相关我不希望主进程那边也要改。应该不会吧？你没打算把甲方接口写进主进程吧？不然改一点动的太多了。然后，我希望到时候相关地方尽量用接口类型，别到处都自己编，不然也太多了

> AGENT

不会，主进程不碰任何甲方接口语义。模式跟现在的 TCP server 一样：

```
main process（纯传输层）
  收到 HTTPS request → 只提取 { method, url, headers, body }
  → IPC 透传给 renderer
  ← renderer 返回 { statusCode, headers, body }
  → 发 HTTPS response

main 完全不知道 setTestTask / testCaseResultReport 是什么
```

类型也是同一个思路——甲方接口类型只定义一次：

```
northbound/core/types.ts
  → InboundRequest（setTestTask / controlTestTask / heartbeat / getSubSysState）
  → OutboundResponse（testCaseResultReport / msgReport）
  → 甲方枚举、错误码等

这些类型被：
  - inbound translator 消费（解析 request）
  - outbound translator 消费（构造 response）
  - 测试 fixture 消费
  - 未来 UI 消费（如果需要展示 northbound 状态）

其他层看到的都是通用类型：
  - platform facade → HttpRequest / HttpResponse（不含甲方语义）
  - main process → 同上，只认 raw HTTP
  - IPC bridge → 同上
```

改动传播路径：甲方改接口 → 只动 `northbound/core/types.ts` + 两个 translator。main / platform / IPC 不动。

这两点我记到 brainstorm note 里，design 阶段当硬约束。还有别的顾虑吗？没有的话直接进 design。

> DEVELOPER

可以，先写文档，不然直接进容易漏

> AGENT

好，按 case 2 落 brainstorm note。先建目录。

> AGENT

Brainstorm note 已落到 `codestable/features/rewrite-northbound/northbound-brainstorm.md`。

核心约束已记录：
- 主进程纯传输，不含甲方语义
- 类型只定义一次，不改多处
- HTTPS 归 platform，northbound 只消费 facade
- 改动传播路径：甲方改接口 → 只动 types + translator

下一步 `cs-feat-design` 会读到这份文件，直接用它当直接合同的种子。

> DEVELOPER

、继续吧？

> AGENT

好，进 design 阶段。先看下有没有 cs-feat-design skill。

> AGENT

启动 cs-feat-design。先做启动检查——并行读取必要材料。

> AGENT

架构文档读完了。现在需要看代码级的实际 API 签名——并行派 agent 查关键实现细节。

> AGENT

所有材料齐了。开始写设计文档。

> AGENT

设计文档已落盘。按 skill 要求，发整体 review 提示：

> 方案 doc 已起草完成，请整体 review：
> 1. 术语有没有和已有概念冲突？
> 2. 第 1 节决策与约束准不准，"不做什么"有没有遗漏？
> 3. 第 2.1 名词层：现状描述对不对？变化是否覆盖所有数据/接口改动？
> 4. 第 2.2 编排层：主流程图和现状→变化能不能跑通你脑子里的场景？跨层纪律有没有漏？
> 5. 第 2.3 挂载点：照这份清单能不能完整卸载？有没有项是内部改动被误列进来？
> 6. 第 2.5 结构健康度：评估的几个文件是否准确？结论（不做 / 微重构）和方案是否同意？
> 7. 第 3 节验收场景：覆盖正常 + 边界 + 错误路径了吗？
>
> 有修改意见直接说，确认后生成 checklist 进实现阶段。

> DEVELOPER

你让子agent去自检

> AGENT

三个自检完成。汇总关键发现：

**边界合规**：10/10 全通过。一个观察：CLAUDE.md 第 92 行和第 88 行有张力（command-ingress vs 独立 northbound），design 用 D1 正确解决了。

**决策一致性**：7 条锁定决策 + 3 条确认项全部一致。发现 7 个新决策需确认（onStepResult 回调机制、映射位置、不重试策略等）。

**覆盖完整性**：3 个关键 gap 需要修：

1. **onStepResult 回调拿不到 TaskInstanceState** — outbound translator 需要 instance 才能查 stepName，但回调只有 instanceId。需要明确通过 `taskService.getInstance()` 获取
2. **executionPlan 编排缺伪代码** — 并行层怎么等、顺序层失败怎么处理、中途失败的清理
3. **回调异常隔离** — onStepResult 如果 throw 会崩 task 执行循环

现在修 design 文档补上这些 gap。

> AGENT

逐个修 gap。

> AGENT

现在补充 controlTestTask 的映射表和 getSubSysState 的数据来源。

> AGENT

现在补充 task 创建中途失败和甲方重连场景的验收场景。

> AGENT

最后明确 HTTPS 库 MVP 选型。

> AGENT

Design 已更新，补齐了自检发现的 3 个关键 gap：

1. **onStepResult 获取 TaskInstanceState** — 明确通过 `taskService.getInstance()` 公开 API 获取，回调异常用 try/catch 隔离
2. **executionPlan 编排伪代码** — 补了并行/顺序层处理算法 + 中途失败处理策略
3. **错误路径** — 补了 S16（创建中途失败）、S17（回调异常隔离）、S18（甲方重发）

还修了几个部分覆盖项：controlTestTask 映射表、getSubSysState 数据来源、移除 settingsReader 依赖、HTTPS 库 MVP 选 Node 原生。

再看一眼有没有要调整的？确认后生成 checklist。

> DEVELOPER

我没意见，我看不过来

> AGENT

好，生成 checklist 然后把 design 改成 已批准。

> AGENT

Design 已批准，checklist 已通过验证。

产出清单：
- `codestable/features/rewrite-northbound/northbound-design.md` — 已批准
- `codestable/features/rewrite-northbound/northbound-checklist.yaml` — 8 步 + 14 检查项，已验证
- `codestable/features/rewrite-northbound/northbound-brainstorm.md` — 讨论过程记录

下一步 `cs-feat-impl` 可以开始。按推进策略先从 Platform HTTP facade 和 task step 回调并行启动。

> DEVELOPER

我打算先压缩

> AGENT

明白，压缩上下文。

**本对话产出**：
- `codestable/features/rewrite-northbound/northbound-brainstorm.md` — 分诊+讨论+锁定约束
- `codestable/features/rewrite-northbound/northbound-design.md` — 已批准，8步推进+14检查项
- `codestable/features/rewrite-northbound/northbound-checklist.yaml` — 已验证

**关键约束留给下一轮**：
- 主进程纯传输，不含甲方语义
- 类型只在 northbound/core/types.ts 定义一次
- HttpFacade 是 platform 层，与 TransportFacade 同级
- task service 加 onStepResult 可选回调，try/catch 隔离

**下一步**：`cs-feat-impl` 按 checklist 8 步推进，先并行做 Platform HTTP facade + task step 回调。

> DEVELOPER

继续吧