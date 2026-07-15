> AGENT

Reading the relevant files to understand the current state before searching for prior sessions.

> AGENT

Now let me check what's in `.agents/skills`.

> AGENT

Entire Recall: --- ## What the three files record **`backlog.md`** — 7 pending enforcement gates, all from 2026-06-22 swarmforge pipeline runs. Each is a recurring failure pattern that hasn't been codified yet: - GPG signing silently fails in agent worktrees → add `--no-gpg-sign` - `entire session current` returns stale/wrong worktree → verify `worktree_path` matches `$PWD` - f-string escaping confusion when generating code with f-strings - auto-mode classifier blocks `git reset --hard` and `gh pr merge` for specifier/integrator roles - 7-char git hash used where 10-char is required (4 roles) - CRAP bootstrap invocation confused (`python -m` vs `uv run python -m`) - mutmut targeted re-run semantics misunderstood (no scan/count mode; targeted reruns reset cache) **`ledger-project.md`** — permanent record across 4 pipeline runs (c1 through c4). Promoted items landed in: `AGENTS.md`, `.agents/roles/cleaner.md`, `.agents/roles/curator.md`, `.agents/roles/coder.md`, `.agents/roles/hardender.md`, `.agents/roles/architect.md`, and two new skills (see below). Rejected items are tagged with reason (swarmforge-only, machine-specific, first-occurrence, inferable from code). **`ledger-swarmforge.md`** — prunable log of swarmforge-scoped operational improvements. All `pending`. Items cover role prompt fixes, permission pre-authorization for blocked commands, integrator/specifier workflow tweaks, mutmut run semantics, and the recurring 10-char hash reminder. --- ## What was created in `.agents/skills` Two skills were promoted from second-occurrence failures: ### […]