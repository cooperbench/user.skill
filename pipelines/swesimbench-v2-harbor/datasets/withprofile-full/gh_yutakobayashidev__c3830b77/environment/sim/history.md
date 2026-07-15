[DEVELOPER]: pdfpc入れて

[AGENT]: pdfpc はPDFプレゼンテーション用のツールですね。どのホストに追加するか確認するため、現在のパッケージ設定を見ます。

[AGENT]: pdfpc はGUIアプリなのでLinux固有パッケージに追加します。

[AGENT]: `nix/modules/linux/home-packages.nix` に `pdfpc` を追加しました。Linux側で `rebuild` すれば使えるようになります。