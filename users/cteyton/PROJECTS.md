# Projects: cteyton

## PackmindHub/context-evaluator ★ (dominant — 100% of sessions)

**What it is**: A web application and CLI that evaluates AI agent documentation files (AGENTS.md, CLAUDE.md, Cursor rules, GitHub Copilot instructions) using 17 specialized evaluators, then automatically remediates identified issues using AI agents (Claude Code, Cursor, OpenCode, GitHub Copilot, OpenAI Codex).

**Tech stack**:
- Runtime: Bun
- Backend: TypeScript, Bun.serve HTTP server, SQLite (via `evaluation-repository.ts`, `remediation-repository.ts`)
- Frontend: React + TypeScript + Tailwind CSS + Chakra UI (added for tree view)
- AI providers: Claude Code CLI, Cursor Agent CLI, OpenCode CLI, GitHub Copilot CLI, OpenAI Codex CLI
- Testing: `bun test` (~1300 tests), Biome linter
- Evaluation: 17 evaluators in `prompts/evaluators/`, unified and independent evaluation formats

**Recurring themes across sessions**:

### Remediation pipeline (primary focus — ~50% of sessions)
- Plan-first 4-phase pipeline: plan errors → execute error fixes → plan suggestions → execute suggestions enrichment
- AI-powered AGENTS.md/CLAUDE.md consolidation (AI merge, not naive concatenation)
- Target agents: `agents-md`, `claude-code`, `github-copilot`, `cursor` — each with specific file path conventions
- Output types: `standard` (rule file), `skill` (SKILL.md), `generic` (inline edit)
- Prompt generator (`src/shared/remediation/prompt-generator.ts`) — heavily modified across sessions

### Evaluation engine
- File discovery (`src/shared/file-system/file-finder.ts`) — finds AGENTS.md, CLAUDE.md, Claude rules, Cursor rules, skills, linked docs
- Context scorer (`src/shared/evaluation/context-scorer.ts`) — power law penalty formula
- Impact evaluation: clone repo → apply git patch → run evaluators → compare scores

### Frontend UI
- RemediateTab: remediation config, execution, multi-remediation history, Packmind promotion
- ContextTab: grouped sections (AGENTS.md, Claude Code, GitHub Copilot, Cursor) + tree view toggle
- RemediationHistoryCard: collapsible card with unified file diff section, action summary grouped by evaluator
- Summary: score display, re-run button (debug mode only)

### Multi-agent CLI support
- Agent CLI wrappers for Cursor (`agent -p --output-format json`), OpenCode, Codex, GitHub Copilot
- Debug mode: `?debug=true` gates internal prompt sections and recalculate-score button

### Infrastructure
- Cloud mode: `CLOUD_MODE=true` env — gates LOC limit enforcement (1M lines), hides remediation CLI selector, disables deletion
- SSE progress streaming for long-running evaluations and remediations
- Changelog maintained per feature (`@CHANGELOG.md`)

**Key file paths cteyton references**:
- `src/shared/remediation/prompt-generator.ts` — most-edited file
- `src/shared/remediation/engine.ts`
- `src/api/routes/remediation.ts`
- `frontend/src/components/RemediateTab.tsx`
- `frontend/src/components/RemediationHistoryCard.tsx`
- `frontend/src/components/ContextTab.tsx`
- `prompts/context-remediation/packmind-remediation-prompt.md`
- `prompts/evaluators/completeness.md`
