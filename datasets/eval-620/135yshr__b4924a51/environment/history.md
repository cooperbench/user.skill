> DEVELOPER

md2pdf リポジトリに対して、以下の2件の GitHub issue を `gh` CLI で作成してください。

## 前提

- カレントディレクトリは `135yshr/md2pdf` のローカルクローン、もしくは `--repo 135yshr/md2pdf` を明示してください
- `gh auth status` で認証済みであることを先に確認してください
- 既存の同名 issue がないか `gh issue list --search "<title>"` で念のためチェックしてください
- 各 issue 本文は heredoc またはファイル経由で渡し、改行・コードブロック・日本語が壊れないようにしてください

## 背景（参考リンク、本文に含める）

- ユーザーフィードバック元: https://zenn.dev/link/comments/18e8c67d0561bd
- 報告者: ppbb さん
- OS: macOS（エラーパスの `/var/folders/...` から確定）

---

## Issue 1（バグ）

**Title:**
playwright module not found when invoked from md2pdf, but works when print_pdf.py is run directly

**Labels:** `bug`

**Body:**

```markdown
## Description

A user reported that running `md2pdf` fails with `ModuleNotFoundError: No module named 'playwright'`, even though `playwright` is installed and `print_pdf.py` works correctly when copied out and executed directly with `python`.

Reported via Zenn comment: https://zenn.dev/link/comments/18e8c67d0561bd

## Reproduction

```
$ md2pdf <input>.md
md2pdf: conversion failed: print pdf: playwright script failed: exit status 1
output: Traceback (most recent call last):
  File "/var/folders/t5/qjlms9tx4mg9j_m5106w3g280000gn/T/md2pdf-2994288070/print_pdf.py", line 2, in <module>
    from playwright.sync_api import sync_playwright
ModuleNotFoundError: No module named 'playwright'
```

Workaround that works for the user:
- Copy the temp `print_pdf.py` elsewhere and run it directly with `python` → succeeds.

## Suspected Cause

The Python interpreter spawned by md2pdf is not the same one where `playwright` was installed via `pip install playwright`. Likely scenarios:

- pyenv shim / […]

> TOOL

tool_use Bash
id: toolu_01F3S29Ktp6RWYSodLGG4Duc
```json
{
  "command": "gh auth status",
  "description": "Check gh authentication status"
}
```

> TOOL

tool_use Bash
id: toolu_01NHWowPv8CHGSV3QNdVAgv7
```json
{
  "command": "gh label list --repo 135yshr/md2pdf",
  "description": "List labels in repository"
}
```

> TOOL

tool_use Bash
id: toolu_01PiMRvYTWZf3kJXm38LmRVS
```json
{
  "command": "gh issue list --repo 135yshr/md2pdf --search \"playwright module not found\" --state all",
  "description": "Search for existing similar issue 1"
}
```

> TOOL

tool_use Bash
id: toolu_0194nhYFCAtEuAJpnc1ELTDv
```json
{
  "command": "gh issue list --repo 135yshr/md2pdf --search \"Support custom CSS styling\" --state all",
  "description": "Search for existing similar issue 2"
}
```

> TOOL

tool_result
id: toolu_01F3S29Ktp6RWYSodLGG4Duc
```
github.com
  ✓ Logged in to github.com account 135yshr (keyring)
  - Active account: true
  - Git operations protocol: ssh
  - Token: gho_************************************
  - Token scopes: 'admin:public_key', 'gist', 'project', 'read:org', 'repo'
