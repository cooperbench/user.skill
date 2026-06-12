# Preferences — dipasqualew

## Pushback distribution

| Type | Rate |
|------|------|
| Correction | 50% |
| Non-pushback | 29% |
| Failure report | 21% |

Half of all follow-ups are corrections. This user almost always has something to adjust.

## What triggers correction

- **Wrong approach / over-engineering**: agent picks a complex path when a simpler one exists → "No we can make this simpler mate."
- **Subtle logical bugs**: wrong env var, dead code never wired up, wrong array index → long precise technical critique
- **Missing a rename/UX detail**: `run-review` should be `review`; `$0` shows as `bun` instead of `vibx`
- **Questions asked one at a time**: batch UX questions into one `AskUserQuestions` call
- **Output format leakage**: CI mode produces fenced JSON block + commentary instead of raw JSON only
- **Agent declares done when it isn't**: user runs the binary, gets an error, pastes it

## What satisfies

- "Yeah fix" — agent identified the right issue, just fix it
- "Cool." — positive acknowledgment before the next task
- "That works" / "That seems great" — brief affirmation of a proposal before pivoting
- Accepts long agent summaries without pushback when implementation is correct (non_pushback: 29%)

## Workflow habits

**Planning**: Will write 685-word plans in full and paste them as a session-opening prompt ("Implement the following plan:"). Also exits plan mode and pastes a full verification checklist.

**Delegation**: 99.3% of code is written by the agent. User does not write code in prompts; they write specs, pastes, and corrections.

**Testing**: Provides explicit verification steps as a checklist. Runs commands locally and pastes raw output. Does not trust "tests pass" from the agent — runs the binary themselves.

**Commits**: Uses a `/commit` skill. Doesn't manually compose commit messages.

**Interruption**: Freely interrupts the agent mid-run with `[Request interrupted by user]` when the direction is wrong.

**Docs**: Explicitly tells the agent to read online documentation: "Read the documentation - The latest documentation online. That's important."

**GitHub**: Uses `gh` CLI and GitHub Actions. References PR numbers by `#1`, `#2`. Expects agent to detect current PR automatically (local or CI).

## Stack preferences visible in prompts

- **TypeScript/Bun** over Python for new CLIs (explicitly migrating Python scripts to `vibx`)
- **Python** acceptable for quick scripts ("Python for now as it requires no setup")
- **`bun build --compile`** for single-binary distribution
- **yargs** for CLI argument parsing
- **vitest** for tests in Bun monorepo
- **`gh` CLI** for GitHub operations (not raw API calls)
- No preference stated for frontend; this is all CLI/backend tooling

## Explanation preference

Results over explanations. When the agent produces a summary table of what it did, the user ignores it and issues the next command. Does not ask "why" — asks the agent to just do it.
