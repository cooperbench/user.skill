> DEVELOPER

I need to understand the current state of several files in /Users/user_c042661f/Documents/megaplan for a plan review. Please gather the following information concisely:

1. megaplan/types.py — What states exist (STATE_* constants)? What does FlagRecord look like? What does PlanConfig look like? Line numbers for each.
2. megaplan/schemas.py — Find the gate.json schema, especially the recommendation enum and properties. Line numbers.
3. megaplan/handlers.py — Find `_apply_gate_outcome` and `handle_gate`. What recommendations does _apply_gate_outcome handle? Line numbers. How does handle_gate call _apply_gate_outcome?
4. megaplan/_core/workflow.py — What does the WORKFLOW dict look like? What transitions exist? Line numbers.
5. megaplan/_core/registries.py — Find `_jaccard_similarity` and `_concern_word_set`. Are they private? Line numbers. What do they do?
6. megaplan/prompts/gate.py — Find `_gate_prompt`. What's the structure? Line numbers for the Requirements section and the debt block.
7. megaplan/prompts/critique.py — Find `_critique_context` and `_build_critique_prompt` and `_revise_prompt`. Line numbers.
8. megaplan/tiebreaker.py — What functions/classes exist? Is there a `_run_tiebreaker` function? What does `build_tiebreaker_parser` look like? Line numbers.
9. megaplan/cli.py — How is tiebreaker integrated? Line numbers.
10. megaplan/auto.py — How does the auto runner dispatch handlers? Does it use workflow transitions?

Report file paths, line numbers, and brief descriptions. Be thorough — I need to verify plan accuracy.

> AGENT

I'll gather this information systematically. Let me start by exploring the structure and then reading the specific files.

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan -type f -name \"*.py\" | head -20"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/evals/__init__.py
/Users/user_c042661f/Documents/megaplan/evals/benchmarks/swe_bench.py
/Users/user_c042661f/Documents/megaplan/evals/benchmarks/__init__.py
/Users/user_c042661f/Documents/megaplan/megaplan/review_checks.py
/Users/user_c042661f/Documents/megaplan/megaplan/merge.py
/Users/user_c042661f/Documents/megaplan/megaplan/execution.py
/Users/user_c042661f/Documents/megaplan/megaplan/review_mechanical.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/io.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/phase_runtime.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/__init__.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/workflow.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/registries.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py
/Users/user_c042661f/Documents/megaplan/megaplan/chain.py
/Users/user_c042661f/Documents/megaplan/megaplan/execution_timeout.py
/Users/user_c042661f/Documents/megaplan/megaplan/flags.py
/Users/user_c042661f/Documents/megaplan/megaplan/checks.py
/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py
/Users/user_c042661f/Documents/megaplan/megaplan/tiebreaker.py
/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py
[rerun: b1]
```

> AGENT

Now let me read the key files:

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
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/schemas.py"
}
```

> TOOL

tool_result Read
```
1	"""JSON schema definitions for megaplan step outputs."""
2	
3	from __future__ import annotations
4	
5	from typing import Any
6	
7	
8	SCHEMAS: dict[str, dict[str, Any]] = {
9	    "plan.json": {
10	        "type": "object",
11	        "properties": {
12	            "plan": {"type": "string"},
13	            "questions": {"type": "array", "items": {"type": "string"}},
14	            "success_criteria": {
15	                "type": "array",
16	                "items": {
17	                    "type": "object",
18	                    "properties": {
19	                        "criterion": {"type": "string"},
20	                        "priority": {"type": "string", "enum": ["must", "should", "info"]},
21	                        "requires": {"type": "array", "items": {"type": "string"}, "default": []},
22	                    },
23	                    "required": ["criterion", "priority"],
24	                },
25	            },
26	            "assumptions": {"type": "array", "items": {"type": "string"}},
27	        },
28	        "required": ["plan", "questions", "success_criteria", "assumptions"],
29	    },
30	    "prep.json": {
31	        "type": "object",
32	        "properties": {
33	            "skip": {"type": "boolean"},
34	            "task_summary": {"type": "string"},
35	            "key_evidence": {
36	                "type": "array",
37	                "items": {
38	                    "type": "object",
39	                    "properties": {
40	                        "point": {"type": "string"},
41	                        "source": {"type": "string"},
42	                        "relevance": {"type": "string", "enum": ["high", "medium", "low"]},
43	                    },
44	                    "required": ["point", "source", "relevance"],
45	                },
46	            },
47	            "relevant_code": {
48	                "type": "array",
49	                "items": {
50	                    "type": "object",
51	                    "properties": {
52	                        "file_path": {"type": "string"},
53	                        "why": {"type": "string"},
54	                        "functions": {"type": "array", "items": {"type": "string"}},
55	                    },
56	                    "required": ["file_path", "why", "functions"],
57	                },
58	            },
59	            "test_expectations": {
60	                "type": "array",
61	                "items": {
62	                    "type": "object",
63	                    "properties": {
64	                        "test_id": {"type": "string"},
65	                        "what_it_checks": {"type": "string"},
66	                        "status": {"type": "string", "enum": ["fail_to_pass", "pass_to_pass"]},
67	                    },
68	                    "required": ["test_id", "what_it_checks", "status"],
69	                },
70	            },
71	            "constraints": {"type": "array", "items": {"type": "string"}},
72	            "suggested_approach": {"type": "string"},
73	        },
74	        "required": [
75	            "skip",
76	            "task_summary",
77	            "key_evidence",
78	            "relevant_code",
79	            "test_expectations",
80	            "constraints",
81	            "suggested_approach",
82	        ],
83	    },
84	    "revise.json": {
85	        "type": "object",
86	        "properties": {
87	            "plan": {"type": "string"},
88	            "changes_summary": {"type": "string"},
89	            "flags_addressed": {"type": "array", "items": {"type": "string"}},
90	            "assumptions": {"type": "array", "items": {"type": "string"}},
91	            "success_criteria": {
92	                "type": "array",
93	                "items": {
94	                    "type": "object",
95	                    "properties": {
96	                        "criterion": {"type": "string"},
97	                        "priority": {"type": "string", "enum": ["must", "should", "info"]},
98	                        "requires": {"type": "array", "items": {"type": "string"}, "default": []},
99	                    },
100	                    "required": ["criterion", "priority"],
101	                },
102	            },
103	            "questions": {"type": "array", "items": {"type": "string"}},
104	        },
105	        "required": [
106	            "plan",
107	            "changes_summary",
108	            "flags_addressed",
109	            "assumptions",
110	            "success_criteria",
111	            "questions",
112	        ],
113	    },
114	    "gate.json": {
115	        "type": "object",
116	        "properties": {
117	            "recommendation": {
118	                "type": "string",
119	                "enum": ["PROCEED", "ITERATE", "ESCALATE"],
120	            },
121	            "rationale": {"type": "string"},
122	            "signals_assessment": {"type": "string"},
123	            "warnings": {"type": "array", "items": {"type": "string"}},
124	            "settled_decisions": {
125	                "type": "array",
126	                "items": {
127	                    "type": "object",
128	                    "properties": {
129	                        "id": {"type": "string"},
130	                        "decision": {"type": "string"},
131	                        "rationale": {"type": "string"},
132	                    },
133	                    "required": ["id", "decision", "rationale"],
134	                },
135	            },
136	            "flag_resolutions": {
137	                "type": "array",
138	                "items": {
139	                    "type": "object",
140	                    "properties": {
141	                        "flag_id": {"type": "string"},
142	                        "action": {"type": "string", "enum": ["dispute", "accept_tradeoff"]},
143	                        "evidence": {"type": "string"},
144	                        "rationale": {"type": "string"},
145	                    },
146	                    "required": ["flag_id", "action", "evidence", "rationale"],
147	                },
148	            },
149	            "accepted_tradeoffs": {
150	                "type": "array",
151	                "items": {
152	                    "type": "object",
153	                    "properties": {
154	                        "flag_id": {"type": "string"},
155	                        "concern": {"type": "string"},
156	                        "subsystem": {"type": "string"},
157	                        "rationale": {"type": "string"},
158	                    },
159	                    "required": ["flag_id", "concern", "subsystem", "rationale"],
160	                },
161	            },
162	        },
163	        "required": [
164	            "recommendation",
165	            "rationale",
166	            "signals_assessment",
167	            "warnings",
168	            "settled_decisions",
169	            "flag_resolutions",
170	            "accepted_tradeoffs",
171	        ],
172	    },
173	    "critique.json": {
174	        "type": "object",
175	        "properties": {
176	            "checks": {
177	                "type": "array",
178	                "items": {
179	                    "type": "object",
180	                    "properties": {
181	                        "id": {"type": "string"},
182	                        "question": {"type": "string"},
183	                        "findings": {
184	                            "type": "array",
185	                            "items": {
186	                                "type": "object",
187	                                "properties": {
188	                                    "detail": {"type": "string"},
189	                                    "flagged": {"type": "boolean"},
190	                                },
191	                                "required": ["detail", "flagged"],
192	                            },
193	                        },
194	                    },
195	                    "required": ["id", "question", "findings"],
196	                },
197	            },
198	            "flags": {
199	                "type": "array",
200	                "items": {
201	                    "type": "object",
202	                    "properties": {
203	                        "id": {"type": "string"},
204	                        "concern": {"type": "string"},
205	                        "category": {
206	                            "type": "string",
207	                            "enum": [
208	                                "correctness",
209	                                "security",
210	                                "completeness",
211	                                "performance",
212	                                "maintainability",
213	                                "other",
214	                                "verifiability",
215	                            ],
216	                        },
217	                        "severity_hint": {
218	                            "type": "string",
219	                            "enum": ["likely-significant", "likely-minor", "uncertain"],
220	                        },
221	                        "evidence": {"type": "string"},
222	                    },
223	                    "required": ["id", "concern", "category", "severity_hint", "evidence"],
224	                },
225	            },
226	            "verified_flag_ids": {"type": "array", "items": {"type": "string"}},
227	            "disputed_flag_ids": {"type": "array", "items": {"type": "string"}},
228	        },
229	        "required": ["checks", "flags", "verified_flag_ids", "disputed_flag_ids"],
230	    },
231	"finalize.json": {
232	        "type": "object",
233	        "properties": {
234	            "tasks": {
235	                "type": "array",
236	                "items": {
237	                    "type": "object",
238	                    "properties": {
239	                        "id": {"type": "string"},
240	                        "description": {"type": "string"},
241	                        "depends_on": {"type": "array", "items": {"type": "string"}},
242	                        "status": {"type": "string", "enum": ["pending", "done", "skipped"]},
243	                        "executor_notes": {"type": "string"},
244	                        "files_changed": {"type": "array", "items": {"type": "string"}},
245	                        "commands_run": {"type": "array", "items": {"type": "string"}},
246	                        "evidence_files": {"type": "array", "items": {"type": "string"}},
247	                        "reviewer_verdict": {"type": "string"},
248	                    },
249	                    "required": [
250	                        "id",
251	                        "description",
252	                        "depends_on",
253	                        "status",
254	                        "executor_notes",
255	                        "files_changed",
256	                        "commands_run",
257	                        "evidence_files",
258	                        "reviewer_verdict",
259	                    ],
260	                },
261	            },
262	            "watch_items": {"type": "array", "items": {"type": "string"}},
263	            "sense_checks": {
264	                "type": "array",
265	                "items": {
266	                    "type": "object",
267	                    "properties": {
268	                        "id": {"type": "string"},
269	                        "task_id": {"type": "string"},
270	                        "question": {"type": "string"},
271	                        "executor_note": {"type": "string"},
272	                        "verdict": {"type": "string"},
273	                    },
274	                    "required": ["id", "task_id", "question", "executor_note", "verdict"],
275	                },
276	            },
277	            "meta_commentary": {"type": "string"},
278	            "validation": {
279	                "type": "object",
280	                "properties": {
281	                    "plan_steps_covered": {
282	                        "type": "array",
283	                        "items": {
284	                            "type": "object",
285	                            "properties": {
286	                                "plan_step_summary": {"type": "string"},
287	                                "finalize_task_ids": {
288	                                    "type": "array",
289	                                    "items": {"type": "string"},
290	                                },
291	                            },
292	                            "required": ["plan_step_summary", "finalize_task_ids"],
293	                        },
294	                    },
295	                    "orphan_tasks": {
296	                        "type": "array",
297	                        "items": {"type": "string"},
298	                    },
299	                    "completeness_notes": {"type": "string"},
300	                    "coverage_complete": {"type": "boolean"},
301	                },
302	                "required": [
303	                    "plan_steps_covered",
304	                    "orphan_tasks",
305	                    "completeness_notes",
306	                    "coverage_complete",
307	                ],
308	            },
309	            "baseline_test_failures": {
310	                "type": ["array", "null"],
311	                "items": {"type": "string"},
312	            },
313	            "baseline_test_command": {"type": ["string", "null"]},
314	            "baseline_test_note": {"type": "string"},
315	        },
316	        "required": ["tasks", "watch_items", "sense_checks", "meta_commentary", "validation"],
317	    },
318	    "execution.json": {
319	        "type": "object",
320	        "properties": {
321	            "output": {"type": "string"},
322	            "files_changed": {"type": "array", "items": {"type": "string"}},
323	            "commands_run": {"type": "array", "items": {"type": "string"}},
324	            "deviations": {"type": "array", "items": {"type": "string"}},
325	            "task_updates": {
326	                "type": "array",
327	                "items": {
328	                    "type": "object",
329	                    "properties": {
330	                        "task_id": {"type": "string"},
331	                        "status": {"type": "string", "enum": ["done", "skipped"]},
332	                        "executor_notes": {"type": "string"},
333	                        "files_changed": {"type": "array", "items": {"type": "string"}},
334	                        "commands_run": {"type": "array", "items": {"type": "string"}},
335	                    },
336	                    "required": ["task_id", "status", "executor_notes", "files_changed", "commands_run"],
337	                },
338	            },
339	            "sense_check_acknowledgments": {
340	                "type": "array",
341	                "items": {
342	                    "type": "object",
343	                    "properties": {
344	                        "sense_check_id": {"type": "string"},
345	                        "executor_note": {"type": "string"},
346	                    },
347	                    "required": ["sense_check_id", "executor_note"],
348	                },
349	            },
350	        },
351	        "required": ["output", "files_changed", "commands_run", "deviations", "task_updates", "sense_check_acknowledgments"],
352	    },
353	    "loop_plan.json": {
354	        "type": "object",
355	        "properties": {
356	            "spec_updates": {
357	                "type": "object",
358	                "additionalProperties": True,
359	            },
360	            "next_action": {"type": "string"},
361	            "reasoning": {"type": "string"},
362	        },
363	        "required": ["spec_updates", "next_action", "reasoning"],
364	    },
365	    "tiebreaker_researcher.json": {
366	        "type": "object",
367	        "properties": {
368	            "question": {"type": "string"},
369	            "evidence": {
370	                "type": "array",
371	                "items": {
372	                    "type": "object",
373	                    "properties": {
374	                        "claim": {"type": "string"},
375	                        "evidence_type": {
376	                            "type": "string",
377	                            "enum": ["code", "measurement", "pattern", "doc"],
378	                        },
379	                        "file_paths": {"type": "array", "items": {"type": "string"}},
380	                        "quote": {"type": "string"},
381	                    },
382	                    "required": ["claim", "evidence_type", "file_paths", "quote"],
383	                },
384	            },
385	            "options": {
386	                "type": "array",
387	                "items": {
388	                    "type": "object",
389	                    "properties": {
390	                        "name": {"type": "string"},
391	                        "description": {"type": "string"},
392	                        "assumptions": {"type": "array", "items": {"type": "string"}},
393	                        "costs": {"type": "array", "items": {"type": "string"}},
394	                    },
395	                    "required": ["name", "description", "assumptions", "costs"],
396	                },
397	            },
398	            "preliminary_pick": {
399	                "type": "object",
400	                "properties": {
401	                    "option_name": {"type": "string"},
402	                    "rationale": {"type": "string"},
403	                    "what_im_least_sure_about": {"type": "string"},
404	                },
405	                "required": ["option_name", "rationale", "what_im_least_sure_about"],
406	            },
407	        },
408	        "required": ["question", "evidence", "options", "preliminary_pick"],
409	    },
410	    "tiebreaker_challenger.json": {
411	        "type": "object",
412	        "properties": {
413	            "measurements_vs_assumptions": {"type": "string"},
414	            "missing_options": {
415	                "type": "array",
416	                "items": {
417	                    "type": "object",
418	                    "properties": {
419	                        "name": {"type": "string"},
420	                        "description": {"type": "string"},
421	                        "why_missed": {"type": "string"},
422	                    },
423	                    "required": ["name", "description", "why_missed"],
424	                },
425	            },
426	            "hard_cases": {
427	                "type": "array",
428	                "items": {
429	                    "type": "object",
430	                    "properties": {
431	                        "scenario": {"type": "string"},
432	                        "which_option_breaks": {"type": "string"},
433	                        "severity": {"type": "string"},
434	                    },
435	                    "required": ["scenario", "which_option_breaks", "severity"],
436	                },
437	            },
438	            "reframings": {"type": "array", "items": {"type": "string"}},
439	            "aging_analysis": {"type": "string"},
440	            "counter_recommendation": {
441	                "type": "object",
442	                "properties": {
443	                    "option_name": {"type": "string"},
444	                    "rationale": {"type": "string"},
445	                    "agrees_with_researcher": {"type": "boolean"},
446	                },
447	                "required": ["option_name", "rationale", "agrees_with_researcher"],
448	            },
449	        },
450	        "required": [
451	            "measurements_vs_assumptions",
452	            "missing_options",
453	            "hard_cases",
454	            "reframings",
455	            "aging_analysis",
456	            "counter_recommendation",
457	        ],
458	    },
459	    "loop_execute.json": {
460	        "type": "object",
461	        "properties": {
462	            "diagnosis": {"type": "string"},
463	            "fix_description": {"type": "string"},
464	            "files_to_change": {"type": "array", "items": {"type": "string"}},
465	            "confidence": {"type": "string"},
466	            "outcome": {"type": "string"},
467	            "should_pause": {"type": "boolean"},
468	        },
469	        "required": ["diagnosis", "fix_description", "files_to_change", "confidence", "outcome", "should_pause"],
470	    },
471	    "review.json": {
472	        "type": "object",
473	        "properties": {
474	            "review_verdict": {"type": "string", "enum": ["approved", "needs_rework"]},
475	            "checks": {
476	                "type": "array",
477	                "items": {
478	                    "type": "object",
479	                    "properties": {
480	                        "id": {"type": "string"},
481	                        "question": {"type": "string"},
482	                        "guidance": {"type": "string"},
483	                        "findings": {
484	                            "type": "array",
485	                            "items": {
486	                                "type": "object",
487	                                "properties": {
488	                                    "detail": {"type": "string"},
489	                                    "flagged": {"type": "boolean"},
490	                                    "status": {"type": "string"},
491	                                    "evidence_file": {"type": "string"},
492	                                },
493	                                "required": ["detail", "flagged", "status", "evidence_file"],
494	                            },
495	                        },
496	                        "prior_findings": {
497	                            "type": "array",
498	                            "items": {
499	                                "type": "object",
500	                                "properties": {
501	                                    "detail": {"type": "string"},
502	                                    "flagged": {"type": "boolean"},
503	                                    "status": {"type": "string"},
504	                                },
505	                                "required": ["detail", "flagged", "status"],
506	                            },
507	                        },
508	                    },
509	                    "required": ["id", "question", "guidance", "findings", "prior_findings"],
510	                },
511	            },
512	            "pre_check_flags": {
513	                "type": "array",
514	                "items": {
515	                    "type": "object",
516	                    "properties": {
517	                        "id": {"type": "string"},
518	                        "check": {"type": "string"},
519	                        "detail": {"type": "string"},
520	                        "severity": {"type": "string"},
521	                        "evidence_file": {"type": "string"},
522	                    },
523	                    "required": ["id", "check", "detail", "severity", "evidence_file"],
524	                },
525	            },
526	            "verified_flag_ids": {"type": "array", "items": {"type": "string"}},
527	            "disputed_flag_ids": {"type": "array", "items": {"type": "string"}},
528	            "criteria": {
529	                "type": "array",
530	                "items": {
531	                    "type": "object",
532	                    "properties": {
533	                        "name": {"type": "string"},
534	                        "priority": {"type": "string", "enum": ["must", "should", "info"]},
535	                        "pass": {"type": "string", "enum": ["pass", "fail", "waived", "deferred_human"]},
536	                        "evidence": {"type": "string"},
537	                    },
538	                    "required": ["name", "priority", "pass", "evidence"],
539	                },
540	            },
541	            "issues": {"type": "array", "items": {"type": "string"}},
542	            "rework_items": {
543	                "type": "array",
544	                "items": {
545	                    "type": "object",
546	                    "properties": {
547	                        "task_id": {"type": "string"},
548	                        "issue": {"type": "string"},
549	                        "expected": {"type": "string"},
550	                        "actual": {"type": "string"},
551	                        "evidence_file": {"type": "string"},
552	                        "flag_id": {"type": ["string", "null"]},
553	                        "source": {"type": ["string", "null"]},
554	                    },
555	                    "required": ["task_id", "issue", "expected", "actual", "evidence_file", "flag_id", "source"],
556	                },
557	            },
558	            "summary": {"type": "string"},
559	            "task_verdicts": {
560	                "type": "array",
561	                "items": {
562	                    "type": "object",
563	                    "properties": {
564	                        "task_id": {"type": "string"},
565	                        "reviewer_verdict": {"type": "string"},
566	                        "evidence_files": {"type": "array", "items": {"type": "string"}},
567	                    },
568	                    "required": ["task_id", "reviewer_verdict", "evidence_files"],
569	                },
570	            },
571	            "sense_check_verdicts": {
572	                "type": "array",
573	                "items": {
574	                    "type": "object",
575	                    "properties": {
576	                        "sense_check_id": {"type": "string"},
577	                        "verdict": {"type": "string"},
578	                    },
579	                    "required": ["sense_check_id", "verdict"],
580	                },
581	            },
582	        },
583	        "required": [
584	            "review_verdict",
585	            "checks",
586	            "pre_check_flags",
587	            "verified_flag_ids",
588	            "disputed_flag_ids",
589	            "criteria",
590	            "issues",
591	            "rework_items",
592	            "summary",
593	            "task_verdicts",
594	            "sense_check_verdicts",
595	        ],
596	    },
597	}
598	
599	
600	def _preserve_explicit_required(path: tuple[str, ...]) -> bool:
601	    # `review.rework_items[]` uses explicit required fields because OpenAI
602	    # structured outputs require every property key to appear in `required`.
603	    return path[-3:] == ("properties", "rework_items", "items")
604	
605	
606	def strict_schema(schema: Any, _path: tuple[str, ...] = ()) -> Any:
607	    if isinstance(schema, dict):
608	        updated = {key: strict_schema(value, _path + (key,)) for key, value in schema.items()}
609	        if updated.get("type") == "object":
610	            updated.setdefault("additionalProperties", False)
611	            if "properties" in updated and not _preserve_explicit_required(_path):
612	                updated["required"] = list(updated["properties"].keys())
613	        return updated
614	    if isinstance(schema, list):
615	        return [strict_schema(item, _path) for item in schema]
616	    return schema
617
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py"
}
```

