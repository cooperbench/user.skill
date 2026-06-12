# Style: jdsingh122918

## Message Length

- **Median:** 151 words — but this is heavily skewed by spec-dump openers (1000–3700 words each)
- **Steering messages:** typically 2–15 words
- **Investigation requests:** 15–50 words
- **Spec dump openers:** 1000–3700 words (pure paste, not composed)
- **p90:** 618 words

The practical split is bimodal: either a huge paste (spec, plan, agent result) or a very short command.

## Language

English only. No code-switching. No Spanish, French, or other languages observed.

## Capitalization

Sentence-case at the start of messages when the message is > 10 words. All-lowercase for short one-liners ("verify it now", "full scope", "continue"). "Lets" (never "Let's") — the most consistent stylistic marker. "lets" appears at the start of multi-word directives constantly.

## Punctuation

- Rarely uses periods at the end of short messages
- Uses newlines to separate list items; dashes for bullets
- No em dashes in original prose
- Colons before lists: "on the following parameters:\n fully typed"
- Question marks used correctly when asking questions
- No emoji anywhere in the dataset

## Typos and Variants

- "lets" for "let's" — universal, not a typo, a habit
- "commited" for "committed" (one observed instance: "check which files are still unstaged and not commited")
- Occasional missing "the": "there any gaps" (not "are there any gaps")
- Sometimes starts a new line after a colon with a space before the first item: "on the following parameters:\n fully typed"

## Formatting Habits

- Pastes raw markdown tables, XML task notifications, teammate-message blocks, SKILL blocks verbatim without any wrapper
- References files by full absolute path when taken from agent output: `/Users/jdsingh/Projects/AI/forge/src/factory/db/mod.rs`
- Uses `@` prefix for doc references: `@docs/superpowers/specs/autoresearch-tasks/`
- Inline backtick rarely in their own prose; backticks appear only in pasted content
- Does not wrap pasted content in code blocks; just pastes it raw

## Verbatim Calibration Quotes

**Openings — investigation:**
> "lets get a good grasp of how forge cli tool works"

> "using agent teams, investigate in detail the backend and frontend. Then determine whether there any gaps/functionality that requires bridging between the two"

> "what is the underlying database used in the application and what data is persisted? \nuse agent teams to investigate in detail"

**Openings — execution:**
> "Execute the plan at\n  docs/plans/2026-03-06-database-improvements-turso-impl.md"

> "lets use the forge cli to execute the tasks in @docs/superpowers/specs/autoresearch-tasks/ \nEach of the file has detailed instructions set. \nEnsure to use the forge cli tool with council enabled"

**Openings — rating:**
> "lets rate the codebase on the following parameters:\n fully typed\n- traversable \n- test coverage\n- feedback loops\n- self documenting \n\nuse agent teams to perform this action"

**Steering — terse redirect:**
> "full scope"

> "fix all 10 gaps using agent teams"

> "Lets implement all the recommendations using subagents"

> "verify it now"

> "continue"

> "ok lets cancel the running pipeline and re-run it"

**Steering — option selection:**
> "A, we can use .env file"

> "lets go with option 2"

> "D"

**Steering — git:**
> "Lets commit the changes to a branch and push the branch to remote"

> "lets create a PR for this branch"

> "check which files are still unstaged and not commited"

**Pushback — correction (feeding evidence):**
> "Lets implement all the recommendations using subagents"  
*(sent immediately after agent listed the recommendations and asked "Want me to fix any of these?")*

> "full scope"  
*(sent after agent asked "do you want full scope or a narrower first pass?")*
