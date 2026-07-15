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