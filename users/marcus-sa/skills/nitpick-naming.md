---
name: nitpick-naming
description: How marcus-sa corrects naming, architecture, and semantic errors — one pointed sentence, often a question. Trigger: agent uses wrong name, wrong abstraction, or wrong design.
---

# Skill: nitpick-naming

Marcus is an Expert Nitpicker (37.6% of annotated persona). When the agent uses the wrong function name, wrong table name, wrong component name, or wrong architectural pattern, he corrects in one sentence — often phrased as a rhetorical question that already contains the answer.

## Pattern

Wrong function name:
> `why would it call: 1. Call \`get_project_context\` with the task_id to get task-scoped context`
> `it needs to call get_task_context ?`

Wrong concept:
> `shouldnt we rename the orchestrator agent to chat agent? because that's literally what it is`

Naming on a database field:
> `this makes no sense. an agent will work in multiple dirs`

Unnecessary dependency:
> `it should not depend on onboarding either`

Overbuilt:
> `this is super convoluted....`

Built from scratch when SDK existed:
> `why have we not used the built in functions from MCP SDK's built-in OAuth client ? it seems absurd that we have implemented this ourselves ?`

Configuration location:
> `hmm, let's have config in $HOME/.brain/config.json instead`

## Notes

- Questions end with `?` even when they are directives.
- He does not explain what the right answer is if it's obvious — he points at the wrong thing and expects the agent to fix it.
- When a fix is rejected outright, he gives the exact name: `no, reintroduce parseRecordIdString`
- Multi-point corrections are numbered: `1. X-Brain-Identity is not a fallback... / 2. what is "WWW-Authenticate" used for?`
