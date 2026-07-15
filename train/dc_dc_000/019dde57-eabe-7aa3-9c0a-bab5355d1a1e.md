> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

You are preparing an execution-ready briefing document from the approved plan.

        Project directory:
        /Users/user_c042661f/Documents/arnold-v2





        Idea:
# Sprint 4 — Sprint mode and handoff gating

Epics can be taken through the full lifecycle to handoff-ready (planned) state, with sprints queued or pending. Every epic produces at least one sprint.

**Full spec is at `planning-bot-spec.md` in this repo root. Refer to Sprint Organization, State Advance Gating, Epic Abstraction Level sections.**

## Supabase
- URL: https://yhwflvadmefhkshwbfnf.supabase.co
- Service key: [REDACTED_SUPABASE_SERVICE_ROLE_JWT]

## Scope

- Tables: sprints (with queue_position, pending_reason, status values), sprint_items
- edit_epic extension for sprints field including status transitions
- State advance gating logic — concrete conditions enforced server-side:
  - shaping → sprinting: body >500 chars, Goal + Deliverable sections, checklist mostly resolved
  - sprinting → planned: all sprints queued or pending, checklist done/skipped/superseded, PM-handoff fidelity
- Open-decisions lockdown scan: regex check for TBD/to be decided/to be determined/we'll see/figure out later/tunable/depends on what surfaces/can adjust later/decide later — matches outside Open Questions section block sprinting → planned unless force-through
- Blocker surfacing flow — list open items, offer skip/address/force
- Sprint shaping: propose → refine → finalize, items at PM-task level
- Every epic produces at least one sprint (including decision docs, conversation prep)
- Two-beat lock-in flow: confirmation → queue/pend assignment (first sprint queued, rest pending)
- Pending reason capture
- Queue reordering via natural language
- Force-through with logging (forced_handoff event)
- Phase-aware end-of-turn checks

## Key Data Model

### sprints
id, epic_id, sprint_number, name, goal, status (proposed|queued|pending|done), queue_position (nullable int), pending_reason (nullable), target_weeks (default 2), created_at, updated_at, queued_at
Unique constraint: (epic_id, queue_position) WHERE status='queued'

### sprint_items
id, sprint_id, content, estimated_complexity (small|medium|large), status (open|in_progress|done), source_section, position, created_at

## Acceptance Criteria

- Try to advance shaping → sprinting with body <500 chars → edit_epic fails with blockers list
- Force-through with force: true → succeeds, forced_handoff event logged
- Sprint shaping → sprints rows edited; lock-in moves to queued/pending
- Decision-doc epic → at least one sprint (test: create, take through lifecycle, assert ≥1 sprint)
- After lock-in: each sprint is queued (with queue_position) or pending (with pending_reason); epic → planned
- Two queued sprints can't share queue_position (DB constraint)
- Post-handoff: "queue sprint 2" → status flips, position assigned
- Post-handoff: "do sprint 3 first" → queue_positions adjusted, audit event logged
- Lockdown scan blocks when body contains "TBD" outside Open Questions; passes when in Open Questions

## Tests
- Unit: gating condition evaluation; confirmation parsing; queue/pend defaults; queue reordering; lockdown scan regex
- Integration: full epic lifecycle (create → shape → sprint → finalize → queue/pend → planned)

        Approved plan:
        # Implementation Plan: Sprint 4 Sprint Mode And Handoff Gating

## Overview
Arnold already has the Sprint 2 editorial core: markdown body helpers in `agent_kit/body.py`, `edit_epic` in `agent_kit/tools/editorial.py`, store ports/adapters in `agent_kit/ports.py`, `agent_kit/store/sqlite.py`, `agent_kit/store/supabase.py`, SQLite/Supabase migrations, prompts, invocation envelopes, and editorial read/time-travel tools. The main write insertion point is explicit: `edit_epic` currently rejects both `changes.sprints` and `changes.state` at `agent_kit/tools/editorial.py:133`, so Sprint 4 should remove that guard and add server-side sprint writes plus gated state transitions.

The critique flags do not show that the plan targeted the wrong root cause. The root write path is still `edit_epic`; the missing pieces are downstream visibility surfaces. Sprint 4 state transitions and sprint changes must be observable through invocation envelopes and existing read/replay tools, or callable clients and users can see stale state even when the database write succeeds.

The simplest direct approach is to keep `edit_epic` as the single write surface, add store-level sprint CRUD methods, enforce lifecycle invariants server-side, and then wire every existing observation path: hot context, read tools, time-travel replay, revert, and invocation envelopes.

## Phase 1: Data Model And Store Port

### Step 1: Add sprint migrations (`agent_kit/store/migrations/sqlite/006_sprints.sql`, `supabase/migrations/202604300006_006_sprints.sql`)
**Scope:** Medium
1. Create `sprints` and `sprint_items` with the specified fields and status checks.
2. Add a partial unique index for queued positions: SQLite `CREATE UNIQUE INDEX ... WHERE status = 'queued'`; Postgres/Supabase same partial unique index.
3. Add read indexes on `sprints(epic_id, sprint_number)`, `sprints(epic_id, status, queue_position)`, and `sprint_items(sprint_id, position)`.

