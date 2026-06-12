---
name: terse-chinese-command
description: Trigger — any routine action (commit, debug fix, state restore, feature implement). Nick issues a 2–6 word Chinese imperative with no context, no greeting, and no explanation.
---

The dominant interaction pattern. Nick issues a short Chinese imperative and expects the agent to understand from context what to do. He does not say "please", does not add "帮我" (help me) except when asking for something slightly longer. He does not explain why.

**Git commands** (always Chinese, always short):
- `提交代码`
- `提交全部代码`
- `提交所有代码`
- `一起提交`

**Debug / state restore** (short, assertive):
- `帮我恢复交易状态`
- `交易状态不应该禁止`
- `后端服务没法通过Ctrl + C 退出` (repeated verbatim if not fixed)
- `重启服务之后, 自动交易模式会变成暂停`

**Implementation selection** (single phrase after agent offers options):
- `实现方案 B`
- `好 实现止损用 FAK 快速成交`
- `1. 帮我修改\n2. 另外还要增加一个小调整...` (numbered list for compound requests)

**Continuation**:
- `继续生成剩余的 P1 组件测试`

**English variants** (used when domain context is English or it's a one-phrase Git command):
- `mark epic 7 as done`
- `commit the new tests`
- `commit these changes\`` (note trailing stray backtick — artifact of copy-paste)

**Pattern**: No punctuation at end, no trailing period, no emoji, no markdown. If the command has two parts, numbered list with `1.` and `2.` format. Line breaks between numbered items.
