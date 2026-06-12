# PROJECTS

## entireio/cli (dominant — 100% of sessions)

**What it is**: A Go CLI tool called `entire` that manages AI coding session checkpoints, integrates with git, and enables resuming sessions from saved states. The product is `entire.io`, a developer tool for AI-assisted coding workflows.

**What pfleidi does here**: Core development — adding features, refactoring, debugging, reviewing. He is one of the primary authors (inferred). He uses Claude Code to implement most code while steering architecture and quality.

**Tech stack**:
- Language: Go (100%)
- CLI framework: Cobra
- VCS integration: git (metadata branches, trailers, squash merges, worktrees)
- Testing: Go test suite with unit tests and e2e tests; e2e tests are expensive (one strategy package takes 34.6s)
- CI: tests must pass before merging (`go test ./...`, `go build ./...`)
- PR workflow: GitHub PRs via `gh pr create`, squash-merge to main
- Linting: nolint annotations with required rationale comments

**Recurring themes / active work areas**:
- **Checkpoint resume**: `entire resume` command, squash-merge support, ordering checkpoints by timestamp
- **Context propagation**: Threading `context.Context` through ~108 files (a large refactoring branch `improve-context-management`)
- **Performance observability**: Hand-rolled `perf` package for measuring hook and lifecycle latencies, writing spans to a logging context
- **Code review automation**: Multi-agent code review dispatched via subagent-driven-development skill; reviews are scoped to branch changes
- **Session display**: Formatting and displaying restored sessions, deduplication logic

**Key packages** (inferred from prompts):
- `cmd/entire/cli/` — CLI entry points (resume.go, explain.go, lifecycle.go, setup.go, etc.)
- `cmd/entire/cli/strategy/` — Strategy interface and implementations (manual_commit, auto_commit)
- `cmd/entire/cli/checkpoint/` — Checkpoint storage and metadata
- `cmd/entire/cli/session/` — Session state and phase management
- `cmd/entire/cli/agent/` — Agent interface (claudecode, geminicli, opencode)
- `perf/` — Performance tracing package (root of repo, importable as `github.com/entireio/cli/perf`)
- `cmd/entire/cli/paths/` — Repo root detection with caching
- `cmd/entire/cli/settings/` — Settings load/save
- `e2e/` — End-to-end tests

**Notes**:
- Plans live in `docs/plans/YYYY-MM-DD-feature.md` but are NOT version-controlled (not committed)
- Design docs live in `docs/requirements/` and follow a specific frontmatter template (title, state, author, date, tags)
- An `ephemera` repo at `github.com/entirehq/ephemera` is used for prototypes
