> DEVELOPER

Explore /Users/user_c042661f/Documents/megaplan to map out how the "make a plan" process works. I want to understand the discrete steps in the planning pipeline (e.g. plan generation, critique, revise, review, etc.) and how they're composed today.

Focus on:
1. The top-level pipeline orchestrator — what file/function runs `megaplan plan` end-to-end? Look in megaplan/cli.py, megaplan/chain.py, megaplan/handlers/, megaplan/agent/.
2. The discrete steps in the pipeline — identify each one (planner, critic, reviser, reviewer, judge, tiebreaker, etc.). For each, note: what file it lives in, what its inputs and outputs are (data shapes / artifacts), and how it's currently invoked.
3. How critiques work specifically — look at megaplan/parallel_critique.py and any review/ folder. What does a critique produce? How is it consumed downstream?
4. How the steps are wired together right now — is it a hardcoded sequence, a graph, configurable via profiles? Look at megaplan/profiles and megaplan/chain.py.
5. Robustness levels — how do different robustness/quality levels change which steps run? Quick mention only.
6. What "composability" obstacles exist today — e.g. shared state passed implicitly, steps that assume specific predecessors, types that aren't unified, hardcoded ordering.

Return a structured report (under 600 words) with: (a) the list of primitive steps and their I/O, (b) where the orchestration logic lives, (c) the top 3-5 things that block free composition of these steps into arbitrary workflows.

This is research only — no code changes.

> AGENT

I'll explore the megaplan repository to understand the "make a plan" process and how the pipeline is orchestrated.

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan -type f -name \"*.py\" | grep -E \"(cli|chain|handler|agent|pipeline)\" | head -20"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/chain.py
/Users/user_c042661f/Documents/megaplan/megaplan/cli.py
/Users/user_c042661f/Documents/megaplan/tests/test_cloud_cli_session.py
/Users/user_c042661f/Documents/megaplan/tests/test_cloud_chain_wrapper.py
/Users/user_c042661f/Documents/megaplan/tests/test_cloud_chain_status.py
/Users/user_c042661f/Documents/megaplan/tests/test_cli_entry.py
/Users/user_c042661f/Documents/megaplan/tests/test_chain.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/batch_runner.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/hermes_constants.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/toolset_distributions.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/run_agent.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/rl_cli.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/toolsets.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/__init__.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/mini_swe_runner.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/hermes_time.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/cli.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/utils.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/trajectory_compressor.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/hermes_state.py
```

> AGENT

Let me explore the directory structure and key files:

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/megaplan/ | grep -E \"\\.py$|^d\""
}
```

> TOOL

tool_result Bash
```
drwxr-xr-x  39 user_c042661f  staff   1248 May  2 18:37 .
drwxr-xr-x  31 user_c042661f  staff    992 May  2 18:37 ..
-rw-r--r--   1 user_c042661f  staff   2640 Apr 10 21:54 __init__.py
-rw-r--r--   1 user_c042661f  staff    105 Mar 20 16:07 __main__.py
drwxr-xr-x@ 31 user_c042661f  staff    992 May  2 01:37 __pycache__
drwxr-xr-x  10 user_c042661f  staff    320 May  2 01:34 _core
drwxr-xr-x  63 user_c042661f  staff   2016 May  2 01:44 agent
-rw-r--r--   1 user_c042661f  staff   4885 May  2 01:35 audit.py
drwxr-xr-x  11 user_c042661f  staff    352 May  2 01:34 audits
-rw-r--r--   1 user_c042661f  staff  36985 May  2 01:34 auto.py
drwxr-xr-x@ 15 user_c042661f  staff    480 May  2 01:34 bakeoff
-rw-r--r--   1 user_c042661f  staff   1975 May  2 01:35 capabilities.py
-rw-r--r--@  1 user_c042661f  staff  25550 Apr 21 12:54 chain.py
-rw-r--r--   1 user_c042661f  staff  58628 May  2 01:36 cli.py
drwxr-xr-x@ 11 user_c042661f  staff    352 May  2 22:39 cloud
drwxr-xr-x   5 user_c042661f  staff    160 May  2 01:34 data
-rw-r--r--   1 user_c042661f  staff   9418 Apr 21 12:33 doc_assembly.py
-rw-r--r--   1 user_c042661f  staff  29354 May  2 01:34 evaluation.py
drwxr-xr-x   8 user_c042661f  staff    256 May  2 01:34 execute
-rw-r--r--   1 user_c042661f  staff    472 May  2 01:37 execution_timeout.py
-rw-r--r--@  1 user_c042661f  staff   8132 Apr 22 03:32 flags.py
drwxr-xr-x@  9 user_c042661f  staff    288 May  2 01:34 forms
drwxr-xr-x@ 15 user_c042661f  staff    480 May  2 01:34 handlers
-rw-r--r--   1 user_c042661f  staff  38397 May  2 01:34 hermes_worker.py
-rw-r--r--   1 user_c042661f  staff   5947 May  2 01:35 iteration_pressure.py
-rw-r--r--   1 user_c042661f  staff  10898 May  2 01:34 key_pool.py
drwxr-xr-x@  9 user_c042661f  staff    288 May  1 06:29 loop
-rw-r--r--   1 user_c042661f  staff  10323 Apr 23 20:31 parallel_critique.py
drwxr-xr-x@ 10 user_c042661f  staff    320 May  2 01:34 profiles
drwxr-xr-x@ 26 user_c042661f  staff    832 May  2 01:35 prompts
drwxr-xr-x@ 10 user_c042661f  staff    320 May  2 01:34 receipts
drwxr-xr-x   7 user_c042661f  staff    224 May  1 06:29 review
-rw-r--r--   1 user_c042661f  staff  31850 May  3 00:13 schemas.py
-rw-r--r--   1 user_c042661f  staff  10447 May  2 01:34 step_edit.py
-rw-r--r--   1 user_c042661f  staff  10894 May  2 01:35 tiebreaker.py
-rw-r--r--   1 user_c042661f  staff   9410 May  2 01:34 types.py
-rw-r--r--   1 user_c042661f  staff   4462 May  2 01:35 verifiability.py
-rw-r--r--   1 user_c042661f  staff  79806 May  3 00:13 workers.py
```

> AGENT

