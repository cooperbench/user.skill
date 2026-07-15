> TOOL

tool_use Bash
id: toolu_01X8YmV9QdxkthLKRrKBJ93a
```json
{
  "command": "ls /home/armel/Projects/OSS/bmad-module-skill-forge/_bmad/config.yaml /home/armel/Projects/OSS/bmad-module-skill-forge/_bmad/config.user.yaml /home/armel/Projects/OSS/bmad-module-skill-forge/_bmad/bmb/config.yaml 2>&1 | head -20",
  "description": "Check for BMad config files"
}
```

> TOOL

tool_result
id: toolu_01X8YmV9QdxkthLKRrKBJ93a
```
/home/armel/Projects/OSS/bmad-module-skill-forge/_bmad/bmb/config.yaml
/home/armel/Projects/OSS/bmad-module-skill-forge/_bmad/config.user.yaml
/home/armel/Projects/OSS/bmad-module-skill-forge/_bmad/config.yaml
```

> TOOL

tool_use Read
id: toolu_01QmJ7j9LjYfAztN5VauMYic
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/_bmad/config.yaml"
}
```

> TOOL

tool_result
id: toolu_01QmJ7j9LjYfAztN5VauMYic
```
1	document_output_language: English
2	output_folder: '{project-root}/_bmad-output'
3	bmb:
4	  name: BMad Builder
5	  description: Standard Skill Compliant Factory for BMad Agents, Workflows and Modules
6	  version: 1.0.0
7	  default_selected: false
8	  bmad_builder_output_folder: '{project-root}/skills'
9	  bmad_builder_reports: '{project-root}/skills/reports'
10	
```

> TOOL

tool_use Read
id: toolu_01XCwM2sA7WPAeFZKdLyYYR4
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/_bmad/config.user.yaml"
}
```

> TOOL

tool_result
id: toolu_01XCwM2sA7WPAeFZKdLyYYR4
```
1	user_name: Armel
2	communication_language: English
3	
```

> AGENT

Hi Armel — Workflow & Skill Builder ready.

What would you like to do?

1. **Build new** — design a new workflow or skill from scratch
2. **Convert** — convert an existing skill (path or URL) into a lean, BMad-compliant version with a before/after report
3. **Analyze / Edit / Rebuild** — point me at an existing skill and I'll ask which mode
4. **Quality check** — run analysis on an existing skill for over-specification and structural issues

Reply with a number, or describe what you have in mind (e.g., "build a skill that does X" or paste a path/URL). Add `--headless` to skip interactive discovery.

> DEVELOPER

@CONTRIBUTING.md fix these issues: https://github.com/armelhbobdad/bmad-module-skill-forge/issues. Organize the commits the smartest way (e.g: one commit per issue if applicable). Link each commit to the related issue(s). Review all the changes for any breaking changes, or missing impacts/bugs/regressions and ect... DO NOT HALLUCINATE. Activate party mode and/or advanced elicitation only if it is necessary.

> AGENT

I'll start by listing the open issues to understand scope, then plan commit organization.

> TOOL

tool_use Bash
id: toolu_014eJsGjmpBe7Yo5k8EBiP8G
```json
{
  "command": "gh issue list --repo armelhbobdad/bmad-module-skill-forge --state open --limit 100 --json number,title,labels,body",
  "description": "List open issues from bmad-module-skill-forge"
}
```

> TOOL

tool_use Bash
id: toolu_01WxRtHivmxkWRVNFThwpJsh
```json
{
  "command": "git status && git log --oneline -20",
  "description": "Check repo state and recent commit style"
}
```

> TOOL

tool_result
id: toolu_014eJsGjmpBe7Yo5k8EBiP8G
```
[{"body":"## Workflow\n`skf-update-skill`\n\n## Step File\n`src/skf-update-skill/steps-c/step-02-detect-changes.md`\n\n## Severity\n`gap`\n<!-- gap: a scenario arose that wasn't covered at all -->\n\n## Fingerprint\n`fp-e8c3699`\n<!-- sha1(\"gap|skf-update-skill|src/skf-update-skill/steps-c/step-02-detect-changes.md|major-version-scope-expansion\")[:7] -->\n\n## Finding\nupdate-skill has no documented mechanism for major-version paradigm shifts where the baseline-tracked module set is wholly replaced upstream and the brief's `scope.include` no longer reflects the real public API.\n\n## Expected\nA formal step (e.g. §1c \"Major-Version Scope Reconciliation\") that fires when the audit-supplied drift report contains an \"out-of-scope new public API\" observation OR when ≥50% of provenance-map exports are detected as deleted in step-02 Category A, with documented `category: \"scope-expansion\"` amendment actions for code paths and a [P]/[S]/[U] menu mirroring §1b's doc-promotion flow.\n\n## Actual\n§1b's brief-amendment machinery exists but is scoped to authoritative-doc promotion (`llms.txt`, `CLAUDE.md`, etc.); there is no formal pattern for promoting code paths into the include set mid-run. I had to stretch §1b's `amendments[]` mechanism with an undocumented `category: \"scope-expansion\"` field and invent action values (`promoted` for code globs, `demoted-include`, `demoted-exclude`) — and the same gap struck again mid-extraction in step-03 when a referenced module (`cocoindex.resources.*`) was discovered to be undocumented in the brief.\n\n## Evidence\n- `src/skf-update-skill/steps-c/step-02-detect-changes.md:60` — §1b \"Discovered Authoritative Files Protocol (Mirror)\" purpose statement is exclusively framed around `llms.txt` / `AGENTS.md` / `.cursorrules`; no extension hook for code globs.\n- `src/skf-update-skill/steps-c/step-02-detect-changes.md:69-73` — heuristic basename list is doc-only.\n- `src/skf-update-skill/steps-c/step-03-re-extract.md:227` — \"DO NOT BE LAZY — For EACH remaining file in the change manifest...\" assumes the manifest covers the new public API, but step-02 Category A only finds files referenced by the previous provenance map.\n- `forge-data/oms-cocoindex/0.3.37/drift-report-20260424-212355.md:127` — drift report explicitly noted ~70 new exports in `python/cocoindex/_internal/api.py` as out-of-scope and recommended \"Run `skf-update-skill` to bring the new surface into scope\" — but update-skill has no step that responds to this signal.\n- The cognee `0.5.8 → 1.0.0` and cocoindex `0.3.37 → 1.0.0` runs are existence proofs that this case is real and recurring.\n\n## Impact\nThis run cost two ad-hoc brief-amendment cycles (one before step-03, one mid-step-03 when `cocoindex.resources.*` was discovered to be needed for the Quick Start example) and required user-facing decisions (\"what is the best move?\" was asked twice) that a documented happy path would have made obvious. The output is correct but the workflow's lack of a formal mechanism here means the cost is paid by every future major-version update.\n\n## Suggested Fix\nAdd §1c (or §2.0) \"Major-Version Scope Reconciliation\" to `step-02-detect-changes.md`. Trigger conditions: (a) audit-supplied drift report contains an \"out-of-scope new public API\" observation, OR (b) ≥50% of provenance-map exports are detected as deleted in step-02 Category A. Action: load the drift report's \"Out-of-Scope Observation\" section if present and present a [P]/[S]/[U] menu (mirroring §1b's doc-promotion flow) for each candidate path glob. Formalize the `category: \"scope-expansion\"` amendment field and document the valid action values: `promoted` (add to `scope.include`), `demoted-include` (remove from `scope.include`), `demoted-exclude` (remove from `scope.exclude`). The cocoindex `0.3.37 → 1.0.0` brief amendments at `forge-data/oms-cocoindex/skill-brief.yaml.amendments[]` (post-this-run) are a concrete reference implementation.\n\n<details>\n<summary>Alternatives considered (optional)</summary>\n\nRouting major-version updates entirely through `skf-brief-skill` (instead of in-flight amendments) would preserve workflow boundaries cleanly, but adds round-trips and re-discovery work that is redundant when the drift report has already done the analysis.\n\n</details>\n\n## Environment\n| Field | Value |\n|-------|-------|\n| Date | 2026-04-25 |\n| OS | Linux (Debian 13) |\n| AI Editor | Claude Code |\n| Model | Claude Opus 4.7 (1M context) |\n| Forge Tier | Deep |\n| SKF Version | 1.0.0 |\n","labels":[{"id":"LA_kwDORPo41s8AAAACe3WXBQ","name":"health-check","description":"Health check findings from SKF workflow runs","color":"0e8a16"},{"id":"LA_kwDORPo41s8AAAACe3WZXw","name":"workflow-improvement","description":"Improvements to SKF workflow step instructions","color":"1d76db"},{"id":"LA_kwDORPo41s8AAAACe3Wa6A","name":"gap","description":"Scenario the workflow did not account for","color":"e99695"},{"id":"LA_kwDORPo41s8AAAACgrKRiQ","name":"fp-e8c3699","description":"Health-check fingerprint dedup key","color":"ededed"}],"number":233,"title":"[health-check][gap][fp-e8c3699] skf-update-skill: no mechanism for major-version scope expansion"}]
```

> TOOL

tool_result
id: toolu_01WxRtHivmxkWRVNFThwpJsh
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
50ee7f7 Merge pull request #232 from armelhbobdad/fix/audit-skill-gaps-230-231
8c7aa90 fix(audit-skill): correct brief-gate framing for new entry points
22dcc0c fix(audit-skill): align step-05 rollup row to the 6-column severity table
0a005f0 fix(audit-skill): surface version preservation in update-skill recommendation
070d8b9 fix(audit-skill): add rollup clause for high-volume uniform findings
c1b165b Merge pull request #229 from armelhbobdad/docs/animated-readme-logo
5735f09 docs(readme): add animated hero logo
a967e84 fix(audit-skill): close three workflow gaps (#216, #217, #218) (#227) (#228)
197c3fc fix(release): lock docs/_data/pinned.yaml.skf_version to package.json.version (#226)
7370b54 chore(docs): post-Epic-6 RELEASING.md polish (Story 6.3 deferreds) (#225)
45bed3a chore(release): remove NPM_TOKEN repo secret + reconcile RELEASING.md (Story 6.3) (#224)
d531945 chore(release): remove release:* scripts from package.json (Story 6.2) (#223)
309f558 chore(release): delete legacy publish.yaml and manual-release.yaml workflows (Story 6.1) (#222)
4e7405a Merge pull request #221 from armelhbobdad/feat/v1-install-smoke-review-patches
d0cddab chore(release): apply code-review patches (Story 5.4)
a6ba417 Merge pull request #220 from armelhbobdad/feat/v1-post-publish-verify
cc2d3b2 docs(release): record cross-platform v1.0.0 install verification (Story 5.4)
075dbcb Merge pull request #219 from armelhbobdad/feat/v1-install-smoke-workflow
5b17847 feat(release): add post-publish install smoke workflow (Story 5.4)
55f40d0 Merge pull request #215 from armelhbobdad/feat/v1-final-review-patches
```

> AGENT

Only one open issue: #233. It's a substantive workflow gap — needs careful reading of the actual files referenced. Let me explore.

> TOOL

