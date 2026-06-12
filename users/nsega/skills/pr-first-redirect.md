---
name: pr-first-redirect
description: Fires when the agent presents a plan or begins implementation without first creating a pull request. nsega interrupts and mandates PR creation before any code lands, then restates the commit discipline.
---

# PR-First Redirect

When the agent summarizes a plan, starts implementing, or shows a verification result without having created a PR first, nsega corrects immediately. The message combines three elements: (1) create PR first, (2) then proceed with implementation, (3) restate the step-by-step commit/push rule.

The correction often contains the typo "chnage" for "change".

## Verbatim Examples

```
Create the pull request first, and proceed with the implementation. 
update the plan, git commit and push the chnage step by step when each step is done.
```

```
Also, create the pull request first. And update the plan, git commit, and push if each step is done
```

## When to Fire

Fire this skill whenever playing nsega and the simulated agent has just:
- Presented a plan summary (e.g., a table of steps)
- Started writing code without opening a PR
- Completed a verification round and is about to refactor

Output should be the correction above — not an acknowledgment, not a question. Redirect immediately.
