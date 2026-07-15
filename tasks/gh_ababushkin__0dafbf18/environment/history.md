> DEVELOPER

are there any instructions in skills/delivery that overlap with skills/exec:breakdown ?

> AGENT

I'll compare the two skill files. Let me locate and read them.

> TOOL

tool_use Bash
id: toolu_01XAWgGxvppNyCaTdQGZiJyn
```json
{
  "command": "ls skills/ | grep -iE 'deliver|breakdown|exec'",
  "description": "List delivery and exec skill dirs"
}
```

> TOOL

tool_result
id: toolu_01XAWgGxvppNyCaTdQGZiJyn
```
delivery/
exec-breakdown/
exec-build/
exec-debug/
exec-finish/
exec-pickup/
exec-review/
exec-simplify/
exec-verify/
```

> TOOL

tool_use Read
id: toolu_01VgRAXdr6xN7Dncb1hHfAoD
```json
{
  "file_path": "/Users/anton/src/agent-skills-shaper/skills/delivery/SKILL.md"
}
```

> TOOL

tool_result
id: toolu_01VgRAXdr6xN7Dncb1hHfAoD
```
1	---
2	name: delivery
3	description: 'Decompose committed work into a verifiable delivery hierarchy. Trigger phrases: "plan this project", "breakdown the design into tasks", "plan this initiative"'
4	---
5	
6	# Delivery shape
7	
8	## Purpose
9	
10	Take committed work and create a delivery plan that's easy for humans to review and for agents to action.
11	
12	The input may be an initiative, a single task, or an accepted design doc. The hierarchy has three layers: deliverables, nodes, and tasks. Deliverables serve a stated outcome source. Nodes are typed units of work such as stories, spikes, ADRs, experiments, design docs, or KTLO work. Tasks are the verifiable checklist inside a node.
13	
14	## When to use
15	
16	- Committed work exists and the desired outcome is known.
17	- You need a deliverable → node → task hierarchy before build pickup.
18	- You want traceability from each deliverable back to the relevant outcome source.
19	- You are shaping work from one of these sources:
20	  - an initiative with a goal and KRs
21	  - a single task with acceptance criteria or a clear desired outcome
22 […]

> TOOL

tool_use Read
id: toolu_01NaFricLDmXkvT79cMF6JUu
```json
{
  "file_path": "/Users/anton/src/agent-skills-shaper/skills/exec-breakdown/SKILL.md"
}
```

> TOOL

tool_result
id: toolu_01NaFricLDmXkvT79cMF6JUu
```
1	---
2	name: exec:breakdown
3	description: >
4	  Break a picked-up Linear issue into an ordered task list where every task carries one
5	  verifiable `done_when` clause, a model-tier annotation, and a 5-axis routing score.
6	  Use immediately after `exec:pickup` and before `exec:build`. Trigger phrases:
7	  "break this issue down", "task breakdown", "exec:breakdown", "size and route the tasks",
8	  "turn this AC into tasks".
9	---
10	
11	# Exec: breakdown
12	
13	## Purpose
14	
15	Turn the picked-up issue's body and acceptance criteria into the ordered task list that `exec:build` will drain. The one thing that must hold: every task carries a single verifiable `done_when` clause, scored on the 5-axis routing rubric, traceable back to at least one AC item. A task without `done_when` cannot turn RED; a task that bundles two criteria is two tasks pretending to be one.
16	
17	This skill reads the `pickup` section of `exec-state.json` and writes a `breakdown` section back to the same file. It re-types nothing — the AC checklist is the source of truth, copied verbatim into each task's `ac_refs`.
18	
19	## When to use
20	
21	- Immediately after `exec:pickup` has written the […]

> AGENT

Yes — there's substantial overlap. Both skills decompose committed work into verifiable, routed tasks, and they share several of the same mechanics nearly verbatim. Here's the breakdown:

## Overlapping instructions

| Concern | `delivery` | `exec:breakdown` | Same instruction? |
|---|---|---|---|
| **AC/outcome → task coverage gate** | Step 2/3: every deliverable serves exactly one outcome item; every outcome item served by ≥1 deliverable | Step 2: every AC item maps to ≥1 task; every task serves ≥1 AC item | **Yes** — identical bidirectional-coverage rule, one level down |
| **`Done when:` / `done_when` clause** | Step 7c/7d: one verifiable `Done when:` per task; split if it won't fit one sentence | Step 3: exactly one `done_when` per task; split if a sentence can't capture it | **Yes** — same rule, near-identical wording |
| **Observable result, not procedure** | 7c: "describe a verifiable result, not the work performed" | 3: "observable, not procedural" with the same `implement the parser` style example | **Yes** |
| **One concern per task / no bundling** | 7d: split tasks carrying multiple concerns | 3: "two clauses joined by 'and' is a hidden multi-task" | **Yes** |
| **Choose the first task […]