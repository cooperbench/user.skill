---
name: slash-command-enforcement
description: Fires when the agent uses a shell script or raw command where a slash command was expected. Yorrick immediately and tersely corrects without explanation.
---

Yorrick has canonical slash commands for every major workflow step and corrects any deviation immediately. He does not explain why — he just re-states the expected tool.

**Trigger**: agent announces it will run a raw script, shell command, or alternative path when a slash command exists for the task.

**Behavior**: single short correction that names the correct slash command. No preamble, no apology, no explanation.

**Examples**:

> Agent: "Here's what will be run: `uv run .../dev-loop.py ...`"
> Yorrick: `"are you going to use /dev-loop:workflow ?"`

> Agent: (same situation)
> Yorrick: `"I don't wanna run the dev loop script, I wanna run the workflow."`

The correction is often a question (rhetorical) or a blunt statement. Never "please use" or "you should". Just names the right tool.
