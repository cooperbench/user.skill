> DEVELOPER

## Summary of Issues by Severity

| Severity | Count | Key Pattern |
|----------|-------|-------------|
| CRITICAL | 1     | Silent `let _ =` on kill during spawn rollback |
| HIGH     | 3     | Silent output channel drop; spawn failure swallowing; PID truncation |
| MEDIUM   | 6     | Unknown status sink; force_stop no-op; missing container cleanup; misleading defaults |

The most urgent fix is Issue 1 (the `let _ =` on kill results during spawn rollback in task_manager.rs). A failed kill during rollback means a running agent process with no tracker -- effectively a resource leak that only surfaces on daemon restart.</result>
<usage><total_tokens>120749</total_tokens><tool_uses>25</tool_uses><duration_ms>149182</duration_ms></usage>
</task-notification>
Full transcript available at: /private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/acc8cf36acdc10892.output

> DEVELOPER

## Positive Observations

Several patterns deserve recognition as good error handling:

1. **Pervasive `.with_context()` usage** -- Nearly every fallible operation includes a descriptive context string with relevant IDs (agent_id, run_id, task_id, file paths). This makes error chains actionable.

2. **`bail!` for validation guards** -- Profile compiler validation, env plan mismatches, and path assertions all use explicit `bail!` with descriptive messages.

3. **`RuntimeSelectionError` as a typed enum** -- The runtime selection module uses `thiserror` for structured, non-generic error types with actionable messages (e.g., "To use host execution for development only, enable --allow-insecure-host-runtime").

4. **Recovery module propagates all errors** -- The `recover_orphans` function chain uses `?` throughout with no silent swallowing.

5. **Docker kill handles terminal container states** -- The `is_terminal_container_error` function correctly treats 304/404/409 as non-errors during kill operations, avoiding false failures when a container is already stopped.

> DEVELOPER

## ISSUE 10: `RuntimeService` Defaults to `Host` Backend and `insecure=true` When No TaskManager Is Set

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/server.rs`, lines 122-136

**Severity:** MEDIUM

**Issue Description:**

```rust
fn runtime_backend_proto(&self) -> i32 {
    let backend = self
        .task_manager
        .as_ref()
        .map(|manager| manager.runtime_backend())
        .unwrap_or(forge_common::run_graph::RuntimeBackend::Host);
    runtime_backend_to_proto(backend) as i32
}

fn insecure_host_runtime(&self) -> bool {
    self.task_manager
        .as_ref()
        .map(|manager| manager.insecure_host_runtime())
        .unwrap_or(true)
}
```

When `task_manager` is `None` (which happens in the `run_server` code path without components, line 182), the service reports `RuntimeBackend::Host` and `insecure_host_runtime: true` in the health endpoint and all RunInfo/TaskInfo responses. This is a **misleading fallback** -- clients might think they're running in insecure host mode when really the task manager simply hasn't been wired in yet.

**User Impact:** API consumers (CLIs, UIs) may display security warnings about insecure host mode that are not actually relevant. Or worse, they may make decisions based on the reported backend that don't reflect reality.

**Recommendation:** When `task_manager` is `None`, report the backend as `Unknown` or `Unset` rather than silently defaulting to `Host + insecure=true`.

> DEVELOPER

## ISSUE 9: Docker Container Not Cleaned Up on Detach After Start

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/docker.rs`, lines 323-328

**Severity:** MEDIUM

**Issue Description:** After successfully starting a Docker container, `spawn_docker_attach_task` is called on a fire-and-forget tokio task. If this task encounters an error writing stdin, it returns early (line 196) without any mechanism to stop or remove the running container:

```rust
if !stdin_payload.is_empty()
    && let Err(error) = input.write_all(&stdin_payload).await
{
    emitter.emit_stderr_line(format!(
        "[forge-runtime::docker] failed to write prepared stdin payload: {error}"
    ));
    return; // Container is still running, nobody will clean it up via this task
}
```

The container continues running but never receives its stdin payload. Depending on the agent program, it may hang forever waiting for stdin.

**User Impact:** An agent container hangs waiting for stdin, consuming Docker resources. The task_manager will eventually poll it and see `Running` status, and it will appear stuck.

**Recommendation:** After failing to deliver the stdin payload, attempt to stop the container or at least log the container ID so operators know which container to inspect.

> DEVELOPER

## ISSUE 8: `send_signal` Returns `Ok(())` for `ESRCH` Without Logging

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/bwrap.rs`, lines 364-376. `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/host.rs`, lines 201-213.

**Severity:** MEDIUM

**Issue Description:**

```rust
fn send_signal(pid: u32, signal: i32) -> Result<()> {
    let rc = unsafe { libc::kill(pid as i32, signal) };
    if rc == 0 { return Ok(()); }
    let error = std::io::Error::last_os_error();
    if error.raw_os_error() == Some(libc::ESRCH) {
        return Ok(());
    }
    Err(error).context("libc::kill failed")
}
```

`ESRCH` means the process does not exist. The function silently returns `Ok(())` as if the signal was delivered. While this is a reasonable design choice for kill operations (the process is already gone), it means the caller cannot distinguish "signal delivered" from "process was already dead." Combined with Issue 7, if the TrackedChild is missing, the caller has no way to know whether the kill was effective or the process was already gone.

**User Impact:** Minor -- the behavior is defensible for kill semantics. But the lack of any tracing event means operators lose the ability to audit kill timelines.

**Recommendation:** Add a `tracing::debug!` when ESRCH is encountered so the kill timeline is auditable.

> DEVELOPER

## ISSUE 7: `kill` Method Returns `Ok(())` When TrackedChild Is Missing

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/bwrap.rs`, lines 271-303. `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/host.rs`, lines 145-174.

**Severity:** MEDIUM

**Issue Description:** In both `bwrap` and `host` kill implementations, when the `TrackedChild` is not in the process map:

```rust
if let Some(child) = self.tracked_child(&handle.agent_id).await {
    child.remember_kill_reason(kill_reason);
}

send_signal(pid, libc::SIGTERM)?;

if let Some(child) = self.tracked_child(&handle.agent_id).await {
    // ... wait logic
}
// Falls through to Ok(()) if TrackedChild is missing
```

If the `tracked_child` lookup fails on the second check (line 284/156), after the SIGTERM was sent, the method returns `Ok(())` without waiting for the process to actually terminate. The process may still be running.

**User Impact:** Callers believe the agent was killed, but it might still be winding down. State transitions based on kill completion may be premature.

**Recommendation:** Log at `debug` level when returning Ok without waiting for the child, and document that the kill is "best-effort" in this path.

> DEVELOPER

## ISSUE 6: `force_stop` Delegates to `graceful_stop` with No Escalation

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/task_manager.rs`, lines 527-529

**Severity:** MEDIUM

**Issue Description:**

```rust
async fn force_stop(&self, agent: &ActiveAgent, reason: &str) -> Result<()> {
    self.graceful_stop(agent, reason).await
}
```

The `AgentSupervisor` trait defines `force_stop` as a separate method from `graceful_stop` -- the semantic contract implies `force_stop` should succeed where `graceful_stop` might not (e.g., SIGKILL vs SIGTERM). Here, force_stop is a no-op delegation. If the `ShutdownCoordinator` calls `graceful_stop`, waits, then calls `force_stop` as an escalation, no actual escalation occurs.

**User Impact:** During daemon shutdown, if an agent does not respond to `graceful_stop` (SIGTERM), `force_stop` will also fail in the same way, leaving the agent running after daemon exit.

**Recommendation:** `force_stop` should directly call `self.runtime.kill()` which already implements SIGTERM-then-SIGKILL escalation, or should bypass the `kill_agent` method and call a more aggressive kill path.

> DEVELOPER

## ISSUE 5: `AgentStatus::Unknown` is a Silent Ambiguity Sink

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/bwrap.rs`, lines 322-327. `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/host.rs`, lines 193-197.

**Severity:** MEDIUM

**Issue Description:** In both `bwrap` and `host` runtime `status()` methods, when the `TrackedChild` is not found in the process map but the PID still exists, the process is reported as `Running`. When neither condition is met, the status is `AgentStatus::Unknown`:

```rust
if process_exists(pid) {
    Ok(AgentStatus::Running)
} else {
    Ok(AgentStatus::Unknown)
}
```

The path to `Unknown` is reached when:
1. The tracked child was removed from the process map (e.g., after a race in `check_agent_status`)
2. The PID no longer exists

No log is emitted when this happens. In `check_agent_status` (task_manager.rs line 306), `Unknown` is treated identically to `Running` and `Initializing` -- the function returns `Ok(None)`, meaning "no terminal status yet." This means a task whose agent died and whose TrackedChild was removed will **silently hang in `Running` state forever**, never transitioning to `Failed`.

**User Impact:** Tasks appear stuck in `Running` indefinitely. The only recovery path is daemon restart, which will detect the orphan and fail it.

**Recommendation:** When status returns `Unknown`, `check_agent_status` should not treat it identically to `Running`. After a configurable number of consecutive `Unknown` polls, it should transition the task […]

> DEVELOPER

## ISSUE 4: `pid as i32` Truncation in Signal Functions

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/bwrap.rs`, lines 365, 379. `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/host.rs`, lines 202, 216.

**Severity:** HIGH

**Issue Description:** The `send_signal` and `process_exists` functions cast `pid: u32` to `i32` using `as`:

```rust
let rc = unsafe { libc::kill(pid as i32, signal) };
```

A PID greater than `i32::MAX` (2,147,483,647) will silently wrap to a negative number. On Linux, `kill(-N, signal)` sends the signal to **all processes in process group N**, which could kill unrelated processes. While PIDs above i32::MAX are rare on most systems, some container runtimes and PID namespaces can produce high PIDs.

**User Impact:** In edge cases, the kill operation could terminate unrelated processes. At minimum, the wrong process gets signaled, and the actual target agent is not killed.

**Recommendation:** Add a bounds check before the cast: `if pid > i32::MAX as u32 { bail!("pid {pid} exceeds i32::MAX") }`. Alternatively, use `i32::try_from(pid).context("pid exceeds i32 range")?`.

> DEVELOPER

## ISSUE 3: `dispatch_enqueued_tasks` Swallows Spawn Failures and Continues

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/task_manager.rs`, lines 185-196

**Severity:** HIGH

**Issue Description:** When `spawn_prepared` fails for an enqueued task, the error is logged at `warn` level and execution continues to the next task:

```rust
match self.spawn_prepared(prepared).await {
    Ok(_) => launched.push(task_id),
    Err(error) => {
        tracing::warn!(
            %error,
            run_id = %run_id,
            task_id = %task_id,
            "failed to dispatch enqueued task"
        );
    }
}
```

The critical gap is: **the task is left in `Materializing` status in the orchestrator** (because `spawn_prepared` transitions to `Materializing` on line 209 before attempting the spawn on line 214). If the spawn fails on line 214, `spawn_prepared` does transition the task to `Failed` internally. But if the error occurs after a successful spawn (e.g., the state persistence fails), the task might remain stuck in `Materializing` forever with no one tracking it.

Additionally, the `dispatch_enqueued_tasks` caller in `main.rs` line 145 also swallows the method-level Result:

```rust
if let Err(error) = lifecycle_manager.dispatch_enqueued_tasks().await {
    tracing::warn!(%error, "task-manager dispatch cycle failed");
}
```

This creates a double-swallow pattern where both levels silently continue.

**User Impact:** If infrastructure is repeatedly failing (Docker daemon down, bwrap unavailable), tasks will silently cycle through `Enqueued -> Materializing -> Failed` with only `warn`-level logs. An […]

> DEVELOPER

## ISSUE 2: Silent Drop of Channel Send in RuntimeOutputSink

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/io.rs`, line 48

**Severity:** HIGH

**Issue Description:** The `RuntimeOutputSink::emit` method silently discards send failures:

```rust
fn emit(&self, envelope: RuntimeOutputEnvelope) {
    if let Some(tx) = &self.tx {
        let _ = tx.send(envelope);
    }
}
```

An unbounded channel's `send` only fails when the receiver is dropped. If the receiver is dropped, **all subsequent agent output is silently lost** -- task stdout, stderr, progress events, everything.

**Hidden Errors:** Receiver-side panic, receiver task cancellation, premature shutdown dropping the receiver half.

**User Impact:** An operator watching task output via `StreamTaskOutput` or `AttachRun` will see the stream go silent with no indication that output is being lost. The daemon continues running normally but output never surfaces.

**Recommendation:** On first send failure, log a `tracing::warn!` once (per agent, using a flag) indicating that the output sink receiver is closed for agent `X`. Do not log on every subsequent failure to avoid log spam.

> DEVELOPER

## ISSUE 1: Silent Drops of Runtime Kill Results During Spawn Rollback

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/task_manager.rs`, lines 248-290

**Severity:** CRITICAL

**Issue Description:** When `spawn_prepared` fails to transition a successfully-spawned task to `Running`, or fails to persist the agent instance row, the cleanup code uses `let _ =` to silently discard errors from `self.runtime.kill(&handle)` and `self.transition_task(...)`. There are three instances:

```rust
// Line 250
let _ = self.runtime.kill(&handle).await;

// Line 271
let _ = self.runtime.kill(&handle).await;

// Lines 276-278
let _ = self
    .transition_task(&prepared.run_id, &prepared.task_id, failed)
    .await;
```

