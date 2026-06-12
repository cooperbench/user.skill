# PREFERENCES

## What triggers correction (37.7% correction rate)

pfleidi is the highest-correcting persona type in the dataset. He corrects when:

1. **Scope creep** — The agent reviews or modifies code outside the current branch. He will ask pointedly if the agent is aware of the explicit constraint.
2. **Bad naming** — Any function, variable, or struct name that doesn't accurately describe what it does. He challenges with a question, proposes an alternative, and often picks from his own suggestion or says "X is fine" to the agent's proposal.
3. **Unnecessary abstractions** — Wrapper structs or helper functions that add layers without necessity. He asks "Is this necessary?" before the code ships.
4. **Tests that don't test the thing** — He specifically calls out tests that re-implement the production logic inline and thus don't catch regressions. He wants tests to exercise the real production path.
5. **Template non-compliance** — If he provides a template (design doc, PR description, span naming convention) and the agent deviates, he sends back a short correction: "This doesn't follow the structure I in the template."
6. **Comment content** — He notices when `//nolint:contextcheck` rationale comments are at risk of being removed or mangled.
7. **Span naming in perf instrumentation** — Variable names for spans must correspond to the code they measure, not the comments around that code.

## What satisfies him

- One-word acknowledgments that the thing was done: he just says "continue" or "Looks good" or "yes, continue"
- When he offers an alternative name and the agent confirms it can work: "collectCheckpointsByAge is fine"
- Getting a clean "All green" after tests pass
- A concise PR description he can copy to clipboard

## Workflow habits

- **Design first**: Uses `/superpowers:brainstorming` before implementation. Never jumps straight to code.
- **Plan before executing**: Uses writing-plans skill, saves plan to `docs/plans/YYYY-MM-DD-feature.md`. Does NOT commit plans.
- **Subagent-driven execution**: Dispatches subagents per task via subagent-driven-development skill.
- **Code review after each task**: Uses `/superpowers:requesting-code-review` focused strictly on branch changes.
- **Branch-scoped reviews**: Always explicitly scopes reviews to "changes in the current branch only."
- **Finish with PR**: Uses finishing-a-development-branch skill, creates PR via `gh pr create`.
- **Clipboard usage**: Frequently asks for PR descriptions or markdown to be copied to clipboard rather than displayed.
- **Interrupts mid-task**: Cuts off the agent when he sees a deviation. Does not wait for the agent to finish.
- **Asks before approving design**: At key inflection points ("Does this make sense?") before implementation starts.

## Tool/stack preferences visible in prompts

- **Go**: The entire codebase is Go. He's familiar with `context.Context` propagation, `sync.Once`, `sort.SliceStable`, interfaces, nolint annotations.
- **Git**: Uses `gh pr create`, `git merge --squash`, squash-merge workflows, metadata branches.
- **Claude Code with superpowers plugins**: `/superpowers:brainstorming`, `/superpowers:requesting-code-review`, `/simplify`, `/commit-commands:commit-push-pr`.
- **OpenTelemetry as a reference**: When designing observability, looks at OTel patterns as the benchmark.
- **No heavyweight dependencies**: Chose to hand-roll the `perf` package over adopting OTel — values minimal dependency trees.
- **TDD-adjacent**: Expects tests to be added when implementing, and for them to be meaningful (not tautological).
- **e2e tests**: Distinguishes e2e tests from unit tests, wants e2e tests to mirror real user workflows ("a user runs `entire resume` on a feature branch, not main").

## What he explicitly rejects

- Reviewing the whole project when asked to review only branch changes
- Committing plans: "Plans are not version controlled in this repo."
- Tests that re-implement production logic rather than calling it
- Span/variable names that don't correspond to what the code actually does
- Unnecessary wrapper structs when the underlying type already has the needed field
