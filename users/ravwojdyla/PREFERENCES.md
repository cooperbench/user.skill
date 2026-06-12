# PREFERENCES — ravwojdyla

## What triggers correction (52.6% of responses)

- Agent summarizes what it did rather than being done silently → user adds a missed micro-requirement.
- Agent misses a formatting preference (f-strings, comma separators for big numbers).
- Agent uses the wrong library (draccus when click was expected).
- Agent says "that's already handled" to something the user just witnessed fail in CI → user ignores the explanation and reports the real error or restates the requirement.
- Agent implements a feature with broader scope than intended (e.g., comment trigger on all issues, not just PRs) → user narrows: `"I want comments on PRs only"`.
- Agent leaves out a code comment the user specifically cares about.

## What constitutes failure report (5.3%)

- CI/GitHub Actions error pasted verbatim with minimal framing.
- No debugging attempt before reporting — just the log.

## What satisfies (42.1% non-pushback)

- Test runs that pass without surprises.
- Commits and pushes that succeed.
- Simple confirmations with no over-explanation.
- Answers to understanding questions (`"ok, with the current workflow file, should the review trigger on every new PR?"`) that are concise and direct.

## Workflow habits

- **Not test-driven**: writes implementation first, asks for integration tests after as a verification step, not as design.
- **Commit cadence**: commits at the end of a task when satisfied, not incrementally (`"ok, commit and push"`).
- **Planning style**: for major refactors, writes the full plan ahead of time and opens with it as a spec dump. For smaller tasks, iterates by correction.
- **Recipes**: references docs/recipes (e.g., `@docs/recipes/fix_issue.md`) as workflow templates — expects the agent to follow them.
- **Does not ask for explanations unless verifying** (`"ok, with the current workflow file, should the review trigger on every new PR?"`). Otherwise just wants results.
- **Interrupts mid-task** when agent takes too long, then resumes with `"continue as you were"`.

## Tool and stack preferences

- `click` over `draccus` for CLI argument parsing.
- f-strings over `.format()` or `%` formatting.
- `uv run` to execute tests.
- GitHub PRs/issues referenced by URL, not shorthand.
- Inline comments added explicitly when user asks; not expected by default.
- Typed outputs/inputs with concern for forward compatibility (raises schema evolution problems proactively).

## Delegation pattern

- Delegates 96% of code to the agent.
- Specifies precisely: library, format, file path, exact behavior.
- Does not specify: cosmetic code style, variable names, function length.
- Trusts the agent to handle pre-commit hooks, imports, and test wiring unless it fails.
