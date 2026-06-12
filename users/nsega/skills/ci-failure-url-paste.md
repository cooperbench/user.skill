---
name: ci-failure-url-paste
description: Fires when GitHub Actions CI fails on nsega's PR. He pastes the PR URL and a terse delegation request, with no further context. No error logs, no description of the failure.
---

# CI Failure URL Paste

When CI breaks, nsega does not describe the failure or paste logs. He pastes the PR URL (or sometimes a specific Actions run URL) and a short imperative. The pattern is two lines: URL on line one, request on line two. He uses double spaces before the URL occasionally.

## Verbatim Example

```
The two GitHub Actions of CI failed  https://github.com/nsega/mcp-obsidian/pull/12
Please address them
```

## When to Fire

Fire this skill when playing nsega and the simulated state includes a CI failure on a PR. The agent is expected to fetch the URL and diagnose autonomously. nsega provides no additional context — this is the entire message. Preserve double spaces before the URL if it appears mid-sentence.
