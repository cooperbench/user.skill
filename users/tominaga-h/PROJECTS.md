# Projects — tominaga-h

## tominaga-h/jarvis-shell ★ (dominant — 100% of sessions)

**What it is**: `jarvish` — an AI-powered interactive shell written in Rust. The shell intercepts commands, routes them to an AI (Claude via streaming API), and can autonomously fix build errors, answer questions in context, and execute shell commands. Named after the Marvel AI butler JARVIS.

**Tech stack**:
- Language: Rust
- readline/TUI: `reedline` crate
- Storage: SQLite via custom `BlackBox` abstraction (`src/storage/`)
- AI: Claude streaming API (`src/ai/stream.rs`, `src/ai/client/agent.rs`)
- Config: TOML (`~/.config/jarvish/config.toml`)
- Build: `cargo` + `make check` (fmt + check + clippy + test, ~400 tests)
- Versioning: semver tags (v1.0.0 through v1.4.0+), release notes per version

**Recurring development themes** (from prompts):
- **Session isolation**: Separating command history and logs per jarvish process instance using a unique session ID (hex key like `[0bf1d4]`).
- **AI intelligence improvements**: Making jarvish's built-in AI smarter — context awareness, file-aware investigation, not cascading errors.
- **Git integration**: Tab-completing branches for `git push`, `git checkout` etc. via `src/cli/completer/git.rs`.
- **Configuration extensibility**: Adding TOML config options for features (e.g., `[completion]`, `[ai]` sections).
- **Tool call visibility**: Making AI-driven file edits (`read_file`, `write_file`, `search_replace`) visually apparent in the terminal.
- **Non-interactive mode**: `-c` flag for single-command execution; preventing AI auto-investigation runaway in non-interactive mode.
- **Avengers multi-agent system**: Hayato has built a parallel AI agent team (`agent-team-avengers`) that runs as sub-agents coordinated by "Nick Fury". Team members: JARVIS (coordinator), Tony Stark (implementer), Bruce Banner (reviewer/verifier), Peter Parker (implementer), Doctor Strange (reviewer), Captain America, Captain Marvel, Shuri. Used for larger refactors requiring parallel file edits with RACE-001 (no concurrent file writes) enforcement.

**File structure clues from prompts**:
- `src/shell/ai_router.rs` — AI routing logic
- `src/shell/investigate.rs` — error investigation flow
- `src/ai/stream.rs` — streaming response handler
- `src/ai/tools/executor.rs` — tool execution (read_file, write_file, search_replace)
- `src/cli/completer/git.rs` — git branch completion
- `src/cli/prompt/git.rs` — git prompt integration
- `src/storage/history.rs` — command history with session filtering
- `src/config/mod.rs`, `src/config/defaults.rs` — TOML config
- `.avengers/` — Avengers multi-agent data directory (plans, dashboards, task lists)
- `.avengers/plans/reviews/bruce/` — Bruce Banner's review/verification reports

**Release cadence**: Frequent point releases; v1.0.0 → v1.4.0+ observed in one month (March–April 2026).
