# Preferences: tslateman

## What satisfies him

- Agent completes the task without needing clarification on details that were implicit.
- Output is clean: passes ruff check + format, tests pass, no stale references.
- Commits are atomic and the body explains the why without padding.
- Names are precise and carry meaning (he notices when they don't).
- The agent uses subagents when the task warrants parallelism.
- Changes to architecture docs stay consistent with implementation decisions.

## What triggers corrections (36.7% of turns)

- **Scope creep:** Agent deletes something it wasn't asked to delete.
  > "woah, I didn't want to delete .git/hooks/pre-push.pre-entire"
- **Over-explanation in commits:** Agent adds a "note" section when the body is enough.
  > "the commit body covers it, skip the note"
- **Low-utility features:** Agent adds a command/skill that doesn't pull its weight.
  > "i think we can cut the /note-why - utility feels low"
- **Misidentifying the target:** Agent removes the skill when he meant the note.
  > "oops! keep the /vamp skill - i just mean drop the note"
- **Wrong tool:** Agent does something the wrong way (e.g., files a GitHub issue without
  checking templates first).
  > "hey... we probably should NOT file issues in this way - we ought to check guidelines first"
- **Verbosity in prose:** Asks to tighten a line, drop em dashes, condense a philosophy
  section to one quote.
- **Stale references in docs:** Plans or docs still referencing `make` after the decision to
  use `just`.

## What triggers rejection (1.9% of turns)

- Agent asks a clarifying question when he already made the call.
  > "the commit body covers it, skip the note" (rejecting the question itself)
- Agent proposes more work when he wants a direct action.
  > "delete plans/plan-praxis-sync-promote.md" (rejecting the prior suggestion)

## Workflow habits

- **Plans before building:** Reviews architecture docs, consistency between plans 001-004,
  before any implementation starts. Uses subagents for the review pass.
- **Commit cadence:** Commits after each meaningful unit of work, using `/commit` slash command.
  Commits have bodies. Does not squash everything at the end.
- **Does not ask for explanations:** Expects the agent to just do it. If he wants to
  understand something, he asks "explain X" in a separate message.
- **Delegates implementation, steers output:** His messages are coordination, not code.
  "use a team of agents" is his typical instruction for anything substantial.
- **Captures decisions:** Uses Lore CLI to record architectural decisions after significant
  sessions. Considers this part of the workflow, not optional.
- **Prefers `just` over `make`:** Notes it as a preference explicitly.
  > "note a preference for just over make (justfile over makefile)"
- **Protobuf over JSON** for event schemas. Python-first, Rust as future hot-path target.

## Tool/stack preferences visible in prompts

- `uv` for Python package management
- `ruff check` + `ruff format` (always run both after changes)
- `pytest` with `--run-integration` flag gating for integration tests
- `justfile` for task running
- SQLite for lightweight persistence
- MQTT for messaging
- Git notes for annotating commits with rationale
- Subagents/Task tool for parallel work
