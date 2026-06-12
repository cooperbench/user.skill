---
name: git-delegation
description: Trigger when Soph delegates git operations — commits, branch reviews, CHANGELOG updates, PR reviews — to the agent with a brief imperative command.
---

# Git delegation

Git tasks are a major intent category (16.6%). Soph delegates them concisely and expects clean execution.

**Commit grouping:**
> "can we group the changes into meaningful commits?"
> "can you commit both changes we did in individual commits for me?"

**CHANGELOG:**
> "can you update CHANGELOG.md for 0.4.6 from 0.4.5"

**Branch / PR review:**
> "can you review the changes in this branch?"
> "can you review the changes in the local branch?"
> "can you review the changes in this branch by two competing agents?"

**Conflict / merge issues:**
> "can you fix the local branch? i merged in main and maybe I resolved the conflict wrong"

**Branch investigations:**
> "I think we don't setup `entire/sessions` branch with a remote properly, can you check?"

After the agent reports back, Soph either confirms ("yes", "ok") or corrects a specific detail ("the squash in GitHub keeps trailers", "ok, make it a 0.5.0"). When a PR is involved, they may also ask: "can you look at the pr comments" or "can you review the copilot comments on the PR?" to process inline feedback.
