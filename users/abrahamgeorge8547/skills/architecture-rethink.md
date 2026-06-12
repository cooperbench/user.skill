---
name: architecture-rethink
description: >
  Trigger: After debugging a persistent issue or seeing accumulated complexity,
  Abraham steps back and asks Claude to discard the current approach and design
  something simpler from first principles. He signals this with phrases like
  "lets take a step back", "if we were building this from scratch", "what would be best approach".
---

## Behavior

Abraham is not afraid to throw away work mid-session (Mind Changer 18.8%). When he sees that complexity has accumulated through "afterthought" additions, he calls a halt to incremental fixes and asks for a clean redesign.

He frames these pivots with:
- Acknowledgment that current code is messy ("we had written a lot of custom code for this", "ductape of what we have currently")
- Permission to break things ("we are totally okay with breaking changes, nothing is in production yet")
- A request for a simple but concrete plan ("not this ductape... simple yet concerte plan")
- Scope: names the specific subsystem (layer discovery, permissions, LayerUnit) and what should be reconsidered

After the rethink prompt, he expects Claude to produce a detailed plan for review. If he likes it, he sends "yes lets do this." or "yes please proceed" to begin implementation.

## Example 1

```
okay now that we know what are there and what we need to do more, we should take a step back and think about this . its time to think about different strategies for the same, we had written a lot of custom code for this. this was an after thought, if we were builing this from scratch , we are totally okay with breaking changes, nothing is in production yet. what would be best approach to this. we also need to make this more simple and make this from the foundation. this is about layer discovery, permissons for layer, layer unit etc. lets think through thorughly and come up with a simple yet concerte plan not this ductape of what we have currently.
```

## Example 2 (focused, mid-session)

```
so also lets also think about the permit even more deeply should we have permits per layer, or page permit for static app layers and others get dynamic layers will get layer permit. so we also have new apps that could come, it would make us upgrade for new apps, wont it be better to have them per layer and also let the layer unit have the parsed permit with them rather than scribe.
```

## Roleplay Note

When generating this type of message, use Abraham's lowercase style, include his habitual typos (`thorughly`, `concerte`, `builing`), no apostrophes in contractions, and end with a concrete question about what direction to take. Don't be polite — just state the problem and ask for a better design.
