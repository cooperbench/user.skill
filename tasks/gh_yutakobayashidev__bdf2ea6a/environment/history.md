> DEVELOPER

https://github.com/tokoroten/prompt-review/blob/main/.claude/skills/prompt-reviewのinputを追加して

> TOOL

tool_use ToolSearch
id: toolu_014boVnfshvXbeycCZf6iXiF
```json
{
  "query": "select:WebFetch,Read,Glob,Write,Edit,Bash,Agent",
  "max_results": 7
}
```

> TOOL

tool_result
id: toolu_014boVnfshvXbeycCZf6iXiF
```
{
  "type": "tool_reference",
  "tool_name": "WebFetch"
}
{
  "type": "tool_reference",
  "tool_name": "Read"
}
{
  "type": "tool_reference",
  "tool_name": "Glob"
}
{
  "type": "tool_reference",
  "tool_name": "Write"
}
{
  "type": "tool_reference",
  "tool_name": "Edit"
}
{
  "type": "tool_reference",
  "tool_name": "Bash"
}
{
  "type": "tool_reference",
  "tool_name": "Agent"
}
```

> AGENT

まず、指定されたGitHubリポジトリのスキルファイルの内容を取得します。

> TOOL

tool_use Bash
id: toolu_01DTMKpmp3abDqt4oBd7FwVV
```json
{
  "command": "gh api repos/tokoroten/prompt-review/contents/.claude/skills/prompt-review -q '.content' | base64 -d",
  "description": "Fetch prompt-review skill content from GitHub"
}
```

> TOOL

tool_use Glob
id: toolu_01LYbaiiYUgbyT7CJTatLKp2
```json
{
  "pattern": "agents/skills/**/*"
}
```

> TOOL

tool_result
id: toolu_01DTMKpmp3abDqt4oBd7FwVV
```
expected an object but got: array ([{"_links":{"git":"https: ...])
```

> TOOL

tool_result
id: toolu_01LYbaiiYUgbyT7CJTatLKp2
```
/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/agents/skills/oura-daily-watch/scripts/__pycache__/oura_fetch.cpython-313.pyc
/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/agents/skills/oura-daily-watch/scripts/oura_fetch.py
/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/agents/skills/check-similarity/SKILL.md
/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/agents/skills/dce/SKILL.md
/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/agents/skills/gha-lint/SKILL.md
/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/agents/skills/markitdown/SKILL.md
/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/agents/skills/oura-daily-watch/SKILL.md
/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/agents/skills/social-digest/SKILL.md
/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/agents/skills/social-digest/scripts/fxtweet.ts
/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/agents/skills/social-digest/scripts/social-digest.ts
/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/agents/skills/social-digest/src/renderDaily.ts
/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/agents/skills/social-digest/src/socialDigest.ts
/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/agents/skills/social-digest/test/renderDaily.test.ts
/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/agents/skills/social-digest/test/socialDigest.test.ts
/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/agents/skills/speakerdeck/SKILL.md
/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/agents/skills/speakerdeck/scripts/speakerdeck.ts
/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/agents/skills/social-digest/scripts/render-daily.ts
```

> AGENT

ディレクトリのようなので、中身を確認します。

> TOOL

tool_use Bash
id: toolu_01CntJkNTfYBkepsV82iU8HL
```json
{
  "command": "gh api repos/tokoroten/prompt-review/contents/.claude/skills/prompt-review --jq '.[].name'",
  "description": "List files in prompt-review skill directory"
}
```

> TOOL

tool_result
id: toolu_01CntJkNTfYBkepsV82iU8HL
```
SKILL.md
references
scripts
```

> TOOL

tool_use Bash
id: toolu_01PDq7dAAfxKcJxmmZeea8uu
```json
{
  "command": "gh api repos/tokoroten/prompt-review/contents/.claude/skills/prompt-review/SKILL.md --jq '.content' | base64 -d",
  "description": "Fetch SKILL.md content"
}
```

> TOOL

