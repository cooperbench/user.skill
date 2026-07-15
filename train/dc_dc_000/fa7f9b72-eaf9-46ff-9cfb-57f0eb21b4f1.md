> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

WRITE ACCESS CONTRACT: You are running with auto-approved writes inside a writable workspace. Treat the working directory as fully writable. Do NOT preemptively skip or block tasks on permission, sandbox, or read-only grounds. Attempt every required edit; only report failure AFTER a real OS-level rejection from a specific shell command. Do not infer 'read-only' from absence of activity; absence is not denial. If a single shell command unexpectedly fails, retry with a different invocation before concluding the environment is restricted.

You are preparing an execution-ready briefing document from the approved plan.

        Project directory:
        /Users/user_c042661f/Documents/reigh-workspace/.megaplan-worktrees/phase-7-20260505/all-claude





        Idea:
Implement Phase 7 (Per-project CAS) of the ArtAgents orchestrator V1 design per docs/orchestrator-v1-plan.md section 12 (Phase 7).

LAUNCHER: every `megaplan` call = `PYENV_VERSION=3.11.11 python -m megaplan ...`.

DRIVING DISCIPLINE: After every CLI call, run `megaplan status --plan <name>` and `megaplan progress --plan <name>`. If `state == finalized` and `batches_remaining > 0`, you MUST run `megaplan execute --plan <name> --confirm-destructive --batch N` for each remaining batch sequentially. DO NOT EXIT while state != done.


PHASE 7 SCOPE (from docs/orchestrator-v1-plan.md):

- Per-project content-addressable store at `<project_slug>/.cas/<sha256>` for produces artifacts.
- When a step's produces check accepts a file, the file is moved into `.cas/<hash>` and a symlink replaces the original path. Subsequent steps that produce identical content reuse the same CAS entry (no duplication).
- Per-project, NOT a shared CAS across projects (per SD: V1 stays single-host file-based with per-project scope).
- Files touched: `artagents/core/task/`, `artagents/core/project/run.py`.

EXIT CRITERIA (from design doc):
- Artifacts stored once and linked into step produces.
- No shared CAS exists across projects.
- Symlinks resolve to `.cas/<sha256>`.
- Identical content from different steps shares one CAS entry.

WHAT TO IMPLEMENT:

1. New module `artagents/core/task/cas.py` (or similar) with:
   - `cas_path(project_dir, sha256) -> Path` — returns `<project_dir>/.cas/<sha256>`
   - `intern(project_dir, source_path) -> Path` — moves file into CAS by content hash, returns CAS path. Idempotent: if hash already exists, leaves the existing entry and discards the source.
   - `link_into_produces(cas_path, target_path)` — symlinks `target_path -> cas_path` (relative symlink so the run dir stays portable).

2. Hook the produces flow (in the runner that handles produces checks):
   - After a produces check passes for a file artifact, intern the file and replace the original path with a symlink to the CAS entry.
   - Update `events.jsonl` records to include the CAS hash for each interned artifact.

3. Tests:
   - `tests/test_cas_intern.py`: writes a file, calls intern twice with identical content, asserts only one CAS entry exists and the second call discards the duplicate source.
   - `tests/test_cas_symlink.py`: full produces flow — step writes a file, post-check it's a symlink into `.cas/<hash>`.
   - `tests/test_cas_per_project.py`: two project slugs with identical content produce two separate CAS entries (per-project scope, NOT shared).

4. Update `artagents/structure.py` to acknowledge `.cas/` as a known per-project directory if there's a directory whitelist; otherwise leave structure alone.

5. Update `.gitignore` to exclude `*/runs/*/.cas/` and `**/.cas/` if not already.

CONSTRAINTS:
- Stay within Phase 7 scope. Do NOT touch Phase 8 inbox or Phase 9 golden tests.
- Additive only. Existing tests must continue to pass.
- No new dependencies (use stdlib `hashlib` and `os.symlink`).
- Honor existing patterns: hash-chained events, gate above dispatch, file-based state.
- The CAS is per-project. There is no shared CAS across projects. Reject any design that introduces one.

STOP CONDITION: Phase 7 done when `pytest tests/` passes with new tests + the produces flow uses `.cas/<sha256>` symlinks.

        Approved plan:
        # Implementation Plan: Phase 7 — Per-Project Content-Addressable Store

## Overview

Phase 7 of the orchestrator V1 design (`docs/orchestrator-v1-plan.md` §12) introduces a **per-project** CAS at `<projects_root>/<slug>/.cas/<sha256>`. When a step's inline produces check passes for a file artifact, the file is moved into `.cas/<hash>` and the original path becomes a relative symlink to the CAS entry. Identical content from later steps reuses the same CAS entry. The CAS is **per-project**, never shared across projects (SD-008, SD-029).

The natural hook point is `_run_inline_checks()` in `artagents/core/task/gate.py:1110-1167`, which runs immediately after a check resolves `ok=True` and emits `produces_check_passed`. Phases 1–6 already landed (gate, three step kinds, produces inline checks, repeat/fan-out, lifecycle verbs, stop-hook nudge). Phase 7 is purely additive.

Project root anchor: `decision.project_root` is a `<projects_root>/<slug>/` Path; the doc's `<project_slug>/.cas/<sha256>` resolves there. After a passing check, the artifact lives at `step_dir / entry.path`. We hash that file, move it into `<project_root>/.cas/<sha256>`, and replace the original with a relative symlink. The hash is recorded on the `produces_check_passed` event so events.jsonl carries the CAS provenance.

Key invariants:
- Stdlib only (`hashlib`, `os`, `pathlib`).
- Symlinks are **relative** so the run dir stays portable.
- Idempotent intern: if the hashed CAS entry already exists, discard the duplicate source and reuse.
- Per-project scope: never walk above `<project_root>`. Each slug has its own `.cas/`.
- All registered checks (`file_nonempty`, `json_file`, `json_schema`, `audio_duration_min`, `image_dimensions`, `all_of`) operate on a single file Path, so a passing check guarantees a regular file exists at `step_dir/entry.path`. Intern runs unconditionally on that path; errors propagate (no defensive wrapping per repo style).
- The `produces_check_passed` event gains an optional `cas_sha256` field. It is omitted (not present) when intern is skipped (already-symlinked re-entry).

## Main Phase

### Step 1: Add the CAS module (`artagents/core/task/cas.py`)
**Scope:** Small
1. **Create** `artagents/core/task/cas.py` with stdlib-only imports (`hashlib`, `os`, `pathlib.Path`):
   - `cas_dir(project_dir: Path) -> Path` — returns `<project_dir>/.cas`.
   - `cas_path(project_dir: Path, sha256: str) -> Path` — returns `<project_dir>/.cas/<sha256>`.
   - `hash_file(path: Path) -> str` — streams the file in 64 KB chunks through `hashlib.sha256()` and returns the lowercase hex digest. Follows symlinks (default `open()` behavior).
   - `intern(project_dir: Path, source_path: Path) -> Path` — matches the brief's signature exactly:
     ```python
     def intern(project_dir, source_path):
         sha = hash_file(source_path)
         target = cas_path(project_dir, sha)
         target.parent.mkdir(parents=True, exist_ok=True)
         if target.exists():
             source_path.unlink()
             return target
         source_path.replace(target)
         return target
     ```
     Caller derives the hash from `target.name` if needed.
   - `link_into_produces(cas_target: Path, target_path: Path) -> None` — `rel = os.path.relpath(cas_target, target_path.parent); os.symlink(rel, target_path)`. If `target_path` exists, `target_path.unlink()` first (covers a rare race where the source is recreated mid-flow).
