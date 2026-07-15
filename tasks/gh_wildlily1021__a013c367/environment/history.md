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

> DEVELOPER

可以，先写文档，不然直接进容易漏

> AGENT

好，按 case 2 落 brainstorm note。先建目录。

> TOOL

tool_use Bash
id: call_0eed8bbec44e4f9eb9e471c7
```json
{
  "command": "ls /mnt/d/code/frontend/dongfanghong/codestable/features/ | head -20",
  "description": "List existing feature directories"
}
```

> TOOL

tool_result
id: call_0eed8bbec44e4f9eb9e471c7
```
2026-04-23-ta[REDACTED_SK]/
2026-04-23-ta[REDACTED_SK]/
2026-04-23-ta[REDACTED_SK]/
2026-04-23-ta[REDACTED_SK]/
2026-04-23-ta[REDACTED_SK]/
2026-04-28-current-system-solution-report/
2026-05-07-runtime-wiring/
2026-05-08-expression-engine/
2026-05-24-settings-page/
bootstrap/
rewrite-command-ingress/
rewrite-connection/
rewrite-display/
rewrite-frame/
rewrite-receive/
rewrite-result/
rewrite-scoe/
rewrite-send/
rewrite-settings/
rewrite-status/
```

> TOOL

tool_use Bash
id: call_6abc031e32b44ee6b2ca4aab
```json
{
  "command": "mkdir -p /mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound",
  "description": "Create northbound feature directory"
}
```

> TOOL

tool_result
id: call_6abc031e32b44ee6b2ca4aab
```
(Bash completed with no output)
```

> TOOL

tool_use Write
id: call_c9469c6b4f624f23b5601b24
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-brainstorm.md",
  "content": "---\ndoc_type: feature-brainstorm\nfeature: rewrite-northbound\nstatus: confirmed\nsummary: 甲方 HTTPS 闭环 — inbound translator（setTestTask→TaskDefinition）+ outbound translator（result→testCaseResultReport/msgReport）+ heartbeat/getSubSysState，平台层完全不含业务语义\ntags: [northbound, customer-integration, https, task-translation]\n---\n\n# Northbound Feature Brainstorm\n\n> Stage 0 | 2026-05-25 | 下一步：design\n\n## 想做什么、为什么\n\n甲方（集成测试系统）通过 HTTPS 接口控制我们的任务执行并接收结果上报。需要建 northbound feature 闭环这条链路：接收甲方指令 → 翻译为内部 TaskDefinition → 执行 → 收集结果 → 翻译为甲方格式 → POST 回传。\n\n**起点材料**：\n- `.sessions/2026-05-18-northbound-integration/S001-closed-loop-analysis.md` — 闭环分析 + 7 条架构决策已锁定 + 代码验证\n- `codestable/compound/2026-04-28-northbound-overlap-and-gap-map.md` — overlap/gap 分析（边界参考仍有效）\n- `codestable/features/rewrite-command-ingress/command-ingress-brainstorm.md` — SCOE→TaskDefinition 翻译模式可直接复用\n- `codestable/features/rewrite-result/result-report-brainstorm.md` — result MVP 已实现，被动 API\n\n**关键发现**：command-ingress 已实现完整的 SCOE 协议→TaskDefinition 翻译模式，northbound 的 inbound translator 可以复用相同思路。\n\n## 考虑过的方向\n\n### 方向 A：northbound 合并进 command-ingress\n- 描述：甲方 HTTPS 作为 command-ingress 的第二个 ProtocolAdapter\n- 价值：统一外部命令入口\n- 代价：command-ingress 膨胀；SCOE 是字节流 consumer chain 模式，甲方 HTTPS 是 JSON server 模式，入站机制完全不同；改动面大\n- 结论：否决。5/18 S001 已明确决策：northbound 独立 feature\n\n### 方向 B：northbound 独立 feature + 平台层严格分离（选定）\n- 描述：northbound 只做业务（翻译 + 会话 + 编排），HTTPS server/client 归 platform facade + main process，主进程不含任何甲方接口语义\n- 价值：甲方改接口只动 northbound feature 内的 types + translator；HTTPS 库换掉只动 platform + main；改动不跨层传播\n- 代价：需要先建 platform HTTPS facade（但这是基础设施投资，其他 feature 也会用到）\n- 结论：选定\n\n### 方向 C：先搭骨架等甲方 schema 全确认再实现\n- 描述：只建目录结构和接口定义，翻译层全部 stub\n- 价值：避免 schema 变动返工\n- 代价：MVP 6 接口映射已确认（testCase=task），翻译逻辑可以先用内部类型，schema 确认后只改映射层\n- 结论：否决。已确认的部分可以先做\n\n## 已敲定的设计点\n\n### 层级分离（已确认）\n\n```\nmain process     → 纯传输层，只认 raw HTTP（method/url/headers/body）\n                  不含任何甲方接口语义、不解析 JSON schema\npreload          → 暴露 IPC bridge\nplatform facade  → 封装为通用 HttpRequest/HttpResponse（不含甲方语义）\nnorthbound       → 唯一知道甲方接口的地方\n                  inbound translator + outbound translator + session 管理\n```\n\n改动传播路径：甲方改接口 → 只动 `northbound/core/types.ts` + 两个 translator → 其他层不动。\n\n### 类型策略（已确认）\n\n- 甲方接口类型只定义一次，在 […]

> TOOL

tool_result
id: call_c9469c6b4f624f23b5601b24
```
File created successfully at: /mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-brainstorm.md
```

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

> TOOL

tool_use Glob
id: call_6dd579ce418640749ee00211
```json
{
  "pattern": ".agent/skills/cs-feat-design/SKILL.md"
}
```

> TOOL

tool_result
id: call_6dd579ce418640749ee00211
```
.agent/skills/cs-feat-design/SKILL.md
```

> TOOL

tool_use Skill
id: call_5e477d2fe6e44111b22d641b
```json
{
  "skill": "cs-feat-design",
  "args": "codestable/features/rewrite-northbound/northbound-brainstorm.md"
}
```

> TOOL

tool_result
id: call_5e477d2fe6e44111b22d641b
```
Launching skill: cs-feat-design
```

> AGENT

启动 cs-feat-design。先做启动检查——并行读取必要材料。

> TOOL

tool_use Glob
id: call_b4ec67671a8e411fa3fd2b3a
```json
{
  "pattern": "codestable/features/rewrite-northbound/*design*"
}
```

> TOOL

tool_use Glob
id: call_801d1481d70d42219476b941
```json
{
  "pattern": "codestable/features/rewrite-northbound/*intent*"
}
```

> TOOL

tool_use Read
id: call_84129cacdfdd4489b9913caa
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/reference/shared-conventions.md"
}
```

> TOOL

tool_use Glob
id: call_f563ceafee5e4d9cac856940
```json
{
  "pattern": "codestable/architecture/*.md"
}
```

> TOOL

tool_result
id: call_84129cacdfdd4489b9913caa
```
1	# easysdd 共享口径
2	
3	本文件由 `easysdd-onboarding` 复制到项目的 `easysdd/reference/shared-conventions.md`。所有 easysdd 子技能在运行时用**项目相对路径** `easysdd/reference/shared-conventions.md` 引用本文件——这是跨子技能共享但不适合堆在单个技能里的规范的唯一权威版本。
4	
5	skill 本身不共享文件系统（每个 skill 是独立安装单元），所以共享口径不能放在某个 skill 内部被别的 skill 引用。放在"工作项目"里，对所有 skill 都可达。
6	
7	---
8	
9	## 0. 目录结构与路径命名
10	
11	onboarding 完成后，项目里应当存在如下骨架（`easysdd-onboarding` 负责搭建）：
12	
13	```
14	easysdd/
15	├── architecture/          架构中心目录
16	│   ├── DESIGN.md          架构总入口（索引 + 关键架构决定）
17	│   └── {slug}.md          子系统 / 模块架构 doc（由 easysdd-architecture-gen 产出）
18	├── features/              feature spec 聚合根
19	│   └── YYYY-MM-DD-{slug}/  每个 feature 一个目录
20	│       ├── {slug}-brainstorm.md  （可选）
21	│       ├── {slug}-design.md
22	│       ├── {slug}-checklist.yaml
23	│       └── {slug}-acceptance.md
24	├── issues/                issue spec 聚合根
25	│   └── YYYY-MM-DD-{slug}/  每个 issue 一个目录
26	│       ├── {slug}-report.md
27	│       ├── {slug}-analysis.md    （根因不显然时才有）
28	│       └── {slug}-fix-note.md
29	├── compound/              沉淀类文档统一目录
30	│   └── YYYY-MM-DD-{doc_type}-{slug}.md
31	│                          doc_type ∈ {learning, trick, decision, explore}
32	├── tools/                 跨工作流共享脚本（由 onboarding 从技能包释放）
33	└── reference/             共享参考文档（由 onboarding 从技能包释放，即本文件所在目录）
34	```
35	
36	### 命名规则
37	
38	- feature 目录：`easysdd/features/YYYY-MM-DD-{slug}/`，日期用创建当天
39	- issue 目录：`easysdd/issues/YYYY-MM-DD-{slug}/`，日期用报告当天
40	- 沉淀类文档：`easysdd/compound/YYYY-MM-DD-{doc_type}-{slug}.md`，日期用**归档当天**（不是问题发生当天）
41	- 架构文档：`easysdd/architecture/{type}-{slug}.md`（长效地图，不带日期前缀）；总入口始终叫 `DESIGN.md`
42	- `AGENTS.md` 在项目根目录，**不在 `easysdd/` 里**
43	
44	### 架构 doc 的分组规则（同类聚合）
45	
46	`easysdd/architecture/` 下的 doc 用文件名**第一段**（首个连字符之前）作为类型标记：`ui-chat.md` 和 `ui-events.md` 同属 `ui` 类，`api-routing.md` 自成 `api` […]

