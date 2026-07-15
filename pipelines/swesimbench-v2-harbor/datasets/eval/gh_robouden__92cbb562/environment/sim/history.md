[DEVELOPER]: Can you add this to your MCP servers (for all projects): { "servers": { "gitnexus": { "command": "npx", "args": ["gitnexus", "mcp"] } } }

[AGENT]: Note: the config you pasted is in VS Code's MCP format. Claude Code stores user-scope MCP servers via the CLI (which writes to `~/.claude.json`), not in `settings.json`. I'll add it with user scope so it's available across all projects.

[AGENT]: Added to `~/.claude.json` at user scope, but the connection check failed. Let me verify the package exists on npm.

[AGENT]: The hang is expected — MCP servers wait on stdin for JSON-RPC. The `Failed to connect` was likely just the first-run `npx` install timing out the health check. Let me prime the cache and test with a real handshake.