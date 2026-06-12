---
name: raw-output-failure
description: How alishakawaguchi reports failures — pastes raw terminal/lint/CI output with zero or minimal commentary. Trigger when a build fails, lint fails, or a CI run fails.
---

# raw-output-failure

alishakawaguchi does not explain failures. They paste the raw output and expect the agent to figure out what's wrong. This is the dominant failure_report style (5.1% of prompts fall into this category, but the pattern appears within correction prompts too).

## Behavior pattern

- No "I got this error" or "this failed:" preamble
- Raw terminal output starts immediately, possibly as the entire message
- For CI failures: pastes a GitHub Actions run URL: "ran it and it failed please debug and fix https://github.com/..."
- For lint: pastes the raw golangci-lint output verbatim
- For test failures: pastes the test runner output (go test -v output)
- Short suffix sometimes added: "and its still not printing out", "please debug and fix"
- Can attach a screenshot `[Image: image/png]` instead of text when the failure is visual

## Examples

**Lint failure (entire message is the lint output):**
```
golangci-lint run
cmd/entire/cli/agent/factoryaidroid/factoryaidroid.go:1: : # github.com/entireio/cli/cmd/entire/cli/agent/factoryaidroid [github.com/entireio/cli/cmd/entire/cli/agent/factoryaidroid.test]
cmd/entire/cli/agent/factoryaidroid/factoryaidroid.go:41:44: undefined: agent.AgentName
cmd/entire/cli/agent/factoryaidroid/factoryaidroid.go:44:44: undefined: agent.AgentType (typecheck)
// Package factoryaidroid implements the Agent interface for Factory AI Droid.
1 issues:
* typecheck: 1
```

**CI failure with URL:**
```
ran it and it failed please debug and fix https://github.com/entireio/cli/actions/runs/23354978743
```

**Visual failure with screenshot:**
```
I don't see ability to run it
[Image: image/png]
```

**Warning paste (from `entire` CLI output, no explanation):**
```
seeing this warning. explain whats going on. the rewind of the code seemed to work

~/Projects/test-repos/factoryai-droid (master) $ entire explain
Branch: master
Checkpoints: 3
...
Warning: failed to restore session transcript: failed to get agent session directory: not implemented
```
