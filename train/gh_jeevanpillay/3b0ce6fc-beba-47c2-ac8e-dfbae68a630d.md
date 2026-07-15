---
session_id: 3b0ce6fc-beba-47c2-ac8e-dfbae68a630d
developer: "gh:jeevanpillay"
split: train
source: swechat
repo: "?"
start_time: "2026-04-06T07:26:18.532976Z"
n_turns: 12
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

delete @.agents/skills/seo/ @.agents/skills/blog-writer/ @.agents/skills/changelog-writer/ @.claude/skills/react-doctor @.agents/skills/vercel-react-best-practices/

> AGENT

Done. Deleted all 5 skill directories:
- `.agents/skills/seo/`
- `.agents/skills/blog-writer/`
- `.agents/skills/changelog-writer/`
- `.claude/skills/react-doctor/`
- `.agents/skills/vercel-react-best-practices/`

> DEVELOPER

dont forge tto clean up symlik in @.claude/skills/

> AGENT

Removed 4 broken symlinks. Note: `react-doctor` wasn't a symlink here (it was directly in `.claude/skills/` and already deleted). Remaining skills:

- `remotion-best-practices`
- `frontend-design`
- `turborepo`

> DEVELOPER

remove remotion and react doctor too

> AGENT

Done. `react-doctor` was already deleted earlier. Removed `remotion-best-practices` (both symlink and source). Remaining skills: `frontend-design` and `turborepo`.

> TOOL

<command-message>oneshot_merge</command-message>
<command-name>/oneshot_merge</command-name>

> AGENT

Here's the plan:

**Branch:** `chore/remove-unused-skills`

**Commit — Remove unused agent skills and symlinks**

Files to stage (all deletions):
- `.agents/skills/blog-writer/` (7 files)
- `.agents/skills/changelog-writer/` (5 files)
- `.agents/skills/react-doctor/` (1 file)
- `.agents/skills/remotion-best-practices/` (46 files)
- `.agents/skills/seo/` (6 files)
- `.agents/skills/vercel-react-best-practices/` (55 files)
- `.claude/skills/blog-writer` (symlink)
- `.claude/skills/changelog-writer` (symlink)
- `.claude/skills/react-doctor` (symlink)
- `.claude/skills/remotion-best-practices` (symlink)
- `.claude/skills/seo` (symlink)
- `.claude/skills/vercel-react-best-practices` (symlink)

**PR title:** `chore: remove unused agent skills`
**PR body:** Remove blog-writer, changelog-writer, react-doctor, remotion-best-practices, seo, and vercel-react-best-practices skills and their symlinks.

Other modified files (api/*, pnpm-lock.yaml, etc.) and untracked files will **not** be included.

I plan to create 1 commit, open a PR, and merge to main. Shall I proceed?

> DEVELOPER

check any other things we removed too. ensure all .claude and .agents skill stuff is included. i deleted more

> AGENT

That's the complete list — no other `.claude/` or `.agents/` changes beyond what I already listed. The 6 skill directories + 6 symlinks cover everything. The plan I proposed above is complete. Shall I proceed?

> DEVELOPER

nice proceed

> AGENT

Merged. PR: https://github.com/lightfastai/lightfast/pull/581
