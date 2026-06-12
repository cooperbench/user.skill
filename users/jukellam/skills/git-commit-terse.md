---
name: git-commit-terse
description: Trigger when jukellam wants to commit and push — he always uses the shortest possible phrasing, sometimes split into two messages.
---

# Skill: git-commit-terse

## Behavior

jukellam never dictates commit messages or explains what to include. He delegates commit message authoring entirely to the agent. His only instruction is one of:

- "commit and push" (most common)
- "commit and push those changes"
- "Commit and push this"
- "commit this" (then waits for result, then "push it")

When the agent fails to commit (e.g., because it tries to take over and do it itself wrongly), he responds with "push it" as a separate terse follow-up.

He occasionally adds a pre-condition before the git command:
- "First commit and push these changes to the repo. Also, I added Entire to this repo to track your context..."
- "Before you commit, update the Claude.md and Website Migration.md files to reflect what has been done."

## Verbatim examples

> "commit and push those changes"

> "Commit and push this"

> "commit this"

> "push it"

> "commit and push"

> "First commit and push these changes to the repo. Also, I added Entire to this repo to track your context and how you help me do this. Is there anything else I need to do to make sure your context is sent to my Github repo with each commit we make going forward?"

## Role-play note

Git instructions are always imperative and short. Do not add "please", "can you", or explanations. If asked to commit after a phase, the full message is two to five words.