2. **Export** `__all__ = ["cas_dir", "cas_path", "hash_file", "intern", "link_into_produces"]`.

### Step 2: Extend the produces event with the CAS hash (`artagents/core/task/events.py`)
**Scope:** Small
1. **Update** `make_produces_check_passed_event` (`artagents/core/task/events.py:185-197`) to accept an optional `cas_sha256: str | None = None` keyword. When non-None, include `"cas_sha256": cas_sha256` in the returned dict; when None, omit the key so events that pre-date Phase 7 (and any non-file pass that we choose to skip) keep their original shape.
2. **Note**: `canonical_event_json` already uses `json.dumps(..., sort_keys=True)`, so adding the key keeps deterministic chain hashing without further change.

### Step 3: Hook intern into the produces flow (`artagents/core/task/gate.py`)
**Scope:** Medium
1. **Import** at the top of `artagents/core/task/gate.py`:
   ```python
   from artagents.core.task.cas import intern, link_into_produces
   ```
2. **Modify** `_run_inline_checks()` at `artagents/core/task/gate.py:1110-1167`. In the `result.ok` branch, before the `make_produces_check_passed_event` append at line 1159, compute `cas_sha256 = _intern_produces_artifact(decision, artifact_path)` and pass it through: `make_produces_check_passed_event(..., cas_sha256=cas_sha256)`.
3. **Implement** module-level helper `_intern_produces_artifact(decision: GateDecision, artifact_path: Path) -> str | None`:
   ```python
   def _intern_produces_artifact(decision, artifact_path):
       if decision.project_root is None:
           return None
       # Already interned (re-entry safety): skip without re-hashing.
       if artifact_path.is_symlink():
           return None
       cas_target = intern(decision.project_root, artifact_path)
       link_into_produces(cas_target, artifact_path)
       return cas_target.name
   ```
   No try/except wrapper — a real I/O failure is a bug, and the repo style prohibits defensive wrappers without concrete evidence they are needed.

### Step 4: Tests (`tests/test_cas_intern.py`, `tests/test_cas_symlink.py`, `tests/test_cas_per_project.py`)
**Scope:** Medium
1. **Create** `tests/test_cas_intern.py`:
   - `test_intern_creates_cas_entry(tmp_path)`: write `a.bin`, call `intern(project_dir, a)`, assert `.cas/<sha256>` exists, contents match, returned Path equals `cas_path(project_dir, sha)`.
   - `test_intern_idempotent_discards_duplicate_source(tmp_path)`: write `a.bin` and `b.bin` with identical bytes. `intern(project_dir, a)` then `intern(project_dir, b)`. Assert: only one entry under `.cas/`, both calls returned the same Path, `b.bin` no longer exists.
   - `test_intern_distinct_content_creates_two_entries(tmp_path)`: two files with different bytes → two entries.
2. **Create** `tests/test_cas_symlink.py`:
   - Reuse the setup from `tests/test_task_inline_checks.py:113` (`test_code_produces_check_passes_advances`). After `record_dispatch_complete(...)`:
     - `(step_dir / "out.json").is_symlink()` is True.
     - `os.readlink(step_dir / "out.json")` returns a relative path (does not start with `/`).
     - `(step_dir / "out.json").resolve()` lives under `<project_root>/.cas/` and ends with the sha256 of the original bytes.
     - The latest `produces_check_passed` event from `read_events(events_path)` has `cas_sha256` equal to that hash.
3. **Create** `tests/test_cas_per_project.py`:
   - Two projects (`projA`, `projB`) under one `tmp_projects_root`, each producing `out.json` with **identical bytes** through a one-step plan.
   - Assert each project has its own `.cas/<sha256>` (two distinct files at the same hash, one per project).
   - Assert no `tmp_projects_root/.cas/` directory exists (no shared CAS).

### Step 5: Update `.gitignore` (`/.gitignore`)
**Scope:** Small
1. **Append** an explicit pattern documenting per-project CAS directories. The existing `runs/` rule already covers `runs/*/.cas/`, but add `**/.cas/` so any depth is excluded for tooling that scans the repo:
   ```
   **/.cas/
   ```

### Step 6: Validation (`tests/`)
**Scope:** Small
1. **Run** the new tests first:
   ```
   PYENV_VERSION=3.11.11 python -m pytest tests/test_cas_intern.py tests/test_cas_symlink.py tests/test_cas_per_project.py -x
   ```
2. **Run** the existing inline-checks and kernel suites to confirm no regression in the produces flow:
   ```
   PYENV_VERSION=3.11.11 python -m pytest tests/test_task_inline_checks.py tests/test_task_kernel_e2e.py tests/test_task_kernel_events.py -x
   ```
3. **Run** the full suite as the final gate:
   ```
   PYENV_VERSION=3.11.11 python -m pytest tests/ -q
   ```
   If any frozen event-chain golden drifts because of the new `cas_sha256` field, regenerate that golden — the brief explicitly directs the hash onto events.jsonl. The `LEGACY_FIXTURE_PLAN` golden in `tests/test_task_inline_checks.py:46` is for `compute_plan_hash` (plan tree, not events) and is unaffected.

## Execution Order
1. Land `cas.py` (Step 1) and the events shape change (Step 2) first — pure additions with no caller.
2. Hook the gate (Step 3) — depends on Steps 1–2.
3. Add tests (Step 4) — depend on Steps 1–3.
4. `.gitignore` update (Step 5) — independent, can land any time.

