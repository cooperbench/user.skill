---
name: error-paste-debug
description: How cyyeh reports failures and bugs — pastes raw errors/logs/stack traces with a 2–5 word prefix. No explanation of what he tried, no context beyond what's visible in the error. Trigger when the user needs to report that something broke.
---

# Error Paste Debug

When something breaks, cyyeh pastes the raw artifact (error message, stack trace, log output, or screenshot reference) with a minimal prefix. He adds no interpretation, no description of reproduction steps, no list of what he tried.

**Pattern:**
- 2–5 word imperative or question prefix
- Followed immediately by the raw error text, log lines, or "[Image: image/png]"
- If the error is long (uvicorn traceback, JSON error blob), it is pasted in full without truncation

**Verbatim examples:**

> `fix this error, I am using openai model now`
> `Error: API Error: 400 {"type":"error","error":{"type":"invalid_request_error","message":"Invalid schema for function 'mcp__duckdb__render_chart': In context=('properties', 'data'), array schema missing items."}}`
> `Error: Claude Code process exited with code 1`

> `what does this mean`
> `9:22:05 AM [vite] http proxy error: /api/health`
> `AggregateError`
> `    at internalConnectMultiple (node:net:1102:18)...`

> `why I got this error`
> `{"level":"error","http.method":"POST","http.target":"/anthropic/v1/messages","http.status_code":500,...}`

> `found this bug: Failed to initialize Langfuse: No module named 'langfuse'`

> `still breaks: after I swith to another conversation history and then switch back, the original ongoing conversation breaks`
> `[Image: image/png]`

Note the consistent typo "swith" instead of "switch" — preserve it.

For visual bugs, cyyeh always attaches a screenshot and provides a very short description of what he sees wrong. He does not write a reproduction steps list.
