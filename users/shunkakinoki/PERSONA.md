# Persona — shunkakinoki

## Background (inferred)

Solo developer / indie hacker (inferred) with a deeply customized dev environment. The entire recorded session history lives inside a single personal repo (`shunkakinoki/dotfiles`), suggesting this person treats their machine config as their primary engineering project — or uses it as a playground while working on other things.

Active contributor to upstream tools: the digest shows a mention of `@shunkakinoki for #1653` in the worktrunk changelog, indicating real open-source involvement beyond dotfile tweaking.

## Domain Expertise

- **NixOS / home-manager**: Navigates flakes, modules, `lib.optionals`, `home.file`, `nix develop`, statix linting, and `make switch` build loops fluently — no hand-holding needed.
- **Fish shell scripting**: Writes and tests custom functions (`_clwrc_function`, `_clrc_function`, `_gco_function`); references `make shell-test` / `make shell-lint` as CI gates.
- **Neovim / Lua**: Knows how treesitter plugins load, references `nvim-treesitter.config`, manages lua config symlinks via home-manager.
- **macOS toolchain**: Bun, Cargo, Homebrew Cask installs, macOS keychain (`security find-generic-password`), launchd agents, Pushover notifications.
- **tmux**: Knows keybinding internals, paste buffer semantics (`run-shell` vs. client-write path).
- **Claude Code internals**: Knows about `--permission-mode bypassPermissions`, `--spawn worktree`, hooks (`stop`, `Bash` matcher), settings.json structure, and remote-control sessions.
- **Tailscale networking**: SSHes into named machines ("kyber machine (tailscale)") mid-session.

## Role (inferred)

Independent developer / technical founder (inferred). No mentions of team, sprint, or manager. All work is self-directed; decides what gets built or reverted.

## Seniority Signals

- Immediately identifies root causes from stack traces without asking for explanation.
- Names specific commit SHAs when requesting reverts.
- Knows which GH Actions step is failing and why without being told.
- Pushes back on implementation aesthetics ("this is ugly"), not just correctness.

## Attitude Toward the Agent

**Mostly trusting, with fast corrections.** Lets the agent run long operations autonomously (nix builds, CI checks); delegates `make format`, `make switch`, PR creation. But when the agent overshoots — explains too much, touches wrong files, or adds unsolicited complexity — the user cuts it off immediately with an interrupt or a one-line redirect. Does not re-explain; expects the agent to infer intent from the correction alone.

Occasionally impatient with latency: notes slow stop-hooks, slow `clwxe` startup, slow token display in the UI.
