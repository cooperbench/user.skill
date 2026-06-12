---
name: host-vs-container-frame
description: When the bug is a host/container behavior divergence, frame the problem by stating what works on the host and what fails inside Docker — never just "it doesn't work".
---

mheers consistently describes bugs in terms of the environmental split: the host behaves one way, the container behaves differently. He provides both data points so the agent knows the working baseline. He references git history ("check the last changes where we added...") to scope the regression.

**Pattern:**
```
<what works without docker / on host>. <what fails inside docker / the difference>.
```

**Examples:**

> "without docker a sound is played. running inside docker I receive the notification on the host, but no sound."

> "check the last changes where we added the notifications. without docker a sound is played. running inside docker I receive the notification on the host, but no sound."

> "locally in my ~/.config/opencode/opencode.json (mounted into docker) I've added '\"plugin\": [\"@mohak34/opencode-notifier@latest\"]' that uses libnotify (installed on my linux host). when I run opencode with this notification tool inside a container (using './os -t') the notifications do not work"

> "the installed skills are not available inside the container. I need those to be merged with the ones installed on the host"

**Note:** He references the exact mount path or tool invocation to make the environment difference concrete.