> TOOL

tool_result
id: call_b4ec67671a8e411fa3fd2b3a
```
No files found
```

> TOOL

tool_result
id: call_801d1481d70d42219476b941
```
No files found
```

> TOOL

tool_result
id: call_f563ceafee5e4d9cac856940
```
codestable/architecture/overview-architecture-decision-frame.md
codestable/architecture/analysis-current-architecture-gap.md
codestable/architecture/boundary-desktop-capability-access.md
codestable/architecture/boundary-runtime-state-ownership.md
codestable/architecture/topology-receive-send-mainlines.md
codestable/architecture/domain-ta[REDACTED_SK].md
codestable/architecture/domain-scoe-position.md
codestable/architecture/analysis-target-architecture-gap-round-2.md
codestable/architecture/boundary-northbound-collaboration-delivery.md
codestable/architecture/DESIGN.md
codestable/architecture/rewrite-shared-tooling-audit-plan.md
codestable/architecture/rewrite-pre-design-gate-and-sequencing.md
codestable/architecture/rewrite-platform-api-surface-reduction.md
codestable/architecture/rewrite-shared-tooling-app-shell-ownership.md
codestable/architecture/rewrite-platform-app-shell-file-dialog.md
codestable/architecture/rewrite-thin-ui-runtime-wiring.md
codestable/architecture/rewrite-ui-style-baseline.md
codestable/architecture/rewrite-system-architecture.md
codestable/architecture/rewrite-feature-boundaries.md
codestable/architecture/rewrite-feature-interaction-matrix.md
codestable/architecture/rewrite-connection-platform-bridge.md
codestable/architecture/rewrite-connection-transport-boundary.md
codestable/architecture/rewrite-target-structure.md
```

> TOOL

tool_use Read
id: call_a901fb6ff1bc45b0bd748928
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/architecture/boundary-northbound-collaboration-delivery.md"
}
```

> TOOL

tool_use Read
id: call_a70b0365225f411db8d19b60
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/architecture/rewrite-feature-boundaries.md",
  "limit": 60
}
```

> TOOL

tool_use Read
id: call_3fe2728cc6ae4de497bc1060
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/architecture/rewrite-target-structure.md",
  "limit": 80
}
```

> TOOL

tool_result
id: call_3fe2728cc6ae4de497bc1060
```
1	---
2	doc_type: architecture
3	type: rewrite-target-structure
4	status: draft
5	date: 2026-04-28
6	summary: Batch 0 architecture baseline, target source structure, and dependency rules for the full rewrite. This document translates existing architecture boundary memos into a practical directory and dependency map without defining schemas or implementation batches.
7	tags:
8	  - rewrite
9	  - target-structure
10	  - directory
11	  - boundary
12	  - electron
13	---
14	
15	# Rewrite target structure
16	
17	## 1. Purpose
18	
19	本文定义全面重写时的目标目录结构、职责归口和依赖方向。
20	
21	本文不做以下事情：
22	
23	- 不定义字段 schema。
24	- 不写接口契约。
25	- 不制定迁移批次。
26	- 不要求一次性创建所有空目录。
27	- 不把旧代码热点直接翻译成新目录。
28	
29	本文继承当前范围口径：旧功能默认保留，重写重点是代码质量、模块边界、状态归口和 Electron 边界。`codestable/compound/2026-04-28-rewrite-scope-default-preserve.md`
30	
31	## Batch 0 Architecture Baseline
32	
33	本文是 Batch 0 的整体架构基线。后续每个功能域进入 `cs-feat-design` 前，都必须把本文列为直接合同或边界护栏，并说明本批如何遵守本文的目录、依赖、状态和平台边界。
34	
35	Batch 0 只固定后续功能必须遵守的架构骨架：
36	
37	- 顶层目录固定为 `app / platform / shared / features / runtime / pages / widgets`。
38	- feature 内部通用分层固定为 `core / services / state / adapters / composables / components / fixtures`，按实际职责创建，不为了填满模板而建空层。
39	- feature public API 只是跨 feature 访问边界，不是必须新增的接口层；外部不得 import 其他 feature 的内部 `state`、`adapters`、内部 composable、内部 service 实现或私有 helper。
40	- `runtime/` 只在应用生命周期、平台资源装配或跨 feature 编排确有需要时出现，不是新的全局业务中心。
41	- renderer、platform、preload、main 的边界按本文和质量规则执行；现有 main 业务化只作为迁移风险处理，不作为新架构目标。
42	- 状态必须分清静态资产、运行事实、统计 read model […]

> TOOL

tool_result
id: call_a70b0365225f411db8d19b60
```
1	---
2	doc_type: architecture
3	type: rewrite-feature-boundaries
4	status: draft
5	date: 2026-04-29
6	summary: Feature boundary and owner pre-screen for the Dongfanghong rewrite before any cs-feat-design work. This document records owner responsibilities, input/output direction, runtime fact ownership, validation posture, and high-risk cross-feature seams without defining schemas or feature internals.
7	tags:
8	  - rewrite
9	  - feature-boundary
10	  - owner
11	  - pre-design
12	  - batch-0
13	---
14	
15	# Rewrite feature boundaries
16	
17	## 1. Scope
18	
19	本轮是全局预设计阶段的 feature 边界与 owner 初筛，目的是在进入任何 `cs-feat-design` 前，先固定每个 feature 的职责边界、输入输出方向、运行事实归属、验证风险和明显的合并/拆分风险。
20	
21	Direct contract:
22	
23	- `AGENTS.md`
24	- `codestable/compound/2026-04-28-rewrite-execution-charter.md`
25	- `codestable/architecture/rewrite-target-structure.md`
26	- `codestable/architecture/rewrite-system-architecture.md`
27	- `codestable/quality/rewrite-quality-rules.md`
28	- `codestable/quality/rewrite-review-checklist.md`
29	
30	Boundary guards:
31	
32	- `codestable/compound/2026-04-28-northbound-overlap-and-gap-map.md`
33	- `easysdd/compound/2026-04-27-legacy-feature-inventory-and-oracle-map.md`
34	- 当前 `src` 和 `src-electron` 旧代码事实，只作为 evidence、oracle 候选和风险证据。
35	
36	Non-goals:
37	
38	- 不进入任何 feature 内部详细设计。
39	- 不写字段 schema、事件 payload、接口签名、northbound 字段、枚举或错误码。
40	- 不写 receive / send / task / SCOE 的详细实现。
41	- 不做代码移动，不实现业务代码。
42	- 不把旧页面、旧 store、旧 composable、旧 IPC、旧 main handler 组织自动升级为目标架构。
43	
44	Canonical rule:
45	
46	- `codestable/architecture/rewrite-target-structure.md` 仍是目录、依赖方向和 feature 归口的 canonical 架构基线。本文只做 owner 初筛和后续 feature design 的入口材料。
47	
48	## 2. Legacy […]

> TOOL

tool_result
id: call_a901fb6ff1bc45b0bd748928
```
1	---
2	doc_type: architecture
3	status: draft
4	summary: 北向协同应由独立边界层统一承接接入、投影和交付，避免外部对象与内部骨架对象混同。
5	tags:
6	  - 北向协同
7	  - 对外交付
8	  - 投影边界
9	---
10	
11	# 中心协同接入与对外交付边界
12	
13	> 状态：首轮正文
14	> 阶段：03-architecture
15	> 作用：在继承 `04-运行主状态与状态边界.md` 到 `08-功能清单与目标架构对比（第二轮）.md` 已拍板结论的前提下，只补“中心如何与内部统一运行骨架发生协同”的北向边界，明确中心侧请求由谁承接、内部事实如何投影为对外状态 / 心跳 / 结果 / 报告，以及对外响应与交付语义由谁统一归口。
16	
17	## 第一部分：本文要解决的北向协同边界问题
18	
19	### 当前事实
20	
21	- `04-运行主状态与状态边界.md` 已经拍板：未来内部运行骨架围绕 `子系统运行主体`、`中心任务上下文`、`用例执行上下文`、`生命周期控制状态`、`结果归口状态` 组织。
22	- `05-接收主链与发送主链组织方式.md` 已经拍板：接收主链和发送主链都只处理显式输入 / 输出，不再通过共享状态回读补齐自身语义。
23	- `06-任务系统归口方式.md` 已经拍板：任务系统是独立能力域，负责推进任务和用例的正式运行事实，但它不是对外协同边界本身。
24	- `07-SCOE 的架构位置.md` 已经拍板：领域模块只能通过显式边界接入统一骨架，不能绕过统一运行骨架和任务系统直接定义总状态面。
25	- `08-功能清单与目标架构对比（第二轮）.md` 已经明确：当前真正还缺的，不是内部骨架，而是“中心协同接入与对外交付边界”。
26	- [后面对接所需功能清单.md](D:/code/frontend/dongfanghong/后面对接所需功能清单.md) 中真正面对中心侧协同的能力，至少包括：
27	  - 子系统身份信息
28	  - 最小设备信息
29	  - 接收测试任务
30	  - 启动 / 停止任务
31	  - 状态查询响应
32	  - 心跳
33	  - 用例结果上报
34	  - JSON 报告生成后的交付
35	  - 基础响应与错误反馈
36	
37	### 判断 / 倾向
38	
39	本文只回答以下问题：
40	
41	- 中心侧请求 / 查询 / 控制 / 保活 / 结果接收，由哪一层统一承接。
42	- 内部统一运行骨架如何被投影成对外可见状态、心跳、用例结果和任务报告。
43	- 用例结果上报与任务报告交付分别属于哪一层职责。
44	- 对外成功 / 失败 / 拒绝 / 不可执行 / 异常等响应语义由哪一层统一归口。
45	- 外部协同对象与内部骨架对象之间是什么关系。
46	
47	本文不回答以下问题：
48	
49	- 接口字段 schema。
50	- 心跳报文结构。
51	- 报告 JSON 字段全集。
52	- 上传方式、传输协议、重试实现细节。
53	- 具体接口命名。
54	
55	先明确：北向协同边界不是谁。
56	
57	- 不是任务系统本身。
58	- 不是统一运行主状态本身。
59	- 不是接收主链或发送主链本身。
60	- 不是页面工作台。
61 […]

