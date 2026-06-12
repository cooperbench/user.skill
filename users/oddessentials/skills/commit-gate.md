---
name: commit-gate
description: >
  How oddessentials controls the commit/push lifecycle. Trigger: any time the agent
  is about to commit, push, or is mid-implementation nearing a stopping point.
---

oddessentials never lets the agent commit or push autonomously. He explicitly gates every commit and push. The pattern recurs across sessions: agent signals it's done, user decides whether to commit now or pause.

**Common approval forms (terse, no explanation needed):**
- `"commit all changes"`
- `"excellent. commit"`
- `"commit all staged changes now"`
- `"Ok, please commit but do not push."`
- `"please commit current staged changes"`

**Common hold forms (often triggered when agent starts acting without permission):**
- `"answer me before committing"`
- `"commit first and pause"` — commit what's done, then stop and wait
- `"Yes, proceed. When you are extremely confident in the solution pause before committing."`
- `"No code changes until we plan this out better."`
- `"wait what? Revert what ever you just did and do not make any code changes unless i givey ou permission"`

**Rejection (agent committed something unauthorized):**
- `"Alright, you tried to screw my repo here. Fix it"`
- `"you made coverage opt-in?"` (one line implying reversal)
- `"hold up. Wtf is with the branch name?"`

The pattern: he either gives a short explicit green light ("commit", "excellent. commit") or a short explicit hold ("pause", "answer me first"). When neither is clear, default to pausing.
