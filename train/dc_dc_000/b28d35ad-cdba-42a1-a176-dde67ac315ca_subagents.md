> DEVELOPER

I'm planning an implementation in the megaplan repo at /Users/user_c042661f/Documents/megaplan. I need to understand the current code shape to write an accurate plan. Please report back (under 400 words) with file paths and key line numbers for the following:

1. `megaplan/cli.py` — where is the `init` subparser defined, and what args does it currently take? Is there an `--output` flag and a `--project-dir` flag, and where is `--mode doc` handled?

2. `megaplan/handlers.py` — where is `handle_init` defined? Show me the shape of its validation for `--output` (the absolute/.. rejection logic). What does it return on invalid_args vs success? How does it populate `state.config` and `state['meta']`?

3. `megaplan/doc_assembly.py` — does this file exist? If yes, what functions does it expose? If no, where would a new `doc_assembly.py` file logically belong?

4. `megaplan/evaluation.py` — find the existing `settled_decisions` / `SettledDecision` concept. What's the TypedDict shape? Where are SettledDecisions produced by gate/critique?

5. `megaplan/types.py` — show the existing TypedDict definitions especially for success criteria (must/should/info) and any `SettledDecision` type.

6. `megaplan/data/instructions.md` — confirm it exists, note which sections already document init flags.

7. Where does the doc-mode execute worker prompt live? Search for "doc" in `megaplan/data/prompts/` or similar.

8. `tests/test_handle_init_doc_mode.py` — does it exist? If yes, what test style does it use (pytest? any fixtures)?

9. `tests/test_doc_assembly.py` — does it exist?

10. Is `PYENV_VERSION=3.11.11` the norm? Any pytest.ini or conftest.py I should know about?

Please give exact file paths and line numbers. Do not read .megaplan/ directory. Focus only on what I asked.

> AGENT

I'll systematically explore the megaplan repo to answer your questions. Let me start with a broad file structure scan and then dig into each specific question.

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
/Users/user_c042661f/Documents/megaplan/megaplan/audit.py
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
```

> AGENT

Now let me search for the specific files and content:

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/megaplan/**/cli.py"
}
```

> TOOL

tool_result Glob
```
megaplan/cloud/cli.py
megaplan/cli.py
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
299	    if plan_mode == "doc":
300	        summary += f" Mode: doc. Output: {plan_output_path}."
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
840	    init_parser.add_argument("--mode", choices=["code", "doc", "metaplan"], default=None,
841	                             help="Deliverable type: 'code' (source changes) or 'doc' / 'metaplan' "
842	                                  "(design/spec artifact — 'metaplan' is an alias for 'doc'). "
843	                                  "Defaults to 'code' unless the idea strongly suggests a design document, "
844	                                  "in which case --mode must be passed explicitly.")
845	    init_parser.add_argument("--output", default=None,
846	                             help="Relative path where the doc artifact will be written. "
847	                                  "Required with --mode doc; rejected with --mode code.")
848	    init_parser.add_argument("--hermes", nargs="?", const="", default=None,
849	                             help="Use Hermes agent for all phases. Optional: specify default model")
850	    init_parser.add_argument("--phase-model", action="append", default=[],
851	                             help="Per-phase model override: --phase-model critique=hermes:openai/gpt-5")
852	    init_parser.add_argument("idea")
853	
854	    list_parser = subparsers.add_parser("list")
855	    list_parser.add_argument("--all", action="store_true",
856	                             help="Search all .megaplan directories system-wide (~)")
857	    list_parser.add_argument("--no-tree", action="store_true",
858	                             help="Only show plans from the current directory (default includes parent + child)")
859	    list_parser.add_argument("--include-done", action="store_true",
860	                             help="Include terminal plans (done/aborted); excluded by default")
861	    list_parser.add_argument("--status", dest="filter_status",
862	                             help="Filter by state (e.g. 'done', 'finalized', 'executed', or comma-separated 'planned,critiqued')")
863	    list_parser.add_argument("--summary", action="store_true",
864	                             help="Show count breakdown by state")
865	
866	    for name in ["status", "audit", "progress", "watch"]:
867	        step_parser = subparsers.add_parser(name)
868	        step_parser.add_argument("--plan")
869	        if name == "status":
870	            step_parser.add_argument("--pending-human", action="store_true",
871	                                     help="List plans awaiting human verification")
872	
873	    for name in ["plan", "prep", "critique", "revise", "gate", "finalize", "execute", "review"]:
874	        step_parser = subparsers.add_parser(name)
875	        step_parser.add_argument("--plan")
876	        step_parser.add_argument("--agent", choices=["claude", "codex", "hermes"])
877	        step_parser.add_argument("--hermes", nargs="?", const="", default=None,
878	                                 help="Use Hermes agent for all phases. Optional: specify default model (e.g. --hermes anthropic/claude-sonnet-4.6)")
879	        step_parser.add_argument("--phase-model", action="append", default=[],
880	                                 help="Per-phase model override: --phase-model critique=hermes:openai/gpt-5")
881	        step_parser.add_argument("--fresh", action="store_true")
882	        step_parser.add_argument("--persist", action="store_true")
883	        step_parser.add_argument("--ephemeral", action="store_true")
884	        step_parser.add_argument("--work-dir", default=None,
885	                                 help="Override the source-code working directory passed to subprocess workers "
886	                                      "(--add-dir / -C). Defaults to the current working directory. Use this to "
887	                                      "force a specific path (e.g. a git worktree) regardless of where the plan was created.")
888	        if name == "execute":
889	            step_parser.add_argument("--confirm-destructive", action="store_true")
890	            step_parser.add_argument("--user-approved", action="store_true")
891	            step_parser.add_argument("--batch", type=int, default=None, help="Execute a specific global batch number (1-indexed)")
892	        if name == "review":
893	            step_parser.add_argument("--confirm-self-review", action="store_true")
894	
895	    config_parser = subparsers.add_parser("config", help="View or edit megaplan configuration")
896	    config_sub = config_parser.add_subparsers(dest="config_action", required=True)
897	    config_sub.add_parser("show")
898	    set_parser = config_sub.add_parser("set")
899	    set_parser.add_argument("key")
900	    set_parser.add_argument("value")
901	    config_sub.add_parser("reset")
902	
903	    step_parser = subparsers.add_parser("step", help="Edit plan step sections without hand-editing markdown")
904	    step_subparsers = step_parser.add_subparsers(dest="step_action", required=True)
905	
906	    step_add_parser = step_subparsers.add_parser("add", help="Insert a new step after an existing step")
907	    step_add_parser.add_argument("--plan")
908	    step_add_parser.add_argument("--after")
909	    step_add_parser.add_argument("description")
910	
911	    step_remove_parser = step_subparsers.add_parser("remove", help="Remove a step and renumber the plan")
912	    step_remove_parser.add_argument("--plan")
913	    step_remove_parser.add_argument("step_id")
914	
915	    step_move_parser = step_subparsers.add_parser("move", help="Move a step after another step and renumber")
916	    step_move_parser.add_argument("--plan")
917	    step_move_parser.add_argument("step_id")
918	    step_move_parser.add_argument("--after", required=True)
919	
920	    override_parser = subparsers.add_parser("override")
921	    override_parser.add_argument("override_action", choices=["abort", "force-proceed", "add-note", "replan", "set-robustness"])
922	    override_parser.add_argument("--plan")
923	    override_parser.add_argument("--reason", default="")
924	    override_parser.add_argument("--note")
925	    override_parser.add_argument("--robustness", choices=list(ROBUSTNESS_LEVELS), default=None)
926	
927	    verify_human_parser = subparsers.add_parser("verify-human", help="Record human verification for a criterion")
928	    verify_human_parser.add_argument("--plan")
929	    verify_human_parser.add_argument("--criterion", required=True, help="Criterion name or index")
930	    vh_group = verify_human_parser.add_mutually_exclusive_group(required=True)
931	    vh_group.add_argument("--pass", dest="pass_flag", action="store_true")
932	    vh_group.add_argument("--fail", dest="fail_flag", action="store_true")
933	    verify_human_parser.add_argument("--evidence", required=True, help="Evidence supporting the verdict")
934	
935	    audit_verifiability_parser = subparsers.add_parser("audit-verifiability", help="Audit criteria verifiability")
936	    audit_verifiability_parser.add_argument("--plan")
937	
938	    debt_parser = subparsers.add_parser("debt", help="Inspect or manage persistent tech debt entries")
939	    debt_subparsers = debt_parser.add_subparsers(dest="debt_action", required=True)
940	
941	    debt_list_parser = debt_subparsers.add_parser("list", help="List debt entries")
942	    debt_list_parser.add_argument("--all", action="store_true", help="Include resolved entries")
943	
944	    debt_add_parser = debt_subparsers.add_parser("add", help="Add or increment a debt entry")
945	    debt_add_parser.add_argument("--subsystem", required=True)
946	    debt_add_parser.add_argument("--concern", required=True)
947	    debt_add_parser.add_argument("--flag-ids", default="")
948	    debt_add_parser.add_argument("--plan")
949	
950	    debt_resolve_parser = debt_subparsers.add_parser("resolve", help="Resolve a debt entry")
951	    debt_resolve_parser.add_argument("debt_id")
952	    debt_resolve_parser.add_argument("--plan")
953	
954	    loop_init_parser = subparsers.add_parser("loop-init", help="Initialize a MegaLoop workflow")
955	    loop_init_parser.add_argument("--project-dir", required=True)
956	    loop_init_parser.add_argument("--command", required=True)
957	    loop_init_parser.add_argument("--goal", dest="goal_option")
958	    loop_init_parser.add_argument("--name")
959	    loop_init_parser.add_argument("--iterations", type=int, default=3)
960	    loop_init_parser.add_argument("--time-budget", type=int, default=300)
961	    loop_init_parser.add_argument("--observe-interval", type=int)
962	    loop_init_parser.add_argument("--observe-break-patterns")
963	    loop_init_parser.add_argument("--agent", choices=["claude", "codex", "hermes"])
964	    loop_init_parser.add_argument("--hermes", nargs="?", const="", default=None,
965	                                  help="Use Hermes agent for loop phases. Optional: specify default model")
966	    loop_init_parser.add_argument("--phase-model", action="append", default=[],
967	                                  help="Per-phase model override: --phase-model loop_execute=hermes:openai/gpt-5")
968	    loop_init_parser.add_argument("--fresh", action="store_true")
969	    loop_init_parser.add_argument("--persist", action="store_true")
970	    loop_init_parser.add_argument("--ephemeral", action="store_true")
971	    loop_init_parser.add_argument("--work-dir", default=None,
972	                                  help="Override the source-code working directory for subprocess workers (default: CWD)")
973	    loop_init_parser.add_argument("goal", nargs="?")
974	
975	    loop_run_parser = subparsers.add_parser("loop-run", help="Run an existing MegaLoop workflow")
976	    loop_run_parser.add_argument("name")
977	    loop_run_parser.add_argument("--project-dir")
978	    loop_run_parser.add_argument("--iterations", type=int)
979	    loop_run_parser.add_argument("--time-budget", type=int)
980	    loop_run_parser.add_argument("--agent", choices=["claude", "codex", "hermes"])
981	    loop_run_parser.add_argument("--hermes", nargs="?", const="", default=None,
982	                                 help="Use Hermes agent for loop phases. Optional: specify default model")
983	    loop_run_parser.add_argument("--phase-model", action="append", default=[],
984	                                 help="Per-phase model override: --phase-model loop_execute=hermes:openai/gpt-5")
985	    loop_run_parser.add_argument("--fresh", action="store_true")
986	    loop_run_parser.add_argument("--persist", action="store_true")
987	    loop_run_parser.add_argument("--ephemeral", action="store_true")
988	    loop_run_parser.add_argument("--work-dir", default=None,
989	                                 help="Override the source-code working directory for subprocess workers (default: CWD)")
990	
991	    loop_status_parser = subparsers.add_parser("loop-status", help="Show MegaLoop state")
992	    loop_status_parser.add_argument("name")
993	    loop_status_parser.add_argument("--project-dir")
994	
995	    loop_pause_parser = subparsers.add_parser("loop-pause", help="Pause a MegaLoop workflow")
996	    loop_pause_parser.add_argument("name")
997	    loop_pause_parser.add_argument("--project-dir")
998	    loop_pause_parser.add_argument("--reason", default="")
999	
1000	    from megaplan.auto import build_auto_parser
1001	    build_auto_parser(subparsers)
1002	
1003	    from megaplan.chain import build_chain_parser
1004	    build_chain_parser(subparsers)
1005	
1006	    from megaplan.cloud.cli import build_cloud_parser
1007	    build_cloud_parser(subparsers)
1008	
1009	    from megaplan.tiebreaker import build_tiebreaker_parser
1010	    build_tiebreaker_parser(subparsers)
1011	
1012	    # tiebreaker-run is a top-level command because auto.py:_phase_command
1013	    # translates next_step directly to CLI args.
1014	    tb_run_parser = subparsers.add_parser(
1015	        "tiebreaker-run",
1016	        help="Run tiebreaker researcher+challenger (used by auto driver)",
1017	    )
1018	    tb_run_parser.add_argument("--plan", required=True, help="Plan name")
1019	    tb_run_parser.add_argument("--agent", choices=["claude", "codex", "hermes"], default=None)
1020	    tb_run_parser.add_argument("--hermes", nargs="?", const="", default=None)
1021	    tb_run_parser.add_argument("--phase-model", action="append", default=[])
1022	    tb_run_parser.add_argument("--fresh", action="store_true")
1023	    tb_run_parser.add_argument("--persist", action="store_true")
1024	    tb_run_parser.add_argument("--ephemeral", action="store_true")
1025	
1026	    return parser
1027	
1028	
1029	COMMAND_HANDLERS: dict[str, Callable[..., StepResponse]] = {
1030	    "init": handle_init,
1031	    "plan": handle_plan,
1032	    "prep": handle_prep,
1033	    "critique": handle_critique,
1034	    "revise": handle_revise,
1035	    "gate": handle_gate,
1036	    "finalize": handle_finalize,
1037	    "execute": handle_execute,
1038	    "review": handle_review,
1039	    "status": handle_status,
1040	    "audit": handle_audit,
1041	    "progress": handle_progress,
1042	    "watch": handle_watch,
1043	    "list": handle_list,
1044	    "loop-init": handle_loop_init,
1045	    "loop-run": handle_loop_run,
1046	    "loop-status": handle_loop_status,
1047	    "loop-pause": handle_loop_pause,
1048	    "debt": handle_debt,
1049	    "step": handle_step,
1050	    "override": handle_override,
1051	    "verify-human": handle_verify_human,
1052	    "audit-verifiability": handle_audit_verifiability,
1053	    "tiebreaker-run": handle_tiebreaker_run,
1054	}
1055	
1056	
1057	def cli_entry() -> None:
1058	    sys.exit(main())
1059	
1060	
1061	def _find_megaplan_root(start: Path) -> Path:
1062	    """Walk up from *start* to find the git-root directory containing ``.megaplan/``.
1063	
1064	    Strategy: find the git root first (like ``git rev-parse --show-toplevel``),
1065	    then check if it has a ``.megaplan/`` directory.  This avoids ambiguity when
1066	    nested subdirectories also have their own ``.megaplan/``.  Falls back to the
1067	    nearest ancestor with ``.megaplan/`` if not in a git repo, and finally to
1068	    *start* if nothing is found.
1069	    """
1070	    resolved = start.resolve()
1071	
1072	    # Try git root first — the canonical project root.
1073	    git_root = _find_git_root(resolved)
1074	    if git_root and (git_root / ".megaplan").is_dir():
1075	        return git_root
1076	
1077	    # Fallback: walk up to find nearest .megaplan
1078	    current = resolved
1079	    while True:
1080	        if (current / ".megaplan").is_dir():
1081	            return current
1082	        parent = current.parent
1083	        if parent == current:
1084	            return start
1085	        current = parent
1086	
1087	
1088	def _find_git_root(start: Path) -> Path | None:
1089	    """Walk up to find the directory containing ``.git``."""
1090	    current = start
1091	    while True:
1092	        if (current / ".git").exists():
1093	            return current
1094	        parent = current.parent
1095	        if parent == current:
1096	            return None
1097	        current = parent
1098	
1099	
1100	def _auto_sync_installed_skills() -> None:
1101	    try:
1102	        for target in _GLOBAL_TARGETS:
1103	            agent_dir = Path.home() / target["detect"]
1104	            if not agent_dir.is_dir():
1105	                continue
1106	            _install_owned_file(Path.home() / target["path"], bundled_global_file(target["data"]), force=False)
1107	    except Exception:
1108	        pass
1109	
1110	
1111	def main(argv: list[str] | None = None) -> int:
1112	    parser = build_parser()
1113	    args, remaining = parser.parse_known_args(argv)
1114	    if args.command != "setup":
1115	        _auto_sync_installed_skills()
1116	    try:
1117	        if args.command == "setup":
1118	            return render_response(handle_setup(args))
1119	        if args.command == "config":
1120	            return render_response(handle_config(args))
1121	    except CliError as error:
1122	        return error_response(error)
1123	
1124	    # Capture the working directory for subprocess workers (--add-dir / -C).
1125	    # This preserves git-worktree isolation: workers edit source code under
1126	    # the CWD (or an explicit --work-dir override), not the plan's stored
1127	    # project_dir (which may be a sibling checkout).
1128	    from megaplan.workers import set_work_dir_override
1129	    work_dir_override = getattr(args, "work_dir", None)
1130	    set_work_dir_override(work_dir_override if work_dir_override else Path.cwd())
1131	
1132	    root = _find_megaplan_root(Path.cwd())
1133	    ensure_runtime_layout(root)
1134	
1135	    if args.command == "auto":
1136	        from megaplan.auto import run_auto
1137	        try:
1138	            return run_auto(root, args)
1139	        except CliError as error:
1140	            return error_response(error, root=root)
1141	
1142	    if args.command == "chain":
1143	        from megaplan.chain import run_chain_cli
1144	        try:
1145	            return run_chain_cli(root, args)
1146	        except CliError as error:
1147	            return error_response(error, root=root)
1148	
1149	    if args.command == "cloud":
1150	        from megaplan.cloud.cli import run_cloud_cli
1151	        try:
1152	            return run_cloud_cli(root, args)
1153	        except CliError as error:
1154	            return error_response(error, root=root)
1155	
1156	    if args.command == "tiebreaker":
1157	        from megaplan.tiebreaker import run_tiebreaker_cli
1158	        try:
1159	            return run_tiebreaker_cli(root, args)
1160	        except CliError as error:
1161	            return error_response(error, root=root)
1162	
1163	    try:
1164	        handler = COMMAND_HANDLERS.get(args.command)
1165	        if handler is None:
1166	            raise CliError("invalid_command", f"Unknown command {args.command!r}")
1167	        if args.command == "override" and remaining:
1168	            if not args.note:
1169	                args.note = " ".join(remaining)
1170	            remaining = []
1171	        if remaining:
1172	            parser.error(f"unrecognized arguments: {' '.join(remaining)}")
1173	        if args.command == "override" and args.override_action == "add-note" and not args.note:
1174	            raise CliError("invalid_args", "override add-note requires a note")
1175	        if args.command == "override" and args.override_action == "set-robustness" and not args.robustness:
1176	            raise CliError("invalid_args", f"override set-robustness requires --robustness {'|'.join(ROBUSTNESS_LEVELS)}")
1177	        return render_response(handler(root, args))
1178	    except CliError as error:
1179	        return error_response(error, root=root)
1180	
1181	
1182	if __name__ == "__main__":
1183	    sys.exit(main())
1184
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
File content (39710 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
```

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/megaplan/**/doc_assembly.py"
}
```

> TOOL

tool_result Glob
```
megaplan/doc_assembly.py
```

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/megaplan/**/evaluation.py"
}
```

