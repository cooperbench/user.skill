> DEVELOPER

### Summary of Findings

**Critical issues:** None.

**Important issues:** None.

**Suggestions (nice to have):**

1. `/home/<USER>/Projects/AI/forge/src/cmd/run.rs` line 483 -- The `IterationAudit` is referenced via fully-qualified path `forge::audit::IterationAudit` rather than being imported alongside the other audit types at line 31. While functional, adding it to the import would be more consistent with the existing style. The import at line 31 currently reads:
   ```
   use forge::audit::{AuditLogger, FileChangeSummary, PhaseAudit, PhaseOutcome, RunConfig};
   ```
   Adding `IterationAudit` here would match the plan's intent and the codebase's convention.

### Plan Deviations Summary

| Deviation | Location | Verdict |
|-----------|----------|---------|
| `git_snapshot_after` uses `tracker.head_sha()` instead of `tracker.snapshot_before()` | `cmd/run.rs:489` | Beneficial -- avoids side effects |
| `ReviewIntegration` setup includes arbiter config, parallel, skip_permissions, forge_dir | `cmd/run.rs:104-126` | Beneficial -- fully functional review system |
| Uses `phase_audit.iterations.len()` instead of separate `completed_at_iteration` counter | `cmd/run.rs:686` | Beneficial -- simpler, equivalent |
| Council override applied through `phase_settings()` instead of inline pattern matching | `cmd/run.rs:138-139`, `forge_config.rs:711-713` | Beneficial -- better separation of concerns |
| `IterationAudit` used via qualified path instead of import | `cmd/run.rs:483` | Neutral -- stylistic |
| `COUNCIL_ENV_MUTEX` for test isolation instead of `--test-threads=1` | `council/config.rs:89` | Beneficial -- more robust |

### Conclusion […]

> DEVELOPER

### `runner.rs` Changes

**Status: Matches plan.**

- `should_use_council` at line 300 correctly uses `resolve_enabled()` (Task C2).
- `should_use_council_effective` at line 312 correctly checks `has_minimum_workers()` (Task A3).
- `run_effective_iteration` at line 345 correctly dispatches (Task A4).
- `run_council_iteration` at line 375 correctly accepts `prompt_context` and `append_system_prompt` (Task A2).

The `run_council_iteration` prompt construction at lines 389-400 uses `push_str` which is slightly more efficient than the plan's `format!("{}\n\n...", prompt, feedback)` approach since it avoids allocating a new string.

No issues found.

> DEVELOPER

### Council Config (`src/council/config.rs`)

**Status: Matches plan.**

Both `has_minimum_workers()` and `resolve_enabled()` are implemented as specified:

- `has_minimum_workers()` at line 38 checks `self.workers.len() >= 2`.
- `resolve_enabled()` at line 43 checks `COUNCIL_ENABLED` env var with boolean parsing fallback.

The implementation uses Rust 2024's `let-else` chain syntax (`if let Ok(...) && let Ok(...)`) which is clean and idiomatic.

The tests are comprehensive and include proper environment variable save/restore logic using the `COUNCIL_ENV_MUTEX` at line 89, which is a good addition to prevent test races. The plan only mentioned `--test-threads=1`; the mutex approach is more robust.

No issues found.

> DEVELOPER

### Task C4: Apply `PhaseOverride.council` in phase settings resolution

**Status: Matches plan with an improved approach.**

The plan specified adding a manual pattern-matching block in `cmd/run.rs`:
```rust
if let Some(council_override) = forge_toml
    .phases
    .overrides
    .iter()
    .find(|(pattern, _)| forge::forge_config::pattern_matches(pattern, &p.name))
    .and_then(|(_, override_cfg)| override_cfg.council)
{
    p.council = Some(council_override);
}
```

The implementation takes a cleaner approach. Instead of duplicating pattern-matching logic in `cmd/run.rs`, the `council` field was added to both `PhaseOverride` (line 213 in `forge_config.rs`) and `PhaseSettings` (line 761 in `forge_config.rs`), and the resolution happens inside `ForgeToml::phase_settings()` at lines 711-713:

```rust
if let Some(council) = override_cfg.council {
    settings.council = Some(council);
}
```

Then in `cmd/run.rs` at lines 138-139, it simply applies the resolved settings:
```rust
if p.council.is_none() {
    p.council = settings.council;
}
```

This is architecturally superior to the plan because:
1. It keeps configuration resolution in the config module rather than scattering it into command handlers.
2. It follows the same pattern used for `permission_mode` resolution (line 135-137).
3. It correctly respects explicit phase-level council settings from `phases.json` (the `p.council.is_none()` guard).

