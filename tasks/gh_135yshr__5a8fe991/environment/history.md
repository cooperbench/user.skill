> DEVELOPER

@articles/60293061fe34dd.md 

批判的に見ると、大きな嘘は少ないですが、いくつかは「正しい方向性を、少し強く言い切りすぎている」印象です。特に リードモデルの定義、再構築可能性、Outboxのサンプルコード、戦略選択フロー は修正した方がよいです。レビュー対象はこちらの記事本文です。 ￼

総評

記事全体の主張はかなり丁寧です。
特に、Outboxは永続イベントログではないこと、Upsertだけでは冪等性の十分条件ではないこと、MAX(version) 判定が厳密ではないことを自分で補足している点は良いです。

ただし批判的に見ると、読者が以下のように誤解する可能性があります。

CQRSのリードモデルは必ず非正規化されていなければならない
Query側にはビジネスルールが一切ない
リードモデルはいつでも再構築できる
Outboxを置けば at-least-once が自然に成立する
迷ったら C → A → B でほぼ決められる

このあたりは、嘘とまでは言わないが、紛らわしいです。

⸻

重大指摘 1: 「リードモデル = 非正規化」は定義として強すぎる

記事ではリードモデルを、

画面やAPIレスポンスの形にあわせて非正規化された、読み取り専用のデータ表現

と定義しています。これは実務上の方針としては理解できますが、CQRSの一般的な定義としては狭すぎます。

Martin Fowler の説明では、CQRSの核は「更新用モデルと読み取り用モデルを分けること」であり、同じDBを共有する場合や、リレーショナルDBのビューに近い形もあり得るとされています。つまり、非正規化はよくある実装方針であって、CQRSの必須条件ではありません。 ￼

特に記事内では戦略Cとして通常の VIEW を扱っています。通常の VIEW はJOINを隠蔽しているだけで、物理的に非正規化されたデータを保持しているわけではありません。そのため、冒頭の定義と後半の戦略Cが少し噛み合っていません。

修正するなら、こうした方が安全です。

リードモデルは、読み取りユースケースに合わせて設計されたデータ表現です。
実装としては、DTO、SQL VIEW、専用テーブル、検索インデックスなどがあり、
性能やUX要件に応じて非正規化されることが多いです。

⸻

重大指摘 2: 「読み取り側はビジネスルールを通す必要がない」は危ない

記事では、

読み取り側はビジネスルールを通す必要がないため、書き込み側とは別の薄い層でよい

という趣旨の説明があります。これは言いたいことは分かりますが、そのまま読むと危険です。

読み取り側でも、以下は普通に必要です。

* 認可
* テナント分離
* 表示可否の判定
* マスキング
* 公開状態によるフィルタリング
* ユーザーごとの可視範囲制御

正確には、Query側が不要なのは「状態遷移を成立させるための不変条件チェック」や「副作用を伴う業務判断」です。
「ビジネスルールが不要」と言うと、認可や可視性制御まで軽視してよいように見えます。

修正案です。

読み取り側は、状態遷移や不変条件を守るためのドメインモデルを必ずしも経由する必要はありません。
ただし、認可・テナント分離・表示可否・マスキングなど、読み取り固有のルールはQuery側にも必要です。

⸻

重大指摘 3: Projectorのサンプルコードに実害のある紛らわしさがある

ここはかなり重要です。

p, ok := r.projectors[e.EventType]
if !ok {
    continue // 未登録のイベントは無視（あとから増やせる）
}

このコードだと、未登録イベントは MarkProcessed されません。つまり 無視しているように見えて、実際には未処理のまま残り、次回以降も何度も取得されます。

コメントの「未登録のイベントは無視」と実装が一致していません。
これは読者がそのまま真似すると、ワーカーが同じ未対応イベントを延々と拾い続ける可能性があります。

さらに、「あとから増やせる」も紛らわしいです。
未登録イベントを本当に無視して processed にしてしまうと、後からProjectorを追加しても、そのイベントを再処理できません。逆に未処理のまま残すなら、無視ではなく「保留」「dead letter」「unsupported event」として扱うべきです。

修正方針はどれかに寄せた方がよいです。

if !ok {
    // 方針1: 未対応イベントはエラーにして止める
    return fmt.Errorf("unsupported event type: %s", e.EventType)
}

または、

if !ok {
    // 方針2: 未対応イベントとして記録し、通常の未処理キューからは外す
    if err := r.outbox.MarkUnsupported(ctx, e.ID, e.EventType); err != nil {
        return err
    }
    continue
}

ここは記事公開前に直した方がよいです。

⸻

重大指摘 4: 「リードモデルはいつでも再構築できる」は言い切りすぎ

記事の後半で、

リードモデルは書き込みモデルの結果系であって、いつでも再構築できる

という趣旨の記述があります。

しかし前半では正しく、

Outbox単独では完全な再構築はできない
再構築可能性を要件にするなら永続的なイベントログが必要

と説明しています。

この2つが少し矛盾して見えます。

正確には、リードモデルは「再構築できるように設計するべきもの」であって、何もしなくてもいつでも再構築できるものではありません。Transactional Outbox の主目的は、DB更新とメッセージ送信の整合性を取ることであり、永続的な再生ログそのものではありません。Outboxパターンでも、メッセージリレーが重複発行し得るため、コンシューマ側の冪等性が必要だと説明されています。 ￼

修正案です。

リードモデルは、書き込みモデルから導出された結果系です。
ただし、再構築できるかどうかは、元データ・イベントログ・再計算バッチ・保持期間を設計しているかに依存します。

⸻

中程度の指摘 1: 「C → A → B」の選択フローは便利だが単純化しすぎ

「迷ったら C → A → B」は、記事の対象スコープでは納得できます。
ただし、フロー図だけ見ると判断軸が少なすぎます。

現在のフローは主に、

* 読み取り頻度
* 結果整合性を許容できるか

で分岐しています。

しかし実務では、少なくとも以下も効きます。

* 集計の重さ
* 検索要件
* 更新頻度
* 書き込みレイテンシの許容値
* 読み取りSLO
* リードモデル再構築の必要性
* 障害時にどちらを優先するか
* 監査・履歴要件
* DBレプリカやキャッシュの有無

Martin Fowler も、CQRSは有効な場面がある一方で、多くのシステムでは複雑性とリスクを増やすため慎重に使うべきだと述べています。 ￼ […]

> AGENT

レビュー内容を確認しました。優先5項目を中心に、中程度・軽微な指摘も反映していきます。

まず重大指摘1（リードモデルの定義）から修正します。

> TOOL

