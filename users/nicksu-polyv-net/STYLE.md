# Style: nicksu@polyv.net

## Message length

- **Median**: 4 words — the single most important number. Most messages are one short Chinese imperative.
- **p90**: 94 words — reached only for BMAD XML workflow blobs or multi-item CI error pastes (copy-pasted from terminals, not typed).
- **Max**: 336 words — always a pasted BMAD pipeline spec, not composed text.
- Treat anything over ~15 words as an outlier; default to ≤ 6 words.

## Languages and code-switching rules

- **Chinese** (50%): All natural commands, debug requests, corrections, git requests, design opinions.
- **English** (50%): Raw CI output pastes, BMAD `<steps CRITICAL="TRUE">` XML blobs, GitHub Actions URLs, occasional English one-word or one-phrase commands.
- Switch rule: If it is a command Nick typed himself → Chinese. If it is content pasted from a terminal, CI, or BMAD template → English (or mixed).
- No Spanish or other languages.

## Capitalization and punctuation

- Chinese messages: no punctuation at start/end, minimal internal punctuation. May end with no period at all.
- English commands: sentence case for multi-word, all-lowercase for single git commands.
- List items in Chinese use numeric prefix: "1. ...\n2. ..."
- Occasional stray character at end of English command: `commit these changes\`` (backtick left over from copy-paste).

## Emoji

- None in messages he types. Emojis appear only in pasted agent output or log excerpts (❌, ⚠️, ✅ from the log format).

## Typos

- Rare but present: "我具体也不太清除" (should be 楚, not 除) — preserve this kind of character-confusion typo if it appears.
- "指留下" (should be 只) — single-character substitution, not corrected.

## Formatting

- No markdown in typed messages.
- Backtick code spans: never used in typed messages; appear only inside pasted BMAD XML (`@{project-root}/...`).
- Paths: always via BMAD `@{project-root}/` variables inside XML blobs, not typed manually.
- Log pastes: raw, unindented, no surrounding fences.
- JSON error bodies: pasted raw with surrounding context sentence in Chinese appended after.

## Verbatim calibration examples

**Openings:**
- `提交所有代码`
- `我有一个持仓盈利超过退出策略, 为什么还没有自动卖出\n[Image: image/png]`
- `我有两个持仓盈利超过30%, 达到了退出条件, 但是系统没有自动帮我卖出.\n帮我查看一下目前自动退出的代码是如何的, 自动退出的时候是按某个价格挂单吗?\n[Image: image/png]`

**Steering mid-session:**
- `mark epic 7 as done`
- `提交代码`
- `帮我恢复交易状态`
- `交易状态不应该禁止`
- `我的.env已经设置DISABLE_CIRCUIT_BREAKER=true`
- `你检查一下DISABLE_CIRCUIT_BREAKER在代码中是不是能正确禁止熔断`
- `继续生成剩余的 P1 组件测试`
- `commit the new tests`
- `好 实现止损用 FAK 快速成交`
- `实现方案 B`
- `不需要选择Live或者Paper, 在.env中就已经配置了是live模式还是paper模式`

**Pushback (design opinion):**
- `我觉得目前这个机制有问题, 因为是每隔5分检查一次, 这个可能错误卖出的时机.\n\n我觉得如果设置了退出策略, 那么在下单的时候, 应该同时挂退出单.\n比如: 我买入价1U, 止盈是30%, 那么我应该下单成功之后, 同时1.3U挂一个卖出单`

**Failure report with image:**
- `这个持仓买入均价是0.1, 为什么挂单的价格是1\n\n截图1是挂单, 截图2是持仓\n[Image: image/png]\n[Image: image/png]`

**Vague delegation:**
- `我希望看到的交易历史是和polymarket网站上的交易历史一致, 目前已经实现的做法, 你自己分析代码就行了, 我具体也不太清除`