## Validation Order
1. Run new CAS tests (cheapest, narrowest).
2. Run inline-checks / kernel-e2e tests to confirm produces flow unchanged for existing scenarios.
3. Run full `pytest tests/` as the final gate; regenerate any drifted event-hash golden only if observed.


        Plan metadata:
        {
  "version": 2,
  "timestamp": "2026-05-05T00:06:09Z",
  "hash": "sha256:f8adcf3c8b69e7678aa0eb128394620874e0537e16095b142826db3983b680b3",
  "changes_summary": "No specific flags were raised; this is a single robustness pass. Tightened the plan in three concrete ways: (1) simplified `intern`'s signature to exactly `(project_dir, source_path) -> Path` per the brief and made the implementation a five-line function (caller derives the hash from `target.name`); (2) removed the defensive `try/except OSError` wrapper around the gate hook and the corresponding \"graceful degradation\" success criterion \u2014 the repo style prohibits defensive wrappers without evidence and all registered produces checks already guarantee a real file exists when ok=True; (3) replaced the `is_file()`-based skip with a clean `is_symlink()` re-entry check (sufficient because produces_check_passed only fires after the check itself confirms the file is readable). Test list narrowed accordingly. Behavior, scope, and exit criteria unchanged.",
  "flags_addressed": [],
  "questions": [
    "Brief says 'update events.jsonl records to include the CAS hash for each interned artifact' \u2014 chosen design puts `cas_sha256` on `produces_check_passed`. A separate `produces_interned` event is cleaner for replay tooling but adds a kind that `derive_cursor` must explicitly ignore. Confirm the inline approach is acceptable.",
    "If any existing event-chain golden fixture captures `produces_check_passed` exactly, regenerating it is in-scope \u2014 confirm rather than alternative (e.g., sidecar manifest) since the brief explicitly directs the hash onto events.jsonl.",
    "Downstream consumers of produces files (e.g. `_resolve_for_each_items` reading sibling produces JSON in `gate.py:689`) use `Path.read_text()`, which transparently follows symlinks. Confirm no consumer in the kernel uses `is_file()` strictly or rejects symlinks."
  ],
  "success_criteria": [
    {
      "criterion": "`pytest tests/test_cas_intern.py tests/test_cas_symlink.py tests/test_cas_per_project.py` all pass",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "`pytest tests/` passes (no regression in existing tests, including produces inline checks and kernel e2e)",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "After a passing produces check on a file artifact, the artifact at `step_dir/<produces.path>` is a symlink resolving to `<project_root>/.cas/<sha256>` whose contents match the original",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "Identical content from two different steps in the same project shares a single CAS entry (one file under `.cas/`)",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "Two distinct project slugs with identical artifact bytes produce two separate `.cas/<sha256>` entries \u2014 no shared CAS at the projects-root level",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "`produces_check_passed` events include a `cas_sha256` field for file-backed checks (and chain integrity remains intact)",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "No new third-party dependencies introduced; `cas.py` uses only stdlib (`hashlib`, `os`, `pathlib`)",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Symlinks created by `link_into_produces` are relative (so a run dir copied/moved with its `.cas/` sibling stays valid)",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "`.gitignore` excludes `.cas/` directories",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "`cas.py` stays under ~120 lines and each function has a single responsibility",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "No code path in `gate.py` walks above `<project_root>` looking for a shared CAS",
      "priority": "should",
      "requires": [
        "read_files",
        "subjective_judgment"
      ]
    },
    {
      "criterion": "`intern` returns the CAS Path exactly as the brief specifies (`(project_dir, source_path) -> Path`); no defensive try/except wrapper around the gate hook",
      "priority": "should",
      "requires": [
        "read_files",
        "subjective_judgment"
      ]
    }
  ],
  "assumptions": [
    "`decision.project_root` (a `<projects_root>/<slug>/` Path, set in `_dispatch_code` and `_dispatch_attested`) is the correct anchor for the per-project CAS; the doc's `<project_slug>/.cas/<sha256>` resolves to this directory.",
    "Adding an optional `cas_sha256` field to `produces_check_passed` is acceptable per the brief's instruction to record the CAS hash in events.jsonl. If a frozen event-chain golden drifts, regenerating that golden is in-scope.",
    "Hooking intern inside `_run_inline_checks` covers both `code` and `attested` step kinds, since both flow through this helper.",
    "All registered produces checks operate on a single file Path; an `ok=True` result implies a real readable file at `step_dir/entry.path`. No defensive wrapper around intern is required, and intern errors should propagate as ordinary exceptions.",
    "`structure.py` validates only `artagents/` top-level package directories, not project state. The brief's 'if there's a directory whitelist; otherwise leave structure alone' clause means no change to `structure.py` is required.",
    "Phase 7 only intercepts new produces checks; pre-existing artifacts are not retroactively interned.",
    "Symlinks via `os.symlink` work on the dev/CI platforms in use (macOS Darwin per env, Linux CI). Windows is out of V1 scope per SD-029."
  ],
  "delta_from_previous_percent": 45.04,
  "structure_warnings": []
}

        Gate summary:
        {
  "recommendation": "ITERATE",
  "rationale": "Light robustness: single revision pass to incorporate critique feedback.",
  "signals_assessment": "",
  "warnings": [],
  "settled_decisions": []
}

        Flag registry:
        [
  {
    "id": "FLAG-P7-001",
    "concern": "CAS write-through corruption footgun: after intern, the produces path is a symlink to .cas/<hash>. Any subsequent write to that path (re-dispatch after crash, future Phase 8/9 replay/inbox, manual scripting, a test that pre-creates files at the produces path) silently rewrites the CAS entry through the symlink, corrupting every other produces in the project that linked to that hash. Plan should chmod 0o444 the CAS entry after the move (and clear write bits before unlinking on duplicate-discard) so writes through stale symlinks fail loudly instead of corrupting the store.",
    "evidence": "Plan step 1 specifies source_path.replace(cas_target) with no chmod follow-up, and link_into_produces creates a relative symlink with default permissions. gate.py:1095-1167 fires intern after produces passes; cursor_rewind on failure means re-dispatch of a step path is part of normal control flow, and nothing blocks a future failure-after-success path or external write from clobbering the CAS file.",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "FLAG-P7-002",
    "concern": "intern() symlink-detection branch is under-specified for non-CAS-symlink sources. The plan only covers the case where source_path is already a symlink under cas_dir. If source_path is a symlink pointing elsewhere (user-staged, stale, foreign), Path.replace() renames the symlink itself rather than the target, so the CAS could end up holding a foreign or dangling symlink at .cas/<hash-of-target> while link_into_produces then symlinks the original path to that link. Plan should hash via streaming open() of the target, copy bytes into CAS, then unlink the source symlink (or reject non-CAS symlinks loudly).",
    "evidence": "Plan step 1 intern() description covers only the already-interned-symlink case. hash_file follows symlinks via open(), but Path.replace renames the link rather than the target, producing a CAS object that is itself a symlink in this edge case.",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "verifiability-0",
    "concern": "Criterion 10: requires human verification (subjective_judgment).",
    "evidence": "",
    "status": "open",
    "severity": "minor"
  }
]

        Critique history:
        [
  {
    "iteration": 1,
    "flag_count": 3,
    "verified": []
  }
]

        Debt watch items (do not make these worse):
[]

        Requirements:
        - Produce structured JSON only.
        - `tasks` must be an ordered array of task objects. Every task object must include:
          - `id`: short stable task ID like `T1`
          - `description`: concrete work item
          - `depends_on`: array of earlier task IDs or `[]`
          - `status`: always `"pending"` at finalize time
          - `executor_notes`: always `""` at finalize time
          - `reviewer_verdict`: always `""` at finalize time
        - `watch_items` must be an array of strings covering runtime risks, critique concerns, and assumptions to keep visible during execution.
        - `sense_checks` must be an array with one verification question per task. Every sense-check object must include:
          - `id`: short stable ID like `SC1`
          - `task_id`: the related task ID
          - `question`: reviewer verification question
          - `verdict`: always `""` at finalize time
        - `user_actions` must be an array of human-only setup or operational actions. Use IDs `U1`, `U2`, ... and include `description` plus `phase` (`before_execute` or `after_execute`). Use optional `blocks_task_ids` when an action blocks specific tasks, optional `rationale` when useful, and `requires_human_only_reason` ONLY when the user_action is the sole coverage for a plan step.
