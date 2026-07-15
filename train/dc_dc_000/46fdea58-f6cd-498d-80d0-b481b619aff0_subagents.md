> DEVELOPER

Explore the megaplan project at /Users/user_c042661f/Documents/megaplan. I need to understand:

1. Overall file structure (ls the top-level and key subdirectories)
2. The gate/review system - how gates work, how criteria are evaluated, how reviews happen
3. The milestone/step model - data structures for milestones, steps, criteria
4. The YAML schema for plans - what fields exist on milestones/steps/criteria
5. Any existing "verify" or "verif" patterns
6. The CHANGELOG.md current state (just the top few entries)
7. The version number and where it's defined

Focus on: megaplan/*.py files, tests/, any YAML schema definitions, CHANGELOG.md. Skip .megaplan/ directory and idea-*.txt files.

Be thorough - read key files in full, especially anything related to gates, criteria, review, and the data model.

> AGENT

I'll explore the megaplan project systematically. Let me start by understanding the overall structure and then dive into the key areas you mentioned.

> TOOL

tool_use Bash
```json
{
  "command": "ls -la"
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

Now let me explore the megaplan directory structure:

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

Let me check the tests directory structure and look at the CHANGELOG:

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/tests/"
}
```

> TOOL

tool_result Bash
```
total 1088
drwxr-xr-x  24 user_c042661f  staff     768 Apr 15 11:10 .
drwxr-xr-x  31 user_c042661f  staff     992 Apr 15 12:24 ..
-rw-r--r--   1 user_c042661f  staff       0 Mar 20 17:09 __init__.py
drwxr-xr-x@ 83 user_c042661f  staff    2656 Apr 15 11:11 __pycache__
-rw-r--r--   1 user_c042661f  staff   10069 Apr 15 11:10 test_chain.py
-rw-r--r--   1 user_c042661f  staff    2616 Apr 11 04:25 test_checks.py
-rw-r--r--   1 user_c042661f  staff    8500 Apr 11 04:26 test_config.py
-rw-r--r--@  1 user_c042661f  staff    7387 Mar 25 21:08 test_core.py
-rw-r--r--@  1 user_c042661f  staff   16422 Apr 15 10:51 test_doc_mode.py
-rw-r--r--   1 user_c042661f  staff   33147 Mar 31 02:31 test_evaluation.py
-rw-r--r--   1 user_c042661f  staff   19989 Apr 11 04:28 test_handle_review_robustness.py
-rw-r--r--@  1 user_c042661f  staff    2564 Apr  8 00:04 test_io_git_patch.py
-rw-r--r--@  1 user_c042661f  staff   31851 Mar 27 06:02 test_loop.py
-rw-r--r--   1 user_c042661f  staff  215294 Apr 15 06:08 test_megaplan.py
-rw-r--r--@  1 user_c042661f  staff   15313 Apr  8 02:45 test_parallel_critique.py
-rw-r--r--   1 user_c042661f  staff   10994 Apr 11 04:29 test_parallel_review.py
-rw-r--r--   1 user_c042661f  staff   41529 Apr 11 04:29 test_prompts.py
-rw-r--r--   1 user_c042661f  staff    7840 Mar 25 21:40 test_quality.py
-rw-r--r--   1 user_c042661f  staff    3176 Apr 11 04:25 test_review_checks.py
-rw-r--r--   1 user_c042661f  staff    4371 Apr  8 02:04 test_review_mechanical.py
-rw-r--r--   1 user_c042661f  staff   18820 Apr 11 04:29 test_schemas.py
-rw-r--r--@  1 user_c042661f  staff    1386 Mar 29 13:27 test_swe_bench.py
-rw-r--r--@  1 user_c042661f  staff    3978 Apr 10 23:14 test_tiny_robustness.py
-rw-r--r--@  1 user_c042661f  staff   64210 Apr 10 23:14 test_workers.py
[rerun: b3]
```

> AGENT

Now let me read the CHANGELOG, version info, and key files:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/CHANGELOG.md",
  "limit": 100
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
```

> AGENT

Now let me read the pyproject.toml for version info:

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

> AGENT

Good! Now let me read the key schema and data structure files. Let me start with schemas.py:

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

Now let me read the types.py file to understand the data structures:

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

Now let me search for files related to gates, review, and verification patterns:

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan/megaplan -name \"*.py\" | grep -E \"(gate|review|verif)\" | head -20"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/review_checks.py
/Users/user_c042661f/Documents/megaplan/megaplan/review_mechanical.py
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/review.py
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/gate.py
/Users/user_c042661f/Documents/megaplan/megaplan/parallel_review.py
[rerun: b4]
```

> AGENT

Now let me read the gate-related files and look at the handlers and evaluation files for how gates work:

> TOOL

tool_use Bash
```json
{
  "command": "wc -l /Users/user_c042661f/Documents/megaplan/megaplan/handlers.py /Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py"
}
```

> TOOL

tool_result Bash
```
2022 /Users/user_c042661f/Documents/megaplan/megaplan/handlers.py
     711 /Users/user_c042661f/Documents/megaplan/megaplan/evaluation.py
    2733 total
[rerun: b5]
```

> AGENT

Let me grep for gate-related functions and check the evaluation.py file:

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

> AGENT

Now let me look at the handlers file to understand how gates are executed. Let me search for key gate handler functions:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def.*gate\\|def.*review\\|def.*verif\\|def.*check_flag\" /Users/user_c042661f/Documents/megaplan/megaplan/handlers.py | head -40"
}
```

> TOOL

tool_result Bash
```
129:def _build_review_blocked_message(
150:def _is_substantive_reviewer_verdict(text: str) -> bool:
216:def _build_review_prompt_override(
231:def _build_gate_prompt_override(
438:def _build_gate_signals_artifact(
460:def _record_gate_debt_entries(
542:def _gate_response_fields(state: PlanState, gate_summary: dict[str, Any], debt_entries_added: int) -> dict[str, Any]:
590:def _store_last_gate(state: PlanState, gate_summary: dict[str, Any]) -> None:
604:def _apply_gate_outcome(
669:def _merge_gate_worker_attempt(base: WorkerResult, retry: WorkerResult) -> WorkerResult:
683:def _merge_resolution_tradeoffs_into_payload(gate_summary: dict[str, Any], worker_payload: dict[str, Any]) -> None:
1049:def handle_gate(root: Path, args: argparse.Namespace) -> StepResponse:
1171:def _ensure_verification_task(payload: dict, state: dict) -> None:
1421:def _merge_review_verdicts(
1469:def _resolve_review_outcome(
1523:def _synthesize_review_rework_items(checks: list[dict[str, Any]]) -> list[dict[str, str]]:
1529:        check_def = review_checks.get_check_by_id(check_id)
1542:            # empty status means the model failed to classify, so we keep the check's default_severity gate as
1576:def handle_review(root: Path, args: argparse.Namespace) -> StepResponse:
[rerun: b6]
```

> AGENT

Let me read the handle_gate function and related gate processing code:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 1049,
  "limit": 200
}
```

> TOOL

tool_result Read
```
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
1061	            resolved=resolved,
1062	        )
1063	        gate_payload = worker.payload
1064	        guidance = build_orchestrator_guidance(
1065	            gate_payload=gate_payload,
1066	            signals=signals_artifact["signals"],
1067	            preflight_passed=all(signals_artifact["preflight_results"].values()),
1068	            preflight_results=signals_artifact["preflight_results"],
1069	            robustness=signals_artifact.get("robustness", "standard"),
1070	            plan_name=state["name"],
1071	        )
1072	        gate_summary = build_gate_artifact(
1073	            signals_artifact,
1074	            gate_payload,
1075	            override_forced=False,
1076	            orchestrator_guidance=guidance,
1077	        )
1078	        gate_summary["reprompted"] = False
1079	        if len(state["meta"].get("weighted_scores", [])) < iteration:
1080	            _append_to_meta(state, "weighted_scores", gate_signals["signals"]["weighted_score"])
1081	        result, next_step, summary, blocking_unresolved_ids = _apply_gate_outcome(
1082	            state,
1083	            gate_summary,
1084	            robustness=gate_signals["robustness"],
1085	            plan_dir=plan_dir,
1086	        )
1087	        if blocking_unresolved_ids:
1088	            reprompt_prompt = _build_gate_prompt_override(
1089	                agent,
1090	                state,
1091	                plan_dir,
1092	                root=root,
1093	                missing_flag_ids=blocking_unresolved_ids,
1094	            )
1095	            retry_worker, _, _, _ = _run_worker(
1096	                "gate",
1097	                state,
1098	                plan_dir,
1099	                args,
1100	                root=root,
1101	                resolved=resolved,
1102	                prompt_override=reprompt_prompt,
1103	            )
1104	            worker = _merge_gate_worker_attempt(worker, retry_worker)
1105	            gate_payload = worker.payload
1106	            guidance = build_orchestrator_guidance(
1107	                gate_payload=gate_payload,
1108	                signals=signals_artifact["signals"],
1109	                preflight_passed=all(signals_artifact["preflight_results"].values()),
1110	                preflight_results=signals_artifact["preflight_results"],
1111	                robustness=signals_artifact.get("robustness", "standard"),
1112	                plan_name=state["name"],
1113	            )
1114	            gate_summary = build_gate_artifact(
1115	                signals_artifact,
1116	                gate_payload,
1117	                override_forced=False,
1118	                orchestrator_guidance=guidance,
1119	            )
1120	            gate_summary["reprompted"] = True
1121	            result, next_step, summary, blocking_unresolved_ids = _apply_gate_outcome(
1122	                state,
1123	                gate_summary,
1124	                robustness=gate_signals["robustness"],
1125	                plan_dir=plan_dir,
1126	            )
1127	            if blocking_unresolved_ids:
1128	                gate_summary["recommendation"] = "ITERATE"
1129	                gate_summary["passed"] = False
1130	                gate_summary["rationale"] = (
1131	                    f"{gate_summary['rationale']} "
1132	                    f"[Auto-downgraded from PROCEED: {len(blocking_unresolved_ids)} "
1133	                    "blocking flag(s) not resolved after reprompt]"
1134	                )
1135	                gate_summary["orchestrator_guidance"] = (
1136	                    "Gate auto-downgraded to ITERATE because blocking flags remained "
1137	                    "unresolved after reprompt. Revise the plan."
1138	                )
1139	                result = "blocked"
1140	                next_step = "revise"
1141	                summary = f"Gate recommendation {gate_summary['recommendation']}: {gate_summary['rationale']}"
1142	        _merge_resolution_tradeoffs_into_payload(gate_summary, worker.payload)
1143	        gate_hash = _write_json_artifact(plan_dir, "gate.json", gate_summary)
1144	        debt_entries_added = 0
1145	        if gate_summary["recommendation"] == "PROCEED":
1146	            debt_entries_added = _record_gate_debt_entries(root, state, gate_summary, worker.payload)
1147	        # Store last_gate AFTER _apply_gate_outcome — the outcome may override
1148	        # the recommendation (e.g. PROCEED → ITERATE when flags are unresolved).
1149	        _store_last_gate(state, gate_summary)
1150	        return _finish_step(
1151	            plan_dir,
1152	            state,
1153	            args,
1154	            step="gate",
1155	            worker=worker,
1156	            agent=agent,
1157	            mode=mode,
1158	            refreshed=refreshed,
1159	            summary=summary,
1160	            artifacts=[signals_filename, "gate.json"],
1161	            output_file="gate.json",
1162	            artifact_hash=gate_hash,
1163	            result=result,
1164	            success=gate_summary["recommendation"] != "PROCEED" or gate_summary["passed"],
1165	            next_step=next_step,
1166	            response_fields=_gate_response_fields(state, gate_summary, debt_entries_added),
1167	            history_fields={"recommendation": gate_summary["recommendation"]},
1168	        )
1169	
1170	
1171	def _ensure_verification_task(payload: dict, state: dict) -> None:
1172	    """Ensure the task list ends with a test verification task.
1173	
1174	    If the last task already looks like a verification/test task, leave it.
1175	    Otherwise append one that depends on all other tasks.
1176	    """
1177	    tasks = payload.get("tasks", [])
1178	    if not tasks:
1179	        return
1180	
1181	    # Check if last task is already a verification task
1182	    last_desc = (tasks[-1].get("description") or "").lower()
1183	    test_keywords = ("run test", "run the test", "verify", "verification", "pytest", "test suite", "run existing test")
1184	    has_verification_task = any(kw in last_desc for kw in test_keywords)
1185	
1186	    if not has_verification_task:
1187	        # Build the verification task
1188	        all_ids = [t["id"] for t in tasks]
1189	        next_num = max((int(t["id"].lstrip("T")) for t in tasks if t["id"].startswith("T")), default=0) + 1
1190	        task_id = f"T{next_num}"
1191	
1192	        # Pull specific test IDs from the original prompt if available
1193	        idea = state.get("idea", "") or ""
1194	        notes = "\n".join(state.get("notes", []) or [])
1195	        source_text = idea + "\n" + notes
1196	
1197	        if "FAIL_TO_PASS" in source_text or "test must pass" in source_text.lower() or "verification" in source_text.lower():
1198	            desc = (
1199	                "Run the tests specified in the task description to verify the fix — run the full test file/module, not just individual functions. "
1200	                "Run the project's existing test suite — do NOT create new test files. "
1201	                "If any test fails, read the error, fix the code, and re-run until all tests pass."
1202	            )
1203	        else:
1204	            desc = (
1205	                "Run tests relevant to the changed files to verify correctness and check for regressions — run the full test file/module, not just individual functions. "
1206	                "Find and run the project's existing test suite — do NOT create new test files. "
1207	                "If any test fails, read the error, fix the code, and re-run until all tests pass."
1208	            )
1209	
1210	        verification_task = {
1211	            "id": task_id,
1212	            "description": desc,
1213	            "depends_on": [all_ids[-1]],
1214	            "status": "pending",
1215	            "executor_notes": "",
1216	            "files_changed": [],
1217	            "commands_run": [],
1218	            "evidence_files": [],
1219	            "reviewer_verdict": "",
1220	        }
1221	        tasks.append(verification_task)
1222	
1223	        # Add a sense check for it
1224	        sense_checks = payload.get("sense_checks", [])
1225	        sc_num = max((int(sc["id"].lstrip("SC")) for sc in sense_checks if sc["id"].startswith("SC")), default=0) + 1
1226	        sense_checks.append({
1227	            "id": f"SC{sc_num}",
1228	            "task_id": task_id,
1229	            "question": "Did the verification tests pass? Were any regressions found and fixed?",
1230	            "executor_note": "",
1231	            "verdict": "",
1232	        })
1233	
1234	    failures = payload.get("baseline_test_failures")
1235	    if isinstance(failures, list) and failures:
1236	        tasks[-1]["description"] += (
1237	            f" Note: {len(failures)} tests were already failing before your changes "
1238	            "(see baseline_test_failures in finalize.json) — do not scope-creep into fixing these."
1239	        )
1240	
1241	
1242	def _capture_test_baseline(project_dir: Path, config: dict[str, Any]) -> dict[str, Any]:
1243	    if os.getenv(MOCK_ENV_VAR) == "1":
1244	        return {
1245	            "baseline_test_failures": [],
1246	            "baseline_test_command": "pytest --tb=no -q --no-header",
1247	        }
1248
```

> AGENT

Now let me read more of the gate logic, specifically the _apply_gate_outcome function:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 604,
  "limit": 100
}
```

> TOOL

tool_result Read
```
604	def _apply_gate_outcome(
605	    state: PlanState,
606	    gate_summary: dict[str, Any],
607	    *,
608	    robustness: str,
609	    plan_dir: Path,
610	) -> tuple[str, str, str, list[str]]:
611	    result = "success"
612	    summary = f"Gate recommendation {gate_summary['recommendation']}: {gate_summary['rationale']}"
613	
614	    # Process explicit flag resolutions when the gate recommends PROCEED.
615	    if gate_summary["recommendation"] == "PROCEED":
616	        unresolved = gate_summary.get("unresolved_flags", [])
617	        resolutions = gate_summary.get("flag_resolutions", [])
618	
619	        # Validate each explicit resolution
620	        valid_resolved_ids: set[str] = set()
621	        for res in resolutions:
622	            action = res.get("action", "")
623	            flag_id = res.get("flag_id", "")
624	            if action == "dispute":
625	                evidence = res.get("evidence", "").strip()
626	                if not evidence or is_rubber_stamp(evidence, strict=True):
627	                    continue  # invalid dispute — skip
628	            elif action == "accept_tradeoff":
629	                rationale = res.get("rationale", "").strip()
630	                if not rationale or is_rubber_stamp(rationale, strict=True):
631	                    continue  # invalid tradeoff acceptance — skip
632	            else:
633	                continue  # unknown action — skip
634	            valid_resolved_ids.add(flag_id)
635	
636	        blocking_unresolved = [
637	            f for f in unresolved
638	            if f.get("severity") in ("significant", "likely-significant")
639	            and f.get("status") in FLAG_BLOCKING_STATUSES
640	            and f.get("id") not in valid_resolved_ids
641	        ]
642	        blocking_unresolved_ids = [f.get("id", "") for f in blocking_unresolved if f.get("id")]
643	
644	        # Persist explicit resolutions
645	        if valid_resolved_ids:
646	            update_flags_after_gate(plan_dir, resolutions)
647	
648	        if blocking_unresolved_ids:
649	            return "unresolved_flags", "gate", summary, blocking_unresolved_ids
650	
651	    if gate_summary["recommendation"] == "PROCEED" and gate_summary["passed"]:
652	        state["current_state"] = STATE_GATED
653	        state["meta"].pop("user_approved_gate", None)
654	        return result, "finalize", summary, []
655	    state["current_state"] = STATE_CRITIQUED
656	    if gate_summary["recommendation"] == "PROCEED":
657	        result = "blocked"
658	        summary = "Gate recommended PROCEED, but preflight checks are still blocking execution."
659	        return result, "revise", summary, []
660	    if gate_summary["recommendation"] == "ITERATE":
661	        return result, "revise", summary, []
662	    if gate_summary["recommendation"] == "ESCALATE":
663	        return result, "override add-note", summary, []
664	    result = "unknown_recommendation"
665	    summary = f"Gate returned unknown recommendation '{gate_summary['recommendation']}'; treating as escalation."
666	    return result, "override add-note", summary, []
667	
668	
669	def _merge_gate_worker_attempt(base: WorkerResult, retry: WorkerResult) -> WorkerResult:
670	    base.payload = retry.payload
671	    base.raw_output = "\n\n".join(part for part in [base.raw_output, retry.raw_output] if part)
672	    if base.trace_output or retry.trace_output:
673	        base.trace_output = "\n\n".join(part for part in [base.trace_output, retry.trace_output] if part)
674	    base.duration_ms += retry.duration_ms
675	    base.cost_usd += retry.cost_usd
676	    base.session_id = retry.session_id or base.session_id
677	    base.prompt_tokens += retry.prompt_tokens
678	    base.completion_tokens += retry.completion_tokens
679	    base.total_tokens += retry.total_tokens
680	    return base
681	
682	
683	def _merge_resolution_tradeoffs_into_payload(gate_summary: dict[str, Any], worker_payload: dict[str, Any]) -> None:
684	    raw_tradeoffs = worker_payload.get("accepted_tradeoffs", [])
685	    merged_tradeoffs = list(raw_tradeoffs) if isinstance(raw_tradeoffs, list) else []
686	    existing_ids = {
687	        item.get("flag_id")
688	        for item in merged_tradeoffs
689	        if isinstance(item, dict) and isinstance(item.get("flag_id"), str)
690	    }
691	    unresolved_by_id = {
692	        flag.get("id"): flag
693	        for flag in gate_summary.get("unresolved_flags", [])
694	        if isinstance(flag, dict) and isinstance(flag.get("id"), str)
695	    }
696	    for resolution in gate_summary.get("flag_resolutions", []):
697	        if not isinstance(resolution, dict) or resolution.get("action") != "accept_tradeoff":
698	            continue
699	        flag_id = resolution.get("flag_id")
700	        if not isinstance(flag_id, str) or flag_id in existing_ids:
701	            continue
702	        flag = unresolved_by_id.get(flag_id)
703	        if not isinstance(flag, dict):
```

> AGENT

Let me look at the gate prompt to understand criteria evaluation:

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

Now let me look at review-related files:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/review_checks.py"
}
```

> TOOL

tool_result Read
```
1	"""Review check registry and helpers.
2	
3	This largely mirrors :mod:`megaplan.checks`; the shared helper body is an
4	extraction candidate once critique and review settle on the same abstraction.
5	"""
6	
7	from __future__ import annotations
8	
9	from dataclasses import dataclass
10	from typing import Any, Final
11	
12	
13	@dataclass(frozen=True)
14	class ReviewCheckSpec:
15	    id: str
16	    question: str
17	    guidance: str
18	    category: str
19	    default_severity: str
20	    tier: str
21	
22	
23	REVIEW_CHECKS: Final[tuple[ReviewCheckSpec, ...]] = (
24	    ReviewCheckSpec(
25	        id="coverage",
26	        question="Does the diff cover every concrete failing example, symptom, or 'X should Y' statement in the original issue?",
27	        guidance=(
28	            "List each concrete failing example, symptom, or behavioral requirement in the issue. "
29	            "For each one, cite the diff line that addresses it and flag anything still uncovered. "
30	            "Also watch for: "
31	            "(a) Opt-in vs default: if the issue wants new default behavior but the diff adds a flag, flag it. "
32	            "(b) Accepted-change violations: if the issue accepts a behavior change, flag code that preserves the old behavior anyway. "
33	            "(c) Secondary sentences: treat extra expectations in side phrases as real requirements. "
34	            "Do NOT flag a verification test referenced by the plan that doesn't exist in the repo as a coverage gap. "
35	            "Test files are a task-level no-modify structural constraint already accepted by the gate; if it still matters, downgrade to status: significant. "
36	            "Focus blocking coverage findings on source changes that miss concrete issue symptoms."
37	        ),
38	        category="completeness",
39	        default_severity="likely-significant",
40	        tier="core",
41	    ),
42	    ReviewCheckSpec(
43	        id="placement",
44	        question="Is the fix placed where the bad state originates, or only where the symptom surfaces?",
45	        guidance=(
46	            "Do a backward trace, not just a forward one. Start from the changed code and ask: where is the bad value first introduced? "
47	            "If your fix runs AFTER the bad state already exists, you are papering over a downstream symptom — flag it, even if the symptom from the issue goes away. "
48	            "Then identify at least two distinct code paths by which a user could trigger this bug (e.g., direct function call, alternate entry point, reflection/registry lookup, import-time evaluation). "
49	            "Does your fix block ALL of them, or only the one the issue demonstrates? If only one, flag it. "
50	            "If the issue involves parsing, serialization, or transformation, verify the fix is at the source of the bad representation, not a downstream consumer that compensates for it. "
51	            "Ask: would a maintainer reviewing this PR expect the fix to live here, or somewhere more fundamental?"
52	        ),
53	        category="correctness",
54	        default_severity="likely-significant",
55	        tier="core",
56	    ),
57	    ReviewCheckSpec(
58	        id="adjacent_calls",
59	        question="Do adjacent callers, sibling usage sites, or downstream consumers still exhibit the bug or mishandle the new values?",
60	        guidance=(
61	            "First: look at other code that calls the changed function, uses the same surrounding pattern, or is registered alongside the changed class. "
62	            "For each sibling site, check whether the reported bug would still affect it and flag any adjacent cases left unfixed. "
63	            "Specifically: if the patch adds a new class/handler alongside existing siblings, enumerate every method those siblings override and ask whether ours should override them too. "
64	            "Second: for any value the patch returns or constructs in a new/error path, trace where it flows next. "
65	            "Check whether downstream consumers actually handle that value correctly, and whether any new sentinel or return-value semantics introduce inconsistencies. "
66	            "Flag anything a maintainer would mark as incomplete."
67	        ),
68	        category="completeness",
69	        default_severity="likely-significant",
70	        tier="core",
71	    ),
72	    ReviewCheckSpec(
73	        id="simplicity",
74	        question="Is this the smallest change that would make the issue's reported example work, and does it match how sibling code solves similar problems?",
75	        guidance=(
76	            "First: describe the smallest possible change that would resolve the reported symptom, then compare that baseline against the actual diff. "
77	            "Every extra line in the patch should be justified against a specific requirement from the issue — if it cannot, flag it as unjustified scope. "
78	            "Second: find 2-3 structurally similar classes or functions in the same module. "
79	            "Enumerate the methods, overrides, or conventions they share, then compare the new code against that pattern. "
80	            "If the patch diverges from the neighborhood's conventions, the divergence must be explicitly justified; otherwise flag it. "
81	            "Over-engineered patches (large refactors when a 1-line fix would do, new config options the issue did not request, backward-compat shims against changes the issue explicitly accepted) should be flagged."
82	        ),
83	        category="maintainability",
84	        default_severity="likely-significant",
85	        tier="core",
86	    ),
87	)
88	
89	_CHECK_BY_ID: Final[dict[str, ReviewCheckSpec]] = {check.id: check for check in REVIEW_CHECKS}
90	_CORE_REVIEW_CHECKS: Final[tuple[ReviewCheckSpec, ...]] = tuple(
91	    check for check in REVIEW_CHECKS if check.tier == "core"
92	)
93	# All current review checks are core. The tier field is retained for parity
94	# with `megaplan/checks.py` and future extensibility — if we add narrower
95	# specialized checks later, demote them to "extended" and they will be
96	# excluded from standard/light robustness here.
97	
98	
99	def get_check_ids() -> list[str]:
100	    return [check.id for check in REVIEW_CHECKS]
101	
102	
103	def get_check_by_id(check_id: str) -> ReviewCheckSpec | None:
104	    return _CHECK_BY_ID.get(check_id)
105	
106	
107	def build_check_category_map() -> dict[str, str]:
108	    return {check.id: check.category for check in REVIEW_CHECKS}
109	
110	
111	def checks_for_robustness(robustness: str) -> tuple[ReviewCheckSpec, ...]:
112	    if robustness in {"robust", "superrobust"}:
113	        return REVIEW_CHECKS
114	    if robustness in {"light", "tiny"}:
115	        return ()
116	    return _CORE_REVIEW_CHECKS
117	
118	
119	def build_empty_template(checks: tuple[ReviewCheckSpec, ...] | None = None) -> list[dict[str, Any]]:
120	    active_checks = REVIEW_CHECKS if checks is None else checks
121	    return [
122	        {
123	            "id": check.id,
124	            "question": check.question,
125	            "findings": [],
126	        }
127	        for check in active_checks
128	    ]
129	
130	
131	_MIN_FINDING_DETAIL_LENGTH = 40
132	
133	
134	def _valid_findings(findings: Any) -> bool:
135	    if not isinstance(findings, list) or not findings:
136	        return False
137	    for finding in findings:
138	        if not isinstance(finding, dict):
139	            return False
140	        detail = finding.get("detail")
141	        flagged = finding.get("flagged")
142	        if not isinstance(detail, str) or not detail.strip():
143	            return False
144	        if len(detail.strip()) < _MIN_FINDING_DETAIL_LENGTH:
145	            return False
146	        if not isinstance(flagged, bool):
147	            return False
148	    return True
149	
150	
151	def validate_review_checks(
152	    payload: Any,
153	    *,
154	    expected_ids: tuple[str, ...] | list[str] | None = None,
155	) -> list[str]:
156	    raw_checks = payload.get("checks") if isinstance(payload, dict) else payload
157	    expected = get_check_ids() if expected_ids is None else list(expected_ids)
158	    if not isinstance(raw_checks, list):
159	        return expected
160	
161	    expected_set = set(expected)
162	    valid_ids: set[str] = set()
163	    invalid_expected_ids: set[str] = set()
164	    invalid_unknown_ids: set[str] = set()
165	    seen_counts: dict[str, int] = {}
166	
167	    for raw_check in raw_checks:
168	        if not isinstance(raw_check, dict):
169	            continue
170	        check_id = raw_check.get("id")
171	        if not isinstance(check_id, str) or not check_id:
172	            continue
173	
174	        seen_counts[check_id] = seen_counts.get(check_id, 0) + 1
175	        if check_id not in expected_set:
176	            invalid_unknown_ids.add(check_id)
177	            continue
178	        if seen_counts[check_id] > 1:
179	            invalid_expected_ids.add(check_id)
180	            continue
181	
182	        question = raw_check.get("question")
183	        findings = raw_check.get("findings")
184	        if not isinstance(question, str) or not question.strip():
185	            invalid_expected_ids.add(check_id)
186	            continue
187	        if not _valid_findings(findings):
188	            invalid_expected_ids.add(check_id)
189	            continue
190	        valid_ids.add(check_id)
191	
192	    return [
193	        check_id
194	        for check_id in expected
195	        if check_id not in valid_ids or check_id in invalid_expected_ids
196	    ] + sorted(invalid_unknown_ids)
197	
198	
199	__all__ = [
200	    "REVIEW_CHECKS",
201	    "ReviewCheckSpec",
202	    "build_check_category_map",
203	    "build_empty_template",
204	    "checks_for_robustness",
205	    "get_check_by_id",
206	    "get_check_ids",
207	    "validate_review_checks",
208	]
209
```

> AGENT

Now let me look at the data structures to see if there's a YAML schema file:

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan -name \"*.yaml\" -o -name \"*.yml\" | head -20"
}
```

> TOOL

tool_result Bash
```
[rerun: b7]
```

> AGENT

Let me check the chain.py file to understand the milestone/step structure in YAML:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/chain.py",
  "limit": 150
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
```

> AGENT

Now let me search for "verify" patterns in the codebase:

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"verif\\|verify\" /Users/user_c042661f/Documents/megaplan/megaplan --include=\"*.py\" | grep -E \"def|class|\\\"verify\" | head -30"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py:def _ensure_verification_task(payload: dict, state: dict) -> None:
/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py:    test_keywords = ("run test", "run the test", "verify", "verification", "pytest", "test suite", "run existing test")
/Users/user_c042661f/Documents/megaplan/megaplan/workers.py:                    "concern": "The plan does not define an observable verification command.",
/Users/user_c042661f/Documents/megaplan/megaplan/workers.py:            {"criterion": "A concrete verification command is defined.", "priority": "should"},
[rerun: b8]
```

> AGENT

Now let me look at the _core module to understand the data loading functions:

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
[rerun: b9]
```

> AGENT

Let me read the _core/__init__.py to see what functions are exported:

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

Let me read workflow.py to see the state machine and step definitions:

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

Perfect! Now let me look at how criteria/success metrics are defined in the plan. Let me check the checks module:

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan/megaplan -name \"checks.py\""
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/checks.py
[rerun: b10]
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/checks.py"
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
180	    payload: Any,
181	    *,
182	    expected_ids: tuple[str, ...] | list[str] | None = None,
183	) -> list[str]:
184	    raw_checks = payload.get("checks") if isinstance(payload, dict) else payload
185	    expected = get_check_ids() if expected_ids is None else list(expected_ids)
186	    if not isinstance(raw_checks, list):
187	        return expected
188	
189	    expected_set = set(expected)
190	    valid_ids: set[str] = set()
191	    invalid_expected_ids: set[str] = set()
192	    invalid_unknown_ids: set[str] = set()
193	    seen_counts: dict[str, int] = {}
194	
195	    for raw_check in raw_checks:
196	        if not isinstance(raw_check, dict):
197	            continue
198	        check_id = raw_check.get("id")
199	        if not isinstance(check_id, str) or not check_id:
200	            continue
201	
202	        seen_counts[check_id] = seen_counts.get(check_id, 0) + 1
203	        if check_id not in expected_set:
204	            invalid_unknown_ids.add(check_id)
205	            continue
206	        if seen_counts[check_id] > 1:
207	            invalid_expected_ids.add(check_id)
208	            continue
209	
210	        question = raw_check.get("question")
211	        findings = raw_check.get("findings")
212	        if not isinstance(question, str) or not question.strip():
213	            invalid_expected_ids.add(check_id)
214	            continue
215	        if not _valid_findings(findings):
216	            invalid_expected_ids.add(check_id)
217	            continue
218	        valid_ids.add(check_id)
219	
220	    return [
221	        check_id
222	        for check_id in expected
223	        if check_id not in valid_ids or check_id in invalid_expected_ids
224	    ] + sorted(invalid_unknown_ids)
225	
226	
227	__all__ = [
228	    "CRITIQUE_CHECKS",
229	    "VALID_SEVERITY_HINTS",
230	    "build_check_category_map",
231	    "build_empty_template",
232	    "checks_for_robustness",
233	    "get_check_by_id",
234	    "get_check_ids",
235	    "validate_critique_checks",
236	]
237
```

> AGENT

Now let me look at a test file to understand the data model better:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"success_criteria\\|gates\\|criteria\" /Users/user_c042661f/Documents/megaplan/tests/test_schemas.py | head -30"
}
```

> TOOL

tool_result Bash
```
24:        "criteria": [],
279:        "criteria": [{"name": "criterion", "priority": "must", "pass": "fail", "evidence": "Missing coverage."}],
372:    assert set(schema["required"]) == {"plan", "questions", "success_criteria", "assumptions"}
430:        "success_criteria",
448:        "criteria",
[rerun: b11]
```

> AGENT

Let me check if there's any YAML spec documentation:

> TOOL

tool_use Bash
```json
{
  "command": "grep -r \"milestone\\|YAML\\|spec\" /Users/user_c042661f/Documents/megaplan/README.md | head -30"
}
```

> TOOL

tool_result Bash
```
[rerun: b12]
```

> AGENT

Let me read the README:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/README.md"
}
```

> TOOL

tool_result Read
```
1	# Megaplan
2	
3	A planning and execution harness that helps LLMs solve complex tasks through structured phases — plan, critique, gate, revise, finalize, execute, and review. Instead of one-shot attempts, Megaplan gives any model a rigorous process with independent critique and gating.
4	
5	## Quick Start — Claude Code / Codex
6	
7	Copy and give this to your agent:
8	
9	```
10	Please install megaplan and set it up for this project:
11	
12	pip install megaplan-harness
13	megaplan setup
14	
15	Once you're done, ask me what I need megaplan for.
16	```
17	
18	## Quick Start — Open Models via OpenRouter
19	
20	Copy and give this to your agent:
21	
22	```
23	Please install megaplan with the open-model backend and set it up:
24	
25	pip install megaplan-harness hermes-agent
26	
27	Then create ~/.hermes/.env with:
28	OPENROUTER_API_KEY=<my key>
29	
30	Then run: megaplan setup
31	
32	Once you're done, ask me what I need megaplan for.
33	```
34	
35	Get an OpenRouter key at [openrouter.ai/keys](https://openrouter.ai/keys). Any model on OpenRouter works — Qwen, Llama, Mistral, DeepSeek, etc.
36	
37	---
38	
39	## How it works
40	
41	```
42	plan → critique → gate → [revise → critique → gate]* → finalize → execute → review
43	```
44	
45	Each phase can use a different model. The critique phase uses an independent model to review the plan and raise flags. The gate decides whether to proceed or iterate. This prevents models from rubber-stamping their own work. Planning now goes through a visible `prep` phase so repository investigation is observable instead of hidden inside `plan`.
46	
47	## Running manually
48	
49	```bash
50	megaplan init --project-dir . "Fix the authentication bug in login.py"
51	megaplan plan --plan <name>
52	megaplan critique --plan <name>
53	megaplan gate --plan <name>
54	megaplan finalize --plan <name>
55	megaplan execute --plan <name>
56	```
57	
58	## Using different models per phase
59	
60	Models with provider prefixes route to direct APIs. Models without a prefix go through OpenRouter:
61	
62	```json
63	{
64	  "models": {
65	    "prep": "zhipu:glm-5.1",
66	    "plan": "zhipu:glm-5.1",
67	    "critique": "minimax:MiniMax-M2.7-highspeed",
68	    "execute": "zhipu:glm-5.1",
69	    "review": "minimax:MiniMax-M2.7-highspeed"
70	  }
71	}
72	```
73	
74	Configure direct provider keys in `~/.hermes/.env`:
75	
76	```bash
77	ZHIPU_API_KEY=...          # for zhipu: prefix
78	MINIMAX_API_KEY=...        # for minimax: prefix
79	GEMINI_API_KEY=...         # for google: prefix
80	```
81	
82	## Robustness levels
83	
84	- **light** — visible `prep` + one critique/revise pass, no gate or review
85	- **standard** — visible `prep` + 4 critique checks (default)
86	- **robust** — visible `prep` + 8 critique checks + parallel critique
87	- **superrobust** — same as robust + parallel review
88	
89	## Observability
90	
91	```bash
92	megaplan status --plan <name>
93	```
94	
95	`status` is the single monitoring command. It exposes lifecycle fields such as `active_step`, `last_step`, notes, cost, execute progress, and next-step runtime guidance.
96	`watch` remains as a backward-compatible alias to `status`.
97	
98	## Subagent mode (Claude Code / Codex)
99	
100	Subagent mode delegates the full workflow to an autonomous agent, returning control only at defined breakpoints. It is the default orchestration mode for Claude Code and Codex. Cursor continues to run inline.
101	
102	```bash
103	megaplan config set orchestration.mode subagent   # default
104	megaplan config set orchestration.mode inline      # switch back
105	```
106	
107	## Configuration & Defaults
108	
109	View all settings with `megaplan config show`. Override with `megaplan config set <key> <value>`. Reset with `megaplan config reset`.
110	
111	| Key | Default | Description |
112	|-----|---------|-------------|
113	| `orchestration.mode` | `subagent` | `inline` or `subagent` (Claude Code and Codex) |
114	| `orchestration.max_critique_concurrency` | `2` | Max parallel critique checks |
115	| `execution.worker_timeout_seconds` | `7200` | Worker process timeout (seconds) |
116	| `execution.max_execute_no_progress` | `3` | No-progress execute attempts before escalation |
117	| `execution.max_review_rework_cycles` | `3` | Review→rework loops before force-proceeding |
118	| `agents.<step>` | varies | Agent for each phase (`claude`, `codex`, `hermes`) |
119	
120	```bash
121	megaplan config set execution.worker_timeout_seconds 3600
122	megaplan config set agents.critique hermes
123	megaplan config reset
124	```
125	
126	## SWE-bench Experiment
127	
128	Megaplan is being tested live against Claude 4.5 Opus on SWE-bench Verified:
129	
130	- **[Live dashboard](https://peteromallet.github.io/swe-bench-challenge/)** — watch the experiment in real time
131	- **[hermes-megaplan](https://github.com/peteromallet/hermes-megaplan)** — experiment orchestration code
132	
133	## Code Health
134	
135	<img src="scorecard.png" width="100%">
136	
137	## License
138	
139	MIT
140
```

> AGENT

Now let me check for any tests that show how the gate and criteria work:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def test.*gate\\|flag_resolutions\\|blocking\" /Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py | head -40"
}
```

> TOOL

tool_result Bash
```
161:def open_blocking_flags(plan_dir: Path) -> list[dict]:
171:def ensure_blocking_flags(plan_dir: Path, count: int) -> list[dict]:
180:        raise AssertionError("expected at least one blocking flag in the fixture")
193:    return open_blocking_flags(plan_dir)
201:    flag_resolutions: list[dict] | None = None,
212:            "flag_resolutions": flag_resolutions or [],
235:def test_init_sets_last_gate_and_next_step_plan(plan_fixture: PlanFixture) -> None:
998:def test_standard_revise_routes_to_critique_and_clears_last_gate(plan_fixture: PlanFixture) -> None:
1014:def test_handle_plan_stores_nonblocking_structure_warnings(plan_fixture: PlanFixture, monkeypatch: pytest.MonkeyPatch) -> None:
1259:def test_handle_revise_requires_prior_iterate_gate(plan_fixture: PlanFixture) -> None:
1267:def test_force_proceed_from_critiqued_writes_override_gate(plan_fixture: PlanFixture) -> None:
1337:def test_replan_from_gated_resets_to_planned(plan_fixture: PlanFixture) -> None:
1364:def test_gate_proceed_with_accepted_tradeoffs_creates_debt(
1370:    flag = ensure_blocking_flags(plan_fixture.plan_dir, 1)[0]
1375:        flag_resolutions=[
1402:def test_gate_iterate_with_empty_accepted_tradeoffs_creates_no_debt(
1415:            "flag_resolutions": [],
1435:def test_gate_proceed_partial_resolutions_still_missing_after_reprompt_downgrades_to_iterate(
1441:    flags = ensure_blocking_flags(plan_fixture.plan_dir, 5)
1446:        flag_resolutions=[
1472:        flag_resolutions=[
1737:def test_gate_retry_does_not_duplicate_weighted_scores(plan_fixture: PlanFixture, monkeypatch: pytest.MonkeyPatch) -> None:
1740:    flag = ensure_blocking_flags(plan_fixture.plan_dir, 1)[0]
1752:                        "flag_resolutions": [],
1772:                        "flag_resolutions": [
1807:def test_gate_proceed_partial_resolutions_triggers_reprompt(
1813:    flags = ensure_blocking_flags(plan_fixture.plan_dir, 2)
1818:        flag_resolutions=[
1832:        flag_resolutions=[
1870:def test_gate_proceed_still_missing_after_reprompt_downgrades_to_iterate(
1876:    flags = ensure_blocking_flags(plan_fixture.plan_dir, 2)
1881:        flag_resolutions=[],
1888:        flag_resolutions=[],
1915:def test_gate_accept_tradeoff_rubber_stamp_rejected(plan_fixture: PlanFixture) -> None:
1918:    flag = ensure_blocking_flags(plan_fixture.plan_dir, 1)[0]
1921:    result, next_step, _, blocking_unresolved_ids = megaplan.handlers._apply_gate_outcome(
1928:            "flag_resolutions": [
1943:    assert blocking_unresolved_ids == [flag["id"]]
1947:def test_gate_accept_tradeoff_concrete_rationale_accepted(plan_fixture: PlanFixture) -> None:
1950:    flag = ensure_blocking_flags(plan_fixture.plan_dir, 1)[0]
[rerun: b13]
```

> AGENT

Excellent. Let me read one of the gate tests to understand the full structure:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py",
  "offset": 1364,
  "limit": 80
}
```

> TOOL

tool_result Read
```
1364	def test_gate_proceed_with_accepted_tradeoffs_creates_debt(
1365	    plan_fixture: PlanFixture,
1366	    monkeypatch: pytest.MonkeyPatch,
1367	) -> None:
1368	    megaplan.handle_plan(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
1369	    megaplan.handle_critique(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
1370	    flag = ensure_blocking_flags(plan_fixture.plan_dir, 1)[0]
1371	    worker = make_gate_worker_result(
1372	        recommendation="PROCEED",
1373	        rationale="Known tradeoff accepted.",
1374	        signals_assessment="Proceeding with one accepted limitation.",
1375	        flag_resolutions=[
1376	            {
1377	                "flag_id": flag["id"],
1378	                "action": "accept_tradeoff",
1379	                "evidence": "",
1380	                "rationale": "The timeout-recovery gap is contained to a low-traffic path and is tracked for a later redesign.",
1381	            }
1382	        ],
1383	        accepted_tradeoffs=[],
1384	        session_id="gate-debt-1",
1385	    )
1386	    monkeypatch.setattr(
1387	        megaplan.workers,
1388	        "run_step_with_worker",
1389	        lambda *args, **kwargs: (worker, "claude", "persistent", False),
1390	    )
1391	
1392	    response = megaplan.handle_gate(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
1393	    registry = read_json(debt_registry_path(plan_fixture.root))
1394	
1395	    assert response["recommendation"] == "PROCEED"
1396	    assert response["reprompted"] is False
1397	    assert response["debt_entries_added"] == 1
1398	    assert len(registry["entries"]) == 1
1399	    assert registry["entries"][0]["flag_ids"] == [flag["id"]]
1400	
1401	
1402	def test_gate_iterate_with_empty_accepted_tradeoffs_creates_no_debt(
1403	    plan_fixture: PlanFixture,
1404	    monkeypatch: pytest.MonkeyPatch,
1405	) -> None:
1406	    megaplan.handle_plan(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
1407	    megaplan.handle_critique(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
1408	    worker = WorkerResult(
1409	        payload={
1410	            "recommendation": "ITERATE",
1411	            "rationale": "Still needs plan work.",
1412	            "signals_assessment": "Revisions are still needed.",
1413	            "warnings": [],
1414	            "settled_decisions": [],
1415	            "flag_resolutions": [],
1416	            "accepted_tradeoffs": [],
1417	        },
1418	        raw_output="{}",
1419	        duration_ms=1,
1420	        cost_usd=0.0,
1421	        session_id="gate-debt-2",
1422	    )
1423	    monkeypatch.setattr(
1424	        megaplan.workers,
1425	        "run_step_with_worker",
1426	        lambda *args, **kwargs: (worker, "claude", "persistent", False),
1427	    )
1428	
1429	    response = megaplan.handle_gate(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
1430	
1431	    assert response["debt_entries_added"] == 0
1432	    assert not debt_registry_path(plan_fixture.root).exists()
1433	
1434	
1435	def test_gate_proceed_partial_resolutions_still_missing_after_reprompt_downgrades_to_iterate(
1436	    plan_fixture: PlanFixture,
1437	    monkeypatch: pytest.MonkeyPatch,
1438	) -> None:
1439	    megaplan.handle_plan(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
1440	    megaplan.handle_critique(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
1441	    flags = ensure_blocking_flags(plan_fixture.plan_dir, 5)
1442	    first_attempt = make_gate_worker_result(
1443	        recommendation="PROCEED",
```

> AGENT

Perfect! Now I have enough information. Let me create a comprehensive summary by reading a few more key pieces on the YAML schema for chain specs:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/chain.py",
  "offset": 150,
  "limit": 100
}
```

> TOOL

tool_result Read
```
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
```

> AGENT

Perfect! Now I have a complete picture. Let me compile a comprehensive final report.

## Summary: Megaplan Project Structure and Gate/Review System

I've completed a thorough exploration of the megaplan project. Here are my findings:

---

### 1. **Overall File Structure**

**Top-level:**
- `/megaplan/` — main package (32 modules)
- `/tests/` — comprehensive test suite (24 test files)
- `/CHANGELOG.md` — v0.16.0 current (released 2026-04-15)
- `/pyproject.toml` — version 0.16.0, Python 3.11+, depends on PyYAML

**Key subdirectories:**
- `megaplan/_core/` — state management, registries, workflow logic, I/O
- `megaplan/loop/` — loop mode (iterative planning)
- `megaplan/prompts/` — phase-specific prompt builders
- `megaplan/data/` — schema/data definitions

---

### 2. **Gate/Review System - How Gates Work**

**Gate Flow (from `handlers.py:handle_gate`):**

1. **Gate Signals Built** (`build_gate_signals` in `evaluation.py`):
   - Collects unresolved significant flags, weighted scores, plan deltas, recurring critiques
   - Computes weighted trajectory and debt overlaps
   - Generates warnings if scope creep, high iteration count, or escalated debt subsystems exist

2. **Worker Runs Gate** (calls Claude/Codex with `_gate_prompt`):
   - Gate receives: plan, critique results, success criteria, gate signals, unresolved flags
   - Returns one of three recommendations: `PROCEED`, `ITERATE`, `ESCALATE`

3. **Flag Resolution Validation** (`_apply_gate_outcome` lines 614-641):
   - **Blocking flags** (severity = "significant" or "likely-significant"):
     - If PROCEED recommended: EVERY blocking flag must have a `flag_resolutions` entry
     - No implicit acceptance — unresolved blocking flags trigger automatic reprompt
   - **Valid resolutions**:
     - `action: "dispute"` — critique is factually wrong (requires concrete evidence, not rubber-stamp)
     - `action: "accept_tradeoff"` — concern is real but intentionally accepted (requires specific rationale)
   - Invalid/rubber-stamp evidence/rationale entries are skipped (see `is_rubber_stamp()` in `evaluation.py:103`)

4. **Reprompt Logic** (lines 1087-1141):
   - If PROCEED has blocking unresolved flags, a reprompt is issued once with missing flag IDs
   - If retry still leaves blocking flags unresolved: auto-downgrade to ITERATE with explanation
   - `gate_summary["reprompted"]` flag tracks if reprompt occurred

5. **Gate Outcome** (lines 651-666):
   - `PROCEED + preflight_passed` → move to `finalize`
   - `PROCEED + !preflight_passed` → move to `revise` (blocked status)
   - `ITERATE` → move to `revise`
   - `ESCALATE` → move to `override add-note` (user decision point)

6. **Debt Recording** (when PROCEED + accepted tradeoffs):
   - `_record_gate_debt_entries()` creates debt registry entries for accepted tradeoffs
   - Tracks subsystem, concern, flag_ids, plan_ids, occurrence count

---

### 3. **Criteria Evaluation in Milestone/Step Model**

**Data Structures (`types.py`):**

- **PlanState**: Contains `name`, `idea`, `current_state`, `iteration`, `config`, `sessions`, `history`, `meta`, `last_gate`
- **PlanMeta** (TypedDict):
  - `significant_counts`: list of flag counts per iteration
  - `weighted_scores`: gate signal scores per iteration
  - `plan_deltas`: % change between plan versions
  - `recurring_critiques`: flags that appear in multiple iterations
  - `total_cost_usd`: cumulative cost
  - `notes`: user annotations
  - `user_approved_gate`: if user manually approved

- **LastGateRecord**: Stores latest gate output (recommendation, rationale, warnings, settled_decisions, passed status, preflight_results)

**Success Criteria** (from `schemas.py` + plan metadata):
- Plan includes `success_criteria` array in plan.json schema
- Each criterion has: `criterion` (string description), `priority` (must/should/info)
- Evaluation happens in critique checks (see `checks.py` for critique check specs)
- Review phase verifies criteria pass/fail against execution

---

### 4. **YAML Schema for Plans (Chain Driver)**

**Chain Spec Structure** (`chain.py:11-27` docstring + `ChainSpec` class):

```yaml
seed:
  plan: <existing-plan-name>           # optional, drives first

milestones:
  - label: m1                           # required
    idea: /path/to/idea-m1.txt         # required
    branch: megaplan/m1-foundation      # optional (informational)
  - label: m2
    idea: /path/to/idea-m2.txt

on_failure:
  abort: stop_chain                    # stop_chain | skip_milestone | retry_milestone

on_escalate:
  abort: stop_chain                    # stop_chain | skip_milestone | retry_milestone

driver:
  stall_threshold: 5                   # iterations before escalation
  max_iterations: 200                  # hard cap
  poll_sleep: 2.0                      # seconds between status checks
  phase_timeout: 300.0                 # per-phase timeout
  status_timeout: 30.0                 # status command timeout
  on_escalate: force-proceed           # force-proceed | abort | fail
  robustness: standard                 # tiny | light | standard | robust | superrobust
  auto_approve: true
```

**Progress Persisted to** `chain_state.json`:
- `current_milestone_index`: -1 (seed), 0+ (milestone index)
- `current_plan_name`: active plan name
- `last_state`: terminal state of last completed plan
- `completed`: list of completed milestone records

---

### 5. **Verify/Verification Patterns**

**Test Verification Task** (`handlers.py:_ensure_verification_task` lines 1171-1239):
- Finalize appends a verification task (test-run) if not already present
- Task description instructs: "Run the tests specified in the task description...run the full test file/module...run the project's existing test suite — do NOT create new test files."
- Automatically creates sense check: "Did the verification tests pass? Were any regressions found and fixed?"
- Tracks baseline test failures so executor doesn't scope-creep fixing pre-existing failures

**Criteria Quality Check** (`checks.py:criteria_quality`):
- Critique checks whether success criteria are verifiable (`must` criteria must have clear yes/no answers)
- Flag subjective goals or numeric guidelines that should be `should` instead of `must`

**No explicit "verify" step** — verification is baked into:
1. Critique checks (including `verification` check in extended tier)
2. Finalize's auto-appended verification task
3. Review phase validates execution against criteria

---

### 6. **CHANGELOG.md — Recent Entries**

**v0.16.0 (2026-04-15):**
- Chain driver: new `megaplan chain` subcommand with YAML spec, resume-from-state, seed plan handling
- Tests cover spec parsing, chain status, validation, happy path, state resume, on-failure policies

**v0.14.0 (2026-04-15):**
- Strict gate flag resolution: PROCEED now requires explicit `flag_resolutions` for ALL blocking flags
- Reprompt once if first response leaves blocking flags unresolved
- Auto-downgrade to ITERATE if retry still fails to resolve blocking flags
- Rubber-stamp detection rejects vague dispute evidence and generic tradeoff rationale

**v0.12.0 (2026-04-15):**
- Auto driver: `megaplan auto --plan <name>` drives plan to terminal state
- Cross-directory plan discovery
- Standard robustness now includes init→plan transition

**v0.10.0 (2026-04-10):**
- Codex backend hardening (timeout recovery, partial output extraction, error classification)
- Plan locking (fcntl) to prevent concurrent step execution
- Active step tracking in state.json (`active_step` field with stale detection at 300s)
- `megaplan status` / `megaplan watch` unified monitoring
- Tiny robustness level (skips critique + gate)
- Parallel review for heavy robustness
- OpenAI strict-schema compatibility (all properties required)

---

### 7. **Version & Schema Locations**

- **Version**: `0.16.0` defined in `/pyproject.toml` (line 7)
- **JSON Schemas**: `/megaplan/schemas.py` — `SCHEMAS` dict with keys:
  - `plan.json`, `prep.json`, `revise.json`, `critique.json`, `gate.json`, `finalize.json`, `execution.json`, `review.json`, `loop_plan.json`, `loop_execute.json`
  - `strict_schema()` function enforces `additionalProperties: false` and auto-populates `required` arrays
  - Notable: `gate.json` requires `flag_resolutions` (array of flag resolution objects) and `accepted_tradeoffs`
  - Notable: `review.json` has `rework_items` with explicit required fields (exception to strict_schema auto-population)

---

### 8. **Key Gate/Criteria Files**

- **/megaplan/handlers.py** — gate execution (lines 1049-1169), flag resolution validation (lines 604-666), debt recording
- **/megaplan/evaluation.py** — gate signals building, flag weighting, rubber-stamp detection, evidence validation
- **/megaplan/prompts/gate.py** — gate prompt with blocking flag requirements and examples
- **/megaplan/checks.py** — 8 critique checks including `criteria_quality` (verifiability check)
- **/megaplan/review_checks.py** — 4 review checks (coverage, placement, adjacent_calls, simplicity)
- **/megaplan/_core/workflow.py** — state machine with gate-driven transitions
- **/megaplan/types.py** — data structures, flag statuses, gate artifact TypedDict
- **/tests/test_megaplan.py** — comprehensive gate tests showing flag_resolutions, reprompt, auto-downgrade patterns

---

This comprehensive system ensures gates are **non-bypassable** (blocking flags require explicit resolution, reprompt on incomplete first attempt, auto-downgrade if still unresolved) while maintaining **auditability** through debt registry, flag history, and settled decisions.
