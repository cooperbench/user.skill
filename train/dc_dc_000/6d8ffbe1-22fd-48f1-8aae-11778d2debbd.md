> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

WRITE ACCESS CONTRACT: You are running with auto-approved writes inside a writable workspace. Treat the working directory as fully writable. Do NOT preemptively skip or block tasks on permission, sandbox, or read-only grounds. Attempt every required edit; only report failure AFTER a real OS-level rejection from a specific shell command. Do not infer 'read-only' from absence of activity; absence is not denial. If a single shell command unexpectedly fails, retry with a different invocation before concluding the environment is restricted.

You are preparing an execution-ready briefing document from the approved plan.

        Project directory:
        /Users/user_c042661f/Documents/reigh-workspace/.megaplan-worktrees/phase-8-20260505/all-claude





        Idea:
Implement Phase 8 (Inbox surface) of the ArtAgents orchestrator V1 design per docs/orchestrator-v1-plan.md section 12 (Phase 8).

LAUNCHER: every `megaplan` call = `PYENV_VERSION=3.11.11 python -m megaplan ...`.

DRIVING DISCIPLINE: After every CLI call, run `megaplan status --plan <name>` and `megaplan progress --plan <name>`. If `state == finalized` and `batches_remaining > 0`, you MUST run `megaplan execute --plan <name> --confirm-destructive --batch N` for each remaining batch sequentially. DO NOT EXIT while state != done.


PHASE 8 SCOPE (from docs/orchestrator-v1-plan.md):

- `runs/<run-id>/inbox/` directory for external completion-signal protocol.
- Files dropped into the inbox by external processes (humans, scripts, other tools) signal that an attested step has completed.
- Inbox files validate into events on the next `next`/`status`/`ack` call.
- Stale or malformed files are ignored (logged but do not crash).
- Files touched: `artagents/core/task/`, lifecycle status/next handlers.

EXIT CRITERIA (from design doc):
- Inbox files validate into events.
- Stale or malformed files are ignored.

WHAT TO IMPLEMENT:

1. Define inbox file format. A simple JSON shape:
   ```json
   {
     "step_id": "...",
     "decision": "approve" | "retry" | "abort",
     "evidence": { ... step-specific artifacts ... },
     "submitted_at": "ISO 8601",
     "submitted_by": "<external-system-name>"
   }
   ```

2. New module `artagents/core/task/inbox.py`:
   - `inbox_dir(run_dir) -> Path` — returns `<run_dir>/inbox/`
   - `scan_inbox(run_dir) -> list[InboxEntry]` — reads, validates, returns parsed entries. Malformed files are logged and skipped, not raised.
   - `consume_inbox_entry(run_dir, entry) -> EventRecord` — validates the entry against the current step expectations, writes a hash-chained event, then moves the inbox file to `<run_dir>/inbox/.consumed/<hash>` (or deletes — pick one and document it).

3. Hook into lifecycle handlers:
   - `artagents next`: scans inbox before computing next step. If the inbox has a valid entry for the current attested step, consume it (record event), then advance the cursor.
   - `artagents status`: scans inbox in read-only mode and surfaces "X inbox entries pending" in output.
   - `artagents ack`: not changed (ack is the explicit verb; inbox is the implicit signal channel).

4. Tests:
   - `tests/test_inbox_scan.py`: drops 3 valid + 1 malformed file, scan returns 3 valid entries and ignores the malformed one without raising.
   - `tests/test_inbox_consume.py`: full flow — attested step waits, drop a valid inbox entry, call `next`, assert event is recorded and cursor advances.
   - `tests/test_inbox_stale.py`: drop an entry referencing a step_id that doesn't match current step, assert it's ignored (logged, not consumed).

5. `runs/<run-id>/AGENT.md` template should mention the inbox surface for human/external operators.

CONSTRAINTS:
- Stay within Phase 8 scope. Do NOT touch Phase 9 golden tests.
- Additive only. Existing tests must continue to pass.
- No new dependencies.
- Inbox is opt-in: presence of `inbox/` directory triggers scanning, absence skips it.
- Honor existing patterns: hash-chained events, gate above dispatch, file-based state.

STOP CONDITION: Phase 8 done when `pytest tests/` passes with new inbox tests + status/next surface inbox entries appropriately.

        Approved plan:

# Implementation Plan: Phase 8 — Inbox Surface

## Overview

Phase 8 introduces a file-drop completion-signal protocol so external processes (humans, scripts, other tools) can attest to a current attested step by dropping a JSON file under `runs/<run-id>/inbox/`. The next `next` / `status` call validates the file against the current cursor, emits a hash-chained event (consuming the file), or logs and ignores it (when stale, malformed, or targeting an ineligible step).

Repository shape:
- Phases 1-7 already landed: kernel (`artagents/core/task/{events,gate,plan,active_run,env,cas}.py`), lifecycle verbs (`lifecycle.py` + `lifecycle_ack.py`), produces+repeat, authoring DSL, stop-hook nudge, per-project CAS.
- Existing patterns to honor: hash-chained `events.jsonl` via `append_event`; `peek_current_step` to read the cursor without mutation; `gate_command` for the dispatch path; `match_attested_command` for identity tokens; `validate_attested_identity` for `--agent` / `--actor` rules; `step_attested` / `item_attested` for approve outcomes; `cursor_rewind` for retry; `make_run_aborted_event` + `clear_active_run` for abort.
- Inbox is **opt-in**: the presence of `<run_dir>/inbox/` triggers scanning. Absence is a no-op.

Eligibility (resolves FLAG-P8-001):
- `validate_attested_identity` rejects `--agent` on `ack.kind="actor"` steps and requires `ARTAGENTS_ACTOR` to match `--actor` on actor steps. A file-drop script cannot satisfy the env-pinned actor path.
- **Phase 8 inbox supports `ack.kind="agent"` attested steps only.** Files targeting an `ack.kind="actor"` step are explicitly skipped with a one-line warning and **moved to `<run_dir>/inbox/.rejected/<sha256>`** so they do not zombie in `inbox/` and keep re-triggering the warning on every `next` / `status` call.
- This narrows the inbox surface but matches the doc's framing of inbox as the channel for "external processes" (scripts, automated systems) — humans use the explicit `ack` verb.

Scope guardrails:
- Additive only. No changes to gate semantics, plan format, or existing event kinds.
- No new dependencies.
- Do not touch Phase 9 (golden tests).
- Reuse existing helpers wherever possible — inbox is glue, not a new gate.

## Main Phase

### Step 1: Define the inbox module (`artagents/core/task/inbox.py`)
**Scope:** Medium

1. **Create** new module with module-level constants and dataclasses:
   - `INBOX_DIR_NAME = "inbox"`, `CONSUMED_DIR_NAME = ".consumed"`, `REJECTED_DIR_NAME = ".rejected"`.
   - `@dataclass(frozen=True) class InboxEntry`: fields `path: Path`, `step_id: str`, `decision: str`, `evidence: tuple[str, ...]`, `submitted_at: str`, `submitted_by: str`, `item_id: str | None`, `raw: dict`.
   - `class InboxValidationError(Exception)` — internal-only; `scan_inbox` catches and converts to log-and-skip.
   - Module-level `_LOGGER = logging.getLogger("artagents.core.task.inbox")`.
2. **Implement** `inbox_dir(run_dir: Path) -> Path` → `run_dir / INBOX_DIR_NAME`.
3. **Implement** `scan_inbox(run_dir: Path) -> list[InboxEntry]`:
   - If `inbox_dir(run_dir)` does not exist, return `[]`.
   - Iterate top-level entries (skip `.consumed/`, `.rejected/`, dot-prefixed names, subdirs).
   - For each file: read, `json.loads`, validate required fields:
     - `step_id: str` non-empty,
     - `decision in {"approve","retry","abort"}`,
     - `submitted_at: str`, `submitted_by: str`,
     - optional `evidence: dict[str, Any]` flattened to `tuple(str(v) for v in evidence.values())` (insertion order),
     - optional `item_id: str` for for_each targeting.
   - On `OSError` / `json.JSONDecodeError` / schema mismatch: `_LOGGER.warning(...)` with the file name and reason, **skip**. Return only valid entries. Files are sorted by `submitted_at` then filename for deterministic processing.
