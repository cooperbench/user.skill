---
name: git-fire-and-forget
description: When the user wants to commit and/or push, they send a 3–5 word lowercase command and move on — no branch name, no commit message, no options.
---

# Git fire-and-forget

The user treats git as punctuation. After a test cycle or fix, they issue a terse push command and expect the agent to handle all the details (commit message, branch, remote target).

**Trigger**: Work is done (tests pass, bugs are fixed, or the user decides the current state is good enough to push).

**Pattern**: 3–5 words, lowercase, imperative, no branch or remote specified.

**Examples**:
- `commit and push remote`
- `push this code to remote`
- `push to remote`
- `push this then`

Note: "push this then" is a correction/redirection — the agent was doing something else and the user wants to stop that and just push.

**What the user does NOT provide**: commit message, branch name, `--force` flag, any confirmation step. They expect the agent to commit all changes with a reasonable message and push to origin.
