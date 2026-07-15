> DEVELOPER

Explore the megaplan repository at /Users/user_c042661f/Documents/megaplan. I need to understand:
1. The overall file structure (main modules, entry points)
2. How the current pipeline works (plan → execute → review flow)
3. Key files: megaplan.sh, any Python modules, prompt templates, config files
4. How steps are currently executed and reviewed
5. What "modes" or step types currently exist

Focus on src/ or the main code directory. Be thorough but skip .megaplan/ artifacts, docs/, and ops/ unless they contain core code. Report file paths and line numbers for [REDACTED]

> AGENT

I'll explore the megaplan repository systematically. Let me start with the top-level structure and key files in parallel.

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/megaplan/",
  "description": "List top-level directory"
}
```

> TOOL

tool_result Bash
```
CHANGELOG.md
LICENSE
README.md
activity-summary-2026-03-20.md
dist
evals
idea-doc-mode.txt
idea-v0.14-strict-gate.txt
megaplan
plan.md
pyproject.toml
review-severity-plumbing.critique_output.json
rework-item-polish-critique_output.json
scorecard.png
tests
uv.lock
[rerun: b1]
```

> TOOL

tool_use Glob
```json
{
  "pattern": "**/*.py",
  "path": "/Users/user_c042661f/Documents/megaplan"
}
```

> TOOL

tool_result Glob
```
megaplan/__main__.py
tests/__init__.py
tests/test_core.py
megaplan/quality.py
tests/test_quality.py
megaplan/loop/__init__.py
megaplan/loop/git.py
megaplan/loop/types.py
megaplan/loop/prompts.py
megaplan/loop/handlers.py
tests/test_loop.py
evals/__init__.py
evals/benchmarks/__init__.py
evals/benchmarks/swe_bench.py
tests/test_swe_bench.py
megaplan/merge.py
tests/test_evaluation.py
.venv/bin/activate_this.py
.venv/lib/python3.11/site-packages/_virtualenv.py
megaplan/execution_quality.py
megaplan/execution_timeout.py
megaplan/_core/registries.py
megaplan/prompts/finalize.py
megaplan/key_pool.py
megaplan/prompts/_shared.py
megaplan/hermes_worker.py
megaplan/parallel_critique.py
megaplan/_core/io.py
tests/test_io_git_patch.py
tests/test_review_mechanical.py
tests/test_parallel_critique.py
megaplan/flags.py
megaplan/prompts/__init__.py
megaplan/prompts/planning.py
megaplan/step_edit.py
megaplan/_core/phase_runtime.py
megaplan/_core/__init__.py
megaplan/execution.py
megaplan/prompts/critique.py
megaplan/__init__.py
megaplan/schemas.py
megaplan/prompts/execute.py
tests/test_workers.py
tests/test_tiny_robustness.py
megaplan/types.py
megaplan/checks.py
megaplan/review_checks.py
megaplan/loop/engine.py
megaplan/prompts/review.py
megaplan/parallel_review.py
megaplan/review_mechanical.py
tests/test_checks.py
tests/test_review_checks.py
tests/test_config.py
tests/test_handle_review_robustness.py
tests/test_parallel_review.py
tests/test_prompts.py
tests/test_schemas.py
megaplan/_core/state.py
megaplan/_core/workflow.py
megaplan/cli.py
megaplan/auto.py
megaplan/handlers.py
megaplan/prompts/gate.py
tests/test_megaplan.py
megaplan/workers.py
megaplan/evaluation.py
```

> TOOL

tool_use Glob
```json
{
  "pattern": "**/*.sh",
  "path": "/Users/user_c042661f/Documents/megaplan"
}
```

> TOOL

tool_result Glob
```
No files found
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/megaplan/megaplan/",
  "description": "List megaplan package directory"
}
```

> TOOL

tool_result Bash
```
__init__.py
__main__.py
__pycache__
_core
auto.py
checks.py
cli.py
data
evaluation.py
execution.py
execution_quality.py
execution_timeout.py
flags.py
handlers.py
hermes_worker.py
key_pool.py
loop
merge.py
parallel_critique.py
parallel_review.py
prompts
quality.py
review_checks.py
review_mechanical.py
schemas.py
step_edit.py
types.py
workers.py
[rerun: b2]
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
File content (12533 tokens) exceeds maximum allowed tokens (10000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/__main__.py"
}
```

> TOOL

tool_result Read
```
1	"""Allow running as `python -m megaplan`."""
2	
3	from megaplan.cli import main
4	import sys
5	
6	sys.exit(main())
7
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/cli.py",
  "offset": 1,
  "limit": 100
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
52	    handle_critique,
53	    handle_execute,
54	    handle_finalize,
55	    handle_gate,
56	    handle_init,
57	    handle_override,
58	    handle_plan,
59	    handle_prep,
60	    handle_review,
61	    handle_revise,
62	)
63	from megaplan.loop.handlers import (
64	    handle_loop_init,
65	    handle_loop_pause,
66	    handle_loop_run,
67	    handle_loop_status,
68	)
69	from megaplan.step_edit import handle_step
70	
71	
72	def render_response(response: StepResponse, *, exit_code: int = 0) -> int:
73	    print(json_dump(response), end="")
74	    return exit_code
75	
76	
77	def _resolve_error_plan_dir(root: Path | None, error: CliError) -> Path | None:
78	    if root is None or error.code != "plan_locked" or not isinstance(error.extra, dict):
79	        return None
80	    plan_name = error.extra.get("plan")
81	    if not isinstance(plan_name, str) or not plan_name:
82	        return None
83	    try:
84	        return resolve_plan_dir(root, plan_name)
85	    except CliError:
86	        return None
87	
88	
89	def _augment_plan_locked_error(
90	    payload: StepResponse,
91	    error: CliError,
92	    *,
93	    root: Path | None,
94	) -> None:
95	    plan_dir = _resolve_error_plan_dir(root, error)
96	    details = payload.get("details")
97	    if not isinstance(details, dict):
98	        details = None
99	    plan_name = (details or {}).get("plan")
100	    if isinstance(plan_name, str) and plan_name:
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
21	TERMINAL_STATES = {STATE_DONE, STATE_ABORTED}
22	
23	
24	# ---------------------------------------------------------------------------
25	# TypedDicts
26	# ---------------------------------------------------------------------------
27	
28	class PlanConfig(TypedDict, total=False):
29	    project_dir: str
30	    auto_approve: bool
31	    robustness: str
32	    agents: dict[str, str]
33	
34	
35	class PlanMeta(TypedDict, total=False):
36	    significant_counts: list[int]
37	    weighted_scores: list[float]
38	    plan_deltas: list[float | None]
39	    recurring_critiques: list[str]
40	    total_cost_usd: float
41	    overrides: list[dict[str, Any]]
42	    notes: list[dict[str, Any]]
43	    user_approved_gate: bool
44	
45	
46	class SessionInfo(TypedDict, total=False):
47	    id: str
48	    mode: str
49	    created_at: str
50	    last_used_at: str
51	    refreshed: bool
52	
53	
54	class ActiveStep(TypedDict, total=False):
55	    step: str
56	    agent: str
57	    mode: str
58	    model: str
59	    run_id: str
60	    session_id: str
61	    started_at: str
62	
63	
64	class PlanVersionRecord(TypedDict, total=False):
65	    version: int
66	    file: str
67	    hash: str
68	    timestamp: str
69	
70	
71	class HistoryEntry(TypedDict, total=False):
72	    step: str
73	    timestamp: str
74	    duration_ms: int
75	    cost_usd: float
76	    result: str
77	    session_mode: str
78	    session_id: str
79	    agent: str
80	    output_file: str
81	    artifact_hash: str
82	    finalize_hash: str
83	    raw_output_file: str
84	    message: str
85	    flags_count: int
86	    flags_addressed: list[str]
87	    recommendation: str
88	    approval_mode: str
89	    environment: dict[str, bool]
90	
91	
92	class ClarificationRecord(TypedDict, total=False):
93	    refined_idea: str
94	    intent_summary: str
95	    questions: list[str]
96	
97	
98	class LastGateRecord(TypedDict, total=False):
99	    recommendation: str
100	    rationale: str
101	    signals_assessment: str
102	    warnings: list[str]
103	    settled_decisions: list["SettledDecision"]
104	    passed: bool
105	    preflight_results: dict[str, bool]
106	    orchestrator_guidance: str
107	
108	
109	class PlanState(TypedDict):
110	    name: str
111	    idea: str
112	    current_state: str
113	    iteration: int
114	    created_at: str
115	    config: PlanConfig
116	    sessions: dict[str, SessionInfo]
117	    plan_versions: list[PlanVersionRecord]
118	    history: list[HistoryEntry]
119	    meta: PlanMeta
120	    last_gate: LastGateRecord
121	    active_step: NotRequired[ActiveStep]
122	    clarification: NotRequired[ClarificationRecord]
123	
124	
125	class _FlagRecordRequired(TypedDict):
126	    id: str
127	    concern: str
128	    category: str
129	    status: str
130	
131	
132	class FlagRecord(_FlagRecordRequired, total=False):
133	    severity_hint: str
134	    evidence: str
135	    raised_in: str
136	    severity: str
137	    verified: bool
138	    verified_in: str
139	    addressed_in: str
140	
141	
142	class FlagRegistry(TypedDict):
143	    flags: list[FlagRecord]
144	
145	
146	class GateCheckResult(TypedDict):
147	    passed: bool
148	    criteria_check: dict[str, Any]
149	    preflight_results: dict[str, bool]
150	    unresolved_flags: list[FlagRecord]
151	
152	
153	class SettledDecision(TypedDict, total=False):
154	    id: str
155	    decision: str
156	    rationale: str
157	
158	
159	class GatePayload(TypedDict):
160	    recommendation: str
161	    rationale: str
162	    signals_assessment: str
163	    warnings: list[str]
164	    settled_decisions: list[SettledDecision]
165	
166	
167	class GateArtifact(TypedDict, total=False):
168	    passed: bool
169	    criteria_check: dict[str, Any]
170	    preflight_results: dict[str, bool]
171	    unresolved_flags: list[FlagRecord]
172	    recommendation: str
173	    rationale: str
174	    signals_assessment: str
175	    warnings: list[str]
176	    settled_decisions: list[SettledDecision]
177	    override_forced: bool
178	    orchestrator_guidance: str
179	    robustness: str
180	    signals: dict[str, Any]
181	
182	
183	class GateSignals(TypedDict, total=False):
184	    robustness: str
185	    signals: dict[str, Any]
186	    warnings: list[str]
187	
188	
189	class StepResponse(TypedDict, total=False):
190	    success: bool
191	    step: str
192	    summary: str
193	    artifacts: list[str]
194	    next_step: str | None
195	    state: str
196	    auto_approve: bool
197	    robustness: str
198	    iteration: int
199	    plan: str
200	    plan_dir: str
201	    questions: list[str]
202	    verified_flags: list[str]
203	    open_flags: list[str]
204	    scope_creep_flags: list[str]
205	    warnings: list[str]
206	    files_changed: list[str]
207	    deviations: list[str]
208	    user_approved_gate: bool
209	    issues: list[str]
210	    valid_next: list[str]
211	    mode: str
212	    installed: list[dict[str, Any]]
213	    config_path: str
214	    routing: dict[str, str]
215	    raw_config: dict[str, Any]
216	    action: str
217	    key: str
218	    value: str
219	    skipped: bool
220	    file: str
221	    plans: list[dict[str, Any]]
222	    recommendation: str
223	    signals: dict[str, Any]
224	    rationale: str
225	    signals_assessment: str
226	    orchestrator_guidance: str
227	    passed: bool
228	    criteria_check: dict[str, Any]
229	    preflight_results: dict[str, bool]
230	    unresolved_flags: list[Any]
231	    error: str
232	    message: str
233	    details: dict[str, Any]
234	    agent_fallback: dict[str, str]
235	
236	
237	class DebtEntry(TypedDict):
238	    id: str
239	    subsystem: str
240	    concern: str
241	    flag_ids: list[str]
242	    plan_ids: list[str]
243	    occurrence_count: int
244	    created_at: str
245	    updated_at: str
246	    resolved: bool
247	    resolved_by: str | None
248	    resolved_at: str | None
249	
250	
251	class DebtRegistry(TypedDict):
252	    entries: list[DebtEntry]
253	
254	
255	# ---------------------------------------------------------------------------
256	# Constants
257	# ---------------------------------------------------------------------------
258	
259	FLAG_BLOCKING_STATUSES = {"open", "disputed", "addressed"}
260	FLAG_VALID_STATUSES = {
261	    "open", "addressed", "disputed", "verified",
262	    "accepted_tradeoff", "gate_disputed",
263	}
264	DEBT_ESCALATION_THRESHOLD = 3
265	MOCK_ENV_VAR = "MEGAPLAN_MOCK_WORKERS"
266	
267	DEFAULT_AGENT_ROUTING: dict[str, str] = {
268	    "plan": "claude",
269	    "prep": "claude",
270	    "critique": "codex",
271	    "revise": "claude",
272	    "gate": "claude",
273	    "finalize": "claude",
274	    "execute": "codex",
275	    "loop_plan": "claude",
276	    "loop_execute": "codex",
277	    "review": "codex",
278	}
279	KNOWN_AGENTS = ["claude", "codex", "hermes"]
280	ROBUSTNESS_LEVELS = ("tiny", "light", "standard", "robust", "superrobust")
281	def parse_agent_spec(spec: str) -> tuple[str, str | None]:
282	    """Parse 'hermes:model/name' → ('hermes', 'model/name') or 'claude' → ('claude', None)."""
283	    if ":" in spec:
284	        agent, model = spec.split(":", 1)
285	        return agent, model
286	    return spec, None
287	
288	
289	SCOPE_CREEP_TERMS = (
290	    "scope creep",
291	    "out of scope",
292	    "beyond the original idea",
293	    "beyond original idea",
294	    "beyond user intent",
295	    "expanded scope",
296	)
297	
298	DEFAULTS = {
299	    "execution.auto_approve": False,
300	    "execution.robustness": "standard",
301	    "execution.worker_timeout_seconds": 7200,
302	    "execution.max_review_rework_cycles": 3,
303	    "execution.max_robust_review_rework_cycles": 2,
304	    "execution.max_execute_no_progress": 3,
305	    "orchestration.max_critique_concurrency": 2,
306	    "orchestration.mode": "subagent",
307	}
308	
309	_SETTABLE_BOOL = {
310	    "execution.auto_approve",
311	}
312	
313	_SETTABLE_ENUM = {
314	    "execution.robustness": ROBUSTNESS_LEVELS,
315	}
316	
317	_SETTABLE_NUMERIC = {
318	    "execution.worker_timeout_seconds",
319	    "execution.max_review_rework_cycles",
320	    "execution.max_robust_review_rework_cycles",
321	    "execution.max_execute_no_progress",
322	    "orchestration.max_critique_concurrency",
323	}
324	
325	
326	# ---------------------------------------------------------------------------
327	# Exception
328	# ---------------------------------------------------------------------------
329	
330	class CliError(Exception):
331	    def __init__(
332	        self,
333	        code: str,
334	        message: str,
335	        *,
336	        valid_next: list[str] | None = None,
337	        extra: dict[str, Any] | None = None,
338	        exit_code: int = 1,
339	    ) -> None:
340	        super().__init__(message)
341	        self.code = code
342	        self.message = message
343	        self.valid_next = valid_next or []
344	        self.extra = extra or {}
345	        self.exit_code = exit_code
346
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
21	                    },
22	                    "required": ["criterion", "priority"],
23	                },
24	            },
25	            "assumptions": {"type": "array", "items": {"type": "string"}},
26	        },
27	        "required": ["plan", "questions", "success_criteria", "assumptions"],
28	    },
29	    "prep.json": {
30	        "type": "object",
31	        "properties": {
32	            "skip": {"type": "boolean"},
33	            "task_summary": {"type": "string"},
34	            "key_evidence": {
35	                "type": "array",
36	                "items": {
37	                    "type": "object",
38	                    "properties": {
39	                        "point": {"type": "string"},
40	                        "source": {"type": "string"},
41	                        "relevance": {"type": "string", "enum": ["high", "medium", "low"]},
42	                    },
43	                    "required": ["point", "source", "relevance"],
44	                },
45	            },
46	            "relevant_code": {
47	                "type": "array",
48	                "items": {
49	                    "type": "object",
50	                    "properties": {
51	                        "file_path": {"type": "string"},
52	                        "why": {"type": "string"},
53	                        "functions": {"type": "array", "items": {"type": "string"}},
54	                    },
55	                    "required": ["file_path", "why", "functions"],
56	                },
57	            },
58	            "test_expectations": {
59	                "type": "array",
60	                "items": {
61	                    "type": "object",
62	                    "properties": {
63	                        "test_id": {"type": "string"},
64	                        "what_it_checks": {"type": "string"},
65	                        "status": {"type": "string", "enum": ["fail_to_pass", "pass_to_pass"]},
66	                    },
67	                    "required": ["test_id", "what_it_checks", "status"],
68	                },
69	            },
70	            "constraints": {"type": "array", "items": {"type": "string"}},
71	            "suggested_approach": {"type": "string"},
72	        },
73	        "required": [
74	            "skip",
75	            "task_summary",
76	            "key_evidence",
77	            "relevant_code",
78	            "test_expectations",
79	            "constraints",
80	            "suggested_approach",
81	        ],
82	    },
83	    "revise.json": {
84	        "type": "object",
85	        "properties": {
86	            "plan": {"type": "string"},
87	            "changes_summary": {"type": "string"},
88	            "flags_addressed": {"type": "array", "items": {"type": "string"}},
89	            "assumptions": {"type": "array", "items": {"type": "string"}},
90	            "success_criteria": {
91	                "type": "array",
92	                "items": {
93	                    "type": "object",
94	                    "properties": {
95	                        "criterion": {"type": "string"},
96	                        "priority": {"type": "string", "enum": ["must", "should", "info"]},
97	                    },
98	                    "required": ["criterion", "priority"],
99	                },
100	            },
101	            "questions": {"type": "array", "items": {"type": "string"}},
102	        },
103	        "required": [
104	            "plan",
105	            "changes_summary",
106	            "flags_addressed",
107	            "assumptions",
108	            "success_criteria",
109	            "questions",
110	        ],
111	    },
112	    "gate.json": {
113	        "type": "object",
114	        "properties": {
115	            "recommendation": {
116	                "type": "string",
117	                "enum": ["PROCEED", "ITERATE", "ESCALATE"],
118	            },
119	            "rationale": {"type": "string"},
120	            "signals_assessment": {"type": "string"},
121	            "warnings": {"type": "array", "items": {"type": "string"}},
122	            "settled_decisions": {
123	                "type": "array",
124	                "items": {
125	                    "type": "object",
126	                    "properties": {
127	                        "id": {"type": "string"},
128	                        "decision": {"type": "string"},
129	                        "rationale": {"type": "string"},
130	                    },
131	                    "required": ["id", "decision", "rationale"],
132	                },
133	            },
134	            "flag_resolutions": {
135	                "type": "array",
136	                "items": {
137	                    "type": "object",
138	                    "properties": {
139	                        "flag_id": {"type": "string"},
140	                        "action": {"type": "string", "enum": ["dispute", "accept_tradeoff"]},
141	                        "evidence": {"type": "string"},
142	                        "rationale": {"type": "string"},
143	                    },
144	                    "required": ["flag_id", "action", "evidence", "rationale"],
145	                },
146	            },
147	            "accepted_tradeoffs": {
148	                "type": "array",
149	                "items": {
150	                    "type": "object",
151	                    "properties": {
152	                        "flag_id": {"type": "string"},
153	                        "concern": {"type": "string"},
154	                        "subsystem": {"type": "string"},
155	                        "rationale": {"type": "string"},
156	                    },
157	                    "required": ["flag_id", "concern", "subsystem", "rationale"],
158	                },
159	            },
160	        },
161	        "required": [
162	            "recommendation",
163	            "rationale",
164	            "signals_assessment",
165	            "warnings",
166	            "settled_decisions",
167	            "flag_resolutions",
168	            "accepted_tradeoffs",
169	        ],
170	    },
171	    "critique.json": {
172	        "type": "object",
173	        "properties": {
174	            "checks": {
175	                "type": "array",
176	                "items": {
177	                    "type": "object",
178	                    "properties": {
179	                        "id": {"type": "string"},
180	                        "question": {"type": "string"},
181	                        "findings": {
182	                            "type": "array",
183	                            "items": {
184	                                "type": "object",
185	                                "properties": {
186	                                    "detail": {"type": "string"},
187	                                    "flagged": {"type": "boolean"},
188	                                },
189	                                "required": ["detail", "flagged"],
190	                            },
191	                        },
192	                    },
193	                    "required": ["id", "question", "findings"],
194	                },
195	            },
196	            "flags": {
197	                "type": "array",
198	                "items": {
199	                    "type": "object",
200	                    "properties": {
201	                        "id": {"type": "string"},
202	                        "concern": {"type": "string"},
203	                        "category": {
204	                            "type": "string",
205	                            "enum": [
206	                                "correctness",
207	                                "security",
208	                                "completeness",
209	                                "performance",
210	                                "maintainability",
211	                                "other",
212	                            ],
213	                        },
214	                        "severity_hint": {
215	                            "type": "string",
216	                            "enum": ["likely-significant", "likely-minor", "uncertain"],
217	                        },
218	                        "evidence": {"type": "string"},
219	                    },
220	                    "required": ["id", "concern", "category", "severity_hint", "evidence"],
221	                },
222	            },
223	            "verified_flag_ids": {"type": "array", "items": {"type": "string"}},
224	            "disputed_flag_ids": {"type": "array", "items": {"type": "string"}},
225	        },
226	        "required": ["checks", "flags", "verified_flag_ids", "disputed_flag_ids"],
227	    },
228	"finalize.json": {
229	        "type": "object",
230	        "properties": {
231	            "tasks": {
232	                "type": "array",
233	                "items": {
234	                    "type": "object",
235	                    "properties": {
236	                        "id": {"type": "string"},
237	                        "description": {"type": "string"},
238	                        "depends_on": {"type": "array", "items": {"type": "string"}},
239	                        "status": {"type": "string", "enum": ["pending", "done", "skipped"]},
240	                        "executor_notes": {"type": "string"},
241	                        "files_changed": {"type": "array", "items": {"type": "string"}},
242	                        "commands_run": {"type": "array", "items": {"type": "string"}},
243	                        "evidence_files": {"type": "array", "items": {"type": "string"}},
244	                        "reviewer_verdict": {"type": "string"},
245	                    },
246	                    "required": [
247	                        "id",
248	                        "description",
249	                        "depends_on",
250	                        "status",
251	                        "executor_notes",
252	                        "files_changed",
253	                        "commands_run",
254	                        "evidence_files",
255	                        "reviewer_verdict",
256	                    ],
257	                },
258	            },
259	            "watch_items": {"type": "array", "items": {"type": "string"}},
260	            "sense_checks": {
261	                "type": "array",
262	                "items": {
263	                    "type": "object",
264	                    "properties": {
265	                        "id": {"type": "string"},
266	                        "task_id": {"type": "string"},
267	                        "question": {"type": "string"},
268	                        "executor_note": {"type": "string"},
269	                        "verdict": {"type": "string"},
270	                    },
271	                    "required": ["id", "task_id", "question", "executor_note", "verdict"],
272	                },
273	            },
274	            "meta_commentary": {"type": "string"},
275	            "validation": {
276	                "type": "object",
277	                "properties": {
278	                    "plan_steps_covered": {
279	                        "type": "array",
280	                        "items": {
281	                            "type": "object",
282	                            "properties": {
283	                                "plan_step_summary": {"type": "string"},
284	                                "finalize_task_ids": {
285	                                    "type": "array",
286	                                    "items": {"type": "string"},
287	                                },
288	                            },
289	                            "required": ["plan_step_summary", "finalize_task_ids"],
290	                        },
291	                    },
292	                    "orphan_tasks": {
293	                        "type": "array",
294	                        "items": {"type": "string"},
295	                    },
296	                    "completeness_notes": {"type": "string"},
297	                    "coverage_complete": {"type": "boolean"},
298	                },
299	                "required": [
300	                    "plan_steps_covered",
301	                    "orphan_tasks",
302	                    "completeness_notes",
303	                    "coverage_complete",
304	                ],
305	            },
306	            "baseline_test_failures": {
307	                "type": ["array", "null"],
308	                "items": {"type": "string"},
309	            },
310	            "baseline_test_command": {"type": ["string", "null"]},
311	            "baseline_test_note": {"type": "string"},
312	        },
313	        "required": ["tasks", "watch_items", "sense_checks", "meta_commentary", "validation"],
314	    },
315	    "execution.json": {
316	        "type": "object",
317	        "properties": {
318	            "output": {"type": "string"},
319	            "files_changed": {"type": "array", "items": {"type": "string"}},
320	            "commands_run": {"type": "array", "items": {"type": "string"}},
321	            "deviations": {"type": "array", "items": {"type": "string"}},
322	            "task_updates": {
323	                "type": "array",
324	                "items": {
325	                    "type": "object",
326	                    "properties": {
327	                        "task_id": {"type": "string"},
328	                        "status": {"type": "string", "enum": ["done", "skipped"]},
329	                        "executor_notes": {"type": "string"},
330	                        "files_changed": {"type": "array", "items": {"type": "string"}},
331	                        "commands_run": {"type": "array", "items": {"type": "string"}},
332	                    },
333	                    "required": ["task_id", "status", "executor_notes", "files_changed", "commands_run"],
334	                },
335	            },
336	            "sense_check_acknowledgments": {
337	                "type": "array",
338	                "items": {
339	                    "type": "object",
340	                    "properties": {
341	                        "sense_check_id": {"type": "string"},
342	                        "executor_note": {"type": "string"},
343	                    },
344	                    "required": ["sense_check_id", "executor_note"],
345	                },
346	            },
347	        },
348	        "required": ["output", "files_changed", "commands_run", "deviations", "task_updates", "sense_check_acknowledgments"],
349	    },
350	    "loop_plan.json": {
351	        "type": "object",
352	        "properties": {
353	            "spec_updates": {
354	                "type": "object",
355	                "additionalProperties": True,
356	            },
357	            "next_action": {"type": "string"},
358	            "reasoning": {"type": "string"},
359	        },
360	        "required": ["spec_updates", "next_action", "reasoning"],
361	    },
362	    "loop_execute.json": {
363	        "type": "object",
364	        "properties": {
365	            "diagnosis": {"type": "string"},
366	            "fix_description": {"type": "string"},
367	            "files_to_change": {"type": "array", "items": {"type": "string"}},
368	            "confidence": {"type": "string"},
369	            "outcome": {"type": "string"},
370	            "should_pause": {"type": "boolean"},
371	        },
372	        "required": ["diagnosis", "fix_description", "files_to_change", "confidence", "outcome", "should_pause"],
373	    },
374	    "review.json": {
375	        "type": "object",
376	        "properties": {
377	            "review_verdict": {"type": "string", "enum": ["approved", "needs_rework"]},
378	            "checks": {
379	                "type": "array",
380	                "items": {
381	                    "type": "object",
382	                    "properties": {
383	                        "id": {"type": "string"},
384	                        "question": {"type": "string"},
385	                        "guidance": {"type": "string"},
386	                        "findings": {
387	                            "type": "array",
388	                            "items": {
389	                                "type": "object",
390	                                "properties": {
391	                                    "detail": {"type": "string"},
392	                                    "flagged": {"type": "boolean"},
393	                                    "status": {"type": "string"},
394	                                    "evidence_file": {"type": "string"},
395	                                },
396	                                "required": ["detail", "flagged", "status", "evidence_file"],
397	                            },
398	                        },
399	                        "prior_findings": {
400	                            "type": "array",
401	                            "items": {
402	                                "type": "object",
403	                                "properties": {
404	                                    "detail": {"type": "string"},
405	                                    "flagged": {"type": "boolean"},
406	                                    "status": {"type": "string"},
407	                                },
408	                                "required": ["detail", "flagged", "status"],
409	                            },
410	                        },
411	                    },
412	                    "required": ["id", "question", "guidance", "findings", "prior_findings"],
413	                },
414	            },
415	            "pre_check_flags": {
416	                "type": "array",
417	                "items": {
418	                    "type": "object",
419	                    "properties": {
420	                        "id": {"type": "string"},
421	                        "check": {"type": "string"},
422	                        "detail": {"type": "string"},
423	                        "severity": {"type": "string"},
424	                        "evidence_file": {"type": "string"},
425	                    },
426	                    "required": ["id", "check", "detail", "severity", "evidence_file"],
427	                },
428	            },
429	            "verified_flag_ids": {"type": "array", "items": {"type": "string"}},
430	            "disputed_flag_ids": {"type": "array", "items": {"type": "string"}},
431	            "criteria": {
432	                "type": "array",
433	                "items": {
434	                    "type": "object",
435	                    "properties": {
436	                        "name": {"type": "string"},
437	                        "priority": {"type": "string", "enum": ["must", "should", "info"]},
438	                        "pass": {"type": "string", "enum": ["pass", "fail", "waived"]},
439	                        "evidence": {"type": "string"},
440	                    },
441	                    "required": ["name", "priority", "pass", "evidence"],
442	                },
443	            },
444	            "issues": {"type": "array", "items": {"type": "string"}},
445	            "rework_items": {
446	                "type": "array",
447	                "items": {
448	                    "type": "object",
449	                    "properties": {
450	                        "task_id": {"type": "string"},
451	                        "issue": {"type": "string"},
452	                        "expected": {"type": "string"},
453	                        "actual": {"type": "string"},
454	                        "evidence_file": {"type": "string"},
455	                        "flag_id": {"type": ["string", "null"]},
456	                        "source": {"type": ["string", "null"]},
457	                    },
458	                    "required": ["task_id", "issue", "expected", "actual", "evidence_file", "flag_id", "source"],
459	                },
460	            },
461	            "summary": {"type": "string"},
462	            "task_verdicts": {
463	                "type": "array",
464	                "items": {
465	                    "type": "object",
466	                    "properties": {
467	                        "task_id": {"type": "string"},
468	                        "reviewer_verdict": {"type": "string"},
469	                        "evidence_files": {"type": "array", "items": {"type": "string"}},
470	                    },
471	                    "required": ["task_id", "reviewer_verdict", "evidence_files"],
472	                },
473	            },
474	            "sense_check_verdicts": {
475	                "type": "array",
476	                "items": {
477	                    "type": "object",
478	                    "properties": {
479	                        "sense_check_id": {"type": "string"},
480	                        "verdict": {"type": "string"},
481	                    },
482	                    "required": ["sense_check_id", "verdict"],
483	                },
484	            },
485	        },
486	        "required": [
487	            "review_verdict",
488	            "checks",
489	            "pre_check_flags",
490	            "verified_flag_ids",
491	            "disputed_flag_ids",
492	            "criteria",
493	            "issues",
494	            "rework_items",
495	            "summary",
496	            "task_verdicts",
497	            "sense_check_verdicts",
498	        ],
499	    },
500	}
501	
502	
503	def _preserve_explicit_required(path: tuple[str, ...]) -> bool:
504	    # `review.rework_items[]` uses explicit required fields because OpenAI
505	    # structured outputs require every property key to appear in `required`.
506	    return path[-3:] == ("properties", "rework_items", "items")
507	
508	
509	def strict_schema(schema: Any, _path: tuple[str, ...] = ()) -> Any:
510	    if isinstance(schema, dict):
511	        updated = {key: strict_schema(value, _path + (key,)) for key, value in schema.items()}
512	        if updated.get("type") == "object":
513	            updated.setdefault("additionalProperties", False)
514	            if "properties" in updated and not _preserve_explicit_required(_path):
515	                updated["required"] = list(updated["properties"].keys())
516	        return updated
517	    if isinstance(schema, list):
518	        return [strict_schema(item, _path) for item in schema]
519	    return schema
520
```

> AGENT

Now let me read the core handlers, execution, and the _core module.

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
File content (23685 tokens) exceeds maximum allowed tokens (10000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/__init__.py"
}
```

