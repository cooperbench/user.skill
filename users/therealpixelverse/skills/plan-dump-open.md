---
name: plan-dump-open
description: "Trigger: user opens a new session for a complex, well-understood change. Pastes a fully written implementation plan with headers, file paths, before/after code snippets, and rationale."
---

For non-trivial features or refactors where the user has already figured out the solution, he opens with a complete structured plan. The plan names exact files, line numbers, SQL expressions, TypeScript code snippets, and explains the "why" in a `## Context` section. The agent is expected to execute it, not design it.

**Structure** (from observed examples):
```
Implement the following plan: # Plan: [Title]
## Context
[Background + reason the current code is wrong]
## Changes
### [File path]
Change [thing] from:
```[code]```
to:
```[code]```
[Why this works end-to-end]
```

This pattern appears for both frontend fixes (navigation URL bug) and backend changes (Windows path normalization in Zod schema + ClickHouse SQL).

**Example opener:**
> "Implement the following plan: # Plan: Navigate by Display Name in Projects List ## Context The Projects list page groups sessions by **display name** (last segment of `git_remote` or `project_path`, e.g. `\"rudel\"`) via `PROJECT_DISPLAY_EXPR` in ClickHouse. Each row shows this short name in the table. However, `handleRowClick` navigates using the raw `row.git_remote || row.project_path`..."

**When NOT this pattern:** Short exploratory openers ("I see 500 errors when loading..."), UX observation sessions ("Tokens by model chart in overview looks like this [image]"), or security questions. Those are 1–2 sentences.
