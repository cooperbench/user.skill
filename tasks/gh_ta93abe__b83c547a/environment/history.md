> DEVELOPER

このサイトの改善案を洗い出して

> AGENT

まずローカルのサイト構成と既存の設計ルールを確認します。改善案だけを出す作業なので、コード変更はせずにUI・実装・コンテンツ面を分けて見ます。

> AGENT

Astroベースの個人サイトのようです。次に主要ページ、共通レイアウト、スタイル、設定を読んで、見た目だけでなくSEO・アクセシビリティ・情報設計も含めて改善点を拾います。

> AGENT

トップはかなりミニマルで、コンテンツ一覧系ページが主な導線になっていそうです。候補の優先度を判断するために、一覧ページとカード・ナビゲーション部品を続けて確認します。

> AGENT

この時点では、アクセシビリティの土台は入っていますが、トップの情報量とページ間導線が薄めです。実際のビルド結果と表示状態も確認して、静的コードだけでは見えない問題を見ます。

> AGENT

細かい実装を見ると、SNS一覧はかなり広く網羅され、Blog詳細は読了時間・共有・関連記事まで入っています。一方でトップやWorks詳細は「何をしている人か」「なぜ見るべきか」の文脈が薄いので、改善案はそこを厚めにします。

> AGENT

`pnpm build` は依存関係チェックで `pnpm install` を促され、TTYなしの確認で止まりました。レビュー自体は続けられるので、まずは既存の `node_modules` から直接実行できるかだけ確認します。

> AGENT

既存の `node_modules/.bin/astro` はあるので、pnpmの依存確認を避けてAstroを直接実行してみます。これでビルド可能なら、表示確認まで進めます。

> AGENT

ネットワーク許可付きのAstro直接ビルドは通りました。外部RSS・OG画像生成にネットワーク依存があることも確認できたので、次はローカルプレビューを立てて主要ページの実画面をざっと見ます。

> AGENT

プレビューは `http://127.0.0.1:4321/` で起動しました。主要ページをヘッドレスブラウザで開き、コンソールエラー、横スクロール、基本的な見出し・導線の状態を確認します。

> AGENT

このリポジトリでは `playwright` パッケージ本体ではなく `@playwright/test` が入っている構成でした。そちら経由で同じ確認を続けます。

> AGENT

ヘッドレス確認用のChromiumが未インストールでした。追加インストールで進めるより、既に使えるローカルブラウザ系ツールがあるかを確認して、余計な依存変更を避けます。

> AGENT

ブラウザMCPが使える状態になりました。ローカルページの表示確認に入る前に、このブラウザ操作用スキルの手順だけ読んでから進めます。

> AGENT

ブラウザ接続の手順を確認しました。以降は外部の別ブラウザではなく、この環境の内蔵ブラウザに接続して表示状態を読みます。

> AGENT

内蔵ブラウザに接続できました。まず通常幅でトップと主要一覧ページを読み、必要ならモバイル幅にも切り替えて崩れや導線の弱さを確認します。

> AGENT

このブラウザAPIでは `networkidle` が使えないため、`load` 完了基準に切り替えます。ページ自体は静的生成なので、これで状態確認には足ります。

> AGENT

実表示から、`/tools` で Pagefind UI の読み込みエラー、Blog詳細でH1が2つ出るケース、トップのファーストビューがCTA以外ほぼ空という点が見えました。次にモバイル幅でナビゲーションと長い一覧ページを確認します。

> AGENT

レスポンシブ確認のため一時的にスマホ幅へ切り替えます。確認後は既定幅に戻します。

> AGENT

モバイル幅では横スクロールは出ていません。ハンバーガーメニューの開閉だけ実操作で確認して、一覧に戻ります。

> AGENT

主要な状態確認は済みました。最後にスクリーンショットで見た目の密度と余白感を確認して、改善案の優先度を整理します。

> AGENT

