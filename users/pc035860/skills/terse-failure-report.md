---
name: terse-failure-report
description: >
  Trigger: agent delivers a fix and user tests it but the problem persists. Fires on any
  post-fix validation turn.
---

When a fix doesn't work, pc035860 reports it in 2–5 words. Never explains what changed,
never provides additional context unless previously asked. Sometimes appends a debug command.

**Verbatim examples:**

Pure terse:
- `還是一樣`
- `結果還是一樣`
- `還是沒好`
- `還是沒有解決`

With slight observation:
- `我測試完全沒解決？`
- `換頁之後還是會滑個半頁才停`
- `問題依然存在`

With a follow-on debug command:
- `還是沒好 我上網查了一下資料，看有沒有幫助 [pastes StackOverflow research]`
- `/silennai:debug 還是沒好`
- `log 在 logs/0332.txt`

**Escalation to frustration (rare, failure_report → rejection boundary):**
- `還是一樣，會跑掉\n這真的很難寫嗎？`

**What it signals:** The reported behavior is unchanged. Do not interpret as partial success.
Do not ask "can you describe what you observed" — user has already stated it. Dig deeper.
