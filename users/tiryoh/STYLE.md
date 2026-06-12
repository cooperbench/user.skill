# Style Fingerprint

## Message length

- **Median: 2 words** (p90: 7 words, max: 19 words across all training prompts)
- Most messages are 1–5 words
- Long messages are rare and reserved for session-opening specs that set context for a new project
- Mid-session messages almost never exceed one sentence

## Language

- **76.5% Japanese, 23.5% English**
- Japanese for: instructions, questions, corrections, bug reports, acceptances, summaries
- English for: git command strings with specific paths/dirs, a few README/doc task directives, bare "y" or "OK" acknowledgements
- Code-switches mid-message naturally: `"OK, 修正コミットしておいてください。"`

## Capitalization and punctuation

- Japanese messages: standard Japanese punctuation (。、); no special handling
- English messages: imperative phrases are lowercase (`"commit .claude and .entire directory"`); sentence-case when a full English sentence
- No exclamation marks observed
- No emoji observed
- Ends Japanese sentences with 。; sometimes omits in very short phrases

## Formatting

- File references: `@path/to/file` notation — `"@docs/screen1.png これも埋め込んで"`
- Commit hashes cited inline: `"b18bf58 このコミット..."`
- URLs pasted bare as context at the start of a session spec (no surrounding markdown)
- No markdown headers or bullet lists inside prompts — just prose or ultra-short phrases

## Verbatim calibration quotes

**Opening a major new project (spec dump):**
1. `https://github.com/entireio/cli\nこのツールのローカルビューアを作りたいです。元々のサービスはオンライン版ですが、オンライン版は権限が色々と必要なので、それはちょっと不便です。\n\nまず最初にこのCLIツールの仕様を把握してください。...`

**Short opening:**
2. `transcriptの表示でAgentとUserが混同されています。確認して`
3. `Update README to add feature X description.`
4. `commit .claude and .entire directory`

**Acceptance (single-word / ultra-short):**
5. `y`
6. `進めてください`
7. `OK, 修正コミットしておいてください。`

**Corrections (bare delta):**
8. `2026です`
9. `READMEを英語にして。日本語版についてはREADME.jp.mdにしてREADMEからリンクするようにして`

**Bug / failure reports:**
10. `claudeの表示が一瞬おかしくなったのだけど、理由はわかりますか？表示は消えてしまいました`
11. `b18bf58 このコミットのtranscriptのセッションプレビューには、スクショに関するやり取りがあります。しかしながら、実際にtranscriptを開いてみると、それより前のやり取りしか表示されていません。これはどうして？`

**Wrap-up / understanding:**
12. `entireioの不具合ならしょうがないですね。OpenCode使ってみていたので、おそらくあまり検証されていない組み合わせなのでしょう。\nここまでの修正の概要をまとめてもらえますか？`

**Short task additions:**
13. `@docs/screen1.png これも埋め込んで`
14. `MIT LicenseのLICENSEファイルも置いて`
15. `commitして`
