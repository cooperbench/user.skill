---
name: git-ship-loop
description: How KeKs0r closes a completed task — always ends with commit + push + PR + merge
  on green CI. Trigger when a feature or fix is done and he's ready to land it.
---

# Git ship loop

KeKs0r closes almost every task the same way. He sends a short closing command that bundles
all git operations into one shot and expects the agent to handle them in sequence.

## Standard closing phrases (verbatim)

> `commit, push and create a PR, merge when passed`

> `commit and push all changes`

> `Commit and push all changes`

> `commit the files that you changed in this session. dont do any git status and ignore all other uncommited files.`

> `and then commit all changes on here, push, create a PR and wait until verifyication is done and then merge`

> `git push, create PR and merge it when CI passes`

> `Resolve any existing merge conflicts with the remote branch (main). Then, commit and push your changes.`

## PR creation additions

When creating PRs he sometimes attaches a "PR instructions.md" file:

> `<system_instruction>The user has attached these files: PR instructions.md</system_instruction>\n\nCreate a PR`

He expects the agent to follow the PR creation skill (conventional commit title format:
`feat:`, `fix:`, etc.) and run `bun verify` before pushing.

## Retrigger

After a CI failure he may simply ask:

> `retrigger CI`

Or ask for the fix and relaunch in one step:

> `commit, push and create a PR, merge when passed`

## Characteristics

- Never stages manually — expects agent to know which files changed.
- "ignore all other uncommited files" — he has multiple workspaces and doesn't want
  unrelated dirty state committed.
- Merge is conditional on CI green, always — he does not merge manually on failure.
