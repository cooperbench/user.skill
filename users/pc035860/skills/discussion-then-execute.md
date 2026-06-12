---
name: discussion-then-execute
description: >
  Trigger: user ends a task prompt with a discussion request before implementation.
  Fires on complex or multi-phase tasks where user wants to align before code is written.
---

For non-trivial features or debugging sessions, pc035860 ends the prompt with a request to
discuss before acting. The phrase is almost always the same:

**Verbatim phrase:**
```
整理一下，跟我討論下一步動作
```
(Summarize and discuss the next steps with me)

This is then immediately followed by `/explore` or a variant like `/explore -a`, `/explore -n 3`,
or `/explore -n 10`.

**Examples:**

Opening a debug session:
```
我想提報一個問題，應該是跟我們用 Trackpad 縮放或換頁的行為有關係。
[...description...]
整理一下，跟我討論下一步動作

- 使用 適合的subagent 或 @agent-general-purpose (run in foreground)...
```

Opening a feature request:
```
討論一下，目前我們有 DuoPage 模式（多頁模式）。
[...spec...]
整理一下，跟我討論下一步動作

/explore
```

**What it signals:** User does NOT want the agent to start implementing immediately. Wants a
plan summary and discussion turn first. If this phrase appears, the agent should analyze and
propose, not write code yet.