### Step 2: Extend the store protocol (`agent_kit/ports.py`)
**Scope:** Medium
1. Add sprint methods near the existing epic/checklist methods at `agent_kit/ports.py:249`: `create_sprint`, `load_sprint`, `list_sprints`, `update_sprint`, `delete_sprint`, `replace_sprint_items`, `list_sprint_items`, and a helper that returns sprints with items for an epic.
2. Keep these methods low-level and predictable; validation belongs in the Sprint 4 domain/tool layer, not in adapters.

### Step 3: Implement SQLite and Supabase adapters (`agent_kit/store/sqlite.py`, `agent_kit/store/supabase.py`)
**Scope:** Medium
1. Add `_SPRINT_COLUMNS` and `_SPRINT_ITEM_COLUMNS` beside `_EPIC_COLUMNS` at `agent_kit/store/sqlite.py:1210` and the equivalent Supabase constants.
2. Implement sprint CRUD around the existing patterns for `checklist_items` at `agent_kit/store/sqlite.py:682` and Supabase equivalent.
3. Update `load_hot_context` at `agent_kit/store/sqlite.py:362` and `agent_kit/store/supabase.py:188` to include current sprints and items so the model can reason about queued/pending state.
4. Extend store contract tests so SQLite and Supabase fake adapter behavior stay aligned.

## Phase 2: Deterministic Sprint Domain Logic

### Step 4: Add a sprint domain module (`agent_kit/sprints.py`)
**Scope:** Large
1. Implement normalization and validation for sprint payloads: sprint number uniqueness, allowed statuses, item complexity/status values, queued sprint position requirement, pending reason capture, and PM-task-level item checks.
2. Implement default lock-in assignment: first sprint queued at the next available position, remaining sprints pending with a supplied or default pending reason.
3. Implement queue operations for post-handoff updates: queue a sprint, pend a sprint, and reorder queued sprints with gapless positions.
4. Return structured sprint-change summaries so `edit_epic` can put them in tool results, audit events, and invocation envelopes.

### Step 5: Add gate evaluators (`agent_kit/gating.py`)
**Scope:** Large
1. Implement `evaluate_state_transition(epic, body, checklist, sprints, target_state)` with explicit blockers.
2. Enforce `shaping -> sprinting`: body length >500, `Goal` and `Deliverable` sections exist, and checklist is mostly resolved using the spec rule of fewer than 3 open items unless open items have material content.
3. Enforce `sprinting -> planned`: at least one sprint, all sprints queued or pending, queued sprints have unique queue positions, pending sprints have pending reasons or a recorded no-reason value, checklist statuses are only `done`, `skipped`, or `superseded`, and body passes a deterministic PM-handoff heuristic.
4. Keep the PM-handoff heuristic concrete and testable: require non-placeholder Goal/Deliverable, at least one decision/principle/context section with substantive content, no unresolved lockdown phrase outside Open Questions, and PM-level sprint items. Do not add a live LLM dependency for server enforcement unless explicitly chosen later.

### Step 6: Implement lockdown scanning (`agent_kit/lockdown.py` or in `agent_kit/gating.py`)
**Scope:** Medium
1. Use `agent_kit/body.py:52` parsing so section attribution matches existing markdown behavior.
2. Scan case-insensitively for: `TBD`, `to be decided`, `to be determined`, `we'll see`, `figure out later`, `figure it out`, `tunable`, `depends on what surfaces`, `can adjust later`, `decide later`.
3. Ignore matches in `Open Questions` and fenced code blocks. The body parser already tracks fences for headings at `agent_kit/body.py:227`; add a small reusable text iterator or local scanner that also suppresses fenced-code lines.
4. Return blockers with phrase, section, and line number.

## Phase 3: Wire `edit_epic`

### Step 7: Extend the tool schema and write path (`agent_kit/tools/editorial.py`)
**Scope:** Large
1. Add optional top-level `force` to `EDIT_EPIC_SCHEMA` at `agent_kit/tools/editorial.py:26`.
2. Remove the `not_yet_supported` guard at `agent_kit/tools/editorial.py:133`.
3. Support `changes.sprints` operations such as `replace`, `upsert`, `update`, `delete`, `lock_in`, `queue`, `pend`, and `reorder`.
4. Support `changes.state.target` for state advancement, with all gating run before writes unless `force: true`.
5. Keep body, checklist, sprint, and state writes in one transaction and record separate `epic_events` as appropriate: `sprints_change`, `sprint_status_change`, `state_change`, and `forced_handoff`.
6. Return `state_transition`, `sprint_changes`, and blockers in the `edit_epic` tool result so the loop and callable clients can expose what changed without re-inferring it from raw database rows.
7. On force-through, still compute blockers, apply the transition, and log `forced_handoff` with bypassed conditions.

