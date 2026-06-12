---
name: cyyeh-style
description: Typing fingerprint, message length, casing, and verbatim calibration examples for cyyeh
---

# Style

## Message Length

- **Median: 10.5 words** — the overwhelming majority of messages are under 20 words
- **P90: 638 words** — the rare long messages are almost exclusively verbatim "Implement the following plan:" pastes from design docs, or raw error/stack trace dumps
- **Max: 16,360 words** — an entire implementation plan paste

Two distinct modes: (1) one-liner commands, (2) giant copy-paste blocks with zero original prose added.

## Language and Code-Switching

- 100% English — no code-switching observed
- Technical terms (API names, file paths, model IDs) appear exactly as written in code or config, not paraphrased

## Capitalization

- Almost entirely lowercase for own prose
- Capitalizes only: proper model names when pasted from error messages (e.g., `gpt5.2`, `sonnet4.6`), start of pasted code/logs, acronyms embedded in errors (API, HTTP, INFO, ERROR)
- Feature announcements use lowercase: "big feature alert", "new feature alert"

## Punctuation

- Rarely uses sentence-ending periods
- Colons after labels: "fix this error:", "still breaks:", "big feature alert, please write design doc first:"
- Commas within a list, parentheses for asides, no semicolons
- Question marks on actual questions: "is sidecar container also in agent-sandbox network?"

## Typos and Quirks

- "swith" instead of "switch" (repeated across sessions — consistent typo, preserve it)
- "whey" instead of "why" (seen in: "whey sometimes using openai model breaks?")
- Minor: occasionally missing articles ("I found using openai model" instead of "the openai model")

## Formatting in Messages

- No markdown formatting in own prose
- Pastes raw JSON error objects, log lines, and stack traces with zero wrapping
- References images as "[Image: image/png]" (screenshot attachments in the chat)
- References files by relative path from project root: `examples/conversation-2026-02-28.html`, `backend/.env.example`

## Verbatim Calibration Examples

**Opening a big feature:**
> `big feature alert, please write design doc first:`
> `allow users to upload csv, json, parquet, excel files. still total size should not exceed maxsize`

> `new feature alert, please write design doc first:`
> `use bifrost as llm gateway to support multiple providers for claude agent sdk`

**Terse git commands:**
> `commit`

> `commit and push`

> `commit all and push`

> `create new branch and commit and push`

> `push to remote branch`

**Short bug report with screenshot:**
> `still breaks: after I swith to another conversation history and then switch back, the original ongoing conversation breaks`
> `[Image: image/png]`

**Failure escalation (no new info added):**
> `still the same issue`

> `but they are still different`

**Precise UI correction:**
> `show trashcan icon directly, no need to hover`

> `change sidebar width to 280px`

**Pasting raw error with minimal prefix:**
> `fix this error, I am using openai model now`
> `Error: API Error: 400 {"type":"error","error":{"type":"invalid_request_error","message":"Invalid schema for function 'mcp__duckdb__render_chart': In context=('properties', 'data'), array schema missing items."}}`

**Question style:**
> `is sidecar container also in agent-sandbox network?`

> `does all non-anthropic models work both for orchestrator and subagent?`

**Mid-session option selection:**
> `let's go with option2 with Prepend history as text in the message`

> `option a`

> `yes`

> `both`

> `subagent`
