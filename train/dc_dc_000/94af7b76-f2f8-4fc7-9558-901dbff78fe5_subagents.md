> DEVELOPER

I'm planning a Sprint 2 feature for the `megaplan` CLI at /Users/user_c042661f/Documents/megaplan/: a `megaplan bakeoff` subcommand that runs the same idea through N profiles concurrently in git worktrees, then compares and merges results.

I need a thorough but focused map of the current codebase, NOT prior plan artifacts (ignore `.megaplan/` directories). Focus on source in `megaplan/` and relevant tests.

Report (be concise, use file:line refs):

1. **CLI structure**: Where is the top-level argparse wired? How are subcommands registered? (Look at `megaplan/cli.py`, `megaplan/__main__.py`.) I need to know how to add a new `bakeoff` subcommand group with sub-subcommands like `bakeoff run`, `bakeoff status`, etc.

2. **`megaplan auto` driver**: Where does it live (probably `megaplan/auto.py`)? What's its entry point / signature? How does it know which plan dir to operate on — is it CWD-based, or explicit flag? What is the `DriverOutcome` type and where is `DriverOutcome.status` defined? List the status values.

3. **Plan state**: Where is `state.json` written and loaded? What's the structure (especially `state.json.config.project_dir` which the brief mentions contains absolute paths)? What directory does `.megaplan/plans/<plan-id>/` contain?

4. **Profiles**: How are named profiles defined (`megaplan/profiles/`)? What's the format of `standard.toml`? How are they loaded and how does `--profile` flag work currently?

5. **Plan directory discovery**: Grep for `rglob` and `.megaplan` to understand the "circular recursion" risk the brief mentions — how does megaplan currently find plan dirs?

6. **Step receipts (Sprint 1 prerequisite)**: Grep for "receipt" or "step_receipt" or similar. Does this concept exist in the codebase already? Is there a canonical prompt hash? A global audit log? The brief says these are a prerequisite — I need to know whether they're implemented or still pending, because bakeoff compare uses receipts as the primary metric source.

7. **Scope drift**: Grep for "scope_drift" or "scope drift" — is this a first-class metric already?

8. **Existing subprocess orchestration**: Does `megaplan` already shell out to itself or to other processes? Any use of `asyncio.create_subprocess_exec` or `subprocess.Popen`? The brief says "auto-driver already shells out per phase" — verify.

9. **Tests**: What's the test layout at `/Users/user_c042661f/Documents/megaplan/tests/`? How are CLI subcommands typically tested?

10. **Git worktree usage**: Any existing worktree code in the repo?

11. **Phase artifacts**: Where does each phase write its artifact (plan_v1.md, critique_v*.json, execution.json, review_output.json)? Just the directory layout, not the full contents.

12. **pyproject.toml**: What's the package name, Python version, current deps (especially asyncio-related, toml parsing)?

Keep it tight — I need enough to write concrete file/line references in a plan, not a full tutorial.

> AGENT

