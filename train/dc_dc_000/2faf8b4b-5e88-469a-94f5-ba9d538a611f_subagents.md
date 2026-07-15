> DEVELOPER

I need to understand the current state of these files for writing tests:

1. Read tests/test_schemas.py - understand existing schema tests
2. Read tests/test_megaplan.py - understand existing integration tests  
3. Read megaplan/capabilities.py - the capability registry
4. Read megaplan/verifiability.py - the verifiability module
5. Read megaplan/types.py - for STATE_AWAITING_HUMAN and related
6. Read megaplan/handlers.py lines around handle_verify_human (around line 2128-2232) and _resolve_review_outcome
7. Read megaplan/auto.py - for the drive() function and AUTOMATION_TERMINAL_STATES usage
8. Check if tests/test_verifiability.py already exists

Report the full contents of capabilities.py, verifiability.py, and types.py. For the other files, report key structures, test patterns, imports, and relevant function signatures. Be thorough - I need enough detail to write tests.

> AGENT

I'll read all these files for you to understand the current state. Let me start by gathering this information.

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/capabilities.py"
}
```

> TOOL

tool_result Read
```
1	"""Closed capability registry and worker discovery for verifiability contracts."""
2	
3	from __future__ import annotations
4	
5	from typing import Any
6	
7	from megaplan.types import DEFAULT_AGENT_ROUTING
8	
9	CONTAINER_CAPABILITIES: frozenset[str] = frozenset({
10	    "run_shell",
11	    "read_files",
12	    "run_tests",
13	    "parse_diff",
14	    "read_build_output",
15	    "run_linter",
16	})
17	
18	HUMAN_CAPABILITIES: frozenset[str] = frozenset({
19	    "drive_browser",
20	    "inspect_runtime_ui",
21	    "observe_runtime_logs",
22	    "subjective_judgment",
23	    "verify_physical_device",
24	})
25	
26	ALL_CAPABILITIES: frozenset[str] = CONTAINER_CAPABILITIES | HUMAN_CAPABILITIES
27	
28	DEFAULT_CONTAINER_CAPABILITIES: frozenset[str] = CONTAINER_CAPABILITIES
29	DEFAULT_HUMAN_CAPABILITIES: frozenset[str] = HUMAN_CAPABILITIES
30	
31	
32	def validate_capabilities(caps: list[str] | set[str]) -> list[str]:
33	    """Return unknown capability strings not in the closed registry."""
34	    return [c for c in caps if c not in ALL_CAPABILITIES]
35	
36	
37	def get_worker_capabilities(state: dict[str, Any]) -> dict[str, set[str]]:
38	    """Build worker-name → capabilities mapping from state config.
39	
40	    Falls back to DEFAULT_CONTAINER_CAPABILITIES for agents listed in
41	    DEFAULT_AGENT_ROUTING that have no explicit config.
42	    """
43	    config = state.get("config", {})
44	    workers_cfg: dict[str, Any] = config.get("workers", {})
45	
46	    result: dict[str, set[str]] = {}
47	
48	    if workers_cfg:
49	        for name, wcfg in workers_cfg.items():
50	            verifies = wcfg.get("verifies", [])
51	            result[name] = set(verifies)
52	    else:
53	        seen_agents = set(DEFAULT_AGENT_ROUTING.values())
54	        for agent in seen_agents:
55	            result[agent] = set(DEFAULT_CONTAINER_CAPABILITIES)
56	
57	    return result
58	
59	
60	def union_verifies(state: dict[str, Any]) -> set[str]:
61	    """Return the union of all workers' verifies sets."""
62	    caps = get_worker_capabilities(state)
63	    result: set[str] = set()
64	    for v in caps.values():
65	        result |= v
66	    return result
67
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/verifiability.py"
}
```

> TOOL

tool_result Read
```
1	"""Verifiability audit — pure-Python capability matching for success criteria."""
2	
3	from __future__ import annotations
4	
5	import warnings
6	from dataclasses import dataclass, field
7	from typing import Any
8	
9	from megaplan.capabilities import ALL_CAPABILITIES, HUMAN_CAPABILITIES
10	
11	
12	@dataclass
13	class CriterionAudit:
14	    criterion_idx: int
15	    verdict: str  # "machine_verifiable" | "human_only" | "unverifiable_no_worker"
16	    rationale: str
17	    missing_caps: list[str] = field(default_factory=list)
18	
19	
20	def audit_criteria(
21	    criteria: list[dict[str, Any]],
22	    worker_caps: dict[str, set[str]],
23	) -> list[CriterionAudit]:
24	    """For each criterion, check requires ⊆ union of all worker verifies sets.
25	
26	    Returns a CriterionAudit per criterion with verdict:
27	      - machine_verifiable: all required caps covered by at least one worker
28	      - human_only: all required caps exist in registry but some need human workers
29	      - unverifiable_no_worker: some required caps not satisfiable by any known worker
30	    """
31	    all_worker_caps = set()
32	    for caps in worker_caps.values():
33	        all_worker_caps |= caps
34	
35	    results: list[CriterionAudit] = []
36	    for idx, criterion in enumerate(criteria):
37	        requires = set(criterion.get("requires", []))
38	        if not requires:
39	            results.append(CriterionAudit(
40	                criterion_idx=idx,
41	                verdict="machine_verifiable",
42	                rationale="No capabilities required (empty requires).",
43	            ))
44	            continue
45	
46	        missing_from_workers = requires - all_worker_caps
47	        if not missing_from_workers:
48	            results.append(CriterionAudit(
49	                criterion_idx=idx,
50	                verdict="machine_verifiable",
51	                rationale="All required capabilities covered by configured workers.",
52	            ))
53	        elif missing_from_workers <= HUMAN_CAPABILITIES:
54	            results.append(CriterionAudit(
55	                criterion_idx=idx,
56	                verdict="human_only",
57	                rationale="Some required capabilities need human verification.",
58	                missing_caps=sorted(missing_from_workers),
59	            ))
60	        else:
61	            truly_unknown = missing_from_workers - HUMAN_CAPABILITIES
62	            results.append(CriterionAudit(
63	                criterion_idx=idx,
64	                verdict="unverifiable_no_worker",
65	                rationale="Required capabilities not satisfiable by any known worker.",
66	                missing_caps=sorted(missing_from_workers),
67	            ))
68	
69	    return results
70	
71	
72	def classify_criteria(
73	    criteria: list[dict[str, Any]],
74	    worker_caps: dict[str, set[str]],
75	) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
76	    """Split criteria into (machine_verifiable, human_deferred).
77	
78	    machine_verifiable includes criteria with verdict machine_verifiable.
79	    human_deferred includes human_only and unverifiable_no_worker.
80	    """
81	    audits = audit_criteria(criteria, worker_caps)
82	    machine: list[dict[str, Any]] = []
83	    human: list[dict[str, Any]] = []
84	    for audit, criterion in zip(audits, criteria):
85	        if audit.verdict == "machine_verifiable":
86	            machine.append(criterion)
87	        else:
88	            human.append(criterion)
89	    return machine, human
90	
91	
92	def validate_requires(
93	    criteria: list[dict[str, Any]],
94	    registry: set[str] | frozenset[str] | None = None,
95	) -> list[str]:
96	    """Check all requires entries are known capability strings.
97	
98	    Returns list of issue strings. Flags must criteria with empty requires
99	    as deprecation warnings.
100	    """
101	    if registry is None:
102	        registry = ALL_CAPABILITIES
103	
104	    issues: list[str] = []
105	    for idx, criterion in enumerate(criteria):
106	        requires = criterion.get("requires", [])
107	        priority = criterion.get("priority", "")
108	
109	        if priority == "must" and not requires:
110	            msg = (
111	                f"Criterion {idx} ({criterion.get('criterion', '?')}): "
112	                f"must-priority criterion has empty requires — "
113	                f"add requires to enable automated verification."
114	            )
115	            issues.append(msg)
116	            warnings.warn(msg, DeprecationWarning, stacklevel=2)
117	
118	        for cap in requires:
119	            if cap not in registry:
120	                issues.append(
121	                    f"Criterion {idx} ({criterion.get('criterion', '?')}): "
122	                    f"unknown capability '{cap}' in requires."
123	                )
124	
125	    return issues
126
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/types.py"
}
```

> TOOL

tool_result Read
```
1	"""Type definitions, constants, and exceptions for megaplan."""
2	
3	from __future__ import annotations
4	
5	from typing import Any, NotRequired, TypedDict
6	
7	
8	# ---------------------------------------------------------------------------
9	# States
10	# ---------------------------------------------------------------------------
11	
12	STATE_INITIALIZED = "initialized"
13	STATE_PREPPED = "prepped"
14	STATE_PLANNED = "planned"
15	STATE_CRITIQUED = "critiqued"
16	STATE_GATED = "gated"
17	STATE_FINALIZED = "finalized"
18	STATE_EXECUTED = "executed"
19	STATE_DONE = "done"
20	STATE_ABORTED = "aborted"
21	STATE_AWAITING_HUMAN = "awaiting_human_verify"
22	TERMINAL_STATES = {STATE_DONE, STATE_ABORTED}
23	AUTOMATION_TERMINAL_STATES = TERMINAL_STATES | {STATE_AWAITING_HUMAN}
24	
25	
26	# ---------------------------------------------------------------------------
27	# TypedDicts
28	# ---------------------------------------------------------------------------
29	
30	class PlanConfig(TypedDict, total=False):
31	    project_dir: str
32	    auto_approve: bool
33	    robustness: str
34	    agents: dict[str, str]
35	    workers: NotRequired[dict[str, Any]]
36	
37	
38	class PlanMeta(TypedDict, total=False):
39	    significant_counts: list[int]
40	    weighted_scores: list[float]
41	    plan_deltas: list[float | None]
42	    recurring_critiques: list[str]
43	    total_cost_usd: float
44	    overrides: list[dict[str, Any]]
45	    notes: list[dict[str, Any]]
46	    user_approved_gate: bool
47	
48	
49	class SessionInfo(TypedDict, total=False):
50	    id: str
51	    mode: str
52	    created_at: str
53	    last_used_at: str
54	    refreshed: bool
55	
56	
57	class ActiveStep(TypedDict, total=False):
58	    step: str
59	    agent: str
60	    mode: str
61	    model: str
62	    run_id: str
63	    session_id: str
64	    started_at: str
65	
66	
67	class PlanVersionRecord(TypedDict, total=False):
68	    version: int
69	    file: str
70	    hash: str
71	    timestamp: str
72	
73	
74	class HistoryEntry(TypedDict, total=False):
75	    step: str
76	    timestamp: str
77	    duration_ms: int
78	    cost_usd: float
79	    result: str
80	    session_mode: str
81	    session_id: str
82	    agent: str
83	    output_file: str
84	    artifact_hash: str
85	    finalize_hash: str
86	    raw_output_file: str
87	    message: str
88	    flags_count: int
89	    flags_addressed: list[str]
90	    recommendation: str
91	    approval_mode: str
92	    environment: dict[str, bool]
93	
94	
95	class ClarificationRecord(TypedDict, total=False):
96	    refined_idea: str
97	    intent_summary: str
98	    questions: list[str]
99	
100	
101	class LastGateRecord(TypedDict, total=False):
102	    recommendation: str
103	    rationale: str
104	    signals_assessment: str
105	    warnings: list[str]
106	    settled_decisions: list["SettledDecision"]
107	    passed: bool
108	    preflight_results: dict[str, bool]
109	    orchestrator_guidance: str
110	
111	
112	class PlanState(TypedDict):
113	    name: str
114	    idea: str
115	    current_state: str
116	    iteration: int
117	    created_at: str
118	    config: PlanConfig
119	    sessions: dict[str, SessionInfo]
120	    plan_versions: list[PlanVersionRecord]
121	    history: list[HistoryEntry]
122	    meta: PlanMeta
123	    last_gate: LastGateRecord
124	    active_step: NotRequired[ActiveStep]
125	    clarification: NotRequired[ClarificationRecord]
126	
127	
128	class _FlagRecordRequired(TypedDict):
129	    id: str
130	    concern: str
131	    category: str
132	    status: str
133	
134	
135	class FlagRecord(_FlagRecordRequired, total=False):
136	    severity_hint: str
137	    evidence: str
138	    raised_in: str
139	    severity: str
140	    verified: bool
141	    verified_in: str
142	    addressed_in: str
143	
144	
145	class FlagRegistry(TypedDict):
146	    flags: list[FlagRecord]
147	
148	
149	class GateCheckResult(TypedDict):
150	    passed: bool
151	    criteria_check: dict[str, Any]
152	    preflight_results: dict[str, bool]
153	    unresolved_flags: list[FlagRecord]
154	
155	
156	class SettledDecision(TypedDict, total=False):
157	    id: str
158	    decision: str
159	    rationale: str
160	
161	
162	class GatePayload(TypedDict):
163	    recommendation: str
164	    rationale: str
165	    signals_assessment: str
166	    warnings: list[str]
167	    settled_decisions: list[SettledDecision]
168	
169	
170	class GateArtifact(TypedDict, total=False):
171	    passed: bool
172	    criteria_check: dict[str, Any]
173	    preflight_results: dict[str, bool]
174	    unresolved_flags: list[FlagRecord]
175	    recommendation: str
176	    rationale: str
177	    signals_assessment: str
178	    warnings: list[str]
179	    settled_decisions: list[SettledDecision]
180	    override_forced: bool
181	    orchestrator_guidance: str
182	    robustness: str
183	    signals: dict[str, Any]
184	
185	
186	class GateSignals(TypedDict, total=False):
187	    robustness: str
188	    signals: dict[str, Any]
189	    warnings: list[str]
190	
191	
192	class StepResponse(TypedDict, total=False):
193	    success: bool
194	    step: str
195	    summary: str
196	    artifacts: list[str]
197	    next_step: str | None
198	    state: str
199	    auto_approve: bool
200	    robustness: str
201	    iteration: int
202	    plan: str
203	    plan_dir: str
204	    questions: list[str]
205	    verified_flags: list[str]
206	    open_flags: list[str]
207	    scope_creep_flags: list[str]
208	    warnings: list[str]
209	    files_changed: list[str]
210	    deviations: list[str]
211	    user_approved_gate: bool
212	    issues: list[str]
213	    valid_next: list[str]
214	    mode: str
215	    installed: list[dict[str, Any]]
216	    config_path: str
217	    routing: dict[str, str]
218	    raw_config: dict[str, Any]
219	    action: str
220	    key: str
221	    value: str
222	    skipped: bool
223	    file: str
224	    plans: list[dict[str, Any]]
225	    recommendation: str
226	    signals: dict[str, Any]
227	    rationale: str
228	    signals_assessment: str
229	    orchestrator_guidance: str
230	    passed: bool
231	    criteria_check: dict[str, Any]
232	    preflight_results: dict[str, bool]
233	    unresolved_flags: list[Any]
234	    error: str
235	    message: str
236	    details: dict[str, Any]
237	    agent_fallback: dict[str, str]
238	
239	
240	class DebtEntry(TypedDict):
241	    id: str
242	    subsystem: str
243	    concern: str
244	    flag_ids: list[str]
245	    plan_ids: list[str]
246	    occurrence_count: int
247	    created_at: str
248	    updated_at: str
249	    resolved: bool
250	    resolved_by: str | None
251	    resolved_at: str | None
252	
253	
254	class DebtRegistry(TypedDict):
255	    entries: list[DebtEntry]
256	
257	
258	# ---------------------------------------------------------------------------
259	# Constants
260	# ---------------------------------------------------------------------------
261	
262	FLAG_BLOCKING_STATUSES = {"open", "disputed", "addressed"}
263	FLAG_VALID_STATUSES = {
264	    "open", "addressed", "disputed", "verified",
265	    "accepted_tradeoff", "gate_disputed",
266	}
267	DEBT_ESCALATION_THRESHOLD = 3
268	MOCK_ENV_VAR = "MEGAPLAN_MOCK_WORKERS"
269	
270	DEFAULT_AGENT_ROUTING: dict[str, str] = {
271	    "plan": "claude",
272	    "prep": "claude",
273	    "critique": "codex",
274	    "revise": "claude",
275	    "gate": "claude",
276	    "finalize": "claude",
277	    "execute": "codex",
278	    "loop_plan": "claude",
279	    "loop_execute": "codex",
280	    "review": "codex",
281	    "tiebreaker_researcher": "codex",
282	    "tiebreaker_challenger": "codex",
283	}
284	KNOWN_AGENTS = ["claude", "codex", "hermes"]
285	ROBUSTNESS_LEVELS = ("tiny", "light", "standard", "robust", "superrobust")
286	def parse_agent_spec(spec: str) -> tuple[str, str | None]:
287	    """Parse 'hermes:model/name' → ('hermes', 'model/name') or 'claude' → ('claude', None)."""
288	    if ":" in spec:
289	        agent, model = spec.split(":", 1)
290	        return agent, model
291	    return spec, None
292	
293	
294	SCOPE_CREEP_TERMS = (
295	    "scope creep",
296	    "out of scope",
297	    "beyond the original idea",
298	    "beyond original idea",
299	    "beyond user intent",
300	    "expanded scope",
301	)
302	
303	DEFAULTS = {
304	    "execution.auto_approve": False,
305	    "execution.robustness": "standard",
306	    "execution.worker_timeout_seconds": 7200,
307	    "execution.max_review_rework_cycles": 3,
308	    "execution.max_robust_review_rework_cycles": 2,
309	    "execution.max_execute_no_progress": 3,
310	    "orchestration.max_critique_concurrency": 2,
311	    "orchestration.mode": "subagent",
312	}
313	
314	_SETTABLE_BOOL = {
315	    "execution.auto_approve",
316	}
317	
318	_SETTABLE_ENUM = {
319	    "execution.robustness": ROBUSTNESS_LEVELS,
320	}
321	
322	_SETTABLE_NUMERIC = {
323	    "execution.worker_timeout_seconds",
324	    "execution.max_review_rework_cycles",
325	    "execution.max_robust_review_rework_cycles",
326	    "execution.max_execute_no_progress",
327	    "orchestration.max_critique_concurrency",
328	}
329	
330	
331	# ---------------------------------------------------------------------------
332	# Exception
333	# ---------------------------------------------------------------------------
334	
335	class CliError(Exception):
336	    def __init__(
337	        self,
338	        code: str,
339	        message: str,
340	        *,
341	        valid_next: list[str] | None = None,
342	        extra: dict[str, Any] | None = None,
343	        exit_code: int = 1,
344	    ) -> None:
345	        super().__init__(message)
346	        self.code = code
347	        self.message = message
348	        self.valid_next = valid_next or []
349	        self.extra = extra or {}
350	        self.exit_code = exit_code
351
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/tests/test_schemas.py"
}
```

> TOOL

tool_result Read
```
1	"""Direct tests for megaplan.schemas."""
2	
3	from __future__ import annotations
4	
5	import json
6	from pathlib import Path
7	
8	from jsonschema import Draft7Validator
9	
10	from megaplan.schemas import SCHEMAS, strict_schema
11	
12	
13	def _review_disk_schema() -> dict[str, object]:
14	    return json.loads((Path(__file__).resolve().parents[1] / ".megaplan" / "schemas" / "review.json").read_text(encoding="utf-8"))
15	
16	
17	def _minimal_review_payload() -> dict[str, object]:
18	    return {
19	        "review_verdict": "approved",
20	        "checks": [],
21	        "pre_check_flags": [],
22	        "verified_flag_ids": [],
23	        "disputed_flag_ids": [],
24	        "criteria": [],
25	        "issues": [],
26	        "rework_items": [],
27	        "summary": "Approved.",
28	        "task_verdicts": [],
29	        "sense_check_verdicts": [],
30	    }
31	
32	
33	def test_schema_registry_matches_5_step_workflow() -> None:
34	    required = {"plan.json", "prep.json", "revise.json", "gate.json", "critique.json", "finalize.json", "execution.json", "review.json"}
35	    assert required.issubset(set(SCHEMAS))
36	
37	
38	# ---------------------------------------------------------------------------
39	# strict_schema tests
40	# ---------------------------------------------------------------------------
41	
42	
43	def test_strict_schema_adds_additional_properties_false() -> None:
44	    result = strict_schema({"type": "object", "properties": {"a": {"type": "string"}}})
45	    assert result["additionalProperties"] is False
46	
47	
48	def test_strict_schema_preserves_existing_additional_properties() -> None:
49	    result = strict_schema({"type": "object", "properties": {"a": {"type": "string"}}, "additionalProperties": True})
50	    assert result["additionalProperties"] is True
51	
52	
53	def test_strict_schema_sets_required_from_properties() -> None:
54	    result = strict_schema({"type": "object", "properties": {"x": {"type": "string"}, "y": {"type": "number"}}})
55	    assert set(result["required"]) == {"x", "y"}
56	
57	
58	def test_strict_schema_normalizes_partial_required_arrays_recursively() -> None:
59	    schema = {
60	        "type": "object",
61	        "required": ["stale_root"],
62	        "properties": {
63	            "inner": {
64	                "type": "object",
65	                "required": ["stale_inner"],
66	                "properties": {"child": {"type": "string"}},
67	            },
68	            "items": {
69	                "type": "array",
70	                "items": {
71	                    "type": "object",
72	                    "required": ["stale_item"],
73	                    "properties": {"name": {"type": "string"}},
74	                },
75	            },
76	        },
77	    }
78	
79	    result = strict_schema(schema)
80	
81	    assert result["required"] == ["inner", "items"]
82	    assert result["properties"]["inner"]["required"] == ["child"]
83	    assert result["properties"]["items"]["items"]["required"] == ["name"]
84	
85	
86	def test_strict_schema_nested_objects_get_additional_properties() -> None:
87	    schema = {
88	        "type": "object",
89	        "properties": {
90	            "inner": {"type": "object", "properties": {"a": {"type": "string"}}},
91	        },
92	    }
93	    result = strict_schema(schema)
94	    assert result["properties"]["inner"]["additionalProperties"] is False
95	    assert result["properties"]["inner"]["required"] == ["a"]
96	
97	
98	def test_strict_schema_array_items_are_strict() -> None:
99	    schema = {
100	        "type": "object",
101	        "properties": {
102	            "list": {
103	                "type": "array",
104	                "items": {"type": "object", "properties": {"name": {"type": "string"}}},
105	            }
106	        },
107	    }
108	    result = strict_schema(schema)
109	    assert result["properties"]["list"]["items"]["additionalProperties"] is False
110	
111	
112	def test_strict_schema_deeply_nested() -> None:
113	    schema = {
114	        "type": "object",
115	        "properties": {
116	            "l1": {
117	                "type": "object",
118	                "properties": {
119	                    "l2": {
120	                        "type": "object",
121	                        "properties": {"l3": {"type": "string"}},
122	                    }
123	                },
124	            }
125	        },
126	    }
127	    result = strict_schema(schema)
128	    assert result["properties"]["l1"]["properties"]["l2"]["additionalProperties"] is False
129	
130	
131	def test_strict_schema_non_object_untouched() -> None:
132	    assert strict_schema({"type": "string"}) == {"type": "string"}
133	    assert strict_schema(42) == 42
134	    assert strict_schema("hello") == "hello"
135	    assert strict_schema([1, 2]) == [1, 2]
136	
137	
138	# ---------------------------------------------------------------------------
139	# Schema completeness tests
140	# ---------------------------------------------------------------------------
141	
142	
143	def test_schema_registry_has_all_expected_steps() -> None:
144	    required_schemas = {"plan.json", "prep.json", "revise.json", "gate.json", "critique.json", "finalize.json", "execution.json", "review.json"}
145	    assert required_schemas.issubset(set(SCHEMAS.keys()))
146	
147	
148	def test_schema_registry_entries_include_required_field() -> None:
149	    for name, schema in SCHEMAS.items():
150	        assert "required" in schema, f"Schema '{name}' missing 'required' field"
151	        assert isinstance(schema["required"], list)
152	
153	
154	def test_schema_registry_entries_are_objects() -> None:
155	    for name, schema in SCHEMAS.items():
156	        assert schema.get("type") == "object", f"Schema '{name}' is not type 'object'"
157	        assert "properties" in schema, f"Schema '{name}' missing 'properties'"
158	
159	
160	def test_critique_schema_flags_have_expected_structure() -> None:
161	    critique = SCHEMAS["critique.json"]
162	    flags_schema = critique["properties"]["flags"]
163	    assert flags_schema["type"] == "array"
164	    item_schema = flags_schema["items"]
165	    assert "id" in item_schema["properties"]
166	    assert "concern" in item_schema["properties"]
167	    assert "category" in item_schema["properties"]
168	    assert "severity_hint" in item_schema["properties"]
169	    assert "evidence" in item_schema["properties"]
170	
171	
172	def test_finalize_schema_tracks_structured_execution_fields() -> None:
173	    finalize = SCHEMAS["finalize.json"]
174	    assert "tasks" in finalize["properties"]
175	    assert "sense_checks" in finalize["properties"]
176	    assert "validation" in finalize["properties"]
177	    assert "baseline_test_failures" in finalize["properties"]
178	    assert "baseline_test_command" in finalize["properties"]
179	    assert "baseline_test_note" in finalize["properties"]
180	    assert "validation" in finalize["required"]
181	    assert "baseline_test_failures" not in finalize["required"]
182	    assert "baseline_test_command" not in finalize["required"]
183	    assert "baseline_test_note" not in finalize["required"]
184	    assert "final_plan" not in finalize["properties"]
185	    assert "task_count" not in finalize["properties"]
186	    task_schema = finalize["properties"]["tasks"]["items"]
187	    assert set(task_schema["properties"]) == {
188	        "id",
189	        "description",
190	        "depends_on",
191	        "status",
192	        "executor_notes",
193	        "files_changed",
194	        "commands_run",
195	        "evidence_files",
196	        "reviewer_verdict",
197	    }
198	    assert task_schema["properties"]["status"]["enum"] == ["pending", "done", "skipped"]
199	    assert "executor_note" in finalize["properties"]["sense_checks"]["items"]["properties"]
200	    # Validation sub-schema
201	    validation_schema = finalize["properties"]["validation"]
202	    assert "plan_steps_covered" in validation_schema["properties"]
203	    assert "orphan_tasks" in validation_schema["properties"]
204	    assert "completeness_notes" in validation_schema["properties"]
205	    assert "coverage_complete" in validation_schema["properties"]
206	    step_item = validation_schema["properties"]["plan_steps_covered"]["items"]
207	    assert "plan_step_summary" in step_item["properties"]
208	    assert "finalize_task_ids" in step_item["properties"]
209	    assert step_item["properties"]["finalize_task_ids"]["type"] == "array"
210	
211	
212	def test_execution_schema_requires_task_updates() -> None:
213	    execution = SCHEMAS["execution.json"]
214	    assert "task_updates" in execution["properties"]
215	    assert "task_updates" in execution["required"]
216	    assert "sense_check_acknowledgments" in execution["properties"]
217	    assert "sense_check_acknowledgments" in execution["required"]
218	    item_schema = execution["properties"]["task_updates"]["items"]
219	    assert item_schema["properties"]["status"]["enum"] == ["done", "skipped"]
220	    assert "files_changed" in item_schema["properties"]
221	    assert "commands_run" in item_schema["properties"]
222	
223	
224	def test_review_schema_requires_task_and_sense_check_verdicts() -> None:
225	    review = SCHEMAS["review.json"]
226	    assert "review_verdict" in review["properties"]
227	    assert "task_verdicts" in review["properties"]
228	    assert "sense_check_verdicts" in review["properties"]
229	    assert "rework_items" in review["properties"]
230	    assert "review_verdict" in review["required"]
231	    assert "task_verdicts" in review["required"]
232	    assert "sense_check_verdicts" in review["required"]
233	    assert "rework_items" in review["required"]
234	    assert "evidence_files" in review["properties"]["task_verdicts"]["items"]["properties"]
235	    # Rework items sub-schema
236	    rework_item = review["properties"]["rework_items"]["items"]
237	    assert "task_id" in rework_item["properties"]
238	    assert "issue" in rework_item["properties"]
239	    assert "expected" in rework_item["properties"]
240	    assert "actual" in rework_item["properties"]
241	    assert "evidence_file" in rework_item["properties"]
242	    assert "flag_id" in rework_item["properties"]
243	    assert "source" in rework_item["properties"]
244	    assert set(rework_item["required"]) == {"task_id", "issue", "expected", "actual", "evidence_file", "flag_id", "source"}
245	    assert rework_item["properties"]["flag_id"]["type"] == ["string", "null"]
246	    assert rework_item["properties"]["source"]["type"] == ["string", "null"]
247	
248	
249	def test_review_schema_accepts_parallel_mode_extensions_in_both_copies() -> None:
250	    payload = {
251	        "review_verdict": "needs_rework",
252	        "checks": [
253	            {
254	                "id": "coverage",
255	                "question": "Does the diff cover the issue?",
256	                "guidance": "Inspect the changed module for missing review follow-up.",
257	                "findings": [
258	                    {
259	                        "detail": "Coverage review found one concrete issue example that the diff still does not handle.",
260	                        "flagged": True,
261	                        "status": "blocking",
262	                        "evidence_file": "pkg/module.py",
263	                    }
264	                ],
265	                "prior_findings": [],
266	            }
267	        ],
268	        "pre_check_flags": [
269	            {
270	                "id": "PRECHECK-SOURCE_TOUCH",
271	                "check": "source_touch",
272	                "detail": "The diff touches a package source file.",
273	                "severity": "minor",
274	                "evidence_file": "pkg/module.py",
275	            }
276	        ],
277	        "verified_flag_ids": ["REVIEW-COVERAGE-001"],
278	        "disputed_flag_ids": ["REVIEW-PARITY-001"],
279	        "criteria": [{"name": "criterion", "priority": "must", "pass": "fail", "evidence": "Missing coverage."}],
280	        "issues": ["Coverage review found a blocking issue."],
281	        "rework_items": [
282	            {
283	                "task_id": "REVIEW",
284	                "issue": "Coverage gap remains.",
285	                "expected": "All issue examples are covered.",
286	                "actual": "One issue example remains uncovered.",
287	                "evidence_file": "pkg/module.py",
288	                "flag_id": None,
289	                "source": "review_coverage",
290	            }
291	        ],
292	        "summary": "Heavy review found a blocking issue.",
293	        "task_verdicts": [
294	            {
295	                "task_id": "T1",
296	                "reviewer_verdict": "Needs follow-up.",
297	                "evidence_files": ["pkg/module.py"],
298	            }
299	        ],
300	        "sense_check_verdicts": [{"sense_check_id": "SC1", "verdict": "Needs follow-up."}],
301	    }
302	    disk_schema = _review_disk_schema()
303	
304	    assert list(Draft7Validator(SCHEMAS["review.json"]).iter_errors(payload)) == []
305	    assert list(Draft7Validator(disk_schema).iter_errors(payload)) == []
306	
307	
308	def test_review_schema_accepts_optional_rework_item_flag_id() -> None:
309	    payload = _minimal_review_payload()
310	    payload["review_verdict"] = "needs_rework"
311	    payload["issues"] = ["Critique flag remains unresolved."]
312	    payload["rework_items"] = [
313	        {
314	            "task_id": "REVIEW",
315	            "issue": "Critique flag remains unresolved.",
316	            "expected": "The final diff addresses the flagged concern directly.",
317	            "actual": "The diff leaves the flagged behavior unchanged.",
318	            "evidence_file": "megaplan/prompts/review.py",
319	            "flag_id": "FLAG-001",
320	            "source": "review_flag_reverify",
321	        }
322	    ]
323	    disk_schema = _review_disk_schema()
324	
325	    assert list(Draft7Validator(SCHEMAS["review.json"]).iter_errors(payload)) == []
326	    assert list(Draft7Validator(disk_schema).iter_errors(payload)) == []
327	
328	
329	def test_review_schema_still_accepts_rework_items_without_flag_id() -> None:
330	    payload = _minimal_review_payload()
331	    payload["review_verdict"] = "needs_rework"
332	    payload["issues"] = ["Executor still needs to finish the review follow-up."]
333	    payload["rework_items"] = [
334	        {
335	            "task_id": "REVIEW",
336	            "issue": "Executor still needs to finish the review follow-up.",
337	            "expected": "All required review follow-up work is complete.",
338	            "actual": "One required review follow-up item is still missing.",
339	            "evidence_file": "megaplan/handlers.py",
340	            "flag_id": None,
341	            "source": None,
342	        }
343	    ]
344	    disk_schema = _review_disk_schema()
345	
346	    assert list(Draft7Validator(SCHEMAS["review.json"]).iter_errors(payload)) == []
347	    assert list(Draft7Validator(disk_schema).iter_errors(payload)) == []
348	
349	
350	# ---------------------------------------------------------------------------
351	# Original tests
352	# ---------------------------------------------------------------------------
353	
354	
355	def test_gate_schema_is_strict_and_requires_core_fields() -> None:
356	    schema = strict_schema(SCHEMAS["gate.json"])
357	    assert schema["additionalProperties"] is False
358	    assert schema["required"] == [
359	        "recommendation",
360	        "rationale",
361	        "signals_assessment",
362	        "warnings",
363	        "settled_decisions",
364	        "flag_resolutions",
365	        "accepted_tradeoffs",
366	    ]
367	    assert schema["properties"]["recommendation"]["enum"] == ["PROCEED", "ITERATE", "ESCALATE"]
368	
369	
370	def test_plan_schema_has_core_fields_only() -> None:
371	    schema = strict_schema(SCHEMAS["plan.json"])
372	    assert set(schema["required"]) == {"plan", "questions", "success_criteria", "assumptions"}
373	    assert "self_flags" not in schema["properties"]
374	    assert "gate_recommendation" not in schema["properties"]
375	
376	
377	def test_prep_schema_exists_and_has_expected_structure() -> None:
378	    schema = strict_schema(SCHEMAS["prep.json"])
379	    assert set(schema["required"]) == {
380	        "skip",
381	        "task_summary",
382	        "key_evidence",
383	        "relevant_code",
384	        "test_expectations",
385	        "constraints",
386	        "suggested_approach",
387	    }
388	    evidence_schema = schema["properties"]["key_evidence"]["items"]
389	    relevant_code_schema = schema["properties"]["relevant_code"]["items"]
390	    test_expectation_schema = schema["properties"]["test_expectations"]["items"]
391	    assert set(evidence_schema["required"]) == {"point", "source", "relevance"}
392	    assert evidence_schema["properties"]["relevance"]["enum"] == ["high", "medium", "low"]
393	    assert set(relevant_code_schema["required"]) == {"file_path", "why", "functions"}
394	    assert relevant_code_schema["properties"]["functions"]["items"]["type"] == "string"
395	    assert set(test_expectation_schema["required"]) == {"test_id", "what_it_checks", "status"}
396	    assert test_expectation_schema["properties"]["status"]["enum"] == ["fail_to_pass", "pass_to_pass"]
397	
398	
399	def test_gate_schema_includes_settled_decisions_structure() -> None:
400	    schema = strict_schema(SCHEMAS["gate.json"])
401	    item_schema = schema["properties"]["settled_decisions"]["items"]
402	    assert set(item_schema["required"]) == {"id", "decision", "rationale"}
403	    assert "rationale" in item_schema["properties"]
404	
405	
406	def test_gate_schema_flag_resolutions_stay_codex_compatible() -> None:
407	    schema = strict_schema(SCHEMAS["gate.json"])
408	    item_schema = schema["properties"]["flag_resolutions"]["items"]
409	
410	    assert set(item_schema["required"]) == {"flag_id", "action", "evidence", "rationale"}
411	    assert "oneOf" not in item_schema
412	    assert set(item_schema["properties"]["action"]["enum"]) == {"dispute", "accept_tradeoff"}
413	    assert "evidence" in item_schema["properties"]
414	    assert "rationale" in item_schema["properties"]
415	
416	
417	def test_schema_registry_covers_the_six_strict_mode_required_fixes() -> None:
418	    revise = SCHEMAS["revise.json"]
419	    gate = SCHEMAS["gate.json"]
420	    review = SCHEMAS["review.json"]
421	    review_check = review["properties"]["checks"]["items"]
422	    review_finding = review_check["properties"]["findings"]["items"]
423	    pre_check_flag = review["properties"]["pre_check_flags"]["items"]
424	
425	    assert set(revise["required"]) == {
426	        "plan",
427	        "changes_summary",
428	        "flags_addressed",
429	        "assumptions",
430	        "success_criteria",
431	        "questions",
432	    }
433	    assert set(gate["required"]) == {
434	        "recommendation",
435	        "rationale",
436	        "signals_assessment",
437	        "warnings",
438	        "settled_decisions",
439	        "flag_resolutions",
440	        "accepted_tradeoffs",
441	    }
442	    assert set(review["required"]) == {
443	        "review_verdict",
444	        "checks",
445	        "pre_check_flags",
446	        "verified_flag_ids",
447	        "disputed_flag_ids",
448	        "criteria",
449	        "issues",
450	        "rework_items",
451	        "summary",
452	        "task_verdicts",
453	        "sense_check_verdicts",
454	    }
455	    assert set(review_check["required"]) == {"id", "question", "guidance", "findings", "prior_findings"}
456	    assert set(review_finding["required"]) == {"detail", "flagged", "status", "evidence_file"}
457	    assert set(pre_check_flag["required"]) == {"id", "check", "detail", "severity", "evidence_file"}
458	
459	
460	def test_strict_schema_new_tracking_objects_are_strict() -> None:
461	    schema = strict_schema(SCHEMAS["finalize.json"])
462	    task_schema = schema["properties"]["tasks"]["items"]
463	    sense_check_schema = schema["properties"]["sense_checks"]["items"]
464	    assert task_schema["additionalProperties"] is False
465	    assert set(task_schema["required"]) == {
466	        "id",
467	        "description",
468	        "depends_on",
469	        "status",
470	        "executor_notes",
471	        "files_changed",
472	        "commands_run",
473	        "evidence_files",
474	        "reviewer_verdict",
475	    }
476	    assert sense_check_schema["additionalProperties"] is False
477	    assert set(sense_check_schema["required"]) == {"id", "task_id", "question", "executor_note", "verdict"}
478
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py"
}
```

> TOOL

tool_result Read
```
File content (65170 tokens) exceeds maximum allowed tokens (10000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/tests/ | grep test_verifiability"
}
```

> TOOL

tool_result Bash
```
[rerun: b1]
```

> AGENT

Now let me read the handlers.py section around the verify_human handlers:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 2100,
  "limit": 200
}
```

