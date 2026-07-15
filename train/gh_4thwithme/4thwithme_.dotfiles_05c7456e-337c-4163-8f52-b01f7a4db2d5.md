---
session_id: "4thwithme/.dotfiles|05c7456e-337c-4163-8f52-b01f7a4db2d5"
developer: "gh:4thwithme"
split: train
source: crawl
repo: 4thwithme/.dotfiles
start_time: "2026-04-03T11:38:38.374Z"
n_turns: 11
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

where claude code buddy lives in the local machine

> AGENT

- **Binary**: `/Users/4thwithme/.local/bin/claude`
- **Config/data**: `~/.claude/`

Key subdirectories in `~/.claude/`:
| Dir | Purpose |
|-----|---------|
| `projects/` | Per-project memory, settings |
| `skills/` | Custom skills |
| `plugins/` | Plugins |
| `sessions/` | Conversation history |
| `settings.json` | Global settings |
| `ide/` | IDE integration data |

> DEVELOPER

i want to rename it

> AGENT

Rename what exactly? The `claude` binary/command to something else?

> DEVELOPER

buddy[Image #1]

> AGENT

You want to alias `claude` to `buddy`. Simple:

```bash
alias buddy='claude'
```

To make it permanent, add it to your shell config:

```bash
echo "alias buddy='claude'" >> ~/.zshrc
```

Want me to add it?

> DEVELOPER

node

> AGENT

You want to rename the companion (Brine the cactus) to "Buddy". Let me find where that's configured.

> AGENT

The companion (Brine) is part of the Superpowers plugin. Let me check where the name is configured.

> AGENT

The mascot (Brine) comes from the status line (`ccstatusline`). Let me check if it has a config for the name.

> AGENT

The "Brine" cactus mascot is not from `ccstatusline` — it's a built-in Claude Code companion feature. The name and character are hardcoded in the Claude Code binary itself, not user-configurable.

There's no setting to rename it. You'd need to either:

1. **File a feature request** with the Claude Code team for custom companion names
2. **Check if `/rename` affects it** — but that only renames the session, not the companion

The companion name "Brine" is baked into the client. Can't change it from your side.
