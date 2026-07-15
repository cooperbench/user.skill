> DEVELOPER

workflow のスライドのコード例はそれぞれ何をやるもの？

> AGENT

workflows ページ (`contents/cloudflare-data-platform/pages/workflows.md`) に2つのコード例があります。 ## 1. TypeScript: `ImageProcessingWorkflow` (pages/workflows.md:14-39) **画像処理パイプライン** を題材に Workflows の核となる 3 機能を見せる例: | ステップ | 役割 | 見せたい機能 | |---|---|---| | `step.do('fetch image')` | R2 から画像を `arrayBuffer()` で取得 | **Workers Bindings 統合** (`this.env.BUCKET`) | | `step.do('generate description')` | Workers AI の LLaVA で「1 文の説明」を生成 | **Workers AI も同じ step で使える** | | `step.waitForEvent('await approval', { timeout: '24 hours' })` | 外部からの `approved` イベントを最大 24 時間待つ | **durable な人間承認待ち** (これが目玉) | | `step.do('publish')` | `public/` プレフィックスで R2 に書き戻す | 承認後の最終ステップ | ★ Insight ───────────────────────────────────── - `step.waitForEvent` の 24h タイムアウトはプロセスが寝てる間も課金されず再開できる — これが「耐久性のある実行エンジン」の象徴で、Lambda + Step Functions 相当の世界を Worker 単体で表現できる - 各 step が冪等な単位として retry されるので、外部 API の重複呼び出しを避けるなら step 境界の切り方が設計上のキモになる ───────────────────────────────────────────────── ## 2. Python: `IngestWorkflow` (pages/workflows.md:126-144) **diamond shape DAG (並列 fan-out → join)** を題材に、TypeScript 版と違う Python SDK 独自の DSL を見せる例: ``` fetch_a ─┐ ├─► merge fetch_b ─┘ ``` - `@step.do()` デコレータで `fetch_a` / `fetch_b` を独立ステップとして宣言 - `merge(fetch_a, fetch_b)` の **引数名がそのまま依存宣言** になる — `fetch_a` という引数があれば `fetch_a` step の完了を待つ - `concurrent=True` で `fetch_a` / `fetch_b` が並列起動 → 両方終わったら `merge` が実行される ★ Insight ───────────────────────────────────── - TypeScript 版は「順序 = `await` の並び」だが、Python 版は「依存 = 引数名」という宣言的 DAG。Airflow / Prefect の世代を経た現代的な書き方で、ML / data pipeline 文脈と相性がいい - 同じ Workflows ランタイムなのに SDK によって DSL が違うのは Cloudflare の典型的なアプローチ (Durable Objects の […]

> DEVELOPER

2つとも実際にデプロイしたい。

> AGENT

実デプロイとなるとスライドのコードだけでは足りない要素 (Bindings 作成・依存関数の中身・トリガー方法) があるので、スコープを合わせさせてください。 ★ Insight ───────────────────────────────────── - スライドのコードは **教育用に切り出された抜粋** で、`this.env.BUCKET` (R2 binding) や `get_a()` / `get_b()` (Python 側) など外部依存が前提になっている — そのままでは `wrangler deploy` に通らない - このリポジトリは Slidev 用に `wrangler.jsonc` が Static Assets 配信向けに構成されているので、Workflows は **別プロジェクト** として作るのが素直 ─────────────────────────────────────────────────

> AGENT

了解。最後にプロジェクト構造だけ確認させてください。 ★ Insight ───────────────────────────────────── - **1 Worker = 1 言語** という制約があるので TypeScript と Python は物理的に別 Worker = 別ディレクトリ (= 別 `wrangler.jsonc`) になる - スライドの例で `await step.waitForEvent(...)` を使っているので、Worker からそのクラスを **`Workflow` binding として自己参照** する設定 (`wrangler.jsonc` の `workflows[]`) が `deploy` 通過の最小要件 — R2 / AI binding は実行時に必要だが `deploy` だけなら省略可 ─────────────────────────────────────────────────

> AGENT

方針確定。`~/Developer/github.com/ta93abe/cf-workflows-examples/` に `ts/` と `py/` を並べる構成で進めます。まずは環境確認とリポジトリ準備から。

> AGENT

タスクを整理して進めます。

> AGENT

