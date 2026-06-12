---
name: url-drop-debug
description: Trigger — user opens a debug session by dropping a raw GitHub issue/discussion URL with zero or minimal surrounding text; expects agent to read the issue and fix it
---

# url-drop-debug

When opening a debug task, the user often provides only a GitHub issue or discussion URL as the entire request, sometimes with one short prefix. No description of the problem. No explanation of what to do. The URL IS the task.

**Variants**:
- Bare URL with a colon prefix: `分析问题:https://github.com/Nagi-ovo/gemini-voyager/discussions/495`
- Bare URL alone (newline only): `https://github.com/Nagi-ovo/gemini-voyager/issues/538`
- URL + single question: `https://github.com/Nagi-ovo/gemini-voyager/issues/497\\ 是插件导致的吗?`
- URL + imperative: `修复：https://github.com/Nagi-ovo/gemini-voyager/issues/421`
- Short reference: `查看 issue 371 是否可以很轻松解决`
- `gh 429 修复正确吗？` — references a PR/issue number without URL

**What is NOT included**:
- Any description of the bug
- Any suggestion of where to look
- Any expected vs actual behavior
- Any "please"

**Expected agent behavior**: read the issue, understand the bug, implement the fix, then commit with `Fixes #xxx`.
