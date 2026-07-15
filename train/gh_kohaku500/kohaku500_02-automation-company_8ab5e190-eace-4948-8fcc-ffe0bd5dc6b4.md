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

現在時刻と前回作業ファイルを確認します。

> AGENT

前回作業を把握しました。現在時刻 05:33。今日は既に多くの実装が完了しています。

**現状把握:**
- mechsense-core.js v1.4.0（4モジュール完備）✅
- 全4アプリ（BoltSense/SpringSense/ResonSense/BearingSense）コード完了 ✅  
- SpringSense JIS B 2704 数値検証 107/107 PASS ✅ (04:33完了)
- BoltSense 申請中（Google審査待ち）

**今最も価値ある仕事の判断:**  
SpringSense に `verify-spring-jis.js`（107/107 PASS）を作ったのと同様、**BoltSense の JIS B 1083 数値検証**がまだ存在しない。BoltSense は申請中で最初に世に出るアプリ。計算品質の文書化が最優先。

まず既存ファイル群を確認します。

> AGENT

bolt-torque-app に多数の検証ファイルがある。既存のものと重複しないか確認してから作業します。

> AGENT

mechsense-core.js の Bolt モジュール実装を確認します。

> AGENT

bolt-torque-app に多数の検証ファイルがある（verify-jis-fixed.js等）が、mechsense-core.js Bolt モジュール専用の JIS B 1083 計算式照合スクリプト（verify-spring-jis.js と同パターン）は存在しない。これを作成します。

手計算値を確認してから実装します。

> AGENT

手計算値を確認しました。`verify-spring-jis.js`（107/107 PASS）と同パターンで `verify-bolt-jis.js` を作成します。

**手計算根拠（TC-01 M10 / 10.9 / steel / dry）:**
- K = p/(2πd) + 0.577×μ×d2/d + μ×Db/(2d) = 0.023873 + 0.078120 + 0.101250 = **0.20324**
- Fy_denom = 1 + 3×(3/dAs × At)² = 1.38033 → Fy = 940×58.0/√1.38033/1000 = **46.40 kN**
- T_lim = K×d×Fy = 0.20324×10×46.40 = **94.31 N·m**

> AGENT

スクリプトを実行して全件 PASS を確認します。

> AGENT

**223/223 PASS。** 作業ログを記録します。

> AGENT

完了しました。

---

**本日の作業成果（05:33）:**

`verify-bolt-jis.js` を新規作成し、JIS B 1083 の 3 つの主要計算式（式(2) トルク係数 K、式(7) 降伏軸力 Fy、式(8) 限界トルク T_lim）を手計算で導出したうえで mechsense-core.js と照合しました。

**結果: 223/223 PASS**（15 テストケース、7 種類のアサーション）

| 検証ポイント | 結果 |
|---|---|
| TC-01 基準ケース（M10/10.9/steel/dry）全値照合 | K=0.20324, Fy=46.40kN, T_lim=94.31N·m すべて一致 |
| TC-03 ボルト破断が支配的になるケース | dominant='ボルト破断' 正常検出 |
| TC-07 摩擦条件 3 種の単調変化 | dry>lube>grease で K・T_lim 正確に減少 |
| TC-08 ねじ込み深さ dep の影響 | Fstr が dep 比例で増加、K・T_lim は不変 |
| Spring / Resonance / Bearing 非破壊 | 既存 3 モジュール正常 |

これで 4 アプリすべての計算品質が数値テストで証明済みになりました。BoltSense は Google 審査中、残作業はオーナー操作 3 点（wrangler deploy / Android Studio ビルド確認 / スクリーンショット）のみです。
