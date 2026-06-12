---
name: ci-failure-paste
description: >
  Trigger: CI or typecheck fails after a PR is created, or something is not producing output.
  upamune reports failures with raw logs or a terse label, no analysis.
---

upamune never diagnoses failures himself before handing them to the agent. He either:

1. **Pastes the raw log verbatim** with no surrounding prose—just the terminal output, including timestamps and exit codes.
2. **States the symptom in ≤4 words** in Japanese.

He does not say "it seems like" or "maybe the problem is". He does not apologize. He reports and expects the agent to investigate.

**Examples:**

Terse label:
> "ci コケてる"

Raw log paste (no wrapper text):
> "5s\nRun bun run typecheck\n$ tsc --noEmit\nsrc/agent/session.ts(9,1): error TS2578: Unused '@ts-expect-error' directive.\n..."

Missing output:
> "何も出てないのでそれを調査してほしい"

Redirecting to a search tool when stuck:
> "o3-search で解決策見つけられない??"
