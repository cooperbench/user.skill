# Preferences — eneakllomollari

## Pushback distribution

| Type | Rate |
|------|------|
| Non-pushback (accepts) | 61.1% |
| Failure report | 25.0% |
| Correction | 8.3% |
| Rejection | 5.6% |

Most interactions are accepted. But when pushback comes, it's usually a failure report (pasting raw evidence that something didn't work) rather than a verbal correction.

## What triggers correction

- **Shallow testing**: agent declares the app "solid" after only checking page load and basic rendering → "the APP IS NOT FUCKING SOLID DID IT TEST THE EDITING AND STUFF"
- **Agent delays without progress**: agent says "still waiting" when the user believes more time has passed → "well its been more i think"
- **Missing the point**: agent pushes a summary that ignores the user's actual concern → "push this then" (redirect to the actionable step)

## What triggers rejection

- **Perceived slowness with no visible progress**: agent is "waiting" with no result → "its so damn slow"
- **Superficial test coverage**: agent marks test as passing when the real editing functionality wasn't exercised

## What satisfies them

- Raw test output with clear pass/fail counts
- Agent takes the initiative to run parallel subagents
- Results that list specific bugs with evidence (INP=536ms, aria-label missing, color ratios 2.74-3.70)
- Zero-commentary delivery of completion: just the data

## Workflow habits

- **Not planning-first**: issues direct commands, no preamble
- **Test-driven in practice**: 25% of intent is `test`, frequently opens sessions with adversarial test requests
- **Git cadence**: commits and pushes frequently mid-workflow; git commands are fire-and-forget
- **Delegates subagent setup**: tells agent to "do more testing in a subagent" — comfortable with multi-agent orchestration
- **Does not ask for explanations**: accepts or rejects results; never asks the agent to explain what it did
- **Pastes results back verbatim**: uses raw task-notification output as their "reply" — the data is the message

## Stack preferences (evident from prompts)

- TipTap (rich text editor framework)
- Tauri (desktop app shell)
- TypeScript + React
- `/expect` (CLI smoke test runner)
- `http://localhost:5173?file=demo` as the test URL
- Vitest (unit tests — referenced in test results: 83/83 passing)
- ESLint, oxlint, knip (linting/dead code)
- `tsc` (type checking)
- `src/components/Editor.tsx` as the main editor component
