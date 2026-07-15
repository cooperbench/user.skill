> DEVELOPER

.sessions/2026-05-21-missing-pages/H001-conversation-prompts.md Northbound 框架，讨论这个？.sessions\2026-05-18-northbound-integration\topic-index.md得看

> DEVELOPER

.sessions/2026-05-21-missing-pages/H001-conversation-prompts.md Northbound 框架，讨论这个？.sessions\2026-05-18-northbound-integration\topic-index.md得看 @.agent/skills/cs-brainstorm/SKILL.md

> AGENT

先读你提到的两份文件，了解上下文。

> TOOL

tool_use Read
id: call_aac8e37ad7f54829bb456d7d
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-21-missing-pages/H001-conversation-prompts.md"
}
```

> TOOL

tool_use Read
id: call_c3ae12a64fd043fd9cdb62ca
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-18-northbound-integration/topic-index.md"
}
```

> TOOL

tool_result
id: call_aac8e37ad7f54829bb456d7d
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

> TOOL

tool_result
id: call_c3ae12a64fd043fd9cdb62ca
```
1	# 甲方对接闭环分析
2	
3	> 状态: active | 创建: 2026-05-18
4	
5	## 专题目标
6	
7	基于甲方 V1.0.1 接口文档（31 接口），确认"甲方控制我们任务、我们回传结果"这条链路是否闭环，识别断点，拍板决策，为后续 northbound feature 设计和实施做准备。
8	
9	## 进展线索
10	
11	### S001 — 闭环讨论与决策拍板
12	- 完整读入甲方文档并拆分为 11 个文件（31 接口），存放在 `rewrite/docs/甲方文档/集成测试系统与各二级子系统接口设计-拆分/`
13	- 并行 3 个子 agent 读取：我方 6 份 northbound 文档、task 系统代码+设计、甲方 4 个核心接口详细规格
14	- 完成 5 个问题分析（Q1 闭环完整性、Q2 HTTPS 放哪、Q3 翻译层形状、Q4 与 command-ingress 关系、Q5 旧 gap 有效性）
15	- 代码级验证 result/task/platform 实际实现状态（另派 1 个 explore agent 查代码）
16	- 拍板所有核心决策（4 轮决策演进：初始 → testCase=task → verdict 依据确认 → 甲方回复）
17	- 产出甲方待确认 2 条 → 甲方回复 immediate=true/isEnd=true → 待确认项清零
18	
19	## 已确认结论
20	
21	### 核心映射
22	
23	- **甲方 testCase = 我们的 task（TaskDefinition）**
24	- 甲方的 executionPlan.layers 中每个 testCaseId → 我们创建一个 task 实例
25	- task 典型 steps = send step（发帧）+ wait-condition step（等接收帧校验参数）
26	- verdict: wait-condition matched → success, timeout/不匹配 → fail, task 被 stop → tbd
27	
28	### MVP 接口（6 个）
29	
30	| 接口 | 方向 | 映射 | 状态 |
31	|------|------|------|------|
32	| setTestTask | 甲方→我们 | testCaseInfo[] 每项 → 一个 task | 逻辑通 |
33	| controlTestTask | 甲方→我们 | abort→stop, pause→pause, continue→resume, stop→stop | […]

> AGENT

好，我看到了完整上下文。按 brainstorm 流程先做分诊前检查——扫一下仓库里 northbound 相关的已有工件和 feature。

> TOOL

tool_use Glob
id: call_9994ccf7ae6a4b10ac01d931
```json
{
  "pattern": "codestable/features/**/northbound*"
}
```

> TOOL

tool_use Glob
id: call_83fe79c90be943f686601162
```json
{
  "pattern": "codestable/roadmap/**/*"
}
```

> TOOL

tool_use Grep
id: call_7ee343da563542ff90cd587b
```json
{
  "pattern": "northbound",
  "path": "/mnt/d/code/frontend/dongfanghong/codestable",
  "output_mode": "files_with_matches",
  "head_limit": 20
}
```

> TOOL

tool_use Read
id: call_e84ef9c4982a442fa299c6ef
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-21-missing-pages/S001-research-and-planning.md",
  "offset": 1,
  "limit": 50
}
```

