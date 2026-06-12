# Preferences — moven0831

## Pushback distribution

- **Non-pushback (acceptance)**: 55.4%
- **Correction**: 32.5%
- **Failure report**: 12.0%

## What triggers correction

- **Wrong parameter/field name**: immediately corrected with the exact string (`"it's \"moltbookApiKey\""`)
- **Missing field in spec or command**: one-line addition (`"the postinig api should have title"`)
- **Agent asking a question instead of acting**: redirect to act (`"Create a proper spec system in markdown syntax..."` — full spec dump to bypass the question)
- **Agent drifting into a long explanation when action is wanted**: interrupt (`[Request interrupted by user]`)
- **Agent proposing a static import where a conditional one is needed**: catches it, asks for the correct approach in the PR feedback loop
- **Agent offering wrong option letter or wrong default**: picks the correct one
- **Spec/plan out of sync**: `"update the spec"`

## What triggers failure reports

- Same command still errors after an agent-proposed fix: `"what about now"` + fresh log dump
- Error is unchanged even after restarting all processes: user notes this explicitly and re-pastes
- Agent lists commands with wrong parameter names: user runs them verbatim and they fail

## What satisfies

- `"looks good"` / `"it works"` / `"sure"` — brief, immediate approval
- No follow-up questions after a terse accept signal means the agent can proceed
- Single-letter `A` or `B` in response to a multi-option proposal = full approval of that path

## Workflow habits

- **Plan-first, always**: sessions either start with a `/superpowers:brainstorming` plugin or a pre-written `Implement the following plan:` block. Never jumps straight to "write the code".
- **Chunk plans into files**: explicitly asked to split a large plan file into per-chunk files for better agent execution; approves when it's done.
- **No test-driven development observed**: 3.5% of intent is `test`; testing is E2E via curl commands, not unit tests.
- **Git via plugin**: uses `/commit-commands:commit-push-pr` rather than dictating git commands.
- **CLAUDE.md maintenance**: runs `/init` and `revise-claude-md` skill after sessions to persist learnings.
- **Reference docs as first-class artifacts**: pastes full URL lists and asks the agent to add them to `docs/` so future agents can find them.
- **Interrupt freely**: uses `[Request interrupted by user]` multiple times; not shy about killing an in-progress response.
- **Dev mode pragmatism**: happy with dev-only endpoints, fake API keys, and stubs while waiting for real credentials.

## Tool / stack preferences

- TypeScript (relay, frontend)
- Hardhat + Solidity (contracts)
- UniRep + Semaphore protocol
- Express + SQLite (relay backend)
- Yarn workspaces (monorepo)
- curl for E2E testing
- Terminal/TUI for UI ("better tech vibe")
- `create-unirep-app` scaffold as starting point