tool_use Read
id: toolu_013ih1JQ9zHaiR3f1WSgBEhs
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/steps-c/step-02-detect-changes.md"
}
```

> TOOL

tool_result
id: toolu_013ih1JQ9zHaiR3f1WSgBEhs
```
1	---
2	nextStepFile: './step-03-re-extract.md'
3	noChangeReportFile: './step-07-report.md'
4	---
5	
6	# Step 2: Detect Changes
7	
8	## STEP GOAL:
9	
10	Compare current source code state against the provenance map to produce a complete change manifest identifying every changed, added, deleted, moved, and renamed file and export since last extraction.
11	
12	## Rules
13	
14	- Focus only on detecting and classifying changes — do not extract or merge
15	- Use subprocess Pattern 4 (parallel) when available; if unavailable, compare sequentially
16	
17	## MANDATORY SEQUENCE
18	
19	**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.
20	
21	### 0. Check for Test Report Input (Gap-Driven Mode)
22	
23	**If `update_mode == "gap-driven"` (set in step-01 via `--from-test-report`):**
24	
25	Load the test report at `{test_report_path}` and extract findings:
26	
27	1. Read the **Gap Report** section — each gap entry has severity, category, and description
28	2. Read the **Coverage Analysis** section — each per-export row has documented/missing/mismatch status
29	3. Translate findings into change manifest format:
30	
31	| Gap Severity | Gap Type | Change Category |
32	|-------------|----------|-----------------|
33	| Critical | Missing export documentation | NEW_EXPORT (undocumented public API) |
34	| High | Signature mismatch | MODIFIED_EXPORT (signature needs update) |
35	| Medium | Missing type/interface docs | NEW_EXPORT (undocumented type) |
36	| Medium | Stale documentation | MODIFIED_EXPORT (docs reference removed export) |
37	| Low | Missing metadata/examples | metadata update |
38	
39	4. Build the change manifest from translated gaps — no file-level timestamp comparison needed since source hasn't changed. For each manifest entry, propagate these fields from the test report finding so step-03 can resolve the export against live source:
40	
41	   - **`severity`** — the Gap Report severity (`Critical`, `High`, `Medium`, `Low`, `Info`). Step-03 §0 and step-06 §3 gate the null-citation fallback on severity: Critical/High gaps must produce AST provenance, Medium/Low/Info gaps may degrade to `unknown`.
42	   - **`source_citation: {file, line}`** — populated only when the finding's `Source:` field is a `file:line` pair (e.g., a Gap Report row that cites `packages/utils/src/builder-utils.ts:33`). Step-03 §0 uses this field to perform a live spot-check against source rather than flagging the export as `unknown`. Omit when the `Source:` field is a region reference (e.g., `@storybook/addon-docs control primitives`) or missing.
43	   - **`remediation_paths: [path, ...]`** — path-like tokens extracted from the finding's `Remediation:` text: any substring matching a recognized source file extension (`.ts`, `.tsx`, `.js`, `.jsx`, `.mjs`, `.cjs`, `.py`, `.rs`, `.go`, `.java`, `.rb`, `.c`, `.h`, `.cpp`), or a directory/glob fragment under the project's source root. Include every matching path verbatim. Step-03 §0a uses this list as the source set for its Targeted Re-Extraction Branch when `source_citation` is absent and severity is Critical/High. Omit the field when the Remediation text names no paths — the entry then falls through to `unknown` or to §0a's halt, depending on severity.
44	5. Set `gap_count` from the total number of translated entries
45	6. **Skip to section 5** (Display Change Summary) with the gap-derived manifest
46	
47	"**Gap-driven update mode.** Translating {gap_count} test report findings into change manifest — source drift detection skipped."
48	
49	**If normal mode:** Continue with source drift detection below.
50	
51	### 1. Scan Current Source State
52	
53	Read the source directory at `{source_root}` and build a current file inventory:
54	- For each source file: record path, file size, last modified timestamp
55	- Focus on file types relevant to the skill (from provenance map file patterns)
56	- Exclude non-source files (node_modules, build artifacts, etc.)
57	
58	### 1b. Discovered Authoritative Files Protocol (Mirror)
59	
60	**Purpose:** mirror `skf-create-skill` §2a into update-skill. `skf-create-skill` §2a catches authoritative AI documentation files (`llms.txt`, `AGENTS.md`, `.cursorrules`, etc.) during **creation**. But a project may add these files *after* the skill was created — for example, an upstream project adopts an `llms.txt` convention six months into development. Without this mirror, update-skill would either miss the new file entirely (if it doesn't match the provenance map's file patterns) or classify it as a generic ADDED file in §2 Category A with no authoritative-file treatment. The mirror surfaces the discovery with the same P/S/U prompt create-skill uses, honoring any prior amendments.
61	
62	**Skip this section entirely if:**
63	
64	- `update_mode == "gap-driven"` (source hasn't drifted — we're verifying test report findings, not discovering new files), OR
65	- `metadata.json.source_type == "docs-only"` (no source tree to scan)
66	
67	**Procedure (identical heuristics to create-skill §2a):**
68	
69	1. **Walk the source tree.** Match file basenames against the heuristic list case-insensitively:
70	   - `llms.txt`, `llms-full.txt`
71	   - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `COPILOT.md`
72	   - `.cursorrules`, `.windsurfrules`, `.clinerules`
73	
74	2. **Cross-reference with provenance map.** For each match:
75	   - **Already in provenance map** (`entries[].source_file` or `file_entries[].source_file` contains this path): the file is already tracked. §2 will detect any drift in the normal flow. No action in §1b.
76	   - **Not in provenance map:** continue to amendment check.
77	
78	3. **Check brief amendments.** Load `brief.scope.amendments[]` from `{forge_data_folder}/{skill_name}/skill-brief.yaml`. For each candidate not in the provenance map:
79	   - **`action: "promoted"` for this path exists:** the brief says this file should be in scope, but it's missing from the provenance map. This means the file was promoted by a prior run but its `file_entries[]` row is missing (e.g. provenance-map was regenerated from source without re-reading amendments). Add the path to `promoted_docs_new[]` (see step 6 below) with its content hash so §4 merge writes a new `file_entries[]` row. No user prompt — the decision was already made. Display: `"Honoring prior amendment: promoted {path} scheduled for file_entries write."`
80	   - **`action: "skipped"` for this path exists:** user previously declined promotion. Honor the skip silently. No prompt, no action.
81	   - **No amendment for this path:** continue to user prompt.
82	
83	4. **Prompt.** For each unresolved candidate, present the same prompt as create-skill §2a:
84	
85	   ```
86	   **New authoritative file discovered since skill creation**
87	
88	   Path: {relative_path_from_source_root}
89	   Size: {line_count} lines, {bytes} bytes
90	   Matched heuristic: {basename}
91	   Provenance age: {days since skill creation}
92	
93	   First 20 lines:
94	   {inline preview}
95	
96	   This file was not present (or not in scope) when the skill was created. How should update-skill handle it?
97	
98	   [P] Promote — extract in this update run AND amend brief for future runs
99	   [S] Skip    — leave out of scope AND record skip in amendments (no re-prompt)
100	   [U] Update  — halt this run and return to skf-brief-skill to refine scope
101	   ```
102	
103	5. **Headless mode (`{headless_mode}` is true):** auto-select `[S] Skip` for every candidate — record `action: "skipped"`, `reason: "headless: no user to prompt"`, `workflow: "skf-update-skill"`. A non-interactive update run must never silently add files to scope.
104	
105	6. **Apply decision:**
106	
107	   - **[P] Promote:**
108	     1. Append `candidate.path` to `brief.scope.include` as a literal glob.
109	     2. Append a `brief.scope.amendments[]` entry: `action: "promoted"`, `path: candidate.path`, `reason: {user-provided or auto: "discovered post-creation — matched heuristic {basename}"}`, `heuristic: {basename}`, `date: {today ISO}`, `workflow: "skf-update-skill"`.
110	     3. **Write the amended brief back to disk immediately** at `{forge_data_folder}/{skill_name}/skill-brief.yaml`. Preserve all other fields.
111	     4. **Compute SHA-256 content hash** of `candidate.path` and add an entry to the in-context `promoted_docs_new[]` list: `{path, heuristic, size_bytes, line_count, content_hash}`. This list is consumed by §4 merge Priority 7 to write new `file_entries[]` rows — promoted docs do NOT go through §3 code re-extraction, which would produce ghost entries on non-code files.
112	     5. Display: `"Promoted {path} — brief amended, scheduled as new file_entries row for file_type doc."`
113	
114	   - **[S] Skip:**
115	     1. Do NOT modify `scope.include`.
116	     2. Append a `brief.scope.amendments[]` entry: `action: "skipped"`, `path: candidate.path`, `reason: {user-provided or auto: "user declined promotion at update-skill §1b"}`, `heuristic: {basename}`, `date: {today ISO}`, `workflow: "skf-update-skill"`.
117	     3. **Write the amended brief back to disk** so neither update-skill nor create-skill will re-prompt in future runs.
118	     4. Display: `"Skipped {path} — decision recorded in amendments."`
119	
120	   - **[U] Update:**
121	     1. Halt the workflow immediately.
122	     2. Display: `"Halting update-skill. Re-run skf-brief-skill to refine scope for {skill_name}, then re-run skf-update-skill."`
123	     3. Exit with status `halted-for-brief-refinement`. Change manifest is discarded — no partial writes.
124	
125	7. **Summary.** After all candidates are resolved (or none were found):
126	
127	   - `"Authoritative files mirror: {N} candidates, {P} promoted, {S} skipped, {A} pre-decided from amendments, {T} already tracked in provenance."`
128	   - If N = 0: `"Authoritative files mirror: no candidates."`
129	
130	**Record for evidence report:** the update-skill evidence report appends `authoritative_files_mirror: {candidates: N, promoted: P, skipped: S, pre_decided: A, already_tracked: T, decisions: [{path, action, heuristic, reason}]}`.
131	
132	**Interaction with §2 change detection:** promoted docs live in `promoted_docs_new[]`, NOT in the change manifest. But §2 Category A ("files in source but not in provenance map → ADDED") would still find the promoted doc files on disk and classify them as ADDED if nothing prevents it. The coordination mechanism is an explicit pre-filter exclusion set built in §2.0 (below) that every Category A subprocess worker receives as an input before it starts scanning. See §2.0 for the exact contract. The exclusion set is the only mechanism guaranteeing that parallel subprocesses cannot double-count `promoted_docs_new[]` paths — prose-level "skip any path" instructions cannot cross subprocess boundaries.
133	
134	### 2. Compare Against Provenance Map
135	
136	**If normal mode (provenance map available):**
137	
138	#### 2.0 — Build Pre-filter Exclusion Set
139	
140	Before launching parallel subprocesses, build a `change_detection_excludes` set in context that Category A subprocess workers must honor. Parallel subprocesses cannot see each other's in-memory state, so any coordination between §1b's decisions and §2's scan results must be pre-materialized into an explicit input the subprocesses receive.
141	
142	The exclusion set includes:
143	
144	- Every path in `promoted_docs_new[]` (populated by §1b). These files are tracked as `file_entries[]` via step-04 Priority 7, not through Category A code extraction. Without this exclusion, Category A would classify them as ADDED (because they're in source but not yet in the provenance map) and §3 re-extract would send them to AST extraction, producing ghost entries.
145	- Every source path in `file_entries[].source_file` where `file_type == "doc"` in the existing provenance map. These are already-tracked authoritative docs; any drift in them is handled by Category D (script/asset file changes), not Category A.
146	
147	Record the set size: "**Change-detection excludes:** {count} paths ({promoted_docs_new count} new promotions + {existing doc file_entries count} already tracked)."
148	
149	#### 2.1 — Launch Category Subprocesses
150	
151	Launch subprocesses in parallel that compare source state against provenance map across these categories, returning change findings per category. **Every subprocess receives `change_detection_excludes` as an explicit input** and applies it to its file-path iteration loop.
152	
153	**Category A — File-level changes:**
154	- Files in provenance map but missing from source → DELETED
155	- Files in source but not in provenance map AND not in `change_detection_excludes` → ADDED
156	- Files in `change_detection_excludes`: skip entirely (routed to file_entries via §1b → step-04 Priority 7, never through Category A)
157	- Files in both but with different timestamps/sizes → MODIFIED
158	- Files with same content at different paths → MOVED
159	
160	**Category B — Export-level changes (for MODIFIED files only):**
161	- For each modified file, compare export list against provenance map exports
162	- Exports in provenance but not in source → DELETED_EXPORT
163	- Exports in source but not in provenance → NEW_EXPORT
164	- Exports with changed signatures/types → MODIFIED_EXPORT
165	- Exports at different line numbers but same content → MOVED_EXPORT
166	
167	**Category C — Rename detection:**
168	- Cross-reference deleted files/exports with added files/exports
169	- If content similarity > 80%: classify as RENAMED instead of deleted+added. **Similarity mechanism by tier:** Quick: compare file size ratio (within 20%) and export name overlap (>70% of exports match by name). Forge and above: use ast-grep to compare export signatures between the deleted and added files. Forge+/Deep: use CCC semantic similarity when available
170	
171	**Category D — Script/asset file changes:**
172	- Compare `file_entries` from provenance-map.json against current source files
173	- For each file_entry: compute current SHA-256 content hash, compare against stored hash
174	- Files with changed hashes → MODIFIED_FILE
175	- Files in provenance but missing from source → DELETED_FILE
176	- Files in source matching detection patterns (scripts/, bin/, assets/, templates/) but not in provenance → NEW_FILE
177	- Files in `scripts/[MANUAL]/` or `assets/[MANUAL]/` → SKIP (user-authored, preserved)
178	
179	Aggregate all subprocess results into a unified change manifest.
180	
181	**If degraded mode (no provenance map):**
182	- All source files are treated as MODIFIED
183	- All exports will be fully re-extracted in step 03
184	- Skip export-level comparison
185	
186	### 3. Build Change Manifest
187	
188	Compile the change manifest with structured entries:
189	
190	```
191	Change Manifest:
192	  files_changed: [count]
193	  files_added: [count]
194	  files_deleted: [count]
195	  files_moved: [count]
196	
197	  exports_modified: [count]
198	  exports_new: [count]
199	  exports_deleted: [count]
200	  exports_renamed: [count]
201	  exports_moved: [count]
202	
203	  scripts_modified, scripts_added, scripts_deleted: {counts}
204	  assets_modified, assets_added, assets_deleted: {counts}
205	
206	  Per-file detail:
207	    {file_path}:
208	      status: MODIFIED|ADDED|DELETED|MOVED
209	      exports_affected: [{export_name, change_type, old_line, new_line}]
210	```
211	
212	### 4. Check for No-Change Shortcut
213	
214	**If zero changes detected across all categories:**
215	
216	"**No changes detected.** Source code matches provenance map exactly.
217	
218	The skill `{skill_name}` is current — no update needed.
219	
220	**Skipping to report step...**"
221	
222	→ Skip steps 03-06, immediately load {noChangeReportFile} with "no changes" status.
223	
224	### 5. Display Change Summary and Auto-Proceed
225	
226	"**Change Detection Complete:**
227	
228	| Category | Count |
229	|----------|-------|
230	| Files modified | {count} |
231	| Files added | {count} |
232	| Files deleted | {count} |
233	| Files moved/renamed | {count} |
234	| Exports affected | {total_export_changes} |
235	
236	**Proceeding to re-extraction of {affected_file_count if normal mode, or gap_count if gap-driven mode} changes...**"
237	
238	### 6. Present MENU OPTIONS
239	
240	Display: "**Proceeding to re-extraction...**"
241	
242	#### Menu Handling Logic:
243	
244	- After change manifest is built, immediately load, read entire file, then execute {nextStepFile}
245	- **EXCEPTION:** If no changes detected (section 4), load {noChangeReportFile} instead
246	
247	#### EXECUTION RULES:
248	
249	- This is an auto-proceed step with no user choices
250	- Proceed directly to next step after change detection completes
251	
252	## CRITICAL STEP COMPLETION NOTE
253	
254	ONLY WHEN the change manifest is fully built will you load {nextStepFile} to begin re-extraction. If no changes detected, skip to {noChangeReportFile}.
255	
256	
```

> TOOL

tool_use Read
id: toolu_01DLSjPcCjp3G3vN8JnzE2XV
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/steps-c/step-03-re-extract.md",
  "offset": 200,
  "limit": 60
}
```

> TOOL

tool_result
id: toolu_01DLSjPcCjp3G3vN8JnzE2XV
```
200	**Quick tier (text pattern matching):**
201	- Extract function/class/type names via regex patterns
202	- Extract export statements via text matching
203	- Confidence: T1-low (pattern-matched, not AST-verified)
204	
205	**Forge tier (AST structural extraction):**
206	
207	⚠️ **CRITICAL:** Load and follow the **AST Extraction Protocol** from `{extractionPatternsData}`. Use the decision tree based on the number of changed files: prefer MCP `find_code()` for small sets, `find_code_by_rule()` with scoped YAML rules for medium sets, and CLI `--json=stream` with line-by-line streaming for large sets. Never use `ast-grep --json` (without `=stream`) — it loads the entire result set into memory and will fail on large codebases.
208	
209	- Extract: function signatures, type definitions, class members, exported constants
210	- Extract: parameter types, return types, JSDoc/docstring comments
211	- Confidence: T1 (AST-verified structural truth)
212	
213	**Tier degradation handling (Forge/Forge+/Deep):** If ast-grep is unavailable or fails on individual files, follow `{tierDegradationRulesData}` for fallback strategy and user notification requirements. Silent degradation is forbidden — the user must always know when AST extraction was skipped.
214	
215	**Deep tier (AST + QMD semantic enrichment):**
216	- Perform all Forge tier extractions (T1)
217	- Additionally: launch a subprocess that queries qmd_bridge for temporal context on changed exports, returning T2 evidence per export
218	- QMD provides: usage patterns, historical context, related documentation
219	- Confidence: T1 for structural, T2 for semantic enrichment
220	
221	**Tool resolution:** `ast_bridge` → ast-grep MCP tools (`find_code`, `find_code_by_rule`) or `ast-grep` CLI. `qmd_bridge` → QMD MCP tools (`mcp__plugin_qmd-plugin_qmd__search`, `vector_search`) or `qmd` CLI. See `knowledge/tool-resolution.md`.
222	
223	### 2. Extract Changed Files
224	
225	**Skip authoritative doc paths.** Before iterating the change manifest, build a skip set from `promoted_docs_new[]` (populated by step-02 §1b) and any existing `file_entries[]` entries with `file_type: "doc"` from the provenance map. These are documentation files tracked for drift detection only — they must not reach AST extraction, which would produce ghost entries on non-code content. If a change manifest entry matches the skip set, skip it silently and continue; doc-type drift is handled by step-02 Category D and step-04 Priority 6/7.
226	
227	DO NOT BE LAZY — For EACH remaining file in the change manifest with status MODIFIED, ADDED, or RENAMED, launch a subprocess that:
228	
229	1. Loads the source file
230	2. Performs tier-appropriate extraction (Quick/Forge/Forge+/Deep)
231	3. For each export found:
232	   - Record: export name, type (function/class/type/constant), signature
233	   - Record: file path, start line, end line
234	   - Record: parameters with types (if function/method)
235	   - Record: return type (if function/method)
236	   - Record: JSDoc/docstring summary (if present)
237	   - Label: confidence tier (T1/T1-low/T2)
238	4. Returns structured extraction findings to parent
239	
240	**For DELETED files:** No extraction needed — deletions handled in merge step.
241	
242	**For MOVED files:** Re-extract at new location to update file:line references.
243	
244	**Re-export tracing (Forge/Deep only):** After extracting changed files, check if any public exports from the package entry point (`__init__.py`, `index.ts`, `lib.rs`) are unresolved — particularly when a changed file is part of a module re-export chain. Follow the **Re-Export Tracing** protocol in `{extractionPatternsTracingData}` to trace unresolved symbols to their actual definition files.
245	
246	### 2b. CCC Semantic Ranking (Forge+ and Deep with ccc)
247	
248	**IF `tools.ccc` is true in forge-tier.yaml:**
249	
250	Before aggregating extraction results, use CCC to assess semantic significance of changes:
251	
252	1. Run `ccc_bridge.search("{skill_name}", source_root, top_k=15)` — **Tool resolution:** `/ccc` skill search (Claude Code), ccc MCP (Cursor), `ccc search` (CLI) — to get the skill's most semantically central files
253	2. Cross-reference the change manifest files with CCC results
254	3. Files appearing in BOTH the change manifest AND CCC's top results are **semantically significant changes** — flag them for priority in the merge step
255	4. Store `{ccc_significant_changes: [{file, score}]}` in context
256	
257	This helps the merge step (section 4) prioritize which changes are most likely to affect the skill's core content vs. peripheral modifications.
258	
259	CCC failures: skip ranking silently, all changes treated equally.
```

> TOOL

tool_use Bash
id: toolu_014oo3Vq7Dfa9EYEuUzzq3ik
```json
{
  "command": "ls /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/ /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/references/ /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/steps-c/ 2>&1",
  "description": "List update-skill structure"
}
```

> TOOL

tool_result
id: toolu_014oo3Vq7Dfa9EYEuUzzq3ik
```
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/:
references
SKILL.md
steps-c

/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/references/:
manual-section-rules.md
merge-conflict-rules.md
remote-source-resolution.md

/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/steps-c/:
step-01-init.md
step-02-detect-changes.md
step-03-re-extract.md
step-04-merge.md
step-05-validate.md
step-06-write.md
step-07-report.md
step-08-health-check.md
```

> TOOL

tool_use Bash
id: toolu_01XrTUdeDdAyeSTUUxEZtVv9
```json
{
  "command": "ls /home/armel/Projects/OSS/bmad-module-skill-forge/forge-data/ 2>&1 | head -30",
  "description": "Check forge-data folder"
}
```

> TOOL

tool_result
id: toolu_01XrTUdeDdAyeSTUUxEZtVv9
```
ls: cannot access '/home/armel/Projects/OSS/bmad-module-skill-forge/forge-data/': No such file or directory
```

> AGENT

Let me track this work and gather more context on the related references.

> TOOL

tool_use ToolSearch
id: toolu_019uEwEfaceB5eUfXRPxri2h
```json
{
  "query": "select:TaskCreate",
  "max_results": 1
}
```

> TOOL

tool_result
id: toolu_019uEwEfaceB5eUfXRPxri2h
```
{
  "type": "tool_reference",
  "tool_name": "TaskCreate"
}
```

> TOOL

tool_use Bash
id: toolu_01H5QhQYrHdzCPnC1JKe5qDt
```json
{
  "command": "grep -rn \"out-of-scope\" /home/armel/Projects/OSS/bmad-module-skill-forge/src/ 2>&1 | head -20",
  "description": "Find out-of-scope references in src"
}
```

> TOOL

tool_result
id: toolu_01H5QhQYrHdzCPnC1JKe5qDt
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01LEMV4XD5JMyk1QfeyPKkTA
```json
{
  "command": "grep -rn \"scope-expansion\\|scope_expansion\\|major.version\" /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/ /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/ 2>&1 | head -30",
  "description": "Search for scope-expansion / major-version mentions"
}
```

> TOOL

tool_result
id: toolu_01LEMV4XD5JMyk1QfeyPKkTA
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01QStn8iuiUzmdtv41QVZVHG
```json
{
  "command": "grep -rn \"Out-of-Scope\\|Out of Scope\\|out_of_scope\" /home/armel/Projects/OSS/bmad-module-skill-forge/src/ 2>&1 | head -20",
  "description": "Find out-of-scope references"
}
```

> TOOL

tool_result
id: toolu_01QStn8iuiUzmdtv41QVZVHG
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01YSJfUjfsexuqEjFmzJbCQ3
```json
{
  "command": "ls /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/ 2>&1",
  "description": "List audit-skill steps"
}
```

> TOOL

tool_result
id: toolu_01YSJfUjfsexuqEjFmzJbCQ3
```
step-01-init.md
step-02-re-index.md
step-03-structural-diff.md
step-04-semantic-diff.md
step-05-severity-classify.md
step-06-report.md
step-07-health-check.md
```

> TOOL

tool_use Bash
id: toolu_012auaXVMH6Dy9Vg5CgGKTzL
```json
{
  "command": "grep -n \"drift\" /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/*.md 2>&1 | head -30",
  "description": "Search drift in audit steps"
}
```

> TOOL

tool_result
id: toolu_012auaXVMH6Dy9Vg5CgGKTzL
```
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-02-re-index.md:3:outputFile: '{forge_version}/drift-report-{timestamp}.md'
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-02-re-index.md:10:Re-scan the source code using the current forge tier tools to build a fresh extraction snapshot. This snapshot will be compared against the original provenance map in Step 03 to detect structural drift.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-02-re-index.md:50:Audit-skill detects drift on files that were in scope during create-skill. The authoritative record of "what was in scope" is the provenance map loaded in step-01. Scan only those files — **audit-skill does NOT discover new files**. New-file detection is the responsibility of `skf-update-skill`, which maintains its own change manifest. To audit a project that has grown new files since creation, run update-skill first, then audit-skill.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-02-re-index.md:52:**Why bounded:** without this constraint, files that were deliberately excluded by the original brief's scope patterns (test fixtures, vendored code, generated artifacts, demo code, unrelated modules) get scanned on every audit and their exports are flagged by step-03 structural diff as "added" — false-positive drift that obscures real structural changes.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-02-re-index.md:151:   - This reduces false-positive structural drift findings where exports were relocated, not removed
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-06-report.md:2:outputFile: '{forge_version}/drift-report-{timestamp}.md'
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-06-report.md:10:Finalize the drift report by completing the Audit Summary with calculated metrics, generating actionable remediation suggestions for each drift finding, and adding provenance metadata. Present the final report to the user with a next-workflow recommendation.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-06-report.md:15:- Do not discover new drift items or reclassify severity
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-06-report.md:28:- Set overall drift score
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-06-report.md:33:For EACH classified drift finding, generate a specific remediation suggestion:
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-06-report.md:86:**Optional:** Minor drift detected. Manual updates sufficient, or run `[US] Update Skill` for automated remediation.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-06-report.md:124:- Set `drift_score` to final calculated score
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-06-report.md:152:**All Clear:** No drift detected. Skill accurately reflects current source code.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-06-report.md:158:1. **[US] Update Skill** — Automatically apply remediations from this drift report
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-06-report.md:171:Write the result contract per `shared/references/output-contract-schema.md`: the per-run record at `{forge_version}/audit-skill-result-{YYYYMMDD-HHmmss}.json` (UTC timestamp, resolution to seconds) and a copy at `{forge_version}/audit-skill-result-latest.json` (stable path for pipeline consumers — copy, not symlink). Include the drift report path in `outputs`; include `drift_count` and `severity` (CLEAN/MINOR/SIGNIFICANT/CRITICAL) in `summary`.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-04-semantic-diff.md:3:outputFile: '{forge_version}/drift-report-{timestamp}.md'
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-04-semantic-diff.md:135:Display: "**Semantic diff complete. {total} semantic drift items found. Proceeding to severity classification...**"
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-05-severity-classify.md:3:outputFile: '{forge_version}/drift-report-{timestamp}.md'
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-05-severity-classify.md:11:Grade every drift finding from Steps 03 and 04 by severity level (CRITICAL/HIGH/MEDIUM/LOW) using the classification rules. Calculate the overall drift score and produce a categorized findings table with confidence tier labels.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-05-severity-classify.md:15:- Only classify severity of existing findings — do not discover new drift items or suggest remediation
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-05-severity-classify.md:40:Gather all drift items from the report:
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-05-severity-classify.md:142:- Set `drift_score` to calculated overall score
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-05-severity-classify.md:146:Display: "**Severity classification complete. Overall drift score: {score}. Proceeding to report generation...**"
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-01-init.md:3:outputFile: '{forge_version}/drift-report-{timestamp}.md'
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-01-init.md:4:templateFile: 'assets/drift-report-template.md'
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-01-init.md:11:Load the existing skill artifacts, provenance map, and forge tier configuration to establish the baseline for drift detection. Create the drift report document and present a baseline summary for user confirmation before proceeding with analysis.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-01-init.md:97:- Flag any mismatches as **constituent drift** with severity HIGH
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-01-init.md:118:Upstream drift detection is the primary use case of this workflow. If the local clone is still pinned to the baseline commit while upstream has shipped newer tags, auditing against the unchanged tree will misleadingly report CLEAN even after a major release.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-01-init.md:146:4. **User gate — Upstream drift detected:**
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-01-init.md:155:   Auditing against the baseline clone will report little-to-no structural drift even if the upstream API has changed. Options:
```

> TOOL

tool_use Bash
id: toolu_01CyakRFaKKFzvHfPdr5qg7q
```json
{
  "command": "grep -rn \"Out-of-Scope\\|out-of-scope\\|Out of scope\" /home/armel/Projects/OSS/bmad-module-skill-forge/src/ 2>&1 | head -20",
  "description": "Search out-of-scope all variants"
}
```

> TOOL

tool_result
id: toolu_01CyakRFaKKFzvHfPdr5qg7q
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01LtdNbSHqRZCstP5pyYfpdr
```json
{
  "command": "grep -rn \"amendments\" /home/armel/Projects/OSS/bmad-module-skill-forge/src/ 2>&1 | head -30",
  "description": "Find amendments references"
}
```

> TOOL

tool_result
id: toolu_01LtdNbSHqRZCstP5pyYfpdr
```
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:68:3. **Check existing amendments.** Before prompting, consult `brief.scope.amendments[]` (see `src/skf-brief-skill/assets/skill-brief-schema.md` for the schema). If any amendment entry has `path == candidate.path`, the decision is already recorded:
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:69:   - `action: "promoted"` → the file should already be in `scope.include` (amendments are write-through). No prompt. **Still populate `promoted_docs[]`** for this path — compute its content hash and add a `{path, heuristic, size_bytes, line_count, content_hash}` entry so step-05 §6 writes the `file_entries[]` row. This is the deterministic replay path for re-runs.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:90:   [S] Skip    — honor the brief exclusion AND record skip in amendments (no re-prompt)
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:101:     3. Append to `brief.scope.amendments[]` a new entry with `action: "promoted"`, `path: candidate.path`, `reason: {user-provided one-sentence reason or auto-generated "authoritative AI docs — matched heuristic {basename}"}`, `heuristic: {basename}`, `date: {today ISO}`, `workflow: "skf-create-skill"`.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:121:     2. Append to `brief.scope.amendments[]` a new entry with `action: "skipped"`, `path: candidate.path`, `reason: {user-provided reason or auto-generated "user declined promotion at create-skill §2a"}`, `heuristic: {basename}`, `date: {today ISO}`, `workflow: "skf-create-skill"`.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:123:     4. Display: "**Skipped `{path}`** — decision recorded in amendments."
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:132:   - `"Authoritative files scan: {N} candidates, {P} promoted, {S} skipped, {A} pre-decided from amendments."`
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:145:**Re-running `skf-create-skill`** reads the amended brief. Files with `action: "promoted"` amendments already appear in `scope.include`, but §2a still runs — it detects the file is in scope AND has an existing amendment, and takes the "pre-decided" silent path. The `promoted_docs[]` list is rebuilt on each run by scanning amendments with `action: "promoted"` (this is the deterministic replay path).
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:152:The brief is the single source of truth for authored scope intent. The provenance map is the single source of truth for extracted state. `scope.amendments[]` is the bridge that records when those two intentionally diverged. `promoted_docs[]` is the in-memory handoff from §2a to step-05 §6; it is not persisted — the persisted form is the `file_entries[]` list in provenance-map.json.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/assets/skill-brief-schema.md:71:  # amendments:
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/assets/skill-brief-schema.md:90:`scope.amendments[]` is an additive, optional audit log of scope decisions made by workflows after the brief was first authored. Its primary writer is `skf-create-skill` §2a (Discovered Authoritative Files Protocol), which appends entries when extraction discovers authoritative AI documentation files (`llms.txt`, `AGENTS.md`, etc.) that the original scope patterns excluded.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/assets/skill-brief-schema.md:103:**Promotion write-through:** When `action: "promoted"`, the workflow also appends the literal path to `scope.include`. This is a belt-and-suspenders design: future `skf-create-skill` runs read `scope.include` during §2 and include the file in the filtered list automatically, so §2a finds no candidate and does not re-prompt. The `amendments[]` entry is the human-readable audit trail of *why* the path was added.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/assets/skill-brief-schema.md:105:**Skip recording:** When `action: "skipped"`, the workflow does NOT modify `scope.include` or `scope.exclude`. The amendment entry alone is enough to prevent re-prompting, because §2a checks `amendments[]` before prompting.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/assets/skill-brief-schema.md:107:**Backward compatibility:** `scope.amendments` is optional. Briefs without this field validate unchanged. Treat missing as an empty list.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/assets/skill-brief-schema.md:109:**Who reads `amendments[]`:**
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/assets/skill-brief-schema.md:116:**Who writes `amendments[]`:**
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/steps-c/step-02-detect-changes.md:60:**Purpose:** mirror `skf-create-skill` §2a into update-skill. `skf-create-skill` §2a catches authoritative AI documentation files (`llms.txt`, `AGENTS.md`, `.cursorrules`, etc.) during **creation**. But a project may add these files *after* the skill was created — for example, an upstream project adopts an `llms.txt` convention six months into development. Without this mirror, update-skill would either miss the new file entirely (if it doesn't match the provenance map's file patterns) or classify it as a generic ADDED file in §2 Category A with no authoritative-file treatment. The mirror surfaces the discovery with the same P/S/U prompt create-skill uses, honoring any prior amendments.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/steps-c/step-02-detect-changes.md:78:3. **Check brief amendments.** Load `brief.scope.amendments[]` from `{forge_data_folder}/{skill_name}/skill-brief.yaml`. For each candidate not in the provenance map:
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/steps-c/step-02-detect-changes.md:79:   - **`action: "promoted"` for this path exists:** the brief says this file should be in scope, but it's missing from the provenance map. This means the file was promoted by a prior run but its `file_entries[]` row is missing (e.g. provenance-map was regenerated from source without re-reading amendments). Add the path to `promoted_docs_new[]` (see step 6 below) with its content hash so §4 merge writes a new `file_entries[]` row. No user prompt — the decision was already made. Display: `"Honoring prior amendment: promoted {path} scheduled for file_entries write."`
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/steps-c/step-02-detect-changes.md:99:   [S] Skip    — leave out of scope AND record skip in amendments (no re-prompt)
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/steps-c/step-02-detect-changes.md:109:     2. Append a `brief.scope.amendments[]` entry: `action: "promoted"`, `path: candidate.path`, `reason: {user-provided or auto: "discovered post-creation — matched heuristic {basename}"}`, `heuristic: {basename}`, `date: {today ISO}`, `workflow: "skf-update-skill"`.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/steps-c/step-02-detect-changes.md:116:     2. Append a `brief.scope.amendments[]` entry: `action: "skipped"`, `path: candidate.path`, `reason: {user-provided or auto: "user declined promotion at update-skill §1b"}`, `heuristic: {basename}`, `date: {today ISO}`, `workflow: "skf-update-skill"`.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/steps-c/step-02-detect-changes.md:118:     4. Display: `"Skipped {path} — decision recorded in amendments."`
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/steps-c/step-02-detect-changes.md:127:   - `"Authoritative files mirror: {N} candidates, {P} promoted, {S} skipped, {A} pre-decided from amendments, {T} already tracked in provenance."`
```

> TOOL

tool_use Read
id: toolu_01SApSG4a7cCdYUAyrLRNiG6
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/assets/skill-brief-schema.md"
}
```

> TOOL

tool_result
id: toolu_01SApSG4a7cCdYUAyrLRNiG6
```
1	# Skill Brief Schema
2	
3	## Required Fields
4	
5	| Field       | Type   | Constraint                                       | Description                                                                 |
6	|-------------|--------|--------------------------------------------------|-----------------------------------------------------------------------------|
7	| name        | string | kebab-case `[a-z0-9-]+`                          | Unique skill identifier                                                     |
8	| version     | string | Semantic version (`X.Y.Z` or `X.Y.Z-prerelease`) | Auto-detect from source (see Version Detection below), fall back to `1.0.0`. **Side effect on remote sources:** `skf-create-skill` treats `version` as an **implicit** `target_version` hint when `target_version` itself is absent — it will try to resolve `{version}` or `v{version}` to a git tag before cloning and fall back to HEAD with a warning if no tag matches. See `skf-create-skill/references/source-resolution-protocols.md` → "Implicit Tag Resolution". |
9	| source_repo | string | GitHub URL or local path                         | Repository or project root (optional when `source_type: "docs-only"`)       |
10	| language    | string | Recognized language                              | Primary programming language                                                |
11	| scope       | object | See Scope Object below                           | Boundary definition                                                         |
12	| description | string | 1-3 sentences                                    | What the skill covers                                                       |
13	| forge_tier  | string | `Quick` / `Forge` / `Forge+` / `Deep`            | Inherited from forge-tier.yaml (Title Case)                                 |
14	| created     | string | ISO date `YYYY-MM-DD`                            | Generation date                                                             |
15	| created_by  | string | user_name from config                            | Who generated the brief                                                     |
16	
17	## Optional Fields
18	
19	| Field              | Type   | Constraint                                       | Description                                                                                                                                                                                                                    |
20	|--------------------|--------|--------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
21	| source_type        | string | `source` or `docs-only`                          | Default `source`. When `docs-only`: `source_repo` optional, `doc_urls` required                                                                                                                                                |
22	| doc_urls           | array  | `{url, label}` objects                           | Documentation URLs for T3 content. Required when `source_type: "docs-only"`                                                                                                                                                    |
23	| `scripts_intent`   | string | `detect` / `none` / free-text                    | Describes whether scripts should be extracted. Values: `detect` (auto-detect from source — default when absent), `none` (skip scripts), or a free-text description of expected scripts (e.g., "CLI validation tools in bin/"). |
24	| `assets_intent`    | string | `detect` / `none` / free-text                    | Describes whether assets should be extracted. Values: `detect` (auto-detect from source — default when absent), `none` (skip assets), or a free-text description of expected assets (e.g., "JSON schemas in schemas/").        |
25	| `target_version`   | string | Semantic version (`X.Y.Z` or `X.Y.Z-prerelease`) | User-specified target version. When present, overrides auto-detection and becomes the skill's version. Recommended for docs-only skills where auto-detection is unavailable.                                                   |
26	| `source_authority` | string | `official` / `community` / `internal`            | Default `community`. Set to `official` only when the skill creator is the library maintainer. Forced to `community` when `source_type: "docs-only"`.                                                                           |
27	| `source_ref`       | string | Git ref (tag/branch/HEAD)                        | Resolved git ref used for source access. Set automatically during tag resolution — do not set manually.                                                                                                                        |
28	| `scope.tier_a_include` | array | Glob patterns                                 | Optional. Narrower tier-A include list for stratified-scope monorepo skills. When present, `skf-test-skill` re-derives the coverage denominator from this list instead of the coarse `scope.include`, so the denominator reflects the authoring surface rather than incidentally-matched internal infrastructure. See `skf-test-skill/references/source-access-protocol.md` stratified-scope resolution. |
29	
30	When `source_type: "docs-only"`:
31	- `source_repo` becomes optional (set to doc site URL for reference)
32	- `doc_urls` must have at least one entry
33	- `source_authority` is forced to `community` (T3 external documentation cannot be `official`)
34	- All extracted content gets `[EXT:{url}]` citations
35	
36	## Version Detection
37	
38	During brief creation, attempt to auto-detect the source version before defaulting to `"1.0.0"`. Check the first matching file in the source:
39	
40	- **Python:** `pyproject.toml` `[project] version` (static) → if `dynamic = ["version"]`, check `__init__.py` for `__version__` → `_version.py` if exists → `setup.py` `version=` → `git describe --tags --abbrev=0`
41	- **JavaScript/TypeScript:** root `package.json` (`"version"`) → if root has `"private": true` with a `"workspaces"` array or lacks a `"version"` field, fall back to a primary workspace package's `package.json` (e.g., `code/core/package.json`, or the first matching `packages/*/package.json`). For GitHub sources, prefer `gh api repos/{owner}/{repo}/releases/latest` → `tag_name` when a non-pre-release tag exists, over a default-branch pre-release. Treat a version containing `-alpha`, `-beta`, `-rc`, `-next`, or `-canary` as a pre-release.
42	- **Rust:** `Cargo.toml` `[package] version` (static) → if `version = { workspace = true }`, resolve from workspace root `Cargo.toml` → `git describe --tags --abbrev=0`
43	- **Go:** version tag from `go.mod` or `git describe --tags --abbrev=0`
44	
45	If the source is a remote GitHub repo, use `gh api repos/{owner}/{repo}/contents/{file}` to read the version file. If the source is local, read the file directly.
46	
47	If detection succeeds, use the detected version. If it fails or returns a non-semver value, fall back to `"1.0.0"`.
48	
49	The create-skill workflow (step-03-extract) also performs version reconciliation at extraction time — if the source version has changed since the brief was created, the extraction step warns and uses the source version.
50	
51	**Target version override:** When `target_version` is present in the brief, it takes precedence over auto-detection. Auto-detection still runs for informational purposes (displayed as "Detected version" alongside the user-specified "Target version"), but the `target_version` value is used as the brief's `version` field. This is particularly useful for docs-only skills (where no package manifest exists) and when the user wants to compile a skill for a specific older version.
52	
53	**Pre-release handling:** If the detected version contains a pre-release tag (e.g., `1.0.0-beta.0`, `2.0.0-rc.1`), preserve it as-is. Pre-release tags are valid semver and must not be stripped. When comparing versions during reconciliation, use semver-aware comparison that respects pre-release ordering.
54	
55	## Scope Object Structure
56	
57	```yaml
58	scope:
59	  type: full-library | specific-modules | public-api | component-library | reference-app | docs-only
60	  include:
61	    - "src/**/*.ts"           # Glob patterns for included files/directories
62	  exclude:
63	    - "**/*.test.*"           # Glob patterns for excluded files
64	    - "**/node_modules/**"
65	  # Optional: narrower tier-A include list for stratified-scope monorepos
66	  # tier_a_include:
67	  #   - "code/core/src/manager-api/**"
68	  #   - "code/core/src/preview-api/**"
69	  notes: "Optional notes about scope decisions"
70	  # Optional: amendment log for scope decisions made during create-skill §2a
71	  # amendments:
72	  #   - path: "apps/docs/public/llms.txt"
73	  #     action: "promoted"          # "promoted" | "skipped"
74	  #     reason: "authoritative AI docs — only source for canonical install command"
75	  #     heuristic: "llms.txt"
76	  #     date: "2026-04-11"
77	  #     workflow: "skf-create-skill"
78	  # Additional fields when scope.type is "component-library":
79	  # registry_path: "path/to/registry.ts"  # Optional — auto-detected if omitted
80	  # ui_variants:                           # Optional — design system variants
81	  #   - name: "shadcnui"
82	  #     package: "packages/components/react-shadcn"
83	  # demo_patterns:                         # Optional — auto-detected if omitted
84	  #   - "**/demo/**"
85	  #   - "**/*.stories.*"
86	```
87	
88	### Scope Amendments (Optional)
89	
90	`scope.amendments[]` is an additive, optional audit log of scope decisions made by workflows after the brief was first authored. Its primary writer is `skf-create-skill` §2a (Discovered Authoritative Files Protocol), which appends entries when extraction discovers authoritative AI documentation files (`llms.txt`, `AGENTS.md`, etc.) that the original scope patterns excluded.
91	
92	**Entry fields:**
93	
94	| Field | Type | Required | Description |
95	|---|---|---|---|
96	| `path` | string | yes | Relative path from source root to the file being amended. Matches the literal path added to `scope.include` (for `promoted` actions). |
97	| `action` | string | yes | One of: `promoted` (file added to scope with a literal `scope.include` entry), `skipped` (user declined promotion; file remains out of scope, decision recorded to prevent re-prompting). |
98	| `reason` | string | yes | Human-readable sentence explaining the decision. Either user-provided at prompt time or auto-generated ("authoritative AI docs — matched heuristic {basename}"). |
99	| `heuristic` | string | yes | The basename heuristic that matched (`llms.txt`, `AGENTS.md`, etc.) so future audits can verify the file still matches its original classification. |
100	| `date` | string | yes | ISO date (`YYYY-MM-DD`) when the amendment was recorded. |
101	| `workflow` | string | yes | Workflow name that wrote the amendment (`skf-create-skill`, `skf-update-skill`). Identifies which workflow's §2a-equivalent made the decision. |
102	
103	**Promotion write-through:** When `action: "promoted"`, the workflow also appends the literal path to `scope.include`. This is a belt-and-suspenders design: future `skf-create-skill` runs read `scope.include` during §2 and include the file in the filtered list automatically, so §2a finds no candidate and does not re-prompt. The `amendments[]` entry is the human-readable audit trail of *why* the path was added.
104	
105	**Skip recording:** When `action: "skipped"`, the workflow does NOT modify `scope.include` or `scope.exclude`. The amendment entry alone is enough to prevent re-prompting, because §2a checks `amendments[]` before prompting.
106	
107	**Backward compatibility:** `scope.amendments` is optional. Briefs without this field validate unchanged. Treat missing as an empty list.
108	
109	**Who reads `amendments[]`:**
110	
111	- `skf-create-skill` §2a consults it to avoid re-prompting on decided files.
112	- `skf-update-skill` §1b (mirror of §2a) consults it for the same reason.
113	- `skf-audit-skill` may optionally report on stale promotions (promoted files that no longer exist in source) as a future enhancement — not currently implemented.
114	- Humans reading the brief see the audit trail of non-obvious scope decisions.
115	
116	**Who writes `amendments[]`:**
117	
118	- `skf-create-skill` §2a (Discovered Authoritative Files Protocol)
119	- `skf-update-skill` §1b (mirror of §2a applied during change detection)
120	- Manual edits by the brief author are permitted but should include all required fields above.
121	
122	## YAML Template
123	
124	```yaml
125	---
126	name: "{skill-name}"
127	version: "{detected-version or 1.0.0}"  # Auto-detect from source, fall back to 1.0.0
128	source_type: "source"                    # "source" (default) or "docs-only"
129	source_repo: "{github-url-or-local-path}"
130	language: "{detected-language}"
131	description: "{brief-description}"
132	forge_tier: "{Quick|Forge|Forge+|Deep}"
133	created: "{date}"
134	created_by: "{user_name}"
135	scope:
136	  type: "{full-library|specific-modules|public-api|component-library|reference-app|docs-only}"
137	  include:
138	    - "{pattern}"
139	  exclude:
140	    - "{pattern}"
141	  notes: "{optional-scope-notes}"
142	# target_version: "X.Y.Z"       # Optional: overrides auto-detection when specified
143	# source_ref: "v0.5.0"          # Auto-resolved — do not set manually
144	# Optional: documentation URLs for T3 content (required when source_type: "docs-only")
145	# doc_urls:
146	#   - url: "https://docs.example.com/api"
147	#     label: "API Reference"
148	# scripts_intent: detect         # Optional: detect | none | description
149	# assets_intent: detect          # Optional: detect | none | description
150	# source_authority: community    # Optional: official | community | internal
151	---
152	```
153	
154	## Human-Readable Presentation Format
155	
156	When presenting the brief for confirmation (brief-skill step 04 only — not applicable to analyze-source batch generation), display as:
157	
158	```
159	Skill Brief: {name}
160	====================
161	
162	Target:      {source_repo}
163	Language:    {language}
164	Forge Tier:  {forge_tier}
165	Description: {description}
166	
167	Scope: {scope.type}
168	  Include: {scope.include patterns, one per line}
169	  Exclude: {scope.exclude patterns, one per line}
170	  Notes:   {scope.notes}
171	
172	{If source_type is "docs-only":}
173	Source Type: docs-only
174	Doc URLs:
175	  {doc_urls, one per line with labels}
176	
177	{If source_type is "source" AND supplemental doc_urls collected:}
178	Supplemental Docs:
179	  {doc_urls, one per line with labels}
180	
181	{If scripts_intent or assets_intent was explicitly set (not default "detect"):}
182	Scripts:    {scripts_intent}
183	Assets:     {assets_intent}
184	
185	Source Authority: {source_authority}
186	
187	{If target_version is set:}
188	Target Version:   {target_version} (user-specified)
189	Detected Version: {detected_version or "N/A"}
190	{Else:}
191	Version:    {version}
192	{End if}
193	Created:    {created}
194	Created by: {created_by}
195	```
196	
197	## Validation Rules
198	
199	1. `name` must be unique within {forge_data_folder}
200	2. `source_repo` must be accessible (gh api for GitHub, path exists for local)
201	3. `language` must be a recognized programming language
202	4. `scope.type` must be one of the six defined types
203	5. `scope.include` must have at least one pattern (exception: `docs-only` scope, where include patterns are optional since no source code is available)
204	6. `forge_tier` must be one of: Quick, Forge, Forge+, Deep (Title Case, must match the tier from forge-tier.yaml, or default to Quick)
205	7. When `source_type: "docs-only"`: `doc_urls` must have >= 1 entry, `source_repo` becomes optional
206	8. Each `doc_urls` entry must have a valid `url` field
207	
```

> TOOL

tool_use Bash
id: toolu_014WpYzvZBXk39zAVXrqNQqU
```json
{
  "command": "ls /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/assets/ 2>&1; cat /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/assets/drift-report-template.md 2>&1 | head -150",
  "description": "Show drift report template"
}
```

> TOOL

tool_result
id: toolu_014WpYzvZBXk39zAVXrqNQqU
```
drift-report-template.md
---
workflowType: 'audit-skill'
stepsCompleted: []
lastStep: ''
date: ''
user_name: ''
skill_name: ''
skill_path: ''
source_path: ''
forge_tier: ''
drift_score: ''
nextWorkflow: ''
previousWorkflow: 'create-skill'
---

