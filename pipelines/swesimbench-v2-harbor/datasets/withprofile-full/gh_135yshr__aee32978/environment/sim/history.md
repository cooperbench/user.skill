[DEVELOPER]: md2pdf リポジトリに対して、以下の2件の GitHub issue を `gh` CLI で作成してください。 ## 前提 - カレントディレクトリは `135yshr/md2pdf` のローカルクローン、もしくは `--repo 135yshr/md2pdf` を明示してください - `gh auth status` で認証済みであることを先に確認してください - 既存の同名 issue がないか `gh issue list --search "<title>"` で念のためチェックしてください - 各 issue 本文は heredoc またはファイル経由で渡し、改行・コードブロック・日本語が壊れないようにしてください ## 背景（参考リンク、本文に含める） - ユーザーフィードバック元: https://zenn.dev/link/comments/18e8c67d0561bd - 報告者: ppbb さん - OS: macOS（エラーパスの `/var/folders/...` から確定） --- ## Issue 1（バグ） **Title:** playwright module not found when invoked from md2pdf, but works when print_pdf.py is run directly **Labels:** `bug` **Body:** ```markdown ## Description A user reported that running `md2pdf` fails with `ModuleNotFoundError: No module named 'playwright'`, even though `playwright` is installed and `print_pdf.py` works correctly when copied out and executed directly with `python`. Reported via Zenn comment: https://zenn.dev/link/comments/18e8c67d0561bd ## Reproduction ``` $ md2pdf <input>.md md2pdf: conversion failed: print pdf: playwright script failed: exit status 1 output: Traceback (most recent call last): File "/var/folders/t5/qjlms9tx4mg9j_m5106w3g280000gn/T/md2pdf-2994288070/print_pdf.py", line 2, in <module> from playwright.sync_api import sync_playwright ModuleNotFoundError: No module named 'playwright' ``` Workaround that works for the user: - Copy the temp `print_pdf.py` elsewhere and run it directly with `python` → succeeds. ## Suspected Cause The Python interpreter spawned by md2pdf is not the same one where `playwright` was installed via `pip install playwright`. Likely scenarios: - pyenv shim / […]

[AGENT]: 認証済み、ラベルあり、重複なし。本文ファイルを作成して issue を作成します。

[AGENT]: 両 issue を作成しました。 - **Issue #29 (bug):** [playwright module not found when invoked from md2pdf, but works when print_pdf.py is run directly](https://github.com/135yshr/md2pdf/issues/29) - **Issue #30 (enhancement):** [Support custom CSS styling and HTML output](https://github.com/135yshr/md2pdf/issues/30) 事前に `gh auth status` で認証確認、`bug` / `enhancement` ラベルの存在確認、同名 issue の重複が無いことも検索で確認済みです。

[DEVELOPER]: #29のissueに問題が発生する原因を教えてください。 調査が終わっていない場合は、先に調査をしてください