> TOOL

tool_result
id: call_e84ef9c4982a442fa299c6ef
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
```

> TOOL

tool_result
id: call_7ee343da563542ff90cd587b
```
Found 20 files limit: 20
codestable/quality/rewrite-quality-rules.md
codestable/features/rewrite-connection/rewrite-connection-checklist.yaml
codestable/features/rewrite-frame/frame-real-acceptance.md
codestable/features/rewrite-send/send-real-brainstorm.md
codestable/features/rewrite-send/send-real-design.md
codestable/features/rewrite-frame/frame-real-design.md
codestable/features/rewrite-task/task-real-brainstorm.md
codestable/quality/code-simplification-audit.md
codestable/roadmap/receive-real/receive-real-roadmap.md
codestable/features/rewrite-send/send-real-acceptance.md
codestable/features/rewrite-result/result-report-brainstorm.md
codestable/features/rewrite-connection/rewrite-connection-acceptance.md
codestable/features/rewrite-command-ingress/command-ingress-design.md
codestable/features/rewrite-command-ingress/command-ingress-checklist.yaml
codestable/features/rewrite-command-ingress/command-ingress-brainstorm.md
codestable/features/rewrite-task/rewrite-task-checklist.yaml
codestable/features/rewrite-storage-local-baseline/rewrite-storage-local-baseline-checklist.yaml
codestable/features/rewrite-display/rewrite-display-checklist.yaml
codestable/features/rewrite-connection/rewrite-connection-design.md
codestable/architecture/rewrite-target-structure.md
```

> TOOL

tool_result
id: call_9994ccf7ae6a4b10ac01d931
```
No files found
```

> TOOL

tool_result
id: call_83fe79c90be943f686601162
```
codestable/roadmap/receive-real/receive-real-items.yaml
codestable/roadmap/receive-real/receive-real-pipeline-acceptance.md
codestable/roadmap/receive-real/receive-real-roadmap.md
```

> TOOL

tool_use Grep
id: call_112725914f0f4b808c67cf83
```json
{
  "pattern": "Northbound",
  "path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-21-missing-pages/S001-research-and-planning.md",
  "output_mode": "content",
  "-n": true
}
```

> TOOL

tool_result
id: call_112725914f0f4b808c67cf83
```
23:- Northbound：4 接口缺失，框架可先搭，等甲方 schema
79:| *并行 | Northbound 框架搭建 | B | 1对话 |
94:| Result ≠ Report ≠ Northbound（三层分离） | S004 | result 只管内部事实 |
134:#### Northbound 补充
402:#### 并行对话：Northbound 框架搭建
440:- Northbound 框架可独立并行
```

> TOOL

tool_use Read
id: call_c416f7c662aa4d0aa0de2ffd
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-21-missing-pages/S001-research-and-planning.md",
  "offset": 134,
  "limit": 60
}
```

> TOOL

