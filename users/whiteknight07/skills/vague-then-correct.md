---
name: vague-then-correct
description: User opens with a broad high-level directive, lets agent plan or start, then fires a sharp correction when the agent goes in the wrong direction. Annotated as "Vague Requester" in 50% of sessions.
---

Whiteknight07 rarely specifies requirements upfront. He delegates the "figure it out" work to the agent, then corrects the direction with a short sharp message when he sees the result going wrong.

The opening prompt is often intentionally open-ended:
- "redo the front page" (no design spec, no constraints)
- "document everything" (no format, no audience, no scope)
- "use explore subagents... do what is needed, basically ask me questions as needed"

The correction is **immediate and decisive** — not negotiated.

**Verbatim examples**:

Opening (vague):
> "I need you to completely rethingk and redo the front page for this app. I need you to Compltely boldly redesign it, you ahve all the freedom in the world to show off your skill use the frontend design skill"

Correction after agent delivered the redesign:
> "now parallel w opus subgagents the same way redo the entire UI"

Opening (vague, documentation):
> "I need you to have proper documentation for this project. Use explore subagents. The subagents should be Opus 4.6 and spawn them across the codebase and have documentation where necessary and needed. Also update the README file. Do what is needed, basically ask me questions as needed."

Correction after agent asked targeted questions:
> "lets have api-reference.md and connit and push"

Opening (vague, deployment):
> "could you pull test on this branch"

Correction after agent gave a detailed analysis with options:
> "reabse"

When the correction is the opposite of what the agent suggested (e.g., agent proposed merge, user wants rebase), he just says the action — no explanation.
