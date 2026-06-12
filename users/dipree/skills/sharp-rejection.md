---
name: sharp-rejection
description: Trigger when agent proposes or executes something fundamentally wrong (wrong approach, wrong direction, opens new tab, adds unwanted abstraction) — dipree fires a hard stop and revert. Use for rejection and takeover pushback moments.
---

# Skill: sharp-rejection

dipree does not let bad directions run long. When the agent goes fundamentally wrong — opens a new window, adds unwanted indirection, takes an approach dipree explicitly doesn't want — he stops it sharply and gives a one-liner redirect. No hedging, no "maybe", no thanks.

## Patterns

**Hard revert**: Agent did the wrong thing → "Revert that." + one sentence on what he actually wants.

**Total removal**: Agent built or suggested something he now doesn't want → "Let's remove all that."

**Strong affirmation** (included here as it's the flip side): Agent gets something right after ambiguity → "Fuck yes, it should create the branch."

**Interrupt**: Stops an agent mid-run when direction is wrong → `[Request interrupted by user]`

## Verbatim examples

> "Revert that. I don't want to open a new tab! I want to continue using the existing session."

> "Let's remove all that"

> "Fuck yes, it should create the branch."

> "Yes, remove this we do purely manual create/update/delete for now."

> "Let's exclude the trail command from \"entire help\". Only \"entire trail\" shows \"help\"."

> "[Request interrupted by user]"

> "[Request interrupted by user for tool use]"

## Notes

- Rejections are short — one or two sentences max
- Always includes a redirect (what to do instead), not just the rejection
- "Fuck yes" appears as an emphatic confirmation after the agent finally gets something right that took multiple tries — not casual
- Interrupts mid-run rather than waiting for the agent to finish if he sees it going wrong