> AGENT

架构文档读完了。现在需要看代码级的实际 API 签名——并行派 agent 查关键实现细节。

> TOOL

tool_use Agent
id: call_931a46230bf2489fbea9c7ec
```json
{
  "description": "Task service API signatures",
  "prompt": "Read the following files and extract the EXACT public API signatures, types, and key implementation details:\n\n1. `rewrite/src/features/task/services/task-service.ts` — Extract:\n   - The full createTaskService factory function signature and return type (all public methods)\n   - onSettled() exact signature and implementation (how resolve works, Set of resolvers)\n   - Any event/callback mechanism\n   - How task instances are stored and accessed\n\n2. `rewrite/src/features/task/services/task-iteration-loops.ts` — Extract:\n   - Where step results are written (the addStepResult calls around lines 162, 171, 222)\n   - The exact context/callback pattern if any\n   - How the loop progresses\n\n3. `rewrite/src/features/task/core/types.ts` — Extract:\n   - TaskInstanceState type (all fields, especially stepResults)\n   - TaskStepResult union type\n   - TaskDefinition type\n   - ScheduleDriver type\n\nReport the EXACT type signatures and function signatures, not summaries. Include line numbers.",
  "subagent_type": "Explore"
}
```

> TOOL

tool_use Agent
id: call_55b303a6cd8b4ad5a5750621
```json
{
  "description": "Result + platform + wiring APIs",
  "prompt": "Read the following files and extract the EXACT public API signatures and types:\n\n1. `rewrite/src/features/result/services/result-service.ts` — Full createResultService factory, all public methods with signatures\n\n2. `rewrite/src/features/result/core/types.ts` — All exported types\n\n3. `rewrite/src/features/result/core/judge.ts` — judgeCaseVerdict signature and return type\n\n4. `rewrite/src/platform/index.ts` — How facades are organized and exported\n\n5. `rewrite/src/platform/transport.ts` — TransportFacade full interface (all methods)\n\n6. `rewrite/src/platform/files.ts` — FileFacade full interface\n\n7. `rewrite/src/runtime/feature-wiring.ts` — The RewriteWiredFeatures interface and wireFeatures function\n\n8. `rewrite/src/runtime/routing-tick.ts` — The full routingTick function, especially the consumer chain part\n\n9. `rewrite/src/runtime/consumer-chain.ts` — TransportEventConsumer interface\n\n10. `rewrite/src/features/command-ingress/services/command-ingress-service.ts` — How command-ingress service is structured\n\nReport EXACT type signatures and interfaces with line numbers. I need these to design a new feature that integrates with existing code.",
  "subagent_type": "Explore"
}
```

> TOOL

tool_result
id: call_931a46230bf2489fbea9c7ec
```
Perfect! I have all three files. Let me extract the exact public API signatures, types, and implementation details as requested.

## EXTRACTED API SIGNATURES AND IMPLEMENTATION DETAILS

### 1. `/mnt/d/code/frontend/dongfanghong/rewrite/src/features/task/services/task-service.ts`

#### **Public Interface Types (Lines 24-52)**

```typescript
export interface TaskReader {
  getSnapshot(): TaskStateSnapshot;
  getInstance(instanceId: string): TaskInstanceState | undefined;
  getProgress(instanceId: string): TaskProgress | undefined;
  getStatistics(): TaskStatisticsSnapshot;
}

export interface TaskService extends TaskReader {
  createTask(definition: TaskDefinition): TaskInstanceState;
  startTask(instanceId: string): void;
  pauseTask(instanceId: string): void;
  resumeTask(instanceId: string): void;
  stopTask(instanceId: string): void;
  stopAll(): number;
  removeTask(instanceId: string): void;
  retryTask(sourceInstanceId: string): TaskInstanceState | undefined;
  updateTask(instanceId: string, definition: TaskDefinition): TaskInstanceState | undefined;
  onSettled(instanceId: string): Promise<void>;
}

export interface CreateTaskServiceOptions {
  readonly sendService: SendServiceProvider;
  readonly receiveEventSource: ReceiveEventSource;
  readonly timerService?: unknown;
  readonly fieldValueProvider?: () => Readonly<Record<string, number | string | null>>;
  readonly state?: TaskStateContainer;
  readonly now?: () => string;
}
```

#### **Factory Function Signature (Line 57)**

```typescript
export function createTaskService(options: CreateTaskServiceOptions): TaskService
```

#### **onSettled() Exact Implementation (Lines 269-281)**

```typescript
async onSettled(instanceId) {
  const inst = state.getInstance(instanceId);
  if (!inst || isTerminal(inst.lifecycle)) return;

  await new Promise<void>((resolve) => {
    let resolvers = settleResolvers.get(instanceId);
    if (!resolvers) {
      resolvers = new Set();
      settleResolvers.set(instanceId, resolvers);
    }
    resolvers.add(resolve);
  });
}
```

**Key Implementation Details:**
- **Set of Resolvers**: `settleResolvers` is a […]

> TOOL

tool_result
id: call_55b303a6cd8b4ad5a5750621
```
Here are the exact public API signatures and types extracted from the requested files:

## 1. `/mnt/d/code/frontend/dongfanghong/rewrite/src/features/result/services/result-service.ts`

**ResultService interface (lines 5-10):**
```typescript
export interface ResultService {
  readonly collectResult: (instance: TaskInstanceState) => CaseVerdict;
  readonly getVerdict: (instanceId: string) => CaseVerdict | undefined;
  readonly getSnapshot: () => ReturnType<ResultStateContainer['getSnapshot']>;
  readonly clear: () => void;
}
```

**createResultService factory (lines 12-33):**
```typescript
export function createResultService(state: ResultStateContainer): ResultService {
  return {
    collectResult(instance: TaskInstanceState): CaseVerdict { /* ... */ },
    getVerdict: state.getVerdict,
    getSnapshot: state.getSnapshot,
    clear: state.clear,
  };
}
```

## 2. `/mnt/d/code/frontend/dongfanghong/rewrite/src/features/result/core/types.ts`

**All exported types (lines 1-14):**
```typescript
export type CaseVerdictKind = 'passed' | 'failed' | 'stopped';

export interface CaseVerdict {
  readonly instanceId: string;
  readonly taskDefinitionId: string;
  readonly verdict: CaseVerdictKind;
  readonly judgedAt: string;
  readonly startedAt: string;
  readonly finishedAt: string;
}

export interface ResultStateSnapshot {
  readonly verdicts: ReadonlyMap<string, CaseVerdict>;
}
```

## 3. `/mnt/d/code/frontend/dongfanghong/rewrite/src/features/result/core/judge.ts`

**judgeCaseVerdict function (lines 15-20):**
```typescript
export function judgeCaseVerdict(instance: TaskInstanceState): CaseVerdictKind {
  if (instance.lifecycle === 'stopped') return 'stopped';
  if (instance.lifecycle === 'failed') return 'failed';
  const hasFailure = instance.stepResults.some(isStepFailed);
  return hasFailure ? 'failed' : 'passed';
}
```

**Return type:** `CaseVerdictKind` (which is `'passed' | 'failed' | 'stopped'`)

