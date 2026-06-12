---
name: context-paste-as-message
description: >
  Trigger: user's next message is raw XML task notification, teammate-message, subagent
  result text, SKILL block, or agent output — pasted verbatim with no wrapping or
  commentary. Used to inject evidence or continue from a subagent result.
---

## Behavior

A large fraction of mid-session messages are not instructions but raw pastes of:

1. **`<task-notification>` XML** — output of a completed background agent task, including the summary and result text
2. **`<teammate-message>` XML** — output from a named teammate/subagent with a summary attribute
3. **SKILL blocks** — `## SKILL: TESTING STRATEGY`, `## SKILL: AGENT REVIEW`, etc., loaded via MCP and passed as context
4. **Markdown-formatted subagent findings** — audit tables, issue lists, code snippets from review agents
5. **Plan sections** — a specific section of a plan document pasted to direct the next implementation step

The user adds **no framing** before or after the paste. The paste itself is the message. The agent is expected to understand that this is context to act on, and that the logical continuation is to implement fixes or continue from where the agent left off.

Sometimes the paste is a correction of the agent's previous plan section (e.g., pasting the corrected plan text instead of describing what to fix).

## Examples

**User message (entire message):**
```
<task-notification> <task-id>a810d3e9589990b24</task-id> ... <status>completed</status> <summary>Agent "Hunt silent failures in PR" completed</summary> <result>Now I have a thorough understanding... ## Summary Table | # | Severity | Location | Issue | ...</result> </task-notification>
```

**User message (entire message):**
```
## SKILL: TESTING STRATEGY # Testing Strategy Apply this testing strategy for all new code: ...
```

**User message (entire message):**
```
## Final Verdict **Issues Found** **Blockers (must fix):** 1. **Task B1, Step 3:** `phase_audit.add_iteration(iteration_audit)` will not compile...
```

**User message (short option selection with no elaboration):**
```
A, we can use .env file
```
