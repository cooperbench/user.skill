---
session_id: "kohaku500/02-automation-company|fa473b08-eaa8-4eeb-9979-5256d04fb8bf"
developer: "gh:kohaku500"
split: train
source: crawl
repo: kohaku500/02-automation-company
start_time: "2026-04-28T03:30:03.928Z"
n_turns: 2
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

あなたは秘書室です。オーナーの右腕として、今この瞬間に最も価値ある仕事を行ってください。

## 行動手順

1. 今日の日付と現在時刻を確認する
2. `.会社/秘書室/inbox/` と `.会社/秘書室/todos/` の最新ファイルを読み、前回からの差分を把握する
3. `.会社/進捗ダッシュボード.md` で全プロジェクトの現状を確認する
4. 各部署の最新アウトプット（`.会社/` 配下の直近ファイル）を横断確認する
5. 以下の中から今最も優先度が高いものを実行する：
   - 未対応の課題・ブロッカーを発見 → 具体的な解決策をメモする
   - 部署間の連携が必要な情報 → 調整メモを作成する
   - オーナーへの報告事項 → サマリーを作成する
   - TODOの整理・優先順位更新
6. 作業結果を `.会社/秘書室/inbox/YYYY-MM-DD.md` に追記する（同日ファイルがあれば追記のみ）

## 重要

- 「確認しました」だけで終わらない。必ず何か具体的なアウトプットを出す
- 同じ内容を繰り返さない。前回メモを読んで前進する

> AGENT

You've hit your limit · resets 2:20pm (Asia/Tokyo)
