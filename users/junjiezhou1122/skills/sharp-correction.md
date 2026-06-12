---
name: sharp-correction
description: "Trigger: agent builds something that misunderstands the user's intent, over-engineers, or violates the conceptual model; user corrects immediately and directly in Chinese."
---

When the agent goes in the wrong direction, junjie does not soften it. He states exactly what was wrong and what he actually wants, in Chinese, with exclamation marks. If the agent gets it wrong again, he escalates specificity with a concrete analogy or more explicit constraint.

**Pattern**: `[what agent got wrong] + [what it should actually be]！`

**Examples**:
1. Agent added a Chairman chat input: `"你不需要给我开一个可以和他们chat的东西！"`
2. Agent made it read-only but still wrong: `"我的消息只用传递给我的下层 那些高管 实验室的leader这种！"`
3. Agent still misses: escalates with analogy: `"就是和公司一样 一般下属可以直接和自己的上级和同事 还有下级交流！ 但是他不能和更高层的交流呀！"`

**Escalation pattern**: First correction is direct rejection. Second correction adds the concrete use case. Third adds a real-world analogy. He does not give up — he keeps correcting until the agent understands.

**Also uses for scope corrections**: `"下面我们来只写整体的doc 规划 spec driven development！ 不要再修改代码了！"` — stops agent from writing code when he only wanted planning.
