---
name: terse-ack
description: Single-word or single-number acknowledgments used to continue, confirm, or select. Triggers when the agent has presented a batch result, a question, or a numbered list and the user is satisfied or has made a choice.
---

When the previous agent output is acceptable or a choice has been made, respond with the minimal token that moves things forward. No praise, no explanation, no "looks good, please proceed." Just the signal.

**Continuation signals:**
- `"next"`
- `"yes"`
- `"batch 2"`
- `"continue until fished with remaining tasks"`
- `"looks good whats next"` (no apostrophe in "whats")
- `"1"` (selecting option 1)
- `"Option A"` (selecting by label)
- `"accept the improvement"`

**Ranked selection** (when agent lists multiple options and user has a preference order):
- `"they all if I am being honest, in order though 3, 1, 2, 4"`

**Dismissal/reset:**
- `"clear"` (bare — no context, just clear)

**Checking on background work:**
- `"just checking are background aagents still alive."`

These messages carry no markdown, no capitalized "Yes," and no trailing period except for the rare casual sentence ending ("alive.").
