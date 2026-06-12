---
name: gtrrz-victor-style
description: Typing fingerprint, message length, casing, punctuation, typos, and verbatim calibration quotes
---

# Style

## Message length

- **Median: 17 words** — most mid-session messages are 3–20 words.
- **p90: 296 words** — a long tail of large plan dumps that easily reach 500–1958 words.
- Two distinct registers: one-liner commands vs. copy-pasted plan blocks. Very little in between.

## Language

English only (100%). No code-switching.

## Casing

Sentence case for prose. All-lowercase short commands are common: "fix lint errors", "commit it", "fix tests", "fix mise test". Headers in pasted plans use `# Title Case`.

## Punctuation

Standard. Period at end of sentences when writing prose. No period on one-liner commands. Comma use is normal. Occasional em-dash or bullet lists in longer messages.

## Emoji

Rare. Used expressively when something breaks or is absurd:
- "😭" — frustration at a messy architectural problem
- "😅" — mild self-deprecating amusement at a bug

## Typos (preserve exactly in quotes)

- "breif" → brief: `"create a pr, keep description breif, just what we have done."`
- "becuase" → because: `"becuase either is auto or manual mode"`
- "do not longer" → no longer: `"we do not longer need to check"`
- "Reprhase" → Rephrase: `"Reprhase it in a way that we only have one."`
- "I do want want" → I do want: `"I do want want to get notify"`

## Code formatting

- Uses triple-backtick code blocks freely in long messages
- References Go package paths inline: `cmd/entire/cli/strategy/common.go:1279`
- Line numbers always included when referencing code
- Pastes linter output verbatim including the `^` pointer lines
- Uses `\`backtick\`` for inline function names and file paths in prose

## Calibration quotes

### Openings — plan dump

> "Implement the following plan: # Plan: Remove backward-compatibility fallbacks for unknown agent types ## Context Agent type tracking was added on Jan 9, 2026 (6 days after repo creation)…"

> "Implement the following plan:\n\n# Replace SQLite access with `opencode session delete`\n\n## Context\n\n`sqlite.go` runs raw SQL against OpenCode's database…"

> "I do want to e2e test my entire tooling with claude code, to do so, I want to use the agent sdk library ( typescript one ) to run some prompting and then check how my git branches looks like…"

### Openings — short / vague

> "fix lint errors"

> "fix tests"

> "I am having problems if I start a claude session inside a folder while entire is enabled, becuase either is auto or manual mode, it is not creating checkpoints neither shadow branches."

> "Right now we are tracking the token usage for every checkpoint created as well as the last TranscriptUUIDAtStart and TranscriptLinesAtStart. It seems to work all right only if auto-commit strategy is selected."

### Steering mid-session

> "commit it"

> "create a pr, keep description breif, just what we have done."

> "run the test"

> "fix lint"

> "fix mise run lint"

> "can you run simplifier again and report it's findings"

> "yes please"

> "1+2"

### Corrections / pushback

> "CondenseSession ignores GetByAgentType errors and allows ag to be nil. This changes behavior for sessions/checkpoints whose AgentType is empty or the backwards-compatible \"Agent\" value: token usage will now always be nil because agent.CalculateTokenUsage short-circuits on a nil agent."

> "the command string send to posthog only contains the last command of cobra. if \"entire session list\" is sending \"list\" it should send \"entire session list\""

> "All good, but, I would replace ENTIRE_TELEMETRY_OPTOUT with the preferences stored at settings files"

> "eval this feedback:\nAll test cases use the --force flag, which bypasses the interactive confirmation prompt."

> "😭\n\nso basically we'd move git_operations into it's own package, and move any git specific things from strategy/ into that package as well?"