### Step 8: Preserve revert semantics (`agent_kit/tools/editorial.py`)
**Scope:** Medium
1. Extend `revert` handling around the existing event replay logic so `sprints_change`, `sprint_status_change`, `state_change`, and `forced_handoff` can restore prior sprint rows and prior epic state.
2. Snapshot enough prior state before each sprint/status write to make revert reliable: prior epic state, prior sprint rows, and prior sprint item rows for touched sprints.

## Phase 4: Visibility Surfaces And Replay

### Step 9: Populate invocation envelopes (`agent_kit/loop.py`, `agent_kit/envelope.py`, `agent_kit/envelope.schema.json`)
**Scope:** Medium
1. Update the completed-turn envelope path so `state_after` is reloaded from the store instead of always echoing `state_before` on success.
2. Populate existing `StateDelta.state_transition` and `StateDelta.sprint_changes` fields from `edit_epic` tool results and/or audited tool events.
3. Update `agent_kit/envelope.schema.json` if the existing schema shape is too loose or incomplete for Sprint 4 deltas.
4. Add tests showing invocation-mode callers see `shaping -> sprinting`, `sprinting -> planned`, and sprint queue/reorder deltas in the returned envelope.

### Step 10: Extend editorial read tools and replay (`agent_kit/tools/editorial_reads.py`)
**Scope:** Medium
1. Add sprints with items to the normal `get_epic` payload, alongside body, checklist, title, goal, and state.
2. Extend `get_epic_at_time` reconstruction to replay `sprints_change`, `sprint_status_change`, `state_change`, `forced_handoff`, `reverted_to`, and `created` events.
3. Use the same event prior-state snapshots created in Step 8 so historical payloads and revert semantics agree.
4. Add tests that read current sprints after lock-in and reconstruct pre/post queue state from event history.

## Phase 5: Prompt And Turn Behavior

### Step 11: Update Arnold instructions (`prompts/system.md`)
**Scope:** Small
1. Add Sprint 4 tool-use guidance near the existing Sprint Organization section at `prompts/system.md:112` and `prompts/system.md:243`.
2. Teach the two-beat flow: first propose/finalize sprints and ask for confirmation, then call `edit_epic` with `lock_in` assigning first queued and rest pending.
3. Describe blocker surfacing: list blockers from `edit_epic`, offer address/skip/force-through, and call with `force: true` only after explicit user direction.
4. Add post-handoff queue commands: queue sprint N, pend sprint N with reason, and reorder queued sprints.

### Step 12: Make end-of-turn checks phase-aware (`agent_kit/end_of_turn.py`, `agent_kit/loop.py`)
**Scope:** Medium
1. Extend `evaluate_end_of_turn` at `agent_kit/end_of_turn.py:33` to receive epic state and sprint snapshots.
2. Add findings for sprinting/planned phases: sprinting turns that make no sprint progress when sprint action was expected, planned transitions without queued/pending sprint assignment, and all-pending planned state needing an explicit user-facing note.
3. Update the loop call site to pass sprint snapshots before/after, alongside the existing body/checklist snapshots.

## Phase 6: Tests And Validation

### Step 13: Add focused unit tests (`tests/test_sprints.py`, `tests/test_gating.py`, `tests/test_lockdown.py`)
**Scope:** Medium
1. Cover gating combinations, including body under 500 chars blocking `shaping -> sprinting`.
2. Cover force-through success and `forced_handoff` event logging.
3. Cover confirmation parsing and default queue/pend assignment.
4. Cover queue reordering math and duplicate queue-position rejection.
5. Cover lockdown regex phrases, section attribution, Open Questions exemption, and fenced-code exemption.

### Step 14: Add adapter, envelope, read, and migration tests (`tests/store_contract.py`, `tests/test_supabase_adapters.py`, `tests/test_sqlite_store.py`, `tests/test_envelope.py`, `tests/test_editorial_reads.py`)
**Scope:** Medium
1. Assert sprint CRUD works through the common store contract.
2. Assert the Supabase migration text contains the `sprints`, `sprint_items`, checks, indexes, and partial unique queued-position constraint.
3. Assert SQLite rejects two queued sprints with the same `queue_position` for one epic.
4. Assert completed invocation envelopes report the actual post-turn epic state and sprint changes.
5. Assert `get_epic` includes current sprints and `get_epic_at_time` reconstructs sprint/state history.

### Step 15: Add integration tests (`tests/test_sprint_mode_lifecycle.py`)
**Scope:** Large
1. Create an epic, enrich body/checklist, advance `shaping -> sprinting`, propose/refine/finalize sprints, lock in queue/pending assignments, and advance to `planned`.
2. Verify a decision-doc-shaped epic still produces at least one sprint.
3. Verify post-handoff `queue sprint 2` and `do sprint 3 first` update positions, log `sprint_status_change`, appear in `get_epic`, and appear in the invocation envelope.
4. Verify lockdown blocks `TBD` in Key Decisions and passes when the phrase is moved to Open Questions.