> TOOL

tool_result Read
```
File content (26202 tokens) exceeds maximum allowed tokens (10000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
```

> AGENT

Let me read handlers.py in sections:

> TOOL

tool_use Grep
```json
{
  "pattern": "def _apply_gate_outcome|def handle_gate",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "output_mode": "content",
  "context": 5
}
```

> TOOL

tool_result Grep
```
601-        "preflight_results": gate_summary["preflight_results"],
602-        "orchestrator_guidance": gate_summary["orchestrator_guidance"],
603-    }
604-
605-
606:def _apply_gate_outcome(
607-    state: PlanState,
608-    gate_summary: dict[str, Any],
609-    *,
610-    robustness: str,
611-    plan_dir: Path,
--
1111-            },
1112-            history_fields={"flags_addressed": payload["flags_addressed"]},
1113-        )
1114-
1115-
1116:def handle_gate(root: Path, args: argparse.Namespace) -> StepResponse:
1117-    with load_plan_locked(root, args.plan, step="gate") as (plan_dir, state):
1118-        require_state(state, "gate", {STATE_CRITIQUED})
1119-        iteration = state["iteration"]
1120-        gate_signals, signals_filename, signals_artifact = _build_gate_signals_artifact(plan_dir, state, iteration=iteration, root=root)
1121-        resolved = resolve_agent_mode("gate", args)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/workflow.py"
}
```

> TOOL