Now let me read the key orchestration files:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/cli.py",
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
37	    is_prose_mode,
38	    json_dump,
39	    load_config,
40	    load_debt_registry,
41	    load_plan,
42	    plan_lock_is_held,
43	    read_json,
44	    resolve_debt,
45	    resolve_plan_dir,
46	    save_debt_registry,
47	    save_config,
48	    subsystem_occurrence_total,
49	    humanize_seconds,
50	)
51	from megaplan.execute.core import build_monitor_hint
52	from megaplan.forms import available_form_ids
53	from megaplan.handlers import (
54	    handle_audit_verifiability,
55	    handle_critique,
56	    handle_execute,
57	    handle_finalize,
58	    handle_gate,
59	    handle_init,
60	    handle_override,
61	    handle_plan,
62	    handle_prep,
63	    handle_review,
64	    handle_revise,
65	    handle_tiebreaker_run,
66	    handle_verify_human,
67	)
68	from megaplan.loop.handlers import (
69	    handle_loop_init,
70	    handle_loop_pause,
71	    handle_loop_run,
72	    handle_loop_status,
73	)
74	from megaplan.profiles import (
75	    load_profile_sources,
76	    load_profiles,
77	    resolve_profile,
78	)
79	from megaplan.step_edit import handle_step
80	
81	
82	def render_response(response: StepResponse, *, exit_code: int = 0) -> int:
83	    if isinstance(response, str):
84	        print(response, end="")
85	        return exit_code
86	    print(json_dump(response), end="")
87	    return exit_code
88	
89	
90	def _resolve_error_plan_dir(root: Path | None, error: CliError) -> Path | None:
91	    if root is None or error.code != "plan_locked" or not isinstance(error.extra, dict):
92	        return None
93	    plan_name = error.extra.get("plan")
94	    if not isinstance(plan_name, str) or not plan_name:
95	        return None
96	    try:
97	        return resolve_plan_dir(root, plan_name)
98	    except CliError:
99	        return None
100
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/chain.py"
}
```

> TOOL

tool_result Read
```
1	"""Chain driver — run a pipeline of milestone plans with state kept in megaplan.
2	
3	This replaces ad-hoc bash orchestration (`chain.sh`). A YAML spec declares an
4	optional seed plan and an ordered list of milestones; each milestone is
5	initialized from an idea file, then driven to `done` via the same auto-loop
6	entry point used by `megaplan auto`.
7	
8	Plan state stays in megaplan. Bash is no longer responsible for polling or
9	deciding the next step — only for process/container liveness.
10	
11	Spec format (YAML)::
12	
13	    seed:
14	      plan: milestone-m0-from-docs-state-20260415-0217
15	    milestones:
16	      - label: m1
17	        idea: /workspace/ideas/M1-foundation-store.txt
18	        branch: megaplan/m1-foundation-store   # optional, currently informational
19	      - label: m1a
20	        idea: /workspace/ideas/M1a-settings-store.txt
21	    on_failure:
22	      abort: stop_chain          # stop_chain | skip_milestone | retry_milestone
23	    on_escalate:
24	      abort: stop_chain          # stop_chain | skip_milestone | retry_milestone
25	
26	Progress is persisted to ``chain_state.json`` beside the spec so a relaunched
27	process can resume where the previous run left off.
28	"""
29	from __future__ import annotations
30	
31	import argparse
32	import json
33	import subprocess
34	import sys
35	import time
36	from dataclasses import dataclass, field
37	from pathlib import Path
38	from typing import Any
39	
40	try:
41	    import yaml
42	except ImportError as exc:  # pragma: no cover - import guard
43	    raise RuntimeError(
44	        "megaplan chain requires PyYAML. Install with `pip install pyyaml`."
45	    ) from exc
46	
47	from megaplan.auto import (
48	    DEFAULT_MAX_ITERATIONS,
49	    DEFAULT_PHASE_TIMEOUT_SECONDS,
50	    DEFAULT_POLL_SLEEP_SECONDS,
51	    DEFAULT_STALL_THRESHOLD,
52	    DEFAULT_STATUS_TIMEOUT_SECONDS,
53	    DriverOutcome,
54	    ESCALATE_ACTIONS,
55	    drive as auto_drive,
56	)
57	from megaplan._core import resolve_plan_dir
58	from megaplan.types import CliError
59	
60	
61	VALID_FAILURE_ACTIONS = ("stop_chain", "skip_milestone", "retry_milestone")
62	TERMINAL_SKIP_STATES = ("done", "aborted", "failed")
63	
64	
65	@dataclass
66	class MilestoneSpec:
67	    label: str
68	    idea: str
69	    branch: str | None = None
70	
71	    @classmethod
72	    def from_dict(cls, raw: dict[str, Any], index: int) -> "MilestoneSpec":
73	        if not isinstance(raw, dict):
74	            raise CliError("invalid_spec", f"milestones[{index}] must be a mapping")
75	        label = raw.get("label")
76	        idea = raw.get("idea")
77	        if not isinstance(label, str) or not label.strip():
78	            raise CliError("invalid_spec", f"milestones[{index}].label is required")
79	        if not isinstance(idea, str) or not idea.strip():
80	            raise CliError("invalid_spec", f"milestones[{index}].idea is required")
81	        branch = raw.get("branch")
82	        if branch is not None and not isinstance(branch, str):
83	            raise CliError("invalid_spec", f"milestones[{index}].branch must be a string")
84	        return cls(label=label, idea=idea, branch=branch)
85	
86	
87	@dataclass
88	class ChainSpec:
89	    milestones: list[MilestoneSpec]
90	    seed_plan: str | None = None
91	    on_failure: str = "stop_chain"
92	    on_escalate: str = "stop_chain"
93	    # Driver knobs propagated into auto.drive for each plan.
94	    stall_threshold: int = DEFAULT_STALL_THRESHOLD
95	    max_iterations: int = DEFAULT_MAX_ITERATIONS
96	    poll_sleep: float = DEFAULT_POLL_SLEEP_SECONDS
97	    phase_timeout: float = DEFAULT_PHASE_TIMEOUT_SECONDS
98	    status_timeout: float = DEFAULT_STATUS_TIMEOUT_SECONDS
99	    escalate_action: str = "force-proceed"  # passed to auto.drive on_escalate
100	    robustness: str = "standard"
101	    auto_approve: bool = True
102	
103	    @classmethod
104	    def from_dict(cls, raw: dict[str, Any]) -> "ChainSpec":
105	        if not isinstance(raw, dict):
106	            raise CliError("invalid_spec", "chain spec must be a YAML mapping")
107	        milestones_raw = raw.get("milestones") or []
108	        if not isinstance(milestones_raw, list):
109	            raise CliError("invalid_spec", "`milestones` must be a list")
110	        milestones = [MilestoneSpec.from_dict(m, i) for i, m in enumerate(milestones_raw)]
111	        seed_raw = raw.get("seed") or {}
112	        seed_plan: str | None = None
113	        if seed_raw:
114	            if not isinstance(seed_raw, dict):
115	                raise CliError("invalid_spec", "`seed` must be a mapping")
116	            seed_plan = seed_raw.get("plan")
117	            if seed_plan is not None and not isinstance(seed_plan, str):
118	                raise CliError("invalid_spec", "`seed.plan` must be a string")
119	            if isinstance(seed_plan, str) and not seed_plan.strip():
120	                seed_plan = None
121	
122	        def _action(section: str, default: str) -> str:
123	            block = raw.get(section) or {}
124	            if not isinstance(block, dict):
125	                raise CliError("invalid_spec", f"`{section}` must be a mapping")
126	            value = block.get("abort", default)
127	            if value not in VALID_FAILURE_ACTIONS:
128	                raise CliError(
129	                    "invalid_spec",
130	                    f"{section}.abort must be one of {VALID_FAILURE_ACTIONS}; got {value!r}",
131	                )
132	            return value
133	
134	        on_failure = _action("on_failure", "stop_chain")
135	        on_escalate = _action("on_escalate", "stop_chain")
136	
137	        driver_raw = raw.get("driver") or {}
138	        if not isinstance(driver_raw, dict):
139	            raise CliError("invalid_spec", "`driver` must be a mapping")
140	        stall = int(driver_raw.get("stall_threshold", DEFAULT_STALL_THRESHOLD))
141	        max_iter = int(driver_raw.get("max_iterations", DEFAULT_MAX_ITERATIONS))
142	        poll = float(driver_raw.get("poll_sleep", DEFAULT_POLL_SLEEP_SECONDS))
143	        phase_to = float(driver_raw.get("phase_timeout", DEFAULT_PHASE_TIMEOUT_SECONDS))
144	        status_to = float(driver_raw.get("status_timeout", DEFAULT_STATUS_TIMEOUT_SECONDS))
145	        esc = driver_raw.get("on_escalate", "force-proceed")
146	        if esc not in ESCALATE_ACTIONS:
147	            raise CliError(
148	                "invalid_spec",
149	                f"driver.on_escalate must be one of {ESCALATE_ACTIONS}; got {esc!r}",
150	            )
151	        robustness = driver_raw.get("robustness", "standard")
152	        if not isinstance(robustness, str):
153	            raise CliError("invalid_spec", "driver.robustness must be a string")
154	        auto_approve = bool(driver_raw.get("auto_approve", True))
155	
156	        return cls(
157	            milestones=milestones,
158	            seed_plan=seed_plan,
159	            on_failure=on_failure,
160	            on_escalate=on_escalate,
161	            stall_threshold=stall,
162	            max_iterations=max_iter,
163	            poll_sleep=poll,
164	            phase_timeout=phase_to,
165	            status_timeout=status_to,
166	            escalate_action=esc,
167	            robustness=robustness,
168	            auto_approve=auto_approve,
169	        )
170	
171	
172	@dataclass
173	class ChainState:
174	    """Persisted progress for a chain run.
175	
176	    ``current_milestone_index`` is -1 before any milestone starts (seed phase),
177	    0 for the first milestone, etc. ``current_plan_name`` is the plan currently
178	    being driven. ``last_state`` is the terminal driver status string from the
179	    most recently completed plan.
180	    """
181	
182	    current_milestone_index: int = -1
183	    current_plan_name: str | None = None
184	    last_state: str | None = None
185	    completed: list[dict[str, Any]] = field(default_factory=list)
186	
187	    def to_dict(self) -> dict[str, Any]:
188	        return {
189	            "current_milestone_index": self.current_milestone_index,
190	            "current_plan_name": self.current_plan_name,
191	            "last_state": self.last_state,
192	            "completed": list(self.completed),
193	        }
194	
195	    @classmethod
196	    def from_dict(cls, raw: dict[str, Any]) -> "ChainState":
197	        return cls(
198	            current_milestone_index=int(raw.get("current_milestone_index", -1)),
199	            current_plan_name=raw.get("current_plan_name"),
200	            last_state=raw.get("last_state"),
201	            completed=list(raw.get("completed") or []),
202	        )
203	
204	
205	def _state_path_for(spec_path: Path) -> Path:
206	    return spec_path.with_name("chain_state.json")
207	
208	
209	def load_spec(spec_path: Path) -> ChainSpec:
210	    if not spec_path.exists():
211	        raise CliError("invalid_spec", f"spec file not found: {spec_path}")
212	    try:
213	        raw = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
214	    except yaml.YAMLError as exc:
215	        raise CliError("invalid_spec", f"YAML parse error: {exc}") from exc
216	    return ChainSpec.from_dict(raw or {})
217	
218	
219	def load_chain_state(spec_path: Path) -> ChainState:
220	    state_path = _state_path_for(spec_path)
221	    if not state_path.exists():
222	        return ChainState()
223	    try:
224	        raw = json.loads(state_path.read_text(encoding="utf-8"))
225	    except json.JSONDecodeError as exc:
226	        raise CliError("invalid_chain_state", f"chain_state.json is invalid JSON: {exc}") from exc
227	    if not isinstance(raw, dict):
228	        raise CliError("invalid_chain_state", "chain_state.json must be an object")
229	    return ChainState.from_dict(raw)
230	
231	
232	def save_chain_state(spec_path: Path, state: ChainState) -> None:
233	    state_path = _state_path_for(spec_path)
234	    tmp = state_path.with_suffix(".tmp")
235	    tmp.write_text(json.dumps(state.to_dict(), indent=2) + "\n", encoding="utf-8")
236	    tmp.replace(state_path)
237	
238	
239	def validate_paths(spec: ChainSpec, root: Path) -> None:
240	    """Check that all idea files exist and the seed plan (if any) is on disk."""
241	    for m in spec.milestones:
242	        idea_path = Path(m.idea)
243	        if not idea_path.exists():
244	            raise CliError(
245	                "missing_idea_file",
246	                f"milestone {m.label!r} idea file not found: {m.idea}",
247	            )
248	    if spec.seed_plan:
249	        try:
250	            resolve_plan_dir(root, spec.seed_plan)
251	        except CliError as exc:
252	            raise CliError(
253	                "missing_seed_plan",
254	                f"seed plan {spec.seed_plan!r} not found under {root}: {exc.message}",
255	            ) from exc
256	
257	
258	# ---------------------------------------------------------------------------
259	# Driving
260	# ---------------------------------------------------------------------------
261	
262	
263	def _plan_state(root: Path, plan: str, *, timeout: float) -> str:
264	    """Read just the `state` field of a plan via `megaplan status`.
265	
266	    Returns "missing" if the plan is not found. Used to decide whether to skip
267	    driving (plan already terminal) vs. run the full auto loop.
268	    """
269	    try:
270	        proc = subprocess.run(
271	            [sys.executable, "-m", "megaplan", "status", "--plan", plan],
272	            cwd=str(root),
273	            capture_output=True,
274	            text=True,
275	            check=False,
276	            timeout=timeout,
277	        )
278	    except subprocess.TimeoutExpired:
279	        return "unknown"
280	    if proc.returncode != 0:
281	        return "missing"
282	    try:
283	        return json.loads(proc.stdout).get("state", "unknown")
284	    except json.JSONDecodeError:
285	        return "unknown"
286	
287	
288	def _refresh_main(root: Path, *, writer, no_git_refresh: bool = False) -> None:
289	    """Best-effort `git fetch + checkout main + pull`. Never raises; logs only.
290	
291	    When ``no_git_refresh`` is True, this is a no-op (still logs that it was
292	    skipped). This guard exists so developer checkouts running ``megaplan
293	    chain`` do not get their currently checked-out branch stomped by an
294	    automatic ``git checkout main``.
295	    """
296	    if no_git_refresh:
297	        writer("[chain] skipping git refresh (--no-git-refresh)\n")
298	        return
299	    for cmd in (
300	        ["git", "fetch", "origin", "main"],
301	        ["git", "checkout", "main"],
302	        ["git", "pull", "--ff-only", "origin", "main"],
303	    ):
304	        try:
305	            proc = subprocess.run(
306	                cmd, cwd=str(root), capture_output=True, text=True, check=False, timeout=120
307	            )
308	            writer(f"[chain] {' '.join(cmd)} -> rc={proc.returncode}\n")
309	        except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
310	            writer(f"[chain] {' '.join(cmd)} failed: {exc}\n")
311	
312	
313	def _init_plan(
314	    root: Path,
315	    idea_path: str,
316	    *,
317	    robustness: str,
318	    auto_approve: bool,
319	    writer,
320	) -> str:
321	    """Run `megaplan init --idea-file ...` and return the plan name."""
322	    args = [sys.executable, "-m", "megaplan", "init", "--project-dir", str(root)]
323	    if auto_approve:
324	        args.append("--auto-approve")
325	    args.extend(["--robustness", robustness, "--idea-file", str(idea_path)])
326	    writer(f"[chain] initializing plan from {idea_path}\n")
327	    proc = subprocess.run(
328	        args, cwd=str(root), capture_output=True, text=True, check=False, timeout=300
329	    )
330	    if proc.returncode != 0:
331	        raise CliError(
332	            "init_failed",
333	            f"megaplan init failed (rc={proc.returncode}): "
334	            f"{proc.stderr.strip() or proc.stdout.strip()[-400:]}",
335	        )
336	    try:
337	        payload = json.loads(proc.stdout)
338	    except json.JSONDecodeError as exc:
339	        raise CliError("init_failed", f"megaplan init produced non-JSON output: {exc}") from exc
340	    plan = payload.get("plan")
341	    if not isinstance(plan, str) or not plan:
342	        raise CliError("init_failed", "megaplan init did not return a plan name")
343	    writer(f"[chain] launched plan={plan}\n")
344	    return plan
345	
346	
347	def _drive_plan(
348	    root: Path,
349	    plan: str,
350	    spec: ChainSpec,
351	    *,
352	    writer,
353	) -> DriverOutcome:
354	    """Run the auto driver for a single plan."""
355	    return auto_drive(
356	        plan,
357	        cwd=root,
358	        stall_threshold=spec.stall_threshold,
359	        max_iterations=spec.max_iterations,
360	        on_escalate=spec.escalate_action,
361	        poll_sleep=spec.poll_sleep,
362	        phase_timeout=spec.phase_timeout,
363	        status_timeout=spec.status_timeout,
364	        writer=writer,
365	    )
366	
367	
368	def _handle_outcome(
369	    outcome: DriverOutcome,
370	    *,
371	    spec: ChainSpec,
372	    writer,
373	) -> str:
374	    """Decide the next action given a DriverOutcome.
375	
376	    Returns one of: "advance" (move to next milestone), "stop" (chain halts),
377	    "retry" (re-run the same milestone), "skip" (advance without waiting).
378	    """
379	    status = outcome.status
380	    if status == "done":
381	        return "advance"
382	    if status == "aborted":
383	        # auto.drive returns aborted both for user aborts and on-escalate=abort.
384	        # Treat according to on_escalate policy so the chain can skip if asked.
385	        writer(f"[chain] plan {outcome.plan} ended aborted\n")
386	        policy = spec.on_escalate
387	    elif status == "escalated":
388	        writer(f"[chain] plan {outcome.plan} escalated — applying on_escalate policy\n")
389	        policy = spec.on_escalate
390	    else:
391	        # failed, stalled, cap → treat as failure
392	        writer(f"[chain] plan {outcome.plan} ended {status}: {outcome.reason}\n")
393	        policy = spec.on_failure
394	    if policy == "stop_chain":
395	        return "stop"
396	    if policy == "skip_milestone":
397	        return "skip"
398	    if policy == "retry_milestone":
399	        return "retry"
400	    return "stop"
401	
402	
403	def run_chain(
404	    spec_path: Path,
405	    root: Path,
406	    *,
407	    writer=sys.stdout.write,
408	    no_git_refresh: bool = False,
409	) -> dict[str, Any]:
410	    """Drive the full chain. Returns a structured JSON-serializable result."""
411	    spec = load_spec(spec_path)
412	    validate_paths(spec, root)
413	    state = load_chain_state(spec_path)
414	
415	    events: list[dict[str, Any]] = []
416	
417	    def log(msg: str, **fields: Any) -> None:
418	        events.append({"msg": msg, **fields})
419	        writer(f"[chain] {msg}\n")
420	
421	    # ---- Seed phase ----
422	    if spec.seed_plan and state.current_milestone_index < 0:
423	        seed_state = _plan_state(root, spec.seed_plan, timeout=spec.status_timeout)
424	        log(f"seed plan {spec.seed_plan} state={seed_state}")
425	        if seed_state not in TERMINAL_SKIP_STATES:
426	            state.current_plan_name = spec.seed_plan
427	            save_chain_state(spec_path, state)
428	            outcome = _drive_plan(root, spec.seed_plan, spec, writer=writer)
429	            state.last_state = outcome.status
430	            save_chain_state(spec_path, state)
431	            decision = _handle_outcome(outcome, spec=spec, writer=writer)
432	            if decision == "stop":
433	                return _result("stopped", state, events, reason=f"seed plan {outcome.status}")
434	            if decision == "retry":
435	                # Recursive retry kept simple: re-drive seed once.
436	                outcome = _drive_plan(root, spec.seed_plan, spec, writer=writer)
437	                state.last_state = outcome.status
438	                save_chain_state(spec_path, state)
439	                if outcome.status != "done":
440	                    return _result("stopped", state, events, reason="seed retry failed")
441	            # skip / advance both proceed to milestones
442	        state.completed.append(
443	            {"label": "seed", "plan": spec.seed_plan, "status": state.last_state or seed_state}
444	        )
445	        state.current_milestone_index = 0
446	        state.current_plan_name = None
447	        save_chain_state(spec_path, state)
448	
449	    elif state.current_milestone_index < 0:
450	        state.current_milestone_index = 0
451	        save_chain_state(spec_path, state)
452	
453	    # ---- Milestones ----
454	    idx = max(state.current_milestone_index, 0)
455	    while idx < len(spec.milestones):
456	        milestone = spec.milestones[idx]
457	        log(f"milestone {milestone.label} starting")
458	
459	        # Resume mid-milestone if we already have a plan name recorded.
460	        if (
461	            state.current_plan_name
462	            and state.current_milestone_index == idx
463	            and _plan_state(root, state.current_plan_name, timeout=spec.status_timeout)
464	            not in ("missing",)
465	        ):
466	            plan_name = state.current_plan_name
467	            log(f"resuming existing plan {plan_name} for {milestone.label}")
468	        else:
469	            _refresh_main(root, writer=writer, no_git_refresh=no_git_refresh)
470	            plan_name = _init_plan(
471	                root,
472	                milestone.idea,
473	                robustness=spec.robustness,
474	                auto_approve=spec.auto_approve,
475	                writer=writer,
476	            )
477	            state.current_milestone_index = idx
478	            state.current_plan_name = plan_name
479	            save_chain_state(spec_path, state)
480	
481	        outcome = _drive_plan(root, plan_name, spec, writer=writer)
482	        state.last_state = outcome.status
483	        save_chain_state(spec_path, state)
484	        decision = _handle_outcome(outcome, spec=spec, writer=writer)
485	
486	        if decision == "stop":
487	            return _result(
488	                "stopped",
489	                state,
490	                events,
491	                reason=f"milestone {milestone.label} ended {outcome.status}",
492	            )
493	        if decision == "retry":
494	            log(f"retrying milestone {milestone.label}")
495	            state.current_plan_name = None  # force re-init next loop
496	            save_chain_state(spec_path, state)
497	            continue
498	        # advance or skip
499	        state.completed.append(
500	            {"label": milestone.label, "plan": plan_name, "status": outcome.status}
501	        )
502	        idx += 1
503	        state.current_milestone_index = idx
504	        state.current_plan_name = None
505	        save_chain_state(spec_path, state)
506	
507	    log("all milestones complete")
508	    return _result("done", state, events)
509	
510	
511	def _result(
512	    status: str, state: ChainState, events: list[dict[str, Any]], *, reason: str = ""
513	) -> dict[str, Any]:
514	    return {
515	        "status": status,
516	        "reason": reason,
517	        "chain_state": state.to_dict(),
518	        "events": events,
519	    }
520	
521	
522	def format_chain_status(spec: ChainSpec, state: ChainState) -> dict[str, Any]:
523	    completed_labels = {
524	        entry.get("label")
525	        for entry in state.completed
526	        if isinstance(entry, dict) and isinstance(entry.get("label"), str)
527	    }
528	    current_milestone: dict[str, Any] | None = None
529	    if 0 <= state.current_milestone_index < len(spec.milestones):
530	        milestone = spec.milestones[state.current_milestone_index]
531	        current_milestone = {
532	            "label": milestone.label,
533	            "index": state.current_milestone_index,
534	        }
535	
536	    per_milestone: list[dict[str, Any]] = []
537	    completed: list[dict[str, Any]] = []
538	    remaining: list[dict[str, Any]] = []
539	    for index, milestone in enumerate(spec.milestones):
540	        if milestone.label in completed_labels:
541	            status = "completed"
542	        elif index == state.current_milestone_index and state.current_plan_name:
543	            status = "in_progress"
544	        else:
545	            status = "pending"
546	        entry = {"label": milestone.label, "index": index, "status": status}
547	        per_milestone.append(entry)
548	        if status == "completed":
549	            completed.append({"label": milestone.label, "index": index})
550	        else:
551	            remaining.append({"label": milestone.label, "index": index})
552	
553	    return {
554	        "current_milestone": current_milestone,
555	        "completed": completed,
556	        "remaining": remaining,
557	        "per_milestone": per_milestone,
558	        "seed_plan": spec.seed_plan,
559	        "current_plan_name": state.current_plan_name,
560	        "last_state": state.last_state,
561	    }
562	
563	
564	def _write_chain_status_pretty(summary: dict[str, Any], *, writer) -> None:
565	    current = summary.get("current_milestone")
566	    current_label = "none"
567	    if isinstance(current, dict):
568	        current_label = f"{current['label']} (index {current['index']})"
569	    completed = summary.get("completed") or []
570	    remaining = summary.get("remaining") or []
571	    completed_labels = ", ".join(item["label"] for item in completed) if completed else "none"
572	    remaining_labels = ", ".join(item["label"] for item in remaining) if remaining else "none"
573	    writer(f"Current milestone: {current_label}\n")
574	    writer(f"Completed: {completed_labels}\n")
575	    writer(f"Remaining: {remaining_labels}\n")
576	    if summary.get("seed_plan"):
577	        writer(f"Seed plan: {summary['seed_plan']}\n")
578	    if summary.get("current_plan_name"):
579	        writer(f"Current plan: {summary['current_plan_name']}\n")
580	    if summary.get("last_state"):
581	        writer(f"Last state: {summary['last_state']}\n")
582	    writer("Per-milestone:\n")
583	    for item in summary.get("per_milestone") or []:
584	        writer(f"  - [{item['status']}] {item['label']} (index {item['index']})\n")
585	
586	
587	# ---------------------------------------------------------------------------
588	# CLI plumbing
589	# ---------------------------------------------------------------------------
590	
591	
592	def build_chain_parser(subparsers: Any) -> None:
593	    chain_parser = subparsers.add_parser(
594	        "chain",
595	        help="Drive a pipeline of milestone plans described by a YAML spec",
596	    )
597	    chain_sub = chain_parser.add_subparsers(dest="chain_action")
598	    # No action == run. `start` is the explicit spelling, kept in sync with the
599	    # backcompat top-level alias.
600	    chain_parser.add_argument(
601	        "--spec",
602	        required=False,
603	        help="Path to the chain spec YAML (required at top-level or on subcommands)",
604	    )
605	    chain_parser.add_argument(
606	        "--no-git-refresh",
607	        action="store_true",
608	        help=(
609	            "Skip the automatic `git checkout main && git pull` that runs "
610	            "before each milestone. Use this on developer checkouts where "
611	            "you do not want chain to stomp on the currently checked-out "
612	            "branch. Default: refresh enabled (preserves CI/orchestrator "
613	            "behavior)."
614	        ),
615	    )
616	
617	    start_parser = chain_sub.add_parser("start", help="Drive a chain spec")
618	    start_parser.add_argument("--spec", required=True, help="Path to the chain spec YAML")
619	    start_parser.add_argument(
620	        "--no-git-refresh",
621	        action="store_true",
622	        help=(
623	            "Skip the automatic `git checkout main && git pull` that runs "
624	            "before each milestone."
625	        ),
626	    )
627	
628	    status_parser = chain_sub.add_parser(
629	        "status", help="Show persisted chain progress without driving"
630	    )
631	    status_parser.add_argument("--spec", required=True, help="Path to the chain spec YAML")
632	
633	
634	def run_chain_cli(root: Path, args: argparse.Namespace, *, writer=sys.stderr.write) -> int:
635	    action = getattr(args, "chain_action", None)
636	    spec_arg = getattr(args, "spec", None)
637	    if not spec_arg:
638	        sys.stderr.write("megaplan chain: --spec is required\n")
639	        return 64
640	    spec_path = Path(spec_arg).expanduser().resolve()
641	
642	    if action == "status":
643	        try:
644	            spec = load_spec(spec_path)
645	            chain_state = load_chain_state(spec_path)
646	        except CliError as exc:
647	            return _emit_error(exc)
648	        summary = format_chain_status(spec, chain_state)
649	        _write_chain_status_pretty(summary, writer=writer)
650	        payload = {
651	            "success": True,
652	            "spec": str(spec_path),
653	            "milestone_count": len(spec.milestones),
654	            "seed_plan": spec.seed_plan,
655	            "chain_state": chain_state.to_dict(),
656	            "summary": summary,
657	        }
658	        sys.stdout.write(json.dumps(payload, indent=2) + "\n")
659	        return 0
660	
661	    if action not in (None, "start"):
662	        return _emit_error(CliError("invalid_args", f"Unknown chain action: {action}"))
663	
664	    no_git_refresh = bool(getattr(args, "no_git_refresh", False))
665	    try:
666	        result = run_chain(spec_path, root, no_git_refresh=no_git_refresh)
667	    except CliError as exc:
668	        return _emit_error(exc)
669	    sys.stdout.write(json.dumps(result, indent=2) + "\n")
670	    if result["status"] == "done":
671	        return 0
672	    return 1
673	
674	
675	def _emit_error(error: CliError) -> int:
676	    payload = {"success": False, "error": error.code, "message": error.message}
677	    sys.stdout.write(json.dumps(payload, indent=2) + "\n")
678	    return error.exit_code or 1
679
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/megaplan/handlers/"
}
```

> TOOL

tool_result Bash
```
total 336
drwxr-xr-x@ 15 user_c042661f  staff    480 May  2 01:34 .
drwxr-xr-x  39 user_c042661f  staff   1248 May  2 18:37 ..
-rw-r--r--   1 user_c042661f  staff   2521 Apr 21 17:59 __init__.py
drwxr-xr-x@ 26 user_c042661f  staff    832 May  2 01:36 __pycache__
-rw-r--r--   1 user_c042661f  staff  19459 May  2 01:34 critique.py
-rw-r--r--   1 user_c042661f  staff   7795 May  2 01:34 execute.py
-rw-r--r--   1 user_c042661f  staff  18709 May  2 01:34 finalize.py
-rw-r--r--   1 user_c042661f  staff  17806 May  2 01:34 gate.py
-rw-r--r--   1 user_c042661f  staff   9346 May  2 01:34 init.py
-rw-r--r--   1 user_c042661f  staff  15363 May  2 01:34 override.py
-rw-r--r--@  1 user_c042661f  staff   6095 Apr 22 03:54 plan.py
-rw-r--r--   1 user_c042661f  staff  26759 May  2 01:34 review.py
-rw-r--r--   1 user_c042661f  staff  12880 May  2 01:34 shared.py
-rw-r--r--@  1 user_c042661f  staff   6681 Apr 23 21:18 tiebreaker.py
-rw-r--r--   1 user_c042661f  staff   4893 May  2 01:34 verifiability.py
```

> AGENT

Now let me examine the handlers and understand the pipeline steps:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers/plan.py"
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	import argparse
4	from pathlib import Path
5	from typing import Any
6	
7	from megaplan import handlers as _pkg
8	from megaplan.types import CliError, STATE_INITIALIZED, STATE_PLANNED, STATE_PREPPED, StepResponse
9	from megaplan._core import load_plan_locked, require_state
10	
11	from .shared import (
12	    _finish_step,
13	    _merge_imported_decision_criteria,
14	    _write_json_artifact,
15	    _write_plan_version,
16	)
17	
18	def handle_plan(root: Path, args: argparse.Namespace) -> StepResponse:
19	    with load_plan_locked(root, args.plan, step="plan") as (plan_dir, state):
20	        require_state(state, "plan", {STATE_INITIALIZED, STATE_PREPPED, STATE_PLANNED})
21	        if state["config"].get("mode") == "joke" and not state["config"].get("primary_criterion"):
22	            raise CliError(
23	                "invalid_state",
24	                "joke mode requires a primary_criterion — declare via --primary-criterion or in the prep brief",
25	            )
26	        rerun = state["current_state"] == STATE_PLANNED
27	        version = state["iteration"] if rerun else state["iteration"] + 1
28	        worker, agent, mode, refreshed = _pkg._run_worker(
29	            "plan",
30	            state,
31	            plan_dir,
32	            args,
33	            root=root,
34	            iteration=version,
35	        )
36	        payload = worker.payload
37	        payload["success_criteria"] = _merge_imported_decision_criteria(
38	            state,
39	            payload["success_criteria"],
40	        )
41	        plan_filename, meta_filename, meta = _write_plan_version(
42	            plan_dir=plan_dir,
43	            state=state,
44	            step="plan",
45	            version=version,
46	            worker=worker,
47	            plan_text=payload["plan"].rstrip() + "\n",
48	            meta_fields={
49	                "questions": payload["questions"],
50	                "success_criteria": payload["success_criteria"],
51	                "assumptions": payload["assumptions"],
52	            },
53	        )
54	        state["iteration"], state["current_state"] = version, STATE_PLANNED
55	        state["meta"].pop("user_approved_gate", None)
56	        state["last_gate"] = {}
57	        state["plan_versions"].append({
58	            "version": version, "file": plan_filename,
59	            "hash": meta["hash"], "timestamp": meta["timestamp"],
60	        })
61	        verb = "Refined" if rerun else "Generated"
62	        return _finish_step(
63	            plan_dir, state, args,
64	            step="plan",
65	            worker=worker, agent=agent, mode=mode, refreshed=refreshed,
66	            summary=f"{verb} plan v{version} with {len(payload['questions'])} questions and {len(payload['success_criteria'])} success criteria.",
67	            artifacts=[plan_filename, meta_filename],
68	            output_file=plan_filename,
69	            artifact_hash=meta["hash"],
70	            response_fields={
71	                "iteration": version,
72	                "questions": payload["questions"],
73	                "assumptions": payload["assumptions"],
74	                "success_criteria": payload["success_criteria"],
75	            },
76	        )
77	
78	def handle_prep(root: Path, args: argparse.Namespace) -> StepResponse:
79	    with load_plan_locked(root, args.plan, step="prep") as (plan_dir, state):
80	        require_state(state, "prep", {STATE_INITIALIZED})
81	        worker, agent, mode, refreshed = _pkg._run_worker("prep", state, plan_dir, args, root=root)
82	        prep_filename = "prep.json"
83	        artifact_hash = _write_json_artifact(plan_dir, prep_filename, worker.payload)
84	        if state["config"].get("mode") == "joke" and not state["config"].get("primary_criterion"):
85	            primary_criterion = worker.payload.get("primary_criterion")
86	            if isinstance(primary_criterion, str) and primary_criterion.strip():
87	                state["config"]["primary_criterion"] = primary_criterion.strip()
88	        code_refs = len(worker.payload.get("relevant_code", []))
89	        test_refs = len(worker.payload.get("test_expectations", []))
90	        state["current_state"] = STATE_PREPPED
91	        return _finish_step(
92	            plan_dir, state, args,
93	            step="prep",
94	            worker=worker, agent=agent, mode=mode, refreshed=refreshed,
95	            summary=f"Prep complete: captured {code_refs} relevant code reference(s) and {test_refs} test expectation(s).",
96	            artifacts=[prep_filename],
97	            output_file=prep_filename,
98	            artifact_hash=artifact_hash,
99	            response_fields={"iteration": state["iteration"]},
100	        )
101	
102	def _build_verifiability_flags(
103	    success_criteria: list[dict[str, Any]],
104	    worker_caps: dict[str, set[str]],
105	) -> list[dict[str, Any]]:
106	    from megaplan.audits.capabilities import ALL_CAPABILITIES
107	    from megaplan.audits.verifiability import audit_criteria, validate_requires
108	
109	    flags: list[dict[str, Any]] = []
110	    issues = validate_requires(success_criteria)
111	    for issue_str in issues:
112	        is_unknown_cap = "unknown capability" in issue_str
113	        flags.append({
114	            "id": f"verifiability-{len(flags)}",
115	            "concern": issue_str,
116	            "category": "verifiability",
117	            "severity_hint": "likely-significant" if is_unknown_cap else "likely-minor",
118	            "status": "open",
119	        })
120	
121	    audits = audit_criteria(success_criteria, worker_caps)
122	    for audit in audits:
123	        if audit.verdict == "unverifiable_no_worker":
124	            flags.append({
125	                "id": f"verifiability-{len(flags)}",
126	                "concern": f"Criterion {audit.criterion_idx}: {audit.rationale} Missing: {', '.join(audit.missing_caps)}",
127	                "category": "verifiability",
128	                "severity_hint": "likely-significant",
129	                "status": "open",
130	            })
131	        elif audit.verdict == "human_only":
132	            flags.append({
133	                "id": f"verifiability-{len(flags)}",
134	                "concern": f"Criterion {audit.criterion_idx}: requires human verification ({', '.join(audit.missing_caps)}).",
135	                "category": "verifiability",
136	                "severity_hint": "likely-minor",
137	                "status": "open",
138	            })
139	
140	    return flags
141
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers/critique.py",
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	import argparse
4	import sys
5	from pathlib import Path
6	from typing import Any
7	
8	from megaplan import handlers as _pkg
9	from megaplan.audits.robustness import validate_critique_checks
10	from megaplan.forms.provocations import select_active_checks
11	from megaplan.forms.directors_notes import update_directors_notes_at_aggregate
12	from megaplan.evaluation import build_gate_artifact, build_orchestrator_guidance, compute_plan_delta_percent, compute_recurring_critiques
13	from megaplan.parallel_critique import run_parallel_critique
14	from megaplan.profiles import apply_profile_expansion
15	from megaplan.types import (
16	    FLAG_BLOCKING_STATUSES,
17	    PlanState,
18	    STATE_CRITIQUED,
19	    STATE_GATED,
20	    STATE_PLANNED,
21	    STATE_TIEBREAKER_PENDING,
22	    StepResponse,
23	)
24	from megaplan.workers import WorkerResult, validate_payload
25	from megaplan._core import (
26	    atomic_write_json,
27	    configured_robustness,
28	    is_creative_mode,
29	    latest_plan_meta_path,
30	    latest_plan_path,
31	    load_plan_locked,
32	    now_utc,
33	    read_json,
34	    require_state,
35	    save_flag_registry,
36	    scope_creep_flags,
37	    sha256_file,
38	    workflow_includes_step,
39	)
40	
41	from .plan import _build_verifiability_flags, _merge_imported_decision_criteria
42	from .shared import _append_to_meta, _finish_step, _raise_step_validation_error, _write_plan_version
43	from .tiebreaker import _build_tiebreaker_reprompt
44	
45	def handle_critique(root: Path, args: argparse.Namespace) -> StepResponse:
46	    with load_plan_locked(root, args.plan, step="critique") as (plan_dir, state):
47	        require_state(state, "critique", {STATE_PLANNED})
48	        apply_profile_expansion(args, Path(state["config"]["project_dir"]), state=state)
49	        iteration = state["iteration"]
50	        robustness = configured_robustness(state)
51	        state["last_gate"] = {}
52	        critique_filename = f"critique_v{iteration}.json"
53	        if robustness == "tiny":
54	            from megaplan.audits.capabilities import get_worker_capabilities
55	            from megaplan.audits.verifiability import audit_criteria, validate_requires
56	
57	            plan_meta = read_json(latest_plan_meta_path(plan_dir, state))
58	            success_criteria = plan_meta.get("success_criteria", [])
59	            worker_caps = get_worker_capabilities(state)
60	
61	            verifiability_flags = _build_verifiability_flags(success_criteria, worker_caps)
62	
63	            stub_critique = {
64	                "checks": [],
65	                "flags": verifiability_flags,
66	                "verified_flag_ids": [],
67	                "disputed_flag_ids": [],
68	            }
69	            validate_payload("critique", stub_critique)
70	            atomic_write_json(plan_dir / critique_filename, stub_critique)
71	            save_flag_registry(plan_dir, {"flags": verifiability_flags})
72	            minimal_gate: dict[str, Any] = {
73	                "recommendation": "ITERATE",
74	                "rationale": "Tiny robustness: critique stubbed; advancing directly to gated.",
75	                "signals_assessment": "",
76	                "warnings": [],
77	                "settled_decisions": [],
78	            }
79	            atomic_write_json(plan_dir / "gate.json", minimal_gate)
80	            state["last_gate"] = {"recommendation": "ITERATE"}
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers/review.py",
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	import argparse
4	import logging
5	import os
6	from pathlib import Path
7	from typing import Any
8	
9	from megaplan import handlers as _pkg
10	from megaplan.review import checks as review_checks
11	from megaplan.execute.core import _check_done_task_evidence, build_monitor_hint
12	from megaplan.evaluation import is_rubber_stamp
13	from megaplan.execute.merge import _validate_and_merge_batch
14	from megaplan.prompts import create_claude_prompt, create_codex_prompt, create_hermes_prompt
15	from megaplan.profiles import apply_profile_expansion
16	from megaplan.receipts import build_receipt
17	from megaplan.receipts.writer import write_receipt
18	from megaplan.types import (
19	    MOCK_ENV_VAR,
20	    CliError,
21	    PlanState,
22	    STATE_AWAITING_HUMAN,
23	    STATE_DONE,
24	    STATE_EXECUTED,
25	    STATE_FINALIZED,
26	    StepResponse,
27	)
28	from megaplan.workers import (
29	    WorkerResult,
30	    validate_payload,
31	    warn_if_work_dir_differs_from_project_dir,
32	)
33	from megaplan._core import (
34	    append_history,
35	    apply_session_update,
36	    atomic_write_json,
37	    atomic_write_text,
38	    clear_active_step,
39	    configured_robustness,
40	    get_effective,
41	    is_prose_mode,
42	    is_creative_mode,
43	    load_plan_locked,
44	    make_history_entry,
45	    now_utc,
46	    read_json,
47	    record_step_failure,
48	    render_final_md,
49	    require_state,
50	    save_state,
51	    save_state_merge_meta,
52	    set_active_step,
53	    sha256_file,
54	)
55	
56	from .shared import (
57	    _attach_next_step_runtime,
58	    _emit_phase_notice,
59	    _run_worker,
60	    _supports_prompt_kwargs,
61	    attach_agent_fallback,
62	    worker_module,
63	)
64	
65	log = logging.getLogger(__name__)
66	
67	
68	def _build_review_blocked_message(
69	    *,
70	    verdict_count: int,
71	    total_tasks: int,
72	    check_count: int,
73	    total_checks: int,
74	    missing_reviewer_evidence: list[str],
75	) -> str:
76	    if missing_reviewer_evidence:
77	        return (
78	            "Blocked: done tasks are missing reviewer evidence_files without a substantive reviewer_verdict ("
79	            + ", ".join(missing_reviewer_evidence)
80	            + "). Re-run review to complete."
```

