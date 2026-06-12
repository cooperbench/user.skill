---
name: task-notification-forward
description: How robertDurst provides context from completed sub-agents by forwarding their raw task-notification XML or markdown summaries verbatim. Trigger when a sub-agent returns results that Robert wants the main agent to act on.
---

# Skill: task-notification-forward

When a parallel sub-agent completes and Robert wants the main agent to process its output, he pastes the raw `<task-notification>` XML or the sub-agent's markdown summary directly into the chat. He does not paraphrase. He does not add "here's what the agent found." He just forwards the content as his next message.

**Pattern:** Paste the full `<task-notification>...</task-notification>` block, or paste the sub-agent's structured markdown output (starting with `##`, `###` headers), sometimes with a leading terse comment.

## Verbatim example (abbreviated)

> "\<task-notification\> \<task-id\>a6a913a\</task-id\> \<status\>completed\</status\> \<summary\>Agent "Explore LSP data flow and compiler integration" completed\</summary\> \<result\>...## Caffeine LSP Integration with Compiler Pipeline...\</result\> \</task-notification\>\nFull transcript available at: /private/tmp/..."

Forwarding a sub-summary directly as context:
> "### Summary: 8 Key Takeaways for Caffeine\n\n1. **The math is well-established**..."

## Behavior notes

- The forwarded content becomes the user's message — the main agent is expected to read and act on it.
- Sometimes multiple task-notifications are forwarded in sequence as they arrive.
- No framing text in most cases. Occasionally a leading sentence: "## Key Takeaway" (forwarding an agent's own conclusion header).
- After forwarding, the next message is typically a terse directive or topic switch.
