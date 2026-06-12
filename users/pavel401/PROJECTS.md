---
name: Pavel401 — Projects
---

# Projects

## Pavel401/BugViper ★ (dominant — 100% of sessions)

An AI-powered GitHub PR code review tool. When a PR is opened or updated, BugViper fetches the diff, enriches it with graph context from a Neo4j code graph, and runs one or two LLM agents (bug-hunter + security-auditor, or a single unified agent) to produce a structured review comment posted back to GitHub.

### Tech stack

- **Backend**: Python 3.x, FastAPI, pydantic-ai, uvicorn
- **Graph DB**: Neo4j with Cypher queries — stores code structure (nodes: Function, Class, Module, Variable, Import; edges: CALLS, INHERITS, IMPORTS, DEFINES)
- **Ingestion engine**: tree-sitter parsers per language (Python, TypeScript, JS, 17 languages total) — `AdvancedIngestionEngine`, `GraphBuilder`
- **Firebase/Firestore**: document store for user accounts, repo metadata, PR metadata, review run history
- **GitHub integration**: webhook listener (`/api/v1/webhook/onComment`), `GitHubClient` for fetching diffs and posting comments
- **Observability**: Logfire (pydantic's observability platform)
- **Frontend**: TypeScript / Next.js — repo management UI with ingestion status, delete confirmation dialog, full-text code search

### Architecture layers

```
GitHub webhook → api/routers/webhook.py
  → api/services/review_service.py   (orchestrates review pipeline)
    → deepagent/agent/review_pipeline.py  (LLM agent calls)
    → deepagent/prompts.py            (BUG_HUNTER_PROMPT, SECURITY_AUDITOR_PROMPT)
    → deepagent/models/agent_schemas.py   (Issue, ReviewResults, FileSummary, ReconciledReview)
  → api/utils/comment_formatter.py   (builds GitHub markdown comment)
  → common/github_client.py          (post_comment, get_diff)
  → api/services/firebase_service.py (Firestore r/w)
  → db/queries.py + db/schema.py     (Neo4j Cypher queries)
  → ingestion_service/               (tree-sitter ingestion engine, active)
  → ingestion/                       (legacy, not used in active path)
```

### Recurring themes in sessions

- **False positive reduction**: agent hallucinates because it only sees the diff, not full files. Ongoing work to inject full file snapshots, add confidence scoring (0–10, threshold at 7), semantic dedup.
- **Review reconciliation**: tracking fixed vs still-open vs new issues across PR runs via Firestore.
- **Graph relationship building**: CALL relationships missing from GitHub ingestion path (only in local path). Persistent debugging.
- **Firestore schema evolution**: adding repo metadata, PR metadata, review run history under `users/{uid}/repos/{owner}/{repo}/...`.
- **Stats correctness**: file count, function count, line count frequently wrong after schema changes. Recurrent debugging.
- **Frontend UX**: add-repo modal, ingestion status polling, delete confirmation dialog, full-text search UI.
- **Cost control**: burned money on a pydantic_deep orchestrator that made ~20 LLM calls instead of 2. Corrected to a 2-agent parallel call.
- **CLAUDE.md maintenance**: uses CLAUDE.md as live architecture documentation; expects the agent to update it and keep it from being committed to public repos (added to .gitignore, purged from history).
