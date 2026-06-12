# Preferences: nicksu@polyv.net

## Pushback distribution

| Type | Rate | Meaning |
|---|---|---|
| correction | 37.7% | Agent output was wrong or misunderstood; Nick redirects |
| non_pushback | 30.4% | Accepted and moved on |
| failure_report | 27.5% | Agent claimed success but system still broken |
| takeover | 4.3% | Nick issues a new command mid-task, overriding the agent |

## What triggers corrections

- **BMAD workflow deviation**: Agent does not load `workflow.xml` or skips a pipeline step → Nick pastes the full `<steps CRITICAL="TRUE">` XML block verbatim.
- **Wrong trading logic**: Agent uses cached values instead of real-time prices; calculates take-profit direction wrong for YES vs. NO; misreads `.env` variable behavior.
- **Misunderstood state**: Agent explains what COULD be the problem instead of fixing the specific thing Nick said is wrong ("交易状态不应该禁止" — state the fact, do not diagnose).
- **Unnecessary UI complexity**: Agent proposes a mode selector in the UI when the mode is already in `.env` — corrected with one sentence.
- **Over-engineering**: Agent proposes Plan A vs. Plan B; Nick picks one and says "实现方案 B" — he does not want the debate, just the implementation.

## What triggers failure reports

- CI checks (black, isort) fail after agent claimed formatting was clean → Nick pastes the raw CI output.
- Runtime errors appear after a fix was committed → Nick pastes the log error with one Chinese line appended.
- GitHub Actions run URL shared when multiple CI errors remain.

## What satisfies Nick

- Implementation matches his short description exactly, no extra UI, no unnecessary options.
- Agent commits code when asked ("提交代码") without asking for confirmation.
- BMAD pipeline completes all steps and produces the expected artifact files.
- Agent picks up on `.env` variable as the source of truth without Nick having to repeat it.

## Workflow habits

- **BMAD-first**: Uses BMAD slash commands (`/bmad-story-team-deliver`, `/bmad-tea-testarch-automate`, etc.) to drive story delivery pipelines. Expects agents to embody BMAD personas.
- **No planning step**: Does not ask for a plan before implementation; goes straight to action commands.
- **Git is a checkpoint**: Commits after each meaningful change; uses Chinese "提交" commands; sometimes commits mid-task with "一起提交".
- **No test-driven**: Does not write tests first; test generation is delegated to BMAD TEA (Test Architect) agent after implementation.
- **Screenshots as spec**: When reporting a UI bug or state discrepancy, attaches a screenshot rather than describing it in text.
- **No PR workflow visible**: All commits go directly; no mention of PRs or branches beyond `develop`.
- **Asks for explanation rarely**: Only uses "understand" intent (~11%) when system behavior is unexpected (why trading was disabled, what a log message means).
- **Restarts as a debugging tool**: "重启服务之后..." — expects the agent to handle persistence across restarts.

## Tool/stack preferences (inferred from prompts)

- Python backend (FastAPI, loguru logging, SQLite via SQLAlchemy)
- React/TypeScript frontend dashboard
- `black` + `isort` for formatting (enforced by CI)
- BMAD framework for agent orchestration
- Polymarket CLOB API (GTC, FAK, FOK orders)
- `.env` configuration (not runtime config UI)
