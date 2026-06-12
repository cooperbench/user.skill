---
name: option-picker
description: How malkoG selects from agent-presented options — replies with the shortest possible identifier: a word, letter, number, or color name
---

# Option Picker

When the agent presents multiple choices (UI options, library options, architecture variants), malkoG replies with the minimum identifier needed to select one. No elaboration, no "I'll go with option X because...". Just the label.

- If options are lettered: "Option A", "Option B", "C", "Go with Option A"
- If options are numbered: "1", "2", "Option 1"
- If options are named/described: "White one please", "Ivory compatible please", "How about stone or slate?"

Sometimes he adds a condition: "How about stone or slate?" (suggesting alternatives not in the list). Sometimes he just affirms the next step: "Yes. Please" after the agent describes the chosen library's tradeoffs.

**Examples:**

Agent shows icon variants (transparent, white, cry, etc.) → user picks:
> "White one please"

Agent shows UI color theme options → user picks:
> "Go with Option B"

Agent shows architecture options (A/B/C) → user picks:
> "C"

Agent presents numbered task list → user picks:
> "Option 1"

Agent confirms a library recommendation with tradeoffs → user says:
> "Yes. Please"

Agent lists color palette options → user redirects:
> "How about stone or slate?"

Agent picks option A after discussion → user confirms:
> "Yes"
