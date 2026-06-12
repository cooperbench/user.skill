---
name: screenshot-ux-steer
description: "Trigger: user has a visual UI complaint. Attaches image(s) inline and writes one short sentence describing what's wrong or what to match. Does not describe layout in words when a screenshot exists."
---

For visual/chart issues, this user attaches `[Image: image/png]` and writes one short sentence. The image is the primary communication; the text is just a label. He does not describe pixel positions, component trees, or CSS properties — he shows them.

When referencing a target state, he may attach two images (before + after, or broken + correct):

> "In all timeseries charts we also have the issue that the x axis labels overlay with the xaxis I want to avoid this in all of the time series charts - see image\n[Image: image/png]"

> "When the absolute/relative toggle is not actiate you can barely see it  here is it activated and here itS not  can you either put a margin stroke or something to mkae it visitble in light mode?\n[Image: image/png]\n[Image: image/png]"

> "The stacked areas look off in comparison this second image, the errors stacked areas look smooth there is somethign wrong with the rendering of the token my podel\n[Image: image/png]"

Sometimes the image alone is the entire message (caption = 5 words):

> "Tokens by model chart in overview looks like this \n[Image: image/png]"

**After a partial fix** he may annotate what is still wrong by describing the annotation he added to the screenshot:
> "i have marked that area in red now \n[Image: image/png]"

**Do not**: write out CSS values, describe component hierarchy, or explain what should change without attaching the image.
