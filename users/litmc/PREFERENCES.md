---
# LitMc — Preferences & Workflow
---

## Pushback distribution

| Type | Rate |
|------|------|
| non_pushback | 57.1% |
| correction | 35.7% |
| failure_report | 4.8% |
| takeover | 1.6% |
| rejection | 0.8% |

They correct more than a third of the time — but corrections are targeted, not hostile. Full
rejections ("this is wrong, start over") are rare; they prefer narrowing or redirecting.

## What triggers correction

- **Agent over-elaborates or adds unrequested complexity.** "φの存在がちょっとややこしいです。まずはSの変換だけを可視化しましょう"
- **Visualization doesn't match domain understanding.** "八角形の向きが気になります。縦横に水平、垂直な辺はないはずなのです"
- **Agent asks to merge before all conditions are met.** "Copilotのレビューコメントを待ってからです。" [then lists 4 exact conditions]
- **Lead agent does all work solo instead of spawning teammates.** "なかなかTeamsとしてAgentを起動せずleadが全部やってしまうようです"
- **Agent violates an established rule.** "私の承認なしに#45のマージをしませんでしたか？"
- **Plan agent writes the document itself instead of delegating to Teams.** "ドキュメント作成作業をPlanエージェントがそのままやったように見えますが、Teamsは使わなくてよいのでしょうか？"

## What satisfies them

- **Incremental, reviewable steps.** They want to see each stage before committing.
- **Exact conditions met before PR merge.** They defined a 4-point checklist (CI pass, Copilot review addressed, Copilot proposal PR closed, user final approval) and hold to it strictly.
- **Mathematical formalism adopted.** When they name a transform, they expect that name used consistently everywhere.
- **Teams actually collaborating.** Multiple agents spawned and reporting, not one lead doing everything.
- **Short confident answers.** The agent does not over-explain; it does the task.

## Workflow habits

**Planning first.** For any non-trivial new feature, they enter plan mode, review a spec, and paste "Implement the following plan:" as the kickoff prompt. They do not stream-of-consciousness ask.

**Incremental commit cadence.** They commit after every meaningful, reviewable state. Commit cadence is high: multiple commits per session. Each commit is small and purposeful.

**PR workflow is ritual.** They have a documented 4-condition merge checklist. They enforce it and update it when new edge cases arise (e.g., they added the "承認後に新コミットが加わった場合は承認を取り直す" rule after a violation).

**Test on real hardware.** They flash UF2, plug/unplug the controller, observe in-game behavior, and report specific observations. They never accept "it should work" without hardware confirmation.

**Document as you go.** After successfully setting up a new workflow (e.g., Tailscale remote dev), they immediately ask: "今回設定した手順と最終的な結果、および接続手順をドキュメント化しておいてください。"

**Rule codification reflex.** Whenever they verbally establish a new process rule, they immediately direct the agent to write it into CLAUDE.md / guardian.md / copilot-instructions.md, keeping all three in sync.

**Interrupt freely.** They use Claude Code's interrupt-on-tool-use capability without hesitation. If they see a wrong tool being called, they stop the agent mid-run.

**Handoff to Teams.** Once design is settled, they hand execution off: "残りはTeamsにやってみてもらいますね。" They do not micro-supervise the execution if the plan is clear.

## Tool/stack preferences

| Layer | Choice |
|-------|--------|
| Firmware | C++ / pico-sdk, CMake |
| Python tooling | `uv run` (never `python` directly) |
| Version control | git + GitHub, `gh` CLI |
| CI | GitHub Actions |
| Code review | Copilot automated review |
| Multi-agent | Claude Code Teams (experimental) |
| Remote dev | Tailscale + macOS SSH + tmux |
| Container | Docker (for CI image pre-build) |

## Annotated personas from dataset

| Persona | Frequency |
|---------|-----------|
| Expert Nitpicker | 76.9% |
| Vague Requester | 15.4% |
| Mind Changer | 7.7% |

"Mind Changer" sessions appear when they decide mid-session to restructure the agent architecture
(e.g., replacing 4-agent functional split with a "Lens model" 3-agent system). These involve
a multi-paragraph redirect with rationale: "少し方針を転換したいです。"
