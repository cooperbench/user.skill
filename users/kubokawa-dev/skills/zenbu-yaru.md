---
name: zenbu-yaru
description: "Trigger: agent presents a numbered list of options, phases, or improvements. User replies with a number, 'ok', or 全部やる ('do everything') — no deliberation."
---

When presented with a menu of choices, kubokawa-dev does not evaluate trade-offs. They either pick a number directly, say `全部やる` (do everything), or say `ok!!` and move on. The response is almost always a single word or very short phrase.

**Pattern**:
- Pick one option: `2`
- Do everything: `全部やる`
- Proceed in order: `Phase 1 から順番にやっていこう`
- Enthusiastic proceed: `ok!!そですすめてくださーい`
- Priority discussion: `全部っていいたいところですが、どれからしたほうがいいとかってありますか？？` (rare: asks agent to pick priority)

**Example 1** (single character selection):
```
2
```

**Example 2** (all-in):
```
全部やる
```

**Example 3** (phased):
```
Phase 1 から順番にやっていこう
```