**Hidden Errors:** If `runtime.kill()` fails (e.g., the bwrap PID is in an unkillable state, Docker daemon is unreachable, SIGTERM delivery fails), the process/container is **leaked** -- it runs indefinitely with no one tracking it. If `transition_task` fails on line 276, the task is left in an inconsistent state in the database (marked `Running` but the agent was killed).

**User Impact:** Zombie agent processes accumulate silently. The daemon believes the spawn failed and returns an error, but the agent continues running and consuming resources. On next recovery pass, the orphaned agent will not match any tracked state.

**Recommendation:** At minimum, log the kill failure at `tracing::error!` level with the agent ID, PID/container ID, and original error. The […]

> DEVELOPER

# Error Handling Audit: `f945716` ("feat(runtime): add backend execution and task dispatch")

## Executive Summary

This commit adds approximately 5,500 lines across 28 files implementing runtime backend execution (bwrap, Docker, host), task lifecycle management, and profile compilation. The error handling is **substantially above average** for Rust code -- the author uses `anyhow::Context` pervasively, returns `Result<T>` from public functions, and employs `bail!` for explicit validation failures. However, I found **10 issues** ranging from critical silent failures to medium-severity gaps.

> DEVELOPER

**1. PID cast overflow: `pid as i32` can silently wrap**

- **Files**: `bwrap.rs` lines 365, 379; `host.rs` lines 202, 216
- **Severity**: HIGH
- **Description**: `libc::kill()` takes a `pid_t` (i32), but the PID comes from `child.id()` which returns `u32`. The cast `pid as i32` will silently wrap PIDs > 2,147,483,647 to negative values. On Linux, negative PIDs to `kill()` are interpreted as process group IDs, which means `send_signal` could kill an unrelated process group.
- **Why it matters**: Although PIDs this large are rare on standard Linux, on systems with PID namespace recycling or large `pid_max`, a wrap would send SIGTERM/SIGKILL to the wrong process group. This is a security-relevant misuse of a low-level unsafe API. The fix is `i32::try_from(pid).context("pid overflow")`.

> DEVELOPER

## Critical Review: f945716 -- "feat(runtime): add backend execution and task dispatch"

### FINDINGS

> DEVELOPER

**Ruling: CONDITIONAL — fix U1, U2, and U3 before merge. All other findings are tracked for fast follow-up.**</result>
<usage><total_tokens>11528</total_tokens><tool_uses>0</tool_uses><duration_ms>45298</duration_ms></usage>
</task-notification>
Full transcript available at: /private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/aa348dd4d26461e50.output

> DEVELOPER

## 5. Recommended Fast Follow-Up (SHOULD FIX, next PR)

Items U4 through U12 should be addressed in an immediate follow-up PR, ideally before the next feature lands on this subsystem. In particular:

- U4 (spawn rollback logging), U5 (stuck tasks on spawn failure), and U10 (hardcoded skip-permissions) carry the highest urgency in this tier.
- U12 (unsound `set_var` in tests) will become a compile error or UB; fix preemptively.

> DEVELOPER

## 4. Required Action Items (Must Fix Before Merge)

These three items block merge:

1. **Fix PID truncation (U1):** Replace `pid as i32` with a checked conversion (`i32::try_from(pid)`) that returns an error if the PID exceeds `i32::MAX`. Apply in both `bwrap.rs` and `host.rs` wherever PIDs are cast for signal delivery.

2. **Sanitize host runtime environment (U2):** The host backend must NOT inherit the daemon's full environment. Construct a minimal, explicit allowlist of environment variables for agent processes (PATH, HOME, LANG, and explicitly configured task variables). Strip everything else.

3. **Remove completed/killed entries from `processes` HashMap (U3):** Add cleanup logic that removes TrackedChild entries from the `processes` map when a process exits (in `check_status`) or is killed (in `kill`). Apply in both `bwrap.rs` and `host.rs`.

> DEVELOPER

## 3. Final Verdict: **CONDITIONAL**

This commit introduces substantial, architecturally sound infrastructure, but it has three issues that present real security or correctness risks in production and must be fixed before merge.

> DEVELOPER

## 2. Arbitration: Spawn Rollback Severity

The Silent Failure Hunter rated the `let _ =` in spawn rollback as **CRITICAL**. I downgrade this to **HIGH / SHOULD FIX** for the following reasons:

- The spawn rollback path only fires when a spawn fails partway through — this is already an error path, not the happy path.
- The leaked process count is bounded by the number of concurrent spawn failures, not by total tasks.
- The daemon's lifecycle reaping and OS process cleanup provide a backstop.
- However, silently ignoring kill failures in rollback is a real code smell that should be fixed promptly — hence HIGH, not MEDIUM.

This is classified as SHOULD FIX: it must be addressed in a fast follow-up PR but does not block this merge.

> DEVELOPER

## Summary Table

| Finding | Claimed Severity | Verdict | Adjusted Severity |
|---------|-----------------|---------|-------------------|
| A: PID cast overflow | HIGH | **CONFIRMED** | HIGH (accurate) |
| B: Host env inheritance | HIGH | **CONFIRMED** | HIGH (accurate, mitigated by dev-mode framing) |
| C: Unbounded `processes` map | HIGH | **CONFIRMED** | HIGH (accurate) |
| D: Silent `let _ =` on rollback kill | CRITICAL | **PARTIALLY CONFIRMED** | HIGH (kill_on_drop mitigates process leak) |
| E: Silent channel send drop | HIGH | **PARTIALLY CONFIRMED** | MEDIUM (intentional fire-and-forget telemetry) |
| F: Spawn failures swallowed | HIGH | **PARTIALLY CONFIRMED** | MEDIUM (spawn_prepared handles its own cleanup) |
| G: force_stop == graceful_stop | MEDIUM | **CONFIRMED** | MEDIUM (accurate, kill() does escalate internally) |
| H: Unknown treated as Running | MEDIUM | **CONFIRMED** | MEDIUM (accurate) |
| I: --dangerously-skip-permissions | MEDIUM | **CONFIRMED** | MEDIUM (accurate, necessary for autonomous agents) |
| J: check/kill race | MEDIUM | **PARTIALLY CONFIRMED** | LOW (RwLock + Mutex provide sufficient serialization) |

**Real issues requiring fixes (in priority order)**:
1. **Finding A** -- trivial fix: use `i32::try_from(pid)` with error propagation in both `send_signal` and […]

> DEVELOPER

## Finding J: Race between `check_agent_status` and `kill_agent`

**Verdict: PARTIALLY CONFIRMED -- Severity overstated (LOW, not MEDIUM)**

At `task_manager.rs:327-401` (`check_agent_status`) and `415-436` (`kill_agent`), both methods call `self.tracker.remove(task_id)`. The `AgentTracker` uses a `RwLock<HashMap<...>>`:

```rust
pub async fn remove(&self, task_id: &TaskNodeId) -> Option<AgentInstance> {
    self.agents.write().await.remove(task_id)
}
```

The claim is that both methods call `remove()` without mutual exclusion. However, the `RwLock` on the `HashMap` does provide mutual exclusion for the `remove()` call itself -- two concurrent `remove()` calls will serialize at the write lock, and the second one will see `None` (key already removed).

Both methods handle the `None` case from `remove()`:
- `check_agent_status` (lines 343, 372, 384): `let Some(removed) = self.tracker.remove(task_id).await else { return Ok(Some(status)); }` -- returns early with the status, just skips the state transition.
- `kill_agent` (line 428): `let removed = self.tracker.remove(task_id).await;` -- continues, and conditionally persists only if `removed.is_some()` (line 432).

The real race window is between `tracker.get()` and `tracker.remove()` -- a task could be removed between the get and the remove. But the consequence is benign: the state transitions are idempotent-ish (transitioning an already-completed task would error, but that error propagates correctly).

The more concerning race is that `kill_agent` calls `self.runtime.kill()` before `tracker.remove()`, while `check_agent_status` calls […]

> DEVELOPER

## Finding I: `--dangerously-skip-permissions` hardcoded

**Verdict: CONFIRMED -- Severity accurate (MEDIUM)**

At `task_manager.rs:647-655`:

```rust
fn default_agent_args() -> Vec<String> {
    vec![
        "--dangerously-skip-permissions".to_string(),
        "--print".to_string(),
        "--output-format".to_string(),
        "stream-json".to_string(),
        "--verbose".to_string(),
    ]
}
```

This is used by `build_launch_spec` (line 631) which is called by `prepare_enqueued_launch` (line 453). All agents dispatched through the queue get `--dangerously-skip-permissions`.

**Mitigating factors**: 
1. This is for invoking `claude` CLI (the AI agent binary), not arbitrary programs. The flag relates to Claude's internal permission model for tool use.
2. In bwrap mode, the agent runs inside a sandbox with namespace isolation, PID isolation, and read-only bind mounts. The `--dangerously-skip-permissions` flag is for the AI agent's internal prompting behavior, while the bwrap sandbox provides the actual security boundary.
3. The agents are autonomous workers executing pre-defined tasks -- they need to operate without interactive permission prompts.

**Assessment**: MEDIUM is accurate. In host mode, this does remove a security barrier. In bwrap/Docker modes, the runtime sandbox provides the real security boundary. The flag name sounds alarming but is about skipping interactive permission prompts in the Claude CLI, which is necessary for autonomous execution. Still, it should ideally be configurable per-backend.

> DEVELOPER

## Finding H: `AgentStatus::Unknown` treated same as `Running`

**Verdict: CONFIRMED -- Severity accurate (MEDIUM)**

At `task_manager.rs:341`:

```rust
match &status {
    AgentStatus::Initializing | AgentStatus::Running | AgentStatus::Unknown => Ok(None),
```

When `status()` returns `Unknown`, `check_agent_status` treats it identically to `Running` -- returning `Ok(None)` which means "no terminal status detected, keep polling."

Looking at when `Unknown` is returned (e.g., `host.rs:193-197`):

```rust
if process_exists(pid) {
    Ok(AgentStatus::Running)
} else {
    Ok(AgentStatus::Unknown)
}
```

This fallback path is reached only when `self.tracked_child()` returns `None` (no entry in the `processes` map) AND the PID no longer exists. This indicates the process has exited but we lost the tracking data. Returning `Unknown` here and then treating it as "keep polling" means `check_agent_status` will keep returning `Ok(None)` forever for this task, since the process is gone and the tracked child is gone.

