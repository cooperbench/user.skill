---
name: commit-by-name
description: Tiryoh requests git commits with short imperative phrases that name the specific files or directories to stage — no explanation of why, no message suggestion.
---

Commit requests are terse imperatives. Tiryoh specifies what to commit but leaves the commit message entirely to the agent. Sometimes in Japanese, sometimes in English.

**Pattern**: `"commit <what>"` or `"<what>をcommitして"` or just `"commitして"` after recent work.

Examples:
- `commit .claude and .entire directory`
- `commitして`
- `OK, 修正コミットしておいてください。`

The English form tends to name specific paths. The Japanese form ("commitして") appears after a recent fix where the scope is obvious from context.
