---
name: detail-correction
description: Short redirect when the agent completes a task but misses one specific detail — a file not updated, a variable not renamed everywhere, a trigger not actually changed. Triggers after accepting the bulk of the work but noticing a gap.
---

Corrections are 1–2 sentences. They name the missing thing specifically, often as a question ("did you update the HANDOFF.md to point to the latest doc") or a brief observation ("hmmm the trigger wasn't changed"). They do not explain why it matters. They do not re-describe the overall task.

**Pattern types:**

*Missed file/reference:*
> `"did you update the HANDOFF.md to point to the latest doc"`
> `"can you updaate any other documentation or code references to GOOGLE_API_KEY"`

*Silent non-change:*
> `"hmmm the trigger wasn't changed"` (soft "hmmm" opener, no capital, no explanation)

*Scope redirect after seeing options:*
> `"let's adjust the skill content directly this time"` (implies agent ran an indirect approach; user wants direct file edit)

*Naming problem identified:*
> `"it seems the generate-evaluator is both a skill and a slash command, confirm this is true and offer proposals for consildation or if valuable having distinct names"`

**Signature cues:**
- Starts with "hmmm" for soft surprise (not anger)
- "can you [verb]" for polite missed-scope
- "did you [verb]" for verification gap
- "let's [verb] directly this time" for approach correction
- Typos present as normal ("consildation", "updaate")
