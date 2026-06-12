---
name: casual-kickoff
description: How Pavel401 opens sessions — often with a single word or vague line, then follows up with more detail only after the agent responds or he orients himself.
---

# casual-kickoff

Pavel401 does not always open with a complete task description. He often starts with a minimal opener ("Hi", a bare question, or a short intent statement) and waits for the agent to orient or respond before dumping the real content.

The contrast is stark: his opening might be one word, but the second message might be 9,000 words of raw logs.

## Pattern

- Minimal opener → context dump in follow-up
- Vague opener → clarifying question → he answers with paste or spec
- Single question → expect agent response → then he pivots or confirms

This is not a sign of vagueness about his goal — he knows what he wants. It's a pacing habit.

## Examples

**Example 1** — single word:
```
Hi
```

**Example 2** — short question with local path (implies specific file review):
```
Review the current /Users/skmabudalam/Documents/BugViper/ingestion_service/languages/python.py does it store the repo path properly ?
```

**Example 3** — short conceptual question:
```
How does Coderabbit and Greptile handles it ?
```

**Example 4** — short confirmation question:
```
Is the files , functions and lasses count correct ?
```

**Example 5** — vague single-line redirect after context exists:
```
Continue from where you left off.
```

**Example 6** — short check-in:
```
bro I just ingested can you check the stats now
```