tool_use Read
id: call_e7696386eb004461930eb51b
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-21-missing-pages/S001-research-and-planning.md",
  "offset": 402,
  "limit": 50
}
```

> TOOL

tool_result
id: call_c416f7c662aa4d0aa0de2ffd
```
134	#### Northbound 补充
135	
136	| 事实 | 来源 | 影响 |
137	|------|------|------|
138	| 4 接口已定：setTestTask / controlTestTask / testCaseResultReport / msgReport | northbound | 与设置/存储页面无直接依赖 |
139	| HTTPS server 在 main process，renderer 处理业务 | northbound | 不影响页面设计 |
140	| "不做"清单：testDataFileDelivery + 详细 report | northbound | 存储页不承载 FTP 交付 |
141	| FTP facade 需新增到 platform | northbound | platform 扩展项 |
142	| testCase = task，翻译层 inbound/outbound | northbound | 与 task-real 耦合 |
143	
144	#### 实施模式补充
145	
146	| 模式 | 来源 | 适用 |
147	|------|------|------|
148	| Checklist-based acceptance：design → checklist → impl → review | S008 | 所有 feature 验收 |
149	| Phased implementation：types → service → adapter → wiring | S007 | 复杂 feature 拆期 |
150	| Consumer chain 分发，非 dispatch | S008 | 跨 feature 数据流 |
151	| 集测验证 1178 tests + lint 必须通过 | S011 | 每个 feature 完成标准 |
152	
153	#### UI 实施约束补充
154	
155	| 约束 | 来源 | 适用 |
156	|------|------|------|
157	| 47 项 UI 审计（3 P0 + 12 P1 + 4 P2）已有纠正模式 | S011 | 新页面避免重犯 |
158	| useAsyncAction / […]

> TOOL

