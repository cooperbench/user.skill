---
name: url-terse-fix
description: When an API endpoint is misbehaving, user pastes the localhost URL on line 1 and a short Russian fix instruction on line 2
---

The user identifies the broken endpoint by URL, optionally pastes the wrong response body, then gives a one-line Russian instruction. No full sentence. Uses "ручку" (Russian dev slang for an API endpoint/handler).

**Trigger**: observing a broken or mis-routed API endpoint in the browser or terminal.

**Pattern**:
```
http://localhost:3838/<path>
<terse Russian instruction>
```

or with response body pasted between URL and instruction.

**Examples**:
> `http://localhost:3838/api/risk-analysis?limit=20`
> `нужно пофиксить эту ручку`

> `http://localhost:3838/code/insights и другие все еще, сделай нормальное api путь`

> `а запросы все еще http://localhost:3838/code/stats а они отдают html`

> `не загружаются со страницы http://localhost:3838/insights?tab=patterns  Internal Server Error`

Note the double-space before "Internal Server Error" — copy-paste artifact preserved as-is.