> TOOL

tool_result Read
```
2100	        "step": "override",
2101	        "summary": summary,
2102	        "next_step": next_steps[0] if next_steps else None,
2103	        "state": state["current_state"],
2104	        "previous_robustness": previous_level,
2105	        "robustness": new_level,
2106	    }
2107	    _attach_next_step_runtime(response)
2108	    return response
2109	
2110	
2111	_OVERRIDE_ACTIONS: dict[str, Callable[[Path, Path, PlanState, argparse.Namespace], StepResponse]] = {
2112	    "add-note": _override_add_note,
2113	    "abort": _override_abort,
2114	    "force-proceed": _override_force_proceed,
2115	    "replan": _override_replan,
2116	    "set-robustness": _override_set_robustness,
2117	}
2118	
2119	
2120	def handle_override(root: Path, args: argparse.Namespace) -> StepResponse:
2121	    plan_dir, state = load_plan(root, args.plan)
2122	    action = args.override_action
2123	    handler = _OVERRIDE_ACTIONS.get(action)
2124	    if handler is None:
2125	        raise CliError("invalid_override", f"Unknown override action: {action}")
2126	    return handler(root, plan_dir, state, args)
2127	
2128	
2129	def handle_verify_human(root: Path, args: argparse.Namespace) -> StepResponse:
2130	    from megaplan._core import plans_root, resolve_plan_dir
2131	    plan_dir, state = load_plan(root, args.plan)
2132	
2133	    if state["current_state"] != STATE_AWAITING_HUMAN:
2134	        raise CliError(
2135	            "wrong_state",
2136	            f"verify-human requires state 'awaiting_human_verify', got '{state['current_state']}'.",
2137	        )
2138	
2139	    criterion_ref = args.criterion
2140	    passed = getattr(args, "pass_flag", False)
2141	    failed = getattr(args, "fail_flag", False)
2142	    evidence = args.evidence
2143	
2144	    plan_meta = read_json(latest_plan_meta_path(plan_dir, state))
2145	    success_criteria = plan_meta.get("success_criteria", [])
2146	
2147	    target_idx: int | None = None
2148	    try:
2149	        idx = int(criterion_ref)
2150	        if 0 <= idx < len(success_criteria):
2151	            target_idx = idx
2152	    except (ValueError, TypeError):
2153	        for i, sc in enumerate(success_criteria):
2154	            if sc.get("criterion", "") == criterion_ref:
2155	                target_idx = i
2156	                break
2157	
2158	    if target_idx is None:
2159	        raise CliError("invalid_criterion", f"Criterion not found: {criterion_ref!r}")
2160	
2161	    verifications_path = plan_dir / "human_verifications.json"
2162	    verifications: list[dict[str, Any]] = []
2163	    if verifications_path.exists():
2164	        verifications = read_json(verifications_path)
2165	        if not isinstance(verifications, list):
2166	            verifications = []
2167	
2168	    verifications.append({
2169	        "criterion_idx": target_idx,
2170	        "criterion": success_criteria[target_idx].get("criterion", ""),
2171	        "verdict": "pass" if passed else "fail",
2172	        "evidence": evidence,
2173	        "timestamp": now_utc(),
2174	    })
2175	    atomic_write_json(verifications_path, verifications)
2176	
2177	    verified_idxs = {
2178	        v["criterion_idx"] for v in verifications if v.get("verdict") == "pass"
2179	    }
2180	
2181	    from megaplan.capabilities import get_worker_capabilities
2182	    from megaplan.verifiability import classify_criteria
2183	
2184	    worker_caps = get_worker_capabilities(state)
2185	    _, human_deferred = classify_criteria(success_criteria, worker_caps)
2186	    deferred_must_idxs = {
2187	        i for i, sc in enumerate(success_criteria)
2188	        if sc in human_deferred and sc.get("priority") == "must"
2189	    }
2190	
2191	    all_verified = deferred_must_idxs <= verified_idxs
2192	    if all_verified:
2193	        state["current_state"] = STATE_DONE
2194	        save_state(plan_dir, state)
2195	        summary = "All deferred must criteria verified. Plan transitioned to done."
2196	    else:
2197	        remaining = deferred_must_idxs - verified_idxs
2198	        summary = f"Verification recorded. {len(remaining)} deferred must criteria remaining."
2199	
2200	    return {
2201	        "success": True,
2202	        "step": "verify-human",
2203	        "plan": state["name"],
2204	        "state": state["current_state"],
2205	        "summary": summary,
2206	        "criterion_idx": target_idx,
2207	        "verdict": "pass" if passed else "fail",
2208	    }
2209	
2210	
2211	def handle_audit_verifiability(root: Path, args: argparse.Namespace) -> StepResponse:
2212	    plan_dir, state = load_plan(root, args.plan)
2213	
2214	    plan_meta = read_json(latest_plan_meta_path(plan_dir, state))
2215	    success_criteria = plan_meta.get("success_criteria", [])
2216	
2217	    from megaplan.capabilities import get_worker_capabilities
2218	    from megaplan.verifiability import audit_criteria, validate_requires
2219	
2220	    worker_caps = get_worker_capabilities(state)
2221	    audits = audit_criteria(success_criteria, worker_caps)
2222	    issues = validate_requires(success_criteria)
2223	
2224	    audit_results = []
2225	    for audit in audits:
2226	        sc = success_criteria[audit.criterion_idx] if audit.criterion_idx < len(success_criteria) else {}
2227	        audit_results.append({
2228	            "criterion_idx": audit.criterion_idx,
2229	            "criterion": sc.get("criterion", ""),
2230	            "priority": sc.get("priority", ""),
2231	            "verdict": audit.verdict,
2232	            "rationale": audit.rationale,
2233	            "missing_caps": audit.missing_caps,
2234	        })
2235	
2236	    return {
2237	        "success": True,
2238	        "step": "audit-verifiability",
2239	        "plan": state["name"],
2240	        "summary": f"Audited {len(success_criteria)} criteria: {sum(1 for a in audits if a.verdict == 'machine_verifiable')} machine-verifiable, {sum(1 for a in audits if a.verdict == 'human_only')} human-only, {sum(1 for a in audits if a.verdict == 'unverifiable_no_worker')} unverifiable.",
2241	        "audits": audit_results,
2242	        "validation_issues": issues,
2243	    }
2244
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"_resolve_review_outcome\\|handle_verify_human\" /Users/user_c042661f/Documents/megaplan/megaplan/handlers.py | head -20"
}
```

