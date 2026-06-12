---
name: product-question-append
description: How kurtn718 appends product/UX/business questions after a technical fix lands — pivots from "did the fix work" to "should we even do it this way for the user / App Store / HIPAA".
---

After partial success on a technical task, kurtn718 often pivots to a product or compliance question appended in the same message. The fix and the question are in one breath.

**UX framing:**
> `"do you think a therapist would want to listen to it later ever?  in the app?  or should we provide an option?  or maybe we keep it simple and have a setting that defaults to remove after upload"`

**App Store / platform question:**
> `"would apple allow me to submit on mac app store with that"`

**Compliance question mid-debug:**
> `"do have to ask how does this affect security, do we scan the rust code elsewhere?"`
> `"what is the dec2025 hippa rule how would i know when they add new rules, and lastly let's go through the questions/decisions"`

**Pattern:**
- Technical directive or status check first.
- Then "and" / "or" / new sentence opens the product angle.
- Questions are genuine; kurtn718 expects the agent to reason through the tradeoff, not just defer.
- Typos common in product questions: "hippa" for "HIPAA", "patent" for "patient".

**Why this matters:** the product question is not a detour — it often reframes the scope of the next subtask. An agent that ignores it and stays on the pure technical track will get a correction.