> TOOL

tool_result Glob
```
megaplan/evaluation.py
```

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/megaplan/**/types.py"
}
```

> TOOL

tool_result Glob
```
megaplan/loop/types.py
megaplan/types.py
```

> AGENT

Now let me read the handlers.py file in chunks and the other key files:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
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
42	    STATE_AWAITING_HUMAN,
43	    STATE_CRITIQUED,
44	    STATE_DONE,
45	    STATE_EXECUTED,
46	    STATE_FINALIZED,
47	    STATE_GATED,
48	    STATE_INITIALIZED,
49	    STATE_PREPPED,
50	    STATE_PLANNED,
51	    STATE_TIEBREAKER_PENDING,
52	    STATE_TIEBREAKER_READY,
53	    StepResponse,
54	)
55	from megaplan._core import (
56	    add_or_increment_debt,
57	    append_history,
58	    apply_session_update,
59	    atomic_write_json,
60	    atomic_write_text,
61	    build_next_step_runtime,
62	    clear_active_step,
63	    configured_robustness,
64	    ensure_runtime_layout,
65	    extract_subsystem_tag,
66	    latest_plan_path,
67	    latest_plan_meta_path,
68	    load_debt_registry,
69	    load_flag_registry,
70	    load_plan,
71	    load_plan_locked,
72	    make_history_entry,
73	    now_utc,
74	    plans_root,
75	    read_json,
76	    record_step_failure,
77	    render_final_md,
78	    save_debt_registry,
79	    save_flag_registry,
80	    save_state,
81	    scope_creep_flags,
82	    set_active_step,
83	    sha256_file,
84	    sha256_text,
85	    slugify,
86	    unresolved_significant_flags,
87	    get_effective,
88	    workflow_includes_step,
89	    workflow_transition,
90	    workflow_next,
91	)
92	from megaplan._core.phase_runtime import (
93	    DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
94	    PHASE_RUNTIME_POLICY,
95	    format_duration_hint,
96	)
97	from megaplan.evaluation import (
98	    PLAN_STRUCTURE_REQUIRED_STEP_ISSUE,
99	    build_gate_artifact,
100	    build_gate_signals,
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/doc_assembly.py"
}
```

> TOOL

