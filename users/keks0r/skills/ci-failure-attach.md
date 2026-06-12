---
name: ci-failure-attach
description: How KeKs0r reports CI or test failures — attaches the log file and sends a one-
  line prompt. Trigger after an agent ships a PR and CI comes back red.
---

# CI failure attach

When CI or a background task fails, KeKs0r attaches the log output as a file and sends a
minimal prose instruction. He does not diagnose the failure himself — that's the agent's job.

## Examples

> `Fix the failing CI actions. I've attached the failure logs.`
*(with `verify_65344981914.log` attached)*

> `check why the verify job on main failed, is it a flaky test, or what is the problem? can you inspect what the issue is, and potentially fix it. We cant have flaky tests, since this will be blocking prod deployments`

> `yes but it failed on CI, why?`

> `did you commit and push your fixes to fix CI?`

> `why is CI failing on this repository on main?`

> `investigate why the release action on CI is failing on main`

## Pasted stack traces (direct debug, no attachment)

When debugging locally he pastes the full terminal output verbatim with a single setup line:

> `I still have trouble deleting an organization\\\n$ doppler run --project rudel...`
*(followed by 30+ lines of raw log)*

> `when people are installing the rudel via npm they are getting this error:\n\`\`\`\nnpm error code EUNSUPPORTEDPROTOCOL\n...\`\`\``

## Characteristics

- Setup sentence is one line: "Fix the failing CI actions." or "check why X is failing."
- No diagnosis hypothesis offered — he wants the agent to investigate.
- Implicit expectation: agent fixes AND commits AND re-triggers, without being asked.
- If the agent asks "should I fix it?" he will reply with a one-word affirmative.