tool_result
id: call_e7696386eb004461930eb51b
```
402	#### 并行对话：Northbound 框架搭建
403	
404	**Lane B** | 预估 1 对话 | 与页面对话并行
405	
406	**直接合同：** `.sessions/2026-05-18-northbound-integration/S001-closed-loop-analysis.md`
407	
408	**Wave 1（6 agent，分 2 批）：**
409	
410	**Batch 1（3 agent 并行）：**
411	- **N1 — northbound 分析文档事实提取**：`S001-closed-loop-analysis.md`（§四-§六 架构决策 + §十三 全量清单）
412	  → 产出：7 条已拍板决策 + 入站/出站完整清单 + 待决项
413	- **N2 — result + task 终态机制**：`rewrite/src/features/result/`（judgeCaseVerdict + result service）+ `rewrite/src/features/task/services/task-service.ts`（onSettled + stepResults）
414	  → 产出：result MVP API 签名 + onSettled 用法 + step 结果存储机制
415	- **N3 — command-ingress 参考模式**：`rewrite/src/features/command-ingress/`（TransportEventConsumer + ProtocolAdapter + Handler 链）
416	  → 产出：已有外部系统接入模式 + 可复用的架构模式
417	
418	**Batch 2（3 agent 并行）：**
419	- **N4 — platform facade 扩展需求**：`rewrite/src/platform/`（当前 facade 全部文件）
420	  → 产出：需要新增的 HTTPS client + FTP facade + IPC bridge 设计
421	- **N5 — main process Electron 能力**：`rewrite/src-electron/main/`（main 入口 + 已有 IPC handlers 模式）
422	  → 产出：main 进程已有能力 + HTTPS server 放在哪里
423	- **N6 — 质量规则 + 架构约束**：`codestable/quality/rewrite-quality-rules.md`（R5/R6/R10）+ `codestable/architecture/boundary-northbound-collaboration-delivery.md`
424	  → 产出：northbound 边界约束清单
425	
426	**Wave 2（主线程设计）：** 框架设计，不写完整实现
427	
428	**Wave 3（3 agent 自检）：**
429	- **SC1 — 边界合规**：对照 R5/R6/R10 确认 main/renderer 分层正确
430	- **SC2 — 与 S001 决策一致性**：对照 7 条已拍板决策
431	- **SC3 — 接口覆盖度**：对照 §十三 全量清单确认框架覆盖
432	
433	**边界护栏：** R5 + R6 + R10 […]

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

> TOOL

tool_use Glob
id: call_ff750b5691f347aea74e1751
```json
{
  "pattern": "codestable/features/**/northbound*"
}
```

> TOOL

tool_use Glob
id: call_83ce697aa27047daae66038e
```json
{
  "pattern": "codestable/features/**/*northbound*design*"
}
```

> TOOL

tool_use Grep
id: call_9d555280b0204739a89dfcca
```json
{
  "pattern": "northbound.*design",
  "path": "/mnt/d/code/frontend/dongfanghong/codestable",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: call_9d555280b0204739a89dfcca
```
Found 23 files
codestable/features/rewrite-storage-local-baseline/rewrite-storage-local-baseline-checklist.yaml
codestable/features/rewrite-connection/rewrite-connection-design.md
codestable/architecture/rewrite-connection-transport-boundary.md
codestable/architecture/rewrite-connection-platform-bridge.md
codestable/architecture/rewrite-feature-interaction-matrix.md
codestable/architecture/rewrite-feature-boundaries.md
codestable/architecture/rewrite-system-architecture.md
codestable/features/rewrite-result/rewrite-result-checklist.yaml
codestable/features/rewrite-result/rewrite-result-design.md
codestable/features/rewrite-scoe/rewrite-scoe-design.md
codestable/compound/2026-05-06-outbound-routing-and-response-decisions.md
codestable/features/rewrite-scoe/rewrite-scoe-checklist.yaml
codestable/compound/2026-05-06-ta[REDACTED_SK].md
codestable/features/rewrite-receive/rewrite-receive-design.md
codestable/architecture/rewrite-thin-ui-runtime-wiring.md
codestable/architecture/rewrite-shared-tooling-app-shell-ownership.md
codestable/architecture/rewrite-platform-api-surface-reduction.md
codestable/architecture/rewrite-pre-design-gate-and-sequencing.md
codestable/features/rewrite-frame/rewrite-frame-design.md
codestable/architecture/rewrite-shared-tooling-audit-plan.md
codestable/compound/2026-04-29-rewrite-domain-order-and-first-batches.md
codestable/compound/2026-04-28-northbound-overlap-and-gap-map.md
codestable/compound/2026-04-24-post-step3-review-and-execution-gating.md
```

> TOOL

tool_result
id: call_ff750b5691f347aea74e1751
```
No files found
```

> TOOL

tool_result
id: call_83ce697aa27047daae66038e
```
No files found
```

> TOOL

tool_use Glob
id: call_e58da76f46414d06980fcb8d
```json
{
  "pattern": "codestable/features/rewrite-result/*"
}
```

> TOOL

tool_use Read
id: call_5743f5323dc94d98859d3b59
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/compound/2026-04-28-northbound-overlap-and-gap-map.md"
}
```

> TOOL

tool_result
id: call_5743f5323dc94d98859d3b59
```
1	# Northbound Overlap And Gap Map
2	
3	Status: discussion draft
4	
5	Scope: northbound overlap workshop. This document records overlap, gap, internal decisions, and questions for later customer clarification. It does not define interface schema and does not design implementation modules.
6	
7	## 1. Baseline Inputs
8	
9	Evidence:
10	
11	- Rewrite baseline requires preserving legacy visible capabilities by default, while not inheriting old organization/state coupling/Electron boundary directly: `codestable/compound/2026-04-28-rewrite-scope-default-preserve.md:19-24`, `37-54`.
12	- Target structure already separates `task`, `status`, `result`, `report`, and `northbound`; northbound is an independent boundary, not an alias of task/status/report: `codestable/architecture/rewrite-target-structure.md:46-73`, `229-247`.
13	- Quality rules explicitly prohibit three false equivalences: old send task equals northbound task, history/CSV equals TestReport, serial/network target equals device/deviceId: `codestable/quality/rewrite-quality-rules.md:188-201`.
14	- Legacy inventory is a static fact and oracle map, not a runtime oracle; real serial/network/SCOE/center/FTP/package validation has not been completed: `easysdd/compound/2026-04-27-legacy-feature-inventory-and-oracle-map.md:16-21`.
15	- Customer documents define the northbound main surface as HTTP/REST plus FTP, with task dispatch/control/result/file/report, device/status/alarm/heartbeat concerns: `refactor/docs/甲方文档/集成测试系统与各二级子系统接口设计-拆分/01-协议与公共规则.md:33-51`, `04-任务主链.md:12-21`, `05-结果、文件与报告回传.md:12-16`, `07-运维控制与链路保活.md:11-18`.
16	- The later-connection checklist narrows the likely practical mainline to task receive, task start/stop, status, case result, task result, JSON report, and report delivery: `后面对接所需功能清单.md:109-115`, `554-581`.
17	
18	Inference: […]