[AGENT]: 調査が終わりました。原因はコード上で明確に特定できます。 ## 根本原因 **該当箇所:** `internal/converter/pdf.go:126-133` ```go func findPython() (string, error) { for _, name := range []string{"python3", "python"} { if p, err := exec.LookPath(name); err == nil { return p, nil } } return "", fmt.Errorf("python3 not found in PATH; ...") } ``` `pdf.go:75-81` でこの結果をそのまま `exec.Command(python, scriptPath)` に渡しているだけで、**「playwright を `import` できる Python」かどうかは一切検証していません**。 ## なぜ「直接 `python` で実行すると成功する」のか ユーザーが `pip install playwright` を打った時の `python3` と、md2pdf が `exec.LookPath("python3")` で解決する `python3` が**別バイナリ**になっているのが原因です。macOS 環境で典型的に起きる組み合わせ: | 状況 | `pip install` した先 | md2pdf が拾う先 | |---|---|---| | pyenv 利用中 | `~/.pyenv/shims/python3` (= 例えば 3.12.x) | shim パスが `PATH` に入っていなければ `/usr/bin/python3` (CLT) | | Homebrew Python 利用中 | `/opt/homebrew/bin/python3` | `PATH` 順次第で `/usr/bin/python3` を先に拾う | | venv アクティブ中 | `$VIRTUAL_ENV/bin/python` | 親プロセスの `PATH` 次第で venv 外の python | ユーザーが `print_pdf.py` を**直接** `python` で叩いた場合は、対話シェル（zsh）の rc が pyenv/Homebrew 用の `PATH` を整えた状態で起動するので、`pip` と同じ Python に解決されて成功します。 ## md2pdf 側でこうなる理由 1. `os/exec` で起動した子プロセスは**親の `PATH` をそのまま継承する**だけで、対話シェルの rc を読み直さない。 2. md2pdf のコードには `PATH` を補強する処理も、`VIRTUAL_ENV` を尊重する処理も、Python 候補を「playwright が import できるか」で篩いにかける処理も無い。 3. `findPython()` は `python3` を最優先で返すので、macOS Command Line Tools の `/usr/bin/python3`（playwright が入っていない素の Apple Python）を引き当てがち。 エラーの `print_pdf.py` 1 行目の `from playwright.sync_api import sync_playwright` で `ModuleNotFoundError` が出ているのは、まさにこの「Python は起動できているが、`site-packages` に playwright が無い」状態の典型的シグネチャです。 ## 補強される根拠（コード上の傍証） - `chromiumPath()` (`converter.go:201-261`) は `CHROME_PATH` という env var フックを持っているのに、Python interpreter にはそれに相当するフックが**存在しない**。 - `flags.go` にも `-mmdc` […]

[AGENT]: 調査完了。原因は `internal/converter/pdf.go:126` の `findPython()` が「playwright が import できる Python かどうか」を検証せず、`exec.LookPath("python3")` で見つかった最初のバイナリ（macOS だと `/usr/bin/python3` などの CLT Python になりがち）をそのまま使う点にあります。

[DEVELOPER]: 報告があった問題を再現することは可能ですか？

[AGENT]: 再現可否を確認するため、まず現在の環境を調べます。

[AGENT]: すでに重要な手掛かりが見えました。`/usr/bin/python3` で `ModuleNotFoundError` が再現しています。続きを確認します。

[AGENT]: 完璧な再現環境です: - `/opt/homebrew/bin/python3` (Python 3.14): playwright **あり** - `/usr/bin/python3` (Apple CLT 3.9.6): playwright **なし** PATH を `/usr/bin:/bin` に絞れば `findPython()` が `/usr/bin/python3` を引き、issue #29 と同一エラーが出るはずです。実際にビルドして再現を試みます。

[AGENT]: **再現成功**。ユーザー報告とビット単位で一致するエラーが出ました（temp パスだけが違うのは想定どおり）。 念のため inverse condition（PATH に Homebrew を含めれば成功すること）も確認します。

[AGENT]: 両条件で挙動が分かれることが確認できました。 ## 再現結果まとめ | PATH | `findPython()` が拾う interpreter | 結果 | |---|---|---| | `/usr/bin:/bin` | `/usr/bin/python3` (Apple CLT 3.9.6, playwright なし) | ❌ `ModuleNotFoundError: No module named 'playwright'` (報告と完全一致) | | `/opt/homebrew/bin:/usr/bin:/bin` | `/opt/homebrew/bin/python3` (3.14, playwright あり) | ✅ PDF 生成成功 | これにより、issue #29 の原因が `internal/converter/pdf.go:126` の `findPython()` に集約されることが**実機で実証**できました。同一マシン上で `PATH` の差だけで成功/失敗が分岐するため、コード以外の要因（OS、依存ライブラリのバージョン、入力ファイル等）は一切関与していません。 ユーザー側で起きている可能性が最も高いシナリオ: - macOS GUI から `md2pdf` を起動した、または対話シェル rc を読まないコンテキストで起動した - 結果として `PATH` に Homebrew/pyenv のパスが入っておらず、`/usr/bin/python3`（Apple CLT）が選ばれた - そこには `pip install playwright` が効いていないため import 失敗

[AGENT]: 再現が確実に取れたので、issue #29 の修正方針（`-python` フラグ追加・`MD2PDF_PYTHON` env var・`import playwright` precheck）はそのまま着手して問題ありません。一時ファイルは片付けました。

