> DEVELOPER

For this repo what is the runnable verification command?

> TOOL

tool_use Bash
id: toolu_01DHWZidybyv9MWS8mQMz95H
```json
{
  "command": "cat AGENTS.md && echo \"---PYPROJECT---\" && cat pyproject.toml 2>/dev/null && echo \"---MAKEFILE---\" && cat Makefile 2>/dev/null; echo \"---ls---\"; ls",
  "description": "Inspect project config for verify command"
}
```

> TOOL

tool_result
id: toolu_01DHWZidybyv9MWS8mQMz95H
```
# AGENTS.md

---PYPROJECT---
[project]
name = "drain-cycle"
version = "0.1.0"
description = "Unattended execution of a Linear cycle: one invocation drains the current cycle's Todo/Backlog issues, each in an isolated worktree under a fresh claude -p session."
requires-python = ">=3.11"
dependencies = [
    "httpx>=0.27",
    "opentelemetry-exporter-otlp-proto-http>=1.27",
    "opentelemetry-instrumentation-httpx>=0.48b0",
    "opentelemetry-sdk>=1.27",
    "python-dotenv>=1.0",
    "pyyaml>=6.0",
    "rich>=15.0.0",
]

[project.scripts]
drain-cycle = "drain_cycle.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["drain_cycle"]

[dependency-groups]
dev = [
    "pytest>=9.0.3",
]
---MAKEFILE---
---ls---
.claude/
.entire/
.private-journal/
.ruff_cache/
.worktrees/
docs/
drain_cycle/
tests/
.env  64B
.gitignore  769B
.linear_config  247B
AGENTS.md  13B
CLAUDE.md  223B
LICENSE  1.0K
README.md  16.3K
conftest.py  966B
mise.toml  24B
pyproject.toml  738B
uv.lock  78.1K
```

> TOOL

tool_use Bash
id: toolu_01S2GTksxem4wv6LyFsPvYJb
```json
{
  "command": "cat mise.toml; echo \"---\"; grep -niE \"pytest|ruff|verif|test|lint|uv run|check\" README.md | head -30",
  "description": "Check mise.toml and README for verify commands"
}
```

> TOOL

tool_result
id: toolu_01S2GTksxem4wv6LyFsPvYJb
```
[tools]
python = "3.12"
---
47:uv tool install .                                              # from a local checkout
60:The CLI reads the key from the first source that defines it: a shell-exported `LINEAR_API_KEY` wins, then `~/.drain-cycle/.env`, then a `.env` at the repo root (a dev-checkout fallback the installed tool never sees). Export it in your shell rc instead of the file if you prefer. The same precedence applies to the optional `HONEYCOMB_API_KEY` (see [Telemetry](#telemetry-optional)).
82:Omit the key to keep the `[.claude, .mcp.json]` default. Each entry is a path relative to the repo root; absent entries are skipped, and a tracked entry git already checked out is never overwritten. **Each entry must be gitignored in the target repo** — the symlink lives inside the worktree, so a non-ignored entry would be staged by the worker's `git add` and would block `git worktree remove` at teardown. The two defaults are gitignored in a typical repo; check any path you add.
84:Verify the install from anywhere:
96:uv tool install --editable .       # symlinks the checkout
155:       runs tests, commits to the issue branch, writes the handoff file,
219:Workers spawn in an isolated worktree. drain-cycle symlinks the repo's project-scoped config (`.claude/`, `.mcp.json`, and any […]

> TOOL

tool_use Bash
id: toolu_01GLxFL2izcZ26Mxeu3oUbFb
```json
{
  "command": "uv run pytest -q 2>&1 | tail -20",
  "description": "Run pytest to confirm verification command"
}
```

> TOOL

tool_result
id: toolu_01GLxFL2izcZ26Mxeu3oUbFb
```
........................................................................ [ 19%]
........................................................................ [ 38%]
........................................................................ [ 57%]
........................................................................ [ 77%]
........................................................................ [ 96%]
.............                                                            [100%]
373 passed in 47.24s
```

> AGENT

The runnable verification command is:

```bash
uv run pytest
```

Confirmed working — just ran it: **373 passed in ~47s**.

Details:
- It's a Python project (`drain-cycle`) managed with **uv**; pytest is the dev dependency (`pyproject.toml` `[dependency-groups].dev`).
- Tests live in `tests/` with a root `conftest.py`.
- There's no Makefile target or mise task defining a custom verify command — `uv run pytest` is the canonical way to run the suite. (Ruff is also present — `.ruff_cache/` — so `uv run ruff check .` would be the lint step if you want it, but it's not wired into a task either.)