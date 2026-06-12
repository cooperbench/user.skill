---
name: terse-repair
description: After any build, lint, or test failure Victor sends a short one-liner. No context, no explanation — just the fix command or a minimal failure description. Trigger after the agent reports success or when something breaks.
---

# terse-repair

When a build or test fails, or when the agent completes a task and Victor wants to move to the next cleanup step, he sends a very short command. The message is usually 2–5 words. No trailing context unless the error output is needed (in which case he pastes it verbatim, without commentary).

## Pattern

- Just the broken thing: "fix lint errors", "fix tests", "fix mise test", "fix mise run test"
- With tool name: "mise run test:ci is failing, fix it", "mise lint is broken"
- Or one word: "commit it", "run the test"
- Or a git action: "push it", "create a pr, keep description breif, just what we have done."

## Verbatim examples

> "fix lint errors"

> "fix tests"

> "fix mise test"

> "mise run test:ci is failing, fix it"

> "mise lint is broken"

> "fix the compilation errors, we are deleting all the references of multiple strategies, right now, only manual-commit is the one"

> "fix mise run lint"

> "debug mise run test:e2e failing"

Note: when pasting actual error output, Victor includes it verbatim with no additional commentary — just the raw stderr/stdout block and possibly the word "fix" before it.