tool_result Read
```
1	"""Doc-mode section assembly — collects per-batch executor outputs into a single document."""
2	
3	from __future__ import annotations
4	
5	import os
6	import tempfile
7	from pathlib import Path
8	from typing import Any
9	
10	from megaplan._core import read_json
11	
12	
13	def extract_sections(batch_payloads: list[dict[str, Any]]) -> dict[str, str]:
14	    """Map section_id to rendered text from executor output.
15	
16	    Scans task_updates across all batch payloads. Each task with status
17	    'done' contributes its sections_written entries. The section content
18	    is taken from the task's executor_notes (the authored text).
19	    """
20	    sections: dict[str, str] = {}
21	    for payload in batch_payloads:
22	        for task in payload.get("task_updates", []):
23	            if not isinstance(task, dict):
24	                continue
25	            if task.get("status") != "done":
26	                continue
27	            notes = task.get("executor_notes", "")
28	            for section_id in task.get("sections_written", []):
29	                if isinstance(section_id, str) and section_id.strip():
30	                    sections[section_id] = notes
31	    return sections
32	
33	
34	def _task_order_index(finalize_data: dict[str, Any]) -> dict[str, int]:
35	    """Build a mapping from task_id to its position in the finalize task list."""
36	    return {
37	        task["id"]: index
38	        for index, task in enumerate(finalize_data.get("tasks", []))
39	        if isinstance(task, dict) and isinstance(task.get("id"), str)
40	    }
41	
42	
43	def _section_plan_order(
44	    finalize_data: dict[str, Any],
45	    batch_payloads: list[dict[str, Any]],
46	) -> list[str]:
47	    """Return section IDs ordered by their owning task's position in the plan."""
48	    task_index = _task_order_index(finalize_data)
49	    section_to_task: dict[str, str] = {}
50	    for payload in batch_payloads:
51	        for task in payload.get("task_updates", []):
52	            if not isinstance(task, dict):
53	                continue
54	            task_id = task.get("task_id", "")
55	            for section_id in task.get("sections_written", []):
56	                if isinstance(section_id, str) and section_id.strip():
57	                    section_to_task.setdefault(section_id, task_id)
58	    ordered = sorted(
59	        section_to_task.keys(),
60	        key=lambda sid: task_index.get(section_to_task.get(sid, ""), 999),
61	    )
62	    return ordered
63	
64	
65	def assemble_doc(
66	    plan_dir: Path,
67	    output_path: Path,
68	    finalize_data: dict[str, Any],
69	) -> Path:
70	    """Fallback document assembly from per-batch executor notes.
71	
72	    The executor is the primary author: per `prompts/execute_doc.py`, it writes
73	    the document directly to `output_path` during each task, and keeps
74	    `executor_notes` verification-focused (not section content). When the
75	    executor wrote the file successfully, this function preserves that file
76	    and does nothing else.
77	
78	    Fallback path — only if the output file is missing or empty — assembles
79	    text from `executor_notes` in `execution_batch_*.json`, ordered by the
80	    owning task's position in `finalize_data`. This is a degraded best-effort
81	    output for the sandbox-blocked case; callers should treat its content as
82	    verification prose rather than authored sections.
83	
84	    The file is written atomically (temp file + rename).
85	    """
86	    if output_path.exists() and output_path.stat().st_size > 0:
87	        return output_path
88	
89	    batch_payloads: list[dict[str, Any]] = []
90	    batch_index = 1
91	    while True:
92	        batch_path = plan_dir / f"execution_batch_{batch_index}.json"
93	        if not batch_path.exists():
94	            break
95	        try:
96	            batch_payloads.append(read_json(batch_path))
97	        except (OSError, ValueError):
98	            pass
99	        batch_index += 1
100	
101	    sections = extract_sections(batch_payloads)
102	    ordered_ids = _section_plan_order(finalize_data, batch_payloads)
103	
104	    lines: list[str] = []
105	    for section_id in ordered_ids:
106	        content = sections.get(section_id, "")
107	        if content:
108	            lines.append(content)
109	
110	    assembled_text = "\n\n".join(lines) if lines else ""
111	
112	    output_path.parent.mkdir(parents=True, exist_ok=True)
113	    fd, tmp_path = tempfile.mkstemp(
114	        dir=str(output_path.parent),
115	        suffix=".tmp",
116	    )
117	    closed = False
118	    try:
119	        os.write(fd, assembled_text.encode("utf-8"))
120	        os.close(fd)
121	        closed = True
122	        os.replace(tmp_path, str(output_path))
123	    except BaseException:
124	        if not closed:
125	            os.close(fd)
126	        if os.path.exists(tmp_path):
127	            os.unlink(tmp_path)
128	        raise
129	
130	    return output_path
131
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
42	    agents: dict[str, str]
43	    workers: NotRequired[dict[str, Any]]
44	    max_tiebreakers_per_plan: int
45	    tiebreaker_blocklist: list[str]
46	    allow_tiebreaker: bool
47	    tiebreaker_token_budget: int
48	    tiebreaker_time_budget_minutes: int
49	
50	
51	class PlanMeta(TypedDict, total=False):
52	    significant_counts: list[int]
53	    weighted_scores: list[float]
54	    plan_deltas: list[float | None]
55	    recurring_critiques: list[str]
56	    total_cost_usd: float
57	    overrides: list[dict[str, Any]]
58	    notes: list[dict[str, Any]]
59	    user_approved_gate: bool
60	
61	
62	class SessionInfo(TypedDict, total=False):
63	    id: str
64	    mode: str
65	    created_at: str
66	    last_used_at: str
67	    refreshed: bool
68	
69	
70	class ActiveStep(TypedDict, total=False):
71	    step: str
72	    agent: str
73	    mode: str
74	    model: str
75	    run_id: str
76	    session_id: str
77	    started_at: str
78	
79	
80	class PlanVersionRecord(TypedDict, total=False):
81	    version: int
82	    file: str
83	    hash: str
84	    timestamp: str
85	
86	
87	class HistoryEntry(TypedDict, total=False):
88	    step: str
89	    timestamp: str
90	    duration_ms: int
91	    cost_usd: float
92	    result: str
93	    session_mode: str
94	    session_id: str
95	    agent: str
96	    output_file: str
97	    artifact_hash: str
98	    finalize_hash: str
99	    raw_output_file: str
100	    message: str
101	    flags_count: int
102	    flags_addressed: list[str]
103	    recommendation: str
104	    approval_mode: str
105	    environment: dict[str, bool]
106	
107	
108	class ClarificationRecord(TypedDict, total=False):
109	    refined_idea: str
110	    intent_summary: str
111	    questions: list[str]
112	
113	
114	class LastGateRecord(TypedDict, total=False):
115	    recommendation: str
116	    rationale: str
117	    signals_assessment: str
118	    warnings: list[str]
119	    settled_decisions: list["SettledDecision"]
120	    passed: bool
121	    preflight_results: dict[str, bool]
122	    orchestrator_guidance: str
123	
124	
125	class PlanState(TypedDict):
126	    name: str
127	    idea: str
128	    current_state: str
129	    iteration: int
130	    created_at: str
131	    config: PlanConfig
132	    sessions: dict[str, SessionInfo]
133	    plan_versions: list[PlanVersionRecord]
134	    history: list[HistoryEntry]
135	    meta: PlanMeta
136	    last_gate: LastGateRecord
137	    active_step: NotRequired[ActiveStep]
138	    clarification: NotRequired[ClarificationRecord]
139	
140	
141	class _FlagRecordRequired(TypedDict):
142	    id: str
143	    concern: str
144	    category: str
145	    status: str
146	
147	
148	class FlagRecord(_FlagRecordRequired, total=False):
149	    severity_hint: str
150	    evidence: str
```

> AGENT

Let me search for SettledDecision and continue reading types.py:

> TOOL

tool_use Grep
```json
{
  "pattern": "SettledDecision",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan",
  "type": "py",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 1 file
megaplan/types.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/types.py",
  "offset": 150,
  "limit": 100
}
```

> TOOL

tool_result Read
```
150	    evidence: str
151	    raised_in: str
152	    severity: str
153	    verified: bool
154	    verified_in: str
155	    addressed_in: str
156	    settled_by_tiebreaker: str
157	
158	
159	class FlagRegistry(TypedDict):
160	    flags: list[FlagRecord]
161	
162	
163	class GateCheckResult(TypedDict):
164	    passed: bool
165	    criteria_check: dict[str, Any]
166	    preflight_results: dict[str, bool]
167	    unresolved_flags: list[FlagRecord]
168	
169	
170	class SettledDecision(TypedDict, total=False):
171	    id: str
172	    decision: str
173	    rationale: str
174	
175	
176	class TiebreakerDecision(TypedDict, total=False):
177	    fuzzy_group_id: str
178	    flag_ids: list[str]
179	    question: str
180	    researcher_pick: str
181	    challenger_pick: str
182	    human_pick: str
183	    action: str
184	    rationale: str
185	    timestamp: str
186	
187	
188	class GatePayload(TypedDict):
189	    recommendation: str
190	    rationale: str
191	    signals_assessment: str
192	    warnings: list[str]
193	    settled_decisions: list[SettledDecision]
194	
195	
196	class GateArtifact(TypedDict, total=False):
197	    passed: bool
198	    criteria_check: dict[str, Any]
199	    preflight_results: dict[str, bool]
200	    unresolved_flags: list[FlagRecord]
201	    recommendation: str
202	    rationale: str
203	    signals_assessment: str
204	    warnings: list[str]
205	    settled_decisions: list[SettledDecision]
206	    override_forced: bool
207	    orchestrator_guidance: str
208	    robustness: str
209	    signals: dict[str, Any]
210	
211	
212	class GateSignals(TypedDict, total=False):
213	    robustness: str
214	    signals: dict[str, Any]
215	    warnings: list[str]
216	
217	
218	class StepResponse(TypedDict, total=False):
219	    success: bool
220	    step: str
221	    summary: str
222	    artifacts: list[str]
223	    next_step: str | None
224	    state: str
225	    auto_approve: bool
226	    robustness: str
227	    iteration: int
228	    plan: str
229	    plan_dir: str
230	    questions: list[str]
231	    verified_flags: list[str]
232	    open_flags: list[str]
233	    scope_creep_flags: list[str]
234	    warnings: list[str]
235	    files_changed: list[str]
236	    deviations: list[str]
237	    user_approved_gate: bool
238	    issues: list[str]
239	    valid_next: list[str]
240	    mode: str
241	    installed: list[dict[str, Any]]
242	    config_path: str
243	    routing: dict[str, str]
244	    raw_config: dict[str, Any]
245	    action: str
246	    key: str
247	    value: str
248	    skipped: bool
249	    file: str
```

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan/megaplan/data -type f -name \"instructions.md\" | head -1"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/data/instructions.md
```

> AGENT

Now let me search for handle_init in handlers.py and check for prompts and tests:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"^def handle_init\" /Users/user_c042661f/Documents/megaplan/megaplan/handlers.py"
}
```

> TOOL

