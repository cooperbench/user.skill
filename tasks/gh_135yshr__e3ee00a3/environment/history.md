> DEVELOPER

次に作成すると良いドキュメントを教えてください

> TOOL

tool_use Bash
id: toolu_01SK4sQ3kZdj6sjsXZNEGTmY
```json
{
  "command": "ls articles/ && echo \"---\" && git log --oneline -20",
  "description": "List articles and recent commits"
}
```

> TOOL

tool_result
id: toolu_01SK4sQ3kZdj6sjsXZNEGTmY
```
05db71175c4746.md
1820de942cca32.md
1b7eb1a3fc3787.md
21b1fa2c9365cc.md
24d20a2df05e30.md
3d95f47f3d2974.md
4076334bb8cb54.md
4415a24c8a2820.md
499cd6335b5fa6.md
4afd548d07480a.md
56e161aff29ff9.md
583ecabd270e4b.md
5de289f64ec515.md
5ffc0f6a7251e4.md
60d7d006c0f38f.md
78e3eb0a2a275a.md
7c5d99d5f45ed7.md
7d2428cbcd258d.md
808fbfe6b7db3d.md
8471b2d4bdc9d3.md
860e12b4a2698a.md
8d2e5d90eafe05.md
92042eacfbdde3.md
978121945958ed.md
98473f8e119657.md
9e3ec9a7d52c98.md
9eca22f9322c40.md
b32070e6b12a01.md
c05cf4efcc591f.md
c10431f5afd26d.md
d27112edbad1fc.md
f14c01658cd157.md
f2027369b648cc.md
f21a35a0d5bbcb.md
f757ebaf058ccd.md
fda3ceeeeb764f.md
---
a2060af DDD×CQRS認可設計記事のレビュー改善 (#97)
1112f24 🎨 format: fix CodeRabbit review comments
24ea69b 🚀 docs: publish CQRS authorization design article
c19f2aa 🎨 format: fix Go naming conventions in code examples
055b12b 📝 docs: clarify intentional rule change from membership to role-based auth
ce808be 📝 docs: review and improve CQRS authorization design article
9f348d7 md2pdf CLIツール紹介記事を追加 (#96)
0d0865f 📝 docs: add md2pdf CLI tool introduction article
d7635d1 DDDの入力バリデーション設計記事を公開 (#95)
18b7171 🚀 Publish validation design article
7d8d461 📝 Align validation article with DDD series conventions
451bb9a 📝 Fix review: improve code consistency and architecture references
faeffc5 📝 Fix evidence gaps and source attribution in validation article
cd9f69d 📝 Fix review: correct inaccuracies in validation article
a6f37da Set article as published
87de2a7 Set article published status to false
189ac58 Claude Code 環境最適化ガイド記事の追加とイベントソーシング記事の改善 (#94)
34a8bc6 📝 Fix CodeRabbit review: replace 筆者 with 私
e4c56e2 🐛 Fix :::message blocks collapsed by Prettier
d7ddf66 🎨 Use Zenn :::message notation for callout blocks
```

> TOOL

tool_use Bash
id: toolu_01E8wkMrZ7JUejFxTVF19TPb
```json
{
  "command": "for f in articles/*.md; do head -8 \"$f\" | grep -E \"^(title|topics|type|published):\" | tr '\\n' ' '; echo \" | $f\"; done",
  "description": "Extract frontmatter from all articles"
}
```

> TOOL

