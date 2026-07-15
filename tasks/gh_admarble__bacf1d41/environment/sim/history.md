[DEVELOPER]: qa 543

[AGENT]: Implementation exists in worktree `feature/543-...` with open PR #629. Let me verify state and pull the diff.

[AGENT]: CI is green, branch in sync, 8 files / +290/-17. Small enough to review inline (per memory: <600-line diffs).

[AGENT]: Tracking review progress as I go.

[AGENT]: Continuing the review — reading the remaining changed files.

[AGENT]: Now reading batch-executor and run-progress changes.

[AGENT]: Now reading the tests added to validate the new behavior.

[AGENT]: Reading is enough — running the targeted tests to verify the implementation works.

[AGENT]: 51 tests pass. Let me check whether the TUI docs were updated to reflect the new activity enrichment.

[AGENT]: All checks pass. Posting QA comment to issue #543 (not PR per project convention) with READY_FOR_MERGE.

[AGENT]: Posted QA review to #543 and added `ready-for-review` label. ## Verdict: READY_FOR_MERGE PR #629 (commit `ee994bb`) cleanly implements all 4 ACs from #543: - **AC-1** — `nowLine` enriched via new `"activity"` progress event variant (option b's intent, implemented over the in-process agent `onOutput` stream rather than tailing the nonexistent `.sequant/logs/<issue>-<phase>.log` files; honestly documented in PR body). - **AC-2** — `lastActivityAt` advances on every accepted activity ping. - **AC-3** — 100 ms throttle in `phase-executor` keeps re-emit rate ≤10 Hz, matching TUI poll budget. - **AC-4** — `nowLineWithStaleFallback` (declarative, snapshot-time) returns coarse `running <phase>` once `ageMs ≥ 5000`. All 5 CI checks green, 0 commits behind main, lint clean, 51/51 targeted tests pass, no new `any` types, CHANGELOG updated, `experimental-tui-dashboard.md`'s existing example now actually matches runtime behavior (no docs changes needed). One non-blocking note about trailing-edge throttle drop is in the comment as a follow-up suggestion. QA comment posted: https://github.com/sequant-io/sequant/issues/543#issuecomment-4431651037