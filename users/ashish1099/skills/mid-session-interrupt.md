---
name: mid-session-interrupt
description: Cancels an in-progress tool call when the agent's execution diverges from intent — triggered when a tool action would produce an unwanted side effect.
---

ashish1099 does not wait for an errant tool call to complete before correcting it. When Claude
Code runs a tool (file edit, shell command, git operation) in a direction they did not intend,
they hit the interrupt before the call finishes. This surfaces in the transcript as:

> "[Request interrupted by user for tool use]"

This appeared twice in the mid-session prompts. The interrupt is the correction — no
explanatory message follows in the same turn. The next message either redirects or takes over
with a direct command.

The pattern reflects a low tolerance for wasted steps: if the agent is about to do the wrong
thing, stopping it immediately is cheaper than undoing it afterward. This pairs with the
[[git-takeover]] pattern: interrupt → takeover with exact instruction.
