---
name: git-ceremony-closer
description: petercr ends every logical unit of work with a commit → branch → PR sequence, issued as short imperative commands. Trigger at the end of a working feature, fix, or session.
---

Git operations are routine closers, not afterthoughts. petercr issues them as a chain of short commands, often in one message or in rapid succession. Branch names are feature-descriptive. PRs always go to main.

**Sequence:**
1. "make a new branch and commit changes to it" (or "commit changes to branch" if already on a feature branch)
2. "great let's make a pr from this branch to main"
3. Occasionally adds files to the PR after creation: "add seo.ts & meta.ts to this pr"

**Stash/switch patterns also appear:**
- "okay let's git stash the header changes, then switch to main and pull"
- "switch to branch feat-ui-updates-and-styles, pull in changes from main, then pop the stash"

**Examples:**

> "great looks good. let's make a new branch, and commit these changes"

> "great let's make a pr from this branch to main"

> "ok good enough for now. make a new branch, and commit changes to it"

> "ok commit changes to branch"

> "great let's commit all these changes to this ongoing pr"

> "add seo.ts & meta.ts to this pr"
