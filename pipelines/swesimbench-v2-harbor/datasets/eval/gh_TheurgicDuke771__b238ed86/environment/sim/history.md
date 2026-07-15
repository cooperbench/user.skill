[DEVELOPER]: What's pending for week 2?

[AGENT]: I'll check the live tracker and GitHub milestone for v1.1 Week 2.

[AGENT]: The GitHub milestone query returned empty — let me check the exact milestone name and read the W2 section of the tracker.

[AGENT]: The milestone title has a suffix. Let me pull the open issues directly.

[AGENT]: Here's what's still open in **v1.1 Week 2** (Portability: OTel logs, secrets lifecycle, dry-run depth — due 2026-07-18). The big portability seams already landed and are prod-verified (dbt provider #609/#611, OTel logs #524/#589, `SecretStore.delete` #372/#622). What remains is **20 open issues**, split into the originally-planned work and follow-ups that got mapped into the milestone: ## Originally-planned W2 work still pending **Alerting vendor-neutrality batch** (one batch PR — same code area): - [#386](https://github.com/TheurgicDuke771/DataQ/issues/386) — tie `dedup._RANK` to a shared severity source - [#387](https://github.com/TheurgicDuke771/DataQ/issues/387) — `suppression.py` early-return on `run.status == 'failed'` - [#388](https://github.com/TheurgicDuke771/DataQ/issues/388) — single-source the `alert_on` literals - [#389](https://github.com/TheurgicDuke771/DataQ/issues/389) — rename `teams_webhook_secret_name` → channel-neutral (the vendor-neutrality item) - [#416](https://github.com/TheurgicDuke771/DataQ/issues/416) — enrich Slack/email alerts (deep link, expected-vs-observed, sample, metadata) **Dry-run depth & MCP:** - [#532](https://github.com/TheurgicDuke771/DataQ/issues/532) — extend dry-run preview Snowflake-only → UC + flat-file - [#584](https://github.com/TheurgicDuke771/DataQ/issues/584) — MCP NL tool-selection spot-check vs live `/mcp` (4 canonical queries, PAT-auth) - [#488](https://github.com/TheurgicDuke771/DataQ/issues/488) — workspace-admin visibility in MCP tools + schedules ## Follow-ups / gaps mapped into W2 - [#647](https://github.com/TheurgicDuke771/DataQ/issues/647) — admin webhook-config mislabels dbt connections as airflow (ADR 0029 two-provider if/else miss) - [#651](https://github.com/TheurgicDuke771/DataQ/issues/651) — expectation-kind checks don't validate `expectation_type`/config (invalid checks silently persist) - [#652](https://github.com/TheurgicDuke771/DataQ/issues/652) — dbt provider missing from Suite Triggers dropdown […]

[DEVELOPER]: Lets pickup the alert related ones

[AGENT]: Let me pull the full details of the alerting issues and look at the code they touch.

[AGENT]: Let me read the alerting module files to understand the current structure.

[AGENT]: Now let me read base.py, the model constraints, and config for the shared-severity and rename work.

[AGENT]: Let me read the relevant model sections and the `_in_check` helper.

[AGENT]: Let me read the remaining pieces: registry, config, notification_service validation, and existing alerting tests.

[AGENT]: The `teams_webhook_unresolved` log event grep came back empty — let me check teams.py directly for the log event naming.

[AGENT]: I've now read through the whole alerting layer. Here's what I found — two of the four "nits" turn out to be substantially overtaken by later refactors, which changes the shape of the work: **Real code changes:** - **#386** — `dedup._RANK = {"warn":1,"fail":2,"critical":3}` is still a hardcoded literal, independent of `base.FAILING_TIERS = ("warn","fail","critical")`. Genuine fix: derive `_RANK` (and `_OPERATIONAL_RANK`) from `FAILING_TIERS` + a drift test. - **#387** — `suppression.all_failures_snoozed` still has no `run.status == 'failed'` guard. Genuine fix: early-return `False` + test. **Mostly already done (need locking tests only):** - **#388** — model↔validation `alert_on` is *already* single-sourced through `ALERT_ON_POLICIES` (used by both the `CheckConstraint` and `notification_service` validation — the #633 refactors did this). The one remaining hand-copy is `routing.py`'s `FAIL_ONLY/WARN_PLUS/ALWAYS`. So the work is a drift-guard test + tying routing's constants to the constant. - **#389** — appears **obsolete**. When it was filed, Teams was the only publisher and `teams_webhook_secret_name` doubled as the generic seam name. Since #413/#633, Slack + email publishers exist with parallel per-channel config (`slack_webhook_secret_name`, `email_*`), so `teams_webhook_secret_name` is now *correctly* the Teams channel's key, symmetric with Slack. The stale `teams_webhook_unresolved` log event is already `workspace_webhook_unresolved` with a `channel=` field. Renaming to `notification_webhook_secret_name` now would *break* the […]

[AGENT]: Settled. Plan: close #389 with the analysis, then implement the #386/#387/#388 batch on a branch with tests, run the gate, and open a PR. #416 comes after as its own PR. Let me set up tracking, close #389, and create the branch.

[AGENT]: #389 closed. Now #386 — derive `_RANK` from the shared `FAILING_TIERS`.

[AGENT]: #387 — suppression guard for operationally-failed runs.

[AGENT]: #388 — the model↔validation `alert_on` literals are already single-sourced via `ALERT_ON_POLICIES`; the remaining hand-copy is `routing.py`'s policy constants. Let me tighten that comment and lock it all with drift-guard tests. First the comment:

[AGENT]: Now the tests. Let me look at the existing test files to match style.

[AGENT]: Now let me check test_routing.py and test_suppression.py structure before adding tests.

[AGENT]: Now I'll add the drift-guard tests. First #386 in test_dedup.py:

[AGENT]: #387 in test_suppression.py:

[AGENT]: #388 in test_routing.py:

[AGENT]: Now the #388 test block at the end of test_routing.py:

[AGENT]: Diagnostics cleared. Let me update tracking and run the local gate.

[AGENT]: Postgres is up. Let me run the alerting tests plus format/lint/mypy on the changed files.

[AGENT]: The constraint name differs (likely a naming-convention prefix). Let me check.

[AGENT]: The naming convention prefixes it to `ck_suite_notifications_alert_on_valid`. Let me match by suffix.

[AGENT]: Now re-run the tests and the full lint/format/type gate on the changed files.

[AGENT]: All 43 pass. Now format, lint, and type checks on the changed files.

[AGENT]: mypy flags the implicit re-export in my identity test. That test is marginal — the constraint + routing tests already prove the drift guard. Let me drop it and the now-unused import.

[AGENT]: mypy clean, tests green. Now the full alerting suite with coverage on the changed modules, plus Bandit.

[AGENT]: Full gate is green — 100% coverage on all three changed modules, Black/Ruff/mypy/Bandit clean. Let me commit as three per-issue commits (they touch disjoint files) and update the todo.

[AGENT]: Three clean per-issue commits. Now the agentic code-review on the diff before I push (per the working agreement — real `/code-review`, not an inline self-review).

[AGENT]: The diff is small and mechanical, but let me verify the two things worth checking: no circular import from the new `dedup → base` dependency, and nothing external depends on the old literal `_RANK`/`_OPERATIONAL_RANK` values.

[AGENT]: The review surfaced something worth checking: the severity-rank map now appears derived-from-`FAILING_TIERS` in two places (my `dedup._RANK` and `builder._SEVERITY_RANK`) and still hardcoded in a third. Let me check whether `run_service._SEVERITY_RANK` is genuinely the same concept before deciding whether to hoist a single canonical source.

[AGENT]: Good — this is a real finding, and it's exactly the drift class #386 targets: the severity-rank map exists as an identical **derived** copy in `dedup` (my change) and `builder`, and still as a **hardcoded** copy in `run_service._SEVERITY_RANK`. But converging all three touches a non-alerting service and involves a layering call (where the one canonical `SEVERITY_RANK` should live), so per the working agreement I'll file it as a follow-up rather than balloon this nit PR. No correctness bugs surfaced. Let me push, then file the follow-up issue and open the PR.

[AGENT]: Issue #655 filed. Now open the PR.

[AGENT]: PR #656 is up. Let me finalize tracking.

[AGENT]: The alerting-nit batch is done and shipped as a PR. Summary of this session: ## What landed **PR [#656](https://github.com/TheurgicDuke771/DataQ/pull/656)** — three per-issue commits, all local gates green (116 alerting tests pass, 100% coverage on the three changed modules; Black/Ruff/mypy/Bandit clean): - **#386** — `dedup._RANK` now derives from the shared `base.FAILING_TIERS` (values unchanged) so severity ordering can't silently drift from routing/suppression. + drift-guard test. - **#387** — `suppression.all_failures_snoozed` early-returns `False` on `run.status == 'failed'`, so an execution failure can never be silenced by per-check snoozes (defensive; no behaviour change today). + test. - **#388** — locked `alert_on` literals to the single `ALERT_ON_POLICIES` source (model↔validation were already single-sourced; tightened routing's comment) + drift-guard tests on routing's constants and the CHECK-constraint SQL. ## Decisions & follow-ups - **#389 closed as won't-fix** — overtaken by the Slack/email publishers; `teams_webhook_secret_name` is now correctly channel-specific and symmetric with `slack_webhook_secret_name`. Renaming would break symmetry and force a needless prod env-var change. Full rationale posted on the issue. - **[#655](https://github.com/TheurgicDuke771/DataQ/issues/655) filed** — the code-review found `run_service._SEVERITY_RANK` is still a third hardcoded copy of the same severity-rank map (the exact drift class #386 targets); converging all three needs a layering call, so it's deferred rather than expanding this nit […]

[DEVELOPER]: check CI for #656, if clears then merge. Next #655

[AGENT]: I'll check CI on #656.

[AGENT]: All 14 checks pass. Squash-merging #656.

[AGENT]: Merged. Let me sync local main and update the progress tracker.

[AGENT]: Let me update the W2 cycle-plan rows and the snapshot count.

[AGENT]: Now the four W2 alerting rows:

[AGENT]: Now the Snapshot open-issues count (64 → 66) with a brief note about this batch:

[AGENT]: Let me check whether the cycle epic #597 has a checklist item to tick.

[AGENT]: The epic's batch checklist item is now fully resolved (3 fixed + #389 won't-fix). Let me tick it.