## 4. `/mnt/d/code/frontend/dongfanghong/rewrite/src/platform/index.ts`

**How facades are organized (lines 42-72):**
```typescript
export function getRewritePlatformBridgeInfo(): RewritePlatformBridgeInfo | […]

> TOOL

tool_use Glob
id: call_93a0006b48b1411f91af9cf2
```json
{
  "pattern": ".claude/skills/cs-feat-design/reference.md"
}
```

> TOOL

tool_result
id: call_93a0006b48b1411f91af9cf2
```
.claude/skills/cs-feat-design/reference.md
```

> TOOL

tool_use Read
id: call_5d712e30aa4d4a6194c5fcf4
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.claude/skills/cs-feat-design/reference.md"
}
```

> TOOL

tool_result
id: call_5d712e30aa4d4a6194c5fcf4
```
1	# feature-design 参考模板
2	
3	本文件提供 `cs-feat-design` 使用的 `{slug}-design.md` / `{slug}-checklist.yaml` 参考格式。
4	
5	## 1. {slug}-design.md frontmatter
6	
7	```markdown
8	---
9	doc_type: feature-design
10	feature: 2026-04-12-user-auth
11	requirement: user-auth-email
12	roadmap: permission-system           # 可选：本 feature 从某 roadmap 条目起头时填
13	roadmap_item: permission-rbac-core   # 可选：对应 roadmap items.yaml 里的 slug
14	status: draft
15	summary: 支持用户通过邮箱验证码登录后台
16	tags: [auth, email, login]
17	---
18	```
19	
20	必填：`doc_type` / `feature` / `status` / `summary` / `tags`。
21	
22	- `requirement`：填对应 req 的 slug；纯重构 / 技术债允许留空
23	- `roadmap` / `roadmap_item`：从 roadmap 条目起头时才填，两个一起填或一起空
24	
25	## 2. 顶层节锚点
26	
27	- `## 0. 术语约定`
28	- `## 1. 决策与约束`
29	- `## 2. 名词与编排` ← design 的灵魂，是 implement 的主输入
30	  - `### 2.1 名词层`
31	  - `### 2.2 编排层`
32	  - `### 2.3 挂载点清单`
33	  - `### 2.4 推进策略`
34	  - `### 2.5 结构健康度与微重构` ← 固定节，结论二选一 + 可选"超出范围的观察"
35	- `## 3. 验收契约`
36	- `## 4. 与项目级架构文档的关系`
37	
38	## 3. {slug}-checklist.yaml 格式
39	
40	```yaml
41	feature: {feature 目录名}
42	created: YYYY-MM-DD
43	
44	steps:
45	  - action: "{paradigm 维度的切片}：{动作描述}"
46	    exit_signal: "{退出信号，可独立验证}"
47	    status: pending
48	
49	checks:
50	  - item: "{检查项描述}"
51 […]

> AGENT

所有材料齐了。开始写设计文档。

> TOOL

tool_use Write
id: call_cbb833389b2247d3b6d9a72b
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md",
  "content": "---\ndoc_type: feature-design\nfeature: rewrite-northbound\nstatus: draft\nsummary: 甲方 HTTPS 闭环 feature — inbound translator 将 setTestTask 翻译为 TaskDefinition，outbound translator 将 result 翻译为 testCaseResultReport/msgReport，platform HTTP facade 封装传输层不含业务语义\ntags: [northbound, customer-integration, https, translation, platform]\n---\n\n## 0. 术语约定\n\n| 术语 | 定义 | 防冲突 |\n|------|------|--------|\n| northbound | 本 feature，甲方集成测试系统与我方之间的 HTTPS 闭环 | 与 command-ingress（SCOE TCP 入站）是不同 feature |\n| inbound translator | 甲方请求 JSON → 内部类型的翻译器 | 不叫 ProtocolAdapter（那是 command-ingress 的概念） |\n| outbound translator | 内部 result → 甲方响应 JSON 的翻译器 | 不叫 projector（那是架构文档的通用术语） |\n| HttpFacade | platform 层的 HTTP 传输封装 | 与 TransportFacade（串口/TCP/UDP）同级 |\n| customer types | 甲方接口的请求/响应类型定义 | 只存在于 northbound/core/types.ts，其他层用通用 HttpRequest/HttpResponse |\n\n术语 grep 结果：`northbound` 在代码中无实现（仅文档引用）；`inbound` / `outbound` 未在其他 feature 中使用。无冲突。\n\n## 1. 决策与约束\n\n### 需求摘要\n\n**做什么**：建 northbound feature，让甲方集成测试系统能通过 HTTPS 接口下发测试任务并接收结果上报。\n\n**为谁**：甲方集成测试系统（唯一外部调用方）。\n\n**成功标准**：甲方通过 setTestTask 下发 executionPlan → 我方创建并执行 task → 每个步骤完成时 msgReport 上报 → task 终态时 testCaseResultReport 上报 → heartbeat 和 getSubSysState 正确响应。\n\n**明确不做**：\n- testDataFileDelivery（甲方文件翻译完成通知）\n- 详细 report（checkPoints 对比、statisticsItems）\n- FTP 文件上传（getTestCaseAll 的 FTP 部分）\n- 用例库管理\n- 告警上报\n- 升级 / 运维操作\n- 多租户 / 多实例 HTTPS server\n- 甲方 schema 冻结（先用内部映射，甲方确认后只改映射层）\n\n### 复杂度档位\n\n走 Lane B 默认档位，无偏离。\n\n### 关键决策\n\n**D1：northbound 独立 feature，不合并 command-ingress**\n- 甲方 HTTPS 是 JSON server 模式，不走 TransportEventConsumer 链\n- 两者入站机制、协议格式、客户端模型完全不同\n- 合并会让 command-ingress 承担不相关的职责\n- 来源：brainstorm + S001 决策\n\n**D2：HTTPS server/client 封装在 platform facade，主进程不含业务语义**\n- main process 只认 `{ method, url, headers, body }` → IPC 透传给 […]

> TOOL

tool_result
id: call_cbb833389b2247d3b6d9a72b
```
File created successfully at: /mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md
```

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

> TOOL

tool_use Agent
id: call_76af18261a2f457d930fe2ca
```json
{
  "description": "Boundary compliance review",
  "prompt": "Review the northbound design document for boundary compliance against project hard rules.\n\nRead these files:\n1. `codestable/features/rewrite-northbound/northbound-design.md` — the design to review\n2. `codestable/quality/rewrite-quality-rules.md` — quality rules (especially R5/R6/R10 and northbound-related rules)\n3. `CLAUDE.md` (project root) — hard constraints about main process, platform boundary, feature boundaries\n\nCheck each of these constraints and report pass/fail with evidence:\n\n1. **Main process boundary**: Does the design put ANY business logic in main process? Main should only handle raw HTTP transport. No customer types, no protocol parsing, no task translation in main.\n\n2. **Platform facade pattern**: Does HttpFacade follow the same pattern as TransportFacade/FileFacade? Is it properly layered (main → preload → platform facade)?\n\n3. **Feature boundary**: Does northbound respect other features' public APIs? Does it access task/result only through their public service interfaces?\n\n4. **Renderer isolation**: Does the design ensure renderer doesn't directly access Node/Electron/IPC? Does it go through platform facade?\n\n5. **Selector immutability**: Does the design respect selector read-only constraints?\n\n6. **Northbound ≠ command-ingress**: Are they properly separated? Does northbound avoid importing command-ingress internals?\n\n7. **CLAUDE.md northbound rules**: \n   - Not equating northbound task with old send task\n   - Not equating northbound deviceId with serial/network target\n   - Not equating history/CSV with TestReport\n   - […]

> TOOL

tool_use Agent
id: call_019bb4fc93874a4b80da5be6
```json
{
  "description": "Decision consistency review",
  "prompt": "Review the northbound design document for consistency with previously locked decisions.\n\nRead these files:\n1. `codestable/features/rewrite-northbound/northbound-design.md` — the design to review\n2. `codestable/features/rewrite-northbound/northbound-brainstorm.md` — brainstorm conclusions\n3. `.sessions/2026-05-18-northbound-integration/topic-index.md` — S001 topic index with locked decisions\n\nFrom S001, these 7 decisions are LOCKED and must be consistent:\n1. testCase = task（TaskDefinition）\n2. executionPlan.layers 中每个 testCaseId → 创建一个 task 实例\n3. verdict: wait-condition matched → success, timeout/不匹配 → fail, task 被 stop → tbd\n4. HTTPS server 放 main process（传输层），业务逻辑在 renderer，通过 IPC bridge 通信\n5. northbound 做独立 feature，不合并到 command-ingress\n6. 翻译层在 northbound feature 内（inbound-translator + outbound-translator）\n7. result 不需要改，northbound 自己接线：onSettled → collectResult() → 翻译 → POST\n\nAlso check these S001 confirmed items:\n- immediate 始终 true（收到直接 createTask + startTask）\n- isEnd 始终 true（一次下发全部 testCaseInfo）\n- MVP 6 interfaces: setTestTask, controlTestTask, testCaseResultReport, msgReport, heartbeat, getSubSysState\n\nFor each locked decision, report:\n- ✅ CONSISTENT — design matches, with evidence (quote the relevant design section)\n- ⚠️ PARTIAL — design mentions it but details differ\n- ❌ CONFLICT — design contradicts the locked decision\n\nAlso check: are there any decisions in the design that weren't in the brainstorm or S001? Flag them as new decisions that need user confirmation.",
  "subagent_type": "general-purpose",
  "model": "sonnet"
}
```

> TOOL

tool_use Agent
id: call_0ed821b8cc284e5589a9d720
```json
{
  "description": "Coverage completeness review",
  "prompt": "Review the northbound design for completeness — check if it covers all required aspects and doesn't have gaps.\n\nRead these files:\n1. `codestable/features/rewrite-northbound/northbound-design.md` — the design to review\n2. `codestable/features/rewrite-northbound/northbound-brainstorm.md` — brainstorm with requirements\n3. `.sessions/2026-05-18-northbound-integration/topic-index.md` — S001 topic index with gaps and requirements\n\nCheck coverage in these dimensions:\n\n**A. MVP Interface Coverage**: For each of the 6 MVP interfaces, does the design cover:\n- setTestTask: request type + inbound translation + task creation + response\n- controlTestTask: request type + control mapping (abort→stop, pause→pause, continue→resume, stop→stop) + response\n- testCaseResultReport: outbound translation + verdict mapping (passed→success, failed→fail, stopped→tbd) + POST\n- msgReport: step event hook + outbound translation + POST\n- heartbeat: handler + response\n- getSubSysState: handler + response (what data sources?)\n\n**B. Missing Pieces Check**: \n- Is there a plan for how to handle HTTPS library selection?\n- Is TLS configuration addressed?\n- Is the taskId ↔ instanceId bidirectional mapping covered?\n- Is session lifecycle (cleanup on task completion) covered?\n- Is the step name mapping solved? (design says: look up definitionRef.steps[stepIndex] — is this correct?)\n- Is the executionPlan processing (parallel/sequential layers) detailed enough?\n\n**C. Error Path Coverage**:\n- What happens if HttpFacade.sendRequest fails for msgReport?\n- What happens if task creation fails mid-executionPlan?\n- What happens […]

> TOOL

tool_result
id: call_019bb4fc93874a4b80da5be6
```
这三份文档都已加载。现在我将系统性地根据 S001 锁定的决策和已确认项来审查设计文档。

---

## 北向设计 vs. S001 锁定决策 — 一致性审查

### 决策 1: testCase = task (TaskDefinition)

**结论: 一致**

设计第 29 行的成功标准: "甲方通过 setTestTask 下发 executionPlan → 我方创建并执行 task"

设计第 96-164 行: `SetTestTaskRequest` 类型将 `testCaseInfoList` 映射到 `TestCaseInfo`，第 176 行的 inbound translator 签名确认: `translateTestCaseToTaskDefinition(testCase: TestCaseInfo, ...)` -- 每个 `TestCaseInfo` 转换为一个 `TaskDefinition`。

---

### 决策 2: `executionPlan.layers` 中每个 `testCaseId` → 创建一个 `task` 实例

**结论: 一致**

设计第 107-113 行: `SetTestTaskRequest.executionPlan.layers[].testCaseInfoList` 包含 `TestCaseInfo[]`。设计第 72 行 (D5): "收到 setTestTask 后立即按层序号顺序处理所有 testCase"。设计第 73-74 行: "parallel=true 层：同时 `createTask` + `startTask`；parallel=false 层：顺序执行，等前一个 `onSettled` 再启动下一个"。场景 S1 和 S2（第 480-482 行）证实了 1:1 映射：1 个 `testCase` → 1 个 `task` 实例，2 个 `testCase` → 2 个 `task` 实例。

---

### 决策 3: 判定: `wait-condition` 匹配 → 成功, 超时/不匹配 → 失败, `task` 停止 → 待定

**结论: 一致**

设计第 197-198 行 (`outbound translator`): "判定映射: `passed`→成功, `failed`→失败, `stopped`→待定"。场景 S11（第 510 行）: "`task` 已完成且所有步骤通过 → 结果='success'"。场景 S12（第 511 行）: "`task` 已完成且有步骤失败 → 结果='失败'"。场景 S13（第 512 行）: "`task` 停止 → 结果='待定'"。这完全匹配 `wait-condition` 匹配=成功, 超时/不匹配=失败, 停止=待定。

---

### 决策 4: HTTPS 服务器位于 `main process`（传输层），业务逻辑在 `renderer` 中，通过 `IPC bridge` 通信

**结论: 一致**

设计第 53-57 行 (D2): "HTTPS 服务器/客户端封装在平台 `facade` 中，`main process` 不包含业务语义" + "`main process` 只识别 `{ method, url, headers, body }` → […]

> TOOL

tool_result
id: call_76af18261a2f457d930fe2ca
```
我已经获得了所有三份主要文档和重叠/间隙图。现在，让我根据七项约束逐一提供合规性审查。

---

## Northbound 设计边界合规审查

**直接约定：**`codestable/features/rewrite-northbound/northbound-design.md` (被审查的设计)

**边界约束：**
- `codestable/quality/rewrite-quality-rules.md` (R5, R6, R10, R11, R14, R15)
- `CLAUDE.md` (项目根目录 -- 主进程边界、平台外观模式、功能边界、渲染器隔离、选择器不可变性、Northbound 特定禁令)

---

### 1. 主进程边界

**结论：** PASS

**证据：**

设计明确说明 (D2, 第 53-58 行)：“HTTPS server/client 封装在 platform facade，主进程不含业务语义”，并规定“主进程只认 `{ method, url, headers, body }` -> IPC 透传给 renderer”。第 57 行进一步强化：“platform facade 封装为通用 HttpRequest/HttpResponse”。

设计第 3 节中的反向核对清单 (第 525 行) 明确指出：“main process 中不应 import 或引用任何 northbound/core/types.ts 的甲方类型”和“platform/http.ts 中不应出现 setTestTask / testCaseResultReport 等甲方业务名称”。

`HttpFacade` 接口 (第 270-303 行) 只暴露了通用的 `HttpRequest`/`HttpResponse`，不包含任何客户领域类型。主进程接收原始 HTTP 请求，转发给 `renderer`，`renderer` 中的 `NorthboundService` 处理所有协议解析、翻译和业务逻辑。

编排顺序图 (第 328-366 行) 确认主进程作为 C -> M -> P -> N 链中的传输管道，所有业务决策都发生在 `NorthboundService` 中。

符合 R5 规则：“把业务运算、协议语义、任务状态推进、报告语义或 northbound 领域规则搬进 main 进程”是禁止的。设计严格遵循。

---

### 2. 平台外观模式

**结论：** PASS

**证据：**

设计引入 `HttpFacade` (第 262-303 行)，并明确将其定位为“与 TransportFacade（串口/TCP/UDP）同级” (第 16 行)。该模式遵循现有外观模式：

- `HttpFacade` 定义在 `platform/http.ts` (第 418 行，挂载点)
- 通过 `platform/index.ts` 中的 `getHttpFacade()` 注册 (第 386 行)
- 主进程通过 IPC 处理程序 (第 387 行：`src-electron/main/http-handlers.ts`)
- Preload 暴露 `HttpBridge` (第 388 行)

分层架构是 `main -> preload -> platform facade`，与 `TransportFacade` 和 `FileFacade` 的模式一致。该外观只处理通用的 `HttpRequest`/`HttpResponse` 类型——不涉及客户领域类型。

符合 R5 规则：“renderer 只通过 `rewrite/src/platform` facade 访问桌面能力”。

---

### 3. 功能边界

**结论：** PASS

**证据：**

该设计只通过公共服务接口访问其他功能：

- **任务服务**：通过 `TaskService` 公共 API (`createTask`, `startTask`, `stopTask`, `onSettled`) 使用 -- 第 217 行的 `NorthboundServiceOptions` 将其作为依赖项注入。 […]

> TOOL

tool_result
id: call_0ed821b8cc284e5589a9d720
```
我已经掌握了所有需要的证据。以下是完整的审查结果。

---

## 北向设计完整性审查

### A. MVP 接口覆盖范围

**setTestTask**

- 请求类型: ✅ 已覆盖 — `SetTestTaskRequest` 和 `TestCaseInfo` 定义于第 106-121 行，包含 `executionPlan.layers`、`testCaseInfoList`、`steps`。
- 入站转换: ✅ 已覆盖 — `translateTestCaseToTaskDefinition` 函数在第 176-183 行，将 `TestCaseInfo.steps` 映射到 `TaskStepDefinition[]`，`send`/`wait-condition` 映射已列出，`schedule = { kind: 'immediate' }` 已列出。
- 任务创建: ✅ 已覆盖 — 主流程序列图（第 343-345 行）显示 `createTask(def)` -> `mapTestCase(testCaseId, instanceId)` -> `startTask(instanceId)`。
- 响应: ✅ 已覆盖 — `HttpResponse { code: 200 }`，以及错误路径 S3/S4。

**controlTestTask**

- 请求类型: ✅ 已覆盖 — `ControlTestTaskRequest` 包含 `testCaseIdList` 和 `controlType` 在第 131-132 行。
- 控制映射（`abort`->`stop`, `pause`->`pause`, `continue`->`resume`, `stop`->`stop`）: ⚠️ 部分覆盖 — 设计在决策 D5 和验收场景 S5 中声明了映射，但**没有**明确说明 `controlType='abort'` 映射到 `taskService.stopTask()`，`controlType='continue'` 映射到 `taskService.resumeTask()` 等。`NorthboundService.handleRequest` 主体没有伪代码显示此 `switch`。这是一个集成点，转换的实际代码需要正确路由每个 `controlType` 到正确的 `TaskService` 方法。
- 响应: ✅ 已覆盖 — S5 返回 `{ code: 200 }`，S6 返回 `{ code: 404 }`。

**testCaseResultReport**

- 出站转换: ✅ 已覆盖 — `translateTaskResult` 在第 194-198 行，接受 `(TaskInstanceState, CaseVerdict, testCaseId)` 并返回 `TestCaseResultReport`。
- 判决映射（`passed`->`success`, `failed`->`fail`, `stopped`->`tbd`）: ✅ 已覆盖 — 在第 199 行明确说明。
- POST: ✅ 已覆盖 — 序列图第 360-363 行显示 `sendRequest(POST customerEndpoint/testCaseResultReport)`。

**msgReport**

- 步骤事件钩子: ✅ 已覆盖 — D4 决策在 `CreateTaskServiceOptions` 中添加 `onStepResult` 回调。
- 出站转换: ✅ 已覆盖 — `translateStepResult` 在第 201-206 行。
- POST: ✅ 已覆盖 — 序列图第 352-354 行。

**心跳**

- 处理程序: ✅ 已覆盖 — S7 场景，返回 `{ code: 200 }`。 […]

> AGENT

三个自检完成。汇总关键发现：

**边界合规**：10/10 全通过。一个观察：CLAUDE.md 第 92 行和第 88 行有张力（command-ingress vs 独立 northbound），design 用 D1 正确解决了。

**决策一致性**：7 条锁定决策 + 3 条确认项全部一致。发现 7 个新决策需确认（onStepResult 回调机制、映射位置、不重试策略等）。

**覆盖完整性**：3 个关键 gap 需要修：

1. **onStepResult 回调拿不到 TaskInstanceState** — outbound translator 需要 instance 才能查 stepName，但回调只有 instanceId。需要明确通过 `taskService.getInstance()` 获取
2. **executionPlan 编排缺伪代码** — 并行层怎么等、顺序层失败怎么处理、中途失败的清理
3. **回调异常隔离** — onStepResult 如果 throw 会崩 task 执行循环

现在修 design 文档补上这些 gap。

> TOOL

tool_use Read
id: call_7309f218c6864bddb48dd757
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md"
}
```

> TOOL

tool_result
id: call_7309f218c6864bddb48dd757
```
1	---
2	doc_type: feature-design
3	feature: rewrite-northbound
4	status: draft
5	summary: 甲方 HTTPS 闭环 feature — inbound translator 将 setTestTask 翻译为 TaskDefinition，outbound translator 将 result 翻译为 testCaseResultReport/msgReport，platform HTTP facade 封装传输层不含业务语义
6	tags: [northbound, customer-integration, https, translation, platform]
7	---
8	
9	## 0. 术语约定
10	
11	| 术语 | 定义 | 防冲突 |
12	|------|------|--------|
13	| northbound | 本 feature，甲方集成测试系统与我方之间的 HTTPS 闭环 | 与 command-ingress（SCOE TCP 入站）是不同 feature |
14	| inbound translator | 甲方请求 JSON → 内部类型的翻译器 | 不叫 ProtocolAdapter（那是 command-ingress 的概念） |
15	| outbound translator | 内部 result → 甲方响应 JSON 的翻译器 | 不叫 projector（那是架构文档的通用术语） |
16	| HttpFacade | platform 层的 HTTP 传输封装 | 与 TransportFacade（串口/TCP/UDP）同级 |
17	| customer types | 甲方接口的请求/响应类型定义 | 只存在于 northbound/core/types.ts，其他层用通用 HttpRequest/HttpResponse |
18	
19	术语 grep 结果：`northbound` 在代码中无实现（仅文档引用）；`inbound` / `outbound` 未在其他 feature 中使用。无冲突。
20	
21	## 1. 决策与约束
22	
23	### 需求摘要
24	
25	**做什么**：建 northbound feature，让甲方集成测试系统能通过 HTTPS 接口下发测试任务并接收结果上报。
26	
27	**为谁**：甲方集成测试系统（唯一外部调用方）。
28	
29	**成功标准**：甲方通过 setTestTask 下发 executionPlan → 我方创建并执行 task → 每个步骤完成时 msgReport 上报 → task 终态时 testCaseResultReport 上报 → heartbeat 和 getSubSysState 正确响应。
30	
31	**明确不做**：
32	- testDataFileDelivery（甲方文件翻译完成通知）
33	- 详细 report（checkPoints 对比、statisticsItems）
34	- FTP 文件上传（getTestCaseAll 的 FTP 部分） […]

