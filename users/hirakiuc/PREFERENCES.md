# Preferences: hirakiuc

## What triggers correction (26.1% of prompts)

- **Skipping the proposal step**: Agent reads feedback and immediately starts coding.
  Correction: "Wait, please make a proposal to address those feedback."
- **Wrong branch**: Agent makes code changes on `main` instead of a topic branch.
  Correction: "Hey, do you forget about this project development workflow? Before making
  code change, you should create a topic branch..."
- **Unexpected scope**: Agent produces a large diff without explanation.
  Correction: "Wait, could you analyze the current situation? I'm really curious why this
  topic branch needs to be changed with so much diffs."
- **Not researching before attempting**: Agent struggles with an unfamiliar API and tries
  to guess instead of looking it up. Correction: "I think, you should research related
  knowledge online at first."
- **Continued feedback delivery without re-reading file**: Correction: "got some feedback.
  please check the @.agent/feedback.md file."

## What triggers failure reports (8.7% of prompts)

- CI failures discovered externally (hirakiuc checks CI themselves, not the agent).
  Report: "CI status shows failure. please check and fix it."
- Unexpected agent state change: "what happened?"

## What satisfies them

- Agent that follows the topic-branch → PR workflow without being reminded.
- Agent that reads @-referenced files before acting.
- Agent that makes a proposal before implementing.
- Agent that proactively researches (online) when stuck on an unfamiliar library.

## Workflow habits

- **Planning first**: Yes — expects proposals before refactoring or large changes.
- **Git discipline**: Very structured. topic branch → commits → PR → merge → pull main.
  Tracks merge events and issues follow-up instructions ("I have merged the pull request
  on GitHub. switch to the main branch and pull the latest commits.").
- **Feedback loop**: Uses `.agent/feedback.md` as an external inbox for code review
  comments. Drops feedback there; tells agent to check it.
- **CI monitoring**: Watches CI themselves; reports failures as one-liners.
- **Explanations**: Asks "Why?" or "What happened?" when something surprises them, but
  only after something unexpected occurs — not as a regular habit.
- **Commit cadence**: Delegates entirely to agent; only enforces the topic-branch rule.
- **No test-driven opening**: Does not specify tests explicitly; relies on AGENTS.md rules
  (testify, require for prerequisites).

## Stack preferences (from project context)

- Go with CGO-free SQLite (`modernc.org/sqlite`)
- bubbletea v2, bubbles, lipgloss for TUI
- OpenTelemetry for observability
- testify for assertions
- Gemini CLI as coding agent
- `make build test lint` as validation cycle
