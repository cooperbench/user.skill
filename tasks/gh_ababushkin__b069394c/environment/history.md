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

> DEVELOPER

the only thing though is that we need to make sure the execution-model is selected during delivery-shaping (i.e. should this task be implemented using sonnet or opus? etc)

> AGENT

Good — that's the load-bearing constraint, and it changes the fix. Model routing is a *decision*, and you want that decision made (and visible) at shaping time, not deferred to pickup. Let me check what routing fields the node contract already carries before I recommend where this lives.

> TOOL

tool_use Read
id: toolu_01TVm33kqVRCK2ZjWCkjxyTp
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/docs/delivery-shape-contract.md",
  "offset": 84,
  "limit": 50
}
```

> TOOL

tool_result
id: toolu_01TVm33kqVRCK2ZjWCkjxyTp
```
84	
85	Every layer file opens with YAML front-matter. The load-bearing tags:
86	
87	```yaml
88	layer:        deliverable | node                   # which layer this file is
89	id:           D1 | N03                              # stable within the plan
90	type:         <node-type>                          # NODE FILES ONLY — the polymorphic node discriminator (see vocabulary); `capability` is one of these types
91	title:        <one line>
92	parent:       <relative path or id of enclosing layer>
93	serves_kr:    KR<n>                                # deliverable↔KR and node↔KR trace
94	maps_to:      <tracker-artefact class>             # milestone/issue/sub-issue class
95	skeleton:     true | (absent)                      # NODE-LEVEL: is this the walking-skeleton node?
96	acceptance:   true | (absent)                      # NODE-LEVEL: does this node verify its parent's cross-seam criterion?
97	external_window: <external constraint> | none      # see constraints — never effort-in-days
98	completion:
99	  form:       <completion-criterion form>          # the type-appropriate form (see vocabulary)
100	  criterion:  <the observable criterion, by form>
101	  verifies_parent: <parent-layer-id> | (absent)   # when acceptance: true — which parent's criterion this node closes
102	delegates_to: <rule or skill that owns this node type's discipline>   # REQUIRED on every node — fires at pickup, not at emission
103	```
104	
105	The five tags the contract is required to pin down:
106 […]

> AGENT

Here's the picture. The node frontmatter (contract lines 85–103) currently carries **no** `model_tier` field — routing only exists at the **task** level, in both `delivery` Step 7f and `exec:breakdown` Step 6. So your constraint ("the model is chosen during shaping") is real and currently *only* satisfied because `delivery` Step 7 does the full task expansion — the very thing that clashes with `exec:breakdown`.

That's the crux: **routing is the one piece of task detail you want front-loaded, but task enumeration is the thing the contract says decays.** They're coupled today because routing rides on the task list. To decouple them, routing has to attach to something stable.

The 5-axis rubric scores risk properties — reasoning complexity, spec completeness, hallucination sensitivity, stakes, orchestration role. Those are **stable properties of a unit of work**; they don't decay between shaping and pickup the way a specific `done_when` path does. So routing *can* be front-loaded safely — but it should attach to the **node** (the stable issue), not to tasks that don't exist yet at shape time.

## Recommended design

**At delivery-shape:** score each node on the 5-axis rubric and pin a node-level `model_tier` + `review_flag` in frontmatter. This is the "should this issue […]

> TOOL

