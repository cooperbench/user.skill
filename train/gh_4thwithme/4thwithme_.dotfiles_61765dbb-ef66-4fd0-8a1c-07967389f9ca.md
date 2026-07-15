> DEVELOPER

how to delete mcp new relic from the user and repo?

> AGENT

The New Relic MCP isn't in any local `settings.json` file — it has the `claude_ai_` prefix, meaning it's a Claude.ai-managed integration (connected via the web app), not a locally configured server.

**Two ways to remove it:**

### 1. CLI (for locally-configured MCPs)
```bash
# User-level
claude mcp remove "New_Relic" -s user

# Project-level
claude mcp remove "New_Relic" -s project
```

### 2. Claude.ai web app (for `claude_ai_`-prefixed MCPs like yours)
Go to **claude.ai → Settings → Integrations** and disconnect New Relic there.

Since the tool names show `mcp__claude_ai_New_Relic__*`, option 2 is the right path for this one. The local `settings.json` approach only applies to MCPs you added via `claude mcp add` or manually in settings files.

> DEVELOPER

No user-scoped MCP server found with name: New_Relic

> AGENT

The name has a space. Try:

```bash
claude mcp remove "claude.ai New Relic" -s user
```

Also there's a second entry `newrelic` (local HTTP). To remove both:

```bash
claude mcp remove "claude.ai New Relic" -s user
claude mcp remove "newrelic" -s user
```

> DEVELOPER

  ~/Documents/repo/recommendations-service   RECO-0000-fix-lint-errors *18 +6 ❯ claude mcp remove "newrelic" -s user
 17:18:07
No user-scoped MCP server found with name: newrelic

> AGENT

It's local scope, not user scope:

```bash
claude mcp remove "newrelic" -s local
```

For `claude.ai New Relic` — that's a claude.ai web integration. Remove it at **claude.ai → Settings → Integrations**.

> DEVELOPER

no verify
