---
name: dead-code-hunt
description: How squishykid identifies and removes dead interface methods and exported symbols. Trigger when squishykid is in a refactor/cleanup session and has just learned that something is unused.
---

squishykid probes for dead code by asking "is X used anywhere?" or "is X unused?". When the agent confirms it's dead, squishykid issues an immediate short removal command — no deliberation.

The pattern:
1. "is X used anywhere?" / "is X unused?"
2. Agent confirms it's dead code
3. "lets remove it" / "lets remove X" / "lets remove X and make a commit"

Sometimes squishykid skips step 1 and goes straight to removal, having already inspected the code themselves.

**Example:**
> `is Agent.GetHookConfigPath used anywhere?`
*(agent confirms unused → squishykid:)*
> `lets remove it`

**Example:**
> `is ParseHookInput unused?`
*(agent confirms → squishykid:)*
> `lets remove ParseHookInput and make a commit`

**Example (direct removal):**
> `lets remove HookSuport.GetSupportedHooks`
> `lets remove Agent.SupportsHooks`

After each removal, squishykid asks "what is the difference between X and Y?" to find the next candidate. Removals are done incrementally, one interface method at a time, each followed by a commit.
