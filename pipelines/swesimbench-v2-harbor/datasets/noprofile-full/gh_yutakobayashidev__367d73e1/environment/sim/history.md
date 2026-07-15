[DEVELOPER]: vphone - macOS で仮想 iOS を動かす いちばん下へジャンプ ピン留めされたアイテム Plat Plat 1時間前に更新 ! vphone-cli の更新が早すぎるので多分ここの情報は古いです。公式READMEの日本語版を見たほうがいいです 要約 事前準備 macOS 26 以上を用意 64GB くらいの空き容量を確保する(余裕を持って) SIP, AMFI を無効化 ← つまり、お使いの端末は脆弱になりますわよ Homebrew リカバリーモード で csrutil disable csrutil allow-research-guests enable 再起動後、通常ターミナルで sudo nvram boot-args="amfi_get_out_of_my_way=1 -v" もう一回再起動 必要なツールをインストール: brew install gnu-tar openssl@3 ldid-procursus sshpass keystone autoconf automake pkg-config libtool git-lfs ツール 一番簡単な方法は vphone-cli を使う。エンドユーザー向けに最適化されているので README 読んで従うだけで OK。 git clone https://github.com/Lakr233/vphone-cli cd vphone-cli 後から気づいたが、CFW のインストールまで以下の 1 コマンドで完了するみたい make setup_machine お手軽だ。CFW インストール以後 (make boot から) は手動でコマンド打ち込みが必要。 初回実行時 セットアップ make setup_tools source .venv/bin/activate これで python venv などが整う バイナリのパッチなど make build make vm_new make fw_prepare make fw_patch 復元 二つのターミナルを同時に開いておく必要がある。 ターミナル1 ターミナル2 make boot_dfu (DFU で起動する) - (DFU のまま) make restore_get_shsh (DFU のまま) make restore (時間かかる) 実行すると DFU のやつが終了する。 Ramdisk と CFW 二つのターミナルを同時に開いておく必要がある。 ターミナル1 ターミナル2 make boot_dfu (DFU で起動する) - (DFU のまま) make ramdisk_build (DFU のまま) make ramdisk_send (DFU のまま) iproxy 2222 22 & (バックグラウンドで実行される) (DFU のまま) make cfw_install (時間かかる) 実行すると DFU のやつが終了する。 起動 make cfw_install 実行すると仮想 iPhone が立ち上がる。しばらく待つと、bash-4.4# みたいな表示がターミナルに出るので、上のコマンドを実行したターミナル内でそのまま 以下のコマンドを実行する。 export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/bin/X11:/usr/games:/iosbinpack64/usr/local/sbin:/iosbinpack64/usr/local/bin:/iosbinpack64/usr/sbin:/iosbinpack64/usr/bin:/iosbinpack64/sbin:/iosbinpack64/bin' mkdir -p /var/dropbear cp /iosbinpack64/etc/profile /var/profile cp /iosbinpack64/etc/motd /var/motd # generate SSH host keys (required for SSH to work) dropbearkey -t rsa -f /var/dropbear/dropbear_rsa_host_key dropbearkey -t ecdsa -f /var/dropbear/dropbear_ecdsa_host_key shutdown -h now 実行すると終了する 2回目以降の起動 以下を実行すると iPhone が立ち上がる。 make boot […]

[AGENT]: 面白いですね！vphone の Nix 化について考えてみます。まず現在の darwin パッケージ設定を確認します。

