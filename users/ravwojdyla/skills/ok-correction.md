---
name: ok-correction
description: After any agent response that misses a detail or needs refinement, user opens with "ok," and states the one missing thing as a compact imperative. Trigger: agent completes a subtask but got some format, library, or scope detail wrong.
---

# ok-correction

After the agent delivers a result, ravwojdyla reads it carefully. If something is off — a format choice, a wrong library, a scope that's too broad — they send a single terse correction starting with `"ok,"`. They do not explain what was wrong. They just state what they want instead.

The `"ok,"` is not agreement; it is a transition marker. It signals the agent's work was received but needs adjustment.

## Pattern

```
ok, <imperative correction in 5–15 words>
```

## Verbatim examples

> `"ok, use f strings in the logging, use `,` to make big numbers more readable"`

> `"ok, now remove the label based trigger"`

> `"ok, now fix it on the current branch"`

> `"ok, now all pass the comment to the prompt as extra instructions"`

> `"ok, commit and push"`

## Notes

- Never starts with "actually", "wait", "no" — always `"ok,"`.
- Does not quote the agent or explain what was wrong.
- One correction at a time; if there are two issues, may send two sequential `"ok,"` messages.