tool_use Edit
id: toolu_019mhDAJihxaTJy5w8QC51Um
```json
{
  "replace_all": false,
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "old_string": "## リードモデルとは何か\n\nCQRSにおける **リードモデル（Read Model）** は、「画面やAPIレスポンスの形にあわせて非正規化された、読み取り専用のデータ表現」です。書き込みモデル（集約）とは独立しており、JOIN・集計・キャッシュ・全文検索インデックスなど、読み取りに都合のよい形を自由に選べます。\n\nCQRSの読み取り側がドメインモデルを必ずしも経由する必要はない、という発想は[Greg Young の CQRS Documents](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)で示されている考え方です。読み取り側はビジネスルールを通す必要がないため、書き込み側とは別の薄い層でよい、という立場です。本記事もこの立場を前提とします。\n\n私は最初、リードモデルを「集約をDTOに変換しただけのもの」と考えていました。しかしそれは**RepositoryからDTOへの詰め替え**にすぎず、CQRSのうまみはほぼ得られません。リードモデルは次の3つの条件を満たして初めて意味を持ちます（**表1**）。\n\n**表1: リードモデルの3条件**\n\n| 条件                              | 説明                                         |\n| --------------------------------- | -------------------------------------------- |\n| 書き込みモデルから独立している    | 集約の構造が変わってもリードモデルが壊れない |\n| 画面・API単位で非正規化されている | 1回のクエリで必要なデータが揃う              |\n| ドメインルールを持たない          | 検証・状態遷移・ビジネス計算は行わない       |\n\nつまり「リードモデルは別物として作る」ことに意味があり、書き込みモデルの構造をそのまま映したリードモデルは、ただの薄いDTOです。\n\nなお3つ目の「ドメインルールを持たない」が指すのは、状態遷移・不変条件・後続業務に影響する判断のことです。表示ラベルの生成やソート用キーの算出といった**純粋な表示ロジック**はリードモデル側に置いても問題ありません。詳しくはアンチパターン1で線引きします。",
  "new_string": "## リードモデルとは何か\n\nCQRSにおける **リードモデル（Read Model）** は、「読み取りユースケースに合わせて設計されたデータ表現」です。実装としては DTO、SQL の VIEW、専用テーブル、検索インデックスなどがあり、性能や UX 要件に応じて非正規化されることが多い、という関係です。書き込みモデル（集約）とは独立しており、JOIN・集計・キャッシュ・全文検索インデックスなど、読み取りに都合のよい形を自由に選べます。\n\nCQRSの読み取り側がドメインモデルを必ずしも経由する必要はない、という発想は[Greg Young の CQRS Documents](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)で示されている考え方です。ここで「経由しなくてよい」のは、**状態遷移を成立させるための不変条件チェックや、副作用を伴う業務判断**です。一方で、認可・テナント分離・表示可否の判定・マスキング・公開状態によるフィルタリングなど、**読み取り固有のルール**は Query 側にも必要です（認可については[シリーズ第2作](https://zenn.dev/135yshr/articles/60d7d006c0f38f)で扱っています）。本記事もこの立場を前提とします。\n\n私は最初、リードモデルを「集約をDTOに変換しただけのもの」と考えていました。しかしそれは**RepositoryからDTOへの詰め替え**にすぎず、CQRSのうまみはほぼ得られません。リードモデルは次の3つの方針を意識して初めて意味を持ちます（**表1**）。これらは必須要件というよりは、「リードモデルを別物として設計する」ことが効くケースの典型像です。\n\n**表1: リードモデル設計の方針**\n\n| 方針                              | 説明                                         |\n| --------------------------------- | -------------------------------------------- |\n| 書き込みモデルから独立している    | 集約の構造が変わってもリードモデルが壊れない |\n| 画面・API単位で形を最適化する     | 1回のクエリで必要なデータが揃う（非正規化や集計の事前計算を含む） |\n| 状態遷移・不変条件は持たない      | 業務判断や副作用を伴うロジックは書き込み側に寄せる |\n\nつまり「リードモデルは別物として作る」ことに意味があり、書き込みモデルの構造をそのまま映したリードモデルは、ただの薄いDTOです。\n\nなお3つ目の「状態遷移・不変条件は持たない」が指すのは、後続業務に影響する判断のことです。表示ラベルの生成やソート用キーの算出といった**純粋な表示ロジック**はリードモデル側に置いても問題ありません。詳しくはアンチパターン1で線引きします。"
}
```

> TOOL

tool_result
id: toolu_019mhDAJihxaTJy5w8QC51Um
```
The file /Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

次に、配置パターンの「離れるほど性能向上」を弱め、戦略選択フローを簡略版と明記します。

> TOOL

tool_use Edit
id: toolu_01XGDAGBybVoh9VFeU6zHYwj
```json
{
  "replace_all": false,
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "old_string": "配置が書き込みモデルから離れるほど読み取り性能と柔軟性は上がりますが、整合性の維持コストも上がります。",
  "new_string": "配置が書き込みモデルから離れるほど、読み取り用途に最適化しやすくなります。一方で、実際の性能はクエリ特性・インデックス設計・同期方式に依存し、必ずしも別ストア化が速いとは限りません。整合性の維持コストと運用コストは上がります。"
}
```

> TOOL

tool_result
id: toolu_01XGDAGBybVoh9VFeU6zHYwj
```
The file /Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_0143ZVr9QZwgaKb6F7aBtZsD
```json
{
  "replace_all": false,
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "old_string": "**図2: 戦略選択のフロー**\n\n「迷ったら戦略C → A → Bの順に検討する」のが私の経験則です。Bは強力ですが、Outboxやワーカー、再構築機構など運用の道具立てが多く、必要になるまで導入を遅らせるのが安全だと感じています。\n\nただしこれは一般則ではありません。次のような条件が最初から分かっている場合は、初期フェーズでも戦略Bから入る判断はあり得ます。",
  "new_string": "**図2: 戦略選択のフロー（簡略版）**\n\nこのフローは**初期判断のための簡略版**です。実際には、読み取り頻度や結果整合性の許容度だけでなく、集計の重さ・検索要件・再構築要件・障害時運用・書き込みレイテンシの許容値・読み取りSLO・監査要件なども合わせて判断します。本記事の経験談スコープ（注文・予約系、数十req/sec規模）ではこの2軸でかなり絞り込めますが、領域が変われば判断軸も増えます。\n\n「迷ったら戦略C → A → Bの順に検討する」のが私の経験則です。Bは強力ですが、Outboxやワーカー、再構築機構など運用の道具立てが多く、必要になるまで導入を遅らせるのが安全だと感じています。\n\nただしこれは一般則ではありません。次のような条件が最初から分かっている場合は、初期フェーズでも戦略Bから入る判断はあり得ます。"
}
```

> TOOL

tool_result
id: toolu_0143ZVr9QZwgaKb6F7aBtZsD
```
The file /Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

戦略Aの判断基準に「同じプライマリDB」前提を追記します。

> TOOL

tool_use Edit
id: toolu_017tUPWB7fma3AChjwtzM5m4
```json
{
  "replace_all": false,
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "old_string": "### 戦略Aを採用する判断基準\n\n- 書き込みと読み取りが**同一データベース**で完結します\n- 「書いた直後に読んだら最新が見えてほしい」という要件が強いです（read-your-writes）\n- プロジェクションが軽く、書き込みのレイテンシに乗せても問題ありません",
  "new_string": "### 戦略Aを採用する判断基準\n\n- 書き込みと読み取りが**同一プライマリDB**で完結します（リードレプリカやキャッシュ越しに読むと read-your-writes は崩れ得るため、ここではプライマリDBを直接読む前提です）\n- 「書いた直後に読んだら最新が見えてほしい」という要件が強いです（read-your-writes）\n- プロジェクションが軽く、書き込みのレイテンシに乗せても問題ありません"
}
```

> TOOL

tool_result
id: toolu_017tUPWB7fma3AChjwtzM5m4
```
The file /Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

重大指摘3: Projectorの未登録イベント処理を修正します。

> TOOL

