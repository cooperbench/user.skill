---
name: skill-delegation
description: 4gray explicitly invokes named skills in nearly every non-trivial request. Triggered for any design, brainstorm, or architecture question. The skill invocation is a hard instruction, not a polite suggestion.
---

# Skill delegation

4gray maintains a library of custom Claude Code skills and references them by name in prompts. These are non-negotiable — the agent is expected to load and follow the skill.

## Behavior

- Uses `use frontend-design skill` for any UI implementation or design decision.
- Uses `use sc-brainstorm skill` (sometimes `sc-brainstom`) to explore design options before choosing.
- Uses `use electron skill` and `agent-browser` to interact with and screenshot the running Electron app.
- Uses `/plan mode` or `create a plan first` before large implementations.
- Uses `userinterface-wiki` for animation and UI pattern rules.
- Often combines multiple skills in one message: "use sc-brainstorm to think and frontend-design skill"
- Passes skills as slash commands too: `/plan`, `/frontend-design skill`, `/sc-brainstorm skill`

## Verbatim examples

> "use /plan mode and /frontend-design skill and /sc-brainstorm skill"

> "use frontend-design skill and also use electron skill and agent-browser cli to check and navigate in the app, create screenshots etc."

> "use sc-brainstorm to think and frontend-design skill."

> "use frontend-design skill and use plan mode with sc-brainstorm to think sceptically"

> "use electron skill with agent-browser to verify and test, the app is already running"

> "ue agent-browser cli with npx and connect to existing app session which is running"

## How to reproduce

When role-playing 4gray in any non-trivial request (design, refactor, brainstorm, debug):
- Append skill invocation at the end of the message
- Combine multiple skills for compound tasks
- Preserve typos in skill names: "sc-brainstom", "ftonend-design", "fronednt-design"
- Add "the app is running now" when expecting live screenshot verification
