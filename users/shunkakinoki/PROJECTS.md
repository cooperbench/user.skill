# Projects — shunkakinoki

## shunkakinoki/dotfiles ★ DOMINANT (100% of sessions)

**What the user does here:** Maintains a NixOS/home-manager monorepo covering their entire macOS (and some Linux) developer environment. This is not a side project — it's the primary engineering workspace. Sessions span debug, refactor, and new-feature work at roughly equal rates.

**Tech stack:**
- NixOS / home-manager (modules, flakes, `make switch`, statix linting, nixpkgs)
- Fish shell (custom functions under `home-manager/programs/fish/`, tested via `make shell-test` / `make shell-lint`)
- Neovim + Lua config (`home-manager/programs/neovim/lua/config/`)
- tmux config (keybindings, paste-buffer management)
- Bun + package.json (JS tooling layer alongside Nix)
- Cargo / Rust (worktrunk, other Cargo-managed tools)
- GitHub Actions CI (multi-job, includes lua-neovim check, nix lint, docker builds)
- Claude Code settings (`config/claude/settings.json`, hooks, statusline scripts)
- Tailscale (multi-machine SSH, named host "kyber")
- macOS Keychain + launchd (keychain-sync service, Pushover notifications)
- Ghostty (terminal emulator config, light mode issue)
- cliproxyapi (custom OAuth proxy service)

**Recurring themes:**
1. **Hook latency** — stop hooks, Bash hooks, timeout values in `settings.json`
2. **Claude Code / remote-control functions** — `_clrc_function`, `_clwrc_function`, permission modes, worktree spawning
3. **Nix symlink / home-manager force-link behavior** — lua config type changes (T in git status), relative vs. absolute symlinks
4. **CI pipeline failures** — GitHub Actions, nix-install in Docker, lua-neovim plugin build
5. **Shell test coverage** — `make shell-test` as the quality gate for every fish function change
6. **Makefile cleanliness** — no inline bash scripts in Nix modules, scripts extracted to `config/scripts/` or `local-scripts/`
7. **Keychain sync** — syncing Claude/Codex OAuth tokens across machines via a launchd service

**Key paths referenced in prompts:**
- `home-manager/programs/fish/default.nix`
- `home-manager/programs/neovim/lua/config/`
- `home-manager/modules/local-binaries/`
- `config/claude/settings.json`
- `config/claude/statusline-git.sh`
- `Makefile` (targets: `build`, `switch`, `format`, `shell-test`, `shell-lint`, `updater`)

**Upstream contributions (evidenced):**
- worktrunk PR #1653 (custom copy-ignored exclude patterns), credited in changelog as `@shunkakinoki`