tool_use Edit
id: toolu_01KtUKoaaP4wm8R65jfLtHsr
```json
{
  "replace_all": false,
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "old_string": "type Runner struct {\n    outbox     OutboxReader\n    projectors map[string]Projector\n}\n\nfunc (r *Runner) Tick(ctx context.Context) error {\n    events, err := r.outbox.FetchUnprocessed(ctx, 100)\n    if err != nil {\n        return err\n    }\n    for _, e := range events {\n        p, ok := r.projectors[e.EventType]\n        if !ok {\n            continue // 未登録のイベントは無視（あとから増やせる）\n        }\n        if err := p.Project(ctx, e.Payload); err != nil {\n            return err // リトライは次の tick で\n        }\n        if err := r.outbox.MarkProcessed(ctx, e.ID); err != nil {\n            return err\n        }\n    }\n    return nil\n}\n```\n\nイベント間の順序保証が必要なら、`aggregate_id` 単位でシリアライズします（同じ集約のイベントは順序通りに処理します）。グローバル順序が必要かどうかは業務によります。金融の取引履歴や監査ログのように「全体で時系列を保証したい」要件があれば別途設計が必要です。私が扱ってきた範囲（注文・予約系）では集約単位の順序で足りるケースがほとんどでした。",
  "new_string": "type Runner struct {\n    outbox     OutboxReader\n    projectors map[string]Projector\n}\n\nfunc (r *Runner) Tick(ctx context.Context) error {\n    events, err := r.outbox.FetchUnprocessed(ctx, 100)\n    if err != nil {\n        return err\n    }\n    for _, e := range events {\n        p, ok := r.projectors[e.EventType]\n        if !ok {\n            // 未登録イベントを continue で素通りさせると未処理のまま残り続け、\n            // 毎回の Tick で同じイベントを取得し続けてしまいます。\n            // ここではエラーにして開発時に気付けるようにします。\n            // 「あとからProjectorを足したい」運用に倒すなら、\n            // 別の状態（unsupported / dead-letter）にマークして\n            // 通常の未処理キューからは外す方針を採ります。\n            return fmt.Errorf(\"unsupported event type: %s (event id=%d)\", e.EventType, e.ID)\n        }\n        if err := p.Project(ctx, e.Payload); err != nil {\n            return err // リトライは次の tick で\n        }\n        if err := r.outbox.MarkProcessed(ctx, e.ID); err != nil {\n            return err\n        }\n    }\n    return nil\n}\n```\n\n未登録イベントの扱いは、運用方針によって2通りに分かれます。\n\n- **方針1: エラーで止める**（上記の例）。未対応イベントが流れたら即座に気付けるので、CI や開発初期に向きます\n- **方針2: `unsupported` 状態に切り替えて通常キューから外す**。たとえば outbox に `status` 列を持たせ、`MarkUnsupported(ctx, e.ID, […]

> TOOL

tool_result
id: toolu_01KtUKoaaP4wm8R65jfLtHsr
```
The file /Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Materialized ViewのPostgreSQL前提を明記します。

> TOOL

tool_use Edit
id: toolu_01Hxu4T2hAdsxDU9t46ss7ET
```json
{
  "replace_all": false,
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "old_string": "### Materialized View の位置づけ\n\nMaterialized View は名前こそ「ビュー」ですが、実態は**結果を永続化したテーブル**です。`REFRESH MATERIALIZED VIEW` 実行時のスナップショットが保存され、それ以降は書き込みテーブルが更新されても自動では反映されません。\n\nこのため Materialized View は次の点で通常の VIEW とは性質が違います。\n\n- 定義変更だけで読み取り結果が反映されません（再作成や REFRESH が必要です）\n- REFRESH のタイミング・頻度・ロック挙動（`CONCURRENTLY` の有無）を運用設計する必要があります\n- インデックスを別途張る対象になります（VIEW にはインデックスを張れません）\n\n本記事の整理では、Materialized View は「戦略Cの素直な延長」というよりも、戦略A / 戦略B に移る前の**中間的な選択肢**として捉えます。小規模な集計や日次バッチでの REFRESH 程度なら Materialized View の方がシンプルに済むこともあります。一方で、REFRESH の頻度・粒度・ロック設計が複雑になってきたタイミングで、戦略Bの Outbox + Projector に移したほうが見通しよくなることもあります。「複雑化のシグナルが出てきたら戦略B」というのが私の判断基準です。",
  "new_string": "### Materialized View の位置づけ\n\n以下は主に **PostgreSQL の Materialized View** を念頭に置いた説明です。DB 製品によって更新方式・自動更新の扱い・インデックスの可否は異なるため、利用 DB のドキュメントで確認してください。\n\nMaterialized View は名前こそ「ビュー」ですが、実態は**結果を永続化したテーブル**です。PostgreSQL では `REFRESH MATERIALIZED VIEW` 実行時のスナップショットが保存され、それ以降は書き込みテーブルが更新されても自動では反映されません。\n\nこのため Materialized View は次の点で通常の VIEW とは性質が違います。\n\n- 定義変更だけで読み取り結果が反映されません（再作成や REFRESH が必要です）\n- REFRESH のタイミング・頻度・ロック挙動（`CONCURRENTLY` の有無、必要な UNIQUE インデックスの設計）を運用設計する必要があります\n- インデックスを別途張る対象になります（PostgreSQL では通常の VIEW にはインデックスを張れません）\n\n本記事の整理では、Materialized View は「戦略Cの素直な延長」というよりも、戦略A / 戦略B に移る前の**中間的な選択肢**として捉えます。小規模な集計や日次バッチでの REFRESH 程度なら Materialized View の方がシンプルに済むこともあります。一方で、REFRESH の頻度・粒度・ロック設計が複雑になってきたタイミングで、戦略Bの Outbox + Projector に移したほうが見通しよくなることもあります。「複雑化のシグナルが出てきたら戦略B」というのが私の判断基準です。"
}
```

> TOOL

tool_result
id: toolu_01Hxu4T2hAdsxDU9t46ss7ET
```
The file /Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

重大指摘4: 「いつでも再構築できる」を修正します。

> TOOL

tool_use Edit
id: toolu_01G2uaRR4NHPq741HsimWj6C
```json
{
  "replace_all": false,
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "old_string": "データの重複は許容します。リードモデルは**書き込みモデルの結果系**であって、いつでも再構築できるからです。",
  "new_string": "データの重複は許容します。リードモデルは**書き込みモデルから導出された結果系**だからです。ただし「いつでも再構築できる」のは自動的にそうなるわけではなく、元データ・イベントログ・再計算バッチ・保持期間を**再構築できるように設計しておく**ことが前提です（戦略Bの再構築可能性の節で触れた通り、Outbox 単独では完全な再構築はできない場合があります）。"
}
```

> TOOL

tool_result
id: toolu_01G2uaRR4NHPq741HsimWj6C
```
The file /Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

中程度指摘4: ドメインイベント肥大化への注意を追加します。

> TOOL

tool_use Edit
id: toolu_01UKibck66ZzXyH7xuicPcsT
```json
{
  "replace_all": false,
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "old_string": "「想定するリードモデルに必要な値か」「外部連携に流す前提でも安全か」を一度立ち止まって考えるくらいの粒度が、ちょうどよいバランスです。",
  "new_string": "「想定するリードモデルに必要な値か」「外部連携に流す前提でも安全か」を一度立ち止まって考えるくらいの粒度が、ちょうどよいバランスです。\n\nもう一つ意識したいのは、**ドメインイベントとプロジェクション専用イベント（または投影用メッセージ）を分けて考える**ことです。たとえば `OrderPlaced` に `CustomerName` を載せるのは、注文時点の顧客名スナップショットに業務上の意味（後から顧客名が変わっても注文履歴は当時の名前を保持する、等）があれば自然です。一方で、一覧画面のラベル表示だけのためにドメインイベントへ表示項目を増やすと、ドメインモデルが画面都合に引っ張られます。表示専用の項目は、ドメインイベントを購読する Projector 側で「投影用の中間表現」に詰め替えて保持するなどの分離が有効です。"
}
```

> TOOL

tool_result
id: toolu_01UKibck66ZzXyH7xuicPcsT
```
The file /Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

軽微指摘3: OutboxWriter.Appendとレスポンスの整合性に注意書きを足します。`ExpectedVersion` を返す例の前提を補足します。

