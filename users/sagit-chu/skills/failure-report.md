---
name: failure-report
description: When a fix doesn't work or a new bug surfaces, user reports it by pasting the raw error or stating the symptom in one sentence, often appending "请检查" or "还是报错". Trigger when the agent's previous fix did not resolve the problem.
---

Sagit-chu does not write bug reports with context, reproduction steps, or environment info. They paste the error string (if there is one) and add a minimal annotation, or just describe the symptom as a single sentence ending in "请检查".

**Error paste pattern** — raw error inline (no code block), followed by "还是报错":
```
Tr QStest2 FatM: create service46 9_9.top failed: listen tcp40.0.0.0:2000: bind: address already inuse.  还是报错
```

**SQL error paste**:
```
添加额外ip的时候报错：SQL logic error: no such column: extra_ips (1)
```

**Symptom description without error text**:
```
创建用户日期选择器没有了，请检查
```
```
普通用户登陆后，首页的仪表隧道权限里 已用流量为0，请检查
```
```
前端编译告警，有一些弃用了，请检查
```

**Re-check request when agent's analysis was wrong**:
```
重新检查一下
```

No elaboration. If the agent needs more information, it must ask — the user won't volunteer it.
