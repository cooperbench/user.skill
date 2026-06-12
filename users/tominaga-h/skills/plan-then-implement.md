---
name: plan-then-implement
description: After the agent proposes a plan and Hayato approves it, he triggers implementation with a fixed bilingual boilerplate message (Japanese title + English execution paragraph). Trigger when agent has proposed a plan and Hayato is ready to proceed.
---

## Behavior

Hayato never lets the agent implement without a plan. Once the plan is ready and approved, he sends a message in two parts:

1. A short Japanese title summarizing what will be implemented (1 line, no punctuation or period).
2. A fixed English paragraph (verbatim, copy-pasted every time) telling the agent to execute without editing the plan file and to use pre-created to-dos.

If the agent tries to implement before a plan exists, Hayato redirects with:
> `修正プランを構築して`
or the more detailed version:
> `修正プランを構築して。\nまた \`ls\` の結果には該当ファイルがあるのに…`

## Verbatim examples

**Example 1** (session ID fix):
```
セッション ID によるログ識別とコマンド履歴分離

Implement the plan as specified, it is attached for your reference. Do NOT edit the plan file itself.

To-do's from the plan have already been created. Do not create them again. Mark them as in_progress as you work, starting with the first one. Don't stop until you have completed all the to-dos.
```

**Example 2** (git push completion):
```
git push 時にカレントブランチを初期補完する

Implement the plan as specified, it is attached for your reference. Do NOT edit the plan file itself.

To-do's from the plan have already been created. Do not create them again. Mark them as in_progress as you work, starting with the first one. Don't stop until you have completed all the to-dos.
```

**Example 3** (plan redirect):
```
修正プランを構築して
```
