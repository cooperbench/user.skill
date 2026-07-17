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
  "file_path": "/home/<USER>/src/agent-skills-shaper/skills/delivery/SKILL.md"
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
  "file_path": "/home/<USER>/src/agent-skills-shaper/skills/exec-breakdown/SKILL.md"
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

> DEVELOPER

i just want to make sure that delivery-shape doesn't produce anything that exec-breakdown would produce so that it doesn't cause a clash and confuse the agent implementing the task

> AGENT

Good — that's the right question to nail down. The two *artifacts* live in different files (Markdown node files vs. `exec-state.json`), but the *content* overlaps (both emit tasks with `done_when` + `Model:`), and `exec:breakdown` already has a guard implying it knows about the collision. Let me check how the artifacts actually flow into `exec:build` to see whether a real clash exists.

> TOOL

tool_use Read
id: toolu_019L6u17aGvNSPUoqGKR4iXC
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/skills/exec-build/SKILL.md"
}
```

> TOOL

tool_use Read
id: toolu_01CHFR7NSUCAVgAScLWH6Tek
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/skills/exec-pickup/SKILL.md"
}
```

> TOOL

tool_result
id: toolu_019L6u17aGvNSPUoqGKR4iXC
```
1	---
2	name: exec:build
3	description: >
4	  Gated RED/GREEN/commit loop for a single broken-down task. Use when picking up any
5	  build task from a delivery plan or issue — whether the repo has a test runner or only
6	  a deterministic verification script. Every increment lands verified, smallest-first, with
7	  a commit trail a reviewer can replay. Trigger phrases: "build this task", "implement this
8	  story", "work on this issue", "pick up this task", "start building", "implement the slice".
9	---
10	
11	# Build
12	
13	## Purpose
14	
15	The gated implementation loop for a single task: a failing check before any code, the minimal change that clears it, then a commit — repeated per slice. The one thing that must hold: no cycle starts without a failing check first. A cycle with no RED is implementation with no proof; three consecutive reds without a named blocker is the signal to escalate to `exec:debug`.
16	
17	## When to use
18	
19	- Picking up any build task from a delivery plan, issue, or node task list.
20	- Implementing a story, feature slice, bug fix, or any change with an […]

> TOOL

tool_result
id: toolu_01CHFR7NSUCAVgAScLWH6Tek
```
1	---
2	name: exec:pickup
3	description: >
4	  Front door for draining a Linear issue end-to-end — pickup through breakdown,
5	  build, review, verify, and PR finishing. Every step is a named delegation to its
6	  owning skill; this is the supervisor pointer, not the procedure. Use when a
7	  drain-cycle worker or supervisor prompt picks up a Linear issue and needs a single
8	  entry point for the full execution workflow. Trigger phrases: "pick up this issue",
9	  "start working on this ticket", "drain this issue", "exec:pickup", "work on ABA-NNN".
10	---
11	
12	# Exec: pickup
13	
14	## Purpose
15	
16	Take a freshly-picked Linear issue all the way to a finished PR with a full review trail. This skill reads the issue, writes the `pickup` section of `exec-state.json`, and then delegates each step — breakdown, build, review, verify, finish — to its owning `exec:*` skill by name. It inlines no procedure; the named delegation is the whole of each step. The issue's acceptance criteria travel inside `exec-state.json` (pickup section) from pickup to the spec-compliance persona in `exec:review`, re-typed by no one and lost by no one.
17	
18	## When to […]

> AGENT

Now I can see the actual execution pipeline. Let me check one thing — whether `delivery`'s node tasks are meant to be the authoritative execution list or just a planning aid, since that determines whether the clash is real.

> TOOL

tool_use Bash
id: toolu_016hmB1G9ZahbmbLY5uUcxR8
```json
{
  "command": "sed -n '1,80p' docs/delivery-shape-contract.md 2>/dev/null | grep -niE 'task|tasks:|exec|breakdown|node body|checklist' ",
  "description": "Search contract for task/exec semantics"
}
```

> TOOL

tool_result
id: toolu_016hmB1G9ZahbmbLY5uUcxR8
```
4:committed initiative into an ordered, verifiable delivery hierarchy — deliverable → node → task —
24:| **Task** | a `- [ ]` / `- [x]` line inside a node | sub-issue-class | the checkbox + its description |
56:  (read top-down starts at the outcome, not at task 1), the rendered tree, and the **hand-count
```

> TOOL

