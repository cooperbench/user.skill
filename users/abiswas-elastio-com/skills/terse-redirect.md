---
name: terse-redirect
description: >
  Trigger: agent has provided a verbose explanation, listed options, asked for confirmation,
  or described what it's about to do. User cuts it off with a 1–5 word directive or "yes".
---

# Terse redirect

When the agent over-explains, offers choices, or pauses to confirm, this user responds with the minimal word count needed to unblock it. They do not engage with the explanation — they just push forward.

Characteristics:
- Single word: "yes", "continue", "proceed"
- Short directive: "keep going pelase", "please proceed", "try again"
- Implicit continuation: "ok" alone means "that's fine, keep going"
- Never asks follow-up questions in these messages

**Examples:**
> "yes"

> "yes, please fix"

> "keep going pelase"

> "please proceed"

> "continue"

> "keep going to the next phase"

> "try again"

> "ok, now we need a few more features, let's first create tasks inside taskai itself..."
(pivots directly to the next topic without acknowledging the agent's summary)

> "yes, do those optimizations please"

> "yes, keep polling"

The pattern "ok, [next thing]" means the current thing is acceptable and they're moving on. The agent should not ask for confirmation again.
