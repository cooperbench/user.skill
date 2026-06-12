---
name: verbatim-test-paste
description: Yorrick's failure-reporting mode: pastes the full terminal output of a failing test run verbatim, with a brief imperative before and after. No diagnosis, no opinions.
---

When a test or command fails, yorrick does not paraphrase or summarize. He dumps the raw output and appends a one-line instruction. The agent is expected to read, diagnose, and fix — no hand-holding needed.

**Trigger**: a test suite fails, a shell command errors, or an integration test produces unexpected output.

**Behavior**: 
1. Opening line (optional, often omitted): brief context or just the path.
2. The raw terminal output, unmodified, including warnings and irrelevant env messages.
3. Closing instruction: terse imperative like "Read the source files, fix the bug, and save the file."

**Example** (used verbatim across 5 separate sessions — same demo, re-run each time):

```
Fix the failing tests in /tmp/workflow-demo/. Here are the test results:

warning: `VIRTUAL_ENV=/Users/yorrickjansen/.cache/uv/builds-v0/.tmpyGo0XM` does not match the project environment path `.venv` and will be ignored
============================= test session starts ==============================
platform darwin -- Python 3.14.2, pytest-8.0.2, pluggy-1.6.0
rootdir: /private/tmp/workflow-demo
configfile: pyproject.toml
collected 2 items

test_math.py .F

=================================== FAILURES ===================================
________________________________ test_multiply _________________________________

    def test_multiply():
>       assert multiply(3, 4) == 12
E       assert 7 == 12
E        +  where 7 = multiply(3, 4)

test_math.py:9: AssertionError
=========================== short test summary info ============================
FAILED test_math.py::test_multiply - assert 7 == 12
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
========================= 1 failed, 1 passed in 0.01s ==========================


Read the source files, fix the bug, and save the file.
```

He does not add "I think the issue is…" or "maybe check X." Pastes and moves on.
