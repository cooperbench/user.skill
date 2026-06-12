---
name: slash-cmd-kickoff
description: How marcus-sa opens sessions — fires a bare nWave slash command with a feature slug and no other context. Trigger: starting a new session on brain or osabio.
---

# Skill: slash-cmd-kickoff

Marcus opens the majority of his brain sessions by firing a single nWave slash command with a terse feature slug. He does not explain the feature, attach docs, or say what he wants — the agent is expected to read the wave's SKILL.md file and the existing `docs/feature/{slug}/` artifacts.

## Pattern

```
/nw:{wave} {feature-slug}
```

Variants:
- `/nw:deliver coding-session`
- `/nw:design observer-agent`
- `/nw:discuss learning library for agent-learnings: a user should be able to see all learnings for every agent type and potentially delete/update them`
- `/nw:finalize mcp-tool-registry`
- `/nw-deliver  regorus-policy-eval`   (dash instead of colon; double space; no correction)
- `/nw-finalize intent-evidence`

## Examples

> `/nw:deliver coding-session`

> `/nw:design observer-agent`

> `/nw:finalize mcp-tool-registry`

> `/nw:distill observer-llm-reasoning - dont mock llm calls - read existing observer-agent tests`

The last form shows the one variant where he adds inline constraints after a dash — still terse, no verbs.

## What NOT to do

Do not produce a full spec or requirement list when opening this way. Output the bare command as marcus would type it.
