> DEVELOPER

I need to understand the test patterns in this project to write doc-mode tests. Please find:

1. Look at tests/ directory - what test files exist, what patterns do they use (pytest fixtures, tmp_path, mocking, etc.)
2. Read tests/test_config.py to understand how handle_init is tested
3. Read tests/test_schemas.py to understand schema testing patterns
4. Look at any test that tests _write_finalize_artifacts or execution_timeout functions
5. Check how validate_execution_evidence is tested

Focus on: fixture patterns, how state dicts are constructed, how handlers are called in tests. Give me file paths and key snippets.

> AGENT

I'll help you understand the test patterns in this project. Let me start by exploring the tests directory and then examining the specific test files you mentioned.

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan/tests -type f -name \"*.py\" | head -20"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/tests/test_parallel_critique.py
/Users/user_c042661f/Documents/megaplan/tests/test_review_checks.py
/Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py
/Users/user_c042661f/Documents/megaplan/tests/test_core.py
/Users/user_c042661f/Documents/megaplan/tests/test_prompts.py
/Users/user_c042661f/Documents/megaplan/tests/test_parallel_review.py
/Users/user_c042661f/Documents/megaplan/tests/__init__.py
/Users/user_c042661f/Documents/megaplan/tests/test_io_git_patch.py
/Users/user_c042661f/Documents/megaplan/tests/test_loop.py
/Users/user_c042661f/Documents/megaplan/tests/test_evaluation.py
/Users/user_c042661f/Documents/megaplan/tests/test_review_mechanical.py
/Users/user_c042661f/Documents/megaplan/tests/test_config.py
/Users/user_c042661f/Documents/megaplan/tests/test_schemas.py
/Users/user_c042661f/Documents/megaplan/tests/test_checks.py
/Users/user_c042661f/Documents/megaplan/tests/test_tiny_robustness.py
/Users/user_c042661f/Documents/megaplan/tests/test_swe_bench.py
/Users/user_c042661f/Documents/megaplan/tests/test_workers.py
/Users/user_c042661f/Documents/megaplan/tests/test_handle_review_robustness.py
/Users/user_c042661f/Documents/megaplan/tests/test_quality.py
[rerun: b1]
```

> AGENT

Now let me read the specific test files you requested:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/tests/test_config.py"
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	import json
4	from argparse import Namespace
5	from pathlib import Path
6	
7	import pytest
8	
9	import megaplan
10	import megaplan.cli as cli_module
11	import megaplan._core.io as io_module
12	from megaplan._core import get_effective
13	from megaplan.types import DEFAULTS
14	
15	
16	@pytest.fixture
17	def isolated_config_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
18	    config_path = tmp_path / ".config" / "megaplan"
19	
20	    def fake_config_dir(home: Path | None = None) -> Path:
21	        del home
22	        return config_path
23	
24	    monkeypatch.setattr(io_module, "config_dir", fake_config_dir)
25	    monkeypatch.setattr(cli_module, "config_dir", fake_config_dir)
26	    return config_path
27	
28	
29	def test_get_effective_returns_default(isolated_config_dir: Path) -> None:
30	    assert not (isolated_config_dir / "config.json").exists()
31	    assert get_effective("execution", "worker_timeout_seconds") == DEFAULTS["execution.worker_timeout_seconds"]
32	
33	
34	def test_get_effective_returns_override(isolated_config_dir: Path) -> None:
35	    isolated_config_dir.mkdir(parents=True, exist_ok=True)
36	    (isolated_config_dir / "config.json").write_text(
37	        json.dumps({"execution": {"worker_timeout_seconds": 1234}}),
38	        encoding="utf-8",
39	    )
40	
41	    assert get_effective("execution", "worker_timeout_seconds") == 1234
42	
43	
44	def test_config_set_numeric(isolated_config_dir: Path) -> None:
45	    response = megaplan.handle_config(
46	        Namespace(
47	            config_action="set",
48	            [REDACTED],
49	            value="3600",
50	        )
51	    )
52	
53	    assert response["success"] is True
54	    assert response["value"] == 3600
55	    saved = json.loads((isolated_config_dir / "config.json").read_text(encoding="utf-8"))
56	    assert saved["execution"]["worker_timeout_seconds"] == 3600
57	    assert isinstance(saved["execution"]["worker_timeout_seconds"], int)
58	
59	
60	@pytest.mark.parametrize(
61	    ("value", "expected"),
62	    [
63	        ("true", True),
64	        ("TRUE", True),
65	        ("1", True),
66	        ("yes", True),
67	        ("YeS", True),
68	        ("on", True),
69	        ("false", False),
70	        ("FALSE", False),
71	        ("0", False),
72	        ("no", False),
73	        ("No", False),
74	        ("off", False),
75	    ],
76	)
77	def test_config_set_execution_auto_approve_bool_tokens(
78	    isolated_config_dir: Path,
79	    value: str,
80	    expected: bool,
81	) -> None:
82	    response = megaplan.handle_config(
83	        Namespace(
84	            config_action="set",
85	            [REDACTED],
86	            value=value,
87	        )
88	    )
89	
90	    assert response["success"] is True
91	    assert response["value"] is expected
92	    saved = json.loads((isolated_config_dir / "config.json").read_text(encoding="utf-8"))
93	    assert saved["execution"]["auto_approve"] is expected
94	
95	
96	def test_config_set_execution_auto_approve_invalid_token(isolated_config_dir: Path) -> None:
97	    with pytest.raises(
98	        megaplan.CliError,
99	        match=r"execution\.auto_approve must be one of: true, false, 1, 0, yes, no, on, off",
100	    ):
101	        megaplan.handle_config(
102	            Namespace(
103	                config_action="set",
104	                [REDACTED],
105	                value="maybe",
106	            )
107	        )
108	
109	
110	@pytest.mark.parametrize("value", ["tiny", "light", "standard", "robust", "superrobust"])
111	def test_config_set_execution_robustness_enum(
112	    isolated_config_dir: Path,
113	    value: str,
114	) -> None:
115	    response = megaplan.handle_config(
116	        Namespace(
117	            config_action="set",
118	            [REDACTED],
119	            value=value,
120	        )
121	    )
122	
123	    assert response["success"] is True
124	    assert response["value"] == value
125	    saved = json.loads((isolated_config_dir / "config.json").read_text(encoding="utf-8"))
126	    assert saved["execution"]["robustness"] == value
127	
128	
129	def test_config_set_execution_robustness_invalid_value(isolated_config_dir: Path) -> None:
130	    with pytest.raises(
131	        megaplan.CliError,
132	        match=r"execution\.robustness must be one of: tiny, light, standard, robust, superrobust",
133	    ):
134	        megaplan.handle_config(
135	            Namespace(
136	                config_action="set",
137	                [REDACTED],
138	                value="turbo",
139	            )
140	        )
141	
142	
143	def test_config_set_invalid_key(isolated_config_dir: Path) -> None:
144	    with pytest.raises(megaplan.CliError, match=r"Unknown config key 'foo\.bar'"):
145	        megaplan.handle_config(
146	            Namespace(
147	                config_action="set",
148	                key="foo.bar",
149	                value="1",
150	            )
151	        )
152	
153	
154	def test_config_set_invalid_type(isolated_config_dir: Path) -> None:
155	    with pytest.raises(
156	        megaplan.CliError,
157	        match=r"execution\.worker_timeout_seconds must be an integer",
158	    ):
159	        megaplan.handle_config(
160	            Namespace(
161	                config_action="set",
162	                [REDACTED],
163	                value="notanumber",
164	            )
165	        )
166	
167	
168	def test_config_set_orchestration_mode(isolated_config_dir: Path) -> None:
169	    response = megaplan.handle_config(
170	        Namespace(
171	            config_action="set",
172	            [REDACTED],
173	            value="inline",
174	        )
175	    )
176	
177	    assert response["success"] is True
178	    assert response["value"] == "inline"
179	    saved = json.loads((isolated_config_dir / "config.json").read_text(encoding="utf-8"))
180	    assert saved["orchestration"]["mode"] == "inline"
181	
182	
183	def test_config_set_orchestration_mode_invalid(isolated_config_dir: Path) -> None:
184	    with pytest.raises(
185	        megaplan.CliError,
186	        match=r"orchestration\.mode must be 'inline' or 'subagent'",
187	    ):
188	        megaplan.handle_config(
189	            Namespace(
190	                config_action="set",
191	                [REDACTED],
192	                value="bogus",
193	            )
194	        )
195	
196	
197	def test_build_parser_init_flags_are_tristate() -> None:
198	    from megaplan.cli import build_parser
199	
200	    parser = build_parser()
201	
202	    parsed = parser.parse_args(["init", "--project-dir", "/tmp", "idea"])
203	    explicit = parser.parse_args(
204	        ["init", "--project-dir", "/tmp", "--auto-approve", "--robustness", "robust", "idea"]
205	    )
206	
207	    assert parsed.auto_approve is None
208	    assert parsed.robustness is None
209	    assert explicit.auto_approve is True
210	    assert explicit.robustness == "robust"
211	
212	
213	def test_handle_init_uses_config_defaults_when_flags_omitted(isolated_config_dir: Path, tmp_path: Path) -> None:
214	    isolated_config_dir.mkdir(parents=True, exist_ok=True)
215	    (isolated_config_dir / "config.json").write_text(
216	        json.dumps({"execution": {"auto_approve": True, "robustness": "robust"}}),
217	        encoding="utf-8",
218	    )
219	    root = tmp_path / "root"
220	    project_dir = tmp_path / "project"
221	    root.mkdir()
222	    project_dir.mkdir()
223	
224	    response = megaplan.handle_init(
225	        root,
226	        Namespace(
227	            project_dir=str(project_dir),
228	            name="config-backed-init",
229	            auto_approve=None,
230	            robustness=None,
231	            hermes=None,
232	            phase_model=[],
233	            idea="idea",
234	        ),
235	    )
236	    state = json.loads((root / ".megaplan" / "plans" / response["plan"] / "state.json").read_text(encoding="utf-8"))
237	
238	    assert response["auto_approve"] is True
239	    assert response["robustness"] == "robust"
240	    assert state["config"]["auto_approve"] is True
241	    assert state["config"]["robustness"] == "robust"
242	
243	
244	def test_handle_init_explicit_robustness_beats_config_default(
245	    isolated_config_dir: Path,
246	    tmp_path: Path,
247	) -> None:
248	    isolated_config_dir.mkdir(parents=True, exist_ok=True)
249	    (isolated_config_dir / "config.json").write_text(
250	        json.dumps({"execution": {"auto_approve": True, "robustness": "robust"}}),
251	        encoding="utf-8",
252	    )
253	    root = tmp_path / "root"
254	    project_dir = tmp_path / "project"
255	    root.mkdir()
256	    project_dir.mkdir()
257	
258	    response = megaplan.handle_init(
259	        root,
260	        Namespace(
261	            project_dir=str(project_dir),
262	            name="explicit-robustness-init",
263	            auto_approve=None,
264	            robustness="light",
265	            hermes=None,
266	            phase_model=[],
267	            idea="idea",
268	        ),
269	    )
270	    state = json.loads((root / ".megaplan" / "plans" / response["plan"] / "state.json").read_text(encoding="utf-8"))
271	
272	    assert response["auto_approve"] is True
273	    assert response["robustness"] == "light"
274	    assert state["config"]["auto_approve"] is True
275	    assert state["config"]["robustness"] == "light"
276
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/tests/test_schemas.py"
}
```

> TOOL

tool_result Read
```
1	"""Direct tests for megaplan.schemas."""
2	
3	from __future__ import annotations
4	
5	import json
6	from pathlib import Path
7	
8	from jsonschema import Draft7Validator
9	
10	from megaplan.schemas import SCHEMAS, strict_schema
11	
12	
13	def _review_disk_schema() -> dict[str, object]:
14	    return json.loads((Path(__file__).resolve().parents[1] / ".megaplan" / "schemas" / "review.json").read_text(encoding="utf-8"))
15	
16	
17	def _minimal_review_payload() -> dict[str, object]:
18	    return {
19	        "review_verdict": "approved",
20	        "checks": [],
21	        "pre_check_flags": [],
22	        "verified_flag_ids": [],
23	        "disputed_flag_ids": [],
24	        "criteria": [],
25	        "issues": [],
26	        "rework_items": [],
27	        "summary": "Approved.",
28	        "task_verdicts": [],
29	        "sense_check_verdicts": [],
30	    }
31	
32	
33	def test_schema_registry_matches_5_step_workflow() -> None:
34	    required = {"plan.json", "prep.json", "revise.json", "gate.json", "critique.json", "finalize.json", "execution.json", "review.json"}
35	    assert required.issubset(set(SCHEMAS))
36	
37	
38	# ---------------------------------------------------------------------------
39	# strict_schema tests
40	# ---------------------------------------------------------------------------
41	
42	
43	def test_strict_schema_adds_additional_properties_false() -> None:
44	    result = strict_schema({"type": "object", "properties": {"a": {"type": "string"}}})
45	    assert result["additionalProperties"] is False
46	
47	
48	def test_strict_schema_preserves_existing_additional_properties() -> None:
49	    result = strict_schema({"type": "object", "properties": {"a": {"type": "string"}}, "additionalProperties": True})
50	    assert result["additionalProperties"] is True
51	
52	
53	def test_strict_schema_sets_required_from_properties() -> None:
54	    result = strict_schema({"type": "object", "properties": {"x": {"type": "string"}, "y": {"type": "number"}}})
55	    assert set(result["required"]) == {"x", "y"}
56	
57	
58	def test_strict_schema_normalizes_partial_required_arrays_recursively() -> None:
59	    schema = {
60	        "type": "object",
61	        "required": ["stale_root"],
62	        "properties": {
63	            "inner": {
64	                "type": "object",
65	                "required": ["stale_inner"],
66	                "properties": {"child": {"type": "string"}},
67	            },
68	            "items": {
69	                "type": "array",
70	                "items": {
71	                    "type": "object",
72	                    "required": ["stale_item"],
73	                    "properties": {"name": {"type": "string"}},
74	                },
75	            },
76	        },
77	    }
78	
79	    result = strict_schema(schema)
80	
81	    assert result["required"] == ["inner", "items"]
82	    assert result["properties"]["inner"]["required"] == ["child"]
83	    assert result["properties"]["items"]["items"]["required"] == ["name"]
84	
85	
86	def test_strict_schema_nested_objects_get_additional_properties() -> None:
87	    schema = {
88	        "type": "object",
89	        "properties": {
90	            "inner": {"type": "object", "properties": {"a": {"type": "string"}}},
91	        },
92	    }
93	    result = strict_schema(schema)
94	    assert result["properties"]["inner"]["additionalProperties"] is False
95	    assert result["properties"]["inner"]["required"] == ["a"]
96	
97	
98	def test_strict_schema_array_items_are_strict() -> None:
99	    schema = {
100	        "type": "object",
101	        "properties": {
102	            "list": {
103	                "type": "array",
104	                "items": {"type": "object", "properties": {"name": {"type": "string"}}},
105	            }
106	        },
107	    }
108	    result = strict_schema(schema)
109	    assert result["properties"]["list"]["items"]["additionalProperties"] is False
110	
111	
112	def test_strict_schema_deeply_nested() -> None:
113	    schema = {
114	        "type": "object",
115	        "properties": {
116	            "l1": {
117	                "type": "object",
118	                "properties": {
119	                    "l2": {
120	                        "type": "object",
121	                        "properties": {"l3": {"type": "string"}},
122	                    }
123	                },
124	            }
125	        },
126	    }
127	    result = strict_schema(schema)
128	    assert result["properties"]["l1"]["properties"]["l2"]["additionalProperties"] is False
129	
130	
131	def test_strict_schema_non_object_untouched() -> None:
132	    assert strict_schema({"type": "string"}) == {"type": "string"}
133	    assert strict_schema(42) == 42
134	    assert strict_schema("hello") == "hello"
135	    assert strict_schema([1, 2]) == [1, 2]
136	
137	
138	# ---------------------------------------------------------------------------
139	# Schema completeness tests
140	# ---------------------------------------------------------------------------
141	
142	
143	def test_schema_registry_has_all_expected_steps() -> None:
144	    required_schemas = {"plan.json", "prep.json", "revise.json", "gate.json", "critique.json", "finalize.json", "execution.json", "review.json"}
145	    assert required_schemas.issubset(set(SCHEMAS.keys()))
146	
147	
148	def test_schema_registry_entries_include_required_field() -> None:
149	    for name, schema in SCHEMAS.items():
150	        assert "required" in schema, f"Schema '{name}' missing 'required' field"
151	        assert isinstance(schema["required"], list)
152	
153	
154	def test_schema_registry_entries_are_objects() -> None:
155	    for name, schema in SCHEMAS.items():
156	        assert schema.get("type") == "object", f"Schema '{name}' is not type 'object'"
157	        assert "properties" in schema, f"Schema '{name}' missing 'properties'"
158	
159	
160	def test_critique_schema_flags_have_expected_structure() -> None:
161	    critique = SCHEMAS["critique.json"]
162	    flags_schema = critique["properties"]["flags"]
163	    assert flags_schema["type"] == "array"
164	    item_schema = flags_schema["items"]
165	    assert "id" in item_schema["properties"]
166	    assert "concern" in item_schema["properties"]
167	    assert "category" in item_schema["properties"]
168	    assert "severity_hint" in item_schema["properties"]
169	    assert "evidence" in item_schema["properties"]
170	
171	
172	def test_finalize_schema_tracks_structured_execution_fields() -> None:
173	    finalize = SCHEMAS["finalize.json"]
174	    assert "tasks" in finalize["properties"]
175	    assert "sense_checks" in finalize["properties"]
176	    assert "validation" in finalize["properties"]
177	    assert "baseline_test_failures" in finalize["properties"]
178	    assert "baseline_test_command" in finalize["properties"]
179	    assert "baseline_test_note" in finalize["properties"]
180	    assert "validation" in finalize["required"]
181	    assert "baseline_test_failures" not in finalize["required"]
182	    assert "baseline_test_command" not in finalize["required"]
183	    assert "baseline_test_note" not in finalize["required"]
184	    assert "final_plan" not in finalize["properties"]
185	    assert "task_count" not in finalize["properties"]
186	    task_schema = finalize["properties"]["tasks"]["items"]
187	    assert set(task_schema["properties"]) == {
188	        "id",
189	        "description",
190	        "depends_on",
191	        "status",
192	        "executor_notes",
193	        "files_changed",
194	        "commands_run",
195	        "evidence_files",
196	        "reviewer_verdict",
197	    }
198	    assert task_schema["properties"]["status"]["enum"] == ["pending", "done", "skipped"]
199	    assert "executor_note" in finalize["properties"]["sense_checks"]["items"]["properties"]
200	    # Validation sub-schema
201	    validation_schema = finalize["properties"]["validation"]
202	    assert "plan_steps_covered" in validation_schema["properties"]
203	    assert "orphan_tasks" in validation_schema["properties"]
204	    assert "completeness_notes" in validation_schema["properties"]
205	    assert "coverage_complete" in validation_schema["properties"]
206	    step_item = validation_schema["properties"]["plan_steps_covered"]["items"]
207	    assert "plan_step_summary" in step_item["properties"]
208	    assert "finalize_task_ids" in step_item["properties"]
209	    assert step_item["properties"]["finalize_task_ids"]["type"] == "array"
210	
211	
212	def test_execution_schema_requires_task_updates() -> None:
213	    execution = SCHEMAS["execution.json"]
214	    assert "task_updates" in execution["properties"]
215	    assert "task_updates" in execution["required"]
216	    assert "sense_check_acknowledgments" in execution["properties"]
217	    assert "sense_check_acknowledgments" in execution["required"]
218	    item_schema = execution["properties"]["task_updates"]["items"]
219	    assert item_schema["properties"]["status"]["enum"] == ["done", "skipped"]
220	    assert "files_changed" in item_schema["properties"]
221	    assert "commands_run" in item_schema["properties"]
222	
223	
224	def test_review_schema_requires_task_and_sense_check_verdicts() -> None:
225	    review = SCHEMAS["review.json"]
226	    assert "review_verdict" in review["properties"]
227	    assert "task_verdicts" in review["properties"]
228	    assert "sense_check_verdicts" in review["properties"]
229	    assert "rework_items" in review["properties"]
230	    assert "review_verdict" in review["required"]
231	    assert "task_verdicts" in review["required"]
232	    assert "sense_check_verdicts" in review["required"]
233	    assert "rework_items" in review["required"]
234	    assert "evidence_files" in review["properties"]["task_verdicts"]["items"]["properties"]
235	    # Rework items sub-schema
236	    rework_item = review["properties"]["rework_items"]["items"]
237	    assert "task_id" in rework_item["properties"]
238	    assert "issue" in rework_item["properties"]
239	    assert "expected" in rework_item["properties"]
240	    assert "actual" in rework_item["properties"]
241	    assert "evidence_file" in rework_item["properties"]
242	    assert "flag_id" in rework_item["properties"]
243	    assert "source" in rework_item["properties"]
244	    assert set(rework_item["required"]) == {"task_id", "issue", "expected", "actual", "evidence_file", "flag_id", "source"}
245	    assert rework_item["properties"]["flag_id"]["type"] == ["string", "null"]
246	    assert rework_item["properties"]["source"]["type"] == ["string", "null"]
247	
248	
249	def test_review_schema_accepts_parallel_mode_extensions_in_both_copies() -> None:
250	    payload = {
251	        "review_verdict": "needs_rework",
252	        "checks": [
253	            {
254	                "id": "coverage",
255	                "question": "Does the diff cover the issue?",
256	                "guidance": "Inspect the changed module for missing review follow-up.",
257	                "findings": [
258	                    {
259	                        "detail": "Coverage review found one concrete issue example that the diff still does not handle.",
260	                        "flagged": True,
261	                        "status": "blocking",
262	                        "evidence_file": "pkg/module.py",
263	                    }
264	                ],
265	                "prior_findings": [],
266	            }
267	        ],
268	        "pre_check_flags": [
269	            {
270	                "id": "PRECHECK-SOURCE_TOUCH",
271	                "check": "source_touch",
272	                "detail": "The diff touches a package source file.",
273	                "severity": "minor",
274	                "evidence_file": "pkg/module.py",
275	            }
276	        ],
277	        "verified_flag_ids": ["REVIEW-COVERAGE-001"],
278	        "disputed_flag_ids": ["REVIEW-PARITY-001"],
279	        "criteria": [{"name": "criterion", "priority": "must", "pass": "fail", "evidence": "Missing coverage."}],
280	        "issues": ["Coverage review found a blocking issue."],
281	        "rework_items": [
282	            {
283	                "task_id": "REVIEW",
284	                "issue": "Coverage gap remains.",
285	                "expected": "All issue examples are covered.",
286	                "actual": "One issue example remains uncovered.",
287	                "evidence_file": "pkg/module.py",
288	                "flag_id": None,
289	                "source": "review_coverage",
290	            }
291	        ],
292	        "summary": "Heavy review found a blocking issue.",
293	        "task_verdicts": [
294	            {
295	                "task_id": "T1",
296	                "reviewer_verdict": "Needs follow-up.",
297	                "evidence_files": ["pkg/module.py"],
298	            }
299	        ],
300	        "sense_check_verdicts": [{"sense_check_id": "SC1", "verdict": "Needs follow-up."}],
301	    }
302	    disk_schema = _review_disk_schema()
303	
304	    assert list(Draft7Validator(SCHEMAS["review.json"]).iter_errors(payload)) == []
305	    assert list(Draft7Validator(disk_schema).iter_errors(payload)) == []
306	
307	
308	def test_review_schema_accepts_optional_rework_item_flag_id() -> None:
309	    payload = _minimal_review_payload()
310	    payload["review_verdict"] = "needs_rework"
311	    payload["issues"] = ["Critique flag remains unresolved."]
312	    payload["rework_items"] = [
313	        {
314	            "task_id": "REVIEW",
315	            "issue": "Critique flag remains unresolved.",
316	            "expected": "The final diff addresses the flagged concern directly.",
317	            "actual": "The diff leaves the flagged behavior unchanged.",
318	            "evidence_file": "megaplan/prompts/review.py",
319	            "flag_id": "FLAG-001",
320	            "source": "review_flag_reverify",
321	        }
322	    ]
323	    disk_schema = _review_disk_schema()
324	
325	    assert list(Draft7Validator(SCHEMAS["review.json"]).iter_errors(payload)) == []
326	    assert list(Draft7Validator(disk_schema).iter_errors(payload)) == []
327	
328	
329	def test_review_schema_still_accepts_rework_items_without_flag_id() -> None:
330	    payload = _minimal_review_payload()
331	    payload["review_verdict"] = "needs_rework"
332	    payload["issues"] = ["Executor still needs to finish the review follow-up."]
333	    payload["rework_items"] = [
334	        {
335	            "task_id": "REVIEW",
336	            "issue": "Executor still needs to finish the review follow-up.",
337	            "expected": "All required review follow-up work is complete.",
338	            "actual": "One required review follow-up item is still missing.",
339	            "evidence_file": "megaplan/handlers.py",
340	            "flag_id": None,
341	            "source": None,
342	        }
343	    ]
344	    disk_schema = _review_disk_schema()
345	
346	    assert list(Draft7Validator(SCHEMAS["review.json"]).iter_errors(payload)) == []
347	    assert list(Draft7Validator(disk_schema).iter_errors(payload)) == []
348	
349	
350	# ---------------------------------------------------------------------------
351	# Original tests
352	# ---------------------------------------------------------------------------
353	
354	
355	def test_gate_schema_is_strict_and_requires_core_fields() -> None:
356	    schema = strict_schema(SCHEMAS["gate.json"])
357	    assert schema["additionalProperties"] is False
358	    assert schema["required"] == [
359	        "recommendation",
360	        "rationale",
361	        "signals_assessment",
362	        "warnings",
363	        "settled_decisions",
364	        "flag_resolutions",
365	        "accepted_tradeoffs",
366	    ]
367	    assert schema["properties"]["recommendation"]["enum"] == ["PROCEED", "ITERATE", "ESCALATE"]
368	
369	
370	def test_plan_schema_has_core_fields_only() -> None:
371	    schema = strict_schema(SCHEMAS["plan.json"])
372	    assert set(schema["required"]) == {"plan", "questions", "success_criteria", "assumptions"}
373	    assert "self_flags" not in schema["properties"]
374	    assert "gate_recommendation" not in schema["properties"]
375	
376	
377	def test_prep_schema_exists_and_has_expected_structure() -> None:
378	    schema = strict_schema(SCHEMAS["prep.json"])
379	    assert set(schema["required"]) == {
380	        "skip",
381	        "task_summary",
382	        "key_evidence",
383	        "relevant_code",
384	        "test_expectations",
385	        "constraints",
386	        "suggested_approach",
387	    }
388	    evidence_schema = schema["properties"]["key_evidence"]["items"]
389	    relevant_code_schema = schema["properties"]["relevant_code"]["items"]
390	    test_expectation_schema = schema["properties"]["test_expectations"]["items"]
391	    assert set(evidence_schema["required"]) == {"point", "source", "relevance"}
392	    assert evidence_schema["properties"]["relevance"]["enum"] == ["high", "medium", "low"]
393	    assert set(relevant_code_schema["required"]) == {"file_path", "why", "functions"}
394	    assert relevant_code_schema["properties"]["functions"]["items"]["type"] == "string"
395	    assert set(test_expectation_schema["required"]) == {"test_id", "what_it_checks", "status"}
396	    assert test_expectation_schema["properties"]["status"]["enum"] == ["fail_to_pass", "pass_to_pass"]
397	
398	
399	def test_gate_schema_includes_settled_decisions_structure() -> None:
400	    schema = strict_schema(SCHEMAS["gate.json"])
401	    item_schema = schema["properties"]["settled_decisions"]["items"]
402	    assert set(item_schema["required"]) == {"id", "decision", "rationale"}
403	    assert "rationale" in item_schema["properties"]
404	
405	
406	def test_gate_schema_flag_resolutions_stay_codex_compatible() -> None:
407	    schema = strict_schema(SCHEMAS["gate.json"])
408	    item_schema = schema["properties"]["flag_resolutions"]["items"]
409	
410	    assert set(item_schema["required"]) == {"flag_id", "action", "evidence", "rationale"}
411	    assert "oneOf" not in item_schema
412	    assert set(item_schema["properties"]["action"]["enum"]) == {"dispute", "accept_tradeoff"}
413	    assert "evidence" in item_schema["properties"]
414	    assert "rationale" in item_schema["properties"]
415	
416	
417	def test_schema_registry_covers_the_six_strict_mode_required_fixes() -> None:
418	    revise = SCHEMAS["revise.json"]
419	    gate = SCHEMAS["gate.json"]
420	    review = SCHEMAS["review.json"]
421	    review_check = review["properties"]["checks"]["items"]
422	    review_finding = review_check["properties"]["findings"]["items"]
423	    pre_check_flag = review["properties"]["pre_check_flags"]["items"]
424	
425	    assert set(revise["required"]) == {
426	        "plan",
427	        "changes_summary",
428	        "flags_addressed",
429	        "assumptions",
430	        "success_criteria",
431	        "questions",
432	    }
433	    assert set(gate["required"]) == {
434	        "recommendation",
435	        "rationale",
436	        "signals_assessment",
437	        "warnings",
438	        "settled_decisions",
439	        "flag_resolutions",
440	        "accepted_tradeoffs",
441	    }
442	    assert set(review["required"]) == {
443	        "review_verdict",
444	        "checks",
445	        "pre_check_flags",
446	        "verified_flag_ids",
447	        "disputed_flag_ids",
448	        "criteria",
449	        "issues",
450	        "rework_items",
451	        "summary",
452	        "task_verdicts",
453	        "sense_check_verdicts",
454	    }
455	    assert set(review_check["required"]) == {"id", "question", "guidance", "findings", "prior_findings"}
456	    assert set(review_finding["required"]) == {"detail", "flagged", "status", "evidence_file"}
457	    assert set(pre_check_flag["required"]) == {"id", "check", "detail", "severity", "evidence_file"}
458	
459	
460	def test_strict_schema_new_tracking_objects_are_strict() -> None:
461	    schema = strict_schema(SCHEMAS["finalize.json"])
462	    task_schema = schema["properties"]["tasks"]["items"]
463	    sense_check_schema = schema["properties"]["sense_checks"]["items"]
464	    assert task_schema["additionalProperties"] is False
465	    assert set(task_schema["required"]) == {
466	        "id",
467	        "description",
468	        "depends_on",
469	        "status",
470	        "executor_notes",
471	        "files_changed",
472	        "commands_run",
473	        "evidence_files",
474	        "reviewer_verdict",
475	    }
476	    assert sense_check_schema["additionalProperties"] is False
477	    assert set(sense_check_schema["required"]) == {"id", "task_id", "question", "executor_note", "verdict"}
478
```

