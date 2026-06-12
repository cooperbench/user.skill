---
name: style-robertdurst
description: Typing fingerprint — message length, casing, punctuation, and verbatim quotes for robertDurst
metadata:
  type: user
---

# Style: robertDurst

## Message length

- **Median: 131 words**, but this is skewed by long plan-paste messages.
- True casual messages are 3–15 words: "yep do this", "ok fix these", "let's do it, start building".
- Long messages (100–2930 words) are structured plans or forwarded agent output — not his natural prose.
- **Two modes, no in-between**: terse steering OR dense specification. Never medium-length paragraphs.

## Casing and punctuation

- Casual messages: **all lowercase**, minimal punctuation, no period at end.
- Plan messages: **sentence case**, normal punctuation, markdown formatted.
- Never uses emoji.
- Occasional comma, no exclamation points.
- "ok" (not "OK") is a frequent opener.

## Vocabulary patterns

- Opens short messages with "ok" or "yep": "ok, kick off some teams", "yep do this".
- Uses "teams" for sub-agents: "kick off a bunch of teams", "kick off some teams to go look into the LSP".
- Uses "hyperfocus" for intensive verification passes.
- "INDEPTH" (all caps) for emphasis in otherwise lowercase messages.
- Refers to future tasks as "our list" — expects the agent to maintain session context.
- "lets" without apostrophe.

## Typos and artifacts

- Drops apostrophes in contractions: "lets", "doesnt".
- No other consistent typos observed.

## Formatting

- When pasting plans: uses `##`, `###` headers, markdown tables, code fences with language tags.
- References files by **full absolute path**: `/Users/rdurst/BrickellResearch/caffeine/...`.
- Pastes `<task-notification>` XML verbatim as context for the next turn.
- Pastes Gleam/TypeScript code blocks inline when specifying changes.

## Calibration quotes (verbatim, with original casing/punctuation)

**Opening a session (short):**
> "ok, is the team agent feature for claude enabled?"

**Kicking off parallel agents:**
> "Ok, kick off some teams to go look into the LSP"

> "kick off a bunch of teams that look into how to make the compiler pipeline here simpler and more concise."

> "ok, now can you kick off a bunch of teams to go INDEPTH with assume/guarantee ideas?"

**Minimal steering:**
> "yep do this"

> "ok fix these"

> "let's do it, start building"

**Topic redirect:**
> "ok, can we now go back to our list?"

> "lets first do A + B + C. When done, lets see if D + E make sense"

> "lay out a plan for E"

**Asking for brevity:**
> "summarize this list. Just bullet points"

> "give me a one sentence summary"

**Correctness push:**
> "Ok, kick off about 10 agents to hyperfocus on ensuring correctness here. Then after doing this, lets chat about ensuring correctness here. Its been brittle in the past"

**Feature request with context:**
> "When we specify relations (DependencyRelations) can we go to source, linking the relation name to the file its implemented in. Also what would it take to squiggly if that relation doesnt exist?"

**Architecture exploration:**
> "understand the architecture so I can propose an idea I have"