> TOOL

tool_result
id: call_e58da76f46414d06980fcb8d
```
codestable/features/rewrite-result/rewrite-result-design.md
codestable/features/rewrite-result/rewrite-result-checklist.yaml
codestable/features/rewrite-result/result-report-brainstorm.md
```

> TOOL

tool_use Read
id: call_7ed9c61e99dc4db7ab48f5c2
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-result/result-report-brainstorm.md"
}
```

> TOOL

tool_result
id: call_7ed9c61e99dc4db7ab48f5c2
```
1	---
2	doc_type: brainstorm
3	feature: rewrite-result
4	date: 2026-05-12
5	status: finalized
6	summary: result-report brainstorm，修正后的 MVP 方案。大幅简化已有 design 中的过度设计。
7	---
8	
9	# Result-Report Brainstorm (2026-05-12)
10	
11	## 1. 已有 design 评估
12	
13	已有 `rewrite-result-design.md`（530 行）和 `rewrite-result-checklist.yaml`。经 code-reviewer + critic 双轮自检，确认以下问题：
14	
15	| 项目 | 已有 design 的做法 | 问题 |
16	|------|-------------------|------|
17	| CaseResult | 独立类型，含 kind/verdictSource/summary/stepDetails/lifecycle | 与 TaskExecutionSummary 重叠，pass/fail 判断是纯函数不需要独立类型 |
18	| TaskResultSummary | 跨执行聚合（totalCases/per-kind counts/lastResult） | 无 MVP 消费者，task 已有 history + statistics，YAGNI |
19	| ResultReadModel | 独立 read model + query filter | task selectors 已提供 instance/progress/history/statistics，多余 |
20	| ResultAggregationRule | 可配置策略（any-fail/all-fail/threshold + skip/timeout/stopped policy） | MVP 用最简规则，不需要可配置策略 |
21	| Report 模板系统 | 未设计但 brainstorm 曾提议"模板引擎+可配置映射" | 甲方格式未确认，建模板引擎是为不存在的需求做优化 |
22	| TaskInstanceCompletion 事件 | 假设 task 会 emit 此事件 | task 没有事件发射机制，也不需要新建——用 onSettled() + runtime 编排即可 |
23	| 报告素材 | result + storage + settings + frame | MVP 只需 TaskInstanceState |
24	| Checklist 步骤数 | 22 步 | 远超 Lane B 8 步上限 |
25	
26	## 2. 修正后的 MVP 方案
27	
28	### 2.1 要做什么
29	
30	**result/ feature（结果收集）**：
31	- runtime 编排：task 终态时（onSettled resolve），runtime […]

> TOOL