I'll conduct a focused exploration of the megaplan codebase to answer your questions. Let me start with the overall structure and then drill into specifics.

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan -type f -name \"*.py\" | head -30"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/evals/__init__.py
/Users/user_c042661f/Documents/megaplan/evals/benchmarks/swe_bench.py
/Users/user_c042661f/Documents/megaplan/evals/benchmarks/__init__.py
/Users/user_c042661f/Documents/megaplan/megaplan/audits/iteration.py
/Users/user_c042661f/Documents/megaplan/megaplan/audits/quality_gates.py
/Users/user_c042661f/Documents/megaplan/megaplan/audits/__init__.py
/Users/user_c042661f/Documents/megaplan/megaplan/audits/audit_engine.py
/Users/user_c042661f/Documents/megaplan/megaplan/audits/robustness.py
/Users/user_c042661f/Documents/megaplan/megaplan/audits/capabilities.py
/Users/user_c042661f/Documents/megaplan/megaplan/audits/hermes_vendoring.py
/Users/user_c042661f/Documents/megaplan/megaplan/audits/verifiability.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/io.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/phase_runtime.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/__init__.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/workflow.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/registries.py
/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py
/Users/user_c042661f/Documents/megaplan/megaplan/chain.py
/Users/user_c042661f/Documents/megaplan/megaplan/flags.py
/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py
/Users/user_c042661f/Documents/megaplan/megaplan/__init__.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/batch_runner.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/honcho_integration/client.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/honcho_integration/session.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/honcho_integration/__init__.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/honcho_integration/cli.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/hermes_constants.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/evals/watch_scoring_all.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/evals/consolidate.py
/Users/user_c042661f/Documents/megaplan/megaplan/agent/evals/config.py
```

> AGENT

Now let me explore the main entry points and structure:

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

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
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
72	from megaplan.profiles import (
73	    load_profile_sources,
74	    load_profiles,
75	    resolve_profile,
76	)
77	from megaplan.step_edit import handle_step
78	
79	
80	def render_response(response: StepResponse, *, exit_code: int = 0) -> int:
81	    print(json_dump(response), end="")
82	    return exit_code
83	
84	
85	def _resolve_error_plan_dir(root: Path | None, error: CliError) -> Path | None:
86	    if root is None or error.code != "plan_locked" or not isinstance(error.extra, dict):
87	        return None
88	    plan_name = error.extra.get("plan")
89	    if not isinstance(plan_name, str) or not plan_name:
90	        return None
91	    try:
92	        return resolve_plan_dir(root, plan_name)
93	    except CliError:
94	        return None
95	
96	
97	def _augment_plan_locked_error(
98	    payload: StepResponse,
99	    error: CliError,
100	    *,
101	    root: Path | None,
102	) -> None:
103	    plan_dir = _resolve_error_plan_dir(root, error)
104	    details = payload.get("details")
105	    if not isinstance(details, dict):
106	        details = None
107	    plan_name = (details or {}).get("plan")
108	    if isinstance(plan_name, str) and plan_name:
109	        monitor_hint = build_monitor_hint(plan_dir or Path(plan_name))
110	        payload["monitor_hint"] = monitor_hint
111	        if details is not None:
112	            details["monitor_hint"] = monitor_hint
113	    raw_active_step = (details or {}).get("active_step")
114	    if isinstance(raw_active_step, dict):
115	        active_step = (
116	            _build_active_step(raw_active_step, plan_dir=plan_dir)
117	            if plan_dir is not None
118	            else dict(raw_active_step)
119	        )
120	        payload["active_step"] = active_step
121	        if details is not None:
122	            details["active_step"] = active_step
123	
124	
125	def error_response(error: CliError, *, root: Path | None = None) -> int:
126	    payload: StepResponse = {
127	        "success": False,
128	        "error": error.code,
129	        "message": error.message,
130	    }
131	    if error.valid_next:
132	        payload["valid_next"] = error.valid_next
133	    if error.extra:
134	        payload["details"] = dict(error.extra)
135	    if error.code == "plan_locked":
136	        _augment_plan_locked_error(payload, error, root=root)
137	    return render_response(payload, exit_code=error.exit_code)
138	
139	
140	def _parse_utc_timestamp(timestamp: str | None) -> datetime | None:
141	    if not isinstance(timestamp, str) or not timestamp:
142	        return None
143	    try:
144	        return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
145	    except ValueError:
146	        return None
147	
148	
149	def _build_progress_payload(plan_dir: Path, state: dict[str, Any]) -> dict[str, Any]:
150	    finalize_path = plan_dir / "finalize.json"
151	    if not finalize_path.exists():
152	        return {
153	            "summary": "No finalize.json yet — plan has not been finalized.",
154	            "tasks_total": 0,
155	            "tasks_done": 0,
156	            "tasks_skipped": 0,
157	            "tasks_pending": 0,
158	            "tasks_blocked": 0,
159	            "batches_total": 0,
160	            "batches_completed": 0,
161	            "tasks": [],
162	        }
163	    finalize_data = read_json(finalize_path)
164	    global_batches = compute_global_batches(finalize_data)
165	    tasks = finalize_data.get("tasks", [])
166	    task_id_to_batch: dict[str, int] = {}
167	    for batch_idx, batch_ids in enumerate(global_batches, start=1):
168	        for task_id in batch_ids:
169	            task_id_to_batch[task_id] = batch_idx
170	    tasks_done = sum(1 for t in tasks if t.get("status") == "done")
171	    tasks_skipped = sum(1 for t in tasks if t.get("status") == "skipped")
172	    tasks_pending = sum(1 for t in tasks if t.get("status") == "pending")
173	    tasks_blocked = sum(1 for t in tasks if t.get("status") == "blocked")
174	    tasks_total = len(tasks)
175	    completed_ids = {
176	        t["id"] for t in tasks if t.get("status") in {"done", "skipped"} and isinstance(t.get("id"), str)
177	    }
178	    batches_completed = sum(
179	        1
180	        for batch_ids in global_batches
181	        if all(tid in completed_ids for tid in batch_ids)
182	    )
183	    task_status_list = [
184	        {
185	            "id": t.get("id", ""),
186	            "status": t.get("status", "pending"),
187	            "batch": task_id_to_batch.get(t.get("id", ""), 0),
188	        }
189	        for t in tasks
190	    ]
191	    return {
192	        "summary": (
193	            f"Execution progress: {tasks_done + tasks_skipped}/{tasks_total} tasks tracked, "
194	            f"{batches_completed}/{len(global_batches)} batches completed. "
195	            "Progress reflects the last finalize.json write (between-batch granularity)."
196	        ),
197	        "tasks_total": tasks_total,
198	        "tasks_done": tasks_done,
199	        "tasks_skipped": tasks_skipped,
200	        "tasks_pending": tasks_pending,
201	        "tasks_blocked": tasks_blocked,
202	        "batches_total": len(global_batches),
203	        "batches_completed": batches_completed,
204	        "tasks": task_status_list,
205	    }
206	
207	
208	def _build_last_step(state: dict[str, Any]) -> dict[str, Any] | None:
209	    history = state.get("history", [])
210	    if not isinstance(history, list) or not history:
211	        return None
212	    last = history[-1]
213	    if not isinstance(last, dict):
214	        return None
215	    return {
216	        "step": last.get("step"),
217	        "result": last.get("result"),
218	        "timestamp": last.get("timestamp"),
219	        "agent": last.get("agent"),
220	        "output_file": last.get("output_file"),
221	    }
222	
223	
224	def _build_active_step(active_step: Any, *, plan_dir: Path) -> dict[str, Any] | None:
225	    if not isinstance(active_step, dict):
226	        return None
227	    details = dict(active_step)
228	    step = details.get("step")
229	    if not isinstance(step, str) or not step:
230	        return details
231	    configured_timeout_seconds = int(get_effective("execution", "worker_timeout_seconds"))
232	    lock_held = plan_lock_is_held(plan_dir)
233	    started_at = _parse_utc_timestamp(details.get("started_at"))
234	    if started_at is not None:
235	        age_seconds = max(0, int((datetime.now(timezone.utc) - started_at).total_seconds()))
236	        details.update(
237	            build_phase_observability(
238	                step,
239	                configured_timeout_seconds=configured_timeout_seconds,
240	                age_seconds=age_seconds,
241	                lock_held=lock_held,
242	            )
243	        )
244	        if details.get("stale"):
245	            orphaned = not lock_held
246	            details["orphaned"] = orphaned
247	            if orphaned:
248	                if step == "execute":
249	                    details["recovery_hint"] = (
250	                        "The active step is stale and no process holds the plan lock. "
251	                        "Safe next action: rerun the same execute command on Codex without --fresh."
252	                    )
253	                else:
254	                    details["recovery_hint"] = (
255	                        "The active step is stale and no process holds the plan lock. "
256	                        "Safe next action: rerun the same step on the same agent before escalating."
257	                    )
258	        max_seconds = int(details.get("expected_duration_seconds", {}).get("max", 0) or 0)
259	        elapsed_label = humanize_seconds(age_seconds)
260	        if details.get("stale"):
261	            details["phase_progress_summary"] = (
262	                f"{step} stale ({elapsed_label} elapsed, expected max {humanize_seconds(max_seconds)}) "
263	                "see recovery_hint."
264	            )
265	        elif step in {"execute", "loop_execute"}:
266	            details["phase_progress_summary"] = (
267	                f"{step} running ({elapsed_label} elapsed, use progress for batch-level detail)."
268	            )
269	        else:
270	            details["phase_progress_summary"] = (
271	                f"{step} running ({elapsed_label} elapsed, typically completes within "
272	                f"{humanize_seconds(max_seconds)})."
273	            )
274	            if max_seconds > 0:
275	                details["progress_pct"] = min(95, int((age_seconds / max_seconds) * 100))
276	    else:
277	        details.update(
278	            build_phase_observability(
279	                step,
280	                configured_timeout_seconds=configured_timeout_seconds,
281	                lock_held=lock_held,
282	            )
283	        )
284	        if step in {"execute", "loop_execute"}:
285	            details["phase_progress_summary"] = (
286	                f"{step} active (start time unknown, use progress for batch-level detail)."
287	            )
288	        else:
289	            details["phase_progress_summary"] = f"{step} active (start time unknown)."
290	    return details
291	
292	
293	def _build_status_payload(plan_dir: Path, state: dict[str, Any]) -> StepResponse:
294	    next_steps = infer_next_steps(state)
295	    notes = state.get("meta", {}).get("notes", [])
296	    lock_path = plan_dir / ".plan.lock"
297	    lock_file_present = lock_path.exists()
298	    lock_held = plan_lock_is_held(plan_dir)
299	    active_step = _build_active_step(state.get("active_step"), plan_dir=plan_dir)
300	    last_step = _build_last_step(state)
301	    plan_mode = state.get("config", {}).get("mode", "code")
302	    plan_output_path = state.get("config", {}).get("output_path")
303	    summary = f"Plan '{state['name']}' is currently in state '{state['current_state']}'."
304	    if plan_mode in {"doc", "joke"}:
305	        summary += f" Mode: {plan_mode}. Output: {plan_output_path}."
306	    if active_step:
307	        summary = (
308	            summary
309	            + f" Active step: {active_step.get('step')} via {active_step.get('agent')}."
310	        )
311	    elif lock_file_present and not lock_held:
312	        summary = (
313	            summary
314	            + " No active step. The `.plan.lock` file may remain on disk even when no process holds the lock."
315	        )
316	    response: StepResponse = {
317	        "success": True,
318	        "step": "status",
319	        "plan": state["name"],
320	        "state": state["current_state"],
321	        "iteration": state["iteration"],
322	        "summary": summary,
323	        "next_step": next_steps[0] if next_steps else None,
324	        "valid_next": next_steps,
325	        "artifacts": sorted(
326	            path.name
327	            for path in plan_dir.iterdir()
328	            if path.is_file() and path.name != ".plan.lock"
329	        ),
330	        "lock_file_present": lock_file_present,
331	        "lock_held": lock_held,
332	        "active_step": active_step,
333	        "last_step": last_step,
334	        "total_cost_usd": state.get("meta", {}).get("total_cost_usd", 0.0),
335	        "mode": plan_mode,
336	        "output_path": plan_output_path,
337	        "notes_count": len(notes) if isinstance(notes, list) else 0,
338	        "notes": notes if isinstance(notes, list) else [],
339	        "session_summaries": [
340	            {"key": key, **value}
341	            for key, value in sorted(state.get("sessions", {}).items())
342	            if isinstance(value, dict)
343	        ],
344	    }
345	    runtime = build_next_step_runtime(
346	        response.get("next_step"),
347	        configured_timeout_seconds=int(get_effective("execution", "worker_timeout_seconds")),
348	    )
349	    if runtime is not None:
350	        response["next_step_runtime"] = runtime
351	    progress = _build_progress_payload(plan_dir, state) if (plan_dir / "finalize.json").exists() else None
352	    if progress is not None:
353	        response["progress"] = progress
354	        response["summary"] = response["summary"] + " " + progress["summary"]
355	    return response
356	
357	
358	def handle_status(root: Path, args: argparse.Namespace) -> StepResponse:
359	    if getattr(args, "pending_human", False):
360	        items = []
361	        for pd in active_plan_dirs(root):
362	            st = read_json(pd / "state.json")
363	            if st.get("current_state") == "awaiting_human_verify":
364	                items.append({"name": st["name"], "state": st["current_state"]})
365	        return {
366	            "success": True,
367	            "step": "status",
368	            "summary": f"Found {len(items)} plan(s) awaiting human verification.",
369	            "plans": items,
370	        }
371	    plan_dir, state = load_plan(root, args.plan)
372	    return _build_status_payload(plan_dir, state)
373	
374	
375	def handle_audit(root: Path, args: argparse.Namespace) -> StepResponse:
376	    plan_dir, state = load_plan(root, args.plan)
377	    return {
378	        "success": True,
379	        "step": "audit",
380	        "plan": state["name"],
381	        "plan_dir": str(plan_dir),
382	        "state": state,
383	    }
384	
385	
386	def handle_progress(root: Path, args: argparse.Namespace) -> StepResponse:
387	    plan_dir, state = load_plan(root, args.plan)
388	    progress = _build_progress_payload(plan_dir, state)
389	    return {
390	        "success": True,
391	        "step": "progress",
392	        "plan": state["name"],
393	        **progress,
394	    }
395	
396	
397	def handle_watch(root: Path, args: argparse.Namespace) -> StepResponse:
398	    response = handle_status(root, args)
399	    response["step"] = "watch"
400	    return response
401	
402	
403	def _collect_megaplan_roots(root: Path, *, tree: bool = False, all_system: bool = False) -> list[Path]:
404	    """Collect .megaplan root directories based on search mode."""
405	    roots: list[Path] = [root]
406	
407	    if all_system:
408	        # Search from home directory downward for all .megaplan directories
409	        home = Path.home()
410	        for megaplan_dir in sorted(home.rglob(".megaplan")):
411	            if megaplan_dir.is_dir() and (megaplan_dir / "plans").is_dir():
412	                candidate = megaplan_dir.parent
413	                if candidate.resolve() != root.resolve():
414	                    roots.append(candidate)
415	    elif tree:
416	        # Walk up to find parent .megaplan directories
417	        current = root.resolve().parent
418	        while True:
419	            if (current / ".megaplan" / "plans").is_dir() and current.resolve() != root.resolve():
420	                roots.append(current)
421	            parent = current.parent
422	            if parent == current:
423	                break
424	            current = parent
425	        # Walk down to find child .megaplan directories
426	        for megaplan_dir in sorted(root.rglob(".megaplan")):
427	            if megaplan_dir.is_dir() and (megaplan_dir / "plans").is_dir():
428	                candidate = megaplan_dir.parent
429	                if candidate.resolve() != root.resolve():
430	                    roots.append(candidate)
431	
432	    return roots
433	
434	
435	def handle_list(root: Path, args: argparse.Namespace) -> StepResponse:
436	    ensure_runtime_layout(root)
437	    filter_status = getattr(args, "filter_status", None)
438	    no_tree = getattr(args, "no_tree", False)
439	    include_done = getattr(args, "include_done", False)
440	    show_summary = getattr(args, "summary", False)
441	    search_all = getattr(args, "all", False)
442	    # Default: tree=True (parent+child), active-only (exclude done/aborted)
443	    # --status overrides the active filter (explicit filter = show exactly that)
444	    search_tree = not no_tree and not search_all
445	    filter_active = not include_done and not filter_status
446	
447	    roots = _collect_megaplan_roots(root, tree=search_tree, all_system=search_all)
448	    total_scanned = 0
449	    allowed_states: set[str] | None = None
450	    if filter_status:
451	        allowed_states = {s.strip() for s in filter_status.split(",")}
452	
453	    items = []
454	    state_counts: dict[str, int] = {}
455	    resolved_root = root.resolve()
456	    for search_root in roots:
457	        resolved_search = search_root.resolve()
458	        is_local = resolved_search == resolved_root
459	        for plan_dir in active_plan_dirs(search_root):
460	            state = read_json(plan_dir / "state.json")
461	            current_state = state["current_state"]
462	            state_counts[current_state] = state_counts.get(current_state, 0) + 1
463	            total_scanned += 1
464	
465	            if filter_active and current_state in TERMINAL_STATES:
466	                continue
467	            if allowed_states and current_state not in allowed_states:
468	                continue
469	
470	            next_steps = infer_next_steps(state)
471	            entry = {
472	                "name": state["name"],
473	                "idea": state["idea"],
474	                "state": current_state,
475	                "iteration": state["iteration"],
476	                "next_step": next_steps[0] if next_steps else None,
477	            }
478	            if not is_local:
479	                try:
480	                    rel = resolved_search.relative_to(resolved_root)
481	                    entry["location"] = f"./{rel}"
482	                    entry["direction"] = "child"
483	                except ValueError:
484	                    try:
485	                        resolved_root.relative_to(resolved_search)
486	                        entry["location"] = os.path.relpath(resolved_search, resolved_root)
487	                        entry["direction"] = "parent"
488	                    except ValueError:
489	                        entry["location"] = str(resolved_search)
490	                        entry["direction"] = "external"
491	            items.append(entry)
492	
493	    summary_parts = [f"Found {len(items)} plans"]
494	    if len(roots) > 1:
495	        summary_parts.append(f"across {len(roots)} directories")
496	    if allowed_states:
497	        summary_parts.append(f"matching {','.join(sorted(allowed_states))}")
498	    if filter_active:
499	        summary_parts.append("(active only)")
500	
501	    result: StepResponse = {
502	        "success": True,
503	        "step": "list",
504	        "summary": f"{'. '.join(summary_parts)}.",
505	        "plans": items,
506	    }
507	    if show_summary:
508	        result["state_summary"] = dict(sorted(state_counts.items()))
509	
510	    # Hints for discovering more plans
511	    hidden_done = total_scanned - len(items) if filter_active else 0
512	    hints: list[str] = []
513	    if hidden_done > 0:
514	        hints.append(f"{hidden_done} completed plans hidden (use --include-done to show)")
515	    if not search_all:
516	        hints.append("Use --all to search all plans system-wide")
517	    if hints:
518	        result["hints"] = hints
519	
520	    return result
521	
522	
523	def handle_debt(root: Path, args: argparse.Namespace) -> StepResponse:
524	    ensure_runtime_layout(root)
525	    action = args.debt_action
526	    registry = load_debt_registry(root)
527	    default_plan_id = getattr(args, "plan", None) or "manual"
528	
529	    if action == "list":
530	        entries = registry["entries"] if args.all else [entry for entry in registry["entries"] if not entry["resolved"]]
531	        grouped: dict[str, list[dict[str, Any]]] = {}
532	        for entry in entries:
533	            grouped.setdefault(entry["subsystem"], []).append(entry)
534	        escalated = {
535	            subsystem: total
536	            for subsystem, total, _entries in escalated_subsystems(registry)
537	        }
538	        by_subsystem = [
539	            {
540	                "subsystem": subsystem,
541	                "escalated": subsystem in escalated,
542	                "total_occurrences": subsystem_occurrence_total(entries_for_subsystem)
543	                if not args.all
544	                else sum(entry["occurrence_count"] for entry in entries_for_subsystem if not entry["resolved"]),
545	                "entries": entries_for_subsystem,
546	            }
547	            for subsystem, entries_for_subsystem in sorted(grouped.items())
548	        ]
549	        return {
550	            "success": True,
551	            "step": "debt",
552	            "action": "list",
553	            "summary": f"Found {len(entries)} debt entries across {len(by_subsystem)} subsystem groups.",
554	            "details": {
555	                "entries": entries,
556	                "by_subsystem": by_subsystem,
557	                "escalated_subsystems": [
558	                    {"subsystem": subsystem, "total_occurrences": total}
559	                    for subsystem, total in sorted(escalated.items())
560	                ],
561	            },
562	        }
563	
564	    if action == "add":
565	        flag_ids = [
566	            flag_id.strip()
567	            for flag_id in (args.flag_ids or "").split(",")
568	            if flag_id.strip()
569	        ]
570	        entry = add_or_increment_debt(
571	            registry,
572	            subsystem=args.subsystem,
573	            concern=args.concern,
574	            flag_ids=flag_ids,
575	            plan_id=default_plan_id,
576	        )
577	        save_debt_registry(root, registry)
578	        return {
579	            "success": True,
580	            "step": "debt",
581	            "action": "add",
582	            "summary": f"Tracked debt entry {entry['id']} for subsystem '{entry['subsystem']}'.",
583	            "details": {"entry": entry},
584	        }
585	
586	    if action == "resolve":
587	        entry = resolve_debt(registry, args.debt_id, default_plan_id)
588	        save_debt_registry(root, registry)
589	        return {
590	            "success": True,
591	            "step": "debt",
592	            "action": "resolve",
593	            "summary": f"Resolved debt entry {entry['id']}.",
594	            "details": {"entry": entry},
595	        }
596	
597	    raise CliError("invalid_args", f"Unknown debt action: {action}")
598	
599	
600	# ---------------------------------------------------------------------------
601	# Setup and config
602	# ---------------------------------------------------------------------------
603	
604	def _canonical_instructions() -> str:
605	    return resources.files("megaplan").joinpath("data", "instructions.md").read_text(encoding="utf-8")
606	
607	
608	_SKILL_HEADER = """\
609	---
610	name: megaplan
611	description: AI agent harness for coordinating Claude and GPT to make and execute extremely robust plans.
612	---
613	
614	"""
615	
616	_CURSOR_HEADER = """\
617	---
618	description: Use megaplan for high-rigor planning on complex, high-risk, or multi-stage tasks.
619	alwaysApply: false
620	---
621	
622	"""
623	
624	
625	def bundled_agents_md() -> str:
626	    return _canonical_instructions()
627	
628	
629	def _subagent_appendix(filename: str) -> str:
630	    content = resources.files("megaplan").joinpath("data", filename).read_text(encoding="utf-8")
631	    content = content.replace(
632	        "{max_execute_no_progress}",
633	        str(get_effective("execution", "max_execute_no_progress")),
634	    )
635	    content = content.replace(
636	        "{max_review_rework_cycles}",
637	        str(get_effective("execution", "max_review_rework_cycles")),
638	    )
639	    return content
640	
641	
642	def _claude_subagent_appendix() -> str:
643	    return _subagent_appendix("claude_subagent_appendix.md")
644	
645	
646	def _codex_subagent_appendix() -> str:
647	    return _subagent_appendix("codex_subagent_appendix.md")
648	
649	
650	def bundled_global_file(name: str) -> str:
651	    content = _canonical_instructions()
652	    if name == "claude_skill.md":
653	        return _SKILL_HEADER + content + "\n\n" + _claude_subagent_appendix()
654	    if name == "codex_skill.md":
655	        return _SKILL_HEADER + content + "\n\n" + _codex_subagent_appendix()
656	    if name == "skill.md":
657	        return _SKILL_HEADER + content
658	    if name == "cursor_rule.mdc":
659	        return _CURSOR_HEADER + content
660	    return content
661	
662	
663	_GLOBAL_TARGETS = [
664	    {"agent": "claude", "detect": ".claude", "path": ".claude/skills/megaplan/SKILL.md", "data": "claude_skill.md"},
665	    {"agent": "codex", "detect": ".codex", "path": ".codex/skills/megaplan/SKILL.md", "data": "codex_skill.md"},
666	    {"agent": "cursor", "detect": ".cursor", "path": ".cursor/rules/megaplan.mdc", "data": "cursor_rule.mdc"},
667	]
668	
669	
670	def _install_owned_file(path: Path, content: str, *, force: bool = False) -> dict[str, bool | str]:
671	    existed = path.exists()
672	    if existed and not force:
673	        if path.read_text(encoding="utf-8") == content:
674	            return {"path": str(path), "skipped": True, "existed": True}
675	    atomic_write_text(path, content)
676	    return {"path": str(path), "skipped": False, "existed": existed}
677	
678	
679	def handle_setup_global(force: bool = False, home: Path | None = None) -> StepResponse:
680	    if home is None:
681	        home = Path.home()
682	    installed: list[dict[str, Any]] = []
683	    detected_count = 0
684	    for target in _GLOBAL_TARGETS:
685	        agent_dir = home / target["detect"]
686	        if not agent_dir.is_dir():
687	            installed.append({"agent": target["agent"], "path": str(home / target["path"]), "skipped": True, "reason": "not installed"})
688	            continue
689	        detected_count += 1
690	        result = _install_owned_file(home / target["path"], bundled_global_file(target["data"]), force=force)
691	        result["agent"] = target["agent"]
692	        installed.append(result)
693	    if detected_count == 0:
694	        return {
695	            "success": False, "step": "setup", "mode": "global",
696	            "summary": "No supported agents detected. Create one of ~/.claude/, ~/.codex/, or ~/.cursor/ and re-run.",
697	            "installed": installed,
698	        }
699	    available = detect_available_agents()
700	    config_path = None
701	    routing = None
702	    if available:
703	        agents_config = {step: (default if default in available else available[0]) for step, default in DEFAULT_AGENT_ROUTING.items()}
704	        config = load_config(home)
705	        config["agents"] = agents_config
706	        config_path = save_config(config, home)
707	        routing = agents_config
708	    lines = []
709	    for rec in installed:
710	        if rec.get("reason") == "not installed":
711	            lines.append(f"  {rec['agent']}: skipped (not installed)")
712	        elif rec["skipped"]:
713	            lines.append(f"  {rec['agent']}: up to date")
714	        else:
715	            lines.append(f"  {rec['agent']}: {'overwrote' if rec['existed'] else 'created'} {rec['path']}")
716	    result_data: dict[str, Any] = {"success": True, "step": "setup", "mode": "global", "summary": "Global setup complete:\n" + "\n".join(lines), "installed": installed}
717	    if config_path is not None:
718	        result_data["config_path"] = str(config_path)
719	        result_data["routing"] = routing
720	    return result_data
721	
722	
723	def handle_setup(args: argparse.Namespace) -> StepResponse:
724	    local = args.local or args.target_dir
725	    if not local:
726	        return handle_setup_global(force=args.force)
727	    target_dir = Path(args.target_dir).resolve() if args.target_dir else Path.cwd()
728	    target = target_dir / "AGENTS.md"
729	    content = bundled_agents_md()
730	    if target.exists() and not args.force:
731	        existing = target.read_text(encoding="utf-8")
732	        if "megaplan" in existing.lower():
733	            return {"success": True, "step": "setup", "summary": f"AGENTS.md already contains megaplan instructions at {target}", "skipped": True}
734	        atomic_write_text(target, existing + "\n\n" + content)
735	        return {"success": True, "step": "setup", "summary": f"Appended megaplan instructions to existing {target}", "file": str(target)}
736	    atomic_write_text(target, content)
737	    return {"success": True, "step": "setup", "summary": f"Created {target}", "file": str(target)}
738	
739	
740	def handle_config(args: argparse.Namespace) -> StepResponse:
741	    action = args.config_action
742	    if action == "show":
743	        config = load_config()
744	        effective_routing = {step: config.get("agents", {}).get(step, default) for step, default in DEFAULT_AGENT_ROUTING.items()}
745	        effective_settings = {
746	            dot_key: get_effective(section, setting)
747	            for dot_key in sorted(DEFAULTS)
748	            for section, setting in [dot_key.split(".", 1)]
749	        }
750	        return {
751	            "success": True,
752	            "step": "config",
753	            "action": "show",
754	            "config_path": str(config_dir() / "config.json"),
755	            "routing": effective_routing,
756	            "effective_settings": effective_settings,
757	            "raw_config": config,
758	        }
759	    if action == "set":
760	        key, value = args.key, args.value
761	        parts = key.split(".", 1)
762	        config = load_config()
763	        valid_keys = [
764	            *(f"agents.{step}" for step in DEFAULT_AGENT_ROUTING),
765	            "orchestration.mode",
766	            *sorted(_SETTABLE_BOOL),
767	            *sorted(_SETTABLE_ENUM),
768	            *sorted(_SETTABLE_NUMERIC),
769	        ]
770	        if len(parts) != 2:
771	            raise CliError(
772	                "invalid_args",
773	                f"Unknown config key '{key}'. Valid keys: {', '.join(valid_keys)}",
774	            )
775	        section, setting = parts
776	        normalized_value = value.strip().lower()
777	        if section == "agents":
778	            if setting not in DEFAULT_AGENT_ROUTING:
779	                raise CliError("invalid_args", f"Unknown step '{setting}'. Valid steps: {', '.join(DEFAULT_AGENT_ROUTING)}")
780	            if value not in KNOWN_AGENTS:
781	                raise CliError("invalid_args", f"Unknown agent '{value}'. Valid agents: {', '.join(KNOWN_AGENTS)}")
782	            config.setdefault("agents", {})[setting] = value
783	        elif key == "orchestration.mode":
784	            if value not in {"inline", "subagent"}:
785	                raise CliError("invalid_args", "orchestration.mode must be 'inline' or 'subagent'")
786	            config.setdefault("orchestration", {})["mode"] = value
787	        elif key in _SETTABLE_BOOL:
788	            if normalized_value in {"true", "1", "yes", "on"}:
789	                parsed_value = True
790	            elif normalized_value in {"false", "0", "no", "off"}:
791	                parsed_value = False
792	            else:
793	                raise CliError(
794	                    "invalid_args",
795	                    f"{key} must be one of: true, false, 1, 0, yes, no, on, off",
796	                )
797	            config.setdefault(section, {})[setting] = parsed_value
798	        elif key in _SETTABLE_ENUM:
799	            allowed_values = _SETTABLE_ENUM[key]
800	            if value not in allowed_values:
801	                raise CliError(
802	                    "invalid_args",
803	                    f"{key} must be one of: {', '.join(allowed_values)}",
804	                )
805	            config.setdefault(section, {})[setting] = value
806	        elif key in _SETTABLE_NUMERIC:
807	            try:
808	                parsed_value = int(value)
809	            except ValueError as exc:
810	                raise CliError("invalid_args", f"{key} must be an integer, got '{value}'") from exc
811	            config.setdefault(section, {})[setting] = parsed_value
812	        else:
813	            raise CliError(
814	                "invalid_args",
815	                f"Unknown config key '{key}'. Valid keys: {', '.join(valid_keys)}",
816	            )
817	        save_config(config)
818	        return {"success": True, "step": "config", "action": "set", "key": key, "value": config[section][setting]}
819	    if action == "profiles":
820	        project_dir = Path.cwd()
821	        profiles_action = args.profiles_action
822	        if profiles_action == "list":
823	            profiles = [
824	                {
825	                    "source": source_label,
826	                    "name": profile_name,
827	                    "phases": phase_map,
828	                }
829	                for source_label, profile_name, phase_map in load_profile_sources(project_dir=project_dir)
830	            ]
831	            return {
832	                "success": True,
833	                "step": "config",
834	                "action": "profiles",
835	                "profiles_action": "list",
836	                "project_dir": str(project_dir),
837	                "profiles": profiles,
838	            }
839	        if profiles_action == "show":
840	            profiles = load_profiles(project_dir=project_dir)
841	            resolved = resolve_profile(args.name, profiles)
842	            return {
843	                "success": True,
844	                "step": "config",
845	                "action": "profiles",
846	                "profiles_action": "show",
847	                "project_dir": str(project_dir),
848	                "name": args.name,
849	                "profile": resolved,
850	            }
851	        raise CliError("invalid_args", f"Unknown profiles action: {profiles_action}")
852	    if action == "reset":
853	        path = config_dir() / "config.json"
854	        if path.exists():
855	            path.unlink()
856	        return {"success": True, "step": "config", "action": "reset", "summary": "Config file removed. Using defaults."}
857	    raise CliError("invalid_args", f"Unknown config action: {action}")
858	
859	
860	# ---------------------------------------------------------------------------
861	# Parser and dispatch
862	# ---------------------------------------------------------------------------
863	
864	def build_parser() -> argparse.ArgumentParser:
865	    parser = argparse.ArgumentParser(description="Megaplan orchestration CLI")
866	    subparsers = parser.add_subparsers(dest="command", required=True)
867	
868	    setup_parser = subparsers.add_parser("setup", help="Install megaplan into agent configs (global by default)")
869	    setup_parser.add_argument("--local", action="store_true", help="Install AGENTS.md into a project instead of global agent configs")
870	    setup_parser.add_argument("--target-dir", help="Directory to install into (default: cwd, implies --local)")
871	    setup_parser.add_argument("--force", action="store_true", help="Overwrite existing files")
872	
873	    init_parser = subparsers.add_parser("init")
874	    init_parser.add_argument("--project-dir", required=True)
875	    init_parser.add_argument("--name")
876	    init_parser.add_argument("--auto-approve", action="store_true", default=None)
877	    init_parser.add_argument("--robustness", choices=list(ROBUSTNESS_LEVELS), default=None)
878	    init_parser.add_argument("--mode", choices=["code", "doc", "metaplan", "joke"], default=None,
879	                             help="Deliverable type: 'code' (source changes), 'doc' / 'metaplan' "
880	                                  "(design/spec artifact — 'metaplan' is an alias for 'doc'), or "
881	                                  "'joke' (film scene script; requires --output). "
882	                                  "Defaults to 'code' unless the idea strongly suggests a design document, "
883	                                  "in which case --mode must be passed explicitly.")
884	    init_parser.add_argument("--output", default=None,
885	                             help="Relative path where the doc or joke artifact will be written. "
886	                                  "Required with --mode doc or --mode joke; rejected with --mode code.")
887	    init_parser.add_argument(
888	        "--primary-criterion",
889	        default=None,
890	        help="Declare the joke-mode primary criterion (for example: 'weirdest coherent'). "
891	             "Valid only with --mode joke.",
892	    )
893	    init_parser.add_argument("--from-doc", default=None,
894	                             help="Relative path to a prior doc-mode artifact whose ## Settled "
895	                                  "Decisions section should be imported. Valid with --mode "
896	                                  "code, --mode doc, or --mode joke.")
897	    init_parser.add_argument(
898	        "--idea-file",
899	        default=None,
900	        help="Read the idea text from a UTF-8 file instead of the positional CLI argument.",
901	    )
902	    init_parser.add_argument(
903	        "--auto-start",
904	        action="store_true",
905	        help="Immediately run the in-process auto driver after initializing the plan.",
906	    )
907	    init_parser.add_argument("--hermes", nargs="?", const="", default=None,
908	                             help="Use Hermes agent for all phases. Optional: specify default model")
909	    init_parser.add_argument("--phase-model", action="append", default=[],
910	                             help="Per-phase model override: --phase-model critique=hermes:openai/gpt-5")
911	    init_parser.add_argument("--profile", default=None,
912	                             help="Named preset from profiles.toml; see 'megaplan config profiles list'.")
913	    init_parser.add_argument("idea", nargs="?")
914	
915	    list_parser = subparsers.add_parser("list")
916	    list_parser.add_argument("--all", action="store_true",
917	                             help="Search all .megaplan directories system-wide (~)")
918	    list_parser.add_argument("--no-tree", action="store_true",
919	                             help="Only show plans from the current directory (default includes parent + child)")
920	    list_parser.add_argument("--include-done", action="store_true",
921	                             help="Include terminal plans (done/aborted); excluded by default")
922	    list_parser.add_argument("--status", dest="filter_status",
923	                             help="Filter by state (e.g. 'done', 'finalized', 'executed', or comma-separated 'planned,critiqued')")
924	    list_parser.add_argument("--summary", action="store_true",
925	                             help="Show count breakdown by state")
926	
927	    for name in ["status", "audit", "progress", "watch"]:
928	        step_parser = subparsers.add_parser(name)
929	        step_parser.add_argument("--plan")
930	        if name == "status":
931	            step_parser.add_argument("--pending-human", action="store_true",
932	                                     help="List plans awaiting human verification")
933	
934	    for name in ["plan", "prep", "critique", "revise", "gate", "finalize", "execute", "review"]:
935	        step_parser = subparsers.add_parser(name)
936	        step_parser.add_argument("--plan")
937	        step_parser.add_argument("--agent", choices=["claude", "codex", "hermes"])
938	        step_parser.add_argument("--hermes", nargs="?", const="", default=None,
939	                                 help="Use Hermes agent for all phases. Optional: specify default model (e.g. --hermes anthropic/claude-sonnet-4.6)")
940	        step_parser.add_argument("--phase-model", action="append", default=[],
941	                                 help="Per-phase model override: --phase-model critique=hermes:openai/gpt-5")
942	        step_parser.add_argument("--profile", default=None,
943	                                 help="Named preset from profiles.toml; see 'megaplan config profiles list'.")
944	        step_parser.add_argument("--fresh", action="store_true")
945	        step_parser.add_argument("--persist", action="store_true")
946	        step_parser.add_argument("--ephemeral", action="store_true")
947	        step_parser.add_argument("--work-dir", default=None,
948	                                 help="Override the source-code working directory passed to subprocess workers "
949	                                      "(--add-dir / -C). Defaults to the current working directory. Use this to "
950	                                      "force a specific path (e.g. a git worktree) regardless of where the plan was created.")
951	        if name == "execute":
952	            step_parser.add_argument("--confirm-destructive", action="store_true")
953	            step_parser.add_argument("--user-approved", action="store_true")
954	            step_parser.add_argument("--batch", type=int, default=None, help="Execute a specific global batch number (1-indexed)")
955	        if name == "review":
956	            step_parser.add_argument("--confirm-self-review", action="store_true")
957	
958	    config_parser = subparsers.add_parser("config", help="View or edit megaplan configuration")
959	    config_sub = config_parser.add_subparsers(dest="config_action", required=True)
960	    config_sub.add_parser("show")
961	    set_parser = config_sub.add_parser("set")
962	    set_parser.add_argument("key")
963	    set_parser.add_argument("value")
964	    config_sub.add_parser("reset")
965	    profiles_parser = config_sub.add_parser("profiles", help="Inspect model profiles from built-in, user, and project layers")
966	    profiles_sub = profiles_parser.add_subparsers(dest="profiles_action", required=True)
967	    profiles_sub.add_parser(
968	        "list",
969	        help="List profiles from all layers",
970	        description="List profiles from all layers. Project-layer profiles are only visible when run from that project directory.",
971	    )
972	    profiles_show_parser = profiles_sub.add_parser("show", help="Show the fully resolved phase map for one profile")
973	    profiles_show_parser.add_argument("name")
974	
975	    step_parser = subparsers.add_parser("step", help="Edit plan step sections without hand-editing markdown")
976	    step_subparsers = step_parser.add_subparsers(dest="step_action", required=True)
977	
978	    step_add_parser = step_subparsers.add_parser("add", help="Insert a new step after an existing step")
979	    step_add_parser.add_argument("--plan")
980	    step_add_parser.add_argument("--after")
981	    step_add_parser.add_argument("description")
982	
983	    step_remove_parser = step_subparsers.add_parser("remove", help="Remove a step and renumber the plan")
984	    step_remove_parser.add_argument("--plan")
985	    step_remove_parser.add_argument("step_id")
986	
987	    step_move_parser = step_subparsers.add_parser("move", help="Move a step after another step and renumber")
988	    step_move_parser.add_argument("--plan")
989	    step_move_parser.add_argument("step_id")
990	    step_move_parser.add_argument("--after", required=True)
991	
992	    override_parser = subparsers.add_parser("override")
993	    override_parser.add_argument("override_action", choices=["abort", "force-proceed", "add-note", "replan", "set-robustness"])
994	    override_parser.add_argument("--plan")
995	    override_parser.add_argument("--reason", default="")
996	    override_parser.add_argument("--note")
997	    override_parser.add_argument("--robustness", choices=list(ROBUSTNESS_LEVELS), default=None)
998	
999	    verify_human_parser = subparsers.add_parser("verify-human", help="Record human verification for a criterion")
1000	    verify_human_parser.add_argument("--plan")
1001	    verify_human_parser.add_argument("--criterion", required=True, help="Criterion name or index")
1002	    vh_group = verify_human_parser.add_mutually_exclusive_group(required=True)
1003	    vh_group.add_argument("--pass", dest="pass_flag", action="store_true")
1004	    vh_group.add_argument("--fail", dest="fail_flag", action="store_true")
1005	    verify_human_parser.add_argument("--evidence", required=True, help="Evidence supporting the verdict")
1006	
1007	    audit_verifiability_parser = subparsers.add_parser("audit-verifiability", help="Audit criteria verifiability")
1008	    audit_verifiability_parser.add_argument("--plan")
1009	
1010	    debt_parser = subparsers.add_parser("debt", help="Inspect or manage persistent tech debt entries")
1011	    debt_subparsers = debt_parser.add_subparsers(dest="debt_action", required=True)
1012	
1013	    debt_list_parser = debt_subparsers.add_parser("list", help="List debt entries")
1014	    debt_list_parser.add_argument("--all", action="store_true", help="Include resolved entries")
1015	
1016	    debt_add_parser = debt_subparsers.add_parser("add", help="Add or increment a debt entry")
1017	    debt_add_parser.add_argument("--subsystem", required=True)
1018	    debt_add_parser.add_argument("--concern", required=True)
1019	    debt_add_parser.add_argument("--flag-ids", default="")
1020	    debt_add_parser.add_argument("--plan")
1021	
1022	    debt_resolve_parser = debt_subparsers.add_parser("resolve", help="Resolve a debt entry")
1023	    debt_resolve_parser.add_argument("debt_id")
1024	    debt_resolve_parser.add_argument("--plan")
1025	
1026	    loop_init_parser = subparsers.add_parser("loop-init", help="Initialize a MegaLoop workflow")
1027	    loop_init_parser.add_argument("--project-dir", required=True)
1028	    loop_init_parser.add_argument("--command", required=True)
1029	    loop_init_parser.add_argument("--goal", dest="goal_option")
1030	    loop_init_parser.add_argument("--name")
1031	    loop_init_parser.add_argument("--iterations", type=int, default=3)
1032	    loop_init_parser.add_argument("--time-budget", type=int, default=300)
1033	    loop_init_parser.add_argument("--observe-interval", type=int)
1034	    loop_init_parser.add_argument("--observe-break-patterns")
1035	    loop_init_parser.add_argument("--agent", choices=["claude", "codex", "hermes"])
1036	    loop_init_parser.add_argument("--hermes", nargs="?", const="", default=None,
1037	                                  help="Use Hermes agent for loop phases. Optional: specify default model")
1038	    loop_init_parser.add_argument("--phase-model", action="append", default=[],
1039	                                  help="Per-phase model override: --phase-model loop_execute=hermes:openai/gpt-5")
1040	    loop_init_parser.add_argument("--profile", default=None,
1041	                                  help="Named preset from profiles.toml; see 'megaplan config profiles list'.")
1042	    loop_init_parser.add_argument("--fresh", action="store_true")
1043	    loop_init_parser.add_argument("--persist", action="store_true")
1044	    loop_init_parser.add_argument("--ephemeral", action="store_true")
1045	    loop_init_parser.add_argument("--work-dir", default=None,
1046	                                  help="Override the source-code working directory for subprocess workers (default: CWD)")
1047	    loop_init_parser.add_argument("goal", nargs="?")
1048	
1049	    loop_run_parser = subparsers.add_parser("loop-run", help="Run an existing MegaLoop workflow")
1050	    loop_run_parser.add_argument("name")
1051	    loop_run_parser.add_argument("--project-dir")
1052	    loop_run_parser.add_argument("--iterations", type=int)
1053	    loop_run_parser.add_argument("--time-budget", type=int)
1054	    loop_run_parser.add_argument("--agent", choices=["claude", "codex", "hermes"])
1055	    loop_run_parser.add_argument("--hermes", nargs="?", const="", default=None,
1056	                                 help="Use Hermes agent for loop phases. Optional: specify default model")
1057	    loop_run_parser.add_argument("--phase-model", action="append", default=[],
1058	                                 help="Per-phase model override: --phase-model loop_execute=hermes:openai/gpt-5")
1059	    loop_run_parser.add_argument("--profile", default=None,
1060	                                 help="Named preset from profiles.toml; see 'megaplan config profiles list'.")
1061	    loop_run_parser.add_argument("--fresh", action="store_true")
1062	    loop_run_parser.add_argument("--persist", action="store_true")
1063	    loop_run_parser.add_argument("--ephemeral", action="store_true")
1064	    loop_run_parser.add_argument("--work-dir", default=None,
1065	                                 help="Override the source-code working directory for subprocess workers (default: CWD)")
1066	
1067	    loop_status_parser = subparsers.add_parser("loop-status", help="Show MegaLoop state")
1068	    loop_status_parser.add_argument("name")
1069	    loop_status_parser.add_argument("--project-dir")
1070	
1071	    loop_pause_parser = subparsers.add_parser("loop-pause", help="Pause a MegaLoop workflow")
1072	    loop_pause_parser.add_argument("name")
1073	    loop_pause_parser.add_argument("--project-dir")
1074	    loop_pause_parser.add_argument("--reason", default="")
1075	
1076	    from megaplan.auto import build_auto_parser
1077	    build_auto_parser(subparsers)
1078	
1079	    from megaplan.chain import build_chain_parser
1080	    build_chain_parser(subparsers)
1081	
1082	    cloud_parser = subparsers.add_parser(
1083	        "cloud",
1084	        add_help=False,
1085	        help="Manage provider-backed megaplan cloud runners",
1086	    )
1087	    cloud_parser.add_argument("cloud_args", nargs=argparse.REMAINDER)
1088	
1089	    from megaplan.prompts.tiebreaker_orchestrator import build_tiebreaker_parser
1090	    build_tiebreaker_parser(subparsers)
1091	
1092	    # tiebreaker-run is a top-level command because auto.py:_phase_command
1093	    # translates next_step directly to CLI args.
1094	    tb_run_parser = subparsers.add_parser(
1095	        "tiebreaker-run",
1096	        help="Run tiebreaker researcher+challenger (used by auto driver)",
1097	    )
1098	    tb_run_parser.add_argument("--plan", required=True, help="Plan name")
1099	    tb_run_parser.add_argument("--agent", choices=["claude", "codex", "hermes"], default=None)
1100	    tb_run_parser.add_argument("--hermes", nargs="?", const="", default=None)
1101	    tb_run_parser.add_argument("--phase-model", action="append", default=[])
1102	    tb_run_parser.add_argument("--profile", default=None,
1103	                               help="Named preset from profiles.toml; see 'megaplan config profiles list'.")
1104	    tb_run_parser.add_argument("--fresh", action="store_true")
1105	    tb_run_parser.add_argument("--persist", action="store_true")
1106	    tb_run_parser.add_argument("--ephemeral", action="store_true")
1107	
1108	    return parser
1109	
1110	
1111	COMMAND_HANDLERS: dict[str, Callable[..., StepResponse]] = {
1112	    "init": handle_init,
1113	    "plan": handle_plan,
1114	    "prep": handle_prep,
1115	    "critique": handle_critique,
1116	    "revise": handle_revise,
1117	    "gate": handle_gate,
1118	    "finalize": handle_finalize,
1119	    "execute": handle_execute,
1120	    "review": handle_review,
1121	    "status": handle_status,
1122	    "audit": handle_audit,
1123	    "progress": handle_progress,
1124	    "watch": handle_watch,
1125	    "list": handle_list,
1126	    "loop-init": handle_loop_init,
1127	    "loop-run": handle_loop_run,
1128	    "loop-status": handle_loop_status,
1129	    "loop-pause": handle_loop_pause,
1130	    "debt": handle_debt,
1131	    "step": handle_step,
1132	    "override": handle_override,
1133	    "verify-human": handle_verify_human,
1134	    "audit-verifiability": handle_audit_verifiability,
1135	    "tiebreaker-run": handle_tiebreaker_run,
1136	}
1137	
1138	
1139	def cli_entry() -> None:
1140	    sys.exit(main())
1141	
1142	
1143	def _find_megaplan_root(start: Path) -> Path:
1144	    """Walk up from *start* to find the git-root directory containing ``.megaplan/``.
1145	
1146	    Strategy: find the git root first (like ``git rev-parse --show-toplevel``),
1147	    then check if it has a ``.megaplan/`` directory.  This avoids ambiguity when
1148	    nested subdirectories also have their own ``.megaplan/``.  Falls back to the
1149	    nearest ancestor with ``.megaplan/`` if not in a git repo, and finally to
1150	    *start* if nothing is found.
1151	    """
1152	    resolved = start.resolve()
1153	
1154	    # Try git root first — the canonical project root.
1155	    git_root = _find_git_root(resolved)
1156	    if git_root and (git_root / ".megaplan").is_dir():
1157	        return git_root
1158	
1159	    # Fallback: walk up to find nearest .megaplan
1160	    current = resolved
1161	    while True:
1162	        if (current / ".megaplan").is_dir():
1163	            return current
1164	        parent = current.parent
1165	        if parent == current:
1166	            return start
1167	        current = parent
1168	
1169	
1170	def _find_git_root(start: Path) -> Path | None:
1171	    """Walk up to find the directory containing ``.git``."""
1172	    current = start
1173	    while True:
1174	        if (current / ".git").exists():
1175	            return current
1176	        parent = current.parent
1177	        if parent == current:
1178	            return None
1179	        current = parent
1180	
1181	
1182	def _auto_sync_installed_skills() -> None:
1183	    try:
1184	        for target in _GLOBAL_TARGETS:
1185	            agent_dir = Path.home() / target["detect"]
1186	            if not agent_dir.is_dir():
1187	                continue
1188	            _install_owned_file(Path.home() / target["path"], bundled_global_file(target["data"]), force=False)
1189	    except Exception:
1190	        pass
1191	
1192	
1193	def main(argv: list[str] | None = None) -> int:
1194	    if argv is None:
1195	        argv = sys.argv[1:]
1196	    if argv and argv[0] == "cloud":
1197	        from megaplan.cloud.cli import _register_cloud_subcommands, run_cloud_cli
1198	
1199	        cloud_parser = argparse.ArgumentParser(prog="megaplan cloud")
1200	        _register_cloud_subcommands(cloud_parser)
1201	        cloud_args = cloud_parser.parse_args(argv[1:])
1202	        root = _find_megaplan_root(Path.cwd())
1203	        ensure_runtime_layout(root)
1204	        try:
1205	            return run_cloud_cli(root, cloud_args)
1206	        except CliError as error:
1207	            return error_response(error, root=root)
1208	
1209	    parser = build_parser()
1210	    args, remaining = parser.parse_known_args(argv)
1211	    if args.command != "setup":
1212	        _auto_sync_installed_skills()
1213	    try:
1214	        if args.command == "setup":
1215	            return render_response(handle_setup(args))
1216	        if args.command == "config":
1217	            return render_response(handle_config(args))
1218	    except CliError as error:
1219	        return error_response(error)
1220	
1221	    # Capture an explicit --work-dir override for subprocess workers
1222	    # (--add-dir / -C). When the flag is NOT passed, leave the override unset
1223	    # so :func:`resolve_work_dir` can default to the plan's stored project_dir
1224	    # (persisted at ``megaplan init``). Defaulting to CWD here silently
1225	    # sandboxes codex to whatever subdirectory the shell happened to be in,
1226	    # which breaks cross-subrepo writes — see resolve_work_dir for the
1227	    # precedence rules.
1228	    from megaplan.workers import set_work_dir_override
1229	    work_dir_override = getattr(args, "work_dir", None)
1230	    set_work_dir_override(Path(work_dir_override) if work_dir_override else None)
1231	
1232	    root = _find_megaplan_root(Path.cwd())
1233	    ensure_runtime_layout(root)
1234	
1235	    if args.command == "auto":
1236	        from megaplan.auto import run_auto
1237	        try:
1238	            return run_auto(root, args)
1239	        except CliError as error:
1240	            return error_response(error, root=root)
1241	
1242	    if args.command == "chain":
1243	        from megaplan.chain import run_chain_cli
1244	        try:
1245	            return run_chain_cli(root, args)
1246	        except CliError as error:
1247	            return error_response(error, root=root)
1248	
1249	    if args.command == "tiebreaker":
1250	        from megaplan.prompts.tiebreaker_orchestrator import run_tiebreaker_cli
1251	        try:
1252	            return run_tiebreaker_cli(root, args)
1253	        except CliError as error:
1254	            return error_response(error, root=root)
1255	
1256	    try:
1257	        handler = COMMAND_HANDLERS.get(args.command)
1258	        if handler is None:
1259	            raise CliError("invalid_command", f"Unknown command {args.command!r}")
1260	        if args.command == "override" and remaining:
1261	            if not args.note:
1262	                args.note = " ".join(remaining)
1263	            remaining = []
1264	        if remaining:
1265	            parser.error(f"unrecognized arguments: {' '.join(remaining)}")
1266	        if args.command == "override" and args.override_action == "add-note" and not args.note:
1267	            raise CliError("invalid_args", "override add-note requires a note")
1268	        if args.command == "override" and args.override_action == "set-robustness" and not args.robustness:
1269	            raise CliError("invalid_args", f"override set-robustness requires --robustness {'|'.join(ROBUSTNESS_LEVELS)}")
1270	        return render_response(handler(root, args))
1271	    except CliError as error:
1272	        return error_response(error, root=root)
1273	
1274	
1275	if __name__ == "__main__":
1276	    sys.exit(main())
1277	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/megaplan/megaplan/*.py"
}
```

