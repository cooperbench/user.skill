---
name: plan-attach-kickoff
description: How KeKs0r opens a session when he has a pre-written plan — attaches plan.md and
  sends minimal or zero text. Trigger when starting a new task with an attached file and sparse
  prose.
---

# Plan-attach kickoff

KeKs0r frequently delegates work by attaching a `plan.md` (or Linear ticket) and sending
either nothing else, or a single short instruction. The plan IS the spec — he expects the agent
to read it and execute without further clarification.

## Pattern

The session-opening message consists of:
1. A Conductor system instruction block (workspace path, branch name)
2. A system instruction block listing the attached files
3. Zero or one line of user text — often just the phase to execute

The user text is either absent or extremely terse:
- *(empty — just the system instructions with the attachment)*
- `implement phase 1 & 2`
- `Fully copy the single session view from \`/Users/marc/Workspace/flick/...\` into rudel. its the best version we have so far`

## Examples

```
<system_instruction>...Baghdad workspace...</system_instruction>
<system_instruction>
The user has attached these files. Read them before proceeding.
- /Users/marc/conductor/workspaces/rudel/baghdad/.context/attachments/plan.md
</system_instruction>
```
*(no user text — the attachment is the entire instruction)*

```
implement phase 1 & 2
```
*(after attaching a plan.md in Lagos workspace)*

## What to infer

- Read every attached file before doing anything else.
- Execute the plan; do not ask for clarification unless something is genuinely ambiguous and
  unrecoverable.
- Do not summarize the plan back to the user — just start working.
