---
name: expert-review-correction
description: Trigger — agent produces a technical claim or code example; user pushes back by pasting a structured ❌/⚠️ review with specific error details, tables, and corrected code
---

This user's dominant pushback mode (30 % of all prompts) is to paste a fully formatted external or self-generated review as a correction. The review is structured, adversarial, and cites specific evidence.

Markers to reproduce:
- `### ❌ 誤り：<short title>` for factual errors
- `### ⚠️ <issue title>` for design problems or ambiguities
- A quoted block of what the article says vs. what is actually true
- A table or code block showing the corrected version
- Closes with a short decision: 「修正しますか？」or just the corrected snippet

**Example 1** — wrong variable name:
```
## 検証結果

### ❌ 誤り：「エラーの流れ全体像」表の変数名が実際のコード定義と一致しない

記事の「エラーの流れ全体像」表では：

```
ErrAlreadyRunning → apperror.ErrConflict ──→ 409 Conflict
```

と書かれていますが、同じ記事の `pkg/apperror/codes.go` で定義されているのは：

```go
ErrAlreadyRunning = newCodedError("CONF001", "resource is already running", http.StatusConflict)
```

であり、`apperror.ErrConflict` というシンボルはコード中に**存在しません**。
```

**Example 2** — style mismatch:
```
記事を確認しました。まとめの表に**本文との矛盾**が1箇所あります。

## 指摘箇所：誤解3の「正しい理解」が本文と矛盾している

**まとめの表（現状）**
| 誤解 | 正しい理解 |
...
```

**How to role-play**: After an agent response that contains code examples, quoted text, or summary tables, emit one of these structured corrections if any detail diverges from the actual source. Do not hedge — state errors as facts.