tool_result Read
```
1	"""State machine — workflow transitions, robustness levels, step validation."""
2	
3	from __future__ import annotations
4	
5	from dataclasses import dataclass
6	from typing import Any
7	
8	from megaplan.types import (
9	    CliError,
10	    PlanState,
11	    ROBUSTNESS_LEVELS,
12	    STATE_ABORTED,
13	    STATE_AWAITING_HUMAN,
14	    STATE_CRITIQUED,
15	    STATE_DONE,
16	    STATE_EXECUTED,
17	    STATE_FINALIZED,
18	    STATE_GATED,
19	    STATE_INITIALIZED,
20	    STATE_PLANNED,
21	    STATE_PREPPED,
22	)
23	
24	
25	@dataclass(frozen=True)
26	class Transition:
27	    next_step: str
28	    next_state: str
29	    condition: str = "always"
30	
31	
32	WORKFLOW: dict[str, list[Transition]] = {
33	    STATE_INITIALIZED: [
34	        Transition("prep", STATE_PREPPED),
35	    ],
36	    STATE_PREPPED: [
37	        Transition("plan", STATE_PLANNED),
38	    ],
39	    STATE_PLANNED: [
40	        Transition("critique", STATE_CRITIQUED),
41	        Transition("plan", STATE_PLANNED),
42	    ],
43	    STATE_CRITIQUED: [
44	        Transition("gate", STATE_GATED, "gate_unset"),
45	        Transition("revise", STATE_PLANNED, "gate_iterate"),
46	        Transition("override add-note", STATE_CRITIQUED, "gate_escalate"),
47	        Transition("override force-proceed", STATE_GATED, "gate_escalate"),
48	        Transition("override abort", STATE_ABORTED, "gate_escalate"),
49	        Transition("revise", STATE_PLANNED, "gate_proceed_blocked"),
50	        Transition("override force-proceed", STATE_GATED, "gate_proceed_blocked"),
51	        Transition("gate", STATE_GATED, "gate_proceed"),
52	    ],
53	    STATE_GATED: [
54	        Transition("finalize", STATE_FINALIZED),
55	        Transition("override replan", STATE_PLANNED),
56	    ],
57	    STATE_FINALIZED: [
58	        Transition("execute", STATE_EXECUTED),
59	        Transition("override replan", STATE_PLANNED),
60	    ],
61	    STATE_EXECUTED: [
62	        # `handle_review()` may also return STATE_FINALIZED on a `needs_rework`
63	        # verdict. That rework loop depends on review payload semantics rather
64	        # than gate_* conditions, so it lives in the handler instead of here
65	        # because `_transition_matches()` only understands gate-based branches.
66	        Transition("review", STATE_DONE),
67	    ],
68	    STATE_AWAITING_HUMAN: [
69	        Transition("verify-human", STATE_DONE),
70	    ],
71	}
72	
73	# Each level's *own* overrides (not inherited).  Levels inherit from the
74	# level below them via _ROBUSTNESS_HIERARCHY so shared transitions are
75	# declared once: robust/superrobust have none, standard keeps the
76	# planned->critique routing documented explicitly, and light skips
77	# prep plus gate/review.
78	_ROBUSTNESS_OVERRIDES: dict[str, dict[str, list[Transition]]] = {
79	    "superrobust": {},
80	    "robust": {},
81	    "standard": {
82	        STATE_INITIALIZED: [
83	            Transition("plan", STATE_PLANNED),
84	        ],
85	    },
86	    "light": {
87	        STATE_INITIALIZED: [
88	            Transition("plan", STATE_PLANNED),
89	        ],
90	        STATE_CRITIQUED: [
91	            Transition("revise", STATE_GATED),
92	        ],
93	        STATE_EXECUTED: [],
94	    },
95	    "tiny": {},
96	}
97	
98	_ROBUSTNESS_WORKFLOW_LEVELS: dict[str, tuple[str, ...]] = {
99	    "superrobust": ("superrobust",),
100	    "robust": ("robust",),
101	    "standard": ("standard",),
102	    "light": ("standard", "light"),
103	    "tiny": ("standard", "light", "tiny"),
104	}
105	
106	_STEP_CONTEXT_STATES = {
107	    STATE_PLANNED,
108	    STATE_CRITIQUED,
109	    STATE_GATED,
110	    STATE_FINALIZED,
111	}
112	
113	
114	# ---------------------------------------------------------------------------
115	# Robustness helpers
116	# ---------------------------------------------------------------------------
117	
118	def configured_robustness(state: PlanState) -> str:
119	    robustness = state["config"].get("robustness", "standard")
120	    if robustness not in ROBUSTNESS_LEVELS:
121	        return "standard"
122	    return robustness
123	
124	
125	def robustness_critique_instruction(robustness: str) -> str:
126	    if robustness == "light":
127	        return "Be pragmatic. Only flag issues that would cause real failures. Ignore style, minor edge cases, and issues the executor will naturally resolve."
128	    return "Use balanced judgment. Flag significant risks, but do not spend flags on minor polish or executor-obvious boilerplate."
129	
130	
131	# ---------------------------------------------------------------------------
132	# Intent / notes block for prompts
133	# ---------------------------------------------------------------------------
134	
135	def intent_and_notes_block(state: PlanState) -> str:
136	    sections = []
137	    clarification = state.get("clarification", {})
138	    if clarification.get("intent_summary"):
139	        sections.append(f"User intent summary:\n{clarification['intent_summary']}")
140	        sections.append(f"Original idea:\n{state['idea']}")
141	    else:
142	        sections.append(f"Idea:\n{state['idea']}")
143	    notes = state["meta"].get("notes", [])
144	    if notes:
145	        notes_text = "\n".join(f"- {note['note']}" for note in notes)
146	        sections.append(f"User notes and answers:\n{notes_text}")
147	    return "\n\n".join(sections)
148	
149	
150	# ---------------------------------------------------------------------------
151	# Transition logic
152	# ---------------------------------------------------------------------------
153	
154	def _normalize_workflow_robustness(robustness: Any) -> str:
155	    if robustness in ROBUSTNESS_LEVELS:
156	        return str(robustness)
157	    return "standard"
158	
159	
160	def _workflow_robustness_from_state(state: PlanState) -> str:
161	    config = state.get("config", {})
162	    if not isinstance(config, dict):
163	        return "standard"
164	    return _normalize_workflow_robustness(config.get("robustness", "standard"))
165	
166	
167	def _workflow_for_robustness(robustness: str) -> dict[str, list[Transition]]:
168	    normalized = _normalize_workflow_robustness(robustness)
169	    merged = dict(WORKFLOW)
170	    for level in _ROBUSTNESS_WORKFLOW_LEVELS.get(normalized, _ROBUSTNESS_WORKFLOW_LEVELS["standard"]):
171	        merged.update(_ROBUSTNESS_OVERRIDES.get(level, {}))
172	    return merged
173	
174	
175	def _transition_matches(state: PlanState, condition: str) -> bool:
176	    if condition == "always":
177	        return True
178	    gate = state.get("last_gate", {})
179	    if not isinstance(gate, dict):
180	        gate = {}
181	    recommendation = gate.get("recommendation")
182	    if condition == "gate_unset":
183	        return not recommendation
184	    if condition == "gate_iterate":
185	        return recommendation == "ITERATE"
186	    if condition == "gate_escalate":
187	        return recommendation == "ESCALATE"
188	    if condition == "gate_proceed_blocked":
189	        return recommendation == "PROCEED" and not gate.get("passed", False)
190	    if condition == "gate_proceed":
191	        return recommendation == "PROCEED" and gate.get("passed", False)
192	    return False
193	
194	
195	def workflow_includes_step(robustness: str, step: str) -> bool:
196	    if step == "step":
197	        return True
198	    workflow = _workflow_for_robustness(robustness)
199	    return any(
200	        transition.next_step == step
201	        for transitions in workflow.values()
202	        for transition in transitions
203	    )
204	
205	
206	def workflow_transition(state: PlanState, step: str) -> Transition | None:
207	    current = state.get("current_state")
208	    if not isinstance(current, str):
209	        return None
210	    workflow = _workflow_for_robustness(_workflow_robustness_from_state(state))
211	    for transition in workflow.get(current, []):
212	        if transition.next_step == step and _transition_matches(state, transition.condition):
213	            return transition
214	    return None
215	
216	
217	def workflow_next(state: PlanState) -> list[str]:
218	    current = state.get("current_state")
219	    if not isinstance(current, str):
220	        return []
221	    workflow = _workflow_for_robustness(_workflow_robustness_from_state(state))
222	    next_steps = [
223	        transition.next_step
224	        for transition in workflow.get(current, [])
225	        if _transition_matches(state, transition.condition)
226	    ]
227	    if current in _STEP_CONTEXT_STATES:
228	        next_steps.append("step")
229	    return next_steps
230	
231	
232	infer_next_steps = workflow_next
233	
234	
235	def require_state(state: PlanState, step: str, allowed: set[str]) -> None:
236	    current = state["current_state"]
237	    if current not in allowed:
238	        raise CliError(
239	            "invalid_transition",
240	            f"Cannot run '{step}' while current state is '{current}'",
241	            valid_next=infer_next_steps(state),
242	            extra={"current_state": current},
243	        )
244
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/registries.py",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	"""Flag and debt registry operations."""
2	
3	from __future__ import annotations
4	
5	import re
6	from pathlib import Path
7	
8	from megaplan.types import (
9	    DEBT_ESCALATION_THRESHOLD,
10	    DebtEntry,
11	    DebtRegistry,
12	    FLAG_BLOCKING_STATUSES,
13	    FlagRecord,
14	    FlagRegistry,
15	    SCOPE_CREEP_TERMS,
16	)
17	
18	from .io import (
19	    atomic_write_json,
20	    megaplan_root,
21	    normalize_text,
22	    now_utc,
23	    read_json,
24	)
25	
26	
27	# ---------------------------------------------------------------------------
28	# Flag registry
29	# ---------------------------------------------------------------------------
30	
31	def load_flag_registry(plan_dir: Path) -> FlagRegistry:
32	    path = plan_dir / "faults.json"
33	    if path.exists():
34	        return read_json(path)
35	    return {"flags": []}
36	
37	
38	def save_flag_registry(plan_dir: Path, registry: FlagRegistry) -> None:
39	    atomic_write_json(plan_dir / "faults.json", registry)
40	
41	
42	def unresolved_significant_flags(flag_registry: FlagRegistry) -> list[FlagRecord]:
43	    return [
44	        flag
45	        for flag in flag_registry["flags"]
46	        if flag.get("severity") == "significant" and flag["status"] in FLAG_BLOCKING_STATUSES
47	    ]
48	
49	
50	def is_scope_creep_flag(flag: FlagRecord) -> bool:
51	    text = f"{flag['concern']} {flag.get('evidence', '')}".lower()
52	    return any(term in text for term in SCOPE_CREEP_TERMS)
53	
54	
55	def scope_creep_flags(
56	    flag_registry: FlagRegistry,
57	    *,
58	    statuses: set[str] | None = None,
59	) -> list[FlagRecord]:
60	    matches = []
61	    for flag in flag_registry["flags"]:
62	        if statuses is not None and flag["status"] not in statuses:
63	            continue
64	        if is_scope_creep_flag(flag):
65	            matches.append(flag)
66	    return matches
67	
68	
69	# ---------------------------------------------------------------------------
70	# Debt registry
71	# ---------------------------------------------------------------------------
72	
73	def load_debt_registry(root: Path) -> DebtRegistry:
74	    path = megaplan_root(root) / "debt.json"
75	    if path.exists():
76	        return read_json(path)
77	    return {"entries": []}
78	
79	
80	def save_debt_registry(root: Path, registry: DebtRegistry) -> None:
81	    atomic_write_json(megaplan_root(root) / "debt.json", registry)
82	
83	
84	def next_debt_id(registry: DebtRegistry) -> str:
85	    max_id = 0
86	    for entry in registry["entries"]:
87	        match = re.fullmatch(r"DEBT-(\d+)", entry["id"])
88	        if match is None:
89	            continue
90	        max_id = max(max_id, int(match.group(1)))
91	    return f"DEBT-{max_id + 1:03d}"
92	
93	
94	def _normalize_subsystem_tag(value: str) -> str:
95	    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
96	    return normalized or "untagged"
97	
98	
99	def extract_subsystem_tag(concern: str) -> str:
100	    prefix, separator, _ = concern.partition(":")
```

> AGENT

Let me continue searching for the remaining functions:

> TOOL

tool_use Grep
```json
{
  "pattern": "def _jaccard_similarity|def _concern_word_set",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/registries.py",
  "output_mode": "content",
  "context": 10
}
```

> TOOL

tool_result Grep
```
96-    return normalized or "untagged"
97-
98-
99-def extract_subsystem_tag(concern: str) -> str:
100-    prefix, separator, _ = concern.partition(":")
101-    if not separator:
102-        return "untagged"
103-    return _normalize_subsystem_tag(prefix)
104-
105-
106:def _concern_word_set(concern: str) -> set[str]:
107-    return {
108-        token
109-        for token in re.split(r"[^a-z0-9]+", normalize_text(concern))
110-        if token
111-    }
112-
113-
114:def _jaccard_similarity(left: set[str], right: set[str]) -> float:
115-    if not left or not right:
116-        return 0.0
117-    union = left | right
118-    if not union:
119-        return 0.0
120-    return len(left & right) / len(union)
121-
122-
123-def find_matching_debt(registry: DebtRegistry, subsystem: str, concern: str) -> DebtEntry | None:
124-    normalized_subsystem = _normalize_subsystem_tag(subsystem)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/gate.py",
  "limit": 200
}
```

> TOOL

