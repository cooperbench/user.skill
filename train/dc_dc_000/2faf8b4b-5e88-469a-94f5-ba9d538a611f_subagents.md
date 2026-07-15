> DEVELOPER

I need to understand the current state of these files for writing tests: 1. Read tests/test_schemas.py - understand existing schema tests 2. Read tests/test_megaplan.py - understand existing integration tests 3. Read megaplan/capabilities.py - the capability registry 4. Read megaplan/verifiability.py - the verifiability module 5. Read megaplan/types.py - for STATE_AWAITING_HUMAN and related 6. Read megaplan/handlers.py lines around handle_verify_human (around line 2128-2232) and _resolve_review_outcome 7. Read megaplan/auto.py - for the drive() function and AUTOMATION_TERMINAL_STATES usage 8. Check if tests/test_verifiability.py already exists Report the full contents of capabilities.py, verifiability.py, and types.py. For the other files, report key structures, test patterns, imports, and relevant function signatures. Be thorough - I need enough detail to write tests.

> AGENT

I'll read all these files for you to understand the current state. Let me start by gathering this information.

> AGENT

Now let me read the handlers.py section around the verify_human handlers:

> AGENT

Now let me read the _resolve_review_outcome function:

> AGENT

Now let me search for the test_megaplan.py to understand testing patterns better:

> AGENT

Let me get key sections from test_megaplan.py to understand the test patterns:

> AGENT

Perfect. Now let me check if test_verifiability.py exists and look at a few complete test examples:

> AGENT

Perfect. Now let me get more context on the auto.py drive() function and the full integration test pattern:

> AGENT

Excellent! Now I have all the information needed. Let me compile a comprehensive report: ## Comprehensive Codebase Analysis for Testing ### **Full Contents: capabilities.py** ```python """Closed capability registry and worker discovery for verifiability contracts.""" from __future__ import annotations from typing import Any from megaplan.types import DEFAULT_AGENT_ROUTING CONTAINER_CAPABILITIES: frozenset[str] = frozenset({ "run_shell", "read_files", "run_tests", "parse_diff", "read_build_output", "run_linter", }) HUMAN_CAPABILITIES: frozenset[str] = frozenset({ "drive_browser", "inspect_runtime_ui", "observe_runtime_logs", "subjective_judgment", "verify_physical_device", }) ALL_CAPABILITIES: frozenset[str] = CONTAINER_CAPABILITIES | HUMAN_CAPABILITIES DEFAULT_CONTAINER_CAPABILITIES: frozenset[str] = CONTAINER_CAPABILITIES DEFAULT_HUMAN_CAPABILITIES: frozenset[str] = HUMAN_CAPABILITIES def validate_capabilities(caps: list[str] | set[str]) -> list[str]: """Return unknown capability strings not in the closed registry.""" return [c for c in caps if c not in ALL_CAPABILITIES] def get_worker_capabilities(state: dict[str, Any]) -> dict[str, set[str]]: """Build worker-name → capabilities mapping from state config. Falls back to DEFAULT_CONTAINER_CAPABILITIES for agents listed in DEFAULT_AGENT_ROUTING that have no explicit config. """ config = state.get("config", {}) workers_cfg: dict[str, Any] = config.get("workers", {}) result: dict[str, set[str]] = {} if workers_cfg: for name, wcfg in workers_cfg.items(): verifies = wcfg.get("verifies", []) result[name] = set(verifies) else: seen_agents = set(DEFAULT_AGENT_ROUTING.values()) for agent in seen_agents: result[agent] = set(DEFAULT_CONTAINER_CAPABILITIES) return result def union_verifies(state: dict[str, Any]) -> set[str]: """Return the union of all workers' verifies sets.""" caps = get_worker_capabilities(state) result: set[str] = set() for v in caps.values(): result |= v return result ``` ### **Full Contents: verifiability.py** ```python """Verifiability audit — pure-Python capability matching for success criteria.""" from __future__ import annotations import warnings from dataclasses import dataclass, field from typing import Any from megaplan.capabilities import ALL_CAPABILITIES, HUMAN_CAPABILITIES @dataclass class CriterionAudit: criterion_idx: int verdict: str # "machine_verifiable" | "human_only" | "unverifiable_no_worker" rationale: str missing_caps: list[str] = field(default_factory=list) def audit_criteria( criteria: list[dict[str, Any]], worker_caps: dict[str, set[str]], ) -> list[CriterionAudit]: """For each criterion, check requires ⊆ union of all worker verifies sets. Returns a CriterionAudit per criterion with verdict: - machine_verifiable: all required caps covered by at least one worker - human_only: all required caps exist in registry but some need human workers - unverifiable_no_worker: some required caps not satisfiable by any known worker """ all_worker_caps = set() for caps in worker_caps.values(): all_worker_caps |= caps results: list[CriterionAudit] = [] for idx, criterion in enumerate(criteria): requires = set(criterion.get("requires", [])) if not requires: results.append(CriterionAudit( criterion_idx=idx, verdict="machine_verifiable", rationale="No capabilities required (empty requires).", )) continue missing_from_workers = requires - all_worker_caps if not missing_from_workers: results.append(CriterionAudit( criterion_idx=idx, verdict="machine_verifiable", rationale="All required capabilities covered by configured workers.", )) elif missing_from_workers <= HUMAN_CAPABILITIES: results.append(CriterionAudit( criterion_idx=idx, verdict="human_only", rationale="Some required capabilities need human verification.", missing_caps=sorted(missing_from_workers), )) […]