# Drift Report: {skill_name}

## Audit Summary

**Skill:** {skill_name}
**Source:** {source_path}
**Tier:** {forge_tier}
**Date:** {date}
**Overall Drift Score:** {drift_score}

| Category  | Count |
|-----------|-------|
| CRITICAL  |       |
| HIGH      |       |
| MEDIUM    |       |
| LOW       |       |
| **Total** |       |

---

## Structural Drift

<!-- Appended by step-03-structural-diff -->

---

## Semantic Drift

<!-- Appended by step-04-semantic-diff (Deep tier only) -->

---

## Severity Classification

<!-- Appended by step-05-severity-classify -->

---

## Remediation Suggestions

<!-- Appended by step-06-report -->

---

## Provenance

<!-- Appended by step-06-report -->
```

> TOOL

tool_use Read
id: toolu_01KwPLimVV2umxanMqDeNXAk
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-audit-skill/steps-c/step-06-report.md"
}
```

> TOOL

tool_result
id: toolu_01KwPLimVV2umxanMqDeNXAk
```
1	---
2	outputFile: '{forge_version}/drift-report-{timestamp}.md'
3	nextStepFile: './step-07-health-check.md'
4	---
5	
6	# Step 6: Generate Report
7	
8	## STEP GOAL:
9	
10	Finalize the drift report by completing the Audit Summary with calculated metrics, generating actionable remediation suggestions for each drift finding, and adding provenance metadata. Present the final report to the user with a next-workflow recommendation.
11	
12	## Rules
13	
14	- Focus on completing the report — summary, remediation, provenance
15	- Do not discover new drift items or reclassify severity
16	- Remediation suggestions must be practical: what to change, where, and why
17	- Chains to the local health-check step via `{nextStepFile}` after completion — the user-facing summary is NOT the terminal step
18	
19	## MANDATORY SEQUENCE
20	
21	**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.
22	
23	### 1. Complete Audit Summary
24	
25	Update the ## Audit Summary section at the top of {outputFile} with final calculated values:
26	
27	- Fill in severity count table from Step 05 classification summary
28	- Set overall drift score
29	- Add total findings count
30	
31	### 2. Generate Remediation Suggestions
32	
33	For EACH classified drift finding, generate a specific remediation suggestion:
34	
35	**CRITICAL findings remediation:**
36	- Removed export → "Remove reference to `{export_name}` from SKILL.md section {section}. Export no longer exists at `{file}:{line}`."
37	- Changed signature → "Update `{export_name}` signature in SKILL.md from `{old_signature}` to `{new_signature}`. See `{file}:{line}`."
38	- Renamed export → "Replace `{old_name}` with `{new_name}` throughout SKILL.md. Renamed at `{file}:{line}`."
39	
40	**HIGH findings remediation:**
41	- New public API (>3) → "Add documentation for {count} new exports to SKILL.md: {export_list}. Consider running update-skill workflow."
42	- Deprecated API → "Mark `{export_name}` as deprecated in SKILL.md. Current replacement: `{replacement}` at `{file}:{line}`."
43	
44	**MEDIUM findings remediation:**
45	- Moved function → "Update file reference for `{export_name}` from `{old_file}` to `{new_file}:{line}`."
46	- New exports (1-3) → "Consider adding `{export_names}` to SKILL.md for completeness."
47	- Changed convention → "Review convention documentation in SKILL.md for currency."
48	
49	**LOW findings remediation:**
50	- Style changes → "Optional: Update style references in SKILL.md to reflect current conventions."
51	
52	Append to {outputFile}:
53	
54	```markdown
55	## Remediation Suggestions
56	
57	### Priority Actions (CRITICAL + HIGH)
58	
59	| # | Severity | Finding | Remediation | Effort |
60	|---|----------|---------|-------------|--------|
61	| 1 | {severity} | {finding} | {specific action} | {low/medium/high} |
62	
63	### Recommended Updates (MEDIUM)
64	
65	| # | Finding | Remediation | Effort |
66	|---|---------|-------------|--------|
67	| 1 | {finding} | {specific action} | {low/medium} |
68	
69	### Optional Improvements (LOW)
70	
71	| # | Finding | Remediation |
72	|---|---------|-------------|
73	| 1 | {finding} | {specific action} |
74	
75	### Workflow Recommendation
76	
77	{IF any CRITICAL or HIGH findings:}
78	**Recommended:** Run `[US] Update Skill` workflow to apply priority remediations automatically.
79	
80	{IF `audit_ref != baseline_ref` (source version bump detected in step-01 §5b):}
81	**Version preservation (non-destructive).** `update-skill` preserves the prior version at `{skill_group}/{baseline_version}/` unchanged and writes the new skill to `{skill_group}/{audit_version}/` (see `skf-update-skill/steps-c/step-04-merge.md` §6b, which creates the new version directory and leaves the previous one on disk). The `active` symlink at `{skill_group}/active` repoints to the new version (see `skf-update-skill/steps-c/step-06-write.md` §5b). On the next export, the prior version's export-manifest entry transitions to `status: archived` — files retained for rollback (see `skf-export-skill/steps-c/step-04-update-context.md`). Do **not** recommend `skf-drop-skill` + `skf-create-skill` for a version bump — that destroys the prior version's artifacts.
82	
83	**Surface new entry points for the brief gate.** If the audit observed new top-level modules, renamed package trees, or new public entry points (new `__init__.py`, `index.ts`, `lib.rs`, or equivalent) that were not in the brief's original scope, call them out here. `update-skill` step-02 §1b detects new candidate files via heuristic and prompts `[P]romote` / `[S]kip` / `[U]pdate-brief`; surfacing them in advance makes that gate faster to resolve, or lets the user refine scope via `skf-brief-skill` before running update-skill.
84	
85	{IF only MEDIUM or LOW findings:}
86	**Optional:** Minor drift detected. Manual updates sufficient, or run `[US] Update Skill` for automated remediation.
87	
88	{IF CLEAN:}
89	**No action needed.** Skill is current with source code.
90	```
91	
92	### 3. Add Provenance Section
93	
94	Append to {outputFile}:
95	
96	```markdown
97	## Provenance
98	
99	| Field | Value |
100	|-------|-------|
101	| **Audit Date** | {current_date} |
102	| **Audited By** | Ferris (Audit mode) |
103	| **Forge Tier** | {tier} |
104	| **Tools Used** | {tool_list based on tier} |
105	| **Source Path** | {source_path} |
106	| **Skill Path** | {skill_path} |
107	| **Provenance Map** | {provenance_map_path} |
108	| **Provenance Age** | {days} days |
109	| **Mode** | {normal / degraded} |
110	| **Baseline Ref / Commit** | `{baseline_ref}` @ `{baseline_commit_short}` |
111	| **Audit Ref / Commit** | `{audit_ref}` @ `{audit_commit_short}` ({audit_ref_source}) |
112	| **Upstream Latest** | `{latest_tag or remote_head or "(not fetched)"}` |
113	
114	**Confidence Legend:**
115	- **T1:** AST extraction — high reliability, structural truth
116	- **T1-low:** Text pattern matching — moderate reliability
117	- **T2:** QMD temporal context — evidence-backed semantic analysis
118	```
119	
120	### 4. Update Report Frontmatter
121	
122	Update {outputFile} frontmatter:
123	- Append `'step-06-report'` to `stepsCompleted`
124	- Set `drift_score` to final calculated score
125	- Set `nextWorkflow` to `'update-skill'` if CRITICAL or HIGH findings, otherwise leave empty
126	
127	### 5. Present Final Report Summary
128	
129	"**Audit Complete: {skill_name}**
130	
131	---
132	
133	**Overall Drift Score: {CLEAN / MINOR / SIGNIFICANT / CRITICAL}**
134	
135	| Severity | Count |
136	|----------|-------|
137	| CRITICAL | {count} |
138	| HIGH | {count} |
139	| MEDIUM | {count} |
140	| LOW | {count} |
141	| **Total** | {total} |
142	
143	**Report saved to:** `{outputFile}`
144	
145	{IF CRITICAL/HIGH findings:}
146	**Action Required:** {count} priority items need remediation. Recommend running `[US] Update Skill` workflow.
147	
148	{IF MEDIUM/LOW only:}
149	**Minor Drift:** Skill is functional but could benefit from updates. See report for details.
150	
151	{IF CLEAN:}
152	**All Clear:** No drift detected. Skill accurately reflects current source code.
153	
154	---
155	
156	**Next Steps:**
157	{IF findings exist:}
158	1. **[US] Update Skill** — Automatically apply remediations from this drift report
159	2. **Review report** — Manual review at `{outputFile}`
160	
161	{IF CLEAN:}
162	1. **No action needed** — Skill is current
163	2. **[EX] Export Skill** — Skill is ready for distribution
164	
165	---
166	
167	**Audit workflow complete.**"
168	
169	### Result Contract
170	
171	Write the result contract per `shared/references/output-contract-schema.md`: the per-run record at `{forge_version}/audit-skill-result-{YYYYMMDD-HHmmss}.json` (UTC timestamp, resolution to seconds) and a copy at `{forge_version}/audit-skill-result-latest.json` (stable path for pipeline consumers — copy, not symlink). Include the drift report path in `outputs`; include `drift_count` and `severity` (CLEAN/MINOR/SIGNIFICANT/CRITICAL) in `summary`.
172	
173	### 6. Chain to Health Check
174	
175	ONLY WHEN the report has been written, presented, and the result contract saved will you then load, read the full file, and execute `{nextStepFile}`. The health-check step is the true terminal step — do not stop here even though the user-facing summary reads as final.
176	
177	
```

