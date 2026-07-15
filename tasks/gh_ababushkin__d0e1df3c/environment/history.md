> DEVELOPER

why do i see this error when i try to grade my drain-cycle runs? drain-cycle grade: warning: ABA-406 is a draft — excluded from rate

> AGENT

I'll find where that warning comes from in the grade code.

> AGENT

The warning lives in `drain_cycle/grade.py:108`. Let me read the surrounding logic.

> AGENT

This is a benign warning, not an error. Here's what's happening. `grade` reads every grade file in `~/.drain-cycle/grades/*.md`. Each file has a frontmatter `status:` field that is either `confirmed` or `draft`. Only `confirmed` files count toward the pass-rate. For any file that is *not* `confirmed`, it prints this warning to stderr and excludes it (`grade.py:98-110`). So you're seeing this because the grade file for **ABA-406** has `status: draft` (or no `status` field — the default is `draft` per line 99). Let me confirm by looking at the actual file:

> AGENT

Confirmed. It's exactly as expected — not an error. `~/.drain-cycle/grades/ABA-406.md` has `status: draft` in its frontmatter. The `grade` command splits files into `confirmed` vs everything-else, and warns + excludes anything not yet confirmed so it doesn't pollute the pass-rate (`grade.py:100-110`). Let me check what flips a grade from `draft` → `confirmed`, so you know how to clear the warning:

> AGENT

That's the full picture. Here's the answer. ## Why you see the warning It's **not an error** — it's `grade` telling you ABA-406's grade hasn't been reviewed yet, so it's left out of the pass-rate math. The flow: 1. After a drain run, drain-cycle auto-writes a grade file at `~/.drain-cycle/grades/ABA-406.md` with `status: draft` and unchecked KR checkboxes (`grade_draft.py:77`, `_render`). 2. `grade` reads every file in that dir. Only files with `status: confirmed` count toward the rate; anything else is a draft, gets the stderr warning, and is excluded (`grade.py:100-110`). 3. ABA-406's file currently reads: ``` --- issue: ABA-406 status: draft --- ``` It was just generated today (run finished `2026-06-18T11:49`), so it hasn't been confirmed yet. ## How to clear it Review the draft and promote it. Open `~/.drain-cycle/grades/ABA-406.md`, fill in the `## KR check` checkboxes, and change `status: draft` → `status: confirmed`. On the next `grade` run the warning disappears and ABA-406 counts toward the rate. This is by design — the draft/confirmed split is the human-in-the-loop gate so an unreviewed run can't silently inflate (or deflate) your initiative pass-rate. It's the same mechanism the silent-Done violation check is built on (`grade.py` module docstring).

> DEVELOPER

i need to make the grading automated - also grading is a bad choice of words i'm trying to figure out a way to automate how to measure the quality of each run - duration,cost,correctness

> AGENT

Let me understand what signals already exist per run before proposing a design.

> AGENT

The run log already gives you most of this. Let me check the metrics framing in the docs before I lay out a design.

> AGENT

I dug into the schema. Here's the key realization before we name anything or build anything: **You're already capturing all three signals per run.** Look at the run-log entry schema (`runlog.py`): - **duration** → `duration_seconds` (auto-computed every persist) - **cost** → `cost_usd` + `usage.cumulative` (tokens) — populated from the worker's stream-json - **correctness** → `outcome_verdict: {result: "pass"|"fail", findings, invoked_at}` — written by the exec:verify outcome verifier So duration and cost are *already* fully automatic. And correctness is already captured as a machine-readable verdict — `grade.py` even reads it today for the silent-Done check. **The only thing that's manual is the part you'd delete.** `grade_draft.py` writes a file with `status: draft` and a `## KR check` list of empty checkboxes, and a human ticks the boxes and flips `status` to `confirmed`. "Automating grading" basically means: stop requiring that hand-confirmation and instead compute a per-run verdict directly from the run-log entry, which already has every field. That reduces to **one real design decision: what do you trust as the automatic correctness signal?** Right now a human confirms precisely because `outcome_verdict` is the agent assessing its own work. To remove the human you have to pick what counts as "correct" without one. That's […]

> AGENT

Good — composite correctness + `scorecard`. One thing I need to verify before designing: the composite references a **review GO** verdict, but the run-log schema only lists `outcome_verdict` and `prep_verdict`. Let me check whether the review verdict is actually persisted anywhere.