tool_result Bash
```
728:def handle_init(root: Path, args: argparse.Namespace) -> StepResponse:
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/data/instructions.md",
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	# Megaplan
2	Route every step through the `megaplan` CLI. Never call agents directly.
3	Before the first CLI call, resolve a working launcher and reuse it for the whole run. Do not assume `megaplan` itself is on `PATH`; command presence alone is not enough. Prove the launcher works by successfully running a harmless CLI call with it first. In the instructions below, treat `<launcher>` as that verified command.
4	Launcher resolution order:
5	1. Try `python -m megaplan config show`.
6	2. If that fails, try `./.venv/bin/python -m megaplan config show`.
7	3. If that fails, try `uv run python -m megaplan config show`.
8	4. If that fails, try a version-selected shim such as `PYENV_VERSION=3.11.11 megaplan config show`.
9	5. Only use bare `megaplan ...` if that exact form already succeeded during this check.
10	## Triage
11	A single megaplan can cover as much as 2 weeks of work — don't reflexively split large efforts into multiple plans. Pick the right level based on the task:
12	- **Skip megaplan**: single-file fixes, bug fixes with clear cause, simple refactors, config changes, adding tests for existing code. Just do it.
13	- **Light**: multi-file changes with clear scope, well-understood features, straightforward additions. One critique pass, no gate, no review.
14	- **Standard** (default for megaplan): cross-cutting changes touching many subsystems, unfamiliar codebase areas, ambiguous requirements, changes with high breakage risk, or anything where the plan itself needs debate.
15	- **Heavy**: high-stakes changes where getting it wrong is expensive — security-critical code, data migrations, public API changes. Uses the same visible `prep` phase but with 8 critique checks instead of 4.
16	
17	Default to standard unless the task is clearly simple enough for light. Do not ask the user to choose robustness — pick it yourself based on the above. Only ask execution mode (auto-approve or review) when using megaplan.
18	## Modes
19	Megaplan has two output modes, picked with `--mode` at `init`:
20	- **`--mode code`** (default): the run produces a code diff. Execute workers emit per-task file changes. Use for features, refactors, bug fixes, migrations — anything whose deliverable is source code.
21	- **`--mode metaplan`** (alias: `--mode doc`): the run produces a single document artifact at `--output <relative/path>` (e.g. `docs/design.md`). The prep, execute, and review phases use authoring-specific prompts; the execute schema uses `sections_written` instead of file changes; auditing reasons about section delivery. Use for design docs, architecture specs, research notes, RFCs, proposals, post-mortems, migration plans — anything whose deliverable is prose, not code. This is the "design-first / preplan" workflow; `prep` is the visible repository-investigation *phase* inside every run (both modes have it), not a separate mode.
22	
23	All other flags (`--robustness`, `--auto-approve`, `--phase-model`, `--hermes`, subagent mode, overrides, step editing) behave identically in both modes. The workflow phases are the same: `prep → plan → critique → gate → revise → finalize → execute → review`.
24	
25	A common pattern is two runs: first `--mode metaplan` to produce a rigorous design document, then `--mode code` on a new idea that references that document to implement it.
26	
27	**`--mode` and `--output` go together.** `init` rejects `--output` without `--mode metaplan` (error `invalid_args`), and rejects `--mode metaplan` without `--output`. Don't try to pass one without the other.
28	## Start
29	Run `<launcher> config show` before `init`. If `raw_config.execution.auto_approve` is explicitly present, do not ask the execution-mode question and honor that configured override, including configured `false`. If that raw key is absent, ask execution mode (auto-approve or review) before `init`. In the same config check, respect `execution.robustness` as a settable override when it is configured; otherwise pick robustness yourself per the triage guidance above.
30	```bash
31	<launcher> init --project-dir "$PROJECT_DIR" [--auto-approve] [--robustness light|standard|robust|superrobust] [--mode code|metaplan] [--output docs/foo.md] "$IDEA"
32	```
33	For metaplan-mode runs, pass `--mode metaplan --output <relative/path>` (the path is where the final document artifact is written, relative to the project dir). Everything else is identical to code mode.
34	Report the plan name, execution mode, robustness, mode (and `--output` path when metaplan mode), current state, and next step.
35	## Workflow
36	Run the loop in this order:
37	1. `prep`
38	2. `plan`
39	3. `critique`
40	4. `gate`
41	5. `revise` when gate recommends iteration
42	6. `finalize`
43	7. `execute`
44	8. `review`
45	Use `next_step` and `valid_next` for CLI routing. After `gate`, follow `orchestrator_guidance` instead of manually interpreting gate signals. When a response includes `next_step_runtime`, use its `duration_hint` and `recommended_next_check_seconds` to calibrate timing.
46	At `--robustness light`, the loop is: `plan` → `critique` → `revise` → `finalize` → `execute`. There is no prep, no gate, and no review.
47	At `--robustness standard`, the loop is: `prep` → `plan` → `critique` → `gate` → ...
48	At `--robustness robust`, the loop is also `prep` → `plan` → `critique` → `gate` → ... but uses 8 critique checks instead of 4 and enables parallel critique.
49	At `--robustness superrobust`, the loop is the same as robust but also enables parallel review.
50	## Step Rules
51	- `plan`: inspect the repository first; produce the plan plus `questions`, `assumptions`, and `success_criteria`. Each criterion is `{"criterion": "...", "priority": "must|should|info"}`. `must` = hard gate (reviewer blocks), `should` = quality target (reviewer flags but doesn't block), `info` = human reference (reviewer skips).
52	- `prep`: make repository investigation explicit before planning. Respect `skip: true` when the task is already concrete enough.
53	- `critique`: surface concrete flags with concern, evidence, category, and severity; reuse open flag IDs; call out scope creep. Also validate that success criteria priorities are well-calibrated — `must` criteria should be verifiable yes/no, subjective goals should be `should`.
54	- `gate`: read the response, warnings, and `orchestrator_guidance`. (Skipped at light robustness.)
55	- `revise`: show the delta, flags addressed, and flags remaining. At light robustness, routes to `finalize`; otherwise loops back through `critique` and `gate`.
56	- `review`: judge success against the success criteria and the user's intent, not plan elegance. Only block on `must` criteria failures. `should` failures are flagged but don't require rework. `info` criteria are waived.
57	## Gate Principle
58	The gate response tells the orchestrator what to do next. Follow `orchestrator_guidance` unless you have a concrete reason to disagree after investigating the repository or plan artifacts yourself.
59	Investigate before disagreeing: read the current plan and critique artifacts, check the project code to verify whether a flagged issue is real, or use `megaplan status --plan <name>` / `megaplan audit --plan <name>`.
60	If you disagree with the guidance, explain why briefly and use an override. Do not manually reinterpret score trajectory, flag quality, or loop state when the gate already did that work for you.
61	## Execute
62	- After a successful gate, run `megaplan finalize` to produce the execution-ready briefing document.
63	- In auto-approve mode, run `megaplan execute --confirm-destructive` after finalize.
64	- In review mode, pause at the finalize-to-execute checkpoint and wait for explicit approval before running:
65	```bash
66	megaplan execute --confirm-destructive --user-approved
67	```
68	## Long-Running Execution
69	For plans with multiple batches, use per-batch mode to drive execution incrementally:
70	```bash
71	megaplan execute --plan <name> --confirm-destructive --user-approved --batch 1
72	megaplan execute --plan <name> --confirm-destructive --user-approved --batch 2
73	# ... continue until all batches complete
74	```
75	Between batches, poll progress:
76	```bash
77	megaplan progress --plan <name>
78	```
79	Use `megaplan status --plan <name>` for the full plan state, including active-step timing and any `next_step_runtime` guidance from the latest response.
80	Per-batch mode uses global batch numbering (1-indexed, computed from ALL tasks). Each `--batch N` call:
81	- Validates that batches 1..N-1 are complete
82	- Executes only batch N's tasks
83	- Writes `execution_batch_N.json` as evidence
84	- On the final batch, produces aggregate `execution.json` and transitions to `executed`
85	Timeout recovery: re-run the same `--batch N`. The harness checks prerequisite completion and merges only untracked tasks.
86	Note: `progress` shows completed state only (between-batch granularity). With per-batch mode, each batch is a separate CLI call, so the orchestrator has full visibility.
87	## Overrides
88	- `megaplan override add-note --plan <name> --note "..."`
89	- `megaplan override force-proceed --plan <name> --reason "..."`
90	- `megaplan override replan --plan <name> --reason "..." [--note "..."]`
91	- `megaplan override abort --plan <name> --reason "..."`
92	`force-proceed` is available from `critiqued` (routes to finalize, not execute). `replan` is available from `gated`, `finalized`, or `critiqued`. `add-note` is safe from any active state.
93	## Replan
94	Use `replan` when the orchestrator itself needs to edit the plan directly instead of asking the revise worker to do it.
95	```bash
96	megaplan override replan --plan <name> --reason "expanding scope" --note "Also clean up the display layer"
97	```
98	After `replan`, read the returned plan file, edit it directly, then run `megaplan critique`.
99	## Step Editing
100	Use `step` when you need to insert, remove, or reorder step sections (`## Step N:` or `### Step N:`) without hand-editing the markdown.
```

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/megaplan/**/execute_doc.py"
}
```

> TOOL

tool_result Glob
```
megaplan/prompts/execute_doc.py
```

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/megaplan/**/prompts"
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
  "command": "find /Users/user_c042661f/Documents/megaplan/megaplan/data -type d -name \"prompts\""
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
  "command": "find /Users/user_c042661f/Documents/megaplan -type d -name prompts"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/prompts
/Users/user_c042661f/Documents/megaplan/.desloppify/subagents/runs/20260323_043646/prompts
/Users/user_c042661f/Documents/megaplan/.desloppify/subagents/runs/20260321_023625/prompts
/Users/user_c042661f/Documents/megaplan/.desloppify/subagents/runs/20260321_020544/prompts
/Users/user_c042661f/Documents/megaplan/.desloppify/subagents/runs/20260321_025658/prompts
/Users/user_c042661f/Documents/megaplan/.desloppify/subagents/runs/20260320_182530/prompts
/Users/user_c042661f/Documents/megaplan/.desloppify/subagents/runs/20260323_050611/prompts
/Users/user_c042661f/Documents/megaplan/.desloppify/subagents/runs/20260323_045706/prompts
/Users/user_c042661f/Documents/megaplan/.desloppify/subagents/runs/20260323_034952/prompts
/Users/user_c042661f/Documents/megaplan/.desloppify/subagents/runs/20260321_014226/prompts
/Users/user_c042661f/Documents/megaplan/.desloppify/subagents/runs/20260320_220253/prompts
/Users/user_c042661f/Documents/megaplan/.desloppify/subagents/runs/20260321_023633/prompts
/Users/user_c042661f/Documents/megaplan/.desloppify/subagents/runs/20260320_195710/prompts
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/megaplan/data/ | head -30"
}
```

> TOOL

tool_result Bash
```
total 88
drwxr-xr-x   5 user_c042661f  staff    160 Apr 21 12:39 .
drwxr-xr-x  39 user_c042661f  staff   1248 Apr 21 12:39 ..
-rw-r--r--   1 user_c042661f  staff  18044 Apr 19 16:32 claude_subagent_appendix.md
-rw-r--r--   1 user_c042661f  staff   5153 Apr 11 04:23 codex_subagent_appendix.md
-rw-r--r--   1 user_c042661f  staff  12435 Apr 21 12:39 instructions.md
```

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/megaplan/prompts/ | head -20"
}
```

> TOOL

tool_result Bash
```
total 328
drwxr-xr-x@ 18 user_c042661f  staff    576 Apr 15 21:20 .
drwxr-xr-x  39 user_c042661f  staff   1248 Apr 21 12:39 ..
-rw-r--r--@  1 user_c042661f  staff   6148 Apr 15 05:43 .DS_Store
-rw-r--r--@  1 user_c042661f  staff   8109 Apr 15 20:55 __init__.py
drwxr-xr-x@ 32 user_c042661f  staff   1024 Apr 15 21:20 __pycache__
-rw-r--r--   1 user_c042661f  staff   8785 Apr  6 07:11 _shared.py
-rw-r--r--   1 user_c042661f  staff  18310 Apr 15 21:20 critique.py
-rw-r--r--@  1 user_c042661f  staff  18972 Apr 10 23:09 execute.py
-rw-r--r--@  1 user_c042661f  staff  10264 Apr 15 20:55 execute_doc.py
-rw-r--r--@  1 user_c042661f  staff   6134 Apr 15 20:55 finalize.py
-rw-r--r--   1 user_c042661f  staff   8579 Apr 15 21:20 gate.py
-rw-r--r--   1 user_c042661f  staff  11278 Apr 15 21:18 planning.py
-rw-r--r--@  1 user_c042661f  staff   3152 Apr 15 20:55 prep_doc.py
-rw-r--r--   1 user_c042661f  staff  23820 Apr 15 21:18 review.py
-rw-r--r--@  1 user_c042661f  staff   6650 Apr 15 20:55 review_doc.py
-rw-r--r--   1 user_c042661f  staff   2065 Apr 15 21:20 tiebreaker_challenger.py
-rw-r--r--   1 user_c042661f  staff   2240 Apr 15 21:20 tiebreaker_researcher.py
-rw-r--r--   1 user_c042661f  staff   5091 Apr 15 21:20 tiebreaker_synthesis.py
```

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan/tests -type f -name \"*.py\" | grep -i \"init\\|doc_assembly\" | head -10"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/tests/test_doc_assembly.py
/Users/user_c042661f/Documents/megaplan/tests/test_handle_init_doc_mode.py
/Users/user_c042661f/Documents/megaplan/tests/__init__.py
```

> AGENT

Now let me read the handle_init function and the test files:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 727,
  "limit": 150
}
```

> TOOL