> TOOL

tool_use Edit
id: toolu_01WBz8jJMXfit9YY9G4FG4J5
```json
{
  "replace_all": false,
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "old_string": "書き込みレスポンスと読み取りリクエストはこんなイメージです。\n\n```go\n// 書き込みレスポンス: outboxにINSERTした最新IDを返す\ntype PlaceOrderResponse struct {\n    OrderID         string `json:\"order_id\"`\n    ExpectedVersion int64  `json:\"expected_version\"` // ← この値以上が見えるはず\n}",
  "new_string": "書き込みレスポンスと読み取りリクエストはこんなイメージです。\n\nなお、戦略Bのサンプルでは `outbox.Append(ctx, events) error` というシグネチャでしたが、`ExpectedVersion` を返したい場合は **INSERT で採番された outbox.id のうち最大値を返すよう拡張する** 必要があります。たとえば `Append(ctx, events) (lastID int64, err error)` のように変えるか、別途 `outbox.LastInsertedID(ctx)` を呼ぶ、といった形で UseCase 側からバージョンを受け取れるようにします。本記事のサンプルでは簡潔さを優先して error 返しのみにしていますが、戦略Bでスタール検知まで採用するならここを揃えてください。\n\n```go\n// 書き込みレスポンス: outboxにINSERTした最新IDを返す\ntype PlaceOrderResponse struct {\n    OrderID         string `json:\"order_id\"`\n    ExpectedVersion int64  `json:\"expected_version\"` // ← この値以上が見えるはず\n}"
}
```

> TOOL

tool_result
id: toolu_01WBz8jJMXfit9YY9G4FG4J5
```
The file /Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

最後にまとめセクションの整合も微調整します。レビューの「リードモデル＝非正規化」を弱めた点と整合させます。

> TOOL

tool_use Edit
id: toolu_01SuCBzty1DtwTYgEC3gpLaa
```json
{
  "replace_all": false,
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "old_string": "- リードモデルは**書き込みモデルとは別物**として設計します。詰め替えだけでは意味がありません\n- プロジェクション戦略は**A: 同期 / B: 非同期（Outbox） / C: オンデマンド**の3つです。整合性モデル・運用要素・初期フェーズ向きの軸で選びます（表2）\n- 迷ったら**C → A → B**の順で検討します。Bは強力ですが運用要素が増えます\n- 結果整合性は技術で消すのではなく、**UXで吸収**します(オプティミスティック更新、バージョン番号、ハイブリッド)\n- リードモデルは**画面・API単位で非正規化**し、業務判断は持たせません",
  "new_string": "- リードモデルは**書き込みモデルとは別物**として設計します。詰め替えだけでは意味がありません\n- プロジェクション戦略は**A: 同期 / B: 非同期（Outbox） / C: オンデマンド**の3つです。整合性モデル・運用要素・初期フェーズ向きの軸で選びます（表2）\n- 迷ったら**C → A → B**の順で検討します。これは初期判断の簡略フローで、集計の重さ・検索要件・再構築要件などが絡む場合は別途検討します\n- 結果整合性は技術で消すのではなく、**UXで吸収**します（オプティミスティック更新、バージョン番号、ハイブリッド）\n- リードモデルは**画面・API単位で形を最適化**し、状態遷移や不変条件は持たせません（認可・テナント分離・表示可否などの読み取り固有ルールは Query 側でも必要です）"
}
```

> TOOL

tool_result ERROR
id: toolu_01SuCBzty1DtwTYgEC3gpLaa
```
<tool_use_error>String to replace not found in file.
String: - リードモデルは**書き込みモデルとは別物**として設計します。詰め替えだけでは意味がありません
- プロジェクション戦略は**A: 同期 / B: 非同期（Outbox） / C: オンデマンド**の3つです。整合性モデル・運用要素・初期フェーズ向きの軸で選びます（表2）
- 迷ったら**C → A → B**の順で検討します。Bは強力ですが運用要素が増えます
- 結果整合性は技術で消すのではなく、**UXで吸収**します(オプティミスティック更新、バージョン番号、ハイブリッド)
- リードモデルは**画面・API単位で非正規化**し、業務判断は持たせません
(note: Edit also tried swapping \uXXXX escapes and their characters; neither form matched, so the mismatch is likely elsewhere in old_string. Re-read the file and copy the exact surrounding text.)</tool_use_error>
```

> TOOL

tool_use Read
id: toolu_01DvCCgFBvB5JsLAsjUMQTwT
```json
{
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "offset": 695,
  "limit": 15
}
```

> TOOL

tool_result
id: toolu_01DvCCgFBvB5JsLAsjUMQTwT
```
695	
696	---
697	
698	## まとめ
699	
700	CQRSのリードモデル設計を、戦略の選び方と実装のポイントから整理しました。
701	
702	- リードモデルは**書き込みモデルとは別物**として設計します。詰め替えだけでは意味がありません
703	- プロジェクション戦略は**A: 同期 / B: 非同期（Outbox） / C: オンデマンド**の3つです。整合性モデル・運用要素・初期フェーズ向きの軸で選びます（表2）
704	- 迷ったら**C → A → B**の順で検討します。Bは強力ですが運用要素が増えます
705	- 結果整合性は技術で消すのではなく、**UXで吸収**します（オプティミスティック更新、バージョン番号、ハイブリッド）
706	- リードモデルは**画面・API単位で非正規化**し、業務判断は持たせません
707	
708	なお Martin Fowler の[CQRS](https://martinfowler.com/bliki/CQRS.html) は CQRS の適用に慎重な立場を取っています。多くのシステムでは CQRS の導入が複雑性を増やすだけになりうる、という議論です。本記事の戦略選択フロー（図2）が「結果整合性を許容できるか」を必ず通る作りなのも、この慎重さを共有しているためです。
709	
```

> TOOL

tool_use Edit
id: toolu_01EMfUqXQNkWrfkJuHeBpDPd
```json
{
  "replace_all": false,
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "old_string": "- 迷ったら**C → A → B**の順で検討します。Bは強力ですが運用要素が増えます\n- 結果整合性は技術で消すのではなく、**UXで吸収**します（オプティミスティック更新、バージョン番号、ハイブリッド）\n- リードモデルは**画面・API単位で非正規化**し、業務判断は持たせません",
  "new_string": "- 迷ったら**C → A → B**の順で検討します。これは初期判断の簡略フローで、集計の重さ・検索要件・再構築要件などが絡む場合は別途検討します\n- 結果整合性は技術で消すのではなく、**UXで吸収**します（オプティミスティック更新、バージョン番号、ハイブリッド）\n- リードモデルは**画面・API単位で形を最適化**し、状態遷移や不変条件は持たせません（認可・テナント分離・表示可否などの読み取り固有ルールは Query 側でも必要です）"
}
```

> TOOL

tool_result
id: toolu_01EMfUqXQNkWrfkJuHeBpDPd
```
The file /Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

lint と format をかけて整合性を確認します。

> TOOL

tool_use Bash
id: toolu_013vNYEUvcS8kiQDj8EKoruV
```json
{
  "command": "npm run fmt -- articles/60293061fe34dd.md 2>&1 | tail -20",
  "description": "Run prettier on the article"
}
```

> TOOL

tool_result
id: toolu_013vNYEUvcS8kiQDj8EKoruV
```
> documents@1.0.0 fmt
> prettier -w "**/*.md" articles/60293061fe34dd.md