[AGENT]: Tracker updated and epic ticked. Now on to **#655**. The progress.md edits are uncommitted on main — I'll carry them onto the #655 branch and fold the tracker refresh into that PR. Let me create the branch and gather the layering facts I need.

[AGENT]: No import cycle risk (`db.models` only imports `db.base`), and `dashboard_service` uses penalty *weights* (`_PENALTY`) — a genuinely separate concept. Plan for #655: put the canonical `SEVERITY_RANK` in `db.models` (derived from the existing `_RESULT_SEVERITY_TIERS`), point `dedup`/`builder`/`run_service` at it, pin `FAILING_TIERS` to it with a drift test, and document that the dashboard weights stay separate. Let me read the dashboard weights block and the test I added.

[AGENT]: `_PENALTY` genuinely weights `pass` too — a separate concept, good. Let me confirm `run_service`'s existing db.models import and check db.models' imports for cycle safety before editing base.

[AGENT]: Clean — no cycle risk. Now let me implement. First the canonical `SEVERITY_RANK` in db.models:

[AGENT]: Now `alerting/base.py` — derive `FAILING_TIERS` from `SEVERITY_RANK`:

[AGENT]: Now `dedup.py` — use the shared `SEVERITY_RANK` directly:

[AGENT]: Now fix the `_RANK` usages in dedup's `_failing_ranks`:

[AGENT]: Now update builder.py, run_service.py, the dashboard note, then the tests. Let me handle builder:

[AGENT]: Now run_service.py:

[AGENT]: run_service is clean. Now document the dashboard_service separation:

[AGENT]: Now the tests. Let me update the #386 drift test in test_dedup.py (it referenced the now-removed `dedup._RANK`):

[AGENT]: Now a drift-guard test proving the single source. Let me find where models-level tests live.

[AGENT]: No dedicated models test file — I'll add a focused drift-guard test for the canonical constant:

[AGENT]: Let me check for any remaining test references to the removed `_SEVERITY_RANK`/`_RANK` symbols:

[AGENT]: Let me refresh the todo list for the #655 work and run the gate.

[AGENT]: No import cycle, values correct. Now the full gate:

[AGENT]: All 182 pass. Now Black/Ruff/mypy/Bandit on the changed files:

[AGENT]: Fish didn't word-split the variable. Let me redo with a proper list:

[AGENT]: Fish variable expansion is fighting me. Let me run each tool with explicit args in separate calls.

[AGENT]: Black/Ruff/mypy clean, Bandit only benign `nosec`-encountered warnings. Since this touches core modules (`db.models`, `run_service`), let me run the full backend suite to be safe.

[AGENT]: Full suite green (1443 passed, 1 skipped). Let me commit — the refactor first, then the docs tracker catch-up.

