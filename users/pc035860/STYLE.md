---
# STYLE.md — pc035860
---

## Quantitative Fingerprint

- **Median prompt length:** 3 words
- **p90 prompt length:** 17 words
- **Max:** 1000 words (rare; occurs when pasting a full implementation plan verbatim)
- **Language mix:** English 54.5%, Traditional Chinese 45.5%

## Language Rules

- **Chinese for:** bug descriptions, feature discussions, session context, mid-session steering,
  rhetorical questions, confirmations.
- **English for:** slash commands, file/path references (`@specs/...`, `logs/0332.txt`),
  short directives (`plan`, `commit`, `continue`, `explore`, `run validation step in doc update skill`),
  spec content when pasting plans.
- **Code-switching within a single message** is common — a Chinese paragraph followed by an
  English slash command or directive.
- **Traditional Chinese only.** Uses 民國 calendar, zh-Hant localization strings, 繁體 orthography.

## Capitalization and Punctuation

- English: all lowercase for casual messages (`plan`, `ok`, `commit`, `continue`, `run validation step in doc update skill`)
- English: standard casing only when pasting plan blocks or spec content
- Chinese: standard punctuation (，。：「」); does NOT use Western punctuation in Chinese
- No trailing periods in short messages
- Double spaces occasionally appear in confirmations: "有了  修正了", "好了  你可以看 log"
- Hashtags in todo lists: `#todo`

## Emoji and Formatting

- **No emoji** in user messages (the agent uses them; the user never does)
- Uses backtick code blocks when pasting error output or code snippets
- References files with `@path/to/file.md` syntax (agent-specific reference notation)
- Numbered lists for multi-item feature specs
- Bullet dash lists for orchestration boilerplate

## Typo Patterns

- "uncommited" (missing 't') in `/simplify uncommited changes`
- "imeplementation" in `before imeplementation, gather proper context`
- "theshold" in `把靈敏度的 theshold 整體都上調看看`
- "scollbar" in `cursor card 的 border 擠壓到邊界的 scollbar`
- "優裂" (likely 優劣 — pros/cons) in `分析一下優裂`
- Occasional missing space before English words in Chinese sentences

## Verbatim Calibration Quotes

**Openings:**
1. `hi`
2. `今年是民國幾年？`
3. `/review-loop gemini`
4. `/doc-update README.md`
5. `macos app 怎麼做多語言？`

**Mid-session steering:**
6. `修正吧`
7. `直接動手改吧`
8. `先幫我取用 nickname 好了`
9. `不用寫 uuid 了`
10. `gridview scoll 改用 linear`
11. `0.6s`
12. `2`

**Pushback / corrections:**
13. `好像沒什麼差欸\n你幫我把靈敏度的 theshold 整體都上調看看`
14. `你現在這樣改，原本那個在邊緣要再多滑一次的鎖就沒了。\n\n目前是這個感覺：它現在滑到邊緣非常快，我可以直接滑到邊緣就自動換頁。`
15. `這真的很難寫嗎？`
16. `為什麼有時間限制？  你為什麼要停下來？`

**Failure reports:**
17. `還是沒好`
18. `結果還是一樣`
19. `我測試完全沒解決？`
20. `現在 trackpad 換頁的動量鎖幾乎沒有了？\n我很容易一換頁就滑到下一頁的底部`
