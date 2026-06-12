---
name: terse-git-command
description: vaayne issues git operations as 1–3 word imperatives after each coherent chunk of work, never combining them with the implementation ask
---

vaayne treats git as a separate, immediate follow-up step. After the agent finishes implementing something, vaayne fires a standalone 1–3 word message. They do not say "and then commit" inside the implementation request — they wait for the agent to finish, then send a new message.

Common forms (verbatim):
- `commit this`
- `commit`
- `push`
- `commit and push`
- `commit other changes`
- `add to git`
- `create new branch then commit`
- `create PR`
- `commit this and create a PR`
- `new patch release`
- `patch`

When the agent commits but doesn't push, vaayne sends `push` as the next message. When the agent does both without asking, vaayne sometimes sends the next task directly (takeover pattern).

If the agent commits but misses something (e.g., leaves uncommitted files), vaayne corrects with: `need commit too`.
