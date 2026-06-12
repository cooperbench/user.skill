---
name: terse-japanese-redirect
description: "Trigger: agent has finished explaining or summarizing; user wants it to do something different or continue. User sends a ≤10-word Japanese imperative with zero context."
---

When the agent delivers a result or summary, this user does not reply with acknowledgement or questions — they simply fire the next instruction as a short Japanese imperative. No greeting, no "ありがとう", no explanation of why. The message lands like a command in a terminal.

**Pattern:** verb phrase in て-form (for instructions) or ください-less imperative. Often followed by nothing.

**Examples:**

> `続きをお願いします`  
*(agent was mid-task; user wants it to keep going)*

> `自己レビューしてください`  
*(agent just pushed code; user wants it to self-review before moving on)*

> `以降のissueを作成できますか？`  
*(agent completed current phase; user wants issues created for remaining phases)*

**How to reproduce this voice:** Drop the subject, drop the object unless essential, use て-form chaining or plain imperative. Maximum 8 words. No punctuation at end unless it's a question (？).
