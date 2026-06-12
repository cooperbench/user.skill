---
name: terminal-paste-debug
description: >
  Trigger: AlienKevin encounters a shell/CLI error or unexpected state. He pastes the
  raw terminal output verbatim (prompt + command + output) followed by a single short question.
---

When debugging, AlienKevin does not describe the problem — he pastes the terminal session directly and appends one question. No "I got this error:", no "here is the output:". Just the block, then the question.

**Verbatim example:**
> `"kevin@kevin-cpu:~/marin-harbor$ npm list -g @openai/codex\n/home/kevin/.nvm/versions/node/v22.22.2/lib\n└── @openai/codex@0.117.0\n\nkevin@kevin-cpu:~/marin-harbor$ which codex\n/home/kevin/.nvm/versions/node/v22.22.2/bin/codex\nkevin@kevin-cpu:~/marin-harbor$ codex\n\n  ✨ Update available! 0.89.0 -> 0.117.0\n...\nI think codex is not resolving to the right bin?"`

**Another example (shorter):**
> `"I deleted the /usr/local codex but now the codex name no longer resolves to a binary"`

The question is always short (one sentence or less), often ending with `?` even when phrased as a statement. He does not attempt to diagnose before asking; he trusts the agent to interpret the raw output. For task-notification failures, he forwards the notification XML directly and asks "Read the output file to retrieve the result: REDACTED.output" — the output file name is the answer format he expects back.