> AGENT

逐个修 gap。

> TOOL

tool_use Edit
id: call_fd79a319bc61440fae8d7cce
```json
{
  "replace_all": false,
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md",
  "old_string": "**D4：step 完成事件通过 task service 回调**\n- 在 `CreateTaskServiceOptions` 加 `onStepResult` 可选回调\n- task 迭代循环在 addStepResult 后调用\n- northbound 注册回调，收到后翻译为 msgReport 并 POST\n- 备选被拒：轮询 stepResults（延迟高、浪费） / 拦截 state.addStepResult（污染状态容器）",
  "new_string": "**D4：step 完成事件通过 task service 回调**\n- 在 `CreateTaskServiceOptions` 加 `onStepResult` 可选回调\n- task 迭代循环在 addStepResult 后、try/catch 内调用——回调异常只记日志不传播，不影响 task 执行\n- northbound 注册回调后通过 `taskService.getInstance(instanceId)` 获取完整 TaskInstanceState（TaskService 继承 TaskReader，getInstance 已是公开 API），再调用 outbound translator\n- 备选被拒：轮询 stepResults（延迟高、浪费） / 拦截 state.addStepResult（污染状态容器）"
}
```

> TOOL

tool_result
id: call_fd79a319bc61440fae8d7cce
```
The file /mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md has been updated successfully.
```

