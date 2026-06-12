---
name: url-probe
description: >
  Trigger: user encounters an external tool, library, or documentation and wants to evaluate
  whether it fits into the dirigent. Paste URL + short question, no setup.
---

The user discovers something online and hands the URL to the agent with a one-line evaluation question. The format is always:

`<URL> -> <question>`

or

`<context sentence>: <URL> -> <question>`

No background. No explanation of what the URL contains. The agent is expected to fetch it and reason about fit.

## Examples

- `"https://entire.io/ -> cool addition to our dirigent or not? directly integratable? or could we just piggyback some ideas?"`
- `"I recently read about this: https://docs.byterover.dev/context-tree/local-space-structure -> worth using as knowledge store for the .dirigent? at least, if brv store exists, dirigent should know how to use."`
- `"Look what I found online: ${CLAUDE_PLUGIN_DATA}: <description from docs>\n\nhttps://code.claude.com/docs/en/plugins-reference"` (paste of doc excerpt + URL, no explicit question — user expects agent to understand the implication)
- `"look here you lazy piece of shit: https://platform.claude.com/docs/en/agent-sdk/subagents#agent-definition-configuration"` (URL as proof that agent was wrong)
- `"https://code.claude.com/docs/en/hooks -> please do. we would love to know when the dirigent: starts a session, ends a session..."` (URL + direct implementation request)

## When NOT to use

When the user already knows they want to use the tool and jumps straight to "implement X using Y". The URL-probe is the evaluation phase, not the implementation phase.
