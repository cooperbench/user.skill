---
name: plan-dump-kickoff
description: >
  Trigger: opening a session to implement a substantial code change. User pastes a complete
  pre-authored implementation plan as the first message, starting with "Implement the following
  plan:" followed by dense structured markdown.
---

The user writes plans in plan mode before starting an agent session. When ready to execute, the
opening prompt is the entire plan pasted verbatim. Plans are 300–1154 words, structured with:
- `##` section headers (Context, Root Cause, Changes, Verification)
- File-path tables with repo, file, change columns
- Code blocks with exact Go snippets including line number references
- A verification block (`go build ./...`, `go test ./pkg/...`)
- Often a transcript reference at the end: `"If you need specific details … read the full
  transcript at: /Users/jan/.claude/projects/…"`

The plan specifies every file, every function, often every line to change. The user expects
the agent to execute exactly this plan, not to redesign it.

**Example opening (abbreviated):**
> `Implement the following plan: # Fix Missing rows.Close() Memory Leaks in SQLite3 Queries ## Context Production memory leaks traced to queries that do full table scans … ## Findings **22 total .Query() calls** … **7 do not** … ## Changes Required ### 1. internal/repository/stats.go — 6 functions missing defer rows.Close() … ## Verification go test ./internal/repository/...`

**Example short-form opening (no plan, just a task):**
> `Apply the patch at @~/Downloads/fix-removed-metrics-shown-as-missing.patch`

> `Update ReleaseNotes and set correct latest Migration`
