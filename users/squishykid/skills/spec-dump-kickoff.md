---
name: spec-dump-kickoff
description: How squishykid opens a session when implementing a pre-planned feature — pastes a complete markdown plan with file paths, code snippets, and section headers. Trigger when starting a non-trivial implementation task at the top of a session.
---

For large implementations, squishykid arrives with a fully written plan and pastes it verbatim as the opening prompt. The plan is structured markdown with sections (Context, Changes, file paths with line numbers, Go code blocks). The opener is always "Implement the following plan:" followed by the plan body.

After the plan is submitted, squishykid immediately reverts to terse mode for the rest of the session. The plan is a one-time data transfer, not an ongoing conversation.

**Example opener (truncated):**
> `Implement the following plan: # Fix: Empty repo "reference not found" error (#242) ## Context In a freshly git init'd repo with no commits, repo.Head() returns plumbing.ErrReferenceNotFound. [...] ## Changes ### 1. Add ErrEmptyRepository sentinel error **File:** cmd/entire/cli/strategy/strategy.go (after line 27) [...]`

**Example opener (hook managers feature):**
> `Implement the following plan: # Detect External Hook Managers and Warn Users ## Context PR #355 fixed hook installation [...] ## New Files ### cmd/entire/cli/strategy/hook_managers.go **Data model:** [...] **Detection function:** [...]`

Plans always include:
- A GitHub issue reference in the title
- Exact file paths with line numbers
- Go code to add verbatim
- A table or list for detection logic
