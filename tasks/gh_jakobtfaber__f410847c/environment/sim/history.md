> SYSTEM

# AGENTS.md instructions for /Users/jakobfaber/Developer/repos/github.com/jakobtfaber/dsa110-FLITS <INSTRUCTIONS> # Codex Configuration ## Learned User Preferences - When the user asks about Codex, interpret that as Codex CLI/configuration specifically; do not answer from Cursor MCP or Cursor IDE state unless explicitly asked. - For cross-agent plan review, use Codex with GPT-5.5 medium effort, Claude Code with Opus 4.8 xhigh effort, and Antigravity through the `agy` CLI when available. - Be conservative about durable memory: capture recurring corrections and stable workspace facts only, not one-off runtime details or transient command output. - For chezmoi-managed dotfiles, edit source under `~/Developer/repos/github.com/jakobtfaber/dotfiles/home/`; restore live drift (e.g. tool-injected shell hooks) with `chezmoi apply --force` on the target file, not direct edits to `~/.*`. - When adding core Homebrew tooling, promote packages into `home/dot_Brewfile.tmpl` (e.g. `dotfiles local promote brew <pkg>`) instead of only running `brew install`. - Maintain Mac-local agent and observability inventories in `~/Obsidian/LLMs/agents/registry/` (`Agent Registry`, `Agent Observability Registry`, inactive-tools log) alongside chezmoi/dotfiles memory—not only in `AGENTS.md`. - Keep `wolfbook.mcpEnabled: false` in Cursor and VS Code so the Wolfbook extension does not rewrite Antigravity/Gemini MCP configs on disk. - Orchestrate Claude Code from Cursor via `claude -p --resume` from the session's project cwd; do not run parallel iTerm […]

> DEVELOPER

Confirm submodule Faber2026 is present.

> AGENT

I’ll check the repo metadata and working tree path directly, then report whether `Faber2026` is registered and present on disk.

> AGENT

`git submodule status` and `.gitmodules` both returned empty, so Git does not currently have any registered submodules in this checkout. I’m checking the path itself now because a plain directory could still exist outside submodule metadata.

> AGENT

The filesystem check also returned no `Faber2026` directory. One more compact file search will confirm there is no matching path or `.gitmodules` file hidden in the repo tree.

> AGENT

`Faber2026` is **not present as a submodule** in this checkout. Checks run from `/Users/jakobfaber/Developer/repos/github.com/jakobtfaber/dsa110-FLITS`: - `git submodule status --recursive` returned no entries. - `.gitmodules` has no registered submodules. - `git ls-files --stage | grep -F 'Faber2026'` returned no tracked path. - `Faber2026/` is not present on disk.