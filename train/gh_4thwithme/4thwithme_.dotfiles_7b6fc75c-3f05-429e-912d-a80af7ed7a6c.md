---
session_id: "4thwithme/.dotfiles|7b6fc75c-3f05-429e-912d-a80af7ed7a6c"
developer: "gh:4thwithme"
split: train
source: crawl
repo: 4thwithme/.dotfiles
start_time: "2026-04-14T15:40:35.444Z"
n_turns: 18
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

help me setup new relic locally https://docs.newrelic.com/docs/agentic-ai/mcp/setup/#claude-code
i want this method

{
  "mcpServers": {
    "newrelic": {
      "httpUrl": "https://mcp.newrelic.com/mcp/",
      "oauth": {
        "enabled": true,
        "clientId": "pUWGgnjsQ0bydqCbavTPpw==",
        "authorizationUrl": "https://login.newrelic.com/login",
        "tokenUrl": "https://mcp.newrelic.com/oauth2/token",
        "scopes": ["openid"]
      }
    }
  }
}

but help me to put right data here

> AGENT

Reading existing settings and checking for MCP config files:

> AGENT

The config data is already correct — those are New Relic's standard OAuth values from their docs. No changes needed there.

This goes in `~/.claude/mcp.json` (global, applies to all projects):

> AGENT

Done. Restart Claude Code — on first use of a New Relic tool it will open a browser for OAuth login with your New Relic account.

> DEVELOPER

where dod you put it?

> AGENT

`~/.claude/mcp.json` — global, applies to all projects.

> DEVELOPER

ok .. but my newrelic is under okta

> AGENT

That's fine. The `authorizationUrl` points to `https://login.newrelic.com/login` — when the browser opens for OAuth, New Relic's login page will detect your org uses Okta SSO and redirect you there automatically.

No config changes needed. Just restart Claude Code and the first New Relic tool call will trigger the browser flow → New Relic login → Okta redirect → done.

> DEVELOPER

ok id did and logged in nothing happend

❯ /mcp                                                                                                                                                                                                                                     
  ⎿  Authentication successful, but server reconnection failed. You may need to manually restart Claude Code for the changes to take effect.    

after browser said all is good

> AGENT

Fully quit and relaunch Claude Code — not just reload. The message says the auth succeeded but the connection needs a fresh start to pick up the tokens.

> DEVELOPER

what does it mean fully quit

> AGENT

Close the app entirely — `Cmd+Q` in the Mac desktop app, or `Ctrl+C` in the terminal if you're running it there — then reopen it.

> DEVELOPER

i use ckaude code

> AGENT

`Ctrl+C` in the terminal to kill the process, then run `claude` again.

> DEVELOPER

yes i did it 100 times

> AGENT

Run `/mcp` again and tell me what status it shows for `newrelic` — connected, error, disconnected, etc.

> DEVELOPER

/var/folders/0q/tm_g36415fvfqd294rghvdnw0000gn/T/TemporaryItems/NSIRD_screencaptureui_NrBW7l/Screenshot\ 2026-04-14\ at\ 17.53.33.png

> AGENT

Auth is good, but the server connection itself is failing. Try option **3. Reconnect** first.

If that still fails — New Relic's MCP server (`mcp.newrelic.com`) might require a specific account feature enabled. Check in your New Relic account settings if there's an "AI" or "MCP" feature that needs to be turned on. It may be gated behind a plan tier or an explicit opt-in.