tool_use AskUserQuestion
id: toolu_01SX7fCBkkwSdeXKSakCgn1D
```json
{
  "questions": [
    {
      "question": "At what granularity should the execution-model decision be made during delivery-shaping?",
      "header": "Routing granularity",
      "multiSelect": false,
      "options": [
        {
          "label": "Node-level at shape, refine at pickup",
          "description": "Delivery scores each node (issue) on the 5-axis rubric → node-level model_tier + review_flag in frontmatter. exec:breakdown enumerates tasks at pickup, each inheriting the node tier and overriding only on genuine divergence. Honors the decay principle; no clash; delivery stops at node+AC.",
          "preview": "# N02-search-endpoint.md frontmatter\nlayer: node\ntype: story\nmodel_tier: Frontier   # <- decided at shape\nreview_flag: elevated\ncompletion:\n  form: acceptance-criteria\n  criterion: \"- **Done when:** results ranked by score\"\n\n# at pickup, exec:breakdown:\n#   T1 inherits Frontier\n#   T2 (trivial cleanup) overrides -> Balanced"
        },
        {
          "label": "Full per-task routing at shape",
          "description": "Delivery produces the complete routed task list (per-task model_tier). exec:breakdown ingests/validates delivery's tasks for delivery-sourced issues, only producing fresh ones for ad-hoc tickets. Literal per-task tiers up front, but front-loads detail the contract says decays, and makes the delivery plan the task source of truth.",
          "preview": "# N02-search-endpoint.md (delivery emits full tasks)\n- [ ] `skeleton` wire /search endpoint\n      Done when: GET /search 200s\n      Model: Frontier\n- [ ] rank results by score\n      Done when: top hit = highest […]

> TOOL

tool_result
id: toolu_01SX7fCBkkwSdeXKSakCgn1D
```
Your questions have been answered: "At what granularity should the execution-model decision be made during delivery-shaping?"="Node-level at shape, refine at pickup" selected preview:
# N02-search-endpoint.md frontmatter
layer: node
type: story
model_tier: Frontier   # <- decided at shape
review_flag: elevated
completion:
  form: acceptance-criteria
  criterion: "- **Done when:** results ranked by score"

# at pickup, exec:breakdown:
#   T1 inherits Frontier
#   T2 (trivial cleanup) overrides -> Balanced. You can now continue with these answers in mind.
```

> AGENT

Node-level it is. Before I write the edits, I need to see what enforces the frontmatter and what the worked example looks like, so the new `model_tier` field passes the gates rather than breaking them.

> TOOL

tool_use Bash
id: toolu_01A51vvAWPdLswEehXbe3w1J
```json
{
  "command": "cd /home/<USER>/src/agent-skills-shaper\necho \"=== bin/ scripts ===\"; ls bin/\necho; echo \"=== example node files ===\"; find examples/delivery-plans -name 'N*.md' | head -5\necho; echo \"=== does check-plan-framing validate frontmatter keys? ===\"\ngrep -niE 'model_tier|frontmatter|front-matter|delegates_to|model:|review_flag|allowed|required' bin/check-plan-framing bin/walk-delivery-plan | head -40",
  "description": "Inspect bin scripts and example nodes"
}
```

> TOOL

tool_result
id: toolu_01A51vvAWPdLswEehXbe3w1J
```
=== bin/ scripts ===
check-plan-framing  21.7K
eval-triggers  4.2K
grade-execution-review  6.9K
walk-delivery-plan  15.0K

=== example node files ===
examples/delivery-plans/_tests/rule-a1-branch/D2-reuse-card-at-checkout/N03-prefill-saved-card.md
examples/delivery-plans/_tests/rule-a1-branch/D1-tokenized-card-vault/N01-card-vault-design-doc.md
examples/delivery-plans/_tests/rule-a1-branch/D1-tokenized-card-vault/N02-store-and-replay-token.md

