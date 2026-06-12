---
name: feedback-redirect
description: >
  Trigger: agent has finished a task or is idle and there is new code review feedback to
  address. hirakiuc never describes the feedback inline — always redirects to the file.
---

When there is external feedback to act on, hirakiuc writes a short two-sentence message:
one to announce feedback exists, one to point the agent at the file. The file path is
always given as a Gemini CLI `@`-reference. The word "please" appears in every instance.
Message length: 10–15 words.

**Examples (verbatim):**

> "got some feedback on the current code base. please check the @.agent/feedback.md file."

> "got some feedback. please check the @.agent/feedback.md file."

The shorter variant ("got some feedback.") appears when the context is already clear.
hirakiuc does not summarize what the feedback says, does not assign priority, and does
not give implementation instructions — all of that is in the file.
