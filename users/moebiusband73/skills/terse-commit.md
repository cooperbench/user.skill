---
name: terse-commit
description: >
  Trigger: agent has finished implementing changes and the user wants to commit. User issues
  a 2–3 word imperative. Occasionally takes over and commits manually (takeover, 2%).
---

After successful implementation, the user signals "done, commit it" with minimal words.
Never specifies a commit message — leaves that entirely to the agent. The three forms used:

**Examples:**
> `commit it`

> `commit the changes`

> `commit this`

The takeover variant (user commits himself without saying anything) accounts for 2% of
sessions. The agent should treat silence after a completed implementation + a prior terse
commit prompt as a signal to not re-propose committing.

Mid-session git requests also stay terse:
> `Check if the fixes are correctly merged in nodes.go`

> `Update cc-backend to latest master HEAD`
