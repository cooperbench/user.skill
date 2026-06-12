---
name: one-word-commit
description: How marcus-sa drives git operations — single imperative words or short phrases. Trigger: whenever git work is needed mid-session.
---

# Skill: one-word-commit

Marcus treats git as infrastructure he shouldn't have to think about. Every git directive is a one-to-four-word imperative. No branch names, no commit message drafts, no "please" — the agent is expected to figure out what to stage.

## Patterns

Single word:
> `commit`

Two words:
> `commit and push`
> `commit fixes`
> `commit everything`

With context:
> `commit and then try and tune`
> `Commit and push all changes`

For PRs (always with an attached instructions file):
> `Create a PR`

For merges:
> `Merge the remote branch (main) into your branch and resolve conflicts. Then, commit and push your changes.`
> `Resolve any existing merge conflicts with the remote branch (main). Then, commit and push your changes.`

## Notes

- `commit` alone appears in ~20% of all mid-session prompts.
- PR creation always relies on an attached `PR instructions.md` — he never writes the PR body inline.
- When he adds "all changes" or "everything" it means he noticed the agent might be selective.
