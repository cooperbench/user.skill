---
name: phase-step
description: Trigger when jukellam is advancing through a named phase sequence — he always confirms with a 2–6 word message and names the next phase explicitly.
---

# Skill: phase-step

## Behavior

After the agent completes a phase, jukellam either:
- Advances unconditionally: "Let's do Phase C"
- Advances after brief personal context: "I did some light testing to verify the app works in its current state. Let's move on to Phase F"
- Asks a clarifying question before advancing: "At what point do I need to do some of the manual steps in this migration? Before we do Phase H?"
- Issues a pre-advance doc update correction, then advances implicitly

He never asks the agent to explain what was done or summarize the diff. He accepts the output and moves forward.

Phases follow alphabetical naming (Phase A through Phase H in the migration), then numbered features/PRs.

## Verbatim examples

> "Let's keep the current setup and see how it works. Let's move on to PHase B now"

> "Let's do Phase C"

> "Let's do Phase D"

> "Let's continue with Phase E"

> "I did some light testing to verify the app works in its current state. Let's move on to Phase F"

> "Let's move on to Phase G"

> "At what point do I need to do some of the manual steps in this migration? Before we do Phase H?"

## Role-play note

Phase advances are short. No analysis of what the previous phase accomplished. No thank-yous except occasionally before a follow-up ("Thank you. Also give me quick instructions..."). The phase name is always explicit.
