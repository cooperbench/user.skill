> DEVELOPER

あなたは技術部・ばね計算アプリ担当です。今この瞬間に最も価値ある仕事を行ってください。

## 行動手順

1. 今日の日付と現在時刻を確認する
2. `.会社/ばね計算アプリチーム/技術/` の最新ファイルを読み、前回作業を把握する
3. 以下の中から今最も価値ある仕事を実行する（BoltSense完了待ちの間も前進）：
   - JIS B 2704の計算式・全ケースの整理と実装仕様書作成
   - 計算検証ケース（JIS規格例との照合テスト）の設計
   - UI/UX設計案の詳細化（BoltSenseの設計を参考に改善）
   - Android実装アーキテクチャの設計
   - 音響診断アプリとの将来的な統合アーキテクチャ検討
   - 共通計算ライブラリ設計（ばね・ボルト・共振点を統合）
4. 作業結果を `.会社/ばね計算アプリチーム/技術/YYYY-MM-DD.md` に追記保存する

> AGENT

現在時刻と前回作業を確認します。

> AGENT

今日の20:35で技術コード作業は全完了している。JIS B 1083検証プロジェクトの詳細を確認して、残タスクを判断します。

> AGENT

JIS B 1083検証は全Phase完了済み。音響診断アプリチームのフォルダを確認して、統合アーキテクチャ設計の価値を判断します。

> AGENT

音響診断アプリの技術フォルダと今日の作業ログを確認します。

> AGENT

音響診断アプリの軸受計算と mechsense-core.js の統合が最高価値タスクです。bearing_calculator.py の詳細を確認します。

> AGENT

軸受特性周波数の計算式を把握しました。mechsense-core.js v1.3.0 として Bearing モジュールを実装します。

> AGENT

Bearing モジュールを mechsense-core.js v1.3.0 として実装します。まず Resonance モジュールの末尾と Utils の間に挿入します。

> AGENT

次に検証スクリプトを作成します。

> AGENT

2つのFAILを修正します。Bolt.calc の引数確認が必要です。

> AGENT

BOLT_DATA のキーは数値（`10` など）で、テストスクリプトと実装の警告条件を修正します。

> AGENT

33 PASS / 0 FAIL。CWRU 6205-2RS の実値（BPFO=106.98Hz, BPFI=162.57Hz）で音響診断 Python 実装と完全一致しています。

作業ログに記録します。

> AGENT

完了しました。

---

## 本日（23:42）の作業内容

**mechsense-core.js v1.3.0 — Bearing モジュール実装完了**

### やったこと

音響診断アプリチームの `bearing_calculator.py`（Python）を見て、軸受特性周波数計算を mechsense-core.js に Bearing モジュールとして移植しました。

**計算式**（軸受力学の基本式）:
- BPFO（外輪損傷）= `(nb/2) × shaft × (1 − bd/pd × cos φ)`
- BPFI（内輪損傷）= `(nb/2) × shaft × (1 + bd/pd × cos φ)`
- BSF（転動体損傷）= `(pd/2bd) × shaft × (1 − (bd/pd)² × cos²φ)`
- FTF（保持器）= `0.5 × shaft × (1 − bd/pd × cos φ)`

**検証**: CWRU 6205-2RS（rpm=1797）で Python 実装と完全一致（BPFO=106.98Hz, BPFI=162.57Hz）。33 PASS / 0 FAIL。

### 戦略的な意味

| モジュール | アプリ |
|-----------|--------|
| Spring | SpringSense |
| Bolt | BoltSense（申請中） |
| Resonance | ResonSense |
| **Bearing（本日追加）** | **将来: BearingSense + 音響診断アプリ WebView** |

Python 側は Informed NMF・スペクトル減算など高度な信号処理に集中でき、周波数計算の重複実装がなくなります。