tool_use Bash
id: toolu_017zKsHWLzExsm5YR9MZ2qv5
```json
{
  "command": "grep -niE 'tasks:|exec:breakdown|exec-breakdown|execution|build pickup|pickup|done_when|done when|re-derive|sub-issue|maps_to' docs/delivery-shape-contract.md",
  "description": "Search contract for exec/task handoff semantics"
}
```

> TOOL

tool_result
id: toolu_017zKsHWLzExsm5YR9MZ2qv5
```
13:> sub-issue-class). Binding those classes to a concrete tracker is the **adapter's** job and lives
24:| **Task** | a `- [ ]` / `- [x]` line inside a node | sub-issue-class | the checkbox + its description |
78:The **manifest is derived, never authored**: a walk-script reconstructs milestone/issue/sub-issue
94:maps_to:      <tracker-artefact class>             # milestone/issue/sub-issue class
102:delegates_to: <rule or skill that owns this node type's discipline>   # REQUIRED on every node — fires at pickup, not at emission
131:   parent's "Done when" is irreducible to ∀child.done** — a KR moving, a journey crossing child
143:Task lines are the sub-issue layer. A task is `- [ ] ` or `- [x] `; an optional leading code-span
160:| **Assumptions** | List items (`- …`), each tagged `(verified)` or `(to-verify)`. Empty section (`*(none)*`) is valid. | `bin/check-plan-framing` enforces the tag on every list item. `(to-verify)` items block pickup. |
182:| `story` | acceptance criteria, in a grounded story form | `- **Done when:** <verifiable state>` list (≥1 item) | At-pickup task breakdown (per node type) | `N02`, `N04`, `N05`, `N06`, `N08` |
219:| `capability` | `the-capability-spec` | At-pickup task breakdown (slice the capability spec into tasks) | a capability carries a […]

> AGENT

Lines 182 and 265–273 look decisive. Let me read them.

> TOOL

tool_use Read
id: toolu_01CWZPAM1dgPenmWotR1JpoP
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/docs/delivery-shape-contract.md",
  "offset": 140,
  "limit": 135
}
```

> TOOL

tool_result
id: toolu_01CWZPAM1dgPenmWotR1JpoP
```
140	   with aggregate verification passing — no special field or tooling required. See `N07` for the
141	   worked example.
142	
143	Task lines are the sub-issue layer. A task is `- [ ] ` or `- [x] `; an optional leading code-span
144	flags it. `` `skeleton` `` marks the walking-skeleton/foundational task; `` `acceptance` `` marks
145	the aggregate-verification task (flag 5 above). Examples:
146	`` - [ ] `skeleton` — walk the tree, read front-matter, print counts (toolchain folded in) ``.
147	`` - [ ] `acceptance` — evaluate aggregate result; write finding (confirmed / falsified) ``.
148	
149	### Five body sections
150	
151	Every node body carries exactly **five sections** in addition to its front-matter, regardless of
152	`type`. `delivery-shape` emits all five by default; `bin/check-plan-framing` enforces their
153	presence (exits 1 if any heading is absent):
154	
155	| Section | Content | Discipline rule |
156	|---------|---------|-----------------|
157	| **What** | For `story`: the grounded Cohn form ("As <role>, I want…, so that…") as the first sentence. For other types: what the node investigates, decides, or maintains. | The Cohn story line is re-housed here, not deleted. |
158	| **Why** […]

> AGENT

I have the decisive answer now. The pipeline and the contract resolve your question — but they also reveal that `delivery`'s SKILL.md currently **violates** the resolution, which is exactly the clash you're worried about.

## The intended design: no clash

The contract is explicit about who owns the task layer. From `docs/delivery-shape-contract.md` §"Delegation — timing & surfacing" (lines 265–270):

> `delegates_to` names the discipline that owns a node, but it fires **at issue-pickup (build time), not during plan emission.** `delivery-shape` emits the hierarchy and stops; the delegate (e.g. `execution-breakdown` for a `story`) runs when the issue-class artefact is picked up… expanding every node's fine-grained tasks at plan time front-loads detail that decays before the node is reached.

And the story-node row (line 182): a `story`'s `## Completion` section holds a `- **Done when:**` list, and the "At-pickup task breakdown (per node type)" is **delegated**, not emitted.

So by contract, the division is clean and there is **no clash**:

| | Produces | Layer |
|---|---|---|
| `delivery` | deliverable → node hierarchy; `story` node carries `Done when:` **acceptance criteria** | stops at the node/AC layer |
| `exec:breakdown` | ordered `tasks[]` with `done_when` + routing, derived **from** those AC items […]