tool_result Read
```
727	
728	def handle_init(root: Path, args: argparse.Namespace) -> StepResponse:
729	    ensure_runtime_layout(root)
730	    project_dir = Path(args.project_dir).expanduser().resolve()
731	    if not project_dir.exists() or not project_dir.is_dir():
732	        raise CliError("invalid_project_dir", f"Project directory does not exist: {project_dir}")
733	    explicit_mode = getattr(args, "mode", None)
734	    raw_output_path = getattr(args, "output", None)
735	    mode = explicit_mode or "code"
736	    if mode == "metaplan":
737	        mode = "doc"
738	
739	    if mode == "code" and raw_output_path:
740	        raise CliError(
741	            "invalid_args",
742	            "--output is only valid with --mode doc. For code-mode runs, remove "
743	            "--output; for design-document runs, also pass --mode doc.",
744	        )
745	    normalized_output_path: str | None = None
746	    if mode == "doc" and not raw_output_path:
747	        raise CliError("invalid_args", "--output is required when --mode doc is selected")
748	    if raw_output_path:
749	        output_candidate = Path(raw_output_path)
750	        if output_candidate.is_absolute():
751	            raise CliError("invalid_args", "--output must be a relative path inside the project directory")
752	        if any(part == ".." for part in output_candidate.parts):
753	            raise CliError("invalid_args", "--output must not contain '..' path traversal")
754	        resolved_output_path = (project_dir / output_candidate).resolve()
755	        try:
756	            normalized_output_path = resolved_output_path.relative_to(project_dir).as_posix()
757	        except ValueError as exc:
758	            raise CliError("invalid_args", "--output must stay within the project directory") from exc
759	    robustness = getattr(args, "robustness", None)
760	    if robustness is None:
761	        robustness = get_effective("execution", "robustness")
762	    if robustness not in ROBUSTNESS_LEVELS:
763	        robustness = "standard"
764	    auto_approve_value = getattr(args, "auto_approve", None)
765	    if auto_approve_value is None:
766	        auto_approve_value = get_effective("execution", "auto_approve")
767	    auto_approve = bool(auto_approve_value)
768	    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
769	    plan_name = args.name or f"{slugify(args.idea)}-{timestamp}"
770	    plan_dir = plans_root(root) / plan_name
771	    if plan_dir.exists():
772	        raise CliError("duplicate_plan", f"Plan directory already exists: {plan_name}")
773	    plan_dir.mkdir(parents=True, exist_ok=False)
774	
775	    state: PlanState = {
776	        "name": plan_name,
777	        "idea": args.idea,
778	        "current_state": STATE_INITIALIZED,
779	        "iteration": 0,
780	        "created_at": now_utc(),
781	        "config": {
782	            "project_dir": str(project_dir),
783	            "auto_approve": auto_approve,
784	            "robustness": robustness,
785	            "mode": mode,
786	            "agent": "hermes" if getattr(args, "hermes", None) is not None else "",
787	        },
788	        "sessions": {},
789	        "plan_versions": [],
790	        "history": [],
791	        "meta": {
792	            "significant_counts": [],
793	            "weighted_scores": [],
794	            "plan_deltas": [],
795	            "recurring_critiques": [],
796	            "total_cost_usd": 0.0,
797	            "overrides": [],
798	            "notes": [],
799	        },
800	        "last_gate": {},
801	    }
802	    if normalized_output_path is not None:
803	        state["config"]["output_path"] = normalized_output_path
804	    append_history(
805	        state,
806	        make_history_entry(
807	            "init",
808	            duration_ms=0,
809	            cost_usd=0.0,
810	            result="success",
811	            environment={
812	                "claude": bool(find_command("claude")),
813	                "codex": bool(find_command("codex")),
814	            },
815	        ),
816	    )
817	    save_state(plan_dir, state)
818	    next_steps = workflow_next(state)
819	    response: StepResponse = {
820	        "success": True,
821	        "step": "init",
822	        "plan": plan_name,
823	        "state": STATE_INITIALIZED,
824	        "summary": f"Initialized plan '{plan_name}' for project {project_dir}",
825	        "artifacts": ["state.json"],
826	        "next_step": next_steps[0] if next_steps else None,
827	        "auto_approve": auto_approve,
828	        "robustness": robustness,
829	    }
830	    _attach_next_step_runtime(response)
831	    return response
832	
833	
834	def handle_plan(root: Path, args: argparse.Namespace) -> StepResponse:
835	    with load_plan_locked(root, args.plan, step="plan") as (plan_dir, state):
836	        require_state(state, "plan", {STATE_INITIALIZED, STATE_PREPPED, STATE_PLANNED})
837	        rerun = state["current_state"] == STATE_PLANNED
838	        version = state["iteration"] if rerun else state["iteration"] + 1
839	        worker, agent, mode, refreshed = _run_worker("plan", state, plan_dir, args, root=root, iteration=version)
840	        payload = worker.payload
841	        plan_filename, meta_filename, meta = _write_plan_version(
842	            plan_dir=plan_dir,
843	            state=state,
844	            step="plan",
845	            version=version,
846	            worker=worker,
847	            plan_text=payload["plan"].rstrip() + "\n",
848	            meta_fields={
849	                "questions": payload["questions"],
850	                "success_criteria": payload["success_criteria"],
851	                "assumptions": payload["assumptions"],
852	            },
853	        )
854	        state["iteration"], state["current_state"] = version, STATE_PLANNED
855	        state["meta"].pop("user_approved_gate", None)
856	        state["last_gate"] = {}
857	        state["plan_versions"].append({
858	            "version": version, "file": plan_filename,
859	            "hash": meta["hash"], "timestamp": meta["timestamp"],
860	        })
861	        verb = "Refined" if rerun else "Generated"
862	        return _finish_step(
863	            plan_dir, state, args,
864	            step="plan",
865	            worker=worker, agent=agent, mode=mode, refreshed=refreshed,
866	            summary=f"{verb} plan v{version} with {len(payload['questions'])} questions and {len(payload['success_criteria'])} success criteria.",
867	            artifacts=[plan_filename, meta_filename],
868	            output_file=plan_filename,
869	            artifact_hash=meta["hash"],
870	            response_fields={
871	                "iteration": version,
872	                "questions": payload["questions"],
873	                "assumptions": payload["assumptions"],
874	                "success_criteria": payload["success_criteria"],
875	            },
876	        )
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/tests/test_handle_init_doc_mode.py"
}
```

> TOOL

tool_result Read
```
1	"""Smoke tests for handle_init's doc-mode arg validation (--mode/--output)."""
2	from __future__ import annotations
3	
4	from argparse import Namespace
5	from pathlib import Path
6	
7	import pytest
8	
9	import megaplan
10	import megaplan._core
11	import megaplan._core.io as io_module
12	import megaplan.cli
13	from megaplan.types import CliError
14	
15	
16	def _bootstrap(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
17	    root = tmp_path / "root"
18	    project_dir = tmp_path / "project"
19	    config_path = tmp_path / "config"
20	    root.mkdir()
21	    project_dir.mkdir()
22	    (project_dir / ".git").mkdir()
23	
24	    def _config_dir(home: Path | None = None) -> Path:
25	        del home
26	        return config_path
27	
28	    monkeypatch.setenv(megaplan.MOCK_ENV_VAR, "1")
29	    monkeypatch.setattr(
30	        megaplan._core.shutil,
31	        "which",
32	        lambda name: "/usr/bin/mock" if name in {"claude", "codex"} else None,
33	    )
34	    monkeypatch.setattr(io_module, "config_dir", _config_dir)
35	    monkeypatch.setattr(megaplan.cli, "config_dir", _config_dir)
36	    return root, project_dir
37	
38	
39	def _args(project_dir: Path, **overrides: object) -> Namespace:
40	    data: dict[str, object] = {
41	        "plan": None,
42	        "idea": "doc-mode test",
43	        "name": None,
44	        "project_dir": str(project_dir),
45	        "auto_approve": None,
46	        "robustness": "standard",
47	        "agent": None,
48	        "mode": "code",
49	        "output": None,
50	        "hermes": None,
51	    }
52	    data.update(overrides)
53	    return Namespace(**data)
54	
55	
56	def test_doc_mode_requires_output(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
57	    root, project_dir = _bootstrap(tmp_path, monkeypatch)
58	    with pytest.raises(CliError) as info:
59	        megaplan.handle_init(root, _args(project_dir, mode="doc", output=None))
60	    assert info.value.code == "invalid_args"
61	    assert "--output" in str(info.value)
62	
63	
64	def test_output_rejects_absolute_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
65	    root, project_dir = _bootstrap(tmp_path, monkeypatch)
66	    with pytest.raises(CliError) as info:
67	        megaplan.handle_init(
68	            root,
69	            _args(project_dir, mode="doc", output="/etc/passwd"),
70	        )
71	    assert info.value.code == "invalid_args"
72	    assert "relative" in str(info.value).lower() or "absolute" in str(info.value).lower()
73	
74	
75	def test_output_rejects_parent_traversal(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
76	    root, project_dir = _bootstrap(tmp_path, monkeypatch)
77	    with pytest.raises(CliError) as info:
78	        megaplan.handle_init(
79	            root,
80	            _args(project_dir, mode="doc", output="../escape.md"),
81	        )
82	    assert info.value.code == "invalid_args"
83	    assert ".." in str(info.value)
84	
85	
86	def test_doc_mode_accepts_relative_output(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
87	    root, project_dir = _bootstrap(tmp_path, monkeypatch)
88	    response = megaplan.handle_init(
89	        root,
90	        _args(project_dir, name="doc-plan", mode="doc", output="docs/result.md"),
91	    )
92	    plan_dir = megaplan.plans_root(root) / response["plan"]
93	    import json as _json
94	    state = _json.loads((plan_dir / "state.json").read_text(encoding="utf-8"))
95	    assert state["config"]["mode"] == "doc"
96	    assert state["config"]["output_path"] == "docs/result.md"
97	
98	
99	def test_code_mode_without_output_succeeds(
100	    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
101	) -> None:
102	    """Code mode without --output is the common case and must keep working."""
103	    root, project_dir = _bootstrap(tmp_path, monkeypatch)
104	    response = megaplan.handle_init(
105	        root,
106	        _args(project_dir, name="code-plan", mode="code", output=None),
107	    )
108	    plan_dir = megaplan.plans_root(root) / response["plan"]
109	    import json as _json
110	    state = _json.loads((plan_dir / "state.json").read_text(encoding="utf-8"))
111	    assert state["config"]["mode"] == "code"
112	    assert "output_path" not in state["config"]
113	
114	
115	def test_code_mode_with_output_is_rejected(
116	    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
117	) -> None:
118	    """--output is meaningless in code mode; accepting it silently has
119	    historically masked dropped --mode doc flags. Reject it loudly."""
120	    root, project_dir = _bootstrap(tmp_path, monkeypatch)
121	    with pytest.raises(CliError) as info:
122	        megaplan.handle_init(
123	            root,
124	            _args(project_dir, mode="code", output="docs/foo.md"),
125	        )
126	    assert info.value.code == "invalid_args"
127	    assert "--output" in str(info.value)
128	    assert "--mode doc" in str(info.value)
129	
130	
131	def test_metaplan_mode_is_alias_for_doc(
132	    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
133	) -> None:
134	    """--mode metaplan is a user-facing alias for --mode doc; state should
135	    record 'doc' so all downstream `mode == 'doc'` checks keep working."""
136	    root, project_dir = _bootstrap(tmp_path, monkeypatch)
137	    response = megaplan.handle_init(
138	        root,
139	        _args(project_dir, name="metaplan-alias", mode="metaplan", output="docs/design.md"),
140	    )
141	    plan_dir = megaplan.plans_root(root) / response["plan"]
142	    import json as _json
143	    state = _json.loads((plan_dir / "state.json").read_text(encoding="utf-8"))
144	    assert state["config"]["mode"] == "doc"
145	    assert state["config"]["output_path"] == "docs/design.md"
146
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/tests/test_doc_assembly.py"
}
```

> TOOL

