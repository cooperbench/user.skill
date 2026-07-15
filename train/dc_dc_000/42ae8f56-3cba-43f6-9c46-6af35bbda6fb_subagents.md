> DEVELOPER

You're designing a feature for megaplan — an LLM-driven engineering CLI at /Users/user_c042661f/Documents/megaplan. It drives a plan (init → plan → critique → gate → finalize → execute → review → done) using per-phase model assignments called "profiles" (see `megaplan/profiles/*.toml`, e.g. `standard.toml` uses claude+codex, `all-open.toml` uses kimi+glm). Profiles are defined in TOML and expand into per-phase `--phase-model` overrides. Each plan today produces a directory at `.megaplan/plans/<plan-id>/` with artifacts per phase (plan_v1.md, critique_v1.json, execution.json, review_output.json, state.json). The auto-driver in `megaplan/auto.py` runs each phase as a subprocess until the plan reaches `done`.

The user wants a new feature: **multi-profile bake-off**. Given one idea, run it in parallel under N profiles (e.g. `standard`, `all-open`, `all-kimi`), compare the results, pick one to keep, and merge learnings back to the main tree. Context: we just ran two back-to-back single-profile tests (all-open and all-kimi) on the same kind of docstring task; discovered that glm-5.1 at execute phase invented unrequested code (a `_sandbox_fingerprint` helper + `sandbox_hash` field) while kimi stayed in scope. That's the kind of signal a bake-off should surface systematically.

The user has already stated these constraints explicitly (do not re-litigate):
- **Concurrent**, not sequential. Efficiency matters.
- **Worktrees** are the isolation mechanism — each profile runs in its own worktree off the base commit.
- At the end there's a **new comparison/selection step** that produces evaluation data.
- Final merge: **keep code from ONE chosen worktree; keep evaluation data from ALL worktrees**, back into the main working tree.

Design this. I want your architectural thinking, not an implementation step-list. Focus on the load-bearing decisions and their tradeoffs. Specifically address:

1. **Worktree lifecycle**: How are the N worktrees created, where do they live (inside .megaplan? sibling dir?), what branch do they run on, how are they cleaned up after, and what happens if one run fails/crashes while others complete?

2. **Concurrent execution mechanics**: Auto-driver is currently a blocking loop. How do N autos run concurrently without stderr noise becoming unusable? Do we use subprocesses, threads, a new orchestrator? How does the user observe progress — unified log, per-profile tails, status command? Where do per-profile logs go?

3. **The comparison/selection step**: This is a new first-class phase. Is it a megaplan subcommand (`megaplan bakeoff compare`) or an integrated phase inside auto? What inputs does it read (state.json × N, artifacts × N, receipts × N — see problem 2)? What decision does it produce — does a human pick, does an LLM judge, does it auto-pick on metrics, or all three? What artifact does it emit?

4. **Merge mechanics**: Picking one tree's code is conceptually easy (`git merge` or copy the diff), but we want ALL evaluation data to come back. So we're doing a weird asymmetric merge: one tree's file changes + every tree's audit/receipt files. How do we structure this so it's clean? Do the eval artifacts live in a directory structured to avoid collision across profiles (e.g. `.megaplan/bakeoffs/<exp-id>/<profile>/`)? What does the final state of the main working tree look like after the merge completes?

5. **Failure and partial success**: One profile crashes at gate, others complete. How does the bake-off degrade gracefully? Does the comparison step proceed with N-1 profiles? Can a failed run be resumed/replayed without re-running the successful ones?

6. **CLI shape**: What does the user invoke? `megaplan bakeoff --idea-file foo.md --profiles standard all-open all-kimi`? How does state live — one top-level bake-off state, or N plan states with a pointer? What does the `status` command show for an in-flight bake-off?

7. **The load-bearing design choice** you think matters most and would cost us the most if we got wrong.

Write your response as design prose with headings, not a step-by-step implementation plan. Call out tradeoffs explicitly. Flag any assumption you're making about megaplan internals you didn't verify. Feel free to read relevant code to ground the design (`megaplan/auto.py`, `megaplan/_core/state.py`, `megaplan/profiles/__init__.py`, `megaplan/handlers/init.py`, `megaplan/types.py`). 700-1000 words.

> AGENT

I'll ground the design in megaplan's actual internals before writing prose.

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/megaplan && ls /Users/user_c042661f/Documents/megaplan/megaplan",
  "description": "List repo structure"
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
docs
evals
megaplan
plan.md
pyproject.toml
scorecard.png
tests
uv.lock
__init__.py
__main__.py
__pycache__
_core
agent
audits
auto.py
chain.py
cli.py
cloud
data
doc_assembly.py
evaluation.py
execute
flags.py
handlers
hermes_worker.py
key_pool.py
loop
parallel_critique.py
profiles
prompts
review
schemas.py
step_edit.py
types.py
workers.py
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
584	        return 4
585	    # rc=3 is already claimed by 'escalated'; use rc=5 for all-blocked so the
586	    # supervisor can distinguish "workers said every task is blocked" from a
587	    # generic stall or escalation.
588	    if outcome.status == "blocked":
589	        return 5
590	    return 1
591
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/megaplan/megaplan/profiles /Users/user_c042661f/Documents/megaplan/megaplan/handlers /Users/user_c042661f/Documents/megaplan/megaplan/_core",
  "description": "List profile and handler modules"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/_core:
__init__.py
__pycache__
io.py
phase_runtime.py
registries.py
state.py
workflow.py

/Users/user_c042661f/Documents/megaplan/megaplan/handlers:
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

/Users/user_c042661f/Documents/megaplan/megaplan/profiles:
__init__.py
__pycache__
all-open.toml
standard.toml
```

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
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers/init.py",
  "limit": 120
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
9	from megaplan.profiles import apply_profile_expansion
10	from megaplan.types import ROBUSTNESS_LEVELS, CliError, PlanState, STATE_INITIALIZED, StepResponse
11	from megaplan._core import (
12	    append_history,
13	    ensure_runtime_layout,
14	    find_command,
15	    get_effective,
16	    make_history_entry,
17	    now_utc,
18	    plans_root,
19	    save_state,
20	    slugify,
21	    workflow_next,
22	)
23	
24	from .shared import _append_to_meta, _attach_next_step_runtime, _validate_relative_path
25	
26	def handle_init(root: Path, args: argparse.Namespace) -> StepResponse:
27	    ensure_runtime_layout(root)
28	    project_dir = Path(args.project_dir).expanduser().resolve()
29	    if not project_dir.exists() or not project_dir.is_dir():
30	        raise CliError("invalid_project_dir", f"Project directory does not exist: {project_dir}")
31	    apply_profile_expansion(args, project_dir)
32	    positional_idea = getattr(args, "idea", None)
33	    idea_file = getattr(args, "idea_file", None)
34	    if positional_idea and idea_file:
35	        raise CliError("invalid_args", "Pass either the positional idea or --idea-file, not both")
36	    if idea_file:
37	        idea_path = Path(idea_file).expanduser().resolve()
38	        try:
39	            idea_text = idea_path.read_text(encoding="utf-8").strip()
40	        except OSError as exc:
41	            raise CliError("invalid_args", f"Unable to read --idea-file {idea_path}: {exc}") from exc
42	        if not idea_text:
43	            raise CliError("invalid_args", "--idea-file must contain non-empty UTF-8 text")
44	    elif positional_idea:
45	        idea_text = positional_idea
46	    else:
47	        raise CliError("invalid_args", "Provide an idea argument or --idea-file <path>")
48	    explicit_mode = getattr(args, "mode", None)
49	    raw_output_path = getattr(args, "output", None)
50	    raw_primary_criterion = getattr(args, "primary_criterion", None)
51	    mode = explicit_mode or "code"
52	    if mode == "metaplan":
53	        mode = "doc"
54	    if raw_primary_criterion and mode != "joke":
55	        raise CliError("invalid_args", "--primary-criterion is only valid with --mode joke")
56	
57	    if mode == "code" and raw_output_path:
58	        raise CliError(
59	            "invalid_args",
60	            "--output is only valid with --mode doc or --mode joke. For code-mode runs, remove "
61	            "--output; for prose artifact runs, also pass --mode doc or --mode joke.",
62	        )
63	    normalized_output_path: str | None = None
64	    if mode in {"doc", "joke"} and not raw_output_path:
65	        raise CliError("invalid_args", f"--output is required when --mode {mode} is selected")
66	    if raw_output_path:
67	        normalized_output_path = _validate_relative_path(project_dir, raw_output_path, "--output")
68	    normalized_primary_criterion: str | None = None
69	    if raw_primary_criterion is not None:
70	        normalized_primary_criterion = str(raw_primary_criterion).strip()
71	        if not normalized_primary_criterion:
72	            raise CliError("invalid_args", "--primary-criterion must be non-empty when provided")
73	    raw_from_doc = getattr(args, "from_doc", None)
74	    from_doc_rel: str | None = None
75	    imported_decisions: list[dict[str, Any]] = []
76	    parse_warnings: list[str] = []
77	    if raw_from_doc:
78	        from_doc_rel = _validate_relative_path(project_dir, raw_from_doc, "--from-doc")
79	        from_doc_abs = project_dir / from_doc_rel
80	        if not from_doc_abs.exists() or not from_doc_abs.is_file():
81	            raise CliError("invalid_args", f"--from-doc path does not exist: {from_doc_rel}")
82	        imported_decisions, parse_warnings = extract_settled_decisions(
83	            from_doc_abs.read_text(encoding="utf-8")
84	        )
85	    robustness = getattr(args, "robustness", None)
86	    if robustness is None:
87	        robustness = get_effective("execution", "robustness")
88	    if robustness not in ROBUSTNESS_LEVELS:
89	        robustness = "standard"
90	    auto_approve_value = getattr(args, "auto_approve", None)
91	    if auto_approve_value is None:
92	        auto_approve_value = get_effective("execution", "auto_approve")
93	    auto_approve = bool(auto_approve_value)
94	    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
95	    plan_name = args.name or f"{slugify(idea_text)}-{timestamp}"
96	    plan_dir = plans_root(root) / plan_name
97	    if plan_dir.exists():
98	        raise CliError("duplicate_plan", f"Plan directory already exists: {plan_name}")
99	    plan_dir.mkdir(parents=True, exist_ok=False)
100	
101	    state: PlanState = {
102	        "name": plan_name,
103	        "idea": idea_text,
104	        "current_state": STATE_INITIALIZED,
105	        "iteration": 0,
106	        "created_at": now_utc(),
107	        "config": {
108	            "project_dir": str(project_dir),
109	            "auto_approve": auto_approve,
110	            "robustness": robustness,
111	            "mode": mode,
112	            "agent": "hermes" if getattr(args, "hermes", None) is not None else "",
113	        },
114	        "sessions": {},
115	        "plan_versions": [],
116	        "history": [],
117	        "meta": {
118	            "significant_counts": [],
119	            "weighted_scores": [],
120	            "plan_deltas": [],
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
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/megaplan/megaplan/profiles/*.toml && grep -l \"receipt\\|audit\" /Users/user_c042661f/Documents/megaplan/megaplan/handlers/*.py 2>/dev/null | head -5 && ls /Users/user_c042661f/Documents/megaplan/megaplan/audits 2>/dev/null",
  "description": "Check profiles and audit artifacts"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/profiles/all-open.toml
/Users/user_c042661f/Documents/megaplan/megaplan/profiles/standard.toml
/Users/user_c042661f/Documents/megaplan/megaplan/handlers/__init__.py
/Users/user_c042661f/Documents/megaplan/megaplan/handlers/execute.py
/Users/user_c042661f/Documents/megaplan/megaplan/handlers/critique.py
/Users/user_c042661f/Documents/megaplan/megaplan/handlers/plan.py
/Users/user_c042661f/Documents/megaplan/megaplan/handlers/tiebreaker.py
__init__.py
__pycache__
audit_engine.py
capabilities.py
hermes_vendoring.py
iteration.py
quality_gates.py
robustness.py
verifiability.py
```

> DEVELOPER

You're designing a feature for megaplan — an LLM-driven engineering CLI at /Users/user_c042661f/Documents/megaplan. It drives a plan through phases (init → plan → critique → gate → finalize → execute → review → done). Each phase uses a model assigned via a "profile" (TOML presets at `megaplan/profiles/*.toml` that map phase → agent+model). Today each plan writes `.megaplan/plans/<plan-id>/` with per-phase artifacts (plan_v1.md, critique_v1.json, execution.json, review_output.json, state.json with a history array). State.history currently records `step, agent, result, duration_ms, cost_usd, prompt_tokens, completion_tokens, output_file, artifact_hash` per phase. Session logs (with actual model metadata) live at `~/.hermes/sessions/session_<id>.json` for hermes-driven runs.

The bigger context: we just ran the same docstring task under two profiles — `all-open` (kimi-plan + glm-execute) and `all-kimi` (kimi everywhere). Kimi planned tightly. GLM-5.1 at execute invented unrequested code (`_sandbox_fingerprint` helper + `sandbox_hash` field in SessionInfo). The execution audit caught it as an advisory ("Git status shows changed files not claimed by any task") but didn't block. The user wants this kind of signal to become *first-class, measurable, and historically queryable* — across every model, at every phase, across every run.

The user wants **per-step auditability** with two complementary layers:
- **Mechanical** — computable metrics from existing artifacts (no judgment required)
- **Qualitative/subjective** — evaluating *how well* a model did at a phase (required judgment: was the critique insightful? did the plan scope correctly? how good was the review?)

They also want the data to be **historically queryable** — across all plans ever, I want to ask "how has GLM performed at execute across all N runs" and get a real answer.

The user is also building a multi-profile bake-off feature in parallel (problem 1). This audit layer has to support bake-off comparison (same-task × N profiles → compare per-phase) AND longitudinal analysis (all-time × one model × one phase → trend).

Design this. Architectural thinking, not implementation steps. Address:

1. **The step receipt**: per-phase structured JSON emitted alongside existing artifacts. What's in it? What's the minimum schema that supports both immediate bake-off comparison and longitudinal analysis? How do we capture input identity (prompt hash, upstream artifact hashes) so we can replay the same input through a different model later? Should it live in the plan dir, or at a global location, or both?

2. **Phase-specific metrics**: each phase has different "interesting" numbers. Design the metrics shape per phase:
   - Plan: step count, task count, files referenced, OOS-file references, plan length
   - Critique: findings count per check, severity distribution, flagged checks vs clean checks
   - Gate: decision, flag resolutions, rework recommendations
   - Finalize: tasks count, sense-checks count
   - Execute: files claimed, files actually in diff, **scope-drift delta** (the metric that would have flagged GLM this session), LOC delta, commands run, advisory-vs-blocking audit findings
   - Review: verdict, rework items, missing-evidence count, per-task verdicts
   What extractors are shared vs per-phase? Where do they live in the codebase?

3. **Scope-drift as a first-class metric**: argue for what the right formula is. Is it just `len(files_in_diff) - len(files_claimed)`? Do we also want LOC-level drift? Do we weight by file? How do we avoid noise from obviously-benign artifacts (e.g., the execution audit file itself)? How do we surface this prominently enough that next time it happens, it's impossible to miss?

4. **Global audit log**: append-only jsonl somewhere. Where — `~/.megaplan/audit/` or `<repo>/.megaplan/audit/`? How do we handle the repo-vs-global question when the user works on many repos? What index keys matter (model × phase is primary; what else)? How do we query it — new CLI subcommand, or do we rely on `jq`?

5. **Qualitative evaluation layer**: 
   - Should it run automatically at the end of a bake-off, or be a separate user-triggered step later?
   - LLM-judge vs human vs both?
   - If LLM-judge: what model judges? What prompt structure — pairwise ("A vs B, which critique was better?") or absolute ("score this critique 1-5")? How do we avoid the judge being biased toward its own outputs?
   - Where does the judgment get stored so it can be queried alongside mechanical metrics?
   - How do we avoid this becoming sloppy / overfit to the models we test against?

6. **The separability problem**: In a bake-off, Profile A's critique reads Profile A's plan; Profile B's critique reads Profile B's plan. So "critique model A vs critique model B" is confounded by plan drift. Does the audit layer need to support **isolated-phase replay** (same plan, re-run critique with N different models) as a first-class mode, or is that a separate tool? If first-class, what does it require from the receipt schema?

7. **The one load-bearing design choice** — what would hurt most if we got it wrong?

Write design prose with headings, not step-lists. Name explicit tradeoffs. Flag assumptions about megaplan internals you didn't verify. Read relevant code as needed (`megaplan/handlers/shared.py`, `megaplan/handlers/execute.py`, `megaplan/handlers/review.py`, `megaplan/_core/state.py`, `megaplan/workers.py`, `megaplan/types.py`, and existing audit code at `megaplan/audits/` if present). 700-1000 words.

> AGENT

I'll explore the codebase first to ground the design in what actually exists.

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/megaplan/",
  "description": "List repo root"
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
docs
evals
megaplan
plan.md
pyproject.toml
scorecard.png
tests
uv.lock
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/megaplan/megaplan/ 2>/dev/null && echo \"---\" && ls /Users/user_c042661f/Documents/megaplan/megaplan/handlers/ 2>/dev/null && echo \"---\" && ls /Users/user_c042661f/Documents/megaplan/megaplan/audits/ 2>/dev/null",
  "description": "List megaplan module structure"
}
```

> TOOL

tool_result Bash
```
__init__.py
__main__.py
__pycache__
_core
agent
audits
auto.py
chain.py
cli.py
cloud
data
doc_assembly.py
evaluation.py
execute
flags.py
handlers
hermes_worker.py
key_pool.py
loop
parallel_critique.py
profiles
prompts
review
schemas.py
step_edit.py
types.py
workers.py
---
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
---
__init__.py
__pycache__
audit_engine.py
capabilities.py
hermes_vendoring.py
iteration.py
quality_gates.py
robustness.py
verifiability.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers/shared.py"
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
16	from megaplan.step_edit import next_plan_artifact_name
17	from megaplan.types import CliError, MOCK_ENV_VAR, PlanState, StepResponse
18	from megaplan._core import (
19	    append_history,
20	    apply_session_update,
21	    atomic_write_json,
22	    atomic_write_text,
23	    build_next_step_runtime,
24	    clear_active_step,
25	    configured_robustness,
26	    get_effective,
27	    infer_next_steps,
28	    make_history_entry,
29	    now_utc,
30	    record_step_failure,
31	    save_state,
32	    set_active_step,
33	    sha256_file,
34	    sha256_text,
35	    workflow_next,
36	)
37	from megaplan._core.phase_runtime import (
38	    DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
39	    PHASE_RUNTIME_POLICY,
40	    format_duration_hint,
41	)
42	from megaplan.evaluation import PLAN_STRUCTURE_REQUIRED_STEP_ISSUE, validate_plan_structure
43	from megaplan.workers import WorkerResult
44	
45	log = logging.getLogger("megaplan")
46	
47	
48	def _append_to_meta(state: PlanState, field: str, value: Any) -> None:
49	    state["meta"].setdefault(field, []).append(value)
50	
51	
52	def _merge_imported_decision_criteria(
53	    state: PlanState,
54	    criteria: list[dict[str, Any]],
55	) -> list[dict[str, Any]]:
56	    imported_decisions = state["meta"].get("imported_decisions", [])
57	    if not imported_decisions:
58	        return criteria
59	
60	    merged = list(criteria)
61	    referenced_ids = {
62	        decision_id
63	        for decision in imported_decisions
64	        for decision_id in [decision.get("id")]
65	        if isinstance(decision_id, str)
66	        and decision_id
67	        and any(
68	            decision_id in criterion_text
69	            for criterion in merged
70	            for criterion_text in [criterion.get("criterion")]
71	            if isinstance(criterion, dict) and isinstance(criterion_text, str)
72	        )
73	    }
74	    for decision in imported_decisions:
75	        decision_id = decision.get("id")
76	        if not isinstance(decision_id, str) or not decision_id or decision_id in referenced_ids:
77	            continue
78	        decision_text = decision.get("decision", "")
79	        if not isinstance(decision_text, str):
80	            decision_text = str(decision_text)
81	        load_bearing = bool(decision.get("load_bearing"))
82	        merged.append(
83	            {
84	                "criterion": f"Plan adheres to imported decision {decision_id}: {decision_text}",
85	                "priority": "must" if load_bearing else "info",
86	                "requires": ["subjective_judgment"] if load_bearing else [],
87	            }
88	        )
89	        referenced_ids.add(decision_id)
90	    return merged
91	
92	
93	def _validate_relative_path(project_dir: Path, raw: str, flag_name: str) -> str:
94	    candidate = Path(raw)
95	    if candidate.is_absolute():
96	        raise CliError(
97	            "invalid_args",
98	            f"{flag_name} must be a relative path inside the project directory",
99	        )
100	    if any(part == ".." for part in candidate.parts):
101	        raise CliError("invalid_args", f"{flag_name} must not contain '..' path traversal")
102	    resolved_path = (project_dir / candidate).resolve()
103	    try:
104	        return resolved_path.relative_to(project_dir).as_posix()
105	    except ValueError as exc:
106	        raise CliError(
107	            "invalid_args",
108	            f"{flag_name} must stay within the project directory",
109	        ) from exc
110	
111	
112	def attach_agent_fallback(response: StepResponse, args: argparse.Namespace) -> None:
113	    if hasattr(args, "_agent_fallback"):
114	        response["agent_fallback"] = args._agent_fallback
115	
116	
117	def _attach_next_step_runtime(response: StepResponse) -> None:
118	    runtime = build_next_step_runtime(
119	        response.get("next_step"),
120	        configured_timeout_seconds=int(get_effective("execution", "worker_timeout_seconds")),
121	    )
122	    if runtime is not None:
123	        response["next_step_runtime"] = runtime
124	
125	
126	_AUTO_NEXT_STEP = object()
127	
128	
129	def _emit_phase_notice(step: str) -> None:
130	    if step not in PHASE_RUNTIME_POLICY:
131	        return
132	    duration_hint = format_duration_hint(
133	        step,
134	        configured_timeout_seconds=DEFAULT_NON_EXECUTE_TIMEOUT_CAP_SECONDS,
135	    )
136	    print(f"[megaplan] Starting {step}... {duration_hint}", file=sys.stderr)
137	
138	
139	def _run_worker(
140	    step: str,
141	    state: PlanState,
142	    plan_dir: Path,
143	    args: argparse.Namespace,
144	    *,
145	    root: Path,
146	    iteration: int | None = None,
147	    resolved: tuple[str, str, bool, str | None] | None = None,
148	    prompt_override: str | None = None,
149	    prompt_kwargs: dict[str, Any] | None = None,
150	) -> tuple[WorkerResult, str, str, bool]:
151	    failure_iteration = state["iteration"] if iteration is None else iteration
152	    from megaplan import handlers as _handlers_pkg
153	
154	    apply_profile_expansion(args, Path(state["config"]["project_dir"]), state=state)
155	    agent, mode, refreshed, model = resolved or _handlers_pkg.resolve_agent_mode(step, args)
156	    run_id = set_active_step(state, step=step, agent=agent, mode=mode, model=model)
157	    _emit_phase_notice(step)
158	    save_state(plan_dir, state)
159	    try:
160	        run_step_kwargs: dict[str, Any] = {
161	            "root": root,
162	            "resolved": (agent, mode, refreshed, model),
163	            "prompt_override": prompt_override,
164	        }
165	        if prompt_kwargs is not None and _supports_prompt_kwargs(worker_module.run_step_with_worker):
166	            run_step_kwargs["prompt_kwargs"] = prompt_kwargs
167	        return worker_module.run_step_with_worker(
168	            step,
169	            state,
170	            plan_dir,
171	            args,
172	            **run_step_kwargs,
173	        )
174	    except CliError as error:
175	        clear_active_step(state, run_id=run_id)
176	        record_step_failure(plan_dir, state, step=step, iteration=failure_iteration, error=error)
177	        raise
178	    except Exception:
179	        clear_active_step(state, run_id=run_id)
180	        save_state(plan_dir, state)
181	        raise
182	
183	
184	def _supports_prompt_kwargs(run_step: Callable[..., Any]) -> bool:
185	    params = inspect.signature(run_step).parameters.values()
186	    return any(param.name == "prompt_kwargs" for param in params) or any(
187	        param.kind == inspect.Parameter.VAR_KEYWORD for param in params
188	    )
189	
190	
191	def _build_gate_prompt_override(
192	    agent_type: str,
193	    state: PlanState,
194	    plan_dir: Path,
195	    *,
196	    root: Path,
197	    missing_flag_ids: list[str],
198	) -> str:
199	    if agent_type == "claude":
200	        base_prompt = create_claude_prompt("gate", state, plan_dir, root=root)
201	    elif agent_type == "hermes":
202	        base_prompt = create_hermes_prompt("gate", state, plan_dir, root=root)
203	    else:
204	        base_prompt = create_codex_prompt("gate", state, plan_dir, root=root)
205	    missing_flags = ", ".join(missing_flag_ids)
206	    addendum = (
207	        "Gate retry for the same iteration.\n"
208	        "Your previous response recommended PROCEED but left blocking flags unresolved.\n"
209	        f"Missing blocking flag IDs: {missing_flags}.\n"
210	        "Return a complete gate response. If you recommend PROCEED, you MUST include "
211	        "`flag_resolutions` entries for every blocking flag. If you cannot resolve every "
212	        "blocking flag, return ITERATE or ESCALATE instead."
213	    )
214	    return f"{base_prompt}\n\n{addendum}"
215	
216	
217	def _finish_step(
218	    plan_dir: Path,
219	    state: PlanState,
220	    args: argparse.Namespace,
221	    *,
222	    step: str,
223	    worker: WorkerResult,
224	    agent: str,
225	    mode: str,
226	    refreshed: bool,
227	    summary: str,
228	    artifacts: list[str],
229	    output_file: str,
230	    artifact_hash: str,
231	    result: str = "success",
232	    success: bool = True,
233	    next_step: object | str | None = _AUTO_NEXT_STEP,
234	    response_fields: dict[str, Any] | None = None,
235	    history_fields: dict[str, Any] | None = None,
236	    run_id: str | None = None,
237	) -> StepResponse:
238	    clear_active_step(state, run_id=run_id)
239	    apply_session_update(state, step, agent, worker.session_id, mode=mode, refreshed=refreshed)
240	    append_history(
241	        state,
242	        make_history_entry(
243	            step,
244	            duration_ms=worker.duration_ms,
245	            cost_usd=worker.cost_usd,
246	            result=result,
247	            worker=worker,
248	            agent=agent,
249	            mode=mode,
250	            output_file=output_file,
251	            artifact_hash=artifact_hash,
252	            prompt_tokens=worker.prompt_tokens,
253	            completion_tokens=worker.completion_tokens,
254	            total_tokens=worker.total_tokens,
255	            **(history_fields or {}),
256	        ),
257	    )
258	    save_state(plan_dir, state)
259	    resolved_next = next_step
260	    if resolved_next is _AUTO_NEXT_STEP:
261	        next_steps = workflow_next(state)
262	        resolved_next = next_steps[0] if next_steps else None
263	    response: StepResponse = {
264	        "success": success,
265	        "step": step,
266	        "summary": summary,
267	        "artifacts": artifacts,
268	        "monitor_hint": build_monitor_hint(plan_dir),
269	        "next_step": resolved_next,
270	        "state": state["current_state"],
271	    }
272	    if response_fields:
273	        response.update(response_fields)
274	    _attach_next_step_runtime(response)
275	    attach_agent_fallback(response, args)
276	    return response
277	
278	
279	def _raise_step_validation_error(
280	    *,
281	    plan_dir: Path,
282	    state: PlanState,
283	    step: str,
284	    iteration: int,
285	    worker: WorkerResult,
286	    code: str,
287	    message: str,
288	) -> None:
289	    error = CliError(code, message, valid_next=infer_next_steps(state), extra={"raw_output": worker.raw_output})
290	    record_step_failure(plan_dir, state, step=step, iteration=iteration, error=error, duration_ms=worker.duration_ms)
291	    raise error
292	
293	
294	def _write_json_artifact(plan_dir: Path, filename: str, payload: dict[str, Any]) -> str:
295	    atomic_write_json(plan_dir / filename, payload)
296	    return sha256_file(plan_dir / filename)
297	
298	
299	def _write_plan_version(
300	    *,
301	    plan_dir: Path,
302	    state: PlanState,
303	    step: str,
304	    version: int,
305	    worker: WorkerResult,
306	    plan_text: str,
307	    meta_fields: dict[str, Any],
308	    plan_filename: str | None = None,
309	) -> tuple[str, str, dict[str, Any]]:
310	    resolved_plan_filename = plan_filename or next_plan_artifact_name(plan_dir, version)
311	    meta_filename = (
312	        f"plan_v{version}.meta.json"
313	        if resolved_plan_filename == f"plan_v{version}.md"
314	        else resolved_plan_filename.replace(".md", ".meta.json")
315	    )
316	    structure_warnings = _validate_generated_plan_or_raise(
317	        plan_dir=plan_dir,
318	        state=state,
319	        step=step,
320	        iteration=version,
321	        worker=worker,
322	        plan_text=plan_text,
323	    )
324	    atomic_write_text(plan_dir / resolved_plan_filename, plan_text)
325	    meta = {
326	        "version": version,
327	        "timestamp": now_utc(),
328	        "hash": sha256_text(plan_text),
329	        **meta_fields,
330	        "structure_warnings": structure_warnings,
331	    }
332	    atomic_write_json(plan_dir / meta_filename, meta)
333	    return resolved_plan_filename, meta_filename, meta
334	
335	
336	def _validate_generated_plan_or_raise(
337	    *,
338	    plan_dir: Path,
339	    state: PlanState,
340	    step: str,
341	    iteration: int,
342	    worker: WorkerResult,
343	    plan_text: str,
344	) -> list[str]:
345	    structure_warnings = validate_plan_structure(plan_text)
346	    if PLAN_STRUCTURE_REQUIRED_STEP_ISSUE in structure_warnings:
347	        error = CliError(
348	            "structure_error",
349	            f"{step.title()} output failed structural validation: {PLAN_STRUCTURE_REQUIRED_STEP_ISSUE}",
350	            valid_next=infer_next_steps(state),
351	            extra={"raw_output": worker.raw_output},
352	        )
353	        record_step_failure(
354	            plan_dir,
355	            state,
356	            step=step,
357	            iteration=iteration,
358	            error=error,
359	            duration_ms=worker.duration_ms,
360	        )
361	        raise error
362	    return structure_warnings
363
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers/execute.py"
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
7	from megaplan.execute.core import (
8	    handle_execute_auto_loop as dispatch_execute_auto_loop,
9	    handle_execute_one_batch as dispatch_execute_one_batch,
10	)
11	from megaplan.profiles import apply_profile_expansion
12	from megaplan.types import (
13	    CliError,
14	    PlanState,
15	    STATE_AWAITING_HUMAN,
16	    STATE_DONE,
17	    STATE_EXECUTED,
18	    STATE_FINALIZED,
19	    StepResponse,
20	)
21	from megaplan._core import (
22	    atomic_write_json,
23	    clear_active_step,
24	    configured_robustness,
25	    latest_plan_meta_path,
26	    load_plan_locked,
27	    read_json,
28	    require_state,
29	    save_state,
30	    set_active_step,
31	    workflow_includes_step,
32	)
33	from megaplan.workers import validate_payload, warn_if_work_dir_differs_from_project_dir
34	
35	from .shared import _emit_phase_notice, attach_agent_fallback, worker_module
36	
37	def _is_rework_reexecution(state: PlanState) -> bool:
38	    """Check if the last completed step was a review with needs_rework."""
39	    for entry in reversed(state.get("history", [])):
40	        if entry.get("step") == "review" and entry.get("result") == "needs_rework":
41	            return True
42	        if entry.get("step") == "execute":
43	            return False
44	    return False
45	
46	def handle_execute(root: Path, args: argparse.Namespace) -> StepResponse:
47	    with load_plan_locked(root, args.plan, step="execute") as (plan_dir, state):
48	        require_state(state, "execute", {STATE_FINALIZED})
49	        apply_profile_expansion(args, Path(state["config"]["project_dir"]), state=state)
50	        # Loud operator warning if the resolved sandbox root is narrower than
51	        # the plan's stored project_dir. Silent divergence here cost entire
52	        # execute runs in the past (codex sandboxed to a subdirectory, writes
53	        # to sibling subrepos failed silently).
54	        warn_if_work_dir_differs_from_project_dir(state)
55	        plan_mode = state["config"].get("mode", "code")
56	        if plan_mode not in {"doc", "joke"} and not args.confirm_destructive:
57	            raise CliError("missing_confirmation", "Execute requires --confirm-destructive")
58	        auto_approve = bool(state["config"].get("auto_approve", False))
59	        if getattr(args, "user_approved", False):
60	            state["meta"]["user_approved_gate"] = True
61	            save_state(plan_dir, state)
62	        if not auto_approve and not state["meta"].get("user_approved_gate", False):
63	            raise CliError(
64	                "missing_approval",
65	                "Execute requires explicit user approval (--user-approved) when auto-approve is not set. The orchestrator must confirm with the user at the gate checkpoint before proceeding.",
66	            )
67	        agent, mode, refreshed, model = worker_module.resolve_agent_mode("execute", args)
68	        # Force fresh session after review kickback to avoid prior-context bias
69	        if not refreshed and _is_rework_reexecution(state):
70	            refreshed = True
71	        run_id = set_active_step(state, step="execute", agent=agent, mode=mode, model=model)
72	        _emit_phase_notice("execute")
73	        save_state(plan_dir, state)
74	        try:
75	            if getattr(args, "batch", None) is not None:
76	                response = dispatch_execute_one_batch(
77	                    root=root,
78	                    plan_dir=plan_dir,
79	                    state=state,
80	                    args=args,
81	                    batch_number=args.batch,
82	                    auto_approve=auto_approve,
83	                    agent=agent,
84	                    mode=mode,
85	                    refreshed=refreshed,
86	                    model=model,
87	                )
88	            else:
89	                response = dispatch_execute_auto_loop(
90	                    root=root,
91	                    plan_dir=plan_dir,
92	                    state=state,
93	                    args=args,
94	                    auto_approve=auto_approve,
95	                    agent=agent,
96	                    mode=mode,
97	                    refreshed=refreshed,
98	                    model=model,
99	                )
100	        except CliError:
101	            clear_active_step(state, run_id=run_id)
102	            save_state(plan_dir, state)
103	            raise
104	        clear_active_step(state, run_id=run_id)
105	        if plan_mode in {"doc", "joke"} and response.get("state") == STATE_EXECUTED:
106	            from megaplan.doc_assembly import assemble_doc
107	            output_path = Path(state["config"]["project_dir"]) / state["config"]["output_path"]
108	            finalize_data = read_json(plan_dir / "finalize.json")
109	            assemble_doc(plan_dir, output_path, finalize_data)
110	        robustness = configured_robustness(state)
111	        if not workflow_includes_step(robustness, "review") and response.get("state") == STATE_EXECUTED:
112	            from megaplan.audits.capabilities import get_worker_capabilities
113	            from megaplan.audits.verifiability import classify_criteria
114	
115	            plan_meta = read_json(latest_plan_meta_path(plan_dir, state))
116	            success_criteria = plan_meta.get("success_criteria", [])
117	            worker_caps = get_worker_capabilities(state)
118	            _, human_deferred = classify_criteria(success_criteria, worker_caps)
119	
120	            stub_criteria = []
121	            has_deferred_must = False
122	            for sc in success_criteria:
123	                entry: dict[str, Any] = {
124	                    "name": sc.get("criterion", ""),
125	                    "priority": sc.get("priority", "info"),
126	                }
127	                if sc in human_deferred:
128	                    entry["pass"] = "deferred_human"
129	                    entry["evidence"] = "Requires human verification capabilities."
130	                    if sc.get("priority") == "must":
131	                        has_deferred_must = True
132	                else:
133	                    entry["pass"] = "pass"
134	                    entry["evidence"] = f"{robustness.title()} robustness: auto-approved."
135	                stub_criteria.append(entry)
136	
137	            next_state = STATE_AWAITING_HUMAN if has_deferred_must else STATE_DONE
138	
139	            stub_review = {
140	                "review_verdict": "approved",
141	                "checks": [],
142	                "pre_check_flags": [],
143	                "verified_flag_ids": [],
144	                "disputed_flag_ids": [],
145	                "criteria": stub_criteria,
146	                "issues": [],
147	                "rework_items": [],
148	                "summary": f"{robustness.title()} robustness: review skipped; stub written for artifact parity.",
149	                "task_verdicts": [],
150	                "sense_check_verdicts": [],
151	            }
152	            validate_payload("review", stub_review)
153	            atomic_write_json(plan_dir / "review.json", stub_review)
154	            artifacts = response.get("artifacts")
155	            if isinstance(artifacts, list) and "review.json" not in artifacts:
156	                artifacts.append("review.json")
157	            state["current_state"] = next_state
158	            save_state(plan_dir, state)
159	            response["state"] = next_state
160	            response["next_step"] = None
161	            response.pop("next_step_runtime", None)
162	        else:
163	            save_state(plan_dir, state)
164	        attach_agent_fallback(response, args)
165	        return response
166
```

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
311	    flags_addressed: list[Any] | None = None,
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

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/audits/audit_engine.py"
}
```

