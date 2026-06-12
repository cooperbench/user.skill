---
name: subagent-orchestration-boilerplate
description: >
  Trigger: user appends parallel-subagent instructions to a task prompt. Fires when the task
  involves code exploration or analysis that would benefit from parallelism.
---

When giving the agent a non-trivial exploration or debugging task, pc035860 appends a fixed
block of orchestration instructions at the end of the prompt. The block is nearly identical
across sessions and repos.

**Full verbatim block (most common form):**
```
- 使用 @agent-Explore (haiku, run in foreground) 來做廣泛的程式碼探索與資料蒐集\
- IMPORTANT: run subagents in parallel\
- First, use the TaskList tool to plan tasks in the user's best interest. Organize parallelization effectively for optimal results.
```

**Variant (with general-purpose agent added):**
```
- 使用 適合的subagent 或 @agent-general-purpose (run in foreground) 來做程式碼的分析\
- 使用 @agent-Explore (haiku, run in foreground) 來做廣泛的程式碼探索與資料蒐集\
- IMPORTANT: run subagents in parallel\
- First, use the TaskList tool to plan tasks in the user's best interest. Organize parallelization effectively for optimal results.
```

**When it appears:** After the main Chinese task description, separated by a blank line. The
preceding content is the actual task; the boilerplate is always at the very end.

**What it signals:** User wants the agent to use subagents in parallel, specifically Haiku for
broad exploration. Does not want the agent to do sequential single-threaded exploration.
