# Preferences

## Pushback distribution

| Type | Rate | Meaning |
|---|---|---|
| non_pushback | 57.7% | Accepts or ignores agent output, fires next command |
| failure_report | 23.1% | Pastes CI/type errors or says "コケてる" |
| takeover | 11.5% | Agent finishes talking; user skips recap and issues next action |
| correction | 7.7% | Agent missed a workflow step; user corrects in ≤3 words |

## What triggers pushback

1. **CI or typecheck failure**: Immediate paste of raw log or "ci コケてる". No blame, no explanation—just the evidence.
2. **Agent forgot a branching step**: "branch 切って"—correction is always terse and specific.
3. **Agent not producing visible output**: "何も出てないのでそれを調査してほしい"—redirects to investigation.
4. **Tool misconfiguration** (tools not wired in): "read / write / edit / bash がツールとして全く使えないみたい。どうにかしてくれ"
5. **Stuck in TUI with no exit**: Reports with a laugh emoji equivalent ("w") and includes full build/session output.

## What satisfies

- Agent implements spec fully without requiring clarification
- Agent commits, pushes, and creates PR in one pass when asked
- Agent correctly identifies root causes (debugging sessions end after one iteration if the fix holds)

## Workflow habits

- **Plans before sessions**: Arrives with complete implementation specs (sometimes pre-generated with brainstorming skill). Does not iterate design with the agent.
- **No explanation requests**: Never asks "why did you do X?" or "can you explain this?" outside of the specific `understand`-intent questions about the *project's own design*, not the agent's choices.
- **Test awareness**: Includes tests in implementation specs ("テスト追加" sections), but doesn't appear to drive implementation test-first from conversation evidence.
- **Commit cadence**: Fires git commands eagerly after each logical unit. Typical sequence: `実装完了 → commit → push → create a pr`.
- **Branch discipline**: Expects the agent to create a feature branch before committing. Will correct if skipped.
- **Uses plugin skills**: Invokes `brainstorming` and `systematic-debugging` skills via the agent system when blocked or planning.
- **Interrupts freely**: Hits Ctrl-C mid-task; treats interruption as a natural workflow primitive, not an emergency.
- **Delegating scale**: Hands entire architectural subsystems to the agent (OverlayFS implementation, bash adapter, shutdown output). Trusts the agent to fill in implementation gaps from a spec.

## Stack / tool preferences visible in prompts

- **Runtime**: Bun (not Node)
- **Language**: TypeScript with strict type checking (`tsc --noEmit`)
- **AI SDK**: Vercel AI SDK (`streamText`)
- **Build**: `bun build --compile --minify --target=bun-darwin-arm64`
- **DB**: SQLite via `BunSqliteAdapter`
- **Providers**: Anthropic (primary), OpenAI, Kimi
- **VCS**: GitHub, PRs via `gh`; branch names are descriptive kebab-case (`feat/bash-fs-overlay-unification`)
