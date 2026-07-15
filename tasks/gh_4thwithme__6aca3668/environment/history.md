> DEVELOPER

hey bro do you know what is CLAUDE_CODE_AUTO_COMPACT_WINDOW

> AGENT

Env var that sets the token threshold triggering auto-compaction.

- **Default**: 200K tokens (or 1M for extended-context models like Opus 4.6)
- **Usage**: `export CLAUDE_CODE_AUTO_COMPACT_WINDOW=500000`
- **Cap**: Can't exceed your model's actual context window

Useful for forcing earlier compaction to reduce costs or prevent context exhaustion in long sessions.