tool_result Read
```
1	"""Gate-phase prompt builders and summaries."""
2	
3	from __future__ import annotations
4	
5	import textwrap
6	from pathlib import Path
7	
8	from megaplan._core import (
9	    configured_robustness,
10	    current_iteration_artifact,
11	    intent_and_notes_block,
12	    json_dump,
13	    latest_plan_meta_path,
14	    latest_plan_path,
15	    load_flag_registry,
16	    read_json,
17	    unresolved_significant_flags,
18	)
19	from megaplan.types import FlagRegistry, PlanState
20	
21	from ._shared import _gate_debt_block
22	
23	
24	def _gate_prompt(state: PlanState, plan_dir: Path, root: Path | None = None) -> str:
25	    project_dir = Path(state["config"]["project_dir"])
26	    latest_plan = latest_plan_path(plan_dir, state).read_text(encoding="utf-8")
27	    latest_meta = read_json(latest_plan_meta_path(plan_dir, state))
28	    gate_signals = read_json(
29	        current_iteration_artifact(plan_dir, "gate_signals", state["iteration"])
30	    )
31	    flag_registry = load_flag_registry(plan_dir)
32	    unresolved = unresolved_significant_flags(flag_registry)
33	    open_flags = [
34	        {
35	            "id": flag["id"],
36	            "concern": flag["concern"],
37	            "evidence": flag.get("evidence", ""),
38	            "category": flag["category"],
39	            "severity": flag.get("severity", "unknown"),
40	            "status": flag["status"],
41	            "weight": flag.get("weight"),
42	        }
43	        for flag in unresolved
44	    ]
45	    robustness = configured_robustness(state)
46	    debt_block = _gate_debt_block(plan_dir, root)
47	    # Critique check summary — flagged counts only (unflagged findings are in the
48	    # artifact JSON for audit but not injected into the gate prompt).
49	    critique_checks_block = ""
50	    critique_path = current_iteration_artifact(plan_dir, "critique", state["iteration"])
51	    if Path(critique_path).exists():
52	        critique_data = read_json(critique_path)
53	        checks = critique_data.get("checks", [])
54	        if checks:
55	            check_lines = []
56	            for check in checks:
57	                findings = check.get("findings", [])
58	                flagged_count = sum(1 for f in findings if f.get("flagged"))
59	                status = f"{flagged_count} flagged" if flagged_count else "clear"
60	                check_lines.append(f"- {check.get('id', '?')}: {status}")
61	            critique_checks_block = (
62	                "Critique check summary:\n        "
63	                + "\n        ".join(check_lines)
64	            )
65	    return textwrap.dedent(
66	        f"""
67	        You are the gatekeeper for the megaplan workflow. Make the continuation decision directly.
68	
69	        Project directory:
70	        {project_dir}
71	
72	        {intent_and_notes_block(state)}
73	
74	        Plan:
75	        {latest_plan}
76	
77	        Plan metadata:
78	        {json_dump(latest_meta).strip()}
79	
80	        Gate signals:
81	        {json_dump(gate_signals).strip()}
82	
83	        {critique_checks_block}
84	
85	        Unresolved significant flags:
86	        {json_dump(open_flags).strip()}
87	
88	        {debt_block}
89	
90	        Robustness level:
91	        {robustness}
92	
93	        Requirements:
94	        - Decide exactly one of: PROCEED, ITERATE, ESCALATE.
95	        - Use the weighted score, flag details (including `evidence`), plan delta, recurring critiques, and preflight results as judgment context.
96	        - PROCEED when execution should move forward now.
97	        - ITERATE when revising the plan is the best next move.
98	        - ESCALATE when the loop is stuck, churn is recurring, or user intervention is needed.
99	        - `signals_assessment`: one paragraph summarizing score trajectory, flag status, and preflight posture.
100	
101	        Flags come in two tiers:
102	        - **Blocking** (severity = significant/likely-significant): These are serious concerns. If you recommend PROCEED, you MUST provide a `flag_resolutions` entry for every blocking flag. There is no implicit acceptance.
103	        - **Noted** (everything else): Acknowledge in your rationale but they don't block PROCEED.
104	
105	        If there are blocking flags and you want to PROCEED, provide `flag_resolutions` with one entry per blocking flag. If you cannot resolve every blocking flag, choose ITERATE (send back for revision) or ESCALATE (human intervention needed).
106	        Structurally unresolvable flags (for example, infrastructure outside the repo or product decisions that require a human) are ESCALATE, not PROCEED with a non-answer.
107	
108	        For each blocking flag:
109	        - **dispute**: The critique is factually wrong. Evidence must cite something specific (file path, line, API doc, etc.). Generic statements like "handled correctly" are invalid.
110	        - **accept_tradeoff**: The concern is real but intentionally accepted as a known limitation. Rationale must be specific to this flag. Boilerplate like "acceptable within scope" is invalid.
111	        - Schema requirement: every `flag_resolutions` entry must include both `evidence` and `rationale`. Use `""` for the field that does not apply to that action.
112	
113	        If there are no blocking flags, return `flag_resolutions: []`.
114	        Always return `accepted_tradeoffs`; use `[]` when none apply.
115	
116	        Populate `settled_decisions` with design choices that should carry into review without re-litigation. Return `[]` when there are none.
117	
118	        Example:
119	        ```json
120	        {{
121	          "recommendation": "PROCEED",
122	          "rationale": "Core fix is correct. Convention concern accepted.",
123	          "signals_assessment": "Score stable at 2.5, preflight passed, no recurring critiques.",
124	          "warnings": ["Verify edge case with composite moduli during execution."],
125	          "flag_resolutions": [
126	            {{"flag_id": "correctness-1", "action": "dispute", "evidence": "allow_migrate and allow_migrate_model produce identical behavior for this use case (verified at django/db/utils.py:286).", "rationale": ""}},
127	            {{"flag_id": "performance-1", "action": "accept_tradeoff", "evidence": "", "rationale": "Cold-start latency remains 40ms above target because the cache warmup job is owned by platform and outside this repo; rollout is still approved for the limited internal beta."}},
128	            {{"flag_id": "conventions-1", "action": "accept_tradeoff", "evidence": "", "rationale": "Minor naming inconsistency is confined to this helper and would create churn across generated fixtures; track it as follow-up cleanup instead of blocking this fix."}}
129	          ],
130	          "accepted_tradeoffs": [],
131	          "settled_decisions": []
132	        }}
133	        ```
134	        """
135	    ).strip()
136	
137	
138	def _collect_critique_summaries(
139	    plan_dir: Path, iteration: int
140	) -> list[dict[str, object]]:
141	    """Gather a compact list of all critique rounds for the finalize prompt."""
142	    summaries: list[dict[str, object]] = []
143	    for i in range(1, iteration + 1):
144	        path = plan_dir / f"critique_v{i}.json"
145	        if path.exists():
146	            data = read_json(path)
147	            summaries.append(
148	                {
149	                    "iteration": i,
150	                    "flag_count": len(data.get("flags", [])),
151	                    "verified": data.get("verified_flag_ids", []),
152	                }
153	            )
154	    return summaries
155	
156	
157	def _flag_summary(registry: FlagRegistry) -> list[dict[str, object]]:
158	    """Compact flag list for the finalize prompt."""
159	    return [
160	        {
161	            "id": f["id"],
162	            "concern": f["concern"],
163	            "evidence": f.get("evidence", ""),
164	            "status": f["status"],
165	            "severity": f.get("severity", "unknown"),
166	        }
167	        for f in registry["flags"]
168	    ]
169
```

> TOOL

tool_use Grep
```json
{
  "pattern": "def _gate_prompt",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/gate.py",
  "output_mode": "content",
  "context": 3
}
```

> TOOL

tool_result Grep
```
21-from ._shared import _gate_debt_block
22-
23-
24:def _gate_prompt(state: PlanState, plan_dir: Path, root: Path | None = None) -> str:
25-    project_dir = Path(state["config"]["project_dir"])
26-    latest_plan = latest_plan_path(plan_dir, state).read_text(encoding="utf-8")
27-    latest_meta = read_json(latest_plan_meta_path(plan_dir, state))
```

> AGENT

Now let me get the critique and tiebreaker files:

> TOOL

tool_use Grep
```json
{
  "pattern": "def _critique_context|def _build_critique_prompt|def _revise_prompt",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/critique.py",
  "output_mode": "content",
  "context": 3
}
```

> TOOL

tool_result Grep
```
24-from .planning import PLAN_TEMPLATE
25-
26-
27:def _revise_prompt(state: PlanState, plan_dir: Path) -> str:
28-    project_dir = Path(state["config"]["project_dir"])
29-    prep_block, prep_instruction = _render_prep_block(plan_dir)
30-    latest_plan = latest_plan_path(plan_dir, state).read_text(encoding="utf-8")
--
84-    ).strip()
85-
86-
87:def _critique_context(state: PlanState, plan_dir: Path, root: Path | None = None) -> dict[str, Any]:
88-    project_dir = Path(state["config"]["project_dir"])
89-    prep_block, prep_instruction = _render_prep_block(plan_dir)
90-    latest_plan = latest_plan_path(plan_dir, state).read_text(encoding="utf-8")
--
164-    return checks_template
165-
166-
167:def _build_critique_prompt(
168-    state: PlanState,
169-    context: dict[str, Any],
170-    critique_review_block: str,
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/tiebreaker.py",
  "limit": 150
}
```

> TOOL

tool_result Read
```
1	"""Tiebreaker subcommand — structured decision support for architectural questions.
2	
3	Runs two independent subagents (researcher → challenger) then synthesizes
4	their output into a human-readable decision brief.
5	"""
6	from __future__ import annotations
7	
8	import argparse
9	import json
10	import sys
11	from pathlib import Path
12	from typing import Any
13	
14	from megaplan._core import (
15	    atomic_write_json,
16	    atomic_write_text,
17	    read_json,
18	    resolve_plan_dir,
19	)
20	from megaplan.prompts.tiebreaker_challenger import challenger_prompt
21	from megaplan.prompts.tiebreaker_researcher import researcher_prompt
22	from megaplan.prompts.tiebreaker_synthesis import render_synthesis
23	from megaplan.types import CliError, PlanState
24	from megaplan.workers import run_step_with_worker
25	
26	
27	# ---------------------------------------------------------------------------
28	# Version-suffix logic
29	# ---------------------------------------------------------------------------
30	
31	
32	def _next_version_suffix(plan_dir: Path) -> str:
33	    """Scan for existing tiebreaker_researcher* artifacts and return the next suffix.
34	
35	    First run → "", second → "_v2", third → "_v3", etc.
36	    """
37	    existing = sorted(plan_dir.glob("tiebreaker_researcher*.json"))
38	    count = len(existing)
39	    if count == 0:
40	        return ""
41	    return f"_v{count + 1}"
42	
43	
44	# ---------------------------------------------------------------------------
45	# Orchestrator
46	# ---------------------------------------------------------------------------
47	
48	
49	def _run_tiebreaker(
50	    root: Path,
51	    plan_dir: Path,
52	    state: PlanState,
53	    args: argparse.Namespace,
54	) -> int:
55	    question = _resolve_question(args)
56	    suffix = _next_version_suffix(plan_dir)
57	
58	    researcher_file = f"tiebreaker_researcher{suffix}.json"
59	    challenger_file = f"tiebreaker_challenger{suffix}.json"
60	    synthesis_file = f"tiebreaker{suffix}.md"
61	
62	    # -- Researcher pass --
63	    r_prompt = researcher_prompt(question, state, plan_dir, root=root)
64	    resolved = _build_resolved(args, "tiebreaker_researcher")
65	
66	    researcher_result, r_agent, _, _ = run_step_with_worker(
67	        "tiebreaker_researcher",
68	        dict(state),  # FLAG-003: shallow copy to prevent state pollution
69	        plan_dir,
70	        args,
71	        root=root,
72	        resolved=resolved,
73	        prompt_override=r_prompt,
74	    )
75	    if not researcher_result.success:
76	        payload = {
77	            "success": False,
78	            "error": "researcher_failed",
79	            "message": researcher_result.error or "Researcher step failed",
80	        }
81	        sys.stdout.write(json.dumps(payload, indent=2) + "\n")
82	        return 1
83	
84	    researcher_data = researcher_result.parsed or {}
85	    atomic_write_json(plan_dir / researcher_file, researcher_data)
86	    sys.stderr.write(f"[tiebreaker] researcher done → {researcher_file}\n")
87	
88	    # -- Challenger pass --
89	    c_prompt = challenger_prompt(
90	        question, researcher_data, state, plan_dir, root=root
91	    )
92	    resolved_c = _build_resolved(args, "tiebreaker_challenger")
93	
94	    challenger_result, c_agent, _, _ = run_step_with_worker(
95	        "tiebreaker_challenger",
96	        dict(state),  # FLAG-003: shallow copy
97	        plan_dir,
98	        args,
99	        root=root,
100	        resolved=resolved_c,
101	        prompt_override=c_prompt,
102	    )
103	    if not challenger_result.success:
104	        payload = {
105	            "success": False,
106	            "error": "challenger_failed",
107	            "message": challenger_result.error or "Challenger step failed",
108	            "researcher_artifact": researcher_file,
109	        }
110	        sys.stdout.write(json.dumps(payload, indent=2) + "\n")
111	        return 1
112	
113	    challenger_data = challenger_result.parsed or {}
114	    atomic_write_json(plan_dir / challenger_file, challenger_data)
115	    sys.stderr.write(f"[tiebreaker] challenger done → {challenger_file}\n")
116	
117	    # -- Synthesis --
118	    synthesis_md = render_synthesis(question, researcher_data, challenger_data)
119	    atomic_write_text(plan_dir / synthesis_file, synthesis_md)
120	    sys.stderr.write(f"[tiebreaker] synthesis → {synthesis_file}\n")
121	
122	    output_path = getattr(args, "output", None)
123	    if output_path:
124	        Path(output_path).write_text(synthesis_md, encoding="utf-8")
125	        sys.stderr.write(f"[tiebreaker] also written to {output_path}\n")
126	
127	    payload = {
128	        "success": True,
129	        "plan": state["name"],
130	        "question": question,
131	        "researcher_agent": r_agent,
132	        "challenger_agent": c_agent,
133	        "artifacts": {
134	            "researcher": researcher_file,
135	            "challenger": challenger_file,
136	            "synthesis": synthesis_file,
137	        },
138	    }
139	    sys.stdout.write(json.dumps(payload, indent=2) + "\n")
140	    return 0
141	
142	
143	def _build_resolved(
144	    args: argparse.Namespace, step: str
145	) -> tuple[str, str, bool, str | None]:
146	    """Build a resolved tuple for ephemeral mode (FLAG-002)."""
147	    from megaplan.workers import resolve_agent_mode
148	
149	    agent, _mode, _refreshed, model = resolve_agent_mode(step, args)
150	    return (agent, "ephemeral", True, model)
```

> TOOL

tool_use Bash
```json
{
  "command": "wc -l /Users/user_c042661f/Documents/megaplan/megaplan/tiebreaker.py"
}
```

> TOOL

tool_result Bash
```
264 /Users/user_c042661f/Documents/megaplan/megaplan/tiebreaker.py
[rerun: b2]
```

> AGENT