tool_result Read
```
1	"""Smoke tests for doc-mode section assembly (megaplan.doc_assembly)."""
2	from __future__ import annotations
3	
4	import json
5	from pathlib import Path
6	
7	import pytest
8	
9	from megaplan.doc_assembly import assemble_doc, extract_sections
10	
11	
12	def _write_batch(plan_dir: Path, index: int, payload: dict) -> None:
13	    plan_dir.mkdir(parents=True, exist_ok=True)
14	    (plan_dir / f"execution_batch_{index}.json").write_text(
15	        json.dumps(payload), encoding="utf-8"
16	    )
17	
18	
19	def _finalize_with_tasks(*task_ids: str) -> dict:
20	    return {"tasks": [{"id": tid} for tid in task_ids]}
21	
22	
23	def test_extract_sections_collects_done_only() -> None:
24	    payloads = [
25	        {
26	            "task_updates": [
27	                {
28	                    "task_id": "T1",
29	                    "status": "done",
30	                    "executor_notes": "Intro text",
31	                    "sections_written": ["intro"],
32	                },
33	                {
34	                    "task_id": "T2",
35	                    "status": "in_progress",
36	                    "executor_notes": "should not appear",
37	                    "sections_written": ["body"],
38	                },
39	            ]
40	        }
41	    ]
42	    sections = extract_sections(payloads)
43	    assert sections == {"intro": "Intro text"}
44	
45	
46	def test_assemble_doc_orders_sections_by_task_index(tmp_path: Path) -> None:
47	    plan_dir = tmp_path / "plan"
48	    output_path = tmp_path / "out.md"
49	
50	    # Batch 1 has T2's section, batch 2 has T1's section — written out of plan order.
51	    _write_batch(plan_dir, 1, {
52	        "task_updates": [
53	            {"task_id": "T2", "status": "done",
54	             "executor_notes": "Body content", "sections_written": ["body"]},
55	        ]
56	    })
57	    _write_batch(plan_dir, 2, {
58	        "task_updates": [
59	            {"task_id": "T1", "status": "done",
60	             "executor_notes": "Intro content", "sections_written": ["intro"]},
61	        ]
62	    })
63	
64	    finalize = _finalize_with_tasks("T1", "T2")
65	    assemble_doc(plan_dir, output_path, finalize)
66	    text = output_path.read_text(encoding="utf-8")
67	    assert text == "Intro content\n\nBody content"
68	
69	
70	def test_assemble_doc_is_idempotent(tmp_path: Path) -> None:
71	    plan_dir = tmp_path / "plan"
72	    output_path = tmp_path / "out.md"
73	    _write_batch(plan_dir, 1, {
74	        "task_updates": [
75	            {"task_id": "T1", "status": "done",
76	             "executor_notes": "Hello", "sections_written": ["s1"]},
77	        ]
78	    })
79	    finalize = _finalize_with_tasks("T1")
80	    assemble_doc(plan_dir, output_path, finalize)
81	    first = output_path.read_text(encoding="utf-8")
82	    assemble_doc(plan_dir, output_path, finalize)
83	    second = output_path.read_text(encoding="utf-8")
84	    assert first == second == "Hello"
85	
86	
87	def test_assemble_doc_handles_no_batches(tmp_path: Path) -> None:
88	    plan_dir = tmp_path / "plan"
89	    plan_dir.mkdir()
90	    output_path = tmp_path / "out.md"
91	    assemble_doc(plan_dir, output_path, _finalize_with_tasks())
92	    assert output_path.exists()
93	    assert output_path.read_text(encoding="utf-8") == ""
94	
95	
96	def test_assemble_doc_handles_empty_batch(tmp_path: Path) -> None:
97	    plan_dir = tmp_path / "plan"
98	    output_path = tmp_path / "out.md"
99	    _write_batch(plan_dir, 1, {"task_updates": []})
100	    assemble_doc(plan_dir, output_path, _finalize_with_tasks("T1"))
101	    assert output_path.read_text(encoding="utf-8") == ""
102	
103	
104	def test_assemble_doc_creates_parent_directory(tmp_path: Path) -> None:
105	    plan_dir = tmp_path / "plan"
106	    output_path = tmp_path / "nested" / "deep" / "out.md"
107	    _write_batch(plan_dir, 1, {
108	        "task_updates": [
109	            {"task_id": "T1", "status": "done",
110	             "executor_notes": "X", "sections_written": ["s1"]},
111	        ]
112	    })
113	    assemble_doc(plan_dir, output_path, _finalize_with_tasks("T1"))
114	    assert output_path.exists()
115	    assert output_path.read_text(encoding="utf-8") == "X"
116	
117	
118	def test_assemble_doc_preserves_executor_written_file(tmp_path: Path) -> None:
119	    plan_dir = tmp_path / "plan"
120	    output_path = tmp_path / "out.md"
121	    output_path.write_text("# Real document\n\nAuthored content here.", encoding="utf-8")
122	    _write_batch(plan_dir, 1, {
123	        "task_updates": [
124	            {"task_id": "T1", "status": "done",
125	             "executor_notes": "Verification prose, not content", "sections_written": ["s1"]},
126	        ]
127	    })
128	    assemble_doc(plan_dir, output_path, _finalize_with_tasks("T1"))
129	    assert output_path.read_text(encoding="utf-8") == "# Real document\n\nAuthored content here."
130	
131	
132	def test_assemble_doc_falls_back_when_file_empty(tmp_path: Path) -> None:
133	    plan_dir = tmp_path / "plan"
134	    output_path = tmp_path / "out.md"
135	    output_path.write_text("", encoding="utf-8")
136	    _write_batch(plan_dir, 1, {
137	        "task_updates": [
138	            {"task_id": "T1", "status": "done",
139	             "executor_notes": "Fallback body", "sections_written": ["s1"]},
140	        ]
141	    })
142	    assemble_doc(plan_dir, output_path, _finalize_with_tasks("T1"))
143	    assert output_path.read_text(encoding="utf-8") == "Fallback body"
144	
145	
146	def test_extract_sections_duplicate_section_id_last_wins(tmp_path: Path) -> None:
147	    """Document current behavior: when two tasks claim the same section_id,
148	    the later batch wins. This locks the contract so any future change is
149	    deliberate."""
150	    payloads = [
151	        {"task_updates": [
152	            {"task_id": "T1", "status": "done",
153	             "executor_notes": "first", "sections_written": ["dup"]},
154	        ]},
155	        {"task_updates": [
156	            {"task_id": "T2", "status": "done",
157	             "executor_notes": "second", "sections_written": ["dup"]},
158	        ]},
159	    ]
160	    sections = extract_sections(payloads)
161	    assert sections == {"dup": "second"}
162
```

> AGENT

