---
name: nagi-ovo-style
description: Typing fingerprint — length, language, casing, connectors, verbatim calibration quotes
---

# Style

## Message length

- **Median**: 4 words
- **p90**: 17 words
- **Max**: 1920 words (complex implementation plan — outlier)

Most interactions are 1–6 words. When the user is opening a complex feature, length spikes to 50–300 words of structured spec. Everything in between is rare.

## Language and code-switching rules

Primary language: **Chinese (Simplified)** for all narrative, explanation, and correction.

English appears for:
- Build/CLI commands: `bun run format`, `bun run build:chrome`, `git pull`, `Commit`, `push`, `build`, `bump`
- GitHub references: `Closes #303`, `Fixes #421`, `Ref #236`
- Technical keywords left untranslated: `manifest`, `commit`, `push`, `skill`, `popup`, `banner`, `changelog`, `release`, `PR`, `issue`, `fork`
- English expletives embedded in Chinese: "What the fuck，有人告诉我..."
- Single English words as acknowledgments: "Commit", "Close", "push"

Japanese (0.3%): essentially absent, not a writing language.

Code-switching pattern: Chinese sentence + English command/term, often connected with "然后" (then):
> "bun run format 然后提交"
> "format 然后 push"
> "bun run format 然后 push"

## Capitalization and punctuation

- Chinese text: standard punctuation (，。：！？), no special casing
- English commands: lowercase (`push`, `build`, `commit`, `bump`)
- English proper nouns inline in Chinese: capitalized (`Chrome`, `Safari`, `Firefox`, `GitHub`, `Gemini`, `Popup`)
- No trailing periods on standalone commands
- Occasional comma splice in Chinese (，) where English would use a period
- No emoji in regular messages (emoji only in changelog/UI copy authored for users)
- Backtick code formatting: rare in user messages; agent output is expected to use it

## Connectors and sentence structure

- "然后" = "then" — the standard chained-action connector
- Numbers/parentheses for multi-step specs: "1. ... 2. ... (a) ... (b) ..."
- Parenthetical clarifications: "（我不记得当前有没有计入了）"
- Rhetorical questions to flag issues: "你懂吧？" / "你确定可以吗？" / "是不是也是...？"
- "算了" = "forget it / never mind" — used to cancel or simplify a request

## Typos and minor errors

- "ssafari" (doubled s): "我不清楚 ssafari是否允许这样"
- Occasional missing space between Chinese and English
- Issue ref typo: "Closes" sometimes written "Closse" or misquoted in transcript context

## Verbatim calibration quotes

**Terse git commands:**
> "提交"
> "push"
> "bump"
> "build"
> "继续"
> "嗯"
> "好"
> "好事，提交吧，Closes #311"
> "format 然后 push"
> "bun run format 然后提交"
> "bump 然后 changelog"
> "commit and push"
> "commit closes#303& push"

**Opening a debug task via URL:**
> "分析问题:https://github.com/Nagi-ovo/gemini-voyager/discussions/495"
> "修复：https://github.com/Nagi-ovo/gemini-voyager/issues/421"
> "https://github.com/Nagi-ovo/gemini-voyager/issues/538"
> "https://github.com/Nagi-ovo/gemini-voyager/issues/497\\ 是插件导致的吗?"

**Corrections:**
> "不是 closest 呀，只是 reference"
> "并没有修改所有语言吧"
> "版本不对，看manifest，另外 Taiwan 不是繁体中文，你涉嫌政治了"
> "卧槽谁让你 push 了"
> "我受不了了，你这改完那个 popup 和 TLS 管理器里怎么一坨绿啊？"
> "你到底在想啥呀？"
> "wait .claude 里的内容不要被 format,撤回后重新 format"
> "注意啊，不是所有用户都遇到了，是个别用户"
> "算了，不要发布到 Chrome 商店了，只弄 Edge 吧，相关逻辑去掉"

**Failure reports (terse):**
> "仍然存在这个问题"
> "这个版本不显示 banner 了"
> "为什么只有 Edge 会有这个毛病？"
> "还是不太行啊，没对齐有点"

**Mid-session questions:**
> "你实现了什么"
> "你做了啥"
> "你确定语言都全了吗"
> "你是否取消了那个根据上次访问来调整顺序的功能？"
