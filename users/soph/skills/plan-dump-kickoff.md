---
name: plan-dump-kickoff
description: Trigger when Soph opens a session by pasting a full structured implementation plan prefixed with "Implement the following plan:". The plan is markdown with headers, file paths, line numbers, code snippets, and a verification command. The agent is expected to execute it verbatim with no discussion.
---

# Plan-dump kickoff

Soph frequently enters plan mode, drafts a complete implementation plan, then pastes the whole thing as the session opener. The message always starts with **"Implement the following plan:"** followed by a markdown document.

The plan includes:
- A context section explaining the problem
- Files to modify with exact line numbers and function names
- Before/after code snippets
- A verification step (usually `mise run fmt && mise run lint && mise run test:ci`)
- Sometimes a trailing note: "If you need specific details from before exiting plan mode… read the full transcript at: /Users/soph/…"

The agent is expected to execute the plan without asking for clarification. Soph only follows up if the agent misses a step or makes an error.

**Example 1 (short plan):**
> "Implement the following plan:\n\n# Fix: Separate OpenCode tool detail extraction in summarize.go\n\n## Context\n\n`extractGenericToolDetail` in summarize.go is shared between OpenCode (camelCase `\"filePath\"`) and Gemini (snake_case `\"file_path\"`). Adding `\"filePath\"` to the shared function mixes format concerns from two different agents.\n\n## Changes\n\n### `cmd/entire/cli/summarize/summarize.go`\n\n1. Revert `extractGenericToolDetail` — remove `\"filePath\"`, keep original Gemini/generic keys\n2. Add `extractOpenCodeToolDetail` with camelCase keys…\n\n## Verification\n\n```bash\nmise run fmt && mise run lint && mise run test:ci\n```"

**Example 2 (complex plan):**
> "Implement the following plan: # Trail Store Refactoring Plan ## Context The trail store (`trail/store.go`) uses O(n) full-flatten+rebuild for every write… ## Files to Modify…"
