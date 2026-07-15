> DEVELOPER

Read the following files in /Users/user_c042661f/Documents/megaplan and report their full contents:
1. megaplan/prompts/prep.py
2. megaplan/prompts/execute.py
3. megaplan/prompts/review.py
4. megaplan/prompts/__init__.py
5. megaplan/prompts/finalize.py

Also check if there's a megaplan/prompts/_shared.py or similar shared helpers file. Report all contents.

> AGENT

I'll read all the specified files in the megaplan/prompts directory.

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/prep.py"
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
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/execute.py"
}
```

> TOOL

tool_result Read
```
1	"""Execute-phase prompt builders and helpers."""
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
21	
22	_EXECUTE_OUTPUT_SHAPE_EXAMPLE = textwrap.dedent(
23	    """
24	    ```json
25	    {
26	      "output": "Implemented the approved plan and captured execution evidence.",
27	      "files_changed": ["megaplan/handlers.py", "megaplan/evaluation.py"],
28	      "commands_run": ["pytest tests/test_megaplan.py -k evidence"],
29	      "deviations": [],
30	      "task_updates": [
31	        {
32	          "task_id": "T6",
33	          "status": "done",
34	          "executor_notes": "Caught the empty-strings edge case while checking execution evidence: blank `commands_run` entries still leave the task uncovered, so the missing-evidence guard behaves correctly.",
35	          "files_changed": ["megaplan/handlers.py"],
36	          "commands_run": ["pytest tests/test_megaplan.py -k execute"]
37	        },
38	        {
39	          "task_id": "T7",
40	          "status": "done",
41	          "executor_notes": "Confirmed the happy path still records task evidence after the prompt updates by rerunning focused tests and checking the tracked task summary stayed intact.",
42	          "files_changed": ["megaplan/prompts.py"],
43	          "commands_run": ["pytest tests/test_prompts.py -k review"]
44	        },
45	        {
46	          "task_id": "T8",
47	          "status": "done",
48	          "executor_notes": "Kept the rubber-stamp thresholds centralized in evaluation so sense checks and reviewer verdicts share one policy entry point while still using different strictness levels.",
49	          "files_changed": ["megaplan/evaluation.py"],
50	          "commands_run": ["pytest tests/test_evaluation.py -k rubber_stamp"]
51	        },
52	        {
53	          "task_id": "T11",
54	          "status": "skipped",
55	          "executor_notes": "Skipped because upstream work is not ready yet; no repo changes were made for this task.",
56	          "files_changed": [],
57	          "commands_run": []
58	        }
59	      ],
60	      "sense_check_acknowledgments": [
61	        {
62	          "sense_check_id": "SC6",
63	          "executor_note": "Confirmed execute only blocks when both files_changed and commands_run are empty for a done task."
64	        }
65	      ]
66	    }
67	    ```
68	    """
69	).strip()
70	
71	_EXECUTE_REQUIREMENTS_TEMPLATE = textwrap.dedent(
72	    """
73	    Requirements:
74	    - Implement the intent, not just the text.
75	    - Adapt if repository reality contradicts the plan.
76	    - Report deviations explicitly.
77	    - Do not over-engineer beyond what the plan prescribes — no str() wraps, .get() fallbacks, or try/except guards unless the plan called for them or you found a concrete reason.
78	    - Do NOT fix unrelated issues you encounter (e.g., dependency compatibility, Python version workarounds). Only change files directly needed for the task. If tests need updating, only update tests that are directly related to your fix.
79	    - If you cannot build the project from source (e.g., C extension compilation failures), report the build failure explicitly. Do NOT fall back to testing against an installed or cached package — that tests the wrong codebase and produces false positives.
80	    - If you cannot verify your changes (tests missing or unrunnable), treat this as high risk — re-examine your implementation with extra scrutiny instead of accepting it on faith.
81	    - If tests fail, read the traceback carefully. Diagnose WHY — don't just retry. Common causes: wrong function/method used, missing import, incorrect type, edge case not handled. Fix the root cause, then re-run.
82	    - When verifying changes, run the entire test file or module (e.g., `pytest tests/test_foo.py`), not individual test functions. Individual tests miss regressions in the same module.
83	    - finalize.json includes baseline_test_failures — a list of test IDs that were already failing before your changes. If a test fails and its ID appears in baseline_test_failures, it is pre-existing — do not scope-creep into fixing it. If baseline_test_failures is null, the baseline could not be captured; use your judgment but err on the side of assuming failures are regressions. You MUST still re-run the FULL test suite with your changes applied — pre-existing failures do not excuse skipping verification. Never narrow to individual test functions and stop.
84	    - Before declaring the work complete, write a short script (not a full test) that reproduces the exact bug or incorrect behavior described in the task. Run it to confirm the fix resolves the issue. Then delete the script so it does not appear in the final diff. If the task description is too vague to write a concrete reproduction, note this explicitly in executor_notes.
85	    - Output concrete files changed and commands run. `files_changed` means files you WROTE or MODIFIED — not files you read or verified. Only list files where you made actual edits.
86	    - Use the tasks in `finalize.json` as the execution boundary.
87	    - Best-effort progress checkpointing: if `{checkpoint_path}` is writable, then after each completed task read the full file, update that task's `status`, `executor_notes`, `files_changed`, and `commands_run`, and write the full file back. Do NOT write to `finalize.json` directly — the harness owns that file.
88	    - Best-effort sense-check checkpointing: if `{checkpoint_path}` is writable, then after each sense check acknowledgment read the full file again, update that sense check's `executor_note`, and write the full file back.
89	    - Always use full read-modify-write updates for `{checkpoint_path}` instead of partial edits. If the sandbox blocks writes, continue execution and rely on the structured output below.
90	    - Structured output remains the authoritative final summary for this step. Disk writes are progress checkpoints for timeout recovery only.
91	    - Return `task_updates` with one object per completed or skipped task.
92	    - `task_updates[].status` must be either `done` or `skipped`. Never return `pending` in execute output.
93	    - If a task is blocked by environment limits, missing devices, or manual-only validation that cannot happen in this session, return `status: "skipped"` and explain the remaining manual follow-up in `executor_notes` and `deviations`.
94	    - Return `sense_check_acknowledgments` with one object per sense check.
95	    - Keep `executor_notes` verification-focused: explain why your changes are correct. The diff already shows what changed; notes should cover edge cases caught, expected behaviors confirmed, or design choices made.
96	    - Follow this JSON shape exactly:
97	    {output_shape}
98	    """
99	).strip()
100	
101	
102	def _execute_review_block(plan_dir: Path) -> str:
103	    review_path = plan_dir / "review.json"
104	    if not review_path.exists():
105	        return "No prior `review.json` exists. Treat this as the first execution pass."
106	    return textwrap.dedent(
107	        f"""
108	        Previous review findings to address on this execution pass (`review.json`):
109	        {json_dump(read_json(review_path)).strip()}
110	        """
111	    ).strip()
112	
113	
114	def _execute_nudges(
115	    finalize_data: dict[str, Any], plan_dir: Path, root: Path | None
116	) -> str:
117	    nudge_lines: list[str] = []
118	    sense_checks = finalize_data.get("sense_checks", [])
119	    if sense_checks:
120	        nudge_lines.append(
121	            "Sense checks to keep in mind during execution (reviewer will verify these):"
122	        )
123	        for sense_check in sense_checks:
124	            nudge_lines.append(
125	                f"- {sense_check['id']} ({sense_check['task_id']}): {sense_check['question']}"
126	            )
127	    watch_items = finalize_data.get("watch_items", [])
128	    if watch_items:
129	        nudge_lines.append("Watch items to keep visible during execution:")
130	        for item in watch_items:
131	            nudge_lines.append(f"- {item}")
132	    debt_watch_items = _debt_watch_lines(plan_dir, root)
133	    if debt_watch_items:
134	        nudge_lines.append("Debt watch items (do not make these worse):")
135	        for item in debt_watch_items:
136	            nudge_lines.append(f"- {item}")
137	    return "\n".join(nudge_lines)
138	
139	
140	def _execute_rerun_guidance(plan_dir: Path, finalize_data: dict[str, Any]) -> str:
141	    tasks = finalize_data.get("tasks", [])
142	    done_tasks = [task for task in tasks if task.get("status") in ("done", "skipped")]
143	    pending_tasks = [task for task in tasks if task.get("status") == "pending"]
144	    if done_tasks and pending_tasks:
145	        done_ids = ", ".join(task["id"] for task in done_tasks)
146	        pending_ids = ", ".join(task["id"] for task in pending_tasks)
147	        return (
148	            f"Re-execution: {len(done_tasks)} tasks already tracked ({done_ids}). "
149	            f"Focus on the {len(pending_tasks)} remaining tasks ({pending_ids}). "
150	            "You must still return task_updates for ALL tasks (including already-tracked ones) — "
151	            "for previously done tasks, preserve their existing status and notes."
152	        )
153	    if done_tasks and not pending_tasks:
154	        review_data = (
155	            read_json(plan_dir / "review.json")
156	            if (plan_dir / "review.json").exists()
157	            else {}
158	        )
159	        rework_items = review_data.get("rework_items", [])
160	        if rework_items:
161	            rework_lines = []
162	            for item in rework_items:
163	                if not isinstance(item, dict):
164	                    continue
165	                task_id = item.get("task_id", "?")
166	                issue = item.get("issue", "")
167	                expected = item.get("expected", "")
168	                actual = item.get("actual", "")
169	                evidence = item.get("evidence_file", "")
170	                entry = f"  - [{task_id}] {issue}"
171	                if expected:
172	                    entry += f"\n    expected: {expected}"
173	                if actual:
174	                    entry += f"\n    actual: {actual}"
175	                if evidence:
176	                    entry += f"\n    evidence: {evidence}"
177	                rework_lines.append(entry)
178	            issue_list = "\n".join(rework_lines)
179	        else:
180	            review_issues = review_data.get("issues", [])
181	            issue_list = (
182	                "\n".join(f"  - {issue}" for issue in review_issues)
183	                if review_issues
184	                else "  (see review.json above for details)"
185	            )
186	        return (
187	            "REWORK REQUIRED: all tasks are already tracked but the reviewer kicked this back.\n"
188	            f"Review issues to fix:\n{issue_list}\n\n"
189	            "You MUST make code changes to address each issue — do not return success without modifying files. "
190	            "For each issue, either fix it and list the file in files_changed, or explain in deviations why no change is needed with line-level evidence. "
191	            "Return task_updates for all tasks with updated evidence."
192	        )
193	    return ""
194	
195	
196	def _execute_approval_note(state: PlanState) -> str:
197	    if state["config"].get("auto_approve"):
198	        return (
199	            "Note: User chose auto-approve mode. This execution was not manually "
200	            "reviewed at the gate. Exercise extra caution on destructive operations."
201	        )
202	    if state["meta"].get("user_approved_gate"):
203	        return "Note: User explicitly approved this plan at the gate checkpoint."
204	    return "Note: Review mode is enabled. Execute should only be running after explicit gate approval."
205	
206	
207	def _execute_prompt(state: PlanState, plan_dir: Path, root: Path | None = None) -> str:
208	    project_dir = Path(state["config"]["project_dir"])
209	    prep_block, prep_instruction = _render_prep_block(plan_dir)
210	    finalize_data = read_json(plan_dir / "finalize.json")
211	    checkpoint_path = str(plan_dir / "execution_checkpoint.json")
212	    latest_meta = read_json(latest_plan_meta_path(plan_dir, state))
213	    gate = read_json(plan_dir / "gate.json")
214	    robustness = configured_robustness(state)
215	    prior_review_block = _execute_review_block(plan_dir)
216	    rerun_guidance = _execute_rerun_guidance(plan_dir, finalize_data)
217	    approval_note = _execute_approval_note(state)
218	    execution_nudges = _execute_nudges(finalize_data, plan_dir, root)
219	    requirements_block = _EXECUTE_REQUIREMENTS_TEMPLATE.format(
220	        checkpoint_path=checkpoint_path,
221	        output_shape=_EXECUTE_OUTPUT_SHAPE_EXAMPLE,
222	    )
223	    return textwrap.dedent(
224	        f"""
225	        Execute the approved plan in the repository.
226	
227	        Project directory:
228	        {project_dir}
229	
230	        {prep_block}
231	
232	        {prep_instruction}
233	
234	        {intent_and_notes_block(state)}
235	
236	        Execution tracking source of truth (`finalize.json`):
237	        {json_dump(finalize_data).strip()}
238	
239	        Absolute checkpoint path for best-effort progress checkpoints (NOT `finalize.json`):
240	        {checkpoint_path}
241	
242	        Plan metadata:
243	        {json_dump(latest_meta).strip()}
244	
245	        Gate summary:
246	        {json_dump(gate).strip()}
247	
248	        {prior_review_block}
249	
250	        {rerun_guidance}
251	
252	        {approval_note}
253	        Robustness level: {robustness}.
254	
255	        {requirements_block}
256	
257	        {execution_nudges}
258	        """
259	    ).strip()
260	
261	
262	def _execute_batch_prompt(
263	    state: PlanState,
264	    plan_dir: Path,
265	    batch_task_ids: list[str],
266	    completed_task_ids: set[str] | None = None,
267	    root: Path | None = None,
268	) -> str:
269	    completed = set(completed_task_ids or set())
270	    finalize_data = read_json(plan_dir / "finalize.json")
271	    all_tasks = finalize_data.get("tasks", [])
272	    tasks_by_id = {
273	        task["id"]: task
274	        for task in all_tasks
275	        if isinstance(task, dict) and isinstance(task.get("id"), str)
276	    }
277	    batch_tasks = [
278	        tasks_by_id[task_id] for task_id in batch_task_ids if task_id in tasks_by_id
279	    ]
280	    completed_tasks = [
281	        task
282	        for task_id, task in tasks_by_id.items()
283	        if task_id in completed and task_id not in set(batch_task_ids)
284	    ]
285	    batch_sense_checks = [
286	        sense_check
287	        for sense_check in finalize_data.get("sense_checks", [])
288	        if sense_check.get("task_id") in set(batch_task_ids)
289	    ]
290	    batch_sense_check_ids = [
291	        sense_check["id"]
292	        for sense_check in batch_sense_checks
293	        if isinstance(sense_check.get("id"), str)
294	    ]
295	    global_batches = compute_task_batches(all_tasks)
296	    batch_number = next(
297	        (
298	            index + 1
299	            for index, batch in enumerate(global_batches)
300	            if batch == batch_task_ids
301	        ),
302	        1,
303	    )
304	    batch_total = len(global_batches) or 1
305	    checkpoint_path = str(batch_artifact_path(plan_dir, batch_number))
306	    prior_batch_deviations = "None"
307	    if batch_number > 1:
308	        prior_batch_artifact = batch_artifact_path(plan_dir, batch_number - 1)
309	        if prior_batch_artifact.exists():
310	            try:
311	                prior_batch_payload = read_json(prior_batch_artifact)
312	            except (OSError, ValueError):
313	                prior_batch_payload = {}
314	            raw_deviations = prior_batch_payload.get("deviations", [])
315	            if isinstance(raw_deviations, list):
316	                deviations = [item for item in raw_deviations if isinstance(item, str)]
317	                if deviations:
318	                    prior_batch_deviations = json_dump(deviations).strip()
319	    approval_note = (
320	        "Note: User chose auto-approve mode. This execution was not manually reviewed at the gate. Exercise extra caution on destructive operations."
321	        if state["config"].get("auto_approve")
322	        else (
323	            "Note: User explicitly approved this plan at the gate checkpoint."
324	            if state["meta"].get("user_approved_gate")
325	            else "Note: Review mode is enabled. Execute should only be running after explicit gate approval."
326	        )
327	    )
328	    debt_watch_items = _debt_watch_lines(plan_dir, root)
329	    debt_watch_block = (
330	        "\n".join(
331	            [
332	                "Debt watch items (do not make these worse):",
333	                *[f"- {item}" for item in debt_watch_items],
334	            ]
335	        )
336	        if debt_watch_items
337	        else "Debt watch items (do not make these worse):\n- None."
338	    )
339	    return textwrap.dedent(
340	        f"""
341	        Execute the approved plan in the repository.
342	
343	        Project directory:
344	        {Path(state["config"]["project_dir"])}
345	
346	        {intent_and_notes_block(state)}
347	
348	        Batch framing:
349	        - Execute batch {batch_number} of {batch_total}.
350	        - Actionable task IDs for this batch: {batch_task_ids}
351	        - Already completed task IDs available as dependency context: {sorted(completed)}
352	
353	        Actionable tasks for this batch:
354	        {json_dump(batch_tasks).strip()}
355	
356	        Completed task context (already satisfied, do not re-execute unless directly required by current edits):
357	        {json_dump(completed_tasks).strip()}
358	
359	        Prior batch deviations (address if applicable):
360	        {prior_batch_deviations}
361	
362	        Batch-scoped sense checks:
363	        {json_dump(batch_sense_checks).strip()}
364	
365	        Full execution tracking source of truth (`finalize.json`):
366	        {json_dump(finalize_data).strip()}
367	
368	        {debt_watch_block}
369	
370	        {approval_note}
371	        Robustness level: {configured_robustness(state)}.
372	
373	        Requirements:
374	        - Execute only the actionable tasks in this batch.
375	        - Treat completed tasks as dependency context, not new work.
376	        - Return structured JSON only.
377	        - Only produce `task_updates` for these tasks: [{", ".join(batch_task_ids)}]
378	        - Only produce `sense_check_acknowledgments` for these sense checks: [{", ".join(batch_sense_check_ids)}]
379	        - Do not include updates for tasks or sense checks outside this batch.
380	        - Keep `executor_notes` verification-focused.
381	        - Best-effort progress checkpointing: if `{checkpoint_path}` is writable, checkpoint task and sense-check updates there (not `finalize.json`). The harness owns `finalize.json`.
382	        - When verifying changes, run the entire test file or module, not individual test functions. Individual tests miss regressions.
383	        - finalize.json includes baseline_test_failures — a list of test IDs that were already failing before your changes. If a test fails and its ID appears in baseline_test_failures, it is pre-existing — do not scope-creep into fixing it. If baseline_test_failures is null, the baseline could not be captured; use your judgment but err on the side of assuming failures are regressions. You MUST still re-run the FULL test suite with your changes applied — pre-existing failures do not excuse skipping verification. Never narrow to individual test functions and stop.
384	        - If this batch includes the final verification task, write a short script that reproduces the exact bug described in the task, run it to confirm the fix resolves it, then delete the script.
385	        """
386	    ).strip()
387
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/review.py"
}
```

> TOOL

tool_result Read
```
1	"""Review-phase prompt builders."""
2	
3	from __future__ import annotations
4	
5	import json
6	import re
7	import textwrap
8	from pathlib import Path
9	from typing import Any
10	
11	from megaplan._core import (
12	    collect_git_diff_patch,
13	    collect_git_diff_summary,
14	    intent_and_notes_block,
15	    json_dump,
16	    latest_plan_meta_path,
17	    latest_plan_path,
18	    load_flag_registry,
19	    read_json,
20	)
21	from megaplan.types import PlanState
22	
23	
24	def _check_field(check: Any, name: str) -> Any:
25	    if isinstance(check, dict):
26	        return check.get(name)
27	    return getattr(check, name)
28	
29	
30	def _review_check_flag_id(check_id: str, index: int) -> str:
31	    stem = re.sub(r"[^A-Z0-9]+", "_", check_id.upper()).strip("_") or "CHECK"
32	    return f"REVIEW-{stem}-{index:03d}"
33	
34	
35	def _review_template_payload(plan_dir: Path) -> dict[str, object]:
36	    finalize_data = read_json(plan_dir / "finalize.json")
37	
38	    task_verdicts = []
39	    for task in finalize_data.get("tasks", []):
40	        task_id = task.get("id", "")
41	        if task_id:
42	            task_verdicts.append({
43	                "task_id": task_id,
44	                "reviewer_verdict": "",
45	                "evidence_files": [],
46	            })
47	
48	    sense_check_verdicts = []
49	    for sc in finalize_data.get("sense_checks", []):
50	        sc_id = sc.get("id", "")
51	        if sc_id:
52	            sense_check_verdicts.append({
53	                "sense_check_id": sc_id,
54	                "verdict": "",
55	            })
56	
57	    criteria = []
58	    for crit in finalize_data.get("success_criteria", []):
59	        if isinstance(crit, dict) and crit.get("name"):
60	            criteria.append({
61	                "name": crit["name"],
62	                "priority": crit.get("priority", "must"),
63	                "pass": "",
64	                "evidence": "",
65	            })
66	
67	    return {
68	        "review_verdict": "",
69	        "criteria": criteria,
70	        "issues": [],
71	        "rework_items": [],
72	        "summary": "",
73	        "task_verdicts": task_verdicts,
74	        "sense_check_verdicts": sense_check_verdicts,
75	    }
76	
77	
78	def _parallel_review_context(state: PlanState, plan_dir: Path) -> dict[str, Any]:
79	    project_dir = Path(state["config"]["project_dir"])
80	    gate = read_json(plan_dir / "gate.json")
81	    settled_decisions = gate.get("settled_decisions", [])
82	    if not isinstance(settled_decisions, list):
83	        settled_decisions = []
84	    return {
85	        "project_dir": project_dir,
86	        "intent_block": intent_and_notes_block(state),
87	        "git_diff": collect_git_diff_patch(project_dir),
88	        "finalize_data": read_json(plan_dir / "finalize.json"),
89	        "settled_decisions": settled_decisions,
90	    }
91	
92	
93	def _build_review_checks_template(
94	    plan_dir: Path,
95	    state: PlanState,
96	    checks: tuple[Any, ...],
97	) -> list[dict[str, object]]:
98	    checks_template: list[dict[str, object]] = []
99	    for check in checks:
100	        entry: dict[str, object] = {
101	            "id": _check_field(check, "id"),
102	            "question": _check_field(check, "question"),
103	            "guidance": _check_field(check, "guidance") or "",
104	            "findings": [],
105	        }
106	        checks_template.append(entry)
107	
108	    if state.get("iteration", 1) <= 1:
109	        return checks_template
110	
111	    prior_path = plan_dir / "review.json"
112	    if not prior_path.exists():
113	        return checks_template
114	
115	    prior = read_json(prior_path)
116	    active_check_ids = {_check_field(check, "id") for check in checks}
117	    prior_checks = {
118	        check.get("id"): check
119	        for check in prior.get("checks", [])
120	        if isinstance(check, dict) and check.get("id") in active_check_ids
121	    }
122	    registry = load_flag_registry(plan_dir)
123	    flag_status = {flag["id"]: flag.get("status", "open") for flag in registry.get("flags", [])}
124	
125	    for entry in checks_template:
126	        check_id = str(entry["id"])
127	        prior_check = prior_checks.get(check_id)
128	        if not isinstance(prior_check, dict):
129	            continue
130	        prior_findings = []
131	        flagged_index = 0
132	        for finding in prior_check.get("findings", []):
133	            if not isinstance(finding, dict):
134	                continue
135	            flagged = bool(finding.get("flagged"))
136	            status = "n/a"
137	            if flagged:
138	                flagged_index += 1
139	                status = flag_status.get(_review_check_flag_id(check_id, flagged_index), "open")
140	            prior_findings.append({
141	                "detail": finding.get("detail", ""),
142	                "flagged": flagged,
143	                "status": finding.get("status", status),
144	            })
145	        if prior_findings:
146	            entry["prior_findings"] = prior_findings
147	    return checks_template
148	
149	
150	def _write_single_check_review_template(
151	    plan_dir: Path,
152	    state: PlanState,
153	    check: Any,
154	    filename: str,
155	) -> Path:
156	    template: dict[str, object] = {
157	        "checks": _build_review_checks_template(plan_dir, state, (check,)),
158	        "flags": [],
159	        "pre_check_flags": [],
160	        "verified_flag_ids": [],
161	        "disputed_flag_ids": [],
162	    }
163	    output_path = plan_dir / filename
164	    output_path.write_text(json.dumps(template, indent=2), encoding="utf-8")
165	    return output_path
166	
167	
168	def _write_criteria_verdict_review_template(
169	    plan_dir: Path,
170	    state: PlanState,
171	    filename: str,
172	) -> Path:
173	    del state
174	    output_path = plan_dir / filename
175	    output_path.write_text(json.dumps(_review_template_payload(plan_dir), indent=2), encoding="utf-8")
176	    return output_path
177	
178	
179	def _settled_decisions_review_block(settled_decisions: list[object]) -> str:
180	    if not settled_decisions:
181	        return "Settled decisions from gate (`gate.json`): []"
182	    return textwrap.dedent(
183	        f"""
184	        Settled decisions from gate (`gate.json`):
185	        {json_dump(settled_decisions).strip()}
186	        """
187	    ).strip()
188	
189	
190	def single_check_review_prompt(
191	    state: PlanState,
192	    plan_dir: Path,
193	    root: Path | None,
194	    check: Any,
195	    output_path: Path,
196	    pre_check_flags: list[dict[str, Any]],
197	) -> str:
198	    del root
199	    context = _parallel_review_context(state, plan_dir)
200	    check_id = _check_field(check, "id")
201	    question = _check_field(check, "question")
202	    guidance = _check_field(check, "guidance") or ""
203	    iteration = state.get("iteration", 1)
204	    iteration_context = ""
205	    if iteration > 1:
206	        iteration_context = (
207	            "\n\nThis is review iteration {iteration}. The template may include prior findings with their current "
208	            "flag status. Verify whether previously raised concerns were actually fixed before you carry them forward."
209	        ).format(iteration=iteration)
210	    return textwrap.dedent(
211	        f"""
212	        You are an independent parallel-review checker. Review one focused dimension of the executed patch against the original issue text.
213	
214	        Project directory:
215	        {context["project_dir"]}
216	
217	        {context["intent_block"]}
218	
219	        Full git diff:
220	        {context["git_diff"]}
221	
222	        Execution tracking state (`finalize.json`):
223	        {json_dump(context["finalize_data"]).strip()}
224	
225	        {_settled_decisions_review_block(context["settled_decisions"])}
226	
227	        Advisory mechanical pre-check flags (copy these verbatim into `pre_check_flags` in the output file):
228	        {json_dump(pre_check_flags).strip()}
229	
230	        Your output template is at: {output_path}
231	        Read this file first. It contains exactly one check slot.
232	
233	        Check ID: {check_id}
234	        Question: {question}
235	        Guidance: {guidance}
236	
237	        Requirements:
238	        - Anchor your reasoning to the original issue text and the full diff above, not to any approved plan.
239	        - Investigate only this check.
240	        - Populate the existing `checks[0].findings` array with concrete findings. Each finding should include:
241	          - `detail`: a full sentence describing what you checked and what you found
242	          - `flagged`: `true` when the finding represents a risk, mismatch, or unresolved question
243	          - `status`: use `blocking`, `significant`, `minor`, or `n/a`
244	          - `evidence_file` when a file path makes the finding easier to act on
245	        - If a concern overlaps with a settled gate decision, do NOT raise it as `blocking`. Mark it `significant` and explain that the severity was downgraded because the gate already settled that concern.
246	        - Use `blocking` only for issue-anchored gaps that should force another revise/execute pass.
247	        - Use `significant` for meaningful but non-blocking concerns, including settled-decision downgrades.
248	        - Use `minor` for informational quality notes that do not justify rework.
249	        - Use `flagged: false` with `status: "n/a"` only when the finding is purely informational and poses no downside.
250	        - Leave `flags` empty unless you discover an additional concern that does not fit the focused check.
251	        - Keep `verified_flag_ids` and `disputed_flag_ids` empty unless you are explicitly confirming or disputing an existing REVIEW-* flag from a prior iteration.
252	        - Preserve the `pre_check_flags` list verbatim in the output file.{iteration_context}
253	        """
254	    ).strip()
255	
256	
257	def parallel_criteria_review_prompt(
258	    state: PlanState,
259	    plan_dir: Path,
260	    root: Path | None,
261	    output_path: Path,
262	) -> str:
263	    """Build the parallel-mode criteria review prompt.
264	
265	    This intentionally does not wrap `_review_prompt()`. The brief literally
266	    asked to keep `_review_prompt()` as the parallel criteria check, but that would
267	    leak plan/gate/execution context that conflicts with the stronger
268	    issue-anchored review contract. This divergence is deliberate.
269	    """
270	    del root
271	    context = _parallel_review_context(state, plan_dir)
272	    return textwrap.dedent(
273	        f"""
274	        Review the execution against the original issue text and the finalized execution criteria.
275	
276	        Project directory:
277	        {context["project_dir"]}
278	
279	        {context["intent_block"]}
280	
281	        Full git diff:
282	        {context["git_diff"]}
283	
284	        Execution tracking state (`finalize.json`):
285	        {json_dump(context["finalize_data"]).strip()}
286	
287	        {_settled_decisions_review_block(context["settled_decisions"])}
288	
289	        Your output template is at: {output_path}
290	        Read the file first and write your final answer into that JSON structure.
291	
292	        Requirements:
293	        - Use only the issue text, full git diff, `finalize.json`, and the settled decisions shown above.
294	        - Do not rely on any approved plan, plan metadata, gate summary, execution summary, or execution audit that are not present here.
295	        - Judge against the success criteria from `finalize.json`, but stay anchored to the original issue text when deciding whether the work actually solved the problem.
296	        - Each criterion has a `priority` (`must`, `should`, or `info`). Apply these rules:
297	          - `must` criteria are hard gates. A `must` criterion that fails means `needs_rework`.
298	          - `should` criteria are quality targets. If the spirit is met but the letter is not, mark `pass` with evidence explaining the gap. Only mark `fail` if the intent was clearly missed. A `should` failure alone does NOT require `needs_rework`.
299	          - `info` criteria are for human reference. Mark them `waived` with a note — do not evaluate them.
300	          - If a criterion cannot be verified in this context, mark it `waived` with an explanation.
301	        - Set `review_verdict` to `needs_rework` only when at least one `must` criterion fails or actual implementation work is incomplete. Use `approved` when all `must` criteria pass, even if some `should` criteria are flagged.
302	        - The settled decisions above are already approved. Verify implementation against them, but do not re-litigate them.
303	        - baseline_test_failures in finalize.json lists tests that were already failing before execution. Do not flag these as rework items unless the executor introduced new failures in those same tests.
304	        - `rework_items` must be structured and directly actionable. Populate `issues` as one-line summaries derived from `rework_items`.
305	        - When approved, keep both `issues` and `rework_items` empty arrays.
306	        """
307	    ).strip()
308	
309	
310	def _settled_decisions_block(gate: dict[str, object]) -> str:
311	    settled_decisions = gate.get("settled_decisions", [])
312	    if not isinstance(settled_decisions, list) or not settled_decisions:
313	        return ""
314	    lines = ["Settled decisions (verify the executor implemented these correctly):"]
315	    for item in settled_decisions:
316	        if not isinstance(item, dict):
317	            continue
318	        decision_id = item.get("id", "DECISION")
319	        decision = item.get("decision", "")
320	        rationale = item.get("rationale", "")
321	        line = f"- {decision_id}: {decision}"
322	        if rationale:
323	            line += f" ({rationale})"
324	        lines.append(line)
325	    lines.append("")
326	    return "\n".join(lines)
327	
328	
329	def _settled_decisions_instruction(gate: dict[str, object]) -> str:
330	    settled_decisions = gate.get("settled_decisions", [])
331	    if not isinstance(settled_decisions, list) or not settled_decisions:
332	        return ""
333	    return "- The decisions listed above were settled at the gate stage. Verify that the executor implemented each settled decision correctly. Flag deviations from these decisions, but do not question the decisions themselves."
334	
335	
336	def _write_review_template(plan_dir: Path, state: PlanState) -> Path:
337	    """Write a pre-populated review output template and return its path.
338	
339	    Pre-fills ``task_verdicts`` and ``sense_check_verdicts`` with the actual
340	    task IDs and sense-check IDs from ``finalize.json`` so the model only has
341	    to fill in verdict text instead of inventing IDs from scratch.  This is
342	    the same pattern used for critique templates and fixes MiniMax-M2.7's
343	    tendency to return empty verdict arrays.
344	    """
345	    finalize_data = read_json(plan_dir / "finalize.json")
346	
347	    task_verdicts = []
348	    for task in finalize_data.get("tasks", []):
349	        task_id = task.get("id", "")
350	        if task_id:
351	            task_verdicts.append({
352	                "task_id": task_id,
353	                "reviewer_verdict": "",
354	                "evidence_files": [],
355	            })
356	
357	    sense_check_verdicts = []
358	    for sc in finalize_data.get("sense_checks", []):
359	        sc_id = sc.get("id", "")
360	        if sc_id:
361	            sense_check_verdicts.append({
362	                "sense_check_id": sc_id,
363	                "verdict": "",
364	            })
365	
366	    # Pre-populate criteria from finalize success_criteria if available
367	    criteria = []
368	    for crit in finalize_data.get("success_criteria", []):
369	        if isinstance(crit, dict) and crit.get("name"):
370	            criteria.append({
371	                "name": crit["name"],
372	                "priority": crit.get("priority", "must"),
373	                "pass": "",
374	                "evidence": "",
375	            })
376	
377	    template = {
378	        "review_verdict": "",
379	        "criteria": criteria,
380	        "issues": [],
381	        "rework_items": [],
382	        "summary": "",
383	        "task_verdicts": task_verdicts,
384	        "sense_check_verdicts": sense_check_verdicts,
385	    }
386	
387	    output_path = plan_dir / "review_output.json"
388	    output_path.write_text(json.dumps(template, indent=2), encoding="utf-8")
389	    return output_path
390	
391	
392	def _review_prompt(
393	    state: PlanState,
394	    plan_dir: Path,
395	    *,
396	    review_intro: str,
397	    criteria_guidance: str,
398	    task_guidance: str,
399	    sense_check_guidance: str,
400	    pre_check_flags: list[dict[str, Any]] | None = None,
401	) -> str:
402	    project_dir = Path(state["config"]["project_dir"])
403	    latest_plan = latest_plan_path(plan_dir, state).read_text(encoding="utf-8")
404	    latest_meta = read_json(latest_plan_meta_path(plan_dir, state))
405	    execution = read_json(plan_dir / "execution.json")
406	    gate = read_json(plan_dir / "gate.json")
407	    finalize_data = read_json(plan_dir / "finalize.json")
408	    settled_decisions_block = _settled_decisions_block(gate)
409	    settled_decisions_instruction = _settled_decisions_instruction(gate)
410	    diff_summary = collect_git_diff_summary(project_dir)
411	    audit_path = plan_dir / "execution_audit.json"
412	    if audit_path.exists():
413	        audit_block = textwrap.dedent(
414	            f"""
415	            Execution audit (`execution_audit.json`):
416	            {json_dump(read_json(audit_path)).strip()}
417	            """
418	        ).strip()
419	    else:
420	        audit_block = "Execution audit (`execution_audit.json`): not present. Skip that artifact gracefully and rely on `finalize.json`, `execution.json`, and the git diff."
421	    flag_reverify_items: list[dict[str, str]] = []
422	    for flag in load_flag_registry(plan_dir).get("flags", []):
423	        if not isinstance(flag, dict):
424	            continue
425	        status = str(flag.get("status", "open"))
426	        if status not in {"open", "addressed", "verified", "disputed"}:
427	            continue
428	        flag_reverify_items.append(
429	            {
430	                "id": str(flag.get("id", "")),
431	                "concern": str(flag.get("concern", "")),
432	                "severity": str(flag.get("severity") or flag.get("severity_hint") or "uncertain"),
433	                "status": status,
434	            }
435	        )
436	    flag_reverify_block = ""
437	    if flag_reverify_items:
438	        flag_reverify_block = textwrap.dedent(
439	            f"""
440	            Critique flags to re-verify against the final diff:
441	            {json_dump(flag_reverify_items).strip()}
442	
443	            For each flag above that was raised during critique, verify whether the final diff actually addresses the concern.
444	            A flag is resolved only if the final diff contains code that directly addresses the concern.
445	            Do not trust pre-execute promises or plan claims; check the diff itself.
446	            Add resolved flag IDs to `verified_flag_ids`.
447	            For any unresolved flag, add a `rework_items` entry with `task_id: "REVIEW"`, `issue`, `expected`, `actual`, `evidence_file`, `flag_id`, and `source: "review_flag_reverify"`.
448	            """
449	        ).strip()
450	    pre_check_block = ""
451	    if pre_check_flags:
452	        pre_check_block = textwrap.dedent(
453	            f"""
454	            Advisory mechanical pre-check flags:
455	            {json_dump(pre_check_flags).strip()}
456	
457	            Copy this list verbatim into the output `pre_check_flags` field.
458	            """
459	        ).strip()
460	    extra_sections = ""
461	    if flag_reverify_block:
462	        extra_sections += f"\n\n{flag_reverify_block}"
463	    if pre_check_block:
464	        extra_sections += f"\n\n{pre_check_block}"
465	    return textwrap.dedent(
466	        f"""
467	        {review_intro}
468	
469	        Project directory:
470	        {project_dir}
471	
472	        {intent_and_notes_block(state)}
473	
474	        Approved plan:
475	        {latest_plan}
476	
477	        Execution tracking state (`finalize.json`):
478	        {json_dump(finalize_data).strip()}
479	
480	        Plan metadata:
481	        {json_dump(latest_meta).strip()}
482	
483	        Gate summary:
484	        {json_dump(gate).strip()}
485	
486	        {settled_decisions_block}{extra_sections}
487	
488	        Execution summary:
489	        {json_dump(execution).strip()}
490	
491	        {audit_block}
492	
493	        Git diff summary:
494	        {diff_summary}
495	
496	        Requirements:
497	        - {criteria_guidance}
498	        - Trust executor evidence by default. Dig deeper only where the git diff, `execution_audit.json`, or vague notes make the claim ambiguous.
499	        - Each criterion has a `priority` (`must`, `should`, or `info`). Apply these rules:
500	          - `must` criteria are hard gates. A `must` criterion that fails means `needs_rework`.
501	          - `should` criteria are quality targets. If the spirit is met but the letter is not, mark `pass` with evidence explaining the gap. Only mark `fail` if the intent was clearly missed. A `should` failure alone does NOT require `needs_rework`.
502	          - `info` criteria are for human reference. Mark them `waived` with a note — do not evaluate them.
503	          - If a criterion (any priority) cannot be verified in this context (e.g., requires manual testing or runtime observation), mark it `waived` with an explanation.
504	        - Set `review_verdict` to `needs_rework` only when at least one `must` criterion fails or actual implementation work is incomplete. Use `approved` when all `must` criteria pass, even if some `should` criteria are flagged.
505	        {settled_decisions_instruction}
506	        - baseline_test_failures in finalize.json lists tests that were already failing before execution. Do not flag these as rework items unless the executor introduced new failures in those same tests.
507	        - {task_guidance}
508	        - {sense_check_guidance}
509	        - Follow this JSON shape exactly:
510	        ```json
511	        {{
512	          "review_verdict": "approved",
513	          "criteria": [
514	            {{
515	              "name": "All existing tests pass",
516	              "priority": "must",
517	              "pass": "pass",
518	              "evidence": "Test suite ran green — 42 passed, 0 failed."
519	            }},
520	            {{
521	              "name": "File under ~300 lines",
522	              "priority": "should",
523	              "pass": "pass",
524	              "evidence": "File is 375 lines — above the target but reasonable given the component's responsibilities. Spirit met."
525	            }},
526	            {{
527	              "name": "Manual smoke tests pass",
528	              "priority": "info",
529	              "pass": "waived",
530	              "evidence": "Cannot be verified in automated review. Noted for manual QA."
531	            }}
532	          ],
533	          "issues": [],
534	          "rework_items": [],
535	          "summary": "Approved. All must criteria pass. The should criterion on line count is close enough given the component scope.",
536	          "task_verdicts": [
537	            {{
538	              "task_id": "T6",
539	              "reviewer_verdict": "Pass. Claimed handler changes and command evidence match the repo state.",
540	              "evidence_files": ["megaplan/handlers.py", "megaplan/evaluation.py"]
541	            }}
542	          ],
543	          "sense_check_verdicts": [
544	            {{
545	              "sense_check_id": "SC6",
546	              "verdict": "Confirmed. The execute blocker only fires when both evidence arrays are empty."
547	            }}
548	          ]
549	        }}
550	        ```
551	        - `rework_items` must be an array of structured rework directives. When `review_verdict` is `needs_rework`, populate one entry per issue with:
552	          - `task_id`: which finalize task this issue relates to
553	          - `issue`: what is wrong
554	          - `expected`: what correct behavior looks like
555	          - `actual`: what was observed
556	          - `evidence_file` (optional): file path supporting the finding
557	          - `flag_id`: critique/review flag ID when applicable, otherwise `null`
558	          - `source`: short machine-readable source tag when applicable, otherwise `null`
559	        - `issues` must still be populated as a flat one-line-per-item summary derived from `rework_items` (for backward compatibility). When approved, both `issues` and `rework_items` should be empty arrays.
560	        - When the work needs another execute pass, keep the same shape and change only `review_verdict` to `needs_rework`; make `issues`, `rework_items`, `summary`, and task verdicts specific enough for the executor to act on directly.
561	        """
562	    ).strip()
563
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
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/finalize.py"
}
```

> TOOL

tool_result Read
```
1	"""Finalize-phase prompt builders."""
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
13	    load_flag_registry,
14	    read_json,
15	)
16	from megaplan.types import PlanState
17	
18	from ._shared import _finalize_debt_block, _render_prep_block
19	from .gate import _collect_critique_summaries, _flag_summary
20	
21	
22	def _finalize_prompt(state: PlanState, plan_dir: Path, root: Path | None = None) -> str:
23	    project_dir = Path(state["config"]["project_dir"])
24	    prep_block, prep_instruction = _render_prep_block(plan_dir)
25	    latest_plan = latest_plan_path(plan_dir, state).read_text(encoding="utf-8")
26	    latest_meta = read_json(latest_plan_meta_path(plan_dir, state))
27	    gate = read_json(plan_dir / "gate.json")
28	    flag_registry = load_flag_registry(plan_dir)
29	    critique_history = _collect_critique_summaries(plan_dir, state["iteration"])
30	    debt_block = _finalize_debt_block(plan_dir, root)
31	    return textwrap.dedent(
32	        f"""
33	        You are preparing an execution-ready briefing document from the approved plan.
34	
35	        Project directory:
36	        {project_dir}
37	
38	        {prep_block}
39	
40	        {prep_instruction}
41	
42	        {intent_and_notes_block(state)}
43	
44	        Approved plan:
45	        {latest_plan}
46	
47	        Plan metadata:
48	        {json_dump(latest_meta).strip()}
49	
50	        Gate summary:
51	        {json_dump(gate).strip()}
52	
53	        Flag registry:
54	        {json_dump(_flag_summary(flag_registry)).strip()}
55	
56	        Critique history:
57	        {json_dump(critique_history).strip()}
58	
59	        {debt_block}
60	
61	        Requirements:
62	        - Produce structured JSON only.
63	        - `tasks` must be an ordered array of task objects. Every task object must include:
64	          - `id`: short stable task ID like `T1`
65	          - `description`: concrete work item
66	          - `depends_on`: array of earlier task IDs or `[]`
67	          - `status`: always `"pending"` at finalize time
68	          - `executor_notes`: always `""` at finalize time
69	          - `reviewer_verdict`: always `""` at finalize time
70	        - `watch_items` must be an array of strings covering runtime risks, critique concerns, and assumptions to keep visible during execution.
71	        - `sense_checks` must be an array with one verification question per task. Every sense-check object must include:
72	          - `id`: short stable ID like `SC1`
73	          - `task_id`: the related task ID
74	          - `question`: reviewer verification question
75	          - `verdict`: always `""` at finalize time
76	        - `meta_commentary` must be a single string with execution guidance, gotchas, or judgment calls that help the executor succeed.
77	        - `validation` must be an object that self-checks plan coverage:
78	          - `plan_steps_covered`: enumerate EVERY step from the approved plan. For each step, provide a short `plan_step_summary` (the step's intent in one phrase) and `finalize_task_ids` (array of task IDs that implement it — a single plan step may map to multiple tasks).
79	          - `orphan_tasks`: task IDs that do not correspond to any plan step. Normally empty. If non-empty, explain in `completeness_notes`.
80	          - `completeness_notes`: free-text explanation of any gaps, deviations, or deliberate omissions.
81	          - `coverage_complete`: set to `true` only if every plan step has at least one finalize task AND you have verified the mapping by reviewing each entry. Set to `false` if any plan step is missing coverage.
82	          - Example:
83	          ```json
84	          "validation": {{
85	            "plan_steps_covered": [
86	              {{"plan_step_summary": "Add retry logic to API client", "finalize_task_ids": ["T1", "T2"]}},
87	              {{"plan_step_summary": "Update configuration schema", "finalize_task_ids": ["T3"]}}
88	            ],
89	            "orphan_tasks": [],
90	            "completeness_notes": "All plan steps mapped to tasks.",
91	            "coverage_complete": true
92	          }}
93	          ```
94	        - Preserve information that strong existing artifacts already capture well: execution ordering, watch-outs, reviewer checkpoints, and practical context.
95	        - The structured output should be self-contained: an executor reading only `finalize.json` should have everything needed to work.
96	        - Keep the task count proportional to the work. A simple 1-2 file fix should be 2 tasks: (1) apply the fix, (2) run tests. Do NOT create separate "inspect" or "read" tasks for simple changes — the executor can read and fix in one step. Only create more tasks when the work has genuinely independent stages.
97	        - The FINAL task MUST always be to run tests and verify the changes work. If specific test IDs or commands are mentioned in the original task, include them. Otherwise, the executor should find and run the tests most relevant to the files changed. If any test fails, read the error, fix the code, and re-run until they pass. Do NOT create new test files — run the project's existing test suite. Additionally, the executor should write a short throwaway script that reproduces the specific bug described in the task, run it to confirm the fix works, then delete the script.
98	        """
99	    ).strip()
100
```

> TOOL

tool_use Glob
```json
{
  "pattern": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/*shared*"
}
```

> TOOL

tool_result Glob
```
megaplan/prompts/_shared.py
megaplan/prompts/__pycache__/_shared.cpython-311.pyc
megaplan/prompts/__pycache__/_shared.cpython-312.pyc
megaplan/prompts/__pycache__/_shared.cpython-314.pyc
```

> AGENT

Now let me read the shared helpers file and also check if prep.py exists:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/_shared.py"
}
```

> TOOL

tool_result Read
```
1	"""Shared prompt helpers used across megaplan phases."""
2	
3	from __future__ import annotations
4	
5	import textwrap
6	from pathlib import Path
7	
8	from megaplan._core import (
9	    debt_by_subsystem,
10	    escalated_subsystems,
11	    json_dump,
12	    load_debt_registry,
13	    read_json,
14	)
15	
16	
17	def _resolve_prompt_root(plan_dir: Path, root: Path | None) -> Path:
18	    if root is not None:
19	        return root
20	    if len(plan_dir.parents) >= 3:
21	        return plan_dir.parents[2]
22	    return plan_dir
23	
24	
25	def _grouped_debt_for_prompt(
26	    plan_dir: Path, root: Path | None
27	) -> dict[str, list[dict[str, object]]]:
28	    registry = load_debt_registry(_resolve_prompt_root(plan_dir, root))
29	    grouped_entries = debt_by_subsystem(registry)
30	    return {
31	        subsystem: [
32	            {
33	                "id": entry["id"],
34	                "concern": entry["concern"],
35	                "occurrence_count": entry["occurrence_count"],
36	                "plan_ids": entry["plan_ids"],
37	            }
38	            for entry in entries
39	        ]
40	        for subsystem, entries in sorted(grouped_entries.items())
41	    }
42	
43	
44	def _escalated_debt_for_prompt(
45	    plan_dir: Path, root: Path | None
46	) -> list[dict[str, object]]:
47	    registry = load_debt_registry(_resolve_prompt_root(plan_dir, root))
48	    return [
49	        {
50	            "subsystem": subsystem,
51	            "total_occurrences": total,
52	            "plan_count": len(
53	                {plan_id for entry in entries for plan_id in entry["plan_ids"]}
54	            ),
55	            "entries": [
56	                {
57	                    "id": entry["id"],
58	                    "concern": entry["concern"],
59	                    "occurrence_count": entry["occurrence_count"],
60	                    "plan_ids": entry["plan_ids"],
61	                }
62	                for entry in entries
63	            ],
64	        }
65	        for subsystem, total, entries in escalated_subsystems(registry)
66	    ]
67	
68	
69	def _debt_watch_lines(plan_dir: Path, root: Path | None) -> list[str]:
70	    lines: list[str] = []
71	    for subsystem, entries in sorted(_grouped_debt_for_prompt(plan_dir, root).items()):
72	        for entry in entries:
73	            lines.append(
74	                f"[DEBT] {subsystem}: {entry['concern']} "
75	                f"(flagged {entry['occurrence_count']} times across {len(entry['plan_ids'])} plans)"
76	            )
77	    return lines
78	
79	
80	def _planning_debt_block(plan_dir: Path, root: Path | None) -> str:
81	    return textwrap.dedent(
82	        f"""
83	        Known accepted debt grouped by subsystem:
84	        {json_dump(_grouped_debt_for_prompt(plan_dir, root)).strip()}
85	
86	        Escalated debt subsystems:
87	        {json_dump(_escalated_debt_for_prompt(plan_dir, root)).strip()}
88	
89	        Debt guidance:
90	        - These are known accepted limitations. Do not re-flag them unless the current plan makes them worse, broadens them, or fails to contain them.
91	        - Prefix every new concern with a subsystem tag followed by a colon, for example `Timeout recovery: retry backoff remains brittle`.
92	        - When a concern is recurring debt that still needs to be flagged, prefix it with `Recurring debt:` after the subsystem tag, for example `Timeout recovery: Recurring debt: retry backoff remains brittle`.
93	        """
94	    ).strip()
95	
96	
97	def _gate_debt_block(plan_dir: Path, root: Path | None) -> str:
98	    return textwrap.dedent(
99	        f"""
100	        Known accepted debt grouped by subsystem:
101	        {json_dump(_grouped_debt_for_prompt(plan_dir, root)).strip()}
102	
103	        Escalated debt subsystems:
104	        {json_dump(_escalated_debt_for_prompt(plan_dir, root)).strip()}
105	
106	        Debt guidance:
107	        - Treat recurring debt as decision context, not background noise.
108	        - If the current unresolved flags overlap an escalated subsystem, prefer recommending holistic redesign over another point fix.
109	        """
110	    ).strip()
111	
112	
113	def _finalize_debt_block(plan_dir: Path, root: Path | None) -> str:
114	    watch_lines = _debt_watch_lines(plan_dir, root)
115	    return textwrap.dedent(
116	        f"""
117	        Debt watch items (do not make these worse):
118	        {json_dump(watch_lines).strip()}
119	        """
120	    ).strip()
121	
122	
123	
124	def _render_prep_block(plan_dir: Path) -> tuple[str, str]:
125	    prep_path = plan_dir / "prep.json"
126	    if not prep_path.exists():
127	        return "", ""
128	    prep = read_json(prep_path)
129	    # If prep decided to skip (task was simple enough), return empty —
130	    # downstream phases will use the original task description as-is
131	    if prep.get("skip", False):
132	        return "", ""
133	    prep = read_json(prep_path)
134	
135	    def _cell(value: object) -> str:
136	        if isinstance(value, list):
137	            value = ", ".join(str(item).strip() for item in value if str(item).strip())
138	        text = str(value).strip()
139	        if not text:
140	            return "-"
141	        return text.replace("|", "\\|").replace("\n", " ")
142	
143	    task_summary = (
144	        str(prep.get("task_summary", "")).strip() or "No task summary provided."
145	    )
146	
147	    evidence_items = prep.get("key_evidence", [])
148	    if isinstance(evidence_items, list) and evidence_items:
149	        evidence_lines = []
150	        for item in evidence_items:
151	            if not isinstance(item, dict):
152	                continue
153	            point = str(item.get("point", "")).strip() or "Unspecified evidence"
154	            source = str(item.get("source", "")).strip() or "unspecified source"
155	            relevance = (
156	                str(item.get("relevance", "")).strip() or "unspecified relevance"
157	            )
158	            evidence_lines.append(
159	                f"- {point} (source: {source}; relevance: {relevance})"
160	            )
161	        evidence_block = (
162	            "\n".join(evidence_lines)
163	            if evidence_lines
164	            else "- No key evidence captured."
165	        )
166	    else:
167	        evidence_block = "- No key evidence captured."
168	
169	    relevant_code_items = prep.get("relevant_code", [])
170	    if isinstance(relevant_code_items, list) and relevant_code_items:
171	        code_lines = [
172	            "| File | Functions | Why |",
173	            "| --- | --- | --- |",
174	        ]
175	        for item in relevant_code_items:
176	            if not isinstance(item, dict):
177	                continue
178	            code_lines.append(
179	                f"| {_cell(item.get('file_path', ''))} | {_cell(item.get('functions', []))} | {_cell(item.get('why', ''))} |"
180	            )
181	        relevant_code_block = (
182	            "\n".join(code_lines)
183	            if len(code_lines) > 2
184	            else "- No directly relevant code captured."
185	        )
186	    else:
187	        relevant_code_block = "- No directly relevant code captured."
188	
189	    test_expectation_items = prep.get("test_expectations", [])
190	    if isinstance(test_expectation_items, list) and test_expectation_items:
191	        test_lines = []
192	        for item in test_expectation_items:
193	            if not isinstance(item, dict):
194	                continue
195	            test_id = str(item.get("test_id", "")).strip() or "unnamed test"
196	            status = str(item.get("status", "")).strip() or "unknown"
197	            what_it_checks = (
198	                str(item.get("what_it_checks", "")).strip()
199	                or "No description provided."
200	            )
201	            test_lines.append(f"- [{status}] {test_id}: {what_it_checks}")
202	        test_expectations_block = (
203	            "\n".join(test_lines)
204	            if test_lines
205	            else "- No explicit test expectations captured."
206	        )
207	    else:
208	        test_expectations_block = "- No explicit test expectations captured."
209	
210	    constraints = prep.get("constraints", [])
211	    if isinstance(constraints, list) and constraints:
212	        constraint_lines = [
213	            f"- {str(item).strip()}" for item in constraints if str(item).strip()
214	        ]
215	        constraints_block = (
216	            "\n".join(constraint_lines)
217	            if constraint_lines
218	            else "- No explicit constraints captured."
219	        )
220	    else:
221	        constraints_block = "- No explicit constraints captured."
222	
223	    suggested_approach = (
224	        str(prep.get("suggested_approach", "")).strip()
225	        or "No suggested approach provided."
226	    )
227	
228	    prep_block = textwrap.dedent(
229	        f"""
230	        Engineering brief produced from the codebase and task details:
231	
232	        ### Task Summary
233	        {task_summary}
234	
235	        ### Key Evidence
236	        {evidence_block}
237	
238	        ### Relevant Code
239	        {relevant_code_block}
240	
241	        ### Test Expectations
242	        {test_expectations_block}
243	
244	        ### Constraints
245	        {constraints_block}
246	
247	        ### Suggested Approach
248	        {suggested_approach}
249	        """
250	    ).strip()
251	    prep_instruction = "The engineering brief above was produced by analyzing the codebase. Use it as a strong starting point, but the suggested approach is a hypothesis — verify it's the best fix, not just a valid one."
252	    return prep_block, prep_instruction
253
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
total 240
drwxr-xr-x@ 12 user_c042661f  staff    384 Apr 15 06:08 .
drwxr-xr-x  31 user_c042661f  staff    992 Apr 15 07:10 ..
-rw-r--r--@  1 user_c042661f  staff   6148 Apr 15 05:43 .DS_Store
-rw-r--r--@  1 user_c042661f  staff   6885 Apr  9 18:57 __init__.py
drwxr-xr-x@ 26 user_c042661f  staff    832 Apr 15 06:09 __pycache__
-rw-r--r--   1 user_c042661f  staff   8785 Apr  6 07:11 _shared.py
-rw-r--r--   1 user_c042661f  staff  16501 Apr 10 22:53 critique.py
-rw-r--r--@  1 user_c042661f  staff  18972 Apr 10 23:09 execute.py
-rw-r--r--   1 user_c042661f  staff   5249 Apr  2 19:38 finalize.py
-rw-r--r--   1 user_c042661f  staff   7482 Apr 15 06:08 gate.py
-rw-r--r--   1 user_c042661f  staff  10773 Apr  9 19:12 planning.py
-rw-r--r--   1 user_c042661f  staff  23152 Apr 11 04:24 review.py
[rerun: b1]
```

> AGENT

I notice that `prep.py` does not exist as a standalone file. Let me check the planning.py file to see if it contains prep-related functions:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/prompts/planning.py"
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
81	    """
82	).strip()
83	
84	
85	def _plan_prompt(state: PlanState, plan_dir: Path) -> str:
86	    project_dir = Path(state["config"]["project_dir"])
87	    prep_block, prep_instruction = _render_prep_block(plan_dir)
88	    clarification = state.get("clarification", {})
89	    if clarification:
90	        clarification_block = textwrap.dedent(
91	            f"""
92	            Existing clarification context:
93	            {json_dump(clarification).strip()}
94	            """
95	        ).strip()
96	    else:
97	        clarification_block = "No prior clarification artifact exists. Identify ambiguities, ask clarifying questions, and state your assumptions inside the plan output."
98	    return textwrap.dedent(
99	        f"""
100	        You are creating an implementation plan for the following idea.
101	
102	        {prep_block}
103	
104	        {prep_instruction}
105	
106	        {intent_and_notes_block(state)}
107	
108	        Project directory:
109	        {project_dir}
110	
111	        {clarification_block}
112	
113	        Requirements:
114	        - If the engineering brief suggests an approach, use it as your starting hypothesis — but before committing, consider if there's a simpler or more fundamental fix. The brief is well-researched input, not a final answer.
115	        - If the brief is absent, incomplete, or says "skip", inspect the repository yourself before planning.
116	        - Stay focused on the requested idea. If repo exploration surfaces unrelated issues or docs, ignore them and return to the task.
117	        - Prefer source code, tests, and directly relevant config files. Avoid `.megaplan/`, prior plan artifacts, and unrelated `docs/` or ops/deployment material unless the task explicitly depends on them.
118	        - Stop exploring once you have enough evidence to name the concrete touch points and validation path. Do not keep browsing after you can write the plan.
119	        - Produce a concrete implementation plan in markdown.
120	        - Define observable success criteria as objects with `criterion` (string) and `priority` (`must`, `should`, or `info`):
121	          - `must` — hard gate. The reviewer will block on failure. Use for correctness, functional requirements, and verifiable outcomes (e.g., "all existing tests pass", "API returns 200 for valid input"). Every `must` criterion must have a clear yes/no answer.
122	          - `should` — quality target. The reviewer flags but does not block. Use for subjective goals, numeric guidelines, and best-effort improvements (e.g., "file under ~300 lines", "no deeply nested conditionals", "each function has a single responsibility").
123	          - `info` — documented for humans, reviewer skips. Use for criteria that cannot be verified in this pipeline (e.g., "13 manual smoke tests pass", "stakeholder sign-off obtained").
124	        - Use the `questions` field for ambiguities that would materially change implementation.
125	        - Use the `assumptions` field for defaults you are making so planning can proceed now.
126	        - Prefer cheap validation steps early.
127	        - Keep the plan proportional to the task. A 1-line fix needs a 2-step plan (apply fix + run tests), not a 5-step investigation.
128	        - If user notes answer earlier questions, incorporate them into the draft plan instead of re-asking them.
129	        - Fix the problem fully. Do not limit scope just to avoid breaking existing tests — update the tests too if needed.
130	        - Prefer the simplest, most direct fix. No fallbacks, type conversions, or defensive wrappers without concrete evidence they are needed.
131	        - If the task or issue hints suggest a specific approach, follow it. Only deviate with concrete counter-evidence.
132	
133	        {PLAN_TEMPLATE}
134	        """
135	    ).strip()
136	
137	
138	def _prep_prompt(state: PlanState, plan_dir: Path, root: Path | None = None) -> str:
139	    del root
140	    project_dir = Path(state["config"]["project_dir"])
141	    output_path = plan_dir / "prep.json"
142	    return textwrap.dedent(
143	        f"""
144	        Prepare a concise engineering brief for the task below. This brief will be the primary context for all subsequent planning and execution.
145	
146	        Task:
147	        {state["idea"]}
148	
149	        Project: {project_dir}
150	        Output file: {output_path}
151	
152	        First, assess: does this task need codebase investigation?
153	
154	        Set "skip": true if ALL of these are true:
155	        - The task names the exact file(s) to change
156	        - The required change is clearly described
157	        - No ambiguity about the approach
158	
159	        Set "skip": false if ANY of these are true:
160	        - The task doesn't say which files to change
161	        - Multiple approaches seem possible
162	        - The task references concepts, APIs, or patterns you'd need to look up in the codebase
163	        - The task involves more than 2-3 files
164	        - There are hints or references that need investigation
165	
166	        If skipping, leave everything else empty. The original task description will be used directly.
167	        If not skipping, fill in the brief:
168	        1. Search the codebase (Glob, Grep, Read) for relevant files and functions.
169	        2. If tests exist for the affected code, read them — they reveal what the fix must actually do, which may differ from what the task description suggests.
170	        3. Extract evidence from the task description — hints, references, error messages.
171	        4. Challenge the obvious path: if the task or hints point to a specific location, verify it's actually the right place. Trace the call chain — where does data flow? Where does it go wrong? The obvious file may be a symptom, not the root cause.
172	        5. If the task describes a bug or incorrect behavior, seriously consider whether it is a symptom of a larger issue. Before proposing a fix, trace the root cause. Ask: why does this happen? Could the same root cause produce other failures? Is the fix a patch on one case, or does it need to address an underlying gap? If the codebase has related functionality that is also incomplete or broken, note it — a narrow fix may not be enough.
173	        6. If you find that a suggested fix already exists in the code, say so explicitly — this means the root cause is elsewhere.
174	        7. Once you identify the function, parameter, or pattern that needs fixing, grep for ALL other usages of it in the codebase. If the same parameter is passed in 3 places, all 3 may need the fix. List every call site in relevant_code — do not stop at the first one.
175	        8. If the code has a `NotImplementedError`, `raise`, `TODO`, or explicit skip for certain inputs, and the bug involves those inputs, the fix likely needs to implement the missing functionality — not just patch around it. Flag this in the brief so the plan knows a larger change is needed.
176	        9. Look for existing helper functions, utilities, or patterns in the codebase that handle similar cases. If there is existing machinery (e.g., a merge function, a validation helper, a base class method), the fix should use it rather than reinventing.
177	        10. Before finalizing, ask: if I change this function, are there other callers that rely on its current behavior? A function called from multiple code paths may need different fixes for different callers — or a new method instead of modifying the existing one.
178	        11. List all usages as a numbered list (1. file:line — description, 2. file:line — description, etc.) so none are missed.
179	        12. Distill into a brief that adds value beyond the raw task description.
180	
181	        Brief fields:
182	        - skip: true if no investigation needed, false if brief has useful content.
183	        - task_summary: What needs to be done, in 2-3 sentences.
184	        - key_evidence: Facts from the task and codebase not obvious from reading the task alone.
185	        - relevant_code: File paths and key functions found by searching.
186	        - test_expectations: Tests that verify the affected behavior.
187	        - constraints: What must not break.
188	        - suggested_approach: A concrete approach grounded in what you found.
189	
190	        """
191	    ).strip()
192	
193
```

> AGENT

Now let me also check if there are additional prompt-related files like critique.py and gate.py:

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
75	        - Verify that the plan remains aligned with the user's original intent, not just internal plan quality.
76	        - Remove unjustified scope growth. If critique raised scope creep, narrow the plan back to the original idea unless the broader work is strictly required.
77	        - Maintain the structural template: H1 title, ## Overview, phase sections with numbered step sections, ## Execution Order or ## Validation Order.
78	        - CRITICAL: Your entire revised plan markdown (all sections) must be output as the `plan` field in the structured output. The prose response must not contain the plan text.
79	        - CRITICAL: Return only the structured JSON object for the schema fields `plan`, `changes_summary`, `flags_addressed`, `assumptions`, `success_criteria`, and `questions`. Do not add commentary before or after the JSON object.
80	
81	        {PLAN_TEMPLATE}
82	        """
83	    ).strip()
84	
85	
86	def _critique_context(state: PlanState, plan_dir: Path, root: Path | None = None) -> dict[str, Any]:
87	    project_dir = Path(state["config"]["project_dir"])
88	    prep_block, prep_instruction = _render_prep_block(plan_dir)
89	    latest_plan = latest_plan_path(plan_dir, state).read_text(encoding="utf-8")
90	    latest_meta = read_json(latest_plan_meta_path(plan_dir, state))
91	    structure_warnings = latest_meta.get("structure_warnings", [])
92	    flag_registry = load_flag_registry(plan_dir)
93	    unresolved = [
94	        {
95	            "id": flag["id"],
96	            "concern": flag["concern"],
97	            "status": flag["status"],
98	            "severity": flag.get("severity"),
99	        }
100	        for flag in flag_registry["flags"]
101	        if flag["status"] in {"addressed", "open", "disputed"}
102	    ]
103	    return {
104	        "project_dir": project_dir,
105	        "prep_block": prep_block,
106	        "prep_instruction": prep_instruction,
107	        "latest_plan": latest_plan,
108	        "latest_meta": latest_meta,
109	        "structure_warnings": structure_warnings,
110	        "unresolved": unresolved,
111	        "debt_block": _planning_debt_block(plan_dir, root),
112	        "robustness": configured_robustness(state),
113	    }
114	
115	
116	def _build_checks_template(
117	    plan_dir: Path,
118	    state: PlanState,
119	    checks: tuple[dict[str, Any], ...],
120	) -> list[dict[str, object]]:
121	    checks_template = []
122	    for check in checks:
123	        entry: dict[str, object] = {
124	            "id": check["id"],
125	            "question": check["question"],
126	            "guidance": check.get("guidance", ""),
127	            "findings": [],
128	        }
129	        checks_template.append(entry)
130	
131	    iteration = state.get("iteration", 1)
132	    if iteration > 1:
133	        prior_path = plan_dir / f"critique_v{iteration - 1}.json"
134	        if prior_path.exists():
135	            prior = read_json(prior_path)
136	            active_check_ids = {check["id"] for check in checks}
137	            prior_checks = {
138	                c.get("id"): c for c in prior.get("checks", [])
139	                if isinstance(c, dict) and c.get("id") in active_check_ids
140	            }
141	            registry = load_flag_registry(plan_dir)
142	            flag_status = {f["id"]: f.get("status", "open") for f in registry.get("flags", [])}
143	            for entry in checks_template:
144	                cid = entry["id"]
145	                if cid in prior_checks:
146	                    pc = prior_checks[cid]
147	                    prior_findings = []
148	                    flagged_count = sum(1 for f in pc.get("findings", []) if f.get("flagged"))
149	                    flagged_idx = 0
150	                    for f in pc.get("findings", []):
151	                        pf: dict[str, object] = {
152	                            "detail": f.get("detail", ""),
153	                            "flagged": f.get("flagged", False),
154	                        }
155	                        if f.get("flagged"):
156	                            flagged_idx += 1
157	                            fid = cid if flagged_count == 1 else f"{cid}-{flagged_idx}"
158	                            pf["status"] = flag_status.get(fid, flag_status.get(cid, "open"))
159	                        else:
160	                            pf["status"] = "n/a"
161	                        prior_findings.append(pf)
162	                    entry["prior_findings"] = prior_findings
163	    return checks_template
164	
165	
166	def _build_critique_prompt(
167	    state: PlanState,
168	    context: dict[str, Any],
169	    critique_review_block: str,
170	) -> str:
171	    return textwrap.dedent(
172	        f"""
173	        You are an independent reviewer. Critique the plan against the actual repository.
174	
175	        Project directory:
176	        {context["project_dir"]}
177	
178	        {context["prep_block"]}
179	
180	        {context["prep_instruction"]}
181	
182	        {intent_and_notes_block(state)}
183	
184	        Plan:
185	        {context["latest_plan"]}
186	
187	        Plan metadata:
188	        {json_dump(context["latest_meta"]).strip()}
189	
190	        Plan structure warnings from validator:
191	        {json_dump(context["structure_warnings"]).strip()}
192	
193	        Existing flags:
194	        {json_dump(context["unresolved"]).strip()}
195	
196	        {context["debt_block"]}
197	
198	        {critique_review_block}
199	
200	        Additional guidelines:
201	        - Robustness level: {context["robustness"]}. {robustness_critique_instruction(context["robustness"])}
202	        - Over-engineering: prefer the simplest approach that fully solves the problem.
203	        - Reuse existing flag IDs when the same concern is still open.
204	        - `verified_flag_ids`: list flag IDs from prior iterations that the revised plan actually resolves (e.g., if the plan was revised to fix FLAG-001, and you confirm the fix is correct, include "FLAG-001"). Only include flags you've verified — don't guess.
205	        - Verify that the plan follows the expected structure when validator warnings or the outline suggest drift.
206	        - Additional flags may use these categories: correctness, security, completeness, performance, maintainability, other.
207	        - Focus on concrete issues, not structural formatting.
208	        """
209	    ).strip()
210	
211	
212	def _write_critique_template(
213	    plan_dir: Path,
214	    state: PlanState,
215	    checks: tuple[dict[str, Any], ...],
216	) -> Path:
217	    """Write the critique output template file and return its path.
218	
219	    The file serves as both guide (check questions + guidance) and output
220	    (findings arrays to fill in). This is the model's sole output channel.
221	    """
222	    import json
223	
224	    template: dict[str, object] = {
225	        "checks": _build_checks_template(plan_dir, state, checks),
226	        "flags": [],
227	        "verified_flag_ids": [],
228	        "disputed_flag_ids": [],
229	    }
230	
231	    output_path = plan_dir / "critique_output.json"
232	    output_path.write_text(json.dumps(template, indent=2), encoding="utf-8")
233	    return output_path
234	
235	
236	def write_single_check_template(
237	    plan_dir: Path,
238	    state: PlanState,
239	    check: dict[str, Any],
240	    output_name: str,
241	) -> Path:
242	    import json
243	
244	    template: dict[str, object] = {
245	        "checks": _build_checks_template(plan_dir, state, (check,)),
246	        "flags": [],
247	        "verified_flag_ids": [],
248	        "disputed_flag_ids": [],
249	    }
250	
251	    output_path = plan_dir / output_name
252	    output_path.write_text(json.dumps(template, indent=2), encoding="utf-8")
253	    return output_path
254	
255	
256	def _critique_prompt(state: PlanState, plan_dir: Path, root: Path | None = None) -> str:
257	    context = _critique_context(state, plan_dir, root)
258	    active_checks = checks_for_robustness(context["robustness"])
259	    # Write the template file — this is both the guide and the output
260	    output_path = _write_critique_template(plan_dir, state, active_checks)
261	    iteration = state.get("iteration", 1)
262	
263	    if active_checks:
264	        iteration_context = ""
265	        if iteration > 1:
266	            iteration_context = (
267	                "\n\n            This is critique iteration {iteration}. "
268	                "The template file includes prior findings with their status. "
269	                "Verify addressed flags were actually fixed, re-flag if inadequate, "
270	                "and check for new issues introduced by the revision."
271	            ).format(iteration=iteration)
272	        critique_review_block = textwrap.dedent(
273	            f"""
274	            Your output template is at: {output_path}
275	            Read this file first — it contains {len(active_checks)} checks, each with a question and guidance.
276	            For each check, investigate the codebase, then add your findings to the `findings` array for that check.
277	
278	            Each finding needs:
279	            - "detail": what you specifically checked and what you found (at least a full sentence)
280	            - "flagged": true if this describes a difference, risk, or tension — even if you think it's justified. false only if purely informational with no possible downside.
281	            - Every check must end with at least one finding. Never leave a `findings` array empty. If you found no issue, add one detailed `flagged: false` finding explaining what you checked and why it appears clear.
282	
283	            When in doubt, flag it — the gate can accept tradeoffs, but it can't act on findings it never sees.
284	
285	            Good: {{"detail": "Checked callers of nthroot_mod in solveset.py line 1205 — passes prime moduli only, consistent with the fix.", "flagged": false}}
286	            Good: {{"detail": "The fix handles empty tuples but not single-element tuples which need a trailing comma.", "flagged": true}}
287	            Bad: {{"detail": "No issue found", "flagged": false}}  ← too brief, will be rejected
288	            Bad: {{"detail": "The hints suggest approach X but the plan uses Y. However Y is consistent with X's intent.", "flagged": false}}  ← a different approach than the hints IS a flag. You found a divergence — flag it. The gate decides if it's acceptable.
289	
290	            After filling in checks, add any additional concerns to the `flags` array (e.g., security, performance, dependencies).
291	            Use the standard format (id, concern, category, severity_hint, evidence). This array can be empty.
292	
293	            Workflow: read the file → investigate → read file again → add finding → write file back. Repeat for each check.{iteration_context}
294	        """
295	        ).strip()
296	    else:
297	        critique_review_block = textwrap.dedent(
298	            f"""
299	            Your output template is at: {output_path}
300	            Review the plan with a broad scope. Consider whether the approach is correct, whether it covers
301	            all the places it needs to, whether it would break callers or violate codebase conventions,
302	            and whether its verification strategy is adequate.
303	
304	            Place any concrete concerns in the `flags` array in the template file using the standard format
305	            (id, concern, category, severity_hint, evidence). Leave `checks` as an empty array.
306	
307	            Workflow: read the file → investigate → read file again → add findings → write file back.
308	        """
309	        ).strip()
310	    return _build_critique_prompt(state, context, critique_review_block)
311	
312	
313	def single_check_critique_prompt(
314	    state: PlanState,
315	    plan_dir: Path,
316	    root: Path | None,
317	    check: dict[str, Any],
318	    template_path: Path,
319	) -> str:
320	    context = _critique_context(state, plan_dir, root)
321	    iteration = state.get("iteration", 1)
322	    iteration_context = ""
323	    if iteration > 1:
324	        iteration_context = (
325	            "\n\n            This is critique iteration {iteration}. "
326	            "The template file includes prior findings with their status. "
327	            "Verify addressed flags were actually fixed, re-flag if inadequate, "
328	            "and check for new issues introduced by the revision."
329	        ).format(iteration=iteration)
330	    critique_review_block = textwrap.dedent(
331	        f"""
332	        Your output template is at: {template_path}
333	        Read this file first — it contains 1 check with a question and guidance.
334	        Investigate only this check, then add your findings to the `findings` array for that check.
335	
336	        Check ID: {check["id"]}
337	        Question: {check["question"]}
338	        Guidance: {check.get("guidance", "")}
339	
340	        Each finding needs:
341	        - "detail": what you specifically checked and what you found (at least a full sentence)
342	        - "flagged": true if this describes a difference, risk, or tension — even if you think it's justified. false only if purely informational with no possible downside.
343	        - This check must end with at least one finding. Never leave its `findings` array empty. If you found no issue, add one detailed `flagged: false` finding explaining what you checked and why it appears clear.
344	
345	        When in doubt, flag it — the gate can accept tradeoffs, but it can't act on findings it never sees.
346	
347	        Good: {{"detail": "Checked callers of nthroot_mod in solveset.py line 1205 — passes prime moduli only, consistent with the fix.", "flagged": false}}
348	        Good: {{"detail": "The fix handles empty tuples but not single-element tuples which need a trailing comma.", "flagged": true}}
349	        Bad: {{"detail": "No issue found", "flagged": false}}  ← too brief, will be rejected
350	        Bad: {{"detail": "The hints suggest approach X but the plan uses Y. However Y is consistent with X's intent.", "flagged": false}}  ← a different approach than the hints IS a flag. You found a divergence — flag it. The gate decides if it's acceptable.
351	
352	        After filling in checks, add any additional concerns to the `flags` array (e.g., security, performance, dependencies).
353	        Use the standard format (id, concern, category, severity_hint, evidence). This array can be empty.
354	
355	        Workflow: read the file → investigate → read file again → add finding → write file back. Repeat for this check.{iteration_context}
356	    """
357	    ).strip()
358	    return _build_critique_prompt(state, context, critique_review_block)
359
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

> AGENT

Perfect! Now I have all the files. Let me provide a comprehensive report of all the prompt files and their contents.

## Report: megaplan/prompts Directory

I've successfully read all the prompt-related files in the `/Users/user_c042661f/Documents/megaplan/megaplan/prompts/` directory. Here's a summary:

### Files Found and Their Contents:

**1. `/megaplan/prompts/__init__.py`** (185 lines)
- Main dispatch table for prompt builders
- Defines three model-specific prompt builder dictionaries: `_CLAUDE_PROMPT_BUILDERS`, `_CODEX_PROMPT_BUILDERS`, and `_HERMES_PROMPT_BUILDERS`
- Maps step names (plan, prep, critique, revise, gate, finalize, execute, review) to their respective builder functions
- Provides `create_claude_prompt()`, `create_codex_prompt()`, and `create_hermes_prompt()` functions that dispatch to builders
- Includes a nested harness guard to prevent recursive megaplan invocations
- Exports all public builders and helper functions

**2. `/megaplan/prompts/execute.py`** (387 lines)
- Builds execution-phase prompts
- Key functions:
  - `_execute_prompt()` - Main execution prompt builder
  - `_execute_batch_prompt()` - For batched task execution
  - `_execute_review_block()` - Includes findings from prior review phase
  - `_execute_nudges()` - Adds sense checks, watch items, and debt reminders
  - `_execute_rerun_guidance()` - Handles re-execution and rework scenarios
  - `_execute_approval_note()` - Notes approval status
- Contains `_EXECUTE_OUTPUT_SHAPE_EXAMPLE` showing expected executor JSON output format
- Contains `_EXECUTE_REQUIREMENTS_TEMPLATE` with execution constraints and verification guidelines

**3. `/megaplan/prompts/review.py`** (563 lines)
- Builds review-phase prompts
- Key functions:
  - `_review_prompt()` - Main review prompt with criteria, task, and sense-check guidance
  - `single_check_review_prompt()` - Focused parallel review for one check dimension
  - `parallel_criteria_review_prompt()` - Parallel mode criteria-only review, anchored to issue text
  - `_review_template_payload()` - Pre-populated template with task/sense-check IDs
  - `_write_review_template()` - Writes output template with verdicts and criteria
  - `_build_review_checks_template()` - Builds check templates with prior findings for iteration
  - `_settled_decisions_review_block()` - Displays gate decisions for verification
- Supports multiple review modes (parallel vs. full) and iterations

**4. `/megaplan/prompts/finalize.py`** (100 lines)
- Builds finalize-phase prompt that prepares execution-ready briefing
- Key function:
  - `_finalize_prompt()` - Creates structured JSON output (tasks, watch items, sense checks, validation coverage)
- Requires tasks array with IDs, descriptions, dependencies, status, and executor notes
- Validates plan coverage by mapping each plan step to finalize tasks
- Includes guidance on task proportionality and final verification requirements

**5. `/megaplan/prompts/planning.py`** (193 lines)
- Builds planning and prep phase prompts
- Key functions:
  - `_plan_prompt()` - Main planning prompt builder
  - `_prep_prompt()` - Engineering brief builder (analyzes codebase to produce brief)
- Contains `PLAN_TEMPLATE` - Example markdown structure for plans (phases, steps, execution order, validation order)
- Prep phase decides whether investigation is needed or can skip; if not skipping, searches codebase for relevant files, functions, tests, constraints, and suggests approach
- Plan phase uses engineering brief as starting hypothesis but encourages verification

**6. `/megaplan/prompts/critique.py`** (359 lines)
- Builds critique and revise phase prompts
- Key functions:
  - `_critique_prompt()` - Independent reviewer prompt
  - `_revise_prompt()` - Plan revision prompt after critique
  - `single_check_critique_prompt()` - Focused critique on one dimension
  - `_write_critique_template()` - Template for critique output
  - `_build_critique_prompt()` - Helper to build full critique prompt
  - `_critique_context()` - Gathers context (prep, plan, metadata, unresolved flags, debt)
  - `_build_checks_template()` - Builds checks with prior findings for iteration
- Supports robustness-based check selection
- Tracks flag status across iterations

**7. `/megaplan/prompts/gate.py`** (169 lines)
- Builds gate-phase prompt for continuation decision
- Key functions:
  - `_gate_prompt()` - Gatekeeper decision prompt (PROCEED/ITERATE/ESCALATE)
  - `_collect_critique_summaries()` - Compiles critique history for finalize
  - `_flag_summary()` - Compact flag list for finalize
- Handles blocking vs. noted flags
- Requires resolution strategies (dispute, accept_tradeoff) for blocking flags
- Tracks settled decisions to carry into review/execution

**8. `/megaplan/prompts/_shared.py`** (253 lines) - **Shared Helpers**
- Common utilities used across phases
- Key functions:
  - `_resolve_prompt_root()` - Determines prompt root directory
  - `_grouped_debt_for_prompt()` - Groups technical debt by subsystem
  - `_escalated_debt_for_prompt()` - Lists critical debt subsystems
  - `_debt_watch_lines()` - Formats debt as watch items
  - `_planning_debt_block()` - Debt context for planning
  - `_gate_debt_block()` - Debt context for gate
  - `_finalize_debt_block()` - Debt watch items for execution
  - `_render_prep_block()` - Transforms prep.json into markdown engineering brief with task summary, evidence, code locations, test expectations, constraints, and suggested approach

### Notes:

- **No `prep.py` file exists** — prep-related functions are in `planning.py` as `_prep_prompt()`
- All phases use `_render_prep_block()` from `_shared.py` to incorporate engineering brief into their prompts
- The architecture supports parallel review modes and iterative refinement with flag tracking
- Heavy use of `json_dump()` and template formatting for structured outputs

> DEVELOPER

Read the following files in /Users/user_c042661f/Documents/megaplan and report their full contents:
1. megaplan/execution.py (focus on _merge_batch_results around line 256, _build_aggregate_execution_payload around line 136, _run_and_merge_batch around line 349, _check_done_task_evidence)
2. megaplan/evaluation.py (focus on validate_execution_evidence around line 123)
3. megaplan/execution_timeout.py (focus on _merge_timeout_checkpoint around line 110, _reset_timeout_invalid_tasks around line 41, _recover_execute_timeout around line 163)
4. megaplan/handlers.py (focus on _write_finalize_artifacts around line 376, and _build_status_payload around line 285)
5. megaplan/cli.py (focus on _build_status_payload around line 285)

Report the actual line numbers for each function so I know exact locations.

> AGENT

I'll read these files and report their contents with line numbers.

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execution.py"
}
```

> TOOL

tool_result Read
```
File content (10496 tokens) exceeds maximum allowed tokens (10000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py"
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
81	    return p.as_posix()
82	
83	
84	def _parse_git_status_paths(stdout: str) -> set[str]:
85	    paths: set[str] = set()
86	    for raw_line in stdout.splitlines():
87	        if not raw_line.strip():
88	            continue
89	        path_text = raw_line[3:].strip() if len(raw_line) >= 4 else raw_line.strip()
90	        if " -> " in path_text:
91	            path_text = path_text.split(" -> ", 1)[1]
92	        cleaned = path_text.strip().strip('"')
93	        if not cleaned:
94	            continue
95	        is_dir = cleaned.endswith("/")
96	        normalized = _normalize_repo_path(cleaned)
97	        if is_dir and not normalized.endswith("/"):
98	            normalized += "/"
99	        paths.add(normalized)
100	    return paths
101	
102	
103	def is_rubber_stamp(text: str, *, strict: bool = False) -> bool:
104	    stripped = text.strip()
105	    normalized = normalize_text(text).strip(" .!?,;:")
106	    if normalized in _GENERIC_ACKS:
107	        return True
108	    if not strict:
109	        return False
110	    if len(stripped) <= _MIN_VERDICT_CHARS:
111	        return True
112	    words = stripped.split()
113	    if len(words) < _MIN_VERDICT_WORDS:
114	        return True
115	    unique_words = {word.lower() for word in words}
116	    return len(unique_words) < _MIN_VERDICT_UNIQUE_WORDS
117	
118	
119	def _is_perfunctory_ack(note: str) -> bool:
120	    return is_rubber_stamp(note, strict=False)
121	
122	
123	def validate_execution_evidence(finalize_data: dict[str, Any], project_dir: Path) -> dict[str, Any]:
124	    findings: list[str] = []
125	    files_claimed = sorted(
126	        {
127	            _normalize_repo_path(path, project_dir)
128	            for task in finalize_data.get("tasks", [])
129	            for path in task.get("files_changed", [])
130	            if isinstance(path, str) and path.strip()
131	        }
132	    )
133	
134	    if not (project_dir / ".git").exists():
135	        return {
136	            "findings": findings,
137	            "files_in_diff": [],
138	            "files_claimed": files_claimed,
139	            "skipped": True,
140	            "reason": "Project directory is not a git repository.",
141	        }
142	
143	    try:
144	        process = subprocess.run(
145	            ["git", "status", "--short"],
146	            cwd=str(project_dir),
147	            text=True,
148	            capture_output=True,
149	            timeout=30,
150	        )
151	    except FileNotFoundError:
152	        return {
153	            "findings": findings,
154	            "files_in_diff": [],
155	            "files_claimed": files_claimed,
156	            "skipped": True,
157	            "reason": "git not found on PATH.",
158	        }
159	    except subprocess.TimeoutExpired:
160	        return {
161	            "findings": findings,
162	            "files_in_diff": [],
163	            "files_claimed": files_claimed,
164	            "skipped": True,
165	            "reason": "git status timed out.",
166	        }
167	
168	    if process.returncode != 0:
169	        return {
170	            "findings": findings,
171	            "files_in_diff": [],
172	            "files_claimed": files_claimed,
173	            "skipped": True,
174	            "reason": f"git status failed: {process.stderr.strip() or process.stdout.strip()}",
175	        }
176	
177	    files_in_diff = sorted(_parse_git_status_paths(process.stdout))
178	    claimed_set = set(files_claimed)
179	    diff_set = set(files_in_diff)
180	
181	    # Git status reports untracked directories as `dir/` (trailing slash).
182	    # A claimed file beneath such a directory should be considered present.
183	    dir_prefixes = [p for p in diff_set if p.endswith("/")]
184	
185	    def _covered_by_diff(claimed: str) -> bool:
186	        if claimed in diff_set:
187	            return True
188	        return any(claimed.startswith(prefix) or claimed == prefix.rstrip("/") for prefix in dir_prefixes)
189	
190	    phantom_claims = sorted(c for c in claimed_set if not _covered_by_diff(c))
191	    if phantom_claims:
192	        findings.append(
193	            "Executor claimed changed files not present in git status: "
194	            + ", ".join(phantom_claims)
195	        )
196	
197	    # For the reverse check, treat a directory as "claimed" when any claimed
198	    # path is under it.
199	    def _dir_is_claimed(diff_path: str) -> bool:
200	        if not diff_path.endswith("/"):
201	            return False
202	        return any(c.startswith(diff_path) for c in claimed_set)
203	
204	    unclaimed_changes = sorted(
205	        d for d in diff_set
206	        if d not in claimed_set and not _dir_is_claimed(d)
207	    )
208	    if unclaimed_changes:
209	        findings.append(
210	            "Git status shows changed files not claimed by any task: "
211	            + ", ".join(unclaimed_changes)
212	        )
213	
214	    for sense_check in finalize_data.get("sense_checks", []):
215	        sense_check_id = sense_check.get("id", "?")
216	        note = sense_check.get("executor_note", "")
217	        if not isinstance(note, str) or not note.strip():
218	            findings.append(f"Sense check {sense_check_id} is missing an executor acknowledgment.")
219	            continue
220	        if _is_perfunctory_ack(note):
221	            findings.append(
222	                f"Sense check {sense_check_id} acknowledgment is perfunctory: {note.strip()!r}."
223	            )
224	
225	    for task in finalize_data.get("tasks", []):
226	        if task.get("status") != "done":
227	            continue
228	        task_id = task.get("id", "?")
229	        notes = task.get("executor_notes", "")
230	        if not isinstance(notes, str) or not notes.strip():
231	            continue
232	        if is_rubber_stamp(notes, strict=True):
233	            findings.append(
234	                f"Task {task_id} executor_notes are perfunctory: {notes.strip()!r}."
235	            )
236	
237	    return {
238	        "findings": findings,
239	        "files_in_diff": files_in_diff,
240	        "files_claimed": files_claimed,
241	        "skipped": False,
242	        "reason": "",
243	    }
244	
245	
246	def flag_weight(flag: FlagRecord) -> float:
247	    """Weight a flag for gate context. Higher = more blocking."""
248	    category = flag.get("category", "other")
249	    concern = flag.get("concern", "").lower()
250	
251	    if category == "security":
252	        return 3.0
253	
254	    implementation_detail_signals = [
255	        "column",
256	        "schema",
257	        "field",
258	        "as written",
259	        "pseudocode",
260	        "seed sql",
261	        "placeholder",
262	    ]
263	    if any(signal in concern for signal in implementation_detail_signals):
264	        return 0.5
265	
266	    weights = {
267	        "correctness": 2.0,
268	        "completeness": 1.5,
269	        "performance": 1.0,
270	        "maintainability": 0.75,
271	        "other": 1.0,
272	    }
273	    return weights.get(category, 1.0)
274	
275	
276	def compute_plan_delta_percent(previous_text: str | None, current_text: str) -> float | None:
277	    if previous_text is None:
278	        return None
279	    ratio = SequenceMatcher(None, previous_text, current_text).ratio()
280	    return round((1.0 - ratio) * 100.0, 2)
281	
282	
283	def compute_recurring_critiques(plan_dir: Path, iteration: int) -> list[str]:
284	    if iteration < 2:
285	        return []
286	    previous = read_json(current_iteration_artifact(plan_dir, "critique", iteration - 1))
287	    current = read_json(current_iteration_artifact(plan_dir, "critique", iteration))
288	    previous_concerns = {normalize_text(flag.get("concern", "")) for flag in previous.get("flags", []) if isinstance(flag, dict)}
289	    current_concerns = {normalize_text(flag.get("concern", "")) for flag in current.get("flags", []) if isinstance(flag, dict)}
290	    return sorted(previous_concerns.intersection(current_concerns))
291	
292	
293	def _strip_fenced_blocks(text: str) -> str:
294	    kept_lines: list[str] = []
295	    inside_fence = False
296	    for line in text.splitlines(keepends=True):
297	        if line.startswith("```"):
298	            inside_fence = not inside_fence
299	            continue
300	        if not inside_fence:
301	            kept_lines.append(line)
302	    if inside_fence:
303	        # Unclosed fence — return original text rather than silently dropping content
304	        return text
305	    return "".join(kept_lines)
306	
307	
308	def _match_section_boundary(line: str) -> tuple[bool, str | None]:
309	    """Check if a line is a section boundary. Returns (is_boundary, section_id)."""
310	    step_match = _PLAN_STEP_RE.match(line) or _PLAN_PHASE_STEP_RE.match(line)
311	    if step_match:
312	        return True, f"S{step_match.group(1)}"
313	    if _PLAN_HEADING_RE.match(line) or _PLAN_PHASE_HEADING_RE.match(line):
314	        return True, None
315	    return False, None
316	
317	
318	def parse_plan_sections(plan_text: str) -> list[PlanSection]:
319	    lines = plan_text.splitlines(keepends=True)
320	    if not lines:
321	        return [PlanSection(heading="", body="", id=None, start_line=1, end_line=0)]
322	
323	    boundaries: list[tuple[int, int, str, str | None]] = []
324	    inside_fence = False
325	    for index, line in enumerate(lines):
326	        if line.startswith("```"):
327	            inside_fence = not inside_fence
328	            continue
329	        if inside_fence:
330	            continue
331	        is_boundary, section_id = _match_section_boundary(line)
332	        if is_boundary:
333	            boundaries.append((index, index + 1, line.rstrip("\n"), section_id))
334	
335	    if inside_fence:
336	        # Unclosed fence — re-scan ignoring fence state so we don't silently lose sections
337	        boundaries = []
338	        for index, line in enumerate(lines):
339	            is_boundary, section_id = _match_section_boundary(line)
340	            if is_boundary:
341	                boundaries.append((index, index + 1, line.rstrip("\n"), section_id))
342	
343	    if not boundaries:
344	        return [PlanSection(heading="", body=plan_text, id=None, start_line=1, end_line=len(lines))]
345	
346	    sections: list[PlanSection] = []
347	    first_index, first_line, _, _ = boundaries[0]
348	    if first_index > 0:
349	        sections.append(
350	            PlanSection(
351	                heading="",
352	                body="".join(lines[:first_index]),
353	                id=None,
354	                start_line=1,
355	                end_line=first_line - 1,
356	            )
357	        )
358	
359	    for boundary_index, (start_index, start_line, heading, section_id) in enumerate(boundaries):
360	        next_start_index = boundaries[boundary_index + 1][0] if boundary_index + 1 < len(boundaries) else len(lines)
361	        sections.append(
362	            PlanSection(
363	                heading=heading,
364	                body="".join(lines[start_index:next_start_index]),
365	                id=section_id,
366	                start_line=start_line,
367	                end_line=next_start_index,
368	            )
369	        )
370	    return sections
371	
372	
373	def reassemble_plan(sections: list[PlanSection]) -> str:
374	    return "".join(section.body for section in sections)
375	
376	
377	def renumber_steps(sections: list[PlanSection]) -> list[PlanSection]:
378	    renumbered: list[PlanSection] = []
379	    step_number = 1
380	    for section in sections:
381	        if section.id is None:
382	            renumbered.append(section)
383	            continue
384	        # Detect heading level (## or ###) and preserve it
385	        step_prefix_match = re.match(r"^(#{2,3})\s+Step\s+\d+:", section.heading)
386	        if not step_prefix_match:
387	            renumbered.append(section)
388	            continue
389	        hashes = step_prefix_match.group(1)
390	        new_heading = re.sub(rf"^{hashes}\s+Step\s+\d+:", f"{hashes} Step {step_number}:", section.heading, count=1)
391	        new_body = re.sub(rf"^{hashes}\s+Step\s+\d+:", f"{hashes} Step {step_number}:", section.body, count=1, flags=re.MULTILINE)
392	        renumbered.append(
393	            PlanSection(
394	                heading=new_heading,
395	                body=new_body,
396	                id=f"S{step_number}",
397	                start_line=section.start_line,
398	                end_line=section.end_line,
399	            )
400	        )
401	        step_number += 1
402	    return renumbered
403	
404	
405	def validate_plan_structure(plan_text: str) -> list[str]:
406	    issues: list[str] = []
407	    stripped = _strip_fenced_blocks(plan_text)
408	
409	    if len(re.findall(r"(?mi)^#\s+.+$", stripped)) != 1:
410	        issues.append("Plan should have exactly one H1 title.")
411	    if not re.search(r"(?mi)^##\s+Overview\s*$", stripped):
412	        issues.append("Plan should include a `## Overview` section.")
413	
414	    # Accept both flat (## Step N:) and hierarchical (### Step N: under ## Phase)
415	    step_matches = list(re.finditer(r"(?im)^#{2,3}\s+Step\s+\d+:\s+.+$", stripped))
416	    if not step_matches:
417	        issues.append(PLAN_STRUCTURE_REQUIRED_STEP_ISSUE)
418	        return issues
419	
420	    if not (
421	        re.search(r"(?mi)^##\s+Execution Order\s*$", stripped)
422	        or re.search(r"(?mi)^##\s+Validation Order\s*$", stripped)
423	    ):
424	        issues.append("Plan should include `## Execution Order` or `## Validation Order`.")
425	
426	    missing_substeps = False
427	    missing_file_refs = False
428	    for index, match in enumerate(step_matches):
429	        start = match.end()
430	        next_heading = re.search(r"(?im)^#{2,3}\s+.+$", stripped[start:])
431	        end = start + next_heading.start() if next_heading else len(stripped)
432	        section = stripped[match.start():end]
433	        if not re.search(r"(?m)^\d+\.\s+", stripped[start:end]):
434	            missing_substeps = True
435	        if not re.search(r"`[^`]+`", section):
436	            missing_file_refs = True
437	
438	    if missing_substeps:
439	        issues.append("Each step section should include at least one numbered substep.")
440	    if missing_file_refs:
441	        issues.append("Each step section should reference at least one file in backticks.")
442	    return issues
443	
444	
445	def _previous_iteration_plan_path(plan_dir: Path, state: PlanState) -> Path | None:
446	    current_version = state["iteration"]
447	    previous_version = current_version - 1
448	    if previous_version < 1:
449	        return None
450	    matching = [
451	        record
452	        for record in state["plan_versions"]
453	        if record.get("version") == previous_version
454	    ]
455	    if not matching:
456	        return None
457	    return plan_dir / matching[-1]["file"]
458	
459	
460	def build_gate_signals(plan_dir: Path, state: PlanState, root: Path | None = None) -> GateSignals:
461	    iteration = state["iteration"]
462	    flag_registry = load_flag_registry(plan_dir)
463	    unresolved = unresolved_significant_flags(flag_registry)
464	    robustness = configured_robustness(state)
465	    open_scope_creep = scope_creep_flags(flag_registry, statuses=FLAG_BLOCKING_STATUSES)
466	    debt_root = root
467	    if debt_root is None:
468	        debt_root = plan_dir.parents[2] if len(plan_dir.parents) >= 3 else plan_dir
469	    debt_registry = load_debt_registry(debt_root)
470	    significant_count = len(
471	        [
472	            flag
473	            for flag in flag_registry["flags"]
474	            if flag.get("severity") == "significant" and flag["status"] != "verified"
475	        ]
476	    )
477	    weighted_score = round(sum(flag_weight(flag) for flag in unresolved), 2)
478	    weighted_history = list(state["meta"].get("weighted_scores", []))
479	    latest_plan_text = latest_plan_path(plan_dir, state).read_text(encoding="utf-8")
480	    previous_plan_path = _previous_iteration_plan_path(plan_dir, state)
481	    previous_text = None
482	    if previous_plan_path is not None and previous_plan_path.exists():
483	        previous_text = previous_plan_path.read_text(encoding="utf-8")
484	    plan_delta = compute_plan_delta_percent(previous_text, latest_plan_text)
485	    recurring = compute_recurring_critiques(plan_dir, iteration)
486	    resolved_flags = [
487	        {
488	            "id": flag["id"],
489	            "concern": flag["concern"],
490	            "resolution": flag.get("evidence", ""),
491	        }
492	        for flag in flag_registry["flags"]
493	        if flag["status"] == "verified"
494	    ]
495	
496	    delta_history = state["meta"].get("plan_deltas", [])
497	    if weighted_history:
498	        trajectory = " -> ".join(str(score) for score in weighted_history) + f" -> {weighted_score}"
499	    else:
500	        trajectory = str(weighted_score)
501	    delta_summary = ", ".join(
502	        "n/a" if delta is None else f"{delta:.1f}%"
503	        for delta in delta_history
504	    ) or "n/a"
505	    loop_summary = (
506	        f"Iteration {iteration}. Weighted score trajectory: {trajectory}. "
507	        f"Plan deltas: {delta_summary}. "
508	        f"Recurring critiques: {len(recurring)}. "
509	        f"Resolved flags: {len(resolved_flags)}. "
510	        f"Open significant flags: {len(unresolved)}."
511	    )
512	    debt_overlaps = []
513	    overlapping_escalated_subsystems: set[str] = set()
514	    escalated_lookup = {
515	        subsystem: total
516	        for subsystem, total, _entries in escalated_subsystems(debt_registry)
517	    }
518	    for flag in unresolved:
519	        subsystem = extract_subsystem_tag(flag["concern"])
520	        match = find_matching_debt(debt_registry, subsystem, flag["concern"])
521	        if match is None:
522	            continue
523	        debt_overlaps.append(
524	            {
525	                "flag_id": flag["id"],
526	                "debt_id": match["id"],
527	                "subsystem": subsystem,
528	                "concern": flag["concern"],
529	                "debt_concern": match["concern"],
530	                "occurrence_count": match["occurrence_count"],
531	                "plan_ids": match["plan_ids"],
532	            }
533	        )
534	        if subsystem in escalated_lookup:
535	            overlapping_escalated_subsystems.add(subsystem)
536	
537	    result: GateSignals = {
538	        "robustness": robustness,
539	        "signals": {
540	            "iteration": iteration,
541	            "idea": state.get("idea", ""),
542	            "significant_flags": significant_count,
543	            "unresolved_flags": [
544	                {
545	                    "id": flag["id"],
546	                    "concern": flag["concern"],
547	                    "category": flag["category"],
548	                    "severity": flag.get("severity", "unknown"),
549	                    "status": flag["status"],
550	                }
551	                for flag in unresolved
552	            ],
553	            "resolved_flags": resolved_flags,
554	            "weighted_score": weighted_score,
555	            "weighted_history": weighted_history,
556	            "plan_delta_from_previous": plan_delta,
557	            "recurring_critiques": recurring,
558	            "scope_creep_flags": [flag["id"] for flag in open_scope_creep],
559	            "loop_summary": loop_summary,
560	            "debt_overlaps": debt_overlaps,
561	            "escalated_debt_subsystems": [
562	                {
563	                    "subsystem": subsystem,
564	                    "total_occurrences": escalated_lookup[subsystem],
565	                }
566	                for subsystem in sorted(overlapping_escalated_subsystems)
567	            ],
568	        },
569	        "warnings": [],
570	    }
571	    if open_scope_creep:
572	        result["warnings"].append(
573	            "Scope creep detected: the plan appears to be expanding beyond the original idea or recorded user notes."
574	        )
575	    if iteration >= 5:
576	        result["warnings"].append(f"Iteration {iteration}: high iteration count.")
577	    if iteration >= 12:
578	        result["warnings"].append(
579	            f"Iteration {iteration}: hard iteration limit reached. Escalation is likely warranted."
580	        )
581	    for subsystem in sorted(overlapping_escalated_subsystems):
582	        result["warnings"].append(
583	            "Recurring debt detected in subsystem "
584	            f"'{subsystem}' (total occurrences: {escalated_lookup[subsystem]}). "
585	            "Recommend holistic redesign rather than another point fix."
586	        )
587	    return result
588	
589	
590	def run_gate_checks(
591	    plan_dir: Path,
592	    state: PlanState,
593	    *,
594	    command_lookup: Callable[[str], str | None] | None = None,
595	) -> GateCheckResult:
596	    project_dir = Path(state["config"]["project_dir"])
597	    meta = read_json(latest_plan_meta_path(plan_dir, state))
598	    flag_registry = load_flag_registry(plan_dir)
599	    unresolved = unresolved_significant_flags(flag_registry)
600	    lookup = command_lookup or (lambda name: None)
601	    configured_agent = state.get("config", {}).get("agent", "")
602	    checks: dict[str, bool] = {
603	        "project_dir_exists": project_dir.exists(),
604	        "project_dir_writable": os.access(project_dir, os.W_OK),
605	        "success_criteria_present": bool(meta.get("success_criteria")),
606	    }
607	    if configured_agent != "hermes":
608	        checks["claude_available"] = bool(lookup("claude"))
609	        checks["codex_available"] = bool(lookup("codex"))
610	    return {
611	        "passed": all(checks.values()),
612	        "criteria_check": {
613	            "count": len(meta.get("success_criteria", [])),
614	            "items": meta.get("success_criteria", []),
615	        },
616	        "preflight_results": checks,
617	        "unresolved_flags": unresolved,
618	    }
619	
620	
621	def build_gate_artifact(
622	    signals: dict[str, Any],
623	    gate_payload: GatePayload,
624	    *,
625	    override_forced: bool,
626	    orchestrator_guidance: str = "",
627	) -> GateArtifact:
628	    preflight = signals["preflight_results"]
629	    recommendation = gate_payload["recommendation"]
630	    warnings = list(signals.get("warnings", [])) + list(gate_payload.get("warnings", []))
631	    return {
632	        "passed": recommendation == "PROCEED" and all(preflight.values()),
633	        "criteria_check": signals["criteria_check"],
634	        "preflight_results": preflight,
635	        "unresolved_flags": signals["unresolved_flags"],
636	        "recommendation": recommendation,
637	        "rationale": gate_payload["rationale"],
638	        "signals_assessment": gate_payload["signals_assessment"],
639	        "warnings": warnings,
640	        "settled_decisions": list(gate_payload.get("settled_decisions", [])),
641	        "override_forced": override_forced,
642	        "orchestrator_guidance": orchestrator_guidance,
643	        "robustness": signals.get("robustness"),
644	        "signals": signals["signals"],
645	        # Gate's flag resolution — used by handler to allow PROCEED past blocking flags
646	        "flag_resolutions": list(gate_payload.get("flag_resolutions", [])),
647	        # Backward compatibility: carry through old-format fields if present
648	        "resolved_flag_ids": list(gate_payload.get("resolved_flag_ids", [])),
649	        "resolution_summary": gate_payload.get("resolution_summary", ""),
650	    }
651	
652	
653	def build_orchestrator_guidance(
654	    gate_payload: GatePayload,
655	    signals: dict[str, Any],
656	    preflight_passed: bool,
657	    preflight_results: dict[str, bool],
658	    robustness: str,
659	    plan_name: str,
660	) -> str:
661	    """Return plain-language next-step guidance for the orchestrator."""
662	    recommendation = gate_payload["recommendation"]
663	    iteration = int(signals.get("iteration", 0))
664	    weighted_score = float(signals.get("weighted_score", 0.0))
665	    weighted_history = list(signals.get("weighted_history", []))
666	    recurring_critiques = list(signals.get("recurring_critiques", []))
667	    unresolved_flags = list(signals.get("unresolved_flags", []))
668	    scope_creep = list(signals.get("scope_creep_flags", []))
669	    previous_score = float(weighted_history[-1]) if weighted_history else None
670	    plateaued = previous_score is not None and weighted_score >= previous_score
671	    worsening = previous_score is not None and weighted_score > previous_score
672	    improving = previous_score is not None and weighted_score < previous_score
673	
674	    if iteration == 1:
675	        guidance = f"First iteration; follow gate recommendation: {recommendation}."
676	    elif recommendation == "PROCEED" and preflight_passed:
677	        guidance = "Plan passed gate and preflight. Proceed to finalize."
678	    elif recommendation == "PROCEED":
679	        failing_checks = ", ".join(
680	            name for name, passed in preflight_results.items() if not passed
681	        )
682	        guidance = f"Gate says PROCEED but preflight blocked. Fix: {failing_checks}."
683	    elif recommendation == "ESCALATE":
684	        guidance = "Gate escalated. Ask the user: force-proceed, add-note, or abort."
685	    elif recommendation == "ITERATE" and plateaued and recurring_critiques:
686	        guidance = (
687	            "Score plateaued with recurring critiques the loop can't fix. Consider "
688	            f"force-proceeding: `megaplan override force-proceed --plan {plan_name}`"
689	        )
690	    elif recommendation == "ITERATE" and improving:
691	        guidance = f"Score improving ({previous_score} -> {weighted_score}). Continue to revise."
692	    elif recommendation == "ITERATE" and worsening:
693	        guidance = (
694	            f"Score worsening ({previous_score} -> {weighted_score}). "
695	            "Investigate; the loop may be diverging."
696	        )
697	    else:
698	        guidance = "Gate recommends another iteration. Revise the plan."
699	
700	    hints: list[str] = []
701	    if unresolved_flags:
702	        hints.append("Verify unresolved flags against the plan and project code before accepting.")
703	    if recurring_critiques:
704	        critiques = ", ".join(recurring_critiques)
705	        hints.append(
706	            f"Recurring critiques ({critiques}); the loop likely can't fix these, so judge if they are real blockers."
707	        )
708	    if scope_creep:
709	        hints.append("Scope creep detected; compare the current plan against the original idea.")
710	
711	    return " ".join([guidance, *hints]).strip()
712
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execution_timeout.py"
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	import argparse
4	import json
5	from pathlib import Path
6	from typing import Any
7	
8	from megaplan._core import (
9	    apply_session_update,
10	    append_history,
11	    atomic_write_json,
12	    atomic_write_text,
13	    batch_artifact_path,
14	    make_history_entry,
15	    read_json,
16	    render_final_md,
17	    save_state,
18	    sha256_file,
19	    store_raw_worker_output,
20	)
21	from megaplan.evaluation import validate_execution_evidence
22	from megaplan.execution_quality import (
23	    _check_done_task_evidence,
24	    _normalize_execute_claimed_path,
25	)
26	from megaplan.merge import _validate_and_merge_batch
27	from megaplan.types import CliError, PlanState, STATE_FINALIZED, StepResponse
28	from megaplan.workers import WorkerResult
29	
30	
31	def _resolve_execute_approval_mode(
32	    *, auto_approve: bool, user_approved_gate: bool
33	) -> str:
34	    if auto_approve:
35	        return "auto_approve"
36	    if user_approved_gate:
37	        return "user_approved"
38	    return "manual"
39	
40	
41	def _reset_timeout_invalid_tasks(
42	    finalize_data: dict[str, Any],
43	    *,
44	    execution_audit: dict[str, Any],
45	    issues: list[str],
46	) -> list[str]:
47	    reset_reasons: dict[str, list[str]] = {}
48	    missing_task_ids = _check_done_task_evidence(
49	        finalize_data.get("tasks", []),
50	        issues=issues,
51	        should_classify=lambda task: True,
52	        has_evidence=lambda task: bool(task.get("files_changed")),
53	        has_advisory_evidence=lambda task: bool(task.get("commands_run")),
54	        missing_message="Done tasks missing both files_changed and commands_run during timeout recovery: ",
55	        advisory_message="Advisory: done tasks rely on commands_run without files_changed during timeout recovery: ",
56	    )
57	    for task_id in missing_task_ids:
58	        reset_reasons.setdefault(task_id, []).append(
59	            "missing both files_changed and commands_run"
60	        )
61	
62	    if not execution_audit.get("skipped"):
63	        files_in_diff = {
64	            _normalize_execute_claimed_path(path)
65	            for path in execution_audit.get("files_in_diff", [])
66	            if isinstance(path, str) and path.strip()
67	        }
68	        for task in finalize_data.get("tasks", []):
69	            if task.get("status") != "done":
70	                continue
71	            claimed_paths = [
72	                _normalize_execute_claimed_path(path)
73	                for path in task.get("files_changed", [])
74	                if isinstance(path, str) and path.strip()
75	            ]
76	            if claimed_paths and any(
77	                path not in files_in_diff for path in claimed_paths
78	            ):
79	                reset_reasons.setdefault(task["id"], []).append(
80	                    "claimed files not present in git status"
81	                )
82	
83	    for task in finalize_data.get("tasks", []):
84	        reasons = reset_reasons.get(task.get("id"))
85	        if not reasons:
86	            continue
87	        note_prefix = str(task.get("executor_notes", "")).strip()
88	        reset_note = (
89	            "Timeout recovery reset this task to pending because "
90	            + " and ".join(reasons)
91	            + "."
92	        )
93	        task["status"] = "pending"
94	        task["executor_notes"] = f"{note_prefix} {reset_note}".strip()
95	
96	    if reset_reasons:
97	        issues.append(
98	            "Reset timed-out done tasks to pending after evidence validation: "
99	            + ", ".join(sorted(reset_reasons))
100	        )
101	    return sorted(reset_reasons)
102	
103	
104	def _timeout_checkpoint_path(plan_dir: Path, *, batch_number: int | None) -> Path:
105	    if batch_number is None:
106	        return plan_dir / "execution_checkpoint.json"
107	    return batch_artifact_path(plan_dir, batch_number)
108	
109	
110	def _merge_timeout_checkpoint(
111	    *,
112	    finalize_data: dict[str, Any],
113	    checkpoint_data: dict[str, Any],
114	    checkpoint_name: str,
115	    issues: list[str],
116	) -> None:
117	    tasks_by_id = {
118	        task["id"]: task
119	        for task in finalize_data.get("tasks", [])
120	        if isinstance(task, dict) and isinstance(task.get("id"), str)
121	    }
122	    merged_tasks, _ = _validate_and_merge_batch(
123	        checkpoint_data.get("task_updates"),
124	        required_fields=(
125	            "task_id",
126	            "status",
127	            "executor_notes",
128	            "files_changed",
129	            "commands_run",
130	        ),
131	        targets_by_id=tasks_by_id,
132	        id_field="task_id",
133	        merge_fields=("status", "executor_notes", "files_changed", "commands_run"),
134	        issues=issues,
135	        validation_label=f"{checkpoint_name}.task_updates",
136	        merge_label="checkpoint task_update",
137	        enum_fields={"status": {"done", "skipped", "completed"}},
138	        nonempty_fields={"executor_notes"},
139	        array_fields=("files_changed", "commands_run"),
140	    )
141	    sense_checks_by_id = {
142	        sense_check["id"]: sense_check
143	        for sense_check in finalize_data.get("sense_checks", [])
144	        if isinstance(sense_check, dict) and isinstance(sense_check.get("id"), str)
145	    }
146	    merged_checks, _ = _validate_and_merge_batch(
147	        checkpoint_data.get("sense_check_acknowledgments"),
148	        required_fields=("sense_check_id", "executor_note"),
149	        targets_by_id=sense_checks_by_id,
150	        id_field="sense_check_id",
151	        merge_fields=("executor_note",),
152	        issues=issues,
153	        validation_label=f"{checkpoint_name}.sense_check_acknowledgments",
154	        merge_label="checkpoint sense_check_acknowledgment",
155	        nonempty_fields={"executor_note"},
156	    )
157	    if merged_tasks > 0 or merged_checks > 0:
158	        issues.append(
159	            f"Recovered timeout checkpoint from {checkpoint_name}: merged {merged_tasks} task update(s) and {merged_checks} sense check acknowledgment(s)."
160	        )
161	
162	
163	def _recover_execute_timeout(
164	    *,
165	    plan_dir: Path,
166	    state: PlanState,
167	    error: CliError,
168	    agent: str,
169	    mode: str,
170	    refreshed: bool,
171	    auto_approve: bool,
172	    args: argparse.Namespace,
173	    batch_number: int | None,
174	    persist_state: bool = True,
175	) -> StepResponse:
176	    deviations = [f"Execute timed out: {error.message}"]
177	    finalize_data = read_json(plan_dir / "finalize.json")
178	    checkpoint_path = _timeout_checkpoint_path(plan_dir, batch_number=batch_number)
179	    try:
180	        checkpoint_data = read_json(checkpoint_path)
181	    except FileNotFoundError:
182	        deviations.append(
183	            f"Advisory: timeout checkpoint {checkpoint_path.name} was not found."
184	        )
185	    except json.JSONDecodeError as exc:
186	        deviations.append(
187	            f"Advisory: timeout checkpoint {checkpoint_path.name} was not valid JSON: {exc}"
188	        )
189	    else:
190	        if isinstance(checkpoint_data, dict):
191	            _merge_timeout_checkpoint(
192	                finalize_data=finalize_data,
193	                checkpoint_data=checkpoint_data,
194	                checkpoint_name=checkpoint_path.name,
195	                issues=deviations,
196	            )
197	        else:
198	            deviations.append(
199	                f"Advisory: timeout checkpoint {checkpoint_path.name} did not contain an object."
200	            )
201	
202	    project_dir = Path(state["config"]["project_dir"])
203	    initial_audit = validate_execution_evidence(finalize_data, project_dir)
204	    if initial_audit["skipped"]:
205	        deviations.append(
206	            f"Advisory audit skip during timeout recovery: {initial_audit['reason']}"
207	        )
208	    for finding in initial_audit["findings"]:
209	        deviations.append(f"Advisory audit finding during timeout recovery: {finding}")
210	
211	    _reset_timeout_invalid_tasks(
212	        finalize_data,
213	        execution_audit=initial_audit,
214	        issues=deviations,
215	    )
216	    execution_audit = validate_execution_evidence(finalize_data, project_dir)
217	    atomic_write_json(plan_dir / "execution_audit.json", execution_audit)
218	    atomic_write_json(plan_dir / "finalize.json", finalize_data)
219	    atomic_write_text(
220	        plan_dir / "final.md", render_final_md(finalize_data, phase="execute")
221	    )
222	
223	    finalize_hash = sha256_file(plan_dir / "finalize.json")
224	    raw_output = str(error.extra.get("raw_output") or error.message)
225	    raw_name = store_raw_worker_output(
226	        plan_dir, "execute", state["iteration"], raw_output
227	    )
228	    session_id = error.extra.get("session_id")
229	    timeout_worker = WorkerResult(
230	        payload={},
231	        raw_output=raw_output,
232	        duration_ms=0,
233	        cost_usd=0.0,
234	        session_id=session_id if isinstance(session_id, str) else None,
235	    )
236	    if persist_state:
237	        apply_session_update(
238	            state,
239	            "execute",
240	            agent,
241	            timeout_worker.session_id,
242	            mode=mode,
243	            refreshed=refreshed,
244	        )
245	    user_approved_gate = bool(state["meta"].get("user_approved_gate", False))
246	    approval_mode = _resolve_execute_approval_mode(
247	        auto_approve=auto_approve,
248	        user_approved_gate=user_approved_gate,
249	    )
250	    if persist_state:
251	        append_history(
252	            state,
253	            make_history_entry(
254	                "execute",
255	                duration_ms=0,
256	                cost_usd=0.0,
257	                result="timeout",
258	                worker=timeout_worker,
259	                agent=agent,
260	                mode=mode,
261	                output_file="finalize.json",
262	                artifact_hash=finalize_hash,
263	                finalize_hash=finalize_hash,
264	                raw_output_file=raw_name,
265	                message=error.message,
266	                approval_mode=approval_mode,
267	            ),
268	        )
269	        save_state(plan_dir, state)
270	
271	    tasks = finalize_data.get("tasks", [])
272	    completed_tasks = [
273	        task for task in tasks if task.get("status") in {"done", "skipped"}
274	    ]
275	    files_changed = sorted(
276	        {
277	            path
278	            for task in completed_tasks
279	            for path in task.get("files_changed", [])
280	            if isinstance(path, str) and path.strip()
281	        }
282	    )
283	    summary = (
284	        "Execute timed out after partial progress. "
285	        f"{len(completed_tasks)}/{len(tasks)} tasks remain marked done or skipped on disk. "
286	        "Re-run execute to finish and re-emit structured output."
287	    )
288	    response: StepResponse = {
289	        "success": False,
290	        "step": "execute",
291	        "summary": summary,
292	        "artifacts": ["execution_audit.json", "finalize.json", "final.md"],
293	        "next_step": "execute",
294	        "state": STATE_FINALIZED,
295	        "files_changed": files_changed,
296	        "deviations": deviations,
297	        "warnings": [summary],
298	        "auto_approve": auto_approve,
299	        "user_approved_gate": user_approved_gate,
300	    }
301	    return response
302
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
File content (23984 tokens) exceeds maximum allowed tokens (10000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
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
File content (12571 tokens) exceeds maximum allowed tokens (10000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
```

> AGENT

I need to read the remaining files in sections. Let me read the handlers.py and cli.py files with specific ranges:

> TOOL

tool_use Bash
```json
{
  "command": "wc -l /Users/user_c042661f/Documents/megaplan/megaplan/handlers.py /Users/user_c042661f/Documents/megaplan/megaplan/cli.py /Users/user_c042661f/Documents/megaplan/megaplan/execution.py /Users/user_c042661f/Documents/megaplan/megaplan/execution_timeout.py"
}
```

> TOOL

tool_result Bash
```
2041 /Users/user_c042661f/Documents/megaplan/megaplan/handlers.py
    1063 /Users/user_c042661f/Documents/megaplan/megaplan/cli.py
    1007 /Users/user_c042661f/Documents/megaplan/megaplan/execution.py
     301 /Users/user_c042661f/Documents/megaplan/megaplan/execution_timeout.py
    4412 total
[rerun: b1]
```

> AGENT

Now let me read the execution.py file with specific sections:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execution.py",
  "offset": 1,
  "limit": 200
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
101	
102	def _snapshot_task_statuses(tasks: list[dict[str, Any]]) -> dict[str, str]:
103	    return {
104	        task["id"]: str(task.get("status", ""))
105	        for task in tasks
106	        if isinstance(task, dict) and isinstance(task.get("id"), str)
107	    }
108	
109	
110	def _append_execute_reconciliation_advisories(
111	    *,
112	    before_statuses: dict[str, str],
113	    tasks_by_id: dict[str, dict[str, Any]],
114	    issues: list[str],
115	) -> None:
116	    for task_id, before_status in before_statuses.items():
117	        after_status = str(tasks_by_id.get(task_id, {}).get("status", ""))
118	        if before_status not in {"done", "skipped"} or after_status == before_status:
119	            continue
120	        issues.append(
121	            f"Advisory: task {task_id} was {before_status!r} on disk before merge but structured output set it to {after_status!r}. Structured output remains authoritative."
122	        )
123	
124	
125	def _stable_unique_strings(values: list[str]) -> list[str]:
126	    seen: set[str] = set()
127	    ordered: list[str] = []
128	    for value in values:
129	        if value in seen:
130	            continue
131	        seen.add(value)
132	        ordered.append(value)
133	    return ordered
134	
135	
136	def _build_aggregate_execution_payload(
137	    batch_payloads: list[dict[str, Any]],
138	    *,
139	    completed_batches: int,
140	    total_batches: int,
141	) -> dict[str, Any]:
142	    outputs = [
143	        f"Batch {index + 1}: {payload.get('output', '')}".strip()
144	        for index, payload in enumerate(batch_payloads)
145	    ]
146	    files_changed: list[str] = []
147	    commands_run: list[str] = []
148	    deviations: list[str] = []
149	    task_updates: list[dict[str, Any]] = []
150	    sense_check_acknowledgments: list[dict[str, Any]] = []
151	    for payload in batch_payloads:
152	        files_changed.extend(
153	            [path for path in payload.get("files_changed", []) if isinstance(path, str)]
154	        )
155	        commands_run.extend(
156	            [
157	                command
158	                for command in payload.get("commands_run", [])
159	                if isinstance(command, str)
160	            ]
161	        )
162	        deviations.extend(
163	            [issue for issue in payload.get("deviations", []) if isinstance(issue, str)]
164	        )
165	        task_updates.extend(
166	            [item for item in payload.get("task_updates", []) if isinstance(item, dict)]
167	        )
168	        sense_check_acknowledgments.extend(
169	            [
170	                item
171	                for item in payload.get("sense_check_acknowledgments", [])
172	                if isinstance(item, dict)
173	            ]
174	        )
175	    output = (
176	        f"Aggregated execute batches: completed {completed_batches}/{total_batches}."
177	    )
178	    if outputs:
179	        output = output + "\n" + "\n".join(outputs)
180	    return {
181	        "output": output,
182	        "files_changed": _stable_unique_strings(files_changed),
183	        "commands_run": _stable_unique_strings(commands_run),
184	        "deviations": deviations,
185	        "task_updates": task_updates,
186	        "sense_check_acknowledgments": sense_check_acknowledgments,
187	    }
188	
189	
190	def _active_sense_check_ids(
191	    finalize_data: dict[str, Any], active_task_ids: set[str]
192	) -> list[str]:
193	    return [
194	        sense_check["id"]
195	        for sense_check in finalize_data.get("sense_checks", [])
196	        if isinstance(sense_check, dict)
197	        and isinstance(sense_check.get("id"), str)
198	        and sense_check.get("task_id") in active_task_ids
199	    ]
200
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execution.py",
  "offset": 130,
  "limit": 130
}
```

> TOOL

tool_result Read
```
130	            continue
131	        seen.add(value)
132	        ordered.append(value)
133	    return ordered
134	
135	
136	def _build_aggregate_execution_payload(
137	    batch_payloads: list[dict[str, Any]],
138	    *,
139	    completed_batches: int,
140	    total_batches: int,
141	) -> dict[str, Any]:
142	    outputs = [
143	        f"Batch {index + 1}: {payload.get('output', '')}".strip()
144	        for index, payload in enumerate(batch_payloads)
145	    ]
146	    files_changed: list[str] = []
147	    commands_run: list[str] = []
148	    deviations: list[str] = []
149	    task_updates: list[dict[str, Any]] = []
150	    sense_check_acknowledgments: list[dict[str, Any]] = []
151	    for payload in batch_payloads:
152	        files_changed.extend(
153	            [path for path in payload.get("files_changed", []) if isinstance(path, str)]
154	        )
155	        commands_run.extend(
156	            [
157	                command
158	                for command in payload.get("commands_run", [])
159	                if isinstance(command, str)
160	            ]
161	        )
162	        deviations.extend(
163	            [issue for issue in payload.get("deviations", []) if isinstance(issue, str)]
164	        )
165	        task_updates.extend(
166	            [item for item in payload.get("task_updates", []) if isinstance(item, dict)]
167	        )
168	        sense_check_acknowledgments.extend(
169	            [
170	                item
171	                for item in payload.get("sense_check_acknowledgments", [])
172	                if isinstance(item, dict)
173	            ]
174	        )
175	    output = (
176	        f"Aggregated execute batches: completed {completed_batches}/{total_batches}."
177	    )
178	    if outputs:
179	        output = output + "\n" + "\n".join(outputs)
180	    return {
181	        "output": output,
182	        "files_changed": _stable_unique_strings(files_changed),
183	        "commands_run": _stable_unique_strings(commands_run),
184	        "deviations": deviations,
185	        "task_updates": task_updates,
186	        "sense_check_acknowledgments": sense_check_acknowledgments,
187	    }
188	
189	
190	def _active_sense_check_ids(
191	    finalize_data: dict[str, Any], active_task_ids: set[str]
192	) -> list[str]:
193	    return [
194	        sense_check["id"]
195	        for sense_check in finalize_data.get("sense_checks", [])
196	        if isinstance(sense_check, dict)
197	        and isinstance(sense_check.get("id"), str)
198	        and sense_check.get("task_id") in active_task_ids
199	    ]
200	
201	
202	def _count_execute_tracking(
203	    finalize_data: dict[str, Any],
204	    *,
205	    active_task_ids: set[str],
206	    active_sense_check_ids: set[str],
207	) -> tuple[int, int, int, int]:
208	    tracked_tasks = sum(
209	        1
210	        for task in finalize_data.get("tasks", [])
211	        if task.get("id") in active_task_ids
212	        and task.get("status") in {"done", "skipped"}
213	    )
214	    acknowledged_checks = sum(
215	        1
216	        for sense_check in finalize_data.get("sense_checks", [])
217	        if sense_check.get("id") in active_sense_check_ids
218	        and str(sense_check.get("executor_note", "")).strip()
219	    )
220	    return (
221	        tracked_tasks,
222	        len(active_task_ids),
223	        acknowledged_checks,
224	        len(active_sense_check_ids),
225	    )
226	
227	
228	def build_blocking_reasons(
229	    *,
230	    tracked_tasks: int,
231	    total_tasks: int,
232	    acknowledged_checks: int,
233	    total_checks: int,
234	    missing_task_evidence: list[str],
235	    timeout_reason: str | None = None,
236	) -> list[str]:
237	    reasons: list[str] = []
238	    if tracked_tasks < total_tasks:
239	        reasons.append(
240	            f"{total_tasks - tracked_tasks}/{total_tasks} tasks have no executor update"
241	        )
242	    if acknowledged_checks < total_checks:
243	        reasons.append(
244	            f"{total_checks - acknowledged_checks}/{total_checks} sense checks have no executor acknowledgment"
245	        )
246	    if missing_task_evidence:
247	        reasons.append(
248	            "done tasks missing both files_changed and commands_run: "
249	            + ", ".join(missing_task_evidence)
250	        )
251	    if timeout_reason is not None:
252	        reasons.append(timeout_reason)
253	    return reasons
254	
255	
256	def _merge_batch_results(
257	    *,
258	    finalize_data: dict[str, Any],
259	    payload: dict[str, Any],
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execution.py",
  "offset": 240,
  "limit": 100
}
```

> TOOL

tool_result Read
```
240	            f"{total_tasks - tracked_tasks}/{total_tasks} tasks have no executor update"
241	        )
242	    if acknowledged_checks < total_checks:
243	        reasons.append(
244	            f"{total_checks - acknowledged_checks}/{total_checks} sense checks have no executor acknowledgment"
245	        )
246	    if missing_task_evidence:
247	        reasons.append(
248	            "done tasks missing both files_changed and commands_run: "
249	            + ", ".join(missing_task_evidence)
250	        )
251	    if timeout_reason is not None:
252	        reasons.append(timeout_reason)
253	    return reasons
254	
255	
256	def _merge_batch_results(
257	    *,
258	    finalize_data: dict[str, Any],
259	    payload: dict[str, Any],
260	    batch_task_ids: list[str],
261	    batch_sense_check_ids: list[str],
262	    issues: list[str],
263	) -> tuple[int, int, int, int]:
264	    batch_task_id_set = set(batch_task_ids)
265	    batch_sense_check_id_set = set(batch_sense_check_ids)
266	    pre_merge_statuses = _snapshot_task_statuses(
267	        [
268	            task
269	            for task in finalize_data.get("tasks", [])
270	            if task.get("id") in batch_task_id_set
271	        ]
272	    )
273	    # Accept task_updates for ANY valid task, not just the current batch.
274	    # Models often complete multiple batches' worth of work in one pass —
275	    # rejecting the extra work as "unknown task_id" wastes correct results.
276	    all_tasks_by_id = {
277	        task["id"]: task
278	        for task in finalize_data.get("tasks", [])
279	        if isinstance(task, dict) and isinstance(task.get("id"), str)
280	    }
281	    merged_count, _ = _validate_and_merge_batch(
282	        payload.get("task_updates"),
283	        required_fields=(
284	            "task_id",
285	            "status",
286	            "executor_notes",
287	            "files_changed",
288	            "commands_run",
289	        ),
290	        targets_by_id=all_tasks_by_id,
291	        id_field="task_id",
292	        merge_fields=("status", "executor_notes", "files_changed", "commands_run"),
293	        issues=issues,
294	        validation_label="task_updates",
295	        merge_label="task_update",
296	        # Don't flag incomplete based on all tasks — check batch coverage below
297	        incomplete_message=None,
298	        enum_fields={"status": {"done", "skipped", "completed"}},
299	        nonempty_fields={"executor_notes"},
300	        array_fields=("files_changed", "commands_run"),
301	    )
302	    # Check batch-specific coverage: how many of THIS batch's tasks got updates?
303	    total_batch_tasks = len(batch_task_id_set)
304	    batch_merged = sum(
305	        1
306	        for tid in batch_task_id_set
307	        if all_tasks_by_id.get(tid, {}).get("status") in ("done", "skipped")
308	    )
309	    if batch_merged < total_batch_tasks:
310	        issues.append(
311	            f"{total_batch_tasks - batch_merged}/{total_batch_tasks} batch tasks have no executor update — tracking is incomplete."
312	        )
313	    # Same for sense checks — accept any valid sense check ID.
314	    all_sense_checks_by_id = {
315	        sense_check["id"]: sense_check
316	        for sense_check in finalize_data.get("sense_checks", [])
317	        if isinstance(sense_check, dict) and isinstance(sense_check.get("id"), str)
318	    }
319	    acknowledged_count, _ = _validate_and_merge_batch(
320	        payload.get("sense_check_acknowledgments"),
321	        required_fields=("sense_check_id", "executor_note"),
322	        targets_by_id=all_sense_checks_by_id,
323	        id_field="sense_check_id",
324	        merge_fields=("executor_note",),
325	        issues=issues,
326	        validation_label="sense_check_acknowledgments",
327	        merge_label="sense_check_acknowledgment",
328	        incomplete_message=None,
329	        nonempty_fields={"executor_note"},
330	    )
331	    total_batch_checks = len(batch_sense_check_id_set)
332	    batch_acknowledged = sum(
333	        1
334	        for sid in batch_sense_check_id_set
335	        if all_sense_checks_by_id.get(sid, {}).get("executor_note")
336	    )
337	    if batch_acknowledged < total_batch_checks:
338	        issues.append(
339	            f"{total_batch_checks - batch_acknowledged}/{total_batch_checks} batch sense checks have no executor acknowledgment — tracking is incomplete."
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execution.py",
  "offset": 340,
  "limit": 120
}
```

> TOOL

tool_result Read
```
340	        )
341	    _append_execute_reconciliation_advisories(
342	        before_statuses=pre_merge_statuses,
343	        tasks_by_id=all_tasks_by_id,
344	        issues=issues,
345	    )
346	    return merged_count, total_batch_tasks, acknowledged_count, total_batch_checks
347	
348	
349	def _run_and_merge_batch(
350	    *,
351	    root: Path,
352	    plan_dir: Path,
353	    state: PlanState,
354	    args: argparse.Namespace,
355	    agent: str,
356	    mode: str,
357	    refreshed: bool,
358	    model: str | None = None,
359	    prompt_override: str | None,
360	    batch_task_ids: list[str],
361	    batch_sense_check_ids: list[str],
362	    finalize_data: dict[str, Any],
363	    batch_number: int,
364	    batches_total: int,
365	    quality_config: dict[str, Any],
366	    capture_git_status_snapshot_fn: Callable[
367	        [Path], tuple[dict[str, str], str | None]
368	    ] = _capture_git_status_snapshot,
369	) -> BatchResult:
370	    project_dir = Path(state["config"]["project_dir"])
371	    before_snapshot, before_error = capture_git_status_snapshot_fn(project_dir)
372	    before_line_counts = capture_before_line_counts(project_dir, before_snapshot.keys())
373	    worker, agent, mode, refreshed = worker_module.run_step_with_worker(
374	        "execute",
375	        state,
376	        plan_dir,
377	        args,
378	        root=root,
379	        resolved=(agent, mode, refreshed, model),
380	        prompt_override=prompt_override,
381	    )
382	    payload = dict(worker.payload)
383	    deviations = list(payload.get("deviations", []))
384	    batch_task_id_set = set(batch_task_ids)
385	    deviations.extend(
386	        _observe_git_changes(
387	            project_dir=project_dir,
388	            payload=payload,
389	            before_snapshot=before_snapshot,
390	            before_error=before_error,
391	            batch_number=batch_number,
392	            batches_total=batches_total,
393	            capture_git_status_snapshot_fn=capture_git_status_snapshot_fn,
394	        )
395	    )
396	    deviations.extend(
397	        _collect_quality_deviations(
398	            project_dir=project_dir,
399	            before_snapshot=before_snapshot,
400	            before_line_counts=before_line_counts,
401	            quality_config=quality_config,
402	            capture_git_status_snapshot_fn=capture_git_status_snapshot_fn,
403	        )
404	    )
405	    merged_count, total_batch_tasks, acknowledged_count, total_batch_checks = (
406	        _merge_batch_results(
407	            finalize_data=finalize_data,
408	            payload=payload,
409	            batch_task_ids=batch_task_ids,
410	            batch_sense_check_ids=batch_sense_check_ids,
411	            issues=deviations,
412	        )
413	    )
414	    missing_task_evidence = _check_done_task_evidence(
415	        finalize_data.get("tasks", []),
416	        issues=deviations,
417	        should_classify=lambda task: task.get("id") in batch_task_id_set,
418	        has_evidence=lambda task: bool(task.get("files_changed")),
419	        has_advisory_evidence=lambda task: bool(task.get("commands_run")),
420	        missing_message="Done tasks missing both files_changed and commands_run: ",
421	        advisory_message="Advisory: done tasks rely on commands_run without files_changed (FLAG-006 softening): ",
422	    )
423	    execution_audit = validate_execution_evidence(finalize_data, project_dir)
424	    if execution_audit["skipped"]:
425	        deviations.append(f"Advisory audit skip: {execution_audit['reason']}")
426	    for finding in execution_audit["findings"]:
427	        deviations.append(f"Advisory audit finding: {finding}")
428	    payload["deviations"] = deviations
429	    atomic_write_json(batch_artifact_path(plan_dir, batch_number), payload)
430	    atomic_write_json(plan_dir / "execution_audit.json", execution_audit)
431	    atomic_write_json(plan_dir / "finalize.json", finalize_data)
432	    atomic_write_text(
433	        plan_dir / "final.md", render_final_md(finalize_data, phase="execute")
434	    )
435	    return BatchResult(
436	        worker=worker,
437	        agent=agent,
438	        mode=mode,
439	        refreshed=refreshed,
440	        payload=payload,
441	        batch_number=batch_number,
442	        batch_task_ids=list(batch_task_ids),
443	        batch_sense_check_ids=list(batch_sense_check_ids),
444	        merged_task_count=merged_count,
445	        total_task_count=total_batch_tasks,
446	        acknowledged_sense_check_count=acknowledged_count,
447	        total_sense_check_count=total_batch_checks,
448	        missing_task_evidence=missing_task_evidence,
449	        execution_audit=execution_audit,
450	        finalize_hash=sha256_file(plan_dir / "finalize.json"),
451	    )
452	
453	
454	def _append_trace_output(plan_dir: Path, trace_output: str | None) -> bool:
455	    if trace_output is None:
456	        return False
457	    trace_path = plan_dir / "execution_trace.jsonl"
458	    existing_trace = (
459	        trace_path.read_text(encoding="utf-8") if trace_path.exists() else ""
```

> AGENT

Now let me read the handlers.py file in sections:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 280,
  "limit": 150
}
```

> TOOL

tool_result Read
```
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
320	    *,
321	    plan_dir: Path,
322	    state: PlanState,
323	    step: str,
324	    iteration: int,
325	    worker: WorkerResult,
326	    code: str,
327	    message: str,
328	) -> None:
329	    error = CliError(code, message, valid_next=infer_next_steps(state), extra={"raw_output": worker.raw_output})
330	    record_step_failure(plan_dir, state, step=step, iteration=iteration, error=error, duration_ms=worker.duration_ms)
331	    raise error
332	
333	
334	def _write_json_artifact(plan_dir: Path, filename: str, payload: dict[str, Any]) -> str:
335	    atomic_write_json(plan_dir / filename, payload)
336	    return sha256_file(plan_dir / filename)
337	
338	
339	def _write_plan_version(
340	    *,
341	    plan_dir: Path,
342	    state: PlanState,
343	    step: str,
344	    version: int,
345	    worker: WorkerResult,
346	    plan_text: str,
347	    meta_fields: dict[str, Any],
348	    plan_filename: str | None = None,
349	) -> tuple[str, str, dict[str, Any]]:
350	    resolved_plan_filename = plan_filename or next_plan_artifact_name(plan_dir, version)
351	    meta_filename = (
352	        f"plan_v{version}.meta.json"
353	        if resolved_plan_filename == f"plan_v{version}.md"
354	        else resolved_plan_filename.replace(".md", ".meta.json")
355	    )
356	    structure_warnings = _validate_generated_plan_or_raise(
357	        plan_dir=plan_dir,
358	        state=state,
359	        step=step,
360	        iteration=version,
361	        worker=worker,
362	        plan_text=plan_text,
363	    )
364	    atomic_write_text(plan_dir / resolved_plan_filename, plan_text)
365	    meta = {
366	        "version": version,
367	        "timestamp": now_utc(),
368	        "hash": sha256_text(plan_text),
369	        **meta_fields,
370	        "structure_warnings": structure_warnings,
371	    }
372	    atomic_write_json(plan_dir / meta_filename, meta)
373	    return resolved_plan_filename, meta_filename, meta
374	
375	
376	def _write_finalize_artifacts(plan_dir: Path, payload: dict[str, Any], state: PlanState) -> str:
377	    baseline = _capture_test_baseline(Path(state["config"]["project_dir"]), state.get("config", {}))
378	    payload.update(baseline)
379	    _ensure_verification_task(payload, state)
380	    _reconcile_validation_after_mutation(payload)
381	    atomic_write_json(plan_dir / "finalize.json", payload)
382	    atomic_write_json(plan_dir / "finalize_snapshot.json", payload)
383	    atomic_write_text(plan_dir / "final.md", render_final_md(payload))
384	    return sha256_file(plan_dir / "finalize.json")
385	
386	
387	def _reconcile_validation_after_mutation(payload: dict[str, Any]) -> None:
388	    """Ensure validation block is consistent with the (possibly mutated) task list.
389	
390	    After _ensure_verification_task() may have appended a task, update the
391	    validation block so orphan_tasks includes any handler-injected tasks.
392	    """
393	    validation = payload.get("validation")
394	    if not validation or not isinstance(validation, dict):
395	        return
396	    task_ids = {t["id"] for t in payload.get("tasks", []) if isinstance(t, dict)}
397	    covered_ids: set[str] = set()
398	    for entry in validation.get("plan_steps_covered", []):
399	        if isinstance(entry, dict):
400	            for tid in entry.get("finalize_task_ids", []):
401	                covered_ids.add(tid)
402	    orphan_ids = set(validation.get("orphan_tasks", []))
403	    for tid in task_ids:
404	        if tid not in covered_ids and tid not in orphan_ids:
405	            orphan_ids.add(tid)
406	    validation["orphan_tasks"] = sorted(orphan_ids)
407	
408	
409	def _validate_finalize_payload(plan_dir: Path, state: PlanState, worker: WorkerResult) -> None:
410	    payload = worker.payload
411	
412	    def _reject(message: str) -> None:
413	        _raise_step_validation_error(
414	            plan_dir=plan_dir, state=state, step="finalize",
415	            iteration=state["iteration"], worker=worker,
416	            code="invalid_finalize", message=message,
417	        )
418	
419	    tasks = payload.get("tasks")
420	    if not isinstance(tasks, list) or not tasks:
421	        _reject("Finalize output must include a non-empty `tasks` list.")
422	    if not isinstance(payload.get("sense_checks"), list):
423	        _reject("Finalize output must include a `sense_checks` list.")
424	    if not isinstance(payload.get("watch_items"), list):
425	        _reject("Finalize output must include a `watch_items` list.")
426	    for index, task in enumerate(tasks, start=1):
427	        tid = task.get("id", index) if isinstance(task, dict) else index
428	        if not isinstance(task, dict):
429	            _reject(f"Finalize task {index} must be an object.")
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 370,
  "limit": 150
}
```

> TOOL

tool_result Read
```
370	        "structure_warnings": structure_warnings,
371	    }
372	    atomic_write_json(plan_dir / meta_filename, meta)
373	    return resolved_plan_filename, meta_filename, meta
374	
375	
376	def _write_finalize_artifacts(plan_dir: Path, payload: dict[str, Any], state: PlanState) -> str:
377	    baseline = _capture_test_baseline(Path(state["config"]["project_dir"]), state.get("config", {}))
378	    payload.update(baseline)
379	    _ensure_verification_task(payload, state)
380	    _reconcile_validation_after_mutation(payload)
381	    atomic_write_json(plan_dir / "finalize.json", payload)
382	    atomic_write_json(plan_dir / "finalize_snapshot.json", payload)
383	    atomic_write_text(plan_dir / "final.md", render_final_md(payload))
384	    return sha256_file(plan_dir / "finalize.json")
385	
386	
387	def _reconcile_validation_after_mutation(payload: dict[str, Any]) -> None:
388	    """Ensure validation block is consistent with the (possibly mutated) task list.
389	
390	    After _ensure_verification_task() may have appended a task, update the
391	    validation block so orphan_tasks includes any handler-injected tasks.
392	    """
393	    validation = payload.get("validation")
394	    if not validation or not isinstance(validation, dict):
395	        return
396	    task_ids = {t["id"] for t in payload.get("tasks", []) if isinstance(t, dict)}
397	    covered_ids: set[str] = set()
398	    for entry in validation.get("plan_steps_covered", []):
399	        if isinstance(entry, dict):
400	            for tid in entry.get("finalize_task_ids", []):
401	                covered_ids.add(tid)
402	    orphan_ids = set(validation.get("orphan_tasks", []))
403	    for tid in task_ids:
404	        if tid not in covered_ids and tid not in orphan_ids:
405	            orphan_ids.add(tid)
406	    validation["orphan_tasks"] = sorted(orphan_ids)
407	
408	
409	def _validate_finalize_payload(plan_dir: Path, state: PlanState, worker: WorkerResult) -> None:
410	    payload = worker.payload
411	
412	    def _reject(message: str) -> None:
413	        _raise_step_validation_error(
414	            plan_dir=plan_dir, state=state, step="finalize",
415	            iteration=state["iteration"], worker=worker,
416	            code="invalid_finalize", message=message,
417	        )
418	
419	    tasks = payload.get("tasks")
420	    if not isinstance(tasks, list) or not tasks:
421	        _reject("Finalize output must include a non-empty `tasks` list.")
422	    if not isinstance(payload.get("sense_checks"), list):
423	        _reject("Finalize output must include a `sense_checks` list.")
424	    if not isinstance(payload.get("watch_items"), list):
425	        _reject("Finalize output must include a `watch_items` list.")
426	    for index, task in enumerate(tasks, start=1):
427	        tid = task.get("id", index) if isinstance(task, dict) else index
428	        if not isinstance(task, dict):
429	            _reject(f"Finalize task {index} must be an object.")
430	        if not isinstance(task.get("id"), str) or not task["id"].strip():
431	            _reject(f"Finalize task {index} is missing a non-empty `id`.")
432	        if not isinstance(task.get("description"), str) or not task["description"].strip():
433	            _reject(f"Finalize task {tid} is missing a non-empty `description`.")
434	        if task.get("status") != "pending":
435	            _reject(f"Finalize task {tid} must start with status `pending`.")
436	
437	
438	def _build_gate_signals_artifact(
439	    plan_dir: Path,
440	    state: PlanState,
441	    *,
442	    iteration: int,
443	    root: Path,
444	) -> tuple[dict[str, Any], str, dict[str, Any]]:
445	    gate_signals = build_gate_signals(plan_dir, state, root=root)
446	    gate_checks = run_gate_checks(plan_dir, state, command_lookup=find_command)
447	    signals_artifact = {
448	        "robustness": gate_signals["robustness"],
449	        "signals": gate_signals["signals"],
450	        "warnings": gate_signals.get("warnings", []),
451	        "criteria_check": gate_checks["criteria_check"],
452	        "preflight_results": gate_checks["preflight_results"],
453	        "unresolved_flags": gate_checks["unresolved_flags"],
454	    }
455	    signals_filename = f"gate_signals_v{iteration}.json"
456	    atomic_write_json(plan_dir / signals_filename, signals_artifact)
457	    return gate_signals, signals_filename, signals_artifact
458	
459	
460	def _record_gate_debt_entries(
461	    root: Path,
462	    state: PlanState,
463	    gate_summary: dict[str, Any],
464	    worker_payload: dict[str, Any],
465	) -> int:
466	    if gate_summary["recommendation"] != "PROCEED":
467	        return 0
468	
469	    raw_tradeoffs = worker_payload.get("accepted_tradeoffs", [])
470	    accepted_tradeoffs = [
471	        item
472	        for item in raw_tradeoffs
473	        if isinstance(item, dict)
474	        and isinstance(item.get("flag_id"), str)
475	        and isinstance(item.get("concern"), str)
476	    ] if isinstance(raw_tradeoffs, list) else []
477	    has_explicit_resolutions = any(
478	        isinstance(item, dict) for item in gate_summary.get("flag_resolutions", [])
479	    )
480	    debt_registry = load_debt_registry(root)
481	    debt_entries_added = 0
482	    if accepted_tradeoffs:
483	        for tradeoff in accepted_tradeoffs:
484	            subsystem_value = tradeoff.get("subsystem")
485	            subsystem = (
486	                subsystem_value
487	                if isinstance(subsystem_value, str) and subsystem_value.strip()
488	                else extract_subsystem_tag(tradeoff["concern"])
489	            )
490	            add_or_increment_debt(
491	                debt_registry,
492	                subsystem=subsystem,
493	                concern=tradeoff["concern"],
494	                flag_ids=[tradeoff["flag_id"]],
495	                plan_id=state["name"],
496	            )
497	            debt_entries_added += 1
498	    elif not has_explicit_resolutions:
499	        for flag in gate_summary["unresolved_flags"]:
500	            if not isinstance(flag, dict):
501	                continue
502	            flag_id = flag.get("id")
503	            concern = flag.get("concern")
504	            if not isinstance(flag_id, str) or not isinstance(concern, str):
505	                continue
506	            add_or_increment_debt(
507	                debt_registry,
508	                subsystem=extract_subsystem_tag(concern),
509	                concern=concern,
510	                flag_ids=[flag_id],
511	                plan_id=state["name"],
512	            )
513	            debt_entries_added += 1
514	    if debt_entries_added:
515	        save_debt_registry(root, debt_registry)
516	    return debt_entries_added
517	
518	
519	def _resolve_revise_transition(state: PlanState) -> tuple[bool, Any]:
```

> AGENT

Now let me read the cli.py file for the _build_status_payload function:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"_build_status_payload\" /Users/user_c042661f/Documents/megaplan/megaplan/cli.py"
}
```

> TOOL

tool_result Bash
```
282:def _build_status_payload(plan_dir: Path, state: dict[str, Any]) -> StepResponse:
343:    return _build_status_payload(plan_dir, state)
[rerun: b2]
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/cli.py",
  "offset": 280,
  "limit": 100
}
```

> TOOL

tool_result Read
```
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
```

> AGENT

Now let me search for _check_done_task_evidence to find its location:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"_check_done_task_evidence\" /Users/user_c042661f/Documents/megaplan/megaplan/execution_quality.py"
}
```

> TOOL

tool_result Bash
```
12:def _check_done_task_evidence(
[rerun: b3]
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execution_quality.py",
  "offset": 1,
  "limit": 100
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
9	from megaplan.quality import run_quality_checks
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
```

> AGENT

Perfect! Now I have all the information. Let me compile a comprehensive report with exact line numbers:

## Summary Report

Here are the requested files with their exact function locations:

### 1. **megaplan/execution.py**
- **`_build_aggregate_execution_payload`**: Lines 136-187
- **`_merge_batch_results`**: Lines 256-346
- **`_run_and_merge_batch`**: Lines 349-451
- **`_check_done_task_evidence`**: Located in `megaplan/execution_quality.py` at lines 12-37 (imported into execution.py at line 32)

### 2. **megaplan/evaluation.py**
- **`validate_execution_evidence`**: Lines 123-243

### 3. **megaplan/execution_timeout.py**
- **`_reset_timeout_invalid_tasks`**: Lines 41-101
- **`_merge_timeout_checkpoint`**: Lines 110-160
- **`_recover_execute_timeout`**: Lines 163-301

### 4. **megaplan/handlers.py**
- **`_build_status_payload`**: NOT FOUND in handlers.py (this function is in cli.py)
- **`_write_finalize_artifacts`**: Lines 376-384

### 5. **megaplan/cli.py**
- **`_build_status_payload`**: Lines 282-338

### Important Note:
There is **no `_build_status_payload` function in handlers.py**. The function exists in `cli.py` at line 282. The handlers.py file does contain related functions like `_write_finalize_artifacts` (line 376) which you requested, and other handler functions, but not a function by that name.

All functions have been located with their precise line numbers. The execution_quality.py file contains `_check_done_task_evidence` which is imported and used in execution.py rather than being defined there.
