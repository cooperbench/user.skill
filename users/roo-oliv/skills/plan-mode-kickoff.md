---
name: plan-mode-kickoff
description: >
  Trigger: opening a new session or starting a new implementation task.
  roo-oliv writes a complete plan in Claude Code's plan mode, then exits and
  immediately fires the agent with the full spec as an opening prompt.
---

# Behavior: plan-mode-kickoff

Every session opener is `"Implement the following plan:"` followed by a structured Markdown document that includes:
- A `# Title` describing the fix or feature
- `## Context` — what was working before, what broke, why it matters
- `## Root Cause` or `## Root Cause Analysis` — detailed technical diagnosis (often includes file paths, line numbers, execution order reasoning)
- `## Implementation Plan` or `## Fix` — step-by-step changes with exact file paths, before/after code snippets in ` ```csharp ` fences, and explicit line numbers
- `## Verification` — numbered checklist of how to confirm the fix works

The user does NOT ask the agent to plan or explore — the plan is complete. The agent's job is pure execution.

Plans frequently end with a footer like:
> `If you need specific details from before exiting plan mode (like exact code snippets, error messages, or content you generated), read the full transcript at: /Users/rodrigooliveira/.REDACTED.jsonl`

## Verbatim examples

**Example 1 (collision fix):**
> `"Implement the following plan: # Fix: contactTime >= 0 check breaks collision resolution ## Context The previous round of changes (CollisionRect, SequentialSystem, \`contactTime >= 0f\`) fixed the snapping bug but broke collision resolution entirely."`

**Example 2 (CSS fix):**
> `"Implement the following plan:\n\n# Fix: Gutter line numbers wrap per-digit when > 1 digit\n\n## Context\nLine numbers in the diff gutter (e.g. \"171\") wrap character-by-character — each digit appears on its own line. The gutter is 28px wide…"`

**Example 3 (dialogue system):**
> `"Implement the following plan: # Dialogue System: Collision Trigger + UI (Level 2) ## Context The previous dialogue implementation used a monolithic \`DialogueUIStateComponent\` on a single entity…"`

## Simulation instructions

When role-playing roo-oliv opening a session: produce a well-structured plan in this format. Do not produce a vague request or ask the agent to figure out the approach. The plan must name specific files, line numbers, and include code snippets where relevant.
