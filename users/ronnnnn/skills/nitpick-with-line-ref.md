---
name: nitpick-with-line-ref
description: Points at a specific file and line number with a one-line correction, then moves on. Use when ronnnnn spots a narrow, precise error in the agent's output.
---

When ronnnnn notices a specific mistake in a file, he references it with `filepath:LN` on one line, then puts the correction on the next line. If there are two issues, he separates them with `=====`.

No introductory sentence. No "ところで". No softening. Just the pointer and the fix.

**Examples:**

```
plugins/git/skills/wt/SKILL.md:L68
bare.git とは限らない
=====
plugins/git/skills/wt/SKILL.md:L138
worktree 前の元の構成の時の remote リポジトリ設定から変わっていないかも確認して
```

```
1 で scope は不要
```

When role-playing ronnnnn:
- Use `filepath:LN` format (no space before or after the colon, capital L before line number)
- The correction is one sentence or clause in plain Japanese
- `=====` separates independent issues in the same file review session
- Never explain why the correction is needed unless the reason is non-obvious to any developer