> AGENT

Now let me explore the auto.py and parallel_critique to understand the orchestration better:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/auto.py",
  "limit": 120
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
20	import os
21	import subprocess
22	import sys
23	import tempfile
24	import time
25	from dataclasses import dataclass, field
26	from pathlib import Path
27	from typing import Any
28	
29	from megaplan.types import (
30	    AUTOMATION_TERMINAL_STATES,
31	    STATE_AWAITING_HUMAN,
32	    STATE_TIEBREAKER_PENDING,
33	    STATE_TIEBREAKER_READY,
34	)
35	
36	
37	DEFAULT_STALL_THRESHOLD = 5
38	DEFAULT_MAX_ITERATIONS = 200
39	DEFAULT_POLL_SLEEP_SECONDS = 1.0
40	DEFAULT_PHASE_TIMEOUT_SECONDS = 3600
41	DEFAULT_STATUS_TIMEOUT_SECONDS = 60
42	DEFAULT_MAX_CONTEXT_RETRIES = 2
43	CONTEXT_EXHAUSTION_FRAGMENT = "ran out of room in the model's context"
44	# When execute exits 0 but state.json's latest execute entry is `result=blocked`,
45	# the executor reported success-with-evidence-gaps (e.g. done tasks missing
46	# files_changed/commands_run). Retrying the same execute is structurally pointless
47	# — the model returned that shape — so we cap retries low and fail fast.
48	DEFAULT_MAX_BLOCKED_RETRIES = 1
49	# Cap on review→rework cycles before the driver bails. This mirrors the
50	# `execution.max_review_rework_cycles` config the review handler enforces
51	# internally (default 3); the auto-driver applies its own cap so that an
52	# unexpected-config or mis-routed rework loop cannot spin indefinitely.
53	DEFAULT_MAX_REVIEW_REWORK_CYCLES = 3
54	ESCALATE_ACTIONS = ("force-proceed", "abort", "fail")
55	PHASE_TIMEOUT_EXIT_CODE = 124  # conventional; matches GNU `timeout`
56	
57	
58	@dataclass
59	class DriverOutcome:
60	    """Terminal outcome reported when the loop exits."""
61	
62	    status: str  # "done" | "stalled" | "escalated" | "failed" | "aborted" | "cap" | "blocked" | "cost_cap_exceeded" | "context_retry_exhausted" | "worker_blocked" | "human_required"
63	    plan: str
64	    final_state: str
65	    iterations: int
66	    reason: str = ""
67	    last_phase: str | None = None
68	    events: list[dict[str, Any]] = field(default_factory=list)
69	    total_cost_usd: float | None = None
70	    cost_cap_usd: float | None = None
71	    context_retries_used: int = 0
72	    max_context_retries: int | None = None
73	    blocked_retries_used: int = 0
74	    max_blocked_retries: int | None = None
75	    blocking_reasons: list[str] = field(default_factory=list)
76	
77	    def to_json(self) -> str:
78	        return json.dumps(
79	            {
80	                "status": self.status,
81	                "plan": self.plan,
82	                "final_state": self.final_state,
83	                "iterations": self.iterations,
84	                "reason": self.reason,
85	                "last_phase": self.last_phase,
86	                "events": self.events,
87	                "total_cost_usd": self.total_cost_usd,
88	                "cost_cap_usd": self.cost_cap_usd,
89	                "context_retries_used": self.context_retries_used,
90	                "max_context_retries": self.max_context_retries,
91	                "blocked_retries_used": self.blocked_retries_used,
92	                "max_blocked_retries": self.max_blocked_retries,
93	                "blocking_reasons": self.blocking_reasons,
94	            },
95	            indent=2,
96	        )
97	
98	
99	def _non_negative_int(value: str) -> int:
100	    try:
101	        parsed = int(value)
102	    except ValueError as error:
103	        raise argparse.ArgumentTypeError(f"invalid non-negative integer: {value}") from error
104	    if parsed < 0:
105	        raise argparse.ArgumentTypeError("value must be non-negative")
106	    return parsed
107	
108	
109	def _non_negative_float(value: str) -> float:
110	    try:
111	        parsed = float(value)
112	    except ValueError as error:
113	        raise argparse.ArgumentTypeError(f"invalid non-negative float: {value}") from error
114	    if parsed < 0:
115	        raise argparse.ArgumentTypeError("value must be non-negative")
116	    return parsed
117	
118	
119	def _run_megaplan(
120	    args: list[str],
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/parallel_critique.py"
}
```

> TOOL

tool_result Read
```
1	"""Parallel Hermes critique runner."""
2	
3	from __future__ import annotations
4	
5	import os
6	import sys
7	import time
8	import uuid
9	from concurrent.futures import ThreadPoolExecutor, as_completed
10	from pathlib import Path
11	from typing import Any
12	
13	from megaplan._core import get_effective, read_json, schemas_root
14	from megaplan.hermes_worker import _toolsets_for_phase, clean_parsed_payload, parse_agent_output
15	from megaplan.prompts.critique import single_check_critique_prompt, write_single_check_template
16	from megaplan.prompts.critique_joke import single_check_critique_joke_prompt
17	from megaplan.types import CliError, PlanState
18	from megaplan.workers import STEP_SCHEMA_FILENAMES, WorkerResult
19	
20	
21	from megaplan.key_pool import (
22	    _load_hermes_env,
23	    _get_api_credential,
24	    resolve_model as _resolve_model,
25	    acquire_key,
26	    report_429,
27	)
28	
29	
30	def _merge_unique(groups: list[list[str]]) -> list[str]:
31	    merged: list[str] = []
32	    seen: set[str] = set()
33	    for group in groups:
34	        for item in group:
35	            if item not in seen:
36	                seen.add(item)
37	                merged.append(item)
38	    return merged
39	
40	
41	def _run_check(
42	    index: int,
43	    check: dict[str, Any],
44	    *,
45	    state: PlanState,
46	    plan_dir: Path,
47	    root: Path,
48	    model: str | None,
49	    schema: dict[str, Any],
50	    project_dir: Path,
51	) -> tuple[int, dict[str, Any], list[str], list[str], float]:
52	    from megaplan.hermes_worker import _import_hermes_runtime
53	
54	    AIAgent, SessionDB = _import_hermes_runtime()
55	
56	    output_path = write_single_check_template(plan_dir, state, check, f"critique_check_{check['id']}.json")
57	    prompt_builder = (
58	        single_check_critique_joke_prompt
59	        if state.get("config", {}).get("mode", "code") == "joke"
60	        else single_check_critique_prompt
61	    )
62	    prompt = prompt_builder(state, plan_dir, root, check, output_path)
63	    resolved_model, agent_kwargs = _resolve_model(model)
64	
65	    _model_lower = (resolved_model or "").lower()
66	    _reasoning_families = ("qwen/qwen3", "deepseek/deepseek-r1")
67	    _reasoning_off = (
68	        {"enabled": False}
69	        if any(_model_lower.startswith(prefix) for prefix in _reasoning_families)
70	        else None
71	    )
72	
73	    def _make_agent(m: str, kw: dict) -> "AIAgent":
74	        a = AIAgent(
75	            model=m,
76	            quiet_mode=True,
77	            skip_context_files=True,
78	            skip_memory=True,
79	            enabled_toolsets=_toolsets_for_phase("critique"),
80	            session_id=str(uuid.uuid4()),
81	            session_db=SessionDB(),
82	            max_tokens=8192,
83	            reasoning_config=_reasoning_off,
84	            **kw,
85	        )
86	        a._print_fn = lambda *args, **kwargs: print(*args, **kwargs, file=sys.stderr)
87	        return a
88	
89	    def _failure_reason(exc: Exception) -> str:
90	        if isinstance(exc, CliError):
91	            return exc.message
92	        return str(exc) or exc.__class__.__name__
93	
94	    def _run_attempt(current_agent, current_output_path: Path) -> tuple[dict[str, Any], dict[str, Any], list[str], list[str], float]:
95	        current_result = current_agent.run_conversation(user_message=prompt)
96	        payload, raw_output = parse_agent_output(
97	            current_agent,
98	            current_result,
99	            output_path=current_output_path,
100	            schema=schema,
101	            step="critique",
102	            project_dir=project_dir,
103	            plan_dir=plan_dir,
104	        )
105	        clean_parsed_payload(payload, schema, "critique")
106	        payload_checks = payload.get("checks")
107	        if not isinstance(payload_checks, list) or len(payload_checks) != 1 or not isinstance(payload_checks[0], dict):
108	            raise CliError(
109	                "worker_parse_error",
110	                f"Parallel critique output for check '{check['id']}' did not contain exactly one check",
111	                extra={"raw_output": raw_output},
112	            )
113	        verified = payload.get("verified_flag_ids", [])
114	        disputed = payload.get("disputed_flag_ids", [])
115	        return (
116	            current_result,
117	            payload_checks[0],
118	            verified if isinstance(verified, list) else [],
119	            disputed if isinstance(disputed, list) else [],
120	            float(current_result.get("estimated_cost_usd", 0.0) or 0.0),
121	            int(current_result.get("prompt_tokens", 0) or 0),
122	            int(current_result.get("completion_tokens", 0) or 0),
123	            int(current_result.get("total_tokens", 0) or 0),
124	        )
125	
126	    agent = _make_agent(resolved_model, agent_kwargs)
127	    try:
128	        _result, check_payload, verified_ids, disputed_ids, cost_usd, pt, ct, tt = _run_attempt(agent, output_path)
129	    except Exception as exc:
130	        # Report 429 to key pool so it cools down this key
131	        exc_str = str(exc)
132	        if "429" in exc_str:
133	            if model and model.startswith("minimax:"):
134	                report_429("minimax", agent_kwargs.get("api_key", ""), cooldown_secs=60)
135	            elif model and model.startswith("zhipu:"):
136	                cooldown = 3600 if "Limit Exhausted" in exc_str else 120
137	                report_429("zhipu", agent_kwargs.get("api_key", ""), cooldown_secs=cooldown)
138	        # Fallback to OpenRouter if primary MiniMax API fails (429, timeout, etc.)
139	        if model and model.startswith("minimax:"):
140	            or_key = acquire_key("openrouter")
141	            if or_key:
142	                from megaplan.key_pool import minimax_openrouter_model
143	                fallback_model = minimax_openrouter_model(model[len("minimax:"):])
144	                fallback_kwargs = {"base_url": "https://openrouter.ai/api/v1", "api_key": or_key}
145	                if isinstance(exc, CliError):
146	                    print(
147	                        f"[parallel-critique] MiniMax returned bad content ({_failure_reason(exc)}), falling back to OpenRouter",
148	                        file=sys.stderr,
149	                    )
150	                else:
151	                    print(f"[parallel-critique] Primary MiniMax failed ({exc}), falling back to OpenRouter", file=sys.stderr)
152	                # Re-write template since the previous agent may have corrupted it
153	                output_path = write_single_check_template(plan_dir, state, check, f"critique_check_{check['id']}.json")
154	                agent = _make_agent(fallback_model, fallback_kwargs)
155	                try:
156	                    _result, check_payload, verified_ids, disputed_ids, cost_usd, pt, ct, tt = _run_attempt(agent, output_path)
157	                except Exception as fallback_exc:
158	                    raise CliError(
159	                        "worker_error",
160	                        (
161	                            f"Parallel critique failed for check '{check['id']}' "
162	                            f"(both MiniMax and OpenRouter): primary={_failure_reason(exc)}; "
163	                            f"fallback={_failure_reason(fallback_exc)}"
164	                        ),
165	                        extra={"check_id": check["id"]},
166	                    ) from fallback_exc
167	            else:
168	                raise
169	        else:
170	            raise
171	    return (
172	        index,
173	        check_payload,
174	        verified_ids,
175	        disputed_ids,
176	        cost_usd,
177	        pt,
178	        ct,
179	        tt,
180	    )
181	
182	
183	def run_parallel_critique(
184	    state: PlanState,
185	    plan_dir: Path,
186	    *,
187	    root: Path,
188	    model: str | None,
189	    checks: tuple[dict[str, Any], ...],
190	    max_concurrent: int | None = None,
191	) -> WorkerResult:
192	    started = time.monotonic()
193	    if not checks:
194	        return WorkerResult(
195	            payload={"checks": [], "flags": [], "verified_flag_ids": [], "disputed_flag_ids": []},
196	            raw_output="parallel",
197	            duration_ms=0,
198	            cost_usd=0.0,
199	            session_id=None,
200	        )
201	
202	    schema = read_json(schemas_root(root) / STEP_SCHEMA_FILENAMES["critique"])
203	    project_dir = Path(state["config"]["project_dir"])
204	    results: list[tuple[dict[str, Any], list[str], list[str]] | None] = [None] * len(checks)
205	    total_cost = 0.0
206	    total_prompt_tokens = 0
207	    total_completion_tokens = 0
208	    total_tokens = 0
209	
210	    real_stdout = sys.stdout
211	    sys.stdout = sys.stderr
212	    try:
213	        concurrency = min(max_concurrent or get_effective("orchestration", "max_critique_concurrency"), len(checks))
214	        with ThreadPoolExecutor(max_workers=concurrency) as executor:
215	            futures = [
216	                executor.submit(
217	                    _run_check,
218	                    index,
219	                    check,
220	                    state=state,
221	                    plan_dir=plan_dir,
222	                    root=root,
223	                    model=model,
224	                    schema=schema,
225	                    project_dir=project_dir,
226	                )
227	                for index, check in enumerate(checks)
228	            ]
229	            for future in as_completed(futures):
230	                index, check_payload, verified_ids, disputed_ids, cost_usd, pt, ct, tt = future.result()
231	                results[index] = (check_payload, verified_ids, disputed_ids)
232	                total_cost += cost_usd
233	                total_prompt_tokens += pt
234	                total_completion_tokens += ct
235	                total_tokens += tt
236	    finally:
237	        sys.stdout = real_stdout
238	
239	    ordered_checks: list[dict[str, Any]] = []
240	    verified_groups: list[list[str]] = []
241	    disputed_groups: list[list[str]] = []
242	    for item in results:
243	        if item is None:
244	            raise CliError("worker_error", "Parallel critique did not return all check results")
245	        check_payload, verified_ids, disputed_ids = item
246	        ordered_checks.append(check_payload)
247	        verified_groups.append(verified_ids)
248	        disputed_groups.append(disputed_ids)
249	
250	    disputed_flag_ids = _merge_unique(disputed_groups)
251	    disputed_set = set(disputed_flag_ids)
252	    verified_flag_ids = [flag_id for flag_id in _merge_unique(verified_groups) if flag_id not in disputed_set]
253	    return WorkerResult(
254	        payload={
255	            "checks": ordered_checks,
256	            "flags": [],
257	            "verified_flag_ids": verified_flag_ids,
258	            "disputed_flag_ids": disputed_flag_ids,
259	        },
260	        raw_output="parallel",
261	        duration_ms=int((time.monotonic() - started) * 1000),
262	        cost_usd=total_cost,
263	        session_id=None,
264	        prompt_tokens=total_prompt_tokens,
265	        completion_tokens=total_completion_tokens,
266	        total_tokens=total_tokens,
267	    )
268
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/megaplan/review/"
}
```

> TOOL

tool_result Bash
```
total 96
drwxr-xr-x   7 user_c042661f  staff    224 May  1 06:29 .
drwxr-xr-x  39 user_c042661f  staff   1248 May  2 18:37 ..
-rw-r--r--   1 user_c042661f  staff   1209 Apr 21 17:59 __init__.py
drwxr-xr-x@ 10 user_c042661f  staff    320 May  1 07:15 __pycache__
-rw-r--r--   1 user_c042661f  staff   9175 Apr 21 17:51 checks.py
-rw-r--r--   1 user_c042661f  staff  13175 Apr 11 03:25 mechanical.py
-rw-r--r--   1 user_c042661f  staff  16159 Apr 23 20:31 parallel.py
```

> AGENT

Let me look at the profiles to understand how robustness levels affect the pipeline:

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/megaplan/profiles/"
}
```