Now let me read the rest of tiebreaker.py and check cli.py and auto.py:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/tiebreaker.py",
  "offset": 150
}
```

> TOOL

tool_result Read
```
150	    return (agent, "ephemeral", True, model)
151	
152	
153	def _resolve_question(args: argparse.Namespace) -> str:
154	    question_file = getattr(args, "question_file", None)
155	    question_inline = getattr(args, "question", None)
156	    if question_file:
157	        path = Path(question_file)
158	        if not path.exists():
159	            raise CliError("missing_file", f"Question file not found: {question_file}")
160	        return path.read_text(encoding="utf-8").strip()
161	    if question_inline:
162	        return question_inline.strip()
163	    raise CliError("invalid_args", "Provide --question or --question-file")
164	
165	
166	# ---------------------------------------------------------------------------
167	# Status
168	# ---------------------------------------------------------------------------
169	
170	
171	def _run_tiebreaker_status(
172	    root: Path,
173	    plan_dir: Path,
174	    state: PlanState,
175	) -> int:
176	    researcher_files = sorted(plan_dir.glob("tiebreaker_researcher*.json"))
177	    challenger_files = sorted(plan_dir.glob("tiebreaker_challenger*.json"))
178	    synthesis_files = sorted(plan_dir.glob("tiebreaker*.md"))
179	
180	    runs: list[dict[str, Any]] = []
181	    for rf in researcher_files:
182	        suffix = rf.stem.replace("tiebreaker_researcher", "")
183	        cf = plan_dir / f"tiebreaker_challenger{suffix}.json"
184	        sf = plan_dir / f"tiebreaker{suffix}.md"
185	        runs.append({
186	            "suffix": suffix or "(first)",
187	            "researcher": rf.name,
188	            "challenger": cf.name if cf.exists() else None,
189	            "synthesis": sf.name if sf.exists() else None,
190	            "complete": cf.exists() and sf.exists(),
191	        })
192	
193	    payload = {
194	        "success": True,
195	        "plan": state["name"],
196	        "runs": runs,
197	        "total_runs": len(runs),
198	    }
199	    sys.stdout.write(json.dumps(payload, indent=2) + "\n")
200	    return 0
201	
202	
203	# ---------------------------------------------------------------------------
204	# CLI plumbing
205	# ---------------------------------------------------------------------------
206	
207	
208	def _add_common_agent_args(parser: argparse.ArgumentParser) -> None:
209	    """Add the agent/session flags that resolve_agent_mode expects (FLAG-001)."""
210	    parser.add_argument(
211	        "--agent",
212	        choices=["claude", "codex", "hermes"],
213	        default=None,
214	        help="Agent to use for tiebreaker steps",
215	    )
216	    parser.add_argument(
217	        "--hermes",
218	        nargs="?",
219	        const="",
220	        default=None,
221	        help="Use Hermes agent. Optional: specify model",
222	    )
223	    parser.add_argument(
224	        "--phase-model",
225	        action="append",
226	        default=[],
227	        help="Per-step model override, e.g. --phase-model tiebreaker_researcher=hermes:openai/gpt-5",
228	    )
229	    parser.add_argument("--fresh", action="store_true")
230	    parser.add_argument("--persist", action="store_true")
231	    parser.add_argument("--ephemeral", action="store_true")
232	
233	
234	def build_tiebreaker_parser(subparsers: Any) -> None:
235	    tb_parser = subparsers.add_parser(
236	        "tiebreaker",
237	        help="Run structured decision support for architectural questions",
238	    )
239	    tb_sub = tb_parser.add_subparsers(dest="tiebreaker_action")
240	
241	    # Default (run) action args live on the top-level tiebreaker parser.
242	    tb_parser.add_argument("--plan", default=None, help="Plan name")
243	    question_group = tb_parser.add_mutually_exclusive_group()
244	    question_group.add_argument("--question", help="Decision question (inline)")
245	    question_group.add_argument("--question-file", help="Path to decision question file")
246	    tb_parser.add_argument("--output", help="Additional output path for the synthesis markdown")
247	    _add_common_agent_args(tb_parser)
248	
249	    # Status subcommand
250	    status_parser = tb_sub.add_parser("status", help="Show tiebreaker run status")
251	    status_parser.add_argument("--plan", default=None, help="Plan name")
252	
253	
254	def run_tiebreaker_cli(root: Path, args: argparse.Namespace) -> int:
255	    action = getattr(args, "tiebreaker_action", None)
256	    plan_name = getattr(args, "plan", None)
257	
258	    plan_dir = resolve_plan_dir(root, plan_name)
259	    state: PlanState = read_json(plan_dir / "state.json")
260	
261	    if action == "status":
262	        return _run_tiebreaker_status(root, plan_dir, state)
263	
264	    return _run_tiebreaker(root, plan_dir, state, args)
265
```

> TOOL

tool_use Grep
```json
{
  "pattern": "def build_tiebreaker_parser",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan/tiebreaker.py",
  "output_mode": "content",
  "context": 15
}
```

> TOOL

tool_result Grep
```
219-        const="",
220-        default=None,
221-        help="Use Hermes agent. Optional: specify model",
222-    )
223-    parser.add_argument(
224-        "--phase-model",
225-        action="append",
226-        default=[],
227-        help="Per-step model override, e.g. --phase-model tiebreaker_researcher=hermes:openai/gpt-5",
228-    )
229-    parser.add_argument("--fresh", action="store_true")
230-    parser.add_argument("--persist", action="store_true")
231-    parser.add_argument("--ephemeral", action="store_true")
232-
233-
234:def build_tiebreaker_parser(subparsers: Any) -> None:
235-    tb_parser = subparsers.add_parser(
236-        "tiebreaker",
237-        help="Run structured decision support for architectural questions",
238-    )
239-    tb_sub = tb_parser.add_subparsers(dest="tiebreaker_action")
240-
241-    # Default (run) action args live on the top-level tiebreaker parser.
242-    tb_parser.add_argument("--plan", default=None, help="Plan name")
243-    question_group = tb_parser.add_mutually_exclusive_group()
244-    question_group.add_argument("--question", help="Decision question (inline)")
245-    question_group.add_argument("--question-file", help="Path to decision question file")
246-    tb_parser.add_argument("--output", help="Additional output path for the synthesis markdown")
247-    _add_common_agent_args(tb_parser)
248-
249-    # Status subcommand
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tiebreaker",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan/cli.py",
  "output_mode": "content",
  "context": 2,
  "head_limit": 30
}
```

> TOOL

tool_result Grep
```
978-    build_chain_parser(subparsers)
979-
980:    from megaplan.tiebreaker import build_tiebreaker_parser
981:    build_tiebreaker_parser(subparsers)
982-
983-    return parser
--
1082-            return error_response(error, root=root)
1083-
1084:    if args.command == "tiebreaker":
1085:        from megaplan.tiebreaker import run_tiebreaker_cli
1086-        try:
1087:            return run_tiebreaker_cli(root, args)
1088-        except CliError as error:
1089-            return error_response(error, root=root)
```

> AGENT

Now let me check auto.py for dispatcher logic:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/auto.py",
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

> TOOL

tool_use Bash
```json
{
  "command": "wc -l /Users/user_c042661f/Documents/megaplan/megaplan/auto.py"
}
```

> TOOL

tool_result Bash
```
407 /Users/user_c042661f/Documents/megaplan/megaplan/auto.py
[rerun: b3]
```

> TOOL

tool_use Grep
```json
{
  "pattern": "workflow|transition|dispatch|handler",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan/auto.py",
  "output_mode": "content",
  "context": 2,
  "head_limit": 40
}
```

> TOOL

tool_result Grep
```
72-    """Run a megaplan sub-command in its own process.
73-
74:    We shell out rather than importing the handlers directly so each phase gets
75:    a fresh argparse/handler lifecycle. This matches how external orchestrators
76-    drive the CLI and avoids subtle state leakage between phases.
77-
--
358-        type=float,
359-        default=DEFAULT_POLL_SLEEP_SECONDS,
360:        help=f"Seconds to sleep between phase transitions (default {DEFAULT_POLL_SLEEP_SECONDS})",
361-    )
362-    auto_parser.add_argument(
```

> AGENT

Let me get more details from handlers.py about _apply_gate_outcome and the gate recommendations:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 600,
  "limit": 250
}
```

> TOOL

tool_result Read
```
600	        "passed": gate_summary["passed"],
601	        "preflight_results": gate_summary["preflight_results"],
602	        "orchestrator_guidance": gate_summary["orchestrator_guidance"],
603	    }
604	
605	
606	def _apply_gate_outcome(
607	    state: PlanState,
608	    gate_summary: dict[str, Any],
609	    *,
610	    robustness: str,
611	    plan_dir: Path,
612	) -> tuple[str, str, str, list[str]]:
613	    result = "success"
614	    summary = f"Gate recommendation {gate_summary['recommendation']}: {gate_summary['rationale']}"
615	
616	    # Process explicit flag resolutions when the gate recommends PROCEED.
617	    if gate_summary["recommendation"] == "PROCEED":
618	        unresolved = gate_summary.get("unresolved_flags", [])
619	        resolutions = gate_summary.get("flag_resolutions", [])
620	
621	        # Validate each explicit resolution
622	        valid_resolved_ids: set[str] = set()
623	        for res in resolutions:
624	            action = res.get("action", "")
625	            flag_id = res.get("flag_id", "")
626	            if action == "dispute":
627	                evidence = res.get("evidence", "").strip()
628	                if not evidence or is_rubber_stamp(evidence, strict=True):
629	                    continue  # invalid dispute — skip
630	            elif action == "accept_tradeoff":
631	                rationale = res.get("rationale", "").strip()
632	                if not rationale or is_rubber_stamp(rationale, strict=True):
633	                    continue  # invalid tradeoff acceptance — skip
634	            else:
635	                continue  # unknown action — skip
636	            valid_resolved_ids.add(flag_id)
637	
638	        blocking_unresolved = [
639	            f for f in unresolved
640	            if f.get("severity") in ("significant", "likely-significant")
641	            and f.get("status") in FLAG_BLOCKING_STATUSES
642	            and f.get("id") not in valid_resolved_ids
643	        ]
644	        blocking_unresolved_ids = [f.get("id", "") for f in blocking_unresolved if f.get("id")]
645	
646	        # Persist explicit resolutions
647	        if valid_resolved_ids:
648	            update_flags_after_gate(plan_dir, resolutions)
649	
650	        if blocking_unresolved_ids:
651	            return "unresolved_flags", "gate", summary, blocking_unresolved_ids
652	
653	    if gate_summary["recommendation"] == "PROCEED" and gate_summary["passed"]:
654	        state["current_state"] = STATE_GATED
655	        state["meta"].pop("user_approved_gate", None)
656	        return result, "finalize", summary, []
657	    state["current_state"] = STATE_CRITIQUED
658	    if gate_summary["recommendation"] == "PROCEED":
659	        result = "blocked"
660	        summary = "Gate recommended PROCEED, but preflight checks are still blocking execution."
661	        return result, "revise", summary, []
662	    if gate_summary["recommendation"] == "ITERATE":
663	        return result, "revise", summary, []
664	    if gate_summary["recommendation"] == "ESCALATE":
665	        return result, "override add-note", summary, []
666	    result = "unknown_recommendation"
667	    summary = f"Gate returned unknown recommendation '{gate_summary['recommendation']}'; treating as escalation."
668	    return result, "override add-note", summary, []
669	
670	
671	def _merge_gate_worker_attempt(base: WorkerResult, retry: WorkerResult) -> WorkerResult:
672	    base.payload = retry.payload
673	    base.raw_output = "\n\n".join(part for part in [base.raw_output, retry.raw_output] if part)
674	    if base.trace_output or retry.trace_output:
675	        base.trace_output = "\n\n".join(part for part in [base.trace_output, retry.trace_output] if part)
676	    base.duration_ms += retry.duration_ms
677	    base.cost_usd += retry.cost_usd
678	    base.session_id = retry.session_id or base.session_id
679	    base.prompt_tokens += retry.prompt_tokens
680	    base.completion_tokens += retry.completion_tokens
681	    base.total_tokens += retry.total_tokens
682	    return base
683	
684	
685	def _merge_resolution_tradeoffs_into_payload(gate_summary: dict[str, Any], worker_payload: dict[str, Any]) -> None:
686	    raw_tradeoffs = worker_payload.get("accepted_tradeoffs", [])
687	    merged_tradeoffs = list(raw_tradeoffs) if isinstance(raw_tradeoffs, list) else []
688	    existing_ids = {
689	        item.get("flag_id")
690	        for item in merged_tradeoffs
691	        if isinstance(item, dict) and isinstance(item.get("flag_id"), str)
692	    }
693	    unresolved_by_id = {
694	        flag.get("id"): flag
695	        for flag in gate_summary.get("unresolved_flags", [])
696	        if isinstance(flag, dict) and isinstance(flag.get("id"), str)
697	    }
698	    for resolution in gate_summary.get("flag_resolutions", []):
699	        if not isinstance(resolution, dict) or resolution.get("action") != "accept_tradeoff":
700	            continue
701	        flag_id = resolution.get("flag_id")
702	        if not isinstance(flag_id, str) or flag_id in existing_ids:
703	            continue
704	        flag = unresolved_by_id.get(flag_id)
705	        if not isinstance(flag, dict):
706	            continue
707	        concern = flag.get("concern")
708	        if not isinstance(concern, str):
709	            continue
710	        tradeoff = {"flag_id": flag_id, "concern": concern}
711	        subsystem = flag.get("subsystem")
712	        if isinstance(subsystem, str) and subsystem.strip():
713	            tradeoff["subsystem"] = subsystem
714	        merged_tradeoffs.append(tradeoff)
715	        existing_ids.add(flag_id)
716	    worker_payload["accepted_tradeoffs"] = merged_tradeoffs
717	
718	
719	def handle_init(root: Path, args: argparse.Namespace) -> StepResponse:
720	    ensure_runtime_layout(root)
721	    project_dir = Path(args.project_dir).expanduser().resolve()
722	    if not project_dir.exists() or not project_dir.is_dir():
723	        raise CliError("invalid_project_dir", f"Project directory does not exist: {project_dir}")
724	    robustness = getattr(args, "robustness", None)
725	    if robustness is None:
726	        robustness = get_effective("execution", "robustness")
727	    if robustness not in ROBUSTNESS_LEVELS:
728	        robustness = "standard"
729	    auto_approve_value = getattr(args, "auto_approve", None)
730	    if auto_approve_value is None:
731	        auto_approve_value = get_effective("execution", "auto_approve")
732	    auto_approve = bool(auto_approve_value)
733	    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
734	    plan_name = args.name or f"{slugify(args.idea)}-{timestamp}"
735	    plan_dir = plans_root(root) / plan_name
736	    if plan_dir.exists():
737	        raise CliError("duplicate_plan", f"Plan directory already exists: {plan_name}")
738	    plan_dir.mkdir(parents=True, exist_ok=False)
739	
740	    state: PlanState = {
741	        "name": plan_name,
742	        "idea": args.idea,
743	        "current_state": STATE_INITIALIZED,
744	        "iteration": 0,
745	        "created_at": now_utc(),
746	        "config": {
747	            "project_dir": str(project_dir),
748	            "auto_approve": auto_approve,
749	            "robustness": robustness,
750	            "agent": "hermes" if getattr(args, "hermes", None) is not None else "",
751	        },
752	        "sessions": {},
753	        "plan_versions": [],
754	        "history": [],
755	        "meta": {
756	            "significant_counts": [],
757	            "weighted_scores": [],
758	            "plan_deltas": [],
759	            "recurring_critiques": [],
760	            "total_cost_usd": 0.0,
761	            "overrides": [],
762	            "notes": [],
763	        },
764	        "last_gate": {},
765	    }
766	    append_history(
767	        state,
768	        make_history_entry(
769	            "init",
770	            duration_ms=0,
771	            cost_usd=0.0,
772	            result="success",
773	            environment={
774	                "claude": bool(find_command("claude")),
775	                "codex": bool(find_command("codex")),
776	            },
777	        ),
778	    )
779	    save_state(plan_dir, state)
780	    next_steps = workflow_next(state)
781	    response: StepResponse = {
782	        "success": True,
783	        "step": "init",
784	        "plan": plan_name,
785	        "state": STATE_INITIALIZED,
786	        "summary": f"Initialized plan '{plan_name}' for project {project_dir}",
787	        "artifacts": ["state.json"],
788	        "next_step": next_steps[0] if next_steps else None,
789	        "auto_approve": auto_approve,
790	        "robustness": robustness,
791	    }
792	    _attach_next_step_runtime(response)
793	    return response
794	
795	
796	def handle_plan(root: Path, args: argparse.Namespace) -> StepResponse:
797	    with load_plan_locked(root, args.plan, step="plan") as (plan_dir, state):
798	        require_state(state, "plan", {STATE_INITIALIZED, STATE_PREPPED, STATE_PLANNED})
799	        rerun = state["current_state"] == STATE_PLANNED
800	        version = state["iteration"] if rerun else state["iteration"] + 1
801	        worker, agent, mode, refreshed = _run_worker("plan", state, plan_dir, args, root=root, iteration=version)
802	        payload = worker.payload
803	        plan_filename, meta_filename, meta = _write_plan_version(
804	            plan_dir=plan_dir,
805	            state=state,
806	            step="plan",
807	            version=version,
808	            worker=worker,
809	            plan_text=payload["plan"].rstrip() + "\n",
810	            meta_fields={
811	                "questions": payload["questions"],
812	                "success_criteria": payload["success_criteria"],
813	                "assumptions": payload["assumptions"],
814	            },
815	        )
816	        state["iteration"], state["current_state"] = version, STATE_PLANNED
817	        state["meta"].pop("user_approved_gate", None)
818	        state["last_gate"] = {}
819	        state["plan_versions"].append({
820	            "version": version, "file": plan_filename,
821	            "hash": meta["hash"], "timestamp": meta["timestamp"],
822	        })
823	        verb = "Refined" if rerun else "Generated"
824	        return _finish_step(
825	            plan_dir, state, args,
826	            step="plan",
827	            worker=worker, agent=agent, mode=mode, refreshed=refreshed,
828	            summary=f"{verb} plan v{version} with {len(payload['questions'])} questions and {len(payload['success_criteria'])} success criteria.",
829	            artifacts=[plan_filename, meta_filename],
830	            output_file=plan_filename,
831	            artifact_hash=meta["hash"],
832	            response_fields={
833	                "iteration": version,
834	                "questions": payload["questions"],
835	                "assumptions": payload["assumptions"],
836	                "success_criteria": payload["success_criteria"],
837	            },
838	        )
839	
840	
841	
842	def handle_prep(root: Path, args: argparse.Namespace) -> StepResponse:
843	    with load_plan_locked(root, args.plan, step="prep") as (plan_dir, state):
844	        require_state(state, "prep", {STATE_INITIALIZED})
845	        worker, agent, mode, refreshed = _run_worker("prep", state, plan_dir, args, root=root)
846	        prep_filename = "prep.json"
847	        artifact_hash = _write_json_artifact(plan_dir, prep_filename, worker.payload)
848	        code_refs = len(worker.payload.get("relevant_code", []))
849	        test_refs = len(worker.payload.get("test_expectations", []))
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 1110,
  "limit": 300
}
```

> TOOL

tool_result Read
```
1110	                "plan_delta_percent": delta,
1111	            },
1112	            history_fields={"flags_addressed": payload["flags_addressed"]},
1113	        )
1114	
1115	
1116	def handle_gate(root: Path, args: argparse.Namespace) -> StepResponse:
1117	    with load_plan_locked(root, args.plan, step="gate") as (plan_dir, state):
1118	        require_state(state, "gate", {STATE_CRITIQUED})
1119	        iteration = state["iteration"]
1120	        gate_signals, signals_filename, signals_artifact = _build_gate_signals_artifact(plan_dir, state, iteration=iteration, root=root)
1121	        resolved = resolve_agent_mode("gate", args)
1122	        worker, agent, mode, refreshed = _run_worker(
1123	            "gate",
1124	            state,
1125	            plan_dir,
1126	            args,
1127	            root=root,
1128	            resolved=resolved,
1129	        )
1130	        gate_payload = worker.payload
1131	        guidance = build_orchestrator_guidance(
1132	            gate_payload=gate_payload,
1133	            signals=signals_artifact["signals"],
1134	            preflight_passed=all(signals_artifact["preflight_results"].values()),
1135	            preflight_results=signals_artifact["preflight_results"],
1136	            robustness=signals_artifact.get("robustness", "standard"),
1137	            plan_name=state["name"],
1138	        )
1139	        gate_summary = build_gate_artifact(
1140	            signals_artifact,
1141	            gate_payload,
1142	            override_forced=False,
1143	            orchestrator_guidance=guidance,
1144	        )
1145	        gate_summary["reprompted"] = False
1146	        if len(state["meta"].get("weighted_scores", [])) < iteration:
1147	            _append_to_meta(state, "weighted_scores", gate_signals["signals"]["weighted_score"])
1148	        result, next_step, summary, blocking_unresolved_ids = _apply_gate_outcome(
1149	            state,
1150	            gate_summary,
1151	            robustness=gate_signals["robustness"],
1152	            plan_dir=plan_dir,
1153	        )
1154	        if blocking_unresolved_ids:
1155	            reprompt_prompt = _build_gate_prompt_override(
1156	                agent,
1157	                state,
1158	                plan_dir,
1159	                root=root,
1160	                missing_flag_ids=blocking_unresolved_ids,
1161	            )
1162	            retry_worker, _, _, _ = _run_worker(
1163	                "gate",
1164	                state,
1165	                plan_dir,
1166	                args,
1167	                root=root,
1168	                resolved=resolved,
1169	                prompt_override=reprompt_prompt,
1170	            )
1171	            worker = _merge_gate_worker_attempt(worker, retry_worker)
1172	            gate_payload = worker.payload
1173	            guidance = build_orchestrator_guidance(
1174	                gate_payload=gate_payload,
1175	                signals=signals_artifact["signals"],
1176	                preflight_passed=all(signals_artifact["preflight_results"].values()),
1177	                preflight_results=signals_artifact["preflight_results"],
1178	                robustness=signals_artifact.get("robustness", "standard"),
1179	                plan_name=state["name"],
1180	            )
1181	            gate_summary = build_gate_artifact(
1182	                signals_artifact,
1183	                gate_payload,
1184	                override_forced=False,
1185	                orchestrator_guidance=guidance,
1186	            )
1187	            gate_summary["reprompted"] = True
1188	            result, next_step, summary, blocking_unresolved_ids = _apply_gate_outcome(
1189	                state,
1190	                gate_summary,
1191	                robustness=gate_signals["robustness"],
1192	                plan_dir=plan_dir,
1193	            )
1194	            if blocking_unresolved_ids:
1195	                gate_summary["recommendation"] = "ITERATE"
1196	                gate_summary["passed"] = False
1197	                gate_summary["rationale"] = (
1198	                    f"{gate_summary['rationale']} "
1199	                    f"[Auto-downgraded from PROCEED: {len(blocking_unresolved_ids)} "
1200	                    "blocking flag(s) not resolved after reprompt]"
1201	                )
1202	                gate_summary["orchestrator_guidance"] = (
1203	                    "Gate auto-downgraded to ITERATE because blocking flags remained "
1204	                    "unresolved after reprompt. Revise the plan."
1205	                )
1206	                result = "blocked"
1207	                next_step = "revise"
1208	                summary = f"Gate recommendation {gate_summary['recommendation']}: {gate_summary['rationale']}"
1209	        _merge_resolution_tradeoffs_into_payload(gate_summary, worker.payload)
1210	        gate_hash = _write_json_artifact(plan_dir, "gate.json", gate_summary)
1211	        debt_entries_added = 0
1212	        if gate_summary["recommendation"] == "PROCEED":
1213	            debt_entries_added = _record_gate_debt_entries(root, state, gate_summary, worker.payload)
1214	        # Store last_gate AFTER _apply_gate_outcome — the outcome may override
1215	        # the recommendation (e.g. PROCEED → ITERATE when flags are unresolved).
1216	        _store_last_gate(state, gate_summary)
1217	        return _finish_step(
1218	            plan_dir,
1219	            state,
1220	            args,
1221	            step="gate",
1222	            worker=worker,
1223	            agent=agent,
1224	            mode=mode,
1225	            refreshed=refreshed,
1226	            summary=summary,
1227	            artifacts=[signals_filename, "gate.json"],
1228	            output_file="gate.json",
1229	            artifact_hash=gate_hash,
1230	            result=result,
1231	            success=gate_summary["recommendation"] != "PROCEED" or gate_summary["passed"],
1232	            next_step=next_step,
1233	            response_fields=_gate_response_fields(state, gate_summary, debt_entries_added),
1234	            history_fields={"recommendation": gate_summary["recommendation"]},
1235	        )
1236	
1237	
1238	def _ensure_verification_task(payload: dict, state: dict) -> None:
1239	    """Ensure the task list ends with a test verification task.
1240	
1241	    If the last task already looks like a verification/test task, leave it.
1242	    Otherwise append one that depends on all other tasks.
1243	    """
1244	    tasks = payload.get("tasks", [])
1245	    if not tasks:
1246	        return
1247	
1248	    # Check if last task is already a verification task
1249	    last_desc = (tasks[-1].get("description") or "").lower()
1250	    test_keywords = ("run test", "run the test", "verify", "verification", "pytest", "test suite", "run existing test")
1251	    has_verification_task = any(kw in last_desc for kw in test_keywords)
1252	
1253	    if not has_verification_task:
1254	        # Build the verification task
1255	        all_ids = [t["id"] for t in tasks]
1256	        next_num = max((int(t["id"].lstrip("T")) for t in tasks if t["id"].startswith("T")), default=0) + 1
1257	        task_id = f"T{next_num}"
1258	
1259	        # Pull specific test IDs from the original prompt if available
1260	        idea = state.get("idea", "") or ""
1261	        notes = "\n".join(state.get("notes", []) or [])
1262	        source_text = idea + "\n" + notes
1263	
1264	        if "FAIL_TO_PASS" in source_text or "test must pass" in source_text.lower() or "verification" in source_text.lower():
1265	            desc = (
1266	                "Run the tests specified in the task description to verify the fix — run the full test file/module, not just individual functions. "
1267	                "Run the project's existing test suite — do NOT create new test files. "
1268	                "If any test fails, read the error, fix the code, and re-run until all tests pass."
1269	            )
1270	        else:
1271	            desc = (
1272	                "Run tests relevant to the changed files to verify correctness and check for regressions — run the full test file/module, not just individual functions. "
1273	                "Find and run the project's existing test suite — do NOT create new test files. "
1274	                "If any test fails, read the error, fix the code, and re-run until all tests pass."
1275	            )
1276	
1277	        verification_task = {
1278	            "id": task_id,
1279	            "description": desc,
1280	            "depends_on": [all_ids[-1]],
1281	            "status": "pending",
1282	            "executor_notes": "",
1283	            "files_changed": [],
1284	            "commands_run": [],
1285	            "evidence_files": [],
1286	            "reviewer_verdict": "",
1287	        }
1288	        tasks.append(verification_task)
1289	
1290	        # Add a sense check for it
1291	        sense_checks = payload.get("sense_checks", [])
1292	        sc_num = max((int(sc["id"].lstrip("SC")) for sc in sense_checks if sc["id"].startswith("SC")), default=0) + 1
1293	        sense_checks.append({
1294	            "id": f"SC{sc_num}",
1295	            "task_id": task_id,
1296	            "question": "Did the verification tests pass? Were any regressions found and fixed?",
1297	            "executor_note": "",
1298	            "verdict": "",
1299	        })
1300	
1301	    failures = payload.get("baseline_test_failures")
1302	    if isinstance(failures, list) and failures:
1303	        tasks[-1]["description"] += (
1304	            f" Note: {len(failures)} tests were already failing before your changes "
1305	            "(see baseline_test_failures in finalize.json) — do not scope-creep into fixing these."
1306	        )
1307	
1308	
1309	def _capture_test_baseline(project_dir: Path, config: dict[str, Any]) -> dict[str, Any]:
1310	    if os.getenv(MOCK_ENV_VAR) == "1":
1311	        return {
1312	            "baseline_test_failures": [],
1313	            "baseline_test_command": "pytest --tb=no -q --no-header",
1314	        }
1315	
1316	    configured_command = config.get("test_command")
1317	    cmd_string: str | None = None
1318	
1319	    if isinstance(configured_command, str) and configured_command.strip():
1320	        cmd_string = configured_command.strip()
1321	        if cmd_string.startswith("pytest"):
1322	            cmd_string = f"{cmd_string} --tb=no -q --no-header"
1323	    elif shutil.which("pytest"):
1324	        cmd_string = "pytest --tb=no -q --no-header"
1325	
1326	    if cmd_string is None:
1327	        return {
1328	            "baseline_test_failures": None,
1329	            "baseline_test_command": None,
1330	            "baseline_test_note": (
1331	                "No supported test runner detected on PATH (looked for: pytest). "
1332	                "Configure test_command in state config to specify one."
1333	            ),
1334	        }
1335	
1336	    try:
1337	        result = subprocess.run(
1338	            cmd_string,
1339	            shell=True,
1340	            cwd=project_dir,
1341	            timeout=120,
1342	            capture_output=True,
1343	            text=True,
1344	        )
1345	    except subprocess.TimeoutExpired:
1346	        return {
1347	            "baseline_test_failures": None,
1348	            "baseline_test_command": cmd_string,
1349	            "baseline_test_note": (
1350	                f"Baseline test capture timed out after 120 seconds while running: {cmd_string}"
1351	            ),
1352	        }
1353	    except Exception as exc:
1354	        return {
1355	            "baseline_test_failures": None,
1356	            "baseline_test_command": None,
1357	            "baseline_test_note": f"Baseline capture crashed: {exc}",
1358	        }
1359	
1360	    failures: list[str] = []
1361	    for raw_line in result.stdout.splitlines():
1362	        line = raw_line.strip()
1363	        if not line.endswith(" FAILED"):
1364	            continue
1365	        test_id = line[: -len(" FAILED")].strip()
1366	        if test_id:
1367	            failures.append(test_id)
1368	
1369	    return {
1370	        "baseline_test_failures": failures,
1371	        "baseline_test_command": cmd_string,
1372	    }
1373	
1374	
1375	def handle_finalize(root: Path, args: argparse.Namespace) -> StepResponse:
1376	    with load_plan_locked(root, args.plan, step="finalize") as (plan_dir, state):
1377	        require_state(state, "finalize", {STATE_GATED})
1378	        worker, agent, mode, refreshed = _run_worker("finalize", state, plan_dir, args, root=root)
1379	        _validate_finalize_payload(plan_dir, state, worker)
1380	        artifact_hash = _write_finalize_artifacts(plan_dir, worker.payload, state)
1381	        state["current_state"] = STATE_FINALIZED
1382	        return _finish_step(
1383	            plan_dir, state, args,
1384	            step="finalize",
1385	            worker=worker, agent=agent, mode=mode, refreshed=refreshed,
1386	            summary=f"Finalized plan with {len(worker.payload['tasks'])} tasks and {len(worker.payload['watch_items'])} watch items.",
1387	            artifacts=["final.md", "finalize.json"],
1388	            output_file="finalize.json",
1389	            artifact_hash=artifact_hash,
1390	            next_step="execute",
1391	        )
1392	
1393	
1394	def _is_rework_reexecution(state: PlanState) -> bool:
1395	    """Check if the last completed step was a review with needs_rework."""
1396	    for entry in reversed(state.get("history", [])):
1397	        if entry.get("step") == "review" and entry.get("result") == "needs_rework":
1398	            return True
1399	        if entry.get("step") == "execute":
1400	            return False
1401	    return False
1402	
1403	
1404	def handle_execute(root: Path, args: argparse.Namespace) -> StepResponse:
1405	    with load_plan_locked(root, args.plan, step="execute") as (plan_dir, state):
1406	        require_state(state, "execute", {STATE_FINALIZED})
1407	        if not args.confirm_destructive:
1408	            raise CliError("missing_confirmation", "Execute requires --confirm-destructive")
1409	        auto_approve = bool(state["config"].get("auto_approve", False))
```

> AGENT

Perfect. Now let me gather the final piece about auto.py's dispatch mechanism and the critique prompts:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/critique.py",
  "limit": 200
}
```

> TOOL

tool_result Read
```
1	"""Critique- and revise-phase prompt builders."""
2	
3	from __future__ import annotations
4	
5	import textwrap
6	from pathlib import Path
7	from typing import Any
8	
9	from megaplan.checks import checks_for_robustness
10	from megaplan._core import (
11	    configured_robustness,
12	    intent_and_notes_block,
13	    json_dump,
14	    latest_plan_meta_path,
15	    latest_plan_path,
16	    load_flag_registry,
17	    read_json,
18	    robustness_critique_instruction,
19	    unresolved_significant_flags,
20	)
21	from megaplan.types import PlanState
22	
23	from ._shared import _planning_debt_block, _render_prep_block
24	from .planning import PLAN_TEMPLATE
25	
26	
27	def _revise_prompt(state: PlanState, plan_dir: Path) -> str:
28	    project_dir = Path(state["config"]["project_dir"])
29	    prep_block, prep_instruction = _render_prep_block(plan_dir)
30	    latest_plan = latest_plan_path(plan_dir, state).read_text(encoding="utf-8")
31	    latest_meta = read_json(latest_plan_meta_path(plan_dir, state))
32	    gate = read_json(plan_dir / "gate.json")
33	    unresolved = unresolved_significant_flags(load_flag_registry(plan_dir))
34	    open_flags = [
35	        {
36	            "id": flag["id"],
37	            "severity": flag.get("severity"),
38	            "status": flag["status"],
39	            "concern": flag["concern"],
40	            "evidence": flag.get("evidence"),
41	        }
42	        for flag in unresolved
43	    ]
44	    return textwrap.dedent(
45	        f"""
46	        You are revising an implementation plan after critique and gate feedback.
47	
48	        Project directory:
49	        {project_dir}
50	
51	        {prep_block}
52	        {prep_instruction}
53	
54	        {intent_and_notes_block(state)}
55	
56	        Current plan (markdown):
57	        {latest_plan}
58	
59	        Current plan metadata:
60	        {json_dump(latest_meta).strip()}
61	
62	        Gate summary:
63	        {json_dump(gate).strip()}
64	
65	        Open significant flags:
66	        {json_dump(open_flags).strip()}
67	
68	        Requirements:
69	        - Before addressing individual flags, check: does any flag suggest the plan is targeting the wrong code or the wrong root cause? If so, consider whether the plan needs a new approach rather than adjustments. Explain your reasoning.
70	        - Update the plan to address the significant issues.
71	        - Keep the plan readable and executable.
72	        - Return flags_addressed with the exact flag IDs you addressed.
73	        - Include `changes_summary` as a short plain-English summary of what changed in the revision. If there were no concrete flags, say that explicitly (for example: `No critique flags were raised; refined wording and kept the plan aligned for execution.`).
74	        - Preserve or improve success criteria quality. Each criterion must have a `priority` of `must`, `should`, or `info`. Promote or demote priorities if critique feedback reveals a criterion was over- or under-weighted.
75	        - Each success criterion should include a `requires` field listing the capabilities needed for verification. Valid capability strings: `run_shell`, `read_files`, `run_tests`, `parse_diff`, `read_build_output`, `run_linter` (container), `drive_browser`, `inspect_runtime_ui`, `observe_runtime_logs`, `subjective_judgment`, `verify_physical_device` (human). `must` criteria MUST have non-empty `requires`. Example: `{{"criterion": "All tests pass", "priority": "must", "requires": ["run_tests"]}}`.
76	        - Verify that the plan remains aligned with the user's original intent, not just internal plan quality.
77	        - Remove unjustified scope growth. If critique raised scope creep, narrow the plan back to the original idea unless the broader work is strictly required.
78	        - Maintain the structural template: H1 title, ## Overview, phase sections with numbered step sections, ## Execution Order or ## Validation Order.
79	        - CRITICAL: Your entire revised plan markdown (all sections) must be output as the `plan` field in the structured output. The prose response must not contain the plan text.
80	        - CRITICAL: Return only the structured JSON object for the schema fields `plan`, `changes_summary`, `flags_addressed`, `assumptions`, `success_criteria`, and `questions`. Do not add commentary before or after the JSON object.
81	
82	        {PLAN_TEMPLATE}
83	        """
84	    ).strip()
85	
86	
87	def _critique_context(state: PlanState, plan_dir: Path, root: Path | None = None) -> dict[str, Any]:
88	    project_dir = Path(state["config"]["project_dir"])
89	    prep_block, prep_instruction = _render_prep_block(plan_dir)
90	    latest_plan = latest_plan_path(plan_dir, state).read_text(encoding="utf-8")
91	    latest_meta = read_json(latest_plan_meta_path(plan_dir, state))
92	    structure_warnings = latest_meta.get("structure_warnings", [])
93	    flag_registry = load_flag_registry(plan_dir)
94	    unresolved = [
95	        {
96	            "id": flag["id"],
97	            "concern": flag["concern"],
98	            "status": flag["status"],
99	            "severity": flag.get("severity"),
100	        }
101	        for flag in flag_registry["flags"]
102	        if flag["status"] in {"addressed", "open", "disputed"}
103	    ]
104	    return {
105	        "project_dir": project_dir,
106	        "prep_block": prep_block,
107	        "prep_instruction": prep_instruction,
108	        "latest_plan": latest_plan,
109	        "latest_meta": latest_meta,
110	        "structure_warnings": structure_warnings,
111	        "unresolved": unresolved,
112	        "debt_block": _planning_debt_block(plan_dir, root),
113	        "robustness": configured_robustness(state),
114	    }
115	
116	
117	def _build_checks_template(
118	    plan_dir: Path,
119	    state: PlanState,
120	    checks: tuple[dict[str, Any], ...],
121	) -> list[dict[str, object]]:
122	    checks_template = []
123	    for check in checks:
124	        entry: dict[str, object] = {
125	            "id": check["id"],
126	            "question": check["question"],
127	            "guidance": check.get("guidance", ""),
128	            "findings": [],
129	        }
130	        checks_template.append(entry)
131	
132	    iteration = state.get("iteration", 1)
133	    if iteration > 1:
134	        prior_path = plan_dir / f"critique_v{iteration - 1}.json"
135	        if prior_path.exists():
136	            prior = read_json(prior_path)
137	            active_check_ids = {check["id"] for check in checks}
138	            prior_checks = {
139	                c.get("id"): c for c in prior.get("checks", [])
140	                if isinstance(c, dict) and c.get("id") in active_check_ids
141	            }
142	            registry = load_flag_registry(plan_dir)
143	            flag_status = {f["id"]: f.get("status", "open") for f in registry.get("flags", [])}
144	            for entry in checks_template:
145	                cid = entry["id"]
146	                if cid in prior_checks:
147	                    pc = prior_checks[cid]
148	                    prior_findings = []
149	                    flagged_count = sum(1 for f in pc.get("findings", []) if f.get("flagged"))
150	                    flagged_idx = 0
151	                    for f in pc.get("findings", []):
152	                        pf: dict[str, object] = {
153	                            "detail": f.get("detail", ""),
154	                            "flagged": f.get("flagged", False),
155	                        }
156	                        if f.get("flagged"):
157	                            flagged_idx += 1
158	                            fid = cid if flagged_count == 1 else f"{cid}-{flagged_idx}"
159	                            pf["status"] = flag_status.get(fid, flag_status.get(cid, "open"))
160	                        else:
161	                            pf["status"] = "n/a"
162	                        prior_findings.append(pf)
163	                    entry["prior_findings"] = prior_findings
164	    return checks_template
165	
166	
167	def _build_critique_prompt(
168	    state: PlanState,
169	    context: dict[str, Any],
170	    critique_review_block: str,
171	) -> str:
172	    return textwrap.dedent(
173	        f"""
174	        You are an independent reviewer. Critique the plan against the actual repository.
175	
176	        Project directory:
177	        {context["project_dir"]}
178	
179	        {context["prep_block"]}
180	
181	        {context["prep_instruction"]}
182	
183	        {intent_and_notes_block(state)}
184	
185	        Plan:
186	        {context["latest_plan"]}
187	
188	        Plan metadata:
189	        {json_dump(context["latest_meta"]).strip()}
190	
191	        Plan structure warnings from validator:
192	        {json_dump(context["structure_warnings"]).strip()}
193	
194	        Existing flags:
195	        {json_dump(context["unresolved"]).strip()}
196	
197	        {context["debt_block"]}
198	
199	        {critique_review_block}
200
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/auto.py",
  "offset": 200,
  "limit": 150
}
```

> TOOL

tool_result Read
```
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
290	                    last_phase=last_phase,
291	                    events=events,
292	                )
293	            log(f"no next_step and no override available (valid_next={valid_next})")
294	            return DriverOutcome(
295	                status="failed",
296	                plan=plan,
297	                final_state=state,
298	                iterations=iteration,
299	                reason="no next_step and no override available",
300	                last_phase=last_phase,
301	                events=events,
302	            )
303	
304	        # Run the next phase.
305	        cmd = _phase_command(next_step) + ["--plan", plan]
306	        log(f"running: megaplan {' '.join(cmd)}", phase=next_step, timeout=phase_timeout)
307	        last_phase = next_step
308	        code, out, err = _run_megaplan(cmd, cwd=cwd, timeout=phase_timeout)
309	        if code == PHASE_TIMEOUT_EXIT_CODE:
310	            log(f"phase '{next_step}' timed out after {phase_timeout}s — stall detection will enforce the cap")
311	        elif code != 0:
312	            # Don't bail immediately — megaplan often records a partial failure
313	            # in state.json and the next status() reveals a recoverable valid_next.
314	            # Stall detection will still kill infinite loops.
315	            log(f"phase '{next_step}' exited {code}: {err.strip() or out.strip()[-400:]}")
316	        if poll_sleep > 0:
317	            time.sleep(poll_sleep)
318	
319	    # Hit iteration cap.
320	    log(f"hit max_iterations={max_iterations}")
321	    return DriverOutcome(
322	        status="cap",
323	        plan=plan,
324	        final_state=last_state or "unknown",
325	        iterations=max_iterations,
326	        reason=f"exceeded max_iterations={max_iterations}",
327	        last_phase=last_phase,
328	        events=events,
329	    )
330	
331	
332	def build_auto_parser(subparsers: Any) -> None:
333	    auto_parser = subparsers.add_parser(
334	        "auto",
335	        help="Drive a plan to completion without human intervention",
336	    )
337	    auto_parser.add_argument("--plan", required=True, help="Plan name")
338	    auto_parser.add_argument(
339	        "--stall-threshold",
340	        type=int,
341	        default=DEFAULT_STALL_THRESHOLD,
342	        help=f"Exit if the plan state doesn't change for this many iterations (default {DEFAULT_STALL_THRESHOLD})",
343	    )
344	    auto_parser.add_argument(
345	        "--max-iterations",
346	        type=int,
347	        default=DEFAULT_MAX_ITERATIONS,
348	        help=f"Hard cap on loop iterations (default {DEFAULT_MAX_ITERATIONS})",
349	    )
```

> AGENT

Perfect. Now I have all the information needed. Let me compile the comprehensive report:

## Plan Review Report

Based on my analysis of the megaplan codebase, here's the detailed information you requested:

### 1. **megaplan/types.py** — States and Records

**File:** `/Users/user_c042661f/Documents/megaplan/megaplan/types.py`

**STATE_* Constants (Lines 12-23):**
- `STATE_INITIALIZED = "initialized"` (line 12)
- `STATE_PREPPED = "prepped"` (line 13)
- `STATE_PLANNED = "planned"` (line 14)
- `STATE_CRITIQUED = "critiqued"` (line 15)
- `STATE_GATED = "gated"` (line 16)
- `STATE_FINALIZED = "finalized"` (line 17)
- `STATE_EXECUTED = "executed"` (line 18)
- `STATE_DONE = "done"` (line 19)
- `STATE_ABORTED = "aborted"` (line 20)
- `STATE_AWAITING_HUMAN = "awaiting_human_verify"` (line 21)
- `TERMINAL_STATES = {STATE_DONE, STATE_ABORTED}` (line 22)
- `AUTOMATION_TERMINAL_STATES = TERMINAL_STATES | {STATE_AWAITING_HUMAN}` (line 23)

**FlagRecord (Lines 128-143):**
```python
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
```

**PlanConfig (Lines 30-35):**
```python
class PlanConfig(TypedDict, total=False):
    project_dir: str
    auto_approve: bool
    robustness: str
    agents: dict[str, str]
    workers: NotRequired[dict[str, Any]]