> TOOL

tool_result Glob
```
megaplan/__main__.py
megaplan/audits/quality_gates.py
megaplan/loop/__init__.py
megaplan/loop/git.py
megaplan/loop/types.py
megaplan/loop/prompts.py
megaplan/loop/handlers.py
megaplan/execute/merge.py
megaplan/_core/registries.py
megaplan/prompts/_shared.py
megaplan/step_edit.py
megaplan/_core/__init__.py
megaplan/__init__.py
megaplan/prompts/execute.py
megaplan/review/mechanical.py
megaplan/prompts/prep_doc.py
megaplan/prompts/review_doc.py
megaplan/audits/capabilities.py
megaplan/_core/phase_runtime.py
megaplan/_core/workflow.py
megaplan/audits/audit_engine.py
megaplan/audits/iteration.py
megaplan/prompts/tiebreaker_challenger.py
megaplan/prompts/tiebreaker_researcher.py
megaplan/prompts/tiebreaker_synthesis.py
megaplan/cloud/__init__.py
megaplan/cloud/providers/__init__.py
megaplan/cloud/templates/__init__.py
megaplan/cloud/wrappers/__init__.py
megaplan/cloud/templates/healthserver.py
megaplan/handlers/override.py
megaplan/doc_assembly.py
megaplan/chain.py
megaplan/auto.py
megaplan/cloud/spec.py
megaplan/cloud/template.py
megaplan/cloud/providers/base.py
megaplan/cloud/redact.py
megaplan/cloud/providers/railway.py
megaplan/cloud/providers/local.py
megaplan/cloud/providers/ssh.py
megaplan/cloud/cli.py
megaplan/execute/__init__.py
megaplan/execute/quality.py
megaplan/audits/verifiability.py
megaplan/prompts/gate.py
megaplan/handlers/verifiability.py
megaplan/review/checks.py
megaplan/review/__init__.py
megaplan/handlers/__init__.py
megaplan/prompts/execute_doc.py
megaplan/handlers/finalize.py
megaplan/evaluation.py
megaplan/execute/timeout.py
megaplan/prompts/finalize.py
megaplan/prompts/review.py
megaplan/prompts/critique.py
megaplan/audits/robustness.py
megaplan/prompts/critique_joke.py
megaplan/prompts/revise_joke.py
megaplan/flags.py
megaplan/prompts/execute_joke.py
megaplan/prompts/review_joke.py
megaplan/prompts/planning.py
megaplan/prompts/__init__.py
megaplan/schemas.py
megaplan/prompts/prep_joke.py
megaplan/handlers/plan.py
megaplan/agent/acp_adapter/__init__.py
megaplan/agent/acp_adapter/__main__.py
megaplan/agent/acp_adapter/auth.py
megaplan/agent/acp_adapter/entry.py
megaplan/agent/acp_adapter/events.py
megaplan/agent/acp_adapter/permissions.py
megaplan/agent/acp_adapter/server.py
megaplan/agent/acp_adapter/session.py
megaplan/agent/acp_adapter/tools.py
megaplan/agent/agent/__init__.py
megaplan/agent/agent/anthropic_adapter.py
megaplan/agent/agent/auxiliary_client.py
megaplan/agent/agent/context_compressor.py
megaplan/agent/agent/context_references.py
megaplan/agent/agent/copilot_acp_client.py
megaplan/agent/agent/display.py
megaplan/agent/agent/insights.py
megaplan/agent/agent/model_metadata.py
megaplan/agent/agent/models_dev.py
megaplan/agent/agent/prompt_builder.py
megaplan/agent/agent/prompt_caching.py
megaplan/agent/agent/redact.py
megaplan/agent/agent/skill_commands.py
megaplan/agent/agent/smart_model_routing.py
megaplan/agent/agent/title_generator.py
megaplan/agent/agent/trajectory.py
megaplan/agent/agent/usage_pricing.py
megaplan/agent/cron/__init__.py
megaplan/agent/cron/jobs.py
megaplan/agent/cron/scheduler.py
megaplan/agent/environments/__init__.py
megaplan/agent/environments/agent_loop.py
(Results are truncated. Consider using a more specific path or pattern.)
```