> TOOL

tool_use Bash
id: toolu_01XP12D8EmQbHEtc4F2ZKkHn
```json
{
  "command": "ls /home/armel/Projects/OSS/bmad-module-skill-forge/tools/ 2>&1 | grep -i 'valid\\|brief\\|skill'",
  "description": "List validator scripts"
}
```

> TOOL

tool_result
id: toolu_01XP12D8EmQbHEtc4F2ZKkHn
```
validate-doc-links.js
validate-docs-drift.js
validate-file-refs.js
validate-skills.js
```

> TOOL

tool_use Bash
id: toolu_01AwaSrwCU9X3pHzBYYFRicZ
```json
{
  "command": "grep -l \"amendments\\|scope\\.include\" /home/armel/Projects/OSS/bmad-module-skill-forge/tools/*.js 2>&1 | head -10",
  "description": "Find validators referencing amendments/scope"
}
```

> TOOL

tool_result
id: toolu_01AwaSrwCU9X3pHzBYYFRicZ
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01LU6KBHnfjTXpbS5r63RKzx
```json
{
  "command": "grep -rn \"scope\\.include\\|brief\\.scope\\|amendments\\[\\|amendments:\" /home/armel/Projects/OSS/bmad-module-skill-forge/src/ /home/armel/Projects/OSS/bmad-module-skill-forge/tools/ 2>&1 | grep -v -E \"node_modules|\\.git\" | head -40",
  "description": "Audit all amendments/scope.include consumers"
}
```

