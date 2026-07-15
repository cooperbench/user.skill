> DEVELOPER

sequant run output is'nt well designed. Shouldn't have this been tackled in past issues?

> DEVELOPER

sequant run output is'nt well designed. Shouldn't have this been tackled in past issues?

> DEVELOPER

sequant run output is'nt well designed. Shouldn't have this been tackled in past issues? (base) tony@Tambras-MacBook-Air sequant % npx sequant run 610 606 --phases exec,qa SEQUANT WORKFLOW Stack generic Phases exec → qa Mode parallel (concurrency: 3) Logging JSON State enabled Issues #610, #606 Worktree isolation: enabled Base branch: main State reconciled: #533, #551, #555, #568, #570, #580, #581, #583, #585, #587, #596, #597 → merged Preparing worktrees from main... Worktrees: 2 created, 0 reused ▸ #610 exec ▸ #606 exec ^C ! Received SIGINT, shutting down gracefully... ✓ Aborted 2 active phases ✓ Cleanup worktree for #606 ✓ Cleanup worktree for #610 ✓ Finalize run logs Interrupted. Cleanup complete. (base) tony@Tambras-MacBook-Air sequant % npx sequant run 606 --phases exec,qa SEQUANT WORKFLOW Stack generic Phases exec → qa Mode parallel (concurrency: 3) Logging JSON State enabled Issues #606 Worktree isolation: enabled Base branch: main State reconciled: #604, #608 → merged ! #606: already merged — skipping (use --force to re-run) All issues already completed. Use --force to re-run. (base) tony@Tambras-MacBook-Air sequant % npx sequant run 614 -q (base) tony@Tambras-MacBook-Air sequant % (base) tony@Tambras-MacBook-Air sequant % npx sequant run 614 -q SEQUANT WORKFLOW Stack generic Phases auto-detect from labels Mode parallel […]

> AGENT

Good question — let me check before assuming this is new ground.

> AGENT

Yes — there's been significant past work on `sequant run` output, but what you're seeing now looks like a **regression from the most recent fix** rather than untouched ground. **What's been done** - #244 — added animated spinners + elapsed time - #282 — fixed spinner/verbose log interleaving - #403 — surfaced errors in non-verbose mode - #421/#435 — MCP progress notifications - #458 (closed Mar 2026) — fixed parallel-run UX freeze by adding per-phase `▸ #N phase` / `✔ #N phase Xm Ys` lines **What's broken in your output** #458 added a *second* output channel (the `▸` / `✔` per-issue lines) for parallel mode. But it's still firing alongside the original spinner channel even for single-issue runs, and the two collide: ``` ▸ #614 spec ✔ #614 spec 5m 13s ← from #458 ✔ spec (1/3) (5m 12s) ← from original spinner — duplicate ... ▸ #614 exec ✔ #614 exec #614 qa ← BUG: exec ✓ collides with qa ▸, exec duration dropped ✔ #614 qa 2m 57s ``` Two specific issues: 1. **Duplicate output** — `▸ #N phase` + `✔ N (X/3)` both fire for a 1-issue run; the parallel-mode lines should suppress when concurrency-effective == 1, […]