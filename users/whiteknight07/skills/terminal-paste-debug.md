---
name: terminal-paste-debug
description: User responds to agent questions or failures by pasting raw SSH/terminal output verbatim with zero commentary. Triggered when the agent asks for more info or when a command fails on the server.
---

When the agent asks "can you run X and share the output?" or when a server command fails, Whiteknight07 does not summarize or annotate — he pastes the full terminal session including the shell prompt, the command, and all output, as-is.

There is **no preamble**, **no explanation**, **no "here's what happened"** — just the raw dump.

**Verbatim examples**:

Agent asked for more server info → user pasted entire SSH session:
> "[stavan@s216 AiTutor]$ <docker ps -a && echo \"===AITUTOR DIR===\" && ls -la && echo \"===ENV===\" && cat .env 2>/dev/null | grep -v SECRET<POSE===\" && cat docker-compose.yml 2>/dev/null && echo \"===ECOSYSTEM===\" && cat ecosystem.config.js 2>/dev/null\n===PM2===\n┌────┬───────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐\n│ id │ name      │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │\n└────┴───────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘\n===DOCKER===\npermission denied while trying to connect to the Docker daemon socket..."

Agent asked for nginx config → user pasted failure:
> "[stavan@s216 AiTutor]$  echo \"===NGINX MAIN===\" && sudo cat /etc/nginx/nginx.conf && echo \"===PORT 4768===\" && ss -tlnp | grep 4768\n===NGINX MAIN===\ncat: /etc/nginx/nginx.conf: No such file or directory"

The same pattern repeats across multiple turns — agent asks for more, user pastes more raw output.
