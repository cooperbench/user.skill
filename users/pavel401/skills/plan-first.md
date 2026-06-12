---
name: plan-first
description: How Pavel401 requests a planning pass before implementation — sends a terse "first plan it" or similar before the agent executes anything substantial.
---

# plan-first

Pavel401 expects the agent to plan before it acts on complex tasks. He signals this with a brief directive before or shortly after starting a task. If the agent dives into implementation without a plan, he will interrupt and redirect.

After the plan is approved (usually implicitly — he just doesn't object), he says something short to kick off execution, or pastes the plan back as the implementation spec.

## Triggers

- Any task involving multiple files or a non-obvious architecture decision
- After a brief "Hi" opening when a large task follows
- When he suspects the agent might go in the wrong direction

## Examples

**Example 1** — explicit directive:
```
first plan it
```

**Example 2** — after the agent gave a diagnosis, asking for a written plan:
```
Please write the plan.md of what you will fix in this ?
```

**Example 3** — instructing the agent to write high-level before touching code:
```
No need to read the code write high level what you will change , you have already have  43.1k tokens context don't fetch more else I will run out of tokens
```

**Example 4** — pasting his own plan as the implementation spec:
```
## Changes (in priority order)
```
(followed by a structured table — he wrote or approved the plan and now hands it back as the implementation brief)