> AGENT

Now let me search for tests related to `_write_finalize_artifacts`, `execution_timeout`, and `validate_execution_evidence`:

> TOOL

tool_use Grep
```json
{
  "pattern": "_write_finalize_artifacts|execution_timeout|validate_execution_evidence",
  "path": "/Users/user_c042661f/Documents/megaplan/tests",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result Grep
```
Found 1 file
tests/test_evaluation.py
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/tests/test_evaluation.py"
}
```

> TOOL

tool_result Read
```
1	"""Direct tests for megaplan.evaluation."""
2	
3	from __future__ import annotations
4	
5	import json
6	import subprocess
7	from pathlib import Path
8	
9	import pytest
10	
11	from megaplan.evaluation import (
12	    PLAN_STRUCTURE_REQUIRED_STEP_ISSUE,
13	    _strip_fenced_blocks,
14	    build_gate_artifact,
15	    build_orchestrator_guidance,
16	    build_gate_signals,
17	    compute_plan_delta_percent,
18	    compute_recurring_critiques,
19	    flag_weight,
20	    is_rubber_stamp,
21	    parse_plan_sections,
22	    reassemble_plan,
23	    renumber_steps,
24	    validate_execution_evidence,
25	    validate_plan_structure,
26	)
27	from megaplan.workers import _build_mock_payload
28	
29	
30	def _write_json(path: Path, data: dict[str, object]) -> None:
31	    path.parent.mkdir(parents=True, exist_ok=True)
32	    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
33	
34	
35	def _state(tmp_path: Path, *, iteration: int = 1, robustness: str = "standard") -> dict[str, object]:
36	    previous_version = iteration - 1
37	    return {
38	        "name": "plan",
39	        "idea": "ship it",
40	        "current_state": "critiqued",
41	        "iteration": iteration,
42	        "created_at": "2026-03-20T00:00:00Z",
43	        "config": {
44	            "project_dir": str(tmp_path / "project"),
45	            "auto_approve": False,
46	            "robustness": robustness,
47	        },
48	        "sessions": {},
49	        "plan_versions": (
50	            [
51	                {
52	                    "version": previous_version,
53	                    "file": f"plan_v{previous_version}a.md",
54	                    "hash": "sha256:prev",
55	                    "timestamp": "2026-03-19T00:00:00Z",
56	                },
57	                {
58	                    "version": iteration,
59	                    "file": f"plan_v{iteration}.md",
60	                    "hash": "sha256:current",
61	                    "timestamp": "2026-03-20T00:00:00Z",
62	                },
63	            ]
64	            if iteration > 1
65	            else [
66	            {
67	                "version": 1,
68	                "file": "plan_v1.md",
69	                "hash": "sha256:current",
70	                "timestamp": "2026-03-20T00:00:00Z",
71	            }
72	            ]
73	        ),
74	        "history": [],
75	        "meta": {
76	            "significant_counts": [],
77	            "weighted_scores": [4.0] if iteration > 1 else [],
78	            "plan_deltas": [33.0] if iteration > 1 else [],
79	            "recurring_critiques": [],
80	            "total_cost_usd": 0.0,
81	            "overrides": [],
82	            "notes": [],
83	        },
84	        "last_gate": {},
85	    }
86	
87	
88	def _scaffold(tmp_path: Path, *, iteration: int = 1, flags: list[dict[str, object]] | None = None) -> tuple[Path, dict[str, object]]:
89	    plan_dir = tmp_path / "plan"
90	    plan_dir.mkdir()
91	    (tmp_path / "project").mkdir()
92	    flags = flags or []
93	    _write_json(plan_dir / "faults.json", {"flags": flags})
94	    _write_json(
95	        plan_dir / f"critique_v{iteration}.json",
96	        {"flags": [{"concern": "same issue"}] if iteration > 1 else [], "verified_flag_ids": [], "disputed_flag_ids": []},
97	    )
98	    if iteration > 1:
99	        previous_version = iteration - 1
100	        _write_json(
101	            plan_dir / f"critique_v{previous_version}.json",
102	            {"flags": [{"concern": "same issue"}], "verified_flag_ids": [], "disputed_flag_ids": []},
103	        )
104	        (plan_dir / f"plan_v{previous_version}a.md").write_text("old plan\n", encoding="utf-8")
105	    (plan_dir / f"plan_v{iteration}.md").write_text("new plan with more detail\n", encoding="utf-8")
106	    _write_json(
107	        plan_dir / f"plan_v{iteration}.meta.json",
108	        {
109	            "version": iteration,
110	            "timestamp": "2026-03-20T00:00:00Z",
111	            "hash": "sha256:test",
112	            "success_criteria": [{"criterion": "criterion", "priority": "must"}],
113	            "questions": [],
114	            "assumptions": [],
115	        },
116	    )
117	    return plan_dir, _state(tmp_path, iteration=iteration)
118	
119	
120	def _signals(
121	    *,
122	    iteration: int = 2,
123	    weighted_score: float = 3.0,
124	    weighted_history: list[float] | None = None,
125	    recurring_critiques: list[str] | None = None,
126	    unresolved_flags: list[dict[str, object]] | None = None,
127	    scope_creep_flags: list[str] | None = None,
128	) -> dict[str, object]:
129	    return {
130	        "iteration": iteration,
131	        "weighted_score": weighted_score,
132	        "weighted_history": weighted_history if weighted_history is not None else [4.0],
133	        "recurring_critiques": recurring_critiques or [],
134	        "unresolved_flags": unresolved_flags or [],
135	        "scope_creep_flags": scope_creep_flags or [],
136	    }
137	
138	
139	# ---------------------------------------------------------------------------
140	# flag_weight tests
141	# ---------------------------------------------------------------------------
142	
143	
144	def test_flag_weight_security_highest() -> None:
145	    assert flag_weight({"category": "security"}) == 3.0
146	
147	
148	def test_flag_weight_correctness() -> None:
149	    assert flag_weight({"category": "correctness"}) == 2.0
150	
151	
152	def test_flag_weight_completeness() -> None:
153	    assert flag_weight({"category": "completeness"}) == 1.5
154	
155	
156	def test_flag_weight_performance() -> None:
157	    assert flag_weight({"category": "performance"}) == 1.0
158	
159	
160	def test_flag_weight_maintainability() -> None:
161	    assert flag_weight({"category": "maintainability"}) == 0.75
162	
163	
164	def test_flag_weight_other() -> None:
165	    assert flag_weight({"category": "other"}) == 1.0
166	
167	
168	def test_flag_weight_unknown_category() -> None:
169	    assert flag_weight({"category": "nonexistent"}) == 1.0
170	
171	
172	def test_flag_weight_missing_category() -> None:
173	    assert flag_weight({}) == 1.0
174	
175	
176	def test_flag_weight_implementation_detail_signals_reduce_weight() -> None:
177	    for signal in ["column", "schema", "field", "as written", "pseudocode", "seed sql", "placeholder"]:
178	        assert flag_weight({"category": "correctness", "concern": f"The {signal} is wrong"}) == 0.5
179	
180	
181	def test_flag_weight_security_overrides_implementation_detail() -> None:
182	    assert flag_weight({"category": "security", "concern": "The schema field is wrong"}) == 3.0
183	
184	
185	def test_flag_weight_empty_flag() -> None:
186	    assert flag_weight({}) == 1.0
187	
188	
189	# ---------------------------------------------------------------------------
190	# compute_plan_delta_percent tests
191	# ---------------------------------------------------------------------------
192	
193	
194	def test_compute_plan_delta_percent_returns_zero_for_identical_texts() -> None:
195	    assert compute_plan_delta_percent("same text", "same text") == 0.0
196	
197	
198	def test_compute_plan_delta_percent_returns_large_delta_for_different_text() -> None:
199	    delta = compute_plan_delta_percent("aaa", "zzz")
200	    assert delta is not None
201	    assert delta > 50.0
202	
203	
204	def test_compute_plan_delta_percent_returns_none_without_previous_text() -> None:
205	    assert compute_plan_delta_percent(None, "anything") is None
206	
207	
208	# ---------------------------------------------------------------------------
209	# compute_recurring_critiques tests
210	# ---------------------------------------------------------------------------
211	
212	
213	def test_compute_recurring_critiques_no_overlap(tmp_path: Path) -> None:
214	    plan_dir = tmp_path / "plan"
215	    plan_dir.mkdir()
216	    _write_json(plan_dir / "critique_v1.json", {"flags": [{"concern": "Issue A"}]})
217	    _write_json(plan_dir / "critique_v2.json", {"flags": [{"concern": "Issue B"}]})
218	    assert compute_recurring_critiques(plan_dir, 2) == []
219	
220	
221	def test_compute_recurring_critiques_iteration_less_than_2(tmp_path: Path) -> None:
222	    plan_dir = tmp_path / "plan"
223	    plan_dir.mkdir()
224	    assert compute_recurring_critiques(plan_dir, 1) == []
225	    assert compute_recurring_critiques(plan_dir, 0) == []
226	
227	
228	# ---------------------------------------------------------------------------
229	# plan structure validation tests
230	# ---------------------------------------------------------------------------
231	
232	
233	def test_strip_fenced_blocks_removes_only_fenced_content() -> None:
234	    text = """before
235	```python
236	inside
237	```
238	after
239	"""
240	    assert _strip_fenced_blocks(text) == "before\nafter\n"
241	
242	
243	def test_parse_plan_sections_basic() -> None:
244	    plan = """# Implementation Plan: Example
245	
246	## Overview
247	Summarize the work.
248	
249	## Step 1: Update validation (`megaplan/evaluation.py`)
250	1. **Add** the validator (`megaplan/evaluation.py:1`).
251	
252	## Notes
253	Keep this section in place.
254	
255	## Step 2: Add tests (`tests/test_evaluation.py`)
256	1. **Cover** the parser (`tests/test_evaluation.py:1`).
257	"""
258	    sections = parse_plan_sections(plan)
259	
260	    assert [section.id for section in sections] == [None, None, "S1", None, "S2"]
261	    assert sections[0].heading == ""
262	    assert sections[0].start_line == 1
263	    assert sections[0].end_line == 2
264	    assert sections[2].heading == "## Step 1: Update validation (`megaplan/evaluation.py`)"
265	    assert sections[2].start_line == 6
266	    assert sections[2].end_line == 8
267	    assert sections[3].heading == "## Notes"
268	    assert sections[4].start_line == 12
269	    assert sections[4].end_line == 13
270	
271	
272	def test_parse_plan_sections_fenced() -> None:
273	    plan = """# Implementation Plan: Example
274	
275	## Overview
276	```md
277	## Step 99: Fake step (`fake.py`)
278	1. **Ignore** this heading (`fake.py:1`).
279	```
280	
281	## Step 1: Real step (`megaplan/evaluation.py`)
282	1. **Add** the validator (`megaplan/evaluation.py:1`).
283	
284	## Validation Order
285	1. Run tests.
286	"""
287	    sections = parse_plan_sections(plan)
288	
289	    assert [section.heading for section in sections] == [
290	        "",
291	        "## Overview",
292	        "## Step 1: Real step (`megaplan/evaluation.py`)",
293	        "## Validation Order",
294	    ]
295	    assert [section.id for section in sections] == [None, None, "S1", None]
296	
297	
298	def test_renumber_steps() -> None:
299	    plan = """# Implementation Plan: Example
300	
301	## Overview
302	Summary.
303	
304	## Step 1: First step (`a.py`)
305	1. **Do** the first part (`a.py:1`).
306	
307	## Step 3: Third step (`c.py`)
308	1. **Do** the third part (`c.py:1`).
309	"""
310	    sections = parse_plan_sections(plan)
311	    renumbered = renumber_steps(sections)
312	
313	    assert [section.id for section in renumbered if section.id is not None] == ["S1", "S2"]
314	    assert "## Step 2: Third step (`c.py`)" in renumbered[-1].body
315	
316	
317	def test_reassemble_roundtrip() -> None:
318	    plan = """# Implementation Plan: Example
319	
320	## Overview
321	Intro text.
322	
323	```python
324	print("## Step 42: not real")
325	```
326	
327	## Step 1: Update validation (`megaplan/evaluation.py`)
328	1. **Add** the validator (`megaplan/evaluation.py:1`).
329	"""
330	    assert reassemble_plan(parse_plan_sections(plan)) == plan
331	
332	
333	def test_validate_plan_structure_accepts_valid_plan() -> None:
334	    plan = """# Implementation Plan: Example
335	
336	## Overview
337	Summarize the work.
338	
339	## Step 1: Update validation (`megaplan/evaluation.py`)
340	**Scope:** Small
341	1. **Add** the validator (`megaplan/evaluation.py:1`).
342	
343	## Step 2: Add tests (`tests/test_evaluation.py`)
344	**Scope:** Small
345	1. **Cover** the expected plan shapes (`tests/test_evaluation.py:1`).
346	
347	## Execution Order
348	1. Land the validator before wiring it.
349	
350	## Validation Order
351	1. Run unit tests first.
352	"""
353	    assert validate_plan_structure(plan) == []
354	
355	
356	def test_validate_plan_structure_warns_when_overview_missing() -> None:
357	    plan = """# Implementation Plan: Example
358	
359	## Step 1: Update validation (`megaplan/evaluation.py`)
360	1. **Add** the validator (`megaplan/evaluation.py:1`).
361	
362	## Validation Order
363	1. Run unit tests first.
364	"""
365	    issues = validate_plan_structure(plan)
366	    assert "Plan should include a `## Overview` section." in issues
367	
368	
369	def test_validate_plan_structure_errors_when_step_sections_missing() -> None:
370	    plan = """# Implementation Plan: Example
371	
372	## Overview
373	Summarize the work.
374	
375	## Validation Order
376	1. Run unit tests first.
377	"""
378	    assert validate_plan_structure(plan) == [PLAN_STRUCTURE_REQUIRED_STEP_ISSUE]
379	
380	
381	def test_validate_plan_structure_warns_when_substeps_missing() -> None:
382	    plan = """# Implementation Plan: Example
383	
384	## Overview
385	Summarize the work.
386	
387	## Step 1: Update validation (`megaplan/evaluation.py`)
388	No numbered substeps here.
389	
390	## Validation Order
391	1. Run unit tests first.
392	"""
393	    issues = validate_plan_structure(plan)
394	    assert "Each step section should include at least one numbered substep." in issues
395	
396	
397	def test_validate_plan_structure_warns_when_ordering_sections_missing() -> None:
398	    plan = """# Implementation Plan: Example
399	
400	## Overview
401	Summarize the work.
402	
403	## Step 1: Update validation (`megaplan/evaluation.py`)
404	1. **Add** the validator (`megaplan/evaluation.py:1`).
405	"""
406	    issues = validate_plan_structure(plan)
407	    assert "Plan should include `## Execution Order` or `## Validation Order`." in issues
408	
409	
410	def test_validate_plan_structure_ignores_headings_inside_fenced_blocks() -> None:
411	    plan = """# Implementation Plan: Example
412	
413	## Overview
414	Summarize the work.
415	
416	```md
417	## Step 99: Fake step (`fake.py`)
418	1. **Ignore** this heading (`fake.py:1`).
419	```
420	
421	## Step 1: Real step (`megaplan/evaluation.py`)
422	1. **Add** the validator (`megaplan/evaluation.py:1`).
423	
424	## Validation Order
425	1. Run unit tests first.
426	"""
427	    assert validate_plan_structure(plan) == []
428	
429	
430	def test_validate_plan_structure_accepts_small_plan_with_single_ordering_section() -> None:
431	    plan = """# Implementation Plan: Example
432	
433	## Overview
434	Summarize the work.
435	
436	## Step 1: Update validation (`megaplan/evaluation.py`)
437	1. **Add** the validator (`megaplan/evaluation.py:1`).
438	
439	## Step 2: Add tests (`tests/test_evaluation.py`)
440	1. **Cover** the change (`tests/test_evaluation.py:1`).
441	
442	## Validation Order
443	1. Run unit tests first.
444	"""
445	    assert validate_plan_structure(plan) == []
446	
447	
448	def test_strip_fenced_blocks_unclosed_fence_returns_original() -> None:
449	    text = """before
450	```python
451	inside code
452	## Step 99: Hidden
453	after fence
454	"""
455	    # Unclosed fence — should return original text to avoid silently losing content
456	    assert _strip_fenced_blocks(text) == text
457	
458	
459	def test_parse_plan_sections_unclosed_fence_still_finds_sections() -> None:
460	    plan = """## Overview
461	Summary.
462	
463	```python
464	code without closing fence
465	
466	## Step 1: Real step
467	1. Do the thing.
468	
469	## Step 2: Another step
470	1. Do another thing.
471	"""
472	    sections = parse_plan_sections(plan)
473	    step_ids = [s.id for s in sections if s.id is not None]
474	    assert "S1" in step_ids
475	    assert "S2" in step_ids
476	
477	
478	def test_validate_plan_structure_accepts_phase_format() -> None:
479	    plan = """# Implementation Plan: Complex Feature
480	
481	## Overview
482	Multi-phase integration.
483	
484	## Phase 1: Foundation
485	
486	### Step 1: Install dependencies (`package.json`)
487	**Scope:** Small
488	1. **Install** the required packages (`package.json:1`).
489	
490	### Step 2: Create migration (`supabase/migrations/`)
491	**Scope:** Small
492	1. **Create** the database table (`supabase/migrations/001.sql:1`).
493	
494	## Phase 2: Core Integration
495	
496	### Step 3: Port the component (`src/components/Editor.tsx`)
497	**Scope:** Medium
498	1. **Copy** and adapt the component (`src/components/Editor.tsx:1`).
499	
500	## Execution Order
501	1. Foundation before integration.
502	
503	## Validation Order
504	1. Run tests after each phase.
505	"""
506	    assert validate_plan_structure(plan) == []
507	
508	
509	def test_parse_plan_sections_phase_format() -> None:
510	    plan = """# Implementation Plan: Example
511	
512	## Overview
513	Summary.
514	
515	## Main Phase
516	
517	### Step 1: First step (`a.py`)
518	1. **Do** the thing (`a.py:1`).
519	
520	### Step 2: Second step (`b.py`)
521	1. **Do** the other thing (`b.py:1`).
522	"""
523	    sections = parse_plan_sections(plan)
524	    step_ids = [s.id for s in sections if s.id is not None]
525	    assert step_ids == ["S1", "S2"]
526	    # Phase header has no id
527	    phase_sections = [s for s in sections if "Main Phase" in s.heading]
528	    assert len(phase_sections) == 1
529	    assert phase_sections[0].id is None
530	
531	
532	def test_renumber_steps_phase_format() -> None:
533	    plan = """# Implementation Plan: Example
534	
535	## Overview
536	Summary.
537	
538	## Main Phase
539	
540	### Step 1: First step (`a.py`)
541	1. **Do** the first part (`a.py:1`).
542	
543	### Step 5: Skipped numbering (`c.py`)
544	1. **Do** the third part (`c.py:1`).
545	"""
546	    sections = parse_plan_sections(plan)
547	    renumbered = renumber_steps(sections)
548	    step_sections = [s for s in renumbered if s.id is not None]
549	    assert [s.id for s in step_sections] == ["S1", "S2"]
550	    assert "### Step 2: Skipped numbering (`c.py`)" in step_sections[1].body
551	
552	
553	def test_render_final_md_none_meta_commentary() -> None:
554	    from megaplan._core import render_final_md
555	    data = {
556	        "tasks": [],
557	        "watch_items": [],
558	        "sense_checks": [],
559	        "meta_commentary": None,
560	    }
561	    result = render_final_md(data)
562	    assert "None." in result  # Should not crash
563	
564	
565	def test_is_rubber_stamp_loose_rejects_generic_ack() -> None:
566	    assert is_rubber_stamp("Confirmed.", strict=False) is True
567	
568	
569	def test_is_rubber_stamp_loose_allows_short_specific_text() -> None:
570	    # Loose mode is blocklist-only (DECISION-001): short but specific text passes
571	    assert is_rubber_stamp("Too short", strict=False) is False
572	
573	
574	def test_is_rubber_stamp_strict_rejects_low_substance_text() -> None:
575	    assert is_rubber_stamp("Verified done good", strict=True) is True
576	
577	
578	def test_is_rubber_stamp_accepts_real_note_in_both_modes() -> None:
579	    note = (
580	        "Confirmed the review prompt still renders the audit fallback and checked that the "
581	        "settled-decision wording only changed reviewer framing."
582	    )
583	    assert is_rubber_stamp(note, strict=False) is False
584	    assert is_rubber_stamp(note, strict=True) is False
585	
586	
587	def test_is_rubber_stamp_allows_short_specific_ack_only_in_loose_mode() -> None:
588	    note = "Confirmed prompt coverage."
589	    assert is_rubber_stamp(note, strict=False) is False
590	    assert is_rubber_stamp(note, strict=True) is True
591	
592	
593	def test_validate_execution_evidence_flags_diff_mismatches_and_weak_notes(
594	    tmp_path: Path,
595	    monkeypatch: pytest.MonkeyPatch,
596	) -> None:
597	    project_dir = tmp_path / "project"
598	    (project_dir / ".git").mkdir(parents=True)
599	    (project_dir / "src").mkdir()
600	    (project_dir / "docs").mkdir()
601	    (project_dir / "src" / "existing.py").write_text("print('ok')\n", encoding="utf-8")
602	    (project_dir / "docs" / "new_name.py").write_text("x = 1\n", encoding="utf-8")
603	
604	    finalize_data = {
605	        "tasks": [
606	            {
607	                "id": "T1",
608	                "files_changed": ["src/existing.py", "docs/new_name.py", "ghost.py"],
609	                "executor_notes": "Verified src/existing.py and confirmed the rename to docs/new_name.py showed up in git status.",
610	            }
611	        ],
612	        "sense_checks": [
613	            {"id": "SC1", "executor_note": "ok"},
614	        ],
615	    }
616	
617	    monkeypatch.setattr(
618	        "megaplan.evaluation.subprocess.run",
619	        lambda *args, **kwargs: subprocess.CompletedProcess(
620	            args=["git", "status", "--short"],
621	            returncode=0,
622	            stdout=" M src/existing.py\n?? untracked.md\nR  old_name.py -> docs/new_name.py\nD  deleted.txt\n",
623	            stderr="",
624	        ),
625	    )
626	
627	    result = validate_execution_evidence(finalize_data, project_dir)
628	
629	    assert result["skipped"] is False
630	    assert result["files_in_diff"] == ["deleted.txt", "docs/new_name.py", "src/existing.py", "untracked.md"]
631	    assert result["files_claimed"] == ["docs/new_name.py", "ghost.py", "src/existing.py"]
632	    assert any("ghost.py" in finding for finding in result["findings"])
633	    assert any("deleted.txt" in finding and "untracked.md" in finding for finding in result["findings"])
634	    assert any("SC1" in finding and "perfunctory" in finding for finding in result["findings"])
635	
636	
637	def test_build_gate_artifact_passes_through_settled_decisions(tmp_path: Path) -> None:
638	    plan_dir, state = _scaffold(tmp_path)
639	    gate_payload = _build_mock_payload(
640	        "gate",
641	        state,
642	        plan_dir,
643	        settled_decisions=[
644	            {
645	                "id": "DECISION-001",
646	                "decision": "Reviewer must respect the softened FLAG-006 behavior.",
647	                "rationale": "This was approved at gate time.",
648	            }
649	        ],
650	    )
651	    artifact = build_gate_artifact(
652	        {
653	            "criteria_check": {"count": 1, "items": ["criterion"]},
654	            "preflight_results": {"project_dir_exists": True},
655	            "unresolved_flags": [],
656	            "warnings": [],
657	            "robustness": "standard",
658	            "signals": {"weighted_score": 0.5},
659	        },
660	        gate_payload,
661	        override_forced=False,
662	    )
663	
664	    assert artifact["settled_decisions"] == gate_payload["settled_decisions"]
665	
666	
667	def test_validate_execution_evidence_skips_without_git_repo(tmp_path: Path) -> None:
668	    project_dir = tmp_path / "project"
669	    project_dir.mkdir()
670	
671	    result = validate_execution_evidence({"tasks": [], "sense_checks": []}, project_dir)
672	
673	    assert result["skipped"] is True
674	    assert result["reason"] == "Project directory is not a git repository."
675	
676	
677	def test_validate_execution_evidence_flags_perfunctory_executor_notes(
678	    tmp_path: Path,
679	    monkeypatch: pytest.MonkeyPatch,
680	) -> None:
681	    project_dir = tmp_path / "project"
682	    (project_dir / ".git").mkdir(parents=True)
683	
684	    finalize_data = {
685	        "tasks": [
686	            {
687	                "id": "T1",
688	                "status": "done",
689	                "files_changed": ["src/main.py"],
690	                "executor_notes": "Verified. Done.",
691	            },
692	            {
693	                "id": "T2",
694	                "status": "done",
695	                "files_changed": [],
696	                "executor_notes": "",
697	            },
698	        ],
699	        "sense_checks": [],
700	    }
701	
702	    monkeypatch.setattr(
703	        "megaplan.evaluation.subprocess.run",
704	        lambda *args, **kwargs: subprocess.CompletedProcess(
705	            args=["git", "status", "--short"],
706	            returncode=0,
707	            stdout=" M src/main.py\n",
708	            stderr="",
709	        ),
710	    )
711	
712	    result = validate_execution_evidence(finalize_data, project_dir)
713	
714	    assert any("Task T1 executor_notes are perfunctory" in finding for finding in result["findings"])
715	    assert not any("Task T2 executor_notes are perfunctory" in finding for finding in result["findings"])
716	
717	
718	def test_validate_execution_evidence_skips_when_git_missing(
719	    tmp_path: Path,
720	    monkeypatch: pytest.MonkeyPatch,
721	) -> None:
722	    project_dir = tmp_path / "project"
723	    (project_dir / ".git").mkdir(parents=True)
724	
725	    def _raise(*args: object, **kwargs: object) -> object:
726	        raise FileNotFoundError
727	
728	    monkeypatch.setattr("megaplan.evaluation.subprocess.run", _raise)
729	
730	    result = validate_execution_evidence({"tasks": [], "sense_checks": []}, project_dir)
731	
732	    assert result["skipped"] is True
733	    assert result["reason"] == "git not found on PATH."
734	
735	
736	def test_validate_execution_evidence_skips_on_timeout(
737	    tmp_path: Path,
738	    monkeypatch: pytest.MonkeyPatch,
739	) -> None:
740	    project_dir = tmp_path / "project"
741	    (project_dir / ".git").mkdir(parents=True)
742	
743	    def _raise(*args: object, **kwargs: object) -> object:
744	        raise subprocess.TimeoutExpired(cmd=["git", "status", "--short"], timeout=30)
745	
746	    monkeypatch.setattr("megaplan.evaluation.subprocess.run", _raise)
747	
748	    result = validate_execution_evidence({"tasks": [], "sense_checks": []}, project_dir)
749	
750	    assert result["skipped"] is True
751	    assert result["reason"] == "git status timed out."
752	
753	
754	def test_validate_execution_evidence_skips_on_nonzero_git_status(
755	    tmp_path: Path,
756	    monkeypatch: pytest.MonkeyPatch,
757	) -> None:
758	    project_dir = tmp_path / "project"
759	    (project_dir / ".git").mkdir(parents=True)
760	
761	    monkeypatch.setattr(
762	        "megaplan.evaluation.subprocess.run",
763	        lambda *args, **kwargs: subprocess.CompletedProcess(
764	            args=["git", "status", "--short"],
765	            returncode=128,
766	            stdout="",
767	            stderr="fatal: not a git repository",
768	        ),
769	    )
770	
771	    result = validate_execution_evidence({"tasks": [], "sense_checks": []}, project_dir)
772	
773	    assert result["skipped"] is True
774	    assert result["reason"] == "git status failed: fatal: not a git repository"
775	
776	
777	# ---------------------------------------------------------------------------
778	# build_gate_signals tests
779	# ---------------------------------------------------------------------------
780	
781	
782	def test_build_gate_signals_no_flags(tmp_path: Path) -> None:
783	    plan_dir, state = _scaffold(tmp_path, iteration=1, flags=[])
784	    result = build_gate_signals(plan_dir, state)
785	    assert result["signals"]["weighted_score"] == 0.0
786	    assert result["signals"]["unresolved_flags"] == []
787	    assert result["warnings"] == []
788	
789	
790	def test_build_gate_signals_iteration_5_warning(tmp_path: Path) -> None:
791	    plan_dir, state = _scaffold(tmp_path, iteration=5, flags=[])
792	    result = build_gate_signals(plan_dir, state)
793	    assert any("high iteration count" in w for w in result["warnings"])
794	
795	
796	def test_build_gate_signals_iteration_12_hard_limit_warning(tmp_path: Path) -> None:
797	    plan_dir, state = _scaffold(tmp_path, iteration=12, flags=[])
798	    result = build_gate_signals(plan_dir, state)
799	    assert any("hard iteration limit" in w for w in result["warnings"])
800	
801	
802	def test_build_gate_signals_resolved_flags_included(tmp_path: Path) -> None:
803	    flags = [
804	        {
805	            "id": "FLAG-001",
806	            "concern": "Was an issue",
807	            "category": "correctness",
808	            "severity_hint": "likely-significant",
809	            "evidence": "Fixed now",
810	            "status": "verified",
811	            "severity": "significant",
812	            "verified": True,
813	            "raised_in": "critique_v1.json",
814	        }
815	    ]
816	    plan_dir, state = _scaffold(tmp_path, iteration=1, flags=flags)
817	    result = build_gate_signals(plan_dir, state)
818	    assert len(result["signals"]["resolved_flags"]) == 1
819	    assert result["signals"]["resolved_flags"][0]["id"] == "FLAG-001"
820	
821	
822	def test_build_gate_signals_first_iteration_no_delta(tmp_path: Path) -> None:
823	    plan_dir, state = _scaffold(tmp_path, iteration=1, flags=[])
824	    result = build_gate_signals(plan_dir, state)
825	    assert result["signals"]["plan_delta_from_previous"] is None
826	
827	
828	# ---------------------------------------------------------------------------
829	# build_orchestrator_guidance tests
830	# ---------------------------------------------------------------------------
831	
832	
833	def test_build_orchestrator_guidance_first_iteration_follows_gate_with_hints() -> None:
834	    guidance = build_orchestrator_guidance(
835	        gate_payload={"recommendation": "ITERATE"},
836	        signals=_signals(
837	            iteration=1,
838	            weighted_history=[],
839	            recurring_critiques=["missing tests"],
840	            unresolved_flags=[{"id": "FLAG-001"}],
841	            scope_creep_flags=["FLAG-009"],
842	        ),
843	        preflight_passed=True,
844	        preflight_results={"project_dir_exists": True},
845	        robustness="standard",
846	        plan_name="demo-plan",
847	    )
848	    assert "First iteration; follow gate recommendation: ITERATE." in guidance
849	    assert "Verify unresolved flags against the plan and project code before accepting." in guidance
850	    assert "Recurring critiques (missing tests)" in guidance
851	    assert "Scope creep detected" in guidance
852	
853	
854	def test_build_orchestrator_guidance_proceed_with_preflight_passed() -> None:
855	    guidance = build_orchestrator_guidance(
856	        gate_payload={"recommendation": "PROCEED"},
857	        signals=_signals(),
858	        preflight_passed=True,
859	        preflight_results={"project_dir_exists": True},
860	        robustness="standard",
861	        plan_name="demo-plan",
862	    )
863	    assert guidance == "Plan passed gate and preflight. Proceed to finalize."
864	
865	
866	def test_build_orchestrator_guidance_proceed_with_preflight_failure_lists_checks() -> None:
867	    guidance = build_orchestrator_guidance(
868	        gate_payload={"recommendation": "PROCEED"},
869	        signals=_signals(unresolved_flags=[{"id": "FLAG-001"}]),
870	        preflight_passed=False,
871	        preflight_results={
872	            "project_dir_exists": True,
873	            "project_dir_writable": False,
874	            "success_criteria_present": False,
875	        },
876	        robustness="standard",
877	        plan_name="demo-plan",
878	    )
879	    assert "Gate says PROCEED but preflight blocked. Fix: project_dir_writable, success_criteria_present." in guidance
880	
881	
882	def test_build_orchestrator_guidance_escalate_requires_user_decision_when_not_auto_force() -> None:
883	    guidance = build_orchestrator_guidance(
884	        gate_payload={"recommendation": "ESCALATE"},
885	        signals=_signals(weighted_score=5.0, weighted_history=[4.0]),
886	        preflight_passed=True,
887	        preflight_results={"project_dir_exists": True},
888	        robustness="standard",
889	        plan_name="demo-plan",
890	    )
891	    assert guidance == "Gate escalated. Ask the user: force-proceed, add-note, or abort."
892	
893	
894	def test_build_orchestrator_guidance_iterate_plateaued_with_recurring_critiques() -> None:
895	    guidance = build_orchestrator_guidance(
896	        gate_payload={"recommendation": "ITERATE"},
897	        signals=_signals(
898	            weighted_score=3.0,
899	            weighted_history=[2.0],
900	            recurring_critiques=["missing tests"],
901	        ),
902	        preflight_passed=True,
903	        preflight_results={"project_dir_exists": True},
904	        robustness="standard",
905	        plan_name="demo-plan",
906	    )
907	    assert "Score plateaued with recurring critiques the loop can't fix." in guidance
908	    assert "megaplan override force-proceed --plan demo-plan" in guidance
909	
910	
911	def test_build_orchestrator_guidance_iterate_improving() -> None:
912	    guidance = build_orchestrator_guidance(
913	        gate_payload={"recommendation": "ITERATE"},
914	        signals=_signals(weighted_score=2.0, weighted_history=[3.5]),
915	        preflight_passed=True,
916	        preflight_results={"project_dir_exists": True},
917	        robustness="standard",
918	        plan_name="demo-plan",
919	    )
920	    assert guidance == "Score improving (3.5 -> 2.0). Continue to revise."
921	
922	
923	def test_build_orchestrator_guidance_iterate_worsening() -> None:
924	    guidance = build_orchestrator_guidance(
925	        gate_payload={"recommendation": "ITERATE"},
926	        signals=_signals(weighted_score=4.5, weighted_history=[3.0]),
927	        preflight_passed=True,
928	        preflight_results={"project_dir_exists": True},
929	        robustness="standard",
930	        plan_name="demo-plan",
931	    )
932	    assert guidance == "Score worsening (3.0 -> 4.5). Investigate; the loop may be diverging."
933	
934	
935	def test_build_orchestrator_guidance_iterate_fallthrough() -> None:
936	    guidance = build_orchestrator_guidance(
937	        gate_payload={"recommendation": "ITERATE"},
938	        signals=_signals(weighted_score=3.0, weighted_history=[3.0]),
939	        preflight_passed=True,
940	        preflight_results={"project_dir_exists": True},
941	        robustness="standard",
942	        plan_name="demo-plan",
943	    )
944	    assert guidance == "Gate recommends another iteration. Revise the plan."
945	
946	
947	# ---------------------------------------------------------------------------
948	# Original tests
949	# ---------------------------------------------------------------------------
950	
951	
952	def test_flag_weight_preserves_low_weight_implementation_details() -> None:
953	    assert flag_weight({"category": "correctness", "concern": "The schema field is wrong"}) == 0.5
954	    assert flag_weight({"category": "security", "concern": "The schema field is wrong"}) == 3.0
955	
956	
957	def test_compute_plan_delta_percent_handles_none() -> None:
958	    assert compute_plan_delta_percent(None, "x") is None
959	    assert compute_plan_delta_percent("same", "same") == 0.0
960	
961	
962	def test_compute_recurring_critiques_detects_overlap(tmp_path: Path) -> None:
963	    plan_dir = tmp_path / "plan"
964	    plan_dir.mkdir()
965	    _write_json(plan_dir / "critique_v1.json", {"flags": [{"concern": "Same issue"}]})
966	    _write_json(plan_dir / "critique_v2.json", {"flags": [{"concern": "same issue"}]})
967	    assert compute_recurring_critiques(plan_dir, 2) == ["same issue"]
968	
969	
970	def test_build_gate_signals_includes_loop_summary_and_previous_version_lookup(tmp_path: Path) -> None:
971	    flags = [
972	        {
973	            "id": "FLAG-001",
974	            "concern": "Missing verification command",
975	            "category": "correctness",
976	            "severity_hint": "likely-significant",
977	            "evidence": "No test listed",
978	            "status": "open",
979	            "severity": "significant",
980	            "verified": False,
981	            "raised_in": "critique_v2.json",
982	        }
983	    ]
984	    plan_dir, state = _scaffold(tmp_path, iteration=2, flags=flags)
985	    result = build_gate_signals(plan_dir, state)
986	    assert result["robustness"] == "standard"
987	    assert result["signals"]["weighted_score"] == 2.0
988	    assert result["signals"]["plan_delta_from_previous"] is not None
989	    assert result["signals"]["recurring_critiques"] == ["same issue"]
990	    assert "Weighted score trajectory" in result["signals"]["loop_summary"]
991	
992	
993	def test_build_gate_signals_emits_scope_creep_and_high_iteration_warnings(tmp_path: Path) -> None:
994	    flags = [
995	        {
996	            "id": "FLAG-007",
997	            "concern": "Scope creep: plan now rewrites the entire app",
998	            "category": "other",
999	            "severity_hint": "likely-significant",
1000	            "evidence": "expanded scope",
1001	            "status": "open",
1002	            "severity": "significant",
1003	            "verified": False,
1004	            "raised_in": "critique_v12.json",
1005	        }
1006	    ]
1007	    plan_dir, state = _scaffold(tmp_path, iteration=12, flags=flags)
1008	    state["config"]["robustness"] = "standard"
1009	    result = build_gate_signals(plan_dir, state)
1010	    assert any("Scope creep detected" in warning for warning in result["warnings"])
1011	    assert any("hard iteration limit reached" in warning for warning in result["warnings"])
1012
```

> AGENT

Now let me look at more test files to understand fixture patterns better:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/tests/test_core.py",
  "offset": 1,
  "limit": 200
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	import pytest
4	
5	from megaplan._core import (
6	    add_or_increment_debt,
7	    batch_artifact_path,
8	    compute_global_batches,
9	    compute_task_batches,
10	    escalated_subsystems,
11	    extract_subsystem_tag,
12	    find_matching_debt,
13	    list_batch_artifacts,
14	    load_debt_registry,
15	    resolve_debt,
16	)
17	
18	
19	def _task(task_id: str, depends_on: list[str] | None = None) -> dict[str, object]:
20	    return {"id": task_id, "depends_on": depends_on or []}
21	
22	
23	def test_compute_task_batches_linear_chain() -> None:
24	    tasks = [_task("T1"), _task("T2", ["T1"]), _task("T3", ["T2"])]
25	    assert compute_task_batches(tasks) == [["T1"], ["T2"], ["T3"]]
26	
27	
28	def test_compute_task_batches_independent_tasks_share_batch() -> None:
29	    tasks = [_task("T1"), _task("T2"), _task("T3")]
30	    assert compute_task_batches(tasks) == [["T1", "T2", "T3"]]
31	
32	
33	def test_compute_task_batches_diamond_graph() -> None:
34	    tasks = [
35	        _task("T1"),
36	        _task("T2", ["T1"]),
37	        _task("T3", ["T1"]),
38	        _task("T4", ["T2", "T3"]),
39	    ]
40	    assert compute_task_batches(tasks) == [["T1"], ["T2", "T3"], ["T4"]]
41	
42	
43	def test_compute_task_batches_cycle_raises() -> None:
44	    tasks = [_task("T1", ["T2"]), _task("T2", ["T1"])]
45	    with pytest.raises(ValueError, match="Cyclic dependency graph"):
46	        compute_task_batches(tasks)
47	
48	
49	def test_compute_task_batches_unknown_dependency_raises() -> None:
50	    with pytest.raises(ValueError, match="Unknown dependency ID 'T9'"):
51	        compute_task_batches([_task("T1", ["T9"])])
52	
53	
54	def test_compute_task_batches_empty_input_returns_empty_list() -> None:
55	    assert compute_task_batches([]) == []
56	
57	
58	def test_compute_task_batches_completed_ids_satisfy_pending_dependencies() -> None:
59	    tasks = [_task("T2", ["T1"])]
60	    assert compute_task_batches(tasks, completed_ids={"T1"}) == [["T2"]]
61	
62	
63	def test_compute_task_batches_completed_ids_allow_parallel_pending_tasks() -> None:
64	    tasks = [_task("T2", ["T1"]), _task("T3", ["T1"])]
65	    assert compute_task_batches(tasks, completed_ids={"T1"}) == [["T2", "T3"]]
66	
67	
68	def test_batch_artifact_path_returns_expected_path(tmp_path) -> None:
69	    assert batch_artifact_path(tmp_path, 3) == tmp_path / "execution_batch_3.json"
70	
71	
72	def test_list_batch_artifacts_returns_sorted_existing_paths(tmp_path) -> None:
73	    batch_three = tmp_path / "execution_batch_3.json"
74	    batch_one = tmp_path / "execution_batch_1.json"
75	    batch_two = tmp_path / "execution_batch_2.json"
76	    for path in (batch_three, batch_one, batch_two):
77	        path.write_text("{}", encoding="utf-8")
78	    (tmp_path / "execution_batch_notes.json").write_text("{}", encoding="utf-8")
79	
80	    assert list_batch_artifacts(tmp_path) == [batch_one, batch_two, batch_three]
81	
82	
83	def test_compute_global_batches_ignores_completed_status_for_stable_partition() -> None:
84	    finalize_data = {
85	        "tasks": [
86	            {"id": "T1", "status": "done", "depends_on": []},
87	            {"id": "T2", "status": "pending", "depends_on": ["T1"]},
88	            {"id": "T3", "status": "skipped", "depends_on": ["T1"]},
89	            {"id": "T4", "status": "pending", "depends_on": ["T2", "T3"]},
90	        ]
91	    }
92	
93	    assert compute_global_batches(finalize_data) == [["T1"], ["T2", "T3"], ["T4"]]
94	
95	
96	def test_load_debt_registry_returns_empty_when_missing(tmp_path) -> None:
97	    assert load_debt_registry(tmp_path) == {"entries": []}
98	
99	
100	def test_add_or_increment_debt_creates_new_entry() -> None:
101	    registry = {"entries": []}
102	
103	    entry = add_or_increment_debt(
104	        registry,
105	        subsystem="Timeout Recovery",
106	        concern="Timeout recovery: Retry backoff is missing",
107	        flag_ids=["FLAG-001"],
108	        plan_id="plan-a",
109	    )
110	
111	    assert entry["id"] == "DEBT-001"
112	    assert entry["subsystem"] == "timeout-recovery"
113	    assert entry["concern"] == "timeout recovery: retry backoff is missing"
114	    assert entry["flag_ids"] == ["FLAG-001"]
115	    assert entry["plan_ids"] == ["plan-a"]
116	    assert entry["occurrence_count"] == 1
117	    assert entry["resolved"] is False
118	
119	
120	def test_add_or_increment_debt_increments_matching_entry() -> None:
121	    registry = {"entries": []}
122	    first = add_or_increment_debt(
123	        registry,
124	        subsystem="timeout-recovery",
125	        concern="Timeout recovery: Retry backoff is missing",
126	        flag_ids=["FLAG-001"],
127	        plan_id="plan-a",
128	    )
129	
130	    second = add_or_increment_debt(
131	        registry,
132	        subsystem="timeout-recovery",
133	        concern="Timeout recovery: retry backoff is missing",
134	        flag_ids=["FLAG-002"],
135	        plan_id="plan-b",
136	    )
137	
138	    assert second is first
139	    assert len(registry["entries"]) == 1
140	    assert second["occurrence_count"] == 2
141	    assert second["flag_ids"] == ["FLAG-001", "FLAG-002"]
142	    assert second["plan_ids"] == ["plan-a", "plan-b"]
143	
144	
145	def test_find_matching_debt_rejects_different_subsystem_even_with_overlap() -> None:
146	    registry = {"entries": []}
147	    add_or_increment_debt(
148	        registry,
149	        subsystem="timeout-recovery",
150	        concern="Timeout recovery: Retry backoff is missing",
151	        flag_ids=["FLAG-001"],
152	        plan_id="plan-a",
153	    )
154	
155	    assert find_matching_debt(
156	        registry,
157	        "execute-paths",
158	        "Timeout recovery: Retry backoff is missing",
159	    ) is None
160	
161	
162	@pytest.mark.parametrize(
163	    ("concern", "expected"),
164	    [
165	        ("Timeout recovery: Retry backoff is missing", "timeout-recovery"),
166	        ("Retry backoff is missing", "untagged"),
167	        ("Execute paths: queue: drain edge case", "execute-paths"),
168	    ],
169	)
170	def test_extract_subsystem_tag_handles_expected_variants(concern: str, expected: str) -> None:
171	    assert extract_subsystem_tag(concern) == expected
172	
173	
174	def test_resolve_debt_sets_resolution_fields() -> None:
175	    registry = {"entries": []}
176	    entry = add_or_increment_debt(
177	        registry,
178	        subsystem="observation",
179	        concern="Observation: Missing event logging",
180	        flag_ids=["FLAG-010"],
181	        plan_id="plan-a",
182	    )
183	
184	    resolved = resolve_debt(registry, entry["id"], "plan-b")
185	
186	    assert resolved["resolved"] is True
187	    assert resolved["resolved_by"] == "plan-b"
188	    assert resolved["resolved_at"] is not None
189	    assert resolved["updated_at"] == resolved["resolved_at"]
190	
191	
192	def test_escalated_subsystems_triggers_for_single_high_occurrence_entry() -> None:
193	    registry = {"entries": []}
194	    entry = add_or_increment_debt(
195	        registry,
196	        subsystem="timeout-recovery",
197	        concern="Timeout recovery: Retry backoff is missing",
198	        flag_ids=["FLAG-001"],
199	        plan_id="plan-a",
200	    )
```

