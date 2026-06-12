# PREFERENCES

## Pushback distribution

| Type | Rate |
|------|------|
| non_pushback | 79.5% |
| correction | 17.9% |
| failure_report | 1.6% |
| rejection | 1.1% |

He mostly accepts agent output. When he corrects, corrections are specific and non-negotiable.

## What triggers corrections

- **Agent retains structures he explicitly asked to remove**: agent kept `commands/` after he said to move everything to `skills/` → immediate multi-line re-instruction
- **Agent uses wrong format**: skill format doesn't match existing skills → `skill のフォーマットは他の skill を参考にして`
- **Code assumes too narrow a case**: `bare.git とは限らない` — line-level precision
- **Subagent context not propagated**: `commitlint の設定をうまく読めていないか、subagent の引き継ぎに問題があるかも`
- **Missing verification step**: expects agent to verify after code change — `スクリプト修正後、期待通りに動作するかどうか実際に確認して`
- **Wrong scope inferred in commit message**: `1 で scope は不要`
- **Fact-checking skipped on review comments**: requires agent to verify review feedback before applying

## What triggers rejection

- Agent performs an irreversible action he didn't explicitly authorize (merge without being asked)
- A command that doesn't exist (`diffit`, `idea`, `idea1`) — pastes raw shell error, no commentary

## What satisfies him

- Autonomous execution without asking for confirmation: he expects the agent to run entire PR watch loops (30–120 min) without interruption
- Short completion summaries (a few lines, not paragraphs)
- Draft PRs created and URL returned — that's the completion signal
- When he selects option `1` or `A`, the agent proceeds immediately without re-confirmation

## Workflow habits

- **Git-heavy**: 36.3% of all prompts are git-intent — creates PRs, commits, watches CI, bumps versions — all via slash commands
- **Slash-command-driven**: `/git:pr-create`, `/git:pr-watch`, `/git:commit`, `/bump-version` — invokes without args, expects the skill to infer context from repo state
- **Never asks for planning first**: opens with the task directly, not "let's plan"
- **No test-driven development**: `test` intent is only 2.9%; testing is done ad-hoc on real directories
- **Commit cadence**: commits frequently via slash command after each change; always via `/git:commit`, never manual
- **Does not ask for explanations**: intent `understand` is only 3.4%; when he asks it's a specific architectural question ("ページングにより全てのステータス確認できてない可能性ある？"), not "explain this to me"
- **Interrupts and restarts**: if a tool call goes wrong he cancels and redirects; does not wait for the agent to recover on its own
- **Verification required**: after any script or functional change, expects the agent to actually run it: `期待通りに動作するかどうか実際に確認して`

## Stack and tool preferences

- Python 3 for hooks (specified explicitly when creating hookify plugin)
- No external YAML dependencies — "外部依存なしの簡易実装"
- Conventional Commits + commitlint for all commit messages
- Draft PRs always; never direct merge without explicit instruction
- Japanese for all skill/agent markdown content; English for code identifiers
- `@"agent-name"` syntax to delegate to specialized agents
- Fact-check via tech-research skill, with MCP overrides: terraform MCP > all for Terraform; google-developer-knowledge MCP > all for GCP
