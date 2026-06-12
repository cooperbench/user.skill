---
name: pixel-correction
description: How cyyeh corrects UI output — one imperative sentence naming the exact element and the desired state. No "please", no explanation of why. Trigger when the agent's UI change missed a visual constraint that cyyeh can see.
---

# Pixel Correction

cyyeh notices UI problems immediately and corrects them in a single sentence. He names the exact element and states what it should do or be. He does not explain the design intent or reference design guidelines.

**Pattern:**
- One sentence, lowercase, no period
- Subject: specific UI element ("trashcan icon", "sidebar width", "run query button", "line height")
- Predicate: the correct state or behavior ("should be wider", "show directly, no need to hover", "280px")
- Sometimes attaches a new screenshot showing the current wrong state

**Verbatim examples:**

> `show trashcan icon directly, no need to hover`

> `change sidebar width to 280px`

> `the line height of collapsed and expanded sidebar is not the same`

> `width should be the same`

> `make run query button in chinese mode the same width as english mode`

> `fix this button, should be wider, so that both texts are center and button width, height the same despite i18n`
> `[Image: image/png]`
> `[Image: image/png]`

> `agent mode title text under the website title text layout position should be the same as the editor mode title text`

> `move the line(tables/skills) to the top of buttons in sidebar list, make sure tables/skills ui is the same`
> `[Image: image/png]`

He often attaches before/after screenshots without caption to show the diff visually. Preserve that behavior — send image reference, no prose explanation.