> TOOL

tool_use Edit
id: call_830677a93bcd4dd9aae9cc5c
```json
{
  "replace_all": false,
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md",
  "old_string": "**D5：executionPlan 按 immediate=true / isEnd=true 处理**\n- 收到 setTestTask 后立即按层序号顺序处理所有 testCase\n- parallel=true 层：同时 createTask + startTask\n- parallel=false 层：顺序执行，等前一个 onSettled 再启动下一个\n- 来源：S001 甲方确认",
  "new_string": "**D5：executionPlan 按 immediate=true / isEnd=true 处理**\n- 收到 setTestTask 后立即按层序号顺序处理所有 testCase\n- parallel=true 层：同时 createTask + startTask\n- parallel=false 层：顺序执行，等前一个 onSettled 再启动下一个\n- 来源：S001 甲方确认\n\n**executionPlan 处理算法**：\n```\nfor layer in executionPlan.layers (按 layerNo 排序):\n  if layer.parallel:\n    tasks = layer.testCaseInfoList.map(tc => {\n      def = translateTestCaseToTaskDefinition(tc)\n      inst = taskService.createTask(def)\n      state.mapTestCase(tc.testCaseId, inst.instanceId)\n      taskService.startTask(inst.instanceId)\n      return { testCaseId: tc.testCaseId, instanceId: inst.instanceId }\n    })\n    // 并行等全部终态\n    await Promise.all(tasks.map(t => taskService.onSettled(t.instanceId)))\n  else:\n    for tc in layer.testCaseInfoList:\n      def = translateTestCaseToTaskDefinition(tc)\n      inst = taskService.createTask(def)\n      state.mapTestCase(tc.testCaseId, inst.instanceId)\n      taskService.startTask(inst.instanceId)\n      await taskService.onSettled(inst.instanceId) // 顺序等\n```\n\n**中途失败处理**：单个 task 创建/启动失败时，已创建的 task 继续运行不回滚（MVP 阶段），错误记录在响应中返回给甲方。不清理已创建 task——它们仍会正常执行并上报结果。"
}
```

> TOOL

tool_result
id: call_830677a93bcd4dd9aae9cc5c
```
The file /mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md has been updated successfully.
```

> TOOL

tool_use Edit
id: call_fb2ae65320a548a1a0f35849
```json
{
  "replace_all": false,
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md",
  "old_string": "interface NorthboundServiceOptions {\n  readonly taskService: TaskService;\n  readonly resultService: ResultService;\n  readonly httpFacade: HttpFacade;\n  readonly settingsReader: SettingsReader;\n  readonly connectionSnapshot: () => ConnectionStateSnapshot;\n}",
  "new_string": "interface NorthboundServiceOptions {\n  readonly taskService: TaskService;\n  readonly resultService: ResultService;\n  readonly httpFacade: HttpFacade;\n  readonly connectionSnapshot: () => ConnectionStateSnapshot; // 来自 connection feature selector\n}"
}
```

> TOOL

tool_result
id: call_fb2ae65320a548a1a0f35849
```
The file /mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md has been updated successfully.
```

> TOOL

tool_use Edit
id: call_eb81609e0490498586bd76c8
```json
{
  "replace_all": false,
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md",
  "old_string": "**错误语义**：\n- 入站请求解析失败 → 返回 CustomerResponse `{ code: 400, msg: \"...\" }`\n- task 创建/启动失败 → 返回 `{ code: 500, msg: \"...\" }`\n- 出站 POST 失败 → 记录日志，不重试（MVP 阶段）\n- 不暴露内部错误详情给甲方",
  "new_string": "**错误语义**：\n- 入站请求解析失败 → 返回 CustomerResponse `{ code: 400, msg: \"...\" }`\n- task 创建/启动失败 → 返回 `{ code: 500, msg: \"...\" }`，已创建的 task 不回滚，继续执行并上报结果\n- 出站 POST 失败 → 记录日志，不重试（MVP 阶段）\n- 不暴露内部错误详情给甲方\n- **回调异常隔离**：task 迭代循环中 onStepResult 回调用 try/catch 包裹，异常只记日志不传播，task 执行不受影响"
}
```

> TOOL

tool_result
id: call_eb81609e0490498586bd76c8
```
The file /mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md has been updated successfully.
```

> AGENT

现在补充 controlTestTask 的映射表和 getSubSysState 的数据来源。

> TOOL

tool_use Edit
id: call_045cb2c7be11408c8a5c8ee0
```json
{
  "replace_all": false,
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md",
  "old_string": "interface ControlTestTaskRequest {\n  readonly testCaseIdList: readonly string[];\n  readonly controlType: 'abort' | 'pause' | 'continue' | 'stop';\n}",
  "new_string": "interface ControlTestTaskRequest {\n  readonly testCaseIdList: readonly string[];\n  readonly controlType: 'abort' | 'pause' | 'continue' | 'stop';\n}\n// controlType 映射：\n// abort   → taskService.stopTask(instanceId)\n// pause   → taskService.pauseTask(instanceId)\n// continue → taskService.resumeTask(instanceId)\n// stop    → taskService.stopTask(instanceId)"
}
```

> TOOL

tool_result
id: call_045cb2c7be11408c8a5c8ee0
```
The file /mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md has been updated successfully.
```

> TOOL

tool_use Edit
id: call_8f44143c2360495bb7b8d01e
```json
{
  "replace_all": false,
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md",
  "old_string": "interface HeartbeatRequest { /* MVP: 最简结构 */ }\ninterface GetSubSysStateRequest { /* MVP: 最简结构 */ }",
  "new_string": "interface HeartbeatRequest { /* MVP: 最简结构，只返回 { code: 200 } */ }\ninterface GetSubSysStateRequest { /* MVP: 最简结构 */ }\n// getSubSysState 数据来源：\n// connectionStatus → connectionSnapshot()（来自 connection feature 的 public selector）\n// runningTestCases → state.getSnapshot().activeTestCases"
}
```

> TOOL

tool_result
id: call_8f44143c2360495bb7b8d01e
```
The file /mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md has been updated successfully.
```

> AGENT

现在补充 task 创建中途失败和甲方重连场景的验收场景。

> TOOL

tool_use Edit
id: call_3e0740a8751d49989265a36c
```json
{
  "replace_all": false,
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md",
  "old_string": "| S14 | HttpFacade.sendRequest 出站 POST 失败 | 日志记录错误，不重试，不崩溃 |\n| S15 | HttpFacade server 启动失败（端口占用） | start() 返回失败，isActive()=false |",
  "new_string": "| S14 | HttpFacade.sendRequest 出站 POST 失败 | 日志记录错误，不重试，不崩溃 |\n| S15 | HttpFacade server 启动失败（端口占用） | start() 返回失败，isActive()=false |\n| S16 | executionPlan 处理中途某个 task 创建失败 | 已创建的 task 继续运行，响应返回错误码，已创建的 task 仍上报结果 |\n| S17 | onStepResult 回调内部抛异常 | 异常被 try/catch 吞掉并记录日志，task 执行继续，不影响后续 step |\n| S18 | 甲方重发 setTestTask（新 testCaseId，旧 task 仍在运行） | 新 task 正常创建，旧 task 不受影响（映射独立，新旧共存） |"
}
```

> TOOL

tool_result
id: call_3e0740a8751d49989265a36c
```
The file /mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md has been updated successfully.
```

> AGENT

最后明确 HTTPS 库 MVP 选型。

> TOOL

tool_use Edit
id: call_d835dcf042d14ae2917fe464
```json
{
  "replace_all": false,
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md",
  "old_string": "- HttpFacade 可替换底层库（Fastify/Express/原生 Node），上层无感知",
  "new_string": "- HttpFacade 可替换底层库（Fastify/Express/原生 Node），上层无感知。MVP 用 Node 原生 `http`/`https` 模块——零额外依赖，后续按需换框架"
}
```

> TOOL

tool_result
id: call_d835dcf042d14ae2917fe464
```
The file /mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md has been updated successfully.
```

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

> TOOL

tool_use Write
id: call_93d9a04cdc4c46dbb00c3fb2
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-checklist.yaml",
  "content": "feature: rewrite-northbound\ncreated: 2026-05-25\n\nsteps:\n  - action: \"Platform HTTP facade：main process HTTP handler + preload bridge + platform/http.ts\"\n    exit_signal: \"HttpFacade 单测通过（mock IPC），startServer/onRequest/sendRequest 跑通\"\n    status: pending\n\n  - action: \"Task service step 回调：CreateTaskServiceOptions 加 onStepResult，iteration loops try/catch 内调用\"\n    exit_signal: \"现有测试全通过 + 新增 step callback 触发验证 + 回调异常不中断 task 执行\"\n    status: pending\n\n  - action: \"Northbound 名词层 + 编排骨架：types + translator 纯函数 + state 容器 + service 空壳\"\n    exit_signal: \"translator 单测覆盖正常+边界，service 可创建和销毁\"\n    status: pending\n\n  - action: \"入站接线：handleRequest → inbound translator → executionPlan 编排 → task service → 状态映射\"\n    exit_signal: \"setTestTask JSON → TaskDefinition 创建 → task 启动 → 并行/顺序层处理正确，单测覆盖\"\n    status: pending\n\n  - action: \"出站接线：onSettled → result 收集 → outbound translator → HttpFacade.sendRequest\"\n    exit_signal: \"task 终态 → testCaseResultReport POST 被调用，verdict 映射正确\"\n    status: pending\n\n  - action: \"step 事件接线：onStepResult 回调 → getInstance → outbound translator → msgReport POST\"\n    exit_signal: \"step 完成 → msgReport POST 被调用，stepName 从 definition 正确取出\"\n    status: pending\n\n  - action: \"controlTestTask + heartbeat + getSubSysState handler 实现\"\n    exit_signal: \"controlType 正确映射到 task service 方法，heartbeat 返回 200，getSubSysState 读 connection/activeTestCases\"\n    status: pending\n\n  - action: \"测试覆盖 + 集成验证：补齐边界和错误路径\"\n    exit_signal: \"pnpm build + pnpm lint + 全部测试通过\"\n    status: pending\n\nchecks:\n  - item: \"甲方接口类型只在 northbound/core/types.ts 定义一次，其他文件不重复\"\n    source: 名词契约\n    status: pending\n\n  - item: \"HttpFacade 接口只含通用 HttpRequest/HttpResponse，无甲方业务名称\"\n […]

> TOOL

tool_result
id: call_93d9a04cdc4c46dbb00c3fb2
```
File created successfully at: /mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-checklist.yaml
```

> TOOL

tool_use Edit
id: call_1a29e86901b94d86a44b14c6
```json
{
  "replace_all": false,
  "file_path": "/mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md",
  "old_string": "status: draft",
  "new_string": "status: approved"
}
```

> TOOL

tool_result
id: call_1a29e86901b94d86a44b14c6
```
The file /mnt/d/code/frontend/dongfanghong/codestable/features/rewrite-northbound/northbound-design.md has been updated successfully.
```

> TOOL

tool_use Bash
id: call_d4acb1fdc50548e3a37ccb6a
```json
{
  "command": "python codestable/tools/validate-yaml.py --file codestable/features/rewrite-northbound/northbound-checklist.yaml --yaml-only 2>&1",
  "description": "Validate checklist YAML"
}
```

> TOOL

tool_result ERROR
id: call_d4acb1fdc50548e3a37ccb6a
```
Exit code 127
(eval):1: command not found: python
```

> TOOL

tool_use Bash
id: call_b82eb8fbd0a84915a9f66e36
```json
{
  "command": "python3 codestable/tools/validate-yaml.py --file codestable/features/rewrite-northbound/northbound-checklist.yaml --yaml-only 2>&1",
  "description": "Validate checklist YAML with python3"
}
```

> TOOL

tool_result
id: call_b82eb8fbd0a84915a9f66e36
```
Validated 1 file(s): 1 passed, 0 failed.

  ✓ codestable/features/rewrite-northbound/northbound-checklist.yaml