No issues found.

> DEVELOPER

### Task B2: Wire `ReviewIntegration` into sequential path

**Status: Matches plan with significant enhancements.**

The plan called for a relatively simple setup:
```rust
let review_config = if forge_toml.reviews.enabled {
    ReviewIntegrationConfig::enabled()
        .with_working_dir(project_dir.clone())
        .with_claude_cmd(&config.claude_cmd)
        .with_verbose(cli.verbose)
} else {
    ReviewIntegrationConfig::default()
};
```

The implementation at `/home/<USER>/Projects/AI/forge/src/cmd/run.rs` lines 104-126 is significantly more comprehensive:

```rust
let review_integration = if forge_toml.reviews.enabled {
    let mut arbiter = ArbiterConfig::default()
        .with_claude_cmd(&config.claude_cmd)
        .with_skip_permissions(config.skip_permissions)
        .with_verbose(cli.verbose)
        .with_confidence_threshold(forge_toml.reviews.confidence_threshold);
    arbiter.mode = forge_toml.reviews.mode.to_resolution_mode();

    let mut review_config = ReviewIntegrationConfig::enabled()
        .with_working_dir(project_dir.clone())
        .with_claude_cmd(&config.claude_cmd)
        .with_parallel(forge_toml.reviews.parallel)
        .with_verbose(cli.verbose);
    review_config.dispatcher = review_config
        .dispatcher
        .clone()
        .with_skip_permissions(config.skip_permissions)
        .with_arbiter(arbiter)
        .with_forge_dir(forge_dir.clone());
    ReviewIntegration::new(review_config)
} else {
    ReviewIntegration::new(ReviewIntegrationConfig::default())
};
```

This is a clear improvement over the plan. The plan's version was missing:
- Arbiter configuration (resolution mode, confidence threshold)
- Parallel review setting
- Skip permissions propagation
- Forge directory propagation

Without these, the review system would lack arbiter-based conflict resolution, would not respect the project's permission settings, and would default to sequential reviews even when parallel was configured. The implementation correctly wires all these configuration knobs through.

**Review execution (lines 668-712):**

The plan specified using `completed_at_iteration` to track which iteration completed the phase and passing it to `run_phase_reviews`. The implementation instead uses `phase_audit.iterations.len() as u32` at line 686. This is equivalent and arguably more robust -- […]

> DEVELOPER

### Task B1: Record `IterationAudit` entries in sequential loop

**Status: Matches plan with beneficial improvements.**

At `/home/<USER>/Projects/AI/forge/src/cmd/run.rs`, lines 399-494:

1. The timing setup at lines 399-400 (`iter_started_at` and `iter_start_instant`) matches the plan exactly.

2. The `IterationAudit` construction at lines 483-494 has a notable improvement over the plan.

**Improvement over plan (beneficial):**

The plan at Task B1 Step 3 specifies:
```rust
git_snapshot_after: Some(
    tracker
        .snapshot_before(&format!("{}-iter-{}", phase.number, iter))
        .unwrap_or_default(),
),
```

The implementation instead uses:
```rust
git_snapshot_after: tracker.head_sha(),
```

This is a better approach. The plan's version would create a new git tag/reference (via `snapshot_before`) for every iteration just to capture the SHA, which is side-effect-heavy and semantically misleading (it is calling `snapshot_before` for an "after" snapshot). The implementation correctly reads the current HEAD SHA directly via `tracker.head_sha()`, which is side-effect-free and semantically clear. This is a justified deviation.

3. The implementation uses `phase_audit.add_iteration(...)` (line 483) instead of directly pushing to `phase_audit.iterations`. This is slightly better because it uses the dedicated `add_iteration` method defined at `/home/<USER>/Projects/AI/forge/src/audit/mod.rs` line 173, which provides a cleaner API. However, the effect is identical.

4. The `IterationAudit` import is done via the fully qualified path `forge::audit::IterationAudit` inline at line 483 rather than importing it at the top of […]

> DEVELOPER

### Task A5: Replace `run_iteration_with_context` with `run_effective_iteration`

**Status: Matches plan.**

At `/home/<USER>/Projects/AI/forge/src/cmd/run.rs`, lines 403-420, the call site correctly uses `run_effective_iteration` with identical arguments to what the plan specifies. The `run_effective_iteration` method in `/home/<USER>/Projects/AI/forge/src/orchestrator/runner.rs` at lines 345-373 correctly routes to `run_council_iteration` or `run_iteration_with_context` based on the guardrailed check. The `run_iteration` convenience method at line 334 was also updated to delegate through `run_effective_iteration`, which is a good consistency improvement not explicitly in the plan but beneficial.

