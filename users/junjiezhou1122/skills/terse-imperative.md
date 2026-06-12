---
name: terse-imperative
description: "Trigger: agent completes a step or is mid-task; user sends a 1–5 word command to continue or pivot without any explanation."
---

When the agent completes a task or pauses, junjie responds with the shortest possible next command — often a single word or a terse imperative with an exclamation mark. No context, no explanation, no politeness.

**Pattern**: `[verb] + [object]?` in Chinese or English, sometimes just a single word.

**Examples**:
- `"continue"`
- `"commit一下"`
- `"先全部实现一下！"`
- `"Now first implement spec 006!"`
- `"先做一个最小的可用版本！"`
- `"用mcp吧 也可以的！"`
- `"先这样！ 我们先做demo而已！"`

The exclamation mark is standard, not emphatic. Length is the signal — if the previous agent turn was correct, the reply is short. Longer replies indicate correction or new direction.
