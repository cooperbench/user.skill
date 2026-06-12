---
name: terse-git-takeover
description: Triggers whenever cteyton wants a commit. Fires after any completed implementation step. 27.7% of all prompts are git operations. Takeover variant fires when the agent summarizes instead of committing (10.1% of prompts). Typos frequent in this context.
---

# Terse git (+ changelog) commands

After any completed implementation step, cteyton sends the shortest possible git instruction. Never elaborates. The message is the entire prompt.

**Standard forms** (non-pushback — agent already ran the commit):
- `"commit"`
- `"commit this"`
- `"commit and update changelog"`
- `"commit and update @CHANGELOG.md"`
- `"commit this and update changelog"`
- `"update changelog with a small sentence"`
- `"commit then"`

**Takeover forms** (agent talked instead of committing):
- `"commit"` (same word, but now it's impatient)
- `"Commit"` (capitalized = more impatient)
- `"commit all your recent changes"`
- `"commit your changes"`
- `"commit and hpush"` (typo for "push")

**Typo variants** (when typing fast):
- `"comit"`
- `"commi"`

## Verbatim examples

> `"commit and update changelog"`

> `"commit"`

> `"comit"`

> `"commit and hpush"`

> `"Commit"` — (capitalized when taking over from a slow agent)

## When NOT to use

If cteyton is mid-plan and has a follow-up question, the git command does not appear. Git commands only appear after implementation is complete or when the agent is narrating rather than acting.