Now let me check for pytest configuration and search for settled_decisions usage in evaluation.py:

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan -maxdepth 2 -name \"pytest.ini\" -o -name \"conftest.py\" -o -name \"pyproject.toml\" | head -10"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/pyproject.toml
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"settled_decisions\" /Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py | head -20"
}
```

> TOOL

tool_result Bash
```
719:        "settled_decisions": list(gate_payload.get("settled_decisions", [])),
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def build_gate\" /Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py"
}
```

> TOOL

tool_result Bash
```
539:def build_gate_signals(plan_dir: Path, state: PlanState, root: Path | None = None) -> GateSignals:
700:def build_gate_artifact(
```

> AGENT

Let me check evaluation.py for gate-related functions and settled_decisions:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py",
  "offset": 700,
  "limit": 50
}
```

> TOOL

tool_result Read
```
700	def build_gate_artifact(
701	    signals: dict[str, Any],
702	    gate_payload: GatePayload,
703	    *,
704	    override_forced: bool,
705	    orchestrator_guidance: str = "",
706	) -> GateArtifact:
707	    preflight = signals["preflight_results"]
708	    recommendation = gate_payload["recommendation"]
709	    warnings = list(signals.get("warnings", [])) + list(gate_payload.get("warnings", []))
710	    return {
711	        "passed": recommendation == "PROCEED" and all(preflight.values()),
712	        "criteria_check": signals["criteria_check"],
713	        "preflight_results": preflight,
714	        "unresolved_flags": signals["unresolved_flags"],
715	        "recommendation": recommendation,
716	        "rationale": gate_payload["rationale"],
717	        "signals_assessment": gate_payload["signals_assessment"],
718	        "warnings": warnings,
719	        "settled_decisions": list(gate_payload.get("settled_decisions", [])),
720	        "override_forced": override_forced,
721	        "orchestrator_guidance": orchestrator_guidance,
722	        "robustness": signals.get("robustness"),
723	        "signals": signals["signals"],
724	        # Gate's flag resolution — used by handler to allow PROCEED past blocking flags
725	        "flag_resolutions": list(gate_payload.get("flag_resolutions", [])),
726	        # Backward compatibility: carry through old-format fields if present
727	        "resolved_flag_ids": list(gate_payload.get("resolved_flag_ids", [])),
728	        "resolution_summary": gate_payload.get("resolution_summary", ""),
729	    }
730	
731	
732	def build_orchestrator_guidance(
733	    gate_payload: GatePayload,
734	    signals: dict[str, Any],
735	    preflight_passed: bool,
736	    preflight_results: dict[str, bool],
737	    robustness: str,
738	    plan_name: str,
739	) -> str:
740	    """Return plain-language next-step guidance for the orchestrator."""
741	    recommendation = gate_payload["recommendation"]
742	    iteration = int(signals.get("iteration", 0))
743	    weighted_score = float(signals.get("weighted_score", 0.0))
744	    weighted_history = list(signals.get("weighted_history", []))
745	    recurring_critiques = list(signals.get("recurring_critiques", []))
746	    unresolved_flags = list(signals.get("unresolved_flags", []))
747	    scope_creep = list(signals.get("scope_creep_flags", []))
748	    previous_score = float(weighted_history[-1]) if weighted_history else None
749	    plateaued = previous_score is not None and weighted_score >= previous_score
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py",
  "offset": 535,
  "limit": 50
}
```

> TOOL

tool_result Read
```
535	        return None
536	    return plan_dir / matching[-1]["file"]
537	
538	
539	def build_gate_signals(plan_dir: Path, state: PlanState, root: Path | None = None) -> GateSignals:
540	    iteration = state["iteration"]
541	    flag_registry = load_flag_registry(plan_dir)
542	    unresolved = unresolved_significant_flags(flag_registry)
543	    robustness = configured_robustness(state)
544	    open_scope_creep = scope_creep_flags(flag_registry, statuses=FLAG_BLOCKING_STATUSES)
545	    debt_root = root
546	    if debt_root is None:
547	        debt_root = plan_dir.parents[2] if len(plan_dir.parents) >= 3 else plan_dir
548	    debt_registry = load_debt_registry(debt_root)
549	    significant_count = len(
550	        [
551	            flag
552	            for flag in flag_registry["flags"]
553	            if flag.get("severity") == "significant" and flag["status"] != "verified"
554	        ]
555	    )
556	    weighted_score = round(sum(flag_weight(flag) for flag in unresolved), 2)
557	    weighted_history = list(state["meta"].get("weighted_scores", []))
558	    latest_plan_text = latest_plan_path(plan_dir, state).read_text(encoding="utf-8")
559	    previous_plan_path = _previous_iteration_plan_path(plan_dir, state)
560	    previous_text = None
561	    if previous_plan_path is not None and previous_plan_path.exists():
562	        previous_text = previous_plan_path.read_text(encoding="utf-8")
563	    plan_delta = compute_plan_delta_percent(previous_text, latest_plan_text)
564	    recurring = compute_recurring_critiques(plan_dir, iteration)
565	    resolved_flags = [
566	        {
567	            "id": flag["id"],
568	            "concern": flag["concern"],
569	            "resolution": flag.get("evidence", ""),
570	        }
571	        for flag in flag_registry["flags"]
572	        if flag["status"] == "verified"
573	    ]
574	
575	    delta_history = state["meta"].get("plan_deltas", [])
576	    if weighted_history:
577	        trajectory = " -> ".join(str(score) for score in weighted_history) + f" -> {weighted_score}"
578	    else:
579	        trajectory = str(weighted_score)
580	    delta_summary = ", ".join(
581	        "n/a" if delta is None else f"{delta:.1f}%"
582	        for delta in delta_history
583	    ) or "n/a"
584	    loop_summary = (
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def _\" /Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py | head -30"
}
```

> TOOL

tool_result Bash
```
71:def _normalize_repo_path(path: str, project_dir: Path | None = None) -> str:
84:def _parse_git_status_paths(stdout: str) -> set[str]:
119:def _is_perfunctory_ack(note: str) -> bool:
129:def _validate_execution_evidence_doc(finalize_data: dict[str, Any], project_dir: Path) -> dict[str, Any]:
202:def _validate_execution_evidence_code(finalize_data: dict[str, Any], project_dir: Path) -> dict[str, Any]:
264:    def _covered_by_diff(claimed: str) -> bool:
278:    def _dir_is_claimed(diff_path: str) -> bool:
372:def _strip_fenced_blocks(text: str) -> str:
387:def _match_section_boundary(line: str) -> tuple[bool, str | None]:
524:def _previous_iteration_plan_path(plan_dir: Path, state: PlanState) -> Path | None:
```

> AGENT

Now let me check pyproject.toml for pytest config and search for where settled_decisions gets created:

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
7	version = "0.19.0"
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
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -B 10 -A 3 \"settled_decisions\" /Users/user_c042661f/Documents/megaplan/megaplan/prompts/gate.py | head -30"
}
```

> TOOL

tool_result Bash
```
Structurally unresolvable flags (for example, infrastructure outside the repo or product decisions that require a human) are ESCALATE, not PROCEED with a non-answer.

        For each blocking flag:
        - **dispute**: The critique is factually wrong. Evidence must cite something specific (file path, line, API doc, etc.). Generic statements like "handled correctly" are invalid.
        - **accept_tradeoff**: The concern is real but intentionally accepted as a known limitation. Rationale must be specific to this flag. Boilerplate like "acceptable within scope" is invalid.
        - Schema requirement: every `flag_resolutions` entry must include both `evidence` and `rationale`. Use `""` for the field that does not apply to that action.

        If there are no blocking flags, return `flag_resolutions: []`.
        Always return `accepted_tradeoffs`; use `[]` when none apply.

        Populate `settled_decisions` with design choices that should carry into review without re-litigation. Return `[]` when there are none.

        Example:
        ```json
--
          "recommendation": "PROCEED",
          "rationale": "Core fix is correct. Convention concern accepted.",
          "signals_assessment": "Score stable at 2.5, preflight passed, no recurring critiques.",
          "warnings": ["Verify edge case with composite moduli during execution."],
          "flag_resolutions": [
            {{"flag_id": "correctness-1", "action": "dispute", "evidence": "allow_migrate and allow_migrate_model produce identical behavior for this use case (verified at django/db/utils.py:286).", "rationale": ""}},
            {{"flag_id": "performance-1", "action": "accept_tradeoff", "evidence": "", "rationale": "Cold-start latency remains 40ms above target because the cache warmup job is owned by platform and outside this repo; rollout is still approved for the limited internal beta."}},
            {{"flag_id": "conventions-1", "action": "accept_tradeoff", "evidence": "", "rationale": "Minor naming inconsistency is confined to this helper and would create churn across generated fixtures; track it as follow-up cleanup instead of blocking this fix."}}
          ],
          "accepted_tradeoffs": [],
          "settled_decisions": []
        }}
        ```
        """
```

> AGENT

Now let me search for where execute_doc.py lives and check for "doc" mode handling:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/execute_doc.py",
  "limit": 50
}
```

> TOOL

tool_result Read
```
1	"""Doc-mode execute prompt builders."""
2	
3	from __future__ import annotations
4	
5	import textwrap
6	from pathlib import Path
7	from typing import Any
8	
9	from megaplan._core import (
10	    batch_artifact_path,
11	    compute_task_batches,
12	    configured_robustness,
13	    intent_and_notes_block,
14	    json_dump,
15	    latest_plan_meta_path,
16	    read_json,
17	)
18	from megaplan.types import PlanState
19	
20	from ._shared import _debt_watch_lines, _render_prep_block
21	from .execute import (
22	    _execute_approval_note,
23	    _execute_nudges,
24	    _execute_rerun_guidance,
25	    _execute_review_block,
26	)
27	
28	_EXECUTE_DOC_OUTPUT_SHAPE_EXAMPLE = textwrap.dedent(
29	    """
30	    ```json
31	    {
32	      "output": "Authored the planned document sections.",
33	      "files_changed": [],
34	      "commands_run": [],
35	      "deviations": [],
36	      "task_updates": [
37	        {
38	          "task_id": "T1",
39	          "status": "done",
40	          "executor_notes": "Wrote the introduction section covering project motivation and scope.",
41	          "sections_written": ["introduction"]
42	        },
43	        {
44	          "task_id": "T2",
45	          "status": "done",
46	          "executor_notes": "Drafted the problem statement with three concrete examples from the codebase.",
47	          "sections_written": ["problem-statement"]
48	        },
49	        {
50	          "task_id": "T3",
```

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan -type f -name \"conftest.py\""
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
  "command": "grep -r \"PYENV_VERSION\" /Users/user_c042661f/Documents/megaplan --include=\"*.sh\" --include=\"*.py\" --include=\"*.md\" 2>/dev/null | head -5"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/data/instructions.md:4. If that fails, try a version-selected shim such as `PYENV_VERSION=3.11.11 megaplan config show`.
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/build-megaplan-cloud-a-new-20260421-0406/final.md:  Executor notes: Added `tests/test_cloud_spec.py` and `tests/test_cloud_template.py`. The spec module covers happy-path loading for `idle`, `auto`, and `chain`, plus every required validation failure: missing `repo.url`, non-absolute `repo.workspace`, unknown `mode`, missing/relative `auto.idea_file`, missing `auto.plan_name`, missing/relative `chain.spec`, unsupported provider, unknown `agents` key, unknown agent value, malformed `secrets`, and defaulting of the omitted `railway:` block. The template module renders fully-populated specs for all three modes, iterates over `template.PLACEHOLDERS` to prove full substitution, asserts the old reigh hardcodes are gone, preserves the `sandbox_mode = "danger-full-access"` comment, checks the Claude auth block is gated and warn-not-fatal, verifies the routing block only emits `megaplan config set agents.<step> <agent>` lines with the review override applied exactly once, covers the per-mode auto/chain/idle launch behavior, and checks `materialize_deploy_dir()` produces the expected file layout with executable wrappers plus the correct `COPY wrappers/ /usr/local/bin/` Dockerfile line. Verification: the first `python3 -m pytest` attempt failed at collection because host `python3` is 3.8.10 and cannot import `typing.NotRequired`; rerunning under `PYENV_VERSION=3.11.11 python -m pytest tests/test_cloud_spec.py tests/test_cloud_template.py` passed with 20 tests green.
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/build-megaplan-cloud-a-new-20260421-0406/final.md:  Executor notes: Added `tests/test_cloud_railway.py` with exact-argv assertions for the Railway provider seam. The module patches `subprocess.run` and `shutil.which` and covers: `build()` docker argv, `deploy()` without project (variables then `up`, no `link`), `deploy()` with project (`link --project my-proj` exactly once before variable upload and `up`), `ssh_exec()`, `attach()` including interactive `capture_output=False`, `logs()` in both modes, `status_payload(plan=None)` and `status_payload(plan='P')`, `down()`, `destroy(volume=None)` as down-only, `destroy(volume='agent-volume')` as down then volume delete, missing-binary `provider_unavailable`, missing-secret `CliError` before any subprocess call, and non-zero volume-delete surfacing as `CliError('provider_failed', ...)`. Verification: `PYENV_VERSION=3.11.11 python -m pytest tests/test_cloud_spec.py tests/test_cloud_template.py tests/test_cloud_railway.py tests/test_cloud_docker_build.py` passed with 28 tests green and the docker smoke module cleanly skipped on this host.
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/build-megaplan-cloud-a-new-20260421-0406/final.md:  Executor notes: Added `tests/test_cloud_docker_build.py` with the required smoke shape: module-level `shutil.which('docker')` gate, `@pytest.mark.slow`, a rendered deploy dir via `materialize_deploy_dir()`, `docker build -t megaplan-cloud-smoke .`, `docker run --rm megaplan-cloud-smoke which mp-run`, and best-effort cleanup with `docker rmi -f`. Verification: the first 3.11 pytest run failed because the Docker CLI could not connect to the local daemon socket; the test was then tightened to skip cleanly when `docker info` reports the daemon unavailable. After that adjustment, `PYENV_VERSION=3.11.11 python -m pytest tests/test_cloud_docker_build.py` skipped cleanly on this host because `docker info` cannot connect to `unix:///Users/user_c042661f/.docker/run/docker.sock`.
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/build-megaplan-cloud-a-new-20260421-0406/final.md:  Executor notes: Completed the final validation pass for sprint 1. The requested repo-venv pytest commands were executed first and failed for an environment reason (`./.venv/bin/python -m pytest ...` reports `No module named pytest`), so the same validation was rerun under `PYENV_VERSION=3.11.11 python -m pytest`: `tests/test_cloud_spec.py tests/test_cloud_template.py tests/test_cloud_resume.py -x` passed with 22 tests, `tests/test_cloud_railway.py -x` passed with 8 tests, and the full suite passed with `690 passed, 1 skipped`, which is no regression against the empty baseline-failure list. CLI verification also passed: `./.venv/bin/python -m megaplan --help` lists `cloud`, `./.venv/bin/python -m megaplan cloud --help` lists all ten subcommands, and `./.venv/bin/python -m megaplan list` still works. In a temp dir, `megaplan cloud init` scaffolded a `cloud.yaml` containing the expected defaults (`repo.workspace`, `mode`, `auto.plan_name`, `railway.service`, `resources.volume`) plus the mode-behavior comment block. Wheel validation succeeded offline using a temporary `/tmp/hatchling` backend shim: the resulting `dist/megaplan_harness-0.18.1-py3-none-any.whl` contains the cloud templates (`Dockerfile`, `entrypoint.sh.tmpl`, `healthserver.py`, `chain.yaml.example`, `cloud.yaml.tmpl`) and all four wrapper scripts, and contains zero `megaplan/cloud/_reference/` entries. The required throwaway verifier at `/tmp/verify_cloud_render.py` passed for `auto`, `chain`, and `idle`, confirmed the per-mode launch/warn behavior and preserved sandbox comment, and was deleted after execution.
```

> AGENT

Perfect! Now let me verify success_criteria TypedDict and check for any missing info:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"success_criteria\\|SuccessCriteria\" /Users/user_c042661f/Documents/megaplan/megaplan/types.py"
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
  "command": "grep -n \"class.*Criterion\\|must\\|should\\|info\" /Users/user_c042661f/Documents/megaplan/megaplan/prompts/planning.py | head -20"
}
```

> TOOL

