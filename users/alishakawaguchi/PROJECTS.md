# Projects: alishakawaguchi

## entireio/cli ★ (dominant — 100% of sessions)

**What it is**: A developer-tooling CLI (`entire`) that wraps AI coding agents and provides checkpoint/rewind/explain/commit functionality. It intercepts agent lifecycle hooks (session start, stop, commit) to create atomic checkpoints of code changes.

**What alishakawaguchi does here**: Adds support for new AI coding agents (Factory AI Droid integration was the main thread across observed sessions), writes E2E test infrastructure for those agents, authors Claude Code skill/plugin files for the team, maintains GitHub Actions CI workflows, and cleans up dead code/tests.

**Tech stack**:
- Go (primary language)
- GitHub Actions (CI/CD, E2E matrix runs)
- tmux (interactive E2E test sessions)
- golangci-lint, mise (task runner)
- Claude Code (the agent used for this repo's development)
- Factory AI Droid, Gemini CLI, OpenCode (agents being integrated)

**Recurring themes across sessions**:
- **Factory AI Droid integration** — Implementing `factoryaidroid` agent package, fixing hook input formats, implementing `GetSessionDir`, `ReadSession`/`WriteSession`, `ParseDroidTranscriptFromBytes`, E2E test runner
- **E2E test infrastructure** — Stabilizing flaky interactive E2E tests, unifying test packages (`e2e/agents/`, `e2e/testutil/`, `e2e/tests/`), adding concurrency limits per agent
- **Dead code / test cleanup** — Removing trivial tests that test constants, one-liners, or obvious Go behavior
- **Skill/plugin authoring** — Creating and iterating on `.claude/skills/agent-integration/` skill files for the team
- **CI workflows** — `e2e.yml`, `e2e-isolated.yml`, `e2e-triage.yml` — adding new agents to the matrix, fixing triage output

**Key files/paths referenced**:
- `cmd/entire/cli/agent/factoryaidroid/` — Droid agent package
- `cmd/entire/cli/strategy/manual_commit_condensation.go` — commit condensation logic
- `cmd/entire/cli/e2e_test/` (old) / `e2e/` (new consolidated) — E2E test infrastructure
- `.claude/skills/agent-integration/` — Claude Code skill files
- `.claude/plugins/agent-integration/` — Plugin command wrappers
- `.github/workflows/e2e.yml`, `e2e-triage.yml`, `e2e-isolated.yml`
- `docs/architecture/agent-guide.md`, `docs/architecture/agent-integration-checklist.md`

**Branch pattern**: `alisha/<feature-name>` (e.g., `alisha/factoryai-agent`, `alisha/agent-integration-skill`, `alisha/improve-agent-integration-skill`, `alisha/e2e-triage-ci-job`)