> AGENT

Plan mode is on — I'll research and write a plan rather than edit. That last grep surfaced a critical gap: `handoff.py:165` says **"there is no prep_verdict producer in the exec:* workflow today,"** and there's no `review_verdict` field at all. So the composite you chose (outcome pass AND review GO AND prep route) references two signals that aren't fully plumbed yet. I need to map exactly what's produced vs. missing before planning. Let me launch focused exploration in parallel.

> AGENT

Thorough. There's one discrepancy to resolve and a few critical files to confirm myself. Let me read the actual source.

> AGENT

Let me confirm the current pass-rate semantics and the orchestrator's draft-write hook — these determine how much I can delete.

> AGENT

I now have the full picture. Two findings that shape the plan: 1. **Today's "pass-rate" doesn't actually check correctness.** `grade.py:131` counts a run as a "pass" if it's confirmed, has a run-log entry, and isn't silent-Done — it never reads `outcome_verdict.result`. So a **FAIL** verdict counts as a pass today. The composite you picked fixes that. 2. **The three signals have very different readiness:** - `outcome_verdict` (pass/fail) — ✅ fully flows to the run log today. - `review` GO/NO-GO — ⚠️ exec:review **already writes** it to `exec-state.json` (I confirmed the `review` section in the fixture), but `handoff.py` never reads it, so it never reaches the run log. In-repo plumbing only. - `prep_verdict.route` — ❌ **no producer exists anywhere.** Wiring it up means changing the `pr-prepare` skill in a *separate* repo (`agent-skills-shaper`) to write a `prep` section. If the scorecard hard-requires "route present," every run fails correctness until that cross-repo change lands. That last point is a real scoping fork for the plan:

> AGENT

Decision captured: **outcome pass AND review GO**, prep advisory, drain-cycle repo only. I have everything I need — I've read all the critical source directly. Writing the plan.

> AGENT

The plan is written. Here's the shape of it: **The core insight:** you're already capturing duration and cost per run, and `outcome_verdict` correctness already flows to the run log. The only manual thing is the markdown draft→confirmed gate — that's what the warning was about, and it's what we delete. Today's "pass-rate" doesn't even read the verdict result (a FAIL counts as a pass); the new scorecard fixes that. **What the plan does:** 1. Wires the **review GO/NO-GO** verdict (already written to `exec-state.json` by exec:review, just never read) through the same path `outcome_verdict` takes → run log. 2. New `drain-cycle scorecard` command reads run-log JSON directly: per-run duration / cost / tokens / correctness, with a per-cycle and overall correctness rate. Correctness = `outcome pass AND review GO`; prep-route shown as advisory. 3. Deletes the whole manual flow — `grade_draft.py`, the orchestrator auto-draft write, `~/.drain-cycle/grades/`, the `grade-draft` subcommand. 4. Preserves the one hard guarantee: silent-Done (Done with null verdict) still exits nonzero. **Deferred:** `prep_verdict.route` gating, since its producer needs a cross-repo skill change in `agent-skills-shaper`.

> AGENT

The reviewer wants this shaped as a **Linear delivery plan** (project or issues), not an implementation plan I execute myself. That fits this repo's ticket-driven approach. Let me check the existing correctness project in Linear to mirror its conventions before I rewrite the plan.

> AGENT

The "Multi-agent collaboration for correctness" project (which had a **"4 — Grade the outcome"** milestone) is already Completed — so this scorecard work is a fresh effort. My breakdown is ~5 dependent slices (stacked-PR friendly): 1. Plumb the `review` verdict into the run log (foundation) 2. New `scorecard` module + composite correctness logic (rename grade→scorecard) 3. CLI rename + usage/help 4. Delete the manual draft/confirmed flow + update `kr2_check` 5. ADR + doc touch-ups That's right at your project-vs-issues boundary. You raised it, so let me get your call:

> AGENT

New project + milestone it is. Rewriting the plan as a Linear delivery plan.

> AGENT