> TOOL

tool_result
id: toolu_01LU6KBHnfjTXpbS5r63RKzx
```
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-test-skill/steps-c/step-03-coverage-check.md:185:  - Set `scope.include` in the brief to point at the package's entry point(s)
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-test-skill/steps-c/step-03-coverage-check.md:222:2. **Otherwise re-derive at test time** from the brief's scope globs per the protocol. When the brief supplies `scope.tier_a_include`, re-derive from that narrower list; otherwise re-derive from `scope.include`. Use the resulting union count as `total_exports`.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-test-skill/steps-c/step-03-coverage-check.md:223:3. **Run the denominator inflation check** defined in `{sourceAccessProtocol}` stratified-scope resolution step 3 whenever re-derivation fell back to `scope.include`. If the `scope.include` union exceeds the provenance-map entry count by more than 25%, emit the Medium-severity `denominator inflation — coarse scope.include union exceeds authored surface` gap and append it to the Coverage Analysis gap list.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-test-skill/steps-c/step-03-coverage-check.md:226:Record the denominator source in the Coverage Analysis section as `Denominator: stratified ({effective_denominator | tier_a_include union | scope.include union}, {N} files matched)`. When stratified scope does not apply, use the standard barrel-based denominator and omit the stratified annotation.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-test-skill/steps-c/step-03-coverage-check.md:230:(`stats.effective_denominator`, `tier_a_include` union, `scope.include` union)
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-test-skill/steps-c/step-03-coverage-check.md:240:- `scope.include` union: {N | absent}           {← chosen if priority (3) applied}
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-test-skill/steps-c/step-03-coverage-check.md:290:**Denominator:** {barrel | stratified ({effective_denominator | scope.include union}, {N} files matched)}
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-test-skill/references/source-access-protocol.md:11:- **Empty-barrel packages (copy-paste / subpath-only distribution):** If the primary entry point is empty or re-exports nothing (e.g., `export {};` in `index.ts`, an empty `__init__.py`, `lib.rs` with no `pub use`), the package does not expose a barrel API. Do **not** compute coverage against the empty barrel — the denominator would be zero and the score meaningless. Instead, consult the skill brief's `scope.include` globs (`forge-data/{skill_name}/skill-brief.yaml`) to identify the authorized entry points, and build the public API surface from the **union of named exports across those files**. The skill brief's `scope.notes` field should document this distribution model explicitly; if present, treat it as confirmation that the empty barrel is by design rather than a bug. If no skill brief is available and the barrel is empty, set `analysis_confidence: docs-only` and report that the source API surface could not be determined.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-test-skill/references/source-access-protocol.md:13:- **Stratified-scope monorepo packages (curated subsets of multi-package repos):** If the source is a monorepo (detect via `packages/` layout, `workspaces` field in root `package.json`, `lerna.json`, `rush.json`, `nx.json`, or Cargo `[workspace]`) AND the skill brief's `scope.include` lists a curated file/directory subset rather than the full workspace, the coverage denominator must reflect only the authored surface, not the monorepo's global export count. This is distinct from the empty-barrel case: each workspace package may have a non-empty barrel, but the skill intentionally documents only a tiered subset.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-test-skill/references/source-access-protocol.md:20:     **Honor `scope.tier_a_include` when present.** When re-deriving, prefer the brief-level `scope.tier_a_include` narrow include list over the coarse `scope.include`. `tier_a_include` is an optional brief field that lists only the authoring surface the brief actually intends to document (tier A), letting the denominator match the brief's authoring-vs-installing intent even when `scope.include` uses coarse globs that also match internal infrastructure. When `tier_a_include` is present, resolve its globs (still filtered by `scope.exclude`), compute the union across those files, and use that count as the denominator. When absent, fall back to resolving `scope.include`.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-test-skill/references/source-access-protocol.md:22:  3. **Denominator inflation check (absent `tier_a_include`).** If re-derivation used `scope.include` because no `tier_a_include` was provided, compare the resulting union count against the provenance-map entry count (when provenance-map exists). If the `scope.include` union is more than 25% larger than the provenance-map entry count, the coarse globs are almost certainly sweeping in internal infrastructure that the brief did not intend to document. Emit a **Medium**-severity gap titled `denominator inflation — coarse scope.include union exceeds authored surface` that points the user at the brief for rescoping via `scope.tier_a_include`. Report both counts (`scope.include union: {N}`, `provenance-map entries: {M}`, `{percent}% inflation`) and state that the coverage score it produced is driven by denominator inflation rather than documentation gaps. The check is skipped when provenance-map is unavailable (there is no baseline to compare against).
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-test-skill/references/source-access-protocol.md:24:  Leave `analysis_confidence` unchanged (still `full` or `provenance-map` per the waterfall) — stratified scope does not degrade confidence, only the denominator. Annotate the coverage report with: `Stratified scope — denominator: {effective_denominator | tier_a_include union | scope.include union} ({N} files matched, {M} exports union)`.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-test-skill/references/source-access-protocol.md:28:- **Pattern-reference apps (non-library source):** If the source is a single-package repo whose purpose is demonstrating an integration pattern rather than distributing a library API — typical markers are `scope.type: "full-library"` **without** a barrel file at any recognized entry-point path (`__init__.py`, `index.ts`/`index.js`, `lib.rs`, `mod.rs`) AND without a monorepo layout — the skill's value lives in wiring patterns, not exports. None of the preceding three clauses fits: there is no barrel to count from, no empty-barrel `scope.include` to consult, and no monorepo stratification to re-derive.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-05-compile.md:110:  - `effective_denominator` (**optional** — emit only for stratified-scope monorepo packages): the count of public exports from files matched by the brief's authoring-surface globs, filtered by `scope.exclude`, resolved against `source_path`. **Prefer `scope.tier_a_include` when the brief supplies it** — that narrow list represents the authoring surface the brief intends to document; resolve its globs across `source_path` and count the union of named exports. **Otherwise use `scope.include`** — the coarse list. This is the coverage denominator `skf-test-skill` uses when the package is a curated subset of a multi-package repository, so it must match the brief's authoring intent. Compute when ALL of the following hold:
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-05-compile.md:112:    2. `scope.type` is not `full-library`, AND the resolved include list (`tier_a_include` if present, else `scope.include`) lists a curated file/directory subset rather than the full workspace.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/sub/step-02b-ccc-discover.md:53:**Primary query:** `"{brief.name} {brief.scope}"`
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/sub/step-02b-ccc-discover.md:57:- `brief.scope` is the scope field (e.g., "Full library", "Public API", or specific module names)
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/sub/step-02b-ccc-discover.md:59:**Query length cap:** Truncate to 80 characters if longer — ccc semantic search is sensitive to overly long queries. When truncating, keep the full skill name and trim `brief.scope` from the end. If `brief.scope` is very short (< 10 chars), append terms from `brief.description` to fill the remaining space.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:41:- `scope.include` — file globs to include
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:65:   - **Already in scope (matched by `scope.include`):** **remove the path from the filtered file list** and add it directly to `promoted_docs[]` with `{path, heuristic, size_bytes, line_count, content_hash}`. No prompt — the user or a prior amendment already said it belongs in scope, but authoritative docs must never reach §4 code extraction. This is both the "already promoted from a prior run" case and the "user manually added to scope.include" case.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:68:3. **Check existing amendments.** Before prompting, consult `brief.scope.amendments[]` (see `src/skf-brief-skill/assets/skill-brief-schema.md` for the schema). If any amendment entry has `path == candidate.path`, the decision is already recorded:
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:69:   - `action: "promoted"` → the file should already be in `scope.include` (amendments are write-through). No prompt. **Still populate `promoted_docs[]`** for this path — compute its content hash and add a `{path, heuristic, size_bytes, line_count, content_hash}` entry so step-05 §6 writes the `file_entries[]` row. This is the deterministic replay path for re-runs.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:82:   Excluded by pattern: {matching_exclude_pattern or "not matched by any scope.include"}
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:100:     2. Append to `brief.scope.include`: add the exact `candidate.path` as a literal glob (no wildcards — the amendment targets this specific file). This write ensures that a re-run of `skf-create-skill` against the amended brief sees the path in scope and skips re-prompting.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:101:     3. Append to `brief.scope.amendments[]` a new entry with `action: "promoted"`, `path: candidate.path`, `reason: {user-provided one-sentence reason or auto-generated "authoritative AI docs — matched heuristic {basename}"}`, `heuristic: {basename}`, `date: {today ISO}`, `workflow: "skf-create-skill"`.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:120:     1. Do NOT modify `scope.include` or `scope.exclude`.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:121:     2. Append to `brief.scope.amendments[]` a new entry with `action: "skipped"`, `path: candidate.path`, `reason: {user-provided reason or auto-generated "user declined promotion at create-skill §2a"}`, `heuristic: {basename}`, `date: {today ISO}`, `workflow: "skf-create-skill"`.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:145:**Re-running `skf-create-skill`** reads the amended brief. Files with `action: "promoted"` amendments already appear in `scope.include`, but §2a still runs — it detects the file is in scope AND has an existing amendment, and takes the "pre-decided" silent path. The `promoted_docs[]` list is rebuilt on each run by scanning amendments with `action: "promoted"` (this is the deterministic replay path).
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:152:The brief is the single source of truth for authored scope intent. The provenance map is the single source of truth for extracted state. `scope.amendments[]` is the bridge that records when those two intentionally diverged. `promoted_docs[]` is the in-memory handoff from §2a to step-05 §6; it is not persisted — the persisted form is the `file_entries[]` list in provenance-map.json.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03-extract.md:192:4. **Construct semantic query:** Build from brief data: `"{brief.name} {brief.scope}"`. Truncate to 80 characters — keep the full skill name and trim `brief.scope` from the end. If `brief.scope` is very short (< 10 chars), append terms from `brief.description` to fill the remaining space.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-test-skill/references/scoring-rules.md:199:| Medium   | Denominator inflation — stratified-scope `scope.include` union exceeds provenance-map entry count by >25% (brief missing `scope.tier_a_include`) |
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/references/extraction-patterns-tracing.md:80:- Only include files within brief's `scope.include` patterns (or auto-detected directories)
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/steps-c/step-03-scope-definition.md:51:- `scope.include`: confirmed doc URLs
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/steps-c/step-03d-component-extraction.md:98:**GATE [default: S]** — if `{headless_mode}` is true: auto-select [S] Skip (props-first extraction without registry), log "headless: no registry detected, auto-skip to props-first extraction (no path was provided in brief.scope.registry_path)", and append `{step: "step-03d-component-extraction", gate: "provide-or-skip-registry", decision: "S", rationale: "headless mode — no human to provide registry path", timestamp: {ISO}}` to `headless_decisions[]`. The default is `[S]` rather than `[P]` because providing a path requires user input that headless cannot supply; skipping degrades gracefully to a smaller but valid extraction.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/steps-c/step-04-confirm-brief.md:42:- **scope.include:** {include patterns from step 03}
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/steps-c/step-04-confirm-brief.md:69:  Include: {scope.include patterns, one per line}
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/assets/skill-brief-schema.md:28:| `scope.tier_a_include` | array | Glob patterns                                 | Optional. Narrower tier-A include list for stratified-scope monorepo skills. When present, `skf-test-skill` re-derives the coverage denominator from this list instead of the coarse `scope.include`, so the denominator reflects the authoring surface rather than incidentally-matched internal infrastructure. See `skf-test-skill/references/source-access-protocol.md` stratified-scope resolution. |
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/assets/skill-brief-schema.md:71:  # amendments:
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/assets/skill-brief-schema.md:90:`scope.amendments[]` is an additive, optional audit log of scope decisions made by workflows after the brief was first authored. Its primary writer is `skf-create-skill` §2a (Discovered Authoritative Files Protocol), which appends entries when extraction discovers authoritative AI documentation files (`llms.txt`, `AGENTS.md`, etc.) that the original scope patterns excluded.
/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/assets/skill-brief-schema.md:96:| `path` | string | yes | Relative path from source root to the file being amended. Matches the literal path added to `scope.include` (for `promoted` actions). |
```

