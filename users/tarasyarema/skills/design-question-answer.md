---
name: design-question-answer
description: How tarasyarema answers numbered design questions — inline, numbered, typo-filled, mixing precision and vagueness in the same run-on message
---

# Skill: Design Question Answer

When the agent presents numbered design choices, Taras answers with a dense inline response: he runs through each item by number, uses casual shorthand, mixes clear decisions with "not sure" hedges, and often appends a follow-up question or research request mid-sentence. Typos are normal.

## Example

Agent asked 6 design questions; Taras replied:

```
1. json blob but typed in ts 2. i think A would be nic. also would be really interesting to support stuff like code based matchers, i.e. execute a JS code with specific inputs (typed) and have boolean output 3. for the claude option I meant `--json-schema`, the abstraction should be `query(input: string): T` where T is a zodiac schema or something we could generate JSON schema dict out of, so internally it would route to the provider it needs (openrouter using ai sdk lib first, if not fallback to claude) 4. I think we would need something like wf executions, and we would essentially need to map tasks with wfExecId or something. we would not queue, but rather on demand. but not sure if we need sopmething like a queue anywaqys for some cases, please research best option here 5. I like the event bus approach, optionally make it [...]
```

## Key signals

- Numbers listed inline (not on separate lines): "1. X 2. Y 3. Z"
- "i think A would be nic" — casual abbreviation for "nice"
- Typos: "sopmething", "anywaqys", "zodiac" (for Zod)
- Hedges mid-decision: "but not sure if we need sopmething like a queue anywaqys for some cases"
- Appends research request: "please research best option here"
- Uses technical shorthand immediately: "wf executions", "wfExecId"
- Doesn't stop to format — one continuous paragraph per answer block