[DEVELOPER]: それでは修正を開始してください

[AGENT]: 修正に着手します。まず現状把握のため、README とテスト、既存テストの規約を確認します。

[AGENT]: CHANGELOG はリリース時の自動生成のようなので触りません。実装に入ります。

[AGENT]: `pdf.go` を書き換えます。`findPython` を `*Converter` のメソッドにして、playwright インポート可否で interpreter を篩い分ける precheck を加えます。

[AGENT]: 次は CLI 側。`-python` フラグと `MD2PDF_PYTHON` env var を flags.go に追加します。

[AGENT]: README にオプション欄追加とトラブルシューティングを追加します。

[AGENT]: テストファイルを作成します。fake Python スクリプトで precheck の挙動を検証する作りにします。

[AGENT]: ユニットテストすべて PASS。lint と統合テスト、それから手動再現を確認します。

[AGENT]: 既存コードの 4 件の errcheck warning だけで、私の変更には新規 lint 違反はありません（`pdf.go:109` の `defer f.Close()` も既存のもの）。手動再現に進みます。

[AGENT]: 4 シナリオすべて期待どおりに動作: - **A** 旧挙動だと素の Python traceback だったエラーが、`/usr/bin/python3 (ModuleNotFoundError: No module named 'playwright')` という形で interpreter パスを明示し、`-python` / `MD2PDF_PYTHON` への誘導まで含んだメッセージに変わった - **B** `-python /opt/homebrew/bin/python3` で成功 - **C** `MD2PDF_PYTHON=/opt/homebrew/bin/python3` で成功 - **D** verbose モードで `python: /opt/homebrew/bin/python3 (auto-detected)` を出力

[AGENT]: 修正完了しました。 ## 変更ファイル（issue #29 関連） | File | 変更内容 | |---|---| | `internal/converter/converter.go` | `Config` に `PythonPath` フィールドを追加 | | `internal/converter/pdf.go` | `findPython()` を `*Converter` メソッド化、`canImportPlaywright` で precheck、エラー時に試した interpreter とリメディエーション（`-python` / `MD2PDF_PYTHON`）を提示 | | `cmd/md2pdf/flags.go` | `-python <path>` フラグ追加、`MD2PDF_PYTHON` env var フォールバック、help 文更新 | | `README.md` | Options 表に `-python` 追記、Troubleshooting セクションを追加 | | `internal/converter/pdf_test.go` (新規) | 5 ケース: 明示パス成功 / 明示パス playwright なし / 明示パス存在しない / 自動検出で playwright なし interpreter を弾く / `lastNonEmptyLine` | ## 検証結果 - `go build ./...` ✅ - `go vet ./...` ✅ - `go test ./...` ✅（unit + integration） - 手動再現 4 シナリオ ✅（restricted PATH のエラー改善 / `-python` で復旧 / `MD2PDF_PYTHON` で復旧 / `-v` で interpreter ログ） `website/` 配下の差分は本セッション開始時点で既に変更済みのもので、issue #29 とは無関係です。

[AGENT]: コミット完了。 ## サマリー - **Branch:** `fix/issue-29-python-playwright` - **Commit:** `2927783` — 🐛 fix: detect Python with playwright installed (#29) - **Stats:** 5 files, +239 / −7 ステージしたのは issue #29 修正に関するファイルのみで、`website/` 配下の既存変更や untracked 物（`.claude/`, `public/` 等）には触れていません。 ## 推奨される次のステップ 1. `git push -u origin fix/issue-29-python-playwright` でリモートに push 2. `gh pr create` で issue #29 を closing keyword でクローズする PR を作成（例: PR 本文に `Closes #29`） 3. CI（Go 1.22 / 1.23、`go vet`、golangci-lint、テスト）の通過確認 4. 必要なら `website/` の既存変更を別コミットでまとめる PR 作成まで進めましょうか？

[DEVELOPER]: create pr

[AGENT]: PR を作成しました。 **PR #31:** https://github.com/135yshr/md2pdf/pull/31 - Base: `main` ← Head: `fix/issue-29-python-playwright` - Closes #29 - Title: 🐛 fix: detect Python interpreter that has playwright CI が走るので結果を確認しつつ、必要ならレビュー依頼に進めます。

