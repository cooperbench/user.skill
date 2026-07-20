> DEVELOPER

.sessions/2026-05-21-missing-pages/H001-conversation-prompts.md 对话D

> TOOL

tool_use Read
id: call_05c503a055b6435abe89e3da
```json
{
  "file_path": "/mnt/d/code/frontend/dongfanghong/.sessions/2026-05-21-missing-pages/H001-conversation-prompts.md"
}
```

> TOOL

tool_result
id: call_05c503a055b6435abe89e3da
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

文件已读取。以下是**对话 D**的完整提示词（第 118-133 行）：

---

## 对话 D：存储管理 — feature 设计

```
Lane B/C | 存储管理高速存储 feature 设计（只设计不实施）

先读 .sessions/2026-05-21-missing-pages/S001-research-and-planning.md §存储管理补充 + §对话 D
再读 .sessions/2026-05-21-missing-pages/topic-index.md

目标：设计高速存储三层架构 — 规则模型 + 分流机制 + Platform 文件流。产出设计文档 + checklist，不写代码

直接合同：S001 §存储管理关键发现 + §存储管理补充
边界护栏：R5 + R6 + CLAUDE.md main 不承载业务逻辑

按 H001 §通用流程指令执行（Phase 1-2，不进 Phase 3 实施设计文档 + checklist 产出 + 自检通过即可。
Wave 1 按 S001 §对话 D 派 9 agent。
```

---

**对话 D 关键信息：**
- **Lane**: B/C（需要设计闭环，可能跨模块）
- **只设计不实施** — 产出设计文档 + checklist 即可
- **目标**: 高速存储三层架构（规则模型 + 分流机制 + Platform 文件流）
- **Wave 1**: 需派 9 agent 收集事实
- **直接合同**: S001 的存储管理关键发现和补充
- **边界护栏**: R5 + R6 + main 不承载业务逻辑

要现在开始执行对话 D 吗？