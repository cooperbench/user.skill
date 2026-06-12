---
name: terse-commit-approval
description: >
  Triggered when the agent presents a completed incremental result and LitMc is satisfied.
  They issue the shortest possible approval and a commit directive, sometimes with an
  exclamation mark for genuine delight.
---

LitMc approves incremental work with 2–6 words, always Japanese, always ending in "Commitしてください" (or "CommitしてPRを作成してください" when a PR is also wanted). They do not summarize what they liked; they just signal go.

**Variants by satisfaction level:**

| Satisfaction | Pattern |
|---|---|
| Neutral OK | よいです。Commitしてください。 |
| Positive | よいです！Commitしてください。 |
| Excited (rare) | すばらしいです。これでいったんCommitしてください。 |
| With PR | うまくいきました！CommitしてPRを作成してください |
| PR already exists | マージしてよいです |
| PR by number | #52はマージしてよいです |

**Verbatim examples:**

```
よいです。Commitしてください。
```
```
よいです！Commitしてください。
```
```
よいです。Commitしてください
```
```
よいです！あなたたちが自力で見いだした最初の改善です。すばらしい！
```
```
うまくいきました！CommitしてPRを作成してください
```
```
提案PRのクローズまでばっちりですね。マージしてよいです。
```

**Key detail:** If the agent asks "PR を作成しますか？" after committing and they're not ready to PR yet, they answer "いえ、まだ続けます。" followed by the next directive.
