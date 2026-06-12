---
name: failure-paste-debug
description: >
  How oddessentials reports a failure — CI, local test run, or hook block. Trigger:
  any CI failure, pre-commit/pre-push block, pytest error, or unexpected behavior.
  Accounts for the 6.4% failure_report pushback distribution.
---

When something breaks, oddessentials pastes the raw output with minimal framing. He does not paraphrase the error — he copies the terminal output, CI run URL, or task-notification XML directly. His framing is usually one sentence or a URL.

**Patterns:**

1. **CI failure → URL + one-line question:**
> `https://github.com/oddessentials/ado-git-repo-insights/actions/runs/23574696309/job/68644515503?pr=199  Carefully review why this check failed in CI and we didn't catch it locally first. /plan a fix that I can review thoroughly.`

2. **Hook block → paste raw terminal output:**
> `Can you explain this? [pre-push] push blocked: CRLF line endings found`
> `[pre-push] Fix: run \`git add --renormalize .\` after checking .gitattributes`
> `error: failed to push some refs to 'https://github.com/oddessentials/ado-git-repo-insights.git'`

3. **pytest failure → paste full session header + error:**
> `PS E:\projects\ado-git-repo-insights> python scripts/run_pytest.py tests/unit/test_version_resolution.py -v 2>&1`
> *(full pytest session output follows, unmodified)*

4. **Task-notification XML → paste verbatim:**
> `<task-notification><task-id>b5p3lel6y</task-id>...<status>failed</status><summary>Background command "Run Python tests from repo root" failed with exit code 1</summary></task-notification>`

5. **One-word/one-phrase after pasting:**
> `"mypy failed in ci"`
> `"fix it"`

He almost never writes a summary of what the error means — the raw output is the message. When he does add commentary it is a direct question: "Carefully review why..." or "Can you explain this?"
