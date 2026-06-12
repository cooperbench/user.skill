# Projects

## entireio/cli ★ DOMINANT (100% of sessions)

**What it is:** A Go CLI tool that wraps AI coding agents (Claude Code, Gemini CLI, OpenCode) with session tracking, git hook infrastructure, checkpoint management, shadow branches, and attribution. Think of it as an observability + rewind layer on top of AI pair-programming sessions.

**What Soph does here:**
- Implements and refines agent hook handlers (`hooks_claudecode_handlers.go`, `hooks_geminicli_handlers.go`) — the lifecycle events that fire on session start/stop, tool use, git commits.
- Maintains the session state machine (`session/phase.go`, `session/state.go`) with phases like IDLE, ACTIVE, ENDED and transitions triggered by events.
- Works on checkpoint and trail stores — git-based storage of session metadata on an orphan branch (`entire/checkpoints/v1`).
- Builds attribution algorithms (`manual_commit_attribution.go`) that calculate what percentage of a commit was agent-written vs. human-written.
- Handles multi-agent support — adding Gemini CLI and OpenCode alongside the existing Claude Code integration.
- Manages the `entire enable`/`entire disable`/`entire resume`/`entire status` user-facing commands.
- Writes integration and E2E tests; runs `mise run test:ci`.
- Cuts releases and maintains `CHANGELOG.md`.

**Recurring themes:**
- Shadow branch architecture (one orphan branch per base commit, carries session metadata and diffs)
- Session ID stability across agent restarts and date changes
- Concurrent session handling (multiple agents per commit)
- Backward compatibility with old session formats
- Performance: O(n) → O(depth) tree operations in checkpoint/trail stores
- Secret redaction in condensed transcripts

**Tech stack:** Go 1.2x, `go-git`, `cobra` CLI, GitHub Actions, `mise` task runner, structured logging via `slog`.

**Codebase paths Soph references frequently:**
- `cmd/entire/cli/` — main CLI commands
- `cmd/entire/cli/session/` — session state machine
- `cmd/entire/cli/checkpoint/` — checkpoint store
- `cmd/entire/cli/trail/` — trail store
- `cmd/entire/cli/summarize/` — transcript condensation
- `cmd/entire/cli/integration_test/` — integration tests
- `cmd/entire/cli/e2e_test/` — E2E tests
- `/Users/soph/Work/entire/devenv/` — local dev environment
- `/Users/soph/Work/entire/test/` — local test repos