> TOOL

tool_use Bash
id: toolu_012GDJhreRMRRCTDu8887cXQ
```json
{
  "command": "ls /home/armel/Projects/OSS/bmad-module-skill-forge/test/ 2>&1; grep -rln \"amendments\\|scope-expansion\" /home/armel/Projects/OSS/bmad-module-skill-forge/test/ 2>&1 | head",
  "description": "Check tests directory for amendments coverage"
}
```

> TOOL

tool_result
id: toolu_012GDJhreRMRRCTDu8887cXQ
```
fixtures
__pycache__
README.md
schema
test-agent-schema.js
test-cli-integration.js
test-compute-score-contract.py
test-installation-components.js
test-knowledge-base.js
test-skf-manifest-ops.py
test-skf-preflight.py
test-skf-rebuild-managed-sections.py
test-skf-severity-classify.py
test-skf-skill-inventory.py
test-skf-structural-diff.py
test-skf-validate-frontmatter.py
test-skf-validate-output.py
test-workflow-state.js
unit-test-schema.js
validate-agent-schema.js
```

> TOOL

tool_use Read
id: toolu_019W2AHvr7sX41Z2bUSvDGZZ
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/steps-c/step-01-init.md"
}
```

> TOOL

tool_result
id: toolu_019W2AHvr7sX41Z2bUSvDGZZ
```
1	---
2	nextStepFile: './step-02-detect-changes.md'
3	manualSectionRulesFile: 'references/manual-section-rules.md'
4	---
5	
6	# Step 1: Initialize Update
7	
8	## STEP GOAL:
9	
10	Load the existing skill and all its provenance data, detect whether this is an individual or stack skill, load the forge tier configuration, and present a baseline summary so the user can confirm the update scope before proceeding.
11	
12	## Rules
13	
14	- Focus only on loading existing artifacts and establishing the baseline — read-only operations
15	- Do not begin change detection (Step 02)
16	
17	## MANDATORY SEQUENCE
18	
19	**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.
20	
21	### 1. Request Skill Path
22	
23	"**Which skill would you like to update?**
24	
25	Provide either:
26	- A skill name (resolves via version-aware path resolution — see `knowledge/version-paths.md`)
27	- A full path to the skill folder
28	- A skill name with `--from-test-report` to use the test report's gap findings instead of source drift detection
29	- `--allow-workspace-drift` (gap-driven mode only) to intentionally bypass the step-03 §0.a guard that halts when the local workspace HEAD does not match `metadata.source_commit`. Only use this if you know the spot-checks should read the current workspace instead of the pinned tree — step-06 will NOT automatically re-pin
30	
31	**Skill:** {user provides path or name}"
32	
33	**Version-Aware Path Resolution:**
34	1. Read `{skills_output_folder}/.export-manifest.json` and look up the skill name in `exports` to get `active_version`
35	2. If found: resolve to `{skill_package}` = `{skills_output_folder}/{skill-name}/{active_version}/{skill-name}/`
36	3. If not in manifest: check for `active` symlink at `{skills_output_folder}/{skill-name}/active` — resolve to `{skill_group}/active/{skill-name}/`
37	4. If neither: fall back to flat path `{skills_output_folder}/{skill-name}/`. If SKILL.md exists at the flat path, auto-migrate per `knowledge/version-paths.md` migration rules
38	5. Store the resolved path as `{resolved_skill_package}` for all subsequent artifact loading
39	
40	Resolve the path to an absolute skill folder location.
41	
42	**If `--from-test-report` was provided (or user references a test report):**
43	Search for the test report at `{forge_data_folder}/{skill_name}/{active_version}/test-report-{skill_name}.md` (i.e., `{forge_version}/test-report-{skill_name}.md`). If not found at the versioned path, fall back to `{forge_data_folder}/{skill_name}/test-report-{skill_name}.md`. If found, set `test_report_path` in context and `update_mode: gap-driven`. If not found at either path, warn and continue with normal source drift mode.
44	
45	**If `--allow-workspace-drift` was provided:** set `allow_workspace_drift: true` in workflow context. This flag is consumed by step-03 §0.a's pre-flight drift guard (gap-driven mode only) and has no effect in normal source-drift mode.
46	
47	### 2. Validate Required Artifacts
48	
49	**Check SKILL.md exists:**
50	- Load `{resolved_skill_package}/SKILL.md`
51	- If missing: **ABORT** — "No SKILL.md found at `{resolved_skill_package}`. Run create-skill first."
52	
53	**Check metadata.json exists:**
54	- Load `{resolved_skill_package}/metadata.json`
55	- Extract: `name`, `skill_type` (single or stack), `version`, `generation_date`, `confidence_tier`, `source_root`
56	- If missing: **ABORT** — "No metadata.json found. This skill may have been created manually. Run create-skill to generate provenance data."
57	
58	**Detect skill type from metadata:**
59	- If `skill_type == "single"` or absent: flag as single skill
60	- If `skill_type == "stack"`: flag as stack skill (multi-file update mode)
61	
62	### Stack Skill Guard
63	
64	After loading metadata.json, check `skill_type`:
65	- If `skill_type` is `"stack"`: display message:
66	  "**Stack skills cannot be surgically updated.** Stack skills compose exports from multiple sources — surgical re-extraction requires re-running the full composition pipeline.
67	  
68	  **To update this stack skill**, run `skf-create-stack-skill` with the same project path. It will re-analyze manifests (code-mode) or re-read constituent skills (compose-mode) and produce an updated stack.
69	  
70	  If you came here from an audit report, the drift report identifies which constituent libraries changed — use that to decide whether re-composition is needed."
71	- Exit the workflow (do not proceed to step-02)
72	
73	### 3. Load Forge Tier Configuration
74	
75	**Load `{sidecar_path}/forge-tier.yaml`:**
76	- Extract: `tier` (Quick, Forge, Forge+, or Deep), available tools
77	- If missing: **ABORT** — "No forge-tier.yaml found. Run setup first to detect available tools."
78	
79	**Apply tier override:** Read `{sidecar_path}/preferences.yaml`. If `tier_override` is set and is a valid tier value (Quick, Forge, Forge+, or Deep), use it instead of the detected tier.
80	
81	**Determine analysis capabilities:**
82	- **Quick:** text pattern matching only → T1-low confidence
83	- **Forge:** AST structural extraction → T1 confidence
84	- **Forge+:** AST structural extraction + CCC semantic ranking → T1 confidence (with ccc signals)
85	- **Deep:** AST + QMD semantic enrichment → T1 + T2 confidence
86	
87	### 4. Load Provenance Map
88	
89	**Load `{forge_data_folder}/{skill_name}/{active_version}/provenance-map.json`** (i.e., `{forge_version}/provenance-map.json`). If not found at the versioned path, fall back to `{forge_data_folder}/{skill_name}/provenance-map.json`:
90	- Extract: export list, file mappings, extraction timestamps, confidence tiers
91	- Calculate provenance age (days since last extraction)
92	
93	**If provenance map missing at both paths:**
94	
95	"**WARNING:** No provenance map found at `{forge_version}/provenance-map.json` or flat fallback.
96	
97	Without a provenance map, update-skill cannot perform targeted change detection. Options:
98	
99	**[D]egraded mode** — Perform full re-extraction with T1-low confidence (equivalent to re-running create-skill but preserving [MANUAL] sections)
100	**[X]** — Abort and run create-skill first to generate provenance data
101	
102	Select: [D] Degraded / [X] Abort"
103	
104	- If D: set `degraded_mode = true`, proceed with full extraction scope
105	- If X: **ABORT**
106	
107	### 5. Load [MANUAL] Section Inventory
108	
109	Load {manualSectionRulesFile} to understand [MANUAL] detection patterns.
110	
111	**Scan SKILL.md for [MANUAL] sections:**
112	- Count all `<!-- [MANUAL:*] -->` markers
113	- Map each [MANUAL] block to its parent section (by heading hierarchy)
114	- Record section names and approximate line positions
115	
116	**For stack skills, also scan:**
117	- All `references/*.md` files for [MANUAL] markers
118	- All `references/integrations/*.md` files for [MANUAL] markers
119	
120	### 6. Resolve Source Code Path
121	
122	**From provenance map (if available):**
123	- Extract `source_root` path
124	- Validate source path exists and is accessible
125	
126	**If source path invalid or missing:**
127	
128	"**Source path from provenance map is invalid:** `{source_root}`
129	
130	Please provide the current source code path:
131	**Path:** {user provides path}"
132	
133	### 7. Present Baseline Summary
134	
135	"**Update Skill Baseline:**
136	
137	| Property | Value |
138	|----------|-------|
139	| **Skill** | {skill_name} |
140	| **Type** | {single/stack} |
141	| **Version** | {version} |
142	| **Created** | {created date} |
143	| **Source** | {source_root} |
144	| **Forge Tier** | {forge_tier} (current) vs {original_tier} (at creation) |
145	| **Provenance Age** | {days} days since last extraction |
146	| **Exports** | {export_count} tracked exports |
147	| **[MANUAL] Sections** | {manual_count} preserved sections |
148	| **Mode** | {normal/degraded/gap-driven} |
149	
150	**Analysis plan:** {tier_description}
151	- {Quick: text pattern diff → T1-low findings}
152	- {Forge: AST structural diff → T1 findings}
153	- {Deep: AST structural + QMD semantic diff → T1 + T2 findings}
154	
155	**Ready to detect changes and update this skill?**"
156	
157	### 8. Present MENU OPTIONS
158	
159	Display: "**Select:** [C] Continue to Change Detection"
160	
161	#### Menu Handling Logic:
162	
163	- IF C: Load, read entire file, then execute {nextStepFile}
164	- IF Any other: help user respond, then [Redisplay Menu Options](#8-present-menu-options)
165	
166	#### EXECUTION RULES:
167	
168	- ALWAYS halt and wait for user input after presenting menu
169	- **GATE [default: C]** — If `{headless_mode}`: auto-proceed with [C] Continue, log: "headless: auto-continue past update confirmation"
170	- ONLY proceed to next step when user selects 'C'
171	
172	## CRITICAL STEP COMPLETION NOTE
173	
174	ONLY WHEN [C] is selected and baseline has been established with all required artifacts loaded, will you then load and read fully `{nextStepFile}` to execute change detection.
175	
176	
```

> AGENT

Plan confirmed: one focused commit closing #233. Two surgical edits — `step-02-detect-changes.md` (new §1c + §2.2 for major-version scope reconciliation) and `skill-brief-schema.md` (formalize `category` field + new actions). No other consumers parse `amendments[]` so it's purely additive.

Let me create a branch and make the edits.

> TOOL

tool_use Bash
id: toolu_01VNmdSPXkf9GErUCr8Z7Sxq
```json
{
  "command": "git checkout -b fix/update-skill-major-version-scope-233",
  "description": "Create branch for issue #233"
}
```

> TOOL

tool_result
id: toolu_01VNmdSPXkf9GErUCr8Z7Sxq
```
Switched to a new branch 'fix/update-skill-major-version-scope-233'
```

> TOOL

tool_use Edit
id: toolu_018eqvZMLNiC12dqJT7zqwwx
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/steps-c/step-02-detect-changes.md",
  "old_string": "### 2. Compare Against Provenance Map\n\n**If normal mode (provenance map available):**\n\n#### 2.0 — Build Pre-filter Exclusion Set",
  "new_string": "### 1c. Major-Version Scope Reconciliation (Pre-Detection)\n\n**Purpose:** When upstream undergoes a paradigm shift (rebrand, package restructure, major-version rewrite), the brief's `scope.include` no longer reflects the real public API. §1b handles new authoritative-doc files; §1c handles new **code globs** that fall outside the original scope. Without it, update-skill silently misses the new surface and pays the gap cost on every future update — the cocoindex `0.3.37 → 1.0.0` and cognee `0.5.8 → 1.0.0` runs are existence proofs that this case is real and recurring.\n\n**Skip this section entirely if:**\n\n- `update_mode == \"gap-driven\"` (test-report mode — source hasn't drifted), OR\n- `metadata.json.source_type == \"docs-only\"` (no source tree to scope), OR\n- No audit drift report is available at the path computed in step 1 below.\n\n**Procedure:**\n\n1. **Locate the most recent audit drift report.** Search `{forge_data_folder}/{skill_name}/{baseline_version}/drift-report-*.md`, sorted by timestamp descending. Pick the latest. If none found, **skip §1c entirely** — the post-detection deletion-ratio trigger in §2.2 still catches major restructures even without an audit pass.\n\n2. **Parse the report for an \"Out-of-Scope Observations\" section.** Look for either a top-level `## Out-of-Scope Observations` heading or a `### Out-of-Scope New Public API` subsection under `## Remediation Suggestions`. Each entry must expose:\n\n   - `path` — literal file path or directory glob (e.g., `python/cocoindex/_internal/api.py` or `python/cocoindex/resources/**`)\n   - `evidence` — short one-liner from the report (export count, rationale)\n\n   **Note:** This section is an optional audit-skill output. `skf-audit-skill` does not currently discover new files (per `src/skf-audit-skill/steps-c/step-02-re-index.md` — new-file detection is the responsibility of update-skill). The section is a forward-looking integration point: manual additions to the drift report or a future audit-skill enhancement populate it. If absent, no candidates from this trigger — proceed to step 6.\n\n3. **Reconcile against existing amendments.** For each candidate, consult `brief.scope.amendments[]`:\n\n   - `action: \"promoted\"` AND `path` matches → already in scope, skip silently.\n   - `action: \"skipped\"` AND `path` matches → user previously declined, honor silently.\n   - `action: \"demoted-include\"` or `action: \"demoted-exclude\"` AND `path` matches → user previously narrowed scope on this path, do not re-prompt; record as `pre_decided`.\n   - No matching amendment → continue to user prompt.\n\n4. **Prompt for each unresolved candidate.** Present the same menu shape as §1b:\n\n   ```\n   **Out-of-scope new public API discovered**\n\n   Path:          {candidate.path}\n   Evidence:      {evidence from drift report}\n   Drift report:  {report relative path}\n\n   This path was not in the brief's `scope.include` when the skill was created. How should update-skill handle it?\n\n   [P] Promote — add to scope.include AND extract in this run\n   [S] Skip    — leave out of scope AND record skip in amendments (no re-prompt)\n   [U] Update  — halt this run and return to skf-brief-skill to refine scope\n   ```\n\n5. **Headless mode (`{headless_mode}` is true):** auto-select `[S] Skip` for every candidate — record `action: \"skipped\"`, `category: \"scope-expansion\"`, `reason: \"headless: no user to prompt\"`, `workflow: \"skf-update-skill\"`. A non-interactive update run must never silently expand scope.\n\n6. **Apply decision:**\n\n   - **[P] Promote:**\n     1. Append `candidate.path` to `brief.scope.include` as a literal glob (preserve any wildcards from the drift report).\n     2. Append a `brief.scope.amendments[]` entry: `action: \"promoted\"`, `category: \"scope-expansion\"`, `path: candidate.path`, `reason: {user-provided or auto: \"out-of-scope new public API — drift report {report basename}\"}`, `evidence: {evidence string}`, `date: {today ISO}`, `workflow: \"skf-update-skill\"`.\n     3. **Write the amended brief back to disk immediately** at `{forge_data_folder}/{skill_name}/skill-brief.yaml`. Preserve all other fields.\n     4. Display: `\"Promoted {path} — brief amended; §2 Category A will pick up matching files as ADDED.\"`\n     5. **No `promoted_docs_new[]` entry and no `change_detection_excludes` write** — promoted code globs flow through the standard §2 Category A → §3 extraction path, unlike §1b's promoted docs which bypass extraction.\n\n   - **[S] Skip:**\n     1. Do NOT modify `scope.include` or `scope.exclude`.\n     2. Append a `brief.scope.amendments[]` entry: `action: \"skipped\"`, `category: \"scope-expansion\"`, `path: candidate.path`, `reason: {user-provided or auto: \"user declined promotion at update-skill §1c\"}`, `evidence: {evidence string}`, `date: {today ISO}`, `workflow: \"skf-update-skill\"`.\n     3. **Write the amended brief back to disk** so neither §1c nor a future run will re-prompt.\n     4. Display: `\"Skipped {path} — decision recorded in amendments.\"`\n\n   - **[U] Update:**\n     1. Halt the workflow immediately.\n     2. Display: `\"Halting update-skill. Re-run skf-brief-skill to refine scope for {skill_name}, then re-run skf-update-skill.\"`\n     3. Exit with status `halted-for-brief-refinement`. Change manifest is not yet built — no partial writes to provenance.\n\n7. **Summary:** After all candidates are resolved (or none were found):\n\n   - `\"Scope reconciliation: {N} candidates, {P} promoted, {S} skipped, {A} pre-decided from amendments.\"`\n   - If N = 0 (section absent or empty): `\"Scope reconciliation: no out-of-scope observations in drift report.\"`\n   - If §1c was skipped entirely (no drift report): omit this line; §2.2 will still run.\n\n**Record for evidence report:** the update-skill evidence report appends `scope_reconciliation_pre: {drift_report: path, candidates: N, promoted: P, skipped: S, pre_decided: A, decisions: [{path, action, evidence}]}` (omit when §1c was skipped).\n\n### 2. Compare Against Provenance Map\n\n**If normal mode (provenance map available):**\n\n#### 2.0 — Build Pre-filter Exclusion Set"
}
```

> TOOL

tool_result
id: toolu_018eqvZMLNiC12dqJT7zqwwx
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/steps-c/step-02-detect-changes.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now add the post-detection trigger (§2.2) and the section-3 update.

> TOOL

tool_use Edit
id: toolu_018exje4KjMFgctLadhk8DDt
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/steps-c/step-02-detect-changes.md",
  "old_string": "Aggregate all subprocess results into a unified change manifest.\n\n**If degraded mode (no provenance map):**\n- All source files are treated as MODIFIED\n- All exports will be fully re-extracted in step 03\n- Skip export-level comparison\n\n### 3. Build Change Manifest",
  "new_string": "Aggregate all subprocess results into a unified change manifest.\n\n**If degraded mode (no provenance map):**\n- All source files are treated as MODIFIED\n- All exports will be fully re-extracted in step 03\n- Skip export-level comparison\n\n#### 2.2 — Major-Version Scope Reconciliation (Post-Detection)\n\n**Purpose:** §1c catches the major-version case when an audit drift report supplies explicit candidates. §2.2 is the safety net that fires when no audit was run (or audit emitted no out-of-scope section): it inspects the just-built Category A/B results for the deletion-ratio signature of a major-version restructure and gives the user an off-ramp before §3 commits the change manifest.\n\n**Skip this section entirely if:**\n\n- `update_mode == \"gap-driven\"` (test-report mode), OR\n- `degraded_mode == true` (no provenance baseline to compare against — every export looks \"modified\", deletion ratio is meaningless), OR\n- Provenance map's tracked export count is zero.\n\n**Trigger:** Compute\n\n```\ndeleted_export_count = (sum of exports across Category A DELETED files)\n                     + (DELETED_EXPORT count from Category B)\ntotal_provenance_exports = provenance_map.entries.length\ndeletion_ratio = deleted_export_count / total_provenance_exports\n```\n\nIf `deletion_ratio >= 0.50`, present the prompt below. Otherwise skip §2.2 silently and continue to §3.\n\n**Prompt:**\n\n```\n**Major-version scope shift detected**\n\nDeleted exports:        {deleted_export_count} of {total_provenance_exports} ({percent}%)\nDeleted files:          {deleted_file_count}\nAdded files (in scope): {added_in_scope_count}\nRenamed/moved exports:  {renamed_or_moved_count}\n\nThe upstream surface appears to have been substantially replaced. The brief's\n`scope.include` patterns may no longer reflect the real public API.\n\n[C] Continue — proceed with re-extraction; the deletion is intentional\n[B] Brief    — halt and re-run skf-brief-skill to refine scope first\n[A] Audit    — halt and run skf-audit-skill to map the new surface, then re-run update-skill\n```\n\n**Headless mode (`{headless_mode}` is true):** auto-select `[C] Continue`, log a WARN-level entry to the evidence report (`scope_reconciliation_post: {trigger: \"deletion-ratio\", ratio: X, decision: \"headless-continue\"}`), and surface the warning in step-07's report. A non-interactive run must not silently halt, but the user must be able to see the signal post-hoc.\n\n**Apply decision:**\n\n- **[C] Continue:** record `scope_reconciliation_post: {trigger: \"deletion-ratio\", ratio: X, decision: \"continue\"}` and proceed to §3.\n- **[B] Brief:** halt with status `halted-for-brief-refinement`. Display: `\"Halting update-skill. Re-run skf-brief-skill to refine scope for {skill_name}, then re-run skf-update-skill.\"` Change manifest discarded — no partial writes.\n- **[A] Audit:** halt with status `halted-for-audit`. Display: `\"Halting update-skill. Run skf-audit-skill against {skill_name} to map the new surface — its drift report will feed §1c on the next update-skill run.\"` Change manifest discarded.\n\n**Why both §1c and §2.2:** §1c is precise (per-path P/S/U) but requires upstream signal from audit-skill. §2.2 is coarse (single halt/continue) but self-contained — it fires even when the user runs update-skill directly without audit. Together they cover the major-version case across the two real workflows.\n\n### 3. Build Change Manifest"
}
```

> TOOL

tool_result
id: toolu_018exje4KjMFgctLadhk8DDt
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-update-skill/steps-c/step-02-detect-changes.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now update the brief schema to formalize the `category` field and new action values.

> TOOL

tool_use Edit
id: toolu_01JqhWHsaVWbmdZcLR4xbSK4
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/assets/skill-brief-schema.md",
  "old_string": "  # Optional: amendment log for scope decisions made during create-skill §2a\n  # amendments:\n  #   - path: \"apps/docs/public/llms.txt\"\n  #     action: \"promoted\"          # \"promoted\" | \"skipped\"\n  #     reason: \"authoritative AI docs — only source for canonical install command\"\n  #     heuristic: \"llms.txt\"\n  #     date: \"2026-04-11\"\n  #     workflow: \"skf-create-skill\"",
  "new_string": "  # Optional: amendment log for scope decisions made during create-skill §2a,\n  # update-skill §1b (auth-doc), and update-skill §1c (scope-expansion).\n  # amendments:\n  #   - path: \"apps/docs/public/llms.txt\"\n  #     action: \"promoted\"          # \"promoted\" | \"skipped\" | \"demoted-include\" | \"demoted-exclude\"\n  #     category: \"auth-doc\"        # \"auth-doc\" (default for legacy entries) | \"scope-expansion\"\n  #     reason: \"authoritative AI docs — only source for canonical install command\"\n  #     heuristic: \"llms.txt\"        # required for auth-doc; absent for scope-expansion\n  #     date: \"2026-04-11\"\n  #     workflow: \"skf-create-skill\"\n  #   - path: \"python/cocoindex/_internal/api.py\"\n  #     action: \"promoted\"\n  #     category: \"scope-expansion\"\n  #     reason: \"out-of-scope new public API — drift report drift-report-20260424-212355.md\"\n  #     evidence: \"~70 new exports flagged out-of-scope by audit\"\n  #     date: \"2026-04-25\"\n  #     workflow: \"skf-update-skill\""
}
```