> AGENT

Now let me check another test file to see more fixture patterns:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def test_\" /Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py | head -30"
}
```

> TOOL

tool_result Bash
```
235:def test_init_sets_last_gate_and_next_step_plan(plan_fixture: PlanFixture) -> None:
241:def test_init_includes_next_step_runtime(plan_fixture: PlanFixture) -> None:
253:def test_init_response_points_to_next_step_by_robustness(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
291:def test_infer_next_steps_matches_new_state_machine() -> None:
296:def test_workflow_next_matches_legacy_partial_state_cases() -> None:
326:def test_workflow_next_light_robustness_overrides(state: dict[str, object], expected: list[str]) -> None:
330:def test_workflow_definition_is_complete_for_standard_flow() -> None:
348:def test_workflow_walk_matches_documented_standard_flow() -> None:
388:def test_workflow_walk_matches_documented_robust_flow() -> None:
432:def test_workflow_walk_matches_documented_light_flow() -> None:
451:def test_all_robustness_levels_route_planned_to_critique() -> None:
460:def test_handle_plan_sets_and_clears_active_step(
493:def test_handle_plan_failure_clears_active_step(
515:def test_clear_active_step_ignores_mismatched_run_id() -> None:
526:def test_tiny_critique_stub_does_not_leak_active_step(
540:def test_capture_test_baseline_success(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
568:def test_capture_test_baseline_no_runner(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
579:def test_capture_test_baseline_timeout(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
594:def test_handle_status_reports_observability_fields(plan_fixture: PlanFixture) -> None:
648:def test_handle_status_uses_execute_runtime_guidance(plan_fixture: PlanFixture) -> None:
668:def test_handle_status_includes_progress_when_finalize_exists(plan_fixture: PlanFixture) -> None:
686:def test_handle_status_distinguishes_lock_file_from_held_lock(plan_fixture: PlanFixture) -> None:
698:def test_handle_watch_combines_status_and_progress(plan_fixture: PlanFixture) -> None:
710:def test_phase_progress_summary_completion_only(plan_fixture: PlanFixture) -> None:
726:def test_phase_progress_summary_stale(plan_fixture: PlanFixture) -> None:
741:def test_plan_rerun_keeps_iteration_and_uses_same_iteration_subversion(plan_fixture: PlanFixture) -> None:
756:def test_override_add_note_includes_next_step_runtime(plan_fixture: PlanFixture) -> None:
770:def test_handle_plan_includes_next_step_runtime(plan_fixture: PlanFixture) -> None:
778:def test_build_monitor_hint_references_status(plan_fixture: PlanFixture) -> None:
785:def test_format_duration_hint_uses_human_readable_ranges() -> None:
[rerun: b2]
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py",
  "offset": 1,
  "limit": 250
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	import json
4	import subprocess
5	import sys
6	import time
7	from argparse import Namespace
8	from dataclasses import dataclass
9	from datetime import datetime, timedelta, timezone
10	from pathlib import Path
11	from typing import Callable
12	
13	import pytest
14	
15	import megaplan
16	import megaplan.cli
17	import megaplan.execution
18	import megaplan.evaluation
19	import megaplan.handlers
20	import megaplan.cli
21	import megaplan._core
22	import megaplan._core.io as io_module
23	import megaplan.workers
24	from megaplan.evaluation import PLAN_STRUCTURE_REQUIRED_STEP_ISSUE, validate_plan_structure
25	from megaplan._core import (
26	    WORKFLOW,
27	    _ROBUSTNESS_OVERRIDES,
28	    clear_active_step,
29	    ensure_runtime_layout,
30	    load_plan,
31	    set_active_step,
32	    workflow_next,
33	)
34	from megaplan.prompts import create_claude_prompt
35	from megaplan.types import STATE_PREPPED
36	from megaplan.workers import WorkerResult, _build_mock_payload
37	
38	
39	def read_json(path: Path) -> dict:
40	    return json.loads(path.read_text(encoding="utf-8"))
41	
42	
43	def run_main_json(
44	    argv: list[str],
45	    *,
46	    cwd: Path,
47	    capsys: pytest.CaptureFixture[str],
48	    monkeypatch: pytest.MonkeyPatch,
49	) -> tuple[int, dict]:
50	    monkeypatch.chdir(cwd)
51	    exit_code = megaplan.main(argv)
52	    return exit_code, json.loads(capsys.readouterr().out)
53	
54	
55	def _write_lines(path: Path, count: int, *, prefix: str = "line") -> None:
56	    path.parent.mkdir(parents=True, exist_ok=True)
57	    path.write_text("\n".join(f"{prefix}_{index}" for index in range(count)) + "\n", encoding="utf-8")
58	
59	
60	def make_args_factory(project_dir: Path) -> Callable[..., Namespace]:
61	    def make_args(**overrides: object) -> Namespace:
62	        data = {
63	            "plan": None,
64	            "idea": "test idea",
65	            "name": "test-plan",
66	            "project_dir": str(project_dir),
67	            "auto_approve": None,
68	            "robustness": None,
69	            "agent": None,
70	            "ephemeral": False,
71	            "fresh": False,
72	            "persist": False,
73	            "confirm_destructive": True,
74	            "user_approved": False,
75	            "confirm_self_review": False,
76	            "batch": None,
77	            "override_action": None,
78	            "note": None,
79	            "reason": "",
80	            "robustness": None,
81	        }
82	        data.update(overrides)
83	        return Namespace(**data)
84	
85	    return make_args
86	
87	
88	@dataclass
89	class PlanFixture:
90	    root: Path
91	    project_dir: Path
92	    plan_name: str
93	    plan_dir: Path
94	    make_args: Callable[..., Namespace]
95	
96	
97	def _make_plan_fixture_with_robustness(
98	    tmp_path: Path,
99	    monkeypatch: pytest.MonkeyPatch,
100	    *,
101	    robustness: str,
102	) -> PlanFixture:
103	    root = tmp_path / "root"
104	    project_dir = tmp_path / "project"
105	    config_path = tmp_path / "config"
106	    root.mkdir()
107	    project_dir.mkdir()
108	    (project_dir / ".git").mkdir()
109	
110	    def _config_dir(home: Path | None = None) -> Path:
111	        del home
112	        return config_path
113	
114	    monkeypatch.setenv(megaplan.MOCK_ENV_VAR, "1")
115	    monkeypatch.setattr(
116	        megaplan._core.shutil,
117	        "which",
118	        lambda name: "/usr/bin/mock" if name in {"claude", "codex"} else None,
119	    )
120	    monkeypatch.setattr(io_module, "config_dir", _config_dir)
121	    monkeypatch.setattr(megaplan.cli, "config_dir", _config_dir)
122	
123	    make_args = make_args_factory(project_dir)
124	    response = megaplan.handle_init(root, make_args(robustness=robustness))
125	    plan_name = response["plan"]
126	    return PlanFixture(
127	        root=root,
128	        project_dir=project_dir,
129	        plan_name=plan_name,
130	        plan_dir=megaplan.plans_root(root) / plan_name,
131	        make_args=make_args,
132	    )
133	
134	
135	@pytest.fixture
136	def plan_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> PlanFixture:
137	    return _make_plan_fixture_with_robustness(tmp_path, monkeypatch, robustness="standard")
138	
139	
140	def load_state(plan_dir: Path) -> dict:
141	    return read_json(plan_dir / "state.json")
142	
143	
144	def latest_plan_name(plan_dir: Path) -> str:
145	    return load_state(plan_dir)["plan_versions"][-1]["file"]
146	
147	
148	def debt_registry_path(root: Path) -> Path:
149	    return root / ".megaplan" / "debt.json"
150	
151	
152	def first_open_significant_flag(plan_dir: Path) -> dict:
153	    registry = read_json(plan_dir / "faults.json")
154	    return next(
155	        flag
156	        for flag in registry["flags"]
157	        if flag["status"] in {"open", "disputed"} and flag.get("severity") == "significant"
158	    )
159	
160	
161	def open_blocking_flags(plan_dir: Path) -> list[dict]:
162	    registry = read_json(plan_dir / "faults.json")
163	    return [
164	        flag
165	        for flag in registry["flags"]
166	        if flag["status"] in {"open", "disputed"}
167	        and flag.get("severity") in {"significant", "likely-significant"}
168	    ]
169	
170	
171	def ensure_blocking_flags(plan_dir: Path, count: int) -> list[dict]:
172	    registry = read_json(plan_dir / "faults.json")
173	    flags = [
174	        flag
175	        for flag in registry["flags"]
176	        if flag["status"] in {"open", "disputed"}
177	        and flag.get("severity") in {"significant", "likely-significant"}
178	    ]
179	    if not flags:
180	        raise AssertionError("expected at least one blocking flag in the fixture")
181	    template = flags[0]
182	    next_index = 1
183	    while len(flags) < count:
184	        clone = dict(template)
185	        clone["id"] = f"{template['id']}-extra-{next_index}"
186	        clone["concern"] = f"{template['concern']} (extra {next_index})"
187	        registry["flags"].append(clone)
188	        flags.append(clone)
189	        next_index += 1
190	    for extra in flags[count:]:
191	        extra["severity"] = "minor"
192	    (plan_dir / "faults.json").write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
193	    return open_blocking_flags(plan_dir)
194	
195	
196	def make_gate_worker_result(
197	    *,
198	    recommendation: str,
199	    rationale: str,
200	    signals_assessment: str,
201	    flag_resolutions: list[dict] | None = None,
202	    accepted_tradeoffs: list[dict] | None = None,
203	    session_id: str,
204	) -> WorkerResult:
205	    return WorkerResult(
206	        payload={
207	            "recommendation": recommendation,
208	            "rationale": rationale,
209	            "signals_assessment": signals_assessment,
210	            "warnings": [],
211	            "settled_decisions": [],
212	            "flag_resolutions": flag_resolutions or [],
213	            "accepted_tradeoffs": accepted_tradeoffs or [],
214	        },
215	        raw_output="{}",
216	        duration_ms=1,
217	        cost_usd=0.0,
218	        session_id=session_id,
219	    )
220	
221	
222	def make_worker_sequence(
223	    results: list[tuple[WorkerResult, str, str, bool]],
224	    call_counter: dict[str, int],
225	) -> Callable[..., tuple[WorkerResult, str, str, bool]]:
226	    iterator = iter(results)
227	
228	    def _run_step_with_worker(*args, **kwargs):
229	        call_counter["count"] += 1
230	        return next(iterator)
231	
232	    return _run_step_with_worker
233	
234	
235	def test_init_sets_last_gate_and_next_step_plan(plan_fixture: PlanFixture) -> None:
236	    state = load_state(plan_fixture.plan_dir)
237	    assert state["current_state"] == megaplan.STATE_INITIALIZED
238	    assert state["last_gate"] == {}
239	
240	
241	def test_init_includes_next_step_runtime(plan_fixture: PlanFixture) -> None:
242	    response = megaplan.handle_init(
243	        plan_fixture.root,
244	        plan_fixture.make_args(name="runtime-test"),
245	    )
246	
247	    assert response["next_step"] == "plan"
248	    assert response["next_step_runtime"]["expected_duration_seconds"]["min"] == 60
249	    assert response["next_step_runtime"]["recommended_next_check_seconds"] == 120
250	    assert "Expected duration:" in response["next_step_runtime"]["duration_hint"]
```

> AGENT

Let me search for more specific testing patterns around handlers and state dictionaries:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"def _state\\|def _build_\\|def _scaffold\\|def _write_json\" /Users/user_c042661f/Documents/megaplan/tests/test_*.py | head -40"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/tests/test_evaluation.py:30:def _write_json(path: Path, data: dict[str, object]) -> None:
/Users/user_c042661f/Documents/megaplan/tests/test_evaluation.py:35:def _state(tmp_path: Path, *, iteration: int = 1, robustness: str = "standard") -> dict[str, object]:
/Users/user_c042661f/Documents/megaplan/tests/test_evaluation.py:88:def _scaffold(tmp_path: Path, *, iteration: int = 1, flags: list[dict[str, object]] | None = None) -> tuple[Path, dict[str, object]]:
/Users/user_c042661f/Documents/megaplan/tests/test_parallel_critique.py:24:def _state(project_dir: Path, *, iteration: int = 1) -> PlanState:
/Users/user_c042661f/Documents/megaplan/tests/test_parallel_critique.py:59:def _scaffold(tmp_path: Path, *, iteration: int = 1) -> tuple[Path, Path, PlanState]:
/Users/user_c042661f/Documents/megaplan/tests/test_parallel_review.py:21:def _state(project_dir: Path, *, iteration: int = 1) -> PlanState:
/Users/user_c042661f/Documents/megaplan/tests/test_parallel_review.py:56:def _scaffold(tmp_path: Path, *, iteration: int = 1) -> tuple[Path, Path, PlanState]:
/Users/user_c042661f/Documents/megaplan/tests/test_prompts.py:41:def _state(project_dir: Path, *, iteration: int = 1) -> PlanState:
/Users/user_c042661f/Documents/megaplan/tests/test_prompts.py:76:def _scaffold(tmp_path: Path, *, iteration: int = 1) -> tuple[Path, PlanState]:
/Users/user_c042661f/Documents/megaplan/tests/test_review_mechanical.py:20:def _state(project_dir: Path) -> dict[str, object]:
[rerun: b3]
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/tests/test_parallel_critique.py",
  "offset": 1,
  "limit": 150
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	import copy
4	import json
5	import sys
6	import time
7	from pathlib import Path
8	from types import ModuleType
9	
10	import pytest
11	
12	from megaplan._core import atomic_write_json, atomic_write_text, read_json, schemas_root
13	from megaplan.checks import checks_for_robustness
14	from megaplan.hermes_worker import parse_agent_output
15	from megaplan.parallel_critique import _run_check, run_parallel_critique
16	from megaplan.prompts.critique import write_single_check_template
17	from megaplan.types import PlanState
18	from megaplan.workers import STEP_SCHEMA_FILENAMES
19	
20	
21	REPO_ROOT = Path(__file__).resolve().parents[1]
22	
23	
24	def _state(project_dir: Path, *, iteration: int = 1) -> PlanState:
25	    return {
26	        "name": "test-plan",
27	        "idea": "parallelize critique",
28	        "current_state": "planned",
29	        "iteration": iteration,
30	        "created_at": "2026-04-01T00:00:00Z",
31	        "config": {
32	            "project_dir": str(project_dir),
33	            "auto_approve": False,
34	            "robustness": "standard",
35	        },
36	        "sessions": {},
37	        "plan_versions": [
38	            {
39	                "version": iteration,
40	                "file": f"plan_v{iteration}.md",
41	                "hash": "sha256:test",
42	                "timestamp": "2026-04-01T00:00:00Z",
43	            }
44	        ],
45	        "history": [],
46	        "meta": {
47	            "significant_counts": [],
48	            "weighted_scores": [],
49	            "plan_deltas": [],
50	            "recurring_critiques": [],
51	            "total_cost_usd": 0.0,
52	            "overrides": [],
53	            "notes": [],
54	        },
55	        "last_gate": {},
56	    }
57	
58	
59	def _scaffold(tmp_path: Path, *, iteration: int = 1) -> tuple[Path, Path, PlanState]:
60	    plan_dir = tmp_path / "plan"
61	    project_dir = tmp_path / "project"
62	    plan_dir.mkdir()
63	    project_dir.mkdir()
64	    (project_dir / ".git").mkdir()
65	    state = _state(project_dir, iteration=iteration)
66	    atomic_write_text(plan_dir / f"plan_v{iteration}.md", "# Plan\nDo it.\n")
67	    atomic_write_json(
68	        plan_dir / f"plan_v{iteration}.meta.json",
69	        {
70	            "version": iteration,
71	            "timestamp": "2026-04-01T00:00:00Z",
72	            "hash": "sha256:test",
73	            "success_criteria": [{"criterion": "criterion", "priority": "must"}],
74	            "questions": [],
75	            "assumptions": [],
76	        },
77	    )
78	    atomic_write_json(plan_dir / "faults.json", {"flags": []})
79	    return plan_dir, project_dir, state
80	
81	
82	def _critique_schema() -> dict:
83	    return read_json(schemas_root(REPO_ROOT) / STEP_SCHEMA_FILENAMES["critique"])
84	
85	
86	def _finding(detail: str, *, flagged: bool) -> dict[str, object]:
87	    return {"detail": detail, "flagged": flagged}
88	
89	
90	def _check_payload(check: dict[str, str], detail: str, *, flagged: bool = False) -> dict[str, object]:
91	    return {
92	        "id": check["id"],
93	        "question": check["question"],
94	        "findings": [_finding(detail, flagged=flagged)],
95	    }
96	
97	
98	def test_run_parallel_critique_merges_in_original_order(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
99	    plan_dir, _project_dir, state = _scaffold(tmp_path)
100	    checks = checks_for_robustness("standard")
101	
102	    def fake_run_check(index: int, check: dict[str, str], **kwargs: object):
103	        del kwargs
104	        if index == 0:
105	            time.sleep(0.05)
106	        return (
107	            index,
108	            _check_payload(check, f"Checked {check['id']} in detail for ordered merge coverage.", flagged=False),
109	            [f"FLAG-00{index + 1}"],
110	            [],
111	            0.25, 0, 0, 0,
112	        )
113	
114	    monkeypatch.setattr("megaplan.parallel_critique._run_check", fake_run_check)
115	
116	    result = run_parallel_critique(state, plan_dir, root=REPO_ROOT, model="mock-model", checks=checks)
117	
118	    assert [check["id"] for check in result.payload["checks"]] == [check["id"] for check in checks]
119	    assert result.payload["flags"] == []
120	    assert result.payload["verified_flag_ids"] == [f"FLAG-{index:03d}" for index in range(1, len(checks) + 1)]
121	    assert result.payload["disputed_flag_ids"] == []
122	
123	
124	def test_run_parallel_critique_disputed_flags_override_verified(
125	    monkeypatch: pytest.MonkeyPatch,
126	    tmp_path: Path,
127	) -> None:
128	    plan_dir, _project_dir, state = _scaffold(tmp_path)
129	    checks = checks_for_robustness("standard")
130	
131	    def fake_run_check(index: int, check: dict[str, str], **kwargs: object):
132	        del kwargs
133	        verified = ["FLAG-001"] if index == 0 else []
134	        disputed = ["FLAG-001"] if index == 1 else []
135	        return (
136	            index,
137	            _check_payload(check, f"Checked {check['id']} with explicit flag merge coverage.", flagged=index == 1),
138	            verified,
139	            disputed,
140	            0.1,
141	            0, 0, 0,
142	        )
143	
144	    monkeypatch.setattr("megaplan.parallel_critique._run_check", fake_run_check)
145	
146	    result = run_parallel_critique(state, plan_dir, root=REPO_ROOT, model="mock-model", checks=checks[:2])
147	
148	    assert result.payload["disputed_flag_ids"] == ["FLAG-001"]
149	    assert "FLAG-001" not in result.payload["verified_flag_ids"]
150
```

> AGENT

Now let me search for usage of `_build_mock_payload` and other handler testing patterns:

> TOOL

tool_use Bash
```json
{
  "command": "grep -A 10 \"_build_mock_payload\" /Users/user_c042661f/Documents/megaplan/tests/test_evaluation.py | head -30"
}
```

> TOOL

tool_result Bash
```
from megaplan.workers import _build_mock_payload


def _write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _state(tmp_path: Path, *, iteration: int = 1, robustness: str = "standard") -> dict[str, object]:
    previous_version = iteration - 1
    return {
--
    gate_payload = _build_mock_payload(
        "gate",
        state,
        plan_dir,
        settled_decisions=[
            {
                "id": "DECISION-001",
                "decision": "Reviewer must respect the softened FLAG-006 behavior.",
                "rationale": "This was approved at gate time.",
            }
        ],
[rerun: b4]
```

> AGENT

Let me look at the actual _build_mock_payload function:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"_build_mock_payload\" /Users/user_c042661f/Documents/megaplan/src/megaplan/workers.py"
}
```

> TOOL

tool_result Bash
```
Exit code 2
grep: /Users/user_c042661f/Documents/megaplan/src/megaplan/workers.py: No such file or directory
[rerun: b5]
```

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan -name \"workers.py\" -type f"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/workers.py
[rerun: b6]
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -A 20 \"def _build_mock_payload\" /Users/user_c042661f/Documents/megaplan/megaplan/workers.py"
}
```

> TOOL

tool_result Bash
```
def _build_mock_payload(step: str, state: dict[str, Any], plan_dir: Path, **overrides: Any) -> dict[str, Any]:
    builder = _MOCK_DEFAULTS.get(step)
    if builder is None:
        raise CliError("unsupported_step", f"Mock worker does not support '{step}'")
    prompt_override = overrides.pop("prompt_override", None)
    if step in _EXECUTE_STEPS:
        if step == "loop_execute":
            return _deep_merge(_default_mock_loop_execute_payload(state, plan_dir, prompt_override=prompt_override), overrides)
        return _deep_merge(_default_mock_execute_payload(state, plan_dir, prompt_override=prompt_override), overrides)
    return _deep_merge(builder(state, plan_dir), overrides)


def _mock_plan(state: PlanState, plan_dir: Path) -> WorkerResult:
    return _mock_result(_build_mock_payload("plan", state, plan_dir))


def _mock_prep(state: PlanState, plan_dir: Path) -> WorkerResult:
    return _mock_result(_build_mock_payload("prep", state, plan_dir))


def _mock_loop_plan(state: PlanState, plan_dir: Path) -> WorkerResult:
[rerun: b7]
```

> AGENT

Now let me check the execution_timeout function:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"execution_timeout\\|_write_finalize_artifacts\" /Users/user_c042661f/Documents/megaplan/megaplan/execution.py"
}
```

> TOOL

tool_result Bash
```
36:from megaplan.execution_timeout import (
[rerun: b8]
```

> TOOL

tool_use Bash
```json
{
  "command": "find /Users/user_c042661f/Documents/megaplan -name \"*timeout*\" -o -name \"*finalize*\" | grep -E \"\\.(py|json)$\""
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/megaplan/megaplan/execution_timeout.py
/Users/user_c042661f/Documents/megaplan/megaplan/prompts/finalize.py
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/five-improvements-to-the-20260325-0450/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/update-main-py-to-print-the-20260410-0320/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/update-main-py-to-print-the-20260410-0320/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/persistent-tech-debt-registry-20260325-2007/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/design-and-implement-a-20260327-0512/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/redesign-the-orchestrator-20260406-1943/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/redesign-the-orchestrator-20260406-1943/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/fix-the-6-remaining-openai-20260409-0502/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/fix-the-6-remaining-openai-20260409-0502/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/standard-review-lift/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/standard-review-lift/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/update-main-py-to-print-the-20260410-0328/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/update-main-py-to-print-the-20260410-0328/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/quality-gates-and-prompt-20260325-0536/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-flux-2-klein-4b-and-9b-20260413-0100/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-flux-2-klein-4b-and-9b-20260413-0100/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/agent-driven-incremental-20260325-0500/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/megaplan-observability-and-20260410-0134/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/megaplan-observability-and-20260410-0134/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/codex-subagent-live-test-20260410-0228/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/codex-subagent-live-test-20260410-0228/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/refactor-the-finalize-execute-20260323-0621/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/set-up-proper-defaults-and-20260406-2002/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/set-up-proper-defaults-and-20260406-2002/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/move-the-entry-page-into-20260401-0450/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/move-the-entry-page-into-20260401-0450/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/consolidate-execute-paths-and-20260325-1906/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-safe-phase-start-notices-20260410-1525/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-safe-phase-start-notices-20260410-1525/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/eliminate-the-duplication-20260406-1943/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/eliminate-the-duplication-20260406-1943/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/clean-up-and-properly-20260331-0149/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-two-injection-mechanisms-20260406-1904/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-two-injection-mechanisms-20260406-1904/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/refactor-megaplan-skill-so-20260406-1818/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/refactor-megaplan-skill-so-20260406-1818/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/clean-up-handler-complexity-20260325-0417/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-a-plan-template-and-20260323-0708/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/robust-review-v2/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/robust-review-v2/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-a-new-tiny-robustness-20260408-0318/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-a-new-tiny-robustness-20260408-0318/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/incremental-execution-20260325-0440/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/design-and-implement-the-note-20260406-1943/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/design-and-implement-the-note-20260406-1943/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/execution-visibility-and-20260325-1632/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/make-all-defaults-in-the-20260406-2140/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/make-all-defaults-in-the-20260406-2140/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-a-megaplan-step-cli-20260323-0801/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/batched-sub-agent-execution-20260325-0617/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-flux-2-klein-4b-and-9b-20260413-0135/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-flux-2-klein-4b-and-9b-20260413-0135/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/fix-megaplan-s-planning-20260409-2103/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/fix-megaplan-s-planning-20260409-2103/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/v0-14-0-strict-flag-20260415-0530/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/v0-14-0-strict-flag-20260415-0530/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/consolidate-all-user-facing-20260406-2113/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/consolidate-all-user-facing-20260406-2113/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/update-all-documentation-20260406-1902/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/update-all-documentation-20260406-1902/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/build-megaloop-a-minimal-20260327-0250/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/harden-megaplan-review-and-20260323-2148/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/re-implement-settable-20260406-2209/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/re-implement-settable-20260406-2209/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-test-baselining-to-the-20260410-2059/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-test-baselining-to-the-20260410-2059/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/codex-flow-test-20260410-0227/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/codex-flow-test-20260410-0227/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-config-backed-defaults-20260408-0303/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-config-backed-defaults-20260408-0303/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-test-baselining-to-the-20260410-2240/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-test-baselining-to-the-20260410-2240/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/harden-the-execute-review-20260325-0320/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/parallelize-the-critique-20260401-1840/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/parallelize-the-critique-20260401-1840/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/update-readme-md-and-the-20260406-2156/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/update-readme-md-and-the-20260406-2156/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-tier-based-critique-check-20260331-1521/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-tier-based-critique-check-20260331-1521/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/between-batch-quality-trip-20260325-2008/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/smoke-test-add-a-one-line-20260409-1454/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/smoke-test-add-a-one-line-20260409-1454/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/refactor-megaplan-workflow-20260326-0151/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/implement-v0-15-0-doc-mode-20260415-0942/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/implement-v0-15-0-doc-mode-20260415-0942/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-simple-observability-for-20260406-2015/finalize.json
/Users/user_c042661f/Documents/megaplan/.megaplan/plans/add-simple-observability-for-20260406-2015/finalize_snapshot.json
/Users/user_c042661f/Documents/megaplan/.megaplan/schemas/finalize.json
[rerun: b9]
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execution_timeout.py",
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
46	    mode: str = "code",
47	) -> list[str]:
48	    reset_reasons: dict[str, list[str]] = {}
49	    if mode == "doc":
50	        missing_task_ids = _check_done_task_evidence(
51	            finalize_data.get("tasks", []),
52	            issues=issues,
53	            should_classify=lambda task: True,
54	            has_evidence=lambda task: bool(task.get("sections_written")),
55	            has_advisory_evidence=lambda task: True,
56	            missing_message="Done tasks missing sections_written during timeout recovery: ",
57	            advisory_message="",
58	        )
59	    else:
60	        missing_task_ids = _check_done_task_evidence(
61	            finalize_data.get("tasks", []),
62	            issues=issues,
63	            should_classify=lambda task: True,
64	            has_evidence=lambda task: bool(task.get("files_changed")),
65	            has_advisory_evidence=lambda task: bool(task.get("commands_run")),
66	            missing_message="Done tasks missing both files_changed and commands_run during timeout recovery: ",
67	            advisory_message="Advisory: done tasks rely on commands_run without files_changed during timeout recovery: ",
68	        )
69	    for task_id in missing_task_ids:
70	        if mode == "doc":
71	            reset_reasons.setdefault(task_id, []).append("missing sections_written")
72	        else:
73	            reset_reasons.setdefault(task_id, []).append(
74	                "missing both files_changed and commands_run"
75	            )
76	
77	    if mode != "doc" and not execution_audit.get("skipped"):
78	        files_in_diff = {
79	            _normalize_execute_claimed_path(path)
80	            for path in execution_audit.get("files_in_diff", [])
81	            if isinstance(path, str) and path.strip()
82	        }
83	        for task in finalize_data.get("tasks", []):
84	            if task.get("status") != "done":
85	                continue
86	            claimed_paths = [
87	                _normalize_execute_claimed_path(path)
88	                for path in task.get("files_changed", [])
89	                if isinstance(path, str) and path.strip()
90	            ]
91	            if claimed_paths and any(
92	                path not in files_in_diff for path in claimed_paths
93	            ):
94	                reset_reasons.setdefault(task["id"], []).append(
95	                    "claimed files not present in git status"
96	                )
97	
98	    for task in finalize_data.get("tasks", []):
99	        reasons = reset_reasons.get(task.get("id"))
100	        if not reasons:
```

> AGENT

Let me check for tests that call handlers directly:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"handle_\\|Handler\\|def test_\" /Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py | grep -A 2 \"def test_handle\" | head -50"
}
```

> TOOL

tool_result Bash
```
460:def test_handle_plan_sets_and_clears_active_step(
485:    megaplan.handle_plan(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
493:def test_handle_plan_failure_clears_active_step(
508:        megaplan.handle_plan(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
515:def test_clear_active_step_ignores_mismatched_run_id() -> None:
--
594:def test_handle_status_reports_observability_fields(plan_fixture: PlanFixture) -> None:
625:    response = megaplan.cli.handle_status(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
648:def test_handle_status_uses_execute_runtime_guidance(plan_fixture: PlanFixture) -> None:
658:    response = megaplan.cli.handle_status(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
668:def test_handle_status_includes_progress_when_finalize_exists(plan_fixture: PlanFixture) -> None:
679:    response = megaplan.cli.handle_status(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
686:def test_handle_status_distinguishes_lock_file_from_held_lock(plan_fixture: PlanFixture) -> None:
690:    response = megaplan.cli.handle_status(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
698:def test_handle_watch_combines_status_and_progress(plan_fixture: PlanFixture) -> None:
701:    status_response = megaplan.cli.handle_status(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
702:    response = megaplan.cli.handle_watch(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
--
770:def test_handle_plan_includes_next_step_runtime(plan_fixture: PlanFixture) -> None:
771:    response = megaplan.handle_plan(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
778:def test_build_monitor_hint_references_status(plan_fixture: PlanFixture) -> None:
--
1014:def test_handle_plan_stores_nonblocking_structure_warnings(plan_fixture: PlanFixture, monkeypatch: pytest.MonkeyPatch) -> None:
1040:    response = megaplan.handle_plan(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
1047:def test_handle_plan_rejects_zero_step_structure_error(plan_fixture: PlanFixture, monkeypatch: pytest.MonkeyPatch) -> None:
1074:        megaplan.handle_plan(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
1082:def test_handle_critique_rejects_invalid_check_payload(plan_fixture: PlanFixture, monkeypatch: pytest.MonkeyPatch) -> None:
1083:    megaplan.handle_plan(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
1108:        megaplan.handle_critique(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
1115:def test_handle_critique_accepts_validated_checks(plan_fixture: PlanFixture, monkeypatch: pytest.MonkeyPatch) -> None:
1122:    megaplan.handle_plan(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
1123:    response = megaplan.handle_critique(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
1129:def test_handle_finalize_validates_payload_shape(plan_fixture: PlanFixture, monkeypatch: pytest.MonkeyPatch) -> None:
1131:    megaplan.handle_plan(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
1132:    megaplan.handle_critique(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
--
1184:def test_handle_finalize_rejects_invalid_payload(plan_fixture: PlanFixture, monkeypatch: pytest.MonkeyPatch) -> None:
1186:    megaplan.handle_plan(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
1187:    megaplan.handle_critique(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
--
1259:def test_handle_revise_requires_prior_iterate_gate(plan_fixture: PlanFixture) -> None:
1260:    megaplan.handle_plan(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
1261:    megaplan.handle_critique(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
[rerun: b10]
```

> AGENT

Now let me get a complete picture of one handler test to see the pattern:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py",
  "offset": 460,
  "limit": 120
}
```

> TOOL

tool_result Read
```
460	def test_handle_plan_sets_and_clears_active_step(
461	    plan_fixture: PlanFixture,
462	    monkeypatch: pytest.MonkeyPatch,
463	) -> None:
464	    observed: dict[str, object] = {}
465	
466	    def fake_run_step_with_worker(step: str, state: dict, plan_dir: Path, args: Namespace, **kwargs: object):
467	        del state, args, kwargs
468	        persisted = read_json(plan_dir / "state.json")
469	        observed.update(persisted["active_step"])
470	        return (
471	            WorkerResult(
472	                payload=_build_mock_payload(step, load_state(plan_dir), plan_dir),
473	                raw_output="{}",
474	                duration_ms=1,
475	                cost_usd=0.0,
476	                session_id="session-1",
477	            ),
478	            "codex",
479	            "persistent",
480	            False,
481	        )
482	
483	    monkeypatch.setattr(megaplan.handlers.worker_module, "run_step_with_worker", fake_run_step_with_worker)
484	
485	    megaplan.handle_plan(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
486	
487	    state = load_state(plan_fixture.plan_dir)
488	    assert observed["step"] == "plan"
489	    assert "started_at" in observed
490	    assert "active_step" not in state
491	
492	
493	def test_handle_plan_failure_clears_active_step(
494	    plan_fixture: PlanFixture,
495	    monkeypatch: pytest.MonkeyPatch,
496	) -> None:
497	    observed: dict[str, object] = {}
498	
499	    def fake_run_step_with_worker(step: str, state: dict, plan_dir: Path, args: Namespace, **kwargs: object):
500	        del step, state, args, kwargs
501	        persisted = read_json(plan_dir / "state.json")
502	        observed.update(persisted["active_step"])
503	        raise megaplan.CliError("worker_error", "boom", extra={"raw_output": "boom"})
504	
505	    monkeypatch.setattr(megaplan.handlers.worker_module, "run_step_with_worker", fake_run_step_with_worker)
506	
507	    with pytest.raises(megaplan.CliError, match="boom"):
508	        megaplan.handle_plan(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
509	
510	    state = load_state(plan_fixture.plan_dir)
511	    assert observed["step"] == "plan"
512	    assert "active_step" not in state
513	
514	
515	def test_clear_active_step_ignores_mismatched_run_id() -> None:
516	    state = {"sessions": {}}
517	    first_run_id = set_active_step(state, step="plan", agent="codex", mode="persistent")
518	    second_run_id = set_active_step(state, step="critique", agent="claude", mode="persistent")
519	
520	    clear_active_step(state, run_id=first_run_id)
521	
522	    assert state["active_step"]["step"] == "critique"
523	    assert state["active_step"]["run_id"] == second_run_id
524	
525	
526	def test_tiny_critique_stub_does_not_leak_active_step(
527	    tmp_path: Path,
528	    monkeypatch: pytest.MonkeyPatch,
529	) -> None:
530	    fixture = _make_plan_fixture_with_robustness(tmp_path, monkeypatch, robustness="tiny")
531	    megaplan.handle_plan(fixture.root, fixture.make_args(plan=fixture.plan_name))
532	
533	    response = megaplan.handle_critique(fixture.root, fixture.make_args(plan=fixture.plan_name))
534	    state = load_state(fixture.plan_dir)
535	
536	    assert response["state"] == megaplan.STATE_GATED
537	    assert "active_step" not in state
538	
539	
540	def test_capture_test_baseline_success(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
541	    monkeypatch.delenv(megaplan.handlers.MOCK_ENV_VAR, raising=False)
542	    monkeypatch.setattr(megaplan.handlers.shutil, "which", lambda name: "/usr/bin/pytest")
543	    monkeypatch.setattr(
544	        megaplan.handlers.subprocess,
545	        "run",
546	        lambda *args, **kwargs: subprocess.CompletedProcess(
547	            args=args[0],
548	            returncode=1,
549	            stdout=(
550	                "tests/test_a.py::test_one FAILED\n"
551	                "tests/test_b.py::test_two FAILED\n"
552	                "2 failed, 5 passed\n"
553	            ),
554	            stderr="",
555	        ),
556	    )
557	
558	    result = megaplan.handlers._capture_test_baseline(tmp_path, {})
559	
560	    assert result["baseline_test_failures"] == [
561	        "tests/test_a.py::test_one",
562	        "tests/test_b.py::test_two",
563	    ]
564	    assert result["baseline_test_command"] == "pytest --tb=no -q --no-header"
565	    assert "baseline_test_note" not in result
566	
567	
568	def test_capture_test_baseline_no_runner(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
569	    monkeypatch.delenv(megaplan.handlers.MOCK_ENV_VAR, raising=False)
570	    monkeypatch.setattr(megaplan.handlers.shutil, "which", lambda name: None)
571	
572	    result = megaplan.handlers._capture_test_baseline(tmp_path, {})
573	
574	    assert result["baseline_test_failures"] is None
575	    assert result["baseline_test_command"] is None
576	    assert "No supported test runner" in result["baseline_test_note"]
577	
578	
579	def test_capture_test_baseline_timeout(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
```

> AGENT

Let me look at test patterns for finalize more closely:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py",
  "offset": 1129,
  "limit": 120
}
```

> TOOL

tool_result Read
```
1129	def test_handle_finalize_validates_payload_shape(plan_fixture: PlanFixture, monkeypatch: pytest.MonkeyPatch) -> None:
1130	    make_args = plan_fixture.make_args
1131	    megaplan.handle_plan(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
1132	    megaplan.handle_critique(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
1133	    megaplan.handle_override(
1134	        plan_fixture.root,
1135	        make_args(plan=plan_fixture.plan_name, override_action="force-proceed", reason="test"),
1136	    )
1137	
1138	    valid_payload = {
1139	        "tasks": [
1140	            {
1141	                "id": "T1",
1142	                "description": "Ship the change",
1143	                "depends_on": [],
1144	                "status": "pending",
1145	                "executor_notes": "",
1146	                "files_changed": [],
1147	                "commands_run": [],
1148	                "evidence_files": [],
1149	                "reviewer_verdict": "",
1150	            }
1151	        ],
1152	        "watch_items": [],
1153	        "sense_checks": [
1154	            {
1155	                "id": "SC1",
1156	                "task_id": "T1",
1157	                "question": "Did it work?",
1158	                "executor_note": "",
1159	                "verdict": "",
1160	            }
1161	        ],
1162	        "meta_commentary": "ok",
1163	    }
1164	    worker = WorkerResult(
1165	        payload=valid_payload,
1166	        raw_output="valid finalize payload",
1167	        duration_ms=1,
1168	        cost_usd=0.0,
1169	        session_id="finalize-valid",
1170	    )
1171	    monkeypatch.setattr(
1172	        megaplan.workers,
1173	        "run_step_with_worker",
1174	        lambda *args, **kwargs: (worker, "claude", "persistent", False),
1175	    )
1176	
1177	    response = megaplan.handle_finalize(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
1178	
1179	    assert response["success"] is True
1180	    assert response["state"] == megaplan.STATE_FINALIZED
1181	    assert read_json(plan_fixture.plan_dir / "finalize.json")["tasks"][0]["status"] == "pending"
1182	
1183	
1184	def test_handle_finalize_rejects_invalid_payload(plan_fixture: PlanFixture, monkeypatch: pytest.MonkeyPatch) -> None:
1185	    make_args = plan_fixture.make_args
1186	    megaplan.handle_plan(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
1187	    megaplan.handle_critique(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
1188	    megaplan.handle_override(
1189	        plan_fixture.root,
1190	        make_args(plan=plan_fixture.plan_name, override_action="force-proceed", reason="test"),
1191	    )
1192	
1193	    invalid_worker = WorkerResult(
1194	        payload={
1195	            "tasks": [
1196	                {
1197	                    "id": "T1",
1198	                    "description": "Broken finalize task",
1199	                    "depends_on": [],
1200	                    "status": "done",
1201	                    "executor_notes": "",
1202	                    "files_changed": [],
1203	                    "commands_run": [],
1204	                    "evidence_files": [],
1205	                    "reviewer_verdict": "",
1206	                }
1207	            ],
1208	            "watch_items": [],
1209	            "sense_checks": [],
1210	        },
1211	        raw_output="invalid finalize payload",
1212	        duration_ms=1,
1213	        cost_usd=0.0,
1214	        session_id="finalize-invalid",
1215	    )
1216	    monkeypatch.setattr(
1217	        megaplan.workers,
1218	        "run_step_with_worker",
1219	        lambda *args, **kwargs: (invalid_worker, "claude", "persistent", False),
1220	    )
1221	
1222	    with pytest.raises(megaplan.CliError, match="status `pending`"):
1223	        megaplan.handle_finalize(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
1224	
1225	    state = load_state(plan_fixture.plan_dir)
1226	    assert state["history"][-1]["result"] == "error"
1227	
1228	
1229	def test_finalize_snapshot_remains_pending_after_execute(plan_fixture: PlanFixture) -> None:
1230	    from megaplan._core import load_finalize_snapshot
1231	
1232	    make_args = plan_fixture.make_args
1233	    megaplan.handle_plan(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
1234	    megaplan.handle_critique(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
1235	    megaplan.handle_override(
1236	        plan_fixture.root,
1237	        make_args(plan=plan_fixture.plan_name, override_action="force-proceed", reason="test"),
1238	    )
1239	
1240	    megaplan.handle_finalize(plan_fixture.root, make_args(plan=plan_fixture.plan_name))
1241	
1242	    snapshot_before_execute = load_finalize_snapshot(plan_fixture.plan_dir)
1243	    assert (plan_fixture.plan_dir / "finalize_snapshot.json").exists()
1244	    assert all(task["status"] == "pending" for task in snapshot_before_execute["tasks"])
1245	
1246	    megaplan.handle_execute(
1247	        plan_fixture.root,
1248	        make_args(plan=plan_fixture.plan_name, confirm_destructive=True, user_approved=True),
```

> AGENT

Perfect! Now let me create a comprehensive summary. Let me also look at one more test file to understand how conftest fixtures work:

> TOOL

tool_use Bash
```json
{
  "command": "ls -la /Users/user_c042661f/Documents/megaplan/tests/conftest.py 2>/dev/null && head -50 /Users/user_c042661f/Documents/megaplan/tests/conftest.py || echo \"No conftest found\""
}
```

> TOOL

tool_result Bash
```
No conftest found
[rerun: b11]
```

> AGENT

Perfect. Now I have enough information. Let me compile the findings:

## Test Patterns in megaplan Project

Based on my analysis of the test suite, here are the key patterns for writing doc-mode tests:

### 1. **Fixture Patterns** - File Paths

**Configuration fixtures** (`/Users/user_c042661f/Documents/megaplan/tests/test_config.py:16-26`):
```python
@pytest.fixture
def isolated_config_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    config_path = tmp_path / ".config" / "megaplan"
    
    def fake_config_dir(home: Path | None = None) -> Path:
        del home
        return config_path
    
    monkeypatch.setattr(io_module, "config_dir", fake_config_dir)
    monkeypatch.setattr(cli_module, "config_dir", fake_config_dir)
    return config_path
```

**Plan fixtures** (`/Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py:88-138`):
```python
@dataclass
class PlanFixture:
    root: Path
    project_dir: Path
    plan_name: str
    plan_dir: Path
    make_args: Callable[..., Namespace]

@pytest.fixture
def plan_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> PlanFixture:
    return _make_plan_fixture_with_robustness(tmp_path, monkeypatch, robustness="standard")
```

### 2. **State Dictionary Construction Patterns**

From `/Users/user_c042661f/Documents/megaplan/tests/test_evaluation.py:35-85` and `/Users/user_c042661f/Documents/megaplan/tests/test_parallel_critique.py:24-56`:

State dicts follow a consistent structure with these key sections:
- `name`, `idea`, `current_state`, `iteration`, `created_at`
- `config`: Contains `project_dir`, `auto_approve`, `robustness`
- `sessions`: Initially empty dict
- `plan_versions`: List of version records with `version`, `file`, `hash`, `timestamp`
- `history`: Initially empty list
- `meta`: Contains `significant_counts`, `weighted_scores`, `plan_deltas`, `recurring_critiques`, `total_cost_usd`, `overrides`, `notes`
- `last_gate`: Initially empty dict

### 3. **Scaffolding Patterns**

From `/Users/user_c042661f/Documents/megaplan/tests/test_evaluation.py:88-117`:
```python
def _scaffold(tmp_path: Path, *, iteration: int = 1, flags: list[dict[str, object]] | None = None) -> tuple[Path, dict[str, object]]:
    plan_dir = tmp_path / "plan"
    plan_dir.mkdir()
    (tmp_path / "project").mkdir()
    flags = flags or []
    _write_json(plan_dir / "faults.json", {"flags": flags})
    _write_json(plan_dir / f"critique_v{iteration}.json", {...})
    (plan_dir / f"plan_v{iteration}.md").write_text("new plan...", encoding="utf-8")
    _write_json(plan_dir / f"plan_v{iteration}.meta.json", {...})
    return plan_dir, _state(tmp_path, iteration=iteration)
```

Key helper: `/Users/user_c042661f/Documents/megaplan/tests/test_evaluation.py:30-32`:
```python
def _write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
```

### 4. **Handler Testing Patterns**

From `/Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py:460-490`:

**Mocking workers for handler tests**:
```python
def fake_run_step_with_worker(step: str, state: dict, plan_dir: Path, args: Namespace, **kwargs: object):
    del state, args, kwargs
    persisted = read_json(plan_dir / "state.json")
    observed.update(persisted["active_step"])
    return (
        WorkerResult(
            payload=_build_mock_payload(step, load_state(plan_dir), plan_dir),
            raw_output="{}",
            duration_ms=1,
            cost_usd=0.0,
            session_id="session-1",
        ),
        "codex",
        "persistent",
        False,
    )

monkeypatch.setattr(megaplan.handlers.worker_module, "run_step_with_worker", fake_run_step_with_worker)
megaplan.handle_plan(plan_fixture.root, plan_fixture.make_args(plan=plan_fixture.plan_name))
```

### 5. **Testing validate_execution_evidence Patterns**

From `/Users/user_c042661f/Documents/megaplan/tests/test_evaluation.py:593-634`:

```python
def test_validate_execution_evidence_flags_diff_mismatches_and_weak_notes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project_dir = tmp_path / "project"
    (project_dir / ".git").mkdir(parents=True)
    (project_dir / "src").mkdir()
    (project_dir / "docs").mkdir()
    (project_dir / "src" / "existing.py").write_text("print('ok')\n", encoding="utf-8")
    (project_dir / "docs" / "new_name.py").write_text("x = 1\n", encoding="utf-8")

    finalize_data = {
        "tasks": [
            {
                "id": "T1",
                "files_changed": ["src/existing.py", "docs/new_name.py", "ghost.py"],
                "executor_notes": "Verified src/existing.py and confirmed the rename...",
            }
        ],
        "sense_checks": [
            {"id": "SC1", "executor_note": "ok"},
        ],
    }

    monkeypatch.setattr(
        "megaplan.evaluation.subprocess.run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=["git", "status", "--short"],
            returncode=0,
            stdout=" M src/existing.py\n?? untracked.md\nR  old_name.py -> docs/new_name.py\n",
            stderr="",
        ),
    )

    result = validate_execution_evidence(finalize_data, project_dir)
    assert result["skipped"] is False
    assert result["files_in_diff"] == ["deleted.txt", "docs/new_name.py", "src/existing.py", "untracked.md"]
```

### 6. **execution_timeout Testing**

From `/Users/user_c042661f/Documents/megaplan/megaplan/execution_timeout.py:41-100`:

The function `_reset_timeout_invalid_tasks` handles two modes:
- `mode="doc"`: Checks `task.get("sections_written")` for evidence
- `mode="code"`: Checks `task.get("files_changed")` and `task.get("commands_run")`

Key pattern for testing:
- Create finalize_data with tasks containing appropriate evidence fields
- Mock subprocess.run to simulate git status output
- Verify issues list gets populated with specific validation failures

### 7. **Common Test Imports and Utilities**

From `/Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py:1-40`:
```python
from argparse import Namespace
from pathlib import Path
from megaplan.workers import WorkerResult, _build_mock_payload
from megaplan._core import load_plan, ensure_runtime_layout, clear_active_step, set_active_step

def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def make_args_factory(project_dir: Path) -> Callable[..., Namespace]:
    def make_args(**overrides: object) -> Namespace:
        data = {
            "plan": None, "idea": "test idea", "name": "test-plan",
            "project_dir": str(project_dir), "auto_approve": None,
            "robustness": None, ...
        }
        data.update(overrides)
        return Namespace(**data)
    return make_args
```

### 8. **Schema Testing Patterns**

From `/Users/user_c042661f/Documents/megaplan/tests/test_schemas.py:40-110`:

Use `strict_schema()` to validate and normalize schemas:
```python
def test_strict_schema_adds_additional_properties_false() -> None:
    result = strict_schema({"type": "object", "properties": {"a": {"type": "string"}}})
    assert result["additionalProperties"] is False

def test_strict_schema_normalizes_partial_required_arrays_recursively() -> None:
    schema = {"type": "object", "required": ["stale_root"], 
              "properties": {"inner": {"type": "object", "required": ["stale_inner"], ...}}}
    result = strict_schema(schema)
    assert result["required"] == ["inner", "items"]
```

### 9. **Finalize Payload Structure**

From `/Users/user_c042661f/Documents/megaplan/tests/test_megaplan.py:1138-1162`:

```python
valid_payload = {
    "tasks": [
        {
            "id": "T1",
            "description": "Ship the change",
            "depends_on": [],
            "status": "pending",
            "executor_notes": "",
            "files_changed": [],
            "commands_run": [],
            "evidence_files": [],
            "reviewer_verdict": "",
        }
    ],
    "watch_items": [],
    "sense_checks": [
        {
            "id": "SC1",
            "task_id": "T1",
            "question": "Did it work?",
            "executor_note": "",
            "verdict": "",
        }
    ],
    "meta_commentary": "ok",
}
```

For doc-mode, the key difference is `sections_written` field replaces file tracking fields, and tasks track document sections instead of code changes.

> DEVELOPER

Read these files and give me the key function signatures and logic I need to test:

1. megaplan/handlers.py - find handle_init (the doc-mode validation: --output required, no absolute paths, no ../ traversal), and _write_finalize_artifacts (the doc-mode branch that skips test baseline and verification task)
2. megaplan/evaluation.py - find validate_execution_evidence and its doc-mode branch
3. megaplan/doc_assembly.py - the full file
4. megaplan/schemas.py - find get_execution_schema_key and the execution_doc.json schema entry
5. megaplan/execution_timeout.py - find _merge_timeout_checkpoint and _reset_timeout_invalid_tasks doc-mode branches
6. megaplan/types.py - find PlanConfig with mode/output_path fields

Give me exact line numbers and the key conditional logic for each.

> AGENT

I'll read these files to find the key function signatures and logic you need to test.

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
File content (24202 tokens) exceeds maximum allowed tokens (10000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
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
123	def validate_execution_evidence(finalize_data: dict[str, Any], project_dir: Path, *, mode: str = "code") -> dict[str, Any]:
124	    if mode == "doc":
125	        return _validate_execution_evidence_doc(finalize_data, project_dir)
126	    return _validate_execution_evidence_code(finalize_data, project_dir)
127	
128	
129	def _validate_execution_evidence_doc(finalize_data: dict[str, Any], project_dir: Path) -> dict[str, Any]:
130	    findings: list[str] = []
131	    tasks = finalize_data.get("tasks", [])
132	
133	    planned_sections: set[str] = set()
134	    claimed_sections: set[str] = set()
135	    for task in tasks:
136	        if task.get("status") != "done":
137	            continue
138	        for section_id in task.get("sections_written", []):
139	            if isinstance(section_id, str) and section_id.strip():
140	                claimed_sections.add(section_id)
141	
142	    for task in tasks:
143	        for section_id in task.get("sections_written", []):
144	            if isinstance(section_id, str) and section_id.strip():
145	                planned_sections.add(section_id)
146	
147	    missing_sections = sorted(planned_sections - claimed_sections)
148	    if missing_sections:
149	        findings.append(
150	            "Planned sections not claimed by any done task: "
151	            + ", ".join(missing_sections)
152	        )
153	
154	    unclaimed = sorted(claimed_sections - planned_sections)
155	    if unclaimed:
156	        findings.append(
157	            "Sections claimed by done tasks but not in any task plan: "
158	            + ", ".join(unclaimed)
159	        )
160	
161	    output_path_str = ""
162	    config = finalize_data.get("config", {})
163	    if isinstance(config, dict):
164	        output_path_str = config.get("output_path", "")
165	    if not output_path_str:
166	        for task in tasks:
167	            if task.get("sections_written"):
168	                break
169	
170	    for sense_check in finalize_data.get("sense_checks", []):
171	        sense_check_id = sense_check.get("id", "?")
172	        note = sense_check.get("executor_note", "")
173	        if not isinstance(note, str) or not note.strip():
174	            findings.append(f"Sense check {sense_check_id} is missing an executor acknowledgment.")
175	            continue
176	        if _is_perfunctory_ack(note):
177	            findings.append(
178	                f"Sense check {sense_check_id} acknowledgment is perfunctory: {note.strip()!r}."
179	            )
180	
181	    for task in tasks:
182	        if task.get("status") != "done":
183	            continue
184	        task_id = task.get("id", "?")
185	        notes = task.get("executor_notes", "")
186	        if not isinstance(notes, str) or not notes.strip():
187	            continue
188	        if is_rubber_stamp(notes, strict=True):
189	            findings.append(
190	                f"Task {task_id} executor_notes are perfunctory: {notes.strip()!r}."
191	            )
192	
193	    return {
194	        "findings": findings,
195	        "files_in_diff": [],
196	        "files_claimed": [],
197	        "skipped": False,
198	        "reason": "",
199	    }
200	
201	
202	def _validate_execution_evidence_code(finalize_data: dict[str, Any], project_dir: Path) -> dict[str, Any]:
203	    findings: list[str] = []
204	    files_claimed = sorted(
205	        {
206	            _normalize_repo_path(path, project_dir)
207	            for task in finalize_data.get("tasks", [])
208	            for path in task.get("files_changed", [])
209	            if isinstance(path, str) and path.strip()
210	        }
211	    )
212	
213	    if not (project_dir / ".git").exists():
214	        return {
215	            "findings": findings,
216	            "files_in_diff": [],
217	            "files_claimed": files_claimed,
218	            "skipped": True,
219	            "reason": "Project directory is not a git repository.",
220	        }
221	
222	    try:
223	        process = subprocess.run(
224	            ["git", "status", "--short"],
225	            cwd=str(project_dir),
226	            text=True,
227	            capture_output=True,
228	            timeout=30,
229	        )
230	    except FileNotFoundError:
231	        return {
232	            "findings": findings,
233	            "files_in_diff": [],
234	            "files_claimed": files_claimed,
235	            "skipped": True,
236	            "reason": "git not found on PATH.",
237	        }
238	    except subprocess.TimeoutExpired:
239	        return {
240	            "findings": findings,
241	            "files_in_diff": [],
242	            "files_claimed": files_claimed,
243	            "skipped": True,
244	            "reason": "git status timed out.",
245	        }
246	
247	    if process.returncode != 0:
248	        return {
249	            "findings": findings,
250	            "files_in_diff": [],
251	            "files_claimed": files_claimed,
252	            "skipped": True,
253	            "reason": f"git status failed: {process.stderr.strip() or process.stdout.strip()}",
254	        }
255	
256	    files_in_diff = sorted(_parse_git_status_paths(process.stdout))
257	    claimed_set = set(files_claimed)
258	    diff_set = set(files_in_diff)
259	
260	    # Git status reports untracked directories as `dir/` (trailing slash).
261	    # A claimed file beneath such a directory should be considered present.
262	    dir_prefixes = [p for p in diff_set if p.endswith("/")]
263	
264	    def _covered_by_diff(claimed: str) -> bool:
265	        if claimed in diff_set:
266	            return True
267	        return any(claimed.startswith(prefix) or claimed == prefix.rstrip("/") for prefix in dir_prefixes)
268	
269	    phantom_claims = sorted(c for c in claimed_set if not _covered_by_diff(c))
270	    if phantom_claims:
271	        findings.append(
272	            "Executor claimed changed files not present in git status: "
273	            + ", ".join(phantom_claims)
274	        )
275	
276	    # For the reverse check, treat a directory as "claimed" when any claimed
277	    # path is under it.
278	    def _dir_is_claimed(diff_path: str) -> bool:
279	        if not diff_path.endswith("/"):
280	            return False
281	        return any(c.startswith(diff_path) for c in claimed_set)
282	
283	    unclaimed_changes = sorted(
284	        d for d in diff_set
285	        if d not in claimed_set and not _dir_is_claimed(d)
286	    )
287	    if unclaimed_changes:
288	        findings.append(
289	            "Git status shows changed files not claimed by any task: "
290	            + ", ".join(unclaimed_changes)
291	        )
292	
293	    for sense_check in finalize_data.get("sense_checks", []):
294	        sense_check_id = sense_check.get("id", "?")
295	        note = sense_check.get("executor_note", "")
296	        if not isinstance(note, str) or not note.strip():
297	            findings.append(f"Sense check {sense_check_id} is missing an executor acknowledgment.")
298	            continue
299	        if _is_perfunctory_ack(note):
300	            findings.append(
301	                f"Sense check {sense_check_id} acknowledgment is perfunctory: {note.strip()!r}."
302	            )
303	
304	    for task in finalize_data.get("tasks", []):
305	        if task.get("status") != "done":
306	            continue
307	        task_id = task.get("id", "?")
308	        notes = task.get("executor_notes", "")
309	        if not isinstance(notes, str) or not notes.strip():
310	            continue
311	        if is_rubber_stamp(notes, strict=True):
312	            findings.append(
313	                f"Task {task_id} executor_notes are perfunctory: {notes.strip()!r}."
314	            )
315	
316	    return {
317	        "findings": findings,
318	        "files_in_diff": files_in_diff,
319	        "files_claimed": files_claimed,
320	        "skipped": False,
321	        "reason": "",
322	    }
323	
324	
325	def flag_weight(flag: FlagRecord) -> float:
326	    """Weight a flag for gate context. Higher = more blocking."""
327	    category = flag.get("category", "other")
328	    concern = flag.get("concern", "").lower()
329	
330	    if category == "security":
331	        return 3.0
332	
333	    implementation_detail_signals = [
334	        "column",
335	        "schema",
336	        "field",
337	        "as written",
338	        "pseudocode",
339	        "seed sql",
340	        "placeholder",
341	    ]
342	    if any(signal in concern for signal in implementation_detail_signals):
343	        return 0.5
344	
345	    weights = {
346	        "correctness": 2.0,
347	        "completeness": 1.5,
348	        "performance": 1.0,
349	        "maintainability": 0.75,
350	        "other": 1.0,
351	    }
352	    return weights.get(category, 1.0)
353	
354	
355	def compute_plan_delta_percent(previous_text: str | None, current_text: str) -> float | None:
356	    if previous_text is None:
357	        return None
358	    ratio = SequenceMatcher(None, previous_text, current_text).ratio()
359	    return round((1.0 - ratio) * 100.0, 2)
360	
361	
362	def compute_recurring_critiques(plan_dir: Path, iteration: int) -> list[str]:
363	    if iteration < 2:
364	        return []
365	    previous = read_json(current_iteration_artifact(plan_dir, "critique", iteration - 1))
366	    current = read_json(current_iteration_artifact(plan_dir, "critique", iteration))
367	    previous_concerns = {normalize_text(flag.get("concern", "")) for flag in previous.get("flags", []) if isinstance(flag, dict)}
368	    current_concerns = {normalize_text(flag.get("concern", "")) for flag in current.get("flags", []) if isinstance(flag, dict)}
369	    return sorted(previous_concerns.intersection(current_concerns))
370	
371	
372	def _strip_fenced_blocks(text: str) -> str:
373	    kept_lines: list[str] = []
374	    inside_fence = False
375	    for line in text.splitlines(keepends=True):
376	        if line.startswith("```"):
377	            inside_fence = not inside_fence
378	            continue
379	        if not inside_fence:
380	            kept_lines.append(line)
381	    if inside_fence:
382	        # Unclosed fence — return original text rather than silently dropping content
383	        return text
384	    return "".join(kept_lines)
385	
386	
387	def _match_section_boundary(line: str) -> tuple[bool, str | None]:
388	    """Check if a line is a section boundary. Returns (is_boundary, section_id)."""
389	    step_match = _PLAN_STEP_RE.match(line) or _PLAN_PHASE_STEP_RE.match(line)
390	    if step_match:
391	        return True, f"S{step_match.group(1)}"
392	    if _PLAN_HEADING_RE.match(line) or _PLAN_PHASE_HEADING_RE.match(line):
393	        return True, None
394	    return False, None
395	
396	
397	def parse_plan_sections(plan_text: str) -> list[PlanSection]:
398	    lines = plan_text.splitlines(keepends=True)
399	    if not lines:
400	        return [PlanSection(heading="", body="", id=None, start_line=1, end_line=0)]
401	
402	    boundaries: list[tuple[int, int, str, str | None]] = []
403	    inside_fence = False
404	    for index, line in enumerate(lines):
405	        if line.startswith("```"):
406	            inside_fence = not inside_fence
407	            continue
408	        if inside_fence:
409	            continue
410	        is_boundary, section_id = _match_section_boundary(line)
411	        if is_boundary:
412	            boundaries.append((index, index + 1, line.rstrip("\n"), section_id))
413	
414	    if inside_fence:
415	        # Unclosed fence — re-scan ignoring fence state so we don't silently lose sections
416	        boundaries = []
417	        for index, line in enumerate(lines):
418	            is_boundary, section_id = _match_section_boundary(line)
419	            if is_boundary:
420	                boundaries.append((index, index + 1, line.rstrip("\n"), section_id))
421	
422	    if not boundaries:
423	        return [PlanSection(heading="", body=plan_text, id=None, start_line=1, end_line=len(lines))]
424	
425	    sections: list[PlanSection] = []
426	    first_index, first_line, _, _ = boundaries[0]
427	    if first_index > 0:
428	        sections.append(
429	            PlanSection(
430	                heading="",
431	                body="".join(lines[:first_index]),
432	                id=None,
433	                start_line=1,
434	                end_line=first_line - 1,
435	            )
436	        )
437	
438	    for boundary_index, (start_index, start_line, heading, section_id) in enumerate(boundaries):
439	        next_start_index = boundaries[boundary_index + 1][0] if boundary_index + 1 < len(boundaries) else len(lines)
440	        sections.append(
441	            PlanSection(
442	                heading=heading,
443	                body="".join(lines[start_index:next_start_index]),
444	                id=section_id,
445	                start_line=start_line,
446	                end_line=next_start_index,
447	            )
448	        )
449	    return sections
450	
451	
452	def reassemble_plan(sections: list[PlanSection]) -> str:
453	    return "".join(section.body for section in sections)
454	
455	
456	def renumber_steps(sections: list[PlanSection]) -> list[PlanSection]:
457	    renumbered: list[PlanSection] = []
458	    step_number = 1
459	    for section in sections:
460	        if section.id is None:
461	            renumbered.append(section)
462	            continue
463	        # Detect heading level (## or ###) and preserve it
464	        step_prefix_match = re.match(r"^(#{2,3})\s+Step\s+\d+:", section.heading)
465	        if not step_prefix_match:
466	            renumbered.append(section)
467	            continue
468	        hashes = step_prefix_match.group(1)
469	        new_heading = re.sub(rf"^{hashes}\s+Step\s+\d+:", f"{hashes} Step {step_number}:", section.heading, count=1)
470	        new_body = re.sub(rf"^{hashes}\s+Step\s+\d+:", f"{hashes} Step {step_number}:", section.body, count=1, flags=re.MULTILINE)
471	        renumbered.append(
472	            PlanSection(
473	                heading=new_heading,
474	                body=new_body,
475	                id=f"S{step_number}",
476	                start_line=section.start_line,
477	                end_line=section.end_line,
478	            )
479	        )
480	        step_number += 1
481	    return renumbered
482	
483	
484	def validate_plan_structure(plan_text: str) -> list[str]:
485	    issues: list[str] = []
486	    stripped = _strip_fenced_blocks(plan_text)
487	
488	    if len(re.findall(r"(?mi)^#\s+.+$", stripped)) != 1:
489	        issues.append("Plan should have exactly one H1 title.")
490	    if not re.search(r"(?mi)^##\s+Overview\s*$", stripped):
491	        issues.append("Plan should include a `## Overview` section.")
492	
493	    # Accept both flat (## Step N:) and hierarchical (### Step N: under ## Phase)
494	    step_matches = list(re.finditer(r"(?im)^#{2,3}\s+Step\s+\d+:\s+.+$", stripped))
495	    if not step_matches:
496	        issues.append(PLAN_STRUCTURE_REQUIRED_STEP_ISSUE)
497	        return issues
498	
499	    if not (
500	        re.search(r"(?mi)^##\s+Execution Order\s*$", stripped)
501	        or re.search(r"(?mi)^##\s+Validation Order\s*$", stripped)
502	    ):
503	        issues.append("Plan should include `## Execution Order` or `## Validation Order`.")
504	
505	    missing_substeps = False
506	    missing_file_refs = False
507	    for index, match in enumerate(step_matches):
508	        start = match.end()
509	        next_heading = re.search(r"(?im)^#{2,3}\s+.+$", stripped[start:])
510	        end = start + next_heading.start() if next_heading else len(stripped)
511	        section = stripped[match.start():end]
512	        if not re.search(r"(?m)^\d+\.\s+", stripped[start:end]):
513	            missing_substeps = True
514	        if not re.search(r"`[^`]+`", section):
515	            missing_file_refs = True
516	
517	    if missing_substeps:
518	        issues.append("Each step section should include at least one numbered substep.")
519	    if missing_file_refs:
520	        issues.append("Each step section should reference at least one file in backticks.")
521	    return issues
522	
523	
524	def _previous_iteration_plan_path(plan_dir: Path, state: PlanState) -> Path | None:
525	    current_version = state["iteration"]
526	    previous_version = current_version - 1
527	    if previous_version < 1:
528	        return None
529	    matching = [
530	        record
531	        for record in state["plan_versions"]
532	        if record.get("version") == previous_version
533	    ]
534	    if not matching:
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
585	        f"Iteration {iteration}. Weighted score trajectory: {trajectory}. "
586	        f"Plan deltas: {delta_summary}. "
587	        f"Recurring critiques: {len(recurring)}. "
588	        f"Resolved flags: {len(resolved_flags)}. "
589	        f"Open significant flags: {len(unresolved)}."
590	    )
591	    debt_overlaps = []
592	    overlapping_escalated_subsystems: set[str] = set()
593	    escalated_lookup = {
594	        subsystem: total
595	        for subsystem, total, _entries in escalated_subsystems(debt_registry)
596	    }
597	    for flag in unresolved:
598	        subsystem = extract_subsystem_tag(flag["concern"])
599	        match = find_matching_debt(debt_registry, subsystem, flag["concern"])
600	        if match is None:
601	            continue
602	        debt_overlaps.append(
603	            {
604	                "flag_id": flag["id"],
605	                "debt_id": match["id"],
606	                "subsystem": subsystem,
607	                "concern": flag["concern"],
608	                "debt_concern": match["concern"],
609	                "occurrence_count": match["occurrence_count"],
610	                "plan_ids": match["plan_ids"],
611	            }
612	        )
613	        if subsystem in escalated_lookup:
614	            overlapping_escalated_subsystems.add(subsystem)
615	
616	    result: GateSignals = {
617	        "robustness": robustness,
618	        "signals": {
619	            "iteration": iteration,
620	            "idea": state.get("idea", ""),
621	            "significant_flags": significant_count,
622	            "unresolved_flags": [
623	                {
624	                    "id": flag["id"],
625	                    "concern": flag["concern"],
626	                    "category": flag["category"],
627	                    "severity": flag.get("severity", "unknown"),
628	                    "status": flag["status"],
629	                }
630	                for flag in unresolved
631	            ],
632	            "resolved_flags": resolved_flags,
633	            "weighted_score": weighted_score,
634	            "weighted_history": weighted_history,
635	            "plan_delta_from_previous": plan_delta,
636	            "recurring_critiques": recurring,
637	            "scope_creep_flags": [flag["id"] for flag in open_scope_creep],
638	            "loop_summary": loop_summary,
639	            "debt_overlaps": debt_overlaps,
640	            "escalated_debt_subsystems": [
641	                {
642	                    "subsystem": subsystem,
643	                    "total_occurrences": escalated_lookup[subsystem],
644	                }
645	                for subsystem in sorted(overlapping_escalated_subsystems)
646	            ],
647	        },
648	        "warnings": [],
649	    }
650	    if open_scope_creep:
651	        result["warnings"].append(
652	            "Scope creep detected: the plan appears to be expanding beyond the original idea or recorded user notes."
653	        )
654	    if iteration >= 5:
655	        result["warnings"].append(f"Iteration {iteration}: high iteration count.")
656	    if iteration >= 12:
657	        result["warnings"].append(
658	            f"Iteration {iteration}: hard iteration limit reached. Escalation is likely warranted."
659	        )
660	    for subsystem in sorted(overlapping_escalated_subsystems):
661	        result["warnings"].append(
662	            "Recurring debt detected in subsystem "
663	            f"'{subsystem}' (total occurrences: {escalated_lookup[subsystem]}). "
664	            "Recommend holistic redesign rather than another point fix."
665	        )
666	    return result
667	
668	
669	def run_gate_checks(
670	    plan_dir: Path,
671	    state: PlanState,
672	    *,
673	    command_lookup: Callable[[str], str | None] | None = None,
674	) -> GateCheckResult:
675	    project_dir = Path(state["config"]["project_dir"])
676	    meta = read_json(latest_plan_meta_path(plan_dir, state))
677	    flag_registry = load_flag_registry(plan_dir)
678	    unresolved = unresolved_significant_flags(flag_registry)
679	    lookup = command_lookup or (lambda name: None)
680	    configured_agent = state.get("config", {}).get("agent", "")
681	    checks: dict[str, bool] = {
682	        "project_dir_exists": project_dir.exists(),
683	        "project_dir_writable": os.access(project_dir, os.W_OK),
684	        "success_criteria_present": bool(meta.get("success_criteria")),
685	    }
686	    if configured_agent != "hermes":
687	        checks["claude_available"] = bool(lookup("claude"))
688	        checks["codex_available"] = bool(lookup("codex"))
689	    return {
690	        "passed": all(checks.values()),
691	        "criteria_check": {
692	            "count": len(meta.get("success_criteria", [])),
693	            "items": meta.get("success_criteria", []),
694	        },
695	        "preflight_results": checks,
696	        "unresolved_flags": unresolved,
697	    }
698	
699	
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
750	    worsening = previous_score is not None and weighted_score > previous_score
751	    improving = previous_score is not None and weighted_score < previous_score
752	
753	    if iteration == 1:
754	        guidance = f"First iteration; follow gate recommendation: {recommendation}."
755	    elif recommendation == "PROCEED" and preflight_passed:
756	        guidance = "Plan passed gate and preflight. Proceed to finalize."
757	    elif recommendation == "PROCEED":
758	        failing_checks = ", ".join(
759	            name for name, passed in preflight_results.items() if not passed
760	        )
761	        guidance = f"Gate says PROCEED but preflight blocked. Fix: {failing_checks}."
762	    elif recommendation == "ESCALATE":
763	        guidance = "Gate escalated. Ask the user: force-proceed, add-note, or abort."
764	    elif recommendation == "ITERATE" and plateaued and recurring_critiques:
765	        guidance = (
766	            "Score plateaued with recurring critiques the loop can't fix. Consider "
767	            f"force-proceeding: `megaplan override force-proceed --plan {plan_name}`"
768	        )
769	    elif recommendation == "ITERATE" and improving:
770	        guidance = f"Score improving ({previous_score} -> {weighted_score}). Continue to revise."
771	    elif recommendation == "ITERATE" and worsening:
772	        guidance = (
773	            f"Score worsening ({previous_score} -> {weighted_score}). "
774	            "Investigate; the loop may be diverging."
775	        )
776	    else:
777	        guidance = "Gate recommends another iteration. Revise the plan."
778	
779	    hints: list[str] = []
780	    if unresolved_flags:
781	        hints.append("Verify unresolved flags against the plan and project code before accepting.")
782	    if recurring_critiques:
783	        critiques = ", ".join(recurring_critiques)
784	        hints.append(
785	            f"Recurring critiques ({critiques}); the loop likely can't fix these, so judge if they are real blockers."
786	        )
787	    if scope_creep:
788	        hints.append("Scope creep detected; compare the current plan against the original idea.")
789	
790	    return " ".join([guidance, *hints]).strip()
791
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
70	    """Read per-batch executor outputs and assemble the final document.
71	
72	    Sections are ordered by their owning task's position in finalize_data.
73	    The file is written atomically (temp file + rename). Running twice
74	    replaces the file completely (idempotent).
75	    """
76	    batch_payloads: list[dict[str, Any]] = []
77	    batch_index = 1
78	    while True:
79	        batch_path = plan_dir / f"execution_batch_{batch_index}.json"
80	        if not batch_path.exists():
81	            break
82	        try:
83	            batch_payloads.append(read_json(batch_path))
84	        except (OSError, ValueError):
85	            pass
86	        batch_index += 1
87	
88	    sections = extract_sections(batch_payloads)
89	    ordered_ids = _section_plan_order(finalize_data, batch_payloads)
90	
91	    lines: list[str] = []
92	    for section_id in ordered_ids:
93	        content = sections.get(section_id, "")
94	        if content:
95	            lines.append(content)
96	
97	    assembled_text = "\n\n".join(lines) if lines else ""
98	
99	    output_path.parent.mkdir(parents=True, exist_ok=True)
100	    fd, tmp_path = tempfile.mkstemp(
101	        dir=str(output_path.parent),
102	        suffix=".tmp",
103	    )
104	    closed = False
105	    try:
106	        os.write(fd, assembled_text.encode("utf-8"))
107	        os.close(fd)
108	        closed = True
109	        os.replace(tmp_path, str(output_path))
110	    except BaseException:
111	        if not closed:
112	            os.close(fd)
113	        if os.path.exists(tmp_path):
114	            os.unlink(tmp_path)
115	        raise
116	
117	    return output_path
118
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
5	from copy import deepcopy
6	from typing import Any
7	
8	
9	SCHEMAS: dict[str, dict[str, Any]] = {
10	    "plan.json": {
11	        "type": "object",
12	        "properties": {
13	            "plan": {"type": "string"},
14	            "questions": {"type": "array", "items": {"type": "string"}},
15	            "success_criteria": {
16	                "type": "array",
17	                "items": {
18	                    "type": "object",
19	                    "properties": {
20	                        "criterion": {"type": "string"},
21	                        "priority": {"type": "string", "enum": ["must", "should", "info"]},
22	                    },
23	                    "required": ["criterion", "priority"],
24	                },
25	            },
26	            "assumptions": {"type": "array", "items": {"type": "string"}},
27	        },
28	        "required": ["plan", "questions", "success_criteria", "assumptions"],
29	    },
30	    "prep.json": {
31	        "type": "object",
32	        "properties": {
33	            "skip": {"type": "boolean"},
34	            "task_summary": {"type": "string"},
35	            "key_evidence": {
36	                "type": "array",
37	                "items": {
38	                    "type": "object",
39	                    "properties": {
40	                        "point": {"type": "string"},
41	                        "source": {"type": "string"},
42	                        "relevance": {"type": "string", "enum": ["high", "medium", "low"]},
43	                    },
44	                    "required": ["point", "source", "relevance"],
45	                },
46	            },
47	            "relevant_code": {
48	                "type": "array",
49	                "items": {
50	                    "type": "object",
51	                    "properties": {
52	                        "file_path": {"type": "string"},
53	                        "why": {"type": "string"},
54	                        "functions": {"type": "array", "items": {"type": "string"}},
55	                    },
56	                    "required": ["file_path", "why", "functions"],
57	                },
58	            },
59	            "test_expectations": {
60	                "type": "array",
61	                "items": {
62	                    "type": "object",
63	                    "properties": {
64	                        "test_id": {"type": "string"},
65	                        "what_it_checks": {"type": "string"},
66	                        "status": {"type": "string", "enum": ["fail_to_pass", "pass_to_pass"]},
67	                    },
68	                    "required": ["test_id", "what_it_checks", "status"],
69	                },
70	            },
71	            "constraints": {"type": "array", "items": {"type": "string"}},
72	            "suggested_approach": {"type": "string"},
73	        },
74	        "required": [
75	            "skip",
76	            "task_summary",
77	            "key_evidence",
78	            "relevant_code",
79	            "test_expectations",
80	            "constraints",
81	            "suggested_approach",
82	        ],
83	    },
84	    "revise.json": {
85	        "type": "object",
86	        "properties": {
87	            "plan": {"type": "string"},
88	            "changes_summary": {"type": "string"},
89	            "flags_addressed": {"type": "array", "items": {"type": "string"}},
90	            "assumptions": {"type": "array", "items": {"type": "string"}},
91	            "success_criteria": {
92	                "type": "array",
93	                "items": {
94	                    "type": "object",
95	                    "properties": {
96	                        "criterion": {"type": "string"},
97	                        "priority": {"type": "string", "enum": ["must", "should", "info"]},
98	                    },
99	                    "required": ["criterion", "priority"],
100	                },
101	            },
102	            "questions": {"type": "array", "items": {"type": "string"}},
103	        },
104	        "required": [
105	            "plan",
106	            "changes_summary",
107	            "flags_addressed",
108	            "assumptions",
109	            "success_criteria",
110	            "questions",
111	        ],
112	    },
113	    "gate.json": {
114	        "type": "object",
115	        "properties": {
116	            "recommendation": {
117	                "type": "string",
118	                "enum": ["PROCEED", "ITERATE", "ESCALATE"],
119	            },
120	            "rationale": {"type": "string"},
121	            "signals_assessment": {"type": "string"},
122	            "warnings": {"type": "array", "items": {"type": "string"}},
123	            "settled_decisions": {
124	                "type": "array",
125	                "items": {
126	                    "type": "object",
127	                    "properties": {
128	                        "id": {"type": "string"},
129	                        "decision": {"type": "string"},
130	                        "rationale": {"type": "string"},
131	                    },
132	                    "required": ["id", "decision", "rationale"],
133	                },
134	            },
135	            "flag_resolutions": {
136	                "type": "array",
137	                "items": {
138	                    "type": "object",
139	                    "properties": {
140	                        "flag_id": {"type": "string"},
141	                        "action": {"type": "string", "enum": ["dispute", "accept_tradeoff"]},
142	                        "evidence": {"type": "string"},
143	                        "rationale": {"type": "string"},
144	                    },
145	                    "required": ["flag_id", "action", "evidence", "rationale"],
146	                },
147	            },
148	            "accepted_tradeoffs": {
149	                "type": "array",
150	                "items": {
151	                    "type": "object",
152	                    "properties": {
153	                        "flag_id": {"type": "string"},
154	                        "concern": {"type": "string"},
155	                        "subsystem": {"type": "string"},
156	                        "rationale": {"type": "string"},
157	                    },
158	                    "required": ["flag_id", "concern", "subsystem", "rationale"],
159	                },
160	            },
161	        },
162	        "required": [
163	            "recommendation",
164	            "rationale",
165	            "signals_assessment",
166	            "warnings",
167	            "settled_decisions",
168	            "flag_resolutions",
169	            "accepted_tradeoffs",
170	        ],
171	    },
172	    "critique.json": {
173	        "type": "object",
174	        "properties": {
175	            "checks": {
176	                "type": "array",
177	                "items": {
178	                    "type": "object",
179	                    "properties": {
180	                        "id": {"type": "string"},
181	                        "question": {"type": "string"},
182	                        "findings": {
183	                            "type": "array",
184	                            "items": {
185	                                "type": "object",
186	                                "properties": {
187	                                    "detail": {"type": "string"},
188	                                    "flagged": {"type": "boolean"},
189	                                },
190	                                "required": ["detail", "flagged"],
191	                            },
192	                        },
193	                    },
194	                    "required": ["id", "question", "findings"],
195	                },
196	            },
197	            "flags": {
198	                "type": "array",
199	                "items": {
200	                    "type": "object",
201	                    "properties": {
202	                        "id": {"type": "string"},
203	                        "concern": {"type": "string"},
204	                        "category": {
205	                            "type": "string",
206	                            "enum": [
207	                                "correctness",
208	                                "security",
209	                                "completeness",
210	                                "performance",
211	                                "maintainability",
212	                                "doc-quality",
213	                                "other",
214	                            ],
215	                        },
216	                        "severity_hint": {
217	                            "type": "string",
218	                            "enum": ["likely-significant", "likely-minor", "uncertain"],
219	                        },
220	                        "evidence": {"type": "string"},
221	                    },
222	                    "required": ["id", "concern", "category", "severity_hint", "evidence"],
223	                },
224	            },
225	            "verified_flag_ids": {"type": "array", "items": {"type": "string"}},
226	            "disputed_flag_ids": {"type": "array", "items": {"type": "string"}},
227	        },
228	        "required": ["checks", "flags", "verified_flag_ids", "disputed_flag_ids"],
229	    },
230	"finalize.json": {
231	        "type": "object",
232	        "properties": {
233	            "tasks": {
234	                "type": "array",
235	                "items": {
236	                    "type": "object",
237	                    "properties": {
238	                        "id": {"type": "string"},
239	                        "description": {"type": "string"},
240	                        "depends_on": {"type": "array", "items": {"type": "string"}},
241	                        "status": {"type": "string", "enum": ["pending", "done", "skipped"]},
242	                        "executor_notes": {"type": "string"},
243	                        "files_changed": {"type": "array", "items": {"type": "string"}},
244	                        "commands_run": {"type": "array", "items": {"type": "string"}},
245	                        "evidence_files": {"type": "array", "items": {"type": "string"}},
246	                        "reviewer_verdict": {"type": "string"},
247	                    },
248	                    "required": [
249	                        "id",
250	                        "description",
251	                        "depends_on",
252	                        "status",
253	                        "executor_notes",
254	                        "files_changed",
255	                        "commands_run",
256	                        "evidence_files",
257	                        "reviewer_verdict",
258	                    ],
259	                },
260	            },
261	            "watch_items": {"type": "array", "items": {"type": "string"}},
262	            "sense_checks": {
263	                "type": "array",
264	                "items": {
265	                    "type": "object",
266	                    "properties": {
267	                        "id": {"type": "string"},
268	                        "task_id": {"type": "string"},
269	                        "question": {"type": "string"},
270	                        "executor_note": {"type": "string"},
271	                        "verdict": {"type": "string"},
272	                    },
273	                    "required": ["id", "task_id", "question", "executor_note", "verdict"],
274	                },
275	            },
276	            "meta_commentary": {"type": "string"},
277	            "validation": {
278	                "type": "object",
279	                "properties": {
280	                    "plan_steps_covered": {
281	                        "type": "array",
282	                        "items": {
283	                            "type": "object",
284	                            "properties": {
285	                                "plan_step_summary": {"type": "string"},
286	                                "finalize_task_ids": {
287	                                    "type": "array",
288	                                    "items": {"type": "string"},
289	                                },
290	                            },
291	                            "required": ["plan_step_summary", "finalize_task_ids"],
292	                        },
293	                    },
294	                    "orphan_tasks": {
295	                        "type": "array",
296	                        "items": {"type": "string"},
297	                    },
298	                    "completeness_notes": {"type": "string"},
299	                    "coverage_complete": {"type": "boolean"},
300	                },
301	                "required": [
302	                    "plan_steps_covered",
303	                    "orphan_tasks",
304	                    "completeness_notes",
305	                    "coverage_complete",
306	                ],
307	            },
308	            "baseline_test_failures": {
309	                "type": ["array", "null"],
310	                "items": {"type": "string"},
311	            },
312	            "baseline_test_command": {"type": ["string", "null"]},
313	            "baseline_test_note": {"type": "string"},
314	        },
315	        "required": ["tasks", "watch_items", "sense_checks", "meta_commentary", "validation"],
316	    },
317	    "execution.json": {
318	        "type": "object",
319	        "properties": {
320	            "output": {"type": "string"},
321	            "files_changed": {"type": "array", "items": {"type": "string"}},
322	            "commands_run": {"type": "array", "items": {"type": "string"}},
323	            "deviations": {"type": "array", "items": {"type": "string"}},
324	            "task_updates": {
325	                "type": "array",
326	                "items": {
327	                    "type": "object",
328	                    "properties": {
329	                        "task_id": {"type": "string"},
330	                        "status": {"type": "string", "enum": ["done", "skipped"]},
331	                        "executor_notes": {"type": "string"},
332	                        "files_changed": {"type": "array", "items": {"type": "string"}},
333	                        "commands_run": {"type": "array", "items": {"type": "string"}},
334	                    },
335	                    "required": ["task_id", "status", "executor_notes", "files_changed", "commands_run"],
336	                },
337	            },
338	            "sense_check_acknowledgments": {
339	                "type": "array",
340	                "items": {
341	                    "type": "object",
342	                    "properties": {
343	                        "sense_check_id": {"type": "string"},
344	                        "executor_note": {"type": "string"},
345	                    },
346	                    "required": ["sense_check_id", "executor_note"],
347	                },
348	            },
349	        },
350	        "required": ["output", "files_changed", "commands_run", "deviations", "task_updates", "sense_check_acknowledgments"],
351	    },
352	    "loop_plan.json": {
353	        "type": "object",
354	        "properties": {
355	            "spec_updates": {
356	                "type": "object",
357	                "additionalProperties": True,
358	            },
359	            "next_action": {"type": "string"},
360	            "reasoning": {"type": "string"},
361	        },
362	        "required": ["spec_updates", "next_action", "reasoning"],
363	    },
364	    "loop_execute.json": {
365	        "type": "object",
366	        "properties": {
367	            "diagnosis": {"type": "string"},
368	            "fix_description": {"type": "string"},
369	            "files_to_change": {"type": "array", "items": {"type": "string"}},
370	            "confidence": {"type": "string"},
371	            "outcome": {"type": "string"},
372	            "should_pause": {"type": "boolean"},
373	        },
374	        "required": ["diagnosis", "fix_description", "files_to_change", "confidence", "outcome", "should_pause"],
375	    },
376	    "review.json": {
377	        "type": "object",
378	        "properties": {
379	            "review_verdict": {"type": "string", "enum": ["approved", "needs_rework"]},
380	            "checks": {
381	                "type": "array",
382	                "items": {
383	                    "type": "object",
384	                    "properties": {
385	                        "id": {"type": "string"},
386	                        "question": {"type": "string"},
387	                        "guidance": {"type": "string"},
388	                        "findings": {
389	                            "type": "array",
390	                            "items": {
391	                                "type": "object",
392	                                "properties": {
393	                                    "detail": {"type": "string"},
394	                                    "flagged": {"type": "boolean"},
395	                                    "status": {"type": "string"},
396	                                    "evidence_file": {"type": "string"},
397	                                },
398	                                "required": ["detail", "flagged", "status", "evidence_file"],
399	                            },
400	                        },
401	                        "prior_findings": {
402	                            "type": "array",
403	                            "items": {
404	                                "type": "object",
405	                                "properties": {
406	                                    "detail": {"type": "string"},
407	                                    "flagged": {"type": "boolean"},
408	                                    "status": {"type": "string"},
409	                                },
410	                                "required": ["detail", "flagged", "status"],
411	                            },
412	                        },
413	                    },
414	                    "required": ["id", "question", "guidance", "findings", "prior_findings"],
415	                },
416	            },
417	            "pre_check_flags": {
418	                "type": "array",
419	                "items": {
420	                    "type": "object",
421	                    "properties": {
422	                        "id": {"type": "string"},
423	                        "check": {"type": "string"},
424	                        "detail": {"type": "string"},
425	                        "severity": {"type": "string"},
426	                        "evidence_file": {"type": "string"},
427	                    },
428	                    "required": ["id", "check", "detail", "severity", "evidence_file"],
429	                },
430	            },
431	            "verified_flag_ids": {"type": "array", "items": {"type": "string"}},
432	            "disputed_flag_ids": {"type": "array", "items": {"type": "string"}},
433	            "criteria": {
434	                "type": "array",
435	                "items": {
436	                    "type": "object",
437	                    "properties": {
438	                        "name": {"type": "string"},
439	                        "priority": {"type": "string", "enum": ["must", "should", "info"]},
440	                        "pass": {"type": "string", "enum": ["pass", "fail", "waived"]},
441	                        "evidence": {"type": "string"},
442	                    },
443	                    "required": ["name", "priority", "pass", "evidence"],
444	                },
445	            },
446	            "issues": {"type": "array", "items": {"type": "string"}},
447	            "rework_items": {
448	                "type": "array",
449	                "items": {
450	                    "type": "object",
451	                    "properties": {
452	                        "task_id": {"type": "string"},
453	                        "issue": {"type": "string"},
454	                        "expected": {"type": "string"},
455	                        "actual": {"type": "string"},
456	                        "evidence_file": {"type": "string"},
457	                        "flag_id": {"type": ["string", "null"]},
458	                        "source": {"type": ["string", "null"]},
459	                    },
460	                    "required": ["task_id", "issue", "expected", "actual", "evidence_file", "flag_id", "source"],
461	                },
462	            },
463	            "summary": {"type": "string"},
464	            "task_verdicts": {
465	                "type": "array",
466	                "items": {
467	                    "type": "object",
468	                    "properties": {
469	                        "task_id": {"type": "string"},
470	                        "reviewer_verdict": {"type": "string"},
471	                        "evidence_files": {"type": "array", "items": {"type": "string"}},
472	                    },
473	                    "required": ["task_id", "reviewer_verdict", "evidence_files"],
474	                },
475	            },
476	            "sense_check_verdicts": {
477	                "type": "array",
478	                "items": {
479	                    "type": "object",
480	                    "properties": {
481	                        "sense_check_id": {"type": "string"},
482	                        "verdict": {"type": "string"},
483	                    },
484	                    "required": ["sense_check_id", "verdict"],
485	                },
486	            },
487	        },
488	        "required": [
489	            "review_verdict",
490	            "checks",
491	            "pre_check_flags",
492	            "verified_flag_ids",
493	            "disputed_flag_ids",
494	            "criteria",
495	            "issues",
496	            "rework_items",
497	            "summary",
498	            "task_verdicts",
499	            "sense_check_verdicts",
500	        ],
501	    },
502	}
503	
504	
505	def _build_execution_doc_schema() -> dict[str, Any]:
506	    schema = deepcopy(SCHEMAS["execution.json"])
507	    schema["properties"]["sections_written"] = schema["properties"].pop("files_changed")
508	    task_update_schema = schema["properties"]["task_updates"]["items"]
509	    task_update_schema["properties"]["sections_written"] = task_update_schema["properties"].pop("files_changed")
510	    task_update_schema["properties"].pop("commands_run", None)
511	    task_update_schema["required"] = ["task_id", "status", "executor_notes", "sections_written"]
512	    schema["required"] = [
513	        "output",
514	        "sections_written",
515	        "commands_run",
516	        "deviations",
517	        "task_updates",
518	        "sense_check_acknowledgments",
519	    ]
520	    return schema
521	
522	
523	SCHEMAS["execution_doc.json"] = _build_execution_doc_schema()
524	
525	
526	def get_execution_schema_key(mode: str) -> str:
527	    return "execution_doc.json" if mode == "doc" else "execution.json"
528	
529	
530	def _preserve_explicit_required(path: tuple[str, ...]) -> bool:
531	    # `review.rework_items[]` uses explicit required fields because OpenAI
532	    # structured outputs require every property key to appear in `required`.
533	    return path[-3:] == ("properties", "rework_items", "items")
534	
535	
536	def strict_schema(schema: Any, _path: tuple[str, ...] = ()) -> Any:
537	    if isinstance(schema, dict):
538	        updated = {key: strict_schema(value, _path + (key,)) for key, value in schema.items()}
539	        if updated.get("type") == "object":
540	            updated.setdefault("additionalProperties", False)
541	            if "properties" in updated and not _preserve_explicit_required(_path):
542	                updated["required"] = list(updated["properties"].keys())
543	        return updated
544	    if isinstance(schema, list):
545	        return [strict_schema(item, _path) for item in schema]
546	    return schema
547
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
46	    mode: str = "code",
47	) -> list[str]:
48	    reset_reasons: dict[str, list[str]] = {}
49	    if mode == "doc":
50	        missing_task_ids = _check_done_task_evidence(
51	            finalize_data.get("tasks", []),
52	            issues=issues,
53	            should_classify=lambda task: True,
54	            has_evidence=lambda task: bool(task.get("sections_written")),
55	            has_advisory_evidence=lambda task: True,
56	            missing_message="Done tasks missing sections_written during timeout recovery: ",
57	            advisory_message="",
58	        )
59	    else:
60	        missing_task_ids = _check_done_task_evidence(
61	            finalize_data.get("tasks", []),
62	            issues=issues,
63	            should_classify=lambda task: True,
64	            has_evidence=lambda task: bool(task.get("files_changed")),
65	            has_advisory_evidence=lambda task: bool(task.get("commands_run")),
66	            missing_message="Done tasks missing both files_changed and commands_run during timeout recovery: ",
67	            advisory_message="Advisory: done tasks rely on commands_run without files_changed during timeout recovery: ",
68	        )
69	    for task_id in missing_task_ids:
70	        if mode == "doc":
71	            reset_reasons.setdefault(task_id, []).append("missing sections_written")
72	        else:
73	            reset_reasons.setdefault(task_id, []).append(
74	                "missing both files_changed and commands_run"
75	            )
76	
77	    if mode != "doc" and not execution_audit.get("skipped"):
78	        files_in_diff = {
79	            _normalize_execute_claimed_path(path)
80	            for path in execution_audit.get("files_in_diff", [])
81	            if isinstance(path, str) and path.strip()
82	        }
83	        for task in finalize_data.get("tasks", []):
84	            if task.get("status") != "done":
85	                continue
86	            claimed_paths = [
87	                _normalize_execute_claimed_path(path)
88	                for path in task.get("files_changed", [])
89	                if isinstance(path, str) and path.strip()
90	            ]
91	            if claimed_paths and any(
92	                path not in files_in_diff for path in claimed_paths
93	            ):
94	                reset_reasons.setdefault(task["id"], []).append(
95	                    "claimed files not present in git status"
96	                )
97	
98	    for task in finalize_data.get("tasks", []):
99	        reasons = reset_reasons.get(task.get("id"))
100	        if not reasons:
101	            continue
102	        note_prefix = str(task.get("executor_notes", "")).strip()
103	        reset_note = (
104	            "Timeout recovery reset this task to pending because "
105	            + " and ".join(reasons)
106	            + "."
107	        )
108	        task["status"] = "pending"
109	        task["executor_notes"] = f"{note_prefix} {reset_note}".strip()
110	
111	    if reset_reasons:
112	        issues.append(
113	            "Reset timed-out done tasks to pending after evidence validation: "
114	            + ", ".join(sorted(reset_reasons))
115	        )
116	    return sorted(reset_reasons)
117	
118	
119	def _timeout_checkpoint_path(plan_dir: Path, *, batch_number: int | None) -> Path:
120	    if batch_number is None:
121	        return plan_dir / "execution_checkpoint.json"
122	    return batch_artifact_path(plan_dir, batch_number)
123	
124	
125	def _merge_timeout_checkpoint(
126	    *,
127	    finalize_data: dict[str, Any],
128	    checkpoint_data: dict[str, Any],
129	    checkpoint_name: str,
130	    issues: list[str],
131	    mode: str = "code",
132	) -> None:
133	    tasks_by_id = {
134	        task["id"]: task
135	        for task in finalize_data.get("tasks", [])
136	        if isinstance(task, dict) and isinstance(task.get("id"), str)
137	    }
138	    if mode == "doc":
139	        required_fields = ("task_id", "status", "executor_notes", "sections_written")
140	        merge_fields = ("status", "executor_notes", "sections_written")
141	        array_fields = ("sections_written",)
142	    else:
143	        required_fields = ("task_id", "status", "executor_notes", "files_changed", "commands_run")
144	        merge_fields = ("status", "executor_notes", "files_changed", "commands_run")
145	        array_fields = ("files_changed", "commands_run")
146	    merged_tasks, _ = _validate_and_merge_batch(
147	        checkpoint_data.get("task_updates"),
148	        required_fields=required_fields,
149	        targets_by_id=tasks_by_id,
150	        id_field="task_id",
151	        merge_fields=merge_fields,
152	        issues=issues,
153	        validation_label=f"{checkpoint_name}.task_updates",
154	        merge_label="checkpoint task_update",
155	        enum_fields={"status": {"done", "skipped", "completed"}},
156	        nonempty_fields={"executor_notes"},
157	        array_fields=array_fields,
158	    )
159	    sense_checks_by_id = {
160	        sense_check["id"]: sense_check
161	        for sense_check in finalize_data.get("sense_checks", [])
162	        if isinstance(sense_check, dict) and isinstance(sense_check.get("id"), str)
163	    }
164	    merged_checks, _ = _validate_and_merge_batch(
165	        checkpoint_data.get("sense_check_acknowledgments"),
166	        required_fields=("sense_check_id", "executor_note"),
167	        targets_by_id=sense_checks_by_id,
168	        id_field="sense_check_id",
169	        merge_fields=("executor_note",),
170	        issues=issues,
171	        validation_label=f"{checkpoint_name}.sense_check_acknowledgments",
172	        merge_label="checkpoint sense_check_acknowledgment",
173	        nonempty_fields={"executor_note"},
174	    )
175	    if merged_tasks > 0 or merged_checks > 0:
176	        issues.append(
177	            f"Recovered timeout checkpoint from {checkpoint_name}: merged {merged_tasks} task update(s) and {merged_checks} sense check acknowledgment(s)."
178	        )
179	
180	
181	def _recover_execute_timeout(
182	    *,
183	    plan_dir: Path,
184	    state: PlanState,
185	    error: CliError,
186	    agent: str,
187	    mode: str,
188	    refreshed: bool,
189	    auto_approve: bool,
190	    args: argparse.Namespace,
191	    batch_number: int | None,
192	    persist_state: bool = True,
193	) -> StepResponse:
194	    deviations = [f"Execute timed out: {error.message}"]
195	    finalize_data = read_json(plan_dir / "finalize.json")
196	    project_dir = Path(state["config"]["project_dir"])
197	    plan_mode = state["config"].get("mode", "code")
198	    checkpoint_path = _timeout_checkpoint_path(plan_dir, batch_number=batch_number)
199	    try:
200	        checkpoint_data = read_json(checkpoint_path)
201	    except FileNotFoundError:
202	        deviations.append(
203	            f"Advisory: timeout checkpoint {checkpoint_path.name} was not found."
204	        )
205	    except json.JSONDecodeError as exc:
206	        deviations.append(
207	            f"Advisory: timeout checkpoint {checkpoint_path.name} was not valid JSON: {exc}"
208	        )
209	    else:
210	        if isinstance(checkpoint_data, dict):
211	            _merge_timeout_checkpoint(
212	                finalize_data=finalize_data,
213	                checkpoint_data=checkpoint_data,
214	                checkpoint_name=checkpoint_path.name,
215	                issues=deviations,
216	                mode=plan_mode,
217	            )
218	        else:
219	            deviations.append(
220	                f"Advisory: timeout checkpoint {checkpoint_path.name} did not contain an object."
221	            )
222	
223	    initial_audit = validate_execution_evidence(finalize_data, project_dir, mode=plan_mode)
224	
225	    if initial_audit["skipped"]:
226	        deviations.append(
227	            f"Advisory audit skip during timeout recovery: {initial_audit['reason']}"
228	        )
229	    for finding in initial_audit["findings"]:
230	        deviations.append(f"Advisory audit finding during timeout recovery: {finding}")
231	
232	    _reset_timeout_invalid_tasks(
233	        finalize_data,
234	        execution_audit=initial_audit,
235	        issues=deviations,
236	        mode=plan_mode,
237	    )
238	    execution_audit = validate_execution_evidence(finalize_data, project_dir, mode=plan_mode)
239	    atomic_write_json(plan_dir / "execution_audit.json", execution_audit)
240	    atomic_write_json(plan_dir / "finalize.json", finalize_data)
241	    atomic_write_text(
242	        plan_dir / "final.md", render_final_md(finalize_data, phase="execute")
243	    )
244	
245	    finalize_hash = sha256_file(plan_dir / "finalize.json")
246	    raw_output = str(error.extra.get("raw_output") or error.message)
247	    raw_name = store_raw_worker_output(
248	        plan_dir, "execute", state["iteration"], raw_output
249	    )
250	    session_id = error.extra.get("session_id")
251	    timeout_worker = WorkerResult(
252	        payload={},
253	        raw_output=raw_output,
254	        duration_ms=0,
255	        cost_usd=0.0,
256	        session_id=session_id if isinstance(session_id, str) else None,
257	    )
258	    if persist_state:
259	        apply_session_update(
260	            state,
261	            "execute",
262	            agent,
263	            timeout_worker.session_id,
264	            mode=mode,
265	            refreshed=refreshed,
266	        )
267	    user_approved_gate = bool(state["meta"].get("user_approved_gate", False))
268	    approval_mode = _resolve_execute_approval_mode(
269	        auto_approve=auto_approve,
270	        user_approved_gate=user_approved_gate,
271	    )
272	    if persist_state:
273	        append_history(
274	            state,
275	            make_history_entry(
276	                "execute",
277	                duration_ms=0,
278	                cost_usd=0.0,
279	                result="timeout",
280	                worker=timeout_worker,
281	                agent=agent,
282	                mode=mode,
283	                output_file="finalize.json",
284	                artifact_hash=finalize_hash,
285	                finalize_hash=finalize_hash,
286	                raw_output_file=raw_name,
287	                message=error.message,
288	                approval_mode=approval_mode,
289	            ),
290	        )
291	        save_state(plan_dir, state)
292	
293	    tasks = finalize_data.get("tasks", [])
294	    completed_tasks = [
295	        task for task in tasks if task.get("status") in {"done", "skipped"}
296	    ]
297	    if plan_mode == "doc":
298	        files_changed = sorted(
299	            {
300	                section
301	                for task in completed_tasks
302	                for section in task.get("sections_written", [])
303	                if isinstance(section, str) and section.strip()
304	            }
305	        )
306	    else:
307	        files_changed = sorted(
308	            {
309	                path
310	                for task in completed_tasks
311	                for path in task.get("files_changed", [])
312	                if isinstance(path, str) and path.strip()
313	            }
314	        )
315	    summary = (
316	        "Execute timed out after partial progress. "
317	        f"{len(completed_tasks)}/{len(tasks)} tasks remain marked done or skipped on disk. "
318	        "Re-run execute to finish and re-emit structured output."
319	    )
320	    response: StepResponse = {
321	        "success": False,
322	        "step": "execute",
323	        "summary": summary,
324	        "artifacts": ["execution_audit.json", "finalize.json", "final.md"],
325	        "next_step": "execute",
326	        "state": STATE_FINALIZED,
327	        "files_changed": files_changed,
328	        "deviations": deviations,
329	        "warnings": [summary],
330	        "auto_approve": auto_approve,
331	        "user_approved_gate": user_approved_gate,
332	    }
333	    return response
334
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
32	    mode: str
33	    output_path: str
34	    agents: dict[str, str]
35	
36	
37	class PlanMeta(TypedDict, total=False):
38	    significant_counts: list[int]
39	    weighted_scores: list[float]
40	    plan_deltas: list[float | None]
41	    recurring_critiques: list[str]
42	    total_cost_usd: float
43	    overrides: list[dict[str, Any]]
44	    notes: list[dict[str, Any]]
45	    user_approved_gate: bool
46	
47	
48	class SessionInfo(TypedDict, total=False):
49	    id: str
50	    mode: str
51	    created_at: str
52	    last_used_at: str
53	    refreshed: bool
54	
55	
56	class ActiveStep(TypedDict, total=False):
57	    step: str
58	    agent: str
59	    mode: str
60	    model: str
61	    run_id: str
62	    session_id: str
63	    started_at: str
64	
65	
66	class PlanVersionRecord(TypedDict, total=False):
67	    version: int
68	    file: str
69	    hash: str
70	    timestamp: str
71	
72	
73	class HistoryEntry(TypedDict, total=False):
74	    step: str
75	    timestamp: str
76	    duration_ms: int
77	    cost_usd: float
78	    result: str
79	    session_mode: str
80	    session_id: str
81	    agent: str
82	    output_file: str
83	    artifact_hash: str
84	    finalize_hash: str
85	    raw_output_file: str
86	    message: str
87	    flags_count: int
88	    flags_addressed: list[str]
89	    recommendation: str
90	    approval_mode: str
91	    environment: dict[str, bool]
92	
93	
94	class ClarificationRecord(TypedDict, total=False):
95	    refined_idea: str
96	    intent_summary: str
97	    questions: list[str]
98	
99	
100	class LastGateRecord(TypedDict, total=False):
101	    recommendation: str
102	    rationale: str
103	    signals_assessment: str
104	    warnings: list[str]
105	    settled_decisions: list["SettledDecision"]
106	    passed: bool
107	    preflight_results: dict[str, bool]
108	    orchestrator_guidance: str
109	
110	
111	class PlanState(TypedDict):
112	    name: str
113	    idea: str
114	    current_state: str
115	    iteration: int
116	    created_at: str
117	    config: PlanConfig
118	    sessions: dict[str, SessionInfo]
119	    plan_versions: list[PlanVersionRecord]
120	    history: list[HistoryEntry]
121	    meta: PlanMeta
122	    last_gate: LastGateRecord
123	    active_step: NotRequired[ActiveStep]
124	    clarification: NotRequired[ClarificationRecord]
125	
126	
127	class _FlagRecordRequired(TypedDict):
128	    id: str
129	    concern: str
130	    category: str
131	    status: str
132	
133	
134	class FlagRecord(_FlagRecordRequired, total=False):
135	    severity_hint: str
136	    evidence: str
137	    raised_in: str
138	    severity: str
139	    verified: bool
140	    verified_in: str
141	    addressed_in: str
142	
143	
144	class FlagRegistry(TypedDict):
145	    flags: list[FlagRecord]
146	
147	
148	class GateCheckResult(TypedDict):
149	    passed: bool
150	    criteria_check: dict[str, Any]
151	    preflight_results: dict[str, bool]
152	    unresolved_flags: list[FlagRecord]
153	
154	
155	class SettledDecision(TypedDict, total=False):
156	    id: str
157	    decision: str
158	    rationale: str
159	
160	
161	class GatePayload(TypedDict):
162	    recommendation: str
163	    rationale: str
164	    signals_assessment: str
165	    warnings: list[str]
166	    settled_decisions: list[SettledDecision]
167	
168	
169	class GateArtifact(TypedDict, total=False):
170	    passed: bool
171	    criteria_check: dict[str, Any]
172	    preflight_results: dict[str, bool]
173	    unresolved_flags: list[FlagRecord]
174	    recommendation: str
175	    rationale: str
176	    signals_assessment: str
177	    warnings: list[str]
178	    settled_decisions: list[SettledDecision]
179	    override_forced: bool
180	    orchestrator_guidance: str
181	    robustness: str
182	    signals: dict[str, Any]
183	
184	
185	class GateSignals(TypedDict, total=False):
186	    robustness: str
187	    signals: dict[str, Any]
188	    warnings: list[str]
189	
190	
191	class StepResponse(TypedDict, total=False):
192	    success: bool
193	    step: str
194	    summary: str
195	    artifacts: list[str]
196	    next_step: str | None
197	    state: str
198	    auto_approve: bool
199	    robustness: str
200	    iteration: int
201	    plan: str
202	    plan_dir: str
203	    questions: list[str]
204	    verified_flags: list[str]
205	    open_flags: list[str]
206	    scope_creep_flags: list[str]
207	    warnings: list[str]
208	    files_changed: list[str]
209	    deviations: list[str]
210	    user_approved_gate: bool
211	    issues: list[str]
212	    valid_next: list[str]
213	    mode: str
214	    installed: list[dict[str, Any]]
215	    config_path: str
216	    routing: dict[str, str]
217	    raw_config: dict[str, Any]
218	    action: str
219	    key: str
220	    value: str
221	    skipped: bool
222	    file: str
223	    plans: list[dict[str, Any]]
224	    recommendation: str
225	    signals: dict[str, Any]
226	    rationale: str
227	    signals_assessment: str
228	    orchestrator_guidance: str
229	    passed: bool
230	    criteria_check: dict[str, Any]
231	    preflight_results: dict[str, bool]
232	    unresolved_flags: list[Any]
233	    error: str
234	    message: str
235	    details: dict[str, Any]
236	    agent_fallback: dict[str, str]
237	
238	
239	class DebtEntry(TypedDict):
240	    id: str
241	    subsystem: str
242	    concern: str
243	    flag_ids: list[str]
244	    plan_ids: list[str]
245	    occurrence_count: int
246	    created_at: str
247	    updated_at: str
248	    resolved: bool
249	    resolved_by: str | None
250	    resolved_at: str | None
251	
252	
253	class DebtRegistry(TypedDict):
254	    entries: list[DebtEntry]
255	
256	
257	# ---------------------------------------------------------------------------
258	# Constants
259	# ---------------------------------------------------------------------------
260	
261	FLAG_BLOCKING_STATUSES = {"open", "disputed", "addressed"}
262	FLAG_VALID_STATUSES = {
263	    "open", "addressed", "disputed", "verified",
264	    "accepted_tradeoff", "gate_disputed",
265	}
266	DEBT_ESCALATION_THRESHOLD = 3
267	MOCK_ENV_VAR = "MEGAPLAN_MOCK_WORKERS"
268	
269	DEFAULT_AGENT_ROUTING: dict[str, str] = {
270	    "plan": "claude",
271	    "prep": "claude",
272	    "critique": "codex",
273	    "revise": "claude",
274	    "gate": "claude",
275	    "finalize": "claude",
276	    "execute": "codex",
277	    "loop_plan": "claude",
278	    "loop_execute": "codex",
279	    "review": "codex",
280	}
281	KNOWN_AGENTS = ["claude", "codex", "hermes"]
282	ROBUSTNESS_LEVELS = ("tiny", "light", "standard", "robust", "superrobust")
283	def parse_agent_spec(spec: str) -> tuple[str, str | None]:
284	    """Parse 'hermes:model/name' → ('hermes', 'model/name') or 'claude' → ('claude', None)."""
285	    if ":" in spec:
286	        agent, model = spec.split(":", 1)
287	        return agent, model
288	    return spec, None
289	
290	
291	SCOPE_CREEP_TERMS = (
292	    "scope creep",
293	    "out of scope",
294	    "beyond the original idea",
295	    "beyond original idea",
296	    "beyond user intent",
297	    "expanded scope",
298	)
299	
300	DEFAULTS = {
301	    "execution.auto_approve": False,
302	    "execution.robustness": "standard",
303	    "execution.worker_timeout_seconds": 7200,
304	    "execution.max_review_rework_cycles": 3,
305	    "execution.max_robust_review_rework_cycles": 2,
306	    "execution.max_execute_no_progress": 3,
307	    "orchestration.max_critique_concurrency": 2,
308	    "orchestration.mode": "subagent",
309	}
310	
311	_SETTABLE_BOOL = {
312	    "execution.auto_approve",
313	}
314	
315	_SETTABLE_ENUM = {
316	    "execution.robustness": ROBUSTNESS_LEVELS,
317	}
318	
319	_SETTABLE_NUMERIC = {
320	    "execution.worker_timeout_seconds",
321	    "execution.max_review_rework_cycles",
322	    "execution.max_robust_review_rework_cycles",
323	    "execution.max_execute_no_progress",
324	    "orchestration.max_critique_concurrency",
325	}
326	
327	
328	# ---------------------------------------------------------------------------
329	# Exception
330	# ---------------------------------------------------------------------------
331	
332	class CliError(Exception):
333	    def __init__(
334	        self,
335	        code: str,
336	        message: str,
337	        *,
338	        valid_next: list[str] | None = None,
339	        extra: dict[str, Any] | None = None,
340	        exit_code: int = 1,
341	    ) -> None:
342	        super().__init__(message)
343	        self.code = code
344	        self.message = message
345	        self.valid_next = valid_next or []
346	        self.extra = extra or {}
347	        self.exit_code = exit_code
348
```

> AGENT

Now let me read the handlers.py file in sections to find handle_init and _write_finalize_artifacts:

> TOOL

tool_use Grep
```json
{
  "pattern": "def handle_init|def _write_finalize_artifacts",
  "path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "output_mode": "content"
}
```

> TOOL

tool_result Grep
```
376:def _write_finalize_artifacts(plan_dir: Path, payload: dict[str, Any], state: PlanState) -> str:
722:def handle_init(root: Path, args: argparse.Namespace) -> StepResponse:
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 722,
  "limit": 100
}
```

> TOOL

tool_result Read
```
722	def handle_init(root: Path, args: argparse.Namespace) -> StepResponse:
723	    ensure_runtime_layout(root)
724	    project_dir = Path(args.project_dir).expanduser().resolve()
725	    if not project_dir.exists() or not project_dir.is_dir():
726	        raise CliError("invalid_project_dir", f"Project directory does not exist: {project_dir}")
727	    mode = getattr(args, "mode", "code") or "code"
728	    raw_output_path = getattr(args, "output", None)
729	    normalized_output_path: str | None = None
730	    if mode == "doc" and not raw_output_path:
731	        raise CliError("invalid_args", "--output is required when --mode doc is selected")
732	    if raw_output_path:
733	        output_candidate = Path(raw_output_path)
734	        if output_candidate.is_absolute():
735	            raise CliError("invalid_args", "--output must be a relative path inside the project directory")
736	        if any(part == ".." for part in output_candidate.parts):
737	            raise CliError("invalid_args", "--output must not contain '..' path traversal")
738	        resolved_output_path = (project_dir / output_candidate).resolve()
739	        try:
740	            normalized_output_path = resolved_output_path.relative_to(project_dir).as_posix()
741	        except ValueError as exc:
742	            raise CliError("invalid_args", "--output must stay within the project directory") from exc
743	    robustness = getattr(args, "robustness", None)
744	    if robustness is None:
745	        robustness = get_effective("execution", "robustness")
746	    if robustness not in ROBUSTNESS_LEVELS:
747	        robustness = "standard"
748	    auto_approve_value = getattr(args, "auto_approve", None)
749	    if auto_approve_value is None:
750	        auto_approve_value = get_effective("execution", "auto_approve")
751	    auto_approve = bool(auto_approve_value)
752	    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
753	    plan_name = args.name or f"{slugify(args.idea)}-{timestamp}"
754	    plan_dir = plans_root(root) / plan_name
755	    if plan_dir.exists():
756	        raise CliError("duplicate_plan", f"Plan directory already exists: {plan_name}")
757	    plan_dir.mkdir(parents=True, exist_ok=False)
758	
759	    state: PlanState = {
760	        "name": plan_name,
761	        "idea": args.idea,
762	        "current_state": STATE_INITIALIZED,
763	        "iteration": 0,
764	        "created_at": now_utc(),
765	        "config": {
766	            "project_dir": str(project_dir),
767	            "auto_approve": auto_approve,
768	            "robustness": robustness,
769	            "mode": mode,
770	            "agent": "hermes" if getattr(args, "hermes", None) is not None else "",
771	        },
772	        "sessions": {},
773	        "plan_versions": [],
774	        "history": [],
775	        "meta": {
776	            "significant_counts": [],
777	            "weighted_scores": [],
778	            "plan_deltas": [],
779	            "recurring_critiques": [],
780	            "total_cost_usd": 0.0,
781	            "overrides": [],
782	            "notes": [],
783	        },
784	        "last_gate": {},
785	    }
786	    if normalized_output_path is not None:
787	        state["config"]["output_path"] = normalized_output_path
788	    append_history(
789	        state,
790	        make_history_entry(
791	            "init",
792	            duration_ms=0,
793	            cost_usd=0.0,
794	            result="success",
795	            environment={
796	                "claude": bool(find_command("claude")),
797	                "codex": bool(find_command("codex")),
798	            },
799	        ),
800	    )
801	    save_state(plan_dir, state)
802	    next_steps = workflow_next(state)
803	    response: StepResponse = {
804	        "success": True,
805	        "step": "init",
806	        "plan": plan_name,
807	        "state": STATE_INITIALIZED,
808	        "summary": f"Initialized plan '{plan_name}' for project {project_dir}",
809	        "artifacts": ["state.json"],
810	        "next_step": next_steps[0] if next_steps else None,
811	        "auto_approve": auto_approve,
812	        "robustness": robustness,
813	    }
814	    _attach_next_step_runtime(response)
815	    return response
816	
817	
818	def handle_plan(root: Path, args: argparse.Namespace) -> StepResponse:
819	    with load_plan_locked(root, args.plan, step="plan") as (plan_dir, state):
820	        require_state(state, "plan", {STATE_INITIALIZED, STATE_PREPPED, STATE_PLANNED})
821	        rerun = state["current_state"] == STATE_PLANNED
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/handlers.py",
  "offset": 376,
  "limit": 150
}
```

> TOOL

tool_result Read
```
376	def _write_finalize_artifacts(plan_dir: Path, payload: dict[str, Any], state: PlanState) -> str:
377	    if state["config"].get("mode") == "doc":
378	        payload["baseline_test_failures"] = None
379	        payload["baseline_test_command"] = None
380	        payload["baseline_test_note"] = "Test baseline not applicable in doc mode."
381	    else:
382	        baseline = _capture_test_baseline(Path(state["config"]["project_dir"]), state.get("config", {}))
383	        payload.update(baseline)
384	        _ensure_verification_task(payload, state)
385	    _reconcile_validation_after_mutation(payload)
386	    atomic_write_json(plan_dir / "finalize.json", payload)
387	    atomic_write_json(plan_dir / "finalize_snapshot.json", payload)
388	    atomic_write_text(plan_dir / "final.md", render_final_md(payload))
389	    return sha256_file(plan_dir / "finalize.json")
390	
391	
392	def _reconcile_validation_after_mutation(payload: dict[str, Any]) -> None:
393	    """Ensure validation block is consistent with the (possibly mutated) task list.
394	
395	    After _ensure_verification_task() may have appended a task, update the
396	    validation block so orphan_tasks includes any handler-injected tasks.
397	    """
398	    validation = payload.get("validation")
399	    if not validation or not isinstance(validation, dict):
400	        return
401	    task_ids = {t["id"] for t in payload.get("tasks", []) if isinstance(t, dict)}
402	    covered_ids: set[str] = set()
403	    for entry in validation.get("plan_steps_covered", []):
404	        if isinstance(entry, dict):
405	            for tid in entry.get("finalize_task_ids", []):
406	                covered_ids.add(tid)
407	    orphan_ids = set(validation.get("orphan_tasks", []))
408	    for tid in task_ids:
409	        if tid not in covered_ids and tid not in orphan_ids:
410	            orphan_ids.add(tid)
411	    validation["orphan_tasks"] = sorted(orphan_ids)
412	
413	
414	def _validate_finalize_payload(plan_dir: Path, state: PlanState, worker: WorkerResult) -> None:
415	    payload = worker.payload
416	
417	    def _reject(message: str) -> None:
418	        _raise_step_validation_error(
419	            plan_dir=plan_dir, state=state, step="finalize",
420	            iteration=state["iteration"], worker=worker,
421	            code="invalid_finalize", message=message,
422	        )
423	
424	    tasks = payload.get("tasks")
425	    if not isinstance(tasks, list) or not tasks:
426	        _reject("Finalize output must include a non-empty `tasks` list.")
427	    if not isinstance(payload.get("sense_checks"), list):
428	        _reject("Finalize output must include a `sense_checks` list.")
429	    if not isinstance(payload.get("watch_items"), list):
430	        _reject("Finalize output must include a `watch_items` list.")
431	    for index, task in enumerate(tasks, start=1):
432	        tid = task.get("id", index) if isinstance(task, dict) else index
433	        if not isinstance(task, dict):
434	            _reject(f"Finalize task {index} must be an object.")
435	        if not isinstance(task.get("id"), str) or not task["id"].strip():
436	            _reject(f"Finalize task {index} is missing a non-empty `id`.")
437	        if not isinstance(task.get("description"), str) or not task["description"].strip():
438	            _reject(f"Finalize task {tid} is missing a non-empty `description`.")
439	        if task.get("status") != "pending":
440	            _reject(f"Finalize task {tid} must start with status `pending`.")
441	
442	
443	def _build_gate_signals_artifact(
444	    plan_dir: Path,
445	    state: PlanState,
446	    *,
447	    iteration: int,
448	    root: Path,
449	) -> tuple[dict[str, Any], str, dict[str, Any]]:
450	    gate_signals = build_gate_signals(plan_dir, state, root=root)
451	    gate_checks = run_gate_checks(plan_dir, state, command_lookup=find_command)
452	    signals_artifact = {
453	        "robustness": gate_signals["robustness"],
454	        "signals": gate_signals["signals"],
455	        "warnings": gate_signals.get("warnings", []),
456	        "criteria_check": gate_checks["criteria_check"],
457	        "preflight_results": gate_checks["preflight_results"],
458	        "unresolved_flags": gate_checks["unresolved_flags"],
459	    }
460	    signals_filename = f"gate_signals_v{iteration}.json"
461	    atomic_write_json(plan_dir / signals_filename, signals_artifact)
462	    return gate_signals, signals_filename, signals_artifact
463	
464	
465	def _record_gate_debt_entries(
466	    root: Path,
467	    state: PlanState,
468	    gate_summary: dict[str, Any],
469	    worker_payload: dict[str, Any],
470	) -> int:
471	    if gate_summary["recommendation"] != "PROCEED":
472	        return 0
473	
474	    raw_tradeoffs = worker_payload.get("accepted_tradeoffs", [])
475	    accepted_tradeoffs = [
476	        item
477	        for item in raw_tradeoffs
478	        if isinstance(item, dict)
479	        and isinstance(item.get("flag_id"), str)
480	        and isinstance(item.get("concern"), str)
481	    ] if isinstance(raw_tradeoffs, list) else []
482	    has_explicit_resolutions = any(
483	        isinstance(item, dict) for item in gate_summary.get("flag_resolutions", [])
484	    )
485	    debt_registry = load_debt_registry(root)
486	    debt_entries_added = 0
487	    if accepted_tradeoffs:
488	        for tradeoff in accepted_tradeoffs:
489	            subsystem_value = tradeoff.get("subsystem")
490	            subsystem = (
491	                subsystem_value
492	                if isinstance(subsystem_value, str) and subsystem_value.strip()
493	                else extract_subsystem_tag(tradeoff["concern"])
494	            )
495	            add_or_increment_debt(
496	                debt_registry,
497	                subsystem=subsystem,
498	                concern=tradeoff["concern"],
499	                flag_ids=[tradeoff["flag_id"]],
500	                plan_id=state["name"],
501	            )
502	            debt_entries_added += 1
503	    elif not has_explicit_resolutions:
504	        for flag in gate_summary["unresolved_flags"]:
505	            if not isinstance(flag, dict):
506	                continue
507	            flag_id = flag.get("id")
508	            concern = flag.get("concern")
509	            if not isinstance(flag_id, str) or not isinstance(concern, str):
510	                continue
511	            add_or_increment_debt(
512	                debt_registry,
513	                subsystem=extract_subsystem_tag(concern),
514	                concern=concern,
515	                flag_ids=[flag_id],
516	                plan_id=state["name"],
517	            )
518	            debt_entries_added += 1
519	    if debt_entries_added:
520	        save_debt_registry(root, debt_registry)
521	    return debt_entries_added
522	
523	
524	def _resolve_revise_transition(state: PlanState) -> tuple[bool, Any]:
525	    has_gate = workflow_includes_step(configured_robustness(state), "gate")
```

> AGENT

Now let me search for execution_timeout.py details:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/megaplan/megaplan/execution_timeout.py",
  "offset": 1,
  "limit": 180
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
46	    mode: str = "code",
47	) -> list[str]:
48	    reset_reasons: dict[str, list[str]] = {}
49	    if mode == "doc":
50	        missing_task_ids = _check_done_task_evidence(
51	            finalize_data.get("tasks", []),
52	            issues=issues,
53	            should_classify=lambda task: True,
54	            has_evidence=lambda task: bool(task.get("sections_written")),
55	            has_advisory_evidence=lambda task: True,
56	            missing_message="Done tasks missing sections_written during timeout recovery: ",
57	            advisory_message="",
58	        )
59	    else:
60	        missing_task_ids = _check_done_task_evidence(
61	            finalize_data.get("tasks", []),
62	            issues=issues,
63	            should_classify=lambda task: True,
64	            has_evidence=lambda task: bool(task.get("files_changed")),
65	            has_advisory_evidence=lambda task: bool(task.get("commands_run")),
66	            missing_message="Done tasks missing both files_changed and commands_run during timeout recovery: ",
67	            advisory_message="Advisory: done tasks rely on commands_run without files_changed during timeout recovery: ",
68	        )
69	    for task_id in missing_task_ids:
70	        if mode == "doc":
71	            reset_reasons.setdefault(task_id, []).append("missing sections_written")
72	        else:
73	            reset_reasons.setdefault(task_id, []).append(
74	                "missing both files_changed and commands_run"
75	            )
76	
77	    if mode != "doc" and not execution_audit.get("skipped"):
78	        files_in_diff = {
79	            _normalize_execute_claimed_path(path)
80	            for path in execution_audit.get("files_in_diff", [])
81	            if isinstance(path, str) and path.strip()
82	        }
83	        for task in finalize_data.get("tasks", []):
84	            if task.get("status") != "done":
85	                continue
86	            claimed_paths = [
87	                _normalize_execute_claimed_path(path)
88	                for path in task.get("files_changed", [])
89	                if isinstance(path, str) and path.strip()
90	            ]
91	            if claimed_paths and any(
92	                path not in files_in_diff for path in claimed_paths
93	            ):
94	                reset_reasons.setdefault(task["id"], []).append(
95	                    "claimed files not present in git status"
96	                )
97	
98	    for task in finalize_data.get("tasks", []):
99	        reasons = reset_reasons.get(task.get("id"))
100	        if not reasons:
101	            continue
102	        note_prefix = str(task.get("executor_notes", "")).strip()
103	        reset_note = (
104	            "Timeout recovery reset this task to pending because "
105	            + " and ".join(reasons)
106	            + "."
107	        )
108	        task["status"] = "pending"
109	        task["executor_notes"] = f"{note_prefix} {reset_note}".strip()
110	
111	    if reset_reasons:
112	        issues.append(
113	            "Reset timed-out done tasks to pending after evidence validation: "
114	            + ", ".join(sorted(reset_reasons))
115	        )
116	    return sorted(reset_reasons)
117	
118	
119	def _timeout_checkpoint_path(plan_dir: Path, *, batch_number: int | None) -> Path:
120	    if batch_number is None:
121	        return plan_dir / "execution_checkpoint.json"
122	    return batch_artifact_path(plan_dir, batch_number)
123	
124	
125	def _merge_timeout_checkpoint(
126	    *,
127	    finalize_data: dict[str, Any],
128	    checkpoint_data: dict[str, Any],
129	    checkpoint_name: str,
130	    issues: list[str],
131	    mode: str = "code",
132	) -> None:
133	    tasks_by_id = {
134	        task["id"]: task
135	        for task in finalize_data.get("tasks", [])
136	        if isinstance(task, dict) and isinstance(task.get("id"), str)
137	    }
138	    if mode == "doc":
139	        required_fields = ("task_id", "status", "executor_notes", "sections_written")
140	        merge_fields = ("status", "executor_notes", "sections_written")
141	        array_fields = ("sections_written",)
142	    else:
143	        required_fields = ("task_id", "status", "executor_notes", "files_changed", "commands_run")
144	        merge_fields = ("status", "executor_notes", "files_changed", "commands_run")
145	        array_fields = ("files_changed", "commands_run")
146	    merged_tasks, _ = _validate_and_merge_batch(
147	        checkpoint_data.get("task_updates"),
148	        required_fields=required_fields,
149	        targets_by_id=tasks_by_id,
150	        id_field="task_id",
151	        merge_fields=merge_fields,
152	        issues=issues,
153	        validation_label=f"{checkpoint_name}.task_updates",
154	        merge_label="checkpoint task_update",
155	        enum_fields={"status": {"done", "skipped", "completed"}},
156	        nonempty_fields={"executor_notes"},
157	        array_fields=array_fields,
158	    )
159	    sense_checks_by_id = {
160	        sense_check["id"]: sense_check
161	        for sense_check in finalize_data.get("sense_checks", [])
162	        if isinstance(sense_check, dict) and isinstance(sense_check.get("id"), str)
163	    }
164	    merged_checks, _ = _validate_and_merge_batch(
165	        checkpoint_data.get("sense_check_acknowledgments"),
166	        required_fields=("sense_check_id", "executor_note"),
167	        targets_by_id=sense_checks_by_id,
168	        id_field="sense_check_id",
169	        merge_fields=("executor_note",),
170	        issues=issues,
171	        validation_label=f"{checkpoint_name}.sense_check_acknowledgments",
172	        merge_label="checkpoint sense_check_acknowledgment",
173	        nonempty_fields={"executor_note"},
174	    )
175	    if merged_tasks > 0 or merged_checks > 0:
176	        issues.append(
177	            f"Recovered timeout checkpoint from {checkpoint_name}: merged {merged_tasks} task update(s) and {merged_checks} sense check acknowledgment(s)."
178	        )
179	
180
```

> AGENT

Perfect! Now I have all the information I need. Let me compile the key findings:

## Key Function Signatures and Logic for Testing

### 1. **megaplan/handlers.py**

**`handle_init()` - Lines 722-815**
- **Doc-mode validation (lines 730-742):**
  - Line 730-731: `if mode == "doc" and not raw_output_path: raise CliError("invalid_args", "--output is required when --mode doc is selected")`
  - Line 734-735: Rejects absolute paths: `if output_candidate.is_absolute(): raise CliError("invalid_args", "--output must be a relative path inside the project directory")`
  - Line 736-737: Blocks `..` traversal: `if any(part == ".." for part in output_candidate.parts): raise CliError("invalid_args", "--output must not contain '..' path traversal")`
  - Line 738-742: Ensures output stays within project dir via `relative_to()` check

**`_write_finalize_artifacts()` - Lines 376-389**
- **Doc-mode branch (lines 377-380):**
  - Line 377: `if state["config"].get("mode") == "doc":`
  - Lines 378-380: Skips test baseline and verification task:
    - Sets `payload["baseline_test_failures"] = None`
    - Sets `payload["baseline_test_command"] = None`
    - Sets `payload["baseline_test_note"] = "Test baseline not applicable in doc mode."`
  - **Code-mode branch (lines 381-384):** Calls `_capture_test_baseline()` and `_ensure_verification_task()`

---

### 2. **megaplan/evaluation.py**

**`validate_execution_evidence()` - Lines 123-126**
- Router function:
  - Line 124: `if mode == "doc": return _validate_execution_evidence_doc(finalize_data, project_dir)`
  - Line 126: Else returns `_validate_execution_evidence_code(finalize_data, project_dir)`

**`_validate_execution_evidence_doc()` - Lines 129-199**
- **Key logic:**
  - Lines 137-145: Collects `claimed_sections` and `planned_sections` from task `sections_written` field
  - Lines 147-151: Checks for missing sections: `missing_sections = sorted(planned_sections - claimed_sections)`
  - Lines 154-159: Checks for unclaimed sections: `unclaimed = sorted(claimed_sections - planned_sections)`
  - Lines 170-179: Validates sense check acknowledgments (requires non-empty `executor_note`, rejects perfunctory acks)
  - Lines 181-191: Validates task executor_notes (rejects rubber stamps for done tasks)
  - Returns dict with `findings`, `files_in_diff: []`, `files_claimed: []`, `skipped: False`

---

### 3. **megaplan/doc_assembly.py** - Full file (Lines 1-118)

**`extract_sections()` - Lines 13-31**
- Maps `section_id → executor_notes` from done tasks' `sections_written`
- Returns `dict[str, str]`

**`assemble_doc()` - Lines 65-117**
- Reads batch payloads (`execution_batch_N.json`)
- Orders sections by task position using `_section_plan_order()`
- Writes atomically to `output_path` via temp file + `os.replace()`

---

### 4. **megaplan/schemas.py**

**`get_execution_schema_key()` - Lines 526-527**
- Router: `return "execution_doc.json" if mode == "doc" else "execution.json"`

**`execution_doc.json` schema - Built by `_build_execution_doc_schema()` Lines 505-523**
- Line 507: Replaces `files_changed` with `sections_written` in root schema
- Lines 508-511: Modifies task_update schema:
  - Adds `sections_written` property
  - Removes `commands_run` property
  - Required fields: `["task_id", "status", "executor_notes", "sections_written"]`
- Stored in `SCHEMAS["execution_doc.json"]` at line 523

---

### 5. **megaplan/execution_timeout.py**

**`_merge_timeout_checkpoint()` - Lines 125-178**
- **Doc-mode branch (lines 138-141):**
  - `required_fields = ("task_id", "status", "executor_notes", "sections_written")`
  - `merge_fields = ("status", "executor_notes", "sections_written")`
  - `array_fields = ("sections_written",)`
- **Code-mode branch (lines 143-145):**
  - `required_fields = ("task_id", "status", "executor_notes", "files_changed", "commands_run")`
  - `merge_fields = ("status", "executor_notes", "files_changed", "commands_run")`
  - `array_fields = ("files_changed", "commands_run")`

**`_reset_timeout_invalid_tasks()` - Lines 41-116**
- **Doc-mode branch (lines 49-58):**
  - Line 54: Checks `has_evidence=lambda task: bool(task.get("sections_written"))`
  - Line 56: Message: `"Done tasks missing sections_written during timeout recovery: "`
  - Line 71: Reset reason: `"missing sections_written"`
- **Code-mode branch (lines 60-68):**
  - Lines 64-65: Checks `files_changed` and `commands_run`
  - Line 77: **Skip git-status check in doc-mode:** `if mode != "doc" and not execution_audit.get("skipped"):`

---

### 6. **megaplan/types.py**

**`PlanConfig` TypedDict - Lines 28-34**
- Line 32: `mode: str` - stores "code" or "doc"
- Line 33: `output_path: str` - relative path for doc output
- Set in `handle_init()` at lines 769, 787

---

## Summary of Test Coverage Needed

1. **Validation in `handle_init`**: Test all three error conditions (missing --output, absolute path, .. traversal)
2. **Finalize artifact branching**: Test that doc-mode skips baseline/verification, code-mode executes them
3. **Evidence validation**: Test doc-mode section tracking vs code-mode file tracking
4. **Timeout recovery**: Test doc-mode uses `sections_written`, code-mode uses `files_changed`, and git-status check is skipped in doc-mode
5. **Schema selection**: Test `get_execution_schema_key()` returns correct schema for each mode
6. **Doc assembly**: Test `extract_sections()` and `assemble_doc()` with section ordering
