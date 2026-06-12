---
name: resume-opener
description: >
  Trigger: starting a new Claude Code session to pick up work from a prior session.
  nosman opens with a single word and expects the agent to restore full context.
---

# resume-opener

When starting a session that continues prior work, nosman types just `resume` — nothing else.
No context, no explanation of what to resume, no session ID. He expects the agent to read
prior context and continue from wherever they left off.

He also uses brief openers like `Test new session` for throwaway test sessions, or states the
next task immediately without preamble when the context is fresh.

## Verbatim examples

```
resume
```

```
Test new session
```

```
what recently changed about the package.json file?
```

When he has a structured task to hand off, he upgrades to the `open-items-delegate` pattern
instead of the bare resume.