> TOOL

tool_result Bash
```
total 64
drwxr-xr-x@ 10 user_c042661f  staff   320 May  2 01:34 .
drwxr-xr-x  39 user_c042661f  staff  1248 May  2 18:37 ..
-rw-r--r--   1 user_c042661f  staff  6555 May  2 01:34 __init__.py
drwxr-xr-x@  4 user_c042661f  staff   128 May  2 01:36 __pycache__
-rw-r--r--   1 user_c042661f  staff   263 May  2 01:34 all-codex.toml
-rw-r--r--   1 user_c042661f  staff   685 May  2 01:34 all-deepseek-flash.toml
-rw-r--r--   1 user_c042661f  staff   657 May  2 01:34 all-deepseek-pro.toml
-rw-r--r--   1 user_c042661f  staff   968 May  2 01:34 all-fireworks-deepseek.toml
-rw-r--r--   1 user_c042661f  staff   582 Apr 23 22:06 all-open.toml
-rw-r--r--   1 user_c042661f  staff   268 Apr 24 19:07 standard.toml
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"STATE_\" /Users/user_c042661f/Documents/megaplan/megaplan/types.py | head -30"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/types.py:STATE_INITIALIZED = "initialized"
/Users/user_c042661f/Documents/megaplan/megaplan/types.py:STATE_PREPPED = "prepped"
/Users/user_c042661f/Documents/megaplan/megaplan/types.py:STATE_PLANNED = "planned"
/Users/user_c042661f/Documents/megaplan/megaplan/types.py:STATE_CRITIQUED = "critiqued"
/Users/user_c042661f/Documents/megaplan/megaplan/types.py:STATE_GATED = "gated"
/Users/user_c042661f/Documents/megaplan/megaplan/types.py:STATE_FINALIZED = "finalized"
/Users/user_c042661f/Documents/megaplan/megaplan/types.py:STATE_EXECUTED = "executed"
/Users/user_c042661f/Documents/megaplan/megaplan/types.py:STATE_DONE = "done"
/Users/user_c042661f/Documents/megaplan/megaplan/types.py:STATE_ABORTED = "aborted"
/Users/user_c042661f/Documents/megaplan/megaplan/types.py:STATE_AWAITING_HUMAN = "awaiting_human_verify"
/Users/user_c042661f/Documents/megaplan/megaplan/types.py:STATE_TIEBREAKER_PENDING = "tiebreaker_pending"
/Users/user_c042661f/Documents/megaplan/megaplan/types.py:STATE_TIEBREAKER_READY = "tiebreaker_ready"
/Users/user_c042661f/Documents/megaplan/megaplan/types.py:TERMINAL_STATES = {STATE_DONE, STATE_ABORTED}
/Users/user_c042661f/Documents/megaplan/megaplan/types.py:    STATE_AWAITING_HUMAN,
/Users/user_c042661f/Documents/megaplan/megaplan/types.py:    STATE_TIEBREAKER_PENDING,
/Users/user_c042661f/Documents/megaplan/megaplan/types.py:    STATE_TIEBREAKER_READY,
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
22	STATE_TIEBREAKER_PENDING = "tiebreaker_pending"
23	STATE_TIEBREAKER_READY = "tiebreaker_ready"
24	TERMINAL_STATES = {STATE_DONE, STATE_ABORTED}
25	AUTOMATION_TERMINAL_STATES = TERMINAL_STATES | {
26	    STATE_AWAITING_HUMAN,
27	    STATE_TIEBREAKER_PENDING,
28	    STATE_TIEBREAKER_READY,
29	}
30	
31	
32	# ---------------------------------------------------------------------------
33	# TypedDicts
34	# ---------------------------------------------------------------------------
35	
36	class PlanConfig(TypedDict, total=False):
37	    project_dir: str
38	    auto_approve: bool
39	    robustness: str
40	    mode: str
41	    output_path: str
42	    from_doc: str
43	    agents: dict[str, str]
44	    workers: NotRequired[dict[str, Any]]
45	    max_tiebreakers_per_plan: int
46	    tiebreaker_blocklist: list[str]
47	    allow_tiebreaker: bool
48	    tiebreaker_token_budget: int
49	    tiebreaker_time_budget_minutes: int
50	    strict_notes: NotRequired[bool]
51	
52	
53	class PlanMeta(TypedDict, total=False):
54	    significant_counts: list[int]
55	    weighted_scores: list[float]
56	    plan_deltas: list[float | None]
57	    recurring_critiques: list[str]
58	    total_cost_usd: float
59	    overrides: list[dict[str, Any]]
60	    notes: list[dict[str, Any]]
61	    imported_decisions: list["SettledDecisionFromDoc"]
62	    user_approved_gate: bool
63	
64	
65	class SessionInfo(TypedDict, total=False):
66	    id: str
67	    mode: str
68	    created_at: str
69	    last_used_at: str
70	    refreshed: bool
71	
72	
73	class ActiveStep(TypedDict, total=False):
74	    step: str
75	    agent: str
76	    mode: str
77	    model: str
78	    run_id: str
79	    session_id: str
80	    started_at: str
81	
82	
83	class PlanVersionRecord(TypedDict, total=False):
84	    version: int
85	    file: str
86	    hash: str
87	    timestamp: str
88	
89	
90	class HistoryEntry(TypedDict, total=False):
91	    step: str
92	    timestamp: str
93	    duration_ms: int
94	    cost_usd: float
95	    result: str
96	    session_mode: str
97	    session_id: str
98	    agent: str
99	    output_file: str
100	    artifact_hash: str
101	    finalize_hash: str
102	    raw_output_file: str
103	    message: str
104	    flags_count: int
105	    flags_addressed: list[Any]
106	    recommendation: str
107	    approval_mode: str
108	    environment: dict[str, bool]
109	
110	
111	class ClarificationRecord(TypedDict, total=False):
112	    refined_idea: str
113	    intent_summary: str
114	    questions: list[str]
115	
116	
117	class LastGateRecord(TypedDict, total=False):
118	    recommendation: str
119	    rationale: str
120	    signals_assessment: str
121	    warnings: list[str]
122	    settled_decisions: list["SettledDecision"]
123	    passed: bool
124	    preflight_results: dict[str, bool]
125	    orchestrator_guidance: str
126	
127	
128	class PlanState(TypedDict):
129	    name: str
130	    idea: str
131	    current_state: str
132	    iteration: int
133	    created_at: str
134	    config: PlanConfig
135	    sessions: dict[str, SessionInfo]
136	    plan_versions: list[PlanVersionRecord]
137	    history: list[HistoryEntry]
138	    meta: PlanMeta
139	    last_gate: LastGateRecord
140	    active_step: NotRequired[ActiveStep]
141	    clarification: NotRequired[ClarificationRecord]
142	
143	
144	class _FlagRecordRequired(TypedDict):
145	    id: str
146	    concern: str
147	    category: str
148	    status: str
149	
150	
151	class FlagRecord(_FlagRecordRequired, total=False):
152	    severity_hint: str
153	    evidence: str
154	    raised_in: str
155	    severity: str
156	    verified: bool
157	    verified_in: str
158	    addressed_in: str
159	    settled_by_tiebreaker: str
160	
161	
162	class FlagRegistry(TypedDict):
163	    flags: list[FlagRecord]
164	
165	
166	class GateCheckResult(TypedDict):
167	    passed: bool
168	    criteria_check: dict[str, Any]
169	    preflight_results: dict[str, bool]
170	    unresolved_flags: list[FlagRecord]
171	
172	
173	class SettledDecision(TypedDict, total=False):
174	    id: str
175	    decision: str
176	    rationale: str
177	
178	
179	class SettledDecisionFromDoc(TypedDict, total=False):
180	    id: str
181	    decision: str
182	    rationale: str
183	    load_bearing: bool
184	
185	
186	class TiebreakerDecision(TypedDict, total=False):
187	    fuzzy_group_id: str
188	    flag_ids: list[str]
189	    question: str
190	    researcher_pick: str
191	    challenger_pick: str
192	    human_pick: str
193	    action: str
194	    rationale: str
195	    timestamp: str
196	
197	
198	class GatePayload(TypedDict):
199	    recommendation: str
200	    rationale: str
201	    signals_assessment: str
202	    warnings: list[str]
203	    settled_decisions: list[SettledDecision]
204	
205	
206	class GateArtifact(TypedDict, total=False):
207	    passed: bool
208	    criteria_check: dict[str, Any]
209	    preflight_results: dict[str, bool]
210	    unresolved_flags: list[FlagRecord]
211	    recommendation: str
212	    rationale: str
213	    signals_assessment: str
214	    warnings: list[str]
215	    settled_decisions: list[SettledDecision]
216	    override_forced: bool
217	    orchestrator_guidance: str
218	    robustness: str
219	    signals: dict[str, Any]
220	
221	
222	class GateSignals(TypedDict, total=False):
223	    robustness: str
224	    signals: dict[str, Any]
225	    warnings: list[str]
226	
227	
228	class StepResponse(TypedDict, total=False):
229	    success: bool
230	    step: str
231	    summary: str
232	    artifacts: list[str]
233	    next_step: str | None
234	    state: str
235	    auto_approve: bool
236	    robustness: str
237	    iteration: int
238	    plan: str
239	    plan_dir: str
240	    questions: list[str]
241	    verified_flags: list[str]
242	    open_flags: list[str]
243	    scope_creep_flags: list[str]
244	    warnings: list[str]
245	    files_changed: list[str]
246	    deviations: list[str]
247	    user_approved_gate: bool
248	    issues: list[str]
249	    valid_next: list[str]
250	    mode: str
251	    installed: list[dict[str, Any]]
252	    config_path: str
253	    routing: dict[str, str]
254	    raw_config: dict[str, Any]
255	    action: str
256	    key: str
257	    value: str
258	    skipped: bool
259	    file: str
260	    plans: list[dict[str, Any]]
261	    recommendation: str
262	    signals: dict[str, Any]
263	    rationale: str
264	    signals_assessment: str
265	    orchestrator_guidance: str
266	    passed: bool
267	    criteria_check: dict[str, Any]
268	    preflight_results: dict[str, bool]
269	    unresolved_flags: list[Any]
270	    error: str
271	    message: str
272	    details: dict[str, Any]
273	    agent_fallback: dict[str, str]
274	
275	
276	class DebtEntry(TypedDict):
277	    id: str
278	    subsystem: str
279	    concern: str
280	    flag_ids: list[str]
281	    plan_ids: list[str]
282	    occurrence_count: int
283	    created_at: str
284	    updated_at: str
285	    resolved: bool
286	    resolved_by: str | None
287	    resolved_at: str | None
288	
289	
290	class DebtRegistry(TypedDict):
291	    entries: list[DebtEntry]
292	
293	
294	# ---------------------------------------------------------------------------
295	# Constants
296	# ---------------------------------------------------------------------------
297	
298	FLAG_BLOCKING_STATUSES = {"open", "disputed", "addressed"}
299	FLAG_VALID_STATUSES = {
300	    "open", "addressed", "disputed", "verified",
301	    "accepted_tradeoff", "gate_disputed",
302	}
303	DEBT_ESCALATION_THRESHOLD = 3
304	MOCK_ENV_VAR = "MEGAPLAN_MOCK_WORKERS"
305	
306	DEFAULT_AGENT_ROUTING: dict[str, str] = {
307	    "plan": "claude",
308	    "prep": "claude",
309	    "critique": "codex",
310	    "revise": "claude",
311	    "gate": "claude",
312	    "finalize": "claude",
313	    "execute": "codex",
314	    "loop_plan": "claude",
315	    "loop_execute": "codex",
316	    "review": "codex",
317	    "tiebreaker_researcher": "codex",
318	    "tiebreaker_challenger": "codex",
319	}
320	KNOWN_AGENTS = ["claude", "codex", "hermes"]
321	ROBUSTNESS_LEVELS = ("tiny", "light", "standard", "robust", "superrobust")
322	def parse_agent_spec(spec: str) -> tuple[str, str | None]:
323	    """Parse 'hermes:model/name' → ('hermes', 'model/name') or 'claude' → ('claude', None)."""
324	    if ":" in spec:
325	        agent, model = spec.split(":", 1)
326	        return agent, model
327	    return spec, None
328	
329	
330	SCOPE_CREEP_TERMS = (
331	    "scope creep",
332	    "out of scope",
333	    "beyond the original idea",
334	    "beyond original idea",
335	    "beyond user intent",
336	    "expanded scope",
337	)
338	
339	DEFAULTS = {
340	    "execution.auto_approve": False,
341	    "execution.robustness": "standard",
342	    "execution.strict_notes": False,
343	    "execution.worker_timeout_seconds": 7200,
344	    "execution.max_review_rework_cycles": 3,
345	    "execution.max_robust_review_rework_cycles": 2,
346	    "execution.max_execute_no_progress": 3,
347	    "orchestration.max_critique_concurrency": 2,
348	    "orchestration.mode": "subagent",
349	}
350	
351	_SETTABLE_BOOL = {
352	    "execution.auto_approve",
353	    "execution.strict_notes",
354	}
355	
356	_SETTABLE_ENUM = {
357	    "execution.robustness": ROBUSTNESS_LEVELS,
358	}
359	
360	_SETTABLE_NUMERIC = {
361	    "execution.worker_timeout_seconds",
362	    "execution.max_review_rework_cycles",
363	    "execution.max_robust_review_rework_cycles",
364	    "execution.max_execute_no_progress",
365	    "orchestration.max_critique_concurrency",
366	}
367	
368	
369	# ---------------------------------------------------------------------------
370	# Exception
371	# ---------------------------------------------------------------------------
372	
373	class CliError(Exception):
374	    def __init__(
375	        self,
376	        code: str,
377	        message: str,
378	        *,
379	        valid_next: list[str] | None = None,
380	        extra: dict[str, Any] | None = None,
381	        exit_code: int = 1,
382	    ) -> None:
383	        super().__init__(message)
384	        self.code = code
385	        self.message = message
386	        self.valid_next = valid_next or []
387	        self.extra = extra or {}
388	        self.exit_code = exit_code
389
```

