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