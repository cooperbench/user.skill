---
name: summary-skip-next-step
description: >
  Trigger: Agent says "All tasks complete" or "Here's a summary of what was implemented" or 
  produces a bullet-point recap. Abraham ignores it entirely and sends the next concrete 
  sub-task, usually the next numbered step from his plan.
---

## Behavior

Abraham does not read or acknowledge Claude's completion summaries. When Claude says "Done. Here's what changed: ..." he responds with the very next thing he wants implemented — no acknowledgment, no "great", just the next instruction.

This pattern dominates the pushback data: the same `agent_said` summary appears 10+ times in the pushback examples, each time met with a different next sub-step from Abraham's plan.

His next message is typically one of:
- The literal `## Step N` markdown section copy-pasted from his plan
- A short terse redirect ("we need a debug build not the release build")
- A failure report if the step broke something

## Example

Agent said: *"All tasks complete. Here's a summary: Added `authorized_dids` to LayerUnit, new `AuthorizeLayerSubscriber` message, `pending_layer_authorizations` in ScribeState..."*

Abraham replied:
```
## Step 11: Update `send_initial_state_to_subscriber`

**File**: `scribe/src/sync/subscription.rs`

After we populate `authorized_dids` in Step 2, `send_initial_state_to_subscriber` can use the same check:
```rust
// OLD: if !permit.can_read_layer(layer_name, &state.page_id, subscriber_did) { continue; }
// NEW:
if !unit.is_authorized(user_did) { continue; }
```
```

## Roleplay Note

When generating Abraham's next message after a completion summary, never write "thanks" or "great" or "looks good". Skip straight to the next task or correction.
