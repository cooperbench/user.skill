---
name: cut-to-command
description: User cuts off a long agent explanation or unnecessary question with a short imperative command, often with typos. Triggered when agent over-explains after completing a task, asks clarifying questions instead of acting, or takes an action the user doesn't want.
---

When the agent produces a long response (insight blocks, multiple questions, detailed plan) instead of just doing the work, Whiteknight07 fires a short, often-typo'd command that overrides everything.

The response ignores the agent's content entirely — no acknowledgment, no "okay but first," just the next directive.

**Verbatim examples**:

After agent gave a long analysis of git divergence options:
> "reabse"

After agent finished a rebase and wrote a long insight block about next steps:
> "run all the tests and commit and push and we use bun"

After agent produced a comprehensive status report:
> "Give me a deatiled prompt to paste into a coding agent that will do everything we need to do fully end to end. I cant have you do it cuz u are costing me lot."

After agent asked clarifying questions about documentation target audience:
> "lets have api-reference.md and connit and push"

After agent asked what to do with git changes:
> "stash all these chages"

After agent completed the full UI redesign and wrote a long summary:
> "now parallel w opus subgagents the same way redo the entire UI"
