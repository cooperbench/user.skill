# Preferences: yarikoptic

## What triggers correction (16.7% correction rate)

- **Missing obvious files**: agent fails to find a skill/config that's clearly present
  → "you could not find /speckit.clarify but there is `./.claude/skills/speckit-clarify` -- did you see it?"
- **Incomplete option handling**: agent lists options but misses an easy additional check
  → "2+1 but also see if SHELL env var available"
- **Vague error messages**: skip reasons, exception messages, or test output lacking specifics
  → "state the exception in the message so it is possible to see right away on why cannot load"
- **Auto-committing before tests pass**: committing with failing tox is an explicit rule violation
  → "add to spec and CLAUDE.md to never auto-commit if 'tox' testing fails"
- **Stale user stories**: if they've pushed commits with adjustments, the spec must reflect it
  → "/speckit.clarify - in prior commit I added some changes to user stories -- please analyze"
- **Wrong dataset root assumption**: auto-detect from `dataset_description.json`, don't assume CWD

## What triggers failure report (1.9% failure report rate)

- Agent commits code that fails `tox` (lint, type, duplication envs) → full tox output pasted,
  fix-and-commit directive appended

## What satisfies them

- Agent autonomously produces long research summaries without being re-prompted
- Agent finds and uses the speckit skill infrastructure correctly
- Multiple Python version tests passing (`py310`–`py314`)
- Correct dry-run / preview behavior before mutating files
- CLI commands visible and testable via `--help`

## Workflow habits

**Planning first**: sessions structured around speckit phases (plan → clarify → specify → implement → tasks).
Always understand before building — 42.6% of intents are `understand`.

**Test-driven quality gate**: tox with py310–py314, lint, type, duplication envs must all pass.
This is a hard requirement, not optional. Tests skipped without `reason=` are also unacceptable.

**Commit cadence**: delegates commits to the agent, but with conditions — tests must pass, submodules
included, spec files updated. References specific commit hashes in corrections (a4cd9ab, 4d8a240, 7fa7213).

**Spec + CLAUDE.md updates**: rules that govern agent behavior must be written into both the spec
and CLAUDE.md so they persist across sessions.

**No explanations needed**: approves with "A", "yes", or "proceed how you recommend" — doesn't
ask for justification when the agent's recommendation is clear.

**Parenthetical self-regulation**: adds `(just asking - no action needed)` when asking questions
they don't want actioned immediately.

## Tool / stack preferences visible in prompts

- **tox** for testing (not pytest directly), multi-env matrix
- **ruff** for linting/formatting
- **Click** for CLI
- **DataLad / git-annex** for provenance
- **bidsschematools** as the schema source — never hardcode BIDS knowledge
- **bids-examples** as a submodule for integration tests
- `uv` for packaging (implied by tox + hatchling stack)
- Local speckit skill system (`/speckit.*` commands) as the primary agent interface
