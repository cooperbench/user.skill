---
name: commit-command
description: Ultra-terse git commands — fires when Zac wants to commit, push, or create a PR. Typically 2-5 words, lowercase, occasionally with file exclusions.
---

Zac treats git operations as one-liners. He does not describe what was changed. He may add a
file exclusion ("ignore the db/index.ts") or a branch instruction, but never a commit message.

The agent is expected to infer the commit message from context.

**Trigger**: Any turn that is ≤6 words and contains "commit", "push", "pull", "pr", or "branch".

## Examples

> "commit and push"

> "push the changes"

> "please commit"

> "commit"

> "did you pull"

> "commit your work, ignore the db/index.ts"

> "commit your changes, leave db/index.ts alone"

> "commit code you changed"

> "alright commit and push this branch and open up a pr so the adr can get a review"

> "pull down changes and resolve conflicts"

> "pull origin main and resolve conflicts"

## Behavior notes

- "ignore the db/index.ts" and "leave db/index.ts alone" are repeated across multiple sessions —
  that file has persistent uncommitted noise Zac doesn't want staged
- When he says "commit", he expects the agent to stage only the files it changed
- "pull pr comments and address any relevant ones" is a full workflow, not just a git pull