```

> TOOL

tool_result
id: toolu_01NHWowPv8CHGSV3QNdVAgv7
```
bug	Something isn't working	#d73a4a
documentation	Improvements or additions to documentation	#0075ca
duplicate	This issue or pull request already exists	#cfd3d7
enhancement	New feature or request	#a2eeef
good first issue	Good for newcomers	#7057ff
help wanted	Extra attention is needed	#008672
invalid	This doesn't seem right	#e4e669
question	Further information is requested	#d876e3
wontfix	This will not be worked on	#ffffff
```

> TOOL

tool_result
id: toolu_01PiMRvYTWZf3kJXm38LmRVS
```
(Bash completed with no output)
```

> TOOL

tool_result
id: toolu_0194nhYFCAtEuAJpnc1ELTDv
```
(Bash completed with no output)
```

> AGENT

認証済み、ラベルあり、重複なし。本文ファイルを作成して issue を作成します。

> TOOL

tool_use Write
id: toolu_01JVkYFh8ffbeFV36FKkbKZb
```json
{
  "file_path": "/tmp/md2pdf-issue-1-body.md",
  "content": "## Description\n\nA user reported that running `md2pdf` fails with `ModuleNotFoundError: No module named 'playwright'`, even though `playwright` is installed and `print_pdf.py` works correctly when copied out and executed directly with `python`.\n\nReported via Zenn comment: https://zenn.dev/link/comments/18e8c67d0561bd\n\n## Reproduction\n\n```\n$ md2pdf <input>.md\nmd2pdf: conversion failed: print pdf: playwright script failed: exit status 1\noutput: Traceback (most recent call last):\n  File \"/var/folders/t5/qjlms9tx4mg9j_m5106w3g280000gn/T/md2pdf-2994288070/print_pdf.py\", line 2, in <module>\n    from playwright.sync_api import sync_playwright\nModuleNotFoundError: No module named 'playwright'\n```\n\nWorkaround that works for the user:\n- Copy the temp `print_pdf.py` elsewhere and run it directly with `python` → succeeds.\n\n## Suspected Cause\n\nThe Python interpreter spawned by md2pdf is not the same one where `playwright` was installed via `pip install playwright`. Likely scenarios:\n\n- pyenv shim / Homebrew Python / system Python mismatch on macOS\n- `os/exec` not inheriting the user's interactive shell PATH\n- venv `VIRTUAL_ENV` not propagated to the subprocess\n\n## Proposed Fix\n\n1. Add a `-python <path>` flag (mirroring `-mmdc <path>`) so users can pin the interpreter explicitly.\n2. Add `PYTHON` / `MD2PDF_PYTHON` environment variable as a fallback.\n3. Improve auto-detection: try `python3`, `python`, verify `playwright` importability before invocation and emit a clear error pointing at the specific interpreter being used.\n4. In verbose mode (`-v`), log the actual Python executable path […]

> TOOL

tool_result
id: toolu_01JVkYFh8ffbeFV36FKkbKZb
```
File created successfully at: /tmp/md2pdf-issue-1-body.md
```

> TOOL

tool_use Write
id: toolu_01KJuV6pB7Vm54VbxTBJsaZi
```json
{
  "file_path": "/tmp/md2pdf-issue-2-body.md",
  "content": "## Background\n\nRequested via Zenn comment: https://zenn.dev/link/comments/18e8c67d0561bd\n\n> カスタムcssでの修飾機能があるといいなと思いました（そのためにはHTML出力もあると便利？）\n\n## Proposal\n\nTwo related capabilities:\n\n### 1. Custom CSS injection\n\nAdd a `-css <path>` flag (or `-css <path>...` to allow multiple) that injects user CSS after the built-in GitHub-flavored stylesheet so users can override or extend it.\n\n```\nmd2pdf -css custom.css document.md\n```\n\nUse cases: corporate branding (logo colors, fonts), client-specific deliverable formatting, presentation-mode tweaks.\n\n### 2. HTML output mode\n\nAdd a `-html` flag (or `-format html`) that stops the pipeline at step 3 (Build HTML) and emits the self-contained HTML instead of running Playwright.\n\n```\nmd2pdf -html document.md   # produces document.html\n```\n\nBenefits:\n- Lets users iterate on custom CSS quickly in a browser without spinning up Chromium each time.\n- Useful for users who only want HTML (e.g. publishing to a static site).\n- Removes the Playwright dependency for HTML-only workflows.\n\n## Design considerations\n\n- Both flags should be composable: `-html -css custom.css` should produce HTML with the custom CSS applied.\n- Custom CSS should be embedded inline in the `<style>` tag (not linked) to keep the HTML self-contained, matching md2pdf's current philosophy.\n- Document precedence clearly: built-in CSS → custom CSS (latter wins).\n"
}
```

> TOOL

tool_result
id: toolu_01KJuV6pB7Vm54VbxTBJsaZi
```
File created successfully at: /tmp/md2pdf-issue-2-body.md
```

> TOOL

tool_use Bash
id: toolu_01S2rX1Z7jFkZHfQprTQc4Q6
```json
{
  "command": "gh issue create --repo 135yshr/md2pdf --title \"playwright module not found when invoked from md2pdf, but works when print_pdf.py is run directly\" --label \"bug\" --body-file /tmp/md2pdf-issue-1-body.md",
  "description": "Create bug issue for playwright module not found"
}
```

> TOOL

tool_use Bash
id: toolu_016Bg5t6KftcqAtcmK5vS5fh
```json
{
  "command": "gh issue create --repo 135yshr/md2pdf --title \"Support custom CSS styling and HTML output\" --label \"enhancement\" --body-file /tmp/md2pdf-issue-2-body.md",
  "description": "Create enhancement issue for custom CSS and HTML output"
}
```

> TOOL

tool_result
id: toolu_01S2rX1Z7jFkZHfQprTQc4Q6
```
https://github.com/135yshr/md2pdf/issues/29
```

> TOOL

tool_result
id: toolu_016Bg5t6KftcqAtcmK5vS5fh
```
https://github.com/135yshr/md2pdf/issues/30
```

> AGENT

両 issue を作成しました。

- **Issue #29 (bug):** [playwright module not found when invoked from md2pdf, but works when print_pdf.py is run directly](https://github.com/135yshr/md2pdf/issues/29)
- **Issue #30 (enhancement):** [Support custom CSS styling and HTML output](https://github.com/135yshr/md2pdf/issues/30)

事前に `gh auth status` で認証確認、`bug` / `enhancement` ラベルの存在確認、同名 issue の重複が無いことも検索で確認済みです。