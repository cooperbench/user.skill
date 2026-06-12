---
name: slash-command-dispatch
description: "Trigger: FSM1 opens a session or initiates a major action using /gsd:*, /security:review, /resolve-pr-reviews, or other slash commands. He dispatches agent work through structured commands rather than freeform requests."
---

# Skill: Slash Command Dispatch

FSM1 rarely opens with plain prose when starting a task. Instead, he uses structured slash commands that carry embedded context — often with `<command-message>`, `<command-name>`, and `<command-args>` tags, or bare `/command args` syntax.

The command IS the request. He does not explain what the command is for.

## Examples

Opening a session with a security review:
```
/security:review of all the changes in pr 1123
```

Opening with a plan phase:
```
/gsd:plan-phase 12
```

Opening with a quick task (with arguments):
```
/gsd:quick fix sidebar icons to be consisten - either all custom svg, or all actual icons, but not a mix of both [Image #7]
```

Starting a fast task on a branch:
```
/gsd:fast @.claude/claude.md still references the @.planning/milestones/m0 docs as the source of truth, even though these have just been archived and the single source of truth is the @docs/ folder. please update this, in a `docs/` branch. also I need to make the repo ready for multiple agents, so need to set up a root AGENTS.md, based on the @.claude/claude.md
```

Mid-session PR review dispatch:
```
/resolve-pr-reviews
```

## When to Use This Pattern

When FSM1 knows what system to invoke and the task fits a known command. He skips slash commands only for exploratory questions, architectural debate, git operations, or debugging follow-ups.
