---
name: git-delegate
description: "Trigger: any point where code is ready to commit/push. User never runs git themselves; always delegates with casual Japanese imperatives or stages first then asks."
---

kubokawa-dev handles staging themselves (sometimes) but always asks the agent to commit and push. The phrasing is casual, cheerful, and often uses the ー elongation marker. Never uses formal language for git requests.

**Variants observed**:
- Just push: `pushしてー`
- Commit + push combined: `コミットしてPUSHしてー`, `stagedにしたよ！コミットしてpushしてー`
- Stage done, now commit: `stagedにさせていただきました。適切なコミットメッセージでコミットしていただけますか？`
- Enthusiastic: `おお！すごい👍コミットしてプッシュしていただけますかー？`
- After a session phase: `対応した内容をコミットしてください`
- Via slash command: `/git-commit` (uses the git-commit skill)

**Example 1** (minimal):
```
コミットしてPUSHしてー
```

**Example 2** (staged first):
```
stagedにしたよ！コミットしてpushしてー
```

**Example 3** (problem push):
```
❯ git push origin main
[entire] Pushing session logs to origin...
To https://github.com/kubokawa-dev/million-pocket.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to...

PUSHしたいよーー
```
