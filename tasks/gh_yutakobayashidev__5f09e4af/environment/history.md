> DEVELOPER

pdfpc入れて

> AGENT

pdfpc はPDFプレゼンテーション用のツールですね。どのホストに追加するか確認するため、現在のパッケージ設定を見ます。

> AGENT

pdfpc はGUIアプリなのでLinux固有パッケージに追加します。

> AGENT

`nix/modules/linux/home-packages.nix` に `pdfpc` を追加しました。Linux側で `rebuild` すれば使えるようになります。

> DEVELOPER

brewにもあるはずだけど、ないの?

> AGENT

確認します。

> AGENT

Homebrew に `pdfpc` ありますね（formulaとして）。brews に追加します。

> DEVELOPER

nixpkgsとしてmacにもない？

> AGENT

`aarch64-darwin` で普通にあります。Homebrew のではなく nixpkgs で統一しましょう。 先ほどの homebrew.nix の変更を戻して、macOS の nixpkgs パッケージに追加します。

> AGENT

両OS共通で使えるので、共通パッケージに追加して Linux 側の重複を外します。

> AGENT

nixpkgs に `aarch64-darwin` 対応の `pdfpc` があったので、共通パッケージ (`nix/modules/home/packages.nix`) に追加しました。Linux/macOS 両方で使えます。`rebuild` で反映されます。

> DEVELOPER

vrcxもある？

> AGENT

ありますね。共通パッケージに移動しますか？それとも macOS では使わないですか？