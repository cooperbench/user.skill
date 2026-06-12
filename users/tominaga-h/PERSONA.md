# Persona — tominaga-h

## Identity

- **GitHub username**: tominaga-h (referred to as "Hayato" in agent instructions he writes himself)
- **Role**: Independent developer / hobbyist systems programmer (inferred)
- **Primary project**: `jarvis-shell` (`jarvish`) — a Rust-based AI-powered interactive shell
- **Platform**: macOS (paths: `/Users/mad-tmng/...`)

## Expertise

- **Rust**: Comfortable with Cargo, `cargo clippy`, `make check`, crate-level architecture. Writes issue descriptions with Rust-specific context (`Arc<RwLock<...>>`, `reedline`, `BlackBox`, `session_id`). (inferred from domain depth)
- **Systems/shell programming**: Understands terminal history, readline behavior, session isolation, SQLite-backed storage, streaming AI responses.
- **Multi-agent orchestration**: Has built a sophisticated "Avengers" agent team system with role-specific instructions, task delegation, and race condition rules (RACE-001). Writes XML-tagged `<teammate-message>` protocols.
- **Python/CTF**: Occasional CTF (Capture The Flag) work (`daily-alpacahack`, crypto challenges) — uses Python, `pycryptodome`. (inferred from debug dump context)
- **Git**: Manages versioned releases (v1.0.0–v1.4.0+), knows tag state precisely, corrects the agent when it's wrong.

## Seniority signals

- Writes detailed, well-structured Japanese issue descriptions with concrete reproduction steps.
- Defines architectural constraints himself (RACE-001: no concurrent writes to the same file).
- Uses `mise` for Python version management (inferred from path), `bat`/`cat` for file inspection.
- Has custom `.claude/commands/` slash commands and a personal `.codex/skills/` system.
- Annotated as "Expert Nitpicker" in 38.5% of sessions — immediately notices scope creep.

## Attitude toward agents

- **Trusting but precise**: Delegates implementation fully once a plan is approved; does not micromanage steps.
- **Zero tolerance for scope creep**: Corrects immediately if the agent adds unrequested features.
- **Monitors progress actively**: Uses "進捗報告" (progress report) to poll multi-agent work.
- **Impatient with confusion**: If the agent works on the wrong issue, gets a one-liner correction with an apology tone ("すみません、Issue #85 でした").
- **Casual when frustrated**: "なんか頭悪いんだよなぁ…" signals genuine frustration, not anger — followed by a log dump for diagnosis.
- **Grants commit permission explicitly**: "OK, 調整した。コミット許可" — agent must wait for this.
