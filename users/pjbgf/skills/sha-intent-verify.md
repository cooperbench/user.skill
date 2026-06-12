---
name: sha-intent-verify
description: After a rebase or conflict resolution, asks the agent to confirm that a specific commit's changes and intent were preserved. Triggers when there is risk that a merge/rebase dropped meaningful work.
---

pjbgf does not review the diff themselves after a complex rebase. Instead they ask the agent
to compare the post-rebase tree against a specific commit SHA and confirm that the *intent*
(not just the diff) was preserved. The word "intent" is used explicitly.

The SHA is given as a full 40-character hex string. The question is phrased as a yes/no
confirmation request but expects the agent to do the analysis.

**Example:**

> "Can you confirm that all changes (and more importantly the intent) from aa72883e2fda43a68e6368f9eb00d250d46725c1 were preserved?"

The parenthetical "and more importantly the intent" signals that a mechanical line-diff is
insufficient — the agent must reason about what the commit was trying to accomplish.
