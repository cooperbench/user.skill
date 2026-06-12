---
name: task-notification-passthrough
description: How baotoq feeds subagent completions back to the orchestrator — by pasting <task-notification> blocks verbatim as his next message. Trigger when a subagent has just completed and the session needs to continue.
---

baotoq uses a Paperclip multi-agent platform where subagents run asynchronously. When a subagent completes, its result arrives as a `<task-notification>` block. baotoq's "response" to this is to paste the notification verbatim back into the conversation so the orchestrating agent can pick it up and continue the workflow.

**Example (short form — quota exhausted):**
```
<task-notification>
<task-id>ae6a84f7ddd958f95</task-id>
<tool-use-id>toolu_01TSE3WTRG9QGPZTi11PjnsP</tool-use-id>
<status>completed</status>
<summary>Agent "Execute plan 25.1-03 catalog" completed</summary>
<result>You're out of extra usage · resets 3am (Asia/Saigon)</result>
<usage><total_tokens>79</total_tokens><tool_uses>31</tool_uses><duration_ms>109697</duration_ms></usage>
</task-notification>
Full transcript available at: /private/tmp/claude-501/-Users-baotoq-Work-micro-commerce/tasks/ae6a84f7ddd958f95.output
```

**Example (full form — successful completion):**
```
<task-notification>
<task-id>a0cd42c5b1981beb1</task-id>
<tool-use-id>toolu_01Uom163434q5ND9BqJZFidL</tool-use-id>
<status>completed</status>
<summary>Agent "Execute plan 25.1-05 cart" completed</summary>
<result>## PLAN COMPLETE

**Plan:** 25.1-05
**Tasks:** 2/2
...
</result>
<usage><total_tokens>89937</total_tokens><tool_uses>71</tool_uses><duration_ms>406371</duration_ms></usage>
</task-notification>
Full transcript available at: /private/tmp/claude-501/-Users-baotoq-Work-micro-commerce/tasks/a0cd42c5b1981beb1.output
```

When role-playing this behavior, produce the `<task-notification>` XML block with plausible task-id (hex string), tool-use-id (`toolu_` prefix), status, summary, and result. Include `Full transcript available at:` line. No text before or after the block.

Multiple notifications may arrive in the same session window when parallel subagents complete at similar times.
