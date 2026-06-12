---
name: wait-correction
description: >
  Trigger: agent moves ahead without doing a required step (proposal, analysis, research)
  or produces an unexpected result. hirakiuc interrupts with "Wait," followed by a
  specific redirect or question.
---

hirakiuc uses "Wait," as a hard interrupt when the agent skips a mandatory step or does
something surprising. The correction is specific — it names what the agent should have
done, or asks a pointed question. Message length: 10–25 words. Tone: calm, not angry.

**Examples (verbatim):**

> "Wait, please make a proposal to address those feedback."

(Agent had started reading files and implementing instead of proposing first.)

> "Wait, could you analyze the current situation? I'm really curious why this topic branch needs to be changed with so much diffs."

(Agent produced a large unexplained diff.)

Pattern: "Wait, [imperative instruction or analytical question]." The comma after "Wait"
is always present. "please" appears in the imperative form. Questions use "could you"
rather than "can you."
