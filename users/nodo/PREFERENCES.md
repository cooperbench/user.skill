# Preferences: nodo

## Pushback distribution

| Type | Rate |
|---|---|
| Non-pushback (accept) | 58.5% |
| Correction | 30.2% |
| Failure report | 7.5% |
| Rejection | 3.8% |

## What triggers corrections

- **Spec/protocol gaps**: agent implements something but misses a required subcommand or capability — nodo quotes the protocol spec gap verbatim
- **Codebase consistency violations**: uses pattern X when the rest of the codebase uses Y (e.g., not trimming stderr, using type assertions instead of `As*` helpers)
- **Silently wrong output**: agent says "done" or "all clean" but CI fails or tests hang — nodo reports the failure tersely without elaboration ("it seems the test hangs or is super slow", "`golangci-lint` failed in ci")
- **Dropped lint annotations**: removing `//nolint:ireturn` comments — "don't remove the `nolint:ireturn` comments"
- **Over-broad reverts**: when reverting partially, agent misses files — "same for `cmd/entire/cli/agent/cursor/lifecycle_test.go`"

## What triggers rejection

- **Direction changes that went wrong**: if a large refactor turns out to be the wrong approach, nodo hard-reverts: "Undo the changes to migrate cursor to an external agent." / "revert it to `main`"
- No negotiation — just a terse hard revert directive

## What satisfies them

- Agent works through the full plan without mid-task questions
- Linters and tests pass on first try
- Fixes are consistent with surrounding codebase patterns (nodo notices inconsistency)
- Review comments addressed precisely — not over-addressed or under-addressed

## Workflow habits

- **Plan-first, then delegate**: writes full spec plans externally (or has them pre-written), pastes them wholesale as opening prompts
- **Code-review loop**: triggers PR review agents (both inline via `/reviewer` command and via task-based review agents), then feeds each critical finding back as a new correction prompt one at a time
- **Sequential issue fixing**: sends one review comment at a time: "Fix this comment: ...", "Another one: ...", "there a few more comments to fix: ..."
- **Interrupts freely**: mid-run interruptions are common; follows with "resume" or "continue"
- **Does not ask for explanations unless blocked**: occasionally asks "why" ("can you explain me why we need Wrap?") when something in the architecture surprises them; otherwise trusts the agent to do the work
- **Tests and linting are hygiene**: runs "run tests and litners" [sic] as a routine step, not a final gate — expects clean output
- **Commit cadence**: uses "Run git rebase main and fix the conflicts." — works on branches, rebases onto main

## Stack preferences (visible in prompts)

- Go (primary language for `entireio/cli`)
- cobra for CLI commands
- golangci-lint with `nolint` directives respected
- `context.Context` with deadlines (flags missing context propagation as a bug)
- `strings.TrimSpace` consistency with rest of codebase
- Generics where appropriate (references `readJSONFromBlob[T any]` as a codebase pattern)
- `exec.CommandContext` for subprocess management
- JSON over stdin/stdout for subprocess protocols
