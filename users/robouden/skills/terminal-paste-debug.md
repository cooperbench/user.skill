---
name: terminal-paste-debug
description: >
  Trigger: robouden wants to share system state or verify something is running.
  He pastes raw shell output directly into the chat, no commentary before or after.
---

When verifying server state, robouden dumps the terminal output inline as plain text.
No code block, no preamble, no explanation — just the raw output:

Example 1 (verifying process binding):
```
root@simplemap:~# ss -tlnp | grep 8765
LISTEN 0      4096               *:8765             *:*    users:(("safecast-new-ma",pid=560087,fd=7))
root@simplemap:~#
```

Example 2 (verifying HTTP response):
```
root@simplemap:~# curl -I http://localhost:8765
HTTP/1.1 200 OK
Server: safecast-new-map/latest
Date: Fri, 20 Feb 2026 14:37:05 GMT

root@simplemap:~#
```

Example 3 (verifying CloudFront headers):
```
rob@rob-GS66-Stealth-10UG:~/Documents/Safecast/safecast-new-map$ curl -I https://simplemap.safecast.org | grep -iE 'cloudfront|x-cache|x-amz-cf-pop'
...
x-cache: Miss from cloudfront
via: 1.1 511de6a20636759c9d22123c6ae73eac.cloudfront.net (CloudFront)
x-amz-cf-pop: NRT12-P9
```

He then waits for the agent to interpret the output and tell him what it means. He does
not add "what does this mean?" — the paste itself is the question.
