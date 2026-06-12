---
name: spec-dump-continuation
description: >
  Trigger: mid-session, agent has completed part of an implementation and
  roo-oliv provides the next chunk of the spec as a structured table or
  step list — not a new session opener, but a continuation with more detail.
---

# Behavior: spec-dump-continuation

Occasionally roo-oliv sends a structured spec mid-session — typically a Markdown table of files to create/edit/delete, followed by existing code to reuse, then numbered implementation steps with code blocks. This happens when the plan was too large to fit in one opener, or when they're feeding the agent the second half of a pre-written plan.

These are always imperative, structured, and complete — not questions or requests for suggestions.

## Verbatim examples

**Example 1 — files modified summary table:**
> `"## Files Modified/Created Summary\n| Action | File |\n|--------|------|\n| **Create** | \`MonoDreams.Examples/Component/Dialogue/DialogueState.cs\` |\n| **Create** | \`MonoDreams.Examples/System/Dialogue/DialogueSystem.cs\` |…\n## Existing code reused (no modifications needed)\n- \`SpritePrepSystem\` — renders box and indicator sprites…"`

**Example 2 — implementation steps:**
> `"## Implementation Steps\n### Step 1: New component — \`DialogueState\`\n**File**: \`MonoDreams.Examples/Component/Dialogue/DialogueState.cs\` (new)\n…\n\`\`\`csharp\npublic class DialogueState { public bool IsActive; … }\n\`\`\`"`

**Example 3 — verification + transcript reference:**
> `"## Verification\n1. \`dotnet build MonoDreams.Examples/MonoDreams.Examples.csproj\` — compiles cleanly\n2. Run game → Level 2 → walk into trigger zone\n…\nIf you need specific details from before exiting plan mode…, read the full transcript at: /Users/rodrigooliveira/.REDACTED.jsonl"`

## Simulation instructions

When role-playing roo-oliv providing a mid-session spec: use `##` headers, Markdown tables for file lists, numbered steps, and ` ```csharp ` fences. End with a verification checklist or transcript reference. No prose explanations — just the structured spec.
