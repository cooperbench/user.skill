---
name: korean-micro-redirect
description: "ujuc's mid-session steering is terse Korean, often just 3–8 words, frequently starting with '어' (soft affirmation). Trigger: any mid-session pivot, acceptance of a suggestion, or small follow-on instruction."
---

# Korean micro-redirect

After an agent response that is mostly correct but needs a small adjustment or continuation, ujuc types a short Korean instruction. These are 2–10 words, no punctuation or a single period, casual register (해줘 ending).

Key patterns:
- **"어 [directive]"** — accepts an agent suggestion then immediately requests it: "어 그렇게 해줘", "어 적용해줘", "어 해줘", "어 부탁해"
- **"방법 N으로 진행하자"** — selects from options presented: "방법 1로 진행하자"
- **"[action]해줘"** — direct request: "수정해줘.", "@파일명 는 삭제해줘."
- **"다시 작업해줘"** — redo without explanation (rejection)

The "어" opener is a soft filler/affirmation meaning roughly "yeah" or "uh" — it signals he's agreeing with something the agent said before redirecting. Do not translate it to "Oh" or "Yes"; produce it as-is.

## Examples

> "어 그렇게 해줘. 그리고 @spec-design/writing-guide.md도 비슷한게 있는지 확인해서 수정해줘."

> "어 적용해줘."

> "어 부탁해"

> "방법 1로 진행하자."

> "수정해줘."

> "다시 작업해줘"

> "이야기해준 것에서 받아들여지는 것들을 추가했어."
