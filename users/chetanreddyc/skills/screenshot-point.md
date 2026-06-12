---
name: screenshot-point
description: Attaches a screenshot and pairs it with a terse imperative command — triggered for any UI bug, visual layout issue, or UI state the user wants to show rather than describe.
---

Sends `[Image #N]` inline in the message, followed by a short command: "see this fix it", "fix that", "why is this showing". Rarely describes what's wrong in words when a screenshot can say it. The screenshot is the primary evidence; the text is the action verb.

For layout bugs specifically, will send multiple screenshots across follow-up messages if the first fix didn't work visually.

**Example 1** (layout bug):
> "hey see this screenshot [Image #4] fix that extra spacing in that page at top in desktop!!"

**Example 2** (repeated fix attempt):
> "hey it still has a lot of space see [Image #5]"

**Example 3** (UI state showing an error):
> "[Image #1] hey see this after i clicked on magic link that opend page is closing quickly without showing anything and after when i swith to checkout page it says email verified but still that identity verification is present in there and when i click on secure payment to proceed it still say's that verification is required still and i cant proceed investigate this behaviour deeper and fix this!"

**Example 4** (pointing to what they want to create):
> "[Image #5] see this is what im donna do create!"
