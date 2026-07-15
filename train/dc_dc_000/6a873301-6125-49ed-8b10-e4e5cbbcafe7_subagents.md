> DEVELOPER

I need to understand the current state of these files for a finalize briefing. Report back concise summaries of:

1. megaplan/types.py - what states exist, what's FlagRecord, what's PlanConfig, line numbers for each
2. megaplan/schemas.py - where gate.json schema is defined, line numbers for recommendation enum
3. megaplan/handlers.py - where handle_gate is, where _apply_gate_outcome is, key line numbers
4. megaplan/_core/workflow.py - where WORKFLOW dict is, where _transition_matches is, line numbers
5. megaplan/_core/registries.py - where _jaccard_similarity and _concern_word_set are, line numbers
6. megaplan/prompts/gate.py - where _gate_prompt is, line numbers
7. megaplan/prompts/critique.py - where _critique_context and _build_critique_prompt are, line numbers
8. megaplan/cli.py - where subparsers are set up, line numbers
9. megaplan/auto.py - where AUTOMATION_TERMINAL_STATES is used, _phase_command, line numbers
10. megaplan/tiebreaker.py - what exists, key functions, line numbers
11. pyproject.toml - current version
12. tests/ - what test files exist

Be thorough - read each file and report specific line numbers.

> AGENT

