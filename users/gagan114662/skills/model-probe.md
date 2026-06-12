---
name: model-probe
description: Opens a session by testing the agent's identity, compliance, or format-following before issuing real work. Trigger at session start when the user's first message is a capability/identity check rather than a task.
---

# model-probe

Before trusting the agent with real work, probe its identity or verify it follows constraints.
This may repeat 2-3 times (same question, different phrasing) until satisfied.

## Patterns

- **Identity probe**: ask which model / version is running
- **Format compliance probe**: issue a highly constrained command ("say X in one word", "reply
  with only: Y") and verify the response matches exactly
- **Repetition**: if the first answer doesn't satisfy, ask again verbatim or rephrase

## Examples

```
which model am i speaking with?
```

```
Reply with only: Hello there friend
```

```
Say 'hello' in one word
```

```
Say hello in 5 words.
```

```
Say hello
```

Multiple variants of "say hello" appeared across different sessions — this is a recurring
session-opener, not a one-time curiosity. The user tests format compliance as a warm-up before
delegating real tasks.
