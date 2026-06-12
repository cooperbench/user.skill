---
name: ci-failure-report
description: "Trigger: A CI job fails on GitHub Actions. FSM1 drops the direct Actions run URL plus a one-sentence observation about what broke, then expects the agent to diagnose and fix."
---

# Skill: CI Failure Report

When something breaks in CI, FSM1 links directly to the failing job URL and states what seems wrong. He does NOT paste log output manually — the URL is the reference. He expects the agent to fetch and analyze it.

His diagnosis is usually partially correct and serves as a starting hypothesis. He may add a suggested direction (e.g., "should this not just be a part of the @cipherbox/api-client extrafiles rather than the api?").

## Examples

Post-release targets job failing:
```
https://github.com/FSM1/cipher-box/actions/runs/23829451708/job/69459555121 the post-release targets job is failing for some reason.
```

Conventional commits parsing issue on merge commit:
```
https://github.com/FSM1/cipher-box/actions/runs/23828669736/job/69457249495?pr=429 seems like the merge commit is causing some issues for the conventional commits parsing - these commits should be skipped in analysis
```

Cascading issue with suggested fix direction:
```
https://github.com/FSM1/cipher-box/actions/runs/23831402584/job/69465572026 that just broke release please. should this not just be a part of the @cipherbox/api-client extrafiles rather than the api? then we avoid the pathing issue entirely.
```

API spec check still failing after a supposed fix:
```
https://github.com/FSM1/cipher-box/actions/runs/23851892351 verify api spec is still failing on the release please branch
```

## Pattern

URL first, observation second, no preamble. If he has a hypothesis about the fix, it comes as a suggestion ("should this not..."), not a directive. Expects agent to take it from there.
