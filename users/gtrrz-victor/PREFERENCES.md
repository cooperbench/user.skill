---
name: gtrrz-victor-preferences
description: What Victor corrects or rejects, what satisfies him, and workflow habits
---

# Preferences

## Pushback distribution

| Type | Rate | Meaning |
|------|------|---------|
| correction | 48.2% | Agent output is wrong; Victor redirects with a specific technical critique |
| non_pushback | 43.7% | Accepts and continues |
| failure_report | 6.3% | Pastes a build/test/lint error and expects a fix |
| takeover | 1.5% | Sends a git action so fast the agent didn't finish explaining |
| rejection | 0.3% | Outright rejects the agent's direction |

## What triggers corrections

- **Nil/error handling gaps**: He catches nil pointer risks, unguarded error paths, subagentsDir="" edge cases, empty transcript data reaching unmarshal logic.
- **Backward-compatibility oversights**: When a refactor breaks handling of old data formats or old agent types, he objects with the exact scenario that breaks.
- **Wrong test coverage**: He notices missing tests for interactive paths, missing assertions for new fields, test expectations that don't match the assertion.
- **Incorrect logic after refactor**: When he asks to clean up code and the agent leaves a bug (wrong index math, wrong flag logic), he catches it immediately.
- **Over-engineering**: "do not implement DisableVersionCheck", "I don't want users to optout please" — he rejects features he didn't ask for.
- **Outdated comments**: Notices when comments reference old function names or old behavior.
- **Verbose agent summaries that miss the point**: He redirects with "eval this feedback:" + the actual issue.

## What satisfies him

- Clean implementation with no dead code left behind.
- Passing `mise run fmt && mise run lint && mise run test:ci`.
- Short PR descriptions — "keep description brief, just what we have done."
- When the agent follows his exact plan without adding unrequested features.
- Short confirmations followed by immediate action.

## Workflow habits

- **Pre-writes plans**: He uses Claude's plan mode (or another tool) to generate a detailed implementation plan, then opens a new session and pastes "Implement the following plan: …" — the agent is an executor, not a planner.
- **Verification is always the same**: `mise run fmt && mise run lint && mise run test:ci`. He includes this at the end of every plan. Sometimes also `go build ./...`.
- **Commit early and often**: "commit it" after each meaningful change. Often wants separate commits for separate concerns: "commit our changes in two commits please, the first for the list changes and the second for -c".
- **Draft PRs**: "push and draft PR please" — doesn't want open PRs from the agent.
- **No explanations requested**: He asks for explanations rarely (9.7% understand intent). When he does, he wants a direct answer, not a tutorial.
- **Uses session interrupts**: Many "[Request interrupted by user for tool use]" entries — he monitors agent tool calls in real time and cuts them off.
- **References Linear**: Mentions issue IDs like "ENT-109 (linear)" mid-session to provide context.
- **Stack preferences**: Go, `mise`, `go-git`, PostHog, GoReleaser Pro, Cobra, Vitest, TypeScript Agent SDK. Nothing exotic.
