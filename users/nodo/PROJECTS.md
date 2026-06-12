# Projects: nodo

## entireio/cli (dominant — 86.7% of sessions)

**What nodo does here**: Builds and maintains the core CLI for the `entireio` product. During the observed period (2026-03-04 to 2026-03-06), work is almost entirely focused on an **external agent plugin protocol** — a mechanism for third-party AI coding agent binaries to integrate with the CLI via PATH discovery and stdin/stdout JSON communication.

**Tech stack**: Go, cobra, golangci-lint, `exec.CommandContext`, JSON protocol over subprocess stdin/stdout

**Architecture (inferred from prompts)**:
- `cmd/entire/cli/agent/` — agent interface and built-in agent implementations (Claude Code, Cursor, Gemini CLI, OpenCode, Factory AI Droid)
- `cmd/entire/cli/agent/external/` — external agent adapter: discovers `entire-agent-<name>` binaries from `$PATH`, communicates via subcommands
- `cmd/entire/cli/strategy/` — git hook strategies (e.g., `manual_commit_hooks.go`)
- `docs/architecture/` — protocol specs, e.g., `external-agent-protocol.md`
- `docs/requirements/external-plugins/` — iterative code review files (`review-01.md`, `review-02.md`, `review-03.md`)
- `hooks_cmd.go` — CLI hook command tree, subject of discovery timing debates

**Recurring themes**:
- Adding `CapabilityDeclarer` interface + `As*` helper functions to replace combinatorial wrapper types
- External agent protocol completeness (all required subcommands implemented, capabilities correctly surfaced)
- Deferring `DiscoverAndRegister` from startup to lazy execution
- Context deadline propagation (hung external binaries blocking CLI)
- Consistency with codebase patterns (`strings.TrimSpace`, `As*` helpers instead of direct type assertions)
- PR review loop: triggering review agents, tracking outstanding issues across review iterations

**Cursor extraction saga**: briefly attempted to extract the Cursor agent into an external binary (`entire-agent-cursor`), then fully reverted when it turned out wrong — "Undo the changes to migrate cursor to an external agent."

---

## entireio/roger-roger (13.3% of sessions)

**What nodo does here**: Uses the `Roger Roger Agent` (a different AI agent UI/product in the `entireio` ecosystem). Prompts in this repo are minimal — the `/reviewer` command invocation is the only observed opening. Likely a supporting product rather than the primary development target during this period.

**Tech stack**: Unknown — insufficient prompt evidence.