スクリーンショット上も、トップは整っている一方で「実績・最近の活動・読ませる理由」がファーストビューに出ていません。`/tools` は検索枠が表示されるものの、Pagefindスクリプトの読み込み失敗がコンソールに出ているため、該当実装を確認します。

> AGENT

改善案は出せる状態です。根拠を短く添えられるよう、該当箇所の行番号だけ最後に拾います。

> AGENT

行番号も揃いました。プレビューサーバーを止めて、作業で生成された差分が残っていないか確認します。

> AGENT

`pnpm build` の失敗時に `.pnpm-store/` が未追跡で作られていました。こちらで発生させた作業ファイルなので、削除確認を取って片付けます。

> AGENT

ざっと見た限り、優先度高めの改善案はこのあたりです。 **優先度 高** 1. `/tools` の検索を直す ビルド後プレビューで `Pagefind UIの読み込みに失敗しました` が出ています。`dist/pagefind` も生成されていないので、Pagefindの導入か生成コマンド追加が必要です。該当: [src/pages/tools.astro](/Users/ta93abe/Developer/github.com/ta93abe/me/src/pages/tools.astro:913), [src/pages/tools.astro](/Users/ta93abe/Developer/github.com/ta93abe/me/src/pages/tools.astro:1064) 2. トップページに「最近の実績・記事・登壇」を出す 現状のファーストビューは `ta93abe`、肩書き、`View Works` / `Links` のみで、何を見ればよいかの文脈が薄いです。最新Works、最新Blog、最新Slidesを3つ並べるだけでも回遊がかなり改善します。該当: [src/components/landing/HeroSection.astro](/Users/ta93abe/Developer/github.com/ta93abe/me/src/components/landing/HeroSection.astro:6) 3. Blog/Book本文内のH1重複を避ける Blog詳細側でタイトルH1を出しているのに、Markdown本文にも `# 最初のブログ投稿` があり、実表示でH1が2つになっています。本文はH2始まりにするか、render時に最初のH1を除去するのがよいです。該当: [src/pages/blog/[id].astro](/Users/ta93abe/Developer/github.com/ta93abe/me/src/pages/blog/[id].astro:118), [src/content/blog/first-post.md](/Users/ta93abe/Developer/github.com/ta93abe/me/src/content/blog/first-post.md:7) 4. `FilterSort` の状態をURLに同期する タグ選択・並び替えがURLに残らないので、共有・戻る操作・再訪問に弱いです。`?tag=Astro&sort=date-desc` のように反映すると一覧ページのUXが上がります。該当: [src/components/FilterSort.astro](/Users/ta93abe/Developer/github.com/ta93abe/me/src/components/FilterSort.astro:188) **優先度 中** 5. Works詳細に成果指標を追加する `dbt-jobs` は良い内容ですが、一覧と詳細で「何を解決したか」「使うと何が嬉しいか」「成果・特徴」がもう少し前面にあると伝わりやすいです。GitHubリンク、主要機能、技術スタック、導入例、成果を定型ブロック化するとよいです。 6. Linksページをカテゴリ分けする 61リンクがフラットに並んでいて、探すより眺めるページになっています。`Development`、`Writing`、`Talks`、`Social`、`Design` などに分け、主要リンクを上段に固定すると使いやすいです。 7. Toolsページは143件あるのでカテゴリナビを追加する 検索修正に加えて、上部にカテゴリジャンプかstickyな目次があると長大ページでも迷いにくいです。 8. ページタイトルのブランド名を統一する トップは `ta93abe | Software Engineer` ですが、他ページは `Works | Portfolio` です。`SITE.name` が `"Portfolio"` なので、`ta93abe` に寄せた方がOGや検索結果で自然です。該当: [src/config/site.ts](/Users/ta93abe/Developer/github.com/ta93abe/me/src/config/site.ts:1) 9. WebSite schema のSearchActionを実機能に合わせる JSON-LDでは `/tools?q=...` を検索先にしていますが、現状Pagefind未生成かつURLクエリ連動も未確認です。検索を直すか、SearchActionを一旦外すのが安全です。該当: [src/utils/schema.ts](/Users/ta93abe/Developer/github.com/ta93abe/me/src/utils/schema.ts:73) **優先度 低** 10. `transition: all` を避ける UIガイドライン上は避けたい指定です。`FilterSort` のチップなどは `transition: color, background-color, border-color` に絞れます。該当: [src/components/FilterSort.astro](/Users/ta93abe/Developer/github.com/ta93abe/me/src/components/FilterSort.astro:129) 11. 記事/Worksのコードブロックコピーボタンを共通化する Blog詳細とWorks詳細で同じコピー処理が重複しています。小さなクライアントスクリプトか共通コンポーネントに寄せると保守しやすいです。 12. E2EをLinks以外にも広げる 現状のE2EはLinks中心です。トップCTA、モバイルメニュー、Blog詳細H1、Tools検索ロード有無を追加すると回帰検知に効きます。 確認メモ: `./node_modules/.bin/astro build` はネットワーク許可ありで成功、ローカルプレビューでデスクトップ/モバイルを確認しました。横スクロールは見当たらず、モバイルメニューの開閉も動作しています。参考に [Vercel Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md) も照合しました。

