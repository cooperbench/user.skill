---
name: vague-opener-then-steer
description: petercr opens sessions with a high-level goal (issue number, screen name, broad feature) and lets Claude form the plan, then corrects specifics mid-session. Trigger when starting a new session or new major task.
---

petercr rarely specifies implementation details in the opening message. They name what they want to accomplish and may reference a design tool or issue tracker, then wait for Claude to propose an approach. Follow-up corrections are terse.

**Pattern:**
- Open: broad directive + optional tool hint or issue ref
- Let Claude plan/implement
- Correct specifics in one clause if off
- Approve with "great" or "yes" then move to next item

**Examples:**

Opening:
> "today we're going to work on issue #27 in this repo. let's make a plan to do it"

Opening with design reference:
> "today we're going to work on adjusting the max height on our header cards and our content cards on desktop views. use the penpot mcp server to view the Desktop page. you can view the frame Intro to see the max widths of the header and cards. then we will apply those max width styles to the landing page first."

Mid-session after approval:
> "ok great now on the landing route page we need to add more top & bottom margin to the headers and cards. they're too close together now"
