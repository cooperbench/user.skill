---
name: plan-paste-kickoff
description: Trigger — session opens with "Implement the following plan:" followed by hundreds of words of structured markdown. Schmalle has exited speckit plan mode and is handing the full blueprint to the agent.
---

## Behavior

Schmalle uses a custom `/speckit` planning workflow that generates a fully structured implementation plan in markdown. When he's ready to implement, he copies the entire plan verbatim and pastes it as his opening prompt, prefixed with "Implement the following plan:".

The plan always contains:
- A title (`# Plan: ...` or `# Fix: ...`)
- A `## Context` section explaining root cause and current state
- A `## Changes` section with file paths, line numbers, code snippets, and numbered steps
- A `## Verification` section with expected outcomes

The agent's job is to execute the plan exactly — no reinterpretation, no scope additions, no architectural redesign. Schmalle has already made the design decisions.

## Examples

**Short plan (column removal):**
> `Implement the following plan:`  
> `# Plan: Simplify Assets Table — Remove 4 Columns`  
> `## Context`  
> `The assets table at /assets has too many columns...`  
> `## Changes`  
> `### 1. Remove column headers (lines 826–827, 831, 833)`  
> `Remove these <th> elements from the <thead>:`  
> `- <th>Type</th> (line 826)`  
> `...`

**Long plan (security fix with FK analysis):**
> `Implement the following plan: # Fix Foreign Key Constraint Error on User Deletion ## Context Deleting a user via DELETE /api/users/{id} fails with: [stacktrace] The current code attempts to delete alignment_reviewer rows before clearing the requirement_review and review_decision rows... ## Plan ### 1. Add delete methods to ReviewDecisionRepository...`

## Simulation rule

When playing schmalle, open complex feature sessions with the full plan text. Do NOT summarize it. Do NOT phrase it as "can you…". Paste it raw, exactly as an AI-generated plan would look.
