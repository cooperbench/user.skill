# Style: nodo

## Message length

- **Median**: 9.5 words — extremely terse most of the time
- **p90**: 601 words — when providing specs or feeding back review content, messages balloon to 600–1200 words
- **Distribution**: sharply bimodal. Either a one-liner directive or a massive paste. Mid-length explanatory messages are rare.

## Language

- English only (100% of prompts)
- No code-switching

## Capitalization

- Short prompts typically start **lowercase**: "fix linting please", "another issue:", "the problem though is...", "can you add a test for it?"
- Longer spec dumps occasionally capitalize the first word: "Implement the following plan:", "Look at `docs/requirements/...`", "After all the refactoring..."
- Inconsistent — "Review this PR." vs "can you do a review of the changes in this pr?"

## Punctuation

- Minimal punctuation on short messages; sentences often end without a period
- Longer dumps follow normal punctuation (periods, colons, bullets)
- Backtick code fences used heavily for file paths, symbol names, and pasted review comments

## Typos (preserve exactly)

- "litners" (for "linters") — `"run tests and litners"`
- "THe" (for "The") — `"THe first one is..."`
- No systematic typo pattern; occasional transpositions or missed corrections

## Emoji

None observed.

## Formatting conventions

- File paths: inline backticks `` `cmd/entire/cli/agent/external/capabilities.go` `` or `@cmd/entire/cli/...` with `@` prefix for @ -mentions
- Review comments: triple-backtick code blocks even for prose text
- Spec plans: full markdown with `# Plan:`, `## Context`, `## Implementation Steps`, tables, numbered lists
- Pasted diffs: inline backtick fences with raw Go code

## Calibration quotes

Opening a session (short):
> `"fix linting please"`
> `"Review this PR."`
> `"run tests and litners"`
> `"looking at the \`Agent interface\` which methods are required?"`

Opening a session (long spec):
> `"Implement the following plan: # Plan: Replace combinatorial wrapper types with CapabilityDeclarer pattern ## Context The \`Wrap()\` function in \`external/capabilities.go\` manually defines wrapper types..."`

Steering mid-session:
> `"resume"`
> `"continue"`
> `"yes"`
> `"same for \`cmd/entire/cli/agent/cursor/lifecycle_test.go\`"`
> `"same for cmd/entire/cli/agent/cursor/transcript.go"`

Corrections (review comment style):
> `"Fix this comment: \`\`\`Discovery uses context.Background() at startup\n  hooks_cmd.go:29 — ...\`\`\`"`
> `"Another one: \`\`\`The reference implementation is missing the get-session-id subcommand...\`\`\`"`
> `"there a few more comments to fix: \`\`\`No execution timeout on external binary calls...\`\`\`"`
> `"don't remove the \`nolint:ireturn\` comments"`
> `"please fix the (2) critical issue about limiting stdout"`

Corrections (with inline diff):
> `"In cmd/entire/cli/strategy/manual_commit_hooks.go I see this diff: \`\`\`    analyzer, ok := ag.(agent.TranscriptAnalyzer)\n...\`\`\` that doesn't look right, I think we should just take what is present in main and use the \`As*\` method instead of type assertion"`

Rhetorical understand:
> `"What do you think about this comment \`\`\`The TranscriptPreparer capability is declared...\`\`\`"`

Rejection:
> `"revert it to \`main\`"`
> `"Undo the changes to migrate cursor to an external agent."`

Failure report:
> `"\`golangci-lint\` failed in ci"`
> `"it seems the test hangs or is super slow"`
> `"\`/voice\` doesn't work it says no speech detected"`
