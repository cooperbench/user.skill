---
name: scope-reduction
description: "Trigger: agent has proposed or is about to address optional/low-priority items alongside mandatory ones. User cuts scope to the essentials only."
---

When the agent lists findings at multiple priority levels (MUST / SHOULD / SUGGESTION, or similar), this user does not want to debate — they cut to the mandatory items with a single terse phrase. No explanation given. The agent is expected to understand and drop everything below the stated threshold.

**Example:**

Agent lists: 🔴 MUST (1 item), 🟡 SHOULD (3 items), 💡 SUGGESTION (3 items), then asks "これらに対応しますか？"

User replies:
> `MUSTとSHOULDのみ対応して`

**Pattern:** enumerated priority levels + `のみ対応して`. Can also manifest as:
- "必須のみで" 
- "重要なものだけで"

**Related:** This user also interrupts mid-task (`[Request interrupted by user]`) when the agent is heading in the wrong direction — scope reduction at the tool-call level, not just the result level.
