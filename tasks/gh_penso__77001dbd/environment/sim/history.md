[DEVELOPER]: https://github.com/moltis-org/moltis/issues/786 might be hard to fix but at least you should add info logs to help debugging what is going on

[AGENT]: Let me explore the browser container code to understand the current logging and where to add more.

[AGENT]: Now let me read the manager and pool files to understand where `container_host` is determined.

[AGENT]: Let me check how `container_host` is configured in `BrowserConfig`.

[AGENT]: Now I have a clear picture. The issue is a Docker-in-Docker networking problem (Moltis probes `127.0.0.1` which is its own loopback, not the host's), but the ask is to add info logs to help users debug this. Let me add targeted logging. Key areas needing better logging: 1. Log `container_host` prominently when starting — this is the likely root cause 2. Log the full docker run command for reproducibility 3. After readiness timeout, fetch container logs to show what Chrome reported 4. Detect running-inside-Docker and warn about `container_host`

[AGENT]: Now let me add logging of the docker run args and the container_host in the readiness check. Also, I need to add container log fetching on failure.

[AGENT]: Now add container log fetching after readiness timeout failure:

[AGENT]: Now add the helper functions `fetch_container_logs`, `inspect_container_status`, and `is_running_in_container` before the `wait_for_ready` function:

[AGENT]: Now let me also add a log in the pool when launching a sandboxed browser, showing the `container_host`:

[AGENT]: Now let's verify it compiles:

[AGENT]: Compiles cleanly. Let me also run the browser crate tests and format check:

[AGENT]: All 86 tests pass. Let me fix the formatting:

[AGENT]: Now let me run clippy on the browser crate to make sure there are no warnings:

[AGENT]: Clean. Let me verify the final state of the changes:

[AGENT]: Here's a summary of the logging improvements: ### `container.rs` 1. **`start_with_backend`** — Now logs `container_host` when starting, so it's immediately visible which address will be probed for readiness. 2. **`start_oci_container`** — Logs the full `docker run` command arguments before executing, allowing users to reproduce the exact container launch. 3. **Readiness failure diagnostics** — When `wait_for_ready` times out: - **`fetch_container_logs()`** — Fetches the last 50 lines of container logs (`docker logs`) to show what Chrome/browserless reported inside the container (crash, permission error, missing libs, etc.). - **`inspect_container_status()`** — Runs `docker inspect` to report whether the container is still running, exited, or OOM-killed. - **`is_running_in_container()`** — Detects if Moltis itself is running inside Docker (via `/.dockerenv`, `container` env var, or cgroup markers) and if so, warns that `browser.container_host` likely needs to be set to `host.docker.internal` — which is the exact fix for issue #786. ### `pool.rs` 4. **`launch_sandboxed_browser`** — Logs `container_host`, `image`, `profile_dir`, and `session_timeout_ms` at the start of the sandboxed launch flow. With these logs, the user from #786 would have seen: - `container_host="127.0.0.1"` prominently in the startup log - Container status (running vs exited/OOM-killed) - Chrome's own error output from inside the container - A direct warning: "moltis appears to […]