---
name: 135yshr-style
description: Typing fingerprint — message lengths, languages, casing, quotes — for 135yshr
metadata:
  type: user
---

## Message length

- **Median: 3 words** — the statistical center of mass is a terse Japanese or English fragment
- **P90: 302 words, max: 335 words** — the upper tail is plan/spec dumps pasted verbatim from slash commands
- Distribution is sharply bimodal: short steers vs. full plan dumps; almost nothing in the 30–100 word range in user-typed messages

## Languages

- **Japanese 49 %, English 51 %** by prompt count
- Japanese dominates: conversational steers, short confirmations, corrections, publishing decisions
- English appears almost exclusively inside pasted slash-command output (`# Smart Commit with Gitmoji…`, `Implement the following plan:`, `/review-doc` blocks) — these are not user-composed prose
- Code-switching rule: the user types in Japanese; English appears only in pasted agent-generated blocks

## Capitalization and punctuation

- Japanese messages: standard Japanese punctuation (。、), no trailing periods for one-liner English fragments
- English in user-written Japanese sentences: minimal; uses half-width for code/tool names (`npm run lint`, `textlint`, `published: false`)
- No emojis in user-typed text; emojis in corrections are copied from external review output

## Formatting

- Short messages: plain prose, no markdown
- Corrections: Markdown headers (`##`, `###`), tables, fenced code blocks — but only when pasting external review output
- File references: backtick paths inline (`` `articles/978121945958ed.md` ``) or `@articles/` mention syntax
- Line numbers referenced as `L127-132`, `L21`

## Verbatim calibration quotes

### Openings (terse)
1. `次に公開すると良い資料を教えてください`
2. `過去に公開した記事の順番を踏まえて今日公開すると良い記事を選定してください`
3. `#14の記事を作成してください`
4. `issue を確認してください`
5. `AI生成コードはなぜ追跡できないのかを公開してください`

### Steers and short redirects
6. `追記してください`
7. `修正に着手してください`
8. `はい`
9. `1`
10. `おすすめの記事を公開してください`
11. `issueに登録してください`
12. `create pr`

### Corrections
13. `ごめんなさい。僕ではなく私にしてください`
14. `文章をですます調に変更してください`
15. `修正が間違えています。\nですます口調に修正することが目的です。\n読み手は目うめの人の可能性もあるのです。\n経緯を書く文章はやめてください`
16. `2回では発生しない可能性があるので、複数回にした方が良いと思いました`
17. `よくある反論への回答だとちょっと言葉が強めなのでもう少し柔らかい表現に変更してください`
18. `自作トランスパイラ（Go で書かれたコード生成ツール）となってしますが、meow のことを書いても良いです`

### Topic queries
19. `次の記事を作成しようと思いますが、DDDやクリーンアーキテクチャーの記事で良さそうなものを書きたいです。\nどんなテーマが良いと思いますか？`
20. `今日、公開するのに良い記事はどれだと思いますか？`
