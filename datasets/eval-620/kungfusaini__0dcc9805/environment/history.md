> DEVELOPER

hey man I need a notifications in claude code (macos desktop notifs) reeaserch

> TOOL

tool_use Agent
id: toolu_01UkkdEbMibp2mWALdyi9Eqt
```json
{
  "description": "Claude Code macOS notifications research",
  "subagent_type": "claude-code-guide",
  "prompt": "Research how to set up macOS desktop notifications in Claude Code (the CLI tool). The user is on macOS (Darwin 24.6.0) and wants notifications to appear on their desktop.\n\nCover:\n1. Built-in notification support in Claude Code — is there a `Notification` hook event? What settings.json configuration is needed?\n2. How to wire it up to actually trigger native macOS notifications (e.g., via `osascript -e 'display notification ...'` or `terminal-notifier`).\n3. Common patterns: notify when Claude needs input (waiting on user), when a task completes (Stop hook), when permission is needed, etc.\n4. Any gotchas on macOS — terminal needing notification permissions in System Settings, Focus/Do Not Disturb behavior, etc.\n5. Concrete settings.json example(s) the user can paste in.\n\nBe practical — the user wants to actually set this up, not just understand it abstractly. Report under 500 words with a copy-pasteable settings.json snippet."
}
```

> TOOL

tool_result
id: toolu_01UkkdEbMibp2mWALdyi9Eqt
```
Perfect! I found comprehensive documentation on macOS desktop notifications in Claude Code. Let me summarize the key findings:

## macOS Desktop Notifications in Claude Code

Claude Code has **built-in `Notification` hook support** designed exactly for this use case. Here's what you need to know:

### 1. **Notification Hook Event**
Yes, `Notification` is a first-class hook event that fires when Claude is waiting for your input or permission. This is specifically designed to alert you to switch back to the terminal.

### 2. **macOS Native Notifications**
Claude Code uses `osascript` to trigger native macOS notifications through the Script Editor app. The command is simple:
```bash
osascript -e 'display notification "Claude Code needs your attention" with title "Claude Code"'
```

### 3. **Common Notification Triggers**
The hook fires on multiple notification types via matchers:
- `permission_prompt` — when Claude needs permission to run a tool
- `idle_prompt` — when Claude finishes and waits for your next input
- `auth_success` — on authentication completion
- `elicitation_dialog`, `elicitation_complete`, `elicitation_response` — MCP server interactions

Use an empty matcher (`""`) to fire on all notification types.

### 4. **macOS Gotcha: Script Editor Permissions**
**This is critical:** `osascript` routes notifications through Script Editor. […]

> AGENT

## macOS Desktop Notifications in Claude Code

Claude Code has a built-in `Notification` hook event designed exactly for this. Here's the rundown:

### The hook
Fires when Claude needs your attention — permission prompts, idle/waiting for input, auth events, etc. Use an empty matcher (`""`) to catch them all.

### Native macOS notifs
Use `osascript` — no extra tools needed:

```bash
osascript -e 'display notification "..." with title "Claude Code"'
```

### Settings (paste into `~/.claude/settings.json`)

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

If you've already got hooks, merge `Notification` as a sibling key inside the existing `"hooks"` object.

### ⚠️ The gotcha that gets everyone
`osascript` routes notifications through **Script Editor**. If Script Editor doesn't have notification permission, it fails silently — no error, just nothing happens.

**One-time fix:**
1. Run `osascript -e 'display notification "test"'` in Terminal
2. Open **System Settings → Notifications**
3. Find **Script Editor**, enable **Allow Notifications**
4. Test again

Also check Focus/Do Not Disturb if you're not seeing them.

### Verify
- Run `/hooks` inside Claude […]