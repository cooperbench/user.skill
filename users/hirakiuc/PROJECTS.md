# Projects: hirakiuc

## hirakiuc/gh-orbit [DOMINANT — 100% of sessions]

**What it is**: A GitHub CLI extension (`gh orbit`) that provides a TUI dashboard for
monitoring GitHub activity (repositories, issues, PRs). Local-first, SQLite-backed,
zero-config.

**Tech stack**:
- Language: Go (CGO-free)
- TUI: bubbletea v2, bubbles, lipgloss
- Storage: SQLite via `modernc.org/sqlite` in WAL mode with foreign keys
- Observability: `go.opentelemetry.io/otel`
- Auth: inherited from `gh` host environment (zero-config)
- Testing: testify (assert + require)
- Build: Makefile (`make build test lint`, `make generate test lint`)
- CI: GitHub Actions (hirakiuc monitors CI and reports failures)

**Architecture principles** (from AGENTS.md):
- Interface-based dependency injection
- Context hygiene: `ctx context.Context` always first arg, never stored in structs
- Hardened SQLite: WAL mode + foreign keys
- Observability on every action

**Agent workflow**:
- Topic branch per feature/fix → commits → PR → hirakiuc reviews → merges → pulls main
- Implementation follows `.agent/implementation_plan.md` roadmap
- Code review feedback delivered via `.agent/feedback.md`
- Agent must run `make build test lint` to baseline before starting, and
  `make generate test lint` after changes
- Agent must run `gh orbit doctor` to verify environment health

**Recurring themes in sessions**:
- Refactoring based on code review feedback (dominant pattern)
- Bubble Tea v2 migration challenges (key event simulation, interface changes)
- Git workflow enforcement (topic branches, PRs)
- CI failure investigation and remediation
- Understanding project state before each session via @AGENTS.md + @GEMINI.md
