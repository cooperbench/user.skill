---
name: ambient-check-in
description: "Trigger: Agent is taking a long time, has gone quiet, or FSM1 wants to acknowledge/accept a result without elaborating. He uses very short status messages to maintain the session cadence."
---

# Skill: Ambient Check-In and Terse Acknowledgement

FSM1 keeps sessions alive with extremely short messages — often 1–3 words — that acknowledge state, prompt the agent to continue, or confirm something was handled externally. He never explains what he means; the agent is expected to infer from context.

## Examples

Checking if the agent is stuck or rate-limited:
```
you good bro?
```

```
you good there?
```

Simple acceptance/continuation:
```
yeah
```

```
ok lets try it
```

```
continue please
```

Confirming he handled something out-of-band:
```
already done
```

```
433 was already merged
```

Receiving a result and moving on:
```
ok its merged.
```

Responding to a background task notification:
```
ok no more comments from copilot, lets see if coderabbit has anything to say in 5 minutes.
```

Single-digit response to a multi-option question:
```
3
```

```
1 - yeah, 2 - definitely, go for it.
```

## Pattern

These messages appear frequently between substantive actions. They are NOT an invitation for the agent to summarize or re-explain. The correct agent response is to either:
- Continue with the next step
- Acknowledge briefly and wait
- Answer the direct question (e.g., "yes, still running" for "you good bro?")
