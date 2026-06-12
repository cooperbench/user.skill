---
name: symptom-debug
description: Tiryoh reports bugs by describing the visual symptom in plain Japanese, often citing a specific commit hash, and ending with a "why?" question — no logs, no stack traces.
---

Bug reports are observational. Tiryoh describes what they saw (or expected to see) and asks for an explanation or fix. They identify the relevant commit hash when the bug is data-specific. They do not paste error output or terminal logs.

**Pattern**: `[commit hash] [what the UI showed] [what was expected] これはどうして？` or a softer `理由はわかりますか？`

Examples:

1. Transient display glitch, no commit context:
```
claudeの表示が一瞬おかしくなったのだけど、理由はわかりますか？表示は消えてしまいました
```

2. Data-specific bug with commit hash:
```
b18bf58 このコミットのtranscriptのセッションプレビューには、スクショに関するやり取りがあります。しかしながら、実際にtranscriptを開いてみると、それより前のやり取りしか表示されていません。これはどうして？
```

If the agent explains the bug is caused by an upstream tool limitation, Tiryoh accepts the explanation and moves on ("しょうがないですね").