I'll systematically explore each of these files to provide you with detailed line numbers and summaries. Let me start by reading all the key files.

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
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/registries.py"
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
101	    if not separator:
102	        return "untagged"
103	    return _normalize_subsystem_tag(prefix)
104	
105	
106	def _concern_word_set(concern: str) -> set[str]:
107	    return {
108	        token
109	        for token in re.split(r"[^a-z0-9]+", normalize_text(concern))
110	        if token
111	    }
112	
113	
114	def _jaccard_similarity(left: set[str], right: set[str]) -> float:
115	    if not left or not right:
116	        return 0.0
117	    union = left | right
118	    if not union:
119	        return 0.0
120	    return len(left & right) / len(union)
121	
122	
123	def find_matching_debt(registry: DebtRegistry, subsystem: str, concern: str) -> DebtEntry | None:
124	    normalized_subsystem = _normalize_subsystem_tag(subsystem)
125	    concern_words = _concern_word_set(concern)
126	    for entry in registry["entries"]:
127	        if entry["resolved"]:
128	            continue
129	        if entry["subsystem"] != normalized_subsystem:
130	            continue
131	        if _jaccard_similarity(_concern_word_set(entry["concern"]), concern_words) > 0.5:
132	            return entry
133	    return None
134	
135	
136	def add_or_increment_debt(
137	    registry: DebtRegistry,
138	    subsystem: str,
139	    concern: str,
140	    flag_ids: list[str],
141	    plan_id: str,
142	) -> DebtEntry:
143	    normalized_subsystem = _normalize_subsystem_tag(subsystem)
144	    normalized_concern = normalize_text(concern)
145	    timestamp = now_utc()
146	    existing = find_matching_debt(registry, normalized_subsystem, normalized_concern)
147	    if existing is not None:
148	        existing["occurrence_count"] += 1
149	        existing["updated_at"] = timestamp
150	        for flag_id in flag_ids:
151	            if flag_id not in existing["flag_ids"]:
152	                existing["flag_ids"].append(flag_id)
153	        if plan_id not in existing["plan_ids"]:
154	            existing["plan_ids"].append(plan_id)
155	        return existing
156	
157	    entry: DebtEntry = {
158	        "id": next_debt_id(registry),
159	        "subsystem": normalized_subsystem,
160	        "concern": normalized_concern,
161	        "flag_ids": list(dict.fromkeys(flag_ids)),
162	        "plan_ids": [plan_id],
163	        "occurrence_count": 1,
164	        "created_at": timestamp,
165	        "updated_at": timestamp,
166	        "resolved": False,
167	        "resolved_by": None,
168	        "resolved_at": None,
169	    }
170	    registry["entries"].append(entry)
171	    return entry
172	
173	
174	def resolve_debt(registry: DebtRegistry, debt_id: str, plan_id: str) -> DebtEntry:
175	    from megaplan.types import CliError
176	
177	    for entry in registry["entries"]:
178	        if entry["id"] != debt_id:
179	            continue
180	        timestamp = now_utc()
181	        entry["resolved"] = True
182	        entry["resolved_by"] = plan_id
183	        entry["resolved_at"] = timestamp
184	        entry["updated_at"] = timestamp
185	        return entry
186	    raise CliError("missing_debt", f"Debt entry '{debt_id}' does not exist")
187	
188	
189	def debt_by_subsystem(registry: DebtRegistry) -> dict[str, list[DebtEntry]]:
190	    grouped: dict[str, list[DebtEntry]] = {}
191	    for entry in registry["entries"]:
192	        if entry["resolved"]:
193	            continue
194	        grouped.setdefault(entry["subsystem"], []).append(entry)
195	    return grouped
196	
197	
198	def subsystem_occurrence_total(entries: list[DebtEntry]) -> int:
199	    return sum(entry["occurrence_count"] for entry in entries)
200	
201	
202	def escalated_subsystems(registry: DebtRegistry) -> list[tuple[str, int, list[DebtEntry]]]:
203	    escalated: list[tuple[str, int, list[DebtEntry]]] = []
204	    for subsystem, entries in debt_by_subsystem(registry).items():
205	        total = subsystem_occurrence_total(entries)
206	        if total >= DEBT_ESCALATION_THRESHOLD:
207	            escalated.append((subsystem, total, entries))
208	    escalated.sort(key=lambda item: (-item[1], item[0]))
209	    return escalated
210
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/gate.py"
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

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/critique.py"
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
201	        Additional guidelines:
202	        - Robustness level: {context["robustness"]}. {robustness_critique_instruction(context["robustness"])}
203	        - Over-engineering: prefer the simplest approach that fully solves the problem.
204	        - Reuse existing flag IDs when the same concern is still open.
205	        - `verified_flag_ids`: list flag IDs from prior iterations that the revised plan actually resolves (e.g., if the plan was revised to fix FLAG-001, and you confirm the fix is correct, include "FLAG-001"). Only include flags you've verified — don't guess.
206	        - Verify that the plan follows the expected structure when validator warnings or the outline suggest drift.
207	        - Additional flags may use these categories: correctness, security, completeness, performance, maintainability, other.
208	        - Focus on concrete issues, not structural formatting.
209	        """
210	    ).strip()
211	
212	
213	def _write_critique_template(
214	    plan_dir: Path,
215	    state: PlanState,
216	    checks: tuple[dict[str, Any], ...],
217	) -> Path:
218	    """Write the critique output template file and return its path.
219	
220	    The file serves as both guide (check questions + guidance) and output
221	    (findings arrays to fill in). This is the model's sole output channel.
222	    """
223	    import json
224	
225	    template: dict[str, object] = {
226	        "checks": _build_checks_template(plan_dir, state, checks),
227	        "flags": [],
228	        "verified_flag_ids": [],
229	        "disputed_flag_ids": [],
230	    }
231	
232	    output_path = plan_dir / "critique_output.json"
233	    output_path.write_text(json.dumps(template, indent=2), encoding="utf-8")
234	    return output_path
235	
236	
237	def write_single_check_template(
238	    plan_dir: Path,
239	    state: PlanState,
240	    check: dict[str, Any],
241	    output_name: str,
242	) -> Path:
243	    import json
244	
245	    template: dict[str, object] = {
246	        "checks": _build_checks_template(plan_dir, state, (check,)),
247	        "flags": [],
248	        "verified_flag_ids": [],
249	        "disputed_flag_ids": [],
250	    }
251	
252	    output_path = plan_dir / output_name
253	    output_path.write_text(json.dumps(template, indent=2), encoding="utf-8")
254	    return output_path
255	
256	
257	def _critique_prompt(state: PlanState, plan_dir: Path, root: Path | None = None) -> str:
258	    context = _critique_context(state, plan_dir, root)
259	    active_checks = checks_for_robustness(context["robustness"])
260	    # Write the template file — this is both the guide and the output
261	    output_path = _write_critique_template(plan_dir, state, active_checks)
262	    iteration = state.get("iteration", 1)
263	
264	    if active_checks:
265	        iteration_context = ""
266	        if iteration > 1:
267	            iteration_context = (
268	                "\n\n            This is critique iteration {iteration}. "
269	                "The template file includes prior findings with their status. "
270	                "Verify addressed flags were actually fixed, re-flag if inadequate, "
271	                "and check for new issues introduced by the revision."
272	            ).format(iteration=iteration)
273	        critique_review_block = textwrap.dedent(
274	            f"""
275	            Your output template is at: {output_path}
276	            Read this file first — it contains {len(active_checks)} checks, each with a question and guidance.
277	            For each check, investigate the codebase, then add your findings to the `findings` array for that check.
278	
279	            Each finding needs:
280	            - "detail": what you specifically checked and what you found (at least a full sentence)
281	            - "flagged": true if this describes a difference, risk, or tension — even if you think it's justified. false only if purely informational with no possible downside.
282	            - Every check must end with at least one finding. Never leave a `findings` array empty. If you found no issue, add one detailed `flagged: false` finding explaining what you checked and why it appears clear.
283	
284	            When in doubt, flag it — the gate can accept tradeoffs, but it can't act on findings it never sees.
285	
286	            Good: {{"detail": "Checked callers of nthroot_mod in solveset.py line 1205 — passes prime moduli only, consistent with the fix.", "flagged": false}}
287	            Good: {{"detail": "The fix handles empty tuples but not single-element tuples which need a trailing comma.", "flagged": true}}
288	            Bad: {{"detail": "No issue found", "flagged": false}}  ← too brief, will be rejected
289	            Bad: {{"detail": "The hints suggest approach X but the plan uses Y. However Y is consistent with X's intent.", "flagged": false}}  ← a different approach than the hints IS a flag. You found a divergence — flag it. The gate decides if it's acceptable.
290	
291	            After filling in checks, add any additional concerns to the `flags` array (e.g., security, performance, dependencies).
292	            Use the standard format (id, concern, category, severity_hint, evidence). This array can be empty.
293	
294	            Workflow: read the file → investigate → read file again → add finding → write file back. Repeat for each check.{iteration_context}
295	        """
296	        ).strip()
297	    else:
298	        critique_review_block = textwrap.dedent(
299	            f"""
300	            Your output template is at: {output_path}
301	            Review the plan with a broad scope. Consider whether the approach is correct, whether it covers
302	            all the places it needs to, whether it would break callers or violate codebase conventions,
303	            and whether its verification strategy is adequate.
304	
305	            Place any concrete concerns in the `flags` array in the template file using the standard format
306	            (id, concern, category, severity_hint, evidence). Leave `checks` as an empty array.
307	
308	            Workflow: read the file → investigate → read file again → add findings → write file back.
309	        """
310	        ).strip()
311	    return _build_critique_prompt(state, context, critique_review_block)
312	
313	
314	def single_check_critique_prompt(
315	    state: PlanState,
316	    plan_dir: Path,
317	    root: Path | None,
318	    check: dict[str, Any],
319	    template_path: Path,
320	) -> str:
321	    context = _critique_context(state, plan_dir, root)
322	    iteration = state.get("iteration", 1)
323	    iteration_context = ""
324	    if iteration > 1:
325	        iteration_context = (
326	            "\n\n            This is critique iteration {iteration}. "
327	            "The template file includes prior findings with their status. "
328	            "Verify addressed flags were actually fixed, re-flag if inadequate, "
329	            "and check for new issues introduced by the revision."
330	        ).format(iteration=iteration)
331	    critique_review_block = textwrap.dedent(
332	        f"""
333	        Your output template is at: {template_path}
334	        Read this file first — it contains 1 check with a question and guidance.
335	        Investigate only this check, then add your findings to the `findings` array for that check.
336	
337	        Check ID: {check["id"]}
338	        Question: {check["question"]}
339	        Guidance: {check.get("guidance", "")}
340	
341	        Each finding needs:
342	        - "detail": what you specifically checked and what you found (at least a full sentence)
343	        - "flagged": true if this describes a difference, risk, or tension — even if you think it's justified. false only if purely informational with no possible downside.
344	        - This check must end with at least one finding. Never leave its `findings` array empty. If you found no issue, add one detailed `flagged: false` finding explaining what you checked and why it appears clear.
345	
346	        When in doubt, flag it — the gate can accept tradeoffs, but it can't act on findings it never sees.
347	
348	        Good: {{"detail": "Checked callers of nthroot_mod in solveset.py line 1205 — passes prime moduli only, consistent with the fix.", "flagged": false}}
349	        Good: {{"detail": "The fix handles empty tuples but not single-element tuples which need a trailing comma.", "flagged": true}}
350	        Bad: {{"detail": "No issue found", "flagged": false}}  ← too brief, will be rejected
351	        Bad: {{"detail": "The hints suggest approach X but the plan uses Y. However Y is consistent with X's intent.", "flagged": false}}  ← a different approach than the hints IS a flag. You found a divergence — flag it. The gate decides if it's acceptable.
352	
353	        After filling in checks, add any additional concerns to the `flags` array (e.g., security, performance, dependencies).
354	        Use the standard format (id, concern, category, severity_hint, evidence). This array can be empty.
355	
356	        Workflow: read the file → investigate → read file again → add finding → write file back. Repeat for this check.{iteration_context}
357	    """
358	    ).strip()
359	    return _build_critique_prompt(state, context, critique_review_block)
360
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/cli.py"
}
```

> TOOL

tool_result Read
```
File content (13190 tokens) exceeds maximum allowed tokens (10000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/auto.py"
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
350	    auto_parser.add_argument(
351	        "--on-escalate",
352	        choices=ESCALATE_ACTIONS,
353	        default="force-proceed",
354	        help="What to do when the gate escalates (default force-proceed)",
355	    )
356	    auto_parser.add_argument(
357	        "--poll-sleep",
358	        type=float,
359	        default=DEFAULT_POLL_SLEEP_SECONDS,
360	        help=f"Seconds to sleep between phase transitions (default {DEFAULT_POLL_SLEEP_SECONDS})",
361	    )
362	    auto_parser.add_argument(
363	        "--phase-timeout",
364	        type=float,
365	        default=DEFAULT_PHASE_TIMEOUT_SECONDS,
366	        help=(
367	            f"Seconds before a single phase subprocess (plan/prep/critique/gate/finalize/execute/review) "
368	            f"is killed and treated as a failure (default {DEFAULT_PHASE_TIMEOUT_SECONDS}s). "
369	            "Stall detection still applies on top."
370	        ),
371	    )
372	    auto_parser.add_argument(
373	        "--status-timeout",
374	        type=float,
375	        default=DEFAULT_STATUS_TIMEOUT_SECONDS,
376	        help=(
377	            f"Seconds before `megaplan status` / override subprocesses are killed "
378	            f"(default {DEFAULT_STATUS_TIMEOUT_SECONDS}s). These should always be quick; "
379	            "hitting this indicates serious trouble."
380	        ),
381	    )
382	
383	
384	def run_auto(root: Path, args: argparse.Namespace) -> int:
385	    """CLI entry point. Returns a POSIX exit code suitable for ``sys.exit``."""
386	    outcome = drive(
387	        args.plan,
388	        cwd=root,
389	        stall_threshold=args.stall_threshold,
390	        max_iterations=args.max_iterations,
391	        on_escalate=args.on_escalate,
392	        poll_sleep=args.poll_sleep,
393	        phase_timeout=args.phase_timeout,
394	        status_timeout=args.status_timeout,
395	    )
396	    sys.stdout.write(outcome.to_json() + "\n")
397	    if outcome.status == "done":
398	        return 0
399	    if outcome.status == "aborted":
400	        return 0  # user-requested abort is not a failure
401	    if outcome.status == "stalled":
402	        return 2
403	    if outcome.status == "escalated":
404	        return 3
405	    if outcome.status == "cap":
406	        return 4
407	    return 1
408
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/tiebreaker.py"
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

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/pyproject.toml"
}
```

> TOOL

tool_result Read
```
1	[build-system]
2	requires = ["hatchling"]
3	build-backend = "hatchling.build"
4	
5	[project]
6	name = "megaplan-harness"
7	version = "0.17.0"
8	description = "AI agent harness for coordinating Claude and GPT to make and execute extremely robust plans"
9	requires-python = ">=3.11"
10	license = { text = "OSNL-0.2" }
11	authors = [
12	    { name = "Peter [REDACTED]" },
13	]
14	keywords = ["ai", "planning", "orchestration", "claude", "codex"]
15	classifiers = [
16	    "Development Status :: 3 - Alpha",
17	    "Environment :: Console",
18	    "Intended Audience :: Developers",
19	    "Topic :: Software Development :: Quality Assurance",
20	]
21	dependencies = [
22	    "PyYAML>=6.0",
23	]
24	
25	[project.scripts]
26	megaplan = "megaplan.cli:cli_entry"
27	
28	[tool.hatch.build.targets.wheel]
29	packages = ["megaplan"]
30	
31	[tool.pytest.ini_options]
32	testpaths = ["tests"]
33
```

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/megaplan/tests/**/*.py"
}
```

> TOOL

tool_result Glob
```
tests/__init__.py
tests/test_core.py
tests/test_quality.py
tests/test_loop.py
tests/test_swe_bench.py
tests/test_evaluation.py
tests/test_io_git_patch.py
tests/test_review_mechanical.py
tests/test_parallel_critique.py
tests/test_workers.py
tests/test_checks.py
tests/test_review_checks.py
tests/test_config.py
tests/test_handle_review_robustness.py
tests/test_parallel_review.py
tests/test_doc_mode.py
tests/test_chain.py
tests/test_prompts.py
tests/test_tiny_robustness.py
tests/test_verifiability.py
tests/test_megaplan.py
tests/test_tiebreaker.py
tests/test_schemas.py
```

> AGENT

Now let me get the handlers.py file in parts to capture the key functions:

> TOOL

tool_use Grep
```json
{
  "pattern": "^def handle_gate",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "output_mode": "content"
}
```

> TOOL

tool_result Grep
```
1116:def handle_gate(root: Path, args: argparse.Namespace) -> StepResponse:
```

> TOOL

tool_use Grep
```json
{
  "pattern": "^def _apply_gate_outcome",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "output_mode": "content"
}
```

> TOOL

tool_result Grep
```
606:def _apply_gate_outcome(
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/cli.py",
  "limit": 300
}
```

> TOOL

tool_result Read
```
1	#!/usr/bin/env python3
2	from __future__ import annotations
3	
4	import argparse
5	import os
6	import sys
7	from datetime import datetime, timezone
8	from importlib import resources
9	from pathlib import Path
10	from typing import Any, Callable
11	
12	from megaplan.types import (
13	    CliError,
14	    DEFAULT_AGENT_ROUTING,
15	    DEFAULTS,
16	    KNOWN_AGENTS,
17	    ROBUSTNESS_LEVELS,
18	    StepResponse,
19	    TERMINAL_STATES,
20	    _SETTABLE_BOOL,
21	    _SETTABLE_ENUM,
22	    _SETTABLE_NUMERIC,
23	)
24	from megaplan._core import (
25	    active_plan_dirs,
26	    add_or_increment_debt,
27	    atomic_write_text,
28	    build_next_step_runtime,
29	    build_phase_observability,
30	    compute_global_batches,
31	    config_dir,
32	    detect_available_agents,
33	    escalated_subsystems,
34	    ensure_runtime_layout,
35	    get_effective,
36	    infer_next_steps,
37	    json_dump,
38	    load_config,
39	    load_debt_registry,
40	    load_plan,
41	    plan_lock_is_held,
42	    read_json,
43	    resolve_debt,
44	    resolve_plan_dir,
45	    save_debt_registry,
46	    save_config,
47	    subsystem_occurrence_total,
48	    humanize_seconds,
49	)
50	from megaplan.execution import build_monitor_hint
51	from megaplan.handlers import (
52	    handle_audit_verifiability,
53	    handle_critique,
54	    handle_execute,
55	    handle_finalize,
56	    handle_gate,
57	    handle_init,
58	    handle_override,
59	    handle_plan,
60	    handle_prep,
61	    handle_review,
62	    handle_revise,
63	    handle_verify_human,
64	)
65	from megaplan.loop.handlers import (
66	    handle_loop_init,
67	    handle_loop_pause,
68	    handle_loop_run,
69	    handle_loop_status,
70	)
71	from megaplan.step_edit import handle_step
72	
73	
74	def render_response(response: StepResponse, *, exit_code: int = 0) -> int:
75	    print(json_dump(response), end="")
76	    return exit_code
77	
78	
79	def _resolve_error_plan_dir(root: Path | None, error: CliError) -> Path | None:
80	    if root is None or error.code != "plan_locked" or not isinstance(error.extra, dict):
81	        return None
82	    plan_name = error.extra.get("plan")
83	    if not isinstance(plan_name, str) or not plan_name:
84	        return None
85	    try:
86	        return resolve_plan_dir(root, plan_name)
87	    except CliError:
88	        return None
89	
90	
91	def _augment_plan_locked_error(
92	    payload: StepResponse,
93	    error: CliError,
94	    *,
95	    root: Path | None,
96	) -> None:
97	    plan_dir = _resolve_error_plan_dir(root, error)
98	    details = payload.get("details")
99	    if not isinstance(details, dict):
100	        details = None
101	    plan_name = (details or {}).get("plan")
102	    if isinstance(plan_name, str) and plan_name:
103	        monitor_hint = build_monitor_hint(plan_dir or Path(plan_name))
104	        payload["monitor_hint"] = monitor_hint
105	        if details is not None:
106	            details["monitor_hint"] = monitor_hint
107	    raw_active_step = (details or {}).get("active_step")
108	    if isinstance(raw_active_step, dict):
109	        active_step = (
110	            _build_active_step(raw_active_step, plan_dir=plan_dir)
111	            if plan_dir is not None
112	            else dict(raw_active_step)
113	        )
114	        payload["active_step"] = active_step
115	        if details is not None:
116	            details["active_step"] = active_step
117	
118	
119	def error_response(error: CliError, *, root: Path | None = None) -> int:
120	    payload: StepResponse = {
121	        "success": False,
122	        "error": error.code,
123	        "message": error.message,
124	    }
125	    if error.valid_next:
126	        payload["valid_next"] = error.valid_next
127	    if error.extra:
128	        payload["details"] = dict(error.extra)
129	    if error.code == "plan_locked":
130	        _augment_plan_locked_error(payload, error, root=root)
131	    return render_response(payload, exit_code=error.exit_code)
132	
133	
134	def _parse_utc_timestamp(timestamp: str | None) -> datetime | None:
135	    if not isinstance(timestamp, str) or not timestamp:
136	        return None
137	    try:
138	        return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
139	    except ValueError:
140	        return None
141	
142	
143	def _build_progress_payload(plan_dir: Path, state: dict[str, Any]) -> dict[str, Any]:
144	    finalize_path = plan_dir / "finalize.json"
145	    if not finalize_path.exists():
146	        return {
147	            "summary": "No finalize.json yet — plan has not been finalized.",
148	            "tasks_total": 0,
149	            "tasks_done": 0,
150	            "tasks_skipped": 0,
151	            "tasks_pending": 0,
152	            "batches_total": 0,
153	            "batches_completed": 0,
154	            "tasks": [],
155	        }
156	    finalize_data = read_json(finalize_path)
157	    global_batches = compute_global_batches(finalize_data)
158	    tasks = finalize_data.get("tasks", [])
159	    task_id_to_batch: dict[str, int] = {}
160	    for batch_idx, batch_ids in enumerate(global_batches, start=1):
161	        for task_id in batch_ids:
162	            task_id_to_batch[task_id] = batch_idx
163	    tasks_done = sum(1 for t in tasks if t.get("status") == "done")
164	    tasks_skipped = sum(1 for t in tasks if t.get("status") == "skipped")
165	    tasks_pending = sum(1 for t in tasks if t.get("status") == "pending")
166	    tasks_total = len(tasks)
167	    completed_ids = {
168	        t["id"] for t in tasks if t.get("status") in {"done", "skipped"} and isinstance(t.get("id"), str)
169	    }
170	    batches_completed = sum(
171	        1
172	        for batch_ids in global_batches
173	        if all(tid in completed_ids for tid in batch_ids)
174	    )
175	    task_status_list = [
176	        {
177	            "id": t.get("id", ""),
178	            "status": t.get("status", "pending"),
179	            "batch": task_id_to_batch.get(t.get("id", ""), 0),
180	        }
181	        for t in tasks
182	    ]
183	    return {
184	        "summary": (
185	            f"Execution progress: {tasks_done + tasks_skipped}/{tasks_total} tasks tracked, "
186	            f"{batches_completed}/{len(global_batches)} batches completed. "
187	            "Progress reflects the last finalize.json write (between-batch granularity)."
188	        ),
189	        "tasks_total": tasks_total,
190	        "tasks_done": tasks_done,
191	        "tasks_skipped": tasks_skipped,
192	        "tasks_pending": tasks_pending,
193	        "batches_total": len(global_batches),
194	        "batches_completed": batches_completed,
195	        "tasks": task_status_list,
196	    }
197	
198	
199	def _build_last_step(state: dict[str, Any]) -> dict[str, Any] | None:
200	    history = state.get("history", [])
201	    if not isinstance(history, list) or not history:
202	        return None
203	    last = history[-1]
204	    if not isinstance(last, dict):
205	        return None
206	    return {
207	        "step": last.get("step"),
208	        "result": last.get("result"),
209	        "timestamp": last.get("timestamp"),
210	        "agent": last.get("agent"),
211	        "output_file": last.get("output_file"),
212	    }
213	
214	
215	def _build_active_step(active_step: Any, *, plan_dir: Path) -> dict[str, Any] | None:
216	    if not isinstance(active_step, dict):
217	        return None
218	    details = dict(active_step)
219	    step = details.get("step")
220	    if not isinstance(step, str) or not step:
221	        return details
222	    configured_timeout_seconds = int(get_effective("execution", "worker_timeout_seconds"))
223	    lock_held = plan_lock_is_held(plan_dir)
224	    started_at = _parse_utc_timestamp(details.get("started_at"))
225	    if started_at is not None:
226	        age_seconds = max(0, int((datetime.now(timezone.utc) - started_at).total_seconds()))
227	        details.update(
228	            build_phase_observability(
229	                step,
230	                configured_timeout_seconds=configured_timeout_seconds,
231	                age_seconds=age_seconds,
232	                lock_held=lock_held,
233	            )
234	        )
235	        if details.get("stale"):
236	            orphaned = not lock_held
237	            details["orphaned"] = orphaned
238	            if orphaned:
239	                if step == "execute":
240	                    details["recovery_hint"] = (
241	                        "The active step is stale and no process holds the plan lock. "
242	                        "Safe next action: rerun the same execute command on Codex without --fresh."
243	                    )
244	                else:
245	                    details["recovery_hint"] = (
246	                        "The active step is stale and no process holds the plan lock. "
247	                        "Safe next action: rerun the same step on the same agent before escalating."
248	                    )
249	        max_seconds = int(details.get("expected_duration_seconds", {}).get("max", 0) or 0)
250	        elapsed_label = humanize_seconds(age_seconds)
251	        if details.get("stale"):
252	            details["phase_progress_summary"] = (
253	                f"{step} stale ({elapsed_label} elapsed, expected max {humanize_seconds(max_seconds)}) "
254	                "see recovery_hint."
255	            )
256	        elif step in {"execute", "loop_execute"}:
257	            details["phase_progress_summary"] = (
258	                f"{step} running ({elapsed_label} elapsed, use progress for batch-level detail)."
259	            )
260	        else:
261	            details["phase_progress_summary"] = (
262	                f"{step} running ({elapsed_label} elapsed, typically completes within "
263	                f"{humanize_seconds(max_seconds)})."
264	            )
265	            if max_seconds > 0:
266	                details["progress_pct"] = min(95, int((age_seconds / max_seconds) * 100))
267	    else:
268	        details.update(
269	            build_phase_observability(
270	                step,
271	                configured_timeout_seconds=configured_timeout_seconds,
272	                lock_held=lock_held,
273	            )
274	        )
275	        if step in {"execute", "loop_execute"}:
276	            details["phase_progress_summary"] = (
277	                f"{step} active (start time unknown, use progress for batch-level detail)."
278	            )
279	        else:
280	            details["phase_progress_summary"] = f"{step} active (start time unknown)."
281	    return details
282	
283	
284	def _build_status_payload(plan_dir: Path, state: dict[str, Any]) -> StepResponse:
285	    next_steps = infer_next_steps(state)
286	    notes = state.get("meta", {}).get("notes", [])
287	    lock_path = plan_dir / ".plan.lock"
288	    lock_file_present = lock_path.exists()
289	    lock_held = plan_lock_is_held(plan_dir)
290	    active_step = _build_active_step(state.get("active_step"), plan_dir=plan_dir)
291	    last_step = _build_last_step(state)
292	    summary = f"Plan '{state['name']}' is currently in state '{state['current_state']}'."
293	    if active_step:
294	        summary = (
295	            summary
296	            + f" Active step: {active_step.get('step')} via {active_step.get('agent')}."
297	        )
298	    elif lock_file_present and not lock_held:
299	        summary = (
300	            summary
```

> AGENT

Let me continue reading cli.py and get specific line numbers for the subparser setup:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"subparsers\\|add_parser\" /Users/user_c042661f/Documents/megaplan/megaplan/cli.py | head -50"
}
```

> TOOL

tool_result Bash
```
818:    subparsers = parser.add_subparsers(dest="command", required=True)
820:    setup_parser = subparsers.add_parser("setup", help="Install megaplan into agent configs (global by default)")
825:    init_parser = subparsers.add_parser("init")
836:    list_parser = subparsers.add_parser("list")
849:        step_parser = subparsers.add_parser(name)
856:        step_parser = subparsers.add_parser(name)
873:    config_parser = subparsers.add_parser("config", help="View or edit megaplan configuration")
874:    config_sub = config_parser.add_subparsers(dest="config_action", required=True)
875:    config_sub.add_parser("show")
876:    set_parser = config_sub.add_parser("set")
879:    config_sub.add_parser("reset")
881:    step_parser = subparsers.add_parser("step", help="Edit plan step sections without hand-editing markdown")
882:    step_subparsers = step_parser.add_subparsers(dest="step_action", required=True)
884:    step_add_parser = step_subparsers.add_parser("add", help="Insert a new step after an existing step")
885:    step_add_parser.add_argument("--plan")
886:    step_add_parser.add_argument("--after")
887:    step_add_parser.add_argument("description")
889:    step_remove_parser = step_subparsers.add_parser("remove", help="Remove a step and renumber the plan")
893:    step_move_parser = step_subparsers.add_parser("move", help="Move a step after another step and renumber")
898:    override_parser = subparsers.add_parser("override")
905:    verify_human_parser = subparsers.add_parser("verify-human", help="Record human verification for a criterion")
913:    audit_verifiability_parser = subparsers.add_parser("audit-verifiability", help="Audit criteria verifiability")
916:    debt_parser = subparsers.add_parser("debt", help="Inspect or manage persistent tech debt entries")
917:    debt_subparsers = debt_parser.add_subparsers(dest="debt_action", required=True)
919:    debt_list_parser = debt_subparsers.add_parser("list", help="List debt entries")
922:    debt_add_parser = debt_subparsers.add_parser("add", help="Add or increment a debt entry")
923:    debt_add_parser.add_argument("--subsystem", required=True)
924:    debt_add_parser.add_argument("--concern", required=True)
925:    debt_add_parser.add_argument("--flag-ids", default="")
926:    debt_add_parser.add_argument("--plan")
928:    debt_resolve_parser = debt_subparsers.add_parser("resolve", help="Resolve a debt entry")
932:    loop_init_parser = subparsers.add_parser("loop-init", help="Initialize a MegaLoop workflow")
951:    loop_run_parser = subparsers.add_parser("loop-run", help="Run an existing MegaLoop workflow")
965:    loop_status_parser = subparsers.add_parser("loop-status", help="Show MegaLoop state")
969:    loop_pause_parser = subparsers.add_parser("loop-pause", help="Pause a MegaLoop workflow")
975:    build_auto_parser(subparsers)
978:    build_chain_parser(subparsers)
981:    build_tiebreaker_parser(subparsers)
[rerun: b1]
```

> AGENT

Perfect! Now let me get the exact line numbers for handlers.py functions:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"^def handle_gate\\|^def _apply_gate_outcome\" /Users/user_c042661f/Documents/megaplan/megaplan/handlers.py"
}
```

> TOOL

tool_result Bash
```
606:def _apply_gate_outcome(
1116:def handle_gate(root: Path, args: argparse.Namespace) -> StepResponse:
[rerun: b2]
```

> AGENT

Excellent! Now let me verify the workflow.py WORKFLOW dict and _transition_matches:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"^WORKFLOW\\|^def _transition_matches\" /Users/user_c042661f/Documents/megaplan/megaplan/_core/workflow.py"
}
```

> TOOL

tool_result Bash
```
32:WORKFLOW: dict[str, list[Transition]] = {
175:def _transition_matches(state: PlanState, condition: str) -> bool:
[rerun: b3]
```

> AGENT

Perfect! Now let me verify the registries and verify gate prompt locations:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"^def _jaccard_similarity\\|^def _concern_word_set\" /Users/user_c042661f/Documents/megaplan/megaplan/_core/registries.py"
}
```

> TOOL

tool_result Bash
```
106:def _concern_word_set(concern: str) -> set[str]:
114:def _jaccard_similarity(left: set[str], right: set[str]) -> float:
[rerun: b4]
```

> AGENT

Now verify the gate.py prompt location:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"^def _gate_prompt\" /Users/user_c042661f/Documents/megaplan/megaplan/prompts/gate.py"
}
```

> TOOL

tool_result Bash
```
24:def _gate_prompt(state: PlanState, plan_dir: Path, root: Path | None = None) -> str:
[rerun: b5]
```

> AGENT

And critique.py functions:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"^def _critique_context\\|^def _build_critique_prompt\" /Users/user_c042661f/Documents/megaplan/megaplan/prompts/critique.py"
}
```

> TOOL

tool_result Bash
```
87:def _critique_context(state: PlanState, plan_dir: Path, root: Path | None = None) -> dict[str, Any]:
167:def _build_critique_prompt(
[rerun: b6]
```

> AGENT

Verify the gate.json schema location and recommendation enum:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n '\"gate.json\"\\|\"recommendation\"' /Users/user_c042661f/Documents/megaplan/megaplan/schemas.py | head -20"
}
```

> TOOL

tool_result Bash
```
114:    "gate.json": {
117:            "recommendation": {
164:            "recommendation",
[rerun: b7]
```

> AGENT

Perfect! Now let me verify AUTOMATION_TERMINAL_STATES and _phase_command in auto.py:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"AUTOMATION_TERMINAL_STATES\\|^def _phase_command\" /Users/user_c042661f/Documents/megaplan/megaplan/auto.py"
}
```

> TOOL

tool_result Bash
```
27:from megaplan.types import AUTOMATION_TERMINAL_STATES, STATE_AWAITING_HUMAN, TERMINAL_STATES
117:def _phase_command(next_step: str) -> list[str]:
186:        if state in AUTOMATION_TERMINAL_STATES:
[rerun: b8]
```

> AGENT

Now let me compile all the information into a comprehensive report:

## Finalize Briefing: Comprehensive File State Summary

### 1. megaplan/types.py
**States defined (lines 8-23):**
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

**FlagRecord (lines 128-143):**
- Required fields class `_FlagRecordRequired` (lines 128-133): id, concern, category, status
- Extended class `FlagRecord` (lines 135-143): adds optional severity_hint, evidence, raised_in, severity, verified, verified_in, addressed_in

**PlanConfig (lines 30-35):**
- TypedDict with project_dir, auto_approve, robustness, agents, workers (optional)

### 2. megaplan/schemas.py
**gate.json schema defined (lines 114-172)**
- Schema location: lines 114-172
- **Recommendation enum (line 118-120):** `"enum": ["PROCEED", "ITERATE", "ESCALATE"]`
- Contains: rationale, signals_assessment, warnings, settled_decisions, flag_resolutions, accepted_tradeoffs

### 3. megaplan/handlers.py
- **handle_gate:** line 1116 (definition start)
- **_apply_gate_outcome:** line 606 (definition start)

### 4. megaplan/_core/workflow.py
- **WORKFLOW dict:** line 32 - contains state transition rules for: INITIALIZED, PREPPED, PLANNED, CRITIQUED, GATED, FINALIZED, EXECUTED, AWAITING_HUMAN (lines 32-71)
- **_transition_matches:** line 175 - evaluates gate conditions (gate_unset, gate_iterate, gate_escalate, gate_proceed_blocked, gate_proceed)

### 5. megaplan/_core/registries.py
- **_concern_word_set:** line 106 - tokenizes concern text into normalized word set
- **_jaccard_similarity:** line 114 - computes intersection/union similarity (0.0-1.0)

### 6. megaplan/prompts/gate.py
- **_gate_prompt:** line 24 - constructs gate decision prompt with plan, flags, signals, debt block, robustness level

### 7. megaplan/prompts/critique.py
- **_critique_context:** line 87 - builds context dict with project_dir, prep_block, latest_plan, metadata, unresolved flags, debt_block
- **_build_critique_prompt:** line 167 - assembles full critique prompt using context + review block

### 8. megaplan/cli.py
**Subparsers setup (lines 818-981):**
- Main subparsers created: line 818 (`parser.add_subparsers(dest="command", required=True)`)
- Individual parsers added:
  - setup: line 820
  - init: line 825
  - list: line 836
  - step commands (plan, prep, critique, revise, gate, finalize, execute, review): lines 848-856
  - config: line 873 (with config_sub subparsers)
  - step: line 881 (with step_subparsers: add, remove, move)
  - override: line 898
  - verify-human: line 905
  - audit-verifiability: line 913
  - debt: line 916 (with debt_subparsers: list, add, resolve)
  - loop-init: line 932
  - loop-run: line 951
  - loop-status: line 965
  - loop-pause: line 969
  - auto: line 975 (via `build_auto_parser`)
  - chain: line 978 (via `build_chain_parser`)
  - tiebreaker: line 981 (via `build_tiebreaker_parser`)

### 9. megaplan/auto.py
- **AUTOMATION_TERMINAL_STATES imported:** line 27 (from megaplan.types)
- **_phase_command:** line 117 - translates next_step to CLI args; execute gets `["execute", "--confirm-destructive", "--user-approved"]`
- **AUTOMATION_TERMINAL_STATES usage:** line 186 - checked in drive() to detect terminal conditions

### 10. megaplan/tiebreaker.py
**Key components:**
- `_next_version_suffix` (line 32) - generates suffix for multiple tiebreaker runs ("", "_v2", "_v3", etc.)
- `_run_tiebreaker` (line 49) - orchestrates researcher→challenger→synthesis pipeline
- `_build_resolved` (line 143) - builds agent mode tuple
- `_resolve_question` (line 153) - reads question from file or inline arg
- `_run_tiebreaker_status` (line 171) - shows tiebreaker run history
- `build_tiebreaker_parser` (line 234) - CLI parser with question args and subcommands (status)
- `run_tiebreaker_cli` (line 254) - CLI entry point

### 11. pyproject.toml
- **Current version:** `0.17.0` (line 7)

### 12. tests/ - Test Files Present
24 test files found:
- `test_core.py`
- `test_quality.py`
- `test_loop.py`
- `test_swe_bench.py`
- `test_evaluation.py`
- `test_io_git_patch.py`
- `test_review_mechanical.py`
- `test_parallel_critique.py`
- `test_workers.py`
- `test_checks.py`
- `test_review_checks.py`
- `test_config.py`
- `test_handle_review_robustness.py`
- `test_parallel_review.py`
- `test_doc_mode.py`
- `test_chain.py`
- `test_prompts.py`
- `test_tiny_robustness.py`
- `test_verifiability.py`
- `test_megaplan.py`
- `test_tiebreaker.py`
- `test_schemas.py`
- `__init__.py`
