---
name: commit-pr-delegate
description: "Trigger: user decides a feature or bug fix batch is done. Delegates all git operations to agent with a 3–7 word command. Never runs git himself."
---

When satisfied with a batch of changes, this user triggers the entire git workflow (verify, diff, commit, push, PR) with a single terse command. He does not specify commit message format, PR title, or branch — the agent is expected to handle all of it (or he has the `pr-creation` skill loaded to govern that).

**Verbatim examples:**

> "ok commit and open pr"

> "Ok I think we are good. Please commit all changes and submit PR"

> "ok commit changes and update PR then"

> "Ok commit changes and submit PR"

> "Ok please do it yourself and call this new branch \"fix/project-paths\""

> "Ok commit all changes pls"

**Pattern**: `ok [commit] [and] [open/submit/update] [pr]` — always lowercase "ok", always imperative, no instructions about the commit message or branch unless deviating from the default.

If CI fails after the PR is opened, he pastes the CI error log (see `error-verbatim-paste.md`) and expects the agent to fix it without a new explicit instruction to commit again.
