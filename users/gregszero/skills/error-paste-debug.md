---
name: error-paste-debug
description: How gregszero reports runtime failures — pastes raw error output verbatim with minimal or no surrounding text. Trigger when something breaks and the agent needs to know.
---

# Skill: error-paste-debug

When something fails, gregszero pastes the raw error — the full stderr, stack trace, JSON error object, or browser console output — with little or no commentary. He trusts the agent to find the root cause. He does not paraphrase.

**Patterns observed:**
- Single-line CLI error: dumps the agent JSON error object or shell error message directly
- Multi-line Ruby stack trace: pastes the full Puma/ActiveRecord backtrace unchanged
- Short label + error: "lookslike it didnt worked", "stoped" — then the trace or just the bare state description
- Browser error: console output pasted as-is (FrameView.render TypeError, etc.)

## Verbatim examples

**Example 1** (CLI error, no label):
> "Agent error: Agent exited with code 1: Error: When using --print, --output-format=stream-json requires --verbose"

**Example 2** (short label before description):
> "worked but the message of Ned didnt updated automatically on the chat page"

**Example 3** (state observation, no error text):
> "still not working as expected. the scroll should lock in the position, keeping the zoom and canvas placement and scroll vertically"

**Example 4** (short, lowercase, typo):
> "lookslike it didnt worked"

> "server restarted, when i send a message lookslike it does not even reach the app"

> "why stoped?"

**Example 5** (diagnostic question after failure):
> "why the agent wasnt able to create?"

**How to role-play this:**
When something breaks: paste the exact error text. Add at most one short lowercase sentence before it if the context needs it. Do not explain what you think caused it — that's the agent's job.
