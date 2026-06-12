---
name: skill-invocation
description: khaong routinely delegates structured workflows to named skills and slash commands, either by sending the full skill markdown as a message or using the slash command syntax. They treat skills as first-class workflow primitives.
---

# Skill Invocation

khaong uses Claude Code plugins and custom skills extensively. When a structured workflow is needed, khaong either:

1. Sends the slash command directly: `/superpowers:brainstorm`, `/review 158`, `/debug-e2e <url>`
2. Pastes the full skill markdown as a user message with the prefix "Base directory for this skill: ..."
3. Types an explicit instruction: "Invoke the superpowers:brainstorming skill and follow it exactly as presented to you"

This is not a workaround — it's khaong's standard operating mode. Skills define HOW the agent should behave for the session.

## Common skills invoked

- `superpowers:brainstorm` — structured brainstorming for feature design
- `superpowers:execute-plan` — plan execution with checkpoint review
- `superpowers:systematic-debugging` — root-cause-first debug protocol
- `superpowers:write-plan` / `superpowers:writing-plans` — plan document generation
- `receiving-code-review` — structured PR feedback processing
- `github-pr-review` / `entire-internal:github-pr-review` — PR thread interaction
- `debug-e2e` — E2E artifact triage

## Examples

Slash command:
> `<command-message>superpowers:brainstorm</command-message>`
> `<command-name>/superpowers:brainstorm</command-name>`

Explicit invocation with arguments:
> `Invoke the superpowers:executing-plans skill and follow it exactly as presented to you`
>
> `ARGUMENTS: keep each commit with working code please (no micro-committing broken state)`

Directing the agent to invoke a skill for one last review pass:
> `can you invoke your requesting-code-review skill for one last pass?`

After completing a subagent review:
> `let's go with #4 and #5 please, though can we stick to the workflow of subagent dev and review?`
