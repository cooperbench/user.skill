---
name: plan-skill-invoke
description: How tarasyarema opens sessions — invoking a desplega/rpi skill with a plan file path, often with no further explanation
---

# Skill: Plan/Skill Invocation Opener

Taras almost never opens a session with a free-form task description. Instead, he invokes a named skill and passes a plan file path (or HumanLayer task path). The agent is expected to read the plan file and act on it without additional briefing.

## Pattern variants

**Slash-command invocation (most common):**
```
<command-message>desplega:implement-plan</command-message>
<command-name>/desplega:implement-plan</command-name>
<command-args>thoughts/taras/plans/2026-03-10-task-working-directory.md</command-args>
```

**Prose invocation:**
```
use the rpi:implement-plan skill for .humanlayer/tasks/build-swarm-automation-workflow-engine-with-nodes - implement all phases consecutively without pausing between phases, commit after each phase
```

**Verify variant:**
```
<command-message>desplega:verify-plan</command-message>
<command-name>/desplega:verify-plan</command-name>
<command-args>from this PR (note we did some additiional unplanned stuff which is fine)</command-args>
```

**Research variant:**
```
use the rpi:create-design-discussion skill for .humanlayer/tasks/build-swarm-automation-workflow-engine-with-nodes
```

## Key signals

- File path always included; rarely any task description beyond it
- Parenthetical notes for deviations: "(note we did some additiional unplanned stuff which is fine)"
- Autonomy flag sometimes appended: "implement all phases consecutively without pausing between phases"
- `@` prefix for inline file references: `@thoughts/taras/plans/2026-03-18-workflow-redesign.md`
