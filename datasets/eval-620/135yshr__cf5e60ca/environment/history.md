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