No issues found.

> DEVELOPER

## Code Review: Council Integration (Stream B + Task A5 + Task C4)

### Overview

I reviewed the implementation in `src/cmd/run.rs`, `src/council/config.rs`, `src/forge_config.rs`, and `src/orchestrator/runner.rs` against the plan in `docs/superpowers/plans/2026-03-11-council-integration.md`. The project compiles cleanly (only pre-existing dead code warnings in `autoresearch`).

Overall, the implementation is well-executed and follows the plan closely. The code is clean, idiomatic Rust, and handles error cases appropriately. Below are my findings organized by task.

> DEVELOPER

### 6. Summary

| Category | Count |
|----------|-------|
| Critical issues | 0 |
| Important issues | 0 |
| Suggestions | 3 |

The implementation faithfully follows the plan with several beneficial improvements:
1. Case-insensitive env var handling
2. Council override resolved through the centralized `phase_settings()` pipeline
3. More efficient string building in council prompt
4. Proper mutex-based test isolation for env var mutations
5. Production-ready review integration config

All 1554 tests pass. The code compiles cleanly. The architecture is sound -- the layered approach (`resolve_enabled` -> `should_use_council` -> `should_use_council_effective` -> `run_effective_iteration`) provides clean separation of concerns with each layer adding one responsibility.

**Relevant files reviewed:**
- `/home/<USER>/Projects/AI/forge/docs/superpowers/plans/2026-03-11-council-integration.md` -- plan document
- `/home/<USER>/Projects/AI/forge/src/council/config.rs` -- Stream A1, C1 implementation
- `/home/<USER>/Projects/AI/forge/src/orchestrator/runner.rs` -- Stream A2-A4, C2 implementation
- `/home/<USER>/Projects/AI/forge/src/forge_config.rs` -- Stream C3 implementation (PhaseOverride, PhaseSettings, phase_settings())
- `/home/<USER>/Projects/AI/forge/src/cmd/run.rs` -- Stream A5, B1, B2, C4 implementation
- `/home/<USER>/Projects/AI/forge/src/audit/mod.rs` -- Stream B1 supporting change
- `/home/<USER>/Projects/AI/forge/src/phase.rs` -- `use_council()` method on Phase (context)</result>
<usage><total_tokens>62377</total_tokens><tool_uses>35</tool_uses><duration_ms>174740</duration_ms></usage>
</task-notification>
Full transcript available at: /private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/c9de2d74-440d-4cc7-a4eb-9abcfa1a6bac/tasks/aa2043d3705f83eef.output

> DEVELOPER

### 5. Issues Found

**IMPORTANT -- No test for `resolve_enabled` integration with `should_use_council`**

There is no test that verifies the full path: env var COUNCIL_ENABLED=true -> `resolve_enabled()` returns true -> `should_use_council()` returns true. The `should_use_council` tests at lines 1501-1577 all use `with_council_env_cleared`, which removes the env var before running. This means the env override path is tested in isolation (`council/config.rs` tests) and the config path is tested in isolation (`runner.rs` tests), but the integration between them is not tested.

This is acceptable for now because the wiring is straightforward (line 305 of runner.rs just calls `config.resolve_enabled()` instead of `config.enabled`), but adding one test like "env var overrides config in runner context" would close this gap.

**SUGGESTION -- `run_effective_iteration` has no routing test**

The `test_run_effective_iteration_compiles` test (line 1643) only verifies compilation by creating and immediately dropping the future. It does not verify that the routing logic actually dispatches to council mode vs single-engine mode. Since `should_use_council_effective` is well-tested separately, this is low risk, but a mock-based test or at minimum a comment explaining the coverage gap would be helpful.

**SUGGESTION -- Warning message in `should_use_council_effective` could include a hint**