> TOOL

tool_result Read
```
1	"""Core infrastructure for megaplan — re-exports from submodules.
2	
3	All public names are available via ``from megaplan._core import <name>``
4	so existing callers don't need to change.
5	"""
6	
7	# Re-export shutil so monkeypatches like `megaplan._core.shutil.which` still work.
8	import shutil  # noqa: F401
9	
10	# -- io.py: pure utilities, atomic I/O, paths, config -----------------------
11	from .io import (
12	    artifact_path,
13	    atomic_write_json,
14	    atomic_write_text,
15	    batch_artifact_path,
16	    collect_git_diff_patch,
17	    collect_git_diff_summary,
18	    compute_global_batches,
19	    compute_task_batches,
20	    config_dir,
21	    current_iteration_artifact,
22	    current_iteration_raw_artifact,
23	    detect_available_agents,
24	    ensure_runtime_layout,
25	    find_command,
26	    get_effective,
27	    json_dump,
28	    list_batch_artifacts,
29	    load_config,
30	    load_finalize_snapshot,
31	    megaplan_root,
32	    normalize_text,
33	    now_utc,
34	    plans_root,
35	    read_json,
36	    render_final_md,
37	    save_config,
38	    schemas_root,
39	    sha256_file,
40	    sha256_text,
41	    slugify,
42	)
43	
44	# -- phase_runtime.py: centralized runtime policy ----------------------------
45	from .phase_runtime import (
46	    DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
47	    PHASE_RUNTIME_POLICY,
48	    build_next_step_runtime,
49	    build_phase_observability,
50	    format_duration_hint,
51	    humanize_seconds,
52	    phase_runtime_policy,
53	    phase_stale_seconds,
54	    phase_timeout_seconds,
55	    resolve_phase_runtime,
56	)
57	
58	# -- state.py: plan state, history, sessions ---------------------------------
59	from .state import (
60	    active_plan_dirs,
61	    active_step_is_stale,
62	    append_history,
63	    apply_session_update,
64	    clear_active_step,
65	    latest_plan_meta_path,
66	    latest_plan_path,
67	    latest_plan_record,
68	    load_plan,
69	    load_plan_from_dir,
70	    load_plan_locked,
71	    make_history_entry,
72	    plan_lock,
73	    plan_lock_is_held,
74	    plan_lock_path,
75	    record_step_failure,
76	    resolve_plan_dir,
77	    save_state,
78	    set_active_step,
79	    store_raw_worker_output,
80	)
81	
82	# -- registries.py: flag + debt registries -----------------------------------
83	from .registries import (
84	    add_or_increment_debt,
85	    debt_by_subsystem,
86	    escalated_subsystems,
87	    extract_subsystem_tag,
88	    find_matching_debt,
89	    is_scope_creep_flag,
90	    load_debt_registry,
91	    load_flag_registry,
92	    next_debt_id,
93	    resolve_debt,
94	    save_debt_registry,
95	    save_flag_registry,
96	    scope_creep_flags,
97	    subsystem_occurrence_total,
98	    unresolved_significant_flags,
99	)
100	
101	# -- workflow.py: state machine, transitions ---------------------------------
102	from megaplan.types import ROBUSTNESS_LEVELS  # noqa: F401 — accessed by tests via megaplan._core
103	
104	from .workflow import (
105	    WORKFLOW,
106	    Transition,
107	    _ROBUSTNESS_OVERRIDES,
108	    configured_robustness,
109	    infer_next_steps,
110	    intent_and_notes_block,
111	    require_state,
112	    robustness_critique_instruction,
113	    workflow_includes_step,
114	    workflow_next,
115	    workflow_transition,
116	)
117	
118	__all__ = [
119	    # io
120	    "artifact_path",
121	    "atomic_write_json",
122	    "atomic_write_text",
123	    "batch_artifact_path",
124	    "collect_git_diff_patch",
125	    "collect_git_diff_summary",
126	    "compute_global_batches",
127	    "compute_task_batches",
128	    "config_dir",
129	    "current_iteration_artifact",
130	    "current_iteration_raw_artifact",
131	    "detect_available_agents",
132	    "ensure_runtime_layout",
133	    "find_command",
134	    "get_effective",
135	    "json_dump",
136	    "list_batch_artifacts",
137	    "load_config",
138	    "load_finalize_snapshot",
139	    "megaplan_root",
140	    "normalize_text",
141	    "now_utc",
142	    "plans_root",
143	    "read_json",
144	    "render_final_md",
145	    "save_config",
146	    "schemas_root",
147	    "sha256_file",
148	    "sha256_text",
149	    "slugify",
150	    # phase_runtime
151	    "DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS",
152	    "PHASE_RUNTIME_POLICY",
153	    "build_next_step_runtime",
154	    "build_phase_observability",
155	    "format_duration_hint",
156	    "humanize_seconds",
157	    "phase_runtime_policy",
158	    "phase_stale_seconds",
159	    "phase_timeout_seconds",
160	    "resolve_phase_runtime",
161	    # state
162	    "active_plan_dirs",
163	    "active_step_is_stale",
164	    "append_history",
165	    "apply_session_update",
166	    "clear_active_step",
167	    "latest_plan_meta_path",
168	    "latest_plan_path",
169	    "latest_plan_record",
170	    "load_plan",
171	    "load_plan_from_dir",
172	    "load_plan_locked",
173	    "make_history_entry",
174	    "plan_lock",
175	    "plan_lock_is_held",
176	    "plan_lock_path",
177	    "record_step_failure",
178	    "resolve_plan_dir",
179	    "save_state",
180	    "set_active_step",
181	    "store_raw_worker_output",
182	    # registries
183	    "add_or_increment_debt",
184	    "debt_by_subsystem",
185	    "escalated_subsystems",
186	    "extract_subsystem_tag",
187	    "find_matching_debt",
188	    "is_scope_creep_flag",
189	    "load_debt_registry",
190	    "load_flag_registry",
191	    "next_debt_id",
192	    "resolve_debt",
193	    "save_debt_registry",
194	    "save_flag_registry",
195	    "scope_creep_flags",
196	    "subsystem_occurrence_total",
197	    "unresolved_significant_flags",
198	    # workflow
199	    "WORKFLOW",
200	    "Transition",
201	    "_ROBUSTNESS_OVERRIDES",
202	    "configured_robustness",
203	    "infer_next_steps",
204	    "intent_and_notes_block",
205	    "require_state",
206	    "robustness_critique_instruction",
207	    "workflow_includes_step",
208	    "workflow_next",
209	    "workflow_transition",
210	]
211
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
13	    STATE_CRITIQUED,
14	    STATE_DONE,
15	    STATE_EXECUTED,
16	    STATE_FINALIZED,
17	    STATE_GATED,
18	    STATE_INITIALIZED,
19	    STATE_PLANNED,
20	    STATE_PREPPED,
21	)
22	
23	
24	@dataclass(frozen=True)
25	class Transition:
26	    next_step: str
27	    next_state: str
28	    condition: str = "always"
29	
30	
31	WORKFLOW: dict[str, list[Transition]] = {
32	    STATE_INITIALIZED: [
33	        Transition("prep", STATE_PREPPED),
34	    ],
35	    STATE_PREPPED: [
36	        Transition("plan", STATE_PLANNED),
37	    ],
38	    STATE_PLANNED: [
39	        Transition("critique", STATE_CRITIQUED),
40	        Transition("plan", STATE_PLANNED),
41	    ],
42	    STATE_CRITIQUED: [
43	        Transition("gate", STATE_GATED, "gate_unset"),
44	        Transition("revise", STATE_PLANNED, "gate_iterate"),
45	        Transition("override add-note", STATE_CRITIQUED, "gate_escalate"),
46	        Transition("override force-proceed", STATE_GATED, "gate_escalate"),
47	        Transition("override abort", STATE_ABORTED, "gate_escalate"),
48	        Transition("revise", STATE_PLANNED, "gate_proceed_blocked"),
49	        Transition("override force-proceed", STATE_GATED, "gate_proceed_blocked"),
50	        Transition("gate", STATE_GATED, "gate_proceed"),
51	    ],
52	    STATE_GATED: [
53	        Transition("finalize", STATE_FINALIZED),
54	        Transition("override replan", STATE_PLANNED),
55	    ],
56	    STATE_FINALIZED: [
57	        Transition("execute", STATE_EXECUTED),
58	        Transition("override replan", STATE_PLANNED),
59	    ],
60	    STATE_EXECUTED: [
61	        # `handle_review()` may also return STATE_FINALIZED on a `needs_rework`
62	        # verdict. That rework loop depends on review payload semantics rather
63	        # than gate_* conditions, so it lives in the handler instead of here
64	        # because `_transition_matches()` only understands gate-based branches.
65	        Transition("review", STATE_DONE),
66	    ],
67	}
68	
69	# Each level's *own* overrides (not inherited).  Levels inherit from the
70	# level below them via _ROBUSTNESS_HIERARCHY so shared transitions are
71	# declared once: robust/superrobust have none, standard keeps the
72	# planned->critique routing documented explicitly, and light skips
73	# prep plus gate/review.
74	_ROBUSTNESS_OVERRIDES: dict[str, dict[str, list[Transition]]] = {
75	    "superrobust": {},
76	    "robust": {},
77	    "standard": {
78	        STATE_INITIALIZED: [
79	            Transition("plan", STATE_PLANNED),
80	        ],
81	    },
82	    "light": {
83	        STATE_INITIALIZED: [
84	            Transition("plan", STATE_PLANNED),
85	        ],
86	        STATE_CRITIQUED: [
87	            Transition("revise", STATE_GATED),
88	        ],
89	        STATE_EXECUTED: [],
90	    },
91	    "tiny": {},
92	}
93	
94	_ROBUSTNESS_WORKFLOW_LEVELS: dict[str, tuple[str, ...]] = {
95	    "superrobust": ("superrobust",),
96	    "robust": ("robust",),
97	    "standard": ("standard",),
98	    "light": ("standard", "light"),
99	    "tiny": ("standard", "light", "tiny"),
100	}
101	
102	_STEP_CONTEXT_STATES = {
103	    STATE_PLANNED,
104	    STATE_CRITIQUED,
105	    STATE_GATED,
106	    STATE_FINALIZED,
107	}
108	
109	
110	# ---------------------------------------------------------------------------
111	# Robustness helpers
112	# ---------------------------------------------------------------------------
113	
114	def configured_robustness(state: PlanState) -> str:
115	    robustness = state["config"].get("robustness", "standard")
116	    if robustness not in ROBUSTNESS_LEVELS:
117	        return "standard"
118	    return robustness
119	
120	
121	def robustness_critique_instruction(robustness: str) -> str:
122	    if robustness == "light":
123	        return "Be pragmatic. Only flag issues that would cause real failures. Ignore style, minor edge cases, and issues the executor will naturally resolve."
124	    return "Use balanced judgment. Flag significant risks, but do not spend flags on minor polish or executor-obvious boilerplate."
125	
126	
127	# ---------------------------------------------------------------------------
128	# Intent / notes block for prompts
129	# ---------------------------------------------------------------------------
130	
131	def intent_and_notes_block(state: PlanState) -> str:
132	    sections = []
133	    clarification = state.get("clarification", {})
134	    if clarification.get("intent_summary"):
135	        sections.append(f"User intent summary:\n{clarification['intent_summary']}")
136	        sections.append(f"Original idea:\n{state['idea']}")
137	    else:
138	        sections.append(f"Idea:\n{state['idea']}")
139	    notes = state["meta"].get("notes", [])
140	    if notes:
141	        notes_text = "\n".join(f"- {note['note']}" for note in notes)
142	        sections.append(f"User notes and answers:\n{notes_text}")
143	    return "\n\n".join(sections)
144	
145	
146	# ---------------------------------------------------------------------------
147	# Transition logic
148	# ---------------------------------------------------------------------------
149	
150	def _normalize_workflow_robustness(robustness: Any) -> str:
151	    if robustness in ROBUSTNESS_LEVELS:
152	        return str(robustness)
153	    return "standard"
154	
155	
156	def _workflow_robustness_from_state(state: PlanState) -> str:
157	    config = state.get("config", {})
158	    if not isinstance(config, dict):
159	        return "standard"
160	    return _normalize_workflow_robustness(config.get("robustness", "standard"))
161	
162	
163	def _workflow_for_robustness(robustness: str) -> dict[str, list[Transition]]:
164	    normalized = _normalize_workflow_robustness(robustness)
165	    merged = dict(WORKFLOW)
166	    for level in _ROBUSTNESS_WORKFLOW_LEVELS.get(normalized, _ROBUSTNESS_WORKFLOW_LEVELS["standard"]):
167	        merged.update(_ROBUSTNESS_OVERRIDES.get(level, {}))
168	    return merged
169	
170	
171	def _transition_matches(state: PlanState, condition: str) -> bool:
172	    if condition == "always":
173	        return True
174	    gate = state.get("last_gate", {})
175	    if not isinstance(gate, dict):
176	        gate = {}
177	    recommendation = gate.get("recommendation")
178	    if condition == "gate_unset":
179	        return not recommendation
180	    if condition == "gate_iterate":
181	        return recommendation == "ITERATE"
182	    if condition == "gate_escalate":
183	        return recommendation == "ESCALATE"
184	    if condition == "gate_proceed_blocked":
185	        return recommendation == "PROCEED" and not gate.get("passed", False)
186	    if condition == "gate_proceed":
187	        return recommendation == "PROCEED" and gate.get("passed", False)
188	    return False
189	
190	
191	def workflow_includes_step(robustness: str, step: str) -> bool:
192	    if step == "step":
193	        return True
194	    workflow = _workflow_for_robustness(robustness)
195	    return any(
196	        transition.next_step == step
197	        for transitions in workflow.values()
198	        for transition in transitions
199	    )
200	
201	
202	def workflow_transition(state: PlanState, step: str) -> Transition | None:
203	    current = state.get("current_state")
204	    if not isinstance(current, str):
205	        return None
206	    workflow = _workflow_for_robustness(_workflow_robustness_from_state(state))
207	    for transition in workflow.get(current, []):
208	        if transition.next_step == step and _transition_matches(state, transition.condition):
209	            return transition
210	    return None
211	
212	
213	def workflow_next(state: PlanState) -> list[str]:
214	    current = state.get("current_state")
215	    if not isinstance(current, str):
216	        return []
217	    workflow = _workflow_for_robustness(_workflow_robustness_from_state(state))
218	    next_steps = [
219	        transition.next_step
220	        for transition in workflow.get(current, [])
221	        if _transition_matches(state, transition.condition)
222	    ]
223	    if current in _STEP_CONTEXT_STATES:
224	        next_steps.append("step")
225	    return next_steps
226	
227	
228	infer_next_steps = workflow_next
229	
230	
231	def require_state(state: PlanState, step: str, allowed: set[str]) -> None:
232	    current = state["current_state"]
233	    if current not in allowed:
234	        raise CliError(
235	            "invalid_transition",
236	            f"Cannot run '{step}' while current state is '{current}'",
237	            valid_next=infer_next_steps(state),
238	            extra={"current_state": current},
239	        )
240
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 1,
  "limit": 120
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	import argparse
4	import inspect
5	import logging
6	import os
7	import shutil
8	import subprocess
9	import sys
10	from datetime import datetime
11	from pathlib import Path
12	from typing import Any, Callable
13	
14	import megaplan.review_checks as review_checks
15	import megaplan.workers as worker_module
16	from megaplan.checks import checks_for_robustness, validate_critique_checks
17	from megaplan.execution import (
18	    _check_done_task_evidence,
19	    build_monitor_hint,
20	    handle_execute_auto_loop as dispatch_execute_auto_loop,
21	    handle_execute_one_batch as dispatch_execute_one_batch,
22	)
23	from megaplan.flags import (
24	    update_flags_after_critique,
25	    update_flags_after_gate,
26	    update_flags_after_review,
27	    update_flags_after_revise,
28	)
29	from megaplan.merge import _validate_and_merge_batch
30	from megaplan.parallel_critique import run_parallel_critique
31	from megaplan.parallel_review import run_parallel_review
32	from megaplan.prompts import create_claude_prompt, create_codex_prompt, create_hermes_prompt
33	from megaplan.review_mechanical import run_pre_checks
34	from megaplan.step_edit import next_plan_artifact_name
35	from megaplan.types import (
36	    FLAG_BLOCKING_STATUSES,
37	    MOCK_ENV_VAR,
38	    ROBUSTNESS_LEVELS,
39	    CliError,
40	    PlanState,
41	    STATE_ABORTED,
42	    STATE_CRITIQUED,
43	    STATE_DONE,
44	    STATE_EXECUTED,
45	    STATE_FINALIZED,
46	    STATE_GATED,
47	    STATE_INITIALIZED,
48	    STATE_PREPPED,
49	    STATE_PLANNED,
50	    StepResponse,
51	)
52	from megaplan._core import (
53	    add_or_increment_debt,
54	    append_history,
55	    apply_session_update,
56	    atomic_write_json,
57	    atomic_write_text,
58	    build_next_step_runtime,
59	    clear_active_step,
60	    configured_robustness,
61	    ensure_runtime_layout,
62	    extract_subsystem_tag,
63	    latest_plan_path,
64	    load_debt_registry,
65	    load_flag_registry,
66	    load_plan,
67	    load_plan_locked,
68	    make_history_entry,
69	    now_utc,
70	    plans_root,
71	    read_json,
72	    record_step_failure,
73	    render_final_md,
74	    save_debt_registry,
75	    save_flag_registry,
76	    save_state,
77	    scope_creep_flags,
78	    set_active_step,
79	    sha256_file,
80	    sha256_text,
81	    slugify,
82	    unresolved_significant_flags,
83	    get_effective,
84	    workflow_includes_step,
85	    workflow_transition,
86	    workflow_next,
87	)
88	from megaplan._core.phase_runtime import (
89	    DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
90	    PHASE_RUNTIME_POLICY,
91	    format_duration_hint,
92	)
93	from megaplan.evaluation import (
94	    PLAN_STRUCTURE_REQUIRED_STEP_ISSUE,
95	    build_gate_artifact,
96	    build_gate_signals,
97	    build_orchestrator_guidance,
98	    compute_plan_delta_percent,
99	    compute_recurring_critiques,
100	    is_rubber_stamp,
101	    run_gate_checks,
102	    validate_plan_structure,
103	)
104	from megaplan.workers import resolve_agent_mode
105	from megaplan._core import find_command, infer_next_steps, require_state
106	from megaplan.workers import WorkerResult, validate_payload
107	
108	log = logging.getLogger("megaplan")
109	
110	
111	def _append_to_meta(state: PlanState, field: str, value: Any) -> None:
112	    state["meta"].setdefault(field, []).append(value)
113	
114	
115	def attach_agent_fallback(response: StepResponse, args: argparse.Namespace) -> None:
116	    if hasattr(args, "_agent_fallback"):
117	        response["agent_fallback"] = args._agent_fallback
118	
119	
120	def _attach_next_step_runtime(response: StepResponse) -> None:
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execution.py",
  "offset": 1,
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	import argparse
4	from dataclasses import dataclass
5	from pathlib import Path
6	from typing import Any, Callable
7	
8	import megaplan.workers as worker_module
9	from megaplan._core import (
10	    apply_session_update,
11	    append_history,
12	    atomic_write_json,
13	    atomic_write_text,
14	    batch_artifact_path,
15	    build_next_step_runtime,
16	    compute_global_batches,
17	    compute_task_batches,
18	    get_effective,
19	    list_batch_artifacts,
20	    load_config,
21	    make_history_entry,
22	    record_step_failure,
23	    read_json,
24	    render_final_md,
25	    save_state,
26	    sha256_file,
27	    store_raw_worker_output,
28	)
29	from megaplan.evaluation import validate_execution_evidence
30	from megaplan.execution_quality import (
31	    _capture_git_status_snapshot,
32	    _check_done_task_evidence,
33	    _collect_quality_deviations,
34	    _observe_git_changes,
35	)
36	from megaplan.execution_timeout import (
37	    _recover_execute_timeout,
38	    _resolve_execute_approval_mode,
39	)
40	from megaplan.merge import _validate_and_merge_batch
41	from megaplan.prompts import _execute_batch_prompt
42	from megaplan.quality import capture_before_line_counts
43	from megaplan.types import (
44	    CliError,
45	    PlanState,
46	    STATE_EXECUTED,
47	    STATE_FINALIZED,
48	    StepResponse,
49	)
50	from megaplan.workers import WorkerResult
51	
52	
53	@dataclass
54	class BatchResult:
55	    worker: WorkerResult
56	    agent: str
57	    mode: str
58	    refreshed: bool
59	    payload: dict[str, Any]
60	    batch_number: int
61	    batch_task_ids: list[str]
62	    batch_sense_check_ids: list[str]
63	    merged_task_count: int
64	    total_task_count: int
65	    acknowledged_sense_check_count: int
66	    total_sense_check_count: int
67	    missing_task_evidence: list[str]
68	    execution_audit: dict[str, Any]
69	    finalize_hash: str
70	
71	
72	def build_monitor_hint(plan_dir: Path) -> str:
73	    return f"Use `megaplan status --plan {plan_dir.name}` for updates."
74	
75	
76	def _attach_next_step_runtime(response: StepResponse) -> None:
77	    runtime = build_next_step_runtime(
78	        response.get("next_step"),
79	        configured_timeout_seconds=int(get_effective("execution", "worker_timeout_seconds")),
80	    )
81	    if runtime is not None:
82	        response["next_step_runtime"] = runtime
83	
84	
85	def _format_execute_tracking_note(
86	    *,
87	    merged_count: int,
88	    total_tasks: int,
89	    acknowledged_count: int,
90	    total_checks: int,
91	) -> str:
92	    tracking_bits: list[str] = []
93	    if total_tasks > 0:
94	        tracking_bits.append(f"{merged_count}/{total_tasks} tasks tracked")
95	    if total_checks > 0:
96	        tracking_bits.append(
97	            f"{acknowledged_count}/{total_checks} sense checks acknowledged"
98	        )
99	    return f" ({', '.join(tracking_bits)})" if tracking_bits else ""
100
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/workers.py",
  "offset": 1,
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	"""Worker orchestration: running Claude and Codex steps."""
2	
3	from __future__ import annotations
4	
5	import argparse
6	import hashlib
7	import json
8	import os
9	import re
10	import shutil
11	import subprocess
12	import tempfile
13	import textwrap
14	import time
15	import uuid
16	from dataclasses import dataclass
17	from pathlib import Path
18	from typing import Any, Callable
19	
20	from megaplan.checks import build_empty_template, checks_for_robustness
21	from megaplan.schemas import SCHEMAS
22	from megaplan.types import (
23	    CliError,
24	    DEFAULT_AGENT_ROUTING,
25	    MOCK_ENV_VAR,
26	    PlanState,
27	    SessionInfo,
28	    parse_agent_spec,
29	)
30	from megaplan._core import (
31	    apply_session_update,
32	    configured_robustness,
33	    detect_available_agents,
34	    phase_timeout_seconds,
35	    get_effective,
36	    json_dump,
37	    latest_plan_meta_path,
38	    load_config,
39	    now_utc,
40	    read_json,
41	    schemas_root,
42	)
43	from megaplan.prompts import create_claude_prompt, create_codex_prompt
44	
45	
46	_EXECUTE_STEPS = {"execute", "loop_execute"}
47	_CODEX_TEMPLATE_WRITE_STEPS = {"critique", "review"}
48	
49	# Shared mapping from step name to schema filename, used by both
50	# run_claude_step and run_codex_step.
51	STEP_SCHEMA_FILENAMES: dict[str, str] = {
52	    "plan": "plan.json",
53	    "prep": "prep.json",
54	    "revise": "revise.json",
55	    "critique": "critique.json",
56	    "gate": "gate.json",
57	    "finalize": "finalize.json",
58	    "execute": "execution.json",
59	    "loop_plan": "loop_plan.json",
60	    "loop_execute": "loop_execute.json",
61	    "review": "review.json",
62	}
63	
64	# Derive required keys per step from SCHEMAS so they aren't duplicated.
65	_STEP_REQUIRED_KEYS: dict[str, list[str]] = {
66	    step: SCHEMAS[filename].get("required", [])
67	    for step, filename in STEP_SCHEMA_FILENAMES.items()
68	}
69	
70	
71	@dataclass
72	class CommandResult:
73	    command: list[str]
74	    cwd: Path
75	    returncode: int
76	    stdout: str
77	    stderr: str
78	    duration_ms: int
79	
80
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/workers.py",
  "offset": 80,
  "limit": 150
}
```

