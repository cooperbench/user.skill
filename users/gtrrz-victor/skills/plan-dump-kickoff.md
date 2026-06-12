---
name: plan-dump-kickoff
description: Victor opens big implementation tasks by pasting a complete pre-written plan with exact file paths, line numbers, before/after code snippets, and a verification section. Trigger when starting a session with a large feature or refactor.
---

# plan-dump-kickoff

Victor pre-writes detailed implementation plans (often using Claude's plan mode or a separate brainstorming session) and opens a new agent session by pasting the entire plan verbatim. The plan format is always:

```
Implement the following plan:

# Plan Title

## Context
[Why this change is needed]

## Changes

### 1. FunctionName (`path/to/file.go`)
- Specific line reference
- Before/after code snippet in fenced blocks

### 2. …

## Files to Modify
| File | Changes |

## Verification
mise run fmt && mise run lint && mise run test:ci

If you need specific details from before exiting plan mode … read the full transcript at: /Users/gtrrz-victor/.REDACTED.jsonl
```

The plan ends with a verification block and sometimes a reference to the full transcript path (redacted in this dataset).

## Verbatim examples

**Example 1** (refactor session opener):
> "Implement the following plan: # Plan: Remove backward-compatibility fallbacks for unknown agent types ## Context Agent type tracking was added on Jan 9, 2026 (6 days after repo creation) and shipped in v0.3.5 (Jan 15). There are no realistic production sessions without agent type info. The codebase has several backward-compat patterns (`DefaultAgentType`, `isSpecificAgentType`, `ResolveAgentForRewind` fallback, backfill logic in hooks) that add complexity for a case that no longer exists. Clean them up. ## Changes ### 1. Remove `DefaultAgentType` and `isSpecificAgentType` (`strategy/common.go`) …"

**Example 2** (smaller refactor, still plan format):
> "Implement the following plan:\n\n# Replace SQLite access with `opencode session delete`\n\n## Context\n\n`sqlite.go` runs raw SQL against OpenCode's database. OpenCode has `opencode session delete <id>` for this. The current SQLite approach hardcodes the DB path, schema, and requires `sqlite3` installed.\n\n## Verification\n\n`mise run fmt && mise run lint && mise run test:ci`"
