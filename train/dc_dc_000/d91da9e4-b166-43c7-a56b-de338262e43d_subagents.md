> DEVELOPER

Explore the megaplan codebase at /Users/user_c042661f/Documents/megaplan to gather information needed to plan a new model-profile feature. Report in under 500 words, focused on concrete file paths and line references.

Specifically find:

1. **CLI surface** (`megaplan/cli.py`): 
   - Which subcommand parsers currently add `--phase-model` and `--hermes` (expected: init, step, loop-init, loop-run, chain, tiebreaker). Report the exact function/block names and approximate line numbers.
   - Pattern used for adding arguments (shared helper? repeated code?).
   - Existing `config` subcommand structure if any (for `config profiles list/show`).

2. **DEFAULT_AGENT_ROUTING** in workers.py or elsewhere — list all the phase keys including tiebreaker sub-phases (tiebreaker_orchestrator, tiebreaker_challenger, tiebreaker_researcher, tiebreaker_synthesis). Confirm the canonical list.

3. **parse_agent_spec** — file path and how it parses "hermes:model/name" strings.

4. **load_config** — where it reads TOML/YAML config, what format, what keys. This is relevant because we need to understand the existing config pattern.

5. **state.py** — confirm structure of `state["config"]` and where it's populated at plan-init time. Look for functions that snapshot CLI args into config.

6. **Existing TOML/tomllib usage** — does the project already use tomllib or another parser? Check pyproject.toml / imports.

7. **Test layout** — where are tests? `tests/` directory? What test framework (pytest)? Report a pattern for a new test file.

8. **The hermes vendor plan dependency** — check if `megaplan/hermes_worker.py` or similar has recently been split or is in flux. Look at git log for any in-progress vendor work.

Do NOT read anything under `.megaplan/` (prior plan artifacts). Focus on source, tests, pyproject.toml, and top-level README if needed for config locations. Do NOT go exploring ops/docs directories. Return paths with line numbers where possible.

> AGENT

