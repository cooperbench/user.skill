> DEVELOPER

Read the following files in full and report their contents back to me verbatim (or summarize key sections with line numbers):

1. /Users/user_c042661f/Documents/megaplan/megaplan/types.py
2. /Users/user_c042661f/Documents/megaplan/megaplan/_core/workflow.py
3. /Users/user_c042661f/Documents/megaplan/megaplan/auto.py (especially lines 1-50 and 180-210)
4. /Users/user_c042661f/Documents/megaplan/megaplan/schemas.py (especially schema definitions for plan.json, revise.json, review.json criteria pass enum, critique.json flags category enum)
5. /Users/user_c042661f/Documents/megaplan/pyproject.toml (version line)
6. /Users/user_c042661f/Documents/megaplan/CHANGELOG.md (first 30 lines)
7. /Users/user_c042661f/Documents/megaplan/megaplan/handlers.py lines 1-30 (imports) and the DEFAULT_AGENT_ROUTING constant if it exists

I need the exact content to make precise edits. Focus on giving me exact line numbers and content for the areas I'll need to modify.

> AGENT

I'll read all these files for you. Let me fetch them in parallel.

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
185	        # Terminal: plan reached a final state.
186	        if state in TERMINAL_STATES:
187	            log(f"terminal state reached: {state}")
188	            return DriverOutcome(
189	                status="done" if state == "done" else "aborted",
190	                plan=plan,
191	                final_state=state,
192	                iterations=iteration,
193	                reason=f"plan entered terminal state '{state}'",
194	                last_phase=last_phase,
195	                events=events,
196	            )
197	
198	        # Stall detection: same state for stall_threshold+ iterations.
199	        if state == last_state:
200	            stall_count += 1
201	            if stall_count >= stall_threshold:
202	                log(f"stalled at state={state} for {stall_count} iterations")
203	                return DriverOutcome(
204	                    status="stalled",
205	                    plan=plan,
206	                    final_state=state,
207	                    iterations=iteration,
208	                    reason=(
209	                        f"stalled at '{state}' for {stall_count} iterations — "
210	                        "manual intervention required"
211	                    ),
212	                    last_phase=last_phase,
213	                    events=events,
214	                )
215	        else:
216	            stall_count = 0
217	            last_state = state
218	
219	        # Escalation: no phase to run but overrides are available.
220	        if not next_step:
221	            if _has_valid_next(status, "override force-proceed"):
222	                if on_escalate == "force-proceed":
223	                    log("gate escalated — force-proceeding (per on_escalate=force-proceed)")
224	                    code, out, err = _run_megaplan(
225	                        [
226	                            "override",
227	                            "force-proceed",
228	                            "--plan",
229	                            plan,
230	                            "--reason",
231	                            "megaplan auto: escalate → force-proceed",
232	                        ],
233	                        cwd=cwd,
234	                        timeout=status_timeout,
235	                    )
236	                    if code != 0:
237	                        log(f"force-proceed failed (exit {code}): {err.strip() or out.strip()}")
238	                        return DriverOutcome(
239	                            status="failed",
240	                            plan=plan,
241	                            final_state=state,
242	                            iterations=iteration,
243	                            reason=f"override force-proceed exited {code}",
244	                            last_phase=last_phase,
245	                            events=events,
246	                        )
247	                    continue
248	                if on_escalate == "abort":
249	                    log("gate escalated — aborting (per on_escalate=abort)")
250	                    _run_megaplan(
251	                        [
252	                            "override",
253	                            "abort",
254	                            "--plan",
255	                            plan,
256	                            "--reason",
257	                            "megaplan auto: escalate → abort",
258	                        ],
259	                        cwd=cwd,
260	                        timeout=status_timeout,
261	                    )
262	                    return DriverOutcome(
263	                        status="aborted",
264	                        plan=plan,
265	                        final_state=state,
266	                        iterations=iteration,
267	                        reason="gate escalated and on_escalate=abort",
268	                        last_phase=last_phase,
269	                        events=events,
270	                    )
271	                # on_escalate == "fail"
272	                log("gate escalated — failing (per on_escalate=fail)")
273	                return DriverOutcome(
274	                    status="escalated",
275	                    plan=plan,
276	                    final_state=state,
277	                    iterations=iteration,
278	                    reason="gate escalated and on_escalate=fail — human required",
279	                    last_phase=last_phase,
280	                    events=events,
281	                )
282	            log(f"no next_step and no override available (valid_next={valid_next})")
283	            return DriverOutcome(
284	                status="failed",
285	                plan=plan,
286	                final_state=state,
287	                iterations=iteration,
288	                reason="no next_step and no override available",
289	                last_phase=last_phase,
290	                events=events,
291	            )
292	
293	        # Run the next phase.
294	        cmd = _phase_command(next_step) + ["--plan", plan]
295	        log(f"running: megaplan {' '.join(cmd)}", phase=next_step, timeout=phase_timeout)
296	        last_phase = next_step
297	        code, out, err = _run_megaplan(cmd, cwd=cwd, timeout=phase_timeout)
298	        if code == PHASE_TIMEOUT_EXIT_CODE:
299	            log(f"phase '{next_step}' timed out after {phase_timeout}s — stall detection will enforce the cap")
300	        elif code != 0:
301	            # Don't bail immediately — megaplan often records a partial failure
302	            # in state.json and the next status() reveals a recoverable valid_next.
303	            # Stall detection will still kill infinite loops.
304	            log(f"phase '{next_step}' exited {code}: {err.strip() or out.strip()[-400:]}")
305	        if poll_sleep > 0:
306	            time.sleep(poll_sleep)
307	
308	    # Hit iteration cap.
309	    log(f"hit max_iterations={max_iterations}")
310	    return DriverOutcome(
311	        status="cap",
312	        plan=plan,
313	        final_state=last_state or "unknown",
314	        iterations=max_iterations,
315	        reason=f"exceeded max_iterations={max_iterations}",
316	        last_phase=last_phase,
317	        events=events,
318	    )
319	
320	
321	def build_auto_parser(subparsers: Any) -> None:
322	    auto_parser = subparsers.add_parser(
323	        "auto",
324	        help="Drive a plan to completion without human intervention",
325	    )
326	    auto_parser.add_argument("--plan", required=True, help="Plan name")
327	    auto_parser.add_argument(
328	        "--stall-threshold",
329	        type=int,
330	        default=DEFAULT_STALL_THRESHOLD,
331	        help=f"Exit if the plan state doesn't change for this many iterations (default {DEFAULT_STALL_THRESHOLD})",
332	    )
333	    auto_parser.add_argument(
334	        "--max-iterations",
335	        type=int,
336	        default=DEFAULT_MAX_ITERATIONS,
337	        help=f"Hard cap on loop iterations (default {DEFAULT_MAX_ITERATIONS})",
338	    )
339	    auto_parser.add_argument(
340	        "--on-escalate",
341	        choices=ESCALATE_ACTIONS,
342	        default="force-proceed",
343	        help="What to do when the gate escalates (default force-proceed)",
344	    )
345	    auto_parser.add_argument(
346	        "--poll-sleep",
347	        type=float,
348	        default=DEFAULT_POLL_SLEEP_SECONDS,
349	        help=f"Seconds to sleep between phase transitions (default {DEFAULT_POLL_SLEEP_SECONDS})",
350	    )
351	    auto_parser.add_argument(
352	        "--phase-timeout",
353	        type=float,
354	        default=DEFAULT_PHASE_TIMEOUT_SECONDS,
355	        help=(
356	            f"Seconds before a single phase subprocess (plan/prep/critique/gate/finalize/execute/review) "
357	            f"is killed and treated as a failure (default {DEFAULT_PHASE_TIMEOUT_SECONDS}s). "
358	            "Stall detection still applies on top."
359	        ),
360	    )
361	    auto_parser.add_argument(
362	        "--status-timeout",
363	        type=float,
364	        default=DEFAULT_STATUS_TIMEOUT_SECONDS,
365	        help=(
366	            f"Seconds before `megaplan status` / override subprocesses are killed "
367	            f"(default {DEFAULT_STATUS_TIMEOUT_SECONDS}s). These should always be quick; "
368	            "hitting this indicates serious trouble."
369	        ),
370	    )
371	
372	
373	def run_auto(root: Path, args: argparse.Namespace) -> int:
374	    """CLI entry point. Returns a POSIX exit code suitable for ``sys.exit``."""
375	    outcome = drive(
376	        args.plan,
377	        cwd=root,
378	        stall_threshold=args.stall_threshold,
379	        max_iterations=args.max_iterations,
380	        on_escalate=args.on_escalate,
381	        poll_sleep=args.poll_sleep,
382	        phase_timeout=args.phase_timeout,
383	        status_timeout=args.status_timeout,
384	    )
385	    sys.stdout.write(outcome.to_json() + "\n")
386	    if outcome.status == "done":
387	        return 0
388	    if outcome.status == "aborted":
389	        return 0  # user-requested abort is not a failure
390	    if outcome.status == "stalled":
391	        return 2
392	    if outcome.status == "escalated":
393	        return 3
394	    if outcome.status == "cap":
395	        return 4
396	    return 1
397
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
  "file_path": "/Users/user_c042661f/Documents/megaplan/CHANGELOG.md"
}
```

> TOOL

tool_result Read
```
1	# Changelog
2	
3	## v0.16.0 — 2026-04-15
4	
5	### Chain driver (`megaplan chain`)
6	
7	New first-class subcommand that drives an ordered pipeline of milestone plans described by a YAML spec. Replaces ad-hoc bash orchestration (`chain.sh`) so plan-state logic lives in megaplan instead of fragile shell polling.
8	
9	- **Spec-driven**: `megaplan chain --spec path/to/chain.yaml` reads milestones, optional seed plan, and failure/escalate policies from YAML.
10	- **Resumable**: progress is persisted to `chain_state.json` next to the spec (`current_milestone_index`, `current_plan_name`, `last_state`, `completed`). A relaunched process reads this file and picks up where the previous run stopped.
11	- **State-aware in the right layer**: each milestone is driven via the existing `megaplan.auto.drive` entry point, so phase selection (`plan → prep → critique → ... → review`) stays in megaplan. Shell wrappers no longer need to classify `next_step`.
12	- **`megaplan chain status --spec PATH`**: prints current chain progress without driving.
13	- **Failure/escalate policies**: `stop_chain` (default), `skip_milestone`, `retry_milestone`.
14	- **Seed handling**: if a seed plan is specified and not already in a terminal state, it is driven first under the same auto loop — fixing the gap where seed plans had no state-aware driver.
15	- **Validation**: up front, the chain driver checks every idea file exists and the seed plan (if set) resolves under the project root. Structured `invalid_spec` / `missing_idea_file` / `missing_seed_plan` errors.
16	- **PyYAML** added as a runtime dependency.
17	
18	### Tests
19	
20	- `tests/test_chain.py` covers spec parsing, `chain status`, idea-file validation, seed-plan validation, happy-path execution (with `auto.drive` mocked), resume-from-`chain_state.json`, and on-failure `stop_chain`.
21	
22	## v0.14.0 — 2026-04-15
23	
24	### Strict gate flag resolution
25	
26	The gate no longer silently accepts unresolved blocking flags on a PROCEED recommendation. PROCEED now requires explicit `flag_resolutions` for every blocking flag, and a retry is issued once when the first response still leaves blocking blockers unresolved.
27	
28	- **No implicit acceptance**: unresolved blocking flags now trigger a single gate reprompt instead of being auto-marked as accepted tradeoffs.
29	- **Auto-downgrade on retry failure**: if the retry still leaves blocking flags unresolved, the gate artifact is rewritten as `ITERATE` with an auto-downgrade rationale note and `reprompted: true`.
30	- **Stricter tradeoff validation**: `accept_tradeoff` entries now require concrete, flag-specific rationale; rubber-stamp phrases are rejected the same way weak dispute evidence is rejected.
31	- **Debt derived from explicit resolutions**: accepted tradeoff debt entries now come from validated `flag_resolutions` rather than fallback unresolved-flag recording.
32	- **Gate test coverage refreshed**: existing gate debt tests now follow the strict-resolution contract, and new tests cover reprompt success, reprompt downgrade, rubber-stamp rejection, no-reprompt happy path, and resolution-derived debt recording.
33	
34	## v0.12.0 — 2026-04-15
35	
36	### Auto driver
37	
38	New `megaplan auto --plan <name>` drives a plan from its current state to a terminal outcome without human intervention. The driver is intentionally dumb: it reads `status`, runs `next_step`, and loops. All real judgment stays in the phase logic.
39	
40	- **Gate escalation policy**: ESCALATE defaults to force-proceed. Opt out with `--on-escalate abort` or `--on-escalate fail`.
41	- **Stall detection**: bails after N consecutive iterations in the same state (default 5).
42	- **Iteration cap**: hard stop at 200 iterations by default to bound runaway loops.
43	- **Structured exit codes**: `done=0`, `failed=1`, `stalled=2`, `escalated=3`, `cap=4` — so shell callers and CI can branch on terminal state without parsing output.
44	- Emits a JSON outcome with the final state snapshot and event log on exit.
45	
46	### Cross-directory plan discovery
47	
48	`resolve_plan_dir` now walks both parent and child directories to locate plans by name, so megaplan commands work from anywhere in a project tree — not just the directory containing `.megaplan/`.
49	
50	- **`megaplan list --tree`**: list plans in the current subtree.
51	- **`megaplan list --all`**: system-wide plan discovery across the whole workspace.
52	
53	### Standard robustness: init→plan transition
54	
55	The `standard` robustness profile now picks up the init→plan transition that was previously only wired under heavier levels. Standard plans no longer stall after init waiting for a transition that never fires.
56	
57	### Tests
58	
59	Added `test_auto` coverage for the driver loop, escalation policies, stall detection, and iteration caps.
60	
61	## v0.10.0 — 2026-04-10
62	
63	### Codex backend hardening
64	
65	The Codex (OpenAI) worker path got a major reliability overhaul, fixing a class of issues that caused silent failures, misclassified errors, and lost output when running with `--agent codex` or Hermes.
66	
67	- **Timeout recovery**: when a Codex step times out, megaplan now attempts to recover partial output from the output file and stdout before raising. If valid structured output was produced before the timeout, the step succeeds instead of failing.
68	- **Per-step timeout caps**: non-execute steps (plan, critique, revise, etc.) are capped at 300s instead of inheriting the full 7200s worker timeout. Execute steps keep the full timeout.
69	- **Environment isolation**: child Codex processes no longer inherit `CODEX_THREAD_ID` or `CODEX_CI` from the parent, preventing workers from attaching to the wrong session.
70	- **Error classifier rewrite**: connection-level failures (DNS, WebSocket, stream disconnect) are now detected before HTTP status codes, fixing false positives where thread IDs or unrelated numbers were misclassified as 429s. Bare numeric patterns (`429`, `500`, etc.) now use word-boundary regex.
71	- **JSON extraction rewrite**: switched from greedy brace-matching to `JSONDecoder.raw_decode()`, which correctly handles trailing logs/traces after the JSON object.
72	- **Merged partial output**: timeout and crash error payloads now include both stderr/stdout and any file the worker managed to write, giving better diagnostics.
73	
74	### Concurrency & observability
75	
76	- **Plan locking**: all step handlers now acquire an `fcntl` file lock, preventing two processes from running steps on the same plan concurrently. Collisions produce a clear error naming the active step and agent.
77	- **Active step tracking**: `state.json` now carries an `active_step` field (`step`, `agent`, `mode`, `run_id`, `started_at`) set before the worker launches and cleared on completion or failure. Stale detection at 300s.
78	- **`megaplan status`**: now returns `active_step`, `last_step`, `total_cost_usd`, notes, and session summaries — everything the orchestrator needs without reading raw state.
79	- **`megaplan watch`**: new command combining `status` + `progress` into a single response for real-time monitoring.
80	
81	### Tiny robustness level
82	
83	New `--robustness tiny` mode stubs the critique and gate steps entirely, going straight from `plan` to `gated` to `finalize`. Useful for trivial tasks where the full critique loop is overhead.
84	
85	### Parallel review for heavy mode
86	
87	Heavy robustness now runs review checks in parallel (same pattern as parallel critique), splitting mechanical checks, sense checks, and task verification across concurrent workers.
88	
89	### OpenAI strict-mode schema compatibility
90	
91	- Recursive `required` reconciliation: all schema properties are now added to `required` arrays to satisfy OpenAI's structured output constraint that every property must be required.
92	- `flag_id` and `source` in review rework items changed from optional strings to required nullable (`["string", "null"]`).
93	- Gate `flag_resolutions` entries now require both `evidence` and `rationale` fields (use `""` for the one that doesn't apply).
94	- `accepted_tradeoffs` is now always returned (use `[]` when empty).
95	
96	### Prompt improvements
97	
98	- **Nested harness guard**: all worker prompts now include a preamble preventing the model from recursively invoking the `megaplan` CLI or skill.
99	- **Plan focus guidance**: planning prompt now tells the model to stop exploring once it has enough evidence, and to avoid `.megaplan/`, prior plan artifacts, and unrelated docs.
100	- **Standard robustness now includes prep**: removed the override that skipped the prep phase for standard robustness. All levels now run prep.
101	
102	### Other
103	
104	- License changed to OSNL 0.2.
105	- README updated: robustness level descriptions, observability section rewritten for `status`/`watch`.
106	- Comprehensive new test suites: `test_handle_review_robustness`, `test_parallel_review`, `test_review_checks`, `test_review_mechanical`, `test_tiny_robustness`, `test_config`, `test_io_git_patch`.
107
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
File content (23685 tokens) exceeds maximum allowed tokens (10000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
```

> AGENT

Let me read the handlers.py file in sections:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 0,
  "limit": 50
}
```

> TOOL

tool_result Read
```
0	from __future__ import annotations
1	
2	import argparse
3	import inspect
4	import logging
5	import os
6	import shutil
7	import subprocess
8	import sys
9	from datetime import datetime
10	from pathlib import Path
11	from typing import Any, Callable
12	
13	import megaplan.review_checks as review_checks
14	import megaplan.workers as worker_module
15	from megaplan.checks import checks_for_robustness, validate_critique_checks
16	from megaplan.execution import (
17	    _check_done_task_evidence,
18	    build_monitor_hint,
19	    handle_execute_auto_loop as dispatch_execute_auto_loop,
20	    handle_execute_one_batch as dispatch_execute_one_batch,
21	)
22	from megaplan.flags import (
23	    update_flags_after_critique,
24	    update_flags_after_gate,
25	    update_flags_after_review,
26	    update_flags_after_revise,
27	)
28	from megaplan.merge import _validate_and_merge_batch
29	from megaplan.parallel_critique import run_parallel_critique
30	from megaplan.parallel_review import run_parallel_review
31	from megaplan.prompts import create_claude_prompt, create_codex_prompt, create_hermes_prompt
32	from megaplan.review_mechanical import run_pre_checks
33	from megaplan.step_edit import next_plan_artifact_name
34	from megaplan.types import (
35	    FLAG_BLOCKING_STATUSES,
36	    MOCK_ENV_VAR,
37	    ROBUSTNESS_LEVELS,
38	    CliError,
39	    PlanState,
40	    STATE_ABORTED,
41	    STATE_CRITIQUED,
42	    STATE_DONE,
43	    STATE_EXECUTED,
44	    STATE_FINALIZED,
45	    STATE_GATED,
46	    STATE_INITIALIZED,
47	    STATE_PREPPED,
48	    STATE_PLANNED,
49	    StepResponse,
```

> TOOL

tool_use Grep
```json
{
  "pattern": "DEFAULT_AGENT_ROUTING",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "output_mode": "content"
}
```

> TOOL

tool_result Grep
```
No matches found
```

> AGENT

Let me search more specifically in handlers.py:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"DEFAULT_AGENT_ROUTING\\|AGENT_ROUTING\" /Users/user_c042661f/Documents/megaplan/megaplan/handlers.py | head -20"
}
```

> TOOL

tool_result Bash
```
[rerun: b1]
```

> AGENT

There doesn't appear to be a DEFAULT_AGENT_ROUTING constant in handlers.py. Let me verify by searching the entire codebase:

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"DEFAULT_AGENT_ROUTING\" /Users/user_c042661f/Documents/megaplan --include=\"*.py\""
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/types.py:DEFAULT_AGENT_ROUTING: dict[str, str] = {
/Users/user_c042661f/Documents/megaplan/megaplan/cli.py:    DEFAULT_AGENT_ROUTING,
/Users/user_c042661f/Documents/megaplan/megaplan/cli.py:        agents_config = {step: (default if default in available else available[0]) for step, default in DEFAULT_AGENT_ROUTING.items()}
/Users/user_c042661f/Documents/megaplan/megaplan/cli.py:        effective_routing = {step: config.get("agents", {}).get(step, default) for step, default in DEFAULT_AGENT_ROUTING.items()}
/Users/user_c042661f/Documents/megaplan/megaplan/cli.py:            *(f"agents.{step}" for step in DEFAULT_AGENT_ROUTING),
/Users/user_c042661f/Documents/megaplan/megaplan/cli.py:            if setting not in DEFAULT_AGENT_ROUTING:
/Users/user_c042661f/Documents/megaplan/megaplan/cli.py:                raise CliError("invalid_args", f"Unknown step '{setting}'. Valid steps: {', '.join(DEFAULT_AGENT_ROUTING)}")
/Users/user_c042661f/Documents/megaplan/megaplan/workers.py:    DEFAULT_AGENT_ROUTING,
/Users/user_c042661f/Documents/megaplan/megaplan/workers.py:                spec = config.get("agents", {}).get(step) or DEFAULT_AGENT_ROUTING[step]
[rerun: b2]
```

> AGENT

Perfect. Now let me compile the full response with all the information you requested:

## Summary of File Contents

Here are the exact contents and locations of the files you requested:

---

### 1. **types.py** — Complete file
File: `/Users/user_c042661f/Documents/megaplan/megaplan/types.py` (346 lines)

Key sections for your edits:

**Lines 267-278** — DEFAULT_AGENT_ROUTING constant:
```python
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
}
```

**Lines 280** — ROBUSTNESS_LEVELS:
```python
ROBUSTNESS_LEVELS = ("tiny", "light", "standard", "robust", "superrobust")
```

---

### 2. **_core/workflow.py** — Complete file
File: `/Users/user_c042661f/Documents/megaplan/megaplan/_core/workflow.py` (240 lines)

Key section for robustness workflow:
- **Lines 74-92**: `_ROBUSTNESS_OVERRIDES` dictionary defining workflow transitions by robustness level
- **Lines 94-100**: `_ROBUSTNESS_WORKFLOW_LEVELS` mapping robustness levels to their inheritance hierarchy
- **Lines 114-124**: Helper functions `configured_robustness()` and `robustness_critique_instruction()`

---

### 3. **auto.py** — Selected sections
File: `/Users/user_c042661f/Documents/megaplan/megaplan/auto.py`

**Lines 1-50** (full):
```python
"""Auto-driver that advances a plan through its phases without human intervention.

This is the mechanical loop that most orchestrators end up writing by hand:
read `status`, run `next_step`, repeat until terminal. All real judgment is
delegated to megaplan's existing phase logic — the driver only applies two
documented defaults:

1. Gate ESCALATE → force-proceed (caller opts out with ``--on-escalate abort``
   or ``--on-escalate fail``).
2. Same state for N consecutive iterations → bail (stall detection).

The driver is intentionally dumb. If a run needs judgment the driver can't
provide, it exits with a non-zero status and prints the state snapshot so the
caller can intervene.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from megaplan.types import TERMINAL_STATES


DEFAULT_STALL_THRESHOLD = 5
DEFAULT_MAX_ITERATIONS = 200
DEFAULT_POLL_SLEEP_SECONDS = 1.0
DEFAULT_PHASE_TIMEOUT_SECONDS = 3600
DEFAULT_STATUS_TIMEOUT_SECONDS = 60
ESCALATE_ACTIONS = ("force-proceed", "abort", "fail")
PHASE_TIMEOUT_EXIT_CODE = 124  # conventional; matches GNU `timeout`


@dataclass
class DriverOutcome:
    """Terminal outcome reported when the loop exits."""

    status: str  # "done" | "stalled" | "escalated" | "failed" | "aborted" | "cap"
    plan: str
    final_state: str
    iterations: int
    reason: str = ""
    last_phase: str | None = None
    events: list[dict[str, Any]] = field(default_factory=list)
```

**Lines 180-210**:
```python
        # Stall detection: same state for stall_threshold+ iterations.
        if state == last_state:
            stall_count += 1
            if stall_count >= stall_threshold:
                log(f"stalled at state={state} for {stall_count} iterations")
                return DriverOutcome(
                    status="stalled",
                    plan=plan,
                    final_state=state,
                    iterations=iteration,
                    reason=(
                        f"stalled at '{state}' for {stall_count} iterations — "
                        "manual intervention required"
                    ),
                    last_phase=last_phase,
                    events=events,
                )
        else:
            stall_count = 0
            last_state = state

        # Escalation: no phase to run but overrides are available.
        if not next_step:
            if _has_valid_next(status, "override force-proceed"):
                if on_escalate == "force-proceed":
                    log("gate escalated — force-proceeding (per on_escalate=force-proceed)")
                    code, out, err = _run_megaplan(
                        [
                            "override",
                            "force-proceed",
                            "--plan",
                            plan,
                            "--reason",
                            "megaplan auto: escalate → force-proceed",
                        ],
```

---

### 4. **schemas.py** — Schema definitions for key steps
File: `/Users/user_c042661f/Documents/megaplan/megaplan/schemas.py` (520 lines)

**plan.json** (lines 9-28):
- Properties: `plan`, `questions`, `success_criteria` (with priority enum: `["must", "should", "info"]`), `assumptions`

**revise.json** (lines 83-111):
- Properties: `plan`, `changes_summary`, `flags_addressed`, `assumptions`, `success_criteria` (same priority enum), `questions`

**review.json** (lines 374-499):
- **Lines 431-443** — `criteria` section with **pass enum** (line 438):
  ```python
  "pass": {"type": "string", "enum": ["pass", "fail", "waived"]},
  ```

**critique.json** (lines 171-227):
- **Lines 196-222** — `flags` array with **category enum** (lines 203-212):
  ```python
  "category": {
      "type": "string",
      "enum": [
          "correctness",
          "security",
          "completeness",
          "performance",
          "maintainability",
          "other",
      ],
  },
  ```

---

### 5. **pyproject.toml** — Version line
File: `/Users/user_c042661f/Documents/megaplan/pyproject.toml`

**Line 7** — Version:
```toml
version = "0.16.0"
```

---

### 6. **CHANGELOG.md** — First 30 lines
File: `/Users/user_c042661f/Documents/megaplan/CHANGELOG.md`

```markdown
# Changelog

## v0.16.0 — 2026-04-15

### Chain driver (`megaplan chain`)

New first-class subcommand that drives an ordered pipeline of milestone plans described by a YAML spec. Replaces ad-hoc bash orchestration (`chain.sh`) so plan-state logic lives in megaplan instead of fragile shell polling.

- **Spec-driven**: `megaplan chain --spec path/to/chain.yaml` reads milestones, optional seed plan, and failure/escalate policies from YAML.
- **Resumable**: progress is persisted to `chain_state.json` next to the spec (`current_milestone_index`, `current_plan_name`, `last_state`, `completed`). A relaunched process reads this file and picks up where the previous run stopped.
- **State-aware in the right layer**: each milestone is driven via the existing `megaplan.auto.drive` entry point, so phase selection (`plan → prep → critique → ... → review`) stays in megaplan. Shell wrappers no longer need to classify `next_step`.
- **`megaplan chain status --spec PATH`**: prints current chain progress without driving.
- **Failure/escalate policies**: `stop_chain` (default), `skip_milestone`, `retry_milestone`.
- **Seed handling**: if a seed plan is specified and not already in a terminal state, it is driven first under the same auto loop — fixing the gap where seed plans had no state-aware driver.
- **Validation**: up front, the chain driver checks every idea file exists and the seed plan (if set) resolves under the project root. Structured `invalid_spec` / `missing_idea_file` / `missing_seed_plan` errors.
- **PyYAML** added as a runtime dependency.

### Tests

- `tests/test_chain.py` covers spec parsing, `chain status`, idea-file validation, seed-plan validation, happy-path execution (with `auto.drive` mocked), resume-from-`chain_state.json`, and on-failure `stop_chain`.

## v0.14.0 — 2026-04-15
```

---

### 7. **handlers.py** — Lines 1-30 (imports)
File: `/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py`

```python
from __future__ import annotations

import argparse
import inspect
import logging
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import megaplan.review_checks as review_checks
import megaplan.workers as worker_module
from megaplan.checks import checks_for_robustness, validate_critique_checks
from megaplan.execution import (
    _check_done_task_evidence,
    build_monitor_hint,
    handle_execute_auto_loop as dispatch_execute_auto_loop,
    handle_execute_one_batch as dispatch_execute_one_batch,
)
from megaplan.flags import (
    update_flags_after_critique,
    update_flags_after_gate,
    update_flags_after_review,
    update_flags_after_revise,
)
```

**Note**: `DEFAULT_AGENT_ROUTING` does **not** exist in `handlers.py` — it's defined in `types.py` (lines 267-278) and imported from there in `cli.py` and `workers.py`.
