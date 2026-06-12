---
name: open-items-delegate
description: >
  Trigger: handing off a set of tracked bugs or TODO items to the agent.
  nosman opens sessions or redirects mid-session using a structured "open items" list.
---

# open-items-delegate

nosman maintains a running list of bugs and unfinished work. When handing off a batch of items,
he uses a fixed preamble followed by a bulleted list. The items are written in third-person
technical language, often referencing specific table names, function names, or UI components.

This pattern appears as both an **opening prompt** (session kickoff) and a **mid-session correction**
(after agent claims done but items remain).

## Verbatim examples

```
Please work on the following open items:
- The `saveGitOidMapping` call now runs on every index pass for every checkpoint; a more targeted approach (e.g., only for checkpoints missing a mapping) could reduce unnecessary DB reads at scale.
```

```
Please work on the following open items:
- subSessionId is never actually populated in the DB — the AppleScript spawn opens a terminal but doesn't return a session ID to store back on the open items
```

```
Please work on the following open items:
- CheckpointDetail.tsx and CheckpointTimeline.tsx may still have hardcoded light colors not audited in this session
- ToolUseItem.tsx and CheckpointMessageItem.tsx dark mode colors were patched but not fully verified in the chat transcript layout
```

The item descriptions are precise and diagnostic — they name the symptom, the specific code
location, and often the root cause. nosman writes these items himself; they are not copy-pasted
agent output.
