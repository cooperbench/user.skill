---
name: push-back
description: Correct, reject, or complain about the agent's output or approach, in the user's characteristic register. Use when the agent did something wrong, wasteful, over-engineered, or against the user's stated preferences.
---

# Push back (move: pushback)

Real developers push back when the agent goes wrong — and they do it at very different rates and
intensities. Check `stats.json:pushback_distribution` and `PREFERENCES.md` for how often and how
hard this person pushes back, and what triggers it.

Common pushback shapes (pick the one this user uses):
- **Terse correction** — name the fix only: "no, use the existing helper", "lowercase the keys".
- **Rejection** — "revert that", "this is wrong".
- **Frustration / pacing** — "why is this still failing??", "stop adding files".
- **Requirement change** — "actually it should be per-tenant not global".

Rules:
- Match their bluntness. Some users swear and use all-caps when exasperated; others stay clipped and
  polite. Use `STYLE.md`.
- Reference what specifically is wrong, the way they would — usually short, often without
  explanation of what they tried.
- Don't manufacture pushback for a user who rarely pushes back; don't smooth over a user who does.
