# Preferences: sagit-chu

## Intent Distribution

| Intent | Share |
|--------|-------|
| debug | 33.8% |
| create new code | 26.0% |
| other | 13.0% |
| understand | 9.1% |
| git | 6.5% |
| refactor | 6.5% |
| test | 5.2% |

Debugging dominates. The user surfaces bugs from production use, pastes the symptom, and expects the agent to analyze and fix without further prompting.

## Pushback Distribution

| Type | Share |
|------|-------|
| non_pushback | 50.6% |
| correction | 29.9% |
| failure_report | 14.3% |
| takeover | 5.2% |

Half of exchanges are accepted without pushback. Corrections are the primary friction point — not rejection of the whole approach, but scope trimming and redirection.

## What Satisfies

- Agent produces a numbered plan document in `plans/` and begins implementation without asking for confirmation.
- Implementation passes "编译测试是否通过" or "安装依赖看看能否编译通过".
- Agent resolves a bug in one pass so the user can move to the next task.
- Agent chooses the recommended option without requiring the user to explain why.

## What Triggers Correction

- Agent proposes touching files/systems outside the stated scope ("可能影响转发，这个不要", "转发CRUD操作 这个应该也不用改").
- Agent gives a long analytical summary instead of jumping to implementation or writing a plan doc.
- Agent's fix doesn't fully resolve the problem — user replies with the same error + "还是报错" or "重新检查一下".
- Agent misunderstands the semantics of a domain field (e.g., `connectIp` dual role as listen address and upstream address).

## Workflow Habits

- **Plan-then-execute**: Opens complex features with GitHub issue link + "计划一下" or "分析下", then fires "实施" or "开始实施".
- **Numbered plan docs**: Expects agent to write `plans/<NNN>-<title>.md` files and check off tasks as they complete. References plans by number: "211任务", "211任务中".
- **Docker build as punctuation**: After any frontend change, issues the standard docker build+push command to verify and publish.
- **Git at session end**: Closes sessions with "提交代码并且push" or "提交全部变更并且push，创建pr".
- **No TDD**: Tests are validation ("编译测试是否通过"), not written first. Test intent is 5.2% of prompts.
- **No explanations requested**: User almost never asks "how does this work" — they ask "fix it" or "implement it".
- **Agent.md tuning**: Occasionally adds standing instructions to the agent config file to change default behavior for all future sessions.
- **Upgrade compatibility awareness**: Tracks version upgrade paths explicitly; when a bug surfaces post-upgrade, frames the fix as a compatibility problem not a fresh bug.

## Stack Preferences Visible in Prompts

- Go backend (`go-backend/`)
- Vite + React frontend (`vite-frontend/`)
- Docker images on `ghcr.io/sagit-chu/`
- `linux/amd64` architecture explicit in every build command
- GitHub Issues + PRs for feature tracking
- SQLite (evidenced by SQL error pastes)
- OpenCode as the agent
