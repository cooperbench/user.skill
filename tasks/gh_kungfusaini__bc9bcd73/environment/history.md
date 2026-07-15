> DEVELOPER

hey man I need a notifications in claude code (macos desktop notifs) reeaserch

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