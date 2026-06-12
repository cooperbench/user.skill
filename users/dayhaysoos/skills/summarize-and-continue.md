---
name: summarize-and-continue
description: How dayhaysoos handles long agent task-tool output mid-session — a fixed phrase that tells the agent to compress the previous output and keep going. Triggers when a background task finishes and the output is too long to act on directly.
---

When the agent's sub-task output is long (tool results, task summaries, deployment logs), dayhaysoos uses a fixed steering phrase to move past it without reading it himself. This phrase appears repeatedly across sessions and is a known steering pattern for OpenCode's task-tool results.

**Exact phrase** (used verbatim, every time):
> "Summarize the task tool output above and continue with your task."

No variation. No additional context. If this phrase appears in a conversation, produce a brief summary of the prior tool output and continue the current task.

Also used to validate end-of-phase:
> "it looks like the reviewer found no high confidence bug. Now I want you to run the commands you would need to confirm that this body of work for this phase is done. Report your results. If you have unexpected errors, fix them."

And to nudge completion:
> "Okay, so I want you to finish ALL of the other slices. Remember to keep reviewing, writing tests and not moving on to the next slice until the last one is complete."
