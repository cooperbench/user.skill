# Projects — zchee

## zchee/zmux ★ dominant (79.2% of sessions)

**What he does here:** Building `zmux` (initially called `agentmux`), a Zig-based terminal multiplexer targeting full tmux parity. He renamed it from `agentmux` to `zmux` mid-project. Sessions cover: cursor style fixes, status bar rendering (format string expansion, padding, tmux.conf parity), shell startup probe/response protocol (OSC sequences, zsh startup relay), server-side GCD / io_uring → libxev migration, key input latency debugging, GPU rendering via Metal/Vulkan, multi-agent parallel implementation with OMX team mode.

**Tech stack:**
- Language: Zig (minimum 0.14.0), targeting macOS and Linux
- Build: `zig build`, `zig build test`, `zig fmt --check`, `zig build --summary all`
- GPU: Metal (macOS), Vulkan (Linux); FreeType font rasterization
- Terminal: Unix domain sockets, PTY, OSC escape sequences (startup probe), Sixel/Kitty inline images
- LSP: `zls` for diagnostics
- Event loop: migrating from GCD/io_uring to `libxev` / `std.Io`
- Tmux reference: https://github.com/tmux/tmux

**Recurring themes:**
- `zig build test` green/red as the gate for any commit
- Status line not rendering as defined in `~/.config/zmux/zmux.conf`
- Startup probe (OSC/zsh) and relay state machine (leader/worker protocol in `src/server.zig`, `src/client.zig`, `src/protocol.zig`, `src/startup_probe.zig`)
- Key input latency ("still very slow launch zsh and key-input")
- Multi-worker team implementations: `implement-the-startup-only-zsh`, `migrate-gcd-and-io-uring-to-li`, `implement-omx-specs-deep-inter`
- Commit hygiene: frequent squash of range `oldhead...newhead`, `$commit` skill

---

## zchee/spanner-manager (12.5% of sessions)

**What he does here:** Google Cloud Spanner management tooling in Go. One observed task: `$ultrawork "Normalize all words that are conventionally capitalized in Go (such as IDs)."` Suggests maintenance and code quality work rather than feature development.

**Tech stack:** Go, Google Cloud Spanner, Protocol Buffers (inferred), Terraform (inferred from persona config)

**Recurring themes:** Go naming convention enforcement (capitalized identifiers), OMX team mode, `$commit` at end

---

## zchee/agent (8.3% of sessions)

**What he does here:** The OMX orchestration framework itself. He builds and extends his own AI-agent tooling: writing skill files (`$skill-creator Zsh completion script skill`), converting external skills to Codex style (`Convert https://github.com/vercel-labs/agent-browser/tree/main/skills/agent-browser to Codex Skill Style`), and managing the agent infrastructure that drives all his other projects.

**Tech stack:** Codex / Claude Code CLI, Zsh (completion scripts, zsh docs at `/opt/homebrew/share/zsh/htmldoc/`), JSON skill schemas, tmux for pane management

**Recurring themes:** Skill authoring, environment context blocks, keyword detection tables, delegation rules, team model resolution
