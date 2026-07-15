> DEVELOPER

can you take a look at https://github.com/entireio/git-sync/issues/63

> AGENT

Now I understand the issue. Let me check how things invoke git in other places to understand the convention:

> AGENT

The bug is clear. In `internal/auth/auth.go:70`, when `git credential fill` runs and the helper has no credentials, git falls back to prompting the user interactively. Setting `GIT_TERMINAL_PROMPT=0` makes git fail instead, so we fall back to anonymous access. Let me check what env handling looks like for similar invocations:

> AGENT

Now let me apply the fix:

> AGENT

Now also remove the now-stale comment in `syncer.go` about the credential fill prompting:

> AGENT

Let me check what testing patterns already exist and verify the build still works:

> AGENT

Now let me add a regression test that exercises the actual command against a clean git env, so it would catch removal of the env var:

> AGENT

Test passes. Let me also verify the test actually fails without the fix, to confirm it's a real regression test:

> AGENT

The test passes in both cases (the test environment doesn't have a TTY so git fails regardless). Let me strengthen the test by actually verifying the env var is set on the command. I'll restructure slightly:

> AGENT

Now `exec` is no longer used in the test. Let me remove the import and verify everything passes:

> AGENT

All clean. Let me also run a broader test to make sure I didn't break anything:

> AGENT

All tests pass. Here's the summary: **Bug**: When `git-sync sync` is run against a public source repo (e.g. `https://gitlab.baylibre.com/...`), it would interactively prompt for username/password on a host the user had never authenticated against. **Root cause** (`internal/auth/auth.go:69`): `git credential fill` falls back to an interactive terminal prompt on `/dev/tty` when no configured helper has credentials. `git-sync` is non-interactive, so this prompt shouldn't happen — anonymous access should be attempted instead. **Fix**: Set `GIT_TERMINAL_PROMPT=0` on the `git credential fill` invocation. With this, when no helper has credentials, git exits non-zero, our existing code treats that as "no credentials found", and we proceed anonymously. I also extracted `newCredentialFillCmd` so the env-var contract is unit-testable (`TestCredentialFillCmdDisablesTerminalPrompt`). Want me to open a PR for this against issue #63?