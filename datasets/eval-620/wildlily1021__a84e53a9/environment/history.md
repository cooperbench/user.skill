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