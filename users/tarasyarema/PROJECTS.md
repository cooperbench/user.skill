# PROJECTS — tarasyarema

## desplega-ai/agent-swarm ★ DOMINANT (100% of sessions)

**What he does here:** Builds, extends, and maintains the core agent-swarm platform. Every session in the dataset is on this repo.

**Tech stack:**
- Runtime: Bun (TypeScript)
- Database: SQLite via `bun:sqlite`, migration-based schema evolution
- HTTP: custom vanilla HTTP server (`src/http/`), no framework
- AI harness: Claude Code (90% of runs), OpenCode/pi-mono (10%)
- Protocol: MCP (Model Context Protocol) for tool exposure
- Containerization: Docker, docker-compose, `Dockerfile.worker`
- Lint/Format: Biome
- Testing: `bun test`
- Monorepo structure with worktrees per feature branch

**Architecture (as of March 2026):**
- `src/commands/runner.ts` — main agent execution loop (~2300 lines)
- `src/commands/worker.ts` — thin worker role wrapper
- `src/be/db.ts` — all SQLite CRUD, singleton db, migration runner
- `src/be/migrations/` — numbered SQL migration files
- `src/http/` — vanilla HTTP routing (tasks, workflows, webhooks, OAuth)
- `src/workflows/` — DAG-based workflow engine (BFS walker, retry poller, resume logic, triggers, event bus)
- `src/workflows/executors/` — typed node executors (PropertyMatch, CodeMatch, Notify, RawLlm, Script, Vcs, Validate, AgentTask)
- `src/providers/` — pluggable AI provider adapters (claude, pi-mono, planned: codex)
- `src/tools/` — MCP tool registrations
- `src/scheduler/` — cron/interval task scheduler
- `src/linear/` — Linear project tracker integration (OAuth, webhook sync, outbound activities)
- `src/github/`, `src/gitlab/` — VCS webhook handlers
- `src/slack/`, `src/agentmail/` — message-origin integrations
- `src/tracker/` — generic tracker abstraction (in progress)
- `new-ui/` — React dashboard UI (separate sub-project)
- `thoughts/taras/` — personal research and plan documents
- `thoughts/shared/` — shared research documents
- `.humanlayer/tasks/` — task definitions for HumanLayer integration

**Recurring themes:**
- Workflow engine redesign — moved from simple node switch to typed executor registry
- Linear integration — OAuth, AgentSession lifecycle, bidirectional sync
- Task working directory (`dir` field) propagation across all task creation paths
- Provider abstraction for harness (Claude → pi-mono → Codex)
- Docker Dockerfile optimization (layer consolidation, npm cache, runtime vs build-time plugin installs)
- Structured output / output schema validation on workflow steps
- E2E test scripts using Docker (lead + worker containers + API)
- One-time scheduled tasks (vs recurring cron)
- Worktree-per-branch development pattern

**Notable branches observed:**
- `2026-03-06-taras/build-swarm-automation-workflow-engine-with-nodes`
- `2026-03-10-feat-task-working-dir`
- `2026-03-11-feat/codex-support`
- `2026-03-18-linear` → `linear-integration-foundation` (PR #161)
- `2026-03-18-feat/workflow-redesign`
- `2026-03-20-refactor-2026-03-20-workflows`

**File naming conventions:**
- Plans: `thoughts/taras/plans/YYYY-MM-DD-topic.md`
- Research: `thoughts/taras/research/YYYY-MM-DD-topic.md`
- Migrations: `src/be/migrations/NNN_description.sql`
- Tests: `src/tests/feature-name.test.ts`