[error] Unable to expand glob pattern: "**/*.md".
[error] EPERM: operation not permitted, scandir '/Users/135yshr/projects/135yshr/documents/.entire/metadata'
articles/60293061fe34dd.md 86ms
```

> AGENT

冒頭の用語集も本文と整合させます。

> TOOL

tool_use Edit
id: toolu_01NVXTiWS2p7jhh5ttArohGj
```json
{
  "replace_all": false,
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "old_string": "- **リードモデル**: 画面・APIレスポンス向けに非正規化された、読み取り専用のデータ表現です",
  "new_string": "- **リードモデル**: 読み取りユースケースに合わせて設計された、読み取り専用のデータ表現です（非正規化されることが多いものの、必須ではありません）"
}
```

> TOOL

tool_result
id: toolu_01NVXTiWS2p7jhh5ttArohGj
```
The file /Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

lint と textlint も走らせて整合性を確認します。

> TOOL

tool_use Bash
id: toolu_014NKuYUQprQLdVrLifFzc7D
```json
{
  "command": "npm run lint 2>&1 | tail -30 && echo \"---\" && npm run lint:text -- articles/60293061fe34dd.md 2>&1 | tail -30",
  "description": "Run lint and textlint"
}
```

> TOOL

tool_result
id: toolu_014NKuYUQprQLdVrLifFzc7D
```
Summary: 29 error(s)
articles/3d95f47f3d2974.md:9 error MD022/blanks-around-headings Headings should be surrounded by blank lines [Expected: 1; Actual: 0; Above] [Context: "title: "Claude Code のステータスラインに残り利用枠を表示する""]
articles/3d95f47f3d2974.md:16 error MD003/heading-style Heading style [Expected: setext; Actual: atx]
articles/3d95f47f3d2974.md:24 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
articles/3d95f47f3d2974.md:36 error MD003/heading-style Heading style [Expected: setext; Actual: atx]
articles/3d95f47f3d2974.md:53 error MD003/heading-style Heading style [Expected: setext; Actual: atx]
articles/3d95f47f3d2974.md:61 error MD003/heading-style Heading style [Expected: setext; Actual: atx]
articles/3d95f47f3d2974.md:65 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
articles/3d95f47f3d2974.md:92 error MD003/heading-style Heading style [Expected: setext; Actual: atx]
articles/3d95f47f3d2974.md:122 error MD003/heading-style Heading style [Expected: setext; Actual: atx]
articles/3d95f47f3d2974.md:331 error MD003/heading-style Heading style [Expected: setext; Actual: atx]
articles/3d95f47f3d2974.md:333 error MD003/heading-style Heading style [Expected: setext; Actual: atx]
articles/3d95f47f3d2974.md:341 error MD003/heading-style Heading style [Expected: setext; Actual: atx]
articles/3d95f47f3d2974.md:349 error MD003/heading-style Heading style [Expected: setext; Actual: atx]
articles/3d95f47f3d2974.md:362 error MD003/heading-style Heading style [Expected: setext; Actual: atx]
articles/3d95f47f3d2974.md:366 error MD003/heading-style Heading style [Expected: setext; Actual: atx]
articles/3d95f47f3d2974.md:370 error MD003/heading-style Heading style [Expected: setext; Actual: atx]
articles/3d95f47f3d2974.md:385 error MD003/heading-style Heading style [Expected: setext; Actual: atx]
articles/3d95f47f3d2974.md:402 error MD003/heading-style Heading style [Expected: setext; Actual: atx]
articles/3d95f47f3d2974.md:425 error MD003/heading-style Heading style [Expected: setext; Actual: atx]
articles/3d95f47f3d2974.md:436 error MD003/heading-style […]

> AGENT

textlint を対象ファイルだけに絞って実行します。

> TOOL

tool_use Bash
id: toolu_01P6bJTRLDZ87krt6yx5AftU
```json
{
  "command": "npx textlint articles/60293061fe34dd.md 2>&1 | tail -80",
  "description": "Run textlint on target article"
}
```

> TOOL

tool_result
id: toolu_01P6bJTRLDZ87krt6yx5AftU
```
/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md
  531:17413  error    Line 531 sentence length(133) exceeds the maximum sentence length of 100.
Over 33 characters                                       ja-technical-writing/sentence-length
  531:17554  error    Line 531 sentence length(130) exceeds the maximum sentence length of 100.
Over 30 characters                                       ja-technical-writing/sentence-length
  617:20746  error    Line 617 sentence length(129) exceeds the maximum sentence length of 100.
Over 29 characters                                       ja-technical-writing/sentence-length
  694:3      ✓ error  一つ => 1つ
数量を表現し、数を数えられるものは算用数字を使用します。任意の数に置き換えても通用する語句がこれに該当します。  ja-technical-writing/arabic-kanji-numbers
  694:23581  error    Line 694 sentence length(102) exceeds the maximum sentence length of 100.
Over 2 characters                                       ja-technical-writing/sentence-length

✖ 5 problems (5 errors, 0 warnings, 0 infos)
✓ 1 fixable problem.
Try to run: $ textlint --fix [file]
```

> AGENT

該当行を確認して長文を分割します。

> TOOL

tool_use Read
id: toolu_01ESEeygA27NCXsdJ35LzMdi
```json
{
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "offset": 525,
  "limit": 15
}
```

> TOOL

tool_result
id: toolu_01ESEeygA27NCXsdJ35LzMdi
```
525	    version       BIGINT NOT NULL  -- ← outbox.id を転記
526	);
527	```
528	
529	書き込みレスポンスと読み取りリクエストはこんなイメージです。
530	
531	なお、戦略Bのサンプルでは `outbox.Append(ctx, events) error` というシグネチャでしたが、`ExpectedVersion` を返したい場合は **INSERT で採番された outbox.id のうち最大値を返すよう拡張する** 必要があります。たとえば `Append(ctx, events) (lastID int64, err error)` のように変えるか、別途 `outbox.LastInsertedID(ctx)` を呼ぶ、といった形で UseCase 側からバージョンを受け取れるようにします。本記事のサンプルでは簡潔さを優先して error 返しのみにしていますが、戦略Bでスタール検知まで採用するならここを揃えてください。
532	
533	```go
534	// 書き込みレスポンス: outboxにINSERTした最新IDを返す
535	type PlaceOrderResponse struct {
536	    OrderID         string `json:"order_id"`
537	    ExpectedVersion int64  `json:"expected_version"` // ← この値以上が見えるはず
538	}
539	
```

> TOOL

tool_use Edit
id: toolu_011wBsjvbVzcxYUgj7D4Jfqc
```json
{
  "replace_all": false,
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "old_string": "なお、戦略Bのサンプルでは `outbox.Append(ctx, events) error` というシグネチャでしたが、`ExpectedVersion` を返したい場合は **INSERT で採番された outbox.id のうち最大値を返すよう拡張する** 必要があります。たとえば `Append(ctx, events) (lastID int64, err error)` のように変えるか、別途 `outbox.LastInsertedID(ctx)` を呼ぶ、といった形で UseCase 側からバージョンを受け取れるようにします。本記事のサンプルでは簡潔さを優先して error 返しのみにしていますが、戦略Bでスタール検知まで採用するならここを揃えてください。",
  "new_string": "なお、戦略Bのサンプルでは `outbox.Append(ctx, events) error` というシグネチャでした。`ExpectedVersion` を返したい場合は、**INSERT で採番された outbox.id のうち最大値を返すよう拡張**する必要があります。実装方法は2通りです。\n\n- `Append(ctx, events) (lastID int64, err error)` のように戻り値を増やす\n- 別途 `outbox.LastInsertedID(ctx)` を呼んで UseCase 側からバージョンを受け取る\n\n本記事のサンプルは簡潔さを優先して error 返しのみにしていますが、戦略Bでスタール検知まで採用するならここを揃えてください。"
}
```

> TOOL

tool_result
id: toolu_011wBsjvbVzcxYUgj7D4Jfqc
```
The file /Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01MtXrNFNmvgAS59beBZiXag
```json
{
  "command": "npx textlint articles/60293061fe34dd.md 2>&1 | tail -30",
  "description": "Re-run textlint"
}
```

