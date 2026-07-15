> DEVELOPER

hey bro, does jira have JIRA cli?

> AGENT

Yes. `jira-cli` — open source Go-based CLI. Install via Homebrew: `brew install jira-cli`.

Also, there's the official Atlassian CLI plugin, but `jira-cli` (by `ankitpokhrel`) is the popular community one.

> DEVELOPER

i'm thinking to use cli instead of mcp..is it good idea?

> AGENT

Bad idea for this context.

**MCP advantages over CLI here:**
- Structured JSON responses — no text parsing
- Direct API access — faster, no subprocess overhead
- Richer data — full issue objects, not truncated CLI output
- Already integrated — `mcp__atlassian__*` tools work natively

**CLI downsides:**
- Text output needs parsing — fragile
- Subprocess overhead per call
- Limited data fidelity vs raw API

Keep MCP. CLI is fine for your own terminal use, not for AI tooling.

> DEVELOPER

i thought cli good, coz it 's simple request response structure

> AGENT

Fair point. But MCP *is* simple request/response — it's just JSON over stdio, same pattern.

The difference: CLI output is **strings** (need parsing), MCP returns **typed objects** (ready to use).

CLI only wins if MCP breaks or isn't available. You have MCP working — no reason to switch.