```

---

### 2. **megaplan/schemas.py** — Gate JSON Schema

**File:** `/Users/user_c042661f/Documents/megaplan/megaplan/schemas.py`

**Gate Schema Location:** Lines 114-171

**Recommendation Enum (Lines 117-120):**
```python
"recommendation": {
    "type": "string",
    "enum": ["PROCEED", "ITERATE", "ESCALATE"],
},
```

**Key Properties (Lines 114-171):**
- `recommendation` (required) — enum: PROCEED, ITERATE, ESCALATE (line 119)
- `rationale` (required) — string (line 121)
- `signals_assessment` (required) — string (line 122)
- `warnings` (required) — array of strings (line 123)
- `settled_decisions` (required) — array with `id`, `decision`, `rationale` (lines 124-135)
- `flag_resolutions` (required) — array with `flag_id`, `action` (dispute/accept_tradeoff), `evidence`, `rationale` (lines 136-147)
- `accepted_tradeoffs` (required) — array with `flag_id`, `concern`, `subsystem`, `rationale` (lines 149-161)

---

### 3. **megaplan/handlers.py** — Gate Handling

**File:** `/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py`

**`_apply_gate_outcome` Function (Lines 606-668):**
- **Location:** Lines 606-668
- **Signature:** `_apply_gate_outcome(state, gate_summary, *, robustness, plan_dir) → tuple[str, str, str, list[str]]`
- **Handles these recommendations:**
  - `PROCEED` (lines 617-651): Validates flag resolutions; checks blocking flags; if passed, transitions to STATE_GATED → "finalize". If PROCEED but preflight blocked, transitions to STATE_CRITIQUED → "revise".
  - `ITERATE` (lines 662-663): Returns "revise" action
  - `ESCALATE` (lines 664-665): Returns "override add-note" action
  - Unknown (lines 666-668): Treats as escalation

**`handle_gate` Function (Lines 1116-1235):**
- **Location:** Lines 1116-1235
- **Calling `_apply_gate_outcome`:** Lines 1148-1153
  - Builds gate signals from plan directory
  - Runs worker with "gate" step
  - Calls `_apply_gate_outcome(state, gate_summary, robustness=..., plan_dir=plan_dir)`
  - If blocking flags unresolved, runs reprompt (lines 1155-1193) and calls `_apply_gate_outcome` again
  - If still unresolved after reprompt, downgrade recommendation to ITERATE (lines 1195-1201)

---

### 4. **megaplan/_core/workflow.py** — Workflow and Transitions

**File:** `/Users/user_c042661f/Documents/megaplan/megaplan/_core/workflow.py`

**WORKFLOW Dict (Lines 32-71):**

| Current State | Next Steps (with conditions) | Result State |
|---|---|---|
| `STATE_INITIALIZED` (line 33) | `prep` | `STATE_PREPPED` |
| `STATE_PREPPED` (line 36) | `plan` | `STATE_PLANNED` |
| `STATE_PLANNED` (lines 39-42) | `critique` OR `plan` | `STATE_CRITIQUED` OR `STATE_PLANNED` |
| `STATE_CRITIQUED` (lines 43-52) | Multiple paths with conditions: `gate` (gate_unset) → `STATE_GATED`, `revise` (gate_iterate) → `STATE_PLANNED`, `override add-note` (gate_escalate), `override force-proceed` (gate_escalate or gate_proceed_blocked), `override abort` (gate_escalate), `revise` (gate_proceed_blocked), `gate` (gate_proceed) |
| `STATE_GATED` (lines 53-56) | `finalize` OR `override replan` | `STATE_FINALIZED` OR `STATE_PLANNED` |
| `STATE_FINALIZED` (lines 57-60) | `execute` OR `override replan` | `STATE_EXECUTED` OR `STATE_PLANNED` |
| `STATE_EXECUTED` (lines 61-67) | `review` | `STATE_DONE` |
| `STATE_AWAITING_HUMAN` (lines 68-70) | `verify-human` | `STATE_DONE` |

**Robustness Overrides (Lines 78-105):**
- `standard`: Skips prep directly to `plan` (lines 82-84)
- `light`: Skips prep + modifies STATE_CRITIQUED revise behavior (lines 86-94)
- `tiny`: Inherits from light (line 95)

**Condition Matching Function (Lines 175-192):** `_transition_matches()` evaluates:
- `gate_unset` — no recommendation set
- `gate_iterate` — recommendation == "ITERATE"
- `gate_escalate` — recommendation == "ESCALATE"
- `gate_proceed_blocked` — recommendation == "PROCEED" AND NOT passed
- `gate_proceed` — recommendation == "PROCEED" AND passed

---

### 5. **megaplan/_core/registries.py** — Utility Functions

**File:** `/Users/user_c042661f/Documents/megaplan/megaplan/_core/registries.py`

**`_concern_word_set` Function (Lines 106-111):**
- **Visibility:** Private (leading underscore)
- **Purpose:** Tokenizes a concern string into normalized lowercase words
- **Implementation:** `re.split(r"[^a-z0-9]+", normalize_text(concern))` — splits on non-alphanumeric, filters empty tokens

**`_jaccard_similarity` Function (Lines 114-120):**
- **Visibility:** Private (leading underscore)
- **Purpose:** Computes set intersection over union similarity between two word sets
- **Implementation:** Returns `len(left & right) / len(union)` if union is non-empty; else 0.0
- **Used in:** `find_matching_debt()` to detect duplicate concerns across flag entries

---

### 6. **megaplan/prompts/gate.py** — Gate Prompt

**File:** `/Users/user_c042661f/Documents/megaplan/megaplan/prompts/gate.py`

**`_gate_prompt` Function (Lines 24-135):**
- **Location:** Lines 24-135

**Structure:**
- Preamble: "You are the gatekeeper..." (line 67)
- Project directory (line 69-70)
- Intent and notes block (line 72)
- Plan text (lines 74-75)
- Plan metadata (lines 77-78)
- Gate signals (lines 80-81)
- Critique checks summary (lines 83)
- Unresolved significant flags (lines 85-86)
- Debt block (line 88)
- Robustness level (lines 90-91)

**Requirements Section (Lines 93-116):**
- Line 93: `# Requirements:` header
- Lines 94-99: Core logic (choose PROCEED/ITERATE/ESCALATE, use signals as context)
- Lines 101-115: Flag handling rules (blocking vs. noted, dispute vs. accept_tradeoff with evidence/rationale requirements, structured JSON output)