[AGENT]: 既にビルドツール群は Nix で入れてますね。vphone-cli の Nix 化について、いくつかの方向性を整理します。 ## 現状と課題 **既に Nix で管理済み:** - `gnutar`, `openssl`, `ldid`, `sshpass`, `keystone`, `autoconf`, `automake`, `pkg-config`, `libtool` → `packages.nix:24-31` - `git-lfs` → 共通パッケージ **Nix 化できない部分:** - SIP / AMFI の無効化 → 手動でリカバリーモードから操作が必要 - `nvram boot-args` の設定 → 手動 **Nix 化の余地がある部分:** ### 1. vphone-cli 自体を Nix パッケージ/devShell にする vphone-cli は `make` + Python venv で動くので、`devShell` や overlay でラップできます。 ```nix # devShell アプローチ（最もシンプル） devShells.vphone = pkgs.mkShell { packages = with pkgs; [ gnutar openssl ldid sshpass keystone autoconf automake pkg-config libtool git-lfs python3 gnumake libimobiledevice # iproxy ]; shellHook = '' echo "vphone dev environment ready" ''; }; ``` これなら `nix develop .#vphone` で必要な依存が全部揃った環境に入れます。 ### 2. `iproxy` の追加 記事にある `iproxy` コマンドは `libimobiledevice` パッケージに含まれています。現状入ってなさそうなので追加が必要です。 ### 3. `make setup_machine` の自動化は限界あり `make setup_machine` 内部で Homebrew のインストールをしている可能性が高いので、Nix で依存を入れた状態なら `make setup_tools` → `make build` からで十分かもしれません。 ## おすすめのアプローチ 一番現実的なのは **devShell** です。理由： - vphone-cli 自体が頻繁に更新されるので、パッケージとして固めるよりクローンしたリポジトリで `make` する方が追従しやすい - Python venv は `make setup_tools` が作るので Nix で管理する必要はない - 必要なのは「依存ツールが揃った環境」であり、devShell がまさにそれ devShell を追加する方向で進めますか？それとも overlay でもう少し踏み込んだパッケージ化をしたいですか？

[DEVELOPER]: 1b4086ee970fd428f463a397ab9f145bfd36987a hashと4d6560d9b493e1d383de8af2796a700ce76e7588の部分をdevshellにしたい

[AGENT]: まず該当コミットの変更内容を確認します。

[AGENT]: 内容を把握しました。flake.nix の devShell 構成を確認します。

[AGENT]: 把握しました。やることは： 1. `darwin/packages.nix` からビルドツール群を削除 2. `flake.nix` に `devShells.vphone` を追加（darwin 限定） 3. libplist overlay と ldid はそのまま残す（devShell 内で使うため）

[AGENT]: ビルドが通るか確認します。

[AGENT]: 評価成功。`mkIf` が flake-parts の `perSystem` 内で正しく動くか少し気になるので、Linux 側でも確認します。

[AGENT]: `mkIf` は flake-parts の `perSystem` ではうまく機能しません。条件分岐で devShell 自体を定義しないようにします。

[AGENT]: 両方 OK です。変更内容のまとめ： **`nix/modules/darwin/packages.nix`** — ビルドツール群（gnutar, openssl, ldid, sshpass, keystone, autoconf, automake, pkg-config, libtool）を削除 **`flake.nix`** — `devShells.vphone` を darwin 限定で追加。上記ツールに加えて `git-lfs`, `python3`, `gnumake`, `libimobiledevice`（iproxy）も含む 使い方： ```bash nix develop .#vphone ``` これで vphone-cli に必要な依存が全て揃った環境に入れます。常用パッケージとして入れる必要がなくなったので、通常の macOS 環境がクリーンになります。

[DEVELOPER]: コミットして

[AGENT]: `nvim/lazy-lock.json` は前回のコミットで入った変更が revert されている形ですが、これは意図した変更ではなさそうなので、vphone 関連の2ファイルだけコミットします。

[AGENT]: コミット完了しました (`0cf57aa`)。pre-commit フックも全てパスしています。

[DEVELOPER]: どうやってvphone

[AGENT]: のことを知りましたか？ということでしょうか、それとも vphone の使い方について聞きたいですか？ 質問の続きが途切れているようなので、意図を教えてください。

[DEVELOPER]: どうやってvphoneこの状態でセットアップすればいいの

[AGENT]: 手順はこうなります： ```bash # 1. devShell に入る（依存ツールが全部揃う） nix develop .#vphone # 2. vphone-cli をクローン git clone https://github.com/Lakr233/vphone-cli cd vphone-cli # 3. セットアップ（Python venv 等） make setup_tools source .venv/bin/activate # 4. ビルド〜復元〜CFW インストール make build make vm_new make fw_prepare make fw_patch # ... 以降は元記事の手順通り（DFU起動、restore、ramdisk、cfw_install） # 5. 2回目以降の起動 make boot iproxy 22222 22222 & # SSH iproxy 5901 5901 & # VNC ``` SIP/AMFI の無効化とリブートは事前に手動で済ませておく必要があります。devShell はあくまでビルドツール群を提供するだけなので、`make` 以降の操作は vphone-cli の README に従う形です。 なお `nix develop .#vphone` を抜けると依存ツールは PATH から消えるので、vphone を使うときは常に devShell 内で作業してください。

