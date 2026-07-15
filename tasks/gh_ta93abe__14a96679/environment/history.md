> DEVELOPER

zellij のSend-keyを使ってOpenCodeに指示出せる？

> AGENT

はい、できます。zellij には外部からペインへキー入力を送り込むアクションがあり、TUI で動く OpenCode に対して文字列やキーを流し込めます。

## 使う主なコマンド

```bash
# 文字列をそのまま入力（改行は送られない）
zellij action write-chars "テスト書いて"

# 生のバイト/キーコードを送る（13 = Enter）
zellij action write 13
```

`write-chars` は文字を打ち込むだけで Enter は送られないので、**入力 → Enter で送信**という2段構えが基本です。

```bash
zellij action write-chars "src/foo.ts のバグを直して" && zellij action write 13
```

## 特定ペインへ送る場合

`zellij action` はデフォルトで「フォーカス中のペイン」に送ります。OpenCode が別ペインにいるなら、先にフォーカスを移す必要があります。

```bash
# OpenCode のペインにフォーカス → 入力 → Enter
zellij action focus-next-pane
zellij action write-chars "指示内容"
zellij action write 13
```

より確実にやるなら、ペインに名前を付けておくか、`--session` を指定して別セッションのターゲットへ送る方法もあります。

```bash
zellij --session <session-name> action write-chars "..."
```

## 注意点

- **改行を含む長文**: `write-chars` で `\n` を入れると OpenCode 側が途中送信と解釈する場合があるので、複数行プロンプトは1行に整形するか、貼り付け（bracketed paste）を意識した方が安全です。
- **送信キーの確認**: OpenCode の送信キーが Enter なのか別キー（例: Ctrl+Enter）なのかで `write` に渡すコードが変わります。Enter は `13`、Ctrl+J は `10` など。
- **フォーカス管理**: スクリプト化するとフォーカスがずれて誤爆しやすいので、`dump-layout` でペイン構成を確認しつつ組むと安定します。

---

`★ Insight ─────────────────────────────────────`
- `write-chars`（文字列）と `write`（生バイト/キーコード）は別物で、「入力」と「送信(Enter)」を分けて考えるのが zellij でTUIを操作する際の定石です。
- OpenCode のようなTUIエージェントは「フォーカス中のペインの標準入力」を読むだけなので、zellij 側は単にキーストロークを流すだけ。エージェント間連携の特別なAPIは不要で、ターミナル入力をエミュレートしているだけです。
`─────────────────────────────────────────────────`

やりたいのは「Claude Code (このセッション) から OpenCode に自動で指示を流す」ような連携でしょうか？ それなら送信ラッパースクリプトを用意すると便利なので、必要なら作ります。