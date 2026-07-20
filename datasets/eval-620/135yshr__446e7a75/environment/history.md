> DEVELOPER

次に公開すると良い記事はありますか？

> AGENT

現在の記事の状態を確認します。

> TOOL

tool_use Bash
id: toolu_01HkgwR49YuBB97eJTTSmRh4
```json
{
  "command": "grep -r \"published:\" articles/ --include=\"*.md\" -l | head -50"
}
```

> TOOL

tool_result
id: toolu_01HkgwR49YuBB97eJTTSmRh4
```
articles/978121945958ed.md
articles/9eca22f9322c40.md
articles/21b1fa2c9365cc.md
articles/9e3ec9a7d52c98.md
articles/860e12b4a2698a.md
articles/8471b2d4bdc9d3.md
articles/05db71175c4746.md
articles/5de289f64ec515.md
articles/fda3ceeeeb764f.md
articles/499cd6335b5fa6.md
articles/f14c01658cd157.md
articles/5ffc0f6a7251e4.md
articles/f757ebaf058ccd.md
articles/4076334bb8cb54.md
articles/1820de942cca32.md
articles/7c5d99d5f45ed7.md
articles/92042eacfbdde3.md
articles/8d2e5d90eafe05.md
articles/7d2428cbcd258d.md
articles/98473f8e119657.md
articles/1b7eb1a3fc3787.md
articles/4415a24c8a2820.md
articles/c05cf4efcc591f.md
articles/56e161aff29ff9.md
articles/60d7d006c0f38f.md
articles/583ecabd270e4b.md
articles/24d20a2df05e30.md
articles/d27112edbad1fc.md
articles/78e3eb0a2a275a.md
articles/f2027369b648cc.md
articles/f21a35a0d5bbcb.md
articles/4afd548d07480a.md
articles/c10431f5afd26d.md
articles/808fbfe6b7db3d.md
articles/b32070e6b12a01.md
```

> TOOL

tool_use Bash
id: toolu_01HnF9wb4jPJDC7q74Xmrp4z
```json
{
  "command": "for f in articles/*.md; do title=$(grep \"^title:\" \"$f\" | head -1); pub=$(grep \"^published:\" \"$f\" | head -1); if echo \"$pub\" | grep -q \"false\"; then echo \"📝 DRAFT: $f — $title\"; fi; done"
}
```

> TOOL

tool_result
id: toolu_01HnF9wb4jPJDC7q74Xmrp4z
```
📝 DRAFT: articles/1820de942cca32.md — title: "LLMをドメインエキスパートとして使う〜ユビキタス言語の整理にAIを活用する〜"
📝 DRAFT: articles/1b7eb1a3fc3787.md — title: "macOS + iTerm2 + tmux + tmuxinator で Claude Code 開発環境を構築する"
📝 DRAFT: articles/21b1fa2c9365cc.md — title: "猫に関連する言葉でプログラミングできる言語「meow」を作った"
📝 DRAFT: articles/583ecabd270e4b.md — title: "AIが生成したDDDコードをどうレビューするか"
📝 DRAFT: articles/60d7d006c0f38f.md — title: "DDDで安全なAPIを設計する〜コマンドとクエリの権限制御パターン〜"
📝 DRAFT: articles/7d2428cbcd258d.md — title: "クリーンアーキテクチャの依存性ルールをGoのimportで強制する方法"
📝 DRAFT: articles/92042eacfbdde3.md — title: "セキュリティレビューで「修正しない」と判断する基準"
📝 DRAFT: articles/9eca22f9322c40.md — title: "meow基礎文法：変数・関数・制御構文をFizzBuzzで学ぶ"
📝 DRAFT: articles/b32070e6b12a01.md — title: "DDDを導入して半年、やってよかったこと・やらなくてよかったこと"
```

> AGENT

下書き状態の記事が9本ありますね。最近の公開記事の傾向と、各下書きの完成度を確認します。

> TOOL

tool_use Bash
id: toolu_01Vd1W5Gn3Kbpr4AdemPbF39
```json
{
  "command": "git log --oneline -10 --format=\"%h %s\""
}
```

> TOOL

tool_result
id: toolu_01Vd1W5Gn3Kbpr4AdemPbF39
```
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
```

> TOOL

tool_use Bash
id: toolu_01BqyqCThBrhxXpGRDVZvGTo
```json
{
  "command": "for f in articles/1820de942cca32.md articles/583ecabd270e4b.md articles/60d7d006c0f38f.md articles/b32070e6b12a01.md articles/7d2428cbcd258d.md articles/92042eacfbdde3.md articles/1b7eb1a3fc3787.md; do echo \"=== $f ($(wc -l < \"$f\") lines) ===\"; head -10 \"$f\"; echo; done"
}
```

> TOOL

