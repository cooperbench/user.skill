---
slug: gagan114662
type: projects
---

# Projects

## gagan114662/openfang (dominant — 100% of sessions)

**What it is:** An open-source multi-agent AI daemon ("openfang") with:
- A local web dashboard at `http://127.0.0.1:50051/`
- A Telegram bot integration (@OpenClawAIDemoBot)
- Multi-provider LLM support: Claude (Anthropic via OAuth token), Codex/OpenAI, Gemini
- A CLI (`openfang-cli`) and a background daemon (`openfang start`)
- Async Rust core (Tokio), Teloxide for Telegram

**Tech stack (inferred from prompts):**
- Language: Rust (Cargo builds, release binaries, Tokio, Teloxide)
- LLM providers: Anthropic (Claude), OpenAI (Codex CLI), Gemini (being phased out by user)
- Bot framework: Teloxide (Rust Telegram library)
- Local path: `/Users/gaganarora/Desktop/my projects/open_fang`

**Recurring themes:**
- Getting the daemon running (`openfang start`) and verifying the dashboard is live
- Configuring LLM provider auth (OAuth token vs API key; Codex CLI authentication)
- Telegram bot setup (bot token, polling, message routing)
- Build issues (Cargo release builds, exit code 144 failures)
- Provider switching: removing Gemini agents, adding Codex/Claude agents
- Session wrap-up and checkpoint branching (`entire/checkpoints/v1`)

**Current state during sessions (inferred):**
- Dashboard was intermittently down; user kept verifying via URL
- Telegram bot created during session (BotFather token pasted)
- Codex authentication was unresolved / in-progress
- Gemini agents were being cleared out in favor of Claude + Codex

**Checkpoint branch target:** `https://entire.io/repositories` (inferred external platform)
