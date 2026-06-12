# PROJECTS — jk-pmi

## BIDEquity/outbid-dirigent ★ dominant (100% of sessions)

**What it is**: A Python CLI tool ("the dirigent") that orchestrates Claude Code agents to implement software from a SPEC.md file. It runs a multi-step pipeline: initialize → analyze → plan → execute (per task) → review (per phase) → entropy minimization → ship (PR). Each step invokes a Claude Code skill or subagent. The user is the creator and primary developer.

**Tech stack**:
- Python with `uv` for packaging and tooling
- Pydantic for schema validation (PLAN.json, contract JSON, review JSON)
- Claude Code plugin system: skills (SKILL.md files), agents (agent definition YAML), hooks (hooks.json)
- Shell scripts for hooks and validation
- `loguru` for logging (`outbid_dirigent.executor` visible in log lines)
- GitHub Actions / PRs (uses `gh pr` CLI)
- Tested against a "smoke test" example project

**Recurring themes**:
- **Ephemeral state management**: where to store run artifacts (`.dirigent/` in repo vs. `$HOME/.dirigent/runs/<id>/`). Settled on `$HOME` approach.
- **Contract quality**: acceptance criteria must be behavioral integration tests, not grep-based structural checks. User enforced this repeatedly.
- **Entropy minimization**: post-session cleanup step to align code and docs, remove dead code, resolve contradictions.
- **Plugin architecture**: ships as a Claude Code plugin with skills, agents, and hooks packaged together.
- **Routing**: the dirigent selects a route (Greenfield/Legacy/Hybrid/Testability/Tracking) based on spec analysis. Tracking route was disabled for being too sensitive.
- **Skill/agent boundary**: frequent exploration of what can be a skill vs. a subagent, how agents are defined, whether agents can be shipped in plugins.
- **OpenCode interoperability**: importing `.opencode` skills as Claude skills on startup.

**Key files / artifacts the dirigent writes**:
- `SPEC.md` — input spec (or user-described inline with `--yolo`)
- `ARCHITECTURE.md` — generated during init
- `PLAN.json` — task plan (phases, tasks, dependencies)
- `.dirigent/contracts/phase-N.json` — acceptance criteria per phase
- `.dirigent/reviews/phase-N.json` — review results
- `$HOME/.dirigent/runs/<id>/` — ephemeral logs and state
- `manifest.json` — run metadata (creation time, commit SHA, content hashes)

**Versioning**: Python package versioned in `pyproject.toml`; Claude plugin versioned in `plugin.json`. The user bumps both together ("bump version and plugin versino").

**PRs**: Uses GitHub PRs via `gh pr`. Currently on PR #9 as of last session. Branch names follow `feat/dirigent-v2-*` or `claude/dirigent-refactor-*` patterns.
