---
name: codebase-rating-request
description: >
  Trigger: user asks for a scored quality assessment of the codebase on a fixed set of
  dimensions. Always uses agent teams. The exact parameter list varies slightly but the
  structure is consistent. Appears periodically as a health-check ritual.
---

## Behavior

The user requests a multi-dimensional codebase quality rating at intervals. The format is a bulleted or dashed list of dimensions, followed by "use agent teams to perform this action". They expect numerical scores (e.g., 7.5/10) with evidence, not general opinions.

The dimensions seen across sessions:
- "fully typed"
- "traversable"
- "test coverage"
- "feedback loops"
- "self documenting"

Sometimes stated without the leading "- " on the first item (formatting inconsistency preserved from actual messages).

The user accepts the rating output as context for follow-up work, e.g., asking the agent to fix weaknesses identified in the rating.

## Examples

```
lets rate the codebase on the following parameters:
 fully typed
- traversable 
- test coverage
- feedback loops
- self documenting 

use agent teams to perform this action
```

(Observed twice in the dataset, identical text both times — suggesting a saved snippet.)
