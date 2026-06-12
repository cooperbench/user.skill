---
name: продолжай-continue
description: When the agent pauses mid-task or finishes a step but more work remains, user sends a bare continue prompt in Russian
---

The user does not narrate what they want continued. They just push the agent forward. The word is either lowercase or capitalized inconsistently. In long task chains (e.g., fixing 10+ TUI errors) this message repeats 8–10 times in a row.

**Trigger**: agent output ends with a checkpoint, a question, or mid-plan stop.

**Variants** (in rough frequency order):
- `продолжай`
- `Продолжай`
- `Делай дальше`

**Examples**:
> `продолжай`

> `Продолжай`

> `Делай дальше`

Never adds "please", never specifies what to continue, never asks if the agent is ready.
