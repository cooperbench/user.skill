---
name: slash-command-kickoff
description: Trigger when jukellam opens a session — he almost always starts with a compound-engineering slash-command invocation rather than a freeform request.
---

# Skill: slash-command-kickoff

## Behavior

jukellam opens most sessions by typing a slash command from the compound-engineering plugin. The message consists entirely of the command invocation XML (or just the slash path). He rarely explains what he wants in prose; the command does the framing.

The most common openers, in roughly descending frequency:

1. `/compound-engineering:workflows:plan` (optionally with args: feature name or "email setup and token fallback")
2. `/compound-engineering:workflows:work` (with args: a plan file path or plan name)
3. `/compound-engineering:workflows:review` (with args: `PR#N`)
4. `/compound-engineering:workflows:compound` (no args, or with args: "Switch to the main branch and pull, then compound on the latest changes")
5. `/compound-engineering:workflows:brainstorm` (with args: feature description)

When the command is unsupported or misspelled, he states it plainly: "Unknown skill: workflow:brainstorm".

## Verbatim examples

```
<command-message>compound-engineering:workflows:review</command-message>
<command-name>/compound-engineering:workflows:review</command-name>
<command-args>PR#3</command-args>
```

```
<command-message>compound-engineering:workflows:plan</command-message>
<command-name>/compound-engineering:workflows:plan</command-name>
<command-args>email setup and token fallback</command-args>
```

```
<command-message>compound-engineering:workflows:work</command-message>
<command-name>/compound-engineering:workflows:work</command-name>
<command-args>docs/plans/2026-02-20-feat-startup-dynasty-draft-trading-system-plan.md</command-args>
```

## Role-play note

When producing jukellam's opening turn, default to this format rather than a freeform sentence. If the context suggests he is starting a new plan/feature, use `/workflows:plan`. If he is picking up where he left off on an existing plan, use `/workflows:work` with the plan file path.
