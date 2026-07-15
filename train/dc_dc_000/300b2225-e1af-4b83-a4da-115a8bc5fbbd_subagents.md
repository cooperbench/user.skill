> DEVELOPER

Explore the megaplan project at /Users/user_c042661f/Documents/megaplan. I need to understand:

1. Overall file structure (ls the top-level and key subdirectories)
2. How CLI commands are registered in megaplan/cli.py — look for argparse subparser patterns
3. How handlers.py dispatches commands — look for handle_* functions
4. How workers are dispatched — find run_codex_step and run_claude_step, understand their signatures
5. How SessionDB works
6. The existing prompt files in megaplan/prompts/
7. The existing JSON schemas in schemas/
8. The types defined in megaplan/types.py
9. How existing phases (plan, critique, execute) wire their workers
10. Current version in pyproject.toml

Thoroughness: very thorough. Report file paths and line numbers for all key integration points.

> AGENT

I'll conduct a thorough exploration of the megaplan project. Let me start by examining the overall structure and then dive into the specific areas you've requested.

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/"
}
```

> TOOL

tool_result Bash
```
total 536
drwxr-xr-x  31 user_c042661f  staff    992 Apr 15 12:24 .
drwx------@ 95 user_c042661f  staff   3040 Apr 15 03:13 ..
-rw-r--r--@  1 user_c042661f  staff   6148 Apr 15 05:57 .DS_Store
drwxr-xr-x   3 user_c042661f  staff     96 Mar 19 23:23 .claude
drwxr-xr-x@ 13 user_c042661f  staff    416 Mar 23 06:09 .desloppify
drwxr-xr-x@  5 user_c042661f  staff    160 Mar 20 01:58 .doubledip
drwxr-xr-x  15 user_c042661f  staff    480 Apr 15 11:14 .git
-rw-r--r--   1 user_c042661f  staff    108 Mar 21 04:45 .gitignore
drwxr-xr-x@  7 user_c042661f  staff    224 Apr 10 22:58 .megaplan
drwxr-xr-x@  6 user_c042661f  staff    192 Mar 20 00:18 .pytest_cache
drwxr-xr-x@  5 user_c042661f  staff    160 Mar 20 19:24 .ruff_cache
drwxr-xr-x   8 user_c042661f  staff    256 Mar 31 02:33 .venv
-rw-r--r--   1 user_c042661f  staff   8755 Apr 15 11:10 CHANGELOG.md
-rw-r--r--   1 user_c042661f  staff   7637 Apr  7 16:18 LICENSE
-rw-r--r--   1 user_c042661f  staff   4572 Apr 11 04:25 README.md
-rw-r--r--@  1 user_c042661f  staff   7932 Mar 20 03:00 activity-summary-2026-03-20.md
drwxr-xr-x@  4 user_c042661f  staff    128 Mar 20 19:44 dist
drwxr-xr-x@  5 user_c042661f  staff    160 Apr  6 07:16 evals
-rw-r--r--@  1 user_c042661f  staff   7662 Apr 15 09:40 idea-doc-mode.txt
-rw-r--r--   1 user_c042661f  staff  16751 Apr 15 12:17 idea-gate-verifiability-critique.txt
-rw-r--r--   1 user_c042661f  staff  16976 Apr 15 12:24 idea-gate-verifiability-losses.txt
-rw-r--r--   1 user_c042661f  staff  16566 Apr 15 12:10 idea-gate-verifiability.txt
-rw-r--r--   1 user_c042661f  staff   6574 Apr 15 05:30 idea-v0.14-strict-gate.txt
drwxr-xr-x  32 user_c042661f  staff   1024 Apr 15 11:11 megaplan
-rw-r--r--@  1 user_c042661f  staff  32797 Apr  7 21:32 plan.md
-rw-r--r--   1 user_c042661f  staff    794 Apr 15 11:10 pyproject.toml
-rw-r--r--@  1 user_c042661f  staff   1338 Apr  8 12:17 review-severity-plumbing.critique_output.json
-rw-r--r--@  1 user_c042661f  staff   1539 Apr  8 13:26 rework-item-polish-critique_output.json
-rw-r--r--   1 user_c042661f  staff  91619 Apr  4 16:29 scorecard.png
drwxr-xr-x  24 user_c042661f  staff    768 Apr 15 11:10 tests
-rw-r--r--   1 user_c042661f  staff    138 Apr 13 00:58 uv.lock
[rerun: b1]
```

> AGENT

Now let me explore the megaplan directory structure and key files:

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/megaplan/"
}
```

> TOOL

tool_result Bash
```
total 1056
drwxr-xr-x  32 user_c042661f  staff   1024 Apr 15 11:11 .
drwxr-xr-x  31 user_c042661f  staff    992 Apr 15 12:24 ..
-rw-r--r--@  1 user_c042661f  staff   6148 Apr 15 05:52 .DS_Store
-rw-r--r--   1 user_c042661f  staff   2640 Apr 10 22:54 __init__.py
-rw-r--r--   1 user_c042661f  staff    105 Mar 20 17:07 __main__.py
drwxr-xr-x@ 74 user_c042661f  staff   2368 Apr 15 11:11 __pycache__
drwxr-xr-x   9 user_c042661f  staff    288 Apr 13 05:06 _core
-rw-r--r--   1 user_c042661f  staff  14691 Apr 15 04:03 auto.py
-rw-r--r--   1 user_c042661f  staff  21068 Apr 15 11:11 chain.py
-rw-r--r--   1 user_c042661f  staff   8799 Apr 11 04:21 checks.py
-rw-r--r--   1 user_c042661f  staff  43387 Apr 15 11:09 cli.py
drwxr-xr-x   5 user_c042661f  staff    160 Apr 11 04:23 data
-rw-r--r--   1 user_c042661f  staff  26139 Apr 15 11:06 evaluation.py
-rw-r--r--   1 user_c042661f  staff  35930 Apr 15 11:06 execution.py
-rw-r--r--@  1 user_c042661f  staff   6569 Mar 31 03:41 execution_quality.py
-rw-r--r--   1 user_c042661f  staff  10449 Apr 15 11:06 execution_timeout.py
-rw-r--r--@  1 user_c042661f  staff   7686 Apr  8 02:54 flags.py
-rw-r--r--   1 user_c042661f  staff  85474 Apr 15 11:06 handlers.py
-rw-r--r--   1 user_c042661f  staff  37606 Apr 15 11:06 hermes_worker.py
-rw-r--r--   1 user_c042661f  staff   9981 Apr  4 01:44 key_pool.py
drwxr-xr-x@  9 user_c042661f  staff    288 Apr 11 04:22 loop
-rw-r--r--   1 user_c042661f  staff   6385 Mar 29 22:58 merge.py
-rw-r--r--@  1 user_c042661f  staff  10042 Apr  6 22:31 parallel_critique.py
-rw-r--r--   1 user_c042661f  staff  16079 Apr 11 04:24 parallel_review.py
drwxr-xr-x@ 12 user_c042661f  staff    384 Apr 15 11:06 prompts
-rw-r--r--   1 user_c042661f  staff  13631 Mar 25 21:39 quality.py
-rw-r--r--   1 user_c042661f  staff   9164 Apr 11 04:22 review_checks.py
-rw-r--r--   1 user_c042661f  staff  13175 Apr 11 04:25 review_mechanical.py
-rw-r--r--   1 user_c042661f  staff  21071 Apr 15 11:06 schemas.py
-rw-r--r--@  1 user_c042661f  staff  10273 Apr  9 23:17 step_edit.py
-rw-r--r--   1 user_c042661f  staff   8237 Apr 15 11:06 types.py
-rw-r--r--   1 user_c042661f  staff  60910 Apr 15 11:06 workers.py
[rerun: b2]
```

> AGENT

