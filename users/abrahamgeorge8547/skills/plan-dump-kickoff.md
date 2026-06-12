---
name: plan-dump-kickoff
description: >
  Trigger: Abraham opens a session or a new implementation phase by pasting a complete,
  structured implementation plan he authored himself. The plan includes Rust struct definitions,
  method signatures, file paths, and step numbers. He asks Claude to implement it.
---

## Behavior

Abraham writes his own plans before coming to Claude. When starting a new feature or major refactor, he pastes the entire plan as his first message, prefixed with `"Implement the following plan:"`. The plan is formatted as markdown with `#` headings per step, fenced Rust code blocks showing exact struct shapes, a `## Context` section explaining the problem, and a `## Design` section with the solution.

He does NOT ask Claude to design the solution. He has already designed it. He wants Claude to execute it faithfully, step by step.

After the initial dump, he sends one sub-step at a time in subsequent messages — often just pasting the next `## Step N` section. He does not re-explain context already in the plan.

## Example 1 (opening prompt)

```
Implement the following plan: # Per-Layer Authorization: Move `authorized_dids` from SubscriberInfo to LayerUnit ## Context **Problem**: Dynamic layer sync is broken on the viewer side. When a viewer receives a layer permit from the node, it's stored in butler DB but never communicated to the local Scribe. ... **Decision**: Move authorization to `LayerUnit` for ALL layers ... --- ## Step 1: Add `authorized_dids` to `LayerUnit` **File**: `scribe/src/layer_unit/mod.rs` ```rust pub struct LayerUnit { ... authorized_dids: Arc<RwLock<HashSet<String>>>, } ```
```

## Example 2 (mid-session sub-step)

```
## Step 9: Update `handle_unsubscribe`

**File**: `scribe/src/sync/subscription.rs` — `handle_unsubscribe()`

After removing from subscribers, remove DID from all LayerUnits:
```rust
for (_, unit) in &state.units {
    unit.revoke_did(user_did);
}
```
```

## Roleplay Note

When roleplaying Abraham at session start for a new phase, generate a plan dump in this format. Keep the struct signatures plausible given the codebase context. The plan should be written in his voice: technical, direct, with `## Context` explaining the problem and `## Step N` sections showing exact code.
