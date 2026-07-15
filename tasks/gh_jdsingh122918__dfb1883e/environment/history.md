> DEVELOPER

### Relevant File Paths

- `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/recovery.rs` -- untested recovery logic (gap 2a)
- `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/task_manager.rs` -- untested completion lifecycle (gap 2b)
- `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/run_orchestrator.rs` -- untested state machine guards (gaps 2c, 3a, 3b)
- `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/server.rs` -- untested stop_run with TaskManager, pagination, workspace validation (gaps 3c, 3e, 3f)
- `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/tests/event_streaming.rs` -- strongest test file with ManagedRuntimeServer
- `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/tests/approval_rpcs.rs` -- exemplary approval lifecycle coverage
- `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/scheduler.rs` -- well-tested inline unit tests</result>
<usage><total_tokens>127144</total_tokens><tool_uses>28</tool_uses><duration_ms>117742</duration_ms></usage>
</task-notification>
Full transcript available at: /private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/a846f7e84af7184e0.output

> DEVELOPER

### 5. Positive Observations

- **Approval lifecycle is thoroughly tested**: The `approval_rpcs.rs` suite covers the full approve/deny/idempotency/not-found cycle with assertions on both the gRPC response and persisted state store. The double-resolution test (`resolve_approval_second_attempt_returns_not_found_and_leaves_first_result_intact`) is particularly good at catching concurrency bugs.

- **Event streaming correctness is well-validated**: The `event_streaming.rs` tests verify cursor alignment between `attach_run` and `stream_task_output`, event ordering, run-scoped filtering, type filtering, live-tail delivery, and replay. The `real_runtime_task_output_streams_live_and_replays` test is a strong end-to-end integration test that exercises real process execution through the `ManagedRuntimeServer`.

- **Idempotency is consistently tested**: Both `kill_task` and `stop_run` have explicit idempotency tests, which prevents a common class of double-action bugs.

- **Persistence verification is systematic**: Tests consistently verify both the gRPC response and the durable `StateStore` state, catching bugs where in-memory state diverges from persisted state.

- **Scheduler has clean inline unit tests**: The `scheduler.rs` inline tests cover ready-task enqueuing, dependency-blocked skipping, paused-run ignoring, and event emission -- all with in-memory state stores, making them fast and deterministic.

- **Shutdown coordinator tests use a well-designed fake supervisor**: The `shutdown.rs` tests use `FakeSupervisor` with configurable `clear_on_graceful`/`clear_on_force` flags, enabling clean testing of the graceful->force->remaining pipeline without real processes.

- **Server startup edge cases are covered**: The stale socket […]

> DEVELOPER

### 4. Test Quality Issues

**4a. Test harness duplication**: The `TestServer` struct and its helper functions (`make_budget`, `make_plan`, `make_milestone`, `make_task`) are duplicated across 5 of the 7 test files (`control_rpcs.rs`, `event_streaming.rs`, `grpc_health.rs`, `query_rpcs.rs`, `submit_run.rs`). This is a maintenance burden -- if the server startup sequence changes, all copies must be updated. A shared test harness module (e.g., `tests/common/mod.rs`) would reduce this risk.

**4b. Direct state mutation in test setup**: The `approval_rpcs.rs` and `create_child_task.rs` harnesses directly mutate orchestrator internals (e.g., `parent.status = TaskStatus::Running { ... }`, `parent.profile.manifest.permissions.spawn_limits.max_children = max_children`) rather than going through the public API. This makes the tests somewhat coupled to internal structure. However, this is a reasonable pragmatic choice given that the test infrastructure cannot easily spawn real running agents in unit tests.

**4c. Socket readiness polling in `TestServer::start()`**: The `grpc_health.rs` and `control_rpcs.rs` versions of `TestServer::start()` poll for socket existence 40 times with 25ms sleep (1 second total) without checking if the handle has finished. The `event_streaming.rs` version is more robust -- it polls 200 times and checks `handle.is_finished()` to fail fast if the server panics. The weaker versions in other test files could cause flaky test timeouts on slow CI.

> DEVELOPER

### 3. Important Improvements (Criticality 5-7)

**3a. `create_child_task` when parent hit hard limit (`max_children` reached) -- Criticality: 7/10**

The `create_child_task.rs` tests exercise:
- Successful creation under soft cap (max_children=5, require_approval_after=5)
- Approval-gated creation after soft cap (max_children=5, require_approval_after=1)
- Not-found for missing parent

But no test verifies the hard limit case -- what happens when the parent has already spawned `max_children` children? The function `check_spawn_limits` (referenced at run_orchestrator.rs line 474) is exercised for the approval path but not for the rejection path. If the hard limit returns an error, there should be a test confirming it returns `FailedPrecondition` or `ResourceExhausted`.

**3b. `create_child_task` when run is not Running -- Criticality: 7/10**

The source code at run_orchestrator.rs line 441 explicitly checks `if run.status != RunStatus::Running` and returns `FailedPrecondition`. No test exercises this guard. A regression would allow child tasks to be created in cancelled/completed runs.

**3c. `stop_run` with active tracked agents (TaskManager integration) -- Criticality: 6/10**

The `control_rpcs.rs` `stop_run_cancels_run_and_leaves_no_active_tasks` test exercises the gRPC path but only through a server without a TaskManager. The server.rs `stop_run` implementation (lines 335-378) has a branch specifically for killing tracked runtime agents before orchestrator-level cancellation. This branch is never exercised because `TestServer::start()` uses `run_server` which creates the […]

> DEVELOPER

### 2. Critical Gaps (Criticality 8-10)

**2a. Recovery module (`recovery.rs`) has no integration or unit tests -- Criticality: 9/10**

The `recover_orphans` and `rebuild_run_graph` functions contain approximately 600 lines of logic covering:
- Reconciling stale tasks (pending, running, materializing) against live agents
- Marking unrecoverable tasks as Failed
- Reconstructing `RunState` from serialized `TaskNodeRow` and `RunRow` data including approval state, milestone status, budget envelopes, worktree plans, and capability envelopes
- Emitting `DaemonRecovered` events
- WAL checkpointing

The `grpc_health.rs` test `restart_preserves_persisted_runs_via_server_bootstrap` exercises the end-to-end restart path but only verifies that the run and tasks are queryable after restart -- it does not test:
- Tasks that were Running at shutdown being correctly failed or reattached
- AwaitingApproval tasks surviving recovery with approvals intact
- Multiple runs in mixed states recovering correctly
- Corrupted or partially-written task rows during recovery
- Runs that should transition from Running to Failed/Cancelled during reconciliation

**Why it matters**: Daemon crashes are the exact scenario where data integrity bugs surface. A regression in `reconstruct_task_node` (line 411-451 of recovery.rs) or `reconcile_run_status` (line 187-208) could silently corrupt run state on every daemon restart.

**2b. Task completion lifecycle via `check_agent_status` -- Criticality: 8/10**

`TaskManager::check_agent_status` (task_manager.rs, lines 330-412) contains the critical logic […]

> DEVELOPER

## Test Coverage Analysis: `runtime-daemon-dispatch` PR

### 1. Summary

The test suite for the `forge-runtime` crate is **well-structured and covers the primary gRPC contract thoroughly**. There are 7 integration test files with approximately 25 test cases, plus inline unit tests in `scheduler.rs`, `shutdown.rs`, and `runtime/mod.rs`. The tests exercise the key gRPC RPCs via real Unix socket connections, validate both happy paths and error conditions, check state persistence across restarts, and verify event streaming behavior including live-tail, replay, filtering, and cursor alignment.

The most significant coverage gaps are in the **recovery module**, **task manager lifecycle paths**, and **run orchestrator state machine transitions** -- areas where production bugs would cause data loss or silent corruption.

> DEVELOPER

## Summary of Findings

| Severity | Count | Key Themes |
|----------|-------|------------|
| CRITICAL | 3 | Silent output loss, stuck tasks from dispatch failures, NoopAgentSupervisor in production |
| HIGH | 3 | No circuit breaker on lifecycle loop, scheduler gives up silently, force_stop == graceful_stop |
| MEDIUM | 7 | PID overflow, phantom agent IDs, fabricated approval IDs, leaked containers, insecure defaults |

The most urgent fixes are Issues 1-3 (CRITICAL), which represent genuinely silent failure modes that would cause users significant confusion in production. Issue 2 in particular can cause infinite retry loops, and Issue 3 means the `run_server` convenience function is structurally broken for real agent management.</result>
<usage><total_tokens>159592</total_tokens><tool_uses>26</tool_uses><duration_ms>153200</duration_ms></usage>
</task-notification>
Full transcript available at: /private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/adc5331c1a1f1c367.output

> DEVELOPER

## Positive Observations

While the issues above are concerning, several patterns in this codebase demonstrate good error handling discipline:

1. **Consistent use of `.with_context()`**: Nearly every `?` propagation includes a `.with_context()` annotation with relevant IDs and operation names. This is excellent for debugging.

2. **Event stream error handling**: The `EventStreamCoordinator` properly sends gRPC `Status::internal` errors to stream consumers when database queries fail, rather than silently dropping the stream.

3. **Recovery module**: The `recover_orphans` and `rebuild_run_graph` functions properly validate database integrity (e.g., rejecting `Running` tasks without `assigned_agent_id`) and surface structural errors rather than papering over them.

4. **Spawn failure rollback**: The `spawn_prepared` method in `TaskManager` correctly transitions tasks to `Failed` when the runtime spawn fails, and also rolls back by killing the agent if post-spawn state updates fail.

5. **gRPC input validation**: The server validates all incoming proto fields (empty strings, missing required fields, unknown enum values) with specific `Status::invalid_argument` errors.

6. **No empty catch blocks**: I found zero instances of empty error handling blocks in the Rust code.

> DEVELOPER

### Issue 13: Approval state fallback parsing silently invents approval IDs

**Location:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/recovery.rs`, lines 573-611

**Severity:** MEDIUM

**Issue Description:** When strict approval-state deserialization fails, the code falls through to a legacy format parser. If the legacy format has a `pending` state but no `approval_id`, it silently invents one: `"recovered-approval"`. This means a recovered pending approval will have a fabricated ID that does not match any approval in the actual approval registry, making it unresolvable.

```rust
"pending" => Ok(ApprovalState::Pending {
    approval_id: ApprovalId::new(
        legacy.get("approval_id")
            .and_then(serde_json::Value::as_str)
            .unwrap_or("recovered-approval"),
    ),
}),
```

**User Impact:** A recovered pending approval cannot be resolved via the API because the approval ID does not match. The task is stuck in `AwaitingApproval` forever.

**Recommendation:** Log a warning when falling back to a fabricated approval ID, and ensure the fabricated approval is registered in the run's approval map so it can actually be resolved.

> DEVELOPER

### Issue 12: `send_signal` treats ESRCH as success

**Location:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/runtime/host.rs`, lines 203-215 (duplicated in `bwrap.rs`)

**Severity:** MEDIUM

**Issue Description:** When `kill()` returns `ESRCH` (process does not exist), `send_signal` returns `Ok(())`. This is intentional for the kill path (the process is already dead), but in the `kill` method of `HostRuntime` (line 155), this means the subsequent `child.wait()` at line 159 may wait indefinitely on a process that has already been reaped. The code is structured to handle this because `wait()` should return immediately for an already-reaped process, but the silent success could mask issues where the tracked child handle belongs to a different process.

**User Impact:** Minor, as the tracked child handle provides protection. But the lack of logging means that operators cannot tell from logs whether the SIGTERM was actually delivered.

