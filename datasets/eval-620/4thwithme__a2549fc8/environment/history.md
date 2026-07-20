> DEVELOPER

hey bro do you know what is CLAUDE_CODE_AUTO_COMPACT_WINDOW

> TOOL

tool_use Agent
id: toolu_01F2V2XbzrmKqPg6x7CjF4rG
```json
{
  "description": "Look up CLAUDE_CODE_AUTO_COMPACT_WINDOW",
  "subagent_type": "claude-code-guide",
  "prompt": "What is CLAUDE_CODE_AUTO_COMPACT_WINDOW? What does it do, what values does it accept, and where is it configured? Be concise."
}
```

> TOOL

tool_result
id: toolu_01F2V2XbzrmKqPg6x7CjF4rG
```
## Summary

**`CLAUDE_CODE_AUTO_COMPACT_WINDOW`** controls the context capacity (in tokens) that triggers auto-compaction.

**What it does:** Sets a custom threshold for when Claude Code compacts conversation history to reclaim context space.

**Values it accepts:**
- Any integer representing tokens
- Capped at your model's actual context window (cannot exceed it)
- Defaults: 200K tokens (standard models) or 1M tokens (extended context models like Opus 4.6)

**Where it's configured:** As an environment variable (set via `export CLAUDE_CODE_AUTO_COMPACT_WINDOW=value` in your shell or in `.env` files).

**Example:** Set to 500K to make a 1M-token model start compacting at 500K instead of waiting for 1M—useful to reduce token costs or prevent context exhaustion in long sessions.

Sources:
- [Claude Code Environment Variables](https://code.claude.com/docs/en/env-vars.md)
- [Claude Code Environment Variables on GitHub](https://gist.github.com/mculp/e6a573f2a45ef7dbbf30f6a8574c7351)
agentId: a6c9809aa66ed9138 (use SendMessage with to: 'a6c9809aa66ed9138' to continue this agent)
<usage>total_tokens: 43291
tool_uses: 6
duration_ms: 35443</usage>
```

> AGENT

Env var that sets the token threshold triggering auto-compaction.

- **Default**: 200K tokens (or 1M for extended-context models like Opus 4.6)
- **Usage**: `export CLAUDE_CODE_AUTO_COMPACT_WINDOW=500000`
- **Cap**: Can't exceed your model's actual context window

Useful for forcing earlier compaction to reduce costs or prevent context exhaustion in long sessions.