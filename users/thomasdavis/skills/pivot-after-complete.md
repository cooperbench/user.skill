---
name: pivot-after-complete
description: How thomasdavis immediately pivots to a new feature or scope expansion when the agent announces completion. Trigger when the agent finishes a task and delivers a summary.
---

# pivot-after-complete

thomasdavis treats the agent's "here's what I did" summary as a pivot point, not a completion. He almost never says "great" or "looks good" before issuing the next directive. The next request arrives within the same breath as the agent's completion summary.

The pivot can be:
- A new adjacent feature ("set it up so we can track all frontend problems too in sentry.io")
- A scope expansion on what was just done ("add far more tracking stacks for how often users execute agents, collections and tools")
- A chain step he expected to already be included ("after claude fixes an automatically reported error in github, i want it to post to discord too")
- A quality escalation ("add way more test i need it to work bullet proof")

He does not say "now that that's done, can you also..." — he just states the next thing as if it was always the plan.

## Examples

**After agent announces all 14 tests pass:**
> "set it up so we can track all frontend problemds too in sentry.io and autofix them"

**After agent announces Discord post done:**
> "after claude fixes an automatically reported error in github, i want it to post to discord too that it fixed an auto reported error etc"

**After agent announces sandbox shell tools implemented:**
> "add way more test i need it to work bullet proof"

**After agent announces metrics audit:**
> "do all of it"

**After agent announces style cleanup done:**
> "go harder in a loop comphrensive"
