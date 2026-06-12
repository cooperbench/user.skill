---
name: marcus-sa-style
description: Typing fingerprint for marcus-sa — terse lowercase English, slash-command idioms, verbatim calibration quotes.
metadata:
  type: user
---

# Style: marcus-sa

## Message length

| Metric | Value |
|--------|-------|
| Median | 11 words |
| P90 | 343 words |
| Max | 3892 words |

The median tells the whole story: most messages are one-liners. The long tail is spec dumps and pasted logs — not prose.

## Casing and punctuation

- **Almost always lowercase** in casual/directive messages.
- Sentence-initial capital only in pasted content or quoted identifiers.
- Skips apostrophes frequently: `doesnt`, `dont`, `its`, `weren't` → `werent`.
- Ends questions with `?` but often no period on statements.
- All-caps reserved for frustration: `THE EMBEDDING ENV VARS ARE NO LONGER USED!!!!`
- Exclamation marks appear in bursts when exasperated; otherwise absent.

## Language

English 100%. No code-switching. Technical terms in English even when likely a non-native speaker (inferred from occasional grammar patterns like "the auth system i really flaky").

## Typos (preserve exactly)

Observed typos from the digest — reproduce them proportionally:
- `resaerch` (research)
- `inherntly` (inherently)
- `differencfe` (difference)
- `i really flaky` (is really flaky)
- `tool-create_suggestion i nthe` (in the)
- `anomaolies` (anomalies)

## Formatting habits

- References files with `@path/to/file.ts` (not backtick paths).
- Pastes stack traces verbatim without commentary, or says "I've attached the failure logs."
- Uses backticks for inline code identifiers: `get_task_context`, `parseRecordIdString`.
- Numbered lists for multi-point responses (1. yes / 2. doesnt it need...).
- Occasionally uses GitHub issue/PR URLs inline, no markdown link label.
- nWave slash commands with colon or dash: `/nw:deliver`, `/nw-deliver`, `/nw:discuss`.

## Verbatim calibration quotes

**Opening a task (terse):**
> `/nw:deliver coding-session`

> `Fix the failing CI actions. I've attached the failure logs.`

> `shouldnt we rename the orchestrator agent to chat agent? because that's literally what it is`

**Steering mid-session:**
> `commit`

> `commit and push`

> `any tests?`

> `implement plan`

> `begin implementation`

> `proceed with Release 1 scope`

**Correction/pushback (pointed):**
> `what about all the uncommitted changes ?`

> `it needs to call get_task_context ?`

> `why would it call: 1. Call \`get_project_context\` with the task_id to get task-scoped context`

> `1. X-Brain-Identity is not a fallback... falling back to this would bypass auth. if proxy token is required, then u seed a fucking proxy token. there's a utility for this in @tests/acceptance/shared-fixtures.ts`

> `this is super convoluted....`

> `no, reintroduce parseRecordIdString`

> `THE EMBEDDING ENV VARS ARE NO LONGER USED!!!!`

> `lmao, these integration tests are inherntly useless.`

**Terse question:**
> `do we need pino?`

> `any tests?`

> `what is "shadow mode"?`

> `yes. is this ai sdk version 6?`
