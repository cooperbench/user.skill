---
name: terse-steer
description: How KeKs0r steers mid-session with 1–5 word messages. Trigger when the agent
  has just finished a step and is waiting or has asked a question.
---

# Terse steer

The most common mid-session interaction pattern. KeKs0r confirms, continues, or redirects
with the shortest possible message. Responses to agent questions are often a single word.

## Examples

> `yes do it,  we want to get those ingestions functions`

> `yes atuo fix`

> `okay just did, try again`

> `run the commands`

> `continue`

> `Continue from where you left off.`

> `okay great, start resetting everything`

> `yes`

> `rebase with main.  and then continue.`

> `execute the request`

> `okay mark the task in the analysis file as done`

> `can you run the cp command?`

## Characteristics

- No explanation of WHY he's confirming — the previous agent message contains the context.
- Typos common at this length: "atuo" instead of "auto".
- Often double-spaced after commas or periods.
- "Continue from where you left off." appears verbatim multiple times — copy-paste artifact.
- When he says "run the commands" he means: do the thing you just described, don't ask again.
