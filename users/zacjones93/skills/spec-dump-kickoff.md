---
name: spec-dump-kickoff
description: Zac opens a complex task by pasting a large document (500–2400 words) — a CrossFit rulebook, investigation report, implementation plan, or ADR body — followed by a short instruction to build or update something.
---

About 1 in 6 sessions begins with a multi-paragraph paste. Zac provides the full context
document first, then a brief imperative. The agent is expected to read the entire document and
act on it without asking follow-up questions.

**Trigger**: Opening message >200 words that contains domain documentation, a formatted report
with headers, or a full implementation plan, followed by ≤15 words of instruction.

## Examples

**Investigation report → fix:**
> "please use an agent team and investigate this issue: # Leaderboard Missing Athletes
> Investigation Report ... [753-word report] ..."

**CrossFit rules → build ADR:**
> "I'm going to give you a report on how CrossFit handles penalties which is the defacto way
> competitions do it... build out an adr for this (004) # CrossFit Games penalty framework: a
> complete system analysis ... [2261-word report] ..."

**Implementation plan → implement:**
> "Implement the following plan: # Plan: Top-level \"Review\" nav item + index page for video
> submissions ... [468-word plan with specific files, code snippets, and UI spec] ..."

**Code review output → verify and fix:**
> "Verify each finding against the current code and only fix it if needed.
> In `@apps/wodsmith-start/src/db/schemas/competitions.ts` around lines 169 - 173,
> The unique constraint on (eventId, userId, divisionId) prevents re-registration..."

## Behavior notes

- Zac frequently dumps documents that are already structured as agent instructions (plans, ADRs, PR descriptions)
- When he says "build out an adr for this (004)", the number is the ADR sequence number
- The document is the spec; the final sentence is the task. Read both.
- He will follow up mid-ADR-session with incremental corrections ("first off, we are using planetscale mysql so get rid of all instances of D1")
