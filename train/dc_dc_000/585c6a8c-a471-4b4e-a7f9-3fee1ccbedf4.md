> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

WRITE ACCESS CONTRACT: You are running with auto-approved writes inside a writable workspace. Treat the working directory as fully writable. Do NOT preemptively skip or block tasks on permission, sandbox, or read-only grounds. Attempt every required edit; only report failure AFTER a real OS-level rejection from a specific shell command. Do not infer 'read-only' from absence of activity; absence is not denial. If a single shell command unexpectedly fails, retry with a different invocation before concluding the environment is restricted.

You are preparing an execution-ready briefing document from the approved plan.

        Project directory:
        /Users/user_c042661f/Documents/reigh-workspace/.megaplan-worktrees/phase-9-20260505/all-claude





        Idea:
Implement Phase 9 (Author test with golden runs) of the ArtAgents orchestrator V1 design per docs/orchestrator-v1-plan.md section 12 (Phase 9).

LAUNCHER: every `megaplan` call = `PYENV_VERSION=3.11.11 python -m megaplan ...`.

DRIVING DISCIPLINE: After every CLI call, run `megaplan status --plan <name>` and `megaplan progress --plan <name>`. If `state == finalized` and `batches_remaining > 0`, you MUST run `megaplan execute --plan <name> --confirm-destructive --batch N` for each remaining batch sequentially. DO NOT EXIT while state != done.


PHASE 9 SCOPE (from docs/orchestrator-v1-plan.md):

- `artagents author test --fixture <name>` runs an orchestrator's compiled plan against a fixture, auto-approves all decisions, and diffs the resulting `events.jsonl` against `<pack>/golden/<fixture>.events.jsonl`.
- Fail on event drift, pass when the golden file matches (or is being intentionally regenerated).
- Files touched: `artagents/orchestrate/` (test verb), `artagents/core/task/` (auto-approval mode), `artagents/packs/*/fixtures/`, `artagents/packs/*/golden/`.

EXIT CRITERIA (from design doc):
- Fixture tests fail on event drift and pass when intentionally regenerated.

WHAT TO IMPLEMENT:

