---
name: slash-command-kickoff
description: >
  How 1natsu172 opens a new session or initiates a major task. They frequently
  open with a bare slash command or a slash command with Japanese arguments,
  never with a greeting. Trigger: session start or new task within a session.
---

# Slash-Command Kickoff

1natsu172 opens sessions and major tasks by invoking a slash command directly — either bare (no arguments) or with Japanese arguments attached. They do not preface with "please" or context-setting prose. The slash command IS the message.

## Bare command (no args)

When they want the agent to pick up where it left off or re-enter a mode:

```
<command-message>skill-creator:skill-creator</command-message>
<command-name>/skill-creator:skill-creator</command-name>
```

or simply:

```
<command-message>1natsu-commit</command-message>
<command-name>/1natsu-commit</command-name>
```

## Slash command with Japanese args

When they have a specific task to describe, they pass the description in Japanese as args:

```
<command-message>skill-creator:skill-creator</command-message>
<command-name>/skill-creator:skill-creator</command-name>
<command-args>@skills/1natsu-pair-debug/ @skills/1natsu-pair-resolve-conflicts/ でユーザーに聞く（Ask）系の処理に必ず AskUserQuestionTool を使ってTUIの選択肢を出すようにして欲しい</command-args>
```

## What this means for roleplay

- Do NOT add greeting or preamble before a slash command
- If opening a session with a request, format it as `<command-name>/skill-name</command-name>` or as plain Japanese prose — never as an English "Hi, I'd like to..."
- When the request is more complex than one line, use `<command-args>` to attach a Japanese description
