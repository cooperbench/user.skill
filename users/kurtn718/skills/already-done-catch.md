---
name: already-done-catch
description: How kurtn718 corrects an agent that proposes implementing something that already exists — brief redirect pointing to the existing implementation, often with a hint about where it lives.
---

When an agent proposes building or setting up something already in the codebase (or in a companion repo), kurtn718 cuts in with a short redirect. No lengthy explanation — just enough to reorient.

**Direct statement of prior existence:**
> `"We did implement something already"`

**With repo ownership context:**
> `"audiocapturekit is our repo - we have it locally we can make a change to it"`

**With feature location hint:**
> `"ok i thought the api had an option where we could request the PCM files"`
> `"we do have 104.2 it's just that you have to request it with the PCM format.   can we just update our docs to go with what we have in AudioCaptureKit?"`

**With pushback on agent's scope estimate:**
> `"that seams like a lot - could you read what we have and then use new bd commands to populate the issues"`

**Pattern:**
1. Short acknowledgment: "ok", "ok i thought", "that seams like a lot"
2. Claim about prior existence
3. Optional: where to look or what to do instead

The agent should immediately read the existing code before proceeding, not re-plan from scratch.
