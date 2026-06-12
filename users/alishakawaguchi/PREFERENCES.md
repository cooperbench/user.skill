# Preferences: alishakawaguchi

## Pushback distribution

| Type | Rate | What it means |
|---|---|---|
| non_pushback | 74.3% | Accepts and moves on — often with a slash command or "commit and push" |
| correction | 18.4% | Issues a precise redirect, usually 1 sentence |
| failure_report | 5.1% | Pastes raw terminal error output |
| takeover | 2.2% | Interrupts and issues the next command directly |

## What triggers correction

- **Misunderstood intent**: Agent does X when user wanted Y. "no thats not what I wanted. I didn't want it to auto trigger."
- **Wrong value/parameter**: Agent uses 6 when user wants 3. "update E2E_CONCURRENT_TEST_LIMIT for droid to be 3."
- **Poor naming**: Agent picks unclear names for files or commands. "prob is really an agent / entire evaluator. e2e test is a test writer."
- **Excessive permissions**: Agent proposes `--dangerously-skip` or overly broad allowlists. "don't use dangerously skip. list exact permissions allowed be very strict."
- **Structural wrong turn**: Logic placed in wrong location. "the commands should point to the skill md file instead of duplicating logic."
- **Over-dependence on hardcoded paths**: "can you clean up skill. make it less dependent on exact file paths."

## What triggers takeover

- Agent is mid-execution and the user has already decided the next step. They interrupt and paste either `/commit-commands:commit` or "commit and push" directly.
- Example: agent explains `IsPaneDead` in detail → user replies "commit and push" (no engagement with explanation).

## What satisfies them

- Clean "Done." or brief summary with no trailing insight box — they do not read `★ Insight ─────` sections.
- A one-line command they can copy: `gh workflow run e2e-triage.yml --ref ...`
- Correct code with the lint passing.
- A PR created and pushed without follow-up questions.

## Workflow habits

1. **Plan mode first**: Uses Claude Code's plan mode to design implementation. The plan is exported as a massive markdown block.
2. **Paste plan to execute**: Opens a new session with "Implement the following plan: ..." followed by the full plan.
3. **Commit slash command**: After implementation, triggers `/commit-commands:commit` or types "commit and push."
4. **PR**: Types "create pr" to open a PR.
5. **Inline follow-up**: Any corrections to the PR come as short steering messages in the same session.
6. **Periodic reviews**: Uses `/simplify` and `/security-review` as standalone prompts.

## Test and code quality views

- Aggressive about removing trivial tests: classifies unit tests that "test a constant" or "test Go's struct literal syntax" as candidates for removal.
- Wants tests to prove non-obvious invariants, not verify obvious behavior.
- Lint must pass before commit: pastes `golangci-lint` output and expects the agent to fix it.
- Favors integration over mocks: "plan has bite-sized steps" suggests preference for concrete, verifiable steps.

## Stack and tool preferences (observed)

- **Language**: Go (primary)
- **Task runner**: `mise` (e.g., `mise run fmt && mise run lint && mise run test:ci`)
- **CI**: GitHub Actions
- **Commit tooling**: `/commit-commands:commit` slash command
- **Agent**: Claude Code exclusively (100% of sessions)
- **Linter**: `golangci-lint`
- **Terminal multiplexer**: tmux (for E2E interactive tests)
- **E2E agents tested**: Factory AI Droid, Gemini CLI, Claude Code, OpenCode

## Explanations

- Does not ask for explanations before acting. The plan already contains the analysis.
- Occasionally asks "why" questions when confused by a UI or system behavior: "why is there a * nect to agent integration", "why can't it exist on my branch?"
- Rarely asks "how" questions about their own codebase: "explain difference between @cmd/entire/cli/e2e_test/ and @cmd/entire/cli/integration_test/", "how hard to setup e2e test for droid", "how to run specific test TestE2E_BasicWorkflow."
- Asks "is X necessary / valuable?" as a genuine cost-benefit question, not rhetorical: "is IsPaneDead necessary / valuable?"
