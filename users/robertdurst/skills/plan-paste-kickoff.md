---
name: plan-paste-kickoff
description: How robertDurst hands off a fully-specified implementation plan. Trigger when the user is about to start a major refactor or feature — they paste a dense markdown doc with headers, tables, before/after code, and file locations, then say "Implement the following plan:".
---

# Skill: plan-paste-kickoff

When Robert is ready to build something well-defined, he writes or pastes a complete implementation specification as a markdown document and leads with "Implement the following plan:". The plan includes context, numbered change sections, before/after code blocks, a file modification table, and explicit notes on what to leave unchanged.

**Pattern:** "Implement the following plan: # Plan: [Title] ## Context ... ## Changes ### 1. ... ### 2. ... ## Files Modified | File | Change |"

## Verbatim example (truncated)

> "Implement the following plan: # Plan: Standardize `generate_resources` Return Type (E) ## Context Datadog's `generate_resources` returns `Result(#(List(Resource), List(String)), CompilationError)` (resources + warnings), while the other 3 vendors return `Result(List(Resource), CompilationError)`. This forces `compiler.gleam` to wrap each non-Datadog vendor... ## Changes ### 1. Update `generate_resources` in honeycomb, dynatrace, newrelic Change return type from `Result(List(Resource), CompilationError)` to `Result(#(List(Resource), List(String)), CompilationError)`, wrapping the final `Ok` with empty warnings `[]`..."

## Behavior notes

- Plan documents are 200–500 words with Gleam code fences.
- Tables list every file to be modified with a one-line description of the change.
- Sections labeled with letter suffixes (A, B, C) that match a prior discussion: "Implement the following plan: # Plan: Deduplicate Codegen Vendor Boilerplate (A + B + C)".
- After implementing, he references the completed items when sequencing next steps: "lets first do A + B + C. When done, lets see if D + E make sense."
