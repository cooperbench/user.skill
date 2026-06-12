---
name: log-attach-debug
description: How marcus-sa reports failures — attaches CI log files and says "Fix the failing CI actions." Trigger: CI failure, test failure, or runtime error.
---

# Skill: log-attach-debug

When CI breaks or acceptance tests fail, Marcus does not describe the error. He attaches the log file and writes a short directive. He expects the agent to read the log, identify the root cause, and fix it — without him explaining anything.

## Pattern

With attached log file:
> `Fix the failing CI actions. I've attached the failure logs.`

With pasted stack trace (no commentary):
```
Run bun test --concurrent --timeout=180000 --env-file=.env tests/acceptance/learning-library/
bun test v1.3.10 (30e609e0)
...
2 tests failed:
(fail) Milestone 3: Full Learning Lifecycle > deactivated learning disappears from active filtered views [120001.27ms]
  ^ this test timed out after 120000ms.
```

Checking status:
> `check the status of the agents. i dont think they're running...`

Noting a runtime error:
> `when I go to tool registry page it fails with "undefined is not an object (evaluating 'mcpServers.length')"`

> `gh runs are still failing`

> `acceptance tests are still failing. check gh pr runs`

## Notes

- He never diagnoses before the agent does — he provides raw evidence and delegates.
- Follow-up corrections on debugging are pointed: "THE EMBEDDING ENV VARS ARE NO LONGER USED!!!!" when the agent proposes a fix using deprecated config.
- When the agent's fix doesn't work, he writes `still fails:` followed by the new stack trace.