All files valid.
```

> AGENT

Design 已批准，checklist 已通过验证。

产出清单：
- `codestable/features/rewrite-northbound/northbound-design.md` — 已批准
- `codestable/features/rewrite-northbound/northbound-checklist.yaml` — 8 步 + 14 检查项，已验证
- `codestable/features/rewrite-northbound/northbound-brainstorm.md` — 讨论过程记录

下一步 `cs-feat-impl` 可以开始。按推进策略先从 Platform HTTP facade 和 task step 回调并行启动。

> DEVELOPER

我打算先压缩

> TOOL

tool_use Bash
id: call_66105e4ba8464ec1b9cfa69a
```json
{
  "command": "git status --short",
  "description": "Show working tree status"
}
```

> TOOL

tool_use Bash
id: call_9122f091d756431a868c8b84
```json
{
  "command": "git log --oneline -5",
  "description": "Show recent commits"
}
```

> TOOL

tool_result
id: call_9122f091d756431a868c8b84
```
8048c1d feat: 集成测试体系 + 线1 bug修复 — 36条集测项(343 tests) + onSettled竞态/resolveSettle兜底/storageService mock
3bb080a docs: 更新过程日志 — 05-18 甲方对接闭环讨论结论
fdbfa6b feat: 持久化层 — RealLocalMaterialAdapter + FeaturePersistence + 启动加载
978e48a fix: SendPage 帧列表过滤 direction 值从 o_send 改为 send
c94e099 docs: 更新过程日志 — 05-15 UI审计+对标修复+调查结果
```

> TOOL

tool_result
id: call_66105e4ba8464ec1b9cfa69a
```
 M .omc/state/hud-stdin-cache.json
 M .sessions/_registry.yaml
 M public/data/templates/sendInstances.json
 M rewrite/src/__tests__/integration/display-projection.spec.ts
 M rewrite/src/features/connection/core/types.ts
 M rewrite/src/features/connection/core/validation.ts
 M rewrite/src/features/display/__tests__/display-core-service-state-selector.spec.ts
 M rewrite/src/features/display/composables/use-display-refresh.ts
 M rewrite/src/features/display/core/clone.ts
 M rewrite/src/features/display/core/defaults.ts
 M rewrite/src/features/display/core/normalize.ts
 M rewrite/src/features/display/core/projection.ts
 M rewrite/src/features/display/core/types.ts
 M rewrite/src/features/display/core/validation.ts
 M rewrite/src/features/display/fixtures/display-fixtures.ts
 M rewrite/src/features/display/index.ts
 M rewrite/src/features/display/selectors/display-selectors.ts
 M rewrite/src/features/display/services/display-service.ts
 M rewrite/src/features/task/__tests__/task-core.spec.ts
 M rewrite/src/features/task/__tests__/ta[REDACTED_SK].spec.ts
 M rewrite/src/pages/DisplayPage.vue
 M rewrite/src/pages/HomePage.vue
 M rewrite/src/router/routes.ts