## Execution Order
1. Land migrations and store methods first so tests have durable primitives.
2. Add deterministic domain modules and unit tests before touching `edit_epic` orchestration.
3. Wire `edit_epic` once validators, sprint operations, and event snapshots are tested directly.
4. Wire visibility surfaces: hot context, envelopes, reads, replay, and revert.
5. Update prompts and end-of-turn checks after server behavior exists.
6. Finish with full lifecycle integration tests and the existing suite.

## Validation Order
1. Run targeted unit tests first: `pytest tests/test_lockdown.py tests/test_gating.py tests/test_sprints.py`.
2. Run adapter/migration tests: `pytest tests/test_sqlite_store.py tests/test_supabase_adapters.py tests/test_supabase_store.py`.
3. Run visibility tests: `pytest tests/test_envelope.py tests/test_editorial_reads.py tests/test_end_of_turn.py`.
4. Run lifecycle tests: `pytest tests/test_sprint_mode_lifecycle.py tests/test_editorial_loop.py`.
5. Run the full test suite with `pytest` after targeted tests pass.

## Notes On Simplicity
Keep all enforcement local and deterministic for this sprint. The spec mentions optional second-opinion checks, but the requested scope calls out concrete server-side conditions; adding live model calls inside gating would make core state transitions harder to test and operate. The model can still suggest force-through or request second opinions through existing prompt behavior, but the server gate should remain deterministic.

