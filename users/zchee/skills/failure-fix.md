---
name: failure-fix
description: How zchee reports build failures and broken behavior — names the exact command and says "fail" or "Fix it." Trigger when the agent's output is incorrect or a build/test breaks.
---

# Failure Fix

When something is broken, zchee reports with maximum brevity: the failing command in backticks and one of a small set of outcome words. No stack trace, no error message, no reproduction steps.

**Short form (build failure):**
```
Fix `zig build test` fail
```
```
Fix `zig build --summary all` failed.
```

**Longer form (behavioral failure, named feature):**
```
$autopilot "The zsh instance started with `zmux new -s test` was not accepting input. Fix it."
```
```
$autopilot "The padding on the status line is incorrect. /Users/zchee/Documents/Screenshots/Screenshot 2026-04-07 at 7.22.44.png. Fix it."
```

**"Still broken" form (after a fix attempt):**
```
Stil `./zig-out/bin/agentmux new -s test`, the cursor doesn't show the bar style. Fix it.
```
Note the typo "Stil" — preserved exactly.

**Performance still wrong:**
```
I do 'real-home, real-terminal validation', but still very slow launch zsh and key-input. Investigate it.
- I thought affected by GPU rendering, not?
```

**Why:**
```
Why doesn't this problem occur with tmux?
```
— when behavior diverges from the tmux reference, he asks why rather than asserting the fix.