> DEVELOPER

### Issue 11: `RuntimeService` defaults to `Host` backend and `insecure=true` when task_manager is None

**Location:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/server.rs`, lines 122-136

**Severity:** MEDIUM

**Issue Description:** When `task_manager` is `None`, the service reports the runtime backend as `Host` and `insecure_host_runtime` as `true`:

```rust
fn runtime_backend_proto(&self) -> i32 {
    let backend = self.task_manager.as_ref()
        .map(|manager| manager.runtime_backend())
        .unwrap_or(forge_common::run_graph::RuntimeBackend::Host);
    // ...
}

fn insecure_host_runtime(&self) -> bool {
    self.task_manager.as_ref()
        .map(|manager| manager.insecure_host_runtime())
        .unwrap_or(true)
}
```

This silently falls back to reporting the daemon as running in insecure host mode. Clients checking these fields will not know whether this is the actual backend or a default. This couples with Issue 3 -- the `run_server` path passes `None` for task_manager.

**User Impact:** Clients may see the daemon as running in insecure host mode when it is actually not managing agents at all. Security-conscious clients may refuse to connect based on a false report.

**Recommendation:** Either require `task_manager` to always be present, or return a distinct value (e.g., `RuntimeBackend::Unspecified`) when the task manager is not configured.

> DEVELOPER

### Issue 10: `best_effort_remove_container` logs at `debug` and suppresses cleanup failures

**Location:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/runtime/docker.rs`, lines 174-189

**Severity:** MEDIUM

**Issue Description:** When Docker container cleanup fails, the error is logged at `debug` level, which is typically not visible in production:

```rust
async fn best_effort_remove_container(&self, container_id: &str) {
    if let Err(error) = self.client.remove_container(...).await {
        tracing::debug!(
            container_id = %container_id,
            error = %error,
            "best-effort Docker container cleanup failed"
        );
    }
}
```

This is called when a container fails to start (line 321). A leaked container consumes Docker resources indefinitely with no indication at the normal log level.

**User Impact:** Containers accumulate silently, consuming memory and disk space. The operator has no visibility unless they check debug-level logs.

**Recommendation:** Log at `warn` level at minimum. Also consider emitting a runtime event so monitoring can detect leaked containers.

> DEVELOPER

### Issue 9: `agent_id` defaults to empty string on missing agent_id in task-output events

**Location:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/state/events.rs`, line 291

**Severity:** MEDIUM

**Issue Description:** When decoding a task-output event, a missing `agent_id` is replaced with an empty-string `AgentId`:

```rust
agent_id: runtime_event.agent_id.unwrap_or_else(|| AgentId::new("")),
```

This creates a phantom agent ID that will not match any real agent. Downstream consumers correlating output events with agent instances will silently fail to find a match. This should be an error for `TaskOutput` events, which should always have an `agent_id`.

**User Impact:** Output events silently lose their agent attribution, making it impossible to correlate output with the specific agent that produced it.

**Recommendation:** Return an error instead of defaulting:

```rust
agent_id: runtime_event.agent_id.ok_or_else(|| 
    anyhow!("task-output row missing agent_id at seq {}", self.seq)
)?,
```

> DEVELOPER

### Issue 8: `pid as i32` cast in `send_signal` can overflow

**Location:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/runtime/host.rs`, line 204 (duplicated in `bwrap.rs` line 367)

**Severity:** MEDIUM

**Issue Description:** The PID is passed as `u32` and then cast to `i32` via `pid as i32`. If the PID exceeds `i32::MAX` (unlikely but possible on some systems), this wraps around silently and sends a signal to the wrong process or PID 0 (which signals the entire process group).

**User Impact:** Sending a signal to PID 0 would kill the entire process group of the daemon.

**Recommendation:** Use `i32::try_from(pid)` and return an error if the conversion fails:

```rust
let pid_i32 = i32::try_from(pid)
    .with_context(|| format!("pid {pid} exceeds i32 range"))?;
```

> DEVELOPER

## MEDIUM Issues

### Issue 7: `process_exists` returns `true` for EPERM -- incorrect when PID recycling occurs

**Location:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/runtime/host.rs`, lines 217-225 (duplicated in `bwrap.rs` lines 380-388)

**Severity:** MEDIUM

**Issue Description:** The `process_exists` function treats `EPERM` as evidence the process exists:

```rust
fn process_exists(pid: u32) -> bool {
    let rc = unsafe { libc::kill(pid as i32, 0) };
    if rc == 0 { return true; }
    let error = std::io::Error::last_os_error();
    matches!(error.raw_os_error(), Some(libc::EPERM))
}
```

When `HostRuntime::status` calls this function (line 195-199), it returns `AgentStatus::Running` if the PID exists but is owned by a different user. If PID recycling has occurred (the agent process exited and a new unrelated process took the same PID), this will incorrectly report a dead agent as running. The task will never be finalized.

**User Impact:** In rare PID recycling scenarios, a task is stuck in `Running` status forever, attached to a process that is not the agent.

**Recommendation:** This is inherently racy, but the risk can be mitigated by preferring the `TrackedChild` path (which owns the process handle). The `process_exists` fallback path should be documented as best-effort and used only when the tracked child is missing. Consider also checking the process start time or command line […]

> DEVELOPER

### Issue 6: `force_stop` delegates to `graceful_stop` with no escalation

**Location:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/task_manager.rs`, lines 610-613

**Severity:** HIGH

**Issue Description:** The `AgentSupervisor` implementation for `TaskManager` has `force_stop` simply delegate to `graceful_stop`:

```rust
async fn force_stop(&self, agent: &ActiveAgent, reason: &str) -> Result<()> {
    self.graceful_stop(agent, reason).await
}
```

The shutdown coordinator calls `force_stop` specifically when `graceful_stop` has already been attempted and the grace period has expired. By making these identical, there is no escalation path. If `graceful_stop` fails (e.g., the process ignores SIGTERM), `force_stop` will also fail in the same way. The underlying `kill_agent` -> `runtime.kill()` in `HostRuntime` does have a SIGTERM->wait->SIGKILL fallback, so the escalation is in the runtime layer, not the supervisor layer. This is somewhat mitigated but the contract violation is concerning -- the shutdown coordinator's architecture expects these to be genuinely different operations.

**User Impact:** On poorly-behaving agents, the shutdown coordinator's two-phase stop sequence is effectively a single phase, potentially extending shutdown time or leaving zombie processes.

**Recommendation:** At minimum, document why this delegation is intentional. Ideally, `force_stop` should use a more aggressive kill mechanism (immediate SIGKILL without the graceful SIGTERM phase).

> DEVELOPER

### Issue 5: Scheduler swallows ready-task computation errors and continues

**Location:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/scheduler.rs`, lines 57-66

**Severity:** HIGH

**Issue Description:** When `run.get_ready_tasks()` fails, the scheduler logs at `error` level and skips the run:

```rust
Err(error) => {
    tracing::error!(
        %error,
        run_id = %run_id,
        "scheduler skipped run after ready-task computation failed"
    );
    continue;
}
```

This means a structurally invalid run graph (e.g., circular dependencies, missing task nodes referenced in depends_on) will cause the scheduler to permanently skip that run on every tick. The run stays in `Running` status forever, and the user has no indication that the scheduler has given up on it.

**Hidden Errors:** Circular dependency cycles introduced by `create_child_task`, corrupted task graph state, data races between concurrent mutations.

**User Impact:** A run appears stuck in `Running` status with no progress. The user must scan daemon logs to find the error. No API or event surfaces this failure.

**Recommendation:** After a configured number of consecutive scheduling failures for a run, emit a `ServiceEvent` or `PolicyViolation` runtime event visible to stream consumers, and consider transitioning the run to `Failed`.

> DEVELOPER

## HIGH Issues

### Issue 4: Lifecycle loop errors are logged but never surfaced to users or trigger backoff

**Location:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/main.rs`, lines 137-155

**Severity:** HIGH

**Issue Description:** The main lifecycle loop runs every 250ms and calls three operations. Each one catches errors with `tracing::warn!` and continues:

```rust
if let Err(error) = lifecycle_manager.drain_runtime_output().await {
    tracing::warn!(%error, "task-manager output drain cycle failed");
}
if let Err(error) = lifecycle_manager.dispatch_enqueued_tasks().await {
    tracing::warn!(%error, "task-manager dispatch cycle failed");
}
if let Err(error) = lifecycle_manager.poll_active_agents().await {
    tracing::warn!(%error, "task-manager poll cycle failed");
}
```

If the SQLite database becomes corrupted, or the disk is full, or the mutex is poisoned, these operations will fail every 250ms, flooding logs with identical warn messages forever. There is no circuit breaker, no backoff, no escalation to `error` level after repeated failures, and no notification to the gRPC health endpoint that the daemon is in a degraded state.

**Hidden Errors:** Database corruption, disk full, mutex poisoning, any persistent infrastructure failure.

**User Impact:** The daemon appears healthy via gRPC health checks while it is actually unable to manage any tasks. Log files grow unboundedly with repeated warn messages.

**Recommendation:** Implement a consecutive failure counter. After N consecutive failures (e.g., 10), escalate to `tracing::error!`, mark […]

> DEVELOPER

### Issue 3: `NoopAgentSupervisor` used in production `run_server` path

**Location:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/server.rs`, lines 150, 64-72 and `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/shutdown.rs`, lines 40-56

**Severity:** CRITICAL

**Issue Description:** The `run_server` function (lines 144-185 in server.rs) and the default `RuntimeService::new` constructor both use `NoopAgentSupervisor`. This is a stub that always returns an empty list of active agents, and its `graceful_stop` / `force_stop` methods are no-ops. In the `run_server` path, this means:

1. Recovery on startup (`recover_orphans`) will see zero live agents and mark ALL actively-running tasks as `Failed`.
2. Shutdown coordination will believe there are zero agents to stop, skip all agent termination logic, and immediately finalize runs.

The `NoopAgentSupervisor` is documented as "Default supervisor used until real runtime-owned agent processes exist" -- but the real `TaskManager` now implements `AgentSupervisor`. The `run_server` path does not use the `TaskManager` at all (passes `None` for task_manager). This means the `run_server` entry point is structurally incapable of properly managing agent lifecycle.

**Hidden Errors:** Any caller using `run_server` instead of `run_server_with_components` gets a daemon that silently fails to stop agents on shutdown and silently fails to reattach agents on recovery.

**User Impact:** Agents are orphaned on shutdown. Tasks are incorrectly marked as failed on restart even if their agents are still […]

> DEVELOPER

### Issue 2: Spawned task dispatch continues after spawn failure without marking task as failed

**Location:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/task_manager.rs`, lines 222-233

**Severity:** CRITICAL

**Issue Description:** In `dispatch_enqueued_tasks`, when `spawn_prepared` fails, the error is logged at `warn` but the task is NOT transitioned to a failed state. The code merely `continue`s to the next task:

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

If `spawn_prepared` fails after already transitioning the task to `Materializing` but before successfully transitioning back to `Failed` internally (which happens inside `spawn_prepared` for the initial spawn failure, but not for ALL failure paths), the task is left stuck in `Materializing` state forever. More importantly, if `spawn_prepared` returns an error for a reason outside the runtime spawn (e.g., the `ensure_spawnable_task` check), the task remains `Enqueued` and will be retried on the next scheduler tick -- potentially causing an infinite retry loop with warn-level log spam and no circuit breaker.

**Hidden Errors:** Network transient errors, resource exhaustion, repeated configuration errors that cause indefinite retry loops.

