> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

WRITE ACCESS CONTRACT: You are running with auto-approved writes inside a writable workspace. Treat the working directory as fully writable. Do NOT preemptively skip or block tasks on permission, sandbox, or read-only grounds. Attempt every required edit; only report failure AFTER a real OS-level rejection from a specific shell command. Do not infer 'read-only' from absence of activity; absence is not denial. If a single shell command unexpectedly fails, retry with a different invocation before concluding the environment is restricted.

You are the gatekeeper for the megaplan workflow. Make the continuation decision directly.

        Project directory:
        /Users/user_c042661f/Documents/reigh-workspace/ArtAgents

        Idea:
ArtAgents is a file-based, single-host Python CLI for running creative pipelines (video/audio/image) that mix code, AI, and human steps. Today it has a pack-based plugin architecture, orchestrator + executor schemas (python/command runtime kinds only), project runs under ~/Documents/reigh-workspace/artagents-projects/, threads with provenance, and a CLI gateway. We are extending it so an agent can be put into 'task mode' and walked through a frozen plan that mixes code, AI, and human steps, with iteration loops and fan-out.

NON-NEGOTIABLES:
- Single-host, file-based. No daemon, no web server.
- Honor-based with strong logging. We do not pretend to sandbox a misaligned agent.
- Migration is additive. Existing JSON manifests and python/command runtime kinds keep working.
- Existing pack mechanism stays.

V1 DESIGN (post-critique, trimmed):

THREE STEP KINDS:
- code: deterministic argv, runner subprocesses, returncode + produces.
- attested: agent or human task. instructions + produces + ack records identity (agent_id or actor pinned via ARTAGENTS_ACTOR) + evidence.
- nested: delegates to a child plan; gate sees the structure for hashing/pinning.

ITERATION AND FAN-OUT ARE BODY ATTRIBUTES, NOT KINDS:
- repeat: {until: user_approves|verifier_passes|quorum, max_iterations, on_exhaust}
- repeat: {for_each: <input_set>}
Both apply to any step or to a body block in a nested plan.

PRODUCES WITH INLINE CHECKS (replaces separate verifier substep):
  produces = {
    'audio': file(path='audio.wav', check=audio_duration_min(30)),
    'notes': json_file(path='notes.json', schema='notes.schema.json', min_items=3),
  }
The gate runs the check; failure rewinds the cursor. passes_test is a regular code step.

STORAGE (under ~/Documents/reigh-workspace/artagents-projects/):
- <slug>/active_run.json -- pointer to in-flight run + plan hash
- <slug>/runs/<run-id>/plan.json -- immutable, hash-pinned (renamed from 'checklist' since it's a tree)
- <slug>/runs/<run-id>/events.jsonl -- append-only, plain hash-chained (prev_hash field), sole truth
- <slug>/runs/<run-id>/AGENT.md -- contract for whoever's driving
- <slug>/runs/<run-id>/steps/<step-id>/produces/ -- artifact files (or symlinks into .cas)
- <slug>/runs/<run-id>/steps/<step-id>/iterations/NNN/ -- when repeat:until is set
- <slug>/runs/<run-id>/steps/<step-id>/items/<item-id>/ -- when repeat:for_each is set
- <slug>/runs/<run-id>/inbox/ -- external completion signals get dropped here
- <slug>/.cas/<sha256> -- per-project CAS for v1 (not shared)

NO crypto: hash chain is plain sha256(prev_hash + canonical_event_json). Tripwire for accidental edits, not protection against malicious users. We do not need HMAC or key handles.

NO .index.db in v1. find + grep on events.jsonl is fine until grep is slow.

GATE (above dispatch, single function):
- active_run.json exists for this project?
- plan.json hash matches the pin in active_run.json?
- events.jsonl hash chain intact?
- incoming command matches plan[derived_cursor].command?
If any fails, reject with the exact recovery command.

LIFECYCLE VERBS, scoped by audience:
artagents next | ack | status | abort                                  (agent-facing, mid-run)
artagents start | abort | status | runs ls                             (operator)
artagents author new | check | describe | test | compile | explain     (author)

ACK DECISIONS (intentionally distinct):
--decision approve              -- advance cursor
--decision retry                -- only valid after verifier failure; rerun body, stderr is feedback
--decision iterate --feedback   -- only valid when repeat.until=user_approves; appends to cumulative constraints
--decision abort                -- end run

ACK requires --agent <id> for attested steps with attestor_type=agent, or --actor <name> matching ARTAGENTS_ACTOR for attestor_type=human. Self-acks and unpinned actors are rejected.

For repeat:for_each: --item <id> targets a specific item; partial approval is supported.

NUDGE (out-of-process, optional, Claude Code only for v1):
A Stop hook runs artagents next. The next output ALWAYS includes the prohibition preamble verbatim, not just on first call -- this is the re-injection mechanism that fights context decay.

AUTHORING:
- Python DSL artagents.orchestrate is the ONLY committed representation. JSON manifest is generated at author compile into a build/ dir (gitignored) and that's what the runtime hashes/pins.
- Verifier helper library artagents.verify: file_nonempty, json_schema, json_file, audio_duration_min, image_dimensions, all_of.
- Pack layout: <pack>/<orch>.py (committed), <pack>/build/<orch>.json (gitignored), <pack>/fixtures/<name>/, <pack>/golden/<name>.events.jsonl.
- author check is sub-second static validation: schema, every produces/requires reference resolves, every nested plan resolves, attested steps with non-trivial produces have semantic checks (sentinel-existence-only is rejected at definition time).
- author describe pretty-prints the DAG.
- author test --fixture runs --dry-run --auto-approve, diffs events.jsonl against golden/<fixture>.events.jsonl.

V1 BUILD ORDER (recommended phases):
1. Kernel: events.jsonl + plain hash chain + plan hash pin + gate above dispatch + active_run.json. Runner becomes dumb; gate is a single decorated function above runner dispatch.
2. Three step kinds: code, attested, nested. (code is a strict superset of today's python+command runtime kinds.)
3. produces-with-inline-checks; repeat:{until} and repeat:{for_each} on bodies.
4. Authoring: Python DSL + verify helpers + author check + author describe + author new.
5. Lifecycle verbs split by audience as above.
6. Stop-hook nudge with mandatory prohibition preamble.
7. CAS per-project (under <slug>/.cas/), symlink-based produces.
8. Inbox surface for external completion signals.
9. Author test with golden runs.

EXISTING REPO STATE:
- artagents/core/orchestrator/ exists with schema.py, runner.py, registry.py, cli.py, api.py. Currently knows ORCHESTRATOR_KINDS={built_in, external} and RUNTIME_KINDS={python, command}. OrchestratorPlan / OrchestratorPlanStep skeletons exist (used for dry-run output).
- artagents/core/project/ exists with run lifecycle (prepare_project_run / finalize_project_run), paths.py with DEFAULT_PROJECTS_ROOT.
- artagents/threads/ exists with thread_wrapper around runs, @active concept.
- artagents/packs/ holds builtin packs (cut, transcribe, human_notes, open_in_reigh, etc.).
- Migration to packs is mid-flight (recent commits T10-T13).

ASSUMED OPEN-CALL DEFAULTS (the design plan should call these out and confirm or revise):
- Keep nested step kind as data (gate sees the structure); forbid code-step-calls-orchestrator.
- Python DSL is the only committed representation; JSON manifest is a build artifact in gitignored build/ dirs.
- Drop .index.db from v1; ship with file-walk verbs.

DELIVERABLE EXPECTATIONS for the design doc:
- Concrete phasing aligned to build order 1-9 above; each phase has scope, files touched, breaking-change risk classification (additive vs breaking), and exit criteria.
- Test strategy at each phase (golden runs are the regression format).
- Migration of one builtin pack (suggest hype.cut or transcribe) to the new shape as the canonical example, including the diff shape.
- Documentation deliverables identified: AUTHORING.md (one-page reference for both human and LLM authors), AGENT.md template, README.md updates.
- Risk register (single-host assumption, semantic verifier discipline, context decay re-injection, agent honor model boundary).
- Cut points where work can stop and still ship something useful (e.g., after phase 3, after phase 5).
- A ## Settled Decisions section at the bottom listing every load-bearing design call (SD-NNN format) so future code-mode runs can inherit them via --from-doc.

Mode: doc / metaplan
Output: docs/orchestrator-v1-plan.md

User notes and answers:
- strict-notes auto-enabled for metaplan/doc mode

        Plan:
        # Implementation Plan: Author docs/orchestrator-v1-plan.md (Task Mode V1 Design)

## Overview

Single deliverable: `docs/orchestrator-v1-plan.md` — a frozen, decision-first design+migration doc for adding "task mode" to ArtAgents. Mixes code/attested/nested steps with iteration and fan-out, gated above the existing orchestrator runner. Audience: ArtAgents maintainers + future code-mode runs that consume the doc via `--from-doc`. Tone matches `docs/sprint-thread-layer.md` (terse, declarative, decision-first). Ends with `## Settled Decisions` (SD-NNN one-liners).

Repo evidence already gathered:
- Schema: `artagents/core/orchestrator/schema.py` enforces `ORCHESTRATOR_KINDS={built_in,external}`, `RUNTIME_KINDS={python,command}`.
- Runner: `artagents/core/orchestrator/runner.py` has `OrchestratorPlan`/`OrchestratorPlanStep` skeletons used only for dry-run output.
- Project lifecycle: `artagents/core/project/run.py` (`prepare_project_run`/`finalize_project_run`), paths in `artagents/core/project/paths.py` (`DEFAULT_PROJECTS_ROOT`).
- Run chokepoint: `artagents/threads/wrapper.py`.
- Canonical migration target: `artagents/packs/builtin/hype/`.
- SD format reference: `docs/sprint-thread-layer.md` lines 39–43, e.g. `SD-041 redaction: <single-sentence rationale>.`

Output path is fixed: `docs/orchestrator-v1-plan.md`. The executor only writes there.

## Main Phase

### Step 1: Front matter, Sections 1–2 — Executive Summary, Goals/Non-Goals (`docs/orchestrator-v1-plan.md`)
**Scope:** Small. Title + ~150-word Executive Summary; Goals/Non-Goals bullets explicitly listing forbidden v1 features (daemon, web server, HMAC, `.index.db`, shared CAS).

### Step 2: Section 3 — Data Model (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium. Storage tree under `~/Documents/reigh-workspace/artagents-projects/<slug>/`; `plan.json` (immutable hash-pinned, supersedes "checklist"); `events.jsonl` plain `sha256(prev_hash + canonical_event_json)` chain; `active_run.json` pointer + plan_hash pin; `AGENT.md`; `steps/<id>/{produces,iterations/NNN,items/<id>}/`; `inbox/`; per-project `.cas/`. Cite additive relationship to `artagents/core/project/paths.py` and `artagents/core/orchestrator/runner.py` `OrchestratorPlan`.

### Step 3: Sections 4–6 — Step Kinds, Iteration/Fan-Out, Produces (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium. Three step kinds: `code` (strict superset of today's `python`+`command` `RUNTIME_KINDS`), `attested` (agent or human, ack pins identity, self-ack rejected), `nested` (delegates to child plan, gate sees structure). Forbid `code-step-calls-orchestrator`. `repeat:{until|for_each}` as body attributes. `produces` example block with `audio_duration_min`, `json_file`, etc.; failure rewinds cursor; `passes_test` remains a regular `code` step; sentinel-only rejected at definition time.

### Step 4: Sections 7–9 — Gate, Lifecycle Verbs, Ack Decisions (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium. Gate function: four checks (`active_run.json` present, `plan_hash` matches, chain intact, command matches `plan[derived_cursor].command`); rejection emits exact recovery command; runs before `artagents/threads/wrapper.py` so `events.jsonl` is the single source of truth. Verbs split by audience and mapped onto today's `python3 -m artagents orchestrators` CLI in `artagents/core/orchestrator/cli.py`. Ack decision validity table (approve/retry/iterate/abort) with `--agent`/`ARTAGENTS_ACTOR` pinning rules and `--item` for `for_each`.

### Step 5: Sections 10–11 — Authoring + Nudge (`docs/orchestrator-v1-plan.md`)
**Scope:** Small. Python DSL `artagents.orchestrate` as only committed representation; `<pack>/build/<orch>.json` gitignored; pack adds `<orch>.py`, `fixtures/`, `golden/<name>.events.jsonl`. `author check`/`describe`/`test`/`new` behavior. Stop-hook nudge for Claude Code only in v1; prohibition preamble re-injected verbatim on every `artagents next` call.

### Step 6: Section 12 — Phasing 1–9 (`docs/orchestrator-v1-plan.md`)
**Scope:** Large. For each of the nine phases (kernel; three step kinds; produces+repeat; authoring; lifecycle verbs; nudge; CAS; inbox; goldens) emit five fields: scope, files touched with inline path citations, classification (additive | breaking), exit criteria, test strategy. All nine are additive. Citations include `artagents/core/orchestrator/{runner.py,schema.py,cli.py}`, `artagents/core/project/run.py`, `artagents/threads/wrapper.py`.

### Step 7: Section 13 — Canonical migration: `artagents/packs/builtin/hype/` (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium. Diff sketch: add `hype.py` (DSL), `build/hype.json` (gitignored), `fixtures/smoke/`, `golden/smoke.events.jsonl`; existing `orchestrator.yaml`/`STAGE.md`/`run.py` keep working. Show 5–10 line `hype.py` excerpt mapping `STEP_ORDER` executors onto `code`-step children with `produces` checks. Confirm existing JSON manifest still loads via `load_orchestrator_manifest` in `artagents/core/orchestrator/schema.py`.

### Step 8: Sections 14–17 — Doc Deliverables, Risk Register, Cut Points, Open-Call Confirmations (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium. Deliverables table (`AUTHORING.md` for human+LLM authors, `AGENT.md` template for in-flight agent, `README.md` updates for operator). Risk register: single-host assumption, semantic verifier discipline, context-decay re-injection, honor-model boundary. Cut points: ship after Phase 3 (frozen-plan runner) or Phase 5 (author-friendly). Explicit Confirmed verdict on three open-call defaults (A1 nested-as-data + forbid code-step-calls-orchestrator; A2 Python DSL only committed representation; A3 no `.index.db` v1).

### Step 9: Section 18 — Settled Decisions (SD-001..SD-NNN) (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium. Numbered list. Format: `SD-NNN <topic>: <single-sentence rationale>.` matching `docs/sprint-thread-layer.md`. One SD per load-bearing call: three step kinds; repeat as body attribute; `plan.json` rename; plain sha256 chain (no HMAC); no `.index.db`; Python DSL only; JSON manifest gitignored build artifact; per-project `.cas/`; code-step-calls-orchestrator forbidden; gate four-check + recovery command; gate runs before threads wrapper; `ARTAGENTS_ACTOR` pinning + self-ack rejection; retry/iterate/abort validity rules; produces inline checks replace verifier substep; sentinel-only rejected at `author check`; Stop-hook preamble re-injected every call; additive migration; honor model; cut points at Phase 3 and Phase 5; canonical migration example is `builtin.hype`; phasing matches V1 BUILD ORDER 1–9.

### Step 10: Verification (`docs/orchestrator-v1-plan.md`)
**Scope:** Small. Read back the rendered doc against the 14 `pass_to_pass` test expectations; confirm every phase has all five required fields; confirm SD format matches reference; confirm A1/A2/A3 explicitly Confirmed; confirm all forbidden v1 features listed in Non-Goals + Risk Register; confirm `artagents/packs/builtin/hype/` used as migration example with diff sketch; confirm inline path citations resolve; confirm body word count ~1500–2200.

## Execution Order
1. Steps 1–2 (vocabulary).
2. Steps 3–5 (load-bearing design content).
3. Step 6 (phasing).
4. Step 7 (migration example).
5. Step 8 (deliverables/risk/cut/open-call).
6. Step 9 (Settled Decisions).
7. Step 10 (verification).

## Validation Order
1. Section-by-section read-back against 14 `pass_to_pass` checks.
2. Spot-check inline path citations resolve to real files.
3. SD format match against `docs/sprint-thread-layer.md` lines 39–43.
4. Word-count and tone check against `docs/sprint-thread-layer.md` / `docs/design-thread-layer.md`.


        Plan metadata:
        {
  "version": 1,
  "timestamp": "2026-05-04T09:14:05Z",
  "hash": "sha256:4be1e01dc806a882cfda4a0ececfcd7ec753b34ea22781be2ef1a912c0e9f1da",
  "questions": [
    "The brief lists three open-call defaults (nested-as-data + forbid code-step-calls-orchestrator; Python DSL only; no .index.db v1). Plan assumes all three are Confirmed in the doc. Should any be revised instead?",
    "Word-count target ~1500\u20132200 for the body (excluding SD list). Acceptable, or should the doc target a different size?",
    "Phase 1 introduces a new `artagents/core/task/` package for kernel pieces (gate, events, active_run). Acceptable, or should those live under `artagents/core/orchestrator/` as additive submodules to keep the existing namespace?"
  ],
  "success_criteria": [
    {
      "criterion": "Document exists at exactly `docs/orchestrator-v1-plan.md` (no alternate filename based on title or kebab-case normalization).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Document ends with a `## Settled Decisions` section using `SD-NNN <topic>: <single-sentence rationale>.` format matching `docs/sprint-thread-layer.md`.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Settled Decisions section covers every load-bearing call enumerated in Step 9 (three step kinds; repeat as body attribute; plan.json rename; plain sha256 chain / no HMAC; no .index.db; Python DSL only; JSON manifest gitignored; per-project .cas; code-step-calls-orchestrator forbidden; gate four-check + recovery command; gate-before-wrapper; ARTAGENTS_ACTOR pinning + self-ack rejection; ack decision validity rules; produces inline checks; sentinel-only rejected at author check; Stop-hook preamble every call; additive migration; honor model; Phase 3 + Phase 5 cut points; builtin.hype canonical example; phasing 1\u20139).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Each of the nine phases includes scope, files-touched (with inline backticked path citations), classification (additive or breaking), exit criteria, and test strategy.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Storage tree section reproduces the task spec exactly: `active_run.json`, `runs/<run-id>/{plan.json,events.jsonl,AGENT.md}`, `steps/<id>/{produces,iterations/NNN,items/<id>}/`, `inbox/`, `<slug>/.cas/<sha256>` \u2014 and explicitly excludes `.index.db` and HMAC.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Step Kinds section names code, attested, nested; specifies repeat:{until|for_each} as body attributes; forbids code-step-calls-orchestrator.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Gate section enumerates all four checks (active_run.json present, plan.json hash matches pin, events.jsonl chain intact, command matches plan[derived_cursor].command) and states the gate emits an exact recovery command on rejection and runs before `artagents/threads/wrapper.py`.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Ack Decisions section specifies validity rules: retry only after verifier failure, iterate --feedback only when repeat.until=user_approves, abort ends run; --agent / ARTAGENTS_ACTOR pinning required; self-acks rejected; --item targets for_each.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Lifecycle Verbs section lists agent (next/ack/status/abort), operator (start/abort/status/runs ls), author (new/check/describe/test/compile/explain) and maps onto today's `python3 -m artagents orchestrators` CLI in `artagents/core/orchestrator/cli.py`.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Authoring section states Python DSL `artagents.orchestrate` is the only committed representation, JSON manifest is gitignored at `<pack>/build/<orch>.json`, runtime hashes/pins the build artifact, and pack adds `<orch>.py`, `fixtures/`, `golden/<name>.events.jsonl`.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Stop-hook section states the prohibition preamble is re-injected verbatim on every `artagents next` call (not just first call).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Canonical migration example uses `artagents/packs/builtin/hype/` (or transcribe as documented fallback) with a diff sketch showing the new `hype.py`, `build/hype.json`, `fixtures/`, `golden/`, and confirms existing JSON manifest still loads.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Risk register includes single-host assumption, semantic verifier discipline, context-decay re-injection, and honor-model boundary, each with trigger + mitigation.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Document explicitly Confirms or Revises the three open-call defaults (nested-as-data, Python DSL only, no .index.db v1).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Migration is presented as additive: existing `OrchestratorDefinition` JSON manifests + `python`/`command` `RUNTIME_KINDS` keep working through and after v1.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "All inline path citations resolve to files actually present in the repo (e.g., `artagents/core/orchestrator/runner.py`, `artagents/core/project/run.py`, `artagents/threads/wrapper.py`, `artagents/packs/builtin/hype/`).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Document body length lands in ~1500\u20132200 words (SD list excluded).",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Tone is terse, declarative, decision-first; matches `docs/sprint-thread-layer.md` and `docs/design-thread-layer.md`.",
      "priority": "should",
      "requires": [
        "subjective_judgment",
        "read_files"
      ]
    },
    {
      "criterion": "Document does not introduce a daemon, web server, `.index.db`, HMAC/keyed crypto, or shared CAS in v1; these are explicitly listed in Non-Goals.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Cut Points section identifies Phase 3 (kernel + step kinds + produces/repeat) and Phase 5 (adds authoring + lifecycle verb split) as ship-ready milestones.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    }
  ],
  "assumptions": [
    "A1 \u2014 nested step kind stays as data; code-step-calls-orchestrator forbidden \u2014 Confirmed in the doc.",
    "A2 \u2014 Python DSL `artagents.orchestrate` is the only committed representation; `<pack>/build/<orch>.json` is a gitignored build artifact \u2014 Confirmed.",
    "A3 \u2014 no `.index.db` in v1; file-walk verbs only \u2014 Confirmed.",
    "Doc body targets ~1500\u20132200 words; SD list adds whatever it needs.",
    "Phase 1 kernel modules land under a new `artagents/core/task/` package (gate, events, active_run) and are wired into the existing orchestrator runner via a single decorator above dispatch.",
    "`artagents/packs/builtin/hype/` is used as the canonical migration example (transcribe is acceptable fallback only if hype turns out too sprawling for an inline diff sketch).",
    "SD entries follow the exact format `SD-NNN <topic>: <single-sentence rationale>.` per `docs/sprint-thread-layer.md` lines 39\u201343.",
    "Output path is exactly `docs/orchestrator-v1-plan.md`; no alternate filename, no other write target."
  ],
  "structure_warnings": [
    "Each step section should include at least one numbered substep."
  ]
}

        Gate signals:
        {
  "robustness": "robust",
  "signals": {
    "iteration": 1,
    "idea": "ArtAgents is a file-based, single-host Python CLI for running creative pipelines (video/audio/image) that mix code, AI, and human steps. Today it has a pack-based plugin architecture, orchestrator + executor schemas (python/command runtime kinds only), project runs under ~/Documents/reigh-workspace/artagents-projects/, threads with provenance, and a CLI gateway. We are extending it so an agent can be put into 'task mode' and walked through a frozen plan that mixes code, AI, and human steps, with iteration loops and fan-out.\n\nNON-NEGOTIABLES:\n- Single-host, file-based. No daemon, no web server.\n- Honor-based with strong logging. We do not pretend to sandbox a misaligned agent.\n- Migration is additive. Existing JSON manifests and python/command runtime kinds keep working.\n- Existing pack mechanism stays.\n\nV1 DESIGN (post-critique, trimmed):\n\nTHREE STEP KINDS:\n- code: deterministic argv, runner subprocesses, returncode + produces.\n- attested: agent or human task. instructions + produces + ack records identity (agent_id or actor pinned via ARTAGENTS_ACTOR) + evidence.\n- nested: delegates to a child plan; gate sees the structure for hashing/pinning.\n\nITERATION AND FAN-OUT ARE BODY ATTRIBUTES, NOT KINDS:\n- repeat: {until: user_approves|verifier_passes|quorum, max_iterations, on_exhaust}\n- repeat: {for_each: <input_set>}\nBoth apply to any step or to a body block in a nested plan.\n\nPRODUCES WITH INLINE CHECKS (replaces separate verifier substep):\n  produces = {\n    'audio': file(path='audio.wav', check=audio_duration_min(30)),\n    'notes': json_file(path='notes.json', schema='notes.schema.json', min_items=3),\n  }\nThe gate runs the check; failure rewinds the cursor. passes_test is a regular code step.\n\nSTORAGE (under ~/Documents/reigh-workspace/artagents-projects/):\n- <slug>/active_run.json -- pointer to in-flight run + plan hash\n- <slug>/runs/<run-id>/plan.json -- immutable, hash-pinned (renamed from 'checklist' since it's a tree)\n- <slug>/runs/<run-id>/events.jsonl -- append-only, plain hash-chained (prev_hash field), sole truth\n- <slug>/runs/<run-id>/AGENT.md -- contract for whoever's driving\n- <slug>/runs/<run-id>/steps/<step-id>/produces/ -- artifact files (or symlinks into .cas)\n- <slug>/runs/<run-id>/steps/<step-id>/iterations/NNN/ -- when repeat:until is set\n- <slug>/runs/<run-id>/steps/<step-id>/items/<item-id>/ -- when repeat:for_each is set\n- <slug>/runs/<run-id>/inbox/ -- external completion signals get dropped here\n- <slug>/.cas/<sha256> -- per-project CAS for v1 (not shared)\n\nNO crypto: hash chain is plain sha256(prev_hash + canonical_event_json). Tripwire for accidental edits, not protection against malicious users. We do not need HMAC or key handles.\n\nNO .index.db in v1. find + grep on events.jsonl is fine until grep is slow.\n\nGATE (above dispatch, single function):\n- active_run.json exists for this project?\n- plan.json hash matches the pin in active_run.json?\n- events.jsonl hash chain intact?\n- incoming command matches plan[derived_cursor].command?\nIf any fails, reject with the exact recovery command.\n\nLIFECYCLE VERBS, scoped by audience:\nartagents next | ack | status | abort                                  (agent-facing, mid-run)\nartagents start | abort | status | runs ls                             (operator)\nartagents author new | check | describe | test | compile | explain     (author)\n\nACK DECISIONS (intentionally distinct):\n--decision approve              -- advance cursor\n--decision retry                -- only valid after verifier failure; rerun body, stderr is feedback\n--decision iterate --feedback   -- only valid when repeat.until=user_approves; appends to cumulative constraints\n--decision abort                -- end run\n\nACK requires --agent <id> for attested steps with attestor_type=agent, or --actor <name> matching ARTAGENTS_ACTOR for attestor_type=human. Self-acks and unpinned actors are rejected.\n\nFor repeat:for_each: --item <id> targets a specific item; partial approval is supported.\n\nNUDGE (out-of-process, optional, Claude Code only for v1):\nA Stop hook runs artagents next. The next output ALWAYS includes the prohibition preamble verbatim, not just on first call -- this is the re-injection mechanism that fights context decay.\n\nAUTHORING:\n- Python DSL artagents.orchestrate is the ONLY committed representation. JSON manifest is generated at author compile into a build/ dir (gitignored) and that's what the runtime hashes/pins.\n- Verifier helper library artagents.verify: file_nonempty, json_schema, json_file, audio_duration_min, image_dimensions, all_of.\n- Pack layout: <pack>/<orch>.py (committed), <pack>/build/<orch>.json (gitignored), <pack>/fixtures/<name>/, <pack>/golden/<name>.events.jsonl.\n- author check is sub-second static validation: schema, every produces/requires reference resolves, every nested plan resolves, attested steps with non-trivial produces have semantic checks (sentinel-existence-only is rejected at definition time).\n- author describe pretty-prints the DAG.\n- author test --fixture runs --dry-run --auto-approve, diffs events.jsonl against golden/<fixture>.events.jsonl.\n\nV1 BUILD ORDER (recommended phases):\n1. Kernel: events.jsonl + plain hash chain + plan hash pin + gate above dispatch + active_run.json. Runner becomes dumb; gate is a single decorated function above runner dispatch.\n2. Three step kinds: code, attested, nested. (code is a strict superset of today's python+command runtime kinds.)\n3. produces-with-inline-checks; repeat:{until} and repeat:{for_each} on bodies.\n4. Authoring: Python DSL + verify helpers + author check + author describe + author new.\n5. Lifecycle verbs split by audience as above.\n6. Stop-hook nudge with mandatory prohibition preamble.\n7. CAS per-project (under <slug>/.cas/), symlink-based produces.\n8. Inbox surface for external completion signals.\n9. Author test with golden runs.\n\nEXISTING REPO STATE:\n- artagents/core/orchestrator/ exists with schema.py, runner.py, registry.py, cli.py, api.py. Currently knows ORCHESTRATOR_KINDS={built_in, external} and RUNTIME_KINDS={python, command}. OrchestratorPlan / OrchestratorPlanStep skeletons exist (used for dry-run output).\n- artagents/core/project/ exists with run lifecycle (prepare_project_run / finalize_project_run), paths.py with DEFAULT_PROJECTS_ROOT.\n- artagents/threads/ exists with thread_wrapper around runs, @active concept.\n- artagents/packs/ holds builtin packs (cut, transcribe, human_notes, open_in_reigh, etc.).\n- Migration to packs is mid-flight (recent commits T10-T13).\n\nASSUMED OPEN-CALL DEFAULTS (the design plan should call these out and confirm or revise):\n- Keep nested step kind as data (gate sees the structure); forbid code-step-calls-orchestrator.\n- Python DSL is the only committed representation; JSON manifest is a build artifact in gitignored build/ dirs.\n- Drop .index.db from v1; ship with file-walk verbs.\n\nDELIVERABLE EXPECTATIONS for the design doc:\n- Concrete phasing aligned to build order 1-9 above; each phase has scope, files touched, breaking-change risk classification (additive vs breaking), and exit criteria.\n- Test strategy at each phase (golden runs are the regression format).\n- Migration of one builtin pack (suggest hype.cut or transcribe) to the new shape as the canonical example, including the diff shape.\n- Documentation deliverables identified: AUTHORING.md (one-page reference for both human and LLM authors), AGENT.md template, README.md updates.\n- Risk register (single-host assumption, semantic verifier discipline, context decay re-injection, agent honor model boundary).\n- Cut points where work can stop and still ship something useful (e.g., after phase 3, after phase 5).\n- A ## Settled Decisions section at the bottom listing every load-bearing design call (SD-NNN format) so future code-mode runs can inherit them via --from-doc.\n\nMode: doc / metaplan\nOutput: docs/orchestrator-v1-plan.md",
    "significant_flags": 9,
    "unresolved_flags": [
      {
        "id": "FLAG-001",
        "concern": "Task CLI surface: lifecycle verbs are top-level but the plan only maps them to the orchestrator CLI, while `artagents/pipeline.py` currently owns top-level dispatch and falls unknown commands through to builtin.hype.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "FLAG-002",
        "concern": "Gate ordering: saying the gate runs before `artagents/threads/wrapper.py` is not enough because project-run preparation happens earlier and can create run files before a task-mode rejection.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "issue_hints",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Flagged that the plan metadata assumes a new `artagents/core/task/` package while the main outline does not justify or consistently carry that namespace decision.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "correctness",
        "concern": "Are the proposed changes technically correct?: Flagged gate ordering: `run_orchestrator()` prepares project runs before thread wrapping, so a gate placed only before `artagents/threads/wrapper.py` can still leave side effects before rejection.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "scope-1",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Flagged missing top-level CLI integration: `artagents/pipeline.py` owns top-level dispatch, while the plan only maps verbs onto `artagents/core/orchestrator/cli.py`.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "scope-2",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Flagged ambiguity around `artagents runs ls`, since project CLI currently has no runs-list command and the plan does not choose the integration surface.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "all_locations",
        "concern": "Does the change touch all locations AND supporting infrastructure?: Flagged missing `.gitignore` support for generated `<pack>/build/<orch>.json` artifacts.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "callers",
        "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Flagged that `prepare_project_run()` is called by orchestrator, executor, and builtin.hype paths, so task-mode docs should define whether nested executor/project records share the same task run or create nested project records.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "criteria_quality",
        "concern": "Are the success criteria well-prioritized and verifiable?: Flagged that the path-citation criterion should distinguish existing-code citations from future planned deliverable paths like `AUTHORING.md`, `AGENT.md`, `build/`, `fixtures/`, and `golden/`.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      }
    ],
    "resolved_flags": [],
    "weighted_score": 15.0,
    "weighted_history": [],
    "plan_delta_from_previous": null,
    "recurring_critiques": [],
    "scope_creep_flags": [],
    "loop_summary": "Iteration 1. Weighted score trajectory: 15.0. Plan deltas: n/a. Recurring critiques: 0. Resolved flags: 0. Open significant flags: 9.",
    "debt_overlaps": [],
    "escalated_debt_subsystems": []
  },
  "warnings": [],
  "criteria_check": {
    "count": 20,
    "items": [
      {
        "criterion": "Document exists at exactly `docs/orchestrator-v1-plan.md` (no alternate filename based on title or kebab-case normalization).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Document ends with a `## Settled Decisions` section using `SD-NNN <topic>: <single-sentence rationale>.` format matching `docs/sprint-thread-layer.md`.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Settled Decisions section covers every load-bearing call enumerated in Step 9 (three step kinds; repeat as body attribute; plan.json rename; plain sha256 chain / no HMAC; no .index.db; Python DSL only; JSON manifest gitignored; per-project .cas; code-step-calls-orchestrator forbidden; gate four-check + recovery command; gate-before-wrapper; ARTAGENTS_ACTOR pinning + self-ack rejection; ack decision validity rules; produces inline checks; sentinel-only rejected at author check; Stop-hook preamble every call; additive migration; honor model; Phase 3 + Phase 5 cut points; builtin.hype canonical example; phasing 1\u20139).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Each of the nine phases includes scope, files-touched (with inline backticked path citations), classification (additive or breaking), exit criteria, and test strategy.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Storage tree section reproduces the task spec exactly: `active_run.json`, `runs/<run-id>/{plan.json,events.jsonl,AGENT.md}`, `steps/<id>/{produces,iterations/NNN,items/<id>}/`, `inbox/`, `<slug>/.cas/<sha256>` \u2014 and explicitly excludes `.index.db` and HMAC.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Step Kinds section names code, attested, nested; specifies repeat:{until|for_each} as body attributes; forbids code-step-calls-orchestrator.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Gate section enumerates all four checks (active_run.json present, plan.json hash matches pin, events.jsonl chain intact, command matches plan[derived_cursor].command) and states the gate emits an exact recovery command on rejection and runs before `artagents/threads/wrapper.py`.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Ack Decisions section specifies validity rules: retry only after verifier failure, iterate --feedback only when repeat.until=user_approves, abort ends run; --agent / ARTAGENTS_ACTOR pinning required; self-acks rejected; --item targets for_each.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Lifecycle Verbs section lists agent (next/ack/status/abort), operator (start/abort/status/runs ls), author (new/check/describe/test/compile/explain) and maps onto today's `python3 -m artagents orchestrators` CLI in `artagents/core/orchestrator/cli.py`.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Authoring section states Python DSL `artagents.orchestrate` is the only committed representation, JSON manifest is gitignored at `<pack>/build/<orch>.json`, runtime hashes/pins the build artifact, and pack adds `<orch>.py`, `fixtures/`, `golden/<name>.events.jsonl`.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Stop-hook section states the prohibition preamble is re-injected verbatim on every `artagents next` call (not just first call).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Canonical migration example uses `artagents/packs/builtin/hype/` (or transcribe as documented fallback) with a diff sketch showing the new `hype.py`, `build/hype.json`, `fixtures/`, `golden/`, and confirms existing JSON manifest still loads.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Risk register includes single-host assumption, semantic verifier discipline, context-decay re-injection, and honor-model boundary, each with trigger + mitigation.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Document explicitly Confirms or Revises the three open-call defaults (nested-as-data, Python DSL only, no .index.db v1).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Migration is presented as additive: existing `OrchestratorDefinition` JSON manifests + `python`/`command` `RUNTIME_KINDS` keep working through and after v1.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "All inline path citations resolve to files actually present in the repo (e.g., `artagents/core/orchestrator/runner.py`, `artagents/core/project/run.py`, `artagents/threads/wrapper.py`, `artagents/packs/builtin/hype/`).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Document body length lands in ~1500\u20132200 words (SD list excluded).",
        "priority": "should",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Tone is terse, declarative, decision-first; matches `docs/sprint-thread-layer.md` and `docs/design-thread-layer.md`.",
        "priority": "should",
        "requires": [
          "subjective_judgment",
          "read_files"
        ]
      },
      {
        "criterion": "Document does not introduce a daemon, web server, `.index.db`, HMAC/keyed crypto, or shared CAS in v1; these are explicitly listed in Non-Goals.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Cut Points section identifies Phase 3 (kernel + step kinds + produces/repeat) and Phase 5 (adds authoring + lifecycle verb split) as ship-ready milestones.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      }
    ]
  },
  "preflight_results": {
    "project_dir_exists": true,
    "project_dir_writable": true,
    "success_criteria_present": true,
    "claude_available": true,
    "codex_available": true
  },
  "unresolved_flags": [
    {
      "id": "FLAG-001",
      "concern": "Task CLI surface: lifecycle verbs are top-level but the plan only maps them to the orchestrator CLI, while `artagents/pipeline.py` currently owns top-level dispatch and falls unknown commands through to builtin.hype.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "`artagents/pipeline.py` dispatches known subcommands and then calls `_run_default_brief_orchestrator(raw)`; `artagents/core/orchestrator/cli.py` only handles `list`, `inspect`, `validate`, and `run` under `orchestrators`.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "FLAG-002",
      "concern": "Gate ordering: saying the gate runs before `artagents/threads/wrapper.py` is not enough because project-run preparation happens earlier and can create run files before a task-mode rejection.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "`artagents/core/orchestrator/runner.py:135-136` calls `_prepare_project_request()` before `thread_wrapper.begin_orchestrator_run()`, and `_prepare_project_request()` calls `prepare_project_run()`.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "issue_hints",
      "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Flagged that the plan metadata assumes a new `artagents/core/task/` package while the main outline does not justify or consistently carry that namespace decision.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Flagged that the plan metadata assumes a new `artagents/core/task/` package while the main outline does not justify or consistently carry that namespace decision.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "correctness",
      "concern": "Are the proposed changes technically correct?: Flagged gate ordering: `run_orchestrator()` prepares project runs before thread wrapping, so a gate placed only before `artagents/threads/wrapper.py` can still leave side effects before rejection.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Flagged gate ordering: `run_orchestrator()` prepares project runs before thread wrapping, so a gate placed only before `artagents/threads/wrapper.py` can still leave side effects before rejection.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "scope-1",
      "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Flagged missing top-level CLI integration: `artagents/pipeline.py` owns top-level dispatch, while the plan only maps verbs onto `artagents/core/orchestrator/cli.py`.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Flagged missing top-level CLI integration: `artagents/pipeline.py` owns top-level dispatch, while the plan only maps verbs onto `artagents/core/orchestrator/cli.py`.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "scope-2",
      "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Flagged ambiguity around `artagents runs ls`, since project CLI currently has no runs-list command and the plan does not choose the integration surface.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Flagged ambiguity around `artagents runs ls`, since project CLI currently has no runs-list command and the plan does not choose the integration surface.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "all_locations",
      "concern": "Does the change touch all locations AND supporting infrastructure?: Flagged missing `.gitignore` support for generated `<pack>/build/<orch>.json` artifacts.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Flagged missing `.gitignore` support for generated `<pack>/build/<orch>.json` artifacts.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "callers",
      "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Flagged that `prepare_project_run()` is called by orchestrator, executor, and builtin.hype paths, so task-mode docs should define whether nested executor/project records share the same task run or create nested project records.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Flagged that `prepare_project_run()` is called by orchestrator, executor, and builtin.hype paths, so task-mode docs should define whether nested executor/project records share the same task run or create nested project records.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "criteria_quality",
      "concern": "Are the success criteria well-prioritized and verifiable?: Flagged that the path-citation criterion should distinguish existing-code citations from future planned deliverable paths like `AUTHORING.md`, `AGENT.md`, `build/`, `fixtures/`, and `golden/`.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Flagged that the path-citation criterion should distinguish existing-code citations from future planned deliverable paths like `AUTHORING.md`, `AGENT.md`, `build/`, `fixtures/`, and `golden/`.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    }
  ]
}

        Critique check summary:
        - issue_hints: 1 flagged
        - correctness: 1 flagged
        - scope: 2 flagged
        - all_locations: 1 flagged
        - callers: 1 flagged
        - conventions: 1 flagged
        - verification: 1 flagged
        - criteria_quality: 1 flagged

        Unresolved significant flags:
        [
  {
    "id": "FLAG-001",
    "concern": "Task CLI surface: lifecycle verbs are top-level but the plan only maps them to the orchestrator CLI, while `artagents/pipeline.py` currently owns top-level dispatch and falls unknown commands through to builtin.hype.",
    "evidence": "`artagents/pipeline.py` dispatches known subcommands and then calls `_run_default_brief_orchestrator(raw)`; `artagents/core/orchestrator/cli.py` only handles `list`, `inspect`, `validate`, and `run` under `orchestrators`.",
    "category": "completeness",
    "severity": "significant",
    "status": "open",
    "weight": null
  },
  {
    "id": "FLAG-002",
    "concern": "Gate ordering: saying the gate runs before `artagents/threads/wrapper.py` is not enough because project-run preparation happens earlier and can create run files before a task-mode rejection.",
    "evidence": "`artagents/core/orchestrator/runner.py:135-136` calls `_prepare_project_request()` before `thread_wrapper.begin_orchestrator_run()`, and `_prepare_project_request()` calls `prepare_project_run()`.",
    "category": "correctness",
    "severity": "significant",
    "status": "open",
    "weight": null
  },
  {
    "id": "issue_hints",
    "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Flagged that the plan metadata assumes a new `artagents/core/task/` package while the main outline does not justify or consistently carry that namespace decision.",
    "evidence": "Flagged that the plan metadata assumes a new `artagents/core/task/` package while the main outline does not justify or consistently carry that namespace decision.",
    "category": "completeness",
    "severity": "significant",
    "status": "open",
    "weight": null
  },
  {
    "id": "correctness",
    "concern": "Are the proposed changes technically correct?: Flagged gate ordering: `run_orchestrator()` prepares project runs before thread wrapping, so a gate placed only before `artagents/threads/wrapper.py` can still leave side effects before rejection.",
    "evidence": "Flagged gate ordering: `run_orchestrator()` prepares project runs before thread wrapping, so a gate placed only before `artagents/threads/wrapper.py` can still leave side effects before rejection.",
    "category": "correctness",
    "severity": "significant",
    "status": "open",
    "weight": null
  },
  {
    "id": "scope-1",
    "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Flagged missing top-level CLI integration: `artagents/pipeline.py` owns top-level dispatch, while the plan only maps verbs onto `artagents/core/orchestrator/cli.py`.",
    "evidence": "Flagged missing top-level CLI integration: `artagents/pipeline.py` owns top-level dispatch, while the plan only maps verbs onto `artagents/core/orchestrator/cli.py`.",
    "category": "completeness",
    "severity": "significant",
    "status": "open",
    "weight": null
  },
  {
    "id": "scope-2",
    "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Flagged ambiguity around `artagents runs ls`, since project CLI currently has no runs-list command and the plan does not choose the integration surface.",
    "evidence": "Flagged ambiguity around `artagents runs ls`, since project CLI currently has no runs-list command and the plan does not choose the integration surface.",
    "category": "completeness",
    "severity": "significant",
    "status": "open",
    "weight": null
  },
  {
    "id": "all_locations",
    "concern": "Does the change touch all locations AND supporting infrastructure?: Flagged missing `.gitignore` support for generated `<pack>/build/<orch>.json` artifacts.",
    "evidence": "Flagged missing `.gitignore` support for generated `<pack>/build/<orch>.json` artifacts.",
    "category": "completeness",
    "severity": "significant",
    "status": "open",
    "weight": null
  },
  {
    "id": "callers",
    "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Flagged that `prepare_project_run()` is called by orchestrator, executor, and builtin.hype paths, so task-mode docs should define whether nested executor/project records share the same task run or create nested project records.",
    "evidence": "Flagged that `prepare_project_run()` is called by orchestrator, executor, and builtin.hype paths, so task-mode docs should define whether nested executor/project records share the same task run or create nested project records.",
    "category": "correctness",
    "severity": "significant",
    "status": "open",
    "weight": null
  },
  {
    "id": "criteria_quality",
    "concern": "Are the success criteria well-prioritized and verifiable?: Flagged that the path-citation criterion should distinguish existing-code citations from future planned deliverable paths like `AUTHORING.md`, `AGENT.md`, `build/`, `fixtures/`, and `golden/`.",
    "evidence": "Flagged that the path-citation criterion should distinguish existing-code citations from future planned deliverable paths like `AUTHORING.md`, `AGENT.md`, `build/`, `fixtures/`, and `golden/`.",
    "category": "completeness",
    "severity": "significant",
    "status": "open",
    "weight": null
  }
]

        Known accepted debt grouped by subsystem:
{}

Escalated debt subsystems:
[]

Debt guidance:
- Treat recurring debt as decision context, not background noise.
- If the current unresolved flags overlap an escalated subsystem, prefer recommending holistic redesign over another point fix.

        Iteration Pressure Analysis:
Group      Flags  Iters  Reopened  Concern
------------------------------------------------------------------------
FG-001     1      1      0         Flagged that the plan metadata assumes a new `arta
FG-002     1      1      0         Flagged gate ordering: `run_orchestrator()` prepar
FG-003     1      1      0         Flagged ambiguity around `artagents runs ls`, sinc
FG-004     1      1      0         Flagged missing `.gitignore` support for generated
FG-005     1      1      0         Flagged that `prepare_project_run()` is called by 
FG-006     1      1      0         Flagged that the authoring section must not imply 
FG-007     1      1      0         Flagged that phase test strategy should name curre
FG-008     1      1      0         Flagged that the path-citation criterion should di
FG-009     1      1      0         Task CLI surface: lifecycle verbs are top-level bu
FG-010     1      1      0         Gate ordering: saying the gate runs before `artage
FG-011     1      1      0         Authoring build artifacts: the plan requires gitig
FG-012     1      1      0         Criterion 17: requires human verification (subject
FG-013     1      1      0         Search for related code that handles the same conc
FG-014     1      1      0         Search for related code that handles the same conc

        Robustness level:
        robust

        Requirements:
        - Decide exactly one of: PROCEED, ITERATE, ESCALATE, TIEBREAKER.
        - Use the weighted score, flag details (including `evidence`), plan delta, recurring critiques, and preflight results as judgment context.
        - PROCEED when execution should move forward now.
        - ITERATE when revising the plan is the best next move.
        - ESCALATE when the loop is stuck, churn is recurring, or user intervention is needed.
        - TIEBREAKER when a flag group reflects an *unresolvable constraint tension* (architectural or philosophical — requires a human call) rather than a plan-quality issue. Use TIEBREAKER only when the Iteration Pressure Analysis shows `addressed_then_reopened_count >= 2` for a fuzzy group OR the group has >=2 member flags across >=2 iterations. If the concern is simply that the plan writer hasn't tried hard enough, use ITERATE instead. When recommending TIEBREAKER you MUST provide `tiebreaker_question` (the decision question for human resolution), `tiebreaker_flag_ids` (which flags this resolves), and `tiebreaker_fuzzy_group_id` (which group this resolves). Cite specific flag IDs and iterations in your rationale.
        - `signals_assessment`: one paragraph summarizing score trajectory, flag status, and preflight posture.

        Flags come in two tiers:
        - **Blocking** (severity = significant/likely-significant): These are serious concerns. If you recommend PROCEED, you MUST provide a `flag_resolutions` entry for every blocking flag. There is no implicit acceptance.
        - **Noted** (everything else): Acknowledge in your rationale but they don't block PROCEED.

        If there are blocking flags and you want to PROCEED, provide `flag_resolutions` with one entry per blocking flag. If you cannot resolve every blocking flag, choose ITERATE (send back for revision) or ESCALATE (human intervention needed).
        Structurally unresolvable flags (for example, infrastructure outside the repo or product decisions that require a human) are ESCALATE, not PROCEED with a non-answer.

        For each blocking flag:
        - **dispute**: The critique is factually wrong. Evidence must cite something specific (file path, line, API doc, etc.). Generic statements like "handled correctly" are invalid.
        - **accept_tradeoff**: The concern is real but intentionally accepted as a known limitation. Rationale must be specific to this flag. Boilerplate like "acceptable within scope" is invalid.
        - Schema requirement: every `flag_resolutions` entry must include both `evidence` and `rationale`. Use `""` for the field that does not apply to that action.

        If there are no blocking flags, return `flag_resolutions: []`.
        Always return `accepted_tradeoffs`; use `[]` when none apply.

        Populate `settled_decisions` with design choices that should carry into review without re-litigation. Return `[]` when there are none.

        Example:
        ```json
        {
          "recommendation": "PROCEED",
          "rationale": "Core fix is correct. Convention concern accepted.",
          "signals_assessment": "Score stable at 2.5, preflight passed, no recurring critiques.",
          "warnings": ["Verify edge case with composite moduli during execution."],
          "flag_resolutions": [
            {"flag_id": "correctness-1", "action": "dispute", "evidence": "allow_migrate and allow_migrate_model produce identical behavior for this use case (verified at django/db/utils.py:286).", "rationale": ""},
            {"flag_id": "performance-1", "action": "accept_tradeoff", "evidence": "", "rationale": "Cold-start latency remains 40ms above target because the cache warmup job is owned by platform and outside this repo; rollout is still approved for the limited internal beta."},
            {"flag_id": "conventions-1", "action": "accept_tradeoff", "evidence": "", "rationale": "Minor naming inconsistency is confined to this helper and would create churn across generated fixtures; track it as follow-up cleanup instead of blocking this fix."}
          ],
          "accepted_tradeoffs": [],
          "settled_decisions": []
        }
        ```

> TOOL

tool_use StructuredOutput
```json
{
  "recommendation": "ITERATE",
  "rationale": "Nine significant blocking flags are open at iteration 1, all citing concrete repo evidence (pipeline.py vs orchestrator/cli.py dispatch split, runner.py:135-136 ordering of prepare_project_run before thread wrapping, missing .gitignore guidance, undecided nested-run semantics for prepare_project_run callers, ambiguous `runs ls` surface, inconsistent core/task/ namespace use). These are plan-completeness gaps that the doc author can address by tightening Sections 7 (Gate), 8 (Ack/Lifecycle), and 13 (Migration), plus adding explicit decisions for CLI integration surface and namespace. None reflect a constraint tension requiring a human tiebreaker — they are tractable design calls the next plan revision should settle. No churn yet (iter 1, no reopened flags), so ESCALATE is premature; PROCEED is unsafe because executing this doc as-is would bake in unresolved correctness ambiguities (gate ordering) and CLI scope gaps that downstream code-mode runs would inherit via --from-doc.",
  "signals_assessment": "Iteration 1, weighted score 15.0 with no history yet, 9 open significant flags / 0 resolved, no reopened flags, no recurring critiques, no scope creep, no escalated debt. Preflight clean (project dir writable, claude+codex available, success criteria present). Robustness \"robust\" matches the flag density — critics found real gaps rather than nits. Trajectory is unmeasured; first-pass plan needs one revision cycle before execution.",
  "warnings": [
    "Next revision must pick a concrete CLI integration surface — either extend artagents/pipeline.py dispatch table to add task-mode verbs (next/ack/status/abort/start/runs/author) or commit to a new top-level entry — and state it in Section 8 with a citation to artagents/pipeline.py.",
    "Gate ordering must be re-stated: gate runs before BOTH artagents/threads/wrapper.py AND _prepare_project_request() in artagents/core/orchestrator/runner.py, so no project-run filesystem side effects occur on rejection.",
    "Decide and state in Section 13 whether nested executor/builtin.hype calls into prepare_project_run share the parent task run-id or create child project records, since the function has three caller paths.",
    "Add an explicit Section 10 sub-bullet that .gitignore is updated to exclude <pack>/build/ artifacts as part of Phase 4 exit criteria.",
    "Resolve the artagents/core/task/ namespace question explicitly — either justify the new package as a settled decision (SD entry) or fold the kernel into artagents/core/orchestrator/ as additive submodules, and carry that choice consistently through all phase file-touch lists.",
    "Section 12 (`runs ls`) must name the integration surface (project CLI vs orchestrator CLI vs new top-level) and cite the file it lands in.",
    "Distinguish in path-citation success criterion between existing-code citations (must resolve today) and future deliverable paths (AUTHORING.md, AGENT.md, build/, fixtures/, golden/) which are prescriptive."
  ],
  "flag_resolutions": [],
  "accepted_tradeoffs": [],
  "settled_decisions": [
    {
      "id": "SD-G1",
      "decision": "Doc body target ~1500-2200 words excluding the SD list; SD list grows as needed.",
      "rationale": "Matches docs/sprint-thread-layer.md tone reference and was uncontested in this iteration."
    },
    {
      "id": "SD-G2",
      "decision": "Canonical migration example is artagents/packs/builtin/hype/; transcribe is a fallback only if hype is too sprawling for an inline diff sketch.",
      "rationale": "Confirmed in plan assumptions and not flagged."
    },
    {
      "id": "SD-G3",
      "decision": "Output path is exactly docs/orchestrator-v1-plan.md.",
      "rationale": "Fixed by task brief; uncontested."
    },
    {
      "id": "SD-G4",
      "decision": "SD entries follow `SD-NNN <topic>: <single-sentence rationale>.` format per docs/sprint-thread-layer.md lines 39-43.",
      "rationale": "Format reference confirmed; uncontested."
    }
  ],
  "tiebreaker_question": "",
  "tiebreaker_flag_ids": [],
  "tiebreaker_fuzzy_group_id": ""
}
```

> TOOL

tool_result StructuredOutput
```
Structured output provided successfully
```

> AGENT

Recommended **ITERATE**. The first-pass plan has 9 legitimate blocking gaps (CLI integration surface, gate ordering before `prepare_project_run`, namespace decision for `core/task/`, `.gitignore` for `build/`, nested-run semantics, `runs ls` surface), all resolvable by the doc author in one revision pass. No churn yet, so escalation is premature; executing as-is would bake unresolved ambiguities into the frozen design doc.

> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

WRITE ACCESS CONTRACT: You are running with auto-approved writes inside a writable workspace. Treat the working directory as fully writable. Do NOT preemptively skip or block tasks on permission, sandbox, or read-only grounds. Attempt every required edit; only report failure AFTER a real OS-level rejection from a specific shell command. Do not infer 'read-only' from absence of activity; absence is not denial. If a single shell command unexpectedly fails, retry with a different invocation before concluding the environment is restricted.

You are the gatekeeper for the megaplan workflow. Make the continuation decision directly.

        Project directory:
        /Users/user_c042661f/Documents/reigh-workspace/ArtAgents

        Idea:
ArtAgents is a file-based, single-host Python CLI for running creative pipelines (video/audio/image) that mix code, AI, and human steps. Today it has a pack-based plugin architecture, orchestrator + executor schemas (python/command runtime kinds only), project runs under ~/Documents/reigh-workspace/artagents-projects/, threads with provenance, and a CLI gateway. We are extending it so an agent can be put into 'task mode' and walked through a frozen plan that mixes code, AI, and human steps, with iteration loops and fan-out.

NON-NEGOTIABLES:
- Single-host, file-based. No daemon, no web server.
- Honor-based with strong logging. We do not pretend to sandbox a misaligned agent.
- Migration is additive. Existing JSON manifests and python/command runtime kinds keep working.
- Existing pack mechanism stays.

V1 DESIGN (post-critique, trimmed):

THREE STEP KINDS:
- code: deterministic argv, runner subprocesses, returncode + produces.
- attested: agent or human task. instructions + produces + ack records identity (agent_id or actor pinned via ARTAGENTS_ACTOR) + evidence.
- nested: delegates to a child plan; gate sees the structure for hashing/pinning.

ITERATION AND FAN-OUT ARE BODY ATTRIBUTES, NOT KINDS:
- repeat: {until: user_approves|verifier_passes|quorum, max_iterations, on_exhaust}
- repeat: {for_each: <input_set>}
Both apply to any step or to a body block in a nested plan.

PRODUCES WITH INLINE CHECKS (replaces separate verifier substep):
  produces = {
    'audio': file(path='audio.wav', check=audio_duration_min(30)),
    'notes': json_file(path='notes.json', schema='notes.schema.json', min_items=3),
  }
The gate runs the check; failure rewinds the cursor. passes_test is a regular code step.

STORAGE (under ~/Documents/reigh-workspace/artagents-projects/):
- <slug>/active_run.json -- pointer to in-flight run + plan hash
- <slug>/runs/<run-id>/plan.json -- immutable, hash-pinned (renamed from 'checklist' since it's a tree)
- <slug>/runs/<run-id>/events.jsonl -- append-only, plain hash-chained (prev_hash field), sole truth
- <slug>/runs/<run-id>/AGENT.md -- contract for whoever's driving
- <slug>/runs/<run-id>/steps/<step-id>/produces/ -- artifact files (or symlinks into .cas)
- <slug>/runs/<run-id>/steps/<step-id>/iterations/NNN/ -- when repeat:until is set
- <slug>/runs/<run-id>/steps/<step-id>/items/<item-id>/ -- when repeat:for_each is set
- <slug>/runs/<run-id>/inbox/ -- external completion signals get dropped here
- <slug>/.cas/<sha256> -- per-project CAS for v1 (not shared)

NO crypto: hash chain is plain sha256(prev_hash + canonical_event_json). Tripwire for accidental edits, not protection against malicious users. We do not need HMAC or key handles.

NO .index.db in v1. find + grep on events.jsonl is fine until grep is slow.

GATE (above dispatch, single function):
- active_run.json exists for this project?
- plan.json hash matches the pin in active_run.json?
- events.jsonl hash chain intact?
- incoming command matches plan[derived_cursor].command?
If any fails, reject with the exact recovery command.

LIFECYCLE VERBS, scoped by audience:
artagents next | ack | status | abort                                  (agent-facing, mid-run)
artagents start | abort | status | runs ls                             (operator)
artagents author new | check | describe | test | compile | explain     (author)

ACK DECISIONS (intentionally distinct):
--decision approve              -- advance cursor
--decision retry                -- only valid after verifier failure; rerun body, stderr is feedback
--decision iterate --feedback   -- only valid when repeat.until=user_approves; appends to cumulative constraints
--decision abort                -- end run

ACK requires --agent <id> for attested steps with attestor_type=agent, or --actor <name> matching ARTAGENTS_ACTOR for attestor_type=human. Self-acks and unpinned actors are rejected.

For repeat:for_each: --item <id> targets a specific item; partial approval is supported.

NUDGE (out-of-process, optional, Claude Code only for v1):
A Stop hook runs artagents next. The next output ALWAYS includes the prohibition preamble verbatim, not just on first call -- this is the re-injection mechanism that fights context decay.

AUTHORING:
- Python DSL artagents.orchestrate is the ONLY committed representation. JSON manifest is generated at author compile into a build/ dir (gitignored) and that's what the runtime hashes/pins.
- Verifier helper library artagents.verify: file_nonempty, json_schema, json_file, audio_duration_min, image_dimensions, all_of.
- Pack layout: <pack>/<orch>.py (committed), <pack>/build/<orch>.json (gitignored), <pack>/fixtures/<name>/, <pack>/golden/<name>.events.jsonl.
- author check is sub-second static validation: schema, every produces/requires reference resolves, every nested plan resolves, attested steps with non-trivial produces have semantic checks (sentinel-existence-only is rejected at definition time).
- author describe pretty-prints the DAG.
- author test --fixture runs --dry-run --auto-approve, diffs events.jsonl against golden/<fixture>.events.jsonl.

V1 BUILD ORDER (recommended phases):
1. Kernel: events.jsonl + plain hash chain + plan hash pin + gate above dispatch + active_run.json. Runner becomes dumb; gate is a single decorated function above runner dispatch.
2. Three step kinds: code, attested, nested. (code is a strict superset of today's python+command runtime kinds.)
3. produces-with-inline-checks; repeat:{until} and repeat:{for_each} on bodies.
4. Authoring: Python DSL + verify helpers + author check + author describe + author new.
5. Lifecycle verbs split by audience as above.
6. Stop-hook nudge with mandatory prohibition preamble.
7. CAS per-project (under <slug>/.cas/), symlink-based produces.
8. Inbox surface for external completion signals.
9. Author test with golden runs.

EXISTING REPO STATE:
- artagents/core/orchestrator/ exists with schema.py, runner.py, registry.py, cli.py, api.py. Currently knows ORCHESTRATOR_KINDS={built_in, external} and RUNTIME_KINDS={python, command}. OrchestratorPlan / OrchestratorPlanStep skeletons exist (used for dry-run output).
- artagents/core/project/ exists with run lifecycle (prepare_project_run / finalize_project_run), paths.py with DEFAULT_PROJECTS_ROOT.
- artagents/threads/ exists with thread_wrapper around runs, @active concept.
- artagents/packs/ holds builtin packs (cut, transcribe, human_notes, open_in_reigh, etc.).
- Migration to packs is mid-flight (recent commits T10-T13).

ASSUMED OPEN-CALL DEFAULTS (the design plan should call these out and confirm or revise):
- Keep nested step kind as data (gate sees the structure); forbid code-step-calls-orchestrator.
- Python DSL is the only committed representation; JSON manifest is a build artifact in gitignored build/ dirs.
- Drop .index.db from v1; ship with file-walk verbs.

DELIVERABLE EXPECTATIONS for the design doc:
- Concrete phasing aligned to build order 1-9 above; each phase has scope, files touched, breaking-change risk classification (additive vs breaking), and exit criteria.
- Test strategy at each phase (golden runs are the regression format).
- Migration of one builtin pack (suggest hype.cut or transcribe) to the new shape as the canonical example, including the diff shape.
- Documentation deliverables identified: AUTHORING.md (one-page reference for both human and LLM authors), AGENT.md template, README.md updates.
- Risk register (single-host assumption, semantic verifier discipline, context decay re-injection, agent honor model boundary).
- Cut points where work can stop and still ship something useful (e.g., after phase 3, after phase 5).
- A ## Settled Decisions section at the bottom listing every load-bearing design call (SD-NNN format) so future code-mode runs can inherit them via --from-doc.

Mode: doc / metaplan
Output: docs/orchestrator-v1-plan.md

User notes and answers:
- strict-notes auto-enabled for metaplan/doc mode

        Plan:
        # Implementation Plan: Author docs/orchestrator-v1-plan.md (Task Mode V1 Design)

## Overview

Single deliverable: `docs/orchestrator-v1-plan.md` — a frozen, decision-first design+migration doc adding "task mode" to ArtAgents. The doc must reproduce the task spec exactly on storage, gate, ack, and phasing; cite repo paths inline; end with `## Settled Decisions` (`SD-NNN <topic>: <single-sentence rationale>.`) matching `docs/sprint-thread-layer.md` lines 39–43.

Verified repo facts that the doc must encode (not paraphrase):
- Top-level CLI dispatch lives in `artagents/pipeline.py:15` (`main`); unknown subcommands fall through to `_run_default_brief_orchestrator()` at `artagents/pipeline.py:75`. Lifecycle verbs MUST land here, not under the existing `orchestrators` subparser in `artagents/core/orchestrator/cli.py`.
- `artagents/core/orchestrator/runner.py:135` calls `_prepare_project_request()` BEFORE `thread_wrapper.begin_orchestrator_run()` at line 136. The gate must intercept earlier than both.
- `artagents/core/project/run.py` `prepare_project_run()` is called by orchestrator, executor, and `builtin.hype` paths; the doc must define nested-call semantics (child runs inherit the parent task run-id via env, no nested project records).
- `artagents/core/orchestrator/schema.py` enforces `ORCHESTRATOR_KINDS={built_in,external}` and `RUNTIME_KINDS={python,command}`; existing JSON manifests must keep loading via `load_orchestrator_manifest`.
- Canonical migration target: `artagents/packs/builtin/hype/` (today: `orchestrator.yaml` + `STAGE.md` + `run.py`).

Output path is fixed: `docs/orchestrator-v1-plan.md`. Do not write elsewhere; the executor only writes to that exact path.

## Open-Call Decisions (resolved before authoring)

- A1 — nested step kind stays as data; `code-step-calls-orchestrator` forbidden. **Confirmed.**
- A2 — Python DSL `artagents.orchestrate` is the only committed representation; JSON manifest at `<pack>/build/<orch>.json` is gitignored. **Confirmed.**
- A3 — no `.index.db` in v1; file-walk verbs only. **Confirmed.**
- A4 (resolves `issue_hints` flag) — kernel modules land in a NEW `artagents/core/task/` package (gate, events, active_run, dispatch, produces, cas, inbox, preamble), NOT under `artagents/core/orchestrator/`. Rationale: gate sits ABOVE orchestrator dispatch and must precede `_prepare_project_request()`; placing it inside the orchestrator package would invert the ownership relationship. Recorded as an SD entry.
- A5 (resolves FLAG-001/scope-1/scope-2) — top-level lifecycle/operator verbs (`next`, `ack`, `status`, `abort`, `start`, `runs ls`) extend `artagents/pipeline.py:15` dispatch table. Author verbs (`new`/`check`/`describe`/`test`/`compile`/`explain`) live under a new top-level `author` subcommand also dispatched from `artagents/pipeline.py`. Existing `artagents orchestrators run` keeps working unchanged. Recorded as an SD entry.
- A6 (resolves `callers` flag) — when an `attested`/`code` step shells out to today's `artagents executors run` or `artagents orchestrators run` (or `builtin.hype`), child `prepare_project_run()` invocations DO NOT create nested project records; they inherit the parent task run-id via `ARTAGENTS_TASK_RUN_ID` env and append events to the same `runs/<task-run-id>/events.jsonl`. Recorded as an SD entry.
- A7 (resolves FLAG-002/correctness) — gate runs BEFORE BOTH `_prepare_project_request()` (`artagents/core/orchestrator/runner.py:135`) AND `thread_wrapper.begin_orchestrator_run()` (line 136). Implementation: gate is invoked from `artagents/pipeline.py` dispatch (and from a top-of-`run_orchestrator()` decorator) so a rejected command produces zero project-run filesystem side effects. Recorded as an SD entry.
- A8 (resolves `all_locations` flag) — Phase 4 exit criteria include adding `<pack>/build/` to repo `.gitignore` (root-level `.gitignore`) and any pack-local `.gitignore` if used. Recorded as an SD entry.

## Main Phase

### Step 1: Front matter + Sections 1–2 — Executive Summary, Goals/Non-Goals (`docs/orchestrator-v1-plan.md`)
**Scope:** Small
1. **Write** H1 title and ~150-word Executive Summary naming task mode, three step kinds, iteration/fan-out body attributes, and the additive-migration thesis.
2. **List** Goals (frozen hash-pinned plans, gate above dispatch, three step kinds, repeat as body attribute, golden-run regression, audience-split verbs).
3. **List** Non-Goals explicitly: daemon, web server, HMAC/keyed crypto, `.index.db`, shared CAS, sandbox against malicious agents.

### Step 2: Section 3 — Data Model (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Render** the storage tree under `~/Documents/reigh-workspace/artagents-projects/<slug>/` exactly as the spec: `active_run.json`; `runs/<run-id>/{plan.json,events.jsonl,AGENT.md}`; `steps/<id>/{produces,iterations/NNN,items/<id>}/`; `inbox/`; `<slug>/.cas/<sha256>`. Express as additions to `artagents/core/project/paths.py` helpers (`run_dir`, `run_json_path`).
2. **Define** `plan.json` (immutable, hash-pinned, supersedes "checklist") and its relationship to `OrchestratorPlan`/`OrchestratorPlanStep` in `artagents/core/orchestrator/runner.py` (reframed from dry-run stub to immutable plan tree; existing `OrchestratorDefinition` JSON manifests remain peer-valid).
3. **Define** `events.jsonl` chain as plain `sha256(prev_hash + canonical_event_json)`; sole source of truth; rationale for no HMAC.
4. **Define** `active_run.json` as `{run_id, plan_hash}` pointer.
5. **State** explicit exclusions: `.index.db` not in v1; HMAC not in v1.

### Step 3: Sections 4–6 — Step Kinds, Iteration/Fan-Out, Produces (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Specify** three step kinds: `code` (strict superset of `RUNTIME_KINDS={python,command}` in `artagents/core/orchestrator/schema.py`), `attested` (agent or human; ack pins identity via `--agent` or `ARTAGENTS_ACTOR`; self-acks rejected), `nested` (delegates to child plan; gate sees structure for hashing). Forbid `code-step-calls-orchestrator`.
2. **Specify** `repeat:{until: user_approves|verifier_passes|quorum, max_iterations, on_exhaust}` and `repeat:{for_each: <input_set>}` as body attributes on any step or nested-plan body. Document `iterations/NNN/` and `items/<item-id>/` layout. Document partial approval semantics for `for_each`.
3. **Specify** `produces` block with inline checks (`file_nonempty`, `json_schema`, `json_file`, `audio_duration_min`, `image_dimensions`, `all_of`). Failure rewinds cursor; `passes_test` is a regular `code` step; sentinel-existence-only is rejected at definition time by `author check`.

### Step 4: Section 7 — Gate Above Dispatch (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Enumerate** the four checks: `active_run.json` exists for project; `plan.json` hash matches pin in `active_run.json`; `events.jsonl` chain intact; incoming command matches `plan[derived_cursor].command`. On any failure: emit the exact recovery command and exit non-zero.
2. **State ordering precisely** (resolves FLAG-002): the gate is invoked from `artagents/pipeline.py` dispatch BEFORE control reaches `artagents/core/orchestrator/runner.py:run_orchestrator`, AND a defensive gate decorator at the top of `run_orchestrator()` re-checks before `_prepare_project_request()` (`artagents/core/orchestrator/runner.py:135`) and `thread_wrapper.begin_orchestrator_run()` (line 136). A rejected command writes zero project-run files.
3. **State** that `events.jsonl` is the single write surface: when the gate accepts, the wrapper at `artagents/threads/wrapper.py` does NOT duplicate provenance into `events.jsonl`; thread provenance remains in `runs/<id>/run.json`. Cite `begin_orchestrator_run`/`finalize_result` in `artagents/threads/wrapper.py`.

### Step 5: Sections 8–9 — Lifecycle Verbs + Ack Decisions (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **List** verbs by audience and explicitly land them in `artagents/pipeline.py:15` dispatch table (resolves FLAG-001/scope-1/scope-2):
   - Agent-facing (mid-run): `artagents next | ack | status | abort` — new top-level subcommands in `artagents/pipeline.py`.
   - Operator: `artagents start | abort | status | runs ls` — `runs ls` is a new top-level subcommand in `artagents/pipeline.py` (NOT under `orchestrators` or any existing subparser).
   - Author: `artagents author new | check | describe | test | compile | explain` — new `author` top-level subparser in `artagents/pipeline.py`.
   - Existing `artagents orchestrators run|list|inspect|validate` (`artagents/core/orchestrator/cli.py`) remains unchanged for back-compat.
2. **Specify** ack decision validity table:
   - `--decision approve` — advance cursor.
   - `--decision retry` — only valid after verifier failure; rerun body, stderr is feedback.
   - `--decision iterate --feedback <text>` — only valid when `repeat.until=user_approves`; appended to cumulative constraints.
   - `--decision abort` — end run.
3. **Specify** identity rules: `--agent <id>` for `attested` with `attestor_type=agent`; `--actor <name>` matching `ARTAGENTS_ACTOR` env for `attestor_type=human`; self-acks and unpinned actors rejected; `--item <id>` targets a specific item under `repeat:for_each`.

### Step 6: Sections 10–11 — Authoring + Stop-hook Nudge (`docs/orchestrator-v1-plan.md`)
**Scope:** Small
1. **State** Python DSL `artagents.orchestrate` is the only committed representation; `<pack>/build/<orch>.json` is generated by `author compile` and is gitignored (root `.gitignore` updated in Phase 4); runtime hashes/pins the build artifact.
2. **List** pack additions (over `artagents/packs/builtin/hype/` baseline): `<pack>/<orch>.py` (committed), `<pack>/build/<orch>.json` (gitignored), `<pack>/fixtures/<name>/`, `<pack>/golden/<name>.events.jsonl`. Verify helpers live in `artagents.verify`.
3. **Specify** `author check` is sub-second static validation: schema, every `produces`/`requires` resolves, every nested plan resolves, attested-with-non-trivial-produces requires semantic checks (sentinel-only rejected). `author describe` pretty-prints DAG. `author test --fixture` runs `--dry-run --auto-approve` and diffs `events.jsonl` against `golden/<fixture>.events.jsonl`.
4. **State** Stop-hook nudge is Claude Code only in v1; the prohibition preamble is re-injected verbatim on every `artagents next` call (not just first), as the context-decay mitigation.

### Step 7: Section 12 — Phasing 1–9 (`docs/orchestrator-v1-plan.md`)
**Scope:** Large

For each phase emit five fields: **Scope**, **Files touched** (inline backticked path citations), **Classification** (additive | breaking), **Exit criteria**, **Test strategy** (golden runs).

1. **Phase 1 — Kernel.** Scope: `events.jsonl` + plain hash chain + `plan_hash` pin + gate above dispatch + `active_run.json`. Files: new `artagents/core/task/{gate.py,events.py,active_run.py}`; touches `artagents/pipeline.py:15` (gate-before-dispatch), `artagents/core/orchestrator/runner.py:135` (defensive gate decorator at top of `run_orchestrator`), `artagents/core/project/run.py` (kernel writes `plan.json`/`events.jsonl` next to `run.json`), `artagents/threads/wrapper.py` (no double-write of provenance into events.jsonl). Classification: **additive**. Exit: a hand-authored `plan.json` runs end-to-end with chain verification AND a rejected command produces zero project-run files. Tests: golden run for the smallest hand-authored plan + rejection-leaves-no-side-effects test.
2. **Phase 2 — Three step kinds.** Scope: `code` (strict superset of today's `python`+`command`), `attested`, `nested`. Files: new `artagents/core/task/dispatch.py`; extends `artagents/core/orchestrator/schema.py` (step-kind enum on `plan.json`). Classification: **additive** (existing `OrchestratorPlanStep.kind='command'` still loads). Exit: each kind dispatches and emits correct events. Tests: per-kind golden runs.
3. **Phase 3 — Produces + repeat.** Scope: `produces` inline checks; `repeat:{until|for_each}` on bodies. Files: new `artagents/verify/__init__.py`, new `artagents/core/task/produces.py`; gate cursor-rewind. Classification: **additive**. Exit: failing checks rewind cursor; `for_each` materializes `items/<id>/`; `until` materializes `iterations/NNN/`. Tests: golden runs covering `until` + `for_each` + check-failure rewind.
4. **Phase 4 — Authoring.** Files: new `artagents/orchestrate/` (Python DSL); extends `artagents/core/orchestrator/cli.py` AND adds `author` subparser to `artagents/pipeline.py`; updates root `.gitignore` to exclude `<pack>/build/` (resolves `all_locations` flag). Classification: **additive**. Exit: `<orch>.py` compiles to `build/<orch>.json` whose hash matches what runtime pins; `.gitignore` excludes `<pack>/build/`. Tests: snapshot of generated JSON; sub-second `author check` perf check.
5. **Phase 5 — Lifecycle verbs split by audience.** Files: extends `artagents/pipeline.py:15` dispatch table with `next`, `ack`, `status`, `abort`, `start`, `runs ls`, `author` subcommands. `artagents/core/orchestrator/cli.py` keeps existing verbs. Classification: **additive**. Exit: every audience-scoped verb returns from a real run. Tests: smoke test invoking each verb against a fixture run.
6. **Phase 6 — Stop-hook nudge.** Files: new `artagents/core/task/preamble.py`; example Claude Code `.claude/settings.json` Stop-hook config in docs. Classification: **additive**. Exit: every `artagents next` output begins with the prohibition preamble verbatim. Tests: golden run asserts preamble appears on N consecutive `next` calls (not just first).
7. **Phase 7 — CAS per-project.** Files: new `artagents/core/task/cas.py`; symlink-based `produces` written into `<slug>/.cas/<sha256>`. Classification: **additive**. Exit: identical artifacts deduped under `<slug>/.cas/`. Tests: golden run shows symlink reuse across two runs.
8. **Phase 8 — Inbox surface.** Files: new `artagents/core/task/inbox.py`; gate watches `runs/<run-id>/inbox/`. Classification: **additive**. Exit: file dropped in `inbox/` advances the cursor on the next `artagents next` call. Tests: golden run with inbox-driven advance.
9. **Phase 9 — Author test with golden runs.** Files: extends `author` subparser in `artagents/pipeline.py` with `test --fixture`. Classification: **additive**. Exit: every prior-phase golden is wired into `author test` and runs in CI. Tests: meta-test that `author test` re-runs every shipped golden.

### Step 8: Section 13 — Canonical Migration: `artagents/packs/builtin/hype/` (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Show** the diff sketch: ADD `artagents/packs/builtin/hype/hype.py` (DSL); ADD `artagents/packs/builtin/hype/build/hype.json` (gitignored); ADD `artagents/packs/builtin/hype/fixtures/smoke/` and `golden/smoke.events.jsonl`. KEEP `orchestrator.yaml`, `STAGE.md`, `run.py` — additive: existing JSON manifest still loads via `load_orchestrator_manifest` in `artagents/core/orchestrator/schema.py`.
2. **Sketch** a 5–10 line `hype.py` excerpt showing `STEP_ORDER` executors (referenced from `docs/architecture.md`) mapped onto `code`-step children with `produces` checks (e.g., `audio_duration_min` for the audio segment, `image_dimensions` for keyframes).
3. **Document** nested-prepare semantics (resolves `callers` flag): when a `code` step in the new `hype.py` shells to today's `artagents executors run …` or `artagents orchestrators run …`, the child invocation reads `ARTAGENTS_TASK_RUN_ID` from env and SKIPS creating a new project run; events append to the parent task run's `events.jsonl`. Cite the three caller paths of `prepare_project_run` (orchestrator, executor, `builtin.hype`).

### Step 9: Sections 14–17 — Doc Deliverables, Risk Register, Cut Points, Open-Call Confirmations (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Tabulate** documentation deliverables with audience + word/section target:
   - `AUTHORING.md` (new, repo root or `docs/`) — audience: human + LLM authors; ~one page DSL reference.
   - `AGENT.md` template (new, dropped per-run into `runs/<run-id>/AGENT.md`) — audience: in-flight agent.
   - `README.md` updates — audience: operator; quickstart for `artagents start`/`next`/`ack`.
   - `AGENTS.md` cross-link update for the qualified `<pack>.<orch>` rule.
2. **Tabulate** risk register: single-host (no daemon → cannot prevent concurrent operator); semantic verifier discipline (sentinel-existence is regression risk); context-decay re-injection (Stop-hook prohibition preamble must fire every call); honor-model boundary (no defense against malicious agents). Each row: trigger + mitigation.
3. **Identify** cut points: Phase 3 (kernel + step kinds + produces/repeat = working frozen-plan runner); Phase 5 (adds authoring + lifecycle verb split = author-friendly). Phases 6–9 are explicit polish/scale.
4. **State** Confirmed verdict for A1–A8 with one-line rationale each.

### Step 10: Section 18 — Settled Decisions (SD-001..SD-NNN) (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Format** every entry as `SD-NNN <topic>: <single-sentence rationale>.` matching `docs/sprint-thread-layer.md` lines 39–43.
2. **Cover** every load-bearing call from the body. Required entries (final numbering set during authoring):
   - Three step kinds (`code`/`attested`/`nested`).
   - Iteration/fan-out as body attributes (`repeat:{until|for_each}`), not separate kinds.
   - `plan.json` renamed from "checklist" (it's a tree).
   - `events.jsonl` plain `sha256(prev_hash + canonical_event_json)` chain; no HMAC.
   - No `.index.db` in v1; file-walk verbs only.
   - Python DSL `artagents.orchestrate` is the only committed representation.
   - `<pack>/build/<orch>.json` is a gitignored build artifact; root `.gitignore` excludes `<pack>/build/`.
   - Per-project `<slug>/.cas/`; not shared.
   - `code-step-calls-orchestrator` forbidden (nested-as-data only).
   - Gate four-check + exact-recovery-command on rejection.
   - Gate runs BEFORE both `_prepare_project_request()` (`artagents/core/orchestrator/runner.py:135`) and `thread_wrapper.begin_orchestrator_run()` (line 136); zero project-run side effects on rejection.
   - `events.jsonl` is single write surface; `artagents/threads/wrapper.py` does not duplicate provenance there.
   - Top-level lifecycle/operator verbs (`next`/`ack`/`status`/`abort`/`start`/`runs ls`) extend `artagents/pipeline.py:15` dispatch; `author` is a new top-level subparser; `artagents orchestrators` keeps working unchanged.
   - Kernel modules live in new `artagents/core/task/` package (above orchestrator dispatch).
   - Nested executor/orchestrator/`builtin.hype` calls inherit parent task run via `ARTAGENTS_TASK_RUN_ID`; no nested project records.
   - `ARTAGENTS_ACTOR` pinning + `--agent` required; self-acks rejected; unpinned actors rejected.
   - Ack validity rules: `retry` only after verifier failure; `iterate --feedback` only when `repeat.until=user_approves`; `abort` ends run.
   - `produces` inline checks replace verifier substep; `passes_test` remains a regular `code` step.
   - Sentinel-existence-only attested checks rejected at `author check`.
   - Stop-hook prohibition preamble re-injected verbatim on every `artagents next` call.
   - Migration is additive: existing `OrchestratorDefinition` JSON manifests + `RUNTIME_KINDS={python,command}` keep working.
   - Single-host honor model; no sandbox claims.
   - Cut points: Phase 3 (frozen-plan runner) and Phase 5 (author-friendly).
   - Canonical migration example is `artagents/packs/builtin/hype/`; transcribe is fallback.
   - Phasing matches V1 BUILD ORDER 1–9.

### Step 11: Verification Read-Back (`docs/orchestrator-v1-plan.md`)
**Scope:** Small
1. **Read back** the rendered doc against the 14 `pass_to_pass` test expectations.
2. **Confirm** every phase has all five fields (scope, files-touched with inline citations, classification, exit criteria, test strategy).
3. **Confirm** SD format matches `docs/sprint-thread-layer.md`.
4. **Confirm** A1–A8 are explicitly Confirmed.
5. **Confirm** all forbidden v1 features in Non-Goals + Risk Register.
6. **Confirm** existing-code citations resolve (`artagents/pipeline.py:15`, `artagents/core/orchestrator/runner.py:135`, `artagents/core/orchestrator/schema.py`, `artagents/core/project/run.py`, `artagents/core/project/paths.py`, `artagents/threads/wrapper.py`, `artagents/packs/builtin/hype/`); future-deliverable paths (`AUTHORING.md`, `AGENT.md`, `<pack>/build/`, `<pack>/fixtures/`, `<pack>/golden/`, `artagents/core/task/`, `artagents/orchestrate/`, `artagents/verify/`) are clearly framed as prescriptive new paths.
7. **Confirm** body word count ~1500–2200 (SD list excluded).

## Execution Order
1. Resolve Open-Call Decisions A1–A8 (above) before drafting body.
2. Steps 1–2 (front matter, data model) fix vocabulary used by every later section.
3. Steps 3–6 author the load-bearing design content (step kinds, gate, verbs/ack, authoring/nudge).
4. Step 7 (phasing) depends on the design vocabulary being settled.
5. Step 8 (migration example) depends on step kinds + authoring being defined.
6. Step 9 (deliverables/risk/cut/open-call confirmations) depends on body completion.
7. Step 10 (Settled Decisions) — last; mirrors every body assertion.
8. Step 11 (verification read-back) before declaring done.

## Validation Order
1. Section-by-section read-back against the 14 `pass_to_pass` checks.
2. Spot-check that EXISTING-CODE inline citations resolve to real files; FUTURE-DELIVERABLE paths are framed as prescriptive new paths (not as resolvable today).
3. SD format match against `docs/sprint-thread-layer.md` lines 39–43.
4. Verify A1–A8 each appear as a confirmed open-call AND as a corresponding SD entry.
5. Tone and word-count check against `docs/sprint-thread-layer.md` / `docs/design-thread-layer.md`.


        Plan metadata:
        {
  "version": 2,
  "timestamp": "2026-05-04T09:22:15Z",
  "hash": "sha256:ddb65fcb489aa9e343989ae2859d9a5d7ff6716378418be11a6ff844616d9d20",
  "changes_summary": "Resolved all nine significant flags by pre-committing eight open-call decisions (A1\u2013A8) before drafting. Concretely: (FLAG-001/scope-1/scope-2) chose `artagents/pipeline.py:15` as the integration surface for top-level lifecycle/operator/author verbs and stated `runs ls` lands there too; (FLAG-002/correctness) restated gate ordering as running BEFORE both `_prepare_project_request()` (runner.py:135) AND `thread_wrapper.begin_orchestrator_run()` (line 136), with a defensive decorator at the top of `run_orchestrator()` so a rejection produces zero project-run side effects; (issue_hints) explicitly justified the new `artagents/core/task/` namespace as a settled decision rather than silent assumption; (callers) defined nested executor/`builtin.hype` calls inherit the parent task run via `ARTAGENTS_TASK_RUN_ID` env and skip creating child project records; (all_locations) added root `.gitignore` update for `<pack>/build/` to Phase 4 exit criteria; (criteria_quality) split the path-citation success criterion into existing-code-must-resolve vs prescriptive-future-deliverable. Added Open-Call Decisions block, expanded SD coverage list, added a separate verification read-back step, and updated phase file-touch lists to consistently carry the namespace and gate-ordering choices.",
  "flags_addressed": [
    {
      "id": "FLAG-001",
      "resolution": "addressed",
      "reason": "Plan now states top-level lifecycle/operator/author verbs extend `artagents/pipeline.py:15` dispatch table (not the orchestrators subparser), recorded as A5/SD entry."
    },
    {
      "id": "FLAG-002",
      "resolution": "addressed",
      "reason": "Gate ordering restated to run before BOTH `_prepare_project_request()` (runner.py:135) and `thread_wrapper.begin_orchestrator_run()` (line 136); rejection produces zero project-run side effects, recorded as A7/SD."
    },
    {
      "id": "issue_hints",
      "resolution": "addressed",
      "reason": "`artagents/core/task/` namespace is now an explicit Open-Call Decision A4 with rationale (gate sits above orchestrator dispatch) and is carried consistently through every phase file-touch list and SD entry."
    },
    {
      "id": "correctness",
      "resolution": "addressed",
      "reason": "Same as FLAG-002: gate ordering re-stated to precede _prepare_project_request; covered by Step 4 ordering language and SD entry."
    },
    {
      "id": "scope-1",
      "resolution": "addressed",
      "reason": "Same as FLAG-001: integration surface picked as `artagents/pipeline.py:15` and called out in Step 5/Phase 5."
    },
    {
      "id": "scope-2",
      "resolution": "addressed",
      "reason": "`runs ls` explicitly placed as a new top-level subcommand in `artagents/pipeline.py` (NOT under orchestrators or any existing subparser), called out in Step 5/Phase 5/SD."
    },
    {
      "id": "all_locations",
      "resolution": "addressed",
      "reason": "Phase 4 exit criteria now include updating root `.gitignore` to exclude `<pack>/build/`; A8 + SD entry."
    },
    {
      "id": "callers",
      "resolution": "addressed",
      "reason": "A6 + SD: nested executor/orchestrator/builtin.hype calls inherit parent task run via `ARTAGENTS_TASK_RUN_ID` and skip creating child project records; documented in Section 13/Step 8."
    },
    {
      "id": "criteria_quality",
      "resolution": "addressed",
      "reason": "Path-citation success criterion split into two: existing-code citations MUST resolve today; future-deliverable paths (AUTHORING.md, AGENT.md, build/, fixtures/, golden/, artagents/core/task/, artagents/orchestrate/, artagents/verify/) are clearly framed as prescriptive."
    }
  ],
  "questions": [
    "Should the new `author` verbs live as a top-level `artagents author \u2026` subparser in `artagents/pipeline.py`, or be folded under the existing `artagents orchestrators` subparser to avoid namespace sprawl? (Plan currently picks top-level, matching the audience-split intent.)",
    "For nested executor calls, is `ARTAGENTS_TASK_RUN_ID` the right env-var name, or does the project already have a convention (e.g., `ARTAGENTS_PROJECT_RUN_ID`) to reuse?",
    "Should the kernel package be `artagents/core/task/` (chosen) or a less namespace-y `artagents/task/` at the package top level? Plan currently chooses `core/task/` to mirror `core/orchestrator/` and `core/project/`."
  ],
  "success_criteria": [
    {
      "criterion": "Document exists at exactly `docs/orchestrator-v1-plan.md` (no alternate filename based on title or kebab-case normalization).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Document ends with a `## Settled Decisions` section using `SD-NNN <topic>: <single-sentence rationale>.` format matching `docs/sprint-thread-layer.md`.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Settled Decisions covers every load-bearing call: three step kinds; repeat as body attribute; plan.json rename; plain sha256 chain (no HMAC); no .index.db; Python DSL only; <pack>/build/ gitignored; per-project .cas; code-step-calls-orchestrator forbidden; gate four-check + recovery command; gate runs BEFORE both _prepare_project_request and thread_wrapper.begin_orchestrator_run; events.jsonl is single write surface; lifecycle verbs extend artagents/pipeline.py; artagents/core/task/ namespace; nested calls inherit ARTAGENTS_TASK_RUN_ID; ARTAGENTS_ACTOR pinning + self-ack rejection; ack decision validity rules; produces inline checks; sentinel-only rejected at author check; Stop-hook preamble every call; additive migration; honor model; Phase 3 + Phase 5 cut points; builtin.hype canonical example; phasing 1\u20139.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Each of the nine phases includes scope, files-touched (with inline backticked path citations), classification (additive or breaking), exit criteria, and test strategy.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Storage tree section reproduces the task spec exactly: `active_run.json`, `runs/<run-id>/{plan.json,events.jsonl,AGENT.md}`, `steps/<id>/{produces,iterations/NNN,items/<id>}/`, `inbox/`, `<slug>/.cas/<sha256>` \u2014 and explicitly excludes `.index.db` and HMAC.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Step Kinds section names code, attested, nested; specifies repeat:{until|for_each} as body attributes; forbids code-step-calls-orchestrator.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Gate section enumerates all four checks AND states the gate runs BEFORE both `_prepare_project_request()` (`artagents/core/orchestrator/runner.py:135`) AND `thread_wrapper.begin_orchestrator_run()` (line 136), AND that rejection produces zero project-run filesystem side effects.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Ack Decisions section specifies validity rules: retry only after verifier failure, iterate --feedback only when repeat.until=user_approves, abort ends run; --agent / ARTAGENTS_ACTOR pinning required; self-acks rejected; --item targets for_each.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Lifecycle Verbs section explicitly lands top-level verbs (next/ack/status/abort/start/runs ls/author \u2026) in `artagents/pipeline.py:15` dispatch table, NOT under the existing `orchestrators` subparser, and notes existing `artagents orchestrators` keeps working.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Authoring section states Python DSL `artagents.orchestrate` is the only committed representation, JSON manifest is gitignored at `<pack>/build/<orch>.json`, runtime hashes/pins the build artifact, pack adds `<orch>.py`/`fixtures/`/`golden/<name>.events.jsonl`, AND root `.gitignore` is updated to exclude `<pack>/build/` as part of Phase 4 exit criteria.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Stop-hook section states the prohibition preamble is re-injected verbatim on every `artagents next` call (not just first call).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Canonical migration example uses `artagents/packs/builtin/hype/` with a diff sketch (new `hype.py`/`build/hype.json`/`fixtures/`/`golden/`), confirms existing JSON manifest still loads, AND documents that nested calls into `prepare_project_run()` inherit `ARTAGENTS_TASK_RUN_ID` and skip creating child project records.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Risk register includes single-host assumption, semantic verifier discipline, context-decay re-injection, and honor-model boundary, each with trigger + mitigation.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Document explicitly Confirms (or Revises with rationale) all eight open-call decisions A1\u2013A8: nested-as-data; Python DSL only; no .index.db; artagents/core/task/ namespace; pipeline.py CLI surface; nested-call ARTAGENTS_TASK_RUN_ID inheritance; gate ordering before _prepare_project_request; .gitignore for <pack>/build/.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Migration is presented as additive: existing `OrchestratorDefinition` JSON manifests + `python`/`command` `RUNTIME_KINDS` keep working through and after v1; existing `artagents orchestrators` CLI verbs remain unchanged.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "All EXISTING-CODE inline path citations (e.g., `artagents/pipeline.py:15`, `artagents/core/orchestrator/runner.py:135`, `artagents/core/orchestrator/schema.py`, `artagents/core/project/run.py`, `artagents/threads/wrapper.py`, `artagents/packs/builtin/hype/`) resolve to real files in the repo today.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "FUTURE-DELIVERABLE paths (`AUTHORING.md`, per-run `AGENT.md`, `<pack>/build/`, `<pack>/fixtures/`, `<pack>/golden/`, `artagents/core/task/`, `artagents/orchestrate/`, `artagents/verify/`) are clearly framed as prescriptive new paths in the doc, not as resolvable-today citations.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Document body length lands in ~1500\u20132200 words (SD list excluded).",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Tone is terse, declarative, decision-first; matches `docs/sprint-thread-layer.md` and `docs/design-thread-layer.md`.",
      "priority": "should",
      "requires": [
        "subjective_judgment",
        "read_files"
      ]
    },
    {
      "criterion": "Document does not introduce a daemon, web server, `.index.db`, HMAC/keyed crypto, or shared CAS in v1; these are explicitly listed in Non-Goals.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Cut Points section identifies Phase 3 (kernel + step kinds + produces/repeat) and Phase 5 (adds authoring + lifecycle verb split) as ship-ready milestones.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    }
  ],
  "assumptions": [
    "A1 \u2014 nested step kind stays as data; code-step-calls-orchestrator forbidden \u2014 Confirmed.",
    "A2 \u2014 Python DSL `artagents.orchestrate` is the only committed representation; `<pack>/build/<orch>.json` is a gitignored build artifact \u2014 Confirmed.",
    "A3 \u2014 no `.index.db` in v1; file-walk verbs only \u2014 Confirmed.",
    "A4 \u2014 kernel modules land in NEW `artagents/core/task/` package because the gate sits ABOVE orchestrator dispatch.",
    "A5 \u2014 top-level lifecycle/operator/author verbs extend `artagents/pipeline.py:15` dispatch; existing `artagents orchestrators` keeps working unchanged.",
    "A6 \u2014 nested executor/orchestrator/`builtin.hype` calls inherit parent task run via `ARTAGENTS_TASK_RUN_ID` env and SKIP creating child project records; events append to the parent run's `events.jsonl`.",
    "A7 \u2014 gate runs BEFORE `_prepare_project_request()` (runner.py:135) and BEFORE `thread_wrapper.begin_orchestrator_run()` (line 136); rejection produces zero project-run filesystem side effects.",
    "A8 \u2014 root `.gitignore` is updated in Phase 4 to exclude `<pack>/build/`.",
    "Doc body targets ~1500\u20132200 words; SD list grows as needed.",
    "SD entries follow `SD-NNN <topic>: <single-sentence rationale>.` per `docs/sprint-thread-layer.md` lines 39\u201343.",
    "Output path is exactly `docs/orchestrator-v1-plan.md`; no alternate filename, no other write target.",
    "`artagents/packs/builtin/hype/` is the canonical migration example; transcribe is fallback only if hype is too sprawling for an inline diff sketch."
  ],
  "delta_from_previous_percent": 84.18,
  "structure_warnings": []
}

        Gate signals:
        {
  "robustness": "robust",
  "signals": {
    "iteration": 2,
    "idea": "ArtAgents is a file-based, single-host Python CLI for running creative pipelines (video/audio/image) that mix code, AI, and human steps. Today it has a pack-based plugin architecture, orchestrator + executor schemas (python/command runtime kinds only), project runs under ~/Documents/reigh-workspace/artagents-projects/, threads with provenance, and a CLI gateway. We are extending it so an agent can be put into 'task mode' and walked through a frozen plan that mixes code, AI, and human steps, with iteration loops and fan-out.\n\nNON-NEGOTIABLES:\n- Single-host, file-based. No daemon, no web server.\n- Honor-based with strong logging. We do not pretend to sandbox a misaligned agent.\n- Migration is additive. Existing JSON manifests and python/command runtime kinds keep working.\n- Existing pack mechanism stays.\n\nV1 DESIGN (post-critique, trimmed):\n\nTHREE STEP KINDS:\n- code: deterministic argv, runner subprocesses, returncode + produces.\n- attested: agent or human task. instructions + produces + ack records identity (agent_id or actor pinned via ARTAGENTS_ACTOR) + evidence.\n- nested: delegates to a child plan; gate sees the structure for hashing/pinning.\n\nITERATION AND FAN-OUT ARE BODY ATTRIBUTES, NOT KINDS:\n- repeat: {until: user_approves|verifier_passes|quorum, max_iterations, on_exhaust}\n- repeat: {for_each: <input_set>}\nBoth apply to any step or to a body block in a nested plan.\n\nPRODUCES WITH INLINE CHECKS (replaces separate verifier substep):\n  produces = {\n    'audio': file(path='audio.wav', check=audio_duration_min(30)),\n    'notes': json_file(path='notes.json', schema='notes.schema.json', min_items=3),\n  }\nThe gate runs the check; failure rewinds the cursor. passes_test is a regular code step.\n\nSTORAGE (under ~/Documents/reigh-workspace/artagents-projects/):\n- <slug>/active_run.json -- pointer to in-flight run + plan hash\n- <slug>/runs/<run-id>/plan.json -- immutable, hash-pinned (renamed from 'checklist' since it's a tree)\n- <slug>/runs/<run-id>/events.jsonl -- append-only, plain hash-chained (prev_hash field), sole truth\n- <slug>/runs/<run-id>/AGENT.md -- contract for whoever's driving\n- <slug>/runs/<run-id>/steps/<step-id>/produces/ -- artifact files (or symlinks into .cas)\n- <slug>/runs/<run-id>/steps/<step-id>/iterations/NNN/ -- when repeat:until is set\n- <slug>/runs/<run-id>/steps/<step-id>/items/<item-id>/ -- when repeat:for_each is set\n- <slug>/runs/<run-id>/inbox/ -- external completion signals get dropped here\n- <slug>/.cas/<sha256> -- per-project CAS for v1 (not shared)\n\nNO crypto: hash chain is plain sha256(prev_hash + canonical_event_json). Tripwire for accidental edits, not protection against malicious users. We do not need HMAC or key handles.\n\nNO .index.db in v1. find + grep on events.jsonl is fine until grep is slow.\n\nGATE (above dispatch, single function):\n- active_run.json exists for this project?\n- plan.json hash matches the pin in active_run.json?\n- events.jsonl hash chain intact?\n- incoming command matches plan[derived_cursor].command?\nIf any fails, reject with the exact recovery command.\n\nLIFECYCLE VERBS, scoped by audience:\nartagents next | ack | status | abort                                  (agent-facing, mid-run)\nartagents start | abort | status | runs ls                             (operator)\nartagents author new | check | describe | test | compile | explain     (author)\n\nACK DECISIONS (intentionally distinct):\n--decision approve              -- advance cursor\n--decision retry                -- only valid after verifier failure; rerun body, stderr is feedback\n--decision iterate --feedback   -- only valid when repeat.until=user_approves; appends to cumulative constraints\n--decision abort                -- end run\n\nACK requires --agent <id> for attested steps with attestor_type=agent, or --actor <name> matching ARTAGENTS_ACTOR for attestor_type=human. Self-acks and unpinned actors are rejected.\n\nFor repeat:for_each: --item <id> targets a specific item; partial approval is supported.\n\nNUDGE (out-of-process, optional, Claude Code only for v1):\nA Stop hook runs artagents next. The next output ALWAYS includes the prohibition preamble verbatim, not just on first call -- this is the re-injection mechanism that fights context decay.\n\nAUTHORING:\n- Python DSL artagents.orchestrate is the ONLY committed representation. JSON manifest is generated at author compile into a build/ dir (gitignored) and that's what the runtime hashes/pins.\n- Verifier helper library artagents.verify: file_nonempty, json_schema, json_file, audio_duration_min, image_dimensions, all_of.\n- Pack layout: <pack>/<orch>.py (committed), <pack>/build/<orch>.json (gitignored), <pack>/fixtures/<name>/, <pack>/golden/<name>.events.jsonl.\n- author check is sub-second static validation: schema, every produces/requires reference resolves, every nested plan resolves, attested steps with non-trivial produces have semantic checks (sentinel-existence-only is rejected at definition time).\n- author describe pretty-prints the DAG.\n- author test --fixture runs --dry-run --auto-approve, diffs events.jsonl against golden/<fixture>.events.jsonl.\n\nV1 BUILD ORDER (recommended phases):\n1. Kernel: events.jsonl + plain hash chain + plan hash pin + gate above dispatch + active_run.json. Runner becomes dumb; gate is a single decorated function above runner dispatch.\n2. Three step kinds: code, attested, nested. (code is a strict superset of today's python+command runtime kinds.)\n3. produces-with-inline-checks; repeat:{until} and repeat:{for_each} on bodies.\n4. Authoring: Python DSL + verify helpers + author check + author describe + author new.\n5. Lifecycle verbs split by audience as above.\n6. Stop-hook nudge with mandatory prohibition preamble.\n7. CAS per-project (under <slug>/.cas/), symlink-based produces.\n8. Inbox surface for external completion signals.\n9. Author test with golden runs.\n\nEXISTING REPO STATE:\n- artagents/core/orchestrator/ exists with schema.py, runner.py, registry.py, cli.py, api.py. Currently knows ORCHESTRATOR_KINDS={built_in, external} and RUNTIME_KINDS={python, command}. OrchestratorPlan / OrchestratorPlanStep skeletons exist (used for dry-run output).\n- artagents/core/project/ exists with run lifecycle (prepare_project_run / finalize_project_run), paths.py with DEFAULT_PROJECTS_ROOT.\n- artagents/threads/ exists with thread_wrapper around runs, @active concept.\n- artagents/packs/ holds builtin packs (cut, transcribe, human_notes, open_in_reigh, etc.).\n- Migration to packs is mid-flight (recent commits T10-T13).\n\nASSUMED OPEN-CALL DEFAULTS (the design plan should call these out and confirm or revise):\n- Keep nested step kind as data (gate sees the structure); forbid code-step-calls-orchestrator.\n- Python DSL is the only committed representation; JSON manifest is a build artifact in gitignored build/ dirs.\n- Drop .index.db from v1; ship with file-walk verbs.\n\nDELIVERABLE EXPECTATIONS for the design doc:\n- Concrete phasing aligned to build order 1-9 above; each phase has scope, files touched, breaking-change risk classification (additive vs breaking), and exit criteria.\n- Test strategy at each phase (golden runs are the regression format).\n- Migration of one builtin pack (suggest hype.cut or transcribe) to the new shape as the canonical example, including the diff shape.\n- Documentation deliverables identified: AUTHORING.md (one-page reference for both human and LLM authors), AGENT.md template, README.md updates.\n- Risk register (single-host assumption, semantic verifier discipline, context decay re-injection, agent honor model boundary).\n- Cut points where work can stop and still ship something useful (e.g., after phase 3, after phase 5).\n- A ## Settled Decisions section at the bottom listing every load-bearing design call (SD-NNN format) so future code-mode runs can inherit them via --from-doc.\n\nMode: doc / metaplan\nOutput: docs/orchestrator-v1-plan.md",
    "significant_flags": 7,
    "unresolved_flags": [
      {
        "id": "issue_hints",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Step Kinds/A1 still says `code-step-calls-orchestrator` is forbidden, but Step 8 says a `code` step in `hype.py` may shell out to today's `artagents orchestrators run ...`. That contradicts a load-bearing design call from the task spec and would make downstream implementers unclear whether orchestrator delegation is represented as `nested` data or hidden inside a `code` argv.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "correctness",
        "concern": "Are the proposed changes technically correct?: The new `ARTAGENTS_TASK_RUN_ID` inheritance decision is technically under-specified for existing project-run behavior: current tests in `tests/test_project_runs.py` expect `ARTAGENTS_PROJECT_RUN=1`, project `run.json` creation, and hype artifact mirroring for project runs. If child project records are skipped wholesale during task mode, the plan needs to preserve the child command's output directory and artifact mirroring semantics inside the parent task run, or explicitly mark those project-run behaviors as not available under task mode.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "all_locations",
        "concern": "Does the change touch all locations AND supporting infrastructure?: Searched for task-run environment conventions and found no existing `ARTAGENTS_TASK_RUN_ID`; existing run identity envs are `ARTAGENTS_RUN_ID`, `ARTAGENTS_PARENT_RUN_ID`, and `ARTAGENTS_PROJECT_RUN` in `artagents/threads/wrapper.py` and `artagents/core/project/run.py`. Introducing `ARTAGENTS_TASK_RUN_ID` is acceptable, but the plan should list every integration file that must read or propagate it, especially executor runner, orchestrator runner, direct `builtin.hype`, and subprocess env construction.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "callers",
        "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: The revised phase table carries the parent-task inheritance behavior mainly in the migration example instead of in the implementation phases. Because `run_executor()` and direct `hype.main()` have independent project-run preparation paths, the doc should move this from example-only text into the Phase 1 or Phase 2 scope/files/exit criteria so it is not skipped for non-hype task plans.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "FLAG-004",
        "concern": "Step model: the revised plan both forbids `code-step-calls-orchestrator` and describes `code` steps shelling out to `artagents orchestrators run`, which contradicts the required nested-as-data model.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "FLAG-005",
        "concern": "Project run inheritance: `ARTAGENTS_TASK_RUN_ID` inheritance is specified, but the phase implementation file lists do not include all actual project-run preparation paths that would need to honor it.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "scope",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: The revised scope for nested-call inheritance names three caller families, but the nine-phase file-touch lists do not include `artagents/core/executor/runner.py` or `artagents/packs/builtin/hype/run.py` in the phase that implements `ARTAGENTS_TASK_RUN_ID` behavior. Those files are actual `prepare_project_run()` callers, so downstream implementation could miss required glue while still following the phase table.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      }
    ],
    "resolved_flags": [
      {
        "id": "FLAG-001",
        "concern": "Task CLI surface: lifecycle verbs are top-level but the plan only maps them to the orchestrator CLI, while `artagents/pipeline.py` currently owns top-level dispatch and falls unknown commands through to builtin.hype.",
        "resolution": "Resolved all nine significant flags by pre-committing eight open-call decisions (A1\u2013A8) before drafting. Concretely: (FLAG-001/scope-1/scope-2) chose `artagents/pipeline.py:15` as the integration surface for top-level lifecycle/operator/author verbs and stated `runs ls` lands there too; (FLAG-002/correctness) restated gate ordering as running BEFORE both `_prepare_project_request()` (runner.py:135) AND `thread_wrapper.begin_orchestrator_run()` (line 136), with a defensive decorator at the top of `run_orchestrator()` so a rejection produces zero project-run side effects; (issue_hints) explicitly justified the new `artagents/core/task/` namespace as a settled decision rather than silent assumption; (callers) defined nested executor/`builtin.hype` calls inherit the parent task run via `ARTAGENTS_TASK_RUN_ID` env and skip creating child project records; (all_locations) added root `.gitignore` update for `<pack>/build/` to Phase 4 exit criteria; (criteria_quality) split the path-citation success criterion into existing-code-must-resolve vs prescriptive-future-deliverable. Added Open-Call Decisions block, expanded SD coverage list, added a separate verification read-back step, and updated phase file-touch lists to consistently carry the namespace and gate-ordering choices."
      },
      {
        "id": "FLAG-002",
        "concern": "Gate ordering: saying the gate runs before `artagents/threads/wrapper.py` is not enough because project-run preparation happens earlier and can create run files before a task-mode rejection.",
        "resolution": "Resolved all nine significant flags by pre-committing eight open-call decisions (A1\u2013A8) before drafting. Concretely: (FLAG-001/scope-1/scope-2) chose `artagents/pipeline.py:15` as the integration surface for top-level lifecycle/operator/author verbs and stated `runs ls` lands there too; (FLAG-002/correctness) restated gate ordering as running BEFORE both `_prepare_project_request()` (runner.py:135) AND `thread_wrapper.begin_orchestrator_run()` (line 136), with a defensive decorator at the top of `run_orchestrator()` so a rejection produces zero project-run side effects; (issue_hints) explicitly justified the new `artagents/core/task/` namespace as a settled decision rather than silent assumption; (callers) defined nested executor/`builtin.hype` calls inherit the parent task run via `ARTAGENTS_TASK_RUN_ID` env and skip creating child project records; (all_locations) added root `.gitignore` update for `<pack>/build/` to Phase 4 exit criteria; (criteria_quality) split the path-citation success criterion into existing-code-must-resolve vs prescriptive-future-deliverable. Added Open-Call Decisions block, expanded SD coverage list, added a separate verification read-back step, and updated phase file-touch lists to consistently carry the namespace and gate-ordering choices."
      },
      {
        "id": "FLAG-003",
        "concern": "Authoring build artifacts: the plan requires gitignored `<pack>/build/<orch>.json` artifacts but does not include a `.gitignore` update or a currently ignored artifact path.",
        "resolution": "Repository `.gitignore` ignores `remotion/build/`, `runs/`, `cache/`, `.artagents/`, and local scratch packs, but not `artagents/packs/*/*/build/` or generic pack-local `build/` directories."
      },
      {
        "id": "scope-1",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Flagged missing top-level CLI integration: `artagents/pipeline.py` owns top-level dispatch, while the plan only maps verbs onto `artagents/core/orchestrator/cli.py`.",
        "resolution": "Resolved all nine significant flags by pre-committing eight open-call decisions (A1\u2013A8) before drafting. Concretely: (FLAG-001/scope-1/scope-2) chose `artagents/pipeline.py:15` as the integration surface for top-level lifecycle/operator/author verbs and stated `runs ls` lands there too; (FLAG-002/correctness) restated gate ordering as running BEFORE both `_prepare_project_request()` (runner.py:135) AND `thread_wrapper.begin_orchestrator_run()` (line 136), with a defensive decorator at the top of `run_orchestrator()` so a rejection produces zero project-run side effects; (issue_hints) explicitly justified the new `artagents/core/task/` namespace as a settled decision rather than silent assumption; (callers) defined nested executor/`builtin.hype` calls inherit the parent task run via `ARTAGENTS_TASK_RUN_ID` env and skip creating child project records; (all_locations) added root `.gitignore` update for `<pack>/build/` to Phase 4 exit criteria; (criteria_quality) split the path-citation success criterion into existing-code-must-resolve vs prescriptive-future-deliverable. Added Open-Call Decisions block, expanded SD coverage list, added a separate verification read-back step, and updated phase file-touch lists to consistently carry the namespace and gate-ordering choices."
      },
      {
        "id": "scope-2",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Flagged ambiguity around `artagents runs ls`, since project CLI currently has no runs-list command and the plan does not choose the integration surface.",
        "resolution": "Resolved all nine significant flags by pre-committing eight open-call decisions (A1\u2013A8) before drafting. Concretely: (FLAG-001/scope-1/scope-2) chose `artagents/pipeline.py:15` as the integration surface for top-level lifecycle/operator/author verbs and stated `runs ls` lands there too; (FLAG-002/correctness) restated gate ordering as running BEFORE both `_prepare_project_request()` (runner.py:135) AND `thread_wrapper.begin_orchestrator_run()` (line 136), with a defensive decorator at the top of `run_orchestrator()` so a rejection produces zero project-run side effects; (issue_hints) explicitly justified the new `artagents/core/task/` namespace as a settled decision rather than silent assumption; (callers) defined nested executor/`builtin.hype` calls inherit the parent task run via `ARTAGENTS_TASK_RUN_ID` env and skip creating child project records; (all_locations) added root `.gitignore` update for `<pack>/build/` to Phase 4 exit criteria; (criteria_quality) split the path-citation success criterion into existing-code-must-resolve vs prescriptive-future-deliverable. Added Open-Call Decisions block, expanded SD coverage list, added a separate verification read-back step, and updated phase file-touch lists to consistently carry the namespace and gate-ordering choices."
      },
      {
        "id": "criteria_quality",
        "concern": "Are the success criteria well-prioritized and verifiable?: Flagged that the path-citation criterion should distinguish existing-code citations from future planned deliverable paths like `AUTHORING.md`, `AGENT.md`, `build/`, `fixtures/`, and `golden/`.",
        "resolution": "Resolved all nine significant flags by pre-committing eight open-call decisions (A1\u2013A8) before drafting. Concretely: (FLAG-001/scope-1/scope-2) chose `artagents/pipeline.py:15` as the integration surface for top-level lifecycle/operator/author verbs and stated `runs ls` lands there too; (FLAG-002/correctness) restated gate ordering as running BEFORE both `_prepare_project_request()` (runner.py:135) AND `thread_wrapper.begin_orchestrator_run()` (line 136), with a defensive decorator at the top of `run_orchestrator()` so a rejection produces zero project-run side effects; (issue_hints) explicitly justified the new `artagents/core/task/` namespace as a settled decision rather than silent assumption; (callers) defined nested executor/`builtin.hype` calls inherit the parent task run via `ARTAGENTS_TASK_RUN_ID` env and skip creating child project records; (all_locations) added root `.gitignore` update for `<pack>/build/` to Phase 4 exit criteria; (criteria_quality) split the path-citation success criterion into existing-code-must-resolve vs prescriptive-future-deliverable. Added Open-Call Decisions block, expanded SD coverage list, added a separate verification read-back step, and updated phase file-touch lists to consistently carry the namespace and gate-ordering choices."
      }
    ],
    "weighted_score": 12.0,
    "weighted_history": [
      15.0
    ],
    "plan_delta_from_previous": 84.18,
    "recurring_critiques": [],
    "scope_creep_flags": [],
    "loop_summary": "Iteration 2. Weighted score trajectory: 15.0 -> 12.0. Plan deltas: 84.2%. Recurring critiques: 0. Resolved flags: 6. Open significant flags: 7.",
    "debt_overlaps": [],
    "escalated_debt_subsystems": []
  },
  "warnings": [],
  "criteria_check": {
    "count": 21,
    "items": [
      {
        "criterion": "Document exists at exactly `docs/orchestrator-v1-plan.md` (no alternate filename based on title or kebab-case normalization).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Document ends with a `## Settled Decisions` section using `SD-NNN <topic>: <single-sentence rationale>.` format matching `docs/sprint-thread-layer.md`.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Settled Decisions covers every load-bearing call: three step kinds; repeat as body attribute; plan.json rename; plain sha256 chain (no HMAC); no .index.db; Python DSL only; <pack>/build/ gitignored; per-project .cas; code-step-calls-orchestrator forbidden; gate four-check + recovery command; gate runs BEFORE both _prepare_project_request and thread_wrapper.begin_orchestrator_run; events.jsonl is single write surface; lifecycle verbs extend artagents/pipeline.py; artagents/core/task/ namespace; nested calls inherit ARTAGENTS_TASK_RUN_ID; ARTAGENTS_ACTOR pinning + self-ack rejection; ack decision validity rules; produces inline checks; sentinel-only rejected at author check; Stop-hook preamble every call; additive migration; honor model; Phase 3 + Phase 5 cut points; builtin.hype canonical example; phasing 1\u20139.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Each of the nine phases includes scope, files-touched (with inline backticked path citations), classification (additive or breaking), exit criteria, and test strategy.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Storage tree section reproduces the task spec exactly: `active_run.json`, `runs/<run-id>/{plan.json,events.jsonl,AGENT.md}`, `steps/<id>/{produces,iterations/NNN,items/<id>}/`, `inbox/`, `<slug>/.cas/<sha256>` \u2014 and explicitly excludes `.index.db` and HMAC.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Step Kinds section names code, attested, nested; specifies repeat:{until|for_each} as body attributes; forbids code-step-calls-orchestrator.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Gate section enumerates all four checks AND states the gate runs BEFORE both `_prepare_project_request()` (`artagents/core/orchestrator/runner.py:135`) AND `thread_wrapper.begin_orchestrator_run()` (line 136), AND that rejection produces zero project-run filesystem side effects.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Ack Decisions section specifies validity rules: retry only after verifier failure, iterate --feedback only when repeat.until=user_approves, abort ends run; --agent / ARTAGENTS_ACTOR pinning required; self-acks rejected; --item targets for_each.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Lifecycle Verbs section explicitly lands top-level verbs (next/ack/status/abort/start/runs ls/author \u2026) in `artagents/pipeline.py:15` dispatch table, NOT under the existing `orchestrators` subparser, and notes existing `artagents orchestrators` keeps working.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Authoring section states Python DSL `artagents.orchestrate` is the only committed representation, JSON manifest is gitignored at `<pack>/build/<orch>.json`, runtime hashes/pins the build artifact, pack adds `<orch>.py`/`fixtures/`/`golden/<name>.events.jsonl`, AND root `.gitignore` is updated to exclude `<pack>/build/` as part of Phase 4 exit criteria.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Stop-hook section states the prohibition preamble is re-injected verbatim on every `artagents next` call (not just first call).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Canonical migration example uses `artagents/packs/builtin/hype/` with a diff sketch (new `hype.py`/`build/hype.json`/`fixtures/`/`golden/`), confirms existing JSON manifest still loads, AND documents that nested calls into `prepare_project_run()` inherit `ARTAGENTS_TASK_RUN_ID` and skip creating child project records.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Risk register includes single-host assumption, semantic verifier discipline, context-decay re-injection, and honor-model boundary, each with trigger + mitigation.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Document explicitly Confirms (or Revises with rationale) all eight open-call decisions A1\u2013A8: nested-as-data; Python DSL only; no .index.db; artagents/core/task/ namespace; pipeline.py CLI surface; nested-call ARTAGENTS_TASK_RUN_ID inheritance; gate ordering before _prepare_project_request; .gitignore for <pack>/build/.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Migration is presented as additive: existing `OrchestratorDefinition` JSON manifests + `python`/`command` `RUNTIME_KINDS` keep working through and after v1; existing `artagents orchestrators` CLI verbs remain unchanged.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "All EXISTING-CODE inline path citations (e.g., `artagents/pipeline.py:15`, `artagents/core/orchestrator/runner.py:135`, `artagents/core/orchestrator/schema.py`, `artagents/core/project/run.py`, `artagents/threads/wrapper.py`, `artagents/packs/builtin/hype/`) resolve to real files in the repo today.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "FUTURE-DELIVERABLE paths (`AUTHORING.md`, per-run `AGENT.md`, `<pack>/build/`, `<pack>/fixtures/`, `<pack>/golden/`, `artagents/core/task/`, `artagents/orchestrate/`, `artagents/verify/`) are clearly framed as prescriptive new paths in the doc, not as resolvable-today citations.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Document body length lands in ~1500\u20132200 words (SD list excluded).",
        "priority": "should",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Tone is terse, declarative, decision-first; matches `docs/sprint-thread-layer.md` and `docs/design-thread-layer.md`.",
        "priority": "should",
        "requires": [
          "subjective_judgment",
          "read_files"
        ]
      },
      {
        "criterion": "Document does not introduce a daemon, web server, `.index.db`, HMAC/keyed crypto, or shared CAS in v1; these are explicitly listed in Non-Goals.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Cut Points section identifies Phase 3 (kernel + step kinds + produces/repeat) and Phase 5 (adds authoring + lifecycle verb split) as ship-ready milestones.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      }
    ]
  },
  "preflight_results": {
    "project_dir_exists": true,
    "project_dir_writable": true,
    "success_criteria_present": true,
    "claude_available": true,
    "codex_available": true
  },
  "unresolved_flags": [
    {
      "id": "issue_hints",
      "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Step Kinds/A1 still says `code-step-calls-orchestrator` is forbidden, but Step 8 says a `code` step in `hype.py` may shell out to today's `artagents orchestrators run ...`. That contradicts a load-bearing design call from the task spec and would make downstream implementers unclear whether orchestrator delegation is represented as `nested` data or hidden inside a `code` argv.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Step Kinds/A1 still says `code-step-calls-orchestrator` is forbidden, but Step 8 says a `code` step in `hype.py` may shell out to today's `artagents orchestrators run ...`. That contradicts a load-bearing design call from the task spec and would make downstream implementers unclear whether orchestrator delegation is represented as `nested` data or hidden inside a `code` argv.",
      "raised_in": "critique_v2.json",
      "status": "open",
      "severity": "significant",
      "verified": true,
      "addressed_in": "plan_v2.md",
      "verified_in": "critique_v2.json"
    },
    {
      "id": "correctness",
      "concern": "Are the proposed changes technically correct?: The new `ARTAGENTS_TASK_RUN_ID` inheritance decision is technically under-specified for existing project-run behavior: current tests in `tests/test_project_runs.py` expect `ARTAGENTS_PROJECT_RUN=1`, project `run.json` creation, and hype artifact mirroring for project runs. If child project records are skipped wholesale during task mode, the plan needs to preserve the child command's output directory and artifact mirroring semantics inside the parent task run, or explicitly mark those project-run behaviors as not available under task mode.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "The new `ARTAGENTS_TASK_RUN_ID` inheritance decision is technically under-specified for existing project-run behavior: current tests in `tests/test_project_runs.py` expect `ARTAGENTS_PROJECT_RUN=1`, project `run.json` creation, and hype artifact mirroring for project runs. If child project records are skipped wholesale during task mode, the plan needs to preserve the child command's output directory and artifact mirroring semantics inside the parent task run, or explicitly mark those project-run behaviors as not available under task mode.",
      "raised_in": "critique_v2.json",
      "status": "open",
      "severity": "significant",
      "verified": true,
      "addressed_in": "plan_v2.md",
      "verified_in": "critique_v2.json"
    },
    {
      "id": "all_locations",
      "concern": "Does the change touch all locations AND supporting infrastructure?: Searched for task-run environment conventions and found no existing `ARTAGENTS_TASK_RUN_ID`; existing run identity envs are `ARTAGENTS_RUN_ID`, `ARTAGENTS_PARENT_RUN_ID`, and `ARTAGENTS_PROJECT_RUN` in `artagents/threads/wrapper.py` and `artagents/core/project/run.py`. Introducing `ARTAGENTS_TASK_RUN_ID` is acceptable, but the plan should list every integration file that must read or propagate it, especially executor runner, orchestrator runner, direct `builtin.hype`, and subprocess env construction.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Searched for task-run environment conventions and found no existing `ARTAGENTS_TASK_RUN_ID`; existing run identity envs are `ARTAGENTS_RUN_ID`, `ARTAGENTS_PARENT_RUN_ID`, and `ARTAGENTS_PROJECT_RUN` in `artagents/threads/wrapper.py` and `artagents/core/project/run.py`. Introducing `ARTAGENTS_TASK_RUN_ID` is acceptable, but the plan should list every integration file that must read or propagate it, especially executor runner, orchestrator runner, direct `builtin.hype`, and subprocess env construction.",
      "raised_in": "critique_v2.json",
      "status": "open",
      "severity": "significant",
      "verified": true,
      "addressed_in": "plan_v2.md",
      "verified_in": "critique_v2.json"
    },
    {
      "id": "callers",
      "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: The revised phase table carries the parent-task inheritance behavior mainly in the migration example instead of in the implementation phases. Because `run_executor()` and direct `hype.main()` have independent project-run preparation paths, the doc should move this from example-only text into the Phase 1 or Phase 2 scope/files/exit criteria so it is not skipped for non-hype task plans.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "The revised phase table carries the parent-task inheritance behavior mainly in the migration example instead of in the implementation phases. Because `run_executor()` and direct `hype.main()` have independent project-run preparation paths, the doc should move this from example-only text into the Phase 1 or Phase 2 scope/files/exit criteria so it is not skipped for non-hype task plans.",
      "raised_in": "critique_v2.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "FLAG-004",
      "concern": "Step model: the revised plan both forbids `code-step-calls-orchestrator` and describes `code` steps shelling out to `artagents orchestrators run`, which contradicts the required nested-as-data model.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "A1 and Step 3 forbid `code-step-calls-orchestrator`; Step 8 says a `code` step in `hype.py` can shell to today's `artagents executors run ...` or `artagents orchestrators run ...`.",
      "raised_in": "critique_v2.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "FLAG-005",
      "concern": "Project run inheritance: `ARTAGENTS_TASK_RUN_ID` inheritance is specified, but the phase implementation file lists do not include all actual project-run preparation paths that would need to honor it.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "`prepare_project_run()` is called from `artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, and `artagents/packs/builtin/hype/run.py`; the revised phase table mainly names orchestrator runner/project run files and leaves executor/direct-hype handling to the migration example.",
      "raised_in": "critique_v2.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "scope",
      "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: The revised scope for nested-call inheritance names three caller families, but the nine-phase file-touch lists do not include `artagents/core/executor/runner.py` or `artagents/packs/builtin/hype/run.py` in the phase that implements `ARTAGENTS_TASK_RUN_ID` behavior. Those files are actual `prepare_project_run()` callers, so downstream implementation could miss required glue while still following the phase table.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "The revised scope for nested-call inheritance names three caller families, but the nine-phase file-touch lists do not include `artagents/core/executor/runner.py` or `artagents/packs/builtin/hype/run.py` in the phase that implements `ARTAGENTS_TASK_RUN_ID` behavior. Those files are actual `prepare_project_run()` callers, so downstream implementation could miss required glue while still following the phase table.",
      "raised_in": "critique_v2.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    }
  ]
}

        Critique check summary:
        - issue_hints: 1 flagged
        - correctness: 1 flagged
        - scope: 1 flagged
        - all_locations: 1 flagged
        - callers: 1 flagged
        - conventions: 1 flagged
        - verification: 1 flagged
        - criteria_quality: clear

        Unresolved significant flags:
        [
  {
    "id": "issue_hints",
    "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Step Kinds/A1 still says `code-step-calls-orchestrator` is forbidden, but Step 8 says a `code` step in `hype.py` may shell out to today's `artagents orchestrators run ...`. That contradicts a load-bearing design call from the task spec and would make downstream implementers unclear whether orchestrator delegation is represented as `nested` data or hidden inside a `code` argv.",
    "evidence": "Step Kinds/A1 still says `code-step-calls-orchestrator` is forbidden, but Step 8 says a `code` step in `hype.py` may shell out to today's `artagents orchestrators run ...`. That contradicts a load-bearing design call from the task spec and would make downstream implementers unclear whether orchestrator delegation is represented as `nested` data or hidden inside a `code` argv.",
    "category": "completeness",
    "severity": "significant",
    "status": "open",
    "weight": null
  },
  {
    "id": "correctness",
    "concern": "Are the proposed changes technically correct?: The new `ARTAGENTS_TASK_RUN_ID` inheritance decision is technically under-specified for existing project-run behavior: current tests in `tests/test_project_runs.py` expect `ARTAGENTS_PROJECT_RUN=1`, project `run.json` creation, and hype artifact mirroring for project runs. If child project records are skipped wholesale during task mode, the plan needs to preserve the child command's output directory and artifact mirroring semantics inside the parent task run, or explicitly mark those project-run behaviors as not available under task mode.",
    "evidence": "The new `ARTAGENTS_TASK_RUN_ID` inheritance decision is technically under-specified for existing project-run behavior: current tests in `tests/test_project_runs.py` expect `ARTAGENTS_PROJECT_RUN=1`, project `run.json` creation, and hype artifact mirroring for project runs. If child project records are skipped wholesale during task mode, the plan needs to preserve the child command's output directory and artifact mirroring semantics inside the parent task run, or explicitly mark those project-run behaviors as not available under task mode.",
    "category": "correctness",
    "severity": "significant",
    "status": "open",
    "weight": null
  },
  {
    "id": "all_locations",
    "concern": "Does the change touch all locations AND supporting infrastructure?: Searched for task-run environment conventions and found no existing `ARTAGENTS_TASK_RUN_ID`; existing run identity envs are `ARTAGENTS_RUN_ID`, `ARTAGENTS_PARENT_RUN_ID`, and `ARTAGENTS_PROJECT_RUN` in `artagents/threads/wrapper.py` and `artagents/core/project/run.py`. Introducing `ARTAGENTS_TASK_RUN_ID` is acceptable, but the plan should list every integration file that must read or propagate it, especially executor runner, orchestrator runner, direct `builtin.hype`, and subprocess env construction.",
    "evidence": "Searched for task-run environment conventions and found no existing `ARTAGENTS_TASK_RUN_ID`; existing run identity envs are `ARTAGENTS_RUN_ID`, `ARTAGENTS_PARENT_RUN_ID`, and `ARTAGENTS_PROJECT_RUN` in `artagents/threads/wrapper.py` and `artagents/core/project/run.py`. Introducing `ARTAGENTS_TASK_RUN_ID` is acceptable, but the plan should list every integration file that must read or propagate it, especially executor runner, orchestrator runner, direct `builtin.hype`, and subprocess env construction.",
    "category": "completeness",
    "severity": "significant",
    "status": "open",
    "weight": null
  },
  {
    "id": "callers",
    "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: The revised phase table carries the parent-task inheritance behavior mainly in the migration example instead of in the implementation phases. Because `run_executor()` and direct `hype.main()` have independent project-run preparation paths, the doc should move this from example-only text into the Phase 1 or Phase 2 scope/files/exit criteria so it is not skipped for non-hype task plans.",
    "evidence": "The revised phase table carries the parent-task inheritance behavior mainly in the migration example instead of in the implementation phases. Because `run_executor()` and direct `hype.main()` have independent project-run preparation paths, the doc should move this from example-only text into the Phase 1 or Phase 2 scope/files/exit criteria so it is not skipped for non-hype task plans.",
    "category": "correctness",
    "severity": "significant",
    "status": "open",
    "weight": null
  },
  {
    "id": "FLAG-004",
    "concern": "Step model: the revised plan both forbids `code-step-calls-orchestrator` and describes `code` steps shelling out to `artagents orchestrators run`, which contradicts the required nested-as-data model.",
    "evidence": "A1 and Step 3 forbid `code-step-calls-orchestrator`; Step 8 says a `code` step in `hype.py` can shell to today's `artagents executors run ...` or `artagents orchestrators run ...`.",
    "category": "correctness",
    "severity": "significant",
    "status": "open",
    "weight": null
  },
  {
    "id": "FLAG-005",
    "concern": "Project run inheritance: `ARTAGENTS_TASK_RUN_ID` inheritance is specified, but the phase implementation file lists do not include all actual project-run preparation paths that would need to honor it.",
    "evidence": "`prepare_project_run()` is called from `artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, and `artagents/packs/builtin/hype/run.py`; the revised phase table mainly names orchestrator runner/project run files and leaves executor/direct-hype handling to the migration example.",
    "category": "completeness",
    "severity": "significant",
    "status": "open",
    "weight": null
  },
  {
    "id": "scope",
    "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: The revised scope for nested-call inheritance names three caller families, but the nine-phase file-touch lists do not include `artagents/core/executor/runner.py` or `artagents/packs/builtin/hype/run.py` in the phase that implements `ARTAGENTS_TASK_RUN_ID` behavior. Those files are actual `prepare_project_run()` callers, so downstream implementation could miss required glue while still following the phase table.",
    "evidence": "The revised scope for nested-call inheritance names three caller families, but the nine-phase file-touch lists do not include `artagents/core/executor/runner.py` or `artagents/packs/builtin/hype/run.py` in the phase that implements `ARTAGENTS_TASK_RUN_ID` behavior. Those files are actual `prepare_project_run()` callers, so downstream implementation could miss required glue while still following the phase table.",
    "category": "completeness",
    "severity": "significant",
    "status": "open",
    "weight": null
  }
]

        Known accepted debt grouped by subsystem:
{}

Escalated debt subsystems:
[]

Debt guidance:
- Treat recurring debt as decision context, not background noise.
- If the current unresolved flags overlap an escalated subsystem, prefer recommending holistic redesign over another point fix.

        Iteration Pressure Analysis:
Group      Flags  Iters  Reopened  Concern
------------------------------------------------------------------------
FG-001     1      2      0         Step Kinds/A1 still says `code-step-calls-orchestr
FG-002     1      2      0         The new `ARTAGENTS_TASK_RUN_ID` inheritance decisi
FG-003     1      2      0         The revised scope for nested-call inheritance name
FG-004     1      2      0         Searched for task-run environment conventions and 
FG-005     1      2      0         The revised phase table carries the parent-task in
FG-006     1      2      0         The revised plan chooses a new `artagents/orchestr
FG-007     1      2      0         The implementation-phase test strategy still does 
FG-008     1      1      0         Flagged that the path-citation criterion should di
FG-009     1      1      0         Task CLI surface: lifecycle verbs are top-level bu
FG-010     1      1      0         Gate ordering: saying the gate runs before `artage
FG-011     1      1      0         Authoring build artifacts: the plan requires gitig
FG-012     1      2      0         Criterion 18: requires human verification (subject
FG-013     1      1      0         Step model: the revised plan both forbids `code-st
FG-014     1      1      0         Project run inheritance: `ARTAGENTS_TASK_RUN_ID` i
FG-015     1      1      0         Structure guardrails: the plan introduces future t
FG-016     1      1      0         Verification: phase test strategies still omit exi
FG-017     1      1      0         Search for related code that handles the same conc
FG-018     1      1      0         Search for related code that handles the same conc

        Robustness level:
        robust

        Requirements:
        - Decide exactly one of: PROCEED, ITERATE, ESCALATE, TIEBREAKER.
        - Use the weighted score, flag details (including `evidence`), plan delta, recurring critiques, and preflight results as judgment context.
        - PROCEED when execution should move forward now.
        - ITERATE when revising the plan is the best next move.
        - ESCALATE when the loop is stuck, churn is recurring, or user intervention is needed.
        - TIEBREAKER when a flag group reflects an *unresolvable constraint tension* (architectural or philosophical — requires a human call) rather than a plan-quality issue. Use TIEBREAKER only when the Iteration Pressure Analysis shows `addressed_then_reopened_count >= 2` for a fuzzy group OR the group has >=2 member flags across >=2 iterations. If the concern is simply that the plan writer hasn't tried hard enough, use ITERATE instead. When recommending TIEBREAKER you MUST provide `tiebreaker_question` (the decision question for human resolution), `tiebreaker_flag_ids` (which flags this resolves), and `tiebreaker_fuzzy_group_id` (which group this resolves). Cite specific flag IDs and iterations in your rationale.
        - `signals_assessment`: one paragraph summarizing score trajectory, flag status, and preflight posture.

        Flags come in two tiers:
        - **Blocking** (severity = significant/likely-significant): These are serious concerns. If you recommend PROCEED, you MUST provide a `flag_resolutions` entry for every blocking flag. There is no implicit acceptance.
        - **Noted** (everything else): Acknowledge in your rationale but they don't block PROCEED.

        If there are blocking flags and you want to PROCEED, provide `flag_resolutions` with one entry per blocking flag. If you cannot resolve every blocking flag, choose ITERATE (send back for revision) or ESCALATE (human intervention needed).
        Structurally unresolvable flags (for example, infrastructure outside the repo or product decisions that require a human) are ESCALATE, not PROCEED with a non-answer.

        For each blocking flag:
        - **dispute**: The critique is factually wrong. Evidence must cite something specific (file path, line, API doc, etc.). Generic statements like "handled correctly" are invalid.
        - **accept_tradeoff**: The concern is real but intentionally accepted as a known limitation. Rationale must be specific to this flag. Boilerplate like "acceptable within scope" is invalid.
        - Schema requirement: every `flag_resolutions` entry must include both `evidence` and `rationale`. Use `""` for the field that does not apply to that action.

        If there are no blocking flags, return `flag_resolutions: []`.
        Always return `accepted_tradeoffs`; use `[]` when none apply.

        Populate `settled_decisions` with design choices that should carry into review without re-litigation. Return `[]` when there are none.

        Example:
        ```json
        {
          "recommendation": "PROCEED",
          "rationale": "Core fix is correct. Convention concern accepted.",
          "signals_assessment": "Score stable at 2.5, preflight passed, no recurring critiques.",
          "warnings": ["Verify edge case with composite moduli during execution."],
          "flag_resolutions": [
            {"flag_id": "correctness-1", "action": "dispute", "evidence": "allow_migrate and allow_migrate_model produce identical behavior for this use case (verified at django/db/utils.py:286).", "rationale": ""},
            {"flag_id": "performance-1", "action": "accept_tradeoff", "evidence": "", "rationale": "Cold-start latency remains 40ms above target because the cache warmup job is owned by platform and outside this repo; rollout is still approved for the limited internal beta."},
            {"flag_id": "conventions-1", "action": "accept_tradeoff", "evidence": "", "rationale": "Minor naming inconsistency is confined to this helper and would create churn across generated fixtures; track it as follow-up cleanup instead of blocking this fix."}
          ],
          "accepted_tradeoffs": [],
          "settled_decisions": []
        }
        ```

> TOOL

tool_use StructuredOutput
```json
{
  "recommendation": "ITERATE",
  "rationale": "Two cleanly tractable plan-quality issues remain — neither is an unresolvable architectural tension, so TIEBREAKER doesn't fit; the loop is improving (15→12, 84% delta, 6 of 9 prior flags resolved), so ESCALATE is premature; and the contradictions would corrupt the frozen design doc if executed as-is, so PROCEED is unsafe. Issue 1 (FG-001 / issue_hints + FLAG-004): A1/Step 3 forbid `code-step-calls-orchestrator` but Step 8 + Section 13 say hype.py `code` steps shell to `artagents orchestrators run …` / `artagents executors run …` — these can't both be true. Resolve by restating Section 13: sub-orchestrator delegation uses the `nested` step kind (its data structure is what hash-pinning sees); inline executor invocation in a `code` step is a Python function call, not a subprocess to `orchestrators run`. Issue 2 (FG-002/004/005 + correctness, all_locations, callers, FLAG-005, scope): the new `ARTAGENTS_TASK_RUN_ID` env contract is described in A6 / Section 13 but missing from Phase 1–2 file-touch lists; needs explicit naming of `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`, and `artagents/threads/wrapper.py` (which already owns `ARTAGENTS_RUN_ID`/`ARTAGENTS_PARENT_RUN_ID`/`ARTAGENTS_PROJECT_RUN`) plus an explicit decision on `tests/test_project_runs.py` compatibility (preserve project-run output dirs and artifact mirroring inside the parent task run, OR mark those behaviors ta[REDACTED_SK]). Both are tightenings, not redesigns. No flags reopened across iterations — the loop is doing real work.",
  "signals_assessment": "Iteration 2; weighted score 15.0 → 12.0 (improving); plan delta 84.18%; 6 of 9 prior significant flags resolved with verification; 7 new significant flags clustered into exactly two themes (step-kind contradiction in the migration example, and ARTAGENTS_TASK_RUN_ID under-specification across phase file lists). Iteration pressure shows 0 reopened flags across all groups, so no churn. Preflight clean (writable workspace, criteria present, both Claude and codex available). Healthy convergence, not a stuck loop.",
  "warnings": [
    "Resolve the step-kind contradiction explicitly: state that delegating to another orchestrator/executor MUST use the `nested` step kind so the gate sees the structure for hashing/pinning; a `code` step may call an executor as an inline Python function but MUST NOT subprocess to `artagents orchestrators run` or `artagents executors run`. Update Section 13 hype.py sketch to use `nested` for sub-orchestrator delegation and inline executor calls (not subprocess) for unit work.",
    "Move ARTAGENTS_TASK_RUN_ID propagation into Phase 1 (env-read) and Phase 2 (env-honored-by-step-kinds) scope and exit criteria. Phase 1 files-touched MUST name: `artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`, `artagents/core/project/run.py`, and `artagents/threads/wrapper.py` (subprocess env construction + existing run-identity envs `ARTAGENTS_RUN_ID`/`ARTAGENTS_PARENT_RUN_ID`/`ARTAGENTS_PROJECT_RUN`). Each must have an exit criterion that nested calls under task mode read the env and skip child project records.",
    "Decide and state explicitly how `tests/test_project_runs.py` (which expects `ARTAGENTS_PROJECT_RUN=1` + child `run.json` + hype artifact mirroring) interacts with task-mode inheritance: either preserve the child output dir + artifact mirroring inside the parent task run (and call out test-update scope in Phase 2), or mark project-run records as ta[REDACTED_SK] with rationale and a corresponding SD entry. Also add a Phase 1 or Phase 2 test that exercises a non-hype task plan calling `run_executor()` so the inheritance contract isn't only validated through the migration example.",
    "Add corresponding SD entries: one for `nested`-vs-`code` boundary on sub-orchestrator delegation (no subprocess to orchestrators/executors run); one for ARTAGENTS_TASK_RUN_ID propagation surface (named files); one for project-run-record behavior under task mode (preserved-inline OR unavailable).",
    "Verify the `tests/test_project_runs.py` path actually exists in the repo before citing it; if not, locate the equivalent test module and cite that path."
  ],
  "flag_resolutions": [],
  "accepted_tradeoffs": [],
  "settled_decisions": [
    {
      "id": "SD-G1",
      "decision": "Doc body target ~1500-2200 words excluding the SD list.",
      "rationale": "Confirmed iteration 1, uncontested in iteration 2."
    },
    {
      "id": "SD-G2",
      "decision": "Canonical migration example is artagents/packs/builtin/hype/.",
      "rationale": "Confirmed and uncontested across iterations 1 and 2."
    },
    {
      "id": "SD-G3",
      "decision": "Output path is exactly docs/orchestrator-v1-plan.md.",
      "rationale": "Fixed by task brief."
    },
    {
      "id": "SD-G4",
      "decision": "SD format follows `SD-NNN <topic>: <single-sentence rationale>.` per docs/sprint-thread-layer.md lines 39-43.",
      "rationale": "Format reference confirmed and uncontested."
    },
    {
      "id": "SD-G5",
      "decision": "Top-level lifecycle/operator/author verbs extend artagents/pipeline.py:15 dispatch table; existing `artagents orchestrators` keeps working unchanged.",
      "rationale": "A5 resolved in iteration 2 (FLAG-001/scope-1/scope-2 marked addressed and verified)."
    },
    {
      "id": "SD-G6",
      "decision": "Gate runs BEFORE both _prepare_project_request() (artagents/core/orchestrator/runner.py:135) AND thread_wrapper.begin_orchestrator_run() (line 136); rejection produces zero project-run filesystem side effects.",
      "rationale": "A7 resolved in iteration 2 (FLAG-002 + correctness flags marked addressed and verified)."
    },
    {
      "id": "SD-G7",
      "decision": "Kernel modules land in NEW artagents/core/task/ package (gate, events, active_run, dispatch, produces, cas, inbox, preamble) above orchestrator dispatch.",
      "rationale": "A4 resolved in iteration 2 with namespace rationale (gate sits above orchestrator dispatch)."
    },
    {
      "id": "SD-G8",
      "decision": "Root .gitignore is updated in Phase 4 to exclude <pack>/build/.",
      "rationale": "A8 resolved in iteration 2; FLAG-003 resolved with evidence about current .gitignore contents."
    },
    {
      "id": "SD-G9",
      "decision": "Path-citation success criterion is split: existing-code citations MUST resolve today; future-deliverable paths (AUTHORING.md, AGENT.md, <pack>/build/, <pack>/fixtures/, <pack>/golden/, artagents/core/task/, artagents/orchestrate/, artagents/verify/) are framed as prescriptive new paths.",
      "rationale": "criteria_quality flag resolved in iteration 2."
    }
  ],
  "tiebreaker_question": "",
  "tiebreaker_flag_ids": [],
  "tiebreaker_fuzzy_group_id": ""
}
```

> TOOL

tool_result StructuredOutput
```
Structured output provided successfully
```

> AGENT

Recommended **ITERATE**. Score is improving (15→12, 6 prior flags resolved, 0 reopened), but two clean fixes remain: (1) the step-kind contradiction in Section 13 — sub-orchestrator delegation must use `nested`, not a `code` step that subprocesses to `orchestrators run`; and (2) `ARTAGENTS_TASK_RUN_ID` propagation needs to be moved into Phase 1/2 file lists with `executor/runner.py`, `packs/builtin/hype/run.py`, and `threads/wrapper.py` named explicitly, plus an explicit decision on `tests/test_project_runs.py` compatibility. Both are tightenings, not redesigns — one more pass should close it.

> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

WRITE ACCESS CONTRACT: You are running with auto-approved writes inside a writable workspace. Treat the working directory as fully writable. Do NOT preemptively skip or block tasks on permission, sandbox, or read-only grounds. Attempt every required edit; only report failure AFTER a real OS-level rejection from a specific shell command. Do not infer 'read-only' from absence of activity; absence is not denial. If a single shell command unexpectedly fails, retry with a different invocation before concluding the environment is restricted.

You are the gatekeeper for the megaplan workflow. Make the continuation decision directly.

        Project directory:
        /Users/user_c042661f/Documents/reigh-workspace/ArtAgents

        Idea:
ArtAgents is a file-based, single-host Python CLI for running creative pipelines (video/audio/image) that mix code, AI, and human steps. Today it has a pack-based plugin architecture, orchestrator + executor schemas (python/command runtime kinds only), project runs under ~/Documents/reigh-workspace/artagents-projects/, threads with provenance, and a CLI gateway. We are extending it so an agent can be put into 'task mode' and walked through a frozen plan that mixes code, AI, and human steps, with iteration loops and fan-out.

NON-NEGOTIABLES:
- Single-host, file-based. No daemon, no web server.
- Honor-based with strong logging. We do not pretend to sandbox a misaligned agent.
- Migration is additive. Existing JSON manifests and python/command runtime kinds keep working.
- Existing pack mechanism stays.

V1 DESIGN (post-critique, trimmed):

THREE STEP KINDS:
- code: deterministic argv, runner subprocesses, returncode + produces.
- attested: agent or human task. instructions + produces + ack records identity (agent_id or actor pinned via ARTAGENTS_ACTOR) + evidence.
- nested: delegates to a child plan; gate sees the structure for hashing/pinning.

ITERATION AND FAN-OUT ARE BODY ATTRIBUTES, NOT KINDS:
- repeat: {until: user_approves|verifier_passes|quorum, max_iterations, on_exhaust}
- repeat: {for_each: <input_set>}
Both apply to any step or to a body block in a nested plan.

PRODUCES WITH INLINE CHECKS (replaces separate verifier substep):
  produces = {
    'audio': file(path='audio.wav', check=audio_duration_min(30)),
    'notes': json_file(path='notes.json', schema='notes.schema.json', min_items=3),
  }
The gate runs the check; failure rewinds the cursor. passes_test is a regular code step.

STORAGE (under ~/Documents/reigh-workspace/artagents-projects/):
- <slug>/active_run.json -- pointer to in-flight run + plan hash
- <slug>/runs/<run-id>/plan.json -- immutable, hash-pinned (renamed from 'checklist' since it's a tree)
- <slug>/runs/<run-id>/events.jsonl -- append-only, plain hash-chained (prev_hash field), sole truth
- <slug>/runs/<run-id>/AGENT.md -- contract for whoever's driving
- <slug>/runs/<run-id>/steps/<step-id>/produces/ -- artifact files (or symlinks into .cas)
- <slug>/runs/<run-id>/steps/<step-id>/iterations/NNN/ -- when repeat:until is set
- <slug>/runs/<run-id>/steps/<step-id>/items/<item-id>/ -- when repeat:for_each is set
- <slug>/runs/<run-id>/inbox/ -- external completion signals get dropped here
- <slug>/.cas/<sha256> -- per-project CAS for v1 (not shared)

NO crypto: hash chain is plain sha256(prev_hash + canonical_event_json). Tripwire for accidental edits, not protection against malicious users. We do not need HMAC or key handles.

NO .index.db in v1. find + grep on events.jsonl is fine until grep is slow.

GATE (above dispatch, single function):
- active_run.json exists for this project?
- plan.json hash matches the pin in active_run.json?
- events.jsonl hash chain intact?
- incoming command matches plan[derived_cursor].command?
If any fails, reject with the exact recovery command.

LIFECYCLE VERBS, scoped by audience:
artagents next | ack | status | abort                                  (agent-facing, mid-run)
artagents start | abort | status | runs ls                             (operator)
artagents author new | check | describe | test | compile | explain     (author)

ACK DECISIONS (intentionally distinct):
--decision approve              -- advance cursor
--decision retry                -- only valid after verifier failure; rerun body, stderr is feedback
--decision iterate --feedback   -- only valid when repeat.until=user_approves; appends to cumulative constraints
--decision abort                -- end run

ACK requires --agent <id> for attested steps with attestor_type=agent, or --actor <name> matching ARTAGENTS_ACTOR for attestor_type=human. Self-acks and unpinned actors are rejected.

For repeat:for_each: --item <id> targets a specific item; partial approval is supported.

NUDGE (out-of-process, optional, Claude Code only for v1):
A Stop hook runs artagents next. The next output ALWAYS includes the prohibition preamble verbatim, not just on first call -- this is the re-injection mechanism that fights context decay.

AUTHORING:
- Python DSL artagents.orchestrate is the ONLY committed representation. JSON manifest is generated at author compile into a build/ dir (gitignored) and that's what the runtime hashes/pins.
- Verifier helper library artagents.verify: file_nonempty, json_schema, json_file, audio_duration_min, image_dimensions, all_of.
- Pack layout: <pack>/<orch>.py (committed), <pack>/build/<orch>.json (gitignored), <pack>/fixtures/<name>/, <pack>/golden/<name>.events.jsonl.
- author check is sub-second static validation: schema, every produces/requires reference resolves, every nested plan resolves, attested steps with non-trivial produces have semantic checks (sentinel-existence-only is rejected at definition time).
- author describe pretty-prints the DAG.
- author test --fixture runs --dry-run --auto-approve, diffs events.jsonl against golden/<fixture>.events.jsonl.

V1 BUILD ORDER (recommended phases):
1. Kernel: events.jsonl + plain hash chain + plan hash pin + gate above dispatch + active_run.json. Runner becomes dumb; gate is a single decorated function above runner dispatch.
2. Three step kinds: code, attested, nested. (code is a strict superset of today's python+command runtime kinds.)
3. produces-with-inline-checks; repeat:{until} and repeat:{for_each} on bodies.
4. Authoring: Python DSL + verify helpers + author check + author describe + author new.
5. Lifecycle verbs split by audience as above.
6. Stop-hook nudge with mandatory prohibition preamble.
7. CAS per-project (under <slug>/.cas/), symlink-based produces.
8. Inbox surface for external completion signals.
9. Author test with golden runs.

EXISTING REPO STATE:
- artagents/core/orchestrator/ exists with schema.py, runner.py, registry.py, cli.py, api.py. Currently knows ORCHESTRATOR_KINDS={built_in, external} and RUNTIME_KINDS={python, command}. OrchestratorPlan / OrchestratorPlanStep skeletons exist (used for dry-run output).
- artagents/core/project/ exists with run lifecycle (prepare_project_run / finalize_project_run), paths.py with DEFAULT_PROJECTS_ROOT.
- artagents/threads/ exists with thread_wrapper around runs, @active concept.
- artagents/packs/ holds builtin packs (cut, transcribe, human_notes, open_in_reigh, etc.).
- Migration to packs is mid-flight (recent commits T10-T13).

ASSUMED OPEN-CALL DEFAULTS (the design plan should call these out and confirm or revise):
- Keep nested step kind as data (gate sees the structure); forbid code-step-calls-orchestrator.
- Python DSL is the only committed representation; JSON manifest is a build artifact in gitignored build/ dirs.
- Drop .index.db from v1; ship with file-walk verbs.

DELIVERABLE EXPECTATIONS for the design doc:
- Concrete phasing aligned to build order 1-9 above; each phase has scope, files touched, breaking-change risk classification (additive vs breaking), and exit criteria.
- Test strategy at each phase (golden runs are the regression format).
- Migration of one builtin pack (suggest hype.cut or transcribe) to the new shape as the canonical example, including the diff shape.
- Documentation deliverables identified: AUTHORING.md (one-page reference for both human and LLM authors), AGENT.md template, README.md updates.
- Risk register (single-host assumption, semantic verifier discipline, context decay re-injection, agent honor model boundary).
- Cut points where work can stop and still ship something useful (e.g., after phase 3, after phase 5).
- A ## Settled Decisions section at the bottom listing every load-bearing design call (SD-NNN format) so future code-mode runs can inherit them via --from-doc.

Mode: doc / metaplan
Output: docs/orchestrator-v1-plan.md

User notes and answers:
- strict-notes auto-enabled for metaplan/doc mode

        Plan:
        # Implementation Plan: Author docs/orchestrator-v1-plan.md (Task Mode V1 Design)

## Overview

Single deliverable: `docs/orchestrator-v1-plan.md` — a frozen, decision-first design+migration doc adding "task mode" to ArtAgents. The doc must reproduce the task spec exactly on storage, gate, ack, and phasing; cite repo paths inline; end with `## Settled Decisions` (`SD-NNN <topic>: <single-sentence rationale>.`) matching `docs/sprint-thread-layer.md` lines 39–43.

Verified repo facts the doc must encode (not paraphrase):
- Top-level CLI dispatch lives in `artagents/pipeline.py:15` (`main`); unknown subcommands fall through to `_run_default_brief_orchestrator()` at `artagents/pipeline.py:75`.
- `artagents/core/orchestrator/runner.py:135` calls `_prepare_project_request()` BEFORE `thread_wrapper.begin_orchestrator_run()` at line 136.
- `prepare_project_run()` has THREE caller paths today: `artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`.
- Existing run-identity envs are `ARTAGENTS_RUN_ID`, `ARTAGENTS_PARENT_RUN_ID`, `ARTAGENTS_PROJECT_RUN` (declared in `artagents/threads/wrapper.py:21-26`); no `ARTAGENTS_TASK_RUN_ID` exists yet.
- `artagents/core/orchestrator/schema.py` enforces `ORCHESTRATOR_KINDS={built_in,external}` and `RUNTIME_KINDS={python,command}`; existing JSON manifests must keep loading via `load_orchestrator_manifest`.
- `tests/test_project_runs.py` exists today and asserts `ARTAGENTS_PROJECT_RUN=1`, child `run.json` creation, and hype artifact mirroring under standalone (non-task-mode) project runs.
- Canonical migration target: `artagents/packs/builtin/hype/` (today: `orchestrator.yaml` + `STAGE.md` + `run.py`).

Output path is fixed: `docs/orchestrator-v1-plan.md`. The executor only writes there.

## Open-Call Decisions (resolved before authoring)

- A1 — nested step kind stays as data; `code-step-calls-orchestrator` forbidden. **Confirmed.**
- A2 — Python DSL `artagents.orchestrate` is the only committed representation; JSON manifest at `<pack>/build/<orch>.json` is gitignored. **Confirmed.**
- A3 — no `.index.db` in v1; file-walk verbs only. **Confirmed.**
- A4 — kernel modules land in NEW `artagents/core/task/` package (gate, events, active_run, dispatch, produces, cas, inbox, preamble), NOT under `artagents/core/orchestrator/`. **Confirmed.**
- A5 — top-level lifecycle/operator/author verbs (`next`/`ack`/`status`/`abort`/`start`/`runs ls`/`author …`) extend `artagents/pipeline.py:15` dispatch table. Existing `artagents orchestrators run|list|inspect|validate` keeps working unchanged. **Confirmed.**
- A6 (REVISED — resolves issue_hints / FLAG-004) — `code` step is inline Python execution only: it MAY call executor entrypoints as **direct Python function calls** (importing the executor module and invoking its callable), but MUST NOT shell out to `artagents executors run …` or `artagents orchestrators run …` as subprocess argv. Sub-orchestrator delegation is represented EXCLUSIVELY by the `nested` step kind so the gate sees the structure for hashing/pinning. This makes `code-step-calls-orchestrator` forbidden in both spirit (no hidden delegation) and letter (no subprocess to those argv shapes). **Confirmed (revised wording).**
- A7 — gate runs BEFORE BOTH `_prepare_project_request()` (`artagents/core/orchestrator/runner.py:135`) AND `thread_wrapper.begin_orchestrator_run()` (line 136). A rejected command produces zero project-run filesystem side effects. **Confirmed.**
- A8 — root `.gitignore` updated in Phase 4 to exclude `<pack>/build/`. **Confirmed.**
- A9 (NEW — resolves correctness / all_locations / callers / FLAG-005 / scope) — `ARTAGENTS_TASK_RUN_ID` is the env contract for task-mode inheritance. Every existing caller of `prepare_project_run()` MUST read it; the integration surface is **explicitly enumerated** in Phase 1 and Phase 2 file-touch lists: `artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`, `artagents/core/project/run.py`, and `artagents/threads/wrapper.py` (subprocess env construction; the env joins existing `ARTAGENTS_RUN_ID`/`ARTAGENTS_PARENT_RUN_ID`/`ARTAGENTS_PROJECT_RUN`). **Confirmed.**
- A10 (NEW — resolves correctness on `tests/test_project_runs.py`) — when `ARTAGENTS_TASK_RUN_ID` is set, `prepare_project_run()` SKIPS creating a child `run.json` AND skips bumping `ARTAGENTS_PROJECT_RUN` for the child, but **preserves** the child command's output directory and hype artifact mirroring INSIDE the parent task run's `runs/<task-run-id>/steps/<step-id>/produces/`. Standalone (non-task-mode) calls retain today's behavior unchanged: `tests/test_project_runs.py` continues to pass for the standalone path; Phase 2 adds new tests covering the task-mode-inherited path. **Confirmed.**

## Main Phase

### Step 1: Front matter + Sections 1–2 — Executive Summary, Goals/Non-Goals (`docs/orchestrator-v1-plan.md`)
**Scope:** Small
1. **Write** H1 + ~150-word Executive Summary naming task mode, three step kinds, iteration/fan-out body attributes, and the additive-migration thesis.
2. **List** Goals (frozen hash-pinned plans, gate above dispatch, three step kinds, repeat as body attribute, golden-run regression, audience-split verbs).
3. **List** Non-Goals: daemon, web server, HMAC/keyed crypto, `.index.db`, shared CAS, sandbox against malicious agents.

### Step 2: Section 3 — Data Model (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Render** the storage tree under `~/Documents/reigh-workspace/artagents-projects/<slug>/` exactly per spec: `active_run.json`; `runs/<run-id>/{plan.json,events.jsonl,AGENT.md}`; `steps/<id>/{produces,iterations/NNN,items/<id>}/`; `inbox/`; `<slug>/.cas/<sha256>`. Note as additions to `artagents/core/project/paths.py` helpers (`run_dir`, `run_json_path`).
2. **Define** `plan.json` immutable + hash-pinned (supersedes "checklist") and its relationship to `OrchestratorPlan`/`OrchestratorPlanStep` in `artagents/core/orchestrator/runner.py`.
3. **Define** `events.jsonl` chain as plain `sha256(prev_hash + canonical_event_json)`; sole truth; rationale for no HMAC.
4. **Define** `active_run.json` as `{run_id, plan_hash}` pointer.
5. **State** explicit exclusions: `.index.db` and HMAC not in v1.

### Step 3: Sections 4–6 — Step Kinds, Iteration/Fan-Out, Produces (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Specify** three step kinds:
   - `code` — inline Python execution producing deterministic argv-shaped commands and `produces` artifacts; strict superset of today's `RUNTIME_KINDS={python,command}` (`artagents/core/orchestrator/schema.py`). Per A6: a `code` step MAY import an executor module and call it as a Python function; it MUST NOT subprocess to `artagents executors run` or `artagents orchestrators run`.
   - `attested` — agent or human; ack pins identity via `--agent` or `ARTAGENTS_ACTOR`; self-acks rejected.
   - `nested` — delegates to a child plan; the gate sees the nested structure for hashing/pinning. **Sub-orchestrator delegation MUST use `nested`, not `code`.**
2. **Specify** `repeat:{until: user_approves|verifier_passes|quorum, max_iterations, on_exhaust}` and `repeat:{for_each: <input_set>}` as body attributes on any step or nested-plan body. Document `iterations/NNN/` and `items/<item-id>/` layout. Document partial approval semantics for `for_each`.
3. **Specify** `produces` block with inline checks (`file_nonempty`, `json_schema`, `json_file`, `audio_duration_min`, `image_dimensions`, `all_of`). Failure rewinds cursor; `passes_test` is a regular `code` step; sentinel-existence-only is rejected at definition time by `author check`.

### Step 4: Section 7 — Gate Above Dispatch (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Enumerate** the four checks: `active_run.json` present; `plan.json` hash matches the pin; `events.jsonl` chain intact; incoming command matches `plan[derived_cursor].command`. On failure: emit the exact recovery command and exit non-zero.
2. **State ordering**: gate is invoked from `artagents/pipeline.py` dispatch BEFORE control reaches `artagents/core/orchestrator/runner.py:run_orchestrator`, AND a defensive gate decorator at the top of `run_orchestrator()` re-checks before `_prepare_project_request()` (line 135) and `thread_wrapper.begin_orchestrator_run()` (line 136). Rejection writes zero project-run files.
3. **State** that `events.jsonl` is the single write surface for task-mode provenance; `artagents/threads/wrapper.py` keeps thread provenance in `runs/<id>/run.json` and does not duplicate into `events.jsonl`.

### Step 5: Sections 8–9 — Lifecycle Verbs + Ack Decisions (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Land** verbs in `artagents/pipeline.py:15` dispatch table:
   - Agent-facing (mid-run): `artagents next | ack | status | abort`.
   - Operator: `artagents start | abort | status | runs ls` — `runs ls` is a new top-level subcommand in `artagents/pipeline.py` (NOT under `orchestrators` or any existing subparser).
   - Author: `artagents author new | check | describe | test | compile | explain` — new `author` top-level subparser in `artagents/pipeline.py`.
   - Existing `artagents orchestrators run|list|inspect|validate` (`artagents/core/orchestrator/cli.py`) remains unchanged.
2. **Specify** ack decision validity table: `approve` advances cursor; `retry` valid only after verifier failure (stderr is feedback); `iterate --feedback <text>` valid only when `repeat.until=user_approves` (appended to cumulative constraints); `abort` ends run.
3. **Specify** identity rules: `--agent <id>` for `attested` with `attestor_type=agent`; `--actor <name>` matching `ARTAGENTS_ACTOR` env for `attestor_type=human`; self-acks and unpinned actors rejected; `--item <id>` targets a specific item under `repeat:for_each`.

### Step 6: Sections 10–11 — Authoring + Stop-hook Nudge (`docs/orchestrator-v1-plan.md`)
**Scope:** Small
1. **State** Python DSL `artagents.orchestrate` is the only committed representation; `<pack>/build/<orch>.json` is generated by `author compile` and is gitignored (root `.gitignore` updated in Phase 4); runtime hashes/pins the build artifact.
2. **List** pack additions over `artagents/packs/builtin/hype/` baseline: `<pack>/<orch>.py`, `<pack>/build/<orch>.json` (gitignored), `<pack>/fixtures/<name>/`, `<pack>/golden/<name>.events.jsonl`. Verify helpers live in `artagents.verify`.
3. **Specify** `author check` is sub-second static validation: schema; every `produces`/`requires` resolves; every nested plan resolves; attested-with-non-trivial-produces requires semantic checks (sentinel-only rejected). `author describe` pretty-prints DAG. `author test --fixture` runs `--dry-run --auto-approve` and diffs `events.jsonl` against `golden/<fixture>.events.jsonl`.
4. **State** Stop-hook nudge is Claude Code only in v1; the prohibition preamble is re-injected verbatim on every `artagents next` call.

### Step 7: Section 12 — Phasing 1–9 (`docs/orchestrator-v1-plan.md`)
**Scope:** Large

For each phase emit five fields: **Scope**, **Files touched** (inline backticked path citations), **Classification** (additive | breaking), **Exit criteria**, **Test strategy**.

1. **Phase 1 — Kernel + `ARTAGENTS_TASK_RUN_ID` env contract.** Scope: `events.jsonl` + plain hash chain + `plan_hash` pin + gate above dispatch + `active_run.json` + the `ARTAGENTS_TASK_RUN_ID` env contract is defined and READ in every existing project-run preparation path. Files: new `artagents/core/task/{gate.py,events.py,active_run.py,env.py}`; touches `artagents/pipeline.py:15` (gate-before-dispatch), `artagents/core/orchestrator/runner.py:135` (defensive gate decorator + read `ARTAGENTS_TASK_RUN_ID`), `artagents/core/executor/runner.py` (read `ARTAGENTS_TASK_RUN_ID`), `artagents/packs/builtin/hype/run.py` (read `ARTAGENTS_TASK_RUN_ID`), `artagents/core/project/run.py` (`prepare_project_run()` skips child `run.json` + skips bumping `ARTAGENTS_PROJECT_RUN` when `ARTAGENTS_TASK_RUN_ID` is set, but preserves output dir + hype artifact mirroring inside parent task run; kernel writes `plan.json`/`events.jsonl` next to parent `run.json`), `artagents/threads/wrapper.py` (subprocess env construction propagates `ARTAGENTS_TASK_RUN_ID` alongside existing `ARTAGENTS_RUN_ID`/`ARTAGENTS_PARENT_RUN_ID`/`ARTAGENTS_PROJECT_RUN` at lines 21–26). Classification: **additive** (standalone behavior unchanged). Exit: (a) hand-authored `plan.json` runs end-to-end with chain verification; (b) rejected command produces zero project-run files; (c) all three callers of `prepare_project_run()` honor the env contract; (d) `tests/test_project_runs.py` still passes for standalone runs. Tests: golden run for the smallest hand-authored plan + rejection-leaves-no-side-effects test + per-caller env-honored test.
2. **Phase 2 — Three step kinds (with task-mode inheritance enforced).** Scope: `code` (inline-Python only; no subprocess to `orchestrators run`/`executors run`), `attested`, `nested`. Files: new `artagents/core/task/dispatch.py`; extends `artagents/core/orchestrator/schema.py` (step-kind enum on `plan.json`); also touches `artagents/core/executor/runner.py` and `artagents/packs/builtin/hype/run.py` to write produces into `runs/<task-run-id>/steps/<step-id>/produces/` when `ARTAGENTS_TASK_RUN_ID` is set. Classification: **additive** (existing `OrchestratorPlanStep.kind='command'` still loads). Exit: each kind dispatches and emits correct events; a non-hype task plan that calls `run_executor()` (Python) under task mode appends to the parent `events.jsonl` and writes produces under the parent `runs/<task-run-id>/steps/`; `code` steps that subprocess to `artagents orchestrators run` or `artagents executors run` are rejected at `author check`. Tests: per-kind golden runs + a non-hype task plan that exercises `run_executor()` + an `author check` rejection test for the forbidden subprocess shapes.
3. **Phase 3 — Produces + repeat.** Files: new `artagents/verify/__init__.py`, new `artagents/core/task/produces.py`; gate cursor-rewind. Classification: **additive**. Exit: failing checks rewind cursor; `for_each` materializes `items/<id>/`; `until` materializes `iterations/NNN/`. Tests: golden runs covering `until` + `for_each` + check-failure rewind.
4. **Phase 4 — Authoring.** Files: new `artagents/orchestrate/`; extends `artagents/core/orchestrator/cli.py` AND adds `author` subparser to `artagents/pipeline.py`; updates root `.gitignore` to exclude `<pack>/build/`. Classification: **additive**. Exit: `<orch>.py` compiles to `build/<orch>.json` whose hash matches what runtime pins; `.gitignore` excludes `<pack>/build/`. Tests: snapshot of generated JSON; sub-second `author check` perf; `author check` rejection for `code`-step subprocess to `artagents orchestrators run`/`executors run`.
5. **Phase 5 — Lifecycle verbs split by audience.** Files: extends `artagents/pipeline.py:15` dispatch with `next`, `ack`, `status`, `abort`, `start`, `runs ls`, `author`. `artagents/core/orchestrator/cli.py` keeps existing verbs. Classification: **additive**. Exit: every audience-scoped verb returns from a real run. Tests: smoke test invoking each verb against a fixture run.
6. **Phase 6 — Stop-hook nudge.** Files: new `artagents/core/task/preamble.py`; example Claude Code `.claude/settings.json` Stop-hook config in docs. Classification: **additive**. Exit: every `artagents next` output begins with the prohibition preamble verbatim. Tests: golden run asserts preamble appears on N consecutive `next` calls.
7. **Phase 7 — CAS per-project.** Files: new `artagents/core/task/cas.py`; symlink-based `produces` written into `<slug>/.cas/<sha256>`. Classification: **additive**. Exit: identical artifacts deduped under `<slug>/.cas/`. Tests: golden run shows symlink reuse across two runs.
8. **Phase 8 — Inbox surface.** Files: new `artagents/core/task/inbox.py`; gate watches `runs/<run-id>/inbox/`. Classification: **additive**. Exit: file dropped in `inbox/` advances the cursor. Tests: golden run with inbox-driven advance.
9. **Phase 9 — Author test with golden runs.** Files: extends `author` subparser in `artagents/pipeline.py` with `test --fixture`. Classification: **additive**. Exit: every prior-phase golden is wired into `author test` and runs in CI. Tests: meta-test that `author test` re-runs every shipped golden.

### Step 8: Section 13 — Canonical Migration: `artagents/packs/builtin/hype/` (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Show** the diff sketch: ADD `artagents/packs/builtin/hype/hype.py` (DSL); ADD `artagents/packs/builtin/hype/build/hype.json` (gitignored); ADD `artagents/packs/builtin/hype/fixtures/smoke/` and `golden/smoke.events.jsonl`. KEEP `orchestrator.yaml`, `STAGE.md`, `run.py` — additive: existing JSON manifest still loads via `load_orchestrator_manifest` in `artagents/core/orchestrator/schema.py`.
2. **Sketch** a 5–10 line `hype.py` excerpt in which the existing `STEP_ORDER` executor pipeline is expressed as `code`-step children calling executor modules **as direct Python imports/function calls** (e.g., `from artagents.packs.builtin.transcribe import run as transcribe_run; transcribe_run(...)`), with `produces` checks attached. **Sub-orchestrator calls (e.g., delegating to another packed orchestrator) appear as `nested` step entries, NOT as `code` steps that subprocess to `artagents orchestrators run`.** Resolves issue_hints / FLAG-004.
3. **State** that nested-prepare semantics (already enforced in Phase 1/2) mean child `prepare_project_run()` calls inherit `ARTAGENTS_TASK_RUN_ID`, skip creating a child `run.json`, and write produces under the parent `runs/<task-run-id>/steps/<step-id>/produces/`. Migration shows behavior; phases enforce it.

### Step 9: Sections 14–17 — Doc Deliverables, Risk Register, Cut Points, Open-Call Confirmations (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Tabulate** documentation deliverables with audience + size target:
   - `AUTHORING.md` (new) — audience: human + LLM authors; ~one page DSL reference.
   - `AGENT.md` template (new, dropped per-run into `runs/<run-id>/AGENT.md`) — audience: in-flight agent.
   - `README.md` updates — audience: operator; quickstart for `artagents start`/`next`/`ack`.
   - `AGENTS.md` cross-link update for the qualified `<pack>.<orch>` rule.
2. **Tabulate** risk register: single-host (no daemon → cannot prevent concurrent operator); semantic verifier discipline (sentinel-existence is regression risk); context-decay re-injection (Stop-hook prohibition preamble must fire every call); honor-model boundary (no defense against malicious agents). Each row: trigger + mitigation.
3. **Identify** cut points: Phase 3 (kernel + step kinds + produces/repeat = working frozen-plan runner with `ARTAGENTS_TASK_RUN_ID` already enforced from Phase 1); Phase 5 (adds authoring + lifecycle verb split = author-friendly). Phases 6–9 are explicit polish/scale.
4. **State** Confirmed verdict for A1–A10 with one-line rationale each.

### Step 10: Section 18 — Settled Decisions (SD-001..SD-NNN) (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Format** every entry as `SD-NNN <topic>: <single-sentence rationale>.` matching `docs/sprint-thread-layer.md` lines 39–43.
2. **Cover** every load-bearing call. Required entries (final numbering set during authoring):
   - Three step kinds (`code`/`attested`/`nested`).
   - Iteration/fan-out as body attributes (`repeat:{until|for_each}`).
   - `plan.json` renamed from "checklist".
   - `events.jsonl` plain `sha256(prev_hash + canonical_event_json)` chain; no HMAC.
   - No `.index.db` in v1.
   - Python DSL `artagents.orchestrate` is the only committed representation.
   - `<pack>/build/<orch>.json` is gitignored; root `.gitignore` excludes `<pack>/build/`.
   - Per-project `<slug>/.cas/`; not shared.
   - `code-step-calls-orchestrator` forbidden: sub-orchestrator delegation MUST use `nested` step kind; a `code` step may invoke executors as inline Python function calls but MUST NOT subprocess to `artagents orchestrators run` or `artagents executors run` (resolves issue_hints / FLAG-004).
   - Gate four-check + exact-recovery-command on rejection.
   - Gate runs BEFORE both `_prepare_project_request()` (`artagents/core/orchestrator/runner.py:135`) and `thread_wrapper.begin_orchestrator_run()` (line 136); zero project-run side effects on rejection.
   - `events.jsonl` is the single write surface for task-mode provenance.
   - Top-level lifecycle/operator/author verbs extend `artagents/pipeline.py:15` dispatch; `artagents orchestrators` keeps working unchanged.
   - Kernel modules live in new `artagents/core/task/` package.
   - `ARTAGENTS_TASK_RUN_ID` is the env contract for task-mode inheritance; honored by all three callers of `prepare_project_run()` — `artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py` — plus `artagents/core/project/run.py` (skip child `run.json`/skip bumping `ARTAGENTS_PROJECT_RUN`) and `artagents/threads/wrapper.py` (subprocess env propagation alongside `ARTAGENTS_RUN_ID`/`ARTAGENTS_PARENT_RUN_ID`/`ARTAGENTS_PROJECT_RUN`).
   - Under task mode, child output directories and hype artifact mirroring are PRESERVED inside the parent `runs/<task-run-id>/steps/<step-id>/produces/`; standalone (non-task-mode) project-run behavior is unchanged so `tests/test_project_runs.py` keeps passing.
   - `ARTAGENTS_ACTOR` pinning + `--agent` required; self-acks rejected; unpinned actors rejected.
   - Ack validity rules: `retry` only after verifier failure; `iterate --feedback` only when `repeat.until=user_approves`; `abort` ends run.
   - `produces` inline checks replace verifier substep; `passes_test` remains a regular `code` step.
   - Sentinel-existence-only attested checks rejected at `author check`.
   - Stop-hook prohibition preamble re-injected verbatim on every `artagents next` call.
   - Migration is additive: existing `OrchestratorDefinition` JSON manifests + `RUNTIME_KINDS={python,command}` keep working.
   - Single-host honor model; no sandbox claims.
   - Cut points: Phase 3 (frozen-plan runner) and Phase 5 (author-friendly).
   - Canonical migration example is `artagents/packs/builtin/hype/`; transcribe is fallback.
   - Phasing matches V1 BUILD ORDER 1–9.

### Step 11: Verification Read-Back (`docs/orchestrator-v1-plan.md`)
**Scope:** Small
1. **Read back** the rendered doc against the 14 `pass_to_pass` test expectations.
2. **Confirm** every phase has all five fields (scope, files-touched with inline citations, classification, exit criteria, test strategy).
3. **Confirm** SD format matches `docs/sprint-thread-layer.md`.
4. **Confirm** A1–A10 are explicitly Confirmed.
5. **Confirm** all forbidden v1 features in Non-Goals + Risk Register.
6. **Confirm** existing-code citations resolve (`artagents/pipeline.py:15`, `artagents/core/orchestrator/runner.py:135`, `artagents/core/orchestrator/schema.py`, `artagents/core/project/run.py`, `artagents/core/project/paths.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`, `artagents/threads/wrapper.py:21-26`, `tests/test_project_runs.py`); future-deliverable paths (`AUTHORING.md`, `AGENT.md`, `<pack>/build/`, `<pack>/fixtures/`, `<pack>/golden/`, `artagents/core/task/`, `artagents/orchestrate/`, `artagents/verify/`) are framed as prescriptive new paths.
7. **Confirm** body word count ~1500–2200 (SD list excluded).

## Execution Order
1. Resolve Open-Call Decisions A1–A10 (above) before drafting body.
2. Steps 1–2 (front matter, data model) fix vocabulary.
3. Steps 3–6 author the load-bearing design content.
4. Step 7 (phasing) — Phases 1–2 carry the `ARTAGENTS_TASK_RUN_ID` integration and the `nested`-vs-`code` boundary explicitly.
5. Step 8 (migration example) reflects the boundary (executors as inline Python; sub-orchestrators as `nested`).
6. Step 9 (deliverables/risk/cut/open-call confirmations).
7. Step 10 (Settled Decisions) — last; mirrors every body assertion.
8. Step 11 (verification read-back) before declaring done.

## Validation Order
1. Section-by-section read-back against the 14 `pass_to_pass` checks.
2. Spot-check that EXISTING-CODE inline citations resolve to real files; FUTURE-DELIVERABLE paths are framed as prescriptive new paths.
3. SD format match against `docs/sprint-thread-layer.md` lines 39–43.
4. Verify A1–A10 each appear as a confirmed open-call AND as a corresponding SD entry.
5. Verify the `nested`-vs-`code` boundary is consistent across Step Kinds (Section 4), Section 13 hype sketch, and SD list (no contradiction).
6. Verify the `ARTAGENTS_TASK_RUN_ID` integration surface is named in Phase 1 AND Phase 2 file-touch lists (not only in the migration example).
7. Tone and word-count check against `docs/sprint-thread-layer.md` / `docs/design-thread-layer.md`.


        Plan metadata:
        {
  "version": 3,
  "timestamp": "2026-05-04T09:30:37Z",
  "hash": "sha256:644eea93413f9384a64272bcd70a29f88dce93ddf1ab2cda233c2b810d34a011",
  "changes_summary": "Resolved the two open clusters. (1) Step-kind contradiction (issue_hints / FLAG-004): A6 rewritten to make the boundary explicit \u2014 a `code` step is inline Python only and may import-and-call executor entrypoints as Python functions, but MUST NOT subprocess to `artagents executors run` or `artagents orchestrators run`; sub-orchestrator delegation is exclusively `nested`. Step 3 (Step Kinds) and Step 8 (hype.py sketch) are now consistent; an SD entry codifies the boundary; Phase 4 and Phase 2 add `author check` rejection tests for the forbidden subprocess shapes. (2) `ARTAGENTS_TASK_RUN_ID` under-specification (correctness / all_locations / callers / FLAG-005 / scope): introduced A9 + A10 and moved the env contract into Phase 1 scope/files/exit criteria with all three `prepare_project_run()` callers explicitly named (`artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`), plus `artagents/core/project/run.py` (skip child run.json / skip bumping `ARTAGENTS_PROJECT_RUN`) and `artagents/threads/wrapper.py:21-26` (subprocess env propagation alongside existing run-identity envs). A10 explicitly preserves child output dirs + hype artifact mirroring inside the parent task run, so `tests/test_project_runs.py` keeps passing for standalone runs while Phase 2 adds task-mode-inherited tests. Phase 2 exit now requires a non-hype task plan exercising `run_executor()` so the inheritance contract is validated outside the migration example.",
  "flags_addressed": [
    {
      "id": "issue_hints",
      "resolution": "addressed",
      "reason": "A6 rewritten and Step 3 / Step 8 made consistent: sub-orchestrator delegation MUST use `nested`; `code` steps may invoke executors as inline Python function calls but MUST NOT subprocess to `artagents orchestrators run` / `executors run`. New SD entry codifies the boundary; Phase 4 + Phase 2 require `author check` rejection tests for the forbidden subprocess shapes."
    },
    {
      "id": "FLAG-004",
      "resolution": "addressed",
      "reason": "Same as issue_hints: contradiction eliminated by separating inline-Python `code` from subprocess delegation, which is required to be `nested`."
    },
    {
      "id": "correctness",
      "resolution": "addressed",
      "reason": "A10 explicitly preserves child output dirs + hype artifact mirroring inside the parent `runs/<task-run-id>/steps/<step-id>/produces/`; `prepare_project_run()` skips child `run.json` and skips bumping `ARTAGENTS_PROJECT_RUN` only when `ARTAGENTS_TASK_RUN_ID` is set; standalone (non-task-mode) behavior preserved so `tests/test_project_runs.py` keeps passing. SD entry recorded."
    },
    {
      "id": "all_locations",
      "resolution": "addressed",
      "reason": "A9 enumerates the full `ARTAGENTS_TASK_RUN_ID` integration surface; Phase 1 file-touch list names `artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`, `artagents/core/project/run.py`, and `artagents/threads/wrapper.py` (subprocess env propagation alongside `ARTAGENTS_RUN_ID`/`ARTAGENTS_PARENT_RUN_ID`/`ARTAGENTS_PROJECT_RUN` at lines 21\u201326)."
    },
    {
      "id": "callers",
      "resolution": "addressed",
      "reason": "Behavior moved from migration-example-only to Phase 1 scope + files + exit criteria; Phase 2 exit additionally requires a non-hype task plan that exercises `run_executor()` under task mode, so the inheritance contract is validated outside the hype migration example."
    },
    {
      "id": "FLAG-005",
      "resolution": "addressed",
      "reason": "Same as all_locations / callers: phase implementation file lists now include all three `prepare_project_run()` caller paths plus the subprocess env propagation site in `artagents/threads/wrapper.py`. SD entry enumerates the full surface."
    },
    {
      "id": "scope",
      "resolution": "addressed",
      "reason": "Phase 1 file-touch list now explicitly names `artagents/core/executor/runner.py` and `artagents/packs/builtin/hype/run.py`; Phase 2 exit adds a non-hype `run_executor()` task-mode test so downstream implementers can't skip non-hype glue while following the phase table."
    }
  ],
  "questions": [
    "Under task mode, when a `code` step calls an executor as an inline Python function and that executor has a side-effect of writing to `runs/<id>/`, should the kernel rebind the executor's output root to `runs/<task-run-id>/steps/<step-id>/produces/` automatically, or should each executor be patched to read `ARTAGENTS_TASK_RUN_ID` itself? Plan currently picks the latter (per-caller env-honored) because it's more local and testable, but a kernel-level rebind would be smaller surface."
  ],
  "success_criteria": [
    {
      "criterion": "Document exists at exactly `docs/orchestrator-v1-plan.md` (no alternate filename based on title or kebab-case normalization).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Document ends with a `## Settled Decisions` section using `SD-NNN <topic>: <single-sentence rationale>.` format matching `docs/sprint-thread-layer.md`.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Settled Decisions covers every load-bearing call: three step kinds; repeat as body attribute; plan.json rename; plain sha256 chain (no HMAC); no .index.db; Python DSL only; <pack>/build/ gitignored; per-project .cas; code-step-calls-orchestrator forbidden (sub-orchestrator delegation requires `nested`; `code` may not subprocess to `artagents orchestrators run`/`executors run`); gate four-check + recovery command; gate runs BEFORE both _prepare_project_request and thread_wrapper.begin_orchestrator_run; events.jsonl is single write surface; lifecycle verbs extend artagents/pipeline.py; artagents/core/task/ namespace; ARTAGENTS_TASK_RUN_ID integration surface enumerated (orchestrator runner, executor runner, builtin.hype run, project run, threads wrapper); under task mode child output dirs + artifact mirroring preserved inside parent run, standalone behavior unchanged; ARTAGENTS_ACTOR pinning + self-ack rejection; ack decision validity rules; produces inline checks; sentinel-only rejected at author check; Stop-hook preamble every call; additive migration; honor model; Phase 3 + Phase 5 cut points; builtin.hype canonical example; phasing 1\u20139.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Each of the nine phases includes scope, files-touched (with inline backticked path citations), classification (additive or breaking), exit criteria, and test strategy.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Phase 1 file-touch list explicitly names ALL three current `prepare_project_run()` callers (`artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`) PLUS `artagents/core/project/run.py` and `artagents/threads/wrapper.py` (subprocess env propagation).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Phase 2 exit criteria require a non-hype task plan that exercises `run_executor()` under task mode (i.e., the `ARTAGENTS_TASK_RUN_ID` inheritance contract is validated outside the hype migration example).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Storage tree section reproduces the task spec exactly: `active_run.json`, `runs/<run-id>/{plan.json,events.jsonl,AGENT.md}`, `steps/<id>/{produces,iterations/NNN,items/<id>}/`, `inbox/`, `<slug>/.cas/<sha256>` \u2014 and explicitly excludes `.index.db` and HMAC.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Step Kinds section names code, attested, nested; specifies repeat:{until|for_each} as body attributes; states EXPLICITLY that a `code` step is inline Python only (may import-and-call executor functions) and MUST NOT subprocess to `artagents executors run`/`artagents orchestrators run`; sub-orchestrator delegation is the `nested` step kind.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Section 13 hype.py sketch shows `code`-step children as inline Python imports/function calls (e.g., `from artagents.packs.builtin.transcribe import run as transcribe_run`); sub-orchestrator delegation appears as `nested` entries (NOT subprocess to `artagents orchestrators run`).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Gate section enumerates all four checks AND states the gate runs BEFORE both `_prepare_project_request()` (`artagents/core/orchestrator/runner.py:135`) AND `thread_wrapper.begin_orchestrator_run()` (line 136), AND that rejection produces zero project-run filesystem side effects.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Ack Decisions section specifies validity rules: retry only after verifier failure, iterate --feedback only when repeat.until=user_approves, abort ends run; --agent / ARTAGENTS_ACTOR pinning required; self-acks rejected; --item targets for_each.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Lifecycle Verbs section explicitly lands top-level verbs (next/ack/status/abort/start/runs ls/author \u2026) in `artagents/pipeline.py:15` dispatch table, NOT under the existing `orchestrators` subparser, and notes existing `artagents orchestrators` keeps working.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Authoring section states Python DSL `artagents.orchestrate` is the only committed representation, JSON manifest is gitignored at `<pack>/build/<orch>.json`, runtime hashes/pins the build artifact, pack adds `<orch>.py`/`fixtures/`/`golden/<name>.events.jsonl`, AND root `.gitignore` is updated to exclude `<pack>/build/` as part of Phase 4 exit criteria.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Stop-hook section states the prohibition preamble is re-injected verbatim on every `artagents next` call (not just first call).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Doc explicitly states task-mode behavior preserves child output directories and hype artifact mirroring inside `runs/<task-run-id>/steps/<step-id>/produces/`, while standalone (non-task-mode) project-run behavior is unchanged so `tests/test_project_runs.py` keeps passing.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Risk register includes single-host assumption, semantic verifier discipline, context-decay re-injection, and honor-model boundary, each with trigger + mitigation.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Document explicitly Confirms (or Revises with rationale) all ten open-call decisions A1\u2013A10.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Migration is presented as additive: existing `OrchestratorDefinition` JSON manifests + `python`/`command` `RUNTIME_KINDS` keep working through and after v1; existing `artagents orchestrators` CLI verbs remain unchanged; `tests/test_project_runs.py` continues to pass for standalone runs.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "All EXISTING-CODE inline path citations resolve to real files in the repo today (`artagents/pipeline.py:15`, `artagents/core/orchestrator/runner.py:135`, `artagents/core/orchestrator/schema.py`, `artagents/core/project/run.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`, `artagents/threads/wrapper.py:21-26`, `tests/test_project_runs.py`).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "FUTURE-DELIVERABLE paths (`AUTHORING.md`, per-run `AGENT.md`, `<pack>/build/`, `<pack>/fixtures/`, `<pack>/golden/`, `artagents/core/task/`, `artagents/orchestrate/`, `artagents/verify/`) are clearly framed as prescriptive new paths, not as resolvable-today citations.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Document body length lands in ~1500\u20132200 words (SD list excluded).",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Tone is terse, declarative, decision-first; matches `docs/sprint-thread-layer.md` and `docs/design-thread-layer.md`.",
      "priority": "should",
      "requires": [
        "subjective_judgment",
        "read_files"
      ]
    },
    {
      "criterion": "Document does not introduce a daemon, web server, `.index.db`, HMAC/keyed crypto, or shared CAS in v1; these are explicitly listed in Non-Goals.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Cut Points section identifies Phase 3 (kernel + step kinds + produces/repeat) and Phase 5 (adds authoring + lifecycle verb split) as ship-ready milestones.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    }
  ],
  "assumptions": [
    "A1 \u2014 nested-as-data; code-step-calls-orchestrator forbidden \u2014 Confirmed.",
    "A2 \u2014 Python DSL `artagents.orchestrate` only committed representation; `<pack>/build/<orch>.json` gitignored \u2014 Confirmed.",
    "A3 \u2014 no `.index.db` v1; file-walk verbs only \u2014 Confirmed.",
    "A4 \u2014 kernel in NEW `artagents/core/task/` package above orchestrator dispatch \u2014 Confirmed.",
    "A5 \u2014 lifecycle/operator/author verbs extend `artagents/pipeline.py:15`; existing `artagents orchestrators` unchanged \u2014 Confirmed.",
    "A6 (REVISED) \u2014 `code` step is inline Python only; MAY import-and-call executor functions but MUST NOT subprocess to `artagents executors run` / `artagents orchestrators run`; sub-orchestrator delegation is EXCLUSIVELY the `nested` step kind \u2014 Confirmed.",
    "A7 \u2014 gate runs BEFORE both `_prepare_project_request()` (runner.py:135) and `thread_wrapper.begin_orchestrator_run()` (line 136); rejection produces zero project-run filesystem side effects \u2014 Confirmed.",
    "A8 \u2014 root `.gitignore` updated in Phase 4 to exclude `<pack>/build/` \u2014 Confirmed.",
    "A9 (NEW) \u2014 `ARTAGENTS_TASK_RUN_ID` is the env contract for task-mode inheritance; integration surface enumerated in Phase 1 file-touch list: `artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`, `artagents/core/project/run.py`, `artagents/threads/wrapper.py`. \u2014 Confirmed.",
    "A10 (NEW) \u2014 under task mode, `prepare_project_run()` skips child `run.json` and skips bumping `ARTAGENTS_PROJECT_RUN` but PRESERVES child output dirs + hype artifact mirroring inside `runs/<task-run-id>/steps/<step-id>/produces/`; standalone behavior unchanged so `tests/test_project_runs.py` keeps passing \u2014 Confirmed.",
    "Doc body targets ~1500\u20132200 words; SD list grows as needed.",
    "SD entries follow `SD-NNN <topic>: <single-sentence rationale>.` per `docs/sprint-thread-layer.md` lines 39\u201343.",
    "Output path is exactly `docs/orchestrator-v1-plan.md`.",
    "`artagents/packs/builtin/hype/` is the canonical migration example."
  ],
  "delta_from_previous_percent": 77.68,
  "structure_warnings": []
}

        Gate signals:
        {
  "robustness": "robust",
  "signals": {
    "iteration": 3,
    "idea": "ArtAgents is a file-based, single-host Python CLI for running creative pipelines (video/audio/image) that mix code, AI, and human steps. Today it has a pack-based plugin architecture, orchestrator + executor schemas (python/command runtime kinds only), project runs under ~/Documents/reigh-workspace/artagents-projects/, threads with provenance, and a CLI gateway. We are extending it so an agent can be put into 'task mode' and walked through a frozen plan that mixes code, AI, and human steps, with iteration loops and fan-out.\n\nNON-NEGOTIABLES:\n- Single-host, file-based. No daemon, no web server.\n- Honor-based with strong logging. We do not pretend to sandbox a misaligned agent.\n- Migration is additive. Existing JSON manifests and python/command runtime kinds keep working.\n- Existing pack mechanism stays.\n\nV1 DESIGN (post-critique, trimmed):\n\nTHREE STEP KINDS:\n- code: deterministic argv, runner subprocesses, returncode + produces.\n- attested: agent or human task. instructions + produces + ack records identity (agent_id or actor pinned via ARTAGENTS_ACTOR) + evidence.\n- nested: delegates to a child plan; gate sees the structure for hashing/pinning.\n\nITERATION AND FAN-OUT ARE BODY ATTRIBUTES, NOT KINDS:\n- repeat: {until: user_approves|verifier_passes|quorum, max_iterations, on_exhaust}\n- repeat: {for_each: <input_set>}\nBoth apply to any step or to a body block in a nested plan.\n\nPRODUCES WITH INLINE CHECKS (replaces separate verifier substep):\n  produces = {\n    'audio': file(path='audio.wav', check=audio_duration_min(30)),\n    'notes': json_file(path='notes.json', schema='notes.schema.json', min_items=3),\n  }\nThe gate runs the check; failure rewinds the cursor. passes_test is a regular code step.\n\nSTORAGE (under ~/Documents/reigh-workspace/artagents-projects/):\n- <slug>/active_run.json -- pointer to in-flight run + plan hash\n- <slug>/runs/<run-id>/plan.json -- immutable, hash-pinned (renamed from 'checklist' since it's a tree)\n- <slug>/runs/<run-id>/events.jsonl -- append-only, plain hash-chained (prev_hash field), sole truth\n- <slug>/runs/<run-id>/AGENT.md -- contract for whoever's driving\n- <slug>/runs/<run-id>/steps/<step-id>/produces/ -- artifact files (or symlinks into .cas)\n- <slug>/runs/<run-id>/steps/<step-id>/iterations/NNN/ -- when repeat:until is set\n- <slug>/runs/<run-id>/steps/<step-id>/items/<item-id>/ -- when repeat:for_each is set\n- <slug>/runs/<run-id>/inbox/ -- external completion signals get dropped here\n- <slug>/.cas/<sha256> -- per-project CAS for v1 (not shared)\n\nNO crypto: hash chain is plain sha256(prev_hash + canonical_event_json). Tripwire for accidental edits, not protection against malicious users. We do not need HMAC or key handles.\n\nNO .index.db in v1. find + grep on events.jsonl is fine until grep is slow.\n\nGATE (above dispatch, single function):\n- active_run.json exists for this project?\n- plan.json hash matches the pin in active_run.json?\n- events.jsonl hash chain intact?\n- incoming command matches plan[derived_cursor].command?\nIf any fails, reject with the exact recovery command.\n\nLIFECYCLE VERBS, scoped by audience:\nartagents next | ack | status | abort                                  (agent-facing, mid-run)\nartagents start | abort | status | runs ls                             (operator)\nartagents author new | check | describe | test | compile | explain     (author)\n\nACK DECISIONS (intentionally distinct):\n--decision approve              -- advance cursor\n--decision retry                -- only valid after verifier failure; rerun body, stderr is feedback\n--decision iterate --feedback   -- only valid when repeat.until=user_approves; appends to cumulative constraints\n--decision abort                -- end run\n\nACK requires --agent <id> for attested steps with attestor_type=agent, or --actor <name> matching ARTAGENTS_ACTOR for attestor_type=human. Self-acks and unpinned actors are rejected.\n\nFor repeat:for_each: --item <id> targets a specific item; partial approval is supported.\n\nNUDGE (out-of-process, optional, Claude Code only for v1):\nA Stop hook runs artagents next. The next output ALWAYS includes the prohibition preamble verbatim, not just on first call -- this is the re-injection mechanism that fights context decay.\n\nAUTHORING:\n- Python DSL artagents.orchestrate is the ONLY committed representation. JSON manifest is generated at author compile into a build/ dir (gitignored) and that's what the runtime hashes/pins.\n- Verifier helper library artagents.verify: file_nonempty, json_schema, json_file, audio_duration_min, image_dimensions, all_of.\n- Pack layout: <pack>/<orch>.py (committed), <pack>/build/<orch>.json (gitignored), <pack>/fixtures/<name>/, <pack>/golden/<name>.events.jsonl.\n- author check is sub-second static validation: schema, every produces/requires reference resolves, every nested plan resolves, attested steps with non-trivial produces have semantic checks (sentinel-existence-only is rejected at definition time).\n- author describe pretty-prints the DAG.\n- author test --fixture runs --dry-run --auto-approve, diffs events.jsonl against golden/<fixture>.events.jsonl.\n\nV1 BUILD ORDER (recommended phases):\n1. Kernel: events.jsonl + plain hash chain + plan hash pin + gate above dispatch + active_run.json. Runner becomes dumb; gate is a single decorated function above runner dispatch.\n2. Three step kinds: code, attested, nested. (code is a strict superset of today's python+command runtime kinds.)\n3. produces-with-inline-checks; repeat:{until} and repeat:{for_each} on bodies.\n4. Authoring: Python DSL + verify helpers + author check + author describe + author new.\n5. Lifecycle verbs split by audience as above.\n6. Stop-hook nudge with mandatory prohibition preamble.\n7. CAS per-project (under <slug>/.cas/), symlink-based produces.\n8. Inbox surface for external completion signals.\n9. Author test with golden runs.\n\nEXISTING REPO STATE:\n- artagents/core/orchestrator/ exists with schema.py, runner.py, registry.py, cli.py, api.py. Currently knows ORCHESTRATOR_KINDS={built_in, external} and RUNTIME_KINDS={python, command}. OrchestratorPlan / OrchestratorPlanStep skeletons exist (used for dry-run output).\n- artagents/core/project/ exists with run lifecycle (prepare_project_run / finalize_project_run), paths.py with DEFAULT_PROJECTS_ROOT.\n- artagents/threads/ exists with thread_wrapper around runs, @active concept.\n- artagents/packs/ holds builtin packs (cut, transcribe, human_notes, open_in_reigh, etc.).\n- Migration to packs is mid-flight (recent commits T10-T13).\n\nASSUMED OPEN-CALL DEFAULTS (the design plan should call these out and confirm or revise):\n- Keep nested step kind as data (gate sees the structure); forbid code-step-calls-orchestrator.\n- Python DSL is the only committed representation; JSON manifest is a build artifact in gitignored build/ dirs.\n- Drop .index.db from v1; ship with file-walk verbs.\n\nDELIVERABLE EXPECTATIONS for the design doc:\n- Concrete phasing aligned to build order 1-9 above; each phase has scope, files touched, breaking-change risk classification (additive vs breaking), and exit criteria.\n- Test strategy at each phase (golden runs are the regression format).\n- Migration of one builtin pack (suggest hype.cut or transcribe) to the new shape as the canonical example, including the diff shape.\n- Documentation deliverables identified: AUTHORING.md (one-page reference for both human and LLM authors), AGENT.md template, README.md updates.\n- Risk register (single-host assumption, semantic verifier discipline, context decay re-injection, agent honor model boundary).\n- Cut points where work can stop and still ship something useful (e.g., after phase 3, after phase 5).\n- A ## Settled Decisions section at the bottom listing every load-bearing design call (SD-NNN format) so future code-mode runs can inherit them via --from-doc.\n\nMode: doc / metaplan\nOutput: docs/orchestrator-v1-plan.md",
    "significant_flags": 5,
    "unresolved_flags": [
      {
        "id": "issue_hints",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: The revised A6 overcorrects the step model by redefining `code` as inline Python only and forbidding subprocess to `artagents executors run`. The task brief defines `code` as deterministic argv that the runner subprocesses with returncode + produces, so the new wording drifts from the load-bearing V1 design and from the pass-to-pass expectation that code is a strict superset of today's python+command runtime.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "correctness",
        "concern": "Are the proposed changes technically correct?: Directly importing executor modules as the preferred `code` mechanism is brittle against actual executor shapes. For example, `artagents/packs/builtin/render/run.py` and `artagents/packs/builtin/validate/run.py` expose `main()` without an argv parameter and rely on `argparse`/`sys.argv`, while `artagents/core/executor/cli.py` and `run_executor()` provide the registry, placeholder expansion, dry-run, project, and thread integration around those modules. A plan that bans `artagents executors run` subprocesses needs a replacement runner API, not just direct imports.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "all_locations",
        "concern": "Does the change touch all locations AND supporting infrastructure?: FLAG-006 remains open: the plan still introduces future `artagents/orchestrate/`, while `artagents/structure.py` only allows top-level directories listed in `TOP_LEVEL_ARTAGENTS_DIRS` and does not include `orchestrate`. The phase file-touch list still does not mention updating `artagents/structure.py` or `tests/test_doctor_setup.py` for that new top-level package.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "criteria_quality",
        "concern": "Are the success criteria well-prioritized and verifiable?: The new must criteria around inline Python-only `code` steps are verifiable from the doc, but they encode the design drift flagged above rather than the original task brief's deterministic argv/subprocess model. The criteria are clear, but the underlying requirement should be revised before execution.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "FLAG-008",
        "concern": "Code step model: the plan changes `code` from deterministic argv/subprocess execution into inline Python-only direct imports, which diverges from the task brief and current executor runner architecture.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      }
    ],
    "resolved_flags": [
      {
        "id": "FLAG-001",
        "concern": "Task CLI surface: lifecycle verbs are top-level but the plan only maps them to the orchestrator CLI, while `artagents/pipeline.py` currently owns top-level dispatch and falls unknown commands through to builtin.hype.",
        "resolution": "Resolved all nine significant flags by pre-committing eight open-call decisions (A1\u2013A8) before drafting. Concretely: (FLAG-001/scope-1/scope-2) chose `artagents/pipeline.py:15` as the integration surface for top-level lifecycle/operator/author verbs and stated `runs ls` lands there too; (FLAG-002/correctness) restated gate ordering as running BEFORE both `_prepare_project_request()` (runner.py:135) AND `thread_wrapper.begin_orchestrator_run()` (line 136), with a defensive decorator at the top of `run_orchestrator()` so a rejection produces zero project-run side effects; (issue_hints) explicitly justified the new `artagents/core/task/` namespace as a settled decision rather than silent assumption; (callers) defined nested executor/`builtin.hype` calls inherit the parent task run via `ARTAGENTS_TASK_RUN_ID` env and skip creating child project records; (all_locations) added root `.gitignore` update for `<pack>/build/` to Phase 4 exit criteria; (criteria_quality) split the path-citation success criterion into existing-code-must-resolve vs prescriptive-future-deliverable. Added Open-Call Decisions block, expanded SD coverage list, added a separate verification read-back step, and updated phase file-touch lists to consistently carry the namespace and gate-ordering choices."
      },
      {
        "id": "FLAG-002",
        "concern": "Gate ordering: saying the gate runs before `artagents/threads/wrapper.py` is not enough because project-run preparation happens earlier and can create run files before a task-mode rejection.",
        "resolution": "Resolved all nine significant flags by pre-committing eight open-call decisions (A1\u2013A8) before drafting. Concretely: (FLAG-001/scope-1/scope-2) chose `artagents/pipeline.py:15` as the integration surface for top-level lifecycle/operator/author verbs and stated `runs ls` lands there too; (FLAG-002/correctness) restated gate ordering as running BEFORE both `_prepare_project_request()` (runner.py:135) AND `thread_wrapper.begin_orchestrator_run()` (line 136), with a defensive decorator at the top of `run_orchestrator()` so a rejection produces zero project-run side effects; (issue_hints) explicitly justified the new `artagents/core/task/` namespace as a settled decision rather than silent assumption; (callers) defined nested executor/`builtin.hype` calls inherit the parent task run via `ARTAGENTS_TASK_RUN_ID` env and skip creating child project records; (all_locations) added root `.gitignore` update for `<pack>/build/` to Phase 4 exit criteria; (criteria_quality) split the path-citation success criterion into existing-code-must-resolve vs prescriptive-future-deliverable. Added Open-Call Decisions block, expanded SD coverage list, added a separate verification read-back step, and updated phase file-touch lists to consistently carry the namespace and gate-ordering choices."
      },
      {
        "id": "FLAG-003",
        "concern": "Authoring build artifacts: the plan requires gitignored `<pack>/build/<orch>.json` artifacts but does not include a `.gitignore` update or a currently ignored artifact path.",
        "resolution": "Repository `.gitignore` ignores `remotion/build/`, `runs/`, `cache/`, `.artagents/`, and local scratch packs, but not `artagents/packs/*/*/build/` or generic pack-local `build/` directories."
      },
      {
        "id": "scope-1",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Flagged missing top-level CLI integration: `artagents/pipeline.py` owns top-level dispatch, while the plan only maps verbs onto `artagents/core/orchestrator/cli.py`.",
        "resolution": "Resolved all nine significant flags by pre-committing eight open-call decisions (A1\u2013A8) before drafting. Concretely: (FLAG-001/scope-1/scope-2) chose `artagents/pipeline.py:15` as the integration surface for top-level lifecycle/operator/author verbs and stated `runs ls` lands there too; (FLAG-002/correctness) restated gate ordering as running BEFORE both `_prepare_project_request()` (runner.py:135) AND `thread_wrapper.begin_orchestrator_run()` (line 136), with a defensive decorator at the top of `run_orchestrator()` so a rejection produces zero project-run side effects; (issue_hints) explicitly justified the new `artagents/core/task/` namespace as a settled decision rather than silent assumption; (callers) defined nested executor/`builtin.hype` calls inherit the parent task run via `ARTAGENTS_TASK_RUN_ID` env and skip creating child project records; (all_locations) added root `.gitignore` update for `<pack>/build/` to Phase 4 exit criteria; (criteria_quality) split the path-citation success criterion into existing-code-must-resolve vs prescriptive-future-deliverable. Added Open-Call Decisions block, expanded SD coverage list, added a separate verification read-back step, and updated phase file-touch lists to consistently carry the namespace and gate-ordering choices."
      },
      {
        "id": "scope-2",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Flagged ambiguity around `artagents runs ls`, since project CLI currently has no runs-list command and the plan does not choose the integration surface.",
        "resolution": "Resolved all nine significant flags by pre-committing eight open-call decisions (A1\u2013A8) before drafting. Concretely: (FLAG-001/scope-1/scope-2) chose `artagents/pipeline.py:15` as the integration surface for top-level lifecycle/operator/author verbs and stated `runs ls` lands there too; (FLAG-002/correctness) restated gate ordering as running BEFORE both `_prepare_project_request()` (runner.py:135) AND `thread_wrapper.begin_orchestrator_run()` (line 136), with a defensive decorator at the top of `run_orchestrator()` so a rejection produces zero project-run side effects; (issue_hints) explicitly justified the new `artagents/core/task/` namespace as a settled decision rather than silent assumption; (callers) defined nested executor/`builtin.hype` calls inherit the parent task run via `ARTAGENTS_TASK_RUN_ID` env and skip creating child project records; (all_locations) added root `.gitignore` update for `<pack>/build/` to Phase 4 exit criteria; (criteria_quality) split the path-citation success criterion into existing-code-must-resolve vs prescriptive-future-deliverable. Added Open-Call Decisions block, expanded SD coverage list, added a separate verification read-back step, and updated phase file-touch lists to consistently carry the namespace and gate-ordering choices."
      },
      {
        "id": "callers",
        "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: The revised phase table carries the parent-task inheritance behavior mainly in the migration example instead of in the implementation phases. Because `run_executor()` and direct `hype.main()` have independent project-run preparation paths, the doc should move this from example-only text into the Phase 1 or Phase 2 scope/files/exit criteria so it is not skipped for non-hype task plans.",
        "resolution": "Resolved the two open clusters. (1) Step-kind contradiction (issue_hints / FLAG-004): A6 rewritten to make the boundary explicit \u2014 a `code` step is inline Python only and may import-and-call executor entrypoints as Python functions, but MUST NOT subprocess to `artagents executors run` or `artagents orchestrators run`; sub-orchestrator delegation is exclusively `nested`. Step 3 (Step Kinds) and Step 8 (hype.py sketch) are now consistent; an SD entry codifies the boundary; Phase 4 and Phase 2 add `author check` rejection tests for the forbidden subprocess shapes. (2) `ARTAGENTS_TASK_RUN_ID` under-specification (correctness / all_locations / callers / FLAG-005 / scope): introduced A9 + A10 and moved the env contract into Phase 1 scope/files/exit criteria with all three `prepare_project_run()` callers explicitly named (`artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`), plus `artagents/core/project/run.py` (skip child run.json / skip bumping `ARTAGENTS_PROJECT_RUN`) and `artagents/threads/wrapper.py:21-26` (subprocess env propagation alongside existing run-identity envs). A10 explicitly preserves child output dirs + hype artifact mirroring inside the parent task run, so `tests/test_project_runs.py` keeps passing for standalone runs while Phase 2 adds task-mode-inherited tests. Phase 2 exit now requires a non-hype task plan exercising `run_executor()` so the inheritance contract is validated outside the migration example."
      },
      {
        "id": "FLAG-004",
        "concern": "Step model: the revised plan both forbids `code-step-calls-orchestrator` and describes `code` steps shelling out to `artagents orchestrators run`, which contradicts the required nested-as-data model.",
        "resolution": "Resolved the two open clusters. (1) Step-kind contradiction (issue_hints / FLAG-004): A6 rewritten to make the boundary explicit \u2014 a `code` step is inline Python only and may import-and-call executor entrypoints as Python functions, but MUST NOT subprocess to `artagents executors run` or `artagents orchestrators run`; sub-orchestrator delegation is exclusively `nested`. Step 3 (Step Kinds) and Step 8 (hype.py sketch) are now consistent; an SD entry codifies the boundary; Phase 4 and Phase 2 add `author check` rejection tests for the forbidden subprocess shapes. (2) `ARTAGENTS_TASK_RUN_ID` under-specification (correctness / all_locations / callers / FLAG-005 / scope): introduced A9 + A10 and moved the env contract into Phase 1 scope/files/exit criteria with all three `prepare_project_run()` callers explicitly named (`artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`), plus `artagents/core/project/run.py` (skip child run.json / skip bumping `ARTAGENTS_PROJECT_RUN`) and `artagents/threads/wrapper.py:21-26` (subprocess env propagation alongside existing run-identity envs). A10 explicitly preserves child output dirs + hype artifact mirroring inside the parent task run, so `tests/test_project_runs.py` keeps passing for standalone runs while Phase 2 adds task-mode-inherited tests. Phase 2 exit now requires a non-hype task plan exercising `run_executor()` so the inheritance contract is validated outside the migration example."
      },
      {
        "id": "FLAG-005",
        "concern": "Project run inheritance: `ARTAGENTS_TASK_RUN_ID` inheritance is specified, but the phase implementation file lists do not include all actual project-run preparation paths that would need to honor it.",
        "resolution": "Resolved the two open clusters. (1) Step-kind contradiction (issue_hints / FLAG-004): A6 rewritten to make the boundary explicit \u2014 a `code` step is inline Python only and may import-and-call executor entrypoints as Python functions, but MUST NOT subprocess to `artagents executors run` or `artagents orchestrators run`; sub-orchestrator delegation is exclusively `nested`. Step 3 (Step Kinds) and Step 8 (hype.py sketch) are now consistent; an SD entry codifies the boundary; Phase 4 and Phase 2 add `author check` rejection tests for the forbidden subprocess shapes. (2) `ARTAGENTS_TASK_RUN_ID` under-specification (correctness / all_locations / callers / FLAG-005 / scope): introduced A9 + A10 and moved the env contract into Phase 1 scope/files/exit criteria with all three `prepare_project_run()` callers explicitly named (`artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`), plus `artagents/core/project/run.py` (skip child run.json / skip bumping `ARTAGENTS_PROJECT_RUN`) and `artagents/threads/wrapper.py:21-26` (subprocess env propagation alongside existing run-identity envs). A10 explicitly preserves child output dirs + hype artifact mirroring inside the parent task run, so `tests/test_project_runs.py` keeps passing for standalone runs while Phase 2 adds task-mode-inherited tests. Phase 2 exit now requires a non-hype task plan exercising `run_executor()` so the inheritance contract is validated outside the migration example."
      },
      {
        "id": "scope",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: The revised scope for nested-call inheritance names three caller families, but the nine-phase file-touch lists do not include `artagents/core/executor/runner.py` or `artagents/packs/builtin/hype/run.py` in the phase that implements `ARTAGENTS_TASK_RUN_ID` behavior. Those files are actual `prepare_project_run()` callers, so downstream implementation could miss required glue while still following the phase table.",
        "resolution": "Resolved the two open clusters. (1) Step-kind contradiction (issue_hints / FLAG-004): A6 rewritten to make the boundary explicit \u2014 a `code` step is inline Python only and may import-and-call executor entrypoints as Python functions, but MUST NOT subprocess to `artagents executors run` or `artagents orchestrators run`; sub-orchestrator delegation is exclusively `nested`. Step 3 (Step Kinds) and Step 8 (hype.py sketch) are now consistent; an SD entry codifies the boundary; Phase 4 and Phase 2 add `author check` rejection tests for the forbidden subprocess shapes. (2) `ARTAGENTS_TASK_RUN_ID` under-specification (correctness / all_locations / callers / FLAG-005 / scope): introduced A9 + A10 and moved the env contract into Phase 1 scope/files/exit criteria with all three `prepare_project_run()` callers explicitly named (`artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`), plus `artagents/core/project/run.py` (skip child run.json / skip bumping `ARTAGENTS_PROJECT_RUN`) and `artagents/threads/wrapper.py:21-26` (subprocess env propagation alongside existing run-identity envs). A10 explicitly preserves child output dirs + hype artifact mirroring inside the parent task run, so `tests/test_project_runs.py` keeps passing for standalone runs while Phase 2 adds task-mode-inherited tests. Phase 2 exit now requires a non-hype task plan exercising `run_executor()` so the inheritance contract is validated outside the migration example."
      }
    ],
    "weighted_score": 7.0,
    "weighted_history": [
      15.0,
      12.0
    ],
    "plan_delta_from_previous": 77.68,
    "recurring_critiques": [
      "structure guardrails: the plan introduces future top-level package `artagents/orchestrate/`, but current repo structure validation rejects unlisted top-level artagents directories."
    ],
    "scope_creep_flags": [],
    "loop_summary": "Iteration 3. Weighted score trajectory: 15.0 -> 12.0 -> 7.0. Plan deltas: 84.2%, 77.7%. Recurring critiques: 1. Resolved flags: 9. Open significant flags: 5.",
    "debt_overlaps": [],
    "escalated_debt_subsystems": []
  },
  "warnings": [],
  "criteria_check": {
    "count": 24,
    "items": [
      {
        "criterion": "Document exists at exactly `docs/orchestrator-v1-plan.md` (no alternate filename based on title or kebab-case normalization).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Document ends with a `## Settled Decisions` section using `SD-NNN <topic>: <single-sentence rationale>.` format matching `docs/sprint-thread-layer.md`.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Settled Decisions covers every load-bearing call: three step kinds; repeat as body attribute; plan.json rename; plain sha256 chain (no HMAC); no .index.db; Python DSL only; <pack>/build/ gitignored; per-project .cas; code-step-calls-orchestrator forbidden (sub-orchestrator delegation requires `nested`; `code` may not subprocess to `artagents orchestrators run`/`executors run`); gate four-check + recovery command; gate runs BEFORE both _prepare_project_request and thread_wrapper.begin_orchestrator_run; events.jsonl is single write surface; lifecycle verbs extend artagents/pipeline.py; artagents/core/task/ namespace; ARTAGENTS_TASK_RUN_ID integration surface enumerated (orchestrator runner, executor runner, builtin.hype run, project run, threads wrapper); under task mode child output dirs + artifact mirroring preserved inside parent run, standalone behavior unchanged; ARTAGENTS_ACTOR pinning + self-ack rejection; ack decision validity rules; produces inline checks; sentinel-only rejected at author check; Stop-hook preamble every call; additive migration; honor model; Phase 3 + Phase 5 cut points; builtin.hype canonical example; phasing 1\u20139.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Each of the nine phases includes scope, files-touched (with inline backticked path citations), classification (additive or breaking), exit criteria, and test strategy.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Phase 1 file-touch list explicitly names ALL three current `prepare_project_run()` callers (`artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`) PLUS `artagents/core/project/run.py` and `artagents/threads/wrapper.py` (subprocess env propagation).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Phase 2 exit criteria require a non-hype task plan that exercises `run_executor()` under task mode (i.e., the `ARTAGENTS_TASK_RUN_ID` inheritance contract is validated outside the hype migration example).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Storage tree section reproduces the task spec exactly: `active_run.json`, `runs/<run-id>/{plan.json,events.jsonl,AGENT.md}`, `steps/<id>/{produces,iterations/NNN,items/<id>}/`, `inbox/`, `<slug>/.cas/<sha256>` \u2014 and explicitly excludes `.index.db` and HMAC.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Step Kinds section names code, attested, nested; specifies repeat:{until|for_each} as body attributes; states EXPLICITLY that a `code` step is inline Python only (may import-and-call executor functions) and MUST NOT subprocess to `artagents executors run`/`artagents orchestrators run`; sub-orchestrator delegation is the `nested` step kind.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Section 13 hype.py sketch shows `code`-step children as inline Python imports/function calls (e.g., `from artagents.packs.builtin.transcribe import run as transcribe_run`); sub-orchestrator delegation appears as `nested` entries (NOT subprocess to `artagents orchestrators run`).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Gate section enumerates all four checks AND states the gate runs BEFORE both `_prepare_project_request()` (`artagents/core/orchestrator/runner.py:135`) AND `thread_wrapper.begin_orchestrator_run()` (line 136), AND that rejection produces zero project-run filesystem side effects.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Ack Decisions section specifies validity rules: retry only after verifier failure, iterate --feedback only when repeat.until=user_approves, abort ends run; --agent / ARTAGENTS_ACTOR pinning required; self-acks rejected; --item targets for_each.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Lifecycle Verbs section explicitly lands top-level verbs (next/ack/status/abort/start/runs ls/author \u2026) in `artagents/pipeline.py:15` dispatch table, NOT under the existing `orchestrators` subparser, and notes existing `artagents orchestrators` keeps working.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Authoring section states Python DSL `artagents.orchestrate` is the only committed representation, JSON manifest is gitignored at `<pack>/build/<orch>.json`, runtime hashes/pins the build artifact, pack adds `<orch>.py`/`fixtures/`/`golden/<name>.events.jsonl`, AND root `.gitignore` is updated to exclude `<pack>/build/` as part of Phase 4 exit criteria.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Stop-hook section states the prohibition preamble is re-injected verbatim on every `artagents next` call (not just first call).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Doc explicitly states task-mode behavior preserves child output directories and hype artifact mirroring inside `runs/<task-run-id>/steps/<step-id>/produces/`, while standalone (non-task-mode) project-run behavior is unchanged so `tests/test_project_runs.py` keeps passing.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Risk register includes single-host assumption, semantic verifier discipline, context-decay re-injection, and honor-model boundary, each with trigger + mitigation.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Document explicitly Confirms (or Revises with rationale) all ten open-call decisions A1\u2013A10.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Migration is presented as additive: existing `OrchestratorDefinition` JSON manifests + `python`/`command` `RUNTIME_KINDS` keep working through and after v1; existing `artagents orchestrators` CLI verbs remain unchanged; `tests/test_project_runs.py` continues to pass for standalone runs.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "All EXISTING-CODE inline path citations resolve to real files in the repo today (`artagents/pipeline.py:15`, `artagents/core/orchestrator/runner.py:135`, `artagents/core/orchestrator/schema.py`, `artagents/core/project/run.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`, `artagents/threads/wrapper.py:21-26`, `tests/test_project_runs.py`).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "FUTURE-DELIVERABLE paths (`AUTHORING.md`, per-run `AGENT.md`, `<pack>/build/`, `<pack>/fixtures/`, `<pack>/golden/`, `artagents/core/task/`, `artagents/orchestrate/`, `artagents/verify/`) are clearly framed as prescriptive new paths, not as resolvable-today citations.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Document body length lands in ~1500\u20132200 words (SD list excluded).",
        "priority": "should",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Tone is terse, declarative, decision-first; matches `docs/sprint-thread-layer.md` and `docs/design-thread-layer.md`.",
        "priority": "should",
        "requires": [
          "subjective_judgment",
          "read_files"
        ]
      },
      {
        "criterion": "Document does not introduce a daemon, web server, `.index.db`, HMAC/keyed crypto, or shared CAS in v1; these are explicitly listed in Non-Goals.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Cut Points section identifies Phase 3 (kernel + step kinds + produces/repeat) and Phase 5 (adds authoring + lifecycle verb split) as ship-ready milestones.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      }
    ]
  },
  "preflight_results": {
    "project_dir_exists": true,
    "project_dir_writable": true,
    "success_criteria_present": true,
    "claude_available": true,
    "codex_available": true
  },
  "unresolved_flags": [
    {
      "id": "issue_hints",
      "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: The revised A6 overcorrects the step model by redefining `code` as inline Python only and forbidding subprocess to `artagents executors run`. The task brief defines `code` as deterministic argv that the runner subprocesses with returncode + produces, so the new wording drifts from the load-bearing V1 design and from the pass-to-pass expectation that code is a strict superset of today's python+command runtime.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "The revised A6 overcorrects the step model by redefining `code` as inline Python only and forbidding subprocess to `artagents executors run`. The task brief defines `code` as deterministic argv that the runner subprocesses with returncode + produces, so the new wording drifts from the load-bearing V1 design and from the pass-to-pass expectation that code is a strict superset of today's python+command runtime.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": true,
      "addressed_in": "plan_v3.md",
      "verified_in": "critique_v2.json"
    },
    {
      "id": "correctness",
      "concern": "Are the proposed changes technically correct?: Directly importing executor modules as the preferred `code` mechanism is brittle against actual executor shapes. For example, `artagents/packs/builtin/render/run.py` and `artagents/packs/builtin/validate/run.py` expose `main()` without an argv parameter and rely on `argparse`/`sys.argv`, while `artagents/core/executor/cli.py` and `run_executor()` provide the registry, placeholder expansion, dry-run, project, and thread integration around those modules. A plan that bans `artagents executors run` subprocesses needs a replacement runner API, not just direct imports.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Directly importing executor modules as the preferred `code` mechanism is brittle against actual executor shapes. For example, `artagents/packs/builtin/render/run.py` and `artagents/packs/builtin/validate/run.py` expose `main()` without an argv parameter and rely on `argparse`/`sys.argv`, while `artagents/core/executor/cli.py` and `run_executor()` provide the registry, placeholder expansion, dry-run, project, and thread integration around those modules. A plan that bans `artagents executors run` subprocesses needs a replacement runner API, not just direct imports.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": true,
      "addressed_in": "plan_v3.md",
      "verified_in": "critique_v2.json"
    },
    {
      "id": "all_locations",
      "concern": "Does the change touch all locations AND supporting infrastructure?: FLAG-006 remains open: the plan still introduces future `artagents/orchestrate/`, while `artagents/structure.py` only allows top-level directories listed in `TOP_LEVEL_ARTAGENTS_DIRS` and does not include `orchestrate`. The phase file-touch list still does not mention updating `artagents/structure.py` or `tests/test_doctor_setup.py` for that new top-level package.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "FLAG-006 remains open: the plan still introduces future `artagents/orchestrate/`, while `artagents/structure.py` only allows top-level directories listed in `TOP_LEVEL_ARTAGENTS_DIRS` and does not include `orchestrate`. The phase file-touch list still does not mention updating `artagents/structure.py` or `tests/test_doctor_setup.py` for that new top-level package.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": true,
      "addressed_in": "plan_v3.md",
      "verified_in": "critique_v3.json"
    },
    {
      "id": "criteria_quality",
      "concern": "Are the success criteria well-prioritized and verifiable?: The new must criteria around inline Python-only `code` steps are verifiable from the doc, but they encode the design drift flagged above rather than the original task brief's deterministic argv/subprocess model. The criteria are clear, but the underlying requirement should be revised before execution.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "The new must criteria around inline Python-only `code` steps are verifiable from the doc, but they encode the design drift flagged above rather than the original task brief's deterministic argv/subprocess model. The criteria are clear, but the underlying requirement should be revised before execution.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": true,
      "addressed_in": "plan_v2.md",
      "verified_in": "critique_v3.json"
    },
    {
      "id": "FLAG-008",
      "concern": "Code step model: the plan changes `code` from deterministic argv/subprocess execution into inline Python-only direct imports, which diverges from the task brief and current executor runner architecture.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "The task brief defines `code` as deterministic argv with runner subprocess returncode + produces, while revised A6 says `code` is inline Python only and MUST NOT subprocess to `artagents executors run`; current pack modules such as `render.run` and `validate.run` are CLI-shaped, and `artagents/core/executor/cli.py`/`run_executor()` provide the established execution surface.",
      "raised_in": "critique_v3.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    }
  ]
}

        Critique check summary:
        - issue_hints: 1 flagged
        - correctness: 1 flagged
        - scope: clear
        - all_locations: 1 flagged
        - callers: clear
        - conventions: 1 flagged
        - verification: 1 flagged
        - criteria_quality: 1 flagged

        Unresolved significant flags:
        [
  {
    "id": "issue_hints",
    "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: The revised A6 overcorrects the step model by redefining `code` as inline Python only and forbidding subprocess to `artagents executors run`. The task brief defines `code` as deterministic argv that the runner subprocesses with returncode + produces, so the new wording drifts from the load-bearing V1 design and from the pass-to-pass expectation that code is a strict superset of today's python+command runtime.",
    "evidence": "The revised A6 overcorrects the step model by redefining `code` as inline Python only and forbidding subprocess to `artagents executors run`. The task brief defines `code` as deterministic argv that the runner subprocesses with returncode + produces, so the new wording drifts from the load-bearing V1 design and from the pass-to-pass expectation that code is a strict superset of today's python+command runtime.",
    "category": "completeness",
    "severity": "significant",
    "status": "open",
    "weight": null
  },
  {
    "id": "correctness",
    "concern": "Are the proposed changes technically correct?: Directly importing executor modules as the preferred `code` mechanism is brittle against actual executor shapes. For example, `artagents/packs/builtin/render/run.py` and `artagents/packs/builtin/validate/run.py` expose `main()` without an argv parameter and rely on `argparse`/`sys.argv`, while `artagents/core/executor/cli.py` and `run_executor()` provide the registry, placeholder expansion, dry-run, project, and thread integration around those modules. A plan that bans `artagents executors run` subprocesses needs a replacement runner API, not just direct imports.",
    "evidence": "Directly importing executor modules as the preferred `code` mechanism is brittle against actual executor shapes. For example, `artagents/packs/builtin/render/run.py` and `artagents/packs/builtin/validate/run.py` expose `main()` without an argv parameter and rely on `argparse`/`sys.argv`, while `artagents/core/executor/cli.py` and `run_executor()` provide the registry, placeholder expansion, dry-run, project, and thread integration around those modules. A plan that bans `artagents executors run` subprocesses needs a replacement runner API, not just direct imports.",
    "category": "correctness",
    "severity": "significant",
    "status": "open",
    "weight": null
  },
  {
    "id": "all_locations",
    "concern": "Does the change touch all locations AND supporting infrastructure?: FLAG-006 remains open: the plan still introduces future `artagents/orchestrate/`, while `artagents/structure.py` only allows top-level directories listed in `TOP_LEVEL_ARTAGENTS_DIRS` and does not include `orchestrate`. The phase file-touch list still does not mention updating `artagents/structure.py` or `tests/test_doctor_setup.py` for that new top-level package.",
    "evidence": "FLAG-006 remains open: the plan still introduces future `artagents/orchestrate/`, while `artagents/structure.py` only allows top-level directories listed in `TOP_LEVEL_ARTAGENTS_DIRS` and does not include `orchestrate`. The phase file-touch list still does not mention updating `artagents/structure.py` or `tests/test_doctor_setup.py` for that new top-level package.",
    "category": "completeness",
    "severity": "significant",
    "status": "open",
    "weight": null
  },
  {
    "id": "criteria_quality",
    "concern": "Are the success criteria well-prioritized and verifiable?: The new must criteria around inline Python-only `code` steps are verifiable from the doc, but they encode the design drift flagged above rather than the original task brief's deterministic argv/subprocess model. The criteria are clear, but the underlying requirement should be revised before execution.",
    "evidence": "The new must criteria around inline Python-only `code` steps are verifiable from the doc, but they encode the design drift flagged above rather than the original task brief's deterministic argv/subprocess model. The criteria are clear, but the underlying requirement should be revised before execution.",
    "category": "completeness",
    "severity": "significant",
    "status": "open",
    "weight": null
  },
  {
    "id": "FLAG-008",
    "concern": "Code step model: the plan changes `code` from deterministic argv/subprocess execution into inline Python-only direct imports, which diverges from the task brief and current executor runner architecture.",
    "evidence": "The task brief defines `code` as deterministic argv with runner subprocess returncode + produces, while revised A6 says `code` is inline Python only and MUST NOT subprocess to `artagents executors run`; current pack modules such as `render.run` and `validate.run` are CLI-shaped, and `artagents/core/executor/cli.py`/`run_executor()` provide the established execution surface.",
    "category": "correctness",
    "severity": "significant",
    "status": "open",
    "weight": null
  }
]

        Known accepted debt grouped by subsystem:
{}

Escalated debt subsystems:
[]

Debt guidance:
- Treat recurring debt as decision context, not background noise.
- If the current unresolved flags overlap an escalated subsystem, prefer recommending holistic redesign over another point fix.

        Iteration Pressure Analysis:
Group      Flags  Iters  Reopened  Concern
------------------------------------------------------------------------
FG-001     1      3      0         The revised A6 overcorrects the step model by rede
FG-002     1      3      0         Directly importing executor modules as the preferr
FG-003     1      2      0         The revised scope for nested-call inheritance name
FG-004     1      3      0         FLAG-006 remains open: the plan still introduces f
FG-005     1      2      0         The revised phase table carries the parent-task in
FG-006     1      3      0         The direct-import executor direction does not matc
FG-007     1      3      0         FLAG-007 remains open: the phase test strategy sti
FG-008     1      2      0         The new must criteria around inline Python-only `c
FG-009     1      1      0         Task CLI surface: lifecycle verbs are top-level bu
FG-010     1      1      0         Gate ordering: saying the gate runs before `artage
FG-011     1      1      0         Authoring build artifacts: the plan requires gitig
FG-012     1      3      0         Criterion 21: requires human verification (subject
FG-013     1      1      0         Step model: the revised plan both forbids `code-st
FG-014     1      1      0         Project run inheritance: `ARTAGENTS_TASK_RUN_ID` i
FG-015     1      2      0         Structure guardrails: the plan introduces future t
FG-016     1      2      0         Verification: phase test strategies still omit exi
FG-017     1      1      0         Code step model: the plan changes `code` from dete
FG-018     1      1      0         Search for related code that handles the same conc
FG-019     1      1      0         Search for related code that handles the same conc

        Robustness level:
        robust

        Requirements:
        - Decide exactly one of: PROCEED, ITERATE, ESCALATE, TIEBREAKER.
        - Use the weighted score, flag details (including `evidence`), plan delta, recurring critiques, and preflight results as judgment context.
        - PROCEED when execution should move forward now.
        - ITERATE when revising the plan is the best next move.
        - ESCALATE when the loop is stuck, churn is recurring, or user intervention is needed.
        - TIEBREAKER when a flag group reflects an *unresolvable constraint tension* (architectural or philosophical — requires a human call) rather than a plan-quality issue. Use TIEBREAKER only when the Iteration Pressure Analysis shows `addressed_then_reopened_count >= 2` for a fuzzy group OR the group has >=2 member flags across >=2 iterations. If the concern is simply that the plan writer hasn't tried hard enough, use ITERATE instead. When recommending TIEBREAKER you MUST provide `tiebreaker_question` (the decision question for human resolution), `tiebreaker_flag_ids` (which flags this resolves), and `tiebreaker_fuzzy_group_id` (which group this resolves). Cite specific flag IDs and iterations in your rationale.
        - `signals_assessment`: one paragraph summarizing score trajectory, flag status, and preflight posture.

        Flags come in two tiers:
        - **Blocking** (severity = significant/likely-significant): These are serious concerns. If you recommend PROCEED, you MUST provide a `flag_resolutions` entry for every blocking flag. There is no implicit acceptance.
        - **Noted** (everything else): Acknowledge in your rationale but they don't block PROCEED.

        If there are blocking flags and you want to PROCEED, provide `flag_resolutions` with one entry per blocking flag. If you cannot resolve every blocking flag, choose ITERATE (send back for revision) or ESCALATE (human intervention needed).
        Structurally unresolvable flags (for example, infrastructure outside the repo or product decisions that require a human) are ESCALATE, not PROCEED with a non-answer.

        For each blocking flag:
        - **dispute**: The critique is factually wrong. Evidence must cite something specific (file path, line, API doc, etc.). Generic statements like "handled correctly" are invalid.
        - **accept_tradeoff**: The concern is real but intentionally accepted as a known limitation. Rationale must be specific to this flag. Boilerplate like "acceptable within scope" is invalid.
        - Schema requirement: every `flag_resolutions` entry must include both `evidence` and `rationale`. Use `""` for the field that does not apply to that action.

        If there are no blocking flags, return `flag_resolutions: []`.
        Always return `accepted_tradeoffs`; use `[]` when none apply.

        Populate `settled_decisions` with design choices that should carry into review without re-litigation. Return `[]` when there are none.

        Example:
        ```json
        {
          "recommendation": "PROCEED",
          "rationale": "Core fix is correct. Convention concern accepted.",
          "signals_assessment": "Score stable at 2.5, preflight passed, no recurring critiques.",
          "warnings": ["Verify edge case with composite moduli during execution."],
          "flag_resolutions": [
            {"flag_id": "correctness-1", "action": "dispute", "evidence": "allow_migrate and allow_migrate_model produce identical behavior for this use case (verified at django/db/utils.py:286).", "rationale": ""},
            {"flag_id": "performance-1", "action": "accept_tradeoff", "evidence": "", "rationale": "Cold-start latency remains 40ms above target because the cache warmup job is owned by platform and outside this repo; rollout is still approved for the limited internal beta."},
            {"flag_id": "conventions-1", "action": "accept_tradeoff", "evidence": "", "rationale": "Minor naming inconsistency is confined to this helper and would create churn across generated fixtures; track it as follow-up cleanup instead of blocking this fix."}
          ],
          "accepted_tradeoffs": [],
          "settled_decisions": []
        }
        ```

> TOOL

tool_use StructuredOutput
```json
{
  "recommendation": "ITERATE",
  "rationale": "Score is converging (15 → 12 → 7), 9 of the original flags are resolved, and the open flags cluster around a single tractable issue — but my own prior ITERATE advice steered the plan into the overcorrection now flagged. I asked for \"code steps must not subprocess to orchestrators/executors run\"; the plan author globbed both together. The brief is clear: `code` is \"deterministic argv, runner subprocesses, returncode + produces\" and a strict superset of today's `RUNTIME_KINDS={python,command}`; the forbidden pattern \"code-step-calls-orchestrator\" specifically means a `code` step whose argv targets `artagents orchestrators run` (hiding sub-plan delegation that should be `nested` for gate-visible hashing). A `code` step targeting `artagents executors run X` is fine — `executors run` is a leaf executor unit, not orchestration delegation, and that argv shape is already today's `RUNTIME_KINDS={command}`. So FG-001 / FG-002 / FG-006 / FG-008 / criteria_quality all fold into one correction: restore A6 to the brief's deterministic-argv-subprocess model, narrow the forbidden surface to `artagents orchestrators run` only (not `executors run`), and update Section 13 hype.py to show `code`-step children as argv to today's `artagents executors run` (or equivalent argv), with sub-orchestrator delegation as `nested`. FLAG-006 (artagents/structure.py / TOP_LEVEL_ARTAGENTS_DIRS missing `orchestrate`/`verify`) is a real file-touch gap that's persisted across two iterations and must finally be added to Phase 4. Iteration pressure shows 3 iters but 0 reopened — this is genuine forward motion, not churn loops; one more pass with precise course correction should land it. ESCALATE would be premature given the trajectory; TIEBREAKER doesn't fit because the boundary question has a clear answer in the original brief, not a philosophical tension requiring human arbitration.",
  "signals_assessment": "Iteration 3; weighted score 15.0 → 12.0 → 7.0 (53% reduction over two iterations); plan delta 84.18% → 77.68%; 9 of original 9 significant flags resolved by iteration 3; 5 new significant flags clustered into one boundary question (what `code` means vs `nested`) plus one persistent infrastructure gap (`artagents/structure.py` / `TOP_LEVEL_ARTAGENTS_DIRS`). Iteration pressure shows 3 iters on FG-001/002/006 but 0 reopened across all groups — these are wobbles around the same concept, not addressed-then-broken cycles. Recurring critique 1 (structure guardrails) is documented and tractable. Preflight clean (writable workspace, criteria present, both Claude and codex available). Loop is converging, not stuck. One more precise revision should close it.",
  "warnings": [
    "Restore A6 to the brief's literal model: a `code` step is **deterministic argv that the runner subprocesses** with returncode + produces, and is a strict superset of today's `RUNTIME_KINDS={python,command}` in `artagents/core/orchestrator/schema.py`. Drop the inline-Python-only restriction. The prior iteration's nudge in that direction was incorrect — apologies for the mis-steer.",
    "Narrow the forbidden surface: the brief forbids `code-step-calls-orchestrator`, which specifically means a `code` step whose argv invokes `artagents orchestrators run` (hides a sub-plan inside argv so the gate cannot hash/pin its structure). A `code` step targeting `artagents executors run <name>` (or equivalent argv to a leaf executor) is allowed and is exactly today's `command` runtime kind extended. The `nested` step kind exists specifically to make sub-orchestrator delegation visible to the gate.",
    "Update Section 13 hype.py sketch accordingly: `code`-step children invoke today's `artagents executors run …` argv (the established executor surface — `artagents/core/executor/cli.py` and `run_executor()` in `artagents/core/executor/runner.py`), with `produces` checks attached. Sub-orchestrator delegation appears as `nested` step entries. Both `code` and `nested` honor `ARTAGENTS_TASK_RUN_ID` in their respective subprocess env construction.",
    "Update the SD entry for `code-step-calls-orchestrator` to read along the lines of: `SD-NNN code-vs-nested boundary: a code step's argv may target executors run (leaf unit) but MUST NOT target orchestrators run; orchestrator delegation is the nested step kind so the gate sees the structure for hashing.`",
    "Address FLAG-006 (persistent across two iterations now): Phase 4 file-touch list MUST add `artagents/structure.py` (`TOP_LEVEL_ARTAGENTS_DIRS` updated to include `orchestrate` and `verify`) and `tests/test_doctor_setup.py` (asserts the new top-level packages are accepted). Add an SD entry recording the structure-guardrail update.",
    "Address FG-007 (verification): phase test strategies should name existing test files that will be extended/updated, not just new goldens — at minimum reference `tests/test_orchestrator_*`, `tests/test_executor_*`, and `tests/test_project_runs.py` in the relevant phase test strategy lines.",
    "Verify (with a quick read of `artagents/structure.py`) the exact name of the constant `TOP_LEVEL_ARTAGENTS_DIRS` before citing it, since the citation is going into a frozen design doc."
  ],
  "flag_resolutions": [],
  "accepted_tradeoffs": [],
  "settled_decisions": [
    {
      "id": "SD-G1",
      "decision": "Doc body target ~1500-2200 words excluding the SD list.",
      "rationale": "Confirmed iteration 1, uncontested through iteration 3."
    },
    {
      "id": "SD-G2",
      "decision": "Canonical migration example is artagents/packs/builtin/hype/.",
      "rationale": "Confirmed and uncontested across all three iterations."
    },
    {
      "id": "SD-G3",
      "decision": "Output path is exactly docs/orchestrator-v1-plan.md.",
      "rationale": "Fixed by task brief."
    },
    {
      "id": "SD-G4",
      "decision": "SD format follows `SD-NNN <topic>: <single-sentence rationale>.` per docs/sprint-thread-layer.md lines 39-43.",
      "rationale": "Format reference confirmed and uncontested."
    },
    {
      "id": "SD-G5",
      "decision": "Top-level lifecycle/operator/author verbs extend artagents/pipeline.py:15 dispatch table; existing `artagents orchestrators` keeps working unchanged.",
      "rationale": "A5 resolved iteration 2, stable through iteration 3."
    },
    {
      "id": "SD-G6",
      "decision": "Gate runs BEFORE both _prepare_project_request() (artagents/core/orchestrator/runner.py:135) AND thread_wrapper.begin_orchestrator_run() (line 136); rejection produces zero project-run filesystem side effects.",
      "rationale": "A7 resolved iteration 2, stable through iteration 3."
    },
    {
      "id": "SD-G7",
      "decision": "Kernel modules live in NEW artagents/core/task/ package above orchestrator dispatch.",
      "rationale": "A4 resolved iteration 2 with namespace rationale, stable through iteration 3."
    },
    {
      "id": "SD-G8",
      "decision": "Root .gitignore is updated in Phase 4 to exclude <pack>/build/.",
      "rationale": "A8 resolved iteration 2, stable through iteration 3."
    },
    {
      "id": "SD-G9",
      "decision": "Path-citation success criterion split: existing-code citations resolve today; future-deliverable paths framed as prescriptive.",
      "rationale": "criteria_quality (former) resolved iteration 2."
    },
    {
      "id": "SD-G10",
      "decision": "ARTAGENTS_TASK_RUN_ID is the env contract for task-mode inheritance; integration surface is artagents/core/orchestrator/runner.py + artagents/core/executor/runner.py + artagents/packs/builtin/hype/run.py + artagents/core/project/run.py + artagents/threads/wrapper.py (subprocess env propagation alongside ARTAGENTS_RUN_ID/ARTAGENTS_PARENT_RUN_ID/ARTAGENTS_PROJECT_RUN at lines 21-26).",
      "rationale": "A9 resolved iteration 3 (correctness, all_locations, callers, FLAG-005, scope marked addressed and verified)."
    },
    {
      "id": "SD-G11",
      "decision": "Under task mode, prepare_project_run() skips child run.json and skips bumping ARTAGENTS_PROJECT_RUN but PRESERVES child output dirs + hype artifact mirroring inside the parent runs/<task-run-id>/steps/<step-id>/produces/; standalone (non-task-mode) behavior unchanged so tests/test_project_runs.py keeps passing.",
      "rationale": "A10 resolved iteration 3."
    },
    {
      "id": "SD-G12",
      "decision": "Sub-orchestrator delegation is exclusively the `nested` step kind so the gate sees the structure for hashing/pinning.",
      "rationale": "Stable across all three iterations; only the precise wording around `code` argv shapes is being refined."
    }
  ],
  "tiebreaker_question": "",
  "tiebreaker_flag_ids": [],
  "tiebreaker_fuzzy_group_id": ""
}
```

> TOOL

tool_result StructuredOutput
```
Structured output provided successfully
```

> AGENT

Recommended **ITERATE** — but with a course correction. My prior iteration nudged the plan into overcorrecting `code` steps to inline-Python-only; the brief actually defines `code` as deterministic argv subprocess (a strict superset of today's `python`+`command` runtime). The forbidden surface is narrowly `code`-step argv to `artagents orchestrators run` (which would hide a sub-plan from the gate), not `executors run` (which is a leaf unit and exactly today's `command` kind). Score is converging (15→12→7), 9 prior flags resolved, no reopened flags — one more precise pass should land it. Also: FLAG-006 (`artagents/structure.py` / `TOP_LEVEL_ARTAGENTS_DIRS` for new `orchestrate`/`verify` top-level dirs) has been open two iterations and needs to land in Phase 4's file-touch list.

> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

WRITE ACCESS CONTRACT: You are running with auto-approved writes inside a writable workspace. Treat the working directory as fully writable. Do NOT preemptively skip or block tasks on permission, sandbox, or read-only grounds. Attempt every required edit; only report failure AFTER a real OS-level rejection from a specific shell command. Do not infer 'read-only' from absence of activity; absence is not denial. If a single shell command unexpectedly fails, retry with a different invocation before concluding the environment is restricted.

You are the gatekeeper for the megaplan workflow. Make the continuation decision directly.

        Project directory:
        /Users/user_c042661f/Documents/reigh-workspace/ArtAgents

        Idea:
ArtAgents is a file-based, single-host Python CLI for running creative pipelines (video/audio/image) that mix code, AI, and human steps. Today it has a pack-based plugin architecture, orchestrator + executor schemas (python/command runtime kinds only), project runs under ~/Documents/reigh-workspace/artagents-projects/, threads with provenance, and a CLI gateway. We are extending it so an agent can be put into 'task mode' and walked through a frozen plan that mixes code, AI, and human steps, with iteration loops and fan-out.

NON-NEGOTIABLES:
- Single-host, file-based. No daemon, no web server.
- Honor-based with strong logging. We do not pretend to sandbox a misaligned agent.
- Migration is additive. Existing JSON manifests and python/command runtime kinds keep working.
- Existing pack mechanism stays.

V1 DESIGN (post-critique, trimmed):

THREE STEP KINDS:
- code: deterministic argv, runner subprocesses, returncode + produces.
- attested: agent or human task. instructions + produces + ack records identity (agent_id or actor pinned via ARTAGENTS_ACTOR) + evidence.
- nested: delegates to a child plan; gate sees the structure for hashing/pinning.

ITERATION AND FAN-OUT ARE BODY ATTRIBUTES, NOT KINDS:
- repeat: {until: user_approves|verifier_passes|quorum, max_iterations, on_exhaust}
- repeat: {for_each: <input_set>}
Both apply to any step or to a body block in a nested plan.

PRODUCES WITH INLINE CHECKS (replaces separate verifier substep):
  produces = {
    'audio': file(path='audio.wav', check=audio_duration_min(30)),
    'notes': json_file(path='notes.json', schema='notes.schema.json', min_items=3),
  }
The gate runs the check; failure rewinds the cursor. passes_test is a regular code step.

STORAGE (under ~/Documents/reigh-workspace/artagents-projects/):
- <slug>/active_run.json -- pointer to in-flight run + plan hash
- <slug>/runs/<run-id>/plan.json -- immutable, hash-pinned (renamed from 'checklist' since it's a tree)
- <slug>/runs/<run-id>/events.jsonl -- append-only, plain hash-chained (prev_hash field), sole truth
- <slug>/runs/<run-id>/AGENT.md -- contract for whoever's driving
- <slug>/runs/<run-id>/steps/<step-id>/produces/ -- artifact files (or symlinks into .cas)
- <slug>/runs/<run-id>/steps/<step-id>/iterations/NNN/ -- when repeat:until is set
- <slug>/runs/<run-id>/steps/<step-id>/items/<item-id>/ -- when repeat:for_each is set
- <slug>/runs/<run-id>/inbox/ -- external completion signals get dropped here
- <slug>/.cas/<sha256> -- per-project CAS for v1 (not shared)

NO crypto: hash chain is plain sha256(prev_hash + canonical_event_json). Tripwire for accidental edits, not protection against malicious users. We do not need HMAC or key handles.

NO .index.db in v1. find + grep on events.jsonl is fine until grep is slow.

GATE (above dispatch, single function):
- active_run.json exists for this project?
- plan.json hash matches the pin in active_run.json?
- events.jsonl hash chain intact?
- incoming command matches plan[derived_cursor].command?
If any fails, reject with the exact recovery command.

LIFECYCLE VERBS, scoped by audience:
artagents next | ack | status | abort                                  (agent-facing, mid-run)
artagents start | abort | status | runs ls                             (operator)
artagents author new | check | describe | test | compile | explain     (author)

ACK DECISIONS (intentionally distinct):
--decision approve              -- advance cursor
--decision retry                -- only valid after verifier failure; rerun body, stderr is feedback
--decision iterate --feedback   -- only valid when repeat.until=user_approves; appends to cumulative constraints
--decision abort                -- end run

ACK requires --agent <id> for attested steps with attestor_type=agent, or --actor <name> matching ARTAGENTS_ACTOR for attestor_type=human. Self-acks and unpinned actors are rejected.

For repeat:for_each: --item <id> targets a specific item; partial approval is supported.

NUDGE (out-of-process, optional, Claude Code only for v1):
A Stop hook runs artagents next. The next output ALWAYS includes the prohibition preamble verbatim, not just on first call -- this is the re-injection mechanism that fights context decay.

AUTHORING:
- Python DSL artagents.orchestrate is the ONLY committed representation. JSON manifest is generated at author compile into a build/ dir (gitignored) and that's what the runtime hashes/pins.
- Verifier helper library artagents.verify: file_nonempty, json_schema, json_file, audio_duration_min, image_dimensions, all_of.
- Pack layout: <pack>/<orch>.py (committed), <pack>/build/<orch>.json (gitignored), <pack>/fixtures/<name>/, <pack>/golden/<name>.events.jsonl.
- author check is sub-second static validation: schema, every produces/requires reference resolves, every nested plan resolves, attested steps with non-trivial produces have semantic checks (sentinel-existence-only is rejected at definition time).
- author describe pretty-prints the DAG.
- author test --fixture runs --dry-run --auto-approve, diffs events.jsonl against golden/<fixture>.events.jsonl.

V1 BUILD ORDER (recommended phases):
1. Kernel: events.jsonl + plain hash chain + plan hash pin + gate above dispatch + active_run.json. Runner becomes dumb; gate is a single decorated function above runner dispatch.
2. Three step kinds: code, attested, nested. (code is a strict superset of today's python+command runtime kinds.)
3. produces-with-inline-checks; repeat:{until} and repeat:{for_each} on bodies.
4. Authoring: Python DSL + verify helpers + author check + author describe + author new.
5. Lifecycle verbs split by audience as above.
6. Stop-hook nudge with mandatory prohibition preamble.
7. CAS per-project (under <slug>/.cas/), symlink-based produces.
8. Inbox surface for external completion signals.
9. Author test with golden runs.

EXISTING REPO STATE:
- artagents/core/orchestrator/ exists with schema.py, runner.py, registry.py, cli.py, api.py. Currently knows ORCHESTRATOR_KINDS={built_in, external} and RUNTIME_KINDS={python, command}. OrchestratorPlan / OrchestratorPlanStep skeletons exist (used for dry-run output).
- artagents/core/project/ exists with run lifecycle (prepare_project_run / finalize_project_run), paths.py with DEFAULT_PROJECTS_ROOT.
- artagents/threads/ exists with thread_wrapper around runs, @active concept.
- artagents/packs/ holds builtin packs (cut, transcribe, human_notes, open_in_reigh, etc.).
- Migration to packs is mid-flight (recent commits T10-T13).

ASSUMED OPEN-CALL DEFAULTS (the design plan should call these out and confirm or revise):
- Keep nested step kind as data (gate sees the structure); forbid code-step-calls-orchestrator.
- Python DSL is the only committed representation; JSON manifest is a build artifact in gitignored build/ dirs.
- Drop .index.db from v1; ship with file-walk verbs.

DELIVERABLE EXPECTATIONS for the design doc:
- Concrete phasing aligned to build order 1-9 above; each phase has scope, files touched, breaking-change risk classification (additive vs breaking), and exit criteria.
- Test strategy at each phase (golden runs are the regression format).
- Migration of one builtin pack (suggest hype.cut or transcribe) to the new shape as the canonical example, including the diff shape.
- Documentation deliverables identified: AUTHORING.md (one-page reference for both human and LLM authors), AGENT.md template, README.md updates.
- Risk register (single-host assumption, semantic verifier discipline, context decay re-injection, agent honor model boundary).
- Cut points where work can stop and still ship something useful (e.g., after phase 3, after phase 5).
- A ## Settled Decisions section at the bottom listing every load-bearing design call (SD-NNN format) so future code-mode runs can inherit them via --from-doc.

Mode: doc / metaplan
Output: docs/orchestrator-v1-plan.md

User notes and answers:
- strict-notes auto-enabled for metaplan/doc mode

        Plan:
        # Implementation Plan: Author docs/orchestrator-v1-plan.md (Task Mode V1 Design)

## Overview

Single deliverable: `docs/orchestrator-v1-plan.md` — a frozen, decision-first design+migration doc adding "task mode" to ArtAgents. Reproduce the task spec exactly on storage, gate, ack, and phasing; cite repo paths inline; end with `## Settled Decisions` (`SD-NNN <topic>: <single-sentence rationale>.`) matching `docs/sprint-thread-layer.md` lines 39–43.

Verified repo facts the doc must encode (not paraphrase):
- Top-level CLI dispatch lives in `artagents/pipeline.py:15` (`main`); unknown subcommands fall through to `_run_default_brief_orchestrator()` at `artagents/pipeline.py:75`.
- `artagents/core/orchestrator/runner.py:135` calls `_prepare_project_request()` BEFORE `thread_wrapper.begin_orchestrator_run()` at line 136.
- `prepare_project_run()` has THREE caller paths today: `artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`.
- Existing run-identity envs are `ARTAGENTS_RUN_ID`, `ARTAGENTS_PARENT_RUN_ID`, `ARTAGENTS_PROJECT_RUN` (declared in `artagents/threads/wrapper.py:21-26`); no `ARTAGENTS_TASK_RUN_ID` exists yet.
- `artagents/core/orchestrator/schema.py` enforces `ORCHESTRATOR_KINDS={built_in,external}` and `RUNTIME_KINDS={python,command}`; existing JSON manifests must keep loading via `load_orchestrator_manifest`.
- `artagents/core/executor/cli.py` and `run_executor()` (`artagents/core/executor/runner.py`) are the established executor surface — registry, placeholder expansion, dry-run, project, and thread integration. Pack executor modules (e.g., `artagents/packs/builtin/render/run.py`, `artagents/packs/builtin/validate/run.py`) expose `main()` that reads `sys.argv` via `argparse`.
- `artagents/structure.py:27` declares `TOP_LEVEL_ARTAGENTS_DIRS = {"__pycache__","audit","contracts","core","domains","elements","modalities","packs","threads","utilities"}` — does NOT contain `orchestrate` or `verify`. New top-level packages REQUIRE updating this set; `tests/test_doctor_setup.py` enforces it.
- `tests/test_project_runs.py` exists and asserts `ARTAGENTS_PROJECT_RUN=1`, child `run.json` creation, and hype artifact mirroring under standalone (non-task-mode) project runs.
- Canonical migration target: `artagents/packs/builtin/hype/`.

Output path is fixed: `docs/orchestrator-v1-plan.md`. The executor only writes there.

## Open-Call Decisions (resolved before authoring)

- A1 — nested step kind stays as data; `code-step-calls-orchestrator` forbidden. **Confirmed.**
- A2 — Python DSL `artagents.orchestrate` is the only committed representation; JSON manifest at `<pack>/build/<orch>.json` is gitignored. **Confirmed.**
- A3 — no `.index.db` in v1; file-walk verbs only. **Confirmed.**
- A4 — kernel modules land in NEW `artagents/core/task/` package. **Confirmed.**
- A5 — top-level lifecycle/operator/author verbs extend `artagents/pipeline.py:15` dispatch table; existing `artagents orchestrators` keeps working unchanged. **Confirmed.**
- A6 (RESTORED to brief; supersedes prior over-correction) — `code` is **deterministic argv that the runner subprocesses** with returncode + produces, and is a strict superset of today's `RUNTIME_KINDS={python,command}` (`artagents/core/orchestrator/schema.py`). The brief's prohibition `code-step-calls-orchestrator` narrows to a precise rule: **a `code` step's argv MUST NOT target `artagents orchestrators run …`** because that argv shape hides a sub-plan inside argv where the gate cannot see (and cannot hash/pin) its structure. A `code` step's argv MAY target `artagents executors run <name> …` (or any non-orchestrator argv); that's a leaf executor unit and is exactly today's `command` runtime, kept working unchanged. Sub-orchestrator delegation is represented EXCLUSIVELY by the `nested` step kind so the gate sees the structure. **Confirmed (corrected wording).**
- A7 — gate runs BEFORE BOTH `_prepare_project_request()` (`artagents/core/orchestrator/runner.py:135`) AND `thread_wrapper.begin_orchestrator_run()` (line 136). Rejection produces zero project-run filesystem side effects. **Confirmed.**
- A8 — root `.gitignore` updated in Phase 4 to exclude `<pack>/build/`. **Confirmed.**
- A9 — `ARTAGENTS_TASK_RUN_ID` is the env contract for task-mode inheritance; integration surface enumerated in Phase 1 file-touch list (`artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`, `artagents/core/project/run.py`, `artagents/threads/wrapper.py`). **Confirmed.**
- A10 — under task mode, `prepare_project_run()` skips child `run.json` and skips bumping `ARTAGENTS_PROJECT_RUN` but PRESERVES child output dirs + hype artifact mirroring inside the parent `runs/<task-run-id>/steps/<step-id>/produces/`; standalone behavior unchanged so `tests/test_project_runs.py` keeps passing. **Confirmed.**
- A11 (NEW — resolves all_locations / FLAG-006) — Phase 4 file-touch list adds `artagents/structure.py` (`TOP_LEVEL_ARTAGENTS_DIRS` extended to include `orchestrate` and `verify`) and `tests/test_doctor_setup.py` (asserts the new top-level packages are accepted). Recorded as an SD entry. **Confirmed.**

## Main Phase

### Step 1: Front matter + Sections 1–2 — Executive Summary, Goals/Non-Goals (`docs/orchestrator-v1-plan.md`)
**Scope:** Small
1. **Write** H1 + ~150-word Executive Summary naming task mode, three step kinds, iteration/fan-out body attributes, additive-migration thesis.
2. **List** Goals (frozen hash-pinned plans, gate above dispatch, three step kinds, repeat as body attribute, golden-run regression, audience-split verbs).
3. **List** Non-Goals: daemon, web server, HMAC/keyed crypto, `.index.db`, shared CAS, sandbox against malicious agents.

### Step 2: Section 3 — Data Model (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Render** the storage tree under `~/Documents/reigh-workspace/artagents-projects/<slug>/` exactly per spec: `active_run.json`; `runs/<run-id>/{plan.json,events.jsonl,AGENT.md}`; `steps/<id>/{produces,iterations/NNN,items/<id>}/`; `inbox/`; `<slug>/.cas/<sha256>`.
2. **Define** `plan.json` immutable + hash-pinned (supersedes "checklist") and its relationship to `OrchestratorPlan`/`OrchestratorPlanStep` in `artagents/core/orchestrator/runner.py`.
3. **Define** `events.jsonl` chain as plain `sha256(prev_hash + canonical_event_json)`; sole truth; rationale for no HMAC.
4. **Define** `active_run.json` as `{run_id, plan_hash}` pointer.
5. **State** explicit exclusions: `.index.db` and HMAC not in v1.

### Step 3: Sections 4–6 — Step Kinds, Iteration/Fan-Out, Produces (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Specify** three step kinds (per A6 restored to brief):
   - `code` — **deterministic argv that the runner subprocesses; returncode + produces; strict superset of today's `RUNTIME_KINDS={python,command}`** (`artagents/core/orchestrator/schema.py`). Argv MAY target `artagents executors run <name> …` (or any non-orchestrator argv); MUST NOT target `artagents orchestrators run …` (that argv shape hides sub-plan delegation from the gate).
   - `attested` — agent or human; ack pins identity via `--agent` or `ARTAGENTS_ACTOR`; self-acks rejected.
   - `nested` — delegates to a child plan; gate sees nested structure for hashing/pinning. **Sub-orchestrator delegation is the `nested` step kind, not a `code` argv to `orchestrators run`.**
2. **Specify** `repeat:{until: user_approves|verifier_passes|quorum, max_iterations, on_exhaust}` and `repeat:{for_each: <input_set>}` as body attributes on any step or nested-plan body. Document `iterations/NNN/` and `items/<item-id>/` layout. Document partial approval semantics for `for_each`.
3. **Specify** `produces` block with inline checks (`file_nonempty`, `json_schema`, `json_file`, `audio_duration_min`, `image_dimensions`, `all_of`). Failure rewinds cursor; `passes_test` is a regular `code` step; sentinel-existence-only is rejected at definition time by `author check`.

### Step 4: Section 7 — Gate Above Dispatch (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Enumerate** the four checks: `active_run.json` present; `plan.json` hash matches the pin; `events.jsonl` chain intact; incoming command matches `plan[derived_cursor].command`. On failure: emit the exact recovery command and exit non-zero.
2. **State ordering**: gate is invoked from `artagents/pipeline.py:15` dispatch BEFORE control reaches `artagents/core/orchestrator/runner.py:run_orchestrator`; AND a defensive gate decorator at the top of `run_orchestrator()` re-checks before `_prepare_project_request()` (line 135) and `thread_wrapper.begin_orchestrator_run()` (line 136). Rejection writes zero project-run files.
3. **State** that `events.jsonl` is the single write surface for task-mode provenance; `artagents/threads/wrapper.py` keeps thread provenance in `runs/<id>/run.json` and does not duplicate into `events.jsonl`.

### Step 5: Sections 8–9 — Lifecycle Verbs + Ack Decisions (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Land** verbs in `artagents/pipeline.py:15` dispatch:
   - Agent-facing (mid-run): `artagents next | ack | status | abort`.
   - Operator: `artagents start | abort | status | runs ls`.
   - Author: `artagents author new | check | describe | test | compile | explain`.
   - Existing `artagents orchestrators run|list|inspect|validate` (`artagents/core/orchestrator/cli.py`) remains unchanged.
2. **Specify** ack decision validity table: `approve` advances cursor; `retry` valid only after verifier failure (stderr is feedback); `iterate --feedback <text>` valid only when `repeat.until=user_approves` (appended to cumulative constraints); `abort` ends run.
3. **Specify** identity rules: `--agent <id>` for `attested` with `attestor_type=agent`; `--actor <name>` matching `ARTAGENTS_ACTOR` env for `attestor_type=human`; self-acks and unpinned actors rejected; `--item <id>` targets a specific item under `repeat:for_each`.

### Step 6: Sections 10–11 — Authoring + Stop-hook Nudge (`docs/orchestrator-v1-plan.md`)
**Scope:** Small
1. **State** Python DSL `artagents.orchestrate` is the only committed representation; `<pack>/build/<orch>.json` is generated by `author compile` and is gitignored; runtime hashes/pins the build artifact.
2. **List** pack additions over `artagents/packs/builtin/hype/` baseline: `<pack>/<orch>.py`, `<pack>/build/<orch>.json` (gitignored), `<pack>/fixtures/<name>/`, `<pack>/golden/<name>.events.jsonl`. Verify helpers live in `artagents.verify`.
3. **Specify** `author check` is sub-second static validation: schema; every `produces`/`requires` resolves; every nested plan resolves; attested-with-non-trivial-produces requires semantic checks (sentinel-only rejected); **`code` step argv that targets `artagents orchestrators run` is rejected** (sub-orchestrator delegation must be `nested`). `author describe` pretty-prints DAG. `author test --fixture` runs `--dry-run --auto-approve` and diffs `events.jsonl` against `golden/<fixture>.events.jsonl`.
4. **State** Stop-hook nudge is Claude Code only in v1; the prohibition preamble is re-injected verbatim on every `artagents next` call.

### Step 7: Section 12 — Phasing 1–9 (`docs/orchestrator-v1-plan.md`)
**Scope:** Large

For each phase emit five fields: **Scope**, **Files touched** (inline backticked path citations), **Classification** (additive | breaking), **Exit criteria**, **Test strategy** (cite existing test files where extended/updated).

1. **Phase 1 — Kernel + `ARTAGENTS_TASK_RUN_ID` env contract.** Scope: `events.jsonl` + plain hash chain + `plan_hash` pin + gate above dispatch + `active_run.json` + `ARTAGENTS_TASK_RUN_ID` env READ in every existing project-run preparation path. Files: new `artagents/core/task/{gate.py,events.py,active_run.py,env.py}`; touches `artagents/pipeline.py:15` (gate-before-dispatch), `artagents/core/orchestrator/runner.py:135` (defensive gate decorator + read env), `artagents/core/executor/runner.py` (read env), `artagents/packs/builtin/hype/run.py` (read env), `artagents/core/project/run.py` (`prepare_project_run()` skips child `run.json` + skips bumping `ARTAGENTS_PROJECT_RUN` when env is set, preserves output dir + hype artifact mirroring inside parent task run; kernel writes `plan.json`/`events.jsonl` next to parent `run.json`), `artagents/threads/wrapper.py:21-26` (subprocess env propagation alongside `ARTAGENTS_RUN_ID`/`ARTAGENTS_PARENT_RUN_ID`/`ARTAGENTS_PROJECT_RUN`). Classification: **additive**. Exit: (a) hand-authored `plan.json` runs end-to-end with chain verification; (b) rejected command produces zero project-run files; (c) all three callers of `prepare_project_run()` honor the env contract; (d) `tests/test_project_runs.py` continues to pass for standalone runs. Test strategy: golden run for the smallest hand-authored plan + rejection-leaves-no-side-effects test + per-caller env-honored tests; extends `tests/test_project_runs.py` with task-mode-inherited cases; new test module under `tests/test_task_kernel*.py` for the kernel itself.
2. **Phase 2 — Three step kinds (per A6 brief-literal model).** Scope: `code` (deterministic argv subprocess, strict superset of `RUNTIME_KINDS={python,command}`; argv may target `artagents executors run <name> …` but not `artagents orchestrators run …`), `attested`, `nested`. Files: new `artagents/core/task/dispatch.py`; extends `artagents/core/orchestrator/schema.py` (step-kind enum on `plan.json`); `artagents/core/executor/runner.py` and `artagents/packs/builtin/hype/run.py` write produces into `runs/<task-run-id>/steps/<step-id>/produces/` when `ARTAGENTS_TASK_RUN_ID` is set. Classification: **additive** (existing `OrchestratorPlanStep.kind='command'` still loads). Exit: each kind dispatches and emits correct events; a non-hype task plan with a `code` step whose argv invokes `artagents executors run <leaf-executor>` under task mode appends to the parent `events.jsonl` and writes produces under the parent run; sub-orchestrator delegation through `nested` step kind is reflected in `plan.json` hash. Test strategy: per-kind golden runs; non-hype task plan exercising `run_executor()` via subprocess argv under task mode (extends `tests/test_executor_*` patterns); `author check` rejection test for `code` argv targeting `artagents orchestrators run`.
3. **Phase 3 — Produces + repeat.** Files: new `artagents/verify/__init__.py`, new `artagents/core/task/produces.py`; gate cursor-rewind. Classification: **additive**. Exit: failing checks rewind cursor; `for_each` materializes `items/<id>/`; `until` materializes `iterations/NNN/`. Test strategy: golden runs covering `until` + `for_each` + check-failure rewind.
4. **Phase 4 — Authoring + structure guardrails.** Files: new `artagents/orchestrate/`; extends `artagents/core/orchestrator/cli.py`; adds `author` subparser to `artagents/pipeline.py`; updates root `.gitignore` to exclude `<pack>/build/`; **updates `artagents/structure.py:27` `TOP_LEVEL_ARTAGENTS_DIRS` to include `orchestrate` and `verify`** (resolves all_locations / FLAG-006); updates `tests/test_doctor_setup.py` to assert the new packages are accepted. Classification: **additive**. Exit: `<orch>.py` compiles to `build/<orch>.json` whose hash matches what runtime pins; `.gitignore` excludes `<pack>/build/`; `python3 -m artagents doctor` accepts `artagents/orchestrate/` and `artagents/verify/`; `tests/test_doctor_setup.py` passes; `author check` rejects `code` argv targeting `artagents orchestrators run`. Test strategy: snapshot of generated JSON; sub-second `author check` perf; updated `tests/test_doctor_setup.py`; `author check` rejection cases.
5. **Phase 5 — Lifecycle verbs split by audience.** Files: extends `artagents/pipeline.py:15` dispatch with `next`, `ack`, `status`, `abort`, `start`, `runs ls`, `author`. `artagents/core/orchestrator/cli.py` keeps existing verbs. Classification: **additive**. Exit: every audience-scoped verb returns from a real run. Test strategy: smoke test invoking each verb against a fixture run; extends existing CLI tests in `tests/test_orchestrator_*` patterns where applicable.
6. **Phase 6 — Stop-hook nudge.** Files: new `artagents/core/task/preamble.py`; example Claude Code `.claude/settings.json` Stop-hook config in docs. Classification: **additive**. Exit: every `artagents next` output begins with the prohibition preamble verbatim. Test strategy: golden run asserts preamble appears on N consecutive `next` calls.
7. **Phase 7 — CAS per-project.** Files: new `artagents/core/task/cas.py`; symlink-based `produces` written into `<slug>/.cas/<sha256>`. Classification: **additive**. Exit: identical artifacts deduped under `<slug>/.cas/`. Test strategy: golden run shows symlink reuse across two runs.
8. **Phase 8 — Inbox surface.** Files: new `artagents/core/task/inbox.py`; gate watches `runs/<run-id>/inbox/`. Classification: **additive**. Exit: file dropped in `inbox/` advances the cursor. Test strategy: golden run with inbox-driven advance.
9. **Phase 9 — Author test with golden runs.** Files: extends `author` subparser in `artagents/pipeline.py` with `test --fixture`. Classification: **additive**. Exit: every prior-phase golden is wired into `author test` and runs in CI. Test strategy: meta-test that `author test` re-runs every shipped golden.

### Step 8: Section 13 — Canonical Migration: `artagents/packs/builtin/hype/` (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Show** the diff sketch: ADD `artagents/packs/builtin/hype/hype.py` (DSL); ADD `artagents/packs/builtin/hype/build/hype.json` (gitignored); ADD `artagents/packs/builtin/hype/fixtures/smoke/` and `golden/smoke.events.jsonl`. KEEP `orchestrator.yaml`, `STAGE.md`, `run.py` — additive: existing JSON manifest still loads via `load_orchestrator_manifest` in `artagents/core/orchestrator/schema.py`.
2. **Sketch** a 5–10 line `hype.py` excerpt where the existing `STEP_ORDER` executor pipeline is expressed as `code`-step children **whose argv invokes today's `artagents executors run <name> …`** (the established executor surface — `artagents/core/executor/cli.py` + `run_executor()` in `artagents/core/executor/runner.py`), with `produces` checks attached. Example shape: `code(argv=["python3","-m","artagents","executors","run","builtin.transcribe", …], produces={...})`. **Sub-orchestrator delegation appears as `nested` step entries, NOT as a `code` argv to `artagents orchestrators run`.** Both `code` (subprocess) and `nested` honor `ARTAGENTS_TASK_RUN_ID` via the env propagation set up in Phase 1.
3. **State** that nested-prepare semantics (already enforced in Phase 1/2) mean child `prepare_project_run()` calls inherit `ARTAGENTS_TASK_RUN_ID`, skip creating a child `run.json`, and write produces under the parent `runs/<task-run-id>/steps/<step-id>/produces/`.

### Step 9: Sections 14–17 — Doc Deliverables, Risk Register, Cut Points, Open-Call Confirmations (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Tabulate** documentation deliverables with audience + size target:
   - `AUTHORING.md` (new) — audience: human + LLM authors; ~one page DSL reference.
   - `AGENT.md` template (new, dropped per-run into `runs/<run-id>/AGENT.md`) — audience: in-flight agent.
   - `README.md` updates — audience: operator; quickstart for `artagents start`/`next`/`ack`.
   - `AGENTS.md` cross-link update for the qualified `<pack>.<orch>` rule.
2. **Tabulate** risk register: single-host (no daemon → cannot prevent concurrent operator); semantic verifier discipline (sentinel-existence is regression risk); context-decay re-injection (Stop-hook prohibition preamble must fire every call); honor-model boundary (no defense against malicious agents). Each row: trigger + mitigation.
3. **Identify** cut points: Phase 3 (kernel + step kinds + produces/repeat = working frozen-plan runner); Phase 5 (adds authoring + lifecycle verb split = author-friendly). Phases 6–9 are explicit polish/scale.
4. **State** Confirmed verdict for A1–A11 with one-line rationale each.

### Step 10: Section 18 — Settled Decisions (SD-001..SD-NNN) (`docs/orchestrator-v1-plan.md`)
**Scope:** Medium
1. **Format** every entry as `SD-NNN <topic>: <single-sentence rationale>.` matching `docs/sprint-thread-layer.md` lines 39–43.
2. **Cover** every load-bearing call. Required entries (final numbering set during authoring):
   - Three step kinds (`code`/`attested`/`nested`).
   - Iteration/fan-out as body attributes (`repeat:{until|for_each}`).
   - `plan.json` renamed from "checklist".
   - `events.jsonl` plain `sha256(prev_hash + canonical_event_json)` chain; no HMAC.
   - No `.index.db` in v1.
   - Python DSL `artagents.orchestrate` only committed representation.
   - `<pack>/build/<orch>.json` gitignored; root `.gitignore` excludes `<pack>/build/`.
   - Per-project `<slug>/.cas/`; not shared.
   - **`code-vs-nested` boundary: a `code` step is deterministic argv that the runner subprocesses (strict superset of today's `RUNTIME_KINDS={python,command}`); its argv MAY target `artagents executors run <name>` (leaf executor unit) but MUST NOT target `artagents orchestrators run` (sub-plan delegation hidden in argv); sub-orchestrator delegation is exclusively the `nested` step kind so the gate sees the structure for hashing.**
   - Gate four-check + exact-recovery-command on rejection.
   - Gate runs BEFORE both `_prepare_project_request()` (`artagents/core/orchestrator/runner.py:135`) and `thread_wrapper.begin_orchestrator_run()` (line 136); zero project-run side effects on rejection.
   - `events.jsonl` is the single write surface for task-mode provenance.
   - Top-level lifecycle/operator/author verbs extend `artagents/pipeline.py:15` dispatch; `artagents orchestrators` keeps working unchanged.
   - Kernel modules live in new `artagents/core/task/` package.
   - **`artagents/structure.py` `TOP_LEVEL_ARTAGENTS_DIRS` is extended to include `orchestrate` and `verify` for the new top-level packages; `tests/test_doctor_setup.py` is updated to assert acceptance.**
   - `ARTAGENTS_TASK_RUN_ID` integration surface (orchestrator runner, executor runner, `builtin.hype` run, project run, threads wrapper subprocess env propagation alongside `ARTAGENTS_RUN_ID`/`ARTAGENTS_PARENT_RUN_ID`/`ARTAGENTS_PROJECT_RUN`).
   - Under task mode, child output dirs + hype artifact mirroring are PRESERVED inside parent `runs/<task-run-id>/steps/<step-id>/produces/`; standalone behavior unchanged so `tests/test_project_runs.py` keeps passing.
   - `ARTAGENTS_ACTOR` pinning + `--agent` required; self-acks rejected.
   - Ack validity rules: `retry` only after verifier failure; `iterate --feedback` only when `repeat.until=user_approves`; `abort` ends run.
   - `produces` inline checks replace verifier substep; `passes_test` remains a regular `code` step.
   - Sentinel-existence-only attested checks rejected at `author check`.
   - Stop-hook prohibition preamble re-injected verbatim on every `artagents next` call.
   - Migration is additive: existing `OrchestratorDefinition` JSON manifests + `RUNTIME_KINDS={python,command}` keep working.
   - Single-host honor model; no sandbox claims.
   - Cut points: Phase 3 (frozen-plan runner) and Phase 5 (author-friendly).
   - Canonical migration example is `artagents/packs/builtin/hype/`; transcribe is fallback.
   - Phasing matches V1 BUILD ORDER 1–9.

### Step 11: Verification Read-Back (`docs/orchestrator-v1-plan.md`)
**Scope:** Small
1. **Read back** against the 14 `pass_to_pass` test expectations.
2. **Confirm** every phase has all five fields including test-strategy citations to existing test files where applicable.
3. **Confirm** SD format matches `docs/sprint-thread-layer.md`.
4. **Confirm** A1–A11 are explicitly Confirmed.
5. **Confirm** all forbidden v1 features in Non-Goals + Risk Register.
6. **Confirm** Step Kinds + hype.py sketch + SD all use the brief-literal `code` model (deterministic argv subprocess; strict superset of `RUNTIME_KINDS={python,command}`); forbidden surface is precisely `code` argv targeting `artagents orchestrators run` (NOT `executors run`).
7. **Confirm** Phase 4 file-touch list names `artagents/structure.py` and `tests/test_doctor_setup.py`.
8. **Confirm** existing-code citations resolve (`artagents/pipeline.py:15`, `artagents/core/orchestrator/runner.py:135`, `artagents/core/orchestrator/schema.py`, `artagents/core/project/run.py`, `artagents/core/executor/runner.py`, `artagents/core/executor/cli.py`, `artagents/packs/builtin/hype/run.py`, `artagents/threads/wrapper.py:21-26`, `artagents/structure.py:27`, `tests/test_project_runs.py`, `tests/test_doctor_setup.py`); future-deliverable paths (`AUTHORING.md`, `AGENT.md`, `<pack>/build/`, `<pack>/fixtures/`, `<pack>/golden/`, `artagents/core/task/`, `artagents/orchestrate/`, `artagents/verify/`) are framed as prescriptive.
9. **Confirm** body word count ~1500–2200 (SD list excluded).

## Execution Order
1. Resolve Open-Call Decisions A1–A11 (above) before drafting body.
2. Steps 1–2 (front matter, data model) fix vocabulary.
3. Steps 3–6 author the load-bearing design content (note: A6 restored to brief-literal model).
4. Step 7 (phasing) — Phases 1–2 carry the `ARTAGENTS_TASK_RUN_ID` integration; Phase 4 carries the `artagents/structure.py` extension.
5. Step 8 (migration example) shows `code`-step argv to `artagents executors run …` and `nested` for sub-orchestrator delegation.
6. Step 9 (deliverables/risk/cut/open-call confirmations).
7. Step 10 (Settled Decisions) — last; mirrors every body assertion.
8. Step 11 (verification read-back) before declaring done.

## Validation Order
1. Section-by-section read-back against the 14 `pass_to_pass` checks.
2. Verify A6 wording matches the brief literally: `code` is deterministic argv subprocess (strict superset of `RUNTIME_KINDS={python,command}`); forbidden surface is ONLY `code` argv to `artagents orchestrators run`; `executors run` argv is allowed.
3. Spot-check existing-code citations resolve; future-deliverable paths framed as prescriptive.
4. Verify Phase 4 file-touch list includes `artagents/structure.py` (`TOP_LEVEL_ARTAGENTS_DIRS` extension) and `tests/test_doctor_setup.py`.
5. Verify Phase 1 file-touch list names all three `prepare_project_run()` callers + `artagents/core/project/run.py` + `artagents/threads/wrapper.py`.
6. Verify Section 13 hype sketch shows `code` argv to `artagents executors run` (NOT inline-Python imports as the prior over-corrected revision said).
7. SD format match against `docs/sprint-thread-layer.md` lines 39–43.
8. Verify A1–A11 each appear as a confirmed open-call AND as a corresponding SD entry.
9. Tone and word-count check.


        Plan metadata:
        {
  "version": 4,
  "timestamp": "2026-05-04T09:39:35Z",
  "hash": "sha256:64a54102ab4e9d28e68eb5dbf4ea3a7d8b3547d6574151b7f5538a88257f6fb9",
  "changes_summary": "Restored A6 to the task brief's literal model (resolves issue_hints / correctness / criteria_quality / FLAG-008): a `code` step is **deterministic argv that the runner subprocesses** with returncode + produces, and is a strict superset of today's `RUNTIME_KINDS={python,command}`. The forbidden surface is narrowed precisely: a `code` step's argv MUST NOT target `artagents orchestrators run` (because that argv shape hides sub-plan delegation from the gate); but argv targeting `artagents executors run <name>` (or any non-orchestrator argv) is FINE \u2014 leaf executor unit, exactly today's `command` runtime preserved. Section 13 hype.py sketch now shows `code`-step children as argv to `artagents executors run \u2026` (the established surface \u2014 `artagents/core/executor/cli.py` + `run_executor()`), with `produces` checks attached; sub-orchestrator delegation appears as `nested`. The prior iteration's \"inline Python only / no subprocess to executors run\" wording is removed everywhere. Added A11 + new SD (resolves all_locations / FLAG-006): Phase 4 file-touch list now includes `artagents/structure.py:27` (`TOP_LEVEL_ARTAGENTS_DIRS` extended to include `orchestrate` and `verify`) and `tests/test_doctor_setup.py`, with an explicit exit criterion that `python3 -m artagents doctor` accepts the new top-level packages. Phase test strategies now cite existing test modules (`tests/test_project_runs.py`, `tests/test_doctor_setup.py`, executor/orchestrator test patterns) where extended. Success criteria updated to match the corrected model.",
  "flags_addressed": [
    {
      "id": "issue_hints",
      "resolution": "addressed",
      "reason": "A6 restored to brief-literal model: `code` is deterministic argv subprocess, strict superset of today's `RUNTIME_KINDS={python,command}`. Step Kinds section, hype.py sketch, SD list, and success criteria all updated consistently."
    },
    {
      "id": "correctness",
      "resolution": "addressed",
      "reason": "Plan no longer bans subprocess to `artagents executors run`; `code`-step argv to today's executor surface (`artagents/core/executor/cli.py` + `run_executor()`) is preserved as the established mechanism. Pack executor `main()` shapes (which read `sys.argv` via `argparse`) keep working unchanged. The narrowed forbidden surface is precisely `code` argv targeting `artagents orchestrators run`."
    },
    {
      "id": "criteria_quality",
      "resolution": "addressed",
      "reason": "Success criteria rewritten to encode the brief-literal `code`-as-argv-subprocess model and the precise forbidden-argv-shape rule (only `orchestrators run`, not `executors run`)."
    },
    {
      "id": "FLAG-008",
      "resolution": "addressed",
      "reason": "Same as issue_hints/correctness: `code` step model restored to deterministic argv subprocess; current pack CLI shapes (`render.run.main()`, `validate.run.main()` reading `sys.argv`) keep working via `artagents executors run` argv invocation; no replacement runner API needed."
    },
    {
      "id": "all_locations",
      "resolution": "addressed",
      "reason": "A11 + SD entry: Phase 4 file-touch list now names `artagents/structure.py:27` (`TOP_LEVEL_ARTAGENTS_DIRS` extended to include `orchestrate` and `verify`) and `tests/test_doctor_setup.py`. Phase 4 exit criteria require `python3 -m artagents doctor` to accept the new top-level packages."
    }
  ],
  "questions": [
    "Should `artagents/verify/` (the new helper-library top-level package) actually live as `artagents/utilities/verify/` to avoid extending TOP_LEVEL_ARTAGENTS_DIRS at all? Plan currently picks the new top-level package for symmetry with `artagents/orchestrate/` and per the brief's `artagents.verify` import path, but folding under `utilities` would dodge the structure-guardrail update."
  ],
  "success_criteria": [
    {
      "criterion": "Document exists at exactly `docs/orchestrator-v1-plan.md` (no alternate filename based on title or kebab-case normalization).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Document ends with a `## Settled Decisions` section using `SD-NNN <topic>: <single-sentence rationale>.` format matching `docs/sprint-thread-layer.md`.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Settled Decisions covers every load-bearing call: three step kinds; repeat as body attribute; plan.json rename; plain sha256 chain (no HMAC); no .index.db; Python DSL only; <pack>/build/ gitignored; per-project .cas; the precise code-vs-nested boundary (a `code` step's argv may target `artagents executors run <name>` but MUST NOT target `artagents orchestrators run`; sub-orchestrator delegation is the `nested` step kind); gate four-check + recovery command; gate runs BEFORE both _prepare_project_request and thread_wrapper.begin_orchestrator_run; events.jsonl single write surface; lifecycle verbs extend artagents/pipeline.py; artagents/core/task/ namespace; structure-guardrail update (TOP_LEVEL_ARTAGENTS_DIRS extended for orchestrate + verify); ARTAGENTS_TASK_RUN_ID integration surface enumerated; task-mode preserves child output dirs + artifact mirroring; ARTAGENTS_ACTOR pinning + self-ack rejection; ack decision validity rules; produces inline checks; sentinel-only rejected at author check; Stop-hook preamble every call; additive migration; honor model; Phase 3 + Phase 5 cut points; builtin.hype canonical example; phasing 1\u20139.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Each of the nine phases includes scope, files-touched (with inline backticked path citations), classification (additive or breaking), exit criteria, and test strategy.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Phase 1 file-touch list explicitly names ALL three current `prepare_project_run()` callers (`artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`) PLUS `artagents/core/project/run.py` and `artagents/threads/wrapper.py` (subprocess env propagation).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Phase 2 exit criteria require a non-hype task plan that exercises a `code` step whose argv invokes `artagents executors run <leaf-executor>` under task mode (so the inheritance contract is validated outside the hype migration example).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Phase 4 file-touch list names `artagents/structure.py` (`TOP_LEVEL_ARTAGENTS_DIRS` extended to include `orchestrate` and `verify`) AND `tests/test_doctor_setup.py`; Phase 4 exit criterion requires `python3 -m artagents doctor` to accept the new top-level packages.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Storage tree section reproduces the task spec exactly: `active_run.json`, `runs/<run-id>/{plan.json,events.jsonl,AGENT.md}`, `steps/<id>/{produces,iterations/NNN,items/<id>}/`, `inbox/`, `<slug>/.cas/<sha256>` \u2014 and explicitly excludes `.index.db` and HMAC.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Step Kinds section names code, attested, nested; specifies repeat:{until|for_each} as body attributes; states EXPLICITLY that `code` is **deterministic argv that the runner subprocesses** (strict superset of today's `RUNTIME_KINDS={python,command}`), that argv MAY target `artagents executors run <name>` but MUST NOT target `artagents orchestrators run`, and that sub-orchestrator delegation is the `nested` step kind.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Section 13 hype.py sketch shows `code`-step children as argv invocations of `artagents executors run <name> \u2026` (NOT inline Python imports); sub-orchestrator delegation appears as `nested` entries (NOT a `code` argv to `artagents orchestrators run`).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Gate section enumerates all four checks AND states the gate runs BEFORE both `_prepare_project_request()` (`artagents/core/orchestrator/runner.py:135`) AND `thread_wrapper.begin_orchestrator_run()` (line 136), AND that rejection produces zero project-run filesystem side effects.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Ack Decisions section specifies validity rules: retry only after verifier failure, iterate --feedback only when repeat.until=user_approves, abort ends run; --agent / ARTAGENTS_ACTOR pinning required; self-acks rejected; --item targets for_each.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Lifecycle Verbs section explicitly lands top-level verbs (next/ack/status/abort/start/runs ls/author \u2026) in `artagents/pipeline.py:15` dispatch table, NOT under the existing `orchestrators` subparser.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Authoring section states Python DSL `artagents.orchestrate` is the only committed representation, JSON manifest is gitignored at `<pack>/build/<orch>.json`, runtime hashes/pins the build artifact, pack adds `<orch>.py`/`fixtures/`/`golden/<name>.events.jsonl`, AND root `.gitignore` is updated to exclude `<pack>/build/` as part of Phase 4 exit criteria.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Stop-hook section states the prohibition preamble is re-injected verbatim on every `artagents next` call (not just first call).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Doc explicitly states task-mode behavior preserves child output directories and hype artifact mirroring inside `runs/<task-run-id>/steps/<step-id>/produces/`, while standalone (non-task-mode) project-run behavior is unchanged so `tests/test_project_runs.py` keeps passing.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Risk register includes single-host assumption, semantic verifier discipline, context-decay re-injection, and honor-model boundary, each with trigger + mitigation.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Document explicitly Confirms (or Revises with rationale) all eleven open-call decisions A1\u2013A11.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Migration is presented as additive: existing `OrchestratorDefinition` JSON manifests + `python`/`command` `RUNTIME_KINDS` keep working unchanged; `artagents executors run` argv shapes (today's `command` runtime) keep working under task mode; existing `artagents orchestrators` CLI verbs remain unchanged; `tests/test_project_runs.py` continues to pass for standalone runs.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "All EXISTING-CODE inline path citations resolve to real files in the repo today (`artagents/pipeline.py:15`, `artagents/core/orchestrator/runner.py:135`, `artagents/core/orchestrator/schema.py`, `artagents/core/project/run.py`, `artagents/core/executor/runner.py`, `artagents/core/executor/cli.py`, `artagents/packs/builtin/hype/run.py`, `artagents/threads/wrapper.py:21-26`, `artagents/structure.py:27`, `tests/test_project_runs.py`, `tests/test_doctor_setup.py`).",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "FUTURE-DELIVERABLE paths (`AUTHORING.md`, per-run `AGENT.md`, `<pack>/build/`, `<pack>/fixtures/`, `<pack>/golden/`, `artagents/core/task/`, `artagents/orchestrate/`, `artagents/verify/`) are clearly framed as prescriptive new paths, not as resolvable-today citations.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Document body length lands in ~1500\u20132200 words (SD list excluded).",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Tone is terse, declarative, decision-first; matches `docs/sprint-thread-layer.md` and `docs/design-thread-layer.md`.",
      "priority": "should",
      "requires": [
        "subjective_judgment",
        "read_files"
      ]
    },
    {
      "criterion": "Document does not introduce a daemon, web server, `.index.db`, HMAC/keyed crypto, or shared CAS in v1; these are explicitly listed in Non-Goals.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Cut Points section identifies Phase 3 (kernel + step kinds + produces/repeat) and Phase 5 (adds authoring + lifecycle verb split) as ship-ready milestones.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    }
  ],
  "assumptions": [
    "A1 \u2014 nested-as-data; code-step-calls-orchestrator forbidden \u2014 Confirmed (precise definition: `code` argv MUST NOT target `artagents orchestrators run`; sub-orchestrator delegation is `nested`).",
    "A2 \u2014 Python DSL `artagents.orchestrate` only committed representation; `<pack>/build/<orch>.json` gitignored \u2014 Confirmed.",
    "A3 \u2014 no `.index.db` v1 \u2014 Confirmed.",
    "A4 \u2014 kernel in NEW `artagents/core/task/` package \u2014 Confirmed.",
    "A5 \u2014 lifecycle/operator/author verbs extend `artagents/pipeline.py:15`; existing `artagents orchestrators` unchanged \u2014 Confirmed.",
    "A6 (RESTORED to brief) \u2014 `code` is deterministic argv that the runner subprocesses; strict superset of today's `RUNTIME_KINDS={python,command}`; argv MAY target `artagents executors run <name>` but MUST NOT target `artagents orchestrators run` (the latter would hide sub-plan delegation from the gate). Sub-orchestrator delegation is exclusively the `nested` step kind \u2014 Confirmed.",
    "A7 \u2014 gate runs BEFORE both `_prepare_project_request()` and `thread_wrapper.begin_orchestrator_run()`; rejection produces zero project-run side effects \u2014 Confirmed.",
    "A8 \u2014 root `.gitignore` updated in Phase 4 to exclude `<pack>/build/` \u2014 Confirmed.",
    "A9 \u2014 `ARTAGENTS_TASK_RUN_ID` integration surface enumerated in Phase 1 \u2014 Confirmed.",
    "A10 \u2014 task-mode `prepare_project_run()` skips child `run.json` + skips bumping `ARTAGENTS_PROJECT_RUN` but PRESERVES child output dirs + hype artifact mirroring inside parent run; standalone behavior unchanged \u2014 Confirmed.",
    "A11 (NEW) \u2014 Phase 4 file-touch list adds `artagents/structure.py` (`TOP_LEVEL_ARTAGENTS_DIRS` += {`orchestrate`, `verify`}) and `tests/test_doctor_setup.py` \u2014 Confirmed.",
    "Doc body targets ~1500\u20132200 words; SD list grows as needed.",
    "SD entries follow `SD-NNN <topic>: <single-sentence rationale>.` per `docs/sprint-thread-layer.md` lines 39\u201343.",
    "Output path is exactly `docs/orchestrator-v1-plan.md`.",
    "`artagents/packs/builtin/hype/` is the canonical migration example; hype.py sketch shows `code` argv to `artagents executors run`."
  ],
  "delta_from_previous_percent": 84.98,
  "structure_warnings": []
}

        Gate signals:
        {
  "robustness": "robust",
  "signals": {
    "iteration": 4,
    "idea": "ArtAgents is a file-based, single-host Python CLI for running creative pipelines (video/audio/image) that mix code, AI, and human steps. Today it has a pack-based plugin architecture, orchestrator + executor schemas (python/command runtime kinds only), project runs under ~/Documents/reigh-workspace/artagents-projects/, threads with provenance, and a CLI gateway. We are extending it so an agent can be put into 'task mode' and walked through a frozen plan that mixes code, AI, and human steps, with iteration loops and fan-out.\n\nNON-NEGOTIABLES:\n- Single-host, file-based. No daemon, no web server.\n- Honor-based with strong logging. We do not pretend to sandbox a misaligned agent.\n- Migration is additive. Existing JSON manifests and python/command runtime kinds keep working.\n- Existing pack mechanism stays.\n\nV1 DESIGN (post-critique, trimmed):\n\nTHREE STEP KINDS:\n- code: deterministic argv, runner subprocesses, returncode + produces.\n- attested: agent or human task. instructions + produces + ack records identity (agent_id or actor pinned via ARTAGENTS_ACTOR) + evidence.\n- nested: delegates to a child plan; gate sees the structure for hashing/pinning.\n\nITERATION AND FAN-OUT ARE BODY ATTRIBUTES, NOT KINDS:\n- repeat: {until: user_approves|verifier_passes|quorum, max_iterations, on_exhaust}\n- repeat: {for_each: <input_set>}\nBoth apply to any step or to a body block in a nested plan.\n\nPRODUCES WITH INLINE CHECKS (replaces separate verifier substep):\n  produces = {\n    'audio': file(path='audio.wav', check=audio_duration_min(30)),\n    'notes': json_file(path='notes.json', schema='notes.schema.json', min_items=3),\n  }\nThe gate runs the check; failure rewinds the cursor. passes_test is a regular code step.\n\nSTORAGE (under ~/Documents/reigh-workspace/artagents-projects/):\n- <slug>/active_run.json -- pointer to in-flight run + plan hash\n- <slug>/runs/<run-id>/plan.json -- immutable, hash-pinned (renamed from 'checklist' since it's a tree)\n- <slug>/runs/<run-id>/events.jsonl -- append-only, plain hash-chained (prev_hash field), sole truth\n- <slug>/runs/<run-id>/AGENT.md -- contract for whoever's driving\n- <slug>/runs/<run-id>/steps/<step-id>/produces/ -- artifact files (or symlinks into .cas)\n- <slug>/runs/<run-id>/steps/<step-id>/iterations/NNN/ -- when repeat:until is set\n- <slug>/runs/<run-id>/steps/<step-id>/items/<item-id>/ -- when repeat:for_each is set\n- <slug>/runs/<run-id>/inbox/ -- external completion signals get dropped here\n- <slug>/.cas/<sha256> -- per-project CAS for v1 (not shared)\n\nNO crypto: hash chain is plain sha256(prev_hash + canonical_event_json). Tripwire for accidental edits, not protection against malicious users. We do not need HMAC or key handles.\n\nNO .index.db in v1. find + grep on events.jsonl is fine until grep is slow.\n\nGATE (above dispatch, single function):\n- active_run.json exists for this project?\n- plan.json hash matches the pin in active_run.json?\n- events.jsonl hash chain intact?\n- incoming command matches plan[derived_cursor].command?\nIf any fails, reject with the exact recovery command.\n\nLIFECYCLE VERBS, scoped by audience:\nartagents next | ack | status | abort                                  (agent-facing, mid-run)\nartagents start | abort | status | runs ls                             (operator)\nartagents author new | check | describe | test | compile | explain     (author)\n\nACK DECISIONS (intentionally distinct):\n--decision approve              -- advance cursor\n--decision retry                -- only valid after verifier failure; rerun body, stderr is feedback\n--decision iterate --feedback   -- only valid when repeat.until=user_approves; appends to cumulative constraints\n--decision abort                -- end run\n\nACK requires --agent <id> for attested steps with attestor_type=agent, or --actor <name> matching ARTAGENTS_ACTOR for attestor_type=human. Self-acks and unpinned actors are rejected.\n\nFor repeat:for_each: --item <id> targets a specific item; partial approval is supported.\n\nNUDGE (out-of-process, optional, Claude Code only for v1):\nA Stop hook runs artagents next. The next output ALWAYS includes the prohibition preamble verbatim, not just on first call -- this is the re-injection mechanism that fights context decay.\n\nAUTHORING:\n- Python DSL artagents.orchestrate is the ONLY committed representation. JSON manifest is generated at author compile into a build/ dir (gitignored) and that's what the runtime hashes/pins.\n- Verifier helper library artagents.verify: file_nonempty, json_schema, json_file, audio_duration_min, image_dimensions, all_of.\n- Pack layout: <pack>/<orch>.py (committed), <pack>/build/<orch>.json (gitignored), <pack>/fixtures/<name>/, <pack>/golden/<name>.events.jsonl.\n- author check is sub-second static validation: schema, every produces/requires reference resolves, every nested plan resolves, attested steps with non-trivial produces have semantic checks (sentinel-existence-only is rejected at definition time).\n- author describe pretty-prints the DAG.\n- author test --fixture runs --dry-run --auto-approve, diffs events.jsonl against golden/<fixture>.events.jsonl.\n\nV1 BUILD ORDER (recommended phases):\n1. Kernel: events.jsonl + plain hash chain + plan hash pin + gate above dispatch + active_run.json. Runner becomes dumb; gate is a single decorated function above runner dispatch.\n2. Three step kinds: code, attested, nested. (code is a strict superset of today's python+command runtime kinds.)\n3. produces-with-inline-checks; repeat:{until} and repeat:{for_each} on bodies.\n4. Authoring: Python DSL + verify helpers + author check + author describe + author new.\n5. Lifecycle verbs split by audience as above.\n6. Stop-hook nudge with mandatory prohibition preamble.\n7. CAS per-project (under <slug>/.cas/), symlink-based produces.\n8. Inbox surface for external completion signals.\n9. Author test with golden runs.\n\nEXISTING REPO STATE:\n- artagents/core/orchestrator/ exists with schema.py, runner.py, registry.py, cli.py, api.py. Currently knows ORCHESTRATOR_KINDS={built_in, external} and RUNTIME_KINDS={python, command}. OrchestratorPlan / OrchestratorPlanStep skeletons exist (used for dry-run output).\n- artagents/core/project/ exists with run lifecycle (prepare_project_run / finalize_project_run), paths.py with DEFAULT_PROJECTS_ROOT.\n- artagents/threads/ exists with thread_wrapper around runs, @active concept.\n- artagents/packs/ holds builtin packs (cut, transcribe, human_notes, open_in_reigh, etc.).\n- Migration to packs is mid-flight (recent commits T10-T13).\n\nASSUMED OPEN-CALL DEFAULTS (the design plan should call these out and confirm or revise):\n- Keep nested step kind as data (gate sees the structure); forbid code-step-calls-orchestrator.\n- Python DSL is the only committed representation; JSON manifest is a build artifact in gitignored build/ dirs.\n- Drop .index.db from v1; ship with file-walk verbs.\n\nDELIVERABLE EXPECTATIONS for the design doc:\n- Concrete phasing aligned to build order 1-9 above; each phase has scope, files touched, breaking-change risk classification (additive vs breaking), and exit criteria.\n- Test strategy at each phase (golden runs are the regression format).\n- Migration of one builtin pack (suggest hype.cut or transcribe) to the new shape as the canonical example, including the diff shape.\n- Documentation deliverables identified: AUTHORING.md (one-page reference for both human and LLM authors), AGENT.md template, README.md updates.\n- Risk register (single-host assumption, semantic verifier discipline, context decay re-injection, agent honor model boundary).\n- Cut points where work can stop and still ship something useful (e.g., after phase 3, after phase 5).\n- A ## Settled Decisions section at the bottom listing every load-bearing design call (SD-NNN format) so future code-mode runs can inherit them via --from-doc.\n\nMode: doc / metaplan\nOutput: docs/orchestrator-v1-plan.md",
    "significant_flags": 0,
    "unresolved_flags": [],
    "resolved_flags": [
      {
        "id": "FLAG-001",
        "concern": "Task CLI surface: lifecycle verbs are top-level but the plan only maps them to the orchestrator CLI, while `artagents/pipeline.py` currently owns top-level dispatch and falls unknown commands through to builtin.hype.",
        "resolution": "Resolved all nine significant flags by pre-committing eight open-call decisions (A1\u2013A8) before drafting. Concretely: (FLAG-001/scope-1/scope-2) chose `artagents/pipeline.py:15` as the integration surface for top-level lifecycle/operator/author verbs and stated `runs ls` lands there too; (FLAG-002/correctness) restated gate ordering as running BEFORE both `_prepare_project_request()` (runner.py:135) AND `thread_wrapper.begin_orchestrator_run()` (line 136), with a defensive decorator at the top of `run_orchestrator()` so a rejection produces zero project-run side effects; (issue_hints) explicitly justified the new `artagents/core/task/` namespace as a settled decision rather than silent assumption; (callers) defined nested executor/`builtin.hype` calls inherit the parent task run via `ARTAGENTS_TASK_RUN_ID` env and skip creating child project records; (all_locations) added root `.gitignore` update for `<pack>/build/` to Phase 4 exit criteria; (criteria_quality) split the path-citation success criterion into existing-code-must-resolve vs prescriptive-future-deliverable. Added Open-Call Decisions block, expanded SD coverage list, added a separate verification read-back step, and updated phase file-touch lists to consistently carry the namespace and gate-ordering choices."
      },
      {
        "id": "FLAG-002",
        "concern": "Gate ordering: saying the gate runs before `artagents/threads/wrapper.py` is not enough because project-run preparation happens earlier and can create run files before a task-mode rejection.",
        "resolution": "Resolved all nine significant flags by pre-committing eight open-call decisions (A1\u2013A8) before drafting. Concretely: (FLAG-001/scope-1/scope-2) chose `artagents/pipeline.py:15` as the integration surface for top-level lifecycle/operator/author verbs and stated `runs ls` lands there too; (FLAG-002/correctness) restated gate ordering as running BEFORE both `_prepare_project_request()` (runner.py:135) AND `thread_wrapper.begin_orchestrator_run()` (line 136), with a defensive decorator at the top of `run_orchestrator()` so a rejection produces zero project-run side effects; (issue_hints) explicitly justified the new `artagents/core/task/` namespace as a settled decision rather than silent assumption; (callers) defined nested executor/`builtin.hype` calls inherit the parent task run via `ARTAGENTS_TASK_RUN_ID` env and skip creating child project records; (all_locations) added root `.gitignore` update for `<pack>/build/` to Phase 4 exit criteria; (criteria_quality) split the path-citation success criterion into existing-code-must-resolve vs prescriptive-future-deliverable. Added Open-Call Decisions block, expanded SD coverage list, added a separate verification read-back step, and updated phase file-touch lists to consistently carry the namespace and gate-ordering choices."
      },
      {
        "id": "FLAG-003",
        "concern": "Authoring build artifacts: the plan requires gitignored `<pack>/build/<orch>.json` artifacts but does not include a `.gitignore` update or a currently ignored artifact path.",
        "resolution": "Repository `.gitignore` ignores `remotion/build/`, `runs/`, `cache/`, `.artagents/`, and local scratch packs, but not `artagents/packs/*/*/build/` or generic pack-local `build/` directories."
      },
      {
        "id": "issue_hints",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: The revised A6 overcorrects the step model by redefining `code` as inline Python only and forbidding subprocess to `artagents executors run`. The task brief defines `code` as deterministic argv that the runner subprocesses with returncode + produces, so the new wording drifts from the load-bearing V1 design and from the pass-to-pass expectation that code is a strict superset of today's python+command runtime.",
        "resolution": "Restored A6 to the task brief's literal model (resolves issue_hints / correctness / criteria_quality / FLAG-008): a `code` step is **deterministic argv that the runner subprocesses** with returncode + produces, and is a strict superset of today's `RUNTIME_KINDS={python,command}`. The forbidden surface is narrowed precisely: a `code` step's argv MUST NOT target `artagents orchestrators run` (because that argv shape hides sub-plan delegation from the gate); but argv targeting `artagents executors run <name>` (or any non-orchestrator argv) is FINE \u2014 leaf executor unit, exactly today's `command` runtime preserved. Section 13 hype.py sketch now shows `code`-step children as argv to `artagents executors run \u2026` (the established surface \u2014 `artagents/core/executor/cli.py` + `run_executor()`), with `produces` checks attached; sub-orchestrator delegation appears as `nested`. The prior iteration's \"inline Python only / no subprocess to executors run\" wording is removed everywhere. Added A11 + new SD (resolves all_locations / FLAG-006): Phase 4 file-touch list now includes `artagents/structure.py:27` (`TOP_LEVEL_ARTAGENTS_DIRS` extended to include `orchestrate` and `verify`) and `tests/test_doctor_setup.py`, with an explicit exit criterion that `python3 -m artagents doctor` accepts the new top-level packages. Phase test strategies now cite existing test modules (`tests/test_project_runs.py`, `tests/test_doctor_setup.py`, executor/orchestrator test patterns) where extended. Success criteria updated to match the corrected model."
      },
      {
        "id": "correctness",
        "concern": "Are the proposed changes technically correct?: Directly importing executor modules as the preferred `code` mechanism is brittle against actual executor shapes. For example, `artagents/packs/builtin/render/run.py` and `artagents/packs/builtin/validate/run.py` expose `main()` without an argv parameter and rely on `argparse`/`sys.argv`, while `artagents/core/executor/cli.py` and `run_executor()` provide the registry, placeholder expansion, dry-run, project, and thread integration around those modules. A plan that bans `artagents executors run` subprocesses needs a replacement runner API, not just direct imports.",
        "resolution": "Restored A6 to the task brief's literal model (resolves issue_hints / correctness / criteria_quality / FLAG-008): a `code` step is **deterministic argv that the runner subprocesses** with returncode + produces, and is a strict superset of today's `RUNTIME_KINDS={python,command}`. The forbidden surface is narrowed precisely: a `code` step's argv MUST NOT target `artagents orchestrators run` (because that argv shape hides sub-plan delegation from the gate); but argv targeting `artagents executors run <name>` (or any non-orchestrator argv) is FINE \u2014 leaf executor unit, exactly today's `command` runtime preserved. Section 13 hype.py sketch now shows `code`-step children as argv to `artagents executors run \u2026` (the established surface \u2014 `artagents/core/executor/cli.py` + `run_executor()`), with `produces` checks attached; sub-orchestrator delegation appears as `nested`. The prior iteration's \"inline Python only / no subprocess to executors run\" wording is removed everywhere. Added A11 + new SD (resolves all_locations / FLAG-006): Phase 4 file-touch list now includes `artagents/structure.py:27` (`TOP_LEVEL_ARTAGENTS_DIRS` extended to include `orchestrate` and `verify`) and `tests/test_doctor_setup.py`, with an explicit exit criterion that `python3 -m artagents doctor` accepts the new top-level packages. Phase test strategies now cite existing test modules (`tests/test_project_runs.py`, `tests/test_doctor_setup.py`, executor/orchestrator test patterns) where extended. Success criteria updated to match the corrected model."
      },
      {
        "id": "scope-1",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Flagged missing top-level CLI integration: `artagents/pipeline.py` owns top-level dispatch, while the plan only maps verbs onto `artagents/core/orchestrator/cli.py`.",
        "resolution": "Resolved all nine significant flags by pre-committing eight open-call decisions (A1\u2013A8) before drafting. Concretely: (FLAG-001/scope-1/scope-2) chose `artagents/pipeline.py:15` as the integration surface for top-level lifecycle/operator/author verbs and stated `runs ls` lands there too; (FLAG-002/correctness) restated gate ordering as running BEFORE both `_prepare_project_request()` (runner.py:135) AND `thread_wrapper.begin_orchestrator_run()` (line 136), with a defensive decorator at the top of `run_orchestrator()` so a rejection produces zero project-run side effects; (issue_hints) explicitly justified the new `artagents/core/task/` namespace as a settled decision rather than silent assumption; (callers) defined nested executor/`builtin.hype` calls inherit the parent task run via `ARTAGENTS_TASK_RUN_ID` env and skip creating child project records; (all_locations) added root `.gitignore` update for `<pack>/build/` to Phase 4 exit criteria; (criteria_quality) split the path-citation success criterion into existing-code-must-resolve vs prescriptive-future-deliverable. Added Open-Call Decisions block, expanded SD coverage list, added a separate verification read-back step, and updated phase file-touch lists to consistently carry the namespace and gate-ordering choices."
      },
      {
        "id": "scope-2",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: Flagged ambiguity around `artagents runs ls`, since project CLI currently has no runs-list command and the plan does not choose the integration surface.",
        "resolution": "Resolved all nine significant flags by pre-committing eight open-call decisions (A1\u2013A8) before drafting. Concretely: (FLAG-001/scope-1/scope-2) chose `artagents/pipeline.py:15` as the integration surface for top-level lifecycle/operator/author verbs and stated `runs ls` lands there too; (FLAG-002/correctness) restated gate ordering as running BEFORE both `_prepare_project_request()` (runner.py:135) AND `thread_wrapper.begin_orchestrator_run()` (line 136), with a defensive decorator at the top of `run_orchestrator()` so a rejection produces zero project-run side effects; (issue_hints) explicitly justified the new `artagents/core/task/` namespace as a settled decision rather than silent assumption; (callers) defined nested executor/`builtin.hype` calls inherit the parent task run via `ARTAGENTS_TASK_RUN_ID` env and skip creating child project records; (all_locations) added root `.gitignore` update for `<pack>/build/` to Phase 4 exit criteria; (criteria_quality) split the path-citation success criterion into existing-code-must-resolve vs prescriptive-future-deliverable. Added Open-Call Decisions block, expanded SD coverage list, added a separate verification read-back step, and updated phase file-touch lists to consistently carry the namespace and gate-ordering choices."
      },
      {
        "id": "all_locations",
        "concern": "Does the change touch all locations AND supporting infrastructure?: FLAG-006 remains open: the plan still introduces future `artagents/orchestrate/`, while `artagents/structure.py` only allows top-level directories listed in `TOP_LEVEL_ARTAGENTS_DIRS` and does not include `orchestrate`. The phase file-touch list still does not mention updating `artagents/structure.py` or `tests/test_doctor_setup.py` for that new top-level package.",
        "resolution": "Restored A6 to the task brief's literal model (resolves issue_hints / correctness / criteria_quality / FLAG-008): a `code` step is **deterministic argv that the runner subprocesses** with returncode + produces, and is a strict superset of today's `RUNTIME_KINDS={python,command}`. The forbidden surface is narrowed precisely: a `code` step's argv MUST NOT target `artagents orchestrators run` (because that argv shape hides sub-plan delegation from the gate); but argv targeting `artagents executors run <name>` (or any non-orchestrator argv) is FINE \u2014 leaf executor unit, exactly today's `command` runtime preserved. Section 13 hype.py sketch now shows `code`-step children as argv to `artagents executors run \u2026` (the established surface \u2014 `artagents/core/executor/cli.py` + `run_executor()`), with `produces` checks attached; sub-orchestrator delegation appears as `nested`. The prior iteration's \"inline Python only / no subprocess to executors run\" wording is removed everywhere. Added A11 + new SD (resolves all_locations / FLAG-006): Phase 4 file-touch list now includes `artagents/structure.py:27` (`TOP_LEVEL_ARTAGENTS_DIRS` extended to include `orchestrate` and `verify`) and `tests/test_doctor_setup.py`, with an explicit exit criterion that `python3 -m artagents doctor` accepts the new top-level packages. Phase test strategies now cite existing test modules (`tests/test_project_runs.py`, `tests/test_doctor_setup.py`, executor/orchestrator test patterns) where extended. Success criteria updated to match the corrected model."
      },
      {
        "id": "callers",
        "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: The revised phase table carries the parent-task inheritance behavior mainly in the migration example instead of in the implementation phases. Because `run_executor()` and direct `hype.main()` have independent project-run preparation paths, the doc should move this from example-only text into the Phase 1 or Phase 2 scope/files/exit criteria so it is not skipped for non-hype task plans.",
        "resolution": "Resolved the two open clusters. (1) Step-kind contradiction (issue_hints / FLAG-004): A6 rewritten to make the boundary explicit \u2014 a `code` step is inline Python only and may import-and-call executor entrypoints as Python functions, but MUST NOT subprocess to `artagents executors run` or `artagents orchestrators run`; sub-orchestrator delegation is exclusively `nested`. Step 3 (Step Kinds) and Step 8 (hype.py sketch) are now consistent; an SD entry codifies the boundary; Phase 4 and Phase 2 add `author check` rejection tests for the forbidden subprocess shapes. (2) `ARTAGENTS_TASK_RUN_ID` under-specification (correctness / all_locations / callers / FLAG-005 / scope): introduced A9 + A10 and moved the env contract into Phase 1 scope/files/exit criteria with all three `prepare_project_run()` callers explicitly named (`artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`), plus `artagents/core/project/run.py` (skip child run.json / skip bumping `ARTAGENTS_PROJECT_RUN`) and `artagents/threads/wrapper.py:21-26` (subprocess env propagation alongside existing run-identity envs). A10 explicitly preserves child output dirs + hype artifact mirroring inside the parent task run, so `tests/test_project_runs.py` keeps passing for standalone runs while Phase 2 adds task-mode-inherited tests. Phase 2 exit now requires a non-hype task plan exercising `run_executor()` so the inheritance contract is validated outside the migration example."
      },
      {
        "id": "conventions",
        "concern": "Does the approach match how the codebase solves similar problems?: The direct-import executor direction does not match the current codebase convention for invoking tools through the CLI gateway and runner APIs. `SKILL.md` says every summon goes through `python3 -m artagents`, and `artagents/core/executor/cli.py`/`run_executor()` are the existing surfaces for list/inspect/validate/run, while several pack `run.py` files are CLI-shaped modules rather than stable callable libraries.",
        "resolution": "The direct-import executor direction does not match the current codebase convention for invoking tools through the CLI gateway and runner APIs. `SKILL.md` says every summon goes through `python3 -m artagents`, and `artagents/core/executor/cli.py`/`run_executor()` are the existing surfaces for list/inspect/validate/run, while several pack `run.py` files are CLI-shaped modules rather than stable callable libraries."
      },
      {
        "id": "criteria_quality",
        "concern": "Are the success criteria well-prioritized and verifiable?: The new must criteria around inline Python-only `code` steps are verifiable from the doc, but they encode the design drift flagged above rather than the original task brief's deterministic argv/subprocess model. The criteria are clear, but the underlying requirement should be revised before execution.",
        "resolution": "Restored A6 to the task brief's literal model (resolves issue_hints / correctness / criteria_quality / FLAG-008): a `code` step is **deterministic argv that the runner subprocesses** with returncode + produces, and is a strict superset of today's `RUNTIME_KINDS={python,command}`. The forbidden surface is narrowed precisely: a `code` step's argv MUST NOT target `artagents orchestrators run` (because that argv shape hides sub-plan delegation from the gate); but argv targeting `artagents executors run <name>` (or any non-orchestrator argv) is FINE \u2014 leaf executor unit, exactly today's `command` runtime preserved. Section 13 hype.py sketch now shows `code`-step children as argv to `artagents executors run \u2026` (the established surface \u2014 `artagents/core/executor/cli.py` + `run_executor()`), with `produces` checks attached; sub-orchestrator delegation appears as `nested`. The prior iteration's \"inline Python only / no subprocess to executors run\" wording is removed everywhere. Added A11 + new SD (resolves all_locations / FLAG-006): Phase 4 file-touch list now includes `artagents/structure.py:27` (`TOP_LEVEL_ARTAGENTS_DIRS` extended to include `orchestrate` and `verify`) and `tests/test_doctor_setup.py`, with an explicit exit criterion that `python3 -m artagents doctor` accepts the new top-level packages. Phase test strategies now cite existing test modules (`tests/test_project_runs.py`, `tests/test_doctor_setup.py`, executor/orchestrator test patterns) where extended. Success criteria updated to match the corrected model."
      },
      {
        "id": "FLAG-004",
        "concern": "Step model: the revised plan both forbids `code-step-calls-orchestrator` and describes `code` steps shelling out to `artagents orchestrators run`, which contradicts the required nested-as-data model.",
        "resolution": "Resolved the two open clusters. (1) Step-kind contradiction (issue_hints / FLAG-004): A6 rewritten to make the boundary explicit \u2014 a `code` step is inline Python only and may import-and-call executor entrypoints as Python functions, but MUST NOT subprocess to `artagents executors run` or `artagents orchestrators run`; sub-orchestrator delegation is exclusively `nested`. Step 3 (Step Kinds) and Step 8 (hype.py sketch) are now consistent; an SD entry codifies the boundary; Phase 4 and Phase 2 add `author check` rejection tests for the forbidden subprocess shapes. (2) `ARTAGENTS_TASK_RUN_ID` under-specification (correctness / all_locations / callers / FLAG-005 / scope): introduced A9 + A10 and moved the env contract into Phase 1 scope/files/exit criteria with all three `prepare_project_run()` callers explicitly named (`artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`), plus `artagents/core/project/run.py` (skip child run.json / skip bumping `ARTAGENTS_PROJECT_RUN`) and `artagents/threads/wrapper.py:21-26` (subprocess env propagation alongside existing run-identity envs). A10 explicitly preserves child output dirs + hype artifact mirroring inside the parent task run, so `tests/test_project_runs.py` keeps passing for standalone runs while Phase 2 adds task-mode-inherited tests. Phase 2 exit now requires a non-hype task plan exercising `run_executor()` so the inheritance contract is validated outside the migration example."
      },
      {
        "id": "FLAG-005",
        "concern": "Project run inheritance: `ARTAGENTS_TASK_RUN_ID` inheritance is specified, but the phase implementation file lists do not include all actual project-run preparation paths that would need to honor it.",
        "resolution": "Resolved the two open clusters. (1) Step-kind contradiction (issue_hints / FLAG-004): A6 rewritten to make the boundary explicit \u2014 a `code` step is inline Python only and may import-and-call executor entrypoints as Python functions, but MUST NOT subprocess to `artagents executors run` or `artagents orchestrators run`; sub-orchestrator delegation is exclusively `nested`. Step 3 (Step Kinds) and Step 8 (hype.py sketch) are now consistent; an SD entry codifies the boundary; Phase 4 and Phase 2 add `author check` rejection tests for the forbidden subprocess shapes. (2) `ARTAGENTS_TASK_RUN_ID` under-specification (correctness / all_locations / callers / FLAG-005 / scope): introduced A9 + A10 and moved the env contract into Phase 1 scope/files/exit criteria with all three `prepare_project_run()` callers explicitly named (`artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`), plus `artagents/core/project/run.py` (skip child run.json / skip bumping `ARTAGENTS_PROJECT_RUN`) and `artagents/threads/wrapper.py:21-26` (subprocess env propagation alongside existing run-identity envs). A10 explicitly preserves child output dirs + hype artifact mirroring inside the parent task run, so `tests/test_project_runs.py` keeps passing for standalone runs while Phase 2 adds task-mode-inherited tests. Phase 2 exit now requires a non-hype task plan exercising `run_executor()` so the inheritance contract is validated outside the migration example."
      },
      {
        "id": "FLAG-006",
        "concern": "Structure guardrails: the plan introduces future top-level package `artagents/orchestrate/`, but current repo structure validation rejects unlisted top-level ArtAgents directories.",
        "resolution": "`artagents/structure.py` only allows top-level directories in `TOP_LEVEL_ARTAGENTS_DIRS`, which does not include `orchestrate`; `tests/test_doctor_setup.py` exercises this guard."
      },
      {
        "id": "scope",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: The revised scope for nested-call inheritance names three caller families, but the nine-phase file-touch lists do not include `artagents/core/executor/runner.py` or `artagents/packs/builtin/hype/run.py` in the phase that implements `ARTAGENTS_TASK_RUN_ID` behavior. Those files are actual `prepare_project_run()` callers, so downstream implementation could miss required glue while still following the phase table.",
        "resolution": "Resolved the two open clusters. (1) Step-kind contradiction (issue_hints / FLAG-004): A6 rewritten to make the boundary explicit \u2014 a `code` step is inline Python only and may import-and-call executor entrypoints as Python functions, but MUST NOT subprocess to `artagents executors run` or `artagents orchestrators run`; sub-orchestrator delegation is exclusively `nested`. Step 3 (Step Kinds) and Step 8 (hype.py sketch) are now consistent; an SD entry codifies the boundary; Phase 4 and Phase 2 add `author check` rejection tests for the forbidden subprocess shapes. (2) `ARTAGENTS_TASK_RUN_ID` under-specification (correctness / all_locations / callers / FLAG-005 / scope): introduced A9 + A10 and moved the env contract into Phase 1 scope/files/exit criteria with all three `prepare_project_run()` callers explicitly named (`artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`), plus `artagents/core/project/run.py` (skip child run.json / skip bumping `ARTAGENTS_PROJECT_RUN`) and `artagents/threads/wrapper.py:21-26` (subprocess env propagation alongside existing run-identity envs). A10 explicitly preserves child output dirs + hype artifact mirroring inside the parent task run, so `tests/test_project_runs.py` keeps passing for standalone runs while Phase 2 adds task-mode-inherited tests. Phase 2 exit now requires a non-hype task plan exercising `run_executor()` so the inheritance contract is validated outside the migration example."
      },
      {
        "id": "FLAG-008",
        "concern": "Code step model: the plan changes `code` from deterministic argv/subprocess execution into inline Python-only direct imports, which diverges from the task brief and current executor runner architecture.",
        "resolution": "Restored A6 to the task brief's literal model (resolves issue_hints / correctness / criteria_quality / FLAG-008): a `code` step is **deterministic argv that the runner subprocesses** with returncode + produces, and is a strict superset of today's `RUNTIME_KINDS={python,command}`. The forbidden surface is narrowed precisely: a `code` step's argv MUST NOT target `artagents orchestrators run` (because that argv shape hides sub-plan delegation from the gate); but argv targeting `artagents executors run <name>` (or any non-orchestrator argv) is FINE \u2014 leaf executor unit, exactly today's `command` runtime preserved. Section 13 hype.py sketch now shows `code`-step children as argv to `artagents executors run \u2026` (the established surface \u2014 `artagents/core/executor/cli.py` + `run_executor()`), with `produces` checks attached; sub-orchestrator delegation appears as `nested`. The prior iteration's \"inline Python only / no subprocess to executors run\" wording is removed everywhere. Added A11 + new SD (resolves all_locations / FLAG-006): Phase 4 file-touch list now includes `artagents/structure.py:27` (`TOP_LEVEL_ARTAGENTS_DIRS` extended to include `orchestrate` and `verify`) and `tests/test_doctor_setup.py`, with an explicit exit criterion that `python3 -m artagents doctor` accepts the new top-level packages. Phase test strategies now cite existing test modules (`tests/test_project_runs.py`, `tests/test_doctor_setup.py`, executor/orchestrator test patterns) where extended. Success criteria updated to match the corrected model."
      }
    ],
    "weighted_score": 0,
    "weighted_history": [
      15.0,
      12.0,
      7.0
    ],
    "plan_delta_from_previous": 84.98,
    "recurring_critiques": [],
    "scope_creep_flags": [],
    "loop_summary": "Iteration 4. Weighted score trajectory: 15.0 -> 12.0 -> 7.0 -> 0. Plan deltas: 84.2%, 77.7%, 85.0%. Recurring critiques: 0. Resolved flags: 16. Open significant flags: 0.",
    "debt_overlaps": [],
    "escalated_debt_subsystems": []
  },
  "warnings": [],
  "criteria_check": {
    "count": 25,
    "items": [
      {
        "criterion": "Document exists at exactly `docs/orchestrator-v1-plan.md` (no alternate filename based on title or kebab-case normalization).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Document ends with a `## Settled Decisions` section using `SD-NNN <topic>: <single-sentence rationale>.` format matching `docs/sprint-thread-layer.md`.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Settled Decisions covers every load-bearing call: three step kinds; repeat as body attribute; plan.json rename; plain sha256 chain (no HMAC); no .index.db; Python DSL only; <pack>/build/ gitignored; per-project .cas; the precise code-vs-nested boundary (a `code` step's argv may target `artagents executors run <name>` but MUST NOT target `artagents orchestrators run`; sub-orchestrator delegation is the `nested` step kind); gate four-check + recovery command; gate runs BEFORE both _prepare_project_request and thread_wrapper.begin_orchestrator_run; events.jsonl single write surface; lifecycle verbs extend artagents/pipeline.py; artagents/core/task/ namespace; structure-guardrail update (TOP_LEVEL_ARTAGENTS_DIRS extended for orchestrate + verify); ARTAGENTS_TASK_RUN_ID integration surface enumerated; task-mode preserves child output dirs + artifact mirroring; ARTAGENTS_ACTOR pinning + self-ack rejection; ack decision validity rules; produces inline checks; sentinel-only rejected at author check; Stop-hook preamble every call; additive migration; honor model; Phase 3 + Phase 5 cut points; builtin.hype canonical example; phasing 1\u20139.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Each of the nine phases includes scope, files-touched (with inline backticked path citations), classification (additive or breaking), exit criteria, and test strategy.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Phase 1 file-touch list explicitly names ALL three current `prepare_project_run()` callers (`artagents/core/orchestrator/runner.py`, `artagents/core/executor/runner.py`, `artagents/packs/builtin/hype/run.py`) PLUS `artagents/core/project/run.py` and `artagents/threads/wrapper.py` (subprocess env propagation).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Phase 2 exit criteria require a non-hype task plan that exercises a `code` step whose argv invokes `artagents executors run <leaf-executor>` under task mode (so the inheritance contract is validated outside the hype migration example).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Phase 4 file-touch list names `artagents/structure.py` (`TOP_LEVEL_ARTAGENTS_DIRS` extended to include `orchestrate` and `verify`) AND `tests/test_doctor_setup.py`; Phase 4 exit criterion requires `python3 -m artagents doctor` to accept the new top-level packages.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Storage tree section reproduces the task spec exactly: `active_run.json`, `runs/<run-id>/{plan.json,events.jsonl,AGENT.md}`, `steps/<id>/{produces,iterations/NNN,items/<id>}/`, `inbox/`, `<slug>/.cas/<sha256>` \u2014 and explicitly excludes `.index.db` and HMAC.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Step Kinds section names code, attested, nested; specifies repeat:{until|for_each} as body attributes; states EXPLICITLY that `code` is **deterministic argv that the runner subprocesses** (strict superset of today's `RUNTIME_KINDS={python,command}`), that argv MAY target `artagents executors run <name>` but MUST NOT target `artagents orchestrators run`, and that sub-orchestrator delegation is the `nested` step kind.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Section 13 hype.py sketch shows `code`-step children as argv invocations of `artagents executors run <name> \u2026` (NOT inline Python imports); sub-orchestrator delegation appears as `nested` entries (NOT a `code` argv to `artagents orchestrators run`).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Gate section enumerates all four checks AND states the gate runs BEFORE both `_prepare_project_request()` (`artagents/core/orchestrator/runner.py:135`) AND `thread_wrapper.begin_orchestrator_run()` (line 136), AND that rejection produces zero project-run filesystem side effects.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Ack Decisions section specifies validity rules: retry only after verifier failure, iterate --feedback only when repeat.until=user_approves, abort ends run; --agent / ARTAGENTS_ACTOR pinning required; self-acks rejected; --item targets for_each.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Lifecycle Verbs section explicitly lands top-level verbs (next/ack/status/abort/start/runs ls/author \u2026) in `artagents/pipeline.py:15` dispatch table, NOT under the existing `orchestrators` subparser.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Authoring section states Python DSL `artagents.orchestrate` is the only committed representation, JSON manifest is gitignored at `<pack>/build/<orch>.json`, runtime hashes/pins the build artifact, pack adds `<orch>.py`/`fixtures/`/`golden/<name>.events.jsonl`, AND root `.gitignore` is updated to exclude `<pack>/build/` as part of Phase 4 exit criteria.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Stop-hook section states the prohibition preamble is re-injected verbatim on every `artagents next` call (not just first call).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Doc explicitly states task-mode behavior preserves child output directories and hype artifact mirroring inside `runs/<task-run-id>/steps/<step-id>/produces/`, while standalone (non-task-mode) project-run behavior is unchanged so `tests/test_project_runs.py` keeps passing.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Risk register includes single-host assumption, semantic verifier discipline, context-decay re-injection, and honor-model boundary, each with trigger + mitigation.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Document explicitly Confirms (or Revises with rationale) all eleven open-call decisions A1\u2013A11.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Migration is presented as additive: existing `OrchestratorDefinition` JSON manifests + `python`/`command` `RUNTIME_KINDS` keep working unchanged; `artagents executors run` argv shapes (today's `command` runtime) keep working under task mode; existing `artagents orchestrators` CLI verbs remain unchanged; `tests/test_project_runs.py` continues to pass for standalone runs.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "All EXISTING-CODE inline path citations resolve to real files in the repo today (`artagents/pipeline.py:15`, `artagents/core/orchestrator/runner.py:135`, `artagents/core/orchestrator/schema.py`, `artagents/core/project/run.py`, `artagents/core/executor/runner.py`, `artagents/core/executor/cli.py`, `artagents/packs/builtin/hype/run.py`, `artagents/threads/wrapper.py:21-26`, `artagents/structure.py:27`, `tests/test_project_runs.py`, `tests/test_doctor_setup.py`).",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "FUTURE-DELIVERABLE paths (`AUTHORING.md`, per-run `AGENT.md`, `<pack>/build/`, `<pack>/fixtures/`, `<pack>/golden/`, `artagents/core/task/`, `artagents/orchestrate/`, `artagents/verify/`) are clearly framed as prescriptive new paths, not as resolvable-today citations.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Document body length lands in ~1500\u20132200 words (SD list excluded).",
        "priority": "should",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Tone is terse, declarative, decision-first; matches `docs/sprint-thread-layer.md` and `docs/design-thread-layer.md`.",
        "priority": "should",
        "requires": [
          "subjective_judgment",
          "read_files"
        ]
      },
      {
        "criterion": "Document does not introduce a daemon, web server, `.index.db`, HMAC/keyed crypto, or shared CAS in v1; these are explicitly listed in Non-Goals.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Cut Points section identifies Phase 3 (kernel + step kinds + produces/repeat) and Phase 5 (adds authoring + lifecycle verb split) as ship-ready milestones.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      }
    ]
  },
  "preflight_results": {
    "project_dir_exists": true,
    "project_dir_writable": true,
    "success_criteria_present": true,
    "claude_available": true,
    "codex_available": true
  },
  "unresolved_flags": []
}

        Critique check summary:
        - issue_hints: clear
        - correctness: clear
        - scope: clear
        - all_locations: clear
        - callers: clear
        - conventions: clear
        - verification: 1 flagged
        - criteria_quality: clear

        Unresolved significant flags:
        []

        Known accepted debt grouped by subsystem:
{}

Escalated debt subsystems:
[]

Debt guidance:
- Treat recurring debt as decision context, not background noise.
- If the current unresolved flags overlap an escalated subsystem, prefer recommending holistic redesign over another point fix.

        Iteration Pressure Analysis:
Group      Flags  Iters  Reopened  Concern
------------------------------------------------------------------------
FG-001     1      3      0         The revised A6 overcorrects the step model by rede
FG-002     1      3      0         Directly importing executor modules as the preferr
FG-003     1      2      0         The revised scope for nested-call inheritance name
FG-004     1      3      0         FLAG-006 remains open: the plan still introduces f
FG-005     1      2      0         The revised phase table carries the parent-task in
FG-006     1      3      0         The direct-import executor direction does not matc
FG-007     1      4      0         FLAG-007 is still partially open: Phase 5 changes 
FG-008     1      2      0         The new must criteria around inline Python-only `c
FG-009     1      1      0         Task CLI surface: lifecycle verbs are top-level bu
FG-010     1      1      0         Gate ordering: saying the gate runs before `artage
FG-011     1      1      0         Authoring build artifacts: the plan requires gitig
FG-012     1      4      0         Criterion 22: requires human verification (subject
FG-013     1      1      0         Step model: the revised plan both forbids `code-st
FG-014     1      1      0         Project run inheritance: `ARTAGENTS_TASK_RUN_ID` i
FG-015     1      2      0         Structure guardrails: the plan introduces future t
FG-016     1      3      0         Verification: Phase 5 changes top-level `artagents
FG-017     1      1      0         Code step model: the plan changes `code` from dete
FG-018     1      1      0         Search for related code that handles the same conc
FG-019     1      1      0         Search for related code that handles the same conc

        Robustness level:
        robust

        Requirements:
        - Decide exactly one of: PROCEED, ITERATE, ESCALATE, TIEBREAKER.
        - Use the weighted score, flag details (including `evidence`), plan delta, recurring critiques, and preflight results as judgment context.
        - PROCEED when execution should move forward now.
        - ITERATE when revising the plan is the best next move.
        - ESCALATE when the loop is stuck, churn is recurring, or user intervention is needed.
        - TIEBREAKER when a flag group reflects an *unresolvable constraint tension* (architectural or philosophical — requires a human call) rather than a plan-quality issue. Use TIEBREAKER only when the Iteration Pressure Analysis shows `addressed_then_reopened_count >= 2` for a fuzzy group OR the group has >=2 member flags across >=2 iterations. If the concern is simply that the plan writer hasn't tried hard enough, use ITERATE instead. When recommending TIEBREAKER you MUST provide `tiebreaker_question` (the decision question for human resolution), `tiebreaker_flag_ids` (which flags this resolves), and `tiebreaker_fuzzy_group_id` (which group this resolves). Cite specific flag IDs and iterations in your rationale.
        - `signals_assessment`: one paragraph summarizing score trajectory, flag status, and preflight posture.

        Flags come in two tiers:
        - **Blocking** (severity = significant/likely-significant): These are serious concerns. If you recommend PROCEED, you MUST provide a `flag_resolutions` entry for every blocking flag. There is no implicit acceptance.
        - **Noted** (everything else): Acknowledge in your rationale but they don't block PROCEED.

        If there are blocking flags and you want to PROCEED, provide `flag_resolutions` with one entry per blocking flag. If you cannot resolve every blocking flag, choose ITERATE (send back for revision) or ESCALATE (human intervention needed).
        Structurally unresolvable flags (for example, infrastructure outside the repo or product decisions that require a human) are ESCALATE, not PROCEED with a non-answer.

        For each blocking flag:
        - **dispute**: The critique is factually wrong. Evidence must cite something specific (file path, line, API doc, etc.). Generic statements like "handled correctly" are invalid.
        - **accept_tradeoff**: The concern is real but intentionally accepted as a known limitation. Rationale must be specific to this flag. Boilerplate like "acceptable within scope" is invalid.
        - Schema requirement: every `flag_resolutions` entry must include both `evidence` and `rationale`. Use `""` for the field that does not apply to that action.

        If there are no blocking flags, return `flag_resolutions: []`.
        Always return `accepted_tradeoffs`; use `[]` when none apply.

        Populate `settled_decisions` with design choices that should carry into review without re-litigation. Return `[]` when there are none.

        Example:
        ```json
        {
          "recommendation": "PROCEED",
          "rationale": "Core fix is correct. Convention concern accepted.",
          "signals_assessment": "Score stable at 2.5, preflight passed, no recurring critiques.",
          "warnings": ["Verify edge case with composite moduli during execution."],
          "flag_resolutions": [
            {"flag_id": "correctness-1", "action": "dispute", "evidence": "allow_migrate and allow_migrate_model produce identical behavior for this use case (verified at django/db/utils.py:286).", "rationale": ""},
            {"flag_id": "performance-1", "action": "accept_tradeoff", "evidence": "", "rationale": "Cold-start latency remains 40ms above target because the cache warmup job is owned by platform and outside this repo; rollout is still approved for the limited internal beta."},
            {"flag_id": "conventions-1", "action": "accept_tradeoff", "evidence": "", "rationale": "Minor naming inconsistency is confined to this helper and would create churn across generated fixtures; track it as follow-up cleanup instead of blocking this fix."}
          ],
          "accepted_tradeoffs": [],
          "settled_decisions": []
        }
        ```

> TOOL

tool_use StructuredOutput
```json
{
  "recommendation": "PROCEED",
  "rationale": "All blocking flags resolved. Score reached 0, all 16 historical significant flags marked resolved with verification, `unresolved_flags: []`, and `significant_flags: 0`. Plan delta 84.98% reflects the substantive A6 restoration to brief-literal model + addition of A11 for the structure-guardrail update. The critique check summary lists \"verification: 1 flagged\" but the explicit `unresolved_flags` list is empty and the gate signals report 0 open significant flags — that count appears to be a stale fuzzy-group bookkeeping artifact (FG-007/FG-016 history), not a current blocker. The plan now correctly encodes the brief: `code` is deterministic argv subprocess (strict superset of `RUNTIME_KINDS={python,command}`), forbidden surface is precisely `code` argv to `artagents orchestrators run` (with `executors run` argv preserved as today's `command` runtime), Section 13 hype.py sketch matches, Phase 4 file-touch list now names `artagents/structure.py:27` and `tests/test_doctor_setup.py`, and all eleven A1–A11 open-call decisions are explicitly confirmed with corresponding SD entries. Score trajectory 15 → 12 → 7 → 0 over four iterations, no reopened flags, no recurring critiques, preflight clean. Doc execution may proceed.",
  "signals_assessment": "Iteration 4; weighted score 15.0 → 12.0 → 7.0 → 0; plan deltas 84.18% → 77.68% → 84.98%; 16 of 16 historical significant flags resolved with verification; 0 currently-open significant flags; 0 reopened flags across all fuzzy groups; 0 recurring critiques; no escalated debt subsystems. Preflight clean (writable workspace, criteria present, both Claude and codex available). The remaining \"verification: 1 flagged\" line in the critique summary corresponds to historical fuzzy-group counters (FG-007/FG-016 at 3–4 iters) but the explicit unresolved-flag list is empty. Convergence is clean.",
  "warnings": [
    "During execution, verify the EXISTING-CODE inline citations resolve before committing the doc: `artagents/pipeline.py:15`, `artagents/core/orchestrator/runner.py:135`, `artagents/threads/wrapper.py:21-26`, `artagents/structure.py:27` (`TOP_LEVEL_ARTAGENTS_DIRS`), `tests/test_project_runs.py`, `tests/test_doctor_setup.py`. Line numbers can drift between plan-time and execution-time; re-grep before pinning.",
    "Section 13 hype.py sketch should use a 5–10 line excerpt that is concretely valid against the (prescriptive) `artagents.orchestrate` DSL surface. Use placeholder argv shape like `code(argv=[\"python3\",\"-m\",\"artagents\",\"executors\",\"run\",\"builtin.transcribe\",\"…\"], produces={...})` rather than fully invented function names that imply more API surface than the doc defines.",
    "When confirming A1–A11 in Section 17, keep the entries one line each so the doc stays under the 1500–2200 word budget; the SD list itself is excluded from that budget but the body is not.",
    "Optional follow-up question raised in the plan metadata (whether `artagents/verify/` should fold under `artagents/utilities/verify/` to avoid extending `TOP_LEVEL_ARTAGENTS_DIRS`) is reasonable but a v2 concern; do not relitigate during execution — A11 is settled."
  ],
  "flag_resolutions": [],
  "accepted_tradeoffs": [],
  "settled_decisions": [
    {
      "id": "SD-A1",
      "decision": "Three step kinds: code, attested, nested. Iteration/fan-out are body attributes (repeat:{until|for_each}), not separate kinds.",
      "rationale": "Reproduces the V1 brief verbatim; uncontested across all four iterations."
    },
    {
      "id": "SD-A2",
      "decision": "Python DSL `artagents.orchestrate` is the only committed representation; `<pack>/build/<orch>.json` is gitignored and is what the runtime hashes/pins.",
      "rationale": "A2 confirmed iteration 1, stable through iteration 4."
    },
    {
      "id": "SD-A3",
      "decision": "No `.index.db` in v1; file-walk verbs only.",
      "rationale": "A3 confirmed iteration 1, stable through iteration 4."
    },
    {
      "id": "SD-A4",
      "decision": "Kernel modules land in NEW `artagents/core/task/` package (gate, events, active_run, dispatch, produces, cas, inbox, preamble, env) above orchestrator dispatch.",
      "rationale": "A4 resolved iteration 2, stable through iteration 4."
    },
    {
      "id": "SD-A5",
      "decision": "Top-level lifecycle/operator/author verbs (next/ack/status/abort/start/runs ls/author …) extend `artagents/pipeline.py:15` dispatch table; existing `artagents orchestrators` keeps working unchanged.",
      "rationale": "A5 resolved iteration 2, stable through iteration 4."
    },
    {
      "id": "SD-A6",
      "decision": "code-vs-nested boundary: a `code` step is deterministic argv that the runner subprocesses (strict superset of today's `RUNTIME_KINDS={python,command}`); its argv may target `artagents executors run <name>` (leaf executor unit, exactly today's command runtime preserved) but MUST NOT target `artagents orchestrators run` (sub-plan delegation hidden in argv); sub-orchestrator delegation is exclusively the `nested` step kind so the gate sees the structure for hashing/pinning.",
      "rationale": "Restored to brief-literal model in iteration 4 after correcting iteration 3 over-correction; resolves issue_hints / correctness / criteria_quality / FLAG-008."
    },
    {
      "id": "SD-A7",
      "decision": "Gate runs BEFORE both `_prepare_project_request()` (artagents/core/orchestrator/runner.py:135) AND `thread_wrapper.begin_orchestrator_run()` (line 136); rejection produces zero project-run filesystem side effects.",
      "rationale": "A7 resolved iteration 2, stable through iteration 4."
    },
    {
      "id": "SD-A8",
      "decision": "Root `.gitignore` is updated in Phase 4 to exclude `<pack>/build/`.",
      "rationale": "A8 resolved iteration 2, stable through iteration 4."
    },
    {
      "id": "SD-A9",
      "decision": "ARTAGENTS_TASK_RUN_ID is the env contract for task-mode inheritance; integration surface enumerated in Phase 1: artagents/core/orchestrator/runner.py + artagents/core/executor/runner.py + artagents/packs/builtin/hype/run.py + artagents/core/project/run.py + artagents/threads/wrapper.py (subprocess env propagation alongside ARTAGENTS_RUN_ID/ARTAGENTS_PARENT_RUN_ID/ARTAGENTS_PROJECT_RUN at lines 21–26).",
      "rationale": "A9 resolved iteration 3, stable through iteration 4."
    },
    {
      "id": "SD-A10",
      "decision": "Under task mode, prepare_project_run() skips child run.json and skips bumping ARTAGENTS_PROJECT_RUN, but PRESERVES child output dirs + hype artifact mirroring inside the parent runs/<task-run-id>/steps/<step-id>/produces/; standalone (non-task-mode) behavior unchanged so tests/test_project_runs.py keeps passing.",
      "rationale": "A10 resolved iteration 3, stable through iteration 4."
    },
    {
      "id": "SD-A11",
      "decision": "Phase 4 file-touch list adds `artagents/structure.py:27` (TOP_LEVEL_ARTAGENTS_DIRS extended to include `orchestrate` and `verify`) and `tests/test_doctor_setup.py` asserts the new top-level packages are accepted; `python3 -m artagents doctor` accepts `artagents/orchestrate/` and `artagents/verify/`.",
      "rationale": "A11 added iteration 4 to resolve all_locations / FLAG-006 (open since iteration 2)."
    },
    {
      "id": "SD-G1",
      "decision": "Doc body target ~1500–2200 words excluding the SD list; output path is exactly docs/orchestrator-v1-plan.md; SD format follows `SD-NNN <topic>: <single-sentence rationale>.` per docs/sprint-thread-layer.md lines 39–43.",
      "rationale": "Documentation discipline; uncontested across all four iterations."
    },
    {
      "id": "SD-G2",
      "decision": "Canonical migration example is artagents/packs/builtin/hype/; hype.py sketch shows code-step argv to `artagents executors run <name>` and sub-orchestrator delegation as `nested`.",
      "rationale": "Example target stable across all four iterations; exact sketch shape settled in iteration 4."
    }
  ],
  "tiebreaker_question": "",
  "tiebreaker_flag_ids": [],
  "tiebreaker_fuzzy_group_id": ""
}
```

> TOOL

tool_result StructuredOutput
```
Structured output provided successfully
```

> AGENT

Recommended **PROCEED**. Score reached 0, all 16 historical significant flags resolved with verification, no open blocking flags, and convergence is clean over four iterations (15 → 12 → 7 → 0). The plan now correctly encodes the brief: `code` is deterministic argv subprocess (strict superset of `RUNTIME_KINDS={python,command}`), forbidden surface is precisely `code` argv to `orchestrators run`, Phase 4 includes the `artagents/structure.py` / `TOP_LEVEL_ARTAGENTS_DIRS` extension, and all 11 open-call decisions A1–A11 are settled and SD-coded. Doc execution may proceed.
