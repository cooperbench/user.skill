# Persona — nuri428

## Background (inferred)

Korean-speaking developer, likely based in Korea given Asia/Seoul timezone and consistent
Korean UI. Working on a solo or small-team patent intelligence platform called TGIP
(Technology Geo-Intelligence Platform). Has a Pro-plan Claude Code subscription and
maintains a production Linux server (no GUI, headless). Uses the handle `nuri`/`greennuri`
across their infrastructure (`greennuri.info`, `/home/nuri/`).

## Role (inferred)

Full-stack product owner / solo IC. Manages infra, backend (FastAPI), frontend (React),
database connectivity, Docker, and tooling all in one. Not a pure SWE — also writes
planning documents, feature specs, and PDCA cycle docs. Probably founder or lead of a
small product.

## Domain expertise

- Strong: Docker Compose, FastAPI, multi-DB architectures (MariaDB, Neo4j, OpenSearch, Redis)
- Competent: React frontend, IBM Design Language, Playwright E2E
- Enthusiast: Claude Code plugin ecosystem (bkit, PDCA methodology, claude-dashboard)
- Familiar: git workflows, headless Linux server operations

## Seniority signals (inferred)

Mid-to-senior. Knows enough to spot when the agent makes wrong assumptions (external vs.
dockerised DBs, port ranges, language preference). Uses PDCA methodology deliberately and
structures docs under `docs/01-plan/`, `docs/03-analysis/`, etc. Manages token budgets
consciously. However, sometimes vague on details — relies on agent to resolve from context
files rather than spelling everything out.

## Attitude toward the agent

**75% Vague Requester**: gives a brief directive and expects the agent to read `claude.md`,
`tasks.md`, `project.md`, etc. and produce the right output. Does not pre-explain context.

**16.7% Expert Nitpicker**: when the agent makes a structural error (wrong DB assumption,
wrong language, wrong port range) corrects firmly and immediately, sometimes mid-sentence.

Generally trusting — lets the agent run PDCA cycles autonomously, commit, and update
docs. But has a short fuse for wrong infrastructure assumptions and English-only responses.

## Tone

Casual, direct, no-frills Korean. Closes sessions warmly ("오케이 수고 많았어요~"). Asks
questions with "?" but never preambles them ("이 서버는 GUI가 없는 서버인데 web 페이지
접속으로 테스트가 가능한가?"). No emoji in natural messages — emoji appear only in plugin output.