1. Author-test CLI (in artagents/orchestrate/cli.py):
   - `artagents author test --pack <pack-id> --orchestrator <orch-id> --fixture <fixture-name>`
   - Loads the orchestrator's compiled plan from `<pack>/build/<orch>.json`.
   - Loads the fixture from `<pack>/fixtures/<fixture-name>/` — fixture provides initial inputs and any external artifacts the steps need.
   - Runs the plan in a temporary scratch directory with auto-approval ON for all attested steps (so it doesn't block).
   - After completion, normalizes the resulting `events.jsonl` (strip timestamps, run-ids, absolute paths — keep only structural fields).
   - Diffs against `<pack>/golden/<fixture-name>.events.jsonl`.
   - Returns 0 on match, 1 on drift with a unified diff printed.

2. Auto-approval mode for attested steps (in core/task/lifecycle_ack.py or new helper):
   - When `ARTAGENTS_AUTHOR_TEST=1` is set, attested steps that would normally block on user ack auto-approve and record a synthetic ack event marked `source: author_test`.
   - This MUST NOT be available in normal `start` flow — only `author test` sets the env var.

3. Event normalization helper (artagents/core/task/normalize.py):
   - Strip volatile fields: `timestamp`, `run_id`, `pid`, absolute paths (replace with `<RUN_DIR>/<rel>`).
   - Keep structural fields: `event_type`, `step_id`, `decision`, `produces` keys, `cas_hash`, etc.
   - Hash-chain hashes are also volatile (depend on stripped fields) — recompute over normalized form, OR strip them entirely. Pick one and document.

4. Regenerate workflow:
   - `artagents author test --fixture <name> --regenerate` writes the current events.jsonl as the new golden.
   - Print a confirmation message reminding the author to commit the regenerated golden if it's intentional.

5. Golden fixture for the canonical hype orchestrator:
   - `artagents/packs/builtin/hype/fixtures/smoke/` — minimal inputs (a small audio file or stub).
   - `artagents/packs/builtin/hype/golden/smoke.events.jsonl` — the expected event sequence.

6. Tests:
   - `tests/test_author_test_pass.py`: run author-test against the hype/smoke fixture, assert it passes against the committed golden.
   - `tests/test_author_test_drift.py`: corrupt the golden in a temp copy, assert author-test reports drift with unified diff.
   - `tests/test_author_test_regenerate.py`: run with --regenerate, assert golden file is rewritten.
   - `tests/test_author_test_auto_approval.py`: assert auto-approval only fires when ARTAGENTS_AUTHOR_TEST=1.

CONSTRAINTS:
- This is the LAST phase of the V1 design. Polish matters here.
- Additive only. Existing tests must continue to pass.
- No new dependencies (stdlib only).
- The author-test must NOT touch real project state — runs in scratch dirs.
- Honor existing patterns: hash-chained events, gate above dispatch, file-based state, per-project CAS.

STOP CONDITION: Phase 9 done when `pytest tests/` passes with new tests + `artagents author test --pack builtin --orchestrator hype --fixture smoke` exits 0 against a committed golden file.

        Approved plan:

# Implementation Plan: Phase 9 — `artagents author test` with golden runs

## Overview

Phase 9 turns `artagents author test --fixture <name>` from the Phase 5 file-vs-file scaffold into a real replay harness:

1. Compile the orchestrator's plan, run it end-to-end in a scratch projects-root with auto-approval for attested steps, capture `events.jsonl`, normalize, and diff against `<pack>/golden/<fixture>.events.jsonl`.
2. Add `--regenerate` to rewrite the golden.
3. Provide a canonical `builtin/hype` smoke fixture and committed golden.

Repo shape:
- DSL + compile already exist (`artagents/orchestrate/{dsl.py,compile.py,cli.py}`); compile writes `<pack>/build/<name>.json`.
- Lifecycle verbs in `artagents/core/task/lifecycle.py` and `lifecycle_ack.py`.
- Gate at `artagents/core/task/gate.py:510 gate_command`, `790 _dispatch_code`, `904 _dispatch_attested`, `1064 validate_attested_identity`, `1096 record_dispatch_complete`, `1218 command_for_argv`.
- Hash-chained events in `artagents/core/task/events.py:25 append_event`.
- Phase 5 `_cmd_test` scaffold lives at `artagents/orchestrate/cli.py:311` (file-vs-file diff only).
- Existing scaffold tests in `tests/test_author_test_scaffold.py` lock in the Phase-5 placeholder behavior.
- DSL resolver loads `<pack>/<name>.py` via `spec_from_file_location` — `artagents/packs/builtin/hype.py` (sibling file) is not shadowed by the existing `artagents/packs/builtin/hype/` folder.

Constraints from the brief: stdlib only, additive, scratch dirs only, preserve hash-chained events.

Driving discipline: for each `megaplan` invocation, status + progress + execute remaining batches sequentially until `state == done`.

## Main Phase

### Step 1: Audit replay touch points (`artagents/orchestrate/cli.py`, `artagents/core/task/{gate.py,lifecycle.py,lifecycle_ack.py,events.py}`)
**Scope:** Small
1. **Confirm** `gate_command` (`artagents/core/task/gate.py:510`) is the in-process entry for code-step dispatch and `record_dispatch_complete` (`gate.py:1096`) writes `step_completed`. Both will be reused directly.
2. **Confirm** attested steps require external `cmd_ack` (`artagents/core/task/lifecycle_ack.py:102`) which calls `validate_attested_identity` (`gate.py:1064`); Phase 9 branches that function on `ARTAGENTS_AUTHOR_TEST=1`.
3. **Note** `tests/test_task_kernel_attested.py:142,160` and `tests/test_inbox_consume.py:61` already assert `attestor_kind in {"agent","actor"}`. Phase 9 must keep that enum intact and stamp author-test provenance on a separate `source` field (per FLAG-P9-002).
4. **Note** the existing Phase 5 scaffold at `artagents/orchestrate/cli.py:287-371` (`_strip_volatile`, `_cmd_test`) — Phase 9 replaces both. The scaffold tests in `tests/test_author_test_scaffold.py` will be removed.

### Step 2: Add the auto-approval branch (`artagents/core/task/env.py`, `artagents/core/task/gate.py`)
**Scope:** Medium
1. **Define** in `artagents/core/task/env.py`: constant `ARTAGENTS_AUTHOR_TEST = "ARTAGENTS_AUTHOR_TEST"` and helper `is_author_test_mode() -> bool` returning `os.environ.get(ARTAGENTS_AUTHOR_TEST) == "1"`. Mirror `task_actor_env`.
2. **Branch identity validation only — never the kind.** Modify `validate_attested_identity` (`artagents/core/task/gate.py:1064`) so that when `is_author_test_mode()` is true:
   - The `--agent`/`--actor` exclusivity rule still fires (rejects both flags set, rejects neither set).
   - The `step.ack.kind == "agent"` branch still requires `args.agent`; returns `("agent", args.agent)` — the canonical kind.
   - The `step.ack.kind == "actor"` branch still requires `args.actor`, BUT skips the `task_actor_env() == args.actor` check and the self-ack rejection; returns `("actor", args.actor)` — the canonical kind.
   - Author-test mode never returns `"author_test"` as `attestor_kind` (per FLAG-P9-002). The author-test marker rides on the separate `source` field in Step 2.3.
3. **Stamp `source="author_test"` independently** in `_dispatch_attested` (`gate.py:904`): when `is_author_test_mode()` is true, after building the `step_attested` / `item_attested` event dict via the existing factories, mutate it with `event["source"] = "author_test"` before `append_event`. Event factories in `events.py` stay pure.
4. **No `cmd_start` guard.** Per FLAG-P9-001, `cmd_start` does not check or reject on `ARTAGENTS_AUTHOR_TEST` — that would deadlock the test runner (which needs the var live across `cmd_start` so subsequent gate dispatch sees author-test mode). The "must not be available in normal start flow" constraint is satisfied structurally: `cmd_start` itself never sets the variable, only `_cmd_test` does, and the test runner sets/restores it within a save/restore block scoped to `run_fixture`. A user who manually exports the variable can bypass identity checks; that's documented as an internal/test-only knob in code comments, consistent with the honor-model boundary in the design doc (SD-025).

### Step 3: Add the event normalization helper (`artagents/core/task/normalize.py`)
**Scope:** Small
1. **Create** module `artagents/core/task/normalize.py` exporting `normalize_events(events: list[dict], *, run_dir: Path | None) -> list[dict]`.
2. **Strip** volatile fields per event: `ts`, `hash`, `run_id`, `pid` (if present). Recursively rewrite any string value that begins with `str(run_dir)` to `"<RUN_DIR>/" + relative_remainder`. Walk dict and list values.
3. **Document** the choice in a one-line module comment: `# We strip 'hash' rather than recomputing — chain hashes are downstream of stripped fields, and structural drift is the diff signal.`
4. **Expose** `dump_events_jsonl(events, path)` writing one canonical `json.dumps(..., sort_keys=True, separators=(",", ":"), ensure_ascii=False)` per line — used by both `--regenerate` and the diff path.

### Step 4: Build the replay driver (`artagents/orchestrate/test_runner.py`)
**Scope:** Medium
1. **Create** `artagents/orchestrate/test_runner.py` with one public function:
   ```python
   def run_fixture(
       *,
       qualified_id: str,
       fixture_dir: Path | None,
       packs_root: Path,
       projects_root: Path,
       project_slug: str = "author_test",
       run_id: str = "fixture_run",
   ) -> Path:  # returns events.jsonl path
   ```
2. **Drive** the run inside a save/restore env block:
   - Save current `ARTAGENTS_AUTHOR_TEST` and `ARTAGENTS_ACTOR`. Set `ARTAGENTS_AUTHOR_TEST=1` and `ARTAGENTS_ACTOR="author_test"`. Restore both in a `finally`.
   - If `fixture_dir` is provided and exists, `shutil.copytree(fixture_dir, projects_root / project_slug, dirs_exist_ok=True)` (so step argv that reads relative inputs finds them).
   - Call `cmd_start([qualified_id, "--project", project_slug, "--name", run_id], packs_root=packs_root, projects_root=projects_root)` — the env var is already live, but `cmd_start` does NOT inspect it (per Step 2.4), so start succeeds normally.
   - Loop until `peek_current_step` reports exhausted (cap 200 iterations to fail loud on author bugs):
     - Code step: build `cmd_str = peek.step.command`. Call `gate_command(slug, cmd_str, shlex.split(cmd_str), root=projects_root)` to log `step_dispatched`. Run the argv with `subprocess.run(cmd_argv, env={**os.environ, **child_subprocess_env(...)}, check=False)`. Call `record_dispatch_complete(decision, rc)` to log `step_completed` and run inline produces checks.
     - Attested step: read `peek.step.ack.kind` (`"agent"` or `"actor"`). Build the right ack flags: `["--agent", "author_test"]` for agent kind, `["--actor", "author_test"]` for actor kind. Call `cmd_ack([path_str, "--project", slug, "--decision", "approve", *flag_pair], projects_root=projects_root)`. Step 2.2's branch keeps `attestor_kind` canonical (`"agent"` or `"actor"`); Step 2.3 stamps `source="author_test"` on the resulting event.
3. **Return** `projects_root / project_slug / "runs" / run_id / "events.jsonl"`.

### Step 5: Rewrite `_cmd_test` and add `--regenerate` (`artagents/orchestrate/cli.py`)
**Scope:** Medium
1. **Replace** `_cmd_test` body (`artagents/orchestrate/cli.py:311-371`) with the Phase 9 implementation:
   - Resolve packs root. If `<pack>/build/<name>.json` is missing, call `compile_to_path(qid, packs_root=packs_root)` first (saves authors a step).
   - Use `tempfile.TemporaryDirectory()` for the scratch projects root.
   - Resolve `fixture_dir = packs_root / pack / "fixtures" / fixture_name` (pass `None` when missing/empty so `run_fixture` skips the copy step).
   - Call `run_fixture(...)` from Step 4. Read events via `read_events`, normalize via `normalize_events(events, run_dir=run_dir)`, render canonical JSONL lines.
   - If `--regenerate`: write golden, print `wrote <path> — commit if intentional`, return 0.
   - Else: read golden (missing/empty without `--regenerate` → exit 1 with "no committed golden; rerun with --regenerate to create one"). Compare normalized line lists. Return 0 on match. On drift, print `difflib.unified_diff(...)` to stdout and return 1.
2. **Wire** the parser in `_build_parser` (`cli.py:462`): `test_p.add_argument("--regenerate", action="store_true")`. Thread `args.regenerate` through `main` (`cli.py:474`) into `_cmd_test`.
3. **Drop** the now-dead `_VOLATILE_EVENT_FIELDS` / `_strip_volatile` helpers (logic moved to `normalize.py`).

### Step 6: Author the canonical hype DSL fixture (`artagents/packs/builtin/hype.py`, `artagents/packs/builtin/fixtures/smoke/`, `artagents/packs/builtin/golden/smoke.events.jsonl`)
**Scope:** Small
1. **Create** `artagents/packs/builtin/hype.py` (sibling file to the legacy `hype/` folder; not shadowed by `spec_from_file_location` loading) with a minimal DSL plan that compiles to `builtin.hype` and runs deterministically on stock Python:
   ```python
   from artagents.orchestrate import orchestrator, code, attested
   @orchestrator("builtin.hype")
   def main():
       return [
           code("noop", argv=["python3", "-c", "print('ok')"]),
           attested("review", command="echo review", instructions="approve to finish", ack="actor"),
       ]
   ```
   Rationale: legacy hype (`orchestrator.yaml` + `hype/run.py`) drives a heavy real-video pipeline. The Phase 9 smoke fixture must be fast and deterministic. This DSL stub is the V1 shape future phases extend; the legacy folder is untouched.
2. **Create** `artagents/packs/builtin/fixtures/smoke/.keep` so the fixture directory exists (no inputs required).
3. **Mint** `artagents/packs/builtin/golden/smoke.events.jsonl` by running `--regenerate` once locally. Spot-check the content: `run_started` → `step_dispatched`/`step_completed` for `noop` → `step_attested` for `review` with `attestor_kind="actor"`, `attestor_id="author_test"`, `source="author_test"`. Commit the file.

### Step 7: Tests (`tests/test_author_test_*`, remove `tests/test_author_test_scaffold.py`)
**Scope:** Medium
1. **Delete** `tests/test_author_test_scaffold.py` — its assertions encode the Phase 5 stub Phase 9 replaces (the docstring explicitly says "the runtime replay path is Phase 9").
2. **Add** `tests/test_author_test_pass.py`: run `author_cli.main(["test", "builtin.hype", "--fixture", "smoke"])` against the real `artagents/packs` root. Assert `rc == 0` and stdout contains `ok builtin.hype --fixture smoke`.
3. **Add** `tests/test_author_test_drift.py`: copy `artagents/packs` to a `tmp_path` packs root via `shutil.copytree`, mutate `golden/smoke.events.jsonl` (e.g. flip a `kind` value), run with `packs_root=<tmp>`, assert `rc == 1` and stdout includes `--- golden/smoke.events.jsonl` and `+++` from `difflib.unified_diff`.
4. **Add** `tests/test_author_test_regenerate.py`: same temp-pack copy. Truncate golden to empty. Run with `--regenerate`. Assert `rc == 0`, golden non-empty, byte-equal to the committed golden (regeneration is deterministic given normalized content).
5. **Add** `tests/test_author_test_auto_approval.py`:
   - Build a tiny demo pack with one `attested` step in a `tmp_path`. Without `ARTAGENTS_AUTHOR_TEST` set: call `cmd_ack` with `--actor` mismatching `ARTAGENTS_ACTOR` → assert non-zero exit (existing behavior preserved). With `ARTAGENTS_AUTHOR_TEST=1`: same mismatched `--actor` → assert success, last event has `kind="step_attested"`, `attestor_kind="actor"` (NOT `"author_test"` — verifies FLAG-P9-002 fix), `source="author_test"`.
   - Assert `cmd_start` succeeds (does NOT reject) when launched with `ARTAGENTS_AUTHOR_TEST=1` in env (verifies FLAG-P9-001 fix: no guard).
   - Use save/restore for env vars to keep the test isolated.

### Step 8: Validation (`pytest`, manual CLI run)
**Scope:** Small
1. Run targeted tests first: `pytest tests/test_author_test_pass.py tests/test_author_test_drift.py tests/test_author_test_regenerate.py tests/test_author_test_auto_approval.py -x`.
2. Run the full suite: `pytest tests/`. Existing tests should pass; only the deleted scaffold suite is gone.
3. Manual smoke: `PYENV_VERSION=3.11.11 python -m artagents author test builtin.hype --fixture smoke` → exit 0.

## Execution Order
1. Steps 1-3 (audit, env helper + auto-approval branch, normalize helper) — pure additions; existing tests stay green.
2. Step 4 (replay driver) — depends on Step 2's auto-approval branch.
3. Step 5 (rewrite `_cmd_test` + `--regenerate`) — depends on Steps 3 + 4.
4. Step 6 (hype fixture + golden) — depends on Step 5 (uses `--regenerate` to mint the committed golden).
5. Step 7 (tests, including scaffold removal).
6. Step 8 (validation).

## Validation Order
1. Auto-approval test (`test_author_test_auto_approval.py`) — cheapest; verifies both flag fixes (no `cmd_start` guard; canonical `attestor_kind`).
2. Integration tests (`test_author_test_{pass,drift,regenerate}.py`) — exercise the full driver.
3. Full `pytest tests/` — catch cross-test regressions, especially in `tests/test_task_kernel_attested.py` and `tests/test_inbox_consume.py` (the `attestor_kind in {agent,actor}` invariant).
4. Manual CLI smoke against the committed golden.


        Plan metadata:
        {
  "version": 2,
  "timestamp": "2026-05-05T02:46:21Z",
  "hash": "sha256:4dc0ceb0c338e5d6220a2575e64ae8d45b868361aac81dd23753c197c16bb29a",
  "changes_summary": "Addressed both significant flags. FLAG-P9-001: removed the `cmd_start` guard against `ARTAGENTS_AUTHOR_TEST=1` (it deadlocked the test runner, which needs the var live across `cmd_start`); the \"not available in normal start\" constraint is satisfied structurally (only `_cmd_test` sets the var, in a save/restore block). FLAG-P9-002: `validate_attested_identity` now keeps the canonical `attestor_kind` enum (`\"agent\"` or `\"actor\"`) in author-test mode rather than returning `\"author_test\"`; the author-test marker rides on a separate `source=\"author_test\"` field injected in `_dispatch_attested`. Test runner now passes the right `--agent`/`--actor` flag based on the step's `ack.kind` so the canonical kind reaches the event. Added test assertions that verify both fixes (`attestor_kind == \"actor\"` not `\"author_test\"`; `cmd_start` succeeds with the env var set).",
  "flags_addressed": [
    {
      "id": "FLAG-P9-001",
      "resolution": "addressed",
      "reason": "Dropped the cmd_start guard. The constraint 'auto-approval must not be available in normal start flow' is now satisfied structurally \u2014 only _cmd_test sets ARTAGENTS_AUTHOR_TEST, in a save/restore env block scoped to run_fixture. cmd_start does not inspect or reject on the variable, so the test runner can set it before cmd_start (where gate dispatch needs it live) without deadlocking. Test added to verify cmd_start succeeds with the env var set."
    },
    {
      "id": "FLAG-P9-002",
      "resolution": "addressed",
      "reason": "validate_attested_identity now returns the canonical attestor_kind ('agent' or 'actor') in author-test mode \u2014 never 'author_test'. The author-test marker is injected as a separate source='author_test' field in _dispatch_attested. The test runner passes --actor or --agent matching step.ack.kind so the canonical kind reaches the event. Existing invariant in tests/test_task_kernel_attested.py:142,160 and tests/test_inbox_consume.py:61 stays intact."
    }
  ],
  "questions": [
    "The brief says the canonical fixture is `builtin.hype`, but the legacy `artagents/packs/builtin/hype/` is a folder containing `orchestrator.yaml` + `run.py` (the real video pipeline). I'm planning to add a NEW `artagents/packs/builtin/hype.py` (sibling file) with a minimal DSL plan whose steps run in milliseconds (echo + attested review). Is that the intent \u2014 a smoke harness for the orchestrator framework, not for the real pipeline? Or do you want the smoke fixture to drive the real `transcribe/cut/render` chain?",
    "The Phase 5 scaffold tests in `tests/test_author_test_scaffold.py` lock in the placeholder behavior that Phase 9 replaces (exit 2 + 'implement Phase 9' message). I'm planning to delete that file. Confirming the scaffold tests are exempt from 'existing tests must continue to pass' because their entire purpose was to encode the Phase-5 stub the brief tells me to replace."
  ],
  "success_criteria": [
    {
      "criterion": "`pytest tests/` passes with the new tests added and `tests/test_author_test_scaffold.py` removed.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "`PYENV_VERSION=3.11.11 python -m artagents author test builtin.hype --fixture smoke` exits 0 against the committed `artagents/packs/builtin/golden/smoke.events.jsonl`.",
      "priority": "must",
      "requires": [
        "run_shell"
      ]
    },
    {
      "criterion": "Modifying any field of the committed golden (e.g. flipping a `kind`) and rerunning the same command exits 1 and prints a `difflib.unified_diff` block to stdout (`--- golden/smoke.events.jsonl` / `+++` lines).",
      "priority": "must",
      "requires": [
        "run_shell",
        "read_files"
      ]
    },
    {
      "criterion": "Running `artagents author test builtin.hype --fixture smoke --regenerate` rewrites `artagents/packs/builtin/golden/smoke.events.jsonl` to byte-equivalent content and exits 0 with a 'commit if intentional' confirmation message.",
      "priority": "must",
      "requires": [
        "run_shell",
        "read_files"
      ]
    },
    {
      "criterion": "Auto-approval (`source: author_test`) only fires when `ARTAGENTS_AUTHOR_TEST=1`. Without it, mismatched `--actor`/self-ack rejections in `validate_attested_identity` continue to fire normally.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "In author-test mode, `step_attested` and `item_attested` events keep `attestor_kind` in {`agent`,`actor`} (never `author_test`); the author-test marker appears only as a separate `source=\"author_test\"` field. Verified by `tests/test_author_test_auto_approval.py` and by the unchanged invariants in `tests/test_task_kernel_attested.py:142,160` and `tests/test_inbox_consume.py:61`.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "`cmd_start` succeeds even when `ARTAGENTS_AUTHOR_TEST=1` is set in the environment (no guard) \u2014 verified by a dedicated test in `tests/test_author_test_auto_approval.py`. The 'not available in normal start flow' constraint is upheld structurally (only `_cmd_test` sets the var).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "The author-test runs against a `tempfile.TemporaryDirectory` scratch projects root \u2014 no files written under `~/Documents/reigh-workspace/artagents-projects/` during the test.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "No new third-party dependencies introduced (stdlib only); `requirements.txt` unchanged.",
      "priority": "must",
      "requires": [
        "parse_diff"
      ]
    },
    {
      "criterion": "Event normalization strips `ts`, `hash`, `run_id`, and replaces any absolute-path string under the scratch run dir with `<RUN_DIR>/<rel>`; the strip-vs-recompute strategy is documented in a one-line comment in `artagents/core/task/normalize.py`.",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "`artagents/orchestrate/cli.py` and `artagents/orchestrate/test_runner.py` each stay under ~400 lines; functions stay single-responsibility (one driver fn, one diff fn, one regenerate fn).",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Hash-chain integrity of `events.jsonl` written during the replay is preserved (the gate's existing `verify_chain` is not bypassed).",
      "priority": "should",
      "requires": [
        "read_files",
        "run_tests"
      ]
    }
  ],
  "assumptions": [
    "Adding `artagents/packs/builtin/hype.py` as a sibling file does NOT collide with the existing `artagents/packs/builtin/hype/` folder for the DSL resolver, because `compile.resolve_orchestrator` loads `<pack>/<name>.py` via `spec_from_file_location` rather than Python's import machinery, so the folder is not a shadow.",
    "The Phase 5 scaffold tests in `tests/test_author_test_scaffold.py` are placeholders Phase 9 replaces (their docstring explicitly defers the runtime replay path to Phase 9). They are deleted as part of Phase 9.",
    "Auto-approval is implemented by branching identity validation in `validate_attested_identity` while keeping the canonical attestor_kind enum, and stamping `source=\"author_test\"` independently in `_dispatch_attested` \u2014 event factories in `events.py` stay pure.",
    "The `cmd_start` flow does NOT inspect `ARTAGENTS_AUTHOR_TEST`. The constraint 'must not be available in normal start flow' is satisfied structurally: `_cmd_test` is the only caller that sets the variable, in a save/restore block scoped to `run_fixture`. Manual user export of the variable is treated as an internal/test-only knob, consistent with the design doc's honor-model boundary (SD-025).",
    "The `builtin.hype` DSL fixture for Phase 9 is a tiny stub (echo code step + attested review with ack='actor') \u2014 not a real transcribe/cut/render pipeline. The smoke fixture's purpose is to lock in the orchestrator framework's event sequence; future phases extend hype.py.",
    "The test runner inspects `peek.step.ack.kind` and passes the matching `--actor` or `--agent` flag, so the resulting `step_attested` event preserves the canonical `attestor_kind` enum (`agent` or `actor`) \u2014 author-test provenance lives only on the separate `source` field.",
    "Author-test runs do NOT need to copy fixture inputs into the scratch project root for the smoke fixture (it has no inputs). `run_fixture` accepts an optional `fixture_dir` and only copies its contents when present."
  ],
  "delta_from_previous_percent": 44.58,
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
    "id": "FLAG-P9-001",
    "concern": "cmd_start guard contradicts the run_fixture flow. Step 2.4 has cmd_start refuse to launch when ARTAGENTS_AUTHOR_TEST=1 is set, but Step 4.2 has run_fixture set ARTAGENTS_AUTHOR_TEST=1 BEFORE calling cmd_start. As written, the test verb cannot bootstrap a run at all: the env var must be live during gate dispatch (so _dispatch_attested sees author-test mode) yet cmd_start refuses when it sees the same var. tests/test_author_test_pass.py would fail at start. The plan needs a reconciliation it does not specify - e.g. a separate internal env var that run_fixture sets, a kwarg to cmd_start that bypasses the guard, or moving the env-set to after cmd_start returns (with a re-confirmation that gate paths only depend on the var being set at dispatch time, not at start time).",
    "evidence": "Addressed both significant flags. FLAG-P9-001: removed the `cmd_start` guard against `ARTAGENTS_AUTHOR_TEST=1` (it deadlocked the test runner, which needs the var live across `cmd_start`); the \"not available in normal start\" constraint is satisfied structurally (only `_cmd_test` sets the var, in a save/restore block). FLAG-P9-002: `validate_attested_identity` now keeps the canonical `attestor_kind` enum (`\"agent\"` or `\"actor\"`) in author-test mode rather than returning `\"author_test\"`; the author-test marker rides on a separate `source=\"author_test\"` field injected in `_dispatch_attested`. Test runner now passes the right `--agent`/`--actor` flag based on the step's `ack.kind` so the canonical kind reaches the event. Added test assertions that verify both fixes (`attestor_kind == \"actor\"` not `\"author_test\"`; `cmd_start` succeeds with the env var set).",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "FLAG-P9-002",
    "concern": "validate_attested_identity returning ('author_test', ...) corrupts the attestor_kind field. The brief specifies a separate source:author_test marker on the ack event, not a new attestor_kind value. make_step_attested_event writes attestor_kind verbatim, and existing tests treat it as an enum of agent/actor (tests/test_task_kernel_attested.py:142,160 and tests/test_inbox_consume.py:61 assert attestor_kind in that set). Returning 'author_test' as the kind from the auto-approval branch will (a) leak a new enum value into the canonical event schema, and (b) make the smoke golden's step_attested record describe the attestor as kind=author_test instead of kind=actor (which is what hype.py declares with ack='actor'). Better: in author-test mode, derive a real kind from the incoming flag (actor or agent) and inject the new source field independently in _dispatch_attested per Step 2.3.",
    "evidence": "Addressed both significant flags. FLAG-P9-001: removed the `cmd_start` guard against `ARTAGENTS_AUTHOR_TEST=1` (it deadlocked the test runner, which needs the var live across `cmd_start`); the \"not available in normal start\" constraint is satisfied structurally (only `_cmd_test` sets the var, in a save/restore block). FLAG-P9-002: `validate_attested_identity` now keeps the canonical `attestor_kind` enum (`\"agent\"` or `\"actor\"`) in author-test mode rather than returning `\"author_test\"`; the author-test marker rides on a separate `source=\"author_test\"` field injected in `_dispatch_attested`. Test runner now passes the right `--agent`/`--actor` flag based on the step's `ack.kind` so the canonical kind reaches the event. Added test assertions that verify both fixes (`attestor_kind == \"actor\"` not `\"author_test\"`; `cmd_start` succeeds with the env var set).",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "FLAG-P9-003",
    "concern": "run_fixture only knows how to ack actor-attested steps. Step 4.2 hardcodes --actor author_test for every attested step. But ack.kind=='agent' steps reject --actor at gate.py:1075-1078 even before the author-test branch can short-circuit. Even if author-test mode skips identity checks entirely, _ack_approve synthesizes the incoming command from peek.step.command + identity tokens; an agent-attested step in a future fixture will be acked under actor identity and the golden's step_attested will record kind=actor for what should be an agent ack. Smoke is fine because the sole attested step uses ack='actor', but run_fixture should branch on peek.step.ack.kind so the harness generalizes - the brief says 'attested steps that would normally block on user ack auto-approve' (generic).",
    "evidence": "Plan Step 4.2; dsl.py:418-450 supports ack='agent'; gate.py:1075-1078 rejects ack.kind=='agent' without --agent.",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "FLAG-P9-004",
    "concern": "test_author_test_auto_approval depends on getting through cmd_start with ARTAGENTS_AUTHOR_TEST set. Step 7.5 calls cmd_ack with mismatched identity under ARTAGENTS_AUTHOR_TEST=1 and expects success. But cmd_ack requires an active_run, and only cmd_start writes active_run.json + run_started events; per Step 2.4 cmd_start refuses when ARTAGENTS_AUTHOR_TEST=1. If the test pre-creates active_run.json/plan.json by hand to skip cmd_start it bypasses the very flow it claims to validate. Downstream symptom of FLAG-P9-001 - once that is resolved the test plan must spell out which path seeds state.",
    "evidence": "Plan Step 7.5 vs Step 2.4; cmd_start at lifecycle.py:127 is the only path that writes active_run.json + run_started events.",
    "status": "open",
    "severity": "minor"
  }
]

        Critique history:
        [
  {
    "iteration": 1,
    "flag_count": 4,
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
{
  "tasks": [
    {
      "id": "T1",
      "description": "Add author-test env helper and auto-approval branches. (a) Create artagents/core/task/env.py constant ARTAGENTS_AUTHOR_TEST = \"ARTAGENTS_AUTHOR_TEST\" and helper is_author_test_mode() (mirrors task_actor_env). (b) In artagents/core/task/gate.py validate_attested_identity (~line 1064): when is_author_test_mode() is true, keep the --agent/--actor exclusivity check, keep the per-kind required-flag check, but skip the ARTAGENTS_ACTOR match check and the self-ack rejection. ALWAYS return the canonical kind (\"agent\" or \"actor\") — never \"author_test\". (c) In _dispatch_attested (~line 904): after the existing event factory builds step_attested/item_attested, if is_author_test_mode() set event[\"source\"] = \"author_test\" before append_event. Do NOT modify event factories in events.py. Do NOT add any guard or branch in cmd_start (lifecycle.py) on this env var.",
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
      "description": "Create artagents/core/task/normalize.py exporting normalize_events(events: list[dict], *, run_dir: Path | None) -> list[dict] and dump_events_jsonl(events, path). Strip volatile fields per event: ts, hash, run_id, pid (when present). Recursively walk dict and list values; rewrite any string starting with str(run_dir) to \"<RUN_DIR>/\" + relative remainder. dump_events_jsonl writes one canonical json.dumps(..., sort_keys=True, separators=(\",\", \":\"), ensure_ascii=False) line per event. Add a one-line module comment documenting the strip-vs-recompute choice: \"# We strip 'hash' rather than recomputing — chain hashes are downstream of stripped fields, and structural drift is the diff signal.\"",
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
      "description": "Create artagents/orchestrate/test_runner.py with public function run_fixture(*, qualified_id, fixture_dir, packs_root, projects_root, project_slug=\"author_test\", run_id=\"fixture_run\") -> Path returning the events.jsonl path. Implementation: save current ARTAGENTS_AUTHOR_TEST and ARTAGENTS_ACTOR env vars; set ARTAGENTS_AUTHOR_TEST=1 and ARTAGENTS_ACTOR=\"author_test\"; restore in finally. If fixture_dir is provided and exists, shutil.copytree(fixture_dir, projects_root / project_slug, dirs_exist_ok=True). Call cmd_start([qualified_id, \"--project\", project_slug, \"--name\", run_id], packs_root=packs_root, projects_root=projects_root). Loop (cap 200 iters) using peek_current_step until exhausted: code step → gate_command(slug, cmd_str, shlex.split(cmd_str), root=projects_root); subprocess.run(cmd_argv, env={**os.environ, **child_subprocess_env(...)}, check=False); record_dispatch_complete(decision, rc). Attested step → branch on peek.step.ack.kind: if \"agent\" use [\"--agent\",\"author_test\"], else [\"--actor\",\"author_test\"]; cmd_ack([path_str, \"--project\", slug, \"--decision\", \"approve\", *flag_pair], projects_root=projects_root). Return projects_root/project_slug/\"runs\"/run_id/\"events.jsonl\". This addresses FLAG-P9-003 (branch on ack.kind so the harness generalizes beyond actor-only).",
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
      "id": "T4",
      "description": "Rewrite artagents/orchestrate/cli.py:_cmd_test (lines ~311-371) for Phase 9 and add --regenerate. Behavior: resolve packs root; if <pack>/build/<orch>.json missing, call compile_to_path(qid, packs_root=packs_root) first. Use tempfile.TemporaryDirectory() as scratch projects root. Resolve fixture_dir = packs_root/pack/\"fixtures\"/fixture_name (pass None to run_fixture if missing or empty). Call run_fixture(...). Read events via read_events; normalize via normalize_events(events, run_dir=run_dir); render canonical lines via dump_events_jsonl. If --regenerate: write golden, print 'wrote <path> — commit if intentional', return 0. Else: read golden; if missing/empty exit 1 with 'no committed golden; rerun with --regenerate to create one'. Compare normalized line lists. Return 0 on match. On drift, print difflib.unified_diff(...) headers '--- golden/<fixture>.events.jsonl' / '+++ actual' and return 1. Add test_p.add_argument(\"--regenerate\", action=\"store_true\") in _build_parser (~cli.py:462) and thread args.regenerate through main into _cmd_test. Delete dead helpers _VOLATILE_EVENT_FIELDS and _strip_volatile.",
      "depends_on": [
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
      "id": "T5",
      "description": "Author canonical hype DSL fixture + mint golden. (a) Create artagents/packs/builtin/hype.py (sibling file — does NOT collide with existing hype/ folder because compile.resolve_orchestrator uses spec_from_file_location): @orchestrator(\"builtin.hype\") returning [code(\"noop\", argv=[\"python3\",\"-c\",\"print('ok')\"]), attested(\"review\", command=\"echo review\", instructions=\"approve to finish\", ack=\"actor\")]. (b) Create artagents/packs/builtin/fixtures/smoke/.keep (empty file). (c) Mint artagents/packs/builtin/golden/smoke.events.jsonl by running PYENV_VERSION=3.11.11 python -m artagents author test builtin.hype --fixture smoke --regenerate locally. Spot-check: run_started → step_dispatched/step_completed for noop → step_attested for review with attestor_kind=\"actor\", attestor_id=\"author_test\", source=\"author_test\". Commit the golden.",
      "depends_on": [
        "T4"
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
      "description": "Replace Phase-5 scaffold tests with Phase-9 tests. (a) Delete tests/test_author_test_scaffold.py (Phase-5 stub it encodes is being replaced; its docstring explicitly defers replay to Phase 9). (b) tests/test_author_test_pass.py: call author_cli.main([\"test\",\"builtin.hype\",\"--fixture\",\"smoke\"]); assert rc==0 and stdout contains 'ok builtin.hype --fixture smoke'. (c) tests/test_author_test_drift.py: shutil.copytree(\"artagents/packs\", tmp_path/\"packs\"); flip a kind value in the copied golden; run with packs_root=<tmp>; assert rc==1 and stdout includes '--- golden/smoke.events.jsonl' and '+++'. (d) tests/test_author_test_regenerate.py: same temp-pack copy; truncate golden to empty; run with --regenerate; assert rc==0; golden non-empty and byte-equal to committed golden. (e) tests/test_author_test_auto_approval.py: build a tiny demo pack in tmp_path with one attested step. Without ARTAGENTS_AUTHOR_TEST set: cmd_ack with --actor mismatching ARTAGENTS_ACTOR → assert non-zero exit. With ARTAGENTS_AUTHOR_TEST=1: same mismatched --actor → assert success; last event has kind=\"step_attested\", attestor_kind=\"actor\" (NOT \"author_test\" — verifies FLAG-P9-002), source=\"author_test\". Also assert cmd_start succeeds with ARTAGENTS_AUTHOR_TEST=1 in env (verifies FLAG-P9-001). Note this test must seed an active_run via cmd_start (per FLAG-P9-004) — do NOT pre-create active_run.json by hand; that's the path the test is validating. Use save/restore for env vars.",
      "depends_on": [
        "T5"
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
      "description": "Validate Phase 9. (1) Run targeted: PYENV_VERSION=3.11.11 pytest tests/test_author_test_pass.py tests/test_author_test_drift.py tests/test_author_test_regenerate.py tests/test_author_test_auto_approval.py -x. (2) Run full suite: PYENV_VERSION=3.11.11 pytest tests/. Existing tests (especially tests/test_task_kernel_attested.py and tests/test_inbox_consume.py with their attestor_kind in {agent,actor} invariants) must remain green. (3) Manual smoke: PYENV_VERSION=3.11.11 python -m artagents author test builtin.hype --fixture smoke → assert exit 0. (4) Drift sanity: temporarily mutate the committed golden, rerun the smoke command, assert exit 1 with unified diff, then revert the mutation. If anything fails: read the error, fix the code, re-run. Write a tiny throwaway script that drives author_cli.main against an intentionally drifted golden copy to confirm drift detection works, run it, then delete the script.",
      "depends_on": [
        "T6"
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
    "FLAG-P9-001 (resolved): cmd_start MUST NOT inspect ARTAGENTS_AUTHOR_TEST. The 'not available in normal start' constraint is satisfied structurally — only _cmd_test sets the env var, in run_fixture's save/restore block. If you find yourself adding a guard in cmd_start, stop — it deadlocks the test runner.",
    "FLAG-P9-002 (resolved): validate_attested_identity must keep the canonical attestor_kind enum ('agent' or 'actor') in author-test mode. NEVER return 'author_test' as the kind. Author-test provenance rides on a separate event['source'] = 'author_test' field injected in _dispatch_attested. Existing assertions in tests/test_task_kernel_attested.py:142,160 and tests/test_inbox_consume.py:61 lock this in.",
    "FLAG-P9-003 (open, addressed in T3): run_fixture must branch on peek.step.ack.kind and pass --agent or --actor accordingly. Hardcoding --actor breaks future agent-attested fixtures and writes wrong attestor_kind into the golden.",
    "FLAG-P9-004 (open, addressed in T6): test_author_test_auto_approval needs cmd_start to succeed with ARTAGENTS_AUTHOR_TEST=1 (the FLAG-P9-001 fix). Do NOT pre-create active_run.json/plan.json by hand — that bypasses the very flow the test validates. Seed run state via cmd_start.",
    "Author-test must run only against tempfile.TemporaryDirectory scratch projects roots. No writes under ~/Documents/reigh-workspace/artagents-projects/ during tests.",
    "Stdlib only — no new third-party deps; requirements.txt unchanged.",
    "Hash-chain integrity: don't bypass gate's verify_chain on the live events.jsonl. Normalization (strip 'hash') applies only to the in-memory diff/regenerate path, not to what gets written by append_event.",
    "DSL resolver assumption: artagents/packs/builtin/hype.py (sibling file) is loaded by spec_from_file_location and is NOT shadowed by the existing artagents/packs/builtin/hype/ folder. If compile fails to find it, audit compile.resolve_orchestrator before changing the layout.",
    "tests/test_author_test_scaffold.py is intentionally deleted in T6 (its docstring defers runtime replay to Phase 9). 'Existing tests must continue to pass' explicitly excludes this scaffold suite.",
    "Event factories in artagents/core/task/events.py stay pure — the source='author_test' field is mutated onto the dict in _dispatch_attested AFTER the factory call, BEFORE append_event.",
    "cli.py and test_runner.py should each stay under ~400 lines; functions stay single-responsibility (run_fixture; diff path; regenerate path)."
  ],
  "sense_checks": [
    {
      "id": "SC1",
      "task_id": "T1",
      "question": "Does artagents/core/task/env.py export ARTAGENTS_AUTHOR_TEST and is_author_test_mode()? Does validate_attested_identity in author-test mode (a) still enforce --agent/--actor exclusivity, (b) still require the per-kind flag, (c) skip ARTAGENTS_ACTOR-match and self-ack rejection, and (d) ALWAYS return canonical kind ('agent'/'actor') — never 'author_test'? Does _dispatch_attested set event['source']='author_test' before append_event when in author-test mode? Is cmd_start unchanged (no guard on the env var)?",
      "verdict": ""
    },
    {
      "id": "SC2",
      "task_id": "T2",
      "question": "Does normalize.py strip ts/hash/run_id/pid, recursively rewrite absolute paths under run_dir to <RUN_DIR>/<rel>, and provide dump_events_jsonl with sort_keys=True, separators=(',',':'), ensure_ascii=False? Is the strip-vs-recompute choice documented in a one-line comment?",
      "verdict": ""
    },
    {
      "id": "SC3",
      "task_id": "T3",
      "question": "Does run_fixture save/restore env vars in finally, copytree the fixture only when present, drive code steps via gate_command + subprocess.run + record_dispatch_complete, and branch on peek.step.ack.kind to pass --agent or --actor (FLAG-P9-003)? Is the iteration cap present (≤200) to fail loud on author bugs?",
      "verdict": ""
    },
    {
      "id": "SC4",
      "task_id": "T4",
      "question": "Does _cmd_test compile-on-demand if build/<orch>.json is missing, run inside tempfile.TemporaryDirectory, normalize via normalize_events with run_dir, support --regenerate (writes golden + 'commit if intentional' message), exit 1 with unified-diff headers on drift, and exit 1 with a clear 'rerun with --regenerate' message when no golden exists? Are _VOLATILE_EVENT_FIELDS / _strip_volatile removed?",
      "verdict": ""
    },
    {
      "id": "SC5",
      "task_id": "T5",
      "question": "Does artagents/packs/builtin/hype.py compile to qualified_id 'builtin.hype' with one code('noop') step plus one attested('review', ack='actor') step? Does the committed golden contain run_started → step_dispatched/step_completed (noop) → step_attested with attestor_kind='actor', attestor_id='author_test', source='author_test'? Was it minted via --regenerate (not hand-written)?",
      "verdict": ""
    },
    {
      "id": "SC6",
      "task_id": "T6",
      "question": "Is tests/test_author_test_scaffold.py deleted? Do the four new tests (pass/drift/regenerate/auto_approval) cover: rc==0 against committed golden; unified-diff headers on drift; byte-equal regenerate; cmd_start succeeds with env var (FLAG-P9-001); attestor_kind=='actor' not 'author_test' (FLAG-P9-002); source=='author_test'; mismatched --actor rejected without env var, accepted with it? Is run state seeded via cmd_start (not pre-created)?",
      "verdict": ""
    },
    {
      "id": "SC7",
      "task_id": "T7",
      "question": "Does pytest tests/ pass in full? Does PYENV_VERSION=3.11.11 python -m artagents author test builtin.hype --fixture smoke exit 0 against the committed golden? Does mutating any field of the committed golden cause exit 1 with a unified-diff block? Was the throwaway repro script deleted after use?",
      "verdict": ""
    }
  ],
  "user_actions": [],
  "meta_commentary": "Phase 9 is the last V1 phase — polish matters. Two flag fixes are load-bearing: (1) cmd_start must NOT inspect ARTAGENTS_AUTHOR_TEST (deadlocks the runner; see FLAG-P9-001), and (2) validate_attested_identity must keep canonical attestor_kind ('agent'/'actor') and let _dispatch_attested stamp source='author_test' independently (FLAG-P9-002). The two open minor flags (P9-003, P9-004) are explicitly handled inside T3 and T6 respectively — read those task descriptions carefully.\n\nExecution order is dependency-driven: T1 (env+gate branch) and T2 (normalize) are independent; T3 (driver) needs T1; T4 (CLI rewrite) needs T2+T3; T5 (fixture+golden) needs T4 (uses --regenerate to mint the committed golden); T6 (tests) needs T5; T7 (validate). DO NOT mint the golden by hand — run the regenerate path so it is byte-equivalent to what the diff path will produce.\n\nAudit step (plan Step 1) is folded into T1's prep — read the cited file:line references (gate.py:510, 790, 904, 1064, 1096; lifecycle_ack.py:102; events.py:25; cli.py:287-371) before editing. Confirm DSL resolver loads sibling .py via spec_from_file_location before assuming hype.py won't shadow with hype/.\n\nConstraints: stdlib only; additive; no writes under real artagents-projects/ (use tempfile.TemporaryDirectory); preserve hash-chained events on disk (normalization is in-memory only). Existing tests stay green except tests/test_author_test_scaffold.py which is intentionally deleted (its docstring defers replay to Phase 9).\n\nIf T7 surfaces a flake or missing piece, fix root-cause then re-run — do not skip tests or weaken assertions to make them pass.",
  "validation": {
    "plan_steps_covered": [
      {
        "plan_step_summary": "Step 1: Audit replay touch points (file/line references in gate, lifecycle, events, cli)",
        "finalize_item_ids": [
          "T1"
        ]
      },
      {
        "plan_step_summary": "Step 2: Add env helper + auto-approval branch in validate_attested_identity and _dispatch_attested; no cmd_start guard",
        "finalize_item_ids": [
          "T1"
        ]
      },
      {
        "plan_step_summary": "Step 3: Add event normalization helper (normalize.py with normalize_events + dump_events_jsonl)",
        "finalize_item_ids": [
          "T2"
        ]
      },
      {
        "plan_step_summary": "Step 4: Build replay driver test_runner.run_fixture with env save/restore, copytree, code+attested loop branching on ack.kind",
        "finalize_item_ids": [
          "T3"
        ]
      },
      {
        "plan_step_summary": "Step 5: Rewrite _cmd_test for Phase 9 + add --regenerate flag + drop dead helpers",
        "finalize_item_ids": [
          "T4"
        ]
      },
      {
        "plan_step_summary": "Step 6: Author canonical hype DSL fixture (hype.py + fixtures/smoke/ + golden/smoke.events.jsonl)",
        "finalize_item_ids": [
          "T5"
        ]
      },
      {
        "plan_step_summary": "Step 7: Tests — delete scaffold, add pass/drift/regenerate/auto_approval suites",
        "finalize_item_ids": [
          "T6"
        ]
      },
      {
        "plan_step_summary": "Step 8: Validation — targeted pytest, full pytest, manual CLI smoke",
        "finalize_item_ids": [
          "T7"
        ]
      }
    ],
    "orphan_tasks": [],
    "completeness_notes": "All 8 plan steps mapped. Step 1 (audit) folds into T1's prep work since it's read-only inspection of cited file:line references that immediately inform the T1 edits — the brief explicitly says simple changes shouldn't have a separate inspect task.",
    "coverage_complete": true
  },
  "baseline_test_command": "PYENV_VERSION=3.11.11 pytest tests/",
  "baseline_test_failures": [],
  "baseline_test_note": "Baseline not run during finalize. The plan asserts existing tests stay green except for tests/test_author_test_scaffold.py which is deliberately deleted in T6 (its Phase-5 stub is what Phase 9 replaces; the docstring explicitly defers runtime replay to Phase 9). Existing invariants in tests/test_task_kernel_attested.py:142,160 and tests/test_inbox_consume.py:61 (attestor_kind ∈ {agent, actor}) are intentionally preserved by the FLAG-P9-002 fix and must continue to pass."
}
```

> TOOL

tool_result StructuredOutput
```
Output does not match required schema: /sense_checks/0: must have required property 'executor_note', /sense_checks/1: must have required property 'executor_note', /sense_checks/2: must have required property 'executor_note', /sense_checks/3: must have required property 'executor_note', /sense_checks/4: must have required property 'executor_note', /sense_checks/5: must have required property 'executor_note', /sense_checks/6: must have required property 'executor_note'
```

> TOOL

tool_use StructuredOutput
```json
{
  "tasks": [
    {
      "id": "T1",
      "description": "Add author-test env helper and auto-approval branches. (a) Create artagents/core/task/env.py constant ARTAGENTS_AUTHOR_TEST = \"ARTAGENTS_AUTHOR_TEST\" and helper is_author_test_mode() (mirrors task_actor_env). (b) In artagents/core/task/gate.py validate_attested_identity (~line 1064): when is_author_test_mode() is true, keep the --agent/--actor exclusivity check, keep the per-kind required-flag check, but skip the ARTAGENTS_ACTOR match check and the self-ack rejection. ALWAYS return the canonical kind (\"agent\" or \"actor\") — never \"author_test\". (c) In _dispatch_attested (~line 904): after the existing event factory builds step_attested/item_attested, if is_author_test_mode() set event[\"source\"] = \"author_test\" before append_event. Do NOT modify event factories in events.py. Do NOT add any guard or branch in cmd_start (lifecycle.py) on this env var.",
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
      "description": "Create artagents/core/task/normalize.py exporting normalize_events(events: list[dict], *, run_dir: Path | None) -> list[dict] and dump_events_jsonl(events, path). Strip volatile fields per event: ts, hash, run_id, pid (when present). Recursively walk dict and list values; rewrite any string starting with str(run_dir) to \"<RUN_DIR>/\" + relative remainder. dump_events_jsonl writes one canonical json.dumps(..., sort_keys=True, separators=(\",\", \":\"), ensure_ascii=False) line per event. Add a one-line module comment documenting the strip-vs-recompute choice: \"# We strip 'hash' rather than recomputing — chain hashes are downstream of stripped fields, and structural drift is the diff signal.\"",
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
      "description": "Create artagents/orchestrate/test_runner.py with public function run_fixture(*, qualified_id, fixture_dir, packs_root, projects_root, project_slug=\"author_test\", run_id=\"fixture_run\") -> Path returning the events.jsonl path. Implementation: save current ARTAGENTS_AUTHOR_TEST and ARTAGENTS_ACTOR env vars; set ARTAGENTS_AUTHOR_TEST=1 and ARTAGENTS_ACTOR=\"author_test\"; restore in finally. If fixture_dir is provided and exists, shutil.copytree(fixture_dir, projects_root / project_slug, dirs_exist_ok=True). Call cmd_start([qualified_id, \"--project\", project_slug, \"--name\", run_id], packs_root=packs_root, projects_root=projects_root). Loop (cap 200 iters) using peek_current_step until exhausted: code step → gate_command(slug, cmd_str, shlex.split(cmd_str), root=projects_root); subprocess.run(cmd_argv, env={**os.environ, **child_subprocess_env(...)}, check=False); record_dispatch_complete(decision, rc). Attested step → branch on peek.step.ack.kind: if \"agent\" use [\"--agent\",\"author_test\"], else [\"--actor\",\"author_test\"]; cmd_ack([path_str, \"--project\", slug, \"--decision\", \"approve\", *flag_pair], projects_root=projects_root). Return projects_root/project_slug/\"runs\"/run_id/\"events.jsonl\". This addresses FLAG-P9-003 (branch on ack.kind so the harness generalizes beyond actor-only).",
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
      "id": "T4",
      "description": "Rewrite artagents/orchestrate/cli.py:_cmd_test (lines ~311-371) for Phase 9 and add --regenerate. Behavior: resolve packs root; if <pack>/build/<orch>.json missing, call compile_to_path(qid, packs_root=packs_root) first. Use tempfile.TemporaryDirectory() as scratch projects root. Resolve fixture_dir = packs_root/pack/\"fixtures\"/fixture_name (pass None to run_fixture if missing or empty). Call run_fixture(...). Read events via read_events; normalize via normalize_events(events, run_dir=run_dir); render canonical lines via dump_events_jsonl. If --regenerate: write golden, print 'wrote <path> — commit if intentional', return 0. Else: read golden; if missing/empty exit 1 with 'no committed golden; rerun with --regenerate to create one'. Compare normalized line lists. Return 0 on match. On drift, print difflib.unified_diff(...) headers '--- golden/<fixture>.events.jsonl' / '+++ actual' and return 1. Add test_p.add_argument(\"--regenerate\", action=\"store_true\") in _build_parser (~cli.py:462) and thread args.regenerate through main into _cmd_test. Delete dead helpers _VOLATILE_EVENT_FIELDS and _strip_volatile.",
      "depends_on": [
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
      "id": "T5",
      "description": "Author canonical hype DSL fixture + mint golden. (a) Create artagents/packs/builtin/hype.py (sibling file — does NOT collide with existing hype/ folder because compile.resolve_orchestrator uses spec_from_file_location): @orchestrator(\"builtin.hype\") returning [code(\"noop\", argv=[\"python3\",\"-c\",\"print('ok')\"]), attested(\"review\", command=\"echo review\", instructions=\"approve to finish\", ack=\"actor\")]. (b) Create artagents/packs/builtin/fixtures/smoke/.keep (empty file). (c) Mint artagents/packs/builtin/golden/smoke.events.jsonl by running PYENV_VERSION=3.11.11 python -m artagents author test builtin.hype --fixture smoke --regenerate locally. Spot-check: run_started → step_dispatched/step_completed for noop → step_attested for review with attestor_kind=\"actor\", attestor_id=\"author_test\", source=\"author_test\". Commit the golden.",
      "depends_on": [
        "T4"
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
      "description": "Replace Phase-5 scaffold tests with Phase-9 tests. (a) Delete tests/test_author_test_scaffold.py (Phase-5 stub it encodes is being replaced; its docstring explicitly defers replay to Phase 9). (b) tests/test_author_test_pass.py: call author_cli.main([\"test\",\"builtin.hype\",\"--fixture\",\"smoke\"]); assert rc==0 and stdout contains 'ok builtin.hype --fixture smoke'. (c) tests/test_author_test_drift.py: shutil.copytree(\"artagents/packs\", tmp_path/\"packs\"); flip a kind value in the copied golden; run with packs_root=<tmp>; assert rc==1 and stdout includes '--- golden/smoke.events.jsonl' and '+++'. (d) tests/test_author_test_regenerate.py: same temp-pack copy; truncate golden to empty; run with --regenerate; assert rc==0; golden non-empty and byte-equal to committed golden. (e) tests/test_author_test_auto_approval.py: build a tiny demo pack in tmp_path with one attested step. Without ARTAGENTS_AUTHOR_TEST set: cmd_ack with --actor mismatching ARTAGENTS_ACTOR → assert non-zero exit. With ARTAGENTS_AUTHOR_TEST=1: same mismatched --actor → assert success; last event has kind=\"step_attested\", attestor_kind=\"actor\" (NOT \"author_test\" — verifies FLAG-P9-002), source=\"author_test\". Also assert cmd_start succeeds with ARTAGENTS_AUTHOR_TEST=1 in env (verifies FLAG-P9-001). Note this test must seed an active_run via cmd_start (per FLAG-P9-004) — do NOT pre-create active_run.json by hand; that's the path the test is validating. Use save/restore for env vars.",
      "depends_on": [
        "T5"
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
      "description": "Validate Phase 9. (1) Run targeted: PYENV_VERSION=3.11.11 pytest tests/test_author_test_pass.py tests/test_author_test_drift.py tests/test_author_test_regenerate.py tests/test_author_test_auto_approval.py -x. (2) Run full suite: PYENV_VERSION=3.11.11 pytest tests/. Existing tests (especially tests/test_task_kernel_attested.py and tests/test_inbox_consume.py with their attestor_kind in {agent,actor} invariants) must remain green. (3) Manual smoke: PYENV_VERSION=3.11.11 python -m artagents author test builtin.hype --fixture smoke → assert exit 0. (4) Drift sanity: temporarily mutate the committed golden, rerun the smoke command, assert exit 1 with unified diff, then revert the mutation. If anything fails: read the error, fix the code, re-run. Write a tiny throwaway script that drives author_cli.main against an intentionally drifted golden copy to confirm drift detection works, run it, then delete the script.",
      "depends_on": [
        "T6"
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
    "FLAG-P9-001 (resolved): cmd_start MUST NOT inspect ARTAGENTS_AUTHOR_TEST. The 'not available in normal start' constraint is satisfied structurally — only _cmd_test sets the env var, in run_fixture's save/restore block. If you find yourself adding a guard in cmd_start, stop — it deadlocks the test runner.",
    "FLAG-P9-002 (resolved): validate_attested_identity must keep the canonical attestor_kind enum ('agent' or 'actor') in author-test mode. NEVER return 'author_test' as the kind. Author-test provenance rides on a separate event['source'] = 'author_test' field injected in _dispatch_attested. Existing assertions in tests/test_task_kernel_attested.py:142,160 and tests/test_inbox_consume.py:61 lock this in.",
    "FLAG-P9-003 (open, addressed in T3): run_fixture must branch on peek.step.ack.kind and pass --agent or --actor accordingly. Hardcoding --actor breaks future agent-attested fixtures and writes wrong attestor_kind into the golden.",
    "FLAG-P9-004 (open, addressed in T6): test_author_test_auto_approval needs cmd_start to succeed with ARTAGENTS_AUTHOR_TEST=1 (the FLAG-P9-001 fix). Do NOT pre-create active_run.json/plan.json by hand — that bypasses the very flow the test validates. Seed run state via cmd_start.",
    "Author-test must run only against tempfile.TemporaryDirectory scratch projects roots. No writes under ~/Documents/reigh-workspace/artagents-projects/ during tests.",
    "Stdlib only — no new third-party deps; requirements.txt unchanged.",
    "Hash-chain integrity: don't bypass gate's verify_chain on the live events.jsonl. Normalization (strip 'hash') applies only to the in-memory diff/regenerate path, not to what gets written by append_event.",
    "DSL resolver assumption: artagents/packs/builtin/hype.py (sibling file) is loaded by spec_from_file_location and is NOT shadowed by the existing artagents/packs/builtin/hype/ folder. If compile fails to find it, audit compile.resolve_orchestrator before changing the layout.",
    "tests/test_author_test_scaffold.py is intentionally deleted in T6 (its docstring defers runtime replay to Phase 9). 'Existing tests must continue to pass' explicitly excludes this scaffold suite.",
    "Event factories in artagents/core/task/events.py stay pure — the source='author_test' field is mutated onto the dict in _dispatch_attested AFTER the factory call, BEFORE append_event.",
    "cli.py and test_runner.py should each stay under ~400 lines; functions stay single-responsibility (run_fixture; diff path; regenerate path)."
  ],
  "sense_checks": [
    {
      "id": "SC1",
      "task_id": "T1",
      "question": "Does artagents/core/task/env.py export ARTAGENTS_AUTHOR_TEST and is_author_test_mode()? Does validate_attested_identity in author-test mode (a) still enforce --agent/--actor exclusivity, (b) still require the per-kind flag, (c) skip ARTAGENTS_ACTOR-match and self-ack rejection, and (d) ALWAYS return canonical kind ('agent'/'actor') — never 'author_test'? Does _dispatch_attested set event['source']='author_test' before append_event when in author-test mode? Is cmd_start unchanged (no guard on the env var)?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC2",
      "task_id": "T2",
      "question": "Does normalize.py strip ts/hash/run_id/pid, recursively rewrite absolute paths under run_dir to <RUN_DIR>/<rel>, and provide dump_events_jsonl with sort_keys=True, separators=(',',':'), ensure_ascii=False? Is the strip-vs-recompute choice documented in a one-line comment?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC3",
      "task_id": "T3",
      "question": "Does run_fixture save/restore env vars in finally, copytree the fixture only when present, drive code steps via gate_command + subprocess.run + record_dispatch_complete, and branch on peek.step.ack.kind to pass --agent or --actor (FLAG-P9-003)? Is the iteration cap present (≤200) to fail loud on author bugs?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC4",
      "task_id": "T4",
      "question": "Does _cmd_test compile-on-demand if build/<orch>.json is missing, run inside tempfile.TemporaryDirectory, normalize via normalize_events with run_dir, support --regenerate (writes golden + 'commit if intentional' message), exit 1 with unified-diff headers on drift, and exit 1 with a clear 'rerun with --regenerate' message when no golden exists? Are _VOLATILE_EVENT_FIELDS / _strip_volatile removed?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC5",
      "task_id": "T5",
      "question": "Does artagents/packs/builtin/hype.py compile to qualified_id 'builtin.hype' with one code('noop') step plus one attested('review', ack='actor') step? Does the committed golden contain run_started → step_dispatched/step_completed (noop) → step_attested with attestor_kind='actor', attestor_id='author_test', source='author_test'? Was it minted via --regenerate (not hand-written)?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC6",
      "task_id": "T6",
      "question": "Is tests/test_author_test_scaffold.py deleted? Do the four new tests (pass/drift/regenerate/auto_approval) cover: rc==0 against committed golden; unified-diff headers on drift; byte-equal regenerate; cmd_start succeeds with env var (FLAG-P9-001); attestor_kind=='actor' not 'author_test' (FLAG-P9-002); source=='author_test'; mismatched --actor rejected without env var, accepted with it? Is run state seeded via cmd_start (not pre-created)?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC7",
      "task_id": "T7",
      "question": "Does pytest tests/ pass in full? Does PYENV_VERSION=3.11.11 python -m artagents author test builtin.hype --fixture smoke exit 0 against the committed golden? Does mutating any field of the committed golden cause exit 1 with a unified-diff block? Was the throwaway repro script deleted after use?",
      "executor_note": "",
      "verdict": ""
    }
  ],
  "user_actions": [],
  "meta_commentary": "Phase 9 is the last V1 phase — polish matters. Two flag fixes are load-bearing: (1) cmd_start must NOT inspect ARTAGENTS_AUTHOR_TEST (deadlocks the runner; see FLAG-P9-001), and (2) validate_attested_identity must keep canonical attestor_kind ('agent'/'actor') and let _dispatch_attested stamp source='author_test' independently (FLAG-P9-002). The two open minor flags (P9-003, P9-004) are explicitly handled inside T3 and T6 respectively — read those task descriptions carefully.\n\nExecution order is dependency-driven: T1 (env+gate branch) and T2 (normalize) are independent; T3 (driver) needs T1; T4 (CLI rewrite) needs T2+T3; T5 (fixture+golden) needs T4 (uses --regenerate to mint the committed golden); T6 (tests) needs T5; T7 (validate). DO NOT mint the golden by hand — run the regenerate path so it is byte-equivalent to what the diff path will produce.\n\nAudit step (plan Step 1) is folded into T1's prep — read the cited file:line references (gate.py:510, 790, 904, 1064, 1096; lifecycle_ack.py:102; events.py:25; cli.py:287-371) before editing. Confirm DSL resolver loads sibling .py via spec_from_file_location before assuming hype.py won't shadow with hype/.\n\nConstraints: stdlib only; additive; no writes under real artagents-projects/ (use tempfile.TemporaryDirectory); preserve hash-chained events on disk (normalization is in-memory only). Existing tests stay green except tests/test_author_test_scaffold.py which is intentionally deleted (its docstring defers replay to Phase 9).\n\nIf T7 surfaces a flake or missing piece, fix root-cause then re-run — do not skip tests or weaken assertions to make them pass.",
  "validation": {
    "plan_steps_covered": [
      {
        "plan_step_summary": "Step 1: Audit replay touch points (file/line references in gate, lifecycle, events, cli)",
        "finalize_item_ids": [
          "T1"
        ]
      },
      {
        "plan_step_summary": "Step 2: Add env helper + auto-approval branch in validate_attested_identity and _dispatch_attested; no cmd_start guard",
        "finalize_item_ids": [
          "T1"
        ]
      },
      {
        "plan_step_summary": "Step 3: Add event normalization helper (normalize.py with normalize_events + dump_events_jsonl)",
        "finalize_item_ids": [
          "T2"
        ]
      },
      {
        "plan_step_summary": "Step 4: Build replay driver test_runner.run_fixture with env save/restore, copytree, code+attested loop branching on ack.kind",
        "finalize_item_ids": [
          "T3"
        ]
      },
      {
        "plan_step_summary": "Step 5: Rewrite _cmd_test for Phase 9 + add --regenerate flag + drop dead helpers",
        "finalize_item_ids": [
          "T4"
        ]
      },
      {
        "plan_step_summary": "Step 6: Author canonical hype DSL fixture (hype.py + fixtures/smoke/ + golden/smoke.events.jsonl)",
        "finalize_item_ids": [
          "T5"
        ]
      },
      {
        "plan_step_summary": "Step 7: Tests — delete scaffold, add pass/drift/regenerate/auto_approval suites",
        "finalize_item_ids": [
          "T6"
        ]
      },
      {
        "plan_step_summary": "Step 8: Validation — targeted pytest, full pytest, manual CLI smoke",
        "finalize_item_ids": [
          "T7"
        ]
      }
    ],
    "orphan_tasks": [],
    "completeness_notes": "All 8 plan steps mapped. Step 1 (audit) folds into T1's prep work since it's read-only inspection of cited file:line references that immediately inform the T1 edits — the brief explicitly says simple changes shouldn't have a separate inspect task.",
    "coverage_complete": true
  },
  "baseline_test_command": "PYENV_VERSION=3.11.11 pytest tests/",
  "baseline_test_failures": [],
  "baseline_test_note": "Baseline not run during finalize. The plan asserts existing tests stay green except for tests/test_author_test_scaffold.py which is deliberately deleted in T6 (its Phase-5 stub is what Phase 9 replaces; the docstring explicitly defers runtime replay to Phase 9). Existing invariants in tests/test_task_kernel_attested.py:142,160 and tests/test_inbox_consume.py:61 (attestor_kind ∈ {agent, actor}) are intentionally preserved by the FLAG-P9-002 fix and must continue to pass."
}
```

> TOOL

tool_result StructuredOutput
```
Structured output provided successfully
```

> AGENT

Finalize document produced: 7 tasks (T1–T7) covering all 8 plan steps, with the Step-1 audit folded into T1's prep. Both load-bearing flag fixes (P9-001 no `cmd_start` guard; P9-002 canonical `attestor_kind` + separate `source` field) are explicit in T1, and the open minor flags (P9-003 ack-kind branching; P9-004 cmd_start-seeds-active-run) are addressed in T3 and T6 respectively. Validation block confirms full coverage; no `user_actions` needed.
