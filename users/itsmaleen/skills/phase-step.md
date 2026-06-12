---
name: phase-step
description: Moves through multi-phase implementation plans one phase at a time, approving each with a short go-ahead message and testing before proceeding. Triggered when working on any feature broken into numbered phases.
---

For larger features (e.g. console-line persistence), itsmaleen does not approve the whole plan upfront and let the agent run. They step through explicitly:
1. Review the plan file and give inline numbered feedback
2. Approve phase 1 with a terse "start implementing" or "start with option 1"
3. Ask how to test phase 1 before authorizing phase 2
4. Approve phase 2 only after phase 1 passes
5. Repeat

Go-ahead messages are one to five words. They do not repeat the plan back or confirm understanding.

Numbered feedback on a multi-item agent proposal matches the agent's list numbering exactly, and may silently skip items they agree with:

> `"1. seems ok for now\n2. keep indefinitely for now\n3. why do we need an export functions?\n4. not yet, not seeing a reason to\n5. yes need to be able to search for a few reasons like resuming a session or turning it into memory\n6. yes"`

**Examples:**

> `"start implementing"`

> `"how can I test phase 1?"`

> `"start with option 1"`

> `"yes continue with phase 2"`

> `"how can we test this phase before moving on to phase 3?"`
