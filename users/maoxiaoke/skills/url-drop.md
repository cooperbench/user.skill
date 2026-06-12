---
name: url-drop
description: >
  Trigger: agent's previous response missed linking something, used the wrong URL, or the user
  wants to point at a specific resource (font, product page, spec). User drops the URL as the
  entire message with zero commentary.
---

# URL Drop

When the agent missed a link, used the wrong URL, or needs a resource reference, maoxiaoke
sends the URL as the complete message. No "here's the link", no "use this instead", no context.

**Characteristics:**
- Entire message is a single URL
- No greeting, no label, no punctuation after URL
- Can be a Google Fonts URL, a product page, a Twitter/X link, or any web resource

**Examples verbatim:**
> "https://anotherme.lemonsqueezy.com/"  ← (sent twice when agent missed the href)
> "https://fonts.google.com/specimen/Gaegu?preview.script=Latn"  ← (as part of feedback, also dropped standalone)

**When to use as maoxiaoke:**
- Agent said "More on Lemon Squeezy" but didn't link it → drop the URL
- Agent used a wrong font URL → drop the correct font URL
- Agent needs to fetch a resource to complete a task → drop the URL

**Context from sessions:**
The agent responded "改为 `More on Lemon Squeezy.`" without making it a hyperlink. User dropped
`https://anotherme.lemonsqueezy.com/` twice consecutively before the agent finally added the link.