I'll systematically explore the megaplan codebase to gather the information needed for the model-profile feature. Let me start with the core files.

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
megaplan/audits/quality_gates.py
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
megaplan/execute/merge.py
tests/test_evaluation.py
.venv/bin/activate_this.py
.venv/lib/python3.11/site-packages/_virtualenv.py
megaplan/_core/registries.py
megaplan/key_pool.py
megaplan/prompts/_shared.py
megaplan/_core/io.py
tests/test_io_git_patch.py
megaplan/step_edit.py
megaplan/_core/__init__.py
megaplan/__init__.py
megaplan/prompts/execute.py
megaplan/loop/engine.py
megaplan/review/parallel.py
megaplan/review/mechanical.py
tests/test_config.py
megaplan/prompts/prep_doc.py
megaplan/prompts/review_doc.py
tests/test_workers.py
megaplan/audits/capabilities.py
tests/test_tiny_robustness.py
megaplan/_core/phase_runtime.py
megaplan/_core/workflow.py
megaplan/audits/audit_engine.py
megaplan/audits/iteration.py
megaplan/prompts/tiebreaker_challenger.py
megaplan/prompts/tiebreaker_researcher.py
megaplan/prompts/tiebreaker_synthesis.py
tests/test_schemas.py
.venv/lib/python3.11/site-packages/_yaml/__init__.py
.venv/lib/python3.11/site-packages/yaml/scanner.py
.venv/lib/python3.11/site-packages/yaml/error.py
.venv/lib/python3.11/site-packages/yaml/constructor.py
.venv/lib/python3.11/site-packages/yaml/composer.py
.venv/lib/python3.11/site-packages/yaml/events.py
.venv/lib/python3.11/site-packages/yaml/__init__.py
.venv/lib/python3.11/site-packages/yaml/representer.py
.venv/lib/python3.11/site-packages/yaml/tokens.py
.venv/lib/python3.11/site-packages/yaml/dumper.py
.venv/lib/python3.11/site-packages/yaml/cyaml.py
.venv/lib/python3.11/site-packages/yaml/parser.py
.venv/lib/python3.11/site-packages/yaml/reader.py
.venv/lib/python3.11/site-packages/yaml/loader.py
.venv/lib/python3.11/site-packages/yaml/resolver.py
.venv/lib/python3.11/site-packages/yaml/serializer.py
.venv/lib/python3.11/site-packages/yaml/nodes.py
.venv/lib/python3.11/site-packages/yaml/emitter.py
megaplan/cloud/__init__.py
megaplan/cloud/providers/__init__.py
megaplan/cloud/templates/__init__.py
megaplan/cloud/wrappers/__init__.py
megaplan/cloud/templates/healthserver.py
tests/test_cloud_docker_build.py
tests/test_cloud_resume.py
.venv/lib/python3.11/site-packages/_distutils_hack/__init__.py
.venv/lib/python3.11/site-packages/_distutils_hack/override.py
.venv/lib/python3.11/site-packages/pkg_resources/__init__.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/__init__.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/appdirs.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/zipp.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/importlib_resources/__init__.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/importlib_resources/_adapters.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/importlib_resources/_common.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/importlib_resources/_compat.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/importlib_resources/_itertools.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/importlib_resources/_legacy.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/importlib_resources/abc.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/importlib_resources/readers.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/importlib_resources/simple.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/jaraco/__init__.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/jaraco/context.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/jaraco/functools.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/jaraco/text/__init__.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/more_itertools/__init__.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/more_itertools/more.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/more_itertools/recipes.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/packaging/__about__.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/packaging/__init__.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/packaging/_manylinux.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/packaging/_musllinux.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/packaging/_structures.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/packaging/markers.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/packaging/requirements.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/packaging/specifiers.py
.venv/lib/python3.11/site-packages/pkg_resources/_vendor/packaging/tags.py
(Results are truncated. Consider using a more specific path or pattern.)
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
7	version = "0.20.0"
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
30	exclude = ["megaplan/cloud/_reference/**"]
31	
32	[tool.pytest.ini_options]
33	testpaths = ["tests"]
34	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan"
}
```

> TOOL

tool_result Read
```
EISDIR: illegal operation on a directory, read '/Users/user_c042661f/Documents/megaplan'
```

> AGENT

Now let me look at the specific files mentioned in the requirements:

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
50	from megaplan.execute.core import build_monitor_hint
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
63	    handle_tiebreaker_run,
64	    handle_verify_human,
65	)
66	from megaplan.loop.handlers import (
67	    handle_loop_init,
68	    handle_loop_pause,
69	    handle_loop_run,
70	    handle_loop_status,
71	)
72	from megaplan.step_edit import handle_step
73	
74	
75	def render_response(response: StepResponse, *, exit_code: int = 0) -> int:
76	    print(json_dump(response), end="")
77	    return exit_code
78	
79	
80	def _resolve_error_plan_dir(root: Path | None, error: CliError) -> Path | None:
81	    if root is None or error.code != "plan_locked" or not isinstance(error.extra, dict):
82	        return None
83	    plan_name = error.extra.get("plan")
84	    if not isinstance(plan_name, str) or not plan_name:
85	        return None
86	    try:
87	        return resolve_plan_dir(root, plan_name)
88	    except CliError:
89	        return None
90	
91	
92	def _augment_plan_locked_error(
93	    payload: StepResponse,
94	    error: CliError,
95	    *,
96	    root: Path | None,
97	) -> None:
98	    plan_dir = _resolve_error_plan_dir(root, error)
99	    details = payload.get("details")
100	    if not isinstance(details, dict):
101	        details = None
102	    plan_name = (details or {}).get("plan")
103	    if isinstance(plan_name, str) and plan_name:
104	        monitor_hint = build_monitor_hint(plan_dir or Path(plan_name))
105	        payload["monitor_hint"] = monitor_hint
106	        if details is not None:
107	            details["monitor_hint"] = monitor_hint
108	    raw_active_step = (details or {}).get("active_step")
109	    if isinstance(raw_active_step, dict):
110	        active_step = (
111	            _build_active_step(raw_active_step, plan_dir=plan_dir)
112	            if plan_dir is not None
113	            else dict(raw_active_step)
114	        )
115	        payload["active_step"] = active_step
116	        if details is not None:
117	            details["active_step"] = active_step
118	
119	
120	def error_response(error: CliError, *, root: Path | None = None) -> int:
121	    payload: StepResponse = {
122	        "success": False,
123	        "error": error.code,
124	        "message": error.message,
125	    }
126	    if error.valid_next:
127	        payload["valid_next"] = error.valid_next
128	    if error.extra:
129	        payload["details"] = dict(error.extra)
130	    if error.code == "plan_locked":
131	        _augment_plan_locked_error(payload, error, root=root)
132	    return render_response(payload, exit_code=error.exit_code)
133	
134	
135	def _parse_utc_timestamp(timestamp: str | None) -> datetime | None:
136	    if not isinstance(timestamp, str) or not timestamp:
137	        return None
138	    try:
139	        return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
140	    except ValueError:
141	        return None
142	
143	
144	def _build_progress_payload(plan_dir: Path, state: dict[str, Any]) -> dict[str, Any]:
145	    finalize_path = plan_dir / "finalize.json"
146	    if not finalize_path.exists():
147	        return {
148	            "summary": "No finalize.json yet — plan has not been finalized.",
149	            "tasks_total": 0,
150	            "tasks_done": 0,
151	            "tasks_skipped": 0,
152	            "tasks_pending": 0,
153	            "tasks_blocked": 0,
154	            "batches_total": 0,
155	            "batches_completed": 0,
156	            "tasks": [],
157	        }
158	    finalize_data = read_json(finalize_path)
159	    global_batches = compute_global_batches(finalize_data)
160	    tasks = finalize_data.get("tasks", [])
161	    task_id_to_batch: dict[str, int] = {}
162	    for batch_idx, batch_ids in enumerate(global_batches, start=1):
163	        for task_id in batch_ids:
164	            task_id_to_batch[task_id] = batch_idx
165	    tasks_done = sum(1 for t in tasks if t.get("status") == "done")
166	    tasks_skipped = sum(1 for t in tasks if t.get("status") == "skipped")
167	    tasks_pending = sum(1 for t in tasks if t.get("status") == "pending")
168	    tasks_blocked = sum(1 for t in tasks if t.get("status") == "blocked")
169	    tasks_total = len(tasks)
170	    completed_ids = {
171	        t["id"] for t in tasks if t.get("status") in {"done", "skipped"} and isinstance(t.get("id"), str)
172	    }
173	    batches_completed = sum(
174	        1
175	        for batch_ids in global_batches
176	        if all(tid in completed_ids for tid in batch_ids)
177	    )
178	    task_status_list = [
179	        {
180	            "id": t.get("id", ""),
181	            "status": t.get("status", "pending"),
182	            "batch": task_id_to_batch.get(t.get("id", ""), 0),
183	        }
184	        for t in tasks
185	    ]
186	    return {
187	        "summary": (
188	            f"Execution progress: {tasks_done + tasks_skipped}/{tasks_total} tasks tracked, "
189	            f"{batches_completed}/{len(global_batches)} batches completed. "
190	            "Progress reflects the last finalize.json write (between-batch granularity)."
191	        ),
192	        "tasks_total": tasks_total,
193	        "tasks_done": tasks_done,
194	        "tasks_skipped": tasks_skipped,
195	        "tasks_pending": tasks_pending,
196	        "tasks_blocked": tasks_blocked,
197	        "batches_total": len(global_batches),
198	        "batches_completed": batches_completed,
199	        "tasks": task_status_list,
200	    }
201	
202	
203	def _build_last_step(state: dict[str, Any]) -> dict[str, Any] | None:
204	    history = state.get("history", [])
205	    if not isinstance(history, list) or not history:
206	        return None
207	    last = history[-1]
208	    if not isinstance(last, dict):
209	        return None
210	    return {
211	        "step": last.get("step"),
212	        "result": last.get("result"),
213	        "timestamp": last.get("timestamp"),
214	        "agent": last.get("agent"),
215	        "output_file": last.get("output_file"),
216	    }
217	
218	
219	def _build_active_step(active_step: Any, *, plan_dir: Path) -> dict[str, Any] | None:
220	    if not isinstance(active_step, dict):
221	        return None
222	    details = dict(active_step)
223	    step = details.get("step")
224	    if not isinstance(step, str) or not step:
225	        return details
226	    configured_timeout_seconds = int(get_effective("execution", "worker_timeout_seconds"))
227	    lock_held = plan_lock_is_held(plan_dir)
228	    started_at = _parse_utc_timestamp(details.get("started_at"))
229	    if started_at is not None:
230	        age_seconds = max(0, int((datetime.now(timezone.utc) - started_at).total_seconds()))
231	        details.update(
232	            build_phase_observability(
233	                step,
234	                configured_timeout_seconds=configured_timeout_seconds,
235	                age_seconds=age_seconds,
236	                lock_held=lock_held,
237	            )
238	        )
239	        if details.get("stale"):
240	            orphaned = not lock_held
241	            details["orphaned"] = orphaned
242	            if orphaned:
243	                if step == "execute":
244	                    details["recovery_hint"] = (
245	                        "The active step is stale and no process holds the plan lock. "
246	                        "Safe next action: rerun the same execute command on Codex without --fresh."
247	                    )
248	                else:
249	                    details["recovery_hint"] = (
250	                        "The active step is stale and no process holds the plan lock. "
251	                        "Safe next action: rerun the same step on the same agent before escalating."
252	                    )
253	        max_seconds = int(details.get("expected_duration_seconds", {}).get("max", 0) or 0)
254	        elapsed_label = humanize_seconds(age_seconds)
255	        if details.get("stale"):
256	            details["phase_progress_summary"] = (
257	                f"{step} stale ({elapsed_label} elapsed, expected max {humanize_seconds(max_seconds)}) "
258	                "see recovery_hint."
259	            )
260	        elif step in {"execute", "loop_execute"}:
261	            details["phase_progress_summary"] = (
262	                f"{step} running ({elapsed_label} elapsed, use progress for batch-level detail)."
263	            )
264	        else:
265	            details["phase_progress_summary"] = (
266	                f"{step} running ({elapsed_label} elapsed, typically completes within "
267	                f"{humanize_seconds(max_seconds)})."
268	            )
269	            if max_seconds > 0:
270	                details["progress_pct"] = min(95, int((age_seconds / max_seconds) * 100))
271	    else:
272	        details.update(
273	            build_phase_observability(
274	                step,
275	                configured_timeout_seconds=configured_timeout_seconds,
276	                lock_held=lock_held,
277	            )
278	        )
279	        if step in {"execute", "loop_execute"}:
280	            details["phase_progress_summary"] = (
281	                f"{step} active (start time unknown, use progress for batch-level detail)."
282	            )
283	        else:
284	            details["phase_progress_summary"] = f"{step} active (start time unknown)."
285	    return details
286	
287	
288	def _build_status_payload(plan_dir: Path, state: dict[str, Any]) -> StepResponse:
289	    next_steps = infer_next_steps(state)
290	    notes = state.get("meta", {}).get("notes", [])
291	    lock_path = plan_dir / ".plan.lock"
292	    lock_file_present = lock_path.exists()
293	    lock_held = plan_lock_is_held(plan_dir)
294	    active_step = _build_active_step(state.get("active_step"), plan_dir=plan_dir)
295	    last_step = _build_last_step(state)
296	    plan_mode = state.get("config", {}).get("mode", "code")
297	    plan_output_path = state.get("config", {}).get("output_path")
298	    summary = f"Plan '{state['name']}' is currently in state '{state['current_state']}'."
299	    if plan_mode in {"doc", "joke"}:
300	        summary += f" Mode: {plan_mode}. Output: {plan_output_path}."
301	    if active_step:
302	        summary = (
303	            summary
304	            + f" Active step: {active_step.get('step')} via {active_step.get('agent')}."
305	        )
306	    elif lock_file_present and not lock_held:
307	        summary = (
308	            summary
309	            + " No active step. The `.plan.lock` file may remain on disk even when no process holds the lock."
310	        )
311	    response: StepResponse = {
312	        "success": True,
313	        "step": "status",
314	        "plan": state["name"],
315	        "state": state["current_state"],
316	        "iteration": state["iteration"],
317	        "summary": summary,
318	        "next_step": next_steps[0] if next_steps else None,
319	        "valid_next": next_steps,
320	        "artifacts": sorted(
321	            path.name
322	            for path in plan_dir.iterdir()
323	            if path.is_file() and path.name != ".plan.lock"
324	        ),
325	        "lock_file_present": lock_file_present,
326	        "lock_held": lock_held,
327	        "active_step": active_step,
328	        "last_step": last_step,
329	        "total_cost_usd": state.get("meta", {}).get("total_cost_usd", 0.0),
330	        "mode": plan_mode,
331	        "output_path": plan_output_path,
332	        "notes_count": len(notes) if isinstance(notes, list) else 0,
333	        "notes": notes if isinstance(notes, list) else [],
334	        "session_summaries": [
335	            {"key": key, **value}
336	            for key, value in sorted(state.get("sessions", {}).items())
337	            if isinstance(value, dict)
338	        ],
339	    }
340	    runtime = build_next_step_runtime(
341	        response.get("next_step"),
342	        configured_timeout_seconds=int(get_effective("execution", "worker_timeout_seconds")),
343	    )
344	    if runtime is not None:
345	        response["next_step_runtime"] = runtime
346	    progress = _build_progress_payload(plan_dir, state) if (plan_dir / "finalize.json").exists() else None
347	    if progress is not None:
348	        response["progress"] = progress
349	        response["summary"] = response["summary"] + " " + progress["summary"]
350	    return response
351	
352	
353	def handle_status(root: Path, args: argparse.Namespace) -> StepResponse:
354	    if getattr(args, "pending_human", False):
355	        items = []
356	        for pd in active_plan_dirs(root):
357	            st = read_json(pd / "state.json")
358	            if st.get("current_state") == "awaiting_human_verify":
359	                items.append({"name": st["name"], "state": st["current_state"]})
360	        return {
361	            "success": True,
362	            "step": "status",
363	            "summary": f"Found {len(items)} plan(s) awaiting human verification.",
364	            "plans": items,
365	        }
366	    plan_dir, state = load_plan(root, args.plan)
367	    return _build_status_payload(plan_dir, state)
368	
369	
370	def handle_audit(root: Path, args: argparse.Namespace) -> StepResponse:
371	    plan_dir, state = load_plan(root, args.plan)
372	    return {
373	        "success": True,
374	        "step": "audit",
375	        "plan": state["name"],
376	        "plan_dir": str(plan_dir),
377	        "state": state,
378	    }
379	
380	
381	def handle_progress(root: Path, args: argparse.Namespace) -> StepResponse:
382	    plan_dir, state = load_plan(root, args.plan)
383	    progress = _build_progress_payload(plan_dir, state)
384	    return {
385	        "success": True,
386	        "step": "progress",
387	        "plan": state["name"],
388	        **progress,
389	    }
390	
391	
392	def handle_watch(root: Path, args: argparse.Namespace) -> StepResponse:
393	    response = handle_status(root, args)
394	    response["step"] = "watch"
395	    return response
396	
397	
398	def _collect_megaplan_roots(root: Path, *, tree: bool = False, all_system: bool = False) -> list[Path]:
399	    """Collect .megaplan root directories based on search mode."""
400	    roots: list[Path] = [root]
401	
402	    if all_system:
403	        # Search from home directory downward for all .megaplan directories
404	        home = Path.home()
405	        for megaplan_dir in sorted(home.rglob(".megaplan")):
406	            if megaplan_dir.is_dir() and (megaplan_dir / "plans").is_dir():
407	                candidate = megaplan_dir.parent
408	                if candidate.resolve() != root.resolve():
409	                    roots.append(candidate)
410	    elif tree:
411	        # Walk up to find parent .megaplan directories
412	        current = root.resolve().parent
413	        while True:
414	            if (current / ".megaplan" / "plans").is_dir() and current.resolve() != root.resolve():
415	                roots.append(current)
416	            parent = current.parent
417	            if parent == current:
418	                break
419	            current = parent
420	        # Walk down to find child .megaplan directories
421	        for megaplan_dir in sorted(root.rglob(".megaplan")):
422	            if megaplan_dir.is_dir() and (megaplan_dir / "plans").is_dir():
423	                candidate = megaplan_dir.parent
424	                if candidate.resolve() != root.resolve():
425	                    roots.append(candidate)
426	
427	    return roots
428	
429	
430	def handle_list(root: Path, args: argparse.Namespace) -> StepResponse:
431	    ensure_runtime_layout(root)
432	    filter_status = getattr(args, "filter_status", None)
433	    no_tree = getattr(args, "no_tree", False)
434	    include_done = getattr(args, "include_done", False)
435	    show_summary = getattr(args, "summary", False)
436	    search_all = getattr(args, "all", False)
437	    # Default: tree=True (parent+child), active-only (exclude done/aborted)
438	    # --status overrides the active filter (explicit filter = show exactly that)
439	    search_tree = not no_tree and not search_all
440	    filter_active = not include_done and not filter_status
441	
442	    roots = _collect_megaplan_roots(root, tree=search_tree, all_system=search_all)
443	    total_scanned = 0
444	    allowed_states: set[str] | None = None
445	    if filter_status:
446	        allowed_states = {s.strip() for s in filter_status.split(",")}
447	
448	    items = []
449	    state_counts: dict[str, int] = {}
450	    resolved_root = root.resolve()
451	    for search_root in roots:
452	        resolved_search = search_root.resolve()
453	        is_local = resolved_search == resolved_root
454	        for plan_dir in active_plan_dirs(search_root):
455	            state = read_json(plan_dir / "state.json")
456	            current_state = state["current_state"]
457	            state_counts[current_state] = state_counts.get(current_state, 0) + 1
458	            total_scanned += 1
459	
460	            if filter_active and current_state in TERMINAL_STATES:
461	                continue
462	            if allowed_states and current_state not in allowed_states:
463	                continue
464	
465	            next_steps = infer_next_steps(state)
466	            entry = {
467	                "name": state["name"],
468	                "idea": state["idea"],
469	                "state": current_state,
470	                "iteration": state["iteration"],
471	                "next_step": next_steps[0] if next_steps else None,
472	            }
473	            if not is_local:
474	                try:
475	                    rel = resolved_search.relative_to(resolved_root)
476	                    entry["location"] = f"./{rel}"
477	                    entry["direction"] = "child"
478	                except ValueError:
479	                    try:
480	                        resolved_root.relative_to(resolved_search)
481	                        entry["location"] = os.path.relpath(resolved_search, resolved_root)
482	                        entry["direction"] = "parent"
483	                    except ValueError:
484	                        entry["location"] = str(resolved_search)
485	                        entry["direction"] = "external"
486	            items.append(entry)
487	
488	    summary_parts = [f"Found {len(items)} plans"]
489	    if len(roots) > 1:
490	        summary_parts.append(f"across {len(roots)} directories")
491	    if allowed_states:
492	        summary_parts.append(f"matching {','.join(sorted(allowed_states))}")
493	    if filter_active:
494	        summary_parts.append("(active only)")
495	
496	    result: StepResponse = {
497	        "success": True,
498	        "step": "list",
499	        "summary": f"{'. '.join(summary_parts)}.",
500	        "plans": items,
501	    }
502	    if show_summary:
503	        result["state_summary"] = dict(sorted(state_counts.items()))
504	
505	    # Hints for discovering more plans
506	    hidden_done = total_scanned - len(items) if filter_active else 0
507	    hints: list[str] = []
508	    if hidden_done > 0:
509	        hints.append(f"{hidden_done} completed plans hidden (use --include-done to show)")
510	    if not search_all:
511	        hints.append("Use --all to search all plans system-wide")
512	    if hints:
513	        result["hints"] = hints
514	
515	    return result
516	
517	
518	def handle_debt(root: Path, args: argparse.Namespace) -> StepResponse:
519	    ensure_runtime_layout(root)
520	    action = args.debt_action
521	    registry = load_debt_registry(root)
522	    default_plan_id = getattr(args, "plan", None) or "manual"
523	
524	    if action == "list":
525	        entries = registry["entries"] if args.all else [entry for entry in registry["entries"] if not entry["resolved"]]
526	        grouped: dict[str, list[dict[str, Any]]] = {}
527	        for entry in entries:
528	            grouped.setdefault(entry["subsystem"], []).append(entry)
529	        escalated = {
530	            subsystem: total
531	            for subsystem, total, _entries in escalated_subsystems(registry)
532	        }
533	        by_subsystem = [
534	            {
535	                "subsystem": subsystem,
536	                "escalated": subsystem in escalated,
537	                "total_occurrences": subsystem_occurrence_total(entries_for_subsystem)
538	                if not args.all
539	                else sum(entry["occurrence_count"] for entry in entries_for_subsystem if not entry["resolved"]),
540	                "entries": entries_for_subsystem,
541	            }
542	            for subsystem, entries_for_subsystem in sorted(grouped.items())
543	        ]
544	        return {
545	            "success": True,
546	            "step": "debt",
547	            "action": "list",
548	            "summary": f"Found {len(entries)} debt entries across {len(by_subsystem)} subsystem groups.",
549	            "details": {
550	                "entries": entries,
551	                "by_subsystem": by_subsystem,
552	                "escalated_subsystems": [
553	                    {"subsystem": subsystem, "total_occurrences": total}
554	                    for subsystem, total in sorted(escalated.items())
555	                ],
556	            },
557	        }
558	
559	    if action == "add":
560	        flag_ids = [
561	            flag_id.strip()
562	            for flag_id in (args.flag_ids or "").split(",")
563	            if flag_id.strip()
564	        ]
565	        entry = add_or_increment_debt(
566	            registry,
567	            subsystem=args.subsystem,
568	            concern=args.concern,
569	            flag_ids=flag_ids,
570	            plan_id=default_plan_id,
571	        )
572	        save_debt_registry(root, registry)
573	        return {
574	            "success": True,
575	            "step": "debt",
576	            "action": "add",
577	            "summary": f"Tracked debt entry {entry['id']} for subsystem '{entry['subsystem']}'.",
578	            "details": {"entry": entry},
579	        }
580	
581	    if action == "resolve":
582	        entry = resolve_debt(registry, args.debt_id, default_plan_id)
583	        save_debt_registry(root, registry)
584	        return {
585	            "success": True,
586	            "step": "debt",
587	            "action": "resolve",
588	            "summary": f"Resolved debt entry {entry['id']}.",
589	            "details": {"entry": entry},
590	        }
591	
592	    raise CliError("invalid_args", f"Unknown debt action: {action}")
593	
594	
595	# ---------------------------------------------------------------------------
596	# Setup and config
597	# ---------------------------------------------------------------------------
598	
599	def _canonical_instructions() -> str:
600	    return resources.files("megaplan").joinpath("data", "instructions.md").read_text(encoding="utf-8")
601	
602	
603	_SKILL_HEADER = """\
604	---
605	name: megaplan
606	description: AI agent harness for coordinating Claude and GPT to make and execute extremely robust plans.
607	---
608	
609	"""
610	
611	_CURSOR_HEADER = """\
612	---
613	description: Use megaplan for high-rigor planning on complex, high-risk, or multi-stage tasks.
614	alwaysApply: false
615	---
616	
617	"""
618	
619	
620	def bundled_agents_md() -> str:
621	    return _canonical_instructions()
622	
623	
624	def _subagent_appendix(filename: str) -> str:
625	    content = resources.files("megaplan").joinpath("data", filename).read_text(encoding="utf-8")
626	    content = content.replace(
627	        "{max_execute_no_progress}",
628	        str(get_effective("execution", "max_execute_no_progress")),
629	    )
630	    content = content.replace(
631	        "{max_review_rework_cycles}",
632	        str(get_effective("execution", "max_review_rework_cycles")),
633	    )
634	    return content
635	
636	
637	def _claude_subagent_appendix() -> str:
638	    return _subagent_appendix("claude_subagent_appendix.md")
639	
640	
641	def _codex_subagent_appendix() -> str:
642	    return _subagent_appendix("codex_subagent_appendix.md")
643	
644	
645	def bundled_global_file(name: str) -> str:
646	    content = _canonical_instructions()
647	    if name == "claude_skill.md":
648	        return _SKILL_HEADER + content + "\n\n" + _claude_subagent_appendix()
649	    if name == "codex_skill.md":
650	        return _SKILL_HEADER + content + "\n\n" + _codex_subagent_appendix()
651	    if name == "skill.md":
652	        return _SKILL_HEADER + content
653	    if name == "cursor_rule.mdc":
654	        return _CURSOR_HEADER + content
655	    return content
656	
657	
658	_GLOBAL_TARGETS = [
659	    {"agent": "claude", "detect": ".claude", "path": ".claude/skills/megaplan/SKILL.md", "data": "claude_skill.md"},
660	    {"agent": "codex", "detect": ".codex", "path": ".codex/skills/megaplan/SKILL.md", "data": "codex_skill.md"},
661	    {"agent": "cursor", "detect": ".cursor", "path": ".cursor/rules/megaplan.mdc", "data": "cursor_rule.mdc"},
662	]
663	
664	
665	def _install_owned_file(path: Path, content: str, *, force: bool = False) -> dict[str, bool | str]:
666	    existed = path.exists()
667	    if existed and not force:
668	        if path.read_text(encoding="utf-8") == content:
669	            return {"path": str(path), "skipped": True, "existed": True}
670	    atomic_write_text(path, content)
671	    return {"path": str(path), "skipped": False, "existed": existed}
672	
673	
674	def handle_setup_global(force: bool = False, home: Path | None = None) -> StepResponse:
675	    if home is None:
676	        home = Path.home()
677	    installed: list[dict[str, Any]] = []
678	    detected_count = 0
679	    for target in _GLOBAL_TARGETS:
680	        agent_dir = home / target["detect"]
681	        if not agent_dir.is_dir():
682	            installed.append({"agent": target["agent"], "path": str(home / target["path"]), "skipped": True, "reason": "not installed"})
683	            continue
684	        detected_count += 1
685	        result = _install_owned_file(home / target["path"], bundled_global_file(target["data"]), force=force)
686	        result["agent"] = target["agent"]
687	        installed.append(result)
688	    if detected_count == 0:
689	        return {
690	            "success": False, "step": "setup", "mode": "global",
691	            "summary": "No supported agents detected. Create one of ~/.claude/, ~/.codex/, or ~/.cursor/ and re-run.",
692	            "installed": installed,
693	        }
694	    available = detect_available_agents()
695	    config_path = None
696	    routing = None
697	    if available:
698	        agents_config = {step: (default if default in available else available[0]) for step, default in DEFAULT_AGENT_ROUTING.items()}
699	        config = load_config(home)
700	        config["agents"] = agents_config
701	        config_path = save_config(config, home)
702	        routing = agents_config
703	    lines = []
704	    for rec in installed:
705	        if rec.get("reason") == "not installed":
706	            lines.append(f"  {rec['agent']}: skipped (not installed)")
707	        elif rec["skipped"]:
708	            lines.append(f"  {rec['agent']}: up to date")
709	        else:
710	            lines.append(f"  {rec['agent']}: {'overwrote' if rec['existed'] else 'created'} {rec['path']}")
711	    result_data: dict[str, Any] = {"success": True, "step": "setup", "mode": "global", "summary": "Global setup complete:\n" + "\n".join(lines), "installed": installed}
712	    if config_path is not None:
713	        result_data["config_path"] = str(config_path)
714	        result_data["routing"] = routing
715	    return result_data
716	
717	
718	def handle_setup(args: argparse.Namespace) -> StepResponse:
719	    local = args.local or args.target_dir
720	    if not local:
721	        return handle_setup_global(force=args.force)
722	    target_dir = Path(args.target_dir).resolve() if args.target_dir else Path.cwd()
723	    target = target_dir / "AGENTS.md"
724	    content = bundled_agents_md()
725	    if target.exists() and not args.force:
726	        existing = target.read_text(encoding="utf-8")
727	        if "megaplan" in existing.lower():
728	            return {"success": True, "step": "setup", "summary": f"AGENTS.md already contains megaplan instructions at {target}", "skipped": True}
729	        atomic_write_text(target, existing + "\n\n" + content)
730	        return {"success": True, "step": "setup", "summary": f"Appended megaplan instructions to existing {target}", "file": str(target)}
731	    atomic_write_text(target, content)
732	    return {"success": True, "step": "setup", "summary": f"Created {target}", "file": str(target)}
733	
734	
735	def handle_config(args: argparse.Namespace) -> StepResponse:
736	    action = args.config_action
737	    if action == "show":
738	        config = load_config()
739	        effective_routing = {step: config.get("agents", {}).get(step, default) for step, default in DEFAULT_AGENT_ROUTING.items()}
740	        effective_settings = {
741	            dot_key: get_effective(section, setting)
742	            for dot_key in sorted(DEFAULTS)
743	            for section, setting in [dot_key.split(".", 1)]
744	        }
745	        return {
746	            "success": True,
747	            "step": "config",
748	            "action": "show",
749	            "config_path": str(config_dir() / "config.json"),
750	            "routing": effective_routing,
751	            "effective_settings": effective_settings,
752	            "raw_config": config,
753	        }
754	    if action == "set":
755	        key, value = args.key, args.value
756	        parts = key.split(".", 1)
757	        config = load_config()
758	        valid_keys = [
759	            *(f"agents.{step}" for step in DEFAULT_AGENT_ROUTING),
760	            "orchestration.mode",
761	            *sorted(_SETTABLE_BOOL),
762	            *sorted(_SETTABLE_ENUM),
763	            *sorted(_SETTABLE_NUMERIC),
764	        ]
765	        if len(parts) != 2:
766	            raise CliError(
767	                "invalid_args",
768	                f"Unknown config key '{key}'. Valid keys: {', '.join(valid_keys)}",
769	            )
770	        section, setting = parts
771	        normalized_value = value.strip().lower()
772	        if section == "agents":
773	            if setting not in DEFAULT_AGENT_ROUTING:
774	                raise CliError("invalid_args", f"Unknown step '{setting}'. Valid steps: {', '.join(DEFAULT_AGENT_ROUTING)}")
775	            if value not in KNOWN_AGENTS:
776	                raise CliError("invalid_args", f"Unknown agent '{value}'. Valid agents: {', '.join(KNOWN_AGENTS)}")
777	            config.setdefault("agents", {})[setting] = value
778	        elif key == "orchestration.mode":
779	            if value not in {"inline", "subagent"}:
780	                raise CliError("invalid_args", "orchestration.mode must be 'inline' or 'subagent'")
781	            config.setdefault("orchestration", {})["mode"] = value
782	        elif key in _SETTABLE_BOOL:
783	            if normalized_value in {"true", "1", "yes", "on"}:
784	                parsed_value = True
785	            elif normalized_value in {"false", "0", "no", "off"}:
786	                parsed_value = False
787	            else:
788	                raise CliError(
789	                    "invalid_args",
790	                    f"{key} must be one of: true, false, 1, 0, yes, no, on, off",
791	                )
792	            config.setdefault(section, {})[setting] = parsed_value
793	        elif key in _SETTABLE_ENUM:
794	            allowed_values = _SETTABLE_ENUM[key]
795	            if value not in allowed_values:
796	                raise CliError(
797	                    "invalid_args",
798	                    f"{key} must be one of: {', '.join(allowed_values)}",
799	                )
800	            config.setdefault(section, {})[setting] = value
801	        elif key in _SETTABLE_NUMERIC:
802	            try:
803	                parsed_value = int(value)
804	            except ValueError as exc:
805	                raise CliError("invalid_args", f"{key} must be an integer, got '{value}'") from exc
806	            config.setdefault(section, {})[setting] = parsed_value
807	        else:
808	            raise CliError(
809	                "invalid_args",
810	                f"Unknown config key '{key}'. Valid keys: {', '.join(valid_keys)}",
811	            )
812	        save_config(config)
813	        return {"success": True, "step": "config", "action": "set", "key": key, "value": config[section][setting]}
814	    if action == "reset":
815	        path = config_dir() / "config.json"
816	        if path.exists():
817	            path.unlink()
818	        return {"success": True, "step": "config", "action": "reset", "summary": "Config file removed. Using defaults."}
819	    raise CliError("invalid_args", f"Unknown config action: {action}")
820	
821	
822	# ---------------------------------------------------------------------------
823	# Parser and dispatch
824	# ---------------------------------------------------------------------------
825	
826	def build_parser() -> argparse.ArgumentParser:
827	    parser = argparse.ArgumentParser(description="Megaplan orchestration CLI")
828	    subparsers = parser.add_subparsers(dest="command", required=True)
829	
830	    setup_parser = subparsers.add_parser("setup", help="Install megaplan into agent configs (global by default)")
831	    setup_parser.add_argument("--local", action="store_true", help="Install AGENTS.md into a project instead of global agent configs")
832	    setup_parser.add_argument("--target-dir", help="Directory to install into (default: cwd, implies --local)")
833	    setup_parser.add_argument("--force", action="store_true", help="Overwrite existing files")
834	
835	    init_parser = subparsers.add_parser("init")
836	    init_parser.add_argument("--project-dir", required=True)
837	    init_parser.add_argument("--name")
838	    init_parser.add_argument("--auto-approve", action="store_true", default=None)
839	    init_parser.add_argument("--robustness", choices=list(ROBUSTNESS_LEVELS), default=None)
840	    init_parser.add_argument("--mode", choices=["code", "doc", "metaplan", "joke"], default=None,
841	                             help="Deliverable type: 'code' (source changes), 'doc' / 'metaplan' "
842	                                  "(design/spec artifact — 'metaplan' is an alias for 'doc'), or "
843	                                  "'joke' (film scene script; requires --output). "
844	                                  "Defaults to 'code' unless the idea strongly suggests a design document, "
845	                                  "in which case --mode must be passed explicitly.")
846	    init_parser.add_argument("--output", default=None,
847	                             help="Relative path where the doc or joke artifact will be written. "
848	                                  "Required with --mode doc or --mode joke; rejected with --mode code.")
849	    init_parser.add_argument(
850	        "--primary-criterion",
851	        default=None,
852	        help="Declare the joke-mode primary criterion (for example: 'weirdest coherent'). "
853	             "Valid only with --mode joke.",
854	    )
855	    init_parser.add_argument("--from-doc", default=None,
856	                             help="Relative path to a prior doc-mode artifact whose ## Settled "
857	                                  "Decisions section should be imported. Valid with --mode "
858	                                  "code, --mode doc, or --mode joke.")
859	    init_parser.add_argument(
860	        "--idea-file",
861	        default=None,
862	        help="Read the idea text from a UTF-8 file instead of the positional CLI argument.",
863	    )
864	    init_parser.add_argument(
865	        "--auto-start",
866	        action="store_true",
867	        help="Immediately run the in-process auto driver after initializing the plan.",
868	    )
869	    init_parser.add_argument("--hermes", nargs="?", const="", default=None,
870	                             help="Use Hermes agent for all phases. Optional: specify default model")
871	    init_parser.add_argument("--phase-model", action="append", default=[],
872	                             help="Per-phase model override: --phase-model critique=hermes:openai/gpt-5")
873	    init_parser.add_argument("idea", nargs="?")
874	
875	    list_parser = subparsers.add_parser("list")
876	    list_parser.add_argument("--all", action="store_true",
877	                             help="Search all .megaplan directories system-wide (~)")
878	    list_parser.add_argument("--no-tree", action="store_true",
879	                             help="Only show plans from the current directory (default includes parent + child)")
880	    list_parser.add_argument("--include-done", action="store_true",
881	                             help="Include terminal plans (done/aborted); excluded by default")
882	    list_parser.add_argument("--status", dest="filter_status",
883	                             help="Filter by state (e.g. 'done', 'finalized', 'executed', or comma-separated 'planned,critiqued')")
884	    list_parser.add_argument("--summary", action="store_true",
885	                             help="Show count breakdown by state")
886	
887	    for name in ["status", "audit", "progress", "watch"]:
888	        step_parser = subparsers.add_parser(name)
889	        step_parser.add_argument("--plan")
890	        if name == "status":
891	            step_parser.add_argument("--pending-human", action="store_true",
892	                                     help="List plans awaiting human verification")
893	
894	    for name in ["plan", "prep", "critique", "revise", "gate", "finalize", "execute", "review"]:
895	        step_parser = subparsers.add_parser(name)
896	        step_parser.add_argument("--plan")
897	        step_parser.add_argument("--agent", choices=["claude", "codex", "hermes"])
898	        step_parser.add_argument("--hermes", nargs="?", const="", default=None,
899	                                 help="Use Hermes agent for all phases. Optional: specify default model (e.g. --hermes anthropic/claude-sonnet-4.6)")
900	        step_parser.add_argument("--phase-model", action="append", default=[],
901	                                 help="Per-phase model override: --phase-model critique=hermes:openai/gpt-5")
902	        step_parser.add_argument("--fresh", action="store_true")
903	        step_parser.add_argument("--persist", action="store_true")
904	        step_parser.add_argument("--ephemeral", action="store_true")
905	        step_parser.add_argument("--work-dir", default=None,
906	                                 help="Override the source-code working directory passed to subprocess workers "
907	                                      "(--add-dir / -C). Defaults to the current working directory. Use this to "
908	                                      "force a specific path (e.g. a git worktree) regardless of where the plan was created.")
909	        if name == "execute":
910	            step_parser.add_argument("--confirm-destructive", action="store_true")
911	            step_parser.add_argument("--user-approved", action="store_true")
912	            step_parser.add_argument("--batch", type=int, default=None, help="Execute a specific global batch number (1-indexed)")
913	        if name == "review":
914	            step_parser.add_argument("--confirm-self-review", action="store_true")
915	
916	    config_parser = subparsers.add_parser("config", help="View or edit megaplan configuration")
917	    config_sub = config_parser.add_subparsers(dest="config_action", required=True)
918	    config_sub.add_parser("show")
919	    set_parser = config_sub.add_parser("set")
920	    set_parser.add_argument("key")
921	    set_parser.add_argument("value")
922	    config_sub.add_parser("reset")
923	
924	    step_parser = subparsers.add_parser("step", help="Edit plan step sections without hand-editing markdown")
925	    step_subparsers = step_parser.add_subparsers(dest="step_action", required=True)
926	
927	    step_add_parser = step_subparsers.add_parser("add", help="Insert a new step after an existing step")
928	    step_add_parser.add_argument("--plan")
929	    step_add_parser.add_argument("--after")
930	    step_add_parser.add_argument("description")
931	
932	    step_remove_parser = step_subparsers.add_parser("remove", help="Remove a step and renumber the plan")
933	    step_remove_parser.add_argument("--plan")
934	    step_remove_parser.add_argument("step_id")
935	
936	    step_move_parser = step_subparsers.add_parser("move", help="Move a step after another step and renumber")
937	    step_move_parser.add_argument("--plan")
938	    step_move_parser.add_argument("step_id")
939	    step_move_parser.add_argument("--after", required=True)
940	
941	    override_parser = subparsers.add_parser("override")
942	    override_parser.add_argument("override_action", choices=["abort", "force-proceed", "add-note", "replan", "set-robustness"])
943	    override_parser.add_argument("--plan")
944	    override_parser.add_argument("--reason", default="")
945	    override_parser.add_argument("--note")
946	    override_parser.add_argument("--robustness", choices=list(ROBUSTNESS_LEVELS), default=None)
947	
948	    verify_human_parser = subparsers.add_parser("verify-human", help="Record human verification for a criterion")
949	    verify_human_parser.add_argument("--plan")
950	    verify_human_parser.add_argument("--criterion", required=True, help="Criterion name or index")
951	    vh_group = verify_human_parser.add_mutually_exclusive_group(required=True)
952	    vh_group.add_argument("--pass", dest="pass_flag", action="store_true")
953	    vh_group.add_argument("--fail", dest="fail_flag", action="store_true")
954	    verify_human_parser.add_argument("--evidence", required=True, help="Evidence supporting the verdict")
955	
956	    audit_verifiability_parser = subparsers.add_parser("audit-verifiability", help="Audit criteria verifiability")
957	    audit_verifiability_parser.add_argument("--plan")
958	
959	    debt_parser = subparsers.add_parser("debt", help="Inspect or manage persistent tech debt entries")
960	    debt_subparsers = debt_parser.add_subparsers(dest="debt_action", required=True)
961	
962	    debt_list_parser = debt_subparsers.add_parser("list", help="List debt entries")
963	    debt_list_parser.add_argument("--all", action="store_true", help="Include resolved entries")
964	
965	    debt_add_parser = debt_subparsers.add_parser("add", help="Add or increment a debt entry")
966	    debt_add_parser.add_argument("--subsystem", required=True)
967	    debt_add_parser.add_argument("--concern", required=True)
968	    debt_add_parser.add_argument("--flag-ids", default="")
969	    debt_add_parser.add_argument("--plan")
970	
971	    debt_resolve_parser = debt_subparsers.add_parser("resolve", help="Resolve a debt entry")
972	    debt_resolve_parser.add_argument("debt_id")
973	    debt_resolve_parser.add_argument("--plan")
974	
975	    loop_init_parser = subparsers.add_parser("loop-init", help="Initialize a MegaLoop workflow")
976	    loop_init_parser.add_argument("--project-dir", required=True)
977	    loop_init_parser.add_argument("--command", required=True)
978	    loop_init_parser.add_argument("--goal", dest="goal_option")
979	    loop_init_parser.add_argument("--name")
980	    loop_init_parser.add_argument("--iterations", type=int, default=3)
981	    loop_init_parser.add_argument("--time-budget", type=int, default=300)
982	    loop_init_parser.add_argument("--observe-interval", type=int)
983	    loop_init_parser.add_argument("--observe-break-patterns")
984	    loop_init_parser.add_argument("--agent", choices=["claude", "codex", "hermes"])
985	    loop_init_parser.add_argument("--hermes", nargs="?", const="", default=None,
986	                                  help="Use Hermes agent for loop phases. Optional: specify default model")
987	    loop_init_parser.add_argument("--phase-model", action="append", default=[],
988	                                  help="Per-phase model override: --phase-model loop_execute=hermes:openai/gpt-5")
989	    loop_init_parser.add_argument("--fresh", action="store_true")
990	    loop_init_parser.add_argument("--persist", action="store_true")
991	    loop_init_parser.add_argument("--ephemeral", action="store_true")
992	    loop_init_parser.add_argument("--work-dir", default=None,
993	                                  help="Override the source-code working directory for subprocess workers (default: CWD)")
994	    loop_init_parser.add_argument("goal", nargs="?")
995	
996	    loop_run_parser = subparsers.add_parser("loop-run", help="Run an existing MegaLoop workflow")
997	    loop_run_parser.add_argument("name")
998	    loop_run_parser.add_argument("--project-dir")
999	    loop_run_parser.add_argument("--iterations", type=int)
1000	    loop_run_parser.add_argument("--time-budget", type=int)
1001	    loop_run_parser.add_argument("--agent", choices=["claude", "codex", "hermes"])
1002	    loop_run_parser.add_argument("--hermes", nargs="?", const="", default=None,
1003	                                 help="Use Hermes agent for loop phases. Optional: specify default model")
1004	    loop_run_parser.add_argument("--phase-model", action="append", default=[],
1005	                                 help="Per-phase model override: --phase-model loop_execute=hermes:openai/gpt-5")
1006	    loop_run_parser.add_argument("--fresh", action="store_true")
1007	    loop_run_parser.add_argument("--persist", action="store_true")
1008	    loop_run_parser.add_argument("--ephemeral", action="store_true")
1009	    loop_run_parser.add_argument("--work-dir", default=None,
1010	                                 help="Override the source-code working directory for subprocess workers (default: CWD)")
1011	
1012	    loop_status_parser = subparsers.add_parser("loop-status", help="Show MegaLoop state")
1013	    loop_status_parser.add_argument("name")
1014	    loop_status_parser.add_argument("--project-dir")
1015	
1016	    loop_pause_parser = subparsers.add_parser("loop-pause", help="Pause a MegaLoop workflow")
1017	    loop_pause_parser.add_argument("name")
1018	    loop_pause_parser.add_argument("--project-dir")
1019	    loop_pause_parser.add_argument("--reason", default="")
1020	
1021	    from megaplan.auto import build_auto_parser
1022	    build_auto_parser(subparsers)
1023	
1024	    from megaplan.chain import build_chain_parser
1025	    build_chain_parser(subparsers)
1026	
1027	    cloud_parser = subparsers.add_parser(
1028	        "cloud",
1029	        add_help=False,
1030	        help="Manage provider-backed megaplan cloud runners",
1031	    )
1032	    cloud_parser.add_argument("cloud_args", nargs=argparse.REMAINDER)
1033	
1034	    from megaplan.prompts.tiebreaker_orchestrator import build_tiebreaker_parser
1035	    build_tiebreaker_parser(subparsers)
1036	
1037	    # tiebreaker-run is a top-level command because auto.py:_phase_command
1038	    # translates next_step directly to CLI args.
1039	    tb_run_parser = subparsers.add_parser(
1040	        "tiebreaker-run",
1041	        help="Run tiebreaker researcher+challenger (used by auto driver)",
1042	    )
1043	    tb_run_parser.add_argument("--plan", required=True, help="Plan name")
1044	    tb_run_parser.add_argument("--agent", choices=["claude", "codex", "hermes"], default=None)
1045	    tb_run_parser.add_argument("--hermes", nargs="?", const="", default=None)
1046	    tb_run_parser.add_argument("--phase-model", action="append", default=[])
1047	    tb_run_parser.add_argument("--fresh", action="store_true")
1048	    tb_run_parser.add_argument("--persist", action="store_true")
1049	    tb_run_parser.add_argument("--ephemeral", action="store_true")
1050	
1051	    return parser
1052	
1053	
1054	COMMAND_HANDLERS: dict[str, Callable[..., StepResponse]] = {
1055	    "init": handle_init,
1056	    "plan": handle_plan,
1057	    "prep": handle_prep,
1058	    "critique": handle_critique,
1059	    "revise": handle_revise,
1060	    "gate": handle_gate,
1061	    "finalize": handle_finalize,
1062	    "execute": handle_execute,
1063	    "review": handle_review,
1064	    "status": handle_status,
1065	    "audit": handle_audit,
1066	    "progress": handle_progress,
1067	    "watch": handle_watch,
1068	    "list": handle_list,
1069	    "loop-init": handle_loop_init,
1070	    "loop-run": handle_loop_run,
1071	    "loop-status": handle_loop_status,
1072	    "loop-pause": handle_loop_pause,
1073	    "debt": handle_debt,
1074	    "step": handle_step,
1075	    "override": handle_override,
1076	    "verify-human": handle_verify_human,
1077	    "audit-verifiability": handle_audit_verifiability,
1078	    "tiebreaker-run": handle_tiebreaker_run,
1079	}
1080	
1081	
1082	def cli_entry() -> None:
1083	    sys.exit(main())
1084	
1085	
1086	def _find_megaplan_root(start: Path) -> Path:
1087	    """Walk up from *start* to find the git-root directory containing ``.megaplan/``.
1088	
1089	    Strategy: find the git root first (like ``git rev-parse --show-toplevel``),
1090	    then check if it has a ``.megaplan/`` directory.  This avoids ambiguity when
1091	    nested subdirectories also have their own ``.megaplan/``.  Falls back to the
1092	    nearest ancestor with ``.megaplan/`` if not in a git repo, and finally to
1093	    *start* if nothing is found.
1094	    """
1095	    resolved = start.resolve()
1096	
1097	    # Try git root first — the canonical project root.
1098	    git_root = _find_git_root(resolved)
1099	    if git_root and (git_root / ".megaplan").is_dir():
1100	        return git_root
1101	
1102	    # Fallback: walk up to find nearest .megaplan
1103	    current = resolved
1104	    while True:
1105	        if (current / ".megaplan").is_dir():
1106	            return current
1107	        parent = current.parent
1108	        if parent == current:
1109	            return start
1110	        current = parent
1111	
1112	
1113	def _find_git_root(start: Path) -> Path | None:
1114	    """Walk up to find the directory containing ``.git``."""
1115	    current = start
1116	    while True:
1117	        if (current / ".git").exists():
1118	            return current
1119	        parent = current.parent
1120	        if parent == current:
1121	            return None
1122	        current = parent
1123	
1124	
1125	def _auto_sync_installed_skills() -> None:
1126	    try:
1127	        for target in _GLOBAL_TARGETS:
1128	            agent_dir = Path.home() / target["detect"]
1129	            if not agent_dir.is_dir():
1130	                continue
1131	            _install_owned_file(Path.home() / target["path"], bundled_global_file(target["data"]), force=False)
1132	    except Exception:
1133	        pass
1134	
1135	
1136	def main(argv: list[str] | None = None) -> int:
1137	    if argv is None:
1138	        argv = sys.argv[1:]
1139	    if argv and argv[0] == "cloud":
1140	        from megaplan.cloud.cli import _register_cloud_subcommands, run_cloud_cli
1141	
1142	        cloud_parser = argparse.ArgumentParser(prog="megaplan cloud")
1143	        _register_cloud_subcommands(cloud_parser)
1144	        cloud_args = cloud_parser.parse_args(argv[1:])
1145	        root = _find_megaplan_root(Path.cwd())
1146	        ensure_runtime_layout(root)
1147	        try:
1148	            return run_cloud_cli(root, cloud_args)
1149	        except CliError as error:
1150	            return error_response(error, root=root)
1151	
1152	    parser = build_parser()
1153	    args, remaining = parser.parse_known_args(argv)
1154	    if args.command != "setup":
1155	        _auto_sync_installed_skills()
1156	    try:
1157	        if args.command == "setup":
1158	            return render_response(handle_setup(args))
1159	        if args.command == "config":
1160	            return render_response(handle_config(args))
1161	    except CliError as error:
1162	        return error_response(error)
1163	
1164	    # Capture the working directory for subprocess workers (--add-dir / -C).
1165	    # This preserves git-worktree isolation: workers edit source code under
1166	    # the CWD (or an explicit --work-dir override), not the plan's stored
1167	    # project_dir (which may be a sibling checkout).
1168	    from megaplan.workers import set_work_dir_override
1169	    work_dir_override = getattr(args, "work_dir", None)
1170	    set_work_dir_override(work_dir_override if work_dir_override else Path.cwd())
1171	
1172	    root = _find_megaplan_root(Path.cwd())
1173	    ensure_runtime_layout(root)
1174	
1175	    if args.command == "auto":
1176	        from megaplan.auto import run_auto
1177	        try:
1178	            return run_auto(root, args)
1179	        except CliError as error:
1180	            return error_response(error, root=root)
1181	
1182	    if args.command == "chain":
1183	        from megaplan.chain import run_chain_cli
1184	        try:
1185	            return run_chain_cli(root, args)
1186	        except CliError as error:
1187	            return error_response(error, root=root)
1188	
1189	    if args.command == "tiebreaker":
1190	        from megaplan.prompts.tiebreaker_orchestrator import run_tiebreaker_cli
1191	        try:
1192	            return run_tiebreaker_cli(root, args)
1193	        except CliError as error:
1194	            return error_response(error, root=root)
1195	
1196	    try:
1197	        handler = COMMAND_HANDLERS.get(args.command)
1198	        if handler is None:
1199	            raise CliError("invalid_command", f"Unknown command {args.command!r}")
1200	        if args.command == "override" and remaining:
1201	            if not args.note:
1202	                args.note = " ".join(remaining)
1203	            remaining = []
1204	        if remaining:
1205	            parser.error(f"unrecognized arguments: {' '.join(remaining)}")
1206	        if args.command == "override" and args.override_action == "add-note" and not args.note:
1207	            raise CliError("invalid_args", "override add-note requires a note")
1208	        if args.command == "override" and args.override_action == "set-robustness" and not args.robustness:
1209	            raise CliError("invalid_args", f"override set-robustness requires --robustness {'|'.join(ROBUSTNESS_LEVELS)}")
1210	        return render_response(handler(root, args))
1211	    except CliError as error:
1212	        return error_response(error, root=root)
1213	
1214	
1215	if __name__ == "__main__":
1216	    sys.exit(main())
1217	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan -name \"workers.py\" -type f | head -5"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/workers.py
```

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan -name \"*worker*\" -type f | grep -v \".venv\" | grep -v \".git\""
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/__pycache__/hermes_worker.cpython-314.pyc
/Users/user_c042661f/Documents/megaplan/megaplan/__pycache__/hermes_worker.cpython-311.pyc
/Users/user_c042661f/Documents/megaplan/megaplan/__pycache__/hermes_worker.cpython-312.pyc
/Users/user_c042661f/Documents/megaplan/megaplan/__pycache__/workers.cpython-314.pyc
/Users/user_c042661f/Documents/megaplan/megaplan/__pycache__/workers.cpython-311.pyc
/Users/user_c042661f/Documents/megaplan/megaplan/__pycache__/workers.cpython-312.pyc
/Users/user_c042661f/Documents/megaplan/megaplan/hermes_worker.py
/Users/user_c042661f/Documents/megaplan/megaplan/workers.py
/Users/user_c042661f/Documents/megaplan/tests/__pycache__/test_workers.cpython-38-pytest-8.3.5.pyc
/Users/user_c042661f/Documents/megaplan/tests/__pycache__/test_workers.cpython-311-pytest-8.3.5.pyc
/Users/user_c042661f/Documents/megaplan/tests/__pycache__/test_workers.cpython-311.pyc
/Users/user_c042661f/Documents/megaplan/tests/__pycache__/test_workers.cpython-311-pytest-9.0.2.pyc
/Users/user_c042661f/Documents/megaplan/tests/__pycache__/test_workers.cpython-311-pytest-9.0.3.pyc
/Users/user_c042661f/Documents/megaplan/tests/__pycache__/test_workers.cpython-312-pytest-8.4.2.pyc
/Users/user_c042661f/Documents/megaplan/tests/test_workers.py
```

> AGENT

Now let me examine the types.py to find DEFAULT_AGENT_ROUTING and parse_agent_spec:

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan -name \"types.py\" -type f | grep -v \".venv\""
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/types.py
/Users/user_c042661f/Documents/megaplan/megaplan/loop/types.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/workers.py",
  "limit": 100
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
20	from megaplan.audits.robustness import (
21	    build_empty_template,
22	    checks_for_robustness,
23	    joke_checks_for_robustness,
24	)
25	from megaplan.schemas import SCHEMAS, get_execution_schema_key
26	from megaplan.types import (
27	    CliError,
28	    DEFAULT_AGENT_ROUTING,
29	    MOCK_ENV_VAR,
30	    PlanState,
31	    SessionInfo,
32	    parse_agent_spec,
33	)
34	from megaplan._core import (
35	    apply_session_update,
36	    configured_robustness,
37	    detect_available_agents,
38	    phase_timeout_seconds,
39	    get_effective,
40	    json_dump,
41	    latest_plan_meta_path,
42	    load_config,
43	    now_utc,
44	    read_json,
45	    schemas_root,
46	)
47	from megaplan.prompts import create_claude_prompt, create_codex_prompt
48	
49	
50	_EXECUTE_STEPS = {"execute", "loop_execute"}
51	_CODEX_TEMPLATE_WRITE_STEPS = {"critique", "review"}
52	
53	# Shared mapping from step name to schema filename, used by both
54	# run_claude_step and run_codex_step.
55	STEP_SCHEMA_FILENAMES: dict[str, str] = {
56	    "plan": "plan.json",
57	    "prep": "prep.json",
58	    "revise": "revise.json",
59	    "critique": "critique.json",
60	    "gate": "gate.json",
61	    "finalize": "finalize.json",
62	    "execute": "execution.json",
63	    "loop_plan": "loop_plan.json",
64	    "loop_execute": "loop_execute.json",
65	    "review": "review.json",
66	    "tiebreaker_researcher": "tiebreaker_researcher.json",
67	    "tiebreaker_challenger": "tiebreaker_challenger.json",
68	}
69	
70	# Derive required keys per step from SCHEMAS so they aren't duplicated.
71	_STEP_REQUIRED_KEYS: dict[str, list[str]] = {
72	    step: SCHEMAS[filename].get("required", [])
73	    for step, filename in STEP_SCHEMA_FILENAMES.items()
74	}
75	
76	
77	@dataclass
78	class CommandResult:
79	    command: list[str]
80	    cwd: Path
81	    returncode: int
82	    stdout: str
83	    stderr: str
84	    duration_ms: int
85	
86	
87	@dataclass
88	class WorkerResult:
89	    payload: dict[str, Any]
90	    raw_output: str
91	    duration_ms: int
92	    cost_usd: float
93	    session_id: str | None = None
94	    trace_output: str | None = None
95	    prompt_tokens: int = 0
96	    completion_tokens: int = 0
97	    total_tokens: int = 0
98	
99	
100	# ---------------------------------------------------------------------------

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/hermes_worker.py",
  "limit": 100
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
81	        # Also check flags array
82	        flags = payload.get("flags", [])
83	        if isinstance(flags, list) and flags:
84	            return True
85	        return False
86	    if step == "review":
87	        # For review: the template is pre-populated with task IDs and sense-check
88	        # IDs (empty verdicts). Check that at least one verdict was filled in, or
89	        # that summary/review_verdict has content.
90	        review_verdict = payload.get("review_verdict", "")
91	        if isinstance(review_verdict, str) and review_verdict.strip():
92	            return True
93	        summary = payload.get("summary", "")
94	        if isinstance(summary, str) and summary.strip():
95	            return True
96	        for tv in payload.get("task_verdicts", []):
97	            if isinstance(tv, dict) and tv.get("reviewer_verdict", "").strip():
98	                return True
99	        for sc in payload.get("sense_check_verdicts", []):
100	            if isinstance(sc, dict) and sc.get("verdict", "").strip():

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Now let me check the types.py file for DEFAULT_AGENT_ROUTING and parse_agent_spec:

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
50	
51	
52	class PlanMeta(TypedDict, total=False):
53	    significant_counts: list[int]
54	    weighted_scores: list[float]
55	    plan_deltas: list[float | None]
56	    recurring_critiques: list[str]
57	    total_cost_usd: float
58	    overrides: list[dict[str, Any]]
59	    notes: list[dict[str, Any]]
60	    imported_decisions: list["SettledDecisionFromDoc"]
61	    user_approved_gate: bool
62	
63	
64	class SessionInfo(TypedDict, total=False):
65	    id: str
66	    mode: str
67	    created_at: str
68	    last_used_at: str
69	    refreshed: bool
70	
71	
72	class ActiveStep(TypedDict, total=False):
73	    step: str
74	    agent: str
75	    mode: str
76	    model: str
77	    run_id: str
78	    session_id: str
79	    started_at: str
80	
81	
82	class PlanVersionRecord(TypedDict, total=False):
83	    version: int
84	    file: str
85	    hash: str
86	    timestamp: str
87	
88	
89	class HistoryEntry(TypedDict, total=False):
90	    step: str
91	    timestamp: str
92	    duration_ms: int
93	    cost_usd: float
94	    result: str
95	    session_mode: str
96	    session_id: str
97	    agent: str
98	    output_file: str
99	    artifact_hash: str
100	    finalize_hash: str
101	    raw_output_file: str
102	    message: str
103	    flags_count: int
104	    flags_addressed: list[Any]
105	    recommendation: str
106	    approval_mode: str
107	    environment: dict[str, bool]
108	
109	
110	class ClarificationRecord(TypedDict, total=False):
111	    refined_idea: str
112	    intent_summary: str
113	    questions: list[str]
114	
115	
116	class LastGateRecord(TypedDict, total=False):
117	    recommendation: str
118	    rationale: str
119	    signals_assessment: str
120	    warnings: list[str]
121	    settled_decisions: list["SettledDecision"]
122	    passed: bool
123	    preflight_results: dict[str, bool]
124	    orchestrator_guidance: str
125	
126	
127	class PlanState(TypedDict):
128	    name: str
129	    idea: str
130	    current_state: str
131	    iteration: int
132	    created_at: str
133	    config: PlanConfig
134	    sessions: dict[str, SessionInfo]
135	    plan_versions: list[PlanVersionRecord]
136	    history: list[HistoryEntry]
137	    meta: PlanMeta
138	    last_gate: LastGateRecord
139	    active_step: NotRequired[ActiveStep]
140	    clarification: NotRequired[ClarificationRecord]
141	
142	
143	class _FlagRecordRequired(TypedDict):
144	    id: str
145	    concern: str
146	    category: str
147	    status: str
148	
149	
150	class FlagRecord(_FlagRecordRequired, total=False):
151	    severity_hint: str
152	    evidence: str
153	    raised_in: str
154	    severity: str
155	    verified: bool
156	    verified_in: str
157	    addressed_in: str
158	    settled_by_tiebreaker: str
159	
160	
161	class FlagRegistry(TypedDict):
162	    flags: list[FlagRecord]
163	
164	
165	class GateCheckResult(TypedDict):
166	    passed: bool
167	    criteria_check: dict[str, Any]
168	    preflight_results: dict[str, bool]
169	    unresolved_flags: list[FlagRecord]
170	
171	
172	class SettledDecision(TypedDict, total=False):
173	    id: str
174	    decision: str
175	    rationale: str
176	
177	
178	class SettledDecisionFromDoc(TypedDict, total=False):
179	    id: str
180	    decision: str
181	    rationale: str
182	    load_bearing: bool
183	
184	
185	class TiebreakerDecision(TypedDict, total=False):
186	    fuzzy_group_id: str
187	    flag_ids: list[str]
188	    question: str
189	    researcher_pick: str
190	    challenger_pick: str
191	    human_pick: str
192	    action: str
193	    rationale: str
194	    timestamp: str
195	
196	
197	class GatePayload(TypedDict):
198	    recommendation: str
199	    rationale: str
200	    signals_assessment: str
201	    warnings: list[str]
202	    settled_decisions: list[SettledDecision]
203	
204	
205	class GateArtifact(TypedDict, total=False):
206	    passed: bool
207	    criteria_check: dict[str, Any]
208	    preflight_results: dict[str, bool]
209	    unresolved_flags: list[FlagRecord]
210	    recommendation: str
211	    rationale: str
212	    signals_assessment: str
213	    warnings: list[str]
214	    settled_decisions: list[SettledDecision]
215	    override_forced: bool
216	    orchestrator_guidance: str
217	    robustness: str
218	    signals: dict[str, Any]
219	
220	
221	class GateSignals(TypedDict, total=False):
222	    robustness: str
223	    signals: dict[str, Any]
224	    warnings: list[str]
225	
226	
227	class StepResponse(TypedDict, total=False):
228	    success: bool
229	    step: str
230	    summary: str
231	    artifacts: list[str]
232	    next_step: str | None
233	    state: str
234	    auto_approve: bool
235	    robustness: str
236	    iteration: int
237	    plan: str
238	    plan_dir: str
239	    questions: list[str]
240	    verified_flags: list[str]
241	    open_flags: list[str]
242	    scope_creep_flags: list[str]
243	    warnings: list[str]
244	    files_changed: list[str]
245	    deviations: list[str]
246	    user_approved_gate: bool
247	    issues: list[str]
248	    valid_next: list[str]
249	    mode: str
250	    installed: list[dict[str, Any]]
251	    config_path: str
252	    routing: dict[str, str]
253	    raw_config: dict[str, Any]
254	    action: str
255	    key: str
256	    value: str
257	    skipped: bool
258	    file: str
259	    plans: list[dict[str, Any]]
260	    recommendation: str
261	    signals: dict[str, Any]
262	    rationale: str
263	    signals_assessment: str
264	    orchestrator_guidance: str
265	    passed: bool
266	    criteria_check: dict[str, Any]
267	    preflight_results: dict[str, bool]
268	    unresolved_flags: list[Any]
269	    error: str
270	    message: str
271	    details: dict[str, Any]
272	    agent_fallback: dict[str, str]
273	
274	
275	class DebtEntry(TypedDict):
276	    id: str
277	    subsystem: str
278	    concern: str
279	    flag_ids: list[str]
280	    plan_ids: list[str]
281	    occurrence_count: int
282	    created_at: str
283	    updated_at: str
284	    resolved: bool
285	    resolved_by: str | None
286	    resolved_at: str | None
287	
288	
289	class DebtRegistry(TypedDict):
290	    entries: list[DebtEntry]
291	
292	
293	# ---------------------------------------------------------------------------
294	# Constants
295	# ---------------------------------------------------------------------------
296	
297	FLAG_BLOCKING_STATUSES = {"open", "disputed", "addressed"}
298	FLAG_VALID_STATUSES = {
299	    "open", "addressed", "disputed", "verified",
300	    "accepted_tradeoff", "gate_disputed",
301	}
302	DEBT_ESCALATION_THRESHOLD = 3
303	MOCK_ENV_VAR = "MEGAPLAN_MOCK_WORKERS"
304	
305	DEFAULT_AGENT_ROUTING: dict[str, str] = {
306	    "plan": "claude",
307	    "prep": "claude",
308	    "critique": "codex",
309	    "revise": "claude",
310	    "gate": "claude",
311	    "finalize": "claude",
312	    "execute": "codex",
313	    "loop_plan": "claude",
314	    "loop_execute": "codex",
315	    "review": "codex",
316	    "tiebreaker_researcher": "codex",
317	    "tiebreaker_challenger": "codex",
318	}
319	KNOWN_AGENTS = ["claude", "codex", "hermes"]
320	ROBUSTNESS_LEVELS = ("tiny", "light", "standard", "robust", "superrobust")
321	def parse_agent_spec(spec: str) -> tuple[str, str | None]:
322	    """Parse 'hermes:model/name' → ('hermes', 'model/name') or 'claude' → ('claude', None)."""
323	    if ":" in spec:
324	        agent, model = spec.split(":", 1)
325	        return agent, model
326	    return spec, None
327	
328	
329	SCOPE_CREEP_TERMS = (
330	    "scope creep",
331	    "out of scope",
332	    "beyond the original idea",
333	    "beyond original idea",
334	    "beyond user intent",
335	    "expanded scope",
336	)
337	
338	DEFAULTS = {
339	    "execution.auto_approve": False,
340	    "execution.robustness": "standard",
341	    "execution.worker_timeout_seconds": 7200,
342	    "execution.max_review_rework_cycles": 3,
343	    "execution.max_robust_review_rework_cycles": 2,
344	    "execution.max_execute_no_progress": 3,
345	    "orchestration.max_critique_concurrency": 2,
346	    "orchestration.mode": "subagent",
347	}
348	
349	_SETTABLE_BOOL = {
350	    "execution.auto_approve",
351	}
352	
353	_SETTABLE_ENUM = {
354	    "execution.robustness": ROBUSTNESS_LEVELS,
355	}
356	
357	_SETTABLE_NUMERIC = {
358	    "execution.worker_timeout_seconds",
359	    "execution.max_review_rework_cycles",
360	    "execution.max_robust_review_rework_cycles",
361	    "execution.max_execute_no_progress",
362	    "orchestration.max_critique_concurrency",
363	}
364	
365	
366	# ---------------------------------------------------------------------------
367	# Exception
368	# ---------------------------------------------------------------------------
369	
370	class CliError(Exception):
371	    def __init__(
372	        self,
373	        code: str,
374	        message: str,
375	        *,
376	        valid_next: list[str] | None = None,
377	        extra: dict[str, Any] | None = None,
378	        exit_code: int = 1,
379	    ) -> None:
380	        super().__init__(message)
381	        self.code = code
382	        self.message = message
383	        self.valid_next = valid_next or []
384	        self.extra = extra or {}
385	        self.exit_code = exit_code
386	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Now let me check _core for load_config, save_config, and state-related functions:

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan/megaplan/_core -name \"*.py\" -type f | head -20"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/_core/io.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/phase_runtime.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/__init__.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/workflow.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/registries.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py
```

