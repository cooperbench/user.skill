---
name: error-paste-terse
description: User pastes raw shell output verbatim then adds a single hypothesis or directive. Triggered whenever a command produces unexpected output or an error.
---

When something breaks, dipasqualew does not describe the error in their own words. They paste the terminal output exactly as it appears — `$` prompt, full stderr, truncated output — then add at most one sentence of commentary or a one-line hypothesis.

The commentary is tentative ("I think", "I am pretty sure") even when their actual analysis is precise. They are diagnosing, not complaining.

## Examples

```
$ python3 plugins/vibereq/scripts/run-review.py "code-review"
Running reviewer 'code-review' for PR #1...
Could not extract JSON from reviewer output
Output:

I think it is not waiting for something?
```

```
$ python3 plugins/vibereq/scripts/run-review.py "code-review"
Running reviewer 'code-review' for PR #1...
Could not extract JSON from reviewer output
Output:

I am pretty sure it is not awaiting for "Running reviewer 'code-review' for PR #1...",

Can you check what's going on?
```

```
❯ /code-review ci
  ⎿  Error: Bash command failed for pattern "!python3
     $CLAUDE_PLUGIN_ROOT/scripts/get-intents.py": ...
     can't open file '/scripts/get-intents.py': [Errno 2] No such file or directory
```
(no commentary — the error speaks for itself)
