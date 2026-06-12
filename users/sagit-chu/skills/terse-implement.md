---
name: terse-implement
description: After a plan or analysis is established, issues a single-word or two-word Chinese command to begin execution. Trigger when the agent has finished scoping a task and is waiting for a go-ahead.
---

Once the agent has presented a plan or analysis, sagit-chu does not say "please proceed" or "that looks good, go ahead." They fire a single imperative and nothing else.

Common triggers:
- Agent finishes a plan document or scope analysis → `实施`
- Agent describes a fix but hasn't applied it → `实施修复`
- Agent pauses asking for confirmation → `开始实施`
- Agent is partway through a multi-step task → `继续`
- Agent presents a completed plan and is ready → `实施`

**Examples:**
```
实施
```
```
开始实施
```
```
继续
```
```
实施修复
```

Never adds explanation, rationale, or acknowledgment. If the agent just finished a long analysis, the user's entire reply is the single action word.
