---
name: letter-picker
description: When the agent presents lettered options, yorrick responds with just the letter (or letter + brief qualifier). He does not restate the option or explain his choice.
---

Yorrick reads menus and picks. He does not explain, hedge, or restate. If he wants a slight variation on the chosen option he adds a clause after the letter.

**Trigger**: agent presents a numbered or lettered list of options/approaches.

**Behavior**: reply is the letter or number alone, or the letter followed by a one-sentence modification.

**Examples**:

> Agent: "A) Minimal async graph engine … B) Layered engine with plugin hooks … C) …"
> Yorrick: `"A\nI want to test our new feature by re-implementing the DelveLoop.py using the engine. But maybe we could call it DelveLoop2 and also I want to do all of that work using /dev-loop:dev-loop"`

> Agent: "1. Change effort to max permanently … 2. Or launch with flags …"
> Yorrick: `"2"`

> Agent: "(Multiple brainstorming options presented)"
> Yorrick: `"c"` or `"C"` or `"yes"` or `"ok"`

> Agent: (follow-up with sub-options)
> Yorrick: `"c) I want to be able to run claude -p and also codecs and also the Gemini coding tool, all three in headless mode."`

Note: the letter can be uppercase or lowercase inconsistently. The one-sentence add-on often contains his characteristic typos ("codecs" for Codex, "cloud-b" for claude -p).
