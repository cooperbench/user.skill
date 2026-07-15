> DEVELOPER

vphone - macOS で仮想 iOS を動かす
いちばん下へジャンプ
ピン留めされたアイテム
Plat
Plat
1時間前に更新

!
vphone-cli の更新が早すぎるので多分ここの情報は古いです。公式READMEの日本語版を見たほうがいいです

要約
事前準備
macOS 26 以上を用意
64GB くらいの空き容量を確保する(余裕を持って)
SIP, AMFI を無効化 ← つまり、お使いの端末は脆弱になりますわよ
Homebrew
リカバリーモード で

csrutil disable
csrutil allow-research-guests enable

再起動後、通常ターミナルで

sudo nvram boot-args="amfi_get_out_of_my_way=1 -v"

もう一回再起動

必要なツールをインストール:

brew install gnu-tar openssl@3 ldid-procursus sshpass keystone autoconf automake pkg-config libtool git-lfs

ツール
一番簡単な方法は vphone-cli を使う。エンドユーザー向けに最適化されているので README 読んで従うだけで OK。



git clone https://github.com/Lakr233/vphone-cli
cd vphone-cli

後から気づいたが、CFW のインストールまで以下の 1 コマンドで完了するみたい

make setup_machine 

お手軽だ。CFW インストール以後 (make boot から) は手動でコマンド打ち込みが必要。

初回実行時
セットアップ
make setup_tools 
source .venv/bin/activate

これで python venv などが整う

バイナリのパッチなど
make build
make vm_new
make fw_prepare
make fw_patch

復元
二つのターミナルを同時に開いておく必要がある。

ターミナル1    ターミナル2
make boot_dfu (DFU で起動する)    -
(DFU のまま)    make restore_get_shsh
(DFU のまま)    make restore (時間かかる)
実行すると DFU のやつが終了する。

Ramdisk と CFW
二つのターミナルを同時に開いておく必要がある。

ターミナル1    ターミナル2
make boot_dfu (DFU で起動する)    -
(DFU のまま)    make ramdisk_build
(DFU のまま)    make ramdisk_send
(DFU のまま)    iproxy 2222 22 & (バックグラウンドで実行される)
(DFU のまま)    make cfw_install (時間かかる)
実行すると DFU のやつが終了する。

起動
make cfw_install

実行すると仮想 iPhone が立ち上がる。しばらく待つと、bash-4.4# みたいな表示がターミナルに出るので、上のコマンドを実行したターミナル内でそのまま 以下のコマンドを実行する。

export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/bin/X11:/usr/games:/iosbinpack64/usr/local/sbin:/iosbinpack64/usr/local/bin:/iosbinpack64/usr/sbin:/iosbinpack64/usr/bin:/iosbinpack64/sbin:/iosbinpack64/bin'

mkdir -p /var/dropbear
cp /iosbinpack64/etc/profile /var/profile
cp /iosbinpack64/etc/motd /var/motd

# generate SSH host keys (required for SSH to work)
dropbearkey -t rsa -f /var/dropbear/dropbear_rsa_host_key
dropbearkey -t ecdsa -f /var/dropbear/dropbear_ecdsa_host_key

shutdown -h now

実行すると終了する

2回目以降の起動
以下を実行すると iPhone が立ち上がる。

make boot […]

> TOOL

tool_use ToolSearch
id: toolu_01QoHHmNUJVVk2MeguWkh9Wc
```json
{
  "query": "select:Read,Grep,Glob,Agent,Bash",
  "max_results": 5
}
```

> TOOL

tool_result
id: toolu_01QoHHmNUJVVk2MeguWkh9Wc
```
{
  "type": "tool_reference",
  "tool_name": "Read"
}
{
  "type": "tool_reference",
  "tool_name": "Grep"
}
{
  "type": "tool_reference",
  "tool_name": "Glob"
}
{
  "type": "tool_reference",
  "tool_name": "Agent"
}
{
  "type": "tool_reference",
  "tool_name": "Bash"
}
```

> AGENT

面白いですね！vphone の Nix 化について考えてみます。まず現在の darwin パッケージ設定を確認します。

> TOOL

tool_use Read
id: toolu_01Gtp7CDaeHnvPADCtemm3fX
```json
{
  "file_path": "/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/nix/modules/darwin/packages.nix"
}
```

> TOOL

tool_use Read
id: toolu_01LFox4tfWHieMzgtxSYQxJe
```json
{
  "file_path": "/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/nix/modules/home/packages.nix"
}
```

> TOOL

tool_use Grep
id: toolu_01N5ej3GR5PByfkJ5htTuCRH
```json
{
  "pattern": "ldid|sshpass|keystone|gnu-tar|gnutar",
  "path": "/Users/yuta/ghq/github.com/yutakobayashidev/dotnix",
  "output_mode": "content"
}
```

> TOOL

tool_result
id: toolu_01N5ej3GR5PByfkJ5htTuCRH
```
nix/modules/darwin/packages.nix:24:      gnutar
nix/modules/darwin/packages.nix:26:      ldid
nix/modules/darwin/packages.nix:27:      sshpass
nix/modules/darwin/packages.nix:28:      keystone
```

> TOOL

