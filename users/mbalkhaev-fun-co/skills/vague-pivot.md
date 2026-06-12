---
name: vague-pivot
description: After a sprint closes (agent gives a long ✅ summary), user immediately pivots to the next high-level goal without acknowledging the completed work
---

The agent delivers a detailed recap of what was done. The user ignores it entirely and opens the next objective with a broad, under-specified Russian sentence. No "great", no "thanks", no continuity reference. The pivot is the only content.

**Trigger**: agent finishes a sprint and summarizes results.

**Pattern**: 5–15 word Russian sentence stating a new goal, often using "надо" (need to) or "нужно" (need to).

**Examples**:
> `Надо лучше связать timeline (diff) с кодом и сделать всю навигацию более связанной`

> `А теперь надо значительно улучшить Code чтобы с детальной страниец со всей инфой`

> `Нужно лучше понимать кодовую базу и в целом code quality`

> `Generating recommendations...`
> `надо генерировать рекомендации по клику и с подпись что будут потрачены токены`
(here the UI label from the screen is pasted, then the instruction — showing exactly what triggered the thought)

Note: "страниец" is a typo for "страницей" — preserve this in roleplay.
