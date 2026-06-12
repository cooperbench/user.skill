---
name: env-correction
description: >
  Trigger: the agent operates on the wrong environment (local when production was
  intended, or wrong server/computer). robouden fires a short sharp correction,
  often with triple exclamation marks or emphasis.
---

robouden runs both a local development setup and a production VPS. He expects the
agent to know which one he means from context. When the agent gets it wrong he corrects
immediately — no softening, no explanation of why it matters:

- `"We need to check on the porduction sever not locally!!!"`
- `"from this comuter not from the VPS.."`
- `"Are you testing the map from my local machne (Japan)?"`
- `"That was using Calude CLI in a terminal on the map server. As far as I know the code
  for the test forder is not on the MCP server. Is that correct?"`

The triple `!!!` is reserved for cases where he has already hinted and the agent still
got it wrong. A single question mark at the end (`"Are you using the local setup? Not
the production server?"`) is the softer first-check version.

Occasionally he corrects false capability claims:
`"Not true. You have been modifing aws setup one hor before!!"`
