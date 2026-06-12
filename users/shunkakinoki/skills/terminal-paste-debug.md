---
name: terminal-paste-debug
description: >
  Triggered when the user reports a bug or failure by pasting raw terminal output — full
  fish shell prompt (with emoji and timing), error stack or CI log — instead of describing
  the problem in prose. Usually ends with a short suffix question or no text at all.
---

When something breaks, the user does not narrate the error. They paste the terminal verbatim — fish prompt (with `📦`, `🥟`, `🐍`, `🦀`, `☁️`, `❯`, timing like `took 10m18s`) + the error output. Any explanatory text comes *after* the paste as a short lowercase suffix, or is omitted entirely.

## Examples

**With suffix:**
```
dotfiles on  main [$!] is 📦 v0.1.0 via 🥟 v1.3.11 via 🐍 v3.13.12 via 🦀 v1.94.1 on ☁️  <EMAIL> took 10m18s
❯ _gco_function
M       bun.lock
T       home-manager/programs/neovim/lua/config/ai.lua
[...]
Already up to date. keep package.json and bun.lock but i want to investigate why the .lua config why is it doing that
```

**Node error + suffix:**
```
/opt/homebrew/Caskroom/claude-code/2.1.79/claude:1
����
SyntaxError: Invalid or unexpected token
    at wrapSafe (node:internal/modules/cjs/loader:1762:18)
[...]
Node.js v25.8.1 why is this failing
```

**No suffix (paste is the entire message):**
The user expects the agent to diagnose from the output alone.

## Roleplay behavior

Produce the raw paste with the fish prompt line intact (emoji, branch name, timing, email placeholder). Keep the stack trace unedited. Append a 3–8 word lowercase question or nothing. No markdown formatting around the paste.
