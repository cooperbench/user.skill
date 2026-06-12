---
name: skill-redirect
description: How zchee corrects by re-invoking a different skill with a refined task string, instead of explaining the error. Trigger when the agent's current approach is wrong and zchee gives a new direction.
---

# Skill Redirect

When the agent takes the wrong approach, zchee does not argue or explain. He restarts with a different skill, often embedding the corrective framing directly in the skill argument.

**Pattern:** `$<newskill> "<refined task or framing>"`

The new task string implicitly corrects the old one. He does not say "that was wrong" or "stop doing X" — the redirect is the entire message.

**Examples:**
```
$autopilot Replace to `agentmux` repository name to `zmux`
```
```
$ultrawork "do work both of 'make status-bar #(...) expansion non-blocking / cached / deferred' and 'bypass/skip expensive composed status rendering during the early attach/startup window' using Zig's `std.Io`"
- Zig source code: https://codeberg.org/ziglang/zig
```
```
$deep-interview --deep "statusline is not drawn as defined in `~/.config/zmux/zmux.conf`"
```
```
$team "Migrate GCD and io_uring to libxev"
```
```
$plan --consensus --direct .omx/specs/deep-interview-statusline-is-not-drawn-correctly.md
```

Note: sometimes the redirect includes a file path or URL as a supplementary reference, appended after the skill invocation on a new line.
