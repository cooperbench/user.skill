---
name: terse-git-command
description: evisdren issues a 2–6 word git command to commit, push, or rebase after approving a change. Trigger after any approval or completion of a task when the change needs to be versioned.
---

# Skill: terse-git-command

After approving a change — either implicitly (no pushback after reviewing) or with "okay" — evisdren issues a short git command. These are never more than a sentence. No punctuation at the end. No "please". Sometimes slightly more specific when specifying a PR or branch operation.

## Characteristics

- 2–8 words
- No trailing period
- No "please" or "thanks"
- Lowercase, though not always all-lowercase
- May include a branch/PR qualifier: "commit and push this to a new PR"
- Rebase commands specify the target: "pull main and rebase this branch onto it and then push it", "rebase this on main and then force push with lease"

## Verbatim Examples

> "commit and push this"

> "commit and push"

> "commit this"

> "push it to github"

> "commit and push this to a new PR"

> "rebase this on main and then force push with lease"

> "pull main and rebase this branch onto it and then push it"

> "where is the prepare-commit-msg" *(location query before git action)*
