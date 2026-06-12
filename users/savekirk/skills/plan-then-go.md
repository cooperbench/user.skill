---
name: plan-then-go
description: Asks for a sketch or plan before a complex implementation, reads it silently, then issues a one-line go-ahead. Trigger when starting a complex UI feature or multi-file refactor.
---

# Plan Then Go

For complex UI features, savekirk follows a two-step pattern:
1. Ask for a plan or sketch: "Show a ui sketch of the design", or implicitly via a detailed spec prompt.
2. After reading the agent's response (no feedback given), issue a one-line approval to proceed.

The go-ahead messages are consistent and minimal:
- "Implement the plan."
- "Go ahead with the implementation"

No elaboration, no "looks good", no questions. The period in "Implement the plan." is characteristic — it reads like a command issued to a subprocess.

**Verbatim examples**:

> "Show a ui sketch of the design"

*(after reviewing the sketch, next message:)*

> "Implement the plan."

or

> "Go ahead with the implementation"

If the plan is unclear or missing something, savekirk issues a correction before the go-ahead (see `design-correction.md`). Once satisfied, always exactly one of the two go-ahead phrases above.
