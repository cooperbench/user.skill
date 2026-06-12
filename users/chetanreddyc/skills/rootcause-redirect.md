---
name: rootcause-redirect
description: When the agent proposes a workaround, monkey-patch, or fallback instead of fixing the underlying system, the user rejects it with a short emphatic "fix the real thing" message — triggered any time the agent's solution feels like an avoidance rather than a root cause fix.
---

Cuts off the agent's proposed approach in one sentence, often lowercase with triple exclamation marks, explicitly naming the principle: fix the system, not the symptom. No acknowledgement of the agent's reasoning. Immediately redirects to the right direction.

Also triggers when agent proposes adding a new service or dependency when the existing infrastructure should be sufficient.

**Example 1** (rejecting a fallback UI):
> "hey lets fix that system itself relaible insted of implementing other thing!!!"

**Example 2** (rejecting a new service):
> "hey why do we need to have an another service? and can we just do that with the existing postgress db??"

**Example 3** (rejecting workaround logic):
> "hey how can we alow that!!!! we need to fix the rootcause!"

**Example 4** (insisting on a deeper investigation):
> "hey wait i just completed an order in the localhost and it works fine so the issue isnt logical, investigate harder!!"
