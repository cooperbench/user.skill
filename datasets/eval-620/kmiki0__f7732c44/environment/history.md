> DEVELOPER

いまコミットされていないファイルある？

> TOOL

tool_use Bash
id: toolu_01D9dMa47pr28wD6wmzFskun
```json
{
  "command": "git status",
  "description": "Show working tree status"
}
```

> TOOL

tool_result
id: toolu_01D9dMa47pr28wD6wmzFskun
```
On branch main
Your branch is ahead of 'origin/main' by 3 commits.
  (use "git push" to publish your local commits)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   src/app/globals.css

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	specs/references/

no changes added to commit (use "git add" and/or "git commit -a")
```

> AGENT

コミットされていないファイルは以下の通りです：

**変更あり（未ステージ）:**
- `src/app/globals.css`

**未追跡（新規）:**
- `specs/references/` ディレクトリ

また、ローカルブランチは `origin/main` より **3コミット先行** しています（未プッシュ）。