> TOOL

tool_use Grep
```json
{
  "pattern": "def load_config|def save_config",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core",
  "output_mode": "content"
}
```

> TOOL

tool_result Grep
```
megaplan/_core/io.py:229:def load_config(home: Path | None = None) -> dict[str, Any]:
megaplan/_core/io.py:244:def save_config(config: dict[str, Any], home: Path | None = None) -> Path:
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/__init__.py",
  "limit": 100
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

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/io.py",
  "limit": 300
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
151	        elif show_execution_gaps and status != "pending":
152	            lines.append("  Executor notes: [MISSING]")
153	            gap_counts["Executor notes missing"] = gap_counts.get("Executor notes missing", 0) + 1
154	        files_changed = task.get("files_changed", [])
155	        if files_changed:
156	            lines.append("  Files changed:")
157	            for path in files_changed:
158	                lines.append(f"    - {path}")
159	        if show_execution_gaps and status == "pending":
160	            gap_counts["Tasks without executor updates"] = gap_counts.get("Tasks without executor updates", 0) + 1
161	        reviewer_verdict = task.get("reviewer_verdict", "")
162	        if reviewer_verdict.strip():
163	            lines.append(f"  Reviewer verdict: {reviewer_verdict}")
164	            evidence_files = task.get("evidence_files", [])
165	            if evidence_files:
166	                lines.append("  Evidence files:")
167	                for path in evidence_files:
168	                    lines.append(f"    - {path}")
169	        elif show_review_gaps:
170	            lines.append("  Reviewer verdict: [PENDING]")
171	            gap_counts["Reviewer verdicts pending"] = gap_counts.get("Reviewer verdicts pending", 0) + 1
172	        lines.append("")
173	
174	    lines.extend(["## Watch Items", ""])
175	    watch_items = finalize_data.get("watch_items", [])
176	    if watch_items:
177	        for item in watch_items:
178	            lines.append(f"- {item}")
179	    else:
180	        lines.append("- None.")
181	    lines.append("")
182	
183	    lines.extend(["## Sense Checks", ""])
184	    if sense_checks:
185	        for sense_check in sense_checks:
186	            lines.append(f"- **{sense_check['id']}** ({sense_check['task_id']}): {sense_check['question']}")
187	            executor_note = sense_check.get("executor_note", "")
188	            if executor_note.strip():
189	                lines.append(f"  Executor note: {executor_note}")
190	            elif show_execution_gaps:
191	                lines.append("  Executor note: [MISSING]")
192	                gap_counts["Sense-check acknowledgments missing"] = gap_counts.get("Sense-check acknowledgments missing", 0) + 1
193	            verdict = sense_check.get("verdict", "")
194	            if verdict.strip():
195	                lines.append(f"  Verdict: {verdict}")
196	            elif show_review_gaps:
197	                lines.append("  Verdict: [PENDING]")
198	                gap_counts["Sense-check verdicts pending"] = gap_counts.get("Sense-check verdicts pending", 0) + 1
199	            lines.append("")
200	    else:
201	        lines.extend(["- None.", ""])
202	
203	    lines.extend(["## Meta", ""])
204	    meta_commentary = (finalize_data.get("meta_commentary") or "").strip()
205	    lines.append(meta_commentary or "None.")
206	    lines.append("")
207	
208	    if gap_counts:
209	        lines.extend(["## Coverage Gaps", ""])
210	        for label, count in gap_counts.items():
211	            lines.append(f"- {label}: {count}")
212	        lines.append("")
213	    return "\n".join(lines)
214	
215	
216	# ---------------------------------------------------------------------------
217	# Config helpers
218	# ---------------------------------------------------------------------------
219	
220	def config_dir(home: Path | None = None) -> Path:
221	    if home is None:
222	        xdg = os.environ.get("XDG_CONFIG_HOME")
223	        if xdg:
224	            return Path(xdg) / "megaplan"
225	        home = Path.home()
226	    return home / ".config" / "megaplan"
227	
228	
229	def load_config(home: Path | None = None) -> dict[str, Any]:
230	    path = config_dir(home) / "config.json"
231	    if not path.exists():
232	        return {}
233	    try:
234	        data = json.loads(path.read_text(encoding="utf-8"))
235	    except (json.JSONDecodeError, ValueError) as exc:
236	        import sys
237	        print(f"megaplan: warning: ignoring malformed config at {path}: {exc}", file=sys.stderr)
238	        return {}
239	    if not isinstance(data, dict):
240	        return {}
241	    return data
242	
243	
244	def save_config(config: dict[str, Any], home: Path | None = None) -> Path:
245	    path = config_dir(home) / "config.json"
246	    atomic_write_json(path, config)
247	    return path
248	
249	
250	def get_effective(section: str, key: str) -> Any:
251	    from megaplan.types import DEFAULTS
252	
253	    default_key = f"{section}.{key}"
254	    if default_key not in DEFAULTS:
255	        raise KeyError(default_key)
256	    config = load_config()
257	    section_config = config.get(section)
258	    if isinstance(section_config, dict) and key in section_config:
259	        return section_config[key]
260	    return DEFAULTS[default_key]
261	
262	
263	def detect_available_agents() -> list[str]:
264	    # Access shutil via the _core package so monkeypatches on megaplan._core.shutil work.
265	    import megaplan._core as _core_pkg
266	    _shutil_ref = _core_pkg.shutil
267	    available = [a for a in KNOWN_AGENTS if a != "hermes" and _shutil_ref.which(a)]
268	    # Hermes is a Python library, not a CLI binary
269	    try:
270	        import run_agent  # noqa: F401
271	        available.append("hermes")
272	    except ImportError:
273	        pass
274	    return available
275	
276	
277	# ---------------------------------------------------------------------------
278	# Runtime layout / path helpers
279	# ---------------------------------------------------------------------------
280	
281	def ensure_runtime_layout(root: Path) -> None:
282	    megaplan_rt = root / ".megaplan"
283	    (megaplan_rt / "plans").mkdir(parents=True, exist_ok=True)
284	    schemas_dir = megaplan_rt / "schemas"
285	    schemas_dir.mkdir(parents=True, exist_ok=True)
286	    for filename, schema in SCHEMAS.items():
287	        atomic_write_json(schemas_dir / filename, strict_schema(schema))
288	
289	
290	def megaplan_root(root: Path) -> Path:
291	    return root / ".megaplan"
292	
293	
294	def plans_root(root: Path) -> Path:
295	    return megaplan_root(root) / "plans"
296	
297	
298	def schemas_root(root: Path) -> Path:
299	    return megaplan_root(root) / "schemas"
300	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Now let me check the state.py and look for how config is populated:

> TOOL

tool_use Grep
```json
{
  "pattern": "config\\[|\"config\":|state\\[\"config\"\\]",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py",
  "output_mode": "content"
}
```

> TOOL

tool_result Grep
```
No matches found
```

> TOOL

tool_use Grep
```json
{
  "pattern": "tomllib|toml|yaml|json",
  "path": "/Users/user_c042661f/Documents/megaplan",
  "output_mode": "files_with_matches",
  "head_limit": 30
}
```

> TOOL

tool_result Grep
```
Found 30 files limit: 30
megaplan/handlers/critique.py
megaplan/handlers/plan.py
tests/test_joke_mode_smoke.py
megaplan/prompts/prep_joke.py
tests/test_init_plan.py
tests/test_handle_init_joke_mode.py
megaplan/handlers/init.py
megaplan/cli.py
megaplan/schemas.py
megaplan/prompts/planning.py
megaplan/prompts/review_joke.py
megaplan/prompts/execute_joke.py
megaplan/_core/state.py
megaplan/flags.py
megaplan/prompts/revise_joke.py
megaplan/parallel_critique.py
megaplan/hermes_worker.py
megaplan/workers.py
megaplan/prompts/critique.py
megaplan/prompts/review.py
megaplan/prompts/finalize.py
megaplan/execute/timeout.py
megaplan/execute/core.py
megaplan/evaluation.py
megaplan/handlers/review.py
megaplan/handlers/finalize.py
megaplan/handlers/execute.py
megaplan/prompts/execute_doc.py
tests/test_handle_review_robustness.py
tests/test_parallel_review.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py",
  "limit": 150
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
9	from typing import TYPE_CHECKING, Any, Iterator
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

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"tomllib\\|PyYAML\" /Users/user_c042661f/Documents/megaplan/pyproject.toml /Users/user_c042661f/Documents/megaplan/megaplan/_core/io.py 2>/dev/null | head -20"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/pyproject.toml:22:    "PyYAML>=6.0",
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"import tomllib\\|import json\\|import yaml\" /Users/user_c042661f/Documents/megaplan/megaplan --include=\"*.py\" | head -20"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/audits/audit_engine.py:import json
/Users/user_c042661f/Documents/megaplan/megaplan/_core/io.py:import json
/Users/user_c042661f/Documents/megaplan/megaplan/chain.py:import json
/Users/user_c042661f/Documents/megaplan/megaplan/chain.py:    import yaml
/Users/user_c042661f/Documents/megaplan/megaplan/hermes_worker.py:import json
/Users/user_c042661f/Documents/megaplan/megaplan/cloud/providers/local.py:import json
/Users/user_c042661f/Documents/megaplan/megaplan/cloud/providers/railway.py:import json
/Users/user_c042661f/Documents/megaplan/megaplan/cloud/providers/ssh.py:import json
/Users/user_c042661f/Documents/megaplan/megaplan/cloud/spec.py:    import yaml
/Users/user_c042661f/Documents/megaplan/megaplan/cloud/cli.py:import json
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/tiebreaker_challenger.py:from megaplan._core import json_dump
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/review.py:import json
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/critique.py:    import json
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/critique.py:    import json
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/tiebreaker_orchestrator.py:import json
/Users/user_c042661f/Documents/megaplan/megaplan/workers.py:import json
/Users/user_c042661f/Documents/megaplan/megaplan/execute/timeout.py:import json
/Users/user_c042661f/Documents/megaplan/megaplan/key_pool.py:import json
/Users/user_c042661f/Documents/megaplan/megaplan/loop/prompts.py:import json
/Users/user_c042661f/Documents/megaplan/megaplan/auto.py:import json
```

> AGENT

Now let me check handlers/init.py to see how config is populated at init time:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def handle_init\\|config\\[\" /Users/user_c042661f/Documents/megaplan/megaplan/handlers/init.py | head -30"
}
```

