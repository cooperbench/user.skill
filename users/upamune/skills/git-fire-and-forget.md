---
name: git-fire-and-forget
description: >
  Trigger: agent has just finished implementing something (fix, feature, refactor).
  upamune issues a compound git command as a single message without waiting for a summary.
---

When implementation is complete, upamune does not acknowledge the agent's closing summary. He immediately fires a single message that chains all required git operations. The phrasing varies but always covers commit + push + PR creation.

English git verbs are always used even when the surrounding text is Japanese. Separators vary: `&`, `/`, `、`, `,` — all equivalent.

**Examples:**

> "commit & push & create a pr"

> "commit して, push して、 create a pr"

> "branch / commit / push / create a pr"

> "check, commit, push, create a pr"

If the agent forgot to create a branch first, a correction comes *before* the full compound: "branch 切って". Once the branch exists, the full compound follows.
