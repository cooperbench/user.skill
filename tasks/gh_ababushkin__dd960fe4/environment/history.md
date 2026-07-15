> DEVELOPER

are there any instructions in skills/delivery that overlap with skills/exec:breakdown ?

> AGENT

I'll compare the two skill files. Let me locate and read them.

> AGENT

Yes — there's substantial overlap. Both skills decompose committed work into verifiable, routed tasks, and they share several of the same mechanics nearly verbatim. Here's the breakdown: ## Overlapping instructions | Concern | `delivery` | `exec:breakdown` | Same instruction? | |---|---|---|---| | **AC/outcome → task coverage gate** | Step 2/3: every deliverable serves exactly one outcome item; every outcome item served by ≥1 deliverable | Step 2: every AC item maps to ≥1 task; every task serves ≥1 AC item | **Yes** — identical bidirectional-coverage rule, one level down | | **`Done when:` / `done_when` clause** | Step 7c/7d: one verifiable `Done when:` per task; split if it won't fit one sentence | Step 3: exactly one `done_when` per task; split if a sentence can't capture it | **Yes** — same rule, near-identical wording | | **Observable result, not procedure** | 7c: "describe a verifiable result, not the work performed" | 3: "observable, not procedural" with the same `implement the parser` style example | **Yes** | | **One concern per task / no bundling** | 7d: split tasks carrying multiple concerns | 3: "two clauses joined by 'and' is a hidden multi-task" | **Yes** | | **Choose the first task […]

> DEVELOPER

i just want to make sure that delivery-shape doesn't produce anything that exec-breakdown would produce so that it doesn't cause a clash and confuse the agent implementing the task

> AGENT

Good — that's the right question to nail down. The two *artifacts* live in different files (Markdown node files vs. `exec-state.json`), but the *content* overlaps (both emit tasks with `done_when` + `Model:`), and `exec:breakdown` already has a guard implying it knows about the collision. Let me check how the artifacts actually flow into `exec:build` to see whether a real clash exists.

> AGENT

Now I can see the actual execution pipeline. Let me check one thing — whether `delivery`'s node tasks are meant to be the authoritative execution list or just a planning aid, since that determines whether the clash is real.

> AGENT

Lines 182 and 265–273 look decisive. Let me read them.

> AGENT

I have the decisive answer now. The pipeline and the contract resolve your question — but they also reveal that `delivery`'s SKILL.md currently **violates** the resolution, which is exactly the clash you're worried about. ## The intended design: no clash The contract is explicit about who owns the task layer. From `docs/delivery-shape-contract.md` §"Delegation — timing & surfacing" (lines 265–270): > `delegates_to` names the discipline that owns a node, but it fires **at issue-pickup (build time), not during plan emission.** `delivery-shape` emits the hierarchy and stops; the delegate (e.g. `execution-breakdown` for a `story`) runs when the issue-class artefact is picked up… expanding every node's fine-grained tasks at plan time front-loads detail that decays before the node is reached. And the story-node row (line 182): a `story`'s `## Completion` section holds a `- **Done when:**` list, and the "At-pickup task breakdown (per node type)" is **delegated**, not emitted. So by contract, the division is clean and there is **no clash**: | | Produces | Layer | |---|---|---| | `delivery` | deliverable → node hierarchy; `story` node carries `Done when:` **acceptance criteria** | stops at the node/AC layer | | `exec:breakdown` | ordered `tasks[]` with `done_when` + routing, derived **from** those AC items […]

> DEVELOPER

the only thing though is that we need to make sure the execution-model is selected during delivery-shaping (i.e. should this task be implemented using sonnet or opus? etc)

> AGENT

Good — that's the load-bearing constraint, and it changes the fix. Model routing is a *decision*, and you want that decision made (and visible) at shaping time, not deferred to pickup. Let me check what routing fields the node contract already carries before I recommend where this lives.

> AGENT

Here's the picture. The node frontmatter (contract lines 85–103) currently carries **no** `model_tier` field — routing only exists at the **task** level, in both `delivery` Step 7f and `exec:breakdown` Step 6. So your constraint ("the model is chosen during shaping") is real and currently *only* satisfied because `delivery` Step 7 does the full task expansion — the very thing that clashes with `exec:breakdown`. That's the crux: **routing is the one piece of task detail you want front-loaded, but task enumeration is the thing the contract says decays.** They're coupled today because routing rides on the task list. To decouple them, routing has to attach to something stable. The 5-axis rubric scores risk properties — reasoning complexity, spec completeness, hallucination sensitivity, stakes, orchestration role. Those are **stable properties of a unit of work**; they don't decay between shaping and pickup the way a specific `done_when` path does. So routing *can* be front-loaded safely — but it should attach to the **node** (the stable issue), not to tasks that don't exist yet at shape time. ## Recommended design **At delivery-shape:** score each node on the 5-axis rubric and pin a node-level `model_tier` + `review_flag` in frontmatter. This is the "should this issue […]

> AGENT

Node-level it is. Before I write the edits, I need to see what enforces the frontmatter and what the worked example looks like, so the new `model_tier` field passes the gates rather than breaking them.

> AGENT

This is the real crux — and it's bigger than the prose. `bin/check-plan-framing` **enforces** per-task `Model:` annotations and a skeleton task on every "executable node" (lines 38, 72, 342–379), with an exemption only for "lite nodes." So the shipped enforcement *requires* `delivery` to emit fully-expanded, Model-annotated tasks today — that enforcement, not just Step 7 prose, is what creates the clash with `exec:breakdown`. Let me read the lite-node logic and one example node so my plan accounts for the gate, not just the docs.

> AGENT

Good news: the enforcement already supports this cleanly. Two facts from the scripts make the change much smaller than the contract prose suggested: 1. **Per-task `Model:` enforcement is conditional** — `nodes_missing_model = [...] if total_tasks > 0 else []`. The skeleton/Model gates only fire *when a node carries tasks*. 2. **A taskless node is already a first-class, gated shape** — the "lite tier … no task layer" path is explicitly *"Used by `delivery-shape` for single-outcome work"*; five-section body + assumption tags + non-goals still apply, but skeleton/tasks/Model do not. So the infrastructure already permits "delivery emits a node with **no** task list." What's missing is only the routing field. That resolves the design: **delivery emits node + AC + node-level routing and stops; `exec:breakdown` is the sole producer of the task layer.** This satisfies both your goals — no clash (goal 1 *requires* delivery not emit tasks, since that's exec:breakdown's output) and model chosen at shape (goal 2, now a node-level field). ## Implementation plan **1. `docs/delivery-shape-contract.md`** - Add `model_tier:` + `review_flag:` to node frontmatter (after `delegates_to`), scored by the 5-axis rubric **at shape time** — the deliberate exception to "delegation fires at pickup," justified because risk scores are stable […]