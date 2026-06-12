---
name: log-dump-debug
description: Pastes raw log output verbatim, preceded by one framing sentence, and expects the agent to diagnose the issue. Trigger when reporting a timeout, crash, or unexpected silence from the running extension.
---

# Log Dump Debug

When savekirk hits a timeout or crash, the sequence is:
1. Report the symptom in one sentence: "keeps timing out", "Checkpoint just loads forever showing progress bar and then debug vscode closes"
2. Ask the agent to add debug logging: "Add debug statements to debug command calls and timeouts"
3. Collect the output, then paste the full raw log — potentially hundreds of lines — with a minimal frame:

> "Log outputs below. Go through to understand the issues"

or:

> "Log outputs in @logs.txt"  *(referencing a file the agent can read)*

The log is never summarized or trimmed. `[runCommandAsync]` spawn/exit lines are pasted wholesale. The user does not interpret the logs first; that is the agent's job.

**Verbatim example frame**:

> "Log outputs below. Go through to understand the issues [runCommandAsync] exit: git show entire/checkpoints/v1:c8/e352d0cd59/0/context.md, code=0, 6ms, stdout=121B, stderr=0B [runCommandAsync] spawn: git show entire/checkpoints/v1:c8/e352d0cd59/0/prompt.txt..."