> DEVELOPER

https://isitagentready.com/ これで高得点を取りたい。

> AGENT

まずそのスコアサイトが何を評価しているかを確認します。評価基準が外部サービス依存なので、実際のページと公開されている説明を見てから、このリポジトリに入れるべき改善へ落とします。

> AGENT

評価カテゴリは確認できました。次に現状の公開向けファイル（`robots.txt`、`_headers`、サイトマップ設定など）を見て、どこが「すぐ点になる改善」か絞ります。

> AGENT

現状は `robots.txt` と sitemap はありますが、AI向けの明示的な発見導線はほぼ未実装です。スコアサイト側のチェック項目から見ると、まず静的サイトで稼げる「Discoverability」「Bot Access Control」「Protocol Discovery の軽量ファイル」を入れるのが現実的です。

> AGENT

スコアサイト自体は `Link` ヘッダーで MCP Server Card、Agent Skills、API Catalog を露出していました。こちらのサイトにも同系統の静的ファイルとヘッダーを足すのが、静的ポートフォリオとしては一番効率が良さそうです。まず実際の現在スコアをAPIで取ります。

> AGENT

現在の公開URLをスキャンすると Level 1 でした。次のLevel 2条件は `Content-Signal` だけですが、高得点を狙うなら同時に `Link` ヘッダー、`.well-known` 系、Markdown negotiation まで入れたいです。Markdown negotiation は静的ファイルだけでは難しいので、デプロイ構成を確認します。

> AGENT

このサイトは Cloudflare Workers の assets 配信なので、`fetch` ハンドラで「通常は静的アセット」「`Accept: text/markdown` だけ Markdown」を返せます。Worker実装に触るため、Cloudflare Workers向けのローカル手順を確認してから編集します。

> AGENT

Cloudflareの最新Docsでは、Workerコードを書く際はStatic Assetsを使い、リクエスト状態をグローバルに置かず、Promiseを取りこぼさないことが推奨されています。これに沿って、スコア向けの `fetch` ハンドラを小さく足します。

> AGENT

必要な設定は `assets.binding` と `assets.run_worker_first` です。Docs上でも `env.ASSETS.fetch(request)` で静的アセットへフォールバックする形が示されているので、その形で実装します。

> AGENT

実装方針を固めました。やることは、(1) `robots.txt` にContent SignalsとAI bot明示、(2) `/.well-known` と `auth.md` などの発見ファイル追加、(3) WorkerでLinkヘッダー・Markdown negotiation・WebMCP registrationを返す、(4) Wranglerのasset bindingを有効化、です。