> TOOL

tool_result Read
```
1	"""Tiebreaker audit tracking — records and aggregates tiebreaker usage stats."""
2	from __future__ import annotations
3	
4	import json
5	from pathlib import Path
6	from typing import Any
7	
8	from megaplan._core import atomic_write_json, read_json, resolve_plan_dir
9	
10	AUDIT_FILE = "tiebreaker_audit.json"
11	
12	
13	def record_tiebreaker_audit(
14	    plan_dir: Path,
15	    decision: dict[str, Any],
16	    researcher_data: dict[str, Any],
17	    challenger_data: dict[str, Any],
18	    tokens_spent: int = 0,
19	    time_seconds: float = 0.0,
20	) -> dict[str, Any]:
21	    """Append an audit record to tiebreaker_audit.json in plan_dir."""
22	    record: dict[str, Any] = {
23	        "plan_name": decision.get("question", ""),
24	        "tiebreaker_index": _next_index(plan_dir),
25	        "fuzzy_group_id": decision.get("fuzzy_group_id", ""),
26	        "question": decision.get("question", ""),
27	        "researcher_pick": researcher_data.get("recommendation", ""),
28	        "challenger_pick": challenger_data.get("recommendation", ""),
29	        "human_pick": decision.get("human_pick", ""),
30	        "action": decision.get("action", ""),
31	        "matched_researcher": decision.get("human_pick", "") == researcher_data.get("recommendation", ""),
32	        "matched_challenger": decision.get("human_pick", "") == challenger_data.get("recommendation", ""),
33	        "tokens_spent": tokens_spent,
34	        "time_seconds": time_seconds,
35	        "timestamp": decision.get("timestamp", ""),
36	    }
37	    records = load_tiebreaker_audit(plan_dir)
38	    records.append(record)
39	    atomic_write_json(plan_dir / AUDIT_FILE, records)
40	    return record
41	
42	
43	def load_tiebreaker_audit(plan_dir: Path) -> list[dict[str, Any]]:
44	    """Read audit records from plan_dir. Returns empty list if none exist."""
45	    audit_path = plan_dir / AUDIT_FILE
46	    if not audit_path.exists():
47	        return []
48	    data = read_json(audit_path)
49	    if not isinstance(data, list):
50	        return []
51	    return data
52	
53	
54	def aggregate_tiebreaker_audit(root: Path) -> dict[str, Any]:
55	    """Cross-plan aggregation for --global flag. Scans all plan directories."""
56	    megaplan_dir = root / ".megaplan" / "plans"
57	    if not megaplan_dir.is_dir():
58	        return {"plans": [], "totals": _empty_totals()}
59	
60	    plan_summaries: list[dict[str, Any]] = []
61	    all_records: list[dict[str, Any]] = []
62	
63	    for plan_path in sorted(megaplan_dir.iterdir()):
64	        if not plan_path.is_dir():
65	            continue
66	        records = load_tiebreaker_audit(plan_path)
67	        if not records:
68	            continue
69	        all_records.extend(records)
70	        plan_summaries.append({
71	            "plan_dir": plan_path.name,
72	            "tiebreaker_count": len(records),
73	            "tokens_spent": sum(r.get("tokens_spent", 0) for r in records),
74	            "time_seconds": sum(r.get("time_seconds", 0) for r in records),
75	            "matched_researcher": sum(1 for r in records if r.get("matched_researcher")),
76	            "matched_challenger": sum(1 for r in records if r.get("matched_challenger")),
77	        })
78	
79	    totals = _compute_totals(all_records)
80	    return {"plans": plan_summaries, "totals": totals}
81	
82	
83	def _next_index(plan_dir: Path) -> int:
84	    return len(load_tiebreaker_audit(plan_dir))
85	
86	
87	def _empty_totals() -> dict[str, Any]:
88	    return {
89	        "total_tiebreakers": 0,
90	        "total_tokens": 0,
91	        "total_time_seconds": 0.0,
92	        "matched_researcher_count": 0,
93	        "matched_challenger_count": 0,
94	    }
95	
96	
97	def _compute_totals(records: list[dict[str, Any]]) -> dict[str, Any]:
98	    if not records:
99	        return _empty_totals()
100	    return {
101	        "total_tiebreakers": len(records),
102	        "total_tokens": sum(r.get("tokens_spent", 0) for r in records),
103	        "total_time_seconds": sum(r.get("time_seconds", 0) for r in records),
104	        "matched_researcher_count": sum(1 for r in records if r.get("matched_researcher")),
105	        "matched_challenger_count": sum(1 for r in records if r.get("matched_challenger")),
106	    }
107	
108	
109	def render_audit_report(data: dict[str, Any]) -> str:
110	    """Render audit data as a human-readable text report."""
111	    lines: list[str] = []
112	    totals = data.get("totals", _empty_totals())
113	    lines.append("=== Tiebreaker Audit Report ===")
114	    lines.append(f"Total tiebreakers: {totals['total_tiebreakers']}")
115	    lines.append(f"Total tokens: {totals['total_tokens']}")
116	    lines.append(f"Total time: {totals['total_time_seconds']:.1f}s")
117	    lines.append(f"Matched researcher: {totals['matched_researcher_count']}")
118	    lines.append(f"Matched challenger: {totals['matched_challenger_count']}")
119	
120	    plans = data.get("plans", [])
121	    if plans:
122	        lines.append("")
123	        lines.append("Per-plan breakdown:")
124	        for p in plans:
125	            lines.append(
126	                f"  {p['plan_dir']}: {p['tiebreaker_count']} tiebreakers, "
127	                f"{p['tokens_spent']} tokens, {p['time_seconds']:.1f}s"
128	            )
129	
130	    return "\n".join(lines)
131
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/megaplan/megaplan/execute/ 2>/dev/null && echo \"---\" && ls /Users/user_c042661f/Documents/megaplan/megaplan/review/ 2>/dev/null",
  "description": "List execute and review dirs"
}
```

> TOOL

tool_result Bash
```
__init__.py
__pycache__
core.py
merge.py
quality.py
timeout.py
---
__init__.py
__pycache__
checks.py
mechanical.py
parallel.py
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
151	    id: str
152	    concern: str
153	    category: str
154	    status: str
155	
156	
157	class FlagRecord(_FlagRecordRequired, total=False):
158	    severity_hint: str
159	    evidence: str
160	    raised_in: str
161	    severity: str
162	    verified: bool
163	    verified_in: str
164	    addressed_in: str
165	    settled_by_tiebreaker: str
166	
167	
168	class FlagRegistry(TypedDict):
169	    flags: list[FlagRecord]
170	
171	
172	class GateCheckResult(TypedDict):
173	    passed: bool
174	    criteria_check: dict[str, Any]
175	    preflight_results: dict[str, bool]
176	    unresolved_flags: list[FlagRecord]
177	
178	
179	class SettledDecision(TypedDict, total=False):
180	    id: str
181	    decision: str
182	    rationale: str
183	
184	
185	class SettledDecisionFromDoc(TypedDict, total=False):
186	    id: str
187	    decision: str
188	    rationale: str
189	    load_bearing: bool
190	
191	
192	class TiebreakerDecision(TypedDict, total=False):
193	    fuzzy_group_id: str
194	    flag_ids: list[str]
195	    question: str
196	    researcher_pick: str
197	    challenger_pick: str
198	    human_pick: str
199	    action: str
200	    rationale: str
201	    timestamp: str
202	
203	
204	class GatePayload(TypedDict):
205	    recommendation: str
206	    rationale: str
207	    signals_assessment: str
208	    warnings: list[str]
209	    settled_decisions: list[SettledDecision]
210	
211	
212	class GateArtifact(TypedDict, total=False):
213	    passed: bool
214	    criteria_check: dict[str, Any]
215	    preflight_results: dict[str, bool]
216	    unresolved_flags: list[FlagRecord]
217	    recommendation: str
218	    rationale: str
219	    signals_assessment: str
220	    warnings: list[str]
221	    settled_decisions: list[SettledDecision]
222	    override_forced: bool
223	    orchestrator_guidance: str
224	    robustness: str
225	    signals: dict[str, Any]
226	
227	
228	class GateSignals(TypedDict, total=False):
229	    robustness: str
230	    signals: dict[str, Any]
231	    warnings: list[str]
232	
233	
234	class StepResponse(TypedDict, total=False):
235	    success: bool
236	    step: str
237	    summary: str
238	    artifacts: list[str]
239	    next_step: str | None
240	    state: str
241	    auto_approve: bool
242	    robustness: str
243	    iteration: int
244	    plan: str
245	    plan_dir: str
246	    questions: list[str]
247	    verified_flags: list[str]
248	    open_flags: list[str]
249	    scope_creep_flags: list[str]
250	    warnings: list[str]
251	    files_changed: list[str]
252	    deviations: list[str]
253	    user_approved_gate: bool
254	    issues: list[str]
255	    valid_next: list[str]
256	    mode: str
257	    installed: list[dict[str, Any]]
258	    config_path: str
259	    routing: dict[str, str]
260	    raw_config: dict[str, Any]
261	    action: str
262	    key: str
263	    value: str
264	    skipped: bool
265	    file: str
266	    plans: list[dict[str, Any]]
267	    recommendation: str
268	    signals: dict[str, Any]
269	    rationale: str
270	    signals_assessment: str
271	    orchestrator_guidance: str
272	    passed: bool
273	    criteria_check: dict[str, Any]
274	    preflight_results: dict[str, bool]
275	    unresolved_flags: list[Any]
276	    error: str
277	    message: str
278	    details: dict[str, Any]
279	    agent_fallback: dict[str, str]
280	
281	
282	class DebtEntry(TypedDict):
283	    id: str
284	    subsystem: str
285	    concern: str
286	    flag_ids: list[str]
287	    plan_ids: list[str]
288	    occurrence_count: int
289	    created_at: str
290	    updated_at: str
291	    resolved: bool
292	    resolved_by: str | None
293	    resolved_at: str | None
294	
295	
296	class DebtRegistry(TypedDict):
297	    entries: list[DebtEntry]
298	
299	
300	# ---------------------------------------------------------------------------
301	# Constants
302	# ---------------------------------------------------------------------------
303	
304	FLAG_BLOCKING_STATUSES = {"open", "disputed", "addressed"}
305	FLAG_VALID_STATUSES = {
306	    "open", "addressed", "disputed", "verified",
307	    "accepted_tradeoff", "gate_disputed",
308	}
309	DEBT_ESCALATION_THRESHOLD = 3
310	MOCK_ENV_VAR = "MEGAPLAN_MOCK_WORKERS"
311	
312	DEFAULT_AGENT_ROUTING: dict[str, str] = {
313	    "plan": "claude",
314	    "prep": "claude",
315	    "critique": "codex",
316	    "revise": "claude",
317	    "gate": "claude",
318	    "finalize": "claude",
319	    "execute": "codex",
320	    "loop_plan": "claude",
321	    "loop_execute": "codex",
322	    "review": "codex",
323	    "tiebreaker_researcher": "codex",
324	    "tiebreaker_challenger": "codex",
325	}
326	KNOWN_AGENTS = ["claude", "codex", "hermes"]
327	ROBUSTNESS_LEVELS = ("tiny", "light", "standard", "robust", "superrobust")
328	def parse_agent_spec(spec: str) -> tuple[str, str | None]:
329	    """Parse 'hermes:model/name' → ('hermes', 'model/name') or 'claude' → ('claude', None)."""
330	    if ":" in spec:
331	        agent, model = spec.split(":", 1)
332	        return agent, model
333	    return spec, None
334	
335	
336	SCOPE_CREEP_TERMS = (
337	    "scope creep",
338	    "out of scope",
339	    "beyond the original idea",
340	    "beyond original idea",
341	    "beyond user intent",
342	    "expanded scope",
343	)
344	
345	DEFAULTS = {
346	    "execution.auto_approve": False,
347	    "execution.robustness": "standard",
348	    "execution.worker_timeout_seconds": 7200,
349	    "execution.max_review_rework_cycles": 3,
350	    "execution.max_robust_review_rework_cycles": 2,
351	    "execution.max_execute_no_progress": 3,
352	    "orchestration.max_critique_concurrency": 2,
353	    "orchestration.mode": "subagent",
354	}
355	
356	_SETTABLE_BOOL = {
357	    "execution.auto_approve",
358	}
359	
360	_SETTABLE_ENUM = {
361	    "execution.robustness": ROBUSTNESS_LEVELS,
362	}
363	
364	_SETTABLE_NUMERIC = {
365	    "execution.worker_timeout_seconds",
366	    "execution.max_review_rework_cycles",
367	    "execution.max_robust_review_rework_cycles",
368	    "execution.max_execute_no_progress",
369	    "orchestration.max_critique_concurrency",
370	}
371	
372	
373	# ---------------------------------------------------------------------------
374	# Exception
375	# ---------------------------------------------------------------------------
376	
377	class CliError(Exception):
378	    def __init__(
379	        self,
380	        code: str,
381	        message: str,
382	        *,
383	        valid_next: list[str] | None = None,
384	        extra: dict[str, Any] | None = None,
385	        exit_code: int = 1,
386	    ) -> None:
387	        super().__init__(message)
388	        self.code = code
389	        self.message = message
390	        self.valid_next = valid_next or []
391	        self.extra = extra or {}
392	        self.exit_code = exit_code
393
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/megaplan/megaplan/execute/ && echo \"---\" && find /Users/user_c042661f/Documents/megaplan/megaplan -name \"*.py\" | xargs grep -l \"scope_drift\\|files_claimed\\|files_in_diff\\|scope creep\" 2>/dev/null | head -10",
  "description": "List execute and find scope-drift references"
}
```

> TOOL

tool_result Bash
```
__init__.py
__pycache__
core.py
merge.py
quality.py
timeout.py
---
/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py
/Users/user_c042661f/Documents/megaplan/megaplan/types.py
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/critique.py
/Users/user_c042661f/Documents/megaplan/megaplan/execute/timeout.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execute/quality.py"
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	import hashlib
4	import subprocess
5	from pathlib import Path
6	from typing import Any, Callable
7	
8	from megaplan.evaluation import _parse_git_status_paths
9	from megaplan.audits.quality_gates import run_quality_checks
10	
11	
12	def _check_done_task_evidence(
13	    tasks: list[dict[str, Any]],
14	    *,
15	    issues: list[str],
16	    should_classify: Callable[[dict[str, Any]], bool],
17	    has_evidence: Callable[[dict[str, Any]], bool],
18	    has_advisory_evidence: Callable[[dict[str, Any]], bool],
19	    missing_message: str,
20	    advisory_message: str,
21	) -> list[str]:
22	    missing_task_ids: list[str] = []
23	    advisory_task_ids: list[str] = []
24	    for task in tasks:
25	        if task.get("status") != "done" or not should_classify(task):
26	            continue
27	        if has_evidence(task):
28	            continue
29	        if has_advisory_evidence(task):
30	            advisory_task_ids.append(task["id"])
31	        else:
32	            missing_task_ids.append(task["id"])
33	    if missing_task_ids:
34	        issues.append(missing_message + ", ".join(missing_task_ids))
35	    if advisory_task_ids:
36	        issues.append(advisory_message + ", ".join(advisory_task_ids))
37	    return missing_task_ids
38	
39	
40	def _normalize_execute_claimed_path(path: str, project_dir: Path | None = None) -> str:
41	    p = Path(path.strip())
42	    if project_dir is not None and p.is_absolute():
43	        try:
44	            p = p.relative_to(project_dir)
45	        except ValueError:
46	            pass
47	    return p.as_posix()
48	
49	
50	def _repo_path_hash(project_dir: Path, relative_path: str) -> str:
51	    target = project_dir / relative_path
52	    if not target.exists():
53	        return "<missing>"
54	    if target.is_dir():
55	        return "<directory>"
56	    return hashlib.sha256(target.read_bytes()).hexdigest()
57	
58	
59	def _capture_git_status_snapshot(
60	    project_dir: Path,
61	) -> tuple[dict[str, str], str | None]:
62	    if not (project_dir / ".git").exists():
63	        return {}, "Project directory is not a git repository."
64	    try:
65	        process = subprocess.run(
66	            ["git", "status", "--short"],
67	            cwd=str(project_dir),
68	            text=True,
69	            capture_output=True,
70	            timeout=30,
71	        )
72	    except FileNotFoundError:
73	        return {}, "git not found on PATH."
74	    except subprocess.TimeoutExpired:
75	        return {}, "git status timed out."
76	    if process.returncode != 0:
77	        return (
78	            {},
79	            f"git status failed: {process.stderr.strip() or process.stdout.strip()}",
80	        )
81	    paths = _parse_git_status_paths(process.stdout)
82	    return {path: _repo_path_hash(project_dir, path) for path in paths}, None
83	
84	
85	def _observed_batch_paths(
86	    *,
87	    project_dir: Path,
88	    before_snapshot: dict[str, str],
89	    after_snapshot: dict[str, str],
90	) -> set[str]:
91	    observed: set[str] = set()
92	    for path in set(before_snapshot) | set(after_snapshot):
93	        before_hash = before_snapshot.get(path)
94	        after_hash = after_snapshot.get(path)
95	        if after_hash is None:
96	            after_hash = _repo_path_hash(project_dir, path)
97	        if before_hash is None or before_hash != after_hash:
98	            observed.add(path)
99	    return observed
100	
101	
102	def _collect_execute_claimed_paths(
103	    payload: dict[str, Any], project_dir: Path | None = None
104	) -> set[str]:
105	    """Collect top-level files_changed only for git observation comparison.
106	
107	    Per-task files_changed are intentionally excluded — they often include
108	    files the executor read/verified but didn't modify, which causes false
109	    phantom-claim deviations when compared against git status deltas.
110	    Per-task evidence is validated separately by the audit path.
111	    """
112	    return {
113	        _normalize_execute_claimed_path(path, project_dir)
114	        for path in payload.get("files_changed", [])
115	        if isinstance(path, str) and path.strip()
116	    }
117	
118	
119	def _observe_git_changes(
120	    *,
121	    project_dir: Path,
122	    payload: dict[str, Any],
123	    before_snapshot: dict[str, str],
124	    before_error: str | None,
125	    batch_number: int,
126	    batches_total: int,
127	    capture_git_status_snapshot_fn: Callable[[Path], tuple[dict[str, str], str | None]],
128	) -> list[str]:
129	    issues: list[str] = []
130	    if before_error is not None:
131	        issues.append(
132	            f"Advisory observation skip before batch {batch_number}/{batches_total}: {before_error}"
133	        )
134	    after_snapshot, after_error = capture_git_status_snapshot_fn(project_dir)
135	    if after_error is not None:
136	        issues.append(
137	            f"Advisory observation skip after batch {batch_number}/{batches_total}: {after_error}"
138	        )
139	    elif before_error is None:
140	        observed_paths = _observed_batch_paths(
141	            project_dir=project_dir,
142	            before_snapshot=before_snapshot,
143	            after_snapshot=after_snapshot,
144	        )
145	        claimed_paths = _collect_execute_claimed_paths(payload, project_dir)
146	        phantom_claims = sorted(claimed_paths - observed_paths)
147	        if phantom_claims:
148	            issues.append(
149	                "Advisory observation mismatch: executor claimed files not observed in git status/content hash delta: "
150	                + ", ".join(phantom_claims)
151	            )
152	        unclaimed_changes = sorted(observed_paths - claimed_paths)
153	        if unclaimed_changes:
154	            issues.append(
155	                "Advisory observation mismatch: git status/content hash delta found unclaimed files: "
156	                + ", ".join(unclaimed_changes)
157	            )
158	    return issues
159	
160	
161	def _collect_quality_deviations(
162	    *,
163	    project_dir: Path,
164	    before_snapshot: dict[str, str],
165	    before_line_counts: dict[str, int],
166	    quality_config: dict[str, Any],
167	    capture_git_status_snapshot_fn: Callable[[Path], tuple[dict[str, str], str | None]],
168	) -> list[str]:
169	    try:
170	        after_snapshot, after_error = capture_git_status_snapshot_fn(project_dir)
171	    except (
172	        Exception
173	    ) as exc:  # pragma: no cover - defensive guard for advisory-only quality checks.
174	        return [
175	            f"Advisory quality: skipped quality checks because post-batch git snapshot failed: {exc}"
176	        ]
177	    if after_error is not None:
178	        return [
179	            f"Advisory quality: skipped quality checks because post-batch git snapshot failed: {after_error}"
180	        ]
181	    changed_paths = _observed_batch_paths(
182	        project_dir=project_dir,
183	        before_snapshot=before_snapshot,
184	        after_snapshot=after_snapshot,
185	    )
186	    return run_quality_checks(
187	        project_dir,
188	        changed_paths=changed_paths,
189	        before_line_counts=before_line_counts,
190	        config=quality_config,
191	    )
192
```

> AGENT