docs で要件が固まりました: ★ Insight ───────────────────────────────────── - **TS**: `wrangler.jsonc` に `workflows[]` (name / binding / class_name) を書き、`WorkflowEntrypoint` を export + Worker の fetch handler を default export するだけ。R2 / Workers AI は実行時必要だが deploy 通過には不要 - **Python**: `compatibility_flags: ["python_workers", "python_workflows"]` が必須・`compatibility_date >= 2025-08-01`・Beta 状態。**現行の Python Worker は `Default(WorkerEntrypoint)` クラスに fetch を入れる新仕様** (2025-08-14 以降のデフォルト) なので、スライドの Workflow class とは別に Worker class が必要 - スライドの `step.waitForEvent` / `get_a` 等は deploy 通過に不要 — 残しても良いがダミー実装にする ─────────────────────────────────────────────────

> AGENT

リポジトリ scaffold OK。次は `.gitignore` と README、そして TS Worker から作っていきます。

> AGENT

## TS Worker を組み立て スライドのコードに加えて、`wrangler deploy` を通すために必要な周辺ファイルを用意します。

> AGENT

ここでスライドのコードをそのまま使った Workflow class を書きます。`step.waitForEvent` は実行時に必要だが deploy 通過には残しても OK。Worker から trigger するための fetch handler が追加で必要 (スライドには無い)。

> AGENT

TS Worker dry-run 成功。`env.IMAGE_PROCESSING (ImageProcessingWorkflow) Workflow` が認識されました。Python に進みます。

> AGENT

両方の dry-run が通りました。実際の deploy に進みます。

> AGENT

TS デプロイ成功 → `https://image-processing-workflow.ta93abe.workers.dev`。次は Python。

> AGENT

Python Worker のデプロイがエラー。`workers` モジュールが見つからない問題で、現代の Python Workers は外部 SDK モードがデフォルトで、ローカルに `workers-py>=1.90` を入れて bundle するか、`disable_python_external_sdk` flag で runtime 内蔵 SDK にフォールバックする必要があります。 ★ Insight ───────────────────────────────────── - Python Workers の最近のアップデート (2025-2026) で SDK が **外部パッケージ化** (workers-py) され、`uv` でローカルに入れて deploy 時に bundle する仕組みに変わった - `disable_python_external_sdk` compatibility flag を付けると、旧来通り **runtime 内蔵の `workers` モジュール** を使える — 最小構成で deploy したいときの逃げ道 ─────────────────────────────────────────────────

> AGENT

エラーメッセージそのものが `disable_python_external_sdk` flag を提案してくれているので、それを追加します。

> AGENT

両方のデプロイが成功しました。

> AGENT

TS Worker は実際に応答してます。最終構成と次にやることをまとめます。 ## 完了状況 | | Worker 名 | URL | binding 状態 | |---|---|---|---| | TS | `image-processing-workflow` | https://image-processing-workflow.ta93abe.workers.dev | `IMAGE_PROCESSING (ImageProcessingWorkflow)` 登録済 | | Python | `ingest-workflow-py` | https://ingest-workflow-py.ta93abe.workers.dev | `INGEST (IngestWorkflow)` 登録済 | ★ Insight ───────────────────────────────────── - **R2 / Workers AI binding を `wrangler.jsonc` から省いても deploy は通る** — Cloudflare の検証は「コードが parse できて Workflow class が見つかること」までで、bindings の整合性は実行時チェック。デモを段階的に組み立てやすい設計 - Python は **Beta** ゆえに SDK 配布方式が `workers-py` (uv 経由 bundle) と内蔵 SDK の二系統に分岐していて、`disable_python_external_sdk` が最小デプロイの逃げ道になる。**正式運用なら `uv run pywrangler deploy` パスに移行する** のが推奨 ───────────────────────────────────────────────── ## 実行に進めるには 実際に Workflow を動かすには bindings を追加して再 deploy するだけです。 - **TS の `ImageProcessingWorkflow`**: `wrangler.jsonc` の末尾コメントにある `r2_buckets` と `ai` をアンコメント → R2 バケットを `wrangler r2 bucket create <name>` で作成 → `/start?imageKey=<key>` で trigger → 承認は `instance.sendEvent({ type: 'approved', payload: {} })` を別ルートで実装 - **Python の `IngestWorkflow`**: 現状でも `/` に GET すれば `INGEST.create()` が走る。Workflows ダッシュボードでビジュアライザを確認できる ## ファイル一覧 ``` ~/Developer/github.com/ta93abe/cf-workflows-examples/ ├── .gitignore ├── README.md ├── ts/ │ ├── package.json │ ├── tsconfig.json │ ├── wrangler.jsonc │ └── src/index.ts └── py/ ├── wrangler.jsonc └── src/entry.py ``` リポジトリは git init のみで未コミットです。GitHub に push する or 最初のコミットを作るのが必要なら、その指示ください。

