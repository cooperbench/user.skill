---
session_id: b449ad2c-564f-4bad-ab35-e02f4dece6b1
developer: "gh:admarble"
split: train
source: entire
repo: sequant-io/sequant
start_time: "2026-04-02T23:55:04.625705Z"
n_turns: 2
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

what skills do you have from sequant?

> AGENT

Here are the Sequant skills available: | Skill | Description | |-------|-------------| | `/assess` | Issue triage and status assessment — analyze state, detect health signals, recommend next action | | `/spec` | Plan review vs Acceptance Criteria for a GitHub issue, plus issue comment draft | | `/exec` | Implementation loop for a single issue until ACs are satisfied | | `/test` | Browser-based testing for admin features | | `/verify` | Execution verification for CLI/script features — runs commands, captures output | | `/qa` | Code review + QA vs Acceptance Criteria, including A+ suggestions and review comment draft | | `/docs` | Generate admin-facing documentation before merging | | `/fullsolve` | Complete issue resolution: spec → exec → test → qa with auto-fix iterations | | `/merger` | Multi-issue integration and merge for completed worktrees | | `/testgen` | Generate test stubs from /spec verification criteria | | `/loop` | Quality loop — parse test/QA findings and iterate until gates pass | | `/clean` | Repository cleanup | | `/reflect` | Strategic reflection on workflow effectiveness | | `/improve` | Codebase analysis, improvement discovery, issue creation, and execution | | `/security-review` | Deep security analysis for sensitive features | | `/upstream` | Monitor Claude Code releases for breaking changes | | `/setup` | Initialize Sequant in your project | | `/release` | Automates version bump, git tag, GitHub release, and npm publish | The typical workflow is: `/assess` → `/spec` → `/exec` → `/verify` or `/test` → `/qa` → `/docs` → `/merger`. Use `/fullsolve` to run the full pipeline in one shot.
