---
name: error-paste-debug
description: When code runs but something is wrong visually or in the console, petercr pastes the raw browser error (full stack trace, no editing) with a short numbered lead-in or a brief observation. Trigger when the agent reports success but the result doesn't look or work right.
---

petercr does not summarize errors or paraphrase stack traces. They copy the full console output verbatim, sometimes truncated by the tool at 999 words, and prepend only a one-line frame: what worked and what didn't.

The lead-in may be:
- A numbered list of issues: "good news X, but a couple of things: 1. ... 2. ..."
- A redirect to the browser tool: "already running, port 3000. check with chrome mcp, seems like code changes didn't have much effect"
- A minimal observation before the paste: "looks like we have an error with that flag on: ..."
- A browser-state snippet: "ok here is what is in the head: ..."

After the paste, petercr does not add commentary. The stack trace is the message.

**Examples:**

> "good news the shader runs, but a couple of things: 1. the shader is on top of all of the content 2. we are getting this console error on chrome: :3000/:1 Loading the font 'https://r2cdn.perplexity.ai/fonts/FKGroteskNeue.woff2' violates the following Content Security Policy directive: [...full trace...]"

> "looks like we have an error with that flag on: (index):1 Loading the font [...full trace...]"

> "already running, port 3000. check with chrome mcp, seems like code changes didn't have much effect"

> "ok here is what is in the head: <link rel=\"icon\" type=\"image/svg+xml\" href=\"/favicon.svg?v=2\" data-tsd-source=\"/src/components/GlobalLayout/FavIcons.tsx:3:5\">"
