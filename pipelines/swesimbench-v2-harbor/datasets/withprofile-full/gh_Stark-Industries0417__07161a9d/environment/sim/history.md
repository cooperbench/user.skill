[DEVELOPER]: Implement the following plan: # Consolidate logging to single file per worktree ## Context Currently `logging.Init(sessionID)` creates a separate log file per session at `.entire/logs/{session-id}.log`. This makes debugging harder because: - You can't `tail -f` before a session starts (file doesn't exist yet) - Concurrent sessions produce separate files you'd need to watch in parallel - Git hooks need to look up the session ID just to find the right log file ## Change Write all logs to a single fixed file: `.entire/logs/entire.log` The `session_id` slog attribute already appears on every log line, so filtering by session is still possible with `jq`. ## Files to modify ### 1. `cmd/entire/cli/logging/logger.go` - Change `Init()` to use fixed filename `"entire.log"` instead of `sessionID+".log"` (line 124) - Update doc comment (line 74-75) - Session ID validation is no longer needed for the file path, but keep it since it's used for the `currentSessionID` attribute — actually, `Init()` should still accept a session ID for the slog attribute. But the validation was only there to prevent path traversal in the filename. Since the filename is now fixed, the validation can be relaxed. However, keeping it is harmless and protects against misuse of `currentSessionID`. Leave it. […]

[AGENT]: I'll start by reading the files that need to be modified to understand the current code.

[AGENT]: Now I have a clear picture. Let me create the task list and implement the changes.

[AGENT]: Now let me implement the changes. Starting with the logger.go and hooks_git_cmd.go changes.

[AGENT]: Good, that diagnostic is pre-existing (it was there before my change). Now let me update `initHookLogging()`.

[AGENT]: Now I need to update `Init()` to accept empty session ID since `initHookLogging` can now pass one. Currently, `Init` validates the session ID and rejects empty strings. Let me check the validation.

[AGENT]: The session ID validation rejects empty strings. Since the filename is now fixed and the session ID is only used for the slog attribute, I should skip validation when the session ID is empty and just allow it through.

[AGENT]: Now update the tests.

[AGENT]: Now I'll rewrite the test file with all the changes: add `logFilePath` helper, update all path references to use `"entire.log"`, and update the `TestInit_RejectsInvalidSessionIDs` to reflect that empty is now allowed.

[AGENT]: Those diagnostics are pre-existing (they were there before too). Now update the docs.

[AGENT]: Now let me also check if the `validation` import is still needed in logger.go (it is, since we still validate non-empty session IDs). Let me also check if there are any other callers of `Init()` that might pass empty strings.

[AGENT]: Let me also check for any other callers in the broader codebase (non-test).

[AGENT]: Good - only two files reference `logging.Init()`. Let me also check if there are other callers outside of the logging package and hooks, perhaps in the hooks handlers for Claude Code.

[AGENT]: Let me check the test file too to make sure it doesn't need updating.

[AGENT]: That's just a comment, no code change needed. Now let me run verification.

[AGENT]: Two lint issues to fix. The `errcheck` one is from my change (I suppressed the error), and the `gosec` one is because I removed the `//nolint:gosec` comment (the path is no longer variable from user input, but the linter still flags it). Let me fix both.

[AGENT]: For the `errcheck` issue, I need to handle the error properly in `hooks_git_cmd.go`. The original code checked `err` - now I'm ignoring it. Since the error from `ReadCurrentSession` isn't actionable (we just want to try reading it), I should use a blank identifier but with a nolint, or just handle it explicitly.

[AGENT]: The cleanest fix is to explicitly handle the error but not bail out:

[AGENT]: Lint passes. Now let's run the tests.

[AGENT]: The logging package tests pass but there are 3 test failures in the `cli` package where other tests still expect the old session-ID-based log file paths. Let me fix those.

[AGENT]: Now let me fix the `TestInitHookLogging` test.

[AGENT]: Now let me also check the "empty" and "missing" session file test cases - since `initHookLogging` no longer bails when there's no session, these tests likely need updating too.

[AGENT]: The test structure looks fine. The "no session file" and "empty session file" cases just verify the cleanup function doesn't panic - that's still valid behavior. Let me run tests again.

[AGENT]: All tests pass. Let me mark the task complete.

[AGENT]: All done. Here's a summary of the changes: **`cmd/entire/cli/logging/logger.go`** - Changed log file from `<sessionID>.log` to fixed `entire.log` - Updated doc comment to reflect new path - Made empty session ID allowed (validation only runs for non-empty IDs, since the filename is no longer derived from it) **`cmd/entire/cli/logging/logger_test.go`** - Added `testLogFilePath(tmpDir)` helper to DRY up repeated path construction - Updated all 8 tests that referenced `sessionID+".log"` to use the helper - Changed `TestInit_RejectsInvalidSessionIDs` to expect empty session ID is now allowed **`cmd/entire/cli/hooks_git_cmd.go`** - `initHookLogging()` no longer bails when there's no session - it always initializes logging (with empty session ID if unknown) **`cmd/entire/cli/hooks_git_cmd_test.go`** - Updated expected log file path from `sessionID+".log"` to `"entire.log"` **`cmd/entire/cli/hook_registry_test.go`** - Updated 2 occurrences of `sessionID+".log"` to `"entire.log"` **`docs/architecture/logging.md`** - Updated file path description and jq examples to use `entire.log` - Added `tail -f` example (now possible since the file path is known upfront)