4. **Implement** `consume_inbox_entry(run_dir, entry, *, slug, projects_root) -> bool`:
   - Compute `peek = peek_current_step(plan, events, slug, project_root=proj_root, run_id=run_id)`.
   - **Stale / ineligible cursor checks** (return `False` without writing events; behavior per branch documented below):
     - Cursor is exhausted, on a `CodeStep`, or `entry.step_id != STEP_PATH_SEP.join(peek.path_tuple)` → log warning, **leave file in place** (operator may correct it). Return `False`.
   - **Eligibility branch on `ack.kind`** (resolves FLAG-P8-001):
     - If decision is `approve` and `peek.step.ack.kind == "actor"`: log warning `"inbox: skipping {file}: ack.kind=actor not supported by inbox protocol (use 'artagents ack --actor ... --decision approve')"`, **move to `.rejected/<sha256>`** so the warning fires once. Return `False`.
     - If decision is `approve` and `peek.step.ack.kind == "agent"`: synthesize incoming command exactly like `cmd_ack._ack_approve` does: `parts = [step.command, "--agent", entry.submitted_by]`, append `["--evidence", e]` per evidence string, append `["--item", entry.item_id]` if entry has one. Call `gate_command(slug, " ".join(shlex.quote(p) for p in parts), [], root=projects_root)`. The gate writes `step_attested` (or `item_attested`) and runs inline produces checks. Call `record_dispatch_complete(decision, 0)` for symmetry.
     - On `TaskRunGateError`: log warning with `exc.reason`, **move to `.rejected/`**. Return `False`. (Failures we surface via the gate — bad evidence, mismatched identity — should not zombie either.)
   - **Retry branch**: if decision is `retry` on an `AttestedStep` whose latest event for the path is `produces_check_failed`:
     - Build `AttestedArgs(agent=entry.submitted_by if ack.kind=="agent" else None, actor=None, evidence=entry.evidence, item=entry.item_id)`.
     - Call `validate_attested_identity(...)` — on rejection, move to `.rejected/`, log, return `False`.
     - For `ack.kind="actor"`: not supported on inbox; move to `.rejected/`, log, return `False`.
     - On success: `append_event(events_path, make_cursor_rewind_event(peek.path_tuple, reason="inbox retry"))`. Move file to `.consumed/`. Return `True`.
   - **Abort branch** (no identity required, mirrors `cmd_abort`): `append_event(events_path, make_run_aborted_event(run_id, reason=f"inbox abort by {entry.submitted_by}"))`, then `clear_active_run(slug, root=projects_root)`. Move file to `.consumed/`. Return `True`.
   - **Move helpers** (atomic): `_move_to(file: Path, dest_dir: Path)` creates `dest_dir`, computes `sha256(file_bytes).hexdigest()` for the new name, uses `os.replace`. On `OSError`, log warning and `Path.unlink()` as a fallback so the file does not get re-processed indefinitely.
5. **Helper** `pending_count(run_dir: Path) -> int` returning `len(scan_inbox(run_dir))`. Re-exported for `cmd_status`.

### Step 2: Hook `cmd_next` to consume inbox entries (`artagents/core/task/lifecycle.py`)
**Scope:** Small

1. **Inject** an inbox pass in `cmd_next` after `read_active_run` succeeds and before `peek_current_step` (`artagents/core/task/lifecycle.py:393`-`410`):
   - `run_dir = proj_root / "runs" / run_id`.
   - `for entry in scan_inbox(run_dir):` wrap each `consume_inbox_entry(run_dir, entry, slug=slug, projects_root=projects_root)` call in `try/except (TaskRunGateError, OSError, EventLogError) as exc: _LOGGER.warning(...)` so one bad file never crashes `next`.
   - **Re-read** `events = read_events(events_path)` and recompute `peek` after the loop so the rest of `cmd_next` (ledger rendering, ack template) sees the post-consume state.
2. Keep edits surgical — no comment unless the WHY is non-obvious.

### Step 3: Hook `cmd_status` to surface pending entries (`artagents/core/task/lifecycle.py`)
**Scope:** Small

1. **In** `cmd_status` (`artagents/core/task/lifecycle.py:245`-`311`), after computing `run_id` / `proj_root`, call `pending = pending_count(proj_root / "runs" / run_id)` (read-only — never consume in status).
2. **Print** `f"inbox:     {pending} pending"` between `current:` and `recent events:` only when `pending > 0`, to keep default output byte-stable for existing snapshot tests.

### Step 4: AGENT.md template mentions inbox surface (`artagents/core/task/lifecycle.py`)
**Scope:** Small

1. **Extend** `_AGENT_MD_TEMPLATE` (`artagents/core/task/lifecycle.py:53`) with a new `INBOX SURFACE` section: file shape (`step_id`, `decision`, `evidence`, `submitted_at`, `submitted_by`, optional `item_id`), drop location (`runs/<run_id>/inbox/`), consume-on-next semantics, and the explicit "agent attestations only" caveat (actor steps must use `artagents ack`). Keep under ~12 lines.

### Step 5: Re-export the inbox API (`artagents/core/task/__init__.py`)
**Scope:** Small

1. **Add** `from .inbox import InboxEntry, consume_inbox_entry, inbox_dir, pending_count, scan_inbox` and append to `__all__`.

### Step 6: Tests (`tests/test_inbox_scan.py`, `tests/test_inbox_consume.py`, `tests/test_inbox_stale.py`)
**Scope:** Medium

1. **`tests/test_inbox_scan.py`**: write 3 valid entries + 1 malformed JSON file under `inbox/`. Assert `scan_inbox` returns 3 valid `InboxEntry` objects, does not raise. Assert `scan_inbox` returns `[]` when the directory does not exist.
2. **`tests/test_inbox_consume.py`**: use `_lifecycle_fixtures.setup_run` with an `ack="agent"` attested orchestrator (mirror `_BODY_AGENT` from `tests/test_lifecycle_next.py:36`). Drop a valid `approve` inbox file targeting the current step. Call `cmd_next`. Assert (a) `events.jsonl` has a `step_attested` event with `attestor_kind="agent"` and `attestor_id="external-script"`; (b) `verify_chain` returns `ok=True`; (c) the inbox file moved to `.consumed/`; (d) the next `cmd_next` shows the run as exhausted.
3. **`tests/test_inbox_stale.py`**: drop an inbox file whose `step_id` does not match the current cursor. Call `cmd_next`. Assert no new event was written (event count unchanged), the file remains in `inbox/` (not moved), and the cursor is unchanged. Add a second sub-test: drop an `approve` entry targeting an `ack="actor"` step; assert the file is moved to `.rejected/`, no event is written, and a warning is logged via `caplog`.

### Step 7: Run the full suite
**Scope:** Small

1. **Run** `PYENV_VERSION=3.11.11 python -m pytest tests/test_inbox_scan.py tests/test_inbox_consume.py tests/test_inbox_stale.py -x` first.
2. **Run** `PYENV_VERSION=3.11.11 python -m pytest tests/` to confirm existing tests still pass.

## Execution Order
1. Land `inbox.py` (Step 1) — pure module, smallest blast radius.
2. Wire `cmd_next` and `cmd_status` (Steps 2-3) and update the AGENT.md template (Step 4).
3. Re-export from `__init__` (Step 5).
4. Add tests (Step 6) and prove (Step 7).