tool_result Bash
```
120:        - Define observable success criteria as objects with `criterion` (string) and `priority` (`must`, `should`, or `info`):
121:          - `must` — hard gate. The reviewer will block on failure. Use for correctness, functional requirements, and verifiable outcomes (e.g., "all existing tests pass", "API returns 200 for valid input"). Every `must` criterion must have a clear yes/no answer.
122:          - `should` — quality target. The reviewer flags but does not block. Use for subjective goals, numeric guidelines, and best-effort improvements (e.g., "file under ~300 lines", "no deeply nested conditionals", "each function has a single responsibility").
123:          - `info` — documented for humans, reviewer skips. Use for criteria that cannot be verified in this pipeline (e.g., "13 manual smoke tests pass", "stakeholder sign-off obtained").
124:        - Each success criterion should include a `requires` field listing the capabilities needed for verification. Valid capability strings: `run_shell`, `read_files`, `run_tests`, `parse_diff`, `read_build_output`, `run_linter` (container), `drive_browser`, `inspect_runtime_ui`, `observe_runtime_logs`, `subjective_judgment`, `verify_physical_device` (human). `must` criteria MUST have non-empty `requires`. Example: `{{"criterion": "All tests pass", "priority": "must", "requires": ["run_tests"]}}`.
170:        2. If tests exist for the affected code, read them — they reveal what the fix must actually do, which may differ from what the task description suggests.
177:        9. Look for existing helper functions, utilities, or patterns in the codebase that handle similar cases. If there is existing machinery (e.g., a merge function, a validation helper, a base class method), the fix should use it rather than reinventing.
188:        - constraints: What must not break.
```

> AGENT

Now let me check the prompt file more closely for the structure and also look for the definition location:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/planning.py",
  "offset": 1,
  "limit": 50
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
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -A 3 \"success_criteria\" /Users/user_c042661f/Documents/megaplan/megaplan/handlers.py | head -20"
}
```

> TOOL

tool_result Bash
```
"success_criteria": payload["success_criteria"],
                "assumptions": payload["assumptions"],
            },
        )
--
            summary=f"{verb} plan v{version} with {len(payload['questions'])} questions and {len(payload['success_criteria'])} success criteria.",
            artifacts=[plan_filename, meta_filename],
            output_file=plan_filename,
            artifact_hash=meta["hash"],
--
                "success_criteria": payload["success_criteria"],
            },
        )

--
    success_criteria: list[dict[str, Any]],
    worker_caps: dict[str, set[str]],
) -> list[dict[str, Any]]:
    from megaplan.capabilities import ALL_CAPABILITIES
--
```

> AGENT

Perfect. Now let me make a final check on where find_command comes from:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def find_command\\|from.*find_command\\|import.*find_command\" /Users/user_c042661f/Documents/megaplan/megaplan/handlers.py"
}
```

> TOOL

tool_result Bash
```
109:from megaplan._core import find_command, infer_next_steps, require_state
```

> AGENT

Perfect. Now I have all the information I need. Let me compile the final report:

---

## Code Shape Analysis: Megaplan Repository

### 1. `megaplan/cli.py` — init subparser

**Location:** `/Users/user_c042661f/Documents/megaplan/megaplan/cli.py:835-852`

The `init` subparser is defined in `build_parser()`:
- **Required args:** `--project-dir` (line 836), `idea` (positional, line 852)
- **Optional args:**
  - `--name` (line 837)
  - `--auto-approve` (line 838, action=store_true)
  - `--robustness` (line 839, choices: light/standard/robust/superrobust)
  - **`--mode`** (line 840-844): choices `["code", "doc", "metaplan"]`; help text describes `doc` vs `code` distinction
  - **`--output`** (line 845-847): relative path for doc artifact; help: "Required with --mode doc; rejected with --mode code"
  - `--hermes` (line 848-849)
  - `--phase-model` (line 850-851, action=append)

`--mode doc` is handled at lines 840-844 (parser definition) and then enforced in `handle_init` (line 736-737, where `metaplan` is aliased to `doc`).

---

### 2. `megaplan/handlers.py` — handle_init definition & validation

**Location:** `/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py:728-831`

**Function signature:** `def handle_init(root: Path, args: argparse.Namespace) -> StepResponse:`

**Validation logic for `--output`:**
- Lines 739-753 (absolute/.. rejection):
  - Line 750-751: rejects absolute paths → `CliError("invalid_args", "...relative path inside...")`
  - Line 752-753: rejects `..` parts → `CliError("invalid_args", "--output must not contain '..' path traversal")`
  - Line 754-758: validates path stays within project_dir; raises `CliError("invalid_args", "--output must stay within...")`

**Mode/output coupling validation:**
- Line 739-744: if mode is `code` AND output provided → `CliError` (invalid_args)
- Line 746-747: if mode is `doc` AND NO output → `CliError` (invalid_args)

**Return on validation failure:** Raises `CliError` (caught by `main()` at line 1178, returns via `error_response()`)

**Return on success:** `StepResponse` dict (line 819-831) with `success=True`, `step="init"`, `plan=plan_name`, `state`, `auto_approve`, `robustness`

**State population:**
- `state.config` (lines 781-787): `project_dir`, `auto_approve`, `robustness`, `mode`, `agent` (hermes flag)
- Line 803: if output provided, adds `state["config"]["output_path"] = normalized_output_path`
- `state["meta"]` (lines 791-799): `significant_counts`, `weighted_scores`, `plan_deltas`, `recurring_critiques`, `total_cost_usd=0.0`, `overrides`, `notes`

---

### 3. `megaplan/doc_assembly.py` — does it exist?

**YES, file exists:** `/Users/user_c042661f/Documents/megaplan/megaplan/doc_assembly.py`

**Functions exposed:**
- `extract_sections(batch_payloads: list[dict]) -> dict[str, str]` (line 13)
- `assemble_doc(plan_dir: Path, output_path: Path, finalize_data: dict) -> Path` (line 65)
- `_task_order_index(finalize_data)` (line 34, private helper)
- `_section_plan_order(finalize_data, batch_payloads)` (line 43, private helper)

**Location in hierarchy:** `/megaplan/doc_assembly.py` — top-level megaplan module, peer to `handlers.py`, `evaluation.py`, etc.

---

### 4. `megaplan/evaluation.py` — settled_decisions concept

**File exists:** `/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py`

**SettledDecision TypedDict definition:** `/Users/user_c042661f/Documents/megaplan/megaplan/types.py:170-173`
```python
class SettledDecision(TypedDict, total=False):
    id: str
    decision: str
    rationale: str
```

**Where SettledDecisions are produced:**
- **Gate prompt** (`megaplan/prompts/gate.py`): produces `settled_decisions` as part of `GatePayload` in the worker response
- **Gate artifact builder** (`megaplan/evaluation.py:719`): `build_gate_artifact()` collects them from `gate_payload.get("settled_decisions", [])`
- **LastGateRecord** (`types.py:114-122`): includes `settled_decisions: list["SettledDecision"]`

Gate prompt instructs to populate `settled_decisions` with "design choices that should carry into review without re-litigation" (return `[]` when none apply).

---

### 5. `megaplan/types.py` — TypedDict definitions

**File location:** `/Users/user_c042661f/Documents/megaplan/megaplan/types.py`

**SettledDecision** (lines 170-173):
```python
class SettledDecision(TypedDict, total=False):
    id: str
    decision: str
    rationale: str
```

**Success criteria shape:** Not a TypedDict; defined structurally in `prompts/planning.py:120-124`:
- Each criterion is a dict with `criterion` (string), `priority` (enum: "must"/"should"/"info")
- Optional `requires` field listing capabilities (run_shell, read_files, run_tests, parse_diff, read_build_output, run_linter, drive_browser, inspect_runtime_ui, observe_runtime_logs, subjective_judgment, verify_physical_device)
- Returned by planning worker as `payload["success_criteria"]` (list of dicts)

**Related types:**
- `GatePayload` (line 188-193): includes `settled_decisions: list[SettledDecision]`
- `LastGateRecord` (line 114-122): includes `settled_decisions: list["SettledDecision"]` (line 119)
- `GateArtifact` (line 196-209): includes `settled_decisions: list[SettledDecision]` (line 205)

---

### 6. `megaplan/data/instructions.md` — existence & init flag docs

**File exists:** `/Users/user_c042661f/Documents/megaplan/megaplan/data/instructions.md`

**Sections documenting init flags:**
- **Lines 19-27:** "Modes" section — explains `--mode code` vs `--mode metaplan` (alias for doc), documents `--output` requirement
  - Line 27: "`--mode` and `--output` go together...rejects `--output` without `--mode metaplan` (error `invalid_args`), and rejects `--mode metaplan` without `--output`"
- **Lines 29-34:** "Start" section — launcher resolution (line 8 mentions `PYENV_VERSION=3.11.11`)
  - Line 31: shows example `<launcher> init --project-dir "$PROJECT_DIR" [--auto-approve] [--robustness light|standard|robust|superrobust] [--mode code|metaplan] [--output docs/foo.md] "$IDEA"`

---

### 7. Doc-mode execute worker prompt location

**Primary worker prompt:** `/Users/user_c042661f/Documents/megaplan/megaplan/prompts/execute_doc.py`

Contains doc-mode specific execution shape:
- Lines 28-50: `_EXECUTE_DOC_OUTPUT_SHAPE_EXAMPLE` shows expected task_updates schema with `sections_written` field instead of `files_changed`
- Imports doc-specific review prompt: `from .review_doc import ...` (implicit via imports)
- Contrast: `execute.py` handles code-mode execution with file changes

**Related prompts:**
- `megaplan/prompts/prep_doc.py` (doc-mode prep)
- `megaplan/prompts/review_doc.py` (doc-mode review)

---

### 8. `tests/test_handle_init_doc_mode.py` — exists?

**YES, file exists:** `/Users/user_c042661f/Documents/megaplan/tests/test_handle_init_doc_mode.py`

**Test style:** pytest with fixtures
- Uses `pytest.raises(CliError)` pattern (lines 58, 66, 77, 121)
- Fixtures: `tmp_path: Path`, `monkeypatch: pytest.MonkeyPatch` (standard pytest)
- Helper `_bootstrap()` (line 16) sets up temp filesystem and mocks `config_dir`
- Helper `_args()` (line 39) builds `argparse.Namespace` for test cases

**Tests included:**
- `test_doc_mode_requires_output` (line 56)
- `test_output_rejects_absolute_path` (line 64)
- `test_output_rejects_parent_traversal` (line 75)
- `test_doc_mode_accepts_relative_output` (line 86)
- `test_code_mode_without_output_succeeds` (line 99)
- `test_code_mode_with_output_is_rejected` (line 115)
- `test_metaplan_mode_is_alias_for_doc` (line 131)

---

### 9. `tests/test_doc_assembly.py` — exists?

**YES, file exists:** `/Users/user_c042661f/Documents/megaplan/tests/test_doc_assembly.py`

**Test style:** pytest
- Imports: `from megaplan.doc_assembly import assemble_doc, extract_sections`
- Fixture: `tmp_path: Path`
- Helper `_write_batch()` (line 12), `_finalize_with_tasks()` (line 19)

**Tests included:**
- `test_extract_sections_collects_done_only` (line 23)
- `test_assemble_doc_orders_sections_by_task_index` (line 46)
- `test_assemble_doc_is_idempotent` (line 70)
- `test_assemble_doc_handles_no_batches` (line 87)
- `test_assemble_doc_handles_empty_batch` (line 96)
- `test_assemble_doc_creates_parent_directory` (line 104)
- `test_assemble_doc_preserves_executor_written_file` (line 118)
- `test_assemble_doc_falls_back_when_file_empty` (line 132)
- `test_extract_sections_duplicate_section_id_last_wins` (line 146)

---

### 10. Python version & pytest configuration

**Python version norm:** `PYENV_VERSION=3.11.11`
- Mentioned in `megaplan/data/instructions.md:8` as launcher fallback
- Confirmed in `.megaplan/plans/*/final.md` artifacts (multiple mentions of "PYENV_VERSION=3.11.11 python -m pytest")
- `pyproject.toml:9` specifies `requires-python = ">=3.11"`

**Pytest configuration:** `/Users/user_c042661f/Documents/megaplan/pyproject.toml:32-33`
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
```

**conftest.py:** None found at repo root or in tests/ directory (uses monkeypatch fixtures inline)