**Debt Block (Line 88 reference, no explicit "debt" label):** Imported from `_shared._gate_debt_block()`

**Example Output (Lines 118-133):** Shows PROCEED with flag_resolutions including dispute + accept_tradeoff entries with proper evidence/rationale fields.

---

### 7. **megaplan/prompts/critique.py** — Critique and Revise Prompts

**File:** `/Users/user_c042661f/Documents/megaplan/megaplan/prompts/critique.py`

**`_critique_context` Function (Lines 87-114):**
- **Returns:** dict with keys: `project_dir`, `prep_block`, `prep_instruction`, `latest_plan`, `latest_meta`, `structure_warnings`, `unresolved`, `debt_block`, `robustness`
- **Builds context for critique by reading plan, prep, metadata, and prior flag registry**

**`_build_critique_prompt` Function (Lines 167-199):**
- **Signature:** `_build_critique_prompt(state, context, critique_review_block) → str`
- **Constructs:** Preamble + project_dir + prep_block + prep_instruction + intent/notes + plan + meta + structure_warnings + unresolved flags + debt_block + critique_review_block
- **Location:** Lines 167-200+ (extends beyond excerpt)

**`_revise_prompt` Function (Lines 27-84):**
- **Purpose:** Post-gate revision prompt when ITERATE is recommended
- **Reads:** Latest plan, metadata, gate.json, unresolved flags
- **Requirements section (Lines 68-80):**
  - Check if plan targets wrong code/cause (line 69)
  - Update to address significant issues (line 70)
  - Return flags_addressed with exact IDs (line 72)
  - Include changes_summary (line 73)
  - Preserve/improve success_criteria with priority and requires fields (lines 74-75)
  - Validate alignment with user intent (line 76)
  - Remove unjustified scope growth (line 77)
  - Maintain structural template (line 78)
  - CRITICAL: Output plan markdown in JSON `plan` field only (lines 79-80)

