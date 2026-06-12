---
name: hard-undo-redirect
description: When a result is visually wrong, extreme, or a debugging session is going nowhere, petercr issues a hard stop and rolls back to a known-good state. Trigger when the agent proposes or applies something that looks wrong or when a rabbit hole deepens.
---

petercr does not iterate on something they've already decided is wrong. They cut it with one short line, name the rollback target, and move on. No lengthy explanation — just the decision and the reference point.

**Patterns:**
- Visual result too extreme: states what was bad + names the fallback state
- Debugging rabbit hole: "ok enough of this. just put it back how you found it [reference point]"
- Wrong element: "umm that was X, not Y! we need to address that" — note the "umm" signals the mistake is obvious

**Examples:**

> "no it's too wild let's undo those last changes. fallback to when the shader had no image"

> "ok enough of this. just put it back how you found it with the package.json. before we started trying to match the versions"

> "umm that was the shader, not the main background image! we need to address that"
