---
name: plan-dump-kickoff
description: How thomasdavis opens large implementation tasks — dumps a fully-structured markdown plan (often 500–4000 words) prefaced with "Implement the following plan:". Trigger when starting a new feature or major change.
---

# plan-dump-kickoff

thomasdavis uses a planning step (Claude Code plan mode) before implementation, then pastes the approved plan directly as his opening prompt. The prompt starts with a literal "Implement the following plan:" header and contains a full markdown spec: titled sections, numbered steps, file tables, code block examples, and Prisma schema snippets.

He does not ask "can you do this?" or "what do you think?". He presents the plan as a work order.

The plan almost always includes:
- `## Context` section explaining why this feature exists
- Ordered implementation steps with file paths and exact changes
- `## Files` table listing action (Create/Edit) and path
- `## Verification` section with manual test steps or commands

He expects the agent to follow the plan exactly, in order, without deviating or asking for clarification.

## Examples

**Short-form plan dump opening:**
> "Implement the following plan: # Add \"Sandbox Logs\" Tab to Agent Detail Page ## Context Agents with sandbox enabled execute shell commands... ## Design Add a \"sandbox logs\" tab to the agent detail page (`/dashboard/agents/[id]?tab=sandbox-logs`)..."

**Verbatim implementation order block (mid-session, after plan mode):**
> "## Implementation Order | Step | What | Files | |------|------|-------| | 1 | blocks.yml entries | `packages/tools/official/blocks.yml` | | 2 | Package structure | `package.json`, `tsconfig.json`..."
