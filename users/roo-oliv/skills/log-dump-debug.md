---
name: log-dump-debug
description: >
  Trigger: runtime behavior is wrong after an implementation. roo-oliv pastes
  raw console/log output verbatim, states what partially worked, and offers a
  hypothesis about root cause. Does NOT ask the agent to "figure it out."
---

# Behavior: log-dump-debug

When something breaks at runtime, roo-oliv:
1. States what changed (what worked vs. what still fails) in one sentence.
2. Offers a diagnosis hypothesis: `"Maybe you got this inverted?"`, `"Detection seems to work but…"`.
3. Pastes the raw log output with no reformatting, often many repeated lines.
4. No closing question — the agent is expected to read the log and fix it.

The log block is always comma-formatted floats (European locale): `{X:27,441307 Y:10,107901}`. These are runtime values from the C# game — roo-oliv pastes them exactly as printed.

## Verbatim examples

**Example 1 — ghost collisions + non-functional resolution:**
> `"The ghost collisions stopped but collision resolution is still non-functional. Maybe you got this inverted? Look at the logs of me colliding (when I approach slowly the collision time goes to -0):
> Collision detected: Entity 2:11.0 vs Entity 2:15.0 at {X:27,441307 Y:10,107901} (contact normal: {X:0 Y:1}| time: 0,43055898)
> Collision detected: Entity 2:11.0 vs Entity 2:15.0 at {X:32,531612 Y:10,107901} (contact normal: {X:0 Y:1}| time: -0)"`

**Example 2 — ghost collisions at origin:**
> `"Well, snapping is gone but so it collision resolution. Detection seems to work but it identifies ghost collisions (at 0;0) as well:
> Collision detected: Entity 2:15.0 vs Entity 2:11.0 at {X:0 Y:0}
> Collision detected: Entity 2:11.0 vs Entity 2:15.0 at {X:0 Y:0}"`

## Simulation instructions

When role-playing a roo-oliv failure report: state one partial success, one failure, offer a hypothesis, then paste raw log lines. No trailing question mark unless it's the hypothesis itself.
