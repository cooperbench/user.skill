# Projects — squishykid

## entireio/cli (dominant — 100% of sessions)

A Go CLI tool that wraps AI coding agents (Claude Code, Gemini CLI, Cursor) with git-based session checkpointing, hook management, and transcript parsing. squishykid is a core maintainer or founder — they know every subsystem and drive the architectural cleanup.

### Subsystems touched in sessions

- **Strategy layer** (`cmd/entire/cli/strategy/`): `manual_commit_session.go`, `auto_commit.go`, `common.go`, `strategy.go`. Handles git session initialization, empty-repo detection, hook manager detection.
- **Hook handlers** (`cmd/entire/cli/hooks_claudecode_handlers.go`, `hooks_geminicli_handers.go`): Per-agent hook wiring. squishykid caught that a change applied to Claude Code handlers also needed to apply to the Gemini CLI handler.
- **Agent interface** (`cmd/entire/cli/agent/`): `agent.go` interface, `claudecode/claude.go`, `geminicli/gemini.go`. Ongoing refactor to move methods between `Agent` and `HookSupport` interfaces, remove dead code (`GetHookConfigPath`, `ParseHookInput`, `SupportsHooks`, `HookHandler`).
- **Transcript parsing** (`cmd/entire/cli/agent/claudecode/`): `transcript_test.go`, `extractUserPrompts` — extended to support Cursor transcripts.
- **Docs**: Updated docs for new agent support (Cursor) using PR 478 as a template.
- **Setup/enable flow** (`cmd/entire/cli/setup.go`): Hook manager detection and warning during `entire enable`.

### Tech stack

- Go (entire codebase)
- `go-git` for git operations (plumbing layer)
- GitHub Actions for CI/e2e tests
- External hook managers: Husky, Lefthook, pre-commit, Overcommit

### Recurring themes

- Dead code removal (interfaces, methods never called in production)
- Go visibility hygiene (exported vs. unexported symbols)
- Test helper deduplication
- Stacked PRs with `rwr/` branches targeting each other
- Hook manager ecosystem compatibility
