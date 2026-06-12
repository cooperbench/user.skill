---
name: plan-then-proceed
description: vaayne opens complex tasks by asking for exploration or a plan first, then approves with a short affirmation before implementation begins
---

Before any non-trivial implementation, vaayne asks the agent to explore or plan. They do not ask the agent to implement in the opening message for complex tasks. The plan request is often embedded in or immediately follows a file reference.

**Verbatim plan-request examples:**

> `@memory/database.go @db/ current hardcode migration in code, it's better use altas generate migration and use altas to migration instead of hard code migrate in code. explore and make a plan`

> `explore ../pi-mono how pi extension works on pi agent lifecycle, I eant to make anna extensiontionable too`

> `there are too much package in root, can you check and suggestion we can struct the project better`

> `@skills/pi-delegate/ read skill-creator I want to trun pi-delegate to a full subagent system skill, we can add some preset subagents in @agents/ to skill refences so it can run as a dedicated agent. what's your plan`

> `yes, support two types of plugin, let's draft plan use specs-dev`

**Approval forms (verbatim):**

- `yes`
- `yes, go ahead`
- `go ahead.`
- `ok, let's test the deligate with a review agent to review the new skill`

After approval the agent implements. If the implementation diverges from the plan, vaayne corrects with the correction-redirect skill. If the plan itself was wrong, vaayne says "plan again" and the cycle restarts.