- Include ONLY actions that require a human outside the executor's repo-editing work: env vars or secrets, infra access such as cloud accounts or VPN, DB migrations the human must trigger, manual UI/UX smoke tests, deploys, and out-of-band approvals.
- Anything that touches code in the repo MUST be a task, not a user_action. Reading docs, editing files, running tests, and writing migration SQL are tasks. Negative example: writing the migration SQL is a task, not a user_action.
- Positive examples: `U1: Set ANTHROPIC_API_KEY in .env (before_execute)`; `U2: Manually smoke test the production deploy in the browser (after_execute)`.
        - `meta_commentary` must be a single string with execution guidance, gotchas, or judgment calls that help the executor succeed.
        - `validation` must be an object that self-checks plan coverage:
          - `plan_steps_covered`: enumerate EVERY step from the approved plan. For each step, provide a short `plan_step_summary` (the step's intent in one phrase) and `finalize_item_ids` (array of task IDs `T*` or user_action IDs `U*` that implement or cover it — a single plan step may map to multiple tasks and/or user_actions).
          - `orphan_tasks`: task IDs that do not correspond to any plan step. Normally empty. If non-empty, explain in `completeness_notes`.
          - `completeness_notes`: free-text explanation of any gaps, deviations, or deliberate omissions.
          - `coverage_complete`: set to `true` only if every plan step has at least one finalize task or user_action AND you have verified the mapping by reviewing each entry. Set to `false` if any plan step is missing coverage.
          - Example:
          ```json
          "validation": {
            "plan_steps_covered": [
              {"plan_step_summary": "Add retry logic to API client", "finalize_item_ids": ["T1", "T2"]},
              {"plan_step_summary": "Set required production secret", "finalize_item_ids": ["U1"]}
            ],
            "orphan_tasks": [],
            "completeness_notes": "All plan steps mapped to tasks.",
            "coverage_complete": true
          }
          ```
        - Preserve information that strong existing artifacts already capture well: execution ordering, watch-outs, reviewer checkpoints, and practical context.
        - The structured output should be self-contained: an executor reading only `finalize.json` should have everything needed to work.
        - Keep the task count proportional to the work. A simple 1-2 file fix should be 2 tasks: (1) apply the fix, (2) run tests. Do NOT create separate "inspect" or "read" tasks for simple changes — the executor can read and fix in one step. Only create more tasks when the work has genuinely independent stages.
        - - The FINAL task MUST always be to run tests and verify the changes work. If specific test IDs or commands are mentioned in the original task, include them. Otherwise, the executor should find and run the tests most relevant to the files changed. If any test fails, read the error, fix the code, and re-run until they pass. Do NOT create new test files — run the project's existing test suite. Additionally, the executor should write a short throwaway script that reproduces the specific bug described in the task, run it to confirm the fix works, then delete the script.

> TOOL

tool_use StructuredOutput
```json
{}
```

> TOOL

tool_result StructuredOutput
```
Output does not match required schema: root: must have required property 'tasks', root: must have required property 'watch_items', root: must have required property 'sense_checks', root: must have required property 'user_actions', root: must have required property 'meta_commentary', root: must have required property 'validation', root: must have required property 'baseline_test_failures', root: must have required property 'baseline_test_command', root: must have required property 'baseline_test_note'
```

> TOOL

tool_use StructuredOutput
```json
{
  "tasks": [
    {
      "id": "T1",
      "description": "Create new module artagents/core/task/cas.py with stdlib-only imports (hashlib, os, pathlib.Path). Implement: cas_dir(project_dir) -> Path returning <project_dir>/.cas; cas_path(project_dir, sha256) -> Path returning <project_dir>/.cas/<sha256>; hash_file(path) streaming sha256 in 64 KB chunks (hex digest, follows symlinks via default open()); intern(project_dir, source_path) -> Path that hashes the source, ensures .cas/ exists, returns the existing target if present (and unlinks the duplicate source), otherwise source_path.replace(target); link_into_produces(cas_target, target_path) creating a RELATIVE symlink via os.path.relpath(cas_target, target_path.parent) and os.symlink(rel, target_path), unlinking target_path first if it exists. Set __all__ = ['cas_dir','cas_path','hash_file','intern','link_into_produces']. Keep file under ~120 lines, single-responsibility per function, no defensive try/except wrappers.",
      "depends_on": [],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T2",
      "description": "Extend make_produces_check_passed_event in artagents/core/task/events.py (~lines 185-197) to accept an optional cas_sha256: str | None = None keyword argument. When non-None, include 'cas_sha256': cas_sha256 in the returned dict; when None, omit the key entirely so events that pre-date Phase 7 (and any non-file pass) keep their original shape. Do NOT alter canonical_event_json — it already uses sort_keys=True so chain hashing remains deterministic.",
      "depends_on": [],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T3",
      "description": "Hook intern into the produces flow in artagents/core/task/gate.py. Add 'from artagents.core.task.cas import intern, link_into_produces' to the imports. In _run_inline_checks() (around lines 1110-1167), in the result.ok branch BEFORE the make_produces_check_passed_event append (around line 1159), compute cas_sha256 = _intern_produces_artifact(decision, artifact_path) and pass it through as a kwarg. Add module-level helper _intern_produces_artifact(decision, artifact_path) -> str | None: returns None if decision.project_root is None; returns None if artifact_path.is_symlink() (re-entry safety — already interned); otherwise calls cas_target = intern(decision.project_root, artifact_path), link_into_produces(cas_target, artifact_path), returns cas_target.name. No try/except wrapper.",
      "depends_on": [
        "T1",
        "T2"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T4",
      "description": "Create tests/test_cas_intern.py with three tests: (a) test_intern_creates_cas_entry — write a.bin, intern it, assert .cas/<sha256> exists, contents match, returned Path equals cas_path(project_dir, sha); (b) test_intern_idempotent_discards_duplicate_source — write a.bin and b.bin with identical bytes, intern both, assert exactly one entry under .cas/, both calls returned the same Path, b.bin no longer exists; (c) test_intern_distinct_content_creates_two_entries — two files with different bytes produce two distinct .cas entries.",
      "depends_on": [
        "T1"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T5",
      "description": "Create tests/test_cas_symlink.py reusing the setup pattern from tests/test_task_inline_checks.py:113 (test_code_produces_check_passes_advances). After record_dispatch_complete(...), assert: (step_dir / 'out.json').is_symlink() is True; os.readlink(step_dir / 'out.json') returns a RELATIVE path (not starting with '/'); (step_dir / 'out.json').resolve() lives under <project_root>/.cas/ and the resolved filename equals the sha256 hex of the original bytes; the latest produces_check_passed event from read_events(events_path) has cas_sha256 equal to that hash.",
      "depends_on": [
        "T1",
        "T2",
        "T3"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T6",
      "description": "Create tests/test_cas_per_project.py: under one tmp_projects_root, run two projects (slugs projA and projB) each producing out.json with IDENTICAL bytes through a one-step plan. Assert each project has its own .cas/<sha256> entry (two separate physical files at the same hash, one per project). Assert no tmp_projects_root/.cas/ directory exists (no shared CAS across projects).",
      "depends_on": [
        "T1",
        "T2",
        "T3"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T7",
      "description": "Append '**/.cas/' to the repo root .gitignore so per-project CAS directories at any depth are excluded. Confirm the existing 'runs/' rule already covers runs/*/.cas/ but add the explicit pattern for tooling that scans the repo independently.",
      "depends_on": [],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T8",
      "description": "Run tests in the prescribed order to validate Phase 7. (1) New CAS tests: PYENV_VERSION=3.11.11 python -m pytest tests/test_cas_intern.py tests/test_cas_symlink.py tests/test_cas_per_project.py -x. (2) Inline-checks/kernel regression: PYENV_VERSION=3.11.11 python -m pytest tests/test_task_inline_checks.py tests/test_task_kernel_e2e.py tests/test_task_kernel_events.py -x. (3) Full suite: PYENV_VERSION=3.11.11 python -m pytest tests/ -q. If any frozen event-chain golden drifts because of the new cas_sha256 field, regenerate that golden (the brief explicitly directs the hash onto events.jsonl). Note: LEGACY_FIXTURE_PLAN at tests/test_task_inline_checks.py:46 is for compute_plan_hash (plan tree, not events) and should NOT need regeneration. Then write a short throwaway script (delete after) that performs a one-step produces flow and prints whether out.json is a symlink resolving under .cas/ — to confirm the fix works end-to-end. If any test fails, fix the code and re-run until green. Do NOT create new test files beyond T4-T6.",
      "depends_on": [
        "T1",
        "T2",
        "T3",
        "T4",
        "T5",
        "T6",
        "T7"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    }
  ],
  "watch_items": [
    "FLAG-P7-001 (minor, open): Future writes through a stale symlink could rewrite the CAS entry through the link and corrupt every other produces in the project that linked to that hash. Plan deliberately does NOT chmod 0o444 the CAS entry — keep this risk visible. If a test or future phase exposes the footgun, the fix is to chmod 0o444 inside intern() after replace() and clear write bits before unlinking on duplicate-discard.",
    "FLAG-P7-002 (minor, open): If source_path is itself a non-CAS symlink pointing elsewhere, Path.replace() renames the link rather than the target, so .cas/<hash-of-target> would hold a foreign symlink. The is_symlink() re-entry skip in _intern_produces_artifact returns None for ANY symlink source, which sidesteps interning a foreign symlink — but it also means a foreign symlink at the produces path is left untouched (no CAS hash on the event). Keep this in mind if a downstream phase expects every passing file produces to have cas_sha256.",
    "Symlinks must be RELATIVE (os.path.relpath against target_path.parent), not absolute, so the run dir + .cas/ pair stays portable when copied or moved.",
    "intern() must be idempotent: if .cas/<sha> already exists, unlink the duplicate source and return the existing target; do NOT re-replace.",
    "Per-project scope is non-negotiable (SD-008, SD-029): never walk above <project_root> looking for a shared CAS. The third test (T6) explicitly asserts no shared CAS at projects-root level.",
    "No defensive try/except around the gate hook — the brief and design doc prohibit it. Real I/O failures should propagate.",
    "Adding the optional cas_sha256 field to produces_check_passed must NOT break the chain hash for prior events: cas_sha256 is omitted entirely (not present) when intern is skipped, so events from before Phase 7 retain their original canonical JSON shape.",
    "If a frozen event-chain golden captures produces_check_passed exactly, regenerating that golden is in-scope per the design (events.jsonl is the documented home for the CAS hash). Do NOT add a sidecar manifest as an alternative.",
    "structure.py is unchanged in this phase — confirm the directory whitelist doesn't reject runs/*/.cas/ by inspection before declaring done; if it does, that is a small additive update.",
    "The CAS hook only fires inside _run_inline_checks (the produces flow). Pre-existing artifacts are NOT retroactively interned — explicit assumption.",
    "Symlinks via os.symlink work on Darwin (dev) and Linux (CI). Windows is out of V1 scope.",
    "verifiability-0: criterion 10 (cas.py under ~120 lines, single responsibility) is human-verified; keep the module compact."
  ],
  "sense_checks": [
    {
      "id": "SC1",
      "task_id": "T1",
      "question": "Does artagents/core/task/cas.py use only stdlib (hashlib, os, pathlib), expose the five named functions, create RELATIVE symlinks in link_into_produces, and stay under ~120 lines? Does intern() match the brief's exact signature (project_dir, source_path) -> Path with the five-line body that returns the existing target on collision and unlinks the duplicate source?",
      "verdict": ""
    },
    {
      "id": "SC2",
      "task_id": "T2",
      "question": "Does make_produces_check_passed_event accept an optional cas_sha256 kwarg, omit the key entirely when None (preserving prior canonical JSON), and include it as 'cas_sha256': <hex> when provided? Is canonical_event_json untouched (still sort_keys=True)?",
      "verdict": ""
    },
    {
      "id": "SC3",
      "task_id": "T3",
      "question": "Does _run_inline_checks call _intern_produces_artifact in the result.ok branch BEFORE emitting produces_check_passed and pass cas_sha256 through? Does _intern_produces_artifact return None when decision.project_root is None or when artifact_path.is_symlink() (re-entry guard), and otherwise call intern then link_into_produces, returning cas_target.name with no try/except wrapper?",
      "verdict": ""
    },
    {
      "id": "SC4",
      "task_id": "T4",
      "question": "Do the three tests in tests/test_cas_intern.py cover (a) basic intern, (b) idempotent duplicate-source discard with single .cas entry, and (c) two distinct contents producing two entries?",
      "verdict": ""
    },
    {
      "id": "SC5",
      "task_id": "T5",
      "question": "Does tests/test_cas_symlink.py confirm out.json is a symlink, that os.readlink returns a relative path (not starting with '/'), that the resolved target lives under <project_root>/.cas/ with filename equal to the sha256 of the original bytes, AND that the latest produces_check_passed event carries that same cas_sha256?",
      "verdict": ""
    },
    {
      "id": "SC6",
      "task_id": "T6",
      "question": "Does tests/test_cas_per_project.py prove per-project scope by asserting (a) projA/.cas/<sha> and projB/.cas/<sha> both exist as separate physical files even though contents are identical, and (b) no tmp_projects_root/.cas/ directory exists?",
      "verdict": ""
    },
    {
      "id": "SC7",
      "task_id": "T7",
      "question": "Does .gitignore now include '**/.cas/' (in addition to whatever runs/ rule already exists), and is the addition minimal — no churn to unrelated entries?",
      "verdict": ""
    },
    {
      "id": "SC8",
      "task_id": "T8",
      "question": "Did the three pytest invocations all pass green (new CAS tests, inline-checks/kernel regression, full suite)? If any event-chain golden drifted, was it regenerated only because of cas_sha256 — and not because of an unrelated change? Was the throwaway repro script deleted after confirming the produces flow ends in a .cas/<sha> symlink?",
      "verdict": ""
    }
  ],
  "user_actions": [],
  "meta_commentary": "Phase 7 is purely additive on top of an already-landed Phases 1-6 codebase. The hook point is well-defined: _run_inline_checks() in artagents/core/task/gate.py around lines 1110-1167, immediately before make_produces_check_passed_event is appended. Land the new module (T1) and the events shape change (T2) first — both are self-contained additions with no caller. Then wire the gate hook (T3). Tests (T4-T6) and .gitignore (T7) can interleave; T7 is fully independent. Key design decisions to preserve while editing: (1) RELATIVE symlinks via os.path.relpath, not absolute — portability of the run dir is a stated invariant; (2) intern() is exactly the five-line body in the plan, no embellishment, idempotent on hash collision; (3) the gate hook is a thin module-level helper with NO try/except — the repo style explicitly rejects defensive wrappers without evidence, and the gate revision summary called this out; (4) cas_sha256 is OMITTED (not 'cas_sha256': None) from the event dict when intern is skipped, so canonical JSON for pre-Phase-7-shape events is byte-identical; (5) the is_symlink() re-entry check in _intern_produces_artifact handles both already-CAS-interned re-runs AND foreign symlinks (per FLAG-P7-002) by skipping cleanly. If running pytest reveals a frozen event-chain golden that captures produces_check_passed and now drifts because of the new optional field, regeneration is in-scope (per the brief's explicit direction to record the hash on events.jsonl). The LEGACY_FIXTURE_PLAN golden at tests/test_task_inline_checks.py:46 is for compute_plan_hash (plan tree), NOT events, and should NOT drift. Watch the two open critique flags (FLAG-P7-001 chmod-immutability, FLAG-P7-002 foreign-symlink edge) — the gate accepted them as minor; do not silently address them mid-execution unless a test fails specifically because of them. Stay strictly within Phase 7: do NOT touch Phase 8 inbox or Phase 9 golden tests. Do NOT modify structure.py unless the directory whitelist actually rejects .cas/ (the assumption is it doesn't, since structure.py validates artagents/ package layout, not project state).",
  "validation": {
    "plan_steps_covered": [
      {
        "plan_step_summary": "Add the CAS module artagents/core/task/cas.py (cas_dir, cas_path, hash_file, intern, link_into_produces)",
        "finalize_item_ids": [
          "T1"
        ]
      },
      {
        "plan_step_summary": "Extend make_produces_check_passed_event with optional cas_sha256 field",
        "finalize_item_ids": [
          "T2"
        ]
      },
      {
        "plan_step_summary": "Hook intern into the produces flow in gate.py via _intern_produces_artifact helper inside _run_inline_checks",
        "finalize_item_ids": [
          "T3"
        ]
      },
      {
        "plan_step_summary": "Add tests/test_cas_intern.py, tests/test_cas_symlink.py, tests/test_cas_per_project.py",
        "finalize_item_ids": [
          "T4",
          "T5",
          "T6"
        ]
      },
      {
        "plan_step_summary": "Update .gitignore to exclude .cas/ at any depth",
        "finalize_item_ids": [
          "T7"
        ]
      },
      {
        "plan_step_summary": "Validation: run new CAS tests, then inline-checks/kernel regression suite, then full pytest tests/ as final gate",
        "finalize_item_ids": [
          "T8"
        ]
      }
    ],
    "orphan_tasks": [],
    "completeness_notes": "Every plan step is mapped to at least one task. No user_actions are needed — Phase 7 is local file edits + tests with no infra, secrets, or out-of-band approvals. structure.py is intentionally not modified per the plan's stated assumption that the existing whitelist (if any) does not reject .cas/; if T8 surfaces a structure.py rejection, the executor will treat it as a small additive update during validation.",
    "coverage_complete": true
  },
  "baseline_test_command": "PYENV_VERSION=3.11.11 python -m pytest tests/ -q",
  "baseline_test_failures": [],
  "baseline_test_note": "Baseline not run during finalize — the plan's validation step (T8) runs the full suite after Phase 7 lands. Phases 1-6 are already committed (per recent commits 1115518 phase-6, 304c6ad phase-5, 9b01db6 phase-4, 73c41df phase-3, a521dda phase-2), so the suite is expected to be green at HEAD; if T8 surfaces unrelated pre-existing failures, the executor should report them and not paper over with edits."
}
```

> TOOL

tool_result StructuredOutput
```
Output does not match required schema: /sense_checks/0: must have required property 'executor_note', /sense_checks/1: must have required property 'executor_note', /sense_checks/2: must have required property 'executor_note', /sense_checks/3: must have required property 'executor_note', /sense_checks/4: must have required property 'executor_note', /sense_checks/5: must have required property 'executor_note', /sense_checks/6: must have required property 'executor_note', /sense_checks/7: must have required property 'executor_note'
```

> TOOL

tool_use StructuredOutput
```json
{
  "tasks": [
    {
      "id": "T1",
      "description": "Create new module artagents/core/task/cas.py with stdlib-only imports (hashlib, os, pathlib.Path). Implement: cas_dir(project_dir) -> Path returning <project_dir>/.cas; cas_path(project_dir, sha256) -> Path returning <project_dir>/.cas/<sha256>; hash_file(path) streaming sha256 in 64 KB chunks (hex digest, follows symlinks via default open()); intern(project_dir, source_path) -> Path that hashes the source, ensures .cas/ exists, returns the existing target if present (and unlinks the duplicate source), otherwise source_path.replace(target); link_into_produces(cas_target, target_path) creating a RELATIVE symlink via os.path.relpath(cas_target, target_path.parent) and os.symlink(rel, target_path), unlinking target_path first if it exists. Set __all__ = ['cas_dir','cas_path','hash_file','intern','link_into_produces']. Keep file under ~120 lines, single-responsibility per function, no defensive try/except wrappers.",
      "depends_on": [],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T2",
      "description": "Extend make_produces_check_passed_event in artagents/core/task/events.py (~lines 185-197) to accept an optional cas_sha256: str | None = None keyword argument. When non-None, include 'cas_sha256': cas_sha256 in the returned dict; when None, omit the key entirely so events that pre-date Phase 7 (and any non-file pass) keep their original shape. Do NOT alter canonical_event_json — it already uses sort_keys=True so chain hashing remains deterministic.",
      "depends_on": [],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T3",
      "description": "Hook intern into the produces flow in artagents/core/task/gate.py. Add 'from artagents.core.task.cas import intern, link_into_produces' to the imports. In _run_inline_checks() (around lines 1110-1167), in the result.ok branch BEFORE the make_produces_check_passed_event append (around line 1159), compute cas_sha256 = _intern_produces_artifact(decision, artifact_path) and pass it through as a kwarg. Add module-level helper _intern_produces_artifact(decision, artifact_path) -> str | None: returns None if decision.project_root is None; returns None if artifact_path.is_symlink() (re-entry safety — already interned); otherwise calls cas_target = intern(decision.project_root, artifact_path), link_into_produces(cas_target, artifact_path), returns cas_target.name. No try/except wrapper.",
      "depends_on": [
        "T1",
        "T2"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T4",
      "description": "Create tests/test_cas_intern.py with three tests: (a) test_intern_creates_cas_entry — write a.bin, intern it, assert .cas/<sha256> exists, contents match, returned Path equals cas_path(project_dir, sha); (b) test_intern_idempotent_discards_duplicate_source — write a.bin and b.bin with identical bytes, intern both, assert exactly one entry under .cas/, both calls returned the same Path, b.bin no longer exists; (c) test_intern_distinct_content_creates_two_entries — two files with different bytes produce two distinct .cas entries.",
      "depends_on": [
        "T1"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T5",
      "description": "Create tests/test_cas_symlink.py reusing the setup pattern from tests/test_task_inline_checks.py:113 (test_code_produces_check_passes_advances). After record_dispatch_complete(...), assert: (step_dir / 'out.json').is_symlink() is True; os.readlink(step_dir / 'out.json') returns a RELATIVE path (not starting with '/'); (step_dir / 'out.json').resolve() lives under <project_root>/.cas/ and the resolved filename equals the sha256 hex of the original bytes; the latest produces_check_passed event from read_events(events_path) has cas_sha256 equal to that hash.",
      "depends_on": [
        "T1",
        "T2",
        "T3"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T6",
      "description": "Create tests/test_cas_per_project.py: under one tmp_projects_root, run two projects (slugs projA and projB) each producing out.json with IDENTICAL bytes through a one-step plan. Assert each project has its own .cas/<sha256> entry (two separate physical files at the same hash, one per project). Assert no tmp_projects_root/.cas/ directory exists (no shared CAS across projects).",
      "depends_on": [
        "T1",
        "T2",
        "T3"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T7",
      "description": "Append '**/.cas/' to the repo root .gitignore so per-project CAS directories at any depth are excluded. Confirm the existing 'runs/' rule already covers runs/*/.cas/ but add the explicit pattern for tooling that scans the repo independently.",
      "depends_on": [],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    },
    {
      "id": "T8",
      "description": "Run tests in the prescribed order to validate Phase 7. (1) New CAS tests: PYENV_VERSION=3.11.11 python -m pytest tests/test_cas_intern.py tests/test_cas_symlink.py tests/test_cas_per_project.py -x. (2) Inline-checks/kernel regression: PYENV_VERSION=3.11.11 python -m pytest tests/test_task_inline_checks.py tests/test_task_kernel_e2e.py tests/test_task_kernel_events.py -x. (3) Full suite: PYENV_VERSION=3.11.11 python -m pytest tests/ -q. If any frozen event-chain golden drifts because of the new cas_sha256 field, regenerate that golden (the brief explicitly directs the hash onto events.jsonl). Note: LEGACY_FIXTURE_PLAN at tests/test_task_inline_checks.py:46 is for compute_plan_hash (plan tree, not events) and should NOT need regeneration. Then write a short throwaway script (delete after) that performs a one-step produces flow and prints whether out.json is a symlink resolving under .cas/ — to confirm the fix works end-to-end. If any test fails, fix the code and re-run until green. Do NOT create new test files beyond T4-T6.",
      "depends_on": [
        "T1",
        "T2",
        "T3",
        "T4",
        "T5",
        "T6",
        "T7"
      ],
      "status": "pending",
      "executor_notes": "",
      "files_changed": [],
      "commands_run": [],
      "auto_attributed_files": null,
      "evidence_files": [],
      "reviewer_verdict": "",
      "stance": null,
      "stop_signal": null
    }
  ],
  "watch_items": [
    "FLAG-P7-001 (minor, open): Future writes through a stale symlink could rewrite the CAS entry through the link and corrupt every other produces in the project that linked to that hash. Plan deliberately does NOT chmod 0o444 the CAS entry — keep this risk visible. If a test or future phase exposes the footgun, the fix is to chmod 0o444 inside intern() after replace() and clear write bits before unlinking on duplicate-discard.",
    "FLAG-P7-002 (minor, open): If source_path is itself a non-CAS symlink pointing elsewhere, Path.replace() renames the link rather than the target, so .cas/<hash-of-target> would hold a foreign symlink. The is_symlink() re-entry skip in _intern_produces_artifact returns None for ANY symlink source, which sidesteps interning a foreign symlink — but it also means a foreign symlink at the produces path is left untouched (no CAS hash on the event). Keep this in mind if a downstream phase expects every passing file produces to have cas_sha256.",
    "Symlinks must be RELATIVE (os.path.relpath against target_path.parent), not absolute, so the run dir + .cas/ pair stays portable when copied or moved.",
    "intern() must be idempotent: if .cas/<sha> already exists, unlink the duplicate source and return the existing target; do NOT re-replace.",
    "Per-project scope is non-negotiable (SD-008, SD-029): never walk above <project_root> looking for a shared CAS. The third test (T6) explicitly asserts no shared CAS at projects-root level.",
    "No defensive try/except around the gate hook — the brief and design doc prohibit it. Real I/O failures should propagate.",
    "Adding the optional cas_sha256 field to produces_check_passed must NOT break the chain hash for prior events: cas_sha256 is omitted entirely (not present) when intern is skipped, so events from before Phase 7 retain their original canonical JSON shape.",
    "If a frozen event-chain golden captures produces_check_passed exactly, regenerating that golden is in-scope per the design (events.jsonl is the documented home for the CAS hash). Do NOT add a sidecar manifest as an alternative.",
    "structure.py is unchanged in this phase — confirm the directory whitelist doesn't reject runs/*/.cas/ by inspection before declaring done; if it does, that is a small additive update.",
    "The CAS hook only fires inside _run_inline_checks (the produces flow). Pre-existing artifacts are NOT retroactively interned — explicit assumption.",
    "Symlinks via os.symlink work on Darwin (dev) and Linux (CI). Windows is out of V1 scope.",
    "verifiability-0: criterion 10 (cas.py under ~120 lines, single responsibility) is human-verified; keep the module compact."
  ],
  "sense_checks": [
    {
      "id": "SC1",
      "task_id": "T1",
      "question": "Does artagents/core/task/cas.py use only stdlib (hashlib, os, pathlib), expose the five named functions, create RELATIVE symlinks in link_into_produces, and stay under ~120 lines? Does intern() match the brief's exact signature (project_dir, source_path) -> Path with the five-line body that returns the existing target on collision and unlinks the duplicate source?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC2",
      "task_id": "T2",
      "question": "Does make_produces_check_passed_event accept an optional cas_sha256 kwarg, omit the key entirely when None (preserving prior canonical JSON), and include it as 'cas_sha256': <hex> when provided? Is canonical_event_json untouched (still sort_keys=True)?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC3",
      "task_id": "T3",
      "question": "Does _run_inline_checks call _intern_produces_artifact in the result.ok branch BEFORE emitting produces_check_passed and pass cas_sha256 through? Does _intern_produces_artifact return None when decision.project_root is None or when artifact_path.is_symlink() (re-entry guard), and otherwise call intern then link_into_produces, returning cas_target.name with no try/except wrapper?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC4",
      "task_id": "T4",
      "question": "Do the three tests in tests/test_cas_intern.py cover (a) basic intern, (b) idempotent duplicate-source discard with single .cas entry, and (c) two distinct contents producing two entries?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC5",
      "task_id": "T5",
      "question": "Does tests/test_cas_symlink.py confirm out.json is a symlink, that os.readlink returns a relative path (not starting with '/'), that the resolved target lives under <project_root>/.cas/ with filename equal to the sha256 of the original bytes, AND that the latest produces_check_passed event carries that same cas_sha256?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC6",
      "task_id": "T6",
      "question": "Does tests/test_cas_per_project.py prove per-project scope by asserting (a) projA/.cas/<sha> and projB/.cas/<sha> both exist as separate physical files even though contents are identical, and (b) no tmp_projects_root/.cas/ directory exists?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC7",
      "task_id": "T7",
      "question": "Does .gitignore now include '**/.cas/' (in addition to whatever runs/ rule already exists), and is the addition minimal — no churn to unrelated entries?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC8",
      "task_id": "T8",
      "question": "Did the three pytest invocations all pass green (new CAS tests, inline-checks/kernel regression, full suite)? If any event-chain golden drifted, was it regenerated only because of cas_sha256 — and not because of an unrelated change? Was the throwaway repro script deleted after confirming the produces flow ends in a .cas/<sha> symlink?",
      "executor_note": "",
      "verdict": ""
    }
  ],
  "user_actions": [],
  "meta_commentary": "Phase 7 is purely additive on top of an already-landed Phases 1-6 codebase. The hook point is well-defined: _run_inline_checks() in artagents/core/task/gate.py around lines 1110-1167, immediately before make_produces_check_passed_event is appended. Land the new module (T1) and the events shape change (T2) first — both are self-contained additions with no caller. Then wire the gate hook (T3). Tests (T4-T6) and .gitignore (T7) can interleave; T7 is fully independent. Key design decisions to preserve while editing: (1) RELATIVE symlinks via os.path.relpath, not absolute — portability of the run dir is a stated invariant; (2) intern() is exactly the five-line body in the plan, no embellishment, idempotent on hash collision; (3) the gate hook is a thin module-level helper with NO try/except — the repo style explicitly rejects defensive wrappers without evidence, and the gate revision summary called this out; (4) cas_sha256 is OMITTED (not 'cas_sha256': None) from the event dict when intern is skipped, so canonical JSON for pre-Phase-7-shape events is byte-identical; (5) the is_symlink() re-entry check in _intern_produces_artifact handles both already-CAS-interned re-runs AND foreign symlinks (per FLAG-P7-002) by skipping cleanly. If running pytest reveals a frozen event-chain golden that captures produces_check_passed and now drifts because of the new optional field, regeneration is in-scope (per the brief's explicit direction to record the hash on events.jsonl). The LEGACY_FIXTURE_PLAN golden at tests/test_task_inline_checks.py:46 is for compute_plan_hash (plan tree), NOT events, and should NOT drift. Watch the two open critique flags (FLAG-P7-001 chmod-immutability, FLAG-P7-002 foreign-symlink edge) — the gate accepted them as minor; do not silently address them mid-execution unless a test fails specifically because of them. Stay strictly within Phase 7: do NOT touch Phase 8 inbox or Phase 9 golden tests. Do NOT modify structure.py unless the directory whitelist actually rejects .cas/ (the assumption is it doesn't, since structure.py validates artagents/ package layout, not project state).",
  "validation": {
    "plan_steps_covered": [
      {
        "plan_step_summary": "Add the CAS module artagents/core/task/cas.py (cas_dir, cas_path, hash_file, intern, link_into_produces)",
        "finalize_item_ids": [
          "T1"
        ]
      },
      {
        "plan_step_summary": "Extend make_produces_check_passed_event with optional cas_sha256 field",
        "finalize_item_ids": [
          "T2"
        ]
      },
      {
        "plan_step_summary": "Hook intern into the produces flow in gate.py via _intern_produces_artifact helper inside _run_inline_checks",
        "finalize_item_ids": [
          "T3"
        ]
      },
      {
        "plan_step_summary": "Add tests/test_cas_intern.py, tests/test_cas_symlink.py, tests/test_cas_per_project.py",
        "finalize_item_ids": [
          "T4",
          "T5",
          "T6"
        ]
      },
      {
        "plan_step_summary": "Update .gitignore to exclude .cas/ at any depth",
        "finalize_item_ids": [
          "T7"
        ]
      },
      {
        "plan_step_summary": "Validation: run new CAS tests, then inline-checks/kernel regression suite, then full pytest tests/ as final gate",
        "finalize_item_ids": [
          "T8"
        ]
      }
    ],
    "orphan_tasks": [],
    "completeness_notes": "Every plan step is mapped to at least one task. No user_actions are needed — Phase 7 is local file edits + tests with no infra, secrets, or out-of-band approvals. structure.py is intentionally not modified per the plan's stated assumption that the existing whitelist (if any) does not reject .cas/; if T8 surfaces a structure.py rejection, the executor will treat it as a small additive update during validation.",
    "coverage_complete": true
  },
  "baseline_test_command": "PYENV_VERSION=3.11.11 python -m pytest tests/ -q",
  "baseline_test_failures": [],
  "baseline_test_note": "Baseline not run during finalize — the plan's validation step (T8) runs the full suite after Phase 7 lands. Phases 1-6 are already committed (per recent commits 1115518 phase-6, 304c6ad phase-5, 9b01db6 phase-4, 73c41df phase-3, a521dda phase-2), so the suite is expected to be green at HEAD; if T8 surfaces unrelated pre-existing failures, the executor should report them and not paper over with edits."
}
```

> TOOL

tool_result StructuredOutput
```
Structured output provided successfully
```

> AGENT

Finalize document submitted: 8 ordered tasks (T1 cas.py module, T2 events field, T3 gate hook, T4–T6 three test files, T7 .gitignore, T8 validation) with matching sense-checks, the two open critique flags surfaced as watch items, and full plan-step coverage. No user_actions needed — Phase 7 is local-only.
