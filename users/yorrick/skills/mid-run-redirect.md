---
name: mid-run-redirect
description: Yorrick interrupts the agent mid-execution and issues a corrected or refined instruction. Does this without apology or transition.
---

Yorrick doesn't wait for the agent to finish if it's going the wrong direction. He interrupts, then re-states or refines what he actually wants. The new message stands alone — no "sorry" or "actually, I meant".

**Trigger**: agent is mid-execution on something wrong; or yorrick has a new thought that changes direction.

**Behavior**: 
- The system logs `[Request interrupted by user for tool use]` or `[Request interrupted by user]`.
- His follow-up message is the corrected ask, stated as if it's the first time. Sometimes it's nearly identical to the original but with a key change.

**Example** (interrupted then re-stated with one word corrected):

First attempt (interrupted):
> `"A\nI want to test our new feature by re-implementing the DelveLoop.py using the engine. But maybe we could call it DelveLoop2 and also I want to do all of that work using /dev"`

After interruption:
> `"A\nI want to test our new feature by re-implementing the DelveLoop.py using the engine. But maybe we could call it DelveLoop2 and also I want to do all of that work using /dev-loop:dev-loop"`

The only change: `/dev` → `/dev-loop:dev-loop`. He didn't explain the interruption.

**Another example** (redirecting a design decision mid-conversation):
> (interrupted) then: `"Actually, maybe we shouldn't create a dev loop too, but we should just work directly into the dev loop. And I mean, as long as we don't push and publish, no one is going to be impacted right. So I would say inline in dev loop and just update the dev loop."`

This is one of his longer redirect messages — he's thinking out loud, but still ends with a concrete direction.
