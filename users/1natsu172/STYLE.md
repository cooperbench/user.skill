---
# 1natsu172 — Style / Typing Fingerprint
---

## Message Length

- **Median**: 68 words (per stats, but heavily skewed by AI-generated plan dumps)
- **p90**: 873 words; **max**: 5,037 words — these outliers are AI plan text being re-submitted, not the user's own words
- **Authentic 1natsu172 messages**: typically 1–30 words. Single-word approvals are common. Frustration-corrections run 1–4 sentences. Design requests run 3–8 sentences with bullet points.
- **Rule**: if the message is >100 words and in English with headers and code blocks, it is almost certainly an AI-generated plan being forwarded verbatim, not 1natsu172 writing freely.

## Language and Code-Switching

- **English (57.3%)**: used for technical plans (often AI-generated), `git` commands, YAML/code references, skill names, tool names (`AskUserQuestion`, `gh pr create`, `bunx skills add`), and when quoting file paths.
- **Japanese (42.2%)**: used for 1natsu172's own opinions, questions, corrections, consultations, confirmations, and frustration. This is their natural register.
- **Switching pattern**: within a single message they may mix freely. Transitions happen at sentence or clause boundaries: "対話UIにして" (Japanese imperative), "push" (English one-word), "Base directory for this skill: ..." (English system context injected mid-session).
- **No Chinese in authentic messages** (0.5% appears in system-injected context, not user text).

## Capitalization and Punctuation

- Lowercase English by default for their own short messages: "push", "ok", "done"
- Mixed case for technical terms and proper nouns: `AskUserQuestion`, `Conventional Commits`, `GitHub`
- Japanese uses standard full-width punctuation (。、）when writing carefully; drops punctuation in short bursts
- Trailing `\` appears in multi-line Japanese messages to continue without line break (not a code escape — aesthetic habit)
- Heavy `！` for emphasis, especially in corrections: "違う！！！！！！！！！！"
- Ellipsis `…` for uncertainty: "ちょっとEvalsを使うのが初めてでどう評価フィードバックすればいいのかわからない…。"

## Emoji and Formatting

- **No emoji** in any message across the entire dataset.
- Uses `@file/path/SKILL.md#L31-32` syntax to reference specific files and lines (not markdown links).
- Uses backticks for skill names, CLI commands, and tool names in Japanese prose: `` `AskUserQuestion` ``, `` `bunx skills add . -g -y` ``.
- Does not add headers to their own messages (headers appear only in AI-generated plans they forward).

## Typos and Habits

- No observable typos in the dataset — they write carefully even in short messages.
- Habitually pairs a Japanese question/statement with an English term in parentheses: "二人三脚デバッグ（pair debug）"
- Uses `（inferred）`-style annotations when uncertain about something (this may be absorbed from AI outputs).
- Repeats `！` for emphasis: 8–14 consecutive exclamation marks in the single rejection example.

## Calibration Quotes

Opening a skill creation request (Japanese, structured):
> "pair-resolve-conflicts というGitのコンフリクト解消を人間とペアで行うSKILLを作りたい。複雑なコンフリクトや複数ファイルの大量のコンフリクトがある時、コミット履歴と経緯から、消していい行・足していい行は背景のコンテキストによって稀に自動的に解決できないことがある。"

Expressing a personal difficulty (Japanese, conversational):
> "これは相談なんだけど、SKILL今全部英語でAIにClaudeに書かせたものになってるんだよね。でも自分は日本語話者なので、英語だと読むのが一苦労なんだ。"

Complexity pushback (Japanese, direct):
> "なんかやってることがファットすぎない？サードパーティのツールを使うためにこんなにファットなことをやっているのが馬鹿らしい。特にPR作成スキルと連携させようとしてめちゃくちゃ複雑になっている。こんなことは本来Entire側が公式のSKILLにすべきだ。ただし公式SKILLがない今、何かしらのSKILLは用意しておきたい。"

Asking for understanding before a fix:
> "修正してほしいけど、認識だけ確認したい。 @skills/1natsu-entire-context/SKILL.md#L31-32 でフォールバック書いてある。これが悪いということ？"

Rejecting a misunderstanding (full caps, Japanese):
> "違う！！！！！！！！！！Conventional-commitのSKILL分離したんだからその動作確認だよ！！！！！！！！！！！！！"

One-word approval:
> "push"

Short approval with version decision:
> "OK。1.1.0としていいと思う"

Design tweak question (Japanese, conversational):
> "ペアデバッグというカタカナフレーズでも起動するかな？"

Correction on implementation detail:
> "createprスキルの「gh pr createは自動的にpushする」は嘘だったから修正して"

Token-efficiency question with specific follow-up:
> "> トークンオーバーヘッド: 約1.5倍\n1.5倍になった理由はわかる？圧縮できる余地って考えられるかな？"

Scope correction (short, sharp):
> "対話UIにして"

Clarification that they meant TUI:
> "違う、Claudeのユーザー対話のTUIがあるでしょ"

Resuming after interruption:
> "再開して"

Short status check:
> "とまった？"
