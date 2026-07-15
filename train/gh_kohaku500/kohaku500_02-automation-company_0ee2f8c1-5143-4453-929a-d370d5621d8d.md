---
session_id: "kohaku500/02-automation-company|0ee2f8c1-5143-4453-929a-d370d5621d8d"
developer: "gh:kohaku500"
split: train
source: crawl
repo: kohaku500/02-automation-company
start_time: "2026-04-25T21:15:09.298Z"
n_turns: 2
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

今日の日付を確認してください。
情報発信部として以下を実行してください：

1. .会社/情報発信部/posts/ の最新投稿履歴を確認する（最後にXへ投稿した日付を把握する）
2. .会社/情報発信部/market-research/ の直近レポートを確認する
3. .会社/営業部/notes/ の最新ファイルでテスター現状を確認する

【X投稿の判断と実行】
- 最後のX投稿から3日以上経過している場合は投稿する
- 投稿文は280文字以内で作成する（日本語約140文字相当）
- BoltSenseテスター募集を訴求する内容にする
- JIS B 1083準拠・現場エンジニア向け・無料テスト参加の呼びかけを含める
- 投稿文が決まったら以下のコマンドで実際にXへ投稿する：
  node /home/makoto1234/makoto_projects/.会社/自動実行/node/post-to-x.js "投稿文"
- 投稿したら .会社/情報発信部/posts/YYYY-MM-DD-x.md に投稿内容を記録する

4. 本日の市場チェックレポートを .会社/情報発信部/market-research/YYYY-MM-DD.md に作成する（同日ファイルがあれば追記）

レポートに含める内容：
- 今日のX投稿状況（投稿したか・しなかった理由）
- BoltSenseテスター募集の進捗
- 次に発信すべきタイミングと内容の提案
- 気づき・メモ

CLAUDE.mdのルールに従い、ファイル名は今日の日付にすること。

> AGENT

Credit balance is too low