> TOOL

tool_result Bash
```
1562:def _resolve_review_outcome(
1742:                result, next_state, next_step = _resolve_review_outcome(
1872:        result, next_state, next_step = _resolve_review_outcome(
2129:def handle_verify_human(root: Path, args: argparse.Namespace) -> StepResponse:
[rerun: b2]
```

> AGENT

Now let me read the _resolve_review_outcome function:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 1562,
  "limit": 150
}
```

> TOOL

tool_result Read
```
1562	def _resolve_review_outcome(
1563	    review_verdict: str,
1564	    verdict_count: int,
1565	    total_tasks: int,
1566	    check_count: int,
1567	    total_checks: int,
1568	    missing_evidence: list[str],
1569	    robustness: str,
1570	    state: PlanState,
1571	    issues: list[str],
1572	    criteria: list[dict[str, Any]] | None = None,
1573	) -> tuple[str, str, str | None]:
1574	    """Determine review result, next state, and next step.
1575	
1576	    Returns (result, next_state, next_step).
1577	    """
1578	    blocked = (
1579	        verdict_count < total_tasks
1580	        or check_count < total_checks
1581	        or bool(missing_evidence)
1582	    )
1583	    if blocked:
1584	        return "blocked", STATE_EXECUTED, "review"
1585	
1586	    rework_requested = review_verdict == "needs_rework"
1587	    if rework_requested:
1588	        cap_key = (
1589	            "max_robust_review_rework_cycles"
1590	            if robustness in {"robust", "superrobust"}
1591	            else "max_review_rework_cycles"
1592	        )
1593	        max_review_rework_cycles = get_effective("execution", cap_key)
1594	        prior_rework_count = sum(
1595	            1 for entry in state.get("history", [])
1596	            if entry.get("step") == "review" and entry.get("result") == "needs_rework"
1597	        )
1598	        if prior_rework_count >= max_review_rework_cycles:
1599	            issues.append(
1600	                f"Max review rework cycles ({max_review_rework_cycles}) reached. "
1601	                "Force-proceeding to done despite unresolved review issues."
1602	            )
1603	        else:
1604	            return "needs_rework", STATE_FINALIZED, "execute"
1605	
1606	    if criteria:
1607	        has_deferred_must = any(
1608	            c.get("pass") == "deferred_human" and c.get("priority") == "must"
1609	            for c in criteria
1610	        )
1611	        if has_deferred_must:
1612	            return "success", STATE_AWAITING_HUMAN, None
1613	
1614	    return "success", STATE_DONE, None
1615	
1616	
1617	_EXPECTED_BY_CHECK_ID = {
1618	    "coverage": "Extend the fix so every concrete failing example, symptom, or 'X should Y' statement in the issue is addressed by at least one diff line.",
1619	    "placement": "Move the fix upstream to where the bad state is first introduced, or extend it to cover any alternate entry points identified in the finding.",
1620	    "adjacent_calls": "Apply the same fix to each additional call site, sibling class, or downstream consumer identified in the finding.",
1621	    "simplicity": "Remove unjustified changes, or justify each extra line against a concrete issue requirement.",
1622	}
1623	
1624	
1625	def _synthesize_review_rework_items(checks: list[dict[str, Any]]) -> list[dict[str, str]]:
1626	    rework_items: list[dict[str, str]] = []
1627	    for check in checks:
1628	        check_id = check.get("id", "")
1629	        if not isinstance(check_id, str) or not check_id:
1630	            continue
1631	        check_def = review_checks.get_check_by_id(check_id)
1632	        if getattr(check_def, "default_severity", "") != "likely-significant":
1633	            continue
1634	        question = str(check.get("question", "") or "").strip()
1635	        findings = check.get("findings", [])
1636	        if not isinstance(findings, list):
1637	            continue
1638	        for finding in findings:
1639	            if not isinstance(finding, dict) or not finding.get("flagged"):
1640	                continue
1641	            status = str(finding.get("status", "") or "").strip().lower()
1642	            # megaplan/prompts/review.py:243-249 constrains status to {blocking, significant, minor, n/a};
1643	            # significant is the explicit non-blocking downgrade for gate-settled concerns, while missing or
1644	            # empty status means the model failed to classify, so we keep the check's default_severity gate as
1645	            # the blocking fallback. That is the safe default for the sympy-21930 / sphinx-9711 regressions.
1646	            if status and status != "blocking":
1647	                continue
1648	            detail = str(finding.get("detail", "") or "").strip()
1649	            evidence_file = finding.get("evidence_file", "")
1650	            if not isinstance(evidence_file, str):
1651	                evidence_file = ""
1652	            issue = detail or question or f"Heavy review found a blocking {check_id} issue."
1653	            # Prefer a per-check actionable expected string; fall back to the
1654	            # check's self-question; ultimately fall back to a generic message.
1655	            expected = (
1656	                _EXPECTED_BY_CHECK_ID.get(check_id)
1657	                or question
1658	                or f"Review check '{check_id}' should pass without blocking findings."
1659	            )
1660	            # `actual` should NOT duplicate `issue` — use a templated
1661	            # acknowledgment of the finding instead so the executor sees
1662	            # a clear "you didn't resolve it" signal without a copy of
1663	            # the detail text.
1664	            actual = f"The diff did not resolve the flagged {check_id} concern above."
1665	            rework_items.append(
1666	                {
1667	                    "task_id": f"REVIEW-{check_id}",
1668	                    "issue": issue,
1669	                    "expected": expected,
1670	                    "actual": actual,
1671	                    "evidence_file": evidence_file,
1672	                    "source": f"review_{check_id}",
1673	                }
1674	            )
1675	    return rework_items
1676	
1677	
1678	def handle_review(root: Path, args: argparse.Namespace) -> StepResponse:
1679	    with load_plan_locked(root, args.plan, step="review") as (plan_dir, state):
1680	        require_state(state, "review", {STATE_EXECUTED})
1681	        robustness = configured_robustness(state)
1682	        pre_check_flags: list[dict[str, Any]] = []
1683	        if robustness in {"standard", "robust", "superrobust"}:
1684	            pre_check_flags = run_pre_checks(plan_dir, state, Path(state["config"]["project_dir"]))
1685	        if robustness in {"standard", "light", "robust"}:
1686	            resolved = None
1687	            prompt_override = None
1688	            prompt_kwargs = None
1689	            if robustness in {"standard", "robust"}:
1690	                resolved = resolve_agent_mode("review", args)
1691	                if _supports_prompt_kwargs(worker_module.run_step_with_worker):
1692	                    prompt_kwargs = {"pre_check_flags": pre_check_flags}
1693	                else:
1694	                    prompt_override = _build_review_prompt_override(
1695	                        resolved[0],
1696	                        state,
1697	                        plan_dir,
1698	                        root=root,
1699	                        pre_check_flags=pre_check_flags,
1700	                    )
1701	            worker, agent, mode, refreshed = _run_worker(
1702	                "review",
1703	                state,
1704	                plan_dir,
1705	                args,
1706	                root=root,
1707	                resolved=resolved,
1708	                prompt_override=prompt_override,
1709	                prompt_kwargs=prompt_kwargs,
1710	            )
1711	            if robustness in {"standard", "robust"}:
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/auto.py",
  "offset": 1,
  "limit": 200
}
```

> TOOL

tool_result Read
```
1	"""Auto-driver that advances a plan through its phases without human intervention.
2	
3	This is the mechanical loop that most orchestrators end up writing by hand:
4	read `status`, run `next_step`, repeat until terminal. All real judgment is
5	delegated to megaplan's existing phase logic — the driver only applies two
6	documented defaults:
7	
8	1. Gate ESCALATE → force-proceed (caller opts out with ``--on-escalate abort``
9	   or ``--on-escalate fail``).
10	2. Same state for N consecutive iterations → bail (stall detection).
11	
12	The driver is intentionally dumb. If a run needs judgment the driver can't
13	provide, it exits with a non-zero status and prints the state snapshot so the
14	caller can intervene.
15	"""
16	from __future__ import annotations
17	
18	import argparse
19	import json
20	import subprocess
21	import sys
22	import time
23	from dataclasses import dataclass, field
24	from pathlib import Path
25	from typing import Any
26	
27	from megaplan.types import AUTOMATION_TERMINAL_STATES, STATE_AWAITING_HUMAN, TERMINAL_STATES
28	
29	
30	DEFAULT_STALL_THRESHOLD = 5
31	DEFAULT_MAX_ITERATIONS = 200
32	DEFAULT_POLL_SLEEP_SECONDS = 1.0
33	DEFAULT_PHASE_TIMEOUT_SECONDS = 3600
34	DEFAULT_STATUS_TIMEOUT_SECONDS = 60
35	ESCALATE_ACTIONS = ("force-proceed", "abort", "fail")
36	PHASE_TIMEOUT_EXIT_CODE = 124  # conventional; matches GNU `timeout`
37	
38	
39	@dataclass
40	class DriverOutcome:
41	    """Terminal outcome reported when the loop exits."""
42	
43	    status: str  # "done" | "stalled" | "escalated" | "failed" | "aborted" | "cap"
44	    plan: str
45	    final_state: str
46	    iterations: int
47	    reason: str = ""
48	    last_phase: str | None = None
49	    events: list[dict[str, Any]] = field(default_factory=list)
50	
51	    def to_json(self) -> str:
52	        return json.dumps(
53	            {
54	                "status": self.status,
55	                "plan": self.plan,
56	                "final_state": self.final_state,
57	                "iterations": self.iterations,
58	                "reason": self.reason,
59	                "last_phase": self.last_phase,
60	                "events": self.events,
61	            },
62	            indent=2,
63	        )
64	
65	
66	def _run_megaplan(
67	    args: list[str],
68	    *,
69	    cwd: Path | None = None,
70	    timeout: float | None = None,
71	) -> tuple[int, str, str]:
72	    """Run a megaplan sub-command in its own process.
73	
74	    We shell out rather than importing the handlers directly so each phase gets
75	    a fresh argparse/handler lifecycle. This matches how external orchestrators
76	    drive the CLI and avoids subtle state leakage between phases.
77	
78	    ``timeout`` is seconds to wait before killing the subprocess. On timeout we
79	    return exit code ``PHASE_TIMEOUT_EXIT_CODE`` and append a marker to stderr
80	    so the driver can surface it as a phase failure without crashing the loop.
81	    The subprocess is killed; any grandchildren it spawned (e.g. codex) may
82	    need a moment to settle but will exit when their parent's pipes close.
83	    """
84	    try:
85	        proc = subprocess.run(
86	            ["megaplan", *args],
87	            cwd=str(cwd) if cwd else None,
88	            capture_output=True,
89	            text=True,
90	            check=False,
91	            timeout=timeout,
92	        )
93	        return proc.returncode, proc.stdout, proc.stderr
94	    except subprocess.TimeoutExpired as expired:
95	        stdout = expired.stdout if isinstance(expired.stdout, str) else ""
96	        stderr = expired.stderr if isinstance(expired.stderr, str) else ""
97	        marker = f"\n[megaplan auto] subprocess timed out after {timeout}s"
98	        return PHASE_TIMEOUT_EXIT_CODE, stdout, (stderr + marker).strip()
99	
100	
101	def _status(
102	    plan: str,
103	    cwd: Path | None = None,
104	    *,
105	    timeout: float = DEFAULT_STATUS_TIMEOUT_SECONDS,
106	) -> dict[str, Any]:
107	    code, out, err = _run_megaplan(["status", "--plan", plan], cwd=cwd, timeout=timeout)
108	    if code != 0:
109	        raise RuntimeError(f"megaplan status failed (exit {code}): {err.strip() or out.strip()}")
110	    return json.loads(out)
111	
112	
113	def _has_valid_next(status: dict[str, Any], action: str) -> bool:
114	    return action in (status.get("valid_next") or [])
115	
116	
117	def _phase_command(next_step: str) -> list[str]:
118	    """Translate a `next_step` from status into the CLI args that run it.
119	
120	    Most phases are one-to-one: next_step == command. Execute adds the
121	    destructive + user-approved flags because auto-mode implies both.
122	    """
123	    if next_step == "execute":
124	        return ["execute", "--confirm-destructive", "--user-approved"]
125	    return [next_step]
126	
127	
128	def drive(
129	    plan: str,
130	    *,
131	    cwd: Path | None = None,
132	    stall_threshold: int = DEFAULT_STALL_THRESHOLD,
133	    max_iterations: int = DEFAULT_MAX_ITERATIONS,
134	    on_escalate: str = "force-proceed",
135	    poll_sleep: float = DEFAULT_POLL_SLEEP_SECONDS,
136	    phase_timeout: float = DEFAULT_PHASE_TIMEOUT_SECONDS,
137	    status_timeout: float = DEFAULT_STATUS_TIMEOUT_SECONDS,
138	    writer=sys.stdout.write,
139	) -> DriverOutcome:
140	    """Drive ``plan`` to completion.
141	
142	    Returns a DriverOutcome with a terminal status. The writer is used for
143	    human-readable progress; structured events are collected on the outcome.
144	    """
145	
146	    if on_escalate not in ESCALATE_ACTIONS:
147	        raise ValueError(f"on_escalate must be one of {ESCALATE_ACTIONS}")
148	
149	    events: list[dict[str, Any]] = []
150	    last_state: str | None = None
151	    stall_count = 0
152	    last_phase: str | None = None
153	
154	    def log(msg: str, **fields: Any) -> None:
155	        events.append({"msg": msg, **fields})
156	        writer(f"[auto {plan}] {msg}\n")
157	
158	    for iteration in range(1, max_iterations + 1):
159	        try:
160	            status = _status(plan, cwd=cwd, timeout=status_timeout)
161	        except (RuntimeError, json.JSONDecodeError) as error:
162	            log(f"status lookup failed: {error}")
163	            return DriverOutcome(
164	                status="failed",
165	                plan=plan,
166	                final_state=last_state or "unknown",
167	                iterations=iteration,
168	                reason=str(error),
169	                last_phase=last_phase,
170	                events=events,
171	            )
172	
173	        state = status.get("state", "")
174	        next_step = status.get("next_step")
175	        valid_next = status.get("valid_next") or []
176	
177	        log(
178	            f"iter {iteration} state={state} next={next_step} valid_next={valid_next}",
179	            iteration=iteration,
180	            state=state,
181	            next_step=next_step,
182	            valid_next=valid_next,
183	        )
184	
185	        # Terminal: plan reached a final state (or automation-terminal).
186	        if state in AUTOMATION_TERMINAL_STATES:
187	            if state == STATE_AWAITING_HUMAN:
188	                log("plan awaiting human verification — automation stopping")
189	                return DriverOutcome(
190	                    status="awaiting_human",
191	                    plan=plan,
192	                    final_state=state,
193	                    iterations=iteration,
194	                    reason="plan has criteria requiring human verification",
195	                    last_phase=last_phase,
196	                    events=events,
197	                )
198	            log(f"terminal state reached: {state}")
199	            return DriverOutcome(
200	                status="done" if state == "done" else "aborted",
```

> AGENT

Now let me search for the test_megaplan.py to understand testing patterns better:

> TOOL

tool_use Bash
```json
{
  "command": "wc -l /Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py"
}
```

> TOOL

tool_result Bash
```
5230 /Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py
[rerun: b3]
```

> AGENT

Let me get key sections from test_megaplan.py to understand the test patterns:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py",
  "offset": 1,
  "limit": 150
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	import json
4	import subprocess
5	import sys
6	import time
7	from argparse import Namespace
8	from dataclasses import dataclass
9	from datetime import datetime, timedelta, timezone
10	from pathlib import Path
11	from typing import Callable
12	
13	import pytest
14	
15	import megaplan
16	import megaplan.cli
17	import megaplan.execution
18	import megaplan.evaluation
19	import megaplan.handlers
20	import megaplan.cli
21	import megaplan._core
22	import megaplan._core.io as io_module
23	import megaplan.workers
24	from megaplan.evaluation import PLAN_STRUCTURE_REQUIRED_STEP_ISSUE, validate_plan_structure
25	from megaplan._core import (
26	    WORKFLOW,
27	    _ROBUSTNESS_OVERRIDES,
28	    clear_active_step,
29	    ensure_runtime_layout,
30	    load_plan,
31	    set_active_step,
32	    workflow_next,
33	)
34	from megaplan.prompts import create_claude_prompt
35	from megaplan.types import STATE_PREPPED
36	from megaplan.workers import WorkerResult, _build_mock_payload
37	
38	
39	def read_json(path: Path) -> dict:
40	    return json.loads(path.read_text(encoding="utf-8"))
41	
42	
43	def run_main_json(
44	    argv: list[str],
45	    *,
46	    cwd: Path,
47	    capsys: pytest.CaptureFixture[str],
48	    monkeypatch: pytest.MonkeyPatch,
49	) -> tuple[int, dict]:
50	    monkeypatch.chdir(cwd)
51	    exit_code = megaplan.main(argv)
52	    return exit_code, json.loads(capsys.readouterr().out)
53	
54	
55	def _write_lines(path: Path, count: int, *, prefix: str = "line") -> None:
56	    path.parent.mkdir(parents=True, exist_ok=True)
57	    path.write_text("\n".join(f"{prefix}_{index}" for index in range(count)) + "\n", encoding="utf-8")
58	
59	
60	def make_args_factory(project_dir: Path) -> Callable[..., Namespace]:
61	    def make_args(**overrides: object) -> Namespace:
62	        data = {
63	            "plan": None,
64	            "idea": "test idea",
65	            "name": "test-plan",
66	            "project_dir": str(project_dir),
67	            "auto_approve": None,
68	            "robustness": None,
69	            "agent": None,
70	            "ephemeral": False,
71	            "fresh": False,
72	            "persist": False,
73	            "confirm_destructive": True,
74	            "user_approved": False,
75	            "confirm_self_review": False,
76	            "batch": None,
77	            "override_action": None,
78	            "note": None,
79	            "reason": "",
80	            "robustness": None,
81	        }
82	        data.update(overrides)
83	        return Namespace(**data)
84	
85	    return make_args
86	
87	
88	@dataclass
89	class PlanFixture:
90	    root: Path
91	    project_dir: Path
92	    plan_name: str
93	    plan_dir: Path
94	    make_args: Callable[..., Namespace]
95	
96	
97	def _make_plan_fixture_with_robustness(
98	    tmp_path: Path,
99	    monkeypatch: pytest.MonkeyPatch,
100	    *,
101	    robustness: str,
102	) -> PlanFixture:
103	    root = tmp_path / "root"
104	    project_dir = tmp_path / "project"
105	    config_path = tmp_path / "config"
106	    root.mkdir()
107	    project_dir.mkdir()
108	    (project_dir / ".git").mkdir()
109	
110	    def _config_dir(home: Path | None = None) -> Path:
111	        del home
112	        return config_path
113	
114	    monkeypatch.setenv(megaplan.MOCK_ENV_VAR, "1")
115	    monkeypatch.setattr(
116	        megaplan._core.shutil,
117	        "which",
118	        lambda name: "/usr/bin/mock" if name in {"claude", "codex"} else None,
119	    )
120	    monkeypatch.setattr(io_module, "config_dir", _config_dir)
121	    monkeypatch.setattr(megaplan.cli, "config_dir", _config_dir)
122	
123	    make_args = make_args_factory(project_dir)
124	    response = megaplan.handle_init(root, make_args(robustness=robustness))
125	    plan_name = response["plan"]
126	    return PlanFixture(
127	        root=root,
128	        project_dir=project_dir,
129	        plan_name=plan_name,
130	        plan_dir=megaplan.plans_root(root) / plan_name,
131	        make_args=make_args,
132	    )
133	
134	
135	@pytest.fixture
136	def plan_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> PlanFixture:
137	    return _make_plan_fixture_with_robustness(tmp_path, monkeypatch, robustness="standard")
138	
139	
140	def load_state(plan_dir: Path) -> dict:
141	    return read_json(plan_dir / "state.json")
142	
143	
144	def latest_plan_name(plan_dir: Path) -> str:
145	    return load_state(plan_dir)["plan_versions"][-1]["file"]
146	
147	
148	def debt_registry_path(root: Path) -> Path:
149	    return root / ".megaplan" / "debt.json"
150
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"^def test_\\|^class Test\" /Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py | head -40"
}
```

> TOOL

tool_result Bash
```
235:def test_init_sets_last_gate_and_next_step_plan(plan_fixture: PlanFixture) -> None:
241:def test_init_includes_next_step_runtime(plan_fixture: PlanFixture) -> None:
253:def test_init_response_points_to_next_step_by_robustness(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
291:def test_infer_next_steps_matches_new_state_machine() -> None:
296:def test_workflow_next_matches_legacy_partial_state_cases() -> None:
326:def test_workflow_next_light_robustness_overrides(state: dict[str, object], expected: list[str]) -> None:
330:def test_workflow_definition_is_complete_for_standard_flow() -> None:
348:def test_workflow_walk_matches_documented_standard_flow() -> None:
388:def test_workflow_walk_matches_documented_robust_flow() -> None:
432:def test_workflow_walk_matches_documented_light_flow() -> None:
451:def test_all_robustness_levels_route_planned_to_critique() -> None:
460:def test_handle_plan_sets_and_clears_active_step(
493:def test_handle_plan_failure_clears_active_step(
515:def test_clear_active_step_ignores_mismatched_run_id() -> None:
526:def test_tiny_critique_stub_does_not_leak_active_step(
540:def test_capture_test_baseline_success(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
568:def test_capture_test_baseline_no_runner(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
579:def test_capture_test_baseline_timeout(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
594:def test_handle_status_reports_observability_fields(plan_fixture: PlanFixture) -> None:
648:def test_handle_status_uses_execute_runtime_guidance(plan_fixture: PlanFixture) -> None:
668:def test_handle_status_includes_progress_when_finalize_exists(plan_fixture: PlanFixture) -> None:
686:def test_handle_status_distinguishes_lock_file_from_held_lock(plan_fixture: PlanFixture) -> None:
698:def test_handle_watch_combines_status_and_progress(plan_fixture: PlanFixture) -> None:
710:def test_phase_progress_summary_completion_only(plan_fixture: PlanFixture) -> None:
726:def test_phase_progress_summary_stale(plan_fixture: PlanFixture) -> None:
741:def test_plan_rerun_keeps_iteration_and_uses_same_iteration_subversion(plan_fixture: PlanFixture) -> None:
756:def test_override_add_note_includes_next_step_runtime(plan_fixture: PlanFixture) -> None:
770:def test_handle_plan_includes_next_step_runtime(plan_fixture: PlanFixture) -> None:
778:def test_build_monitor_hint_references_status(plan_fixture: PlanFixture) -> None:
785:def test_format_duration_hint_uses_human_readable_ranges() -> None:
799:def test_emit_phase_notice_writes_to_stderr_only(capsys: pytest.CaptureFixture[str]) -> None:
810:def test_emit_phase_notice_ignores_non_phase_commands(capsys: pytest.CaptureFixture[str]) -> None:
820:def test_workflow_mock_end_to_end(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
907:def test_workflow_light_robustness_single_pass(
956:def test_cli_registers_prep_command() -> None:
967:def test_light_critique_routes_to_revise(
982:def test_light_revise_routes_to_finalize(
998:def test_standard_revise_routes_to_critique_and_clears_last_gate(plan_fixture: PlanFixture) -> None:
1014:def test_handle_plan_stores_nonblocking_structure_warnings(plan_fixture: PlanFixture, monkeypatch: pytest.MonkeyPatch) -> None:
1047:def test_handle_plan_rejects_zero_step_structure_error(plan_fixture: PlanFixture, monkeypatch: pytest.MonkeyPatch) -> None:
[rerun: b4]
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"import\\|from\" /Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py | head -50"
}
```

> TOOL

tool_result Bash
```
1:from __future__ import annotations
3:import json
4:import subprocess
5:import sys
6:import time
7:from argparse import Namespace
8:from dataclasses import dataclass
9:from datetime import datetime, timedelta, timezone
10:from pathlib import Path
11:from typing import Callable
13:import pytest
15:import megaplan
16:import megaplan.cli
17:import megaplan.execution
18:import megaplan.evaluation
19:import megaplan.handlers
20:import megaplan.cli
21:import megaplan._core
22:import megaplan._core.io as io_module
23:import megaplan.workers
24:from megaplan.evaluation import PLAN_STRUCTURE_REQUIRED_STEP_ISSUE, validate_plan_structure
25:from megaplan._core import (
34:from megaplan.prompts import create_claude_prompt
35:from megaplan.types import STATE_PREPPED
36:from megaplan.workers import WorkerResult, _build_mock_payload
452:    """All robustness levels go directly from planned to critique."""
686:def test_handle_status_distinguishes_lock_file_from_held_lock(plan_fixture: PlanFixture) -> None:
821:    from megaplan.handlers import handle_prep
962:    from megaplan.handlers import handle_prep
1230:    from megaplan._core import load_finalize_snapshot
1267:def test_force_proceed_from_critiqued_writes_override_gate(plan_fixture: PlanFixture) -> None:
1337:def test_replan_from_gated_resets_to_planned(plan_fixture: PlanFixture) -> None:
1445:        signals_assessment="Proceeding after addressing the most important blockers.",
1513:    assert "[Auto-downgraded from PROCEED:" in response["rationale"]
1686:import fcntl
1687:import sys
1688:import time
1689:from pathlib import Path
1909:    assert "[Auto-downgraded from PROCEED:" in response["rationale"]
2057:def test_gate_debt_derived_from_flag_resolutions(
2138:    from megaplan.flags import update_flags_after_critique
2148:    from megaplan.flags import update_flags_after_critique
2168:    from megaplan.flags import update_flags_after_critique
2187:    from megaplan.flags import update_flags_after_critique
2208:    from megaplan.flags import update_flags_after_critique
2224:def test_update_flags_after_critique_severity_from_hint(plan_fixture: PlanFixture) -> None:
2226:    from megaplan.flags import update_flags_after_critique
2245:    from megaplan.flags import update_flags_after_critique, update_flags_after_revise  # noqa: F811
2246:    from megaplan._core import save_flag_registry
2379:    # Remove success criteria from meta
[rerun: b5]
```

> AGENT

Perfect. Now let me check if test_verifiability.py exists and look at a few complete test examples:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py",
  "offset": 235,
  "limit": 100
}
```

> TOOL

tool_result Read
```
235	def test_init_sets_last_gate_and_next_step_plan(plan_fixture: PlanFixture) -> None:
236	    state = load_state(plan_fixture.plan_dir)
237	    assert state["current_state"] == megaplan.STATE_INITIALIZED
238	    assert state["last_gate"] == {}
239	
240	
241	def test_init_includes_next_step_runtime(plan_fixture: PlanFixture) -> None:
242	    response = megaplan.handle_init(
243	        plan_fixture.root,
244	        plan_fixture.make_args(name="runtime-test"),
245	    )
246	
247	    assert response["next_step"] == "plan"
248	    assert response["next_step_runtime"]["expected_duration_seconds"]["min"] == 60
249	    assert response["next_step_runtime"]["recommended_next_check_seconds"] == 120
250	    assert "Expected duration:" in response["next_step_runtime"]["duration_hint"]
251	
252	
253	def test_init_response_points_to_next_step_by_robustness(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
254	    root = tmp_path / "root"
255	    project_dir = tmp_path / "project"
256	    root.mkdir()
257	    project_dir.mkdir()
258	    monkeypatch.setattr(
259	        megaplan._core.shutil,
260	        "which",
261	        lambda name: "/usr/bin/mock" if name in {"claude", "codex"} else None,
262	    )
263	    make_args = make_args_factory(project_dir)
264	    standard = megaplan.handle_init(root, make_args(name="standard-plan", robustness="standard"))
265	    light = megaplan.handle_init(root, make_args(name="light-plan", robustness="light"))
266	    robust = megaplan.handle_init(root, make_args(name="robust-plan", robustness="robust"))
267	    assert standard["next_step"] == "plan"
268	    assert light["next_step"] == "plan"
269	    assert robust["next_step"] == "prep"
270	
271	
272	_LEGACY_STATE_MACHINE_CASES = [
273	    ({"current_state": megaplan.STATE_INITIALIZED, "last_gate": {}}, ["plan"]),
274	    ({"current_state": STATE_PREPPED, "last_gate": {}}, ["plan"]),
275	    ({"current_state": megaplan.STATE_PLANNED, "last_gate": {}}, ["critique", "plan", "step"]),
276	    ({"current_state": megaplan.STATE_CRITIQUED, "last_gate": {}}, ["gate", "step"]),
277	    ({"current_state": megaplan.STATE_CRITIQUED, "last_gate": {"recommendation": "ITERATE"}}, ["revise", "step"]),
278	    (
279	        {"current_state": megaplan.STATE_CRITIQUED, "last_gate": {"recommendation": "ESCALATE"}},
280	        ["override add-note", "override force-proceed", "override abort", "step"],
281	    ),
282	    (
283	        {"current_state": megaplan.STATE_CRITIQUED, "last_gate": {"recommendation": "PROCEED", "passed": False}},
284	        ["revise", "override force-proceed", "step"],
285	    ),
286	    ({"current_state": megaplan.STATE_GATED, "last_gate": {}}, ["finalize", "override replan", "step"]),
287	    ({"current_state": megaplan.STATE_FINALIZED, "last_gate": {}}, ["execute", "override replan", "step"]),
288	]
289	
290	
291	def test_infer_next_steps_matches_new_state_machine() -> None:
292	    for state, expected in _LEGACY_STATE_MACHINE_CASES:
293	        assert megaplan.infer_next_steps(state) == expected
294	
295	
296	def test_workflow_next_matches_legacy_partial_state_cases() -> None:
297	    for state, expected in _LEGACY_STATE_MACHINE_CASES:
298	        assert workflow_next(state) == expected
299	
300	
301	@pytest.mark.parametrize(
302	    ("state", "expected"),
303	    [
304	        (
305	            {"current_state": megaplan.STATE_INITIALIZED, "last_gate": {}, "config": {"robustness": "light"}},
306	            ["plan"],
307	        ),
308	        (
309	            {"current_state": megaplan.STATE_CRITIQUED, "last_gate": {}, "config": {"robustness": "light"}},
310	            ["revise", "step"],
311	        ),
312	        (
313	            {
314	                "current_state": megaplan.STATE_CRITIQUED,
315	                "last_gate": {"recommendation": "ESCALATE"},
316	                "config": {"robustness": "light"},
317	            },
318	            ["revise", "step"],
319	        ),
320	        (
321	            {"current_state": megaplan.STATE_EXECUTED, "last_gate": {}, "config": {"robustness": "light"}},
322	            [],
323	        ),
324	    ],
325	)
326	def test_workflow_next_light_robustness_overrides(state: dict[str, object], expected: list[str]) -> None:
327	    assert workflow_next(state) == expected
328	
329	
330	def test_workflow_definition_is_complete_for_standard_flow() -> None:
331	    expected_states = {
332	        megaplan.STATE_INITIALIZED,
333	        megaplan.STATE_PLANNED,
334	        megaplan.STATE_CRITIQUED,
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/tests/test_verifiability.py 2>&1"
}
```

> TOOL

tool_result Bash
```
Exit code 1
ls: /Users/user_c042661f/Documents/megaplan/tests/test_verifiability.py: No such file or directory
[rerun: b6]
```

> AGENT

Perfect. Now let me get more context on the auto.py drive() function and the full integration test pattern:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/auto.py",
  "offset": 140,
  "limit": 150
}
```

> TOOL

tool_result Read
```
140	    """Drive ``plan`` to completion.
141	
142	    Returns a DriverOutcome with a terminal status. The writer is used for
143	    human-readable progress; structured events are collected on the outcome.
144	    """
145	
146	    if on_escalate not in ESCALATE_ACTIONS:
147	        raise ValueError(f"on_escalate must be one of {ESCALATE_ACTIONS}")
148	
149	    events: list[dict[str, Any]] = []
150	    last_state: str | None = None
151	    stall_count = 0
152	    last_phase: str | None = None
153	
154	    def log(msg: str, **fields: Any) -> None:
155	        events.append({"msg": msg, **fields})
156	        writer(f"[auto {plan}] {msg}\n")
157	
158	    for iteration in range(1, max_iterations + 1):
159	        try:
160	            status = _status(plan, cwd=cwd, timeout=status_timeout)
161	        except (RuntimeError, json.JSONDecodeError) as error:
162	            log(f"status lookup failed: {error}")
163	            return DriverOutcome(
164	                status="failed",
165	                plan=plan,
166	                final_state=last_state or "unknown",
167	                iterations=iteration,
168	                reason=str(error),
169	                last_phase=last_phase,
170	                events=events,
171	            )
172	
173	        state = status.get("state", "")
174	        next_step = status.get("next_step")
175	        valid_next = status.get("valid_next") or []
176	
177	        log(
178	            f"iter {iteration} state={state} next={next_step} valid_next={valid_next}",
179	            iteration=iteration,
180	            state=state,
181	            next_step=next_step,
182	            valid_next=valid_next,
183	        )
184	
185	        # Terminal: plan reached a final state (or automation-terminal).
186	        if state in AUTOMATION_TERMINAL_STATES:
187	            if state == STATE_AWAITING_HUMAN:
188	                log("plan awaiting human verification — automation stopping")
189	                return DriverOutcome(
190	                    status="awaiting_human",
191	                    plan=plan,
192	                    final_state=state,
193	                    iterations=iteration,
194	                    reason="plan has criteria requiring human verification",
195	                    last_phase=last_phase,
196	                    events=events,
197	                )
198	            log(f"terminal state reached: {state}")
199	            return DriverOutcome(
200	                status="done" if state == "done" else "aborted",
201	                plan=plan,
202	                final_state=state,
203	                iterations=iteration,
204	                reason=f"plan entered terminal state '{state}'",
205	                last_phase=last_phase,
206	                events=events,
207	            )
208	
209	        # Stall detection: same state for stall_threshold+ iterations.
210	        if state == last_state:
211	            stall_count += 1
212	            if stall_count >= stall_threshold:
213	                log(f"stalled at state={state} for {stall_count} iterations")
214	                return DriverOutcome(
215	                    status="stalled",
216	                    plan=plan,
217	                    final_state=state,
218	                    iterations=iteration,
219	                    reason=(
220	                        f"stalled at '{state}' for {stall_count} iterations — "
221	                        "manual intervention required"
222	                    ),
223	                    last_phase=last_phase,
224	                    events=events,
225	                )
226	        else:
227	            stall_count = 0
228	            last_state = state
229	
230	        # Escalation: no phase to run but overrides are available.
231	        if not next_step:
232	            if _has_valid_next(status, "override force-proceed"):
233	                if on_escalate == "force-proceed":
234	                    log("gate escalated — force-proceeding (per on_escalate=force-proceed)")
235	                    code, out, err = _run_megaplan(
236	                        [
237	                            "override",
238	                            "force-proceed",
239	                            "--plan",
240	                            plan,
241	                            "--reason",
242	                            "megaplan auto: escalate → force-proceed",
243	                        ],
244	                        cwd=cwd,
245	                        timeout=status_timeout,
246	                    )
247	                    if code != 0:
248	                        log(f"force-proceed failed (exit {code}): {err.strip() or out.strip()}")
249	                        return DriverOutcome(
250	                            status="failed",
251	                            plan=plan,
252	                            final_state=state,
253	                            iterations=iteration,
254	                            reason=f"override force-proceed exited {code}",
255	                            last_phase=last_phase,
256	                            events=events,
257	                        )
258	                    continue
259	                if on_escalate == "abort":
260	                    log("gate escalated — aborting (per on_escalate=abort)")
261	                    _run_megaplan(
262	                        [
263	                            "override",
264	                            "abort",
265	                            "--plan",
266	                            plan,
267	                            "--reason",
268	                            "megaplan auto: escalate → abort",
269	                        ],
270	                        cwd=cwd,
271	                        timeout=status_timeout,
272	                    )
273	                    return DriverOutcome(
274	                        status="aborted",
275	                        plan=plan,
276	                        final_state=state,
277	                        iterations=iteration,
278	                        reason="gate escalated and on_escalate=abort",
279	                        last_phase=last_phase,
280	                        events=events,
281	                    )
282	                # on_escalate == "fail"
283	                log("gate escalated — failing (per on_escalate=fail)")
284	                return DriverOutcome(
285	                    status="escalated",
286	                    plan=plan,
287	                    final_state=state,
288	                    iterations=iteration,
289	                    reason="gate escalated and on_escalate=fail — human required",
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py",
  "offset": 820,
  "limit": 100
}
```

> TOOL

tool_result Read
```
820	def test_workflow_mock_end_to_end(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
821	    from megaplan.handlers import handle_prep
822	
823	    plan_fixture = _make_plan_fixture_with_robustness(tmp_path, monkeypatch, robustness="robust")
824	    make_args = plan_fixture.make_args
825	    recorded_steps: list[str] = []
826	    original_run_step = megaplan.workers.run_step_with_worker
827	
828	    def _record(step: str, *args: object, **kwargs: object) -> tuple[WorkerResult, str, str, bool]:
829	        recorded_steps.append(step)
830	        return original_run_step(step, *args, **kwargs)
831	
832	    monkeypatch.setattr(megaplan.workers, "run_step_with_worker", _record)
833	    megaplan.handle_override(
834	        plan_fixture.root,
835	        make_args(plan=plan_fixture.plan_name, override_action="add-note", note="keep changes scoped"),
836	    )
837	    prep = handle_prep(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
838	    plan = megaplan.handle_plan(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
839	    critique1 = megaplan.handle_critique(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
840	    gate1 = megaplan.handle_gate(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
841	    revise = megaplan.handle_revise(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
842	    critique2 = megaplan.handle_critique(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
843	    gate2 = megaplan.handle_gate(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
844	    finalize = megaplan.handle_finalize(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
845	    finalized_tracking = read_json(plan_fixture.plan_dir / "finalize.json")
846	    final_md_after_finalize = (plan_fixture.plan_dir / "final.md").read_text(encoding="utf-8")
847	    execute = megaplan.handle_execute(
848	        plan_fixture.root,
849	        make_args(plan=plan_fixture.plan_name, confirm_destructive=True, user_approved=True),
850	    )
851	    finalized_after_execute = read_json(plan_fixture.plan_dir / "finalize.json")
852	    final_md_after_execute = (plan_fixture.plan_dir / "final.md").read_text(encoding="utf-8")
853	    review = megaplan.handle_review(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
854	    finalized_after_review = read_json(plan_fixture.plan_dir / "finalize.json")
855	    final_md_after_review = (plan_fixture.plan_dir / "final.md").read_text(encoding="utf-8")
856	    plan_meta = read_json(plan_fixture.plan_dir / "plan_v1.meta.json")
857	    revise_meta = read_json(plan_fixture.plan_dir / "plan_v2.meta.json")
858	    state = load_state(plan_fixture.plan_dir)
859	
860	    assert prep["state"] == STATE_PREPPED
861	    assert prep["next_step"] == "plan"
862	    assert plan["state"] == megaplan.STATE_PLANNED
863	    assert plan["next_step"] == "critique"
864	    assert critique1["state"] == megaplan.STATE_CRITIQUED
865	    assert gate1["recommendation"] == "ITERATE"
866	    assert revise["state"] == megaplan.STATE_PLANNED
867	    assert revise["next_step"] == "critique"
868	    assert critique2["iteration"] == 2
869	    assert gate2["state"] == megaplan.STATE_GATED
870	    assert gate2["recommendation"] == "PROCEED"
871	    assert finalize["state"] == megaplan.STATE_FINALIZED
872	    assert plan_meta["structure_warnings"] == []
873	    assert revise_meta["structure_warnings"] == []
874	    assert (plan_fixture.plan_dir / "final.md").exists()
875	    assert (plan_fixture.plan_dir / "finalize.json").exists()
876	    assert (plan_fixture.plan_dir / "prep.json").exists()
877	    assert finalized_tracking["tasks"][0]["status"] == "pending"
878	    assert "# Execution Checklist" in final_md_after_finalize
879	    assert execute["state"] == megaplan.STATE_EXECUTED
880	    assert all(task["status"] == "done" for task in finalized_after_execute["tasks"])
881	    assert all(task["executor_notes"] for task in finalized_after_execute["tasks"])
882	    assert "Executor notes:" in final_md_after_execute
883	    assert review["state"] == megaplan.STATE_DONE
884	    assert all(task["reviewer_verdict"] for task in finalized_after_review["tasks"])
885	    assert all(check["verdict"] for check in finalized_after_review["sense_checks"])
886	    assert "Reviewer verdict:" in final_md_after_review
887	    assert "Verdict:" in final_md_after_review
888	    execute_entry = next(entry for entry in state["history"] if entry["step"] == "execute")
889	    review_entry = next(entry for entry in state["history"] if entry["step"] == "review")
890	    assert execute_entry["finalize_hash"].startswith("sha256:")
891	    assert review_entry["finalize_hash"].startswith("sha256:")
892	    assert recorded_steps == [
893	        "prep",
894	        "plan",
895	        "critique",
896	        "gate",
897	        "revise",
898	        "critique",
899	        "gate",
900	        "finalize",
901	        "execute",
902	        "review",
903	    ]
904	    assert (plan_fixture.project_dir / "IMPLEMENTED_BY_MEGAPLAN.txt").exists()
905	
906	
907	def test_workflow_light_robustness_single_pass(
908	    tmp_path: Path,
909	    monkeypatch: pytest.MonkeyPatch,
910	) -> None:
911	    plan_fixture = _make_plan_fixture_with_robustness(tmp_path, monkeypatch, robustness="light")
912	    make_args = plan_fixture.make_args
913	    recorded_steps: list[str] = []
914	    original_run_step = megaplan.workers.run_step_with_worker
915	
916	    def _record(step: str, *args: object, **kwargs: object) -> tuple[WorkerResult, str, str, bool]:
917	        recorded_steps.append(step)
918	        return original_run_step(step, *args, **kwargs)
919
```

> AGENT

Excellent! Now I have all the information needed. Let me compile a comprehensive report:

## Comprehensive Codebase Analysis for Testing

### **Full Contents: capabilities.py**

```python
"""Closed capability registry and worker discovery for verifiability contracts."""

from __future__ import annotations

from typing import Any

from megaplan.types import DEFAULT_AGENT_ROUTING

CONTAINER_CAPABILITIES: frozenset[str] = frozenset({
    "run_shell",
    "read_files",
    "run_tests",
    "parse_diff",
    "read_build_output",
    "run_linter",
})

HUMAN_CAPABILITIES: frozenset[str] = frozenset({
    "drive_browser",
    "inspect_runtime_ui",
    "observe_runtime_logs",
    "subjective_judgment",
    "verify_physical_device",
})

ALL_CAPABILITIES: frozenset[str] = CONTAINER_CAPABILITIES | HUMAN_CAPABILITIES

DEFAULT_CONTAINER_CAPABILITIES: frozenset[str] = CONTAINER_CAPABILITIES
DEFAULT_HUMAN_CAPABILITIES: frozenset[str] = HUMAN_CAPABILITIES


def validate_capabilities(caps: list[str] | set[str]) -> list[str]:
    """Return unknown capability strings not in the closed registry."""
    return [c for c in caps if c not in ALL_CAPABILITIES]


def get_worker_capabilities(state: dict[str, Any]) -> dict[str, set[str]]:
    """Build worker-name → capabilities mapping from state config.

    Falls back to DEFAULT_CONTAINER_CAPABILITIES for agents listed in
    DEFAULT_AGENT_ROUTING that have no explicit config.
    """
    config = state.get("config", {})
    workers_cfg: dict[str, Any] = config.get("workers", {})

    result: dict[str, set[str]] = {}

    if workers_cfg:
        for name, wcfg in workers_cfg.items():
            verifies = wcfg.get("verifies", [])
            result[name] = set(verifies)
    else:
        seen_agents = set(DEFAULT_AGENT_ROUTING.values())
        for agent in seen_agents:
            result[agent] = set(DEFAULT_CONTAINER_CAPABILITIES)

    return result


def union_verifies(state: dict[str, Any]) -> set[str]:
    """Return the union of all workers' verifies sets."""
    caps = get_worker_capabilities(state)
    result: set[str] = set()
    for v in caps.values():
        result |= v
    return result
```

### **Full Contents: verifiability.py**

```python
"""Verifiability audit — pure-Python capability matching for success criteria."""

from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from typing import Any

from megaplan.capabilities import ALL_CAPABILITIES, HUMAN_CAPABILITIES


@dataclass
class CriterionAudit:
    criterion_idx: int
    verdict: str  # "machine_verifiable" | "human_only" | "unverifiable_no_worker"
    rationale: str
    missing_caps: list[str] = field(default_factory=list)


def audit_criteria(
    criteria: list[dict[str, Any]],
    worker_caps: dict[str, set[str]],
) -> list[CriterionAudit]:
    """For each criterion, check requires ⊆ union of all worker verifies sets.

    Returns a CriterionAudit per criterion with verdict:
      - machine_verifiable: all required caps covered by at least one worker
      - human_only: all required caps exist in registry but some need human workers
      - unverifiable_no_worker: some required caps not satisfiable by any known worker
    """
    all_worker_caps = set()
    for caps in worker_caps.values():
        all_worker_caps |= caps

    results: list[CriterionAudit] = []
    for idx, criterion in enumerate(criteria):
        requires = set(criterion.get("requires", []))
        if not requires:
            results.append(CriterionAudit(
                criterion_idx=idx,
                verdict="machine_verifiable",
                rationale="No capabilities required (empty requires).",
            ))
            continue

        missing_from_workers = requires - all_worker_caps
        if not missing_from_workers:
            results.append(CriterionAudit(
                criterion_idx=idx,
                verdict="machine_verifiable",
                rationale="All required capabilities covered by configured workers.",
            ))
        elif missing_from_workers <= HUMAN_CAPABILITIES:
            results.append(CriterionAudit(
                criterion_idx=idx,
                verdict="human_only",
                rationale="Some required capabilities need human verification.",
                missing_caps=sorted(missing_from_workers),
            ))
        else:
            truly_unknown = missing_from_workers - HUMAN_CAPABILITIES
            results.append(CriterionAudit(
                criterion_idx=idx,
                verdict="unverifiable_no_worker",
                rationale="Required capabilities not satisfiable by any known worker.",
                missing_caps=sorted(missing_from_workers),
            ))

    return results


def classify_criteria(
    criteria: list[dict[str, Any]],
    worker_caps: dict[str, set[str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split criteria into (machine_verifiable, human_deferred).

    machine_verifiable includes criteria with verdict machine_verifiable.
    human_deferred includes human_only and unverifiable_no_worker.
    """
    audits = audit_criteria(criteria, worker_caps)
    machine: list[dict[str, Any]] = []
    human: list[dict[str, Any]] = []
    for audit, criterion in zip(audits, criteria):
        if audit.verdict == "machine_verifiable":
            machine.append(criterion)
        else:
            human.append(criterion)
    return machine, human


def validate_requires(
    criteria: list[dict[str, Any]],
    registry: set[str] | frozenset[str] | None = None,
) -> list[str]:
    """Check all requires entries are known capability strings.

    Returns list of issue strings. Flags must criteria with empty requires
    as deprecation warnings.
    """
    if registry is None:
        registry = ALL_CAPABILITIES

    issues: list[str] = []
    for idx, criterion in enumerate(criteria):
        requires = criterion.get("requires", [])
        priority = criterion.get("priority", "")

        if priority == "must" and not requires:
            msg = (
                f"Criterion {idx} ({criterion.get('criterion', '?')}): "
                f"must-priority criterion has empty requires — "
                f"add requires to enable automated verification."
            )
            issues.append(msg)
            warnings.warn(msg, DeprecationWarning, stacklevel=2)

        for cap in requires:
            if cap not in registry:
                issues.append(
                    f"Criterion {idx} ({criterion.get('criterion', '?')}): "
                    f"unknown capability '{cap}' in requires."
                )

    return issues
```

### **Full Contents: types.py**

```python
"""Type definitions, constants, and exceptions for megaplan."""

from __future__ import annotations

from typing import Any, NotRequired, TypedDict


# ---------------------------------------------------------------------------
# States
# ---------------------------------------------------------------------------

STATE_INITIALIZED = "initialized"
STATE_PREPPED = "prepped"
STATE_PLANNED = "planned"
STATE_CRITIQUED = "critiqued"
STATE_GATED = "gated"
STATE_FINALIZED = "finalized"
STATE_EXECUTED = "executed"
STATE_DONE = "done"
STATE_ABORTED = "aborted"
STATE_AWAITING_HUMAN = "awaiting_human_verify"
TERMINAL_STATES = {STATE_DONE, STATE_ABORTED}
AUTOMATION_TERMINAL_STATES = TERMINAL_STATES | {STATE_AWAITING_HUMAN}


# ---------------------------------------------------------------------------
# TypedDicts
# ---------------------------------------------------------------------------

class PlanConfig(TypedDict, total=False):
    project_dir: str
    auto_approve: bool
    robustness: str
    agents: dict[str, str]
    workers: NotRequired[dict[str, Any]]


class PlanMeta(TypedDict, total=False):
    significant_counts: list[int]
    weighted_scores: list[float]
    plan_deltas: list[float | None]
    recurring_critiques: list[str]
    total_cost_usd: float
    overrides: list[dict[str, Any]]
    notes: list[dict[str, Any]]
    user_approved_gate: bool


class SessionInfo(TypedDict, total=False):
    id: str
    mode: str
    created_at: str
    last_used_at: str
    refreshed: bool


class ActiveStep(TypedDict, total=False):
    step: str
    agent: str
    mode: str
    model: str
    run_id: str
    session_id: str
    started_at: str


class PlanVersionRecord(TypedDict, total=False):
    version: int
    file: str
    hash: str
    timestamp: str


class HistoryEntry(TypedDict, total=False):
    step: str
    timestamp: str
    duration_ms: int
    cost_usd: float
    result: str
    session_mode: str
    session_id: str
    agent: str
    output_file: str
    artifact_hash: str
    finalize_hash: str
    raw_output_file: str
    message: str
    flags_count: int
    flags_addressed: list[str]
    recommendation: str
    approval_mode: str
    environment: dict[str, bool]


class ClarificationRecord(TypedDict, total=False):
    refined_idea: str
    intent_summary: str
    questions: list[str]


class LastGateRecord(TypedDict, total=False):
    recommendation: str
    rationale: str
    signals_assessment: str
    warnings: list[str]
    settled_decisions: list["SettledDecision"]
    passed: bool
    preflight_results: dict[str, bool]
    orchestrator_guidance: str


class PlanState(TypedDict):
    name: str
    idea: str
    current_state: str
    iteration: int
    created_at: str
    config: PlanConfig
    sessions: dict[str, SessionInfo]
    plan_versions: list[PlanVersionRecord]
    history: list[HistoryEntry]
    meta: PlanMeta
    last_gate: LastGateRecord
    active_step: NotRequired[ActiveStep]
    clarification: NotRequired[ClarificationRecord]


class _FlagRecordRequired(TypedDict):
    id: str
    concern: str
    category: str
    status: str


class FlagRecord(_FlagRecordRequired, total=False):
    severity_hint: str
    evidence: str
    raised_in: str
    severity: str
    verified: bool
    verified_in: str
    addressed_in: str


class FlagRegistry(TypedDict):
    flags: list[FlagRecord]


class GateCheckResult(TypedDict):
    passed: bool
    criteria_check: dict[str, Any]
    preflight_results: dict[str, bool]
    unresolved_flags: list[FlagRecord]


class SettledDecision(TypedDict, total=False):
    id: str
    decision: str
    rationale: str


class GatePayload(TypedDict):
    recommendation: str
    rationale: str
    signals_assessment: str
    warnings: list[str]
    settled_decisions: list[SettledDecision]


class GateArtifact(TypedDict, total=False):
    passed: bool
    criteria_check: dict[str, Any]
    preflight_results: dict[str, bool]
    unresolved_flags: list[FlagRecord]
    recommendation: str
    rationale: str
    signals_assessment: str
    warnings: list[str]
    settled_decisions: list[SettledDecision]
    override_forced: bool
    orchestrator_guidance: str
    robustness: str
    signals: dict[str, Any]


class GateSignals(TypedDict, total=False):
    robustness: str
    signals: dict[str, Any]
    warnings: list[str]


class StepResponse(TypedDict, total=False):
    success: bool
    step: str
    summary: str
    artifacts: list[str]
    next_step: str | None
    state: str
    auto_approve: bool
    robustness: str
    iteration: int
    plan: str
    plan_dir: str
    questions: list[str]
    verified_flags: list[str]
    open_flags: list[str]
    scope_creep_flags: list[str]
    warnings: list[str]
    files_changed: list[str]
    deviations: list[str]
    user_approved_gate: bool
    issues: list[str]
    valid_next: list[str]
    mode: str
    installed: list[dict[str, Any]]
    config_path: str
    routing: dict[str, str]
    raw_config: dict[str, Any]
    action: str
    key: str
    value: str
    skipped: bool
    file: str
    plans: list[dict[str, Any]]
    recommendation: str
    signals: dict[str, Any]
    rationale: str
    signals_assessment: str
    orchestrator_guidance: str
    passed: bool
    criteria_check: dict[str, Any]
    preflight_results: dict[str, bool]
    unresolved_flags: list[Any]
    error: str
    message: str
    details: dict[str, Any]
    agent_fallback: dict[str, str]


class DebtEntry(TypedDict):
    id: str
    subsystem: str
    concern: str
    flag_ids: list[str]
    plan_ids: list[str]
    occurrence_count: int
    created_at: str
    updated_at: str
    resolved: bool
    resolved_by: str | None
    resolved_at: str | None


class DebtRegistry(TypedDict):
    entries: list[DebtEntry]


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FLAG_BLOCKING_STATUSES = {"open", "disputed", "addressed"}
FLAG_VALID_STATUSES = {
    "open", "addressed", "disputed", "verified",
    "accepted_tradeoff", "gate_disputed",
}
DEBT_ESCALATION_THRESHOLD = 3
MOCK_ENV_VAR = "MEGAPLAN_MOCK_WORKERS"

DEFAULT_AGENT_ROUTING: dict[str, str] = {
    "plan": "claude",
    "prep": "claude",
    "critique": "codex",
    "revise": "claude",
    "gate": "claude",
    "finalize": "claude",
    "execute": "codex",
    "loop_plan": "claude",
    "loop_execute": "codex",
    "review": "codex",
    "tiebreaker_researcher": "codex",
    "tiebreaker_challenger": "codex",
}
KNOWN_AGENTS = ["claude", "codex", "hermes"]
ROBUSTNESS_LEVELS = ("tiny", "light", "standard", "robust", "superrobust")
def parse_agent_spec(spec: str) -> tuple[str, str | None]:
    """Parse 'hermes:model/name' → ('hermes', 'model/name') or 'claude' → ('claude', None)."""
    if ":" in spec:
        agent, model = spec.split(":", 1)
        return agent, model
    return spec, None


SCOPE_CREEP_TERMS = (
    "scope creep",
    "out of scope",
    "beyond the original idea",
    "beyond original idea",
    "beyond user intent",
    "expanded scope",
)

DEFAULTS = {
    "execution.auto_approve": False,
    "execution.robustness": "standard",
    "execution.worker_timeout_seconds": 7200,
    "execution.max_review_rework_cycles": 3,
    "execution.max_robust_review_rework_cycles": 2,
    "execution.max_execute_no_progress": 3,
    "orchestration.max_critique_concurrency": 2,
    "orchestration.mode": "subagent",
}

_SETTABLE_BOOL = {
    "execution.auto_approve",
}

_SETTABLE_ENUM = {
    "execution.robustness": ROBUSTNESS_LEVELS,
}

_SETTABLE_NUMERIC = {
    "execution.worker_timeout_seconds",
    "execution.max_review_rework_cycles",
    "execution.max_robust_review_rework_cycles",
    "execution.max_execute_no_progress",
    "orchestration.max_critique_concurrency",
}


# ---------------------------------------------------------------------------
# Exception
# ---------------------------------------------------------------------------

class CliError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        *,
        valid_next: list[str] | None = None,
        extra: dict[str, Any] | None = None,
        exit_code: int = 1,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.valid_next = valid_next or []
        self.extra = extra or {}
        self.exit_code = exit_code
```

---

### **handlers.py - handle_verify_human (lines 2129-2209)**

```python
def handle_verify_human(root: Path, args: argparse.Namespace) -> StepResponse:
    from megaplan._core import plans_root, resolve_plan_dir
    plan_dir, state = load_plan(root, args.plan)

    if state["current_state"] != STATE_AWAITING_HUMAN:
        raise CliError(
            "wrong_state",
            f"verify-human requires state 'awaiting_human_verify', got '{state['current_state']}'.",
        )

    criterion_ref = args.criterion
    passed = getattr(args, "pass_flag", False)
    failed = getattr(args, "fail_flag", False)
    evidence = args.evidence

    plan_meta = read_json(latest_plan_meta_path(plan_dir, state))
    success_criteria = plan_meta.get("success_criteria", [])

    target_idx: int | None = None
    try:
        idx = int(criterion_ref)
        if 0 <= idx < len(success_criteria):
            target_idx = idx
    except (ValueError, TypeError):
        for i, sc in enumerate(success_criteria):
            if sc.get("criterion", "") == criterion_ref:
                target_idx = i
                break

    if target_idx is None:
        raise CliError("invalid_criterion", f"Criterion not found: {criterion_ref!r}")

    verifications_path = plan_dir / "human_verifications.json"
    verifications: list[dict[str, Any]] = []
    if verifications_path.exists():
        verifications = read_json(verifications_path)
        if not isinstance(verifications, list):
            verifications = []

    verifications.append({
        "criterion_idx": target_idx,
        "criterion": success_criteria[target_idx].get("criterion", ""),
        "verdict": "pass" if passed else "fail",
        "evidence": evidence,
        "timestamp": now_utc(),
    })
    atomic_write_json(verifications_path, verifications)

    verified_idxs = {
        v["criterion_idx"] for v in verifications if v.get("verdict") == "pass"
    }

    from megaplan.capabilities import get_worker_capabilities
    from megaplan.verifiability import classify_criteria

    worker_caps = get_worker_capabilities(state)
    _, human_deferred = classify_criteria(success_criteria, worker_caps)
    deferred_must_idxs = {
        i for i, sc in enumerate(success_criteria)
        if sc in human_deferred and sc.get("priority") == "must"
    }

    all_verified = deferred_must_idxs <= verified_idxs
    if all_verified:
        state["current_state"] = STATE_DONE
        save_state(plan_dir, state)
        summary = "All deferred must criteria verified. Plan transitioned to done."
    else:
        remaining = deferred_must_idxs - verified_idxs
        summary = f"Verification recorded. {len(remaining)} deferred must criteria remaining."

    return {
        "success": True,
        "step": "verify-human",
        "plan": state["name"],
        "state": state["current_state"],
        "summary": summary,
        "criterion_idx": target_idx,
        "verdict": "pass" if passed else "fail",
    }
```

### **handlers.py - _resolve_review_outcome (lines 1562-1614)**

```python
def _resolve_review_outcome(
    review_verdict: str,
    verdict_count: int,
    total_tasks: int,
    check_count: int,
    total_checks: int,
    missing_evidence: list[str],
    robustness: str,
    state: PlanState,
    issues: list[str],
    criteria: list[dict[str, Any]] | None = None,
) -> tuple[str, str, str | None]:
    """Determine review result, next state, and next step.

    Returns (result, next_state, next_step).
    """
    blocked = (
        verdict_count < total_tasks
        or check_count < total_checks
        or bool(missing_evidence)
    )
    if blocked:
        return "blocked", STATE_EXECUTED, "review"

    rework_requested = review_verdict == "needs_rework"
    if rework_requested:
        cap_key = (
            "max_robust_review_rework_cycles"
            if robustness in {"robust", "superrobust"}
            else "max_review_rework_cycles"
        )
        max_review_rework_cycles = get_effective("execution", cap_key)
        prior_rework_count = sum(
            1 for entry in state.get("history", [])
            if entry.get("step") == "review" and entry.get("result") == "needs_rework"
        )
        if prior_rework_count >= max_review_rework_cycles:
            issues.append(
                f"Max review rework cycles ({max_review_rework_cycles}) reached. "
                "Force-proceeding to done despite unresolved review issues."
            )
        else:
            return "needs_rework", STATE_FINALIZED, "execute"

    if criteria:
        has_deferred_must = any(
            c.get("pass") == "deferred_human" and c.get("priority") == "must"
            for c in criteria
        )
        if has_deferred_must:
            return "success", STATE_AWAITING_HUMAN, None

    return "success", STATE_DONE, None
```

---

### **auto.py - drive() function signature and key logic (lines 128-207)**

Key points:
- Returns `DriverOutcome` with status field that can be: "done", "stalled", "escalated", "failed", "aborted", "cap", "awaiting_human"
- `AUTOMATION_TERMINAL_STATES = TERMINAL_STATES | {STATE_AWAITING_HUMAN}` in types.py (line 23)
- When `state == STATE_AWAITING_HUMAN`, returns `DriverOutcome(status="awaiting_human", ...)`
- Checks state against `AUTOMATION_TERMINAL_STATES` to determine if loop should stop
- Handles stall detection, escalation, and phase failures

---

### **test_megaplan.py - Key Testing Patterns**

**Imports & Setup (lines 1-150):**
```python
from argparse import Namespace
import megaplan
import pytest
from megaplan._core import load_plan, ensure_runtime_layout, save_state
from megaplan.types import STATE_PREPPED, STATE_AWAITING_HUMAN, AUTOMATION_TERMINAL_STATES
```

**PlanFixture dataclass (lines 88-132):**
```python
@dataclass
class PlanFixture:
    root: Path
    project_dir: Path
    plan_name: str
    plan_dir: Path
    make_args: Callable[..., Namespace]

# Setup function
def _make_plan_fixture_with_robustness(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    robustness: str,
) -> PlanFixture:
    # Creates .git, mocks worker discovery, enables mock mode
    monkeypatch.setenv(megaplan.MOCK_ENV_VAR, "1")
    response = megaplan.handle_init(root, make_args(robustness=robustness))
    plan_name = response["plan"]
    return PlanFixture(...)
```

**Test Pattern (workflow_mock_end_to_end, lines 820-905):**
- Creates fixture with `_make_plan_fixture_with_robustness(tmp_path, monkeypatch, robustness="robust")`
- Uses `make_args` factory to create Namespace for each handler call
- Calls handlers sequentially: `handle_plan()` → `handle_critique()` → `handle_gate()` → etc.
- Asserts on response fields: `state`, `next_step`, `recommendation`, iteration
- Reads and verifies artifact files: `finalize.json`, `final.md`, `plan_v1.meta.json`, etc.
- Uses `load_state(plan_fixture.plan_dir)` to read plan state from disk

**Schema Tests Pattern (test_schemas.py, lines 33-150):**
- Direct assertions on `SCHEMAS[name]` dict structure
- Validates required fields, nested object types
- Uses Draft7Validator for payload validation
- Tests both strict_schema transformations and payload validity

---

### **test_schemas.py - Existing Schema Tests**

Test imports and helpers:
```python
from jsonschema import Draft7Validator
from megaplan.schemas import SCHEMAS, strict_schema

def _minimal_review_payload() -> dict[str, object]:
    return {
        "review_verdict": "approved",
        "checks": [],
        "pre_check_flags": [],
        # ... all required fields
    }
```

Test pattern examples:
- `test_schema_registry_matches_5_step_workflow()` - checks SCHEMAS keys
- `test_strict_schema_adds_additional_properties_false()` - validates transformation
- `test_critique_schema_flags_have_expected_structure()` - deep assertions on nested schema
- `test_review_schema_accepts_parallel_mode_extensions_in_both_copies()` - validator with Draft7Validator

---

### **Key Files/Paths You'll Reference**

- `/Users/user_c042661f/Documents/megaplan/megaplan/capabilities.py` - registry
- `/Users/user_c042661f/Documents/megaplan/megaplan/verifiability.py` - audit logic
- `/Users/user_c042661f/Documents/megaplan/megaplan/types.py` - constants (STATE_AWAITING_HUMAN, AUTOMATION_TERMINAL_STATES)
- `/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py` - handle_verify_human (line 2129) + handle_audit_verifiability (line 2211)
- `/Users/user_c042661f/Documents/megaplan/megaplan/auto.py` - drive() function, AUTOMATION_TERMINAL_STATES usage
- `/Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py` - integration test patterns (PlanFixture, end-to-end workflows)
- `/Users/user_c042661f/Documents/megaplan/tests/test_schemas.py` - schema validation patterns

**Note:** `tests/test_verifiability.py` does NOT exist yet — you will be creating it.