At `/home/<USER>/Projects/AI/forge/src/orchestrator/runner.rs`, line 326, the warning reads:
```
"Council is enabled but […]

> DEVELOPER

### 4. Test Coverage Assessment

**`src/council/config.rs` -- 17 tests:**
- `has_minimum_workers`: 3 tests (0, 1, 2 workers) -- covers boundary conditions
- `resolve_enabled`: 4 tests (no env, env=true, env=false, env=invalid) -- covers all branches
- Serialization, parsing, defaults: 10 tests -- comprehensive

**`src/orchestrator/runner.rs` -- 7 council-related tests:**
- `should_use_council`: 4 tests (disabled, enabled, phase override true, phase override false)
- `should_use_council_effective`: 3 tests (no workers fallback, with workers, disabled)
- `run_effective_iteration`: 1 compilation test (line 1643) -- verifies the method exists and type-checks

**`src/forge_config.rs` -- council-related tests:**
- `test_phase_override_council_field`: Tests TOML parsing of council field
- `test_phase_override_council_field_absent`: Tests default (None)
- `test_forge_toml_phase_settings_no_override`: Verifies council=None without overrides
- `test_forge_toml_phase_settings_with_council_override`: Tests pattern matching for council overrides

> DEVELOPER

### 3. Code Quality Assessment

**Naming:** Consistent and clear. `should_use_council` vs `should_use_council_effective` clearly communicates the guardrail layer. `resolve_enabled` is a good name for the env-override pattern.

**Error handling:** Properly uses `.context()` for anyhow enrichment (e.g., line 388 of runner.rs). The council config path uses `unwrap_or(false)` which is correct -- missing config means council is not available.

**Documentation:** All public methods have doc comments. The `run_effective_iteration` comment at line 344 of runner.rs is brief but adequate. The `should_use_council_effective` comment at line 311 is clear about the guardrail purpose.

**`run_iteration` backward compatibility:** The existing `run_iteration` method (line 334-342) was updated to delegate to `run_effective_iteration` with all optional params as `None`. This maintains backward compatibility for any callers that used the simpler API.

> DEVELOPER

### 2. Deviations from Plan -- Assessment

**Deviation 1 (Beneficial): `resolve_enabled()` uses `to_ascii_lowercase()` and let-chains**

Plan specified:
```rust
if let Ok(val) = std::env::var("COUNCIL_ENABLED") {
    if let Ok(parsed) = val.parse::<bool>() {
        return parsed;
    }
}
```

Implementation at `/home/<USER>/Projects/AI/forge/src/council/config.rs`, lines 43-51:
```rust
if let Ok(value) = std::env::var("COUNCIL_ENABLED")
    && let Ok(enabled) = value.to_ascii_lowercase().parse::<bool>()
{
    return enabled;
}
```

Assessment: **Beneficial.** The `to_ascii_lowercase()` call makes the env var case-insensitive (`TRUE`, `True`, `true` all work), which is more user-friendly. The let-chain syntax is idiomatic for Rust Edition 2024. No issue here.

**Deviation 2 (Beneficial): Task C4 -- council override applied via `phase_settings()` instead of inline code**

The plan (Task C4) specified adding inline code in `cmd/run.rs` to manually look up the override pattern and apply `council_override`. Instead, the implementation adds the `council` field to `PhaseSettings` and resolves it inside `ForgeToml::phase_settings()` at `/home/<USER>/Projects/AI/forge/src/forge_config.rs`, lines 711-713:
```rust
if let Some(council) = override_cfg.council {
    settings.council = Some(council);
}
```

Then in `cmd/run.rs` lines 138-140, it applies it uniformly:
```rust
if p.council.is_none() {
    p.council = settings.council;
}
```

Assessment: **Beneficial.** This is a better architecture than the plan specified. The council override flows through the same `phase_settings()` pipeline as budget, permission_mode, and context_limit overrides. This keeps `cmd/run.rs` clean […]

> DEVELOPER

### 1. Plan Alignment Analysis

**Stream A (Dispatch) -- FULLY IMPLEMENTED**

| Plan Task | Status | Notes |
|-----------|--------|-------|
| A1: `has_minimum_workers()` | Done | Exact match to plan spec |
| A2: Upgrade `run_council_iteration` signature | Done | Adds `prompt_context` and `append_system_prompt` params as planned |
| A3: `should_use_council_effective` | Done | Matches plan with minor cosmetic differences |
| A4: `run_effective_iteration` | Done | Exact match to plan spec |
| A5: Update call site in `cmd/run.rs` | Done | `run_effective_iteration` correctly replaces `run_iteration_with_context` |

**Stream C (Config) -- FULLY IMPLEMENTED**

| Plan Task | Status | Notes |
|-----------|--------|-------|
| C1: `resolve_enabled()` with env var | Done | Minor beneficial deviation in implementation |
| C2: Wire `resolve_enabled()` into `should_use_council` | Done | Exact match |
| C3: `council` field on `PhaseOverride` | Done | Exact match |
| C4: Apply `PhaseOverride.council` in phase settings | Done | Implemented differently than plan -- see details below |

**Stream B (Audit + Reviews) -- FULLY IMPLEMENTED**

| Plan Task | Status | Notes |
|-----------|--------|-------|
| B1: Record `IterationAudit` entries | Done | Uses `phase_audit.add_iteration()` instead of `.push()` |
| B2: Wire `ReviewIntegration` | Done | Richer […]

> DEVELOPER

## Code Review: Council Integration (Streams A + C)

### Executive Summary

The implementation is well-executed and closely follows the plan. All 1554 library tests pass. The code is clean, well-tested, and the architecture is sound. I found no critical issues. I have a few important observations and minor suggestions below.

> DEVELOPER

## Final Verdict

### What Was Done Well

1. The implementation faithfully follows the plan across all three streams
2. Test coverage is thorough and tests are properly isolated for env var mutation
3. Serde annotations are correct with proper backward compatibility
4. The `with_council_env_cleared()` helper is a clean pattern for env var test safety
5. The review integration setup in `cmd/run.rs` goes beyond the plan's sketch to provide production-ready configuration
6. Code organization follows existing patterns (e.g., `add_iteration()` mirrors `add_compaction_event()`)

### Issues Summary

| Severity | File | Description |
|----------|------|-------------|
| Suggestion | `src/audit/mod.rs` | No dedicated unit test for `PhaseAudit::add_iteration()` (trivial method, tested implicitly) |
| Suggestion | `src/cmd/autoresearch/mod.rs` | Unrelated changes mixed into the council integration changeset -- separate commits would improve history |

### Relevant Files

- `/home/<USER>/Projects/AI/forge/docs/superpowers/plans/2026-03-11-council-integration.md` -- the plan
- `/home/<USER>/Projects/AI/forge/src/forge_config.rs` -- Stream C: `PhaseOverride.council`, `PhaseSettings.council`, `phase_settings()` resolution
- `/home/<USER>/Projects/AI/forge/src/audit/mod.rs` -- Stream B: `PhaseAudit::add_iteration()`
- `/home/<USER>/Projects/AI/forge/src/council/config.rs` -- Tasks A1+C1: `has_minimum_workers()`, `resolve_enabled()`, `COUNCIL_ENV_MUTEX`
- `/home/<USER>/Projects/AI/forge/src/orchestrator/runner.rs` -- Tasks A2-A4, C2: `run_effective_iteration`, `should_use_council_effective`, `run_council_iteration` upgrade
- `/home/<USER>/Projects/AI/forge/src/cmd/run.rs` -- Tasks A5, B1, B2, C4: call site wiring, iteration audit, review integration, council override application
- `/home/<USER>/Projects/AI/forge/src/cmd/autoresearch/mod.rs` -- unplanned autoresearch wiring (out of scope but clean)

**Overall assessment: […]

> DEVELOPER

## 7. Cross-Cutting Concerns

### Thread Safety of Env Var Tests

The env var tests in `council/config.rs` and `orchestrator/runner.rs` both use `COUNCIL_ENV_MUTEX` for synchronization. The mutex is defined once in `council/config.rs` (line 87) and imported in `runner.rs` (line 960). All tests that touch `COUNCIL_ENABLED` acquire the lock. This is correct -- Rust's test harness runs tests in parallel by default, and env vars are process-global state.

### Serde Backward Compatibility

All new `Option<bool>` fields use `#[serde(default)]`, which means:
- Existing TOML files without `council` fields will deserialize correctly (to `None`)
- Existing JSON audit files without new fields will deserialize correctly
- No breaking changes to serialization format