tool_result
id: toolu_01E8wkMrZ7JUejFxTVF19TPb
```
title: "Claude Code の作業環境を体系的に見直す実践ガイド" type: "tech" topics: ["ClaudeCode", "AI", "開発効率化", "プロンプトエンジニアリング"] published: true  | articles/05db71175c4746.md
title: "LLMをドメインエキスパートとして使う〜ユビキタス言語の整理にAIを活用する〜" type: "tech" topics: ["Go", "DDD", "AI", "LLM", "ユビキタス言語"] published: false  | articles/1820de942cca32.md
title: "macOS + iTerm2 + tmux + tmuxinator で Claude Code 開発環境を構築する" type: "tech" topics: ["tmux", "tmuxinator", "iterm2", "macos", "claudecode"] published: false  | articles/1b7eb1a3fc3787.md
title: "猫に関連する言葉でプログラミングできる言語「meow」を作った" type: "tech" topics: ["Go", "自作言語", "プログラミング言語", "コンパイラ"] published: false  | articles/21b1fa2c9365cc.md
title: "MarkdownをPDFに変換するCLIツール md2pdf を作った" type: "tech" topics: ["Go", "Markdown", "PDF", "Mermaid", "CLI"] published: true  | articles/24d20a2df05e30.md
title: "" type: "tech" # tech: 技術記事 / idea: アイデア topics: [] published: false  | articles/3d95f47f3d2974.md
title: "脆弱性レビューで「安全」と判断できた2つのケースと多層防御の話" type: "tech" topics: ["security", "go"] published: true  | articles/4076334bb8cb54.md
title: "コンテキストマップを描いてからコードを書く〜戦略的DDDのすすめ〜" type: "tech" topics: ["Go", "DDD", "ContextMap", "戦略的DDD", "設計"] published: true  | articles/4415a24c8a2820.md
title: "GitHubのPRテンプレートを0から作る方法" type: "tech" topics: ["GitHub", "PullRequest", "Template", "VibeCoding"] published: true  | articles/499cd6335b5fa6.md
title: "Goの非公開フィールドで集約の不変条件を守る設計パターン" type: "tech" topics: ["Go", "DDD", "集約", "設計", "アーキテクチャ"] published: true  | articles/4afd548d07480a.md
title: "Go × DDDのエラーハンドリング設計〜ドメインエラーとインフラエラーを分離する〜" type: "tech" topics: ["Go", "DDD", "エラーハンドリング", "CleanArchitecture", "設計"] published: true  | articles/56e161aff29ff9.md
title: "AIが生成したDDDコードをどうレビューするか" type: "tech" topics: ["Go", "DDD", "AI", "CodeReview", "LLM"] published: false  | articles/583ecabd270e4b.md
title: "UseCase層は本当に必要か〜Goでのクリーンアーキテクチャ最小構成〜" type: "tech" topics: ["Go", "CleanArchitecture", "DDD", "設計", "アーキテクチャ"] published: true  | articles/5de289f64ec515.md
title: "イベントソーシングをGoで実装したら「applyの意味」を完全に誤解していた" […]

> TOOL

tool_use Read
id: toolu_01HpeKcYCTWZHXbz4CZJVdvt
```json
{
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/3d95f47f3d2974.md"
}
```

> TOOL

tool_result
id: toolu_01HpeKcYCTWZHXbz4CZJVdvt
```
1	---
2	title: ""
3	emoji: "👌"
4	type: "tech" # tech: 技術記事 / idea: アイデア
5	topics: []
6	published: false
7	---
8	---
9	title: "Claude Code のステータスラインに残り利用枠を表示する"
10	emoji: "📊"
11	type: "tech"
12	topics: ["claudecode", "bash", "shell", "macos", "anthropic"]
13	published: false
14	---
15	
16	## はじめに
17	
18	Claude Code を使っていると、「あと何時間でリセットされるんだっけ？」「今どれくらい枠を使ったんだろう？」と気になる瞬間が何度もあります。そのたびに `/usage` コマンドを叩くのは地味に面倒です。
19	
20	この記事では、**Claude Code のステータスライン (画面下部に常時表示される行) に、5 時間ウィンドウと 7 日間ウィンドウの残量とリセット時刻を表示する方法** を、自作シェルスクリプトで実現する手順を紹介します。
21	
22	完成形はこんな見た目になります。
23	
24	```
25	🤖 Opus 4.7 │ 📊 12.3k/200k ██░░░░░░░░ 6% │ 5h: 🟢残72% (↻2.3h @14:30) │ 7d: 🟡残48% (↻3.2d @04/22 09:00) │ 💰$1.25
26	```
27	
28	左から順に、使っているモデル、コンテキストウィンドウの消費量、5 時間ウィンドウの残量とリセット時刻、7 日間ウィンドウの残量とリセット時刻、そしてセッションのコストが並びます。
29	
30	対象環境は macOS です。Keychain コマンドや `date -r` など macOS 固有のコマンドを使っています。
31	
32	:::message alert
33	この記事で使う `/api/oauth/usage` は Claude Code 内部で使われている **非公開のエンドポイント** です。仕様が予告なく変更される可能性があります。本記事の内容は執筆時点 (2026 年 4 月) のものであり、動作を保証するものではありません。自己責任でご利用ください。
34	:::
35	
36	## ステータスラインとは
37	
38	Claude Code には、ターミナルの下部に任意の情報を常時表示できる `statusLine` という仕組みがあります。`~/.claude/settings.json` にコマンドを登録しておくと、Claude Code がそのコマンドを定期的に実行し、標準出力された文字列をステータスラインとして表示してくれます。
39	
40	設定はこんな形です。
41	
42	```json
43	{
44	  "statusLine": {
45	    "type": "command",
46	    "command": "bash ~/.claude/statusline.sh"
47	  }
48	}
49	```
50	
51	コマンドには JSON が標準入力で渡され、そこにはモデル名やコンテキスト使用量、セッションコストなどの情報が含まれています。シェルスクリプトでもこの JSON を `jq` で解析すれば、好きな形式でステータスラインを組み立てられます。
52	
53	## なぜ自作が必要なのか
54	
55	Claude Code がステータスラインスクリプトに渡してくれる JSON には、実は […]

