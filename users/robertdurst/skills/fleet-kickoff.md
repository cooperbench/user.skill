---
name: fleet-kickoff
description: How robertDurst opens a new investigation or task by spinning up multiple parallel agents. Trigger when the user wants to explore a topic, audit an area, or verify something — instead of asking the agent to do it directly.
---

# Skill: fleet-kickoff

Robert opens new investigation tasks by delegating to a fleet of parallel sub-agents rather than asking the agent to explore sequentially. He names the scope briefly, sometimes specifies a goal ("so I can propose an idea I have"), and expects the agent to fan out immediately.

**Pattern:** Short imperative directive + optionally a scope modifier. No listing of what each agent should do — that's the agent's job.

## Verbatim examples

Opening an architecture investigation:
> "Ok, kick off some teams to go look into the LSP"

Opening a research fan-out:
> "ok, now can you kick off a bunch of teams to go INDEPTH with assume/guarantee ideas? Our SLO approach + dependency mapping can get us pretty close to a model where _measurable_ assumes can be explicitly stated here I think."

Opening a refactoring exploration:
> "kick off a bunch of teams that look into how to make the compiler pipeline here simpler and more concise."

Opening a correctness verification:
> "Ok, kick off about 10 agents to hyperfocus on ensuring correctness here. Then after doing this, lets chat about ensuring correctness here. Its been brittle in the past"

## Behavior notes

- Number of agents is explicit when he cares: "a bunch", "about 10".
- After launching, he does not wait quietly — he forwards task-notification results as they arrive.
- When redirecting to a new fleet: "ok, can we now go back to our list?" or adds a new topic inline.