tool_use Read
id: call_0386480867d24619aae5504f
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-result/rewrite-result-design.md",
  "limit": 40
}
```

> TOOL

tool_result
id: call_0386480867d24619aae5504f
```
1	---
2	doc_type: feature-design
3	feature: rewrite-result
4	status: draft
5	date: 2026-05-06
6	summary: 东方红上位机重写中 result feature 的 owner scope、核心类型、结果聚合规则、与 task/send/receive/storage/status/report/northbound 的交互契约和边界定义。
7	---
8	
9	# Rewrite result feature design
10	
11	## 1. Direct contract
12	
13	本设计只依据以下正式工件判断范围和完成度：
14	
15	1. `codestable/compound/2026-04-28-rewrite-execution-charter.md`
16	2. `codestable/architecture/rewrite-target-structure.md`
17	3. `codestable/architecture/rewrite-system-architecture.md`
18	4. `codestable/architecture/rewrite-feature-boundaries.md`
19	5. `codestable/architecture/rewrite-feature-interaction-matrix.md`
20	6. `codestable/quality/rewrite-quality-rules.md`
21	7. `codestable/quality/rewrite-review-checklist.md`
22	8. `codestable/features/rewrite-task/rewrite-task-design.md`
23	9. `codestable/features/rewrite-send/rewrite-send-design.md`
24	10. `codestable/features/rewrite-receive/rewrite-receive-design.md`
25	11. `codestable/features/rewrite-storage-local-baseline/rewrite-storage-local-baseline-design.md`
26	12. `codestable/compound/2026-05-06-ta[REDACTED_SK].md`
27	13. `codestable/compound/2026-05-06-outbound-routing-and-response-decisions.md`
28	
29	`codestable/architecture/rewrite-target-structure.md` 仍是 canonical 架构基线。task design 固定 task 输出 TaskInstanceCompletion 作为内部 lifecycle 事实；send design 固定 send 输出 SendResult；receive design 固定 receive 输出 parsed field values 和 trigger candidate。
30	
31	## 2. Boundary guards
32	
33	- 本轮是 Lane A design，只产出 design/checklist，不写实现代码。
34	- result owns 内部结果事实（case result truth、task result truth、执行摘要、结果归因和聚合规则）。
35	- result does not own report 文件生成、HTTP/FTP 交付、外部响应语义、外部 schema/枚举/错误码、northbound delivery closure。
36	- result ≠ report。result 定义内部事实；report 从 result + storage 读取素材生成文件。
37	- result ≠ storage。result 定义事实模型；storage 负责持久化。
38	- result 不冻结 northbound 外部 schema、错误码或 TestReport 格式。
39	- result 不拥有 send/receive/task/connection/SCOE 的运行事实，只消费它们的 public event/selector。
40	- 跨 feature 只通过 public API、runtime 编排、显式事件或只读 selector 交互。
```

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

> TOOL

tool_use Read
id: call_4f4628e54f3f4b57a5b26f5e
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-command-ingress/command-ingress-brainstorm.md"
}
```

> TOOL

tool_use Read
id: call_15abc91958ae4719bd4da0d4
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-command-ingress/command-ingress-design.md",
  "limit": 80
}
```

> TOOL

tool_result
id: call_15abc91958ae4719bd4da0d4
```
1	# command-ingress design
2	
3	> 日期：2026-05-09
4	> 状态：draft
5	> 直接合同：command-ingress-brainstorm.md
6	> 依赖：task（types 已确认）、connection（API 已确认）、frame（API 已确认）
7	
8	## 类型引用约定
9	
10	本 design 引用的 task 类型以 **task-real design**（`codestable/features/rewrite-task/task-real-design.md`）为最终真相源。task-real 尚未实施，以下映射标注了当前代码 vs task-real design 的差异。command-ingress 实施必须等 task-real 实施完成后才能开始。
11	
12	| 当前代码名 | task-real design 名 | 变更性质 | 来源 |
13	|---|---|---|---|
14	| `TaskSchedulingMode` | `ScheduleDriver` discriminated union | 替代 | task-real design §1.1 |
15	| `WaitCondition` | `ConditionTerm`（新增 `logicOperator`） | 扩展 | task-real design §1.1 |
16	| `WaitConditionStepConfig.condition` | `WaitConditionConfig.conditions` 数组 | 单→数组 | task-real design §1.2 |
17	| `WaitConditionStepConfig.timeoutMs: number` | `WaitConditionConfig.timeoutMs?: number` | 必选→可选 | task-real design §1.2 |
18	| `SendStepDefinition.sendConfig` | `TaskStepDefinition.config` | 统一字段名 | task-real design §1.2 |
19	| `WaitConditionStepDefinition.waitConfig` | `TaskStepDefinition.config` | 统一字段名 | task-real design §1.2 |
20	| `DelayStepDefinition.delayConfig` | `TaskStepDefinition.config` | 统一字段名 | task-real design §1.2 |
21	| `TaskDefinition.schedulingMode` | `TaskDefinition.schedule: ScheduleDriver` | 替代 | task-real design §1.2 |
22	| `TaskDefinition.triggerSource` | 移除 | 删除 | task-real design §1.2 |
23	| `TaskDefinition.targetId?` | 移到 `SendStepConfig.targetId` | 下沉 | task-real design §1.2 |
24	| **不存在** | `TaskDefinition.fieldVariations` | **新增** | task-real design §1.2 | […]

