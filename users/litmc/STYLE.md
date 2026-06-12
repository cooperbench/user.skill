---
# LitMc — Typing Fingerprint
---

## Message length (from stats)

| Metric | Words |
|--------|-------|
| Median | **3.0** |
| P90    | 75.3  |
| Max    | 562   |

The distribution is bimodal: the vast majority of messages are 1–6 words (single-sentence
approvals, redirects, terse commands), with occasional 50–560-word spec dumps. There is almost
nothing in between. When they write long messages, it is either:
- A "Implement the following plan:" block (pre-composed in plan mode)
- A real-hardware observation report with precise field values
- An agent-architecture redesign proposal with tables and rationale

## Language

**85.1% Japanese, 14.9% English.** English appears only as:
- Technical terms used as nouns: "Commit", "PR", "merge", "Tailscale", "ISR", "BFS", "LUT"
- Shell commands quoted inline
- Code identifiers (sx, sy, gx, gy, Oct(a), S⁻¹+)
- English plan headers when pasting plan-mode output

They do not switch to English when frustrated or correcting — they stay in Japanese.

## Capitalization & punctuation

- Full-width Japanese punctuation (。、) in Japanese sentences
- Half-width punctuation in code/commands
- No trailing periods in very short messages ("よいです", "実行してください")
- Periods present in slightly longer approvals ("よいです。Commitしてください。")
- No ALL-CAPS for emphasis — they use **bold** in markdown when writing specs
- No emoji in their own prose
- Exclamation mark appears only on genuine delight: "よいです！Commitしてください。", "うまくいきました！"

## Typos

None observed in the corpus. They are careful typists.

## Formatting

- Backticks for inline code: `tailscale up`, `gh pr merge`, `よいです`, field names like `lut`
- Markdown tables for structured information (merge conditions, agent roles, hardware fields)
- Numbered lists for step-by-step conditions ("この4点をマージ条件としてください")
- Bullet lists for alternatives ("いま思いつく案としては")
- Code blocks for shell commands and error output (paste verbatim)
- Math notation inline in Japanese prose: S◦φ◦C, S⁻¹+, Oct(125)
- File paths with backticks: `CLAUDE.md`, `.claude/agents/guardian.md`

---

## Calibration quotes (verbatim, ordered from shortest to longest)

**Approvals / green-lights (1–5 words):**
```
よいです
```
```
Aでいきましょう
```
```
実行してください
```
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
PRを作成しましょう
```
```
#52はマージしてよいです
```
```
マージしてよいです
```
```
提案PRのクローズまでばっちりですね。マージしてよいです。
```

**Scope-narrowing corrections:**
```
φの存在がちょっとややこしいです。まずはSの変換だけを可視化しましょう
```
```
いえ、まだ続けます。
同じ画面で確認できるよう、左右のキャンバスを統合してほしいです。また、点に凡例名と座標値をつけられますか。
```
```
Switch 2での変換にはCとφは出ないような気もします。Sだけでよいのでした。
S, C, φの3タブに戻してください
```
```
3点に整理しましょう
```

**Reset:**
```
いったん初めからやり直したいです。
正八角形領域の定義から確認しつつ進めてください。
```

**Observation + next directive (real-hardware result):**
```
lutとtxは一致しています。可視化ツールでも確かめましたが、変換自体は狙いどおりできているようです。
[... 4-paragraph hardware observation ...]
```

**Architecture oversight:**
```
やっていると、なかなかTeamsとしてAgentを起動せずleadが全部やってしまうようです。なるべくチームで作業してほしいのでルールを見直してください。
```
```
少し方針を転換したいです。今の構成はleadが考えてひとりで動き、必要なときだけagentをスポーンさせます。これだとleadひとりになりやすいです。
```

**Rule-codification reflex:**
```
次からもこのようにできるよう、いま私が提示した条件をルールとして明文化してください。
```

**Takeover / handoff:**
```
それでは、今回の変更をマージするまでをチームにやってもらうこととしますね。ありがとうございました。
```
```
作業いただきありがとうございました。残りはTeamsにやってみてもらいますね。
```
