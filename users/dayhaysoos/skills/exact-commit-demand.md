---
name: exact-commit-demand
description: How dayhaysoos corrects the agent when it describes a git action instead of providing a copy-paste command. Triggers when agent explains what to run but doesn't give the exact command, or when agent does part of the git workflow but not all of it.
---

dayhaysoos wants a ready-to-paste terminal command, not a description of what to do. When the agent narrates git steps ("you should add and commit the file"), he corrects with a demand for the literal command. He also extends this rule permanently: "Do that every time."

He applies the same pattern to incomplete git workflows: if the agent commits but doesn't push, or pushes but doesn't make a PR, he calls it out immediately with a one-liner correction.

**Example 1** (after agent described git steps):
> "Give me the exact add/commit command for this. Do that every time."

**Example 2** (after agent pushed without PR):
> "you pushed but didn't make the PR. Put all that info in the PR"

**Example 3** (after agent did neither):
> "I want you to commit everything we have unstaged right now. Push to the branch and make a PR summarizing what we did here in this branch"

When role-playing this user, if the prior agent response involved git work without a copy-paste command, the user's next message will be short, lowercase-starting if terse, and imperative. The correction is a directive, not a question.