> TOOL

tool_result Bash
```
25:def handle_init(root: Path, args: argparse.Namespace) -> StepResponse:
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers/init.py",
  "limit": 200
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	import argparse
4	from datetime import datetime
5	from pathlib import Path
6	from typing import Any
7	
8	from megaplan.doc_assembly import extract_settled_decisions
9	from megaplan.types import ROBUSTNESS_LEVELS, CliError, PlanState, STATE_INITIALIZED, StepResponse
10	from megaplan._core import (
11	    append_history,
12	    ensure_runtime_layout,
13	    find_command,
14	    get_effective,
15	    make_history_entry,
16	    now_utc,
17	    plans_root,
18	    save_state,
19	    slugify,
20	    workflow_next,
21	)
22	
23	from .shared import _append_to_meta, _attach_next_step_runtime, _validate_relative_path
24	
25	def handle_init(root: Path, args: argparse.Namespace) -> StepResponse:
26	    ensure_runtime_layout(root)
27	    project_dir = Path(args.project_dir).expanduser().resolve()
28	    if not project_dir.exists() or not project_dir.is_dir():
29	        raise CliError("invalid_project_dir", f"Project directory does not exist: {project_dir}")
30	    positional_idea = getattr(args, "idea", None)
31	    idea_file = getattr(args, "idea_file", None)
32	    if positional_idea and idea_file:
33	        raise CliError("invalid_args", "Pass either the positional idea or --idea-file, not both")
34	    if idea_file:
35	        idea_path = Path(idea_file).expanduser().resolve()
36	        try:
37	            idea_text = idea_path.read_text(encoding="utf-8").strip()
38	        except OSError as exc:
39	            raise CliError("invalid_args", f"Unable to read --idea-file {idea_path}: {exc}") from exc
40	        if not idea_text:
41	            raise CliError("invalid_args", "--idea-file must contain non-empty UTF-8 text")
42	    elif positional_idea:
43	        idea_text = positional_idea
44	    else:
45	        raise CliError("invalid_args", "Provide an idea argument or --idea-file <path>")
46	    explicit_mode = getattr(args, "mode", None)
47	    raw_output_path = getattr(args, "output", None)
48	    raw_primary_criterion = getattr(args, "primary_criterion", None)
49	    mode = explicit_mode or "code"
50	    if mode == "metaplan":
51	        mode = "doc"
52	    if raw_primary_criterion and mode != "joke":
53	        raise CliError("invalid_args", "--primary-criterion is only valid with --mode joke")
54	
55	    if mode == "code" and raw_output_path:
56	        raise CliError(
57	            "invalid_args",
58	            "--output is only valid with --mode doc or --mode joke. For code-mode runs, remove "
59	            "--output; for prose artifact runs, also pass --mode doc or --mode joke.",
60	        )
61	    normalized_output_path: str | None = None
62	    if mode in {"doc", "joke"} and not raw_output_path:
63	        raise CliError("invalid_args", f"--output is required when --mode {mode} is selected")
64	    if raw_output_path:
65	        normalized_output_path = _validate_relative_path(project_dir, raw_output_path, "--output")
66	    normalized_primary_criterion: str | None = None
67	    if raw_primary_criterion is not None:
68	        normalized_primary_criterion = str(raw_primary_criterion).strip()
69	        if not normalized_primary_criterion:
70	            raise CliError("invalid_args", "--primary-criterion must be non-empty when provided")
71	    raw_from_doc = getattr(args, "from_doc", None)
72	    from_doc_rel: str | None = None
73	    imported_decisions: list[dict[str, Any]] = []
74	    parse_warnings: list[str] = []
75	    if raw_from_doc:
76	        from_doc_rel = _validate_relative_path(project_dir, raw_from_doc, "--from-doc")
77	        from_doc_abs = project_dir / from_doc_rel
78	        if not from_doc_abs.exists() or not from_doc_abs.is_file():
79	            raise CliError("invalid_args", f"--from-doc path does not exist: {from_doc_rel}")
80	        imported_decisions, parse_warnings = extract_settled_decisions(
81	            from_doc_abs.read_text(encoding="utf-8")
82	        )
83	    robustness = getattr(args, "robustness", None)
84	    if robustness is None:
85	        robustness = get_effective("execution", "robustness")
86	    if robustness not in ROBUSTNESS_LEVELS:
87	        robustness = "standard"
88	    auto_approve_value = getattr(args, "auto_approve", None)
89	    if auto_approve_value is None:
90	        auto_approve_value = get_effective("execution", "auto_approve")
91	    auto_approve = bool(auto_approve_value)
92	    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
93	    plan_name = args.name or f"{slugify(idea_text)}-{timestamp}"
94	    plan_dir = plans_root(root) / plan_name
95	    if plan_dir.exists():
96	        raise CliError("duplicate_plan", f"Plan directory already exists: {plan_name}")
97	    plan_dir.mkdir(parents=True, exist_ok=False)
98	
99	    state: PlanState = {
100	        "name": plan_name,
101	        "idea": idea_text,
102	        "current_state": STATE_INITIALIZED,
103	        "iteration": 0,
104	        "created_at": now_utc(),
105	        "config": {
106	            "project_dir": str(project_dir),
107	            "auto_approve": auto_approve,
108	            "robustness": robustness,
109	            "mode": mode,
110	            "agent": "hermes" if getattr(args, "hermes", None) is not None else "",
111	        },
112	        "sessions": {},
113	        "plan_versions": [],
114	        "history": [],
115	        "meta": {
116	            "significant_counts": [],
117	            "weighted_scores": [],
118	            "plan_deltas": [],
119	            "recurring_critiques": [],
120	            "total_cost_usd": 0.0,
121	            "overrides": [],
122	            "notes": [],
123	        },
124	        "last_gate": {},
125	    }
126	    if normalized_output_path is not None:
127	        state["config"]["output_path"] = normalized_output_path
128	    if normalized_primary_criterion is not None:
129	        state["config"]["primary_criterion"] = normalized_primary_criterion
130	    if from_doc_rel is not None:
131	        state["config"]["from_doc"] = from_doc_rel
132	        state["meta"]["imported_decisions"] = imported_decisions
133	    for warning in parse_warnings:
134	        _append_to_meta(state, "notes", {"timestamp": now_utc(), "note": warning})
135	    append_history(
136	        state,
137	        make_history_entry(
138	            "init",
139	            duration_ms=0,
140	            cost_usd=0.0,
141	            result="success",
142	            environment={
143	                "claude": bool(find_command("claude")),
144	                "codex": bool(find_command("codex")),
145	            },
146	        ),
147	    )
148	    save_state(plan_dir, state)
149	    next_steps = workflow_next(state)
150	    response: StepResponse = {
151	        "success": True,
152	        "step": "init",
153	        "plan": plan_name,
154	        "state": STATE_INITIALIZED,
155	        "summary": f"Initialized plan '{plan_name}' for project {project_dir}",
156	        "artifacts": ["state.json"],
157	        "next_step": next_steps[0] if next_steps else None,
158	        "auto_approve": auto_approve,
159	        "robustness": robustness,
160	    }
161	    if parse_warnings:
162	        response["warnings"] = parse_warnings
163	    if bool(getattr(args, "auto_start", False)):
164	        from megaplan.auto import drive as auto_drive
165	
166	        outcome = auto_drive(
167	            plan_name,
168	            cwd=root,
169	        )
170	        response["auto_outcome"] = {
171	            "status": outcome.status,
172	            "plan": outcome.plan,
173	            "final_state": outcome.final_state,
174	            "iterations": outcome.iterations,
175	            "reason": outcome.reason,
176	            "last_phase": outcome.last_phase,
177	            "events": outcome.events,
178	        }
179	    _attach_next_step_runtime(response)
180	    return response
181	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Now let me check the git log to see recent work on hermes_worker.py and check for test structure:

> TOOL

tool_use Bash
```json
{
  "command": "git log --oneline -20 megaplan/hermes_worker.py 2>/dev/null | head -10"
}
```

> TOOL

tool_result Bash
```
650677b feat(cli): add --mode joke for film scene scripts
016645b refactor: split audit/execute modules into subpackages; remove legacy test_megaplan.py
9a55210 v0.15.0: doc-mode (metaplan) — execute produces a document instead of code
d820fde remove research phase — fold into prep
088f6db fix: report Z.AI 429s to key pool (1h cooldown for quota, 2m for rate limit)
4c5dc66 fix(review): pre-populate review template with task/sense-check IDs
99a49ed feat: track token usage per phase for cost analysis
43898f1 feat: add key pool, parallel critique, and pipeline improvements
86e6534 fix: make template file instructions explicit and actionable
1f6fe83 fix: add minimax: provider prefix routing in hermes_worker
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/tests/ | head -20"
}
```

> TOOL

tool_result Bash
```
total 1600
drwxr-xr-x   61 user_c042661f  staff   1952 Apr 22 04:51 .
drwxr-xr-x   25 user_c042661f  staff    800 Apr 22 04:57 ..
-rw-r--r--    1 user_c042661f  staff      0 Mar 20 17:09 __init__.py
drwxr-xr-x@ 221 user_c042661f  staff   7072 Apr 22 04:51 __pycache__
-rw-r--r--@   1 user_c042661f  staff   6110 Apr 21 13:19 conftest.py
drwxr-xr-x@   3 user_c042661f  staff     96 Apr 21 13:58 fixtures
-rw-r--r--@   1 user_c042661f  staff  12031 Apr 21 18:35 test_audits.py
-rw-r--r--@   1 user_c042661f  staff   7789 Apr 21 13:57 test_auto.py
-rw-r--r--@   1 user_c042661f  staff  17203 Apr 21 14:10 test_chain.py
-rw-r--r--    1 user_c042661f  staff   2627 Apr 21 18:51 test_checks.py
-rw-r--r--@   1 user_c042661f  staff   1698 Apr 21 14:55 test_cli_entry.py
-rw-r--r--@   1 user_c042661f  staff   8225 Apr 21 14:36 test_cloud_chain_status.py
-rw-r--r--@   1 user_c042661f  staff   8061 Apr 21 14:55 test_cloud_chain_wrapper.py
-rw-r--r--@   1 user_c042661f  staff   7380 Apr 21 18:26 test_cloud_cli_session.py
-rw-r--r--@   1 user_c042661f  staff   2164 Apr 21 05:30 test_cloud_docker_build.py
-rw-r--r--@   1 user_c042661f  staff   7338 Apr 21 14:34 test_cloud_local.py
-rw-r--r--@   1 user_c042661f  staff   2009 Apr 21 14:36 test_cloud_local_lifecycle.py
-rw-r--r--@   1 user_c042661f  staff   1683 Apr 21 14:35 test_cloud_logs_follow_redacted.py
-rw-r--r--@   1 user_c042661f  staff   4699 Apr 21 13:59 test_cloud_persistent_dir.py
```

> TOOL

tool_use Bash
```json
{
  "command": "head -30 /Users/user_c042661f/Documents/megaplan/tests/test_core.py"
}
```

> TOOL

tool_result Bash
```
from __future__ import annotations

