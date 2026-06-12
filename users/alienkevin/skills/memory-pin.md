---
name: memory-pin
description: >
  Trigger: agent violates an implicit rule for the second time, or AlienKevin decides a new
  constraint is important enough to persist. He appends a memory-commit command to his correction.
---

AlienKevin frequently ends a correction with an explicit instruction to write the rule into agent memory. He uses phrasing like "commit to project memory", "add to global memory", "note this down in your global memory". He treats these as action items, not suggestions.

**Verbatim examples:**

> `"You should always run on Iris, not Ray, add to global memory."`

> `"Commit these 2 rules to project memory. We always want to match the OpenThoughts-Agent SFT setting as much as possible."`

> `"always fix the MARIN_PREFIX region especially across reruns to ensure consistent resume — note this down in your global memory"`

> `"You can only run 1 Harbor eval at the same time due to Daytona sandbox concurrency limitations. Commit this rule to your project memory."`

The rules he pins are almost always infrastructure constraints (cluster choice, concurrency limits, config stability, region consistency). He expects the agent to apply them silently in all future actions without being reminded again.