### `PhaseOverride` Derives `Default`

`PhaseOverride` has `#[derive(Default)]` which gives `council: None` -- correct behavior.

> DEVELOPER

## 6. Unplanned Changes: `src/cmd/autoresearch/mod.rs`

### Assessment: NOT Related to Council Integration

This file's changes are completely unrelated to the council integration plan. The diff shows:

1. **Stub `cmd_autoresearch` replaced with working implementation** -- the placeholder `println!("autoresearch: not yet implemented")` was replaced with a full implementation that builds `LoopConfig`, creates `AutoresearchGitOps`, and delegates to `run_loop()`
2. **`StubMutator` and `StubExecutor` added** -- these implement the `PromptMutator` and `BenchmarkExecutor` traits with error-returning stubs
3. **`#[allow(dead_code)]` annotations removed** -- from `BUILT_IN_SPECIALISTS`, `expand_specialists`, and `generate_default_tag` since they are now used by the real implementation
4. **New imports added** -- `git_ops::AutoresearchGitOps`, `loop_runner::{LoopConfig, run_loop}`

### Evaluation

These changes are:
- **Out of scope** for the council integration plan -- they belong to the autoresearch feature, which is a separate workstream
- **Not harmful** to the council integration -- they modify a completely separate command (`forge autoresearch`) with no shared code paths
- **Self-consistent** -- the implementation correctly wires CLI args to `LoopConfig`, creates proper git ops, and handles dry-run/resume flags

