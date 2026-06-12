---
name: evisdren-preferences
description: What evisdren corrects, rejects, approves, and their workflow habits.
metadata:
  type: user
---

# Preferences: evisdren

## Pushback Distribution

- **Correction: 57.1%** — dominant mode. Agent's approach diverged from intent.
- **Non-pushback: 34.9%** — agent got it right; next command follows immediately.
- **Failure report: 7.9%** — manual test revealed a bug; pastes terminal evidence.

## What They Correct or Reject

- **Too-synthetic test setups**: Rejects lightweight fake repos; insists on cloning real repos (e.g., `entireio/cli`) for benchmarks.
- **Wrong implementation approach**: If agent picks a complex path when a simpler one exists, they say so directly and redirect. E.g., "Let's make an update here... I remember we discussed having an 'always' option on the commit prompt itself — did that get dropped for a reason?"
- **Wrong settings file target**: Catches when the agent writes to `settings.local.json` instead of `settings.json` or vice versa.
- **Hardcoded strings over constants**: Calls out `"always"` instead of `settings.CommitLinkingAlways` immediately.
- **Benchmark design flaws**: Corrects accumulating-branch benchmarks that degrade over iterations; insists on fresh `BenchRepo` per iteration.
- **Non-deterministic behavior**: Flags map iteration order in agent detection as a bug.
- **Incomplete PR comment responses**: If agent says "Done" but missed a point from a reviewer comment, they relay the missed feedback.
- **Lint violations**: Relays linter errors verbatim and asks the agent to fix them.
- **Flaky test patterns**: Rejects global mutable state for test mocks; wants proper injection.

## What Satisfies Them

- Short "Done." or commit SHA after completing a task — no extra explanation needed.
- When agent correctly interprets a terse redirect without asking clarifying questions.
- When agent addresses all numbered points in a spec in order.
- When agent self-identifies a root cause clearly before fixing it.

## Workflow Habits

- **Pre-written specs**: Opens complex sessions with a detailed markdown plan. Does NOT discover the design collaboratively — comes in with it.
- **Manual testing after every significant change**: Runs `entire enable`, makes commits, checks terminal output, checks settings JSON files on disk.
- **Interrupt-driven**: Frequently interrupts the agent mid-execution (`[Request interrupted by user for tool use]`) — does not wait for the agent to finish before redirecting.
- **Numbered-list task batching**: Accepts a list of suggestions from agent then scopes: "let's start with implementing suggestions 1-4 first", "okay now let's do 6,7,8,10".
- **External reviewer integration**: Uses Copilot and Cursor for PR reviews, then relays their comments verbatim to Claude Code for implementation.
- **Commit cadence**: Commits after each logical unit of work; uses short commands ("commit and push this", "commit and push", "push it to github").
- **Rebase workflow**: Prefers rebasing onto main before pushing; uses `--force-with-lease`.
- **Mise.toml for tasks**: All bench/test tasks live in `mise.toml`; asks for new tasks to be added there.
- **No test-first discipline**: Tests and benchmarks are added after (or alongside) implementation, not before. Often adds them in a separate session or follow-up prompt.
- **Does NOT ask for explanations by default**: When they want to understand something, they ask explicitly ("give me an overview", "does that read the entire git repo into memory first"). Otherwise they just want the change done.
- **Reads diffs**: Does not need the agent to summarize what changed; they read the output themselves.
