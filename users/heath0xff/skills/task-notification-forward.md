---
name: task-notification-forward
description: >
  Trigger: a background agent finishes and emits a <task-notification> XML block in the session.
  heath forwards it verbatim as his next message without any wrapper commentary.
---

When a background agent completes, heath pastes the entire `<task-notification>` XML block
(including task-id, output-file path, status, summary, and full result) as his next "message"
with no preamble or reaction. This is how he feeds agent output back into the conversation.

The result block inside the notification is often truncated at 1932+ words and contains the agent's
findings in full markdown. Heath does not summarize or react — he forwards the raw block.

This pattern constitutes ~30% of mid-session prompts in the training data.

## Verbatim example

> `<task-notification> <task-id>afc2d2d1adaea0eea</task-id> <tool-use-id>toolu_01MGrMGes8qGTCdrPa3wPPeQ</tool-use-id> <output-file>/private/tmp/claude-501/-Users-heath-code-hChat/9a07290e-a8a5-4d69-9a46-2088f7c7d18b/tasks/afc2d2d1adaea0eea.output</output-file> <status>completed</status> <summary>Agent "Architecture and design review" completed</summary> <result>Perfect! Now I have a comprehensive view. Let me compile my findings into a detailed architecture review. ## Architecture and Design Review: hChat ...`

When role-playing heath, if the session context includes a completed background task, emit the
`<task-notification>` block exactly as it would appear — do not paraphrase it.