**Recommendation:** These changes should have been committed separately and not mixed with the council integration work. They make the git history harder to understand when looking at what the council integration changed. However, since the changes […]

> DEVELOPER

## 5. Council Config (`src/council/config.rs`)

### Plan Alignment: Excellent

- **Task A1:** `has_minimum_workers()` implemented with 3 tests (empty, one, two workers)
- **Task C1:** `resolve_enabled()` implemented with env var override, 4 tests covering: no env, env true, env false, env invalid

### Implementation Quality

The `resolve_enabled()` method uses Rust 2024's let-chain syntax (`if let Ok(value) = ... && let Ok(enabled) = ...`), which is idiomatic for the declared edition. The `to_ascii_lowercase()` call before `parse::<bool>()` is a minor improvement over the plan (which just used `parse::<bool>()` directly). Since `bool::parse()` accepts "true"/"false" case-sensitively, the `to_ascii_lowercase()` makes it also handle "TRUE", "True", etc. This is a **beneficial deviation**.

The `COUNCIL_ENV_MUTEX` static (line 87) is declared `pub(crate)` and used by both the local tests and `runner.rs` tests. This is a clean approach to env var test isolation.

### Issues: None

> DEVELOPER

using agent teams and the following in context docs/superpowers/plans/2026-03-11-council-integration.md
review the implementation code

> AGENT

Good — `snapshot_sha` is set at line 281 (before the iteration loop starts) and records the SHA from the pre-phase snapshot. This is the correct "before" value for each iteration.

---

### Summary

The implementation is **faithful to the plan** with a few improvements:
1. `push_str` instead of `format!` for feedback append (less allocation)
2. `head_sha()` instead of `snapshot_before()` for post-iteration SHA (avoids creating commits)
3. Mutex-based env var test isolation (better than `--test-threads=1`)
4. More complete `ReviewIntegration` setup with arbiter/dispatcher configuration
5. Phase review specialist wiring from forge_toml (necessary for reviews to work)

**One housekeeping item**: The `autoresearch/mod.rs` changes should be committed separately — they're unrelated to council integration.

> METADATA

<task-notification>
<task-id>adc6ad759dc1b8209</task-id>
<tool-use-id>REDACTED</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/c9de2d74-440d-4cc7-a4eb-9abcfa1a6bac/tasks/adc6ad759dc1b8209.output</output-file>
<status>completed</status>
<summary>Agent "Review cmd/run.rs changes" completed</summary>
<result>Now I have a thorough understanding of both the plan and the implementation. Let me compile my review.

---

## Code Review: Council Integration (Stream B + Task A5 + Task C4)

### Overview

I reviewed the implementation in `src/cmd/run.rs`, `src/council/config.rs`, `src/forge_config.rs`, and `src/orchestrator/runner.rs` against the plan in `docs/superpowers/plans/2026-03-11-council-integration.md`. The project compiles cleanly (only pre-existing dead code warnings in `autoresearch`).

Overall, the implementation is well-executed and follows the plan closely. The code is clean, idiomatic Rust, and handles error cases appropriately. Below are my findings organized by task.

---

### Task A5: Replace `run_iteration_with_context` with `run_effective_iteration`

**Status: Matches plan.**

At `/home/<USER>/Projects/AI/forge/src/cmd/run.rs`, lines 403-420, the call site correctly uses `run_effective_iteration` with identical arguments to what the plan specifies. The `run_effective_iteration` method in `/home/<USER>/Projects/AI/forge/src/orchestrator/runner.rs` at lines 345-373 correctly routes to `run_council_iteration` or `run_iteration_with_context` based on the guardrailed check. The `run_iteration` convenience method at line 334 was also updated to delegate through `run_effective_iteration`, which is a good consistency improvement not explicitly in the plan but beneficial.

No issues found.

---

### Task B1: Record `IterationAudit` entries in sequential loop

**Status: Matches plan with beneficial improvements.**

At `/home/<USER>/Projects/AI/forge/src/cmd/run.rs`, lines 399-494:

1. The timing setup […]

> METADATA

