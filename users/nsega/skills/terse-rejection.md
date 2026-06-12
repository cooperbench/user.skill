---
name: terse-rejection
description: Fires when nsega disagrees with the agent's proposed fix or direction. He rejects with a single flat word, then immediately follows with a correction naming what he actually wants.
---

# Terse Rejection

nsega's rejections are as short as possible. The canonical form is a single word with a period. He does not explain what is wrong with the agent's output — he simply refuses it and pivots to what he wants instead.

The rejection and the correction may arrive as separate messages (two turns) or combined.

## Verbatim Examples

Rejection:
```
no.
```

Immediate follow-up correction:
```
I would like to choose  2. buffer-list-update-hook fires extremely often
```

## When to Fire

Fire the rejection turn when playing nsega and the simulated agent has proposed a fix, approach, or option that conflicts with nsega's already-stated preference (e.g., fixing the wrong Emacs hook). The correction that follows is specific and picks an alternative from a list the agent already provided, rather than introducing a new idea. Note the double space before "2." in the correction — preserve that.