> TOOL

tool_result
id: toolu_01MtXrNFNmvgAS59beBZiXag
```
/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md
  622:20741  error    Line 622 sentence length(129) exceeds the maximum sentence length of 100.
Over 29 characters                                       ja-technical-writing/sentence-length
  699:3      ✓ error  一つ => 1つ
数量を表現し、数を数えられるものは算用数字を使用します。任意の数に置き換えても通用する語句がこれに該当します。  ja-technical-writing/arabic-kanji-numbers
  699:23576  error    Line 699 sentence length(102) exceeds the maximum sentence length of 100.
Over 2 characters                                       ja-technical-writing/sentence-length

✖ 3 problems (3 errors, 0 warnings, 0 infos)
✓ 1 fixable problem.
Try to run: $ textlint --fix [file]
```

> TOOL

tool_use Read
id: toolu_01GtxaUy9RnuTXfwc4ryN1Uc
```json
{
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "offset": 620,
  "limit": 8
}
```

> TOOL

tool_result
id: toolu_01GtxaUy9RnuTXfwc4ryN1Uc
```
620	```
621	
622	データの重複は許容します。リードモデルは**書き込みモデルから導出された結果系**だからです。ただし「いつでも再構築できる」のは自動的にそうなるわけではなく、元データ・イベントログ・再計算バッチ・保持期間を**再構築できるように設計しておく**ことが前提です（戦略Bの再構築可能性の節で触れた通り、Outbox 単独では完全な再構築はできない場合があります）。
623	
624	### 非正規化を恐れない
625	
626	JOINを避けるために、リードモデルでは積極的に値を埋め込みます。`customer_name` を `orders` 側にも持つ、`total_amount` を計算済みで持つ、といった具合です。
627	
```

> TOOL

tool_use Edit
id: toolu_011wtpKkZW288KAMMC7TPhQs
```json
{
  "replace_all": false,
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "old_string": "データの重複は許容します。リードモデルは**書き込みモデルから導出された結果系**だからです。ただし「いつでも再構築できる」のは自動的にそうなるわけではなく、元データ・イベントログ・再計算バッチ・保持期間を**再構築できるように設計しておく**ことが前提です（戦略Bの再構築可能性の節で触れた通り、Outbox 単独では完全な再構築はできない場合があります）。",
  "new_string": "データの重複は許容します。リードモデルは**書き込みモデルから導出された結果系**だからです。\n\nただし「いつでも再構築できる」のは自動的にそうなるわけではありません。元データ・イベントログ・再計算バッチ・保持期間を**再構築できるように設計しておく**ことが前提です。戦略Bの再構築可能性の節で触れた通り、Outbox 単独では完全な再構築はできない場合があります。"
}
```

> TOOL

tool_result
id: toolu_011wtpKkZW288KAMMC7TPhQs
```
The file /Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Read
id: toolu_015JfKA9pSV7saCF8pRvBXje
```json
{
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "offset": 697,
  "limit": 10
}
```

> TOOL

tool_result
id: toolu_015JfKA9pSV7saCF8pRvBXje
```
697	- ペイロードが肥大化して保存・転送コストが増えます
698	
699	「想定するリードモデルに必要な値か」「外部連携に流す前提でも安全か」を一度立ち止まって考えるくらいの粒度が、ちょうどよいバランスです。
700	
701	もう一つ意識したいのは、**ドメインイベントとプロジェクション専用イベント（または投影用メッセージ）を分けて考える**ことです。たとえば `OrderPlaced` に `CustomerName` を載せるのは、注文時点の顧客名スナップショットに業務上の意味（後から顧客名が変わっても注文履歴は当時の名前を保持する、等）があれば自然です。一方で、一覧画面のラベル表示だけのためにドメインイベントへ表示項目を増やすと、ドメインモデルが画面都合に引っ張られます。表示専用の項目は、ドメインイベントを購読する Projector 側で「投影用の中間表現」に詰め替えて保持するなどの分離が有効です。
702	
703	---
704	
705	## まとめ
706	
```

> TOOL

tool_use Edit
id: toolu_017ZcPaSbj7tgTqd8QTFt4AQ
```json
{
  "replace_all": false,
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "old_string": "「想定するリードモデルに必要な値か」「外部連携に流す前提でも安全か」を一度立ち止まって考えるくらいの粒度が、ちょうどよいバランスです。\n\nもう一つ意識したいのは、**ドメインイベントとプロジェクション専用イベント（または投影用メッセージ）を分けて考える**ことです。たとえば `OrderPlaced` に `CustomerName` を載せるのは、注文時点の顧客名スナップショットに業務上の意味（後から顧客名が変わっても注文履歴は当時の名前を保持する、等）があれば自然です。一方で、一覧画面のラベル表示だけのためにドメインイベントへ表示項目を増やすと、ドメインモデルが画面都合に引っ張られます。表示専用の項目は、ドメインイベントを購読する Projector 側で「投影用の中間表現」に詰め替えて保持するなどの分離が有効です。",
  "new_string": "「想定するリードモデルに必要な値か」「外部連携に流す前提でも安全か」を1つひとつ立ち止まって考えるくらいの粒度が、ちょうどよいバランスです。\n\nもう1つ意識したいのは、**ドメインイベントとプロジェクション専用イベント（または投影用メッセージ）を分けて考える**ことです。たとえば `OrderPlaced` に `CustomerName` を載せるのは、注文時点の顧客名スナップショットに業務上の意味があれば自然です（後から顧客名が変わっても注文履歴は当時の名前を保持する、等）。\n\n一方で、一覧画面のラベル表示だけのためにドメインイベントへ表示項目を増やすと、ドメインモデルが画面都合に引っ張られます。表示専用の項目は、ドメインイベントを購読する Projector 側で「投影用の中間表現」に詰め替えて保持するなどの分離が有効です。"
}
```

> TOOL

tool_result
id: toolu_017ZcPaSbj7tgTqd8QTFt4AQ
```
The file /Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01QG91VXff58LcoERqXEmzPA
```json
{
  "command": "npx textlint articles/60293061fe34dd.md 2>&1 | tail -20",
  "description": "Re-run textlint"
}
```

> TOOL

tool_result
id: toolu_01QG91VXff58LcoERqXEmzPA
```
/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md
  701:23581  error  Line 701 sentence length(102) exceeds the maximum sentence length of 100.
Over 2 characters  ja-technical-writing/sentence-length