## Validation Order
1. Targeted: new inbox tests.
2. Lifecycle regression: `pytest tests/test_lifecycle_*.py` to confirm `cmd_next` / `cmd_status` are byte-stable when `inbox/` is absent.
3. Full suite: `pytest tests/`.


        Plan metadata:
        {
  "version": 2,
  "timestamp": "2026-05-05T00:56:49Z",
  "hash": "sha256:6deb845795c6933f3102885b054f86a0a081c8d1adacdf26bd5c0b7ad8dacc78",
  "changes_summary": "Addressed FLAG-P8-001 by branching `consume_inbox_entry` on `peek.step.ack.kind`: inbox supports `ack.kind=\"agent\"` attested steps only; `ack.kind=\"actor\"` files are skipped with a one-line warning AND moved to `<run_dir>/inbox/.rejected/<sha256>` so they do not zombie. Added the same `.rejected/` quarantine for any `TaskRunGateError` raised mid-consume (bad evidence, mismatched identity). Added a third sub-case to `tests/test_inbox_stale.py` covering the actor-step rejection path. Added `item_id` to `InboxEntry` so for_each item targeting is explicit. Documented the agent-only caveat in the AGENT.md template extension. Tightened the Overview with an Eligibility section that names the FLAG and the design choice.",
  "flags_addressed": [
    {
      "id": "FLAG-P8-001",
      "resolution": "addressed",
      "reason": "consume_inbox_entry now branches on peek.step.ack.kind: agent steps follow the existing approve/retry/abort flow; actor steps are explicitly skipped with a clear warning and the file moves to <run_dir>/inbox/.rejected/<sha256> so it does not zombie in inbox/ and re-trigger warnings on every next/status. The same quarantine path catches TaskRunGateError raised mid-consume. tests/test_inbox_stale.py adds a sub-case asserting the actor-step rejection moves the file to .rejected/ and writes no events. Plan Overview now names the eligibility decision (agent-only) and the doc-framing rationale (inbox is for external processes; humans use ack)."
    }
  ],
  "questions": [
    "How should the `evidence` dict in the inbox payload be flattened into the gate's `tuple[str, ...]` evidence list \u2014 by values only, by `key=value` strings, or by a single JSON-serialized string? The plan assumes values-only.",
    "Should `cmd_status` always print `inbox: 0 pending` for transparency, or only print when `>0` to keep default output unchanged? The plan picks the latter."
  ],
  "success_criteria": [
    {
      "criterion": "`tests/test_inbox_scan.py` passes \u2014 scan_inbox returns 3 valid entries from a directory with 3 valid + 1 malformed file and does not raise",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "`tests/test_inbox_consume.py` passes \u2014 dropping a valid approve entry on an ack.kind=agent step, calling cmd_next, results in a step_attested event in events.jsonl and the file moved to .consumed/",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "`tests/test_inbox_stale.py` passes \u2014 (a) non-matching step_id is logged and left in inbox/ with no event written, (b) approve entry targeting an ack.kind=actor step is moved to .rejected/ and writes no event",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "All existing tests in tests/ continue to pass after changes",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Inbox is opt-in: when `runs/<run-id>/inbox/` does not exist, cmd_next and cmd_status produce byte-identical output to their pre-Phase-8 behavior (verified by existing tests in test_lifecycle_next.py / test_lifecycle_status.py)",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Consumed inbox files are moved to `<run_dir>/inbox/.consumed/`; ineligible/quarantined files are moved to `<run_dir>/inbox/.rejected/`. Neither path is left in `inbox/` to trigger repeated warnings.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "consume_inbox_entry branches on peek.step.ack.kind: ack.kind=agent files are processed via gate_command; ack.kind=actor files are skipped with a warning and quarantined to .rejected/ (FLAG-P8-001 resolution)",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "`scan_inbox` and `consume_inbox_entry` use `logging.getLogger(\"artagents.core.task.inbox\").warning(...)` for all skip paths and do not raise on malformed input",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Hash-chain integrity: every inbox-induced event is appended via `append_event` so verify_chain returns ok=True after consume",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "AGENT.md template (run_dir/AGENT.md) mentions the inbox surface with file shape, drop path, consume-on-next semantics, and the explicit 'agent attestations only' caveat",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "`artagents/core/task/inbox.py` stays under ~300 lines and avoids defensive wrappers around already-validated dataclass fields",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "No new third-party dependencies are added (requirements.txt unchanged)",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "`cmd_next` retains byte-stable preamble output across two consecutive calls when inbox is empty (existing test_preamble_byte_identical_across_two_calls invariant)",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    }
  ],
  "assumptions": [
    "Inbox supports `ack.kind=\"agent\"` attested steps only in Phase 8. Files targeting `ack.kind=\"actor\"` steps are quarantined to `.rejected/` with a clear warning so the operator knows to use `artagents ack` instead. This matches the design doc's framing of inbox as the channel for external processes; humans use the explicit ack verb.",
    "`submitted_by` maps to `--agent` for agent-eligible attested steps. The `ARTAGENTS_ACTOR` coupling on the actor path is incompatible with unattended file-drop scripts.",
    "Consumed inbox files move to `<run_dir>/inbox/.consumed/<sha256>`. Files that fail validation post-scan (stale step_id) stay in `inbox/`. Files that fail eligibility (actor step) or fail mid-consume (TaskRunGateError) move to `<run_dir>/inbox/.rejected/<sha256>` to prevent zombie warnings.",
    "The `evidence` dict in the inbox payload is flattened by value (insertion order) into a tuple of strings and passed via the gate's `--evidence` token mechanism.",
    "`cmd_status` prints `inbox: N pending` only when N > 0 to keep default output byte-stable.",
    "Inbox handling in `cmd_next` is best-effort: any exception from one entry is caught, logged, and processing continues.",
    "Inbox does not introduce any new event kinds. Consumed entries reuse `step_attested` / `item_attested` / `cursor_rewind` / `run_aborted` so existing replay logic works unchanged.",
    "Inbox does not handle the `iterate` decision (cumulative feedback authoring is explicit; inbox handles only `approve` / `retry` / `abort` per the brief).",
    "`cmd_ack` is intentionally not modified \u2014 ack remains the explicit verb; inbox is the implicit signal channel."
  ],
  "delta_from_previous_percent": 37.92,
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
    "id": "FLAG-P8-001",
    "concern": "Inbox-on-actor: submitted_by mapping to --agent makes inbox unusable for any AttestedStep with ack.kind=actor. The synthesized command lacks --actor, and validate_attested_identity at artagents/core/task/gate.py:1075-1083 rejects with 'attested step ack.kind=actor requires --actor' (and even with --actor it would also require ARTAGENTS_ACTOR env to match, which a file-drop script will not set). The plan picks --agent in its assumptions list but does not handle the failure path: gate_command will raise TaskRunGateError mid-consume, which the cmd_next try/except catches and logs, but the inbox file is left in place forever and the operator gets no clear signal that this kind of step is not eligible. consume_inbox_entry should branch on peek.step.ack.kind: skip-with-warning ('inbox not supported for ack.kind=actor steps') for actor steps, or use --actor when ack.kind=actor and accept the ARTAGENTS_ACTOR coupling. As written, an inbox file targeting an actor step becomes a permanent zombie.",
    "evidence": "Addressed FLAG-P8-001 by branching `consume_inbox_entry` on `peek.step.ack.kind`: inbox supports `ack.kind=\"agent\"` attested steps only; `ack.kind=\"actor\"` files are skipped with a one-line warning AND moved to `<run_dir>/inbox/.rejected/<sha256>` so they do not zombie. Added the same `.rejected/` quarantine for any `TaskRunGateError` raised mid-consume (bad evidence, mismatched identity). Added a third sub-case to `tests/test_inbox_stale.py` covering the actor-step rejection path. Added `item_id` to `InboxEntry` so for_each item targeting is explicit. Documented the agent-only caveat in the AGENT.md template extension. Tightened the Overview with an Eligibility section that names the FLAG and the design choice.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "FLAG-P8-002",
    "concern": "Move-to-.consumed naming: the plan specifies move entry.path to inbox/.consumed/<event_hash> but gate_command returns GateDecision, which does not expose the hash of the just-appended step_attested/item_attested event. To compute event_hash the implementor must re-read events.jsonl after the gate write and re-parse the trailing line - extra I/O for an auditable filename that adds little value over the original filename or a content sha. Recommend simplifying to original-filename or sha256(content).json so the move is a deterministic os.replace with no post-hoc disk read. As written the contract is under-specified and will produce ad-hoc implementations.",
    "evidence": "artagents/core/task/gate.py:78-92 (GateDecision fields - no event hash); plan Step 1.4 specifies <event_hash> filename without saying how to derive it.",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "FLAG-P8-003",
    "concern": "Evidence dict flattening risks shlex/match degradation: the plan coerces JSON evidence dict to tuple[str, ...] of dict values. If any value is non-string (number, list, nested dict) the synthesized command will pass arbitrary stringified objects as --evidence tokens. match_attested_command at artagents/core/task/gate.py:1025-1061 will accept any string, so the gate won't reject; but downstream evidence-consuming code (e.g. _extract_iterate_feedback) and operator audit-readability degrade. scan_inbox should validate that every evidence value is a non-empty string and reject the file as malformed otherwise (logged-and-skipped per the brief). Also, the brief and plan disagree on shape: brief says evidence is an object, gate semantically uses tuple[str,...]; consider accepting either a list-of-strings or a dict-of-strings and document.",
    "evidence": "Plan Step 1.3 ('Coerce evidence dict to tuple[str, ...] of values'); brief JSON shape uses object for evidence; artagents/core/task/gate.py:1025-1061 (match_attested_command tokenization).",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "FLAG-P8-004",
    "concern": "for_each item_id missing from inbox shape: when the current cursor is inside a for_each host, gate dispatch picks first-uncompleted item unless the synthesized command carries --item <id> (artagents/core/task/gate.py:768-787). The plan says --item <id> if peek is in a for_each frame and the entry includes one but the documented JSON shape (step_id/decision/evidence/submitted_at/submitted_by) has no item_id field, so external authors have no way to target a specific item. In practice the inbox will always advance the next-due item - fine for sequential approvals but surprising if an operator drops two files for two different items concurrently. Either add item_id to the documented shape (and tests), or explicitly document 'inbox advances the next-due item only' as a Phase 8 limitation.",
    "evidence": "Phase 8 brief JSON shape lists step_id/decision/evidence/submitted_at/submitted_by only; artagents/core/task/gate.py:768-787 (target_item resolution from --item).",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "FLAG-P8-005",
    "concern": "cmd_next becomes state-mutating: pre-Phase-8, cmd_next is a printer (a 'see next legal action' verb operators run repeatedly without side effects). After the plan's hook, cmd_next consumes inbox files mid-call and writes step_attested / cursor_rewind / run_aborted events. The 'inbox empty implies byte-stable' invariant holds only when the directory is empty/absent; the moment a file is present, the second next call produces different output from the first, and operators using next purely to inspect the run will inadvertently advance the cursor. Either accept this and document loudly (the AGENT.md INBOX SURFACE section should warn 'artagents next consumes inbox/'), or split the consume side into a dedicated verb (artagents inbox consume) and have status/next surface counts only. The plan picks implicit-consume but does not warn operators.",
    "evidence": "artagents/core/task/lifecycle.py:367-521 (cmd_next is currently read-only printer); plan Step 2 hooks consume into cmd_next directly.",
    "status": "open",
    "severity": "minor"
  }
]

        Critique history:
        [
  {
    "iteration": 1,
    "flag_count": 5,
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
      "description": "Create artagents/core/task/inbox.py with: module constants (INBOX_DIR_NAME='inbox', CONSUMED_DIR_NAME='.consumed', REJECTED_DIR_NAME='.rejected'), module logger _LOGGER=logging.getLogger('artagents.core.task.inbox'), frozen dataclass InboxEntry(path: Path, step_id: str, decision: str, evidence: tuple[str, ...], submitted_at: str, submitted_by: str, item_id: str | None, raw: dict), internal InboxValidationError exception, and helper inbox_dir(run_dir) -> run_dir / 'inbox'. Also implement pending_count(run_dir) -> int delegating to scan_inbox.",
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
      "description": "Implement scan_inbox(run_dir) in inbox.py: return [] if inbox dir absent. Iterate top-level entries (skip subdirs and dot-prefixed names like .consumed/.rejected). For each file: read bytes, json.loads, validate required fields step_id (non-empty str), decision in {'approve','retry','abort'}, submitted_at (str), submitted_by (str). Optional evidence: dict where every value is a non-empty string -> flatten to tuple(str(v) for v in evidence.values()) preserving insertion order; reject the file as malformed if any evidence value is non-string or empty (FLAG-P8-003). Optional item_id (str). On OSError/JSONDecodeError/schema mismatch: _LOGGER.warning(file name + reason) and skip. Sort returned entries by (submitted_at, filename) for deterministic ordering.",
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
      "id": "T3",
      "description": "Implement consume_inbox_entry(run_dir, entry, *, slug, projects_root) -> bool in inbox.py. Compute peek via peek_current_step. Stale checks (cursor exhausted, on CodeStep, or step_id mismatch): log warning and leave file in place, return False. Branch on decision: APPROVE — if peek.step.ack.kind=='actor' log warning 'inbox: skipping <file>: ack.kind=actor not supported by inbox protocol (use artagents ack ...)' and move to .rejected/<sha256> (FLAG-P8-001); if ack.kind=='agent' synthesize parts=[step.command,'--agent',entry.submitted_by] then ['--evidence',e] per evidence string then ['--item',entry.item_id] when present, call gate_command(slug, shlex-joined, [], root=projects_root); on TaskRunGateError log exc.reason and move to .rejected/, return False; on success move file to .consumed/ and return True. RETRY — only valid when latest event for the path is produces_check_failed and ack.kind=='agent'; build AttestedArgs and validate_attested_identity (on rejection move to .rejected/), append make_cursor_rewind_event(peek.path_tuple, reason='inbox retry') via append_event, move to .consumed/, return True. ABORT — append make_run_aborted_event(run_id, reason=f'inbox abort by {entry.submitted_by}'), call clear_active_run(slug, root=projects_root), move to .consumed/, return True. Provide _move_to(file, dest_dir) helper that creates dest_dir, computes sha256(file_bytes).hexdigest() for the new filename, uses os.replace; on OSError log warning and unlink as fallback so files do not loop.",
      "depends_on": [
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
      "description": "Hook inbox consumption into cmd_next in artagents/core/task/lifecycle.py: after read_active_run succeeds and before peek_current_step (~line 393-410), compute run_dir = proj_root/'runs'/run_id and iterate scan_inbox(run_dir), calling consume_inbox_entry inside try/except (TaskRunGateError, OSError, EventLogError) so a single bad file never crashes next. After the loop, re-read events via read_events(events_path) and recompute peek so the rest of cmd_next observes post-consume state. Keep edits surgical; no new comments unless WHY is non-obvious.",
      "depends_on": [
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
      "description": "Hook pending count into cmd_status in artagents/core/task/lifecycle.py (~line 245-311): after run_id/proj_root are computed, call pending = pending_count(proj_root/'runs'/run_id) read-only (never consume). Print 'inbox:     {pending} pending' between the 'current:' line and 'recent events:' ONLY when pending > 0 to keep default output byte-stable for existing snapshot/lifecycle tests.",
      "depends_on": [
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
      "description": "Extend _AGENT_MD_TEMPLATE in artagents/core/task/lifecycle.py (~line 53) with a new INBOX SURFACE section (~12 lines): file shape (step_id, decision, evidence, submitted_at, submitted_by, optional item_id), drop location runs/<run_id>/inbox/, consume-on-next semantics, the explicit 'agent attestations only — actor steps must use artagents ack' caveat (FLAG-P8-001), and a one-line operator warning that 'artagents next consumes inbox/' so they know cmd_next becomes state-mutating when inbox files are present (FLAG-P8-005).",
      "depends_on": [
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
      "description": "Re-export inbox API from artagents/core/task/__init__.py: add `from .inbox import InboxEntry, consume_inbox_entry, inbox_dir, pending_count, scan_inbox` and append those names to __all__.",
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
      "id": "T8",
      "description": "Write tests/test_inbox_scan.py: drop 3 valid JSON files (varied submitted_at/submitted_by) plus 1 malformed JSON file under runs/<id>/inbox/. Assert scan_inbox returns 3 InboxEntry objects, did not raise, and the malformed file produced a logged warning (use caplog). Add a sub-test asserting scan_inbox returns [] when the inbox directory does not exist (opt-in behavior).",
      "depends_on": [
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
    },
    {
      "id": "T9",
      "description": "Write tests/test_inbox_consume.py: use the existing _lifecycle_fixtures.setup_run helper with an ack='agent' attested orchestrator (mirror _BODY_AGENT in tests/test_lifecycle_next.py:36). Drop a valid approve inbox file targeting the current step with submitted_by='external-script' and a non-empty evidence dict. Call cmd_next. Assert (a) events.jsonl contains a step_attested event with attestor_kind='agent' and attestor_id='external-script'; (b) verify_chain(...) returns ok=True; (c) the inbox file was moved to inbox/.consumed/ (not just deleted); (d) a follow-up cmd_next call shows the run as exhausted.",
      "depends_on": [
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
    },
    {
      "id": "T10",
      "description": "Write tests/test_inbox_stale.py with three sub-cases: (a) drop an inbox approve file whose step_id does NOT match the current cursor — call cmd_next, assert no new event was written (event count unchanged), file remains in inbox/ (not moved), and cursor is unchanged; (b) drop an approve entry targeting an ack='actor' attested step — assert the file is moved to inbox/.rejected/, no event is written, and a warning was logged via caplog (FLAG-P8-001); (c) drop a malformed (bad JSON) file — assert it is skipped, left in place, and warning is logged.",
      "depends_on": [
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
    },
    {
      "id": "T11",
      "description": "Run targeted then full test suite. First: `PYENV_VERSION=3.11.11 python -m pytest tests/test_inbox_scan.py tests/test_inbox_consume.py tests/test_inbox_stale.py -x`. Then lifecycle regression: `PYENV_VERSION=3.11.11 python -m pytest tests/test_lifecycle_next.py tests/test_lifecycle_status.py tests/test_lifecycle_ack.py -x` to verify byte-stable behavior when inbox/ is absent. Finally `PYENV_VERSION=3.11.11 python -m pytest tests/` for the full sweep. If any test fails: read the error, fix the underlying code (do NOT modify test expectations to make them pass unless the test was wrong), and re-run until green. Additionally, write a small throwaway script that reproduces the Phase 8 happy path (init a run, drop an approve inbox file, call cmd_next, print events.jsonl tail) to confirm end-to-end behavior, then delete the script.",
      "depends_on": [
        "T4",
        "T5",
        "T6",
        "T8",
        "T9",
        "T10"
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
    "Inbox is opt-in: when runs/<id>/inbox/ does not exist, cmd_next and cmd_status MUST be byte-identical to pre-Phase-8 output. Existing test_lifecycle_next.py / test_lifecycle_status.py snapshots are the canary.",
    "FLAG-P8-001: ack.kind='actor' files must be quarantined to .rejected/ with a clear warning, NOT left in inbox/ to zombie. The same .rejected/ path catches TaskRunGateError raised mid-consume so failed-evidence files do not loop.",
    "FLAG-P8-005: cmd_next becomes state-mutating when inbox files are present. AGENT.md must warn operators that 'artagents next consumes inbox/' so they don't accidentally advance the cursor while inspecting state.",
    "Hash-chain integrity: every inbox-induced event must go through append_event so verify_chain returns ok=True after consume. Do NOT bypass append_event.",
    "Re-read events and recompute peek inside cmd_next AFTER the inbox consume loop — otherwise the rest of cmd_next renders pre-consume state and prints the wrong ledger / ack template.",
    "Evidence values must all be non-empty strings (FLAG-P8-003). scan_inbox should reject (log+skip) entries where any evidence value is non-string, to prevent stringified objects flowing through gate_command's --evidence tokens.",
    "Filename for moved files: use sha256(file_bytes).hexdigest() to avoid the FLAG-P8-002 problem of trying to derive the just-appended event hash via post-hoc events.jsonl re-read.",
    "Best-effort consume in cmd_next: each entry wrapped in try/except so one bad file never crashes the verb. Catch (TaskRunGateError, OSError, EventLogError).",
    "Do NOT modify cmd_ack — ack remains the explicit verb; inbox is the implicit signal channel. Phase 8 is additive only.",
    "Phase 9 (golden tests) is out of scope. Do not touch it.",
    "No new third-party dependencies. requirements.txt must remain unchanged.",
    "for_each item targeting via optional item_id is supported in InboxEntry but the documented JSON shape now exposes item_id explicitly (FLAG-P8-004). Tests should at least sanity-check non-for_each happy path; explicit for_each item targeting is a future enhancement.",
    "Inbox does NOT introduce any new event kinds — reuse step_attested / item_attested / cursor_rewind / run_aborted so existing replay logic continues to work.",
    "inbox.py target size: under ~300 lines; avoid defensive wrappers around already-validated dataclass fields."
  ],
  "sense_checks": [
    {
      "id": "SC1",
      "task_id": "T1",
      "question": "Does inbox.py define InboxEntry as a frozen dataclass with all required fields including item_id, the module-level logger, and the constants for inbox/.consumed/.rejected directory names without importing any new third-party deps?",
      "verdict": ""
    },
    {
      "id": "SC2",
      "task_id": "T2",
      "question": "Does scan_inbox skip subdirectories and dot-prefixed names, validate decision is in {approve,retry,abort}, validate every evidence value is a non-empty string, return entries sorted by (submitted_at, filename), and never raise on malformed input (instead log+skip via _LOGGER.warning)?",
      "verdict": ""
    },
    {
      "id": "SC3",
      "task_id": "T3",
      "question": "Does consume_inbox_entry branch on peek.step.ack.kind so 'actor' approve entries are quarantined to .rejected/<sha256> with a one-line warning (FLAG-P8-001), 'agent' entries call gate_command via shlex-joined synthesized parts, TaskRunGateError raised mid-consume also moves the file to .rejected/, abort branch calls clear_active_run after appending make_run_aborted_event, and stale-cursor entries are left in inbox/ untouched?",
      "verdict": ""
    },
    {
      "id": "SC4",
      "task_id": "T4",
      "question": "Does cmd_next's inbox loop run after read_active_run and before peek_current_step, wrap each entry in try/except for TaskRunGateError/OSError/EventLogError, and re-read events plus recompute peek AFTER the loop so subsequent ledger and ack-template rendering observes post-consume state?",
      "verdict": ""
    },
    {
      "id": "SC5",
      "task_id": "T5",
      "question": "Does cmd_status only print the 'inbox: N pending' line when pending > 0 (preserving byte-stable default output), and does it use a read-only call (pending_count) without invoking consume_inbox_entry?",
      "verdict": ""
    },
    {
      "id": "SC6",
      "task_id": "T6",
      "question": "Does the AGENT.md template's INBOX SURFACE section document the JSON shape (including item_id), the drop location runs/<run_id>/inbox/, consume-on-next semantics, the agent-attestations-only caveat (FLAG-P8-001), and the operator warning that 'artagents next consumes inbox/' (FLAG-P8-005)?",
      "verdict": ""
    },
    {
      "id": "SC7",
      "task_id": "T7",
      "question": "Are InboxEntry, consume_inbox_entry, inbox_dir, pending_count, and scan_inbox both imported and added to __all__ in artagents/core/task/__init__.py?",
      "verdict": ""
    },
    {
      "id": "SC8",
      "task_id": "T8",
      "question": "Does test_inbox_scan.py drop 3 valid + 1 malformed file, assert scan_inbox returns exactly 3 entries without raising, verify a warning was logged for the malformed file, and include the missing-directory case returning []?",
      "verdict": ""
    },
    {
      "id": "SC9",
      "task_id": "T9",
      "question": "Does test_inbox_consume.py exercise the full happy path on an ack='agent' attested step: cmd_next consumes the inbox file, events.jsonl gains a step_attested with attestor_kind='agent' and attestor_id='external-script', verify_chain ok=True, file moved to inbox/.consumed/, and a follow-up cmd_next reports the run exhausted?",
      "verdict": ""
    },
    {
      "id": "SC10",
      "task_id": "T10",
      "question": "Does test_inbox_stale.py cover all three sub-cases: (a) mismatched step_id leaves file in inbox/ with no event written, (b) approve on ack='actor' step moves file to inbox/.rejected/ with warning logged and no event written, (c) malformed JSON is skipped+logged?",
      "verdict": ""
    },
    {
      "id": "SC11",
      "task_id": "T11",
      "question": "Did all new inbox tests pass, did the lifecycle_next/lifecycle_status/lifecycle_ack tests still pass byte-stably (inbox-empty parity), did the full pytest sweep pass, and was the throwaway happy-path repro script written, executed, then deleted?",
      "verdict": ""
    }
  ],
  "user_actions": [],
  "meta_commentary": "Phase 8 is glue between an external file-drop protocol and the existing kernel — keep it additive and reuse helpers. Critical sequencing: land inbox.py first (T1-T3 build on each other), then wire lifecycle hooks (T4-T6), then re-export (T7), then write tests (T8-T10), then run them (T11). FLAG resolutions to keep front-of-mind: (1) FLAG-P8-001 — branch on peek.step.ack.kind in consume_inbox_entry; actor approve files MUST move to .rejected/ to avoid zombies (test_inbox_stale.py sub-case (b) is the canary). (2) FLAG-P8-002 — use sha256(file_bytes) for the moved-file name, NOT the appended event hash (which would require post-hoc events.jsonl re-read). (3) FLAG-P8-003 — scan_inbox must reject entries whose evidence values are non-string or empty so junk does not flow through gate_command's --evidence tokens. (4) FLAG-P8-004 — InboxEntry exposes item_id; documented JSON shape includes it. (5) FLAG-P8-005 — cmd_next becomes state-mutating when inbox files exist; AGENT.md template must call this out. Byte-stability invariants: when inbox/ is absent, cmd_next and cmd_status produce identical output to pre-Phase-8 — existing test_lifecycle_next.py / test_lifecycle_status.py / test_preamble_byte_identical_across_two_calls are the canaries; if any of those break, your hook is leaking output. After consuming files in cmd_next, MUST re-read events and recompute peek so the rest of cmd_next observes post-consume state. Hash-chain integrity: every inbox-induced event flows through append_event — verify_chain ok=True is a hard requirement. Do not modify cmd_ack. No new dependencies. inbox.py should stay under ~300 lines; resist defensive wrapping around already-validated dataclass fields.",
  "validation": {
    "plan_steps_covered": [
      {
        "plan_step_summary": "Step 1: Define inbox module with constants, dataclass InboxEntry, scan_inbox, consume_inbox_entry, pending_count, _move_to helper, logger",
        "finalize_item_ids": [
          "T1",
          "T2",
          "T3"
        ]
      },
      {
        "plan_step_summary": "Step 2: Hook cmd_next to consume inbox entries (loop with try/except, then re-read events and recompute peek)",
        "finalize_item_ids": [
          "T4"
        ]
      },
      {
        "plan_step_summary": "Step 3: Hook cmd_status to surface pending count read-only, only when > 0 to preserve byte-stable output",
        "finalize_item_ids": [
          "T5"
        ]
      },
      {
        "plan_step_summary": "Step 4: Extend AGENT.md template with INBOX SURFACE section including agent-only caveat and consume-on-next warning",
        "finalize_item_ids": [
          "T6"
        ]
      },
      {
        "plan_step_summary": "Step 5: Re-export inbox API from artagents/core/task/__init__.py",
        "finalize_item_ids": [
          "T7"
        ]
      },
      {
        "plan_step_summary": "Step 6: Tests — test_inbox_scan.py, test_inbox_consume.py, test_inbox_stale.py (with three sub-cases including actor-step rejection)",
        "finalize_item_ids": [
          "T8",
          "T9",
          "T10"
        ]
      },
      {
        "plan_step_summary": "Step 7: Run targeted tests, lifecycle regression tests, and full suite",
        "finalize_item_ids": [
          "T11"
        ]
      }
    ],
    "orphan_tasks": [],
    "completeness_notes": "Every step of the approved plan maps to one or more tasks. Step 1 split into T1 (skeleton/constants/dataclass), T2 (scan_inbox with FLAG-P8-003 evidence validation), and T3 (consume_inbox_entry with FLAG-P8-001 actor branch and FLAG-P8-002 sha256 filename). Steps 2-4 are surgical lifecycle.py edits (T4-T6). Step 5 is the re-export (T7). Step 6 produces the three test files (T8-T10). Step 7 is the validation run (T11). No user_actions are needed — Phase 8 is purely repo-internal additive code with no env vars, no infra, no manual smoke tests required.",
    "coverage_complete": true
  },
  "baseline_test_failures": [],
  "baseline_test_command": "PYENV_VERSION=3.11.11 python -m pytest tests/",
  "baseline_test_note": "Baseline not run during finalize. Plan asserts existing pytest tests/ pass on the current branch (post-Phase 7); Phase 8 must remain additive and keep them green. Executor should run the baseline command before any edits if there is doubt about the starting state."
}
```

> TOOL

tool_result StructuredOutput
```
Output does not match required schema: /sense_checks/0: must have required property 'executor_note', /sense_checks/1: must have required property 'executor_note', /sense_checks/2: must have required property 'executor_note', /sense_checks/3: must have required property 'executor_note', /sense_checks/4: must have required property 'executor_note', /sense_checks/5: must have required property 'executor_note', /sense_checks/6: must have required property 'executor_note', /sense_checks/7: must have required property 'executor_note', /sense_checks/8: must have required property 'executor_note', /sense_checks/9: must have required property 'executor_note', /sense_checks/10: must have required property 'executor_note'
```

> TOOL

tool_use StructuredOutput
```json
{
  "tasks": [
    {
      "id": "T1",
      "description": "Create artagents/core/task/inbox.py with: module constants (INBOX_DIR_NAME='inbox', CONSUMED_DIR_NAME='.consumed', REJECTED_DIR_NAME='.rejected'), module logger _LOGGER=logging.getLogger('artagents.core.task.inbox'), frozen dataclass InboxEntry(path: Path, step_id: str, decision: str, evidence: tuple[str, ...], submitted_at: str, submitted_by: str, item_id: str | None, raw: dict), internal InboxValidationError exception, and helper inbox_dir(run_dir) -> run_dir / 'inbox'. Also implement pending_count(run_dir) -> int delegating to scan_inbox.",
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
      "description": "Implement scan_inbox(run_dir) in inbox.py: return [] if inbox dir absent. Iterate top-level entries (skip subdirs and dot-prefixed names like .consumed/.rejected). For each file: read bytes, json.loads, validate required fields step_id (non-empty str), decision in {'approve','retry','abort'}, submitted_at (str), submitted_by (str). Optional evidence: dict where every value is a non-empty string -> flatten to tuple(str(v) for v in evidence.values()) preserving insertion order; reject the file as malformed if any evidence value is non-string or empty (FLAG-P8-003). Optional item_id (str). On OSError/JSONDecodeError/schema mismatch: _LOGGER.warning(file name + reason) and skip. Sort returned entries by (submitted_at, filename) for deterministic ordering.",
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
      "id": "T3",
      "description": "Implement consume_inbox_entry(run_dir, entry, *, slug, projects_root) -> bool in inbox.py. Compute peek via peek_current_step. Stale checks (cursor exhausted, on CodeStep, or step_id mismatch): log warning and leave file in place, return False. Branch on decision: APPROVE — if peek.step.ack.kind=='actor' log warning 'inbox: skipping <file>: ack.kind=actor not supported by inbox protocol (use artagents ack ...)' and move to .rejected/<sha256> (FLAG-P8-001); if ack.kind=='agent' synthesize parts=[step.command,'--agent',entry.submitted_by] then ['--evidence',e] per evidence string then ['--item',entry.item_id] when present, call gate_command(slug, shlex-joined, [], root=projects_root); on TaskRunGateError log exc.reason and move to .rejected/, return False; on success move file to .consumed/ and return True. RETRY — only valid when latest event for the path is produces_check_failed and ack.kind=='agent'; build AttestedArgs and validate_attested_identity (on rejection move to .rejected/), append make_cursor_rewind_event(peek.path_tuple, reason='inbox retry') via append_event, move to .consumed/, return True. ABORT — append make_run_aborted_event(run_id, reason=f'inbox abort by {entry.submitted_by}'), call clear_active_run(slug, root=projects_root), move to .consumed/, return True. Provide _move_to(file, dest_dir) helper that creates dest_dir, computes sha256(file_bytes).hexdigest() for the new filename, uses os.replace; on OSError log warning and unlink as fallback so files do not loop.",
      "depends_on": [
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
      "description": "Hook inbox consumption into cmd_next in artagents/core/task/lifecycle.py: after read_active_run succeeds and before peek_current_step (~line 393-410), compute run_dir = proj_root/'runs'/run_id and iterate scan_inbox(run_dir), calling consume_inbox_entry inside try/except (TaskRunGateError, OSError, EventLogError) so a single bad file never crashes next. After the loop, re-read events via read_events(events_path) and recompute peek so the rest of cmd_next observes post-consume state. Keep edits surgical; no new comments unless WHY is non-obvious.",
      "depends_on": [
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
      "description": "Hook pending count into cmd_status in artagents/core/task/lifecycle.py (~line 245-311): after run_id/proj_root are computed, call pending = pending_count(proj_root/'runs'/run_id) read-only (never consume). Print 'inbox:     {pending} pending' between the 'current:' line and 'recent events:' ONLY when pending > 0 to keep default output byte-stable for existing snapshot/lifecycle tests.",
      "depends_on": [
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
      "description": "Extend _AGENT_MD_TEMPLATE in artagents/core/task/lifecycle.py (~line 53) with a new INBOX SURFACE section (~12 lines): file shape (step_id, decision, evidence, submitted_at, submitted_by, optional item_id), drop location runs/<run_id>/inbox/, consume-on-next semantics, the explicit 'agent attestations only — actor steps must use artagents ack' caveat (FLAG-P8-001), and a one-line operator warning that 'artagents next consumes inbox/' so they know cmd_next becomes state-mutating when inbox files are present (FLAG-P8-005).",
      "depends_on": [
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
      "description": "Re-export inbox API from artagents/core/task/__init__.py: add `from .inbox import InboxEntry, consume_inbox_entry, inbox_dir, pending_count, scan_inbox` and append those names to __all__.",
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
      "id": "T8",
      "description": "Write tests/test_inbox_scan.py: drop 3 valid JSON files (varied submitted_at/submitted_by) plus 1 malformed JSON file under runs/<id>/inbox/. Assert scan_inbox returns 3 InboxEntry objects, did not raise, and the malformed file produced a logged warning (use caplog). Add a sub-test asserting scan_inbox returns [] when the inbox directory does not exist (opt-in behavior).",
      "depends_on": [
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
    },
    {
      "id": "T9",
      "description": "Write tests/test_inbox_consume.py: use the existing _lifecycle_fixtures.setup_run helper with an ack='agent' attested orchestrator (mirror _BODY_AGENT in tests/test_lifecycle_next.py:36). Drop a valid approve inbox file targeting the current step with submitted_by='external-script' and a non-empty evidence dict. Call cmd_next. Assert (a) events.jsonl contains a step_attested event with attestor_kind='agent' and attestor_id='external-script'; (b) verify_chain(...) returns ok=True; (c) the inbox file was moved to inbox/.consumed/ (not just deleted); (d) a follow-up cmd_next call shows the run as exhausted.",
      "depends_on": [
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
    },
    {
      "id": "T10",
      "description": "Write tests/test_inbox_stale.py with three sub-cases: (a) drop an inbox approve file whose step_id does NOT match the current cursor — call cmd_next, assert no new event was written (event count unchanged), file remains in inbox/ (not moved), and cursor is unchanged; (b) drop an approve entry targeting an ack='actor' attested step — assert the file is moved to inbox/.rejected/, no event is written, and a warning was logged via caplog (FLAG-P8-001); (c) drop a malformed (bad JSON) file — assert it is skipped, left in place, and warning is logged.",
      "depends_on": [
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
    },
    {
      "id": "T11",
      "description": "Run targeted then full test suite. First: `PYENV_VERSION=3.11.11 python -m pytest tests/test_inbox_scan.py tests/test_inbox_consume.py tests/test_inbox_stale.py -x`. Then lifecycle regression: `PYENV_VERSION=3.11.11 python -m pytest tests/test_lifecycle_next.py tests/test_lifecycle_status.py tests/test_lifecycle_ack.py -x` to verify byte-stable behavior when inbox/ is absent. Finally `PYENV_VERSION=3.11.11 python -m pytest tests/` for the full sweep. If any test fails: read the error, fix the underlying code (do NOT modify test expectations to make them pass unless the test was wrong), and re-run until green. Additionally, write a small throwaway script that reproduces the Phase 8 happy path (init a run, drop an approve inbox file, call cmd_next, print events.jsonl tail) to confirm end-to-end behavior, then delete the script.",
      "depends_on": [
        "T4",
        "T5",
        "T6",
        "T8",
        "T9",
        "T10"
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
    "Inbox is opt-in: when runs/<id>/inbox/ does not exist, cmd_next and cmd_status MUST be byte-identical to pre-Phase-8 output. Existing test_lifecycle_next.py / test_lifecycle_status.py snapshots are the canary.",
    "FLAG-P8-001: ack.kind='actor' files must be quarantined to .rejected/ with a clear warning, NOT left in inbox/ to zombie. The same .rejected/ path catches TaskRunGateError raised mid-consume so failed-evidence files do not loop.",
    "FLAG-P8-005: cmd_next becomes state-mutating when inbox files are present. AGENT.md must warn operators that 'artagents next consumes inbox/' so they don't accidentally advance the cursor while inspecting state.",
    "Hash-chain integrity: every inbox-induced event must go through append_event so verify_chain returns ok=True after consume. Do NOT bypass append_event.",
    "Re-read events and recompute peek inside cmd_next AFTER the inbox consume loop — otherwise the rest of cmd_next renders pre-consume state and prints the wrong ledger / ack template.",
    "Evidence values must all be non-empty strings (FLAG-P8-003). scan_inbox should reject (log+skip) entries where any evidence value is non-string, to prevent stringified objects flowing through gate_command's --evidence tokens.",
    "Filename for moved files: use sha256(file_bytes).hexdigest() to avoid the FLAG-P8-002 problem of trying to derive the just-appended event hash via post-hoc events.jsonl re-read.",
    "Best-effort consume in cmd_next: each entry wrapped in try/except so one bad file never crashes the verb. Catch (TaskRunGateError, OSError, EventLogError).",
    "Do NOT modify cmd_ack — ack remains the explicit verb; inbox is the implicit signal channel. Phase 8 is additive only.",
    "Phase 9 (golden tests) is out of scope. Do not touch it.",
    "No new third-party dependencies. requirements.txt must remain unchanged.",
    "for_each item targeting via optional item_id is supported in InboxEntry but the documented JSON shape now exposes item_id explicitly (FLAG-P8-004). Tests should at least sanity-check non-for_each happy path; explicit for_each item targeting is a future enhancement.",
    "Inbox does NOT introduce any new event kinds — reuse step_attested / item_attested / cursor_rewind / run_aborted so existing replay logic continues to work.",
    "inbox.py target size: under ~300 lines; avoid defensive wrappers around already-validated dataclass fields."
  ],
  "sense_checks": [
    {
      "id": "SC1",
      "task_id": "T1",
      "question": "Does inbox.py define InboxEntry as a frozen dataclass with all required fields including item_id, the module-level logger, and the constants for inbox/.consumed/.rejected directory names without importing any new third-party deps?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC2",
      "task_id": "T2",
      "question": "Does scan_inbox skip subdirectories and dot-prefixed names, validate decision is in {approve,retry,abort}, validate every evidence value is a non-empty string, return entries sorted by (submitted_at, filename), and never raise on malformed input (instead log+skip via _LOGGER.warning)?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC3",
      "task_id": "T3",
      "question": "Does consume_inbox_entry branch on peek.step.ack.kind so 'actor' approve entries are quarantined to .rejected/<sha256> with a one-line warning (FLAG-P8-001), 'agent' entries call gate_command via shlex-joined synthesized parts, TaskRunGateError raised mid-consume also moves the file to .rejected/, abort branch calls clear_active_run after appending make_run_aborted_event, and stale-cursor entries are left in inbox/ untouched?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC4",
      "task_id": "T4",
      "question": "Does cmd_next's inbox loop run after read_active_run and before peek_current_step, wrap each entry in try/except for TaskRunGateError/OSError/EventLogError, and re-read events plus recompute peek AFTER the loop so subsequent ledger and ack-template rendering observes post-consume state?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC5",
      "task_id": "T5",
      "question": "Does cmd_status only print the 'inbox: N pending' line when pending > 0 (preserving byte-stable default output), and does it use a read-only call (pending_count) without invoking consume_inbox_entry?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC6",
      "task_id": "T6",
      "question": "Does the AGENT.md template's INBOX SURFACE section document the JSON shape (including item_id), the drop location runs/<run_id>/inbox/, consume-on-next semantics, the agent-attestations-only caveat (FLAG-P8-001), and the operator warning that 'artagents next consumes inbox/' (FLAG-P8-005)?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC7",
      "task_id": "T7",
      "question": "Are InboxEntry, consume_inbox_entry, inbox_dir, pending_count, and scan_inbox both imported and added to __all__ in artagents/core/task/__init__.py?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC8",
      "task_id": "T8",
      "question": "Does test_inbox_scan.py drop 3 valid + 1 malformed file, assert scan_inbox returns exactly 3 entries without raising, verify a warning was logged for the malformed file, and include the missing-directory case returning []?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC9",
      "task_id": "T9",
      "question": "Does test_inbox_consume.py exercise the full happy path on an ack='agent' attested step: cmd_next consumes the inbox file, events.jsonl gains a step_attested with attestor_kind='agent' and attestor_id='external-script', verify_chain ok=True, file moved to inbox/.consumed/, and a follow-up cmd_next reports the run exhausted?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC10",
      "task_id": "T10",
      "question": "Does test_inbox_stale.py cover all three sub-cases: (a) mismatched step_id leaves file in inbox/ with no event written, (b) approve on ack='actor' step moves file to inbox/.rejected/ with warning logged and no event written, (c) malformed JSON is skipped+logged?",
      "executor_note": "",
      "verdict": ""
    },
    {
      "id": "SC11",
      "task_id": "T11",
      "question": "Did all new inbox tests pass, did the lifecycle_next/lifecycle_status/lifecycle_ack tests still pass byte-stably (inbox-empty parity), did the full pytest sweep pass, and was the throwaway happy-path repro script written, executed, then deleted?",
      "executor_note": "",
      "verdict": ""
    }
  ],
  "user_actions": [],
  "meta_commentary": "Phase 8 is glue between an external file-drop protocol and the existing kernel — keep it additive and reuse helpers. Critical sequencing: land inbox.py first (T1-T3 build on each other), then wire lifecycle hooks (T4-T6), then re-export (T7), then write tests (T8-T10), then run them (T11). FLAG resolutions to keep front-of-mind: (1) FLAG-P8-001 — branch on peek.step.ack.kind in consume_inbox_entry; actor approve files MUST move to .rejected/ to avoid zombies (test_inbox_stale.py sub-case (b) is the canary). (2) FLAG-P8-002 — use sha256(file_bytes) for the moved-file name, NOT the appended event hash (which would require post-hoc events.jsonl re-read). (3) FLAG-P8-003 — scan_inbox must reject entries whose evidence values are non-string or empty so junk does not flow through gate_command's --evidence tokens. (4) FLAG-P8-004 — InboxEntry exposes item_id; documented JSON shape includes it. (5) FLAG-P8-005 — cmd_next becomes state-mutating when inbox files exist; AGENT.md template must call this out. Byte-stability invariants: when inbox/ is absent, cmd_next and cmd_status produce identical output to pre-Phase-8 — existing test_lifecycle_next.py / test_lifecycle_status.py / test_preamble_byte_identical_across_two_calls are the canaries; if any of those break, your hook is leaking output. After consuming files in cmd_next, MUST re-read events and recompute peek so the rest of cmd_next observes post-consume state. Hash-chain integrity: every inbox-induced event flows through append_event — verify_chain ok=True is a hard requirement. Do not modify cmd_ack. No new dependencies. inbox.py should stay under ~300 lines; resist defensive wrapping around already-validated dataclass fields.",
  "validation": {
    "plan_steps_covered": [
      {
        "plan_step_summary": "Step 1: Define inbox module with constants, dataclass InboxEntry, scan_inbox, consume_inbox_entry, pending_count, _move_to helper, logger",
        "finalize_item_ids": [
          "T1",
          "T2",
          "T3"
        ]
      },
      {
        "plan_step_summary": "Step 2: Hook cmd_next to consume inbox entries (loop with try/except, then re-read events and recompute peek)",
        "finalize_item_ids": [
          "T4"
        ]
      },
      {
        "plan_step_summary": "Step 3: Hook cmd_status to surface pending count read-only, only when > 0 to preserve byte-stable output",
        "finalize_item_ids": [
          "T5"
        ]
      },
      {
        "plan_step_summary": "Step 4: Extend AGENT.md template with INBOX SURFACE section including agent-only caveat and consume-on-next warning",
        "finalize_item_ids": [
          "T6"
        ]
      },
      {
        "plan_step_summary": "Step 5: Re-export inbox API from artagents/core/task/__init__.py",
        "finalize_item_ids": [
          "T7"
        ]
      },
      {
        "plan_step_summary": "Step 6: Tests — test_inbox_scan.py, test_inbox_consume.py, test_inbox_stale.py (with three sub-cases including actor-step rejection)",
        "finalize_item_ids": [
          "T8",
          "T9",
          "T10"
        ]
      },
      {
        "plan_step_summary": "Step 7: Run targeted tests, lifecycle regression tests, and full suite",
        "finalize_item_ids": [
          "T11"
        ]
      }
    ],
    "orphan_tasks": [],
    "completeness_notes": "Every step of the approved plan maps to one or more tasks. Step 1 split into T1 (skeleton/constants/dataclass), T2 (scan_inbox with FLAG-P8-003 evidence validation), and T3 (consume_inbox_entry with FLAG-P8-001 actor branch and FLAG-P8-002 sha256 filename). Steps 2-4 are surgical lifecycle.py edits (T4-T6). Step 5 is the re-export (T7). Step 6 produces the three test files (T8-T10). Step 7 is the validation run (T11). No user_actions are needed — Phase 8 is purely repo-internal additive code with no env vars, no infra, no manual smoke tests required.",
    "coverage_complete": true
  },
  "baseline_test_failures": [],
  "baseline_test_command": "PYENV_VERSION=3.11.11 python -m pytest tests/",
  "baseline_test_note": "Baseline not run during finalize. Plan asserts existing pytest tests/ pass on the current branch (post-Phase 7); Phase 8 must remain additive and keep them green. Executor should run the baseline command before any edits if there is doubt about the starting state."
}
```

> TOOL

tool_result StructuredOutput
```
Structured output provided successfully
```

> AGENT

Finalize document produced. 11 tasks (T1–T11), 11 sense-checks, no user_actions required (Phase 8 is purely repo-internal). All 5 flags from the gate (FLAG-P8-001 through P8-005) are mapped into watch_items, task descriptions, and meta_commentary so the executor will not lose them mid-implementation. Coverage validation: complete, all 7 plan steps mapped.