> DEVELOPER

workflow de

> DEVELOPER

workflow で loop とか if else がかけたりするよね。ドキュメント確認して

> AGENT

確認します。Workflows での control flow がどう扱われているか docs を引きます。

> AGENT

書けます。ただし「**determinism rule**」が制約条件として明文化されています。 ## 書けるパターン (公式 docs より) **`if / else` (条件分岐)** ✅ ```typescript const config = await step.do("fetch config", async () => { return await this.env.KV.get("feature-flags", { type: "json" }); }); if (config.enableEmailNotifications) { await step.do("send email", async () => { /* ... */ }); } if (event.payload.userType === "premium") { await step.do("premium processing", async () => { /* ... */ }); } ``` **`for` ループ (動的ステップ展開)** ✅ ```typescript const catList = await step.do("get cat list from KV", async () => { return await this.env.KV.get("cat-list"); }); for (const cat of catList) { await step.do(`get cat: ${cat}`, async () => { return await this.env.KV.get(cat); }); } ``` ## やってはいけないパターン 🔴 **非決定的な値を条件にする** ```typescript if (Math.random() > 0.5) { // ❌ 再起動時に経路が変わる await step.do("maybe do something", async () => {}); } ``` ✅ **step.do の中にラップして deterministic に** ```typescript const shouldProcess = await step.do("decide randomly", async () => { return Math.random() > 0.5; // 結果は step として永続化されるので再起動後も同じ }); if (shouldProcess) { await step.do("conditionally do something", async () => {}); } ``` 🔴 **step 名が非決定的** ```typescript await step.do(`step #1 at: ${Date.now()}`, ...) // ❌ 名前が cache key なので毎回ミスする ``` ★ Insight ───────────────────────────────────── - **核となるルール**: control flow は step **の外** に書ける。ただし条件式・ループ対象は `event.payload` か **過去の step の戻り値** […]

> DEVELOPER

ts の方は loop やif/elseを組み込んでほしい。

> AGENT

スライドの「画像処理」文脈を保ちつつ、loop と if/else が自然に登場するパターンに拡張します。 ★ Insight ───────────────────────────────────── - 画像処理に **loop** を入れるなら「複数画像をバッチ処理」が自然 — `event.payload.imageKeys[]` を受けて `for` で展開、step 名に imageKey を埋め込めば各画像ごとに独立した durable step として cache される - **if/else** は「自動承認 vs 人間承認」が現実味のある分岐 — Workers AI の判定結果 (confidence や `safety` スコア) が閾値を超えたら `step.do` で即 publish、超えなければ `step.waitForEvent` で 24h durable に承認待ち - どちらも **deterministic** に基づく分岐: `imageKeys` は `event.payload` 由来、confidence は前段 step の戻り値由来 — 公式 docs の制約をクリアしている ─────────────────────────────────────────────────

> AGENT

dry-run 通りました。loop/if/else 版の deploy を完了させてから、バウンドワーカーの話に答えます。

> AGENT

loop/if/else 版の deploy も成功。新しい質問に答えます。

> AGENT

