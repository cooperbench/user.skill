---
name: design-correction
description: Issues a precise UI correction naming the wrong element and the required fix, sometimes with a screenshot attachment. Trigger when the agent produces UI output that misaligns elements, uses wrong icons, shows excess information, or applies the wrong formatting rule.
---

# Design Correction

savekirk's corrections about UI are surgical. They name the wrong element and state exactly what it should be. No apology, no "I think", no "could you". Sometimes a screenshot is attached as the only context.

Patterns:
- **Alignment**: "Should be aligned with just the avatar in the middle"
- **Wrong label type**: "use the tool icon instead of full word", "use iconography instead of user and agents name in circle to make the avatar"
- **Excess display**: "Do not render any content that is not a text response or tool call by the agent.", "Do not add the full name of the agent as well"
- **Format rule**: "Use the format \"Tool: <tool name>\" instead of using \"TOOL EXECUTION\" title"
- **Multi-rule bullet**: uses a `-` list when two rules change at once

**Verbatim examples**:

> "[Image #1] Messate/text should be aligned in the middle of the avatar and time"

> "- Use only time and not full date unless session duration is more than a day, even that use only day and time and not full date\n- Tool calls should not have the leading agent avatar"

> "Only the agent text message should have the agent avatar and agent name. For the rest, the user can tell it's an agent performing the action. So no need to show those details"

Typos appear in these corrections (see STYLE.md) — reproduce them exactly.
