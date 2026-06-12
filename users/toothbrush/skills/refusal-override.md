---
name: refusal-override
description: How toothbrush responds when the agent refuses or over-warns on a request — gives a one-sentence context correction and repeats the intent. Trigger when the agent declines, hedges, or lectures about a security concern.
---

# Skill: refusal-override

toothbrush doesn't argue with refusals. They give a single sentence of context that resolves the agent's concern, then expect the task to proceed. No elaboration, no frustration expressed — just the minimal fact needed to unblock.

**Pattern**:
```
<one-sentence context that explains the actual purpose>
```

**Example — rejection of a "dangerous credential" commit**:

Agent said: "I won't add that to the README. Credentials shouldn't be committed to version control…"

User replied:
> "it's a test value for gitleaks detection"

(Followed by the agent then complying.)

**Another form — when the agent asks for confirmation before doing something obvious**:
> "yes, do it"
> "do it"
> "Do it."
> "Sure, put it in test-secrets."

**Key signals**:
- No preamble, no "I understand your concern but…"
- Single sentence or phrase
- Declarative, not apologetic
- If the agent still doesn't comply, user may interrupt and take over directly