I've seen enough. The task is a single design document — tasks aren't relevant. Let me quickly check the handlers for review and one more spot to ground the design.

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers/review.py"
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	import argparse
4	import os
5	from pathlib import Path
6	from typing import Any
7	
8	from megaplan import handlers as _pkg
9	from megaplan.review import checks as review_checks
10	from megaplan.execute.core import _check_done_task_evidence, build_monitor_hint
11	from megaplan.evaluation import is_rubber_stamp
12	from megaplan.execute.merge import _validate_and_merge_batch
13	from megaplan.prompts import create_claude_prompt, create_codex_prompt, create_hermes_prompt
14	from megaplan.profiles import apply_profile_expansion
15	from megaplan.types import (
16	    MOCK_ENV_VAR,
17	    CliError,
18	    PlanState,
19	    STATE_AWAITING_HUMAN,
20	    STATE_DONE,
21	    STATE_EXECUTED,
22	    STATE_FINALIZED,
23	    StepResponse,
24	)
25	from megaplan.workers import (
26	    WorkerResult,
27	    validate_payload,
28	    warn_if_work_dir_differs_from_project_dir,
29	)
30	from megaplan._core import (
31	    append_history,
32	    apply_session_update,
33	    atomic_write_json,
34	    atomic_write_text,
35	    clear_active_step,
36	    configured_robustness,
37	    get_effective,
38	    load_plan_locked,
39	    make_history_entry,
40	    read_json,
41	    record_step_failure,
42	    render_final_md,
43	    require_state,
44	    save_state,
45	    set_active_step,
46	    sha256_file,
47	)
48	
49	from .shared import (
50	    _attach_next_step_runtime,
51	    _emit_phase_notice,
52	    _run_worker,
53	    _supports_prompt_kwargs,
54	    attach_agent_fallback,
55	    worker_module,
56	)
57	
58	def _build_review_blocked_message(
59	    *,
60	    verdict_count: int,
61	    total_tasks: int,
62	    check_count: int,
63	    total_checks: int,
64	    missing_reviewer_evidence: list[str],
65	) -> str:
66	    if missing_reviewer_evidence:
67	        return (
68	            "Blocked: done tasks are missing reviewer evidence_files without a substantive reviewer_verdict ("
69	            + ", ".join(missing_reviewer_evidence)
70	            + "). Re-run review to complete."
71	        )
72	    return (
73	        "Blocked: incomplete review coverage "
74	        f"({verdict_count}/{total_tasks} task verdicts, {check_count}/{total_checks} sense checks). "
75	        "Re-run review to complete."
76	    )
77	
78	def _is_substantive_reviewer_verdict(text: str) -> bool:
79	    return not is_rubber_stamp(text, strict=True)
80	
81	def _build_review_prompt_override(
82	    agent_type: str,
83	    state: PlanState,
84	    plan_dir: Path,
85	    *,
86	    root: Path,
87	    pre_check_flags: list[dict[str, Any]],
88	) -> str:
89	    if agent_type == "claude":
90	        return create_claude_prompt("review", state, plan_dir, root=root, pre_check_flags=pre_check_flags)
91	    if agent_type == "hermes":
92	        return create_hermes_prompt("review", state, plan_dir, root=root, pre_check_flags=pre_check_flags)
93	    return create_codex_prompt("review", state, plan_dir, root=root, pre_check_flags=pre_check_flags)
94	
95	def _merge_review_verdicts(
96	    worker_payload: dict[str, Any],
97	    finalize_data: dict[str, Any],
98	    issues: list[str],
99	) -> tuple[int, int, int, int, list[str]]:
100	    """Merge task verdicts and sense check verdicts into finalize_data.
101	
102	    Returns (verdict_count, total_tasks, check_count, total_checks, missing_evidence).
103	    """
104	    tasks_by_id = {task["id"]: task for task in finalize_data.get("tasks", [])}
105	    verdict_count, total_tasks = _validate_and_merge_batch(
106	        worker_payload.get("task_verdicts"),
107	        required_fields=("task_id", "reviewer_verdict", "evidence_files"),
108	        targets_by_id=tasks_by_id,
109	        id_field="task_id",
110	        merge_fields=("reviewer_verdict", "evidence_files"),
111	        issues=issues,
112	        validation_label="task_verdicts",
113	        merge_label="task_verdict",
114	        incomplete_message=lambda merged, total: f"Incomplete review: {merged}/{total} tasks received a reviewer verdict.",
115	        nonempty_fields={"reviewer_verdict"},
116	        array_fields=("evidence_files",),
117	    )
118	    sense_checks_by_id = {sc["id"]: sc for sc in finalize_data.get("sense_checks", [])}
119	    check_count, total_checks = _validate_and_merge_batch(
120	        worker_payload.get("sense_check_verdicts"),
121	        required_fields=("sense_check_id", "verdict"),
122	        targets_by_id=sense_checks_by_id,
123	        id_field="sense_check_id",
124	        merge_fields=("verdict",),
125	        issues=issues,
126	        validation_label="sense_check_verdicts",
127	        merge_label="sense_check_verdict",
128	        incomplete_message=lambda merged, total: f"Incomplete review: {merged}/{total} sense checks received a verdict.",
129	        nonempty_fields={"verdict"},
130	    )
131	    missing_evidence = _check_done_task_evidence(
132	        finalize_data.get("tasks", []),
133	        issues=issues,
134	        should_classify=lambda task: bool(task.get("reviewer_verdict", "").strip()),
135	        has_evidence=lambda task: bool(task.get("evidence_files")),
136	        has_advisory_evidence=lambda task: _is_substantive_reviewer_verdict(task.get("reviewer_verdict", "")),
137	        missing_message="Done tasks missing reviewer evidence_files without a substantive reviewer_verdict: ",
138	        advisory_message="Advisory: done tasks rely on substantive reviewer_verdict without evidence_files (FLAG-006 softening): ",
139	    )
140	    return verdict_count, total_tasks, check_count, total_checks, missing_evidence
141	
142	def _resolve_review_outcome(
143	    review_verdict: str,
144	    verdict_count: int,
145	    total_tasks: int,
146	    check_count: int,
147	    total_checks: int,
148	    missing_evidence: list[str],
149	    robustness: str,
150	    state: PlanState,
151	    issues: list[str],
152	    criteria: list[dict[str, Any]] | None = None,
153	) -> tuple[str, str, str | None]:
154	    """Determine review result, next state, and next step.
155	
156	    Returns (result, next_state, next_step).
157	    """
158	    blocked = (
159	        verdict_count < total_tasks
160	        or check_count < total_checks
161	        or bool(missing_evidence)
162	    )
163	    if blocked:
164	        return "blocked", STATE_EXECUTED, "review"
165	
166	    rework_requested = review_verdict == "needs_rework"
167	    if rework_requested:
168	        cap_key = (
169	            "max_robust_review_rework_cycles"
170	            if robustness in {"robust", "superrobust"}
171	            else "max_review_rework_cycles"
172	        )
173	        max_review_rework_cycles = get_effective("execution", cap_key)
174	        prior_rework_count = sum(
175	            1 for entry in state.get("history", [])
176	            if entry.get("step") == "review" and entry.get("result") == "needs_rework"
177	        )
178	        if prior_rework_count >= max_review_rework_cycles:
179	            issues.append(
180	                f"Max review rework cycles ({max_review_rework_cycles}) reached. "
181	                "Force-proceeding to done despite unresolved review issues."
182	            )
183	        else:
184	            return "needs_rework", STATE_FINALIZED, "execute"
185	
186	    if criteria:
187	        has_deferred_must = any(
188	            c.get("pass") == "deferred_human" and c.get("priority") == "must"
189	            for c in criteria
190	        )
191	        if has_deferred_must:
192	            return "success", STATE_AWAITING_HUMAN, None
193	
194	    return "success", STATE_DONE, None
195	
196	_EXPECTED_BY_CHECK_ID = {
197	    "coverage": "Extend the fix so every concrete failing example, symptom, or 'X should Y' statement in the issue is addressed by at least one diff line.",
198	    "placement": "Move the fix upstream to where the bad state is first introduced, or extend it to cover any alternate entry points identified in the finding.",
199	    "adjacent_calls": "Apply the same fix to each additional call site, sibling class, or downstream consumer identified in the finding.",
200	    "simplicity": "Remove unjustified changes, or justify each extra line against a concrete issue requirement.",
201	}
202	
203	def _synthesize_review_rework_items(checks: list[dict[str, Any]]) -> list[dict[str, str]]:
204	    rework_items: list[dict[str, str]] = []
205	    for check in checks:
206	        check_id = check.get("id", "")
207	        if not isinstance(check_id, str) or not check_id:
208	            continue
209	        check_def = review_checks.get_check_by_id(check_id)
210	        if getattr(check_def, "default_severity", "") != "likely-significant":
211	            continue
212	        question = str(check.get("question", "") or "").strip()
213	        findings = check.get("findings", [])
214	        if not isinstance(findings, list):
215	            continue
216	        for finding in findings:
217	            if not isinstance(finding, dict) or not finding.get("flagged"):
218	                continue
219	            status = str(finding.get("status", "") or "").strip().lower()
220	            # megaplan/prompts/review.py:243-249 constrains status to {blocking, significant, minor, n/a};
221	            # significant is the explicit non-blocking downgrade for gate-settled concerns, while missing or
222	            # empty status means the model failed to classify, so we keep the check's default_severity gate as
223	            # the blocking fallback. That is the safe default for the sympy-21930 / sphinx-9711 regressions.
224	            if status and status != "blocking":
225	                continue
226	            detail = str(finding.get("detail", "") or "").strip()
227	            evidence_file = finding.get("evidence_file", "")
228	            if not isinstance(evidence_file, str):
229	                evidence_file = ""
230	            issue = detail or question or f"Heavy review found a blocking {check_id} issue."
231	            # Prefer a per-check actionable expected string; fall back to the
232	            # check's self-question; ultimately fall back to a generic message.
233	            expected = (
234	                _EXPECTED_BY_CHECK_ID.get(check_id)
235	                or question
236	                or f"Review check '{check_id}' should pass without blocking findings."
237	            )
238	            # `actual` should NOT duplicate `issue` — use a templated
239	            # acknowledgment of the finding instead so the executor sees
240	            # a clear "you didn't resolve it" signal without a copy of
241	            # the detail text.
242	            actual = f"The diff did not resolve the flagged {check_id} concern above."
243	            rework_items.append(
244	                {
245	                    "task_id": f"REVIEW-{check_id}",
246	                    "issue": issue,
247	                    "expected": expected,
248	                    "actual": actual,
249	                    "evidence_file": evidence_file,
250	                    "source": f"review_{check_id}",
251	                }
252	            )
253	    return rework_items
254	
255	def handle_review(root: Path, args: argparse.Namespace) -> StepResponse:
256	    with load_plan_locked(root, args.plan, step="review") as (plan_dir, state):
257	        require_state(state, "review", {STATE_EXECUTED})
258	        apply_profile_expansion(args, Path(state["config"]["project_dir"]), state=state)
259	        # Mirror the execute-phase sandbox-divergence warning so reviewers
260	        # notice when codex is pinned to a narrower tree than the plan's
261	        # project_dir.
262	        warn_if_work_dir_differs_from_project_dir(state)
263	        robustness = configured_robustness(state)
264	        plan_mode = state["config"].get("mode", "code")
265	        pre_check_flags: list[dict[str, Any]] = []
266	        if robustness in {"standard", "robust", "superrobust"} and plan_mode not in {"doc", "joke"}:
267	            pre_check_flags = _pkg.run_pre_checks(plan_dir, state, Path(state["config"]["project_dir"]))
268	        if robustness in {"standard", "light", "robust"}:
269	            resolved = None
270	            prompt_override = None
271	            prompt_kwargs = None
272	            if robustness in {"standard", "robust"}:
273	                resolved = _pkg.resolve_agent_mode("review", args)
274	                if _supports_prompt_kwargs(worker_module.run_step_with_worker):
275	                    prompt_kwargs = {"pre_check_flags": pre_check_flags}
276	                else:
277	                    prompt_override = _build_review_prompt_override(
278	                        resolved[0],
279	                        state,
280	                        plan_dir,
281	                        root=root,
282	                        pre_check_flags=pre_check_flags,
283	                    )
284	            worker, agent, mode, refreshed = _run_worker(
285	                "review",
286	                state,
287	                plan_dir,
288	                args,
289	                root=root,
290	                resolved=resolved,
291	                prompt_override=prompt_override,
292	                prompt_kwargs=prompt_kwargs,
293	            )
294	            if robustness in {"standard", "robust"}:
295	                worker.payload["pre_check_flags"] = pre_check_flags
296	                _pkg.update_flags_after_review(plan_dir, worker.payload, iteration=state["iteration"])
297	            atomic_write_json(plan_dir / "review.json", worker.payload)
298	        else:
299	            agent_type, mode, refreshed, model = _pkg.resolve_agent_mode("review", args)
300	            if agent_type != "hermes" or os.getenv(MOCK_ENV_VAR) == "1":
301	                worker, agent, mode, refreshed = _run_worker(
302	                    "review",
303	                    state,
304	                    plan_dir,
305	                    args,
306	                    root=root,
307	                    resolved=(agent_type, mode, refreshed, model),
308	                )
309	                atomic_write_json(plan_dir / "review.json", worker.payload)
310	                issues = list(worker.payload.get("issues", []))
311	                finalize_data = read_json(plan_dir / "finalize.json")
312	
313	                review_verdict = worker.payload.get("review_verdict")
314	                if review_verdict not in {"approved", "needs_rework"}:
315	                    issues.append("Invalid review_verdict; expected 'approved' or 'needs_rework'.")
316	                    review_verdict = "needs_rework"
317	
318	                verdict_count, total_tasks, check_count, total_checks, missing_evidence = _merge_review_verdicts(
319	                    worker.payload, finalize_data, issues,
320	                )
321	                atomic_write_json(plan_dir / "finalize.json", finalize_data)
322	                atomic_write_text(plan_dir / "final.md", render_final_md(finalize_data, phase="review"))
323	                finalize_hash = sha256_file(plan_dir / "finalize.json")
324	
325	                result, next_state, next_step = _resolve_review_outcome(
326	                    review_verdict, verdict_count, total_tasks,
327	                    check_count, total_checks, missing_evidence,
328	                    robustness,
329	                    state, issues,
330	                    criteria=worker.payload.get("criteria", []),
331	                )
332	                state["current_state"] = next_state
333	
334	                clear_active_step(state)
335	                apply_session_update(state, "review", agent, worker.session_id, mode=mode, refreshed=refreshed)
336	                append_history(
337	                    state,
338	                    make_history_entry(
339	                        "review",
340	                        duration_ms=worker.duration_ms, cost_usd=worker.cost_usd,
341	                        result=result,
342	                        worker=worker, agent=agent, mode=mode,
343	                        output_file="review.json",
344	                        prompt_tokens=worker.prompt_tokens,
345	                        completion_tokens=worker.completion_tokens,
346	                        total_tokens=worker.total_tokens,
347	                        artifact_hash=sha256_file(plan_dir / "review.json"),
348	                        finalize_hash=finalize_hash,
349	                    ),
350	                )
351	                save_state(plan_dir, state)
352	
353	                passed = sum(1 for c in worker.payload.get("criteria", []) if c.get("pass") in (True, "pass"))
354	                total = len(worker.payload.get("criteria", []))
355	                if result == "blocked":
356	                    summary = _build_review_blocked_message(
357	                        verdict_count=verdict_count, total_tasks=total_tasks,
358	                        check_count=check_count, total_checks=total_checks,
359	                        missing_reviewer_evidence=missing_evidence,
360	                    )
361	                elif result == "needs_rework":
362	                    summary = "Review requested another execute pass. Re-run execute using the review findings as context."
363	                else:
364	                    summary = f"Review complete: {passed}/{total} success criteria passed."
365	
366	                response: StepResponse = {
367	                    "success": result == "success",
368	                    "step": "review",
369	                    "summary": summary,
370	                    "artifacts": ["review.json", "finalize.json", "final.md"],
371	                    "monitor_hint": build_monitor_hint(plan_dir),
372	                    "next_step": next_step,
373	                    "state": next_state,
374	                    "issues": issues,
375	                    "rework_items": list(worker.payload.get("rework_items", [])),
376	                }
377	                _attach_next_step_runtime(response)
378	                attach_agent_fallback(response, args)
379	                return response
380	
381	            run_id = None
382	            try:
383	                run_id = set_active_step(state, step="review", agent=agent_type, mode=mode, model=model)
384	                _emit_phase_notice("review")
385	                save_state(plan_dir, state)
386	                checks = review_checks.checks_for_robustness("superrobust")
387	                parallel_result = _pkg.run_parallel_review(
388	                    state,
389	                    plan_dir,
390	                    root=root,
391	                    model=model if agent_type == "hermes" else None,
392	                    checks=checks,
393	                    pre_check_flags=pre_check_flags,
394	                )
395	                criteria_payload = parallel_result.payload.get("criteria_payload")
396	                if not isinstance(criteria_payload, dict):
397	                    raise CliError("worker_parse_error", "Parallel review did not return a criteria payload object")
398	                merged_payload = dict(criteria_payload)
399	                merged_payload["checks"] = list(parallel_result.payload.get("checks", []))
400	                merged_payload["pre_check_flags"] = pre_check_flags
401	                merged_payload["verified_flag_ids"] = list(parallel_result.payload.get("verified_flag_ids", []))
402	                merged_payload["disputed_flag_ids"] = list(parallel_result.payload.get("disputed_flag_ids", []))
403	
404	                review_rework_items = _synthesize_review_rework_items(merged_payload["checks"])
405	                merged_payload.setdefault("rework_items", [])
406	                merged_payload.setdefault("issues", [])
407	                if review_rework_items:
408	                    merged_payload["rework_items"].extend(review_rework_items)
409	                    existing_issues = {str(issue) for issue in merged_payload["issues"] if isinstance(issue, str)}
410	                    for item in review_rework_items:
411	                        if item["issue"] not in existing_issues:
412	                            merged_payload["issues"].append(item["issue"])
413	                            existing_issues.add(item["issue"])
414	                    merged_payload["review_verdict"] = "needs_rework"
415	
416	                validate_payload("review", merged_payload)
417	                atomic_write_json(plan_dir / "review.json", merged_payload)
418	                _pkg.update_flags_after_review(plan_dir, merged_payload, iteration=state["iteration"])
419	                worker = WorkerResult(
420	                    payload=merged_payload,
421	                    raw_output=parallel_result.raw_output,
422	                    duration_ms=parallel_result.duration_ms,
423	                    cost_usd=parallel_result.cost_usd,
424	                    session_id=None,
425	                    prompt_tokens=parallel_result.prompt_tokens,
426	                    completion_tokens=parallel_result.completion_tokens,
427	                    total_tokens=parallel_result.total_tokens,
428	                )
429	                agent, mode, refreshed = "hermes", "persistent", True
430	            except CliError as error:
431	                clear_active_step(state, run_id=run_id)
432	                record_step_failure(plan_dir, state, step="review", iteration=state["iteration"], error=error)
433	                raise
434	            except Exception:
435	                clear_active_step(state, run_id=run_id)
436	                save_state(plan_dir, state)
437	                raise
438	
439	        issues = list(worker.payload.get("issues", []))
440	        finalize_data = read_json(plan_dir / "finalize.json")
441	
442	        review_verdict = worker.payload.get("review_verdict")
443	        if review_verdict not in {"approved", "needs_rework"}:
444	            issues.append("Invalid review_verdict; expected 'approved' or 'needs_rework'.")
445	            review_verdict = "needs_rework"
446	
447	        verdict_count, total_tasks, check_count, total_checks, missing_evidence = _merge_review_verdicts(
448	            worker.payload, finalize_data, issues,
449	        )
450	
451	        atomic_write_json(plan_dir / "finalize.json", finalize_data)
452	        atomic_write_text(plan_dir / "final.md", render_final_md(finalize_data, phase="review"))
453	        finalize_hash = sha256_file(plan_dir / "finalize.json")
454	
455	        result, next_state, next_step = _resolve_review_outcome(
456	            review_verdict, verdict_count, total_tasks,
457	            check_count, total_checks, missing_evidence,
458	            robustness,
459	            state, issues,
460	            criteria=worker.payload.get("criteria", []),
461	        )
462	        state["current_state"] = next_state
463	
464	        clear_active_step(state)
465	        apply_session_update(state, "review", agent, worker.session_id, mode=mode, refreshed=refreshed)
466	        append_history(
467	            state,
468	            make_history_entry(
469	                "review",
470	                duration_ms=worker.duration_ms, cost_usd=worker.cost_usd,
471	                result=result,
472	                worker=worker, agent=agent, mode=mode,
473	                output_file="review.json",
474	                prompt_tokens=worker.prompt_tokens,
475	                completion_tokens=worker.completion_tokens,
476	                total_tokens=worker.total_tokens,
477	                artifact_hash=sha256_file(plan_dir / "review.json"),
478	                finalize_hash=finalize_hash,
479	            ),
480	        )
481	        save_state(plan_dir, state)
482	
483	        passed = sum(1 for c in worker.payload.get("criteria", []) if c.get("pass") in (True, "pass"))
484	        total = len(worker.payload.get("criteria", []))
485	        if result == "blocked":
486	            summary = _build_review_blocked_message(
487	                verdict_count=verdict_count, total_tasks=total_tasks,
488	                check_count=check_count, total_checks=total_checks,
489	                missing_reviewer_evidence=missing_evidence,
490	            )
491	        elif result == "needs_rework":
492	            summary = "Review requested another execute pass. Re-run execute using the review findings as context."
493	        else:
494	            summary = f"Review complete: {passed}/{total} success criteria passed."
495	
496	        response: StepResponse = {
497	            "success": result == "success",
498	            "step": "review",
499	            "summary": summary,
500	            "artifacts": ["review.json", "finalize.json", "final.md"],
501	            "monitor_hint": build_monitor_hint(plan_dir),
502	            "next_step": next_step,
503	            "state": next_state,
504	            "issues": issues,
505	            "rework_items": list(worker.payload.get("rework_items", [])),
506	        }
507	        _attach_next_step_runtime(response)
508	        attach_agent_fallback(response, args)
509	        return response
510
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/megaplan/megaplan/profiles/ && echo \"---\" && find /Users/user_c042661f/Documents/megaplan/megaplan -maxdepth 3 -name \"workers.py\" -o -name \"hermes_worker.py\" | head -5",
  "description": "List profiles and worker files"
}
```

> TOOL

tool_result Bash
```
__init__.py
__pycache__
all-open.toml
standard.toml
---
/Users/user_c042661f/Documents/megaplan/megaplan/hermes_worker.py
/Users/user_c042661f/Documents/megaplan/megaplan/workers.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/workers.py",
  "offset": 1,
  "limit": 120
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
12	import sys
13	import tempfile
14	import textwrap
15	import time
16	import uuid
17	from dataclasses import dataclass
18	from pathlib import Path
19	from typing import Any, Callable
20	
21	from megaplan.audits.robustness import (
22	    build_empty_template,
23	    checks_for_robustness,
24	    joke_checks_for_robustness,
25	)
26	from megaplan.schemas import SCHEMAS, get_execution_schema_key
27	from megaplan.types import (
28	    CliError,
29	    DEFAULT_AGENT_ROUTING,
30	    MOCK_ENV_VAR,
31	    PlanState,
32	    SessionInfo,
33	    parse_agent_spec,
34	)
35	from megaplan._core import (
36	    apply_session_update,
37	    configured_robustness,
38	    detect_available_agents,
39	    phase_timeout_seconds,
40	    get_effective,
41	    json_dump,
42	    latest_plan_meta_path,
43	    load_config,
44	    now_utc,
45	    read_json,
46	    schemas_root,
47	)
48	from megaplan.prompts import create_claude_prompt, create_codex_prompt
49	
50	
51	_EXECUTE_STEPS = {"execute", "loop_execute"}
52	_CODEX_TEMPLATE_WRITE_STEPS = {"critique", "review"}
53	
54	# Shared mapping from step name to schema filename, used by both
55	# run_claude_step and run_codex_step.
56	STEP_SCHEMA_FILENAMES: dict[str, str] = {
57	    "plan": "plan.json",
58	    "prep": "prep.json",
59	    "revise": "revise.json",
60	    "critique": "critique.json",
61	    "gate": "gate.json",
62	    "finalize": "finalize.json",
63	    "execute": "execution.json",
64	    "loop_plan": "loop_plan.json",
65	    "loop_execute": "loop_execute.json",
66	    "review": "review.json",
67	    "tiebreaker_researcher": "tiebreaker_researcher.json",
68	    "tiebreaker_challenger": "tiebreaker_challenger.json",
69	}
70	
71	# Derive required keys per step from SCHEMAS so they aren't duplicated.
72	_STEP_REQUIRED_KEYS: dict[str, list[str]] = {
73	    step: SCHEMAS[filename].get("required", [])
74	    for step, filename in STEP_SCHEMA_FILENAMES.items()
75	}
76	
77	
78	@dataclass
79	class CommandResult:
80	    command: list[str]
81	    cwd: Path
82	    returncode: int
83	    stdout: str
84	    stderr: str
85	    duration_ms: int
86	
87	
88	@dataclass
89	class WorkerResult:
90	    payload: dict[str, Any]
91	    raw_output: str
92	    duration_ms: int
93	    cost_usd: float
94	    session_id: str | None = None
95	    trace_output: str | None = None
96	    prompt_tokens: int = 0
97	    completion_tokens: int = 0
98	    total_tokens: int = 0
99	
100	
101	# ---------------------------------------------------------------------------
102	# Worker working directory resolution (git-worktree isolation)
103	#
104	# When megaplan is invoked from a git worktree, the plan's stored project_dir
105	# may point at a *different* checkout (usually the main repo). To avoid
106	# subprocess workers writing source code into the wrong working tree, resolve
107	# the "working directory" at CLI entry (CWD, or an explicit --work-dir
108	# override) and pass *that* through to the worker's --add-dir / -C flags.
109	#
110	# Plan state files (.megaplan/plans/...) still live under project_dir; only
111	# the source-code working tree tracked by the subprocess changes.
112	# ---------------------------------------------------------------------------
113	
114	_WORK_DIR_OVERRIDE: Path | None = None
115	_WORK_DIR_WARNED: bool = False
116	
117	
118	def set_work_dir_override(path: Path | str | None) -> None:
119	    """Set an explicit working directory for subprocess workers.
120
```

> AGENT

I have enough grounding. Note the user mentioned `all-kimi` but only `all-open.toml` and `standard.toml` exist today — I'll treat `all-kimi` as a profile the user will add, not an existing one. Now the design.

---

# Multi-Profile Bake-Off: Architectural Design

## Framing

A bake-off is not a new plan lifecycle. It is a meta-orchestrator that spawns N existing plan lifecycles, then runs a single additional phase (comparison) across their outputs. The load-bearing insight is that megaplan's `auto.py` is already a clean, self-contained driver that exits with a structured `DriverOutcome`; if we preserve that contract, the bake-off becomes a thin layer that launches N drivers in isolation and joins on their outcomes. The wrong move here is to reach into `auto.drive()` and make it multi-aware — the right move is to treat each profile run as a black box that produces `(worktree, plan-dir, outcome)` and do all bake-off bookkeeping outside.

## 1. Worktree Lifecycle

Worktrees live as **siblings** of the main repo, not inside `.megaplan/`. A path like `../.megaplan-worktrees/<exp-id>/<profile>/` keeps them off the indexed tree and avoids the circular-recursion risk of putting a checkout of the repo inside the repo's own `.megaplan/` (which megaplan's `resolve_plan_dir` already walks with `rglob(".megaplan")` — putting worktrees there would make plan resolution ambiguous across profiles). Each worktree is created with `git worktree add --detach <path> <base-sha>`, where `base-sha` is captured once at bake-off start so every profile demonstrably starts from the same commit. Detached is deliberate: these are throwaway heads, we don't want N profile branches polluting `git branch`.

Cleanup is **explicit and deferred**. On bake-off completion, evaluation artifacts are copied back first, then worktrees are removed with `git worktree remove --force`. On crash or SIGINT, worktrees are left in place with a `BAKEOFF_CRASHED` marker file; the next `megaplan bakeoff status <exp-id>` command can offer to clean them up. Never auto-delete on failure — the diff in a crashed worktree is often the most interesting forensic artifact, which is exactly the signal that surfaced the glm-5.1 invention bug in the first place.

## 2. Concurrent Execution

The orchestrator launches N `megaplan auto --plan <name>` subprocesses, one per worktree, with `cwd=<worktree>` and pipes redirected to per-profile log files at `.megaplan/bakeoffs/<exp-id>/<profile>/auto.log`. Do not interleave to a shared stderr — that's unreadable at N=3+ and destroys the post-mortem value. The orchestrator polls `<worktree>/.megaplan/plans/<plan>/state.json` mtimes plus subprocess `poll()` to track progress.

For observability: a `megaplan bakeoff status <exp-id>` subcommand reads each profile's `state.json` plus the running subprocess PIDs, prints a compact table (`profile | state | phase | iter | age`). For live watching, `megaplan bakeoff tail <exp-id> [--profile X]` either tails one log or multiplexes all of them with `[profile]` prefixes (a la `tail -f`). A unified log is a convenience view, **not** the canonical log — canonical logs are per-profile files.

Subprocesses, not threads. The auto-driver already shells out per phase; threading gives us nothing and makes signal handling worse. Use `asyncio.create_subprocess_exec` or `concurrent.futures.ProcessPoolExecutor` — I'd lean `asyncio` because it makes the "wait for any to finish, then check others" pattern natural.

## 3. Comparison/Selection Step

This is a **new first-class phase**, implemented as a megaplan subcommand (`megaplan bakeoff compare --exp <exp-id>`) so it can be run standalone, resumed, or re-run with a different judge model after the bake-off completes. Embedding it inside a driver loop would violate the "each profile is a black box" principle.

Inputs the compare step ingests per profile: `state.json` (final state, iteration counts, rework cycles), `plan_v*.md`, `critique_v*.json`, `execution.json`, `review_output.json`, receipts from `audits/`, the git diff (`git diff <base-sha>..HEAD` inside the worktree), and the auto-driver's final `DriverOutcome` JSON. It emits `.megaplan/bakeoffs/<exp-id>/comparison.json` + `comparison.md`.

The decision layer is **three-tier**, in this order:
1. **Auto-computed metrics**: diff stats, test pass/fail, rework cycle count, escalations, review outcome, duration, tokens consumed. These are always produced.
2. **LLM judge**: a single model (configurable, default claude) reads all N bundles and produces a structured verdict with scope-drift flags, quality ranking, and concerns per profile. This is where the glm-5.1 `_sandbox_fingerprint` invention gets caught — the judge is explicitly prompted to flag "code not traceable to a plan task."
3. **Human override**: the `comparison.md` presents the judge's verdict + metrics, and the human runs `megaplan bakeoff pick --exp <exp-id> --profile <name>` to record the selection. If they agree with the judge, that's one command.

The judge is **advisory**, the human is authoritative. This matters because the whole point of the bake-off is to catch failures in LLM output quality; trusting an LLM as the sole judge reintroduces the failure mode we're trying to detect.

## 4. Merge Mechanics

The asymmetric merge has a clean structure because the two halves touch disjoint paths:

- **Code half** (from one chosen worktree): apply `git diff <base-sha>..<chosen-worktree-HEAD>` to the main working tree. Not `git merge` — we don't want the commit history of a detached throwaway branch in the main tree. Either `git apply` the patch or `cp -r` the changed files. Patch-apply is cleaner because it fails loudly on conflicts with any main-tree work that happened in parallel.

- **Evaluation half** (from all worktrees): copy `.megaplan/bakeoffs/<exp-id>/<profile>/` trees back. These paths are **profile-namespaced by construction**, so there is no collision. The compare step's `comparison.json` lives at `.megaplan/bakeoffs/<exp-id>/comparison.json`, alongside a `chosen` pointer.

Final main-tree state post-merge: the chosen profile's code changes applied, plus `.megaplan/bakeoffs/<exp-id>/{standard,all-open,all-kimi,comparison.json,chosen.json}/...` with full artifacts from every profile. The chosen plan's `.megaplan/plans/<plan-id>/` is **also** copied back so follow-up work can reference it; the losing profiles' plan dirs stay only in the bake-off archive, not in `.megaplan/plans/`. This avoids polluting the plan list with rejected runs while preserving forensics.

Assumption I did not verify: that no megaplan handler writes absolute paths into state that would break when moved from worktree to main tree. `state.json` stores `config.project_dir` — the merge step must rewrite that field to the main tree's path (or the archive must be treated as read-only forensic data, never loaded by live commands).

## 5. Failure and Partial Success

Each profile's driver exits with a `DriverOutcome.status` in `{done, stalled, escalated, failed, aborted, cap, blocked, awaiting_human, tiebreaker_*}`. The bake-off treats anything other than `done` as a non-winner candidate but **still surfaces it to the comparison step** — a profile that stalls at gate is itself valuable evaluation data ("this profile can't plan this kind of idea"). Compare proceeds with whatever succeeded; the report explicitly labels failed profiles rather than hiding them.

Resumability: because each worktree's plan state is independent and persisted, `megaplan bakeoff resume <exp-id>` checks each profile's state, relaunches auto only for profiles that haven't reached terminal, and leaves the winners alone. The bake-off state file tracks `launched_at`, `profiles[].pid`, `profiles[].outcome` so resume can distinguish "crashed mid-run" from "finished".

## 6. CLI Shape

```
megaplan bakeoff run --idea-file foo.md --profiles standard all-open all-kimi [--mode code] [--exp-id <name>]
megaplan bakeoff status [--exp <id>]
megaplan bakeoff tail --exp <id> [--profile X]
megaplan bakeoff compare --exp <id> [--judge claude]
megaplan bakeoff pick --exp <id> --profile <name>
megaplan bakeoff merge --exp <id>
megaplan bakeoff abandon --exp <id>
```

State: **one top-level bake-off state** at `.megaplan/bakeoffs/<exp-id>/bakeoff.json` (base-sha, profiles list, worktree paths, plan-ids, outcomes, chosen, phase) with pointers to each profile's plan state. N plan states already exist inside worktrees — they're the authoritative per-profile record. The bake-off state is a thin coordination layer, not a duplication.

`status` for an in-flight bake-off shows a per-profile table. `status` when a bake-off is the "current" context (detected by the presence of an unfinished `.megaplan/bakeoffs/<exp-id>/bakeoff.json` without a `merged_at`) takes precedence over the normal single-plan status view, with a clear `[bakeoff <exp-id>]` header.

## 7. The Load-Bearing Decision

**The comparison step's artifact schema is the thing that matters most.** Not the worktree mechanics, not the concurrency — those are solved problems we just have to wire up correctly. The comparison schema is the new thing, and it determines whether this feature has compounding value or becomes a novelty.

If `comparison.json` is well-structured — with stable fields like `scope_drift_flags[]`, `metrics.{diff_lines,tests_added,rework_cycles,duration_s,escalations}`, `judge_verdict.{rank,rationale,concerns}`, `human_decision.{chosen,rationale}` — then bake-offs accumulate into a dataset you can mine: "kimi wins on docstring tasks 7/10 times," "glm-5.1 produces scope drift 30% of runs," "claude plans but codex executes better on TS." That is the actual product. The worktrees and the concurrency are plumbing.

If the schema is ad-hoc or captures only the winner's name, every bake-off is a one-off and the forensic value evaporates the moment you tear the worktrees down. Spend disproportionate design effort on that schema, version it explicitly (`schema_version: 1`), and make every bake-off write the same fields even when a profile failed early (nulls and flags, not missing keys). Everything else is easy to change later; the artifact schema is the one thing that, once populated across a dozen runs, becomes painful to migrate.

---

### Critical Files for Implementation

- /Users/user_c042661f/Documents/megaplan/megaplan/auto.py
- /Users/user_c042661f/Documents/megaplan/megaplan/cli.py
- /Users/user_c042661f/Documents/megaplan/megaplan/profiles/__init__.py
- /Users/user_c042661f/Documents/megaplan/megaplan/handlers/init.py
- /Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py

> AGENT

I have enough grounding. Now the design document.

---

# Per-Step Auditability for megaplan

This design introduces a structured **step receipt** emitted alongside each phase artifact, a global **audit log** derived from those receipts, and a **qualitative evaluation** layer that sits on top. It is shaped by two constraints the user named: bake-off comparison (same task, N profiles, one time) and longitudinal analysis (one model × one phase × all history). The existing `state.history` array and the per-plan artifacts (`plan_v1.md`, `critique_v1.json`, `execution.json`, `review.json`) stay authoritative; receipts are a denormalized, append-only projection designed for querying.

Assumptions I didn't fully verify: that hermes session JSON at `~/.hermes/sessions/session_<id>.json` is the canonical place to recover actual model metadata; that `workers.WorkerResult` carries `session_id` for every agent path including codex/claude wrappers (I saw it on the claude/codex paths but didn't trace every branch); and that the existing `megaplan/audits/` directory is for runtime pre/post-execute quality gates, not historical analytics — the `tiebreaker_audit.json` precedent at `megaplan/audits/audit_engine.py` is a plan-dir JSON that aggregates globally, which is the nearest analogue I found.

## The Step Receipt

One receipt per `(plan_id, phase, iteration, attempt)` — written as `step_receipt_<phase>_v<iteration>.json` into the plan dir *and* appended (as a single line) to a global jsonl. Dual write is deliberate: the plan-dir copy is narrated alongside the artifact for humans resuming a specific plan; the jsonl is for fleet-wide queries and is the only thing a longitudinal query has to scan. If they diverge, the plan dir wins and the jsonl can be rebuilt from plan dirs.

Minimum schema, in three tiers:

- **Identity & provenance** — `receipt_id` (uuid), `plan_id`, `phase`, `iteration`, `attempt`, `timestamp_utc`, `profile_name` (e.g. `all-open`), `agent`, `agent_mode` (`oneshot`/`persistent`), `model_configured` (what the profile asked for), `model_actual` (what the hermes session says actually answered — these diverge more than people think), `session_id`, `megaplan_version` (git sha or pyproject version), `schema_version` of the receipt itself.
- **Input identity** — `prompt_hash` (sha256 of the full rendered prompt), `upstream_artifact_hashes` (ordered: e.g. critique's upstream is the plan_v1.md hash; execute's upstream is finalize.json hash; review's is execution.json + finalize.json). This is the replay key: to re-run *the same input* through a different model later, you resolve these hashes back to bytes.
- **Mechanical metrics** — a `metrics` object, phase-shaped (below). Plus `cost_usd`, `duration_ms`, `prompt_tokens`, `completion_tokens`, and a `verdict` string the phase can overload (`approved`/`needs_rework`/`proceed`/etc.).

Tradeoff: `prompt_hash` is expensive to make stable. The same prompt contains timestamps, plan-id, repo-relative paths, maybe env fingerprints. A **canonical prompt hash** — hash of the prompt after redacting a fixed allow-list of transient fields — is what's actually queryable. Ship both: `prompt_hash_raw` for exact debugging, `prompt_hash_canonical` for replay-equivalence. Without this, isolated-phase replay (section 6) is useless.

## Phase-Specific Metrics

I want one `extractors/` module (probably `megaplan/receipts/extractors.py`) with per-phase pure functions `extract_plan_metrics(plan_text, plan_meta, idea)`, `extract_critique_metrics(critique_json)`, etc. They take already-written artifacts as input and return dicts — no I/O of their own, so they're trivially testable and replayable on historical plans to backfill.

- **Plan**: `step_count`, `task_count`, `files_referenced` (list), `files_referenced_in_scope`/`out_of_scope` against a resolved repo path set, `oos_file_count`, `plan_chars`, `plan_words`, `success_criteria_count`, `must_vs_info_ratio`, `structure_warnings_count`.
- **Critique**: `findings_per_check` (map), `severity_distribution` (`blocking`/`likely-significant`/`minor`), `clean_checks_count`, `flagged_checks_count`, `rubber_stamp_ratio` (reuses `is_rubber_stamp`), `novel_concern_ids` (diff vs prior critique iterations).
- **Gate**: `recommendation` (PROCEED/ITERATE/ESCALATE), `blocking_flags_resolved`, `blocking_flags_remaining`, `override_forced` (bool), `signals_hash`.
- **Finalize**: `tasks_count`, `sense_checks_count`, `per_task_evidence_file_count`, `finalize_hash`.
- **Execute**: `files_claimed` (from `files_changed`), `files_in_diff` (git delta post-run), `scope_drift_files_added`, `scope_drift_files_missing`, `loc_added`, `loc_removed`, `loc_added_outside_claimed`, `commands_run_count`, `advisory_issues_count`, `blocking_issues_count`, `audit_phantom_claims`, `audit_unclaimed_changes`. Most of this is already computed inside `megaplan/execute/quality.py` — the work is *surfacing* it into a structured receipt instead of throwing it into an issues-list.
- **Review**: `review_verdict`, `task_verdicts_count`/`total_tasks`, `sense_check_verdicts_count`/`total`, `missing_evidence_count`, `rework_items_count`, `criteria_pass_count`, `criteria_deferred_count`, `pre_check_flag_counts_by_severity`.

Shared helpers live in `megaplan/receipts/shared.py`: `count_git_loc_delta`, `resolve_repo_relative_paths`, `hash_prompt_canonical`. Extractors are called from each handler right before `_finish_step` (in `handlers/shared.py`) and the dict is handed to `make_history_entry` + a new `emit_receipt` sibling call.

## Scope-Drift as a First-Class Metric

The GLM-at-execute failure is the crucial test case. The minimum viable formula:

```
scope_drift_files_added   = |files_in_diff \ files_claimed \ benign_set|
scope_drift_files_missing = |files_claimed  \ files_in_diff|
```

where `benign_set` is a static allow-list: `.megaplan/**`, `execution.json`, `final.md`, `review.json`, `*.meta.json`, lock files, generated lockfiles explicitly declared in plan. That list lives in a single constant, not scattered.

LOC drift matters as a *second* signal because GLM's pattern (invented helper, invented field) is *content* drift inside already-claimed files. So also track `loc_added_outside_claimed` and `loc_added_in_claimed_but_not_in_task_evidence` — the second one is harder but catches "claimed the file, added 40 extra lines unrelated to the task." Pragmatic v1: compute LOC drift only at the file level, flag if `loc_added_outside_claimed > 0`.

Do **not** weight by file. Weighting invites a judgment call per file that becomes stale fast. Keep the raw numbers; let the reviewer (human or LLM-judge) decide if the drift matters.

Surfacing: scope_drift should appear in three places. (1) Top of the `StepResponse` summary for execute when non-zero — loud, unambiguous. (2) A `scope_drift_severity` field on the receipt (`none`/`low`/`high`) using dumb thresholds (`added > 0 and outside_claimed_loc > 20` → high). (3) Promoted from advisory to **blocking** in `execute/quality.py` when severity is high, behind a robustness-level gate (warn at `standard`, block at `robust`/`superrobust`). The current behavior — advisory-only — is what let the GLM regression slip; the design decision worth making explicit is that scope drift above threshold becomes a blocking gate by default.

## Global Audit Log

Location: **`~/.megaplan/audit/receipts.jsonl`**, with an optional per-repo mirror at `<repo>/.megaplan/audit/receipts.jsonl`. The home-dir copy is authoritative for cross-repo longitudinal queries; the repo copy exists so a repo is self-contained (shareable, reproducible in CI). Writes are append-only with fsync; a `receipts.index.sqlite` alongside is rebuilt on demand from the jsonl and stores the queryable columns: `(model_actual, phase, profile_name, plan_id, timestamp, repo_path, verdict, scope_drift_severity, cost_usd)`. Rebuilding from jsonl rather than writing to sqlite inline avoids making sqlite a correctness dependency — jsonl is the source of truth, sqlite is a cache.

Index keys that matter, ranked: `model_actual × phase` (the primary longitudinal query), `profile_name × plan_id` (the bake-off query), `prompt_hash_canonical` (the replay query), `repo_path × phase` (per-project trends).

Query surface: a `megaplan audit` subcommand. `megaplan audit query --model glm-5.1 --phase execute --since 30d --agg avg,p50,p95` for the fleet question. `megaplan audit bakeoff <plan_group_id>` for per-phase profile comparison, rendering a table. Do **not** rely on `jq` alone as the interface — the schema is too wide and the aggregations (median, stddev) are annoying in jq. But the jsonl should remain jq-queryable as a fallback; don't invent a binary format.

## Qualitative Evaluation Layer

Separate from the mechanical layer, separate file (`step_judgment_<phase>_v<iter>.json`), linked by `receipt_id`. Not written during a run — written **on demand** via `megaplan audit judge <plan_id> [--phase ...]`. Running it automatically after every run is wasteful and makes every plan cost 2× to 3×; running it on demand (or automatically only after a bake-off) keeps it tractable.

LLM-judge, pairwise whenever possible, absolute only as fallback. Pairwise ("given these two critiques of the same plan, which is more insightful and why?") is empirically more reliable than 1–5 scoring. The bake-off structure *gives you* pairs for free. For longitudinal analysis there's no natural pair — there, use absolute rubric scoring, but *anchor* it: present the model with a known-good and known-bad example of the phase output (stored as reference fixtures) and ask it to score relative to those. This blunts rubric drift.

Self-bias mitigation: judge with a **third model that isn't either contestant** in a pairwise. For bake-off of `all-open` vs `all-kimi`, the judge should be Sonnet or GPT-5, not kimi or glm. Accept that you can't eliminate bias; document which judge was used (`judge_model`, `judge_prompt_version`) on every judgment record, and keep both judgments if you run multiple judges. Run periodic sanity checks where a small set of judgments are redone by a human (you); store those as the calibration set.

Storage: judgments live in `~/.megaplan/audit/judgments.jsonl`, keyed by `receipt_id`, queryable via the same subcommand (`megaplan audit query --with-judgment`). Joining mechanical + qualitative at query time is the whole point.

Overfitting: the judge prompt itself must be version-controlled in-repo (`megaplan/prompts/judge/*.md`) and the version recorded on every judgment. The temptation will be to tune the judge prompt to catch the GLM-at-execute case; resist. Keep the rubric model-agnostic ("did the output scope to the task? did it invent new public API not requested?") and let mechanical metrics catch the concrete cases.

## The Separability Problem

Isolated-phase replay must be first-class. Without it, a bake-off answers "is profile A better than profile B?" but never "is model X better at phase P?" — and the user explicitly asked the second question.

This is where the `prompt_hash_canonical` + `upstream_artifact_hashes` in the receipt pay for themselves. A replay command — `megaplan replay --plan <id> --phase critique --model glm-5.1` — resolves the exact plan+state at that phase boundary (from the receipt's upstream hashes), reconstructs the prompt bit-identical, runs it through the requested model, and writes a *replay receipt* (`replay_id` referencing the original `receipt_id`). The replay receipt is just another row in the jsonl, with `replay_of=<receipt_id>`, so queries like "all critiques ever generated against plan_v1 hash X" join naturally.

What it requires from the receipt schema: the upstream hashes have to be *resolvable* — either the bytes are still in the plan dir, or they're stored in a content-addressed blob store alongside (`~/.megaplan/audit/blobs/<sha256>`). v1 relies on the plan dir (good enough for recent plans, breaks for archived ones). v2 introduces the blob store; don't build v2 until v1 proves the workflow.

## The One Load-Bearing Choice

**Input identity — specifically the canonical prompt hash.** If this is wrong, everything downstream degrades gracefully into "interesting but not trusted." A sloppy prompt hash means replay isn't really replay, longitudinal "same phase, different model" queries aren't comparing like-for-like, and bake-off judgments are confounded by prompt drift we can't detect. Get this one right before shipping anything else: define exactly which fields are redacted before hashing, write a test that proves two runs of the same plan at the same phase produce identical canonical hashes, and version the canonicalization function so future changes are detectable rather than silent. Everything else (metrics shapes, jsonl location, judge model) can be iterated on; the prompt hash is the load-bearing primitive the rest of the system rests on.

### Critical Files for Implementation
- /Users/user_c042661f/Documents/megaplan/megaplan/handlers/shared.py
- /Users/user_c042661f/Documents/megaplan/megaplan/_core/state.py
- /Users/user_c042661f/Documents/megaplan/megaplan/execute/quality.py
- /Users/user_c042661f/Documents/megaplan/megaplan/workers.py
- /Users/user_c042661f/Documents/megaplan/megaplan/audits/audit_engine.py

> DEVELOPER

You are auditing a megaplan multi-profile bake-off that ran tonight. Four model profiles concurrently attempted to implement the same feature spec; this is a real-world test of profile differentiation.

## Background

**The task** (in `.megaplan/ideas/auto-retry-and-cost-cap.md`): two combined features for `megaplan auto`:
1. Auto-retry execute with `--fresh` when codex returns "Codex ran out of room in the model's context"
2. New `--max-cost-usd N` flag that aborts gracefully when cumulative spend exceeds N

**The 4 profiles:**
- `standard`: claude (plan/revise/finalize) + codex (critique/execute/review)
- `all-open`: kimi-k2.6 (plan/revise/finalize) + glm-5.1 (critique/execute/review)
- `all-kimi`: kimi-k2.6 for ALL phases
- `all-deepseek`: deepseek-v4-pro for all phases — **DEAD on init** (HTTP 404 from OpenRouter, model didn't exist)

**Experiment ID**: `reliability-20260424-235843`

**Where the data lives:**
- Worktrees: `/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/<profile>/`
- Bakeoff archive: `/Users/user_c042661f/Documents/megaplan/.megaplan/bakeoffs/reliability-20260424-235843/<profile>/` — contains `auto.log`, `outcome.json`, `init.log`
- Per-profile plan dir inside each worktree: `<worktree>/.megaplan/plans/reliability-20260424-235843/` — contains `state.json`, `final.md`, `finalize.json`, `plan_v*.md`, `critique_v*.json`, `gate.json`, `gate_signals_v*.json`, `execution_batch_*.json`, `execution.json`, `execution_audit.json`, `review.json` (only standard), `step_receipt_*.json` (sprint 1 receipts).
- Working directory for git diff: each worktree is a separate detached-HEAD checkout from base SHA `5044b795`. Run `git -C <worktree> diff HEAD` to see each profile's source changes.

**Outcomes:**
- `standard`: status=done, review=approved, 0 rework items, 4 files changed (597+ / 64-)
- `all-open`: status=stalled — substantial work present in worktree (7 files, 565+ / 2-) but auto-driver got stuck; never reviewed
- `all-kimi`: status=stalled — even more work (8 files, 636+ / 6-); never reviewed
- `all-deepseek`: dead at init phase (404 from OpenRouter)

## What to audit

Produce a comparative analysis. Be opinionated. The user wants USEFUL signal, not a checkbox tour. Specifically:

1. **Per-profile work assessment**: For each of the 3 profiles that produced code (standard, all-open, all-kimi):
   - What design did each take? Look at the actual diff via `git -C <worktree> diff HEAD`. Quote key snippets.
   - How does each handle Task A (context-retry-with-fresh)? Compare regex-match approach, retry counter management, integration with stall logic.
   - How does each handle Task B (`--max-cost-usd`)? Compare check timing (after every phase? only certain phases?), how cumulative cost is summed, abort state-transition, error reporting.
   - Code quality: clear naming? Tests included? Edge cases handled? Defensive guards?
   - Scope discipline: did they only touch what the task required, or did they wander? (Look at execution_audit.json for any scope-drift findings.)

2. **Why the hermes profiles stalled**: Both `all-open` and `all-kimi` stalled at state=finalized after running execute repeatedly. Each execute apparently did partial work (5+ batches written, real code on disk) but state never transitioned to "executed". The auto.log iterations 12-17 for all-open all show the same `state=finalized next=execute` loop. Diagnose:
   - What pattern caused the stall? Look at `execution.json` (shows 0 completed_tasks despite batch files existing) and the per-batch json files. Was each batch starting fresh and overwriting prior progress?
   - Did execute exit with success or failure each iter? Look at the JSON event log embedded at the end of auto.log.
   - Is this the SAME class of bug the task was meant to fix (context-window-style failures), or something different (e.g. validation gating)?

3. **Cost vs value comparison**: Use the per-phase cost breakdown:
   - `standard`: $3.71 recorded but cost-tracking is broken (codex phases show $0; real cost likely 2-3× higher)
   - `all-open`: $14.13 — hermes critique alone was $2.79 / 4.47M tokens. glm-5.1 dominant cost.
   - `all-kimi`: $4.57 — kimi cheaper per token than glm
   - Which gave best value (work-shipped-per-dollar)?
   - Critique cost is enormous on glm-5.1. Why?

4. **Pick a winner**. Justify in one paragraph. The user will use your pick to inform `megaplan bakeoff pick`.

5. **Three concrete megaplan follow-up bugs / improvements** uncovered by this run, ranked by impact. Examples we noticed but want you to confirm and add to:
   - Cost tracking is broken for codex phases in standard profile — needs same instrumentation as claude phases
   - `bakeoff run --detach`'s subprocess didn't write its own outcome.json file (stdout-only). Real bug.
   - Both hermes profiles hit the exact failure mode the task was designed to fix — proving the bug is general

Output format: markdown, 600-1000 words. Lead with the winner, then sections per topic. Quote 2-3 actual code snippets you find compelling. Be specific (file paths, function names, line numbers where possible).

> AGENT

I'll audit this bake-off systematically. Let me start by exploring the data layout in parallel.

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/ && echo \"---\" && ls /Users/user_c042661f/Documents/megaplan/.megaplan/bakeoffs/reliability-20260424-235843/",
  "description": "List worktree and bakeoff directories"
}
```

> TOOL

tool_result Bash
```
all-deepseek
all-kimi
all-open
standard
---
all-deepseek
all-kimi
all-open
bakeoff.json
standard
```

> TOOL

tool_use Bash
```json
{
  "command": "cat /Users/user_c042661f/Documents/megaplan/.megaplan/ideas/auto-retry-and-cost-cap.md",
  "description": "Read the task spec"
}
```

> TOOL

tool_result Bash
```
# Two related `megaplan auto` reliability/safety features

Bundled because both touch the auto-driver loop (`megaplan/auto.py`) and its
retry / termination logic. Ship them together so the flag surface is coherent.

## Task A — Auto-retry execute on codex context-window exhaustion

### Problem
When a long persistent codex session exhausts its context window, codex returns
this error text to the worker:

> Codex ran out of room in the model's context window. Start a new thread or
> clear earlier history before retrying.

Current behavior: auto-driver sees `phase 'execute' exited 1`, retries the same
`megaplan execute` subprocess (same session), fails the same way, and after
`--stall-threshold` iterations (default 5) bails with `stalled at state=finalized`.

We saw this IRL: sprint 2 execute completed 14/16 batches (~40 min of work) and
then burned 6 retry iterations + ~4 min of wall time before finally giving up —
requiring manual intervention (`megaplan execute --fresh --plan <name>`).

### Requirement
In `megaplan/auto.py`, when the execute phase exits non-zero AND the captured
subprocess stderr/stdout contains the fragment `"ran out of room in the model's context"`
(case-insensitive), the auto-driver must:

1. Log a clear message that context exhaustion was detected.
2. Re-run the execute phase with `--fresh` appended to the command.
3. Count this as a *separate retry category* — it should NOT count toward the
   normal stall threshold, and it should NOT happen more than `--max-context-retries`
   times per plan (default `2`).
4. If retries are exhausted AND the error keeps occurring, fall through to the
   existing stall logic (don't loop forever).

### CLI
- Add `--max-context-retries N` to `megaplan auto` (default `2`).
- No behavioral change when `N=0` (off).

### Tests
- Mock-subprocess test: execute "fails" with the context-exhaustion fragment in
  its output; auto-driver retries with `--fresh` appended; on second attempt the
  mock returns success; auto reaches terminal `done`.
- Mock-subprocess test: executed 3× with context-exhaustion error; with
  `--max-context-retries 2`, auto-driver stops retrying after the 2nd fresh retry.
- Regression: a generic execute failure (no context-exhaustion fragment) still
  goes through the existing stall-threshold path (not the fresh-retry path).

---

## Task B — Cost cap on `megaplan auto`

### Problem
`megaplan auto` can spend unbounded money. Receipts (Sprint 1) record
`cost_usd` per phase. The `state["history"]` also accumulates per-phase cost.
But nothing uses this for a pre-emptive abort — a runaway plan keeps spending.

### Requirement
Add `--max-cost-usd N` (float) to `megaplan auto`. After every phase subprocess
returns:

1. Sum `cost_usd` across every entry in `state["history"]`.
2. If the sum exceeds `N`, abort the auto loop with a new terminal outcome
   status `cost_cap_exceeded`.
3. Surface the final total and the cap in the outcome JSON so callers can see
   how far over they went on the last phase.
4. Default when unset: no cap (existing behavior).

The check runs *after* each phase completes — so a single phase that blows the
budget on its own still finishes (don't try to abort mid-phase), but the NEXT
phase won't launch.

### CLI
- `megaplan auto --max-cost-usd 5.00` — aborts after any phase pushes cumulative
  spend past $5.00.
- Invalid value (negative, non-numeric): argparse rejects with a clear message.

### Tests
- Mock-subprocess test: per-phase cost 1.00; `--max-cost-usd 2.50` → after phase 3
  the loop aborts with `cost_cap_exceeded` in the outcome.
- Mock-subprocess test: phase returns cost 10.00 (a single expensive phase);
  `--max-cost-usd 5.00` → that phase completes, *next* phase doesn't launch,
  outcome reports `cost_cap_exceeded`.
- Regression: when `--max-cost-usd` is unset, behavior is unchanged (no early
  termination regardless of cost).

---

## Combined success criteria

1. Both flags (`--max-context-retries`, `--max-cost-usd`) appear in
   `megaplan auto --help`.
2. All new tests pass alongside the existing test suite.
3. A manual smoke test with `--max-cost-usd 0.0001` aborts on the first phase
   that costs anything (proves the cap is evaluated after every phase).
4. A manual smoke test with a mock executor that emits the context-exhaustion
   error verifies the `--fresh` retry path actually runs.
5. The outcome JSON for both abort paths contains the new terminal status
   string (`cost_cap_exceeded` or `context_retry_exhausted`) and the full
   cost / retry counts.

## Out of scope

- Mid-phase cost limiting (cancelling a running subprocess).
- Retry strategies for non-context errors (e.g. rate limits, network).
- Cost prediction / forecasting before a phase runs.
- Cross-plan budgeting (per-plan only, not global).
```

> TOOL

tool_use Bash
```json
{
  "command": "cat /Users/user_c042661f/Documents/megaplan/.megaplan/bakeoffs/reliability-20260424-235843/bakeoff.json",
  "description": "Read bakeoff manifest"
}
```

> TOOL

tool_result Bash
```
{
  "schema_version": 1,
  "experiment_id": "reliability-20260424-235843",
  "base_sha": "5044b7952ab1cd34e9ad76773ed95941b8d00227",
  "idea_hash": "521ee6103e4f96b284460f71457443dd0adf37beb9cbd53ad5e316df3a0356de",
  "idea_path": [REDACTED],
  "mode": "code",
  "profiles": [
    {
      "name": "standard",
      "worktree": [REDACTED],
      "plan_id": "reliability-20260424-235843",
      "pid": 71951,
      "launched_at": "2026-04-24T21:58:48Z",
      "terminated_at": null,
      "outcome": null,
      "log_path": [REDACTED],
      "outcome_path": [REDACTED]
    },
    {
      "name": "all-open",
      "worktree": [REDACTED],
      "plan_id": "reliability-20260424-235843",
      "pid": 71952,
      "launched_at": "2026-04-24T21:58:48Z",
      "terminated_at": null,
      "outcome": null,
      "log_path": [REDACTED],
      "outcome_path": [REDACTED]
    },
    {
      "name": "all-kimi",
      "worktree": [REDACTED],
      "plan_id": "reliability-20260424-235843",
      "pid": 71953,
      "launched_at": "2026-04-24T21:58:48Z",
      "terminated_at": null,
      "outcome": null,
      "log_path": [REDACTED],
      "outcome_path": [REDACTED]
    },
    {
      "name": "all-deepseek",
      "worktree": [REDACTED],
      "plan_id": "reliability-20260424-235843",
      "pid": 71954,
      "launched_at": "2026-04-24T21:58:48Z",
      "terminated_at": null,
      "outcome": null,
      "log_path": [REDACTED],
      "outcome_path": [REDACTED]
    }
  ],
  "phase": "running",
  "chosen_profile": null,
  "merged_at": null,
  "judge_model": null
}
```

> TOOL

tool_use Bash
```json
{
  "command": "for p in standard all-open all-kimi all-deepseek; do echo \"=== $p ===\"; cat /Users/user_c042661f/Documents/megaplan/.megaplan/bakeoffs/reliability-20260424-235843/$p/outcome.json 2>/dev/null || echo \"(no outcome.json)\"; done",
  "description": "Read all profile outcomes"
}
```

> TOOL

tool_result Bash
```
=== standard ===
{
  "status": "done",
  "plan": "reliability-20260424-235843",
  "final_state": "done",
  "iterations": 10,
  "reason": "plan entered terminal state 'done'",
  "last_phase": "review",
  "events": [
    {
      "msg": "iter 1 state=initialized next=plan valid_next=['plan']",
      "iteration": 1,
      "state": "initialized",
      "next_step": "plan",
      "valid_next": [
        "plan"
      ]
    },
    {
      "msg": "running: megaplan plan --plan reliability-20260424-235843",
      "phase": "plan",
      "timeout": 3600
    },
    {
      "msg": "iter 2 state=planned next=critique valid_next=['critique', 'plan', 'step']",
      "iteration": 2,
      "state": "planned",
      "next_step": "critique",
      "valid_next": [
        "critique",
        "plan",
        "step"
      ]
    },
    {
      "msg": "running: megaplan critique --plan reliability-20260424-235843",
      "phase": "critique",
      "timeout": 3600
    },
    {
      "msg": "iter 3 state=critiqued next=gate valid_next=['gate', 'step']",
      "iteration": 3,
      "state": "critiqued",
      "next_step": "gate",
      "valid_next": [
        "gate",
        "step"
      ]
    },
    {
      "msg": "running: megaplan gate --plan reliability-20260424-235843",
      "phase": "gate",
      "timeout": 3600
    },
    {
      "msg": "iter 4 state=critiqued next=revise valid_next=['revise', 'step']",
      "iteration": 4,
      "state": "critiqued",
      "next_step": "revise",
      "valid_next": [
        "revise",
        "step"
      ]
    },
    {
      "msg": "running: megaplan revise --plan reliability-20260424-235843",
      "phase": "revise",
      "timeout": 3600
    },
    {
      "msg": "iter 5 state=planned next=critique valid_next=['critique', 'plan', 'step']",
      "iteration": 5,
      "state": "planned",
      "next_step": "critique",
      "valid_next": [
        "critique",
        "plan",
        "step"
      ]
    },
    {
      "msg": "running: megaplan critique --plan reliability-20260424-235843",
      "phase": "critique",
      "timeout": 3600
    },
    {
      "msg": "iter 6 state=critiqued next=gate valid_next=['gate', 'step']",
      "iteration": 6,
      "state": "critiqued",
      "next_step": "gate",
      "valid_next": [
        "gate",
        "step"
      ]
    },
    {
      "msg": "running: megaplan gate --plan reliability-20260424-235843",
      "phase": "gate",
      "timeout": 3600
    },
    {
      "msg": "iter 7 state=gated next=finalize valid_next=['finalize', 'override replan', 'step']",
      "iteration": 7,
      "state": "gated",
      "next_step": "finalize",
      "valid_next": [
        "finalize",
        "override replan",
        "step"
      ]
    },
    {
      "msg": "running: megaplan finalize --plan reliability-20260424-235843",
      "phase": "finalize",
      "timeout": 3600
    },
    {
      "msg": "iter 8 state=finalized next=execute valid_next=['execute', 'override replan', 'step']",
      "iteration": 8,
      "state": "finalized",
      "next_step": "execute",
      "valid_next": [
        "execute",
        "override replan",
        "step"
      ]
    },
    {
      "msg": "running: megaplan execute --confirm-destructive --user-approved --plan reliability-20260424-235843",
      "phase": "execute",
      "timeout": 3600
    },
    {
      "msg": "iter 9 state=executed next=review valid_next=['review']",
      "iteration": 9,
      "state": "executed",
      "next_step": "review",
      "valid_next": [
        "review"
      ]
    },
    {
      "msg": "running: megaplan review --plan reliability-20260424-235843",
      "phase": "review",
      "timeout": 3600
    },
    {
      "msg": "iter 10 state=done next=None valid_next=[]",
      "iteration": 10,
      "state": "done",
      "next_step": null,
      "valid_next": []
    },
    {
      "msg": "terminal state reached: done"
    }
  ]
}=== all-open ===
{
  "status": "stalled",
  "plan": "reliability-20260424-235843",
  "final_state": "finalized",
  "iterations": 17,
  "reason": "stalled at state=finalized for 5 iterations (auto-driver retried execute but state did not transition; partial work persisted in worktree)",
  "last_phase": "execute",
  "events": []
}=== all-kimi ===
{
  "status": "stalled",
  "plan": "reliability-20260424-235843",
  "final_state": "finalized",
  "iterations": 13,
  "reason": "stalled at state=finalized for 5 iterations (auto-driver retried execute but state did not transition; partial work persisted in worktree)",
  "last_phase": "execute",
  "events": []
}=== all-deepseek ===
(no outcome.json)
```

> TOOL

tool_use Bash
```json
{
  "command": "for p in standard all-open all-kimi; do echo \"=== $p ===\"; git -C /Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/$p diff HEAD --stat 2>&1; done",
  "description": "Get diff stats per profile"
}
```

> TOOL

tool_result Bash
```
=== standard ===
 megaplan/auto.py                    | 243 ++++++++++++++++------
 tests/test_auto.py                  | 393 +++++++++++++++++++++++++++++++++++-
 tests/test_cloud_local_lifecycle.py |  21 +-
 tests/test_workers.py               |   4 +-
 4 files changed, 597 insertions(+), 64 deletions(-)
=== all-open ===
 megaplan/auto.py                            | 132 ++++++++-
 megaplan/chain.py                           |  16 +-
 megaplan/cloud/templates/chain.yaml.example |   2 +
 megaplan/handlers/init.py                   |   4 +
 tests/test_auto.py                          | 404 ++++++++++++++++++++++++++++
 tests/test_core_without_cloud.py            |   5 +
 tests/test_handle_init_idea_file.py         |   4 +
 7 files changed, 565 insertions(+), 2 deletions(-)
=== all-kimi ===
 megaplan/auto.py                            | 184 ++++++++++++-
 megaplan/chain.py                           |  15 ++
 megaplan/cloud/templates/chain.yaml.example |   3 +
 megaplan/handlers/init.py                   |   3 +
 tests/test_auto.py                          | 387 +++++++++++++++++++++++++++-
 tests/test_chain.py                         |  43 ++++
 tests/test_core_without_cloud.py            |   4 +
 tests/test_handle_init_idea_file.py         |   3 +
 8 files changed, 636 insertions(+), 6 deletions(-)
```

> AGENT

Now let me get the actual diffs for each profile.

> TOOL

tool_use Bash
```json
{
  "command": "git -C /Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/standard diff HEAD -- megaplan/auto.py",
  "description": "Standard profile auto.py diff"
}
```

> TOOL

tool_result Bash
```
diff --git a/megaplan/auto.py b/megaplan/auto.py
index 744984e8..340d8aef 100644
--- a/megaplan/auto.py
+++ b/megaplan/auto.py
@@ -29,7 +29,6 @@ from megaplan.types import (
     STATE_AWAITING_HUMAN,
     STATE_TIEBREAKER_PENDING,
     STATE_TIEBREAKER_READY,
-    TERMINAL_STATES,
 )
 
 
@@ -38,6 +37,8 @@ DEFAULT_MAX_ITERATIONS = 200
 DEFAULT_POLL_SLEEP_SECONDS = 1.0
 DEFAULT_PHASE_TIMEOUT_SECONDS = 3600
 DEFAULT_STATUS_TIMEOUT_SECONDS = 60
+DEFAULT_MAX_CONTEXT_RETRIES = 2
+CONTEXT_EXHAUSTION_FRAGMENT = "ran out of room in the model's context"
 # Cap on review→rework cycles before the driver bails. This mirrors the
 # `execution.max_review_rework_cycles` config the review handler enforces
 # internally (default 3); the auto-driver applies its own cap so that an
@@ -51,13 +52,17 @@ PHASE_TIMEOUT_EXIT_CODE = 124  # conventional; matches GNU `timeout`
 class DriverOutcome:
     """Terminal outcome reported when the loop exits."""
 
-    status: str  # "done" | "stalled" | "escalated" | "failed" | "aborted" | "cap" | "blocked"
+    status: str  # "done" | "stalled" | "escalated" | "failed" | "aborted" | "cap" | "blocked" | "cost_cap_exceeded" | "context_retry_exhausted"
     plan: str
     final_state: str
     iterations: int
     reason: str = ""
     last_phase: str | None = None
     events: list[dict[str, Any]] = field(default_factory=list)
+    total_cost_usd: float | None = None
+    cost_cap_usd: float | None = None
+    context_retries_used: int = 0
+    max_context_retries: int | None = None
 
     def to_json(self) -> str:
         return json.dumps(
@@ -69,11 +74,35 @@ class DriverOutcome:
                 "reason": self.reason,
                 "last_phase": self.last_phase,
                 "events": self.events,
+                "total_cost_usd": self.total_cost_usd,
+                "cost_cap_usd": self.cost_cap_usd,
+                "context_retries_used": self.context_retries_used,
+                "max_context_retries": self.max_context_retries,
             },
             indent=2,
         )
 
 
+def _non_negative_int(value: str) -> int:
+    try:
+        parsed = int(value)
+    except ValueError as error:
+        raise argparse.ArgumentTypeError(f"invalid non-negative integer: {value}") from error
+    if parsed < 0:
+        raise argparse.ArgumentTypeError("value must be non-negative")
+    return parsed
+
+
+def _non_negative_float(value: str) -> float:
+    try:
+        parsed = float(value)
+    except ValueError as error:
+        raise argparse.ArgumentTypeError(f"invalid non-negative float: {value}") from error
+    if parsed < 0:
+        raise argparse.ArgumentTypeError("value must be non-negative")
+    return parsed
+
+
 def _run_megaplan(
     args: list[str],
     *,
@@ -152,6 +181,30 @@ def _resolve_plan_dir(plan: str, cwd: Path | None) -> Path | None:
     return None
 
 
+def _sum_history_cost_usd(plan_dir: Path | None) -> float:
+    if plan_dir is None:
+        return 0.0
+
+    try:
+        with (plan_dir / "state.json").open(encoding="utf-8") as handle:
+            state_data = json.load(handle)
+    except (OSError, json.JSONDecodeError):
+        return 0.0
+
+    if not isinstance(state_data, dict):
+        return 0.0
+
+    total = 0.0
+    for entry in state_data.get("history") or []:
+        if not isinstance(entry, dict):
+            continue
+        try:
+            total += float(entry.get("cost_usd", 0.0) or 0.0)
+        except (TypeError, ValueError):
+            continue
+    return round(total, 6)
+
+
 def _get_review_marker(plan_dir: Path | None) -> float | None:
     """Return a monotonically-advancing marker for the current review cycle.
 
