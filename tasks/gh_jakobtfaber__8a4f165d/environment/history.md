> SYSTEM

# AGENTS.md instructions for /home/<USER>/Developer/repos/github.com/jakobtfaber/dsa110-FLITS

<INSTRUCTIONS>
# Codex Configuration

## Learned User Preferences

- When the user asks about Codex, interpret that as Codex CLI/configuration specifically; do not answer from Cursor MCP or Cursor IDE state unless explicitly asked.
- For cross-agent plan review, use Codex with GPT-5.5 medium effort, Claude Code with Opus 4.8 xhigh effort, and Antigravity through the `agy` CLI when available.
- Be conservative about durable memory: capture recurring corrections and stable workspace facts only, not one-off runtime details or transient command output.
- For chezmoi-managed dotfiles, edit source under `~/Developer/repos/github.com/jakobtfaber/dotfiles/home/`; restore live drift (e.g. tool-injected shell hooks) with `chezmoi apply --force` on the target file, not direct edits to `~/.*`.
- When adding core Homebrew tooling, promote packages into `home/dot_Brewfile.tmpl` (e.g. `dotfiles local promote brew <pkg>`) instead of only running `brew install`.
- Maintain Mac-local agent and observability inventories in `~/Obsidian/LLMs/agents/registry/` (`Agent Registry`, `Agent Observability Registry`, inactive-tools log) alongside chezmoi/dotfiles memory—not only in `AGENTS.md`.
- Keep `wolfbook.mcpEnabled: false` in Cursor and VS Code so the Wolfbook extension does not rewrite Antigravity/Gemini MCP configs on disk.
- Orchestrate Claude Code from Cursor via `claude -p --resume` from the session's project cwd; do not run parallel iTerm […]

> DEVELOPER

Confirm submodule Faber2026 is present.

> AGENT

I’ll check the repo metadata and working tree path directly, then report whether `Faber2026` is registered and present on disk.

> TOOL

tool_use shell_command
id: call_nOeIzHnYmGrSEhHeRus0FH7V
```json
{
  "command": "git submodule status --recursive",
  "workdir": "/home/<USER>/Developer/repos/github.com/jakobtfaber/dsa110-FLITS",
  "timeout_ms": 10000
}
```

> TOOL

tool_use shell_command
id: call_ZE71Qq9hFMyIPgUoRqlgdQAD
```json
{
  "command": "git config --file .gitmodules --get-regexp 'submodule\\..*\\.(path|url)' || true",
  "workdir": "/home/<USER>/Developer/repos/github.com/jakobtfaber/dsa110-FLITS",
  "timeout_ms": 10000
}
```

> TOOL

tool_use shell_command
id: call_CTYRkAfx1GtgDGwV8cmctPS5
```json
{
  "command": "ls -ld Faber2026 2>/dev/null || true",
  "workdir": "/home/<USER>/Developer/repos/github.com/jakobtfaber/dsa110-FLITS",
  "timeout_ms": 10000
}
```

> TOOL

tool_result
id: call_nOeIzHnYmGrSEhHeRus0FH7V
```
Exit code: 0
Wall time: 0.4 seconds
Output:

```

> TOOL

tool_result
id: call_ZE71Qq9hFMyIPgUoRqlgdQAD
```
Exit code: 0
Wall time: 0.1 seconds
Output:

```

> TOOL

tool_result
id: call_CTYRkAfx1GtgDGwV8cmctPS5
```
Command blocked by PreToolUse hook: rtk-codex-guard: shell command should use RTK compact output.

Suggested command:
rtk ls -ld Faber2026 2>/dev/null || true

To bypass for this command, prefix it with: RTK_DISABLED=1. Command: ls -ld Faber2026 2>/dev/null || true
```

> AGENT

`git submodule status` and `.gitmodules` both returned empty, so Git does not currently have any registered submodules in this checkout. I’m checking the path itself now because a plain directory could still exist outside submodule metadata.

> TOOL

tool_use shell_command
id: call_a5wJlcOW1Cb5s0h12EX2nyoV
```json
{
  "command": "rtk ls -ld Faber2026 2>/dev/null || true",
  "workdir": "/home/<USER>/Developer/repos/github.com/jakobtfaber/dsa110-FLITS",
  "timeout_ms": 10000
}
```

> TOOL

tool_use shell_command
id: call_LKcP6l6vyi93VxWK7ZZEnZNS
```json
{
  "command": "rg --files -g '.gitmodules' -g '*Faber2026*' -g '!*.png' -g '!*.jpg'",
  "workdir": "/home/<USER>/Developer/repos/github.com/jakobtfaber/dsa110-FLITS",
  "timeout_ms": 10000
}
```

> TOOL

tool_result
id: call_a5wJlcOW1Cb5s0h12EX2nyoV
```
Exit code: 0
Wall time: 0.1 seconds
Output:

```

> TOOL

tool_result
id: call_LKcP6l6vyi93VxWK7ZZEnZNS
```
Command blocked by PreToolUse hook: rtk-codex-guard: shell command should use RTK compact output.

Suggested command:
rtk grep --files -g '.gitmodules' -g '*Faber2026*' -g '!*.png' -g '!*.jpg'

To bypass for this command, prefix it with: RTK_DISABLED=1. Command: rg --files -g '.gitmodules' -g '*Faber2026*' -g '!*.png' -g '!*.jpg'
```

> AGENT

The filesystem check also returned no `Faber2026` directory. One more compact file search will confirm there is no matching path or `.gitmodules` file hidden in the repo tree.

> TOOL

tool_use shell_command
id: call_To2nuE1cxBCWOPs6WYEkVo6X
```json
{
  "command": "rtk grep --files -g '.gitmodules' -g '*Faber2026*' -g '!*.png' -g '!*.jpg'",
  "workdir": "/home/<USER>/Developer/repos/github.com/jakobtfaber/dsa110-FLITS",
  "timeout_ms": 10000
}
```

> TOOL

tool_use shell_command
id: call_zjsegtATta0kn2aWAfTgH0VF
```json
{
  "command": "git ls-files --stage | grep -F 'Faber2026' || true",
  "workdir": "/home/<USER>/Developer/repos/github.com/jakobtfaber/dsa110-FLITS",
  "timeout_ms": 10000
}
```

> TOOL

tool_result
id: call_To2nuE1cxBCWOPs6WYEkVo6X
```
Exit code: 2
Wall time: 0.2 seconds
Output:
grep: option `--files' is ambiguous
usage: grep [REDACTED] [-A num] [-B num] [-C[num]]
	[-e pattern] [-f file] [--binary-files=value] [--color=when]
	[--context[=num]] [--directories=action] [--label] [--line-buffered]
	[--null] [pattern] [file ...]

```

> TOOL

tool_result
id: call_zjsegtATta0kn2aWAfTgH0VF
```
Exit code: 0
Wall time: 0.1 seconds
Output:

```

> AGENT

`Faber2026` is **not present as a submodule** in this checkout.

Checks run from `/home/<USER>/Developer/repos/github.com/jakobtfaber/dsa110-FLITS`:

- `git submodule status --recursive` returned no entries.
- `.gitmodules` has no registered submodules.
- `git ls-files --stage | grep -F 'Faber2026'` returned no tracked path.
- `Faber2026/` is not present on disk.