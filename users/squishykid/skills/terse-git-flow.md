---
name: terse-git-flow
description: How squishykid issues git commands — rapid-fire, 2-6 words, often chained across consecutive turns. Trigger when the current task is done and it's time to commit, push, or open a PR.
---

squishykid treats git operations as a reflex, not a ceremony. After any meaningful code change they immediately fire one of these commands, often in sequence across turns:

- "commit and push"
- "push it"
- "git push"
- "make a PR for this"
- "create a PR"
- "commit and create a pr referencing #279 and #293"
- "commit as 'agent: remove HookHandler'"
- "commit this on a feature branch. use prefix 'rwr/' for the branch name"

They specify branch naming (`rwr/` prefix), PR references (issue numbers inline), and stacking ("create a PR on top of 427") but do not elaborate on commit message style beyond the message itself.

**Example — after implementation completes:**
> `commit this on a feature branch. use prefix 'rwr/' for the branch name`

**Example — routine push:**
> `commit and create a pr referencing issue 424`

**Example — minimal:**
> `git push`