> AGENT

Now let me check the core module to understand how states transition and next steps are inferred:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def infer_next_steps\\|def workflow_includes_step\\|def next_step_after\" /Users/user_c042661f/Documents/megaplan/megaplan/_core/__init__.py | head -10"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan/megaplan/_core -name \"*.py\" -type f"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/_core/io.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/phase_runtime.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/__init__.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/modes.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/workflow.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/registries.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/workflow.py",
  "limit": 150
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
22	    STATE_TIEBREAKER_PENDING,
23	    STATE_TIEBREAKER_READY,
24	)
25	from .modes import is_creative_mode
26	
27	
28	@dataclass(frozen=True)
29	class Transition:
30	    next_step: str
31	    next_state: str
32	    condition: str = "always"
33	
34	
35	WORKFLOW: dict[str, list[Transition]] = {
36	    STATE_INITIALIZED: [
37	        Transition("prep", STATE_PREPPED),
38	    ],
39	    STATE_PREPPED: [
40	        Transition("plan", STATE_PLANNED),
41	    ],
42	    STATE_PLANNED: [
43	        Transition("critique", STATE_CRITIQUED),
44	        Transition("plan", STATE_PLANNED),
45	    ],
46	    STATE_CRITIQUED: [
47	        Transition("gate", STATE_GATED, "gate_unset"),
48	        Transition("revise", STATE_PLANNED, "gate_iterate"),
49	        Transition("tiebreaker", STATE_TIEBREAKER_PENDING, "gate_tiebreaker"),
50	        Transition("override add-note", STATE_CRITIQUED, "gate_escalate"),
51	        Transition("override force-proceed", STATE_GATED, "gate_escalate"),
52	        Transition("override abort", STATE_ABORTED, "gate_escalate"),
53	        Transition("revise", STATE_PLANNED, "gate_proceed_blocked"),
54	        Transition("override force-proceed", STATE_GATED, "gate_proceed_blocked"),
55	        Transition("gate", STATE_GATED, "gate_proceed"),
56	    ],
57	    STATE_GATED: [
58	        Transition("finalize", STATE_FINALIZED),
59	        Transition("override replan", STATE_PLANNED),
60	    ],
61	    STATE_FINALIZED: [
62	        Transition("execute", STATE_EXECUTED),
63	        Transition("override replan", STATE_PLANNED),
64	    ],
65	    STATE_EXECUTED: [
66	        # `handle_review()` may also return STATE_FINALIZED on a `needs_rework`
67	        # verdict. That rework loop depends on review payload semantics rather
68	        # than gate_* conditions, so it lives in the handler instead of here
69	        # because `_transition_matches()` only understands gate-based branches.
70	        Transition("review", STATE_DONE),
71	    ],
72	    STATE_AWAITING_HUMAN: [
73	        Transition("verify-human", STATE_DONE),
74	    ],
75	    STATE_TIEBREAKER_PENDING: [
76	        Transition("tiebreaker-run", STATE_TIEBREAKER_READY),
77	    ],
78	    STATE_TIEBREAKER_READY: [
79	        Transition("tiebreaker-decide", STATE_CRITIQUED),
80	    ],
81	}
82	
83	# Each level's *own* overrides (not inherited).  Levels inherit from the
84	# level below them via _ROBUSTNESS_HIERARCHY so shared transitions are
85	# declared once: robust/superrobust have none, standard keeps the
86	# planned->critique routing documented explicitly, and light skips
87	# prep plus gate/review.
88	_ROBUSTNESS_OVERRIDES: dict[str, dict[str, list[Transition]]] = {
89	    "superrobust": {},
90	    "robust": {},
91	    "standard": {
92	        STATE_INITIALIZED: [
93	            Transition("plan", STATE_PLANNED),
94	        ],
95	    },
96	    "light": {
97	        STATE_INITIALIZED: [
98	            Transition("plan", STATE_PLANNED),
99	        ],
100	        STATE_CRITIQUED: [
101	            Transition("revise", STATE_GATED),
102	        ],
103	        STATE_EXECUTED: [],
104	    },
105	    "tiny": {},
106	}
107	
108	_ROBUSTNESS_WORKFLOW_LEVELS: dict[str, tuple[str, ...]] = {
109	    "superrobust": ("superrobust",),
110	    "robust": ("robust",),
111	    "standard": ("standard",),
112	    "light": ("standard", "light"),
113	    "tiny": ("standard", "light", "tiny"),
114	}
115	
116	_STEP_CONTEXT_STATES = {
117	    STATE_PLANNED,
118	    STATE_CRITIQUED,
119	    STATE_GATED,
120	    STATE_FINALIZED,
121	}
122	
123	
124	# ---------------------------------------------------------------------------
125	# Robustness helpers
126	# ---------------------------------------------------------------------------
127	
128	def configured_robustness(state: PlanState) -> str:
129	    robustness = state["config"].get("robustness", "standard")
130	    if robustness not in ROBUSTNESS_LEVELS:
131	        return "standard"
132	    return robustness
133	
134	
135	def robustness_critique_instruction(robustness: str) -> str:
136	    if robustness == "light":
137	        return "Be pragmatic. Only flag issues that would cause real failures. Ignore style, minor edge cases, and issues the executor will naturally resolve."
138	    return "Use balanced judgment. Flag significant risks, but do not spend flags on minor polish or executor-obvious boilerplate."
139	
140	
141	# ---------------------------------------------------------------------------
142	# Intent / notes block for prompts
143	# ---------------------------------------------------------------------------
144	
145	def intent_and_notes_block(state: PlanState) -> str:
146	    sections = []
147	    clarification = state.get("clarification", {})
148	    if clarification.get("intent_summary"):
149	        sections.append(f"User intent summary:\n{clarification['intent_summary']}")
150	        sections.append(f"Original idea:\n{state['idea']}")
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"infer_next_steps\\|workflow_includes_step\" /Users/user_c042661f/Documents/megaplan/megaplan/_core/workflow.py | head -5"
}
```

> TOOL

tool_result Bash
```
225:def workflow_includes_step(robustness: str, step: str) -> bool:
268:infer_next_steps = workflow_next
277:            valid_next=infer_next_steps(state),
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/workflow.py",
  "offset": 200,
  "limit": 80
}
```

> TOOL

tool_result Read
```
200	    return merged
201	
202	
203	def _transition_matches(state: PlanState, condition: str) -> bool:
204	    if condition == "always":
205	        return True
206	    gate = state.get("last_gate", {})
207	    if not isinstance(gate, dict):
208	        gate = {}
209	    recommendation = gate.get("recommendation")
210	    if condition == "gate_unset":
211	        return not recommendation
212	    if condition == "gate_iterate":
213	        return recommendation == "ITERATE"
214	    if condition == "gate_escalate":
215	        return recommendation == "ESCALATE"
216	    if condition == "gate_tiebreaker":
217	        return recommendation == "TIEBREAKER"
218	    if condition == "gate_proceed_blocked":
219	        return recommendation == "PROCEED" and not gate.get("passed", False)
220	    if condition == "gate_proceed":
221	        return recommendation == "PROCEED" and gate.get("passed", False)
222	    return False
223	
224	
225	def workflow_includes_step(robustness: str, step: str) -> bool:
226	    if step == "step":
227	        return True
228	    workflow = _workflow_for_robustness(robustness)
229	    return any(
230	        transition.next_step == step
231	        for transitions in workflow.values()
232	        for transition in transitions
233	    )
234	
235	
236	def workflow_transition(state: PlanState, step: str) -> Transition | None:
237	    current = state.get("current_state")
238	    if not isinstance(current, str):
239	        return None
240	    workflow = _workflow_for_robustness(
241	        _workflow_robustness_from_state(state),
242	        creative=is_creative_mode(state),
243	    )
244	    for transition in workflow.get(current, []):
245	        if transition.next_step == step and _transition_matches(state, transition.condition):
246	            return transition
247	    return None
248	
249	
250	def workflow_next(state: PlanState) -> list[str]:
251	    current = state.get("current_state")
252	    if not isinstance(current, str):
253	        return []
254	    workflow = _workflow_for_robustness(
255	        _workflow_robustness_from_state(state),
256	        creative=is_creative_mode(state),
257	    )
258	    next_steps = [
259	        transition.next_step
260	        for transition in workflow.get(current, [])
261	        if _transition_matches(state, transition.condition)
262	    ]
263	    if current in _STEP_CONTEXT_STATES:
264	        next_steps.append("step")
265	    return next_steps
266	
267	
268	infer_next_steps = workflow_next
269	
270	
271	def require_state(state: PlanState, step: str, allowed: set[str]) -> None:
272	    current = state["current_state"]
273	    if current not in allowed:
274	        raise CliError(
275	            "invalid_transition",
276	            f"Cannot run '{step}' while current state is '{current}'",
277	            valid_next=infer_next_steps(state),
278	            extra={"current_state": current},
279	        )
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers/revise.py",
  "limit": 50
}
```

> TOOL

tool_result Read
```
File does not exist. Note: your current working directory is /Users/user_c042661f/Documents/megaplan.
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers/tiebreaker.py"
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	import argparse
4	from pathlib import Path
5	
6	from megaplan.prompts import create_claude_prompt, create_codex_prompt, create_hermes_prompt
7	from megaplan.types import (
8	    CliError,
9	    PlanState,
10	    STATE_AWAITING_HUMAN,
11	    STATE_PLANNED,
12	    STATE_TIEBREAKER_PENDING,
13	    STATE_TIEBREAKER_READY,
14	    StepResponse,
15	)
16	from megaplan._core import atomic_write_json, load_flag_registry, load_plan_locked, now_utc, read_json, require_state, save_flag_registry
17	
18	def _build_tiebreaker_reprompt(
19	    agent_type: str, state: PlanState, plan_dir: Path, *, root: Path,
20	) -> str:
21	    if agent_type == "claude":
22	        base_prompt = create_claude_prompt("gate", state, plan_dir, root=root)
23	    elif agent_type == "hermes":
24	        base_prompt = create_hermes_prompt("gate", state, plan_dir, root=root)
25	    else:
26	        base_prompt = create_codex_prompt("gate", state, plan_dir, root=root)
27	    addendum = (
28	        "You recommended TIEBREAKER but no flag shows mechanical recurrence signal "
29	        "(addressed_then_reopened_count >= 2, or >=2 flags across >=2 iterations). "
30	        "Either identify specific flag(s) with iteration history or pick ITERATE."
31	    )
32	    return f"{base_prompt}\n\n{addendum}"
33	
34	def handle_tiebreaker_run(root: Path, args: argparse.Namespace) -> StepResponse:
35	    from megaplan._core import workflow_transition
36	    with load_plan_locked(root, args.plan, step="tiebreaker-run") as (plan_dir, state):
37	        require_state(state, "tiebreaker-run", {STATE_TIEBREAKER_PENDING})
38	        gate_data = read_json(plan_dir / "gate.json")
39	        question = gate_data.get("tiebreaker_question", "")
40	        flag_ids = gate_data.get("tiebreaker_flag_ids", [])
41	        fuzzy_group_id = gate_data.get("tiebreaker_fuzzy_group_id", "")
42	        if not question:
43	            raise CliError("missing_tiebreaker_question", "Gate artifact missing tiebreaker_question")
44	
45	        tb_args = argparse.Namespace(
46	            plan=args.plan, question=question, question_file=None,
47	            output=None, agent=getattr(args, "agent", None),
48	            hermes=getattr(args, "hermes", None),
49	            phase_model=list(getattr(args, "phase_model", [])),
50	            profile=getattr(args, "profile", None),
51	            fresh=getattr(args, "fresh", False),
52	            persist=getattr(args, "persist", False),
53	            ephemeral=getattr(args, "ephemeral", False),
54	        )
55	        from megaplan.prompts.tiebreaker_orchestrator import _run_tiebreaker
56	        exit_code = _run_tiebreaker(root, plan_dir, state, tb_args)
57	        transition = workflow_transition(state, "tiebreaker-run")
58	        state["current_state"] = transition.next_state
59	        return {
60	            "success": exit_code == 0,
61	            "step": "tiebreaker-run",
62	            "summary": f"Tiebreaker run {'completed' if exit_code == 0 else 'failed'} for question: {question[:80]}",
63	            "state": state["current_state"],
64	            "plan": state["name"],
65	            "next_step": "tiebreaker decide",
66	            "details": {
67	                "question": question,
68	                "flag_ids": flag_ids,
69	                "fuzzy_group_id": fuzzy_group_id,
70	            },
71	        }
72	
73	def handle_tiebreaker_decide(root: Path, args: argparse.Namespace) -> StepResponse:
74	    from megaplan._core import workflow_transition
75	    with load_plan_locked(root, args.plan, step="tiebreaker-decide") as (plan_dir, state):
76	        require_state(state, "tiebreaker-decide", {STATE_TIEBREAKER_READY})
77	        action = getattr(args, "tiebreaker_decide_action", "pick")
78	        pick = getattr(args, "pick", None)
79	        escalate = getattr(args, "escalate", False)
80	        replan = getattr(args, "replan", False)
81	        rationale = getattr(args, "rationale", "")
82	        if escalate:
83	            action = "escalate"
84	        elif replan:
85	            action = "replan"
86	        else:
87	            action = "pick"
88	
89	        gate_data = read_json(plan_dir / "gate.json")
90	        flag_ids = gate_data.get("tiebreaker_flag_ids", [])
91	        fuzzy_group_id = gate_data.get("tiebreaker_fuzzy_group_id", "")
92	        question = gate_data.get("tiebreaker_question", "")
93	
94	        researcher_files = sorted(plan_dir.glob("tiebreaker_researcher*.json"))
95	        challenger_files = sorted(plan_dir.glob("tiebreaker_challenger*.json"))
96	        researcher_data = read_json(researcher_files[-1]) if researcher_files else {}
97	        challenger_data = read_json(challenger_files[-1]) if challenger_files else {}
98	
99	        from megaplan.types import TiebreakerDecision
100	        decision: TiebreakerDecision = {
101	            "fuzzy_group_id": fuzzy_group_id,
102	            "flag_ids": flag_ids,
103	            "question": question,
104	            "researcher_pick": researcher_data.get("recommendation", ""),
105	            "challenger_pick": challenger_data.get("recommendation", ""),
106	            "human_pick": pick or "",
107	            "action": action,
108	            "rationale": rationale,
109	            "timestamp": now_utc(),
110	        }
111	
112	        decisions_path = plan_dir / "tiebreaker_decisions.json"
113	        existing = read_json(decisions_path) if decisions_path.exists() else []
114	        if not isinstance(existing, list):
115	            existing = []
116	        existing.append(decision)
117	        atomic_write_json(decisions_path, existing)
118	
119	        from megaplan.audits.audit_engine import record_tiebreaker_audit
120	        record_tiebreaker_audit(plan_dir, decision, researcher_data, challenger_data)
121	
122	        if action == "pick" and flag_ids:
123	            registry = load_flag_registry(plan_dir)
124	            for flag in registry.get("flags", []):
125	                if flag["id"] in flag_ids:
126	                    flag["settled_by_tiebreaker"] = fuzzy_group_id
127	            save_flag_registry(plan_dir, registry)
128	
129	        if action == "escalate":
130	            state["current_state"] = STATE_AWAITING_HUMAN
131	            next_step_val = "override add-note"
132	        elif action == "replan":
133	            state["current_state"] = STATE_PLANNED
134	            next_step_val = "critique"
135	        else:
136	            transition = workflow_transition(state, "tiebreaker-decide")
137	            state["current_state"] = transition.next_state
138	            next_step_val = "revise"
139	
140	        return {
141	            "success": True,
142	            "step": "tiebreaker-decide",
143	            "summary": f"Tiebreaker decided: {action} — {rationale[:80]}",
144	            "state": state["current_state"],
145	            "plan": state["name"],
146	            "next_step": next_step_val,
147	            "details": {
148	                "action": action,
149	                "pick": pick,
150	                "fuzzy_group_id": fuzzy_group_id,
151	                "flag_ids": flag_ids,
152	            },
153	        }
154
```

> AGENT

Perfect! Let me also look at the revise handler and understand how critique results flow:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers/revise.py",
  "limit": 80
}
```