✖ 1 problem (1 error, 0 warnings, 0 infos)
```

> TOOL

tool_use Read
id: toolu_01Am7BbyEJ7EMZqRBr2GD6a2
```json
{
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "offset": 699,
  "limit": 6
}
```

> TOOL

tool_result
id: toolu_01Am7BbyEJ7EMZqRBr2GD6a2
```
699	「想定するリードモデルに必要な値か」「外部連携に流す前提でも安全か」を1つひとつ立ち止まって考えるくらいの粒度が、ちょうどよいバランスです。
700	
701	もう1つ意識したいのは、**ドメインイベントとプロジェクション専用イベント（または投影用メッセージ）を分けて考える**ことです。たとえば `OrderPlaced` に `CustomerName` を載せるのは、注文時点の顧客名スナップショットに業務上の意味があれば自然です（後から顧客名が変わっても注文履歴は当時の名前を保持する、等）。
702	
703	一方で、一覧画面のラベル表示だけのためにドメインイベントへ表示項目を増やすと、ドメインモデルが画面都合に引っ張られます。表示専用の項目は、ドメインイベントを購読する Projector 側で「投影用の中間表現」に詰め替えて保持するなどの分離が有効です。
704	
```

> TOOL

tool_use Edit
id: toolu_01Rc5wutTEZzzsNn6rB13PA8
```json
{
  "replace_all": false,
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "old_string": "もう1つ意識したいのは、**ドメインイベントとプロジェクション専用イベント（または投影用メッセージ）を分けて考える**ことです。たとえば `OrderPlaced` に `CustomerName` を載せるのは、注文時点の顧客名スナップショットに業務上の意味があれば自然です（後から顧客名が変わっても注文履歴は当時の名前を保持する、等）。",
  "new_string": "もう1つ意識したいのは、**ドメインイベントとプロジェクション専用イベント（または投影用メッセージ）を分けて考える**ことです。\n\nたとえば `OrderPlaced` に `CustomerName` を載せるのは、注文時点の顧客名スナップショットに業務上の意味があれば自然です（後から顧客名が変わっても注文履歴は当時の名前を保持する、等）。"
}
```

> TOOL

tool_result
id: toolu_01Rc5wutTEZzzsNn6rB13PA8
```
The file /Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01TMdwh8SDKbXwWJUR29YDwo
```json
{
  "command": "npx textlint articles/60293061fe34dd.md 2>&1 | tail -10 && npm run fmt -- articles/60293061fe34dd.md 2>&1 | tail -5",
  "description": "Final textlint and format"
}
```

> TOOL

tool_result
id: toolu_01TMdwh8SDKbXwWJUR29YDwo
```
/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md
  703:23581  error  Line 703 sentence length(102) exceeds the maximum sentence length of 100.
Over 2 characters  ja-technical-writing/sentence-length

✖ 1 problem (1 error, 0 warnings, 0 infos)

> prettier -w "**/*.md" articles/60293061fe34dd.md

[error] Unable to expand glob pattern: "**/*.md".
[error] EPERM: operation not permitted, scandir '/Users/135yshr/projects/135yshr/documents/.entire/metadata'
articles/60293061fe34dd.md 81ms (unchanged)
```

> TOOL

tool_result
id: toolu_011ei1P7akeTZy3ePb68fHif
```
700	
701	もう1つ意識したいのは、**ドメインイベントとプロジェクション専用イベント（または投影用メッセージ）を分けて考える**ことです。
702	
703	たとえば `OrderPlaced` に `CustomerName` を載せるのは、注文時点の顧客名スナップショットに業務上の意味があれば自然です（後から顧客名が変わっても注文履歴は当時の名前を保持する、等）。
704	
705	一方で、一覧画面のラベル表示だけのためにドメインイベントへ表示項目を増やすと、ドメインモデルが画面都合に引っ張られます。表示専用の項目は、ドメインイベントを購読する Projector 側で「投影用の中間表現」に詰め替えて保持するなどの分離が有効です。
706	
707	---
```

> TOOL

tool_use Read
id: toolu_011ei1P7akeTZy3ePb68fHif
```json
{
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "offset": 700,
  "limit": 8
}
```

> TOOL

tool_use Edit
id: toolu_01GrpuCKJFtJktGu8Q7ec5Ab
```json
{
  "replace_all": false,
  "file_path": "/Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md",
  "old_string": "たとえば `OrderPlaced` に `CustomerName` を載せるのは、注文時点の顧客名スナップショットに業務上の意味があれば自然です（後から顧客名が変わっても注文履歴は当時の名前を保持する、等）。",
  "new_string": "たとえば `OrderPlaced` に `CustomerName` を載せるのは、注文時点の顧客名スナップショットに業務上の意味があれば自然です。後から顧客名が変わっても、注文履歴は当時の名前を保持できます。"
}
```

> TOOL

