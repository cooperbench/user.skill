---
name: pre-push-deep-review
description: >
  Trigger: Armel is about to commit or push a batch of changes. He asks for a
  deep review of the last N commits before allowing the push to proceed.
---

A standard ritual before shipping. Armel always requests a "deep review" of recent commits
to catch missing impacts, bugs, regressions, or broken links before they hit the remote.
The request is brief and formulaic. He sometimes escalates to "ultra deep review" for larger
batches.

After the review, he either:
- Fixes identified issues selectively ("fix all N" or names specific ones)
- Commits immediately ("commit", "perfect. please commit")
- Asks follow-up questions about specific findings

## Examples

**Standard pre-push:**
> "Deep review the changes from the last 7 commits for any breaking changes, or missing impact and ect..."

**Before a manual push:**
> "before I manually push everything, run a last ultra deep review of the last 4 recents commits to detect any missing impacts, bug, improvements, etc..."

**After agent delivers review:**
> "fix all 15"

**Or selective:**
> "review the changes for any breaking changes, or missing impact."

**Terse pre-commit:**
> "Before we open a PR. Run a deep review to make sure we did forget missing impact, etc..."
