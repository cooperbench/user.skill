---
name: spec-dump-kickoff
description: evisdren opens a complex feature session with a pre-written implementation plan — markdown headers, file paths, tables, code blocks. Trigger when starting a multi-step feature or refactor that evisdren has clearly thought through before the session.
---

# Skill: spec-dump-kickoff

evisdren comes to complex sessions with a complete design already written. The opening message is a long markdown document (200–870 words) that specifies exactly what files to change, what the new behavior should be, and sometimes includes a table of test scenarios or seeding strategies. The agent's job is execution, not design. evisdren does NOT invite feedback on the plan before starting — they say "Implement the following plan:" or similar.

## Characteristics

- Begins with `Implement the following plan:` or a context-setting header
- Uses `##` and `###` for sections
- Includes file paths in bold or as code
- Includes code snippets (Go functions, JSON) to show the exact shape expected
- May include a table (test matrix, seeding breakdown)
- No typos — this was written carefully beforehand
- Can be 600–870 words; does not feel the need to summarize

## Verbatim Examples

**Example 1 (commit hook perf test):**
> "Implement the following plan: # Plan: Commit Hook Performance Test ## Context A user with ~95 sessions (88 ended, 6 idle, 1 active) and ~100 checkpoints experienced **25.5s** commit time vs **0.335s** without Entire (v0.4.7). We need a reproducible test that: 1. Recreates this exact scenario locally (no remote/GitHub needed) 2. Measures PrepareCommitMsg + PostCommit separately 3. Tests scaling across different session counts (10, 50, 100, 200) ## New File **`cmd/entire/cli/strategy/commit_hook_perf_test.go`** — build tag `hookperf`"

**Example 2 (strategy abstraction removal):**
> "Implement the following plan: # Plan: Remove Strategy Abstraction & Add `commit_linking` Setting ## Context The CLI has a `Strategy` interface abstraction (`strategy.go`) designed to support multiple session strategies, but only one implementation (`ManualCommitStrategy`) has ever existed. ... ## Implementation Steps ### Step 1: Add `commit_linking` setting to `EntireSettings` **Files:** - `cmd/entire/cli/settings/settings.go`"
