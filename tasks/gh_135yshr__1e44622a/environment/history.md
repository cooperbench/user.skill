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

> DEVELOPER

#29のissueに問題が発生する原因を教えてください。
調査が終わっていない場合は、先に調査をしてください

> TOOL

tool_use ToolSearch
id: toolu_01V4bcrYMazTZGttVaQ5NYjc
```json
{
  "query": "select:TaskCreate,TaskUpdate",
  "max_results": 2
}
```

> TOOL

tool_result
id: toolu_01V4bcrYMazTZGttVaQ5NYjc
```
{
  "type": "tool_reference",
  "tool_name": "TaskCreate"
}
{
  "type": "tool_reference",
  "tool_name": "TaskUpdate"
}
```

> TOOL

tool_use TaskCreate
id: toolu_01DepqHWWEy3whbHnwvmTrBC
```json
{
  "subject": "Investigate root cause of issue #29",
  "description": "Read pdf.go, flags.go, and converter to understand how md2pdf invokes Python and why playwright import fails when run via subprocess but succeeds when print_pdf.py is run directly.",
  "activeForm": "Investigating root cause of issue #29"
}
```

> TOOL

tool_result
id: toolu_01DepqHWWEy3whbHnwvmTrBC
```
Task #1 created successfully: Investigate root cause of issue #29
```

> TOOL

tool_use TaskUpdate
id: toolu_01CRCinbW3Ys8WMvPoDuDNdy
```json
{
  "taskId": "1",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_01CRCinbW3Ys8WMvPoDuDNdy
```
Updated task #1 status
```

> TOOL

tool_use Bash
id: toolu_01TKzRvL8arZ3CGmc6LvLM7m
```json
{
  "command": "ls /Users/135yshr/go/src/github.com/135yshr/md2pdf/internal/converter/ /Users/135yshr/go/src/github.com/135yshr/md2pdf/cmd/md2pdf/",
  "description": "List converter and cmd directories"
}
```

> TOOL

tool_result
id: toolu_01TKzRvL8arZ3CGmc6LvLM7m
```
/Users/135yshr/go/src/github.com/135yshr/md2pdf/cmd/md2pdf/:
flags.go
main.go

/Users/135yshr/go/src/github.com/135yshr/md2pdf/internal/converter/:
converter_integration_test.go
converter.go
html_test.go
html.go
mermaid.go
parser_test.go
parser.go
pdf.go
```

> TOOL

tool_use Read
id: toolu_011VWGhxwfRzrwLDo3X4oXrw
```json
{
  "file_path": "/Users/135yshr/go/src/github.com/135yshr/md2pdf/internal/converter/pdf.go"
}
```

> TOOL

tool_result
id: toolu_011VWGhxwfRzrwLDo3X4oXrw
```
1	package converter
2	
3	import (
4		"fmt"
5		"os"
6		"os/exec"
7		"path/filepath"
8		"text/template"
9		"strings"
10	)
11	
12	// playwrightScript is the Python script template executed to print a PDF.
13	// It uses the Playwright sync API with Chromium.
14	const playwrightScript = `
15	from playwright.sync_api import sync_playwright
16	import sys
17	
18	html_path = {{.HTMLPath | quote}}
19	pdf_path  = {{.PDFPath  | quote}}
20	page_size = {{.PageSize | quote}}
21	margin    = {
22	    "top":    {{.MarginTop    | quote}},
23	    "bottom": {{.MarginBottom | quote}},
24	    "left":   {{.MarginLeft   | quote}},
25	    "right":  {{.MarginRight  | quote}},
26	}
27	
28	with sync_playwright() as p:
29	    browser = p.chromium.launch(args=["--no-sandbox", "--disable-setuid-sandbox"])
30	    page = browser.new_page()
31	    page.goto("file://" + html_path)
32	    page.wait_for_load_state("networkidle")
33	    page.evaluate("document.fonts.ready")
34	    page.pdf(
35	        path=pdf_path,
36	        format=page_size,
37	        margin=margin,
38	        print_background=True,
39	    )
40	    browser.close()
41	
42	print("ok")
43	`
44	
45	// scriptData holds the values interpolated into playwrightScript.
46	type scriptData struct {
47		HTMLPath     string
48		PDFPath      string
49		PageSize     string
50		MarginTop    string
51		MarginBottom string
52		MarginLeft   string
53		MarginRight  string
54	}
55	
56	// printPDF renders htmlPath to a PDF at pdfPath using a […]

