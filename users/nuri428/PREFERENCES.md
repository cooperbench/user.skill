# Preferences — nuri428

## Pushback distribution

| Type | Rate |
|------|------|
| non_pushback | 55% |
| correction | 36.2% |
| failure_report | 6.2% |
| rejection | 2.5% |

## What triggers correction (36.2%)

1. **English-only response**: corrects immediately — "앞으로 답은 최대한 한글로 해줘"
2. **Agent creates Docker containers for external services**: external DBs (MariaDB,
   OpenSearch, Neo4j) are always pre-existing on 192.168.0.10 — never to be dockerised
3. **Agent stopping short or summarising instead of doing**: "순서대로 작업을 진행해줘", "계속해"
4. **Wrong port convention**: dev = 4만번대 (48xxx), prod = 5만번대 (58xxx)
5. **Task done but agent asks for next steps** instead of proceeding: user fires the
   next PDCA command directly
6. **Agent reports completion then asks "진행할까요?"**: user bypasses with next command

## What triggers failure_report (6.2%)

- Plugin not found / session crash: "이 컴에 설치된 claude가 오류가 생긴것 같은데 점검 바람"
- "Unknown skill: claude-dashboard:setup" (plugin not installed)
- Server-side errors the agent can't resolve (rate limit, websocket, etc.)
- **Does not narrate failures** — just pastes the error or states the symptom tersely

## What triggers rejection (2.5%)

- Agent completes a task but user was already invoking the *next* slash command: result
  is dropped silently and the new command takes over ("Unknown skill: pdca" fired while
  agent was still returning the plan-complete summary)

## What satisfies

- Agent reads `claude.md`, `tasks.md`, `project.md` at session start without being told
  which files specifically to load
- Agent sorts tasks by criticality automatically
- Agent commits and records work history in a resumable format
- Korean-language output throughout
- PDCA cycle executed end-to-end (plan → design → do → analyze → iterate → report → archive)
- External DB connections validated; headless browser used on GUI-less server

## Workflow habits

- **PDCA-first**: structures all feature work through the bkit PDCA plugin cycle
- **Session-boundary rituals**: always loads state at start ("claude.md를 읽어서..."), always
  saves state at end ("잔여작업을 기록해줘", "작업 내역을 저장해줘")
- **Token-aware**: monitors usage via `/claude-dashboard:check-usage`, winds down before
  hitting limits and requests a spec dump for the next session
- **Commit-then-continue**: after significant work, asks for a commit then immediately
  moves to the next task without waiting for confirmation
- **Does not ask for explanations**: just results — the agent's reasoning in output is
  largely ignored; the user reads task completion signals, not methodology prose
- **Plugin exploration**: experiments with new Claude Code plugins (ohmyclaudecode, rc,
  remote-control, claude-dashboard) and expects the agent to help install or debug them
- **No test-driven mindset**: tests are requested after implementation ("지금 프론트엔드에
  페이지 기능들이 정상적인지 체크가 필요해"), not before
- **IBM Design Language preference**: UI work defaults to IBM Black / data-driven aesthetic

## Stack preferences visible in prompts

- Docker Compose (dev/prod split by port range)
- FastAPI backend, React frontend
- MariaDB, Neo4j (knowledge graph), OpenSearch (full-text), Redis
- Playwright for E2E (headless on server)
- bkit plugin ecosystem (PDCA, entire, claude-dashboard)
