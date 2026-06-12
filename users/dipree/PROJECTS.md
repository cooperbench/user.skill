---
name: dipree-projects
description: Repo breakdown, tech stack, and recurring themes for dipree.
---

# Projects: dipree

## entireio/cli ★ (dominant — 100% of sessions)

**What it is**: A Go CLI tool (`entire`) that wraps AI agent workflows into git hooks, automating code review, commit metadata, and agent context. Supports Claude Code and Gemini CLI as agents.

**Tech stack**: Go, Cobra (CLI framework), interactive TUI prompts (bubbletea/huh), golangci-lint v2, mise, GitHub Actions CI, shadow git branches for trail data, JSON state files under `.entire/`

**Active features during the session period (2026-02-09 to 2026-03-19)**:

### Wingman (primary focus)
An automated code review loop: after a commit/stop hook, a background process spawns a Claude reviewer that writes suggestions to `.entire/REVIEW.md`, then auto-applies them to the active session. Key files: `wingman.go`, `wingman_review.go`, `wingman_spawn_unix.go`, `hooks.go`, `hooks_claudecode_handlers.go`.

Recurring problems dipree debugged:
- Lock file staleness causing false "Reviewing..." notifications
- Phase check bug (`isSessionIdle` returning false for `PhaseEnded`, blocking auto-apply)
- Stale session state files (`orphaned test.json`) blocking `hasAnyLiveSession`
- REVIEW.md not being picked up after session close
- Hook response JSON format wrong (needed `hookSpecificOutput` nesting)
- Auto-apply triggering a new tab instead of using existing session

### Trails
Branch-scoped metadata stored on a shadow git branch (`entire/trails/v1`). Supports `create`, `update`, `list`, `show`. Interactive create flow: title → branch derived from title → optional checkout flag.

Recurring problems dipree fixed:
- Trail list only showing local, not remote
- Branch not being pushed after trail creation
- `done` and `closed` statuses erroneously selectable
- User attribution showing git name instead of GitHub username
- Automated trail generation code left over after removal

### Enable / onboarding (`entire enable`)
Interactive multi-select for choosing which agents (Claude Code, Gemini CLI) to hook into the repo. Re-runnable — shows current selection state.

Issues dipree caught:
- Deselected agent hooks not being removed on re-run
- Crashing on empty selection instead of showing inline validation message
- `isFullyEnabled()` becoming dead code after refactor

### Hook system
`UserPromptSubmit`, `SessionStart`, `Stop`, `PostCommit` hooks. Hook response format: `{"hookSpecificOutput": {"hookEventName": "...", "additionalContext": "..."}}`. Used for REVIEW.md injection, wingman status notifications, "Powered by Entire" system messages.

## Sibling repos (referenced, not committed to)

- **entire-playground**: A test repo where dipree runs the built `entire` binary against real Claude sessions to verify wingman behavior end-to-end
- **entire.io** / **entire.io-1**: Likely a web frontend or related service; referenced for cross-checking trail JSON format/lifecycle

## Recurring themes across all work

- Visibility: constantly wants notifications/log messages showing what background processes are doing
- Event-driven correctness: deep focus on hook lifecycle, phase state machines, race conditions between concurrent processes
- UX polish: interactive flows must handle edge cases gracefully (inline validation, not crashes)
- Git hygiene: commits frequently, maintains clean branches, tracks draft PRs, closes out review comments