> TOOL

tool_result Read
```
80	
81	@dataclass
82	class WorkerResult:
83	    payload: dict[str, Any]
84	    raw_output: str
85	    duration_ms: int
86	    cost_usd: float
87	    session_id: str | None = None
88	    trace_output: str | None = None
89	    prompt_tokens: int = 0
90	    completion_tokens: int = 0
91	    total_tokens: int = 0
92	
93	
94	def run_command(
95	    command: list[str],
96	    *,
97	    cwd: Path,
98	    stdin_text: str | None = None,
99	    env: dict[str, str] | None = None,
100	    timeout: int | None = None,
101	) -> CommandResult:
102	    started = time.monotonic()
103	    timeout = timeout or get_effective("execution", "worker_timeout_seconds")
104	    try:
105	        process = subprocess.run(
106	            command,
107	            cwd=str(cwd),
108	            input=stdin_text,
109	            text=True,
110	            capture_output=True,
111	            env=env,
112	            timeout=timeout,
113	        )
114	    except FileNotFoundError as exc:
115	        raise CliError(
116	            "agent_not_found",
117	            f"Command not found: {command[0]}",
118	        ) from exc
119	    except subprocess.TimeoutExpired as exc:
120	        def _coerce_timeout_output(value: Any) -> str:
121	            if value is None:
122	                return ""
123	            if isinstance(value, bytes):
124	                return value.decode("utf-8", errors="replace")
125	            return str(value)
126	
127	        raise CliError(
128	            "worker_timeout",
129	            f"Command timed out after {timeout}s: {' '.join(command[:3])}...",
130	            extra={"raw_output": _coerce_timeout_output(exc.stdout) + _coerce_timeout_output(exc.stderr)},
131	        ) from exc
132	    return CommandResult(
133	        command=command,
134	        cwd=cwd,
135	        returncode=process.returncode,
136	        stdout=process.stdout,
137	        stderr=process.stderr,
138	        duration_ms=int((time.monotonic() - started) * 1000),
139	    )
140	
141	
142	_CODEX_ERROR_PATTERNS: list[tuple[str, str, str]] = [
143	    # (pattern_substring, error_code, human_message)
144	    # Keep transport failures ahead of generic HTTP/status matches so
145	    # thread IDs or unrelated numbers do not get misclassified as 429s.
146	    ("failed to lookup address information", "connection_error", "Codex could not resolve the backend host"),
147	    ("failed to connect to websocket", "connection_error", "Codex could not connect to the realtime backend"),
148	    ("stream disconnected before completion", "connection_error", "Codex connection dropped before completion"),
149	    ("error sending request for url", "connection_error", "Codex could not send the backend request"),
150	    ("nodename nor servname provided", "connection_error", "Codex could not resolve the backend host"),
151	    ("connection error", "connection_error", "Codex could not connect to the API"),
152	    ("connection refused", "connection_error", "Codex could not connect to the API"),
153	    ("rate limit", "rate_limit", "Codex hit a rate limit"),
154	    ("rate_limit", "rate_limit", "Codex hit a rate limit"),
155	    ("quota", "quota_exceeded", "Codex quota exceeded"),
156	    ("context length", "context_overflow", "Prompt exceeded Codex context length"),
157	    ("context_length", "context_overflow", "Prompt exceeded Codex context length"),
158	    ("maximum context", "context_overflow", "Prompt exceeded Codex context length"),
159	    ("too many tokens", "context_overflow", "Prompt exceeded Codex context length"),
160	    ("timed out", "worker_timeout", "Codex request timed out"),
161	    ("timeout", "worker_timeout", "Codex request timed out"),
162	    ("invalid_json_schema", "schema_error", "Codex request rejected: invalid JSON schema"),
163	    ("invalid_request_error", "schema_error", "Codex request rejected: invalid request"),
164	    ("internal server error", "api_error", "Codex API returned an internal error"),
165	    ("model not found", "model_error", "Codex model not found or unavailable"),
166	    ("permission denied", "permission_error", "Codex permission denied"),
167	    ("authentication", "auth_error", "Codex authentication failed"),
168	    ("unauthorized", "auth_error", "Codex authentication failed"),
169	]
170	
171	
172	def _codex_retry_guidance(step: str | None = None) -> str:
173	    if step in _EXECUTE_STEPS:
174	        return (
175	            "Re-run the same execute step on Codex once before changing agent; "
176	            "preserve the existing session path unless a fresh retry is explicitly needed."
177	        )
178	    return "Re-run the same step on Codex once before changing agent."
179	
180	
181	def _diagnose_codex_failure(raw: str, returncode: int) -> tuple[str, str]:
182	    """Parse Codex stderr/stdout for known error patterns. Returns (error_code, message)."""
183	    lower = raw.lower()
184	    for pattern, code, message in _CODEX_ERROR_PATTERNS:
185	        if pattern in lower:
186	            return code, f"{message}. {_codex_retry_guidance()}"
187	    if re.search(r"\bhttp\s*429\b", lower) or re.search(r"\b429\b", lower):
188	        return "rate_limit", f"Codex hit a rate limit (HTTP 429). {_codex_retry_guidance()}"
189	    if re.search(r"\bhttp\s*400\b", lower) or re.search(r"\b400\b", lower):
190	        return "schema_error", f"Codex API rejected request (HTTP 400). {_codex_retry_guidance()}"
191	    if re.search(r"\bhttp\s*500\b", lower) or re.search(r"\b500\b", lower):
192	        return "api_error", f"Codex API returned an internal error (HTTP 500). {_codex_retry_guidance()}"
193	    if re.search(r"\bhttp\s*502\b", lower) or re.search(r"\b502\b", lower):
194	        return "api_error", f"Codex API returned a gateway error (HTTP 502). {_codex_retry_guidance()}"
195	    if re.search(r"\bhttp\s*503\b", lower) or re.search(r"\b503\b", lower):
196	        return "api_error", f"Codex API service unavailable (HTTP 503). {_codex_retry_guidance()}"
197	    return "worker_error", (
198	        f"Codex step failed with exit code {returncode} (no recognized error pattern in output). "
199	        + _codex_retry_guidance()
200	    )
201	
202	
203	def _codex_timeout_for_step(step: str) -> int:
204	    configured_timeout = int(get_effective("execution", "worker_timeout_seconds"))
205	    return phase_timeout_seconds(step, configured_timeout_seconds=configured_timeout)
206	
207	
208	def _codex_exec_mode_flags(step: str) -> list[str]:
209	    if step in _EXECUTE_STEPS or step in _CODEX_TEMPLATE_WRITE_STEPS:
210	        # In trusted-container mode we pass --dangerously-bypass-approvals-and-sandbox
211	        # elsewhere in the invocation, and Codex rejects the combination of
212	        # --full-auto + --dangerously-bypass-approvals-and-sandbox (they both
213	        # configure approval/sandbox and conflict). Skip --full-auto here;
214	        # the bypass flag already grants the auto-approval behavior needed.
215	        if _trusted_container():
216	            return []
217	        return ["--full-auto"]
218	    return []
219	
220	
221	_ROLLOUT_MISSING_PATTERNS = (
222	    "no rollout found for thread id",
223	    "thread/resume failed",
224	)
225	
226	
227	def _is_rollout_missing(raw: str) -> bool:
228	    """Detect Codex's signal that a session/thread id has no rollout.
229
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 120,
  "limit": 200
}
```

> TOOL

tool_result Read
```
120	def _attach_next_step_runtime(response: StepResponse) -> None:
121	    runtime = build_next_step_runtime(
122	        response.get("next_step"),
123	        configured_timeout_seconds=int(get_effective("execution", "worker_timeout_seconds")),
124	    )
125	    if runtime is not None:
126	        response["next_step_runtime"] = runtime
127	
128	
129	def _build_review_blocked_message(
130	    *,
131	    verdict_count: int,
132	    total_tasks: int,
133	    check_count: int,
134	    total_checks: int,
135	    missing_reviewer_evidence: list[str],
136	) -> str:
137	    if missing_reviewer_evidence:
138	        return (
139	            "Blocked: done tasks are missing reviewer evidence_files without a substantive reviewer_verdict ("
140	            + ", ".join(missing_reviewer_evidence)
141	            + "). Re-run review to complete."
142	        )
143	    return (
144	        "Blocked: incomplete review coverage "
145	        f"({verdict_count}/{total_tasks} task verdicts, {check_count}/{total_checks} sense checks). "
146	        "Re-run review to complete."
147	    )
148	
149	
150	def _is_substantive_reviewer_verdict(text: str) -> bool:
151	    return not is_rubber_stamp(text, strict=True)
152	
153	
154	_AUTO_NEXT_STEP = object()
155	
156	
157	def _emit_phase_notice(step: str) -> None:
158	    if step not in PHASE_RUNTIME_POLICY:
159	        return
160	    duration_hint = format_duration_hint(
161	        step,
162	        configured_timeout_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
163	    )
164	    print(f"[megaplan] Starting {step}... {duration_hint}", file=sys.stderr)
165	
166	
167	def _run_worker(
168	    step: str,
169	    state: PlanState,
170	    plan_dir: Path,
171	    args: argparse.Namespace,
172	    *,
173	    root: Path,
174	    iteration: int | None = None,
175	    resolved: tuple[str, str, bool, str | None] | None = None,
176	    prompt_override: str | None = None,
177	    prompt_kwargs: dict[str, Any] | None = None,
178	) -> tuple[WorkerResult, str, str, bool]:
179	    failure_iteration = state["iteration"] if iteration is None else iteration
180	    agent, mode, refreshed, model = resolved or resolve_agent_mode(step, args)
181	    run_id = set_active_step(state, step=step, agent=agent, mode=mode, model=model)
182	    _emit_phase_notice(step)
183	    save_state(plan_dir, state)
184	    try:
185	        run_step_kwargs: dict[str, Any] = {
186	            "root": root,
187	            "resolved": (agent, mode, refreshed, model),
188	            "prompt_override": prompt_override,
189	        }
190	        if prompt_kwargs is not None and _supports_prompt_kwargs(worker_module.run_step_with_worker):
191	            run_step_kwargs["prompt_kwargs"] = prompt_kwargs
192	        return worker_module.run_step_with_worker(
193	            step,
194	            state,
195	            plan_dir,
196	            args,
197	            **run_step_kwargs,
198	        )
199	    except CliError as error:
200	        clear_active_step(state, run_id=run_id)
201	        record_step_failure(plan_dir, state, step=step, iteration=failure_iteration, error=error)
202	        raise
203	    except Exception:
204	        clear_active_step(state, run_id=run_id)
205	        save_state(plan_dir, state)
206	        raise
207	
208	
209	def _supports_prompt_kwargs(run_step: Callable[..., Any]) -> bool:
210	    params = inspect.signature(run_step).parameters.values()
211	    return any(param.name == "prompt_kwargs" for param in params) or any(
212	        param.kind == inspect.Parameter.VAR_KEYWORD for param in params
213	    )
214	
215	
216	def _build_review_prompt_override(
217	    agent_type: str,
218	    state: PlanState,
219	    plan_dir: Path,
220	    *,
221	    root: Path,
222	    pre_check_flags: list[dict[str, Any]],
223	) -> str:
224	    if agent_type == "claude":
225	        return create_claude_prompt("review", state, plan_dir, root=root, pre_check_flags=pre_check_flags)
226	    if agent_type == "hermes":
227	        return create_hermes_prompt("review", state, plan_dir, root=root, pre_check_flags=pre_check_flags)
228	    return create_codex_prompt("review", state, plan_dir, root=root, pre_check_flags=pre_check_flags)
229	
230	
231	def _build_gate_prompt_override(
232	    agent_type: str,
233	    state: PlanState,
234	    plan_dir: Path,
235	    *,
236	    root: Path,
237	    missing_flag_ids: list[str],
238	) -> str:
239	    if agent_type == "claude":
240	        base_prompt = create_claude_prompt("gate", state, plan_dir, root=root)
241	    elif agent_type == "hermes":
242	        base_prompt = create_hermes_prompt("gate", state, plan_dir, root=root)
243	    else:
244	        base_prompt = create_codex_prompt("gate", state, plan_dir, root=root)
245	    missing_flags = ", ".join(missing_flag_ids)
246	    addendum = (
247	        "Gate retry for the same iteration.\n"
248	        "Your previous response recommended PROCEED but left blocking flags unresolved.\n"
249	        f"Missing blocking flag IDs: {missing_flags}.\n"
250	        "Return a complete gate response. If you recommend PROCEED, you MUST include "
251	        "`flag_resolutions` entries for every blocking flag. If you cannot resolve every "
252	        "blocking flag, return ITERATE or ESCALATE instead."
253	    )
254	    return f"{base_prompt}\n\n{addendum}"
255	
256	
257	def _finish_step(
258	    plan_dir: Path,
259	    state: PlanState,
260	    args: argparse.Namespace,
261	    *,
262	    step: str,
263	    worker: WorkerResult,
264	    agent: str,
265	    mode: str,
266	    refreshed: bool,
267	    summary: str,
268	    artifacts: list[str],
269	    output_file: str,
270	    artifact_hash: str,
271	    result: str = "success",
272	    success: bool = True,
273	    next_step: object | str | None = _AUTO_NEXT_STEP,
274	    response_fields: dict[str, Any] | None = None,
275	    history_fields: dict[str, Any] | None = None,
276	    run_id: str | None = None,
277	) -> StepResponse:
278	    clear_active_step(state, run_id=run_id)
279	    apply_session_update(state, step, agent, worker.session_id, mode=mode, refreshed=refreshed)
280	    append_history(
281	        state,
282	        make_history_entry(
283	            step,
284	            duration_ms=worker.duration_ms,
285	            cost_usd=worker.cost_usd,
286	            result=result,
287	            worker=worker,
288	            agent=agent,
289	            mode=mode,
290	            output_file=output_file,
291	            artifact_hash=artifact_hash,
292	            prompt_tokens=worker.prompt_tokens,
293	            completion_tokens=worker.completion_tokens,
294	            total_tokens=worker.total_tokens,
295	            **(history_fields or {}),
296	        ),
297	    )
298	    save_state(plan_dir, state)
299	    resolved_next = next_step
300	    if resolved_next is _AUTO_NEXT_STEP:
301	        next_steps = workflow_next(state)
302	        resolved_next = next_steps[0] if next_steps else None
303	    response: StepResponse = {
304	        "success": success,
305	        "step": step,
306	        "summary": summary,
307	        "artifacts": artifacts,
308	        "monitor_hint": build_monitor_hint(plan_dir),
309	        "next_step": resolved_next,
310	        "state": state["current_state"],
311	    }
312	    if response_fields:
313	        response.update(response_fields)
314	    _attach_next_step_runtime(response)
315	    attach_agent_fallback(response, args)
316	    return response
317	
318	
319	def _raise_step_validation_error(
```

> TOOL

tool_use Grep
```json
{
  "pattern": "^def handle_",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "output_mode": "content",
  "context": 2
}
```

> TOOL

tool_result Grep
```
715-
716-
717:def handle_init(root: Path, args: argparse.Namespace) -> StepResponse:
718-    ensure_runtime_layout(root)
719-    project_dir = Path(args.project_dir).expanduser().resolve()
--
792-
793-
794:def handle_plan(root: Path, args: argparse.Namespace) -> StepResponse:
795-    with load_plan_locked(root, args.plan, step="plan") as (plan_dir, state):
796-        require_state(state, "plan", {STATE_INITIALIZED, STATE_PREPPED, STATE_PLANNED})
--
838-
839-
840:def handle_prep(root: Path, args: argparse.Namespace) -> StepResponse:
841-    with load_plan_locked(root, args.plan, step="prep") as (plan_dir, state):
842-        require_state(state, "prep", {STATE_INITIALIZED})
--
859-
860-
861:def handle_critique(root: Path, args: argparse.Namespace) -> StepResponse:
862-    with load_plan_locked(root, args.plan, step="critique") as (plan_dir, state):
863-        require_state(state, "critique", {STATE_PLANNED})
--
992-
993-
994:def handle_revise(root: Path, args: argparse.Namespace) -> StepResponse:
995-    with load_plan_locked(root, args.plan, step="revise") as (plan_dir, state):
996-        require_state(state, "revise", {STATE_CRITIQUED})
--
1047-
1048-
1049:def handle_gate(root: Path, args: argparse.Namespace) -> StepResponse:
1050-    with load_plan_locked(root, args.plan, step="gate") as (plan_dir, state):
1051-        require_state(state, "gate", {STATE_CRITIQUED})
--
1306-
1307-
1308:def handle_finalize(root: Path, args: argparse.Namespace) -> StepResponse:
1309-    with load_plan_locked(root, args.plan, step="finalize") as (plan_dir, state):
1310-        require_state(state, "finalize", {STATE_GATED})
--
1335-
1336-
1337:def handle_execute(root: Path, args: argparse.Namespace) -> StepResponse:
1338-    with load_plan_locked(root, args.plan, step="execute") as (plan_dir, state):
1339-        require_state(state, "execute", {STATE_FINALIZED})
--
1574-
1575-
1576:def handle_review(root: Path, args: argparse.Namespace) -> StepResponse:
1577-    with load_plan_locked(root, args.plan, step="review") as (plan_dir, state):
1578-        require_state(state, "review", {STATE_EXECUTED})
--
2014-
2015-
2016:def handle_override(root: Path, args: argparse.Namespace) -> StepResponse:
2017-    plan_dir, state = load_plan(root, args.plan)
2018-    action = args.override_action
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/__init__.py"
}
```

> TOOL

