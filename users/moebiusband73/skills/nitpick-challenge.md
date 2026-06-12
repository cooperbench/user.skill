---
name: nitpick-challenge
description: >
  Trigger: agent provides an explanation or summary that the user finds technically incomplete
  or subtly incorrect. User responds with a "Why" probe rather than a correction — forcing the
  agent to re-examine its reasoning. Annotated persona "Expert Nitpicker" at 57.4%.
---

When the agent's stated rationale conflicts with the user's mental model, the user does not
say "that's wrong." Instead they ask a "Why" question that exposes the gap, often as a
two-sentence chain ("Why is X. Why does Y."). The tone is neutral and technical — it reads
like a technical interview question, not frustration.

After the agent corrects itself, the user often accepts the clarification with `"Yes please
add a clarification to the README"` or similar — the nitpick resolves into an action.

**Example — challenging a cache sizing explanation:**
> `Why is the option cache-size-mb set to DB size / max-open-connections and not to DB size. Why does this allow to hold the complete DB in memory when the cache size is smaller than the total DB?`

**Example — challenging scope of server resources:**
> `Our server has 512GB main memory. Does it make sense to make cache_size and soft_heap_limit configurable to make use of the main memory capacity?`
(Implicit challenge: "you've hardcoded conservative defaults on a 512 GB machine.")

**Example — understanding question that becomes a challenge:**
> `Does it make sense to also inline the literal state value in other places?`

**Example — narrowly scoped "explain" request (not a challenge, just curiosity):**
> `Explain how Fix 3 works and why this is an improvement`
