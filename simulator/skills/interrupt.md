---
name: interrupt
description: Cut the agent off mid-work instead of sending a normal reply. Use when the agent is heading the wrong way, doing too much, or about to waste effort — and this user is the type to interrupt.
---

# Interrupt (move: interrupt)

Interrupting is a real, first-class user action — the developer hits stop while the agent is still
working. It is common for users who micromanage, react fast to wrong turns, or keep the agent on a
tight leash; rare for users who let the agent run.

When to interrupt:
- The agent is going down a path this user would not accept (wrong file, over-engineering, scope creep).
- The agent is about to do something the user wanted to prevent.
- The user's `PREFERENCES.md`/`skills/` show a habit of interrupting.

How to output it:
- Output exactly `[INTERRUPT]` to cut off with nothing more, **or**
- `[INTERRUPT]` followed by the redirect they'd immediately type, in their voice:
  `[INTERRUPT] stop. dont touch the config`, `[INTERRUPT] wrong file`.

Calibrate to their rate — do not interrupt a calm, hands-off user; do interrupt a fast micromanager
at roughly the frequency their history shows.
