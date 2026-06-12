# Projects: khaong

## entireio/cli ★ (dominant repo — 100% of sessions)

**What it is:** Entire CLI — a Go command-line tool that wraps git hooks to provide session-aware checkpoint management for AI coding sessions. Hooks integrate with Claude Code, Gemini CLI, and GitHub Copilot CLI. Sessions track transcript lines, token usage, staged files, and commit metadata.

**Tech stack:**
- Go (primary language)
- go-git v5 for git operations (known bug: `worktree.Status()` writes the index)
- `mise` for task running
- GitHub Actions for CI (E2E test matrix across agents)
- `gotestsum` for test reporting
- tmux for interactive E2E session control
- Linear for project management (issue prefix: ENT-)

**What khaong does here:**
- Designs and implements hook handlers for session lifecycle events (start, stop, session-end, pre-compress, post-commit)
- Manages a state machine tracking session phases (IDLE → ACTIVE → ACTIVE_COMMITTED, etc.)
- Debugs git index corruption caused by go-git v5 side effects in worktree contexts
- Writes and debugs E2E tests that spin up real agent sessions in tmux
- Maintains a stacked PR workflow off feature branches (parent: `alex/ent-221-*`)
- Reviews PRs from teammate soph
- Integrates with Linear MCP for issue tracking from within sessions

**Recurring themes:**
- Worktree index corruption (go-git v5 `worktree.Status()` rewriting the index during hooks)
- Session state persistence (`.git/entire-sessions/*.json`)
- Transcript parsing (extracting file changes from agent transcript JSONL)
- Shadow branch lifecycle (temporary "entire/sessions" branches)
- Checkpoint condensation (merging shadow state at commit time)
- E2E test reliability on CI (timing issues, artifact capture, preflight dependency checks)
- Multi-agent support (Claude Code, Gemini CLI, GitHub Copilot CLI, opencode)

**Key internal paths referenced:**
- `cmd/entire/cli/strategy/manual_commit_hooks.go` — manual-commit strategy hook handlers
- `cmd/entire/cli/lifecycle.go` — agent lifecycle dispatcher
- `cmd/entire/cli/session/state.go` — session state struct
- `cmd/entire/cli/logging/logger.go` — structured JSON logging
- `docs/plans/` — written implementation plans khaong references at session start
- `e2e/artifacts/{timestamp}/` — E2E test artifact output
- `.git/entire-sessions/` — runtime session state files
