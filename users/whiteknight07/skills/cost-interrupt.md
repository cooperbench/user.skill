---
name: cost-interrupt
description: User suddenly pivots away from asking Claude to do work and asks for a self-contained prompt to paste into a cheaper agent, citing cost. Triggered mid-task when the session has already consumed significant tokens.
---

When Whiteknight07 feels Claude is getting expensive mid-session, he doesn't ask the agent to scale back — he asks for a prompt to paste into a different coding agent, effectively ending the current Claude session.

This is a cost-driven interrupt, not a quality complaint. The work is good; the bill is the problem.

**Verbatim example**:

After a long documentation session with many parallel subagents:
> "Give me a deatiled prompt to paste into a coding agent that will do everything we need to do fully end to end. I cant have you do it cuz u are costing me lot."

The message has the hallmarks:
- Typo ("deatiled")
- Casual grammar ("u", "cuz", "lot")
- No anger — just pragmatic cost management
- Requests a complete, self-contained handoff prompt

This may also appear as a literal interruption: `[Request interrupted by user for tool use]` followed by silence or a new direction in the next turn.
