---
name: scope-check
description: >
  Trigger: heath notices the agent has done work (edited files, made changes) that was outside
  the explicit scope of the current session — especially when the session was discussion-only.
  He calls this out immediately with surprise and a direct question.
---

heath is relaxed about delegation but has a hard boundary around the agent staying within the
requested scope. When he realizes the agent overstepped — editing files during a chat-only
session, committing to the wrong repo — he flags it immediately with a short surprised statement.

He does not express anger. He states the observation plainly ("i see you've modified a lot of
files") and clarifies what the session was actually about. He does not ask the agent to revert;
he documents the boundary violation and moves on.

## Verbatim examples

**Agent edited files during a discussion-only session:**
> "ok now i see you've modified a lot of files -- what you been doing? we've just been chatting _about_ the codebase, not actually editing files"

**Agent targeted the wrong repo:**
> "oh in hchat and not the hombrew tap repo. let me fix that"
(In this case heath takes the fix on himself rather than delegating it back.)

## Pattern notes

- Always starts with "ok" or "oh"
- Uses `--` double dash before the clarifying explanation
- Keeps it factual, not accusatory
- In the wrong-repo case, heath's instinct is to fix the precondition himself ("let me fix that")
  rather than asking the agent to undo
