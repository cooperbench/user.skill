# Preferences: adrientaudiere

## What triggers pushback (35.4% correction, 7.7% failure_report, 3.1% rejection)

- **Agent exceeds scope.** When the agent commits all changes when only specific files were implied, or modifies more than the stated target (e.g., roxygen block), user sends a narrow "only add X to Y" correction.
- **Agent gets the direction wrong.** Sorting ascending vs. descending, left vs. right sides of a plot — corrects flatly with "No, I want the inverse," or repeats the goal with slightly more detail until it lands.
- **Agent summarizes what the user did.** When the agent attributes an action to itself that the user actually performed, user replies "No, I did."
- **Agent offers options instead of acting.** When the agent asks "which files should I commit?", user replies "all the changes" — does not want to make decisions the agent should infer.
- **Failure reports are paste-only.** User pastes the error verbatim with no commentary. Expects agent to diagnose and fix.

## What satisfies

- Brief "yes" or "Yes !" when the agent's proposed fix is correct.
- Runs `/r-check` or `/r-test` after a code session as implicit acceptance.
- Commits with "commit this" after a satisfactory result — this is the sign-off.
- Explicitly approves "mechanical and safe" changes: `"Yes, tackle the suggestion with clearly mechanical and safe ones."`

## Workflow habits

- **Custom command-driven.** Uses `/r-check` (style + document + R CMD check), `/r-build` (build pkgdown site + tarball + lint), `/r-test` (test suite + coverage) as session openers and closers. These commands embed extensive instructions; the user just triggers them.
- **Approval-gated changes.** Commands include "Never modify code without explicit user approval" and "ask the user 'Should I apply this fix?' before making any change." User expects every proposed fix to be shown as a diff before application.
- **TDD when adding features.** Explicitly: "So lets create the test file in a new testthat file and after we will improve the code to pass the test (sort of test-driven development)."
- **Iterates rapidly, interrupts freely.** Sends `[Request interrupted by user for tool use]` multiple times per session. Does not wait for completion if the direction is wrong.
- **Commits frequently.** "commit this" appears multiple times per session — one logical change per commit rather than batching.
- **Quality tracking.** Monitors codefactor grade, codecov percentage, lint issue count, and R CMD check NOTEs. These are first-class outcomes, not side-effects.

## Tool/stack preferences

- **R ecosystem:** devtools, testthat, lintr, pkgdown, rcmdcheck, covr, air (formatter), magrittr/native pipe
- **Package CI:** Codecov (MiscMetabar token), codefactor, R CMD check `--as-cran`
- **Claude Code slash commands** as the primary workflow automation layer
- **Suppresses `return_linter`** rule explicitly — prefers not to enforce return value style
- **Does not want `T`/`F` in code** — strict `TRUE`/`FALSE`
- **Avoids magrittr `.` placeholder** — migrating to native pipe + anonymous functions
