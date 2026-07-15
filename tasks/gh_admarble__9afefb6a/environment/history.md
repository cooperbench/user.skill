> DEVELOPER

qa 543

> AGENT

Implementation exists in worktree `feature/543-...` with open PR #629. Let me verify state and pull the diff.

> AGENT

CI is green, branch in sync, 8 files / +290/-17. Small enough to review inline (per memory: <600-line diffs).

> AGENT

Tracking review progress as I go.

> AGENT

Continuing the review — reading the remaining changed files.

> AGENT

Now reading batch-executor and run-progress changes.

> AGENT

Now reading the tests added to validate the new behavior.

> AGENT

Reading is enough — running the targeted tests to verify the implementation works.

> AGENT

51 tests pass. Let me check whether the TUI docs were updated to reflect the new activity enrichment.

> AGENT

All checks pass. Posting QA comment to issue #543 (not PR per project convention) with READY_FOR_MERGE.

> AGENT

Posted QA review to #543 and added `ready-for-review` label. ## Verdict: READY_FOR_MERGE PR #629 (commit `ee994bb`) cleanly implements all 4 ACs from #543: - **AC-1** — `nowLine` enriched via new `"activity"` progress event variant (option b's intent, implemented over the in-process agent `onOutput` stream rather than tailing the nonexistent `.sequant/logs/<issue>-<phase>.log` files; honestly documented in PR body). - **AC-2** — `lastActivityAt` advances on every accepted activity ping. - **AC-3** — 100 ms throttle in `phase-executor` keeps re-emit rate ≤10 Hz, matching TUI poll budget. - **AC-4** — `nowLineWithStaleFallback` (declarative, snapshot-time) returns coarse `running <phase>` once `ageMs ≥ 5000`. All 5 CI checks green, 0 commits behind main, lint clean, 51/51 targeted tests pass, no new `any` types, CHANGELOG updated, `experimental-tui-dashboard.md`'s existing example now actually matches runtime behavior (no docs changes needed). One non-blocking note about trailing-edge throttle drop is in the comment as a follow-up suggestion. QA comment posted: https://github.com/sequant-io/sequant/issues/543#issuecomment-4431651037

> DEVELOPER

any gaps?

> AGENT

Adversarial second look — yes, a few. None are blocking but worth naming: 1. **Throttle logic in `phase-executor.ts` has no direct test.** The PR body flagged this and called the wiring "~5 lines." Fair, but it's the mechanism behind AC-3 — if a future refactor drops `lastActivityAtMs`, nothing fails. Mitigating factor: AC-3 is satisfied externally by the TUI's 10 Hz poll rate even if the per-phase throttle is broken (state mutations are cheap). So it's an optimization test, not a correctness test. 2. **`run-progress.ts` activity-filter is also untested.** Two lines (`if (event === "activity") return` in both the renderer and heartbeat branches). If someone deletes them, the non-TUI line renderer would print ~10 log lines/sec during active phases. Cosmetic regression, not a break. A 5-line test would cover both branches. 3. **Trailing-edge throttle drop** (already in the comment). 100ms leading-edge throttle means the last useful output before agent goes idle can be lost — display shows the prior chunk for up to 5s until the coarse fallback kicks in. Real but minor; the 5s fallback masks it. 4. **`extractActivityLine` only strips SGR escapes** (already in the comment). Cursor-movement / OSC sequences would pass through. Almost certainly fine for Claude Code […]