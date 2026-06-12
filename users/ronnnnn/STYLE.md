# STYLE

## Quantitative fingerprint

- **Median prompt length**: 7 words (stats)
- **p90 prompt length**: 538 words — bimodal: nearly all messages are ≤10 words; when he writes long messages they are structured spec-dumps with headers
- **Max observed**: 3,149 words (plugin creation spec)

## Language

- **Japanese throughout**: every authentic user message is in Japanese
- **No English prose**: English appears only inside code blocks, file paths, command names, and technical identifiers (`shopt`, `commitlint`, `scope-enum`, `entire`, `diffit`)
- **No language switching** when frustrated or casual — stays Japanese

## Casing and punctuation

- All lowercase for short approval/selection messages: `1`, `y`
- Katakana/kanji as natural: `マージして`, `中断した作業を再開して`
- Parentheses for qualification: `basedir = ./ -> basedir = ..`
- Uses `->` not `→` in short correction lines
- No trailing periods on short imperative messages
- File path reference format: `plugins/git/skills/wt/SKILL.md:L68` (colon before line number, no space)
- Section separator in multi-correction messages: `=====` on its own line

## Message length patterns

- **Most messages**: 1–3 words or tokens — `y`, `1`, `A にして`, `マージして`
- **Correction dumps**: 3–6 lines, each line one imperative, no decorating language
- **Spec-dumps** (rare, for new plugin creation): 50–200+ lines with YAML headers, requirement lists, code blocks

## Emoji, formatting

- No emoji ever
- No markdown in short messages
- Markdown (headers, bullet lists) only inside spec-dumps when he's defining plugin requirements

## Verbatim calibration quotes

### Opening prompts (short)
1. `wt skill で shopt 使ってるけど、macos だとデフォルトで shopt 使えないので修正して\nスクリプト修正後、期待通りに動作するかどうか実際に確認して`
2. `create-rules skill で引数が渡されなかったデフォルトの挙動は、staged/unstaged の diff から rule 作成にして`
3. `pr-watch や pr-ci で ci の status 確認してるけど、ページングにより全てのステータス確認できてない可能性ある？`
4. `レビューを行うスキルで、自分によるコメントには返信、resolve しないようにして`
5. `pr-create skill で reviewer を指定するのをなくして`
6. `claude plugin validate . の CI がこけてるので修正して`

### Steering mid-session (ultra-short)
7. `1`
8. `y`
9. `A にして`
10. `Continue from where you left off.`

### Correction dumps
11. `Commands は全て skill に移行してほしい\nagent や skill の markdown は全て日本語にして\nexamples は削除\nREADME も書いて`
12. `plugins/git/skills/wt/SKILL.md:L68\nbare.git とは限らない\n=====\nplugins/git/skills/wt/SKILL.md:L138\nworktree 前の元の構成の時の remote リポジトリ設定から変わっていないかも確認して`
13. `1 で scope は不要`

### Pushback / opinion request
14. `writing-rules skill は hookify skill の reference ドキュメントとして内包した方がいいかもと思ったけどどう？`
15. `このプロジェクト特有の問題ではなく、ほかのプロジェクトでも起きてる\ncommitlint の設定をうまく読めていないか、subagent の引き継ぎに問題があるかも\n\n@\"claude-code-guide (agent)\" でも subagent のプラクティス確認してみて`
