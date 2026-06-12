---
name: spec-dump-kickoff
description: >
  Trigger: user opens a session with a pre-written implementation spec, plan, or task
  document. The message starts with "You are implementing a project per the following spec."
  or "Execute the plan at" or "Implement the following plan:". Expects the agent to execute
  without clarification. May include component tables, code patterns, and dependency chains.
---

## Behavior

The user arrives with a complete implementation spec generated externally (from a `docs/superpowers/specs/` file or `docs/plans/` file). They paste the entire spec as the opening message and expect full execution — no questions, no design discussion.

The spec typically contains:
- A **Goal** section
- A **Components** table (name, description, complexity, dependencies)
- **Code Patterns** section with concrete Rust snippets showing the exact API to implement
- Module registration instructions
- Test expectations

When the path form is used, the user references the file directly:
> "Execute the plan at\n  docs/plans/2026-03-06-database-improvements-turso-impl.md"

When the inline form is used, the full spec is pasted verbatim:
> "You are implementing a project per the following spec. ## SPECIFICATION # Implementation Spec: Single Experiment Step for Autoresearch Loop > Generated from: docs/superpowers/specs/autoresearch-tasks/T11-single-experiment.md ..."

## Examples

```
You are implementing a project per the following spec. ## SPECIFICATION # Implementation Spec: Budget Tracker for Autoresearch Experiment Loop > Generated from: docs/superpowers/specs/autoresearch-tasks/T10-budget-tracker.md > Generated at: 2026-03-11T21:49:26.112710+00:00 ## Goal Implement a BudgetTracker struct...
```

```
Execute the plan at
  docs/plans/2026-03-06-database-improvements-turso-impl.md
```

```
Implement the following plan: # Dependency Upgrade Implementation Plan ## Context The Forge project has 8 Rust crates with major updates available...
```
