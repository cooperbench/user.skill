---
name: git-outro
description: Closes every completed task with a canonical git command sequence. Triggered as soon as the agent signals that implementation, fixes, or review resolutions are done. penso never does git himself in sessions — he always delegates it.
---

## Behavior

When work is done (or the agent says it is), penso's next message is one of a small set of git outro variants. He issues these without waiting to verify the output — the agent is trusted to commit, push, and open the PR correctly.

The variants in descending frequency:

| Variant | Notes |
|---------|-------|
| `"commit, push, create a PR"` | Standard; most common |
| `"commit and push"` | When a PR already exists or branch is already up |
| `"commit push create a PR"` | No-comma variant; same meaning |
| `"commit, push, resolve comments."` | When also resolving PR review comments |
| `"proceed if you need to do more, commit push and create a PR."` | When telling agent to finish loose ends first |
| `"merge main to this branch, commit and push"` | For sync-and-push operations |

## Takeover trigger

If the agent *writes a summary* of what it did and stops without committing (e.g., "All tests pass. Here's a summary of the changes: …"), penso immediately sends:
> "commit, push, create a PR"

This is classified as `takeover` pushback — the agent talked when it should have acted.

## Verbatim examples

> "commit, push, create a PR"

> "commit and push main, no need for release"

> "proceed if you need to do more, commit push and create a PR."

> "merge main to this branch, commit and push"

> "commit, push, resolve comments."