> AGENT

スコア判定に通すには、ファイル名だけでなくJSON構造もある程度合っている必要があります。スキャナーの公開フロントエンドJSに検査キーが出ているので、検査が期待する名前・パスを確認します。

> AGENT

一度DNS解決が失敗しました。スコア閾値の確認は補助情報なので、再取得だけ試して、取れなければ既に取れたチェック結果を元に実装を進めます。

> AGENT

Cloudflareのスキャナー自身は、`server-card.json`、Agent Skills index、API Catalogをかなり単純なJSONで公開していました。同じ形に合わせつつ、このサイトで実体のないOAuthや決済は偽装せず、コンテンツサイトとして正直に高得点を狙う構成にします。

> AGENT

現状の実装と設定を確認して、スコアに効く項目だけを実装候補に絞ります。特に `robots.txt`、Worker のレスポンスヘッダー、well-known 系の発見可能性を見ます。

> AGENT

公開スキャンでは Content Site プロファイルの未達が `Link` ヘッダー、Markdown ネゴシエーション、Content-Signal でした。DNS-AID は DNS 側の設定なので、リポジトリ側ではそれ以外を確実に取りに行きます。

> AGENT

Worker は今 `scheduled` だけなので、静的アセットの前に薄い `fetch` を挟めば、ページ本体を大きく変えずに判定対象のレスポンスだけ調整できます。あわせて存在しない well-known が 500 にならないよう、最後は必ず `ASSETS.fetch` に流します。

> AGENT

ここから編集します。スコア目的だけで OAuth や決済を偽装すると後で実利用上の負債になるので、実態に合う「コンテンツサイトとしての発見可能性」を上げる変更に限定します。

> AGENT

判定サイトの説明上も「まず robots.txt と sitemap、homepage の discovery headers/metadata」が最短ルートなので、ここを本体にします。API/OAuth/決済のような実体がない機能はスコア目的で盛らず、`auth.md` には「認証不要」と明示する形にします。

> AGENT

実装範囲を確定しました。`robots.txt` と `_headers` に Content-Signal を入れ、Worker で `/` の Markdown 応答、`Link` ヘッダー、`llms.txt`、`api-catalog`、`auth.md`、MCP/Agent Skills の発見用エンドポイントを返すようにします。

> AGENT

これからファイルを書き換えます。主な変更は `worker/index.ts` の `fetch` 追加、`wrangler.jsonc` の Static Assets binding 有効化、`robots.txt` と `_headers` の Content-Signal、Layout への WebMCP ツール登録です。

> AGENT

編集は入りました。次に型とビルドで Worker の `fetch`、Astro の inline script、Wrangler 設定が破綻していないかを確認します。

> AGENT

Astro build は通りました。`tsc` はこのリポジトリに直接入っていなかったので、代わりに Wrangler の dry-run で Worker と `wrangler.jsonc` の整合性を見ます。

> AGENT

Wrangler dry-run も Worker と assets binding を認識しました。ログファイルをホーム配下へ書こうとして sandbox の警告は出ていますが、dry-run 自体は assets と Worker を束ねて完了しています。続けてローカルで実際のヘッダーと well-known 応答を叩きます。

> AGENT

ローカル Worker が `http://127.0.0.1:8787` で起動しました。ここから scanner が見に行く代表エンドポイントを直接確認します。

> AGENT

代表エンドポイントは期待どおり返っています。`/` は `Link` と `Vary: Accept`、Markdown リクエストは `text/markdown`、存在しない Web Bot Auth は 500 ではなく 404 です。Wrangler から型生成の更新警告が出たので、生成ファイルも合わせます。

> AGENT

`wrangler types` で `worker-configuration.d.ts` も更新しました。最後にもう一度 build/dry-run と差分確認をして、不要な生成物が混ざっていないか確認します。