> TOOL

tool_result
id: call_4f4628e54f3f4b57a5b26f5e
```
1	# command-ingress brainstorm
2	
3	> 日期：2026-05-09
4	> 状态：结论已锁定，ready for cs-feat-design
5	> Lane：Lane B（单 feature，不拆 roadmap）
6	> 依赖：task-real（brainstorm 已锁定）、connection-complete（TCP/UDP adapter）
7	
8	## 结论
9	
10	command-ingress 是统一的**外部系统命令入站 feature**，接收 SCOE TCP 协议和新甲方 HTTPS 接口的指令，解析协议后分发执行并回传结果。
11	
12	核心设计选择：
13	
14	1. **消费者链入站分发**：routingTick 定义 `TransportEventConsumer` 接口，依次调用消费者（command-ingress 先于 receive），每个消费者返回 `{consumed, remaining}`。routingTick 不知道也不评估任何领域条件
15	2. **两种命令路由**：发帧+等条件类走 task 执行引擎（构造 TaskDefinition），查询/状态类走 handler 直接处理
16	3. **SCOE 6 种命令全部可映射**：4 种直接 handler，2 种翻译为 TaskDefinition
17	4. **不自建帧列表、不自建条件系统、不建执行器框架**
18	5. **多客户端保留但不加并发控制**（复刻旧系统行为）
19	6. **回应机制极简**：只有 UDP 成功帧，无失败帧，无重试
20	
21	## 事实与证据
22	
23	### 旧 SCOE 系统（22 文件）
24	
25	来源：`src/composables/scoe/`、`src/stores/scoeStore.ts`、`src/utils/receive/scoeFrame.ts`、`src/types/scoe/`
26	
27	#### 命令生命周期（6 阶段）
28	
29	```
30	TCP Server 接收指令帧
31	  → 功能码验证（SCOE 标识 + 指令码，4 字节）
32	  → 校验和验证（sum % 256）
33	  → 参数提取（按 offset/length 从字节流提取 → receiveCode 选项匹配）
34	  → 命令分发（6 种执行器策略映射）
35	  → 执行（发帧/状态操作/查询 + 异步轮询条件等待）
36	  → 回应（UDP 发 successFrameId 帧 或 只记录错误状态）
37	```
38	
39	#### 6 种命令分类
40	
41	| 命令 | 分类 | 旧行为 | 新系统映射 |
42	|------|------|--------|-----------|
43	| LOAD_SATELLITE_ID | 状态操作 | 查卫星配置→验证→加载帧配置→更新状态 | handler 直接操作 |
44	| UNLOAD_SATELLITE_ID | 状态操作 | 清除状态→重置统计 | handler 直接操作 |
45	| HEALTH_CHECK | 查询 | 返回连接状态+健康状态快照 | handler 返回 […]

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

> TOOL

tool_use Agent
id: call_4de31534aa6b46aaa0137c41
```json
{
  "description": "Explore northbound current state",
  "subagent_type": "Explore",
  "prompt": "Thorough exploration of the northbound-related current state in the codebase. I need to understand what actually exists in code right now.\n\nCheck these areas:\n\n1. **command-ingress feature** — `rewrite/src/features/command-ingress/` — what files exist? Is it implemented or just designed? Check the actual code structure, any stubs for HTTPS/northbound.\n\n2. **result feature** — `rewrite/src/features/result/` — what's implemented? Specifically check result-service.ts, judge.ts, any collector logic.\n\n3. **task feature** — `rewrite/src/features/task/` — specifically task-service.ts, check onSettled() API, step result emission, any hook/callback mechanism.\n\n4. **platform facade** — `rewrite/src/platform/` — check for any HTTPS server, HTTP client, FTP facade, or northbound-related platform APIs. What transport/file APIs exist?\n\n5. **runtime** — `rewrite/src/runtime/` — check routing-tick.ts for TransportEventConsumer chain, feature-wiring.ts for how features are wired, any northbound wiring.\n\n6. **main process** — `rewrite/src-electron/main/` — check for any HTTPS server, HTTP handlers, northbound-related IPC.\n\n7. **Electron preload** — `rewrite/src-electron/preload/` — check for any northbound-exposed APIs.\n\nFor each area, report:\n- What files exist\n- What's actually implemented vs stub/empty\n- Any northbound-specific code or comments\n\nBe thorough — search for keywords like \"northbound\", \"https\", \"ftp\", \"setTestTask\", \"testCaseResult\", \"msgReport\" across the codebase too."
}
```

> TOOL

tool_result
id: call_4de31534aa6b46aaa0137c41
```
Perfect! Now I have enough information. Let me compile my comprehensive findings:

