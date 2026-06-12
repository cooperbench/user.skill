---
name: design-challenge
description: >
  Trigger: agent has implemented something with a structural assumption the user did not ask for
  (e.g., a required "name" column). User notices the assumption and questions it — not to understand
  the code, but to argue it should be removed or changed.
---

The user asks a one-sentence question in plain Japanese: "why does X have to be Y?" — then immediately follows with their own preferred alternative in the next message if the agent's explanation doesn't convince them.

The question is short and uses `なぜ？` or `ということ？`. It is not a request for a code tour; it is the opening move of a negotiation about design.

**Example (challenge):**

> `名前列が必ずあるのはなぜ？`
> *(Why does the name column have to be there?)*

**Example (follow-up after agent explains):**

> `識別子が必要ということ？であればランダムのIDde`
> *(So an identifier is needed? In that case, a random ID [de — fragment, implies "is fine / would work"])*

The follow-up cuts off: `de` is the unfinished particle `で`, meaning the user typed their conclusion, hit enter, and the agent should infer "a random ID would suffice." The user does not complete the sentence.