tool_result Read
```
1	"""Prompt builders for each megaplan step and dispatch tables."""
2	
3	from __future__ import annotations
4	
5	from functools import partial
6	from pathlib import Path
7	from typing import Callable
8	
9	from megaplan.types import CliError, PlanState
10	
11	from ._shared import (
12	    _debt_watch_lines,
13	    _escalated_debt_for_prompt,
14	    _finalize_debt_block,
15	    _gate_debt_block,
16	    _grouped_debt_for_prompt,
17	    _planning_debt_block,
18	    _render_prep_block,
19	    _resolve_prompt_root,
20	)
21	from .critique import (
22	    _critique_prompt,
23	    _revise_prompt,
24	    _write_critique_template,
25	)
26	from .execute import (
27	    _execute_approval_note,
28	    _execute_batch_prompt,
29	    _execute_nudges,
30	    _execute_prompt,
31	    _execute_rerun_guidance,
32	    _execute_review_block,
33	)
34	from .finalize import _finalize_prompt
35	from .gate import _collect_critique_summaries, _flag_summary, _gate_prompt
36	from .planning import PLAN_TEMPLATE, _plan_prompt, _prep_prompt
37	from .review import (
38	    _review_prompt,
39	    _settled_decisions_block,
40	    _settled_decisions_instruction,
41	    _write_review_template,
42	)
43	
44	_PromptBuilder = Callable[..., str]
45	
46	_CLAUDE_PROMPT_BUILDERS: dict[str, _PromptBuilder] = {
47	    "plan": _plan_prompt,
48	    "prep": _prep_prompt,
49	    "critique": _critique_prompt,
50	    "revise": _revise_prompt,
51	    "gate": _gate_prompt,
52	    "finalize": _finalize_prompt,
53	    "execute": _execute_prompt,
54	    "review": partial(
55	        _review_prompt,
56	        review_intro="Review the execution critically against user intent and observable success criteria.",
57	        criteria_guidance="Judge against the success criteria, not plan elegance.",
58	        task_guidance="Review each task by cross-referencing the executor's per-task `files_changed` and `commands_run` against the git diff and any audit findings.",
59	        sense_check_guidance="Review every sense check explicitly. Confirm concise executor acknowledgments when they are specific; dig deeper only when they are perfunctory or contradicted by the code.",
60	    ),
61	}
62	
63	_CODEX_PROMPT_BUILDERS: dict[str, _PromptBuilder] = {
64	    "plan": _plan_prompt,
65	    "prep": _prep_prompt,
66	    "critique": _critique_prompt,
67	    "revise": _revise_prompt,
68	    "gate": _gate_prompt,
69	    "finalize": _finalize_prompt,
70	    "execute": _execute_prompt,
71	    "review": partial(
72	        _review_prompt,
73	        review_intro="Review the implementation against the success criteria.",
74	        criteria_guidance="Verify each success criterion explicitly.",
75	        task_guidance="Cross-reference each task's `files_changed` and `commands_run` against the git diff and any audit findings.",
76	        sense_check_guidance="Review every `sense_check` explicitly and treat perfunctory acknowledgments as a reason to dig deeper.",
77	    ),
78	}
79	
80	_HERMES_PROMPT_BUILDERS: dict[str, _PromptBuilder] = {
81	    "plan": _plan_prompt,
82	    "prep": _prep_prompt,
83	    "critique": _critique_prompt,
84	    "revise": _revise_prompt,
85	    "gate": _gate_prompt,
86	    "finalize": _finalize_prompt,
87	    "execute": _execute_prompt,
88	    "review": partial(
89	        _review_prompt,
90	        review_intro="Review the execution critically against user intent and observable success criteria.",
91	        criteria_guidance="Judge against the success criteria, not plan elegance.",
92	        task_guidance="Review each task by cross-referencing the executor's per-task `files_changed` and `commands_run` against the git diff and any audit findings.",
93	        sense_check_guidance="Review every sense check explicitly. Confirm concise executor acknowledgments when they are specific; dig deeper only when they are perfunctory or contradicted by the code.",
94	    ),
95	}
96	
97	_NESTED_HARNESS_GUARD = (
98	    "You are already running inside the megaplan harness for this step. "
99	    "Do the requested planning/review/execution work directly. "
100	    "Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, "
101	    "do NOT start nested megaplan plans, and do NOT recurse into another planning harness. "
102	    "Treat mentions of megaplan in the repository or environment as implementation context only."
103	)
104	
105	
106	def _prepend_harness_guard(prompt: str) -> str:
107	    return f"{_NESTED_HARNESS_GUARD}\n\n{prompt}"
108	
109	
110	def create_claude_prompt(
111	    step: str, state: PlanState, plan_dir: Path, root: Path | None = None, **prompt_kwargs: object
112	) -> str:
113	    builder = _CLAUDE_PROMPT_BUILDERS.get(step)
114	    if builder is None:
115	        raise CliError("unsupported_step", f"Unsupported Claude step '{step}'")
116	    if step == "review":
117	        return _prepend_harness_guard(builder(state, plan_dir, **prompt_kwargs))
118	    if step in {"prep", "critique", "gate", "finalize", "execute"}:
119	        return _prepend_harness_guard(builder(state, plan_dir, root=root))
120	    return _prepend_harness_guard(builder(state, plan_dir))
121	
122	
123	def create_codex_prompt(
124	    step: str, state: PlanState, plan_dir: Path, root: Path | None = None, **prompt_kwargs: object
125	) -> str:
126	    builder = _CODEX_PROMPT_BUILDERS.get(step)
127	    if builder is None:
128	        raise CliError("unsupported_step", f"Unsupported Codex step '{step}'")
129	    if step == "review":
130	        return _prepend_harness_guard(builder(state, plan_dir, **prompt_kwargs))
131	    if step in {"prep", "critique", "gate", "finalize", "execute"}:
132	        return _prepend_harness_guard(builder(state, plan_dir, root=root))
133	    return _prepend_harness_guard(builder(state, plan_dir))
134	
135	
136	def create_hermes_prompt(
137	    step: str, state: PlanState, plan_dir: Path, root: Path | None = None, **prompt_kwargs: object
138	) -> str:
139	    builder = _HERMES_PROMPT_BUILDERS.get(step)
140	    if builder is None:
141	        raise CliError("unsupported_step", f"Unsupported Hermes step '{step}'")
142	    if step == "review":
143	        return _prepend_harness_guard(builder(state, plan_dir, **prompt_kwargs))
144	    if step in {"prep", "critique", "gate", "finalize", "execute"}:
145	        return _prepend_harness_guard(builder(state, plan_dir, root=root))
146	    return _prepend_harness_guard(builder(state, plan_dir))
147	
148	
149	__all__ = [
150	    "PLAN_TEMPLATE",
151	    "_CLAUDE_PROMPT_BUILDERS",
152	    "_CODEX_PROMPT_BUILDERS",
153	    "_HERMES_PROMPT_BUILDERS",
154	    "_collect_critique_summaries",
155	    "_critique_prompt",
156	    "_debt_watch_lines",
157	    "_escalated_debt_for_prompt",
158	    "_execute_approval_note",
159	    "_execute_batch_prompt",
160	    "_execute_nudges",
161	    "_execute_prompt",
162	    "_execute_rerun_guidance",
163	    "_execute_review_block",
164	    "_finalize_debt_block",
165	    "_finalize_prompt",
166	    "_flag_summary",
167	    "_gate_debt_block",
168	    "_gate_prompt",
169	    "_grouped_debt_for_prompt",
170	    "_plan_prompt",
171	    "_planning_debt_block",
172	    "_prep_prompt",
173	    "_write_critique_template",
174	    "_render_prep_block",
175	    "_resolve_prompt_root",
176	    "_review_prompt",
177	    "_revise_prompt",
178	    "_settled_decisions_block",
179	    "_settled_decisions_instruction",
180	    "_write_review_template",
181	    "create_claude_prompt",
182	    "create_codex_prompt",
183	    "create_hermes_prompt",
184	]
185
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/planning.py",
  "offset": 1,
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	"""Planning-phase prompt builders."""
2	
3	from __future__ import annotations
4	
5	import textwrap
6	from pathlib import Path
7	
8	from megaplan._core import (
9	    intent_and_notes_block,
10	    json_dump,
11	    latest_plan_meta_path,
12	    latest_plan_path,
13	    read_json,
14	)
15	from megaplan.types import PlanState
16	
17	from ._shared import _render_prep_block
18	
19	PLAN_TEMPLATE = textwrap.dedent(
20	    """
21	    Plan template — simple format (adapt to the actual repo and scope):
22	    ````md
23	    # Implementation Plan: [Title]
24	
25	    ## Overview
26	    Summarize the goal, current repository shape, and the constraints that matter.
27	
28	    ## Main Phase
29	
30	    ### Step 1: Audit the current behavior (`megaplan/prompts.py`)
31	    **Scope:** Small
32	    1. **Inspect** the current implementation and call out the exact insertion points (`megaplan/prompts.py:29`).
33	
34	    ### Step 2: Add the first change (`megaplan/evaluation.py`)
35	    **Scope:** Medium
36	    1. **Implement** the smallest viable change with exact file references (`megaplan/evaluation.py:1`).
37	    2. **Capture** any tricky behavior with a short example.
38	       ```python
39	       issues = validate_plan_structure(plan_text)
40	       ```
41	
42	    ### Step 3: Wire downstream behavior (`megaplan/handlers.py`, `megaplan/workers.py`)
43	    **Scope:** Medium
44	    1. **Update** the runtime flow in the touched files (`megaplan/handlers.py:400`, `megaplan/workers.py:199`).
45	
46	    ### Step 4: Prove the change (`tests/test_evaluation.py`, `tests/test_megaplan.py`)
47	    **Scope:** Small
48	    1. **Run** the cheapest targeted checks first (`tests/test_evaluation.py:1`).
49	    2. **Finish** with broader verification once the wiring is in place (`tests/test_megaplan.py:1`).
50	
51	    ## Execution Order
52	    1. Update prompts and mocks before enforcing stricter validation.
53	    2. Land higher-risk wiring after the validator and tests are ready.
54	
55	    ## Validation Order
56	    1. Start with focused unit tests.
57	    2. Run the broader suite after the flow changes are in place.
58	    ````
59	
60	    For complex plans, use multiple phases:
61	    ````md
62	    ## Phase 1: Foundation — Dependencies, DB, Types
63	
64	    ### Step 1: Install dependencies (`package.json`)
65	    ...
66	
67	    ### Step 2: Create database migration (`supabase/migrations/`)
68	    ...
69	
70	    ## Phase 2: Core Integration
71	
72	    ### Step 3: Port the main component (`src/components/`)
73	    ...
74	    ````
75	
76	    Template guidance:
77	    - Simple plans: use `## Main Phase` with `### Step N:` sections underneath.
78	    - Complex plans: use multiple `## Phase N:` sections, each containing `### Step N:` steps. Step numbers are global (not per-phase).
79	    - The flat `## Step N:` format (without phases) also works for backwards compatibility.
80	    - Key invariants: one H1 title, one `## Overview`, numbered step sections (`### Step N:` or `## Step N:`), and at least one ordering section.
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 794,
  "limit": 100
}
```

> TOOL

tool_result Read
```
794	def handle_plan(root: Path, args: argparse.Namespace) -> StepResponse:
795	    with load_plan_locked(root, args.plan, step="plan") as (plan_dir, state):
796	        require_state(state, "plan", {STATE_INITIALIZED, STATE_PREPPED, STATE_PLANNED})
797	        rerun = state["current_state"] == STATE_PLANNED
798	        version = state["iteration"] if rerun else state["iteration"] + 1
799	        worker, agent, mode, refreshed = _run_worker("plan", state, plan_dir, args, root=root, iteration=version)
800	        payload = worker.payload
801	        plan_filename, meta_filename, meta = _write_plan_version(
802	            plan_dir=plan_dir,
803	            state=state,
804	            step="plan",
805	            version=version,
806	            worker=worker,
807	            plan_text=payload["plan"].rstrip() + "\n",
808	            meta_fields={
809	                "questions": payload["questions"],
810	                "success_criteria": payload["success_criteria"],
811	                "assumptions": payload["assumptions"],
812	            },
813	        )
814	        state["iteration"], state["current_state"] = version, STATE_PLANNED
815	        state["meta"].pop("user_approved_gate", None)
816	        state["last_gate"] = {}
817	        state["plan_versions"].append({
818	            "version": version, "file": plan_filename,
819	            "hash": meta["hash"], "timestamp": meta["timestamp"],
820	        })
821	        verb = "Refined" if rerun else "Generated"
822	        return _finish_step(
823	            plan_dir, state, args,
824	            step="plan",
825	            worker=worker, agent=agent, mode=mode, refreshed=refreshed,
826	            summary=f"{verb} plan v{version} with {len(payload['questions'])} questions and {len(payload['success_criteria'])} success criteria.",
827	            artifacts=[plan_filename, meta_filename],
828	            output_file=plan_filename,
829	            artifact_hash=meta["hash"],
830	            response_fields={
831	                "iteration": version,
832	                "questions": payload["questions"],
833	                "assumptions": payload["assumptions"],
834	                "success_criteria": payload["success_criteria"],
835	            },
836	        )
837	
838	
839	
840	def handle_prep(root: Path, args: argparse.Namespace) -> StepResponse:
841	    with load_plan_locked(root, args.plan, step="prep") as (plan_dir, state):
842	        require_state(state, "prep", {STATE_INITIALIZED})
843	        worker, agent, mode, refreshed = _run_worker("prep", state, plan_dir, args, root=root)
844	        prep_filename = "prep.json"
845	        artifact_hash = _write_json_artifact(plan_dir, prep_filename, worker.payload)
846	        code_refs = len(worker.payload.get("relevant_code", []))
847	        test_refs = len(worker.payload.get("test_expectations", []))
848	        state["current_state"] = STATE_PREPPED
849	        return _finish_step(
850	            plan_dir, state, args,
851	            step="prep",
852	            worker=worker, agent=agent, mode=mode, refreshed=refreshed,
853	            summary=f"Prep complete: captured {code_refs} relevant code reference(s) and {test_refs} test expectation(s).",
854	            artifacts=[prep_filename],
855	            output_file=prep_filename,
856	            artifact_hash=artifact_hash,
857	            response_fields={"iteration": state["iteration"]},
858	        )
859	
860	
861	def handle_critique(root: Path, args: argparse.Namespace) -> StepResponse:
862	    with load_plan_locked(root, args.plan, step="critique") as (plan_dir, state):
863	        require_state(state, "critique", {STATE_PLANNED})
864	        iteration = state["iteration"]
865	        robustness = configured_robustness(state)
866	        state["last_gate"] = {}
867	        critique_filename = f"critique_v{iteration}.json"
868	        if robustness == "tiny":
869	            stub_critique = {
870	                "checks": [],
871	                "flags": [],
872	                "verified_flag_ids": [],
873	                "disputed_flag_ids": [],
874	            }
875	            validate_payload("critique", stub_critique)
876	            atomic_write_json(plan_dir / critique_filename, stub_critique)
877	            save_flag_registry(plan_dir, {"flags": []})
878	            minimal_gate: dict[str, Any] = {
879	                "recommendation": "ITERATE",
880	                "rationale": "Tiny robustness: critique stubbed; advancing directly to gated.",
881	                "signals_assessment": "",
882	                "warnings": [],
883	                "settled_decisions": [],
884	            }
885	            atomic_write_json(plan_dir / "gate.json", minimal_gate)
886	            state["last_gate"] = {"recommendation": "ITERATE"}
887	            state["current_state"] = STATE_GATED
888	            stub_worker = WorkerResult(
889	                payload=stub_critique,
890	                raw_output="",
891	                duration_ms=0,
892	                cost_usd=0.0,
893	                session_id=None,
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 861,
  "limit": 140
}
```

> TOOL

tool_result Read
```
861	def handle_critique(root: Path, args: argparse.Namespace) -> StepResponse:
862	    with load_plan_locked(root, args.plan, step="critique") as (plan_dir, state):
863	        require_state(state, "critique", {STATE_PLANNED})
864	        iteration = state["iteration"]
865	        robustness = configured_robustness(state)
866	        state["last_gate"] = {}
867	        critique_filename = f"critique_v{iteration}.json"
868	        if robustness == "tiny":
869	            stub_critique = {
870	                "checks": [],
871	                "flags": [],
872	                "verified_flag_ids": [],
873	                "disputed_flag_ids": [],
874	            }
875	            validate_payload("critique", stub_critique)
876	            atomic_write_json(plan_dir / critique_filename, stub_critique)
877	            save_flag_registry(plan_dir, {"flags": []})
878	            minimal_gate: dict[str, Any] = {
879	                "recommendation": "ITERATE",
880	                "rationale": "Tiny robustness: critique stubbed; advancing directly to gated.",
881	                "signals_assessment": "",
882	                "warnings": [],
883	                "settled_decisions": [],
884	            }
885	            atomic_write_json(plan_dir / "gate.json", minimal_gate)
886	            state["last_gate"] = {"recommendation": "ITERATE"}
887	            state["current_state"] = STATE_GATED
888	            stub_worker = WorkerResult(
889	                payload=stub_critique,
890	                raw_output="",
891	                duration_ms=0,
892	                cost_usd=0.0,
893	                session_id=None,
894	                prompt_tokens=0,
895	                completion_tokens=0,
896	                total_tokens=0,
897	            )
898	            agent, _mode, _refreshed, _model = resolve_agent_mode("critique", args)
899	            return _finish_step(
900	                plan_dir, state, args,
901	                step="critique",
902	                worker=stub_worker,
903	                agent=agent,
904	                mode="stub",
905	                refreshed=False,
906	                summary="Tiny robustness: critique stubbed; advancing directly to gated.",
907	                artifacts=[critique_filename, "faults.json", "gate.json"],
908	                output_file=critique_filename,
909	                artifact_hash=sha256_file(plan_dir / critique_filename),
910	                response_fields={
911	                    "iteration": iteration,
912	                    "checks": [],
913	                    "verified_flags": [],
914	                    "open_flags": [],
915	                    "scope_creep_flags": [],
916	                },
917	                history_fields={"flags_count": 0},
918	            )
919	        active_checks = checks_for_robustness(robustness)
920	        expected_ids = [check["id"] for check in active_checks]
921	        agent_type, mode, refreshed, model = resolve_agent_mode("critique", args)
922	        if len(active_checks) > 1 and agent_type == "hermes":
923	            try:
924	                worker = run_parallel_critique(state, plan_dir, root=root, model=model, checks=active_checks)
925	                agent, mode, refreshed = "hermes", "persistent", True
926	            except Exception as exc:
927	                print(f"[parallel-critique] Failed, falling back to sequential: {exc}", file=sys.stderr)
928	                worker, agent, mode, refreshed = _run_worker(
929	                    "critique",
930	                    state,
931	                    plan_dir,
932	                    args,
933	                    root=root,
934	                    resolved=(agent_type, mode, refreshed, model),
935	                )
936	        else:
937	            worker, agent, mode, refreshed = _run_worker(
938	                "critique",
939	                state,
940	                plan_dir,
941	                args,
942	                root=root,
943	                resolved=(agent_type, mode, refreshed, model),
944	            )
945	        invalid_checks = validate_critique_checks(worker.payload, expected_ids=expected_ids)
946	        if invalid_checks:
947	            _raise_step_validation_error(plan_dir=plan_dir, state=state, step="critique", iteration=iteration, worker=worker, code="invalid_critique", message="Critique output failed check validation: " + ", ".join(invalid_checks))
948	        atomic_write_json(plan_dir / critique_filename, worker.payload)
949	        registry = update_flags_after_critique(plan_dir, worker.payload, iteration=iteration)
950	        significant = len([flag for flag in registry["flags"] if flag.get("severity") == "significant" and flag["status"] in FLAG_BLOCKING_STATUSES])
951	        _append_to_meta(state, "significant_counts", significant)
952	        recurring = compute_recurring_critiques(plan_dir, iteration)
953	        _append_to_meta(state, "recurring_critiques", recurring)
954	        state["current_state"] = STATE_CRITIQUED
955	        skip_gate = not workflow_includes_step(robustness, "gate")
956	        if skip_gate:
957	            minimal_gate: dict[str, Any] = {
958	                "recommendation": "ITERATE",
959	                "rationale": "Light robustness: single revision pass to incorporate critique feedback.",
960	                "signals_assessment": "",
961	                "warnings": [],
962	                "settled_decisions": [],
963	            }
964	            atomic_write_json(plan_dir / "gate.json", minimal_gate)
965	            state["last_gate"] = {"recommendation": "ITERATE"}
966	        scope_flags_list = scope_creep_flags(registry, statuses=FLAG_BLOCKING_STATUSES)
967	        open_flags_detail = [
968	            {"id": flag["id"], "concern": flag["concern"], "category": flag["category"], "severity": flag.get("severity", "unknown")}
969	            for flag in registry["flags"]
970	            if flag["status"] == "open"
971	        ]
972	        response_fields: dict[str, Any] = {
973	            "iteration": iteration,
974	            "checks": worker.payload.get("checks", []),
975	            "verified_flags": worker.payload.get("verified_flag_ids", []),
976	            "open_flags": open_flags_detail,
977	            "scope_creep_flags": [flag["id"] for flag in scope_flags_list],
978	        }
979	        if scope_flags_list:
980	            response_fields["warnings"] = ["Scope creep detected in the plan. Surface this drift to the user while continuing the loop."]
981	        return _finish_step(
982	            plan_dir, state, args,
983	            step="critique",
984	            worker=worker, agent=agent, mode=mode, refreshed=refreshed,
985	            summary=f"Recorded {len(worker.payload.get('flags', []))} critique flags.",
986	            artifacts=[critique_filename, "faults.json"],
987	            output_file=critique_filename,
988	            artifact_hash=sha256_file(plan_dir / critique_filename),
989	            response_fields=response_fields,
990	            history_fields={"flags_count": len(worker.payload.get("flags", []))},
991	        )
992	
993	
994	def handle_revise(root: Path, args: argparse.Namespace) -> StepResponse:
995	    with load_plan_locked(root, args.plan, step="revise") as (plan_dir, state):
996	        require_state(state, "revise", {STATE_CRITIQUED})
997	        has_gate, revise_transition = _resolve_revise_transition(state)
998	        previous_plan = latest_plan_path(plan_dir, state).read_text(encoding="utf-8")
999	        worker, agent, mode, refreshed = _run_worker("revise", state, plan_dir, args, root=root, iteration=state["iteration"] + 1)
1000	        payload = worker.payload
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 1337,
  "limit": 120
}
```

> TOOL

tool_result Read
```
1337	def handle_execute(root: Path, args: argparse.Namespace) -> StepResponse:
1338	    with load_plan_locked(root, args.plan, step="execute") as (plan_dir, state):
1339	        require_state(state, "execute", {STATE_FINALIZED})
1340	        if not args.confirm_destructive:
1341	            raise CliError("missing_confirmation", "Execute requires --confirm-destructive")
1342	        auto_approve = bool(state["config"].get("auto_approve", False))
1343	        if getattr(args, "user_approved", False):
1344	            state["meta"]["user_approved_gate"] = True
1345	            save_state(plan_dir, state)
1346	        if not auto_approve and not state["meta"].get("user_approved_gate", False):
1347	            raise CliError(
1348	                "missing_approval",
1349	                "Execute requires explicit user approval (--user-approved) when auto-approve is not set. The orchestrator must confirm with the user at the gate checkpoint before proceeding.",
1350	            )
1351	        agent, mode, refreshed, model = worker_module.resolve_agent_mode("execute", args)
1352	        # Force fresh session after review kickback to avoid prior-context bias
1353	        if not refreshed and _is_rework_reexecution(state):
1354	            refreshed = True
1355	        run_id = set_active_step(state, step="execute", agent=agent, mode=mode, model=model)
1356	        _emit_phase_notice("execute")
1357	        save_state(plan_dir, state)
1358	        try:
1359	            if getattr(args, "batch", None) is not None:
1360	                response = dispatch_execute_one_batch(
1361	                    root=root,
1362	                    plan_dir=plan_dir,
1363	                    state=state,
1364	                    args=args,
1365	                    batch_number=args.batch,
1366	                    auto_approve=auto_approve,
1367	                    agent=agent,
1368	                    mode=mode,
1369	                    refreshed=refreshed,
1370	                    model=model,
1371	                )
1372	            else:
1373	                response = dispatch_execute_auto_loop(
1374	                    root=root,
1375	                    plan_dir=plan_dir,
1376	                    state=state,
1377	                    args=args,
1378	                    auto_approve=auto_approve,
1379	                    agent=agent,
1380	                    mode=mode,
1381	                    refreshed=refreshed,
1382	                    model=model,
1383	                )
1384	        except CliError:
1385	            clear_active_step(state, run_id=run_id)
1386	            save_state(plan_dir, state)
1387	            raise
1388	        clear_active_step(state, run_id=run_id)
1389	        robustness = configured_robustness(state)
1390	        if not workflow_includes_step(robustness, "review") and response.get("state") == STATE_EXECUTED:
1391	            # Preserve the data-parity invariant even when review is skipped by robustness.
1392	            stub_review = {
1393	                "review_verdict": "approved",
1394	                "checks": [],
1395	                "pre_check_flags": [],
1396	                "verified_flag_ids": [],
1397	                "disputed_flag_ids": [],
1398	                "criteria": [],
1399	                "issues": [],
1400	                "rework_items": [],
1401	                "summary": f"{robustness.title()} robustness: review skipped; stub written for artifact parity.",
1402	                "task_verdicts": [],
1403	                "sense_check_verdicts": [],
1404	            }
1405	            validate_payload("review", stub_review)
1406	            atomic_write_json(plan_dir / "review.json", stub_review)
1407	            artifacts = response.get("artifacts")
1408	            if isinstance(artifacts, list) and "review.json" not in artifacts:
1409	                artifacts.append("review.json")
1410	            state["current_state"] = STATE_DONE
1411	            save_state(plan_dir, state)
1412	            response["state"] = STATE_DONE
1413	            response["next_step"] = None
1414	            response.pop("next_step_runtime", None)
1415	        else:
1416	            save_state(plan_dir, state)
1417	        attach_agent_fallback(response, args)
1418	        return response
1419	
1420	
1421	def _merge_review_verdicts(
1422	    worker_payload: dict[str, Any],
1423	    finalize_data: dict[str, Any],
1424	    issues: list[str],
1425	) -> tuple[int, int, int, int, list[str]]:
1426	    """Merge task verdicts and sense check verdicts into finalize_data.
1427	
1428	    Returns (verdict_count, total_tasks, check_count, total_checks, missing_evidence).
1429	    """
1430	    tasks_by_id = {task["id"]: task for task in finalize_data.get("tasks", [])}
1431	    verdict_count, total_tasks = _validate_and_merge_batch(
1432	        worker_payload.get("task_verdicts"),
1433	        required_fields=("task_id", "reviewer_verdict", "evidence_files"),
1434	        targets_by_id=tasks_by_id,
1435	        id_field="task_id",
1436	        merge_fields=("reviewer_verdict", "evidence_files"),
1437	        issues=issues,
1438	        validation_label="task_verdicts",
1439	        merge_label="task_verdict",
1440	        incomplete_message=lambda merged, total: f"Incomplete review: {merged}/{total} tasks received a reviewer verdict.",
1441	        nonempty_fields={"reviewer_verdict"},
1442	        array_fields=("evidence_files",),
1443	    )
1444	    sense_checks_by_id = {sc["id"]: sc for sc in finalize_data.get("sense_checks", [])}
1445	    check_count, total_checks = _validate_and_merge_batch(
1446	        worker_payload.get("sense_check_verdicts"),
1447	        required_fields=("sense_check_id", "verdict"),
1448	        targets_by_id=sense_checks_by_id,
1449	        id_field="sense_check_id",
1450	        merge_fields=("verdict",),
1451	        issues=issues,
1452	        validation_label="sense_check_verdicts",
1453	        merge_label="sense_check_verdict",
1454	        incomplete_message=lambda merged, total: f"Incomplete review: {merged}/{total} sense checks received a verdict.",
1455	        nonempty_fields={"verdict"},
1456	    )
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 1576,
  "limit": 120
}
```

> TOOL

tool_result Read
```
1576	def handle_review(root: Path, args: argparse.Namespace) -> StepResponse:
1577	    with load_plan_locked(root, args.plan, step="review") as (plan_dir, state):
1578	        require_state(state, "review", {STATE_EXECUTED})
1579	        robustness = configured_robustness(state)
1580	        pre_check_flags: list[dict[str, Any]] = []
1581	        if robustness in {"standard", "robust", "superrobust"}:
1582	            pre_check_flags = run_pre_checks(plan_dir, state, Path(state["config"]["project_dir"]))
1583	        if robustness in {"standard", "light", "robust"}:
1584	            resolved = None
1585	            prompt_override = None
1586	            prompt_kwargs = None
1587	            if robustness in {"standard", "robust"}:
1588	                resolved = resolve_agent_mode("review", args)
1589	                if _supports_prompt_kwargs(worker_module.run_step_with_worker):
1590	                    prompt_kwargs = {"pre_check_flags": pre_check_flags}
1591	                else:
1592	                    prompt_override = _build_review_prompt_override(
1593	                        resolved[0],
1594	                        state,
1595	                        plan_dir,
1596	                        root=root,
1597	                        pre_check_flags=pre_check_flags,
1598	                    )
1599	            worker, agent, mode, refreshed = _run_worker(
1600	                "review",
1601	                state,
1602	                plan_dir,
1603	                args,
1604	                root=root,
1605	                resolved=resolved,
1606	                prompt_override=prompt_override,
1607	                prompt_kwargs=prompt_kwargs,
1608	            )
1609	            if robustness in {"standard", "robust"}:
1610	                worker.payload["pre_check_flags"] = pre_check_flags
1611	                update_flags_after_review(plan_dir, worker.payload, iteration=state["iteration"])
1612	            atomic_write_json(plan_dir / "review.json", worker.payload)
1613	        else:
1614	            agent_type, mode, refreshed, model = resolve_agent_mode("review", args)
1615	            if agent_type != "hermes" or os.getenv(MOCK_ENV_VAR) == "1":
1616	                worker, agent, mode, refreshed = _run_worker(
1617	                    "review",
1618	                    state,
1619	                    plan_dir,
1620	                    args,
1621	                    root=root,
1622	                    resolved=(agent_type, mode, refreshed, model),
1623	                )
1624	                atomic_write_json(plan_dir / "review.json", worker.payload)
1625	                issues = list(worker.payload.get("issues", []))
1626	                finalize_data = read_json(plan_dir / "finalize.json")
1627	
1628	                review_verdict = worker.payload.get("review_verdict")
1629	                if review_verdict not in {"approved", "needs_rework"}:
1630	                    issues.append("Invalid review_verdict; expected 'approved' or 'needs_rework'.")
1631	                    review_verdict = "needs_rework"
1632	
1633	                verdict_count, total_tasks, check_count, total_checks, missing_evidence = _merge_review_verdicts(
1634	                    worker.payload, finalize_data, issues,
1635	                )
1636	                atomic_write_json(plan_dir / "finalize.json", finalize_data)
1637	                atomic_write_text(plan_dir / "final.md", render_final_md(finalize_data, phase="review"))
1638	                finalize_hash = sha256_file(plan_dir / "finalize.json")
1639	
1640	                result, next_state, next_step = _resolve_review_outcome(
1641	                    review_verdict, verdict_count, total_tasks,
1642	                    check_count, total_checks, missing_evidence,
1643	                    robustness,
1644	                    state, issues,
1645	                )
1646	                state["current_state"] = next_state
1647	
1648	                clear_active_step(state)
1649	                apply_session_update(state, "review", agent, worker.session_id, mode=mode, refreshed=refreshed)
1650	                append_history(
1651	                    state,
1652	                    make_history_entry(
1653	                        "review",
1654	                        duration_ms=worker.duration_ms, cost_usd=worker.cost_usd,
1655	                        result=result,
1656	                        worker=worker, agent=agent, mode=mode,
1657	                        output_file="review.json",
1658	                        prompt_tokens=worker.prompt_tokens,
1659	                        completion_tokens=worker.completion_tokens,
1660	                        total_tokens=worker.total_tokens,
1661	                        artifact_hash=sha256_file(plan_dir / "review.json"),
1662	                        finalize_hash=finalize_hash,
1663	                    ),
1664	                )
1665	                save_state(plan_dir, state)
1666	
1667	                passed = sum(1 for c in worker.payload.get("criteria", []) if c.get("pass") in (True, "pass"))
1668	                total = len(worker.payload.get("criteria", []))
1669	                if result == "blocked":
1670	                    summary = _build_review_blocked_message(
1671	                        verdict_count=verdict_count, total_tasks=total_tasks,
1672	                        check_count=check_count, total_checks=total_checks,
1673	                        missing_reviewer_evidence=missing_evidence,
1674	                    )
1675	                elif result == "needs_rework":
1676	                    summary = "Review requested another execute pass. Re-run execute using the review findings as context."
1677	                else:
1678	                    summary = f"Review complete: {passed}/{total} success criteria passed."
1679	
1680	                response: StepResponse = {
1681	                    "success": result == "success",
1682	                    "step": "review",
1683	                    "summary": summary,
1684	                    "artifacts": ["review.json", "finalize.json", "final.md"],
1685	                    "monitor_hint": build_monitor_hint(plan_dir),
1686	                    "next_step": next_step,
1687	                    "state": next_state,
1688	                    "issues": issues,
1689	                    "rework_items": list(worker.payload.get("rework_items", [])),
1690	                }
1691	                _attach_next_step_runtime(response)
1692	                attach_agent_fallback(response, args)
1693	                return response
1694	
1695	            run_id = None
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/workers.py",
  "offset": 230,
  "limit": 150
}
```

> TOOL

tool_result Read
```
230	    Happens when: container was restarted between phases and codex's session
231	    store (usually ``$HOME/.codex/sessions``) was wiped, but megaplan's plan
232	    state still has the session id and tries to ``codex exec resume <id>``.
233	
234	    Match is case-insensitive on known substrings so minor wording changes
235	    upstream don't break recovery. Fall back to failing loudly if Codex
236	    introduces a new error string — false positives here would mask real
237	    session crashes.
238	    """
239	    if not raw:
240	        return False
241	    lowered = raw.lower()
242	    return any(pat in lowered for pat in _ROLLOUT_MISSING_PATTERNS)
243	
244	
245	def _trusted_container() -> bool:
246	    """Return True when MEGAPLAN_TRUSTED_CONTAINER is set to a truthy value.
247	
248	    In a locked-down container (Docker/Railway/Kubernetes without
249	    user-namespace capabilities), bubblewrap's default sandbox fails with
250	    ``bwrap: Creating new namespace failed: Permission denied`` because
251	    ``kernel.unprivileged_userns_clone`` is not settable by an unprivileged
252	    user. Per the official guidance at
253	    https://docs.docker.com/ai/sandboxes/agents/codex/ the operator is
254	    expected to rely on container-level isolation and bypass the Codex
255	    sandbox entirely. Setting ``MEGAPLAN_TRUSTED_CONTAINER=1`` on the
256	    worker environment activates that path.
257	    """
258	    return os.environ.get("MEGAPLAN_TRUSTED_CONTAINER", "").strip().lower() in {
259	        "1",
260	        "true",
261	        "yes",
262	        "on",
263	    }
264	
265	
266	def _codex_child_env() -> dict[str, str]:
267	    env = os.environ.copy()
268	    # Nested Codex workers should not inherit the parent Codex session state.
269	    # Those variables can cause the child to attach to the outer thread/CI
270	    # context instead of behaving like an isolated worker invocation.
271	    env.pop("CODEX_THREAD_ID", None)
272	    env.pop("CODEX_CI", None)
273	    return env
274	
275	
276	def _merge_partial_output(raw_output: str, output_path: Path) -> str:
277	    merged = raw_output or ""
278	    try:
279	        partial = output_path.read_text(encoding="utf-8").strip()
280	    except (FileNotFoundError, OSError, UnicodeDecodeError):
281	        partial = ""
282	    if partial and partial not in merged:
283	        if merged and not merged.endswith("\n"):
284	            merged += "\n"
285	        merged += "[partial_output_file]\n" + partial
286	    return merged
287	
288	
289	def extract_session_id(raw: str) -> str | None:
290	    # Try structured JSONL first (codex --json emits {"type":"thread.started","thread_id":"..."})
291	    for line in raw.splitlines():
292	        line = line.strip()
293	        if not line:
294	            continue
295	        try:
296	            obj = json.loads(line)
297	            if isinstance(obj, dict) and obj.get("thread_id"):
298	                return str(obj["thread_id"])
299	        except (json.JSONDecodeError, ValueError):
300	            continue
301	    # Fallback: unstructured text pattern
302	    match = re.search(r"\bsession[_ ]id[: ]+([0-9a-fA-F-]{8,})", raw)
303	    return match.group(1) if match else None
304	
305	
306	def parse_claude_envelope(raw: str) -> tuple[dict[str, Any], dict[str, Any]]:
307	    try:
308	        envelope = json.loads(raw)
309	    except json.JSONDecodeError as exc:
310	        raise CliError("parse_error", f"Claude output was not valid JSON: {exc}", extra={"raw_output": raw}) from exc
311	    if isinstance(envelope, dict) and envelope.get("is_error"):
312	        message = envelope.get("result") or envelope.get("message") or "Claude returned an error"
313	        lower = str(message).lower()
314	        error_code = "worker_error"
315	        if any(pattern in lower for pattern in ("not logged in", "/login", "unauthorized", "authentication")):
316	            error_code = "auth_error"
317	        raise CliError(error_code, f"Claude step failed: {message}", extra={"raw_output": raw})
318	    # When using --json-schema, structured output lives in "structured_output"
319	    # rather than "result" (which may be empty).
320	    payload: Any = envelope
321	    if isinstance(envelope, dict):
322	        if "structured_output" in envelope and isinstance(envelope["structured_output"], dict):
323	            payload = envelope["structured_output"]
324	        elif "result" in envelope:
325	            payload = envelope["result"]
326	    if isinstance(payload, str):
327	        if not payload.strip():
328	            raise CliError("parse_error", "Claude returned empty result (check structured_output field)", extra={"raw_output": raw})
329	        try:
330	            payload = json.loads(payload)
331	        except json.JSONDecodeError as exc:
332	            raise CliError("parse_error", f"Claude result payload was not valid JSON: {exc}", extra={"raw_output": raw}) from exc
333	    if not isinstance(payload, dict):
334	        raise CliError("parse_error", "Claude result payload was not an object", extra={"raw_output": raw})
335	    return envelope, payload
336	
337	
338	def _extract_json_candidates_from_raw(raw: str) -> list[dict[str, Any]]:
339	    """Extract plausible JSON payload objects from raw agent output."""
340	
341	    def _iter_nested_json_dicts(value: Any) -> list[dict[str, Any]]:
342	        candidates: list[dict[str, Any]] = []
343	        if isinstance(value, dict):
344	            candidates.append(value)
345	            prioritized_keys = (
346	                "structured_output",
347	                "result",
348	                "payload",
349	                "text",
350	                "message",
351	            )
352	            for key in prioritized_keys:
353	                if key not in value:
354	                    continue
355	                nested = value.get(key)
356	                candidates.extend(_iter_nested_json_dicts(nested))
357	            for nested in value.values():
358	                candidates.extend(_iter_nested_json_dicts(nested))
359	            return candidates
360	        if isinstance(value, list):
361	            for item in value:
362	                candidates.extend(_iter_nested_json_dicts(item))
363	            return candidates
364	        if isinstance(value, str):
365	            text = value.strip()
366	            if text.startswith("{") or text.startswith("["):
367	                try:
368	                    parsed = json.loads(text)
369	                except json.JSONDecodeError:
370	                    return []
371	                return _iter_nested_json_dicts(parsed)
372	        return []
373	
374	    candidates: list[dict[str, Any]] = []
375	
376	    # Strategy 1: look for ```json ... ``` fenced blocks
377	    fenced = re.findall(r"```json\s*\n(.*?)```", raw, re.DOTALL)
378	    for block in fenced:
379	        try:
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/loop/engine.py",
  "offset": 1,
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	"""Core MegaLoop engine."""
2	from __future__ import annotations
3	
4	import argparse
5	import re
6	import shutil
7	import subprocess
8	import threading
9	import time
10	from collections import deque
11	from pathlib import Path
12	from typing import Any, Callable
13	
14	from megaplan._core import (
15	    atomic_write_json,
16	    atomic_write_text,
17	    current_iteration_artifact,
18	    current_iteration_raw_artifact,
19	    ensure_runtime_layout,
20	    now_utc,
21	    read_json,
22	)
23	from megaplan.loop.git import git_commit, git_revert, parse_metric
24	from megaplan.loop.prompts import build_loop_prompt
25	from megaplan.loop.types import IterationResult, LoopSpec, LoopState, Observation
26	from megaplan.workers import WorkerResult, resolve_agent_mode, run_step_with_worker, update_session_state
27	_DEFAULT_ALLOWED_CHANGES = ["."]
28	_COMMAND_OUTPUT_LIMIT = 12000
29	_DEFAULT_TIME_BUDGET_SECONDS = 300
30	_MONITORED_OUTPUT_BUFFER_LIMIT = 200_000
31	def _loop_dir(project_dir: str | Path, name: str) -> Path:
32	    return Path(project_dir) / ".megaplan" / "loops" / name
33	def _state_path(project_dir: str | Path, name: str) -> Path:
34	    return _loop_dir(project_dir, name) / "state.json"
35	def _normalized_args(args: argparse.Namespace | None) -> argparse.Namespace:
36	    values = vars(args).copy() if args is not None else {}
37	    normalized = argparse.Namespace(**values)
38	    defaults = {
39	        "agent": None,
40	        "phase_model": [],
41	        "hermes": None,
42	        "ephemeral": False,
43	        "fresh": False,
44	        "persist": False,
45	        "confirm_self_review": False,
46	        "iterations": None,
47	        "time_budget": None,
48	        "time_budget_seconds": None,
49	    }
50	    for key, value in defaults.items():
51	        if not hasattr(normalized, key):
52	            setattr(normalized, key, value)
53	    return normalized
54	def _string_list(value: Any, *, default: list[str] | None = None) -> list[str]:
55	    if value is None:
56	        return list(default or [])
57	    if isinstance(value, str):
58	        return [item.strip() for item in value.split(",") if item.strip()]
59	    if isinstance(value, (list, tuple)):
60	        return [str(item).strip() for item in value if str(item).strip()]
61	    return list(default or [])
62	def _merge_value(existing: Any, update: Any) -> Any:
63	    if isinstance(existing, list) and isinstance(update, list):
64	        merged: list[Any] = []
65	        for item in [*existing, *update]:
66	            if item not in merged:
67	                merged.append(item)
68	        return merged
69	    return update
70	def _merge_spec(spec: LoopSpec, updates: dict[str, Any]) -> LoopSpec:
71	    merged: LoopSpec = dict(spec)
72	    for key, value in updates.items():
73	        if value in (None, "", []):
74	            continue
75	        merged[key] = _merge_value(merged.get(key), value)
76	    return merged
77	def _time_budget_seconds(state: LoopState, args: argparse.Namespace | None) -> int:
78	    normalized = _normalized_args(args)
79	    budget = (
80	        getattr(normalized, "time_budget_seconds", None)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/auto.py",
  "offset": 1,
  "limit": 80
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
27	from megaplan.types import TERMINAL_STATES
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
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/loop/types.py"
}
```

> TOOL

tool_result Read
```
1	"""Types for the MegaLoop iterative agent workflow."""
2	
3	from __future__ import annotations
4	
5	from typing import NotRequired, TypedDict
6	
7	from megaplan.types import PlanConfig, SessionInfo
8	
9	
10	class Observation(TypedDict):
11	    elapsed_seconds: int
12	    tail_output: str
13	    metric: float | None
14	    action: str
15	
16	
17	class IterationResult(TypedDict, total=False):
18	    iteration: int
19	    phase: str
20	    outcome: str
21	    diagnosis: str
22	    fix_description: str
23	    files_to_change: list[str]
24	    confidence: str
25	    should_pause: bool
26	    returncode: int
27	    command_output: str
28	    metric: float
29	    commit_sha: str
30	    reverted: bool
31	    reasoning: str
32	    observations: list[Observation]
33	
34	
35	class LoopSpec(TypedDict, total=False):
36	    goal: str
37	    command: str
38	    success_criteria: list[str]
39	    allowed_changes: list[str]
40	    optimization_strategy: str
41	    bug_finding_approach: str
42	    philosophy: str
43	    metric_pattern: str
44	    known_issues: list[str]
45	    tried_and_failed: list[str]
46	    best_result_summary: str
47	    current_best: IterationResult
48	    observe_interval: int
49	    observe_break_patterns: list[str]
50	    observe_metric_stall: int
51	
52	
53	class LoopState(TypedDict):
54	    name: str
55	    spec: LoopSpec
56	    phase: str
57	    status: str
58	    iteration: int
59	    config: PlanConfig
60	    sessions: dict[str, SessionInfo]
61	    created_at: NotRequired[str]
62	    updated_at: NotRequired[str]
63	    max_iterations: NotRequired[int]
64	    results: NotRequired[list[IterationResult]]
65	    current_best: NotRequired[IterationResult]
66	    pause_requested: NotRequired[bool]
67	    pause_reason: NotRequired[str]
68
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/cli.py",
  "offset": 100,
  "limit": 200
}
```

> TOOL

tool_result Read
```
100	    if isinstance(plan_name, str) and plan_name:
101	        monitor_hint = build_monitor_hint(plan_dir or Path(plan_name))
102	        payload["monitor_hint"] = monitor_hint
103	        if details is not None:
104	            details["monitor_hint"] = monitor_hint
105	    raw_active_step = (details or {}).get("active_step")
106	    if isinstance(raw_active_step, dict):
107	        active_step = (
108	            _build_active_step(raw_active_step, plan_dir=plan_dir)
109	            if plan_dir is not None
110	            else dict(raw_active_step)
111	        )
112	        payload["active_step"] = active_step
113	        if details is not None:
114	            details["active_step"] = active_step
115	
116	
117	def error_response(error: CliError, *, root: Path | None = None) -> int:
118	    payload: StepResponse = {
119	        "success": False,
120	        "error": error.code,
121	        "message": error.message,
122	    }
123	    if error.valid_next:
124	        payload["valid_next"] = error.valid_next
125	    if error.extra:
126	        payload["details"] = dict(error.extra)
127	    if error.code == "plan_locked":
128	        _augment_plan_locked_error(payload, error, root=root)
129	    return render_response(payload, exit_code=error.exit_code)
130	
131	
132	def _parse_utc_timestamp(timestamp: str | None) -> datetime | None:
133	    if not isinstance(timestamp, str) or not timestamp:
134	        return None
135	    try:
136	        return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
137	    except ValueError:
138	        return None
139	
140	
141	def _build_progress_payload(plan_dir: Path, state: dict[str, Any]) -> dict[str, Any]:
142	    finalize_path = plan_dir / "finalize.json"
143	    if not finalize_path.exists():
144	        return {
145	            "summary": "No finalize.json yet — plan has not been finalized.",
146	            "tasks_total": 0,
147	            "tasks_done": 0,
148	            "tasks_skipped": 0,
149	            "tasks_pending": 0,
150	            "batches_total": 0,
151	            "batches_completed": 0,
152	            "tasks": [],
153	        }
154	    finalize_data = read_json(finalize_path)
155	    global_batches = compute_global_batches(finalize_data)
156	    tasks = finalize_data.get("tasks", [])
157	    task_id_to_batch: dict[str, int] = {}
158	    for batch_idx, batch_ids in enumerate(global_batches, start=1):
159	        for task_id in batch_ids:
160	            task_id_to_batch[task_id] = batch_idx
161	    tasks_done = sum(1 for t in tasks if t.get("status") == "done")
162	    tasks_skipped = sum(1 for t in tasks if t.get("status") == "skipped")
163	    tasks_pending = sum(1 for t in tasks if t.get("status") == "pending")
164	    tasks_total = len(tasks)
165	    completed_ids = {
166	        t["id"] for t in tasks if t.get("status") in {"done", "skipped"} and isinstance(t.get("id"), str)
167	    }
168	    batches_completed = sum(
169	        1
170	        for batch_ids in global_batches
171	        if all(tid in completed_ids for tid in batch_ids)
172	    )
173	    task_status_list = [
174	        {
175	            "id": t.get("id", ""),
176	            "status": t.get("status", "pending"),
177	            "batch": task_id_to_batch.get(t.get("id", ""), 0),
178	        }
179	        for t in tasks
180	    ]
181	    return {
182	        "summary": (
183	            f"Execution progress: {tasks_done + tasks_skipped}/{tasks_total} tasks tracked, "
184	            f"{batches_completed}/{len(global_batches)} batches completed. "
185	            "Progress reflects the last finalize.json write (between-batch granularity)."
186	        ),
187	        "tasks_total": tasks_total,
188	        "tasks_done": tasks_done,
189	        "tasks_skipped": tasks_skipped,
190	        "tasks_pending": tasks_pending,
191	        "batches_total": len(global_batches),
192	        "batches_completed": batches_completed,
193	        "tasks": task_status_list,
194	    }
195	
196	
197	def _build_last_step(state: dict[str, Any]) -> dict[str, Any] | None:
198	    history = state.get("history", [])
199	    if not isinstance(history, list) or not history:
200	        return None
201	    last = history[-1]
202	    if not isinstance(last, dict):
203	        return None
204	    return {
205	        "step": last.get("step"),
206	        "result": last.get("result"),
207	        "timestamp": last.get("timestamp"),
208	        "agent": last.get("agent"),
209	        "output_file": last.get("output_file"),
210	    }
211	
212	
213	def _build_active_step(active_step: Any, *, plan_dir: Path) -> dict[str, Any] | None:
214	    if not isinstance(active_step, dict):
215	        return None
216	    details = dict(active_step)
217	    step = details.get("step")
218	    if not isinstance(step, str) or not step:
219	        return details
220	    configured_timeout_seconds = int(get_effective("execution", "worker_timeout_seconds"))
221	    lock_held = plan_lock_is_held(plan_dir)
222	    started_at = _parse_utc_timestamp(details.get("started_at"))
223	    if started_at is not None:
224	        age_seconds = max(0, int((datetime.now(timezone.utc) - started_at).total_seconds()))
225	        details.update(
226	            build_phase_observability(
227	                step,
228	                configured_timeout_seconds=configured_timeout_seconds,
229	                age_seconds=age_seconds,
230	                lock_held=lock_held,
231	            )
232	        )
233	        if details.get("stale"):
234	            orphaned = not lock_held
235	            details["orphaned"] = orphaned
236	            if orphaned:
237	                if step == "execute":
238	                    details["recovery_hint"] = (
239	                        "The active step is stale and no process holds the plan lock. "
240	                        "Safe next action: rerun the same execute command on Codex without --fresh."
241	                    )
242	                else:
243	                    details["recovery_hint"] = (
244	                        "The active step is stale and no process holds the plan lock. "
245	                        "Safe next action: rerun the same step on the same agent before escalating."
246	                    )
247	        max_seconds = int(details.get("expected_duration_seconds", {}).get("max", 0) or 0)
248	        elapsed_label = humanize_seconds(age_seconds)
249	        if details.get("stale"):
250	            details["phase_progress_summary"] = (
251	                f"{step} stale ({elapsed_label} elapsed, expected max {humanize_seconds(max_seconds)}) "
252	                "see recovery_hint."
253	            )
254	        elif step in {"execute", "loop_execute"}:
255	            details["phase_progress_summary"] = (
256	                f"{step} running ({elapsed_label} elapsed, use progress for batch-level detail)."
257	            )
258	        else:
259	            details["phase_progress_summary"] = (
260	                f"{step} running ({elapsed_label} elapsed, typically completes within "
261	                f"{humanize_seconds(max_seconds)})."
262	            )
263	            if max_seconds > 0:
264	                details["progress_pct"] = min(95, int((age_seconds / max_seconds) * 100))
265	    else:
266	        details.update(
267	            build_phase_observability(
268	                step,
269	                configured_timeout_seconds=configured_timeout_seconds,
270	                lock_held=lock_held,
271	            )
272	        )
273	        if step in {"execute", "loop_execute"}:
274	            details["phase_progress_summary"] = (
275	                f"{step} active (start time unknown, use progress for batch-level detail)."
276	            )
277	        else:
278	            details["phase_progress_summary"] = f"{step} active (start time unknown)."
279	    return details
280	
281	
282	def _build_status_payload(plan_dir: Path, state: dict[str, Any]) -> StepResponse:
283	    next_steps = infer_next_steps(state)
284	    notes = state.get("meta", {}).get("notes", [])
285	    lock_path = plan_dir / ".plan.lock"
286	    lock_file_present = lock_path.exists()
287	    lock_held = plan_lock_is_held(plan_dir)
288	    active_step = _build_active_step(state.get("active_step"), plan_dir=plan_dir)
289	    last_step = _build_last_step(state)
290	    summary = f"Plan '{state['name']}' is currently in state '{state['current_state']}'."
291	    if active_step:
292	        summary = (
293	            summary
294	            + f" Active step: {active_step.get('step')} via {active_step.get('agent')}."
295	        )
296	    elif lock_file_present and not lock_held:
297	        summary = (
298	            summary
299	            + " No active step. The `.plan.lock` file may remain on disk even when no process holds the lock."
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/cli.py",
  "offset": 300,
  "limit": 200
}
```

> TOOL

tool_result Read
```
300	        )
301	    response: StepResponse = {
302	        "success": True,
303	        "step": "status",
304	        "plan": state["name"],
305	        "state": state["current_state"],
306	        "iteration": state["iteration"],
307	        "summary": summary,
308	        "next_step": next_steps[0] if next_steps else None,
309	        "valid_next": next_steps,
310	        "artifacts": sorted(
311	            path.name
312	            for path in plan_dir.iterdir()
313	            if path.is_file() and path.name != ".plan.lock"
314	        ),
315	        "lock_file_present": lock_file_present,
316	        "lock_held": lock_held,
317	        "active_step": active_step,
318	        "last_step": last_step,
319	        "total_cost_usd": state.get("meta", {}).get("total_cost_usd", 0.0),
320	        "notes_count": len(notes) if isinstance(notes, list) else 0,
321	        "notes": notes if isinstance(notes, list) else [],
322	        "session_summaries": [
323	            {"key": key, **value}
324	            for key, value in sorted(state.get("sessions", {}).items())
325	            if isinstance(value, dict)
326	        ],
327	    }
328	    runtime = build_next_step_runtime(
329	        response.get("next_step"),
330	        configured_timeout_seconds=int(get_effective("execution", "worker_timeout_seconds")),
331	    )
332	    if runtime is not None:
333	        response["next_step_runtime"] = runtime
334	    progress = _build_progress_payload(plan_dir, state) if (plan_dir / "finalize.json").exists() else None
335	    if progress is not None:
336	        response["progress"] = progress
337	        response["summary"] = response["summary"] + " " + progress["summary"]
338	    return response
339	
340	
341	def handle_status(root: Path, args: argparse.Namespace) -> StepResponse:
342	    plan_dir, state = load_plan(root, args.plan)
343	    return _build_status_payload(plan_dir, state)
344	
345	
346	def handle_audit(root: Path, args: argparse.Namespace) -> StepResponse:
347	    plan_dir, state = load_plan(root, args.plan)
348	    return {
349	        "success": True,
350	        "step": "audit",
351	        "plan": state["name"],
352	        "plan_dir": str(plan_dir),
353	        "state": state,
354	    }
355	
356	
357	def handle_progress(root: Path, args: argparse.Namespace) -> StepResponse:
358	    plan_dir, state = load_plan(root, args.plan)
359	    progress = _build_progress_payload(plan_dir, state)
360	    return {
361	        "success": True,
362	        "step": "progress",
363	        "plan": state["name"],
364	        **progress,
365	    }
366	
367	
368	def handle_watch(root: Path, args: argparse.Namespace) -> StepResponse:
369	    response = handle_status(root, args)
370	    response["step"] = "watch"
371	    return response
372	
373	
374	def _collect_megaplan_roots(root: Path, *, tree: bool = False, all_system: bool = False) -> list[Path]:
375	    """Collect .megaplan root directories based on search mode."""
376	    roots: list[Path] = [root]
377	
378	    if all_system:
379	        # Search from home directory downward for all .megaplan directories
380	        home = Path.home()
381	        for megaplan_dir in sorted(home.rglob(".megaplan")):
382	            if megaplan_dir.is_dir() and (megaplan_dir / "plans").is_dir():
383	                candidate = megaplan_dir.parent
384	                if candidate.resolve() != root.resolve():
385	                    roots.append(candidate)
386	    elif tree:
387	        # Walk up to find parent .megaplan directories
388	        current = root.resolve().parent
389	        while True:
390	            if (current / ".megaplan" / "plans").is_dir() and current.resolve() != root.resolve():
391	                roots.append(current)
392	            parent = current.parent
393	            if parent == current:
394	                break
395	            current = parent
396	        # Walk down to find child .megaplan directories
397	        for megaplan_dir in sorted(root.rglob(".megaplan")):
398	            if megaplan_dir.is_dir() and (megaplan_dir / "plans").is_dir():
399	                candidate = megaplan_dir.parent
400	                if candidate.resolve() != root.resolve():
401	                    roots.append(candidate)
402	
403	    return roots
404	
405	
406	def handle_list(root: Path, args: argparse.Namespace) -> StepResponse:
407	    ensure_runtime_layout(root)
408	    filter_status = getattr(args, "filter_status", None)
409	    no_tree = getattr(args, "no_tree", False)
410	    include_done = getattr(args, "include_done", False)
411	    show_summary = getattr(args, "summary", False)
412	    search_all = getattr(args, "all", False)
413	    # Default: tree=True (parent+child), active-only (exclude done/aborted)
414	    # --status overrides the active filter (explicit filter = show exactly that)
415	    search_tree = not no_tree and not search_all
416	    filter_active = not include_done and not filter_status
417	
418	    roots = _collect_megaplan_roots(root, tree=search_tree, all_system=search_all)
419	    total_scanned = 0
420	    allowed_states: set[str] | None = None
421	    if filter_status:
422	        allowed_states = {s.strip() for s in filter_status.split(",")}
423	
424	    items = []
425	    state_counts: dict[str, int] = {}
426	    resolved_root = root.resolve()
427	    for search_root in roots:
428	        resolved_search = search_root.resolve()
429	        is_local = resolved_search == resolved_root
430	        for plan_dir in active_plan_dirs(search_root):
431	            state = read_json(plan_dir / "state.json")
432	            current_state = state["current_state"]
433	            state_counts[current_state] = state_counts.get(current_state, 0) + 1
434	            total_scanned += 1
435	
436	            if filter_active and current_state in TERMINAL_STATES:
437	                continue
438	            if allowed_states and current_state not in allowed_states:
439	                continue
440	
441	            next_steps = infer_next_steps(state)
442	            entry = {
443	                "name": state["name"],
444	                "idea": state["idea"],
445	                "state": current_state,
446	                "iteration": state["iteration"],
447	                "next_step": next_steps[0] if next_steps else None,
448	            }
449	            if not is_local:
450	                try:
451	                    rel = resolved_search.relative_to(resolved_root)
452	                    entry["location"] = f"./{rel}"
453	                    entry["direction"] = "child"
454	                except ValueError:
455	                    try:
456	                        resolved_root.relative_to(resolved_search)
457	                        entry["location"] = os.path.relpath(resolved_search, resolved_root)
458	                        entry["direction"] = "parent"
459	                    except ValueError:
460	                        entry["location"] = str(resolved_search)
461	                        entry["direction"] = "external"
462	            items.append(entry)
463	
464	    summary_parts = [f"Found {len(items)} plans"]
465	    if len(roots) > 1:
466	        summary_parts.append(f"across {len(roots)} directories")
467	    if allowed_states:
468	        summary_parts.append(f"matching {','.join(sorted(allowed_states))}")
469	    if filter_active:
470	        summary_parts.append("(active only)")
471	
472	    result: StepResponse = {
473	        "success": True,
474	        "step": "list",
475	        "summary": f"{'. '.join(summary_parts)}.",
476	        "plans": items,
477	    }
478	    if show_summary:
479	        result["state_summary"] = dict(sorted(state_counts.items()))
480	
481	    # Hints for discovering more plans
482	    hidden_done = total_scanned - len(items) if filter_active else 0
483	    hints: list[str] = []
484	    if hidden_done > 0:
485	        hints.append(f"{hidden_done} completed plans hidden (use --include-done to show)")
486	    if not search_all:
487	        hints.append("Use --all to search all plans system-wide")
488	    if hints:
489	        result["hints"] = hints
490	
491	    return result
492	
493	
494	def handle_debt(root: Path, args: argparse.Namespace) -> StepResponse:
495	    ensure_runtime_layout(root)
496	    action = args.debt_action
497	    registry = load_debt_registry(root)
498	    default_plan_id = getattr(args, "plan", None) or "manual"
499
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/checks.py",
  "offset": 1,
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	"""Critique check registry and helpers."""
2	
3	from __future__ import annotations
4	
5	from typing import Any, Final, TypedDict
6	
7	
8	VALID_SEVERITY_HINTS: Final[set[str]] = {"likely-significant", "likely-minor", "uncertain"}
9	
10	
11	class CritiqueCheckSpec(TypedDict):
12	    id: str
13	    question: str
14	    guidance: str
15	    category: str
16	    default_severity: str
17	    tier: str
18	
19	
20	CRITIQUE_CHECKS: Final[tuple[CritiqueCheckSpec, ...]] = (
21	    {
22	        "id": "issue_hints",
23	        "question": "Did the work fully address the issue hints, user notes, and approved plan requirements?",
24	        "guidance": (
25	            "Cross-check the result against explicit user notes, critique corrections, and watch items. "
26	            "Flag anything the implementation ignored, contradicted, or only partially covered."
27	        ),
28	        "category": "completeness",
29	        "default_severity": "likely-significant",
30	        "tier": "core",
31	    },
32	    {
33	        "id": "correctness",
34	        "question": "Are the proposed changes technically correct?",
35	        "guidance": (
36	            "Look for logic errors, invalid assumptions, broken invariants, schema mismatches, "
37	            "or behavior that would fail at runtime. When the fix adds a conditional branch, "
38	            "check whether it handles all relevant cases — not just the one reported in the issue."
39	        ),
40	        "category": "correctness",
41	        "default_severity": "likely-significant",
42	        "tier": "core",
43	    },
44	    {
45	        "id": "scope",
46	        "question": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?",
47	        "guidance": (
48	            "Look at how the changed function is used across the codebase. Does the fix only address "
49	            "one caller's scenario while others remain broken? Flag missing required work or out-of-scope "
50	            "edits. A minimal patch is often right, but check whether the underlying problem is bigger "
51	            "than what the issue describes."
52	        ),
53	        "category": "completeness",
54	        "default_severity": "likely-significant",
55	        "tier": "core",
56	    },
57	    {
58	        "id": "all_locations",
59	        "question": "Does the change touch all locations AND supporting infrastructure?",
60	        "guidance": (
61	            "Search for all instances of the symbol/pattern being changed. Also ask: does this "
62	            "feature require setup, registration, or integration code beyond the core logic? "
63	            "Missing glue code causes test failures even when the core fix is correct."
64	        ),
65	        "category": "completeness",
66	        "default_severity": "likely-significant",
67	        "tier": "core",
68	    },
69	    {
70	        "id": "callers",
71	        "question": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?",
72	        "guidance": (
73	            "Grep for call sites. For each caller, check what values it passes — especially edge cases "
74	            "like None, zero, empty, or composite inputs. Then ask: should this change be here, or in "
75	            "a caller, callee, or new method?"
76	        ),
77	        "category": "correctness",
78	        "default_severity": "likely-significant",
79	        "tier": "core",
80	    },
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/checks.py",
  "offset": 80,
  "limit": 100
}
```

> TOOL

tool_result Read
```
80	    },
81	    {
82	        "id": "conventions",
83	        "question": "Does the approach match how the codebase solves similar problems?",
84	        "guidance": (
85	            "Check not just naming/style but how similar PROBLEMS are solved in this codebase. "
86	            "If the codebase adds new methods for similar cases, the plan should too. "
87	            "Do not spend findings on trivial stylistic preferences."
88	        ),
89	        "category": "maintainability",
90	        "default_severity": "likely-minor",
91	        "tier": "extended",
92	    },
93	    {
94	        "id": "verification",
95	        "question": "Is there convincing verification for the change?",
96	        "guidance": (
97	            "Flag missing tests or weak validation. If verification tests exist, trace the test's "
98	            "execution path through your patch — does every branch it exercises produce the expected "
99	            "result? A patch can look correct but fail because it misses one code path the test covers. "
100	            "If you manually verify an edge case because existing tests don't cover it, also test the cases next to it."
101	        ),
102	        "category": "completeness",
103	        "default_severity": "likely-minor",
104	        "tier": "extended",
105	    },
106	    {
107	        "id": "criteria_quality",
108	        "question": "Are the success criteria well-prioritized and verifiable?",
109	        "guidance": (
110	            "Check that each `must` criterion has a clear yes/no answer verifiable from code, tests, or "
111	            "git diff. Subjective goals, numeric guidelines, and aspirational targets should be `should`, "
112	            "not `must`. Criteria requiring manual testing or human judgment should be `info`. "
113	            "Flag any `must` criterion that is ambiguous, subjective, or unverifiable in the review pipeline."
114	        ),
115	        "category": "completeness",
116	        "default_severity": "likely-significant",
117	        "tier": "extended",
118	    },
119	)
120	
121	_CHECK_BY_ID: Final[dict[str, CritiqueCheckSpec]] = {check["id"]: check for check in CRITIQUE_CHECKS}
122	_CORE_CRITIQUE_CHECKS: Final[tuple[CritiqueCheckSpec, ...]] = tuple(
123	    check for check in CRITIQUE_CHECKS if check["tier"] == "core"
124	)
125	
126	
127	def get_check_ids() -> list[str]:
128	    return [check["id"] for check in CRITIQUE_CHECKS]
129	
130	
131	def get_check_by_id(check_id: str) -> CritiqueCheckSpec | None:
132	    return _CHECK_BY_ID.get(check_id)
133	
134	
135	def build_check_category_map() -> dict[str, str]:
136	    return {check["id"]: check["category"] for check in CRITIQUE_CHECKS}
137	
138	
139	def checks_for_robustness(robustness: str) -> tuple[CritiqueCheckSpec, ...]:
140	    if robustness in {"robust", "superrobust"}:
141	        return CRITIQUE_CHECKS
142	    if robustness in {"light", "tiny"}:
143	        return ()
144	    return _CORE_CRITIQUE_CHECKS
145	
146	
147	def build_empty_template(checks: tuple[CritiqueCheckSpec, ...] | None = None) -> list[dict[str, Any]]:
148	    active_checks = CRITIQUE_CHECKS if checks is None else checks
149	    return [
150	        {
151	            "id": check["id"],
152	            "question": check["question"],
153	            "findings": [],
154	        }
155	        for check in active_checks
156	    ]
157	
158	
159	_MIN_FINDING_DETAIL_LENGTH = 40  # Must describe what was checked, not just "No issue"
160	
161	
162	def _valid_findings(findings: Any) -> bool:
163	    if not isinstance(findings, list) or not findings:
164	        return False
165	    for finding in findings:
166	        if not isinstance(finding, dict):
167	            return False
168	        detail = finding.get("detail")
169	        flagged = finding.get("flagged")
170	        if not isinstance(detail, str) or not detail.strip():
171	            return False
172	        if len(detail.strip()) < _MIN_FINDING_DETAIL_LENGTH:
173	            return False
174	        if not isinstance(flagged, bool):
175	            return False
176	    return True
177	
178	
179	def validate_critique_checks(
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/workers.py",
  "offset": 450,
  "limit": 120
}
```

> TOOL

tool_result Read
```
450	    if not isinstance(payload, dict):
451	        raise CliError("parse_error", f"Output file {path.name} did not contain a JSON object")
452	    return payload
453	
454	
455	def _recover_codex_payload(
456	    step: str,
457	    *,
458	    plan_dir: Path,
459	    output_path: Path,
460	    raw: str,
461	) -> dict[str, Any] | None:
462	    payload = None
463	    try:
464	        payload = parse_json_file(output_path)
465	    except CliError:
466	        pass
467	    if payload is None:
468	        fallback_names = {
469	            "critique": "critique_output.json",
470	        }
471	        fallback_name = fallback_names.get(step, f"{step}_output.json")
472	        fallback_path = plan_dir / fallback_name
473	        if fallback_path != output_path and fallback_path.exists():
474	            try:
475	                payload = parse_json_file(fallback_path)
476	            except CliError:
477	                pass
478	    raw_candidates = _extract_json_candidates_from_raw(raw)
479	    candidate_payloads: list[dict[str, Any]] = []
480	    if payload is not None:
481	        candidate_payloads.append(payload)
482	    candidate_payloads.extend(raw_candidates)
483	    valid_payloads: list[dict[str, Any]] = []
484	    for candidate in candidate_payloads:
485	        normalized = _normalize_codex_payload(step, candidate)
486	        try:
487	            validate_payload(step, normalized)
488	        except CliError:
489	            continue
490	        valid_payloads.append(normalized)
491	    if not valid_payloads:
492	        return None
493	    if step == "critique" and len(valid_payloads) > 1:
494	        def _findings_count(item: dict[str, Any]) -> int:
495	            checks = item.get("checks", [])
496	            return sum(len(check.get("findings", [])) for check in checks if isinstance(check, dict))
497	
498	        return max(valid_payloads, key=_findings_count)
499	    return valid_payloads[0]
500	
501	
502	def validate_payload(step: str, payload: dict[str, Any]) -> None:
503	    if step == "execute":
504	        full_required = _STEP_REQUIRED_KEYS.get(step, [])
505	        missing_full = [key for key in full_required if key not in payload]
506	        if not missing_full:
507	            return
508	        batch_required = ["task_updates", "sense_check_acknowledgments"]
509	        missing_batch = [key for key in batch_required if key not in payload]
510	        if not missing_batch:
511	            return
512	        raise CliError(
513	            "parse_error",
514	            (
515	                "execute output missing required keys: "
516	                + ", ".join(missing_full)
517	                + ". Batch execute payloads may omit aggregate fields, "
518	                + "but must include task_updates and sense_check_acknowledgments."
519	            ),
520	        )
521	    required = _STEP_REQUIRED_KEYS.get(step)
522	    if required is None:
523	        return
524	    missing = [key for key in required if key not in payload]
525	    if missing:
526	        raise CliError("parse_error", f"{step} output missing required keys: {', '.join(missing)}")
527	
528	
529	def _mock_result(
530	    payload: dict[str, Any],
531	    *,
532	    trace_output: str | None = None,
533	) -> WorkerResult:
534	    return WorkerResult(
535	        payload=payload,
536	        raw_output=json_dump(payload),
537	        duration_ms=10,
538	        cost_usd=0.0,
539	        session_id=str(uuid.uuid4()),
540	        trace_output=trace_output,
541	    )
542	
543	
544	def _deep_merge(base: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
545	    merged = dict(base)
546	    for key, value in overrides.items():
547	        base_value = merged.get(key)
548	        if isinstance(base_value, dict) and isinstance(value, dict):
549	            merged[key] = _deep_merge(base_value, value)
550	            continue
551	        merged[key] = value
552	    return merged
553	
554	
555	def _default_mock_plan_payload(state: PlanState, plan_dir: Path) -> dict[str, Any]:
556	    payload: dict[str, Any] = {
557	        "plan": textwrap.dedent(
558	            f"""
559	            # Implementation Plan: Mock Planning Pass
560	
561	            ## Overview
562	            Produce a concrete plan for: {state['idea']}. Keep the scope grounded in the repository and define validation before execution.
563	
564	            ## Step 1: Inspect the current flow (`megaplan/workers.py`)
565	            **Scope:** Small
566	            1. **Inspect** the planner and prompt touch points before editing (`megaplan/workers.py:199`, `megaplan/prompts.py:29`).
567	
568	            ## Step 2: Implement the smallest viable change (`megaplan/handlers.py`)
569	            **Scope:** Medium
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/workers.py",
  "offset": 700,
  "limit": 150
}
```

> TOOL

tool_result Read
```
700	        "disputed_flag_ids": [],
701	    }
702	
703	
704	
705	def _default_mock_revise_payload(state: PlanState, plan_dir: Path) -> dict[str, Any]:
706	    return {
707	        "plan": textwrap.dedent(
708	            f"""
709	            # Implementation Plan: Mock Revision Pass
710	
711	            ## Overview
712	            Refine the plan for: {state['idea']}. Tighten file-level scope and keep validation explicit.
713	
714	            ## Step 1: Reconfirm file scope (`megaplan/handlers.py`)
715	            **Scope:** Small
716	            1. **Inspect** the exact edit points before changing the plan (`megaplan/handlers.py:540`).
717	
718	            ## Step 2: Tighten the implementation slice (`megaplan/workers.py`)
719	            **Scope:** Medium
720	            1. **Limit** the plan to the smallest coherent change set (`megaplan/workers.py:256`).
721	            2. **Illustrate** the intended shape when it helps reviewers.
722	               ```python
723	               changes_summary = "Added explicit scope and verification details."
724	               ```
725	
726	            ## Step 3: Reconfirm verification (`tests/test_workers.py`)
727	            **Scope:** Small
728	            1. **Run** a concrete verification command and record the expected proof point (`tests/test_workers.py:251`).
729	
730	            ## Execution Order
731	            1. Re-scope the plan before adjusting implementation details.
732	            2. Re-run validation after the plan is tightened.
733	
734	            ## Validation Order
735	            1. Start with the focused worker and handler tests.
736	            2. End with the broader suite if the focused checks pass.
737	            """
738	        ).strip(),
739	        "changes_summary": "Added explicit repo-scoping and verification steps.",
740	        "flags_addressed": ["FLAG-001", "FLAG-002"],
741	        "assumptions": ["The repository contains enough context for implementation."],
742	        "success_criteria": [
743	            {"criterion": "The plan identifies exact touch points before editing.", "priority": "must"},
744	            {"criterion": "A concrete verification command is defined.", "priority": "should"},
745	        ],
746	        "questions": [],
747	    }
748	
749	
750	def _default_mock_gate_payload(state: PlanState, plan_dir: Path) -> dict[str, Any]:
751	    recommendation = "ITERATE" if state["iteration"] == 1 else "PROCEED"
752	    return {
753	        "recommendation": recommendation,
754	        "rationale": (
755	            "First critique cycle still needs another pass."
756	            if recommendation == "ITERATE"
757	            else "Signals are strong enough to move into execution."
758	        ),
759	        "signals_assessment": (
760	            "Iteration 1 still carries unresolved significant flags and should revise."
761	            if recommendation == "ITERATE"
762	            else "Weighted score and loop trajectory support proceeding."
763	        ),
764	        "warnings": [],
765	        "settled_decisions": [],
766	        "flag_resolutions": [],
767	        "accepted_tradeoffs": [],
768	    }
769	
770	
771	def _default_mock_finalize_payload(state: PlanState, plan_dir: Path) -> dict[str, Any]:
772	    return {
773	        "tasks": [
774	            {
775	                "id": "T1",
776	                "description": f"Implement: {state['idea']}",
777	                "depends_on": [],
778	                "status": "pending",
779	                "executor_notes": "",
780	                "files_changed": [],
781	                "commands_run": [],
782	                "evidence_files": [],
783	                "reviewer_verdict": "",
784	            },
785	            {
786	                "id": "T2",
787	                "description": "Verify success criteria",
788	                "depends_on": [],
789	                "status": "pending",
790	                "executor_notes": "",
791	                "files_changed": [],
792	                "commands_run": [],
793	                "evidence_files": [],
794	                "reviewer_verdict": "",
795	            },
796	        ],
797	        "watch_items": ["Ensure repository state matches plan assumptions"],
798	        "sense_checks": [
799	            {
800	                "id": "SC1",
801	                "task_id": "T1",
802	                "question": "Verify implementation matches the stated idea.",
803	                "executor_note": "",
804	                "verdict": "",
805	            },
806	            {
807	                "id": "SC2",
808	                "task_id": "T2",
809	                "question": "Verify success criteria were actually checked.",
810	                "executor_note": "",
811	                "verdict": "",
812	            },
813	        ],
814	        "meta_commentary": "This is a mock finalize output.",
815	        "validation": {
816	            "plan_steps_covered": [
817	                {"plan_step_summary": f"Implement: {state['idea']}", "finalize_task_ids": ["T1"]},
818	                {"plan_step_summary": "Verify success criteria", "finalize_task_ids": ["T2"]},
819	            ],
820	            "orphan_tasks": [],
821	            "completeness_notes": "All plan steps mapped to tasks.",
822	            "coverage_complete": True,
823	        },
824	    }
825	
826	
827	def _task_ids_from_prompt_override(prompt_override: str | None) -> set[str] | None:
828	    if prompt_override is None:
829	        return None
830	    match = re.search(r"Only produce `?task_updates`? for these tasks:\s*\[([^\]]*)\]", prompt_override)
831	    if match is None:
832	        return None
833	    task_ids = {item.strip() for item in match.group(1).split(",") if item.strip()}
834	    return task_ids
835	
836	
837	def _default_mock_execute_payload(
838	    state: PlanState,
839	    plan_dir: Path,
840	    *,
841	    prompt_override: str | None = None,
842	) -> dict[str, Any]:
843	    target = Path(state["config"]["project_dir"]) / "IMPLEMENTED_BY_MEGAPLAN.txt"
844	    relative_target = str(target.relative_to(Path(state["config"]["project_dir"])))
845	    payload = {
846	        "output": "Mock execution completed successfully.",
847	        "files_changed": [relative_target],
848	        "commands_run": ["mock-write IMPLEMENTED_BY_MEGAPLAN.txt"],
849	        "deviations": [],
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"^def run_\" /Users/user_c042661f/Documents/megaplan/megaplan/workers.py",
  "description": "Find run_ function definitions in workers.py"
}
```

> TOOL

tool_result Bash
```
94:def run_command(
1088:def run_claude_step(
1142:def run_codex_step(
1479:def run_step_with_worker(
[rerun: b3]
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/workers.py",
  "offset": 1088,
  "limit": 100
}
```

> TOOL

tool_result Read
```
1088	def run_claude_step(
1089	    step: str,
1090	    state: PlanState,
1091	    plan_dir: Path,
1092	    *,
1093	    root: Path,
1094	    fresh: bool,
1095	    prompt_override: str | None = None,
1096	    prompt_kwargs: dict[str, Any] | None = None,
1097	) -> WorkerResult:
1098	    if os.getenv(MOCK_ENV_VAR) == "1":
1099	        return mock_worker_output(step, state, plan_dir, prompt_override=prompt_override, prompt_kwargs=prompt_kwargs)
1100	    project_dir = Path(state["config"]["project_dir"])
1101	    schema_name = STEP_SCHEMA_FILENAMES[step]
1102	    schema_text = json.dumps(read_json(schemas_root(root) / schema_name))
1103	    session_key = session_key_for(step, "claude")
1104	    session = state["sessions"].get(session_key, {})
1105	    session_id = session.get("id")
1106	    command = ["claude", "-p", "--output-format", "json", "--json-schema", schema_text, "--add-dir", str(project_dir)]
1107	    if step in _EXECUTE_STEPS:
1108	        command.extend(["--permission-mode", "bypassPermissions"])
1109	    if session_id and not fresh:
1110	        command.extend(["--resume", session_id])
1111	    else:
1112	        session_id = str(uuid.uuid4())
1113	        command.extend(["--session-id", session_id])
1114	    prompt = prompt_override if prompt_override is not None else create_claude_prompt(
1115	        step,
1116	        state,
1117	        plan_dir,
1118	        root=root,
1119	        **(prompt_kwargs or {}),
1120	    )
1121	    try:
1122	        result = run_command(command, cwd=project_dir, stdin_text=prompt)
1123	    except CliError as error:
1124	        if error.code == "worker_timeout":
1125	            error.extra["session_id"] = session_id
1126	        raise
1127	    raw = result.stdout or result.stderr
1128	    envelope, payload = parse_claude_envelope(raw)
1129	    try:
1130	        validate_payload(step, payload)
1131	    except CliError as error:
1132	        raise CliError(error.code, error.message, extra={"raw_output": raw}) from error
1133	    return WorkerResult(
1134	        payload=payload,
1135	        raw_output=raw,
1136	        duration_ms=result.duration_ms,
1137	        cost_usd=float(envelope.get("total_cost_usd", 0.0) or 0.0),
1138	        session_id=str(envelope.get("session_id") or session_id),
1139	    )
1140	
1141	
1142	def run_codex_step(
1143	    step: str,
1144	    state: PlanState,
1145	    plan_dir: Path,
1146	    *,
1147	    root: Path,
1148	    persistent: bool,
1149	    fresh: bool = False,
1150	    json_trace: bool = False,
1151	    prompt_override: str | None = None,
1152	    prompt_kwargs: dict[str, Any] | None = None,
1153	) -> WorkerResult:
1154	    if os.getenv(MOCK_ENV_VAR) == "1":
1155	        return mock_worker_output(step, state, plan_dir, prompt_override=prompt_override, prompt_kwargs=prompt_kwargs)
1156	    project_dir = Path(state["config"]["project_dir"])
1157	    schema_file = schemas_root(root) / STEP_SCHEMA_FILENAMES[step]
1158	    session_key = session_key_for(step, "codex")
1159	    session = state["sessions"].get(session_key, {})
1160	    out_handle = tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False)
1161	    out_handle.close()
1162	    output_path = Path(out_handle.name)
1163	    prompt = prompt_override if prompt_override is not None else create_codex_prompt(
1164	        step,
1165	        state,
1166	        plan_dir,
1167	        root=root,
1168	        **(prompt_kwargs or {}),
1169	    )
1170	    timeout_seconds = _codex_timeout_for_step(step)
1171	
1172	    if persistent and session.get("id") and not fresh:
1173	        # codex exec resume does not support --output-schema; we rely on
1174	        # validate_payload() after parsing the output file instead. It also
1175	        # does not accept --add-dir; resumed sessions keep the workspace that
1176	        # was granted when the session was created.
1177	        command = ["codex", "exec", "resume"]
1178	        command.extend(_codex_exec_mode_flags(step))
1179	        if json_trace:
1180	            command.append("--json")
1181	        command.extend([
1182	            "--skip-git-repo-check",
1183	            "-o", str(output_path),
1184	            str(session["id"]), "-",
1185	        ])
1186	    else:
1187	        command = [
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/workers.py",
  "offset": 1142,
  "limit": 100
}
```

> TOOL

tool_result Read
```
1142	def run_codex_step(
1143	    step: str,
1144	    state: PlanState,
1145	    plan_dir: Path,
1146	    *,
1147	    root: Path,
1148	    persistent: bool,
1149	    fresh: bool = False,
1150	    json_trace: bool = False,
1151	    prompt_override: str | None = None,
1152	    prompt_kwargs: dict[str, Any] | None = None,
1153	) -> WorkerResult:
1154	    if os.getenv(MOCK_ENV_VAR) == "1":
1155	        return mock_worker_output(step, state, plan_dir, prompt_override=prompt_override, prompt_kwargs=prompt_kwargs)
1156	    project_dir = Path(state["config"]["project_dir"])
1157	    schema_file = schemas_root(root) / STEP_SCHEMA_FILENAMES[step]
1158	    session_key = session_key_for(step, "codex")
1159	    session = state["sessions"].get(session_key, {})
1160	    out_handle = tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False)
1161	    out_handle.close()
1162	    output_path = Path(out_handle.name)
1163	    prompt = prompt_override if prompt_override is not None else create_codex_prompt(
1164	        step,
1165	        state,
1166	        plan_dir,
1167	        root=root,
1168	        **(prompt_kwargs or {}),
1169	    )
1170	    timeout_seconds = _codex_timeout_for_step(step)
1171	
1172	    if persistent and session.get("id") and not fresh:
1173	        # codex exec resume does not support --output-schema; we rely on
1174	        # validate_payload() after parsing the output file instead. It also
1175	        # does not accept --add-dir; resumed sessions keep the workspace that
1176	        # was granted when the session was created.
1177	        command = ["codex", "exec", "resume"]
1178	        command.extend(_codex_exec_mode_flags(step))
1179	        if json_trace:
1180	            command.append("--json")
1181	        command.extend([
1182	            "--skip-git-repo-check",
1183	            "-o", str(output_path),
1184	            str(session["id"]), "-",
1185	        ])
1186	    else:
1187	        command = [
1188	            "codex",
1189	            "exec",
1190	            "--skip-git-repo-check",
1191	            "-C",
1192	            str(project_dir),
1193	            "--add-dir",
1194	            str(plan_dir),
1195	        ]
1196	        if _trusted_container():
1197	            # In a trusted container the surrounding runtime is the sandbox.
1198	            # Skip the workspace-write sandbox (which requires user namespaces
1199	            # that most container runtimes don't grant) and let Codex run
1200	            # unsandboxed. The outer container boundary still contains writes.
1201	            command.append("--dangerously-bypass-approvals-and-sandbox")
1202	        else:
1203	            command.extend([
1204	                "-c",
1205	                f"sandbox_workspace_write.writable_roots=[\"{project_dir}\"]",
1206	            ])
1207	        command.extend([
1208	            "-o",
1209	            str(output_path),
1210	        ])
1211	        if not persistent:
1212	            command.append("--ephemeral")
1213	        command.extend(_codex_exec_mode_flags(step))
1214	        if json_trace:
1215	            command.append("--json")
1216	        command.extend(["--output-schema", str(schema_file), "-"])
1217	
1218	    try:
1219	        result = run_command(
1220	            command,
1221	            cwd=Path.cwd(),
1222	            stdin_text=prompt,
1223	            env=_codex_child_env(),
1224	            timeout=timeout_seconds,
1225	        )
1226	    except CliError as error:
1227	        error.extra["raw_output"] = _merge_partial_output(
1228	            str(error.extra.get("raw_output", "")),
1229	            output_path,
1230	        )
1231	        # Recover from a lost session: container restarted since the session was
1232	        # created, codex's rollout store is gone, but megaplan still has the id.
1233	        # Clear the stale session and retry once with fresh=True.
1234	        if not fresh and persistent and session.get("id") and _is_rollout_missing(
1235	            str(error.extra.get("raw_output", ""))
1236	        ):
1237	            log.info(
1238	                "Codex session %s has no rollout (container restart or session wipe); "
1239	                "retrying %s with a fresh session",
1240	                session["id"],
1241	                step,
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/workers.py",
  "offset": 1479,
  "limit": 100
}
```

> TOOL

tool_result Read
```
1479	def run_step_with_worker(
1480	    step: str,
1481	    state: PlanState,
1482	    plan_dir: Path,
1483	    args: argparse.Namespace,
1484	    *,
1485	    root: Path,
1486	    resolved: tuple[str, str, bool, str | None] | None = None,
1487	    prompt_override: str | None = None,
1488	    prompt_kwargs: dict[str, Any] | None = None,
1489	) -> tuple[WorkerResult, str, str, bool]:
1490	    agent, mode, refreshed, model = resolved or resolve_agent_mode(step, args)
1491	    effective_refreshed = refreshed
1492	    explicit_agent = _agent_requested_explicitly(step, args)
1493	    attempted_agents: set[str] = set()
1494	    while True:
1495	        attempted_agents.add(agent)
1496	        try:
1497	            if agent == "hermes":
1498	                # Deferred import to avoid circular import (hermes_worker imports from workers)
1499	                from megaplan.hermes_worker import run_hermes_step
1500	                worker = run_hermes_step(
1501	                    step,
1502	                    state,
1503	                    plan_dir,
1504	                    root=root,
1505	                    fresh=effective_refreshed,
1506	                    model=model,
1507	                    prompt_override=prompt_override,
1508	                )
1509	            elif agent == "claude":
1510	                worker = run_claude_step(
1511	                    step,
1512	                    state,
1513	                    plan_dir,
1514	                    root=root,
1515	                    fresh=effective_refreshed,
1516	                    prompt_override=prompt_override,
1517	                    prompt_kwargs=prompt_kwargs,
1518	                )
1519	            else:
1520	                attempted_retry = False
1521	                while True:
1522	                    try:
1523	                        worker = run_codex_step(
1524	                            step,
1525	                            state,
1526	                            plan_dir,
1527	                            root=root,
1528	                            persistent=(mode == "persistent"),
1529	                            fresh=effective_refreshed,
1530	                            json_trace=(step == "execute"),
1531	                            prompt_override=prompt_override,
1532	                            prompt_kwargs=prompt_kwargs,
1533	                        )
1534	                        break
1535	                    except CliError as error:
1536	                        session_id = error.extra.get("session_id")
1537	                        if (
1538	                            attempted_retry
1539	                            or step in _EXECUTE_STEPS
1540	                            or error.code not in {"worker_timeout", "connection_error"}
1541	                        ):
1542	                            raise
1543	                        attempted_retry = True
1544	                        if mode == "persistent" and isinstance(session_id, str) and session_id:
1545	                            apply_session_update(
1546	                                state,
1547	                                step,
1548	                                agent,
1549	                                session_id,
1550	                                mode=mode,
1551	                                refreshed=effective_refreshed,
1552	                            )
1553	                            effective_refreshed = False
1554	                        continue
1555	            return worker, agent, mode, effective_refreshed
1556	        except CliError as error:
1557	            if explicit_agent or error.code not in {"auth_error", "connection_error"}:
1558	                raise
1559	            fallback_candidates = [
1560	                candidate
1561	                for candidate in _runtime_fallback_candidates(agent)
1562	                if candidate not in attempted_agents
1563	            ]
1564	            if not fallback_candidates:
1565	                raise
1566	            fallback_agent = fallback_candidates[0]
1567	            args._agent_fallback = {
1568	                "requested": agent,
1569	                "resolved": fallback_agent,
1570	                "reason": f"{agent} runtime unhealthy: {error.code}",
1571	            }
1572	            agent = fallback_agent
1573	            model = None
1574	            effective_refreshed = True
1575
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/hermes_worker.py",
  "offset": 1,
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	"""Hermes Agent worker for megaplan — runs phases via AIAgent with OpenRouter."""
2	
3	from __future__ import annotations
4	
5	import json
6	import os
7	import sys
8	import time
9	from pathlib import Path
10	
11	from megaplan.types import CliError, MOCK_ENV_VAR, PlanState
12	from megaplan.workers import (
13	    STEP_SCHEMA_FILENAMES,
14	    WorkerResult,
15	    mock_worker_output,
16	    session_key_for,
17	    validate_payload,
18	)
19	from megaplan._core import read_json, schemas_root
20	from megaplan.prompts import create_hermes_prompt
21	
22	
23	def check_hermes_available() -> tuple[bool, str]:
24	    """Check if Hermes Agent is importable and has API credentials."""
25	    try:
26	        from run_agent import AIAgent  # noqa: F401
27	    except ImportError:
28	        return (False, "hermes-agent not installed. Install with: pip install hermes-agent")
29	
30	    # Check for API key — Hermes stores keys in ~/.hermes/.env, loaded via dotenv.
31	    # After dotenv load, the key is available as an env var.
32	    api_key = os.environ.get("OPENROUTER_API_KEY")
33	    if not api_key:
34	        # Try loading from Hermes .env file directly
35	        try:
36	            from hermes_cli.config import get_env_path
37	            env_path = get_env_path()
38	            if env_path and env_path.exists():
39	                for line in env_path.read_text().splitlines():
40	                    line = line.strip()
41	                    if line.startswith("OPENROUTER_API_KEY="):
42	                        api_key = line.split("=", 1)[1].strip().strip("'\"")
43	                        break
44	        except (ImportError, Exception):
45	            pass
46	
47	    if not api_key:
48	        return (False, "OPENROUTER_API_KEY not set. Configure via env var or ~/.hermes/.env")
49	    return (True, "")
50	
51	
52	def _toolsets_for_phase(phase: str) -> list[str] | None:
53	    """Return toolsets for a given megaplan phase.
54	
55	    Execute phase gets full terminal + file + web access.
56	    Plan, critique, and revise get file + web (verify APIs against docs).
57	    Gate, finalize, review get file only (judgment, not investigation).
58	    """
59	    if phase == "execute":
60	        return ["terminal", "file", "web"]
61	    if phase in ("plan", "prep", "critique", "revise"):
62	        return ["file", "web"]
63	    return ["file"]
64	
65	
66	_TEMPLATE_FILE_PHASES = {"finalize", "review", "prep"}
67	_CUSTOM_TEMPLATE_PHASES = {"critique", "review"}
68	
69	
70	def _template_has_content(payload: dict, step: str) -> bool:
71	    """Check if a template-file payload has real content (not just the empty template)."""
72	    if step == "critique":
73	        # For critique: check if any check has non-empty findings
74	        checks = payload.get("checks", [])
75	        if isinstance(checks, list):
76	            for check in checks:
77	                if isinstance(check, dict):
78	                    findings = check.get("findings", [])
79	                    if isinstance(findings, list) and findings:
80	                        return True
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py",
  "offset": 1,
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	"""Gate-signal scoring and loop diagnostics."""
2	
3	from __future__ import annotations
4	
5	import os
6	import re
7	import subprocess
8	from dataclasses import dataclass
9	from difflib import SequenceMatcher
10	from pathlib import Path
11	from typing import Any, Callable
12	
13	from megaplan.types import (
14	    FLAG_BLOCKING_STATUSES,
15	    FlagRecord,
16	    GateArtifact,
17	    GateCheckResult,
18	    GatePayload,
19	    GateSignals,
20	    PlanState,
21	)
22	from megaplan._core import (
23	    configured_robustness,
24	    current_iteration_artifact,
25	    escalated_subsystems,
26	    extract_subsystem_tag,
27	    find_matching_debt,
28	    latest_plan_meta_path,
29	    latest_plan_path,
30	    load_debt_registry,
31	    load_flag_registry,
32	    normalize_text,
33	    read_json,
34	    scope_creep_flags,
35	    unresolved_significant_flags,
36	)
37	
38	
39	PLAN_STRUCTURE_REQUIRED_STEP_ISSUE = "Plan must include at least one step section (`## Step N:` or `### Step N:` under a phase)."
40	_PLAN_HEADING_RE = re.compile(r"^##\s+.+$")
41	_PLAN_PHASE_HEADING_RE = re.compile(r"^###\s+.+$")
42	_PLAN_STEP_RE = re.compile(r"^##\s+Step\s+(\d+):\s+.+$")
43	_PLAN_PHASE_STEP_RE = re.compile(r"^###\s+Step\s+(\d+):\s+.+$")
44	_GENERIC_ACKS = {
45	    "ack",
46	    "checked",
47	    "confirmed",
48	    "done",
49	    "good",
50	    "looks good",
51	    "n/a",
52	    "na",
53	    "ok",
54	    "verified",
55	    "yes",
56	}
57	_MIN_VERDICT_CHARS = 20
58	_MIN_VERDICT_WORDS = 4
59	_MIN_VERDICT_UNIQUE_WORDS = 3
60	
61	
62	@dataclass(frozen=True)
63	class PlanSection:
64	    heading: str
65	    body: str
66	    id: str | None
67	    start_line: int
68	    end_line: int
69	
70	
71	def _normalize_repo_path(path: str, project_dir: Path | None = None) -> str:
72	    p = Path(path.strip())
73	    if project_dir is not None and p.is_absolute():
74	        try:
75	            project_abs = project_dir.resolve()
76	            resolved = p.resolve()
77	            rel = resolved.relative_to(project_abs)
78	            return rel.as_posix()
79	        except (ValueError, OSError):
80	            pass
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/cli.py",
  "offset": 500,
  "limit": 200
}
```

> TOOL

tool_result Read
```
500	    if action == "list":
501	        entries = registry["entries"] if args.all else [entry for entry in registry["entries"] if not entry["resolved"]]
502	        grouped: dict[str, list[dict[str, Any]]] = {}
503	        for entry in entries:
504	            grouped.setdefault(entry["subsystem"], []).append(entry)
505	        escalated = {
506	            subsystem: total
507	            for subsystem, total, _entries in escalated_subsystems(registry)
508	        }
509	        by_subsystem = [
510	            {
511	                "subsystem": subsystem,
512	                "escalated": subsystem in escalated,
513	                "total_occurrences": subsystem_occurrence_total(entries_for_subsystem)
514	                if not args.all
515	                else sum(entry["occurrence_count"] for entry in entries_for_subsystem if not entry["resolved"]),
516	                "entries": entries_for_subsystem,
517	            }
518	            for subsystem, entries_for_subsystem in sorted(grouped.items())
519	        ]
520	        return {
521	            "success": True,
522	            "step": "debt",
523	            "action": "list",
524	            "summary": f"Found {len(entries)} debt entries across {len(by_subsystem)} subsystem groups.",
525	            "details": {
526	                "entries": entries,
527	                "by_subsystem": by_subsystem,
528	                "escalated_subsystems": [
529	                    {"subsystem": subsystem, "total_occurrences": total}
530	                    for subsystem, total in sorted(escalated.items())
531	                ],
532	            },
533	        }
534	
535	    if action == "add":
536	        flag_ids = [
537	            flag_id.strip()
538	            for flag_id in (args.flag_ids or "").split(",")
539	            if flag_id.strip()
540	        ]
541	        entry = add_or_increment_debt(
542	            registry,
543	            subsystem=args.subsystem,
544	            concern=args.concern,
545	            flag_ids=flag_ids,
546	            plan_id=default_plan_id,
547	        )
548	        save_debt_registry(root, registry)
549	        return {
550	            "success": True,
551	            "step": "debt",
552	            "action": "add",
553	            "summary": f"Tracked debt entry {entry['id']} for subsystem '{entry['subsystem']}'.",
554	            "details": {"entry": entry},
555	        }
556	
557	    if action == "resolve":
558	        entry = resolve_debt(registry, args.debt_id, default_plan_id)
559	        save_debt_registry(root, registry)
560	        return {
561	            "success": True,
562	            "step": "debt",
563	            "action": "resolve",
564	            "summary": f"Resolved debt entry {entry['id']}.",
565	            "details": {"entry": entry},
566	        }
567	
568	    raise CliError("invalid_args", f"Unknown debt action: {action}")
569	
570	
571	# ---------------------------------------------------------------------------
572	# Setup and config
573	# ---------------------------------------------------------------------------
574	
575	def _canonical_instructions() -> str:
576	    return resources.files("megaplan").joinpath("data", "instructions.md").read_text(encoding="utf-8")
577	
578	
579	_SKILL_HEADER = """\
580	---
581	name: megaplan
582	description: AI agent harness for coordinating Claude and GPT to make and execute extremely robust plans.
583	---
584	
585	"""
586	
587	_CURSOR_HEADER = """\
588	---
589	description: Use megaplan for high-rigor planning on complex, high-risk, or multi-stage tasks.
590	alwaysApply: false
591	---
592	
593	"""
594	
595	
596	def bundled_agents_md() -> str:
597	    return _canonical_instructions()
598	
599	
600	def _subagent_appendix(filename: str) -> str:
601	    content = resources.files("megaplan").joinpath("data", filename).read_text(encoding="utf-8")
602	    content = content.replace(
603	        "{max_execute_no_progress}",
604	        str(get_effective("execution", "max_execute_no_progress")),
605	    )
606	    content = content.replace(
607	        "{max_review_rework_cycles}",
608	        str(get_effective("execution", "max_review_rework_cycles")),
609	    )
610	    return content
611	
612	
613	def _claude_subagent_appendix() -> str:
614	    return _subagent_appendix("claude_subagent_appendix.md")
615	
616	
617	def _codex_subagent_appendix() -> str:
618	    return _subagent_appendix("codex_subagent_appendix.md")
619	
620	
621	def bundled_global_file(name: str) -> str:
622	    content = _canonical_instructions()
623	    if name == "claude_skill.md":
624	        return _SKILL_HEADER + content + "\n\n" + _claude_subagent_appendix()
625	    if name == "codex_skill.md":
626	        return _SKILL_HEADER + content + "\n\n" + _codex_subagent_appendix()
627	    if name == "skill.md":
628	        return _SKILL_HEADER + content
629	    if name == "cursor_rule.mdc":
630	        return _CURSOR_HEADER + content
631	    return content
632	
633	
634	_GLOBAL_TARGETS = [
635	    {"agent": "claude", "detect": ".claude", "path": ".claude/skills/megaplan/SKILL.md", "data": "claude_skill.md"},
636	    {"agent": "codex", "detect": ".codex", "path": ".codex/skills/megaplan/SKILL.md", "data": "codex_skill.md"},
637	    {"agent": "cursor", "detect": ".cursor", "path": ".cursor/rules/megaplan.mdc", "data": "cursor_rule.mdc"},
638	]
639	
640	
641	def _install_owned_file(path: Path, content: str, *, force: bool = False) -> dict[str, bool | str]:
642	    existed = path.exists()
643	    if existed and not force:
644	        if path.read_text(encoding="utf-8") == content:
645	            return {"path": str(path), "skipped": True, "existed": True}
646	    atomic_write_text(path, content)
647	    return {"path": str(path), "skipped": False, "existed": existed}
648	
649	
650	def handle_setup_global(force: bool = False, home: Path | None = None) -> StepResponse:
651	    if home is None:
652	        home = Path.home()
653	    installed: list[dict[str, Any]] = []
654	    detected_count = 0
655	    for target in _GLOBAL_TARGETS:
656	        agent_dir = home / target["detect"]
657	        if not agent_dir.is_dir():
658	            installed.append({"agent": target["agent"], "path": str(home / target["path"]), "skipped": True, "reason": "not installed"})
659	            continue
660	        detected_count += 1
661	        result = _install_owned_file(home / target["path"], bundled_global_file(target["data"]), force=force)
662	        result["agent"] = target["agent"]
663	        installed.append(result)
664	    if detected_count == 0:
665	        return {
666	            "success": False, "step": "setup", "mode": "global",
667	            "summary": "No supported agents detected. Create one of ~/.claude/, ~/.codex/, or ~/.cursor/ and re-run.",
668	            "installed": installed,
669	        }
670	    available = detect_available_agents()
671	    config_path = None
672	    routing = None
673	    if available:
674	        agents_config = {step: (default if default in available else available[0]) for step, default in DEFAULT_AGENT_ROUTING.items()}
675	        config = load_config(home)
676	        config["agents"] = agents_config
677	        config_path = save_config(config, home)
678	        routing = agents_config
679	    lines = []
680	    for rec in installed:
681	        if rec.get("reason") == "not installed":
682	            lines.append(f"  {rec['agent']}: skipped (not installed)")
683	        elif rec["skipped"]:
684	            lines.append(f"  {rec['agent']}: up to date")
685	        else:
686	            lines.append(f"  {rec['agent']}: {'overwrote' if rec['existed'] else 'created'} {rec['path']}")
687	    result_data: dict[str, Any] = {"success": True, "step": "setup", "mode": "global", "summary": "Global setup complete:\n" + "\n".join(lines), "installed": installed}
688	    if config_path is not None:
689	        result_data["config_path"] = str(config_path)
690	        result_data["routing"] = routing
691	    return result_data
692	
693	
694	def handle_setup(args: argparse.Namespace) -> StepResponse:
695	    local = args.local or args.target_dir
696	    if not local:
697	        return handle_setup_global(force=args.force)
698	    target_dir = Path(args.target_dir).resolve() if args.target_dir else Path.cwd()
699	    target = target_dir / "AGENTS.md"
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/phase_runtime.py",
  "offset": 1,
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	"""Centralized per-phase runtime policy for patience, polling, and timeouts."""
2	
3	from __future__ import annotations
4	
5	from dataclasses import asdict, dataclass
6	from typing import Any
7	
8	
9	DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS = 900
10	
11	
12	@dataclass(frozen=True)
13	class PhaseRuntimePolicy:
14	    expected_min_seconds: int
15	    expected_max_seconds: int | None
16	    recommended_next_check_seconds: int
17	    escalation_threshold_seconds: int | None
18	    timeout_cap_seconds: int | None
19	    artifact_mode: str = "completion_only"
20	
21	
22	@dataclass(frozen=True)
23	class ResolvedPhaseRuntime:
24	    expected_duration_seconds: dict[str, int]
25	    recommended_next_check_seconds: int
26	    escalation_threshold_seconds: int
27	    timeout_budget_seconds: int
28	    artifact_mode: str
29	
30	
31	PHASE_RUNTIME_POLICY: dict[str, PhaseRuntimePolicy] = {
32	    "prep": PhaseRuntimePolicy(
33	        expected_min_seconds=30,
34	        expected_max_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
35	        recommended_next_check_seconds=60,
36	        escalation_threshold_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
37	        timeout_cap_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
38	    ),
39	    "plan": PhaseRuntimePolicy(
40	        expected_min_seconds=60,
41	        expected_max_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
42	        recommended_next_check_seconds=120,
43	        escalation_threshold_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
44	        timeout_cap_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
45	    ),
46	    "critique": PhaseRuntimePolicy(
47	        expected_min_seconds=60,
48	        expected_max_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
49	        recommended_next_check_seconds=120,
50	        escalation_threshold_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
51	        timeout_cap_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
52	    ),
53	    "revise": PhaseRuntimePolicy(
54	        expected_min_seconds=60,
55	        expected_max_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
56	        recommended_next_check_seconds=120,
57	        escalation_threshold_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
58	        timeout_cap_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
59	    ),
60	    "gate": PhaseRuntimePolicy(
61	        expected_min_seconds=30,
62	        expected_max_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
63	        recommended_next_check_seconds=60,
64	        escalation_threshold_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
65	        timeout_cap_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
66	    ),
67	    "finalize": PhaseRuntimePolicy(
68	        expected_min_seconds=60,
69	        expected_max_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
70	        recommended_next_check_seconds=120,
71	        escalation_threshold_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
72	        timeout_cap_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
73	    ),
74	    "execute": PhaseRuntimePolicy(
75	        expected_min_seconds=300,
76	        expected_max_seconds=None,
77	        recommended_next_check_seconds=300,
78	        escalation_threshold_seconds=None,
79	        timeout_cap_seconds=None,
80	    ),
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/cli.py",
  "offset": 700,
  "limit": 200
}
```

> TOOL

tool_result Read
```
700	    content = bundled_agents_md()
701	    if target.exists() and not args.force:
702	        existing = target.read_text(encoding="utf-8")
703	        if "megaplan" in existing.lower():
704	            return {"success": True, "step": "setup", "summary": f"AGENTS.md already contains megaplan instructions at {target}", "skipped": True}
705	        atomic_write_text(target, existing + "\n\n" + content)
706	        return {"success": True, "step": "setup", "summary": f"Appended megaplan instructions to existing {target}", "file": str(target)}
707	    atomic_write_text(target, content)
708	    return {"success": True, "step": "setup", "summary": f"Created {target}", "file": str(target)}
709	
710	
711	def handle_config(args: argparse.Namespace) -> StepResponse:
712	    action = args.config_action
713	    if action == "show":
714	        config = load_config()
715	        effective_routing = {step: config.get("agents", {}).get(step, default) for step, default in DEFAULT_AGENT_ROUTING.items()}
716	        effective_settings = {
717	            dot_key: get_effective(section, setting)
718	            for dot_key in sorted(DEFAULTS)
719	            for section, setting in [dot_key.split(".", 1)]
720	        }
721	        return {
722	            "success": True,
723	            "step": "config",
724	            "action": "show",
725	            "config_path": str(config_dir() / "config.json"),
726	            "routing": effective_routing,
727	            "effective_settings": effective_settings,
728	            "raw_config": config,
729	        }
730	    if action == "set":
731	        key, value = args.key, args.value
732	        parts = key.split(".", 1)
733	        config = load_config()
734	        valid_keys = [
735	            *(f"agents.{step}" for step in DEFAULT_AGENT_ROUTING),
736	            "orchestration.mode",
737	            *sorted(_SETTABLE_BOOL),
738	            *sorted(_SETTABLE_ENUM),
739	            *sorted(_SETTABLE_NUMERIC),
740	        ]
741	        if len(parts) != 2:
742	            raise CliError(
743	                "invalid_args",
744	                f"Unknown config key '{key}'. Valid keys: {', '.join(valid_keys)}",
745	            )
746	        section, setting = parts
747	        normalized_value = value.strip().lower()
748	        if section == "agents":
749	            if setting not in DEFAULT_AGENT_ROUTING:
750	                raise CliError("invalid_args", f"Unknown step '{setting}'. Valid steps: {', '.join(DEFAULT_AGENT_ROUTING)}")
751	            if value not in KNOWN_AGENTS:
752	                raise CliError("invalid_args", f"Unknown agent '{value}'. Valid agents: {', '.join(KNOWN_AGENTS)}")
753	            config.setdefault("agents", {})[setting] = value
754	        elif key == "orchestration.mode":
755	            if value not in {"inline", "subagent"}:
756	                raise CliError("invalid_args", "orchestration.mode must be 'inline' or 'subagent'")
757	            config.setdefault("orchestration", {})["mode"] = value
758	        elif key in _SETTABLE_BOOL:
759	            if normalized_value in {"true", "1", "yes", "on"}:
760	                parsed_value = True
761	            elif normalized_value in {"false", "0", "no", "off"}:
762	                parsed_value = False
763	            else:
764	                raise CliError(
765	                    "invalid_args",
766	                    f"{key} must be one of: true, false, 1, 0, yes, no, on, off",
767	                )
768	            config.setdefault(section, {})[setting] = parsed_value
769	        elif key in _SETTABLE_ENUM:
770	            allowed_values = _SETTABLE_ENUM[key]
771	            if value not in allowed_values:
772	                raise CliError(
773	                    "invalid_args",
774	                    f"{key} must be one of: {', '.join(allowed_values)}",
775	                )
776	            config.setdefault(section, {})[setting] = value
777	        elif key in _SETTABLE_NUMERIC:
778	            try:
779	                parsed_value = int(value)
780	            except ValueError as exc:
781	                raise CliError("invalid_args", f"{key} must be an integer, got '{value}'") from exc
782	            config.setdefault(section, {})[setting] = parsed_value
783	        else:
784	            raise CliError(
785	                "invalid_args",
786	                f"Unknown config key '{key}'. Valid keys: {', '.join(valid_keys)}",
787	            )
788	        save_config(config)
789	        return {"success": True, "step": "config", "action": "set", "key": key, "value": config[section][setting]}
790	    if action == "reset":
791	        path = config_dir() / "config.json"
792	        if path.exists():
793	            path.unlink()
794	        return {"success": True, "step": "config", "action": "reset", "summary": "Config file removed. Using defaults."}
795	    raise CliError("invalid_args", f"Unknown config action: {action}")
796	
797	
798	# ---------------------------------------------------------------------------
799	# Parser and dispatch
800	# ---------------------------------------------------------------------------
801	
802	def build_parser() -> argparse.ArgumentParser:
803	    parser = argparse.ArgumentParser(description="Megaplan orchestration CLI")
804	    subparsers = parser.add_subparsers(dest="command", required=True)
805	
806	    setup_parser = subparsers.add_parser("setup", help="Install megaplan into agent configs (global by default)")
807	    setup_parser.add_argument("--local", action="store_true", help="Install AGENTS.md into a project instead of global agent configs")
808	    setup_parser.add_argument("--target-dir", help="Directory to install into (default: cwd, implies --local)")
809	    setup_parser.add_argument("--force", action="store_true", help="Overwrite existing files")
810	
811	    init_parser = subparsers.add_parser("init")
812	    init_parser.add_argument("--project-dir", required=True)
813	    init_parser.add_argument("--name")
814	    init_parser.add_argument("--auto-approve", action="store_true", default=None)
815	    init_parser.add_argument("--robustness", choices=list(ROBUSTNESS_LEVELS), default=None)
816	    init_parser.add_argument("--hermes", nargs="?", const="", default=None,
817	                             help="Use Hermes agent for all phases. Optional: specify default model")
818	    init_parser.add_argument("--phase-model", action="append", default=[],
819	                             help="Per-phase model override: --phase-model critique=hermes:openai/gpt-5")
820	    init_parser.add_argument("idea")
821	
822	    list_parser = subparsers.add_parser("list")
823	    list_parser.add_argument("--all", action="store_true",
824	                             help="Search all .megaplan directories system-wide (~)")
825	    list_parser.add_argument("--no-tree", action="store_true",
826	                             help="Only show plans from the current directory (default includes parent + child)")
827	    list_parser.add_argument("--include-done", action="store_true",
828	                             help="Include terminal plans (done/aborted); excluded by default")
829	    list_parser.add_argument("--status", dest="filter_status",
830	                             help="Filter by state (e.g. 'done', 'finalized', 'executed', or comma-separated 'planned,critiqued')")
831	    list_parser.add_argument("--summary", action="store_true",
832	                             help="Show count breakdown by state")
833	
834	    for name in ["status", "audit", "progress", "watch"]:
835	        step_parser = subparsers.add_parser(name)
836	        step_parser.add_argument("--plan")
837	
838	    for name in ["plan", "prep", "critique", "revise", "gate", "finalize", "execute", "review"]:
839	        step_parser = subparsers.add_parser(name)
840	        step_parser.add_argument("--plan")
841	        step_parser.add_argument("--agent", choices=["claude", "codex", "hermes"])
842	        step_parser.add_argument("--hermes", nargs="?", const="", default=None,
843	                                 help="Use Hermes agent for all phases. Optional: specify default model (e.g. --hermes anthropic/claude-sonnet-4.6)")
844	        step_parser.add_argument("--phase-model", action="append", default=[],
845	                                 help="Per-phase model override: --phase-model critique=hermes:openai/gpt-5")
846	        step_parser.add_argument("--fresh", action="store_true")
847	        step_parser.add_argument("--persist", action="store_true")
848	        step_parser.add_argument("--ephemeral", action="store_true")
849	        if name == "execute":
850	            step_parser.add_argument("--confirm-destructive", action="store_true")
851	            step_parser.add_argument("--user-approved", action="store_true")
852	            step_parser.add_argument("--batch", type=int, default=None, help="Execute a specific global batch number (1-indexed)")
853	        if name == "review":
854	            step_parser.add_argument("--confirm-self-review", action="store_true")
855	
856	    config_parser = subparsers.add_parser("config", help="View or edit megaplan configuration")
857	    config_sub = config_parser.add_subparsers(dest="config_action", required=True)
858	    config_sub.add_parser("show")
859	    set_parser = config_sub.add_parser("set")
860	    set_parser.add_argument("key")
861	    set_parser.add_argument("value")
862	    config_sub.add_parser("reset")
863	
864	    step_parser = subparsers.add_parser("step", help="Edit plan step sections without hand-editing markdown")
865	    step_subparsers = step_parser.add_subparsers(dest="step_action", required=True)
866	
867	    step_add_parser = step_subparsers.add_parser("add", help="Insert a new step after an existing step")
868	    step_add_parser.add_argument("--plan")
869	    step_add_parser.add_argument("--after")
870	    step_add_parser.add_argument("description")
871	
872	    step_remove_parser = step_subparsers.add_parser("remove", help="Remove a step and renumber the plan")
873	    step_remove_parser.add_argument("--plan")
874	    step_remove_parser.add_argument("step_id")
875	
876	    step_move_parser = step_subparsers.add_parser("move", help="Move a step after another step and renumber")
877	    step_move_parser.add_argument("--plan")
878	    step_move_parser.add_argument("step_id")
879	    step_move_parser.add_argument("--after", required=True)
880	
881	    override_parser = subparsers.add_parser("override")
882	    override_parser.add_argument("override_action", choices=["abort", "force-proceed", "add-note", "replan", "set-robustness"])
883	    override_parser.add_argument("--plan")
884	    override_parser.add_argument("--reason", default="")
885	    override_parser.add_argument("--note")
886	    override_parser.add_argument("--robustness", choices=list(ROBUSTNESS_LEVELS), default=None)
887	
888	    debt_parser = subparsers.add_parser("debt", help="Inspect or manage persistent tech debt entries")
889	    debt_subparsers = debt_parser.add_subparsers(dest="debt_action", required=True)
890	
891	    debt_list_parser = debt_subparsers.add_parser("list", help="List debt entries")
892	    debt_list_parser.add_argument("--all", action="store_true", help="Include resolved entries")
893	
894	    debt_add_parser = debt_subparsers.add_parser("add", help="Add or increment a debt entry")
895	    debt_add_parser.add_argument("--subsystem", required=True)
896	    debt_add_parser.add_argument("--concern", required=True)
897	    debt_add_parser.add_argument("--flag-ids", default="")
898	    debt_add_parser.add_argument("--plan")
899
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/cli.py",
  "offset": 900,
  "limit": 120
}
```

> TOOL

tool_result Read
```
900	    debt_resolve_parser = debt_subparsers.add_parser("resolve", help="Resolve a debt entry")
901	    debt_resolve_parser.add_argument("debt_id")
902	    debt_resolve_parser.add_argument("--plan")
903	
904	    loop_init_parser = subparsers.add_parser("loop-init", help="Initialize a MegaLoop workflow")
905	    loop_init_parser.add_argument("--project-dir", required=True)
906	    loop_init_parser.add_argument("--command", required=True)
907	    loop_init_parser.add_argument("--goal", dest="goal_option")
908	    loop_init_parser.add_argument("--name")
909	    loop_init_parser.add_argument("--iterations", type=int, default=3)
910	    loop_init_parser.add_argument("--time-budget", type=int, default=300)
911	    loop_init_parser.add_argument("--observe-interval", type=int)
912	    loop_init_parser.add_argument("--observe-break-patterns")
913	    loop_init_parser.add_argument("--agent", choices=["claude", "codex", "hermes"])
914	    loop_init_parser.add_argument("--hermes", nargs="?", const="", default=None,
915	                                  help="Use Hermes agent for loop phases. Optional: specify default model")
916	    loop_init_parser.add_argument("--phase-model", action="append", default=[],
917	                                  help="Per-phase model override: --phase-model loop_execute=hermes:openai/gpt-5")
918	    loop_init_parser.add_argument("--fresh", action="store_true")
919	    loop_init_parser.add_argument("--persist", action="store_true")
920	    loop_init_parser.add_argument("--ephemeral", action="store_true")
921	    loop_init_parser.add_argument("goal", nargs="?")
922	
923	    loop_run_parser = subparsers.add_parser("loop-run", help="Run an existing MegaLoop workflow")
924	    loop_run_parser.add_argument("name")
925	    loop_run_parser.add_argument("--project-dir")
926	    loop_run_parser.add_argument("--iterations", type=int)
927	    loop_run_parser.add_argument("--time-budget", type=int)
928	    loop_run_parser.add_argument("--agent", choices=["claude", "codex", "hermes"])
929	    loop_run_parser.add_argument("--hermes", nargs="?", const="", default=None,
930	                                 help="Use Hermes agent for loop phases. Optional: specify default model")
931	    loop_run_parser.add_argument("--phase-model", action="append", default=[],
932	                                 help="Per-phase model override: --phase-model loop_execute=hermes:openai/gpt-5")
933	    loop_run_parser.add_argument("--fresh", action="store_true")
934	    loop_run_parser.add_argument("--persist", action="store_true")
935	    loop_run_parser.add_argument("--ephemeral", action="store_true")
936	
937	    loop_status_parser = subparsers.add_parser("loop-status", help="Show MegaLoop state")
938	    loop_status_parser.add_argument("name")
939	    loop_status_parser.add_argument("--project-dir")
940	
941	    loop_pause_parser = subparsers.add_parser("loop-pause", help="Pause a MegaLoop workflow")
942	    loop_pause_parser.add_argument("name")
943	    loop_pause_parser.add_argument("--project-dir")
944	    loop_pause_parser.add_argument("--reason", default="")
945	
946	    from megaplan.auto import build_auto_parser
947	    build_auto_parser(subparsers)
948	
949	    return parser
950	
951	
952	COMMAND_HANDLERS: dict[str, Callable[..., StepResponse]] = {
953	    "init": handle_init,
954	    "plan": handle_plan,
955	    "prep": handle_prep,
956	    "critique": handle_critique,
957	    "revise": handle_revise,
958	    "gate": handle_gate,
959	    "finalize": handle_finalize,
960	    "execute": handle_execute,
961	    "review": handle_review,
962	    "status": handle_status,
963	    "audit": handle_audit,
964	    "progress": handle_progress,
965	    "watch": handle_watch,
966	    "list": handle_list,
967	    "loop-init": handle_loop_init,
968	    "loop-run": handle_loop_run,
969	    "loop-status": handle_loop_status,
970	    "loop-pause": handle_loop_pause,
971	    "debt": handle_debt,
972	    "step": handle_step,
973	    "override": handle_override,
974	}
975	
976	
977	def cli_entry() -> None:
978	    sys.exit(main())
979	
980	
981	def _find_megaplan_root(start: Path) -> Path:
982	    """Walk up from *start* to find the git-root directory containing ``.megaplan/``.
983	
984	    Strategy: find the git root first (like ``git rev-parse --show-toplevel``),
985	    then check if it has a ``.megaplan/`` directory.  This avoids ambiguity when
986	    nested subdirectories also have their own ``.megaplan/``.  Falls back to the
987	    nearest ancestor with ``.megaplan/`` if not in a git repo, and finally to
988	    *start* if nothing is found.
989	    """
990	    resolved = start.resolve()
991	
992	    # Try git root first — the canonical project root.
993	    git_root = _find_git_root(resolved)
994	    if git_root and (git_root / ".megaplan").is_dir():
995	        return git_root
996	
997	    # Fallback: walk up to find nearest .megaplan
998	    current = resolved
999	    while True:
1000	        if (current / ".megaplan").is_dir():
1001	            return current
1002	        parent = current.parent
1003	        if parent == current:
1004	            return start
1005	        current = parent
1006	
1007	
1008	def _find_git_root(start: Path) -> Path | None:
1009	    """Walk up to find the directory containing ``.git``."""
1010	    current = start
1011	    while True:
1012	        if (current / ".git").exists():
1013	            return current
1014	        parent = current.parent
1015	        if parent == current:
1016	            return None
1017	        current = parent
1018	
1019
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/megaplan/megaplan/data/",
  "description": "List data directory"
}
```

> TOOL

tool_result Bash
```
claude_subagent_appendix.md
codex_subagent_appendix.md
instructions.md
[rerun: b4]
```

> AGENT

I now have a thorough understanding of the codebase. Here is the complete report:

---

## Megaplan Repository: Architecture Report

### 1. Overall File Structure

The project is a Python package at `/Users/user_c042661f/Documents/megaplan/megaplan/` with the following top-level layout:

```
megaplan/                 ← Python package root
  __main__.py             ← entry point: python -m megaplan
  cli.py                  ← argparse + COMMAND_HANDLERS dispatch table
  types.py                ← all TypedDicts, constants, CliError
  schemas.py              ← JSON schema definitions for every step artifact
  handlers.py             ← one handle_* function per pipeline step
  workers.py              ← subprocess invocation of claude / codex / hermes
  execution.py            ← batched execute loop
  execution_quality.py    ← git-diff audit, quality deviations
  execution_timeout.py    ← timeout recovery
  evaluation.py           ← gate signal scoring, plan structure validation
  checks.py               ← critique check registry (CRITIQUE_CHECKS tuple)
  review_checks.py        ← review pre-check registry
  review_mechanical.py    ← run_pre_checks()
  flags.py                ← flag state transitions (critique/gate/review/revise)
  quality.py              ← line-count capture
  merge.py                ← _validate_and_merge_batch()
  parallel_critique.py    ← hermes-parallel critique
  parallel_review.py      ← hermes-parallel review
  hermes_worker.py        ← Hermes/OpenRouter agent worker
  key_pool.py             ← API key rotation
  auto.py                 ← auto-driver (drives full plan lifecycle hands-free)
  step_edit.py            ← handle_step: add/remove/move plan steps
  _core/
    __init__.py           ← re-exports from submodules
    io.py                 ← file I/O, config, schemas_root, artifact paths
    state.py              ← load/save plan state, history, sessions, plan lock
    workflow.py           ← WORKFLOW state machine + Transition + robustness
    registries.py         ← flag registry + debt registry
    phase_runtime.py      ← PHASE_RUNTIME_POLICY per step
  prompts/
    __init__.py           ← create_claude_prompt / create_codex_prompt / create_hermes_prompt
    planning.py           ← _plan_prompt, _prep_prompt, PLAN_TEMPLATE
    critique.py           ← _critique_prompt, _revise_prompt, _write_critique_template
    execute.py            ← _execute_prompt, _execute_batch_prompt
    finalize.py           ← _finalize_prompt
    gate.py               ← _gate_prompt
    review.py             ← _review_prompt, _write_review_template
    _shared.py            ← debt/note blocks, prep block rendering
  loop/
    __init__.py
    engine.py             ← MegaLoop iterative agent engine
    handlers.py           ← handle_loop_init/run/status/pause
    types.py              ← LoopSpec, LoopState, IterationResult TypedDicts
    prompts.py            ← build_loop_prompt
    git.py                ← git_commit, git_revert, parse_metric
  data/
    instructions.md       ← canonical AGENTS.md text
    claude_subagent_appendix.md
    codex_subagent_appendix.md
