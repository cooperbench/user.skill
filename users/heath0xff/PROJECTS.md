# Projects: heath0xFF

## heath0xFF/hChat (dominant — 100% of sessions)

**What it is**: A Rust desktop chat client for LLM endpoints, built with egui/eframe. Connects to
local Ollama, OpenRouter, and any OpenAI-compatible API. Distributed for macOS via a Homebrew tap.
Config lives at `~/.config/hchat/config.toml`.

**What heath does there**: Everything. He is the sole author. He uses the agent to:
- Write all features ("let's add in a config reload button")
- Run paranoid multi-agent code reviews before and after large changes
- Fix bugs reported from his own testing ("there's a bug with using openrouter in hchat now")
- Handle git tagging and release pushes
- Set up CI/CD (GitHub Actions for Homebrew formula automation)
- Write documentation (README, example.config.toml, agents.md)

**Tech stack**:
- **Language**: Rust (edition 2021)
- **GUI**: egui 0.34 / eframe 0.34 (immediate-mode; full UI rebuilt every frame)
- **Async**: tokio with runtime embedded in `ChatApp` struct
- **HTTP**: reqwest 0.12 with streaming support
- **Storage**: rusqlite 0.31 with bundled SQLite, WAL mode
- **Config**: serde + toml, atomic writes via temp file, 1MB size cap
- **Serialization**: serde_json for LLM API payloads
- **UI extras**: egui-commonmark for markdown rendering, arboard for clipboard

**Module structure**:
- `src/main.rs` — entry point
- `src/app.rs` — monolithic (1100+ lines): ChatApp struct (44 fields), all UI rendering, all state management, async coordination
- `src/api.rs` — HTTP streaming, model fetching, StreamEvent enum, OpenRouter special-casing
- `src/config.rs` — Config struct, TOML load/save, try_load() fallible variant
- `src/storage.rs` — SQLite CRUD for conversations and messages
- `src/message.rs` — Message and Role types

**Recurring themes in sessions**:
- Performance: clone hot-paths in egui frame loop (lines 541, 846, 866 of app.rs flagged repeatedly)
- Security: plaintext API key storage in config.toml (knows it's a problem, hasn't solved it yet)
- Code quality: monolithic app.rs, Result<T, String> anti-pattern, unwrap/expect overuse
- Config lifecycle: hot-reloading config without restart was a recurring pain point that drove the "reload config" feature
- OpenRouter integration: model listing, endpoint switching, API key propagation

**Distribution**:
- Homebrew tap (separate repo, automated via GitHub Actions on tag push)
- Releases tagged as v0.3.x; last known tags in session: v0.3.4, v0.3.5
- GitHub: `github.com/hhheath/hChat` (inferred from code comment in api.rs)

**agents.md**: A documentation file in the repo that describes the codebase for agent consumption,
maintained by heath as part of his workflow. He reviews and updates it when agents identify stale
content.