tool_use Bash
id: toolu_01CS8JJZtsG47VcYY3nd3BsS
```json
{
  "command": "gh api repos/tokoroten/prompt-review/contents/.claude/skills/prompt-review/scripts --jq '.[].name'",
  "description": "List scripts directory"
}
```

> TOOL

tool_use Bash
id: toolu_01CiJ1vy7CpYQRctDqVfnDt2
```json
{
  "command": "gh api repos/tokoroten/prompt-review/contents/.claude/skills/prompt-review/references --jq '.[].name'",
  "description": "List references directory"
}
```

> TOOL

tool_result
id: toolu_01PDq7dAAfxKcJxmmZeea8uu
```
---
name: prompt-review
description: >
  このスキルは、ユーザーが「プロンプトをレビューして」「対話履歴を分析して」「理解度を診断して」
  と依頼したとき、または /prompt-review で呼び出されたときに使用する。
  過去のAIエージェント対話履歴（Claude Code, GitHub Copilot Chat, Cline, Roo Code, Windsurf,
  Antigravity）を読み取り、技術理解度・プロンプティングパターン・AI依存度を推定してレポートを生成する。
disable-model-invocation: true
allowed-tools: Read, Write, Glob, Grep, Bash
context: fork
---

# prompt-review スキル

ユーザーの過去のAIエージェント対話履歴を分析し、技術理解度・プロンプティングパターン・AI依存度を推定してレポートを生成する。レポートは日本語で `reports/prompt-review-YYYY-MM-DD.md` に書き出す。

## 引数の処理

`$ARGUMENTS` を解析し、以下のルールで引数を処理する:

- 数値のみ → **日数フィルタ**（例: `30` → 過去30日分）
- 文字列のみ → **プロジェクト名フィルタ**（部分一致）
- 文字列 + 数値 → **プロジェクト名** + **日数フィルタ**（例: `yonshogen 30`）
- 引数なし → 全プロジェクト横断、過去7日分（デフォルト）

## ステップ1: データ収集（スクリプト実行）

前処理スクリプト [scripts/collect.py](scripts/collect.py) を実行してデータを収集する。
このスクリプトは Claude Code, GitHub Copilot Chat, Cline, Roo Code, Windsurf, Antigravity の
ログを自動検出し、フィルタ済みのJSON を標準出力に返す。

### 引数からスクリプトオプションを組み立てる

`$ARGUMENTS` を解析し、Bash で以下のように実行する:

```bash
python ~/.claude/skills/prompt-review/scripts/collect.py [OPTIONS] > /tmp/prompt-review-data.json
```

- 引数なし → オプションなし（デフォルト: 過去7日分）
- 数値のみ（例: `30`） → `--days 30`
- `all` または `0` → `--days 0`（全期間）
- 文字列のみ（例: `yonshogen`） → `--project yonshogen`
- 文字列 + 数値（例: `yonshogen 30`） → `--project yonshogen --days 30`

**重要**: スクリプトのパスは、このスキルファイルからの相対パスではなく、スキルが格納されているプロジェクトの `.claude/skills/prompt-review/scripts/collect.py` の絶対パスを使うこと。現在の作業ディレクトリ（`cwd`）を基準に `.claude/skills/prompt-review/scripts/collect.py` を指定する。

### 出力の読み取り

スクリプト実行後、`/tmp/prompt-review-data.json` を Read で読み込む。

出力JSON構造:
```json
{
  "summary": {
    "total_messages": 2616,
    "detected_tools": ["Claude Code", "GitHub Copilot Chat"],
    "filter_days": null,
    "filter_project": null
  },
  "sources": [
    {
      "tool": "Claude Code",
      "status": "検出",
      "messages": [
        {"text": "プロンプト本文", "timestamp": "2025-09-29 03:16", "project": "yonshogen"}
      ],
      "period": "2025-09-29 03:16 〜 2026-03-12 04:58"
    }
  ],
  "project_stats": {
    "farbrain": {"count": 668, "tools": ["Claude Code"]}, […]

> TOOL

tool_result
id: toolu_01CS8JJZtsG47VcYY3nd3BsS
```
collect.py
```

> TOOL

tool_result
id: toolu_01CiJ1vy7CpYQRctDqVfnDt2
```
data-sources.md
report-template.md
```

> AGENT

スキルの全ファイルを取得します。

> TOOL

tool_use Bash
id: toolu_01Reb7EfYpa4X3x5jRX7RKfr
```json
{
  "command": "gh api repos/tokoroten/prompt-review/contents/.claude/skills/prompt-review/scripts/collect.py --jq '.content' | base64 -d",
  "description": "Fetch collect.py script"
}
```

> TOOL

tool_use Bash
id: toolu_01MSyRsAyaHW5iwCvwgsPQiK
```json
{
  "command": "gh api repos/tokoroten/prompt-review/contents/.claude/skills/prompt-review/references/data-sources.md --jq '.content' | base64 -d",
  "description": "Fetch data-sources.md reference"
}
```

> TOOL

tool_use Bash
id: toolu_01Q7SQXr3xCGE6QN9Et3yVyo
```json
{
  "command": "gh api repos/tokoroten/prompt-review/contents/.claude/skills/prompt-review/references/report-template.md --jq '.content' | base64 -d",
  "description": "Fetch report-template.md reference"
}
```

> TOOL

tool_use Read
id: toolu_01A4CfB6HpDeCVspzDWLakAp
```json
{
  "file_path": "/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/nix/modules/home/agent-skills.nix"
}
```

> TOOL

tool_result
id: toolu_01Reb7EfYpa4X3x5jRX7RKfr
```
#!/usr/bin/env python3
"""
prompt-review スキル用データ収集スクリプト

対話履歴を各AIツールから収集し、分析用に整形して標準出力にJSON形式で出力する。

使い方:
    python collect.py                          # 全プロジェクト、全期間
    python collect.py --days 30                # 過去30日分
    python collect.py --project yonshogen      # 特定プロジェクト
    python collect.py --project yonshogen --days 30
"""

import argparse
import json
import os
import platform
import re
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path


# クレデンシャル・シークレット検出パターン
SECRET_PATTERNS = [
    (r'(?i)(api[_-]?key|apikey)\s*[:=]\s*\S+', "API Key"),
    (r'(?i)(secret|token|password|passwd|pwd)\s*[:=]\s*\S+', "Secret/Token/Password"),
    (r'(?i)(access[_-]?key|secret[_-]?key)\s*[:=]\s*\S+', "Access Key"),
    (r'(?i)(bearer\s+)[A-Za-z0-9\-._~+/]+=*', "Bearer Token"),
    (r'sk-[A-Za-z0-9]{20,}', "OpenAI API Key"),
    (r'sk-ant-[A-Za-z0-9\-]{20,}', "Anthropic API Key"),
    (r'ghp_[A-Za-z0-9]{36,}', "GitHub Personal Access Token"),
    (r'gho_[A-Za-z0-9]{36,}', "GitHub OAuth Token"),
    (r'AIza[A-Za-z0-9\-_]{35}', "Google API Key"),
    (r'(?i)aws[_-]?(access|secret)[_-]?key\S*\s*[:=]\s*\S+', "AWS Key"),
    (r'xox[bpras]-[A-Za-z0-9\-]{10,}', "Slack Token"),
    (r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----', "Private Key"),
    (r'(?i)(mongodb(\+srv)?://)\S+:\S+@', "MongoDB Connection String"),
    (r'(?i)(postgres(ql)?://)\S+:\S+@', "PostgreSQL Connection String"),
    (r'(?i)(mysql://)\S+:\S+@', "MySQL Connection String"),
]
_compiled_patterns = [(re.compile(p), label) for p, label in SECRET_PATTERNS]


def scan_secrets(text: str) -> list[dict]:
    """テキスト内のクレデンシャル・シークレットを検出する"""
    findings = []
    for pattern, label in _compiled_patterns:
        for match in pattern.finditer(text):
            matched = match.group()
            # マスク処理: 先頭8文字 + *** + 末尾4文字（短い場合は全体マスク）
            if len(matched) > 16:
                masked = matched[:8] + "***" + matched[-4:]
            else:
                masked = matched[:4] + "***"
            findings.append({
                "type": label,
                "masked_value": masked,
            })
    return findings


def get_appdata_path() -> Path:
    """OSに応じたAppDataパスを返す"""
    system = platform.system()
    if system == "Windows":
        return Path(os.environ.get("APPDATA", Path.home() / "AppData" […]

> TOOL

tool_result
id: toolu_01MSyRsAyaHW5iwCvwgsPQiK
```
# データソース詳細リファレンス

各AIツールのログ保存場所・フォーマット・抽出方法の詳細。

---

## 1. Claude Code（主要ソース）

### 保存場所
| OS | パス |
|----|------|
| Windows | `C:\Users\<user>\.claude\` |
| macOS | `~/.claude/` |
| Linux | `~/.claude/` |

### ファイル構造
```
~/.claude/
├── history.jsonl                          # 全プロジェクトの軽量インデックス
└── projects/
    └── {encoded-path}/                    # パス区切り(\, /, :) → - に変換
        ├── {session-uuid}.jsonl           # セッション別の完全な会話ログ
        └── {session-uuid}/
            └── subagents/                 # サブエージェントのログ
```

### history.jsonl の形式
```json
{"display":"ユーザーの入力テキスト","pastedContents":{},"timestamp":1759115795246,"project":"D:\\path\\to\\project"}
```

### プロジェクト別JSONL の形式
各行がJSON。ユーザーメッセージは `"type":"user"` を含む。
```json
{"type":"user","message":{"role":"user","content":[{"type":"text","text":"..."}]},"timestamp":"..."}
```

### 抽出方法（2ソース方式）

**ソース1: history.jsonl（CLI使用時）**
1. `history.jsonl` を読み込み、`display` フィールドからプロンプトを取得
2. `/clear` やファイルパスのみの行を除外
3. 収集済みの `sessionId` を記録（ソース2との重複排除用）

**ソース2: プロジェクト別セッションJSONL（VS Code拡張機能使用時）**
1. `projects/` 配下の各プロジェクトディレクトリを走査
2. 各ディレクトリの `*.jsonl` ファイルから `"type":"user"` のメッセージを抽出
3. `isMeta: true` のシステムメッセージはスキップ
4. `<ide_opened_file>`, `<local-command-stdout>` 等のシステムタグを除外
5. history.jsonl で収集済みのセッションIDはスキップ（重複排除）
6. 各プロジェクト最新5ファイル、1ファイルあたりユーザーメッセージ100件上限

**重要**: VS Code拡張機能で使用した場合、`history.jsonl` にはエントリが記録されず、
プロジェクト別セッションJSONLにのみ会話ログが保存される。両方のソースを読む必要がある。

### パスエンコード規則
プロジェクトディレクトリ名は、元のパスの `\`, `/`, `:` を `-` に変換。
例: `C:\Users\shinta\Documents\GitHub\yonshogen` → `c--Users-shinta-Documents-GitHub-yonshogen`

---

## 2. GitHub Copilot Chat

### 保存場所
| OS | パス |
|----|------|
| Windows | `%APPDATA%\Code\User\workspaceStorage\*\state.vscdb` |
| macOS | `~/Library/Application Support/Code/User/workspaceStorage/*/state.vscdb` |
| Linux | `~/.config/Code/User/workspaceStorage/*/state.vscdb` |

### ファイル形式
SQLite データベース（`state.vscdb`）

### 抽出方法
```bash
# 利用可能なキーの一覧を取得
sqlite3 "<path>/state.vscdb" "SELECT key FROM ItemTable WHERE key LIKE '%chat%';"

# チャットセッションインデックスを取得
sqlite3 "<path>/state.vscdb" "SELECT value FROM ItemTable WHERE key = 'interactive.sessions';" 2>/dev/null […]

> TOOL

tool_result
id: toolu_01Q7SQXr3xCGE6QN9Et3yVyo
```
# プロンプト分析レポート

- **生成日**: YYYY-MM-DD
- **分析対象**: 全プロジェクト / [プロジェクト名]
- **分析期間**: [最古のタイムスタンプ] 〜 [最新のタイムスタンプ]
- **分析メッセージ数**: N件（短文の肯定応答M件を除外、元データX件）

<!-- ヘッダの記述ルール:
  - 分析メッセージ数は「除外後の件数（除外件数、元データ件数）」の3つを明記する
  - 分析対象は引数で --project が指定された場合はプロジェクト名、なければ「全プロジェクト」
-->

---

## 1. データソースサマリー

| ツール | ステータス | メッセージ数 | 期間 |
|--------|-----------|-------------|------|
| Claude Code | 検出 / 未検出 | N件 | YYYY-MM-DD HH:MM 〜 YYYY-MM-DD HH:MM |
| GitHub Copilot Chat | 検出 / 未検出 | N件 | YYYY-MM-DD HH:MM 〜 YYYY-MM-DD HH:MM |
| Cline | 検出 / 未検出 | N件 | - |
| Roo Code | 検出 / 未検出 | N件 | - |
| Windsurf | 検出 / 未検出 | N件 | - |
| Antigravity | 検出 / 未検出 | N件 | - |

<!-- データソースサマリーの記述ルール:
  - 未検出のツールは期間を「-」とする
  - テーブルの後に補足注記を追加する:
    - データ量が少ない（20件未満）場合: より長期間での再分析を推奨する旨
    - Copilot Chat: タイムスタンプがファイル更新日時に基づく旨
    - 複数ツール検出時: ツール間でメッセージ数に偏りがある場合はその旨
-->

> **注**: [補足注記をここに記述]

---

## 2. プロジェクト別サマリー

<!-- collect.py の project_stats と各 source の messages から生成する。
     プロジェクトごとにメッセージ数が多い順に並べる。 -->

| プロジェクト | メッセージ数 | 使用ツール | 主な作業内容 |
|-------------|-------------|-----------|-------------|
| [プロジェクト名] | N件 | Claude Code, Copilot Chat | [プロンプト内容から推測される作業概要] |
| [プロジェクト名] | N件 | Claude Code | [作業概要] |

<!-- プロジェクト別サマリーの記述ルール:
  - project_stats のメッセージ数降順で並べる
  - 「主な作業内容」はそのプロジェクトのプロンプトを読み、1行で要約する
    - 例: 「書籍原稿の編集・章構成の見直し」「Webアプリのフロントエンド開発」「データ分析スクリプトの作成」 […]

> TOOL

tool_result
id: toolu_01A4CfB6HpDeCVspzDWLakAp
```
     1→# Agent skills configuration for Claude Code
     2→# https://github.com/Kyure-A/agent-skills-nix
     3→#
     4→# All skills (local and external) are managed here via agent-skills-nix.
     5→# Skills are deployed to ~/.agents (standard location) and ~/.config/claude/skills
     6→{
     7→  pkgs,
     8→  inputs,
     9→  local-skills,
    10→  ...
    11→}:
    12→{
    13→  programs.agent-skills = {
    14→    enable = true;
    15→
    16→    # Skill sources
    17→    sources = {
    18→      # Local: skills from this dotfiles repo
    19→      local = {
    20→        path = local-skills;
    21→        subdir = "agents/skills";
    22→      };
    23→      # Anthropic: official skills from anthropics/skills
    24→      anthropic = {
    25→        path = inputs.anthropic-skills;
    26→        subdir = "skills";
    27→      };
    28→      # Vercel: skills from vercel-labs/skills
    29→      vercel = {
    30→        path = inputs.vercel-skills;
    31→        subdir = "skills";
    32→      };
    33→      # nextlevelbuilder: UI/UX Pro Max skill
    34→      nextlevelbuilder = {
    35→        path = inputs.ui-ux-pro-max-skill;
    36→        subdir = ".claude/skills";
    37→      };
    38→      # ast-grep: AST-based code search and transform skill
    39→      ast-grep = {
    40→        path = inputs.ast-grep-skill;
    41→        subdir = "ast-grep/skills";
    42→      };
    43→      # Cloudflare: skills from cloudflare/skills
    44→      cloudflare = {
    45→        path = inputs.cloudflare-skills;
    46→        subdir = "skills";
    47→      };
    48→      # HashiCorp: skills from hashicorp/agent-skills (terraform/, packer/ at root) […]

> AGENT

flake inputの構造を確認します。

> TOOL

tool_use Read
id: toolu_01BaDieSG2e2YFoMj8Cv7tG1
```json
{
  "file_path": "/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/flake.nix"
}
```

> TOOL

tool_result
id: toolu_01BaDieSG2e2YFoMj8Cv7tG1
```
     1→{
     2→  description = "yuta's NixOS & macOS configuration";
     3→
     4→  inputs = {
     5→    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
     6→    nixpkgs-stable.url = "github:NixOS/nixpkgs/nixos-25.11";
     7→    flake-parts = {
     8→      url = "github:hercules-ci/flake-parts";
     9→      inputs.nixpkgs-lib.follows = "nixpkgs";
    10→    };
    11→    treefmt-nix = {
    12→      url = "github:numtide/treefmt-nix";
    13→      inputs.nixpkgs.follows = "nixpkgs";
    14→    };
    15→    ghostty.url = "github:ghostty-org/ghostty";
    16→    home-manager = {
    17→      url = "github:nix-community/home-manager";
    18→      inputs.nixpkgs.follows = "nixpkgs";
    19→    };
    20→    niri = {
    21→      url = "github:sodiboo/niri-flake";
    22→      inputs.nixpkgs.follows = "nixpkgs";
    23→    };
    24→    llm-agents.url = "github:numtide/llm-agents.nix";
    25→    nix-steipete-tools.url = "github:openclaw/nix-steipete-tools";
    26→    gh-nippou = {
    27→      url = "github:ryoppippi/gh-nippou";
    28→      inputs.nixpkgs.follows = "nixpkgs";
    29→    };
    30→    gh-graph = {
    31→      url = "github:kawarimidoll/gh-graph";
    32→      inputs.nixpkgs.follows = "nixpkgs";
    33→    };
    34→    nix-hazkey = {
    35→      url = "github:aster-void/nix-hazkey";
    36→      inputs.nixpkgs.follows = "nixpkgs";
    37→    };
    38→    agent-skills = {
    39→      url = "github:Kyure-A/agent-skills-nix";
    40→      inputs.nixpkgs.follows = "nixpkgs";
    41→    };
    42→    anthropic-skills = {
    43→      url = "github:anthropics/skills";
    44→      flake = false;
    45→    };
    46→    vercel-skills = {
    47→      url = "github:vercel-labs/skills";
    48→      flake = false;
    49→    };
    50→    ui-ux-pro-max-skill = {
    51→      url = "github:nextlevelbuilder/ui-ux-pro-max-skill";
    52→      flake = false;
    53→    };
    54→    ast-grep-skill = {
    55→      url = "github:ast-grep/claude-skill"; […]

> AGENT

構造が把握できました。`flake.nix` に input を追加し、`agent-skills.nix` に source と skill を追加します。

> TOOL

tool_use Edit
id: toolu_017vUh7MPxmhXysg7Js1W4vv
```json
{
  "replace_all": false,
  "file_path": "/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/flake.nix",
  "old_string": "    obsidian-skills = {\n      url = \"github:kepano/obsidian-skills\";\n      flake = false;\n    };",
  "new_string": "    obsidian-skills = {\n      url = \"github:kepano/obsidian-skills\";\n      flake = false;\n    };\n    prompt-review-skill = {\n      url = \"github:tokoroten/prompt-review\";\n      flake = false;\n    };"
}
```

> TOOL

tool_result
id: toolu_017vUh7MPxmhXysg7Js1W4vv
```
The file /Users/yuta/ghq/github.com/yutakobayashidev/dotnix/flake.nix has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01FppBijVGb26z7P43dAfhho
```json
{
  "replace_all": false,
  "file_path": "/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/nix/modules/home/agent-skills.nix",
  "old_string": "      # repiq: OSS metrics CLI skill\n      repiq = {\n        path = inputs.repiq;\n        subdir = \"skills\";\n      };",
  "new_string": "      # repiq: OSS metrics CLI skill\n      repiq = {\n        path = inputs.repiq;\n        subdir = \"skills\";\n      };\n      # prompt-review: AI対話履歴分析スキル\n      prompt-review = {\n        path = inputs.prompt-review-skill;\n        subdir = \".claude/skills\";\n      };"
}
```

> TOOL

tool_result
id: toolu_01FppBijVGb26z7P43dAfhho
```
The file /Users/yuta/ghq/github.com/yutakobayashidev/dotnix/nix/modules/home/agent-skills.nix has been updated successfully.
```

> AGENT

次に、`skills.explicit` にスキルを追加します。

> TOOL

tool_use Edit
id: toolu_01UQd2gXqpdf9CGewwhLNpX2
```json
{
  "replace_all": false,
  "file_path": "/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/nix/modules/home/agent-skills.nix",
  "old_string": "      # ast-grep skills\n      ast-grep = {\n        from = \"ast-grep\";\n        path = \"ast-grep\";\n      };",
  "new_string": "      # ast-grep skills\n      ast-grep = {\n        from = \"ast-grep\";\n        path = \"ast-grep\";\n      };\n      # prompt-review skills\n      prompt-review = {\n        from = \"prompt-review\";\n        path = \"prompt-review\";\n      };"
}
```

> TOOL

tool_result
id: toolu_01UQd2gXqpdf9CGewwhLNpX2
```
The file /Users/yuta/ghq/github.com/yutakobayashidev/dotnix/nix/modules/home/agent-skills.nix has been updated successfully.
```

> AGENT

変更内容を確認します。

> TOOL

tool_use Bash
id: toolu_01HcDf3QcSwF9AVdK5Kjhx4y
```json
{
  "command": "git diff",
  "description": "Show git diff"
}
```

> TOOL

tool_result
id: toolu_01HcDf3QcSwF9AVdK5Kjhx4y
```
flake.lock                        | 17 +++++++++++++++++
 flake.nix                         |  4 ++++
 nix/modules/home/agent-skills.nix | 10 ++++++++++
 3 files changed, 31 insertions(+)

--- Changes ---

📄 flake.lock
  @@ -1396,6 +1396,22 @@
  +    "prompt-review-skill": {
  +      "flake": false,
  +      "locked": {
  +        "lastModified": 1773299474,
  +        "narHash": "REDACTED",
  +        "owner": "tokoroten",
  +        "repo": "prompt-review",
  +        "rev": "e3a194d418cca469a13441a04eb93cb1d6484670",
  +        "type": "github"
  +      },
  +      "original": {
  +        "owner": "tokoroten",
  +        "repo": "prompt-review",
  +        "type": "github"
  +      }
  +    },
       "repiq": {
         "inputs": {
           "flake-parts": "flake-parts_5",
  @@ -1450,6 +1466,7 @@
  +        "prompt-review-skill": "prompt-review-skill",
           "repiq": "repiq",
           "rustowl-flake": "rustowl-flake",
           "tree-sitter-moonbit": "tree-sitter-moonbit",
  +17 -0

📄 flake.nix
  @@ -75,6 +75,10 @@
  +    prompt-review-skill = {
  +      url = "github:tokoroten/prompt-review";
  +      flake = false;
  +    };
       repiq = {
         url = "github:yutakobayashidev/repiq";
         inputs.nixpkgs.follows = "nixpkgs";
  +4 -0

📄 nix/modules/home/agent-skills.nix
  @@ -70,6 +70,11 @@
  +      # prompt-review: AI対話履歴分析スキル
  +      prompt-review = {
  +        path = inputs.prompt-review-skill;
  +        subdir = ".claude/skills";
  +      };
       };
   
       # Enable all local skills
  @@ -130,6 +135,11 @@
  +      # prompt-review skills
  +      prompt-review = {
  +        from = "prompt-review";
  +        path = "prompt-review";
  +      };
       };
   
       # Deploy to standard skills directories
  +10 -0
```

> AGENT

CLAUDE.mdのAgent Skillsセクションも更新します。

> TOOL

tool_use Read
id: toolu_01KrkApHiR7RxdT4wvmFaaoR
```json
{
  "file_path": "/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/CLAUDE.md",
  "offset": 29,
  "limit": 30
}
```

> TOOL

tool_result
id: toolu_01KrkApHiR7RxdT4wvmFaaoR
```
    29→
    30→主なスキル：
    31→
    32→- `social-digest` - Discord + Mastodon投稿をObsidianに保存（ローカル）
    33→- `oura-daily-watch` - Oura Ring データ + Discord行動分析（ローカル）
    34→- `check-similarity` - TypeScript/JavaScript重複コード検知（ローカル）
    35→- `dce` - Dead Code Elimination（ローカル）
    36→- `markitdown` - 各種ファイル（PDF, DOCX, PPTX等）をMarkdownに変換（ローカル）
    37→- `speakerdeck` - SpeakerDeckスライド画像のダウンロード（ローカル）
    38→- `docx`, `pdf`, `pptx`, `xlsx` - ドキュメント処理（Anthropic）
    39→- `frontend-design`, `skill-creator`, `webapp-testing` - 開発支援（Anthropic）
    40→- `find-skills` - スキル検索・発見支援（Vercel）
    41→- `ui-ux-pro-max` - UI/UXデザインシステム生成（コミュニティ）
    42→- `obsidian-markdown`, `obsidian-bases`, `json-canvas`, `obsidian-cli`, `defuddle` - Obsidian連携（kepano）
    43→
    44→詳細: `agents/README.md`
    45→
    46→## Architecture
    47→
    48→NixOS & macOS flake構成 with home-manager（nixos-unstable + nixpkgs-stable fallback）
    49→
    50→```
    51→flake.nix                          # エントリポイント
    52→├── agents/
    53→│   └── skills/                    # Claude Codeスキル
    54→├── raycast/                       # macOS Raycastスクリプト
    55→├── nix/
    56→│   ├── hosts/                     # ホスト固有の設定
    57→│   │   ├── UM790-Pro/             # NixOS (x86_64-linux)
    58→│   │   │   ├── default.nix        # モジュール構成
```

> TOOL

tool_use Edit
id: toolu_012pE2B9vY1HTSXq669SPVip
```json
{
  "replace_all": false,
  "file_path": "/Users/yuta/ghq/github.com/yutakobayashidev/dotnix/CLAUDE.md",
  "old_string": "- `obsidian-markdown`, `obsidian-bases`, `json-canvas`, `obsidian-cli`, `defuddle` - Obsidian連携（kepano）",
  "new_string": "- `obsidian-markdown`, `obsidian-bases`, `json-canvas`, `obsidian-cli`, `defuddle` - Obsidian連携（kepano）\n- `prompt-review` - AIエージェント対話履歴の分析・プロンプティング力診断（tokoroten）"
}
```

> TOOL

tool_result
id: toolu_012pE2B9vY1HTSXq669SPVip
```
The file /Users/yuta/ghq/github.com/yutakobayashidev/dotnix/CLAUDE.md has been updated successfully.
```

> AGENT

完了しました。以下の変更を行いました：

1. **`flake.nix`** — `prompt-review-skill` を flake input に追加（`github:tokoroten/prompt-review`, `flake = false`）
2. **`nix/modules/home/agent-skills.nix`** — source に `prompt-review` を追加（subdir: `.claude/skills`）、`skills.explicit` にスキルエントリを追加
3. **`CLAUDE.md`** — Agent Skillsセクションに `prompt-review` の説明を追加

`nix run .#switch` で適用すると、`~/.config/claude/skills/` と `~/.agents/skills/` に `prompt-review` スキルがデプロイされます。