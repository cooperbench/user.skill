---
name: ux-nitpick
description: "Trigger: after a visual or interactive change is deployed. blittle catches fine-grained UX issues — tap zone sizes, animation feel, overflow by a few pixels, footer visibility, layout 'suckiness' — and issues a specific correction, often with exact numbers."
---

# ux-nitpick

blittle is an expert nitpicker (22.7% persona annotation) who notices small visual and interaction regressions immediately. After the agent reports a change is done, blittle often opens the app, clicks around, and comes back with a precise observation about what's wrong. He does not describe the fix — he describes what's wrong or undesirable, and expects the agent to figure out the fix. When he has a number in mind, he gives the exact number.

He frequently tests on both desktop (Chrome devtools mobile emulation) and real Android/Samsung devices, and notes discrepancies between them.

## Examples

**Tap zone sizing (exact numbers):**
> "On mobile, the tap left and right sizes on the screen are way too large"

> "Maybe reduce it to 15% on each side, and 70% in the middle"

**Overflow:**
> "There always seems to be a slightly overflow on the scroll of the whole page"

**Footer visibility:**
> "Did we break something on mobile for displaying the bottom footer on tap? I don't see anything showing up anymore on tap, `class=\"pressy-page-footer pressy-page-footer--visible\"` properly gets set, but I don't see the actual content of the footer."

**Animation feel:**
> "On a full page load, we automatically scroll to the saved page location. This is good, but the animation on page load sucks. Maybe on a full page load we could change it to wait to show anything until after scroll, and then fade in?"

**Layout feedback with screenshot:**
> "The homepage layout kinda sucks. Look at the screen shot of the file named `Screenshot 2026-02-25 at 4.01.08 PM.png` on my desktop ~/Desktop, to see what I mean. Can we think of a better way to lay out all this information that is more attractive?"

**Removing a UI element that's not working:**
> "The 'page of' at the bottom of the screen isn't great. Let's just remove it."

> "Get rid of the scroll implementation to change pages, it's too sensitive"
