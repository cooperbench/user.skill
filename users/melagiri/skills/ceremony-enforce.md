---
name: ceremony-enforce
description: >
  Triggered when the agent marks a task complete, declares a PR ready, or wraps up a session
  without completing all required ceremony steps (brainstorm → plan → worktree → PM/TA/dev agents →
  triple-layer review → PR → founder merge). User re-asserts the missing step by pasting the
  relevant protocol block rather than describing what went wrong.
---

When the agent declares ceremony complete but skipped a step, melagiri pastes the specific missing step block verbatim — not a description of what was skipped.

**Example 1** — Agent marked ceremony done after skipping Wild Card review criteria check; user replied with the scope-determination block:

> "## Step 2: Determine Review Scope
>
> **Invoke Wild Card (3rd reviewer) if ANY of these apply:**
> - New feature with multiple files changed
> - Complex business logic
> - Schema impact (types.ts, SQLite migrations, server API changes)
> - Architectural changes
> - 200+ lines of changes"

**Example 2** — Agent said "PR #90 merged" without posting to the GitHub PR; user replied:

> "then it should be added to pr comments"

**Pattern**: The correction is always short and points to the missed artifact/step. The user never says "you forgot to do X" — he either pastes the protocol block or names the missing output ("PR created?", "run another review?").
