---
name: pattern-reference
description: >
  Trigger: user wants new code to behave like existing code. They name the existing function
  or pattern explicitly and say "do it the same way" — this is a hard constraint, not a hint.
---

This user values internal consistency. When specifying new behavior, they name the existing
function that already handles the analogous case and require parity. The reference appears in:

- Opening spec plans (as implementation guidance):
  > `"\`extract_messages\` と同じパターン（\`ok\` チェック + \`needed\`/\`provided\` スコープ表示）でエラーを返すようにする。"`
  
  > `"既存の \`fetch_thread_replies\` と同じパターンで実装"`

- Mid-session corrections (as a requirement the agent missed):
  > `"権限が足りなくて取得できていなさそう。extract_messagesでやっているように、足りていない権限があればエラーを出すようにしたい。"`

**The rule**: when the user says "X と同じパターンで" or "Xでやっているように", find function X in
the codebase, read it, and replicate its error-handling and return-type conventions exactly.
Do not invent a new error handling style.

Common referenced patterns in `slk`:
- `extract_messages` — checks `ok` field, returns `Err` with `needed`/`provided` scope info
- `fetch_thread_replies` — curl-based API call pattern
