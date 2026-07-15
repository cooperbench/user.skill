> DEVELOPER

hey man so I need you to find the diff report, the most latest one. It sbould be in the plans folder on dev-sprint. Make sure you do a pull first

> AGENT

The latest diff report on `dev_sprint` is:

**`docs/plans/reports/design-implementation-diff-consolidated-report.md`**

Last updated today (2026-05-11) in commit `6ed0e68`. It's the consolidated design-vs-implementation diff report covering all feature-set folders (FS1–FS12), plus database, definitions, orchestration, LLM management, testing, and UI.

Want me to pull the full contents so you can read it here, or are you looking for something more specific within it?

> DEVELOPER

Are you sure there is no other oneit shoul dbe in the audit folder?

> AGENT

The most recent dated one in the audits folder is:

**`docs/plans/audits/dev-sprint-to-dev-capability-diff-2026-05-08.md`**

There's also the related **`dev-sprint-to-dev-capability-diff-top-level-gates-2026-05-08.md`** from the same date.

Want me to pull one of those up?

> DEVELOPER

So basically o am in in charge of porting features from dev-spront to dev. Apparently there is a list of features somewheere. I remember him saying that there is also the design vs impletionatio diff stuff but I really don't know how it all ties together

> AGENT

Let me pull up the key docs so I can explain how they connect.

> AGENT

OK, now I've got the full picture. Here's how it all ties together:

---

### The porting workflow: how the docs connect

There are **two layers** of docs serving different purposes:

**1. The Capability Diff (your port checklist)**
`docs/plans/audits/dev-sprint-to-dev-capability-diff-2026-05-08.md`

This is your primary working document. It has:
- A **Capability Matrix** — each row is a portworthy feature (DB storage, FS10 validation, FS11 QC, FS2 retrieval, etc.)
- **Readiness** ratings (`Near`, `Not-ready`)
- **Pre-port work** — what needs to happen before each slice can land
- **Recommended Port Order** — a numbered list (1–10) of the sequence to port things in

Think of this as **"what to port, in what order, and what's blocking each piece."**

**2. The Design-vs-Implementation Diffs (per-feature-set gap reports)**
`docs/plans/reports/design-implementation-diff-consolidated-report.md` plus individual `docs/plans/FS<N>/fs<N>-design-implementation-diff.md` files

These tell you **"for each feature set, what does the design say it should do vs. what the code actually does today."** They're useful context when you're porting a specific feature — they flag drift, missing pieces, and things that exist in code but aren't in the design (or vice versa).

---

### How they work together in practice

1. Look at the **Capability Diff** to pick your next port slice (following the recommended order)
2. Before porting that slice, check the relevant **FS design-implementation diff** to understand what gaps exist and what the design expects
3. Port the code, verify with the pre-push checks, open a PR to `dev`

You've already done a few of these — the recent commits on your current branch (`port/document-storage-authority`) and PRs #172–#174 are early items from that port order.

Want me to check where you're at in the port order based on what's already landed on `dev`?

> DEVELOPER

yeah show me where we're at in the port order. also he said ther are differnt statuses like mplemented not tested, done not verified.

> AGENT

Now let me check the individual design-implementation diffs for the status vocabulary.

> AGENT

OK here's the full picture. The status system uses **three dimensions** per capability row:

### The three status columns

| Column | What it means | Values you'll see |
|---|---|---|
| **Readiness** | Can this be ported right now? | `Ready`, `Near`, `Not-ready` |
| **Port gate** | Has it actually been ported and verified? | `[x]` (done) or `[ ]` (not yet) |
| **Test evidence** | Were the required tests actually run? | Free-text — says exactly which tests passed and which "were not rerun" |

So the statuses Patrick mentioned map to something like:
- **"Implemented, not tested"** = `Readiness: Near` + tests listed but "not rerun on clean port branch"
- **"Done, not verified"** = `Port gate: [ ]` even though readiness might be `Near` or `Ready` — the targeted tests haven't been rerun on `dev`

### Where you are in the port order

Based on what's landed on `dev` (PRs #167–#174), here's the scorecard:

| # | Port slice | Status on dev |
|---|---|---|
| 1 | **Base storage & migrations** | **Landed** — PR #167 (schema/models/migrations), #169 (stores/repos/contracts) |
| 2 | **Prompt/LLM infrastructure** | **Landed** — PR #168 (LLM tiers/config/FS11 QC module), #170 (task_id routing), #172 (render bundle/fit store), #173 (prompt extraction), #174 (prompt trace persistence) |
| 3 | **`P-E2E-GRAPH-01` live graph gate repair** | The only `[x]` port gate in the report — **not yet on dev** |
| 4 | **Document storage authority** | **In progress** — your current branch `port/document-storage-authority` (PR #175 / commit `7fb968e`) |
| 5 | **FS11 QC infrastructure** | `[ ]` not ported |
| 6 | **FS10 validation lifecycle** | `[ ]` not ported |
| 7 | **FS2 runtime/Research Defensibility** | `[ ]` not ported |
| 8 | **FS3 extraction/graph admission** | `[ ]` not ported |
| 9 | **FS4 estimator/training** | `[ ]` not ported |
| 10 | **FS5–FS7 downstream** | `[ ]` not ported |
| 11 | **API/worker** | `[ ]` not ported |
| 12 | **Ops/deployment** | `Not-ready` |
| 13 | **Fixtures/scratch** | `Not-ready` |

**You're roughly through steps 1–2 of the port order**, with step 4 (document storage) in flight and step 3 (the graph gate repair) still pending.

> DEVELOPER

no but i literally saw mplemented as a word in the statuses, do yo not see that?

> AGENT

Let me search more carefully for that exact vocabulary.

> AGENT

Found it. Let me check the diagram-code-map files — those have the `implementation_status` field with the specific values.

> AGENT

Hmm, those only have `implemented` and `planned`. Let me look more broadly — maybe it's in the consolidated diff report or somewhere else with a table of statuses.

> AGENT

There it is. The status vocabulary is in **`docs/plans/FS10/fs-capability-test-coverage.md`**. There are two sets:

### Coverage status
| Status | Meaning |
|---|---|
| `covered` | Has named gates, scoring view, and enough shape to be runnable once prerequisites are met |
| `partial` | Has gates and scoring view, but some behavior/threshold/implementation is incomplete |
| `deferred` | Intentionally out of scope (must state `Reason:`) |
| `gap` | Missing a sufficient gate, scoring view, or package — needs an owner and follow-up |

### Blocking status
| Status | Meaning |
|---|---|
| `blocking` | Part of the core acceptance path |
| `blocking rollout` | Outside the core FS1–FS7 ladder, but blocks full rollout for its feature set |

And separately in the **diagram-code-map TOML files**, each node has:
- `implementation_status = "implemented"` — code exists on dev_sprint
- `implementation_status = "planned"` — designed but not yet coded

So when Patrick said "implemented not tested" — that's a node marked `implemented` in the code-map but whose capability row is `partial` or has `[ ]` in the port gate (tests not rerun on a clean branch). "Done not verified" is the same idea — the code is there but the targeted test batch hasn't been rerun to earn the `[x]`.

> DEVELOPER

no that's not it. I saw his screena dn it said implemented not tested or not verified for example do you see nohting with that in the reports/ did you pull ?

> AGENT

Let me fetch again and look more carefully at what's actually on dev_sprint right now, especially recent additions.

> AGENT

Found it. It's in **`AGENTS.md`** and **`agent_rules/README.md`**. Let me get the full status vocabulary from there.

> AGENT

That's it. Here are the statuses — from `AGENTS.md` line 196:

| Status | Meaning |
|---|---|
| `pending` | Run record exists but work hasn't started |
| `in_progress` | Actively being worked |
| `blocked` | Cannot proceed without a specific resolution |
| `implemented` | Code or docs exist, but **verification is incomplete** |
| `verified` | Acceptance criteria met and all required gates passed |
| `superseded` | Source plans changed enough that a new run record should own it |
| `deferred` | Intentionally moved out of current scope |

And the key rule Patrick set:

> A run with passing unit tests but missing process, integration, or performance evidence remains `implemented`, **not** `verified`. Never mark a run `verified` without evidence for every required gate.

So that's what you saw — `implemented` means "the code is there but it hasn't been fully tested/verified against all the gates yet."

> DEVELOPER

okanyways let's go back to porting the features. So, what is the workflow you mentioend?

> AGENT

Here's the workflow for porting a feature from `dev_sprint` to `dev`:

1. **Pick the next slice** from the capability diff's recommended port order (`docs/plans/audits/dev-sprint-to-dev-capability-diff-2026-05-08.md`)
2. **Check its readiness** — only `[x]` port gate rows are immediately portable; `Near` rows need their pre-port work done first
3. **Read the relevant FS design-implementation diff** (`docs/plans/FS<N>/fs<N>-design-implementation-diff.md`) to understand what the design expects vs what the code does
4. **Branch off `dev`**, cherry-pick or reconstruct the slice from `dev_sprint`
5. **Run the baseline checks:**
   - `uv run ruff check .`
   - `uv run ruff format --check .`
   - `uv run python -m pytest --ignore=tests/frontend -x -q`
   - Plus any area-specific targeted tests listed in the capability row
6. **Open a draft PR to `dev`**, tag `@kungfusaini`
7. **Mark the port gate** — only `[x]` once every listed test is actually run and passing

You're through steps 1–2 of the port order (storage/migrations and prompt/LLM infra), with document storage authority in progress on your current branch. Want to pick up where you left off on that, or move to the next slice?

> DEVELOPER

So what I need to do is create some stuff on the linear board. Assigned to me, I want an epic for porting over dev sprint, then I want a ticket for every feater we hae to port. Make a plan first and then do that okay?

> AGENT

Let me check what Linear tools are available and review the port order to build out the ticket list.

> AGENT

I need to authenticate with Linear first, and also review the exact feature list from the capability diff. Let me do both.

> AGENT

Please open this URL in your browser to authorize Linear:

https://mcp.linear.app/authorize?response_type=code&client_id=https%3A%2F%2Fclaude.ai%2Foauth%2Fclaude-code-client-metadata&code_challenge=z539QTJnYOGZbzL4Uw6tTATvdphhUbh164kUeFbj8wo&code_challenge_method=S256&redirect_uri=http%3A%2F%2Flocalhost%3A60403%2Fcallback&state=1uUloe1-KfTXEHAAz-Lhj45EdsBu6ng7K5A2fY6M5zw&resource=https%3A%2F%2Fmcp.linear.app%2F

Once you've authorized, the Linear tools will become available and I can start planning the tickets.

> DEVELOPER

done

> AGENT

Let me gather the Linear context and review the port list in parallel.

> AGENT

Good, I have everything I need. Let me write up the plan.

> AGENT

Good, now I have the statuses. Let me update the plan with the exact status IDs.

> AGENT

The plan is ready. Here's the summary:

- **1 milestone** ("Port dev_sprint to dev") as the epic under the existing Elijah Pipeline Development project
- **13 tickets** — one per port slice from the capability diff, each with description, dependencies, and required tests
- Tickets 1-2 marked **Done** (already landed), ticket 3 marked **In Progress** (your current branch), tickets 4-13 marked **Todo**
- All assigned to you with the Feature label

> AGENT

Good question. Based on the capability diff's **Readiness** and **Port gate** columns:

| # | Slice | Readiness | Port gate | Status on dev |
|---|---|---|---|---|
| 1 | Base storage & migrations | - | `[x]` | **Already landed** |
| 2 | Prompt/LLM infrastructure | - | `[x]` | **Already landed** |
| 3 | Document storage authority | `Near` | `[ ]` | **In progress** (your branch) |
| 4 | P-E2E-GRAPH-01 graph gate repair | **`Ready`** | `[x]` | Not ported yet |
| 5 | FS11 QC infrastructure | `Near` | `[ ]` | Not ported |
| 6 | FS10 validation lifecycle | `Near` | `[ ]` | Not ported |
| 7 | FS2 runtime/Research Defensibility | `Near` | `[ ]` | Not ported |
| 8 | FS3 extraction/graph admission | `Near` | `[ ]` | Not ported |
| 9 | FS4 estimator/training stack | `Near` | `[ ]` | Not ported |
| 10 | FS5 edge weighting | `Near` | `[ ]` | Not ported |
| 11 | FS6/FS7 inference & output | `Near` | `[ ]` | Not ported |
| 12 | API/worker | `Near` | `[ ]` | Not ported |
| 13 | Ops/Docker/LiteLLM | `Not-ready` | `[ ]` | Not ported |

**Only ticket #4 (P-E2E-GRAPH-01 graph gate repair) is `Ready`** — it's the only row in the capability diff with both `Ready` readiness and a `[x]` port gate. It's a narrow, focused repair.

Everything else is `Near` — meaning the code exists on `dev_sprint` and is coherent, but targeted tests need to be rerun on a clean `dev`-based branch before it can earn its port gate tick. `Near` items are portable once you reconstruct them on `dev` and verify the tests pass.

Ops (#13) is `Not-ready` — needs a separate review against current deployment assumptions.

How do you want to reflect this in the tickets? Should I add the readiness status to each ticket, or change which ones we create?

> DEVELOPER

Okay so the implmenetion of them is all done but it's just not tested yet or whta?

> AGENT

Right. For the `Near` items, the code **exists on `dev_sprint`** — Patrick built it all out. But "porting" isn't just copying the code over. For each slice you need to:

1. **Reconstruct it** on a clean branch off `dev` (cherry-pick or rebuild)
2. **Rerun the targeted tests** on that clean branch (not just unit tests — the specific process/analytical gate tests listed in the capability diff)
3. **Pass the baseline checks** (ruff, format, pytest)

So the work for each ticket is really: reconstruct the slice on `dev`, verify it works there, open a PR.

The code is `implemented` (in the status vocabulary we found) but not `verified` — meaning it hasn't been proven on `dev` with all required gate evidence.

The exception is **#4 (P-E2E-GRAPH-01)** which Patrick already ran all the tests for on `dev_sprint` and marked `Ready` with full evidence — so that one just needs a clean cherry-pick and PR.

Want me to reflect this in the ticket descriptions — that the implementation exists on `dev_sprint` and the work is to port + verify on `dev`? And should I keep all 13 tickets, or just the ones that aren't done yet?

> DEVELOPER

Yeah please and also in each ticket you need to search deeply if there is any documentation for those features, what it eh testing doc etc. Be complete please

> AGENT

Let me do a deep dive on all the port slices. I'll launch 3 explore agents in parallel to cover everything.

> AGENT

Now I have everything. Let me write the complete plan with full ticket details.

> AGENT

Plan approved. Let me start creating everything in Linear. First the milestone, then all the tickets.

> AGENT

Milestone created. Now let me create the tickets. I'll do the first batch in parallel.

> AGENT

First 4 created: SPI-225 (Done), SPI-226 (Done), SPI-227 (In Progress), SPI-228 (Todo). Now tickets 5-8.

> AGENT

SPI-229 through SPI-232 created. Now tickets 9-13.

> AGENT

All 13 tickets created. Here's the summary:

| # | Ticket | Status | Priority |
|---|---|---|---|
| 1 | [SPI-225](https://linear.app/spire-elijah/issue/SPI-225) — Base storage & migrations | **Done** | High |
| 2 | [SPI-226](https://linear.app/spire-elijah/issue/SPI-226) — Prompt/LLM infrastructure | **Done** | High |
| 3 | [SPI-227](https://linear.app/spire-elijah/issue/SPI-227) — Document storage authority | **In Progress** | High |
| 4 | [SPI-228](https://linear.app/spire-elijah/issue/SPI-228) — P-E2E-GRAPH-01 graph gate repair | Todo | **Urgent** |
| 5 | [SPI-229](https://linear.app/spire-elijah/issue/SPI-229) — FS11 QC infrastructure | Todo | High |
| 6 | [SPI-230](https://linear.app/spire-elijah/issue/SPI-230) — FS10 validation lifecycle | Todo | High |
| 7 | [SPI-231](https://linear.app/spire-elijah/issue/SPI-231) — FS2 runtime/Research Defensibility | Todo | High |
| 8 | [SPI-232](https://linear.app/spire-elijah/issue/SPI-232) — FS3 extraction/graph admission | Todo | High |
| 9 | [SPI-233](https://linear.app/spire-elijah/issue/SPI-233) — FS4 estimator/training stack | Todo | High |
| 10 | [SPI-234](https://linear.app/spire-elijah/issue/SPI-234) — FS5 edge weighting | Todo | High |
| 11 | [SPI-235](https://linear.app/spire-elijah/issue/SPI-235) — FS6/FS7 inference & output | Todo | Medium |
| 12 | [SPI-236](https://linear.app/spire-elijah/issue/SPI-236) — API auth/worker context | Todo | Medium |
| 13 | [SPI-237](https://linear.app/spire-elijah/issue/SPI-237) — Ops/LiteLLM/Docker | Todo | Low |

All under milestone **"Port dev_sprint to dev"**, assigned to you, with blocking relationships set up between dependent tickets. Each ticket has full design docs, source code paths, test files, gates, and dependencies listed.

> DEVELOPER

wher where is the link to the milestone

> AGENT

The milestone doesn't have a direct URL in the API response unfortunately — Linear milestones live inside the project view. You can find it at:

**https://linear.app/spire-elijah/project/elijah-pipeline-development-ee09b9062361**

Click into the project and you'll see the **"Port dev_sprint to dev"** milestone with all 13 tickets grouped under it (showing 17% progress since 2 of 13 are done).

> DEVELOPER

yeah but the milestone is not assigned to me. so that's not correct I dont' want a milestone then please, just an epic

> AGENT

Got it. Let me create an epic issue and reparent all 13 tickets under it.

> AGENT

Epic created: [SPI-238](https://linear.app/spire-elijah/issue/SPI-238/epic-port-dev-sprint-to-dev). Now reparenting all 13 tickets under it.

> AGENT

Done. All 13 sub-tickets are now parented under the epic:

**[SPI-238: Epic: Port dev_sprint to dev](https://linear.app/spire-elijah/issue/SPI-238/epic-port-dev-sprint-to-dev)** — assigned to you, In Progress.

You can also delete the "Port dev_sprint to dev" milestone from the project settings if you want to clean that up — I can't delete it via the API.

> DEVELOPER

Okay so is the ticket order encoded?

> AGENT

Yes, the **dependency order is encoded via blocking relationships** between the tickets. For example:

- SPI-229 (FS11) is **blocked by** SPI-225 (storage)
- SPI-230 (FS10) is **blocked by** SPI-225 + SPI-229
- SPI-233 (FS4) is **blocked by** SPI-225 + SPI-229 + SPI-230
- SPI-234 (FS5) is **blocked by** SPI-229 + SPI-230 + SPI-233
- SPI-235 (FS6/FS7) is **blocked by** SPI-234

But there's no explicit **sort order** or numbering on the tickets themselves — Linear doesn't have a built-in "sequence number" field. The port order is listed in the epic description (SPI-238), and the blocking relations enforce what can't start before what.

Want me to add a prefix like `[1/13]`, `[2/13]` etc. to each ticket title so the order is visible at a glance on the board?

> DEVELOPER

Can any tickets be done in parallel?

> AGENT

Yes — based on the blocking relationships, here's the dependency graph:

```
Already done: SPI-225 (storage), SPI-226 (prompt/LLM)
                    │
        ┌───────────┼───────────┬──────────────┐
        ▼           ▼           ▼              ▼
    SPI-227     SPI-228     SPI-229        SPI-236
    Doc store   Graph gate  FS11 QC        API/worker
    (in prog)   (ready!)    
        │                       │
        ▼                       ▼
    SPI-232                 SPI-230
    FS3                     FS10
                                │
                        ┌───────┴───────┐
                        ▼               ▼
                    SPI-231         SPI-233
                    FS2             FS4
                                    │
                                    ▼
                                SPI-234
                                FS5
                                    │
                                    ▼
                                SPI-235
                                FS6/FS7
                                    
                            SPI-237 (Ops — last)
```

**Right now, 4 tickets can run in parallel:**
- **SPI-227** (Document storage) — already in progress
- **SPI-228** (P-E2E-GRAPH-01) — Ready, all deps landed
- **SPI-229** (FS11 QC) — all deps landed
- **SPI-236** (API/worker) — all deps landed

After those land, more parallel lanes open up (FS3 and FS10 can go at the same time, then FS2 and FS4 can go at the same time).

> DEVELOPER

okay awesome please update the ticket with this please. THe idea is that we can have multiple worktress working on these at the same time. For this to happen, we have to be very clear about acceptance criteria

> AGENT

Let me update the epic with the parallel lanes, then add clear acceptance criteria to every sub-ticket. I'll start with the epic and the 4 currently-unblocked tickets.

> AGENT

Epic updated. Now adding acceptance criteria to all sub-tickets. Starting with the 4 currently-unblocked ones.

> AGENT

4 unblocked tickets updated. Now updating the remaining 5 tickets (SPI-230 through SPI-235, SPI-237) with the same structure.

> AGENT

Now the last two — SPI-235 (FS6/FS7) and SPI-237 (Ops).

> AGENT

All 13 tickets updated. Every ticket now has:

- **Lane assignment** — which parallel lane it belongs to
- **Owned files** — files no other ticket should touch
- **Shared files** — files that overlap with other tickets, with scope constraints (e.g. "only touch document/artifact columns")
- **Acceptance criteria** — checkboxes with exact `pytest` commands plus behavioral requirements
- **Blocking relationships** — encoded in Linear's blocking system

This should be enough for multiple worktrees to pick up unblocked tickets and work independently without stepping on each other.

> DEVELOPER

So on every ticket, we need to have the order in which the agent should do to implement this properly. Then what it needs to do is collate the related design docs and docs and check that what's on dev sprint matches what's in the design docs. Then needs to look at what's in dev and then you know harmonize these three things. So the current implementation of dev sprint, the documentation, and what's currently on dev. And then if there's anything that's unclear or any design decision that seems stupid, for example overcomplicating things for no reason, going back on established patterns, for example, we have a node. If they're as JSON back in, we need to be aware of that, we need to be aware of all these things. Then it can ask me questions so that we can come to a good idea of what the current implementation is and what it should be. And then once I say and only when I say and approve on the plan, the agent can then implement it and open the review up. Only after running all the tests.

> AGENT

Got it. Let me update every ticket with this workflow. It's a structured 5-phase process that ensures the agent doesn't just blindly copy code — it reviews, questions, gets approval, then implements.

> AGENT

Epic updated with the full 5-phase workflow. Now I need to add the workflow steps to each sub-ticket. Let me build a standard block and add it to all active tickets (SPI-227 through SPI-237). I'll prepend the workflow to each ticket's existing description.

> AGENT

Two agents are updating all 11 sub-tickets in the background — adding the 5-phase workflow (Research → Harmonize → Ask questions → Implement → Open PR) to each one. The key gate is **Phase 3 is blocking** — no agent can implement without your explicit approval.

I'll let you know when both are done.

> DEVELOPER

We also have to make sure that we mention the testing that Patty mentioned so you mentioned that some of the tickets they're like near because they're not fully done. So and you also mentioned that there's some documents that show how to test it, is that true or no?

> AGENT

Good question. Let me check exactly what testing docs exist for each feature set.

> AGENT

So here's what exists per ticket:

| Ticket | Dedicated test plan? | Testing doc |
|---|---|---|
| SPI-227 (Doc storage) | No dedicated test plan | Tested via capability diff's P-DB gates |
| SPI-228 (Graph gate) | No dedicated test plan, but top-level gates report has full live-run evidence | `docs/plans/FS10/top-level-process-and-analytical-tests.md` (P-E2E-GRAPH-01) |
| SPI-229 (FS11 QC) | No dedicated test plan | `docs/plans/FS10/fs-capability-test-coverage.md` (P-FS11-01, A-FS11-01) |
| SPI-230 (FS10) | Yes — multiple | `docs/plans/FS10/analytical-test-matrix.md`, `fs-capability-test-coverage.md`, `top-level-process-and-analytical-tests.md` |
| SPI-231 (FS2) | No dedicated test plan | `fs-capability-test-coverage.md` (P-FS2-01, A-FS2-01), `archive/fs2-fs5-implementation-verification-report.md` |
| SPI-232 (FS3) | No dedicated test plan | `fs-capability-test-coverage.md` (P-FS3-01, A-FS3-01) |
| SPI-233 (FS4) | Archived | `archive/fs4-fs10-fs11-sequencing-plan.md`, `archive/fs4-test-questions-integration.md` |
| SPI-234 (FS5) | **Yes** | `docs/plans/FS5/fs5-fs10-fs11-test-plan.md`, `fs5-fs10-fs11-sequencing-plan.md` |
| SPI-235 (FS6/FS7) | **Yes** | `docs/plans/FS6/fs6-fs10-fs11-test-plan.md`, `docs/plans/FS7/fs7-fs10-fs11-test-plan.md` |
| SPI-236 (API) | No dedicated test plan | `docs/plans/orchestration/state-transition-conformance-report.md` |
| SPI-237 (Ops) | No dedicated test plan | `docs/plans/testing/github-parity-verification-checklist.md` |

So the answer is: **some tickets have dedicated test plans (FS5, FS6, FS7), and all tickets are covered by the capability test coverage matrix** (`docs/plans/FS10/fs-capability-test-coverage.md`) which lists the required gates per feature set. The top-level gates report (`top-level-process-and-analytical-tests.md`) also documents which tests Patrick ran and which ones are still pending.

The "Near" status specifically means: Patrick's top-level gate run covered P-FS1-01 through P-FS4-01 in production-lock mode, but **the targeted per-FS test batches were not rerun on a clean branch**. That's what each ticket needs to do during Phase 4.

Want me to add references to these testing docs in each ticket, so the agent knows exactly where to look for test requirements?

> AGENT

Tickets 233-237 done. Yes, let me add the testing doc references to each ticket. The other agent should finish shortly too — let me add the test doc references once it completes.

> DEVELOPER

yeah please do that

> DEVELOPER

So the testing needs to be if there's a testing plan available then needs to be that needs to happen as part of the roll out. So the testing needs to be done or implemented. And same for if there's no testing plan then we need to think about how to test it.

> AGENT

Got it. So the rule is:

- **Has a test plan** (FS5, FS6, FS7) → the agent must follow it, implement the tests, run them
- **No test plan** (everything else) → the agent must propose a test approach during Phase 3, get your approval, then implement tests

Let me update all 11 active tickets with this.

> AGENT

All 11 tickets now have testing requirements. Here's the rule as encoded:

| Has test plan? | Tickets | What the agent does |
|---|---|---|
| **Yes — follow it** | SPI-234 (FS5), SPI-235 (FS6/FS7) | Must follow the dedicated `fs*-fs10-fs11-test-plan.md` during implementation |
| **No — propose one** | All others (SPI-227–233, 236, 237) | Must propose a test approach during Phase 2, get your approval in Phase 3, then implement tests |
| **Live evidence** | SPI-228 (graph gate) | Must reproduce Patrick's live-run evidence from the top-level gates report |

Every ticket also references `docs/plans/FS10/fs-capability-test-coverage.md` and the capability diff's test evidence column so the agent knows exactly what gates need to pass.

> AGENT

Both background agents are done. All 13 tickets now have:

1. **5-phase workflow** (Research → Harmonize → Ask questions [BLOCKING] → Implement → Open PR)
2. **Testing requirements** (dedicated test plan if one exists, or must propose + get approval if not)
3. **Owned/shared files** for parallel worktree safety
4. **Acceptance criteria** with exact test commands
5. **Blocking relationships** encoding the dependency graph

Everything's set up on the board. Want to start working on any of the 4 unblocked tickets?

> DEVELOPER

is there anything that's missing?

> AGENT

Let me think about this critically. A few things come to mind:

1. **Pinned source commit** — `dev_sprint` is still getting commits (latest `0621983`). Should we pin a specific commit SHA so all agents port from the same baseline? Otherwise one agent might port from a newer commit than another and they could conflict.

2. **Shared file merge strategy** — Multiple tickets touch `packages/storage/database.py` (almost all of them). Even with the "only touch your columns" rule, if Lane 1 and Lane 3 are working simultaneously, the second PR to land will have merge conflicts. Should there be a rule like "rebase on dev before opening PR" or "later tickets rebase on top of earlier merged tickets"?

3. **Where to save the Phase 2 harmonization report** — The agent does research and produces a comparison. Should that go in the PR description? In a comment on the Linear ticket? In a doc in the repo? If it's just in the conversation, it's lost.

4. **PR should reference the ticket** — Should each PR title include the SPI number (e.g. `SPI-227: Port document storage authority`)?

5. **The orphaned milestone** — "Port dev_sprint to dev" milestone still exists on the project. I can't delete it via API — you'd need to remove it manually in Linear settings.

6. **Memory for future conversations** — I should save the porting workflow context so future conversations know about this epic and how to work on it.

Any of these worth addressing, or anything else you're thinking about?

> DEVELOPER

No so for 1 we can just take as it is at the point of working, no need to pin. For 2, I will I will merge the tickets that like I'll merge the PRs once they're put up there and they pass the tests and then we can start implementing the next thing so we shouldn't move on until all the dependencies are merged. in terms of the phase two, I don't want to report. I just want to discuss it. You can put it in a comment on the linear ticket if you like. You should actually do that. Put it in a comment on the linear ticket so we can keep discussing it as well. The PR should reference the ticket, yes. You can I did delete the milestone, so that should be fine as well. Yes, you should save this to your memory also.

> AGENT

Now let me update the tickets with the two remaining rules: Phase 2 goes as a Linear comment, and PRs reference the SPI number. Let me update the epic workflow since that's where all tickets inherit from.

> AGENT

Done. Everything's updated:

- **Epic** now has the dependency rule ("don't start until blockers are merged on dev"), Phase 2 findings go as Linear comments, PR titles must include SPI number, PRs opened as drafts
- **Memory** saved for future conversations
- **Milestone** — you've already deleted it

The board is ready to go. Anything else, or want to pick up one of the 4 unblocked tickets?

> DEVELOPER

Awesome. So let's say that I want to have multiple agents running in parallel. Should I just talk to you and you do that, or should I open up different work trees on Cloud and have four different town wheels? What do you think?

> AGENT

I'd recommend **opening separate Claude Code sessions in separate worktrees**. Here's why:

**Multiple worktrees (recommended):**
- Each agent gets its own full context window dedicated to one ticket
- The research phase alone (reading all design docs, dev_sprint code, dev code, diffs) is heavy — it'll eat a lot of context
- Each agent can have a focused conversation with you about its specific ticket during Phase 3
- No risk of agents cross-contaminating each other's work
- Git worktrees give clean isolation — no accidental file conflicts

**Me spawning sub-agents (not ideal for this):**
- Sub-agents can't have a back-and-forth conversation with you — they run and return
- But Phase 3 is a blocking discussion where you need to ask questions, push back, approve
- That interactive loop doesn't work well with fire-and-forget sub-agents

**Suggested setup:**

```
# Terminal 1 — Lane 1
git worktree add ../elijah-spi-227 dev
cd ../elijah-spi-227 && claude

# Terminal 2 — Lane 2
git worktree add ../elijah-spi-228 dev
cd ../elijah-spi-228 && claude

# Terminal 3 — Lane 3
git worktree add ../elijah-spi-229 dev
cd ../elijah-spi-229 && claude

# Terminal 4 — Lane 4
git worktree add ../elijah-spi-236 dev
cd ../elijah-spi-236 && claude
```

Then tell each session "Work on SPI-227" (or whichever ticket). They'll pick up CLAUDE.md, read the Linear ticket, and start the 5-phase workflow. You can rotate between terminals to answer Phase 3 questions as they come up.

> DEVELOPER

Hey man so I started doing all this and I did everything except for lane 3 which i started, the problem is, I dont' what know worktree I ussed, maybe it's called 229 or soething? can you find it

> AGENT

Your worktree `229` is at `/Users/sumeet/matrix/elijah/.claude/worktrees/229` but it's actually on branch `port/spi-230-pr1-core-stores` — looks like it may have been repurposed or the branch name doesn't match the folder. 

To open it in Claude Code: `! cd /Users/sumeet/matrix/elijah/.claude/worktrees/229 && claude`

> DEVELOPER

Hey once again I lost where I was working. We had finished all the lanes and moved on to newer work!

> AGENT

The full SPI-238 epic and its 13 child tickets are all Done. You've moved on to newer work. Here are the active candidates:

**Open PR (draft):**
- **#219 — SPI-262**: LiteLLM preflight refactor + prompt task ID contract
  - Worktree: `.claude/worktrees/agent-aeb7e76b6275d56e6` (locked)

**Active locked worktrees (likely in-progress):**
- **SPI-264** — FS1 core runtime port → `.claude/worktrees/agent-a289756c84b945eac`
- **SPI-262** — LiteLLM preflight refactor → `.claude/worktrees/agent-aeb7e76b6275d56e6`

**Backlog tickets that might be the "newer work":**
- SPI-240 — deferred FS12 route port
- SPI-256 — codebase structure investigation
- SPI-259 — elijah_seed.sql auto-load decision

Want me to peek inside SPI-262 and SPI-264 worktrees to see which one has uncommitted progress?

> DEVELOPER

No so I wanna resume that chat but ifk how (I was doing both spi  264 and 262 from the saem chat)

> AGENT

You can resume Claude Code sessions with `claude --resume`. Let me find the session that worked on both.

> AGENT

Found it. Your chat was session `2a1ed168-96c5-480c-825e-15dacbe0b705` running in the **`229`** worktree — it spawned SPI-262 and SPI-264 as subagents from there.

To resume:

```
! cd /Users/sumeet/matrix/elijah/.claude/worktrees/229 && claude --resume 2a1ed168-96c5-480c-825e-15dacbe0b705
```

Or just `cd` there and run `claude --resume` to pick from the list. Last activity was May 15 16:08, parent transcript is 18MB so it's a long-running chat.

> DEVELOPER

hey man ther was another conversation I was having in a differnt wortree just a few minutes ago on the UI? can you find it?

> AGENT

Found it:

**Worktree:** `.claude/worktrees/floofy-watching-hopcroft` (branch `worktree-floofy-watching-hopcroft`)
**Session:** `5c519836-42a5-4a10-b863-5ec89ccb5d19` — last activity May 19 08:44
**Topic:** SPI-242 (CF ZT → per-user Elijah identity bridging)

To resume:
```
! cd /Users/sumeet/matrix/elijah/.claude/worktrees/floofy-watching-hopcroft && claude --resume 5c519836-42a5-4a10-b863-5ec89ccb5d19
```