> AGENT

Now let me search for auto.py, state.py, and profiles code:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/auto.py",
  "limit": 150
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
27	from megaplan.types import (
28	    AUTOMATION_TERMINAL_STATES,
29	    STATE_AWAITING_HUMAN,
30	    STATE_TIEBREAKER_PENDING,
31	    STATE_TIEBREAKER_READY,
32	    TERMINAL_STATES,
33	)
34	
35	
36	DEFAULT_STALL_THRESHOLD = 5
37	DEFAULT_MAX_ITERATIONS = 200
38	DEFAULT_POLL_SLEEP_SECONDS = 1.0
39	DEFAULT_PHASE_TIMEOUT_SECONDS = 3600
40	DEFAULT_STATUS_TIMEOUT_SECONDS = 60
41	# Cap on review→rework cycles before the driver bails. This mirrors the
42	# `execution.max_review_rework_cycles` config the review handler enforces
43	# internally (default 3); the auto-driver applies its own cap so that an
44	# unexpected-config or mis-routed rework loop cannot spin indefinitely.
45	DEFAULT_MAX_REVIEW_REWORK_CYCLES = 3
46	ESCALATE_ACTIONS = ("force-proceed", "abort", "fail")
47	PHASE_TIMEOUT_EXIT_CODE = 124  # conventional; matches GNU `timeout`
48	
49	
50	@dataclass
51	class DriverOutcome:
52	    """Terminal outcome reported when the loop exits."""
53	
54	    status: str  # "done" | "stalled" | "escalated" | "failed" | "aborted" | "cap" | "blocked"
55	    plan: str
56	    final_state: str
57	    iterations: int
58	    reason: str = ""
59	    last_phase: str | None = None
60	    events: list[dict[str, Any]] = field(default_factory=list)
61	
62	    def to_json(self) -> str:
63	        return json.dumps(
64	            {
65	                "status": self.status,
66	                "plan": self.plan,
67	                "final_state": self.final_state,
68	                "iterations": self.iterations,
69	                "reason": self.reason,
70	                "last_phase": self.last_phase,
71	                "events": self.events,
72	            },
73	            indent=2,
74	        )
75	
76	
77	def _run_megaplan(
78	    args: list[str],
79	    *,
80	    cwd: Path | None = None,
81	    timeout: float | None = None,
82	) -> tuple[int, str, str]:
83	    """Run a megaplan sub-command in its own process.
84	
85	    We shell out rather than importing the handlers directly so each phase gets
86	    a fresh argparse/handler lifecycle. This matches how external orchestrators
87	    drive the CLI and avoids subtle state leakage between phases.
88	
89	    ``timeout`` is seconds to wait before killing the subprocess. On timeout we
90	    return exit code ``PHASE_TIMEOUT_EXIT_CODE`` and append a marker to stderr
91	    so the driver can surface it as a phase failure without crashing the loop.
92	    The subprocess is killed; any grandchildren it spawned (e.g. codex) may
93	    need a moment to settle but will exit when their parent's pipes close.
94	    """
95	    try:
96	        proc = subprocess.run(
97	            [sys.executable, "-m", "megaplan", *args],
98	            cwd=str(cwd) if cwd else None,
99	            capture_output=True,
100	            text=True,
101	            check=False,
102	            timeout=timeout,
103	        )
104	        return proc.returncode, proc.stdout, proc.stderr
105	    except subprocess.TimeoutExpired as expired:
106	        stdout = expired.stdout if isinstance(expired.stdout, str) else ""
107	        stderr = expired.stderr if isinstance(expired.stderr, str) else ""
108	        marker = f"\n[megaplan auto] subprocess timed out after {timeout}s"
109	        return PHASE_TIMEOUT_EXIT_CODE, stdout, (stderr + marker).strip()
110	
111	
112	def _status(
113	    plan: str,
114	    cwd: Path | None = None,
115	    *,
116	    timeout: float = DEFAULT_STATUS_TIMEOUT_SECONDS,
117	) -> dict[str, Any]:
118	    code, out, err = _run_megaplan(["status", "--plan", plan], cwd=cwd, timeout=timeout)
119	    if code != 0:
120	        raise RuntimeError(f"megaplan status failed (exit {code}): {err.strip() or out.strip()}")
121	    return json.loads(out)
122	
123	
124	def _has_valid_next(status: dict[str, Any], action: str) -> bool:
125	    return action in (status.get("valid_next") or [])
126	
127	
128	def _phase_command(next_step: str) -> list[str]:
129	    """Translate a `next_step` from status into the CLI args that run it.
130	
131	    Most phases are one-to-one: next_step == command. Execute adds the
132	    destructive + user-approved flags because auto-mode implies both.
133	    """
134	    if next_step == "execute":
135	        return ["execute", "--confirm-destructive", "--user-approved"]
136	    return [next_step]
137	
138	
139	def _resolve_plan_dir(plan: str, cwd: Path | None) -> Path | None:
140	    """Best-effort resolution of ``.megaplan/plans/<plan>`` near ``cwd``.
141	
142	    Walks up parents of ``cwd`` looking for a ``.megaplan/plans/<plan>``
143	    directory, matching how ``megaplan status`` resolves plans. Returns
144	    ``None`` if the plan dir can't be located — callers should treat that
145	    as "no review marker available" and fall back to the plain stall-count.
146	    """
147	    base = (cwd or Path.cwd()).resolve()
148	    for candidate in (base, *base.parents):
149	        plan_dir = candidate / ".megaplan" / "plans" / plan
150	        if (plan_dir / "state.json").exists():

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py",
  "limit": 100
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

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/megaplan/megaplan/profiles*"
}
```

> TOOL

tool_result Glob
```
No files found
```

> AGENT

Let me search for profiles:

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan -type f -name \"*profile*\" | grep -v \".megaplan\" | head -20"
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
  "command": "find /Users/user_c042661f/Documents/megaplan/megaplan -type f \\( -name \"*.py\" -o -name \"*.toml\" \\) | grep -i profile"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/profiles/standard.toml
/Users/user_c042661f/Documents/megaplan/megaplan/profiles/__init__.py
/Users/user_c042661f/Documents/megaplan/megaplan/profiles/all-open.toml
```

> AGENT

Now let me search for key terms from the brief:

> TOOL

tool_use Grep
```json
{
  "pattern": "receipt|step_receipt",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 6 files
megaplan/agent/tests/gateway/test_slack.py
megaplan/agent/skills/productivity/powerpoint/LICENSE.txt
megaplan/agent/optional-skills/blockchain/base/scripts/base_client.py
megaplan/agent/gateway/platforms/webhook.py
megaplan/agent/gateway/platforms/slack.py
megaplan/agent/gateway/platforms/signal.py
```

> TOOL

tool_use Grep
```json
{
  "pattern": "scope_drift|scope drift",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 4 files
megaplan/agent/auto_improve/iterations/001/consolidated/tasks/sphinx-doc__sphinx-8035/traces/review_v2.json
megaplan/agent/auto_improve/iterations/001/consolidated/tasks/sphinx-doc__sphinx-8035/traces/gate_v2.json
megaplan/agent/auto_improve/iterations/001/consolidated/tasks/sphinx-doc__sphinx-8035/traces/finalize_v2.json
megaplan/agent/auto_improve/iterations/001/consolidated/tasks/sphinx-doc__sphinx-8035/traces/execute_v2.json
```

> TOOL

tool_use Grep
```json
{
  "pattern": "subprocess\\.Popen|create_subprocess_exec",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 36 files
megaplan/loop/engine.py
megaplan/agent/evals/run_evals.py
megaplan/agent/evals/parallel.py
megaplan/agent/auto_improve/scale.py
megaplan/agent/auto_improve/iterations/012/consolidated/tasks/django__django-16032/traces/prep_v1.json
megaplan/agent/auto_improve/iterations/007/consolidated/tasks/django__django-10973/traces/prep_v1.json
megaplan/agent/auto_improve/cron.py
megaplan/agent/auto_improve/add_workers.py
megaplan/agent/tools/voice_mode.py
megaplan/agent/tools/terminal_tool.py
megaplan/agent/tools/rl_training_tool.py
megaplan/agent/tools/process_registry.py
megaplan/agent/tools/environments/ssh.py
megaplan/agent/tools/environments/singularity.py
megaplan/agent/tools/environments/persistent_shell.py
megaplan/agent/tools/environments/local.py
megaplan/agent/tools/environments/docker.py
megaplan/agent/tools/code_execution_tool.py
megaplan/agent/tools/browser_tool.py
megaplan/agent/tests/tools/test_voice_mode.py
megaplan/agent/tests/tools/test_ssh_environment.py
megaplan/agent/tests/tools/test_process_registry.py
megaplan/agent/tests/tools/test_local_env_blocklist.py
megaplan/agent/tests/tools/test_browser_homebrew_paths.py
megaplan/agent/tests/test_parallel_integration.py
megaplan/agent/tests/gateway/test_whatsapp_connect.py
megaplan/agent/tests/gateway/test_update_command.py
megaplan/agent/skills/creative/ascii-video/references/troubleshooting.md
megaplan/agent/skills/creative/ascii-video/references/scenes.md
megaplan/agent/skills/creative/ascii-video/references/optimization.md
megaplan/agent/skills/creative/ascii-video/references/inputs.md
megaplan/agent/skills/creative/ascii-video/references/architecture.md
megaplan/agent/gateway/run.py
megaplan/agent/gateway/platforms/whatsapp.py
megaplan/agent/agent/copilot_acp_client.py
megaplan/cloud/providers/base.py
```

> TOOL

tool_use Grep
```json
{
  "pattern": "worktree|git worktree",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 28 files
megaplan/workers.py
megaplan/cli.py
megaplan/agent/website/docs/user-guide/git-worktrees.md
megaplan/agent/website/docs/user-guide/configuration.md
megaplan/agent/website/docs/user-guide/cli.md
megaplan/agent/website/docs/user-guide/checkpoints-and-rollback.md
megaplan/agent/website/docs/reference/cli-commands.md
megaplan/agent/evals/benchmarks/swe_bench.py
megaplan/agent/cli.py
megaplan/agent/cli-config.yaml.example
megaplan/agent/auto_improve/iterations/012/consolidated/tasks/sphinx-doc__sphinx-9461/traces/critique_v1.json
megaplan/agent/RELEASE_v0.3.0.md
megaplan/agent/RELEASE_v0.2.0.md
megaplan/agent/tools/terminal_tool.py
megaplan/agent/tests/test_worktree_security.py
megaplan/agent/tests/test_worktree.py
megaplan/agent/tests/test_minisweagent_path.py
megaplan/agent/tests/hermes_cli/test_setup_noninteractive.py
megaplan/agent/tests/hermes_cli/test_coalesce_session_args.py
megaplan/agent/tests/hermes_cli/test_chat_skills_flag.py
megaplan/agent/skills/dogfood/hermes-agent-setup/SKILL.md
megaplan/agent/skills/autonomous-ai-agents/opencode/SKILL.md
megaplan/agent/skills/autonomous-ai-agents/codex/SKILL.md
megaplan/agent/skills/autonomous-ai-agents/claude-code/SKILL.md
megaplan/agent/minisweagent_path.py
megaplan/agent/mini_swe_runner.py
megaplan/agent/hermes_cli/main.py
megaplan/agent/.gitignore
```

> AGENT

Let me check for rglob and circular recursion references:

> TOOL

tool_use Grep
```json
{
  "pattern": "rglob.*megaplan|\\.megaplan.*rglob",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan",
  "type": "py",
  "output_mode": "content",
  "head_limit": 30
}
```

> TOOL

tool_result Grep
```
megaplan/cli.py:410:        for megaplan_dir in sorted(home.rglob(".megaplan")):
megaplan/cli.py:426:        for megaplan_dir in sorted(root.rglob(".megaplan")):
megaplan/_core/state.py:70:        for megaplan_dir in sorted(root.resolve().rglob(".megaplan")):
megaplan/agent/evals/benchmarks/swe_bench.py:58:    for finalize_path in workspace_path.rglob(".megaplan/plans/*/finalize.json"):
```

> AGENT