<task-notification>
<task-id>aa2043d3705f83eef</task-id>
<tool-use-id>toolu_01DacdLPxJptJVPtx3hLvZAm</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/c9de2d74-440d-4cc7-a4eb-9abcfa1a6bac/tasks/aa2043d3705f83eef.output</output-file>
<status>completed</status>
<summary>Agent "Review council config changes" completed</summary>
<result>All 1554 tests pass. Now I have all the information needed for a comprehensive review.

---

## Code Review: Council Integration (Streams A + C)

### Executive Summary

The implementation is well-executed and closely follows the plan. All 1554 library tests pass. The code is clean, well-tested, and the architecture is sound. I found no critical issues. I have a few important observations and minor suggestions below.

---

### 1. Plan Alignment Analysis

**Stream A (Dispatch) -- FULLY IMPLEMENTED**

| Plan Task | Status | Notes |
|-----------|--------|-------|
| A1: `has_minimum_workers()` | Done | Exact match to plan spec |
| A2: Upgrade `run_council_iteration` signature | Done | Adds `prompt_context` and `append_system_prompt` params as planned |
| A3: `should_use_council_effective` | Done | Matches plan with minor cosmetic differences |
| A4: `run_effective_iteration` | Done | Exact match to plan spec |
| A5: Update call site in `cmd/run.rs` | Done | `run_effective_iteration` correctly replaces `run_iteration_with_context` |

**Stream C (Config) -- FULLY IMPLEMENTED**

| Plan Task | Status | Notes |
|-----------|--------|-------|
| C1: `resolve_enabled()` with env var | Done | Minor beneficial deviation in implementation |
| C2: Wire […]

> METADATA

<task-notification>
<task-id>a6052520d0af782af</task-id>
<tool-use-id>REDACTED</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/c9de2d74-440d-4cc7-a4eb-9abcfa1a6bac/tasks/a6052520d0af782af.output</output-file>
<status>completed</status>
<summary>Agent "Review forge_config + audit changes" completed</summary>
<result>`tracker.head_sha()` returns `Option<String>`, and the `IterationAudit.git_snapshot_after` field is typed `Option<String>`, so the types align. The plan's approach used `snapshot_before()` which creates a git tag/snapshot, while `head_sha()` just reads the current HEAD. The implementation's approach is simpler and avoids creating extra git refs per iteration -- this is a **reasonable simplification** that still captures the post-iteration git state.

---

## 5. Council Config (`src/council/config.rs`)

### Plan Alignment: Excellent

- **Task A1:** `has_minimum_workers()` implemented with 3 tests (empty, one, two workers)
- **Task C1:** `resolve_enabled()` implemented with env var override, 4 tests covering: no env, env true, env false, env invalid

### Implementation Quality

The `resolve_enabled()` method uses Rust 2024's let-chain syntax (`if let Ok(value) = ... && let Ok(enabled) = ...`), which is idiomatic for the declared edition. The `to_ascii_lowercase()` call before `parse::<bool>()` is a minor improvement over the plan (which just used `parse::<bool>()` directly). Since `bool::parse()` accepts "true"/"false" case-sensitively, the `to_ascii_lowercase()` makes it also handle "TRUE", "True", etc. This is a **beneficial deviation**.

The `COUNCIL_ENV_MUTEX` static (line 87) is declared `pub(crate)` and used by both the local tests and `runner.rs` tests. This is a clean approach to env […]

> AGENT

All three review agents have completed. Here's the consolidated verdict:

---

## Review Summary: Council Integration

### Verdict: **Solid implementation, ready to proceed.**

**Build/Tests**: 1554 tests pass, clean build, no new clippy warnings.

### All plan tasks are fully implemented:

| Stream | Tasks | Status |
|--------|-------|--------|
| A (Dispatch) | A1-A5 | Complete |
| B (Audit + Reviews) | B1-B2 | Complete |
| C (Config) | C1-C4 | Complete |

### Beneficial deviations from plan (all three reviewers agree):

1. **`tracker.head_sha()`** instead of `snapshot_before()` for `git_snapshot_after` — avoids creating unwanted snapshot commits
2. **`push_str`** instead of `format!` for feedback append — avoids extra allocation
3. **`COUNCIL_ENV_MUTEX`** instead of `--test-threads=1` — more robust test isolation
4. **Council override via `phase_settings()`** pipeline instead of inline pattern matching in `cmd/run.rs` — better separation of concerns
5. **Richer `ReviewIntegration` setup** with arbiter config, parallel, skip_permissions — production-ready vs stub
6. **`to_ascii_lowercase()`** in `resolve_enabled()` — handles "TRUE"/"True" etc.

