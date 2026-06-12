---
name: slash-command-fire
description: Fires a slash command with zero preamble when ronnnnn wants to trigger a known skill workflow. Use when the user's entire message is a bare command invocation with no additional text.
---

ronnnnn triggers automation by sending a bare slash command — nothing before it, nothing after it. No description of intent, no arguments unless required. The command is the entire message.

The agent is expected to know what the command does and execute it autonomously to completion.

**Examples:**

```
/git:pr-create
```

```
/git:pr-watch
```

```
/bump-version
```

```
/git:commit
```

When role-playing ronnnnn:
- If the current context calls for creating a PR, committing, or watching CI, output just the slash command
- Do not add "お願いします" or any framing text
- The command name is always lowercase with colons as namespace separators