> AGENT

リポジトリ内の既存記事（公開済み 25 本、下書き 10 本）と直近のシリーズの流れを踏まえて、優先度の高いものを 3 つ提案します。

## 推奨する次の記事

### 1.  **DDD × CQRS のリードモデル設計 〜プロジェクションと結果整合性〜**（最有力）

直近で書いた認可設計（`60d7d006c0f38f.md`）と CQRS 導入前の記事（`9e3ec9a7d52c98.md`）の自然な続編です。シリーズで「コマンド側」「認可」までは整備済みですが、**読み取り側（クエリ／リードモデル）の作り方と結果整合性の扱い** がまだ抜けています。ここを書くと CQRS シリーズが綺麗に閉じます。

扱える内容の例：
- 書き込みモデルからプロジェクションを生成する 3 パターン（同期 / 非同期 / オンデマンド）
- リードモデルをドメイン層に置かない理由
- 結果整合性のレイテンシをどう UX で吸収するか（read-your-writes など）
- イベントソーシング記事（`5ffc0f6a7251e4.md`）との接続

### 2.  **DDD 連載のロードマップ記事（目次・読み順ガイド）**

公開済みの DDD 関連記事が 15 本前後あり、読者が「どの順で読めばいいか」を迷う段階に来ています。**戦略的 DDD → 戦術的 DDD → アーキテクチャ → 高度なパターン（CQRS / ES / ACL）** の流れに沿って、既存記事をまとめる目次記事を 1 本書くと回遊性が大きく上がります。新規執筆量が少なく、ROI が高いです。

### 3.  **Claude Code の hooks 活用パターン集**

`05db71175c4746.md`（環境を体系的に見直す）とステータスライン下書き（`3d95f47f3d2974.md`）の延長で、`hooks` を使った具体的な自動化レシピ集はまだありません。`pre-commit` 連携、Stop イベントでの通知、PostToolUse での自動フォーマットなど、再現性が高くニーズも明確です。

---

## おすすめの一手

直近のシリーズ完結性を考えると **(1) CQRS リードモデル設計** が最も収まりが良く、執筆コストに対して読者価値も高いです。書き始めるなら `npx zenn new:article` でスラッグを生成し、`published: false` で骨子から作るのが良いと思います。

下書きのまま塩漬けになっている 10 本（特に `7d2428cbcd258d.md` 依存性ルールを import で強制 / `583ecabd270e4b.md` AI 生成 DDD コードのレビュー）を仕上げる方向も並行候補です。どれから着手しますか。