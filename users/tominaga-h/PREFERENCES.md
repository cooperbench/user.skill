# Preferences — tominaga-h

## Pushback distribution

- **non_pushback** (61.1%): Accepts most agent output — especially after plan-driven implementation.
- **correction** (30.1%): Redirects scope, wrong issue number, missing spec detail, or asking for a plan instead of implementing.
- **failure_report** (8.0%): Pastes failing output verbatim for diagnosis.
- **rejection** (0.9%): Rare outright rejection.

## What triggers correction

- **Scope creep**: Agent adds unasked-for features (e.g., session key in welcome banner). Fixed with a single Japanese sentence stating what is NOT needed.
- **Wrong issue number**: Agent implements #86 when #85 was meant. Fixed with "すみません、Issue #X でした".
- **Implementing without a plan**: If agent skips straight to code, Hayato redirects: "修正プランを構築して".
- **Incorrect factual claim**: Agent says v1.3.0 tag doesn't exist when it does; Hayato pastes `git tag | cat` output.
- **Missing implementation detail**: Agent proposes an `ai` config key with wrong name; Hayato gives exact name and section.

## What triggers failure_report

- Feature doesn't work after implementation ("コマンド履歴のセッション分離がうまく行ってません。デバッグしてください").
- AI behavior is wrong in production use ("なんか頭悪いんだよなぁ…" + full terminal output paste).
- Build artifact confirms the issue: pastes debug log data for the agent to analyze.

## What satisfies

- Clean plan execution with no scope additions.
- Successful `make check` / `cargo check` / `cargo clippy` results (agent reports these proactively).
- Behavior confirmed on `jarvish` itself (he tests on the real shell).
- Multi-agent tasks completing with Bruce's "approved" verification.

## Workflow habits

1. **Plan-first**: Expects agent to propose a plan before implementing. Once approved, sends implementation boilerplate.
2. **To-do tracking**: Uses a task/to-do list system; tells agent "Do not create them again. Mark them as in_progress as you work."
3. **Commit gating**: Explicitly blocks commits ("待機") until he's done manual adjustments, then grants permission ("コミット許可").
4. **Multi-agent delegation**: For complex tasks, spawns the Avengers system (Fury → JARVIS → Tony/Peter/Bruce/Strange/Cap/Marvel/Shuri).
5. **Progress polling**: Sends "進捗報告" to get status updates from the agent team.
6. **Versioned releases**: Uses `/release vX.Y.Z` custom command; tags each release.
7. **No explanation preference**: Does not ask agents to explain what they did; prefers results and verification output.
8. **Testing on real shell**: Asks "今回修正したことってjarvish上でどうやったら確かめられる？" — wants to verify manually.

## Stack and tool preferences visible in prompts

- **Language**: Rust (primary), Python (CTF/scripting)
- **Build**: `cargo`, `make check` (fmt + check + clippy + test)
- **Shell tools**: `bat`, `cat`, `git`, `ls`
- **AI agent tools used by jarvish**: `read_file`, `write_file`, `search_replace`, `execute_shell_command`
- **Config format**: TOML (`~/.config/jarvish/config.toml`)
- **Storage**: SQLite-backed history via custom `BlackBox` abstraction
- **TUI/readline**: `reedline` crate
