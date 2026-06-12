---
name: git-one-liner
description: Trigger when it's time to commit and/or push — dipree fires a terse fragment, not a full sentence. Use when any change has been made and git action is expected.
---

# Skill: git-one-liner

dipree issues git commands as minimal fragments. No explanation, no context, no request for confirmation. He treats commit/push as ambient housekeeping — fires it the moment a unit of work is done.

## Patterns

| Situation | What dipree types |
|-----------|-------------------|
| Just wants a commit | `commit` |
| Commit + push together | `commit and push` / `Commit+push` / `commit an push` |
| Agent just summarized work | `commit this` |
| Push after a prior commit | `push` / `push it` |
| With branch setup | `Create a branch, commit the changes` |
| With PR creation | `Create a draft PR with precise description of all the functionality and behavior.` |
| With docs update | `commit and push, document` |

## Verbatim examples

> "Commit+push"

> "commit an push"

> "commit this"

> "push it"

> "commit"

> "push"

> "commit and push"

> "Commit and push"

## Notes

- Capitalization is inconsistent — both "commit" and "Commit" appear; no signal in the casing
- No punctuation on one-word commands
- Will fire "commit this" as a takeover when agent is narrating instead of acting
- If there are lint/format steps implied by the workflow, sometimes chains: "Run lint and fix the issues, then push."
