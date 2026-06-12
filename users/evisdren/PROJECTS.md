---
name: evisdren-projects
description: Repos and project context for evisdren.
metadata:
  type: project
---

# Projects: evisdren

## entireio/cli ★ (dominant — 100% of sessions)

**What it is**: A Go CLI tool (`entire`) that hooks into git's `prepare-commit-msg` and `post-commit` hooks to record which AI coding agent session was active when a commit was made. Sessions are stored as JSONL transcripts on a shadow git branch (`entire/checkpoints/v1`), enabling post-hoc linking of commits to AI session context.

**What evisdren does here**:
- Designs and implements settings architecture (`commit_linking`, `settings.json` vs `settings.local.json` merge logic).
- Writes performance benchmarks (`BenchmarkSeedShadowBranch`, `BenchmarkSeedMetadataBranch`, `TestCommitHookPerformance`) with real repo clones.
- Refactors abstraction layers (removing the `Strategy` interface, inlining `ManualCommitStrategy`).
- Builds multi-agent support (Claude Code, Gemini CLI, Codex hooks), including a multi-select TUI for `entire enable`.
- Debugs macOS/Homebrew distribution issues (Gatekeeper notarization).
- Manages PRs with Copilot and Cursor reviews relayed through Claude Code.

**Tech stack**:
- Go (primary), `go-git` for git operations
- `mise.toml` for task running (bench, test, compare tasks)
- `gh` CLI for PRs and repo management
- `golangci-yaml` for linting (`ireturn` rule)
- `benchstat` for benchmark comparison
- zstd compression (being evaluated for checkpoint transcripts)
- macOS + Homebrew distribution

**Recurring themes**:
- Performance: hook latency at 100+ sessions, push time for large checkpoint branches
- Settings correctness: which file to write to, merge order, migration of deprecated fields
- Real-world data: insists on real repo clones and real checkpoint data for tests
- Multi-agent ecosystem: ensuring `entire` works with Claude Code, Gemini CLI, Codex