[DEVELOPER]: 今回の修正で環境変数かパラメータで指定できるようになりましたが、これらの指定がなくて動作できるようにすることは難しいですか？

[AGENT]: 難易度別に2つの選択肢があります。 **A. 既知パスを総当たり (簡単・1〜2 時間)** 今の `findPython()` は PATH 上の `python3`/`python` しか試していません。`mmdcDefaultPaths` と同じノリで Homebrew (`/opt/homebrew/bin/python3`)、pyenv shim (`~/.pyenv/shims/python3`, `~/.anyenv/envs/pyenv/shims/python3`)、macOS Framework Python (`/Library/Frameworks/Python.framework/...`)、`$VIRTUAL_ENV/bin/python` を候補に加え、各々で playwright precheck を回す形にすれば、ユーザー無設定で救える割合が大きく増えます。**欠点:** asdf/conda/nix のような非標準インストールは依然取り逃がす上、候補リストのメンテが必要。 **B. Python+Playwright 自体を捨てる (本質的・1〜2 日)** `chromedp`（Go で Chrome DevTools Protocol を喋るライブラリ）に置き換えれば、Python ランタイム依存をまるごと削除できます。`pdf.go` を書き直すことになりますが、Playwright がやっているのは「Chrome に HTML を読ませて `Page.printToPDF`」だけなので、`chromedp.Run(ctx, chromedp.Navigate, page.PrintToPDF...)` で素直に再現可能です。**欠点:** `wait_for_load_state("networkidle")` や `document.fonts.ready` 相当を自前で書く必要があり、CJK/font 周りの挙動を再検証する必要あり。代わりに「3 つあるランタイム依存（mmdc・Python・Chromium）が 2 つ（mmdc・Chromium）に減る」という大きなリターン。 私のおすすめは **B**。issue #30（HTML 出力モード）も近い領域に手を入れることになるので、合わせて取り組むと無駄が少ないです。とはいえ A も即効性があり、B に着手するまでの繋ぎとして十分機能します。 どちらで進めますか？（A だけ、A→Bの順、いきなり B、いずれもアリです）

[DEVELOPER]: A

[AGENT]: A で進めます。`findPython()` を拡張して、PATH 上の `python3`/`python` で見つからない/playwright が無い場合に Homebrew・pyenv shim・`$VIRTUAL_ENV`・`/usr/bin/python3` 等を順に試すようにします。テスト用にスタブできる構造にして既存テストも更新します。

[AGENT]: 既存テストが well-known パスに干渉されないようスタブを入れ、新規ケースも追加します。

[AGENT]: 全テストパス。フルテスト＋手動再現を実施します。

[AGENT]: 3 シナリオすべて期待どおり。restricted PATH でも `-python` 不要で auto-detect 成功。クリーンアップしてコミットします。

[AGENT]: PR #31 を更新しました。 ## 追加コミット (3116809) **✨ feat: probe well-known Python paths for playwright** `findPython()` の auto-detect 範囲を以下の順で拡張: 1. PATH 上の `python3` / `python`（既存） 2. `$VIRTUAL_ENV/bin/python3`（アクティブな venv） 3. `~/.pyenv/shims/python3`、`~/.anyenv/envs/pyenv/shims/python3` 4. `/opt/homebrew/bin/python3`、`/usr/local/bin/python3` 5. `/usr/bin/python3` 各候補は既存の `import playwright` precheck で検証。存在しないパスは silent skip でエラー出力を汚さない仕様。 ## 検証結果 | シナリオ | 結果 | |---|---| | `PATH=/usr/bin:/bin` | ✅ `/opt/homebrew/bin/python3` を well-known から自動検出 | | `env -i HOME=$HOME`（PATH 完全空） | ✅ 同上、auto-detect 成功 | | `-python` 明示 | ✅ user-specified が引き続き優先 | `go build`, `go vet`, `go test ./...` すべてパス。テストは `extraPythonCandidatesFn` を差し替える `stubExtraPythonCandidates` ヘルパーを通じて well-known パスを制御できるようにし、ホストマシンの実 Python を拾わないように修正しました。 PR: https://github.com/135yshr/md2pdf/pull/31