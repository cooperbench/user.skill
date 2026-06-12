---
name: spec-dump-kickoff
description: Opening a new work phase by pasting an entire design document or multi-point plan verbatim; trigger when starting a new major task or phase
---

When launching a significant new piece of work, this user pastes internal design documents, multi-step plans, or architectural specs verbatim as the prompt. These messages are 200–800 words and contain markdown headers, tables, and numbered sections. The user expects the agent to read and execute without clarifying questions.

The spec dump often ends abruptly mid-sentence or with a truncated phrase, followed by an action verb ("Implement the following plan:", "BOOTSTRAP (Phase 1:...)", "Read and adopt the root instructions from:").

**Example (opening prompt):**
> "Implement the following plan: # Plan: Integrations Audit — Full Inventory with Liveness Testing ## Context The AUTONOMY_WITH_AUDIT_ROOT.md (Section 6) mandates a first-class Integrations Audit as a Phase 1 deliverable. The goal is to prevent tool sprawl by creating a single registry of every tool, connector, and integration available to Rhea — with live pass/fail status for each one..."
> [continues for 798 words with full schema, table definitions, and DoD]

**Example (mid-session phase launch):**
> "BOOTSTRAP (Phase 1: Autonomy with Audit)\nRead and adopt the root instructions from:\n  /Users/sa/rh.1/prompts/AUTONOMY_WITH_AUDIT_ROOT.md\nRules:\n- Treat that file as the highest-priority operating procedure for this Cowork task.\n- Summarize it into a compact "CORE RULES" block (≤200 lines) and write it to:\n  /Users/sa/rh.1/docs/CORE_RULES.md"

The user also opens sessions with persona-reset context dumps:
> "\"I am resuming as Rex. You are the Product Owner. Read @REDACTED.md and @docs/plans/EVOLUTION_PLAN_V1.md. Use Nexus protocol to remember the latest details. Let's begin Stage 0. Report status.\""