Now let me check profiles and pyproject.toml:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/profiles/__init__.py"
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	import argparse
4	import tomllib
5	from importlib.resources import files
6	from pathlib import Path
7	from typing import Any
8	
9	from .._core.io import config_dir
10	from ..types import CliError, DEFAULT_AGENT_ROUTING, KNOWN_AGENTS, parse_agent_spec
11	
12	VALID_PHASE_KEYS = frozenset(DEFAULT_AGENT_ROUTING.keys())
13	
14	
15	def _known_profiles_text(profiles: dict[str, dict[str, str]]) -> str:
16	    names = sorted(profiles)
17	    return ", ".join(names) if names else "(none)"
18	
19	
20	def _raise_invalid_profile(path: Any, profile_name: str, key: str, message: str) -> None:
21	    raise CliError(
22	        "invalid_profile",
23	        f"Invalid profile '{profile_name}' in {path}: {message} (key: {key})",
24	    )
25	
26	
27	def _validate_profile_map(path: Any, profile_name: str, raw_profile: Any) -> dict[str, str]:
28	    if not isinstance(raw_profile, dict):
29	        raise CliError(
30	            "invalid_profile",
31	            f"Invalid profile '{profile_name}' in {path}: expected a TOML table of phase keys",
32	        )
33	    validated: dict[str, str] = {}
34	    for phase, raw_spec in raw_profile.items():
35	        if phase not in VALID_PHASE_KEYS:
36	            _raise_invalid_profile(
37	                path,
38	                profile_name,
39	                str(phase),
40	                f"unknown phase '{phase}'. Valid phases: {', '.join(sorted(VALID_PHASE_KEYS))}",
41	            )
42	        if not isinstance(raw_spec, str):
43	            _raise_invalid_profile(path, profile_name, phase, f"expected a string agent spec, got {type(raw_spec).__name__}")
44	        agent, _model = parse_agent_spec(raw_spec)
45	        if agent not in KNOWN_AGENTS:
46	            _raise_invalid_profile(
47	                path,
48	                profile_name,
49	                phase,
50	                f"unknown agent '{agent}' in spec {raw_spec!r}. Valid agents: {', '.join(KNOWN_AGENTS)}",
51	            )
52	        validated[str(phase)] = raw_spec
53	    return validated
54	
55	
56	def _parse_profiles_doc(path: Any, content: str) -> dict[str, dict[str, str]]:
57	    try:
58	        data = tomllib.loads(content)
59	    except tomllib.TOMLDecodeError as exc:
60	        raise CliError("invalid_profile", f"Malformed TOML in {path}: {exc}") from exc
61	    if not data:
62	        return {}
63	    if not isinstance(data, dict):
64	        raise CliError("invalid_profile", f"Invalid profile file {path}: expected a TOML object at the top level")
65	    raw_profiles = data.get("profiles", {})
66	    if raw_profiles in ({}, None):
67	        return {}
68	    if not isinstance(raw_profiles, dict):
69	        raise CliError("invalid_profile", f"Invalid profile file {path}: [profiles] must be a TOML table")
70	    profiles: dict[str, dict[str, str]] = {}
71	    for profile_name, raw_profile in raw_profiles.items():
72	        profiles[profile_name] = _validate_profile_map(path, profile_name, raw_profile)
73	    return profiles
74	
75	
76	def _load_profiles_file(path: Any) -> dict[str, dict[str, str]]:
77	    try:
78	        content = path.read_text(encoding="utf-8")
79	    except FileNotFoundError:
80	        return {}
81	    except OSError as exc:
82	        raise CliError("invalid_profile", f"Unable to read profile file {path}: {exc}") from exc
83	    return _parse_profiles_doc(path, content)
84	
85	
86	def _built_in_profile_files() -> list[Any]:
87	    return sorted(
88	        (
89	            entry
90	            for entry in files("megaplan.profiles").iterdir()
91	            if entry.is_file() and entry.name.endswith(".toml")
92	        ),
93	        key=lambda entry: entry.name,
94	    )
95	
96	
97	def load_profile_sources(
98	    home: Path | None = None,
99	    project_dir: Path | None = None,
100	) -> list[tuple[str, str, dict[str, str]]]:
101	    sources: list[tuple[str, str, dict[str, str]]] = []
102	
103	    for path in _built_in_profile_files():
104	        for profile_name, phase_map in _load_profiles_file(path).items():
105	            sources.append(("built-in", profile_name, dict(phase_map)))
106	
107	    user_path = config_dir(home) / "profiles.toml"
108	    for profile_name, phase_map in _load_profiles_file(user_path).items():
109	        sources.append(("user", profile_name, dict(phase_map)))
110	
111	    if project_dir is not None:
112	        project_path = Path(project_dir) / ".megaplan" / "profiles.toml"
113	        for profile_name, phase_map in _load_profiles_file(project_path).items():
114	            sources.append(("project", profile_name, dict(phase_map)))
115	
116	    return sources
117	
118	
119	def load_profiles(
120	    home: Path | None = None,
121	    project_dir: Path | None = None,
122	) -> dict[str, dict[str, str]]:
123	    profiles: dict[str, dict[str, str]] = {}
124	    for _source_label, profile_name, phase_map in load_profile_sources(home=home, project_dir=project_dir):
125	        profiles[profile_name] = dict(phase_map)
126	    return profiles
127	
128	
129	def resolve_profile(name: str, profiles: dict[str, dict[str, str]]) -> dict[str, str]:
130	    try:
131	        return dict(profiles[name])
132	    except KeyError as exc:
133	        raise CliError(
134	            "unknown_profile",
135	            f"Unknown profile '{name}'. Known profiles: {_known_profiles_text(profiles)}",
136	        ) from exc
137	
138	
139	def profile_to_phase_models(profile: dict[str, str]) -> list[str]:
140	    return [f"{phase}={spec}" for phase, spec in profile.items()]
141	
142	
143	def apply_profile_expansion(
144	    args: argparse.Namespace,
145	    project_dir: Path | None,
146	    state: dict | None = None,
147	) -> argparse.Namespace:
148	    """Expand a --profile into per-phase --phase-model overrides.
149	
150	    The state fallback is needed because the auto-driver invokes each phase as a
151	    fresh subprocess that does not propagate the --profile flag, so handlers must
152	    recover the profile name from state['config']['profile'].
153	    """
154	    if getattr(args, "_profile_applied", False):
155	        return args
156	
157	    profile_name = getattr(args, "profile", None)
158	    if profile_name is None and state is not None:
159	        profile_name = (state.get("config") or {}).get("profile")
160	    phase_models = list(getattr(args, "phase_model", None) or [])
161	
162	    if profile_name:
163	        profiles = load_profiles(project_dir=project_dir)
164	        resolved = resolve_profile(profile_name, profiles)
165	        phase_models.extend(profile_to_phase_models(resolved))
166	        args.profile = profile_name
167	
168	    args.phase_model = phase_models
169	    args._profile_applied = True
170	    return args
171	
172	
173	__all__ = [
174	    "VALID_PHASE_KEYS",
175	    "apply_profile_expansion",
176	    "load_profile_sources",
177	    "load_profiles",
178	    "profile_to_phase_models",
179	    "resolve_profile",
180	]
181	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/profiles/standard.toml"
}
```

> TOOL

tool_result Read
```
1	# claude: plan/prep/revise/gate/finalize/loop_plan - codex: critique/execute/review/loop_execute/tiebreakers
2	[profiles.standard]
3	plan = "claude"
4	prep = "claude"
5	critique = "codex"
6	revise = "claude"
7	gate = "claude"
8	finalize = "claude"
9	execute = "codex"
10	loop_plan = "claude"
11	loop_execute = "codex"
12	review = "codex"
13	tiebreaker_researcher = "codex"
14	tiebreaker_challenger = "codex"
15	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
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
25	[project.optional-dependencies]
26	agent = [
27	    "openai",
28	    "anthropic>=0.39.0",
29	    "python-dotenv",
30	    "fire",
31	    "httpx",
32	    "rich",
33	    "tenacity",
34	    "pyyaml",
35	    "requests",
36	    "jinja2",
37	    "pydantic>=2.0",
38	    "prompt_toolkit",
39	    "firecrawl-py",
40	    "parallel-web>=0.4.2",
41	    "fal-client",
42	    "edge-tts",
43	    "faster-whisper>=1.0.0",
44	    "litellm>=1.75.5",
45	    "typer",
46	    "platformdirs",
47	    "PyJWT[crypto]",
48	]
49	
50	[project.scripts]
51	megaplan = "megaplan.cli:cli_entry"
52	
53	[tool.hatch.build.targets.wheel]
54	packages = ["megaplan"]
55	exclude = ["megaplan/cloud/_reference/**", "megaplan/agent/pyproject.toml"]
56	
57	[tool.pytest.ini_options]
58	testpaths = ["tests"]
59	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Now let me look at tests and phase artifacts:

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/tests/ 2>/dev/null | head -20"
}
```

> TOOL

tool_result Bash
```
total 1648
drwxr-xr-x   63 user_c042661f  staff   2016 Apr 23 23:22 .
drwxr-xr-x   25 user_c042661f  staff    800 Apr 23 22:52 ..
-rw-r--r--    1 user_c042661f  staff      0 Mar 20 17:09 __init__.py
drwxr-xr-x@ 125 user_c042661f  staff   4000 Apr 24 01:25 __pycache__
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

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/tests/test_auto.py",
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	"""Tests for megaplan.auto — the auto-driver loop.
2	
3	Focus: the rework-cycle-aware stall detector added in v0.18.1. A plan in
4	``finalized`` state that's doing review→rework loops should not be flagged
5	as stalled just because ``state`` hasn't advanced — new ``review.json``
6	artifacts indicate real forward progress.
7	"""
8	from __future__ import annotations
9	
10	import json
11	import os
12	from pathlib import Path
13	import sys
14	from unittest.mock import patch
15	
16	import pytest
17	
18	from megaplan import auto
19	from megaplan.auto import drive
20	
21	
22	def _make_plan_dir(tmp_path: Path, plan: str) -> Path:
23	    """Create a skeletal plan dir that `_resolve_plan_dir` can locate."""
24	    plan_dir = tmp_path / ".megaplan" / "plans" / plan
25	    plan_dir.mkdir(parents=True)
26	    (plan_dir / "state.json").write_text(
27	        json.dumps({"name": plan, "current_state": "finalized"}),
28	        encoding="utf-8",
29	    )
30	    return plan_dir
31	
32	
33	def _finalized_status(plan: str) -> dict:
34	    """Return a status snapshot that looks like 'review is next'."""
35	    return {
36	        "success": True,
37	        "step": "status",
38	        "plan": plan,
39	        "state": "finalized",
40	        "iteration": 1,
41	        "summary": "Plan is in state 'finalized'.",
42	        "next_step": "review",
43	        "valid_next": ["review"],
44	    }
45	
46	
47	def test_stall_counter_resets_when_review_json_is_rewritten(tmp_path: Path) -> None:
48	    """Stall detection must be rework-aware.
49	
50	    Simulates the production bug: state pinned at `finalized` while execute
51	    rework and review re-run. Each time review rewrites `review.json`, the
52	    stall counter must reset so the driver doesn't bail prematurely.
53	    """
54	    plan = "rework-plan"
55	    plan_dir = _make_plan_dir(tmp_path, plan)
56	    review_path = plan_dir / "review.json"
57	    review_path.write_text("{}", encoding="utf-8")
58	    base_mtime = review_path.stat().st_mtime
59	
60	    iteration_counter = {"n": 0}
61	
62	    def fake_status(plan_name: str, cwd=None, timeout=60):
63	        # Always return finalized — simulates state ping-pong that looks
64	        # stuck to the naive stall counter.
65	        return _finalized_status(plan_name)
66	
67	    def fake_run(args, cwd=None, timeout=None):
68	        # Every phase invocation bumps review.json mtime by 1s, simulating
69	        # a completed review cycle. Over 6 iterations the driver should
70	        # observe ~5 rework cycles — well past the default stall_threshold
71	        # of 5, but NOT bail because each cycle resets the counter.
72	        iteration_counter["n"] += 1
73	        new_mtime = base_mtime + iteration_counter["n"]
74	        os.utime(review_path, (new_mtime, new_mtime))
75	        return 0, "{}", ""
76	
77	    # Cap iterations low and allow plenty of rework cycles so we exercise
78	    # the reset path without tripping the rework cap.
79	    with patch.object(auto, "_status", side_effect=fake_status), \
80	         patch.object(auto, "_run_megaplan", side_effect=fake_run):

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"plan_v1\\|critique_v\\|execution.json\\|review_output\" /Users/user_c042661f/Documents/megaplan/megaplan --include=\"*.py\" | head -20"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/audits/iteration.py:    """Scan critique_v{N}.json artifacts to reconstruct per-flag status transitions."""
/Users/user_c042661f/Documents/megaplan/megaplan/audits/iteration.py:        critique_path = plan_dir / f"critique_v{iteration}.json"
/Users/user_c042661f/Documents/megaplan/megaplan/agent/evals/audit.py:    "execute": "execution.json",
/Users/user_c042661f/Documents/megaplan/megaplan/agent/evals/run_evals.py:        # Also check aggregate execution.json
/Users/user_c042661f/Documents/megaplan/megaplan/agent/evals/run_evals.py:        exec_path = plan_dir / "execution.json"
/Users/user_c042661f/Documents/megaplan/megaplan/agent/evals/run_evals.py:        filename = f"critique_v{iteration}.json"
/Users/user_c042661f/Documents/megaplan/megaplan/agent/evals/run_evals.py:        return "execution.json", _read_json_file(plan_dir / "execution.json")
/Users/user_c042661f/Documents/megaplan/megaplan/agent/auto_improve/dashboard.py:    for critique_file in sorted(run_dir.glob("megaplan/critique_v*.json")):
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_benchmark_scoring.py:    (fixture_dir / "plan_v1.md").write_text("# Plan\n", encoding="utf-8")
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_benchmark_scoring.py:    (fixture_dir / "plan_v1.meta.json").write_text(
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_benchmark_scoring.py:    (fixture_dir / "execution.json").write_text(json.dumps({"output": "ok"}), encoding="utf-8")
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_benchmark_scoring.py:    assert (plan_dir / "plan_v1.md").exists()
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_benchmark_scoring.py:    assert (plan_dir / "execution.json").exists()
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_benchmark_scoring.py:    assert "missing plan_v1.md" in issues
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_benchmark_scoring.py:    assert "missing execution.json" in issues
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_evals/test_run_evals.py:            self._write_json(self.plan_dir / f"critique_v{iteration}.json", {"phase": phase})
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_evals/test_run_evals.py:            self._write_json(self.plan_dir / "execution.json", {"phase": phase})
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_evals/test_audit.py:    assert (output_dir / "megaplan" / "critique_v2.json").exists()
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_evals/test_audit.py:    assert (output_dir / "traces" / "critique_v2.json").exists()
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_evals/test_audit.py:    assert (output_dir / "phases" / "critique_v2.json").exists()
```

> AGENT

Let me check the loop worktree code and more on auto driver:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/loop/git.py",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	"""Small git helpers for MegaLoop iterations."""
2	
3	from __future__ import annotations
4	
5	import re
6	import subprocess
7	from pathlib import Path
8	
9	
10	def _run_git(project_dir: str | Path, args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
11	    return subprocess.run(
12	        ["git", *args],
13	        cwd=str(project_dir),
14	        text=True,
15	        capture_output=True,
16	        check=check,
17	    )
18	
19	
20	def _normalize_pathspec(pattern: str) -> str:
21	    if pattern.startswith(":("):
22	        return pattern
23	    return f":(glob){pattern}"
24	
25	
26	def _changed_allowed_paths(project_dir: str | Path, allowed_changes: list[str]) -> list[str]:
27	    if not allowed_changes:
28	        return []
29	    status = _run_git(
30	        project_dir,
31	        ["status", "--porcelain", "--untracked-files=all", "--", *(_normalize_pathspec(item) for item in allowed_changes)],
32	    )
33	    paths: list[str] = []
34	    for line in status.stdout.splitlines():
35	        if len(line) < 4:
36	            continue
37	        path = line[3:]
38	        if " -> " in path:
39	            path = path.split(" -> ", 1)[1]
40	        if path not in paths:
41	            paths.append(path)
42	    return paths
43	
44	
45	def git_commit(project_dir: str | Path, message: str, allowed_changes: list[str]) -> str | None:
46	    changed_paths = _changed_allowed_paths(project_dir, allowed_changes)
47	    if not changed_paths:
48	        return None
49	    _run_git(project_dir, ["add", "--", *changed_paths])
50	    staged = _run_git(project_dir, ["diff", "--cached", "--name-only", "--", *changed_paths], check=False)
51	    if not staged.stdout.strip():
52	        return None
53	    _run_git(project_dir, ["commit", "-m", message, "--only", "--", *changed_paths])
54	    return git_current_sha(project_dir)
55	
56	
57	def git_revert(project_dir: str | Path, commit_sha: str) -> None:
58	    try:
59	        _run_git(project_dir, ["revert", "--no-edit", commit_sha])
60	    except subprocess.CalledProcessError:
61	        try:
62	            _run_git(project_dir, ["revert", "--abort"], check=False)
63	        except subprocess.CalledProcessError:
64	            pass
65	
66	
67	def git_current_sha(project_dir: str | Path) -> str:
68	    result = _run_git(project_dir, ["rev-parse", "HEAD"])
69	    return result.stdout.strip()
70	
71	
72	def parse_metric(output: str, pattern: str) -> float | None:
73	    match = re.search(pattern, output, re.MULTILINE)
74	    if match is None:
75	        return None
76	    captured = next((group for group in match.groups() if group is not None), match.group(0))
77	    try:
78	        return float(captured)
79	    except (TypeError, ValueError):
80	        numeric = re.search(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", str(captured))
81	        if numeric is None:
82	            return None
83	        try:
84	            return float(numeric.group(0))
85	        except ValueError:
86	            return None
87	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/auto.py",
  "limit": 250,
  "offset": 150
}
```

> TOOL

tool_result Read
```
150	        if (plan_dir / "state.json").exists():
151	            return plan_dir
152	    return None
153	
154	
155	def _get_review_marker(plan_dir: Path | None) -> float | None:
156	    """Return a monotonically-advancing marker for the current review cycle.
157	
158	    Uses ``review.json`` mtime — each completed review phase rewrites the
159	    file, so the mtime bumps once per review cycle. This is race-free
160	    enough for stall detection: the driver only checks the marker between
161	    iterations, and mtime granularity (~1s on APFS/ext4) is finer than the
162	    minimum review runtime.
163	
164	    Returns ``None`` when no marker is available (plan dir missing, review
165	    not yet run, or stat failed) — the caller must treat ``None == None``
166	    as "no progress observed" and fall through to plain stall detection.
167	    """
168	    if plan_dir is None:
169	        return None
170	    review_path = plan_dir / "review.json"
171	    try:
172	        return review_path.stat().st_mtime
173	    except (OSError, FileNotFoundError):
174	        return None
175	
176	
177	def drive(
178	    plan: str,
179	    *,
180	    cwd: Path | None = None,
181	    stall_threshold: int = DEFAULT_STALL_THRESHOLD,
182	    max_iterations: int = DEFAULT_MAX_ITERATIONS,
183	    max_review_rework_cycles: int = DEFAULT_MAX_REVIEW_REWORK_CYCLES,
184	    on_escalate: str = "force-proceed",
185	    poll_sleep: float = DEFAULT_POLL_SLEEP_SECONDS,
186	    phase_timeout: float = DEFAULT_PHASE_TIMEOUT_SECONDS,
187	    status_timeout: float = DEFAULT_STATUS_TIMEOUT_SECONDS,
188	    writer=sys.stdout.write,
189	) -> DriverOutcome:
190	    """Drive ``plan`` to completion.
191	
192	    Returns a DriverOutcome with a terminal status. The writer is used for
193	    human-readable progress; structured events are collected on the outcome.
194	    """
195	
196	    if on_escalate not in ESCALATE_ACTIONS:
197	        raise ValueError(f"on_escalate must be one of {ESCALATE_ACTIONS}")
198	
199	    events: list[dict[str, Any]] = []
200	    last_state: str | None = None
201	    stall_count = 0
202	    last_phase: str | None = None
203	
204	    # Rework-cycle tracking. When review returns `needs_rework`, the plan
205	    # ping-pongs `finalized ↔ executed ↔ finalized` while execute re-runs
206	    # batches. From the driver's naive view that looks like a stall, but
207	    # every completed review rewrites `review.json`, so its mtime is a
208	    # reliable "forward progress" marker — each advance means a real
209	    # review cycle finished since we last observed the state.
210	    plan_dir = _resolve_plan_dir(plan, cwd)
211	    last_review_marker = _get_review_marker(plan_dir)
212	    rework_cycles_observed = 0
213	
214	    def log(msg: str, **fields: Any) -> None:
215	        events.append({"msg": msg, **fields})
216	        writer(f"[auto {plan}] {msg}\n")
217	
218	    for iteration in range(1, max_iterations + 1):
219	        try:
220	            status = _status(plan, cwd=cwd, timeout=status_timeout)
221	        except (RuntimeError, json.JSONDecodeError) as error:
222	            log(f"status lookup failed: {error}")
223	            return DriverOutcome(
224	                status="failed",
225	                plan=plan,
226	                final_state=last_state or "unknown",
227	                iterations=iteration,
228	                reason=str(error),
229	                last_phase=last_phase,
230	                events=events,
231	            )
232	
233	        state = status.get("state", "")
234	        next_step = status.get("next_step")
235	        valid_next = status.get("valid_next") or []
236	
237	        log(
238	            f"iter {iteration} state={state} next={next_step} valid_next={valid_next}",
239	            iteration=iteration,
240	            state=state,
241	            next_step=next_step,
242	            valid_next=valid_next,
243	        )
244	
245	        # Terminal: plan reached a final state (or automation-terminal).
246	        if state in AUTOMATION_TERMINAL_STATES:
247	            if state == STATE_AWAITING_HUMAN:
248	                log("plan awaiting human verification — automation stopping")
249	                return DriverOutcome(
250	                    status="awaiting_human",
251	                    plan=plan,
252	                    final_state=state,
253	                    iterations=iteration,
254	                    reason="plan has criteria requiring human verification",
255	                    last_phase=last_phase,
256	                    events=events,
257	                )
258	            if state == STATE_TIEBREAKER_PENDING:
259	                log("tiebreaker pending — run 'megaplan tiebreaker-run --plan <name>' to execute")
260	                return DriverOutcome(
261	                    status="tiebreaker_pending",
262	                    plan=plan,
263	                    final_state=state,
264	                    iterations=iteration,
265	                    reason="gate recommended tiebreaker — researcher/challenger run needed",
266	                    last_phase=last_phase,
267	                    events=events,
268	                )
269	            if state == STATE_TIEBREAKER_READY:
270	                log("tiebreaker ready — run 'megaplan tiebreaker decide --plan <name>' to resolve")
271	                return DriverOutcome(
272	                    status="tiebreaker_ready",
273	                    plan=plan,
274	                    final_state=state,
275	                    iterations=iteration,
276	                    reason="tiebreaker synthesis complete — awaiting human decision",
277	                    last_phase=last_phase,
278	                    events=events,
279	                )
280	            log(f"terminal state reached: {state}")
281	            return DriverOutcome(
282	                status="done" if state == "done" else "aborted",
283	                plan=plan,
284	                final_state=state,
285	                iterations=iteration,
286	                reason=f"plan entered terminal state '{state}'",
287	                last_phase=last_phase,
288	                events=events,
289	            )
290	
291	        # Review-cycle progress: a fresh review.json means a real review
292	        # pass completed since the last iteration. This counts as forward
293	        # progress even when `state` looks unchanged (finalized→executed→
294	        # finalized during a needs_rework loop) — reset the stall counter
295	        # so execute has a full rework pass before tripping stall detection.
296	        current_review_marker = _get_review_marker(plan_dir)
297	        if (
298	            current_review_marker is not None
299	            and current_review_marker != last_review_marker
300	        ):
301	            if last_review_marker is not None:
302	                rework_cycles_observed += 1
303	                log(
304	                    f"review.json updated — rework cycle {rework_cycles_observed} "
305	                    f"observed, resetting stall counter",
306	                    rework_cycles_observed=rework_cycles_observed,
307	                )
308	                stall_count = 0
309	            last_review_marker = current_review_marker
310	
311	            if rework_cycles_observed > max_review_rework_cycles:
312	                # Review handler has its own internal cap (see
313	                # handlers.py::handle_review — force-proceeds to done when
314	                # prior_rework_count hits max_review_rework_cycles). This
315	                # driver cap is a belt-and-braces guard against config drift
316	                # or unexpected loops the handler didn't catch.
317	                log(
318	                    f"observed {rework_cycles_observed} rework cycles "
319	                    f"(cap={max_review_rework_cycles}) — bailing"
320	                )
321	                return DriverOutcome(
322	                    status="stalled",
323	                    plan=plan,
324	                    final_state=state,
325	                    iterations=iteration,
326	                    reason=(
327	                        f"exceeded review rework cap "
328	                        f"({rework_cycles_observed} cycles > "
329	                        f"{max_review_rework_cycles}) — review keeps "
330	                        "returning needs_rework without resolving"
331	                    ),
332	                    last_phase=last_phase,
333	                    events=events,
334	                )
335	
336	        # Stall detection: same state for stall_threshold+ iterations.
337	        if state == last_state:
338	            stall_count += 1
339	            if stall_count >= stall_threshold:
340	                # Distinguish an all-blocked outcome from a generic stall.
341	                # When execute reports every pending task as `blocked`, the
342	                # problem is a poisoned session or genuinely broken env —
343	                # supervisors should react differently (e.g. retry with a
344	                # fresh session) rather than just restart and loop.
345	                progress = status.get("progress") or {}
346	                tasks_blocked = int(progress.get("tasks_blocked", 0) or 0)
347	                tasks_pending = int(progress.get("tasks_pending", 0) or 0)
348	                if tasks_blocked > 0 and tasks_pending == 0:
349	                    log(
350	                        f"all pending tasks reported status=blocked "
351	                        f"({tasks_blocked} blocked) — treating as poisoned outcome"
352	                    )
353	                    return DriverOutcome(
354	                        status="blocked",
355	                        plan=plan,
356	                        final_state=state,
357	                        iterations=iteration,
358	                        reason=(
359	                            "all tasks reported blocked — workers may be poisoned "
360	                            "or the environment may genuinely be broken"
361	                        ),
362	                        last_phase=last_phase,
363	                        events=events,
364	                    )
365	                log(f"stalled at state={state} for {stall_count} iterations")
366	                return DriverOutcome(
367	                    status="stalled",
368	                    plan=plan,
369	                    final_state=state,
370	                    iterations=iteration,
371	                    reason=(
372	                        f"stalled at '{state}' for {stall_count} iterations — "
373	                        "manual intervention required"
374	                    ),
375	                    last_phase=last_phase,
376	                    events=events,
377	                )
378	        else:
379	            stall_count = 0
380	            last_state = state
381	
382	        # Escalation: no phase to run but overrides are available.
383	        if not next_step:
384	            if _has_valid_next(status, "override force-proceed"):
385	                if on_escalate == "force-proceed":
386	                    log("gate escalated — force-proceeding (per on_escalate=force-proceed)")
387	                    code, out, err = _run_megaplan(
388	                        [
389	                            "override",
390	                            "force-proceed",
391	                            "--plan",
392	                            plan,
393	                            "--reason",
394	                            "megaplan auto: escalate → force-proceed",
395	                        ],
396	                        cwd=cwd,
397	                        timeout=status_timeout,
398	                    )
399	                    if code != 0:

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Let me search for more info on state.json structure and artifact directories:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py",
  "limit": 200,
  "offset": 100
}
```

> TOOL

tool_result Read
```
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

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"state.json\" /Users/user_c042661f/Documents/megaplan/megaplan --include=\"*.py\" -A 3 | grep -E \"config|project_dir|state.json\" | head -30"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py:        if child.is_dir() and (child / "state.json").exists():
/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py:        if (plan_dir / "state.json").exists():
/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py:            if (candidate / "state.json").exists():
/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py:                if (candidate / "state.json").exists():
/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py:        state = read_json(plan_dir / "state.json")
/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py:    state = read_json(plan_dir / "state.json")
/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py:        atomic_write_json(plan_dir / "state.json", state)
/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py:    state_path = plan_dir / "state.json"
/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py:    atomic_write_json(plan_dir / "state.json", state)
/Users/user_c042661f/Documents/megaplan/megaplan/chain.py:Progress is persisted to ``chain_state.json`` beside the spec so a relaunched
/Users/user_c042661f/Documents/megaplan/megaplan/chain.py:    return spec_path.with_name("chain_state.json")
/Users/user_c042661f/Documents/megaplan/megaplan/chain.py:        raise CliError("invalid_chain_state", f"chain_state.json is invalid JSON: {exc}") from exc
/Users/user_c042661f/Documents/megaplan/megaplan/chain.py:        raise CliError("invalid_chain_state", "chain_state.json must be an object")
/Users/user_c042661f/Documents/megaplan/megaplan/agent/evals/run_evals.py:        artifact_name="state.json",
/Users/user_c042661f/Documents/megaplan/megaplan/agent/evals/run_evals.py:    state_path = plan_dir / "state.json"
/Users/user_c042661f/Documents/megaplan/megaplan/agent/evals/run_evals.py:        path = plan_dir / "state.json"
/Users/user_c042661f/Documents/megaplan/megaplan/agent/evals/run_evals.py:        return "state.json", _read_json_file(path)
/Users/user_c042661f/Documents/megaplan/megaplan/agent/auto_improve/cron.py:STATE_PATH = ITER_DIR / "_cron_state.json"
/Users/user_c042661f/Documents/megaplan/megaplan/agent/auto_improve/dashboard.py:    state_path = run_dir / "megaplan" / "state.json"
/Users/user_c042661f/Documents/megaplan/megaplan/agent/optional-skills/productivity/telephony/scripts/telephony.py:    return _hermes_home() / "telephony_state.json"
/Users/user_c042661f/Documents/megaplan/megaplan/agent/optional-skills/productivity/telephony/scripts/telephony.py-def _load_root_config() -> dict[str, Any]:
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_benchmark_scoring.py:    (plan_dir / "state.json").write_text(
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_benchmark_scoring.py:    state = json.loads((plan_dir / "state.json").read_text(encoding="utf-8"))
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_benchmark_scoring.py:    (plan_dir / "state.json").write_text(
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_evals/test_run_evals.py:        return self.plan_dir / "state.json"
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/skills/test_telephony_skill.py:    state = json.loads((tmp_path / ".hermes" / "telephony_state.json").read_text(encoding="utf-8"))
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/skills/test_telephony_skill.py:    state_path = tmp_path / "telephony_state.json"
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/skills/test_telephony_skill.py:    state_path = tmp_path / "telephony_state.json"
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/skills/test_telephony_skill.py:    state_path = tmp_path / "telephony_state.json"
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/skills/test_telephony_skill.py:        hermes_home / "telephony_state.json",
```

> AGENT

Let me check the types to understand DriverOutcome and plan state:

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"class PlanState\\|class DriverOutcome\\|config.*project_dir\" /Users/user_c042661f/Documents/megaplan/megaplan --include=\"*.py\" -A 5 | head -60"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py:    project_dir = Path(state["config"]["project_dir"])
/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py-    meta = read_json(latest_plan_meta_path(plan_dir, state))
/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py-    flag_registry = load_flag_registry(plan_dir)
/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py-    unresolved = unresolved_significant_flags(flag_registry)
/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py-    lookup = command_lookup or (lambda name: None)
/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py-    configured_agent = state.get("config", {}).get("agent", "")
--
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_benchmark_scoring.py:                "config": {"project_dir": str(workspace), "auto_approve": True, "robustness": "light"},
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_benchmark_scoring.py-                "meta": {"notes": ["keep"]},
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_benchmark_scoring.py-            }
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_benchmark_scoring.py-        ),
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_benchmark_scoring.py-        encoding="utf-8",
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_benchmark_scoring.py-    )
--
/Users/user_c042661f/Documents/megaplan/megaplan/types.py:class PlanState(TypedDict):
/Users/user_c042661f/Documents/megaplan/megaplan/types.py-    name: str
/Users/user_c042661f/Documents/megaplan/megaplan/types.py-    idea: str
/Users/user_c042661f/Documents/megaplan/megaplan/types.py-    current_state: str
/Users/user_c042661f/Documents/megaplan/megaplan/types.py-    iteration: int
/Users/user_c042661f/Documents/megaplan/megaplan/types.py-    created_at: str
--
/Users/user_c042661f/Documents/megaplan/megaplan/hermes_worker.py:    project_dir = Path(state["config"]["project_dir"])
/Users/user_c042661f/Documents/megaplan/megaplan/hermes_worker.py-    plan_mode = state["config"].get("mode", "code")
/Users/user_c042661f/Documents/megaplan/megaplan/hermes_worker.py-    from megaplan.schemas import get_execution_schema_key
/Users/user_c042661f/Documents/megaplan/megaplan/hermes_worker.py-    schema_name = get_execution_schema_key(plan_mode) if step == "execute" else STEP_SCHEMA_FILENAMES[step]
/Users/user_c042661f/Documents/megaplan/megaplan/hermes_worker.py-    schema = read_json(schemas_root(root) / schema_name)
/Users/user_c042661f/Documents/megaplan/megaplan/hermes_worker.py-    output_path: Path | None = None
--
/Users/user_c042661f/Documents/megaplan/megaplan/parallel_critique.py:    project_dir = Path(state["config"]["project_dir"])
/Users/user_c042661f/Documents/megaplan/megaplan/parallel_critique.py-    results: list[tuple[dict[str, Any], list[str], list[str]] | None] = [None] * len(checks)
/Users/user_c042661f/Documents/megaplan/megaplan/parallel_critique.py-    total_cost = 0.0
/Users/user_c042661f/Documents/megaplan/megaplan/parallel_critique.py-    total_prompt_tokens = 0
/Users/user_c042661f/Documents/megaplan/megaplan/parallel_critique.py-    total_completion_tokens = 0
/Users/user_c042661f/Documents/megaplan/megaplan/parallel_critique.py-    total_tokens = 0
--
/Users/user_c042661f/Documents/megaplan/megaplan/review/parallel.py:    project_dir = Path(state["config"]["project_dir"])
/Users/user_c042661f/Documents/megaplan/megaplan/review/parallel.py-    results: list[tuple[dict[str, Any], list[str], list[str]] | None] = [None] * len(checks)
/Users/user_c042661f/Documents/megaplan/megaplan/review/parallel.py-    criteria_payload: dict[str, Any] | None = None
/Users/user_c042661f/Documents/megaplan/megaplan/review/parallel.py-    total_cost = 0.0
/Users/user_c042661f/Documents/megaplan/megaplan/review/parallel.py-    total_prompt_tokens = 0
/Users/user_c042661f/Documents/megaplan/megaplan/review/parallel.py-    total_completion_tokens = 0
--
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/tiebreaker_challenger.py:    project_dir = Path(state["config"]["project_dir"])
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/tiebreaker_challenger.py-    prep_block, prep_instruction = _render_prep_block(plan_dir)
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/tiebreaker_challenger.py-
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/tiebreaker_challenger.py-    return textwrap.dedent(f"""\
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/tiebreaker_challenger.py-You are a senior engineer stress-testing a colleague's architectural research.
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/tiebreaker_challenger.py-Your mandate is **stress-test, not restate**. Do not summarize or agree with
--
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/tiebreaker_researcher.py:    project_dir = Path(state["config"]["project_dir"])
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/tiebreaker_researcher.py-    prep_block, prep_instruction = _render_prep_block(plan_dir)
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/tiebreaker_researcher.py-
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/tiebreaker_researcher.py-    plan_text = ""
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/tiebreaker_researcher.py-    try:
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/tiebreaker_researcher.py-        plan_path = latest_plan_path(plan_dir, state)
--
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/execute_doc.py:    project_dir = Path(state["config"]["project_dir"])
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/execute_doc.py-    output_path = state["config"].get("output_path", "output.md")
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/execute_doc.py-    prep_block, prep_instruction = _render_prep_block(plan_dir)
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/execute_doc.py-    finalize_data = read_json(plan_dir / "finalize.json")
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/types.py",
  "limit": 150
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
70	    # Fingerprint of the sandbox-affecting config captured when this session
71	    # was created (see megaplan.workers._sandbox_fingerprint). At resume
72	    # time we refuse to reuse a session whose fingerprint no longer matches
73	    # the current invocation — otherwise codex silently keeps the old
74	    # sandbox when the operator toggles MEGAPLAN_TRUSTED_CONTAINER or
75	    # changes --work-dir, leading to repeated invisible failures.
76	    sandbox_hash: str
77	
78	
79	class ActiveStep(TypedDict, total=False):
80	    step: str
81	    agent: str
82	    mode: str
83	    model: str
84	    run_id: str
85	    session_id: str
86	    started_at: str
87	
88	
89	class PlanVersionRecord(TypedDict, total=False):
90	    version: int
91	    file: str
92	    hash: str
93	    timestamp: str
94	
95	
96	class HistoryEntry(TypedDict, total=False):
97	    step: str
98	    timestamp: str
99	    duration_ms: int
100	    cost_usd: float
101	    result: str
102	    session_mode: str
103	    session_id: str
104	    agent: str
105	    output_file: str
106	    artifact_hash: str
107	    finalize_hash: str
108	    raw_output_file: str
109	    message: str
110	    flags_count: int
111	    flags_addressed: list[Any]
112	    recommendation: str
113	    approval_mode: str
114	    environment: dict[str, bool]
115	
116	
117	class ClarificationRecord(TypedDict, total=False):
118	    refined_idea: str
119	    intent_summary: str
120	    questions: list[str]
121	
122	
123	class LastGateRecord(TypedDict, total=False):
124	    recommendation: str
125	    rationale: str
126	    signals_assessment: str
127	    warnings: list[str]
128	    settled_decisions: list["SettledDecision"]
129	    passed: bool
130	    preflight_results: dict[str, bool]
131	    orchestrator_guidance: str
132	
133	
134	class PlanState(TypedDict):
135	    name: str
136	    idea: str
137	    current_state: str
138	    iteration: int
139	    created_at: str
140	    config: PlanConfig
141	    sessions: dict[str, SessionInfo]
142	    plan_versions: list[PlanVersionRecord]
143	    history: list[HistoryEntry]
144	    meta: PlanMeta
145	    last_gate: LastGateRecord
146	    active_step: NotRequired[ActiveStep]
147	    clarification: NotRequired[ClarificationRecord]
148	
149	
150	class _FlagRecordRequired(TypedDict):

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Perfect! Now let me check for handlers and phase structure:

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
total 288
drwxr-xr-x@ 15 user_c042661f  staff    480 Apr 23 23:22 .
drwxr-xr-x  30 user_c042661f  staff    960 Apr 23 23:23 ..
-rw-r--r--   1 user_c042661f  staff   2521 Apr 21 18:59 __init__.py
drwxr-xr-x@ 26 user_c042661f  staff    832 Apr 24 01:23 __pycache__
-rw-r--r--   1 user_c042661f  staff  17990 Apr 23 23:06 critique.py
-rw-r--r--   1 user_c042661f  staff   7227 Apr 23 23:17 execute.py
-rw-r--r--@  1 user_c042661f  staff  10142 Apr 22 04:18 finalize.py
-rw-r--r--   1 user_c042661f  staff  17637 Apr 23 23:06 gate.py
-rw-r--r--@  1 user_c042661f  staff   7387 Apr 23 22:17 init.py
-rw-r--r--   1 user_c042661f  staff   8947 Apr 21 13:20 override.py
-rw-r--r--@  1 user_c042661f  staff   6095 Apr 22 04:54 plan.py
-rw-r--r--   1 user_c042661f  staff  23158 Apr 23 23:22 review.py
-rw-r--r--   1 user_c042661f  staff  11875 Apr 23 23:22 shared.py
-rw-r--r--@  1 user_c042661f  staff   6681 Apr 23 22:18 tiebreaker.py
-rw-r--r--   1 user_c042661f  staff   4744 Apr 21 18:50 verifiability.py
```

> AGENT

Now let me look for the prep and revise handlers and check build_auto_parser:

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"def handle_prep\\|def handle_revise\" /Users/user_c042661f/Documents/megaplan/megaplan --include=\"*.py\""
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/handlers/plan.py:def handle_prep(root: Path, args: argparse.Namespace) -> StepResponse:
/Users/user_c042661f/Documents/megaplan/megaplan/handlers/critique.py:def handle_revise(root: Path, args: argparse.Namespace) -> StepResponse:
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/auto.py",
  "limit": 100,
  "offset": 400
}
```

> TOOL

tool_result Read
```
400	                        log(f"force-proceed failed (exit {code}): {err.strip() or out.strip()}")
401	                        return DriverOutcome(
402	                            status="failed",
403	                            plan=plan,
404	                            final_state=state,
405	                            iterations=iteration,
406	                            reason=f"override force-proceed exited {code}",
407	                            last_phase=last_phase,
408	                            events=events,
409	                        )
410	                    continue
411	                if on_escalate == "abort":
412	                    log("gate escalated — aborting (per on_escalate=abort)")
413	                    _run_megaplan(
414	                        [
415	                            "override",
416	                            "abort",
417	                            "--plan",
418	                            plan,
419	                            "--reason",
420	                            "megaplan auto: escalate → abort",
421	                        ],
422	                        cwd=cwd,
423	                        timeout=status_timeout,
424	                    )
425	                    return DriverOutcome(
426	                        status="aborted",
427	                        plan=plan,
428	                        final_state=state,
429	                        iterations=iteration,
430	                        reason="gate escalated and on_escalate=abort",
431	                        last_phase=last_phase,
432	                        events=events,
433	                    )
434	                # on_escalate == "fail"
435	                log("gate escalated — failing (per on_escalate=fail)")
436	                return DriverOutcome(
437	                    status="escalated",
438	                    plan=plan,
439	                    final_state=state,
440	                    iterations=iteration,
441	                    reason="gate escalated and on_escalate=fail — human required",
442	                    last_phase=last_phase,
443	                    events=events,
444	                )
445	            log(f"no next_step and no override available (valid_next={valid_next})")
446	            return DriverOutcome(
447	                status="failed",
448	                plan=plan,
449	                final_state=state,
450	                iterations=iteration,
451	                reason="no next_step and no override available",
452	                last_phase=last_phase,
453	                events=events,
454	            )
455	
456	        # Run the next phase.
457	        cmd = _phase_command(next_step) + ["--plan", plan]
458	        log(f"running: megaplan {' '.join(cmd)}", phase=next_step, timeout=phase_timeout)
459	        last_phase = next_step
460	        code, out, err = _run_megaplan(cmd, cwd=cwd, timeout=phase_timeout)
461	        if code == PHASE_TIMEOUT_EXIT_CODE:
462	            log(f"phase '{next_step}' timed out after {phase_timeout}s — stall detection will enforce the cap")
463	        elif code != 0:
464	            # Don't bail immediately — megaplan often records a partial failure
465	            # in state.json and the next status() reveals a recoverable valid_next.
466	            # Stall detection will still kill infinite loops.
467	            log(f"phase '{next_step}' exited {code}: {err.strip() or out.strip()[-400:]}")
468	        if poll_sleep > 0:
469	            time.sleep(poll_sleep)
470	
471	    # Hit iteration cap.
472	    log(f"hit max_iterations={max_iterations}")
473	    return DriverOutcome(
474	        status="cap",
475	        plan=plan,
476	        final_state=last_state or "unknown",
477	        iterations=max_iterations,
478	        reason=f"exceeded max_iterations={max_iterations}",
479	        last_phase=last_phase,
480	        events=events,
481	    )
482	
483	
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

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def build_auto_parser\\|def run_auto\" /Users/user_c042661f/Documents/megaplan/megaplan/auto.py"
}
```

> TOOL

tool_result Bash
```
484:def build_auto_parser(subparsers: Any) -> None:
561:def run_auto(root: Path, args: argparse.Namespace) -> int:
```

> AGENT

Now let me get a comprehensive look at the auto.py final parts and check for phase artifacts locations:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/auto.py",
  "limit": 100,
  "offset": 561
}
```

> TOOL

tool_result Read
```
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
584	        return 4
585	    # rc=3 is already claimed by 'escalated'; use rc=5 for all-blocked so the
586	    # supervisor can distinguish "workers said every task is blocked" from a
587	    # generic stall or escalation.
588	    if outcome.status == "blocked":
589	        return 5
590	    return 1
591	

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"plan_v\\|critique_v\\|execution\\.json\\|review\\.json\\|finalize\\.json\" /Users/user_c042661f/Documents/megaplan/megaplan/_core/io.py | head -20"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/io.py",
  "limit": 120
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

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/io.py",
  "limit": 100,
  "offset": 140
}
```

> TOOL

tool_result Read
```
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

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def.*plan.*path\\|def.*artifact\\|latest_.*path\" /Users/user_c042661f/Documents/megaplan/megaplan/_core/io.py"
}
```

> TOOL

tool_result Bash
```
298:def artifact_path(plan_dir: Path, filename: str) -> Path:
302:def batch_artifact_path(plan_dir: Path, batch_number: int) -> Path:
306:def list_batch_artifacts(plan_dir: Path) -> list[Path]:
323:def current_iteration_artifact(plan_dir: Path, prefix: str, iteration: int) -> Path:
327:def current_iteration_raw_artifact(plan_dir: Path, prefix: str, iteration: int) -> Path:
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/_core/io.py",
  "limit": 120,
  "offset": 285
}
```

> TOOL

tool_result Read
```
285	
286	def megaplan_root(root: Path) -> Path:
287	    return root / ".megaplan"
288	
289	
290	def plans_root(root: Path) -> Path:
291	    return megaplan_root(root) / "plans"
292	
293	
294	def schemas_root(root: Path) -> Path:
295	    return megaplan_root(root) / "schemas"
296	
297	
298	def artifact_path(plan_dir: Path, filename: str) -> Path:
299	    return plan_dir / filename
300	
301	
302	def batch_artifact_path(plan_dir: Path, batch_number: int) -> Path:
303	    return plan_dir / f"execution_batch_{batch_number}.json"
304	
305	
306	def list_batch_artifacts(plan_dir: Path) -> list[Path]:
307	    def sort_key(path: Path) -> tuple[int, str]:
308	        match = re.fullmatch(r"execution_batch_(\d+)\.json", path.name)
309	        if match is None:
310	            raise ValueError(f"Unexpected batch artifact filename: {path.name}")
311	        return (int(match.group(1)), path.name)
312	
313	    return sorted(
314	        (
315	            path
316	            for path in plan_dir.glob("execution_batch_*.json")
317	            if path.is_file() and re.fullmatch(r"execution_batch_(\d+)\.json", path.name)
318	        ),
319	        key=sort_key,
320	    )
321	
322	
323	def current_iteration_artifact(plan_dir: Path, prefix: str, iteration: int) -> Path:
324	    return plan_dir / f"{prefix}_v{iteration}.json"
325	
326	
327	def current_iteration_raw_artifact(plan_dir: Path, prefix: str, iteration: int) -> Path:
328	    return plan_dir / f"{prefix}_v{iteration}_raw.txt"
329	
330	
331	# ---------------------------------------------------------------------------
332	# Git diff summary (used by prompts)
333	# ---------------------------------------------------------------------------
334	
335	import subprocess
336	
337	
338	def collect_git_diff_summary(project_dir: Path) -> str:
339	    if not (project_dir / ".git").exists():
340	        return "Project directory is not a git repository."
341	    try:
342	        process = subprocess.run(
343	            ["git", "status", "--short"],
344	            cwd=str(project_dir),
345	            text=True,
346	            capture_output=True,
347	            timeout=30,
348	        )
349	    except FileNotFoundError:
350	        return "git not found on PATH."
351	    except subprocess.TimeoutExpired:
352	        return "git status timed out."
353	    if process.returncode != 0:
354	        return f"Unable to read git status: {process.stderr.strip() or process.stdout.strip()}"
355	    return process.stdout.strip() or "No git changes detected."
356	
357	
358	def collect_git_diff_patch(project_dir: Path) -> str:
359	    if not (project_dir / ".git").exists():
360	        return "Project directory is not a git repository."
361	
362	    def _run_git(
363	        args: list[str],
364	        *,
365	        allow_returncodes: tuple[int, ...] = (0,),
366	    ) -> tuple[subprocess.CompletedProcess[str] | None, str | None]:
367	        try:
368	            process = subprocess.run(
369	                ["git", *args],
370	                cwd=str(project_dir),
371	                text=True,
372	                capture_output=True,
373	                timeout=30,
374	            )
375	        except FileNotFoundError:
376	            return None, "git not found on PATH."
377	        except subprocess.TimeoutExpired:
378	            return None, "git diff timed out."
379	        if process.returncode not in allow_returncodes:
380	            detail = process.stderr.strip() or process.stdout.strip()
381	            return None, f"Unable to read git diff: {detail}"
382	        return process, None
383	
384	    tracked_process, error = _run_git(["diff", "--binary", "--no-ext-diff", "HEAD"])
385	    if error:
386	        return error
387	
388	    untracked_process, error = _run_git(["ls-files", "--others", "--exclude-standard"])
389	    if error:
390	        return error
391	
392	    patches: list[str] = []
393	    tracked_patch = (tracked_process.stdout if tracked_process is not None else "").rstrip()
394	    if tracked_patch:
395	        patches.append(tracked_patch)
396	
397	    untracked_paths = [
398	        line.strip()
399	        for line in (untracked_process.stdout if untracked_process is not None else "").splitlines()
400	        if line.strip()
401	    ]
402	    for rel_path in untracked_paths:
403	        if not (project_dir / rel_path).exists():
404	            continue

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Perfect! Let me now look for receipt/step_receipt more carefully and get info on latest_*_path functions:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"latest_plan_path\\|latest_critique_path\\|latest_.*path\" /Users/user_c042661f/Documents/megaplan/megaplan/_core/io.py"
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
  "command": "grep -r \"latest_plan_path\\|latest.*artifact\\|latest.*path\" /Users/user_c042661f/Documents/megaplan/megaplan --include=\"*.py\" | head -20"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/_core/__init__.py:    latest_plan_meta_path,
/Users/user_c042661f/Documents/megaplan/megaplan/_core/__init__.py:    latest_plan_path,
/Users/user_c042661f/Documents/megaplan/megaplan/_core/__init__.py:    "latest_plan_meta_path",
/Users/user_c042661f/Documents/megaplan/megaplan/_core/__init__.py:    "latest_plan_path",
/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py:def latest_plan_path(plan_dir: Path, state: PlanState) -> Path:
/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py:def latest_plan_meta_path(plan_dir: Path, state: PlanState) -> Path:
/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py:    latest_plan_meta_path,
/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py:    latest_plan_path,
/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py:    latest_plan_text = latest_plan_path(plan_dir, state).read_text(encoding="utf-8")
/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py:    meta = read_json(latest_plan_meta_path(plan_dir, state))
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/test_auth_nous_provider.py:def test_mint_retry_uses_latest_rotated_refresh_token(tmp_path, monkeypatch):
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/tiebreaker_researcher.py:    latest_plan_path,
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/tiebreaker_researcher.py:        plan_path = latest_plan_path(plan_dir, state)
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/execute_doc.py:    latest_plan_meta_path,
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/execute_doc.py:    latest_meta = read_json(latest_plan_meta_path(plan_dir, state))
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/execute.py:    latest_plan_meta_path,
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/execute.py:    latest_meta = read_json(latest_plan_meta_path(plan_dir, state))
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/finalize.py:    latest_plan_meta_path,
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/finalize.py:    latest_plan_path,
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/finalize.py:    latest_plan = latest_plan_path(plan_dir, state).read_text(encoding="utf-8")
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def latest_plan_path\\|def latest_plan_meta_path\" /Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py -A 5"
}
```

> TOOL

tool_result Bash
```
399:def latest_plan_path(plan_dir: Path, state: PlanState) -> Path:
400-    return plan_dir / latest_plan_record(state)["file"]
401-
402-
403:def latest_plan_meta_path(plan_dir: Path, state: PlanState) -> Path:
404-    record = latest_plan_record(state)
405-    meta_name = record["file"].replace(".md", ".meta.json")
406-    return plan_dir / meta_name
```

> AGENT

Now let me do a final check on the directory layout by looking at an example plan directory:

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan -type d -name \"plans\" 2>/dev/null | head -1 | xargs ls -la 2>/dev/null | head -20"
}
```

> TOOL

tool_result Bash
```
This Bash command contains multiple operations. The following part requires approval: xargs ls -la
```

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan/.megaplan/plans -type f -name \"*.json\" -o -name \"*.md\" 2>/dev/null | head -30"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/critique_v2.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/plan_v1.meta.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/state.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/critique_v3.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/execution_audit.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/gate_signals_v3.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/gate.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/plan_v1.md
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/gate_signals_v2.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/gate_signals_v1.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/plan_v2.md
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/plan_v3.meta.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/plan_v3.md
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/faults.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/final.md
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/review.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/plan_v2.meta.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/execution.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/critique_v1.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/update-main-py-to-print-the-20260410-0316/critique_output.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/update-main-py-to-print-the-20260410-0316/plan_v1.meta.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/update-main-py-to-print-the-20260410-0316/state.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/update-main-py-to-print-the-20260410-0316/gate.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/update-main-py-to-print-the-20260410-0316/plan_v1.md
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/update-main-py-to-print-the-20260410-0316/faults.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/update-main-py-to-print-the-20260410-0316/critique_v1.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/update-main-py-to-print-the-20260410-0320/critique_output.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/update-main-py-to-print-the-20260410-0320/plan_v1.meta.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/update-main-py-to-print-the-20260410-0320/state.json
```

> AGENT

Perfect! Now let me check for receipts more comprehensively:

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"receipt\" /Users/user_c042661f/Documents/megaplan/megaplan --include=\"*.py\" -i | head -20"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/agent/optional-skills/blockchain/base/scripts/base_client.py:        {"method": "eth_getTransactionReceipt", "params": [tx_hash]},
/Users/user_c042661f/Documents/megaplan/megaplan/agent/optional-skills/blockchain/base/scripts/base_client.py:    receipt = by_id.get(1)
/Users/user_c042661f/Documents/megaplan/megaplan/agent/optional-skills/blockchain/base/scripts/base_client.py:    gas_used = hex_to_int(receipt.get("gasUsed")) if receipt else None
/Users/user_c042661f/Documents/megaplan/megaplan/agent/optional-skills/blockchain/base/scripts/base_client.py:        hex_to_int(receipt.get("effectiveGasPrice")) if receipt and receipt.get("effectiveGasPrice")
/Users/user_c042661f/Documents/megaplan/megaplan/agent/optional-skills/blockchain/base/scripts/base_client.py:    l1_fee_wei = hex_to_int(receipt.get("l1Fee")) if receipt and receipt.get("l1Fee") else 0
/Users/user_c042661f/Documents/megaplan/megaplan/agent/optional-skills/blockchain/base/scripts/base_client.py:    if receipt:
/Users/user_c042661f/Documents/megaplan/megaplan/agent/optional-skills/blockchain/base/scripts/base_client.py:        out["status"] = "success" if receipt.get("status") == "0x1" else "failed"
/Users/user_c042661f/Documents/megaplan/megaplan/agent/optional-skills/blockchain/base/scripts/base_client.py:        out["contract_created"] = receipt.get("contractAddress")
/Users/user_c042661f/Documents/megaplan/megaplan/agent/optional-skills/blockchain/base/scripts/base_client.py:        out["log_count"] = len(receipt.get("logs", []))
/Users/user_c042661f/Documents/megaplan/megaplan/agent/optional-skills/blockchain/base/scripts/base_client.py:    if receipt:
/Users/user_c042661f/Documents/megaplan/megaplan/agent/optional-skills/blockchain/base/scripts/base_client.py:        for log in receipt.get("logs", []):
/Users/user_c042661f/Documents/megaplan/megaplan/agent/tests/gateway/test_slack.py:        """Reactions should be added on receipt and swapped on completion."""
/Users/user_c042661f/Documents/megaplan/megaplan/agent/gateway/platforms/signal.py:        # while still filtering other sync events (read receipts, typing, etc.)
/Users/user_c042661f/Documents/megaplan/megaplan/agent/gateway/platforms/webhook.py:        info stored during webhook receipt so it doesn't leak memory.
/Users/user_c042661f/Documents/megaplan/megaplan/agent/gateway/platforms/slack.py:        # Add 👀 reaction to acknowledge receipt
```

> AGENT

So receipts don't exist yet. Now let me check the loop engine for worktree code:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"worktree\\|git worktree\" /Users/user_c042661f/Documents/megaplan/megaplan/loop/engine.py | head -20"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/loop/engine.py",
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
26	from megaplan.profiles import apply_profile_expansion
27	from megaplan.workers import WorkerResult, resolve_agent_mode, run_step_with_worker, update_session_state
28	_DEFAULT_ALLOWED_CHANGES = ["."]
29	_COMMAND_OUTPUT_LIMIT = 12000
30	_DEFAULT_TIME_BUDGET_SECONDS = 300
31	_MONITORED_OUTPUT_BUFFER_LIMIT = 200_000
32	def _loop_dir(project_dir: str | Path, name: str) -> Path:
33	    return Path(project_dir) / ".megaplan" / "loops" / name
34	def _state_path(project_dir: str | Path, name: str) -> Path:
35	    return _loop_dir(project_dir, name) / "state.json"
36	def _normalized_args(args: argparse.Namespace | None) -> argparse.Namespace:
37	    values = vars(args).copy() if args is not None else {}
38	    if "phase_model" in values:
39	        values["phase_model"] = list(values["phase_model"] or [])
40	    normalized = argparse.Namespace(**values)
41	    defaults = {
42	        "agent": None,
43	        "phase_model": [],
44	        "hermes": None,
45	        "ephemeral": False,
46	        "fresh": False,
47	        "persist": False,
48	        "confirm_self_review": False,
49	        "iterations": None,
50	        "time_budget": None,
51	        "time_budget_seconds": None,
52	    }
53	    for key, value in defaults.items():
54	        if not hasattr(normalized, key):
55	            setattr(normalized, key, value)
56	    return normalized
57	def _string_list(value: Any, *, default: list[str] | None = None) -> list[str]:
58	    if value is None:
59	        return list(default or [])
60	    if isinstance(value, str):
61	        return [item.strip() for item in value.split(",") if item.strip()]
62	    if isinstance(value, (list, tuple)):
63	        return [str(item).strip() for item in value if str(item).strip()]
64	    return list(default or [])
65	def _merge_value(existing: Any, update: Any) -> Any:
66	    if isinstance(existing, list) and isinstance(update, list):
67	        merged: list[Any] = []
68	        for item in [*existing, *update]:
69	            if item not in merged:
70	                merged.append(item)
71	        return merged
72	    return update
73	def _merge_spec(spec: LoopSpec, updates: dict[str, Any]) -> LoopSpec:
74	    merged: LoopSpec = dict(spec)
75	    for key, value in updates.items():
76	        if value in (None, "", []):
77	            continue
78	        merged[key] = _merge_value(merged.get(key), value)
79	    return merged
80	def _time_budget_seconds(state: LoopState, args: argparse.Namespace | None) -> int:

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Perfect! Now let me verify some final details about DriverOutcome status values:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/auto.py",
  "limit": 60,
  "offset": 50
}
```

> TOOL

tool_result Read
```
50	@dataclass
51	class DriverOutcome:
52	    """Terminal outcome reported when the loop exits."""
53	
54	    status: str  # "done" | "stalled" | "escalated" | "failed" | "aborted" | "cap" | "blocked"
55	    plan: str
56	    final_state: str
57	    iterations: int
58	    reason: str = ""
59	    last_phase: str | None = None
60	    events: list[dict[str, Any]] = field(default_factory=list)
61	
62	    def to_json(self) -> str:
63	        return json.dumps(
64	            {
65	                "status": self.status,
66	                "plan": self.plan,
67	                "final_state": self.final_state,
68	                "iterations": self.iterations,
69	                "reason": self.reason,
70	                "last_phase": self.last_phase,
71	                "events": self.events,
72	            },
73	            indent=2,
74	        )
75	
76	
77	def _run_megaplan(
78	    args: list[str],
79	    *,
80	    cwd: Path | None = None,
81	    timeout: float | None = None,
82	) -> tuple[int, str, str]:
83	    """Run a megaplan sub-command in its own process.
84	
85	    We shell out rather than importing the handlers directly so each phase gets
86	    a fresh argparse/handler lifecycle. This matches how external orchestrators
87	    drive the CLI and avoids subtle state leakage between phases.
88	
89	    ``timeout`` is seconds to wait before killing the subprocess. On timeout we
90	    return exit code ``PHASE_TIMEOUT_EXIT_CODE`` and append a marker to stderr
91	    so the driver can surface it as a phase failure without crashing the loop.
92	    The subprocess is killed; any grandchildren it spawned (e.g. codex) may
93	    need a moment to settle but will exit when their parent's pipes close.
94	    """
95	    try:
96	        proc = subprocess.run(
97	            [sys.executable, "-m", "megaplan", *args],
98	            cwd=str(cwd) if cwd else None,
99	            capture_output=True,
100	            text=True,
101	            check=False,
102	            timeout=timeout,
103	        )
104	        return proc.returncode, proc.stdout, proc.stderr
105	    except subprocess.TimeoutExpired as expired:
106	        stdout = expired.stdout if isinstance(expired.stdout, str) else ""
107	        stderr = expired.stderr if isinstance(expired.stderr, str) else ""
108	        marker = f"\n[megaplan auto] subprocess timed out after {timeout}s"
109	        return PHASE_TIMEOUT_EXIT_CODE, stdout, (stderr + marker).strip()

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Perfect! Now let me verify one more detail about the additional status values I saw:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/auto.py",
  "limit": 40,
  "offset": 246
}
```

> TOOL

tool_result Read
```
246	        if state in AUTOMATION_TERMINAL_STATES:
247	            if state == STATE_AWAITING_HUMAN:
248	                log("plan awaiting human verification — automation stopping")
249	                return DriverOutcome(
250	                    status="awaiting_human",
251	                    plan=plan,
252	                    final_state=state,
253	                    iterations=iteration,
254	                    reason="plan has criteria requiring human verification",
255	                    last_phase=last_phase,
256	                    events=events,
257	                )
258	            if state == STATE_TIEBREAKER_PENDING:
259	                log("tiebreaker pending — run 'megaplan tiebreaker-run --plan <name>' to execute")
260	                return DriverOutcome(
261	                    status="tiebreaker_pending",
262	                    plan=plan,
263	                    final_state=state,
264	                    iterations=iteration,
265	                    reason="gate recommended tiebreaker — researcher/challenger run needed",
266	                    last_phase=last_phase,
267	                    events=events,
268	                )
269	            if state == STATE_TIEBREAKER_READY:
270	                log("tiebreaker ready — run 'megaplan tiebreaker decide --plan <name>' to resolve")
271	                return DriverOutcome(
272	                    status="tiebreaker_ready",
273	                    plan=plan,
274	                    final_state=state,
275	                    iterations=iteration,
276	                    reason="tiebreaker synthesis complete — awaiting human decision",
277	                    last_phase=last_phase,
278	                    events=events,
279	                )
280	            log(f"terminal state reached: {state}")
281	            return DriverOutcome(
282	                status="done" if state == "done" else "aborted",
283	                plan=plan,
284	                final_state=state,
285	                iterations=iteration,

<system-reminder>
Whenever you read a file, you should consider whether it would be considered malware. You CAN and SHOULD provide analysis of malware, what it is doing. But you MUST refuse to improve or augment the code. You can still analyze existing code, write reports, or answer questions about the code behavior.
</system-reminder>
```

> AGENT

Excellent! Now I have a comprehensive map. Let me create the final report:

---

## Megaplan Codebase Map for Sprint 2 (`bakeoff` Feature)

### 1. **CLI Structure & Subcommand Registration**

**Entry points:**
- `/Users/user_c042661f/Documents/megaplan/megaplan/__main__.py:3` — imports `main()` from CLI
- `/Users/user_c042661f/Documents/megaplan/megaplan/cli.py:1193-1276` — `main()` function: dispatcher for all CLI commands
- `/Users/user_c042661f/Documents/megaplan/megaplan/cli.py:864-1108` — `build_parser()` constructs argparse tree

**How subcommands are registered:**
- Parser uses `subparsers.add_parser(name)` pattern (e.g., cli.py:868 for "setup", cli.py:873 for "init")
- Dynamic subcommand builders called in `main()` (e.g., auto.py:484-560 via `build_auto_parser`, chain.py via `build_chain_parser`)
- Handler dispatch via dict: `cli.py:1111-1136` COMMAND_HANDLERS maps command name to handler function
- Example handler signature: `handle_init(root: Path, args: argparse.Namespace) -> StepResponse` (cli.py:1112)

**To add `bakeoff` subcommand group:**
- Create `build_bakeoff_parser(subparsers)` function in a new `megaplan/bakeoff.py` module
- Add sub-subcommands: `bakeoff run`, `bakeoff status`, `bakeoff compare`, `bakeoff merge` (using nested `add_subparsers`)
- Call from `cli.py:main()` around line 1076-1080 (after auto/chain imports)
- Add handlers dict entries in COMMAND_HANDLERS

---

### 2. **Auto Driver (`megaplan auto`)**

**Location & entry point:**
- `/Users/user_c042661f/Documents/megaplan/megaplan/auto.py` — entire driver implementation
- `build_auto_parser()` — line 484-560 (parser definition)
- `run_auto(root, args)` — line 561-590 (CLI handler)
- `drive(plan, *, cwd=None, ...)` — line 177-481 (core loop, CWD-based discovery)

**How it discovers plan dir:**
- `_resolve_plan_dir(plan, cwd)` — line 139-152: walks up parents from `cwd` looking for `.megaplan/plans/<plan>`, matches `megaplan status` logic
- Returns `None` if not found (safe fallback for optional features)

**Entry point signature:**
```python
def drive(plan: str, *, cwd: Path | None = None, stall_threshold=5, max_iterations=200, ...) -> DriverOutcome
```

**DriverOutcome type & status values:**
- Defined at `/Users/user_c042661f/Documents/megaplan/megaplan/auto.py:50-74` as `@dataclass`
- `status` field can be: `"done"` | `"stalled"` | `"escalated"` | `"failed"` | `"aborted"` | `"cap"` | `"blocked"` | `"awaiting_human"` | `"tiebreaker_pending"` | `"tiebreaker_ready"` (see lines 246-289 for terminal state handling)
- Exit codes: 0 (done/aborted), 2 (stalled), 3 (escalated), 4 (cap), 5 (blocked), 1 (other failures) — line 575-590

**Subprocess orchestration:**
- `_run_megaplan(args, cwd, timeout)` — line 77-109: uses `subprocess.run([sys.executable, "-m", "megaplan", *args], ...)` 
- Each phase runs as fresh subprocess to avoid state leakage (line 86-87 comment)
- Timeout handling: returns exit code 124 on timeout, captures stdout/stderr (line 95-109)

---

### 3. **Plan State & Configuration**

**State file location & structure:**
- **Path:** `.megaplan/plans/<plan-id>/state.json`
- **Type:** `PlanState` TypedDict defined at `/Users/user_c042661f/Documents/megaplan/megaplan/types.py:134-148`
- **Key fields:**
  - `config: PlanConfig` (line 140) contains:
    - `project_dir: str` (absolute path to workspace) — types.py:37
    - `auto_approve: bool`
    - `robustness: str`
    - `mode: str` ("code", "doc", "metaplan", "joke")
    - `output_path: str` (for doc modes)
    - `agents: dict[str, str]` (per-phase agent assignments)
  - `current_state: str` — one of: initialized, prepped, planned, critiqued, gated, finalized, executed, done, aborted, awaiting_human_verify, tiebreaker_pending, tiebreaker_ready (types.py:12-28)
  - `iteration: int` — incremented per phase
  - `history: list[HistoryEntry]` — audit trail with cost_usd per step
  - `sessions: dict[str, SessionInfo]` — persistent session handles per agent
  - `meta: PlanMeta` — notes, costs, overrides
  - `last_gate: LastGateRecord` — gate signals + recommendation

**Load/save functions:**
- Load: `/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py:95-98` `load_plan(root, requested_name) -> (Path, PlanState)`
- Save: `/Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py:218` `save_state(plan_dir, state)`

---

### 4. **Named Profiles**

**Format & location:**
- TOML files: `[profiles.<name>]` — maps phase name to agent spec
- Loaded from three layers (in order of precedence):
  1. Project layer: `.megaplan/profiles.toml` (local to plan's project dir)
  2. User layer: `~/.config/megaplan/profiles.toml`
  3. Built-in: `/Users/user_c042661f/Documents/megaplan/megaplan/profiles/standard.toml` + `/megaplan/profiles/all-open.toml`

**Example (`standard.toml` lines 1-15):**
```toml
[profiles.standard]
plan = "claude"
critique = "codex"
execute = "codex"
review = "codex"
```

**Loading & usage:**
- `load_profiles(home=None, project_dir=None)` — `/Users/user_c042661f/Documents/megaplan/megaplan/profiles/__init__.py:119-126` returns dict[name → phase_map]
- `resolve_profile(name, profiles)` — line 129-136 retrieves one profile
- `apply_profile_expansion(args, project_dir, state)` — line 143-170 converts `--profile name` into `--phase-model phase=agent:model` list
- Current flag: `--profile <name>` in init, plan, prep, critique, revise, gate, finalize, execute, review (see cli.py:911, 942, etc.)

---

### 5. **Plan Directory Discovery & Circular Recursion Risk**

**Current mechanisms:**
- **Tree search** (`--tree` default in `list`): walks up parents + down children via `rglob(".megaplan")` — cli.py:410, 426, 70
- **Flat search** (`--no-tree`): current directory only
- **System-wide** (`--all`): `home.rglob(".megaplan")` — cli.py:410
- **Risk comment:** The brief mentions "circular recursion" — code uses `rglob` which can traverse very large trees (see state.py:70 `root.resolve().rglob(".megaplan")`)

**For `bakeoff`:**
- Plan dir discovery uses `resolve_plan_dir(root, plan_name)` — state.py:53-92
- Walks up then down from a CWD-relative root
- **No circular recursion**: each `rglob` is explicit and terminates (not a walk-up from nested .megaplan dirs)

---

### 6. **Step Receipts & Canonical Hashes (Sprint 1 Prerequisite)**

**Current status: NOT IMPLEMENTED**

- No `receipt`, `step_receipt`, or similar concept found in codebase
- No canonical prompt hash storage identified
- No global audit log beyond `state.json["history"]` (which records phase completion with cost_usd, but not input/output hashes)
- `HistoryEntry` (types.py:96-115) includes `artifact_hash` and `finalize_hash` but NO input-hash or receipt ID

**For bakeoff `compare` subcommand:**
- Will need to either:
  1. Implement receipts first (hash of prompt + state → runnable artifact ID), OR
  2. Use filenames as proxies: `plan_v1.md`, `critique_v2.json`, `execution.json` are versioned, but profiles/prompt changes aren't hashed
- Current artifact paths: see next section

**Scope drift metric:** NOT FOUND (no existing `scope_drift` field in state or evaluation code)

---

### 7. **Phase Artifacts & Directory Layout**

**All artifacts live in plan_dir (`.megaplan/plans/<plan-id>/`):**

| Phase | Output Files |
|-------|------|
| **plan** | `plan_v{N}.md`, `plan_v{N}.meta.json` |
| **prep** | (metadata only in plan_v{N}.meta.json) |
| **critique** | `critique_v{N}.json`, `critique_output.json` |
| **revise** | (modifies plan_v{N}.md) |
| **gate** | `gate.json`, `gate_signals_v{N}.json` |
| **finalize** | `finalize.json` |
| **execute** | `execution.json`, `execution_batch_1.json`, `execution_batch_2.json`, ... |
| **review** | `review.json` |
| **final** | `final.md` (doc mode only) |
| **fault tracking** | `faults.json` |

**Path functions:**
- `latest_plan_path(plan_dir, state)` — state.py:399-400 returns `plan_v{iteration}.md`
- `current_iteration_artifact(plan_dir, prefix, iteration)` — io.py:323-324 returns `{prefix}_v{iteration}.json`
- `batch_artifact_path(plan_dir, batch_number)` — io.py:302-303 returns `execution_batch_{N}.json`

---

### 8. **Existing Subprocess Orchestration**

**Yes — auto driver shells out per phase:**
- `_run_megaplan(args, cwd, timeout)` — auto.py:77-109
- Each phase runs: `python -m megaplan <phase> --plan <name>` in subprocess
- Used for stall detection + timeout enforcement (line 86-87 comment: "each phase gets a fresh lifecycle")

**Subprocess management:**
- `subprocess.run()` with `capture_output=True`, `timeout=<phase_timeout>` (default 3600s)
- On timeout: returns code 124, captures partial stdout/stderr
- Poll sleep between iterations: default 1.0s (can be overridden)

---

### 9. **Test Layout**

**Location:** `/Users/user_c042661f/Documents/megaplan/tests/`

**Key test files:**
- `test_auto.py` — auto-driver loop tests (stall detection, rework cycles)
- `test_cli_entry.py` — CLI entry point
- `test_chain.py` — chain orchestration
- `test_audits.py` — audit engine
- Fixtures in `tests/fixtures/`

**CLI testing pattern:**
- Parse args, call handler, check response dict
- Example: `test_auto.py:47-83` mocks `_status()` and `_run_megaplan()` to simulate plan progression

---

### 10. **Git Worktree Usage**

**Currently:**
- `megaplan/loop/git.py` — git helpers for MegaLoop (commit, revert, sha extraction), NOT worktree-specific
- `subprocess.run(["git", ...], cwd=project_dir)` — used in loop engine for commits (engine.py:23)
- No native `git worktree` commands in core megaplan

**For `bakeoff`:**
- Will need to add worktree creation: `git worktree add <path> <ref>`
- Cleanup: `git worktree remove <path>`
- Each profile run in isolation (separate working dir)

---

### 11. **Pyproject & Dependencies**

**Location:** `/Users/user_c042661f/Documents/megaplan/pyproject.toml`

**Package:**
- Name: `megaplan-harness`
- Python: `>=3.11`
- Entry point: `megaplan = "megaplan.cli:cli_entry"` (line 51)

**Core dependencies:** PyYAML
**Optional (agent extras):** anthropic>=0.39.0, openai, fire, httpx, rich, tenacity, pydantic>=2.0, etc.

**For async/subprocess:** Only stdlib `subprocess` is used (no asyncio in core CLI, though agent bundle has more)

---

## Quick Reference for Bakeoff Implementation

**Handlers will need:**
1. New `megaplan/bakeoff.py` with:
   - `build_bakeoff_parser(subparsers)` — define run/status/compare/merge sub-subcommands
   - `run_bakeoff_run(root, args)` — create N worktrees, call `run_auto()` in each, collect DriverOutcome per profile
   - `run_bakeoff_status(root, args)` — poll all active worktree plans
   - `run_bakeoff_compare(root, args)` — read execution/review artifacts per profile, diff metrics (awaiting receipts)
   - `run_bakeoff_merge(root, args)` — merge winner back to main branch, cleanup worktrees

2. **Plan discovery:** Use `_find_megaplan_root()` from cli.py:1143 + `resolve_plan_dir()` from state.py:53
3. **State/artifacts:** Load via `load_plan()` (state.py:95), access `state["config"]["project_dir"]` for subprocess context
4. **Profile expansion:** Call `apply_profile_expansion(args, project_dir, state)` to apply `--profile` before each worktree run
5. **Wait for receipts:** Phase 1 deliverable per brief — store hashes/canonical prompts in `state.json` or new `receipts.json`

---

That's your tight, navigable map. All file:line references are actionable for a planning document.