However, there is a mitigating factor: for this to happen, the `processes` map entry must have been lost (which doesn't happen in normal operation -- entries are never removed, per Finding C). After a daemon restart, the tracker is empty and the stale handle would hit this path.

**Assessment**: MEDIUM is accurate. Tasks with `Unknown` status will indeed hang indefinitely in the polling loop. The daemon restart […]

> DEVELOPER

## Finding G: `force_stop` delegates to `graceful_stop` with no escalation

**Verdict: CONFIRMED -- Severity accurate (MEDIUM)**

At `task_manager.rs:584-586`:

```rust
async fn force_stop(&self, agent: &ActiveAgent, reason: &str) -> Result<()> {
    self.graceful_stop(agent, reason).await
}
```

This is indeed a direct delegation with no escalation. Looking at how it is used in `shutdown.rs:152-156`:

```rust
for agent in &force_candidates {
    self.agent_supervisor
        .force_stop(agent, "daemon_shutdown_force")
        .await
```

The shutdown coordinator calls `graceful_stop` first, waits for the grace period, then calls `force_stop` on remaining agents. Since `force_stop` just calls `graceful_stop` again, it resends SIGTERM (which the process may have already ignored) and waits 2 seconds for exit before calling `force_kill` (SIGKILL). So there IS escalation to SIGKILL -- it just happens inside `kill()` at `host.rs:162-171`:

```rust
Err(_) => {
    child.force_kill().await...
```

The `kill()` method sends SIGTERM, waits 2 seconds, then SIGKILL. So the first graceful_stop sends SIGTERM+wait+SIGKILL, and if the agent survives that (unlikely but possible if tracked_child is `None`), force_stop does exactly the same thing.

**Assessment**: MEDIUM is accurate. The naming is misleading and there is no differentiated behavior, but the underlying `kill()` method does escalate to SIGKILL. The issue is more about API contract violation than practical risk.

> DEVELOPER

## Finding F: `dispatch_enqueued_tasks` swallows spawn failures

**Verdict: PARTIALLY CONFIRMED -- Severity overstated (MEDIUM, not HIGH)**

At `task_manager.rs:220-230`:

```rust
match self.spawn_prepared(prepared).await {
    Ok(_) => launched.push(task_id),
    Err(error) => {
        tracing::warn!(
            %error,
            run_id = %run_id,
            task_id = %task_id,
            "failed to dispatch enqueued task"
        );
    }
}
```

The finding claims tasks could get stuck in non-terminal states. However, looking at `spawn_prepared()` (lines 237-324), when the runtime spawn itself fails (lines 249-270), the method transitions the task to `TaskStatus::Failed` before returning the error:

```rust
Err(error) => {
    let failure_status = TaskStatus::Failed {
        error: error.to_string(),
        duration: Utc::now() - materialized_at,
    };
    self.transition_task(&prepared.run_id, &prepared.task_id, failure_status)
        .await
        ...
}
```

So the task is moved to `Failed` inside `spawn_prepared` before the error propagates to `dispatch_enqueued_tasks`. The task does NOT get stuck.

The only way a task could get stuck is if `prepare_enqueued_launch` succeeds, `spawn_prepared` is called, and `spawn_prepared`'s internal state transition to `Materializing` succeeds, but then the transition to `Failed` also fails (both DB writes failing). That's an extremely unlikely double-failure scenario.

For preparation failures (lines 207-217), the code explicitly calls `self.fail_preparation(...)` which transitions to `Failed`.

**Assessment**: MEDIUM at most. The code already handles the common failure paths correctly by transitioning tasks to Failed. The warn-and-continue pattern […]

> DEVELOPER

## Finding E: Silent drop of channel send in RuntimeOutputSink

**Verdict: PARTIALLY CONFIRMED -- Severity overstated (MEDIUM, not HIGH)**

At `io.rs:46-50`:

```rust
fn emit(&self, envelope: RuntimeOutputEnvelope) {
    if let Some(tx) = &self.tx {
        let _ = tx.send(envelope);
    }
}
```

The `let _ = tx.send(envelope)` does silently discard output when the receiver is dropped. However, several mitigating factors reduce the severity:

1. This is an `mpsc::UnboundedSender` -- it only fails when the receiver is dropped, which normally only happens during shutdown.
2. The `RuntimeOutputSink` has a `disabled()` constructor that explicitly creates a `None` sender, showing that output loss is an expected/designed operational mode.
3. Output here is telemetry (stdout/stderr lines, token usage), not critical state transitions. Task state transitions go through the `RunOrchestrator` directly.
4. During shutdown, the daemon is tearing down anyway -- losing output at that point is acceptable.

If the receiver drops unexpectedly during normal operation (a bug), then yes, all subsequent output is silently lost. But this would indicate a larger architectural failure.

**Assessment**: MEDIUM is the right severity. The `let _ =` is intentional design for a fire-and-forget telemetry channel. Logging a warning on the first failure would be a reasonable improvement, but HIGH overstates […]

> DEVELOPER

## Finding D: Silent `let _ =` on kill during spawn rollback

**Verdict: PARTIALLY CONFIRMED -- Severity overstated (HIGH, not CRITICAL)**

At `task_manager.rs:279-290`:

```rust
if let Err(error) = self
    .transition_task(&prepared.run_id, &prepared.task_id, running_status)
    .await
{
    let _ = self.runtime.kill(&handle).await;
    return Err(error).with_context(|| { ... });
}
```

And at `task_manager.rs:303-317`:

```rust
if let Err(error) = self.persist_spawned_agent(agent_row).await {
    let _ = self.runtime.kill(&handle).await;
    let failed = TaskStatus::Failed { ... };
    let _ = self
        .transition_task(&prepared.run_id, &prepared.task_id, failed)
        .await;
    return Err(error).with_context(|| { ... });
}
```

The `let _ =` on `kill()` is real. If the kill fails, the process is leaked. However, the reviewers claimed CRITICAL severity. The context matters: these are rollback paths for rare failure modes (state transition or persistence failure after a successful spawn). The function already returns an error to the caller, indicating the spawn failed. The process also has `kill_on_drop(true)` set (both `bwrap.rs:215` and `host.rs:80`), so when all `Arc<TrackedChild>` references are eventually dropped, tokio will attempt to kill the child.

The `let _ =` on `transition_task` in the second block (line 309-311) is more concerning -- if both the agent persistence and the task failure transition fail, the task could remain in `Running` state in the orchestrator with no […]

> DEVELOPER

## Finding C: Unbounded growth in `processes` HashMap (memory leak)

**Verdict: CONFIRMED -- Severity accurate (HIGH)**

In both `bwrap.rs:257-260` and `host.rs:131-134`, the spawn method inserts into `self.processes`:

```rust
self.processes
    .write()
    .await
    .insert(prepared.agent_id.clone(), tracked_child);
```

But neither `kill()` nor `status()` ever calls `self.processes.write().await.remove(...)`. The `kill()` method (e.g., `host.rs:145-174`) calls `self.tracked_child()` which does a read-only `get().cloned()`, performs the kill, but never removes the entry. Similarly, `status()` only reads.

The `TaskManager.check_agent_status()` calls `self.tracker.remove()` to remove from the `AgentTracker` -- but that is a separate data structure from the runtime's `processes` HashMap. The runtime-level `processes` map is never cleaned up.

Over a long-running daemon lifetime, each spawned agent leaves a `TrackedChild` (containing a `Mutex<Child>` and kill reason) permanently in the map. While each entry is relatively small (the child process has already exited), this is an unbounded leak.

**Assessment**: HIGH is appropriate. Over a daemon lifetime with many task dispatches, this will grow without bound. Each `TrackedChild` holds a `Mutex<Child>` wrapping tokio's `Child` struct plus the kill reason string.

> DEVELOPER

## Finding B: Host runtime inherits full parent environment

**Verdict: CONFIRMED -- Severity accurate (HIGH)**

At `host.rs:76-97`:

```rust
let mut command = Command::new(&prepared.launch.program);
command
    .args(&prepared.launch.args)
    .current_dir(&prepared.workspace)
    .kill_on_drop(true)
    .stdout(Stdio::piped())
    .stderr(Stdio::piped());
// ...
for (key, value) in &prepared.launch.env {
    command.env(key, value);
}
command.env("FORGE_AGENT_ID", prepared.agent_id.as_str());
```

`Command::new()` inherits the parent process environment by default. The code uses `.env()` to add environment variables on top but never calls `.env_clear()` first. This means every agent launched in host mode inherits the daemon's full environment, including any secrets (API keys, tokens, credentials) present in the daemon process.

**Mitigating factor**: The file header says "This backend exists as the explicit development fallback" and the spawn method guards on `RuntimeEnvPlan::Host { explicit_opt_in: true }`. This is explicitly an insecure dev-mode backend. Contrast with `bwrap.rs` which uses `--clearenv` (line 108) to sanitize the environment.

**Assessment**: HIGH is accurate for the host backend taken on its own. The explicit opt-in guard and the "insecure" naming do provide some mitigation, but the lack of `env_clear()` means any secret in the daemon environment leaks to agents. Could be argued as MEDIUM given the explicit dev-mode framing, but HIGH is defensible.

> DEVELOPER

# Validation Report: Commit f945716

## Finding A: PID cast overflow -- `pid as i32` can silently wrap

**Verdict: CONFIRMED -- Severity accurate (HIGH)**

The code at `bwrap.rs:365` and `host.rs:202` is identical:

```rust
fn send_signal(pid: u32, signal: i32) -> Result<()> {
    let rc = unsafe { libc::kill(pid as i32, signal) };
```

And at `bwrap.rs:379` / `host.rs:216`:

```rust
fn process_exists(pid: u32) -> bool {
    let rc = unsafe { libc::kill(pid as i32, 0) };
```

The `pid` parameter is `u32`, and `libc::kill` takes `libc::pid_t` which is `i32`. If a PID exceeds `i32::MAX` (2,147,483,647), the cast `pid as i32` wraps to a negative value. Passing a negative PID to `kill()` sends the signal to all processes in the process group whose PGID equals the absolute value of that number. This is a real correctness/safety bug.

**Mitigating factor**: On Linux, the default `pid_max` is 32,768 (maximum configurable is 4,194,304 on 64-bit), so PIDs above `i32::MAX` are effectively impossible in practice. On macOS, PIDs are also well within `i32` range. The severity is technically HIGH from a correctness standpoint (undefined behavior potential in unsafe code), but practically exploitable only on exotic configurations. A `TryFrom<u32>` conversion with an error return would be the correct […]

> DEVELOPER

### Summary Verdict: **CONDITIONAL**

Fix before merge:

1. **Finding 1 (HIGH):** Replace the unbounded channel with a bounded channel or add a queue-depth guard. At minimum, add monitoring/logging when the queue depth exceeds a threshold.

2. **Finding 2 (HIGH):** Batch the SQLite writes — acquire the orchestrator lock once per drain cycle and write all envelopes in a single transaction, or move persistence to a dedicated writer task.

3. **Finding 3+7 (MEDIUM):** The `yield_now` approach for final-output capture is unreliable. Either track the I/O task JoinHandles in `TrackedChild` and await them before finalizing, or introduce a completion signal the emitter sends when the pipe is drained.

4. **Finding 4 (MEDIUM):** Decide whether `SessionCaptured`, `FinalPayload`, `AssistantText`, and `Thinking` events should be forwarded through the runtime output path. If intentionally dropped, document this. If not, this is a regression that needs fixing.

Items 5, 6, 8, and 9 are worth addressing but not merge-blockers.</result>
<usage><total_tokens>81451</total_tokens><tool_uses>23</tool_uses><duration_ms>165761</duration_ms></usage>
</task-notification>
Full transcript available at: /private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/a0ab3385e24a58439.output

> DEVELOPER

### Finding 9 — `emit_chunk_lines` Allocates a String Per Chunk via `from_utf8_lossy`

**File:** `crates/forge-runtime/src/runtime/io.rs` lines 312-325  
**Severity:** LOW (performance)

`String::from_utf8_lossy(chunk)` creates a `Cow<str>` which is then pushed into the buffer string. For non-UTF8 data (which shouldn't happen with JSON but could happen with binary stdout), this will silently replace bytes with the Unicode replacement character, potentially corrupting JSON parsing downstream. More critically, this allocates on every chunk regardless.

**Why it matters:** Could cause garbled JSON if the Docker mux stream splits a multi-byte UTF-8 character across chunks, leading to replacement characters mid-JSON that would cause parse failures.

> DEVELOPER

### Finding 8 — Spawned I/O Tasks Have No Cancellation or Tracking

**File:** `crates/forge-runtime/src/runtime/io.rs` lines 116-121, 273-288, 291-309, 188-234  
**Severity:** MEDIUM

All spawned I/O drain tasks (`spawn_stdout_task`, `spawn_stderr_task`, `spawn_docker_attach_task`) return no `JoinHandle`. They are fire-and-forget. If the daemon needs to shut down gracefully, there is no way to:

1. Wait for these tasks to complete (to ensure all output is flushed).
2. Cancel them (to avoid keeping zombie tasks alive).
3. Know if they have panicked.

The `TrackedChild` struct stores the `Child` but not the I/O task handles. On shutdown, the child process is killed, but the I/O tasks may still be reading from closed pipes and emitting into the now-drained channel.

**Why it matters:** During daemon shutdown, final output events may be lost because the I/O tasks are not awaited. In pathological cases, panics in spawned tasks will be silently swallowed.

> DEVELOPER

### Finding 7 — `yield_now` Is Not a Reliable Synchronization Primitive

**File:** `crates/forge-runtime/src/task_manager.rs` line 344  
**Severity:** MEDIUM

`tokio::task::yield_now().await` is used to give the I/O drain tasks a chance to push their final data. This is not a reliable mechanism. Depending on the tokio runtime's task scheduling, the drain tasks may not get scheduled before the current task resumes. On a single-threaded runtime or under load, this yield may do nothing useful.

**Why it matters:** This is part of Finding 3 but worth calling out separately as an architectural concern. The correct solution would be to join the I/O task handles or use a completion signal.

> DEVELOPER

### Finding 6 — Docker: `has_stdin.then_some(input)` May Leak the Write Half

**File:** `crates/forge-runtime/src/runtime/docker.rs` lines 297-330 and `io.rs` lines 176-235  
**Severity:** MEDIUM

When `has_stdin` is false, the attach call still requests `stdout(true)` and `stderr(true)` but now always returns an `input` write half. The code passes `has_stdin.then_some(input)` which drops the `input` when there's no stdin. However, within `spawn_docker_attach_task`, when `input` is `None`, there is no explicit shutdown of the write half — it is simply not opened. This is acceptable **but** in the previous code, attach was only called when there was stdin payload. Now attach is always called (even when `has_stdin` is false), which is a behavior change. If the container's process is waiting for stdin EOF and never gets it (because we're not shutting down the write half of the attach stream), it may hang.

Wait, re-reading: when `has_stdin` is false, `attach_stdin` is `Some(false)`, so the Docker API should not open a stdin stream. But `has_stdin.then_some(input)` discards the write half returned by bollard without shutting it down. The bollard `input` is returned regardless of the attach options. Dropping without shutdown may leave Docker daemon resources in limbo.

**Why it matters:** Could cause container hangs if the Docker API still provides […]

> DEVELOPER

### Finding 5 — TokenUsage Always Sets `tokens == cumulative` (Never Incremental)

**File:** `crates/forge-common/src/output_parser.rs` lines 55-58  
**Severity:** MEDIUM

```rust
events.push(ParsedOutputEvent::TaskOutput(TaskOutput::TokenUsage {
    tokens: cumulative,
    cumulative,
}));
```

The `TokenUsage` struct has two fields: `tokens` (incremental for this event) and `cumulative`. Both are set to the same value, meaning the `tokens` field is meaningless — it just duplicates `cumulative`. The old code in `direct_execution.rs` had the same behavior, so this is not a regression, but the extraction to a shared parser is a good time to note this is misleading: any consumer trying to compute per-event incremental usage from `tokens` will get incorrect data.

**Why it matters:** Downstream token budgeting or cost tracking that relies on the `tokens` field being incremental will be incorrect.

> DEVELOPER

### Finding 4 — RuntimeOutputEmitter Silently Drops Non-TaskOutput Events

**File:** `crates/forge-runtime/src/runtime/io.rs` lines 82-88  
**Severity:** MEDIUM

`emit_stdout_line` calls `parse_output_line` which can produce `AssistantText`, `Thinking`, `ToolCall`, `SessionCaptured`, and `FinalPayload` events. However, the `if let ParsedOutputEvent::TaskOutput(output) = event` guard silently discards all of these. This means:

- Session IDs captured by the parser are thrown away (the session ID is never forwarded to the runtime event system).
- `FinalPayload` events that were previously persisted in `direct_execution.rs` are now silently dropped in the runtime path.
- `AssistantText` events that were previously emitted as `ExecutionEvent::AssistantText` are lost.

This is a behavioral regression vs. the `direct_execution.rs` path that still emits all event types via `emit_parsed_events`.

**Why it matters:** Any consumer that depends on `SessionCaptured` or `FinalPayload` events from runtime-managed agents will not receive them. The runtime path loses significant observability data that the direct execution path retains.

> DEVELOPER

### Finding 3 — Race: Output Events Lost Between Process Exit and Drain

**File:** `crates/forge-runtime/src/task_manager.rs` lines 340-346  
**Severity:** MEDIUM

When `check_agent_status` detects a terminal state, it does `tokio::task::yield_now().await` then `drain_runtime_output()` to capture final output. However, `yield_now` only yields once to the executor; there is no guarantee the I/O drain tasks (which are separate spawned tasks reading stdout/stderr line-by-line) have completed and pushed all their final lines into the channel. The process may have exited, but the stdout pipe's BufReader may still have data in its kernel buffer or BufReader internal buffer that hasn't been read and emitted yet.

For Docker containers, `spawn_docker_attach_task` runs `flush_partial_line` only after the stream terminates, but the stream termination is asynchronous and may not have completed by the time `yield_now` returns.

**Why it matters:** The final token usage or PromiseDone signal may arrive after the drain, meaning `tokens_consumed` in the completed task could be zero or stale, and the PromiseDone signal may not be persisted as a runtime event before task completion is recorded. The test uses `sleep(150ms)` to paper over this, but there is no reliable synchronization in production.

> DEVELOPER

### Finding 2 — Orchestrator Lock Held Per-Envelope During Drain

**File:** `crates/forge-runtime/src/task_manager.rs` lines 174-193 (drain_runtime_output) and 494-513 (append_task_output_event)  
**Severity:** HIGH

`drain_runtime_output` collects all pending envelopes, then for **each envelope** calls `append_task_output_event`, which acquires the orchestrator `Mutex` lock, calls `record_runtime_event_for_agent` (which does a `spawn_blocking` SQLite write), and releases. This means the orchestrator lock is acquired and released N times per drain cycle, and during each acquisition, it blocks all gRPC handlers and the dispatch/poll loops that also need the orchestrator.

Additionally, inside `record_runtime_event_for_agent`, a `spawn_blocking` is awaited while the orchestrator lock is held. The blocking threadpool is shared with all other `spawn_blocking` calls. If the blocking pool is saturated, this will stall the orchestrator lock for an extended period, blocking all concurrent operations on the daemon.

**Why it matters:** With a burst of 500 envelopes, the drain loop will acquire the orchestrator mutex 500 times, each time doing a synchronous SQLite write via spawn_blocking. This serializes the entire daemon for the duration. gRPC clients will see increased latency or timeouts.

> DEVELOPER

## Critical Review: `feat(runtime): stream live task output events` (3509c34)

### Finding 1 — Unbounded Channel as Back-Pressure-Free Output Queue

**File:** `crates/forge-runtime/src/runtime/io.rs` lines 31-51  
**Severity:** HIGH

`RuntimeOutputSink` uses `mpsc::unbounded_channel()`. Every stdout and stderr line from every running agent is pushed into this single channel. The channel is only drained by the ticker loop in `main.rs` every 250ms. A fast-producing agent (or multiple concurrent agents) can accumulate millions of envelopes in memory before the drain cycle fires. There is no backpressure: the `emit` method ignores the send result (`let _ = tx.send(...)`), and there is no cap on queue depth.

**Why it matters:** A chatty agent that emits thousands of lines per second will cause unbounded heap growth. Over the 250ms tick interval, a single agent writing at 10K lines/second produces 2,500 envelopes with cloned `RunId`, `TaskNodeId`, `AgentId`, `TaskOutput`, and `DateTime` per interval. Multiple agents compound this. Under sustained load this is a denial-of-service vector against the daemon itself.

> DEVELOPER

## Summary of Findings

| # | Severity | File | Issue |
|---|----------|------|-------|
| 1 | CRITICAL | `io.rs:48` | `let _ = tx.send()` silently drops all output events when receiver is gone |
| 2 | HIGH | `output_parser.rs:36-38` | JSON parse failure silently demotes to raw text, error discarded |
| 3 | HIGH | `io.rs:269-309` | Spawned I/O tasks discard JoinHandle, panics silently swallowed |
| 4 | HIGH | `task_manager.rs:220-230` | Failed spawns only logged, task may enter zombie state |
| 5 | MEDIUM | `task_manager.rs:283,304` | Kill errors discarded, agents may run orphaned |
| 6 | HIGH | `io.rs:82-88` | `emit_stdout_line` silently drops AssistantText, Thinking, ToolCall, FinalPayload events |
| 7 | MEDIUM | `io.rs:313` | `from_utf8_lossy` silently corrupts binary data |
| 8 | MEDIUM | `output_parser.rs:79,113` | Unrecognized event types silently dropped |
| 9 | MEDIUM | `io.rs:158,165` | `expect()` on mutex will panic on poisoning |
| 10 | MEDIUM | `task_manager.rs:309-311` | `let _ =` discards transition-to-Failed error |
| 11 | MEDIUM | `io.rs:116-121` | Missing stdout/stderr pipes are not reported |

Issues 1, 3, 4, and 6 are the most impactful: they represent paths where […]

> DEVELOPER

## Positive Observations

Several patterns in this commit deserve acknowledgment:

1. **Consistent `.context()` usage in `task_manager.rs`**: Nearly every `Result` propagation includes actionable context with the task ID and operation name. This is excellent and will make debugging straightforward.

2. **Error propagation through `anyhow::Result`**: The Rust type system ensures most errors cannot be silently ignored. The `?` operator and `.with_context()` chains are well-used throughout `bwrap.rs`, `docker.rs`, and `host.rs`.

3. **`DirectExecutionFacade` refactoring**: The refactoring to use the shared `output_parser` maintains the existing error handling discipline from the original code, including the `collect_reader_result` pattern that surfaces join errors.

4. **Runtime selection fail-closed policy**: `select_runtime` in `mod.rs` correctly refuses to proceed without an explicit opt-in for insecure modes, with clear error messages explaining what the operator must do.

5. **Lifecycle ticker error handling in `main.rs`**: Lines 142-149 log each lifecycle failure at `warn` level and continue the loop, which is appropriate for a polling-based daemon.

> DEVELOPER

## Issue 11: `TrackedChild` stdout/stderr pipes silently detach on `take()`

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/io.rs`, lines 116-121

**Severity:** MEDIUM

```rust
if let Some(stdout) = child.stdout.take() {
    spawn_stdout_task(stdout, emitter.clone());
}
if let Some(stderr) = child.stderr.take() {
    spawn_stderr_task(stderr, emitter.clone());
}
```

If `child.stdout` or `child.stderr` is `None` (which should not happen since `Stdio::piped()` was set, but could happen due to OS-level issues or race conditions), the code silently proceeds without capturing that stream. There is no log, no warning, no error. The agent's output would be completely lost with no indication.

**Hidden Errors:** OS resource exhaustion, pipe creation failure, race with process exit.

**User Impact:** Agent runs but produces no visible output. Indistinguishable from an agent that simply produced no output.

**Recommendation:** Log when pipes are unexpectedly absent:

```rust
if let Some(stdout) = child.stdout.take() {
    spawn_stdout_task(stdout, emitter.clone());
} else {
    tracing::warn!("child process stdout pipe was not available -- output will not be captured");
}
```

> DEVELOPER

## Issue 10: `let _ = self.transition_task(...)` discards state persistence error

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/task_manager.rs`, lines 309-311

**Severity:** MEDIUM

```rust
let _ = self
    .transition_task(&prepared.run_id, &prepared.task_id, failed)
    .await;
```

When `persist_spawned_agent` fails, the code tries to transition the task to `Failed` but discards the result of that transition. If the transition also fails (e.g., the state store is down), the task may be stuck in `Running` with a killed agent.

**Hidden Errors:** Database unavailable, disk full, concurrent state modifications.

**User Impact:** Task appears as `Running` in the UI but has no actual agent. Same zombie-task scenario as Issue 4.

**Recommendation:** Log the transition failure:

```rust
if let Err(transition_error) = self
    .transition_task(&prepared.run_id, &prepared.task_id, failed)
    .await
{
    tracing::error!(
        %transition_error,
        task_id = %prepared.task_id,
        "failed to transition task to Failed after agent persistence failure"
    );
}
```

> DEVELOPER

## Issue 9: `kill_reason` mutex uses `expect` -- will panic on poisoning

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/io.rs`, lines 158 and 165

**Severity:** MEDIUM

```rust
pub fn remember_kill_reason(&self, reason: impl Into<String>) {
    let mut kill_reason = self.kill_reason.lock().expect("kill reason mutex poisoned");
    *kill_reason = Some(reason.into());
}

pub fn kill_reason(&self) -> Option<String> {
    self.kill_reason
        .lock()
        .expect("kill reason mutex poisoned")
        .clone()
}
```

Using `.expect()` on a `StdMutex::lock()` means the daemon will panic if another thread panicked while holding this lock. In a long-running daemon, a panic in the kill path would take down the entire process.

**Hidden Errors:** A panic anywhere that holds the `kill_reason` lock (even momentarily) poisons the mutex and causes all subsequent callers to panic.

**User Impact:** Daemon crash, all running agents orphaned.

**Recommendation:** Use `.lock().unwrap_or_else(|poisoned| poisoned.into_inner())` to recover from poisoning, or switch to `parking_lot::Mutex` which does not have poisoning semantics.

> DEVELOPER

## Issue 8: Unrecognized JSON event types are silently ignored

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-common/src/output_parser.rs`, line 79

**Severity:** MEDIUM

```rust
match event_type {
    "assistant" => emit_assistant_events(&mut events, json),
    "content_block_delta" => emit_delta_events(&mut events, json),
    "result" | "response.completed" => {
        // ...
    }
    _ => {}
}
```

The catch-all `_ => {}` silently ignores any unrecognized event type. When the upstream Claude API adds new event types (which it does regularly), or when there is a protocol mismatch, these events vanish without a trace. No log, no metric, no indication that the parser encountered something unexpected.

Similarly, on line 113: `_ => {}` in `emit_assistant_events` silently drops unrecognized content block types.

**Hidden Errors:** New API event types, protocol version mismatches, corrupted type fields.

**User Impact:** New capabilities from the underlying agent are invisible to the runtime. Debugging protocol issues becomes harder because there is no evidence of what was received.

**Recommendation:** Add `tracing::trace!` logging for unrecognized types:

```rust
_ => {
    tracing::trace!(event_type = event_type, "unrecognized stream-json event type");
}
```

> DEVELOPER

## Issue 7: `from_utf8_lossy` silently corrupts binary data in Docker output

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/io.rs`, line 313

**Severity:** MEDIUM

```rust
fn emit_chunk_lines(buffer: &mut String, chunk: &[u8], mut emit: impl FnMut(String)) {
    buffer.push_str(&String::from_utf8_lossy(chunk));
    // ...
}
```

`from_utf8_lossy` replaces invalid UTF-8 sequences with the Unicode replacement character (U+FFFD) without any indication that data was corrupted. If a Docker container produces binary output on stdout (which could happen with non-text tools or corrupted streams), the lossy conversion will silently mangle the data and produce lines containing replacement characters.

Compare this with `DirectExecutionFacade` which uses `BufReader::lines()` which returns a proper I/O error on invalid UTF-8 -- and that error IS surfaced through the `collect_reader_result` mechanism.

**Hidden Errors:** Binary data in stdout, encoding mismatches, multi-byte UTF-8 split across chunk boundaries.

**User Impact:** Agent output is silently corrupted. The user sees replacement characters in the output but has no indication that data was lost.

**Recommendation:** Use `from_utf8` and handle the error explicitly. At minimum, log a warning on the first lossy conversion:

```rust
match std::str::from_utf8(chunk) {
    Ok(valid) => buffer.push_str(valid),
    Err(err) => {
        tracing::warn!("non-UTF-8 bytes in container output at byte offset {}", err.valid_up_to());
        buffer.push_str(&String::from_utf8_lossy(chunk));
    }
}
```

> DEVELOPER

## Issue 6: `emit_stdout_line` silently drops non-TaskOutput parsed events

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/io.rs`, lines 82-88

**Severity:** HIGH

```rust
pub fn emit_stdout_line(&self, state: &mut ParsedOutputState, line: String) {
    for event in parse_output_line(state, self.output_mode, line) {
        if let ParsedOutputEvent::TaskOutput(output) = event {
            self.emit(output);
        }
    }
}
```

This method calls `parse_output_line`, which produces multiple event types: `TaskOutput`, `AssistantText`, `Thinking`, `ToolCall`, `SessionCaptured`, and `FinalPayload`. However, `emit_stdout_line` only emits `TaskOutput` events. All other event types are silently discarded.

Compare with `direct_execution.rs` (`emit_parsed_events`, lines 326-389), which carefully maps every `ParsedOutputEvent` variant to a corresponding `ExecutionEvent`. The runtime pipeline loses:
- `AssistantText` -- the actual text the assistant produced
- `Thinking` -- the thinking/reasoning trace
- `ToolCall` -- tool invocation information
- `SessionCaptured` -- the session ID (though this IS captured via `ParsedOutputState`)
- `FinalPayload` -- the final result payload

This means the runtime streaming pipeline delivers a subset of what `DirectExecutionFacade` delivers. The shared parser was created to unify behavior, but the runtime side only uses part of it.

**User Impact:** Users streaming runtime output see signals, token usage, and promises, but miss assistant text, thinking traces, and tool calls. This is a significant loss of information for monitoring agent behavior.

**Recommendation:** Either extend `RuntimeOutputEnvelope` / `TaskOutput` […]

> DEVELOPER

## Issue 5: `let _ = self.runtime.kill(&handle).await` discards kill errors

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/task_manager.rs`, line 283 and line 304

**Severity:** MEDIUM

```rust
// Line 283
let _ = self.runtime.kill(&handle).await;

// Line 304
let _ = self.runtime.kill(&handle).await;
```

Both of these discard the result of killing a runtime agent. On line 283, if transitioning the task to `Running` fails after a successful spawn, the cleanup kill is fire-and-forget. On line 304, if persisting the agent instance fails, the kill is also fire-and-forget.

If the kill itself fails, you now have a running agent process with no tracking in the `TaskManager`. It will consume resources (and potentially tokens) with no way to stop it.

**Hidden Errors:** Process already exited, permission denied, container not found, network error to Docker daemon.

**User Impact:** An orphaned agent process runs untracked, consuming tokens and compute. The user sees the task as `Failed` but the agent is still running.

**Recommendation:** At minimum, log the kill error:

```rust
if let Err(kill_error) = self.runtime.kill(&handle).await {
    tracing::error!(
        %kill_error,
        agent_id = %handle.agent_id,
        task_id = %prepared.task_id,
        "failed to kill agent during cleanup -- agent may be orphaned"
    );
}
```

> DEVELOPER

## Issue 4: `dispatch_enqueued_tasks` silently skips failed spawns

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/task_manager.rs`, lines 220-230

**Severity:** HIGH

```rust
match self.spawn_prepared(prepared).await {
    Ok(_) => launched.push(task_id),
    Err(error) => {
        tracing::warn!(
            %error,
            run_id = %run_id,
            task_id = %task_id,
            "failed to dispatch enqueued task"
        );
    }
}
```

When a spawn fails after preparation succeeds (lines 220-230), the task is only logged with `warn` and then skipped. The task remains in whatever state `spawn_prepared` left it in. Critically, the task is **not** transitioned to `Failed` in this branch. Look at the flow:

- `prepare_enqueued_launch` succeeds
- `spawn_prepared` is called, which calls `ensure_spawnable_task` (transitions to `Materializing`)
- If `runtime.spawn(prepared)` fails inside `spawn_prepared`, the task IS transitioned to Failed (line 256)
- But if `spawn_prepared` fails at ANY other point (e.g., the transition to `Materializing` fails, or `persist_spawned_agent` fails and the second `transition_task` also fails), the error is returned
- Back in `dispatch_enqueued_tasks`, that error is only logged and the task is stuck

The task could be stuck in `Materializing` or `Running` forever with no agent actually running.

**Hidden Errors:** State store failures, concurrent modification of task state, `transition_task` failures.

**User Impact:** A task silently enters a zombie state -- it appears in-progress but nothing is executing. The user […]

> DEVELOPER

## Issue 3: Spawned I/O tasks silently swallow panics and join errors

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/io.rs`, lines 269-289 (`spawn_stdout_task`) and 291-309 (`spawn_stderr_task`)

**Severity:** HIGH

Both `spawn_stdout_task` and `spawn_stderr_task` call `tokio::spawn()` and discard the `JoinHandle`. If the spawned task panics (e.g., due to a bug in the emitter, or a poisoned mutex), the panic is silently swallowed by Tokio's default task panic handler. The parent code has no way to detect that output capture stopped.

Compare this to the `DirectExecutionFacade` in `direct_execution.rs` which correctly holds the `JoinHandle` and calls `collect_reader_result()` to surface join errors. The runtime side lacks this discipline.

```rust
fn spawn_stdout_task<R>(reader: R, emitter: RuntimeOutputEmitter)
where
    R: AsyncRead + Unpin + Send + 'static,
{
    tokio::spawn(async move {  // JoinHandle is discarded!
        // ...
    });
}
```

**Hidden Errors:** Panics in parsing logic, unexpected emitter state, lock poisoning in `ParsedOutputState`.

**User Impact:** If the stdout reader task panics, the agent's output stream silently ends. The agent continues running and consuming tokens, but the user sees no further output. No error, no warning.

**Recommendation:** Return the `JoinHandle` from both functions and have `TrackedChild` monitor them. At minimum, name the tasks and install a panic hook that logs:

```rust
fn spawn_stdout_task<R>(reader: R, emitter: RuntimeOutputEmitter) […]

> DEVELOPER

## Issue 2: JSON parse failure silently demotes structured events to raw text

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-common/src/output_parser.rs`, lines 36-38

**Severity:** HIGH

```rust
ParsedOutputMode::StreamJson => serde_json::from_str::<Value>(&line)
    .map(|json| parse_stream_json_event(state, &json))
    .unwrap_or_else(|_| vec![ParsedOutputEvent::TaskOutput(TaskOutput::Stdout(line))]),
```

When the output mode is `StreamJson`, any line that fails JSON parsing is silently repackaged as a raw `Stdout` event. The JSON parse error itself (`_`) is thrown away. This is a fallback that masks real problems:

1. If the agent's output format changes or is corrupted, the daemon will happily emit garbage as stdout instead of reporting a parse failure.
2. If there is a framing issue (truncated JSON, partial line reads), the user receives raw JSON fragments instead of structured events, with no indication that something went wrong.
3. The original error (which serde_json would provide with exact position information) is lost.

**Hidden Errors:** Malformed JSON from agent, UTF-8 boundary issues in chunked reads, upstream API format changes.

**User Impact:** The user configured `StreamJson` mode expecting structured output. Instead they receive raw text chunks. They have no way to know that parsing failed -- the daemon gives no signal that it fell back to raw mode.

**Recommendation:** At least log the parse failure at `debug` or `trace` level. For […]

> DEVELOPER

## Issue 1: Silent channel send failure -- events permanently lost

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/io.rs`, line 48

**Severity:** CRITICAL

```rust
fn emit(&self, envelope: RuntimeOutputEnvelope) {
    if let Some(tx) = &self.tx {
        let _ = tx.send(envelope);
    }
}
```

The `let _ = tx.send(envelope)` discards the `Result` returned by `mpsc::UnboundedSender::send()`. If the receiving half of the channel is dropped (e.g., the `TaskManager` is torn down before agents finish, or the receiver lock is poisoned), every subsequent output event -- stdout lines, token usage, progress signals, DONE promises -- is silently dropped. The user sees no output from their agent. No log entry. No error. Nothing.

This is doubly dangerous because `RuntimeOutputSink::channel()` is the only way to get an active sink. If the receiver side drops, every agent's output is lost for the remainder of the daemon's lifetime.

**Hidden Errors:** Receiver dropped due to panic in drain loop, premature shutdown, or `TaskManager` destruction.

**User Impact:** Agent runs to completion, consumes tokens, but the user sees zero output events. The task may even be marked "Completed" with 0 tokens consumed because the `TokenUsage` events were lost. Debugging this would be a nightmare -- the user would have to realize that events were generated but never […]

> DEVELOPER

# Error Handling Audit: Commit 3509c34 ("feat(runtime): stream live task output events")

## Summary

This commit adds a streaming output pipeline that captures agent stdout/stderr, parses structured JSON events, and delivers them through the daemon to gRPC clients. The overall error handling quality is above average for a Rust codebase -- the `Result<T>` propagation with `.context()` is used consistently in most places. However, I found several issues that range from CRITICAL silent failures to MEDIUM missed context.

> DEVELOPER

**Ruling: CONDITIONAL — fix items 1 and 2 above, then this is clear to merge.**</result>
<usage><total_tokens>11658</total_tokens><tool_uses>0</tool_uses><duration_ms>44230</duration_ms></usage>
</task-notification>
Full transcript available at: /private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/acdfc369cf57ebe53.output

> DEVELOPER

## 5. Recommended Fast Follow-ups (SHOULD FIX)

These should be tracked as issues and resolved promptly after merge:

- Retain and await I/O task JoinHandles; propagate panics (#3)
- Replace `yield_now` with a proper completion signal (e.g., wait on JoinHandles or a oneshot channel) (#5)
- Batch-drain output events under a single lock acquisition (#4)
- Transition tasks to `Failed` on spawn failure (#6)
- Log and handle kill errors instead of `let _ =` (#7)
- Log JSON parse errors at debug level before demoting to raw text (#8)
- Use `mutex.lock().unwrap_or_else(|e| e.into_inner())` or equivalent instead of `expect()` (#9)

> DEVELOPER

## 4. Required Action Items Before Merge

The following two items **must be resolved** to unblock merge:

1. **Bound the output channel and handle backpressure.** Replace the unbounded channel with a bounded one (reasonable capacity, e.g., 1024 or 4096). When the channel is full, the sender must either apply backpressure (block/await), drop with a logged warning and a counter, or use a policy the caller can reason about. When the receiver is gone, `tx.send()` failures must be detected — at minimum logged at `warn` level, and ideally used to signal the I/O tasks to stop.

2. **Forward all event types, not just TaskOutput.** `emit_stdout_line` must handle `AssistantText`, `Thinking`, `ToolCall`, `SessionCaptured`, and `FinalPayload` — either by forwarding them through the output channel with appropriate event wrappers, or by explicitly documenting which events are intentionally filtered and why. The current silent drop is a regression and must not ship.

> DEVELOPER

## 3. Final Verdict: **CONDITIONAL**

The commit is well-structured and delivers real functionality (output streaming is a necessary capability). However, two findings represent real bugs or architectural defects that will cause silent data loss in normal operation. These must be addressed before merge.

The SHOULD FIX items are real concerns but are acceptable as fast follow-ups given that the runtime daemon is not yet in production use.

> DEVELOPER

## 2. Arbitration: Channel Issue Severity

The Hunter rated the silent send-drop as **CRITICAL**. The Critic rated the unbounded channel as **HIGH**. I rule these as **one issue with two symptoms**, and I rate the combined finding as **MUST FIX (HIGH-CRITICAL)**. Here is my reasoning:

- The unbounded channel alone would be HIGH — it is a resource leak under adversarial/chatty conditions but not an immediate correctness bug in normal use.
- The silent send-drop alone would be HIGH — losing events is bad, but the receiver being gone implies the consumer has already disconnected, so the practical impact is limited.
- **Together**, however, they form a pipeline with no backpressure AND no failure detection. The system cannot push back on a fast producer, and when things go wrong it cannot tell anyone. This combination is what elevates it to MUST FIX: the output subsystem is architecturally unsound and will silently misbehave in any non-trivial deployment.

I do not rate it CRITICAL (i.e., "stop everything, revert") because the feature is new, behind the runtime daemon path, and not yet serving production traffic. But it must be fixed before merge.

> DEVELOPER

## Summary Table

| Finding | Verdict | Claimed Severity | Validated Severity |
|---------|---------|-----------------|-------------------|
| A: Unbounded channel | CONFIRMED | HIGH/CRITICAL | MEDIUM |
| B: Lock held per-envelope | CONFIRMED | HIGH | HIGH |
| C: yield_now unreliable | CONFIRMED | MEDIUM | MEDIUM |
| D: Non-TaskOutput dropped | CONFIRMED | MEDIUM/HIGH | MEDIUM/HIGH |
| E: JoinHandle discarded | CONFIRMED | HIGH/MEDIUM | MEDIUM |
| F: JSON parse fallback | CONFIRMED | HIGH | LOW/MEDIUM |
| G: Zombie tasks on spawn fail | FALSE POSITIVE | HIGH | N/A |
| H: Kill errors in rollback | CONFIRMED | MEDIUM | MEDIUM |
| I: Mutex expect panic | CONFIRMED | MEDIUM | LOW |
| J: UTF-8 lossy corruption | CONFIRMED | MEDIUM | MEDIUM |

**Key takeaways:**
- 9 of 10 findings are real; Finding G is a false positive because `spawn_prepared` properly transitions failed tasks to terminal states before returning errors.
- Findings B, C, D, and E are the most actionable. B and E are architecturally related (no join handles means no reliable drain, which forces the yield_now hack in C).
- Finding F was overstated -- the […]

> DEVELOPER

### FINDING J: `from_utf8_lossy` silently corrupts binary/split-UTF8 data

**Verdict: CONFIRMED -- severity accurate (MEDIUM)**

At `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/io.rs` lines 312-313:

```rust
fn emit_chunk_lines(buffer: &mut String, chunk: &[u8], mut emit: impl FnMut(String)) {
    buffer.push_str(&String::from_utf8_lossy(chunk));
```

This function is used exclusively in `spawn_docker_attach_task` (line 211-217) for Docker container output streams (Bollard's `LogOutput` returns `Bytes`). Docker multiplexed streams can split data at arbitrary byte boundaries, including in the middle of multi-byte UTF-8 sequences. When `from_utf8_lossy` encounters a truncated multi-byte character at the end of a chunk, it replaces it with U+FFFD. The next chunk will then start with trailing bytes of that character, which will also be replaced. This corrupts the original data and could break JSON parsing downstream. Note that the host and bwrap paths use `BufReader::lines()` which handles this correctly via tokio's line reader. This issue is specific to the Docker path. MEDIUM severity is accurate -- it requires specific conditions (multi-byte chars at chunk boundaries) but the consequence (corrupted JSON) is significant.

> DEVELOPER

### FINDING I: Mutex `expect()` will panic on poisoning

**Verdict: CONFIRMED -- severity LOW (not MEDIUM)**

At `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/io.rs` lines 158 and 165:

```rust
pub fn remember_kill_reason(&self, reason: impl Into<String>) {
    let mut kill_reason = self.kill_reason.lock().expect("kill reason mutex poisoned");
    *kill_reason = Some(reason.into());
}

pub fn kill_reason(&self) -> Option<String> {
    self.kill_reason
        .lock()
        .expect("kill reason mutex poisoned")
        .clone()
}
```

This uses `std::sync::Mutex` (not tokio), and `.expect()` will indeed panic if the mutex is poisoned. However, mutex poisoning only happens if a thread panics while holding the lock. The lock-holding scope in both functions is trivial (just assignment/clone, no fallible operations), so poisoning would only occur from a prior panic on another thread holding this same lock -- which means the process is already in a compromised state. Using `.expect()` on `std::sync::Mutex` for infallible inner operations is an accepted Rust pattern. **Severity: LOW**, not MEDIUM. The daemon is already in trouble if this fires.

> DEVELOPER

### FINDING H: Kill errors discarded with `let _ =` during spawn rollback

**Verdict: CONFIRMED -- severity accurate (MEDIUM)**

At `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/task_manager.rs` lines 283 and 304:

```rust
// Line 283:
let _ = self.runtime.kill(&handle).await;

// Line 304:
let _ = self.runtime.kill(&handle).await;
```

These are rollback paths during spawn failure cleanup. If `kill` fails, the spawned agent process continues running but is not tracked (since registration never happened or was rolled back). The agent would be a genuinely orphaned process. However, this is a narrow failure window (kill failing on a just-spawned process is rare), and the alternative (propagating the kill error) would mask the original failure reason. MEDIUM is appropriate -- logging the kill error would be a meaningful improvement.

> DEVELOPER

### FINDING G: `dispatch_enqueued_tasks` silently skips failed spawns -- zombie tasks

**Verdict: FALSE POSITIVE**

At `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/task_manager.rs` lines 220-230:

```rust
match self.spawn_prepared(prepared).await {
    Ok(_) => launched.push(task_id),
    Err(error) => {
        tracing::warn!(
            %error,
            run_id = %run_id,
            task_id = %task_id,
            "failed to dispatch enqueued task"
        );
    }
}
```

The claim says tasks may remain stuck in Materializing/Running. But look at `spawn_prepared` (lines 237-324): every failure path properly transitions the task to a terminal state before returning `Err`:

1. Runtime spawn failure (line 251-270): transitions task to `TaskStatus::Failed` before returning error.
2. Running transition failure (line 279-289): kills the agent and returns error. The task is left in `Materializing`, but this path only fires if the orchestrator itself can't persist the transition -- a catastrophic failure.
3. Agent persistence failure (line 303-317): kills the agent, transitions task to `TaskStatus::Failed`, then returns error.

The only edge case is path 2 where `transition_task` itself fails, leaving the task in `Materializing`. But this is an infrastructure failure (DB down), not a normal spawn failure. The warn-and-continue in `dispatch_enqueued_tasks` is appropriate because `spawn_prepared` already handles cleanup. **FALSE POSITIVE** -- the claim of "zombie tasks" is not substantiated by the code.

> DEVELOPER

### FINDING F: JSON parse failure silently demotes to raw stdout

**Verdict: CONFIRMED -- severity PARTIALLY OVERSTATED (LOW/MEDIUM, not HIGH)**

At `/home/<USER>/Projects/AI/forge/crates/forge-common/src/output_parser.rs` lines 36-38:

```rust
ParsedOutputMode::StreamJson => serde_json::from_str::<Value>(&line)
    .map(|json| parse_stream_json_event(state, &json))
    .unwrap_or_else(|_| vec![ParsedOutputEvent::TaskOutput(TaskOutput::Stdout(line))]),
```

A JSON parse failure falls back to emitting the raw line as `TaskOutput::Stdout`. This is **the same behavior as the old `DirectExecutionFacade`** code before this commit (see the diff where the old code did `if let Ok(json) = serde_json::from_str::<Value>(&line) { ... } else { send_event(... Stdout(line) ...) }`). This is a deliberate and reasonable fallback -- Claude CLI may emit non-JSON diagnostic lines even in stream-json mode. The parse error is not "discarded" in a harmful way; the raw line is preserved as output. HIGH severity is overstated. This is LOW/MEDIUM at most -- a debug-level log of parse failures would be a nice-to-have but the behavior is correct.

> DEVELOPER

### FINDING E: Spawned I/O tasks discard JoinHandle -- panics swallowed

**Verdict: CONFIRMED -- severity PARTIALLY OVERSTATED (MEDIUM, not HIGH)**

At `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/io.rs` lines 269-289 and 291-309:

```rust
fn spawn_stdout_task<R>(reader: R, emitter: RuntimeOutputEmitter)
where
    R: AsyncRead + Unpin + Send + 'static,
{
    tokio::spawn(async move {
        let mut lines = BufReader::new(reader).lines();
        let mut state = ParsedOutputState::default();
        loop {
            match lines.next_line().await {
                Ok(Some(line)) => emitter.emit_stdout_line(&mut state, line),
                Ok(None) => break,
                Err(error) => { ... break; }
            }
        }
    });
}
```

The `JoinHandle` from `tokio::spawn` is indeed discarded. The functions return nothing. This means: (1) panics inside the task are caught by tokio's default panic handler (logged to stderr) but not propagated to the caller; (2) there's no way for `TrackedChild::new` or `check_agent_status` to wait for I/O tasks to complete, which is the root cause of Finding C. However, panics in these tasks are unlikely -- they just do `BufReader::lines()` reads and emit events. The real impact is the inability to join on completion, not panic swallowing. MEDIUM is the right severity; HIGH overstates the panic risk.

> DEVELOPER

### FINDING D: Non-TaskOutput parsed events silently dropped

**Verdict: CONFIRMED -- severity accurate (MEDIUM/HIGH)**

At `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/io.rs` lines 82-88:

```rust
pub fn emit_stdout_line(&self, state: &mut ParsedOutputState, line: String) {
    for event in parse_output_line(state, self.output_mode, line) {
        if let ParsedOutputEvent::TaskOutput(output) = event {
            self.emit(output);
        }
    }
}
```

Compare with `DirectExecutionFacade` at `direct_execution.rs` lines 326-381, which handles ALL variants:

```rust
async fn emit_parsed_events(...) {
    for event in events {
        match event {
            ParsedOutputEvent::TaskOutput(output) => { ... }
            ParsedOutputEvent::AssistantText(text) => { ... }
            ParsedOutputEvent::Thinking(thinking) => { ... }
            ParsedOutputEvent::ToolCall { name, input } => { ... }
            ParsedOutputEvent::SessionCaptured(session_id) => { ... }
            ParsedOutputEvent::FinalPayload(payload) => { ... }
        }
    }
}
```

The runtime path drops `AssistantText`, `Thinking`, `ToolCall`, `SessionCaptured`, and `FinalPayload`. This is a deliberate design choice *at this stage* -- the runtime output channel only carries `TaskOutput` variants, and the dropped events are informational/streaming events that the daemon doesn't yet have an equivalent channel for. However, `SessionCaptured` loss means session resume won't work, and `FinalPayload` loss means the full result payload is unavailable to post-processing. This is a real feature gap. The finding is CONFIRMED but whether it's a "regression" depends on perspective -- the runtime path is new and intentionally narrower, […]

> DEVELOPER

### FINDING C: Output events lost between process exit and drain (yield_now unreliable)

**Verdict: CONFIRMED -- severity accurate (MEDIUM)**

At `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/task_manager.rs` line 344:

```rust
if matches!(
    status,
    AgentStatus::Exited { .. } | AgentStatus::Killed { .. } | AgentStatus::Crashed { .. }
) {
    tokio::task::yield_now().await;
    self.drain_runtime_output().await?;
}
```

`yield_now()` yields the current task to the tokio scheduler but provides no guarantee that the spawned I/O reader tasks (`spawn_stdout_task`, `spawn_stderr_task`) have finished reading and emitting all envelopes. The I/O tasks at io.rs lines 269-309 are fire-and-forget `tokio::spawn` calls. If the process exits but the BufReader still has data buffered in the pipe, `yield_now` may return before those tasks complete their final reads and `emit` calls. The final `result` JSON line (which contains `FinalPayload` with token usage and `PromiseDone`) could still be in-flight. The existing integration tests pass because they add a 150ms sleep before checking, masking this race. MEDIUM is accurate -- data loss is probabilistic, not certain.

> DEVELOPER

### FINDING B: Orchestrator lock held per-envelope during drain

**Verdict: CONFIRMED -- severity accurate (HIGH)**

At `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/task_manager.rs` lines 173-193:

```rust
pub async fn drain_runtime_output(&self) -> Result<usize> {
    let mut envelopes = Vec::new();
    {
        let mut rx = self.runtime_output_rx.lock().await;
        while let Ok(envelope) = rx.try_recv() {
            envelopes.push(envelope);
        }
    }

    for envelope in &envelopes {
        if let TaskOutput::TokenUsage { cumulative, .. } = &envelope.output {
            self.tracker
                .update_tokens_consumed(&envelope.task_id, *cumulative)
                .await;
        }
        self.append_task_output_event(envelope).await?;
    }
    Ok(envelopes.len())
}
```

And `append_task_output_event` at lines 494-514:

```rust
async fn append_task_output_event(&self, envelope: &RuntimeOutputEnvelope) -> Result<()> {
    let mut orchestrator = self.orchestrator.lock().await;
    orchestrator.record_runtime_event_for_agent(...)
        .await
        ...
}
```

And `record_runtime_event_for_agent` (run_orchestrator.rs lines 1124-1159) acquires the orchestrator mutex (already held), does `append_and_wake` which calls `spawn_blocking` for SQLite, then does another `spawn_blocking` for `update_run_cursor`. So for N envelopes, the orchestrator lock is acquired and released N times, each time doing two `spawn_blocking` calls. This serializes the daemon loop while draining. HIGH severity is appropriate because if a fast-running agent produces many output lines before the first poll, hundreds of sequential blocking writes will stall gRPC operations that also need the orchestrator lock.

> DEVELOPER

## Validation Report: Commit 3509c34 Findings

### FINDING A: Unbounded channel with no backpressure

**Verdict: CONFIRMED -- severity PARTIALLY OVERSTATED (MEDIUM, not CRITICAL)**

The code at `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/io.rs` lines 31-51:

```rust
pub fn channel() -> (Self, mpsc::UnboundedReceiver<RuntimeOutputEnvelope>) {
    let (tx, rx) = mpsc::unbounded_channel();
    (Self { tx: Some(tx) }, rx)
}

fn emit(&self, envelope: RuntimeOutputEnvelope) {
    if let Some(tx) = &self.tx {
        let _ = tx.send(envelope);
    }
}
```

The channel is indeed unbounded and `let _ =` discards send errors. However, the practical severity is lower than CRITICAL for two reasons: (1) agent output is line-oriented text/JSON from Claude CLI -- the throughput is bounded by the speed of an LLM generating tokens, which is far from "millions of envelopes" territory; (2) `drain_runtime_output` is called in the daemon's poll loop (on every `check_agent_status` terminal detection at line 344-345, and likely in the main daemon tick), so the queue doesn't grow unboundedly in normal operation. The `let _ =` on send is a legitimate concern since a dropped receiver means events are silently lost with no logging. **Severity: MEDIUM** (not HIGH/CRITICAL). The unbounded channel is a reasonable design choice for this throughput level, but the silent send-error discard should be logged.

> DEVELOPER

### SUMMARY

| Severity | Count | Key Issues |
|----------|-------|------------|
| CRITICAL | 0 | - |
| HIGH | 3 | PID cast overflow to `kill()`, host env inheritance, processes HashMap memory leak |
| MEDIUM | 7 | kill_reasons leak, container name collision, output discarded, dangerously-skip-permissions hardcoded, race between poll and kill, unsafe set_var in tests, no Docker timeout |
| LOW | 1 | Lifecycle loop tick behavior |

### VERDICT: **CONDITIONAL**

The commit should not be merged without addressing the three HIGH items:

1. **PID cast overflow** (findings 1) -- Use `i32::try_from(pid)?` instead of `pid as i32` in `send_signal` and `process_exists`. Sending signals to wrong PIDs is a security issue.

2. **Host runtime environment inheritance** (finding 2) -- Add `.env_clear()` before setting agent-specific environment variables in `host.rs`. Agents should not inherit the daemon's secrets.

3. **Unbounded `processes`/`kill_reasons` growth** (findings 3, 4) -- Add cleanup of entries in `status()` when a terminal state is detected, or in `kill()` after the process is reaped. Without this, long-running daemons will leak memory proportionally to total agents spawned.

Finding 6 (output discarded) is also concerning but appears to be in-progress based on uncommitted changes in the working tree. If […]

> DEVELOPER

**11. Task manager lifecycle loop runs dispatch and poll sequentially**

- **File**: `main.rs` lines 131-155 (committed version)
- **Severity**: LOW
- **Description**: The lifecycle ticker runs `dispatch_enqueued_tasks()` then `poll_active_agents()` sequentially on each 250ms tick. Both acquire the orchestrator mutex. If either operation is slow (e.g., spawning a process takes time, or polling many agents), the tick interval will slip and the next tick will fire immediately, potentially causing a tight loop.
- **Why it matters**: Under load with many agents, the lifecycle loop could consume excessive CPU by never actually sleeping between ticks. A `MissedTickBehavior::Delay` would be more appropriate.

> DEVELOPER

**10. No timeout on Docker container start**

- **File**: `docker.rs` lines 349-357 (committed version)
- **Severity**: MEDIUM
- **Description**: After `create_container`, `start_container` is called without any timeout. If the Docker daemon hangs (e.g., waiting for an image layer, or a Docker bug), this call will block the spawn operation indefinitely.
- **Why it matters**: A hung `start_container` would prevent the task from ever completing or failing, and the gRPC handler would hang. The `ensure_image` pull loop also has no timeout -- pulling a large image could block for an arbitrary duration.

> DEVELOPER

**9. `set_var`/`remove_var` in tests are unsound on Rust 2024**

- **File**: `task_manager.rs` lines 729-732, 762-763, 797-798, 821
- **Severity**: MEDIUM
- **Description**: The tests use `unsafe { std::env::set_var("CLAUDE_CMD", ...) }` and `unsafe { std::env::remove_var("CLAUDE_CMD") }`. In Rust 2024 edition (which this project targets per CLAUDE.md), `set_var` and `remove_var` are marked `unsafe` because they are not thread-safe when other threads may be reading environment variables. The code uses a `StdMutex` guard (`ENV_MUTEX`), but this only protects against races with other tests that use the same mutex -- not against arbitrary environment reads in other threads or tokio tasks.
- **Why it matters**: In a multi-threaded tokio test runtime, `set_var` in one test can race with `default_agent_program()` in another test's spawned agent. The mutex only serializes tests that acquire it, not the environment access itself.

> DEVELOPER

**8. Race condition between `check_agent_status` and `kill_agent`**

- **File**: `task_manager.rs` lines 292-366, 380-401
- **Severity**: MEDIUM
- **Description**: `check_agent_status` and `kill_agent` both call `self.tracker.remove()` without mutual exclusion. If `poll_active_agents` is running concurrently (e.g., from the 250ms lifecycle ticker) while `kill_agent` is called from a gRPC handler, both could attempt to process the same task:
  1. `poll_active_agents` calls `check_agent_status`, finds the agent exited
  2. Concurrently, `kill_agent` is called for the same task
  3. Both call `self.tracker.remove()` -- one succeeds, one gets `None`
  4. The winner transitions the task, the loser may try `run_id_for_task` and get stale data

  The `AgentTracker` itself is protected by `RwLock`, but the check-then-act sequences across multiple lock acquisitions are not atomic.
- **Why it matters**: Could result in duplicate task state transitions, which may violate state machine invariants in the orchestrator, or cause `kill_agent` to fail with "no tracked agent" error after the poll cycle already cleaned it up.

> DEVELOPER

**7. `--dangerously-skip-permissions` hardcoded in agent launch**

- **File**: `task_manager.rs` lines 590-598
- **Severity**: MEDIUM
- **Description**: `default_agent_args()` hardcodes `--dangerously-skip-permissions` as a launch argument for all agents. This flag disables Claude's built-in permission checks.
- **Why it matters**: This is appropriate for sandboxed backends (bwrap, docker) where the runtime itself enforces isolation. But when running with the host backend, this means an agent can execute arbitrary commands on the host without any permission checking. Combined with finding 2 (full environment inheritance), this creates a situation where the host runtime provides zero security barriers. The flag should be conditional on the selected backend, or at minimum logged as a warning when combined with host runtime.

> DEVELOPER

**6. Stdout/stderr silently drained and discarded (committed version)**

- **File**: `io.rs` lines 112-120 (committed version, `spawn_drain_task`)
- **Severity**: MEDIUM
- **Description**: In the committed version at f945716, `TrackedChild::new` takes only `child` and `stdin_payload` -- it does NOT accept an emitter. Stdout and stderr are silently drained to `/dev/null` via `tokio::io::sink()`. This means all agent output (including error messages, progress, results) is completely lost.
- **Why it matters**: This is a correctness concern. The `output_mode: AgentOutputMode::StreamJson` is set in `build_launch_spec`, indicating the daemon expects structured output from agents. But the committed code discards it entirely. No task output events will ever be emitted to the event stream. The daemon will only ever know about process exit codes, not actual agent results. Note: the working tree has uncommitted changes that add output capture, but the committed version at f945716 does not have it.

> DEVELOPER

**5. Docker container name collision on reuse**

- **File**: `docker.rs` lines 274-278 (committed version)
- **Severity**: MEDIUM
- **Description**: Container names are generated as `forge-agent-{sanitized_agent_id}`. The `auto_remove` flag is set to `false`, and `best_effort_remove_container` is only called on start failure. If an agent ID is reused (which `AgentId::generate()` makes unlikely but not impossible with user-supplied IDs in tests), or if a prior container with that name was not cleaned up, `create_container` will fail with a 409 Conflict. There is no retry or old-container cleanup before creation.
- **Why it matters**: While unlikely in production due to `AgentId::generate()` using UUIDs, any daemon restart without container cleanup or any test reuse path could hit this. A robust guard would be to attempt removal of the same name before creation.

> DEVELOPER

**4. Docker `kill_reasons` HashMap never cleaned**

- **File**: `docker.rs` (struct `DockerRuntime`)
- **Severity**: MEDIUM
- **Description**: When an agent is killed, `remember_kill_reason()` inserts into `self.kill_reasons`. This map is only read by `kill_reason()` but entries are never removed, even after the container is fully gone and status has been read.
- **Why it matters**: Same unbounded growth pattern as finding 3. Over time in a long-running daemon, the `kill_reasons` map accumulates one entry per killed container forever.

> DEVELOPER

**3. Unbounded growth in `processes` HashMap (memory leak)**

- **Files**: `bwrap.rs` (struct `BwrapRuntime`), `host.rs` (struct `HostRuntime`)
- **Severity**: HIGH
- **Description**: When a process is spawned, an `Arc<TrackedChild>` is inserted into `self.processes`. After the process terminates, the entry is **never removed**. Neither `status()` (which detects exit) nor `kill()` (which terminates the process) remove the entry. The `AgentTracker` in `task_manager.rs` correctly removes entries via `self.tracker.remove()`, but the underlying runtime's `processes` map grows forever.
- **Why it matters**: In a long-running daemon that spawns many agents over time, the `processes` HashMap will accumulate `TrackedChild` entries, each holding a `Mutex<Child>` for an already-exited process plus its kill reason. This is a memory leak proportional to the total number of agents ever spawned.

> DEVELOPER

Lets spawn a council of agents. Here are their roles and responsibilities:
  - Agent to review the changes made to the codebase in a critical manner
  - Agent to ensure that the critical recommendations if any are valid
  - Agent to commit the change as per the critical recommendations if there are any
  - Agent to supervise the above group of agents and is final arbitrator. This agent can also spawn multile other
  agents if required.

> TOOL

[Request interrupted by user]

> DEVELOPER

Lets spawn a council of agents. Here are their roles and responsibilities:
  - Agent to review the changes made to the codebase in a critical manner
  - Agent to ensure that the critical recommendations if any are valid
  - Agent to commit the change as per the critical recommendations if there are any
  - Agent to supervise the above group of agents and is final arbitrator. This agent can also spawn multile other
  agents if required.

The above is applied to the last commit to this branch

> AGENT

Both agents are actively reviewing. Waiting for their reports to come in before launching the next phase of the council.

<details>
<summary>Council pipeline</summary>

1. **Phase 1** (running): Critical Reviewer + Silent Failure Hunter analyze the commit independently
2. **Phase 2** (pending): Validator agent cross-checks critical findings against the actual code
3. **Phase 3** (pending): Supervisor agent synthesizes all reports, makes final ruling, and optionally spawns additional focused agents

</details>

> METADATA

<task-notification>
<task-id>acc8cf36acdc10892</task-id>
<tool-use-id>REDACTED</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/acc8cf36acdc10892.output</output-file>
<status>completed</status>
<summary>Agent "Hunt silent failures in last commit" completed</summary>
<result>Now I have all the data I need. Let me compile my comprehensive error handling audit.

---

# Error Handling Audit: `f945716` ("feat(runtime): add backend execution and task dispatch")

## Executive Summary

This commit adds approximately 5,500 lines across 28 files implementing runtime backend execution (bwrap, Docker, host), task lifecycle management, and profile compilation. The error handling is **substantially above average** for Rust code -- the author uses `anyhow::Context` pervasively, returns `Result<T>` from public functions, and employs `bail!` for explicit validation failures. However, I found **10 issues** ranging from critical silent failures to medium-severity gaps.

---

## ISSUE 1: Silent Drops of Runtime Kill Results During Spawn Rollback

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/task_manager.rs`, lines 248-290

**Severity:** CRITICAL

**Issue Description:** When `spawn_prepared` fails to transition a successfully-spawned task to `Running`, or fails to persist the agent instance row, the cleanup code uses `let _ =` to silently discard errors from `self.runtime.kill(&handle)` and `self.transition_task(...)`. There are three instances:

```rust
// Line 250
let _ = self.runtime.kill(&handle).await;

// Line 271
let _ = self.runtime.kill(&handle).await;

// Lines 276-278
let _ = self
    .transition_task(&prepared.run_id, &prepared.task_id, failed)
    .await;
```

**Hidden Errors:** If `runtime.kill()` fails (e.g., the […]

> AGENT

Critic agent is still working through the codebase. Will proceed as soon as it reports back.

> METADATA

<task-notification>
<task-id>a036c791877b0d33e</task-id>
<tool-use-id>toolu_019kzu5BoBFrkGpaFByuzuS3</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/a036c791877b0d33e.output</output-file>
<status>completed</status>
<summary>Agent "Critical code review of last commit" completed</summary>
<result>Now I have a comprehensive view of the committed code at f945716. Let me compile my findings.

---

## Critical Review: f945716 -- "feat(runtime): add backend execution and task dispatch"

### FINDINGS

---

**1. PID cast overflow: `pid as i32` can silently wrap**

- **Files**: `bwrap.rs` lines 365, 379; `host.rs` lines 202, 216
- **Severity**: HIGH
- **Description**: `libc::kill()` takes a `pid_t` (i32), but the PID comes from `child.id()` which returns `u32`. The cast `pid as i32` will silently wrap PIDs > 2,147,483,647 to negative values. On Linux, negative PIDs to `kill()` are interpreted as process group IDs, which means `send_signal` could kill an unrelated process group.
- **Why it matters**: Although PIDs this large are rare on standard Linux, on systems with PID namespace recycling or large `pid_max`, a wrap would send SIGTERM/SIGKILL to the wrong process group. This is a security-relevant misuse of a low-level unsafe API. The fix is `i32::try_from(pid).context("pid overflow")`.

---

**2. Host runtime inherits full parent environment**

- **Files**: `host.rs` lines 76-97 (committed version)
- **Severity**: HIGH
- **Description**: The host runtime uses `Command::new()` with `.env()` additions, but without calling `.env_clear()` first. […]

> AGENT

Phase 2 agents launched:

| Role | Agent | Status |
|------|-------|--------|
| **Critical Reviewer** | `critic` | Done — 11 findings, verdict CONDITIONAL |
| **Silent Failure Hunter** | `silent-failure-hunter` | Done — 10 findings, 1 CRITICAL |
| **Validator** | `validator` | Running — reading actual code to confirm/reject each finding |
| **Supervisor** | `supervisor` | Running — synthesizing reports, producing final ruling |

Waiting for both to complete...

> METADATA

<task-notification>
<task-id>aa348dd4d26461e50</task-id>
<tool-use-id>REDACTED</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/aa348dd4d26461e50.output</output-file>
<status>completed</status>
<summary>Agent "Supervise council and arbitrate" completed</summary>
<result>

# Supervisor Review Ruling — Commit f945716

## 1. Unified, Deduplicated Findings

I have merged the two reports into a single prioritized list. Where both reviewers flagged the same issue, I note the overlap and take the higher severity.

| # | Classification | Finding | Source |
|---|---------------|---------|--------|
| U1 | **MUST FIX** | **PID `as i32` truncation can send signals to wrong process groups.** On platforms where PID exceeds i32::MAX, `kill(-pgid)` hits an arbitrary process group. Both reviewers independently flagged this, confirming it is real and dangerous. | Critic #1, Hunter #4 |
| U2 | **MUST FIX** | **Host runtime inherits full parent environment — agents receive the daemon's secrets.** This is a privilege escalation path. An agent running under the host backend gets every env var the daemon holds (API keys, tokens, database credentials). The entire point of a runtime sandbox is to prevent this. | Critic #2 |
| U3 | **MUST FIX** | **Unbounded `processes` HashMap — TrackedChild entries are never removed.** This is a memory leak proportional to total tasks over daemon lifetime. In a long-running daemon, this will eventually exhaust […]

> AGENT

Supervisor has delivered the ruling. Still waiting for the Validator to finish cross-checking findings against the actual code — this will confirm or reject the 3 must-fix items before we proceed.

> METADATA

<task-notification>
<task-id>a1056f21b1f24734d</task-id>
<tool-use-id>toolu_015bfEBQ1Vb7HpLtHYyLSkuU</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/a1056f21b1f24734d.output</output-file>
<status>completed</status>
<summary>Agent "Validate critical review findings" completed</summary>
<result>Now I have all the source code needed to validate every finding. Let me compile my validation report.

---

# Validation Report: Commit f945716

## Finding A: PID cast overflow -- `pid as i32` can silently wrap

**Verdict: CONFIRMED -- Severity accurate (HIGH)**

The code at `bwrap.rs:365` and `host.rs:202` is identical:

```rust
fn send_signal(pid: u32, signal: i32) -> Result<()> {
    let rc = unsafe { libc::kill(pid as i32, signal) };
```

And at `bwrap.rs:379` / `host.rs:216`:

```rust
fn process_exists(pid: u32) -> bool {
    let rc = unsafe { libc::kill(pid as i32, 0) };
```

The `pid` parameter is `u32`, and `libc::kill` takes `libc::pid_t` which is `i32`. If a PID exceeds `i32::MAX` (2,147,483,647), the cast `pid as i32` wraps to a negative value. Passing a negative PID to `kill()` sends the signal to all processes in the process group whose PGID equals the absolute value of that number. This is a real correctness/safety bug.

**Mitigating factor**: On Linux, the default `pid_max` is 32,768 (maximum configurable is 4,194,304 on 64-bit), so PIDs above `i32::MAX` are effectively impossible in practice. On macOS, PIDs are also well within `i32` range. The severity is […]

> AGENT

All four council agents have completed. Here's the final consolidated ruling:

---

## Council Verdict: **CONDITIONAL**

### MUST FIX before merge (3 items — validated against actual code)

| # | Finding | Files | Fix |
|---|---------|-------|-----|
| **1** | **PID `as i32` truncation** — can send signals to wrong process groups | `bwrap.rs:365,379` `host.rs:202,216` | Replace `pid as i32` with `i32::try_from(pid)?` |
| **2** | **Host runtime leaks daemon env** — agents inherit all secrets | `host.rs:76-97` | Add `.env_clear()` before `.env()` calls |
| **3** | **Unbounded `processes` HashMap** — TrackedChild entries never removed | `bwrap.rs`, `host.rs` | Remove entries in `kill()` and on terminal status in `status()` |

### SHOULD FIX (fast follow-up PR)

| # | Finding | Validated Severity |
|---|---------|-------------------|
| 4 | Silent `let _ =` on kill during spawn rollback (task_manager.rs:279-317) | HIGH (downgraded from CRITICAL — `kill_on_drop` mitigates) |
| 5 | `dispatch_enqueued_tasks` swallows spawn failures | MEDIUM (spawn_prepared handles its own cleanup) |
| 6 | Silent channel send drop in RuntimeOutputSink | MEDIUM (intentional fire-and-forget design) |
| 7 | Docker `kill_reasons` HashMap never cleaned | MEDIUM |
| 8 | `force_stop` == `graceful_stop` (no escalation) | MEDIUM […]

> DEVELOPER

Lets spawn a council of agents. Here are their roles and responsibilities:
  - Agent to review the changes made to the codebase in a critical manner
  - Agent to ensure that the critical recommendations if any are valid
  - Agent to commit the change as per the critical recommendations if there are any
  - Agent to supervise the above group of agents and is final arbitrator. This agent can also spawn multile other
  agents if required.

The above is applied to the last commit to this branch

> AGENT

Council Phase 1 launched:

| Role | Agent | Status |
|------|-------|--------|
| **Critical Reviewer** | `critic` | Running — reviewing all 12 changed files |
| **Silent Failure Hunter** | `silent-hunter` | Running — hunting error handling gaps |
| **Validator** | *pending* | Launches after reviewers finish |
| **Supervisor** | *pending* | Final arbitrator — launches after reviewers finish |

Waiting for Phase 1 to complete...

> METADATA

<task-notification>
<task-id>a0ab3385e24a58439</task-id>
<tool-use-id>toolu_01T1BDymYD689fiYPnP8GpXP</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/a0ab3385e24a58439.output</output-file>
<status>completed</status>
<summary>Agent "Critical review of output streaming commit" completed</summary>
<result>I have now thoroughly reviewed all the changed files. Here is my structured review.

---

## Critical Review: `feat(runtime): stream live task output events` (3509c34)

### Finding 1 — Unbounded Channel as Back-Pressure-Free Output Queue

**File:** `crates/forge-runtime/src/runtime/io.rs` lines 31-51  
**Severity:** HIGH

`RuntimeOutputSink` uses `mpsc::unbounded_channel()`. Every stdout and stderr line from every running agent is pushed into this single channel. The channel is only drained by the ticker loop in `main.rs` every 250ms. A fast-producing agent (or multiple concurrent agents) can accumulate millions of envelopes in memory before the drain cycle fires. There is no backpressure: the `emit` method ignores the send result (`let _ = tx.send(...)`), and there is no cap on queue depth.

**Why it matters:** A chatty agent that emits thousands of lines per second will cause unbounded heap growth. Over the 250ms tick interval, a single agent writing at 10K lines/second produces 2,500 envelopes with cloned `RunId`, `TaskNodeId`, `AgentId`, `TaskOutput`, and `DateTime` per interval. Multiple agents compound this. Under sustained load this is a denial-of-service vector against the daemon itself.

---

### Finding 2 — Orchestrator Lock Held Per-Envelope During Drain

**File:** `crates/forge-runtime/src/task_manager.rs` lines […]

> AGENT

Critical Reviewer is done (9 findings, verdict CONDITIONAL). Waiting for Silent Failure Hunter to finish before launching Phase 2.

> METADATA

<task-notification>
<task-id>a5be0d8f7c291a6d1</task-id>
<tool-use-id>REDACTED</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/a5be0d8f7c291a6d1.output</output-file>
<status>completed</status>
<summary>Agent "Hunt silent failures in output streaming" completed</summary>
<result>Now I have a thorough understanding of all the changed files. Let me compile the full error handling audit.

---

# Error Handling Audit: Commit 3509c34 ("feat(runtime): stream live task output events")

## Summary

This commit adds a streaming output pipeline that captures agent stdout/stderr, parses structured JSON events, and delivers them through the daemon to gRPC clients. The overall error handling quality is above average for a Rust codebase -- the `Result<T>` propagation with `.context()` is used consistently in most places. However, I found several issues that range from CRITICAL silent failures to MEDIUM missed context.

---

## Issue 1: Silent channel send failure -- events permanently lost

**Location:** `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/io.rs`, line 48

**Severity:** CRITICAL

```rust
fn emit(&self, envelope: RuntimeOutputEnvelope) {
    if let Some(tx) = &self.tx {
        let _ = tx.send(envelope);
    }
}
```

The `let _ = tx.send(envelope)` discards the `Result` returned by `mpsc::UnboundedSender::send()`. If the receiving half of the channel is dropped (e.g., the `TaskManager` is torn down before agents finish, or the receiver lock is poisoned), every subsequent output event -- stdout lines, token usage, progress signals, DONE promises -- is silently dropped. The […]

> AGENT

Phase 2 launched:

| Role | Agent | Status |
|------|-------|--------|
| **Critical Reviewer** | `critic` | Done — 9 findings, verdict CONDITIONAL |
| **Silent Failure Hunter** | `silent-hunter` | Done — 11 findings, 1 CRITICAL |
| **Validator** | `validator` | Running — reading actual code to confirm/reject findings |
| **Supervisor** | `supervisor` | Running — synthesizing and arbitrating |

Waiting for both to report back...

> METADATA

<task-notification>
<task-id>acdfc369cf57ebe53</task-id>
<tool-use-id>REDACTED</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/acdfc369cf57ebe53.output</output-file>
<status>completed</status>
<summary>Agent "Supervise and arbitrate council findings" completed</summary>
<result>

# Supervisor Ruling — Commit 3509c34

## 1. Unified, Deduplicated Findings

I have merged the two reports, collapsed overlaps, and ordered by priority.

| # | Classification | Finding | Sources |
|---|---------------|---------|---------|
| 1 | **MUST FIX** | **Unbounded channel with silent send-drop**: The output channel is unbounded (no backpressure), meaning a chatty agent grows the heap without limit. Additionally, `let _ = tx.send()` silently discards all events once the receiver is gone — the system has no way to detect or react to a disconnected consumer. These are two facets of one design flaw: the output pipeline has no flow control and no failure signaling. | Critic #1, Hunter #1 |
| 2 | **MUST FIX** | **Non-TaskOutput events silently dropped**: `emit_stdout_line` only forwards `TaskOutput` events. All other event types — `AssistantText`, `Thinking`, `ToolCall`, `SessionCaptured`, `FinalPayload` — are silently discarded. This is a functional regression vs `DirectExecutionFacade` and means consumers of the stream get an incomplete picture of agent activity. | Critic #4, Hunter #6 |
| 3 | **SHOULD FIX** | **Spawned I/O task JoinHandles discarded**: Both stdout and stderr reader tasks are `tokio::spawn`'d […]

> AGENT

Supervisor has ruled. Waiting for the Validator to finish confirming findings against actual code before presenting the final report.

> METADATA

<task-notification>
<task-id>a8d53686eb81a73d8</task-id>
<tool-use-id>toolu_01N9yPQAnHQteP8bNXkXox8D</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/a8d53686eb81a73d8.output</output-file>
<status>completed</status>
<summary>Agent "Validate findings against actual code" completed</summary>
<result>Now I have all the code I need. Let me produce the validation report.

---

## Validation Report: Commit 3509c34 Findings

### FINDING A: Unbounded channel with no backpressure

**Verdict: CONFIRMED -- severity PARTIALLY OVERSTATED (MEDIUM, not CRITICAL)**

The code at `/home/<USER>/Projects/AI/forge/crates/forge-runtime/src/runtime/io.rs` lines 31-51:

```rust
pub fn channel() -> (Self, mpsc::UnboundedReceiver<RuntimeOutputEnvelope>) {
    let (tx, rx) = mpsc::unbounded_channel();
    (Self { tx: Some(tx) }, rx)
}

fn emit(&self, envelope: RuntimeOutputEnvelope) {
    if let Some(tx) = &self.tx {
        let _ = tx.send(envelope);
    }
}
```

The channel is indeed unbounded and `let _ =` discards send errors. However, the practical severity is lower than CRITICAL for two reasons: (1) agent output is line-oriented text/JSON from Claude CLI -- the throughput is bounded by the speed of an LLM generating tokens, which is far from "millions of envelopes" territory; (2) `drain_runtime_output` is called in the daemon's poll loop (on every `check_agent_status` terminal detection at line 344-345, and likely in the main daemon tick), so the queue doesn't grow unboundedly in normal operation. The `let _ =` on send is a legitimate concern since a dropped receiver means events are silently lost with […]

> AGENT

All four council agents have reported. Here's the final consolidated ruling:

---

## Council Verdict: **CONDITIONAL**

### Validator Corrections

The validator **rejected 1 finding** and **adjusted severities** on several others:

| Finding | Reviewer Severity | Validated Severity | Notes |
|---------|------------------|-------------------|-------|
| Unbounded channel | CRITICAL/HIGH | **MEDIUM** | LLM output throughput is naturally bounded; not "millions of envelopes" |
| Zombie tasks on spawn fail | HIGH | **FALSE POSITIVE** | `spawn_prepared` already transitions to Failed internally |
| JSON parse fallback | HIGH | **LOW/MEDIUM** | Same behavior as pre-existing code; intentional design |
| JoinHandle discarded | HIGH | **MEDIUM** | Panic risk low; real issue is inability to join |
| Mutex expect | MEDIUM | **LOW** | Accepted Rust pattern for infallible inner ops |

### MUST FIX before merge (2 items)

| # | Finding | Why |
|---|---------|-----|
| **1** | **Orchestrator lock held per-envelope during drain** (task_manager.rs:173-193, 494-514) — N mutex acquisitions + spawn_blocking per drain cycle | Serializes the daemon under any real load. Batch writes under a single lock acquisition. |
| **2** | **Non-TaskOutput events silently dropped** (io.rs:82-88) — AssistantText, Thinking, ToolCall, SessionCaptured, FinalPayload all discarded | Functional […]