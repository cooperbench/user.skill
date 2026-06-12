---
name: task-notification-relay
description: How Mathews-Tom provides mid-session context — by pasting raw <task-notification> XML verbatim as his prompt, often appended with "Read the output file to retrieve the result: REDACTED.output". Trigger when a background agent has completed and the user wants to signal that completion.
---

# Task Notification Relay

Mid-session, Mathews-Tom does not summarize task results or write a narrative update. Instead, he pastes the raw `<task-notification>` XML verbatim as his entire prompt. When the notification references an output file, he appends "Read the output file to retrieve the result: REDACTED.output".

This is how he signals: "a background task completed — act on what's in here." He expects the agent to read the notification, extract relevant info, and continue without prompting.

Notifications come in two forms:
1. **Brief**: just status, summary, output-file pointer
2. **Full result embedded**: includes a multi-paragraph `<result>` block with the sub-agent's full output, then "Full transcript available at: REDACTED.output"

He pastes these even when the result is clearly a pass (exit code 0), as a log-keeping habit.

## Examples

**Example 1** (brief form):
```
<task-notification>
<task-id>b079152</task-id>
<output-file>REDACTED.output</output-file>
<status>completed</status>
<summary>Background command "Validate microattention.py runs successfully" completed (exit code 0)</summary>
</task-notification>
Read the output file to retrieve the result: REDACTED.output
```

**Example 2** (full result embedded, truncated):
```
<task-notification> <task-id>a1dfb23</task-id> <status>completed</status> <summary>Agent "Implement microattention.py" completed</summary> <result>Comment density is 40.7% -- right at the 30-40% target. All criteria met: - All 5 variants implemented as standalone functions - All outputs numerically valid (no NaN, no overflow) - Cosine similarity ordering correct: MHA=1.0 > GQA > MQA > Sliding Window > Vanilla - FLOP/memory tradeoffs correctly shown in table - Runtime: ~93ms (well under 1 minute) - 349 lines ...</result> <usage>total_tokens: 96155 tool_uses: 20 duration_ms: 445219</usage> </task-notification> Full transcript available at: REDACTED.output
```

**Example 3** (sub-agent requesting permissions — Mathews-Tom relays even failure/blocked states):
```
<task-notification> <task-id>a201b8d</task-id> <status>completed</status> <summary>Agent "Implement microembedding.py" completed</summary> <result>I need Bash permission to run the script. The user explicitly requested that I run the script and report the results as part of the task requirements...</result> <usage>total_tokens: 58098 tool_uses: 7 duration_ms: 111681</usage> </task-notification>
Full transcript available at: REDACTED.output
```
