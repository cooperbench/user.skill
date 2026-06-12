---
name: log-dump-debug
description: How Pavel401 reports runtime failures — pastes the full raw log or JSON output verbatim with no summary or preamble, expects the agent to diagnose from the wall of text.
---

# log-dump-debug

When something breaks at runtime, Pavel401 does not narrate the error. He pastes the raw stdout, log lines, JSON, or curl output directly into the message with no framing text. The paste IS the bug report.

The agent must read the raw content, identify the issue, and respond with a diagnosis + fix — not ask clarifying questions.

## Triggers

- Something stopped working ("delete repo is not working")
- He ran a command and the output looks wrong
- A webhook fired and behaved unexpectedly
- Stats endpoint returned garbage values

## Examples

**Example 1** — raw application log dump (opening message, zero preamble):
```
Application startup complete. Logfire project URL: https://logfire-us.pydantic.dev/pavel401/nomaibackend 2026-02-17 11:37:54,546 - api.routers.webhook - INFO - Received GitHub webhook: issue_comment 2026-02-17 11:37:54,546 - api.routers.webhook - INFO - PR review triggered: Pavel401/BugViper#5 ...
```
(followed by thousands of words of log output and diff context — no introduction)

**Example 2** — symptom + wrong data inline:
```
I don't think the 99 files
624 functions
67 classes
780,431,213 lines
typescript
unknown
python stats are correct
```

**Example 3** — symptom statement, minimal words:
```
look at the api.log it has so many issues
```

**Example 4** — raw JSON paste with symptom:
```
DELETE CLICK {
    "id": null,
    "name": "BugViper",
    "owner": "Pavel401",
    ...
    "file_count": 99
}
```

**Example 5** — after agent fix, still wrong:
```
But now the lines is wrong {
    "repository_id": "Pavel401/FinanceBro",
    "statistics": {
        "files": 12,
        ...
        "lines": 307176,
        ...
    }
}
```
