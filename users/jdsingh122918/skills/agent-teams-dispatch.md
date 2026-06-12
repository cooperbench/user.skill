---
name: agent-teams-dispatch
description: >
  Trigger: user directs any multi-file investigation, fix, or implementation using the
  phrase "use agent teams" or "using agent teams". Applied broadly — investigation, fixing,
  rating, UI design, gap bridging. Never explains the parallelism; assumes the agent knows.
---

## Behavior

The user appends "use agent teams to perform this action", "using agent teams", or "fix all X using agent teams" to their request. This is their standing instruction for any task that spans multiple files, modules, or concerns. They don't explain the topology — the agent is expected to decompose and dispatch.

Characteristic patterns:
- Appended to investigation requests: "use agent teams to investigate in detail"
- Appended to fix requests: "fix all X gaps using agent teams"
- Appended to rating requests: "use agent teams to perform this action"
- Appended to implementation: "Lets implement all the recommendations using subagents"
- Used for UI exploration: "Use frontend design tool to brainstorm and playground html tool to mock up various options. Use agent teams"

The user also references specific agent types by name: "use agent-browser", "use context7 mcp", "lets use subagents".

## Examples

```
using agent teams, investigate in detail the backend and frontend. Then determine whether there any gaps/functionality that requires bridging between the two
```

```
lets rate the codebase on the following parameters:
 fully typed
- traversable 
- test coverage
- feedback loops
- self documenting 

use agent teams to perform this action
```

```
fix all 10 gaps using agent teams
```

```
Lets implement all the recommendations using subagents
```

```
use the following database URL --> libsql://forge-fermatsolutions.aws-us-east-2.turso.io
and the following turso token --> REDACTED
```
