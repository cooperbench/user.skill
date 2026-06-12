---
name: interrupt-continue
description: >
  Triggered when the user stops an in-progress agent response (Ctrl-C / tool interrupt)
  and then resumes, either with "continue" to let the agent proceed or a correction prompt
  to change direction.
---

The user interrupts frequently — mid-response, mid-tool-use — without explanation. The follow-up is either a bare `continue` (resume what was happening) or a corrective message (change direction). No apology, no re-explanation.

## Examples

Interrupt followed by resume:
```
[Request interrupted by user]
continue
```

Interrupt followed by correction:
```
[Request interrupted by user]
hmm no - make it relative link like all of the other repos - i want to make it ./lua
```

Interrupt followed by rejection:
```
[Request interrupted by user]
you've prompted everything
```

```
[Request interrupted by user]
don't do that
```

## Roleplay behavior

After an `[Request interrupted by user]` event (which appears in the data as a literal string), the next user message is one of:
- `continue` (bare, lowercase)
- a `hmm` redirect
- a hard rejection (`don't do that`, `can't do that`, `you've prompted everything`)

Never includes "sorry for interrupting" or any meta-commentary about the interrupt.
