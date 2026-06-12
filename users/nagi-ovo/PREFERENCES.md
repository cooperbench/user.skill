---
name: nagi-ovo-preferences
description: What triggers corrections/rejections, workflow habits, and what satisfies this user
---

# Preferences

## What triggers corrections (46% of pushbacks)

- **Wrong commit keyword**: using "Closes" when should be "Ref", or vice versa — immediate one-line correction
- **Missing locales**: agent updates 1–3 of 10 languages; user catches it with "并没有修改所有语言吧" or "你确定语言都全了吗"
- **Unsolicited push**: agent pushes to remote without being asked — "卧槽谁让你 push 了"
- **Over-formatting**: agent formats `.claude/` files that should not be formatted — "wait .claude 里的内容不要被 format,撤回后重新 format"
- **Scope creep**: agent changes things beyond what was asked (e.g., renames in generate-sponsor script when asked only for minimal changes)
- **Visual slop**: design changes that make everything the same color ("一坨绿"), or lack genuine aesthetic improvement
- **Wrong assumptions about users**: broad population issue treated as universal ("注意啊，不是所有用户都遇到了，是个别用户")
- **Incorrect political/geographic framing**: "Taiwan 不是繁体中文，你涉嫌政治了"
- **Version number mismatch**: agent uses wrong version; user checks manifest

## What triggers rejections (3.3% of pushbacks)

- Agent proposes solution requiring additional permissions the user doesn't want: "这样也不好，不要加权限"
- Design output is too timid / "AI slop" — triggers `/bolder` or `/polish` skill override
- Agent pushes before being asked

## What triggers failure reports (8.5% of pushbacks)

- Pastes screenshot when visual bug not fixed
- Pastes raw DOM when element injection fails
- Pastes terminal error verbatim when build/runtime error occurs
- Short statement: "仍然存在这个问题", "这个版本不显示 banner 了"

## What satisfies

- Implementation proceeds without errors and passes build
- Single acknowledgment: "好", "嗯", "好事" — then immediately next task
- "ok 了，commit Closes #445" — rare explicit approval before next step
- Agent commits in the right format on first try

## Workflow habits

**Build cycle**: expects agent to `bun run build:chrome` (or platform-specific) after every code change. Has stated this explicitly. Never needs to be reminded more than once per session.

**Commit format**: uses commitlint; expects conventional commits. Bump commits are separate from feature commits. Always references issues with `Fixes #xxx`, `Closes #xxx`, or `Ref #xxx`.

**Planning first**: for complex features, writes a full implementation plan (sometimes hundreds of words) before handing off with "Implement the following plan:". Does not want agent to redesign the approach.

**No explanations for simple things**: "提交" means commit and push the current staged changes. No need to summarize what is being committed.

**Does not want help with decisions already made**: "算了，不要发布到 Chrome 商店了，只弄 Edge 吧" — once the decision is stated, execute it, don't re-propose alternatives.

**Test cadence**: rarely writes tests (test intent is 0.2%). Relies on build passing and manual visual inspection.

**Documentation parallel**: expects VitePress docs and all-language READMEs to be updated alongside feature changes. Will ask "文档里是不是还缺少这些功能的介绍?" if agent forgets.

**Interrupts freely**: uses "[Request interrupted by user]" when agent is going in the wrong direction. This is not an error — it's their preferred way to redirect.

**Custom skills**: has `/bolder`, `/polish`, `/safari-release`, `/health`, `/frontend-design` skills. May invoke them mid-session by pasting the skill content as a takeover message.

## Stack and tooling preferences

- Bun over npm/yarn
- VitePress for docs
- TypeScript (strict)
- Tailwind CSS for UI
- `bun run format` before committing
- `bun run lint` / `bun run typecheck` / `bun run test` as verification chain
- `bun run bump` for version bumping
- GitHub Actions for CI/release
- No extra permissions in manifest unless strictly necessary
