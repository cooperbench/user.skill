---
name: status-pulse
description: >
  Trigger: user sends a short status-check message during an ongoing experiment, paper edit,
  or VM job. Fires on any variant of "how is everything", "ETA", "how is it now", "how good is
  the paper now", "any still running experiments", "so no more experiments are running".
---

# status-pulse

henryph24 checks in frequently with ultra-short status queries. He expects the agent to
synthesize current GPU state, experiment progress, and paper acceptance estimate — all without
being given any new context. These are never questions; they are requests for a full situational
report delivered immediately.

The query is always 2–6 words, often no punctuation, often lowercase, sometimes grammatically
incomplete. He never explains what he wants summarized.

## Pattern

- 2-6 words
- Lowercase (sometimes first-word cap)
- No punctuation or minimal punctuation
- No slash command

## Verbatim examples

> `how is everything`

> `how is it now`

> `ETA`

> `So how is everything now?`

> `by now can we have a borderline accepted paper`

> `how good is the paper now for neuralips 2026`

> `any still running experiments`

> `so no more experiments are running at RACE VM`

> `how are the running experiments`

> `how are our experiments so far`

## What he does NOT say

He does not say "can you give me an update on the experiments and paper status" — that is an
assistant's framing. He just fires the minimal question and trusts the agent to know the context.
