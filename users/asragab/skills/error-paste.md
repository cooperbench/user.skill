---
name: error-paste
description: Raw CI/test output pasted verbatim as the entire message body, followed optionally by a 3–5 word plain-text label. Triggers when CI fails or a test run produces unexpected output that the user wants the agent to diagnose and fix.
---

Dump the full stdout/stderr block inline — no code fence, no reformatting, no "here is the error." Just the raw text starting from the command invocation line. If a brief label is needed to clarify intent, append it on a new line after the log.

**Pattern:**
```
Run uv run pytest tests/test_llm_judge.py -k "integration_google" -v
  uv run pytest …
  [full raw log]
Error: Process completed with exit code 5.

workflow integration tests not running
```

**Variations observed:**
- Long pytest traceback → `"test failures"` (two words, no period)
- Empty collection output → `"workflow integration tests not running"` (one sentence, no period)
- Evaluator score JSON → pasted inline with no label at all, treated as context
- Plugin validation error → pasted mid-sentence: `"Are they supposed to be there or not supposed to be there? What is the deal is the test doc contract wrong, creating a plugin can't be that difficult Error: Failed to install…"` (error text fused into prose without delimiter)

No analysis, no hypothesis about root cause. The agent is expected to figure it out.
