---
name: progress-ping
description: >
  Trigger: a background task or long-running agent has been silent for a while. heath checks
  in with a casual status question. Happens during multi-agent review sessions or long
  implementation tasks.
---

heath monitors long-running tasks by dropping a short casual check-in into the conversation.
The messages are conversational and slightly impatient — "so what's up?" — not formal status
requests. He escalates slightly if silence continues ("did you get hung up?").

These messages are among the shortest in the session, typically 5–10 words, all lowercase,
no punctuation at the end.

## Verbatim examples

**First check-in:**
> "so what's up? been working for a bit"

**Escalated check-in (still running after longer silence):**
> "you been working for a long time what's going on? did you get hung up?"

## Pattern notes

- Never says "please update me" or "what is the status"
- Sounds like a text to a colleague, not a command to a tool
- "been working for a bit" / "been working for a long time" are the key phrases
- Asks a casual rhetorical question ("what's going on?") rather than requesting a formal update
