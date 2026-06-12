# Preferences — pjbgf

## Pushback distribution

| Type           | Rate |
|----------------|------|
| Non-pushback   | 60%  |
| Correction     | 27%  |
| Failure report | 13%  |

## What triggers correction

- **Agent leaves out a required API change**: e.g., leaving `PlainOpenWithOptions` calls unchanged when the field they pass is deprecated → immediate correction naming the exact field and the behavioral reason.
- **Agent asks for clarification instead of acting**: when the agent says "could you clarify which two issues?" on a message that already had context (however implicit) → user dumps the full issue text.
- **Agent produces dead code**: unused fields, heap allocations that serve no function → user pastes the static-analysis finding verbatim.
- **Rebase/conflict resolution may have dropped intent**: user asks for SHA-level confirmation rather than reading the diff themselves.

## What triggers failure report

- **Regression discovered after multiple commits**: user tests the feature, finds it broken, traces it to a window of commits, reports with the error message and a time anchor ("10 commits ago").
- **Broken tests after conflict resolution**: terse report, no stack trace: "Fix the broken tests - they may have been caused by a conflict resolution."

## What satisfies

- Clean, no-explanation commit confirmations: "Committed as `3005c7a8`. Working tree is clean." → user proceeds to the next task.
- Agent follows the refactor spec exactly across all callsites.
- Agent builds and tests after a dependency upgrade without being asked a second time.

## Workflow habits

- **No planning phase**: opens sessions with a direct imperative, not "let's plan X".
- **Git-heavy cadence**: nearly half of all prompts are git operations — stages and commits frequently, sometimes after every logical change.
- **Delegates test verification**: asks the agent to build and test after changes ("Build and test the code to ensure all works as expected.").
- **Interrupts when direction is wrong**: uses `[Request interrupted by user for tool use]` — does not wait for the agent to finish a bad path.
- **Selects from agent-offered options**: does not redesign; picks the closest option and moves on ("Let's go with option B").
- **References external tools**: pastes static-analysis/code-review output rather than describing issues in own words.
- **Does not ask for explanations**: no "can you explain why", no "walk me through this" — result-oriented only.

## Tool / stack preferences visible in prompts

- go-git v5 → v6 migration awareness; knows the module path change.
- Prefers `git.PlainOpen` over `git.PlainOpenWithOptions` with empty options.
- Knows that `EnableDotGitCommonDir` is now default behavior in go-git v6.
- Aware of batch fetch optimization patterns (`FetchBlobsByHash`, `CollectTranscriptBlobHashes`).
