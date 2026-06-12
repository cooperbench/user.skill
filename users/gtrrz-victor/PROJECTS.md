---
name: gtrrz-victor-projects
description: Repositories and recurring work themes for gtrrz-victor
---

# Projects

## entireio/cli ★ (dominant — 100% of sessions)

**What it is**: A Go CLI tool called `entire` that hooks into AI agent runtimes (Claude Code, Gemini CLI, Cursor, OpenCode, OpenClaw) and creates git checkpoints automatically during coding sessions. Checkpoints live on shadow branches (`entire/<commit-hash[:7]>`) and a sessions metadata branch (`entire/sessions`). Users can rewind, explain, and replay their AI session history.

**Tech stack**:
- Go (primary) — Cobra CLI framework, `go-git`, `bufio`, `syscall`, standard library
- TypeScript — e2e tests (Vitest + Anthropic Agent SDK), hook handlers for OpenClaw and OpenCode
- `mise` — task runner (`mise run fmt`, `mise run lint`, `mise run test:ci`, `mise run test:e2e`)
- GoReleaser Pro — release pipeline with Homebrew tap (`entirehq/tap/entire`)
- PostHog — async analytics via detached subprocess
- Linear — issue tracking (e.g., ENT-109)

**Package layout** (inferred from prompts):
- `cmd/entire/cli/` — root, setup, status, doctor, explain, rewind, reset commands
- `cmd/entire/cli/strategy/` — manual-commit strategy (the only one now; auto-commit was removed)
- `cmd/entire/cli/checkpoint/` — checkpoint storage, committed.go, metadata structs
- `cmd/entire/cli/session/` — session state files in `.git/entire-sessions/`
- `cmd/entire/cli/agent/` — agent registry + per-agent packages: claudecode/, gemini/, cursor/, opencode/, openclaw/
- `cmd/entire/cli/transcript/` — shared JSONL parser
- `cmd/entire/cli/telemetry/` — PostHog async detached subprocess
- `cmd/entire/cli/versioncheck/` — version update notifications
- `cmd/entire/cli/settings/` — settings files (.entire/settings.json)
- `cmd/entire/cli/buildinfo/` — Version and Commit vars for ldflags
- `e2e/` — TypeScript end-to-end tests

**Recurring themes**:
- Refactoring backward-compat code after features stabilize (agent type tracking, session ID format, checkpoint storage format, strategies consolidation)
- Adding new agent integrations (OpenCode, OpenClaw, Cursor TranscriptAnalyzer)
- Checkpoint storage format evolution: flat → versioned subdirectories, map → array Sessions
- Token usage tracking per session
- PostHog telemetry with opt-in consent
- Version check notifications (brew update)
- `entire explain` UX improvements (listing checkpoints, temporary vs committed)
- Shadow branch design (suffixes → single branch with reset-on-overlap)
- Session ID format (date-prefix → direct agent UUID)
- GoReleaser + GitHub App for Homebrew tap automation
