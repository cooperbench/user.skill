---
name: error-paste-debug
description: How dayhaysoos reports failures — raw terminal output or error message pasted verbatim, no preamble, no explanation. Triggers when a command fails or UI shows an unexpected error.
---

When something breaks, dayhaysoos pastes the exact failure with zero framing. No "I got this error:" — just the output. The agent is expected to read the paste and diagnose.

For UI errors, he types the error message text exactly as it appears on screen.

For terminal failures, he pastes the full shell session including the prompt line, the hanging command, the ^C interrupts, and the retry attempts.

**Example 1** (terminal failure):
```
nickdejesus@MacBook-Pro-6 nimbus % tar -czf /tmp/nimbus-src.tar.gz -C /Users/nickdejesus/Code/nimbus .COMMIT_SHA="$(git rev-parse HEAD)"

^C
nickdejesus@MacBook-Pro-6 nimbus %
nickdejesus@MacBook-Pro-6 nimbus %
nickdejesus@MacBook-Pro-6 nimbus % tar -czf /tmp/nimbus-src.tar.gz -C /Users/nickdejesus/Code/nimbus .
COMMIT_SHA="$(git rev-parse HEAD)"
^[[D^C
nickdejesus@MacBook-Pro-6 nimbus %
```

**Example 2** (UI error, no preamble):
> "Unable to load review Unexpected token '<', \"<!doctype \"... is not valid JSON"

After pasting, he may add a brief question if he has a hypothesis: "why do we need VITE_NIMBUS_API_BASE_URL to be able to see?" — but often he just pastes and waits for the diagnosis.
