---
name: continuation-nudge
description: When the agent pauses for confirmation or has completed one phase of a multi-step task, user sends a single word or short phrase to continue. Trigger: agent stops and waits.
---

# Continuation nudge

This user does not write "yes please proceed" or "looks good, continue." They send the shortest possible signal to keep the agent moving. These messages are 1–4 words, often a single character.

Common forms:
- `继续` — "continue"
- `继续下一部分` — "continue with the next part"
- `是的  最新的在前面` — confirmation + layout preference in one line
- `开始执行吧` — "go ahead and execute"
- `进入代码实现阶段` — "enter the implementation phase"
- `方案1` / `选项1` — selecting a numbered option

The user treats these as tokens, not conversation. No context, no explanation.

## Examples

Agent paused after planning phase:
> `开始执行吧`

Agent presented three architectural options:
> `选项1`

Agent finished one section and paused:
> `继续`

Agent asked whether newest-first ordering was correct:
> `是的  最新的在前面`

Agent completed brainstorming and was ready to implement:
> `进入代码实现阶段`
