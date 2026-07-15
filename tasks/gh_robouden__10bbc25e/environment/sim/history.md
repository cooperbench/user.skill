> DEVELOPER

Can you use the gitnexus MCP server now?

> AGENT

No — there's no `gitnexus` MCP server available in this session. The MCP servers I currently have access to are: - claude.ai Blues - claude.ai Gmail - claude.ai Google Calendar - claude.ai Google Drive - claude.ai Motherduck - claude.ai Safecast_MCP - claude.ai Slack If you've just added gitnexus, you'll likely need to restart Claude Code (or reconnect the MCP server) for it to show up. Want me to help check your MCP configuration?

> DEVELOPER

?

> AGENT

The screenshot shows `gitnexus` is connected as a User MCP, but its tools aren't exposed to this session — none appear in my deferred tools list. This usually means the session was started before gitnexus was added/connected. Try `/mcp` to refresh, or restart Claude Code so the gitnexus tools get registered.

> DEVELOPER

But in the terminal it works fine?

> AGENT

The dialog says "Unable to connect. Is the computer able to access the url?" — so the VSCode extension can't reach the gitnexus URL, even though the terminal CLI can. That's why the previous screen showed "connected" (terminal session) but this VSCode session can't load its tools. Common causes: - VSCode is running in a different environment (e.g. WSL/remote/devcontainer) than your terminal, so it can't resolve `localhost` or a private host that the terminal can. - Proxy / `HTTP_PROXY` env vars are set in your shell but not inherited by VSCode. - The MCP entry in `~/.claude.json` uses a hostname only reachable from the terminal's network namespace. Quick checks: 1. Look at the gitnexus URL in `~/.claude.json` — is it `localhost`, a LAN IP, or a tunneled host? 2. From a VSCode integrated terminal (not your normal terminal), run `curl -v <that-url>`. If that fails too, it's an environment-level reachability issue, not a Claude one. Want me to read `~/.claude.json` and check the gitnexus entry?

> DEVELOPER

yes

> AGENT

Reading the gitnexus entry from `~/.claude.json`.

> AGENT

Found it — gitnexus is configured as `http://localhost:4747/api/mcp`. Let me check if it's reachable.

> AGENT

Diagnosis: gitnexus is configured at `http://localhost:4747/api/mcp`, but **nothing is listening on port 4747** — the connection is refused, no `gitnexus` process is running, and no socket is bound. So the VSCode dialog is correct: the server isn't reachable. The earlier "connected" status in your terminal `/mcp` screen must have been stale (cached from a prior successful connection — the CLI doesn't always re-probe). To fix: - Start the gitnexus server (whatever launches it on :4747) and then click **Reconnect** in the VSCode MCP dialog. - If you don't remember how it's started, tell me and I can look for a launch script / systemd unit / package.