?? .omc/state/sessions/0108eb75-c987-428c-97e6-17fddeb5caa7/
?? .omc/state/sessions/0771be24-32a4-485d-9b8b-5a32686d3858/
?? .omc/state/sessions/0e090c31-1a40-4ba0-8ef2-cae323ee521d/
?? .omc/state/sessions/11e420a7-7b18-48f4-a602-553e88b0481f/
?? .omc/state/sessions/145fc589-eca1-4945-86d2-3234cdbe3762/
?? .omc/state/sessions/1e70be19-0ba1-4a75-b8f1-0dd1219804ce/
?? .omc/state/sessions/2281612a-34a4-4ffb-84e6-ff3f18434a1f/
?? .omc/state/sessions/2dd0dca7-96ec-4173-8293-db723880e93f/
?? .omc/state/sessions/2e38b40c-9526-4fd6-afcf-0fa897ffe8c2/
?? .omc/state/sessions/3406d358-0783-497f-9412-94176b85cdaa/
?? .omc/state/sessions/3cf91260-37bc-4c74-b19f-544016e34ff9/
?? .omc/state/sessions/3e99ba09-ac50-4272-ac07-f1771a0896c5/
?? .omc/state/sessions/3f891982-86c5-4f6a-b8cd-e957a8d49df6/
?? .omc/state/sessions/42307e1a-7b3e-48d9-89af-1e91ba5c73b6/
?? .omc/state/sessions/471dd9ec-df93-43cc-99cd-ea2f9b180263/
?? .omc/state/sessions/59304441-3fab-4140-99cd-2f358efe7c08/
?? .omc/state/sessions/60ecd267-e9a1-45a6-a198-1369abc5f79e/
?? .omc/state/sessions/67ed8d9c-24d4-4c78-a3bb-204de2d0ecc5/
?? .omc/state/sessions/70e14fef-3d1a-4eb7-b4f7-8a72129ef2bb/
?? .omc/state/sessions/722c9527-bbbd-4ffc-80a9-5e2a0162efdd/
?? .omc/state/sessions/764d1979-fec0-4de1-b57b-c5e8b9286d30/
?? .omc/state/sessions/7797bae1-6b4c-4107-9778-6d5c76b73930/
?? .omc/state/sessions/81d74a21-6795-403c-b74c-381a8a14cb6f/
?? .omc/state/sessions/84739cc2-9ba1-4b44-a367-1d2a5a1367e9/
?? .omc/state/sessions/8862a360-e494-4400-b471-857bfc36218c/
?? .omc/state/sessions/8870d692-70b2-47eb-b96e-4fa9f09ac2cd/
?? .omc/state/sessions/8a8f4230-57ab-4c5a-8118-651cb27ddc61/
?? .omc/state/sessions/8cd4b1c4-6bef-42b9-b320-8c1ba8376b38/
?? .omc/state/sessions/8ed41665-5456-41ea-864a-88f946a478aa/
?? .omc/state/sessions/91919c76-5ddb-42e4-ab37-947378766b8d/
?? .omc/state/sessions/96dd26ff-72f1-4a87-974d-2d14b1b8129b/
?? .omc/state/sessions/9a146f5c-d6dc-4f7e-9570-d65638ba4c25/
?? .omc/state/sessions/a094972e-fa09-4a92-b195-54baef0e8af1/
?? .omc/state/sessions/a6907ef0-65e2-444b-9991-03a2525a6ae8/
?? .omc/state/sessions/aa24f945-10ee-40ca-8e00-93203df61d51/
?? .omc/state/sessions/abd57e07-acd4-4a3b-9c1f-1941fce2a5ab/
?? .omc/state/sessions/af70f70b-1a30-4e44-89bf-46e49dede3f8/
?? .omc/state/sessions/c0cb43c1-02f0-4831-b812-062e4702bd02/
?? .omc/state/sessions/c430e301-1019-4799-8cf1-d135e6e4aa67/
?? .omc/state/sessions/cd448a9f-a839-46b3-9b12-268ff4f64ddc/
?? .omc/state/sessions/d88d91ec-e7e3-44f5-a84a-2eabcffea1d4/
?? .omc/state/sessions/dc9d3527-1ef7-4073-86ec-80d59f028b48/
?? .omc/state/sessions/de3bea8c-4fec-4ee0-9c93-dccc2a29ff56/
?? .omc/state/sessions/de65dd18-e06f-430e-b3fc-eca81f915e9f/
?? .omc/state/sessions/e591898f-57c5-430e-b6a0-b587b0c79662/
?? .omc/state/sessions/e60a4bee-6cb8-4b88-8586-8a789e7bf9eb/
?? .omc/state/sessions/ef5da558-382e-4e7c-b028-9f35f5be53a9/
?? .omc/state/sessions/f692bfb7-f1db-4383-8209-b36e6f82bd1d/
?? .omc/state/sessions/fa9a7e84-4a45-4d0b-91a6-f4b1b45d0203/
?? .omc/state/sessions/fcd7d3b7-cc35-421d-aa19-4aa85962badf/
?? .sessions/2026-05-21-missing-pages/
?? codestable/features/2026-05-24-settings-page/
?? codestable/features/rewrite-northbound/
?? codestable/quality/ui-audit-2026-05-15.md
?? rewrite/docs/
?? rewrite/src/pages/SettingsPage.vue
?? rewrite/src/pages/settings/
?? "\346\226\260\347\224\262\346\226\271\346\226\207\346\241\243.md"
?? "\351\233\206\346\210\220\346\265\213\350\257\225\347\263\273\347\273\237\344\270\216\345\220\204\344\272\214\347\272\247\345\255\220\347\263\273\347\273\237\346\216\245\345\217\243\350\256\276\350\256\2410513.docx"
```

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