tool_result
id: toolu_01LFox4tfWHieMzgtxSYQxJe
```
     1→# home-managerの共通パッケージリスト（Linux/macOS共通）
     2→{ pkgs, lib, ... }:
     3→
     4→{
     5→  home.packages = with pkgs; [
     6→    # Version Control
     7→    bit-vcs
     8→    git
     9→    git-wt
    10→    git-lfs
    11→    git-filter-repo
    12→    lazygit
    13→    jujutsu
    14→    jj-desc
    15→
    16→    # Development Tools
    17→    nil
    18→    nix-init
    19→    ni
    20→    wabt
    21→
    22→    # CLI Utilities
    23→    curl
    24→    wget
    25→    aria2
    26→    xh
    27→    ripgrep
    28→    fzf
    29→    peco
    30→    jq
    31→    jnv
    32→    tokei
    33→    cloc
    34→    similarity-ts
    35→    lsd
    36→    btop
    37→    zoxide
    38→    tree
    39→    glow
    40→    gum
    41→    vhs
    42→    yazi
    43→    imagemagick
    44→    ffmpeg
    45→    python313Packages.markitdown
    46→    stable.yt-dlp
    47→    halloy
    48→    obsidian
    49→
    50→    # Network Tools
    51→    tunnelto
    52→    speedtest-cli
    53→    bandwhich
    54→    nmap
    55→    dnsutils
    56→
    57→    # Misc
    58→    sl
    59→    fastfetch
    60→  ];
    61→}
    62→
```

> TOOL

tool_result
id: toolu_01Gtp7CDaeHnvPADCtemm3fX
```
     1→# macOS固有パッケージ
     2→# brew-nix: Homebrew cask を Nix パッケージとして管理（バージョン固定・ロールバック可能）
     3→# /Applications へのインストールが必須な cask は homebrew.nix で管理
     4→{ pkgs, ... }:
     5→
     6→{
     7→  home.packages =
     8→    with pkgs;
     9→    [
    10→      # Terminal
    11→      ghostty-bin
    12→      difit
    13→
    14→      # macOS apps (overlay)
    15→      readout
    16→
    17→      # macOS CLI tools
    18→      terminal-notifier
    19→      coreutils
    20→      cocoapods
    21→      watchman
    22→
    23→      # Build tools
    24→      gnutar
    25→      openssl
    26→      ldid
    27→      sshpass
    28→      keystone
    29→      autoconf
    30→      automake
    31→      pkg-config
    32→      libtool
    33→    ]
    34→    # brew-nix casks
    35→    ++ (with pkgs.brewCasks; [
    36→      # Communication
    37→      discord
    38→      element
    39→      mattermost
    40→      # nani # TODO: upstream download URL returns 404
    41→      signal
    42→      simplex
    43→      slack
    44→      telegram
    45→      wechat
    46→
    47→      # AI / LLM
    48→      chatgpt
    49→
    50→      # Productivity
    51→      anki
    52→      figma
    53→      linear-linear
    54→      notion-calendar
    55→
    56→      # Development
    57→      proxyman
    58→      tableplus
    59→
    60→      # Media
    61→      vlc
    62→      ogdesign-eagle
    63→
    64→      # Utilities
    65→      appcleaner
    66→      raycast
    67→      screen-studio
    68→      stats
    69→      yubico-authenticator
    70→
    71→      # Hardware
    72→      arduino-ide
    73→
    74→      # Other
    75→      sidequest
    76→      zoom
    77→    ]);
    78→}
    79→
```

> AGENT

既にビルドツール群は Nix で入れてますね。vphone-cli の Nix 化について、いくつかの方向性を整理します。

## 現状と課題

**既に Nix で管理済み:**
- `gnutar`, `openssl`, `ldid`, `sshpass`, `keystone`, `autoconf`, `automake`, `pkg-config`, `libtool` → `packages.nix:24-31`
- `git-lfs` → 共通パッケージ

**Nix 化できない部分:**
- SIP / AMFI の無効化 → 手動でリカバリーモードから操作が必要
- `nvram boot-args` の設定 → 手動

**Nix 化の余地がある部分:**

### 1. vphone-cli 自体を Nix パッケージ/devShell にする

vphone-cli は `make` + Python venv で動くので、`devShell` や overlay でラップできます。

```nix
# devShell アプローチ（最もシンプル）
devShells.vphone = pkgs.mkShell {
  packages = with pkgs; [
    gnutar openssl ldid sshpass keystone
    autoconf automake pkg-config libtool
    git-lfs python3 gnumake
    libimobiledevice  # iproxy
  ];
  shellHook = ''
    echo "vphone dev environment ready"
  '';
};
```

これなら `nix develop .#vphone` で必要な依存が全部揃った環境に入れます。

### 2. `iproxy` の追加

記事にある `iproxy` コマンドは `libimobiledevice` パッケージに含まれています。現状入ってなさそうなので追加が必要です。

### 3. `make setup_machine` の自動化は限界あり

`make setup_machine` 内部で Homebrew のインストールをしている可能性が高いので、Nix で依存を入れた状態なら `make setup_tools` → `make build` からで十分かもしれません。

## おすすめのアプローチ

一番現実的なのは **devShell** です。理由：

- vphone-cli 自体が頻繁に更新されるので、パッケージとして固めるよりクローンしたリポジトリで `make` する方が追従しやすい
- Python venv は `make setup_tools` が作るので Nix で管理する必要はない
- 必要なのは「依存ツールが揃った環境」であり、devShell がまさにそれ

devShell を追加する方向で進めますか？それとも overlay でもう少し踏み込んだパッケージ化をしたいですか？