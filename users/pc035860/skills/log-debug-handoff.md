---
name: log-debug-handoff
description: >
  Trigger: agent needs runtime log data to debug; user provides the log file path. Fires
  after agent adds debug logging and asks user to reproduce.
---

When the agent instruments the code and asks for logs, pc035860 runs the app, captures the
output to a log file, and replies with just the path — sometimes with a suggestion to use
a subagent for analysis if the log is large.

**Short form (most common):**
```
log 在 logs/2027.txt
```
```
logs/0332.txt
```
```
logs/1736.txt
```

**With subagent suggestion (for large logs):**
```
log 在 logs/2027.txt
可以用 subagent 分析
```
```
好了，這次 log 比較大，建議用 subagent 處理
```

**With success signal mixed in:**
```
我看成功了，修好了!
logs/0341.txt
```

**What it signals:** The user has reproduced the issue and captured logs. The agent should
read the referenced file (using a subagent if the file is large) and analyze the log content
to identify the root cause. Do not ask the user to paste the log content inline.
