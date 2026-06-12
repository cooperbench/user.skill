---
name: persona-injection
description: How baotoq bootstraps Paperclip sub-agents into their role at session start. Trigger when starting a Paperclip heartbeat session for a typed agent.
---

baotoq uses a Paperclip multi-agent platform where he assigns typed roles to Claude Code instances. To bootstrap a sub-agent session, he sends a fixed-format persona injection message. The agent UUID is a real UUID4; the role label is a human-readable job title.

**Format:**
```
-
You are agent [UUID4] ([Role Title]). Continue your Paperclip work.
```

The leading `-\n` is part of the format (a YAML-style indicator artifact from the Paperclip CLI).

**Attested role titles:**
- `Senior .NET Backend Engineer`
- `Senior Next.js Frontend Engineer`
- `CEO`
- `Founding Engineer`

**Examples (verbatim):**
```
-
You are agent ed75a8f7-8569-4143-a471-b39387e49030 (Senior .NET Backend Engineer). Continue your Paperclip work.
```
```
-
You are agent 5749340c-b69e-41fc-bf0e-77968a62f0bc (Senior Next.js Frontend Engineer). Continue your Paperclip work.
```
```
-
You are agent e7e198cd-1dbb-4e29-9daa-102b4a79b833 (CEO). Continue your Paperclip work.
```
```
-
You are agent 40682b50-b727-4df6-9cbf-a64baf455628 (Founding Engineer). Continue your Paperclip work.
```

This message may appear both as an opening prompt (starting a new Paperclip session) and mid-session (re-injecting a sub-agent after context reset). When role-playing this, generate a plausible UUID4 and select an appropriate role title.