### Suggestions (all minor, none blocking):

1. **Warning message** in `should_use_council_effective` dropped the actionable hint `"Add at least 2 workers in [council.workers] in forge.toml"` — consider adding it back
2. **`IterationAudit`** is used via qualified path at `cmd/run.rs:483` rather than imported alongside other […]

> DEVELOPER

lets implement the suggestions using agent teams

> AGENT

Three agents launched in parallel:
1. **Warning hint** — adding actionable message to `should_use_council_effective` in `runner.rs`
2. **Import cleanup** — moving `IterationAudit` to the import block in `cmd/run.rs`
3. **Integration tests** — adding env var override tests for `should_use_council` in `runner.rs`

Waiting for all three to complete...

> METADATA

<task-notification>
<task-id>a18f6654d9887b82e</task-id>
<tool-use-id>REDACTED</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/c9de2d74-440d-4cc7-a4eb-9abcfa1a6bac/tasks/a18f6654d9887b82e.output</output-file>
<status>completed</status>
<summary>Agent "Add actionable hint to warning" completed</summary>
<result>Done. Updated the warning message at line 326 in `/home/<USER>/Projects/AI/forge/src/orchestrator/runner.rs` to include the actionable hint: `Add at least 2 workers in [council.workers] in forge.toml.`</result>
<usage><total_tokens>11874</total_tokens><tool_uses>3</tool_uses><duration_ms>43005</duration_ms></usage>
</task-notification>
Full transcript available at: /private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/c9de2d74-440d-4cc7-a4eb-9abcfa1a6bac/tasks/a18f6654d9887b82e.output

> AGENT

Agent 1 (warning hint) done. Waiting for the other two...

> METADATA

<task-notification>
<task-id>a55f02729125c1c81</task-id>
<tool-use-id>REDACTED</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/c9de2d74-440d-4cc7-a4eb-9abcfa1a6bac/tasks/a55f02729125c1c81.output</output-file>
<status>completed</status>
<summary>Agent "Add IterationAudit to imports" completed</summary>
<result>Both changes have been made to `/home/<USER>/Projects/AI/forge/src/cmd/run.rs`:

1. **Line 31**: Added `IterationAudit` to the import statement.
2. **Line 483**: Changed `forge::audit::IterationAudit {` to `IterationAudit {`.</result>
<usage><total_tokens>22880</total_tokens><tool_uses>3</tool_uses><duration_ms>47752</duration_ms></usage>
</task-notification>
Full transcript available at: /private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/c9de2d74-440d-4cc7-a4eb-9abcfa1a6bac/tasks/a55f02729125c1c81.output

> AGENT

Agent 2 (import cleanup) done. Waiting for agent 3...

> METADATA

<task-notification>
<task-id>a566a1febfde0b748</task-id>
<tool-use-id>REDACTED</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/c9de2d74-440d-4cc7-a4eb-9abcfa1a6bac/tasks/a566a1febfde0b748.output</output-file>
<status>completed</status>
<summary>Agent "Add env var integration test" completed</summary>
<result>Both tests compile and pass. I added the two tests to `/home/<USER>/Projects/AI/forge/src/orchestrator/runner.rs` after the existing `test_should_use_council_effective_disabled` test:

1. **`test_should_use_council_env_override_enables`** - Verifies that setting `COUNCIL_ENABLED=true` env var causes `should_use_council()` to return `true` even when the config has `enabled = false`.

2. **`test_should_use_council_env_override_disables`** - Verifies the reverse: `COUNCIL_ENABLED=false` env var causes `should_use_council()` to return `false` even when the config has `enabled = true`.</result>
<usage><total_tokens>14520</total_tokens><tool_uses>5</tool_uses><duration_ms>65631</duration_ms></usage>
</task-notification>
Full transcript available at: /private/tmp/claude-501/-Users-jdsingh-Projects-AI-forge/c9de2d74-440d-4cc7-a4eb-9abcfa1a6bac/tasks/a566a1febfde0b748.output

> AGENT

All three suggestions implemented. Build passes, **1556 tests pass** (up from 1554 — the 2 new env var integration tests).

Summary of changes:
1. **Warning hint** — `runner.rs:326` now includes `"Add at least 2 workers in [council.workers] in forge.toml."`
2. **Import cleanup** — `cmd/run.rs` imports `IterationAudit` at line 31 and uses the short name at the construction site
3. **Integration tests** — 2 new tests in `runner.rs` verify the full env var → `resolve_enabled()` → `should_use_council()` path in both directions