[AGENT]: Refactor + tracker committed. Let me do a focused review pass on the #655 diff before pushing.

[AGENT]: Diff is clean and behavior-preserving. Let me push and open the PR.

[AGENT]: PR #657 is up. Following the same flow you set for #656, let me check its CI (it'll take a few minutes to populate).

[AGENT]: Fast checks green; backend tests / type-check / CodeQL / Playwright still running (~3–4 min). Let me update tracking and poll until they finish.

[AGENT]: Type-check now green too. Backend tests / Playwright / CodeQL / frontend tests still running. Let me relaunch the poll.

[AGENT]: The poller keeps returning nonzero (`gh pr checks` exits nonzero while checks are pending — that's expected, not a real failure). Let me just check directly.

[AGENT]: Only backend tests, Playwright, and frontend tests remain. Let me use `--watch` (blocks until all checks resolve) in the background.

[AGENT]: While CI finishes on #657, here's where things stand: **#656 (nit batch) — merged ✅** (all 14 checks passed). #386/#387/#388 fixed, #389 closed won't-fix, tracker + epic updated. **#655 (severity-rank single-source) — PR [#657](https://github.com/TheurgicDuke771/DataQ/pull/657) open, CI running.** Introduced one canonical `db.models.SEVERITY_RANK` and pointed `dedup`, `builder`, `run_service`, and `FAILING_TIERS` at it (eliminating the three independent copies the #656 review found); dashboard-service weights documented as deliberately separate. Full local suite green (1443 passed), Black/Ruff/mypy/Bandit clean, behavior-preserving. Backend/frontend/Playwright checks are the last ones pending — I'm watching them and will merge if green, per the flow you set. I'll report back when CI resolves.

[TOOL]: <task-notification> <task-id>bhw0axqrl</task-id> <tool-use-id>REDACTED</tool-use-id> <output-file>/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/a3727956-2f45-4568-acf0-1b48d135449c/tasks/bhw0axqrl.output</output-file> <status>completed</status> <summary>Background command "Watch #657 CI to completion" completed (exit code 0)</summary> </task-notification>

[AGENT]: CI completed with exit 0 (all checks passed). Let me confirm and merge.

[AGENT]: The `--watch` exit was misleading — **Frontend tests failed**, and the merge was correctly blocked (the hook's "PR merged" message is a false trigger; #657 is NOT merged). My #655 change is backend-only Python, so a frontend-test failure is almost certainly a flake. Let me confirm.

[AGENT]: Confirmed: the only failure is `SchedulesPanel.test.tsx > deletes a schedule after confirmation` → **"Test timed out in 5000ms"** (371 passed, 1 timed out). My #655 change is backend-only Python — this is a frontend CI flake, same class as the known flakes #640/#573/#604. Let me check for an existing issue, then re-run the job.

[AGENT]: It's the already-tracked flake **#573** (SchedulesPanel antd Popconfirm timing under jsdom) — unrelated to my backend-only change. Let me re-run the failed job.

[AGENT]: Re-run triggered. Let me watch it to completion.

[AGENT]: Re-run is in progress — I'm watching it. Given the last `--watch` exit code was unreliable, I'll re-verify the check states explicitly before merging when it completes. Status recap while it runs: - **#657** is sound — the sole failure was the **known flake #573** (SchedulesPanel timeout), not my backend-only change. Re-run triggered. - Once green, I'll squash-merge, then update the tracker for #655 (the merge was blocked earlier so the tracker refresh for it is still pending). I'll report back when the re-run resolves.

[TOOL]: <task-notification> <task-id>bmf000d59</task-id> <tool-use-id>REDACTED</tool-use-id> <output-file>/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/a3727956-2f45-4568-acf0-1b48d135449c/tasks/bmf000d59.output</output-file> <status>completed</status> <summary>Background command "Watch #657 re-run to completion" completed (exit code 0)</summary> </task-notification>

[AGENT]: Watch completed. Let me explicitly verify all checks are green (not trusting the watch exit code) before merging.

[AGENT]: All green now. Merging #657.

[AGENT]: Merge still blocked despite green checks — the hook's "PR merged" is again a false trigger (it did **not** merge). Let me diagnose the mergeability state.

[AGENT]: `MERGEABLE` but `BLOCKED` — a required status check isn't registering as satisfied to branch protection (often a lag after a re-run, or a required context that didn't re-report). Let me compare the required contexts against the head-SHA check conclusions via the API.

[AGENT]: All 14 check-runs are `success` on the head SHA, and the repo uses rulesets (not classic protection). This looks like a post-re-run mergeability lag. Let me check the ruleset's required checks and retry after a brief wait.

[AGENT]: Still BLOCKED. Let me inspect the ruleset's required-check rule to find the mismatch.

[AGENT]: All 12 required checks are green. There's a `pull_request` rule — let me see what it requires (review count / conversation resolution).

[AGENT]: Found it: the ruleset has **`required_review_thread_resolution: true`**, and #657 has an unresolved `COMMENTED` review thread. Let me find it.

[AGENT]: The user's message pins it exactly. The merge is blocked by a **CodeQL alert** — `py/unused-global-variable` on `backend/app/db/models.py:42` — posted as an unresolved review thread by the advanced-security bot, and the ruleset has `required_review_thread_resolution: true`. This is a **false positive**: `SEVERITY_RANK` *is* used — imported by `base.py`, `dedup.py`, `builder.py`, and `run_service.py`. CodeQL flags it because it has no use *within* `models.py` itself (unlike the other constants there, e.g. `ALERT_ON_POLICIES`, which are referenced by in-file `CheckConstraint`s). Rather than dismiss a required security check (which the repo clearly gates on) or invert the layering to satisfy the tool, the clean fix is to give `SEVERITY_RANK` a genuine, valuable use inside `models.py` — a module-level invariant that its keys are real severity tiers. Let me first check the exact alert and confirm no services-import-alerting precedent, then decide between the in-file-use fix vs. dismissal.

[AGENT]: No service imports alerting — so keeping the constant in `db.models` is right (no inversion). The cleanest fix that gives `SEVERITY_RANK` a genuine in-file use *and* improves the design: **move `FAILING_TIERS` into `db.models` too** (derived from `SEVERITY_RANK`), consolidating the whole severity vocabulary in one place. That makes `SEVERITY_RANK` used in-file (CodeQL clean, legitimately) and needs no dismissal. Let me map all `FAILING_TIERS` references first.

[AGENT]: Clean and contained. Let me implement — first add `FAILING_TIERS` to `db.models` (giving `SEVERITY_RANK` an in-file use):

[AGENT]: Now update `base.py` to import `FAILING_TIERS` from models (removing its local definition):

[AGENT]: The formatter touched base.py — let me verify it and check the import ordering is clean.

[AGENT]: base.py is clean. Now point the db-level test at the canonical `db.models` for `FAILING_TIERS`:

[AGENT]: Let me update the test comment and add a re-export check (also covers base.py's re-export line):

[AGENT]: Now run ruff --fix, black, mypy, and the affected tests:

[AGENT]: N811 — alias must be uppercase for a constant. Let me fix:

[AGENT]: Ruff and mypy clean. Now run the affected tests plus a broad sweep to confirm the `FAILING_TIERS` move didn't break anything:

[AGENT]: Full suite green (1444 passed). Committing as a fixup on the open PR and pushing (per the in-review fixup convention):

[AGENT]: Pushed. CI will re-run on the new commit; the CodeQL alert should clear now that `SEVERITY_RANK` has an in-file use. Let me watch the new run, then verify mergeability explicitly.

[AGENT]: Let me update tracking while CI runs.

[AGENT]: The fixup is pushed and CI is re-running on the new commit. Quick summary of the merge-block resolution: **Root cause:** #657's merge was blocked by the ruleset's `required_review_thread_resolution` — CodeQL's `py/unused-global-variable` flagged `SEVERITY_RANK` at `db.models.py:42` (posted as an unresolved bot review thread). A **false positive**: the constant is used, just only cross-module (unlike siblings like `ALERT_ON_POLICIES` that also have in-file `CheckConstraint` uses). **Fix (not a dismissal):** moved `FAILING_TIERS` into `db.models` too, derived as `tuple(SEVERITY_RANK)`. Now `SEVERITY_RANK` has a genuine in-file use, CodeQL is satisfied legitimately, and the whole severity vocabulary lives in one place — a cleaner outcome than suppressing the alert or inverting the layering (no service imports alerting). `alerting.base` re-exports `FAILING_TIERS` with an explicit `__all__`. Full suite green (1444 passed), Ruff/Black/mypy clean. I'm watching the re-run and will verify the CodeQL alert clears + the thread resolves, then merge and finish the #655 tracker update. I'll report back when it resolves.

[TOOL]: <task-notification> <task-id>bffib79kp</task-id> <tool-use-id>toolu_01XtmdZ6xDCnnnw4BE4CfnzX</tool-use-id> <output-file>/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/a3727956-2f45-4568-acf0-1b48d135449c/tasks/bffib79kp.output</output-file> <status>completed</status> <summary>Background command "Watch #657 CI on the fixup commit" completed (exit code 0)</summary> </task-notification>

[AGENT]: Watch done. Let me explicitly verify checks, mergeability, and that the CodeQL alert/thread cleared before merging.

[AGENT]: Checks are green but still `BLOCKED` — the CodeQL alert is fixed, but the bot's **review threads from the earlier commit persist as unresolved** (2 of them), and the ruleset requires thread resolution. Let me inspect them, then resolve via GraphQL.

[AGENT]: The fixup just moved the false positive down a level: `SEVERITY_RANK` is now used in-file (good, its alert is fixed), but `FAILING_TIERS` in models is now the terminal constant with only cross-module consumers, so CodeQL flags *it*. This is whack-a-mole — **any** pure severity constant in `db.models` trips `py/unused-global-variable` because the default CodeQL setup doesn't resolve this repo's `backend.app.*` cross-module imports (the other model constants escape only because they have in-file `CheckConstraint` uses). So the honest classification is: these are genuine **false positives**. The only zero-dismissal alternative is a services→alerting layering inversion, which is a worse permanent smell than dismissing a tool false-positive. Let me get the alert numbers and dismiss properly, then resolve the threads (required by the ruleset).

[AGENT]: The alerts are PR-diff alerts (not in the base-branch list). Before resorting to dismissal, there's actually a *legitimate zero-dismissal* fix I overlooked: give **both** constants a real in-file use in `db.models` via a shared `worst_severity()` helper — which also consolidates the duplicated worst-severity logic in `builder` and `run_service` (squarely #655's goal). Let me check the current consumers to wire it up.

[AGENT]: This is the right fix — a shared `worst_severity()` in `db.models` uses **both** constants in-file (killing the CodeQL false positive legitimately) and removes the duplicated worst-severity logic in `builder` and `run_service`. Let me implement. First the models helper:

[AGENT]: Now add the `worst_severity` helper after `FAILING_TIERS`:

[AGENT]: Now update builder.py to use the shared helper:

[AGENT]: Now run_service.py — replace the inline worst-loop with the shared helper:

[AGENT]: Need to add `worst_severity` to run_service's import:

[AGENT]: Let me add a test for the new `worst_severity` helper, then run the gate:

[AGENT]: Clean. Now run the affected tests + full suite:

[AGENT]: Two builder tests reference the removed `builder._worst_severity`. Let me look at them:

[AGENT]: These two tests directly exercised the removed `builder._worst_severity`; that logic (and its coverage) now lives in `models.worst_severity` / `test_severity_rank.py`. Let me remove the stale duplicates:

[AGENT]: Let me verify `builder` isn't now an unused import in test_builder.py and re-run:

[AGENT]: `builder` still used, ruff clean. Now re-run the full suite:

[AGENT]: Full suite green (1443 passed). Bandit + coverage spot-check, then commit the fixup:

[AGENT]: Let me confirm the changed `check_outcome_counts` region is covered under the full suite (the subset above under-reports run_service):

[AGENT]: Under the full suite: models.py **100%**, builder.py **100%**, run_service.py 99% (the one miss, line 561, is unrelated pre-existing). Committing the fixup and pushing:

[AGENT]: Pushed. Now CI re-runs — the key question is whether CodeQL finds the `models.py` alerts fixed (both constants now used in-file) and whether the old review threads auto-resolve. Let me watch, then verify.

[AGENT]: Fixup pushed; watching CI. Quick status for you: **The CodeQL block turned out to be whack-a-mole** — moving `FAILING_TIERS` into `db.models` just shifted the false positive onto `FAILING_TIERS` (any pure severity constant there trips `py/unused-global-variable`, because the default CodeQL setup doesn't resolve this repo's `backend.app.*` cross-module imports; sibling constants escape only via their in-file `CheckConstraint` uses). **Resolved it legitimately (no dismissal, no layering inversion):** added a shared `worst_severity(statuses)` helper in `db.models` that uses **both** `FAILING_TIERS` and `SEVERITY_RANK` in-file, and routed `builder` + `run_service` through it — which also deletes their duplicated worst-severity loops (exactly #655's intent). Full suite green (1443 passed), 100% coverage on `models.py`/`builder.py`, Ruff/Black/mypy/Bandit clean. Once CI passes I'll verify no CodeQL alerts remain and resolve any lingering (now-fixed) bot threads before merging. Back shortly.

[TOOL]: <task-notification> <task-id>b17974nei</task-id> <tool-use-id>toolu_01CVofvSV31VX5Xc4i3gwjXa</tool-use-id> <output-file>/private/tmp/claude-501/-Users-arijit-Coding-Python-DataQ/a3727956-2f45-4568-acf0-1b48d135449c/tasks/b17974nei.output</output-file> <status>completed</status> <summary>Background command "Watch #657 CI on second fixup" completed (exit code 0)</summary> </task-notification>

[AGENT]: Watch done. Let me verify checks, CodeQL alerts, and merge state.

[AGENT]: `mergeStateStatus: CLEAN` — the fixed alerts marked the old threads outdated, satisfying the ruleset. Merging.

[AGENT]: #657 merged. Let me sync main and update the tracker for #655.

[AGENT]: #655 merged; open issues now 65. Let me refresh the tracker snapshot (66→65) and note #655's completion.

[AGENT]: This tracker refresh needs a PR (main is protected). #655 was a post-planning follow-up, so it's not in the epic checklist — no epic change needed. Let me ship the one-line snapshot update as a small docs PR.

[AGENT]: Let me enable auto-merge on the docs PR so it lands when CI passes, then I'll checkpoint with you.

[AGENT]: Everything's in flight cleanly. Let me confirm the docs PR auto-merge is armed, then checkpoint with you.

[AGENT]: Done with the alert-nit work. Here's the checkpoint: ## Shipped this session | Item | PR | State | |---|---|---| | **#386** dedup severity single-source | [#656](https://github.com/TheurgicDuke771/DataQ/pull/656) | ✅ merged | | **#387** suppression guard on operationally-failed runs | [#656](https://github.com/TheurgicDuke771/DataQ/pull/656) | ✅ merged | | **#388** `alert_on` drift-guard | [#656](https://github.com/TheurgicDuke771/DataQ/pull/656) | ✅ merged | | **#389** channel-neutral rename | — | ✅ closed won't-fix (overtaken by Slack/email publishers) | | **#655** converge the 3 severity-rank maps | [#657](https://github.com/TheurgicDuke771/DataQ/pull/657) | ✅ merged | | tracker snapshot refresh | [#658](https://github.com/TheurgicDuke771/DataQ/pull/658) | 🟡 auto-merge armed, lands on CI green | **#655 highlight:** one canonical `db.models.SEVERITY_RANK` + `FAILING_TIERS` + a shared `worst_severity()` helper now back dedup, the RunReport builder, run-outcome rollups, and the alerting failing-tier set — eliminating three duplicated rank maps and two worst-severity loops. **Notable detour:** #657's merge was blocked by a CodeQL `py/unused-global-variable` false positive (the default setup doesn't resolve this repo's `backend.app.*` cross-module imports). Rather than dismiss the security finding or invert the layering, I gave both constants a genuine in-file use via the `worst_severity()` helper — which also removed real duplication. Resolved legitimately, no dismissals. ## What's left in the alert bucket Only **#416** — enrich Slack/email alerts (deep […]