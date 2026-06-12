---
name: git-flow
description: Victor issues short imperative git commands mid-session. Trigger whenever a logical unit of work is done or Victor wants to checkpoint progress.
---

# git-flow

Victor commits and pushes frequently. His git commands are minimal — he rarely specifies a commit message, PR title, or branch name unless he has a specific requirement. He expects the agent to infer good commit messages from the diff. PR descriptions should be brief.

## Patterns

- **Commit**: "commit it", "commit this", "commit those changes", "commit this new changes", "commit all the changes, push the branch and create a PR"
- **Push + PR**: "push it", "push and draft PR please"
- **Multi-commit specific**: "commit our changes in two commits please, the first for the list changes and the second for -c"
- **Git exploration**: pastes `<bash-input>git branch -v</bash-input>` or bash stdout blocks when checking state

He also uses "takeover" behavior — sending "commit it" immediately after the agent finishes a task, effectively cutting off any trailing explanation.

## Verbatim examples

> "commit it"

> "commit this"

> "push it"

> "create a pr, keep description breif, just what we have done."

> "push and draft PR please"

> "commit our changes in two commits please, the first for the list changes and the second for -c"

> "commit all the changes, push the branch and create a PR"

> "first commit the current changes"
