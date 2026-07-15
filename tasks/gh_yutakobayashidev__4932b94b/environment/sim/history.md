[DEVELOPER]: claude codeの設定、plansDirectoryを./plans日シテ

[DEVELOPER]: claude codeの設定、plansDirectoryを./plansにして

[AGENT]: `plansDirectory` はプロジェクト設定ではなくCLI設定なので、`claude config set` で設定します。

[DEVELOPER]: いや、claude-code.nixで永続化できるから

[AGENT]: `claude-code.nix` の `settings.json` に `plansDirectory = "./plans"` を追加しました。`nix run .#switch` で反映できます。