> TOOL

tool_use Read
id: toolu_016NGZwKdCUf8KE9Znm2ZdMR
```json
{
  "file_path": "/Users/135yshr/go/src/github.com/135yshr/md2pdf/cmd/md2pdf/flags.go"
}
```

> TOOL

tool_result
id: toolu_016NGZwKdCUf8KE9Znm2ZdMR
```
1	package main
2	
3	import (
4		"errors"
5		"flag"
6		"fmt"
7		"os"
8		"path/filepath"
9		"strings"
10	
11		"github.com/135yshr/md2pdf/internal/converter"
12	)
13	
14	// defaultFontPaths lists common locations for Noto Sans CJK JP fonts,
15	// searched in order when no explicit -font flag is provided.
16	var defaultFontPaths = []string{
17		// Linux (Debian/Ubuntu)
18		"/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
19		"/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
20		// macOS (Homebrew)
21		"/opt/homebrew/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
22		"/usr/local/share/fonts/noto/NotoSansCJK-Regular.ttc",
23		// Fallback: no custom font (system default)
24		"",
25	}
26	
27	// mmdcDefaultPaths lists common install locations for the Mermaid CLI (mmdc).
28	var mmdcDefaultPaths = []string{
29		"mmdc", // found in $PATH
30		"/usr/local/bin/mmdc",
31		"/usr/bin/mmdc",
32		// npm global installs (Linux/macOS)
33		"/home/claude/.npm-global/bin/mmdc",
34		"/usr/local/lib/node_modules/.bin/mmdc",
35		"/opt/homebrew/bin/mmdc",
36	}
37	
38	// parseFlags parses command-line arguments and returns a Config.
39	func parseFlags(args []string) (*converter.Config, error) {
40		fs := flag.NewFlagSet("md2pdf", flag.ContinueOnError)
41		fs.SetOutput(os.Stderr)
42	
43		output := fs.String("o", "", "Output PDF file path (default: <input>.pdf)")
44		fontRegular := fs.String("font", "", "Path to Noto Sans CJK JP Regular .ttc/.ttf font file")
45		fontBold := fs.String("font-bold", "", "Path to Noto Sans CJK JP Bold .ttc/.ttf font file")
46		fontMedium := fs.String("font-medium", "", […]

> TOOL

tool_use Read
id: toolu_01CqDa9FpqWoR3e21sn3bRiR
```json
{
  "file_path": "/Users/135yshr/go/src/github.com/135yshr/md2pdf/internal/converter/converter.go"
}
```

> TOOL

tool_result
id: toolu_01CqDa9FpqWoR3e21sn3bRiR
```
1	// Package converter orchestrates the Markdown → HTML → PDF pipeline.
2	//
3	// The pipeline consists of three stages:
4	//  1. Parse Markdown and extract fenced Mermaid code blocks.
5	//  2. Render each Mermaid block to an SVG file using the mmdc CLI.
6	//  3. Build a self-contained GitHub-styled HTML file and print it to PDF
7	//     using a headless Chromium browser (via the Playwright Python driver).
8	package converter
9	
10	import (
11		"fmt"
12		"io"
13		"net/url"
14		"os"
15		"os/exec"
16		"path/filepath"
17		"regexp"
18		"strings"
19	)
20	
21	// Config holds all runtime options for the converter.
22	type Config struct {
23		// InputFile is the path to the source Markdown file.
24		InputFile string
25		// OutputFile is the destination PDF path.
26		OutputFile string
27		// FontRegular is the file path to the Noto Sans CJK JP Regular font.
28		FontRegular string
29		// FontBold is the file path to the Noto Sans CJK JP Bold font.
30		FontBold string
31		// FontMedium is the file path to the Noto Sans CJK JP Medium font.
32		FontMedium string
33		// […]

> AGENT

調査が終わりました。原因はコード上で明確に特定できます。

## 根本原因

**該当箇所:** `internal/converter/pdf.go:126-133`

```go
func findPython() (string, error) {
    for _, name := range []string{"python3", "python"} {
        if p, err := exec.LookPath(name); err == nil {
            return p, nil
        }
    }
    return "", fmt.Errorf("python3 not found in PATH; ...")
}
```

`pdf.go:75-81` でこの結果をそのまま `exec.Command(python, scriptPath)` に渡しているだけで、**「playwright を `import` できる Python」かどうかは一切検証していません**。

## なぜ「直接 `python` で実行すると成功する」のか

ユーザーが `pip install playwright` を打った時の `python3` と、md2pdf が `exec.LookPath("python3")` で解決する `python3` が**別バイナリ**になっているのが原因です。macOS 環境で典型的に起きる組み合わせ:

| 状況 | `pip install` した先 | md2pdf が拾う先 |
|---|---|---|
| pyenv 利用中 | `~/.pyenv/shims/python3` (= 例えば 3.12.x) | shim パスが `PATH` に入っていなければ `/usr/bin/python3` (CLT) |
| Homebrew Python 利用中 | `/opt/homebrew/bin/python3` | `PATH` 順次第で `/usr/bin/python3` を先に拾う |
| venv アクティブ中 | `$VIRTUAL_ENV/bin/python` | 親プロセスの `PATH` 次第で venv 外の python |

ユーザーが `print_pdf.py` を**直接** `python` で叩いた場合は、対話シェル（zsh）の rc が pyenv/Homebrew 用の `PATH` を整えた状態で起動するので、`pip` と同じ Python に解決されて成功します。

## md2pdf 側でこうなる理由

1. `os/exec` で起動した子プロセスは**親の `PATH` をそのまま継承する**だけで、対話シェルの rc を読み直さない。
2. md2pdf のコードには `PATH` を補強する処理も、`VIRTUAL_ENV` を尊重する処理も、Python 候補を「playwright が import できるか」で篩いにかける処理も無い。
3. `findPython()` は `python3` を最優先で返すので、macOS Command Line Tools の `/usr/bin/python3`（playwright が入っていない素の Apple Python）を引き当てがち。

エラーの `print_pdf.py` 1 行目の `from playwright.sync_api import sync_playwright` で `ModuleNotFoundError` が出ているのは、まさにこの「Python は起動できているが、`site-packages` に playwright が無い」状態の典型的シグネチャです。

## 補強される根拠（コード上の傍証）

- `chromiumPath()` (`converter.go:201-261`) は `CHROME_PATH` という env var フックを持っているのに、Python interpreter にはそれに相当するフックが**存在しない**。
- `flags.go` にも `-mmdc` […]

> TOOL

tool_use TaskUpdate
id: toolu_015n18brGmyRdHJpwA2D9ukc
```json
{
  "taskId": "1",
  "status": "completed"
}
```

> TOOL

tool_result
id: toolu_015n18brGmyRdHJpwA2D9ukc
```
Updated task #1 status
```

> AGENT

調査完了。原因は `internal/converter/pdf.go:126` の `findPython()` が「playwright が import できる Python かどうか」を検証せず、`exec.LookPath("python3")` で見つかった最初のバイナリ（macOS だと `/usr/bin/python3` などの CLT Python になりがち）をそのまま使う点にあります。

> DEVELOPER

報告があった問題を再現することは可能ですか？

> AGENT

再現可否を確認するため、まず現在の環境を調べます。

> TOOL

tool_use Bash
id: toolu_01BmJn6qTXotRFRXJg3QbDmG
```json
{
  "command": "echo \"=== which python3/python ===\" && which -a python3 && echo \"---\" && which -a python; echo \"=== /usr/bin/python3 ===\"; /usr/bin/python3 --version 2>&1; echo \"---\"; /usr/bin/python3 -c \"import playwright; print(playwright.__file__)\" 2>&1",
  "description": "Check which python3 resolves to and whether playwright is importable"
}
```

> TOOL

tool_use Bash
id: toolu_014fN8MJFAzNcjE1GsvhxEza
```json
{
  "command": "echo \"PATH=$PATH\"; echo \"---\"; echo \"VIRTUAL_ENV=$VIRTUAL_ENV\"; echo \"PYENV_VERSION=$PYENV_VERSION\"; ls -la /opt/homebrew/bin/python* 2>/dev/null; ls -la ~/.pyenv/shims/python* 2>/dev/null",
  "description": "Check PATH, venv, pyenv state"
}
```

> TOOL

tool_result ERROR
id: toolu_01BmJn6qTXotRFRXJg3QbDmG
```
Exit code 1
=== which python3/python ===
/opt/homebrew/bin/python3
/Users/135yshr/.anyenv/envs/pyenv/shims/python3
/usr/bin/python3
---
/Users/135yshr/.anyenv/envs/pyenv/shims/python
=== /usr/bin/python3 ===
Python 3.9.6
---
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'playwright'
```

> TOOL

tool_result ERROR
id: toolu_014fN8MJFAzNcjE1GsvhxEza
```
<tool_use_error>Cancelled: parallel tool call Bash(echo "=== which python3/python ===" && w…) errored</tool_use_error>
```

> TOOL

tool_use Bash
id: toolu_01GE54vE4sh1UGTdqkfojHGx
```json
{
  "command": "command -v mmdc; ls /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome 2>/dev/null && echo \"Chrome OK\"; ls ~/Library/Caches/ms-playwright 2>/dev/null",
  "description": "Check mmdc and Chromium availability"
}
```

> TOOL

tool_result ERROR
id: toolu_01GE54vE4sh1UGTdqkfojHGx
```
<tool_use_error>Cancelled: parallel tool call Bash(echo "=== which python3/python ===" && w…) errored</tool_use_error>
```

> AGENT

すでに重要な手掛かりが見えました。`/usr/bin/python3` で `ModuleNotFoundError` が再現しています。続きを確認します。

> TOOL

tool_use Bash
id: toolu_01XgCpGAEomSg2ECpMcJWRxS
```json
{
  "command": "echo \"=== PATH ===\"; echo \"$PATH\"; echo \"=== /opt/homebrew/bin/python3 ===\"; /opt/homebrew/bin/python3 --version 2>&1; /opt/homebrew/bin/python3 -c \"import playwright; print(playwright.__file__)\" 2>&1; echo \"=== pyenv shim ===\"; /Users/135yshr/.anyenv/envs/pyenv/shims/python3 --version 2>&1; /Users/135yshr/.anyenv/envs/pyenv/shims/python3 -c \"import playwright; print(playwright.__file__)\" 2>&1",
  "description": "Check whether playwright is installed in the other python interpreters"
}
```

> TOOL

tool_use Bash
id: toolu_01RBmDtmpch6zs7t6fGTaLe4
```json
{
  "command": "command -v mmdc 2>&1; ls ~/Library/Caches/ms-playwright 2>&1 | head",
  "description": "Check mmdc and playwright browsers cache"
}
```

> TOOL

tool_result
id: toolu_01XgCpGAEomSg2ECpMcJWRxS
```
=== PATH ===
/Users/135yshr/.bun/bin:/Users/135yshr/.proto/shims:/Users/135yshr/.proto/bin:/Users/135yshr/.amplify/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/Users/135yshr/.local/bin:/opt/homebrew/opt/libpq/bin:/usr/local/opt/mysql-client/bin:/Users/135yshr/.anyenv/envs/pyenv/shims:/Users/135yshr/.anyenv/envs/pyenv/bin:/Users/135yshr/.anyenv/envs/nodenv/shims:/Users/135yshr/.anyenv/envs/nodenv/bin:/Users/135yshr/.anyenv/bin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin:/opt/pmk/env/global/bin:/Library/TeX/texbin:/Users/135yshr/.bun/bin:/Users/135yshr/.proto/shims:/Users/135yshr/.proto/bin:/Users/135yshr/.amplify/bin:/Users/135yshr/.cargo/bin:/Applications/iTerm.app/Contents/Resources/utilities:/Users/135yshr/Library/Android/sdk/platform-tools:/Users/135yshr/Library/Android/sdk/emulator:/Users/135yshr/development/flutter/bin:/Users/135yshr/development/flutter/.pub-cache/bin:/Users/135yshr/.pub-cache/bin:/Users/135yshr/fvm/default/bin:/Users/135yshr/bin:/Users/135yshr/go/bin:/Users/135yshr/sdk/go1.24.11/bin:/usr/local/opt/coreutils/libexec/gnubin:/Users/135yshr/go/bin:/Users/135yshr/go/pkg/mod/golang.org/toolchain@v0.0.1-go1.26.2.darwin-arm64/bin:/usr/local/opt/coreutils/libexec/gnubin:/Users/135yshr/.claude/plugins/cache/claude-plugins-official/code-review/unknown/bin:/Users/135yshr/.claude/plugins/cache/claude-plugins-official/context7/unknown/bin:/Users/135yshr/.claude/plugins/cache/claude-plugins-official/serena/unknown/bin:/Users/135yshr/.claude/plugins/cache/claude-plugins-official/frontend-design/unknown/bin:/Users/135yshr/.claude/plugins/cache/claude-plugins-official/pr-review-toolkit/unknown/bin:/Users/135yshr/.claude/plugins/cache/claude-plugins-official/gopls-lsp/1.0.0/bin:/Users/135yshr/.claude/plugins/cache/claude-plugins-official/typescript-lsp/1.0.0/bin:/Users/135yshr/.claude/plugins/cache/claude-plugins-official/coderabbit/1.1.1/bin:/Users/135yshr/.claude/plugins/cache/claude-plugins-official/chrome-devtools-mcp/0.22.0/bin:/Users/135yshr/.claude/plugins/cache/claude-plugins-official/claude-code-setup/1.0.0/bin:/Users/135yshr/.claude/plugins/cache/claude-plugins-official/github/unknown/bin:/Users/135yshr/.claude/plugins/cache/claude-plugins-official/deploy-on-aws/1.2.0/bin:/Users/135yshr/.claude/plugins/cache/claude-plugins-official/terraform/unknown/bin:/Users/135yshr/.claude/plugins/cache/claude-plugins-official/slack/1.0.0/bin:/Users/135yshr/.claude/plugins/cache/claude-plugins-official/vercel/0.42.1/bin:/Users/135yshr/.claude/plugins/cache/claude-plugins-official/commit-commands/unknown/bin:/Users/135yshr/.claude/plugins/cache/openai-codex/codex/1.0.2/bin
=== /opt/homebrew/bin/python3 ===
Python 3.14.3
/opt/homebrew/lib/python3.14/site-packages/playwright/__init__.py
=== pyenv shim ===
Python 3.14.3
/opt/homebrew/lib/python3.14/site-packages/playwright/__init__.py
```

> TOOL

tool_result
id: toolu_01RBmDtmpch6zs7t6fGTaLe4
```
/opt/homebrew/bin/mmdc
chromium_headless_shell-1194
chromium_headless_shell-1208
chromium-1194
chromium-1208
ffmpeg-1011
```

> AGENT

完璧な再現環境です:
- `/opt/homebrew/bin/python3` (Python 3.14): playwright **あり**
- `/usr/bin/python3` (Apple CLT 3.9.6): playwright **なし**

PATH を `/usr/bin:/bin` に絞れば `findPython()` が `/usr/bin/python3` を引き、issue #29 と同一エラーが出るはずです。実際にビルドして再現を試みます。

> TOOL

tool_use Bash
id: toolu_01ReahDNUaF4WGLZgXEQo7XB
```json
{
  "command": "go build -o /tmp/md2pdf-repro ./cmd/md2pdf && ls -la /tmp/md2pdf-repro",
  "description": "Build md2pdf binary for reproduction"
}
```

> TOOL

tool_use Write
id: toolu_01WLyymnqMHEXcNgG4rSLDTS
```json
{
  "file_path": "/tmp/md2pdf-repro-input.md",
  "content": "# Repro\n\nHello, world. Issue #29 reproduction.\n"
}
```

> TOOL

tool_result
id: toolu_01ReahDNUaF4WGLZgXEQo7XB
```
-rwxr-xr-x@ 1 135yshr  staff  6440274  5月  9 17:58 /tmp/md2pdf-repro
```

> TOOL

tool_result
id: toolu_01WLyymnqMHEXcNgG4rSLDTS
```
File created successfully at: /tmp/md2pdf-repro-input.md
```

> TOOL

tool_use Bash
id: toolu_01Jdj8ShVVfsjsvFtA65qVVZ
```json
{
  "command": "env -i HOME=\"$HOME\" PATH=\"/usr/bin:/bin\" /tmp/md2pdf-repro -mmdc /opt/homebrew/bin/mmdc -o /tmp/md2pdf-repro.pdf /tmp/md2pdf-repro-input.md 2>&1; echo \"---exit=$?---\"",
  "description": "Reproduce issue #29 with restricted PATH that resolves python3 to /usr/bin/python3"
}
```

> TOOL

tool_result
id: toolu_01Jdj8ShVVfsjsvFtA65qVVZ
```
Converting /tmp/md2pdf-repro-input.md ...
md2pdf: conversion failed: print pdf: playwright script failed: exit status 1
output: Traceback (most recent call last):
  File "/tmp/md2pdf-4023649013/print_pdf.py", line 2, in <module>
    from playwright.sync_api import sync_playwright
ModuleNotFoundError: No module named 'playwright'

---exit=1---
```

> AGENT

**再現成功**。ユーザー報告とビット単位で一致するエラーが出ました（temp パスだけが違うのは想定どおり）。

念のため inverse condition（PATH に Homebrew を含めれば成功すること）も確認します。

> TOOL

tool_use Bash
id: toolu_01A6qSGhRRQ5BHzDaeR7MQtH
```json
{
  "command": "PATH=\"/opt/homebrew/bin:/usr/bin:/bin\" /tmp/md2pdf-repro -mmdc /opt/homebrew/bin/mmdc -o /tmp/md2pdf-repro.pdf /tmp/md2pdf-repro-input.md 2>&1; echo \"---exit=$?---\"; ls -la /tmp/md2pdf-repro.pdf 2>&1",
  "description": "Verify md2pdf succeeds when PATH has homebrew python first"
}
```

> TOOL

tool_result
id: toolu_01A6qSGhRRQ5BHzDaeR7MQtH
```
Converting /tmp/md2pdf-repro-input.md ...
PDF saved to /tmp/md2pdf-repro.pdf
---exit=0---
-rw-r--r--@ 1 135yshr  wheel  12351  5月  9 17:59 /tmp/md2pdf-repro.pdf
```

> AGENT

両条件で挙動が分かれることが確認できました。

## 再現結果まとめ

| PATH | `findPython()` が拾う interpreter | 結果 |
|---|---|---|
| `/usr/bin:/bin` | `/usr/bin/python3` (Apple CLT 3.9.6, playwright なし) | ❌ `ModuleNotFoundError: No module named 'playwright'` (報告と完全一致) |
| `/opt/homebrew/bin:/usr/bin:/bin` | `/opt/homebrew/bin/python3` (3.14, playwright あり) | ✅ PDF 生成成功 |

これにより、issue #29 の原因が `internal/converter/pdf.go:126` の `findPython()` に集約されることが**実機で実証**できました。同一マシン上で `PATH` の差だけで成功/失敗が分岐するため、コード以外の要因（OS、依存ライブラリのバージョン、入力ファイル等）は一切関与していません。

ユーザー側で起きている可能性が最も高いシナリオ:
- macOS GUI から `md2pdf` を起動した、または対話シェル rc を読まないコンテキストで起動した
- 結果として `PATH` に Homebrew/pyenv のパスが入っておらず、`/usr/bin/python3`（Apple CLT）が選ばれた
- そこには `pip install playwright` が効いていないため import 失敗

> TOOL

tool_use Bash
id: toolu_01XCuYWTiW2HjAyAXXHnxaV8
```json
{
  "command": "rm -f /tmp/md2pdf-repro /tmp/md2pdf-repro.pdf /tmp/md2pdf-repro-input.md /tmp/md2pdf-issue-1-body.md /tmp/md2pdf-issue-2-body.md",
  "description": "Clean up reproduction artifacts"
}
```

> TOOL

tool_result
id: toolu_01XCuYWTiW2HjAyAXXHnxaV8
```
(Bash completed with no output)
```

> AGENT

再現が確実に取れたので、issue #29 の修正方針（`-python` フラグ追加・`MD2PDF_PYTHON` env var・`import playwright` precheck）はそのまま着手して問題ありません。一時ファイルは片付けました。