## loop/if/else 版 deploy 完了 ``` Uploaded image-processing-workflow (2.97 sec) Deployed image-processing-workflow triggers (3.20 sec) https://image-processing-workflow.ta93abe.workers.dev workflow: image-processing Current Version ID: 80dff4b8-1cc7-40a4-8599-7d826ef3947d ``` 新しいエンドポイント: - `GET /start?imageKeys=a.jpg,b.jpg&threshold=0.7` — バッチ起動 - `GET /approve?id=<id>&imageKey=<key>` — `step.waitForEvent` を release (人間承認パスのとき) 組み込んだパターン: - **loop**: `for (const imageKey of imageKeys)` で各画像ごとに `step.do` (step 名に `imageKey` を埋めて cache key を deterministic に) - **if/else**: `analysis.confidence >= autoApproveThreshold` で `auto-publish` vs `waitForEvent → 承認後 publish` を分岐 --- ## 「バウンドワーカー (bound worker)」について これは Workflows ダッシュボードでの用語で、**Workflow class を物理的に保持している Worker** のことです。 ★ Insight ───────────────────────────────────── - Cloudflare Workflows は「Workflow という独立リソース」ではなく、**Worker の中で `WorkflowEntrypoint` を継承したクラス** として実装される。だから 1 つの Workflow には必ず「そのクラスが書かれている Worker (= script)」が紐付く - ダッシュボードで Workflow を開いたとき表示される「バウンドワーカー」は、その Workflow の `wrangler.jsonc` で `script_name` が指す Worker (省略時は同じ Worker) — 今回のケースだと `image-processing-workflow` Worker が `image-processing` Workflow の bound worker ───────────────────────────────────────────────── ### 今回の関係図 ``` Worker: image-processing-workflow ├── fetch handler (/start, /status, /approve) ├── class ImageProcessingWorkflow ← Workflow class └── binding: IMAGE_PROCESSING ──┐ ↓ Workflow: image-processing ←─── bound worker: image-processing-workflow ``` `wrangler.jsonc` の対応関係: | `wrangler.jsonc` のフィールド | ダッシュボード上の意味 | |---|---| | `name` (top-level): `image-processing-workflow` | **Worker 名** (= バウンドワーカー名) | | `workflows[].name`: `image-processing` | **Workflow 名** | | `workflows[].class_name`: `ImageProcessingWorkflow` | Worker 内のどのクラスが Workflow か | | `workflows[].binding`: `IMAGE_PROCESSING` | Worker の `env` から参照するときの変数名 | | `workflows[].script_name` (省略) […]

> AGENT

No response requested.

> DEVELOPER

workflow から workflow を呼べる？

> AGENT

docs で確認します。

> AGENT

呼べます。`step.do` の中で **child workflow の `create()` を呼ぶ** のが公式パターンです。 ## 公式パターン (docs より) ```typescript export class ParentWorkflow extends WorkflowEntrypoint<Env, Params> { async run(event, step) { const result = await step.do("initial processing", async () => { return { fileKey: "output.pdf" }; }); // child workflow を起動 const childInstance = await step.do("trigger child workflow", async () => { return await this.env.CHILD_WORKFLOW.create({ id: `child-${event.instanceId}`, params: { fileKey: result.fileKey }, }); }); // 親はここで即進む — 子の完了を待たない await step.do("continue with other work", async () => { console.log(`Started child workflow: ${childInstance.id}`); }); } } ``` ★ Insight ───────────────────────────────────── - **Fire-and-forget セマンティクス**: 親は `create()` が返ってきたらすぐ次へ進む。子は完全に独立して走る。「親が子を待つ」が欲しければ自前で `instance.status()` を polling するか、子から `sendEvent` で親に通知 + 親側で `step.waitForEvent` で受ける durable wait パターンを組む - **必ず step.do で wrap する**: `create()` は副作用 (子インスタンス作成) を持つので、step 外で呼ぶと engine 再起動時に **子が二重起動** する可能性がある。これは [Rules of Workflows](https://developers.cloudflare.com/workflows/build/rules-of-workflows/) の「side effects は step に閉じ込めろ」の原則そのもの - **ID を deterministic にする**: `id: \`child-${event.instanceId}\`` のように親 instance ID から導出すると、create 自体が冪等になる (重複 ID は `create` がエラーを返す = 重複防止になる)。`createBatch` を使うと最大 100 件一気に起動できて fan-out パターンに最適 ───────────────────────────────────────────────── ## 設定上の必要事項 呼びたい子 Workflow への binding を **親 Worker の `wrangler.jsonc`** に追加するだけ: ```jsonc { "name": "parent-worker", "workflows": [ { "name": "parent", "binding": "PARENT", "class_name": "ParentWorkflow" }, { "name": "child", "binding": "CHILD_WORKFLOW", "class_name": "ChildWorkflow" // 別 Worker にある場合は "script_name": "child-worker" を追加 } ] […]