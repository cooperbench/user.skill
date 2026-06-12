# Projects: tslateman

## tslateman/reck ★ dominant (63.4% of sessions)

**What it is:** An autonomous manufacturing intelligence system. Detects anomalies in
industrial sensor signals, proposes corrective actions, validates them through a safety
pipeline, executes, monitors, and learns from outcomes.

**Stack:** Python 3.12+, uv, asyncio, MQTT (EMQX broker), protobuf (reck.proto), SQLite,
pytest, ruff. Rust gRPC stub (`watch/rust/`) as the future hot-path target. `justfile` for
task running.

**Architecture:**
- `sim/` — virtual plant (temperature, pressure, flow) publishing SignalEvents
- `watch/` — AnomalyDetector with rolling window (deque) per signal source
- `triage/` — Prioritizer (HIGH/MEDIUM/LOW by sigma distance)
- `rules/` — RuleEngine (YAML-based), RuleConfidence (Beta distribution, SQLite)
- `guard/` — ConstraintChecker (YAML-based bounds and rate-of-change limits)
- `gate/` — GateKeeper (GO/NO_GO/ESCALATE decision with confidence threshold)
- `act/` — ActionExecutor (setpoint commands via MQTT, rollback)
- `monitor/` — ActionMonitor (polls post-action, returns MonitorResult with KPIs)
- `breaker/` — CircuitBreaker (trips on 3 consecutive failures)
- `escalate/` — EscalationHandler (writes JSONL, emits to Praxis CLI)
- `ledger/` — DecisionArchive (JSONL log, Lore integration)
- `memory/` — BaselineStore (Welford online mean/stddev in SQLite)
- `proto/` — reck.proto (source of truth for event schema)

**Recurring themes:**
- Plan-first discipline: plans 001-004 reviewed for consistency before any implementation.
- "Skeleton discipline": module docstrings start with "Stub:" until fully implemented.
- Safety pipeline is non-negotiable: guard → gate → act → monitor → breaker → escalate.
- Multi-agent build pattern: "team-lead" assigns tasks to named subagent panes via tmux.
- Captures architectural decisions to Lore after each major phase.

**Key decisions tslateman made:**
- `just` over `make`; `justfile` not `Makefile`
- Protobuf over JSON for event schemas
- Python-first; Rust only for hot-path after algorithms stabilize
- gRPC for the Python↔Rust boundary
- `pytest.mark.integration` for integration tests, skipped by default
- Beta distribution (Bayesian) for rule confidence tracking

## tslateman/duet (36.6% of sessions)

**What it is:** A Claude Code plugin providing skills, commands, and agent definitions for
reflection, code quality, writing, and design work.

**Structure:**
- `skills/` — methodology skills (naming, review, debugging, prose, design, ia, adr, vibe-check…)
- `commands/` — explicit workflows (vamp, retro, sweep, debrief, probe, lint…)
- `agents/` — subagent definitions (code-simplifier)
- `notes/` — philosophy.md, riffs.md (stable at 3 files)
- `scripts/` — generate-readme.sh, prettier pre-commit hook
- `evals/` — skill evaluation scenarios (vibe-check, review)

**Recurring themes:**
- Jazz vocabulary: vamp (survey between tasks), duet (human-AI collaboration), probe, riffs.
- Precision in naming: renames things when the name is semantically wrong.
  (whats-next → vamp, question → probe, diagnose → debugging, oracle → telos)
- Skills have named frameworks behind them (Strunk, Agans, Bacchelli & Bird, etc.).
- FRAMEWORKS.md as discovery catalog indexed by problem type.
- DX polish: README truncation, hardcoded paths, markdown lint errors, URL formatting.
- Eval framework: format assertions + content assertions, discrimination between skill/no-skill.
- Philosophy: human-AI as a musical duet — productive surprise, not control.
