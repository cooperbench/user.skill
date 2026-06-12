---
# 1natsu172 — Preferences
---

## Pushback Distribution

- **Non-pushback**: 71.8% — they approve most agent work, often with one word
- **Correction**: 24.8% — the primary failure mode; agent did the wrong thing or went too far
- **Failure report**: 3.0% — agent's output was broken or incomplete in a detectable way
- **Rejection**: 0.5% — rare; reserved for fundamental misunderstandings

## What Triggers Corrections

1. **Wrong scope / misread intent**: The agent ran a general test when they asked specifically to test the Conventional Commits skill split. Triggered: "違う！！！！！！！！！！Conventional-commitのSKILL分離したんだからその動作確認だよ！！！！！！！！！！！！！"

2. **Over-engineering**: The agent built a complex multi-skill pipeline for an `entire` integration. Triggered: "なんかやってることがファットすぎない？"

3. **False claims in skill content**: The agent wrote "`gh pr create` は自動的にpushする" which was wrong. Triggered: "createprスキルの「gh pr createは自動的にpushする」は嘘だったから修正して"

4. **Platform-specific language in a cross-platform skill**: Agent wrote "TUI上で" (on TUI) in skill instructions. Triggered: "TUI上でという指示は不要では？あくまで例で言っただけで、SKILLは汎用なのでVscode拡張やGUIアプリでも動く。"

5. **Redundant verbosity in skill files**: Tool name repeated in every section. Triggered: "そもそもどっちのファイルも全体的に毎回 AskUserQuestionTool を使うことを明示しているが冗長では？"

6. **Leftover workspace files**: After an eval run, the workspace directory and evals file were not cleaned up. Triggered: "@1natsu-entire-context-workspace/ これ残す必要ある？ないなら削除" and "evalsファイルも残ってる"

7. **Version numbering choice**: The agent used v2.0.0 when they wanted v0.x.x to signal beta status. Triggered: "entireのバージョンなんで2系なの？むしろBeta扱いだから0系じゃないとイカしい"

8. **Agent didn't wait for push command**: After a commit, agent should wait for "push" instruction — not push automatically.

## What Satisfies Them

- Agent verifies its understanding before implementing: they approve this pattern explicitly.
- Agent proposes a simplified approach after over-engineering: "対話UIにして" (one-sentence redirect accepted immediately).
- Compressed SKILL.md with clear diff: "OK。1.1.0としていいと思う"
- Agent cleans up correctly on first try: "一旦大丈夫！"
- Eval results show clear quality improvement: they read the table and approve quickly.

## Workflow Habits

- **Planning before implementation**: Uses EnterPlanMode, generates a detailed plan, then passes the plan text back as "Implement the following plan:" — agent executes against the plan.
- **Skill TDD**: Always runs baseline evals (without_skill) before writing the skill, then evals (with_skill) after, then reviews the diff in the eval viewer.
- **Commit cadence**: Commits after each logical unit of work. Does not batch unrelated changes. Baseline version (v1.0.0) committed before quality improvement (v1.1.0).
- **Does not explain goals from scratch each session**: Expects agent to track session context. Short commands only ("再開して", "push") after approval.
- **Interrupts rather than waits**: If they see the agent going wrong mid-task, they interrupt immediately.
- **Asks "why" rather than just correcting**: "なぜこれらの記述は残っているのか？" — they want to understand the agent's reasoning before deciding what to do.
- **Does not want explanations of what the agent did**: They can read the diff. They want status of what was done, not a narrative of it.

## Tool and Stack Preferences

- Claude Code as the agent (100% of sessions)
- `bunx skills add . -g -y` for installing skills globally
- `gh` CLI for GitHub operations
- Conventional Commits for all commit messages (has a dedicated `1natsu-conventional-commits` skill)
- `entire` CLI for session history (has a `1natsu-entire-context` skill)
- Git worktrees for isolation (references the `using-git-worktrees` superpowers skill)
- Japanese-language skill files preferred over English (asked agent to localize all skills to Japanese)
- Semantic versioning with prerelease conventions (v0.x.x for beta)