[DEVELOPER]: push

[AGENT]: プッシュ完了しました。

[DEVELOPER]: nix develop .#vphoneは~/ghq/github.com/Lakr233/vphone-cliで使いたいんだけど

[AGENT]: `direnv` を使えば、vphone-cli ディレクトリに入るだけで自動的に devShell が有効になります。

[AGENT]: direnv が既に設定されてますね。vphone-cli ディレクトリに `.envrc` を置けば OK です。

[AGENT]: 設定完了です。これで `~/ghq/github.com/Lakr233/vphone-cli` に `cd` するだけで自動的に vphone の devShell が有効になります。 `.envrc` は vphone-cli のローカルファイルなので git 管理外です（vphone-cli の `.gitignore` に入ってなければ `git diff` に出ますが、あなたのリポジトリには影響しません）。

[DEVELOPER]: dev shell作ったはいいが、インストールスクリプトで結局homebrewを使わされそうだ、、yuta@M2-MacBook-Air  ~/ghq/github.com/Lakr233/vphone-cli   main  make setup_machine SUDO_PASSWORD="" \ NONE_INTERACTIVE="" \ zsh scripts/setup_machine.sh \ \ \ [*] setup_machine mode: base, project_setup=run, non_interactive=0 === Installing Homebrew dependencies === ideviceinstaller: installing ✔︎ JSON API cask.jws.json Downloaded 15.4MB/ 15.4MB ✔︎ JSON API formula.jws.json Downloaded 31.9MB/ 31.9MB ==> Fetching downloads for: ideviceinstaller ✔︎ Bottle Manifest ideviceinstaller (1.2.0) Downloaded 23.6KB/ 23.6KB ✔︎ Bottle Manifest ca-certificates (2025-12-02) Downloaded 2.0KB/ 2.0KB ✔︎ Bottle ca-certificates (2025-12-02) Downloaded 131.8KB/131.8KB ✔︎ Bottle Manifest openssl@3 (3.6.1) Downloaded 11.8KB/ 11.8KB ✔︎ Bottle Manifest xz (5.8.2) Downloaded 11.8KB/ 11.8KB ✔︎ Bottle Manifest libplist (2.7.0) Downloaded 10.2KB/ 10.2KB ✔︎ Bottle Manifest libimobiledevice-glue (1.3.2) Downloaded 10.8KB/ 10.8KB ✔︎ Bottle Manifest zstd (1.5.7_1) Downloaded 13.2KB/ 13.2KB ✔︎ Bottle Manifest libusbmuxd (2.1.1) Downloaded 12.5KB/ 12.5KB ✔︎ Bottle libplist (2.7.0) Downloaded 170.6KB/170.6KB ✔︎ Bottle Manifest libtatsu (1.0.5) Downloaded 16.6KB/ 16.6KB ✔︎ Bottle Manifest libimobiledevice (1.4.0) Downloaded 22.6KB/ 22.6KB ✔︎ Bottle Manifest lz4 (1.10.0) Downloaded 13.8KB/ 13.8KB ✔︎ Bottle lz4 (1.10.0) Downloaded 279.7KB/279.7KB ✔︎ Bottle Manifest libzip (1.11.4_1) Downloaded 11.4KB/ 11.4KB ✔︎ Bottle Manifest libtasn1 (4.21.0) Downloaded 7.9KB/ 7.9KB ✔︎ Bottle xz (5.8.2) Downloaded 764.3KB/764.3KB ✔︎ Bottle libtasn1 (4.21.0) Downloaded 165.3KB/165.3KB ✔︎ Bottle zstd (1.5.7_1) Downloaded 793.6KB/793.6KB ✔︎ Bottle libimobiledevice-glue (1.3.2) Downloaded 76.3KB/ 76.3KB ✔︎ Bottle […]

[AGENT]: セットアップスクリプトの中身を確認して、Homebrew を迂回できるか見てみます。

[AGENT]: `install_brew_deps`（660-678行目）が Homebrew を要求しています。`make setup_machine` は `--skip-project-setup` オプションがあるものの、Homebrew インストールはスキップされません。 重要なのは `ideviceinstaller` と `wget`, `python@3.13` が devShell に足りていない点です。対応策： 1. devShell に不足パッケージを追加 2. `make setup_machine --skip-project-setup` で Homebrew + setup_tools をスキップして使う、もしくは `make setup_tools` と `make build` を個別に実行 Makefile を確認して、`setup_tools` が何をしているか見ます。

