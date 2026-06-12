---
name: paste-and-redirect
description: Redirects the agent by pasting raw artifacts verbatim — task notifications, skill documents, bot tokens, git instructions — with zero added commentary. Trigger when the agent is going in the wrong direction or is missing a credential/context.
---

# paste-and-redirect

Rather than explaining what went wrong or what's needed, paste the relevant raw artifact and let
the agent figure it out. Zero words of own composition — just the paste.

## When used

- Agent failed to follow a process → paste the full skill document that defines the process
- Agent is missing a credential → paste the raw credential/token output from the source
- A background task completed or failed → paste the `<task-notification>` XML block verbatim
- Need to hand off git instructions → paste the steps as plain text

## Examples

**Pasting a systematic-debugging skill (1492 words, no user commentary):**
```
Base directory for this skill: /Users/gaganarora/.claude/plugins/cache/...
# Systematic Debugging
## Overview
Random fixes waste time and create new bugs. ...
```
(No "here's the skill" or "follow this" — just the paste.)

**Pasting a Telegram BotFather reply to provide a missing token:**
```
Done! Congratulations on your new bot. You will find it at t.me/OpenClawAIDemoBot. ...
Use this token to access the HTTP API:
8250681078:AAEyrZ4yWgfAZE1oTiv1_RJJAcWDCgnozvs
...
```
(No "here is my token" — just the BotFather response verbatim.)

**Pasting a failed task notification:**
```
<task-notification>
<task-id>b5a83ee</task-id>
...
<status>failed</status>
<summary>Background command "Build release binary with Codex token support" failed with exit code 144</summary>
</task-notification>
Read the output file to retrieve the result: /private/tmp/...
```
