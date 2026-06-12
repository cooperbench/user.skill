---
name: task-notification-forward
description: How tarasyarema forwards completed sub-agent task-notification XML mid-session, with no added commentary
---

# Skill: Task Notification Forward

When a background sub-agent completes, Taras pastes the raw `<task-notification>` XML block directly as his next message. He rarely adds commentary — the notification output speaks for itself. If the result reveals a failure, the notification IS the correction.

## Examples

**Completion forward (no added text):**
```
<task-notification>
<task-id>bd30mk687</task-id>
<tool-use-id>toolu_0176UH8JtqtHKEU7G3j3uTFW</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-taras-Documents-code-agent-swarm/tasks/bd30mk687.output</output-file>
<status>failed</status>
<summary>Background command "Build Docker image from updated Dockerfile" failed with exit code 1</summary>
</task-notification>
Read the output file to retrieve the result: /private/tmp/.../bd30mk687.output
```

**Background completion with follow-up read instruction:**
```
<task-notification>
<task-id>by1v8mwb3</task-id>
...
<status>completed</status>
<summary>Background command "Start API server" completed (exit code 0)</summary>
</task-notification>
Read the output file to retrieve the result: /private/tmp/.../by1v8mwb3.output
```

**Full sub-agent result forwarded as correction context:**
The full `<result>...</result>` block from a review agent becomes the pushback when it contains FAIL items — Taras pastes it wholesale, then either stays silent or adds a one-liner like "the tests should be based on what was done in this PR! check rpi files".

## Key signals

- Verbatim XML paste, no rewording
- "Read the output file to retrieve the result: <path>" appended exactly as the system generated it
- File paths use `/private/tmp/claude-501/-Users-taras-...` prefix (macOS temp dir for his machine)
- He pastes these even for non-pushback situations — it's how he provides context, not just how he signals failure
