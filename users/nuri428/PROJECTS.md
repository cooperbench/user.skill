# Projects — nuri428

## nuri428/patent_board_full ★ dominant (100% of sessions)

**What it is**: TGIP — Technology Geo-Intelligence Platform. A patent intelligence web
application with AI-powered search, graph-based knowledge representation, and analytical
workbench. The tagline is "하나의 기술 오브젝트 → 4가지 관찰 시점" (one tech object, four
observation angles). Decision-neutral: surfaces evidence, not recommendations.

**Inferred purpose**: Commercial or research-grade product tracking patent landscapes,
likely used for technology scouting, R&D intelligence, or IP analysis.

### Tech stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (port 8001) |
| Frontend | React (port 3000), IBM Design Language / IBM Black theme |
| MCP server | port 8082 |
| LangGraph agent | separate service |
| Database (external) | MariaDB `pa_system` + `patent_db` (51 tables) on 192.168.0.10 |
| Graph DB (external) | Neo4j `patentsKg` (667,671 nodes) on 192.168.0.10 |
| Search (external) | OpenSearch v2.16.0 on 192.168.0.10 |
| Cache | Redis v7.4.1 |
| Containerisation | Docker Compose — dev ports 48xxx, prod ports 58xxx |
| E2E tests | Playwright (headless, 12 tests, all passing as of session 3) |
| CI state | Healthy (`/health/detailed` green across all services) |

### Recurring themes in sessions

- **PDCA cycle management**: every feature goes through plan → design → do → analyze →
  iterate → report → archive using the bkit plugin
- **External service connectivity**: recurring source of bugs — `.env` misconfiguration,
  Redis port mismatches, OpenSearch health check endpoint issues
- **Frontend iteration**: IBM Black UI, page routing dead-link fixes, Dashboard
  hardcoded-data removal, React component state management
- **Docker compose stabilisation**: health checks, multi-stage builds, port unification
- **Session state persistence**: `claude.md`, `tasks.md`, `work_log.md`, `project_spec.md`
  maintained across sessions for continuity
- **Plugin/tooling exploration**: installs and debugs Claude Code plugins, monitors token
  usage, uses `/rc` and remote control features

### Infrastructure note

The server has no GUI. Web UI testing is done via headless Playwright. The production
domain is `tgip.greennuri.info`. The developer's home directory is `/home/nuri/`.
