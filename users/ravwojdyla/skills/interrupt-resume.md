---
name: interrupt-resume
description: User interrupts the agent mid-task, then sends "continue as you were" to resume. Trigger: agent is running a long operation or getting verbose mid-task.
---

# interrupt-resume

ravwojdyla uses `[Request interrupted by user]` to stop the agent mid-task, then follows up with `"continue as you were"` to resume without restating the original instruction. This is a pacing and control mechanism, not a correction.

## Verbatim example

Session shows:
```
[Request interrupted by user]
```
followed by:
> `"continue as you were"`

## Notes

- No explanation for why the interrupt happened.
- `"continue as you were"` is verbatim — not "continue", not "go ahead", not "keep going".
- Used sparingly; not a common pattern but distinctive when it appears.
- After resuming, user does not restate context — assumes the agent retains state.