## Northbound Current State Exploration Report

Based on a thorough exploration of the codebase, here's what actually exists today:

---

## 1. COMMAND-INGRESS FEATURE (`rewrite/src/features/command-ingress/`)

**Status: FULLY IMPLEMENTED for SCOE protocol, NO northbound/HTTPS stubs**

**Files that exist:**
- `/mnt/d/code/frontend/dongfanghong/rewrite/src/features/command-ingress/core/` - Complete implementation
- `/mnt/d/code/frontend/dongfanghong/rewrite/src/features/command-ingress/adapters/scoe-protocol-adapter.ts` - Full SCOE TCP protocol adapter
- `/mnt/d/code/frontend/dongfanghong/rewrite/src/features/command-ingress/services/` - Command ingress service
- `/mnt/d/code/frontend/dongfanghong/rewrite/src/features/command-ingress/composables/` - UI composables

**What's implemented:**
- SCOE binary protocol adapter (TCP/serial transport)
- 6 command functions: `load_satellite_id`, `unload_satellite_id`, `health_check`, `link_check`, `send_frame`, `read_file_and_send`
- Command → TaskDefinition translation (for `send_frame` and `read_file_and_send`)
- Full state machine for SCOE lifecycle
- TransportEventConsumer chain integration

**What's NOT implemented:**
- NO HTTPS server
- NO northbound protocol adapter
- NO stub for northbound entry point

**Placeholder found:**
- `/mnt/d/code/frontend/dongfanghong/rewrite/src/features/command-ingress/composables/use-task-report.ts:7-9` - `reportTasks()` throws "Not implemented"
- `/mnt/d/code/frontend/dongfanghong/rewrite/src/features/command-ingress/composables/use-central-docking.ts:26-28` - `connect()` throws "Not implemented" (for HTTPS docking)

---

## 2. RESULT FEATURE (`rewrite/src/features/result/`)

**Status: MVP IMPLEMENTED - Complete verdict logic, passive collection**

**Files that exist:**
- `/mnt/d/code/frontend/dongfanghong/rewrite/src/features/result/core/judge.ts` - Full verdict logic
- `/mnt/d/code/frontend/dongfanghong/rewrite/src/features/result/services/result-service.ts` - Complete service
- `/mnt/d/code/frontend/dongfanghong/rewrite/src/features/result/core/types.ts` - All types defined

**What's implemented:**
- `judgeCaseVerdict()` - Returns `passed/failed/stopped` based on step results […]

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