tests/                    ← pytest test suite
evals/                    ← SWE-bench evaluations
pyproject.toml            ← package metadata
```

---

### 2. How the Current Pipeline Works

The pipeline is a **typed state machine** defined in `/Users/user_c042661f/Documents/megaplan/megaplan/_core/workflow.py` (line 31). States are constants in `/Users/user_c042661f/Documents/megaplan/megaplan/types.py` (lines 12–21).

**Full robustness flow (robust/superrobust):**

```
initialized → [prep] → prepped → [plan] → planned → [critique] → critiqued
  → gate decision:
      PROCEED+passed → [gate] → gated → [finalize] → finalized → [execute] → executed → [review] → done
      ITERATE        → [revise] → planned  (loop back to critique)
      ESCALATE       → override required (add-note / force-proceed / abort)
```

**Standard (default):** skips `prep` — starts with `plan` directly.

**Light:** skips `prep`, skips `gate`, collapses revise → gated in one step, skips `review`.

**Tiny:** stubs out critique and gate entirely, jumps straight to `gated`.

The review step can cycle back: if `review_verdict == "needs_rework"`, the state returns to `finalized` and `execute` runs again (up to `max_review_rework_cycles`, default 3).

---

### 3. Key Files — Paths and Key Locations

**Entry point:**
- `/Users/user_c042661f/Documents/megaplan/megaplan/__main__.py` — 6 lines, calls `cli.main()`
- `/Users/user_c042661f/Documents/megaplan/megaplan/cli.py:802` — `build_parser()` defines all subcommands
- `/Users/user_c042661f/Documents/megaplan/megaplan/cli.py:952` — `COMMAND_HANDLERS` dict maps command names to handler functions

**State machine:**
- `/Users/user_c042661f/Documents/megaplan/megaplan/_core/workflow.py:31` — `WORKFLOW` dict (state → list of `Transition`)
- `/Users/user_c042661f/Documents/megaplan/megaplan/_core/workflow.py:74` — `_ROBUSTNESS_OVERRIDES` per robustness level
- `/Users/user_c042661f/Documents/megaplan/megaplan/_core/workflow.py:202` — `workflow_transition()` resolves the right transition
- `/Users/user_c042661f/Documents/megaplan/megaplan/_core/workflow.py:213` — `workflow_next()` / `infer_next_steps()` returns valid next steps

**Handlers (plan → execute → review flow):**
- `/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py:794` — `handle_plan()`
- `/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py:840` — `handle_prep()`
- `/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py:861` — `handle_critique()`
- `/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py:994` — `handle_revise()`
- `/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py:1049` — `handle_gate()`
- `/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py:1308` — `handle_finalize()`
- `/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py:1337` — `handle_execute()` — dispatches to `dispatch_execute_one_batch` or `dispatch_execute_auto_loop`
- `/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py:1576` — `handle_review()` — runs pre-checks, parallel review (hermes), merges verdicts, resolves rework cycles
- `/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py:2016` — `handle_override()`

**Worker invocation:**
- `/Users/user_c042661f/Documents/megaplan/megaplan/workers.py:1088` — `run_claude_step()` — calls `claude -p --output-format json --json-schema` via subprocess, parses envelope
- `/Users/user_c042661f/Documents/megaplan/megaplan/workers.py:1142` — `run_codex_step()` — calls `codex exec [resume|new]`, writes output to temp file
- `/Users/user_c042661f/Documents/megaplan/megaplan/workers.py:1479` — `run_step_with_worker()` — top-level dispatcher with agent fallback logic
- `/Users/user_c042661f/Documents/megaplan/megaplan/hermes_worker.py:1` — `run_hermes_step()` via `AIAgent` / OpenRouter

**Prompt templates:**
- `/Users/user_c042661f/Documents/megaplan/megaplan/prompts/__init__.py:46` — `_CLAUDE_PROMPT_BUILDERS`, `_CODEX_PROMPT_BUILDERS`, `_HERMES_PROMPT_BUILDERS` dispatch dicts
- `/Users/user_c042661f/Documents/megaplan/megaplan/prompts/planning.py:19` — `PLAN_TEMPLATE` (markdown plan format example)
- `/Users/user_c042661f/Documents/megaplan/megaplan/data/instructions.md` — canonical AGENTS.md / skill instructions

**Config:**
- Config stored in `~/.megaplan/config.json` (not a repo file), loaded via `_core/io.py`
- `/Users/user_c042661f/Documents/megaplan/megaplan/types.py:298` — `DEFAULTS` dict (all configurable settings with defaults)
- `/Users/user_c042661f/Documents/megaplan/megaplan/types.py:267` — `DEFAULT_AGENT_ROUTING` (which agent handles each step)

**Schemas:**
- `/Users/user_c042661f/Documents/megaplan/megaplan/schemas.py` — `SCHEMAS` dict with JSON schemas for `plan.json`, `prep.json`, `revise.json`, `gate.json`, `critique.json`, `finalize.json`, `execution.json`, `loop_plan.json`, `loop_execute.json`, `review.json`

---

### 4. How Steps Are Executed and Reviewed

**Execution (`execute` step):**
- Requires `--confirm-destructive` flag and either `auto_approve=True` in config or `--user-approved` CLI flag (line 1340–1350 in handlers.py)
- `finalize.json` is pre-split into dependency-ordered batches via `compute_global_batches()` / `compute_task_batches()`
- Each batch is sent to the agent (codex by default) as an `_execute_batch_prompt`
- After each batch, `_validate_and_merge_batch()` writes task statuses back to `finalize.json`
- Quality audit: `_observe_git_changes()`, `_check_done_task_evidence()`, `_collect_quality_deviations()` run between batches
- Session continuity: codex uses `codex exec resume <session_id>` for persistent sessions; `--fresh` forces a new session

**Review (`review` step):**
- Mechanical pre-checks run first (`run_pre_checks()` in `review_mechanical.py`) for robustness ≥ standard
- For `superrobust`, parallel review via `run_parallel_review()` (hermes splits checks)
- The agent produces `review.json` with `review_verdict` = `"approved"` or `"needs_rework"`
- `_merge_review_verdicts()` writes `reviewer_verdict` and `evidence_files` back into `finalize.json` for each task and sense check
- If `needs_rework`, `_resolve_review_outcome()` decides whether to cycle back to `finalized` (re-execute) or block if coverage is incomplete
- Review cycles are capped by `max_review_rework_cycles` (default 3) and `max_robust_review_rework_cycles` (default 2)

**Auto-driver (`megaplan auto`):**
- `/Users/user_c042661f/Documents/megaplan/megaplan/auto.py` — shells out `megaplan <step>` in a loop, handles ESCALATE (default: force-proceed), and bails on stalls (default 5 consecutive same-state iterations)

---

### 5. Modes and Step Types

**Robustness levels** (`types.py:280`): `tiny`, `light`, `standard`, `robust`, `superrobust`
- `tiny` — critique/gate stubbed; direct jump to gated
- `light` — no prep, no gate, no review; revise collapses directly to gated
- `standard` — no prep; full critique/gate/execute/review
- `robust` / `superrobust` — adds prep; superrobust adds extra critique checks

**Agent routing** (`types.py:267` — `DEFAULT_AGENT_ROUTING`):
- `plan`, `prep`, `revise`, `gate`, `finalize`, `loop_plan` → **claude**
- `critique`, `execute`, `loop_execute`, `review` → **codex**
- Any step can be overridden via `megaplan config set agents.<step> <agent>` or `--agent` / `--hermes` flags

**Three agents:**
- `claude` — invoked as `claude -p --output-format json --json-schema <schema>` with structured output
- `codex` — invoked as `codex exec` with `--output-schema` and temp output file; supports persistent sessions (`--persist`) or ephemeral (`--ephemeral`)
- `hermes` — Python API (`run_agent.AIAgent`) via OpenRouter; supports parallel critique/review for superrobust

**Session modes** (workers.py):
- `persistent` — reuses `codex exec resume <session_id>` across iterations (used in execute)
- `ephemeral` — no session reuse (default for non-execute steps with `--ephemeral`)
- `fresh` (`--fresh`) — force a new session even when a session ID is stored

**Worker step schemas** (`workers.py:51` — `STEP_SCHEMA_FILENAMES`): `plan`, `prep`, `revise`, `critique`, `gate`, `finalize`, `execute`, `loop_plan`, `loop_execute`, `review`

**MegaLoop** (separate from the plan pipeline):
- `loop-init` → `loop-run` → `loop-status` / `loop-pause`
- Iterative agent loop for optimization/debugging tasks
- Uses `loop_plan` and `loop_execute` steps with their own schemas
- State stored in `.megaplan/loops/<name>/state.json`
- Commits and reverts via `loop/git.py`
