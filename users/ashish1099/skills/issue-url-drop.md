---
name: issue-url-drop
description: References a GitHub issue by pasting the raw URL followed by a single context word — triggered when pointing the agent to a tracked bug or task.
---

When ashish1099 wants the agent to look at a GitHub issue, they paste the full URL and append
a single word ("issue") with no markdown link syntax, no title, no explanation. The word acts
as a type label, not a sentence.

> "https://github.com/Obmondo/gfetch/issues/1 issue"

The agent is expected to fetch the issue, read it, and figure out what to do. No instruction
is given about what action to take — that is left to context. This is consistent with the
broader pattern of treating the agent as capable of inferring intent from minimal signals.
