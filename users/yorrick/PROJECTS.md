# Projects — yorrick

## yorrick/claude-code-plugins ★ DOMINANT (100% of sessions)

**What it is**: A monorepo of Claude Code plugins that automate and enhance the AI-coding workflow. Yorrick both uses and develops these plugins on himself — true dogfooding.

**Tech stack**: Python 3.14, uv, pyproject.toml, pytest, asyncio. macOS-native. GitHub CLI (`gh`) for issue/PR management.

**Key components** (inferred from prompts):

### `dev-loop` plugin
The core plugin. Automates the full development lifecycle:
- Takes a GitHub issue URL
- Creates a feature branch + git worktree
- Implements the plan (headless Claude agent)
- Runs smoke tests in a loop (`--max-iterations N`)
- Creates a PR
- Runs a review loop: `/simplify` + `/code-review:code-review` + `/security-review`

Exposes slash commands: `/dev-loop:dev-loop`, `/dev-loop:workflow`.

Versioned: `0.22.4`, `0.24.0`, `0.27.0` seen in session paths. Active development throughout 2026-03-13 to 2026-03-17.

### `engine.py` — StateGraph engine
A lightweight async Python graph execution engine. Nodes are async functions; edges can have conditions; supports cycles (for retry loops). Used by `dev-loop.py` internally and exposed so other scripts can build custom workflows.

Key API: `StateGraph`, `claude_node`, `shell_node`, `END`, `graph.to_mermaid()`, `graph.run()`, `--diagram` flag.

Developed during this session window as a new extraction from dev-loop internals.

### `self-improve-skill` plugin (inferred)
Mentioned indirectly. Contains `/superpowers:brainstorming`, `/superpowers:using-git-worktrees`, `/superpowers:finishing-a-development-branch`, `/superpowers:executing-plans`.

### `CLAUDE.md`
The project's agent instruction file. Yorrick treats it as the source of truth for mandatory workflow steps. Frequently updated mid-session to encode new norms (quality gates, issue tracking, brainstorm-first policy, opus+max for brainstorming).

**Recurring themes**:
- Making Claude Code agents more autonomous (headless, skip-permissions)
- Progress visibility: silent background jobs are a pain point ("we don't have any kind of feedback")
- Multi-model orchestration: detecting Codex/Gemini availability and using them as nodes
- Distribution: how to ship plugins so others can install them via the Claude Code marketplace/git
- Quality enforcement: lint + format + typecheck + docs gates on every change

**Git workflow**: works on `main` directly for small changes; uses git worktrees + feature branches for plugin issues. PRs created via `gh pr create`, merged with `ok, merge PR`.
