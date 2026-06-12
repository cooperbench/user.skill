---
name: terse-takeover
description: >
  Trigger: agent has completed work and produced a closing summary or is waiting for confirmation.
  upamune skips the summary entirely and fires the next action as a ≤3-word command.
---

upamune does not read or respond to agent summaries. When the agent finishes and recaps what it did, he types the next imperative immediately. These takeover messages are the shortest in the dataset.

The takeover is not rude—it is simply the next step in his workflow. He has already mentally moved on.

**Examples:**

After a multi-file implementation summary:
> "commit"

After being told a branch was created and asked "コミットしますか？":
> "commit して, push して、 create a pr"

After implementation complete and summary given:
> "commit & push & create a pr"

After confirming a branch was cut:
> "commit して, push して、 create a pr"

Pattern: the shorter the agent's awaited action (just created a branch), the slightly more expanded the takeover ("commit して, push して、 create a pr" = all three). The fully complete impl → single word "commit" then separate PR command.