**User Impact:** A task silently enters an infinite retry loop, consuming resources and filling logs, with no way […]

> DEVELOPER

## CRITICAL Issues

### Issue 1: Silent fire-and-forget of runtime output channel sends

**Location:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/runtime/io.rs`, line 48

**Severity:** CRITICAL

**Issue Description:** The `RuntimeOutputSink::emit()` method silently discards errors when sending runtime output events via the unbounded channel:

```rust
fn emit(&self, envelope: RuntimeOutputEnvelope) {
    if let Some(tx) = &self.tx {
        let _ = tx.send(envelope);
    }
}
```

The `let _ = tx.send(envelope)` discards the `SendError` without any logging. If the receiver is dropped (because the drain task panicked, was cancelled, or the channel was closed), every subsequent output event -- stdout lines, stderr lines, token usage updates, session captures, tool calls, assistant text -- is silently discarded. The user sees no output from their agent and has no indication why.

**Hidden Errors:** Receiver-side panic, premature channel closure, task manager shutdown ordering bugs that drop the receiver before all output is flushed.

**User Impact:** Agent output disappears without explanation. The task appears to run but produces no visible output. Debugging this requires knowing to check whether the mpsc receiver is still alive, which is non-obvious.

**Recommendation:** At minimum, log at `debug` or `warn` level when the send fails, including the task_id and agent_id context. Ideally, the first occurrence should log at `warn` to […]

> DEVELOPER

# Error Handling Audit: `runtime-daemon-dispatch` PR

## Executive Summary

This PR adds a substantial `forge-runtime` crate with ~15,000 lines of new production code. The error handling is generally above average -- most error paths use `anyhow::Context`, propagate errors with `?`, and include contextual information. However, I found several significant issues that range from silent failures to inappropriate fallbacks that could cause debugging nightmares in production.

> DEVELOPER

### Summary

The codebase is well-structured overall with thorough error handling using `.context()`, proper use of `spawn_blocking` for most SQLite operations, comprehensive test coverage, and a clean separation between the gRPC layer, orchestration, task management, and state persistence. The profile compiler has a solid security model with fail-closed validation of untrusted overlays. The event streaming architecture with cursor-based replay is well-designed.

The one critical finding is a CLAUDE.md violation: a blocking `std::sync::Mutex` acquisition + synchronous SQLite query on a tokio worker thread in the `pending_approvals` gRPC handler. This should be wrapped in `spawn_blocking` to match the pattern used everywhere else in the crate. The two important findings are code quality issues in pagination token semantics and confusing variable aliasing that could lead to future bugs.</result>
<usage><total_tokens>164174</total_tokens><tool_uses>49</tool_uses><duration_ms>177637</duration_ms></usage>
</task-notification>
Full transcript available at: /private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/a8288beb63222ca28.output

> DEVELOPER

### Important (80-89)

**2. Pagination next_page_token uses wrong index -- returns second-to-last page item when exactly one more page remains** (Confidence: 82)

File: `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/server.rs`, lines 418-421 and 497-502

The `next_page_token` is set to `runs.get(end_index - 1)` (the last item of the current page). When the client sends this back, `page_start_index_for_runs` finds that item and returns `position + 1`. This works correctly for cursor-based pagination **but only if item IDs are stable and unique across calls**. Since the runs list is filtered and sorted in-memory from the `RunOrchestrator`'s `HashMap`, and new runs can be inserted between calls, the page token could point to an item that has shifted position or disappeared, causing `invalid run page token` errors. This is a known limitation of cursor-based pagination over in-memory collections rather than database-backed cursors.

However, the more concerning issue is that the same pattern is applied for `list_tasks` and here the `next_page_token` should semantically point to the element **after** the last returned item (the element at `end_index`), not the last returned element. The current approach conflates the "last seen" cursor with the "resume from" point -- it happens to work only because `page_start_index_for_*` adds 1. This is fragile and confusing. Consider using `end_index` […]

> DEVELOPER

### Critical (90-100)

**1. Blocking synchronous database call inside async gRPC handler violates CLAUDE.md** (Confidence: 95)

File: `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/server.rs`, line 657

CLAUDE.md rule: "Use tokio for all async -- never block in async code"

The `pending_approvals` handler calls `self.state_store.latest_seq()` directly, which internally calls `with_connection()`, acquiring a `std::sync::Mutex` lock and performing synchronous SQLite I/O on the tokio worker thread. Every other state store call from async code in this crate correctly wraps the work in `tokio::task::spawn_blocking`.

```rust
let fence = self
    .state_store
    .latest_seq()
    .map_err(|error| Status::internal(format!("failed to load approval fence: {error}")))?;
```

Fix: Wrap in `spawn_blocking`, similar to how `counts()` is implemented in `state/mod.rs`:

```rust
let state_store = Arc::clone(&self.state_store);
let fence = tokio::task::spawn_blocking(move || state_store.latest_seq())
    .await
    .map_err(|error| Status::internal(format!("approval fence task failed: {error}")))?
    .map_err(|error| Status::internal(format!("failed to load approval fence: {error}")))?;
```

> DEVELOPER

## Code Review: `runtime-daemon-dispatch` PR

**Reviewing files across:**
- `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/` (server.rs, run_orchestrator.rs, task_manager.rs, event_stream.rs, scheduler.rs, main.rs, lib.rs, shutdown.rs, recovery.rs, profile_compiler.rs)
- `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/state/` (mod.rs, schema.rs, events.rs, runs.rs, tasks.rs, agent_instances.rs)
- `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/runtime/` (mod.rs, io.rs, host.rs, docker.rs, bwrap.rs)
- `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/events.rs`

> DEVELOPER

**Positive Findings**

- `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/events.rs:1-8`: The module-level doc comment excellently explains the purpose of runtime events and lists four concrete use cases (CLI attach/detach, Factory UI, audit trail, daemon restart recovery). This provides high-value context for future maintainers.

- `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/runtime.rs:1-9`: The module doc on `AgentRuntime` trait clearly explains what the trait abstracts over, why it exists, and what each backend is responsible for. The numbered contract in `spawn()`'s doc comment (lines 126-135) is a strong example of documenting behavioral requirements.

- `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/runtime.rs:113-121`: The trait-level doc listing all three implementations (`BwrapRuntime`, `DockerRuntime`, `HostRuntime`) with their platform context and the daemon's selection mechanism is valuable navigational documentation.

- `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/state/mod.rs:32-35`: The `StateStore::open` doc comment accurately describes the three initialization steps (WAL mode, foreign keys, schema creation) and matches the implementation exactly.

- `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/recovery.rs:44`: The doc on `recover_orphans` accurately describes its role: "Reconcile stale non-terminal tasks and runs before the daemon starts serving."

- `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/shutdown.rs:66`: The doc on `ShutdownCoordinator` ("Coordinates daemon shutdown against scheduler and runtime-owned agents") is concise and accurately reflects the implementation.

- The field-level documentation throughout `RuntimeEventKind` in `events.rs` is thorough and accurate. Every variant has a clear, non-redundant comment explaining its purpose, and the field comments provide useful context about the […]

> DEVELOPER

**Recommended Removals**

13. **Location**: `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/run_orchestrator.rs:74`
    - **Rationale**: `/// Create a new empty orchestrator.` on `RunOrchestrator::new` restates what the constructor name already conveys. The method signature (`state_store`, `event_stream`) makes the inputs obvious. This comment adds no value.

14. **Location**: `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/task_manager.rs:45-46`
    - **Rationale**: `/// Create an empty agent tracker.` on `AgentTracker::new()` restates what `new()` and `Default` already convey. This is trivially obvious.

15. **Location**: `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/event_stream.rs:46`
    - **Rationale**: `/// Create a new coordinator backed by the shared runtime state store.` on `EventStreamCoordinator::new(state_store)` restates what the constructor signature already conveys perfectly.

> DEVELOPER

**Improvement Opportunities**

4. **Location**: `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/recovery.rs:28`
   - **Current state**: `RecoveryResult` has a field `stale_sockets_cleaned` which is always set to `0` at line 78 (`result.stale_sockets_cleaned = 0;`). The struct exposes this field publicly but no code ever populates it with a meaningful value. The doc comment on `RecoveryResult` at line 28 says "Aggregate result of reconciling durable task/run state on daemon startup" -- which is accurate, but the struct contains dead data.
   - **Suggestion**: Either remove the `stale_sockets_cleaned` field since it is unused, or add a `// TODO: implement socket cleanup during recovery` comment next to the hardcoded `0` assignment so future maintainers know this is a planned feature, not a bug.

5. **Location**: `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/recovery.rs:33`
   - **Current state**: The field `tasks_left_pending` is populated from `queued.len()` where `queued` is `query_tasks_by_status(&["Pending", "Enqueued"])`. The field name says "pending" but it actually counts both Pending and Enqueued tasks. This is mildly misleading.
   - **Suggestion**: Rename to `tasks_left_schedulable` or update the doc comment with `/// Number of tasks left in Pending or Enqueued state (not needing recovery action).`

6. **Location**: `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/runtime/mod.rs:3-4`
   - **Current state**: The module doc says "Plan 4 freezes the backend-facing launch contract, then layers secure runtime backends and fail-closed backend selection on top." This […]

> DEVELOPER

**Critical Issues**

1. **Location**: `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/runtime.rs:89`
   - **Issue**: The doc comment on `AgentStatus::Exited` says "The agent exited successfully (exit code 0)." However, the `exit_code` field is `i32` and the `status_from_exit_status` function in `crates/forge-runtime/src/runtime/io.rs:257-261` maps any `exit_status.success()` to `Exited`, which on most systems means exit code 0 -- but the struct carries an arbitrary `i32`. The comment misleadingly implies exit code is always 0, when the variant is capable of carrying any code. More importantly, the Docker runtime (`docker.rs:500`) explicitly constructs `Exited { exit_code: 0 }` only for zero, but the data type does not enforce this constraint. The comment should say "The agent exited with a successful status" rather than hardcoding "exit code 0," since the field exists to carry the actual exit code.
   - **Suggestion**: Change to `/// The agent exited with a successful exit status.`

2. **Location**: `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/run_orchestrator.rs:1`
   - **Issue**: The module-level doc comment says `//! Minimal SubmitRun orchestration over the durable state store.` This is inaccurate. The module is 2,604 lines containing 22+ public methods spanning run submission, task lifecycle transitions, child task creation, approval resolution, task killing, run cancellation, run failure, event emission, result summary updates, and multi-agent event recording. Calling this "minimal SubmitRun orchestration" significantly understates […]

> DEVELOPER

**Summary**

I analyzed all code comments across the 15 key files in this PR, cross-referencing each comment against the actual implementation. The codebase is generally well-documented with accurate structural and API-level comments. However, I found several issues ranging from factually misleading comments to comments that will quickly become stale as this code evolves. Below are the findings organized by severity.

> DEVELOPER

## Summary Ratings

| Type Family | Encapsulation | Expression | Usefulness | Enforcement |
|---|---|---|---|---|
| ID Newtypes | 7 | 6 | 9 | 5 |
| BudgetEnvelope | 3 | 5 | 8 | 4 |
| TaskStatus/RunStatus | 7 | 8 | 9 | 5 |
| RunState/RunGraph | 2 | 6 | 9 | 4 |
| RuntimeEvent/EventKind | 4 | 8 | 7 | 3 |
| BusMessage | 3 | 5 | 6 | 2 |
| AgentHandle | 2 | 3 | 8 | 2 |
| Policy hierarchy | 3 | 6 | 8 | 3 |
| State Store rows | 5 | 4 | 7 | 6 |
| AgentRuntime trait | 6 | 7 | 8 | 5 |
| Proto conversion | 8 | 9 | 9 | 9 |

