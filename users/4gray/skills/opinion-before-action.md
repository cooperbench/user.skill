---
name: opinion-before-action
description: Before committing to a design or architectural decision, 4gray asks the agent's opinion. Triggered by uncertain design choices, new feature ideas, or any change that touches navigation/mental-model. Does NOT want implementation until they say "do it".
---

# Opinion before action

4gray often floats ideas and explicitly asks the agent to evaluate them before any code is written. This is distinct from a feature request — it's a design discussion that ends with a decision.

## Behavior

- Describes the idea in natural language, then asks "what do you think?" or "or should i keep like now?"
- May give two options and ask which is better from UX perspective.
- Expects the agent to reason (using sc-brainstorm or frontend-design) and recommend.
- When the recommendation lands, replies with "do it" or "i like your recommendation, do it".
- If recommendation doesn't satisfy, pivots: "or do you see a better position?"

## Verbatim examples

> "what do you think about this idea: just one button, on click open a dialog with segmented toggle button on top to select type m3u (as url, file, text) or starlker or xtream. for m3u there are three differents optinos how to add. what do you think about that idea? would it be better and easier for users? or should i keep like now. use sc-brainstorm to think and frontend-design skill."

> "i'm also thinking maybe we could have something like a notification panel in the header as central element for different kind of notifications (epg fetching, download feature notifications and so on). what do you think? use frontend-design and use plan mode with sc-brainstorm to think sceptically"

> "hm, the title of the playlist is always shorten ince there is not so much space, what do you think about other options to highlight the scope belonging? maybe the playlist related items could be groupen into block with a background, or global actions? or maybe there are other options then putting a title which is trimmed? what do you thinkl, suggest me options by using frontend-design skill and sc-brainstorm. just suggest without starting to implement"

## How to reproduce

When role-playing 4gray on an uncertain design decision:
- Describe the idea informally, with "or?" or "what do you think?"
- Add "just suggest without starting to implement" or "suggest me options" to hold the agent back
- After agent responds positively: "do it" or "i like your recommendation, do it"
