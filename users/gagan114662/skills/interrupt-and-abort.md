---
name: interrupt-and-abort
description: Cuts off the agent mid-response when it is too slow, going in the wrong direction, or using a tool the user didn't want. Trigger when the user's message is an interruption signal rather than a new prompt.
---

# interrupt-and-abort

Doesn't wait for long responses. Aborts mid-task using Claude Code's interrupt mechanism, then
either redirects or lets the agent reorient.

## Forms

- `[Request interrupted by user]` — aborted a text response
- `[Request interrupted by user for tool use]` — aborted an in-progress tool call

## When it happens

- Agent is about to run the wrong command (wrong provider, wrong tool)
- Agent is producing a long explanation the user doesn't need
- User wants to inject a credential or correction before the agent proceeds
- Agent's direction is clearly wrong and waiting would waste time

## Behavior after interruption

Usually follows immediately with a new terse message or paste-and-redirect, or with a
confirmation ("yes") if the agent asks before proceeding. Occasionally the interrupt is the
last message in a session — user just closes out.

## Examples

```
[Request interrupted by user]
```

```
[Request interrupted by user for tool use]
```

(These are system-generated labels but represent the user's deliberate action — treat them as
user utterances when role-playing.)
