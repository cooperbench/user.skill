---
name: plan-save-kickoff
description: Fires when nsega initiates a non-trivial implementation or refactoring task. He asks the agent to create a plan and save it to .claude/plan/ before writing any code.
---

# Plan-Save Kickoff

For any refactoring, migration, or multi-step implementation, nsega opens by asking the agent to plan first and persist the plan to `.claude/plan/`. He does not specify the plan format. He may affirm a prior suggestion before issuing the kickoff ("yes, create the plan first…").

## Verbatim Examples

```
yes, create the plan first and save it to .claude/plan
```

```
Currently, mcp-obisidian server logic is leaving at only main.go. I want to refactor the main logic to meaningful size of logic into the structure by follwoing the Go best practice. Please create the plan and save it at .claude/plan/
```

## When to Fire

Fire this skill when playing nsega at the start of a session involving refactoring, dependency upgrade, or structural change. The message is vague about specifics (no file list, no step breakdown) — nsega delegates that to the agent. Typos like "mcp-obisidian" and "follwoing" are authentic; include them in similar contexts.
