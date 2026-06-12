---
name: format-demand
description: "Trigger: agent has produced output in a table, markdown-heavy, or otherwise non-copyable format. User demands a plain copy-pasteable format."
---

When the agent uses markdown tables or decorative formatting for output the user intends to paste elsewhere (PR body, comment, etc.), this user issues a brief format correction with no explanation.

**Example:**

Agent produces a PR description as a markdown table with `|------|------|` formatting.

User replies:
> `コピペしやすい形式で出して欲しい`

**What this means in practice:** Plain text, no markdown tables, no heavy formatting. Output that can be pasted directly into a GitHub PR description or comment without cleanup. Bullet lists are acceptable; tables are not preferred.

**Broader pattern:** This user values output they can act on immediately without post-processing. The same preference shows in workflow design: slash commands encode the full procedure so the agent runs it without prompting. The format demand is the reactive version of this — correcting an agent that forces manual cleanup.
