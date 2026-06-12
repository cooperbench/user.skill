---
name: numbered-answer
description: >
  Trigger: the agent has asked hutusi multiple clarifying questions (numbered or bulleted).
  hutusi answers each point with a compact numbered list, one answer per point, often just
  a word or short phrase per item.
---

When an agent enumerates questions or options, hutusi responds in kind with a minimal numbered list. He does not re-state the question, does not use full sentences, and does not add explanation unless something is non-obvious. Each answer is as short as possible.

**Example:**

Agent asked about Obsidian import file format, frontmatter fields, tag handling, and content type.

hutusi replied:
> "1. YYYY-MM-DD.md, 2. no fields 3. yes, extract to frontmatter 4. mostly text."

Another example — selecting from agent-presented options by number only:
> "3"

Or selecting all of a presented list:
> "all three"

**Pattern**: `1. [answer], 2. [answer] 3. [answer] 4. [answer].` — commas and periods are inconsistent. No re-statement of the question. As terse as possible.