tool_result
id: toolu_01BqyqCThBrhxXpGRDVZvGTo
```
=== articles/1820de942cca32.md (     370 lines) ===
---
title: "LLMをドメインエキスパートとして使う〜ユビキタス言語の整理にAIを活用する〜"
emoji: "🧠"
type: "tech"
topics: ["Go", "DDD", "AI", "LLM", "ユビキタス言語"]
published: false
---

## はじめに


=== articles/583ecabd270e4b.md (     434 lines) ===
---
title: "AIが生成したDDDコードをどうレビューするか"
emoji: "🤖"
type: "tech"
topics: ["Go", "DDD", "AI", "CodeReview", "LLM"]
published: false
---

## はじめに


=== articles/60d7d006c0f38f.md (     474 lines) ===
---
title: "DDDで安全なAPIを設計する〜コマンドとクエリの権限制御パターン〜"
emoji: "🔐"
type: "tech"
topics: ["Go", "DDD", "CQRS", "認可", "セキュリティ"]
published: false
---

## はじめに


=== articles/b32070e6b12a01.md (     431 lines) ===
---
title: "DDDを導入して半年、やってよかったこと・やらなくてよかったこと"
emoji: "📝"
type: "tech"
topics: ["Go", "DDD", "振り返り", "チーム開発", "実体験"]
published: false
---

## はじめに


=== articles/7d2428cbcd258d.md (     370 lines) ===
---
title: "クリーンアーキテクチャの依存性ルールをGoのimportで強制する方法"
emoji: "🚧"
type: "tech"
topics: ["Go", "CleanArchitecture", "依存性ルール", "CI", "静的解析"]
published: false
---

## はじめに


=== articles/92042eacfbdde3.md (     149 lines) ===
---
title: "セキュリティレビューで「修正しない」と判断する基準"
emoji: "⚖️"
type: "tech"
topics: ["security", "oss"]
published: false
---

## はじめに


=== articles/1b7eb1a3fc3787.md (     351 lines) ===
---
title: "macOS + iTerm2 + tmux + tmuxinator で Claude Code 開発環境を構築する"
emoji: "🖥"
type: "tech"
topics: ["tmux", "tmuxinator", "iterm2", "macos", "claudecode"]
published: false
---

この記事では、macOS 上で iTerm2・tmux・tmuxinator を組み合わせた開発環境を構築します。Claude Code・nvim・コマンドラインを同時に使える環境を、上から順に実行するだけで整えられます。tmux を初めて使う方にも対応しています。
```

> TOOL

tool_use Bash
id: toolu_014NwNjqKf7Uxs4P1Bpmy4BH
```json
{
  "command": "# 公開済みDDD記事の一覧を確認（シリーズの流れを把握）\nfor f in articles/*.md; do pub=$(grep \"^published:\" \"$f\" | head -1); if echo \"$pub\" | grep -q \"true\"; then title=$(grep \"^title:\" \"$f\" | head -1 | sed 's/title: //'); topics=$(grep \"^topics:\" \"$f\" | head -1); if echo \"$topics\" | grep -qi \"ddd\"; then echo \"$f — $title\"; fi; fi; done"
}
```

> TOOL

tool_result
id: toolu_014NwNjqKf7Uxs4P1Bpmy4BH
```
articles/4415a24c8a2820.md — "コンテキストマップを描いてからコードを書く〜戦略的DDDのすすめ〜"
articles/4afd548d07480a.md — "Goの非公開フィールドで集約の不変条件を守る設計パターン"
articles/56e161aff29ff9.md — "Go × DDDのエラーハンドリング設計〜ドメインエラーとインフラエラーを分離する〜"
articles/5de289f64ec515.md — "UseCase層は本当に必要か〜Goでのクリーンアーキテクチャ最小構成〜"
articles/5ffc0f6a7251e4.md — "イベントソーシングをGoで実装したら「applyの意味」を完全に誤解していた"
articles/78e3eb0a2a275a.md — "DDDのテスト戦略〜集約とドメインサービスをどうテストするか〜"
articles/860e12b4a2698a.md — "GoのRepositoryパターン再考〜DB依存を剥がすのはどこまで必要か〜"
articles/98473f8e119657.md — "Goで値オブジェクトをどこまで作るべきか〜コスパの良いDDD戦術設計〜"
articles/9e3ec9a7d52c98.md — "DDDにCQRSを導入する前に知っておきたいこと〜誤解しやすい4つのポイントと理想的な設計〜"
articles/c05cf4efcc591f.md — "ドメインイベントで集約間の結合を断ち切る〜Goでの実装パターン〜"
articles/d27112edbad1fc.md — "境界づけられたコンテキストをGoのモジュール構成に落とし込む"
articles/f2027369b648cc.md — "Goでクリーンアーキテクチャを導入するとinterfaceが爆発する問題への処方箋"
articles/f21a35a0d5bbcb.md — "軽量DDDは本当にアンチパターンか〜段階的DDD導入のリアル〜"
articles/f757ebaf058ccd.md — "腐敗防止層（ACL）をGoで実装する〜外部APIとドメインモデルの翻訳パターン〜"
articles/fda3ceeeeb764f.md — "DDDの入力バリデーション設計〜ドメイン層で何を守り、何を外に任せるか〜"
```

> AGENT

下書き記事の状況を踏まえて、おすすめをまとめます。

---

## 次に公開するおすすめ記事

DDDシリーズが15本公開済みで非常に充実しています。下書き9本の中から、**公開優先度が高い順**に提案します。

### 1. 「DDDで安全なAPIを設計する〜コマンドとクエリの権限制御パターン〜」(474行)
- **理由**: 直近で「入力バリデーション設計」と「CQRS」の記事を公開済みで、CQRS + 認可の話題は自然な次のステップです。ボリュームも十分で完成度が高そうです。

### 2. 「AIが生成したDDDコードをどうレビューするか」(434行)
- **理由**: DDD × AI は今トレンド性が非常に高いテーマです。既存のDDDシリーズの読者層に刺さりやすく、新規読者も獲得しやすいです。

### 3. 「LLMをドメインエキスパートとして使う〜ユビキタス言語の整理にAIを活用する〜」(370行)
- **理由**: 上記2と合わせて「DDD × AI」のミニシリーズとして連続公開すると相乗効果が期待できます。

### 4. 「DDDを導入して半年、やってよかったこと・やらなくてよかったこと」(431行)
- **理由**: 振り返り・実体験系の記事はエンゲージメントが高い傾向があります。シリーズの中間まとめ的な位置づけになります。

---

**一番のおすすめは 1 の「権限制御パターン」** です。シリーズの流れ（バリデーション → CQRS → 権限制御）として最も自然で、読者が次に知りたい内容と合致しています。

内容を確認してレビューしましょうか？