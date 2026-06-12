---
name: result-paste-relay
description: When a background task completes and the user receives a task-notification, they paste the raw output block verbatim as their next message — no intro, no commentary, no follow-up question.
---

# Result paste relay

The user relays completed task output by pasting it raw into the chat. They do not summarize, introduce, or annotate it. The paste is the message.

**Trigger**: A background task (E2E test agent, parallel subagent) completes and the user receives the output. They want the agent to act on it.

**Pattern**: Paste the full task-notification XML block or the structured test result markdown block verbatim. No lead-in sentence. No trailing comment. Sometimes only the key section (e.g., just the "Bugs/Issues Found" section, or just the "Exit code: 1" line).

**Examples**:

Minimal — just the headline:
> `**Exit code: 1** (due to 1 failure)`  
> ``  
> `**Overall: 24 passed, 1 failed, 26 total steps, 8m 27s runtime**`

Full — the bug list section only:
> `## Bugs and Issues Found ### 1. XSS via execCommand('insertHTML') (Low Severity) ...`

Full task notification block (XML):
> `<task-notification> <task-id>a0364520771d6ea36</task-id> ... </task-notification>`

**What this means**: The user expects the agent to read the pasted result and decide what to do next — they are not narrating, they are handing off data.