tool_result
id: toolu_01GrpuCKJFtJktGu8Q7ec5Ab
```
The file /Users/135yshr/projects/135yshr/documents/articles/60293061fe34dd.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01CLoU2ASsBDpjjo1JF1L2pX
```json
{
  "command": "npx textlint articles/60293061fe34dd.md 2>&1 | tail -10",
  "description": "Final textlint check"
}
```

> TOOL

tool_result
id: toolu_01CLoU2ASsBDpjjo1JF1L2pX
```
(Bash completed with no output)
```

> AGENT

textlint も通りました。最後にprettier も走らせて確認します。

> TOOL

tool_use Bash
id: toolu_013s4qBqei5Hok9hhfwJGdPY
```json
{
  "command": "npx prettier --check articles/60293061fe34dd.md 2>&1 | tail -5 && npx markdownlint-cli2 articles/60293061fe34dd.md 2>&1 | tail -10",
  "description": "Final lint checks"
}
```

> TOOL

tool_result
id: toolu_013s4qBqei5Hok9hhfwJGdPY
```
Checking formatting...
All matched files use Prettier code style!
markdownlint-cli2 v0.21.0 (markdownlint v0.40.0)
Finding: articles/60293061fe34dd.md !node_modules/**
Linting: 1 file(s)
Summary: 0 error(s)
```

> AGENT

lint も textlint もすべて通りました。修正内容を要約します。

**反映した修正（優先5項目）**
1. **重大1（定義）**: 「リードモデル = 非正規化」を弱め、「読み取りユースケースに合わせて設計されたデータ表現」に。表1も「方針」表現に変更し、用語集も整合
2. **重大2（業務ルール）**: 「ビジネスルール不要」を「状態遷移・不変条件は不要、認可/テナント分離/表示可否などの読み取り固有ルールは Query 側にも必要」へ言い換え
3. **重大3（Projector の `continue` バグ）**: 未登録イベントを `continue` で素通りさせる例を修正。エラー停止する例に変え、「あとから増やす」運用に倒すには `MarkUnsupported` 系の状態管理が必要であることを補足
4. **重大4（再構築）**: 「いつでも再構築できる」を「再構築できるように設計しておくことが前提」に修正、Outbox 単独では完全再構築できない旨を再掲
5. **中1（戦略フロー）**: 図2を「簡略版」と明記し、追加で見るべき軸（集計の重さ・検索要件・再構築要件など）を明示。まとめも同調修正

**反映した修正（その他）**
- 中2: 「離れるほど性能向上」を「最適化しやすくなる／必ずしも速くない」に弱化
- 中3: Materialized View に PostgreSQL 前提を明記、VIEW にインデックスを張れない件もPostgreSQL 前提に
- 中4: ドメインイベント肥大化への注意を追記（プロジェクション専用イベントとの分離）
- 軽1: 戦略Aに「同一プライマリDB前提」「リードレプリカ越しでは read-your-writes が崩れ得る」を明記
- 軽3: `outbox.Append` シグネチャと `ExpectedVersion` レスポンスの整合を補足

> TOOL

tool_use Bash
id: toolu_01G7mKahxaDA3xcnV55weLE8
```json
{
  "command": "git status && echo \"---\" && git branch --show-current",
  "description": "Check status and current branch"
}
```

> TOOL

tool_result
id: toolu_01G7mKahxaDA3xcnV55weLE8
```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   articles/60293061fe34dd.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.codex/
	AGENTS.md
	"CQRS_Documents_\346\227\245\346\234\254\350\252\236\350\250\263.docx"
	articles/3d95f47f3d2974.md

no changes added to commit (use "git add" and/or "git commit -a")
---
main
```

> AGENT

main ブランチにいるので、新しいブランチを作成してからコミットします。

> TOOL

tool_use Bash
id: toolu_01KNraNKSuvoGwQsSyX8zTLZ
```json
{
  "command": "git checkout -b docs/cqrs-readmodel-review-fixes && git add articles/60293061fe34dd.md && git diff --staged --stat",
  "description": "Create branch and stage changes"
}
```

> TOOL

tool_result
id: toolu_01KNraNKSuvoGwQsSyX8zTLZ
```
Switched to a new branch 'docs/cqrs-readmodel-review-fixes'
 articles/60293061fe34dd.md | 76 ++++++++++++++++++++++++++++++++--------------
 1 file changed, 54 insertions(+), 22 deletions(-)
```

> TOOL

tool_use Bash
id: toolu_01ShL212kBNYQ3dVwy1BJY4A
```json
{
  "command": "git log --oneline -5",
  "description": "Check recent commit style"
}
```

> TOOL

tool_result
id: toolu_01ShL212kBNYQ3dVwy1BJY4A
```
9a195f9 docs: CQRS リードモデル設計の記事を追加 (#99)
2d0d0b3 ⬆️ deps: bump zenn-cli to 0.4.8
f06427f 🎨 format: tighten bold notation spacing in read model section
ec2bdd0 DDD×CQRSのリードモデル設計記事を追加（下書き） (#98)
91b62aa 🎨 format: unify bullet points to polite tone per review
```

> TOOL

tool_use Bash
id: toolu_0166SjJm4UQ7uv1pHR4Q1VsS
```json
{
  "command": "git commit -m \"$(cat <<'EOF'\n📝 docs: refine read model definition and projector example\n\nReflect critical review feedback on the CQRS read model article:\n- Soften \"read model = denormalized\" definition to design intent\n- Clarify read-side rules: only state transitions/invariants are skippable\n- Fix projector example where unsupported events were silently skipped\n- Note rebuildability requires deliberate design, not automatic\n- Mark strategy selection flow as a simplified initial decision\n- Add PostgreSQL caveats for materialized view and view indexing\n- Caution against domain event bloat for projection convenience\nEOF\n)\" && git status",
  "description": "Create commit and verify"
}
```

> TOOL

tool_result
id: toolu_0166SjJm4UQ7uv1pHR4Q1VsS
```
[STARTED] Backing up original state...
[COMPLETED] Backed up original state in git stash (513d1fe)
[STARTED] Running tasks for staged files...
[STARTED] package.json — 1 file
[STARTED] *.md — 1 file
[STARTED] prettier --write
[COMPLETED] prettier --write
[STARTED] markdownlint-cli2
[COMPLETED] markdownlint-cli2
[STARTED] textlint
[COMPLETED] textlint
[COMPLETED] *.md — 1 file
[COMPLETED] package.json — 1 file
[COMPLETED] Running tasks for staged files...
[STARTED] Applying modifications from tasks...
[COMPLETED] Applying modifications from tasks...
[STARTED] Cleaning up temporary files...
[COMPLETED] Cleaning up temporary files...
[docs/cqrs-readmodel-review-fixes c8d4e87] 📝 docs: refine read model definition and projector example
 1 file changed, 54 insertions(+), 22 deletions(-)
On branch docs/cqrs-readmodel-review-fixes
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.codex/
	AGENTS.md
	"CQRS_Documents_\346\227\245\346\234\254\350\252\236\350\250\263.docx"
	articles/3d95f47f3d2974.md

nothing added to commit but untracked files present (use "git add" to track)
```

> AGENT

コミットが完了しました。

**コミット**: `c8d4e87` 📝 docs: refine read model definition and projector example
**ブランチ**: `docs/cqrs-readmodel-review-fixes`（mainから分岐）
**変更**: `articles/60293061fe34dd.md` — 54 insertions(+), 22 deletions(-)

レビューフィードバックを反映した記事改訂をコミット済みです。lint-staged の Prettier / markdownlint / textlint もすべて通過しました。

**次のステップ候補**
- `git push -u origin docs/cqrs-readmodel-review-fixes` でリモートへプッシュ
- `gh pr create --assignee 135yshr` で PR 作成（CLAUDE.md ルール準拠）
- 追加のレビュー反映が必要なら本ブランチで続けて編集

> TOOL

tool_use Bash
id: toolu_01VGMbTxvUVATa2ifDvNFAct
```json
{
  "command": "git branch --show-current && git status && echo \"---\" && git diff articles/60293061fe34dd.md",
  "description": "Check branch, status and diff"
}
```

> TOOL

tool_result
id: toolu_01VGMbTxvUVATa2ifDvNFAct
```
docs/cqrs-readmodel-review-fixes
On branch docs/cqrs-readmodel-review-fixes
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   articles/60293061fe34dd.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.codex/
	AGENTS.md
	"CQRS_Documents_\346\227\245\346\234\254\350\252\236\350\250\263.docx"
	articles/3d95f47f3d2974.md

no changes added to commit (use "git add" and/or "git commit -a")
---
diff --git a/articles/60293061fe34dd.md b/articles/60293061fe34dd.md
index 0d99eb1..7bcda9d 100644
--- a/articles/60293061fe34dd.md
+++ b/articles/60293061fe34dd.md
@@ -3,7 +3,7 @@ title: "DDD×CQRSのリードモデル設計〜プロジェクションと結果
 emoji: "📖"
 type: "tech"
 topics: ["Go", "DDD", "CQRS", "ReadModel", "設計"]
-published: false
+published: true
 ---
 
 ## はじめに
```

> AGENT

変更は `published: false` → `true` の1行のみ。記事公開のフラグ切り替えです。

> TOOL

tool_use Bash
id: toolu_015K786APZ7u4ofQ7EX1kvxJ
```json
{
  "command": "git add articles/60293061fe34dd.md && git commit -m \"$(cat <<'EOF'\n🚀 release: publish CQRS read model article\n\nFlip the front matter published flag to release the article.\nEOF\n)\" && git log --oneline -3",
  "description": "Commit publish flag change"
}
```

> TOOL

tool_result
id: toolu_015K786APZ7u4ofQ7EX1kvxJ
```
[STARTED] Backing up original state...
[COMPLETED] Backed up original state in git stash (11d0b57)
[STARTED] Running tasks for staged files...
[STARTED] package.json — 1 file
[STARTED] *.md — 1 file
[STARTED] prettier --write
[COMPLETED] prettier --write
[STARTED] markdownlint-cli2
[COMPLETED] markdownlint-cli2
[STARTED] textlint
[COMPLETED] textlint
[COMPLETED] *.md — 1 file
[COMPLETED] package.json — 1 file
[COMPLETED] Running tasks for staged files...
[STARTED] Applying modifications from tasks...
[COMPLETED] Applying modifications from tasks...
[STARTED] Cleaning up temporary files...
[COMPLETED] Cleaning up temporary files...
[docs/cqrs-readmodel-review-fixes e11225e] 🚀 release: publish CQRS read model article
 1 file changed, 1 insertion(+), 1 deletion(-)
e11225e 🚀 release: publish CQRS read model article
c8d4e87 📝 docs: refine read model definition and projector example
9a195f9 docs: CQRS リードモデル設計の記事を追加 (#99)
```

> AGENT

コミットが完了しました。

**コミット**: `e11225e` 🚀 release: publish CQRS read model article
**ブランチ**: `docs/cqrs-readmodel-review-fixes`
**変更**: `articles/60293061fe34dd.md` — `published: false` → `true`

ブランチ上に2コミット積まれた状態です。

**次のステップ候補**
- `git push -u origin docs/cqrs-readmodel-review-fixes` でリモートへプッシュ
- `gh pr create --assignee 135yshr` で PR を作成（CLAUDE.md ルール準拠）
- 公開直前のローカル確認なら `npx zenn preview` でプレビュー