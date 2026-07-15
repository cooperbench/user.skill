> DEVELOPER

why I see this error? Bifrost started on port 8081 Waiting for backend on port 8000... INFO: Will watch for changes in these directories: ['/Users/cyyeh/Desktop/duckdb-data-agent/.claude/worktrees/k8s-agent-sandbox/backend'] INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit) INFO: Started reloader process [29634] using WatchFiles Failed to create sandbox backend Traceback (most recent call last): File "/Users/cyyeh/Desktop/duckdb-data-agent/.claude/worktrees/k8s-agent-sandbox/backend/app/main.py", line 20, in <module> sandbox_backend = get_sandbox_backend() ^^^^^^^^^^^^^^^^^^^^^ File "/Users/cyyeh/Desktop/duckdb-data-agent/.claude/worktrees/k8s-agent-sandbox/backend/app/sandbox/__init__.py", line 12, in get_sandbox_backend from app.sandbox.docker_backend import DockerBackend, DockerConfig File "/Users/cyyeh/Desktop/duckdb-data-agent/.claude/worktrees/k8s-agent-sandbox/backend/app/sandbox/docker_backend.py", line 15, in <module> import docker ModuleNotFoundError: No module named 'docker'

> AGENT

The `docker` Python package isn't installed. Let me check the project dependencies.

> SYSTEM

Tool loaded.

> AGENT

The `docker` package is an **optional** dependency (line 20 in `pyproject.toml`), but `SANDBOX_RUNTIME` defaults to `"docker"` when the env var isn't set. So `get_sandbox_backend()` tries to import `docker`, which isn't installed. Two options: 1. **Install the optional docker extra:** ```bash cd backend && poetry install -E docker ``` 2. **If you don't need Docker sandboxing**, set the env var to skip it — but you'd need a valid alternative runtime (`k8s`), or don't call `get_sandbox_backend()` at all. Most likely you just need to install the optional dependency: ```bash cd /Users/cyyeh/Desktop/duckdb-data-agent/.claude/worktrees/k8s-agent-sandbox/backend poetry install -E docker ```