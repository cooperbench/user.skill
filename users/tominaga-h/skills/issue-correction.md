---
name: issue-correction
description: When the agent implements the wrong issue number, Hayato sends a brief apologetic Japanese correction with the correct issue number. Trigger when agent has started work on the wrong GitHub issue.
---

## Behavior

When Hayato realizes (or the agent reports) it implemented the wrong issue, he sends a short polite correction. It always starts with "すみません" (sorry/excuse me) and states the correct issue number. No further explanation.

This also applies when the agent misremembers the git state (e.g., claiming a tag doesn't exist when it does) — Hayato pastes the actual `git` command output to prove it.

## Verbatim examples

**Example 1** (wrong issue):
```
すみません、Issue #85 でした
```

**Example 2** (wrong git state — with proof):
```
1.3.0のタグは打たれてます
```
git tag | cat
v1.0.0
v1.0.1
v1.0.2
v1.1.0
v1.1.1
v1.1.2
v1.2.0
v1.2.1
v1.2.3
v1.3.0
```
```
