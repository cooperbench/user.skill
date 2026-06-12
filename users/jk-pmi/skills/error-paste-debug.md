---
name: error-paste-debug
description: >
  Trigger: something failed — a CLI run, a hook load, a tool execution, a test.
  Paste the raw error output verbatim, then append a short imperative or question.
---

The user does not summarize errors. They paste the exact output — timestamps, log levels, module paths, stack traces — and append one of a small set of closers:

- `-> debug why this is happening`
- `-> debug why`
- `debug why   <error text>` (error inline after "debug why")
- `Is this fixed now?`
- `why?`
- nothing (paste alone)

The paste includes no commentary. The raw log IS the bug report. Typos in the closer are common.

## Examples

```
ing greenfield scaffold...
2026-04-03 20:28:10.989 | INFO     | outbid_dirigent.executor:greenfield_scaffold:232 - Greenfield scaffold produced: testing-strategy.md, architecture-decisions.md
Fri Apr  3 08:28:11 PM UTC 2026: [dirigent] [2026-04-03 20:28:11] ⏭️ Task planning übersprungen: bereits abgeschlossen
2026-04-03 20:28:11.609 | ERROR    | outbid_dirigent.executor:execute_plan:449 - No plan found
Fri Apr  3 08:28:12 PM UTC 2026: [dirigent] [2026-04-03 20:28:12] 🛑 Ausführung gestoppt: Schritt 'Ausführung' fehlgeschlagen -> debug why this is happening
```

```
1 error:
    Failed to load hooks from
    /home/dev/.claude/plugins/cache/outbid-dirigent/dirigent/0.2.0/hooks/hooks.json:
    Duplicate hooks file detected: ./hooks/hooks.json resolves to already-loaded file
    ...
    → Check hooks.json file syntax and structure
```

```
debug why   Local plugins cannot be updated remotely. To update, modify the source at: ./src/outbid_dirigent/plugin
```

```
$CLAUDE_PLUGIN_DATA is not set as external env variable :/ this kinda kills this
```

Also used for questions about behavior rather than errors:
- `"but isnt there a retry?"`
- `"does ot work when i --resume?"`
- `"ok, any idea why it worked this time? just luck?"`