> TOOL

tool_result Read
```
File does not exist. Note: your current working directory is /Users/user_c042661f/Documents/megaplan.
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"class WorkerResult\\|def _run_worker\\|def handle\" /Users/user_c042661f/Documents/megaplan/megaplan/handlers/__init__.py | head -20"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/megaplan/megaplan/handlers/"
}
```

> TOOL

tool_result Bash
```
__init__.py
__pycache__
critique.py
execute.py
finalize.py
gate.py
init.py
override.py
plan.py
review.py
shared.py
tiebreaker.py
verifiability.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers/__init__.py",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	from megaplan.audits.robustness import validate_critique_checks
2	from megaplan.review.mechanical import run_pre_checks
3	from megaplan.review.parallel import run_parallel_review
4	from megaplan.flags import update_flags_after_review
5	from megaplan.workers import resolve_agent_mode
6	
7	from .shared import (
8	    log,
9	    _AUTO_NEXT_STEP,
10	    MOCK_ENV_VAR,
11	    shutil,
12	    subprocess,
13	    worker_module,
14	    _run_worker,
15	    _finish_step,
16	    _emit_phase_notice,
17	    attach_agent_fallback,
18	    _attach_next_step_runtime,
19	    _supports_prompt_kwargs,
20	    _build_gate_prompt_override,
21	    _raise_step_validation_error,
22	    _write_json_artifact,
23	    _write_plan_version,
24	    _validate_generated_plan_or_raise,
25	    _append_to_meta,
26	    _merge_imported_decision_criteria,
27	    _validate_relative_path,
28	)
29	from .init import handle_init
30	from .plan import handle_plan, handle_prep, _build_verifiability_flags
31	from .critique import handle_critique, handle_revise, _validate_tiebreaker
32	from .gate import (
33	    _build_gate_signals_artifact,
34	    _record_gate_debt_entries,
35	    _resolve_revise_transition,
36	    _next_progress_step,
37	    _remaining_significant_flags,
38	    _gate_response_fields,
39	    _store_last_gate,
40	    _apply_gate_outcome,
41	    _merge_gate_worker_attempt,
42	    _merge_resolution_tradeoffs_into_payload,
43	    handle_gate,
44	)
45	from .finalize import (
46	    _reconcile_validation_after_mutation,
47	    _validate_finalize_payload,
48	    _ensure_verification_task,
49	    _capture_test_baseline,
50	    _write_finalize_artifacts,
51	    handle_finalize,
52	)
53	from .execute import _is_rework_reexecution, handle_execute
54	from .review import (
55	    _build_review_blocked_message,
56	    _is_substantive_reviewer_verdict,
57	    _build_review_prompt_override,
58	    _merge_review_verdicts,
59	    _resolve_review_outcome,
60	    _synthesize_review_rework_items,
61	    handle_review,
62	)
63	from .override import (
64	    _override_add_note,
65	    _override_abort,
66	    _override_force_proceed,
67	    _override_replan,
68	    _override_set_robustness,
69	    handle_override,
70	)
71	from .verifiability import handle_verify_human, handle_audit_verifiability
72	from .tiebreaker import _build_tiebreaker_reprompt, handle_tiebreaker_run, handle_tiebreaker_decide
73	
74	__all__ = [
75	    "handle_init",
76	    "handle_plan",
77	    "handle_prep",
78	    "handle_critique",
79	    "handle_revise",
80	    "handle_gate",
81	    "handle_finalize",
82	    "handle_execute",
83	    "handle_review",
84	    "handle_override",
85	    "handle_audit_verifiability",
86	    "handle_verify_human",
87	    "handle_tiebreaker_run",
88	    "handle_tiebreaker_decide",
89	]
90
```

