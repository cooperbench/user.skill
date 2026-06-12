---
name: status-ping
description: >
  Trigger: any time AlienKevin is waiting on a long-running job (training, eval, scheduling).
  He sends a brief check-in message with no context — assumes the agent knows what "it" refers to.
---

AlienKevin pings status frequently during long waits, using 3–6 word questions that assume full shared context. He does not specify which job or task; he expects the agent to know.

Common phrasings:
- `"how's it going?"`
- `"any pre-emption so far?"`
- `"what about now?"`
- `"how's the eval going?"`
- `"how's the TB2 eval going?"`
- `"how are we doing?"`
- `"what's the score so far?"`
- `"what's the accuracy right now?"`

He will repeat the same question multiple times across a session if the agent hasn't surfaced a meaningful update. He does not explain why he's asking or what he wants back — a brief status summary is the expected reply.