import pytest

from megaplan._core import (
    add_or_increment_debt,
    batch_artifact_path,
    compute_global_batches,
    compute_task_batches,
    escalated_subsystems,
    extract_subsystem_tag,
    find_matching_debt,
    list_batch_artifacts,
    load_debt_registry,
    resolve_debt,
)


def _task(task_id: str, depends_on: list[str] | None = None) -> dict[str, object]:
    return {"id": task_id, "depends_on": depends_on or []}


def test_compute_task_batches_linear_chain() -> None:
    tasks = [_task("T1"), _task("T2", ["T1"]), _task("T3", ["T2"])]
    assert compute_task_batches(tasks) == [["T1"], ["T2"], ["T3"]]


def test_compute_task_batches_independent_tasks_share_batch() -> None:
    tasks = [_task("T1"), _task("T2"), _task("T3")]
    assert compute_task_batches(tasks) == [["T1", "T2", "T3"]]
```

> AGENT

Now let me verify the tiebreaker orchestrator parser and check the chain.py for YAML usage:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"build_tiebreaker_parser\\|build_chain_parser\" /Users/user_c042661f/Documents/megaplan/megaplan/prompts/tiebreaker_orchestrator.py /Users/user_c042661f/Documents/megaplan/megaplan/chain.py | head -20"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/tiebreaker_orchestrator.py:215:def build_tiebreaker_parser(subparsers: Any) -> None:
/Users/user_c042661f/Documents/megaplan/megaplan/chain.py:592:def build_chain_parser(subparsers: Any) -> None:
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/chain.py",
  "limit": 100
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

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Let me also check workers.py for parse_agent_spec usage and get the auto.py handler structure:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"parse_agent_spec\\|--hermes\\|--phase-model\" /Users/user_c042661f/Documents/megaplan/megaplan/workers.py | head -30"
}
```