=== does check-plan-framing validate frontmatter keys? ===
bin/walk-delivery-plan:8:front-matter, never authored.
bin/walk-delivery-plan:12:front-matter the contract pins down is a small fixed set of keys, and a targeted
bin/walk-delivery-plan:14:than pulling in a parser. If a plan's front-matter ever outgrows this reader,
bin/walk-delivery-plan:23:    in README is required.
bin/walk-delivery-plan:25:    small-scale delivery-shape path. No manifest oracle is required; the
bin/walk-delivery-plan:51:# Required front-matter keys per layer. A file missing any of these is
bin/walk-delivery-plan:53:REQUIRED = {
bin/walk-delivery-plan:63:# --- front-matter reader -----------------------------------------------------
bin/walk-delivery-plan:72:    """Extract the contract's front-matter keys from a layer file.
bin/walk-delivery-plan:85:        raise PlanError(f"{path}: missing opening '---' front-matter fence")
bin/walk-delivery-plan:89:        raise PlanError(f"{path}: front-matter fence not closed with '---'")
bin/walk-delivery-plan:116:    missing = [k for k in REQUIRED[layer] if k not in fm]
bin/walk-delivery-plan:118:        raise PlanError(f"{path}: {layer} missing required front-matter {missing}")
bin/walk-delivery-plan:156:    the README is not required to carry a hand-count manifest table.
bin/walk-delivery-plan:171:            raise PlanError(f"{nfile}: lite node missing required front-matter {missing}")
bin/walk-delivery-plan:337:    # tier (flat N*.md files at root, no manifest oracle required).
bin/check-plan-framing:19:     the heading is required on all of them).
bin/check-plan-framing:38:     a `Model:` annotation somewhere in the task text. This ensures each […]

> AGENT

This is the real crux — and it's bigger than the prose. `bin/check-plan-framing` **enforces** per-task `Model:` annotations and a skeleton task on every "executable node" (lines 38, 72, 342–379), with an exemption only for "lite nodes." So the shipped enforcement *requires* `delivery` to emit fully-expanded, Model-annotated tasks today — that enforcement, not just Step 7 prose, is what creates the clash with `exec:breakdown`.

Let me read the lite-node logic and one example node so my plan accounts for the gate, not just the docs.

> TOOL

tool_use Bash
id: toolu_01K1DStUNJpKGb1PxpCPGiQn
```json
{
  "command": "cd /home/<USER>/src/agent-skills-shaper\necho \"=== check-plan-framing: lite-node + model enforcement region ===\"\nsed -n '40,75p;360,400p' bin/check-plan-framing\necho \"=== walk REQUIRED keys ===\"\nsed -n '51,62p;160,175p' bin/walk-delivery-plan",
  "description": "Read lite-node and model enforcement logic"
}
```

> TOOL

tool_result
id: toolu_01K1DStUNJpKGb1PxpCPGiQn
```
=== check-plan-framing: lite-node + model enforcement region ===
     execute it, preventing ambiguous task assignment.

  5. Non-goals well-formed when present — `## Non-goals` is an optional section.
     When present its body must carry at least one list item; a node with the
     heading but an empty section fails.

Two tier shapes are accepted:

  - **Full tier** — root contains `D<n>-*/` deliverable directories with
     `N<nn>-*.md` nodes inside (the original schema). The skeleton mandate
     applies whenever any executable node (`story`, `refactor`, `capability`,
     `migration`, `experiment`) carries tasks.
  - **Lite tier** — root contains `N<nn>-*.md` files directly with no `D*`
     deliverable directories. Used by `delivery-shape` for single-outcome work.
     Skeleton, tasks, and Model annotations are not required when the lite
     plan carries no tasks at all (the small-scale path has no task layer);
     the five-section body, assumption tags, and Non-goals lint still apply.

Like the walk-script, this reader is deliberately dependency-free (stdlib only,
no YAML library): it needs just two front-matter keys (`layer`, `type`), a
heading scan, and the walk-script's task-line *regex* (`TASK_RE`) — so a
targeted reader is more boring, and more honest about what it relies on, than
pulling in a parser. Headings and list items inside fenced code blocks […]

> AGENT

Good news: the enforcement already supports this cleanly. Two facts from the scripts make the change much smaller than the contract prose suggested:

1. **Per-task `Model:` enforcement is conditional** — `nodes_missing_model = [...] if total_tasks > 0 else []`. The skeleton/Model gates only fire *when a node carries tasks*.
2. **A taskless node is already a first-class, gated shape** — the "lite tier … no task layer" path is explicitly *"Used by `delivery-shape` for single-outcome work"*; five-section body + assumption tags + non-goals still apply, but skeleton/tasks/Model do not.

So the infrastructure already permits "delivery emits a node with **no** task list." What's missing is only the routing field. That resolves the design: **delivery emits node + AC + node-level routing and stops; `exec:breakdown` is the sole producer of the task layer.** This satisfies both your goals — no clash (goal 1 *requires* delivery not emit tasks, since that's exec:breakdown's output) and model chosen at shape (goal 2, now a node-level field).

## Implementation plan

**1. `docs/delivery-shape-contract.md`**
- Add `model_tier:` + `review_flag:` to node frontmatter (after `delegates_to`), scored by the 5-axis rubric **at shape time** — the deliberate exception to "delegation fires at pickup," justified because risk scores are stable […]