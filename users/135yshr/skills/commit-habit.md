---
name: commit-habit
description: Trigger — after any batch of file changes, the user fires /commit (or raw git push / create pr) as a reflex, often the very next turn
---

Git operations are the most frequent intent (25.9 %). The user treats commit/push/PR as punctuation — not a deliberate workflow step but an automatic keystroke after any editing session.

**Patterns** (in order of frequency):
1. `/commit` slash command (appears as `<command-name>/commit</command-name>` in the digest)
2. `create pr` — raw two-word PR creation instruction
3. `git push` — pasted as a bash input

These often appear with no surrounding context — just the command alone on its own turn, immediately after a content change or lint fix.

**Example sequence**:
```
[agent writes article edits and runs textlint]

user: <command-message>commit</command-message>
      <command-name>/commit</command-name>

[agent commits]

user: <bash-input>git push</bash-input>
```

**How to role-play**: After 2–4 turns of substantive editing, emit `/commit` (as the slash command syntax) or `create pr` as a standalone turn. Do not describe what was done; just fire the command.
