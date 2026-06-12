---
name: log-dump-debug
description: When jarvish behaves incorrectly, Hayato pastes the full raw terminal output or debug log verbatim (often thousands of words) with a one-line Japanese preamble expressing mild frustration or a simple request to analyze. Trigger when a feature has misbehaved in actual use.
---

## Behavior

Hayato does not summarize or interpret failures — he dumps the raw evidence. The structure is always:

1. Optional one-line Japanese preamble (frustration or request)
2. Triple-backtick block containing the full terminal output, including timestamps, box-drawing characters, prompt decorations, and all noise

The preamble ranges from neutral request to casual complaint:
- Neutral: `この時のログデータを入手しました。どんなデバッグログになっているか確認してください。`
- Casual complaint: `なんか頭悪いんだよなぁ… 以下の出力をみてみて。`

After the agent reproduces the issue and confirms, Hayato sends:
> `Issue reproduced, please proceed.`

After fix is verified:
> `The issue has been fixed. Please clean up the instrumentation.`

## Verbatim examples

**Example 1** (debug log analysis):
```
この時のログデータを入手しました。どんなデバッグログになっているか確認してください。 ``` 2026-03-13T23:12:00.022+09:00 [0bf1d4] DEBUG jarvish::ai::stream: src/ai/stream.rs:115: Received text chunk chunk=199 content_length=4 has_content=true content=data
[...thousands of log lines...]
```
```

**Example 2** (wrong AI behavior):
```
なんか頭悪いんだよなぁ… 以下の出力をみてみて。 ``` ✔︎ jarvis in  ~/lab/daily-alpacahack/substance 22:52:45 ❯ bat chal.py
[...full bat output, terminal session, etc...]
```
```

**Example 3** (simple failure report):
```
コマンド履歴のセッション分離がうまく行ってません。デバッグしてください
```