Let me continue exploring the subdirectories:

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/megaplan/prompts/"
}
```

> TOOL

tool_result Bash
```
total 240
drwxr-xr-x@ 12 user_c042661f  staff    384 Apr 15 11:06 .
drwxr-xr-x  32 user_c042661f  staff   1024 Apr 15 11:11 ..
-rw-r--r--@  1 user_c042661f  staff   6148 Apr 15 05:43 .DS_Store
-rw-r--r--   1 user_c042661f  staff   6885 Apr 15 11:06 __init__.py
drwxr-xr-x@ 29 user_c042661f  staff    928 Apr 15 11:07 __pycache__
-rw-r--r--   1 user_c042661f  staff   8785 Apr  6 07:11 _shared.py
-rw-r--r--   1 user_c042661f  staff  16501 Apr 10 22:53 critique.py
-rw-r--r--@  1 user_c042661f  staff  18972 Apr 10 23:09 execute.py
-rw-r--r--   1 user_c042661f  staff   5249 Apr 15 11:06 finalize.py
-rw-r--r--   1 user_c042661f  staff   7482 Apr 15 06:08 gate.py
-rw-r--r--   1 user_c042661f  staff  10773 Apr  9 19:12 planning.py
-rw-r--r--   1 user_c042661f  staff  23152 Apr 15 11:06 review.py
[rerun: b3]
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/megaplan/data/"
}
```

> TOOL

tool_result Bash
```
total 80
drwxr-xr-x   5 user_c042661f  staff    160 Apr 11 04:23 .
drwxr-xr-x  32 user_c042661f  staff   1024 Apr 15 11:11 ..
-rw-r--r--   1 user_c042661f  staff  17799 Apr 11 04:23 claude_subagent_appendix.md
-rw-r--r--   1 user_c042661f  staff   5153 Apr 11 04:23 codex_subagent_appendix.md
-rw-r--r--   1 user_c042661f  staff   9651 Apr 11 04:23 instructions.md
[rerun: b4]
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/megaplan/_core/"
}
```

> TOOL

tool_result Bash
```
total 136
drwxr-xr-x   9 user_c042661f  staff    288 Apr 13 05:06 .
drwxr-xr-x  32 user_c042661f  staff   1024 Apr 15 11:11 ..
-rw-r--r--   1 user_c042661f  staff   5220 Apr 10 22:53 __init__.py
drwxr-xr-x@ 20 user_c042661f  staff    640 Apr 13 05:06 __pycache__
-rw-r--r--@  1 user_c042661f  staff  14688 Apr  7 23:26 io.py
-rw-r--r--   1 user_c042661f  staff   9161 Apr 10 14:55 phase_runtime.py
-rw-r--r--   1 user_c042661f  staff   6313 Mar 31 14:31 registries.py
-rw-r--r--   1 user_c042661f  staff  13116 Apr 13 04:11 state.py
-rw-r--r--   1 user_c042661f  staff   8058 Apr 13 05:06 workflow.py
[rerun: b5]
```

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan -name \"schemas*\" -type f"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/__pycache__/schemas.cpython-312.pyc
/Users/user_c042661f/Documents/megaplan/megaplan/__pycache__/schemas.cpython-311.pyc
/Users/user_c042661f/Documents/megaplan/megaplan/__pycache__/schemas.cpython-314.pyc
/Users/user_c042661f/Documents/megaplan/megaplan/schemas.py
[rerun: b6]
```

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan -path \"*schemas*\" -name \"*.json\" -type f"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/.megaplan/schemas/loop_execute.json
/Users/user_c042661f/Documents/megaplan/.megaplan/schemas/revise.json
/Users/user_c042661f/Documents/megaplan/.megaplan/schemas/integrate.json
/Users/user_c042661f/Documents/megaplan/.megaplan/schemas/plan.json
/Users/user_c042661f/Documents/megaplan/.megaplan/schemas/loop_plan.json
/Users/user_c042661f/Documents/megaplan/.megaplan/schemas/prep.json
/Users/user_c042661f/Documents/megaplan/.megaplan/schemas/gate.json
/Users/user_c042661f/Documents/megaplan/.megaplan/schemas/clarify.json
/Users/user_c042661f/Documents/megaplan/.megaplan/schemas/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/schemas/research.json
/Users/user_c042661f/Documents/megaplan/.megaplan/schemas/critique.json
/Users/user_c042661f/Documents/megaplan/.megaplan/schemas/execution_doc.json
/Users/user_c042661f/Documents/megaplan/.megaplan/schemas/review.json
/Users/user_c042661f/Documents/megaplan/.megaplan/schemas/execution.json
/Users/user_c042661f/Documents/megaplan/.doubledip/schemas/integrate.json
/Users/user_c042661f/Documents/megaplan/.doubledip/schemas/plan.json
/Users/user_c042661f/Documents/megaplan/.doubledip/schemas/triage.json
/Users/user_c042661f/Documents/megaplan/.doubledip/schemas/critique.json
/Users/user_c042661f/Documents/megaplan/.doubledip/schemas/review.json
/Users/user_c042661f/Documents/megaplan/.doubledip/schemas/execution.json
[rerun: b7]
```

> AGENT

Now let me read the key files to understand the architecture:

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
7	version = "0.16.0"
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

> AGENT

Now let me examine the CLI file to understand command registration:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/cli.py",
  "offset": 1,
  "limit": 200
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
```

> AGENT

Let me continue reading the CLI file to find the argparse setup:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"add_subparsers\\|add_parser\\|def \" /Users/user_c042661f/Documents/megaplan/megaplan/cli.py | head -100"
}
```

> TOOL

tool_result Bash
```
72:def render_response(response: StepResponse, *, exit_code: int = 0) -> int:
77:def _resolve_error_plan_dir(root: Path | None, error: CliError) -> Path | None:
89:def _augment_plan_locked_error(
117:def error_response(error: CliError, *, root: Path | None = None) -> int:
132:def _parse_utc_timestamp(timestamp: str | None) -> datetime | None:
141:def _build_progress_payload(plan_dir: Path, state: dict[str, Any]) -> dict[str, Any]:
197:def _build_last_step(state: dict[str, Any]) -> dict[str, Any] | None:
213:def _build_active_step(active_step: Any, *, plan_dir: Path) -> dict[str, Any] | None:
282:def _build_status_payload(plan_dir: Path, state: dict[str, Any]) -> StepResponse:
341:def handle_status(root: Path, args: argparse.Namespace) -> StepResponse:
346:def handle_audit(root: Path, args: argparse.Namespace) -> StepResponse:
357:def handle_progress(root: Path, args: argparse.Namespace) -> StepResponse:
368:def handle_watch(root: Path, args: argparse.Namespace) -> StepResponse:
374:def _collect_megaplan_roots(root: Path, *, tree: bool = False, all_system: bool = False) -> list[Path]:
406:def handle_list(root: Path, args: argparse.Namespace) -> StepResponse:
494:def handle_debt(root: Path, args: argparse.Namespace) -> StepResponse:
575:def _canonical_instructions() -> str:
596:def bundled_agents_md() -> str:
600:def _subagent_appendix(filename: str) -> str:
613:def _claude_subagent_appendix() -> str:
617:def _codex_subagent_appendix() -> str:
621:def bundled_global_file(name: str) -> str:
641:def _install_owned_file(path: Path, content: str, *, force: bool = False) -> dict[str, bool | str]:
650:def handle_setup_global(force: bool = False, home: Path | None = None) -> StepResponse:
694:def handle_setup(args: argparse.Namespace) -> StepResponse:
711:def handle_config(args: argparse.Namespace) -> StepResponse:
802:def build_parser() -> argparse.ArgumentParser:
804:    subparsers = parser.add_subparsers(dest="command", required=True)
806:    setup_parser = subparsers.add_parser("setup", help="Install megaplan into agent configs (global by default)")
811:    init_parser = subparsers.add_parser("init")
822:    list_parser = subparsers.add_parser("list")
835:        step_parser = subparsers.add_parser(name)
839:        step_parser = subparsers.add_parser(name)
856:    config_parser = subparsers.add_parser("config", help="View or edit megaplan configuration")
857:    config_sub = config_parser.add_subparsers(dest="config_action", required=True)
858:    config_sub.add_parser("show")
859:    set_parser = config_sub.add_parser("set")
862:    config_sub.add_parser("reset")
864:    step_parser = subparsers.add_parser("step", help="Edit plan step sections without hand-editing markdown")
865:    step_subparsers = step_parser.add_subparsers(dest="step_action", required=True)
867:    step_add_parser = step_subparsers.add_parser("add", help="Insert a new step after an existing step")
868:    step_add_parser.add_argument("--plan")
869:    step_add_parser.add_argument("--after")
870:    step_add_parser.add_argument("description")
872:    step_remove_parser = step_subparsers.add_parser("remove", help="Remove a step and renumber the plan")
876:    step_move_parser = step_subparsers.add_parser("move", help="Move a step after another step and renumber")
881:    override_parser = subparsers.add_parser("override")
888:    debt_parser = subparsers.add_parser("debt", help="Inspect or manage persistent tech debt entries")
889:    debt_subparsers = debt_parser.add_subparsers(dest="debt_action", required=True)
891:    debt_list_parser = debt_subparsers.add_parser("list", help="List debt entries")
894:    debt_add_parser = debt_subparsers.add_parser("add", help="Add or increment a debt entry")
895:    debt_add_parser.add_argument("--subsystem", required=True)
896:    debt_add_parser.add_argument("--concern", required=True)
897:    debt_add_parser.add_argument("--flag-ids", default="")
898:    debt_add_parser.add_argument("--plan")
900:    debt_resolve_parser = debt_subparsers.add_parser("resolve", help="Resolve a debt entry")
904:    loop_init_parser = subparsers.add_parser("loop-init", help="Initialize a MegaLoop workflow")
923:    loop_run_parser = subparsers.add_parser("loop-run", help="Run an existing MegaLoop workflow")
937:    loop_status_parser = subparsers.add_parser("loop-status", help="Show MegaLoop state")
941:    loop_pause_parser = subparsers.add_parser("loop-pause", help="Pause a MegaLoop workflow")
980:def cli_entry() -> None:
984:def _find_megaplan_root(start: Path) -> Path:
1011:def _find_git_root(start: Path) -> Path | None:
1023:def main(argv: list[str] | None = None) -> int:
[rerun: b8]
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/cli.py",
  "offset": 802,
  "limit": 180
}
```

> TOOL

tool_result Read
```
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
949	    from megaplan.chain import build_chain_parser
950	    build_chain_parser(subparsers)
951	
952	    return parser
953	
954	
955	COMMAND_HANDLERS: dict[str, Callable[..., StepResponse]] = {
956	    "init": handle_init,
957	    "plan": handle_plan,
958	    "prep": handle_prep,
959	    "critique": handle_critique,
960	    "revise": handle_revise,
961	    "gate": handle_gate,
962	    "finalize": handle_finalize,
963	    "execute": handle_execute,
964	    "review": handle_review,
965	    "status": handle_status,
966	    "audit": handle_audit,
967	    "progress": handle_progress,
968	    "watch": handle_watch,
969	    "list": handle_list,
970	    "loop-init": handle_loop_init,
971	    "loop-run": handle_loop_run,
972	    "loop-status": handle_loop_status,
973	    "loop-pause": handle_loop_pause,
974	    "debt": handle_debt,
975	    "step": handle_step,
976	    "override": handle_override,
977	}
978	
979	
980	def cli_entry() -> None:
981	    sys.exit(main())
```

> AGENT

Now let me examine the handlers file:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 1,
  "limit": 150
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
```

> AGENT

Let me search for handle_* function definitions:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"^def handle_\" /Users/user_c042661f/Documents/megaplan/megaplan/handlers.py"
}
```

> TOOL

tool_result Bash
```
717:def handle_init(root: Path, args: argparse.Namespace) -> StepResponse:
794:def handle_plan(root: Path, args: argparse.Namespace) -> StepResponse:
840:def handle_prep(root: Path, args: argparse.Namespace) -> StepResponse:
861:def handle_critique(root: Path, args: argparse.Namespace) -> StepResponse:
994:def handle_revise(root: Path, args: argparse.Namespace) -> StepResponse:
1049:def handle_gate(root: Path, args: argparse.Namespace) -> StepResponse:
1308:def handle_finalize(root: Path, args: argparse.Namespace) -> StepResponse:
1337:def handle_execute(root: Path, args: argparse.Namespace) -> StepResponse:
1576:def handle_review(root: Path, args: argparse.Namespace) -> StepResponse:
2016:def handle_override(root: Path, args: argparse.Namespace) -> StepResponse:
[rerun: b9]
```

> AGENT

Now let me examine the workers file to find run_codex_step and run_claude_step:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"^def run_\\|^async def run_\" /Users/user_c042661f/Documents/megaplan/megaplan/workers.py"
}
```