@@ -181,6 +234,8 @@ def drive(
     stall_threshold: int = DEFAULT_STALL_THRESHOLD,
     max_iterations: int = DEFAULT_MAX_ITERATIONS,
     max_review_rework_cycles: int = DEFAULT_MAX_REVIEW_REWORK_CYCLES,
+    max_cost_usd: float | None = None,
+    max_context_retries: int = DEFAULT_MAX_CONTEXT_RETRIES,
     on_escalate: str = "force-proceed",
     poll_sleep: float = DEFAULT_POLL_SLEEP_SECONDS,
     phase_timeout: float = DEFAULT_PHASE_TIMEOUT_SECONDS,
@@ -200,6 +255,7 @@ def drive(
     last_state: str | None = None
     stall_count = 0
     last_phase: str | None = None
+    context_retry_count = 0
 
     # Rework-cycle tracking. When review returns `needs_rework`, the plan
     # ping-pongs `finalized ↔ executed ↔ finalized` while execute re-runs
@@ -215,22 +271,63 @@ def drive(
         events.append({"msg": msg, **fields})
         writer(f"[auto {plan}] {msg}\n")
 
+    def _outcome(
+        status: str,
+        *,
+        final_state: str,
+        iterations: int,
+        reason: str = "",
+        last_phase: str | None = None,
+    ) -> DriverOutcome:
+        return DriverOutcome(
+            status=status,
+            plan=plan,
+            final_state=final_state,
+            iterations=iterations,
+            reason=reason,
+            last_phase=last_phase,
+            events=events,
+            total_cost_usd=_sum_history_cost_usd(plan_dir),
+            cost_cap_usd=max_cost_usd,
+            context_retries_used=context_retry_count,
+            max_context_retries=max_context_retries,
+        )
+
     for iteration in range(1, max_iterations + 1):
         try:
             status = _status(plan, cwd=cwd, timeout=status_timeout)
         except (RuntimeError, json.JSONDecodeError) as error:
             log(f"status lookup failed: {error}")
-            return DriverOutcome(
-                status="failed",
-                plan=plan,
+            return _outcome(
+                "failed",
                 final_state=last_state or "unknown",
                 iterations=iteration,
                 reason=str(error),
                 last_phase=last_phase,
-                events=events,
             )
 
         state = status.get("state", "")
+
+        if max_cost_usd is not None:
+            cumulative = _sum_history_cost_usd(plan_dir)
+            if cumulative > max_cost_usd:
+                log(
+                    f"cost cap exceeded after phase '{last_phase}': "
+                    f"total_cost_usd={cumulative} > cost_cap_usd={max_cost_usd}",
+                    total_cost_usd=cumulative,
+                    cost_cap_usd=max_cost_usd,
+                )
+                return _outcome(
+                    "cost_cap_exceeded",
+                    final_state=state,
+                    iterations=iteration,
+                    reason=(
+                        f"cost cap exceeded after phase '{last_phase}': "
+                        f"{cumulative} > {max_cost_usd}"
+                    ),
+                    last_phase=last_phase,
+                )
+
         next_step = status.get("next_step")
         valid_next = status.get("valid_next") or []
 
@@ -246,46 +343,38 @@ def drive(
         if state in AUTOMATION_TERMINAL_STATES:
             if state == STATE_AWAITING_HUMAN:
                 log("plan awaiting human verification — automation stopping")
-                return DriverOutcome(
-                    status="awaiting_human",
-                    plan=plan,
+                return _outcome(
+                    "awaiting_human",
                     final_state=state,
                     iterations=iteration,
                     reason="plan has criteria requiring human verification",
                     last_phase=last_phase,
-                    events=events,
                 )
             if state == STATE_TIEBREAKER_PENDING:
                 log("tiebreaker pending — run 'megaplan tiebreaker-run --plan <name>' to execute")
-                return DriverOutcome(
-                    status="tiebreaker_pending",
-                    plan=plan,
+                return _outcome(
+                    "tiebreaker_pending",
                     final_state=state,
                     iterations=iteration,
                     reason="gate recommended tiebreaker — researcher/challenger run needed",
                     last_phase=last_phase,
-                    events=events,
                 )
             if state == STATE_TIEBREAKER_READY:
                 log("tiebreaker ready — run 'megaplan tiebreaker decide --plan <name>' to resolve")
-                return DriverOutcome(
-                    status="tiebreaker_ready",
-                    plan=plan,
+                return _outcome(
+                    "tiebreaker_ready",
                     final_state=state,
                     iterations=iteration,
                     reason="tiebreaker synthesis complete — awaiting human decision",
                     last_phase=last_phase,
-                    events=events,
                 )
             log(f"terminal state reached: {state}")
-            return DriverOutcome(
-                status="done" if state == "done" else "aborted",
-                plan=plan,
+            return _outcome(
+                "done" if state == "done" else "aborted",
                 final_state=state,
                 iterations=iteration,
                 reason=f"plan entered terminal state '{state}'",
                 last_phase=last_phase,
-                events=events,
             )
 
         # Review-cycle progress: a fresh review.json means a real review
@@ -318,9 +407,8 @@ def drive(
                     f"observed {rework_cycles_observed} rework cycles "
                     f"(cap={max_review_rework_cycles}) — bailing"
                 )
-                return DriverOutcome(
-                    status="stalled",
-                    plan=plan,
+                return _outcome(
+                    "stalled",
                     final_state=state,
                     iterations=iteration,
                     reason=(
@@ -330,7 +418,6 @@ def drive(
                         "returning needs_rework without resolving"
                     ),
                     last_phase=last_phase,
-                    events=events,
                 )
 
         # Stall detection: same state for stall_threshold+ iterations.
@@ -350,9 +437,8 @@ def drive(
                         f"all pending tasks reported status=blocked "
                         f"({tasks_blocked} blocked) — treating as poisoned outcome"
                     )
-                    return DriverOutcome(
-                        status="blocked",
-                        plan=plan,
+                    return _outcome(
+                        "blocked",
                         final_state=state,
                         iterations=iteration,
                         reason=(
@@ -360,12 +446,10 @@ def drive(
                             "or the environment may genuinely be broken"
                         ),
                         last_phase=last_phase,
-                        events=events,
                     )
                 log(f"stalled at state={state} for {stall_count} iterations")
-                return DriverOutcome(
-                    status="stalled",
-                    plan=plan,
+                return _outcome(
+                    "stalled",
                     final_state=state,
                     iterations=iteration,
                     reason=(
@@ -373,7 +457,6 @@ def drive(
                         "manual intervention required"
                     ),
                     last_phase=last_phase,
-                    events=events,
                 )
         else:
             stall_count = 0
@@ -398,14 +481,12 @@ def drive(
                     )
                     if code != 0:
                         log(f"force-proceed failed (exit {code}): {err.strip() or out.strip()}")
-                        return DriverOutcome(
-                            status="failed",
-                            plan=plan,
+                        return _outcome(
+                            "failed",
                             final_state=state,
                             iterations=iteration,
                             reason=f"override force-proceed exited {code}",
                             last_phase=last_phase,
-                            events=events,
                         )
                     continue
                 if on_escalate == "abort":
@@ -422,35 +503,29 @@ def drive(
                         cwd=cwd,
                         timeout=status_timeout,
                     )
-                    return DriverOutcome(
-                        status="aborted",
-                        plan=plan,
+                    return _outcome(
+                        "aborted",
                         final_state=state,
                         iterations=iteration,
                         reason="gate escalated and on_escalate=abort",
                         last_phase=last_phase,
-                        events=events,
                     )
                 # on_escalate == "fail"
                 log("gate escalated — failing (per on_escalate=fail)")
-                return DriverOutcome(
-                    status="escalated",
-                    plan=plan,
+                return _outcome(
+                    "escalated",
                     final_state=state,
                     iterations=iteration,
                     reason="gate escalated and on_escalate=fail — human required",
                     last_phase=last_phase,
-                    events=events,
                 )
             log(f"no next_step and no override available (valid_next={valid_next})")
-            return DriverOutcome(
-                status="failed",
-                plan=plan,
+            return _outcome(
+                "failed",
                 final_state=state,
                 iterations=iteration,
                 reason="no next_step and no override available",
                 last_phase=last_phase,
-                events=events,
             )
 
         # Run the next phase.
@@ -458,6 +533,39 @@ def drive(
         log(f"running: megaplan {' '.join(cmd)}", phase=next_step, timeout=phase_timeout)
         last_phase = next_step
         code, out, err = _run_megaplan(cmd, cwd=cwd, timeout=phase_timeout)
+        if max_context_retries > 0:
+            while (
+                next_step == "execute"
+                and code != 0
+                and CONTEXT_EXHAUSTION_FRAGMENT.lower() in ((out or "") + (err or "")).lower()
+            ):
+                if context_retry_count >= max_context_retries:
+                    log(
+                        f"context exhaustion retry cap reached ({max_context_retries}) — bailing",
+                        context_retries_used=context_retry_count,
+                        max_context_retries=max_context_retries,
+                    )
+                    return _outcome(
+                        "context_retry_exhausted",
+                        final_state=state,
+                        iterations=iteration,
+                        reason=(
+                            f"context exhaustion retry cap reached "
+                            f"({context_retry_count}/{max_context_retries})"
+                        ),
+                        last_phase=last_phase,
+                    )
+                log(
+                    "context exhaustion detected — retrying execute with "
+                    f"--fresh (retry {context_retry_count + 1}/{max_context_retries})",
+                    context_retries_used=context_retry_count,
+                    max_context_retries=max_context_retries,
+                    next_context_retry=context_retry_count + 1,
+                )
+                context_retry_count += 1
+                if "--fresh" not in cmd:
+                    cmd = [*cmd, "--fresh"]
+                code, out, err = _run_megaplan(cmd, cwd=cwd, timeout=phase_timeout)
         if code == PHASE_TIMEOUT_EXIT_CODE:
             log(f"phase '{next_step}' timed out after {phase_timeout}s — stall detection will enforce the cap")
         elif code != 0:
@@ -470,14 +578,12 @@ def drive(
 
     # Hit iteration cap.
     log(f"hit max_iterations={max_iterations}")
-    return DriverOutcome(
-        status="cap",
-        plan=plan,
+    return _outcome(
+        "cap",
         final_state=last_state or "unknown",
         iterations=max_iterations,
         reason=f"exceeded max_iterations={max_iterations}",
         last_phase=last_phase,
-        events=events,
     )
 
 
@@ -516,6 +622,24 @@ def build_auto_parser(subparsers: Any) -> None:
             "stuck at 'finalized'. Mirrors execution.max_review_rework_cycles."
         ),
     )
+    auto_parser.add_argument(
+        "--max-cost-usd",
+        type=_non_negative_float,
+        default=None,
+        help=(
+            "Abort automation after cumulative state history cost exceeds this "
+            "USD cap. The check runs after each phase completes (default no cap)."
+        ),
+    )
+    auto_parser.add_argument(
+        "--max-context-retries",
+        type=_non_negative_int,
+        default=DEFAULT_MAX_CONTEXT_RETRIES,
+        help=(
+            f"Fresh execute retries to allow after Codex context-window "
+            f"exhaustion (default {DEFAULT_MAX_CONTEXT_RETRIES}; 0 disables)."
+        ),
+    )
     auto_parser.add_argument(
         "--on-escalate",
         choices=ESCALATE_ACTIONS,
@@ -566,12 +690,16 @@ def run_auto(root: Path, args: argparse.Namespace) -> int:
         stall_threshold=args.stall_threshold,
         max_iterations=args.max_iterations,
         max_review_rework_cycles=args.max_review_rework_cycles,
+        max_cost_usd=args.max_cost_usd,
+        max_context_retries=args.max_context_retries,
         on_escalate=args.on_escalate,
         poll_sleep=args.poll_sleep,
         phase_timeout=args.phase_timeout,
         status_timeout=args.status_timeout,
     )
     sys.stdout.write(outcome.to_json() + "\n")
+    # Exit codes: 0 done/aborted, 1 failed/unknown, 2 stalled, 3 escalated,
+    # 4 iteration cap, 5 blocked, 6 cost cap exceeded, 7 context retry exhausted.
     if outcome.status == "done":
         return 0
     if outcome.status == "aborted":
@@ -582,9 +710,10 @@ def run_auto(root: Path, args: argparse.Namespace) -> int:
         return 3
     if outcome.status == "cap":
         return 4
-    # rc=3 is already claimed by 'escalated'; use rc=5 for all-blocked so the
-    # supervisor can distinguish "workers said every task is blocked" from a
-    # generic stall or escalation.
     if outcome.status == "blocked":
         return 5
+    if outcome.status == "cost_cap_exceeded":
+        return 6
+    if outcome.status == "context_retry_exhausted":
+        return 7
     return 1
```

> TOOL

tool_use Bash
```json
{
  "command": "git -C /Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-open diff HEAD -- megaplan/auto.py",
  "description": "All-open profile auto.py diff"
}
```

> TOOL

tool_result Bash
```
diff --git a/megaplan/auto.py b/megaplan/auto.py
index 744984e8..b1c2e35e 100644
--- a/megaplan/auto.py
+++ b/megaplan/auto.py
@@ -43,6 +43,7 @@ DEFAULT_STATUS_TIMEOUT_SECONDS = 60
 # internally (default 3); the auto-driver applies its own cap so that an
 # unexpected-config or mis-routed rework loop cannot spin indefinitely.
 DEFAULT_MAX_REVIEW_REWORK_CYCLES = 3
+DEFAULT_MAX_CONTEXT_RETRIES = 2
 ESCALATE_ACTIONS = ("force-proceed", "abort", "fail")
 PHASE_TIMEOUT_EXIT_CODE = 124  # conventional; matches GNU `timeout`
 
@@ -51,13 +52,17 @@ PHASE_TIMEOUT_EXIT_CODE = 124  # conventional; matches GNU `timeout`
 class DriverOutcome:
     """Terminal outcome reported when the loop exits."""
 
-    status: str  # "done" | "stalled" | "escalated" | "failed" | "aborted" | "cap" | "blocked"
+    status: str  # "done" | "stalled" | "escalated" | "failed" | "aborted" | "cap" | "blocked" | "cost_cap_exceeded" | "context_retry_exhausted"
     plan: str
     final_state: str
     iterations: int
     reason: str = ""
     last_phase: str | None = None
     events: list[dict[str, Any]] = field(default_factory=list)
+    total_cost_usd: float = 0.0
+    max_cost_usd: float | None = None
+    context_retries_used: int = 0
+    max_context_retries: int = 0
 
     def to_json(self) -> str:
         return json.dumps(
@@ -69,6 +74,10 @@ class DriverOutcome:
                 "reason": self.reason,
                 "last_phase": self.last_phase,
                 "events": self.events,
+                "total_cost_usd": self.total_cost_usd,
+                "max_cost_usd": self.max_cost_usd,
+                "context_retries_used": self.context_retries_used,
+                "max_context_retries": self.max_context_retries,
             },
             indent=2,
         )
@@ -185,6 +194,8 @@ def drive(
     poll_sleep: float = DEFAULT_POLL_SLEEP_SECONDS,
     phase_timeout: float = DEFAULT_PHASE_TIMEOUT_SECONDS,
     status_timeout: float = DEFAULT_STATUS_TIMEOUT_SECONDS,
+    max_cost_usd: float | None = None,
+    max_context_retries: int = DEFAULT_MAX_CONTEXT_RETRIES,
     writer=sys.stdout.write,
 ) -> DriverOutcome:
     """Drive ``plan`` to completion.
@@ -200,6 +211,7 @@ def drive(
     last_state: str | None = None
     stall_count = 0
     last_phase: str | None = None
+    context_retries_used = 0
 
     # Rework-cycle tracking. When review returns `needs_rework`, the plan
     # ping-pongs `finalized ↔ executed ↔ finalized` while execute re-runs
@@ -286,8 +298,38 @@ def drive(
                 reason=f"plan entered terminal state '{state}'",
                 last_phase=last_phase,
                 events=events,
+                context_retries_used=context_retries_used,
+                max_context_retries=max_context_retries,
             )
 
+        # Cost-cap guard: abort if cumulative spend exceeds the configured cap.
+        # Placed after the terminal-state check so done/aborted are not masked,
+        # and before review-cycle tracking. Guarded by last_phase so it never
+        # fires before any phase has completed.
+        if last_phase is not None and max_cost_usd is not None:
+            total_cost = status.get("total_cost_usd", 0.0)
+            if total_cost > max_cost_usd:
+                log(
+                    f"cost cap exceeded: total_cost_usd={total_cost:.2f} > "
+                    f"max_cost_usd={max_cost_usd:.2f} — aborting"
+                )
+                return DriverOutcome(
+                    status="cost_cap_exceeded",
+                    plan=plan,
+                    final_state=state,
+                    iterations=iteration,
+                    reason=(
+                        f"cumulative cost ${total_cost:.2f} exceeded cap "
+                        f"${max_cost_usd:.2f}"
+                    ),
+                    last_phase=last_phase,
+                    events=events,
+                    total_cost_usd=total_cost,
+                    max_cost_usd=max_cost_usd,
+                    context_retries_used=context_retries_used,
+                    max_context_retries=max_context_retries,
+                )
+
         # Review-cycle progress: a fresh review.json means a real review
         # pass completed since the last iteration. This counts as forward
         # progress even when `state` looks unchanged (finalized→executed→
@@ -374,6 +416,8 @@ def drive(
                     ),
                     last_phase=last_phase,
                     events=events,
+                    context_retries_used=context_retries_used,
+                    max_context_retries=max_context_retries,
                 )
         else:
             stall_count = 0
@@ -465,6 +509,58 @@ def drive(
             # in state.json and the next status() reveals a recoverable valid_next.
             # Stall detection will still kill infinite loops.
             log(f"phase '{next_step}' exited {code}: {err.strip() or out.strip()[-400:]}")
+
+            # Context-exhaustion retry: when codex runs out of room in its
+            # context window, re-running execute with --fresh starts a new
+            # session that can continue from where the old one left off.
+            combined_output = (out + err).lower()
+            if (
+                next_step == "execute"
+                and "ran out of room in the model's context" in combined_output
+                and max_context_retries > 0
+            ):
+                log("context window exhaustion detected — retrying with --fresh")
+                while context_retries_used < max_context_retries:
+                    context_retries_used += 1
+                    log(
+                        f"fresh retry {context_retries_used}/{max_context_retries}",
+                        context_retries_used=context_retries_used,
+                    )
+                    retry_code, retry_out, retry_err = _run_megaplan(
+                        cmd + ["--fresh"], cwd=cwd, timeout=phase_timeout,
+                    )
+                    if retry_code == 0:
+                        log("fresh retry succeeded — continuing main loop")
+                        break
+                    # Check if the retry also failed with context exhaustion
+                    retry_combined = (retry_out + retry_err).lower()
+                    if "ran out of room in the model's context" not in retry_combined:
+                        # Different error — break to normal failure handling;
+                        # stall logic will catch it.
+                        log(
+                            f"fresh retry failed with a different error (exit {retry_code})",
+                        )
+                        break
+                else:
+                    # All retries exhausted with same context error.
+                    log(
+                        f"all {max_context_retries} context retries exhausted — aborting"
+                    )
+                    return DriverOutcome(
+                        status="context_retry_exhausted",
+                        plan=plan,
+                        final_state=state,
+                        iterations=iteration,
+                        reason=(
+                            f"exhausted {max_context_retries} context-exhaustion "
+                            f"retries with --fresh"
+                        ),
+                        last_phase=last_phase,
+                        events=events,
+                        context_retries_used=context_retries_used,
+                        max_context_retries=max_context_retries,
+                    )
+
         if poll_sleep > 0:
             time.sleep(poll_sleep)
 
@@ -478,9 +574,19 @@ def drive(
         reason=f"exceeded max_iterations={max_iterations}",
         last_phase=last_phase,
         events=events,
+        context_retries_used=context_retries_used,
+        max_context_retries=max_context_retries,
     )
 
 
+def _non_negative_float(value: str) -> float:
+    """Argparse type that rejects negative values for float arguments."""
+    f = float(value)
+    if f < 0:
+        raise argparse.ArgumentTypeError(f"value must be non-negative, got {value}")
+    return f
+
+
 def build_auto_parser(subparsers: Any) -> None:
     auto_parser = subparsers.add_parser(
         "auto",
@@ -556,6 +662,24 @@ def build_auto_parser(subparsers: Any) -> None:
             "hitting this indicates serious trouble."
         ),
     )
+    auto_parser.add_argument(
+        "--max-context-retries",
+        type=int,
+        default=DEFAULT_MAX_CONTEXT_RETRIES,
+        help=(
+            f"Max retries with --fresh when codex exhausts its context window "
+            f"(default {DEFAULT_MAX_CONTEXT_RETRIES}). Set to 0 to disable."
+        ),
+    )
+    auto_parser.add_argument(
+        "--max-cost-usd",
+        type=_non_negative_float,
+        default=None,
+        help=(
+            "Abort the auto loop when cumulative cost exceeds this value in USD "
+            "(default: no cap). Must be non-negative."
+        ),
+    )
 
 
 def run_auto(root: Path, args: argparse.Namespace) -> int:
@@ -570,6 +694,8 @@ def run_auto(root: Path, args: argparse.Namespace) -> int:
         poll_sleep=args.poll_sleep,
         phase_timeout=args.phase_timeout,
         status_timeout=args.status_timeout,
+        max_cost_usd=args.max_cost_usd,
+        max_context_retries=args.max_context_retries,
     )
     sys.stdout.write(outcome.to_json() + "\n")
     if outcome.status == "done":
@@ -587,4 +713,8 @@ def run_auto(root: Path, args: argparse.Namespace) -> int:
     # generic stall or escalation.
     if outcome.status == "blocked":
         return 5
+    if outcome.status == "cost_cap_exceeded":
+        return 6
+    if outcome.status == "context_retry_exhausted":
+        return 7
     return 1
```

> TOOL

tool_use Bash
```json
{
  "command": "git -C /Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-kimi diff HEAD -- megaplan/auto.py",
  "description": "All-kimi profile auto.py diff"
}
```

> TOOL

tool_result Bash
```
diff --git a/megaplan/auto.py b/megaplan/auto.py
index 744984e8..61d8ef3a 100644
--- a/megaplan/auto.py
+++ b/megaplan/auto.py
@@ -29,7 +29,6 @@ from megaplan.types import (
     STATE_AWAITING_HUMAN,
     STATE_TIEBREAKER_PENDING,
     STATE_TIEBREAKER_READY,
-    TERMINAL_STATES,
 )
 
 
@@ -43,21 +42,42 @@ DEFAULT_STATUS_TIMEOUT_SECONDS = 60
 # internally (default 3); the auto-driver applies its own cap so that an
 # unexpected-config or mis-routed rework loop cannot spin indefinitely.
 DEFAULT_MAX_REVIEW_REWORK_CYCLES = 3
+DEFAULT_MAX_CONTEXT_RETRIES = 2
 ESCALATE_ACTIONS = ("force-proceed", "abort", "fail")
 PHASE_TIMEOUT_EXIT_CODE = 124  # conventional; matches GNU `timeout`
 
 
+def _non_negative_float(value: str) -> float | None:
+    """Argparse type validator: accepts non-negative floats, rejects negatives."""
+    if value is None:
+        return None
+    try:
+        f = float(value)
+    except ValueError as exc:
+        raise argparse.ArgumentTypeError(f"must be a float, got {value!r}") from exc
+    if f < 0:
+        raise argparse.ArgumentTypeError(f"must be non-negative, got {f}")
+    return f
+
+
 @dataclass
 class DriverOutcome:
     """Terminal outcome reported when the loop exits."""
 
-    status: str  # "done" | "stalled" | "escalated" | "failed" | "aborted" | "cap" | "blocked"
+    # Terminal statuses:
+    # "done" | "stalled" | "escalated" | "failed" | "aborted" | "cap" | "blocked"
+    # | "awaiting_human" | "tiebreaker_pending" | "tiebreaker_ready"
+    # | "cost_cap_exceeded" | "context_retry_exhausted"
+    status: str
     plan: str
     final_state: str
     iterations: int
     reason: str = ""
     last_phase: str | None = None
     events: list[dict[str, Any]] = field(default_factory=list)
+    total_cost_usd: float | None = None
+    max_cost_usd: float | None = None
+    context_retry_count: int = 0
 
     def to_json(self) -> str:
         return json.dumps(
@@ -69,6 +89,9 @@ class DriverOutcome:
                 "reason": self.reason,
                 "last_phase": self.last_phase,
                 "events": self.events,
+                "total_cost_usd": self.total_cost_usd,
+                "max_cost_usd": self.max_cost_usd,
+                "context_retry_count": self.context_retry_count,
             },
             indent=2,
         )
@@ -125,14 +148,18 @@ def _has_valid_next(status: dict[str, Any], action: str) -> bool:
     return action in (status.get("valid_next") or [])
 
 
-def _phase_command(next_step: str) -> list[str]:
+def _phase_command(next_step: str, fresh: bool = False) -> list[str]:
     """Translate a `next_step` from status into the CLI args that run it.
 
     Most phases are one-to-one: next_step == command. Execute adds the
     destructive + user-approved flags because auto-mode implies both.
+    When ``fresh`` is True and the step is ``execute``, append ``--fresh``.
     """
     if next_step == "execute":
-        return ["execute", "--confirm-destructive", "--user-approved"]
+        cmd = ["execute", "--confirm-destructive", "--user-approved"]
+        if fresh:
+            cmd.append("--fresh")
+        return cmd
     return [next_step]
 
 
@@ -185,6 +212,8 @@ def drive(
     poll_sleep: float = DEFAULT_POLL_SLEEP_SECONDS,
     phase_timeout: float = DEFAULT_PHASE_TIMEOUT_SECONDS,
     status_timeout: float = DEFAULT_STATUS_TIMEOUT_SECONDS,
+    max_context_retries: int = DEFAULT_MAX_CONTEXT_RETRIES,
+    max_cost_usd: float | None = None,
     writer=sys.stdout.write,
 ) -> DriverOutcome:
     """Drive ``plan`` to completion.
@@ -200,6 +229,8 @@ def drive(
     last_state: str | None = None
     stall_count = 0
     last_phase: str | None = None
+    context_retry_count = 0
+    pending_fresh = False
 
     # Rework-cycle tracking. When review returns `needs_rework`, the plan
     # ping-pongs `finalized ↔ executed ↔ finalized` while execute re-runs
@@ -211,6 +242,18 @@ def drive(
     last_review_marker = _get_review_marker(plan_dir)
     rework_cycles_observed = 0
 
+    def _compute_total_cost() -> float:
+        if plan_dir is None:
+            return float(status.get("total_cost_usd", 0.0) or 0.0)
+        try:
+            state_data = json.loads((plan_dir / "state.json").read_text(encoding="utf-8"))
+            return sum(
+                float(entry.get("cost_usd", 0.0) or 0.0)
+                for entry in state_data.get("history", [])
+            )
+        except (OSError, json.JSONDecodeError):
+            return float(status.get("total_cost_usd", 0.0) or 0.0)
+
     def log(msg: str, **fields: Any) -> None:
         events.append({"msg": msg, **fields})
         writer(f"[auto {plan}] {msg}\n")
@@ -228,6 +271,9 @@ def drive(
                 reason=str(error),
                 last_phase=last_phase,
                 events=events,
+                total_cost_usd=_compute_total_cost(),
+                max_cost_usd=max_cost_usd,
+                context_retry_count=context_retry_count,
             )
 
         state = status.get("state", "")
@@ -242,6 +288,29 @@ def drive(
             valid_next=valid_next,
         )
 
+        # Cost cap check.
+        total_cost = _compute_total_cost()
+        if max_cost_usd is not None and total_cost > max_cost_usd:
+            log(
+                f"cumulative cost ${total_cost:.4f} exceeds cap ${max_cost_usd:.4f} — aborting",
+                total_cost_usd=total_cost,
+                max_cost_usd=max_cost_usd,
+            )
+            return DriverOutcome(
+                status="cost_cap_exceeded",
+                plan=plan,
+                final_state=state,
+                iterations=iteration,
+                reason=(
+                    f"cumulative cost ${total_cost:.4f} exceeds cap ${max_cost_usd:.4f}"
+                ),
+                last_phase=last_phase,
+                events=events,
+                total_cost_usd=total_cost,
+                max_cost_usd=max_cost_usd,
+                context_retry_count=context_retry_count,
+            )
+
         # Terminal: plan reached a final state (or automation-terminal).
         if state in AUTOMATION_TERMINAL_STATES:
             if state == STATE_AWAITING_HUMAN:
@@ -254,6 +323,9 @@ def drive(
                     reason="plan has criteria requiring human verification",
                     last_phase=last_phase,
                     events=events,
+                    total_cost_usd=_compute_total_cost(),
+                    max_cost_usd=max_cost_usd,
+                    context_retry_count=context_retry_count,
                 )
             if state == STATE_TIEBREAKER_PENDING:
                 log("tiebreaker pending — run 'megaplan tiebreaker-run --plan <name>' to execute")
@@ -265,6 +337,9 @@ def drive(
                     reason="gate recommended tiebreaker — researcher/challenger run needed",
                     last_phase=last_phase,
                     events=events,
+                    total_cost_usd=_compute_total_cost(),
+                    max_cost_usd=max_cost_usd,
+                    context_retry_count=context_retry_count,
                 )
             if state == STATE_TIEBREAKER_READY:
                 log("tiebreaker ready — run 'megaplan tiebreaker decide --plan <name>' to resolve")
@@ -276,6 +351,9 @@ def drive(
                     reason="tiebreaker synthesis complete — awaiting human decision",
                     last_phase=last_phase,
                     events=events,
+                    total_cost_usd=_compute_total_cost(),
+                    max_cost_usd=max_cost_usd,
+                    context_retry_count=context_retry_count,
                 )
             log(f"terminal state reached: {state}")
             return DriverOutcome(
@@ -286,6 +364,9 @@ def drive(
                 reason=f"plan entered terminal state '{state}'",
                 last_phase=last_phase,
                 events=events,
+                total_cost_usd=_compute_total_cost(),
+                max_cost_usd=max_cost_usd,
+                context_retry_count=context_retry_count,
             )
 
         # Review-cycle progress: a fresh review.json means a real review
@@ -331,6 +412,9 @@ def drive(
                     ),
                     last_phase=last_phase,
                     events=events,
+                    total_cost_usd=_compute_total_cost(),
+                    max_cost_usd=max_cost_usd,
+                    context_retry_count=context_retry_count,
                 )
 
         # Stall detection: same state for stall_threshold+ iterations.
@@ -361,6 +445,9 @@ def drive(
                         ),
                         last_phase=last_phase,
                         events=events,
+                        total_cost_usd=_compute_total_cost(),
+                        max_cost_usd=max_cost_usd,
+                        context_retry_count=context_retry_count,
                     )
                 log(f"stalled at state={state} for {stall_count} iterations")
                 return DriverOutcome(
@@ -374,6 +461,9 @@ def drive(
                     ),
                     last_phase=last_phase,
                     events=events,
+                    total_cost_usd=_compute_total_cost(),
+                    max_cost_usd=max_cost_usd,
+                    context_retry_count=context_retry_count,
                 )
         else:
             stall_count = 0
@@ -406,6 +496,9 @@ def drive(
                             reason=f"override force-proceed exited {code}",
                             last_phase=last_phase,
                             events=events,
+                            total_cost_usd=_compute_total_cost(),
+                            max_cost_usd=max_cost_usd,
+                            context_retry_count=context_retry_count,
                         )
                     continue
                 if on_escalate == "abort":
@@ -430,6 +523,9 @@ def drive(
                         reason="gate escalated and on_escalate=abort",
                         last_phase=last_phase,
                         events=events,
+                        total_cost_usd=_compute_total_cost(),
+                        max_cost_usd=max_cost_usd,
+                        context_retry_count=context_retry_count,
                     )
                 # on_escalate == "fail"
                 log("gate escalated — failing (per on_escalate=fail)")
@@ -441,6 +537,9 @@ def drive(
                     reason="gate escalated and on_escalate=fail — human required",
                     last_phase=last_phase,
                     events=events,
+                    total_cost_usd=_compute_total_cost(),
+                    max_cost_usd=max_cost_usd,
+                    context_retry_count=context_retry_count,
                 )
             log(f"no next_step and no override available (valid_next={valid_next})")
             return DriverOutcome(
@@ -451,10 +550,14 @@ def drive(
                 reason="no next_step and no override available",
                 last_phase=last_phase,
                 events=events,
+                total_cost_usd=_compute_total_cost(),
+                max_cost_usd=max_cost_usd,
+                context_retry_count=context_retry_count,
             )
 
         # Run the next phase.
-        cmd = _phase_command(next_step) + ["--plan", plan]
+        cmd = _phase_command(next_step, fresh=pending_fresh) + ["--plan", plan]
+        pending_fresh = False
         log(f"running: megaplan {' '.join(cmd)}", phase=next_step, timeout=phase_timeout)
         last_phase = next_step
         code, out, err = _run_megaplan(cmd, cwd=cwd, timeout=phase_timeout)
@@ -465,6 +568,48 @@ def drive(
             # in state.json and the next status() reveals a recoverable valid_next.
             # Stall detection will still kill infinite loops.
             log(f"phase '{next_step}' exited {code}: {err.strip() or out.strip()[-400:]}")
+
+        # Context-exhaustion retry: if execute failed with the known
+        # context-window fragment, retry with --fresh.
+        if code != 0 and last_phase == "execute":
+            combined = (out + err).lower()
+            if "ran out of room in the model's context" in combined:
+                if max_context_retries > 0:
+                    if context_retry_count + 1 > max_context_retries:
+                        log(
+                            f"context-window exhaustion persists after "
+                            f"{max_context_retries} fresh retries — giving up",
+                            context_retry_count=context_retry_count,
+                        )
+                        return DriverOutcome(
+                            status="context_retry_exhausted",
+                            plan=plan,
+                            final_state=state,
+                            iterations=iteration,
+                            reason=(
+                                f"context-window exhaustion after {max_context_retries} "
+                                f"fresh retries exhausted — manual intervention required"
+                            ),
+                            last_phase=last_phase,
+                            events=events,
+                            total_cost_usd=_compute_total_cost(),
+                            max_cost_usd=max_cost_usd,
+                            context_retry_count=context_retry_count,
+                        )
+                    log(
+                        f"context-window exhaustion detected "
+                        f"(retry {context_retry_count + 1}/{max_context_retries}) — "
+                        f"will re-run execute with --fresh",
+                        context_retry_count=context_retry_count + 1,
+                    )
+                    context_retry_count += 1
+                    pending_fresh = True
+                    stall_count = 0
+                    last_state = None
+                    if poll_sleep > 0:
+                        time.sleep(poll_sleep)
+                    continue
+
         if poll_sleep > 0:
             time.sleep(poll_sleep)
 
@@ -478,6 +623,9 @@ def drive(
         reason=f"exceeded max_iterations={max_iterations}",
         last_phase=last_phase,
         events=events,
+        total_cost_usd=_compute_total_cost(),
+        max_cost_usd=max_cost_usd,
+        context_retry_count=context_retry_count,
     )
 
 
@@ -556,6 +704,26 @@ def build_auto_parser(subparsers: Any) -> None:
             "hitting this indicates serious trouble."
         ),
     )
+    auto_parser.add_argument(
+        "--max-context-retries",
+        type=int,
+        default=DEFAULT_MAX_CONTEXT_RETRIES,
+        help=(
+            f"Max retries when the execute phase fails due to a model context-window "
+            f"exhaustion error (default {DEFAULT_MAX_CONTEXT_RETRIES}). Each retry "
+            "re-runs execute with --fresh. Set to 0 to disable."
+        ),
+    )
+    auto_parser.add_argument(
+        "--max-cost-usd",
+        type=_non_negative_float,
+        default=None,
+        help=(
+            "Abort after any phase pushes cumulative spend past this USD cap. "
+            "The phase that exceeds the cap is allowed to finish; the next phase "
+            "does not launch."
+        ),
+    )
 
 
 def run_auto(root: Path, args: argparse.Namespace) -> int:
@@ -570,6 +738,8 @@ def run_auto(root: Path, args: argparse.Namespace) -> int:
         poll_sleep=args.poll_sleep,
         phase_timeout=args.phase_timeout,
         status_timeout=args.status_timeout,
+        max_context_retries=args.max_context_retries,
+        max_cost_usd=args.max_cost_usd,
     )
     sys.stdout.write(outcome.to_json() + "\n")
     if outcome.status == "done":
@@ -587,4 +757,8 @@ def run_auto(root: Path, args: argparse.Namespace) -> int:
     # generic stall or escalation.
     if outcome.status == "blocked":
         return 5
+    if outcome.status == "cost_cap_exceeded":
+        return 6
+    if outcome.status == "context_retry_exhausted":
+        return 7
     return 1
```

> AGENT

The task tools aren't relevant for this read-only audit task. Let me investigate the scope drift in all-open and all-kimi (extra files touched), plus cost data and stall info.

> TOOL

tool_use Bash
```json
{
  "command": "git -C /Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-open diff HEAD -- megaplan/chain.py megaplan/handlers/init.py megaplan/cloud/templates/chain.yaml.example",
  "description": "All-open scope drift files"
}
```

> TOOL

tool_result Bash
```
diff --git a/megaplan/chain.py b/megaplan/chain.py
index 6bb6436c..8ffcfca8 100644
--- a/megaplan/chain.py
+++ b/megaplan/chain.py
@@ -45,6 +45,7 @@ except ImportError as exc:  # pragma: no cover - import guard
     ) from exc
 
 from megaplan.auto import (
+    DEFAULT_MAX_CONTEXT_RETRIES,
     DEFAULT_MAX_ITERATIONS,
     DEFAULT_PHASE_TIMEOUT_SECONDS,
     DEFAULT_POLL_SLEEP_SECONDS,
@@ -96,6 +97,8 @@ class ChainSpec:
     poll_sleep: float = DEFAULT_POLL_SLEEP_SECONDS
     phase_timeout: float = DEFAULT_PHASE_TIMEOUT_SECONDS
     status_timeout: float = DEFAULT_STATUS_TIMEOUT_SECONDS
+    max_cost_usd: float | None = None
+    max_context_retries: int = DEFAULT_MAX_CONTEXT_RETRIES
     escalate_action: str = "force-proceed"  # passed to auto.drive on_escalate
     robustness: str = "standard"
     auto_approve: bool = True
@@ -152,6 +155,13 @@ class ChainSpec:
         if not isinstance(robustness, str):
             raise CliError("invalid_spec", "driver.robustness must be a string")
         auto_approve = bool(driver_raw.get("auto_approve", True))
+        max_cost_raw = driver_raw.get("max_cost_usd")
+        max_cost_usd: float | None = float(max_cost_raw) if max_cost_raw is not None else None
+        if max_cost_usd is not None and max_cost_usd < 0:
+            raise CliError("invalid_spec", "driver.max_cost_usd must be non-negative")
+        max_context_retries = int(driver_raw.get("max_context_retries", DEFAULT_MAX_CONTEXT_RETRIES))
+        if max_context_retries < 0:
+            raise CliError("invalid_spec", "driver.max_context_retries must be non-negative")
 
         return cls(
             milestones=milestones,
@@ -163,6 +173,8 @@ class ChainSpec:
             poll_sleep=poll,
             phase_timeout=phase_to,
             status_timeout=status_to,
+            max_cost_usd=max_cost_usd,
+            max_context_retries=max_context_retries,
             escalate_action=esc,
             robustness=robustness,
             auto_approve=auto_approve,
@@ -361,6 +373,8 @@ def _drive_plan(
         poll_sleep=spec.poll_sleep,
         phase_timeout=spec.phase_timeout,
         status_timeout=spec.status_timeout,
+        max_cost_usd=spec.max_cost_usd,
+        max_context_retries=spec.max_context_retries,
         writer=writer,
     )
 
@@ -388,7 +402,7 @@ def _handle_outcome(
         writer(f"[chain] plan {outcome.plan} escalated — applying on_escalate policy\n")
         policy = spec.on_escalate
     else:
-        # failed, stalled, cap → treat as failure
+        # failed, stalled, cap, cost_cap_exceeded, context_retry_exhausted → treat as failure
         writer(f"[chain] plan {outcome.plan} ended {status}: {outcome.reason}\n")
         policy = spec.on_failure
     if policy == "stop_chain":
diff --git a/megaplan/cloud/templates/chain.yaml.example b/megaplan/cloud/templates/chain.yaml.example
index a7181fc5..65574582 100644
--- a/megaplan/cloud/templates/chain.yaml.example
+++ b/megaplan/cloud/templates/chain.yaml.example
@@ -35,3 +35,5 @@ driver:
   on_escalate: force-proceed  # force-proceed | abort | fail
   robustness: standard
   auto_approve: true
+  # max_cost_usd: 10.0        # Abort when cumulative spend exceeds this USD value (default: no cap)
+  # max_context_retries: 2     # Max --fresh retries on codex context exhaustion (default 2, set 0 to disable)
diff --git a/megaplan/handlers/init.py b/megaplan/handlers/init.py
index b0353993..2991b5e2 100644
--- a/megaplan/handlers/init.py
+++ b/megaplan/handlers/init.py
@@ -179,6 +179,10 @@ def handle_init(root: Path, args: argparse.Namespace) -> StepResponse:
             "reason": outcome.reason,
             "last_phase": outcome.last_phase,
             "events": outcome.events,
+            "total_cost_usd": outcome.total_cost_usd,
+            "max_cost_usd": outcome.max_cost_usd,
+            "context_retries_used": outcome.context_retries_used,
+            "max_context_retries": outcome.max_context_retries,
         }
     _attach_next_step_runtime(response)
     return response
```

> TOOL

tool_use Bash
```json
{
  "command": "git -C /Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-kimi diff HEAD -- megaplan/chain.py megaplan/handlers/init.py megaplan/cloud/templates/chain.yaml.example",
  "description": "All-kimi scope drift files"
}
```

> TOOL

tool_result Bash
```
diff --git a/megaplan/chain.py b/megaplan/chain.py
index 6bb6436c..b8af68a8 100644
--- a/megaplan/chain.py
+++ b/megaplan/chain.py
@@ -45,6 +45,7 @@ except ImportError as exc:  # pragma: no cover - import guard
     ) from exc
 
 from megaplan.auto import (
+    DEFAULT_MAX_CONTEXT_RETRIES,
     DEFAULT_MAX_ITERATIONS,
     DEFAULT_PHASE_TIMEOUT_SECONDS,
     DEFAULT_POLL_SLEEP_SECONDS,
@@ -99,6 +100,8 @@ class ChainSpec:
     escalate_action: str = "force-proceed"  # passed to auto.drive on_escalate
     robustness: str = "standard"
     auto_approve: bool = True
+    max_context_retries: int = DEFAULT_MAX_CONTEXT_RETRIES
+    max_cost_usd: float | None = None
 
     @classmethod
     def from_dict(cls, raw: dict[str, Any]) -> "ChainSpec":
@@ -152,6 +155,10 @@ class ChainSpec:
         if not isinstance(robustness, str):
             raise CliError("invalid_spec", "driver.robustness must be a string")
         auto_approve = bool(driver_raw.get("auto_approve", True))
+        max_ctx = int(driver_raw.get("max_context_retries", DEFAULT_MAX_CONTEXT_RETRIES))
+        max_cost = driver_raw.get("max_cost_usd")
+        if max_cost is not None:
+            max_cost = float(max_cost)
 
         return cls(
             milestones=milestones,
@@ -166,6 +173,8 @@ class ChainSpec:
             escalate_action=esc,
             robustness=robustness,
             auto_approve=auto_approve,
+            max_context_retries=max_ctx,
+            max_cost_usd=max_cost,
         )
 
 
@@ -361,6 +370,8 @@ def _drive_plan(
         poll_sleep=spec.poll_sleep,
         phase_timeout=spec.phase_timeout,
         status_timeout=spec.status_timeout,
+        max_context_retries=spec.max_context_retries,
+        max_cost_usd=spec.max_cost_usd,
         writer=writer,
     )
 
@@ -379,6 +390,10 @@ def _handle_outcome(
     status = outcome.status
     if status == "done":
         return "advance"
+    # Hard safety limits are non-retryable regardless of on_failure policy.
+    if status in ("cost_cap_exceeded", "context_retry_exhausted"):
+        writer(f"[chain] plan {outcome.plan} ended {status}: {outcome.reason}\n")
+        return "stop"
     if status == "aborted":
         # auto.drive returns aborted both for user aborts and on-escalate=abort.
         # Treat according to on_escalate policy so the chain can skip if asked.
diff --git a/megaplan/cloud/templates/chain.yaml.example b/megaplan/cloud/templates/chain.yaml.example
index a7181fc5..797dad29 100644
--- a/megaplan/cloud/templates/chain.yaml.example
+++ b/megaplan/cloud/templates/chain.yaml.example
@@ -35,3 +35,6 @@ driver:
   on_escalate: force-proceed  # force-proceed | abort | fail
   robustness: standard
   auto_approve: true
+  # Safety switches added in v0.x.x
+  max_context_retries: 2   # fresh execute retries on codex context-window exhaustion (0 = off)
+  max_cost_usd: null      # cumulative spend cap in USD; null means unlimited
diff --git a/megaplan/handlers/init.py b/megaplan/handlers/init.py
index b0353993..70b189be 100644
--- a/megaplan/handlers/init.py
+++ b/megaplan/handlers/init.py
@@ -179,6 +179,9 @@ def handle_init(root: Path, args: argparse.Namespace) -> StepResponse:
             "reason": outcome.reason,
             "last_phase": outcome.last_phase,
             "events": outcome.events,
+            "total_cost_usd": outcome.total_cost_usd,
+            "max_cost_usd": outcome.max_cost_usd,
+            "context_retry_count": outcome.context_retry_count,
         }
     _attach_next_step_runtime(response)
     return response
```

> AGENT

Now let me check the auto.log files for the stalled profiles plus cost data and execution.json.

> TOOL

tool_use Bash
```json
{
  "command": "cat /Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-open/.megaplan/plans/reliability-20260424-235843/execution.json 2>/dev/null | head -120",
  "description": "Check all-open execution.json"
}
```

> TOOL

tool_result Bash
```
{
  "output": "Aggregated execute batches: completed 1/1.\nBatch 1: Executed T9 (final validation task). All previously-completed tasks (T1\u2013T8) remain done with no regressions. Focused test suites pass 38/38. Full repository suite: 810 passed, 2 pre-existing failures (Docker unavailable and unrelated codex test). Both --max-context-retries and --max-cost-usd appear in megaplan auto --help. Negative value rejection for --max-cost-usd confirmed. DriverOutcome fields, to_json(), DEFAULT_MAX_CONTEXT_RETRIES, exit codes 6/7, init.py glue, chain.yaml.example, and ChainSpec propagation all verified. Throwaway verification script run and deleted.",
  "commands_run": [
    "python -m pytest tests/test_auto.py tests/test_chain.py tests/test_handle_init_idea_file.py --tb=short -q --no-header",
    "python -m pytest --tb=short -q --no-header",
    "python -m megaplan auto --help",
    "python _verify_flags.py && rm _verify_flags.py"
  ],
  "deviations": [
    "Done tasks missing both files_changed and commands_run: T1, T2, T3, T4, T5, T6, T7, T8",
    "Advisory: done tasks rely on commands_run without files_changed (FLAG-006 softening): T9",
    "Advisory audit finding: Git status shows changed files not claimed by any task: megaplan/auto.py, megaplan/chain.py, megaplan/cloud/templates/chain.yaml.example, megaplan/handlers/init.py, tests/test_auto.py, tests/test_core_without_cloud.py, tests/test_handle_init_idea_file.py",
    "Advisory audit finding: Git status shows changed files not claimed by any task: megaplan/auto.py, megaplan/chain.py, megaplan/cloud/templates/chain.yaml.example, megaplan/handlers/init.py, tests/test_auto.py, tests/test_core_without_cloud.py, tests/test_handle_init_idea_file.py"
  ],
  "task_updates": [
    {
      "task_id": "T1",
      "status": "done",
      "executor_notes": "Already completed in prior execution pass. DriverOutcome has four new fields with safe defaults (total_cost_usd=0.0, max_cost_usd=None, context_retries_used=0, max_context_retries=0). to_json() includes all four. DEFAULT_MAX_CONTEXT_RETRIES=2 defined at line 46.",
      "files_changed": [],
      "commands_run": []
    },
    {
      "task_id": "T2",
      "status": "done",
      "executor_notes": "Already completed in prior execution pass. Both --max-context-retries and --max-cost-usd in --help output confirmed. _non_negative_float rejects negatives. Both flags passed from run_auto to drive().",
      "files_changed": [],
      "commands_run": []
    },
    {
      "task_id": "T3",
      "status": "done",
      "executor_notes": "Already completed in prior execution pass. ChainSpec includes max_cost_usd and max_context_retries with correct defaults. Parsed from driver block in from_dict(). Propagated through _drive_plan(). DEFAULT_MAX_CONTEXT_RETRIES imported.",
      "files_changed": [],
      "commands_run": []
    },
    {
      "task_id": "T4",
      "status": "done",
      "executor_notes": "Already completed in prior execution pass. Context-exhaustion retry triggers only for next_step=='execute' with specific error fragment. Uses cmd + ['--fresh'] without mutating. Increments context_retries_used. Returns context_retry_exhausted when exhausted. Preserves stall_count and last_state.",
      "files_changed": [],
      "commands_run": []
    },
    {
      "task_id": "T5",
      "status": "done",
      "executor_notes": "Already completed in prior execution pass. Cost-cap check placed after terminal-state block and before review-cycle tracking. Guarded by last_phase is not None. Uses status.get('total_cost_usd', 0.0) exclusively with NO dead-code history fallback. Returns cost_cap_exceeded with total_cost_usd and max_cost_usd.",
      "files_changed": [],
      "commands_run": []
    },
    {
      "task_id": "T6",
      "status": "done",
      "executor_notes": "Already completed in prior execution pass. cost_cap_exceeded->6 and context_retry_exhausted->7 exit codes inserted after blocked->5. init.py auto_outcome dict includes all four new fields.",
      "files_changed": [],
      "commands_run": []
    },
    {
      "task_id": "T7",
      "status": "done",
      "executor_notes": "Already completed in prior execution pass. chain.yaml.example documents max_cost_usd and max_context_retries in driver block as commented-out examples.",
      "files_changed": [],
      "commands_run": []
    },
    {
      "task_id": "T8",
      "status": "done",
      "executor_notes": "Already completed in prior execution pass. 9 new unit tests all pass: context retry success (--fresh verified), context retry exhausted (context_retries_used==2), context retry then different error (stall path), generic failure uses stall path (context_retries_used==0), cost cap cumulative (total_cost_usd==3.00), cost cap single expensive phase, cost cap does not mask done, cost cap unset no early termination, cost cap does not fire before first phase.",
      "files_changed": [],
      "commands_run": []
    },
    {
      "task_id": "T9",
      "status": "done",
      "executor_notes": "Focused suites: 38/38 passed (test_auto.py 15 tests, test_chain.py, test_handle_init_idea_file.py). Full suite: 810 passed, 2 pre-existing failures (test_cloud_local_lifecycle_smoke: Docker not available; test_run_codex_step_uses_full_auto_for_critique_template_writes: unrelated codex assertion). Both flags confirmed in 'megaplan auto --help'. Throwaway script verified: flags in help, negative --max-cost-usd rejection, DriverOutcome fields with safe defaults, to_json() includes new fields, DEFAULT_MAX_CONTEXT_RETRIES=2. Script deleted after verification.",
      "files_changed": [],
      "commands_run": [
        "python -m pytest tests/test_auto.py tests/test_chain.py tests/test_handle_init_idea_file.py --tb=short -q --no-header",
        "python -m pytest --tb=short -q --no-header",
        "python -m megaplan auto --help",
        "python _verify_flags.py && rm _verify_flags.py"
      ]
    }
  ],
  "sense_check_acknowledgments": [
    {
      "sense_check_id": "SC1",
      "executor_note": "Confirmed: DriverOutcome has four new fields (total_cost_usd=0.0, max_cost_usd=None, context_retries_used=0, max_context_retries=0) all with safe defaults. to_json() includes all four. DEFAULT_MAX_CONTEXT_RETRIES=2 at line 46."
    },
    {
      "sense_check_id": "SC2",
      "executor_note": "Confirmed: Both --max-context-retries and --max-cost-usd appear in 'megaplan auto --help'. Negative values rejected with 'value must be non-negative' error. Both flags passed from run_auto into drive()."
    },
    {
      "sense_check_id": "SC3",
      "executor_note": "Confirmed: ChainSpec includes max_cost_usd (float|None, default None) and max_context_retries (int, default DEFAULT_MAX_CONTEXT_RETRIES=2). Parsed in from_dict() from driver block. Propagated through _drive_plan(). DEFAULT_MAX_CONTEXT_RETRIES imported in chain.py."
    },
    {
      "sense_check_id": "SC4",
      "executor_note": "Confirmed: Context-exhaustion retry triggers only for next_step=='execute' with exact fragment check. Uses cmd + ['--fresh'] (non-mutating). Increments context_retries_used on every attempt. Returns context_retry_exhausted when while-else fires. stall_count and last_state NOT reset."
    },
    {
      "sense_check_id": "SC5",
      "executor_note": "Confirmed: Cost-cap check at line 309, after terminal-state block (line 292 return) and before review-cycle tracking (line 338). Guarded by 'last_phase is not None'. Uses status.get('total_cost_usd', 0.0) exclusively \u2014 NO dead-code history fallback. Returns cost_cap_exceeded with total_cost_usd and max_cost_usd."
    },
    {
      "sense_check_id": "SC6",
      "executor_note": "Confirmed: cost_cap_exceeded -> exit code 6, context_retry_exhausted -> exit code 7, both inserted after blocked -> 5 and before return 1. init.py auto_outcome dict includes total_cost_usd, max_cost_usd, context_retries_used, max_context_retries at lines 182-185."
    },
    {
      "sense_check_id": "SC7",
      "executor_note": "Confirmed: chain.yaml.example lines 38-39 document max_cost_usd and max_context_retries in the driver block as commented-out examples with descriptions."
    },
    {
      "sense_check_id": "SC8",
      "executor_note": "Confirmed: All 9 new tests pass. Context retry success verifies --fresh via assertion on mock_run.call_args_list. Cost cap cumulative verifies total_cost_usd==3.00. Generic failure test confirms stall path with context_retries_used==0. Cost-cap-does-not-mask-done verifies done wins over cost_cap_exceeded."
    },
    {
      "sense_check_id": "SC9",
      "executor_note": "Confirmed: tests/test_auto.py (15), test_chain.py, test_handle_init_idea_file.py all pass (38/38). Full suite: 810 passed, 2 pre-existing failures (Docker unavailable + unrelated codex test). Throwaway --help verification script run and deleted."
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-open/.megaplan/plans/reliability-20260424-235843/",
  "description": "List all-open plan dir"
}
```

> TOOL

tool_result Bash
```
critique_check_all_locations.json
critique_check_callers.json
critique_check_correctness.json
critique_check_issue_hints.json
critique_check_scope.json
critique_v1.json
critique_v2.json
critique_v3.json
execution.json
execution_audit.json
execution_batch_1.json
execution_batch_2.json
execution_batch_3.json
execution_batch_4.json
execution_batch_5.json
execution_checkpoint.json
faults.json
final.md
finalize.json
finalize_output.json
finalize_snapshot.json
gate.json
gate_signals_v1.json
gate_signals_v2.json
gate_signals_v3.json
plan_v1.md
plan_v1.meta.json
plan_v1_raw.txt
plan_v2.md
plan_v2.meta.json
plan_v3.md
plan_v3.meta.json
state.json
```

> TOOL

tool_use Bash
```json
{
  "command": "tail -300 /Users/user_c042661f/Documents/megaplan/.megaplan/bakeoffs/reliability-20260424-235843/all-open/auto.log",
  "description": "Tail of all-open auto.log"
}
```

> TOOL

tool_result Bash
```
[auto reliability-20260424-235843] iter 5 state=critiqued next=revise valid_next=['revise', 'step']
[auto reliability-20260424-235843] running: megaplan revise --plan reliability-20260424-235843
[auto reliability-20260424-235843] iter 6 state=planned next=critique valid_next=['critique', 'plan', 'step']
[auto reliability-20260424-235843] running: megaplan critique --plan reliability-20260424-235843
[auto reliability-20260424-235843] iter 7 state=critiqued next=gate valid_next=['gate', 'step']
[auto reliability-20260424-235843] running: megaplan gate --plan reliability-20260424-235843
[auto reliability-20260424-235843] iter 8 state=critiqued next=revise valid_next=['revise', 'step']
[auto reliability-20260424-235843] running: megaplan revise --plan reliability-20260424-235843
[auto reliability-20260424-235843] iter 9 state=planned next=critique valid_next=['critique', 'plan', 'step']
[auto reliability-20260424-235843] running: megaplan critique --plan reliability-20260424-235843
[auto reliability-20260424-235843] iter 10 state=critiqued next=gate valid_next=['gate', 'step']
[auto reliability-20260424-235843] running: megaplan gate --plan reliability-20260424-235843
[auto reliability-20260424-235843] iter 11 state=gated next=finalize valid_next=['finalize', 'override replan', 'step']
[auto reliability-20260424-235843] running: megaplan finalize --plan reliability-20260424-235843
[auto reliability-20260424-235843] iter 12 state=finalized next=execute valid_next=['execute', 'override replan', 'step']
[auto reliability-20260424-235843] running: megaplan execute --confirm-destructive --user-approved --plan reliability-20260424-235843
[auto reliability-20260424-235843] iter 13 state=finalized next=execute valid_next=['execute', 'override replan', 'step']
[auto reliability-20260424-235843] running: megaplan execute --confirm-destructive --user-approved --plan reliability-20260424-235843
[auto reliability-20260424-235843] iter 14 state=finalized next=execute valid_next=['execute', 'override replan', 'step']
[auto reliability-20260424-235843] running: megaplan execute --confirm-destructive --user-approved --plan reliability-20260424-235843
[auto reliability-20260424-235843] iter 15 state=finalized next=execute valid_next=['execute', 'override replan', 'step']
[auto reliability-20260424-235843] running: megaplan execute --confirm-destructive --user-approved --plan reliability-20260424-235843
[auto reliability-20260424-235843] iter 16 state=finalized next=execute valid_next=['execute', 'override replan', 'step']
[auto reliability-20260424-235843] running: megaplan execute --confirm-destructive --user-approved --plan reliability-20260424-235843
[auto reliability-20260424-235843] iter 17 state=finalized next=execute valid_next=['execute', 'override replan', 'step']
[auto reliability-20260424-235843] stalled at state=finalized for 5 iterations
{
  "status": "stalled",
  "plan": "reliability-20260424-235843",
  "final_state": "finalized",
  "iterations": 17,
  "reason": "stalled at 'finalized' for 5 iterations \u2014 manual intervention required",
  "last_phase": "execute",
  "events": [
    {
      "msg": "iter 1 state=initialized next=plan valid_next=['plan']",
      "iteration": 1,
      "state": "initialized",
      "next_step": "plan",
      "valid_next": [
        "plan"
      ]
    },
    {
      "msg": "running: megaplan plan --plan reliability-20260424-235843",
      "phase": "plan",
      "timeout": 3600
    },
    {
      "msg": "phase 'plan' exited 1: [megaplan] Starting plan... Expected duration: 1m-15m.\n/Users/user_c042661f/.pyenv/versions/3.11.11/lib/python3.11/site-packages/requests/__init__.py:113: RequestsDependencyWarning: urllib3 (2.6.3) or chardet (7.4.0.post1)/charset_normalizer (3.4.1) doesn't match a supported version!\n  warnings.warn(\n  [tool] \u30fd(>\u2200<\u2606)\u2606 processing...\n  [tool] (\u25d5\u1d17\u25d5\u273f) \u26a1 running 2 tools concurrently\n  [done] \u26a1 2/2 tools completed in 1.3s total (1.0s)\n  \u250a \ud83d\udd0e find      megaplan/auto.py  0.6s\n  \u250a \ud83d\udd0e find      test_auto  0.6s\n  [tool] (\uff61\u2022\u0301\ufe3f\u2022\u0300\uff61) pondering...\n  [tool] (\u2605\u03c9\u2605) \u26a1 running 2 tools concurrently\n  [done] \u26a1 2/2 tools completed in 1.7s total (1.0s)\n  \u250a \ud83d\udcd6 read      ...235843/all-open/megaplan/auto.py  0.8s\n  \u250a \ud83d\udcd6 read      ...5843/all-open/tests/test_auto.py  0.8s\n  [tool] \u0669(\u0e51\u275b\u1d17\u275b\u0e51)\u06f6 synthesizing...\n  [tool] (\u2267\u25e1\u2266) \u26a1 running 2 tools concurrently\n  [done] \u26a1 2/2 tools completed in 1.3s total (1.0s)\n  \u250a \ud83d\udcd6 read      ...235843/all-open/megaplan/auto.py  0.8s\n  \u250a \ud83d\udd0e grep      cost_usd  0.4s\n  [tool] (\u00b4\uff65_\uff65`) pondering...\n  [tool] (\u2605\u03c9\u2605) \u26a1 running 2 tools concurrently\n  [done] \u26a1 2/2 tools completed in 1.3s total (1.0s)\n  \u250a \ud83d\udcd6 read      ...all-open/megaplan/_core/state.py  0.8s\n  \u250a \ud83d\udd0e grep      history  0.4s\n  [tool] (\uff61\u2022\u0301\ufe3f\u2022\u0300\uff61) contemplating...\n  [tool] \u266a(\u00b4\u03b5` ) \u26a1 running 2 tools concurrently\n  [done] \u26a1 2/2 tools completed in 0.8s total (0.5s)\n  \u250a \ud83d\udd0e grep      total_cost_usd  0.4s\n  \u250a \ud83d\udd0e grep      def status  0.4s\n  [tool] (\u00b4\uff65_\uff65`) computing...\n  [tool] \u30fe(\uff3e\u2207\uff3e) \ud83d\udcd6 /Users/user_c042661f/Documen...\n  [done] \u250a \ud83d\udcd6 read      ...-235843/all-open/megaplan/cli.py  0.8s (1.0s)\n  [tool] \u0ca0_\u0ca0 musing...\n  [tool] (\u25d5\u203f\u25d5\u273f) \u26a1 running 2 tools concurrently\n  [done] \u26a1 2/2 tools completed in 0.9s total (0.5s)\n  \u250a \ud83d\udd0e grep      history  0.4s\n  \u250a \ud83d\udd0e grep      def load_plan  0.4s\n  [tool] \u25c9_\u25c9 mulling...\n  [tool] (\u25d5\u203f\u25d5\u273f) \ud83d\udd0e --fresh\n  [done] \u250a \ud83d\udd0e grep      --fresh  0.4s (0.5s)\n  [tool] ( \u2022_\u2022)>\u2310\u25a0-\u25a0 synthesizing...\n  [tool] (\u25d5\u203f\u25d5\u273f) \ud83d\udd0e fresh\n  [done] \u250a \ud83d\udd0e grep      fresh  0.4s (0.5s)\n  [tool] \u25c9_\u25c9 brainstorming...\n  [tool] (\u25d5\u203f\u25d5\u273f) \u26a1 running 2 tools concurrently\n  [done] \u26a1 2/2 tools completed in 1.3s total (1.0s)\n  \u250a \ud83d\udcd6 read      ...l-open/megaplan/hermes_worker.py  0.9s\n  \u250a \ud83d\udd0e grep      add_argument.*--fresh  0.4s\n  [tool] ( \u0361\u00b0 \u035c\u0296 \u0361\u00b0) reasoning...\n  [tool] ( \u02d8\u25bd\u02d8)\u3063 \ud83d\udcd6 /Users/user_c042661f/Documen...\n  [done] \u250a \ud83d\udcd6 read      ...-235843/all-open/megaplan/cli.py  0.8s (1.0s)\n  [tool] (\u25d4_\u25d4) analyzing...\n  [tool] (\u25d5\u203f\u25d5\u273f) \u26a1 running 2 tools concurrently\n  [done] \u26a1 2/2 tools completed in 0.9s total (0.5s)\n  \u250a \ud83d\udd0e grep      def test_  0.4s\n  \u250a \ud83d\udd0e find      pytest  0.4s\n  [tool] (\uff61\u2022\u0301\ufe3f\u2022\u0300\uff61) brainstorming...\n  [tool] (\u2605\u03c9\u2605) \ud83d\udd0e pyproject.toml|setup.py|pyt...\n  [done] \u250a \ud83d\udd0e find      pyproject.toml|setup.py|pytest.ini  0.4s (0.5s)\n  [tool] (\u2299_\u2299) formulating...\n  [tool] (\u2267\u25e1\u2266) \ud83d\udd0e *\n  [done] \u250a \ud83d\udd0e find      *  0.4s (0.5s)\n  [tool] (\u00ac\u203f\u00ac) cogitating...\n  [tool] ( \u02d8\u25bd\u02d8)\u3063 \ud83d\udcd6 /Users/user_c042661f/Documen...\n  [done] \u250a \ud83d\udcd6 read      ...4-235843/all-open/pyproject.toml  0.8s (1.0s)\n  [tool] \u0669(\u0e51\u275b\u1d17\u275b\u0e51)\u06f6 ruminating...\n  [tool] \u30fe(\uff3e\u2207\uff3e) \ud83d\udcd6 /Users/user_c042661f/Documen...\n  [done] \u250a \ud83d\udcd6 read      ...235843/all-open/megaplan/auto.py  0.8s (1.0s)\n  [tool] (\u00ac\u203f\u00ac) pondering..."
    },
    {
      "msg": "iter 2 state=initialized next=plan valid_next=['plan']",
      "iteration": 2,
      "state": "initialized",
      "next_step": "plan",
      "valid_next": [
        "plan"
      ]
    },
    {
      "msg": "running: megaplan plan --plan reliability-20260424-235843",
      "phase": "plan",
      "timeout": 3600
    },
    {
      "msg": "iter 3 state=planned next=critique valid_next=['critique', 'plan', 'step']",
      "iteration": 3,
      "state": "planned",
      "next_step": "critique",
      "valid_next": [
        "critique",
        "plan",
        "step"
      ]
    },
    {
      "msg": "running: megaplan critique --plan reliability-20260424-235843",
      "phase": "critique",
      "timeout": 3600
    },
    {
      "msg": "iter 4 state=critiqued next=gate valid_next=['gate', 'step']",
      "iteration": 4,
      "state": "critiqued",
      "next_step": "gate",
      "valid_next": [
        "gate",
        "step"
      ]
    },
    {
      "msg": "running: megaplan gate --plan reliability-20260424-235843",
      "phase": "gate",
      "timeout": 3600
    },
    {
      "msg": "iter 5 state=critiqued next=revise valid_next=['revise', 'step']",
      "iteration": 5,
      "state": "critiqued",
      "next_step": "revise",
      "valid_next": [
        "revise",
        "step"
      ]
    },
    {
      "msg": "running: megaplan revise --plan reliability-20260424-235843",
      "phase": "revise",
      "timeout": 3600
    },
    {
      "msg": "iter 6 state=planned next=critique valid_next=['critique', 'plan', 'step']",
      "iteration": 6,
      "state": "planned",
      "next_step": "critique",
      "valid_next": [
        "critique",
        "plan",
        "step"
      ]
    },
    {
      "msg": "running: megaplan critique --plan reliability-20260424-235843",
      "phase": "critique",
      "timeout": 3600
    },
    {
      "msg": "iter 7 state=critiqued next=gate valid_next=['gate', 'step']",
      "iteration": 7,
      "state": "critiqued",
      "next_step": "gate",
      "valid_next": [
        "gate",
        "step"
      ]
    },
    {
      "msg": "running: megaplan gate --plan reliability-20260424-235843",
      "phase": "gate",
      "timeout": 3600
    },
    {
      "msg": "iter 8 state=critiqued next=revise valid_next=['revise', 'step']",
      "iteration": 8,
      "state": "critiqued",
      "next_step": "revise",
      "valid_next": [
        "revise",
        "step"
      ]
    },
    {
      "msg": "running: megaplan revise --plan reliability-20260424-235843",
      "phase": "revise",
      "timeout": 3600
    },
    {
      "msg": "iter 9 state=planned next=critique valid_next=['critique', 'plan', 'step']",
      "iteration": 9,
      "state": "planned",
      "next_step": "critique",
      "valid_next": [
        "critique",
        "plan",
        "step"
      ]
    },
    {
      "msg": "running: megaplan critique --plan reliability-20260424-235843",
      "phase": "critique",
      "timeout": 3600
    },
    {
      "msg": "iter 10 state=critiqued next=gate valid_next=['gate', 'step']",
      "iteration": 10,
      "state": "critiqued",
      "next_step": "gate",
      "valid_next": [
        "gate",
        "step"
      ]
    },
    {
      "msg": "running: megaplan gate --plan reliability-20260424-235843",
      "phase": "gate",
      "timeout": 3600
    },
    {
      "msg": "iter 11 state=gated next=finalize valid_next=['finalize', 'override replan', 'step']",
      "iteration": 11,
      "state": "gated",
      "next_step": "finalize",
      "valid_next": [
        "finalize",
        "override replan",
        "step"
      ]
    },
    {
      "msg": "running: megaplan finalize --plan reliability-20260424-235843",
      "phase": "finalize",
      "timeout": 3600
    },
    {
      "msg": "iter 12 state=finalized next=execute valid_next=['execute', 'override replan', 'step']",
      "iteration": 12,
      "state": "finalized",
      "next_step": "execute",
      "valid_next": [
        "execute",
        "override replan",
        "step"
      ]
    },
    {
      "msg": "running: megaplan execute --confirm-destructive --user-approved --plan reliability-20260424-235843",
      "phase": "execute",
      "timeout": 3600
    },
    {
      "msg": "iter 13 state=finalized next=execute valid_next=['execute', 'override replan', 'step']",
      "iteration": 13,
      "state": "finalized",
      "next_step": "execute",
      "valid_next": [
        "execute",
        "override replan",
        "step"
      ]
    },
    {
      "msg": "running: megaplan execute --confirm-destructive --user-approved --plan reliability-20260424-235843",
      "phase": "execute",
      "timeout": 3600
    },
    {
      "msg": "iter 14 state=finalized next=execute valid_next=['execute', 'override replan', 'step']",
      "iteration": 14,
      "state": "finalized",
      "next_step": "execute",
      "valid_next": [
        "execute",
        "override replan",
        "step"
      ]
    },
    {
      "msg": "running: megaplan execute --confirm-destructive --user-approved --plan reliability-20260424-235843",
      "phase": "execute",
      "timeout": 3600
    },
    {
      "msg": "iter 15 state=finalized next=execute valid_next=['execute', 'override replan', 'step']",
      "iteration": 15,
      "state": "finalized",
      "next_step": "execute",
      "valid_next": [
        "execute",
        "override replan",
        "step"
      ]
    },
    {
      "msg": "running: megaplan execute --confirm-destructive --user-approved --plan reliability-20260424-235843",
      "phase": "execute",
      "timeout": 3600
    },
    {
      "msg": "iter 16 state=finalized next=execute valid_next=['execute', 'override replan', 'step']",
      "iteration": 16,
      "state": "finalized",
      "next_step": "execute",
      "valid_next": [
        "execute",
        "override replan",
        "step"
      ]
    },
    {
      "msg": "running: megaplan execute --confirm-destructive --user-approved --plan reliability-20260424-235843",
      "phase": "execute",
      "timeout": 3600
    },
    {
      "msg": "iter 17 state=finalized next=execute valid_next=['execute', 'override replan', 'step']",
      "iteration": 17,
      "state": "finalized",
      "next_step": "execute",
      "valid_next": [
        "execute",
        "override replan",
        "step"
      ]
    },
    {
      "msg": "stalled at state=finalized for 5 iterations"
    }
  ]
}
```

> AGENT

Important — execution.json says all 9 tasks are "done" but state still says finalized. Let me check the standard profile's outputs, the cost data, and the all-kimi audit too.

> TOOL

tool_use Bash
```json
{
  "command": "cat /Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/standard/.megaplan/plans/reliability-20260424-235843/execution_audit.json 2>/dev/null | head -100",
  "description": "Standard execution audit"
}
```

> TOOL

tool_result Bash
```
{
  "findings": [
    "Executor claimed changed files not present in git status: .megaplan/plans/reliability-20260424-235843/execution_batch_6.json",
    "Git status shows changed files not claimed by any task: tests/test_workers.py"
  ],
  "files_in_diff": [
    "megaplan/auto.py",
    "tests/test_auto.py",
    "tests/test_cloud_local_lifecycle.py",
    "tests/test_workers.py"
  ],
  "files_claimed": [
    ".megaplan/plans/reliability-20260424-235843/execution_batch_6.json",
    "megaplan/auto.py",
    "tests/test_auto.py",
    "tests/test_cloud_local_lifecycle.py"
  ],
  "skipped": false,
  "reason": ""
}
```

> TOOL

tool_use Bash
```json
{
  "command": "cat /Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-open/.megaplan/plans/reliability-20260424-235843/execution_audit.json 2>/dev/null | head -200",
  "description": "All-open execution audit"
}
```

> TOOL

tool_result Bash
```
{
  "findings": [
    "Git status shows changed files not claimed by any task: megaplan/auto.py, megaplan/chain.py, megaplan/cloud/templates/chain.yaml.example, megaplan/handlers/init.py, tests/test_auto.py, tests/test_core_without_cloud.py, tests/test_handle_init_idea_file.py"
  ],
  "files_in_diff": [
    "megaplan/auto.py",
    "megaplan/chain.py",
    "megaplan/cloud/templates/chain.yaml.example",
    "megaplan/handlers/init.py",
    "tests/test_auto.py",
    "tests/test_core_without_cloud.py",
    "tests/test_handle_init_idea_file.py"
  ],
  "files_claimed": [],
  "skipped": false,
  "reason": ""
}
```

> TOOL

tool_use Bash
```json
{
  "command": "cat /Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-kimi/.megaplan/plans/reliability-20260424-235843/execution_audit.json 2>/dev/null | head -200",
  "description": "All-kimi execution audit"
}
```

> TOOL

tool_result Bash
```
{
  "findings": [
    "Git status shows changed files not claimed by any task: megaplan/auto.py, tests/test_auto.py, tests/test_chain.py",
    "Sense check SC9 is missing an executor acknowledgment."
  ],
  "files_in_diff": [
    "megaplan/auto.py",
    "megaplan/chain.py",
    "megaplan/cloud/templates/chain.yaml.example",
    "megaplan/handlers/init.py",
    "tests/test_auto.py",
    "tests/test_chain.py",
    "tests/test_core_without_cloud.py",
    "tests/test_handle_init_idea_file.py"
  ],
  "files_claimed": [
    "megaplan/chain.py",
    "megaplan/cloud/templates/chain.yaml.example",
    "megaplan/handlers/init.py",
    "tests/test_core_without_cloud.py",
    "tests/test_handle_init_idea_file.py"
  ],
  "skipped": false,
  "reason": ""
}
```

> TOOL

tool_use Bash
```json
{
  "command": "for p in standard all-open all-kimi; do echo \"=== $p ===\"; python3 -c \"import json; d=json.load(open('/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/$p/.megaplan/plans/reliability-20260424-235843/state.json')); h=d.get('history',[]); print('phases:', len(h)); total=0; [print(f'  {e.get(\\\"phase\\\",\\\"?\\\"):>10s}  cost=\\${float(e.get(\\\"cost_usd\\\",0) or 0):.4f}  tok={e.get(\\\"total_tokens\\\",\\\"?\\\")}  model={e.get(\\\"model\\\",\\\"?\\\")[:40] if e.get(\\\"model\\\") else \\\"?\\\"}') or globals().__setitem__('total', total+float(e.get('cost_usd',0) or 0)) for e in h]; print(f'  total: \\${sum(float(e.get(\\\"cost_usd\\\",0) or 0) for e in h):.4f}')\"; done",
  "description": "Cost breakdown per profile"
}
```

> TOOL

tool_result Bash
```
=== standard ===
phases: 10
           ?  cost=$0.0000  tok=?  model=?
           ?  cost=$1.0101  tok=?  model=?
           ?  cost=$0.0000  tok=?  model=?
           ?  cost=$0.4302  tok=?  model=?
           ?  cost=$0.9291  tok=?  model=?
           ?  cost=$0.0000  tok=?  model=?
           ?  cost=$0.3050  tok=?  model=?
           ?  cost=$1.0335  tok=?  model=?
           ?  cost=$0.0000  tok=?  model=?
           ?  cost=$0.0000  tok=?  model=?
  total: $3.7079
=== all-open ===
phases: 17
           ?  cost=$0.0000  tok=?  model=?
           ?  cost=$0.0000  tok=?  model=?
           ?  cost=$0.2097  tok=580227  model=?
           ?  cost=$2.7870  tok=4502907  model=?
           ?  cost=$0.0204  tok=21329  model=?
           ?  cost=$0.1905  tok=598147  model=?
           ?  cost=$2.5991  tok=4029545  model=?
           ?  cost=$0.0348  tok=26614  model=?
           ?  cost=$0.1007  tok=174093  model=?
           ?  cost=$4.5776  tok=7935973  model=?
           ?  cost=$0.0394  tok=30050  model=?
           ?  cost=$0.1187  tok=408557  model=?
           ?  cost=$0.1604  tok=?  model=?
           ?  cost=$1.4997  tok=?  model=?
           ?  cost=$0.5289  tok=?  model=?
           ?  cost=$0.8355  tok=?  model=?
           ?  cost=$0.4267  tok=?  model=?
  total: $14.1291
=== all-kimi ===
phases: 13
           ?  cost=$0.0000  tok=?  model=?
           ?  cost=$0.1358  tok=369276  model=?
           ?  cost=$1.0942  tok=4268782  model=?
           ?  cost=$0.0300  tok=25908  model=?
           ?  cost=$0.2231  tok=878383  model=?
           ?  cost=$1.2266  tok=4926180  model=?
           ?  cost=$0.0218  tok=26773  model=?
           ?  cost=$0.1551  tok=543743  model=?
           ?  cost=$0.0892  tok=?  model=?
           ?  cost=$0.0890  tok=?  model=?
           ?  cost=$0.4547  tok=?  model=?
           ?  cost=$0.0825  tok=?  model=?
           ?  cost=$0.9719  tok=?  model=?
  total: $4.5737
```

> TOOL

tool_use Bash
```json
{
  "command": "python3 -c \"\nimport json\nfor p in ['standard','all-open','all-kimi']:\n    d=json.load(open(f'/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/{p}/.megaplan/plans/reliability-20260424-235843/state.json'))\n    print(f'=== {p} ===')\n    for e in d.get('history',[]):\n        print(' ', list(e.keys()))\n    break\n\"",
  "description": "Inspect history entry shape"
}
```

> TOOL

tool_result Bash
```
=== standard ===
  ['step', 'timestamp', 'duration_ms', 'cost_usd', 'result', 'environment']
  ['step', 'timestamp', 'duration_ms', 'cost_usd', 'result', 'session_mode', 'session_id', 'agent', 'output_file', 'artifact_hash']
  ['step', 'timestamp', 'duration_ms', 'cost_usd', 'result', 'session_mode', 'session_id', 'agent', 'output_file', 'artifact_hash', 'flags_count']
  ['step', 'timestamp', 'duration_ms', 'cost_usd', 'result', 'session_mode', 'session_id', 'agent', 'output_file', 'artifact_hash', 'recommendation']
  ['step', 'timestamp', 'duration_ms', 'cost_usd', 'result', 'session_mode', 'session_id', 'agent', 'output_file', 'artifact_hash', 'flags_addressed']
  ['step', 'timestamp', 'duration_ms', 'cost_usd', 'result', 'session_mode', 'session_id', 'agent', 'output_file', 'artifact_hash', 'flags_count']
  ['step', 'timestamp', 'duration_ms', 'cost_usd', 'result', 'session_mode', 'session_id', 'agent', 'output_file', 'artifact_hash', 'recommendation']
  ['step', 'timestamp', 'duration_ms', 'cost_usd', 'result', 'session_mode', 'session_id', 'agent', 'output_file', 'artifact_hash']
  ['step', 'timestamp', 'duration_ms', 'cost_usd', 'result', 'session_mode', 'session_id', 'agent', 'output_file', 'artifact_hash', 'finalize_hash', 'approval_mode']
  ['step', 'timestamp', 'duration_ms', 'cost_usd', 'result', 'session_mode', 'session_id', 'agent', 'output_file', 'artifact_hash', 'finalize_hash']
```

> TOOL

tool_use Bash
```json
{
  "command": "python3 -c \"\nimport json\nd=json.load(open('/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/standard/.megaplan/plans/reliability-20260424-235843/state.json'))\nimport json\nprint(json.dumps(d.get('history',[])[:3], indent=2))\n\"",
  "description": "Standard history first entries"
}
```

> TOOL

tool_result Bash
```
[
  {
    "step": "init",
    "timestamp": "2026-04-24T21:58:45Z",
    "duration_ms": 0,
    "cost_usd": 0.0,
    "result": "success",
    "environment": {
      "claude": true,
      "codex": true
    }
  },
  {
    "step": "plan",
    "timestamp": "2026-04-24T22:02:47Z",
    "duration_ms": 238692,
    "cost_usd": 1.0100945000000001,
    "result": "success",
    "session_mode": "persistent",
    "session_id": "b4324225-de0f-41a3-8207-79e74d93c776",
    "agent": "claude",
    "output_file": "plan_v1.md",
    "artifact_hash": "sha256:44372f482e4c9a95f792c503a615e4ba42ad4a9e08b91e9c54e1b33adcc0d8e2"
  },
  {
    "step": "critique",
    "timestamp": "2026-04-24T22:05:12Z",
    "duration_ms": 143858,
    "cost_usd": 0.0,
    "result": "success",
    "session_mode": "persistent",
    "session_id": "019dc184-571b-7551-91a9-811ffbd49f24",
    "agent": "codex",
    "output_file": "critique_v1.json",
    "artifact_hash": "sha256:b2dd77f9ed74a86134208271374e530c2cbaec7ea6166824a5eb0a933732e2d4",
    "flags_count": 12
  }
]
```

> AGENT

Now I can confirm: standard's codex phases (critique/execute/review) all show $0 cost — broken instrumentation. Let me check stall details and execution batches for hermes profiles.

> TOOL

tool_use Bash
```json
{
  "command": "python3 -c \"\nimport json\nd=json.load(open('/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-open/.megaplan/plans/reliability-20260424-235843/execution.json'))\nprint('keys:', list(d.keys()))\nprint('completed_tasks:', d.get('completed_tasks'))\nprint('total_tasks:', d.get('total_tasks'))\nprint('status:', d.get('status'))\nprint('batch_count:', d.get('batch_count'))\n\"",
  "description": "All-open execution.json shape"
}
```

> TOOL

tool_result Bash
```
keys: ['output', 'commands_run', 'deviations', 'task_updates', 'sense_check_acknowledgments', 'files_changed']
completed_tasks: None
total_tasks: None
status: None
batch_count: None
```

> TOOL

tool_use Bash
```json
{
  "command": "python3 -c \"\nimport json\nfor p in ['all-open','all-kimi']:\n    d=json.load(open(f'/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/{p}/.megaplan/plans/reliability-20260424-235843/execution.json'))\n    print('===',p,'===')\n    print(json.dumps(d, indent=2)[:2000])\n    print()\n\"",
  "description": "Both hermes execution.json"
}
```

> TOOL

tool_result Bash
```
=== all-open ===
{
  "output": "Aggregated execute batches: completed 1/1.\nBatch 1: Executed T9 (final validation task). All previously-completed tasks (T1\u2013T8) remain done with no regressions. Focused test suites pass 38/38. Full repository suite: 810 passed, 2 pre-existing failures (Docker unavailable and unrelated codex test). Both --max-context-retries and --max-cost-usd appear in megaplan auto --help. Negative value rejection for --max-cost-usd confirmed. DriverOutcome fields, to_json(), DEFAULT_MAX_CONTEXT_RETRIES, exit codes 6/7, init.py glue, chain.yaml.example, and ChainSpec propagation all verified. Throwaway verification script run and deleted.",
  "commands_run": [
    "python -m pytest tests/test_auto.py tests/test_chain.py tests/test_handle_init_idea_file.py --tb=short -q --no-header",
    "python -m pytest --tb=short -q --no-header",
    "python -m megaplan auto --help",
    "python _verify_flags.py && rm _verify_flags.py"
  ],
  "deviations": [
    "Done tasks missing both files_changed and commands_run: T1, T2, T3, T4, T5, T6, T7, T8",
    "Advisory: done tasks rely on commands_run without files_changed (FLAG-006 softening): T9",
    "Advisory audit finding: Git status shows changed files not claimed by any task: megaplan/auto.py, megaplan/chain.py, megaplan/cloud/templates/chain.yaml.example, megaplan/handlers/init.py, tests/test_auto.py, tests/test_core_without_cloud.py, tests/test_handle_init_idea_file.py",
    "Advisory audit finding: Git status shows changed files not claimed by any task: megaplan/auto.py, megaplan/chain.py, megaplan/cloud/templates/chain.yaml.example, megaplan/handlers/init.py, tests/test_auto.py, tests/test_core_without_cloud.py, tests/test_handle_init_idea_file.py"
  ],
  "task_updates": [
    {
      "task_id": "T1",
      "status": "done",
      "executor_notes": "Already completed in prior execution pass. DriverOutcome has four new fields with safe defaults (total_cost_usd=0.0, max_cost_usd=None, context_retries_used=0, max_context_r

=== all-kimi ===
{
  "output": "Aggregated execute batches: completed 3/4.\nBatch 1: T6 complete. Updated megaplan/chain.py to integrate the new auto-driver safety features into the chain path. ChainSpec now exposes max_context_retries and max_cost_usd; from_dict parses them from the YAML driver block; _drive_plan forwards them to auto_drive(); and _handle_outcome treats cost_cap_exceeded and context_retry_exhausted as non-retryable terminal conditions returning 'stop' regardless of on_failure policy. Also fixed tests/test_core_without_cloud.py to include DEFAULT_MAX_CONTEXT_RETRIES in its fake_auto mock module, preventing a regression. Full suite: 801 passed, 2 pre-existing unrelated failures.\nBatch 2: T7 completed successfully. Updated init.py auto_outcome dict to include total_cost_usd, max_cost_usd, and context_retry_count. Updated chain.yaml.example to document driver.max_context_retries and driver.max_cost_usd. Fixed test regressions in test_core_without_cloud.py and test_handle_init_idea_file.py caused by the new fields. Full test suite: 801 passed, 2 pre-existing unrelated failures.\nBatch 3: Batch 7 (T8) completed successfully. Added 8 new unit tests to tests/test_auto.py and 2 chain integration tests to tests/test_chain.py. All 34 tests in test_auto.py + test_chain.py pass. Full suite: 812 passed, 2 pre-existing unrelated failures (test_local_provider_lifecycle_smoke, test_run_codex_step_uses_full_auto_for_critique_template_writes). The megaplan auto --help smoke test confirms both --max-context-retries and --max-cost-usd flags are present. Note: megaplan/auto.py had to be fully reconstructed during this batch because an earlier automated fix script corrupted it and git checkout reverted it to original; the reconstructed file includes all T1-T7 changes plus an additional fix ensuring all terminal DriverOutcome returns populate total_cost_usd, max_cost_usd, and context_retry_count (required for test_a to assert context_retry_count on a done outcome).",
  "commands_run": [
```

> AGENT

Both hermes profiles' execution.json shows the work completed but state doesn't reflect it. Let me look at the state.json transition logic and check finalize.json to understand the stall.

> TOOL

tool_use Bash
```json
{
  "command": "python3 -c \"\nimport json\nfor p in ['all-open','all-kimi']:\n    d=json.load(open(f'/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/{p}/.megaplan/plans/reliability-20260424-235843/state.json'))\n    print('===',p,'===')\n    print('current_state:', d.get('current_state', d.get('state','?')))\n    h=d.get('history',[])\n    for e in h:\n        print(f'  {e.get(\\\"step\\\",\\\"?\\\"):>10s}  result={e.get(\\\"result\\\",\\\"?\\\"):<10s}  output={e.get(\\\"output_file\\\",\\\"?\\\")[:40] if e.get(\\\"output_file\\\") else \\\"\\\"}')\n\"",
  "description": "Hermes profile state and history"
}
```

> TOOL

tool_result Bash
```
=== all-open ===
current_state: finalized
        init  result=success     output=
        plan  result=error       output=
        plan  result=success     output=plan_v1.md
    critique  result=success     output=critique_v1.json
        gate  result=success     output=gate.json
      revise  result=success     output=plan_v2.md
    critique  result=success     output=critique_v2.json
        gate  result=success     output=gate.json
      revise  result=success     output=plan_v3.md
    critique  result=success     output=critique_v3.json
        gate  result=success     output=gate.json
    finalize  result=success     output=finalize.json
     execute  result=blocked     output=execution.json
     execute  result=blocked     output=execution.json
     execute  result=blocked     output=execution.json
     execute  result=blocked     output=execution.json
     execute  result=blocked     output=execution.json
=== all-kimi ===
current_state: finalized
        init  result=success     output=
        plan  result=success     output=plan_v1.md
    critique  result=success     output=critique_v1.json
        gate  result=success     output=gate.json
      revise  result=success     output=plan_v2.md
    critique  result=success     output=critique_v2.json
        gate  result=success     output=gate.json
    finalize  result=success     output=finalize.json
     execute  result=blocked     output=execution.json
     execute  result=blocked     output=execution.json
     execute  result=blocked     output=execution.json
     execute  result=blocked     output=execution.json
     execute  result=blocked     output=execution.json
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-open/.megaplan/plans/reliability-20260424-235843/execution_batch_*.json && echo \"---\" && python3 -c \"\nimport json\nfor i in range(1,6):\n    p=f'/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-open/.megaplan/plans/reliability-20260424-235843/execution_batch_{i}.json'\n    try:\n        d=json.load(open(p))\n        print(f'batch {i}: keys={list(d.keys())[:8]}, output_preview={str(d.get(\\\"output\\\",\\\"\\\"))[:120]}')\n    except Exception as e:\n        print(f'batch {i}: ERROR {e}')\n\"",
  "description": "All-open execution batches"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-open/.megaplan/plans/reliability-20260424-235843/execution_batch_1.json
/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-open/.megaplan/plans/reliability-20260424-235843/execution_batch_2.json
/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-open/.megaplan/plans/reliability-20260424-235843/execution_batch_3.json
/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-open/.megaplan/plans/reliability-20260424-235843/execution_batch_4.json
/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-open/.megaplan/plans/reliability-20260424-235843/execution_batch_5.json
---
batch 1: keys=['output', 'files_changed', 'commands_run', 'deviations', 'task_updates', 'sense_check_acknowledgments'], output_preview=Executed T9 (final validation task). All previously-completed tasks (T1–T8) remain done with no regressions. Focused tes
batch 2: keys=['output', 'files_changed', 'commands_run', 'deviations', 'task_updates', 'sense_check_acknowledgments'], output_preview=T2 completed: Added --max-context-retries (int, default 2) and --max-cost-usd (float, default None, custom argparse type
batch 3: keys=['output', 'files_changed', 'commands_run', 'deviations', 'task_updates', 'sense_check_acknowledgments'], output_preview=Batch 3 complete. T3 (ChainSpec propagation), T4 (context-exhaustion retry), and T5 (cost-cap guard) all implemented and
batch 4: keys=['output', 'files_changed', 'commands_run', 'deviations', 'task_updates', 'sense_check_acknowledgments'], output_preview=Batch 4 complete. T6: Added exit codes cost_cap_exceeded→6 and context_retry_exhausted→7 in run_auto after blocked→5; up
batch 5: keys=['output', 'files_changed', 'commands_run', 'deviations', 'task_updates', 'sense_check_acknowledgments'], output_preview=T8 complete. Added 9 unit tests to tests/test_auto.py following existing mock-subprocess patterns. Also added context_re
```

> AGENT

Smoking gun: `result=blocked` — execute kept returning blocked. Let me see why and confirm the deepseek init failure.

> TOOL

tool_use Bash
```json
{
  "command": "python3 -c \"\nimport json\nfor p in ['all-open','all-kimi']:\n    d=json.load(open(f'/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/{p}/.megaplan/plans/reliability-20260424-235843/state.json'))\n    h=d.get('history',[])\n    for e in h:\n        if e.get('step')=='execute':\n            print(f'=== {p} execute entry ===')\n            print(json.dumps({k:v for k,v in e.items() if k not in ('environment',)}, indent=2)[:1500])\n            print()\n            break\n\"",
  "description": "Inspect execute history entry"
}
```

> TOOL

tool_result Bash
```
=== all-open execute entry ===
{
  "step": "execute",
  "timestamp": "2026-04-24T23:25:58Z",
  "duration_ms": 109131,
  "cost_usd": 0.16040885000000002,
  "result": "blocked",
  "session_mode": "persistent",
  "session_id": "9c339631-4b98-4eca-b4c9-a1f19b45dcb7",
  "agent": "hermes",
  "output_file": "execution.json",
  "artifact_hash": "sha256:25051b7e07d8825cad7fe883d62172b5377ea102677c5acc7a7cecf13b66c66a",
  "finalize_hash": "sha256:4c2102999824de9edf9b3376c29bb73604c85844b2fd77ae74d1682516d3e014",
  "approval_mode": "auto_approve"
}

=== all-kimi execute entry ===
{
  "step": "execute",
  "timestamp": "2026-04-24T23:09:18Z",
  "duration_ms": 140475,
  "cost_usd": 0.0892184216,
  "result": "blocked",
  "session_mode": "persistent",
  "session_id": "6456263b-1dac-42fe-b835-8ff87e2fdd84",
  "agent": "hermes",
  "output_file": "execution.json",
  "artifact_hash": "sha256:6cc84934e0d2f811fc184365e66d5522e82da46abae4e9c90effd21f57b28269",
  "finalize_hash": "sha256:f18520bccb8e43a8f4130f6e999c5bd34892a427e5996ddea9eb7af6038dc7b7",
  "approval_mode": "auto_approve"
}
```

> TOOL

tool_use Bash
```json
{
  "command": "cat /Users/user_c042661f/Documents/megaplan/.megaplan/bakeoffs/reliability-20260424-235843/all-deepseek/init.log 2>/dev/null | head -50 && echo \"---\" && cat /Users/user_c042661f/Documents/megaplan/.megaplan/bakeoffs/reliability-20260424-235843/all-deepseek/auto.log 2>/dev/null | head -80",
  "description": "Deepseek failure logs"
}
```

> TOOL

tool_result Bash
```
{
  "success": true,
  "step": "init",
  "plan": "reliability-20260424-235843",
  "state": "initialized",
  "summary": "Initialized plan 'reliability-20260424-235843' for project /Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-deepseek",
  "artifacts": [
    "state.json"
  ],
  "next_step": "plan",
  "auto_approve": true,
  "robustness": "standard",
  "next_step_runtime": {
    "expected_duration_seconds": {
      "min": 60,
      "max": 900
    },
    "recommended_next_check_seconds": 120,
    "duration_hint": "Expected duration: 1m-15m."
  }
}
---
[auto reliability-20260424-235843] iter 1 state=initialized next=plan valid_next=['plan']
[auto reliability-20260424-235843] running: megaplan plan --plan reliability-20260424-235843
[auto reliability-20260424-235843] phase 'plan' exited 1: [megaplan] Starting plan... Expected duration: 1m-15m.
/Users/user_c042661f/.pyenv/versions/3.11.11/lib/python3.11/site-packages/requests/__init__.py:113: RequestsDependencyWarning: urllib3 (2.6.3) or chardet (7.4.0.post1)/charset_normalizer (3.4.1) doesn't match a supported version!
  warnings.warn(
  [tool] ( •_•)>⌐■-■ musing...
  [done] (╥_╥) error, retrying... (1.0s)
⚠️  API call failed (attempt 1/3): NotFoundError
   🔌 Provider: openrouter  Model: deepseek/deepseek-v4-pro
   🌐 Endpoint: https://openrouter.ai/api/v1
   📝 Error: Error code: 404 - {'error': {'message': 'No endpoints available matching your guardrail restrictions and data policy. Configure: https://openrouter.ai/settings/privacy', 'code': 404}}
   ⏱️  Elapsed: 1.01s  Context: 2 msgs, ~3,133 tokens
🧾 Request debug dump written to: /Users/user_c042661f/.hermes/sessions/request_dump_33ca2750-081b-4fd5-bd68-9c90f7b6505c_20260424_235853_072967.json
❌ Non-retryable client error (HTTP 404). Aborting.
   🔌 Provider: openrouter  Model: deepseek/deepseek-v4-pro
   🌐 Endpoint: https://openrouter.ai/api/v1
   💡 This type of error won't be fixed by retrying.
[auto reliability-20260424-235843] iter 2 state=initialized next=plan valid_next=['plan']
[auto reliability-20260424-235843] running: megaplan plan --plan reliability-20260424-235843
[auto reliability-20260424-235843] phase 'plan' exited 1: [megaplan] Starting plan... Expected duration: 1m-15m.
/Users/user_c042661f/.pyenv/versions/3.11.11/lib/python3.11/site-packages/requests/__init__.py:113: RequestsDependencyWarning: urllib3 (2.6.3) or chardet (7.4.0.post1)/charset_normalizer (3.4.1) doesn't match a supported version!
  warnings.warn(
  [tool] ( ˘⌣˘)♡ reasoning...
  [done] (╥_╥) error, retrying... (0.5s)
⚠️  API call failed (attempt 1/3): NotFoundError
   🔌 Provider: openrouter  Model: deepseek/deepseek-v4-pro
   🌐 Endpoint: https://openrouter.ai/api/v1
   📝 Error: Error code: 404 - {'error': {'message': 'No endpoints available matching your guardrail restrictions and data policy. Configure: https://openrouter.ai/settings/privacy', 'code': 404}}
   ⏱️  Elapsed: 0.51s  Context: 2 msgs, ~3,133 tokens
🧾 Request debug dump written to: /Users/user_c042661f/.hermes/sessions/request_dump_90d97ddc-31d5-414b-b9f3-a7a649f7a6e6_20260424_235856_524157.json
❌ Non-retryable client error (HTTP 404). Aborting.
   🔌 Provider: openrouter  Model: deepseek/deepseek-v4-pro
   🌐 Endpoint: https://openrouter.ai/api/v1
   💡 This type of error won't be fixed by retrying.
[auto reliability-20260424-235843] iter 3 state=initialized next=plan valid_next=['plan']
[auto reliability-20260424-235843] running: megaplan plan --plan reliability-20260424-235843
[auto reliability-20260424-235843] phase 'plan' exited 1: [megaplan] Starting plan... Expected duration: 1m-15m.
/Users/user_c042661f/.pyenv/versions/3.11.11/lib/python3.11/site-packages/requests/__init__.py:113: RequestsDependencyWarning: urllib3 (2.6.3) or chardet (7.4.0.post1)/charset_normalizer (3.4.1) doesn't match a supported version!
  warnings.warn(
  [tool] (¬‿¬) processing...
  [done] (╥_╥) error, retrying... (0.5s)
⚠️  API call failed (attempt 1/3): NotFoundError
   🔌 Provider: openrouter  Model: deepseek/deepseek-v4-pro
   🌐 Endpoint: https://openrouter.ai/api/v1
   📝 Error: Error code: 404 - {'error': {'message': 'No endpoints available matching your guardrail restrictions and data policy. Configure: https://openrouter.ai/settings/privacy', 'code': 404}}
   ⏱️  Elapsed: 0.50s  Context: 2 msgs, ~3,133 tokens
🧾 Request debug dump written to: /Users/user_c042661f/.hermes/sessions/request_dump_bcb98413-e173-44f1-8bb7-e978b9b8e383_20260424_235900_157063.json
❌ Non-retryable client error (HTTP 404). Aborting.
   🔌 Provider: openrouter  Model: deepseek/deepseek-v4-pro
   🌐 Endpoint: https://openrouter.ai/api/v1
   💡 This type of error won't be fixed by retrying.
[auto reliability-20260424-235843] iter 4 state=initialized next=plan valid_next=['plan']
[auto reliability-20260424-235843] running: megaplan plan --plan reliability-20260424-235843
[auto reliability-20260424-235843] phase 'plan' exited 1: [megaplan] Starting plan... Expected duration: 1m-15m.
/Users/user_c042661f/.pyenv/versions/3.11.11/lib/python3.11/site-packages/requests/__init__.py:113: RequestsDependencyWarning: urllib3 (2.6.3) or chardet (7.4.0.post1)/charset_normalizer (3.4.1) doesn't match a supported version!
  warnings.warn(
  [tool] ◉_◉ reflecting...
  [done] (╥_╥) error, retrying... (0.5s)
⚠️  API call failed (attempt 1/3): NotFoundError
   🔌 Provider: openrouter  Model: deepseek/deepseek-v4-pro
   🌐 Endpoint: https://openrouter.ai/api/v1
   📝 Error: Error code: 404 - {'error': {'message': 'No endpoints available matching your guardrail restrictions and data policy. Configure: https://openrouter.ai/settings/privacy', 'code': 404}}
   ⏱️  Elapsed: 0.50s  Context: 2 msgs, ~3,133 tokens
🧾 Request debug dump written to: /Users/user_c042661f/.hermes/sessions/request_dump_9826de40-d987-4d5d-8906-d3ac2535f289_20260424_235902_925557.json
❌ Non-retryable client error (HTTP 404). Aborting.
   🔌 Provider: openrouter  Model: deepseek/deepseek-v4-pro
   🌐 Endpoint: https://openrouter.ai/api/v1
   💡 This type of error won't be fixed by retrying.
[auto reliability-20260424-235843] iter 5 state=initialized next=plan valid_next=['plan']
[auto reliability-20260424-235843] running: megaplan plan --plan reliability-20260424-235843
[auto reliability-20260424-235843] phase 'plan' exited 1: [megaplan] Starting plan... Expected duration: 1m-15m.
/Users/user_c042661f/.pyenv/versions/3.11.11/lib/python3.11/site-packages/requests/__init__.py:113: RequestsDependencyWarning: urllib3 (2.6.3) or chardet (7.4.0.post1)/charset_normalizer (3.4.1) doesn't match a supported version!
  warnings.warn(
  [tool] (◔_◔) cogitating...
  [done] (╥_╥) error, retrying... (0.5s)
⚠️  API call failed (attempt 1/3): NotFoundError
   🔌 Provider: openrouter  Model: deepseek/deepseek-v4-pro
   🌐 Endpoint: https://openrouter.ai/api/v1
   📝 Error: Error code: 404 - {'error': {'message': 'No endpoints available matching your guardrail restrictions and data policy. Configure: https://openrouter.ai/settings/privacy', 'code': 404}}
   ⏱️  Elapsed: 0.50s  Context: 2 msgs, ~3,133 tokens
```

> AGENT

Now let me grab the standard profile review.json result and check for "blocked" semantics — what's making each execute return blocked?

> TOOL

tool_use Bash
```json
{
  "command": "python3 -c \"\nimport json\nd=json.load(open('/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/standard/.megaplan/plans/reliability-20260424-235843/review.json'))\nprint('keys:', list(d.keys()))\nprint('outcome:', d.get('outcome'))\nprint('rework_items:', len(d.get('rework_items',[])))\nprint('summary:', str(d.get('summary',''))[:300])\n\"",
  "description": "Standard review.json"
}
```

> TOOL

tool_result Bash
```
keys: ['review_verdict', 'checks', 'pre_check_flags', 'verified_flag_ids', 'disputed_flag_ids', 'criteria', 'issues', 'rework_items', 'summary', 'task_verdicts', 'sense_check_verdicts']
outcome: None
rework_items: 0
summary: Approved. All must criteria are satisfied. The implementation matches the settled decisions: context retry is guarded off at N=0, context exhaustion has a dedicated exit-7 outcome, cost is summed from state history with strict `>`, exit codes are wired, and outcome JSON has a stable schema. Non-bloc
```

> TOOL

tool_use Bash
```json
{
  "command": "python3 -c \"\nimport json\nd=json.load(open('/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-kimi/.megaplan/plans/reliability-20260424-235843/execution_batch_1.json'))\n# count task statuses\ntask_updates=d.get('task_updates',[])\nfrom collections import Counter\nprint('batch1 statuses:', Counter(t.get('status') for t in task_updates))\nprint('batch1 task ids+status:', [(t.get('task_id'),t.get('status')) for t in task_updates])\n\"",
  "description": "Why are tasks blocked?"
}
```

> TOOL

tool_result Bash
```
batch1 statuses: Counter({'done': 1})
batch1 task ids+status: [('T1', 'done')]
```

> TOOL

tool_use Bash
```json
{
  "command": "python3 -c \"\nimport json\n# all-kimi: what are statuses across batches?\nfrom collections import Counter\nall_updates={}\nfor i in range(1,9):\n    p=f'/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-kimi/.megaplan/plans/reliability-20260424-235843/execution_batch_{i}.json'\n    try:\n        d=json.load(open(p))\n    except FileNotFoundError:\n        continue\n    for t in d.get('task_updates',[]):\n        all_updates[t.get('task_id')]=t.get('status')\n    print(f'batch{i}: {[(t.get(\\\"task_id\\\"),t.get(\\\"status\\\")) for t in d.get(\\\"task_updates\\\",[])]}')\nprint()\nprint('all-kimi final task statuses:', all_updates)\nprint()\n# all-open\nall_updates={}\nfor i in range(1,9):\n    p=f'/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-open/.megaplan/plans/reliability-20260424-235843/execution_batch_{i}.json'\n    try:\n        d=json.load(open(p))\n    except FileNotFoundError:\n        continue\n    for t in d.get('task_updates',[]):\n        all_updates[t.get('task_id')]=t.get('status')\n    print(f'batch{i}: {[(t.get(\\\"task_id\\\"),t.get(\\\"status\\\")) for t in d.get(\\\"task_updates\\\",[])]}')\nprint()\nprint('all-open final task statuses:', all_updates)\n\"",
  "description": "Per-batch task statuses for both hermes profiles"
}
```

> TOOL

tool_result Bash
```
batch1: [('T1', 'done')]
batch2: [('T2', 'done')]
batch3: [('T3', 'done'), ('T4', 'done')]
batch4: [('T5', 'done')]
batch5: [('T6', 'done')]
batch6: [('T7', 'done')]
batch7: [('T8', 'done')]

all-kimi final task statuses: {'T1': 'done', 'T2': 'done', 'T3': 'done', 'T4': 'done', 'T5': 'done', 'T6': 'done', 'T7': 'done', 'T8': 'done'}

batch1: [('T1', 'done'), ('T2', 'done'), ('T3', 'done'), ('T4', 'done'), ('T5', 'done'), ('T6', 'done'), ('T7', 'done'), ('T8', 'done'), ('T9', 'done')]
batch2: [('T2', 'done')]
batch3: [('T3', 'done'), ('T4', 'done'), ('T5', 'done')]
batch4: [('T6', 'done'), ('T7', 'done')]
batch5: [('T8', 'done')]

all-open final task statuses: {'T1': 'done', 'T2': 'done', 'T3': 'done', 'T4': 'done', 'T5': 'done', 'T6': 'done', 'T7': 'done', 'T8': 'done', 'T9': 'done'}
```

> AGENT

Tasks complete each batch but state stays `finalized` and result is `blocked`. Let me look at the standard execution test count + a quick look at standard's execute approach.

> TOOL

tool_use Bash
```json
{
  "command": "grep -c \"^def test_\" /Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/standard/tests/test_auto.py /Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-open/tests/test_auto.py /Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-kimi/tests/test_auto.py",
  "description": "Test function counts"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-open/tests/test_auto.py:15
/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/standard/tests/test_auto.py:18
/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-kimi/tests/test_auto.py:15
```

> TOOL

tool_use Bash
```json
{
  "command": "python3 -c \"\nimport json\nd=json.load(open('/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-open/.megaplan/plans/reliability-20260424-235843/finalize.json'))\n# Look at what's in finalize / why execute returns blocked\nprint('keys:',list(d.keys()))\n\" 2>&1 | head -10",
  "description": "Check finalize.json shape"
}
```

> TOOL

tool_result Bash
```
keys: ['tasks', 'watch_items', 'sense_checks', 'meta_commentary', 'validation', 'baseline_test_failures', 'baseline_test_command', 'baseline_test_note']
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"blocked\" /Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py 2>/dev/null | head -30",
  "description": "Look for \"blocked\" returns in execute core"
}
```

> TOOL

tool_result Bash
```
324:        enum_fields={"status": {"done", "skipped", "completed", "blocked"}},
666:    blocked = bool(blocking_reasons)
667:    if is_final_batch and all_tracked and not blocked:
676:        "blocked"
677:        if blocked
744:    if aggregate_payload is not None and not blocked:
749:    if blocked:
771:    # Surface worker-reported `status=blocked` tasks prominently. Merged
773:    # in this batch that ended in 'blocked' so supervisors see the real
775:    batch_blocked_ids = [
779:        and task.get("status") == "blocked"
782:    if blocked:
784:    if batch_blocked_ids:
786:            f"{len(batch_blocked_ids)} task(s) reported status=blocked by the worker "
791:        "success": not blocked,
806:        "blocked_task_ids": batch_blocked_ids,
808:    if next_step == "execute" and not blocked:
846:    blocked_task_ids = {
849:        if task.get("status") == "blocked" and isinstance(task.get("id"), str)
856:    # Treat blocked tasks as "satisfied" for batching only so pending tasks
858:    # raises "Unknown dependency ID" because blocked tasks are neither in the
862:        pending_tasks, completed_ids=completed_task_ids | blocked_task_ids
1033:    if blocked_task_ids:
1035:            f"Pre-existing blocked tasks treated as satisfied for scheduling: "
1036:            f"{sorted(blocked_task_ids)}. Downstream tasks ran assuming the blocked "
1090:    blocked = bool(blocking_reasons)
1091:    if not blocked and timeout_error is None:
1103:    result_value = "blocked" if blocked else "success"
1175:    elif blocked:
1186:        "success": not blocked and timeout_error is None,
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py",
  "offset": 650,
  "limit": 50
}
```

> TOOL

tool_result Read
```
650	    aggregate_payload: dict[str, Any] | None = None
651	    batch_payloads: list[dict[str, Any]] = []
652	    drift = None
653	    if is_final_batch and all_tracked:
654	        plan_mode = state["config"].get("mode", "code")
655	        batch_payloads = [read_json(path) for path in list_batch_artifacts(plan_dir)]
656	        aggregate_payload = _build_aggregate_execution_payload(
657	            batch_payloads,
658	            completed_batches=len(batch_payloads),
659	            total_batches=batches_total,
660	            mode=plan_mode,
661	        )
662	        atomic_write_json(plan_dir / "execution.json", aggregate_payload)
663	        drift = _compute_execute_scope_drift(project_dir, aggregate_payload)
664	        _append_scope_drift_blocker(blocking_reasons, state, drift)
665	
666	    blocked = bool(blocking_reasons)
667	    if is_final_batch and all_tracked and not blocked:
668	        state["current_state"] = STATE_EXECUTED
669	
670	    user_approved_gate = bool(state["meta"].get("user_approved_gate", False))
671	    approval_mode = _resolve_execute_approval_mode(
672	        auto_approve=auto_approve,
673	        user_approved_gate=user_approved_gate,
674	    )
675	    result_value = (
676	        "blocked"
677	        if blocked
678	        else "success" if (is_final_batch and all_tracked) else "partial"
679	    )
680	    append_history(
681	        state,
682	        make_history_entry(
683	            "execute",
684	            duration_ms=result.worker.duration_ms,
685	            cost_usd=result.worker.cost_usd,
686	            result=result_value,
687	            worker=result.worker,
688	            agent=result.agent,
689	            mode=result.mode,
690	            output_file=f"execution_batch_{batch_number}.json",
691	            artifact_hash=sha256_file(batch_artifact_path(plan_dir, batch_number)),
692	            finalize_hash=result.finalize_hash,
693	            approval_mode=approval_mode,
694	        ),
695	    )
696	    if aggregate_payload is not None and drift is not None:
697	        receipt_worker = WorkerResult(
698	            payload=aggregate_payload,
699	            raw_output="",
```

> AGENT

Found it. State only transitions to STATE_EXECUTED when `is_final_batch and all_tracked and not blocked`. Scope-drift triggers `_append_scope_drift_blocker`. Let me confirm:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"_append_scope_drift_blocker\\|scope_drift\\|files not claimed\" /Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py | head -20",
  "description": "Scope drift logic"
}
```

> TOOL

tool_result Bash
```
48:from megaplan.receipts.drift import collect_loc_by_file, compute_scope_drift
510:def _compute_execute_scope_drift(project_dir: Path, aggregate_payload: dict[str, Any]):
519:    return compute_scope_drift(
526:def _append_scope_drift_blocker(
534:            f"scope_drift_severity=high: unclaimed files {sorted(drift.files_added)} "
663:        drift = _compute_execute_scope_drift(project_dir, aggregate_payload)
664:        _append_scope_drift_blocker(blocking_reasons, state, drift)
769:        summary = f"[scope_drift={drift.severity}] {summary}"
1041:    drift = _compute_execute_scope_drift(project_dir, aggregate_payload)
1088:    _append_scope_drift_blocker(blocking_reasons, state, drift)
1184:        summary = f"[scope_drift={drift.severity}] {summary}"
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py",
  "offset": 510,
  "limit": 45
}
```

> TOOL

tool_result Read
```
510	def _compute_execute_scope_drift(project_dir: Path, aggregate_payload: dict[str, Any]):
511	    files_claimed = _collect_execute_claimed_paths(aggregate_payload, project_dir)
512	    try:
513	        observed_snapshot, observed_error = _capture_git_status_snapshot(project_dir)
514	    except Exception:
515	        observed_snapshot = {}
516	        observed_error = "snapshot unavailable"
517	    files_in_diff = set(observed_snapshot.keys()) if observed_error is None else set()
518	    loc_by_file = collect_loc_by_file(project_dir, files_in_diff)
519	    return compute_scope_drift(
520	        files_claimed=files_claimed,
521	        files_in_diff=files_in_diff,
522	        loc_by_file=loc_by_file,
523	    )
524	
525	
526	def _append_scope_drift_blocker(
527	    blocking_reasons: list[str],
528	    state: PlanState,
529	    drift: Any,
530	) -> None:
531	    robustness = configured_robustness(state)
532	    if drift.severity == "high" and robustness in {"robust", "superrobust"}:
533	        blocking_reasons.append(
534	            f"scope_drift_severity=high: unclaimed files {sorted(drift.files_added)} "
535	            f"with {drift.loc_added_outside_claimed} LOC outside the claimed set"
536	        )
537	
538	
539	def handle_execute_one_batch(
540	    *,
541	    root: Path,
542	    plan_dir: Path,
543	    state: PlanState,
544	    args: argparse.Namespace,
545	    batch_number: int,
546	    auto_approve: bool,
547	    agent: str,
548	    mode: str,
549	    refreshed: bool,
550	    model: str | None = None,
551	) -> StepResponse:
552	    finalize_data = read_json(plan_dir / "finalize.json")
553	    global_config = load_config()
554	    quality_config = global_config.get("quality_checks", {})
```

> AGENT

That's only for robust/superrobust. The hermes profiles likely ran at "standard" robustness. So why blocked? Let me look more carefully — it could be the `blocking_reasons` list itself populated for other reasons.

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"blocking_reasons.append\\|blocking_reasons =\" /Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py | head -20",
  "description": "All blocking reason injections"
}
```

> TOOL

tool_result Bash
```
533:        blocking_reasons.append(
634:    blocking_reasons = build_blocking_reasons(
989:        blocking_reasons = build_blocking_reasons(
1076:    blocking_reasons = build_blocking_reasons(
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py",
  "offset": 615,
  "limit": 55
}
```

> TOOL

tool_result Read
```
615	                refreshed=refreshed,
616	                auto_approve=auto_approve,
617	                args=args,
618	                batch_number=batch_number,
619	            )
620	        record_step_failure(
621	            plan_dir, state, step="execute", iteration=state["iteration"], error=error
622	        )
623	        raise
624	
625	    apply_session_update(
626	        state,
627	        "execute",
628	        result.agent,
629	        result.worker.session_id,
630	        mode=result.mode,
631	        refreshed=result.refreshed,
632	    )
633	    trace_written = _append_trace_output(plan_dir, result.worker.trace_output)
634	    blocking_reasons = build_blocking_reasons(
635	        tracked_tasks=result.merged_task_count,
636	        total_tasks=result.total_task_count,
637	        acknowledged_checks=result.acknowledged_sense_check_count,
638	        total_checks=result.total_sense_check_count,
639	        missing_task_evidence=result.missing_task_evidence,
640	    )
641	
642	    all_tasks = finalize_data.get("tasks", [])
643	    is_final_batch = batch_number == batches_total
644	    all_tracked = all(
645	        task.get("status") in {"done", "skipped"}
646	        for task in all_tasks
647	        if isinstance(task.get("id"), str)
648	    )
649	
650	    aggregate_payload: dict[str, Any] | None = None
651	    batch_payloads: list[dict[str, Any]] = []
652	    drift = None
653	    if is_final_batch and all_tracked:
654	        plan_mode = state["config"].get("mode", "code")
655	        batch_payloads = [read_json(path) for path in list_batch_artifacts(plan_dir)]
656	        aggregate_payload = _build_aggregate_execution_payload(
657	            batch_payloads,
658	            completed_batches=len(batch_payloads),
659	            total_batches=batches_total,
660	            mode=plan_mode,
661	        )
662	        atomic_write_json(plan_dir / "execution.json", aggregate_payload)
663	        drift = _compute_execute_scope_drift(project_dir, aggregate_payload)
664	        _append_scope_drift_blocker(blocking_reasons, state, drift)
665	
666	    blocked = bool(blocking_reasons)
667	    if is_final_batch and all_tracked and not blocked:
668	        state["current_state"] = STATE_EXECUTED
669
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def build_blocking_reasons\\|missing_task_evidence\" /Users/user_c042661f/Documents/megaplan/megaplan/execute/*.py /Users/user_c042661f/Documents/megaplan/megaplan/_core/*.py 2>/dev/null | head -20",
  "description": "Find build_blocking_reasons"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py:77:    missing_task_evidence: list[str]
/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py:251:def build_blocking_reasons(
/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py:257:    missing_task_evidence: list[str],
/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py:269:    if missing_task_evidence:
/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py:272:            + ", ".join(missing_task_evidence)
/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py:449:        missing_task_evidence = _check_done_task_evidence(
/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py:459:        missing_task_evidence = _check_done_task_evidence(
/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py:493:        missing_task_evidence=missing_task_evidence,
/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py:639:        missing_task_evidence=result.missing_task_evidence,
/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py:994:            missing_task_evidence=result.missing_task_evidence,
/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py:1057:        missing_task_evidence = _check_done_task_evidence(
/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py:1067:        missing_task_evidence = _check_done_task_evidence(
/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py:1081:        missing_task_evidence=missing_task_evidence,
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py",
  "offset": 251,
  "limit": 30
}
```

> TOOL

tool_result Read
```
251	def build_blocking_reasons(
252	    *,
253	    tracked_tasks: int,
254	    total_tasks: int,
255	    acknowledged_checks: int,
256	    total_checks: int,
257	    missing_task_evidence: list[str],
258	    timeout_reason: str | None = None,
259	) -> list[str]:
260	    reasons: list[str] = []
261	    if tracked_tasks < total_tasks:
262	        reasons.append(
263	            f"{total_tasks - tracked_tasks}/{total_tasks} tasks have no executor update"
264	        )
265	    if acknowledged_checks < total_checks:
266	        reasons.append(
267	            f"{total_checks - acknowledged_checks}/{total_checks} sense checks have no executor acknowledgment"
268	        )
269	    if missing_task_evidence:
270	        reasons.append(
271	            "done tasks missing both files_changed and commands_run: "
272	            + ", ".join(missing_task_evidence)
273	        )
274	    if timeout_reason is not None:
275	        reasons.append(timeout_reason)
276	    return reasons
277	
278	
279	def _merge_batch_results(
280	    *,
```

> AGENT

Got it. The hermes deviations confirm: "Done tasks missing both files_changed and commands_run: T1, T2, T3, T4, T5, T6, T7, T8". The hermes agents marked tasks done but didn't populate `files_changed` or `commands_run` — so `missing_task_evidence` triggers the blocker, blocked=True, state stays finalized.

I have all the data I need. Producing the final audit.

---

# Megaplan bake-off audit — `reliability-20260424-235843`

## Winner: `standard` (claude+codex)

It is the only profile that reached terminal `done` with an approved review, the only one that produced a tight, scope-disciplined diff (4 files, 597+/64-), and it did it for a fraction of the cost of the open-models variants. More importantly, both hermes profiles were knocked off the rails by an orthogonal megaplan bug (worker-reported `result=blocked` from missing per-task evidence) — so this run is a clean win for the reference profile and a damning signal about hermes execute-payload formatting. Pick `standard`.

---

## 1. Per-profile work assessment

All three profiles converged on the *same broad design*: extend `DriverOutcome` with cost/retry fields, add two argparse types (`_non_negative_float` etc.), add a cost-cap branch and a context-exhaustion branch in `drive()`, add exit codes 6 & 7. They diverge sharply on placement, taste, and discipline.

### Task A (context-retry-with-fresh)

| | placement | retry mechanism | counts toward stall? |
|--|--|--|--|
| **standard** | inline `while` loop *immediately after* `_run_megaplan` returns, before stall-detection branches see the failure | `cmd = [*cmd, "--fresh"]` (idempotent: `if "--fresh" not in cmd`) | no — retry loop returns on success or `context_retry_exhausted` |
| **all-open** | inside the `code != 0` branch with a `while/else` Python construct | `cmd + ["--fresh"]` each call | partially — same iteration |
| **all-kimi** | sets a `pending_fresh = bool` flag and `continue`s back to top of loop, where `_phase_command(next_step, fresh=pending_fresh)` re-derives the command. Also `stall_count = 0` and `last_state = None` to deliberately suppress stall detection | flag-driven | no — explicitly resets stall |

Standard's regex (`CONTEXT_EXHAUSTION_FRAGMENT`) is module-level, lower-cased once, and matched lower-case against `(out + err)` — clean. All-open and all-kimi inline the same fragment string. All-kimi is the most elegant in concept (refactor `_phase_command` to take `fresh: bool`) but pays for it with significant added state (`pending_fresh`) and a stall-counter reset that violates the spec's intent ("don't loop forever").

Compelling snippet — **standard** (`megaplan/auto.py:533-565`), terse and self-contained:

```python
while (
    next_step == "execute"
    and code != 0
    and CONTEXT_EXHAUSTION_FRAGMENT.lower() in ((out or "") + (err or "")).lower()
):
    if context_retry_count >= max_context_retries:
        return _outcome("context_retry_exhausted", ...)
    context_retry_count += 1
    if "--fresh" not in cmd:
        cmd = [*cmd, "--fresh"]
    code, out, err = _run_megaplan(cmd, cwd=cwd, timeout=phase_timeout)
```

### Task B (`--max-cost-usd`)

The spec says: *"Sum `cost_usd` across every entry in `state["history"]`."* Two profiles obeyed; one cheated.

- **standard** — `_sum_history_cost_usd(plan_dir)` reads `state.json`, iterates history, sums `cost_usd`. Defensive: `(OSError, json.JSONDecodeError)`, `float(... or 0.0)` with `(TypeError, ValueError)` guards. Called from `_outcome()` so every terminal branch surfaces the live total.
- **all-kimi** — same approach, `_compute_total_cost()` closure that reads state.json and falls back to `status.get("total_cost_usd", 0.0)` if read fails.
- **all-open** — *uses `status.get("total_cost_usd", 0.0)` only.* That field doesn't exist on the status object — silent always-zero. The check is dead code. Their own SC5 acknowledgment even brags about removing the "dead-code history fallback" — but the live code is the dead path. **This is a real bug.**

Compelling snippet — **all-kimi** closure (`megaplan/auto.py:244-253`):

```python
def _compute_total_cost() -> float:
    if plan_dir is None:
        return float(status.get("total_cost_usd", 0.0) or 0.0)
    try:
        state_data = json.loads((plan_dir / "state.json").read_text(encoding="utf-8"))
        return sum(
            float(entry.get("cost_usd", 0.0) or 0.0)
            for entry in state_data.get("history", [])
        )
    except (OSError, json.JSONDecodeError):
        return float(status.get("total_cost_usd", 0.0) or 0.0)
```

### Code quality, tests, scope

- Tests: standard 18, all-open 15, all-kimi 15. Standard ships the most coverage and is the only profile that doesn't touch chain.py / init.py / chain.yaml.example — i.e. the only one that respected the task's stated scope.
- Scope drift: all-open and all-kimi both swept in `chain.py`, `handlers/init.py`, `cloud/templates/chain.yaml.example`. Their own audits flagged it: `execution_audit.json` has *"Git status shows changed files not claimed by any task: megaplan/auto.py, megaplan/chain.py, …"*. Standard's audit only flagged a stale claim and a pre-existing test edit (`tests/test_workers.py` looks unrelated, ~4 lines).
- All-open's all-tasks-done-in-batch-1 then re-emitted as 4 more batches reveals a confused executor that kept re-running the same plan after the first pass already "did" everything.

## 2. Why the hermes profiles stalled

Each `execute` invocation **succeeded** at the worker level but state.json records `result: "blocked"` and `current_state` never advanced past `finalized`. Root cause is in `megaplan/execute/core.py:251` `build_blocking_reasons` + the deviation log on disk:

> *"Done tasks missing both files_changed and commands_run: T1, T2, T3, T4, T5, T6, T7, T8"*

The hermes worker marks each task `done` in `task_updates` but emits empty `files_changed: []` and empty `commands_run: []`. `build_blocking_reasons` flags this, sets `blocked=True`, the `if … and not blocked: state["current_state"] = STATE_EXECUTED` guard (`core.py:667`) fails, the state stays `finalized`. The auto-driver sees `state=finalized next=execute` again and reruns. Each rerun produces a *new* batch file (5 of them on each profile) but the work was already on disk after batch 1 — re-execution is no-op-but-still-blocked.

This is **not** the context-window class of failure the task targeted — codex never blew up. It's hermes failing the executor's evidence schema. So both retry features the profiles built would have fired never. The auto-driver loop is also blind to `result=blocked` in history (it only reads `state` from status), which is why the stall-threshold path eventually catches it after 5 iterations — exactly as the existing `--stall-threshold` is supposed to. The driver behaved correctly; the executor evidence rule did.

Each subprocess exited 0 (event log shows `running:` with no `phase 'execute' exited` message at iters 12-17) — so no retry/path was triggerable.

## 3. Cost vs value

| profile | total $ | tokens | terminal | shipped? |
|--|--|--|--|--|
| standard | $3.71 (codex phases recorded $0 — real cost likely $7-10) | n/a | done/approved | **yes** |
| all-open | $14.13 | ~18.8M | stalled | partial work, drift |
| all-kimi | $4.57 | ~11.0M | stalled | partial work, drift |
| all-deepseek | $0 | 0 | dead | no |

Glm-5.1 critique alone is **$2.79 + $2.60 + $4.58 across three critique passes = $9.97** of the all-open total. That's the dominant line item by far. Cause: glm-5.1 critique wrote 4-8M token critiques per pass — way over what kimi or codex emit. This is a profile-config issue (glm critique is over-eager / under-truncated), not a pipeline issue. All-kimi shows that kimi is dramatically more efficient (~$1.20/critique, similar token count) — kimi-as-everything is the cheap-and-stalled outcome, ~$1.10/M tokens vs glm at ~$0.62/M but with 2x the volume.

Best $/work-shipped: **standard by a wide margin** since it's the only one that shipped. Best $/work-attempted: kimi. Worst: glm-5.1 critique.

## 4. Three follow-up bugs ranked

1. **Worker `result=blocked` is invisible to the auto-driver.** When execute returns 0 but flips state.json to `result: "blocked"` because of evidence-schema gaps, the driver enters the same `state=finalized → run execute` loop the task tried to fix — a dead-loop that *only* stall-threshold catches. The driver should detect the most-recent history entry's `result == "blocked"` and treat it as a phase failure (or surface a new outcome status, e.g. `worker_blocked`). This is the single most impactful bug in this run: it killed two profiles end-to-end.

2. **Codex phases record `cost_usd: 0` in standard profile.** state.json shows `cost=$0` for every codex step (critique, execute, review, gate). True spend is invisible — `--max-cost-usd` is broken for this profile because the cap will never see codex spend. Same instrumentation as claude phases needed in the codex worker path.

3. **`bakeoff run --detach` doesn't write outcome.json.** The bakeoff manifest's `outcome` fields are all `null` and `terminated_at: null` — the supervisor evidently captured outcomes only via stdout (auto.log tail) but never wrote per-profile `outcome.json` to disk. Also `phase: "running"` in `bakeoff.json` despite all four subprocs being long-since terminal.

Honorable mentions: (a) the spec asked for argparse to reject "negative, non-numeric"; only standard and all-kimi properly subclass `ArgumentTypeError` for both; all-open lets `float("abc")` raise the default ValueError. (b) `chain.py`/`init.py` needing parallel updates is a real ergonomic gap — the hermes profiles correctly identified plumbing the new fields through the chain handler but did so without adding the work to their plan, hence the scope-drift findings. The right answer is for megaplan's planner to surface this as a known-coupling rule.

Key files:
- `/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/standard/megaplan/auto.py` — winning impl
- `/Users/user_c042661f/Documents/.megaplan-worktrees/reliability-20260424-235843/all-open/megaplan/auto.py:300` — broken cost-cap (reads non-existent status field)
- `/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py:251-276` — `build_blocking_reasons`, root cause of hermes stall
- `/Users/user_c042661f/Documents/megaplan/megaplan/execute/core.py:666-668` — state-transition gate that stays `finalized` on `blocked`
