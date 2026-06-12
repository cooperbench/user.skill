---
name: ci-failure-report
description: >
  Trigger: hirakiuc notices a CI failure externally (checks GitHub Actions themselves)
  and reports it to the agent. Also used when the agent enters an unexpected state.
---

hirakiuc does NOT paste CI logs, error output, or stack traces. Failure reports are
one-liners: state the failure type, tell the agent to handle it. Or, for unexpected agent
behavior, just ask "what happened?" These are the shortest prompts in the dataset.

**Examples (verbatim):**

> "CI status shows failure. please check and fix it."

> "what happened?"

> "What happened?"

Note the mixed capitalization of "what" — both forms occur. "what happened?" (lowercase)
appears to be the more spontaneous version; "What happened?" may occur at the start of a
new exchange. The agent is expected to investigate without further information.

This pattern reflects that hirakiuc monitors CI themselves and brings failures to the
agent, rather than asking the agent to monitor CI proactively.
