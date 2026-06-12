# Preferences — penso

## Pushback distribution

| Type           | Rate  | What triggers it |
|----------------|-------|-----------------|
| non_pushback   | 53.3% | Agent does the work correctly |
| failure_report | 22.2% | CI/test output shows failures |
| correction     | 20.0% | Agent misses constraints, leaves work incomplete, excuses failures |
| takeover       | 3.3%  | Agent summarizes instead of committing |
| rejection      | 1.1%  | Agent repeatedly fails to complete an action (e.g., GPG signing) |

## What triggers each pushback type

**failure_report** — raw paste of failing test output or CI output, no preamble:
- The agent says "that check was pre-existing, not our fault" → he pastes the next run's failures.
- The agent says "release pushed, CI should pick up the tag" → he pastes the CI failure URL.
- He never explains *what* failed; the raw output is the message.

**correction** — agent misread the requirement or left work incomplete:
- "I like 1 but then it should require only to setup auth, not all the onboarding steps" (narrows scope of agent's proposed option)
- "commit and push main, no need for release" (cuts off agent's elaborate release plan)
- "Look at comments in https://…/pull/389 and solve them" (after agent declares itself done)
- "did you fix all issues? Can you resolve comments then?" (after agent says "done" but PR comments remain)
- "Is that what the entire documentation say? Why do I have this directory?" (questions agent's answer, wants source verification)

**takeover** — agent writes a summary/explanation but doesn't commit:
- "commit, push, create a PR" (issued immediately after agent's summary, no commentary)

**rejection** — "try again" repeated when agent is stuck on GPG/pinentry failures.

## What satisfies him

- Agent implements a spec completely and without compile/lint errors on the first try.
- CI passes after local-validate.
- PR created with correct branch and description.
- PR review comments resolved and marked done.
- He occasionally confirms with brief: `"please yes"`, `"apply the best fix yes"`, `"Yes create it"`.

## Workflow habits

**Planning first, then implement.** For large tasks, penso writes a complete implementation plan *himself* (in Claude Code's plan mode, evidenced by the plan format and the transcript path reference inside one plan). He then pastes the plan as the session opener: `"Implement the following plan: # Plan: …"`. He does not ask the agent to plan for him — he plans, then executes via the agent.

**For small/unclear bugs:** links GitHub issue + "suggest a fix" or "look at the code and plan a fix". Short-form, exploratory delegation.

**Validation cadence:** runs `./scripts/local-validate.sh <PR#>` locally after agent work, pastes full output. Iterates until clean. Then creates PR, reads review comments, asks agent to resolve.

**Commit signing:** uses GPG with YubiKey. Occasionally causes signing failures in headless sessions, which he responds to with "try again" (up to 3×) before pushing manually or accepting unsigned commits.

**Worktree pattern:** maintains one git worktree per feature branch at `~/.superset/worktrees/moltis/<branch>/`. Branch names describe the feature: `soul-location`, `tailscale-redirects`, `stt-401-during-onboarding`, `local-llm-raw-token`, `versioning`, `installation-feedback`.

**Test-driven?** No. Tests appear after implementation (22.2% of pushback is test failures, 2.2% of intent is `test`). He runs tests to validate, not to drive design.

**Explanation preference:** almost never asks for explanation. Occasionally: `"give me a good understanding"` (opening), or `"And what are the comments about this: …"` (follow-up on a quoted passage). But most of the time: no explanation wanted, just action.

**Documentation:** aware enough to say: `"commit and push, add something in CLAUDE.md and AGENTS.md about always making sure documentation is up to date when adding or changing features."` — treats docs as part of the commit.

## Tool/stack preferences

- **Rust** for all backend; multi-crate Cargo workspace
- **`cargo +nightly-2025-11-30 fmt`** for formatting
- **biome** for JS/TS linting
- **`./scripts/local-validate.sh <PR#>`** as the local CI gate (runs fmt, lint, i18n, zizmor, tests)
- **GitHub PRs** as the unit of change; reviews from greptile and Codex bots addressed
- **Tailscale** for remote access, **Docker** for sandboxing
- **`entire`** for checkpoint/context tracking (`.entire/` directory in repo)
- **date-based versioning** (YYYYMMDD.NN) over semver for releases
