---
name: ci-error-paste
description: When CI or a tool fails, user pastes the error verbatim in a fenced code block with minimal framing. Trigger: an agent-implemented change fails in GitHub Actions or a test runner.
---

# ci-error-paste

ravwojdyla does not debug CI failures himself before reporting them. When something breaks, he sends one framing sentence (`"ah, ok. when X happens, I get error in GH:"`) followed by a fenced code block with the raw error text. No diagnosis, no stack trace narration — just the output.

## Pattern

```
<one framing sentence>.

```
<raw error or log output>
```
```

## Verbatim example

> `"ah, ok. when labeled happens, I get error in GH:\n\n` ``` `\nAction failed with error: track_progress for pull_request events is only supported for actions: opened, synchronize, ready_for_review, reopened. Current action: labeled\n` ``` `"`

## Notes

- `"ah, ok."` is the standard opener for this pattern — mild acknowledgment of the situation.
- The error is always the full relevant text, not trimmed.
- No "can you fix this?" — the paste implies a fix is expected.
- If the agent's explanation contradicts what just happened in CI, user ignores the explanation and shows the evidence.
