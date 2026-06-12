---
name: terse-correction
description: How malkoG corrects the agent — short, pointed redirect, no explanation; fires immediately when the agent does the wrong thing
---

# Terse Correction

When the agent does something wrong, malkoG fires a single sentence naming the problem. No preamble, no apology, no explanation of why it's wrong. Just the correction.

The correction often:
- Starts with "Wait," when it's a factual error the agent just made
- Starts with "Okay," when acknowledging the agent's confusion before correcting it
- Names the right value directly: "Okay correction. not 1.0.1, 1.1.0"
- Ends the conversation there — no "please fix this" follow-up

**Examples:**

Agent opens PR to wrong repo → user replies:
> "Wait, it should point at hackerspub/android."

Agent says `hackerspub/android` doesn't exist → user replies:
> "Okay, it was hackers-pub"

Agent implements HTML tag highlighting instead of code block syntax highlighting → user replies:
> "Not highlighting html, syntax highlighting code snippet. Got it?"

Agent renders `<span><code>` markup visible in the output → user replies:
> "But, it renders starts with <span><code>..."

Agent uses wrong version number → user replies:
> "Okay correction. not 1.0.1, 1.1.0"

Agent filed a note instead of a GitHub issue → user replies:
> "I mean, github issue"
