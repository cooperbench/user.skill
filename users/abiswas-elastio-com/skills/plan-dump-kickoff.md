---
name: plan-dump-kickoff
description: >
  Trigger: user is starting a large feature session. They open with "Implement the following plan:"
  followed by 300–2678 words of structured markdown spec including step numbers, file paths,
  line numbers, SQL schemas, code snippets, and verification checklists.
---

# Plan-dump kickoff

When opening a large feature session, this user pre-writes a complete implementation plan and pastes it as the first message. The plan is structured with `## Step N:` headers, pipe tables for file lists, backtick code blocks for exact snippets, and a `## Verification` section at the end.

Key characteristics:
- Always starts with "Implement the following plan:"
- Includes exact file paths (`api/internal/api/cloudinary_handlers.go`)
- Includes line number references ("line 505", "~line 224")
- Includes Go struct definitions, SQL migration files, TypeScript interfaces
- Ends with a numbered verification checklist (build, test, manual steps, deploy)
- May include note: "If you need specific details from before exiting plan mode... read the full transcript at: /Users/anshumanbiswas/.REDACTED.jsonl"

**Example (abridged):**
> "Implement the following plan: # Plan: Asset Management Section in Settings ## Context Users need a way to manage all files they've uploaded across projects. Currently, files can only be seen per-task in TaskDetail. The new \"My Assets\" section in Settings lets users browse, search, edit alt text, and delete their own uploads, plus view files from shared project members. --- ## Changes Overview ### Backend (2 new handlers + 2 routes) **File: `api/internal/api/cloudinary_handlers.go`** 1. **`HandleListAssets`** — `GET /api/assets?q=&type=&limit=&offset=` ..."

After pasting the plan, the user goes quiet and expects full autonomous execution. They will interrupt if something looks wrong.
