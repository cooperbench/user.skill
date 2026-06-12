---
name: log-paste-debug
description: Trigger when Soph reports a failure by pasting raw logs, error output, or test failures with minimal or no commentary, expecting the agent to diagnose and fix.
---

# Log paste debug

When something breaks, Soph pastes the output directly. The preamble is short — a sentence or two setting context — followed by the raw artifact. No summary, no analysis. The agent is expected to read the log and identify the issue.

**Patterns:**

- Go compiler errors: paste the exact error output, then "can you take a look?" or "can you fix?"
- CLI output: paste what they saw in the terminal
- JSONL log lines: paste structured log entries from `.entire/logs/`
- Test failures: paste the `=== RUN` output block
- CI action failures: paste the action log block

**Example 1 (compiler error):**
> "when running `mise run test:ci` I get these errors:\n\ncmd/entire/cli/integration_test/last_checkpoint_id_test.go:76:31: invalid operation: state.LastCheckpointID != firstCheckpointID (mismatched types id.CheckpointID and string)…"

**Example 2 (CLI failure with user context):**
> "I'm currently getting this error in /Users/soph/Work/entire/devenv/entire.io, and there are no uncommited changes:\n\n❯ entire resume batch-supabase-webhook-operations\nyou have uncommitted changes. Please commit or stash them first"

**Example 3 (customer log paste):**
> "I have a customer using the cli (this repo) with opencode, the installation looks right, he sees this log in .entire/logs:\n\n{\"time\":\"2026-02-26T10:59:00.979416+01:00\",\"level\":\"INFO\",\"msg\":\"turn-start\"…}"

**Example 4 (E2E test failure):**
> "I think this is the last failure: === NAME TestE2E_Scenario3_MultipleGranularCommits…"

After pasting, Soph typically ends with a short question ("what could go wrong?", "can you check?") or nothing at all.