> AGENT

Now let me look at the shared handlers to understand the worker invocation pattern:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers/shared.py",
  "limit": 100
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
6	import shutil
7	import subprocess
8	import sys
9	from pathlib import Path
10	from typing import Any, Callable
11	
12	import megaplan.workers as worker_module
13	from megaplan.execute.core import build_monitor_hint
14	from megaplan.profiles import apply_profile_expansion
15	from megaplan.prompts import create_claude_prompt, create_codex_prompt, create_hermes_prompt
16	from megaplan.receipts import build_receipt
17	from megaplan.receipts.writer import write_receipt
18	from megaplan.step_edit import next_plan_artifact_name
19	from megaplan.types import CliError, MOCK_ENV_VAR, PlanState, StepResponse
20	from megaplan._core import (
21	    append_history,
22	    apply_session_update,
23	    atomic_write_json,
24	    atomic_write_text,
25	    build_next_step_runtime,
26	    clear_active_step,
27	    configured_robustness,
28	    get_effective,
29	    infer_next_steps,
30	    make_history_entry,
31	    now_utc,
32	    record_step_failure,
33	    save_state,
34	    save_state_merge_meta,
35	    set_active_step,
36	    sha256_file,
37	    sha256_text,
38	    workflow_next,
39	)
40	from megaplan._core.phase_runtime import (
41	    DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
42	    PHASE_RUNTIME_POLICY,
43	    format_duration_hint,
44	)
45	from megaplan.evaluation import PLAN_STRUCTURE_REQUIRED_STEP_ISSUE, validate_plan_structure
46	from megaplan.workers import WorkerResult
47	
48	log = logging.getLogger("megaplan")
49	
50	
51	def _append_to_meta(state: PlanState, field: str, value: Any) -> None:
52	    state["meta"].setdefault(field, []).append(value)
53	
54	
55	def _merge_imported_decision_criteria(
56	    state: PlanState,
57	    criteria: list[dict[str, Any]],
58	) -> list[dict[str, Any]]:
59	    imported_decisions = state["meta"].get("imported_decisions", [])
60	    if not imported_decisions:
61	        return criteria
62	
63	    merged = list(criteria)
64	    referenced_ids = {
65	        decision_id
66	        for decision in imported_decisions
67	        for decision_id in [decision.get("id")]
68	        if isinstance(decision_id, str)
69	        and decision_id
70	        and any(
71	            decision_id in criterion_text
72	            for criterion in merged
73	            for criterion_text in [criterion.get("criterion")]
74	            if isinstance(criterion, dict) and isinstance(criterion_text, str)
75	        )
76	    }
77	    for decision in imported_decisions:
78	        decision_id = decision.get("id")
79	        if not isinstance(decision_id, str) or not decision_id or decision_id in referenced_ids:
80	            continue
81	        decision_text = decision.get("decision", "")
82	        if not isinstance(decision_text, str):
83	            decision_text = str(decision_text)
84	        load_bearing = bool(decision.get("load_bearing"))
85	        merged.append(
86	            {
87	                "criterion": f"Plan adheres to imported decision {decision_id}: {decision_text}",
88	                "priority": "must" if load_bearing else "info",
89	                "requires": ["subjective_judgment"] if load_bearing else [],
90	            }
91	        )
92	        referenced_ids.add(decision_id)
93	    return merged
94	
95	
96	def _validate_relative_path(project_dir: Path, raw: str, flag_name: str) -> str:
97	    candidate = Path(raw)
98	    if candidate.is_absolute():
99	        raise CliError(
100	            "invalid_args",
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def _run_worker\\|def _finish_step\" /Users/user_c042661f/Documents/megaplan/megaplan/handlers/shared.py"
}
```

> TOOL

tool_result Bash
```
142:def _run_worker(
222:def _finish_step(
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers/shared.py",
  "offset": 142,
  "limit": 150
}
```

> TOOL

tool_result Read
```
142	def _run_worker(
143	    step: str,
144	    state: PlanState,
145	    plan_dir: Path,
146	    args: argparse.Namespace,
147	    *,
148	    root: Path,
149	    iteration: int | None = None,
150	    resolved: tuple[str, str, bool, str | None] | None = None,
151	    prompt_override: str | None = None,
152	    prompt_kwargs: dict[str, Any] | None = None,
153	) -> tuple[WorkerResult, str, str, bool]:
154	    failure_iteration = state["iteration"] if iteration is None else iteration
155	    from megaplan import handlers as _handlers_pkg
156	
157	    apply_profile_expansion(args, Path(state["config"]["project_dir"]), state=state)
158	    agent, mode, refreshed, model = resolved or _handlers_pkg.resolve_agent_mode(step, args)
159	    run_id = set_active_step(state, step=step, agent=agent, mode=mode, model=model)
160	    _emit_phase_notice(step)
161	    # Phases hold the lock for many minutes; merge meta to avoid clobbering
162	    # concurrent override appends to ``meta.notes`` / ``meta.overrides``.
163	    save_state_merge_meta(plan_dir, state)
164	    try:
165	        run_step_kwargs: dict[str, Any] = {
166	            "root": root,
167	            "resolved": (agent, mode, refreshed, model),
168	            "prompt_override": prompt_override,
169	        }
170	        if prompt_kwargs is not None and _supports_prompt_kwargs(worker_module.run_step_with_worker):
171	            run_step_kwargs["prompt_kwargs"] = prompt_kwargs
172	        return worker_module.run_step_with_worker(
173	            step,
174	            state,
175	            plan_dir,
176	            args,
177	            **run_step_kwargs,
178	        )
179	    except CliError as error:
180	        clear_active_step(state, run_id=run_id)
181	        record_step_failure(plan_dir, state, step=step, iteration=failure_iteration, error=error)
182	        raise
183	    except Exception:
184	        clear_active_step(state, run_id=run_id)
185	        save_state_merge_meta(plan_dir, state)
186	        raise
187	
188	
189	def _supports_prompt_kwargs(run_step: Callable[..., Any]) -> bool:
190	    params = inspect.signature(run_step).parameters.values()
191	    return any(param.name == "prompt_kwargs" for param in params) or any(
192	        param.kind == inspect.Parameter.VAR_KEYWORD for param in params
193	    )
194	
195	
196	def _build_gate_prompt_override(
197	    agent_type: str,
198	    state: PlanState,
199	    plan_dir: Path,
200	    *,
201	    root: Path,
202	    missing_flag_ids: list[str],
203	) -> str:
204	    if agent_type == "claude":
205	        base_prompt = create_claude_prompt("gate", state, plan_dir, root=root)
206	    elif agent_type == "hermes":
207	        base_prompt = create_hermes_prompt("gate", state, plan_dir, root=root)
208	    else:
209	        base_prompt = create_codex_prompt("gate", state, plan_dir, root=root)
210	    missing_flags = ", ".join(missing_flag_ids)
211	    addendum = (
212	        "Gate retry for the same iteration.\n"
213	        "Your previous response recommended PROCEED but left blocking flags unresolved.\n"
214	        f"Missing blocking flag IDs: {missing_flags}.\n"
215	        "Return a complete gate response. If you recommend PROCEED, you MUST include "
216	        "`flag_resolutions` entries for every blocking flag. If you cannot resolve every "
217	        "blocking flag, return ITERATE or ESCALATE instead."
218	    )
219	    return f"{base_prompt}\n\n{addendum}"
220	
221	
222	def _finish_step(
223	    plan_dir: Path,
224	    state: PlanState,
225	    args: argparse.Namespace,
226	    *,
227	    step: str,
228	    worker: WorkerResult,
229	    agent: str,
230	    mode: str,
231	    refreshed: bool,
232	    summary: str,
233	    artifacts: list[str],
234	    output_file: str,
235	    artifact_hash: str,
236	    result: str = "success",
237	    success: bool = True,
238	    next_step: object | str | None = _AUTO_NEXT_STEP,
239	    response_fields: dict[str, Any] | None = None,
240	    history_fields: dict[str, Any] | None = None,
241	    run_id: str | None = None,
242	) -> StepResponse:
243	    clear_active_step(state, run_id=run_id)
244	    apply_session_update(state, step, agent, worker.session_id, mode=mode, refreshed=refreshed)
245	    append_history(
246	        state,
247	        make_history_entry(
248	            step,
249	            duration_ms=worker.duration_ms,
250	            cost_usd=worker.cost_usd,
251	            result=result,
252	            worker=worker,
253	            agent=agent,
254	            mode=mode,
255	            output_file=output_file,
256	            artifact_hash=artifact_hash,
257	            prompt_tokens=worker.prompt_tokens,
258	            completion_tokens=worker.completion_tokens,
259	            total_tokens=worker.total_tokens,
260	            **(history_fields or {}),
261	        ),
262	    )
263	    if step not in {"execute", "review"}:
264	        project_dir = Path(state["config"]["project_dir"])
265	        try:
266	            receipt = build_receipt(
267	                phase=step,
268	                state=state,
269	                plan_dir=plan_dir,
270	                args=args,
271	                worker=worker,
272	                agent=agent,
273	                mode=mode,
274	                output_file=output_file,
275	                artifact_hash=artifact_hash,
276	                verdict=(history_fields or {}).get("verdict"),
277	            )
278	            write_receipt(plan_dir, receipt, project_dir=project_dir)
279	        except Exception:
280	            log.warning("Receipt emission failed for step %s", step, exc_info=True)
281	    save_state_merge_meta(plan_dir, state)
282	    resolved_next = next_step
283	    if resolved_next is _AUTO_NEXT_STEP:
284	        next_steps = workflow_next(state)
285	        resolved_next = next_steps[0] if next_steps else None
286	    response: StepResponse = {
287	        "success": success,
288	        "step": step,
289	        "summary": summary,
290	        "artifacts": artifacts,
291	        "monitor_hint": build_monitor_hint(plan_dir),
```

> AGENT

Excellent! Now I have enough understanding. Let me create a comprehensive report:

## MEGAPLAN "MAKE A PLAN" PIPELINE: STRUCTURAL ANALYSIS

### 1. THE DISCRETE STEPS & I/O CONTRACTS

The pipeline consists of **11 primitive steps** (some are variants; true atoms are lower):

| Step | File | Input | Output | Notes |
|------|------|-------|--------|-------|
| **init** | `handlers/init.py` | Idea string, project config | `PlanState` w/ `STATE_INITIALIZED` | Creates plan dir, loads config |
| **prep** | `handlers/plan.py` | `STATE_INITIALIZED` | `prep.json` + `STATE_PREPPED` | Analyzes codebase, extracts context |
| **plan** | `handlers/plan.py` | `STATE_PREPPED` or `STATE_PLANNED` (rerun) | `plan_vN.json` + metadata + `STATE_PLANNED` | Generates/refines plan, questions, success criteria |
| **critique** | `handlers/critique.py` | `STATE_PLANNED` | `critique_vN.json` + flag registry + `STATE_CRITIQUED` | **Parallel checks** via `parallel_critique.py` (concurrent ThreadPoolExecutor) |
| **revise** | `handlers/critique.py` | `STATE_CRITIQUED` + gate rec. ITERATE | `plan_vN+1.json` + `STATE_PLANNED` | Re-plan in response to critique flags |
| **gate** | `handlers/gate.py` | `STATE_CRITIQUED` | `gate.json` + flag resolutions + `STATE_GATED` or branches | Judges: PROCEED / ITERATE / TIEBREAKER / ESCALATE |
| **finalize** | `handlers/finalize.py` | `STATE_GATED` | `finalize.json` + prep tasks, test baseline + `STATE_FINALIZED` | Generates test/execution tasks |
| **execute** | `handlers/execute.py` | `STATE_FINALIZED` | Task execution results + `STATE_EXECUTED` | Runs CLI commands, code changes |
| **review** | `handlers/review.py` | `STATE_EXECUTED` | Task verdicts (✓/✗) + `STATE_DONE` or rework loop | Mechanical + parallel checks; can loop to finalize |
| **tiebreaker-run** | `handlers/tiebreaker.py` | `STATE_TIEBREAKER_PENDING` | Researcher & challenger perspectives + `STATE_TIEBREAKER_READY` | Runs two agents in parallel on disputed flags |
| **tiebreaker-decide** | `handlers/tiebreaker.py` | `STATE_TIEBREAKER_READY` | Tiebreaker decision record + routes to `STATE_CRITIQUED` or `STATE_AWAITING_HUMAN` | Human/LLM picks winner or escalates |

### 2. THE ORCHESTRATION LOGIC

**Top-level entry:** `megaplan/cli.py` → `handle_*` → **`_run_worker()`** (in `handlers/shared.py`)

**Persistence layer:** State machine in `_core/workflow.py`
- **Current state** (`state["current_state"]`) gates which steps are valid
- **Transitions** are condition-based: gate recommendation (ITERATE, PROCEED, ESCALATE, TIEBREAKER) determines next branch
- **Workflow defs by robustness** override which steps run (e.g., `tiny` skips prep, `light` skips review)

**Auto-driver:** `megaplan/auto.py` implements a **dumb loop**:
1. Read plan state via `megaplan status`
2. Call `megaplan [next-step]` 
3. Check result; repeat until terminal state or escalation

**Hardcoded orchestration points:**
- `infer_next_steps(state)` in `_core/workflow.py:250` → looks at `state["current_state"]` + `state["last_gate"]["recommendation"]`
- Each handler calls `_run_worker()`, which invokes the appropriate LLM worker
- `_finish_step()` persists state, appends history, and computes next steps via `workflow_next()`

### 3. HOW CRITIQUES WORK

**File:** `megaplan/parallel_critique.py` (120 lines) + `handlers/critique.py`

**Input:** Plan + success criteria → generate **checks** (from audits/forms)
**Execution:** 
- ThreadPoolExecutor runs each check in parallel (concurrency: config `orchestration.max_critique_concurrency`, default 2)
- Each check spawns a Hermes/Claude agent with `single_check_critique_prompt`
- Outputs: `critique_check_{id}.json` (one per check)

**Output shape:**
```python
{
  "checks": [{"id": X, "text": "...", "passed": bool, ...}, ...],
  "flags": [...],
  "verified_flag_ids": [...],
  "disputed_flag_ids": [...]
}
```

**Consumed by:** `handlers/gate.py` → flag audit → decision to ITERATE/PROCEED/TIEBREAKER

### 4. CURRENT WIRING (HOW STEPS ARE CONNECTED)

**Hardcoded state machine** (`_core/workflow.py:35–81`):
```python
WORKFLOW = {
  STATE_INITIALIZED → ["prep"]
  STATE_PREPPED → ["plan"]
  STATE_PLANNED → ["critique", "plan"] (rerun)
  STATE_CRITIQUED → [
    "gate" (gate_unset),
    "revise" (gate_iterate),
    "tiebreaker" (gate_tiebreaker),
    "override ..." (gate_escalate),
  ]
  ...
}
```

**Robustness overrides** (`_core/workflow.py:88–114`):
- `tiny`: skips prep, review
- `light`: skips prep, review; gate→revise (not gate)
- `standard`: skips prep (init→plan directly)
- `robust` / `superrobust`: full path

**No graph representation** — transitions are lists indexed by current state. Conditions are string tokens (`gate_iterate`, `always`, etc.) checked via `_transition_matches()`.

### 5. ROBUSTNESS LEVELS & STEP CHANGES

| Level | Path Changes |
|-------|--------------|
| `tiny` | init→plan→critique→gate→finalize→execute→✗(no review)→done |
| `light` | init→plan→critique→gate-as-revise→finalize→execute→done |
| `standard` | init→plan→critique→gate→finalize→execute→review→done |
| `robust` | init→prep→plan→critique→gate→finalize→execute→review→done |
| `superrobust` | Full + more aggressive critique/review |

### 6. TOP COMPOSABILITY OBSTACLES

1. **Implicit gate recommendation routing** — Next step is inferred from `state["last_gate"]["recommendation"]` and `current_state`. Steps assume specific predecessors (e.g., `revise` expects `STATE_CRITIQUED`). No explicit dependency DAG.

2. **Gate-coupled iteration loop** — `critique → gate` is tightly bound. Revising requires gate's ITERATE signal. Cannot easily insert a new critique variant or gate logic without modifying `workflow.py`.

3. **Critique-check generation is hidden in audit/form layers** — Which checks run depends on config + robustness + project state, not a declared schema. Hard to swap critique strategies without touching audits.

4. **Worker invocation is agent-routed not step-routed** — `_run_worker()` resolves agent (claude/codex/hermes) and model inside the handler, using CLI args + profile. Each step handler hard-codes agent precedence. No unified invocation registry.

5. **State serialization assumes JSON locality** — Plan state lives in `state.json`; artifacts in sibling files. A step that needs outputs from multiple prior steps must load them independently (e.g., gate reading critique + plan). No artifact graph or manifest.

**Practical impact:** Adding a parallel "quality review" step before gate, or swapping critique for a different validator, requires changes to `workflow.py` + handler + state transitions. Hard to compose arbitrary sequences.
