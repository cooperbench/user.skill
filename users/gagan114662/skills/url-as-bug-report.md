---
name: url-as-bug-report
description: Reports a broken service by pasting the URL and a 2-4 word complaint. No stack trace, no context, no steps to reproduce. Trigger when the user's message is a bare URL followed by "not working", "is down", or similar.
---

# url-as-bug-report

When something is broken, paste the URL and add the shortest possible description of the symptom.
No explanation, no logs, no context. Agent is expected to diagnose from there.

**Pattern:** `<url> <2-4 word complaint>`

## Examples

```
http://127.0.0.1:50051/ this is not working
```

```
http://127.0.0.1:50051/ is down i wanna see codex and claude here
```

The second example is slightly longer because it also states what SHOULD be visible — this is
the maximum elaboration. Still no punctuation, all lowercase.
