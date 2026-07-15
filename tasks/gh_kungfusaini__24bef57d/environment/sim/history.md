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

> DEVELOPER

Ther is no script editor option

> AGENT

Yeah, that's a common gotcha — **Script Editor only shows up in the Notifications list after it's actually fired a notification once.** It's lazy-registered.

### Try this first
Run this in your terminal:
```bash
osascript -e 'display notification "hello" with title "Claude Code"'
```

Then immediately reopen **System Settings → Notifications** and scroll. Script Editor should appear now. If you got a permission prompt instead — accept it.

### If it still doesn't show
On newer macOS (Sequoia/Sonoma), notifications sometimes get attributed to your **terminal app itself** (Ghostty/iTerm/Terminal/Alacritty) rather than Script Editor. Check the Notifications list for *your terminal app name* and make sure it's allowed.

### More reliable alternative: `terminal-notifier`
Honestly, `osascript` notifications are flaky on modern macOS. `terminal-notifier` is more dependable:

```bash
brew install terminal-notifier
```

Then update your hook:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "terminal-notifier -title 'Claude Code' -message 'Needs your attention' -sound default"
          }
        ]
      }
    ]
  }
}
```

`terminal-notifier` registers itself as its own app in System Settings, so the permission entry shows up immediately and reliably.

Which terminal are you running Claude Code in? I can give you a more targeted answer.

> DEVELOPER

ternimal notifer is already working and running

> AGENT

Sweet, then you're basically done. Drop this into `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "terminal-notifier -title 'Claude Code' -message 'Needs your attention' -sound default -group claude-code"
          }
        ]
      }
    ]
  }
}
```

`-group claude-code` means new notifications replace old ones instead of stacking — change or remove if you want them to pile up.

### Want notifications when long tasks finish too?
Add a `Stop` hook (fires when Claude finishes responding):

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          { "type": "command", "command": "terminal-notifier -title 'Claude Code' -message 'Needs your attention' -sound default -group claude-code" }
        ]
      ],
      "Stop": [
        {
          "matcher": "",
          "hooks": [
            { "type": "command", "command": "terminal-notifier -title 'Claude Code' -message 'Done' -sound Glass -group claude-code" }
          ]
        }
      ]
    }
  }
}
```

Run `/hooks` inside Claude Code afterward to confirm both are registered. Want me to apply this to your settings file directly?

> DEVELOPER

no put it needs to tell me the task so I know which window to swtich too

> AGENT

Good thinking. Claude Code passes JSON to the hook on stdin — including `cwd` (project dir) and `message` (what Claude is asking). Parse it with `jq`:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "input=$(cat); terminal-notifier -title \"Claude: $(basename \"$(echo \"$input\" | jq -r .cwd)\")\" -message \"$(echo \"$input\" | jq -r .message)\" -sound default -group \"claude-$(echo \"$input\" | jq -r .session_id)\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "input=$(cat); terminal-notifier -title \"Claude: $(basename \"$(echo \"$input\" | jq -r .cwd)\")\" -message 'Done' -sound Glass -group \"claude-$(echo \"$input\" | jq -r .session_id)\""
          }
        ]
      }
    ]
  }
}
```

### What you'll see
- **Title:** `Claude: dot-config` (the project folder name)
- **Message:** the actual prompt, e.g. `Claude needs your permission to use Bash`

`-group` is keyed per session, so each Claude window's notifications replace their own old ones but don't clobber other sessions.

### Cleaner alternative (recommended)
Inline `jq` gets ugly fast. Make a small script and call it from the hook:

`~/.claude/bin/notify.sh`:
```bash
#!/usr/bin/env bash
input=$(cat)
cwd=$(echo "$input" | jq -r .cwd)
msg=$(echo "$input" | jq -r '.message // "Done"')
session=$(echo "$input" | jq -r […]

> DEVELOPER

Yes go for it

> AGENT

Quick snag — I can't find `terminal-notifier` on your PATH. I checked `/opt/homebrew/bin`, `/usr/local/bin`, `~/.nix-profile/bin`, and even mdfind — only license files inside node_modules turn up.

Did you maybe confirm `osascript` notifications working instead? Or is `terminal-notifier` installed somewhere unusual?

> AGENT

Dug thoroughly — `terminal-notifier` is **not installed**. It's not in your nix flake (neither `systemPackages` nor `homebrew.brews`), not in `/nix/store`, not in `/opt/homebrew`, not in `~/.nix-profile/bin`, not in npm/bun globals, and not on any directory in your `$PATH`. The mdfind hits were just license files inside random `node_modules`. You may be thinking of a different tool.

Going with `osascript` since it's built-in. Writing the script and wiring it up now.