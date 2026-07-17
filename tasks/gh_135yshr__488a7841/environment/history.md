> TOOL

tool_use Bash
id: toolu_01ArcpfY2EMoh1ZVhbKi4ptK
```json
{
  "command": "git status && echo \"---\" && git branch --show-current",
  "description": "Check git status and current branch"
}
```

> TOOL

tool_result
id: toolu_01ArcpfY2EMoh1ZVhbKi4ptK
```
On branch examples/06-japanese-document
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   examples/06-japanese-document/README.md
	new file:   examples/06-japanese-document/input.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.claude/
	.cursor/
	.entire/
	.hugo_build.lock
	public/

---
examples/06-japanese-document
```

> TOOL

tool_use Bash
id: toolu_01Hth6tkT1j5CDZs3r8yGWS4
```json
{
  "command": "git diff --staged",
  "description": "Show staged changes"
}
```

> TOOL

tool_result
id: toolu_01Hth6tkT1j5CDZs3r8yGWS4
```
diff --git a/examples/06-japanese-document/README.md b/examples/06-japanese-document/README.md
new file mode 100644
index 0000000..5581b28
--- /dev/null
+++ b/examples/06-japanese-document/README.md
@@ -0,0 +1,48 @@
+# Example: 完全日本語ドキュメント（PRD）
+
+仮想プロダクト「ChouseiNeko v2.0」のプロダクト要件定義書（PRD）です。
+**完全に日本語で書かれた実務文書**として、md2pdf の日本語レンダリング
+品質を確認するためのショーケースです。
+
+`examples/01-design-doc` が「英語ベース＋日本語混在の技術文書」だったのに
+対し、こちらは「**敬体（ですます調）で書かれた、非エンジニアにも読まれる
+ビジネス文書**」を想定しています。
+
+## 含まれるファイル
+
+- `input.md` — 入力Markdown
+- `output.pdf` — md2pdf で生成されたPDF（リポジトリにコミット）
+
+## このサンプルが示すもの
+
+- ✅ 完全日本語の見出し・本文（敬体）
+- ✅ Mermaid **フローチャート**（v1 と v2.0 の操作フロー比較）
+- ✅ Mermaid **ガントチャート**（リリース計画）
+- ✅ GitHub Flavored Markdown の表（KPI・ペルソナ・成功指標など複数）
+- ✅ コードブロック（JSON によるAPIスキーマ例）
+- ✅ ユーザーインタビューの肉声を再現する引用ブロック
+- ✅ MUST / SHOULD / COULD で整理した箇条書きとスコープ定義
+- ✅ 変更履歴・関連ドキュメント・用語集など実務PRDの定型要素
+
+## PDFを再生成する
+
+```sh
+md2pdf -o examples/06-japanese-document/output.pdf examples/06-japanese-document/input.md
+```
+
+書式の調整例:
+
+```sh
+md2pdf \
+  -page-size A4 \
+  -margin-top 20mm -margin-bottom 20mm \
+  -margin-left 18mm -margin-right 18mm \
+  -o examples/06-japanese-document/output.pdf \
+  examples/06-japanese-document/input.md
+```
+
+## 想定される利用シーン
+
+- プロダクトマネージャーが Markdown で書いた PRD を、社内向けに PDF で配布
+- 経営層・営業・カスタマーサクセスへの共有資料として配布
+- レビュー後にバージョン管理した PDF をクライアントへ提示
diff --git a/examples/06-japanese-document/input.md b/examples/06-japanese-document/input.md
new file mode 100644
index 0000000..8f7b14f
--- /dev/null
+++ b/examples/06-japanese-document/input.md
@@ -0,0 +1,402 @@
+# プロダクト要件定義書（PRD）
+
+## ChouseiNeko v2.0「スマート予約」機能
+
+| 項目 | 内容 |
+|---|---|
+| ドキュメント番号 | PRD-CN-2026-005 |
+| バージョン | 2.0 |
+| 作成者 | プロダクト本部 山田 太郎 |
+| レビュアー | 田中（エンジニアリング）、佐藤（デザイン）、鈴木（営業） […]

> TOOL

tool_use Bash
id: toolu_01XS2uxeL8gaFn6rS1LyXEUD
```json
{
  "command": "git log --oneline -10",
  "description": "Check recent commits for style"
}
```

> TOOL

tool_result
id: toolu_01XS2uxeL8gaFn6rS1LyXEUD
```
fd93c04 ✨ feat: add design doc example showcasing mixed EN/JA (#26)
ebe1012 :bookmark: release: v0.2.4
508348b 📝 docs: sharpen README positioning and audience (#25)
742f432 :bookmark: release: v0.2.3
6db028e 🐛 fix: escape quotes in Mermaid block matcher (#24)
9252e57 chore(ci): bump actions/upload-pages-artifact from 3 to 5 (#23)
236b1fd chore(ci): bump actions/checkout from 4 to 6 (#22)
822075a chore(ci): bump actions/deploy-pages from 4 to 5 (#21)
f44d56c chore(ci): bump actions/configure-pages from 5 to 6 (#20)
047aca4 Inline critical CSS to boost mobile performance (#19)
```

> TOOL

tool_use Bash
id: toolu_01C3SarF2yLbCnxni61x1wjf
```json
{
  "command": "git commit -m \"$(cat <<'EOF'\n✨ feat: add full-Japanese PRD example\n\nAdd examples/06-japanese-document showcasing a complete Japanese product\nrequirements document, covering Mermaid flowchart and gantt diagrams,\nmultiple GFM tables, JSON code blocks, and quotes — to validate Noto Sans\nCJK JP rendering on a non-engineering business document.\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <<REDACTED_EMAIL>>\nEOF\n)\" && git status",
  "description": "Commit staged changes"
}
```

> TOOL

tool_result
id: toolu_01C3SarF2yLbCnxni61x1wjf
```
[examples/06-japanese-document d237c75] ✨ feat: add full-Japanese PRD example
 2 files changed, 450 insertions(+)
 create mode 100644 examples/06-japanese-document/README.md
 create mode 100644 examples/06-japanese-document/input.md
On branch examples/06-japanese-document
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.claude/
	.cursor/
	.entire/
	.hugo_build.lock
	public/

nothing added to commit but untracked files present (use "git add" to track)
```

> AGENT

コミット完了しました。

**コミット**: `d237c75` ✨ feat: add full-Japanese PRD example
- `examples/06-japanese-document/README.md` 新規追加
- `examples/06-japanese-document/input.md` 新規追加（450行追加）

**次のステップ案**:
- `git push -u origin examples/06-japanese-document` でリモートへプッシュ
- `output.pdf` を生成してコミットに追加（READMEで言及されているため）
- PR作成（`/commit-commands:commit-push-pr` または `gh pr create`）

未追跡の `.claude/`, `.cursor/`, `.entire/`, `.hugo_build.lock`, `public/` はローカル作業ファイルのため、コミットには含めていません。必要なら `.gitignore` への追加を検討してください。

> DEVELOPER

create pr

> TOOL

tool_use Bash
id: toolu_01Y5vquGiQGW669oxjvUNWBD
```json
{
  "command": "git status",
  "description": "Check git status"
}
```

> TOOL

tool_result
id: toolu_01Y5vquGiQGW669oxjvUNWBD
```
On branch examples/06-japanese-document
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.claude/
	.cursor/
	.entire/
	.hugo_build.lock
	public/

nothing added to commit but untracked files present (use "git add" to track)
```

> TOOL

tool_use Bash
id: toolu_012h7LGwvdZHx2PdcdHug5he
```json
{
  "command": "git log main..HEAD --oneline",
  "description": "Show commits ahead of main"
}
```

> TOOL

tool_result
id: toolu_012h7LGwvdZHx2PdcdHug5he
```
d237c75 ✨ feat: add full-Japanese PRD example
```

> TOOL

tool_use Bash
id: toolu_01WGjr2LY7WgeCCThTCAeLmm
```json
{
  "command": "git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>&1 || echo \"no upstream\"",
  "description": "Check upstream tracking"
}
```

> TOOL

tool_result
id: toolu_01WGjr2LY7WgeCCThTCAeLmm
```
fatal: no upstream configured for branch 'examples/06-japanese-document'
no upstream
```

> TOOL

tool_use Bash
id: toolu_01KLxYaarnANUhPkPstCoXzY
```json
{
  "command": "git diff main...HEAD --stat",
  "description": "Show diff stats vs main"
}
```

> TOOL

tool_result
id: toolu_01KLxYaarnANUhPkPstCoXzY
```
 examples/06-japanese-document/README.md |  48 ++++
 examples/06-japanese-document/input.md  | 402 ++++++++++++++++++++++++++++++++
 2 files changed, 450 insertions(+)
```

> TOOL

tool_use Bash
id: toolu_01KxDwwYGrjkBofktUNQd8vp
```json
{
  "command": "git push -u origin examples/06-japanese-document",
  "description": "Push branch to remote"
}
```

> TOOL

tool_result
id: toolu_01KxDwwYGrjkBofktUNQd8vp
```
[entire] Pushing entire/checkpoints/v1 to origin..... done
remote: 
remote: Create a pull request for 'examples/06-japanese-document' on GitHub by visiting:        
remote:      https://github.com/135yshr/md2pdf/pull/new/examples/06-japanese-document        
remote: 
To github.com:135yshr/md2pdf.git
 * [new branch]      examples/06-japanese-document -> examples/06-japanese-document
branch 'examples/06-japanese-document' set up to track 'origin/examples/06-japanese-document'.
```

> TOOL

tool_use Bash
id: toolu_01TqTVUpRxGM7B6g9BzpbhxV
```json
{
  "command": "gh pr create --title \"✨ feat: add full-Japanese PRD example (06-japanese-document)\" --body \"$(cat <<'EOF'\n## Summary\n- 完全日本語のプロダクト要件定義書（PRD）を題材にしたサンプル `examples/06-japanese-document` を追加\n- Mermaid フローチャート・ガントチャート、GFM 表、JSON コードブロック、引用、箇条書きを含み、Noto Sans CJK JP の日本語レンダリング品質を確認できる実務文書ショーケース\n- 既存の `examples/01-design-doc`（英語ベース＋日本語混在）とは異なる、敬体（ですます調）で書かれた非エンジニア向けビジネス文書という位置付け\n\n## Test plan\n- [ ] `md2pdf -o examples/06-japanese-document/output.pdf examples/06-japanese-document/input.md` でPDFが生成できることを確認\n- [ ] 生成PDFで日本語フォント（Noto Sans CJK JP）が正しく描画されていることを確認\n- [ ] Mermaid フローチャートとガントチャートが正しくSVGとしてインライン化されていることを確認\n- [ ] GFM の表（KPI・ペルソナ等）、JSON コードブロック、引用ブロックが意図通り表示されることを確認\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\nEOF\n)\"",
  "description": "Create pull request"
}
```

> TOOL

tool_result
id: toolu_01TqTVUpRxGM7B6g9BzpbhxV
```
Warning: 5 uncommitted changes
https://github.com/135yshr/md2pdf/pull/27
```

> AGENT

PR作成完了しました。

**PR #27**: ✨ feat: add full-Japanese PRD example (06-japanese-document)
🔗 https://github.com/135yshr/md2pdf/pull/27

未コミットの5ファイル（`.claude/`, `.cursor/`, `.entire/`, `.hugo_build.lock`, `public/`）は警告が出ましたがローカル作業ファイルのため含めていません。必要なら `.gitignore` への追加をご検討ください。

> TOOL

tool_use Bash
id: toolu_016Z6wLbeLc4QfBpH6eFxc1N
```json
{
  "command": "git status && echo \"---BRANCH---\" && git branch --show-current",
  "description": "Check status and branch"
}
```

> TOOL

tool_result
id: toolu_016Z6wLbeLc4QfBpH6eFxc1N
```
On branch docs/comparison-images
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   README.md
	new file:   docs/images/comparison/after-md2pdf-japanese.png
	new file:   docs/images/comparison/before-md-to-pdf-japanese.png
	new file:   docs/images/comparison/before-pandoc-japanese.png

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.claude/
	.cursor/
	.entire/
	.hugo_build.lock
	docs/images/before-pandoc-japanese.png
	public/

---BRANCH---
docs/comparison-images
```

> TOOL

tool_use Bash
id: toolu_016HggdxuqjnQaV6ozjG1PCR
```json
{
  "command": "git diff --staged",
  "description": "Show staged diff"
}
```

> TOOL

tool_result
id: toolu_016HggdxuqjnQaV6ozjG1PCR
```
diff --git a/README.md b/README.md
index 71b4db3..7b57583 100644
--- a/README.md
+++ b/README.md
@@ -7,8 +7,13 @@ docs, runbooks, security reports — into clean, deliverable PDFs. Mermaid
 diagrams render as inline SVG. Japanese (and other CJK) text renders without
 font breakage. Single Go binary, drop-in for CI.
 
-<!-- TODO(#2): docs/images/before-after.png を追加したらここに掲載 -->
-<!-- ![Before / After](docs/images/before-after.png) -->
+<p align="center">
+  <img src="docs/images/comparison/after-md2pdf-japanese.png"
+       alt="Sample PDF generated by md2pdf with Japanese text and Mermaid flowchart"
+       width="700">
+  <br>
+  <em>Output of <code>examples/06-japanese-document</code>: Japanese text and a colored Mermaid flowchart, both rendered cleanly.</em>
+</p>
 
 ## Features
 
@@ -154,6 +159,26 @@ flowchart TD
 3. **Build HTML** — a self-contained HTML file is assembled with GitHub-flavored CSS, `@font-face` declarations for Noto Sans CJK JP, and the rendered SVGs injected inline.
 4. **Print PDF** — a headless Chromium browser (via Playwright) loads the HTML and prints it to PDF.
 
+## Comparison with other tools
+
+Pandoc, md-to-pdf, and other Markdown-to-PDF tools are powerful and flexible.
+md2pdf focuses on a narrower use case: turning **technical Markdown with
+Mermaid diagrams and Japanese (CJK) text into clean PDFs with minimal setup**.
+
+The screenshots below show what happens when you convert the same Japanese
+PRD […]

> TOOL

tool_use Bash
id: toolu_01AYwRkHqMdcHnZQHSxeXMwr
```json
{
  "command": "git commit -m \"$(cat <<'EOF'\n✨ feat: add comparison screenshots to README\n\nAdd side-by-side screenshots comparing md2pdf with Pandoc and md-to-pdf\non the same Japanese PRD document, and replace the placeholder TODO at\nthe top of the README with the md2pdf hero image. Helps new readers\nimmediately see why md2pdf exists for the CJK + Mermaid combination.\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <<REDACTED_EMAIL>>\nEOF\n)\" && git status",
  "description": "Commit staged changes"
}
```

> TOOL

tool_result
id: toolu_01AYwRkHqMdcHnZQHSxeXMwr
```
[docs/comparison-images 52364fe] ✨ feat: add comparison screenshots to README
 4 files changed, 27 insertions(+), 2 deletions(-)
 create mode 100644 docs/images/comparison/after-md2pdf-japanese.png
 create mode 100644 docs/images/comparison/before-md-to-pdf-japanese.png
 create mode 100644 docs/images/comparison/before-pandoc-japanese.png
On branch docs/comparison-images
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.claude/
	.cursor/
	.entire/
	.hugo_build.lock
	docs/images/before-pandoc-japanese.png
	public/

nothing added to commit but untracked files present (use "git add" to track)
```

> AGENT

コミット完了しました。

**コミット**: `52364fe` ✨ feat: add comparison screenshots to README
- `README.md` ヒーロー画像と比較セクションを追加
- `docs/images/comparison/` 配下に3枚のスクリーンショット追加（after-md2pdf / before-md-to-pdf / before-pandoc）

**次のステップ案**:
- `git push -u origin docs/comparison-images` でリモートへプッシュ
- PR作成（`/commit-commands:commit-push-pr` または `gh pr create`）
- 重複ファイル `docs/images/before-pandoc-japanese.png`（未追跡）は `docs/images/comparison/` 配下に既にコミット済みのため削除を検討

未追跡の `.claude/`, `.cursor/`, `.entire/`, `.hugo_build.lock`, `public/` はローカル作業ファイルのため含めていません。