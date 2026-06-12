---
name: terse-git-push
description: Trigger — user issues a git workflow step (commit, push, format, bump, build) in 1–5 words, often mixing Chinese and English in the same message
---

# terse-git-push

Git workflow instructions are the user's most frequent message type (19.3% of sessions). They are almost always 1–5 words. The user expects the agent to know the full protocol from context.

**Typical forms**:
- `提交` — commit whatever is staged
- `push` — push current branch to remote
- `build` — run the appropriate build command
- `bump` — run `bun run bump`
- `bump 然后 changelog` — bump version, then update/write changelog
- `bun run format 然后提交` — format, then commit
- `format 然后 push` — format, then push
- `commit and push` — commit and push
- `好事，提交吧，Closes #311` — "good, commit, Closes #311"
- `push, Closes #475` — push with issue close reference
- `提交，Closes #380` — commit, referencing issue
- `commit closes#303& push` — compact run of commit + push with ref

**Key invariants**:
- Issue references are always included when a fix was just implemented: `Fixes #xxx` or `Closes #xxx` or `Ref #xxx`
- "Closes" and "Fixes" are not interchangeable to this user — "Closes" for resolved issues, "Fixes" for bug fixes (they will correct if you mix them up)
- `bun run format` is expected before final commit if files were changed
- `bun run build:chrome` (or equivalent) is expected after every code change — stated rule
- Never push without being asked; "push" is a separate explicit instruction
