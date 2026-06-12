---
name: git-clean-commit
description: Corrects commit format immediately after the agent creates a commit — triggered when the agent adds co-author lines, multi-line bodies, or anything beyond a single plain imperative message.
---

Rejects agent-added attribution (Co-authored-by, Co-Authored-By) and verbose multi-line commit messages. Wants one plain line only. Also tells the agent which branch to push to by name without using the branch creation workflow.

**Example 1** (removing attribution):
> "remove that coautherd by and keep the commit msg normal one line only!"

**Example 2** (naming the target branch):
> "so lets push this into the current fixingmajorissues branch!"
