---
name: takeover-direct
description: Interrupts an agent that is summarizing completed work or presenting options, issuing the next action directive before the agent finishes. Triggers when the result is clearly good enough and the next step is obvious — no need to read the full recap.
---

When the agent has just finished a batch and is writing a summary or presenting "what would you like to do?" options, cut in with the next directive. Do not acknowledge the summary. Do not confirm it was good. Just issue the command.

**Examples:**

After agent posts a full batch summary table:
> `"commit changes, merge locally back to main, create handoff document for next batch"`

After agent completes batch 2 and lists next options:
> `"use the skill finish the branch"`

After agent provides a design decision tree:
> `"Option A"`

**Shape of takeover messages:**
- Imperative sentences, present tense
- Reference specific skill names when the skill is known ("use the skill finish the branch")
- Combine multiple directives with commas ("commit, merge locally back to main, create handoff document")
- Never explains why the previous output didn't need a full read

**Contrast with corrections:** Takeovers accept the work implicitly and redirect forward. Corrections acknowledge something was missing or wrong.
