---
name: vague-opener
description: Opens sessions with 1–3 word prompts or a single sentence that names a feature/problem area but provides no file paths, error messages, or implementation context. Triggered at the start of a new session or new work block.
---

itsmaleen frequently opens sessions with the minimum viable description — a feature area, a single verb, or a brief symptom report. They expect the agent to read recent changes, explore the codebase, and surface what's relevant before asking for clarification.

The opener is almost never a complete specification. It may be:
- A single noun: the feature or system to work on
- A terse verb phrase: what they want to happen
- A brief symptom with no stack trace: just the observable problem

The agent is expected to investigate without prompting for more context.

**Examples:**

> `"auth"`

> `"config"`

> `"see the recent changes made? Having issues with agent console not being able to scroll"`

> `"Something in the recent changes has broken the build version of the app and now server won't start. Don't make any edits but investigate what happened that broke server. It's probably a change that has to do with analytics"`
