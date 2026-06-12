# Projects — penso

## moltis-org/moltis ★ DOMINANT (100% of sessions)

**What it is:** A self-hosted AI agent platform written in Rust. Multi-crate Cargo workspace. Users install it locally/on a server, connect LLM providers, and interact via web UI, CLI, or external channels (Telegram, Teams). Think: a self-hosted Claude Code alternative with multi-provider support, voice, sandboxing, and remote access.

**Tech stack:**
- Language: Rust (primary), TypeScript/JS (web UI)
- Build: Cargo workspace, cargo +nightly for fmt, biome for JS
- CI: GitHub Actions; local gate: `./scripts/local-validate.sh <PR#>`
- Auth: session cookies, GPG-signed commits via YubiKey
- Deployment: macOS launchd, Linux systemd, Docker, Tailscale
- Testing: `cargo nextest`, Playwright E2E tests

**Crate structure (inferred from prompts):**
| Crate | Role |
|-------|------|
| `crates/gateway/` | Core HTTP/WS gateway, auth middleware, state management |
| `crates/cli/` | CLI entrypoint, node commands |
| `crates/providers/` | LLM provider integrations (OpenAI, Anthropic, GitHub Copilot, local LLM) |
| `crates/agents/` | Agent model, conversation conversion, tool-call handling |
| `crates/chat/` | Chat routing, model selection, provider priority |
| `crates/onboarding/` | Setup wizard, sentinel file, identity management |
| `crates/config/` | Config loading, identity/soul/user file management |
| `crates/node-host/` | Distributed node runner, launchd/systemd service generation |
| `crates/projects/` | Git worktree management |
| `crates/mcp/` | MCP client |
| `crates/auth/` | Credential store |
| `crates/oauth/` | OAuth flows, PKCE, device flow |
| `crates/telegram/` | Telegram bot channel |
| `crates/msteams/` | MS Teams webhook channel |
| `crates/web/` | Web UI (TypeScript/Playwright E2E) |

**Recurring themes in penso's sessions:**

1. **Provider integrations** — adding/fixing LLM provider support. Recent: GitHub Copilot Responses API (`gpt-5.4+`), local LLM raw token streaming, OpenAI Codex.

2. **Auth and onboarding** — STT 401 during onboarding, soul/identity file location refactor (`soul-location` branch), Tailscale remote access with redirect loop fix.

3. **Release management** — date-based versioning migration (semver → YYYYMMDD.NN), update checker refactor, release workflow automation.

4. **Installation/user feedback** — Discord transcript sessions: user reports issues, penso asks agent to plan+fix all of them in batch.

5. **PR hygiene** — multiple sessions dedicated entirely to resolving PR review comments from greptile and Codex bots.

6. **Debug loop** — heavy test failure iteration with `local-validate.sh`. Common failures: formatting (cargo fmt, biome), GPG signing in headless terminal, test environment issues (worktree tests failing due to `commit.gpgsign=true`).

**Branch naming convention:** descriptive kebab-case per feature: `soul-location`, `stt-401-during-onboarding`, `tailscale-redirects`, `local-llm-raw-token`, `versioning`, `installation-feedback`.

**Worktree root:** `~/.superset/worktrees/moltis/<branch>/` (abbreviated as `~/.s/w/m/<branch>/` in shell prompts).

**Issue tracker:** GitHub issues at `github.com/moltis-org/moltis/issues/`. penso references issues by number (e.g., #319, #350, #351, #356, #376, #378, #384, #389, #392, #397, #398).

**PR review bots:** greptile and Codex (automated). penso regularly asks the agent to read and resolve their comments.