> TOOL

tool_result Bash
```
32:    parse_agent_spec,
1623:    or from --phase-model / --hermes CLI flags. None means use agent default.
1627:    # Check --phase-model overrides first (highest priority)
1633:                agent, model = parse_agent_spec(pm_spec)
1636:        # Check --hermes flag
1646:                agent, model = parse_agent_spec(explicit)
1651:                agent, model = parse_agent_spec(spec)
1663:        # For hermes via --hermes flag, give a specific error
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def run_auto\\|def build_auto_parser\" /Users/user_c042661f/Documents/megaplan/megaplan/auto.py"
}
```

> TOOL

tool_result Bash
```
484:def build_auto_parser(subparsers: Any) -> None:
561:def run_auto(root: Path, args: argparse.Namespace) -> int:
```

> AGENT

Let me get the key areas for resolve_agent_and_model function:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/workers.py",
  "offset": 1620,
  "limit": 100
}
```

> TOOL

tool_result Read
```
1620	    call with no session saved.
1621	
1622	    The model is extracted from compound agent specs (e.g. 'hermes:openai/gpt-5')
1623	    or from --phase-model / --hermes CLI flags. None means use agent default.
1624	    """
1625	    model = None
1626	
1627	    # Check --phase-model overrides first (highest priority)
1628	    phase_models = getattr(args, "phase_model", None) or []
1629	    for pm in phase_models:
1630	        if "=" in pm:
1631	            pm_step, pm_spec = pm.split("=", 1)
1632	            if pm_step == step:
1633	                agent, model = parse_agent_spec(pm_spec)
1634	                break
1635	    else:
1636	        # Check --hermes flag
1637	        hermes_flag = getattr(args, "hermes", None)
1638	        if hermes_flag is not None:
1639	            agent = "hermes"
1640	            if isinstance(hermes_flag, str) and hermes_flag:
1641	                model = hermes_flag
1642	        else:
1643	            # Check explicit --agent flag
1644	            explicit = args.agent
1645	            if explicit:
1646	                agent, model = parse_agent_spec(explicit)
1647	            else:
1648	                # Fall back to config / defaults
1649	                config = load_config(home)
1650	                spec = config.get("agents", {}).get(step) or DEFAULT_AGENT_ROUTING[step]
1651	                agent, model = parse_agent_spec(spec)
1652	
1653	    # Validate agent availability
1654	    explicit_agent = args.agent  # was an explicit --agent flag used?
1655	    if not _is_agent_available(agent):
1656	        # If explicitly requested (via --agent), fail immediately
1657	        if explicit_agent and not any(pm.startswith(f"{step}=") for pm in (getattr(args, "phase_model", None) or [])):
1658	            if agent == "hermes":
1659	                from megaplan.hermes_worker import check_hermes_available
1660	                ok, msg = check_hermes_available()
1661	                raise CliError("agent_not_found", msg if not ok else f"Agent '{agent}' not found")
1662	            raise CliError("agent_not_found", f"Agent '{agent}' not found on PATH")
1663	        # For hermes via --hermes flag, give a specific error
1664	        if getattr(args, "hermes", None) is not None or agent == "hermes":
1665	            from megaplan.hermes_worker import check_hermes_available
1666	            ok, msg = check_hermes_available()
1667	            if not ok:
1668	                raise CliError("agent_not_found", msg)
1669	        # Try fallback
1670	        available = detect_available_agents()
1671	        if not available:
1672	            raise CliError(
1673	                "agent_not_found",
1674	                "No supported agents found. Install claude, codex, or hermes-agent.",
1675	            )
1676	        fallback = available[0]
1677	        args._agent_fallback = {
1678	            "requested": agent,
1679	            "resolved": fallback,
1680	            "reason": f"{agent} not available",
1681	        }
1682	        agent = fallback
1683	        model = None  # Reset model when falling back
1684	
1685	    ephemeral = getattr(args, "ephemeral", False)
1686	    fresh = getattr(args, "fresh", False)
1687	    persist = getattr(args, "persist", False)
1688	    conflicting = sum([fresh, persist, ephemeral])
1689	    if conflicting > 1:
1690	        raise CliError("invalid_args", "Cannot combine --fresh, --persist, and --ephemeral")
1691	    if ephemeral:
1692	        return agent, "ephemeral", True, model
1693	    refreshed = fresh
1694	    # Review with Claude: default to fresh to avoid self-bias (principle #5)
1695	    if step == "review" and agent == "claude":
1696	        if persist and not getattr(args, "confirm_self_review", False):
1697	            raise CliError("invalid_args", "Claude review requires --confirm-self-review when using --persist")
1698	        if not persist:
1699	            refreshed = True
1700	    return agent, "persistent", refreshed, model
1701	
1702	
1703	def run_step_with_worker(
1704	    step: str,
1705	    state: PlanState,
1706	    plan_dir: Path,
1707	    args: argparse.Namespace,
1708	    *,
1709	    root: Path,
1710	    resolved: tuple[str, str, bool, str | None] | None = None,
1711	    prompt_override: str | None = None,
1712	    prompt_kwargs: dict[str, Any] | None = None,
1713	) -> tuple[WorkerResult, str, str, bool]:
1714	    agent, mode, refreshed, model = resolved or resolve_agent_mode(step, args)
1715	    effective_refreshed = refreshed
1716	    explicit_agent = _agent_requested_explicitly(step, args)
1717	    attempted_agents: set[str] = set()
1718	    while True:
1719	        attempted_agents.add(agent)

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/auto.py",
  "offset": 484,
  "limit": 100
}
```

> TOOL

tool_result Read
```
484	def build_auto_parser(subparsers: Any) -> None:
485	    auto_parser = subparsers.add_parser(
486	        "auto",
487	        help="Drive a plan to completion without human intervention",
488	    )
489	    auto_parser.add_argument("--plan", required=True, help="Plan name")
490	    auto_parser.add_argument(
491	        "--stall-threshold",
492	        type=int,
493	        default=DEFAULT_STALL_THRESHOLD,
494	        help=(
495	            f"Exit if the plan state doesn't change for this many iterations "
496	            f"AND no new review.json has been written (default "
497	            f"{DEFAULT_STALL_THRESHOLD}). Use --max-review-rework-cycles for "
498	            "the rework-loop limit — execute rework can span many iterations "
499	            "with state pinned at 'finalized', which is not a real stall."
500	        ),
501	    )
502	    auto_parser.add_argument(
503	        "--max-iterations",
504	        type=int,
505	        default=DEFAULT_MAX_ITERATIONS,
506	        help=f"Hard cap on loop iterations (default {DEFAULT_MAX_ITERATIONS})",
507	    )
508	    auto_parser.add_argument(
509	        "--max-review-rework-cycles",
510	        type=int,
511	        default=DEFAULT_MAX_REVIEW_REWORK_CYCLES,
512	        help=(
513	            f"Cap on observed review→rework cycles before the driver bails "
514	            f"(default {DEFAULT_MAX_REVIEW_REWORK_CYCLES}). A rework cycle is "
515	            "counted each time review.json is rewritten while state appears "
516	            "stuck at 'finalized'. Mirrors execution.max_review_rework_cycles."
517	        ),
518	    )
519	    auto_parser.add_argument(
520	        "--on-escalate",
521	        choices=ESCALATE_ACTIONS,
522	        default="force-proceed",
523	        help="What to do when the gate escalates (default force-proceed)",
524	    )
525	    auto_parser.add_argument(
526	        "--poll-sleep",
527	        type=float,
528	        default=DEFAULT_POLL_SLEEP_SECONDS,
529	        help=f"Seconds to sleep between phase transitions (default {DEFAULT_POLL_SLEEP_SECONDS})",
530	    )
531	    auto_parser.add_argument(
532	        "--phase-timeout",
533	        type=float,
534	        default=DEFAULT_PHASE_TIMEOUT_SECONDS,
535	        help=(
536	            f"Seconds before a single phase subprocess (plan/prep/critique/gate/finalize/execute/review) "
537	            f"is killed and treated as a failure (default {DEFAULT_PHASE_TIMEOUT_SECONDS}s). "
538	            "Stall detection still applies on top."
539	        ),
540	    )
541	    auto_parser.add_argument(
542	        "--work-dir",
543	        default=None,
544	        help=(
545	            "Override the source-code working directory for subprocess workers "
546	            "(--add-dir / -C). Defaults to the current working directory."
547	        ),
548	    )
549	    auto_parser.add_argument(
550	        "--status-timeout",
551	        type=float,
552	        default=DEFAULT_STATUS_TIMEOUT_SECONDS,
553	        help=(
554	            f"Seconds before `megaplan status` / override subprocesses are killed "
555	            f"(default {DEFAULT_STATUS_TIMEOUT_SECONDS}s). These should always be quick; "
556	            "hitting this indicates serious trouble."
557	        ),
558	    )
559	
560	
561	def run_auto(root: Path, args: argparse.Namespace) -> int:
562	    """CLI entry point. Returns a POSIX exit code suitable for ``sys.exit``."""
563	    outcome = drive(
564	        args.plan,
565	        cwd=root,
566	        stall_threshold=args.stall_threshold,
567	        max_iterations=args.max_iterations,
568	        max_review_rework_cycles=args.max_review_rework_cycles,
569	        on_escalate=args.on_escalate,
570	        poll_sleep=args.poll_sleep,
571	        phase_timeout=args.phase_timeout,
572	        status_timeout=args.status_timeout,
573	    )
574	    sys.stdout.write(outcome.to_json() + "\n")
575	    if outcome.status == "done":
576	        return 0
577	    if outcome.status == "aborted":
578	        return 0  # user-requested abort is not a failure
579	    if outcome.status == "stalled":
580	        return 2
581	    if outcome.status == "escalated":
582	        return 3
583	    if outcome.status == "cap":

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Perfect! Now let me compile the final report. I have enough information to provide a comprehensive analysis.

## Summary Report: Model-Profile Feature Exploration

Based on systematic exploration of the megaplan codebase, here are the key findings organized by requirement:

### 1. **CLI Surface** (`megaplan/cli.py`)

**Subcommands with `--phase-model` and `--hermes` arguments:**
- **init** (line 869-872): `--hermes` with optional model, `--phase-model` with append action
- **plan, prep, critique, revise, gate, finalize, execute, review** (lines 895-914): all have both flags
- **loop-init** (lines 985-988): both flags present
- **loop-run** (lines 1002-1005): both flags present
- **tiebreaker-run** (lines 1039-1046): both flags present
- **chain** (via `build_chain_parser` at line 1025): not visible in main cli.py but uses same pattern
- **tiebreaker** (via `build_tiebreaker_parser` at line 1034): external builder

**Pattern used:** Repeated code blocks—no shared helper. Each parser explicitly adds both arguments (lines 871-872, 898-901, 985-988, 1002-1005, 1045-1046).

**Existing config structure:** `config show/set/reset` subcommand exists (lines 916-922). Currently supports `agents.<step>` config keys and direct settings. No `profiles` subcommand yet.

### 2. **DEFAULT_AGENT_ROUTING** (`megaplan/types.py`, lines 305-318)

Complete routing table confirmed:
```python
DEFAULT_AGENT_ROUTING = {
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
```
No `tiebreaker_orchestrator` or `tiebreaker_synthesis` as phase keys; these are orchestration phases, not routing targets.

### 3. **parse_agent_spec** (`megaplan/types.py`, lines 321-326)

Location: `/Users/user_c042661f/Documents/megaplan/megaplan/types.py:321`

Implementation:
```python
def parse_agent_spec(spec: str) -> tuple[str, str | None]:
    """Parse 'hermes:model/name' → ('hermes', 'model/name') or 'claude' → ('claude', None)."""
    if ":" in spec:
        agent, model = spec.split(":", 1)
        return agent, model
    return spec, None
```

**Usage in workers.py** (line 1633, 1646, 1651): Called to extract model from `--phase-model` and `--hermes` arguments.

### 4. **load_config** (`megaplan/_core/io.py`, lines 229-241)

Location: `/Users/user_c042661f/Documents/megaplan/megaplan/_core/io.py:229`

- Reads from `~/.config/megaplan/config.json` (XDG_CONFIG_HOME aware)
- Format: JSON dict
- Currently stores: `agents` (routing map) and various execution settings (`auto_approve`, `robustness`, worker timeouts, etc.)
- Config is loaded at runtime and merged with `DEFAULTS` via `get_effective()`

**save_config**: Line 244—writes same JSON format atomically.

### 5. **state.py** (`megaplan/_core/state.py`)

**state["config"]** structure initialized at plan init (`megaplan/handlers/init.py:105-111`):
```python
"config": {
    "project_dir": str(project_dir),
    "auto_approve": auto_approve,
    "robustness": robustness,
    "mode": mode,
    "agent": "hermes" if getattr(args, "hermes", None) is not None else "",
}
```

Additional config keys added conditionally:
- `output_path` (line 127, for doc/joke modes)
- `primary_criterion` (line 129, for joke mode)
- `from_doc` (line 131, for doc imports)

**Note:** Currently only stores a simple boolean "agent" flag, not full routing. Phase models are resolved on-the-fly from CLI args.

### 6. **Config Parser Usage** (`megaplan/_core/io.py` and `megaplan/chain.py`)

- **JSON**: Main format used (io.py, atomic_write_json)
- **PyYAML**: Required dependency (pyproject.toml:22). Used in `megaplan/chain.py` for milestone specs (line 40-45)
- **tomllib**: Not used anywhere in codebase
- No existing TOML parsing infrastructure

### 7. **Test Layout**

Location: `/Users/user_c042661f/Documents/megaplan/tests/`

Framework: **pytest** (specified in `pyproject.toml:32-33`)

Test pattern observed in `test_core.py`:
- Imports from `megaplan._core`
- Uses pytest fixtures
- Conftest.py provides shared fixtures (line 6 of test_core.py references conftest)

For new model-profile tests: Follow pattern of `test_workers.py` or `test_config.py` (both exist in tests/). Place in `tests/test_profiles.py`.

### 8. **Hermes Vendor Status** (`megaplan/hermes_worker.py`)

Location: `/Users/user_c042661f/Documents/megaplan/megaplan/hermes_worker.py`

Git history (last 10 commits) shows:
- No recent splits or in-flight refactoring
- Module is stable; last notable change was "minimax: provider prefix routing in hermes_worker" (commit 1f6fe83)
- hermes_worker.py imports from `megaplan.workers` (WorkerResult, STEP_SCHEMA_FILENAMES, validate_payload)
- check_hermes_available() function handles dependency + API key validation (lines 23-49)

### Key Observations for Model-Profile Design

1. **Current per-phase model resolution** happens in `workers.py:resolve_agent_mode()` (line 1714+) by checking:
   - `--phase-model step=hermes:model/name` (highest priority)
   - `--hermes model` flag (fallback)
   - `--agent hermes` flag
   - Global config agents routing
   - DEFAULT_AGENT_ROUTING

2. **No persistent profile storage** in config.json yet—only runtime CLI overrides.

3. **State['config']['agent']** stores only boolean, not full routing—profiles should enhance this.

4. **Test coverage exists** for workers (test_workers.py) and config (test_config.py); new tests should follow atomic, focused patterns.

**Files to modify for profiles feature:**
- `megaplan/types.py`: Add ProfileConfig TypedDict, extend PlanConfig
- `megaplan/cli.py`: Add `config profiles list/show/create/delete` subcommands
- `megaplan/_core/io.py`: Add load_profiles(), save_profiles()
- `megaplan/handlers/init.py`: Wire profile selection into state["config"]
- `megaplan/workers.py`: Update resolve_agent_mode() to check profile lookup
- `tests/test_profiles.py`: New test file