[AGENT]: なるほど。`setup_tools.sh` も `brew list` / `brew install` を使っています（32-46行目）。さらに `brew --prefix openssl@3` で trustcache のビルドに使っています（62行目）。 問題は vphone-cli のスクリプトが Homebrew の存在を前提としている点です。完全に Homebrew を排除するのは難しいですが、**Nix で依存が既に PATH にある状態なら、Homebrew 部分をスキップ**できます。 現実的な使い方としては： ```bash # vphone-cli ディレクトリに cd（direnv で devShell 自動有効化） cd ~/ghq/github.com/Lakr233/vphone-cli # setup_tools の brew 部分はスキップして、個別に必要なステップだけ実行 # もしくは setup_machine --skip-project-setup で brew + setup_tools をスキップ make setup_tools # brew 部分は失敗するが、それ以外は動く可能性あり # または setup_machine 全自動で --skip-project-setup make setup_machine SKIP_PROJECT_SETUP=1 ``` ただし `setup_tools.sh` の trustcache ビルドが `brew --prefix openssl@3` を参照するので、そこも壊れます。devShell 側で `OPENSSL_PREFIX` 等の環境変数を設定するか、もしくは **brew を入れたまま `make setup_machine` を一発で通す**のが一番楽です。 vphone-cli はスクリプトが全面的に Homebrew 前提で書かれているので、Nix で完全に置き換えるには各スクリプトへのパッチが必要になり、upstream の更新に追従しにくくなります。現実的には： 1. **devShell はビルドツールの宣言的管理として残す**（`nix develop .#vphone` で何が必要かわかる） 2. **実際のセットアップは `make setup_machine` をそのまま使う**（Homebrew で重複インストールされるが実害なし） Homebrew 排除にこだわりますか？それとも `make setup_machine` で普通にセットアップして進めますか？

[DEVELOPER]: make setup_machineでいいが、nixの設定で宣言されていないhomebrewは消されるようになってるはず

[AGENT]: `cleanup = "uninstall"` なので、`brews` に宣言されていない formula は `nix run .#switch` 時に消されますね。 vphone-cli が必要とする brew formula を `homebrew.nix` の `brews` に追加する必要があります。`setup_machine.sh:663-665` によると： - `ideviceinstaller`, `wget`, `gnu-tar`, `openssl@3`, `ldid-procursus`, `sshpass`, `keystone`, `autoconf`, `automake`, `pkg-config`, `libtool`, `git-lfs`, `python@3.13` ただし `setup_tools.sh` は自前で libimobiledevice をビルドするし、brew の formula のうち Nix devShell で既に提供しているものも多いです。一番確実なのは **brew formula として宣言して `make setup_machine` をそのまま通す**方向です。 devShell はもう不要になるので削除して、代わりに `homebrew.nix` の `brews` に追加しましょうか？それとも devShell は残しつつ brew にも宣言を入れますか？

[DEVELOPER]: devShell はもう不要になるので削除して、代わりに homebrew.nix の brews に追加

[AGENT]: 次に flake.nix から vphone devShell を削除し、darwin/packages.nix からビルドツール群も削除されていることを確認します。

[AGENT]: libplist overlay と ldid overlay も Nix パッケージとしてはもう使わないので削除します。

[AGENT]: libplist overlay は ldid (Nix パッケージ) のためだけのものだったので、もう不要です。

[AGENT]: darwin/packages.nix も確認。

[AGENT]: ビルドツールは既に消えています。ビルドを確認します。

[AGENT]: OK です。変更まとめ： - **`homebrew.nix`** — vphone-cli の依存 formula を `brews` に追加（`gnu-tar`, `openssl@3`, `ldid-procursus`, `sshpass`, `keystone`, `autoconf`, `automake`, `pkg-config`, `libtool`, `git-lfs`, `python@3.13`, `ideviceinstaller`, `wget`） - **`flake.nix`** — `devShells.vphone` を削除 - **`nix/overlays/libplist.nix`** — 削除（Nix の ldid 用だったので不要） - **`nix/overlays/default.nix`** — libplist.nix の参照を削除 - **`vphone-cli/.envrc`** — 削除 これで `nix run .#switch` 後に `make setup_machine` がそのまま通るようになります。コミットしますか？