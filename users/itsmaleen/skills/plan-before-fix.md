---
name: plan-before-fix
description: When a bug has persisted through multiple failed fix attempts, explicitly asks the agent to stop making changes and produce a plan first. Triggered after 2+ consecutive failure reports without resolution.
---

itsmaleen tolerates iterative debugging, but when a loop repeats without progress (same or similar error on the next CI run), they explicitly brake the agent: stop editing, think, and plan.

The request is always a short imperative. It may:
- Ask for a plan before authorizing the next change
- Ask the agent to explain how its current diagnosis actually connects to the observed error
- Request that the investigation happen outside the working directory

After the plan is produced, they review it and either approve incrementally ("yes go ahead and try it") or ask a pointed clarifying question about a specific step.

**Examples:**

> `"Before making changes again, let's plan what needs to change - suggest a plan"`

> `"how does that relate to this error?\n  security: SecItemCopyMatching: The specified item could not be found in the keychain."`

> `"Don't make any edits but investigate what happened that broke server. It's probably a change that has to do with analytics"`