> TOOL

tool_result
id: toolu_01JqhWHsaVWbmdZcLR4xbSK4
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/assets/skill-brief-schema.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01Lm2fK3FSPJbb99S5ZNRCn8
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/assets/skill-brief-schema.md",
  "old_string": "### Scope Amendments (Optional)\n\n`scope.amendments[]` is an additive, optional audit log of scope decisions made by workflows after the brief was first authored. Its primary writer is `skf-create-skill` §2a (Discovered Authoritative Files Protocol), which appends entries when extraction discovers authoritative AI documentation files (`llms.txt`, `AGENTS.md`, etc.) that the original scope patterns excluded.\n\n**Entry fields:**\n\n| Field | Type | Required | Description |\n|---|---|---|---|\n| `path` | string | yes | Relative path from source root to the file being amended. Matches the literal path added to `scope.include` (for `promoted` actions). |\n| `action` | string | yes | One of: `promoted` (file added to scope with a literal `scope.include` entry), `skipped` (user declined promotion; file remains out of scope, decision recorded to prevent re-prompting). |\n| `reason` | string | yes | Human-readable sentence explaining the decision. Either user-provided at prompt time or auto-generated (\"authoritative AI docs — matched heuristic {basename}\"). |\n| `heuristic` | string | yes | The basename heuristic that matched (`llms.txt`, `AGENTS.md`, etc.) so future audits can verify the file still matches its original classification. |\n| `date` | string | yes | ISO date (`YYYY-MM-DD`) when the amendment was recorded. |\n| `workflow` | string | yes | Workflow name that wrote the amendment (`skf-create-skill`, `skf-update-skill`). Identifies which workflow's §2a-equivalent made the decision. |\n\n**Promotion write-through:** When `action: \"promoted\"`, the workflow also appends the literal path to `scope.include`. This is a belt-and-suspenders design: future `skf-create-skill` runs read `scope.include` during §2 and include the file in the filtered list automatically, so §2a finds no candidate and does not re-prompt. The `amendments[]` entry is the human-readable audit trail of *why* the path was added.\n\n**Skip recording:** When `action: \"skipped\"`, the workflow does NOT modify `scope.include` or `scope.exclude`. The amendment entry alone is enough to prevent re-prompting, because §2a checks `amendments[]` before prompting.\n\n**Backward compatibility:** `scope.amendments` is optional. Briefs without this field validate unchanged. Treat missing as an empty list.\n\n**Who reads `amendments[]`:**\n\n- `skf-create-skill` §2a consults it to avoid re-prompting on decided files.\n- `skf-update-skill` §1b (mirror of §2a) consults it for the same reason.\n- `skf-audit-skill` may optionally report on stale promotions (promoted files that no longer exist in source) as a future enhancement — not currently implemented.\n- Humans reading the brief see the audit trail of non-obvious scope decisions.\n\n**Who writes `amendments[]`:**\n\n- `skf-create-skill` §2a (Discovered Authoritative Files Protocol)\n- `skf-update-skill` §1b (mirror of §2a applied during change detection)\n- Manual edits by the brief author are permitted but should include all required fields above.",
  "new_string": "### Scope Amendments (Optional)\n\n`scope.amendments[]` is an additive, optional audit log of scope decisions made by workflows after the brief was first authored. Two writer paths exist today:\n\n- **Auth-doc promotions** (`category: \"auth-doc\"`) — `skf-create-skill` §2a and its mirror `skf-update-skill` §1b append entries when extraction discovers authoritative AI documentation files (`llms.txt`, `AGENTS.md`, etc.) that the original scope patterns excluded.\n- **Scope-expansion promotions** (`category: \"scope-expansion\"`) — `skf-update-skill` §1c appends entries when an audit drift report flags out-of-scope new public API paths (typically a major-version restructure where the brief's `scope.include` no longer reflects the real surface).\n\n**Entry fields:**\n\n| Field | Type | Required | Description |\n|---|---|---|---|\n| `path` | string | yes | Relative path (or glob, for `category: \"scope-expansion\"`) from source root to the file or tree being amended. For `promoted` actions this matches the literal entry added to `scope.include`. |\n| `action` | string | yes | One of: `promoted` (path added to `scope.include`), `skipped` (user declined promotion; decision recorded to prevent re-prompting), `demoted-include` (path removed from `scope.include` — only valid with `category: \"scope-expansion\"`), `demoted-exclude` (path removed from `scope.exclude` — only valid with `category: \"scope-expansion\"`). |\n| `category` | string | no | One of: `auth-doc` (default for entries without this field — the historical sole use case), `scope-expansion`. Distinguishes which workflow path wrote the entry and which writer-rules apply on re-runs. |\n| `reason` | string | yes | Human-readable sentence explaining the decision. Either user-provided at prompt time or auto-generated. |\n| `heuristic` | string | conditional | Required for `category: \"auth-doc\"` — the basename that matched (`llms.txt`, `AGENTS.md`, etc.). Omit for `category: \"scope-expansion\"`. |\n| `evidence` | string | conditional | Required for `category: \"scope-expansion\"` — short rationale from the source signal (e.g., a drift-report finding's evidence one-liner). Omit for `category: \"auth-doc\"`. |\n| `date` | string | yes | ISO date (`YYYY-MM-DD`) when the amendment was recorded. |\n| `workflow` | string | yes | Workflow name that wrote the amendment (`skf-create-skill`, `skf-update-skill`). Identifies which workflow made the decision. |\n\n**Promotion write-through:** When `action: \"promoted\"`, the workflow also appends the literal path to `scope.include`. This is a belt-and-suspenders design: future runs read `scope.include` during scope filtering and include the file in the filtered list automatically, so the §2a/§1b/§1c discovery loop finds no candidate and does not re-prompt. The `amendments[]` entry is the human-readable audit trail of *why* the path was added.\n\n**Skip recording:** When `action: \"skipped\"`, the workflow does NOT modify `scope.include` or `scope.exclude`. The amendment entry alone is enough to prevent re-prompting, because the discovery loop checks `amendments[]` before prompting.\n\n**Demotion (scope-expansion only):** `demoted-include` removes a previously-promoted path from `scope.include` — used when a prior `[P]` decision is reversed. `demoted-exclude` removes a path from `scope.exclude` — used when a previously excluded path needs to be re-evaluated. Both write the structural change and append the amendment so future runs see the rationale. Demotion is not valid for `category: \"auth-doc\"`: auth-doc skips already prevent re-prompting without scope mutation.\n\n**Backward compatibility:** `scope.amendments` is optional. Briefs without this field validate unchanged. Treat missing as an empty list. Existing entries without `category` are equivalent to `category: \"auth-doc\"` — readers must default the field when absent.\n\n**Who reads `amendments[]`:**\n\n- `skf-create-skill` §2a consults it to avoid re-prompting on decided auth-doc files.\n- `skf-update-skill` §1b (mirror of §2a) consults it for the same auth-doc reason.\n- `skf-update-skill` §1c consults it to avoid re-prompting on decided scope-expansion candidates and to honor prior `demoted-*` decisions.\n- `skf-audit-skill` may optionally report on stale promotions (promoted paths that no longer exist in source) as a future enhancement — not currently implemented.\n- Humans reading the brief see the audit trail of non-obvious scope decisions.\n\n**Who writes `amendments[]`:**\n\n- `skf-create-skill` §2a (Discovered Authoritative Files Protocol) — `category: \"auth-doc\"`\n- `skf-update-skill` §1b (mirror of §2a applied during change detection) — `category: \"auth-doc\"`\n- `skf-update-skill` §1c (Major-Version Scope Reconciliation) — `category: \"scope-expansion\"`\n- Manual edits by the brief author are permitted but should include all required fields above (and `category` when the entry is not an auth-doc decision)."
}
```

> TOOL

tool_result
id: toolu_01Lm2fK3FSPJbb99S5ZNRCn8
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/assets/skill-brief-schema.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now run the quality gate to make sure nothing breaks.

> TOOL

tool_use Bash
id: toolu_0118W8Z9kPxFLFRSbc4pfq6t
```json
{
  "command": "npm run quality 2>&1 | tail -80",
  "description": "Run quality gate",
  "timeout": 300000
}
```

> TOOL

tool_result
id: toolu_0118W8Z9kPxFLFRSbc4pfq6t
```
[32m✓[0m link resolves: split-body-strategy.md -> agentskills-spec.md
[32m✓[0m link resolves: split-body-strategy.md -> skill-lifecycle.md
[32m✓[0m link resolves: tool-resolution.md -> ccc-bridge.md
[32m✓[0m link resolves: tool-resolution.md -> progressive-capability.md
[32m✓[0m link resolves: tool-resolution.md -> confidence-tiers.md
[32m✓[0m link resolves: tool-resolution.md -> qmd-registry.md
[32m✓[0m link resolves: version-paths.md -> agentskills-spec.md
[32m✓[0m link resolves: version-paths.md -> skill-lifecycle.md
[32m✓[0m link resolves: version-paths.md -> provenance-tracking.md
[32m✓[0m link resolves: zero-hallucination.md -> confidence-tiers.md
[32m✓[0m link resolves: zero-hallucination.md -> provenance-tracking.md
[32m✓[0m link resolves: zero-hallucination.md -> progressive-capability.md
[32m✓[0m cross-fragment links detected (at least one)
[32m✓[0m no broken cross-fragment links

[36m========================================
Test Results:
  Passed: [32m95[0m
  Warnings: [33m0[0m
  Failed: [31m0[0m
========================================[0m

[32m✨ Knowledge base tests passed![0m


> bmad-module-skill-forge@1.0.0 validate:schemas
> node test/validate-agent-schema.js

🔍 Scanning for agent and manifest files...

Found 0 agent file(s), 1 manifest file(s)

✅ src/skf-forger/bmad-skill-manifest.yaml

✨ All 1 file(s) passed validation!


> bmad-module-skill-forge@1.0.0 validate:skills
> node tools/validate-skills.js --strict


Validating skills in: /home/armel/Projects/OSS/bmad-module-skill-forge/src
Mode: STRICT (exit 1 on HIGH+)


────────────────────────────────────────────────────────────

Summary:
   Skills scanned: 15
   Skills with findings: 0
   Total findings: 0

   All skills passed validation!


> bmad-module-skill-forge@1.0.0 validate:refs
> node tools/validate-file-refs.js --strict


Validating file references in: /home/armel/Projects/OSS/bmad-module-skill-forge/src
Mode: STRICT (exit 1 on issues)

Found 180 source files


────────────────────────────────────────────────────────────

Summary:
   Files scanned: 180
   References checked: 269
   Broken references: 0
   Absolute path leaks: 0

   All file references valid!


> bmad-module-skill-forge@1.0.0 docs:validate-drift
> node tools/validate-docs-drift.js

OK: skf_version 1.0.0 matches package.json; 4 skills checked against /home/armel/Projects/OSS/oh-my-skills, no drift.
```

> AGENT

All 95 knowledge tests, schema validation, skills validation, file refs, and docs drift pass. Let me look at the final diff before committing.

> TOOL

tool_use Bash
id: toolu_01U4XniRF6QHqeXU5idxCKvp
```json
{
  "command": "git diff --stat",
  "description": "Show diff stats"
}
```

> TOOL

tool_result
id: toolu_01U4XniRF6QHqeXU5idxCKvp
```
 src/skf-brief-skill/assets/skill-brief-schema.md   |  54 ++++++---
 .../steps-c/step-02-detect-changes.md              | 123 +++++++++++++++++++++
 2 files changed, 159 insertions(+), 18 deletions(-)
```

> TOOL

tool_use Bash
id: toolu_01P6QPRheiYjQCNqddynFvAZ
```json
{
  "command": "git add src/skf-update-skill/steps-c/step-02-detect-changes.md src/skf-brief-skill/assets/skill-brief-schema.md && git status",
  "description": "Stage edits and confirm"
}
```

> TOOL

tool_result
id: toolu_01P6QPRheiYjQCNqddynFvAZ
```
On branch fix/update-skill-major-version-scope-233
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   src/skf-brief-skill/assets/skill-brief-schema.md
	modified:   src/skf-update-skill/steps-c/step-02-detect-changes.md
```

> TOOL

tool_use Bash
id: toolu_017u1AULCwWwGhQuqT5yxkXJ
```json
{
  "command": "git commit -m \"$(cat <<'EOF'\nfeat(update-skill): add major-version scope reconciliation (#233)\n\nCloses the gap surfaced by health-check #233: when upstream undergoes a\nparadigm shift (rebrand, package restructure, major-version rewrite), the\nbrief's `scope.include` no longer reflects the real public API. update-skill\nhad no documented mechanism to handle this — the cocoindex 0.3.37 -> 1.0.0\nand cognee 0.5.8 -> 1.0.0 runs paid the cost via ad-hoc brief amendments\nand forced user-facing decisions every run.\n\n- step-02-detect-changes.md §1c (pre-detection): parses an audit drift\n  report's \"Out-of-Scope Observations\" section and presents a per-path\n  P/S/U menu, mirroring §1b's auth-doc flow. Headless auto-skips.\n- step-02-detect-changes.md §2.2 (post-detection): self-contained safety\n  net that fires when >=50% of provenance-map exports are deleted, even\n  without an audit pass. Single C/B/A halt-or-continue decision.\n- skill-brief-schema.md: formalizes the `category` field on amendments\n  (`auth-doc` | `scope-expansion`, defaulting to `auth-doc` for backward\n  compat) and documents the new actions `demoted-include` and\n  `demoted-exclude` for code-glob amendments.\n\nNo regressions: amendments[] has no programmatic consumers — only step\nfiles and humans read it. New fields are additive and gated by `category`.\nThe `promoted` action retains its original write-through semantics; legacy\nauth-doc entries without a `category` field are read as `auth-doc`.\n\nFixes #233\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\nEOF\n)\"",
  "description": "Commit the change"
}
```

> TOOL

tool_result
id: toolu_017u1AULCwWwGhQuqT5yxkXJ
```
<persisted-output>
Output too large (50.2KB). Full output saved to: /home/armel/.claude/projects/-home-armel-Projects-OSS-bmad-module-skill-forge/99f00f8e-1ebb-42e9-8fb3-ccbaf250ddad/tool-results/b09qdt6bt.txt

Preview (first 2KB):
[STARTED] Backing up original state...
[COMPLETED] Backed up original state in git stash (e7639a5)
[STARTED] Running tasks for staged files...
[STARTED] package.json — 2 files
[STARTED] *.{js,cjs,mjs} — 0 files
[STARTED] *.yaml — 0 files
[STARTED] *.json — 0 files
[STARTED] *.md — 2 files
[STARTED] *.astro — 0 files
[SKIPPED] *.{js,cjs,mjs} — no files
[SKIPPED] *.yaml — no files
[SKIPPED] *.json — no files
[SKIPPED] *.astro — no files
[STARTED] markdownlint-cli2
[COMPLETED] markdownlint-cli2
[COMPLETED] *.md — 2 files
[COMPLETED] package.json — 2 files
[COMPLETED] Running tasks for staged files...
[STARTED] Applying modifications from tasks...
[COMPLETED] Applying modifications from tasks...
[STARTED] Cleaning up temporary files...
[COMPLETED] Cleaning up temporary files...

> bmad-module-skill-forge@1.0.0 test
> npm run test:schemas && npm run test:install && npm run test:cli && npm run test:workflow && npm run test:python && npm run test:knowledge && npm run validate:schemas && npm run validate:skills && npm run validate:refs && npm run lint && npm run lint:md && npm run format:check


> bmad-module-skill-forge@1.0.0 test:schemas
> node test/test-agent-schema.js

[36m╔═══════════════════════════════════════════════════════════╗[0m
[36m║  Agent Schema Validation Test Suite                      ║[0m
[36m╚═══════════════════════════════════════════════════════════╝[0m

Found [36m52[0m test fixture(s)

[34m❌ CRITICAL ACTIONS (invalid)[0m
  [32m✓[0m empty-string-in-actions [2mGot expected error (custom): agent.critical_actions[] must be a non-empty string[0m
  [32m✓[0m actions-as-string [2mGot expected error (invalid_type): Expected array, received string[0m

[34m❌ MENU (invalid)[0m
  [32m✓[0m missing-menu [2mGot expected error (invalid_type): Required[0m
  [32m✓[0m empty-menu [2mGot expected error (too_small): agent.menu must include at least one entry[0m

[34m❌ MENU COMMANDS (invalid)[0m
...
</persisted-output>
```

> TOOL

tool_use Bash
id: toolu_01UNE8xzecdz7NGap7jBNJpz
```json
{
  "command": "git log --oneline -3 && git status",
  "description": "Verify commit landed"
}
```

> TOOL

tool_result
id: toolu_01UNE8xzecdz7NGap7jBNJpz
```
48cdfc9 feat(update-skill): add major-version scope reconciliation (#233)
50ee7f7 Merge pull request #232 from armelhbobdad/fix/audit-skill-gaps-230-231
8c7aa90 fix(audit-skill): correct brief-gate framing for new entry points
On branch fix/update-skill-major-version-scope-233
nothing to commit, working tree clean
```

> AGENT

Commit landed cleanly through the husky pre-commit hook (markdownlint + full `npm run quality` test suite). Want me to push the branch and open a PR for #233?

**Summary**
- 1 open issue (#233) → 1 commit `48cdfc9` `feat(update-skill): add major-version scope reconciliation (#233)` on branch `fix/update-skill-major-version-scope-233`.
- 2 files, +159/-18:
  - `src/skf-update-skill/steps-c/step-02-detect-changes.md` — new §1c (pre-detection, drift-report-driven P/S/U menu) and §2.2 (post-detection, ≥50%-deletion safety net with C/B/A halt-or-continue).
  - `src/skf-brief-skill/assets/skill-brief-schema.md` — formalized `category` field (`auth-doc` default for backward compat, `scope-expansion` new), documented `demoted-include`/`demoted-exclude` actions.

**Regression review**
- `amendments[]` has zero programmatic consumers (grepped `tools/`, `test/`, `src/`) — only step files and humans read it. New fields are additive.
- Existing entries without `category` are read as `auth-doc` (documented).
- `promoted` action keeps its write-through semantics; `demoted-*` is gated to `category: scope-expansion` so create-skill §2a / update-skill §1b auth-doc paths are untouched.
- §1c skips entirely when no drift report exists — never blocks the normal-mode run.
- §2.2 skips on `degraded_mode` (deletion ratio is meaningless without a baseline) and on `gap-driven` mode.
- Quality gate (95 knowledge tests, schema validation, skills validation, file refs, docs drift) all green; husky pre-commit hook ran the full suite without complaint.
