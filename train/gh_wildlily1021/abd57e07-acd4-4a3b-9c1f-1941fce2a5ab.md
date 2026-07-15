> DEVELOPER

/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/conversation-plan.md 对话4

> DEVELOPER

/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/conversation-plan.md 对话4

> TOOL

tool_use Read
id: call_a54e8a07c9284b208f7c3fd1
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/conversation-plan.md"
}
```

> TOOL

tool_result
id: call_a54e8a07c9284b208f7c3fd1
```
1	# 集成测试：完整对话规划 + 提示词
2	
3	> 7 轮对话，5 轮可并行，总计约 60 个子 agent
4	
5	## 并行关系
6	
7	```
8	对话 1（历史）──┐
9	对话 2（feature 上）──┤
10	对话 3（feature 下）──┼──→ 对话 6（综合）──→ 对话 7+（实施）
11	对话 4（旧代码）──┤
12	对话 5（新代码接缝）──┘
13	```
14	
15	对话 1-5 完全独立，可以同时开 5 个 Claude Code 对话并行跑。对话 6 等前 5 个全部完成后再开。
16	
17	---
18	
19	## 对话 1：历史讨论提取
20	
21	**专题文件**：`.sessions/2026-05-19-integration-testing/S001-historical-extraction.md`
22	**Agent 数**：12 个，4 批 × 3
23	
24	### 提示词
25	
26	```
27	## 任务
28	
29	调研 rewrite 项目中集成测试的验收承诺现状，从 26 天的历史讨论记录中提取所有验收标准、已知缺口和测试期望，产出事实报告，不做任何设计或实施。
30	
31	## 调研范围
32	
33	1. 每个阶段（S001-S015）承诺了什么验收标准？
34	2. 哪些验收标准有单测证据（列具体 tests 数量和文件名）？
35	3. 哪些验收标准只有"已通过"结论但无具体测试证据？
36	4. 所有标记为 known-gaps / deferred / 推迟 / 待后续 的条目
37	5. 所有涉及"真实硬件验证"、"runtime validation"、"端到端"的提及
38	6. 跨 feature 交互中哪些只在集成时才出现（单元测不到的接缝）
39	
40	## 子 agent 策略
41	
42	4 批，每批 3 个 agent 并行。
43	
44	### 批次 1
45	
46	#### Agent 1：S001 + S002（架构奠基 + 基础 feature）
47	- 读：`.sessions/2026-04-23-rewrite-main-thread/S001-architecture-codestable-foundation.md`、`S002-first-features-and-review.md`
48	- 回答：
49	  1. S001 的 16 条质量红线（R1-R16）中，哪些直接要求集成测试级别的验证？
50	  2. S001 第 10 节"Northbound 独立定位"中的所有"不得"项，哪些需要集成测试证明合规？
51	  3. S002 的 7 个基础 feature 各自的 Verdict 和具体 tests 数量？
52	  4. 交叉审查 M1（ReadonlyDeep 重复）修复后的验证证据？
53	  5. Send/Task/SCOE/Result 的 design 完成后，验收标准具体是什么？
54	
55	#### Agent 2：S003 + S004（三线并行 + 密集讨论日）
56	- 读：`.sessions/2026-04-23-rewrite-main-thread/S003-send-bridge-scoe-three-lanes.md`、`S004-ta[REDACTED_SK].md`
57	- 回答：
58	  1. S003 三线并行各自的验收证据是什么？Bridge Phase 1-3 的 pass-with-known-gaps 具体 gaps？
59	  2. S003 执行引擎统一决策的 6 项（D1-D6），哪些有测试证明、哪些只有文档？
60	  3. S004 的 19 个对话中，task service 层实现修复了哪些 bug？这些 bug 是否暗示集成缺陷？
61	  4. S004 settings 完整闭环的验证方式？Runtime wiring 三连的测试覆盖？
62	  5. S004 架构文档 34 处同步，是否引入了文档-代码不一致风险？
63	
64	#### Agent 3：S005 + S014（架构审计 + 主控对话）
65	- 读：`.sessions/2026-04-23-rewrite-main-thread/S005-receive-real-design-and-audit.md`、`S014-runtime-real-master-control.md`
66	- 回答：
67	  1. S005 的 6 维度审计结果：1 违规 + 10 风险的具体内容，哪些需要集成测试覆盖？
68	  2. S005 旧系统三线调研发现了什么？新旧覆盖矩阵中 P0/P1/P2 缺口是什么？
69	  3. S014 主控对话 7 阶段每个阶段留下的未决项？
70	  4. S014 阶段 6（事件恢复）中丢失的 14 个文件，恢复后是否全部验证？
71	  5. S014 阶段 7 的进度盘点，哪些 feature 声称 100% 完成但缺少 runtime 证据？
72	
73	### 批次 2
74	
75	#### Agent 4：S007（Real Feature 实施期）
76	- 读：`.sessions/2026-04-23-rewrite-main-thread/S007-real-feature-implementation.md`
77	- 回答：
78	  1. Expression Engine 112 tests 覆盖了什么能力？没覆盖什么（特别是集成到 receive/send/task 时）？
79	  2. Frame-real 验收中"L2 消费者测试通过（receive 9 pass + runtime 28 pass）"具体指什么？
80	  3. Receive-real Phase 1-4 各阶段的测试数量？Phase 4 背压测试的验证方式？
81	  4. Platform-network-transport 的 9 条 acceptance criteria 中，AC1-AC3 需要"手动网络验证"具体指什么？
82	  5. Connection 580+ tests 和 Send-real 100 tests 是单元级还是集成级？
83	  6. Task-real brainstorm 和 Command-ingress brainstorm 锁定的设计决策，哪些还没实现？
84	
85	#### Agent 5：S008（Feature 验收期）
86	- 读：`.sessions/2026-04-23-rewrite-main-thread/S008-feature-acceptance-and-command-ingress.md`
87	- 回答：
88	  1. Task-real Phase 1 验收 PASS 的证据？Phase 2 验收 PASS-WITH-KNOWN-GAPS 的 known-gaps？
89	  2. Task-real 间歇性测试失败的根因？30-40% 套件间歇性失败是否已解决？
90	  3. Command-ingress W1/W2/W3 各波的测试数量？W2 中 CRITICAL 修复是否需要回归保护？
91	  4. Command-ingress 验收 PASS 时 803 tests 是否包含跨 feature 集成？
92	  5. Receive-real 最终验收的 globalParams 推迟，对集成测试的影响？
93	  6. Storage-real 的 6 个外部依赖 gap 具体是什么？
94	
95	#### Agent 6：S009 + S010（简化 + 测试修复）
96	- 读：`.sessions/2026-04-23-rewrite-main-thread/S009-simplification-audit-and-ui-design.md`、`S010-test-fix-send-task-simplification.md`
97	- 回答：
98	  1. 代码简化审计 5 个 feature 的发现：clone 重复、selector 死 surface、validation 重复——这些简化是否引入回归风险？
99	  2. Send/Task 简化实施的 S-S1~S-S3、T-S1~T-S2 是否全部完成？
100	  3. S010 的 66 个测试失败根因分析？修复后哪些还没跑通？
101	  4. S010 第 76 行列出的 7 项待验证风险，当前状态？
102	  5. Receive processor 中间状态（unused import）是否已清理？
103	
104	### 批次 3
105	
106	#### Agent 7：S011 上半（Wave 0-4 + 审计）
107	- 读：`.sessions/2026-04-23-rewrite-main-thread/S011-ui-infrastructure-and-pages.md`（重点 05-13 部分）
108	- 回答：
109	  1. Wave 0 Task 类型重组 30 项，是否全部有测试？
110	  2. Wave 1-3 expression 集成到 receive 的验证方式？
111	  3. Wave 4 基础设施中 connection selectors dead surface 删除（142 行），是否导致回归？
112	  4. 设计-代码对齐审计发现的 8 个不一致，修复后是否验证？
113	
114	#### Agent 8：S011 下半（6 页面 + 审计修复）
115	- 读：`.sessions/2026-04-23-rewrite-main-thread/S011-ui-infrastructure-and-pages.md`（重点 05-15 部分）
116	- 回答：
117	  1. 85 文件大提交后 build/lint/test 的具体结果？
118	  2. 47 项 UI 审计中 P0 的 3 项（任务编辑弹窗拆分、发送编辑弹窗加 QForm、CI 高亮弹窗 @hide 清理）是否影响数据通路？
119	  3. Service 完成度调查确认"10 个 feature service 层全部 100%"——证据是什么？逐个 feature 列出？
120	  4. SendPage P0 Bug（direction 值错误）修复后是否有回归测试？
121	
122	#### Agent 9：S012 + S015（持久化 + 集测起点）
123	- 读：`.sessions/2026-04-23-rewrite-main-thread/S012-persistence-and-process-organization.md`、`S015-integration-testing.md`
124	- 回答：
125	  1. LazyPersistence 模式在什么场景下数据会丢？（启动中崩溃、save 时机未设计）
126	  2. RealLocalMaterialAdapter 软删除策略（写 .deleted 文件）是否测试过？
127	  3. 只实现了 frames 的启动加载，connections 和 settings 的恢复状态？
128	  4. S015 已列的 10 个集测维度，是否有遗漏或多余？
129	
130	### 批次 4
131	
132	#### Agent 10：质量规则中的测试要求
133	- 读：`codestable/quality/rewrite-quality-rules.md`（全文）
134	- 回答：
135	  1. §8 Minimum Test Expectations 列出的 9 项优先 fixture，每一项的当前覆盖状态？
136	  2. §9 Quality Gate 的实施前/中/后检查项，哪些是集成测试级别才能覆盖的？
137	  3. §10 Current Evidence Notes 中的 8 条旧代码事实，哪些需要在集成测试中证明"新系统已消灭"？
138	
139	#### Agent 11：审查清单中的验证层级
140	- 读：`codestable/quality/rewrite-review-checklist.md`（重点 §8 高频数据、§9 Receive/Send、§14 Oracle）
141	- 回答：
142	  1. §14 的 10 级验证 taxonomy 中，rewrite 项目当前覆盖到了哪几级？
143	  2. §8 高频数据 checklist 中的每一项，是否需要真 TCP 集成测试？
144	  3. §9 Receive/Send checklist 中的 red flags，新系统是否真正避免了每一个？
145	
146	#### Agent 12：H002 TCP 接线验证状态
147	- 读：`.sessions/2026-04-23-rewrite-main-thread/H002-local-tcp-loopback-handoff.md`、`rewrite/src/features/connection/adapters/composite-adapter.ts`、`rewrite/src/app/rewriteRuntime.ts`
148	- 回答：
149	  1. Composite adapter 的实现是否完整？哪些边界情况没覆盖？
150	  2. Bootstrap 同时创建 serial + network adapter 后，wireFeatures 是否正确路由？
151	  3. fanOutToStorage 调用加了之后，storage bridge 是否真正写入数据？
152	  4. 有没有实际跑过 TCP 环路的证据？
153	
154	## 汇报要求
155	
156	- 中文，facts-first
157	- 每条发现标注来源 note 编号和段落
158	- 不确定标注"待确认"
159	- 最终产出写入 `.sessions/2026-05-19-integration-testing/S001-historical-extraction.md`
160	```
161	
162	---
163	
164	## 对话 2：Feature 设计文档提取（上）
165	
166	**专题文件**：`.sessions/2026-05-19-integration-testing/S002-feature-designs-upper.md`
167	**Agent 数**：9 个，3 批 × 3
168	
169	### 提示词
170	
171	```
172	## 任务
173	
174	调研 rewrite 项目中 5 个核心 feature 的设计文档，提取所有验收标准、跨 feature 交互契约和测试期望，产出事实报告，不做任何设计或实施。
175	
176	## 调研范围
177	
178	从 codestable/features/ 下的 design.md + checklist.yaml（如有 brainstorm.md 也读）提取：
179	1. 每个 feature 的验收标准原文
180	2. 跨 feature 交互契约（依赖哪些 feature、被哪些 feature 消费）
181	3. checklist 中的测试项
182	4. 已标注的 known-gaps 和 deferred 项
183	
184	## 子 agent 策略
185	
186	3 批，每批 3 个 agent 并行。
187	
188	### 批次 1
189	
190	#### Agent 1：frame feature
191	- 读：`codestable/features/rewrite-frame/` 下所有 .md 和 .yaml
192	- 读：`codestable/features/rewrite-frame-real/` 下所有 .md 和 .yaml（如存在）
193	- 读：`rewrite/src/features/frame/index.ts`（public API surface）
194	- 回答：
195	  1. frame design 的验收标准逐条列出
196	  2. frame 被哪些 feature 消费？消费方式（通过 public API 还是通过其他方式）？
197	  3. frame-real design 的增量验收标准？
198	  4. checklist 中标注的测试项，哪些已实现、哪些未实现？
199	  5. 帧定义全局唯一约束在设计层面如何保证？集成测试能否验证？
200	
201	#### Agent 2：connection feature
202	- 读：`codestable/features/rewrite-connection/` 下所有 .md 和 .yaml
203	- 读：`codestable/features/rewrite-connection-complete/` 下所有 .md 和 .yaml（如存在）
204	- 读：`rewrite/src/features/connection/index.ts`
205	- 回答：
206	  1. connection design 的验收标准逐条列出
207	  2. connection 与 platform/transport 的交互契约？
208	  3. connection-complete 的增量验收标准？
209	  4. TCP/UDP 连接的 lifecycle 设计，哪些状态转换需要集成测试？
210	  5. composite adapter 加入后，设计文档是否需要更新？
211	
212	#### Agent 3：receive feature
213	- 读：`codestable/features/rewrite-receive/` 下所有 .md 和 .yaml
214	- 读：`codestable/features/receive-real-pipeline/` 下所有 .md 和 .yaml（如存在）
215	- 读：`rewrite/src/features/receive/index.ts`
216	- 回答：
217	  1. receive design 的验收标准逐条列出
218	  2. receive-real-pipeline roadmap 的各阶段验收标准？
219	  3. receive 消费 frame 的方式？与 expression engine 的集成契约？
220	  4. 扇出到 display/storage/task 的设计，每个扇出路径的验收条件？
221	  5. globalParams 收集推迟的影响范围？
222	
223	### 批次 2
224	
225	#### Agent 4：send feature
226	- 读：`codestable/features/rewrite-send/` 下所有 .md 和 .yaml
227	- 读：`codestable/features/send-real/` 下所有 .md 和 .yaml（如存在）
228	- 读：`rewrite/src/features/send/index.ts`
229	- 回答：
230	  1. send design 的验收标准逐条列出
231	  2. send-real design 的 9 步 pipeline 验收标准？
232	  3. send 与 connection 的交互契约（transportWriter、targetResolver）？
233	  4. send 与 frame 的交互契约（frameReader）？
234	  5. checksum/patch 的边界情况（CRC32、length field backfill）需要什么级别的测试？
235	
236	#### Agent 5：expression engine
237	- 读：`codestable/features/2026-05-08-expression-engine/` 下所有 .md 和 .yaml
238	- 读：`rewrite/src/shared/expression/index.ts`
239	- 读：`rewrite/src/shared/expression/__tests__/` 下所有 spec 文件名（不需要读内容，只看测试覆盖了哪些模块）
240	- 回答：
241	  1. expression engine design 的验收标准逐条列出
242	  2. 112 tests 覆盖了哪些能力？（从 spec 文件名推断）
243	  3. expression 集成到 receive/send/task 时的契约变化？
244	  4. 性能要求（P1/P2）的具体数值和当前验证状态？
245	  5. shared/ 纯 TS 约束的验证方式？
246	
247	#### Agent 6：runtime wiring
248	- 读：`codestable/features/2026-05-07-runtime-wiring/` 下所有 .md 和 .yaml
249	- 读：`rewrite/src/runtime/index.ts`、`rewrite/src/runtime/feature-wiring.ts`
250	- 回答：
251	  1. runtime wiring design 的验收标准逐条列出
252	  2. event-driven 架构（routingTick）的验收条件？
253	  3. 5 条缺失数据通路的修复状态？
254	  4. runtime 与各 feature 的装配契约（wireFeatures 接口）？
255	  5. routingTick 预算截断的验收条件？
256	
257	### 批次 3
258	
259	#### Agent 7：settings feature
260	- 读：`codestable/features/rewrite-settings/` 下所有 .md 和 .yaml
261	- 读：`rewrite/src/features/settings/index.ts`
262	- 回答：
263	  1. settings design 的验收标准逐条列出
264	  2. settings 作为 7 个下游 feature 的配置输入源，契约是什么？
265	  3. normalize/validation 的测试覆盖？
266	  4. 持久化集成状态？
267	
268	#### Agent 8：storage-local-baseline feature
269	- 读：`codestable/features/rewrite-storage-local-baseline/` 下所有 .md 和 .yaml
270	- 读：`rewrite/src/features/storage-local-baseline/index.ts`
271	- 回答：
272	  1. storage design 的验收标准逐条列出
273	  2. adapter port 模式的验证？
274	  3. RealLocalMaterialAdapter 的验证状态？
275	  4. 与 platform file facade 的集成契约？
276	  5. 6 个外部依赖 gap 具体是什么？
277	
278	#### Agent 9：display + status features
279	- 读：`codestable/features/rewrite-display/` 下所有 .md 和 .yaml
280	- 读：`codestable/features/rewrite-status/` 下所有 .md 和 .yaml
281	- 读：`rewrite/src/features/display/index.ts`、`rewrite/src/features/status/index.ts`
282	- 回答：
283	  1. display design 的验收标准？特别是 table/chart/constellation projection
284	  2. status design 的验收标准？
285	  3. 身份标识统一（groupId→frameId, dataItemId→fieldId）的实施状态？
286	  4. display 与 receive 的扇出 bridge 验收？
287	
288	## 汇报要求
289	
290	- 中文，facts-first
291	- 每条发现标注来源文件路径和段落
292	- 不确定标注"待确认"
293	- 最终产出写入 `.sessions/2026-05-19-integration-testing/S002-feature-designs-upper.md`
294	```
295	
296	---
297	
298	## 对话 3：Feature 设计文档提取（下）
299	
300	**专题文件**：`.sessions/2026-05-19-integration-testing/S003-feature-designs-lower.md`
301	**Agent 数**：9 个，3 批 × 3
302	
303	### 提示词
304	
305	```
306	## 任务
307	
308	调研 rewrite 项目中 task/command-ingress/result/report 四个 feature 的设计文档，提取所有验收标准、跨 feature 交互契约和测试期望，产出事实报告。
309	
310	## 子 agent 策略
311	
312	3 批，每批 3 个 agent 并行。
313	
314	### 批次 1
315	
316	#### Agent 1：task feature（核心）
317	- 读：`codestable/features/rewrite-task/` 下所有 .md 和 .yaml
318	- 读：`rewrite/src/features/task/index.ts`
319	- 回答：
320	  1. task design 的验收标准逐条列出（通用执行引擎定位）
321	  2. ScheduleDriver 4 种模式的验收条件？
322	  3. step 多态化（send-step/wait-condition-step/delay-step）的验收？
323	  4. condition-matcher 的 AND/OR 组合验证？
324	  5. task 与 send/receive 的交互契约（ports 依赖注入）？
325	
326	#### Agent 2：task-real design
327	- 读：`codestable/features/rewrite-task/task-real-design.md`（如存在）
328	- 读：`rewrite/src/features/task/core/types.ts`（看 ScheduleDriver/ConditionTerm 等新类型）
329	- 回答：
330	  1. task-real 的详细设计验收标准？
331	  2. Phase 1（类型+条件）和 Phase 2（统一引擎）各自的 checklist？
332	  3. FieldVariation + StepRepeat 的验收条件？
333	  4. TimerService port 的设计？
334	  5. 间歇性测试失败的根因和解决方案？
335	
336	#### Agent 3：command-ingress feature
337	- 读：`codestable/features/rewrite-command-ingress/` 下所有 .md 和 .yaml
338	- 读：`rewrite/src/features/command-ingress/index.ts`
339	- 回答：
340	  1. command-ingress design 的验收标准逐条列出
341	  2. SCOE protocol adapter（两阶段状态机）的验收？
342	  3. 6 种 handler 的验收条件？
343	  4. TaskBuilder 的翻译逻辑验收（ScoeCommand → TaskDefinition）？
344	  5. 消费者链（routingTick integration）的验收？
345	
346	### 批次 2
347	
348	#### Agent 4：command-ingress 详解
349	- 读：`rewrite/src/features/command-ingress/core/protocol-adapter.ts`
350	- 读：`rewrite/src/features/command-ingress/core/task-builder.ts`
351	- 读：`rewrite/src/features/command-ingress/__tests__/scoe-protocol-adapter.spec.ts`（只看 describe 块和 it 块的描述）
352	- 回答：
353	  1. 协议解析的测试覆盖了哪些功能码？
354	  2. TaskBuilder 翻译了哪些命令类型？每种类型的测试？
355	  3. 迁移脚本的验证覆盖？
356	
357	#### Agent 5：result + report features
358	- 读：`codestable/features/rewrite-result/` 下所有 .md 和 .yaml
359	- 读：`codestable/features/rewrite-report/` 下所有 .md 和 .yaml（如存在）
360	- 读：`rewrite/src/features/result/index.ts`、`rewrite/src/features/report/index.ts`
361	- 回答：
362	  1. result design 的验收标准？
363	  2. Result/Report/Northbound 三层分离的验证？
364	  3. TaskInstanceCompletion 作为唯一素材入口的验证？
365	  4. report feature 的设计状态（是否已有 design.md）？
366	
367	#### Agent 6：northbound feature
368	- 读：`codestable/compound/2026-04-28-northbound-overlap-and-gap-map.md`
369	- 读：`.sessions/2026-05-18-northbound-integration/` 下所有文件（如果有）
370	- 回答：
371	  1. northbound 的 gap 清单？
372	  2. 甲方 4 接口闭环决策的具体内容？
373	  3. 哪些 northbound 能力需要在集成测试中覆盖？
374	  4. MVP 6 接口的状态？
375	
376	### 批次 3
377	
378	#### Agent 7：跨 feature 交互矩阵
379	- 读：`codestable/architecture/rewrite-feature-interaction-matrix.md`（如存在）
380	- 读：`codestable/architecture/rewrite-feature-boundaries.md`
381	- 回答：
382	  1. 所有 feature 之间的交互路径？
383	  2. 哪些交互路径有测试覆盖、哪些没有？
384	  3. 哪些交互是 runtime 编排（bridge）、哪些是直接 public API 调用？
385	
386	#### Agent 8：统一执行引擎决策
387	- 读：`codestable/compound/2026-05-06-ta[REDACTED_SK].md`
388	- 读：`codestable/compound/2026-05-06-outbound-routing-and-response-decisions.md`
389	- 回答：
390	  1. 统一执行引擎 6 项决策各自的验证方式？
391	  2. 出站路由 4 个决策的验证？
392	  3. 三条出站路径（用户/SCOE/Northbound）的集成测试需求？
393	
394	#### Agent 9：旧系统调研事实
395	- 读：`codestable/compound/2026-05-07-old-system-investigation-scoe-expression-visualization.md`（如存在）
396	- 回答：
397	  1. 旧 SCOE 的 22 文件功能清单中哪些行为必须保留？
398	  2. 旧表达式引擎的 1385 行中哪些行为必须保留？
399	  3. 旧可视化 1074 行中哪些行为必须保留？
400	
401	## 汇报要求
402	
403	- 中文，facts-first
404	- 每条发现标注来源文件路径和段落
405	- 不确定标注"待确认"
406	- 最终产出写入 `.sessions/2026-05-19-integration-testing/S003-feature-designs-lower.md`
407	```
408	
409	---
410	
411	## 对话 4：旧系统可观测行为提取
412	
413	**专题文件**：`.sessions/2026-05-19-integration-testing/S004-legacy-observable-behaviors.md`
414	**Agent 数**：9 个，3 批 × 3
415	
416	### 提示词
417	
418	```
419	## 任务
420	
421	调研 rewrite 项目的旧系统代码，提取所有必须保留的可观测业务行为，作为集成测试的 oracle 来源。产出事实报告。
422	
423	## 调研范围
424	
425	从旧代码（`src/`）中提取：
426	1. 旧系统的用户可见行为（页面操作、数据流、定时任务、SCOE 命令等）
427	2. 每个行为在新系统中的对应 feature
428	3. 可作为 oracle 的旧代码位置
429	4. 保留/排除建议
430	
431	## 子 agent 策略
432	
433	3 批，每批 3 个 agent 并行。
434	
435	### 批次 1
436	
437	#### Agent 1：旧 receive/send 数据流
438	- 读：`src/stores/frames/receiveFramesStore.ts`（重点看数据流入、解析、统计、触发逻辑）
439	- 读：`src/composables/frames/sendFrame/useUnifiedSender.ts`（发送流程）
440	- 回答：
441	  1. 旧 receive 的完整数据流路径（从串口/网络收到字节 → 解析 → 展示 → 触发）？
442	  2. 旧 send 的完整流程（从用户点击 → 构帧 → 发送 → 结果）？
443	  3. receiveFramesStore 承载了哪些不应该在一个 store 里的职责？
444	  4. useUnifiedSender 的 SCOE UDP target 特判具体逻辑？
445	  5. 这些行为的 oracle 来源（可以录制的输入输出样本）？
446	
447	#### Agent 2：旧 SCOE/task 执行
448	- 读：`src/stores/scoeStore.ts`（配置 + 状态 + 连接 + 发送 + 测试工具）
449	- 读：`src/components/frames/FrameSend/TimedSend/TimedSendDialog.vue`（定时发送）
450	- 读：`src/components/frames/FrameSend/TriggerSend/TriggerSendDialog.vue`（触发发送）
451	- 回答：
452	  1. 旧 SCOE 的完整命令处理流程（接收 → 解析 → 执行 → 确认）？
453	  2. 旧定时发送的完整流程？
454	  3. 旧触发发送的条件判断逻辑？
455	  4. SCOE 测试工具的录制/回放行为？
456	  5. 这些行为的 oracle 来源？
457	
458	#### Agent 3：旧连接管理
459	- 读：`src/stores/serialStore.ts`（串口连接生命周期）
460	- 读：`src/stores/netWorkStore.ts`（网络连接生命周期）
461	- 读：`src-electron/main/ipc/networkHandlers.ts`（main 进程网络处理）
462	- 回答：
463	  1. 旧串口连接的完整生命周期（打开 → 配置 → 收发 → 断开 → 重连）？
464	  2. 旧 TCP/UDP 连接的完整生命周期？
465	  3. 旧网络接收中的高速存储分流逻辑？
466	  4. 连接状态在 UI 上的展示行为？
467	  5. 这些行为的 oracle 来源？
468	
469	### 批次 2
470	
471	#### Agent 4：旧表达式/解析
472	- 读：`src/utils/expressionEngine.ts`（如存在）或 grep 找到旧表达式引擎代码
473	- 读：`src/utils/frames/frameParser.ts`（如存在）或 grep 找到旧帧解析代码
474	- 回答：
475	  1. 旧表达式引擎的核心行为？（求值、依赖排序、缓存）
476	  2. 旧帧解析的核心行为？（字节到字段、applyFactor）
477	  3. 旧条件判断的核心行为？（AND/OR 组合、触发条件）
478	  4. 有哪些旧配置文件样本可以作为 oracle？
479	
480	#### Agent 5：旧存储/历史/CSV
481	- 读：`src/stores/historyDataStore.ts`（如存在）
482	- 读：旧 CSV 导出/导入相关代码
483	- 回答：
484	  1. 旧历史数据的存储和查询行为？
485	  2. 旧 CSV 导出的格式和行为？
486	  3. 旧数据导入的行为？
487	  4. 这些在新系统中的对应 feature？
488	
489	#### Agent 6：旧帧定义管理
490	- 读：`src/stores/frames/framesConfigStore.ts`（如存在）
491	- 读：`src/stores/frames/frameInstanceStore.ts`（如存在）
492	- 回答：
493	  1. 旧帧定义的 CRUD 行为？
494	  2. 旧帧实例的管理行为？
495	  3. 旧帧导入/导出的格式和行为？
496	  4. 旧 JSON 格式与新格式的差异？
497	
498	### 批次 3
499	
500	#### Agent 7：旧状态展示
501	- 读：旧状态指示、健康检查相关代码
502	- 回答：
503	  1. 旧连接状态指示的具体展示行为？
504	  2. 旧健康检查的行为？
505	  3. 旧统计展示的行为？
506	
507	#### Agent 8：旧设置/配置
508	- 读：旧设置相关 store 或配置文件
509	- 回答：
510	  1. 旧系统的配置项完整清单？
511	  2. 每个配置项在新系统中的对应？
512	  3. 配置持久化的旧行为？
513	
514	#### Agent 9：旧系统页面入口完整清单
515	- 读：`src/router/` 下路由配置
516	- 读：旧系统侧边栏/导航组件
517	- 回答：
518	  1. 旧系统所有页面入口和路由？
519	  2. 每个入口在新系统中的对应路由？
520	  3. 是否有入口在新系统中缺失？
521	
522	## 汇报要求
523	
524	- 中文，facts-first
525	- 每条行为标注旧代码位置（文件:行号）
526	- 每条行为标注新系统对应 feature
527	- 标注 oracle 来源（代码位置/配置文件样本/截图/可录制）
528	- 最终产出写入 `.sessions/2026-05-19-integration-testing/S004-legacy-observable-behaviors.md`
529	```
530	
531	---
532	
533	## 对话 5：新系统接缝审计
534	
535	**专题文件**：`.sessions/2026-05-19-integration-testing/S005-new-system-seam-audit.md`
536	**Agent 数**：9 个，3 批 × 3
537	
538	### 提示词
539	
540	```
541	## 任务
542	
543	调研 rewrite 项目新系统的 runtime 接缝、adapter 边界和持久化时序，识别所有集成级别的断裂风险。产出事实报告。
544	
545	## 调研范围
546	
547	从 rewrite/src/runtime/、features/*/adapters/、features/*/services/ 中识别：
548	1. 所有 bridge 的数据流向和可能的断裂点
549	2. composite adapter 的边界情况
550	3. persistence 的时序风险
551	4. routingTick 的竞态和背压风险
552	
553	## 子 agent 策略
554	
555	3 批，每批 3 个 agent 并行。
556	
557	### 批次 1
558	
559	#### Agent 1：所有 bridge 文件逐个审计
560	- 读：`rewrite/src/runtime/bridges/` 下所有 .ts 文件
561	- 对每个 bridge 回答：
562	  1. 接收什么输入、产出什么输出
563	  2. 输入为空时的行为
564	  3. 下游失败时的错误传播
565	  4. 高频数据下的缓冲/节流机制
566	  5. 需要什么集成测试覆盖
567	
568	#### Agent 2：composite adapter + real adapters 审计
569	- 读：`rewrite/src/features/connection/adapters/composite-adapter.ts`
570	- 读：`rewrite/src/features/connection/adapters/real-network-adapter.ts`
571	- 读：`rewrite/src/features/connection/adapters/real-serial-adapter.ts`
572	- 回答：
573	  1. composite adapter 的 config.kind 路由是否覆盖所有 TransportKind？
574	  2. serial adapter 不可用时，serial 连接的错误行为？
575	  3. network adapter 的 TCP server/client 模式差异？
576	  4. UDP write 无 remoteHost/remotePort 时的错误行为？
577	  5. drainEvents() 的批量行为和可能的竞态？
578	
579	#### Agent 3：platform facade + main handlers 审计
580	- 读：`rewrite/src/platform/transport.ts`
581	- 读：`rewrite/src-electron/main/network-handlers.ts`
582	- 读：`rewrite/src-electron/preload/index.ts`（transport 部分）
583	- 回答：
584	  1. platform facade 的缓存/单例行为？
585	  2. main TCP server 的 client 连接/断开事件传播？
586	  3. preload IPC 的 serial vs network 路由逻辑？
587	  4. 批量传输的 batch 参数和窗口行为？
588	
589	### 批次 2
590	
591	#### Agent 4：routingTick 数据流审计
592	- 读：`rewrite/src/runtime/routing-tick.ts`
593	- 读：`rewrite/src/runtime/__tests__/helpers.ts`（看 mock 结构）
594	- 回答：
595	  1. drainAdapterEvents → filter data → drainInputSource → fanOut 的完整链路
596	  2. 100ms 间隔下的背压风险？如果一次 drain 产出大量事件会怎样？
597	  3. maxEventsPerTick=50 截断后，被截断的事件是否丢失？
598	  4. receiveService.drainInputSource 的内部行为（同步还是异步、是否缓冲）？
599	  5. fanOutToDisplay 和 fanOutToStorage 的错误隔离？
600	
601	#### Agent 5：feature service 交互接缝
602	- 读：`rewrite/src/features/send/services/send-service.ts`（看 transportWriter 和 targetResolver 调用点）
603	- 读：`rewrite/src/features/task/services/task-service.ts`（看 sendService 和 receiveEventSource 调用点）
604	- 读：`rewrite/src/features/command-ingress/services/command-ingress-service.ts`（看 taskService 和 sendService 调用点）
605	- 回答：
606	  1. send-service 调用 transportWriter.write 时的错误传播？
607	  2. task-service 调用 sendService.execute 后的结算逻辑？
608	  3. command-ingress-service 创建 task 后的监控逻辑？
609	  4. 这些 service 间交互的集成测试缺口？
610	
611	#### Agent 6：persistence 时序审计
612	- 读：`rewrite/src/runtime/persistence.ts`
613	- 读：`rewrite/src/app/rewriteRuntime.ts`（LazyPersistence 部分）
614	- 回答：
615	  1. LazyPersistence setDelegate 前后的行为差异？
616	  2. load() 并发读三个文件的错误隔离？
617	  3. save*() 系列方法的触发时机？（当前只有手动）
618	  4. frames 启动加载后 replaceFrames 的副作用？
619	  5. connections 和 settings 的启动恢复缺失的影响？
620	
621	### 批次 3
622	
623	#### Agent 7：connection service lifecycle 审计
624	- 读：`rewrite/src/features/connection/services/` 下所有 .ts 文件
625	- 回答：
626	  1. connect → connected → data flow → disconnect 的完整生命周期
627	  2. reconnect 机制的当前状态？
628	  3. 多连接并发时的 adapter 共享行为？
629	  4. autoConnect 的实现状态？
630	
631	#### Agent 8：receive pipeline 接缝审计
632	- 读：`rewrite/src/features/receive/core/processor.ts`
633	- 读：`rewrite/src/features/receive/core/expression-pass.ts`
634	- 回答：
635	  1. processor 的完整处理链（match → parse → expression → output）
636	  2. expression pass 失败时的错误传播？
637	  3. read model 更新频率和竞态风险？
638	
639	#### Agent 9：现有集成测试覆盖审计
640	- 读：`rewrite/src/runtime/__tests__/feature-wiring.spec.ts`（看测试了什么）
641	- 读：`rewrite/src/runtime/__tests__/routing-tick.spec.ts`（看 mock 了什么）
642	- 读：`rewrite/src/runtime/__tests__/bootstrap-integration.spec.ts`
643	- 回答：
644	  1. 现有 runtime 测试覆盖了哪些集成场景？
645	  2. mock 替代了哪些真实依赖？
646	  3. 哪些 mock 在真实环境下行为可能不同？
647	  4. 给出"现有测试已覆盖"和"需要新集成测试"的分界线
648	
649	## 汇报要求
650	
651	- 中文，facts-first
652	- 每条发现标注文件路径和行号
653	- 对每个接缝给出风险等级（高/中/低）和建议的测试类型
654	- 最终产出写入 `.sessions/2026-05-19-integration-testing/S005-new-system-seam-audit.md`
655	```
656	
657	---
658	
659	## 对话 6：综合 + 排除 + 优先级（等 1-5 全部完成后）
660	
661	**专题文件**：`.sessions/2026-05-19-integration-testing/S006-test-scope-synthesis.md`
662	**Agent 数**：1-2（本对话以主线程综合为主）
663	
664	### 提示词
665	
666	```
667	## 任务
668	
669	综合 S001-S005 所有提取结果，去重、排除已有单测覆盖的项、分级优先级，产出最终集测范围清单。
670	
671	## 必读
672	
673	1. `.sessions/2026-05-19-integration-testing/S001-historical-extraction.md`
674	2. `.sessions/2026-05-19-integration-testing/S002-feature-designs-upper.md`
675	3. `.sessions/2026-05-19-integration-testing/S003-feature-designs-lower.md`
676	4. `.sessions/2026-05-19-integration-testing/S004-legacy-observable-behaviors.md`
677	5. `.sessions/2026-05-19-integration-testing/S005-new-system-seam-audit.md`
678	
679	## 排除规则
680	
681	以下条目排除出集测清单：
682	- 已有 815+ 单测覆盖的 feature 内部逻辑
683	- 纯 UI 展示/样式问题（归 manual checklist）
684	- 涉及真实串口/SCOE 硬件的验证（归 hardware validation）
685	- 涉及甲方 northbound HTTP/FTP 的验证（归 customer validation）
686	
687	## 产出格式
688	
689	每条集测项含：
690	- ID（T001, T002...）
691	- 标题
692	- 覆盖的 feature 列表
693	- 测试类型：真 TCP / fake adapter / Vitest 集成 / manual checklist
694	- 优先级：P0（数据通路核心）/ P1（重要接缝）/ P2（边界情况）
695	- 依赖：需要哪些前置条件
696	- oracle 来源：从 S004 中引用
697	- 对应的质量规则条目（R1-R16）
698	
699	## Lane 判定
700	
701	Lane B：综合分析任务，产出一份文档，单对话可完成。
702	```
703	
704	---
705	
706	## 对话 7+：集测实施
707	
708	**Agent 数**：每轮 9-12 个，按批次
709	
710	### 提示词模板（每轮复用）
711	
712	```
713	## 任务
714	
715	按 S006 集测范围清单实施第 N 批集成测试。
716	
717	## 直接合同
718	
719	- `.sessions/2026-05-19-integration-testing/S006-test-scope-synthesis.md`
720	- 本批覆盖的测试项：{列出 T### 编号}
721	
722	## 边界护栏
723	
724	- `codestable/quality/rewrite-quality-rules.md`
725	- `codestable/architecture/rewrite-target-structure.md`
726	
727	## 实施前检查
728	
729	1. 直接合同已列出
730	2. 覆盖旧系统可观测行为：{从 S004 引用}
731	3. 涉及 feature 归口：{列出}
732	4. 外部只通过 public API：确认
733	5. 涉及 Electron/preload/main：否（Vitest 中用 Node net/dgram）
734	6. 涉及 SCOE/northbound/高速数据：{是/否}
735	7. 验证方式：pnpm build + pnpm lint + pnpm test
736	
737	## 实施规则
738	
739	- TCP 测试用 Node `net` 模块，参考 `connection-network-adapter.spec.ts` 模式
740	- 不引入新依赖，只用 Vitest + Node 内置模块
741	- 测试文件放在 `rewrite/src/__tests__/integration/` 下
742	- 每个测试文件覆盖 1-3 个相关测试项
743	- 测试必须可重复运行，不依赖外部服务
744	
745	## 子 agent 策略
746	
747	{根据本批具体测试项拆分}
748	
749	## 使用 skill
750	
751	cs-feat-impl
752	```
753	
```

> AGENT

对话 4：旧系统可观测行为提取。先检查专题目录和已有文件。

> TOOL

tool_use Bash
id: call_5036979b9c814dcc8587b52f
```json
{
  "command": "ls -la /mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/ 2>/dev/null || echo \"目录不存在\"",
  "description": "Check session directory"
}
```

> TOOL

tool_use Bash
id: call_802c046084d14414bb651a86
```json
{
  "command": "ls /mnt/d/code/frontend/dongfanghong/src/stores/ 2>/dev/null | head -30",
  "description": "List old system stores"
}
```

> TOOL

tool_result
id: call_5036979b9c814dcc8587b52f
```
S001-agent1-s001-s002.md  11.0K
S001-agent10-quality-rules.md  10.6K
S001-agent11-review-checklist.md  11.1K
S001-agent12-h002-tcp.md  8.9K
S001-agent2-s003-s004.md  11.8K
S001-agent3-s005-s014.md  16.3K
S001-agent4-s007.md  12.4K
S001-agent5-s008.md  9.6K
S001-agent6-s009-s010.md  9.4K
S001-agent7-s011-upper.md  6.6K
S001-agent8-s011-lower.md  8.0K
S001-agent9-s012-s015.md  8.1K
S001-historical-extraction.md  14.0K
S002-feature-designs-upper.md  21.7K
conversation-plan.md  31.6K
topic-index.md  5.2K
```

> TOOL

tool_result
id: call_802c046084d14414bb651a86
```
common/
frames/
connectionTargetsStore.ts  8.1K
framesStore.ts  490B
globalStatsStore.ts  6.8K
highSpeedStorageStore.ts  9.2K
historyAnalysis.ts  12.9K
index.ts  874B
netWorkStore.ts  9.2K
scoeStore.ts  10.3K
serialStore.ts  20.9K
settingsStore.ts  586B
statusIndicators.ts  7.0K
```

> TOOL

tool_use Read
id: call_1435611b2e9c4ebdb7895a1b
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/topic-index.md"
}
```

> TOOL

tool_result
id: call_1435611b2e9c4ebdb7895a1b
```
1	# 集成测试体系建立
2	
3	> 状态: active | 时间跨度: 2026-05-19 ~ | 最后更新: 2026-05-19
4	
5	## 目标
6	
7	为 rewrite 系统建立集成测试体系。输入来源：26 天的讨论记录、10+ feature 设计文档、旧系统可观测行为、新系统实际代码。产出：结构化集测清单 + 可执行的端到端测试。
8	
9	## 进展线索
10	
11	- **S001** 历史讨论提取 — 12 个 agent 并行提取完成，合并报告已写入
12	  - 核心发现：835 tests 全部单元级+fake adapter级，零跨 feature 集成测试；十级验证 taxonomy 覆盖 Level 1-3 充分、Level 6-10 零覆盖
13	  - P0 缺口：端到端数据通路（6 条链路无测试）、Selector 不可变性（5 个 feature 浅拷贝）、持久化层（无自动 save + 软删除 bug + 恢复空转）、Composite Adapter（null dereference + 无测试）
14	  - P1 缺口：6 条 Feature 间接缝、6 项 Quality Gate 检查、条件匹配一致性、globalParams 推迟、文档-代码 drift
15	  - 13 项待确认需综合阶段核实
16	- **S002** Feature 设计文档提取 — 从 codestable/features/ 下所有 design.md + checklist.yaml 提取验收标准和跨 feature 交互契约
17	  - 对话 2 完成（上）：9 个 agent 覆盖 frame/connection/receive/send/expression-engine/runtime-wiring/settings/storage-local-baseline/display/status。关键发现：expression engine 最完整（29 条验收+性能已验证）、frame-real 6/6 done、storage 验证全部 pending、routingTick 是核心集成接缝、globalParams 推迟影响全局统计依赖、身份标识统一未完成（display/status 仍在用 groupId/dataItemId）
18	- **S003** 旧系统可观测行为提取 — 从旧代码提取必须保留的可观测行为，作为 oracle 来源
19	- **S004** 新系统接缝审计 — 读 runtime bridges、adapters、composite adapter，识别集成接缝和断裂点
20	- **S005** 集测范围综合 — 合并所有提取结果，按优先级分级，确定真 TCP / fake adapter / manual checklist 边界
21	- **S006** 集测实施 — 按范围写测试
22	
23	## 已确认结论
24	
25	- 54 个 spec 文件全部是单元级 + fake adapter 测试，feature 间接缝零覆盖
26	- H002 已完成 TCP 接线，composite adapter 可用，数据通路物理上已通
27	- connection-network-adapter.spec.ts 已有 Node `net` 模块先例，可在 Vitest 中直接起 TCP
28	
29	## 未决项
30	
31	- S001 13 项待确认需在 S006 综合阶段核实
32	- 集测范围清单尚未产出（S006）
33	- 旧系统哪些可观测行为必须保留尚未逐项确认（S004 对话 4）
34	- 新系统接缝审计尚未执行（S005 对话 5）
35	- 真 TCP 测试在 CI 环境（WSL2 / Windows）的兼容性待验证
36	
37	## 当前位置
38	
39	S001 对话 1 完成（12 agent 并行，4 批 × 3）。S002 对话 2-3 待执行。S003-S006 待后续对话。
40	
41	## 对话规划
42	
43	### 对话 1：历史讨论提取（S001）
44	
45	输入：`.sessions/2026-04-23-rewrite-main-thread/` 下所有 S###.md 和 H###.md
46	
47	子 agent 策略：
48	- Agent 1：读 S001-S005 + S014，提取架构级验收承诺和质量规则中与测试相关的段落
49	- Agent 2：读 S006-S008，提取 feature 实施期的验收结论、known-gaps、测试数量
50	- Agent 3：读 S009-S012，提取 UI 阶段的审计发现、已知 bug、技术债
51	
52	产出格式：每条提取结果含 { 来源 note, feature, 具体行为描述, 验收结论, 已有测试证据, 缺口 }
53	
54	### 对话 2-3：Feature 设计文档提取（S002）
55	
56	输入：`codestable/features/` 下所有 design.md + checklist.yaml + brainstorm.md
57	
58	子 agent 策略（每轮 3 agent，按 feature 分组）：
59	- 对话 2：frame / connection / receive / send / expression-engine
60	- 对话 3：task / command-ingress / storage / settings / display / status
61	
62	产出：每条含 { feature, 验收标准原文, 跨 feature 交互契约, checklist 中测试项, 已实现/未实现 }
63	
64	### 对话 4：旧系统可观测行为提取（S003）
65	
66	输入：`src/` 下旧代码（stores/components/handlers）
67	
68	子 agent 策略：
69	- Agent 1：读旧 receive/send 相关代码，提取数据流行为
70	- Agent 2：读旧 SCOE/task 相关代码，提取命令执行行为
71	- Agent 3：读旧 storage/history/CSV 代码，提取持久化行为
72	
73	产出：每条含 { 旧行为描述, 代码位置, 新系统对应 feature, oracle 来源, 保留/排除 }
74	
75	### 对话 5：新系统接缝审计（S004）
76	
77	输入：`rewrite/src/runtime/` + `rewrite/src/features/*/adapters/` + `rewrite/src/features/*/services/`
78	
79	子 agent 策略：
80	- Agent 1：读所有 bridge 文件，分析数据流向和断裂风险
81	- Agent 2：读 composite-adapter + real-network-adapter + real-serial-adapter，分析 adapter 路由边界
82	- Agent 3：读 persistence.ts + bootstrap，分析启动加载和保存时机
83	
84	产出：接缝清单 + 每个接缝的测试建议
85	
86	### 对话 6：综合 + 排除（S005）
87	
88	合并 S001-S004 所有提取结果，去重、排除已有单测覆盖的项、分级优先级。
89	
90	产出：最终集测范围清单（文件形式，作为 S006 的直接合同）
91	
92	### 对话 7+：集测实施（S006）
93	
94	按 S005 的清单写测试。每轮对话覆盖一批。
95	
96	## 附属文件
97	
98	- `conversation-plan.md` — 7 轮对话完整规划 + 全部提示词
99	- `H001-scope-extraction-handoff.md` — 对话 1 提示词（模板 6 格式，conversation-plan 中已包含完整版）
100	
```

> AGENT

专题目录存在，S001 和 S002 已完成。现在执行对话 4：旧系统可观测行为提取。先确认旧代码关键文件存在。

> TOOL

tool_use Bash
id: call_efc1b61ca2e1417db772012f
```json
{
  "command": "echo \"=== 旧 receive/send ===\" && ls -la /mnt/d/code/frontend/dongfanghong/src/stores/frames/ 2>/dev/null && ls /mnt/d/code/frontend/dongfanghong/src/composables/ 2>/dev/null | head -20 && echo \"=== 旧 SCOE/task ===\" && ls -la /mnt/d/code/frontend/dongfanghong/src/stores/scoeStore.ts 2>/dev/null && echo \"=== 旧连接 ===\" && ls -la /mnt/d/code/frontend/dongfanghong/src/stores/serialStore.ts /mnt/d/code/frontend/dongfanghong/src/stores/netWorkStore.ts 2>/dev/null && echo \"=== 旧网络 handlers ===\" && ls /mnt/d/code/frontend/dongfanghong/src-electron/main/ipc/ 2>/dev/null | head -20",
  "description": "Verify old system files exist"
}
```

> TOOL

tool_use Bash
id: call_efd056f36a7c4ebdb3be9ec2
```json
{
  "command": "echo \"=== 旧表达式 ===\" && find /mnt/d/code/frontend/dongfanghong/src/utils -name \"*expression*\" -o -name \"*Expression*\" 2>/dev/null && echo \"=== 旧帧解析 ===\" && find /mnt/d/code/frontend/dongfanghong/src/utils -name \"*parser*\" -o -name \"*Parser*\" -o -name \"*frame*\" 2>/dev/null | head -10 && echo \"=== 旧历史 ===\" && ls /mnt/d/code/frontend/dongfanghong/src/stores/historyAnalysis.ts 2>/dev/null && echo \"=== 旧帧配置 ===\" && find /mnt/d/code/frontend/dongfanghong/src/stores/frames -name \"*.ts\" 2>/dev/null && echo \"=== 旧路由 ===\" && ls /mnt/d/code/frontend/dongfanghong/src/router/ 2>/dev/null",
  "description": "Verify more old system files"
}
```

> TOOL

tool_result ERROR
id: call_efd056f36a7c4ebdb3be9ec2
```
Exit code 1
=== 旧表达式 ===
```

> TOOL

tool_result
id: call_efc1b61ca2e1417db772012f
```
=== 旧 receive/send ===
dataDisplayStore.ts  33.0K
frameEditorStore.ts  2.7K
frameFieldsStore.ts  9.5K
frameFilterStore.ts  1.2K
frameTemplateStore.ts  3.7K
receiveFramesStore.ts  38.8K
scoeFrameInstancesStore.ts  20.5K
sendFrameInstancesStore.ts  11.4K
sendTasksStore.ts  15.3K
common/
frames/
scoe/
serial/
settings/
window/
README.md  6.1K
index.ts  139B
=== 旧 SCOE/task ===
/mnt/d/code/frontend/dongfanghong/src/stores/scoeStore.ts  10.3K
=== 旧连接 ===
/mnt/d/code/frontend/dongfanghong/src/stores/netWorkStore.ts  9.2K
/mnt/d/code/frontend/dongfanghong/src/stores/serialStore.ts  20.9K
=== 旧网络 handlers ===
dataStorageHandlers.ts  5.1K
fileMetadataHandlers.ts  3.6K
highSpeedStorageHandlers.ts  13.5K
historyDataHandlers.ts  16.5K
index.ts  1.2K
menuHandlers.ts  346B
networkHandlers.ts  21.0K
receiveConfigCache.ts  4.2K
receiveHandlers.ts  7.4K
serialHandlers.ts  17.9K
timerManagerHandlers.ts  12.2K
windowHandlers.ts  582B
```

> TOOL

tool_use Bash
id: call_4572aad55dbd47a4b564fa32
```json
{
  "command": "echo \"=== 旧表达式引擎 ===\" && find /mnt/d/code/frontend/dongfanghong/src -name \"*expression*\" -o -name \"*Expression*\" 2>/dev/null && echo \"=== 旧帧解析 ===\" && find /mnt/d/code/frontend/dongfanghong/src -name \"*frameParser*\" -o -name \"*FrameParser*\" 2>/dev/null && echo \"=== 旧条件 ===\" && find /mnt/d/code/frontend/dongfanghong/src -name \"*condition*\" -o -name \"*Condition*\" -o -name \"*trigger*\" -o -name \"*Trigger*\" 2>/dev/null | head -10 && echo \"=== 旧设置 ===\" && find /mnt/d/code/frontend/dongfanghong/src -name \"*setting*\" -o -name \"*Setting*\" 2>/dev/null | head -10 && echo \"=== 旧路由 ===\" && find /mnt/d/code/frontend/dongfanghong/src/router -name \"*.ts\" -o -name \"*.js\" 2>/dev/null",
  "description": "Search for old system files broadly"
}
```

> TOOL

tool_result ERROR
id: call_4572aad55dbd47a4b564fa32
```
Exit code 1
=== 旧表达式引擎 ===
```

> TOOL

tool_use Glob
id: call_6cf7c428223a44908c26c1e3
```json
{
  "pattern": "src/**/*expression*"
}
```

> TOOL

tool_use Glob
id: call_5553ae7854204f62becf2240
```json
{
  "pattern": "src/**/*Expression*"
}
```

> TOOL

tool_use Glob
id: call_77f43b1d7d654a0291d19172
```json
{
  "pattern": "src/router/**/*"
}
```

> TOOL

tool_result
id: call_5553ae7854204f62becf2240
```
src/composables/frames/useFrameExpressionManager.ts
src/composables/frames/useExpressionCalculator.ts
```

> TOOL

tool_result
id: call_6cf7c428223a44908c26c1e3
```
No files found
```

> TOOL

tool_result
id: call_77f43b1d7d654a0291d19172
```
src/router/index.ts
src/router/routes.ts
```

> TOOL

tool_use Glob
id: call_a4b7c71fac3a4682896632ef
```json
{
  "pattern": "src/components/frames/FrameSend/**/*.vue"
}
```

> TOOL

tool_use Glob
id: call_25211ebd6ee8430fb9cccf81
```json
{
  "pattern": "src/stores/frames/*.ts"
}
```

> TOOL

tool_result
id: call_25211ebd6ee8430fb9cccf81
```
src/stores/frames/frameEditorStore.ts
src/stores/frames/frameFieldsStore.ts
src/stores/frames/sendFrameInstancesStore.ts
src/stores/frames/frameFilterStore.ts
src/stores/frames/dataDisplayStore.ts
src/stores/frames/sendTasksStore.ts
src/stores/frames/frameTemplateStore.ts
src/stores/frames/scoeFrameInstancesStore.ts
src/stores/frames/receiveFramesStore.ts
```

> TOOL

tool_result
id: call_a4b7c71fac3a4682896632ef
```
src/components/frames/FrameSend/EnhancedSequentialSend/TaskStatusPanel.vue
src/components/frames/FrameSend/TriggerSend/ConditionTriggerPanel.vue
src/components/frames/FrameSend/TriggerSend/TimeTriggerPanel.vue
src/components/frames/FrameSend/TriggerSend/TriggerConditionList.vue
src/components/frames/FrameSend/TriggerSend/TriggerConfigPanel.vue
src/components/frames/FrameSend/TriggerSend/TriggerTypeSelector.vue
src/components/frames/FrameSend/EnhancedSequentialSend/StrategySelector.vue
src/components/frames/FrameSend/TimedSend/TimedConfigPanel.vue
src/components/frames/FrameSend/TimedSend/TimedConfigDialog.vue
src/components/frames/FrameSend/TriggerSend/TriggerConfigDialog.vue
src/components/frames/FrameSend/FrameInstanceList.vue
src/components/frames/FrameSend/FrameInstanceEditor.vue
src/components/frames/FrameSend/FrameFormatList.vue
src/components/frames/FrameSend/FramePreview.vue
src/components/frames/FrameSend/SendTargetSelector.vue
src/components/frames/FrameSend/EnhancedSequentialSend/InstanceSequenceTable.vue
src/components/frames/FrameSend/TimedSend/TimedSendDialog.vue
src/components/frames/FrameSend/EnhancedSequentialSend/EnhancedSequentialSendDialog.vue
src/components/frames/FrameSend/ActiveTasksMonitor.vue
src/components/frames/FrameSend/TriggerSend/TriggerSendDialog.vue
```

> AGENT

旧代码结构确认完毕。开始执行对话 4：3 批 × 3 个 agent 并行提取旧系统可观测行为。

> TOOL

tool_use TaskCreate
id: call_d61d0e9328e64d2d9d2165c3
```json
{
  "subject": "批次 1：旧 receive/send + SCOE/task + 连接管理 提取",
  "description": "Agent 1-3 并行提取旧 receive/send 数据流、SCOE/task 执行、连接管理的可观测行为",
  "activeForm": "提取批次 1（旧数据流/SCOE/连接）"
}
```

> TOOL

tool_use TaskCreate
id: call_d82fb494ba144b11869ef4fb
```json
{
  "subject": "批次 2：旧表达式/解析 + 存储/历史 + 帧定义 提取",
  "description": "Agent 4-6 并行提取旧表达式引擎、存储/历史/CSV、帧定义管理的可观测行为",
  "activeForm": "提取批次 2（旧表达式/存储/帧定义）"
}
```

> TOOL

tool_use TaskCreate
id: call_0cf5d5a800ec42beacfb803c
```json
{
  "subject": "批次 3：旧状态展示 + 设置/配置 + 页面入口 提取",
  "description": "Agent 7-9 并行提取旧状态展示、设置/配置、页面入口的可观测行为",
  "activeForm": "提取批次 3（旧状态/设置/页面）"
}
```

> TOOL

tool_use TaskCreate
id: call_4d4b6d3370c6456ea1acfac6
```json
{
  "subject": "综合 9 个 agent 结果写入 S004-legacy-observable-behaviors.md",
  "description": "合并 9 个 agent 的产出，去重整理，写入最终报告",
  "activeForm": "综合写入最终报告"
}
```

> TOOL

tool_result
id: call_4d4b6d3370c6456ea1acfac6
```
Task #1 created successfully: 综合 9 个 agent 结果写入 S004-legacy-observable-behaviors.md
```

> TOOL

tool_result
id: call_0cf5d5a800ec42beacfb803c
```
Task #2 created successfully: 批次 3：旧状态展示 + 设置/配置 + 页面入口 提取
```

> TOOL

tool_result
id: call_d82fb494ba144b11869ef4fb
```
Task #3 created successfully: 批次 2：旧表达式/解析 + 存储/历史 + 帧定义 提取
```

> TOOL

tool_result
id: call_d61d0e9328e64d2d9d2165c3
```
Task #4 created successfully: 批次 1：旧 receive/send + SCOE/task + 连接管理 提取
```

> TOOL

tool_use TaskUpdate
id: call_89160e2521764366b4b0321c
```json
{
  "taskId": "3",
  "addBlockedBy": [
    "4"
  ]
}
```

> TOOL

tool_use TaskUpdate
id: call_80ba0f340c0a44f195698ece
```json
{
  "taskId": "2",
  "addBlockedBy": [
    "3"
  ]
}
```

> TOOL

tool_use TaskUpdate
id: call_d2788df4eb2a4379846fbd7a
```json
{
  "taskId": "1",
  "addBlockedBy": [
    "2"
  ]
}
```

> TOOL

tool_result
id: call_d2788df4eb2a4379846fbd7a
```
Updated task #1 blockedBy
```

> TOOL

tool_result
id: call_89160e2521764366b4b0321c
```
Updated task #3 blockedBy
```

> TOOL

tool_result
id: call_80ba0f340c0a44f195698ece
```
Updated task #2 blockedBy
```

> TOOL

tool_use TaskUpdate
id: call_4a0d4f9f4eb84c8bbed393d1
```json
{
  "status": "in_progress",
  "taskId": "4"
}
```

> TOOL

tool_result
id: call_4a0d4f9f4eb84c8bbed393d1
```
Updated task #4 status
```

> AGENT

启动批次 1（3 agent 并行）。

> TOOL

tool_use Agent
id: call_5442d2e6dcd942cdb297a0bb
```json
{
  "description": "Agent1: 旧 receive/send 数据流",
  "prompt": "## 任务\n\n调研旧系统的 receive 和 send 数据流，提取所有必须保留的可观测业务行为。只做事实提取，不做设计或实施。\n\n## 需要读的文件\n\n1. `src/stores/frames/receiveFramesStore.ts` — 旧 receive 数据流（38.8K，重点看数据流入、解析、统计、触发逻辑）\n2. `src/stores/frames/sendFrameInstancesStore.ts` — 旧 send 帧实例管理\n3. `src/stores/frames/sendTasksStore.ts` — 旧 send 任务管理（15.3K）\n4. `src/composables/frames/` 目录下与 send 相关的文件（查找 useUnifiedSender 或类似文件）\n\n## 需要回答的问题\n\n1. 旧 receive 的完整数据流路径（从串口/网络收到字节 → 解析 → 展示 → 触发）？每一步调用了什么函数、触发了什么事件？\n2. 旧 send 的完整流程（从用户点击 → 构帧 → 发送 → 结果）？\n3. receiveFramesStore 承载了哪些职责？列出所有 action/computed/watcher\n4. sendTasksStore 中定时发送和触发发送的具体流程？\n5. receive 中的数据统计（帧计数、字节计数、错误计数）的具体行为？\n6. receive 中的条件触发（满足条件后触发 send）的具体逻辑？\n7. 这些行为的 oracle 来源（可以录制的输入输出样本）？\n\n## 汇报格式\n\n中文，facts-first。每条行为：\n- 旧行为描述\n- 代码位置（文件:行号 或文件:函数名）\n- 行为在新系统中的对应 feature（如知道的话）\n- oracle 来源评估（代码位置/配置文件样本/可录制）\n- 保留/排除建议\n\n将结果写入 `/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-agent1-receive-send.md`",
  "run_in_background": true
}
```

> TOOL

tool_use Agent
id: call_a1b5e0cb97cd40c3ad4e5d43
```json
{
  "description": "Agent2: 旧 SCOE/task 执行",
  "prompt": "## 任务\n\n调研旧系统的 SCOE 命令处理和任务执行行为，提取所有必须保留的可观测业务行为。只做事实提取，不做设计或实施。\n\n## 需要读的文件\n\n1. `src/stores/scoeStore.ts` — SCOE 配置+状态+连接+发送+测试工具（10.3K）\n2. `src/stores/frames/scoeFrameInstancesStore.ts` — SCOE 帧实例（20.5K）\n3. `src/components/frames/FrameSend/TimedSend/TimedSendDialog.vue` — 定时发送\n4. `src/components/frames/FrameSend/TriggerSend/TriggerSendDialog.vue` — 触发发送\n5. `src/components/frames/FrameSend/EnhancedSequentialSend/EnhancedSequentialSendDialog.vue` — 增强顺序发送\n6. `src/components/frames/FrameSend/ActiveTasksMonitor.vue` — 活跃任务监控\n\n## 需要回答的问题\n\n1. 旧 SCOE 的完整命令处理流程（接收 → 解析 → 执行 → 确认）？两阶段状态机的具体逻辑？\n2. 旧定时发送的完整流程？定时器的创建/暂停/恢复/停止行为？\n3. 旧触发发送的条件判断逻辑？条件类型和组合方式？\n4. 旧顺序发送的步骤执行逻辑？步骤间的等待和条件判断？\n5. SCOE 测试工具的录制/回放行为？\n6. 活跃任务监控展示了什么信息？如何更新？\n7. 这些行为的 oracle 来源？\n\n## 汇报格式\n\n中文，facts-first。每条行为：\n- 旧行为描述\n- 代码位置（文件:行号 或文件:函数名）\n- 行为在新系统中的对应 feature（如知道的话）\n- oracle 来源评估\n- 保留/排除建议\n\n将结果写入 `/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-agent2-scoe-task.md`",
  "run_in_background": true
}
```

> TOOL

tool_use Agent
id: call_c6550b8e4ca04266a378b716
```json
{
  "description": "Agent3: 旧连接管理",
  "prompt": "## 任务\n\n调研旧系统的连接管理行为，提取所有必须保留的可观测业务行为。只做事实提取，不做设计或实施。\n\n## 需要读的文件\n\n1. `src/stores/serialStore.ts` — 串口连接生命周期（20.9K）\n2. `src/stores/netWorkStore.ts` — 网络连接生命周期（9.2K）\n3. `src-electron/main/ipc/networkHandlers.ts` — main 进程网络处理（21.0K）\n4. `src-electron/main/ipc/serialHandlers.ts` — main 进程串口处理（17.9K）\n5. `src/stores/connectionTargetsStore.ts` — 连接目标管理（8.1K）\n\n## 需要回答的问题\n\n1. 旧串口连接的完整生命周期（打开 → 配置 → 收发 → 断开 → 重连）？每个状态转换的触发条件和 UI 表现？\n2. 旧 TCP/UDP 连接的完整生命周期？TCP server/client 模式的差异？UDP 的特殊性？\n3. 旧网络接收中的高速存储分流逻辑？\n4. 连接状态在 UI 上的展示行为？状态指示器更新频率？\n5. 多连接并发管理？连接切换行为？\n6. 连接配置的 CRUD 行为？\n7. 自动连接/自动重连的行为？\n8. 这些行为的 oracle 来源？\n\n## 汇报格式\n\n中文，facts-first。每条行为：\n- 旧行为描述\n- 代码位置（文件:行号 或文件:函数名）\n- 行为在新系统中的对应 feature（如知道的话）\n- oracle 来源评估\n- 保留/排除建议\n\n将结果写入 `/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-agent3-connection.md`",
  "run_in_background": true
}
```

> TOOL

tool_result
id: call_5442d2e6dcd942cdb297a0bb
```
Async agent launched successfully.
agentId: a2260d32850f85677 (internal ID - do not mention to user. Use SendMessage with to: 'a2260d32850f85677' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using. Work on non-overlapping tasks, or briefly tell the user what you launched and end your response.
output_file: /tmp/claude-1000/-mnt-d-code-frontend-dongfanghong/abd57e07-acd4-4a3b-9c1f-1941fce2a5ab/tasks/a2260d32850f85677.output
Do NOT Read or Bash tail this file — it is the full sub-agent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> TOOL

tool_result
id: call_a1b5e0cb97cd40c3ad4e5d43
```
Async agent launched successfully.
agentId: a8a527877baf72e21 (internal ID - do not mention to user. Use SendMessage with to: 'a8a527877baf72e21' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using. Work on non-overlapping tasks, or briefly tell the user what you launched and end your response.
output_file: /tmp/claude-1000/-mnt-d-code-frontend-dongfanghong/abd57e07-acd4-4a3b-9c1f-1941fce2a5ab/tasks/a8a527877baf72e21.output
Do NOT Read or Bash tail this file — it is the full sub-agent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> TOOL

tool_result
id: call_c6550b8e4ca04266a378b716
```
Async agent launched successfully.
agentId: a8c1d3c068102ccce (internal ID - do not mention to user. Use SendMessage with to: 'a8c1d3c068102ccce' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using. Work on non-overlapping tasks, or briefly tell the user what you launched and end your response.
output_file: /tmp/claude-1000/-mnt-d-code-frontend-dongfanghong/abd57e07-acd4-4a3b-9c1f-1941fce2a5ab/tasks/a8c1d3c068102ccce.output
Do NOT Read or Bash tail this file — it is the full sub-agent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> AGENT

批次 1 已启动（3 个 agent 并行）：
- Agent 1：旧 receive/send 数据流
- Agent 2：旧 SCOE/task 执行
- Agent 3：旧连接管理

等待批次 1 完成后启动批次 2。

> AGENT

Agent 2（SCOE/task）完成，提取了 34 条可观测行为。等待 Agent 1 和 Agent 3 完成。

> AGENT

Agent 3（连接管理）完成，提取了 13 项保留行为 + 6 项排除 + 7 项需重新设计。还在等 Agent 1（receive/send）。

> AGENT

批次 1 全部完成。标记完成，启动批次 2。

> TOOL

tool_use TaskUpdate
id: call_26add7591e454dba8529db9b
```json
{
  "status": "completed",
  "taskId": "4"
}
```

> TOOL

tool_use TaskUpdate
id: call_cf0e123ce4d0495f9bff1e27
```json
{
  "status": "in_progress",
  "taskId": "3"
}
```

> TOOL

tool_result
id: call_26add7591e454dba8529db9b
```
Updated task #4 status
```

> TOOL

tool_result
id: call_cf0e123ce4d0495f9bff1e27
```
Updated task #3 status
```

> TOOL

tool_use Agent
id: call_a823e0c1a88646fc8c4a9a22
```json
{
  "description": "Agent4: 旧表达式/解析",
  "prompt": "## 任务\n\n调研旧系统的表达式引擎和帧解析行为，提取所有必须保留的可观测业务行为。只做事实提取，不做设计或实施。\n\n## 需要读的文件\n\n1. `src/composables/frames/useExpressionCalculator.ts` — 旧表达式计算\n2. `src/composables/frames/useFrameExpressionManager.ts` — 旧表达式管理\n3. 在 `src/` 下搜索表达式求值相关代码（grep \"evaluateExpression\" 或 \"expressionEngine\" 或 \"calcExpression\"）\n4. 在 `src/` 下搜索帧解析相关代码（grep \"frameParser\" 或 \"parseFrame\" 或 \"frameToBuffer\" 或 \"bufferToFrame\" 或 \"parseField\"）\n5. 在 `src/` 下搜索条件判断相关代码（grep \"conditionMatch\" 或 \"matchCondition\" 或 \"checkCondition\" 或 \"evaluateCondition\"）\n\n## 需要回答的问题\n\n1. 旧表达式引擎的核心行为？\n   - 支持哪些运算符和函数？\n   - 变量如何解析？（依赖排序？缓存？）\n   - 表达式何时计算？（收到数据时？定时？）\n   - 循环依赖如何处理？\n   - 错误处理？（除零、类型不匹配、引用不存在字段）\n2. 旧帧解析的核心行为？\n   - 字节到字段的解析流程？\n   - applyFactor（倍率/偏移）的具体行为？\n   - 11 种数据类型的解析规则？\n   - 字段字节序（大端/小端）处理？\n   - CRC/校验和计算？\n3. 旧条件判断的核心行为？\n   - AND/OR 组合逻辑？\n   - 支持的比较运算符？\n   - 条件触发的评估时机？\n   - 短路求值？\n4. 有哪些旧配置文件样本可以作为 oracle？\n\n## 汇报格式\n\n中文，facts-first。每条行为：\n- 旧行为描述\n- 代码位置（文件:行号 或文件:函数名）\n- 行为在新系统中的对应 feature（如知道的话）\n- oracle 来源评估\n- 保留/排除建议\n\n将结果写入 `/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-agent4-expression-parser.md`",
  "run_in_background": true
}
```

> TOOL

tool_use Agent
id: call_8705a5653eab487993bd23a1
```json
{
  "description": "Agent5: 旧存储/历史/CSV",
  "prompt": "## 任务\n\n调研旧系统的数据存储、历史记录和 CSV 导出行为，提取所有必须保留的可观测业务行为。只做事实提取，不做设计或实施。\n\n## 需要读的文件\n\n1. `src/stores/frames/dataDisplayStore.ts` — 数据展示/存储（33K，最大的 store）\n2. `src/stores/historyAnalysis.ts` — 历史数据分析（12.9K）\n3. `src/stores/globalStatsStore.ts` — 全局统计（6.8K）\n4. `src/stores/highSpeedStorageStore.ts` — 高速存储（9.2K）\n5. `src-electron/main/ipc/historyDataHandlers.ts` — 历史数据 IPC 处理（16.5K）\n6. `src-electron/main/ipc/dataStorageHandlers.ts` — 数据存储 IPC（5.1K）\n7. `src-electron/main/ipc/highSpeedStorageHandlers.ts` — 高速存储 IPC（13.5K）\n8. 搜索 CSV 相关代码：grep \"csv\" 或 \"CSV\" 或 \"export\" 或 \"import\" 在 src/ 目录\n\n## 需要回答的问题\n\n1. 旧历史数据的存储行为？\n   - 数据如何存储？（SQLite？文件？内存？）\n   - 查询行为？（按时间范围、按帧类型、按字段？）\n   - 数据保留策略？（自动清理？手动清理？）\n2. 旧 CSV 导出的行为？\n   - 导出哪些数据？（原始字节？解析后字段值？统计？）\n   - CSV 格式？（列名、分隔符、编码？）\n   - 导出触发方式？\n3. 旧数据导入的行为？\n   - 支持什么格式的导入？\n   - 导入后的数据如何使用？\n4. 高速存储的具体行为？\n   - 什么条件触发高速存储？\n   - 文件格式和轮转策略？\n   - 读取和回放行为？\n5. 全局统计的具体行为？\n   - 统计哪些指标？\n   - 统计更新频率？\n   - 统计重置行为？\n6. 数据展示的查询行为？\n   - 实时数据如何展示？\n   - 历史数据如何回放？\n   - 数据过滤和排序？\n\n## 汇报格式\n\n中文，facts-first。每条行为：\n- 旧行为描述\n- 代码位置（文件:行号 或文件:函数名）\n- 行为在新系统中的对应 feature（如知道的话）\n- oracle 来源评估\n- 保留/排除建议\n\n将结果写入 `/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-agent5-storage-history-csv.md`",
  "run_in_background": true
}
```

> TOOL

tool_use Agent
id: call_7b6d56822846494094251a61
```json
{
  "description": "Agent6: 旧帧定义管理",
  "prompt": "## 任务\n\n调研旧系统的帧定义管理行为，提取所有必须保留的可观测业务行为。只做事实提取，不做设计或实施。\n\n## 需要读的文件\n\n1. `src/stores/frames/frameEditorStore.ts` — 帧编辑器（2.7K）\n2. `src/stores/frames/frameFieldsStore.ts` — 帧字段管理（9.5K）\n3. `src/stores/frames/frameFilterStore.ts` — 帧过滤（1.2K）\n4. `src/stores/frames/frameTemplateStore.ts` — 帧模板（3.7K）\n5. `src/stores/framesStore.ts` — 顶层帧 store（490B）\n6. 搜索帧导入/导出代码：grep \"importFrame\" 或 \"exportFrame\" 或 \"importJson\" 或 \"exportJson\" 在 src/ 目录\n7. 搜索帧配置相关：grep \"frameConfig\" 或 \"frameTemplate\" 或 \"frameDefinition\" 在 src/ 目录\n\n## 需要回答的问题\n\n1. 旧帧定义的 CRUD 行为？\n   - 创建：新帧的默认值？必填字段？\n   - 读取：帧列表如何加载和缓存？\n   - 更新：哪些字段可编辑？编辑后的即时生效机制？\n   - 删除：删除确认？级联删除？\n2. 旧帧实例的管理行为？\n   - sendFrameInstancesStore 和 scoeFrameInstancesStore 的区别？\n   - 实例参数如何覆盖帧定义？\n   - 实例的 CRUD 行为？\n3. 旧帧导入/导出的行为？\n   - 支持的格式？（JSON？CSV？）\n   - 导出内容？（定义？实例？配置？）\n   - 导入时的合并/覆盖策略？\n   - 校验行为？\n4. 旧帧字段管理的行为？\n   - 字段类型支持？（11种数据类型的具体配置）\n   - 字段排列顺序？\n   - 字段分组？\n5. 旧 JSON 格式与新格式的差异？\n   - 结构差异\n   - 字段命名差异\n   - 数据类型差异\n6. 帧模板的使用行为？\n   - 模板创建和管理？\n   - 基于模板创建帧？\n   - 模板库？\n\n## 汇报格式\n\n中文，facts-first。每条行为：\n- 旧行为描述\n- 代码位置（文件:行号 或文件:函数名）\n- 行为在新系统中的对应 feature（如知道的话）\n- oracle 来源评估\n- 保留/排除建议\n\n将结果写入 `/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-agent6-frame-definition.md`",
  "run_in_background": true
}
```

> TOOL

tool_result
id: call_a823e0c1a88646fc8c4a9a22
```
Async agent launched successfully.
agentId: a86f7610a7d474da1 (internal ID - do not mention to user. Use SendMessage with to: 'a86f7610a7d474da1' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using. Work on non-overlapping tasks, or briefly tell the user what you launched and end your response.
output_file: /tmp/claude-1000/-mnt-d-code-frontend-dongfanghong/abd57e07-acd4-4a3b-9c1f-1941fce2a5ab/tasks/a86f7610a7d474da1.output
Do NOT Read or Bash tail this file — it is the full sub-agent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> TOOL

tool_result
id: call_8705a5653eab487993bd23a1
```
Async agent launched successfully.
agentId: a03afd1ce5619d867 (internal ID - do not mention to user. Use SendMessage with to: 'a03afd1ce5619d867' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using. Work on non-overlapping tasks, or briefly tell the user what you launched and end your response.
output_file: /tmp/claude-1000/-mnt-d-code-frontend-dongfanghong/abd57e07-acd4-4a3b-9c1f-1941fce2a5ab/tasks/a03afd1ce5619d867.output
Do NOT Read or Bash tail this file — it is the full sub-agent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> TOOL

tool_result
id: call_7b6d56822846494094251a61
```
Async agent launched successfully.
agentId: afd5d43bbb729d4e6 (internal ID - do not mention to user. Use SendMessage with to: 'afd5d43bbb729d4e6' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using. Work on non-overlapping tasks, or briefly tell the user what you launched and end your response.
output_file: /tmp/claude-1000/-mnt-d-code-frontend-dongfanghong/abd57e07-acd4-4a3b-9c1f-1941fce2a5ab/tasks/afd5d43bbb729d4e6.output
Do NOT Read or Bash tail this file — it is the full sub-agent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> AGENT

批次 2 已启动（3 个 agent 并行）：
- Agent 4：旧表达式引擎/帧解析/条件判断
- Agent 5：旧存储/历史/CSV/高速存储
- Agent 6：旧帧定义管理/导入导出

等待完成。

> AGENT

Agent 5（存储/历史/CSV）完成，27 条行为，保留 25 条。等待 Agent 4 和 Agent 6。

> AGENT

Agent 4（表达式/解析）完成，19 条保留 + 8 条排除。等待 Agent 6（帧定义管理）。

> AGENT

批次 2 全部完成。标记完成，启动批次 3。

> TOOL

tool_use TaskUpdate
id: call_d3fa6dda5fb94e8387fbddb3
```json
{
  "status": "completed",
  "taskId": "3"
}
```

> TOOL

tool_use TaskUpdate
id: call_d283132b1a1f494faf939e94
```json
{
  "status": "in_progress",
  "taskId": "2"
}
```

> TOOL

tool_result
id: call_d283132b1a1f494faf939e94
```
Updated task #2 status
```

> TOOL

tool_result
id: call_d3fa6dda5fb94e8387fbddb3
```
Updated task #3 status
```

> TOOL

tool_use Agent
id: call_be83e2b3a136404a907ccbf5
```json
{
  "description": "Agent7: 旧状态展示",
  "prompt": "## 任务\n\n调研旧系统的状态指示、健康检查和统计展示行为，提取所有必须保留的可观测业务行为。只做事实提取，不做设计或实施。\n\n## 需要读的文件\n\n1. `src/stores/statusIndicators.ts` — 状态指示器（7.6K 估算）\n2. `src/stores/globalStatsStore.ts` — 全局统计（6.8K）\n3. 搜索旧状态指示组件：在 `src/components/` 下搜索 \"status\" 或 \"indicator\" 或 \"StatusIndicator\"\n4. 搜索健康检查相关：在 `src/` 下搜索 \"healthCheck\" 或 \"heartbeat\" 或 \"alive\"\n5. 搜索统计展示相关：在 `src/components/` 下搜索 \"stats\" 或 \"statistics\" 或 \"counter\"\n\n## 需要回答的问题\n\n1. 旧连接状态指示的具体展示行为？\n   - 有哪些状态？（已连接、已断开、连接中、错误？）\n   - 状态更新频率？\n   - 多连接状态如何展示？\n2. 旧健康检查的行为？\n   - 是否有心跳机制？\n   - 超时检测？\n   - 自动恢复？\n3. 旧统计展示的行为？\n   - 实时统计（帧计数、字节计数、错误率）？\n   - 统计面板位置和更新频率？\n   - 统计重置行为？\n\n## 汇报格式\n\n中文，facts-first。每条行为：\n- 旧行为描述\n- 代码位置（文件:行号 或文件:函数名）\n- 行为在新系统中的对应 feature（如知道的话）\n- oracle 来源评估\n- 保留/排除建议\n\n将结果写入 `/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-agent7-status-indicators.md`",
  "run_in_background": true
}
```

> TOOL

tool_use Agent
id: call_602f74c37f154809a9a759b6
```json
{
  "description": "Agent8: 旧设置/配置",
  "prompt": "## 任务\n\n调研旧系统的设置和配置管理行为，提取所有必须保留的可观测业务行为。只做事实提取，不做设计或实施。\n\n## 需要读的文件\n\n1. `src/stores/settingsStore.ts` — 顶层设置 store（586B）\n2. `src/stores/frames/frameFilterStore.ts` — 帧过滤器配置（1.2K）\n3. 搜索设置相关 store：在 `src/stores/` 下搜索 \"setting\" 或 \"config\" 或 \"preference\"\n4. 搜索 `src/composables/settings/` 目录\n5. 搜索旧配置文件默认值：在 `src/` 下搜索 \"defaultConfig\" 或 \"initialConfig\" 或 \"defaultSettings\"\n6. 搜索旧系统参数配置：grep \"globalParams\" 或 \"systemParams\" 或 \"deviceParams\" 在 src/ 目录\n\n## 需要回答的问题\n\n1. 旧系统的配置项完整清单？\n   - 应用级配置？（主题、语言、窗口布局？）\n   - 功能级配置？（接收配置、发送配置、连接配置？）\n   - 每个配置项的类型、默认值、范围？\n2. 每个配置项在新系统中的对应？\n   - 哪些配置项在新系统中已有对应？\n   - 哪些配置项在新系统中缺失？\n   - 哪些配置项不再需要？\n3. 配置持久化的旧行为？\n   - 存储位置？（localStorage？文件？）\n   - 保存时机？（实时？退出时？）\n   - 加载时机？（启动时？首次访问？）\n   - 配置恢复/重置行为？\n\n## 汇报格式\n\n中文，facts-first。每条行为：\n- 旧行为描述\n- 代码位置（文件:行号 或文件:函数名）\n- 行为在新系统中的对应 feature（如知道的话）\n- oracle 来源评估\n- 保留/排除建议\n\n将结果写入 `/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-agent8-settings-config.md`",
  "run_in_background": true
}
```

> TOOL

tool_use Agent
id: call_133113a60fd345fb8d8be377
```json
{
  "description": "Agent9: 旧系统页面入口",
  "prompt": "## 任务\n\n调研旧系统的所有页面入口和路由，提取完整的页面结构清单，标注每个入口在新系统中的对应。只做事实提取，不做设计或实施。\n\n## 需要读的文件\n\n1. `src/router/routes.ts` — 路由定义\n2. `src/router/index.ts` — 路由入口\n3. 搜索侧边栏/导航组件：在 `src/components/` 下搜索 \"sidebar\" 或 \"navigation\" 或 \"menu\" 或 \"drawer\"\n4. 搜索布局组件：`src/layouts/` 目录\n5. 搜索旧系统主入口：`src/App.vue`\n\n## 需要回答的问题\n\n1. 旧系统所有页面入口和路由？\n   - 每个路由的 path、name、component、meta？\n   - 嵌套路由结构？\n   - 动态路由参数？\n2. 旧系统的导航结构？\n   - 侧边栏菜单项？\n   - 页面切换方式？\n   - Tab/子页面切换？\n3. 每个入口在新系统中的对应路由？\n   - 列出旧路由 → 新路由映射\n   - 是否有旧功能在新系统中缺失？\n   - 是否有新系统新增的页面？\n4. 旧系统的布局结构？\n   - 主布局？\n   - 全屏模式？\n   - 对话框/弹窗页面？\n\n## 汇报格式\n\n中文，facts-first。格式：\n- 旧路由完整列表（path、name、功能描述）\n- 旧导航结构\n- 新旧路由映射表\n- 缺失项列表\n- 保留/排除建议\n\n将结果写入 `/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-agent9-routes-pages.md`",
  "run_in_background": true
}
```

> TOOL

tool_result
id: call_be83e2b3a136404a907ccbf5
```
Async agent launched successfully.
agentId: a98dc2dd79ce11965 (internal ID - do not mention to user. Use SendMessage with to: 'a98dc2dd79ce11965' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using. Work on non-overlapping tasks, or briefly tell the user what you launched and end your response.
output_file: /tmp/claude-1000/-mnt-d-code-frontend-dongfanghong/abd57e07-acd4-4a3b-9c1f-1941fce2a5ab/tasks/a98dc2dd79ce11965.output
Do NOT Read or Bash tail this file — it is the full sub-agent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> TOOL

tool_result
id: call_602f74c37f154809a9a759b6
```
Async agent launched successfully.
agentId: afd5decc193afcf0c (internal ID - do not mention to user. Use SendMessage with to: 'afd5decc193afcf0c' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using. Work on non-overlapping tasks, or briefly tell the user what you launched and end your response.
output_file: /tmp/claude-1000/-mnt-d-code-frontend-dongfanghong/abd57e07-acd4-4a3b-9c1f-1941fce2a5ab/tasks/afd5decc193afcf0c.output
Do NOT Read or Bash tail this file — it is the full sub-agent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> TOOL

tool_result
id: call_133113a60fd345fb8d8be377
```
Async agent launched successfully.
agentId: a81a377a137885859 (internal ID - do not mention to user. Use SendMessage with to: 'a81a377a137885859' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes.
Do not duplicate this agent's work — avoid working with the same files or topics it is using. Work on non-overlapping tasks, or briefly tell the user what you launched and end your response.
output_file: /tmp/claude-1000/-mnt-d-code-frontend-dongfanghong/abd57e07-acd4-4a3b-9c1f-1941fce2a5ab/tasks/a81a377a137885859.output
Do NOT Read or Bash tail this file — it is the full sub-agent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> AGENT

批次 3 已启动（3 个 agent 并行）：
- Agent 7：旧状态指示/健康检查/统计展示
- Agent 8：旧设置/配置管理
- Agent 9：旧系统页面入口/路由

等待完成。

> AGENT

Agent 9（页面入口）完成。发现 3 个旧页面在新系统缺失：存储管理、历史分析、系统设置。等待 Agent 7 和 Agent 8。

> AGENT

Agent 7（状态展示）完成，27 条行为，保留 26 条。等待最后一个 Agent 8（设置/配置）。

> AGENT

全部 9 个 agent 完成。标记批次 3 完成，开始综合。

> TOOL

tool_use TaskUpdate
id: call_2bc995bc68c44ec084e0886d
```json
{
  "status": "completed",
  "taskId": "2"
}
```

> TOOL

tool_use TaskUpdate
id: call_0eb4a466f3c5458d960e1431
```json
{
  "status": "in_progress",
  "taskId": "1"
}
```

> TOOL

tool_result
id: call_2bc995bc68c44ec084e0886d
```
Updated task #2 status
```

> TOOL

tool_result
id: call_0eb4a466f3c5458d960e1431
```
Updated task #1 status
```

> AGENT

读取所有 agent 产出文件进行综合。

> TOOL

tool_use Read
id: call_c3c07c5a793b40b79b3aeefc
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-agent1-receive-send.md"
}
```

> TOOL

tool_use Read
id: call_0752576afcf44bc696e16952
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-agent2-scoe-task.md"
}
```

> TOOL

tool_use Read
id: call_482e6562da634514a89ac7ea
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-agent3-connection.md"
}
```

> TOOL

tool_result
id: call_0752576afcf44bc696e16952
```
1	# [S004] 旧系统 SCOE 命令处理与任务执行可观测行为提取
2	
3	> 2026-05-19 | 调研 | 进行中
4	
5	## 目标
6	
7	调研旧系统的 SCOE 命令处理和任务执行行为，提取所有必须保留的可观测业务行为。只做事实提取，不做设计或实施。
8	
9	## 记录
10	
11	### 一、SCOE 命令处理流程
12	
13	#### 行为 1：SCOE 状态轮询（1 秒定时器）
14	
15	- **旧行为描述**：SCOE 系统启动后注册一个 1 秒间隔的常开定时器 `SCOE_UPDATE_STATUS`，每秒调用 `updateStatus()`。`updateStatus()` 做三件事：(1) 递增 `runtimeSeconds`；(2) 重置 `receiveCommandSuccess = false`；(3) 若 `scoeFramesLoaded` 为 true 则递增 `satelliteIdRuntimeSeconds`，否则清零所有指令统计。
16	- **代码位置**：`scoeStore.ts:293-311`（`updateStatus`）、`scoeStore.ts:322-341`（定时器注册）
17	- **新系统对应 feature**：SCOE 归入"指令接入"feature，状态轮询属 runtim 层
18	- **oracle 来源评估**：代码实现即 oracle。定时器常开 + 每秒 tick 是明确的可观测行为
19	- **保留/排除建议**：保留。1 秒状态 tick 是 SCOE 与外部系统交互的节奏基础
20	
21	#### 行为 2：卫星加载状态管理
22	
23	- **旧行为描述**：每秒 `updateStatus()` 中调用 `checkSatelliteLoad()`。若 `scoeFramesLoaded = true` 且 UDP 未连接，则自动建立 UDP 连接（连接参数来自 `globalConfig.udpIpAddress/udpPort` + `selectedConfig.sendConfig.udpIpAddress/udpPort` 作为 remoteHosts）。若 `scoeFramesLoaded = false` 且 UDP 已连接，则断开 UDP 并清空 `loadedSatelliteId`。
24	- **代码位置**：`scoeStore.ts:216-247`（`checkSatelliteLoad`）
25	- **新系统对应 feature**：指令接入 feature 的连接生命周期
26	- **oracle 来源评估**：代码即 oracle。UDP 连接与卫星加载状态耦合是关键行为
27	- **保留/排除建议**：保留。SCOE 帧加载/卸载与 UDP 连接的联动是核心业务行为
28	
29	#### 行为 3：每秒自动发送所有 SCOE 帧
30	
31	- **旧行为描述**：每秒 `updateStatus()` 中调用 `sendScoeFrames()`。若 UDP 已连接，遍历 `scoeFrameInstancesStore.sendInstances` 中的所有帧实例，逐个通过 `sendFrameInstance('network:scoe-udp:scoe-udp-remote', instance)` 发送。发送结果失败仅打印警告，不中断后续帧的发送。
32	- **代码位置**：`scoeStore.ts:278-287`（`sendScoeFrames`）
33	- **新系统对应 feature**：指令接入 feature 的帧发送
34	- **oracle 来源评估**：代码即 oracle。每秒轮询式全量发送是 SCOE 协议的核心行为
35	- **保留/排除建议**：保留。SCOE 协议要求周期性发送帧数据
36	
37	#### 行为 4：TCP Server 连接管理
38	
39	- **旧行为描述**：SCOE 可启动一个 TCP Server（`scoe-tcp-server`），IP 和端口从 `globalConfig.tcpServerIp/tcpServerPort` 读取。支持自动连接（`tcpServerAutoConnect`）——初始化时若该选项为 true 则自动调用 `checkTcpConnection()`。TCP 连接是 toggle 语义：未连接时调用则连接，已连接时调用则断开。
40	- **代码位置**：`scoeStore.ts:252-273`（`checkTcpConnection`）、`scoeStore.ts:319`（自动连接）
41	- **新系统对应 feature**：指令接入 feature 的连接管理
42	- **oracle 来源评估**：代码即 oracle
43	- **保留/排除建议**：保留。TCP Server 是接收外部指令的通道
44	
45	#### 行为 5：SCOE 接收指令配置模型
46	
47	- **旧行为描述**：每个 SCOE 接收指令（`ScoeReceiveCommand`）包含以下可配置项：
48	  - `label`：指令标签（显示名）
49	  - `code`：功能码（十六进制字符串，如 `"0x1234"`）
50	  - `function`：指令功能枚举，包括：`LOAD_SATELLITE_ID`、`UNLOAD_SATELLITE_ID`、`HEALTH_CHECK`、`LINK_CHECK`、`SEND_FRAME`、`READ_FILE_AND_SEND`
51	  - `checksums`：校验和配置数组（每项含 enabled/offset/length/checksumOffset）
52	  - `params`：参数数组（每项含 id/label/value/type/offset/length/options），参数选项含 `receiveCode`
53	  - `frameInstances`：关联的发送帧实例数组
54	  - `completionConditions`：完成条件数组
55	  - `completionTimeout`：完成条件超时（默认 5000ms）
56	  - `successFrameId`：执行成功后发送的帧 ID
57	- **代码位置**：`src/types/scoe/receiveCommand.ts:85-108`（`ScoeReceiveCommand` 接口）
58	- **新系统对应 feature**：指令接入 feature 的指令定义
59	- **oracle 来源评估**：类型定义 + 默认工厂函数
60	- **保留/排除建议**：保留。这六种指令功能是 SCOE 协议的核心能力集
61	
62	#### 行为 6：SCOE 完成条件匹配模型
63	
64	- **旧行为描述**：完成条件（`CompletionCondition`）支持两种模式：
65	  - **固定值匹配**：`useParam=false`，指定 `sourceFrameId/sourceFieldId` + `operator`（EQUAL/NOT_EQUAL/GREATER_THAN/LESS_THAN/GREATER_EQUAL/LESS_EQUAL）+ `targetFixedValue`
66	  - **参数选项匹配**：`useParam=true`，指定 `targetParamId`，通过 `options` 数组匹配（每项含 `operator` + `matchValue`）
67	- **代码位置**：`src/types/scoe/receiveCommand.ts:160-180`（`CompletionCondition` 接口）、`scoeFrameInstancesStore.ts:510-570`（CRUD 方法）
68	- **新系统对应 feature**：指令接入 feature 的条件匹配
69	- **oracle 来源评估**：类型定义
70	- **保留/排除建议**：保留。六种比较运算符和固定值/参数选项两种模式构成 SCOE 指令确认的匹配能力
71	
72	#### 行为 7：SCOE 状态统计
73	
74	- **旧行为描述**：SCOE 状态（`ScoeStatus`）跟踪以下统计指标：
75	  - `runtimeSeconds`：软件运行总秒数（每秒 +1）
76	  - `satelliteIdRuntimeSeconds`：当前卫星 ID 加载累计秒（加载时 +1，卸载时清零）
77	  - `commandReceiveCount`：指令接收总计数
78	  - `commandSuccessCount`：指令执行成功总计数
79	  - `lastCommandCode`：最近一条指令功能码
80	  - `commandErrorCount`：指令执行出错计数
81	  - `lastErrorReason`：指令执行出错原因（枚举：无错误/卫星ID不存在/配置不完整/正在加载/指令码不存在/校验和错误/完成条件超时）
82	  - `loadedSatelliteId`：已加载配置的卫星 ID
83	  - `healthStatus`：健康状态（unknown/healthy/error）
84	  - `linkTestResult`：链路自检结果（unknown/pass/fail）
85	  - `scoeFramesLoaded`：SCOE 帧是否已加载
86	  - `receiveCommandSuccess`：接收指令执行完成标志（每秒重置为 false）
87	- **代码位置**：`src/types/scoe/index.ts:57-83`（`ScoeStatus` 接口）、`scoeStore.ts:293-311`（更新逻辑）
88	- **新系统对应 feature**：指令接入 feature 的状态管理
89	- **oracle 来源评估**：类型定义 + 更新逻辑
90	- **保留/排除建议**：保留。这些统计指标是 SCOE 面板显示的核心数据
91	
92	#### 行为 8：卫星配置管理
93	
94	- **旧行为描述**：SCOE 支持多卫星配置（`ScoeSatelliteConfig[]`）。每个配置包含发送配置（卫星识别字/信息标识/信源标识/信宿标识/UDP IP/UDP 端口）和接收配置（额外含型号ID/卫星ID/三个识别开关）。配置持久化通过 `dataStorageAPI.scoeSatelliteConfigs.saveAll/list`。全局配置（`ScoeGlobalConfig`）含 TCP Server 参数、UDP 参数、6 个字节偏移量配置（信息标识/信源/信宿/型号ID/卫星ID/功能码）、成功帧 ID 和高亮配置。
95	- **代码位置**：`scoeStore.ts:82-173`（配置管理）、`src/types/scoe/index.ts:10-131`（类型定义）
96	- **新系统对应 feature**：指令接入 feature 的配置管理
97	- **oracle 来源评估**：类型定义 + 持久化 API
98	- **保留/排除建议**：保留。多卫星配置和字节偏移量配置是 SCOE 协议的必要参数
99	
100	---
101	
102	### 二、定时发送流程
103	
104	#### 行为 9：定时发送配置模型
105	
106	- **旧行为描述**：定时发送（`TimedStrategyConfig`）配置项：
107	  - `sendInterval`：发送间隔（毫秒），默认 1000ms
108	  - `repeatCount`：重复次数，默认 1
109	  - `isInfinite`：是否无限循环，默认 false
110	  - 配置持久化到帧实例的 `strategyConfig` 中
111	  - 配置变更时通过 watch 自动保存到 store
112	- **代码位置**：`TimedSendDialog.vue:43-47`（本地状态）、`TimedSendDialog.vue:111-124`（`setTimedConfig`）
113	- **新系统对应 feature**：task feature 的定时发送 step
114	- **oracle 来源评估**：代码实现
115	- **保留/排除建议**：保留。间隔/重复次数/无限循环是定时发送的核心参数
116	
117	#### 行为 10：定时发送执行流程
118	
119	- **旧行为描述**：
120	  1. 用户点击"开始定时发送"
121	  2. 通过 `useSendTaskManager().createTimedTask()` 创建任务（状态 `idle`）
122	  3. 通过 `startTask()` 启动任务
123	  4. `startTimedTask()` 初始化帧实例缓存（deepClone），将状态改为 `running`
124	  5. 立即执行第一次发送
125	  6. 若需重复，通过 `timerManager.registerTimer()` 注册 interval 定时器，按 `sendInterval` 间隔重复执行
126	  7. 每次发送更新进度（`currentCount`、`percentage`）
127	  8. 达到 `repeatCount` 后自动完成（状态 `completed`），清理缓存和定时器
128	  9. 无限循环模式只更新 `currentCount` 和 `nextExecutionTime`，不设上限
129	- **代码位置**：`useSendTaskExecutor.ts:542-656`（`createTimedSender` + `startTimedTask`）
130	- **新系统对应 feature**：task feature 的 step 执行引擎
131	- **oracle 来源评估**：代码实现。执行流程完整且可追溯
132	- **保留/排除建议**：保留。立即发送第一次 + interval 重复 + 自动完成是定时发送的核心行为
133	
134	#### 行为 11：定时发送的帧实例缓存与参数变化
135	
136	- **旧行为描述**：
137	  - 每个任务启动时 deepClone 所有帧实例到缓存（`frameInstanceCaches` Map）
138	  - 若实例启用参数变化（`enableVariation`），每次发送前按 `currentVariationIndex` 更新缓存实例的字段值
139	  - 发送使用缓存实例而非原始实例，避免修改原始配置
140	  - 任务完成后清理缓存
141	- **代码位置**：`useSendTaskExecutor.ts:54-75`（缓存初始化）、`useSendTaskExecutor.ts:80-101`（参数更新）
142	- **新系统对应 feature**：task feature 的 step 执行引擎
143	- **oracle 来源评估**：代码实现
144	- **保留/排除建议**：保留。帧实例不可变 + 参数变化是"可变参数发送"能力的基础
145	
146	#### 行为 12：关闭对话框时的任务继续行为
147	
148	- **旧行为描述**：定时发送对话框关闭时，若任务仍在运行，弹出确认对话框，用户可选"停止任务并关闭"或"后台运行"。选后台运行则任务继续执行，对话框关闭。
149	- **代码位置**：`TimedSendDialog.vue:193-220`（关闭逻辑）
150	- **新系统对应 feature**：task feature 的 UI 交互
151	- **oracle 来源评估**：代码实现
152	- **保留/排除建议**：保留。后台运行任务是用户可感知的 UI 行为
153	
154	---
155	
156	### 三、触发发送流程
157	
158	#### 行为 13：触发发送配置模型（条件触发）
159	
160	- **旧行为描述**：条件触发（`triggerType='condition'`）配置项：
161	  - `sourceId`：监听来源（从连接目标列表中选择）
162	  - `triggerFrameId`：触发帧（从接收帧列表中选择）
163	  - `conditions`：触发条件数组，每个条件含 `fieldId`（已映射字段）、`condition`（equals/not_equals/greater/less/contains）、`value`（匹配值）、`logicOperator`（and/or）
164	  - `continueListening`：触发后是否继续监听（默认 true）
165	  - `responseDelay`：响应延时（毫秒），触发后延时发送
166	- **代码位置**：`TriggerSendDialog.vue:58-72`（本地状态）、`TriggerSendDialog.vue:171-203`（`setTriggerConfig`）
167	- **新系统对应 feature**：task feature 的条件触发 step
168	- **oracle 来源评估**：代码实现
169	- **保留/排除建议**：保留。来源+帧+条件+继续监听+延时构成条件触发的完整参数
170	
171	#### 行为 14：触发发送配置模型（时间触发）
172	
173	- **旧行为描述**：时间触发（`triggerType='time'`）配置项：
174	  - `executeTime`：执行时间（ISO 8601 datetime）
175	  - `isRecurring`：是否重复执行
176	  - `recurringType`：重复类型（second/minute/hour/daily/weekly/monthly）
177	  - `recurringInterval`：重复间隔
178	  - `endTime`：重复结束时间
179	- **代码位置**：`TriggerSendDialog.vue:68-72`（本地状态）、`TriggerSendDialog.vue:186-195`（时间配置构建）
180	- **新系统对应 feature**：task feature 的时间触发 step
181	- **oracle 来源评估**：代码实现
182	- **保留/排除建议**：保留。执行时间+重复+6 种重复粒度+结束时间构成时间触发的完整参数
183	
184	#### 行为 15：条件触发条件评估逻辑
185	
186	- **旧行为描述**：
187	  - 空条件数组 = 接收到帧即触发（默认触发）
188	  - 条件评估支持 AND/OR 逻辑组合（通过 `logicOperator` 字段）
189	  - 支持短路逻辑：AND 遇 false 或 OR 遇 true 提前结束
190	  - 单个条件支持 5 种操作符：equals（字符串比较）、not_equals（字符串比较）、greater/less（数值比较）、contains（字符串包含）
191	  - 条件中的 `fieldId` 通过接收帧映射关系（`receiveFramesStore.mappings`）查找对应的 `dataItem`
192	  - 评估失败（找不到字段或数据项）时，AND 逻辑返回 false，OR 逻辑继续检查
193	- **代码位置**：`useSendTaskTriggerListener.ts:100-158`（`evaluateTriggerConditions`）、`useSendTaskTriggerListener.ts:189-218`（`evaluateSingleCondition`）
194	- **新系统对应 feature**：task feature 的条件匹配，匹配逻辑归 shared/
195	- **oracle 来源评估**：代码实现。条件评估逻辑完整且边界清晰
196	- **保留/排除建议**：保留。AND/OR 组合 + 5 种操作符 + 短路逻辑是条件触发的核心判断能力
197	
198	#### 行为 16：条件触发执行流程
199	
200	- **旧行为描述**：
201	  1. 用户点击"开始监听"
202	  2. 创建 `triggered` 类型任务，状态 `idle`
203	  3. `startTask()` -> `startTriggeredTask()` 初始化帧实例缓存
204	  4. 将任务状态改为 `waiting-trigger`
205	  5. 注册触发监听器（`registerTriggerListener`），记录 sourceId/triggerFrameId/conditions/continueListening/responseDelay
206	  6. 当接收帧系统收到数据时，调用 `handleFrameReceived(frameId, sourceId, updatedDataItems)`
207	  7. 遍历活跃监听器，匹配 frameId + sourceId
208	  8. 匹配成功后评估条件，条件满足则执行
209	  9. 执行前若 `responseDelay > 0`，先等待延时
210	  10. 发送帧实例（单实例用 `processInstance`，多实例用 `processMultipleInstances`）
211	  11. 若 `continueListening = true`，保持 `waiting-trigger` 状态继续监听；否则完成任务
212	- **代码位置**：`useSendTaskTriggerListener.ts:70-95`（`handleFrameReceived`）、`useSendTaskTriggerListener.ts:223-306`（`executeTriggerTask`）
213	- **新系统对应 feature**：task feature 的触发执行
214	- **oracle 来源评估**：代码实现
215	- **保留/排除建议**：保留。注册监听 -> 接收帧回调 -> 条件匹配 -> 延时 -> 发送 -> 继续监听是条件触发的完整生命周期
216	
217	#### 行为 17：时间触发执行流程
218	
219	- **旧行为描述**：
220	  1. 创建 `triggered` 类型任务（`triggerType='time'`）
221	  2. 计算初始执行时间与当前时间的差值
222	  3. 将任务状态改为 `waiting-schedule`
223	  4. 注册 setTimeout 定时器，到达执行时间后执行
224	  5. 执行时状态改为 `running`，发送所有帧实例
225	  6. 若 `isRecurring = true`，计算下次执行时间，再次进入 `waiting-schedule`
226	  7. 重复类型支持 6 种：second/minute/hour/daily/weekly/monthly，按 `recurringInterval` 递增
227	  8. 若设置了 `endTime`，下次执行时间超过 endTime 则完成任务
228	  9. 一次性执行（`isRecurring = false`）完成后直接 `completed`
229	- **代码位置**：`useSendTaskExecutor.ts:794-937`（`createScheduledExecutor` + `startTimedTriggeredTask`）
230	- **新系统对应 feature**：task feature 的时间触发 step
231	- **oracle 来源评估**：代码实现
232	- **保留/排除建议**：保留。等待调度 -> 执行 -> 重复/完成是时间触发的完整生命周期
233	
234	---
235	
236	### 四、顺序发送流程（Enhanced Sequential Send）
237	
238	#### 行为 18：多帧发送策略选择
239	
240	- **旧行为描述**：多帧发送对话框（`EnhancedSequentialSendDialog`）支持 4 种策略：
241	  - **immediate**：立即发送，所有帧实例按序发送一次
242	  - **timed**：定时发送，所有帧实例按序发送，按间隔重复
243	  - **triggered**：触发发送，所有帧实例按序发送，触发条件满足时执行
244	  - **variable**：可变参数发送，基于定时发送实现，每轮更新参数值
245	- **代码位置**：`EnhancedSequentialSendDialog.vue:86`（策略类型定义）、`EnhancedSequentialSendDialog.vue:634-763`（`startSendingTask`）
246	- **新系统对应 feature**：task feature 的多 step 任务
247	- **oracle 来源评估**：代码实现
248	- **保留/排除建议**：保留。4 种策略覆盖了所有发送场景
249	
250	#### 行为 19：多帧序列管理
251	
252	- **旧行为描述**：
253	  - 用户可从可用帧实例列表中选择实例添加到发送序列
254	  - 每个序列项包含：帧实例引用、发送目标 ID、实例间延时（默认 1000ms）
255	  - 支持上移/下移调整顺序
256	  - 支持移除序列项
257	  - 序列数据持久化到 `localStorage`（key: `enhanced-sequential-send-instances`）
258	  - 每个序列项支持独立设置发送目标（可选择不同的连接目标）
259	- **代码位置**：`EnhancedSequentialSendDialog.vue:280-346`（序列管理方法）
260	- **新系统对应 feature**：task feature 的 step 配置
261	- **oracle 来源评估**：代码实现
262	- **保留/排除建议**：保留。多帧序列管理是用户直接操作的核心 UI 行为
263	
264	#### 行为 20：可变参数发送
265	
266	- **旧行为描述**：
267	  - 每个序列项可启用参数变化（`enableVariation`）
268	  - 配置字段变化（`fieldVariations`）：指定字段 ID 和变化值数组
269	  - 变化值支持手动输入（逗号分隔）和文件导入（.txt/.csv，支持换行/回车/逗号分隔）
270	  - 执行时验证所有可变字段的值数组长度一致，不一致则报错
271	  - 重复次数 = 参数数组长度
272	  - 第 N 轮发送时，使用第 N 个参数值更新帧实例字段
273	- **代码位置**：`EnhancedSequentialSendDialog.vue:362-502`（可变参数管理）、`EnhancedSequentialSendDialog.vue:702-744`（variable 策略执行）
274	- **新系统对应 feature**：task feature 的可变参数 step
275	- **oracle 来源评估**：代码实现
276	- **保留/排除建议**：保留。参数变化是测试工具的重要能力
277	
278	#### 行为 21：任务配置导入/导出
279	
280	- **旧行为描述**：
281	  - 多帧发送配置支持导出为 JSON 文件（存储到 `data/frames/taskConfigs`）
282	  - 导入时验证配置文件格式（`validateTaskConfigFile`）和实例引用有效性（`validateInstanceReferences`）
283	  - 导入时恢复策略配置和序列数据
284	- **代码位置**：`EnhancedSequentialSendDialog.vue:534-629`（`handleGetTaskConfigData` + `handleSetTaskConfigData`）
285	- **新系统对应 feature**：task feature 的持久化
286	- **oracle 来源评估**：代码实现
287	- **保留/排除建议**：保留。配置导入/导出是用户可见的功能入口
288	
289	---
290	
291	### 五、SCOE 测试工具（录制/回放）
292	
293	#### 行为 22：发送/接收数据录制
294	
295	- **旧行为描述**：
296	  - 发送数据录制：通过 `addSendData(data)` 添加记录，当 `sendStopped = false` 时录制
297	  - 接收数据录制：通过 `addReceiveData(data, checksumValid, failedReason)` 添加记录，当 `receiveStopped = false` 时录制
298	  - 每条记录含：时间戳（精确到毫秒的中文格式）、原始数据（hex 字符串）、校验状态（仅接收）、预计算的高亮段
299	  - 数据列表按时间倒序排列（新数据在前）
300	  - 最大记录行数可配置（`maxRecordLines`，默认 30，范围 1-10000）
301	  - 超出限制时裁剪旧数据
302	- **代码位置**：`useScoeTestTool.ts:113-178`（`addSendData` + `addReceiveData`）
303	- **新系统对应 feature**：指令接入 feature 的测试工具
304	- **oracle 来源评估**：代码实现
305	- **保留/排除建议**：保留。数据录制是测试工具的核心能力
306	
307	#### 行为 23：数据高亮显示
308	
309	- **旧行为描述**：
310	  - 支持为发送区和接收区分别配置高亮规则（`HighlightConfigs`）
311	  - 每条高亮规则含：名称、字节偏移量（offset）、字节长度（length）
312	  - 高亮颜色循环使用 6 种预设颜色（蓝/绿/黄/紫/粉/橙），自动分配
313	  - 数据被分割为连续的高亮/非高亮段（`DataSegment[]`），UI 按段渲染
314	  - 相邻高亮配置的颜色不同
315	- **代码位置**：`useScoeTestTool.ts:42-108`（`calculateSegments`）、`src/types/scoe/highlightConfig.ts`（类型定义）
316	- **新系统对应 feature**：指令接入 feature 的测试工具 UI
317	- **oracle 来源评估**：代码实现
318	- **保留/排除建议**：保留。数据高亮帮助用户快速定位帧数据中的关键字段
319	
320	#### 行为 24：发送/接收录制开关
321	
322	- **旧行为描述**：
323	  - 发送录制默认停止（`sendStopped = true`），需手动开启
324	  - 接收录制默认开启（`receiveStopped = false`）
325	  - 初始化时清空所有数据
326	- **代码位置**：`useScoeTestTool.ts:31-34`（默认值）、`useScoeTestTool.ts:204-207`（初始化）
327	- **新系统对应 feature**：指令接入 feature 的测试工具 UI
328	- **oracle 来源评估**：代码实现
329	- **保留/排除建议**：保留。录制开关是用户直接操作的 UI 控件
330	
331	---
332	
333	### 六、活跃任务监控
334	
335	#### 行为 25：活跃任务列表与筛选
336	
337	- **旧行为描述**：
338	  - 任务监控面板（`ActiveTasksMonitor`）显示所有活动任务（running + paused + waiting-trigger + waiting-schedule）
339	  - 支持按类型筛选：全部/顺序/定时/多实例定时/触发/多实例触发
340	  - 支持按状态筛选：全部/运行中/已暂停/等待触发/等待执行/错误
341	  - 每个任务显示：名称、状态 badge（颜色区分）、类型 badge、任务图标
342	- **代码位置**：`ActiveTasksMonitor.vue:31-44`（筛选逻辑）、`ActiveTasksMonitor.vue:47-63`（标签映射）、`ActiveTasksMonitor.vue:241-381`（模板）
343	- **新系统对应 feature**：task feature 的监控 UI
344	- **oracle 来源评估**：代码实现
345	- **保留/排除建议**：保留。任务列表和筛选是用户管理并发任务的核心入口
346	
347	#### 行为 26：任务进度展示
348	
349	- **旧行为描述**：
350	  - 运行中/已暂停任务显示进度条（`q-linear-progress`）和百分比
351	  - 定时任务：显示"已执行 N 次"（无限循环）或 "N/M"（有限次）
352	  - 定时任务额外显示下次发送剩余时间（"X 时 Y 分后"/"X 分 Y 秒后"/"X 秒后"/"即将执行"）
353	  - 触发任务在 `waiting-trigger` 状态显示"等待触发条件满足"
354	  - 时间触发任务在 `waiting-schedule` 状态显示"将在 X 后执行"
355	  - 所有运行中的任务显示运行时长（"X 时 Y 分 Z 秒"）
356	  - 错误任务显示错误信息
357	- **代码位置**：`ActiveTasksMonitor.vue:106-150`（时间计算函数）、`ActiveTasksMonitor.vue:264-327`（进度展示模板）
358	- **新系统对应 feature**：task feature 的监控 UI
359	- **oracle 来源评估**：代码实现
360	- **保留/排除建议**：保留。进度/时间/状态的实时展示是用户直接感知的行为
361	
362	#### 行为 27：任务操作控制
363	
364	- **旧行为描述**：
365	  - running 状态：可暂停（pause）、可停止（stop）
366	  - paused 状态：可继续（resume）、可停止（stop）
367	  - waiting-trigger 状态：可停止监听（stop）
368	  - waiting-schedule 状态：可停止定时（stop）
369	  - error 状态：可重试（start）
370	  - 停止任务时：清理定时器、注销触发监听器、更新状态为 completed
371	  - 暂停任务时：仅更新状态为 paused（定时器不实际暂停，resume 时需重新启动）
372	  - 强制清理（`forceCleanupTask`）：清空所有定时器 + 监听器，状态设为 error
373	- **代码位置**：`ActiveTasksMonitor.vue:83-103`（操作分发）、`useSendTaskController.ts:26-65`（stopTask）、`useSendTaskController.ts:70-92`（pauseTask）、`useSendTaskController.ts:97-117`（resumeTask）
374	- **新系统对应 feature**：task feature 的控制操作
375	- **oracle 来源评估**：代码实现
376	- **保留/排除建议**：保留。暂停/继续/停止/重试/强制清理是任务管理的完整操作集
377	
378	---
379	
380	### 七、任务状态机
381	
382	#### 行为 28：任务状态机完整转换
383	
384	- **旧行为描述**：任务状态（`TaskStatus`）共 7 种，转换规则：
385	  - `idle` -> `running`（启动顺序/定时任务）、`idle` -> `waiting-trigger`（启动条件触发任务）、`idle` -> `waiting-schedule`（启动时间触发任务）
386	  - `running` -> `completed`（所有实例发送完成）、`running` -> `error`（发送失败）、`running` -> `paused`（用户暂停）
387	  - `paused` -> `running`（用户恢复）
388	  - `waiting-trigger` -> `running`（条件满足，开始发送）、`waiting-trigger` -> `completed`（用户停止）
389	  - `waiting-schedule` -> `running`（执行时间到达）、`waiting-schedule` -> `completed`（用户停止）
390	  - `completed` 任务自动从列表移除
391	- **代码位置**：`sendTasksStore.ts:15-30`（类型定义）、`useSendTaskExecutor.ts` 各 `startXxxTask` 函数、`useSendTaskController.ts` 控制函数
392	- **新系统对应 feature**：task feature 的状态机
393	- **oracle 来源评估**：代码实现。状态机转换完整且可追溯
394	- **保留/排除建议**：保留。7 种状态和转换规则构成任务执行的状态骨架
395	
396	#### 行为 29：任务进度批量更新优化
397	
398	- **旧行为描述**：
399	  - 任务进度不直接更新 store，而是写入缓存（`progressCache`）
400	  - 每 1 秒批量同步缓存到 store（`BATCH_UPDATE_INTERVAL = 1000`）
401	  - 任务完成/错误/暂停时强制同步（`forceSyncCache`）
402	  - 通过状态索引（`statusIndexes` Map）实现 O(1) 状态查询
403	  - `taskMap` 实现 O(1) ID 查找
404	- **代码位置**：`sendTasksStore.ts:153-358`（缓存和索引机制）
405	- **新系统对应 feature**：task feature 的性能优化层
406	- **oracle 来源评估**：代码实现
407	- **保留/排除建议**：保留性能优化思路，但具体实现可按新架构调整。1 秒批量更新和高频发送场景下的性能保障是可观测的间接行为（UI 流畅度）
408	
409	---
410	
411	### 八、帧实例管理
412	
413	#### 行为 30：SCOE 帧实例发送列表管理
414	
415	- **旧行为描述**：
416	  - 发送帧实例列表（`sendInstances`）持久化到 `dataStorageAPI.scoeFramesSendInstances`
417	  - 支持添加/复制/删除/选择帧实例
418	  - 选择时创建 deepClone 到 `localSendInstance` 作为编辑副本
419	  - 编辑后通过 `applyLocalEdit()` 将本地副本写回列表
420	  - 支持取消编辑（恢复到原始状态）
421	  - 可用帧过滤条件：`isSCOEFrame && direction === 'send'`
422	- **代码位置**：`scoeFrameInstancesStore.ts:55-218`（发送实例管理）
423	- **新系统对应 feature**：frame feature 的实例管理（SCOE 标记实例）
424	- **oracle 来源评估**：代码实现
425	- **保留/排除建议**：保留。帧实例的 CRUD 和编辑副本模式是用户直接操作的行为
426	
427	#### 行为 31：SCOE 接收指令列表管理
428	
429	- **旧行为描述**：
430	  - 接收指令列表（`receiveCommands`）持久化到 `dataStorageAPI.scoeFramesReceiveCommands`
431	  - 支持添加/复制/删除/选择接收指令
432	  - 每个指令可关联多个帧实例（`frameInstances`）用于响应发送
433	  - 每个指令可配置多个校验和（`checksums`）
434	  - 每个指令可配置多个参数（`params`），每个参数可配置多个选项（`options`）
435	  - 每个指令可配置多个完成条件（`completionConditions`）
436	  - UI 展开状态（`expandedParamIds`/`expandedInstanceIds`/`expandedConditionIds`）用于管理嵌套编辑
437	- **代码位置**：`scoeFrameInstancesStore.ts:220-570`（接收指令管理）
438	- **新系统对应 feature**：指令接入 feature 的指令配置
439	- **oracle 来源评估**：代码实现
440	- **保留/排除建议**：保留。接收指令的嵌套配置（参数->选项、帧实例、完成条件）是 SCOE 指令定义的核心数据结构
441	
442	---
443	
444	### 九、发送连接管理
445	
446	#### 行为 32：连接断开时任务自动暂停
447	
448	- **旧行为描述**：
449	  - 发送帧到目标时，若 `sendFrameInstance` 返回失败，检查目标是否可用（`isTargetAvailable`）
450	  - 若目标不可用（连接断开），自动将任务状态改为 `paused`，错误信息为"连接已断开"
451	  - 任务暂停后不再发送，等待用户处理
452	- **代码位置**：`useSendTaskExecutor.ts:222-247`（`sendFrameToTarget`）
453	- **新系统对应 feature**：task feature 的容错处理
454	- **oracle 来源评估**：代码实现
455	- **保留/排除建议**：保留。连接断开自动暂停是用户可感知的保护行为
456	
457	#### 行为 33：实例间延时
458	
459	- **旧行为描述**：
460	  - 多实例顺序发送时，实例间可配置延时（`interval`，默认 1000ms）
461	  - 最后一个实例发送后不添加延时
462	  - 延时通过 `setTimeout` 实现
463	- **代码位置**：`useSendTaskExecutor.ts:252-260`（`addInstanceDelay`）
464	- **新系统对应 feature**：task feature 的 step 间延时
465	- **oracle 来源评估**：代码实现
466	- **保留/排除建议**：保留。实例间延时控制发送节奏是协议需求
467	
468	---
469	
470	### 十、全局配置与字节偏移
471	
472	#### 行为 34：SCOE 全局字节偏移配置
473	
474	- **旧行为描述**：SCOE 全局配置（`ScoeGlobalConfig`）定义了 6 个字节偏移量：
475	  - `messageIdentifierOffset`（信息标识，默认 0）
476	  - `sourceIdentifierOffset`（信源标识，默认 1）
477	  - `destinationIdentifierOffset`（信宿标识，默认 2）
478	  - `modelIdOffset`（型号 ID，默认 3）
479	  - `satelliteIdOffset`（卫星 ID，默认 7）
480	  - `functionCodeOffset`（功能码，默认 11）
481	  - 另有 `successFrameId`：执行成功后发送的帧 ID
482	- **代码位置**：`src/types/scoe/index.ts:97-130`（`ScoeGlobalConfig` 接口）、默认值在 `defaultScoeGlobalConfig`
483	- **新系统对应 feature**：指令接入 feature 的协议配置
484	- **oracle 来源评估**：类型定义 + 默认值
485	- **保留/排除建议**：保留。字节偏移量是 SCOE 协议解析的必要参数
486	
487	---
488	
489	## 后续
490	
491	1. **关于"两阶段状态机"**：旧代码中未发现显式的"两阶段状态机"实现。SCOE 命令处理流程中的状态更新逻辑在 `updateStatus()` 中是简单的每秒重置 + 累加。如果"两阶段状态机"指的是 SCOE 外部设备（而非上位机软件）内部的协议状态机，则需要在硬件文档或甲方协议规范中寻找，旧上位机代码不是 oracle。
492	
493	2. **SCOE 命令接收与解析**：旧代码中 `scoeStore` 和 `scoeFrameInstancesStore` 定义了接收指令的配置模型（`ScoeReceiveCommand`），但没有找到实际接收 TCP 数据 -> 解析指令码 -> 匹配配置 -> 执行对应功能（加载卫星/卸载/健康自检/链路自检/发送帧/读取文件发送）的运行时代码。这意味着：要么这部分逻辑在 main process 的网络回调中（TCP Server 收到数据后），要么尚未实现。需要进一步检查 main process 代码确认。
494	
495	3. **测试工具的录制/回放**：旧代码中的 `useScoeTestTool` 只实现了数据录制（发送/接收数据列表），没有找到回放（replay）功能。录制的数据是追加到列表中的 hex 字符串，没有持久化到文件或重新发送的能力。
496	
497	4. **需要进一步确认的项目**：
498	   - TCP Server 收到数据后的指令解析和执行逻辑（可能在 main process）
499	   - `ScoeStatus` 中 `commandReceiveCount`/`commandSuccessCount`/`lastCommandCode` 等字段的实际更新位置（`updateStatus` 中只做清零/重置，递增逻辑可能在别处）
500	   - SCOE 指令的校验和验证逻辑（配置存在但验证代码未在已读文件中找到）
501	
```

> TOOL

tool_result
id: call_482e6562da634514a89ac7ea
```
1	# [S004] 旧系统连接管理可观测行为提取
2	
3	> 2026-05-19 | 调研 | active
4	
5	## 目标
6	
7	从旧系统代码中提取串口、网络（TCP/UDP/TCP Server）连接管理的所有可观测业务行为，为重写 connection feature 提供事实基础。只做事实提取，不做设计或实施。
8	
9	## 记录
10	
11	---
12	
13	### 一、串口连接完整生命周期
14	
15	#### 1.1 串口枚举（发现）
16	
17	- **旧行为**：通过读取 Windows 注册表 `HKLM:\HARDWARE\DEVICEMAP\SERIALCOMM` 获取可用 COM 端口列表。使用 PowerShell 命令执行，返回包含 `path`（如 COM3）、`manufacturer`、`pnpId`、`isOpen` 信息的端口描述。
18	- **代码位置**：`src-electron/main/ipc/serialHandlers.ts:51-123`（`listPorts` / `listPortsFromRegistry`）
19	- **渲染端调用**：`serialAPI.listPorts(forceRefresh)` → `serial:list` IPC
20	- **新系统对应 feature**：connection feature（串口枚举子能力）
21	- **oracle 来源**：Windows 注册表；代码中是唯一枚举路径（SerialPort 库的 list 方法未被使用，被注册表方式替代）。仅支持 Windows。
22	- **保留建议**：**保留**。枚举可用串口是核心能力，但实现方式需从注册表 PowerShell 迁移到跨平台方案（serialport 库原生 list）。
23	
24	#### 1.2 串口连接状态机
25	
26	- **旧行为**：串口连接有四个状态：`disconnected` → `connecting` → `connected` → `error`。状态转换：
27	  - `disconnected` → `connecting`：用户调用 `connectPort(portPath)` 时
28	  - `connecting` → `connected`：`serialAPI.open` 成功返回时
29	  - `connecting` → `error`：`serialAPI.open` 失败或异常时
30	  - `connected` → `disconnected`：用户主动断开 `disconnectPort(portPath)` 或端口意外关闭
31	  - `connected` → `error`：串口运行中发生错误
32	  - `error` → `connecting`：用户再次尝试连接
33	- **代码位置**：
34	  - 状态定义：`src/types/serial/serial.ts:66`（`ConnectionStatus = 'disconnected' | 'connecting' | 'connected' | 'error'`）
35	  - 状态转换：`src/stores/serialStore.ts:161-209`（`connectPort`）、`216-243`（`disconnectPort`）、`355-376`（`updatePortStatus`）
36	- **新系统对应 feature**：connection feature
37	- **oracle 来源**：代码事实。四状态模型完整覆盖。
38	- **保留建议**：**保留**。四状态模型合理，应作为新系统串口连接状态基础。
39	
40	#### 1.3 串口配置
41	
42	- **旧行为**：
43	  - 默认配置：`baudRate: 9600, dataBits: 8, stopBits: 1, parity: 'none', flowControl: 'none', autoOpen: false`
44	  - 支持的参数：baudRate、dataBits（5/6/7/8）、stopBits（1/1.5/2）、parity（none/even/odd/mark/space）、flowControl（none/hardware/software）、bufferSize、timeout
45	  - 配置持久化：每个端口独立配置通过 `useStorage('serial-options-map')` 持久化到 localStorage；全局默认配置通过 `useStorage('default-serial-options')` 持久化
46	  - 热更新配置：已连接的串口修改配置时，先关闭再重新打开（`setPortOptions` in serialHandlers.ts:467-490）
47	  - 未连接时修改配置只保存不立即应用
48	- **代码位置**：
49	  - 默认配置：`src/stores/serialStore.ts:22-29`
50	  - 持久化：`src/stores/serialStore.ts:54-59`
51	  - 热更新：`src/stores/serialStore.ts:295-314`、`src-electron/main/ipc/serialHandlers.ts:467-490`
52	  - 类型定义：`src/types/serial/serial.ts:6-21`
53	- **新系统对应 feature**：connection feature（配置子能力）
54	- **oracle 来源**：代码事实。配置参数与 SerialPort 库对齐。
55	- **保留建议**：**保留**。配置参数集合和热更新行为均为必要。持久化方式需迁移到新系统的持久化层。
56	
57	#### 1.4 串口数据收发
58	
59	- **旧行为**：
60	  - **接收**：main 进程通过 SerialPort `data` 事件接收原始二进制数据，广播 `serial:data` IPC 事件到所有渲染进程窗口。渲染端 serialStore 监听后同时更新 `receivedMessagesMap`（最近 100 条）和调用 `receiveFramesStore.handleReceivedData('serial', portPath, data)` 进行帧解析。
61	  - **发送**：支持三种发送方式：`sendText`（文本/十六进制）、`sendBinary`（Uint8Array）、`sendFrameInstance`（帧实例转 Buffer）。发送前检查连接状态。发送成功后 main 进程广播 `serial:data:sent` 事件。
62	  - **缓冲区清除**：`clearBuffer` 重置 bytesReceived 计数器（非真正清除缓冲区数据）
63	  - **历史记录**：每个端口维护收发历史（`receivedMessagesMap` / `sentMessagesMap`），限制 100 条，支持清空
64	- **代码位置**：
65	  - 接收：`src-electron/main/ipc/serialHandlers.ts:522-541`、`src/stores/serialStore.ts:392-421`
66	  - 发送：`src-electron/main/ipc/serialHandlers.ts:286-365`、`src/stores/serialStore.ts:510-579`
67	  - 历史记录：`src/stores/serialStore.ts:62-89`、`599-672`
68	- **新系统对应 feature**：connection feature（数据通道）+ receive/send feature
69	- **oracle 来源**：代码事实。
70	- **保留建议**：
71	  - **保留**：多端口并发收发、发送前置连接检查、帧实例发送。
72	  - **排除**：`receivedMessagesMap` / `sentMessagesMap` 的 100 条内存历史——这是旧系统调试/调试页面功能，新系统的 receive feature 有自己的帧存储。
73	
74	#### 1.5 串口状态广播
75	
76	- **旧行为**：main 进程在以下时机广播状态到所有渲染窗口：
77	  - 端口打开成功
78	  - 端口关闭
79	  - 数据接收（更新 bytesReceived）
80	  - 数据发送完成（更新 bytesSent）
81	  - 错误事件
82	  - 渲染端状态监听有 500ms 防抖（`useDebounceFn(..., 500)`）
83	- **代码位置**：
84	  - main 端广播：`src-electron/main/ipc/serialHandlers.ts:567-578`（`broadcastStatus`）
85	  - 渲染端防抖：`src/stores/serialStore.ts:449-465`
86	- **新系统对应 feature**：connection feature
87	- **oracle 来源**：代码事实。
88	- **保留建议**：**保留**。状态广播 + 防抖是合理的性能优化模式。新系统应在 platform facade 中统一实现。
89	
90	#### 1.6 串口连接生命周期清理
91	
92	- **旧行为**：
93	  - 应用退出时（`app.on('will-quit')`）自动关闭所有串口
94	  - 组件卸载时（`onUnmounted`）断开所有串口并清理监听器
95	  - 每个端口有独立的监听器清理函数数组（dataListener、sentDataListener、statusListener、allStatusListener）
96	- **代码位置**：
97	  - 应用级清理：`src-electron/main/ipc/serialHandlers.ts:639-651`
98	  - 组件级清理：`src/stores/serialStore.ts:707-715`
99	  - 监听器管理：`src/stores/serialStore.ts:382-502`
100	- **新系统对应 feature**：connection feature + app lifecycle
101	- **oracle 来源**：代码事实。
102	- **保留建议**：**保留**。生命周期清理是必要行为。
103	
104	#### 1.7 最后使用串口记忆
105	
106	- **旧行为**：记录最后使用的串口路径（`useStorage('last-used-port')`），用于下次启动时的默认选择。
107	- **代码位置**：`src/stores/serialStore.ts:51`
108	- **新系统对应 feature**：connection feature
109	- **oracle 来源**：代码事实。
110	- **保留建议**：**保留**。UX 便利行为。
111	
112	#### 1.8 串口断开全部
113	
114	- **旧行为**：`disconnectAllPorts()` 通过 `serialAPI.closeAll()` 一次性向 main 进程请求关闭所有端口，main 进程遍历 `portConnections` Map 逐一关闭，清空 `activePorts` 列表。
115	- **代码位置**：`src/stores/serialStore.ts:249-288`、`src-electron/main/ipc/serialHandlers.ts:259-278`
116	- **新系统对应 feature**：connection feature
117	- **oracle 来源**：代码事实。
118	- **保留建议**：**保留**。批量断开是必要操作。
119	
120	---
121	
122	### 二、TCP/UDP 网络连接完整生命周期
123	
124	#### 2.1 TCP 客户端模式
125	
126	- **旧行为**：
127	  - 创建 `net.Socket` 连接到指定的 `host:port`
128	  - 强制禁用 Nagle 算法（`setNoDelay(true)`），强制禁用 keepAlive（`setKeepAlive(false)`）
129	  - 连接超时默认 5000ms，可通过配置覆盖
130	  - 连接成功：状态 `connected`，广播 `network:connectionEvent`（type: 'connected'）
131	  - 数据接收：按 `\r\n` 分割（`handleTcpData`），逐包发送 `network:data` 事件到渲染进程
132	  - 连接错误/超时/关闭：广播对应事件，清理连接记录（`connections.delete`）
133	  - **无自动重连**：连接断开后需要用户手动重新连接（`autoReconnect` 字段存在于类型定义但未在 main 进程中实现）
134	- **代码位置**：`src-electron/main/ipc/networkHandlers.ts:85-141`（`connectTcp`）
135	- **新系统对应 feature**：connection feature（TCP 客户端子类型）
136	- **oracle 来源**：代码事实。TCP 客户端行为完整。
137	- **保留建议**：**保留**。TCP 客户端连接行为均为必要。需注意：
138	  - `\r\n` 分割逻辑是硬编码协议行为，新系统应可配置
139	  - `setKeepAlive(false)` 和 `setNoDelay(true)` 应可通过配置控制
140	  - `autoReconnect` 类型定义存在但未实现，新系统需决定是否实现
141	
142	#### 2.2 TCP Server 模式
143	
144	- **旧行为**：
145	  - 使用 `net.createServer` 监听指定 `host:port`
146	  - 接受多客户端连接，维护客户端列表 `tcpServerClients`
147	  - 每个客户端的 socket 设置 `setKeepAlive(false)` 和 `setNoDelay(true)`
148	  - 数据接收：所有客户端数据通过同一连接 ID 汇入 `handleTcpData`，按 `\r\n` 分割
149	  - 发送数据：向所有已连接客户端广播（`clients.forEach(client.write(...))`）
150	  - 客户端断开时从列表中移除，不触发服务器级别的 disconnected 事件
151	  - 服务器关闭时广播 `network:connectionEvent`（type: 'disconnected'）
152	- **代码位置**：`src-electron/main/ipc/networkHandlers.ts:146-224`（`connectTcpServer`）
153	- **新系统对应 feature**：connection feature（TCP Server 子类型）
154	- **oracle 来源**：代码事实。
155	- **保留建议**：**保留**。TCP Server 多客户端管理是必要行为。注意：
156	  - 向所有客户端广播发送是旧系统行为，新系统需确认是否需要定向发送
157	  - 客户端生命周期管理（连接/断开）需要独立事件通知
158	
159	#### 2.3 UDP 模式
160	
161	- **旧行为**：
162	  - 使用 `dgram.createSocket('udp4')` 创建 UDP socket
163	  - 绑定到指定 `host:port` 进行监听（`socket.bind`）
164	  - 当 `host === '0.0.0.0'` 时，bind 时不指定 host（`undefined`），表示监听所有接口
165	  - 支持广播模式（`options.broadcast` → `setBroadcast(true)`）
166	  - 数据接收：所有接收到的消息通过 `handleDataReceived` 处理（注意 UDP 不做 `\r\n` 分割）
167	  - 数据发送：需要指定目标地址（`targetHost` 格式 `host:port`），使用 `socket.send`
168	  - 远程主机列表：配置中可包含 `remoteHosts` 数组，每个远程主机有独立的 `id`、`name`、`host`、`port`、`enabled`、`description`
169	- **代码位置**：`src-electron/main/ipc/networkHandlers.ts:229-292`（`connectUdp`）、`src/types/serial/network.ts:11-19`（RemoteHost 类型）
170	- **新系统对应 feature**：connection feature（UDP 子类型）
171	- **oracle 来源**：代码事实。
172	- **保留建议**：**保留**。UDP 绑定+远程主机列表模式是完整的。远程主机列表作为 UDP 的发送目标管理，与 TCP/TCP Server 的发送模型不同。
173	
174	#### 2.4 网络连接通用状态管理
175	
176	- **旧行为**：
177	  - `NetworkConnectionManager` 类在 main 进程管理所有网络连接，使用 `Map<connectionId, NetworkConnection>` 存储
178	  - 连接状态：`connecting` → `connected` → `disconnected` / `error`
179	  - 重复连接处理：如果连接已存在且 `isConnected=true`，返回错误；如果 `isConnected=false`（残留），先清理再重新创建
180	  - 连接统计：每个连接维护 `bytesReceived`、`bytesSent`、`messagesReceived`、`messagesSent`、`lastActivity`、`connectionTime`
181	  - 断开连接：根据类型分别处理（TCP 销毁 socket、TCP Server 关闭所有客户端+关闭服务器、UDP 关闭 socket）
182	  - 渲染端 `netWorkStore` 通过 IPC 调用 main 进程方法，监听事件更新本地状态
183	- **代码位置**：
184	  - main 进程：`src-electron/main/ipc/networkHandlers.ts:22-609`（`NetworkConnectionManager`）
185	  - 渲染端：`src/stores/netWorkStore.ts:1-337`
186	- **新系统对应 feature**：connection feature
187	- **oracle 来源**：代码事实。
188	- **保留建议**：**保留**。通用连接管理、统计、断开清理均为必要行为。
189	
190	#### 2.5 网络数据接收事件链
191	
192	- **旧行为**：
193	  - main 进程接收到数据后调用 `handleDataReceived`
194	  - `handleDataReceived` 首先更新统计，然后检查高速存储规则
195	  - 如果命中高速存储规则，数据**不发送到渲染进程**，只做异步文件存储
196	  - 如果未命中，通过 `emitDataEvent` 将数据发送到所有渲染进程（`Array.from(data)` 转为普通数组以通过 IPC）
197	  - 渲染端 `networkAPI.onData` 监听 `network:data` 事件，将数据转为 `Uint8Array` 后调用 `receiveFramesStore.handleReceivedData('network', connectionId, data)`
198	  - 同时更新连接的 `lastActivity` 时间
199	- **代码位置**：
200	  - main 进程分流：`src-electron/main/ipc/networkHandlers.ts:498-521`（`handleDataReceived`）
201	  - 渲染端接收：`src/stores/netWorkStore.ts:200-219`（`setupNetworkDataHandling`）
202	- **新系统对应 feature**：connection feature + receive feature + storage feature
203	- **oracle 来源**：代码事实。
204	- **保留建议**：**保留**。数据接收 → 高速存储分流 → 渲染进程通知的完整链路需要保留。
205	
206	---
207	
208	### 三、高速存储分流逻辑
209	
210	#### 3.1 高速存储触发条件
211	
212	- **旧行为**：
213	  - 在网络数据接收路径 `handleDataReceived` 中，每次收到数据都调用 `storageManager.shouldStore(connectionId, data)`
214	  - 匹配条件：存储功能已启用（`config.enabled`）+ 规则已启用（`rule.enabled`）+ 连接 ID 匹配（解析 `network:` 前缀后的实际连接 ID）+ 帧头模式匹配（至少一个 headerPattern 完全匹配数据前缀）
215	  - 匹配后数据**不发送到渲染进程**，只异步写入文件（不阻塞数据处理）
216	  - 帧头匹配是精确前缀匹配（逐字节比较）
217	- **代码位置**：
218	  - 分流入口：`src-electron/main/ipc/networkHandlers.ts:507-517`
219	  - 匹配逻辑：`src-electron/main/ipc/highSpeedStorageHandlers.ts:104-119`（`shouldStore`）
220	  - 帧头匹配：`src-electron/main/ipc/highSpeedStorageHandlers.ts:77-96`（`matchFrameHeader`）
221	- **新系统对应 feature**：storage feature（高速存储子能力）
222	- **oracle 来源**：代码事实。注意此分流只在网络连接路径中，串口连接路径**没有**高速存储分流。
223	- **保留建议**：**保留**。高速存储分流是业务关键路径。但新系统应评估：
224	  - 是否串口也需要高速存储分流
225	  - 帧头匹配逻辑是否应从 storage 移到 shared/ 作为纯函数
226	
227	#### 3.2 高速存储文件管理
228	
229	- **旧行为**：
230	  - 存储位置：`userDataPath/business-data/` 目录
231	  - 文件名格式：`business_data_{ISO时间戳}.txt`
232	  - 数据格式：每行一条十六进制字符串
233	  - 文件轮转：达到 `maxFileSize`（默认 100MB）时关闭当前文件，清理超出 `rotationCount`（默认 5）的旧文件，创建新文件
234	  - 统计信息：`totalFramesStored`、`totalBytesStored`、`frameTypeStats`、`storageStartTime`、`lastStorageTime`
235	  - 重置统计：关闭写入流、删除当前文件、清零所有统计
236	- **代码位置**：`src-electron/main/ipc/highSpeedStorageHandlers.ts:140-388`
237	- **新系统对应 feature**：storage feature
238	- **oracle 来源**：代码事实。
239	- **保留建议**：**保留**。文件轮转、统计、重置均为必要行为。但新系统应将存储路径管理移到 platform facade。
240	
241	#### 3.3 高速存储配置
242	
243	- **旧行为**：
244	  - 单一规则（`FrameHeaderRule`）：包含 `connectionId`、`headerPatterns`（十六进制字符串数组）、`enabled`
245	  - 全局配置：`enabled`、`rule`、`maxFileSize`、`enableRotation`、`rotationCount`
246	  - 配置通过 IPC `highSpeedStorage:updateConfig` 动态更新
247	  - 从禁用变为启用时初始化写入流；从启用变为禁用时关闭存储
248	- **代码位置**：`src-electron/main/ipc/highSpeedStorageHandlers.ts:296-319`（`updateConfig`）、`src/types/serial/highSpeedStorage.ts`
249	- **新系统对应 feature**：storage feature
250	- **oracle 来源**：代码事实。
251	- **保留建议**：**保留**。动态配置启停行为合理。
252	
253	---
254	
255	### 四、连接状态 UI 展示行为
256	
257	#### 4.1 连接状态指示器
258	
259	- **旧行为**：
260	  - 串口状态：`portConnectionStatuses` Map，每个端口独立状态（disconnected/connecting/connected/error）
261	  - 网络状态：`connections` 数组中每个连接的 `isConnected` + `status` 字段
262	  - 状态更新：串口通过 `serial:status` IPC 事件（500ms 防抖），网络通过 `network:connectionEvent` 事件
263	  - 计算属性：`hasConnectedPort`（至少一个串口已连接）、`connectedCount`（网络已连接数）、`hasActiveConnections`（是否有活跃网络连接）
264	  - 连接统计：每端口/每连接的 `bytesReceived`、`bytesSent`
265	- **代码位置**：
266	  - 串口：`src/stores/serialStore.ts:42-43`（`portConnectionStatuses`）、`101-108`（计算属性）、`449`（防抖）
267	  - 网络：`src/stores/netWorkStore.ts:19-43`（状态和计算属性）、`222-249`（事件监听）
268	- **新系统对应 feature**：connection feature（selector 暴露）
269	- **oracle 来源**：代码事实。
270	- **保留建议**：**保留**。状态指示器和统计信息是 UI 核心需求。500ms 防抖是合理的更新频率。
271	
272	#### 4.2 错误信息展示
273	
274	- **旧行为**：
275	  - 串口：每个端口独立错误信息 `portErrorMessages` Map，连接失败、运行错误都会设置
276	  - 网络：全局 `lastError` + 每个连接的 `connection.error` 字段
277	  - 错误清除：串口 `clearPortError` 在连接尝试时清除；网络 `clearError` 手动清除
278	- **代码位置**：
279	  - 串口：`src/stores/serialStore.ts:44-45`、`333-348`
280	  - 网络：`src/stores/netWorkStore.ts:25`、`281-283`
281	- **新系统对应 feature**：connection feature
282	- **oracle 来源**：代码事实。
283	- **保留建议**：**保留**。错误信息独立管理合理。
284	
285	---
286	
287	### 五、多连接并发管理
288	
289	#### 5.1 多串口并发
290	
291	- **旧行为**：
292	  - 支持同时连接多个串口（`portConnections` Map in main process）
293	  - 每个端口独立的连接状态、配置、数据收发通道
294	  - `activePorts` 数组记录所有已连接端口
295	  - 数据接收按 `portPath` 分流到对应的 `receivedMessagesMap[portPath]`
296	  - `getAllMessages()` 可展平所有端口的消息并按时间戳排序
297	- **代码位置**：`src/stores/serialStore.ts:48`（`activePorts`）、`62-89`（消息映射）、`655-672`（`getAllMessages`）
298	- **新系统对应 feature**：connection feature
299	- **oracle 来源**：代码事实。
300	- **保留建议**：**保留**。多串口并发是核心需求。
301	
302	#### 5.2 网络多连接并发
303	
304	- **旧行为**：
305	  - `NetworkConnectionManager` 支持同时管理多个 TCP/TCP Server/UDP 连接
306	  - 每个连接有唯一 `id`，不同类型连接共存
307	  - TCP Server 的多客户端也是并发的（`tcpServerClients` Map）
308	  - `disconnectAll()` 使用 `Promise.allSettled` 并行断开
309	- **代码位置**：`src-electron/main/ipc/networkHandlers.ts:22-28`（数据结构）、`288-293`（渲染端 disconnectAll）
310	- **新系统对应 feature**：connection feature
311	- **oracle 来源**：代码事实。
312	- **保留建议**：**保留**。多网络连接并发是必要能力。
313	
314	#### 5.3 连接目标统一视图
315	
316	- **旧行为**：
317	  - `connectionTargetsStore` 将串口和网络连接统一为 `ConnectionTarget` 列表
318	  - 目标 ID 编码规则：串口 `serial:{portPath}`，网络 TCP/Server `network:{connectionId}`，网络 UDP 远程主机 `network:{connectionId}:{remoteHostId}`
319	  - 提供按类型分组（`serialTargets` / `networkTargets`）、按连接状态过滤（`connectedTargets`）
320	  - `getFirstAvailableTargetId()` 优先返回已连接目标
321	  - `isTargetAvailable(targetId)` 检查目标是否可用
322	  - `getValidatedTargetPath(targetId)` 为发送路由提供验证后的路径
323	  - 300ms 防抖刷新（`useDebounceFn(..., 1000)`，实际代码注释写的 300ms 但传入 1000ms）
324	  - 通过 `watchEffect` 监听串口和网络状态变化自动刷新
325	- **代码位置**：`src/stores/connectionTargetsStore.ts:1-253`
326	- **新系统对应 feature**：connection feature（selector）+ send feature（目标选择）
327	- **oracle 来源**：代码事实。
328	- **保留建议**：**保留**。统一目标视图是发送操作的基础。但注意：
329	  - `getValidatedTargetPath` 的路径编码规则需要在新系统中重新设计
330	  - UDP 远程主机作为独立发送目标的概念需要保留
331	
332	---
333	
334	### 六、连接配置的 CRUD 行为
335	
336	#### 6.1 串口配置持久化
337	
338	- **旧行为**：
339	  - 每个端口独立配置存储到 localStorage（`useStorage('serial-options-map')`）
340	  - 全局默认配置存储到 localStorage（`useStorage('default-serial-options')`）
341	  - 新端口使用默认配置，修改后保存为端口独立配置
342	  - 连接时优先使用端口独立配置，无则使用默认配置
343	- **代码位置**：`src/stores/serialStore.ts:54-59`（持久化）、`173-174`（使用）
344	- **新系统对应 feature**：connection feature + persistence
345	- **oracle 来源**：代码事实。
346	- **保留建议**：**保留**。配置持久化行为合理，但存储方式需迁移。
347	
348	#### 6.2 网络连接配置
349	
350	- **旧行为**：
351	  - `NetworkConnectionConfig` 包含：id、name、type、host、port、remoteHosts、autoReconnect、timeout、description
352	  - 连接配置由调用方（UI 或其他 store）构造并传入，store 本身不持久化连接配置
353	  - 连接成功后配置信息随 `NetworkConnection` 对象保存在 main 进程内存中
354	  - 断开后连接记录从内存中删除（`connections.delete(connectionId)`）
355	- **代码位置**：`src/types/serial/network.ts:22-32`（配置类型）、`src-electron/main/ipc/networkHandlers.ts:53-58`（连接创建）
356	- **新系统对应 feature**：connection feature + persistence
357	- **oracle 来源**：代码事实。注意：旧系统网络连接配置**没有持久化**，重启后需要重新创建。
358	- **保留建议**：**保留**连接配置类型。新系统应增加持久化能力（保留已创建的连接配置跨重启）。
359	
360	#### 6.3 高速存储规则配置
361	
362	- **旧行为**：
363	  - `StorageConfig` 包含：enabled、rule（单一 FrameHeaderRule）、maxFileSize、enableRotation、rotationCount
364	  - `FrameHeaderRule` 包含：id、connectionId、headerPatterns、enabled
365	  - 规则验证：检查 connectionId 非空、至少一个 headerPattern、十六进制格式合法、偶数长度
366	  - 配置通过 IPC 动态更新
367	- **代码位置**：`src/types/serial/highSpeedStorage.ts:8-24`、`src-electron/main/ipc/highSpeedStorageHandlers.ts:394-429`（`validateRule`）
368	- **新系统对应 feature**：storage feature
369	- **oracle 来源**：代码事实。
370	- **保留建议**：**保留**。规则配置和验证行为完整。
371	
372	---
373	
374	### 七、自动连接/自动重连行为
375	
376	#### 7.1 自动连接
377	
378	- **旧行为**：**无自动连接行为**。应用启动时只刷新可用端口列表（`serialStore.refreshPorts()`）和连接目标列表（`connectionTargetsStore.refreshTargets()`），不自动连接任何端口或网络。
379	- **代码位置**：`src/layouts/useAppLifecycle.ts:45-52`（onMounted）
380	- **oracle 来源**：代码事实。
381	- **保留建议**：**排除**。当前无自动连接。如新系统需要自动连接，需作为新需求设计。
382	
383	#### 7.2 自动重连
384	
385	- **旧行为**：**类型定义中存在 `autoReconnect` 字段**（`NetworkConnectionConfig.autoReconnect?: boolean`），但**main 进程和渲染端均未实现自动重连逻辑**。连接断开后（错误、超时、对端关闭），只更新状态为 `disconnected`/`error`，不做任何重连尝试。
386	- **代码位置**：`src/types/serial/network.ts:29`（字段定义）
387	- **oracle 来源**：代码事实。字段存在但无实现，属于预留接口。
388	- **保留建议**：**排除旧实现**（因为没有实现）。新系统如需自动重连，应作为新需求设计，可参考此字段名。
389	
390	---
391	
392	### 八、应用启动时的连接初始化
393	
394	- **旧行为**：
395	  - `useAppLifecycle.onMounted`：
396	    1. `serialStore.refreshPorts()` — 刷新可用串口列表（从注册表获取）
397	    2. `connectionTargetsStore.refreshTargets()` — 构建统一连接目标列表
398	    3. 同时初始化帧模板、发送实例、接收配置、全局统计、SCOE 等
399	  - `netWorkStore.initialize()`：
400	    1. `setupNetworkDataHandling()` — 设置数据监听、连接事件监听、状态变化监听
401	    2. `refreshConnections()` — 从 main 进程获取当前连接列表（通常为空，因为是新启动）
402	  - `connectionTargetsStore` 自动 watchEffect：串口/网络状态变化时自动重新构建目标列表
403	- **代码位置**：
404	  - 应用级：`src/layouts/useAppLifecycle.ts:45-52`
405	  - 网络初始化：`src/stores/netWorkStore.ts:297-300`
406	  - 目标自动更新：`src/stores/connectionTargetsStore.ts:218-231`
407	- **新系统对应 feature**：app lifecycle + connection feature
408	- **oracle 来源**：代码事实。
409	- **保留建议**：**保留**。启动时序：先枚举端口 → 建立监听 → 构建统一目标列表。这个顺序合理。
410	
411	---
412	
413	### 九、TCP 数据分割行为
414	
415	#### 9.1 TCP \r\n 分割
416	
417	- **旧行为**：
418	  - TCP 数据接收时按 `\r\n`（0x0D 0x0A）分割为独立数据包
419	  - `handleTcpData` 遍历数据查找所有 `\r\n` 位置，提取之间的数据
420	  - 不以 `\r\n` 结尾的剩余数据作为最后一个包
421	  - 空包（连续 `\r\n` 或开头 `\r\n`）被过滤掉
422	  - UDP 数据不做分割，直接作为整包处理
423	- **代码位置**：`src-electron/main/ipc/networkHandlers.ts:466-493`（`handleTcpData`）
424	- **新系统对应 feature**：connection feature（数据预处理）或 receive feature
425	- **oracle 来源**：代码事实。
426	- **保留建议**：**保留分割行为但参数化**。`\r\n` 分割是旧系统硬编码的协议假设，新系统应支持可配置的分隔符或无分割模式。这是业务关键行为，不能丢失。
427	
428	---
429	
430	### 十、IPC 通道一览
431	
432	#### 10.1 串口 IPC 通道
433	
434	| IPC 通道 | 方向 | 用途 |
435	|---|---|---|
436	| `serial:list` | invoke | 列出可用串口 |
437	| `serial:open` | invoke | 打开串口 |
438	| `serial:close` | invoke | 关闭串口 |
439	| `serial:close-all` | invoke | 关闭所有串口 |
440	| `serial:write` | invoke | 写入数据（文本/hex） |
441	| `serial:send` | invoke | 发送帧数据（二进制） |
442	| `serial:read` | invoke | 读取缓冲区数据 |
443	| `serial:status` | invoke | 获取单个端口状态 |
444	| `serial:all-status` | invoke | 获取所有端口状态 |
445	| `serial:setOptions` | invoke | 设置串口参数 |
446	| `serial:clearBuffer` | invoke | 清除接收缓冲区计数 |
447	| `serial:data` | on | 数据接收事件 |
448	| `serial:data:sent` | on | 数据发送确认事件 |
449	| `serial:status` | on | 状态变化事件（注意与 invoke 同名） |
450	
451	- **代码位置**：
452	  - main 端注册：`src-electron/main/ipc/serialHandlers.ts:581-631`
453	  - preload 桥接：`src-electron/preload/api/serial.ts`
454	- **新系统对应 feature**：connection feature（platform facade）
455	- **保留建议**：**保留语义，重写通道**。新系统的 preload facade 应提供类型安全的 API，不暴露裸 IPC 通道名。
456	
457	#### 10.2 网络 IPC 通道
458	
459	| IPC 通道 | 方向 | 用途 |
460	|---|---|---|
461	| `network:connect` | invoke | 创建网络连接 |
462	| `network:disconnect` | invoke | 断开连接 |
463	| `network:send` | invoke | 发送数据 |
464	| `network:getConnections` | invoke | 获取连接列表 |
465	| `network:getStatus` | invoke | 获取连接状态 |
466	| `network:data` | on | 数据接收事件 |
467	| `network:connectionEvent` | on | 连接事件（connected/disconnected/error） |
468	| `network:statusChange` | on | 状态变化事件 |
469	
470	- **代码位置**：
471	  - main 端注册：`src-electron/main/ipc/networkHandlers.ts:668-678`
472	  - preload 桥接：`src-electron/preload/api/network.ts`
473	- **新系统对应 feature**：connection feature（platform facade）
474	- **保留建议**：同上。
475	
476	#### 10.3 高速存储 IPC 通道
477	
478	| IPC 通道 | 方向 | 用途 |
479	|---|---|---|
480	| `highSpeedStorage:updateConfig` | invoke | 更新存储配置 |
481	| `highSpeedStorage:getConfig` | invoke | 获取当前配置 |
482	| `highSpeedStorage:getStats` | invoke | 获取统计信息 |
483	| `highSpeedStorage:validateRule` | invoke | 验证规则 |
484	| `highSpeedStorage:resetStats` | invoke | 重置统计 |
485	
486	- **代码位置**：`src-electron/main/ipc/highSpeedStorageHandlers.ts:491-501`
487	- **新系统对应 feature**：storage feature（platform facade）
488	- **保留建议**：同上。
489	
490	---
491	
492	### 十一、其他发现
493	
494	#### 11.1 串口端口热插拔
495	
496	- **旧行为**：**无主动热插拔检测**。`refreshPorts` 是被动调用（应用启动时调用一次）。没有定期轮询或 USB 事件监听。用户需要手动触发刷新。
497	- **代码位置**：`src/stores/serialStore.ts:134-154`（`refreshPorts`）
498	- **oracle 来源**：代码事实。
499	- **保留建议**：**排除旧行为，作为新需求评估**。新系统可考虑监听 USB 串口插拔事件自动刷新。
500	
501	#### 11.2 网络连接事件清理
502	
503	- **旧行为**：`netWorkStore` 有三个独立的监听器清理函数（`dataListenerCleanup`、`connectionEventCleanup`、`statusChangeCleanup`），通过 `cleanupListeners()` 统一管理。但 `initialize()` 是公开方法，需要外部调用。
504	- **代码位置**：`src/stores/netWorkStore.ts:27-29`、`261-276`、`297-300`
505	- **oracle 来源**：代码事实。
506	- **保留建议**：**保留**。监听器生命周期管理是必要行为。
507	
508	#### 11.3 UDP 目标地址解析
509	
510	- **旧行为**：`sendData` 接收 `targetHost` 参数，格式为 `host:port`。解析时按 `:` 分割，如果 parts.length === 2 则使用解析后的 host 和 port，否则使用连接默认配置。UDP 发送使用 `socket.send(data, port, host)`。
511	- **代码位置**：`src-electron/main/ipc/networkHandlers.ts:359-371`（地址解析）、`420-436`（UDP 发送）
512	- **新系统对应 feature**：connection feature
513	- **oracle 来源**：代码事实。
514	- **保留建议**：**保留**。UDP 目标地址动态指定是必要能力。
515	
516	#### 11.4 连接 ID 命名规则
517	
518	- **旧行为**：网络连接 ID 由外部（UI/调用方）生成传入。串口使用端口路径（如 `COM3`）作为标识。`connectionTargetsStore` 使用复合 ID：`serial:{portPath}`、`network:{connectionId}`、`network:{connectionId}:{remoteHostId}`。
519	- **代码位置**：`src/stores/connectionTargetsStore.ts:56-121`（ID 生成）
520	- **新系统对应 feature**：connection feature
521	- **oracle 来源**：代码事实。
522	- **保留建议**：**保留命名空间概念，重写编码规则**。`type:id` 命名空间概念合理，具体编码应在设计阶段确定。
523	
524	---
525	
526	## 后续
527	
528	### 行为保留/排除汇总
529	
530	**保留的行为（核心，不可丢失）**：
531	1. 串口四状态生命周期（disconnected → connecting → connected → error）
532	2. 串口配置参数集合 + 每端口独立配置 + 热更新（关闭重开）
533	3. 多串口并发管理
534	4. TCP 客户端连接（setNoDelay、超时、\r\n 分割）
535	5. TCP Server 多客户端管理
536	6. UDP 绑定 + 远程主机列表 + 广播模式
537	7. 网络数据高速存储分流（连接 ID + 帧头匹配 → 文件存储，不转发渲染进程）
538	8. 高速存储文件轮转（大小限制 + 文件数量限制）
539	9. 统一连接目标视图（串口 + 网络合并为 ConnectionTarget）
540	10. 连接统计（bytes/messages/activity）
541	11. 最后使用串口记忆
542	12. 应用退出时关闭所有连接
543	13. TCP \r\n 数据分割
544	
545	**排除的行为**：
546	1. `receivedMessagesMap` / `sentMessagesMap` 100 条内存历史（调试功能，receive feature 有独立存储）
547	2. 自动连接/自动重连（类型定义存在但未实现）
548	3. 串口端口热插拔自动检测（无实现）
549	4. Windows 注册表 PowerShell 枚举方式（应迁移到 serialport 库原生 list）
550	5. `clearBuffer` 只重置计数器不真正清空缓冲区（行为名不副实，新系统应明确语义）
551	6. `autoOpen: false` 配置项（始终 false，新系统不需要此配置）
552	
553	**需重新设计的行为**：
554	1. 连接配置持久化方式（从 localStorage 迁移到新持久化层）
555	2. 网络连接配置持久化（旧系统无持久化，新系统应增加）
556	3. IPC 通道命名和 preload 桥接方式
557	4. 连接目标 ID 编码规则
558	5. TCP \r\n 分割是否参数化
559	6. UDP 远程主机管理的持久化
560	7. 高速存储配置的持久化
561	
562	### oracle 来源评估
563	
564	| 行为领域 | oracle 可信度 | 说明 |
565	|---|---|---|
566	| 串口连接生命周期 | 高 | 代码事实完整，四状态模型清晰 |
567	| TCP/UDP 连接管理 | 高 | main 进程代码完整，类型定义完备 |
568	| 高速存储分流 | 高 | 代码链路完整：shouldStore → storeData → 文件轮转 |
569	| 连接目标统一视图 | 高 | connectionTargetsStore 完整实现 |
570	| 自动重连 | 低 | 仅有类型定义，无实现代码 |
571	| UI 状态展示 | 中 | store 有状态和计算属性，但缺少 UI 组件代码佐证 |
572	
573	### 新系统 feature 映射
574	
575	| 旧行为 | 新系统 feature |
576	|---|---|
577	| 串口枚举/连接/断开/配置 | connection feature |
578	| TCP/UDP/TCP Server 连接管理 | connection feature |
579	| 数据收发通道（IPC 事件） | connection feature（platform facade） |
580	| TCP \r\n 分割 | connection feature 或 receive feature（待设计确定） |
581	| 高速存储分流 + 文件管理 | storage feature |
582	| 统一连接目标视图 | connection feature（selector）+ send feature |
583	| 连接统计 | connection feature（selector） |
584	| 配置持久化 | persistence layer + connection feature |
585	
```

> TOOL

tool_result
id: call_c3c07c5a793b40b79b3aeefc
```
1	# [S004] 旧系统 receive/send 数据流事实提取
2	
3	> 2026-05-19 | 调研 | 进行中
4	
5	## 目标
6	
7	从旧系统代码中提取 receive 和 send 的完整数据流路径、所有可观测业务行为，为重写提供 oracle 基线。
8	
9	---
10	
11	## 一、旧 Receive 完整数据流路径
12	
13	### 1.1 入口：串口/网络数据到达
14	
15	**串口路径**
16	- `serialStore.ts` 监听 `serialAPI.onData` 回调
17	- 收到 `{ portPath, data }` 后调用 `receiveFramesStore.handleReceivedData('serial', portPath, new Uint8Array(data.data))`
18	- 代码位置: `src/stores/serialStore.ts:416`
19	
20	**网络路径**
21	- `netWorkStore.ts` 监听 `networkAPI.onData` 回调
22	- 收到 `{ connectionId, data, timestamp }` 后调用 `receiveFramesStore.handleReceivedData('network', connectionId, uint8Data)`
23	- 代码位置: `src/stores/netWorkStore.ts:212`
24	
25	### 1.2 统一入口：handleReceivedData（renderer 侧）
26	
27	- 位置: `receiveFramesStore.ts:852-892`
28	- 行为: **串行处理锁** — 如果正在处理数据（`processingLock`），新数据进入 `pendingProcessQueue` 排队
29	- 串行保证: 同一时刻只有一个 `processDataInternal` 在执行，队列中的请求按 FIFO 顺序处理
30	
31	### 1.3 内部处理：processDataInternal
32	
33	位置: `receiveFramesStore.ts:1005-1144`
34	
35	完整步骤链：
36	
37	1. **全局统计更新**（同步）
38	   - `globalStatsStore.incrementReceivedPackets()` — 接收包计数 +1
39	   - `globalStatsStore.addReceivedBytes(data.length)` — 接收字节累加
40	
41	2. **SCOE 帧分流**（条件分支）
42	   - 条件: `sourceId === 'scoe-tcp-server'`
43	   - 调用 `handleScoeFrame(data)` 尝试作为 SCOE 帧处理
44	   - 如果 SCOE 处理成功，直接 return，不再走通用帧匹配路径
45	   - SCOE 处理包括: isScoeFrame 检测 → checksum 校验 → 参数解析 → scoeCommandExecutor.executeCommand → addReceiveData 记录
46	
47	3. **主进程帧匹配与解析**（IPC 调用）
48	   - 调用 `receiveAPI.handleReceivedData(source, sourceId, data)` → 通过 `window.electron.receive.handleReceivedData` → IPC 到主进程
49	   - 主进程处理链（`receiveHandlers.ts:32-160`）：
50	     a. 从 `receiveConfigCache` 获取缓存的帧模板、映射、分组
51	     b. `createDataPacket(source, sourceId, data)` 创建数据包对象
52	     c. `matchDataToFrame(packet, frames)` 执行帧匹配（基于 matchRules）
53	     d. `processReceivedData(packet, matchResult, mappings, groups)` 提取字段值
54	     e. `applyDataProcessResult(processResult, updatedGroups)` 应用到分组副本
55	   - 返回给 renderer: `{ success, updatedGroups, updatedDataItems, recentPacket, frameStats, errors }`
56	
57	4. **失败处理**（result.success === false）
58	   - `globalStatsStore.incrementUnmatchedFrames()` — 未匹配帧计数 +1
59	   - 如果包含解析错误: `globalStatsStore.incrementFrameParseErrors()` — 解析错误计数 +1
60	   - 记录到 `recentPackets`
61	
62	5. **成功处理**（result.success === true）
63	   - `globalStatsStore.incrementMatchedFrames()` — 匹配成功帧计数 +1
64	   - 记录到 `recentPackets`（最多 100 条，FIFO）
65	   - 更新 `frameDataCache`（fieldId → value 映射）
66	   - **增量更新数据项** — 遍历 `updatedDataItems`，跳过表达式字段，直接赋值 `dataItem.value` 和 `dataItem.displayValue`
67	   - **表达式计算** — `frameExpressionManager.calculateAndApplyReceiveFrame(frameId)` 同步计算间接字段
68	   - **星座图数据收集** — 异步调用 `collectConstellationData`，将 bytes 类型字段数据送入 dataDisplayStore
69	   - **帧统计更新** — `frameStats` Map 中累加 `totalReceived`、更新 `lastReceiveTime`
70	   - **触发条件检查** — 调用 `checkTriggerConditions(frameId, sourceId, updatedDataItems)` → 通知 sendTasksStore
71	
72	### 1.4 配置同步到主进程
73	
74	- 位置: `receiveFramesStore.ts:235-267`
75	- 触发方式: watch `configForWatch`（排除 value/displayValue 的 groups + mappings 变化）
76	- 行为:
77	  - 1 秒防抖后调用 `saveConfig()` 持久化
78	  - 500ms 防抖后调用 `syncConfigToMainProcess()` 更新主进程缓存
79	  - 帧模板变化时也触发 `debouncedSyncCache`
80	
81	---
82	
83	## 二、旧 Send 完整数据流路径
84	
85	### 2.1 任务创建
86	
87	入口: `useSendTaskManager` → `useSendTaskCreator`
88	
89	四种任务类型:
90	1. **顺序发送** (`createSequentialTask`) — 一组帧实例按顺序发送，发完即止
91	2. **定时发送** (`createTimedTask`) — 参数: instances, sendInterval, repeatCount, isInfinite
92	3. **条件触发发送** (`createTriggeredTask`) — 参数: instances, sourceId, triggerFrameId, conditions, continueListening
93	4. **时间触发发送** (`createTimedTriggeredTask`) — 参数: instances, executeTime, isRecurring, recurringType, recurringInterval, endTime
94	
95	所有类型创建后存入 `sendTasksStore.addTask()`，状态初始为 `idle`。
96	
97	### 2.2 任务启动
98	
99	入口: `useSendTaskExecutor.startTask(taskId)` — 根据 `task.type` 分发
100	
101	#### 顺序发送 (startSequentialTask)
102	- 初始化帧实例缓存（deepClone）
103	- 状态 → `running`
104	- 调用 `processMultipleInstances(taskId)` — 按顺序逐个发送
105	- 每个实例发送前后更新实例级 status（idle→running→completed/error）
106	- 完成后状态 → `completed`，清理缓存
107	
108	#### 定时发送 (startTimedTask)
109	- 初始化帧实例缓存
110	- 状态 → `running`
111	- 使用 `createTimedSender` 通用定时器：
112	  - 首次立即发送一轮所有实例
113	  - 之后按 `sendInterval` 设置 interval 定时器
114	  - 每轮发送前检查 `isTaskStillRunning`、是否达到 `repeatCount`
115	  - 支持参数变化：`updateCachedInstanceFields(cachedInstance, currentCount)` 按轮次索引更新字段值
116	  - `isInfinite` 模式：只更新计数不设上限
117	  - 达到上限后状态 → `completed`
118	- 连接断开时状态 → `paused`（`sendFrameToTarget` 中检测）
119	
120	#### 条件触发发送 (startTriggeredTask)
121	- 初始化帧实例缓存
122	- 状态 → `waiting-trigger`
123	- 注册触发监听器: `sendTasksStore.registerTaskTriggerListener(taskId, config)`
124	- 监听器在 `useSendTaskTriggerListener` 中管理
125	
126	#### 时间触发发送 (startTimedTriggeredTask)
127	- 初始化帧实例缓存
128	- 使用 `createScheduledExecutor`：
129	  - 状态 → `waiting-schedule`
130	  - 计算下次执行时间（支持一次性 / 重复: second/minute/hour/daily/weekly/monthly）
131	  - 到达时间后状态 → `running`，执行一轮发送
132	  - 重复模式下计算下次时间，状态回到 `waiting-schedule`
133	  - 超过 endTime 或一次性完成后状态 → `completed`
134	
135	### 2.3 单帧发送流程
136	
137	入口: `useUnifiedSender.sendFrameInstance(targetId, frameInstance)`
138	
139	1. **表达式计算** — 如果帧有表达式字段，先 `calculateAndApplySendFrame` 计算
140	2. **倍率应用** — 非 bytes 类型且 factor !== 1 时，`value = Number(value) * factor`
141	3. **序列化** — `frameToBuffer(frameInstanceTemp)` 转为 Uint8Array
142	4. **路由发送** — 根据 `targetId` 格式解析目标类型：
143	   - `serial:COM1` → `serialAPI.sendData(portPath, data)`
144	   - `network:tcp-xxx` → `networkAPI.send(connectionId, data)` 或带 targetHost 的 UDP 发送
145	5. **统计更新**（异步 setTimeout）：
146	   - 成功: `sendFrameInstancesStore.updateSendStatsCache(instance)` — 缓存中 sendCount++, lastSentAt 更新
147	   - 成功: `globalStatsStore.incrementSentPackets()` + `addSentBytes(data.length)`
148	   - SCOE UDP 目标: `scoeStore.addSendData(hexString)` 记录发送的十六进制
149	   - 失败: `globalStatsStore.incrementCommunicationErrors()`
150	
151	### 2.4 触发条件匹配流程
152	
153	**receive 到 send 的桥接路径:**
154	
155	1. `processDataInternal` 成功后 → `checkTriggerConditions(frameId, sourceId, updatedDataItems)` (receiveFramesStore.ts:1186)
156	2. → `sendTasksStore.handleFrameReceived(frameId, sourceId, dataItems)` (sendTasksStore.ts:556)
157	3. → `triggerListener.handleFrameReceived(frameId, sourceId, updatedDataItems)` (useSendTaskTriggerListener.ts:70)
158	
159	**条件评估** (`evaluateTriggerConditions`):
160	- 遍历所有活跃监听器，匹配 `triggerFrameId === frameId` 且 `sourceId === sourceId`
161	- 检查任务状态是否为 `waiting-trigger`
162	- 空条件数组 = 接收到帧即触发
163	- 有条件时: 通过 `receiveFramesStore.mappings` 查找 `fieldId → dataItemId` 映射
164	- 支持 AND/OR 逻辑组合，条件操作符: equals / not_equals / greater / less / contains
165	- 所有值比较都用 String() 或 Number() 转换后比较
166	
167	**触发执行** (`executeTriggerTask`):
168	- 可选 responseDelay 延迟
169	- 单实例: `processInstance(taskId, 0, 1, true)`
170	- 多实例: `processMultipleInstances(taskId)`
171	- 执行后清理实例缓存
172	- `continueListening === false`: 注销监听器，任务 → completed
173	- `continueListening === true`: 保持监听，下次匹配可再次触发
174	
175	### 2.5 任务控制
176	
177	入口: `useSendTaskController`
178	
179	- `stopTask(taskId)` — 清理定时器 + 触发监听器，状态 → completed
180	- `pauseTask(taskId)` — 仅更新状态 → paused（定时器实际未暂停，依赖 executeOnce 中 isTaskStillRunning 检查）
181	- `resumeTask(taskId)` — 状态 → running（注意: 暂停后的定时器恢复逻辑不完整，代码注释承认这一点）
182	- `stopAllTasks()` — 遍历所有 running/paused/waiting-trigger 任务调用 stopTask
183	- `forceCleanupTask(taskId)` — 强制清理定时器 + 监听器，状态 → error
184	
185	---
186	
187	## 三、receiveFramesStore 职责清单
188	
189	### 3.1 状态（ref）
190	| 状态 | 类型 | 用途 |
191	|------|------|------|
192	| groups | DataGroup[] | 数据分组，包含 dataItems（带 value/displayValue） |
193	| mappings | FrameFieldMapping[] | 帧.字段 → 分组.数据项 映射关系 |
194	| frameStats | Map<string, ReceiveFrameStats> | 每帧统计（totalReceived, lastReceiveTime, checksumFailures, errorCount） |
195	| selectedFrameId | string | UI 当前选中帧 |
196	| selectedGroupId | number | UI 当前选中分组 |
197	| isLoading | boolean | 加载状态 |
198	| recentPackets | ReceivedDataPacket[] | 最近 100 个数据包（用于调试/监控） |
199	| frameDataCache | Map<string, Map<string, unknown>> | 帧ID → (fieldId → value) 快速缓存，供表达式计算和条件检查 |
200	| processingLock | boolean | 数据处理串行锁 |
201	| pendingProcessQueue | array | 排队等待处理的数据包 |
202	
203	### 3.2 计算属性（computed）
204	| 属性 | 用途 |
205	|------|------|
206	| receiveFrames | 过滤 direction === 'receive' 的帧模板 |
207	| receiveFrameOptions | 帧选项列表（id, name, fields） |
208	| selectedFrameDataItems | 选中帧的映射 + 数据项联合信息 |
209	| selectedGroup | 当前选中分组 |
210	| availableReceiveFrameOptions | 帧选项（label/value 格式，用于下拉） |
211	| getAvailableFrameFieldOptions | 指定帧的已映射字段选项 |
212	| allReceiveFrameData | frameDataCache 的只读引用 |
213	| directDataFrames | 只含直接数据字段的接收帧副本（过滤 indirect） |
214	| configForWatch | 排除 value/displayValue 的配置快照（用于自动保存） |
215	
216	### 3.3 Watcher
217	| watch 目标 | 行为 |
218	|------------|------|
219	| configForWatch | 配置变化时 1s 防抖保存 + 500ms 防抖同步主进程缓存 |
220	| frameTemplateStore.frames | 帧模板变化时同步主进程缓存 |
221	
222	### 3.4 Actions（方法）
223	| 方法 | 职责 |
224	|------|------|
225	| loadConfig | 从 dataStorageAPI 加载 groups + mappings，验证映射，同步主进程 |
226	| saveConfig | 持久化 groups + mappings |
227	| exportConfig | 导出配置对象 |
228	| importConfig | 导入配置（验证、清空、重建、同步主进程） |
229	| validateMappings | IPC 调用主进程验证映射完整性 |
230	| selectFrame / selectGroup | UI 选择 |
231	| addGroup / removeGroup / updateGroup | 分组 CRUD |
232	| addDataItemToGroup / updateDataItem / removeDataItem | 数据项 CRUD |
233	| addMapping / removeMapping | 映射关系 CRUD |
234	| toggleDataItemVisibility / toggleDataItemFavorite | UI 状态切换 |
235	| clearDataItemValues | 清空所有数据项的 value/displayValue |
236	| handleReceivedData | 统一数据接收入口（串行锁 + 内部处理） |
237	| processDataInternal | 核心数据处理（统计→SCOE→帧匹配→更新→表达式→星座图→触发） |
238	| handleScoeFrame | SCOE 帧专属处理 |
239	| checkTriggerConditions | receive→send 触发桥接 |
240	| collectConstellationData | 星座图数据收集 |
241	| updateFrameStats | 帧级统计更新 |
242	| clearReceiveStats | 清空统计和缓存 |
243	| getRecentPackets | 获取最近数据包（可按 source/sourceId 过滤） |
244	| findOrphanedDataItems | 查找无映射的孤立数据项 |
245	| removeInvalidMappings | 清理无效映射 |
246	| removeOrphanedDataItems | 清理孤立数据项 |
247	| moveVisibleDataItemUp / moveVisibleDataItemDown | 可见项排序 |
248	| syncConfigToMainProcess | 同步配置到主进程缓存 |
249	| debouncedSaveConfig / debouncedSyncCache | 防抖保存/同步 |
250	
251	---
252	
253	## 四、sendTasksStore 职责清单
254	
255	### 4.1 状态
256	| 状态 | 用途 |
257	|------|------|
258	| tasks | shallowRef<SendTask[]> — 所有任务 |
259	| statusIndexes | Map<TaskStatus, Set<string>> — 按状态索引，O(1) 查询 |
260	| taskMap | Map<string, SendTask> — ID 到任务的快速映射 |
261	| progressCache / configCache | Map — 批量更新缓存（1s 同步到 store） |
262	
263	### 4.2 计算属性
264	| 属性 | 用途 |
265	|------|------|
266	| activeTasks | running + paused + waiting-trigger + waiting-schedule |
267	| runningTasks | 仅 running |
268	| completedTasks | 仅 completed |
269	| errorTasks | 仅 error |
270	| waitingTriggerTasks | 仅 waiting-trigger |
271	
272	### 4.3 Actions
273	| 方法 | 职责 |
274	|------|------|
275	| addTask | 创建任务，更新索引 |
276	| getTaskById / getTaskByName | 查询 |
277	| updateTaskStatus | 状态转换（含索引更新），completed 时自动 removeTask |
278	| updateTask | 通用更新（配置更新走缓存） |
279	| removeTask | 删除任务 |
280	| clearCompletedTasks / clearErrorTasks / clearAllTasks | 批量清理 |
281	| stopAllRunningTasks | 批量暂停 |
282	| updateTaskProgressCached | 进度缓存更新（1s 批量同步） |
283	| updateTaskConfigCached | 配置缓存更新 |
284	| forceSyncCache | 强制同步缓存 |
285	| syncCacheToStore | 批量同步缓存到 store |
286	| registerTaskTriggerListener | 注册触发监听器 |
287	| unregisterTaskTriggerListener | 注销触发监听器 |
288	| handleFrameReceived | 透传给 triggerListener |
289	| getActiveTriggerListeners / getTriggerListenerStats | 监听器查询 |
290	
291	---
292	
293	## 五、sendFrameInstancesStore 职责清单
294	
295	### 5.1 核心职责
296	- 帧实例 CRUD（创建、复制、删除、更新、排序）
297	- 帧实例收藏管理
298	- 帧实例编辑（localInstance 编辑副本、hexValues、保存）
299	- 帧实例导入/导出（JSON）
300	- 帧模板更新时联动更新实例
301	- 触发配置管理（条件触发、时间触发）
302	- 发送统计管理（sendCount, lastSentAt 缓存）
303	
304	### 5.2 触发配置状态
305	- `triggerType`: 'condition' | 'time'
306	- 条件触发: sourceId, triggerFrameId, conditions, continueListening
307	- 时间触发: executeTime, isRecurring, recurringType, recurringInterval, endTime
308	- `responseDelay`: 触发后延迟执行时间
309	
310	---
311	
312	## 六、全局统计（globalStatsStore）
313	
314	| 统计项 | 更新位置 |
315	|--------|---------|
316	| sentPackets | useUnifiedSender.sendFrameInstance 成功后 |
317	| receivedPackets | receiveFramesStore.processDataInternal 入口 |
318	| sentBytes | useUnifiedSender.sendFrameInstance 成功后 |
319	| receivedBytes | receiveFramesStore.processDataInternal 入口 |
320	| matchedFrames | receiveFramesStore.processDataInternal 成功后 |
321	| unmatchedFrames | receiveFramesStore.processDataInternal 失败后 |
322	| communicationErrors | useUnifiedSender.sendFrameInstance 失败后 |
323	| frameParseErrors | receiveFramesStore.processDataInternal 解析错误时 |
324	| systemStats (时间/位置) | 每秒更新，表达式系统可消费 |
325	
326	统计项全部为累加计数器，resetStats 一次性清零。所有统计通过 `availableStats` computed 暴露给表达式系统。
327	
328	---
329	
330	## 七、可观测业务行为清单
331	
332	### R-01: 串口数据接收并自动匹配帧
333	
334	**旧行为:** 串口收到原始字节 → 自动按帧模板匹配 → 匹配成功则解析字段值 → 更新 UI 数据项
335	
336	**代码位置:**
337	- 入口: `serialStore.ts:416` → `receiveFramesStore.handleReceivedData`
338	- 主进程: `receiveHandlers.ts:32-160`
339	- 匹配: `dataProcessor.ts:54-113` (`matchDataToFrame`)
340	- 解析: `dataProcessor.ts:440-566` (`processReceivedData`)
341	- 字段值提取: `dataProcessor.ts:199-430` (`extractFieldValue`)
342	
343	**新系统对应 feature:** receive feature
344	
345	**oracle 来源:** 可录制 — 固定帧模板 + 固定输入字节 → 验证输出字段值
346	
347	**保留建议:** 保留。帧匹配和字段解析是核心数据流。
348	
349	---
350	
351	### R-02: 网络数据接收并自动匹配帧
352	
353	**旧行为:** 网络连接收到原始字节 → 同串口路径处理（区分 sourceId）
354	
355	**代码位置:**
356	- 入口: `netWorkStore.ts:212` → `receiveFramesStore.handleReceivedData`
357	- 后续路径同 R-01
358	
359	**新系统对应 feature:** receive feature
360	
361	**oracle 来源:** 同 R-01
362	
363	**保留建议:** 保留。
364	
365	---
366	
367	### R-03: 接收数据串行处理（处理锁）
368	
369	**旧行为:** 同一时刻只有一个数据处理流程在执行，后续数据排队 FIFO 处理
370	
371	**代码位置:** `receiveFramesStore.ts:806-892` (`processingLock` + `pendingProcessQueue`)
372	
373	**新系统对应 feature:** receive feature（是否需要串行锁取决于新架构）
374	
375	**oracle 来源:** 代码逻辑验证
376	
377	**保留建议:** 需讨论。串行保证防止竞态，但可能影响高频场景吞吐。新系统应评估是否需要锁、用锁粒度多大。
378	
379	---
380	
381	### R-04: SCOE 帧分流处理
382	
383	**旧行为:** sourceId === 'scoe-tcp-server' 时，数据优先走 SCOE 专属处理路径（识别→校验→参数解析→指令执行→记录）。SCOE 处理成功则不走通用帧匹配。
384	
385	**代码位置:** `receiveFramesStore.ts:899-1000` (`handleScoeFrame`)
386	
387	**新系统对应 feature:** 指令接入 feature
388	
389	**oracle 来源:** SCOE 帧配置文件 + 录制的输入字节
390	
391	**保留建议:** 保留 SCOE 帧识别和校验行为。但 SCOE 专属路径应统一到指令接入 feature，不复用旧 SCOE 独立模块结构。
392	
393	---
394	
395	### R-05: 数据项值增量更新
396	
397	**旧行为:** 帧匹配成功后，只更新有映射的数据项的 value 和 displayValue，不覆盖整个 groups。跳过表达式字段。
398	
399	**代码位置:** `receiveFramesStore.ts:1076-1089`
400	
401	**新系统对应 feature:** receive feature
402	
403	**oracle 来源:** 固定帧模板 + 映射 + 输入字节 → 验证各数据项值
404	
405	**保留建议:** 保留。增量更新是性能关键。
406	
407	---
408	
409	### R-06: 表达式字段计算
410	
411	**旧行为:** 直接字段值更新后，同步计算该帧上的表达式字段（indirect 字段），并更新对应数据项的 value/displayValue。
412	
413	**代码位置:** `receiveFramesStore.ts:1092-1099`，委托给 `useFrameExpressionManager`
414	
415	**新系统对应 feature:** 表达式引擎（shared/）+ receive feature 调用
416	
417	**oracle 来源:** 配置表达式 + 输入直接字段值 → 验证间接字段输出
418	
419	**保留建议:** 保留。新系统表达式引擎已在 shared/ 实现。
420	
421	---
422	
423	### R-07: 帧级统计（每帧接收计数、最后接收时间）
424	
425	**旧行为:** 每次帧匹配成功后，frameStats Map 中该帧的 totalReceived 累加，lastReceiveTime 更新。
426	
427	**代码位置:** `receiveFramesStore.ts:1108-1125`
428	
429	**新系统对应 feature:** receive feature
430	
431	**oracle 来源:** 发送 N 帧后验证统计数据
432	
433	**保留建议:** 保留。
434	
435	---
436	
437	### R-08: 全局统计（收发包数、字节数、匹配率、错误率）
438	
439	**旧行为:** 全局累加统计，分四类: 通信统计（收发包/字节）、帧匹配统计（匹配/未匹配）、错误统计（通信错误/解析错误）、系统统计（运行时间/位置）。
440	
441	**代码位置:** `globalStatsStore.ts`
442	
443	**新系统对应 feature:** 全局统计（可能是独立 feature 或 receive/send 的公共能力）
444	
445	**oracle 来源:** 发送/接收固定数量数据后验证统计值
446	
447	**保留建议:** 保留。
448	
449	---
450	
451	### R-09: 最近数据包记录（调试用）
452	
453	**旧行为:** 保留最近 100 个数据包（无论匹配成功或失败），可按 source/sourceId 过滤查询。
454	
455	**代码位置:** `receiveFramesStore.ts:134-143, 1248-1261`
456	
457	**新系统对应 feature:** receive feature 的调试/监控能力
458	
459	**oracle 来源:** UI 观察验证
460	
461	**保留建议:** 保留。
462	
463	---
464	
465	### R-10: 配置自动保存和主进程同步
466	
467	**旧行为:** groups/mappings 变化时 1s 防抖保存到本地存储，500ms 防抖同步到主进程缓存。帧模板变化也触发主进程同步。
468	
469	**代码位置:** `receiveFramesStore.ts:168-267`
470	
471	**新系统对应 feature:** receive feature 的持久化层
472	
473	**oracle 来源:** 修改配置后重启验证持久化
474	
475	**保留建议:** 保留。新系统持久化策略可能不同（FeaturePersistence 已实现），但行为需等价。
476	
477	---
478	
479	### R-11: 映射关系验证和孤立数据项清理
480	
481	**旧行为:** 导入配置后验证映射完整性。提供 `findOrphanedDataItems`、`removeInvalidMappings`、`removeOrphanedDataItems` 方法。
482	
483	**代码位置:** `receiveFramesStore.ts:614-803`
484	
485	**新系统对应 feature:** receive feature 配置管理
486	
487	**oracle 来源:** 构造含孤立项的配置 → 调用清理方法 → 验证结果
488	
489	**保留建议:** 保留。
490	
491	---
492	
493	### R-12: 星座图数据收集
494	
495	**旧行为:** 帧匹配成功后，如果数据项类型为 bytes 且有映射关系，收集数据到 dataDisplayStore 供星座图可视化。
496	
497	**代码位置:** `receiveFramesStore.ts:1149-1181`
498	
499	**新系统对应 feature:** 可视化 feature（独立于 receive）
500	
501	**oracle 来源:** 录制 bytes 类型字段的输入数据 → 验证星座图数据
502	
503	**保留建议:** 保留行为，但新系统中星座图收集由可视化 feature 消费 receive 数据，不是 receive 自己做。
504	
505	---
506	
507	### R-13: 标签显示（labelOptions 匹配）
508	
509	**旧行为:** 数据项启用 `useLabel` 时，解析后的 displayValue 会与 `labelOptions` 匹配，匹配到则显示标签而非原始值。匹配通过十六进制归一化比较。
510	
511	**代码位置:** `dataProcessor.ts:523-533`
512	
513	**新系统对应 feature:** receive feature 数据展示
514	
515	**oracle 来源:** 配置 labelOptions + 发送匹配值 → 验证显示标签
516	
517	**保留建议:** 保留。
518	
519	---
520	
521	### R-14: 倍率应用
522	
523	**旧行为:** 字段有 factor 且不等于 1 时，解析后的值乘以 factor，保留最多 5 位小数。send 方向在序列化前也应用倍率。
524	
525	**代码位置:**
526	- receive: `dataProcessor.ts:121-134` (`applyFactor`)
527	- send: `useUnifiedSender.ts:88-98`
528	
529	**新系统对应 feature:** 帧 field 定义的一部分，shared/ 纯函数
530	
531	**oracle 来源:** 配置 factor + 输入原始值 → 验证输出
532	
533	**保留建议:** 保留。
534	
535	---
536	
537	### R-15: 直接/间接数据字段区分
538	
539	**旧行为:** 帧匹配时只使用 `dataParticipationType === 'direct'`（或未设置默认为 direct）的字段。间接字段（indirect / 表达式字段）不参与帧匹配，通过表达式计算得出。
540	
541	**代码位置:** `receiveFramesStore.ts:823-844` (`directDataFrames` computed)
542	
543	**新系统对应 feature:** receive feature 帧匹配
544	
545	**oracle 来源:** 配置含 direct + indirect 字段的帧 → 发送数据 → 验证只有 direct 字段参与匹配
546	
547	**保留建议:** 保留。
548	
549	---
550	
551	### R-16: receive→send 条件触发桥接
552	
553	**旧行为:** 帧匹配成功后，将 frameId + sourceId + 更新的数据项传给 sendTasksStore → triggerListener，遍历所有活跃监听器匹配条件，满足则触发发送任务执行。
554	
555	**代码位置:**
556	- 桥接入口: `receiveFramesStore.ts:1186-1231` (`checkTriggerConditions`)
557	- 条件评估: `useSendTaskTriggerListener.ts:100-158`
558	- 单条件操作符: `useSendTaskTriggerListener.ts:189-218`
559	
560	**新系统对应 feature:** receive feature 发出事件 → task feature 消费
561	
562	**oracle 来源:** 配置触发条件 + 发送满足/不满足条件的帧 → 验证是否触发
563	
564	**保留建议:** 保留。但新系统中条件匹配逻辑归 shared/ 纯函数，触发行为归 task feature。
565	
566	---
567	
568	### R-17: 条件触发支持 AND/OR 逻辑组合
569	
570	**旧行为:** 多条件支持 AND/OR 逻辑运算符连接，支持短路求值。
571	
572	**代码位置:** `useSendTaskTriggerListener.ts:113-158`
573	
574	**新系统对应 feature:** shared/ 条件匹配纯函数
575	
576	**oracle 来源:** 构造 AND/OR 条件组合 → 输入不同值组合 → 验证触发结果
577	
578	**保留建议:** 保留。
579	
580	---
581	
582	### S-01: 单帧发送（用户手动发送）
583	
584	**旧行为:** 用户选择帧实例和目标连接 → 表达式计算 → 倍率应用 → 序列化 → 按目标类型路由（串口/网络 TCP/UDP）→ 更新统计。
585	
586	**代码位置:** `useUnifiedSender.ts:69-178` (`sendFrameInstance`)
587	
588	**新系统对应 feature:** send feature
589	
590	**oracle 来源:** 固定帧实例 + 目标 → 捕获发送的字节
591	
592	**保留建议:** 保留。
593	
594	---
595	
596	### S-02: 顺序发送任务
597	
598	**旧行为:** 一组帧实例按顺序逐个发送，每个实例独立状态追踪（running/completed/error），全部完成后任务标记 completed。
599	
600	**代码位置:** `useSendTaskExecutor.ts:490-537` (`startSequentialTask`)
601	
602	**新系统对应 feature:** task feature
603	
604	**oracle 来源:** 创建顺序任务 + 验证发送顺序和完成状态
605	
606	**保留建议:** 保留。
607	
608	---
609	
610	### S-03: 定时发送任务
611	
612	**旧行为:** 按固定间隔重复发送一组帧实例。支持有限次数和无限循环。支持参数变化（每轮更新字段值）。首次立即发送。
613	
614	**代码位置:** `useSendTaskExecutor.ts:542-728` (`createTimedSender` + `startTimedTask`)
615	
616	**新系统对应 feature:** task feature
617	
618	**oracle 来源:** 创建定时任务 + 验证间隔和次数
619	
620	**保留建议:** 保留。
621	
622	---
623	
624	### S-04: 定时任务参数变化
625	
626	**旧行为:** 帧实例启用 `enableVariation` 时，每轮发送前按 `currentVariationIndex` 更新字段值为 `fieldVariations[roundIndex]` 中的值。
627	
628	**代码位置:** `useSendTaskExecutor.ts:80-101` (`updateCachedInstanceFields`)
629	
630	**新系统对应 feature:** task feature
631	
632	**oracle 来源:** 配置参数变化 + 验证每轮发送的字段值
633	
634	**保留建议:** 保留。
635	
636	---
637	
638	### S-05: 条件触发发送任务
639	
640	**旧行为:** 任务进入 `waiting-trigger` 状态，注册触发监听器。receive 数据匹配到指定帧 + 条件满足后，按 responseDelay 延迟后执行发送。支持 `continueListening` 控制是否持续监听。
641	
642	**代码位置:** `useSendTaskExecutor.ts:733-789` + `useSendTaskTriggerListener.ts:223-306`
643	
644	**新系统对应 feature:** task feature
645	
646	**oracle 来源:** 配置触发条件 + 发送满足条件的帧 → 验证触发和发送
647	
648	**保留建议:** 保留。
649	
650	---
651	
652	### S-06: 时间触发发送任务
653	
654	**旧行为:** 指定执行时间（一次性或重复），到达时间后发送一组帧实例。重复支持 second/minute/hour/daily/weekly/monthly 间隔。支持 endTime 限制。
655	
656	**代码位置:** `useSendTaskExecutor.ts:794-976` (`createScheduledExecutor` + `startTimedTriggeredTask`)
657	
658	**新系统对应 feature:** task feature
659	
660	**oracle 来源:** 设置近未来时间 → 验证触发执行
661	
662	**保留建议:** 保留。
663	
664	---
665	
666	### S-07: 任务暂停/恢复
667	
668	**旧行为:** pause 更新状态为 paused，但定时器未真正暂停（依赖执行函数中 isTaskStillRunning 检查跳过执行）。resume 更新状态为 running，但定时器恢复逻辑不完整（代码注释承认这一点）。
669	
670	**代码位置:** `useSendTaskController.ts:70-117`
671	
672	**新系统对应 feature:** task feature
673	
674	**oracle 来源:** 暂停/恢复后验证任务行为
675	
676	**保留建议:** 保留需求，但新系统应正确实现暂停/恢复。旧行为是已知缺陷。
677	
678	---
679	
680	### S-08: 任务停止
681	
682	**旧行为:** 停止任务时清理定时器 + 触发监听器，状态 → completed（注意：不是 cancelled，是 completed）。
683	
684	**代码位置:** `useSendTaskController.ts:26-65`
685	
686	**新系统对应 feature:** task feature
687	
688	**oracle 来源:** 停止后验证清理和状态
689	
690	**保留建议:** 保留。新系统应区分 completed 和 stopped/cancelled。
691	
692	---
693	
694	### S-09: 连接断开自动暂停
695	
696	**旧行为:** 发送帧时如果目标连接不可用（`isTargetAvailable` 返回 false），自动将任务状态改为 paused 并记录原因。
697	
698	**代码位置:** `useSendTaskExecutor.ts:233-237` (`sendFrameToTarget`)
699	
700	**新系统对应 feature:** task feature + connection feature 协同
701	
702	**oracle 来源:** 发送中断开连接 → 验证任务状态变为 paused
703	
704	**保留建议:** 保留。
705	
706	---
707	
708	### S-10: 发送统计（实例级 sendCount/lastSentAt）
709	
710	**旧行为:** 每次发送成功后，帧实例的 sendCount +1，lastSentAt 更新为当前时间。统计先写入缓存，定时器批量同步到 store。
711	
712	**代码位置:**
713	- 缓存更新: `sendFrameInstancesStore.ts:251-269` (`updateSendStatsCache`)
714	- 批量同步: `sendFrameInstancesStore.ts:200-249` (`updateSendStats`)
715	
716	**新系统对应 feature:** send feature
717	
718	**oracle 来源:** 发送 N 次 → 验证统计值
719	
720	**保留建议:** 保留。
721	
722	---
723	
724	### S-11: SCOE UDP 发送记录
725	
726	**旧行为:** 如果发送目标是 `network:scoe-udp:scoe-udp-remote`，发送成功后额外将发送数据以十六进制形式记录到 scoeStore。
727	
728	**代码位置:** `useUnifiedSender.ts:154-159`
729	
730	**新系统对应 feature:** 指令接入 feature
731	
732	**oracle 来源:** 发送 SCOE UDP 帧 → 验证记录
733	
734	**保留建议:** 保留记录行为，但归属指令接入 feature。
735	
736	---
737	
738	### S-12: 实例间延时
739	
740	**旧行为:** 多实例任务发送时，每个实例发送完后可配置延时（`instanceConfig.interval`），最后一个实例不延时。
741	
742	**代码位置:** `useSendTaskExecutor.ts:252-260` (`addInstanceDelay`)
743	
744	**新系统对应 feature:** task feature
745	
746	**oracle 来源:** 多实例任务 + 验证发送间隔
747	
748	**保留建议:** 保留。
749	
750	---
751	
752	### S-13: 帧实例 deepClone 缓存
753	
754	**旧行为:** 任务启动时 deepClone 所有帧实例作为缓存，发送时使用缓存副本，避免修改原始实例。每轮参数变化修改缓存而非原始。
755	
756	**代码位置:** `useSendTaskExecutor.ts:54-75` (`initializeFrameInstanceCache`)
757	
758	**新系统对应 feature:** task feature
759	
760	**oracle 来源:** 任务执行期间修改原始实例 → 验证不影响正在运行的任务
761	
762	**保留建议:** 保留。隔离运行时副本和持久化实例是正确做法。
763	
764	---
765	
766	### S-14: 任务进度追踪
767	
768	**旧行为:** 实时追踪 currentCount（当前发送轮次/帧数）、totalCount、percentage、currentInstanceIndex、nextExecutionTime。进度更新走缓存，1s 批量同步到 store。
769	
770	**代码位置:**
771	- 进度更新: `useSendTaskExecutor.ts` 各处调用 `updateTaskProgressCached`
772	- 批量同步: `sendTasksStore.ts:269-301` (`syncCacheToStore`)
773	
774	**新系统对应 feature:** task feature
775	
776	**oracle 来源:** 运行任务 + 观察 UI 进度
777	
778	**保留建议:** 保留。
779	
780	---
781	
782	### S-15: 触发监听器管理
783	
784	**旧行为:** 触发任务注册监听器后，可查询活跃监听器列表、按帧清理监听器、查询统计信息（总数、按帧/按源分布、有条件/无条件数量）。
785	
786	**代码位置:** `useSendTaskTriggerListener.ts:311-372`
787	
788	**新系统对应 feature:** task feature
789	
790	**oracle 来源:** 注册多个监听器 → 查询统计 → 验证
791	
792	**保留建议:** 保留。
793	
794	---
795	
796	### S-16: 帧实例导入/导出 JSON
797	
798	**旧行为:** 支持将帧实例配置导出为 JSON 文件，以及从 JSON 文件导入配置。
799	
800	**代码位置:** `sendFrameInstancesStore.ts:349`（代理到 `useInstancesImportExport`）
801	
802	**新系统对应 feature:** send feature 持久化
803	
804	**oracle 来源:** 导出 JSON → 导入 → 验证一致性
805	
806	**保留建议:** 保留。
807	
808	---
809	
810	### S-17: 帧模板更新联动实例
811	
812	**旧行为:** 当帧模板定义变更时（字段增删改），已有的帧实例自动同步更新。
813	
814	**代码位置:** `sendFrameInstancesStore.ts:33`（代理到 `useInstanceFrameUpdates`）
815	
816	**新系统对应 feature:** send feature + frame feature 协同
817	
818	**oracle 来源:** 修改帧模板 → 验证实例字段同步
819	
820	**保留建议:** 保留。
821	
822	---
823	
824	### S-18: UDP 远程主机发送
825	
826	**旧行为:** 网络目标格式 `network:xxx:host:port` 时，解析为 UDP 远程主机目标，使用 `networkAPI.send(connectionId, data, targetHost)` 发送。
827	
828	**代码位置:** `useUnifiedSender.ts:118-136`
829	
830	**新系统对应 feature:** send feature（网络发送路由）
831	
832	**oracle 来源:** 配置 UDP 目标 → 验证发送
833	
834	**保留建议:** 保留。
835	
836	---
837	
838	## 八、字段值提取支持的数据类型
839	
840	| 数据类型 | 字节数 | 大/小端 | 倍率 | 标签 |
841	|----------|--------|---------|------|------|
842	| uint8 | 1 | - | 支持 | 支持 |
843	| int8 | 1 | - | 支持 | 支持 |
844	| uint16 | 2 | 支持 | 支持 | 支持 |
845	| int16 | 2 | 支持 | 支持 | 支持 |
846	| uint32 | 4 | 支持 | 支持 | 支持 |
847	| int32 | 4 | 支持 | 支持 | 支持 |
848	| uint64 | 8 | 支持 | 支持 | 支持 |
849	| int64 | 8 | 支持 | 支持 | 支持 |
850	| float | 4 | 支持 | 支持 | 支持 |
851	| double | 8 | 支持 | 支持 | 支持 |
852	| bytes | 变长 | - | - | 支持（ASCII 模式/十六进制） |
853	
854	代码位置: `dataProcessor.ts:199-430` (`extractFieldValue`)
855	
856	---
857	
858	## 九、排除项（旧行为缺陷，不应复制）
859	
860	| 行为 | 问题 | 建议 |
861	|------|------|------|
862	| 暂停后定时器不真正暂停 | 定时器继续触发但被 isTaskStillRunning 跳过 | 新系统应正确实现暂停/恢复 |
863	| 任务停止状态为 completed 而非 cancelled | 用户主动停止和自然完成无法区分 | 新系统应区分 stopped/cancelled/completed |
864	| 串行处理锁可能成为高频瓶颈 | 所有数据源共享一个处理锁 | 新系统应评估是否需要更细粒度锁 |
865	| 旧 SCOE 模块直接耦合 receiveFramesStore | SCOE 逻辑嵌入 receive 主路径 | 新系统统一到指令接入 feature |
866	| globalStats 累加计数器无持久化 | 重启后统计清零 | 是否需要持久化取决于业务需求 |
867	| 条件匹配通过 receiveFramesStore.mappings 查找 fieldId | 触发监听器直接访问 receive store 内部数据 | 新系统应通过公共 API 获取映射信息 |
868	| 进度缓存批量同步 1s 间隔 | 快速完成的任务可能在完成时进度显示不准确 | 新系统应在任务完成时强制同步 |
869	
870	---
871	
872	## 后续
873	
874	1. 将以上行为清单映射到新系统各 feature 的 design spec
875	2. 补充条件触发匹配算法的详细 oracle 测试用例（AND/OR 短路、各种比较操作符）
876	3. 调研旧系统帧匹配算法（matchRules 的具体规则生成逻辑）
877	4. 调研旧系统表达式引擎（`useFrameExpressionManager`）的具体行为，与新 shared/ 引擎对标
878	5. 调研星座图数据收集的下游消费方式（`dataDisplayStore`）
879	
```

> TOOL

tool_use Read
id: call_2d9c97122ef64256bc7e8a1e
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-agent4-expression-parser.md"
}
```

> TOOL

tool_use Read
id: call_da4ebaf690b042bcb738dacc
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-agent5-storage-history-csv.md"
}
```

> TOOL

tool_use Read
id: call_67ff9c778c994e8282fc69af
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-agent6-frame-definition.md"
}
```

> TOOL

tool_result
id: call_67ff9c778c994e8282fc69af
```
1	# [S004] 旧系统帧定义管理行为提取 — Agent6
2	
3	> 2026-05-19 | 调研 | 事实提取完成
4	
5	## 目标
6	
7	调研旧系统的帧定义管理行为，提取所有必须保留的可观测业务行为。只做事实提取，不做设计或实施。
8	
9	---
10	
11	## 1. 帧定义 CRUD 行为
12	
13	### 1.1 创建
14	
15	**旧行为：** 新帧通过 `createEmptyFrame()` 工厂函数生成默认值，填入 `Frame` 结构后通过 `frameTemplateStore.createFrame()` 保存。创建后全量 `saveAll` 到持久化。
16	
17	| 默认字段 | 值 | 位置 |
18	| --- | --- | --- |
19	| id | `nanoid()` | `factories.ts:64` |
20	| lastId | `''` | `factories.ts:65` |
21	| name | `'新帧配置'` | `factories.ts:66` |
22	| description | `''` | `factories.ts:67` |
23	| direction | `'send'` | `factories.ts:68` |
24	| fields | `[]` | `factories.ts:69` |
25	| timestamp | `Date.now()` | `factories.ts:70` |
26	| createdAt / updatedAt | `new Date()` | `factories.ts:71-72` |
27	| isFavorite | `false` | `factories.ts:73` |
28	| options | `{ autoChecksum: true, bigEndian: false, includeLengthField: false }` | `frameDefaults.ts:86-90` |
29	| identifierRules | `[]` | `factories.ts:76` |
30	
31	**必填字段验证：** name 非空 + fields.length > 0（`frameEditorStore.ts:39`）
32	
33	**代码位置：**
34	- 工厂函数：`src/types/frames/factories.ts:63-78`
35	- Store create：`src/stores/frames/frameTemplateStore.ts:43-68`
36	- Editor init：`src/stores/frames/frameEditorStore.ts:63-66`
37	
38	**oracle 来源评估：** 工厂函数 + Store 实现完整，高可信度。
39	
40	**新系统对应 feature：** frame feature 的 createFrame service。
41	
42	**保留建议：** 保留。所有默认值、必填验证、direction 默认 send 等行为用户可观测。
43	
44	---
45	
46	### 1.2 读取（帧列表加载和缓存）
47	
48	**旧行为：**
49	- `fetchFrames()` 调用 `dataStorageAPI.framesConfig.list()` 一次加载全部帧到 `frames: ref<Frame[]>`。
50	- 存储路径：`data/templates/framesConfig`（`configDefaults.ts:6`）。
51	- 通过 `window.electron.dataStorage.framesConfig.list()` 经 IPC 从 main 进程读文件。
52	- 没有分页机制；`FRAMES_PER_PAGE = 20` 只用于 UI 显示（`frameDefaults.ts:126`），不用于数据加载。
53	- `receiveFramesStore` 通过 `computed` 过滤 `frameTemplateStore.frames` 中 `direction === 'receive'` 的帧。
54	- 应用启动时 `useAppLifecycle.ts:48` 加载帧模板。
55	
56	**代码位置：**
57	- `frameTemplateStore.ts:26-39`（fetchFrames）
58	- `receiveFramesStore.ts:270-273`（receiveFrames computed）
59	- `layouts/useAppLifecycle.ts:48`（启动加载）
60	
61	**oracle 来源评估：** 完整代码链路，高可信度。
62	
63	**新系统对应 feature：** frame feature 的 loadFrames / selectFrames。
64	
65	**保留建议：** 保留全量加载、按 direction 过滤、启动时自动加载行为。分页为 UI 展示策略，不是核心行为。
66	
67	---
68	
69	### 1.3 更新
70	
71	**旧行为：**
72	- 编辑器通过 `editorStore.setEditorFrame(frame)` 深拷贝进入编辑状态，保存初始状态 JSON 字符串用于变更检测（`frameEditorStore.ts:43-49`）。
73	- 深度 watch `editorFrame`，通过 JSON 序列化比较检测变更，设置 `hasChanges` 标志（`frameEditorStore.ts:21-32`）。
74	- 字段变更通过 `fieldStore.saveField()` → `editorStore.updateEditorFrame({ fields })` 联动（`frameFieldsStore.ts:267`）。
75	- 保存时：`frameTemplateStore.updateFrame()` 做 `deepClone` + `updatedAt` 时间戳更新 + `saveAll` 全量写回（`frameTemplateStore.ts:70-89`）。
76	- 编辑模式支持 `create` 和 `edit` 两种。编辑模式下 ID 可修改，修改后删除旧 ID 记录（`useFrameEditor.ts:111-112`）。
77	
78	**可编辑字段（通过 Frame 接口 + editor 行为推断）：**
79	- name, description, direction, fields, options, identifierRules, isFavorite, isSCOEFrame
80	- id（在编辑模式下可修改，有冲突检测）
81	
82	**代码位置：**
83	- `frameEditorStore.ts:43-61`（setEditorFrame / updateEditorFrame）
84	- `frameTemplateStore.ts:70-89`（updateFrame）
85	- `useFrameEditor.ts:82-125`（saveFrame 协调逻辑）
86	
87	**oracle 来源评估：** 编辑器 + Store + composable 三层完整，高可信度。
88	
89	**新系统对应 feature：** frame feature 的 updateFrame / editor 状态管理。
90	
91	**保留建议：** 保留深拷贝编辑、变更检测、字段联动更新、ID 修改（含冲突检测）、全量 saveAll。
92	
93	---
94	
95	### 1.4 删除
96	
97	**旧行为：**
98	- `frameTemplateStore.deleteFrame(id)` 调用 `dataStorageAPI.framesConfig.delete(id)` 后本地 filter 移除。
99	- 若删除的是当前选中帧，清空 `selectedFrameId`（`frameTemplateStore.ts:102-103`）。
100	- **无前端确认对话框**（删除操作在 `FrameList.vue:292-310`，只做 try/catch + notify，无 `$q.dialog` 确认）。
101	- **无级联删除**：删除帧定义后，关联的 sendFrameInstances、scoeFrameInstances、receiveConfig mappings 不会被自动清理。`receiveFramesStore.removeInvalidMappings()` 和 `removeOrphanedDataItems()` 可手动清理无效映射，但不在帧删除时自动触发。
102	
103	**代码位置：**
104	- `frameTemplateStore.ts:91-114`
105	- `FrameList.vue:292-310`
106	- `receiveFramesStore.ts:660-754`（手动清理映射）
107	
108	**oracle 来源评估：** Store 实现明确；前端无确认、无级联属于可观测行为。
109	
110	**新系统对应 feature：** frame feature 的 deleteFrame。
111	
112	**保留建议：**
113	- 保留：删除后清空选中状态。
114	- 排除（旧 bug）：无确认对话框。新系统应加确认。
115	- 排除（旧 bug）：无级联清理。新系统应在帧删除时触发关联实例/映射的清理。
116	
117	---
118	
119	### 1.5 复制帧
120	
121	**旧行为：**
122	- `useFrameTemplates.duplicateFrame(id)` 找到原帧，创建深拷贝，name 加 `(副本)` 后缀，删除 id（让 store 生成新 nanoid），isFavorite 重置为 false，timestamp 更新为 `Date.now()`（`useFrameTemplates.ts:61-88`）。
123	
124	**代码位置：** `src/composables/frames/useFrameTemplates.ts:61-88`
125	
126	**保留建议：** 保留。复制是用户常用操作。
127	
128	---
129	
130	### 1.6 收藏
131	
132	**旧行为：**
133	- `frameTemplateStore.toggleFavorite(id)` 切换 `isFavorite` 布尔值并调用 `updateFrame` 持久化（`frameTemplateStore.ts:122-127`）。
134	- 发送帧实例也有独立的 `toggleFavorite`（`sendFrameInsComposable.ts:265-271`）。
135	
136	**保留建议：** 保留帧级和实例级独立收藏。
137	
138	---
139	
140	## 2. 帧实例管理行为
141	
142	### 2.1 sendFrameInstancesStore vs scoeFrameInstancesStore
143	
144	**sendFrameInstancesStore：**
145	- 管理普通发送帧实例，持久化路径 `data/templates/sendInstances`。
146	- 实例通过 `createSendFrameInstance(frame, id)` 从帧模板创建，复制所有字段（包括非 configurable 字段）到实例。
147	- 支持完整 CRUD：create / update / delete / copy / toggleFavorite / moveInstance（拖拽排序）。
148	- 实例编辑使用 localInstance 深拷贝模式 + applyLocalEdit 回写。
149	- 支持批量删除 `deleteInstances(ids)`。
150	- 支持帧定义更新后批量同步到关联实例 `updateInstancesByFrameId(frameId)`。
151	
152	**scoeFrameInstancesStore：**
153	- 管理 SCOE 帧实例，持久化路径 `data/templates/scoeSendInstances`。
154	- 只管理 `isSCOEFrame === true` 且 `direction === 'send'` 的帧。
155	- 发送帧实例 + 接收指令列表（`receiveCommands`）双重管理。
156	- 接收指令结构包含：params（参数列表）、frameInstances（帧实例）、completionConditions（完成条件）、checksums（校验和）。
157	- 实例 ID 为递增数字字符串（不是 nanoid）。
158	
159	**代码位置：**
160	- `src/stores/frames/sendFrameInstancesStore.ts`
161	- `src/composables/frames/sendFrame/sendFrameInsComposable.ts`
162	- `src/stores/frames/scoeFrameInstancesStore.ts`
163	
164	**oracle 来源评估：** 两个 Store 实现完整，行为清晰。
165	
166	**新系统对应 feature：**
167	- sendFrameInstances → send feature（或 frame feature 的实例子域）
168	- scoeFrameInstances → SCOE feature（统一通过指令接入 feature）
169	
170	**保留建议：**
171	- 保留：帧模板到实例的字段复制、localInstance 编辑模式、批量同步更新。
172	- 排除：SCOE 实例的独立管理行为（SCOE 已统一到指令接入 feature）。
173	
174	---
175	
176	### 2.2 实例参数如何覆盖帧定义
177	
178	**旧行为：**
179	- `createSendFrameInstance(frame, id)` 从帧创建实例时：
180	  - 所有字段（包括非 configurable 字段）都复制到实例，保留完整字段列表。
181	  - 每个字段的 `value` 初始化为 `field.defaultValue || ''`。
182	  - 字段的 `label` 来自 `field.name`。
183	  - select/radio 类型字段若无线有选项，自动生成默认选项。
184	  - `paramCount` = configurable 字段数量（仅用于显示）。
185	- 实例编辑时，字段值 `value` 可自由修改，不影响帧定义。
186	- 帧定义更新后，`createUpdatedInstanceFromFrame` 合并逻辑：已存在的字段保留 value，新字段用 defaultValue，移除的字段被删除（`sendFrameInsComposable.ts:587-657`）。
187	
188	**代码位置：**
189	- `src/types/frames/sendInstanceFactories.ts:14-93`
190	- `src/composables/frames/sendFrame/sendFrameInsComposable.ts:587-657`
191	
192	**保留建议：** 保留全字段复制 + 编辑不回写帧定义 + 帧更新后增量同步逻辑。
193	
194	---
195	
196	### 2.3 实例的 CRUD 行为
197	
198	| 操作 | 行为 | 位置 |
199	| --- | --- | --- |
200	| 创建 | 从帧模板创建，自动命名 `{frameName} #{nextNumber}`，ID 为递增数字 | `sendFrameInsComposable.ts:128-159` |
201	| 复制 | 深拷贝 + 新 ID + 新编号，保留原字段值 | `sendFrameInsComposable.ts:222-262` |
202	| 更新 | localInstance 深拷贝编辑 → applyLocalEdit → saveEditedInstance，支持 ID 修改 | `sendFrameInsComposable.ts:447-512` |
203	| 删除 | 单个删除 + 批量删除，删除后清空选中状态 | `sendFrameInsComposable.ts:182-219` |
204	| 移动 | 拖拽排序，失败时重新 fetch 回滚 | `sendFrameInsComposable.ts:274-314` |
205	| ID 修改 | 编辑模式下可修改实例 ID，保存时检测冲突，删除旧 ID 记录 | `sendFrameInsComposable.ts:459-494` |
206	
207	**保留建议：** 保留全部 CRUD 行为。ID 修改 + 冲突检测属于关键用户操作。
208	
209	---
210	
211	## 3. 帧导入/导出行为
212	
213	### 3.1 帧定义导入/导出
214	
215	**旧行为：**
216	- **导出格式：** JSON。通过 `fileDialogManager.exportFile()` 将 `templateStore.frames` 数组导出为文件。
217	- **导出内容：** 全部帧定义数组（`Frame[]`），包括 fields、options、identifierRules 等。
218	- **导入格式：** JSON。通过 `fileDialogManager.importFile()` 读取。
219	- **导入校验：** 只校验 `Array.isArray(result.fileData)`，无更深层的 schema 校验。
220	- **导入合并策略：** **全量覆盖**（`saveAll`），导入的数组直接替换现有所有帧。
221	- **导入路径：** 默认目录 `${pathAPI.getDataPath()}data/frames/configs`。
222	
223	**代码位置：**
224	- 导出：`src/pages/frames/FrameList.vue:313-348`
225	- 导入：`src/pages/frames/FrameList.vue:351-387`
226	
227	---
228	
229	### 3.2 发送帧实例导入/导出
230	
231	**旧行为：**
232	- **导出格式：** JSON。在 `FrameSendPage.vue:209` 调用 `dataStorageAPI.sendInstances.saveAll()` 导出。
233	- **导入格式：** JSON。通过 `importFromJSON(json)` 导入（`sendFrameInsComposable.ts:531-552`）。
234	- **导入校验：** 校验 `Array.isArray(data)`。
235	- **导入合并策略：** 全量覆盖。
236	
237	**代码位置：**
238	- `src/composables/frames/sendFrame/sendFrameInsComposable.ts:529-552`
239	- `src/pages/FrameSendPage.vue:209-229`
240	
241	---
242	
243	### 3.3 接收配置导入/导出
244	
245	**旧行为：**
246	- **导出：** `receiveFramesStore.exportConfig()` 返回 `{ groups, mappings, version }` JSON 对象。
247	- **导入：** `importConfig(config)` 校验 groups/mappings 是数组后全量替换，重置运行时 value/displayValue。
248	- **导入后同步：** 立即调用 `syncConfigToMainProcess()` 将配置同步到主进程缓存。
249	
250	**代码位置：** `src/stores/frames/receiveFramesStore.ts:372-417`
251	
252	**oracle 来源评估：** 导入导出代码完整，JSON 格式确认。
253	
254	**新系统对应 feature：** frame feature 的 import/export；send feature 的 import/export。
255	
256	**保留建议：**
257	- 保留：JSON 格式导出/导入。
258	- 保留：导入校验（至少验证数组格式）。
259	- 排除（旧 bug）：全量覆盖策略过于粗暴。新系统可考虑增量合并或冲突提示。
260	- 保留：接收配置导入后同步到主进程。
261	
262	---
263	
264	## 4. 帧字段管理行为
265	
266	### 4.1 字段数据类型支持
267	
268	**11 种数据类型**（`frameDefaults.ts:30-42`）：
269	
270	| 类型 | 字节数 | fixedLength | 需要指定 length |
271	| --- | --- | --- | --- |
272	| uint8 | 1 | 1 | 否 |
273	| int8 | 1 | 1 | 否 |
274	| uint16 | 2 | 2 | 否 |
275	| int16 | 2 | 2 | 否 |
276	| uint32 | 4 | 4 | 否 |
277	| int32 | 4 | 4 | 否 |
278	| uint64 | 8 | 8 | 否 |
279	| int64 | 8 | 8 | 否 |
280	| float | 4 | 4 | 否 |
281	| double | 8 | 8 | 否 |
282	| bytes | N | null | **是** |
283	
284	**注意：** `string` 类型在 `FIELD_TYPE_CONFIGS` 中定义但不在 `FIELD_TYPE_OPTIONS` 中，属于未暴露类型。
285	
286	**代码位置：** `src/config/frameDefaults.ts:30-42, 67-81`
287	
288	---
289	
290	### 4.2 字段输入类型
291	
292	**4 种输入类型**（`frameDefaults.ts:196-201`）：
293	
294	| 输入类型 | needsOptions | minOptions | maxOptions | hasDefaultOption | 描述 |
295	| --- | --- | --- | --- | --- | --- |
296	| input | 否 | 0 | 0 | 否 | 普通输入框 |
297	| select | 是 | 2 | 20 | 是 | 下拉选择框 |
298	| radio | 是 | 2 | 10 | 是 | 单选按钮组 |
299	| expression | 否 | 0 | 0 | 否 | 自定义表达式 |
300	
301	**切换输入类型时的自动行为**（`frameFieldsStore.ts:278-303`）：
302	- 切到 select：若无 options，自动填充 `DEFAULT_SELECT_OPTIONS`（3 选项）。
303	- 切到 radio：若无 options，自动填充 `DEFAULT_RADIO_OPTIONS`（2 选项）。
304	- 切回 input：清空 options，defaultValue 重置为 `'0x00'`。
305	
306	**代码位置：** `src/config/frameDefaults.ts:162-201`，`src/stores/frames/frameFieldsStore.ts:278-303`
307	
308	---
309	
310	### 4.3 字段属性完整列表
311	
312	| 属性 | 类型 | 必填 | 默认值 | 说明 |
313	| --- | --- | --- | --- | --- |
314	| id | string | 是 | nanoid() | 唯一标识 |
315	| name | string | 是 | '新字段' | 字段名称 |
316	| dataType | FieldType | 是 | 'uint8' | 数据类型 |
317	| length | number | 是 | 1 | 长度（字节/元素数） |
318	| factor | number | 否 | 1 | 因子 |
319	| description | string | 否 | '' | 描述 |
320	| validOption | ValidationParam | 否 | DEFAULT_VALID_OPTION | 校验设置 |
321	| defaultValue | string | 否 | '0' | 默认值 |
322	| inputType | FieldInputType | 是 | 'input' | 输入控件类型 |
323	| configurable | boolean | 是 | true | 发送用例中是否可配置 |
324	| bigEndian | boolean | 否 | true | 端序 |
325	| isASCII | boolean | 否 | - | ASCII 模式 |
326	| options | Option[] | 否 | [] | select/radio 选项 |
327	| dataParticipationType | 'direct'\|'indirect' | 否 | 'direct' | 数据参与类型 |
328	| expressionConfig | ExpressionConfig | 否 | - | 表达式配置 |
329	
330	**代码位置：** `src/types/frames/fields.ts:48-71`，`src/types/frames/factories.ts:13-30`
331	
332	---
333	
334	### 4.4 字段操作行为
335	
336	| 操作 | 行为 | 位置 |
337	| --- | --- | --- |
338	| 添加 | 末尾追加，自动选中 | `frameFieldsStore.ts:239-242` |
339	| 删除 | splice 移除，调整选中索引 | `frameFieldsStore.ts:80-95` |
340	| 复制 | 紧接原位置之后插入，name 加 `(副本)` 后缀，新 id | `frameFieldsStore.ts:97-115` |
341	| 移动 | splice 拖拽，更新选中索引 | `frameFieldsStore.ts:117-142` |
342	| 编辑 | tempField 深拷贝 → 编辑 → saveField 回写 → editorStore.updateEditorFrame | `frameFieldsStore.ts:167-271` |
343	
344	**验证规则**（`frameUtils.ts:244-319`）：
345	- 字段名称非空
346	- dataType 必填
347	- bytes 类型 length > 0
348	- expression 类型必须有 expressionConfig
349	- 字段名称在帧内唯一
350	
351	**代码位置：** `src/utils/frames/frameUtils.ts:244-319`
352	
353	---
354	
355	### 4.5 校验和字段配置
356	
357	**ValidationParam 结构**（`fields.ts:82-87`）：
358	
359	| 字段 | 类型 | 说明 |
360	| --- | --- | --- |
361	| isChecksum | boolean | 是否为校验和字段 |
362	| startFieldIndex | string | 起始字段索引 |
363	| endFieldIndex | string | 结束字段索引 |
364	| checksumMethod | string | 方法：crc16 / crc32 / xor8 / sum8 |
365	
366	默认校验方法：`sum8`（`frameDefaults.ts:120`）。
367	
368	**帧级 options**（`frames.ts:9-13`）：
369	- autoChecksum: boolean — 自动计算校验和
370	- bigEndian: boolean — 全局端序
371	- includeLengthField: boolean — 是否包含长度字段
372	
373	**保留建议：** 全部保留。校验和计算是帧编码的核心能力。
374	
375	---
376	
377	### 4.6 表达式字段
378	
379	**旧行为：**
380	- 字段可设置 `inputType: 'expression'`，此时字段 `configurable` 默认为 false，`dataParticipationType` 为 `'indirect'`。
381	- 表达式配置 `ExpressionConfig` 包含：多条件表达式列表（condition + expression）、变量映射列表。
382	- 变量映射支持 4 种数据源：current_field / frame_field / global_stat / scoe_data。
383	- 变量标识符（identifier）用于表达式中引用。
384	- 表达式验证：至少一个表达式 + 变量标识符唯一性。
385	- 表达式字段不参与帧匹配（`directDataFrames` computed 过滤掉 indirect 字段）。
386	- 接收数据时，表达式字段跳过正常更新，由 `frameExpressionManager.calculateAndApplyReceiveFrame` 单独计算。
387	
388	**代码位置：**
389	- 类型定义：`src/types/frames/fields.ts:7-45`
390	- 工厂函数：`src/types/frames/factories.ts:38-57`
391	- 默认配置：`src/utils/frames/defaultConfigs.ts:88-205`
392	- 接收过滤：`src/stores/frames/receiveFramesStore.ts:823-843`
393	- 表达式计算：`src/stores/frames/receiveFramesStore.ts:1091-1099`
394	
395	**保留建议：** 保留表达式字段的完整配置能力（多条件表达式、变量映射、4 种数据源）。表达式执行引擎归口 shared/，但配置 UI 和触发逻辑归 frame feature。
396	
397	---
398	
399	### 4.7 帧识别规则
400	
401	**旧行为：**
402	- `IdentifierRule` 结构：startIndex、endIndex、operator、value、logicOperator（and/or）。
403	- 帧可定义多条识别规则，用于接收时帧匹配。
404	- 默认值：startIndex=0, endIndex=7, operator='eq', value='0x00', logicOperator='and'。
405	
406	**代码位置：**
407	- 类型：`src/types/frames/frames.ts:15-21`
408	- 默认值：`src/config/frameDefaults.ts:105-111`
409	
410	**保留建议：** 保留帧识别规则作为帧定义的一部分。
411	
412	---
413	
414	## 5. 旧 JSON 格式与新格式的关键差异
415	
416	### 5.1 帧定义存储格式
417	
418	**旧格式（持久化到 JSON 文件）：**
419	- 存储路径：`data/templates/framesConfig`
420	- 格式：`Frame[]` 数组，每个 Frame 包含完整 fields、options、identifierRules。
421	- 通过 `dataStorageAPI.framesConfig.saveAll()` 全量写入。
422	- Date 类型在序列化时转为 ISO 字符串，nanoid 生成字符串 ID。
423	
424	**新系统已有的帧定义**（从 `rewrite/src/features/frame/` 推断）：
425	- 新系统帧定义核心结构类似，但已重构为 feature 架构。
426	- 具体格式差异需对照新系统 `FrameDefinition` 类型确认。
427	
428	### 5.2 实例存储格式
429	
430	**旧格式：**
431	- 发送实例：`data/templates/sendInstances`，`SendFrameInstance[]`
432	- SCOE 发送实例：`data/templates/scoeSendInstances`
433	- SCOE 接收指令：`data/templates/scoeReceiveCommands`
434	- 接收配置：`data/templates/receiveConfig`，`{ groups, mappings, version }` 对象
435	
436	### 5.3 迁移注意事项
437	
438	- 旧系统 Date 字段 `createdAt`/`updatedAt` 在 JSON 中为 ISO 字符串，反序列化后需转回 Date。
439	- `lastId` 字段用于编辑模式下跟踪 ID 变更，新系统可简化。
440	- 旧系统 `Frame.timestamp` 是 number（毫秒时间戳），`createdAt`/`updatedAt` 是 Date 对象。
441	- 旧系统实例的 `paramCount` 仅用于 UI 显示，非核心数据。
442	
443	**保留建议：** 旧 JSON 可作为迁移 oracle，但不污染新系统核心模型。迁移时需做格式转换。
444	
445	---
446	
447	## 6. 帧模板的使用行为
448	
449	### 6.1 帧模板管理（frameTemplateStore）
450	
451	**旧行为：**
452	- 帧模板即帧定义，不存在独立的"模板"概念。`frameTemplateStore` 是所有帧定义的唯一 Store。
453	- 帧列表页面（`FrameList.vue`）展示所有帧，支持搜索、过滤（方向、日期范围）、排序（ID/名称/日期/使用次数）。
454	- 帧详情面板展示选中帧的字段列表和参数。
455	- 帧编辑器（`FrameEditor.vue`）是独立路由页面，支持创建/编辑两种模式。
456	
457	### 6.2 帧与实例的关系
458	
459	- 帧定义是模板（1），实例是从模板创建的具体配置（N）。
460	- 实例保留帧 ID 引用（`frameId`），但不维护反向引用。
461	- 帧更新时可触发关联实例的批量同步（`updateInstancesByFrameId`），但不是强制的。
462	
463	### 6.3 基于 SCOE 标记的特殊帧
464	
465	- 帧有 `isSCOEFrame` 布尔标记。
466	- SCOE 帧在 `scoeFrameInstancesStore` 中独立管理。
467	- SCOE 帧的过滤条件：`isSCOEFrame === true && direction === 'send'`（或 `'receive'`）。
468	
469	**代码位置：**
470	- `src/stores/frames/scoeFrameInstancesStore.ts:55-65`
471	- `src/types/frames/frames.ts:39`（isSCOEFrame 字段）
472	
473	**保留建议：**
474	- 排除 `isSCOEFrame` 标记。新系统中 SCOE 统一通过指令接入 feature，不再需要帧级 SCOE 标记。
475	- 保留帧列表的搜索/过滤/排序行为。
476	- 保留帧编辑器的独立路由页面模式。
477	
478	---
479	
480	## 7. 过滤与排序行为
481	
482	**旧行为：**
483	- 搜索：按 name、description、fields.name 模糊匹配（不区分大小写）。
484	- 方向过滤：按 `direction` 精确匹配。
485	- 日期范围过滤：按 `createdAt` 范围过滤。
486	- 排序选项：ID（localeCompare）、name（localeCompare）、date（降序）、usage（降序）。
487	
488	**代码位置：** `src/utils/frames/frameUtils.ts:354-456`
489	
490	**保留建议：** 保留全部过滤和排序行为。
491	
492	---
493	
494	## 8. 自动保存与配置同步
495	
496	**旧行为（receiveFramesStore 特有）：**
497	- 监听 `groups` 和 `mappings` 变化（排除运行时 value/displayValue），1 秒防抖自动保存。
498	- 监听帧模板变化，500ms 防抖同步到主进程缓存。
499	- 主进程缓存用于数据接收时的帧匹配，避免每次接收数据都 IPC 传配置。
500	
501	**代码位置：** `src/stores/frames/receiveFramesStore.ts:168-267`
502	
503	**保留建议：** 保留配置同步到主进程缓存的行为（性能关键）。新系统应通过 platform facade 实现，不直接暴露 IPC。
504	
505	---
506	
507	## 9. 帧定义的完整数据流
508	
509	```
510	用户操作 → FrameEditor.vue
511	  → useFrameEditor (composable, 协调)
512	    → frameEditorStore (编辑状态)
513	    → frameFieldsStore (字段状态)
514	    → frameTemplateStore (持久化)
515	      → dataStorageAPI.framesConfig (IPC → main → 文件)
516	```
517	
518	**帧实例数据流：**
519	```
520	用户选帧 → sendFrameInstancesStore.createInstance(frameId)
521	  → frameTemplateStore.frames → 找到帧定义
522	  → createSendFrameInstance(frame, id) → 从帧创建实例
523	  → dataStorageAPI.sendInstances.save → 持久化
524	```
525	
526	---
527	
528	## 10. 汇总：必须保留的行为清单
529	
530	### 高优先级（核心业务行为）
531	
532	1. **帧 CRUD**：全量加载、深拷贝编辑、变更检测、saveAll 持久化、ID 修改（含冲突检测）
533	2. **字段 11 种数据类型**：uint8/int8/.../double/bytes，含 fixedLength 和 needsLength 配置
534	3. **字段 4 种输入类型**：input/select/radio/expression，含自动选项生成
535	4. **字段操作**：添加、删除、复制（含命名后缀）、移动、编辑（tempField 模式）
536	5. **帧验证**：name 非空、至少一个字段、字段名唯一性、bytes 类型 length > 0
537	6. **实例从帧创建**：全字段复制、configurable 标记、选项自动生成
538	7. **帧更新后实例同步**：已存在字段保留 value，新字段用 defaultValue
539	8. **校验和配置**：isChecksum、startFieldIndex/endFieldIndex、checksumMethod（4 种方法）
540	9. **表达式字段**：多条件表达式、变量映射（4 种数据源）、indirect 数据参与
541	10. **帧识别规则**：startIndex/endIndex/operator/value/logicOperator
542	11. **帧选项**：autoChecksum / bigEndian / includeLengthField
543	12. **JSON 导入/导出**：帧定义全量导出/导入
544	13. **收藏功能**：帧级 + 实例级独立收藏
545	14. **配置同步到主进程缓存**（接收帧匹配性能关键）
546	
547	### 中优先级（可观测 UI 行为）
548	
549	15. **帧列表过滤**：搜索（name/desc/fieldName）、direction、日期范围
550	16. **帧列表排序**：ID、name、date、usage
551	17. **帧复制**：深拷贝 + `(副本)` 命名 + 新 ID
552	18. **实例 CRUD**：创建、复制（含自动编号）、删除（含批量）、拖拽排序、ID 修改
553	19. **实例编辑**：localInstance 深拷贝模式、十六进制值显示、校验和自动计算
554	
555	### 低优先级（可简化或排除）
556	
557	20. **SCOE 帧标记 isSCOEFrame** — 排除，新系统统一通过指令接入
558	21. **FRAMES_PER_PAGE = 20** — UI 展示策略，非核心
559	22. **全量覆盖式导入** — 排除旧策略，新系统应提供冲突处理
560	23. **lastId 字段** — 编辑模式 ID 变更跟踪，新系统可简化实现
561	24. **receiveConfig 的 groups/mappings 结构** — 属于 receive feature，非帧定义核心
562	
563	---
564	
565	## 后续
566	
567	无。本文件为纯事实提取，供后续设计和实施参考。
568	
```

> TOOL

tool_result
id: call_2d9c97122ef64256bc7e8a1e
```
1	# [S004] 旧系统表达式引擎与帧解析行为调研
2	
3	> 2026-05-19 | 调研 | 完成
4	
5	## 目标
6	
7	调研旧系统的表达式引擎和帧解析行为，提取所有必须保留的可观测业务行为。只做事实提取，不做设计或实施。
8	
9	---
10	
11	## 一、旧表达式引擎核心行为
12	
13	### 1.1 表达式计算模型
14	
15	**旧行为描述**：表达式引擎采用"条件表达式列表 + 变量映射"模型。每个字段的 `expressionConfig` 包含一组 `ConditionalExpression[]`（条件 + 表达式对）和一组 `VariableMapping[]`（变量标识符到数据源的映射）。计算时按列表顺序逐条评估条件，第一个条件为真的表达式被执行并返回结果；若所有条件均不满足，返回默认值 `0`。
16	
17	- **代码位置**：`src/composables/frames/useExpressionCalculator.ts:189-264`（`calculateConditionalExpression` + `calculateExpression`）
18	- **新系统对应**：`shared/` 表达式引擎（纯 TypeScript）
19	- **Oracle 来源**：`public/data/frames/configs/3.json`（包含多条件表达式的接收帧配置，含 `var1*2`、`var1+var2` 等）
20	- **保留建议**：必须保留。条件-表达式对、顺序评估、默认值 0 的语义是核心业务行为。
21	
22	### 1.2 安全求值机制
23	
24	**旧行为描述**：使用 `new Function(...keys, 'return (expression)')` 构造受限执行环境。将变量和数学函数注入作用域，用户表达式在沙盒化的上下文中执行。
25	
26	- **代码位置**：`src/composables/frames/useExpressionCalculator.ts:151-186`（`safeEvaluate`）
27	- **新系统对应**：`shared/` 表达式引擎
28	- **Oracle 来源**：代码逻辑本身
29	- **保留建议**：保留"受限求值"语义。新系统可用 AST 解析或 mathjs 替代 `new Function`，但必须保持等价的函数和变量注入能力。
30	
31	### 1.3 支持的运算符和函数
32	
33	**旧行为描述**：因为使用 `new Function` + JavaScript 表达式语法，实际支持 JavaScript 所有运算符（算术、比较、逻辑、三元、位运算等）。注入的数学函数有：
34	- `Math` 对象（完整）
35	- `abs`, `ceil`, `floor`, `round`, `max`, `min`
36	- `sin`, `cos`, `tan`
37	- `sqrt`, `log`, `exp`, `pow`
38	
39	- **代码位置**：`src/composables/frames/useExpressionCalculator.ts:155-170`
40	- **新系统对应**：`shared/` 表达式引擎
41	- **Oracle 来源**：代码；配置样本 `3.json` 中使用 `var1*2`、`var1+var2`
42	- **保留建议**：必须保留全部数学函数。新系统若改用白名单机制，需确保以上函数全部在白名单内。
43	
44	### 1.4 变量解析 — 四种数据源
45	
46	**旧行为描述**：变量通过 `VariableMapping` 从四种数据源解析：
47	1. **`CURRENT_FIELD`**：当前帧的其他字段（通过 `sourceId` 指定字段 ID）
48	2. **`FRAME_FIELD`**：其他帧的字段（通过 `frameId` + `fieldId`）——如果是同帧字段则走当前帧数据
49	3. **`GLOBAL_STAT`**：全局统计数据（通过 `globalStatsStore.getStatValue`）
50	4. **`SCOE_DATA`**：SCOE 配置/状态数据（通过路径解析 `status.xxx` / `config.xxx`）
51	
52	未解析成功的变量默认值为 `0`。
53	
54	- **代码位置**：`src/composables/frames/useExpressionCalculator.ts:56-148`（`resolveVariableValue` + `resolveAllVariables`）
55	- **新系统对应**：`shared/` 表达式引擎的变量解析；数据源来自各 feature public API
56	- **Oracle 来源**：`public/data/frames/configs/3.json` 中 `sourceType: "current_field"` 的变量映射
57	- **保留建议**：`CURRENT_FIELD` 和 `FRAME_FIELD` 必须保留。`GLOBAL_STAT` 需评估（新系统全局统计 feature 是否保留）。`SCOE_DATA` 属于 SCOE 专有，归入 SCOE/指令接入 feature 处理。
58	
59	### 1.5 依赖排序（拓扑排序）
60	
61	**旧行为描述**：表达式字段之间可能存在依赖（字段 A 的表达式引用字段 B 的值）。系统通过以下流程处理：
62	1. 从表达式和变量映射中提取当前帧字段引用（`extractFieldReferences`）
63	2. 构建依赖图（`analyzeDependencies`）
64	3. Kahn 算法拓扑排序（`topologicalSort`）
65	4. 按排序结果依次计算，每计算完一个字段立即更新上下文数据
66	
67	循环依赖检测：若排序失败（存在环），所有表达式字段返回错误，不执行计算。
68	
69	- **代码位置**：`src/composables/frames/useExpressionCalculator.ts:348-467`（依赖分析 + 拓扑排序）；`src/composables/frames/useFrameExpressionManager.ts:154-274`（`calculateWithDependencies` 按序执行）
70	- **新系统对应**：`shared/` 表达式引擎
71	- **Oracle 来源**：`public/data/frames/configs/3.json` 中字段 `340LYOzVTf81_koKFk61G` 的变量 `var2` 引用了自身（`sourceId` 指向自身），测试自引用场景
72	- **保留建议**：必须保留。依赖排序和循环检测是表达式引擎的核心正确性保证。
73	
74	### 1.6 依赖缓存
75	
76	**旧行为描述**：`useFrameExpressionManager` 维护了一个 `dependencyCache`（Map），缓存依赖分析和排序结果。缓存键为 `frameId + 表达式数量`。缓存有效期 5 分钟，且配置哈希不变时才命中。缓存上限 50 条，LRU 淘汰。
77	
78	- **代码位置**：`src/composables/frames/useFrameExpressionManager.ts:26-119`
79	- **新系统对应**：`shared/` 表达式引擎（缓存属于实现细节，非可观测行为）
80	- **Oracle 来源**：代码逻辑
81	- **保留建议**：缓存是性能优化而非可观测行为，新系统可自行决定缓存策略。但拓扑排序结果必须确定且可复现。
82	
83	### 1.7 类型处理 — 下取整规则
84	
85	**旧行为描述**：表达式计算结果在写回帧数据时，会根据字段数据类型处理：
86	- `float` / `double`：保持原值
87	- 其他数字类型（`uint8/16/32/64`, `int8/16/32/64`）：`Math.floor()` 向下取整
88	- 非数字类型：保持原值
89	
90	- **代码位置**：`src/composables/frames/useFrameExpressionManager.ts:127-145`（`processValueByDataType`）
91	- **新系统对应**：`shared/` 表达式引擎或 frame feature
92	- **Oracle 来源**：代码逻辑
93	- **保留建议**：必须保留。这个取整行为直接影响表达式字段的最终值，是用户可感知的业务行为。
94	
95	### 1.8 表达式计算时机
96	
97	**旧行为描述**：
98	- **接收帧**：每次收到匹配的帧数据后，表达式在数据解析完成后立即计算（`calculateAndApplyReceiveFrame`），更新对应的 dataItem 值。
99	- **发送帧**：在发送前计算表达式（`calculateAndApplySendFrame`），更新实例字段值后再组帧。
100	
101	- **代码位置**：`src/composables/frames/useFrameExpressionManager.ts:502-507`（接收帧便捷方法）；`src/composables/frames/useFrameExpressionManager.ts:488-496`（发送帧便捷方法）
102	- **新系统对应**：receive feature 的数据解析管线；send feature 的组帧管线
103	- **Oracle 来源**：代码调用链
104	- **保留建议**：必须保留。计算时机影响表达式字段中变量引用的时序正确性。
105	
106	### 1.9 错误处理
107	
108	**旧行为描述**：
109	- 变量解析失败 → 默认值 `0`
110	- 表达式语法错误 → 抛出 `Error('表达式计算错误: ...')`，上层 catch 返回 `success: false`
111	- 循环依赖 → 所有字段返回 `success: false`，error 为 `循环依赖错误: ...`
112	- 条件表达式计算异常 → 返回 `success: false`
113	- 通用 catch → 返回 `success: false`
114	
115	计算结果不会导致系统崩溃，但错误的表达式字段值不会被应用（只 console.error）。
116	
117	- **代码位置**：`src/composables/frames/useExpressionCalculator.ts:183-184`（safeEvaluate catch）；`src/composables/frames/useFrameExpressionManager.ts:193-206`（循环依赖处理）；`src/composables/frames/useFrameExpressionManager.ts:259-271`（通用 catch）
118	- **新系统对应**：`shared/` 表达式引擎
119	- **Oracle 来源**：代码逻辑
120	- **保留建议**：必须保留。"不崩溃、错误不应用、默认值为 0"的容错语义是可观测行为。
121	
122	---
123	
124	## 二、旧帧解析核心行为
125	
126	### 2.1 字节到字段的解析流程
127	
128	**旧行为描述**：解析按字段在帧定义中的顺序依次进行。每个字段有 `length`（字节数）和 `dataType`。从 `startOffset` 开始提取 `length` 字节，根据 `dataType` 解析为对应类型的值。字段偏移量通过累加每个字段的 `length` 计算。
129	
130	- **代码位置**：`src/utils/receive/dataProcessor.ts:199-430`（`extractFieldValue`）；`src/utils/receive/dataProcessor.ts:486-489`（偏移量计算）
131	- **新系统对应**：frame feature 的帧解析
132	- **Oracle 来源**：所有 `public/data/frames/configs/*.json` 中的字段定义
133	- **保留建议**：必须保留。顺序解析、偏移量累加是帧解析的基础语义。
134	
135	### 2.2 11 种数据类型的解析规则
136	
137	**旧行为描述**：支持以下 11 种数据类型（对应 `FieldType`）：
138	
139	| 类型 | 长度 | 解析规则 |
140	|------|------|----------|
141	| `uint8` | 1 | 直接读取字节 |
142	| `int8` | 1 | `> 127` 时减 256 转负数 |
143	| `uint16` | 2 | 两字节组合（端序敏感） |
144	| `int16` | 2 | 两字节组合，`> 32767` 时减 65536 |
145	| `uint32` | 4 | 四字节组合，`>>> 0` 确保无符号 |
146	| `int32` | 4 | 四字节组合，`> 2147483647` 时减 4294967296 |
147	| `uint64` | 8 | `BigInt` 解析（`parseBigIntFromBytes`） |
148	| `int64` | 8 | `BigInt` 解析，`> 0x7FFFFFFFFFFFFFFF` 时转负数 |
149	| `float` | 4 | `DataView.getFloat32` |
150	| `double` | 8 | `DataView.getFloat64` |
151	| `bytes` | 自定义 | `isASCII` 时按字符解码；否则转十六进制字符串 |
152	
153	特殊处理：
154	- `float` 的 `displayValue` 保留 2 位小数（`.toFixed(2)`）
155	- `double` 的 `displayValue` 保留 4 位小数（`.toFixed(4)`）
156	- `uint64`/`int64` 应用 factor 后四舍五入（`Math.round`）
157	- `bytes` ASCII 模式过滤 0 字节
158	
159	- **代码位置**：`src/utils/receive/dataProcessor.ts:221-421`（switch 分支）
160	- **新系统对应**：frame feature 的字段解析
161	- **Oracle 来源**：配置样本中各类字段的 `dataType` 声明
162	- **保留建议**：全部保留。这些解析规则是协议正确性的基础。
163	
164	### 2.3 字节序处理
165	
166	**旧行为描述**：每个字段有 `bigEndian` 属性（默认 `true`）。解析时根据此属性决定字节顺序：
167	- 大端序（默认）：高字节在前
168	- 小端序：低字节在前
169	
170	`float` 和 `double` 通过 `DataView` 的 `littleEndian` 参数处理。`uint64`/`int64` 通过 BigInt 移位处理。
171	
172	- **代码位置**：`src/utils/receive/dataProcessor.ts` 各 case 分支中的 `field.bigEndian === false` 判断
173	- **新系统对应**：frame feature
174	- **Oracle 来源**：配置样本中字段的 `bigEndian` 属性
175	- **保留建议**：必须保留。字节序影响解析正确性。
176	
177	### 2.4 applyFactor（倍率/偏移）
178	
179	**旧行为描述**：字段有可选的 `factor` 属性。当 `factor` 存在且不等于 1 时，解析后的数值乘以 factor。结果使用 `parseFloat(result.toFixed(5))` 限制为最多 5 位小数，避免浮点精度问题。
180	
181	factor 在以下时机应用：
182	- 接收帧解析：`extractFieldValue` 中对数值类型应用
183	- 发送帧组帧：`getFullHexString` 中对有 factor 的字段值先乘以 factor 再转十六进制
184	
185	- **代码位置**：`src/utils/receive/dataProcessor.ts:121-134`（`applyFactor` + `shouldApplyFactor`）；`src/utils/frames/hexCovertUtils.ts:254-258`（发送端 factor）
186	- **新系统对应**：frame feature
187	- **Oracle 来源**：配置样本中字段的 `factor` 属性
188	- **保留建议**：必须保留。倍率是协议解析的核心功能，5 位小数限制是可观测行为。
189	
190	### 2.5 帧识别（匹配）规则
191	
192	**旧行为描述**：帧通过 `identifierRules` 进行识别。每条规则指定 `startIndex`、`endIndex`（包含）、`operator` 和 `value`。所有规则必须全部满足（AND 逻辑）才算匹配。支持的运算符：
193	
194	| 运算符 | 别名 | 含义 |
195	|--------|------|------|
196	| `eq` | `==`, `=` | 等于 |
197	| `neq` | `!=` | 不等于 |
198	| `gt` | `>` | 大于 |
199	| `gte` | `>=` | 大于等于 |
200	| `lt` | `<` | 小于 |
201	| `lte` | `<=` | 小于等于 |
202	| `contains` | - | 包含 |
203	| `not_contains` | - | 不包含 |
204	
205	匹配时将实际数据和期望值都转换为十六进制字符串进行比较。
206	
207	- **代码位置**：`src/utils/receive/frameMatchers.ts:14-110`
208	- **新系统对应**：frame feature / receive feature
209	- **Oracle 来源**：帧定义中的 `identifierRules` 字段
210	- **保留建议**：必须保留。帧识别是接收管线的入口。
211	
212	### 2.6 数据参与类型（direct / indirect）
213	
214	**旧行为描述**：字段有 `dataParticipationType` 属性（默认 `direct`）：
215	- `direct`：参与组帧发送或从帧中直接解析
216	- `indirect`：不参与组帧，通过表达式计算得出或作为计算参数
217	
218	在发送帧组帧时（`frameToBuffer`），只包含 `direct` 字段。在接收帧解析时，所有字段都参与偏移量计算（间接字段在帧结构中占位）。
219	
220	- **代码位置**：`src/utils/frames/frameInstancesUtils.ts:352-354`（组帧过滤）；`src/utils/receive/dataProcessor.ts:486-489`（解析时无过滤）
221	- **新系统对应**：frame feature
222	- **Oracle 来源**：`public/data/frames/configs/3.json` 中 `dataParticipationType: "indirect"` 的表达式字段
223	- **保留建议**：必须保留。direct/indirect 决定哪些字段参与实际字节编解码。
224	
225	### 2.7 校验和计算
226	
227	**旧行为描述**：字段可通过 `validOption.isChecksum = true` 标记为校验字段。支持四种校验方法：
228	
229	| 方法 | 算法 |
230	|------|------|
231	| `xor8` | 所有字节异或 |
232	| `sum8` | 所有字节累加，取低 8 位 |
233	| `crc16` | Modbus CRC-16（初始值 0xFFFF，多项式 0xA001） |
234	| `crc32` | 标准 CRC-32（初始值 0xFFFFFFFF，多项式 0xEDB88320） |
235	
236	校验范围通过 `startFieldIndex` 和 `endFieldIndex` 指定。在 `frameToBuffer` 中，组帧前先计算校验值并写入校验字段。
237	
238	- **代码位置**：`src/utils/frames/frameInstancesUtils.ts:154-340`（`calculateChecksum` + `calculateXor8/Sum8/Crc16/Crc32`）
239	- **新系统对应**：frame feature
240	- **Oracle 来源**：配置样本中字段的 `validOption` 配置
241	- **保留建议**：必须保留。四种校验算法的精确实现必须保持字节级兼容。
242	
243	### 2.8 标签显示（labelOptions）
244	
245	**旧行为描述**：数据项有 `useLabel` + `labelOptions` 机制。当启用时，将解析的 displayValue 转换为十六进制后与 labelOptions 的 value（也转为十六进制）匹配。匹配成功时用 label 替代原始值显示。
246	
247	- **代码位置**：`src/utils/receive/dataProcessor.ts:523-533`
248	- **新系统对应**：receive feature / UI 层
249	- **Oracle 来源**：配置样本中 dataItem 的 `labelOptions`
250	- **保留建议**：必须保留。标签显示是用户可感知的展示行为。
251	
252	---
253	
254	## 三、旧条件判断核心行为
255	
256	### 3.1 发送触发条件（TriggerCondition）
257	
258	**旧行为描述**：发送任务的触发条件由 `TriggerCondition[]` 定义。每个条件指定 `fieldId`（关联的数据项）、`condition`（操作符）和 `value`（期望值）。条件之间通过 `logicOperator` 连接（`and` / `or`）。
259	
260	支持的操作符：
261	- `equals`：字符串比较
262	- `not_equals`：字符串比较
263	- `greater`：数值比较
264	- `less`：数值比较
265	- `contains`：字符串包含
266	
267	AND/OR 混合逻辑评估规则：按条件顺序依次评估，使用前一个条件的 `logicOperator` 与当前结果组合。存在短路求值：AND 遇到 false 或 OR 遇到 true 时提前结束。空条件数组 = 接收到帧就触发。
268	
269	- **代码位置**：`src/composables/frames/sendFrame/useSendTaskTriggerListener.ts:100-158`（`evaluateTriggerConditions`）；`src/composables/frames/sendFrame/useSendTaskTriggerListener.ts:189-218`（`evaluateSingleCondition`）
270	- **新系统对应**：send feature / task feature 的触发引擎
271	- **Oracle 来源**：`src/types/frames/sendInstances.ts:118-124`（`TriggerCondition` 接口）
272	- **保留建议**：必须保留。五种操作符和 AND/OR 短路逻辑是核心业务行为。
273	
274	### 3.2 SCOE 完成条件（CompletionCondition）
275	
276	**旧行为描述**：SCOE 指令的完成条件由 `CompletionCondition[]` 定义。与发送触发条件不同，它支持两种模式：
277	
278	1. **固定值模式**（`useParam = false`）：直接比较源字段值与 `targetFixedValue`，使用 `operator`
279	2. **参数模式**（`useParam = true`）：通过参数值在参数选项中查找索引，再用同一索引在条件的 `options` 数组中找到匹配规则（operator + matchValue）
280	
281	所有条件必须全部满足（AND 逻辑，无 OR）。条件检查使用定时轮询机制（默认 100ms 间隔），有超时机制（默认 5000ms）。
282	
283	- **代码位置**：`src/utils/receive/scoeFrame.ts:416-491`（`checkCompletionConditions`）；`src/utils/receive/scoeFrame.ts:501-540`（`waitForCompletionConditions`）
284	- **新系统对应**：指令接入 feature / SCOE 子系统
285	- **Oracle 来源**：`public/data/templates/scoeReceiveCommands.json`（含 params 和 conditions 的指令配置）
286	- **保留建议**：必须保留。参数索引匹配模式是 SCOE 特有的业务行为。
287	
288	### 3.3 比较运算符（compareValues）
289	
290	**旧行为描述**：通用比较函数 `compareValues`（在 `hexCovertUtils.ts` 中），支持六种运算符：
291	
292	| 运算符 | 含义 | 数值模式 | 字符串模式 |
293	|--------|------|----------|-----------|
294	| `equal` | 等于 | 数值比较 | 字符串比较 |
295	| `not_equal` | 不等于 | 数值比较 | 字符串比较 |
296	| `greater_than` | 大于 | 数值比较 | 不支持 |
297	| `less_than` | 小于 | 数值比较 | 不支持 |
298	| `greater_equal` | 大于等于 | 数值比较 | 不支持 |
299	| `less_equal` | 小于等于 | 数值比较 | 不支持 |
300	
301	自动检测：先尝试将两个值解析为数值（支持十六进制），如果都成功则数值比较，否则字符串比较。只有 equal/not_equal 支持字符串比较模式。
302	
303	- **代码位置**：`src/utils/frames/hexCovertUtils.ts:338-375`（`compareValues`）
304	- **新系统对应**：`shared/` 纯函数
305	- **Oracle 来源**：代码逻辑
306	- **保留建议**：必须保留。六种运算符和自动类型检测是可观测的比较语义。
307	
308	### 3.4 SCOE 帧识别流程
309	
310	**旧行为描述**：SCOE 帧识别是独立于通用帧识别的多步骤流程：
311	
312	1. 验证功能码（4 字节：SCOE 标识 + 指令码 + 2 字节固定值）
313	2. 若 SCOE 帧未加载，只接受加载指令（指令码 `01`）
314	3. 若 SCOE 帧已加载，验证三标志（信息标识、信源标识、信宿标识，按开关启用）
315	4. 验证型号 ID（4 字节）和卫星 ID（4 字节）
316	5. 全部通过才识别为 SCOE 帧
317	
318	- **代码位置**：`src/utils/receive/scoeFrame.ts:167-291`（`isScoeFrame`）
319	- **新系统对应**：指令接入 feature
320	- **Oracle 来源**：`public/data/scoe/satelliteConfigs/1.json`；`public/data/scoe/scoeConfigs/1.json`
321	- **保留建议**：保留核心识别流程。但具体的多步骤验证应归入 SCOE/指令接入 feature 的内部实现。
322	
323	### 3.5 SCOE 校验和验证
324	
325	**旧行为描述**：SCOE 有独立的校验和验证机制（`validateChecksums`）。支持多个校验配置，每个配置指定：起始偏移（`offset`）、长度（`length`）和校验位偏移（`checksumOffset`）。校验算法为累加取模 256。支持 enabled 开关。
326	
327	- **代码位置**：`src/utils/receive/scoeFrame.ts:310-358`
328	- **新系统对应**：指令接入 feature
329	- **Oracle 来源**：`public/data/templates/scoeReceiveCommands.json` 中指令的 `checksums` 字段
330	- **保留建议**：必须保留。SCOE 校验和验证是 SCOE 协议的一部分。
331	
332	---
333	
334	## 四、配置样本 Oracle 汇总
335	
336	| 文件 | 内容 | Oracle 价值 |
337	|------|------|-------------|
338	| `public/data/frames/configs/3.json` | 含表达式字段的接收帧定义（条件表达式、变量映射、自引用） | 高 — 表达式配置结构 oracle |
339	| `public/data/frames/configs/*.json`（25 个文件含 expressionConfig） | 各类帧定义，部分含表达式 | 中 — 多样化配置样本 |
340	| `public/data/templates/framesConfig.json` | 帧配置模板 | 中 — 完整帧结构 oracle |
341	| `public/data/templates/sendInstances.json` | 发送实例模板（含表达式字段） | 高 — 发送帧表达式 oracle |
342	| `public/data/templates/scoeReceiveCommands.json` | SCOE 接收指令（含 params + completionConditions） | 高 — 条件判断 oracle |
343	| `public/data/scoe/satelliteConfigs/1.json` | 卫星配置 | 中 — SCOE 识别参数 oracle |
344	| `public/data/scoe/scoeConfigs/1.json` | SCOE 全局配置 | 中 — SCOE 帧识别偏移 oracle |
345	
346	---
347	
348	## 五、可观测行为保留/排除汇总
349	
350	### 必须保留（核心业务行为）
351	
352	| # | 行为 | 归口 feature | Oracle |
353	|---|------|-------------|--------|
354	| 1 | 条件-表达式对顺序评估，默认值 0 | shared/ 表达式引擎 | configs/3.json |
355	| 2 | 13 种数学函数注入（Math 全对象 + abs/ceil/floor/round/max/min/sin/cos/tan/sqrt/log/exp/pow） | shared/ 表达式引擎 | 代码 |
356	| 3 | 四种变量数据源（CURRENT_FIELD / FRAME_FIELD / GLOBAL_STAT / SCOE_DATA），未解析默认 0 | shared/ 变量解析 | configs/3.json |
357	| 4 | 拓扑排序（Kahn 算法），循环依赖检测，按序计算并即时更新上下文 | shared/ 表达式引擎 | configs/3.json（自引用） |
358	| 5 | 类型处理（float/double 保持原值，其他整数类型 Math.floor） | shared/ 或 frame | 代码 |
359	| 6 | 接收帧解析后立即计算表达式；发送帧组帧前计算表达式 | receive/send feature | 代码调用链 |
360	| 7 | 11 种数据类型解析规则（含 BigInt 64 位、DataView float/double、bytes ASCII 模式） | frame feature | 配置样本 |
361	| 8 | 大端/小端字节序 | frame feature | 配置样本 bigEndian |
362	| 9 | applyFactor（乘以 factor，toFixed(5) 限 5 位小数） | frame feature | 配置样本 factor |
363	| 10 | 帧识别规则（8 种运算符，AND 逻辑） | frame/receive feature | 帧定义 identifierRules |
364	| 11 | direct/indirect 数据参与类型 | frame feature | configs/3.json |
365	| 12 | 四种校验和算法（xor8/sum8/crc16/crc32） | frame feature | 配置样本 validOption |
366	| 13 | 标签显示（labelOptions 十六进制匹配） | receive feature | 配置样本 |
367	| 14 | 发送触发条件（5 种操作符，AND/OR 短路逻辑） | send/task feature | TriggerCondition 接口 |
368	| 15 | SCOE 完成条件（固定值模式 + 参数索引匹配模式，AND 逻辑，定时轮询 + 超时） | 指令接入 feature | scoeReceiveCommands.json |
369	| 16 | 通用比较运算符（6 种，自动数值/字符串检测） | shared/ | 代码 |
370	| 17 | SCOE 帧多步骤识别流程 | 指令接入 feature | scoeFrame.ts |
371	| 18 | SCOE 校验和验证（累加取模 256） | 指令接入 feature | scoeReceiveCommands.json |
372	| 19 | 错误容错（不崩溃、错误不应用、console.error 记录） | shared/ + 各 feature | 代码 |
373	
374	### 可排除（非核心或需重新设计）
375	
376	| # | 行为 | 排除理由 |
377	|---|------|----------|
378	| 1 | `new Function` 求值方式 | 实现细节，新系统用 AST/mathjs 替代，保持等价语义即可 |
379	| 2 | 依赖缓存（5 分钟 TTL、50 条上限、配置哈希） | 性能优化实现细节，新系统自行决定缓存策略 |
380	| 3 | 计算历史记录（`calculationHistory`，上限 100 条） | 调试辅助，非核心业务行为 |
381	| 4 | `globalStatsStore` 直接依赖 | 新系统通过 feature public API 间接访问，不直接依赖 store |
382	| 5 | `scoeStore` 直接依赖 | 新系统通过指令接入 feature public API 访问 |
383	| 6 | `receiveFramesStore` 直接依赖 | 新系统通过 feature public API 访问 |
384	| 7 | `frameTemplateStore` 直接依赖 | 新系统通过 frame feature public API 访问 |
385	| 8 | 表达式中 `extractVariablesFromExpression` 的正则提取方式 | 实现细节，新系统可用 AST 分析替代 |
386	
387	---
388	
389	## 后续
390	
391	无。本调研为纯事实提取，后续由设计/实施对话消费。
392	
```

> TOOL

tool_result
id: call_da4ebaf690b042bcb738dacc
```
1	# [S004-Agent5] 旧系统数据存储、历史记录与 CSV 导出可观测行为提取
2	
3	> 2026-05-19 | 调研 | 完成
4	> 来源文件：8 个核心文件 + 类型定义 + 辅助工具
5	
6	## 目标
7	
8	提取旧系统在数据存储、历史记录管理、CSV 导出、高速存储、全局统计、数据展示方面的全部可观测业务行为，供新系统 receive-real / storage / visualization feature 参考。
9	
10	---
11	
12	## 一、历史数据存储行为
13	
14	### 1.1 存储介质：JSON 文件，按小时分文件
15	
16	**旧行为**：历史数据存储为 JSON 文件，文件路径 `{userDataPath}/data/history-statistics/{hourKey}.json`，hourKey 格式 `YYYY-MM-DD-HH`（如 `2026-05-19-14`）。支持 gzip 压缩，压缩后为 `.json.gz`。同一小时只保留一个文件（压缩或未压缩二选一）。
17	
18	- **代码位置**：
19	  - `src-electron/main/ipc/historyDataHandlers.ts:34-52` — `getHistoryDataDirectory()` 和 `getFilePath()`
20	  - `src-electron/main/ipc/historyDataHandlers.ts:55-59` — `isCompressed()` 优先检查 .json.gz
21	- **新系统对应**：storage feature
22	- **oracle 评估**：代码完整，行为明确
23	- **建议**：保留。按小时分文件的设计在高频采集场景下合理，新系统可保留此策略或改为 SQLite 但必须保持等价的按小时查询能力
24	
25	### 1.2 文件结构：HourlyDataFile
26	
27	**旧行为**：每个小时文件结构为 `HourlyDataFile`：
28	```ts
29	{
30	  metadata: {
31	    version: '1.0.0',
32	    hourKey: 'YYYY-MM-DD-HH',
33	    groups: GroupMetadata[],   // 分组+数据项元数据
34	    totalDataItems: number,
35	    createdAt: number,         // 时间戳
36	    updatedAt: number,
37	  },
38	  records: HistoryDataRecord[] // { timestamp, data: unknown[] }
39	}
40	```
41	`records[].data` 是一个扁平数组，所有分组的所有数据项按全局索引顺序存储。
42	
43	- **代码位置**：
44	  - `src/types/storage/historyData.ts:8-40` — 类型定义
45	  - `src/stores/frames/dataDisplayStore.ts:338-352` — `createHistoryDataRecord()` 构建逻辑
46	- **新系统对应**：storage feature
47	- **oracle 评估**：代码完整
48	- **建议**：保留。新系统存储格式可自由选择，但必须能表达相同的分组元数据+时间序列记录语义
49	
50	### 1.3 增量写入（批量追加）
51	
52	**旧行为**：支持通过 `appendBatchRecords` 增量追加记录到已有小时文件。如果文件已存在，解析后追加 records；如果不存在，使用传入的 metadata 创建新文件。写入后更新 `updatedAt` 时间戳。
53	
54	- **代码位置**：`src-electron/main/ipc/historyDataHandlers.ts:102-157`
55	- **新系统对应**：storage feature 的写入 API
56	- **oracle 评估**：代码完整
57	- **建议**：保留增量写入能力，但新系统应考虑写性能优化（批量 append、fsync 策略等）
58	
59	### 1.4 定期保存触发机制
60	
61	**旧行为**：
62	1. **数据收集定时器**：常开模式，默认每 1 秒（`updateInterval: 1000`）执行 `collectCurrentData()`
63	2. **历史数据保存定时器**：仅在 recording 启用时运行，默认每 5 分钟（`csvSaveInterval` 设置，单位分钟，默认 5）触发 `saveAllHistoryBatches()`
64	3. **小时边界检测**：`collectCurrentData()` 中检测小时切换，切换时自动保存上一小时数据
65	4. **停止记录时**：保存所有未保存的批次数据
66	
67	- **代码位置**：
68	  - `src/stores/frames/dataDisplayStore.ts:554-553` — `startDataCollection()`
69	  - `src/stores/frames/dataDisplayStore.ts:596-630` — `startRecordingTimers()`
70	  - `src/stores/frames/dataDisplayStore.ts:362-374` — 小时边界检测
71	  - `src/stores/frames/dataDisplayStore.ts:717-732` — `stopRecording()`
72	- **新系统对应**：receive-real + storage feature 协作
73	- **oracle 评估**：代码完整
74	- **建议**：保留。定时收集+定期持久化+小时边界自动切换是核心行为
75	
76	### 1.5 自动开始记录
77	
78	**旧行为**：应用启动时，如果 `settingsStore.autoStartRecording` 为 true（默认 true），自动调用 `dataDisplayStore.startRecording()`。
79	
80	- **代码位置**：`src/layouts/useAppLifecycle.ts:65-68`
81	- **新系统对应**：app lifecycle + receive feature
82	- **oracle 评估**：代码完整
83	- **建议**：保留此设置项和行为
84	
85	### 1.6 内存中缓存机制
86	
87	**旧行为**：
88	1. **循环缓冲区**：`CircularBuffer<DataRecord>`，按 groupId 索引。容量根据活跃图表数动态调整（0 图表=1000，1 图表=5000，2 图表=3000）
89	2. **historyBatches**：`Map<hourKey, HourlyDataFile>`，用于记录模式下积累未保存数据
90	3. **延迟清理**：每 10 秒检查一次，根据活跃图表数调整缓冲区容量
91	4. **时间过期清理**：每小时检查，移除超过 `maxHistoryHours`（默认 24 小时）的旧记录
92	
93	- **代码位置**：
94	  - `src/stores/frames/dataDisplayStore.ts:51-115` — `CircularBuffer` 类
95	  - `src/stores/frames/dataDisplayStore.ts:160-161` — `historyRecordsCache`
96	  - `src/stores/frames/dataDisplayStore.ts:247-274` — `performDelayedCleanup()`
97	  - `src/stores/frames/dataDisplayStore.ts:739-763` — `cleanHistoryRecords()`
98	- **新系统对应**：storage + visualization feature
99	- **oracle 评估**：代码完整，性能优化策略清晰
100	- **建议**：保留动态容量调整策略。新系统可优化实现但应保持等价效果
101	
102	---
103	
104	## 二、历史数据查询行为
105	
106	### 2.1 查询可用小时键
107	
108	**旧行为**：扫描 `{userDataPath}/data/history-statistics/` 目录，列出所有 `.json` 或 `.json.gz` 文件，提取文件名作为 hourKey，去重排序返回。
109	
110	- **代码位置**：
111	  - `src-electron/main/ipc/historyDataHandlers.ts:81-99` — `getAvailableHours`
112	  - `src/stores/historyAnalysis.ts:158-166` — `fetchAvailableHours()`
113	- **新系统对应**：storage feature 查询 API
114	- **oracle 评估**：代码完整
115	- **建议**：保留。用户需要能看到哪些小时有数据
116	
117	### 2.2 按时间范围批量加载
118	
119	**旧行为**：给定时间范围，生成所有覆盖的 hourKey 列表，批量加载对应文件，合并 records 并按时间戳排序。返回 `Record<hourKey, HourlyDataFile>` 格式。
120	
121	- **代码位置**：
122	  - `src-electron/main/ipc/historyDataHandlers.ts:557-620` — `loadMultipleHours`
123	  - `src/stores/historyAnalysis.ts:174-230` — `loadHistoryData()`
124	- **新系统对应**：storage feature 批量查询
125	- **oracle 评估**：代码完整
126	- **建议**：保留。批量按小时加载是新系统 history analysis 页面的核心查询模式
127	
128	### 2.3 历史数据按分组/数据项过滤
129	
130	**旧行为**：加载后，用户可在左侧面板选择分组和数据项（`DataItemSelection`），`filteredData` 计算属性按时间范围过滤。图表数据 `chartDataSets` 按图表配置过滤到特定 groupId + dataItemId。
131	
132	- **代码位置**：
133	  - `src/stores/historyAnalysis.ts:93-107` — `filteredData`
134	  - `src/stores/historyAnalysis.ts:110-153` — `chartDataSets`
135	  - `src/stores/historyAnalysis.ts:233-278` — 数据项选择管理方法
136	- **新系统对应**：visualization feature
137	- **oracle 评估**：代码完整
138	- **建议**：保留。按分组/数据项选择和多图表展示是历史数据分析的核心交互
139	
140	### 2.4 多图表展示
141	
142	**旧行为**：支持 1-4 个图表并行显示（`MultiChartSettings`），每个图表可独立选择数据项、配置标题和 Y 轴（自动缩放、统计计算）。图表配置通过 `useStorage` 持久化到 localStorage。
143	
144	- **代码位置**：
145	  - `src/stores/historyAnalysis.ts:46-55` — `multiChartSettings`
146	  - `src/stores/historyAnalysis.ts:281-362` — 图表管理方法
147	  - `src/pages/HistoryAnalysisPage.vue:267-430` — 页面布局
148	- **新系统对应**：visualization feature
149	- **oracle 评估**：代码完整
150	- **建议**：保留。多图表+独立配置是关键用户交互
151	
152	---
153	
154	## 三、CSV 导出行为
155	
156	### 3.1 CSV 导出配置
157	
158	**旧行为**：CSV 导出通过 `CSVExportDialog` 组件触发，用户可配置：
159	- **文件名**：自定义或自动生成（格式 `history_data_YYYYMMDD_HHmmss`）
160	- **时间范围**：使用当前 historyAnalysis store 中的 timeRange
161	- **选中数据项**：从 `dataItemSelections` 中选择
162	- **包含表头**：可选，默认包含
163	- **包含时间戳**：可选，默认包含
164	- **输出方式**：预设路径（`settings.csvDefaultOutputPath`）或手动选择（系统保存对话框）
165	- **时间格式选项**：`YYYY-MM-DD HH:mm:ss`、`YYYY/MM/DD HH:mm:ss`、`MM/DD/YYYY HH:mm:ss`、`DD.MM.YYYY HH:mm:ss`、`ISO 8601`、`Unix 时间戳`
166	
167	- **代码位置**：
168	  - `src/components/storage/CSVExportDialog.vue:1-401` — 完整对话框
169	  - `src/types/storage/historyData.ts:115-131` — `CSVExportConfig` 类型
170	- **新系统对应**：storage feature 导出 + UI 页面
171	- **oracle 评估**：代码完整，UI 交互完整
172	- **建议**：保留。CSV 导出是用户关键需求，时间格式选项和预设路径行为应保留
173	
174	### 3.2 CSV 生成逻辑
175	
176	**旧行为**：
177	1. 根据时间范围生成 hourKey 列表
178	2. 批量加载对应文件（支持压缩文件）
179	3. 合并、按时间范围过滤、按时间戳排序
180	4. 生成 CSV：
181	   - 分隔符：逗号（`,`）
182	   - 编码：UTF-8
183	   - 表头格式：`timestamp` 或自定义，数据项表头为 `{groupLabel}_{dataItemLabel}`
184	   - 时间戳格式：`YYYY-MM-DD HH:MM:SS`（ISO 格式去掉 T 和毫秒 Z）
185	   - 每行按选中数据项的 metadata index 从 `record.data[]` 取值
186	   - 空值用空字符串表示
187	5. 写入文件
188	
189	- **代码位置**：`src-electron/main/ipc/historyDataHandlers.ts:305-474`
190	- **新系统对应**：storage feature 导出
191	- **oracle 评估**：代码完整，格式逻辑清晰
192	- **建议**：保留。CSV 逗号分隔+UTF-8+表头命名规则+时间戳格式是可观测行为
193	
194	### 3.3 快捷键 Ctrl+E 导出
195	
196	**旧行为**：在 HistoryAnalysisPage 按 Ctrl+E 打开导出对话框（前提：有选中数据项）。
197	
198	- **代码位置**：`src/pages/HistoryAnalysisPage.vue:232-244`
199	- **新系统对应**：UI 交互
200	- **oracle 评估**：代码完整
201	- **建议**：排除。快捷键是 UI 细节，非核心业务行为，新系统自行决定
202	
203	---
204	
205	## 四、数据导入/导出行为（配置数据）
206	
207	### 4.1 JSON 配置数据导入导出
208	
209	**旧行为**：通过 `DataStorageManager` 和 `dataStorageApi`，支持以下数据类型的 CRUD + 导入导出：
210	- `framesConfig` — 帧配置模板
211	- `sendInstances` — 发送实例
212	- `receiveConfig` — 接收配置
213	- `scoeSatelliteConfigs` — SCOE 卫星配置
214	- `scoeFramesSendInstances` — SCOE 发送实例
215	- `scoeFramesReceiveCommands` — SCOE 接收命令
216	
217	每个类型统一提供 `list` / `save` / `delete` / `saveAll` / `export` / `import` 六个操作。导出为 JSON 文件，导入也仅支持 JSON。存储路径为 `{userDataPath}/{dirPath}.json`。
218	
219	- **代码位置**：
220	  - `src/config/configDefaults.ts:1-17` — `DATA_PATH_MAP`
221	  - `src-electron/main/ipc/dataStorageHandlers.ts:1-198` — `DataStorageManager` + handler 注册
222	  - `src/api/common/dataStorageApi.ts:1-90` — renderer 侧 API 封装
223	  - `src/components/common/ImportExportActions.vue:1-133` — UI 组件
224	- **新系统对应**：各 feature 的持久化层
225	- **oracle 评估**：代码完整
226	- **建议**：保留配置数据的导入导出能力。这是用户迁移和备份配置的需求。但新系统不采用旧的通用 DataStorageManager 模式，各 feature 自行管理持久化
227	
228	---
229	
230	## 五、高速存储行为
231	
232	### 5.1 触发条件
233	
234	**旧行为**：在 main 进程的网络数据接收处理中，每收到一帧数据都检查高速存储规则：
235	1. 存储功能必须 enabled
236	2. 规则必须存在且 enabled
237	3. 规则的 connectionId 必须匹配当前连接 ID（支持 `network:connId:remoteId` 格式，提取中间的 connId）
238	4. 帧头必须匹配规则中的任一 headerPattern（十六进制字符串逐字节比较）
239	
240	**关键行为**：匹配高速存储规则的数据**不会发送到渲染进程**（`return` 跳过 `emitDataEvent`），只有非业务数据才发送到渲染进程。
241	
242	- **代码位置**：
243	  - `src-electron/main/ipc/networkHandlers.ts:498-521` — `handleDataReceived()`
244	  - `src-electron/main/ipc/highSpeedStorageHandlers.ts:77-119` — `shouldStore()` + `matchFrameHeader()`
245	- **新系统对应**：receive-real + storage（高速存储路径）
246	- **oracle 评估**：代码完整，行为非常明确
247	- **建议**：保留。业务数据与遥测数据分流是关键架构决策，新系统必须保持等价行为
248	
249	### 5.2 存储文件格式
250	
251	**旧行为**：
252	- 存储路径：`{userDataPath}/business-data/business_data_{ISO-timestamp}.txt`
253	- 文件名中的 ISO timestamp 的 `:` 和 `.` 替换为 `-`
254	- 每帧数据写为一行十六进制大写字符串（`Array.from(data).map(byte => byte.toString(16).padStart(2, '0').toUpperCase()).join('')`）
255	- 使用 `createWriteStream` 追加写入（flags: 'a'）
256	
257	- **代码位置**：
258	  - `src-electron/main/ipc/highSpeedStorageHandlers.ts:142-146` — `generateFilePath()`
259	  - `src-electron/main/ipc/highSpeedStorageHandlers.ts:248-271` — `storeData()`
260	- **新系统对应**：storage feature（高速路径）
261	- **oracle 评估**：代码完整
262	- **建议**：保留。十六进制每行一帧的格式简单高效，新系统可保持或改为二进制格式但需保持读写能力
263	
264	### 5.3 文件轮转策略
265	
266	**旧行为**：
267	- 默认最大文件大小 100MB（`maxFileSize: 100`）
268	- 默认启用轮转（`enableRotation: true`）
269	- 默认保留 5 个轮转文件（`rotationCount: 5`）
270	- 文件达到大小限制时：关闭当前流 -> 清理旧文件 -> 初始化新流
271	- 清理旧文件：按修改时间降序排列，保留最新的 N 个，删除其余
272	
273	- **代码位置**：
274	  - `src-electron/main/ipc/highSpeedStorageHandlers.ts:180-241` — `checkFileRotation()` + `cleanupOldFiles()`
275	  - `src/stores/highSpeedStorageStore.ts:22-28` — 默认配置
276	- **新系统对应**：storage feature
277	- **oracle 评估**：代码完整
278	- **建议**：保留。文件轮转是防止磁盘占满的必要机制，100MB/5 文件是合理默认值
279	
280	### 5.4 高速存储统计
281	
282	**旧行为**：维护实时统计信息：
283	- `totalFramesStored` — 总存储帧数
284	- `totalBytesStored` — 总存储字节数
285	- `currentFileSize` — 当前文件大小（估算：每帧 `dataSize * 2 + 1` 字节）
286	- `storageStartTime` / `lastStorageTime` — 开始/最后存储时间
287	- `frameTypeStats` — 按规则 ID 统计帧数
288	- `isStorageActive` — 存储是否活跃
289	- `currentFilePath` — 当前写入文件路径
290	
291	- **代码位置**：
292	  - `src-electron/main/ipc/highSpeedStorageHandlers.ts:278-291` — `updateStats()`
293	  - `src/types/serial/highSpeedStorage.ts:29-38` — `StorageStats` 类型
294	- **新系统对应**：storage feature 统计
295	- **oracle 评估**：代码完整
296	- **建议**：保留。用户需要看到存储状态和统计
297	
298	### 5.5 高速存储配置持久化
299	
300	**旧行为**：配置通过 `useStorage('highSpeedStorageConfig', ...)` 持久化到 localStorage。初始化时与 main 进程双向同步（main 有配置则以 main 为准，否则将本地配置同步到 main）。
301	
302	- **代码位置**：`src/stores/highSpeedStorageStore.ts:22-28` 和 `src/stores/highSpeedStorageStore.ts:245-264`
303	- **新系统对应**：storage feature 配置管理
304	- **oracle 评估**：代码完整
305	- **建议**：保留。但新系统应统一配置持久化策略，不依赖 localStorage
306	
307	### 5.6 重置统计 = 删除当前文件
308	
309	**旧行为**：`resetStats()` 不仅重置统计数字，还关闭当前写入流并**删除当前存储文件**。
310	
311	- **代码位置**：`src-electron/main/ipc/highSpeedStorageHandlers.ts:350-388`
312	- **新系统对应**：storage feature
313	- **oracle 评估**：代码完整
314	- **建议**：保留。重置 = 清空是合理语义
315	
316	---
317	
318	## 六、全局统计行为
319	
320	### 6.1 统计指标
321	
322	**旧行为**：`globalStatsStore` 维护四类统计：
323	
324	**系统统计**（每秒更新）：
325	- `uptime` — 运行时间（秒）
326	- `year/month/day/hour/minute/second/millisecond` — 当前时间分解
327	- `allSeconds` — Unix 时间戳（秒）
328	- `startTime` — 应用启动时间戳
329	
330	**通信统计**：
331	- `sentPackets` / `receivedPackets` — 收发包计数
332	- `sentBytes` / `receivedBytes` — 收发字节数
333	
334	**帧匹配统计**：
335	- `matchedFrames` — 匹配成功帧数
336	- `unmatchedFrames` — 未匹配帧数
337	
338	**错误统计**：
339	- `communicationErrors` — 通信错误数
340	- `frameParseErrors` — 帧解析错误数
341	
342	- **代码位置**：
343	  - `src/stores/globalStatsStore.ts:17-84` — 状态定义和计算属性
344	  - `src/stores/globalStatsStore.ts:136-168` — 增量更新方法
345	- **新系统对应**：可能归 connection / receive / 各 feature 分别维护
346	- **oracle 评估**：代码完整
347	- **建议**：保留。所有统计指标都有观测价值。新系统可拆分到各 feature 但需保持等价的汇总能力
348	
349	### 6.2 统计更新频率
350	
351	**旧行为**：系统统计每秒更新一次（`interval: 1000`），通信/帧/错误统计通过 increment 方法实时更新。
352	
353	- **代码位置**：`src/stores/globalStatsStore.ts:92-99`
354	- **新系统对应**：各 feature 统计
355	- **oracle 评估**：代码完整
356	- **建议**：保留每秒时间更新 + 实时递增的模式
357	
358	### 6.3 统计供表达式引擎消费
359	
360	**旧行为**：`availableStats` 计算属性将所有统计汇总为一个扁平对象，`getStatValue(statKey)` 方法供表达式系统按名称获取统计值。
361	
362	- **代码位置**：`src/stores/globalStatsStore.ts:55-86` 和 `src/stores/globalStatsStore.ts:171-173`
363	- **新系统对应**：shared/ 表达式引擎 + 各 feature 统计注入
364	- **oracle 评估**：代码完整
365	- **建议**：保留。表达式引擎需要访问统计值是新系统的既定需求
366	
367	### 6.4 统计重置
368	
369	**旧行为**：`resetStats()` 将所有四类统计归零。
370	
371	- **代码位置**：`src/stores/globalStatsStore.ts:176-210`
372	- **新系统对应**：各 feature 统计管理
373	- **oracle 评估**：代码完整
374	- **建议**：保留。用户需要重置统计的能力
375	
376	### 6.5 位置信息
377	
378	**旧行为**：初始化时调用 `location.fetchLocation()` 获取经纬度，存入 `systemStats.latitude` / `systemStats.longitude`（整数，精确到分）。
379	
380	- **代码位置**：`src/stores/globalStatsStore.ts:88-106` 和 `src/stores/globalStatsStore.ts:122-133`
381	- **新系统对应**：待定（可能归 platform facade）
382	- **oracle 评估**：代码完整
383	- **建议**：保留位置信息获取能力，但新系统应通过 platform facade 提供
384	
385	---
386	
387	## 七、数据展示行为
388	
389	### 7.1 实时数据表格展示
390	
391	**旧行为**：两个独立表格（table1 / table2），每个表格可配置：
392	- 选择一个分组（`selectedGroupId`）
393	- 三种显示模式：`table`（数值表格）、`chart`（曲线图）、`special`（星座图）
394	- 图表模式下可选中特定数据项（`chartSelectedItems`）
395	
396	表格模式下每行显示：编号、标签、displayValue、hexValue、可见性、收藏标记。
397	
398	- **代码位置**：
399	  - `src/stores/frames/dataDisplayStore.ts:118-128` — table 配置
400	  - `src/stores/frames/dataDisplayStore.ts:286-302` — `getTableData()`
401	- **新系统对应**：visualization feature
402	- **oracle 评估**：代码完整
403	- **建议**：保留双表格+三模式的展示能力
404	
405	### 7.2 星座图模式
406	
407	**旧行为**：`special` 模式下显示 IQ 星座图：
408	- 配置：`bitWidth`（位宽，默认 12）、`sampleCount`（采样数，默认 16）、`pointSize`（点大小）
409	- 数据源：分别配置 I 路和 Q 路的 frameId + fieldId
410	- 刷新间隔：可配置，默认 1000ms
411	- 数据处理：从 hex 字符串按 bitWidth 提取数值，支持有符号数
412	- I 路取前一半采样，Q 路取后一半采样
413	- 使用定时器定期刷新显示数据（refreshConstellationData -> clear 已累积数据）
414	
415	- **代码位置**：
416	  - `src/stores/frames/dataDisplayStore.ts:25-42` — `ConstellationConfig` 类型
417	  - `src/stores/frames/dataDisplayStore.ts:131-147` — 配置持久化
418	  - `src/stores/frames/dataDisplayStore.ts:806-906` — 星座图数据管理
419	- **新系统对应**：visualization feature（星座图子组件）
420	- **oracle 评估**：代码完整
421	- **建议**：保留。星座图是卫星通信领域的标准可视化需求
422	
423	### 7.3 数据收集时机
424	
425	**旧行为**：`collectCurrentData()` 在以下条件之一满足时才执行实际数据收集：
426	1. table1 或 table2 处于 chart 模式且选中了分组
427	2. 正在 recording
428	
429	否则直接跳过（性能优化）。收集时只处理被用到的分组的被选中数据项。
430	
431	- **代码位置**：`src/stores/frames/dataDisplayStore.ts:394-403` — 早期退出判断
432	- **新系统对应**：receive-real 数据分发
433	- **oracle 评估**：代码完整
434	- **建议**：保留按需收集的优化策略
435	
436	### 7.4 hex 转换缓存
437	
438	**旧行为**：使用 LRU 缓存（最大 1000 条）缓存 hex 转换结果，避免重复计算。缓存满时清理前半部分。
439	
440	- **代码位置**：`src/stores/frames/dataDisplayStore.ts:168-169` 和 `src/stores/frames/dataDisplayStore.ts:222-244`
441	- **新系统对应**：shared/ 或 visualization 内部优化
442	- **oracle 评估**：代码完整
443	- **建议**：排除。这是性能优化细节，新系统自行决定缓存策略
444	
445	---
446	
447	## 八、数据清理行为
448	
449	### 8.1 历史数据过期清理
450	
451	**旧行为**：`cleanupOldData(daysToKeep)` 按 hourKey 字符串比较，删除早于 cutoff 日期的文件。支持同时删除 .json 和 .json.gz。
452	
453	- **代码位置**：`src-electron/main/ipc/historyDataHandlers.ts:512-554`
454	- **新系统对应**：storage feature
455	- **oracle 评估**：代码完整
456	- **建议**：保留。按天保留策略是必要的磁盘管理功能
457	
458	### 8.2 删除特定小时数据
459	
460	**旧行为**：`deleteHourData(hourKey)` 可删除指定小时的文件（同时删 .json 和 .json.gz）。
461	
462	- **代码位置**：`src-electron/main/ipc/historyDataHandlers.ts:477-509`
463	- **新系统对应**：storage feature
464	- **oracle 评估**：代码完整
465	- **建议**：保留。用户需要手动删除特定小时数据的能力
466	
467	### 8.3 压缩小时数据
468	
469	**旧行为**：`compressHourData(hourKey)` 将未压缩的 .json 文件 gzip 压缩为 .json.gz，然后删除原文件。
470	
471	- **代码位置**：`src-electron/main/ipc/historyDataHandlers.ts:160-192`
472	- **新系统对应**：storage feature
473	- **oracle 评估**：代码完整
474	- **建议**：保留。自动压缩旧数据节省磁盘空间
475	
476	### 8.4 内存循环缓冲区容量动态调整
477	
478	**旧行为**：根据活跃图表数（0/1/2）动态设置循环缓冲区容量（1000/5000/3000），每 10 秒检查一次。
479	
480	- **代码位置**：`src/stores/frames/dataDisplayStore.ts:247-274`
481	- **新系统对应**：visualization 或 storage
482	- **oracle 评估**：代码完整
483	- **建议**：保留动态调整语义，具体数值新系统可调
484	
485	---
486	
487	## 九、存储统计查询
488	
489	### 9.1 历史数据存储统计
490	
491	**旧行为**：`getStorageStats()` 返回：
492	- `totalFiles` — 总文件数
493	- `totalSize` — 总大小（字节）
494	- `totalRecords` — 总记录数（简化处理，代码中注释说明实际需遍历所有文件）
495	- `dateRange` — 最早/最新日期
496	- `compressionRatio` — 压缩比
497	
498	- **代码位置**：`src-electron/main/ipc/historyDataHandlers.ts:241-302`
499	- **新系统对应**：storage feature
500	- **oracle 评估**：代码完整，totalRecords 为已知简化
501	- **建议**：保留。存储统计是用户管理磁盘空间的依据
502	
503	---
504	
505	## 十、汇总：新系统各 feature 需保留的核心行为清单
506	
507	| 编号 | 行为 | 旧代码位置 | 新系统归属 | 保留/排除 |
508	|------|------|-----------|-----------|----------|
509	| H-01 | JSON 文件按小时存储历史数据 | historyDataHandlers.ts:34-52 | storage | 保留 |
510	| H-02 | HourlyDataFile 结构（分组元数据+时间序列） | types/storage/historyData.ts:8-40 | storage | 保留 |
511	| H-03 | 增量追加记录到小时文件 | historyDataHandlers.ts:102-157 | storage | 保留 |
512	| H-04 | 定时收集（1s）+ 定期持久化（5min）+ 小时边界切换 | dataDisplayStore.ts:554-630 | receive + storage | 保留 |
513	| H-05 | 自动开始记录（可配置） | useAppLifecycle.ts:65-68 | app lifecycle | 保留 |
514	| H-06 | 循环缓冲区 + 动态容量 + 时间过期清理 | dataDisplayStore.ts:51-274 | storage/visualization | 保留 |
515	| H-07 | 查询可用小时键 + 按时间范围批量加载 | historyDataHandlers.ts:81-620 | storage | 保留 |
516	| H-08 | 历史数据按分组/数据项过滤 + 多图表展示 | historyAnalysis.ts:93-362 | visualization | 保留 |
517	| C-01 | CSV 导出（文件名/时间范围/数据项选择/表头/时间戳/预设路径） | CSVExportDialog.vue + historyDataHandlers.ts:305-474 | storage + UI | 保留 |
518	| C-02 | CSV 格式：逗号分隔、UTF-8、{group}_{item} 表头、ISO 时间戳 | historyDataHandlers.ts:403-456 | storage | 保留 |
519	| D-01 | JSON 配置导入导出（帧/发送/接收/SCOE） | dataStorageHandlers.ts + dataStorageApi.ts | 各 feature 持久化 | 保留 |
520	| S-01 | 高速存储：帧头匹配 + 连接 ID 匹配触发 | networkHandlers.ts:498-521 | receive + storage | 保留 |
521	| S-02 | 匹配高速存储规则的数据不发送到渲染进程 | networkHandlers.ts:515-517 | receive | 保留（关键） |
522	| S-03 | 高速存储文件格式：每帧一行十六进制大写 | highSpeedStorageHandlers.ts:248-271 | storage | 保留 |
523	| S-04 | 文件轮转：100MB 上限 + 保留 5 个 + 按时间排序清理 | highSpeedStorageHandlers.ts:180-241 | storage | 保留 |
524	| S-05 | 高速存储统计（帧数/字节数/文件大小/活跃状态） | highSpeedStorageHandlers.ts:278-291 | storage | 保留 |
525	| S-06 | 重置统计 = 删除当前文件 | highSpeedStorageHandlers.ts:350-388 | storage | 保留 |
526	| G-01 | 全局统计：时间/通信/帧匹配/错误四类 | globalStatsStore.ts:17-84 | 各 feature | 保留 |
527	| G-02 | 统计每秒更新 + 实时递增 | globalStatsStore.ts:92-168 | 各 feature | 保留 |
528	| G-03 | 统计供表达式引擎消费 | globalStatsStore.ts:55-86, 171-173 | shared/ 表达式 | 保留 |
529	| G-04 | 位置信息获取 | globalStatsStore.ts:122-133 | platform facade | 保留 |
530	| V-01 | 双表格+三模式（table/chart/constellation） | dataDisplayStore.ts:118-302 | visualization | 保留 |
531	| V-02 | 星座图（IQ 数据源配置 + 按位宽提取 + 定时刷新） | dataDisplayStore.ts:806-906 | visualization | 保留 |
532	| CL-01 | 过期数据清理（按天保留） | historyDataHandlers.ts:512-554 | storage | 保留 |
533	| CL-02 | 删除指定小时数据 | historyDataHandlers.ts:477-509 | storage | 保留 |
534	| CL-03 | 压缩旧数据文件（gzip） | historyDataHandlers.ts:160-192 | storage | 保留 |
535	| -- | Ctrl+E 快捷键导出 | HistoryAnalysisPage.vue:232-244 | UI | 排除 |
536	| -- | hex 转换 LRU 缓存 | dataDisplayStore.ts:168-244 | 内部优化 | 排除 |
537	
538	---
539	
540	## 后续
541	
542	无。本文档已完成全部 8 个核心文件的事实提取，所有行为已标注代码位置、新系统对应归属和保留/排除建议。
543	
```

> TOOL

tool_use Read
id: call_435e035495624e8d84c7cbda
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-agent7-status-indicators.md"
}
```

> TOOL

tool_use Read
id: call_3e47b3c7049d473393df26b9
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-agent8-settings-config.md"
}
```

> TOOL

tool_use Read
id: call_f85b4c99592b45b5928f5c09
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-agent9-routes-pages.md"
}
```

> TOOL

tool_result
id: call_435e035495624e8d84c7cbda
```
1	# [S004-Agent7] 状态指示、健康检查和统计展示 — 旧系统可观测行为提取
2	
3	> 2026-05-19 | 事实提取 | 状态: 完成
4	
5	## 目标
6	
7	提取旧系统中所有与状态指示、健康检查、统计展示相关的可观测业务行为，作为新系统保留/排除的依据。
8	
9	---
10	
11	## 一、连接状态指示
12	
13	### 行为 1: 网络连接四态展示
14	
15	- **旧行为**: 网络连接有四种状态：`idle`（未连接）、`connecting`（连接中）、`connected`（已连接）、`error`（连接失败）。每种状态有独立的颜色（grey/green/orange/red）、图标（wifi_off/wifi/wifi_find/wifi_off）和文本（未连接/已连接/连接中/连接失败）。
16	- **代码位置**: `src/components/connect/NetworkConnectionCard.vue:22-48`（getStatusColor/getStatusIcon/getStatusText 函数）
17	- **状态类型定义**: `src/types/serial/network.ts:9` — `NetworkConnectionStatus = 'connected' | 'disconnected' | 'connecting' | 'error'`
18	- **新系统对应 feature**: connection feature
19	- **Oracle 来源**: 代码 + 类型定义，证据充分
20	- **建议**: **保留**。四态模型是连接管理的核心可观测行为，新系统 connection feature 应保留等价状态。
21	
22	### 行为 2: 串口连接四态展示
23	
24	- **旧行为**: 串口连接同样有四种状态：`disconnected`、`connecting`、`connected`、`error`。通过 `ConnectionStatus` 类型定义，UI 用 check_circle 绿色图标标识已连接。
25	- **代码位置**: `src/types/serial/serial.ts:66` — `ConnectionStatus = 'disconnected' | 'connecting' | 'connected' | 'error'`
26	- **代码位置**: `src/stores/serialStore.ts:42` — `portConnectionStatuses`
27	- **新系统对应 feature**: connection feature
28	- **Oracle 来源**: 类型定义 + store，证据充分
29	- **建议**: **保留**。与网络连接状态模型一致。
30	
31	### 行为 3: 网络连接卡片网格展示（最多 9 个）
32	
33	- **旧行为**: 连接管理页面用 3 列网格展示所有网络连接配置卡片，上限 9 个。每张卡片显示连接名称、地址（type://host:port）、状态标签、错误信息、操作按钮（编辑/删除/连接/断开）。已连接状态下禁用删除按钮。
34	- **代码位置**: `src/components/connect/ConnectionContentPanel.vue:156-178`
35	- **新系统对应 feature**: connection feature UI
36	- **Oracle 来源**: 组件模板，证据充分
37	- **建议**: **保留**。9 连接上限和卡片布局是具体 UI 行为。
38	
39	### 行为 4: 连接状态实时事件驱动更新
40	
41	- **旧行为**: 连接状态通过事件驱动实时更新。`networkAPI.onConnectionEvent` 监听 `connected`/`disconnected`/`error` 三种事件类型，直接修改对应连接的 `isConnected`、`status`、`error` 属性。
42	- **代码位置**: `src/stores/netWorkStore.ts:222-249`
43	- **新系统对应 feature**: connection feature 状态层
44	- **Oracle 来源**: store 逻辑，证据充分
45	- **建议**: **保留**。事件驱动状态更新是核心行为模式。
46	
47	### 行为 5: 网络连接统计（按连接）
48	
49	- **旧行为**: 每个网络连接维护独立的统计信息：`bytesReceived`、`bytesSent`、`messagesReceived`、`messagesSent`、`lastActivity`、`connectionTime`、`error`。通过 `networkAPI.onStatusChange` 实时更新。
50	- **代码位置**: `src/types/serial/network.ts:53-62` — `NetworkStatus` 接口
51	- **代码位置**: `src/stores/netWorkStore.ts:252-255` — statusChange 监听
52	- **新系统对应 feature**: connection feature 统计
53	- **Oracle 来源**: 类型定义 + store，证据充分
54	- **建议**: **保留**。按连接维度的收发统计是核心可观测行为。
55	
56	---
57	
58	## 二、状态指示灯系统
59	
60	### 行为 6: 用户可配置的状态指示灯
61	
62	- **旧行为**: 用户可创建多个状态指示灯，每个指示灯绑定一个 receive 数据项（通过 groupId + dataItemId），配置值-颜色映射。指示灯以圆点 + 标签形式展示在顶部 HeaderBar 中。支持全局启用/禁用开关。配置通过 `useStorage` 持久化到 localStorage。
63	- **代码位置**: `src/stores/statusIndicators.ts:15-239` — 整个 store
64	- **代码位置**: `src/components/common/StatusIndicators.vue:1-49` — 展示组件
65	- **代码位置**: `src/components/layout/HeaderBar.vue:13-15` — 嵌入 HeaderBar
66	- **类型定义**: `src/types/frames/receive.ts:150-169` — `StatusIndicatorConfig`、`StatusIndicatorSettings`、`ValueColorMapping`
67	- **新系统对应 feature**: receive feature 的指示灯子能力
68	- **Oracle 来源**: store + 组件 + 类型定义，证据充分
69	- **建议**: **保留**。用户可配置的状态指示灯是核心展示能力，绑定 receive 数据项的值变化到视觉反馈。
70	
71	### 行为 7: 指示灯值匹配逻辑（精确值 + 数值范围）
72	
73	- **旧行为**: 指示灯支持两种值匹配方式：(1) 精确值匹配 — 字符串相等比较；(2) 数值范围匹配 — 支持 "min-max" 格式（如 "10-20"），自动解析为范围。匹配成功时使用映射颜色，无匹配时使用默认颜色。数据项不存在或值为 null/undefined 时，指示灯不激活。
74	- **代码位置**: `src/stores/statusIndicators.ts:40-88` — parseValueType / isValueMatch / getIndicatorStatus
75	- **新系统对应 feature**: receive feature 的指示灯匹配逻辑
76	- **Oracle 来源**: store 方法，证据充分
77	- **建议**: **保留**。精确值 + 范围匹配是核心匹配行为。
78	
79	### 行为 8: 指示灯定时刷新（1 秒间隔）
80	
81	- **旧行为**: 指示灯通过 1 秒间隔的 `setInterval` 定时刷新。每次刷新先做快照对比（hasDataChanged），仅在数据变化时才触发计算属性更新。这是性能优化手段，避免每秒都重算。
82	- **代码位置**: `src/stores/statusIndicators.ts:91-128` — hasDataChanged / startAutoUpdate
83	- **新系统对应 feature**: receive feature 的指示灯更新机制
84	- **Oracle 来源**: store 方法，证据充分
85	- **建议**: **保留**。1 秒轮询 + 快照对比是具体行为模式，新系统可以用响应式替代，但"数据变化才更新"的语义应保留。
86	
87	### 行为 9: 指示灯配置对话框
88	
89	- **旧行为**: 提供完整的配置对话框，支持：添加/删除指示灯、选择关联数据项（从所有 receive 数据分组和数据项中选择）、设置默认颜色、配置值-颜色映射（支持 color picker）、如果数据项有 labelOptions 则自动使用下拉选择替代自由输入。保存时清空现有配置后批量写入。
90	- **代码位置**: `src/components/common/StatusIndicatorConfigDialog.vue:1-291`
91	- **新系统对应 feature**: receive feature 的指示灯配置 UI
92	- **Oracle 来源**: 组件代码，证据充分
93	- **建议**: **保留**。完整的配置 CRUD 行为。
94	
95	### 行为 10: 指示灯 Tooltip 显示详情
96	
97	- **旧行为**: 鼠标悬停指示灯时显示 tooltip，格式为 `{label}: 激活 ({value})` 或 `{label}: 未激活 ({value})` 或 `{label}: 数据项不存在`。
98	- **代码位置**: `src/components/common/StatusIndicators.vue:7` — title 绑定
99	- **代码位置**: `src/components/common/StatusIndicators.vue:35-44` — getIndicatorStatusText
100	- **新系统对应 feature**: receive feature 的指示灯展示
101	- **Oracle 来源**: 组件代码，证据充分
102	- **建议**: **保留**。Tooltip 悬停详情是用户交互细节。
103	
104	---
105	
106	## 三、健康检查
107	
108	### 行为 11: SCOE 健康自检指令
109	
110	- **旧行为**: SCOE 系统支持"健康自检"指令，检查三个条件：(1) 已加载卫星ID（`loadedSatelliteId` 非空）；(2) SCOE 帧已加载（`scoeFramesLoaded` 为 true）；(3) 连接目标路径有效（`network:scoe-udp:scoe-udp-remote` 存在）。三者全部满足则状态为 `healthy`，否则为 `error`。结果写入 `scoeStore.status.healthStatus`。
111	- **代码位置**: `src/composables/scoe/commands/healthCheck.ts:1-43` — executeHealthCheck
112	- **状态枚举**: `src/types/scoe/index.ts:75` — `healthStatus: 'unknown' | 'healthy' | 'error'`
113	- **新系统对应 feature**: 指令接入 / SCOE 子系统
114	- **Oracle 来源**: 命令执行器 + 类型定义，证据充分
115	- **建议**: **保留**。健康自检是 SCOE 的核心运维行为。注意当前实现是 TODO 级别，逻辑较简陋。
116	
117	### 行为 12: SCOE 链路自检指令
118	
119	- **旧行为**: SCOE 系统支持"链路自检"指令，遍历所有 receive 数据分组和数据项，检查三个特定标签的数据项：(1) "载波同步锁定"值是否为 1；(2) "定时同步锁定"值是否为 1；(3) "帧同步锁定"值是否为 1。全部为 1 则 `pass`，否则 `fail`。结果写入 `scoeStore.status.linkTestResult`。
120	- **代码位置**: `src/composables/scoe/commands/linkCheck.ts:14-46` — executeLinkCheck
121	- **状态枚举**: `src/types/scoe/index.ts:76` — `linkTestResult: 'unknown' | 'pass' | 'fail'`
122	- **新系统对应 feature**: 指令接入 / SCOE 子系统
123	- **Oracle 来源**: 命令执行器，证据充分
124	- **建议**: **保留，但实现方式需改进**。当前通过硬编码数据项标签名匹配是脆弱的。新系统应使用更可靠的标识机制（如数据项 ID），但"检查载波/定时/帧三个锁定状态"的业务语义必须保留。
125	
126	### 行为 13: SCOE 状态面板展示
127	
128	- **旧行为**: SCOE 有独立的状态面板，展示 10 个状态项：
129	  1. 软件启动累计秒（格式化为 Xh Xm Xs）
130	  2. 当前卫星ID加载累计秒
131	  3. 指令接收总计数（toLocaleString 格式化）
132	  4. 指令执行成功总计数
133	  5. 指令执行出错计数
134	  6. 最近一条指令功能码
135	  7. 指令执行出错原因（ScoeErrorReason 枚举值）
136	  8. 已加载配置的卫星ID
137	  9. 健康状态（healthy=绿色"正常"/unknown=灰色"未自检"/error=红色"异常"）
138	  10. 链路自检结果（pass=绿色"通过"/fail=红色"失败"/unknown=灰色"未自检"）
139	- **代码位置**: `src/components/scoe/StatusPanel.vue:1-185`
140	- **新系统对应 feature**: 指令接入 / SCOE 状态展示
141	- **Oracle 来源**: 组件代码，证据充分
142	- **建议**: **保留**。10 项 SCOE 运维指标是完整的状态面板行为。
143	
144	### 行为 14: SCOE 状态数据结构
145	
146	- **旧行为**: SCOE 状态由 `ScoeStatus` 接口定义，包含：runtimeSeconds、satelliteIdRuntimeSeconds、commandReceiveCount、commandSuccessCount、lastCommandCode、commandErrorCount、lastErrorReason、loadedSatelliteId、healthStatus、linkTestResult、scoeFramesLoaded、receiveCommandSuccess。初始值中 healthStatus 和 linkTestResult 都是 `unknown`。
147	- **代码位置**: `src/types/scoe/index.ts:57-82` — ScoeStatus 接口
148	- **代码位置**: `src/types/scoe/index.ts:161-174` — defaultScoeStatus 默认值
149	- **新系统对应 feature**: 指令接入 / SCOE 状态模型
150	- **Oracle 来源**: 类型定义，证据充分
151	- **建议**: **保留**。ScoeStatus 是 SCOE 子系统的完整状态模型。
152	
153	### 行为 15: SCOE 错误原因枚举
154	
155	- **旧行为**: SCOE 定义了 6 种错误原因枚举：NONE（无错误）、SATELLITE_ID_NOT_FOUND、SATELLITE_CONFIG_INCOMPLETE、SATELLITE_ID_LOADING、COMMAND_CODE_NOT_FOUND、CHECKSUM_ERROR、COMPLETION_CONDITION_TIMEOUT。初始值为 `ScoeErrorReason.NONE`。
156	- **代码位置**: `src/types/scoe/receiveCommand.ts:113-121` — ScoeErrorReason 枚举
157	- **新系统对应 feature**: 指令接入 / SCOE 错误模型
158	- **Oracle 来源**: 类型定义，证据充分
159	- **建议**: **保留**。SCOE 错误原因枚举是运维可观测行为。
160	
161	---
162	
163	## 四、全局统计系统
164	
165	### 行为 16: 全局统计分类和字段
166	
167	- **旧行为**: 全局统计分四类：
168	  - **系统统计**：year/month/day/hour/minute/second/millisecond/allSeconds/startTime/uptime/latitude/longitude。其中 uptime 从 startTime 起每秒递增。
169	  - **通信统计**：sentPackets、receivedPackets、sentBytes、receivedBytes（均为累计计数器）。
170	  - **帧匹配统计**：matchedFrames、unmatchedFrames（均为累计计数器）。
171	  - **错误统计**：communicationErrors、frameParseErrors（均为累计计数器）。
172	- **代码位置**: `src/stores/globalStatsStore.ts:17-50` — 四类 ref 定义
173	- **新系统对应 feature**: 可能为 runtime 层面或独立 stats feature
174	- **Oracle 来源**: store 定义，证据充分
175	- **建议**: **保留**。四类统计是新系统运行时的基础可观测能力。
176	
177	### 行为 17: 统计值暴露给表达式系统
178	
179	- **旧行为**: 全局统计通过 `availableStats` 计算属性暴露，聚合所有四类统计并计算派生值（totalPackets、totalBytes、totalErrors），由 `getStatValue(statKey)` 方法供表达式引擎按 key 取值。
180	- **代码位置**: `src/stores/globalStatsStore.ts:55-85` — availableStats computed
181	- **代码位置**: `src/stores/globalStatsStore.ts:171-173` — getStatValue
182	- **新系统对应 feature**: shared/ 表达式引擎的统计变量源
183	- **Oracle 来源**: store 方法，证据充分
184	- **建议**: **保留**。统计值作为表达式变量源是跨 feature 的关键能力。
185	
186	### 行为 18: 系统统计每秒更新（含位置信息）
187	
188	- **旧行为**: 系统统计通过 `timerManager.registerTimer` 以 1000ms 间隔定时更新。每次更新计算 uptime、年月日时分秒毫秒。初始化时还获取一次 GPS 位置信息（经纬度精确到分）。
189	- **代码位置**: `src/stores/globalStatsStore.ts:88-133` — initialize / updateSystemStats / updateLocationInfo
190	- **新系统对应 feature**: runtime 层面的定时更新
191	- **Oracle 来源**: store 方法，证据充分
192	- **建议**: **保留**。时间统计是基础能力；GPS 位置信息是否保留取决于新系统是否有定位需求。
193	
194	### 行为 19: 统计重置
195	
196	- **旧行为**: 全局统计提供 `resetStats()` 方法，将四类统计全部归零。系统统计部分（时间/位置）也归零，startTime 归零。调用后打印 console.log。
197	- **代码位置**: `src/stores/globalStatsStore.ts:176-210` — resetStats
198	- **新系统对应 feature**: stats feature 重置能力
199	- **Oracle 来源**: store 方法，证据充分
200	- **建议**: **保留**。统计重置是运维操作。
201	
202	### 行为 20: 通信统计由外部 store 递增
203	
204	- **旧行为**: 通信统计（sentPackets/receivedPackets/sentBytes/receivedBytes）不自动采集，而是暴露 `incrementSentPackets`、`addSentBytes` 等方法由外部调用方在数据收发时手动递增。
205	- **代码位置**: `src/stores/globalStatsStore.ts:136-168` — 六个 increment/add 方法
206	- **新系统对应 feature**: connection / send / receive feature 在数据路径中调用
207	- **Oracle 来源**: store 方法，证据充分
208	- **建议**: **保留，但改为自动采集**。新系统的统计应在数据路径中自动采集，而非依赖外部手动调用。
209	
210	---
211	
212	## 五、Receive 帧级统计
213	
214	### 行为 21: 帧级统计信息
215	
216	- **旧行为**: 每个 receive 帧维护独立统计：`frameId`、`totalReceived`（总接收数）、`lastReceiveTime`（上次接收时间）、`checksumFailures`（校验失败数）、`errorCount`（错误数）、`lastReceivedFrame`（最后接收帧原始数据）。通过 `Map<string, ReceiveFrameStats>` 存储。
217	- **代码位置**: `src/types/frames/receive.ts:49-56` — ReceiveFrameStats 接口
218	- **代码位置**: `src/stores/frames/receiveFramesStore.ts:95` — frameStats ref
219	- **新系统对应 feature**: receive feature 统计
220	- **Oracle 来源**: 类型 + store，证据充分
221	- **建议**: **保留**。帧级统计是 receive 的核心可观测行为。
222	
223	### 行为 22: 帧统计面板展示
224	
225	- **旧行为**: receive 页面有独立的统计面板，展示：
226	  - **总体统计**：接收总数（智能格式化 K/M）、错误总数、校验失败数、活跃帧数、错误率（百分比，>5% 显示红色，否则绿色）
227	  - **当前帧统计**：选中帧的接收次数、错误次数、最后接收时间（相对时间：X 秒前/X 分钟前/X 小时前/X 天前）
228	  - **记录状态**：是否正在记录数据、运行时间、记录数、开始/停止记录按钮
229	- **代码位置**: `src/components/frames/receive/FrameStatsPanel.vue:1-227`
230	- **新系统对应 feature**: receive feature 的统计展示 UI
231	- **Oracle 来源**: 组件代码，证据充分
232	- **建议**: **保留**。帧统计面板是 receive 的核心展示能力。
233	
234	### 行为 23: 帧统计重置（全局 + 单帧）
235	
236	- **旧行为**: 支持两种重置：
237	  - **全局重置**：清空所有 frameStats，同时将所有数据项的 value 归 null、displayValue 归空字符串。操作前有 confirm 弹窗。
238	  - **单帧重置**：仅删除选中帧的统计数据。操作前有 confirm 弹窗。
239	- **代码位置**: `src/components/frames/receive/FrameStatsPanel.vue:66-84` — resetStats / resetSelectedFrameStats
240	- **新系统对应 feature**: receive feature 的统计管理
241	- **Oracle 来源**: 组件方法，证据充分
242	- **建议**: **保留**。两种粒度的重置是具体用户操作行为。
243	
244	---
245	
246	## 六、发送任务状态监视
247	
248	### 行为 24: 活动任务监视器
249	
250	- **旧行为**: 有独立的活动任务监视器对话框，展示所有正在执行的发送任务。每个任务显示：任务名称、类型标签（顺序/定时/触发）、状态 badge（7 种状态：idle/running/paused/completed/error/waiting-trigger/waiting-schedule）、进度条和进度百分比、下次执行倒计时（定时任务）、运行时长、错误信息。支持按类型和状态筛选。
251	- **代码位置**: `src/components/frames/FrameSend/ActiveTasksMonitor.vue:1-418`
252	- **新系统对应 feature**: task feature 的任务监控 UI
253	- **Oracle 来源**: 组件代码，证据充分
254	- **建议**: **保留**。任务监视器是发送任务管理的核心 UI。
255	
256	### 行为 25: 任务状态颜色映射
257	
258	- **旧行为**: 7 种任务状态有固定颜色映射：idle=blue-grey, running=blue, paused=orange, completed=positive, error=negative, waiting-trigger=purple, waiting-schedule=indigo。每种状态有对应的中文标签和操作按钮。
259	- **代码位置**: `src/components/frames/FrameSend/ActiveTasksMonitor.vue:54-73` — taskStatusLabels / taskStatusColors
260	- **新系统对应 feature**: task feature 的状态展示
261	- **Oracle 来源**: 组件代码，证据充分
262	- **建议**: **保留**。状态颜色映射是 UI 视觉一致性的一部分。
263	
264	---
265	
266	## 七、网络测试工具
267	
268	### 行为 26: 网络测试工具中的快速发送预设
269	
270	- **旧行为**: 网络测试工具内置 5 个快速发送预设：心跳包（FF FF 00 01）、查询状态（FF FF 00 02）、复位命令（FF FF 00 03）、Hello、Test。前三个是 hex 格式，后两个是 text 格式。
271	- **代码位置**: `src/components/connect/NetworkTestTools.vue:179-184` — quickSendPresets
272	- **新系统对应 feature**: connection feature 的测试工具
273	- **Oracle 来源**: 组件代码，证据充分
274	- **建议**: **排除**。硬编码的预设值是旧系统特定协议实现，新系统不应硬编码。
275	
276	### 行为 27: 网络测试工具的收发数据展示
277	
278	- **旧行为**: 测试工具展示收发数据日志，发送数据蓝色（->前缀）、接收数据绿色（<-前缀）、错误红色（warning前缀）。支持 hex/text 格式切换、自动滚动、保存到文件、清空。接收区最大 1000 行。
279	- **代码位置**: `src/components/connect/NetworkTestTools.vue:124-161` — addReceivedData / clearReceiveArea / saveReceiveData
280	- **新系统对应 feature**: connection feature 的测试工具
281	- **Oracle 来源**: 组件代码，证据充分
282	- **建议**: **保留**。数据收发日志的彩色展示和格式切换是通用测试能力。
283	
284	---
285	
286	## 八、汇总
287	
288	### 按类别统计
289	
290	| 类别 | 行为数 | 保留 | 排除 |
291	|------|--------|------|------|
292	| 连接状态指示 | 5 | 5 | 0 |
293	| 状态指示灯系统 | 5 | 5 | 0 |
294	| 健康检查 | 5 | 5 | 0 |
295	| 全局统计系统 | 5 | 5 | 0 |
296	| Receive 帧级统计 | 3 | 3 | 0 |
297	| 发送任务状态监视 | 2 | 2 | 0 |
298	| 网络测试工具 | 2 | 1 | 1 |
299	| **合计** | **27** | **26** | **1** |
300	
301	### 排除项
302	
303	| 编号 | 行为 | 排除原因 |
304	|------|------|----------|
305	| 行为 26 | 快速发送预设（心跳包/查询状态/复位命令） | 硬编码旧协议特定字节序列，新系统不应硬编码 |
306	
307	### 保留但需改进的实现方式
308	
309	| 编号 | 行为 | 改进原因 |
310	|------|------|----------|
311	| 行为 8 | 指示灯 1 秒轮询刷新 | 新系统应改用响应式数据流，不再需要定时轮询 |
312	| 行为 12 | 链路自检通过数据项标签名匹配 | 新系统应使用数据项 ID 替代标签名匹配 |
313	| 行为 18 | GPS 位置信息 | 需确认新系统是否有定位需求 |
314	| 行为 20 | 通信统计手动递增 | 新系统应在数据路径中自动采集 |
315	
316	### 新系统 feature 归口映射
317	
318	| 旧行为类别 | 新系统 feature |
319	|------------|---------------|
320	| 连接状态指示（行为 1-5） | connection feature |
321	| 状态指示灯（行为 6-10） | receive feature 的指示灯子能力 |
322	| SCOE 健康检查（行为 11-15） | 指令接入 feature |
323	| 全局统计（行为 16-20） | runtime 层面或独立 stats 能力 |
324	| 帧级统计（行为 21-23） | receive feature |
325	| 任务监视（行为 24-25） | task feature |
326	| 测试工具（行为 27） | connection feature |
327	
328	## 记录
329	
330	无额外记录。
331	
332	## 后续
333	
334	无。
335	
```

> TOOL

tool_result
id: call_f85b4c99592b45b5928f5c09
```
1	# [S004-agent9] 旧系统页面入口与路由完整清单
2	
3	> 2026-05-19 | 事实提取 | 状态：完成
4	
5	## 目标
6	
7	提取旧系统所有页面入口、路由定义、导航结构，并与新系统逐项对照，形成完整的新旧映射表。
8	
9	## 记录
10	
11	### 1. 旧系统路由完整列表
12	
13	路由定义文件：`src/router/routes.ts`
14	
15	旧系统只有一层嵌套路由结构：所有业务页面都是 `/` 根路由（使用 `MainLayout.vue` 布局）的 children。
16	
17	| # | path | component | 侧边栏名称 | 功能描述 |
18	|---|------|-----------|------------|---------|
19	| 1 | `/` (空字符串，即 `/`) | `pages/home/HomePage.vue` | 首页 | 应用首页，仅显示标题"激光链路标准测试设备" |
20	| 2 | `/connect` | `pages/ConnectConfigPage.vue` | 连接 | 连接配置管理。左右分栏：左侧连接列表，右侧三个 tab（网口配置/串口配置/测试工具） |
21	| 3 | `/frames/list` | `pages/frames/FrameList.vue` | 配置 | 帧列表（帧配置管理）。左右分栏：左侧帧表格+过滤，右侧帧详情面板。支持新建/编辑/复制/删除/收藏/导入/导出 |
22	| 4 | `/frames/editor` | `pages/frames/FrameEditor.vue` | （从帧列表导航进入，无侧边栏入口） | 帧编辑器。创建/编辑帧定义。左侧基本信息，中间字段列表+字段预览，弹窗式字段编辑器 |
23	| 5 | `/frames/send` | `pages/FrameSendPage.vue` | 发送 | 帧发送页面。帧格式列表、帧实例列表、实例编辑器、帧预览、目标选择器、定时发送/触发发送/顺序发送弹窗、活动任务监控 |
24	| 6 | `/frames/receive` | `pages/ReceiveFramePage.vue` | 接收 | 接收帧页面。两种模式——编辑模式（三栏：接收帧选择器/数据项列表/统计面板），显示模式（双栏：数据组管理/数据展示容器） |
25	| 7 | `/settings` | `pages/settings/Index.vue` | 设置 | 系统设置。数据记录设置（自动开始记录/保存间隔）、其他应用选项 |
26	| 8 | `/storage` | `pages/storage/HighSpeedStoragePage.vue` | 存储 | 高速存储管理。配置和管理业务数据的高速存储功能（几百 Mbps 网络数据存储） |
27	| 9 | `/history` | `pages/HistoryAnalysisPage.vue` | 历史 | 历史分析。时间选择器+数据选择器+多图表展示，支持 CSV 导出和图表设置 |
28	| 10 | `/scoe` | `pages/SCOEConfigPage.vue` | SCOE | SCOE 配置。三栏：左侧卫星配置列表、中间配置表单、右侧状态面板 |
29	| 11 | `/:catchAll(.*)*` | `pages/ErrorNotFound.vue` | （无） | 404 页面 |
30	
31	**路由特点：**
32	- 无动态路由参数（`/frames/editor` 通过 query string `?id=xxx` 或 `?new=true` 传递参数）
33	- 无 name 属性定义
34	- 无 meta 属性
35	- 无路由守卫
36	- 无多级嵌套（除根布局外）
37	- 使用 `createWebHashHistory`（hash 模式路由）
38	
39	### 2. 旧系统导航结构
40	
41	#### 2.1 侧边栏（SidePanel.vue）
42	
43	侧边栏定义 9 个导航项，硬编码在 `src/components/layout/SidePanel.vue`：
44	
45	```typescript
46	const navItems = ref([
47	  { label: '首页',    path: '/',            icon: 'home' },
48	  { label: '连接',    path: '/connect',     icon: 'insights' },
49	  { label: 'SCOE',    path: '/scoe',        icon: 'satellite' },
50	  { label: '配置',    path: '/frames/list', icon: 'view_list' },
51	  { label: '发送',    path: '/frames/send', icon: 'send' },
52	  { label: '接收',    path: '/frames/receive', icon: 'download' },
53	  { label: '存储',    path: '/storage',     icon: 'storage' },
54	  { label: '历史',    path: '/history',     icon: 'history' },
55	  { label: '设置',    path: '/settings',    icon: 'settings' },
56	]);
57	```
58	
59	**导航方式：** 点击侧边栏项 → `router.push(path)` → 全页面切换。
60	
61	**侧边栏 UI 行为：**
62	- 默认 mini 模式（宽度 60px，只显示图标）
63	- 鼠标悬停展开（宽度 120px，显示图标+文字）
64	- 使用 `mini-to-overlay` 模式
65	- 深色主题（`bg-[#1a202c]`）
66	
67	#### 2.2 顶部栏（HeaderBar.vue）
68	
69	- 左侧：Logo + 应用名称"激光链路标准测试设备"
70	- 中间：状态指示灯（`StatusIndicators` 组件）
71	- 右侧：窗口控制按钮（最小化/最大化/关闭）
72	- 整行可拖拽移动窗口（`-webkit-app-region: drag`）
73	
74	#### 2.3 页面间导航（非侧边栏）
75	
76	| 来源页面 | 目标页面 | 导航方式 |
77	|---------|---------|---------|
78	| 帧列表 `/frames/list` | 帧编辑器 `/frames/editor?new=true` | 点击"新建帧"按钮 → `router.push` |
79	| 帧列表 `/frames/list` | 帧编辑器 `/frames/editor?id=xxx` | 帧操作菜单"编辑" → `router.push` |
80	| 帧发送 `/frames/send` | 弹窗：定时发送/触发发送/顺序发送/任务监控 | Dialog 弹窗，非路由 |
81	
82	#### 2.4 页面内 Tab 切换
83	
84	| 页面 | Tab 结构 |
85	|------|---------|
86	| 连接 `/connect` | 右侧面板三个 tab：网口配置 / 串口配置 / 测试工具 |
87	| 接收 `/frames/receive` | 两种模式切换：编辑模式 / 显示模式 |
88	| 帧发送 `/frames/send` | 通过弹窗访问：定时发送 / 触发发送 / 顺序发送 / 任务监控 |
89	
90	#### 2.5 全局弹窗
91	
92	- **FileListDialog**：全局文件对话框，挂载在 `MainLayout.vue` 中，通过 EventBus 打开（`FILE_DIALOG_OPEN` 事件），用于导入/导出文件操作。
93	
94	### 3. 旧系统布局结构
95	
96	#### 3.1 主布局（MainLayout.vue）
97	
98	```
99	q-layout (view="hHh lpR fFf")
100	├── q-header (固定高度 48px)
101	│   └── HeaderBar
102	├── div.flex (内容区域，高度 calc(100vh - 28px))
103	│   ├── q-drawer (侧边栏，mini 模式，固定 60px/展开 120px)
104	│   │   └── SidePanel
105	│   └── q-page-container (flex-grow)
106	│       └── router-view
107	└── FileListDialog (全局文件对话框，条件渲染)
108	```
109	
110	**布局特点：**
111	- 全局深色主题（`bg-[#0f172a]`）
112	- 侧边栏 mini-to-overlay 模式
113	- 无全屏模式
114	- 无独立的空白/登录页
115	- 布局 composable 分为三个：`useLayoutDrawer`（侧边栏状态）、`useFileDialog`（全局文件对话框）、`useAppLifecycle`（应用生命周期初始化）
116	
117	#### 3.2 页面内部布局模式
118	
119	| 页面 | 布局模式 |
120	|------|---------|
121	| 首页 | 居中标题 |
122	| 连接 | 左右分栏（24vw + 1fr），右侧含 tab |
123	| 帧列表 | 左右分栏（帧表格 + 30vw 详情面板） |
124	| 帧编辑器 | 三栏（300px 左侧 + 主区域），主区域内字段列表+预览 |
125	| 帧发送 | 多组件组合（帧格式列表 + 实例列表 + 编辑器 + 预览 + 目标选择） |
126	| 接收 | 编辑模式三栏（240px + 1fr + 300px）/ 显示模式双栏 |
127	| 设置 | 单栏表单 |
128	| 存储 | 单栏，居中 max-w-4xl |
129	| 历史 | 左右可调分栏（320px + 1fr） |
130	| SCOE | 三栏（w-64 + flex-1 + w-56） |
131	
132	### 4. 新旧路由映射表
133	
134	| 旧路由 | 旧侧边栏名 | 新路由 | 新侧边栏名 | 映射关系 |
135	|-------|-----------|-------|-----------|---------|
136	| `/` | 首页 | `/` | 总览 | 直接对应。旧系统首页仅标题，新系统改为仪表盘（连接/帧/任务/发送统计+快速入口） |
137	| `/connect` | 连接 | `/connection` | 连接管理 | 直接对应。新系统包含串口/网络连接管理，不再含测试工具 tab |
138	| `/frames/list` | 配置 | `/frames` | 帧定义 | 直接对应。帧列表+帧详情 |
139	| `/frames/editor` | （从列表导航） | `/frames/editor/:frameId?` | （从列表导航） | 直接对应。旧用 query `?id=xxx`，新用路由参数 `:frameId?` |
140	| `/frames/send` | 发送 | `/send` | 帧发送 | 直接对应 |
141	| `/frames/receive` | 接收 | `/display` | 实时展示 | 对应关系变化。旧"接收"页面含帧配置+数据展示，新系统拆分为 receive service（后台）+ display 页面（展示） |
142	| `/scoe` | SCOE | `/command-ingress` | 指令接入 | 概念合并升级。旧 SCOE 配置页 → 新"指令接入"页（含 SCOE 配置+监控+测试工具+中心对接，范围更大） |
143	| `/storage` | 存储 | 无 | 无 | **新系统缺失** |
144	| `/history` | 历史 | 无 | 无 | **新系统缺失** |
145	| `/settings` | 设置 | 无 | 无 | **新系统缺失** |
146	| 无 | 无 | `/tasks` | 任务管理 | **新系统新增**。旧系统的定时发送/触发发送/顺序发送散在发送页弹窗中，新系统独立为任务管理页 |
147	| `/:catchAll(.*)*` | 无 | 无 | 无 | 新系统未定义 catch-all/404 路由 |
148	
149	### 5. 新系统路由详情
150	
151	路由定义文件：`rewrite/src/router/routes.ts`
152	
153	| # | path | component | 侧边栏名称 | 功能描述 |
154	|---|------|-----------|------------|---------|
155	| 1 | `/` (空字符串) | `pages/HomePage.vue` | 总览 | 仪表盘首页。连接/帧/任务/发送统计卡片、快速入口、连接状态列表、系统快照 |
156	| 2 | `/connection` | `pages/ConnectionPage.vue` | 连接管理 | 连接管理。卡片式连接列表+新建连接弹窗（串口/网络） |
157	| 3 | `/frames` | `pages/FrameListPage.vue` | 帧定义 | 帧列表+帧详情面板+导入弹窗。支持方向过滤、收藏、搜索、克隆、删除 |
158	| 4 | `/frames/editor/:frameId?` | `pages/FrameEditorPage.vue` | （从列表导航） | 帧编辑器。基本信息+标识规则+字段列表+字段编辑弹窗。支持动态路由参数 |
159	| 5 | `/send` | `pages/SendPage.vue` | 帧发送 | 帧发送。左栏帧列表+中栏实例表格/编辑+目标选择器+帧预览 |
160	| 6 | `/display` | `pages/DisplayPage.vue` | 实时展示 | 实时数据展示。接收生命周期状态、计数器、字段值表、最近输入表、帧统计表、散点图、波形图 |
161	| 7 | `/tasks` | `pages/TaskManagePage.vue` | 任务管理 | 任务管理。活动任务+历史任务 tab、任务编辑器（步骤：发送/延时/等待条件）、任务执行详情 |
162	| 8 | `/command-ingress` | `pages/CommandIngressPage.vue` | 指令接入 | 指令接入。多 tab：监控/配置/测试工具/中心对接。包含 SCOE 配置、命令日志、卫星配置表、心跳/链路测试/对接任务 |
163	
164	**新系统路由特点：**
165	- 使用动态路由参数（`:frameId?`）
166	- 无 catch-all 路由
167	- 无 meta/name 属性
168	- 无路由守卫
169	- 侧边栏默认收起（`drawerOpen = false`），非 mini-to-overlay 模式
170	
171	### 6. 新系统导航结构
172	
173	导航项定义在 `rewrite/src/app/AppShell.vue`：
174	
175	```typescript
176	const navigationItems = [
177	  { label: '总览',     to: '/',               icon: 'dashboard' },
178	  { label: '连接管理', to: '/connection',     icon: 'link' },
179	  { label: '帧定义',   to: '/frames',         icon: 'view_agenda' },
180	  { label: '帧发送',   to: '/send',           icon: 'send' },
181	  { label: '实时展示', to: '/display',        icon: 'monitor_heart' },
182	  { label: '任务管理', to: '/tasks',          icon: 'assignment' },
183	  { label: '指令接入', to: '/command-ingress', icon: 'settings_input_antenna' },
184	];
185	```
186	
187	**导航方式：** 点击侧边栏项 → `router.push(to)` → 全页面切换。侧边栏使用独立 `AppNavigation` widget 组件。
188	
189	**新系统侧边栏 UI 行为：**
190	- 默认收起（`drawerOpen = false`）
191	- 有 `show-if-above` 属性（小屏幕自动收起）
192	- 手动点击 hamburger 按钮切换
193	- 宽度由 CSS token `--rw-size-app-drawer` 控制
194	
195	### 7. 缺失项列表
196	
197	#### 7.1 旧功能在新系统中缺失
198	
199	| 旧页面 | 功能 | 状态 | 备注 |
200	|-------|------|------|------|
201	| `/storage` | 高速存储管理 | 缺失 | 支持几百 Mbps 网络数据存储的配置和管理 |
202	| `/history` | 历史数据分析 | 缺失 | 时间选择器+数据选择器+多图表展示+CSV 导出 |
203	| `/settings` | 系统设置 | 缺失 | 自动开始记录、保存间隔等应用配置 |
204	| 连接页测试工具 tab | 网口/串口测试工具 | 可能已合并 | 旧连接页右侧有"测试"tab，新连接页未见，可能移到 command-ingress 页测试工具 tab |
205	| 接收帧配置 | 接收帧选择+数据项配置 | 架构变化 | 旧接收页含配置+展示，新系统拆为 receive service（后台）+ display 页（纯展示），配置方式待确认 |
206	| 帧编辑器字段预览 | 实时字段预览区域 | 缺失或变化 | 旧编辑器有 FrameFieldPreview 组件，新编辑器未见 |
207	
208	#### 7.2 新系统新增能力
209	
210	| 新页面 | 功能 | 对应旧系统 |
211	|-------|------|-----------|
212	| `/tasks` | 独立任务管理页（创建/编辑/执行/监控任务） | 旧系统定时/触发/顺序发送散在发送页弹窗中，无独立任务页 |
213	| `/command-ingress` | 指令接入统一页（SCOE+监控+测试+中心对接） | 旧系统仅有 `/scoe` 配置页，监控/测试/对接分散 |
214	
215	#### 7.3 404 页面
216	
217	旧系统有 `ErrorNotFound.vue` catch-all 路由。新系统未定义。
218	
219	### 8. 保留/排除建议
220	
221	#### 保留（新系统已有对应）
222	
223	| 旧页面 | 建议 | 理由 |
224	|-------|------|------|
225	| 首页 | 保留升级 | 新首页已升级为仪表盘，功能远超旧首页 |
226	| 连接配置 | 保留 | 新连接页覆盖旧功能 |
227	| 帧列表 | 保留 | 新帧定义页覆盖旧功能 |
228	| 帧编辑器 | 保留 | 新编辑器覆盖旧功能，路由参数方式改进 |
229	| 帧发送 | 保留 | 新发送页覆盖旧功能 |
230	| SCOE 配置 | 合并保留 | 合并到指令接入页，范围更大 |
231	
232	#### 排除（旧代码组织不保留）
233	
234	| 旧页面 | 建议 | 理由 |
235	|-------|------|------|
236	| 接收帧页面（整体） | 拆分保留 | 按重写总原则，配置逻辑和展示逻辑拆分为独立 feature，不保留旧的单页面耦合方式 |
237	| 旧路由 hash 模式 | 排除 | 新系统可自行选择路由模式 |
238	
239	#### 待补充（新系统缺失，需要新增）
240	
241	| 页面 | 优先级 | 理由 |
242	|------|--------|------|
243	| 存储管理页 | 高 | 高速存储是核心业务功能 |
244	| 历史分析页 | 高 | 历史数据分析是核心业务功能 |
245	| 系统设置页 | 中 | 应用配置入口 |
246	| 404 页面 | 低 | 基础体验完善 |
247	
248	## 后续
249	
250	无。
251	
```

> TOOL

tool_result
id: call_3e47b3c7049d473393df26b9
```
1	# [S004-agent8] 旧系统设置与配置管理行为调研
2	
3	> 2026-05-19 | 调研 | 完成
4	
5	## 目标
6	
7	调研旧系统的设置和配置管理行为，提取所有必须保留的可观测业务行为。只做事实提取，不做设计或实施。
8	
9	## 记录
10	
11	### 一、旧系统配置项完整清单
12	
13	旧系统的配置分散在多个 store 和组件中，使用 `@vueuse/core` 的 `useStorage` 绑定 localStorage 做持久化，或通过 `dataStorageAPI` 持久化到文件。没有统一的设置页面或集中式配置管理。
14	
15	#### 1.1 应用级配置（settingsStore）
16	
17	**文件**: `src/stores/settingsStore.ts`
18	
19	| 配置项 | 类型 | 默认值 | 存储键 | 说明 |
20	|--------|------|--------|--------|------|
21	| autoStartRecording | boolean | true | `settings.autoStartRecording` | 自动开始记录 |
22	| csvDefaultOutputPath | string | '' | `settings.csvDefaultOutputPath` | CSV 导出默认路径 |
23	| csvSaveInterval | number | 5（分钟） | `settings.csvSaveInterval` | CSV 保存间隔 |
24	
25	- 持久化方式：`useStorage` -> localStorage，实时写入
26	- 无主题、语言、窗口布局等应用外观配置
27	- 无配置重置/恢复功能
28	
29	#### 1.2 串口配置（serialStore）
30	
31	**文件**: `src/stores/serialStore.ts`
32	
33	| 配置项 | 类型 | 默认值 | 存储键 | 说明 |
34	|--------|------|--------|--------|------|
35	| lastUsedPort | string | '' | `last-used-port` | 上次使用的串口路径（用于默认选择） |
36	| portSerialOptions | Record<string, SerialPortOptions> | {} | `serial-options-map` | 每个串口独立的配置映射 |
37	| defaultSerialOptions | SerialPortOptions | {baudRate:9600, dataBits:8, stopBits:1, parity:'none', flowControl:'none', autoOpen:false} | `default-serial-options` | 全局默认串口配置 |
38	
39	`SerialPortOptions` 完整字段：
40	- `baudRate`: 波特率（可选值：110~1000000）
41	- `dataBits`: 数据位（5/6/7/8）
42	- `stopBits`: 停止位（1/1.5/2）
43	- `parity`: 校验位（none/even/odd/mark/space）
44	- `flowControl`: 流控制（none/hardware/software）
45	- `bufferSize`: 缓冲区大小
46	- `autoOpen`: 是否自动打开
47	- `timeout`: 超时设置(ms)
48	
49	- 持久化方式：`useStorage` -> localStorage，实时写入
50	- 每个串口路径有独立配置，连接时读取 `portSerialOptions[portPath]` 或 fallback 到 `defaultSerialOptions`
51	- 无配置重置功能
52	
53	#### 1.3 帧过滤器配置（frameFilterStore）
54	
55	**文件**: `src/stores/frames/frameFilterStore.ts`
56	
57	| 配置项 | 类型 | 默认值 | 说明 |
58	|--------|------|--------|------|
59	| searchQuery | string | '' | 搜索关键词 |
60	| filters | FilterOptions | {protocol:'', frameType:'', direction:'', dateRange:undefined} | 过滤条件 |
61	| sortOrder | string | 'id' | 排序方式（id/name/date/usage） |
62	| showFilterPanel | boolean | false | 过滤面板是否显示 |
63	
64	- **不持久化**：使用普通 `ref`，刷新后丢失
65	- `resetFilters()` 方法可重置为默认值
66	- FilterOptions 定义在 `src/config/frameDefaults.ts`
67	
68	#### 1.4 数据显示配置（dataDisplayStore）
69	
70	**文件**: `src/stores/frames/dataDisplayStore.ts`
71	
72	| 配置项 | 类型 | 默认值 | 存储键 | 说明 |
73	|--------|------|--------|--------|------|
74	| table1Config | TableConfig | {selectedGroupId:null, displayMode:'table', chartSelectedItems:[]} | `table1Config` | 表格1配置 |
75	| table2Config | TableConfig | {selectedGroupId:null, displayMode:'table', chartSelectedItems:[]} | `table2Config` | 表格2配置 |
76	| table1ScatterConfig | ConstellationConfig | {bitWidth:12, sampleCount:16, pointSize:3, refreshInterval:1000, iDataSource:{frameId:'',fieldId:''}, qDataSource:{frameId:'',fieldId:''}} | `table1ScatterConfig` | 星座图1配置 |
77	| table2ScatterConfig | ConstellationConfig | 同上 | `table2ScatterConfig` | 星座图2配置 |
78	| displaySettings | DisplaySettings | {updateInterval:1000, csvSaveInterval:5*60*1000, maxHistoryHours:24, enableAutoSave:true, enableRecording:false, enableHistoryStorage:true} | 不持久化 | 显示设置（运行时状态） |
79	
80	`TableConfig` 字段：
81	- `selectedGroupId`: 选中分组ID
82	- `displayMode`: 'table' | 'special' | 'chart'
83	- `chartSelectedItems`: 图表选中数据项ID数组
84	- `yAxisConfig`: Y轴配置（可选）
85	
86	`ConstellationConfig` 字段：
87	- `bitWidth`: 位宽（默认12）
88	- `sampleCount`: 采样数（默认16）
89	- `pointSize`: 点大小（默认3）
90	- `refreshInterval`: 刷新间隔ms（默认1000）
91	- `iDataSource`/`qDataSource`: I/Q路数据源 {frameId, fieldId}
92	
93	`DisplaySettings` 字段：
94	- `updateInterval`: 数据更新间隔ms（默认1000）
95	- `csvSaveInterval`: CSV保存间隔ms（从 settingsStore.csvSaveInterval 派生）
96	- `maxHistoryHours`: 最大历史记录小时数（默认24）
97	- `enableAutoSave`: 自动保存（默认true）
98	- `enableRecording`: 是否正在记录（默认false，运行时状态）
99	- `enableHistoryStorage`: 历史数据存储（默认true）
100	
101	- 持久化方式：tableConfig 和 scatterConfig 通过 `useStorage` -> localStorage 持久化
102	- displaySettings 不持久化，为运行时状态
103	
104	#### 1.5 历史分析图表配置（historyAnalysisStore）
105	
106	**文件**: `src/stores/historyAnalysis.ts`
107	
108	| 配置项 | 类型 | 默认值 | 存储键 | 说明 |
109	|--------|------|--------|--------|------|
110	| multiChartSettings | MultiChartSettings | {chartCount:1, charts:[{id:1,title:'图表1',selectedDataItems:[]}]} | `historyAnalysis_chartSettings` | 多图表布局配置 |
111	
112	- 持久化方式：`useStorage` -> localStorage
113	- 图表数量范围 1~4，标题和数据项选择跨会话保留
114	
115	#### 1.6 状态指示灯配置（statusIndicatorStore）
116	
117	**文件**: `src/stores/statusIndicators.ts`
118	
119	| 配置项 | 类型 | 默认值 | 存储键 | 说明 |
120	|--------|------|--------|--------|------|
121	| settings | StatusIndicatorSettings | {indicators:[], isEnabled:true} | `statusIndicatorSettings` | 状态指示灯配置 |
122	
123	`StatusIndicatorSettings` 字段：
124	- `isEnabled`: 总开关
125	- `indicators`: StatusIndicatorConfig 数组
126	  - `id`: 唯一ID
127	  - `label`: 标签
128	  - `groupId`: 关联分组ID
129	  - `dataItemId`: 关联数据项ID
130	  - `valueMappings`: ValueColorMapping[]（值到颜色映射）
131	  - `defaultColor`: 默认颜色（'#6b7280'）
132	
133	- 持久化方式：`useStorage` -> localStorage
134	- 用户可自定义任意数量的指示灯，每个指示灯可配置值-颜色映射
135	
136	#### 1.7 高速存储配置（highSpeedStorageStore）
137	
138	**文件**: `src/stores/highSpeedStorageStore.ts`
139	
140	| 配置项 | 类型 | 默认值 | 存储键 | 说明 |
141	|--------|------|--------|--------|------|
142	| config | StorageConfig | {enabled:false, rule:null, maxFileSize:100, enableRotation:true, rotationCount:5} | `highSpeedStorageConfig` | 高速存储配置 |
143	
144	`StorageConfig` 字段：
145	- `enabled`: 是否启用
146	- `rule`: FrameHeaderRule | null（帧头识别规则）
147	  - `connectionId`: 关联连接ID
148	  - `headerPatterns`: 帧头十六进制字符串数组
149	  - `enabled`: 规则是否启用
150	- `maxFileSize`: 最大文件大小MB（默认100）
151	- `enableRotation`: 文件轮转（默认true）
152	- `rotationCount`: 轮转文件数量（默认5）
153	
154	- 持久化方式：`useStorage` -> localStorage + 同步到 main 进程
155	- 初始化时双向同步：优先使用 main 进程配置，否则将本地配置同步到 main
156	
157	#### 1.8 SCOE 配置（scoeStore）
158	
159	**文件**: `src/stores/scoeStore.ts`, `src/types/scoe/index.ts`
160	
161	| 配置项 | 类型 | 持久化 | 说明 |
162	|--------|------|--------|------|
163	| globalConfig | ScoeGlobalConfig | 文件（dataStorageAPI） | SCOE 全局配置 |
164	| satelliteConfigs | ScoeSatelliteConfig[] | 文件（dataStorageAPI） | 卫星配置列表 |
165	
166	`ScoeGlobalConfig` 字段：
167	- `scoeIdentifier`: SCOE 标识
168	- `tcpServerIp`: TCP Server IP（默认'0.0.0.0'）
169	- `tcpServerPort`: TCP Server 端口（默认8080）
170	- `tcpServerAutoConnect`: 自动连接（默认false）
171	- `udpIpAddress`: UDP IP
172	- `udpPort`: UDP 端口
173	- 字节偏移量：messageIdentifierOffset, sourceIdentifierOffset, destinationIdentifierOffset, modelIdOffset, satelliteIdOffset, functionCodeOffset
174	- `successFrameId`: 执行成功帧ID
175	- `highlightConfigs`: 测试工具高亮配置
176	
177	`ScoeSatelliteConfig` 字段：
178	- `id`: 配置ID
179	- `satelliteId`: 卫星ID
180	- `sendConfig`: {satelliteIdentifier, messageIdentifier, sourceIdentifier, destinationIdentifier, udpIpAddress, udpPort}
181	- `receiveConfig`: {satelliteIdentifier, messageIdentifier, sourceIdentifier, destinationIdentifier, modelId, satelliteId, recognitionMessageId, recognitionSourceId, recognitionDestinationId}
182	
183	- 持久化方式：通过 `dataStorageAPI.scoeSatelliteConfigs.saveAll/load` 写入文件
184	- 保存时机：每次修改后立即保存（addSatelliteConfig、deleteSatelliteConfig、saveAllConfigs）
185	- 加载时机：initialize 时从文件加载
186	
187	#### 1.9 帧模板配置（frameTemplateStore）
188	
189	**文件**: `src/stores/frames/frameTemplateStore.ts`
190	
191	- 帧定义列表（Frame[]）通过 `dataStorageAPI.framesConfig` CRUD
192	- 持久化到文件系统
193	- 保存时机：每次创建/更新/删除后立即保存
194	- 加载时机：手动调用 fetchFrames
195	
196	`Frame` 中的配置性字段：
197	- `options`: FrameOptions {autoChecksum, bigEndian, includeLengthField}
198	- `identifierRules`: IdentifierRule[] 帧识别规则
199	- `isFavorite`: 收藏标记
200	
201	#### 1.10 多帧发送配置（sendFrameInstancesStore + 组件局部状态）
202	
203	**文件**: `src/stores/frames/sendFrameInstancesStore.ts`, `src/components/frames/FrameSend/EnhancedSequentialSend/EnhancedSequentialSendDialog.vue`
204	
205	| 配置项 | 类型 | 默认值 | 存储键 | 说明 |
206	|--------|------|--------|--------|------|
207	| multiFrameStrategyConfig | StrategyConfig | {type:'triggered', triggerType:'condition', responseDelay:0} | `multi-frame-strategy-config` | 多帧全局策略 |
208	| selectedInstances | FrameInstanceInTask[] | [] | `enhanced-sequential-send-instances` | 多帧发送选中的实例列表 |
209	| variableInterval | number | 1000 | `enhanced-sequential-send-variable-interval` | 可变参数发送间隔 |
210	
211	#### 1.11 帧字段默认配置常量
212	
213	**文件**: `src/config/frameDefaults.ts`, `src/utils/frames/defaultConfigs.ts`
214	
215	这些不是持久化配置，而是代码内嵌的默认值常量：
216	
217	| 常量 | 默认值 | 说明 |
218	|------|--------|------|
219	| DEFAULT_FRAME_OPTIONS | {autoChecksum:true, bigEndian:false, includeLengthField:false} | 新帧默认选项 |
220	| DEFAULT_FILTER_OPTIONS | {protocol:'', frameType:'', direction:'', dateRange:undefined} | 默认过滤条件 |
221	| DEFAULT_IDENTIFIER_RULES | {startIndex:0, endIndex:7, operator:'eq', value:'0x00', logicOperator:'and'} | 默认识别规则 |
222	| DEFAULT_VALID_OPTION | {isChecksum:false, startFieldIndex:'0', endFieldIndex:'0', checksumMethod:'sum8'} | 默认校验设置 |
223	| FRAMES_PER_PAGE | 20 | 每页帧数 |
224	| RECENT_FRAMES_LIMIT | 10 | 最近使用帧数上限 |
225	| createDefaultTimedConfig() | {type:'timed', sendInterval:1000, repeatCount:10, isInfinite:false, startDelay:0} | 定时策略默认值 |
226	| createDefaultTriggerConfig() | {type:'triggered', triggerType:'condition', responseDelay:0, sourceId:'', triggerFrameId:'', conditions:[...]} | 触发策略默认值 |
227	| createDefaultExpressionConfig() | {expressions:[{condition:'true', expression:'0'}], variables:[]} | 表达式默认值 |
228	
229	### 二、配置持久化行为总结
230	
231	#### 2.1 存储位置
232	
233	| 机制 | 使用场景 | 位置 |
234	|------|---------|------|
235	| `useStorage` (VueUse -> localStorage) | 轻量级用户偏好、表格配置、串口配置等 | 浏览器 localStorage |
236	| `dataStorageAPI` (IPC -> main -> 文件) | 帧定义、SCOE 卫星配置等大结构数据 | 用户数据目录文件 |
237	
238	#### 2.2 保存时机
239	
240	- localStorage（useStorage）：**实时**，每次响应式值变更时自动写入
241	- 文件存储（dataStorageAPI）：**操作后立即**，每次 CRUD 操作完成后保存
242	- 无批量保存或退出时保存的机制
243	
244	#### 2.3 加载时机
245	
246	- localStorage（useStorage）：**首次访问时**，store 创建时自动从 localStorage 读取
247	- 文件存储（dataStorageAPI）：**显式调用**，如 `fetchFrames()`、`loadSatelliteConfigs()`
248	
249	#### 2.4 配置恢复/重置行为
250	
251	- `frameFilterStore.resetFilters()`: 重置过滤条件为默认值（不持久化的配置）
252	- `dataDisplayStore`: 无显式重置方法
253	- `settingsStore`: 无重置方法
254	- `serialStore`: 无重置方法
255	- `scoeStore`: 无重置方法（需手动修改配置）
256	- **结论：旧系统几乎没有配置恢复/重置功能**
257	
258	### 三、新系统对应关系
259	
260	#### 3.1 已在新系统中有对应的配置
261	
262	| 旧配置 | 新系统对应 | 新系统文件 |
263	|--------|-----------|-----------|
264	| autoStartRecording | settings.recording.autoStartRecording | `rewrite/src/features/settings/core/types.ts` |
265	| csvDefaultOutputPath | settings.recording.csvDefaultOutputPath | 同上 |
266	| csvSaveInterval (分钟) | settings.recording.csvSaveIntervalMinutes | 同上 |
267	| maxHistoryHours | settings.storage.maxHistoryHours | 同上 |
268	| enableAutoSave | settings.storage.enableAutoSave | 同上 |
269	| enableHistoryStorage | settings.storage.enableHistoryStorage | 同上 |
270	| updateInterval | settings.general.updateInterval | 同上 |
271	
272	新系统 settings feature 已实现的增强：
273	- `SettingsSnapshot` 统一数据结构，schema 版本化
274	- `SettingsService` 提供 replace/update/reset 操作
275	- `SettingsReader` 只读接口
276	- 验证和归一化机制（validation.ts, normalize.ts）
277	- 按 scope 重置（all/recording/storage/general）
278	- 持久化通过 `FeaturePersistence` 写入 `{dataDir}/state/settings.json`
279	
280	#### 3.2 在新系统中可能缺失的配置
281	
282	| 旧配置 | 新系统状态 | 建议 |
283	|--------|-----------|------|
284	| 串口配置（per-port options, default options, lastUsedPort） | connection feature 有 TransportConfig，但串口参数配置待确认 | 需检查 connection feature 是否覆盖 |
285	| 帧过滤器配置（searchQuery, filters, sortOrder） | frame feature 有 filter 相关能力，待确认细节 | 需检查 frame feature filter API |
286	| 表格显示配置（table1Config, table2Config, displayMode, selectedGroupId） | display feature 存在，待确认 | 需检查 display feature |
287	| 星座图配置（scatterConfig: bitWidth, sampleCount, 数据源） | display feature 待确认 | 需检查 display feature |
288	| 历史分析图表配置（multiChartSettings） | 待确认 | 需检查 history/display 相关 |
289	| 状态指示灯配置（indicators, isEnabled, valueMappings） | 待确认 | 需检查 status feature |
290	| 高速存储配置（StorageConfig, FrameHeaderRule） | storage-local-baseline feature 存在，待确认 | 需检查 storage feature |
291	| SCOE 全局配置（globalConfig, satelliteConfigs） | command-ingress feature 存在，待确认 | 需检查 command-ingress |
292	| 多帧发送策略配置（multiFrameStrategyConfig, selectedInstances） | send feature + task feature 存在，待确认 | 需检查 send/task |
293	| 帧字段默认配置常量 | shared/ 或 frame/core 待确认 | 需检查常量位置 |
294	
295	#### 3.3 不再需要的配置
296	
297	| 旧配置 | 原因 |
298	|--------|------|
299	| `showFilterPanel` (frameFilterStore) | UI 展开状态，运行时临时状态，无需持久化 |
300	| `autoScroll` (serialStore) | UI 滚动行为，运行时临时状态 |
301	| `enableRecording` (displaySettings) | 运行时状态（是否正在记录），非配置项 |
302	| 串口消息记录（receivedMessagesMap, sentMessagesMap） | 运行时缓冲区，非配置项 |
303	
304	### 四、逐条可观测行为清单
305	
306	#### 4.1 保留 -- 应用设置
307	
308	1. **自动开始记录开关**
309	   - 旧行为：应用启动后，如果 autoStartRecording=true，自动开始数据记录
310	   - 代码位置：`src/stores/settingsStore.ts:10` + `src/stores/frames/dataDisplayStore.ts` 中引用
311	   - 新系统对应：settings feature `recording.autoStartRecording`
312	   - oracle 评估：高可靠性（useStorage 直接持久化）
313	   - 建议：**保留**
314	
315	2. **CSV 导出路径记忆**
316	   - 旧行为：记住用户选择的 CSV 默认输出路径
317	   - 代码位置：`src/stores/settingsStore.ts:13`
318	   - 新系统对应：settings feature `recording.csvDefaultOutputPath`
319	   - oracle 评估：高可靠性
320	   - 建议：**保留**
321	
322	3. **CSV 保存间隔配置**
323	   - 旧行为：用户可设置 CSV 保存间隔（默认5分钟），实际值乘以 60*1000 转为毫秒
324	   - 代码位置：`src/stores/settingsStore.ts:16` + `src/stores/frames/dataDisplayStore.ts:153`
325	   - 新系统对应：settings feature `recording.csvSaveIntervalMinutes`
326	   - oracle 评估：高可靠性
327	   - 建议：**保留**
328	
329	4. **数据更新间隔**
330	   - 旧行为：控制数据收集定时器间隔（默认1000ms）
331	   - 代码位置：`src/stores/frames/dataDisplayStore.ts:150`
332	   - 新系统对应：settings feature `general.updateInterval`
333	   - oracle 评估：高可靠性
334	   - 建议：**保留**
335	
336	5. **最大历史记录小时数**
337	   - 旧行为：控制历史数据保留时间（默认24小时）
338	   - 代码位置：`src/stores/frames/dataDisplayStore.ts:153`
339	   - 新系统对应：settings feature `storage.maxHistoryHours`
340	   - oracle 评估：高可靠性
341	   - 建议：**保留**
342	
343	6. **自动保存开关**
344	   - 旧行为：是否启用自动保存
345	   - 代码位置：`src/stores/frames/dataDisplayStore.ts:154`
346	   - 新系统对应：settings feature `storage.enableAutoSave`
347	   - oracle 评估：高可靠性
348	   - 建议：**保留**
349	
350	7. **历史数据存储开关**
351	   - 旧行为：是否启用历史数据存储到文件
352	   - 代码位置：`src/stores/frames/dataDisplayStore.ts:155`
353	   - 新系统对应：settings feature `storage.enableHistoryStorage`
354	   - oracle 评估：高可靠性
355	   - 建议：**保留**
356	
357	#### 4.2 保留 -- 串口配置
358	
359	8. **每个串口独立配置记忆**
360	   - 旧行为：每个串口路径有独立的波特率、数据位、停止位、校验位、流控配置，记住用户上次设置
361	   - 代码位置：`src/stores/serialStore.ts:54` (`portSerialOptions`)
362	   - 新系统对应：待确认 connection feature
363	   - oracle 评估：高可靠性（localStorage 持久化）
364	   - 建议：**保留**
365	
366	9. **全局默认串口配置**
367	   - 旧行为：新串口使用默认配置 {baudRate:9600, dataBits:8, stopBits:1, parity:'none', flowControl:'none'}
368	   - 代码位置：`src/stores/serialStore.ts:22-29,57-59`
369	   - 新系统对应：待确认 connection feature 默认值
370	   - oracle 评估：高可靠性
371	   - 建议：**保留**
372	
373	10. **上次使用的串口记忆**
374	    - 旧行为：记住上次使用的串口路径，用于默认选择
375	    - 代码位置：`src/stores/serialStore.ts:52`
376	    - 新系统对应：待确认 connection feature
377	    - oracle 评估：中可靠性（依赖 localStorage，串口路径可能因硬件变化失效）
378	    - 建议：**保留**（作为可选优化，非核心行为）
379	
380	#### 4.3 保留 -- 数据显示配置
381	
382	11. **双表格分组选择记忆**
383	    - 旧行为：两个表格各自记住选中的分组ID、显示模式（表格/图表/星座图）、图表选中项
384	    - 代码位置：`src/stores/frames/dataDisplayStore.ts:118-128`
385	    - 新系统对应：待确认 display feature
386	    - oracle 评估：高可靠性
387	    - 建议：**保留**
388	
389	12. **星座图参数配置持久化**
390	    - 旧行为：记住位宽、采样数、点大小、刷新间隔、I/Q数据源配置
391	    - 代码位置：`src/stores/frames/dataDisplayStore.ts:131-147`
392	    - 新系统对应：待确认 display feature
393	    - oracle 评估：高可靠性
394	    - 建议：**保留**
395	
396	13. **历史分析多图表配置**
397	    - 旧行为：记住图表数量（1~4）、每个图表的标题和选中的数据项
398	    - 代码位置：`src/stores/historyAnalysis.ts:46-55`
399	    - 新系统对应：待确认
400	    - oracle 评估：高可靠性
401	    - 建议：**保留**
402	
403	#### 4.4 保留 -- 状态指示灯
404	
405	14. **状态指示灯配置持久化**
406	    - 旧行为：记住所有自定义指示灯的配置（标签、关联分组/数据项、值-颜色映射、启用状态）
407	    - 代码位置：`src/stores/statusIndicators.ts:17-19`
408	    - 新系统对应：待确认 status feature
409	    - oracle 评估：高可靠性
410	    - 建议：**保留**
411	
412	#### 4.5 保留 -- 高速存储配置
413	
414	15. **高速存储配置持久化**
415	    - 旧行为：记住是否启用、识别规则、最大文件大小、轮转设置；初始化时与 main 进程双向同步
416	    - 代码位置：`src/stores/highSpeedStorageStore.ts:22-28,245-264`
417	    - 新系统对应：待确认 storage-local-baseline feature
418	    - oracle 评估：高可靠性（localStorage + main 进程同步）
419	    - 建议：**保留**
420	
421	#### 4.6 保留 -- SCOE 配置
422	
423	16. **SCOE 全局配置持久化**
424	    - 旧行为：TCP/UDP 连接参数、字节偏移量、自动连接开关等保存到文件
425	    - 代码位置：`src/stores/scoeStore.ts:117-132`, `src/types/scoe/index.ts:184-203`
426	    - 新系统对应：待确认 command-ingress feature
427	    - oracle 评估：高可靠性（文件持久化）
428	    - 建议：**保留**（作为 command-ingress 配置的一部分）
429	
430	17. **SCOE 卫星配置列表持久化**
431	    - 旧行为：支持多卫星配置的 CRUD，每次操作后立即保存
432	    - 代码位置：`src/stores/scoeStore.ts:82-193`
433	    - 新系统对应：待确认 command-ingress feature
434	    - oracle 评估：高可靠性
435	    - 建议：**保留**
436	
437	#### 4.7 保留 -- 帧定义与默认配置
438	
439	18. **帧定义持久化**
440	    - 旧行为：帧定义列表（含字段、选项、识别规则）保存到文件，支持 CRUD
441	    - 代码位置：`src/stores/frames/frameTemplateStore.ts:26-145`
442	    - 新系统对应：frame feature 已实现
443	    - oracle 评估：高可靠性
444	    - 建议：**保留**
445	
446	19. **帧字段默认配置常量**
447	    - 旧行为：新帧使用默认选项（自动校验和、小端序、无长度字段等）
448	    - 代码位置：`src/config/frameDefaults.ts:86-91`
449	    - 新系统对应：待确认 frame/core 默认值
450	    - oracle 评估：高可靠性（硬编码常量）
451	    - 建议：**保留默认值**
452	
453	20. **发送策略默认配置常量**
454	    - 旧行为：定时发送默认1秒间隔/10次重复；触发发送默认条件触发/无延迟
455	    - 代码位置：`src/utils/frames/defaultConfigs.ts:23-46`
456	    - 新系统对应：待确认 send/task feature
457	    - oracle 评估：高可靠性
458	    - 建议：**保留默认值**
459	
460	#### 4.8 保留 -- 多帧发送配置
461	
462	21. **多帧发送策略和实例序列持久化**
463	    - 旧行为：记住多帧发送的策略配置、选中的实例列表、可变参数间隔
464	    - 代码位置：`src/stores/frames/sendFrameInstancesStore.ts:42-46`, `EnhancedSequentialSendDialog.vue:155,182-185`
465	    - 新系统对应：待确认 send/task feature
466	    - oracle 评估：中可靠性（localStorage，引用可能因帧实例删除失效）
467	    - 建议：**保留**（策略配置和间隔设置；实例列表引用需做失效检查）
468	
469	#### 4.9 排除 -- 不需要保留的行为
470	
471	22. **帧过滤器 UI 状态**
472	    - 旧行为：searchQuery、filters、sortOrder、showFilterPanel 不持久化
473	    - 代码位置：`src/stores/frames/frameFilterStore.ts`
474	    - 建议：**排除**（旧系统本身就不持久化，运行时临时状态）
475	
476	23. **串口消息缓冲区**
477	    - 旧行为：receivedMessagesMap、sentMessagesMap 为运行时缓冲区，限制100条
478	    - 代码位置：`src/stores/serialStore.ts:62-89`
479	    - 建议：**排除**（运行时状态）
480	
481	24. **串口自动滚动**
482	    - 旧行为：autoScroll 控制接收区是否自动滚动
483	    - 代码位置：`src/stores/serialStore.ts:95`
484	    - 建议：**排除**（UI 运行时状态，且旧系统不持久化）
485	
486	25. **记录运行时状态**
487	    - 旧行为：recordingStatus（isRecording、startTime、recordCount 等）为运行时状态
488	    - 代码位置：`src/stores/frames/dataDisplayStore.ts:175-181`
489	    - 建议：**排除**（运行时状态，非配置项）
490	
491	### 五、新系统 settings feature 与旧系统差异
492	
493	| 维度 | 旧系统 | 新系统 |
494	|------|--------|--------|
495	| 配置集中度 | 分散在 10+ 个 store | settings feature 统一管理应用级配置 |
496	| 持久化机制 | localStorage（useStorage）+ 文件（dataStorageAPI） | JSON 文件（{dataDir}/state/settings.json） |
497	| 数据结构 | 扁平 key-value（localStorage） | 嵌套 SettingsSnapshot（schema 版本化） |
498	| 校验 | 无 | normalize + validation |
499	| 重置 | 仅 frameFilter 有 resetFilters() | 按 scope 重置（all/recording/storage/general） |
500	| 只读保护 | 无 | ReadonlyDeep 类型 |
501	| 串口配置 | localStorage per-port map | 待确认（connection feature） |
502	| SCOE/帧/存储 | 独立文件存储 | 各 feature 自行管理持久化 |
503	
504	新系统 settings feature 目前只覆盖了旧系统 `settingsStore` + `dataDisplayStore.displaySettings` 中的部分配置（7 项）。以下旧配置在新系统中尚未确认有对应：
505	
506	- 串口配置（per-port / default / lastUsedPort）
507	- 表格显示配置（table1Config, table2Config, displayMode, selectedGroupId）
508	- 星座图配置（scatterConfig）
509	- 历史分析图表配置（multiChartSettings）
510	- 状态指示灯配置（indicators, isEnabled, valueMappings）
511	- 高速存储配置（StorageConfig, FrameHeaderRule）
512	- SCOE 配置（globalConfig, satelliteConfigs）
513	- 多帧发送策略配置
514	
515	这些配置可能归入各自 feature 的配置管理，也可能需要 settings feature 统一协调。这属于设计决策，不在本调研范围。
516	
517	## 后续
518	
519	无。
520	
```

> AGENT

全部 9 个 agent 文件已读完。开始写综合报告。

> TOOL

tool_use Write
id: call_6ff2af99002e4ef1b5a4152a
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-legacy-observable-behaviors.md",
  "content": "# [S004] 旧系统可观测行为提取 — 综合报告\n\n> 2026-05-19 | 调研 | 完成\n> 9 个 agent 并行提取，3 批 × 3\n\n## 目标\n\n从旧系统代码中提取所有必须保留的可观测业务行为，作为集成测试 oracle 来源和新系统验收基线。\n\n---\n\n## 一、提取总览\n\n| Agent | 调研范围 | 提取行为数 | 保留 | 排除 | 需重新设计 |\n|-------|---------|-----------|------|------|-----------|\n| 1 | receive/send 数据流 | 36 | 30 | 6 | — |\n| 2 | SCOE/task 执行 | 34 | 34 | 0 | — |\n| 3 | 连接管理 | 26 | 13 | 6 | 7 |\n| 4 | 表达式/解析/条件 | 27 | 19 | 8 | — |\n| 5 | 存储/历史/CSV | 27 | 25 | 2 | — |\n| 6 | 帧定义管理 | 24 | 20 | 4 | — |\n| 7 | 状态指示/健康检查/统计 | 27 | 26 | 1 | — |\n| 8 | 设置/配置 | 25 | 21 | 4 | — |\n| 9 | 页面入口/路由 | 10 路由 | 6 | 2 | 2 |\n| **合计** | | **~236** | **~194** | **~33** | **~9** |\n\n详细产出见各 agent 文件：\n- `S004-agent1-receive-send.md`\n- `S004-agent2-scoe-task.md`\n- `S004-agent3-connection.md`\n- `S004-agent4-expression-parser.md`\n- `S004-agent5-storage-history-csv.md`\n- `S004-agent6-frame-definition.md`\n- `S004-agent7-status-indicators.md`\n- `S004-agent8-settings-config.md`\n- `S004-agent9-routes-pages.md`\n\n---\n\n## 二、按 feature 归口的行为清单\n\n### 2.1 connection feature（连接管理）\n\n**必须保留（13 项）：**\n1. 串口四状态生命周期（disconnected → connecting → connected → error）\n2. 串口配置参数集（baudRate/dataBits/stopBits/parity/flowControl）+ 每端口独立配置 + 热更新（关闭重开）\n3. 多串口并发管理（独立状态/配置/数据通道）\n4. TCP 客户端连接（setNoDelay + 5000ms 超时 + \\r\\n 分割）\n5. TCP Server 多客户端管理（广播发送）\n6. UDP 绑定 + 远程主机列表 + 广播模式\n7. 统一连接目标视图（serial:{port} / network:{connId} / network:{connId}:{remoteId}）\n8. 连接统计（bytes/messages/activity per connection）\n9. 最后使用串口记忆\n10. 应用退出时关闭所有连接\n11. TCP \\r\\n 数据分割（需参数化）\n12. 网络连接卡片网格展示（最多 9 个，四态颜色/图标/文本）\n13. 连接状态事件驱动实时更新（500ms 防抖）\n\n**排除（6 项）：**\n- receivedMessagesMap/sentMessagesMap 100 条内存历史（调试功能）\n- 自动连接/自动重连（类型定义存在但未实现）\n- 串口热插拔自动检测（无实现）\n- Windows 注册表 PowerShell 枚举方式（应迁移到 serialport 库）\n- clearBuffer 只重置计数器不真正清空（语义不清）\n- autoOpen: false 配置项（始终 false）\n\n**需重新设计（7 项）：**\n- 配置持久化方式（localStorage → 新持久化层）\n- 网络连接配置持久化（旧系统无持久化）\n- IPC 通道命名和 preload 桥接方式\n- 连接目标 ID 编码规则\n- TCP \\r\\n 分割参数化\n- UDP 远程主机管理持久化\n- 高速存储配置持久化\n\n**关键 oracle：** 四状态模型完整、TCP/UDP 行为完整、高速存储分流链路完整。\n\n---\n\n### 2.2 receive feature（接收管线）\n\n**必须保留（17 项）：**\n1. 串口/网络数据接收 → 自动帧匹配 → 字段解析 → UI 更新\n2. 数据项值增量更新（跳过表达式字段）\n3. 帧级统计（每帧 totalReceived/lastReceiveTime/checksumFailures/errorCount）\n4. 全局统计（收发包/字节/匹配率/错误率/系统时间）\n5. 最近 100 个数据包记录（调试用）\n6. 配置自动保存和主进程缓存同步（1s/500ms 防抖）\n7. 映射关系验证和孤立数据项清理\n8. 表达式字段接收后立即计算\n9. 帧识别规则匹配（8 种运算符 AND 逻辑）\n10. 11 种数据类型解析（含 BigInt 64 位）\n11. 大端/小端字节序\n12. applyFactor（乘以 factor，toFixed(5) 限 5 位小数）\n13. direct/indirect 数据字段区分\n14. labelOptions 标签显示\n15. receive→send 条件触发桥接\n16. 条件触发 AND/OR 短路逻辑\n17. 帧统计面板展示（全局+单帧两种粒度重置）\n\n**关键 oracle：** `public/data/frames/configs/*.json` 中的帧定义可构造固定输入→验证输出。\n\n---\n\n### 2.3 send feature（发送管线）\n\n**必须保留（18 项）：**\n1. 单帧发送（表达式计算→倍率→序列化→路由→统计）\n2. 顺序发送任务\n3. 定时发送任务（间隔/次数/无限循环/首次立即）\n4. 定时任务参数变化\n5. 条件触发发送（监听→匹配→延时→执行→持续监听）\n6. 时间触发发送（6 种重复粒度 + endTime）\n7. 任务暂停/恢复（旧行为有缺陷，新系统应正确实现）\n8. 任务停止（清理定时器+监听器）\n9. 连接断开自动暂停\n10. 发送统计（实例级 sendCount/lastSentAt）\n11. SCOE UDP 发送记录\n12. 实例间延时\n13. 帧实例 deepClone 缓存（隔离运行时副本和持久化实例）\n14. 任务进度追踪（1s 批量同步）\n15. 触发监听器管理\n16. 帧实例导入/导出 JSON\n17. 帧模板更新联动实例\n18. UDP 远程主机发送\n\n**关键 oracle：** 固定帧实例+目标→捕获发送字节可录制。\n\n---\n\n### 2.4 task feature（任务执行引擎）\n\n**必须保留（从 SCOE/task agent 提取的 34 项）：**\n- 7 种任务状态完整转换（idle/running/paused/completed/error/waiting-trigger/waiting-schedule）\n- 定时发送配置模型（间隔/重复/无限循环）\n- 触发发送配置模型（条件触发 + 时间触发）\n- 条件评估逻辑（5 种操作符 + AND/OR 短路）\n- 4 种多帧策略（immediate/timed/triggered/variable）\n- 可变参数发送（fieldVariations + 参数数组长度验证）\n- 任务配置导入/导出\n- 活跃任务监控（列表/进度/操作控制）\n- 进度批量更新优化（1s 缓存同步）\n\n---\n\n### 2.5 command-ingress feature（指令接入 / SCOE）\n\n**必须保留：**\n1. SCOE 帧识别流程（功能码验证 + 三标志验证 + 型号/卫星 ID 验证）\n2. SCOE 校验和验证（累加取模 256）\n3. SCOE 完成条件匹配（固定值模式 + 参数索引匹配模式）\n4. SCOE 接收指令配置模型（6 种功能）\n5. SCOE 全局字节偏移配置（6 个偏移量）\n6. SCOE 卫星配置管理（多卫星 CRUD）\n7. SCOE 状态统计（12 个指标）\n8. SCOE 测试工具（数据录制 + 高亮显示）\n9. SCOE 健康自检（卫星加载 + 帧加载 + 连接路径）\n10. SCOE 链路自检（载波/定时/帧三个锁定状态，需改用 ID 匹配）\n\n**关键发现：** SCOE 命令接收与执行的运行时链路在 renderer 侧代码中未找到完整实现，可能在 main process 或尚未实现。\n\n---\n\n### 2.6 frame feature（帧定义管理）\n\n**必须保留：**\n1. 帧 CRUD（深拷贝编辑、变更检测、ID 修改含冲突检测）\n2. 11 种数据类型 + 4 种输入类型（input/select/radio/expression）\n3. 字段操作（添加/删除/复制/移动/编辑 tempField 模式）\n4. 字段验证（name 非空、至少一字段、字段名唯一、bytes length > 0）\n5. 校验和配置（4 种方法：xor8/sum8/crc16/crc32）\n6. 帧识别规则（8 种运算符 AND 逻辑）\n7. 帧选项（autoChecksum/bigEndian/includeLengthField）\n8. JSON 导入/导出\n9. 帧实例从帧模板创建（全字段复制、configurable 标记）\n10. 帧更新后实例同步（已存在保留 value、新字段用 defaultValue）\n11. 收藏功能（帧级+实例级独立）\n12. 帧列表过滤/排序（搜索/direction/日期范围/ID/name/date/usage）\n13. 帧复制（深拷贝 + `(副本)` 命名 + 新 ID）\n\n**排除：**\n- isSCOEFrame 标记（统一通过指令接入 feature）\n- 全量覆盖式导入（应提供冲突处理）\n- 无确认删除（应加确认对话框）\n- 无级联清理（应在帧删除时触发关联清理）\n\n---\n\n### 2.7 storage feature（存储/历史/高速存储）\n\n**必须保留：**\n1. JSON 文件按小时存储历史数据\n2. 增量追加记录到小时文件\n3. 定时收集（1s）+ 定期持久化（5min）+ 小时边界自动切换\n4. 自动开始记录（可配置）\n5. 循环缓冲区 + 动态容量 + 时间过期清理\n6. 查询可用小时键 + 按时间范围批量加载\n7. CSV 导出（文件名/时间范围/数据项/6 种时间格式/预设路径）\n8. CSV 格式（逗号分隔、UTF-8、{group}_{item} 表头、ISO 时间戳）\n9. 高速存储帧头匹配 + 连接 ID 匹配触发\n10. 匹配高速存储规则的数据**不发送到渲染进程**（关键架构分流）\n11. 高速存储文件格式（每帧一行十六进制大写）\n12. 文件轮转（100MB + 5 文件）\n13. 高速存储统计\n14. 重置统计 = 删除当前文件\n15. 过期数据清理（按天保留）\n16. 压缩旧数据文件（gzip）\n\n**关键 oracle：** 高速存储分流行为在 `networkHandlers.ts:515-517` 有明确代码（return 跳过 emitDataEvent）。\n\n---\n\n### 2.8 shared/ expression engine（表达式引擎）\n\n**必须保留（19 项核心）：**\n1. 条件-表达式对顺序评估，默认值 0\n2. 13 种数学函数注入\n3. 4 种变量数据源（CURRENT_FIELD/FRAME_FIELD/GLOBAL_STAT/SCOE_DATA），未解析默认 0\n4. 拓扑排序（Kahn 算法）+ 循环依赖检测\n5. 类型处理（float/double 保持，整数 Math.floor）\n6. 接收帧解析后立即计算；发送帧组帧前计算\n7. 错误容错（不崩溃、错误不应用、console.error 记录）\n8. 通用比较运算符（6 种 + 自动数值/字符串检测）\n9. 发送触发条件（5 种操作符 + AND/OR 短路逻辑）\n\n**排除（8 项实现细节）：**\n- `new Function` 求值方式\n- 依赖缓存策略\n- 计算历史记录\n- 各 store 直接依赖（新系统通过 feature public API）\n\n**关键 oracle：** `public/data/frames/configs/3.json` 含多条件表达式+变量映射+自引用。\n\n---\n\n### 2.9 display/visualization feature（数据展示）\n\n**必须保留：**\n1. 双表格+三模式（table/chart/constellation）\n2. 星座图（IQ 数据源配置 + 按位宽提取 + 定时刷新）\n3. 按需数据收集优化\n4. 历史数据按分组/数据项过滤 + 多图表展示（1-4 图表）\n5. 多图表独立配置（标题/Y 轴/数据项选择）\n\n---\n\n### 2.10 settings feature（配置管理）\n\n**必须保留（21 项）：**\n- 应用级 7 项（autoStartRecording、csvDefaultOutputPath、csvSaveInterval、updateInterval、maxHistoryHours、enableAutoSave、enableHistoryStorage）\n- 串口配置 3 项（per-port、default、lastUsedPort）\n- 数据显示 3 项（双表格分组选择、星座图参数、历史图表配置）\n- 状态指示灯 1 项\n- 高速存储 1 项\n- SCOE 配置 2 项\n- 帧定义默认值 3 项\n- 多帧发送策略 1 项\n\n**排除（4 项运行时状态）：**\n- 帧过滤器 UI 状态（不持久化）\n- 串口消息缓冲区\n- 自动滚动\n- 记录运行时状态\n\n---\n\n## 三、关键发现\n\n### 3.1 新系统缺失的 3 个页面\n\n| 旧页面 | 功能 | 优先级 |\n|-------|------|--------|\n| `/storage` | 高速存储管理（几百 Mbps 网络数据存储配置） | 高 |\n| `/history` | 历史数据分析（时间选择+多图表+CSV 导出） | 高 |\n| `/settings` | 系统设置 | 中 |\n\n### 3.2 SCOE 命令执行运行时链路缺失\n\n旧代码中定义了 SCOE 接收指令的完整配置模型（6 种功能码、完成条件、校验和），但 renderer 侧代码未找到\"收到 TCP 数据 → 解析指令码 → 匹配功能 → 执行\"的完整运行时链路。可能位于 main process 或尚未实现。需进一步确认。\n\n### 3.3 高速存储分流是关键架构决策\n\n匹配高速存储规则的网络数据**不发送到渲染进程**（`networkHandlers.ts:515-517` return 跳过 emitDataEvent）。这意味着部分网络数据只有文件级记录，不经过 receive 管线。新系统必须保持等价行为。\n\n### 3.4 旧系统已知缺陷清单（不应复制到新系统）\n\n| 缺陷 | 位置 | 影响 |\n|------|------|------|\n| 暂停后定时器不真正暂停 | useSendTaskController.ts | 定时器继续触发但被 isTaskStillRunning 跳过 |\n| 任务停止状态为 completed 而非 cancelled | sendTasksStore | 用户停止和自然完成无法区分 |\n| 串行处理锁可能成为高频瓶颈 | receiveFramesStore.ts | 所有数据源共享一个处理锁 |\n| SCOE 模块直接耦合 receiveFramesStore | receiveFramesStore.ts | SCOE 逻辑嵌入 receive 主路径 |\n| globalStats 累加计数器无持久化 | globalStatsStore | 重启后统计清零 |\n| 条件匹配直接访问 receive store 内部 | useSendTaskTriggerListener.ts | 触发监听器直接访问 receive store |\n| 进度缓存 1s 批量同步 | sendTasksStore | 快速完成任务进度显示不准确 |\n| 帧删除无级联清理 | frameTemplateStore | 关联实例/映射不会被自动清理 |\n| 帧导入全量覆盖 | FrameList.vue | 导入会覆盖所有现有帧 |\n| TCP \\r\\n 分割硬编码 | networkHandlers.ts | 不支持其他分割符 |\n| 链路自检用数据项标签名匹配 | linkCheck.ts | 脆弱，应改用 ID |\n\n### 3.5 Oracle 来源评估\n\n| 行为领域 | oracle 可信度 | 来源 |\n|---------|-------------|------|\n| 串口/网络连接生命周期 | 高 | 四状态模型代码完整 |\n| 帧解析（11 种类型） | 高 | `public/data/frames/configs/*.json` |\n| 表达式引擎 | 高 | `configs/3.json` + 代码逻辑 |\n| 高速存储分流 | 高 | 代码链路完整 |\n| SCOE 命令执行运行时 | 低 | 配置模型完整但运行时链路未找到 |\n| CSV 导出格式 | 高 | 代码逻辑完整 |\n| 任务状态机 | 高 | 7 状态 + 转换规则完整 |\n\n---\n\n## 四、排除规则（供 S006 综合阶段使用）\n\n以下旧行为**不进入**集测范围：\n\n1. 已标记为旧系统缺陷的行为（上表 11 项）\n2. 实现细节（`new Function`、缓存策略、LRU、序列化方式）\n3. 各 store 间的直接依赖（新系统通过 feature public API）\n4. 纯 UI 运行时状态（展开/折叠、自动滚动、过滤器面板）\n5. 硬编码的旧协议预设（网络测试工具快速发送）\n6. isSCOEFrame 标记（统一到指令接入）\n7. 全量覆盖式导入导出策略\n8. Windows 注册表串口枚举方式\n\n---\n\n## 五、集测高价值 oracle 样本清单\n\n| 文件 | 内容 | 集测价值 |\n|------|------|---------|\n| `public/data/frames/configs/*.json` | 帧定义（含表达式字段） | 帧解析/匹配 oracle |\n| `public/data/templates/framesConfig.json` | 帧配置模板 | 帧结构 oracle |\n| `public/data/templates/sendInstances.json` | 发送实例（含表达式） | 发送帧 oracle |\n| `public/data/templates/scoeReceiveCommands.json` | SCOE 接收指令 | 条件匹配 oracle |\n| `public/data/scoe/satelliteConfigs/1.json` | 卫星配置 | SCOE 识别参数 oracle |\n| `public/data/scoe/scoeConfigs/1.json` | SCOE 全局配置 | SCOE 帧识别偏移 oracle |\n\n---\n\n## 后续\n\n1. **S005（对话 5）**：新系统接缝审计，应重点验证上述行为在新系统代码中的实现覆盖度\n2. **S006（对话 6）**：综合所有提取结果，按 P0/P1/P2 分级形成最终集测清单\n3. SCOE 命令执行运行时链路需在接缝审计中确认\n4. 3 个缺失页面（存储/历史/设置）需确认是否在集测范围内\n"
}
```

> TOOL

tool_result
id: call_6ff2af99002e4ef1b5a4152a
```
File created successfully at: /mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/S004-legacy-observable-behaviors.md
```

> AGENT

更新 topic-index 和注册表。

> TOOL

tool_use Read
id: call_dd1e3061d73e43c4a110d35d
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/topic-index.md"
}
```

> TOOL

tool_result
id: call_dd1e3061d73e43c4a110d35d
```
1	# 集成测试体系建立
2	
3	> 状态: active | 时间跨度: 2026-05-19 ~ | 最后更新: 2026-05-19
4	
5	## 目标
6	
7	为 rewrite 系统建立集成测试体系。输入来源：26 天的讨论记录、10+ feature 设计文档、旧系统可观测行为、新系统实际代码。产出：结构化集测清单 + 可执行的端到端测试。
8	
9	## 进展线索
10	
11	- **S001** 历史讨论提取 — 12 个 agent 并行提取完成，合并报告已写入
12	  - 核心发现：835 tests 全部单元级+fake adapter级，零跨 feature 集成测试；十级验证 taxonomy 覆盖 Level 1-3 充分、Level 6-10 零覆盖
13	  - P0 缺口：端到端数据通路（6 条链路无测试）、Selector 不可变性（5 个 feature 浅拷贝）、持久化层（无自动 save + 软删除 bug + 恢复空转）、Composite Adapter（null dereference + 无测试）
14	  - P1 缺口：6 条 Feature 间接缝、6 项 Quality Gate 检查、条件匹配一致性、globalParams 推迟、文档-代码 drift
15	  - 13 项待确认需综合阶段核实
16	- **S002** Feature 设计文档提取 — 从 codestable/features/ 下所有 design.md + checklist.yaml 提取验收标准和跨 feature 交互契约
17	  - 对话 2 完成（上）：9 个 agent 覆盖 frame/connection/receive/send/expression-engine/runtime-wiring/settings/storage-local-baseline/display/status。关键发现：expression engine 最完整（29 条验收+性能已验证）、frame-real 6/6 done、storage 验证全部 pending、routingTick 是核心集成接缝、globalParams 推迟影响全局统计依赖、身份标识统一未完成（display/status 仍在用 groupId/dataItemId）
18	  - 对话 3 完成（下）：9 个 agent 覆盖 task/task-real/command-ingress/result-report/northbound/执行引擎/出站路由/feature 交互矩阵/旧系统行为。关键发现：task 70+ 单测覆盖充分但 Phase 2 类型重组未实施、command-ingress 25/25 checklist 全 done、result 有设计偏离（事件机制改 onSettled、类型大幅简化）、report 无独立 design、northbound 大部分能力未实现、43 条 feature 交互路径零集成测试覆盖、16 个 P0/P1/P2 集成测试接缝已识别
19	- **S003** 旧系统可观测行为提取 — 从旧代码提取必须保留的可观测行为，作为 oracle 来源
20	- **S004** 新系统接缝审计 — 读 runtime bridges、adapters、composite adapter，识别集成接缝和断裂点
21	- **S005** 集测范围综合 — 合并所有提取结果，按优先级分级，确定真 TCP / fake adapter / manual checklist 边界
22	- **S006** 集测实施 — 按范围写测试
23	
24	## 已确认结论
25	
26	- 54 个 spec 文件全部是单元级 + fake adapter 测试，feature 间接缝零覆盖
27	- H002 已完成 TCP 接线，composite adapter 可用，数据通路物理上已通
28	- connection-network-adapter.spec.ts 已有 Node `net` 模块先例，可在 Vitest 中直接起 TCP
29	
30	## 未决项
31	
32	- S001 13 项待确认需在 S006 综合阶段核实
33	- 集测范围清单尚未产出（S006）
34	- 旧系统哪些可观测行为必须保留尚未逐项确认（S004 对话 4）
35	- 新系统接缝审计尚未执行（S005 对话 5）
36	- 真 TCP 测试在 CI 环境（WSL2 / Windows）的兼容性待验证
37	
38	## 当前位置
39	
40	S001 对话 1 完成（12 agent 并行，4 批 × 3）。S002 对话 2-3 完成。S003-S006 待后续对话。
41	
42	## 对话规划
43	
44	### 对话 1：历史讨论提取（S001）
45	
46	输入：`.sessions/2026-04-23-rewrite-main-thread/` 下所有 S###.md 和 H###.md
47	
48	子 agent 策略：
49	- Agent 1：读 S001-S005 + S014，提取架构级验收承诺和质量规则中与测试相关的段落
50	- Agent 2：读 S006-S008，提取 feature 实施期的验收结论、known-gaps、测试数量
51	- Agent 3：读 S009-S012，提取 UI 阶段的审计发现、已知 bug、技术债
52	
53	产出格式：每条提取结果含 { 来源 note, feature, 具体行为描述, 验收结论, 已有测试证据, 缺口 }
54	
55	### 对话 2-3：Feature 设计文档提取（S002）
56	
57	输入：`codestable/features/` 下所有 design.md + checklist.yaml + brainstorm.md
58	
59	子 agent 策略（每轮 3 agent，按 feature 分组）：
60	- 对话 2：frame / connection / receive / send / expression-engine
61	- 对话 3：task / command-ingress / storage / settings / display / status
62	
63	产出：每条含 { feature, 验收标准原文, 跨 feature 交互契约, checklist 中测试项, 已实现/未实现 }
64	
65	### 对话 4：旧系统可观测行为提取（S003）
66	
67	输入：`src/` 下旧代码（stores/components/handlers）
68	
69	子 agent 策略：
70	- Agent 1：读旧 receive/send 相关代码，提取数据流行为
71	- Agent 2：读旧 SCOE/task 相关代码，提取命令执行行为
72	- Agent 3：读旧 storage/history/CSV 代码，提取持久化行为
73	
74	产出：每条含 { 旧行为描述, 代码位置, 新系统对应 feature, oracle 来源, 保留/排除 }
75	
76	### 对话 5：新系统接缝审计（S004）
77	
78	输入：`rewrite/src/runtime/` + `rewrite/src/features/*/adapters/` + `rewrite/src/features/*/services/`
79	
80	子 agent 策略：
81	- Agent 1：读所有 bridge 文件，分析数据流向和断裂风险
82	- Agent 2：读 composite-adapter + real-network-adapter + real-serial-adapter，分析 adapter 路由边界
83	- Agent 3：读 persistence.ts + bootstrap，分析启动加载和保存时机
84	
85	产出：接缝清单 + 每个接缝的测试建议
86	
87	### 对话 6：综合 + 排除（S005）
88	
89	合并 S001-S004 所有提取结果，去重、排除已有单测覆盖的项、分级优先级。
90	
91	产出：最终集测范围清单（文件形式，作为 S006 的直接合同）
92	
93	### 对话 7+：集测实施（S006）
94	
95	按 S005 的清单写测试。每轮对话覆盖一批。
96	
97	## 附属文件
98	
99	- `conversation-plan.md` — 7 轮对话完整规划 + 全部提示词
100	- `H001-scope-extraction-handoff.md` — 对话 1 提示词（模板 6 格式，conversation-plan 中已包含完整版）
101	
```

> TOOL

tool_use Edit
id: call_ca429edf08de417d8473044d
```json
{
  "replace_all": false,
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/topic-index.md",
  "old_string": "> 状态: active | 时间跨度: 2026-05-19 ~ | 最后更新: 2026-05-19",
  "new_string": "> 状态: active | 时间跨度: 2026-05-19 ~ | 最后更新: 2026-05-19 (对话 4)"
}
```

> TOOL

tool_result
id: call_ca429edf08de417d8473044d
```
The file /mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/topic-index.md has been updated successfully.
```

> TOOL

tool_use Edit
id: call_2da0784e641041c4a57d4ad6
```json
{
  "replace_all": false,
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/topic-index.md",
  "old_string": "- **S003** 旧系统可观测行为提取 — 从旧代码提取必须保留的可观测行为，作为 oracle 来源",
  "new_string": "- **S003** 旧系统可观测行为提取 — 从旧代码提取必须保留的可观测行为，作为 oracle 来源\n  - 对话 4 完成：9 agent 并行（3 批 × 3），覆盖 receive/send/SCOE/task/连接/表达式/解析/存储/历史/CSV/帧定义/状态指示/设置/路由\n  - 核心发现：~236 条可观测行为，~194 条保留，~33 条排除，~9 条需重新设计\n  - 3 个旧页面在新系统缺失（存储管理、历史分析、系统设置）\n  - SCOE 命令执行运行时链路在 renderer 侧未找到完整实现\n  - 高速存储分流是关键架构决策（匹配数据不转发渲染进程）\n  - 11 项旧系统已知缺陷标记为不复制\n  - 6 个高价值 oracle 样本文件已识别"
}
```

> TOOL

tool_result
id: call_2da0784e641041c4a57d4ad6
```
The file /mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/topic-index.md has been updated successfully.
```

> TOOL

tool_use Edit
id: call_4fdc91cf819f44e8a6695876
```json
{
  "replace_all": false,
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/topic-index.md",
  "old_string": "- 旧系统哪些可观测行为必须保留尚未逐项确认（S004 对话 4）",
  "new_string": "- 旧系统可观测行为已提取完成（S003 对话 4），~194 条保留行为作为 oracle 基线"
}
```

> TOOL

tool_result
id: call_4fdc91cf819f44e8a6695876
```
The file /mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/topic-index.md has been updated successfully.
```

> TOOL

tool_use Edit
id: call_8d236141b1ac400fabc33d50
```json
{
  "replace_all": false,
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/topic-index.md",
  "old_string": "S001 对话 1 完成（12 agent 并行，4 批 × 3）。S002 对话 2-3 完成。S003-S006 待后续对话。",
  "new_string": "S001 对话 1 完成、S002 对话 2-3 完成、S003 对话 4 完成（9 agent 并行）。S004 对话 5 待执行。"
}
```

> TOOL

tool_result
id: call_8d236141b1ac400fabc33d50
```
The file /mnt/d/code/frontend/dongfanghong/.sessions/2026-05-19-integration-testing/topic-index.md has been updated successfully.
```

> TOOL

tool_use TaskUpdate
id: call_906e19f440e04482a5acacf1
```json
{
  "status": "completed",
  "taskId": "1"
}
```

> TOOL

tool_result
id: call_906e19f440e04482a5acacf1
```
Updated task #1 status
```

> AGENT

对话 4 完成。汇总：

**旧系统可观测行为提取 — 9 个 agent 并行（3 批 × 3）**

- 从旧代码提取 **~236 条可观测行为**，其中 **~194 条保留**、**~33 条排除**、**~9 条需重新设计**
- 覆盖 10 个 feature 域：connection/receive/send/task/command-ingress/frame/storage/expression/display/settings
- **3 个旧页面在新系统缺失**：存储管理、历史分析、系统设置
- **SCOE 命令执行运行时链路**在 renderer 侧未找到完整实现，需在接缝审计中确认
- **11 项旧系统已知缺陷**标记为不复制到新系统
- 产出文件：`S004-legacy-observable-behaviors.md`（综合报告）+ 9 个 agent 详细文件

下一步：对话 5（新系统接缝审计）可独立并行执行。
