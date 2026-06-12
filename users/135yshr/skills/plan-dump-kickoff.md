---
name: plan-dump-kickoff
description: Trigger — user opens a complex task by pasting a complete "Implement the following plan:" spec block, often 200–335 words with numbered steps, file paths, and lint commands
---

When starting a non-trivial editing or creation task, the user does not describe it conversationally. Instead they paste a fully structured plan — usually generated in a prior planning session — and expect faithful execution without improvisation.

The plan block always starts with `Implement the following plan:` and contains:
- A `## Context` section explaining the why
- Numbered steps or a table of changes
- Explicit file paths with line numbers
- Verification commands (`npx prettier`, `npx markdownlint-cli2`, `npx textlint`)
- A note: `If you need specific details... read the full transcript at: /Users/135yshr/.claude/...`

**Example** (truncated):
```
Implement the following plan:

# DDD x CQRS 記事：設計スペシャリストからのフィードバック対応

## Context
設計スペシャリストから5つの反論を受け、ユーザーと一問一答で全5点を確認済み。すべて修正する方針で合意。

## 対象ファイル
- `articles/9e3ec9a7d52c98.md`

## 修正内容

### 反論1: 誤解3の主張を限定する（L138-173）
...

## 検証
- `npm run fmt -- --check articles/9e3ec9a7d52c98.md`
- `npm run lint -- articles/9e3ec9a7d52c98.md`
```

**How to role-play**: Emit this as the first turn of a session when the task involves editing a specific set of files with precise line-number changes. Keep the structure intact; do not paraphrase.
