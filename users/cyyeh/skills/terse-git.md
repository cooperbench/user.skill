---
name: terse-git
description: How cyyeh issues git commands — ultra-short imperative phrases, often a single word or a chained action. Covers ~20% of all prompts. Trigger when the user wants to commit, push, branch, or raise a PR.
---

# Terse Git

Git operations are the most formulaic part of cyyeh's message style. They are short imperatives, often a single word, with no arguments or options specified — he trusts the agent to figure out branch names, commit messages, and remote targets.

**Common forms (in roughly ascending complexity):**

> `commit`

> `commit it`

> `commit this`

> `commit and push`

> `commit this and push`

> `commit all and push`

> `push it`

> `push to remote branch`

> `create a PR`

> `create new branch and push and raise pr`

> `create new branch and commit and push`

> `create new branch and commit all changes and push`

> `create new branch and commit and push and merge`

> `commit all and push and raise pr and merge`

> `remote branch also deleted`

**Takeover pattern:** When git operations don't go as expected or the agent hesitates, cyyeh takes over with a combined action command: "create new branch and commit and push and merge" or "commit all and push and raise pr and merge". He does not debug git failures — he just re-issues a more comprehensive command.

**Correction pattern:** If the agent is in the wrong branch: "you should not be in main branch, work in litellm-proxy worktree"

If the agent did something extra he didn't want: "only keep add multi_select guidance of all commits, and revert all other updates"