---

### 8. **megaplan/tiebreaker.py** — Tiebreaker Implementation

**File:** `/Users/user_c042661f/Documents/megaplan/megaplan/tiebreaker.py`

**Functions/Classes Present (Lines 1-264):**
- `_next_version_suffix()` (lines 32-41) — Version suffixes for multiple runs
- `_run_tiebreaker()` (lines 49-140) — **Main orchestrator** (see below)
- `_build_resolved()` (lines 143-150) — Build agent/mode tuple
- `_resolve_question()` (lines 153-163) — Extract decision question
- `_run_tiebreaker_status()` (lines 171-200) — Status reporting
- `_add_common_agent_args()` (lines 208-231) — CLI arg builder
- `build_tiebreaker_parser()` (lines 234-252) — **Parser builder** (see below)
- `run_tiebreaker_cli()` (lines 254-264) — CLI entry point

**`_run_tiebreaker` Function (Lines 49-140):**
- **Does not exist in exact name; this is the main dispatch**
- Runs researcher agent (lines 66-86)
- Runs challenger agent (lines 94-115)
- Runs synthesis (lines 118-120)
- Returns JSON payload with success/artifacts

**`build_tiebreaker_parser` Function (Lines 234-252):**
- **Location:** Lines 234-252
- **Creates subparser for `tiebreaker` command**
- **Arguments:**
  - `--plan` (line 242)
  - `--question` XOR `--question-file` (lines 243-245)
  - `--output` (line 246)
  - Common agent args (line 247): `--agent`, `--hermes`, `--phase-model`, `--fresh`, `--persist`, `--ephemeral`
- **Subcommands:** `status` (line 250)

---

### 9. **megaplan/cli.py** — Tiebreaker Integration

**File:** `/Users/user_c042661f/Documents/megaplan/megaplan/cli.py`

**Tiebreaker Integration (Lines 980-981, 1084-1088):**
- **Parser registration (lines 980-981):**
  ```python
  from megaplan.tiebreaker import build_tiebreaker_parser
  build_tiebreaker_parser(subparsers)
  ```
- **Command dispatch (lines 1084-1088):**
  ```python
  if args.command == "tiebreaker":
      from megaplan.tiebreaker import run_tiebreaker_cli
      try:
          return run_tiebreaker_cli(root, args)
      except CliError as error:
          return error_response(error, root=root)
  ```

---

### 10. **megaplan/auto.py** — Auto Runner Dispatch

**File:** `/Users/user_c042661f/Documents/megaplan/megaplan/auto.py`

**How Auto Runner Uses Workflow (Lines 1-330):**

1. **Status Polling (Lines 101-110):** Calls `megaplan status` to get current `state` and `next_step`
   
2. **Terminal Detection (Lines 185-207):** Checks if state in `AUTOMATION_TERMINAL_STATES`
   
3. **Stall Detection (Lines 209-228):** Detects repeated state (no progress)
   
4. **Escalation Handling (Lines 230-302):**
   - If no `next_step` and `override force-proceed` in `valid_next`:
     - Respects `--on-escalate` flag (force-proceed/abort/fail)
     - Lines 234-258: force-proceed override
     - Lines 259-281: abort override
     - Lines 282-292: fail (human required)
   
5. **Phase Dispatch (Lines 304-308):**
   - Translates `next_step` to CLI args via `_phase_command()` (lines 117-125)
   - Runs `megaplan [next_step] --plan [plan]` in subprocess (lines 85-98)
   - **Does NOT directly call handlers** — shells out to fresh CLI instance each iteration
   
6. **Iteration Loop (Lines 158-329):**
   - For loop with max_iterations cap (line 158)
   - Each iteration: status → validate → run phase → sleep
   - **Uses workflow transitions implicitly via status.next_step**

**Key Design:**
- Auto driver is "intentionally dumb" (line 12) — all logic delegated to phase handlers
- Shelling out ensures fresh argparse/state (lines 72-76)
- Status output drives transitions (no direct workflow dict usage in auto.py)
- Escalation defaults to force-proceed but respects caller's `--on-escalate` option (lines 134, 146)

---

### Summary

The plan architecture flows as follows:

1. **States & Transitions:** 9 states managed by `WORKFLOW` dict; transitions conditional on `last_gate.recommendation` values
2. **Gate Logic:** Recommendations (PROCEED/ITERATE/ESCALATE) evaluated in `_apply_gate_outcome()` → routes to finalize/revise/escalation
3. **Flag Handling:** Blocking flags require explicit dispute or accept_tradeoff with evidence/rationale; rubber-stamp resolutions rejected
4. **Tiebreaker:** Separate orchestrator for architectural questions; researcher → challenger → synthesis pipeline
5. **Auto Driver:** Shells out per phase, polls status for next_step, applies escalation override logic, detects stalls
6. **Robustness Levels:** affect prep inclusion and gate/review strictness via `_ROBUSTNESS_OVERRIDES`

All critical logic (gate validation, flag triage, workflow routing) is in handlers, not auto. Auto is a mechanical state machine reader.
