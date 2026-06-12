---
name: terse-git-command
description: Issues git operations as 1–4 word imperatives with no context. Triggers whenever a logical unit of work is done and needs committing, staging, or rebasing.
---

pjbgf issues git commands as the shortest possible imperative. No explanation of what changed,
no commit message guidance, no "please". The agent is expected to compose the commit message,
stage the right files, and handle conflicts independently.

Capitalization is inconsistent — sometimes lowercase, sometimes sentence-case. Both are real.

**Examples:**

> "commit staged changes"

> "commit this"

> "stage and commit"

> "Commit"

> "Fix the new rebase conflicts"

The last example ("Fix the new rebase conflicts") is still a git task despite reading like a
debug command — the user expects the agent to resolve git conflict markers, not diagnose code.