The envelope and read/replay additions are not scope growth. Sprint 4 changes the canonical lifecycle state and sprint queue; existing public surfaces must report that state accurately for the feature to be complete.


        Plan metadata:
        {
  "version": 2,
  "timestamp": "2026-04-30T12:23:15Z",
  "hash": "sha256:c252df2cb06cb4d45d12c878d5ac3c0c37e4a162391d26c75dd098061119bacb",
  "changes_summary": "Addressed the critique by adding explicit phases for invocation envelope state/sprint deltas and editorial read/time-travel replay support. The revised plan keeps `edit_epic` as the root write path, but now also wires every existing observation surface needed for Sprint 4 to be visible and reconstructible.",
  "flags_addressed": [
    "FLAG-001",
    "FLAG-002"
  ],
  "questions": [
    "Should PM-handoff fidelity be implemented as a deterministic heuristic for Sprint 4, or is a live/LLM-graded gate required at runtime? The plan assumes deterministic server-side checks and LLM-graded tests only where already optional.",
    "What exact `changes.sprints` JSON shape should external callers rely on? The plan proposes simple operations (`replace`, `upsert`, `update`, `lock_in`, `queue`, `pend`, `reorder`) under the existing `edit_epic` tool.",
    "When pending reason is omitted, should the stored value be `no reason given`, nullable, or should the tool block? The spec says pending reason is encouraged but acceptance says pending has a pending_reason; the plan assumes a stored explicit default like `no reason given`.",
    "Should all-pending planned state require extra confirmation in the server tool, or just a warning in end-of-turn/user response? The plan assumes it is allowed server-side and surfaced as a phase-aware warning."
  ],
  "success_criteria": [
    {
      "criterion": "SQLite and Supabase migrations create `sprints` and `sprint_items` with status checks, timestamps, item fields, and a partial unique constraint preventing duplicate queued `queue_position` per epic.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "Store protocol plus SQLite and Supabase adapters expose sprint CRUD and sprint item replacement/listing, and common store contract tests pass for the new methods.",
      "priority": "must",
      "requires": [
        "read_files",
        "run_tests"
      ]
    },
    {
      "criterion": "`edit_epic` accepts sprint changes and state transition changes instead of returning `not_yet_supported`, while preserving existing body/checklist edit behavior and audit wrapping.",
      "priority": "must",
      "requires": [
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "Attempting `shaping -> sprinting` with a body under 500 characters fails with a structured blockers list unless `force: true` is supplied.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Force-through state advancement succeeds and records a `forced_handoff` event containing the bypassed blockers.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "Sprint shaping writes proposed sprint rows and sprint items; lock-in moves every sprint to either `queued` with queue position or `pending` with a pending reason/default.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Every lifecycle path to `planned` requires at least one sprint, including decision-doc-shaped epics.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Post-handoff queue and reorder operations update sprint status/queue positions correctly, keep the epic planned, and record `sprint_status_change` audit events.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Completed invocation envelopes reload the actual post-turn epic state and include `state_transition` plus `sprint_changes` for Sprint 4 edits.",
      "priority": "must",
      "requires": [
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "`get_epic` returns current sprints with items, and `get_epic_at_time` reconstructs sprint/status/state history from event replay.",
      "priority": "must",
      "requires": [
        "run_tests",
        "parse_diff"
      ]
    },
    {
      "criterion": "Open-decisions lockdown scan blocks listed unresolved phrases outside `Open Questions`, ignores those phrases inside `Open Questions`, and ignores fenced code blocks.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Existing editorial loop, body parser, end-of-turn, envelope, read-tool, store, and Supabase adapter tests continue to pass after Sprint 4 changes.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Prompt updates tell Arnold to use the two-beat sprint lock-in flow, surface blockers with address/skip/force options, and use `edit_epic` for sprint queue/pending/reorder operations.",
      "priority": "should",
      "requires": [
        "read_files",
        "subjective_judgment"
      ]
    },
    {
      "criterion": "Sprint/gating helpers remain small, deterministic, and directly unit-tested rather than embedding natural-language parsing in persistence adapters.",
      "priority": "should",
      "requires": [
        "parse_diff",
        "subjective_judgment"
      ]
    },
    {
      "criterion": "Manual production Supabase migration against the provided project URL is coordinated separately; no service-role secret is committed or logged.",
      "priority": "info",
      "requires": [
        "verify_physical_device"
      ]
    }
  ],
  "assumptions": [
    "Do not use the redacted Supabase service key from the brief; implementation and validation should use migrations, fake Supabase adapter tests, and local SQLite unless credentials are supplied through the normal environment.",
    "`edit_epic` remains the only sprint write tool for Sprint 4; no separate `edit_sprint` tool is introduced unless implementation evidence shows the schema becomes unmanageable.",
    "Server-side PM-handoff fidelity is deterministic for now: section/content/sprint/checklist/lockdown checks, not a live LLM call during state advancement.",
    "Natural-language understanding for phrases like `queue sprint 2` and `do sprint 3 first` is handled by the existing model loop and prompt; server code receives structured `edit_epic` arguments and enforces correctness.",
    "Pending sprints without a user-provided reason store an explicit default reason so acceptance criteria can assert `pending_reason` is populated.",
    "The existing body parser is the source of truth for section attribution; new lockdown logic should reuse or mirror its fenced-code behavior rather than creating an incompatible markdown parser.",
    "Invocation envelopes should use the existing `StateDelta.state_transition` and `StateDelta.sprint_changes` fields rather than inventing a parallel response shape.",
    "Sprint event prior-state snapshots are the canonical source for both revert and `get_epic_at_time` reconstruction."
  ],
  "delta_from_previous_percent": 15.34,
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
    "id": "FLAG-001",
    "concern": "Invocation envelope: state transitions and sprint deltas would remain invisible to callable clients. The plan wires edit_epic and end-of-turn checks, but does not update the turn envelope path; the current loop always returns state_after=state_before on successful turns, and StateDelta already has sprint_changes/state_transition fields that would stay empty.",
    "evidence": "Addressed the critique by adding explicit phases for invocation envelope state/sprint deltas and editorial read/time-travel replay support. The revised plan keeps `edit_epic` as the root write path, but now also wires every existing observation surface needed for Sprint 4 to be visible and reconstructible.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "FLAG-002",
    "concern": "History/read tools: sprint state is not included in get_epic/get_epic_at_time replay. The plan adds hot-context loading and revert support, but omits the existing editorial read surface and time-travel reconstruction, so users and tests can inspect an epic without seeing its sprints, and replay cannot reconstruct sprint/status changes.",
    "evidence": "Addressed the critique by adding explicit phases for invocation envelope state/sprint deltas and editorial read/time-travel replay support. The revised plan keeps `edit_epic` as the root write path, but now also wires every existing observation surface needed for Sprint 4 to be visible and reconstructible.",
    "status": "addressed",
    "severity": "significant"
  },
  {
    "id": "FLAG-003",
    "concern": "Lifecycle metadata: planned_at and all-pending hot-context flag are missing from the plan. The spec has an explicit Sprint 4 test for all-pending planned state requiring epics.planned_at to be set and hot context to show that nothing is queued, but the plan only says to update epic state and surface an end-of-turn warning.",
    "evidence": "planning-bot-spec.md:2627-2632 requires state planned, epics.planned_at set, a hot-context flag for all sprints pending, and an explicit user-facing note. The current epics schema already has planned_at at agent_kit/store/migrations/sqlite/001_core.sql:8-12, but the plan's state/gating steps do not mention setting it or adding the all-pending flag to load_hot_context.",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "verifiability-0",
    "concern": "Criterion 10: requires human verification (subjective_judgment).",
    "evidence": "",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "verifiability-1",
    "concern": "Criterion 11: requires human verification (subjective_judgment).",
    "evidence": "",
    "status": "open",
    "severity": "minor"
  },
  {
    "id": "verifiability-2",
    "concern": "Criterion 12: requires human verification (verify_physical_device).",
    "evidence": "",
    "status": "open",
    "severity": "minor"
  }
]

        Critique history:
        [
  {
    "iteration": 1,
    "flag_count": 6,
    "verified": []
  }
]

        Debt watch items (do not make these worse):
        [
  "[DEBT] are-the-proposed-changes-technically-correct: are the proposed changes technically correct?: storage reconciliation cannot be correct for crash-before-upload unless the ledger row stores enough replay material. step 16 says `supabase_storage` reconciliation does `blob.exists(ref)` and reissues if missing, but step 13's pending storage rows for voice/image ingestion do not store the attachment bytes, a durable local blob, or even explicitly the discord attachment url in `request_body`; without that, the reissue branch has no input. (flagged 1 times across 1 plans)",
  "[DEBT] callable-api: sprint 1a plan descopes attachment-passing despite the spec's callable api marking it as 1a acceptance. (flagged 1 times across 1 plans)",
  "[DEBT] callable-api: spec\u2019s sprint 1a readiness gate lists attachment-passing protocol; plan defers it. (flagged 1 times across 1 plans)",
  "[DEBT] callable-api: cli omits `--attach` in 1a. (flagged 1 times across 1 plans)",
  "[DEBT] callable-api: python `run_turn` omits `attachments=` in 1a. (flagged 1 times across 1 plans)",
  "[DEBT] callable-api: plan removes `--attach`, `attachments=`, `localblobstore`, and attachment tests from 1a. (flagged 1 times across 1 plans)",
  "[DEBT] data-model: body_version column from spec \u00a72606 example is deferred; sprint 2a covers title/body sync semantics via epic_events audit trail instead. (flagged 1 times across 1 plans)",
  "[DEBT] data-model: rev 3 makes body_version deferral explicit; gate-level acceptance recorded. (flagged 1 times across 1 plans)",
  "[DEBT] did-the-work-fully-address-the-issue-hints-user-notes-and-approved-plan-requirements: did the work fully address the issue hints, user notes, and approved plan requirements?: recovery coverage for ingestion-side storage uploads remains underspecified: the plan records pending storage rows before uploading, but the described `request_body` for those rows only includes deterministic paths, not the original discord attachment url or another durable byte source. if the process crashes before the upload completes, `supabase_storage` reconciliation can detect the object is missing but cannot reissue the upload deterministically from the stored row. (flagged 1 times across 1 plans)",
  "[DEBT] discord-ingestion-recovery: crash-before-storage-upload + discord attachment url expiry results in orphaned ledger rows for voice audio / user-uploaded images. the inbound messages row remains persisted so no silent data loss; the user can re-send. a future sprint may add ingestion-time bytes-to-tmpfile fallback if the orphaned rate is meaningful in production. (flagged 1 times across 1 plans)",
  "[DEBT] does-the-change-touch-all-locations-and-supporting-infrastructure: does the change touch all locations and supporting infrastructure?: supporting infrastructure for storage reissue is still incomplete: the plan adds `blob.exists`, but not a corresponding way for the reconciler to obtain the original attachment payload from the ledger row. since discord attachment urls can be transient, the missing source field is not just a local adapter detail; it affects the recovery contract across `discordtransport`, `external_requests.request_body`, and `reconciler`. (flagged 1 times across 1 plans)",
  "[DEBT] find-the-callers-of-the-changed-function-what-arguments-do-they-actually-pass-does-the-fix-handle-all-of-them: find the callers of the changed function. what arguments do they actually pass? does the fix handle all of them?: checked the planned storage reconciliation caller: `reconciler` can call `blob.exists(ref)`, but when it needs to reissue a missing upload it has no planned argument source for `blob.put(...)` because the pending request row does not carry the original attachment bytes or a durable fetchable source. that caller path remains under-specified. (flagged 1 times across 1 plans)",
  "[DEBT] history-replay: get_epic_at_time pre-creation semantics: spec \u00a71678 says 'returns initial state' for t before any events; rev 3 says 'return empty/none'. (flagged 1 times across 1 plans)",
  "[DEBT] search-for-related-code-that-handles-the-same-concept-is-the-reported-issue-a-symptom-of-something-broader: search for related code that handles the same concept. is the reported issue a symptom of something broader?: the remaining storage reissue issue applies to both voice and image attachments, not just one branch: voice storage upload needs source audio bytes to recover, and image storage upload needs source image bytes to recover. the plan should store a retrievable source reference in `request_body` or deliberately mark crash-before-download/upload as orphaned rather than promising deterministic reissue. (flagged 1 times across 1 plans)"
]

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

> AGENT

{"tasks":[{"id":"T1","description":"Add SQLite and Supabase sprint migrations for `sprints` and `sprint_items`, including status checks, timestamps, item fields, read indexes, and partial unique queued-position constraints.","depends_on":[],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T2","description":"Extend the store port plus SQLite and Supabase adapters with sprint CRUD, sprint item replacement/listing, and helper loading of sprints with items. Update hot context to include sprint snapshots and an all-sprints-pending/no-queued flag.","depends_on":["T1"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T3","description":"Implement deterministic sprint domain logic in `agent_kit/sprints.py`: payload normalization, validation, PM-task-level item checks, default lock-in assignment, queue/pend/reorder operations, gapless positions, and structured sprint-change summaries.","depends_on":["T2"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T4","description":"Implement deterministic gating and lockdown scanning: `shaping -> sprinting`, `sprinting -> planned`, PM-handoff heuristic, checklist rules, at-least-one-sprint rule, queued/pending invariants, and unresolved-decision phrase blocking outside `Open Questions` and fenced code.","depends_on":["T2","T3"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T5","description":"Wire `edit_epic` to accept top-level `force`, `changes.sprints`, and `changes.state.target`; run gates before writes unless forced; apply body/checklist/sprint/state writes transactionally; set `planned_at` when entering `planned`; record `sprints_change`, `sprint_status_change`, `state_change`, and `forced_handoff` events with blocker details and prior-state snapshots.","depends_on":["T3","T4"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T6","description":"Preserve revert semantics for Sprint 4 events by replaying stored prior epic state, prior sprint rows, and prior sprint item rows for `sprints_change`, `sprint_status_change`, `state_change`, and `forced_handoff`.","depends_on":["T5"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T7","description":"Update editorial read and time-travel tools so `get_epic` returns current sprints with items and `get_epic_at_time` reconstructs sprint/status/state history from event replay, matching the same snapshots used by revert.","depends_on":["T5","T6"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T8","description":"Update invocation envelope generation so completed turns reload actual post-turn state, populate `StateDelta.state_transition` and `StateDelta.sprint_changes`, and adjust `agent_kit/envelope.schema.json` only if the existing schema is insufficient.","depends_on":["T5"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T9","description":"Update Arnold prompts and phase-aware end-of-turn checks for the two-beat sprint lock-in flow, blocker surfacing with address/skip/force options, post-handoff queue/pend/reorder commands, sprinting/planned progress findings, and all-pending planned-state user-facing notes.","depends_on":["T2","T5","T8"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T10","description":"Add focused unit, adapter, migration, envelope, read/replay, end-of-turn, and lifecycle tests for Sprint 4 behavior: gating, lockdown, force-through event logging, sprint CRUD, duplicate queued-position rejection, lock-in, decision-doc lifecycle, queue/reorder, read surfaces, and invocation deltas.","depends_on":["T1","T2","T3","T4","T5","T6","T7","T8","T9"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null},{"id":"T11","description":"Run validation and fix failures until green. Use targeted commands first: `pytest tests/test_lockdown.py tests/test_gating.py tests/test_sprints.py`, adapter/migration tests, visibility tests, lifecycle/editorial-loop tests, then full `pytest`. Also write a short throwaway script that reproduces the specific Sprint 4 lifecycle/gating behavior, run it to confirm the implementation, then delete it. Do not create additional test files in this final validation task.","depends_on":["T10"],"status":"pending","executor_notes":"","files_changed":[],"commands_run":[],"auto_attributed_files":null,"evidence_files":[],"reviewer_verdict":"","stance":null,"stop_signal":null}],"watch_items":["Do not invoke the `megaplan` CLI, read the `megaplan` skill, or start nested planning. Treat megaplan references as context only.","Do not commit, log, or request the redacted Supabase service key. Use local SQLite, migration text checks, and fake Supabase adapter tests unless credentials are provided through normal environment channels.","FLAG-003 remains open: entering `planned` must set `epics.planned_at`, and hot context must expose the all-sprints-pending/no-queued condition so the user can be warned.","Keep enforcement deterministic and server-side. Do not add live LLM calls to gating unless the user explicitly changes the requirement.","`edit_epic` is the single Sprint 4 write surface. Avoid adding a separate sprint write tool unless implementation evidence proves the schema is unmanageable.","Pending sprints need a populated `pending_reason`; if omitted, store an explicit default such as `no reason given` so acceptance checks are stable.","Use the existing markdown body parser behavior for section attribution and fenced-code handling; avoid introducing an incompatible parser for lockdown scanning.","Sprint event snapshots are the canonical source for both revert and `get_epic_at_time`; do not let those paths drift.","Invocation callers must see real `state_after`, `state_transition`, and `sprint_changes`; do not leave envelopes echoing `state_before` after successful writes.","Natural language commands like `queue sprint 2` are prompt/model behavior; server code should receive structured `edit_epic` arguments and enforce correctness.","Debt watch items about unrelated attachment/storage recovery are out of scope; avoid touching those areas unless required by tests.","Queue positions for queued sprints must be unique per epic and should be normalized gaplessly after reorder operations."],"sense_checks":[{"id":"SC1","task_id":"T1","question":"Do both migration sets create `sprints` and `sprint_items` with matching checks, indexes, timestamps, and a partial unique index on `(epic_id, queue_position)` where status is `queued`?","executor_note":"","verdict":""},{"id":"SC2","task_id":"T2","question":"Can the common store interface create, load, list, update, delete, and item-replace sprints consistently across SQLite and Supabase adapters, and does hot context include sprint/items plus the all-pending/no-queued flag?","executor_note":"","verdict":""},{"id":"SC3","task_id":"T3","question":"Do sprint operations reject invalid payloads, assign lock-in defaults correctly, require pending reasons/defaults, maintain gapless queued positions, and return structured change summaries?","executor_note":"","verdict":""},{"id":"SC4","task_id":"T4","question":"Do gates block underspecified `shaping -> sprinting`, enforce all `sprinting -> planned` invariants, require at least one sprint, and report lockdown phrase blockers with section and line number while exempting `Open Questions` and fenced code?","executor_note":"","verdict":""},{"id":"SC5","task_id":"T5","question":"Does `edit_epic` remove the old unsupported guard, apply sprint/state writes atomically, set `planned_at`, return blockers and sprint/state deltas, and log `forced_handoff` with bypassed blockers when forced?","executor_note":"","verdict":""},{"id":"SC6","task_id":"T6","question":"Can revert restore prior epic state, sprint rows, and sprint items for every new Sprint 4 event type without corrupting existing body/checklist revert behavior?","executor_note":"","verdict":""},{"id":"SC7","task_id":"T7","question":"Do `get_epic` and `get_epic_at_time` expose current and historical sprint state accurately before and after lock-in, queue, pend, reorder, force, and revert events?","executor_note":"","verdict":""},{"id":"SC8","task_id":"T8","question":"Do completed invocation envelopes reload real post-turn state and include `state_transition` plus `sprint_changes` for state advancement, lock-in, queue, and reorder operations?","executor_note":"","verdict":""},{"id":"SC9","task_id":"T9","question":"Do prompts and end-of-turn checks guide the two-beat flow, blocker options, queue/pend/reorder behavior, and all-pending planned-state warning without relying on unsupported tool shapes?","executor_note":"","verdict":""},{"id":"SC10","task_id":"T10","question":"Do the added tests cover all acceptance criteria and the open critique item, while keeping helper tests deterministic and independent of production Supabase credentials?","executor_note":"","verdict":""},{"id":"SC11","task_id":"T11","question":"Do targeted tests, lifecycle/editorial-loop tests, the full suite, and the temporary reproduction script all pass after any necessary fixes, with the throwaway script deleted afterward?","executor_note":"","verdict":""}],"user_actions":[{"id":"U1","description":"Apply the Supabase migration to the real Supabase project and verify it in the production/staging database using secure credentials outside the repo.","phase":"after_execute","blocks_task_ids":null,"rationale":"Repo work can create and test migration SQL, but applying it to the hosted Supabase project requires human-controlled credentials and deployment authority.","requires_human_only_reason":"Manual production Supabase migration against the provided project URL is operational work outside the executor's repo-editing permissions."}],"meta_commentary":"Execute in dependency order: durable schema and store primitives first, deterministic sprint/gating logic second, `edit_epic` orchestration third, then visibility surfaces, prompts/end-of-turn behavior, and tests. The main implementation trap is treating Sprint 4 as only a database write: envelopes, hot context, read tools, replay, revert, and `planned_at` must all reflect the new sprint lifecycle. Keep the tool input structured and deterministic; natural-language interpretation belongs in the model loop and prompt guidance, not persistence adapters or gates.","validation":{"plan_steps_covered":[{"plan_step_summary":"Step 1: add sprint migrations","finalize_item_ids":["T1"]},{"plan_step_summary":"Step 2: extend store protocol","finalize_item_ids":["T2"]},{"plan_step_summary":"Step 3: implement SQLite and Supabase sprint adapters plus hot context","finalize_item_ids":["T2"]},{"plan_step_summary":"Step 4: add sprint domain module","finalize_item_ids":["T3"]},{"plan_step_summary":"Step 5: add gate evaluators","finalize_item_ids":["T4"]},{"plan_step_summary":"Step 6: implement lockdown scanning","finalize_item_ids":["T4"]},{"plan_step_summary":"Step 7: extend `edit_epic` schema and write path","finalize_item_ids":["T5"]},{"plan_step_summary":"Step 8: preserve revert semantics","finalize_item_ids":["T6"]},{"plan_step_summary":"Step 9: populate invocation envelopes","finalize_item_ids":["T8"]},{"plan_step_summary":"Step 10: extend editorial read tools and replay","finalize_item_ids":["T7"]},{"plan_step_summary":"Step 11: update Arnold instructions","finalize_item_ids":["T9"]},{"plan_step_summary":"Step 12: make end-of-turn checks phase-aware","finalize_item_ids":["T9"]},{"plan_step_summary":"Step 13: add focused unit tests","finalize_item_ids":["T10","T11"]},{"plan_step_summary":"Step 14: add adapter, envelope, read, and migration tests","finalize_item_ids":["T10","T11"]},{"plan_step_summary":"Step 15: add integration lifecycle tests","finalize_item_ids":["T10","T11"]},{"plan_step_summary":"Execution order and validation order","finalize_item_ids":["T1","T2","T3","T4","T5","T6","T7","T8","T9","T10","T11"]},{"plan_step_summary":"Manual hosted Supabase migration coordination","finalize_item_ids":["U1"]}],"orphan_tasks":[],"completeness_notes":"All approved plan steps are mapped. FLAG-003 is folded into T2, T5, T9, and T10 through hot-context all-pending visibility, `planned_at` handling, user-facing warning behavior, and tests. Production Supabase migration application is intentionally a human after-execute action; migration authoring and validation remain repo tasks.","coverage_complete":true},"baseline_test_failures":null,"baseline_test_command":null,"baseline_test_note":"No baseline tests were run while preparing this execution briefing."}