> AGENT

再ビルドと Wrangler dry-run は通っています。確認用に起動したローカル Worker を止めます。

> AGENT

ローカル Worker は停止済みです。最後に差分を見て、今回の目的から外れる変更やビルド生成物が混ざっていないか確認します。

> AGENT

`.wrangler/` がローカル検証で生成された未追跡ファイルとして残っています。これは今回の実装物ではないので、中身を確認してから掃除します。

> AGENT

`.wrangler/` は空ディレクトリだけでした。未追跡ノイズなので削除します。

> AGENT

生成ノイズは消しました。最終状態を確認します。

> AGENT

想定外に `pnpm-workspace.yaml` と `docs/AGENT_READINESS_PLAN.md` が差分に出ています。私が入れたパッチ対象ではないので、中身を見て今回の作業由来か、既存の並行変更かを切り分けます。

> AGENT

この 2 つは今回のパッチや検証コマンドでは作っていない内容で、かつ `pnpm-workspace.yaml` は `allowBuilds: set this to true or false` という未確定値を含んでいます。今回のスコア改善とは別変更として扱い、ここでは触らずに進めます。

> AGENT

今回触ったコードのフォーマット/静的チェックもかけます。`pnpm` は今別差分の影響を受ける可能性があるので、ローカルの Biome バイナリを直接使います。

> AGENT

Biome はロジックではなく整形差分だけを指摘しました。`worker/index.ts` を Biome で整形します。

> AGENT

整形後にチェックとビルドを再実行します。

> AGENT

整形後も Biome、Astro build、Wrangler dry-run は通りました。最後に差分の最終確認だけ行います。

> AGENT

実装対象の差分はまとまりました。最終回答用に変更箇所の行番号を拾います。

> AGENT

実装しました。主な変更は [worker/index.ts](/Users/ta93abe/Developer/github.com/ta93abe/me/worker/index.ts:397) に Worker `fetch` を追加して、`Link` ヘッダー、Markdown negotiation、`llms.txt`、`api-catalog`、`auth.md`、MCP Server Card、Agent Skills、簡易 MCP endpoint を返すようにした点です。あわせて [robots.txt](/Users/ta93abe/Developer/github.com/ta93abe/me/public/robots.txt:5) に AI bot rules と `Content-Signal`、[_headers](/Users/ta93abe/Developer/github.com/ta93abe/me/public/_headers:11) に `Content-Signal`、[Layout.astro](/Users/ta93abe/Developer/github.com/ta93abe/me/src/layouts/Layout.astro:96) に WebMCP 用の read-only tool 登録を追加しました。[wrangler.jsonc](/Users/ta93abe/Developer/github.com/ta93abe/me/wrangler.jsonc:4) では Static Assets binding と `run_worker_first` を有効化しています。 検証済みです: `biome check`、`astro build`、`wrangler deploy --dry-run` は通過。ローカル Worker でも `/` の `Link`/`Vary`、`Accept: text/markdown`、`/.well-known/api-catalog`、`/.well-known/mcp/server-card.json`、`/.well-known/agent-skills/index.json`、`/auth.md`、`/mcp` を確認しました。 未対応は DNS-AID です。これはリポジトリではなく DNS 側の SVCB/HTTPS レコード設定が必要です。公開スコアへ反映するには、まだ本番デプロイが必要です。 なお、作業中に私の変更とは別に `pnpm-workspace.yaml` と `docs/AGENT_READINESS_PLAN.md` の差分が現れています。今回の実装とは切り離して、そのまま触っていません。 参照: [Is Your Site Agent-Ready?](https://isitagentready.com/), [Cloudflare Static Assets binding](https://developers.cloudflare.com/workers/static-assets/binding/), [Worker script routing](https://developers.cloudflare.com/workers/static-assets/routing/worker-script/), [Static Assets headers](https://developers.cloudflare.com/workers/static-assets/headers/)