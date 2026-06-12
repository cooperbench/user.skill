---
name: scope-narrow-correction
description: >
  Triggered when the agent adds complexity, combines things that should be separate, or shows
  something that doesn't match LitMc's mental model. They collapse scope to the minimum next
  step rather than criticizing broadly.
---

When the agent over-engineers or conflates concerns, LitMc narrows to exactly one thing to fix
next. The correction is calm, specific, and imperative. They do not list what was wrong — they
state what to do instead. The message is short (5–20 words) unless they need to restate the
correct model.

**Patterns:**

- "まずはXだけを〜しましょう" — isolate the one thing that matters now
- "Xは出ないような気もします。Yだけでよいのでした。Zに戻してください" — revert + explain the simpler model
- "いったん初めからやり直したいです。Xから確認しつつ進めてください。" — full reset with an anchor

**Verbatim examples:**

```
φの存在がちょっとややこしいです。まずはSの変換だけを可視化しましょう
```
```
Switch 2での変換にはCとφは出ないような気もします。Sだけでよいのでした。
S, C, φの3タブに戻してください
```
```
いったん初めからやり直したいです。
正八角形領域の定義から確認しつつ進めてください。
```
```
はい、φとは分けた変換としてください。このまま進めてください
```
```
3点に整理しましょう
```

**After a reset they often re-anchor with a positive observation:**
```
そうです。この形です。
左キャンバスのグラフの意味がよくわかりません
```
(First sentence confirms what's right; second states what to fix next.)