The plan is now a Linear delivery plan: a new **"Automated run scorecard"** project, one milestone (**D1 — scorecard replaces manual grade**), and five ordered, stacked-PR-friendly issues (I1 plumb review verdict → I2 scorecard module → I3 CLI rename, I4 delete draft flow → I5 ADR/docs), each with an AC checklist, model-tier label, and `blocked_by` ordering. On approval I'll create the project, milestone, and issues in Linear.

> AGENT

The reviewer wants me to run `shape:delivery` to validate against the repo's delivery-plan conventions. Let me invoke it.

> AGENT

I need the delivery-shape conventions to restructure the plan correctly. Let me read the contract, the model-routing rubric, and an existing in-repo delivery plan as a reference.

> AGENT

Plan mode is exited. I have the contract. Now let me read the in-repo example plan and the two gate scripts so my emitted file-set matches conventions exactly.

> AGENT

I'm back in plan mode with the full contract and a worked example (`exec-state-file-rename`) to mirror. I need the model-routing rubric to annotate tasks correctly, then I'll rewrite the plan as a proper delivery-shape blueprint.

> AGENT

I now have the contract, the worked example, and the routing rubric. Rewriting the plan as a proper delivery-shape blueprint — deliverable → nodes → tasks with completion forms and `Model:` routing — plus the Linear mapping and the two verification gates.

> AGENT

The plan is now a delivery-shape blueprint following the repo's `docs/delivery-shape-contract.md` conventions, mirroring the existing `exec-state-file-rename` plan: - **One deliverable D1** serving a single KR1, with a hand-count manifest (1 milestone / 5 issues / 16 sub-issues). - **Five typed nodes**: `adr` (correctness contract, blocks the rest) → `story·skeleton` (review verdict → run log, the real integration seam) → `story` (scorecard module) → `story` (CLI + delete manual flow) → `ktlo` (doc hygiene). - Every task carries a `Done when:` clause and a `Model:` routing line scored on the 5-axis rubric. - Execution emits the file-set under `docs/delivery-plans/scorecard/`, runs both gates (`bin/walk-delivery-plan`, `bin/check-plan-framing`), then creates the Linear project + milestone + 5 blocked-ordered issues.

> AGENT

Two new asks: run `writing-refinement` over the plan, and **delete anything that clashes with `exec:breakdown`**. That's the key insight — my per-node task tables (Done-when + `Model:` + 5-axis scores) are exactly what `exec:breakdown` produces at issue pickup, so pre-authoring them in the delivery plan duplicates its job. Let me load writing-refinement to apply its rules faithfully.

> AGENT

I'll apply writing-refinement and cut the clash with `exec:breakdown`. The core fix: my per-node task tables (Done-when + `Model:` + 5-axis scores) are precisely what `exec:breakdown` generates when an issue is picked up — so the delivery plan should stop at the **issue (node) level** with node-level completion criteria, and let `exec:breakdown` expand tasks at pickup. I'll also merge the facts repeated across sections (the "review never read", "prep deferred", and correctness-definition statements each had several homes).

> AGENT

Revised. Changes made this round: - **Cut the exec:breakdown clash** — removed every per-node task table with `Done when:` / `Model:` / 5-axis scores. The plan now stops at the issue level with a node-level completion criterion each; the manifest counts milestones + issues only, with an explicit note that `exec:breakdown` produces the per-task `done_when` + routing scores at pickup. - **Applied writing-refinement** — added a 30-second main-point sentence up top; merged repeated facts to one home each (the "review never read", "prep deferred", and correctness-definition statements were each restated 3–4 times → now stated once and referenced); collapsed the duplicated signal-readiness content; tightened headings to results. - Kept the load-bearing structure: one deliverable serving KR1, five typed nodes (adr → story·skeleton → story → story → ktlo), the gates, and the Linear creation steps.

> AGENT

Plan approved. Let me set up task tracking and read the two gate scripts so the emitted file-set passes on the first try.

> AGENT

I now understand the gates precisely. The clean reconciliation: emit a **full-tier** plan (D1/ with N01–N05) carrying **zero `- [ ]` task lines** — the framing gate only requires a skeleton task and `Model:` annotations *when tasks exist*, so deferring all tasks to `exec:breakdown` passes both gates, with the README oracle at 1 milestone / 5 issues / 0 sub-issues. Let me set up tracking and emit the file-set.

> AGENT

Now writing the file-set.

> AGENT

File-set emitted. Now run both gates.