**Top 3 highest-impact improvements:**

1. **Encapsulate `BudgetEnvelope`** -- make `consumed`, `subtree_consumed` private; replace `remaining` with a computed method. This eliminates the most dangerous redundant source of truth.

2. **Encapsulate `RunState`** -- make `tasks`, `status`, `milestones`, `approvals` non-pub; force all mutations through methods that validate invariants.

3. **Restructure `AgentHandle`** as an enum -- make the backend-specific data (pid […]

> DEVELOPER

## Cross-Cutting Concerns

### 1. The pub-field pattern is pervasive and is the PR's primary type design weakness

Nearly every struct in the PR has all-pub fields. This is understandable for a first implementation -- it reduces friction -- but it means that invariants documented in method contracts and doc comments are advisory rather than enforced. The types where this matters most, in priority order:

1. **`BudgetEnvelope`** -- the `remaining` derived field is trivially desynchronizable
2. **`RunState`** -- the central state machine with multiple interrelated invariants
3. **`TaskNode`** -- the durable unit of work whose status, approval, and agent assignment must be coordinated
4. **`AgentHandle`** -- backend-specific data should be an enum, not optional fields

### 2. State machine transitions are underchecked

`TaskStatus` and `RunStatus` both represent state machines with defined lifecycles, but neither enforces valid transitions. Adding a `can_transition_to()` check is low-cost and high-value.

### 3. The proto conversion layer is the strongest part of the type system

The `forge-proto/src/convert` module is the best-designed component in the PR. It correctly treats the proto boundary as a trust boundary, validates everything, uses macros for consistency, and has excellent test coverage. The rest of the type system would benefit from applying […]

> DEVELOPER

## Type: Proto/Domain Conversion Layer

**Files**: `/Users/jdsingh/Projects/AI/forge/crates/forge-proto/src/convert/`

### Invariants Identified
- Proto `*_UNSPECIFIED` (value 0) is always rejected on decode
- Negative integers from proto are rejected with `ConversionError::NegativeValue`
- Overflow from u64 to i64 is rejected with `ConversionError::OutOfRange`
- Required proto sub-messages are checked with `require_message()`
- Memory size strings are parsed with explicit suffix handling
- Blank proto IDs are rejected

### Ratings
- **Encapsulation**: 8/10
  The conversion layer is well-structured. `TryFromProto` and `IntoProto` traits define the contract. The `impl_enum_convert!` macro ensures consistent bidirectional conversion for all enums.

- **Invariant Expression**: 9/10
  The `ConversionError` enum clearly enumerates all possible failure modes. The macro-based enum conversion ensures that every domain variant maps to exactly one proto variant and vice versa. The `BudgetPolicyDefaults` type explicitly names the policy-dependent defaults that cannot come from the proto message.

- **Invariant Usefulness**: 9/10
  This layer is the trust boundary between untrusted gRPC input and trusted domain types. Every validation here prevents a class of bugs downstream.

- **Invariant Enforcement**: 9/10
  Excellent enforcement. `UNSPECIFIED` values are rejected. Negative integers are caught. Missing required fields are caught. Unsupported budget fields are explicitly rejected with clear error messages. The `initial_budget_from_proto` function even rejects non-zero `max_children`, `require_approval_after`, […]

> DEVELOPER

## Type: RunGraph

**File**: `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/run_graph.rs` (lines 20-49)

### Invariants Identified
- `runs` HashMap keys must equal `RunState::id` for each entry
- Only one `RunGraph` should exist in the daemon (singleton)

### Ratings
- **Encapsulation**: 4/10
  The `runs` field is pub. The `insert_run()` method correctly uses `run.id.clone()` as the key, but external code can bypass it.

- **Invariant Expression**: 4/10
  The type is essentially a `HashMap<RunId, RunState>` with no additional structure.

- **Invariant Usefulness**: 5/10
  The wrapper provides a convenient named type rather than a bare HashMap, but adds minimal semantic value.

- **Invariant Enforcement**: 4/10
  `insert_run()` correctly derives the key from the run's ID, maintaining key-value consistency. But since `runs` is pub, this can be bypassed.

### Recommended Improvements
- Make `runs` non-pub and add a `pub fn runs(&self) -> &HashMap<RunId, RunState>` read-only accessor. Mutation should go through `insert_run()` and `get_run_mut()` exclusively.

> DEVELOPER

## Type: AgentRuntime trait + AgentLaunchSpec + PreparedAgentLaunch

**File**: `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/runtime.rs`

### Invariants Identified
- `spawn()` takes ownership of the launch contract and returns an `AgentHandle`
- `kill()` and `status()` operate on handles produced by `spawn()`
- The trait is `Send + Sync` (daemon-safe)
- `AgentLaunchSpec` fully describes the process invocation
- `PreparedAgentLaunch` bundles the spec with context (profile, task, workspace, sockets)

### Ratings
- **Encapsulation**: 6/10
  The trait interface is well-designed with clear async methods. `PreparedAgentLaunch` bundles all required context into a single transfer type. However, `AgentLaunchSpec` has all pub fields and no validation (e.g., empty `program` path).

- **Invariant Expression**: 7/10
  The three-method trait surface (`spawn`, `kill`, `status`) is minimal and complete. The doc comments specify exactly what each backend must do (materialize env, bind sockets, set resource limits, etc.). The `AgentOutputMode` enum clearly distinguishes text vs. JSON output protocols.

- **Invariant Usefulness**: 8/10
  The trait contract enables backend substitution (bwrap/docker/host) without changing the daemon's orchestration logic. The launch spec makes the process invocation fully describable and serializable.

- **Invariant Enforcement**: 5/10
  The trait methods return `Result`, so backends can signal failures. However, there is no type-level guarantee that `kill()` and `status()` are only called on handles produced by […]

> DEVELOPER

## Type: State Store Row Types (RunRow, TaskNodeRow, AgentInstanceRow, EventRow)

**Files**: `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/state/runs.rs`, `tasks.rs`, `agent_instances.rs`, `events.rs`

### Invariants Identified
- Row types use `String` for fields that are enums or JSON in the domain types (status, profile, budget, approval_state, etc.)
- Foreign key constraints: task_nodes.run_id -> runs.id, agent_instances.task_id -> task_nodes.id, event_log.run_id -> runs.id
- Timestamps are stored as RFC3339 strings

### Ratings
- **Encapsulation**: 5/10
  The `StateStore` struct properly encapsulates the database connection behind `Arc<Mutex<Connection>>`. The `with_connection` helper provides controlled access. Row types themselves are simple DTOs, which is appropriate for their role.

- **Invariant Expression**: 4/10
  The row types use `String` where the domain types use strongly-typed enums. `TaskNodeRow.status` is a raw `String` that could be "anything", while the domain type is `TaskStatus`. `TaskNodeRow.budget` is a JSON string. This means the persistence layer can store invalid data that would be rejected by domain type deserialization.

- **Invariant Usefulness**: 7/10
  Foreign key constraints in the SQLite schema (enforced via `PRAGMA foreign_keys = ON`) prevent orphaned records. Index coverage is good for the expected query patterns.

- **Invariant Enforcement**: 6/10
  SQLite foreign keys are properly enabled and tested (the `foreign_key_prevents_orphan_tasks` and `foreign_key_prevents_orphan_agent_instances` tests verify this). The `ensure!` macro in update methods prevents […]

> DEVELOPER

## Type: Policy hierarchy (Policy, LimitsPolicy, CredentialPolicy, NetworkPolicy, etc.)

**File**: `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/policy.rs`

### Invariants Identified
- `CredentialPolicy`: `denied` takes precedence over `allowed`
- `NetworkPolicy`: denylist takes precedence over allowlist
- `LimitsPolicy`: `max_children_per_task <= max_tasks_total`
- `CostPolicy`: `warn_at_percent <= 100`
- `SpawnLimits` (in manifest.rs): `require_approval_after <= max_children`

### Ratings
- **Encapsulation**: 3/10
  All fields are pub. Default implementations are provided and sensible.

- **Invariant Expression**: 6/10
  The `PolicyDecision` enum (Approved / RequiresApproval / Denied) is well-designed. `ViolationSeverity` clearly grades violations. The `NetworkDefault` and `MemoryAccessDefault` enums make the default stance explicit.

- **Invariant Usefulness**: 8/10
  Policy invariants directly control security boundaries -- credential access, network egress, spawn limits. Getting these wrong has real consequences.

- **Invariant Enforcement**: 3/10
  The `Default` impls set restrictive defaults (deny-all network, deny project writes), which is the correct security stance. However, there is no validation that prevents nonsensical configurations like `warn_at_percent = 200`, `max_children_per_task = 100` with `max_tasks_total = 50`, or `require_approval_after > max_children`.

### Strengths
- Secure-by-default: `NetworkDefault::Deny`, `MemoryAccessDefault::Deny` for project writes.
- The `PolicyDecision` type clearly separates the three possible outcomes.

### Concerns
- No cross-field validation. `LimitsPolicy` allows `max_concurrent > max_tasks_total` or `max_depth = 0` (which would prevent any execution).
- `SpawnLimits::require_approval_after` has no relationship […]

> DEVELOPER

## Type: AgentHandle

**File**: `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/run_graph.rs` (lines 546-562)

### Invariants Identified
- Either `pid` or `container_id` should be set, depending on `backend`
- `backend == Bwrap` or `backend == Host` implies `pid.is_some()`
- `backend == Docker` implies `container_id.is_some()`
- `socket_dir` must be a valid directory path

### Ratings
- **Encapsulation**: 2/10
  All fields are pub. The relationship between `backend` and `pid`/`container_id` is entirely unchecked.

- **Invariant Expression**: 3/10
  The type does not express the backend-specific data relationship at the type level. Both `pid` and `container_id` are `Option`, even though exactly one should be `Some` depending on `backend`. This is a classic "make illegal states unrepresentable" opportunity that was missed.

- **Invariant Usefulness**: 8/10
  These invariants are important -- querying a Docker container by PID or killing a host process by container ID would be a bug.

- **Invariant Enforcement**: 2/10
  No enforcement. You can create an `AgentHandle` with `backend: RuntimeBackend::Docker, pid: Some(42), container_id: None` and the type will not complain.

### Recommended Improvements
- Use an enum for the backend-specific handle data:
  ```rust
  pub enum AgentHandle {
      Bwrap { agent_id: AgentId, pid: u32, socket_dir: PathBuf },
      Docker { agent_id: AgentId, container_id: String, socket_dir: PathBuf },
      Host { agent_id: AgentId, pid: u32, […]

> DEVELOPER

## Type: BusMessage

**File**: `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/events.rs` (lines 393-521)

### Invariants Identified
- Request/Reply pattern requires matching `ChannelId` for correlation
- Broadcast messages are topic-scoped
- Namespace routing rules: parent-child always allowed, siblings within same parent allowed, cross-tree denied

### Ratings
- **Encapsulation**: 3/10
  All variant fields are pub. The routing rules (parent-child allowed, cross-tree denied) are entirely documentation-level; nothing in the type prevents constructing a `Request` with arbitrary `from`/`to` fields.

- **Invariant Expression**: 5/10
  The variants clearly separate request/response, broadcast, and lifecycle messages. However, the routing policy is invisible at the type level.

- **Invariant Usefulness**: 6/10
  The message types themselves are straightforward. The routing rules are where the real invariants live, but those are external to the type.

- **Invariant Enforcement**: 2/10
  Zero enforcement. The `from`/`to` fields accept any `TaskNodeId`, and there is nothing preventing construction of messages that violate namespace routing rules.

### Strengths
- Clean separation of message purposes into distinct enum variants.
- The `Reply` pattern using `ChannelId` is sound.

### Concerns
- **Structural overlap with RuntimeEventKind**: `BusMessage::ChildTaskRequested`, `BusMessage::TaskCompleted`, `BusMessage::TaskFailed`, `BusMessage::Shutdown`, etc. mirror `RuntimeEventKind` variants with slightly different field shapes. This is a maintenance risk.
- The `payload: Value` fields (using `serde_json::Value`) are fully untyped. Any JSON […]

> DEVELOPER

## Type: RuntimeEvent + RuntimeEventKind

**File**: `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/events.rs`

### Invariants Identified
- `seq` is monotonically increasing (assigned by the SQLite event log)
- `run_id` is always present
- `task_id` and `agent_id` are optional, context-dependent on the event kind
- Each `RuntimeEventKind` variant carries exactly the data relevant to that event
- Events should be append-only (immutable once persisted)

### Ratings
- **Encapsulation**: 4/10
  All fields are `pub`. The `seq` field can be set to any value, even though it should only be assigned by the database. The `RuntimeEvent` struct is essentially a DTO with no behavior.

- **Invariant Expression**: 8/10
  The `RuntimeEventKind` enum is well-designed. Each variant carries precisely the data it needs. The comment-based grouping (Run lifecycle, Task lifecycle, Agent lifecycle, etc.) is clear. The contextual `task_id`/`agent_id` in the envelope allows filtering without deserializing the payload.

- **Invariant Usefulness**: 7/10
  The event structure enables replay, audit, and live streaming -- all critical system capabilities. However, there is no type-level connection between the envelope's `task_id`/`agent_id` and the inner `RuntimeEventKind` variants that also carry task/agent IDs (e.g., `AgentSpawned { task_id }`). This means the same information can be inconsistent between the envelope and the payload.

- **Invariant Enforcement**: 3/10
  No enforcement at […]

> DEVELOPER

## Type: RunState

**File**: `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/run_graph.rs` (lines 94-253)

### Invariants Identified
- `tasks` HashMap keys must match `TaskNode::id` values
- `milestones` HashMap keys must match `MilestoneState` milestone IDs
- Parent-child relationships in `TaskNode` must form a valid tree (no cycles, parent exists in `tasks`)
- `depends_on` references must point to tasks that exist in the same run
- `status` must be consistent with milestone and task states
- `total_tokens` should equal the sum of all task token consumption
- `last_event_cursor` tracks the latest applied event

### Ratings
- **Encapsulation**: 2/10
  Every field is `pub`. External code can freely insert tasks with mismatched IDs, create circular parent-child references, set `status` to `Completed` while tasks are still running, or manipulate `total_tokens` to any value. The carefully written helper methods (`add_child_task`, `update_task_status`, `assign_agent`, `get_ready_tasks`) are easily bypassed.

- **Invariant Expression**: 6/10
  The `get_ready_tasks()` method is well-designed with explicit documentation of what "ready" means. The `RunGraphError` enum correctly models structural failures. However, the type definition itself does not communicate its invariants -- they are entirely implicit.

- **Invariant Usefulness**: 9/10
  These invariants are critical for correctness. A dangling dependency, a cyclic parent-child chain, or an inconsistent status could cause the scheduler to deadlock, skip tasks, […]

> DEVELOPER

## Type: TaskStatus (enum)

**File**: `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/run_graph.rs` (lines 345-389)

### Invariants Identified
- Lifecycle follows: Pending -> (AwaitingApproval | Enqueued) -> Materializing -> Running -> (Completed | Failed | Killed)
- `Running` variant carries the agent ID and start time
- `Completed` variant carries the result and duration
- `Failed` variant carries the error and duration
- Only one terminal state can be reached

### Ratings
- **Encapsulation**: 7/10
  The enum variants carry associated data that belongs with the state, which is good. However, the `PartialEq` derive on the entire enum (which includes `chrono::Duration`) means equality comparison is available and meaningful.

- **Invariant Expression**: 8/10
  State machine transitions are documented in the doc comment, and the associated data per variant naturally prevents accessing agent information when the task is not running. This is a textbook "make illegal states unrepresentable" pattern.

- **Invariant Usefulness**: 9/10
  Tying the `agent_id` to the `Running` variant, and `AgentResult` to the `Completed` variant, prevents accessing result data for a task that hasn't finished and prevents accessing the agent for a task that isn't running. This eliminates an entire class of "checked the wrong field" bugs.

- **Invariant Enforcement**: 5/10
  The state transitions themselves are NOT enforced by […]

> DEVELOPER

## Type: BudgetEnvelope

**File**: `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/manifest.rs` (lines 250-313)

### Invariants Identified
- `remaining == allocated - consumed` (derived/computed field)
- `consumed` and `subtree_consumed` increase monotonically (via `saturating_add`)
- `subtree_consumed >= consumed` (subtree includes self)
- `warn_at_percent` is a percentage (0-100)

### Ratings
- **Encapsulation**: 3/10
  All fields are `pub`. Any consumer can set `consumed = 100` while leaving `remaining = allocated`, violating the derived-field invariant. The `consume()` method correctly maintains consistency, but direct field mutation bypasses it entirely.

- **Invariant Expression**: 5/10
  The `remaining` field is documented as a "computed convenience field," but it is stored as a mutable pub field rather than a derived getter. This invites desynchronization. The `warn_at_percent` field has no compile-time or construction-time constraint enforcing that it is in range 0..=100, though the proto layer does validate this.

- **Invariant Usefulness**: 8/10
  Budget tracking with subtree rollup is critical for the daemon's resource governance. Correct enforcement prevents budget overrun and enables accurate cost reporting.

- **Invariant Enforcement**: 4/10
  The `new()` constructor correctly initializes `consumed = 0, subtree_consumed = 0, remaining = allocated`. The `consume()` and `consume_subtree()` methods use `saturating_add`/`saturating_sub` to prevent panics on overflow. However, fields are `pub`, so all invariants can be trivially bypassed. The `is_warning_threshold_reached()` […]

> DEVELOPER

## Type: Newtype ID Family (RunId, TaskNodeId, AgentId, MilestoneId, ApprovalId, SpawnId, ChannelId)

**File**: `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/ids.rs`

### Invariants Identified
- Each ID kind is a distinct type at the type level -- prevents passing a `RunId` where a `TaskNodeId` is expected
- Inner string is always present (no `Option`-wrapping)
- `generate()` produces UUID v4 values

### Ratings
- **Encapsulation**: 7/10
  The inner `String` is private, accessible only through `as_str()` and `into_inner()`. However, the unconstrained `From<&str>` and `From<String>` impls bypass any format validation, making it trivial to create IDs with arbitrary content including empty strings. The `new()` constructor accepts any `Into<String>` without validation.

- **Invariant Expression**: 6/10
  The macro-based approach is clean and consistent. However, the types do not express whether an ID was generated (UUID) versus user-supplied, and empty strings are silently accepted at construction time on the domain side -- only the proto conversion layer rejects blanks.

- **Invariant Usefulness**: 9/10
  Newtype IDs are extremely valuable. They prevent a large class of argument-swap bugs in a system with 7 different string identifier kinds that all look the same at the value level.

- **Invariant Enforcement**: 5/10
  Enforcement is weak at construction. `RunId::new("")` happily creates an empty ID. The proto layer in […]

> DEVELOPER

# Type Design Analysis: `runtime-daemon-dispatch` PR

This analysis covers the type system introduced across `forge-common`, `forge-proto`, and `forge-runtime` for the runtime daemon platform. I evaluated approximately 60 new or substantially modified types across 8 key modules.

> DEVELOPER

## Summary

| Fix | File | Verdict |
|-----|------|---------|
| C1 -- Silent output channel discard | `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/runtime/io.rs` | **VERIFIED** -- Error is logged at error level with full context, deduplication prevents log flooding, unit test covers the behavior. |
| C2 -- Failed dispatch leaves task stuck in infinite retry | `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/task_manager.rs` | **VERIFIED** -- Task is transitioned to `Failed` via `finalize_dispatch_failure`, meta-failures are logged at error level, the original spawn error is always logged, and a dedicated test validates the state transition. |

Both fixes are well-implemented, follow the project's error handling conventions (structured tracing with contextual fields, appropriate severity levels), and include test coverage.</result>
<usage><total_tokens>22367</total_tokens><tool_uses>8</tool_uses><duration_ms>56898</duration_ms></usage>
</task-notification>
Full transcript available at: /private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/a3912c6da60a58b88.output

> DEVELOPER

## Fix C2 -- Failed dispatch leaves task stuck in infinite retry

**File:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/task_manager.rs`

**Relevant code (lines 223-244):**

```rust
match self.spawn_prepared(prepared).await {
    Ok(_) => launched.push(task_id),
    Err(error) => {
        if let Err(mark_error) = self
            .finalize_dispatch_failure(&run_id, &task_id, error.to_string())
            .await
        {
            tracing::error!(
                %mark_error,
                run_id = %run_id,
                task_id = %task_id,
                "failed to persist dispatch failure"
            );
        }
        tracing::warn!(
            %error,
            run_id = %run_id,
            task_id = %task_id,
            "failed to dispatch enqueued task"
        );
    }
}
```

**Verdict: VERIFIED**

The fix is correct and thorough. The original code only logged the `spawn_prepared` failure at warn level without transitioning the task, causing the task to remain in `Enqueued` status and be retried every 250ms forever. The fix now:

1. **Transitions the task to Failed** -- `finalize_dispatch_failure` (lines 526-554) transitions the task to `TaskStatus::Failed { error, duration }`, which removes it from the `enqueued_tasks()` query and breaks the infinite retry loop. The method checks that the task is still in `Enqueued` or `Materializing` status before transitioning, which is a correct guard against race conditions.

2. **Handles the meta-failure gracefully** -- If `finalize_dispatch_failure` itself fails (e.g., database write error), the error is logged at `tracing::error!` level with full context (`mark_error`, `run_id`, `task_id`). This is important -- if the state transition […]

> DEVELOPER

## Fix C1 -- Silent output channel discard

**File:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/runtime/io.rs`

**Relevant code (lines 64-78):**

```rust
fn emit(&self, envelope: RuntimeOutputEnvelope) {
    if let Some(tx) = &self.tx {
        if let Err(error) = tx.send(envelope)
            && !self.receiver_dropped.swap(true, Ordering::Relaxed)
        {
            let envelope = error.0;
            tracing::error!(
                run_id = %envelope.run_id,
                task_id = %envelope.task_id,
                agent_id = %envelope.agent_id,
                "runtime output receiver dropped; live agent output will be lost until the daemon is restarted"
            );
        }
    }
}
```

**Verdict: VERIFIED**

The fix is correct and well-implemented. The original `let _ = tx.send(envelope)` has been replaced with proper error handling that:

1. **Logs the error with rich context** -- The `tracing::error!` call includes `run_id`, `task_id`, and `agent_id`, giving operators everything they need to diagnose the issue. The message clearly explains the consequence: "live agent output will be lost until the daemon is restarted."

2. **Uses appropriate severity** -- `tracing::error!` is correct here. A dropped receiver means all subsequent agent output is silently lost, which is a production-impacting condition that warrants error-level logging.

3. **Includes a smart deduplication guard** -- The `receiver_dropped` `AtomicBool` with `swap(true, Ordering::Relaxed)` ensures the error message is emitted exactly once. This is a thoughtful choice -- without it, every subsequent output event would flood the logs with […]

> DEVELOPER

**Summary: All four medium-severity fixes (M1, M2, M4, M6) are VERIFIED.**</result>
<usage><total_tokens>17517</total_tokens><tool_uses>5</tool_uses><duration_ms>29655</duration_ms></usage>
</task-notification>
Full transcript available at: /private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/ad4ae44be4ed71afa.output

> DEVELOPER

**M6 -- Insecure defaults when task_manager is None: VERIFIED**

In `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/server.rs`:

- `runtime_backend_proto()` (lines 122-127): When `task_manager` is `None`, defaults to `proto::RuntimeBackend::Unspecified as i32` instead of `Host`.
- `insecure_host_runtime()` (lines 129-134): When `task_manager` is `None`, defaults to `false` instead of `true`.

Both are the expected safe defaults.

> DEVELOPER

**M4 -- Docker container cleanup logged at debug: VERIFIED**

The `best_effort_remove_container` method in `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/runtime/docker.rs` line 183 now uses `tracing::warn!` instead of `tracing::debug!`, with a clear message: `"best-effort Docker container cleanup failed; container may leak"`.

> DEVELOPER

**M2 -- Missing agent_id defaults to empty string: VERIFIED**

The original `unwrap_or_else(|| AgentId::new(""))` pattern is completely gone. The current code at `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/state/events.rs` lines 291-293 now uses:

```rust
agent_id: runtime_event
    .agent_id
    .ok_or_else(|| anyhow!("task-output row missing agent_id at seq {}", self.seq))?,
```

This correctly returns an error instead of silently defaulting. There is also a dedicated test `decode_task_output_event_rejects_missing_agent_id` (line 553) that validates this behavior.

> DEVELOPER

**M1 -- pid as i32 overflow: VERIFIED**

Both files now use a dedicated `pid_t_from_u32` helper that calls `i32::try_from(pid)` with `.context("pid exceeds libc::pid_t range")`, returning a `Result` instead of using a bare `as i32` cast.

- `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/runtime/host.rs` lines 251-255
- `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/runtime/bwrap.rs` lines 410-414

> DEVELOPER

## Summary

| Fix | Status | Notes |
|-----|--------|-------|
| C3 -- NoopAgentSupervisor | **VERIFIED** | Bootstrap guard rejects active state; metadata correctly reports Unspecified/false when no TaskManager; tests cover both the rejection and the metadata values |
| C4 -- Blocking sync DB call | **VERIFIED** | `pending_approvals` now calls async `latest_event_seq()` which wraps SQLite I/O in `spawn_blocking`; all DB access in handlers follows this pattern consistently |</result>
<usage><total_tokens>30102</total_tokens><tool_uses>17</tool_uses><duration_ms>63565</duration_ms></usage>
</task-notification>
Full transcript available at: /private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/a200585445e22a6fb.output

> DEVELOPER

## Fix C4 -- Blocking sync DB call on tokio worker thread

### Verification Summary

**Rating: VERIFIED**

The `pending_approvals` handler at line 660 now calls `self.state_store.latest_event_seq().await` (line 673) instead of the synchronous `self.state_store.latest_seq()`.

The `latest_event_seq` method in `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/state/mod.rs` (lines 107-112) wraps the synchronous `latest_seq()` call inside `tokio::task::spawn_blocking`, which moves the blocking SQLite I/O off the tokio worker thread:

```rust
pub async fn latest_event_seq(&self) -> Result<i64> {
    let store = self.clone();
    tokio::task::spawn_blocking(move || store.latest_seq())
        .await
        .map_err(|error| anyhow!("latest event sequence task failed: {error}"))?
}
```

The same pattern is used for the `counts()` call in the `health` handler (line 839), which also uses `spawn_blocking` internally (lines 81-104 of `state/mod.rs`). Both database access points in server handlers are now non-blocking.

No new issues were introduced by these fixes. The `ensure_quiescent_runtime_state` function also correctly uses `spawn_blocking` for its database queries (line 192).

> DEVELOPER

## Fix C3 -- NoopAgentSupervisor in production run_server path

### Verification Summary

**Rating: VERIFIED**

The fix addresses all three aspects of the original bug:

**1. Bootstrap rejection for active runtime state:**
`/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/server.rs`, line 151 -- `run_server` now calls `ensure_quiescent_runtime_state()` (lines 190-207) before doing anything else. This function uses `spawn_blocking` to check both active tasks (Materializing/Running) and active agent instances. If either exist, it bails with a clear error message: `"run_server cannot bootstrap over active runtime state"`. This prevents the dangerous scenario where `NoopAgentSupervisor` would run recovery against live agents.

**2. NoopAgentSupervisor is safe given the guard:**
`run_server` still uses `NoopAgentSupervisor` (line 153), but this is now safe because the `ensure_quiescent_runtime_state` guard on line 151 guarantees there are no active tasks or agents. The noop supervisor will never encounter live agents to recover or terminate, making it a correct choice for this code path. Recovery at line 154 will only process already-finished or crashed state.

**3. Metadata reports correct values when TaskManager is None:**
Lines 122-134 show that `runtime_backend_proto()` returns `RuntimeBackend::Unspecified` and `insecure_host_runtime()` returns `false` when `self.task_manager` is `None`. This is the correct behavior -- the server does not claim `Host` backend or set `insecure_host_runtime = true` when no TaskManager is […]

> DEVELOPER

## Summary

| Type | Verdict | Key Improvement | Remaining Gap |
|------|---------|-----------------|---------------|
| BudgetEnvelope | PARTIALLY FIXED | `remaining` is now computed; mutation methods exist | `consumed`, `subtree_consumed`, `allocated`, `warn_at_percent` are still `pub` fields |
| RunState | VERIFIED | All fields non-pub; validated mutation methods; `can_transition_to()` state machines for both RunStatus and TaskStatus | `TaskNode` fields are still `pub`, though access is mediated through `RunState` |
| AgentHandle | VERIFIED | Restructured from `Option<pid> + Option<container_id>` into a backend-discriminated enum with three variants | None significant |

The most actionable remaining improvement is making `BudgetEnvelope`'s fields non-pub and adding read-only accessors, which would close the last encapsulation gap without adding complexity.</result>
<usage><total_tokens>38278</total_tokens><tool_uses>11</tool_uses><duration_ms>86094</duration_ms></usage>
</task-notification>
Full transcript available at: /private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/a4bf0c7837eb35b54.output

> DEVELOPER

## 3. AgentHandle Structure

**File:** `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/run_graph.rs` (lines 996-1096)

**Status: VERIFIED**

### What was done well

The `Option<pid> + Option<container_id>` anti-pattern has been replaced with a proper backend-discriminated enum:

```rust
pub enum AgentHandle {
    Host { agent_id, pid: u32, socket_dir },
    Bwrap { agent_id, pid: u32, socket_dir },
    Docker { agent_id, container_id: String, socket_dir },
}
```

This makes illegal states unrepresentable:
- A `Host` handle always has a `pid` and never has a `container_id`.
- A `Docker` handle always has a `container_id` and never has a `pid`.
- A `Bwrap` handle (Linux bubblewrap) always has a `pid`, distinct from Docker.

Named constructors (`host()`, `bwrap()`, `docker()`) provide ergonomic creation. The accessor methods `pid()` and `container_id()` return `Option` types that correctly reflect which backends support which identifier, derived from the discriminant rather than stored as independent optional fields.

A companion `RuntimeBackend` enum (line 1099) provides a lightweight discriminant without the associated data, useful for matching or display without carrying handle details.

### Ratings

- **Encapsulation**: 8/10 -- Variant fields are non-pub (enum variant fields in Rust are private by default in struct-like variants). Accessors are provided.
- **Invariant Expression**: 10/10 -- The enum structure makes the backend discrimination self-documenting. It is impossible […]

> DEVELOPER

## 2. RunState Encapsulation

**File:** `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/run_graph.rs` (lines 109-655)

**Status: VERIFIED**

### What was done well

All fields of `RunState` are non-pub (lines 111-148). This is a substantial improvement over the original "all fields pub" design. The type now enforces access through:

- Read-only accessor methods: `id()`, `project()`, `workspace()`, `plan()`, `milestones()`, `tasks()`, `approvals()`, `status()`, etc.
- Validated mutation methods: `update_task_status()`, `update_run_status()`, `add_child_task()`, `attach_child_task()`, `insert_approval()`, `transition_task()`, etc.
- State transition validation via `can_transition_to()` on both `RunStatus` (line 1152) and `TaskStatus` (line 811), with proper `RunGraphError` variants for invalid transitions.
- Construction through dedicated factory methods: `new_submitted()` which forces `RunStatus::Submitted` and zeroed counters, and `rehydrated()` for deserialization.

The `TaskStatus::can_transition_to()` method implements a well-defined lifecycle state machine:
```
Pending -> AwaitingApproval | Enqueued | Materializing | Running | Failed | Killed
AwaitingApproval -> Enqueued | Materializing | Running | Failed | Killed
Enqueued -> Materializing | Running | Failed | Killed
Materializing -> Running | Failed | Killed
Running -> Completed | Failed | Killed
Terminal states (Completed | Failed | Killed) -> nothing
```

The `RunStatus::can_transition_to()` similarly enforces:
```
Submitted -> Planning | Running | Failed | Cancelled
Planning -> Running | Failed | Cancelled
Running -> Paused | Completed | Failed | […]

> DEVELOPER

## 1. BudgetEnvelope Encapsulation

**File:** `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/manifest.rs` (lines 250-312)

**Status: PARTIALLY FIXED**

### What was done well

- `remaining()` is now a computed method (line 291-293), not a stored field. This eliminates the redundant source of truth problem.
- The type has a proper constructor `new()` that initializes `consumed` and `subtree_consumed` to zero.
- Mutation is channeled through `consume()` and `consume_subtree()` methods that use saturating arithmetic.
- Useful derived queries like `is_warning_threshold_reached()` and `is_exhausted()` are provided.
- The warning threshold check uses `u128` promotion to avoid overflow, which is a good defensive choice.
- Tests cover normal usage, subtree rollup, and overflow edge cases.

### What remains unfixed

The `consumed` and `subtree_consumed` fields are still `pub` (lines 256, 259). This means external code can bypass the `consume()` and `consume_subtree()` methods entirely, setting these fields to arbitrary values, including values that violate the invariant that `subtree_consumed >= consumed`. The test at line 1414 (`run.tasks.get_mut(&root_id).unwrap().budget.consume(500)`) is a correct usage, but line 1382 shows tests directly accessing internal mutable state of `RunState` via `run.tasks.get_mut(...)`, which would also allow `budget.consumed = 9999` or similar nonsense.

Additionally, `allocated` and `warn_at_percent` are also `pub`, meaning a caller could change `allocated` after construction, undermining the budget tracking entirely. […]

> DEVELOPER

## Summary

| Fix | Status | Notes |
|-----|--------|-------|
| I1 -- Lifecycle circuit breaker | **VERIFIED** | Complete with threshold, escalation to error, shutdown, and tests |
| I2 -- Scheduler permanently skips runs | **VERIFIED** | Fails the run on graph errors, persists to store, tested |
| I3 -- force_stop delegates to graceful_stop | **VERIFIED** | Separate `kill` vs `force_kill` paths, SIGTERM vs SIGKILL, tested |
| I5 -- BudgetEnvelope.remaining desync | **PARTIALLY FIXED** | `remaining` is now computed (good), but `consumed`, `subtree_consumed`, and `allocated` are still `pub` fields, allowing external mutation that could cause desync |
| I6 -- RunState all-pub fields | **VERIFIED** | All fields non-pub, mutation through validated methods only |</result>
<usage><total_tokens>65545</total_tokens><tool_uses>32</tool_uses><duration_ms>127919</duration_ms></usage>
</task-notification>
Full transcript available at: /private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/a613f9365350d3ca7.output

> DEVELOPER

## Fix I6 -- RunState all-pub fields

**File:** `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/run_graph.rs`

**Rating: VERIFIED**

The fix is correct and thorough. All fields of `RunState` are now non-pub (lines 111-148):

```
id: RunId,
project: String,
workspace: PathBuf,
plan: RunPlan,
milestones: HashMap<MilestoneId, MilestoneState>,
tasks: HashMap<TaskNodeId, TaskNode>,
approvals: HashMap<ApprovalId, PendingApproval>,
status: RunStatus,
last_event_cursor: u64,
submitted_at: DateTime<Utc>,
finished_at: Option<DateTime<Utc>>,
total_tokens: u64,
estimated_cost_usd: f64,
```

None have `pub` visibility. The struct provides:

- **Read accessors:** `id()`, `project()`, `workspace()`, `plan()`, `milestones()`, `tasks()`, `approvals()`, `status()`, `last_event_cursor()`, `submitted_at()`, `finished_at()`, `total_tokens()`, `estimated_cost_usd()`, plus convenience methods like `task()`, `milestone()`, `approval()`, `contains_task()`, `task_count()`, `iter_tasks()`, etc.
- **Validated mutation methods:** `update_task_status()`, `transition_task()`, `update_run_status()`, `add_child_task()`, `attach_child_task()`, `insert_approval()`, `take_approval()`, `set_task_approval_state()`, `set_task_result_summary()`, `assign_agent()`, `set_task_dependencies()`, `link_child_task()`, `update_task_spawn_limits()`, `set_last_event_cursor()`, `set_finished_at()`, `update_totals()`.
- **Construction:** `new_submitted()` and `rehydrated()` are the only ways to create a `RunState`.

The mutation methods include proper validation -- for example, `update_task_status` and `transition_task` validate the state machine via `can_transition_to()` and return `RunGraphError::InvalidTaskTransition` on violation. `update_run_status` similarly validates via `can_transition_to` on `RunStatus`. `add_child_task` validates parent existence. This is a well-done encapsulation.

**Note:** `TaskNode` (line 699) still has all-pub fields, but this was not part of the original issue (I6 specifically called out `RunState`). The `TaskNode` fields being pub is mitigated by the fact that `RunState.tasks` is non-pub, so […]

> DEVELOPER

## Fix I5 -- BudgetEnvelope.remaining desync

**File:** `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/manifest.rs`

**Rating: PARTIALLY FIXED**

The `remaining` field has been correctly removed and replaced with a computed method `pub fn remaining(&self) -> u64` (line 291) that returns `self.allocated.saturating_sub(self.consumed)`. This eliminates the desync risk.

However, the second part of the fix is **not addressed**: `consumed` and `subtree_consumed` are still `pub` fields (lines 256, 259). The original issue specified:

> `consumed` and `subtree_consumed` should be non-pub.

These fields are accessed directly from outside `manifest.rs`:

- `run_graph.rs:388` -- `task.budget.consumed` (read)
- `server.rs:983` -- `task.budget.consumed` (read)
- `server.rs:990` -- `task.budget.subtree_consumed` (read)
- `recovery.rs:481` -- `budget.consumed` (read)
- `forge-proto/src/convert/manifest.rs:557-558` -- test assertions on `.consumed` and `.subtree_consumed`

All external usages are **reads**, not writes. The fields should be made non-pub with accessor methods `pub fn consumed(&self) -> u64` and `pub fn subtree_consumed(&self) -> u64` to prevent external code from mutating them and causing desync. The mutation path should be exclusively through `consume()` and `consume_subtree()`.

Additionally, `allocated` is also still `pub` (line 253), which means external code could directly modify `allocated` and create the same class of desync that removing `remaining` was meant to prevent. A `pub fn allocated(&self) -> u64` accessor would complete the encapsulation.

> DEVELOPER

## Fix I3 -- force_stop delegates to graceful_stop

**File:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/task_manager.rs`

**Rating: VERIFIED**

The fix is correct and complete. `force_stop` (line 672) now calls `self.force_kill_agent(&agent.task_id, reason)` instead of `self.graceful_stop(...)`. The call chain is:

1. `force_stop` (line 672) -> `force_kill_agent` (line 441) -> `stop_agent(task_id, reason, true)` (line 446).
2. `stop_agent` (line 449) checks the `force` boolean (line 456): when `true`, it calls `self.runtime.force_kill(&instance.handle, &reason)` (line 458), which maps to `SIGKILL` in the host runtime (confirmed at `host.rs:193: send_signal(pid, libc::SIGKILL)`). When `false` (graceful path), it calls `self.runtime.kill()` which sends `SIGTERM` with a 2-second timeout before escalating to `SIGKILL`.
3. `graceful_stop` (line 663) calls `self.kill_agent()` which routes to `stop_agent(..., false)`.

The trait-level separation is clean:
- `kill` = SIGTERM with timeout, escalate to SIGKILL
- `force_kill` = immediate SIGKILL
- `graceful_stop` -> `kill` (graceful path)
- `force_stop` -> `force_kill` (aggressive path)

A dedicated test `supervisor_force_stop_uses_runtime_force_kill` (line 1272) verifies that `force_stop` calls `force_kill` (not `kill`) on the runtime, asserting `kill_calls == 0` and `force_kill_calls == 1`.

> DEVELOPER

## Fix I2 -- Scheduler permanently skips runs

**File:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/scheduler.rs`

**Rating: VERIFIED**

The fix is correct and complete. When `run.get_ready_tasks()` fails (line 59), the scheduler now:

1. Logs at `tracing::error!` level (line 61) with the run_id and a clear message: "scheduler failing run after ready-task computation failed".
2. Drops the orchestrator lock (line 65) before calling `self.fail_invalid_run(&run_id).await` (line 66).
3. The `fail_invalid_run` method (lines 97-106) calls `orchestrator.fail_run(run_id)`, which transitions the run to `Failed` status -- making it visible to clients as a terminal state rather than leaving it silently stuck in `Running`.
4. If `fail_run` itself fails, a second `tracing::error!` is emitted (line 100) with context.
5. A dedicated integration test `scheduler_fails_run_when_graph_is_invalid` (lines 292-334) verifies this by injecting a corrupted run graph with a dangling dependency, asserting both in-memory and persisted state show `RunStatus::Failed`.

The error handling chain is complete: the failure is logged, the run transitions to a visible terminal state, and both the graph and persistent store are updated.

> DEVELOPER

# Error Handling Audit: Fix Verification Report

## Fix I1 -- Lifecycle loop circuit breaker

**File:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/main.rs`

**Rating: VERIFIED**

The fix is correct and complete. The implementation introduces:

1. A `LifecycleCircuitBreaker` struct (lines 25-55) with a configurable threshold (`LIFECYCLE_FAILURE_THRESHOLD = 8`).
2. `record_cycle(failed: bool) -> bool` resets the counter on success and increments on failure using `saturating_add`, returning `true` when the threshold is reached.
3. The lifecycle loop (lines 174-224) tracks `cycle_failed` across all three operations (`drain_runtime_output`, `dispatch_enqueued_tasks`, `poll_active_agents`).
4. When the circuit breaker trips, the code escalates to `tracing::error!` (line 211) and initiates a full daemon shutdown via `lifecycle_shutdown.initiate_shutdown(reason, None)` (line 212). The shutdown itself is not silently swallowed -- if it fails, a second `tracing::error!` is emitted (line 214).
5. Unit tests at lines 324-345 verify both reset-on-success and trip-at-threshold behavior.

**Minor observations (non-blocking):** There is no exponential backoff between ticks during consecutive failures -- each failing cycle still runs at the 250ms cadence until the threshold trips. This is acceptable given that the threshold is 8 (2 seconds of sustained failure), and the daemon shuts down rather than degrading, which is the right behavior for persistent failures like DB corruption. The individual operation logs at `warn!` level […]

> DEVELOPER

lets create a PR for this branch

> AGENT

There are unstaged changes in several runtime files and untracked files (including `crates/forge-common/target/` which should not be committed). Would you like me to:

1. **Commit the unstaged source changes first**, then create the PR
2. **Create the PR from the 7 existing commits only**, leaving the unstaged changes out

The 7 commits on this branch cover:
- Runtime platform foundation (domain types, contracts, plans)
- Runtime daemon core with gRPC server and approval system
- Backend execution and task dispatch
- Live task output event streaming
- Review fixes across iterations

> DEVELOPER

1

> AGENT

PR created: https://github.com/jdsingh122918/forge/pull/21

> TOOL

<command-message>pr-review-toolkit:review-pr</command-message>
<command-name>/pr-review-toolkit:review-pr</command-name>

> SYSTEM

# Comprehensive PR Review

Run a comprehensive pull request review using multiple specialized agents, each focusing on a different aspect of code quality.

**Review Aspects (optional):** ""

## Review Workflow:

1. **Determine Review Scope**
   - Check git status to identify changed files
   - Parse arguments to see if user requested specific review aspects
   - Default: Run all applicable reviews

2. **Available Review Aspects:**

   - **comments** - Analyze code comment accuracy and maintainability
   - **tests** - Review test coverage quality and completeness
   - **errors** - Check error handling for silent failures
   - **types** - Analyze type design and invariants (if new types added)
   - **code** - General code review for project guidelines
   - **simplify** - Simplify code for clarity and maintainability
   - **all** - Run all applicable reviews (default)

3. **Identify Changed Files**
   - Run `git diff --name-only` to see modified files
   - Check if PR already exists: `gh pr view`
   - Identify file types and what reviews apply

4. **Determine Applicable Reviews**

   Based on changes:
   - **Always applicable**: code-reviewer (general quality)
   - **If test files changed**: pr-test-analyzer
   - **If comments/docs added**: comment-analyzer
   - **If error handling changed**: silent-failure-hunter
   - **If types added/modified**: type-design-analyzer
   - **After passing review**: code-simplifier (polish and […]

> AGENT

Launched 5 review agents in parallel:

1. **Code reviewer** — general quality and CLAUDE.md compliance
2. **Silent failure hunter** — error handling and swallowed errors
3. **Test analyzer** — test coverage gaps
4. **Type design analyzer** — type safety and invariants
5. **Comment analyzer** — comment accuracy and staleness

I'll compile the results as they come back.

<details>
<summary>Waiting for all 5 agents to complete...</summary>

The agents are analyzing ~31k lines of new code across 62 files. This may take a few minutes.
</details>

> METADATA

<task-notification>
<task-id>a846f7e84af7184e0</task-id>
<tool-use-id>REDACTED</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/a846f7e84af7184e0.output</output-file>
<status>completed</status>
<summary>Agent "Test coverage analysis" completed</summary>
<result>Now I have a thorough understanding of both the source code and test coverage. Let me compile my analysis.

---

## Test Coverage Analysis: `runtime-daemon-dispatch` PR

### 1. Summary

The test suite for the `forge-runtime` crate is **well-structured and covers the primary gRPC contract thoroughly**. There are 7 integration test files with approximately 25 test cases, plus inline unit tests in `scheduler.rs`, `shutdown.rs`, and `runtime/mod.rs`. The tests exercise the key gRPC RPCs via real Unix socket connections, validate both happy paths and error conditions, check state persistence across restarts, and verify event streaming behavior including live-tail, replay, filtering, and cursor alignment.

The most significant coverage gaps are in the **recovery module**, **task manager lifecycle paths**, and **run orchestrator state machine transitions** -- areas where production bugs would cause data loss or silent corruption.

---

### 2. Critical Gaps (Criticality 8-10)

**2a. Recovery module (`recovery.rs`) has no integration or unit tests -- Criticality: 9/10**

The `recover_orphans` and `rebuild_run_graph` functions contain approximately 600 lines of logic covering:
- Reconciling stale tasks (pending, running, materializing) against live agents
- Marking unrecoverable tasks as Failed
- Reconstructing `RunState` from serialized `TaskNodeRow` and `RunRow` data […]

> AGENT

Test coverage analysis is back. Waiting for the remaining 4 agents to complete...

> METADATA

<task-notification>
<task-id>adc5331c1a1f1c367</task-id>
<tool-use-id>toolu_01Xu5pj3V4Ai12tZKCGfPoPz</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/adc5331c1a1f1c367.output</output-file>
<status>completed</status>
<summary>Agent "Silent failure analysis" completed</summary>
<result>I now have a thorough understanding of the codebase. Let me compile my findings.

---

# Error Handling Audit: `runtime-daemon-dispatch` PR

## Executive Summary

This PR adds a substantial `forge-runtime` crate with ~15,000 lines of new production code. The error handling is generally above average -- most error paths use `anyhow::Context`, propagate errors with `?`, and include contextual information. However, I found several significant issues that range from silent failures to inappropriate fallbacks that could cause debugging nightmares in production.

---

## CRITICAL Issues

### Issue 1: Silent fire-and-forget of runtime output channel sends

**Location:** `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/runtime/io.rs`, line 48

**Severity:** CRITICAL

**Issue Description:** The `RuntimeOutputSink::emit()` method silently discards errors when sending runtime output events via the unbounded channel:

```rust
fn emit(&self, envelope: RuntimeOutputEnvelope) {
    if let Some(tx) = &self.tx {
        let _ = tx.send(envelope);
    }
}
```

The `let _ = tx.send(envelope)` discards the `SendError` without any logging. If the receiver is dropped (because the drain task panicked, was cancelled, or the channel was closed), every subsequent output event -- stdout lines, stderr lines, token usage updates, session captures, tool calls, assistant text -- is silently discarded. The user sees no […]

> AGENT

Silent failure analysis is back. 3 agents still running...

> METADATA

<task-notification>
<task-id>a8288beb63222ca28</task-id>
<tool-use-id>toolu_0171WrSz665RhW3v4L2EkjLW</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/a8288beb63222ca28.output</output-file>
<status>completed</status>
<summary>Agent "Code review for PR" completed</summary>
<result>This is during server startup, before serving begins, so blocking here is acceptable.

Now I have all the information I need for the review. Let me compile the findings.

---

## Code Review: `runtime-daemon-dispatch` PR

**Reviewing files across:**
- `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/` (server.rs, run_orchestrator.rs, task_manager.rs, event_stream.rs, scheduler.rs, main.rs, lib.rs, shutdown.rs, recovery.rs, profile_compiler.rs)
- `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/state/` (mod.rs, schema.rs, events.rs, runs.rs, tasks.rs, agent_instances.rs)
- `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/runtime/` (mod.rs, io.rs, host.rs, docker.rs, bwrap.rs)
- `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/events.rs`

---

### Critical (90-100)

**1. Blocking synchronous database call inside async gRPC handler violates CLAUDE.md** (Confidence: 95)

File: `/Users/jdsingh/Projects/AI/forge/crates/forge-runtime/src/server.rs`, line 657

CLAUDE.md rule: "Use tokio for all async -- never block in async code"

The `pending_approvals` handler calls `self.state_store.latest_seq()` directly, which internally calls `with_connection()`, acquiring a `std::sync::Mutex` lock and performing synchronous SQLite I/O on the tokio worker thread. Every other state store call from async code in this crate correctly wraps the work in `tokio::task::spawn_blocking`.

```rust
let fence = self
    .state_store
    .latest_seq()
    .map_err(|error| Status::internal(format!("failed to load approval fence: {error}")))?;
```

Fix: Wrap in `spawn_blocking`, similar to how `counts()` is implemented in `state/mod.rs`:

```rust
let state_store = Arc::clone(&self.state_store);
let fence = tokio::task::spawn_blocking(move || state_store.latest_seq())
    .await
    .map_err(|error| Status::internal(format!("approval fence task failed: {error}")))?
    .map_err(|error| Status::internal(format!("failed […]

> AGENT

Code review is back. 2 agents still running (type design + comment analysis)...

> METADATA

<task-notification>
<task-id>aebe4b1d9703cfaed</task-id>
<tool-use-id>REDACTED</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/aebe4b1d9703cfaed.output</output-file>
<status>completed</status>
<summary>Agent "Comment accuracy analysis" completed</summary>
<result>The module has 22+ public functions across ~2600 lines. That's far from "minimal." Let me now finalize my analysis.

---

**Summary**

I analyzed all code comments across the 15 key files in this PR, cross-referencing each comment against the actual implementation. The codebase is generally well-documented with accurate structural and API-level comments. However, I found several issues ranging from factually misleading comments to comments that will quickly become stale as this code evolves. Below are the findings organized by severity.

---

**Critical Issues**

1. **Location**: `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/runtime.rs:89`
   - **Issue**: The doc comment on `AgentStatus::Exited` says "The agent exited successfully (exit code 0)." However, the `exit_code` field is `i32` and the `status_from_exit_status` function in `crates/forge-runtime/src/runtime/io.rs:257-261` maps any `exit_status.success()` to `Exited`, which on most systems means exit code 0 -- but the struct carries an arbitrary `i32`. The comment misleadingly implies exit code is always 0, when the variant is capable of carrying any code. More importantly, the Docker runtime (`docker.rs:500`) explicitly constructs `Exited { exit_code: 0 }` only for zero, but the data type does not enforce this constraint. The comment should say "The agent exited with a successful status" rather than […]

> AGENT

Comment analysis is back. 1 agent remaining (type design)...

> METADATA

<task-notification>
<task-id>a97c68888ec197c3e</task-id>
<tool-use-id>toolu_01RKvLgdZYJiYRwYb4JuJHFL</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/206d870e-7f6f-4e92-9b7a-035603905453/tasks/a97c68888ec197c3e.output</output-file>
<status>completed</status>
<summary>Agent "Type design analysis" completed</summary>
<result>Now I have a thorough understanding of all the types. Let me produce the analysis.

---

# Type Design Analysis: `runtime-daemon-dispatch` PR

This analysis covers the type system introduced across `forge-common`, `forge-proto`, and `forge-runtime` for the runtime daemon platform. I evaluated approximately 60 new or substantially modified types across 8 key modules.

---

## Type: Newtype ID Family (RunId, TaskNodeId, AgentId, MilestoneId, ApprovalId, SpawnId, ChannelId)

**File**: `/Users/jdsingh/Projects/AI/forge/crates/forge-common/src/ids.rs`

### Invariants Identified
- Each ID kind is a distinct type at the type level -- prevents passing a `RunId` where a `TaskNodeId` is expected
- Inner string is always present (no `Option`-wrapping)
- `generate()` produces UUID v4 values

### Ratings
- **Encapsulation**: 7/10
  The inner `String` is private, accessible only through `as_str()` and `into_inner()`. However, the unconstrained `From<&str>` and `From<String>` impls bypass any format validation, making it trivial to create IDs with arbitrary content including empty strings. The `new()` constructor accepts any `Into<String>` without validation.

- **Invariant Expression**: 6/10
  The macro-based approach is clean and consistent. However, the types do not express whether an ID was generated (UUID) versus user-supplied, and empty strings are silently accepted at construction time on the domain […]

> AGENT

All 5 review agents have completed. Here's the aggregated review:

---

# PR Review Summary — `runtime-daemon-dispatch`

## Critical Issues (4 found)

| # | Agent | Issue | Location |
|---|-------|-------|----------|
| 1 | **error-handling** | `let _ = tx.send(envelope)` silently discards output events when receiver is dropped — agent output vanishes with no indication | `runtime/io.rs:48` |
| 2 | **error-handling** | `dispatch_enqueued_tasks` logs spawn failures but never transitions task to Failed — causes infinite retry loops | `task_manager.rs:222-233` |
| 3 | **error-handling** | `NoopAgentSupervisor` used in production `run_server` path — orphans agents on shutdown, falsely fails tasks on recovery | `server.rs:150`, `shutdown.rs:40-56` |
| 4 | **code-review** | Blocking `state_store.latest_seq()` on tokio worker thread in `pending_approvals` — violates "never block in async" rule | `server.rs:657` |

## Important Issues (6 found)

| # | Agent | Issue | Location |
|---|-------|-------|----------|
| 5 | **error-handling** | Lifecycle loop has no circuit breaker — DB corruption causes infinite 250ms warn-log spam with no health degradation | `main.rs:137-155` |
| 6 | **error-handling** | Scheduler permanently skips runs with invalid graphs — run stays `Running` forever with no user-visible signal | `scheduler.rs:57-66` |
| 7 | **error-handling** | […]

> TOOL

<command-message>pr-review-toolkit:review-pr</command-message>
<command-name>/pr-review-toolkit:review-pr</command-name>

> SYSTEM

# Comprehensive PR Review

Run a comprehensive pull request review using multiple specialized agents, each focusing on a different aspect of code quality.

**Review Aspects (optional):** ""

## Review Workflow:

1. **Determine Review Scope**
   - Check git status to identify changed files
   - Parse arguments to see if user requested specific review aspects
   - Default: Run all applicable reviews

2. **Available Review Aspects:**

   - **comments** - Analyze code comment accuracy and maintainability
   - **tests** - Review test coverage quality and completeness
   - **errors** - Check error handling for silent failures
   - **types** - Analyze type design and invariants (if new types added)
   - **code** - General code review for project guidelines
   - **simplify** - Simplify code for clarity and maintainability
   - **all** - Run all applicable reviews (default)

3. **Identify Changed Files**
   - Run `git diff --name-only` to see modified files
   - Check if PR already exists: `gh pr view`
   - Identify file types and what reviews apply

4. **Determine Applicable Reviews**

   Based on changes:
   - **Always applicable**: code-reviewer (general quality)
   - **If test files changed**: pr-test-analyzer
   - **If comments/docs added**: comment-analyzer
   - **If error handling changed**: silent-failure-hunter
   - **If types added/modified**: type-design-analyzer
   - **After passing review**: code-simplifier (polish and […]

> AGENT

We just completed a full review with all 5 agents. Would you like me to:

1. **Fix the critical issues** identified in the review
2. **Re-run the review** on specific aspects (e.g., just `code` or `errors`)
3. **Something else**

The 4 critical issues from the previous review were:
- Silent output channel send discard (`io.rs:48`)
- Stuck tasks from dispatch failure (`task_manager.rs:222-233`)
- `NoopAgentSupervisor` in production path (`server.rs:150`)
- Blocking sync DB call in async handler (`server.rs:657`)