> TOOL

tool_result Bash
```
94:def run_command(
1088:def run_claude_step(
1142:def run_codex_step(
1477:def run_step_with_worker(
[rerun: b10]
```

> AGENT

Excellent! Now let me read the worker functions:

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
  "limit": 150
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
1237	            print(
1238	                f"[megaplan] Codex session {session['id']} has no rollout "
1239	                f"(container restart or session wipe); retrying {step} with a fresh session",
1240	                flush=True,
1241	            )
1242	            # Drop the stale session id so later phases don't also try to resume it.
1243	            state["sessions"].pop(session_key, None)
1244	            return run_codex_step(
1245	                step,
1246	                state,
1247	                plan_dir,
1248	                root=root,
1249	                persistent=persistent,
1250	                fresh=True,
1251	                json_trace=json_trace,
1252	                prompt_override=prompt_override,
1253	                prompt_kwargs=prompt_kwargs,
1254	            )
1255	        if error.code == "worker_timeout":
1256	            recovered_payload = _recover_codex_payload(
1257	                step,
1258	                plan_dir=plan_dir,
1259	                output_path=output_path,
1260	                raw=str(error.extra.get("raw_output", "")),
1261	            )
1262	            if recovered_payload is not None:
1263	                timeout_session_id = session.get("id") if persistent else None
1264	                if timeout_session_id is None:
1265	                    timeout_session_id = extract_session_id(str(error.extra.get("raw_output", "")))
1266	                return WorkerResult(
1267	                    payload=recovered_payload,
1268	                    raw_output=str(error.extra.get("raw_output", "")),
1269	                    duration_ms=0,
1270	                    cost_usd=0.0,
1271	                    session_id=timeout_session_id,
1272	                    trace_output=str(error.extra.get("raw_output", "")) if json_trace else None,
1273	                )
1274	            timeout_session_id = session.get("id") if persistent else None
1275	            if timeout_session_id is None:
1276	                timeout_session_id = extract_session_id(error.extra.get("raw_output", ""))
1277	            if timeout_session_id is not None:
1278	                error.extra["session_id"] = timeout_session_id
1279	            diagnosed_code, diagnosed_message = _diagnose_codex_failure(
1280	                str(error.extra.get("raw_output", "")),
1281	                124,
1282	            )
1283	            if diagnosed_code == "connection_error":
1284	                raise CliError(
1285	                    diagnosed_code,
1286	                    diagnosed_message,
1287	                    extra=error.extra,
1288	                    valid_next=error.valid_next,
1289	                    exit_code=error.exit_code,
1290	                ) from error
1291	            raise CliError(
```

> AGENT

Now let me look at the state.py to understand SessionDB:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py"
}
```

> TOOL

tool_result Read
```
1	"""Plan state management — load, save, history, sessions, failure recording."""
2	
3	from __future__ import annotations
4	
5	import uuid
6	from contextlib import contextmanager
7	from datetime import datetime, timezone
8	from pathlib import Path
9	from typing import TYPE_CHECKING, Iterator
10	
11	import fcntl
12	
13	from megaplan.types import (
14	    ActiveStep,
15	    CliError,
16	    HistoryEntry,
17	    PlanState,
18	    PlanVersionRecord,
19	    TERMINAL_STATES,
20	)
21	from .phase_runtime import DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS, phase_stale_seconds
22	
23	from .io import (
24	    atomic_write_json,
25	    atomic_write_text,
26	    current_iteration_raw_artifact,
27	    now_utc,
28	    plans_root,
29	    read_json,
30	)
31	
32	if TYPE_CHECKING:
33	    from megaplan.workers import WorkerResult
34	
35	
36	DEFAULT_ACTIVE_STEP_STALE_SECONDS = DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS
37	
38	
39	# ---------------------------------------------------------------------------
40	# Plan resolution
41	# ---------------------------------------------------------------------------
42	
43	def active_plan_dirs(root: Path) -> list[Path]:
44	    if not plans_root(root).exists():
45	        return []
46	    directories: list[Path] = []
47	    for child in plans_root(root).iterdir():
48	        if child.is_dir() and (child / "state.json").exists():
49	            directories.append(child)
50	    return sorted(directories)
51	
52	
53	def resolve_plan_dir(root: Path, requested_name: str | None) -> Path:
54	    plan_dirs = active_plan_dirs(root)
55	    if requested_name:
56	        plan_dir = plans_root(root) / requested_name
57	        if (plan_dir / "state.json").exists():
58	            return plan_dir
59	        # Walk up parent directories — plan may live in an ancestor's .megaplan/
60	        current = root.resolve().parent
61	        while True:
62	            candidate = plans_root(current) / requested_name
63	            if (candidate / "state.json").exists():
64	                return candidate
65	            parent = current.parent
66	            if parent == current:
67	                break
68	            current = parent
69	        # Walk down child directories — plan may live in a subdirectory's .megaplan/
70	        for megaplan_dir in sorted(root.resolve().rglob(".megaplan")):
71	            if megaplan_dir.is_dir():
72	                candidate = megaplan_dir / "plans" / requested_name
73	                if (candidate / "state.json").exists():
74	                    return candidate
75	        raise CliError("missing_plan", f"Plan '{requested_name}' does not exist")
76	    if not plan_dirs:
77	        raise CliError("missing_plan", "No plans found. Run init first.")
78	    active = []
79	    for plan_dir in plan_dirs:
80	        state = read_json(plan_dir / "state.json")
81	        if state.get("current_state") not in TERMINAL_STATES:
82	            active.append(plan_dir)
83	    if len(active) == 1:
84	        return active[0]
85	    if len(plan_dirs) == 1:
86	        return plan_dirs[0]
87	    names = [path.name for path in active or plan_dirs]
88	    raise CliError(
89	        "ambiguous_plan",
90	        "Multiple plans exist; pass --plan explicitly",
91	        extra={"plans": names},
92	    )
93	
94	
95	def load_plan(root: Path, requested_name: str | None) -> tuple[Path, PlanState]:
96	    plan_dir = resolve_plan_dir(root, requested_name)
97	    return load_plan_from_dir(plan_dir)
98	
99	
100	def load_plan_from_dir(plan_dir: Path) -> tuple[Path, PlanState]:
101	    state = read_json(plan_dir / "state.json")
102	    migrated = False
103	    if state.get("current_state") == "clarified":
104	        state["current_state"] = "initialized"
105	        migrated = True
106	    elif state.get("current_state") == "evaluated":
107	        state["current_state"] = "critiqued"
108	        state["last_gate"] = {}
109	        migrated = True
110	    if "last_evaluation" in state:
111	        del state["last_evaluation"]
112	        migrated = True
113	    if "last_gate" not in state:
114	        state["last_gate"] = {}
115	        migrated = True
116	    if migrated:
117	        atomic_write_json(plan_dir / "state.json", state)
118	    return plan_dir, state
119	
120	
121	def _parse_utc_timestamp(timestamp: str | None) -> datetime | None:
122	    if not isinstance(timestamp, str) or not timestamp:
123	        return None
124	    try:
125	        return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
126	    except ValueError:
127	        return None
128	
129	
130	def active_step_is_stale(
131	    active_step: ActiveStep | None,
132	    *,
133	    configured_timeout_seconds: int = DEFAULT_ACTIVE_STEP_STALE_SECONDS,
134	) -> bool:
135	    if not isinstance(active_step, dict):
136	        return False
137	    step = active_step.get("step")
138	    if not isinstance(step, str) or not step:
139	        return False
140	    started_at = _parse_utc_timestamp(active_step.get("started_at"))
141	    if started_at is None:
142	        return False
143	    age_seconds = max(0, int((datetime.now(timezone.utc) - started_at).total_seconds()))
144	    return age_seconds >= phase_stale_seconds(
145	        step,
146	        configured_timeout_seconds=configured_timeout_seconds,
147	    )
148	
149	
150	def plan_lock_path(plan_dir: Path) -> Path:
151	    return plan_dir / ".plan.lock"
152	
153	
154	def plan_lock_is_held(plan_dir: Path) -> bool:
155	    lock_path = plan_lock_path(plan_dir)
156	    lock_path.parent.mkdir(parents=True, exist_ok=True)
157	    with lock_path.open("a+", encoding="utf-8") as handle:
158	        try:
159	            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
160	        except BlockingIOError:
161	            return True
162	        finally:
163	            try:
164	                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
165	            except OSError:
166	                pass
167	    return False
168	
169	
170	def _build_plan_locked_details(plan_dir: Path, *, step: str) -> dict[str, object]:
171	    state_path = plan_dir / "state.json"
172	    details: dict[str, object] = {"plan": plan_dir.name, "step": step}
173	    if not state_path.exists():
174	        return details
175	    try:
176	        state = read_json(state_path)
177	    except Exception:
178	        return details
179	    if not isinstance(state, dict):
180	        return details
181	    active_step = state.get("active_step")
182	    if isinstance(active_step, dict):
183	        details["active_step"] = dict(active_step)
184	    return details
185	
186	
187	@contextmanager
188	def plan_lock(plan_dir: Path, *, step: str) -> Iterator[None]:
189	    lock_path = plan_lock_path(plan_dir)
190	    lock_path.parent.mkdir(parents=True, exist_ok=True)
191	    with lock_path.open("a+", encoding="utf-8") as handle:
192	        try:
193	            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
194	        except BlockingIOError as exc:
195	            details = _build_plan_locked_details(plan_dir, step=step)
196	            active_step = details.get("active_step")
197	            if isinstance(active_step, dict):
198	                message = (
199	                    f"Cannot run '{step}' because plan '{plan_dir.name}' already has an active "
200	                    f"'{active_step.get('step')}' step via {active_step.get('agent')}."
201	                )
202	            else:
203	                message = f"Cannot run '{step}' because plan '{plan_dir.name}' is locked by another process."
204	            raise CliError("plan_locked", message, extra=details) from exc
205	        try:
206	            yield
207	        finally:
208	            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
209	
210	
211	@contextmanager
212	def load_plan_locked(root: Path, requested_name: str | None, *, step: str) -> Iterator[tuple[Path, PlanState]]:
213	    plan_dir = resolve_plan_dir(root, requested_name)
214	    with plan_lock(plan_dir, step=step):
215	        yield load_plan_from_dir(plan_dir)
216	
217	
218	def save_state(plan_dir: Path, state: PlanState) -> None:
219	    atomic_write_json(plan_dir / "state.json", state)
220	
221	
222	def apply_session_update(
223	    state: PlanState,
224	    step: str,
225	    agent: str,
226	    session_id: str | None,
227	    *,
228	    mode: str,
229	    refreshed: bool,
230	) -> None:
231	    from megaplan.workers import update_session_state
232	
233	    result = update_session_state(
234	        step,
235	        agent,
236	        session_id,
237	        mode=mode,
238	        refreshed=refreshed,
239	        existing_sessions=state["sessions"],
240	    )
241	    if result is not None:
242	        key, entry = result
243	        state["sessions"][key] = entry
244	
245	
246	def set_active_step(
247	    state: PlanState,
248	    *,
249	    step: str,
250	    agent: str,
251	    mode: str,
252	    model: str | None = None,
253	    run_id: str | None = None,
254	) -> str:
255	    resolved_run_id = run_id or str(uuid.uuid4())
256	    active_step: ActiveStep = {
257	        "step": step,
258	        "agent": agent,
259	        "mode": mode,
260	        "run_id": resolved_run_id,
261	        "started_at": now_utc(),
262	    }
263	    if model:
264	        active_step["model"] = model
265	    if mode == "persistent":
266	        from megaplan.workers import session_key_for
267	
268	        session = state.get("sessions", {}).get(session_key_for(step, agent, model), {})
269	        session_id = session.get("id")
270	        if isinstance(session_id, str) and session_id:
271	            active_step["session_id"] = session_id
272	    state["active_step"] = active_step
273	    return resolved_run_id
274	
275	
276	def clear_active_step(state: PlanState, *, run_id: str | None = None) -> None:
277	    active_step = state.get("active_step")
278	    if run_id is not None and isinstance(active_step, dict) and active_step.get("run_id") != run_id:
279	        return
280	    state.pop("active_step", None)
281	
282	
283	# ---------------------------------------------------------------------------
284	# History helpers
285	# ---------------------------------------------------------------------------
286	
287	def append_history(state: PlanState, entry: HistoryEntry) -> None:
288	    state["history"].append(entry)
289	    state["meta"].setdefault("total_cost_usd", 0.0)
290	    state["meta"]["total_cost_usd"] = round(
291	        float(state["meta"]["total_cost_usd"]) + float(entry.get("cost_usd", 0.0)),
292	        6,
293	    )
294	
295	
296	def make_history_entry(
297	    step: str,
298	    *,
299	    duration_ms: int,
300	    cost_usd: float,
301	    result: str,
302	    worker: WorkerResult | None = None,
303	    agent: str | None = None,
304	    mode: str | None = None,
305	    output_file: str | None = None,
306	    artifact_hash: str | None = None,
307	    finalize_hash: str | None = None,
308	    raw_output_file: str | None = None,
309	    message: str | None = None,
310	    flags_count: int | None = None,
311	    flags_addressed: list[str] | None = None,
312	    recommendation: str | None = None,
313	    approval_mode: str | None = None,
314	    environment: dict[str, bool] | None = None,
315	    prompt_tokens: int = 0,
316	    completion_tokens: int = 0,
317	    total_tokens: int = 0,
318	) -> HistoryEntry:
319	    entry: HistoryEntry = {
320	        "step": step,
321	        "timestamp": now_utc(),
322	        "duration_ms": duration_ms,
323	        "cost_usd": cost_usd,
324	        "result": result,
325	    }
326	    if total_tokens > 0:
327	        entry["prompt_tokens"] = prompt_tokens
328	        entry["completion_tokens"] = completion_tokens
329	        entry["total_tokens"] = total_tokens
330	    if worker is not None and agent is not None and mode is not None:
331	        entry["session_mode"] = mode
332	        entry["session_id"] = worker.session_id
333	        entry["agent"] = agent
334	    if output_file is not None:
335	        entry["output_file"] = output_file
336	    if artifact_hash is not None:
337	        entry["artifact_hash"] = artifact_hash
338	    if finalize_hash is not None:
339	        entry["finalize_hash"] = finalize_hash
340	    if raw_output_file is not None:
341	        entry["raw_output_file"] = raw_output_file
342	    if message is not None:
343	        entry["message"] = message
344	    if flags_count is not None:
345	        entry["flags_count"] = flags_count
346	    if flags_addressed is not None:
347	        entry["flags_addressed"] = flags_addressed
348	    if recommendation is not None:
349	        entry["recommendation"] = recommendation
350	    if approval_mode is not None:
351	        entry["approval_mode"] = approval_mode
352	    if environment is not None:
353	        entry["environment"] = environment
354	    return entry
355	
356	
357	def store_raw_worker_output(plan_dir: Path, step: str, iteration: int, content: str) -> str:
358	    filename = current_iteration_raw_artifact(plan_dir, step, iteration).name
359	    atomic_write_text(plan_dir / filename, content)
360	    return filename
361	
362	
363	def record_step_failure(
364	    plan_dir: Path,
365	    state: PlanState,
366	    *,
367	    step: str,
368	    iteration: int,
369	    error: CliError,
370	    duration_ms: int = 0,
371	) -> None:
372	    raw_output = str(error.extra.get("raw_output") or error.message)
373	    raw_name = store_raw_worker_output(plan_dir, step, iteration, raw_output)
374	    append_history(
375	        state,
376	        make_history_entry(
377	            step,
378	            duration_ms=duration_ms,
379	            cost_usd=0.0,
380	            result="error",
381	            raw_output_file=raw_name,
382	            message=error.message,
383	        ),
384	    )
385	    save_state(plan_dir, state)
386	
387	
388	# ---------------------------------------------------------------------------
389	# Plan version helpers
390	# ---------------------------------------------------------------------------
391	
392	def latest_plan_record(state: PlanState) -> PlanVersionRecord:
393	    plan_versions = state["plan_versions"]
394	    if not plan_versions:
395	        raise CliError("missing_plan_version", "No plan version exists yet")
396	    return plan_versions[-1]
397	
398	
399	def latest_plan_path(plan_dir: Path, state: PlanState) -> Path:
400	    return plan_dir / latest_plan_record(state)["file"]
401	
402	
403	def latest_plan_meta_path(plan_dir: Path, state: PlanState) -> Path:
404	    record = latest_plan_record(state)
405	    meta_name = record["file"].replace(".md", ".meta.json")
406	    return plan_dir / meta_name
407
```

> AGENT

Now let me check the prompt files and then schemas:

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/megaplan/prompts/*.py"
}
```

> TOOL

tool_result Bash
```
This command requires approval
```

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan/megaplan/prompts -name \"*.py\" -type f"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/execute.py
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/__init__.py
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/finalize.py
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/_shared.py
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/review.py
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/gate.py
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/planning.py
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/critique.py
[rerun: b11]
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

> AGENT

Now let me examine schemas.py:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/schemas.py",
  "offset": 1,
  "limit": 200
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
```

> AGENT

Let me get a sample JSON schema:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/.megaplan/schemas/plan.json"
}
```

> TOOL

tool_result Read
```
1	{
2	  "type": "object",
3	  "properties": {
4	    "plan": {
5	      "type": "string"
6	    },
7	    "questions": {
8	      "type": "array",
9	      "items": {
10	        "type": "string"
11	      }
12	    },
13	    "success_criteria": {
14	      "type": "array",
15	      "items": {
16	        "type": "object",
17	        "properties": {
18	          "criterion": {
19	            "type": "string"
20	          },
21	          "priority": {
22	            "type": "string",
23	            "enum": [
24	              "must",
25	              "should",
26	              "info"
27	            ]
28	          }
29	        },
30	        "required": [
31	          "criterion",
32	          "priority"
33	        ],
34	        "additionalProperties": false
35	      }
36	    },
37	    "assumptions": {
38	      "type": "array",
39	      "items": {
40	        "type": "string"
41	      }
42	    }
43	  },
44	  "required": [
45	    "plan",
46	    "questions",
47	    "success_criteria",
48	    "assumptions"
49	  ],
50	  "additionalProperties": false
51	}
52
```

> AGENT

Now let me check how phases wire their workers. Let me look at one of the existing phase handler implementations:

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

> AGENT

Now let me look at the _run_worker function to see how it dispatches:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"^def _run_worker\" /Users/user_c042661f/Documents/megaplan/megaplan/handlers.py"
}
```

> TOOL

tool_result Bash
```
167:def _run_worker(
[rerun: b12]
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 167,
  "limit": 150
}
```

> TOOL

tool_result Read
```
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
```

> AGENT

Now let me check the run_step_with_worker function:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/workers.py",
  "offset": 1477,
  "limit": 120
}
```

> TOOL

tool_result Read
```
1477	def run_step_with_worker(
1478	    step: str,
1479	    state: PlanState,
1480	    plan_dir: Path,
1481	    args: argparse.Namespace,
1482	    *,
1483	    root: Path,
1484	    resolved: tuple[str, str, bool, str | None] | None = None,
1485	    prompt_override: str | None = None,
1486	    prompt_kwargs: dict[str, Any] | None = None,
1487	) -> tuple[WorkerResult, str, str, bool]:
1488	    agent, mode, refreshed, model = resolved or resolve_agent_mode(step, args)
1489	    effective_refreshed = refreshed
1490	    explicit_agent = _agent_requested_explicitly(step, args)
1491	    attempted_agents: set[str] = set()
1492	    while True:
1493	        attempted_agents.add(agent)
1494	        try:
1495	            if agent == "hermes":
1496	                # Deferred import to avoid circular import (hermes_worker imports from workers)
1497	                from megaplan.hermes_worker import run_hermes_step
1498	                worker = run_hermes_step(
1499	                    step,
1500	                    state,
1501	                    plan_dir,
1502	                    root=root,
1503	                    fresh=effective_refreshed,
1504	                    model=model,
1505	                    prompt_override=prompt_override,
1506	                )
1507	            elif agent == "claude":
1508	                worker = run_claude_step(
1509	                    step,
1510	                    state,
1511	                    plan_dir,
1512	                    root=root,
1513	                    fresh=effective_refreshed,
1514	                    prompt_override=prompt_override,
1515	                    prompt_kwargs=prompt_kwargs,
1516	                )
1517	            else:
1518	                attempted_retry = False
1519	                while True:
1520	                    try:
1521	                        worker = run_codex_step(
1522	                            step,
1523	                            state,
1524	                            plan_dir,
1525	                            root=root,
1526	                            persistent=(mode == "persistent"),
1527	                            fresh=effective_refreshed,
1528	                            json_trace=(step == "execute"),
1529	                            prompt_override=prompt_override,
1530	                            prompt_kwargs=prompt_kwargs,
1531	                        )
1532	                        break
1533	                    except CliError as error:
1534	                        session_id = error.extra.get("session_id")
1535	                        if (
1536	                            attempted_retry
1537	                            or step in _EXECUTE_STEPS
1538	                            or error.code not in {"worker_timeout", "connection_error"}
1539	                        ):
1540	                            raise
1541	                        attempted_retry = True
1542	                        if mode == "persistent" and isinstance(session_id, str) and session_id:
1543	                            apply_session_update(
1544	                                state,
1545	                                step,
1546	                                agent,
1547	                                session_id,
1548	                                mode=mode,
1549	                                refreshed=effective_refreshed,
1550	                            )
1551	                            effective_refreshed = False
1552	                        continue
1553	            return worker, agent, mode, effective_refreshed
1554	        except CliError as error:
1555	            if explicit_agent or error.code not in {"auth_error", "connection_error"}:
1556	                raise
1557	            fallback_candidates = [
1558	                candidate
1559	                for candidate in _runtime_fallback_candidates(agent)
1560	                if candidate not in attempted_agents
1561	            ]
1562	            if not fallback_candidates:
1563	                raise
1564	            fallback_agent = fallback_candidates[0]
1565	            args._agent_fallback = {
1566	                "requested": agent,
1567	                "resolved": fallback_agent,
1568	                "reason": f"{agent} runtime unhealthy: {error.code}",
1569	            }
1570	            agent = fallback_agent
1571	            model = None
1572	            effective_refreshed = True
1573
```

> AGENT

Now let me look at a few more schema examples and understand existing phases better:

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/.megaplan/schemas/ | head -20"
}
```

> TOOL

tool_result Bash
```
total 120
drwxr-xr-x@ 16 user_c042661f  staff   512 Apr 15 12:42 .
drwxr-xr-x@  7 user_c042661f  staff   224 Apr 10 22:58 ..
-rw-------@  1 user_c042661f  staff   641 Mar 23 01:51 clarify.json
-rw-------@  1 user_c042661f  staff  2235 Apr 15 12:42 critique.json
-rw-------@  1 user_c042661f  staff  1887 Apr 15 12:42 execution.json
-rw-------@  1 user_c042661f  staff  1735 Apr 15 10:53 execution_doc.json
-rw-------@  1 user_c042661f  staff  3901 Apr 15 12:42 finalize.json
-rw-------@  1 user_c042661f  staff  2279 Apr 15 12:42 gate.json
-rw-------@  1 user_c042661f  staff   726 Mar 23 01:51 integrate.json
-rw-------@  1 user_c042661f  staff   573 Apr 15 12:42 loop_execute.json
-rw-------@  1 user_c042661f  staff   342 Apr 15 12:42 loop_plan.json
-rw-------@  1 user_c042661f  staff   907 Apr 15 12:42 plan.json
-rw-------@  1 user_c042661f  staff  2175 Apr 15 12:42 prep.json
-rw-------@  1 user_c042661f  staff   782 Apr  1 20:49 research.json
-rw-------@  1 user_c042661f  staff  5894 Apr 15 12:42 review.json
-rw-------@  1 user_c042661f  staff  1113 Apr 15 12:42 revise.json
[rerun: b13]
```

> AGENT

Let me check the workflow/state file to understand how phases transition:

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

> AGENT

Perfect! Now let me look at one more example handler to see the pattern, and examine the critique phase which seems more complex:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 861,
  "limit": 200
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
1001	        validate_payload("revise", payload)
1002	        version = state["iteration"] + 1
1003	        plan_text = payload["plan"].rstrip() + "\n"
1004	        delta = compute_plan_delta_percent(previous_plan, plan_text)
1005	        plan_filename, meta_filename, meta = _write_plan_version(
1006	            plan_dir=plan_dir, state=state, step="revise", version=version,
1007	            worker=worker, plan_filename=f"plan_v{version}.md", plan_text=plan_text,
1008	            meta_fields={
1009	                "changes_summary": payload["changes_summary"],
1010	                "flags_addressed": payload["flags_addressed"],
1011	                "questions": payload.get("questions", []),
1012	                "success_criteria": payload.get("success_criteria", []),
1013	                "assumptions": payload.get("assumptions", []),
1014	                "delta_from_previous_percent": delta,
1015	            },
1016	        )
1017	        state["iteration"], state["current_state"] = version, revise_transition.next_state
1018	        state["meta"].pop("user_approved_gate", None)
1019	        if has_gate:
1020	            state["last_gate"] = {}
1021	        state["plan_versions"].append({
1022	            "version": version, "file": plan_filename,
1023	            "hash": meta["hash"], "timestamp": meta["timestamp"],
1024	        })
1025	        _append_to_meta(state, "plan_deltas", delta)
1026	        update_flags_after_revise(plan_dir, payload["flags_addressed"], plan_file=plan_filename, summary=payload["changes_summary"])
1027	        next_step = _next_progress_step(state)
1028	        remaining = _remaining_significant_flags(plan_dir)
1029	        return _finish_step(
1030	            plan_dir, state, args,
1031	            step="revise",
1032	            worker=worker, agent=agent, mode=mode, refreshed=refreshed,
1033	            summary=f"Updated plan to v{version}; addressed {len(payload['flags_addressed'])} flags.",
1034	            artifacts=[plan_filename, meta_filename, "faults.json"],
1035	            output_file=plan_filename,
1036	            artifact_hash=meta["hash"],
1037	            next_step=next_step,
1038	            response_fields={
1039	                "iteration": version,
1040	                "changes_summary": payload["changes_summary"],
1041	                "flags_addressed": payload["flags_addressed"],
1042	                "flags_remaining": remaining,
1043	                "plan_delta_percent": delta,
1044	            },
1045	            history_fields={"flags_addressed": payload["flags_addressed"]},
1046	        )
1047	
1048	
1049	def handle_gate(root: Path, args: argparse.Namespace) -> StepResponse:
1050	    with load_plan_locked(root, args.plan, step="gate") as (plan_dir, state):
1051	        require_state(state, "gate", {STATE_CRITIQUED})
1052	        iteration = state["iteration"]
1053	        gate_signals, signals_filename, signals_artifact = _build_gate_signals_artifact(plan_dir, state, iteration=iteration, root=root)
1054	        resolved = resolve_agent_mode("gate", args)
1055	        worker, agent, mode, refreshed = _run_worker(
1056	            "gate",
1057	            state,
1058	            plan_dir,
1059	            args,
1060	            root=root,
```

> AGENT

Now let me look at the io.py to see database operations:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/io.py",
  "offset": 1,
  "limit": 150
}
```

> TOOL

tool_result Read
```
1	"""Atomic I/O, JSON helpers, path resolution, and config management."""
2	
3	from __future__ import annotations
4	
5	import hashlib
6	import json
7	import os
8	import re
9	import tempfile
10	from pathlib import Path
11	from typing import Any
12	
13	from megaplan.schemas import SCHEMAS, strict_schema
14	from megaplan.types import KNOWN_AGENTS
15	
16	
17	# ---------------------------------------------------------------------------
18	# Pure utilities
19	# ---------------------------------------------------------------------------
20	
21	def now_utc() -> str:
22	    from datetime import datetime, timezone
23	
24	    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
25	
26	
27	def slugify(text: str, max_length: int = 30) -> str:
28	    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
29	    if len(slug) <= max_length:
30	        return slug or "plan"
31	    truncated = slug[:max_length]
32	    last_hyphen = truncated.rfind("-")
33	    if last_hyphen > 10:
34	        truncated = truncated[:last_hyphen]
35	    return truncated or "plan"
36	
37	
38	def json_dump(obj: Any) -> str:
39	    return json.dumps(obj, indent=2, sort_keys=False) + "\n"
40	
41	
42	def normalize_text(text: str) -> str:
43	    return re.sub(r"\s+", " ", text.strip().lower())
44	
45	
46	def sha256_text(content: str) -> str:
47	    return "sha256:" + hashlib.sha256(content.encode("utf-8")).hexdigest()
48	
49	
50	def sha256_file(path: Path) -> str:
51	    return sha256_text(path.read_text(encoding="utf-8"))
52	
53	
54	def compute_task_batches(
55	    tasks: list[dict[str, Any]],
56	    completed_ids: set[str] | None = None,
57	) -> list[list[str]]:
58	    completed = set(completed_ids or set())
59	    if not tasks:
60	        return []
61	
62	    task_ids = [task["id"] for task in tasks]
63	    task_id_set = set(task_ids)
64	    remaining: dict[str, set[str]] = {}
65	    order_index = {task_id: index for index, task_id in enumerate(task_ids)}
66	
67	    for task in tasks:
68	        task_id = task["id"]
69	        deps = task.get("depends_on", [])
70	        if not isinstance(deps, list):
71	            deps = []
72	        normalized_deps: set[str] = set()
73	        for dep in deps:
74	            if dep in task_id_set:
75	                normalized_deps.add(dep)
76	                continue
77	            if dep in completed:
78	                continue
79	            raise ValueError(f"Unknown dependency ID '{dep}' for task '{task_id}'")
80	        remaining[task_id] = normalized_deps
81	
82	    batches: list[list[str]] = []
83	    satisfied = set(completed)
84	    unscheduled = set(task_ids)
85	
86	    while unscheduled:
87	        ready = [
88	            task_id
89	            for task_id in unscheduled
90	            if remaining[task_id].issubset(satisfied)
91	        ]
92	        ready.sort([REDACTED])
93	        if not ready:
94	            cycle_ids = sorted(unscheduled, [REDACTED])
95	            raise ValueError("Cyclic dependency graph detected among tasks: " + ", ".join(cycle_ids))
96	        batches.append(ready)
97	        satisfied.update(ready)
98	        unscheduled.difference_update(ready)
99	
100	    return batches
101	
102	
103	def compute_global_batches(finalize_data: dict[str, Any]) -> list[list[str]]:
104	    tasks = finalize_data.get("tasks", [])
105	    return compute_task_batches(tasks)
106	
107	
108	# ---------------------------------------------------------------------------
109	# Atomic I/O
110	# ---------------------------------------------------------------------------
111	
112	def atomic_write_text(path: Path, content: str) -> None:
113	    path.parent.mkdir(parents=True, exist_ok=True)
114	    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
115	        handle.write(content)
116	        temp_path = Path(handle.name)
117	    temp_path.replace(path)
118	
119	
120	def atomic_write_json(path: Path, data: Any) -> None:
121	    atomic_write_text(path, json_dump(data))
122	
123	
124	def read_json(path: Path) -> Any:
125	    return json.loads(path.read_text(encoding="utf-8"))
126	
127	
128	def load_finalize_snapshot(plan_dir: Path) -> dict[str, Any]:
129	    return read_json(plan_dir / "finalize_snapshot.json")
130	
131	
132	def render_final_md(finalize_data: dict[str, Any], *, phase: str = "finalize") -> str:
133	    show_execution_gaps = phase in ("execute", "review")
134	    show_review_gaps = phase == "review"
135	    tasks = finalize_data.get("tasks", [])
136	    sense_checks = finalize_data.get("sense_checks", [])
137	
138	    lines = ["# Execution Checklist", ""]
139	    gap_counts: dict[str, int] = {}
140	    for task in tasks:
141	        status = task.get("status")
142	        checkbox = "[x]" if status == "done" else "[ ]"
143	        status_suffix = " (skipped)" if status == "skipped" else ""
144	        lines.append(f"- {checkbox} **{task['id']}:** {task['description']}{status_suffix}")
145	        depends_on = task.get("depends_on", [])
146	        if depends_on:
147	            lines.append(f"  Depends on: {', '.join(depends_on)}")
148	        executor_notes = task.get("executor_notes", "")
149	        if executor_notes.strip():
150	            lines.append(f"  Executor notes: {executor_notes}")
```

> AGENT

Now let me check the init file to see what's exported from _core:

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

> AGENT

Perfect! Now let me compile all this into a comprehensive report. Let me also check one more execution schema to be thorough:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/.megaplan/schemas/execution.json"
}
```

> TOOL

tool_result Read
```
1	{
2	  "type": "object",
3	  "properties": {
4	    "output": {
5	      "type": "string"
6	    },
7	    "files_changed": {
8	      "type": "array",
9	      "items": {
10	        "type": "string"
11	      }
12	    },
13	    "commands_run": {
14	      "type": "array",
15	      "items": {
16	        "type": "string"
17	      }
18	    },
19	    "deviations": {
20	      "type": "array",
21	      "items": {
22	        "type": "string"
23	      }
24	    },
25	    "task_updates": {
26	      "type": "array",
27	      "items": {
28	        "type": "object",
29	        "properties": {
30	          "task_id": {
31	            "type": "string"
32	          },
33	          "status": {
34	            "type": "string",
35	            "enum": [
36	              "done",
37	              "skipped"
38	            ]
39	          },
40	          "executor_notes": {
41	            "type": "string"
42	          },
43	          "files_changed": {
44	            "type": "array",
45	            "items": {
46	              "type": "string"
47	            }
48	          },
49	          "commands_run": {
50	            "type": "array",
51	            "items": {
52	              "type": "string"
53	            }
54	          }
55	        },
56	        "required": [
57	          "task_id",
58	          "status",
59	          "executor_notes",
60	          "files_changed",
61	          "commands_run"
62	        ],
63	        "additionalProperties": false
64	      }
65	    },
66	    "sense_check_acknowledgments": {
67	      "type": "array",
68	      "items": {
69	        "type": "object",
70	        "properties": {
71	          "sense_check_id": {
72	            "type": "string"
73	          },
74	          "executor_note": {
75	            "type": "string"
76	          }
77	        },
78	        "required": [
79	          "sense_check_id",
80	          "executor_note"
81	        ],
82	        "additionalProperties": false
83	      }
84	    }
85	  },
86	  "required": [
87	    "output",
88	    "files_changed",
89	    "commands_run",
90	    "deviations",
91	    "task_updates",
92	    "sense_check_acknowledgments"
93	  ],
94	  "additionalProperties": false
95	}
96
```

> AGENT

Perfect! Now I have all the information I need. Let me compile a comprehensive report.

## Megaplan Project Architecture — Comprehensive Exploration Report

### 1. OVERALL FILE STRUCTURE

**Top-level directories:**
```
/Users/user_c042661f/Documents/megaplan/
├── megaplan/                  # Main package (v0.16.0)
├── tests/                     # Test suite
├── .megaplan/                 # Runtime state directory
├── .git/                       # Git repository
├── pyproject.toml             # Package metadata
├── README.md, CHANGELOG.md    # Documentation
└── Various idea/planning docs
```

**megaplan/ subdirectories:**
```
megaplan/
├── __init__.py                # Package initialization
├── __main__.py                # CLI entry
├── cli.py                     # Command-line interface (43KB)
├── handlers.py                # Phase handlers (85KB) — core orchestration
├── workers.py                 # Worker dispatch (60KB) — Claude/Codex/Hermes runners
├── types.py                   # Type definitions & constants
├── schemas.py                 # JSON schema definitions
├── prompts/                   # Prompt templates for each phase
│   ├── __init__.py            # Prompt dispatch tables
│   ├── _shared.py
│   ├── planning.py
│   ├── critique.py
│   ├── execute.py
│   ├── finalize.py
│   ├── gate.py
│   └── review.py
├── _core/                     # Core infrastructure
│   ├── __init__.py            # Re-exports all core APIs
│   ├── state.py               # Plan state, locks, history, sessions
│   ├── io.py                  # Atomic I/O, config, paths
│   ├── workflow.py            # State machine & transitions
│   ├── registries.py          # Flag & debt registries
│   └── phase_runtime.py       # Timeout policy
├── execution.py               # Execution orchestration
├── evaluation.py              # Gate logic & validation
├── handlers*.py               # Various domain handlers
├── parallel_*.py              # Parallel phases
└── other modules
```

---

### 2. CLI COMMAND REGISTRATION (megaplan/cli.py)

**Command registration pattern: argparse subparsers**

**File:** `/Users/user_c042661f/Documents/megaplan/megaplan/cli.py`

**Function:** `build_parser()` — lines 802–952
- Creates root `ArgumentParser` with `add_subparsers(dest="command", required=True)` at line 804
- Registers all commands as subparsers

**Command categories:**

| Command | Lines | Subcommand Args |
|---------|-------|-----------------|
| `setup` | 806–809 | `--local`, `--target-dir`, `--force` |
| `init` | 811–820 | `--project-dir` (req), `--name`, `--auto-approve`, `--robustness`, `--hermes`, `--phase-model` |
| `list` | 822–832 | `--all`, `--no-tree`, `--include-done`, `--status`, `--summary` |
| `status/audit/progress/watch` | 834–836 | `--plan` |
| **Phase steps** (plan, prep, critique, revise, gate, finalize, execute, review) | 838–854 | `--plan`, `--agent`, `--hermes`, `--phase-model`, `--fresh`, `--persist`, `--ephemeral`; execute also has `--confirm-destructive`, `--user-approved`, `--batch` |
| `config` | 856–862 | Sub-actions: show, set, reset |
| `step` | 864–879 | Sub-actions: add, remove, move |
| `override` | 881–886 | Actions: abort, force-proceed, add-note, replan, set-robustness |
| `debt` | 888–902 | Sub-actions: list, add, resolve |
| `loop-*` (loop-init, loop-run, loop-status, loop-pause) | 904–944 | Various loop-specific args |
| `auto` / `chain` | 946–950 | Custom parsers from auto.py and chain.py |

**Command dispatch table:**
- **Lines 955–977:** `COMMAND_HANDLERS` dict maps command names to handler functions
- Maps: `init` → `handle_init`, `plan` → `handle_plan`, etc.

**Example subparser creation (lines 838–854):**
```python
for name in ["plan", "prep", "critique", "revise", "gate", "finalize", "execute", "review"]:
    step_parser = subparsers.add_parser(name)
    step_parser.add_argument("--plan")
    step_parser.add_argument("--agent", choices=["claude", "codex", "hermes"])
    # ... more args
```

---

### 3. HANDLERS DISPATCH (megaplan/handlers.py)

**File:** `/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py` (85KB)

**Pattern:** Each handler function signature is `handler(root: Path, args: argparse.Namespace) -> StepResponse`

**Key handlers:**

| Handler | Lines | Purpose |
|---------|-------|---------|
| `handle_init` | 717–791 | Initialize new plan |
| `handle_plan` | 794–836 | Generate initial plan |
| `handle_prep` | 840–858 | Prepare context (code refs, test expectations) |
| `handle_critique` | 861–991 | Run critique checks, flag issues |
| `handle_revise` | 994–1046 | Revise plan based on critique |
| `handle_gate` | 1049–1307 | Gate decision (PROCEED/ITERATE/ESCALATE) |
| `handle_finalize` | 1308–1335 | Finalize execution plan (generate tasks) |
| `handle_execute` | 1337–1575 | Execute tasks in batches |
| `handle_review` | 1576–2015 | Review execution against success criteria |
| `handle_override` | 2016+ | Force proceed, abort, replan, etc. |

**Core dispatch function: `_run_worker()` — lines 167–207**
- Signature: `_run_worker(step, state, plan_dir, args, *, root, iteration=None, resolved=None, prompt_override=None, prompt_kwargs=None) → (WorkerResult, agent, mode, refreshed)`
- Sets active step in state
- Calls `worker_module.run_step_with_worker()` — delegates to workers.py
- Catches errors, records failures, clears active step
- Line 192: dispatches to `run_step_with_worker()` with proper kwargs

**Finish step helper: `_finish_step()` — lines 257–316**
- Updates state, appends history
- Applies session updates
- Computes next step via `workflow_next(state)`
- Returns `StepResponse` JSON dict
- Attaches runtime hints for next step

---

### 4. WORKERS DISPATCH (megaplan/workers.py)

**File:** `/Users/user_c042661f/Documents/megaplan/megaplan/workers.py` (60KB)

**Key entry point: `run_step_with_worker()` — lines 1477–1573**

**Signature:**
```python
def run_step_with_worker(
    step: str,
    state: PlanState,
    plan_dir: Path,
    args: argparse.Namespace,
    *,
    root: Path,
    resolved: tuple[str, str, bool, str | None] | None = None,
    prompt_override: str | None = None,
    prompt_kwargs: dict[str, Any] | None = None,
) → tuple[WorkerResult, str, str, bool]
```

**Dispatch logic (lines 1492–1573):**
1. Resolves agent/mode/model from args via `resolve_agent_mode()`
2. Loops attempting agents with fallback logic
3. Agent-specific dispatch:
   - **Hermes:** calls `run_hermes_step()` (deferred import at line 1497) — lines 1495–1506
   - **Claude:** calls `run_claude_step()` — lines 1507–1516
   - **Codex:** calls `run_codex_step()` — lines 1521–1531
4. Returns `(WorkerResult, agent_name, mode, refreshed_flag)`
5. Implements fallback logic for auth/connection errors (lines 1554–1572)

**Worker functions:**

#### `run_claude_step()` — lines 1088–1139
**Signature:**
```python
def run_claude_step(
    step: str,
    state: PlanState,
    plan_dir: Path,
    *,
    root: Path,
    fresh: bool,
    prompt_override: str | None = None,
    prompt_kwargs: dict[str, Any] | None = None,
) → WorkerResult
```

**Implementation:**
- Line 1098–1099: Mock check via `MOCK_ENV_VAR`
- Line 1101: Loads schema from `schemas_root(root) / STEP_SCHEMA_FILENAMES[step]`
- Lines 1103–1105: Retrieves session (for persistent sessions)
- Lines 1106–1113: Builds claude command with `--json-schema`, `--add-dir`, optional `--session-id` or `--resume`
- Line 1114–1120: Creates prompt via `create_claude_prompt()` or prompt_override
- Line 1122: Executes via `run_command()`, captures stdout/stderr
- Lines 1128–1132: Parses envelope, validates payload
- Returns `WorkerResult` with payload, raw_output, duration_ms, cost_usd, session_id

#### `run_codex_step()` — lines 1142–1320+
**Signature:**
```python
def run_codex_step(
    step: str,
    state: PlanState,
    plan_dir: Path,
    *,
    root: Path,
    persistent: bool,
    fresh: bool = False,
    json_trace: bool = False,
    prompt_override: str | None = None,
    prompt_kwargs: dict[str, Any] | None = None,
) → WorkerResult
```

**Key features:**
- Lines 1172–1185: Resume path if persistent session exists (codex exec resume)
- Lines 1186–1216: Create path with sandbox config, output schema
- Lines 1218–1225: Executes codex command with stdin prompt
- Lines 1226–1254: Session recovery on rollout missing (container restart handling)
- Lines 1255–1273: Timeout payload recovery from partial output
- Line 1219–1225: `run_command()` wrapper with `timeout_seconds` parameter

#### `run_command()` — lines 94–154
**Signature:**
```python
def run_command(
    command: list[str],
    *,
    cwd: Path,
    stdin_text: str = "",
    env: dict[str, str] | None = None,
    timeout: int | None = None,
) → CommandResult
```

**Returns:**
```python
@dataclass
class CommandResult:
    returncode: int
    stdout: str
    stderr: str
    duration_ms: int
```

---

### 5. SESSION MANAGEMENT (megaplan/_core/state.py)

**File:** `/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py`

**Session structure in PlanState:**
- `state["sessions"]` is a dict mapping session keys to session info dicts
- Session key format: built via `session_key_for(step, agent, model=None)` (workers.py)
- Session entry structure (SessionInfo TypedDict):
  ```python
  {
    "id": str,           # UUID or session ID from worker
    "mode": str,         # "persistent" | "ephemeral"
    "created_at": str,   # ISO timestamp
    "last_used_at": str, # ISO timestamp
    "refreshed": bool,   # Whether fresh session was created
  }
  ```

**Core functions:**

| Function | Lines | Purpose |
|----------|-------|---------|
| `load_plan_locked()` | 212–215 | Context manager: acquires file lock on plan, loads state |
| `plan_lock()` | 188–208 | File-based locking via fcntl |
| `plan_lock_is_held()` | 154–167 | Check if plan is already locked |
| `set_active_step()` | 246–273 | Records which step is currently running with agent/session |
| `clear_active_step()` | 276–280 | Clears active step after completion |
| `apply_session_update()` | 222–243 | Updates session info in state after worker run |
| `append_history()` | 287–293 | Appends execution history entry |
| `make_history_entry()` | 296–354 | Builds HistoryEntry dict |
| `save_state()` | 218–219 | Atomic write of state.json |

**Key state fields (PlanState TypedDict in types.py):**
- `name: str` — plan identifier
- `idea: str` — user's original request
- `current_state: str` — one of STATE_* constants
- `iteration: int` — plan version number
- `config: PlanConfig` — project_dir, auto_approve, robustness, agents routing
- `sessions: dict[str, SessionInfo]` — active agent sessions
- `plan_versions: list[PlanVersionRecord]` — history of plan versions
- `history: list[HistoryEntry]` — per-step execution log
- `meta: PlanMeta` — costs, scores, notes, etc.
- `last_gate: LastGateRecord` — result of most recent gate
- `active_step: NotRequired[ActiveStep]` — currently-running phase

---

### 6. PROMPT FILES (megaplan/prompts/)

**File:** `/Users/user_c042661f/Documents/megaplan/megaplan/prompts/__init__.py`

**Prompt builder dispatch tables (lines 46–95):**

```python
_CLAUDE_PROMPT_BUILDERS: dict[str, Callable] = {
    "plan": _plan_prompt,
    "prep": _prep_prompt,
    "critique": _critique_prompt,
    "revise": _revise_prompt,
    "gate": _gate_prompt,
    "finalize": _finalize_prompt,
    "execute": _execute_prompt,
    "review": partial(_review_prompt, review_intro=..., criteria_guidance=..., ...),
}

_CODEX_PROMPT_BUILDERS: dict[str, Callable] = { ... }  # Similar mapping
_HERMES_PROMPT_BUILDERS: dict[str, Callable] = { ... }  # Similar mapping
```

**Prompt creation functions (lines 110–146):**

| Function | Lines | Purpose |
|----------|-------|---------|
| `create_claude_prompt()` | 110–120 | Builds Claude prompt for step, adds guard clause |
| `create_codex_prompt()` | 123–133 | Builds Codex prompt for step |
| `create_hermes_prompt()` | 136–146 | Builds Hermes prompt for step |

**Guard clause (lines 97–107):**
- Prepends `_NESTED_HARNESS_GUARD` to prevent nested megaplan invocations
- Applied to all steps via `_prepend_harness_guard()`

**Prompt modules:**

| Module | Purpose |
|--------|---------|
| `planning.py` | `_plan_prompt()`, `_prep_prompt()`, `PLAN_TEMPLATE` |
| `critique.py` | `_critique_prompt()`, `_revise_prompt()`, `_write_critique_template()` |
| `execute.py` | `_execute_prompt()`, `_execute_batch_prompt()`, `_execute_approval_note()`, `_execute_nudges()` |
| `finalize.py` | `_finalize_prompt()` — builds task checklist |
| `gate.py` | `_gate_prompt()`, `_collect_critique_summaries()`, `_flag_summary()` |
| `review.py` | `_review_prompt()`, `_write_review_template()`, `_settled_decisions_block()` |
| `_shared.py` | Shared utilities: debt blocks, prep block rendering, prompt root resolution |

---

### 7. JSON SCHEMAS (megaplan/schemas.py and .megaplan/schemas/)

**Schema definition location:** `/Users/user_c042661f/Documents/megaplan/megaplan/schemas.py`

**Schema files stored at:** `/Users/user_c042661f/Documents/megaplan/.megaplan/schemas/`

**Available schemas:**

| Schema | Output of | Purpose |
|--------|-----------|---------|
| `plan.json` | plan/revise step | `{plan, questions[], success_criteria[], assumptions[]}` |
| `prep.json` | prep step | `{skip, task_summary, key_evidence[], relevant_code[], test_expectations[], constraints[], suggested_approach}` |
| `critique.json` | critique step | `{checks[{id, question, findings[]}], flags[], verified_flag_ids[], disputed_flag_ids[]}` |
| `revise.json` | revise step | `{plan, changes_summary, flags_addressed[], assumptions[], success_criteria[], questions[]}` |
| `gate.json` | gate step | `{recommendation (enum: PROCEED/ITERATE/ESCALATE), rationale, signals_assessment, warnings[], settled_decisions[], flag_resolutions[], accepted_tradeoffs[]}` |
| `finalize.json` | finalize step | `{tasks[], sense_checks[], execution_strategies}` |
| `execution.json` | execute step | `{output, files_changed[], commands_run[], deviations[], task_updates[], sense_check_acknowledgments[]}` |
| `review.json` | review step | `{task_verdicts[], sense_check_assessments[], issues[], needs_rework}` |
| `loop_plan.json` | loop-plan phase | Simplified plan schema |
| `loop_execute.json` | loop-execute phase | Simplified execution schema |

**Example schema structure (plan.json — lines 9–28 in schemas.py):**
```json
{
  "type": "object",
  "properties": {
    "plan": {"type": "string"},
    "questions": {"type": "array", "items": {"type": "string"}},
    "success_criteria": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "criterion": {"type": "string"},
          "priority": {"type": "string", "enum": ["must", "should", "info"]}
        },
        "required": ["criterion", "priority"]
      }
    },
    "assumptions": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["plan", "questions", "success_criteria", "assumptions"]
}
```

**Schema loading:**
- Line 1101 in workers.py: `schema_text = json.dumps(read_json(schemas_root(root) / schema_name))`
- Passed to claude via `--json-schema` arg
- Passed to codex via `--output-schema` arg

---

### 8. TYPE DEFINITIONS (megaplan/types.py)

**File:** `/Users/user_c042661f/Documents/megaplan/megaplan/types.py` (346 lines)

**State constants (lines 12–21):**
```python
STATE_INITIALIZED = "initialized"    # After init
STATE_PREPPED = "prepped"            # After prep
STATE_PLANNED = "planned"            # After plan
STATE_CRITIQUED = "critiqued"        # After critique
STATE_GATED = "gated"                # After gate decision
STATE_FINALIZED = "finalized"        # After finalize
STATE_EXECUTED = "executed"          # After execute
STATE_DONE = "done"                  # After review → APPROVED
STATE_ABORTED = "aborted"            # Forced abort
TERMINAL_STATES = {STATE_DONE, STATE_ABORTED}
```

**Key TypedDicts:**

| TypedDict | Fields | Purpose |
|-----------|--------|---------|
| `PlanConfig` | project_dir, auto_approve, robustness, agents | Plan execution config |
| `PlanMeta` | significant_counts, weighted_scores, plan_deltas, recurring_critiques, total_cost_usd, overrides, notes, user_approved_gate | Metadata tracking |
| `SessionInfo` | id, mode, created_at, last_used_at, refreshed | Agent session info |
| `ActiveStep` | step, agent, mode, model, run_id, session_id, started_at | Currently-running phase |
| `HistoryEntry` | step, timestamp, duration_ms, cost_usd, result, session_mode, session_id, agent, output_file, artifact_hash, message, flags_count, etc. | Per-step execution record |
| `PlanState` | name, idea, current_state, iteration, created_at, config, sessions, plan_versions, history, meta, last_gate, active_step, clarification | Complete plan state |
| `GatePayload` | recommendation, rationale, signals_assessment, warnings, settled_decisions | Gate output |
| `StepResponse` | success, step, summary, artifacts, next_step, state, mode, error, message, details | JSON response to CLI |

**Agent routing (lines 267–286):**
```python
DEFAULT_AGENT_ROUTING: dict[str, str] = {
    "plan": "claude",       # Planning = Claude
    "prep": "claude",       # Prep = Claude
    "critique": "codex",    # Critique = Codex
    "revise": "claude",     # Revise = Claude
    "gate": "claude",       # Gate decision = Claude
    "finalize": "claude",   # Finalize = Claude
    "execute": "codex",     # Execution = Codex
    "loop_plan": "claude",
    "loop_execute": "codex",
    "review": "codex",      # Review = Codex
}
KNOWN_AGENTS = ["claude", "codex", "hermes"]
ROBUSTNESS_LEVELS = ("tiny", "light", "standard", "robust", "superrobust")
```

**Flag constants (lines 259–263):**
```python
FLAG_BLOCKING_STATUSES = {"open", "disputed", "addressed"}
FLAG_VALID_STATUSES = {"open", "addressed", "disputed", "verified", "accepted_tradeoff", "gate_disputed"}
DEBT_ESCALATION_THRESHOLD = 3
MOCK_ENV_VAR = "MEGAPLAN_MOCK_WORKERS"
```

**Defaults configuration (lines 298–323):**
```python
DEFAULTS = {
    "execution.auto_approve": False,
    "execution.robustness": "standard",
    "execution.worker_timeout_seconds": 7200,  # 2 hours
    "execution.max_review_rework_cycles": 3,
    "execution.max_robust_review_rework_cycles": 2,
    "execution.max_execute_no_progress": 3,
    "orchestration.max_critique_concurrency": 2,
    "orchestration.mode": "subagent",
}
```

---

### 9. HOW EXISTING PHASES WIRE WORKERS

**Pattern: Three-layer architecture**

#### Layer 1: CLI → handlers.py
- Command → `handle_<phase>()` function
- Example: `megaplan plan --plan myplan` → `handle_plan(root, args)` at line 794

#### Layer 2: handlers → workers
- Handler calls `_run_worker(step, state, plan_dir, args, root=root)` at line 199
- `_run_worker()` sets active step, calls `worker_module.run_step_with_worker()` at line 192
- Error handling + session update

#### Layer 3: workers → agent executor
- `run_step_with_worker()` resolves agent (claude/codex/hermes) from args
- Dispatches to agent-specific runner: `run_claude_step()`, `run_codex_step()`, or `run_hermes_step()`
- Returns WorkerResult with payload

#### Layer 4: Post-worker processing
- Handler receives WorkerResult, validates payload via `validate_payload(step, payload)`
- Writes artifacts to disk (JSON files, markdown files, etc.)
- Updates plan state (new state, flags, history)
- Calls `_finish_step()` to save and return response

**Example: plan phase (lines 794–836)**
```
handle_plan():
  1. load_plan_locked() — acquire lock, load state
  2. require_state() — verify current_state is valid
  3. _run_worker("plan", state, plan_dir, args, root=root)
     ↓ (calls run_step_with_worker in workers.py)
     ↓ Claude or Codex generates plan
  4. Validate payload: payload["plan"], payload["questions"], etc.
  5. _write_plan_version() — save plan.md + meta.json
  6. Update state: iteration++, current_state=STATE_PLANNED
  7. _finish_step() — save state, return response with next_step
```

**Example: critique phase (lines 861–991)**
```
handle_critique():
  1. load_plan_locked()
  2. Check robustness level:
     - "tiny" → stub critique, skip to gate
     - otherwise → run parallel_critique() or _run_worker()
  3. _run_worker("critique", state, plan_dir, args, root=root)
     ↓ Codex or Hermes generates critique checks + flags
  4. Validate checks match expected_ids
  5. Update flag registry via update_flags_after_critique()
  6. Count significant flags
  7. Auto-generate gate stub if light robustness (skip gate)
  8. _finish_step() with flag counts + open flags
```

**Workflow transitions (workflow.py, lines 31–67):**

State machine defines valid transitions:
```
WORKFLOW: dict[str, list[Transition]] = {
    STATE_INITIALIZED: [Transition("prep", STATE_PREPPED)],
    STATE_PREPPED: [Transition("plan", STATE_PLANNED)],
    STATE_PLANNED: [
        Transition("critique", STATE_CRITIQUED),
        Transition("plan", STATE_PLANNED),  # re-plan
    ],
    STATE_CRITIQUED: [
        Transition("gate", STATE_GATED, "gate_unset"),  # first time
        Transition("revise", STATE_PLANNED, "gate_iterate"),  # if gate says ITERATE
        Transition("override ...", ..., "gate_escalate"),  # if escalated
    ],
    STATE_GATED: [Transition("finalize", STATE_FINALIZED)],
    STATE_FINALIZED: [Transition("execute", STATE_EXECUTED)],
    STATE_EXECUTED: [Transition("review", STATE_DONE)],
}
```

**Robustness overrides** allow skipping phases:
- `light` robustness: skips prep, combines gate decision into critique
- `tiny` robustness: stubs critique entirely, skips review

---

### 10. CURRENT VERSION

**File:** `/Users/user_c042661f/Documents/megaplan/pyproject.toml`

**Version:** `0.16.0`

**Metadata:**
- Name: `megaplan-harness`
- Description: "AI agent harness for coordinating Claude and GPT to make and execute extremely robust plans"
- License: OSNL-0.2
- Entry point: `megaplan = "megaplan.cli:cli_entry"`
- Python requirement: >=3.11
- Dependencies: PyYAML >= 6.0

---

### INTEGRATION SUMMARY

**End-to-end flow for a phase:**

1. **CLI** (`cli.py`, line 804): User runs `megaplan plan --plan myplan`
2. **Dispatch** (`cli.py`, line 1023 onwards): `main()` parses args, calls `COMMAND_HANDLERS["plan"](root, args)`
3. **Handler** (`handlers.py`, line 794): `handle_plan()` acquires lock, validates state, calls `_run_worker()`
4. **Worker dispatch** (`handlers.py`, line 192): `run_step_with_worker()` resolves agent from args/config
5. **Agent runner** (`workers.py`, line 1507–1516): `run_claude_step()` or `run_codex_step()` 
   - Loads schema, creates prompt via `create_claude_prompt()`
   - Executes `claude` or `codex` subprocess with prompt + schema
   - Parses output, validates against schema
   - Returns `WorkerResult(payload, raw_output, duration_ms, cost_usd, session_id)`
6. **Post-processing** (`handlers.py`, line 801–836): Handler writes artifacts, updates state + history
7. **Finish** (`handlers.py`, line 822): `_finish_step()` saves state, computes next_step via `workflow_next()`, returns JSON response
8. **State transition**: `workflow.py` validates next step via `workflow_transition()` + robustness-specific overrides

**Key integration points:**

| Module | Role | Key Exports |
|--------|------|-------------|
| `types.py` | Type definitions & constants | State constants, TypedDicts, routing tables |
| `_core/state.py` | Plan state persistence | load_plan_locked, set_active_step, append_history |
| `_core/workflow.py` | State machine | WORKFLOW, workflow_next, workflow_transition |
| `_core/io.py` | I/O & config | atomic_write_json, read_json, schemas_root |
| `_core/registries.py` | Flag/debt tracking | load_flag_registry, update_flags_after_* |
| `prompts/__init__.py` | Prompt dispatch | create_claude_prompt, _CLAUDE_PROMPT_BUILDERS |
| `schemas.py` | JSON schema definitions | SCHEMAS dict |
| `handlers.py` | Phase orchestration | handle_plan, handle_critique, _run_worker, _finish_step |
| `workers.py` | Agent dispatch | run_step_with_worker, run_claude_step, run_codex_step |
| `cli.py` | CLI entry | build_parser, COMMAND_HANDLERS, main |
