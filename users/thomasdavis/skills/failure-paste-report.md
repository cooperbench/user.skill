---
name: failure-paste-report
description: How thomasdavis reports failures — pastes raw task notification XML or CLI output verbatim as his reply, with no commentary. Trigger when a background command fails or a screenshot shows an error.
---

# failure-paste-report

When a background command fails or the UI shows something wrong, thomasdavis does not describe the error in his own words. He pastes the failure artifact directly:

- Failed task notification: the full `<task-notification>` XML block with `<status>failed</status>`
- Screenshot: sends an image (`[Image: image/png]` or `[Image: source: REDACTED...]`) as the entire message
- CLI error output: pastes raw terminal output (e.g., cloudflared logs, build errors) with no preamble

Occasionally he adds a one-liner after the paste, but the paste *is* the report. He expects the agent to read the output file or interpret the screenshot without being told what the error is.

## Examples

**Task notification failure paste (no surrounding text):**
> "\<task-notification\>\n\<task-id\>b4f17e3\</task-id\>\n\<output-file\>/private/tmp/claude-501/.../tasks/b4f17e3.output\</output-file\>\n\<status\>failed\</status\>\n\<summary\>Background command \"Type-check all packages\" failed with exit code 1\</summary\>\n\</task-notification\>\nRead the output file to retrieve the result: /private/tmp/..."

**Screenshot as full message:**
> "[Image: source: REDACTED 2026-02-13 at 12.35.31 AM.png]"

**CLI paste with embedded question:**
> "ajaxdavis@Ajaxs-MBP platform % cloudflared tunnel --url http://localhost:3333/ 2026-02-17T05:57:26Z INF Thank you for trying Cloudflare Tunnel... [long terminal output] could you analyze why this url seems to hang while loading"

**MCP error output pasted verbatim:**
> "⏺ claude-code-tools - perplexity-ai-ai-sdk--perplexitySearch (MCP)(query: \"jamesspalding.org\", max_results: 10)\n  ⎿  Error: MCP error -32602: Tool not found in collection: perplexity-ai-ai-sdk--perplexitySearch\n\n⏺ ... can you check the database i definitely added the tool call to my collection otherwise how would you know to call it"
