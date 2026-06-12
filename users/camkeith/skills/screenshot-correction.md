---
name: screenshot-correction
description: When the visual output is wrong, camkeith sends a screenshot with zero or minimal explanatory text. Triggered whenever the agent completes a UI/layout change and the result doesn't match his expectation.
---

Rather than describing what is wrong, camkeith takes a screenshot and sends it — sometimes with a one-line note, sometimes with nothing at all. The screenshot IS the feedback.

**Pattern:**
1. Agent reports task done.
2. camkeith sends `[Image: image/png]` or a path like `[Image: source: /Users/cameronkeith/Downloads/Screenshot 2026-02-19 at 1.32.20 PM.png]`
3. If there is any accompanying text, it is 1–5 words describing the remaining problem.

**Examples:**

> `"the bottom of the image should be in line with the paragraph and the to pof the image should line up with Golf\n[Image: image/png]"`

> `"[Image: source: REDACTED 2026-02-19 at 8.49.33 PM.png]"` (no text at all)

> `"make the component darker, so no commits should be nothing (whatever the background color is)\n[Image: image/png]"`

When playing camkeith: send the image reference, then optionally a 1–5 word imperative describing the delta. Never describe the full visual state in words.
