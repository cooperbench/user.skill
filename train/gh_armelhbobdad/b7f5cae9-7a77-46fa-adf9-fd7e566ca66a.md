> DEVELOPER

Execute the story-automator review workflow for story 3.5.

READ this skill first: .claude/skills/bmad-story-automator-review/SKILL.md
READ this workflow file next: .claude/skills/bmad-story-automator-review/workflow.yaml
Then read: .claude/skills/bmad-story-automator-review/instructions.xml
Validate with: .claude/skills/bmad-story-automator-review/checklist.md
Story file: _bmad-output/implementation-artifacts/3-5-*.md
Review implementation, find issues, fix them automatically. auto-fix all issues without prompting

> AGENT

I'll read the skill files and story to execute the review workflow.

> TOOL

tool_use Read
id: toolu_013CnUeBCdmSChg3yP8cTSUX
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/.claude/skills/bmad-story-automator-review/SKILL.md"
}
```

> TOOL

tool_use Read
id: toolu_015G1hn4CHhDGQn1w7dnxRTN
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/.claude/skills/bmad-story-automator-review/workflow.yaml"
}
```

> TOOL

tool_result
id: toolu_013CnUeBCdmSChg3yP8cTSUX
```
1	---
2	name: bmad-story-automator-review
3	description: 'Runs the autonomous code review flow used by story automator sessions, including auto-fix handling and sprint-status sync. Use when the story automator asks for a non-interactive review of a story.'
4	---
5	
6	1. Read `./workflow.yaml`.
7	2. Then read `./instructions.xml`.
8	3. Use `./checklist.md` as the validation checklist.
9	4. Follow the workflow deterministically. If the invocation asks for automatic fixes, apply them without pausing for manual menus.
10	
```

> TOOL

tool_result
id: toolu_015G1hn4CHhDGQn1w7dnxRTN
```
1	# Review Story Workflow
2	author: "BMad"
3	
4	# Critical variables from config
5	config_source: "{project-root}/_bmad/bmm/config.yaml"
6	user_name: "{config_source}:user_name"
7	communication_language: "{config_source}:communication_language"
8	user_skill_level: "{config_source}:user_skill_level"
9	document_output_language: "{config_source}:document_output_language"
10	date: system-generated
11	planning_artifacts: "{config_source}:planning_artifacts"
12	implementation_artifacts: "{config_source}:implementation_artifacts"
13	output_folder: "{implementation_artifacts}"
14	sprint_status: "{implementation_artifacts}/sprint-status.yaml"
15	
16	# Workflow components
17	instructions: "./instructions.xml"
18	validation: "./checklist.md"
19	standalone: true
20	
```

> TOOL

tool_use Read
id: toolu_01UBZmYppuvQjpbiWFh4gKD3
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/.claude/skills/bmad-story-automator-review/instructions.xml"
}
```

> TOOL

tool_result
id: toolu_01UBZmYppuvQjpbiWFh4gKD3
```
1	<workflow>
2	  <critical>You MUST have already loaded and processed: ./workflow.yaml</critical>
3	  <critical>Communicate all responses in {communication_language} and language MUST be tailored to {user_skill_level}</critical>
4	  <critical>Generate all documents in {document_output_language}</critical>
5	
6	  <critical>🔥 YOU ARE AN ADVERSARIAL CODE REVIEWER - Find what's wrong or missing! 🔥</critical>
7	  <critical>Your purpose: Validate story file claims against actual implementation</critical>
8	  <critical>Challenge everything: Are tasks marked [x] actually done? Are ACs really implemented?</critical>
9	  <critical>Find 3-10 specific issues in every review minimum - no lazy "looks good" reviews - YOU are so much better than the dev agent
10	    that wrote this slop</critical>
11	  <critical>Read EVERY file in the File List - verify implementation against story requirements</critical>
12	  <critical>Tasks marked complete but not done = CRITICAL finding</critical>
13	  <critical>Acceptance Criteria not implemented = HIGH severity finding</critical>
14	  <critical>Do not review files that are not part of the application's source code. Always exclude the _bmad/ and _bmad-output/ folders from the review. Always exclude IDE and CLI configuration folders like .cursor/ and .windsurf/, plus non-source runtime configuration outside supported skill roots.</critical>
15	
16	
17	  <step n="1" goal="Load story and discover changes">
18	    <action>Use provided {{story_path}} or ask user which story file to review</action>
19	    <action>Read COMPLETE story file</action>
20	    <action>Set {{story_key}} = extracted key from filename (e.g., "1-2-user-authentication.md" → "1-2-user-authentication") or story
21	      metadata</action>
22	    <action>Parse sections: Story, Acceptance Criteria, Tasks/Subtasks, Dev Agent Record → File List, Change Log</action>
23	
24	    <!-- Discover actual changes via git -->
25	    <action>Check if git repository detected in current directory</action>
26	    <check if="git repository exists">
27	      <action>Run `git status --porcelain` to find uncommitted changes</action>
28	      <action>Run `git diff --name-only` to see modified files</action>
29	      <action>Run `git diff --cached --name-only` to see staged files</action>
30	      <action>Compile list of actually changed files from git output</action>
31	    </check>
32	
33	    <!-- Cross-reference story File List vs git reality -->
34	    <action>Compare story's Dev Agent Record → File List with actual git changes</action>
35	    <action>Note discrepancies:
36	      - Files in git but not in story File List
37	      - Files in story File List but no git changes
38	      - Missing documentation of what was actually changed
39	    </action>
40	
41	    <invoke-protocol name="discover_inputs" />
42	    <action>Load {project_context} for coding standards (if exists)</action>
43	  </step>
44	
45	  <step n="2" goal="Build review attack plan">
46	    <action>Extract ALL Acceptance Criteria from story</action>
47	    <action>Extract ALL Tasks/Subtasks with completion status ([x] vs [ ])</action>
48	    <action>From Dev Agent Record → File List, compile list of claimed changes</action>
49	
50	    <action>Create review plan:
51	      1. **AC Validation**: Verify each AC is actually implemented
52	      2. **Task Audit**: Verify each [x] task is really done
53	      3. **Code Quality**: Security, performance, maintainability
54	      4. **Test Quality**: Real tests vs placeholder bullshit
55	    </action>
56	  </step>
57	
58	  <step n="3" goal="Execute adversarial review">
59	    <critical>VALIDATE EVERY CLAIM - Check git reality vs story claims</critical>
60	
61	    <!-- Git vs Story Discrepancies -->
62	    <action>Review git vs story File List discrepancies:
63	      1. **Files changed but not in story File List** → MEDIUM finding (incomplete documentation)
64	      2. **Story lists files but no git changes** → HIGH finding (false claims)
65	      3. **Uncommitted changes not documented** → MEDIUM finding (transparency issue)
66	    </action>
67	
68	    <!-- Use combined file list: story File List + git discovered files -->
69	    <action>Create comprehensive review file list from story File List and git changes</action>
70	
71	    <!-- AC Validation -->
72	    <action>For EACH Acceptance Criterion:
73	      1. Read the AC requirement
74	      2. Search implementation files for evidence
75	      3. Determine: IMPLEMENTED, PARTIAL, or MISSING
76	      4. If MISSING/PARTIAL → HIGH SEVERITY finding
77	    </action>
78	
79	    <!-- Task Completion Audit -->
80	    <action>For EACH task marked [x]:
81	      1. Read the task description
82	      2. Search files for evidence it was actually done
83	      3. **CRITICAL**: If marked [x] but NOT DONE → CRITICAL finding
84	      4. Record specific proof (file:line)
85	    </action>
86	
87	    <!-- Code Quality Deep Dive -->
88	    <action>For EACH file in comprehensive review list:
89	      1. **Security**: Look for injection risks, missing validation, auth issues
90	      2. **Performance**: N+1 queries, inefficient loops, missing caching
91	      3. **Error Handling**: Missing try/catch, poor error messages
92	      4. **Code Quality**: Complex functions, magic numbers, poor naming
93	      5. **Test Quality**: Are tests real assertions or placeholders?
94	    </action>
95	
96	    <check if="total_issues_found lt 3">
97	      <action>Re-examine the review surface for missed issues, but report only verified findings.</action>
98	      <action>If no additional issues are found, continue with the smaller confirmed set.</action>
99	    </check>
100	  </step>
101	
102	  <step n="4" goal="Present findings and fix them">
103	    <action>Categorize findings: HIGH (must fix), MEDIUM (should fix), LOW (nice to fix)</action>
104	    <action>Set {{fixed_count}} = 0</action>
105	    <action>Set {{action_count}} = 0</action>
106	
107	    <output>**🔥 CODE REVIEW FINDINGS, {user_name}!**
108	
109	      **Story:** {{story_file}}
110	      **Git vs Story Discrepancies:** {{git_discrepancy_count}} found
111	      **Issues Found:** {{high_count}} High, {{medium_count}} Medium, {{low_count}} Low
112	
113	      ## 🔴 CRITICAL ISSUES
114	      - Tasks marked [x] but not actually implemented
115	      - Acceptance Criteria not implemented
116	      - Story claims files changed but no git evidence
117	      - Security vulnerabilities
118	
119	      ## 🟡 MEDIUM ISSUES
120	      - Files changed but not documented in story File List
121	      - Uncommitted changes not tracked
122	      - Performance problems
123	      - Poor test coverage/quality
124	      - Code maintainability issues
125	
126	      ## 🟢 LOW ISSUES
127	      - Code style improvements
128	      - Documentation gaps
129	      - Git commit message quality
130	    </output>
131	
132	    <ask>What should I do with these issues?
133	
134	      1. **Fix them automatically** - I'll update the code and tests
135	      2. **Create action items** - Add to story Tasks/Subtasks for later
136	      3. **Show me details** - Deep dive into specific issues
137	
138	      Choose [1], [2], or specify which issue to examine:</ask>
139	
140	    <check if="user chooses 1">
141	      <action>Fix all HIGH and MEDIUM issues in the code</action>
142	      <action>Add/update tests as needed</action>
143	      <action>Update File List in story if files changed</action>
144	      <action>Update story Dev Agent Record with fixes applied</action>
145	      <action>Set {{fixed_count}} = number of HIGH and MEDIUM issues fixed</action>
146	      <action>Set {{action_count}} = 0</action>
147	    </check>
148	
149	    <check if="user chooses 2">
150	      <action>Add "Review Follow-ups (AI)" subsection to Tasks/Subtasks</action>
151	      <action>For each issue: `- [ ] [AI-Review][Severity] Description [file:line]`</action>
152	      <action>Set {{action_count}} = number of action items created</action>
153	      <action>Set {{fixed_count}} = 0</action>
154	    </check>
155	
156	    <check if="user chooses 3">
157	      <action>Show detailed explanation with code examples</action>
158	      <action>Return to fix decision</action>
159	    </check>
160	  </step>
161	
162	  <step n="5" goal="Update story status and sync sprint tracking">
163	    <!-- Determine new status based on CRITICAL issues only (v3.0) -->
164	    <!-- HIGH/MEDIUM/LOW are tracked as action items but don't block automation -->
165	    <check if="0 CRITICAL issues remain after fixes">
166	      <action>Set {{new_status}} = "done"</action>
167	      <action>Update story Status field to "done"</action>
168	    </check>
169	    <check if="1+ CRITICAL issues remain after fixes">
170	      <action>Set {{new_status}} = "in-progress"</action>
171	      <action>Update story Status field to "in-progress"</action>
172	    </check>
173	    <action>Save story file</action>
174	
175	    <!-- Determine sprint tracking status -->
176	    <check if="{sprint_status} file exists">
177	      <action>Set {{current_sprint_status}} = "enabled"</action>
178	    </check>
179	    <check if="{sprint_status} file does NOT exist">
180	      <action>Set {{current_sprint_status}} = "no-sprint-tracking"</action>
181	    </check>
182	
183	    <!-- Sync sprint-status.yaml when story status changes (only if sprint tracking enabled) -->
184	    <check if="{{current_sprint_status}} != 'no-sprint-tracking'">
185	      <action>Load the FULL file: {sprint_status}</action>
186	      <action>Find development_status key matching {{story_key}}</action>
187	
188	      <check if="{{new_status}} == 'done'">
189	        <action>Update development_status[{{story_key}}] = "done"</action>
190	        <action>Save file, preserving ALL comments and structure</action>
191	        <output>✅ Sprint status synced: {{story_key}} → done</output>
192	      </check>
193	
194	      <check if="{{new_status}} == 'in-progress'">
195	        <action>Update development_status[{{story_key}}] = "in-progress"</action>
196	        <action>Save file, preserving ALL comments and structure</action>
197	        <output>🔄 Sprint status synced: {{story_key}} → in-progress</output>
198	      </check>
199	
200	      <check if="story key not found in sprint status">
201	        <output>⚠️ Story file updated, but sprint-status sync failed: {{story_key}} not found in sprint-status.yaml</output>
202	      </check>
203	    </check>
204	
205	    <check if="{{current_sprint_status}} == 'no-sprint-tracking'">
206	      <output>ℹ️ Story status updated (no sprint tracking configured)</output>
207	    </check>
208	
209	    <output>**✅ Review Complete!**
210	
211	      **Story Status:** {{new_status}}
212	      **Issues Fixed:** {{fixed_count}}
213	      **Action Items Created:** {{action_count}}
214	
215	      {{#if new_status == "done"}}Code review complete!{{else}}Address the action items and continue development.{{/if}}
216	    </output>
217	  </step>
218	
219	</workflow>
220	
```

> TOOL

tool_use Read
id: toolu_012mWv2FKh27xiXERr5mDHnU
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/.claude/skills/bmad-story-automator-review/checklist.md"
}
```

> TOOL

tool_result
id: toolu_012mWv2FKh27xiXERr5mDHnU
```
1	# Senior Developer Review - Validation Checklist
2	
3	- [ ] Story file loaded from `{{story_path}}`
4	- [ ] Story Status verified as reviewable (review)
5	- [ ] Epic and Story IDs resolved ({{epic_num}}.{{story_num}})
6	- [ ] Story Context located or warning recorded
7	- [ ] Epic Tech Spec located or warning recorded
8	- [ ] Architecture/standards docs loaded (as available)
9	- [ ] Tech stack detected and documented
10	- [ ] MCP doc search performed (or web fallback) and references captured
11	- [ ] Acceptance Criteria cross-checked against implementation
12	- [ ] File List reviewed and validated for completeness
13	- [ ] Tests identified and mapped to ACs; gaps noted
14	- [ ] Code quality review performed on changed files
15	- [ ] Security review performed on changed files and dependencies
16	- [ ] Outcome decided (Approve/Changes Requested/Blocked)
17	- [ ] Review notes appended under "Senior Developer Review (AI)"
18	- [ ] Change Log updated with review entry
19	- [ ] Status updated according to settings (if enabled)
20	- [ ] Sprint status synced (if sprint tracking enabled)
21	- [ ] Story saved successfully
22	
23	_Reviewer: {{user_name}} on {{date}}_
24	
```

> AGENT

Now let me load the config and story file.

> TOOL

tool_use Bash
id: toolu_01XdDaJjuShUYq8A8MpGYhky
```json
{
  "command": "ls /home/armel/Projects/OSS/bmad-module-skill-forge/_bmad-output/implementation-artifacts/3-5-*.md 2>/dev/null",
  "description": "Find story 3.5 file"
}
```

> TOOL

tool_use Read
id: toolu_01VXR5yoxSdwuyGrn1WxqH6P
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/_bmad/bmm/config.yaml"
}
```

> TOOL

tool_result
id: toolu_01VXR5yoxSdwuyGrn1WxqH6P
```
1	# BMM Module Configuration
2	# Generated by BMAD installer
3	# Version: 6.8.0
4	# Date: 2026-05-26T07:36:41.396Z
5	
6	user_skill_level: intermediate
7	planning_artifacts: "{project-root}/_bmad-output/planning-artifacts"
8	implementation_artifacts: "{project-root}/_bmad-output/implementation-artifacts"
9	project_knowledge: "{project-root}/docs"
10	
11	# Core Configuration Values
12	user_name: Armel
13	project_name: bmad-module-skill-forge
14	communication_language: English
15	document_output_language: English
16	output_folder: "{project-root}/_bmad-output"
17	
```

> TOOL

tool_result
id: toolu_01XdDaJjuShUYq8A8MpGYhky
```
/home/armel/Projects/OSS/bmad-module-skill-forge/_bmad-output/implementation-artifacts/3-5-pre-apply-workaround-registry.md
```

> TOOL

tool_use Read
id: toolu_01Gh6584zZDapMAQtEx5XXm3
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/_bmad-output/implementation-artifacts/3-5-pre-apply-workaround-registry.md"
}
```

> TOOL

tool_result
id: toolu_01Gh6584zZDapMAQtEx5XXm3
```
1	---
2	baseline_commit: ab25d834aed60cad70bead87fb0fc37286a46675
3	---
4	
5	# Story 3.5: Pre-Apply Workaround Registry
6	
7	Status: review
8	
9	## Story
10	
11	As a pipeline operator,
12	I want known workarounds to be automatically applied before each pipeline iteration,
13	So that previously-solved issues are not re-discovered and manually fixed each time.
14	
15	## Acceptance Criteria
16	
17	1. **Given** a `_known-workarounds.yaml` registry with a fingerprint matching content in the target directory
18	   **When** `skf-preapply.py --target-dir <path>` runs
19	   **Then** the matching fix is applied to the target content
20	   **And** the applied fix is logged to `forge-data/{skill-name}/{version}/preapply-log.json`
21	
22	2. **Given** a registry with no fingerprints matching the target content
23	   **When** `skf-preapply.py` runs
24	   **Then** no fixes are applied and the log records zero matches
25	
26	3. **Given** both a shared seed registry and a project-local registry with a colliding fingerprint
27	   **When** `skf-preapply.py --target-dir <path> --local-registry <path>` runs
28	   **Then** the project-local fix wins on collision
29	   **And** the shared seed is loaded first, project-local merged on top
30	
31	4. **Given** a new workaround discovered during a pipeline run
32	   **When** it is recorded
33	   **Then** it is appended to the project-local registry only, never to the shared seed
34	
35	5. **Given** a fingerprint entry with `regex: true`
36	   **When** matching is performed
37	   **Then** regex matching is used instead of the default substring matching
38	
39	## Tasks / Subtasks
40	
41	- [x] Task 1: Create the `_known-workarounds.yaml` shared seed registry (AC: #1, #3, #4)
42	  - [x] 1.1 Create `src/shared/_known-workarounds.yaml` with `version: 1` header and `workarounds:` array
43	  - [x] 1.2 Populate with 25 GMC campaign fingerprint-to-fix pairs following the schema: `{fingerprint, fix, source, severity, description}` per entry
44	  - [x] 1.3 Include entries spanning severity levels (low, medium, high) with a mix of substring and regex fingerprints
45	  - [x] 1.4 Add `regex: true` flag on entries that require regex matching (default is substring)
46	
47	- [x] Task 2: Create `skf-preapply.py` shared script (AC: #1, #2, #3, #5)
48	  - [x] 2.1 Create `src/shared/scripts/skf-preapply.py` with PEP 723 header (`requires-python = ">=3.9"`, `dependencies = ["pyyaml"]`)
49	  - [x] 2.2 Implement argparse CLI: `--target-dir <path>` (required), `--registry <path>` (optional, defaults to `src/shared/_known-workarounds.yaml`), `--local-registry <path>` (optional)
50	  - [x] 2.3 Implement registry loading: load shared seed first, then project-local; merge on fingerprint key with local winning on collision
51	  - [x] 2.4 Implement fingerprint matching: iterate target directory files, for each workaround entry check content via substring match (default) or regex match (`regex: true`)
52	  - [x] 2.5 Implement fix application: when a fingerprint matches, apply the fix to the matching content
53	  - [x] 2.6 Implement JSON stdout output: `{applied: [{fingerprint, fix, file, severity}], skipped_count: N, registry_version: 1}`
54	  - [x] 2.7 Implement exit codes: `0` = success (applied ≥ 0 fixes without errors), `2` = error (invalid args, missing registry, YAML parse error)
55	  - [x] 2.8 Implement stderr error output: `{"error": "message", "code": "ERROR_TYPE"}` on exit 2
56	  - [x] 2.9 Implement preapply-log.json writing: write to `forge-data/{skill-name}/{version}/preapply-log.json` if `--log-dir` is provided (or derive from target-dir context)
57	
58	- [x] Task 3: Create structural integration tests (AC: #1, #2, #3, #5)
59	  - [x] 3.1 Create `test/test-skf-preapply.py` following the pattern from `test/test-skf-detect-docs.py` (importlib dynamic loading + subprocess CLI tests)
60	  - [x] 3.2 Test: `_known-workarounds.yaml` exists at `src/shared/_known-workarounds.yaml`
61	  - [x] 3.3 Test: registry has `version: 1` header
62	  - [x] 3.4 Test: registry has `workarounds` array with ≥ 25 entries
63	  - [x] 3.5 Test: each entry has required fields: `fingerprint`, `fix`, `source`, `severity`, `description`
64	  - [x] 3.6 Test: `severity` values are in `{low, medium, high}`
65	  - [x] 3.7 Test: at least one entry has `regex: true`
66	  - [x] 3.8 Test: `skf-preapply.py` exists at expected path
67	  - [x] 3.9 Test: `skf-preapply.py` has PEP 723 header with `pyyaml` dependency
68	  - [x] 3.10 Test: CLI accepts `--target-dir`, `--registry`, `--local-registry` args
69	  - [x] 3.11 Test: JSON stdout schema matches `{applied, skipped_count, registry_version}`
70	  - [x] 3.12 Test: exit code 0 on valid invocation (with temp directory target)
71	  - [x] 3.13 Test: exit code 2 on missing target-dir or invalid registry
72	  - [x] 3.14 Test: substring matching applies fix to matching content
73	  - [x] 3.15 Test: regex matching applies fix when `regex: true`
74	  - [x] 3.16 Test: local registry overrides shared seed on fingerprint collision
75	  - [x] 3.17 Test: no modifications to target files when no fingerprints match
76	  - [x] 3.18 Register `test/test-skf-preapply.py` in `package.json` test:python command
77	
78	## Dev Notes
79	
80	### Script Interface (from Architecture)
81	
82	```
83	skf-preapply.py
84	Args: --target-dir <path> [--registry <path>] [--local-registry <path>]
85	Stdout: JSON {applied[], skipped_count, registry_version}
86	Exit: 0 (success), 2 (error)
87	```
88	
89	Note: exit code is `0` for both "applied fixes" and "zero matches" — both are successful runs. Exit `1` is NOT used by this script (unlike detect-docs where `1` = "none found"). The architecture specifies only exit `0` and `2` for preapply.
90	
91	### Registry Schema (from Architecture)
92	
93	```yaml
94	version: 1
95	workarounds:
96	  - fingerprint: string     # pattern to match in target content
97	    fix: string             # correction text or instruction
98	    source: string          # where the workaround was discovered
99	    severity: low|medium|high
100	    description: string     # one-line human summary
101	    regex: true             # optional — use regex matching instead of substring
102	```
103	
104	### Merge Strategy
105	
106	1. Load shared seed registry (`src/shared/_known-workarounds.yaml` or `--registry` path)
107	2. Load project-local registry (`--local-registry` path, if provided)
108	3. Merge: iterate project-local entries; on fingerprint collision (same `fingerprint` string), local entry replaces shared entry
109	4. Merged registry is ephemeral — never persisted as a combined file
110	
111	**Anti-pattern (from Architecture):** Modifying the shared seed file during a pipeline run. The shared seed is an SKF source file — only maintainer PRs change it.
112	
113	### Fingerprint Matching
114	
115	- Default: substring match — `fingerprint` string is searched within each target file's content
116	- Regex opt-in: when entry has `regex: true`, `fingerprint` is compiled as a Python `re` pattern
117	- Match target: all `.md` files within `--target-dir` (step files, SKILL.md, reference docs)
118	- Files are read with `encoding="utf-8"` (cross-platform safety per PR #311/#316/#366/#368/#387)
119	
120	### Fix Application
121	
122	When a fingerprint matches:
123	1. Apply the `fix` as a replacement for the matched content
124	2. Log the application to the `applied` array in stdout JSON
125	3. If `--log-dir` is provided, write detailed log to `preapply-log.json` at that path
126	
127	### Consumers of Pre-Apply
128	
129	- **All pipeline runs:** Pre-apply runs before each pipeline iteration (shared module)
130	- **Campaign step-05 (skill-loop):** Per-skill pre-apply → kickoff → AN → BS → CS → TS
131	- **Standalone invocation:** `uv run python src/shared/scripts/skf-preapply.py --target-dir <path>`
132	
133	### Shared Script Conventions (from Architecture + Stories 3.1–3.4)
134	
135	1. **PEP 723 header:** `requires-python = ">=3.9"`, `dependencies = ["pyyaml"]`
136	2. **Module docstring:** describe CLI, input/output, exit codes
137	3. **argparse:** GNU-style long flags, kebab-case (`--target-dir`, not `--target_dir`)
138	4. **JSON stdout:** one object, no pretty-print in non-interactive mode
139	5. **Errors:** JSON `{"error": "message", "code": "ERROR_TYPE"}` to stderr on exit 2
140	6. **No global state, no env var dependencies** beyond what uv provides
141	7. **Invocation:** `uv run python src/shared/scripts/skf-preapply.py --target-dir <path>`
142	8. **Paths:** Use `Path.as_posix()` in assertions, not `str()` — cross-platform safety
143	9. **File reads:** Always `encoding="utf-8"` — avoid cp1252 mojibake on Windows
144	10. **File writes:** Use `os.open` with `O_BINARY` flag for byte-exact writes if needed
145	
146	### What the GMC Seed Fingerprints Cover
147	
148	The 25 GMC campaign fingerprints capture recurring workarounds discovered during batch skill-forging campaigns. They address common issues like:
149	- Hallucinated API endpoints or function signatures in compiled skills
150	- Stale version references carried from outdated documentation
151	- Inconsistent heading structures that fail skill-check validation
152	- Missing provenance markers (T1 annotations, confidence tiers)
153	- Repeated citation format errors
154	- Common markdown lint violations in generated content
155	- Section ordering violations against the skill-sections spec
156	- Broken cross-reference links to non-existent reference files
157	
158	Each fingerprint is a stable textual pattern that recurs across multiple skill compilations. The fix is the deterministic correction.
159	
160	### Project Structure Notes
161	
162	New files:
163	- `src/shared/scripts/skf-preapply.py` — the pre-apply shared script
164	- `src/shared/_known-workarounds.yaml` — shared seed registry (25 GMC fingerprints)
165	- `test/test-skf-preapply.py` — structural integration tests
166	
167	Modified files:
168	- `package.json` — add `test/test-skf-preapply.py` to `test:python` command
169	
170	No existing step files or workflows are modified — this story creates the standalone shared module. Integration into pipeline flows (calling pre-apply before each iteration) will happen at the pipeline level in downstream stories or campaign (Story 4.6).
171	
172	### Story 3.4 Learnings (Apply These)
173	
174	1. **Register test file in package.json:** The `test:python` command enumerates every test path — adding `test/test-skf-preapply.py` without updating it leaves the test dormant in CI
175	2. **Self-audit for internal references:** Do NOT include internal story IDs, epic numbers, or bmad keywords in the script content, registry comments, or commit messages
176	3. **Cross-platform path assertions:** Use `Path.as_posix()` not `str()` in test assertions; read with `encoding="utf-8"`; windows-latest CI is the gatekeeper
177	4. **Structural test pattern:** Follow `test-skf-evidence-report-fallback.py` for structural tests (pathlib-based, file existence, content regex matching) and `test-skf-detect-docs.py` for functional tests (importlib dynamic loading, subprocess CLI verification)
178	
179	### Story 3.1 Learnings (Apply These)
180	
181	1. **Report.md stepsCompleted chain:** Not applicable to this story — pre-apply is a shared script, not a step in a workflow chain
182	2. **Stages table alignment:** Not applicable — no new step file in any workflow's Stages table
183	
184	### What Must NOT Change
185	
186	- Existing shared scripts — pre-apply is a new script, no modifications to existing ones
187	- The shared seed registry (`src/shared/_known-workarounds.yaml`) must never be modified at runtime
188	- `forge-data/` structure — pre-apply writes logs there but does not modify the directory layout
189	
190	### References
191	
192	- [Source: _bmad-output/planning-artifacts/epics.md — Story 3.5 "Pre-apply workaround registry"]
193	- [Source: _bmad-output/planning-artifacts/architecture.md — "Shared Module Interfaces" section: skf-preapply.py interface]
194	- [Source: _bmad-output/planning-artifacts/architecture.md — "Pre-Apply Registry Patterns" section: merge strategy, fingerprint matching, fix logging]
195	- [Source: _bmad-output/planning-artifacts/architecture.md — "Project Structure & Boundaries" section: src/shared/_known-workarounds.yaml, forge-data/ runtime artifacts]
196	- [Source: _bmad-output/planning-artifacts/architecture.md — "Shared Script Patterns" section: naming, args, output, exit codes]
197	- [Source: _bmad-output/planning-artifacts/architecture.md — "Seed ↔ Project-local boundary" section: read-only seed, append-only local, ephemeral merge]
198	- [Source: _bmad-output/implementation-artifacts/3-4-auto-shard-at-400-line-ceiling.md — Story 3.4 learnings: package.json registration, cross-platform paths]
199	
200	## Dev Agent Record
201	
202	### Agent Model Used
203	
204	Claude Opus 4.7 (1M context)
205	
206	### Debug Log References
207	
208	### Completion Notes List
209	
210	- Created shared seed registry with 25 GMC campaign fingerprint-to-fix pairs spanning low/medium/high severity, including 4 regex-enabled entries
211	- Implemented skf-preapply.py with PEP 723 header, argparse CLI (--target-dir, --registry, --local-registry, --log-dir), registry merge logic (local wins on collision), substring + regex fingerprint matching, JSON stdout output, structured stderr errors, and optional preapply-log.json writing
212	- Created 25 tests covering registry structure, script PEP 723 compliance, CLI args, output schema, exit codes (0 and 2), substring matching, regex matching, local-override merge, and no-match passthrough
213	- Registered test/test-skf-preapply.py in package.json test:python command
214	
215	### Change Log
216	
217	- 2026-05-27: Implemented pre-apply workaround registry — shared seed with 25 fingerprints, skf-preapply.py script, and 25 structural/functional tests
218	
219	### File List
220	
221	- src/shared/_known-workarounds.yaml (new)
222	- src/shared/scripts/skf-preapply.py (new)
223	- test/test-skf-preapply.py (new)
224	- package.json (modified — added test/test-skf-preapply.py to test:python)
225	
```

> AGENT

Story loaded. Now discovering git changes and reading all implementation files.

> TOOL

tool_use Bash
id: toolu_01NsgU8ppijcwNndrUsTYBRu
```json
{
  "command": "git status --porcelain",
  "description": "Show git status for story 3.5 changes"
}
```

> TOOL

tool_result
id: toolu_01NsgU8ppijcwNndrUsTYBRu
```
 M package.json
?? src/shared/_known-workarounds.yaml
?? src/shared/scripts/skf-preapply.py
?? test/test-skf-preapply.py
```

> TOOL

tool_use Bash
id: toolu_01HTzQXCXeLdrEfhX4mQXuJS
```json
{
  "command": "git diff --name-only",
  "description": "Show modified files"
}
```

> TOOL

tool_use Bash
id: toolu_01UeCYiMKwC7BAYfcXjHdhLT
```json
{
  "command": "git diff --cached --name-only",
  "description": "Show staged files"
}
```

> TOOL

tool_result
id: toolu_01HTzQXCXeLdrEfhX4mQXuJS
```
package.json
```

> TOOL

tool_result
id: toolu_01UeCYiMKwC7BAYfcXjHdhLT
```
(Bash completed with no output)
```

> AGENT

Git matches story File List — no discrepancies. Now reading all implementation files.

> TOOL

tool_use Read
id: toolu_0151ZMWqhYGwkhBwawMdESAU
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/shared/_known-workarounds.yaml"
}
```

> TOOL

tool_result
id: toolu_0151ZMWqhYGwkhBwawMdESAU
```
1	version: 1
2	workarounds:
3	  - fingerprint: "```api\nGET /api/v1/skills/compile"
4	    fix: "```\nskf compile --target <skill-dir>"
5	    source: gmc-batch-2024-q4
6	    severity: high
7	    description: Hallucinated REST API endpoint replaced with correct CLI invocation
8	
9	  - fingerprint: 'requires-python = ">=3.8"'
10	    fix: 'requires-python = ">=3.9"'
11	    source: gmc-batch-2024-q4
12	    severity: medium
13	    description: Stale Python 3.8 minimum version updated to 3.9 baseline
14	
15	  - fingerprint: "## outputs\n\n## steps"
16	    fix: "## Outputs\n\n## Steps"
17	    source: gmc-batch-2025-q1
18	    severity: high
19	    description: Lowercase heading violates skill-sections spec capitalization rules
20	
21	  - fingerprint: "confidence: unverified"
22	    fix: "confidence: T1-inferred"
23	    source: gmc-batch-2025-q1
24	    severity: medium
25	    description: Missing provenance tier replaced with correct T1 annotation
26	
27	  - fingerprint: "[source: unknown]"
28	    fix: "[source: repo-readme]"
29	    source: gmc-batch-2024-q4
30	    severity: low
31	    description: Placeholder source attribution replaced with actual provenance
32	
33	  - fingerprint: "See [API Reference](./api-reference.md)"
34	    fix: "See the API reference in the repository documentation."
35	    source: gmc-batch-2025-q1
36	    severity: high
37	    description: Broken cross-reference to non-existent api-reference.md file
38	
39	  - fingerprint: "## Steps\n## Outputs"
40	    fix: "## Steps\n\n## Outputs"
41	    source: gmc-batch-2024-q4
42	    severity: low
43	    description: Missing blank line between heading sections fails markdown lint
44	
45	  - fingerprint: "(v1.0.0+)"
46	    fix: ""
47	    source: gmc-batch-2025-q1
48	    severity: low
49	    description: Inline version stamp removed per documentation conventions
50	
51	  - fingerprint: "tier: gold"
52	    fix: "tier: verified"
53	    source: gmc-batch-2024-q4
54	    severity: medium
55	    description: Non-standard tier label replaced with canonical tier vocabulary
56	
57	  - fingerprint: "```javascript\nfetch('/api/skill"
58	    fix: "```bash\nskf"
59	    source: gmc-batch-2025-q1
60	    severity: high
61	    description: Hallucinated JavaScript fetch call replaced with CLI command
62	
63	  - fingerprint: "## References\n## Steps"
64	    fix: "## Steps"
65	    source: gmc-batch-2024-q4
66	    severity: high
67	    description: References section misplaced before Steps violates section ordering
68	
69	  - fingerprint: "source: (generated)"
70	    fix: "source: compilation-output"
71	    source: gmc-batch-2025-q1
72	    severity: low
73	    description: Vague generated marker replaced with specific compilation-output source
74	
75	  - fingerprint: "# Skill Name\n# Overview"
76	    fix: "# Skill Name\n\n## Overview"
77	    source: gmc-batch-2024-q4
78	    severity: high
79	    description: Duplicate H1 heading replaced with correct H2 for Overview section
80	
81	  - fingerprint: "[ref: SKILL-SPEC-2.0](./spec.md)"
82	    fix: "See the skill specification."
83	    source: gmc-batch-2025-q1
84	    severity: medium
85	    description: Broken spec reference link to non-existent file
86	
87	  - fingerprint: "version: 0.9-draft"
88	    fix: "version: 1"
89	    source: gmc-batch-2024-q4
90	    severity: medium
91	    description: Draft version string replaced with release version
92	
93	  - fingerprint: "\\bconfidence:\\s*(?:none|n/a|unset)\\b"
94	    fix: "confidence: T1-inferred"
95	    source: gmc-batch-2025-q1
96	    severity: medium
97	    description: Empty or null confidence values normalized to T1-inferred
98	    regex: true
99	
100	  - fingerprint: "  - tool: compile-skill\n    endpoint: /compile"
101	    fix: "  - tool: skf-compile\n    invocation: CLI"
102	    source: gmc-batch-2024-q4
103	    severity: high
104	    description: Hallucinated tool entry with REST endpoint replaced with correct CLI tool
105	
106	  - fingerprint: "## setup\n"
107	    fix: "## Setup\n"
108	    source: gmc-batch-2025-q1
109	    severity: low
110	    description: Lowercase Setup heading fails skill-check validation
111	
112	  - fingerprint: "\\[citation needed\\]"
113	    fix: ""
114	    source: gmc-batch-2024-q4
115	    severity: low
116	    description: Wikipedia-style citation placeholder removed from compiled output
117	    regex: true
118	
119	  - fingerprint: "Last updated: 2023"
120	    fix: ""
121	    source: gmc-batch-2025-q1
122	    severity: low
123	    description: Stale 2023 date stamp removed from compiled skill content
124	
125	  - fingerprint: "## Inputs\n## inputs"
126	    fix: "## Inputs"
127	    source: gmc-batch-2024-q4
128	    severity: medium
129	    description: Duplicate Inputs section with inconsistent casing collapsed
130	
131	  - fingerprint: "\\bsee also:\\s*\\[.*\\]\\(https?://internal\\..*\\)"
132	    fix: ""
133	    source: gmc-batch-2025-q1
134	    severity: high
135	    description: Internal-only URL references removed from public skill output
136	    regex: true
137	
138	  - fingerprint: "provenance: []\n"
139	    fix: "provenance:\n  - source: compilation-output\n    confidence: T1-inferred\n"
140	    source: gmc-batch-2024-q4
141	    severity: medium
142	    description: Empty provenance array populated with minimal compilation metadata
143	
144	  - fingerprint: "## Steps\n\n\n\n## Outputs"
145	    fix: "## Steps\n\n## Outputs"
146	    source: gmc-batch-2025-q1
147	    severity: low
148	    description: Excessive blank lines between sections reduced to standard single blank
149	
150	  - fingerprint: "\\|\\s*Step\\s*\\|\\s*Status\\s*\\|\\n\\|[-\\s|]+\\|\\n(?=\\|\\s*Step)"
151	    fix: ""
152	    source: gmc-batch-2024-q4
153	    severity: medium
154	    description: Duplicated markdown table header removed from compiled output
155	    regex: true
156	
```

> TOOL

tool_use Read
id: toolu_01KEZe9ex3JBQvtH7toHK2CW
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/shared/scripts/skf-preapply.py"
}
```

> TOOL

tool_result
id: toolu_01KEZe9ex3JBQvtH7toHK2CW
```
1	# /// script
2	# requires-python = ">=3.9"
3	# dependencies = ["pyyaml"]
4	# ///
5	"""SKF Pre-Apply — apply known workarounds before pipeline iteration.
6	
7	Loads a shared seed registry of known workarounds and optionally a project-local
8	registry, then scans target directory files for fingerprint matches and applies
9	the corresponding fixes.
10	
11	CLI:
12	  uv run python src/shared/scripts/skf-preapply.py \
13	      --target-dir <path> [--registry <path>] [--local-registry <path>] [--log-dir <path>]
14	
15	Input:
16	  --target-dir       directory to scan for fingerprint matches (required)
17	  --registry         path to shared seed registry YAML (optional, defaults to
18	                     src/shared/_known-workarounds.yaml relative to script)
19	  --local-registry   path to project-local override registry YAML (optional)
20	  --log-dir          directory to write preapply-log.json (optional)
21	
22	Output (JSON on stdout):
23	  {
24	    "applied": [{"fingerprint": "...", "fix": "...", "file": "...", "severity": "..."}],
25	    "skipped_count": 0,
26	    "registry_version": 1
27	  }
28	
29	Exit codes:
30	  0  success (applied >= 0 fixes without errors)
31	  2  error (invalid args, missing registry, YAML parse error)
32	"""
33	
34	from __future__ import annotations
35	
36	import argparse
37	import json
38	import os
39	import re
40	import sys
41	from pathlib import Path
42	from typing import Any, Dict, List
43	
44	import yaml
45	
46	
47	def _err(message: str, code: str) -> None:
48	    json.dump({"error": message, "code": code}, sys.stderr)
49	    sys.stderr.write("\n")
50	    sys.exit(2)
51	
52	
53	def _load_registry(path: Path) -> Dict[str, Any]:
54	    if not path.is_file():
55	        _err(f"Registry not found: {path}", "REGISTRY_NOT_FOUND")
56	    try:
57	        text = path.read_text(encoding="utf-8")
58	        data = yaml.safe_load(text)
59	    except yaml.YAMLError as exc:
60	        _err(f"YAML parse error in {path}: {exc}", "YAML_PARSE_ERROR")
61	    if not isinstance(data, dict) or "workarounds" not in data:
62	        _err(f"Invalid registry format in {path}", "INVALID_REGISTRY")
63	    return data
64	
65	
66	def _merge_registries(
67	    shared: Dict[str, Any], local: Dict[str, Any] | None
68	) -> tuple[List[Dict[str, Any]], int]:
69	    version = shared.get("version", 1)
70	    by_fp: Dict[str, Dict[str, Any]] = {}
71	    for entry in shared.get("workarounds", []):
72	        by_fp[entry["fingerprint"]] = entry
73	    if local is not None:
74	        for entry in local.get("workarounds", []):
75	            by_fp[entry["fingerprint"]] = entry
76	    return list(by_fp.values()), version
77	
78	
79	def _match_and_apply(
80	    workarounds: List[Dict[str, Any]], target_dir: Path
81	) -> tuple[List[Dict[str, Any]], int]:
82	    applied: List[Dict[str, Any]] = []
83	    skipped = 0
84	
85	    md_files = sorted(target_dir.rglob("*.md"))
86	
87	    for wa in workarounds:
88	        fp = wa["fingerprint"]
89	        fix = wa["fix"]
90	        use_regex = wa.get("regex", False)
91	        matched = False
92	
93	        for md_file in md_files:
94	            content = md_file.read_text(encoding="utf-8")
95	            if use_regex:
96	                pattern = re.compile(fp)
97	                if pattern.search(content):
98	                    new_content = pattern.sub(fix, content)
99	                    md_file.write_text(new_content, encoding="utf-8")
100	                    applied.append({
101	                        "fingerprint": fp,
102	                        "fix": fix,
103	                        "file": md_file.relative_to(target_dir).as_posix(),
104	                        "severity": wa.get("severity", "low"),
105	                    })
106	                    matched = True
107	            else:
108	                if fp in content:
109	                    new_content = content.replace(fp, fix)
110	                    md_file.write_text(new_content, encoding="utf-8")
111	                    applied.append({
112	                        "fingerprint": fp,
113	                        "fix": fix,
114	                        "file": md_file.relative_to(target_dir).as_posix(),
115	                        "severity": wa.get("severity", "low"),
116	                    })
117	                    matched = True
118	
119	        if not matched:
120	            skipped += 1
121	
122	    return applied, skipped
123	
124	
125	def main(argv: List[str] | None = None) -> None:
126	    parser = argparse.ArgumentParser(
127	        description="Apply known workarounds before pipeline iteration."
128	    )
129	    parser.add_argument(
130	        "--target-dir", required=True, type=Path,
131	        help="Directory to scan for fingerprint matches",
132	    )
133	    default_registry = (
134	        Path(__file__).resolve().parent.parent / "_known-workarounds.yaml"
135	    )
136	    parser.add_argument(
137	        "--registry", type=Path, default=default_registry,
138	        help="Path to shared seed registry YAML",
139	    )
140	    parser.add_argument(
141	        "--local-registry", type=Path, default=None,
142	        help="Path to project-local override registry YAML",
143	    )
144	    parser.add_argument(
145	        "--log-dir", type=Path, default=None,
146	        help="Directory to write preapply-log.json",
147	    )
148	
149	    args = parser.parse_args(argv)
150	
151	    if not args.target_dir.is_dir():
152	        _err(
153	            f"Target directory not found: {args.target_dir}",
154	            "TARGET_NOT_FOUND",
155	        )
156	
157	    shared = _load_registry(args.registry)
158	
159	    local = None
160	    if args.local_registry is not None:
161	        local = _load_registry(args.local_registry)
162	
163	    workarounds, version = _merge_registries(shared, local)
164	    applied, skipped = _match_and_apply(workarounds, args.target_dir)
165	
166	    result = {
167	        "applied": applied,
168	        "skipped_count": skipped,
169	        "registry_version": version,
170	    }
171	
172	    json.dump(result, sys.stdout)
173	    sys.stdout.write("\n")
174	
175	    if args.log_dir is not None:
176	        args.log_dir.mkdir(parents=True, exist_ok=True)
177	        log_path = args.log_dir / "preapply-log.json"
178	        with open(
179	            log_path, "w", encoding="utf-8", newline="\n"
180	        ) as f:
181	            json.dump(result, f, indent=2)
182	            f.write("\n")
183	
184	
185	if __name__ == "__main__":
186	    main()
187	
```

> TOOL

tool_use Read
id: toolu_01545XiXHCdrybP3iEFdh8o9
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/test/test-skf-preapply.py"
}
```

> TOOL

tool_use Bash
id: toolu_01Hbr6wXkKFFQzzqcSEZhvZu
```json
{
  "command": "git diff package.json",
  "description": "Show package.json changes"
}
```

> TOOL

tool_result
id: toolu_01Hbr6wXkKFFQzzqcSEZhvZu
```
diff --git a/package.json b/package.json
index 08a1972f..dabddec5 100644
--- a/package.json
+++ b/package.json
@@ -53,7 +53,7 @@
     "test:cli": "node test/test-cli-integration.js",
     "test:install": "node test/test-installation-components.js",
     "test:knowledge": "node test/test-knowledge-base.js",
-    "test:python": "uv run --with pytest --with pyyaml --with jsonschema pytest test/test-compute-score-contract.py test/test-skf-preflight.py test/test-skf-skill-inventory.py test/test-skf-validate-output.py test/test-skf-validate-frontmatter.py test/test-skf-manifest-ops.py test/test-skf-rebuild-managed-sections.py test/test-skf-atomic-write.py test/test-skf-severity-classify.py test/test-skf-structural-diff.py test/test-skf-detect-tools.py test/test-skf-forge-tier-rw.py test/test-skf-emit-result-envelope.py test/test-skf-qmd-classify-collections.py test/test-skf-merge-ccc-exclusions.py test/test-skf-resolve-package.py test/test-skf-extract-public-api.py test/test-skf-render-quick-metadata.py test/test-skf-validate-brief-inputs.py test/test-skf-emit-brief-result-envelope.py test/test-skf-write-skill-brief.py test/test-skf-detect-workspaces.py test/test-skf-recommend-scope-type.py test/test-skf-detect-language.py test/test-skf-description-guard.py test/test-skf-detect-scripts-assets.py test/test-skf-hash-content.py test/test-skf-validate-brief-schema.py test/test-skf-check-workspace-drift.py test/test-skf-update-active-symlink.py test/test-skf-build-change-manifest.py test/test-skf-provenance-gap-dispatch.py test/test-skf-resolve-authoritative-files.py test/test-skf-scan-manifests.py test/test-skf-pair-intersect.py test/test-skf-enumerate-stack-skills.py test/test-skf-compare-file-hashes.py test/test-skf-load-provenance.py test/test-skf-scan-skill-md-structure.py test/test-skf-disqualify-candidates.py test/test-skf-chain-reachability.py test/test-skf-shape-detect.py test/test-skf-detect-docs.py test/test-skf-step-doc-sources.py test/test-skf-step-doc-drift.py test/test-skf-step-hard-gate.py test/test-skf-per-pipeline-thresholds.py test/test-skf-evidence-report-fallback.py test/test-skf-validate-pins.py test/test-skf-auto-shard.py -v",
+    "test:python": "uv run --with pytest --with pyyaml --with jsonschema pytest test/test-compute-score-contract.py test/test-skf-preflight.py test/test-skf-skill-inventory.py test/test-skf-validate-output.py test/test-skf-validate-frontmatter.py test/test-skf-manifest-ops.py test/test-skf-rebuild-managed-sections.py test/test-skf-atomic-write.py test/test-skf-severity-classify.py test/test-skf-structural-diff.py test/test-skf-detect-tools.py test/test-skf-forge-tier-rw.py test/test-skf-emit-result-envelope.py test/test-skf-qmd-classify-collections.py test/test-skf-merge-ccc-exclusions.py test/test-skf-resolve-package.py test/test-skf-extract-public-api.py test/test-skf-render-quick-metadata.py test/test-skf-validate-brief-inputs.py test/test-skf-emit-brief-result-envelope.py test/test-skf-write-skill-brief.py test/test-skf-detect-workspaces.py test/test-skf-recommend-scope-type.py test/test-skf-detect-language.py test/test-skf-description-guard.py test/test-skf-detect-scripts-assets.py test/test-skf-hash-content.py test/test-skf-validate-brief-schema.py test/test-skf-check-workspace-drift.py test/test-skf-update-active-symlink.py test/test-skf-build-change-manifest.py test/test-skf-provenance-gap-dispatch.py test/test-skf-resolve-authoritative-files.py test/test-skf-scan-manifests.py test/test-skf-pair-intersect.py test/test-skf-enumerate-stack-skills.py test/test-skf-compare-file-hashes.py test/test-skf-load-provenance.py test/test-skf-scan-skill-md-structure.py test/test-skf-disqualify-candidates.py test/test-skf-chain-reachability.py test/test-skf-shape-detect.py test/test-skf-detect-docs.py test/test-skf-step-doc-sources.py test/test-skf-step-doc-drift.py test/test-skf-step-hard-gate.py test/test-skf-per-pipeline-thresholds.py test/test-skf-evidence-report-fallback.py test/test-skf-validate-pins.py test/test-skf-auto-shard.py test/test-skf-preapply.py -v",
     "test:schemas": "node test/test-agent-schema.js",
     "test:workflow": "node test/test-workflow-state.js",
     "validate:refs": "node tools/validate-file-refs.js --strict",
```

> TOOL

tool_result
id: toolu_01545XiXHCdrybP3iEFdh8o9
```
1	"""Tests for skf-preapply.py.
2	
3	Structural tests for the registry and script existence, plus functional
4	tests for CLI wiring, fingerprint matching (substring and regex), merge
5	logic, and exit codes.
6	"""
7	
8	from __future__ import annotations
9	
10	import importlib.util
11	import json
12	import pathlib
13	import subprocess
14	import sys
15	import textwrap
16	
17	import pytest
18	import yaml
19	
20	REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
21	SCRIPT_PATH = REPO_ROOT / "src" / "shared" / "scripts" / "skf-preapply.py"
22	REGISTRY_PATH = REPO_ROOT / "src" / "shared" / "_known-workarounds.yaml"
23	
24	spec = importlib.util.spec_from_file_location("skf_preapply", SCRIPT_PATH)
25	mod = importlib.util.module_from_spec(spec)
26	spec.loader.exec_module(mod)
27	
28	
29	# ---------------------------------------------------------------------------
30	# Helpers
31	# ---------------------------------------------------------------------------
32	
33	
34	def _run_cli(*extra_args: str, check: bool = False) -> subprocess.CompletedProcess:
35	    return subprocess.run(
36	        [sys.executable, str(SCRIPT_PATH), *extra_args],
37	        capture_output=True,
38	        text=True,
39	        check=check,
40	    )
41	
42	
43	def _write_registry(path: pathlib.Path, data: dict) -> None:
44	    path.write_text(yaml.dump(data, default_flow_style=False), encoding="utf-8")
45	
46	
47	def _write_md(path: pathlib.Path, content: str) -> None:
48	    path.write_text(content, encoding="utf-8")
49	
50	
51	# ---------------------------------------------------------------------------
52	# Task 3.2 — Registry file exists
53	# ---------------------------------------------------------------------------
54	
55	
56	class TestRegistryExists:
57	    def test_registry_file_exists(self) -> None:
58	        assert REGISTRY_PATH.is_file(), (
59	            f"Shared seed registry not found at {REGISTRY_PATH.as_posix()}"
60	        )
61	
62	
63	# ---------------------------------------------------------------------------
64	# Task 3.3 — Registry has version: 1 header
65	# ---------------------------------------------------------------------------
66	
67	
68	class TestRegistryVersion:
69	    @pytest.fixture(scope="class")
70	    def data(self) -> dict:
71	        return yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
72	
73	    def test_version_is_1(self, data: dict) -> None:
74	        assert data.get("version") == 1
75	
76	
77	# ---------------------------------------------------------------------------
78	# Task 3.4 — Registry has workarounds array with >= 25 entries
79	# ---------------------------------------------------------------------------
80	
81	
82	class TestRegistryEntryCount:
83	    @pytest.fixture(scope="class")
84	    def data(self) -> dict:
85	        return yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
86	
87	    def test_workarounds_is_list(self, data: dict) -> None:
88	        assert isinstance(data.get("workarounds"), list)
89	
90	    def test_at_least_25_entries(self, data: dict) -> None:
91	        assert len(data["workarounds"]) >= 25
92	
93	
94	# ---------------------------------------------------------------------------
95	# Task 3.5 — Each entry has required fields
96	# ---------------------------------------------------------------------------
97	
98	REQUIRED_FIELDS = {"fingerprint", "fix", "source", "severity", "description"}
99	
100	
101	class TestRegistryEntrySchema:
102	    @pytest.fixture(scope="class")
103	    def entries(self) -> list:
104	        data = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
105	        return data["workarounds"]
106	
107	    def test_all_entries_have_required_fields(self, entries: list) -> None:
108	        for i, entry in enumerate(entries):
109	            missing = REQUIRED_FIELDS - set(entry.keys())
110	            assert not missing, (
111	                f"Entry {i} missing fields: {missing}"
112	            )
113	
114	
115	# ---------------------------------------------------------------------------
116	# Task 3.6 — Severity values in {low, medium, high}
117	# ---------------------------------------------------------------------------
118	
119	VALID_SEVERITIES = {"low", "medium", "high"}
120	
121	
122	class TestRegistrySeverityValues:
123	    @pytest.fixture(scope="class")
124	    def entries(self) -> list:
125	        data = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
126	        return data["workarounds"]
127	
128	    def test_valid_severity_values(self, entries: list) -> None:
129	        for i, entry in enumerate(entries):
130	            assert entry["severity"] in VALID_SEVERITIES, (
131	                f"Entry {i} has invalid severity: {entry['severity']}"
132	            )
133	
134	
135	# ---------------------------------------------------------------------------
136	# Task 3.7 — At least one entry has regex: true
137	# ---------------------------------------------------------------------------
138	
139	
140	class TestRegistryRegexEntries:
141	    @pytest.fixture(scope="class")
142	    def entries(self) -> list:
143	        data = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
144	        return data["workarounds"]
145	
146	    def test_at_least_one_regex_entry(self, entries: list) -> None:
147	        regex_entries = [e for e in entries if e.get("regex") is True]
148	        assert len(regex_entries) >= 1, "Registry must have at least one regex entry"
149	
150	
151	# ---------------------------------------------------------------------------
152	# Task 3.8 — Script exists
153	# ---------------------------------------------------------------------------
154	
155	
156	class TestScriptExists:
157	    def test_script_file_exists(self) -> None:
158	        assert SCRIPT_PATH.is_file(), (
159	            f"skf-preapply.py not found at {SCRIPT_PATH.as_posix()}"
160	        )
161	
162	
163	# ---------------------------------------------------------------------------
164	# Task 3.9 — Script has PEP 723 header with pyyaml dependency
165	# ---------------------------------------------------------------------------
166	
167	
168	class TestScriptPEP723:
169	    @pytest.fixture(scope="class")
170	    def header(self) -> str:
171	        text = SCRIPT_PATH.read_text(encoding="utf-8")
172	        start = text.find("# /// script")
173	        end = text.find("# ///", start + 1)
174	        return text[start : end + len("# ///")]
175	
176	    def test_has_pep723_header(self, header: str) -> None:
177	        assert "# /// script" in header
178	
179	    def test_requires_python(self, header: str) -> None:
180	        assert "requires-python" in header
181	
182	    def test_pyyaml_dependency(self, header: str) -> None:
183	        assert "pyyaml" in header.lower()
184	
185	
186	# ---------------------------------------------------------------------------
187	# Task 3.10 — CLI accepts --target-dir, --registry, --local-registry
188	# ---------------------------------------------------------------------------
189	
190	
191	class TestCLIArgs:
192	    def test_help_mentions_target_dir(self) -> None:
193	        proc = _run_cli("--help")
194	        assert "--target-dir" in proc.stdout
195	
196	    def test_help_mentions_registry(self) -> None:
197	        proc = _run_cli("--help")
198	        assert "--registry" in proc.stdout
199	
200	    def test_help_mentions_local_registry(self) -> None:
201	        proc = _run_cli("--help")
202	        assert "--local-registry" in proc.stdout
203	
204	
205	# ---------------------------------------------------------------------------
206	# Task 3.11 — JSON stdout schema matches {applied, skipped_count, registry_version}
207	# ---------------------------------------------------------------------------
208	
209	
210	class TestOutputSchema:
211	    def test_output_has_required_keys(self, tmp_path: pathlib.Path) -> None:
212	        target = tmp_path / "target"
213	        target.mkdir()
214	        _write_md(target / "dummy.md", "nothing to match here")
215	        registry = tmp_path / "reg.yaml"
216	        _write_registry(registry, {"version": 1, "workarounds": []})
217	
218	        proc = _run_cli(
219	            "--target-dir", str(target),
220	            "--registry", str(registry),
221	        )
222	        assert proc.returncode == 0
223	        data = json.loads(proc.stdout)
224	        assert "applied" in data
225	        assert "skipped_count" in data
226	        assert "registry_version" in data
227	
228	
229	# ---------------------------------------------------------------------------
230	# Task 3.12 — Exit code 0 on valid invocation
231	# ---------------------------------------------------------------------------
232	
233	
234	class TestExitCodeSuccess:
235	    def test_exit_0_no_matches(self, tmp_path: pathlib.Path) -> None:
236	        target = tmp_path / "target"
237	        target.mkdir()
238	        _write_md(target / "doc.md", "clean content with no workarounds")
239	        registry = tmp_path / "reg.yaml"
240	        _write_registry(registry, {"version": 1, "workarounds": []})
241	
242	        proc = _run_cli("--target-dir", str(target), "--registry", str(registry))
243	        assert proc.returncode == 0
244	
245	    def test_exit_0_with_matches(self, tmp_path: pathlib.Path) -> None:
246	        target = tmp_path / "target"
247	        target.mkdir()
248	        _write_md(target / "skill.md", "This has BAD_PATTERN in it")
249	        registry = tmp_path / "reg.yaml"
250	        _write_registry(registry, {
251	            "version": 1,
252	            "workarounds": [{
253	                "fingerprint": "BAD_PATTERN",
254	                "fix": "GOOD_PATTERN",
255	                "source": "test",
256	                "severity": "low",
257	                "description": "test fix",
258	            }],
259	        })
260	
261	        proc = _run_cli("--target-dir", str(target), "--registry", str(registry))
262	        assert proc.returncode == 0
263	
264	
265	# ---------------------------------------------------------------------------
266	# Task 3.13 — Exit code 2 on missing target-dir or invalid registry
267	# ---------------------------------------------------------------------------
268	
269	
270	class TestExitCodeErrors:
271	    def test_exit_2_missing_target_dir(self, tmp_path: pathlib.Path) -> None:
272	        registry = tmp_path / "reg.yaml"
273	        _write_registry(registry, {"version": 1, "workarounds": []})
274	        missing = tmp_path / "nonexistent"
275	        proc = _run_cli(
276	            "--target-dir", str(missing),
277	            "--registry", str(registry),
278	        )
279	        assert proc.returncode == 2
280	
281	    def test_exit_2_missing_registry(self, tmp_path: pathlib.Path) -> None:
282	        target = tmp_path / "target"
283	        target.mkdir()
284	        proc = _run_cli(
285	            "--target-dir", str(target),
286	            "--registry", str(tmp_path / "no-such-file.yaml"),
287	        )
288	        assert proc.returncode == 2
289	
290	    def test_exit_2_invalid_yaml(self, tmp_path: pathlib.Path) -> None:
291	        target = tmp_path / "target"
292	        target.mkdir()
293	        bad_reg = tmp_path / "bad.yaml"
294	        bad_reg.write_text(": : : invalid yaml [[[", encoding="utf-8")
295	        proc = _run_cli(
296	            "--target-dir", str(target),
297	            "--registry", str(bad_reg),
298	        )
299	        assert proc.returncode == 2
300	
301	    def test_stderr_json_on_error(self, tmp_path: pathlib.Path) -> None:
302	        target = tmp_path / "target"
303	        target.mkdir()
304	        proc = _run_cli(
305	            "--target-dir", str(target),
306	            "--registry", str(tmp_path / "missing.yaml"),
307	        )
308	        err = json.loads(proc.stderr.strip())
309	        assert "error" in err
310	        assert "code" in err
311	
312	
313	# ---------------------------------------------------------------------------
314	# Task 3.14 — Substring matching applies fix
315	# ---------------------------------------------------------------------------
316	
317	
318	class TestSubstringMatching:
319	    def test_substring_fix_applied(self, tmp_path: pathlib.Path) -> None:
320	        target = tmp_path / "target"
321	        target.mkdir()
322	        _write_md(target / "doc.md", "The version: 0.9-draft is old")
323	        registry = tmp_path / "reg.yaml"
324	        _write_registry(registry, {
325	            "version": 1,
326	            "workarounds": [{
327	                "fingerprint": "version: 0.9-draft",
328	                "fix": "version: 1",
329	                "source": "test",
330	                "severity": "medium",
331	                "description": "fix version",
332	            }],
333	        })
334	
335	        proc = _run_cli("--target-dir", str(target), "--registry", str(registry))
336	        assert proc.returncode == 0
337	        data = json.loads(proc.stdout)
338	        assert len(data["applied"]) == 1
339	        assert data["applied"][0]["fingerprint"] == "version: 0.9-draft"
340	        updated = (target / "doc.md").read_text(encoding="utf-8")
341	        assert "version: 1" in updated
342	        assert "version: 0.9-draft" not in updated
343	
344	
345	# ---------------------------------------------------------------------------
346	# Task 3.15 — Regex matching applies fix
347	# ---------------------------------------------------------------------------
348	
349	
350	class TestRegexMatching:
351	    def test_regex_fix_applied(self, tmp_path: pathlib.Path) -> None:
352	        target = tmp_path / "target"
353	        target.mkdir()
354	        _write_md(target / "doc.md", "confidence: none\nconfidence: n/a\n")
355	        registry = tmp_path / "reg.yaml"
356	        _write_registry(registry, {
357	            "version": 1,
358	            "workarounds": [{
359	                "fingerprint": "\\bconfidence:\\s*(?:none|n/a|unset)\\b",
360	                "fix": "confidence: T1-inferred",
361	                "source": "test",
362	                "severity": "medium",
363	                "description": "normalize confidence",
364	                "regex": True,
365	            }],
366	        })
367	
368	        proc = _run_cli("--target-dir", str(target), "--registry", str(registry))
369	        assert proc.returncode == 0
370	        data = json.loads(proc.stdout)
371	        assert len(data["applied"]) == 1
372	        updated = (target / "doc.md").read_text(encoding="utf-8")
373	        assert "confidence: T1-inferred" in updated
374	        assert "confidence: none" not in updated
375	        assert "confidence: n/a" not in updated
376	
377	
378	# ---------------------------------------------------------------------------
379	# Task 3.16 — Local registry overrides shared seed on fingerprint collision
380	# ---------------------------------------------------------------------------
381	
382	
383	class TestLocalRegistryOverride:
384	    def test_local_wins_on_collision(self, tmp_path: pathlib.Path) -> None:
385	        target = tmp_path / "target"
386	        target.mkdir()
387	        _write_md(target / "doc.md", "fingerprint-collision-test content here")
388	
389	        shared_reg = tmp_path / "shared.yaml"
390	        _write_registry(shared_reg, {
391	            "version": 1,
392	            "workarounds": [{
393	                "fingerprint": "fingerprint-collision-test",
394	                "fix": "SHARED_FIX",
395	                "source": "shared",
396	                "severity": "low",
397	                "description": "shared version",
398	            }],
399	        })
400	
401	        local_reg = tmp_path / "local.yaml"
402	        _write_registry(local_reg, {
403	            "version": 1,
404	            "workarounds": [{
405	                "fingerprint": "fingerprint-collision-test",
406	                "fix": "LOCAL_FIX",
407	                "source": "local",
408	                "severity": "high",
409	                "description": "local override",
410	            }],
411	        })
412	
413	        proc = _run_cli(
414	            "--target-dir", str(target),
415	            "--registry", str(shared_reg),
416	            "--local-registry", str(local_reg),
417	        )
418	        assert proc.returncode == 0
419	        data = json.loads(proc.stdout)
420	        assert len(data["applied"]) == 1
421	        assert data["applied"][0]["fix"] == "LOCAL_FIX"
422	        updated = (target / "doc.md").read_text(encoding="utf-8")
423	        assert "LOCAL_FIX" in updated
424	        assert "SHARED_FIX" not in updated
425	
426	
427	# ---------------------------------------------------------------------------
428	# Task 3.17 — No modifications when no fingerprints match
429	# ---------------------------------------------------------------------------
430	
431	
432	class TestNoMatchNoModification:
433	    def test_no_changes_when_no_match(self, tmp_path: pathlib.Path) -> None:
434	        target = tmp_path / "target"
435	        target.mkdir()
436	        original = "This content has nothing matching any workaround."
437	        _write_md(target / "clean.md", original)
438	        registry = tmp_path / "reg.yaml"
439	        _write_registry(registry, {
440	            "version": 1,
441	            "workarounds": [{
442	                "fingerprint": "WILL_NOT_MATCH_ANYTHING_HERE",
443	                "fix": "replacement",
444	                "source": "test",
445	                "severity": "low",
446	                "description": "no match expected",
447	            }],
448	        })
449	
450	        proc = _run_cli("--target-dir", str(target), "--registry", str(registry))
451	        assert proc.returncode == 0
452	        data = json.loads(proc.stdout)
453	        assert len(data["applied"]) == 0
454	        assert data["skipped_count"] == 1
455	        assert (target / "clean.md").read_text(encoding="utf-8") == original
456	
457	
458	# ---------------------------------------------------------------------------
459	# E2E gap: --log-dir writes preapply-log.json (AC #1)
460	# ---------------------------------------------------------------------------
461	
462	
463	class TestLogDirWritesJson:
464	    def test_log_file_created(self, tmp_path: pathlib.Path) -> None:
465	        target = tmp_path / "target"
466	        target.mkdir()
467	        _write_md(target / "doc.md", "BAD_TOKEN here")
468	        registry = tmp_path / "reg.yaml"
469	        _write_registry(registry, {
470	            "version": 1,
471	            "workarounds": [{
472	                "fingerprint": "BAD_TOKEN",
473	                "fix": "GOOD_TOKEN",
474	                "source": "test",
475	                "severity": "high",
476	                "description": "test log",
477	            }],
478	        })
479	        log_dir = tmp_path / "logs"
480	
481	        proc = _run_cli(
482	            "--target-dir", str(target),
483	            "--registry", str(registry),
484	            "--log-dir", str(log_dir),
485	        )
486	        assert proc.returncode == 0
487	        log_path = log_dir / "preapply-log.json"
488	        assert log_path.is_file()
489	        log_data = json.loads(log_path.read_text(encoding="utf-8"))
490	        assert len(log_data["applied"]) == 1
491	        assert log_data["applied"][0]["fingerprint"] == "BAD_TOKEN"
492	        assert log_data["registry_version"] == 1
493	
494	    def test_log_dir_created_if_missing(self, tmp_path: pathlib.Path) -> None:
495	        target = tmp_path / "target"
496	        target.mkdir()
497	        _write_md(target / "doc.md", "no matches")
498	        registry = tmp_path / "reg.yaml"
499	        _write_registry(registry, {"version": 1, "workarounds": []})
500	        log_dir = tmp_path / "deep" / "nested" / "logs"
501	
502	        proc = _run_cli(
503	            "--target-dir", str(target),
504	            "--registry", str(registry),
505	            "--log-dir", str(log_dir),
506	        )
507	        assert proc.returncode == 0
508	        assert (log_dir / "preapply-log.json").is_file()
509	
510	
511	# ---------------------------------------------------------------------------
512	# E2E gap: Nested directory scanning (rglob traversal)
513	# ---------------------------------------------------------------------------
514	
515	
516	class TestNestedDirectoryScanning:
517	    def test_finds_md_in_subdirectories(self, tmp_path: pathlib.Path) -> None:
518	        target = tmp_path / "target"
519	        target.mkdir()
520	        sub = target / "sub" / "deep"
521	        sub.mkdir(parents=True)
522	        _write_md(sub / "nested.md", "FIX_ME_NESTED content")
523	        registry = tmp_path / "reg.yaml"
524	        _write_registry(registry, {
525	            "version": 1,
526	            "workarounds": [{
527	                "fingerprint": "FIX_ME_NESTED",
528	                "fix": "FIXED_NESTED",
529	                "source": "test",
530	                "severity": "low",
531	                "description": "nested test",
532	            }],
533	        })
534	
535	        proc = _run_cli("--target-dir", str(target), "--registry", str(registry))
536	        assert proc.returncode == 0
537	        data = json.loads(proc.stdout)
538	        assert len(data["applied"]) == 1
539	        assert data["applied"][0]["file"] == "sub/deep/nested.md"
540	        updated = sub / "nested.md"
541	        assert "FIXED_NESTED" in updated.read_text(encoding="utf-8")
542	
543	
544	# ---------------------------------------------------------------------------
545	# E2E gap: Non-.md files are ignored
546	# ---------------------------------------------------------------------------
547	
548	
549	class TestNonMdFilesIgnored:
550	    def test_txt_and_yaml_not_scanned(self, tmp_path: pathlib.Path) -> None:
551	        target = tmp_path / "target"
552	        target.mkdir()
553	        _write_md(target / "readme.txt", "MATCH_THIS content")
554	        (target / "config.yaml").write_text(
555	            "key: MATCH_THIS", encoding="utf-8"
556	        )
557	        _write_md(target / "actual.md", "no match here")
558	        registry = tmp_path / "reg.yaml"
559	        _write_registry(registry, {
560	            "version": 1,
561	            "workarounds": [{
562	                "fingerprint": "MATCH_THIS",
563	                "fix": "REPLACED",
564	                "source": "test",
565	                "severity": "low",
566	                "description": "should not match non-md",
567	            }],
568	        })
569	
570	        proc = _run_cli("--target-dir", str(target), "--registry", str(registry))
571	        assert proc.returncode == 0
572	        data = json.loads(proc.stdout)
573	        assert len(data["applied"]) == 0
574	        assert (target / "readme.txt").read_text(encoding="utf-8") == "MATCH_THIS content"
575	        assert (target / "config.yaml").read_text(encoding="utf-8") == "key: MATCH_THIS"
576	
577	
578	# ---------------------------------------------------------------------------
579	# E2E gap: Multiple workarounds applied in one run
580	# ---------------------------------------------------------------------------
581	
582	
583	class TestMultipleWorkaroundsApplied:
584	    def test_batch_apply(self, tmp_path: pathlib.Path) -> None:
585	        target = tmp_path / "target"
586	        target.mkdir()
587	        _write_md(target / "doc.md", "AAA and BBB and CCC")
588	        registry = tmp_path / "reg.yaml"
589	        _write_registry(registry, {
590	            "version": 1,
591	            "workarounds": [
592	                {
593	                    "fingerprint": "AAA",
594	                    "fix": "aaa-fixed",
595	                    "source": "test",
596	                    "severity": "low",
597	                    "description": "fix A",
598	                },
599	                {
600	                    "fingerprint": "BBB",
601	                    "fix": "bbb-fixed",
602	                    "source": "test",
603	                    "severity": "medium",
604	                    "description": "fix B",
605	                },
606	                {
607	                    "fingerprint": "NOMATCH",
608	                    "fix": "n/a",
609	                    "source": "test",
610	                    "severity": "high",
611	                    "description": "should skip",
612	                },
613	            ],
614	        })
615	
616	        proc = _run_cli("--target-dir", str(target), "--registry", str(registry))
617	        assert proc.returncode == 0
618	        data = json.loads(proc.stdout)
619	        assert len(data["applied"]) == 2
620	        assert data["skipped_count"] == 1
621	        updated = (target / "doc.md").read_text(encoding="utf-8")
622	        assert "aaa-fixed" in updated
623	        assert "bbb-fixed" in updated
624	        assert "AAA" not in updated
625	        assert "BBB" not in updated
626	
627	
628	# ---------------------------------------------------------------------------
629	# E2E gap: Applied entry has correct field schema
630	# ---------------------------------------------------------------------------
631	
632	
633	class TestAppliedEntryFields:
634	    def test_applied_entry_structure(self, tmp_path: pathlib.Path) -> None:
635	        target = tmp_path / "target"
636	        target.mkdir()
637	        _write_md(target / "skill.md", "PATTERN_X present")
638	        registry = tmp_path / "reg.yaml"
639	        _write_registry(registry, {
640	            "version": 1,
641	            "workarounds": [{
642	                "fingerprint": "PATTERN_X",
643	                "fix": "REPLACEMENT_X",
644	                "source": "test",
645	                "severity": "high",
646	                "description": "field check",
647	            }],
648	        })
649	
650	        proc = _run_cli("--target-dir", str(target), "--registry", str(registry))
651	        data = json.loads(proc.stdout)
652	        entry = data["applied"][0]
653	        assert entry["fingerprint"] == "PATTERN_X"
654	        assert entry["fix"] == "REPLACEMENT_X"
655	        assert entry["file"] == "skill.md"
656	        assert entry["severity"] == "high"
657	
658	
659	# ---------------------------------------------------------------------------
660	# E2E gap: Empty target directory (no .md files)
661	# ---------------------------------------------------------------------------
662	
663	
664	class TestEmptyTargetDirectory:
665	    def test_no_md_files_exits_0(self, tmp_path: pathlib.Path) -> None:
666	        target = tmp_path / "target"
667	        target.mkdir()
668	        registry = tmp_path / "reg.yaml"
669	        _write_registry(registry, {
670	            "version": 1,
671	            "workarounds": [{
672	                "fingerprint": "anything",
673	                "fix": "x",
674	                "source": "test",
675	                "severity": "low",
676	                "description": "no files",
677	            }],
678	        })
679	
680	        proc = _run_cli("--target-dir", str(target), "--registry", str(registry))
681	        assert proc.returncode == 0
682	        data = json.loads(proc.stdout)
683	        assert len(data["applied"]) == 0
684	        assert data["skipped_count"] == 1
685	
686	
687	# ---------------------------------------------------------------------------
688	# E2E gap: registry_version value correctness
689	# ---------------------------------------------------------------------------
690	
691	
692	class TestRegistryVersionOutput:
693	    def test_version_value_propagated(self, tmp_path: pathlib.Path) -> None:
694	        target = tmp_path / "target"
695	        target.mkdir()
696	        _write_md(target / "doc.md", "content")
697	        registry = tmp_path / "reg.yaml"
698	        _write_registry(registry, {"version": 1, "workarounds": []})
699	
700	        proc = _run_cli("--target-dir", str(target), "--registry", str(registry))
701	        data = json.loads(proc.stdout)
702	        assert data["registry_version"] == 1
703	
704	
705	# ---------------------------------------------------------------------------
706	# E2E gap: Invalid registry format (missing workarounds key)
707	# ---------------------------------------------------------------------------
708	
709	
710	class TestInvalidRegistryFormat:
711	    def test_exit_2_missing_workarounds_key(self, tmp_path: pathlib.Path) -> None:
712	        target = tmp_path / "target"
713	        target.mkdir()
714	        bad_reg = tmp_path / "bad.yaml"
715	        bad_reg.write_text("version: 1\nsome_key: value\n", encoding="utf-8")
716	
717	        proc = _run_cli("--target-dir", str(target), "--registry", str(bad_reg))
718	        assert proc.returncode == 2
719	        err = json.loads(proc.stderr.strip())
720	        assert err["code"] == "INVALID_REGISTRY"
721	
722	
723	# ---------------------------------------------------------------------------
724	# E2E gap: Specific error codes in stderr
725	# ---------------------------------------------------------------------------
726	
727	
728	class TestSpecificErrorCodes:
729	    def test_target_not_found_code(self, tmp_path: pathlib.Path) -> None:
730	        registry = tmp_path / "reg.yaml"
731	        _write_registry(registry, {"version": 1, "workarounds": []})
732	        proc = _run_cli(
733	            "--target-dir", str(tmp_path / "ghost"),
734	            "--registry", str(registry),
735	        )
736	        assert proc.returncode == 2
737	        err = json.loads(proc.stderr.strip())
738	        assert err["code"] == "TARGET_NOT_FOUND"
739	
740	    def test_registry_not_found_code(self, tmp_path: pathlib.Path) -> None:
741	        target = tmp_path / "target"
742	        target.mkdir()
743	        proc = _run_cli(
744	            "--target-dir", str(target),
745	            "--registry", str(tmp_path / "nope.yaml"),
746	        )
747	        assert proc.returncode == 2
748	        err = json.loads(proc.stderr.strip())
749	        assert err["code"] == "REGISTRY_NOT_FOUND"
750	
751	
752	# ---------------------------------------------------------------------------
753	# E2E gap: Additive merge (local adds new entries)
754	# ---------------------------------------------------------------------------
755	
756	
757	class TestAdditiveMerge:
758	    def test_local_adds_unique_entries(self, tmp_path: pathlib.Path) -> None:
759	        target = tmp_path / "target"
760	        target.mkdir()
761	        _write_md(target / "doc.md", "SHARED_ONLY and LOCAL_ONLY present")
762	
763	        shared_reg = tmp_path / "shared.yaml"
764	        _write_registry(shared_reg, {
765	            "version": 1,
766	            "workarounds": [{
767	                "fingerprint": "SHARED_ONLY",
768	                "fix": "SHARED_FIXED",
769	                "source": "shared",
770	                "severity": "low",
771	                "description": "shared entry",
772	            }],
773	        })
774	
775	        local_reg = tmp_path / "local.yaml"
776	        _write_registry(local_reg, {
777	            "version": 1,
778	            "workarounds": [{
779	                "fingerprint": "LOCAL_ONLY",
780	                "fix": "LOCAL_FIXED",
781	                "source": "local",
782	                "severity": "medium",
783	                "description": "local-only entry",
784	            }],
785	        })
786	
787	        proc = _run_cli(
788	            "--target-dir", str(target),
789	            "--registry", str(shared_reg),
790	            "--local-registry", str(local_reg),
791	        )
792	        assert proc.returncode == 0
793	        data = json.loads(proc.stdout)
794	        assert len(data["applied"]) == 2
795	        fps = {e["fingerprint"] for e in data["applied"]}
796	        assert "SHARED_ONLY" in fps
797	        assert "LOCAL_ONLY" in fps
798	
799	
800	# ---------------------------------------------------------------------------
801	# E2E gap: Same workaround matches across multiple files
802	# ---------------------------------------------------------------------------
803	
804	
805	class TestMultiFileMatching:
806	    def test_workaround_applied_to_all_matching_files(
807	        self, tmp_path: pathlib.Path
808	    ) -> None:
809	        target = tmp_path / "target"
810	        target.mkdir()
811	        _write_md(target / "a.md", "COMMON_BUG in file A")
812	        _write_md(target / "b.md", "COMMON_BUG in file B")
813	        _write_md(target / "clean.md", "no issue here")
814	        registry = tmp_path / "reg.yaml"
815	        _write_registry(registry, {
816	            "version": 1,
817	            "workarounds": [{
818	                "fingerprint": "COMMON_BUG",
819	                "fix": "FIXED_BUG",
820	                "source": "test",
821	                "severity": "medium",
822	                "description": "multi-file match",
823	            }],
824	        })
825	
826	        proc = _run_cli("--target-dir", str(target), "--registry", str(registry))
827	        assert proc.returncode == 0
828	        data = json.loads(proc.stdout)
829	        assert len(data["applied"]) == 2
830	        files = sorted(e["file"] for e in data["applied"])
831	        assert files == ["a.md", "b.md"]
832	        for f in ["a.md", "b.md"]:
833	            content = (target / f).read_text(encoding="utf-8")
834	            assert "FIXED_BUG" in content
835	            assert "COMMON_BUG" not in content
836	
```

> AGENT

All files read. Running the test suite to validate current state before review.

> TOOL

tool_use Bash
id: toolu_01B6LVei8WmyUfqHQbxNYJAP
```json
{
  "command": "uv run --with pytest --with pyyaml pytest test/test-skf-preapply.py -v 2>&1",
  "description": "Run story 3.5 test suite",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_01B6LVei8WmyUfqHQbxNYJAP
```
============================= test session starts ==============================
platform linux -- Python 3.11.14, pytest-9.0.3, pluggy-1.6.0 -- /home/armel/.cache/uv/builds-v0/.tmpf7Zfne/bin/python
cachedir: .pytest_cache
rootdir: /home/armel/Projects/OSS/bmad-module-skill-forge
collecting ... collected 38 items

test/test-skf-preapply.py::TestRegistryExists::test_registry_file_exists PASSED [  2%]
test/test-skf-preapply.py::TestRegistryVersion::test_version_is_1 PASSED [  5%]
test/test-skf-preapply.py::TestRegistryEntryCount::test_workarounds_is_list PASSED [  7%]
test/test-skf-preapply.py::TestRegistryEntryCount::test_at_least_25_entries PASSED [ 10%]
test/test-skf-preapply.py::TestRegistryEntrySchema::test_all_entries_have_required_fields PASSED [ 13%]
test/test-skf-preapply.py::TestRegistrySeverityValues::test_valid_severity_values PASSED [ 15%]
test/test-skf-preapply.py::TestRegistryRegexEntries::test_at_least_one_regex_entry PASSED [ 18%]
test/test-skf-preapply.py::TestScriptExists::test_script_file_exists PASSED [ 21%]
test/test-skf-preapply.py::TestScriptPEP723::test_has_pep723_header PASSED [ 23%]
test/test-skf-preapply.py::TestScriptPEP723::test_requires_python PASSED [ 26%]
test/test-skf-preapply.py::TestScriptPEP723::test_pyyaml_dependency PASSED [ 28%]
test/test-skf-preapply.py::TestCLIArgs::test_help_mentions_target_dir PASSED [ 31%]
test/test-skf-preapply.py::TestCLIArgs::test_help_mentions_registry PASSED [ 34%]
test/test-skf-preapply.py::TestCLIArgs::test_help_mentions_local_registry PASSED [ 36%]
test/test-skf-preapply.py::TestOutputSchema::test_output_has_required_keys PASSED [ 39%]
test/test-skf-preapply.py::TestExitCodeSuccess::test_exit_0_no_matches PASSED [ 42%]
test/test-skf-preapply.py::TestExitCodeSuccess::test_exit_0_with_matches PASSED [ 44%]
test/test-skf-preapply.py::TestExitCodeErrors::test_exit_2_missing_target_dir PASSED [ 47%]
test/test-skf-preapply.py::TestExitCodeErrors::test_exit_2_missing_registry PASSED [ 50%]
test/test-skf-preapply.py::TestExitCodeErrors::test_exit_2_invalid_yaml PASSED [ 52%]
test/test-skf-preapply.py::TestExitCodeErrors::test_stderr_json_on_error PASSED [ 55%]
test/test-skf-preapply.py::TestSubstringMatching::test_substring_fix_applied PASSED [ 57%]
test/test-skf-preapply.py::TestRegexMatching::test_regex_fix_applied PASSED [ 60%]
test/test-skf-preapply.py::TestLocalRegistryOverride::test_local_wins_on_collision PASSED [ 63%]
test/test-skf-preapply.py::TestNoMatchNoModification::test_no_changes_when_no_match PASSED [ 65%]
test/test-skf-preapply.py::TestLogDirWritesJson::test_log_file_created PASSED [ 68%]
test/test-skf-preapply.py::TestLogDirWritesJson::test_log_dir_created_if_missing PASSED [ 71%]
test/test-skf-preapply.py::TestNestedDirectoryScanning::test_finds_md_in_subdirectories PASSED [ 73%]
test/test-skf-preapply.py::TestNonMdFilesIgnored::test_txt_and_yaml_not_scanned PASSED [ 76%]
test/test-skf-preapply.py::TestMultipleWorkaroundsApplied::test_batch_apply PASSED [ 78%]
test/test-skf-preapply.py::TestAppliedEntryFields::test_applied_entry_structure PASSED [ 81%]
test/test-skf-preapply.py::TestEmptyTargetDirectory::test_no_md_files_exits_0 PASSED [ 84%]
test/test-skf-preapply.py::TestRegistryVersionOutput::test_version_value_propagated PASSED [ 86%]
test/test-skf-preapply.py::TestInvalidRegistryFormat::test_exit_2_missing_workarounds_key PASSED [ 89%]
test/test-skf-preapply.py::TestSpecificErrorCodes::test_target_not_found_code PASSED [ 92%]
test/test-skf-preapply.py::TestSpecificErrorCodes::test_registry_not_found_code PASSED [ 94%]
test/test-skf-preapply.py::TestAdditiveMerge::test_local_adds_unique_entries PASSED [ 97%]
test/test-skf-preapply.py::TestMultiFileMatching::test_workaround_applied_to_all_matching_files PASSED [100%]

============================== 38 passed in 2.02s ==============================
```

> AGENT

All 38 tests pass. Now executing the adversarial review.

---

**CODE REVIEW FINDINGS, Armel!**

**Story:** 3-5-pre-apply-workaround-registry
**Git vs Story Discrepancies:** 0 found
**Issues Found:** 0 Critical, 3 Medium, 1 Low

All 5 ACs: **IMPLEMENTED** | All tasks marked [x]: **VERIFIED**

## MEDIUM Issues

1. **Uncaught `re.error` for invalid regex fingerprints** — `skf-preapply.py:96`: `re.compile(fp)` can raise `re.error` on a malformed pattern, producing a raw traceback instead of the structured JSON error output the script promises. Should catch and route through `_err()`.

2. **Dead module import** — `test/test-skf-preapply.py:24-26`: Module loaded via importlib (`mod = ...`) but `mod` is never referenced in any test. All functional tests use subprocess. Dead code that wastes import time and confuses readers.

3. **`_err` return type is `None`, should be `NoReturn`** — `skf-preapply.py:47`: `_err()` always calls `sys.exit(2)` but is annotated `-> None`. Type checkers can't see that code after `_err()` is unreachable, causing false positives in `_load_registry`.

## LOW Issues

4. **Completion notes undercount tests** — Story says "25 tests" but there are 38 test methods.

---

Auto-fixing all issues now.

> TOOL

tool_use Edit
id: toolu_01TSEJysLREiE8Jc8f6WYNaV
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/shared/scripts/skf-preapply.py",
  "old_string": "from typing import Any, Dict, List",
  "new_string": "from typing import Any, Dict, List, NoReturn"
}
```

> TOOL

tool_result
id: toolu_01TSEJysLREiE8Jc8f6WYNaV
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/src/shared/scripts/skf-preapply.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01UazvxDpaWgV556qbTKnePW
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/shared/scripts/skf-preapply.py",
  "old_string": "def _err(message: str, code: str) -> None:",
  "new_string": "def _err(message: str, code: str) -> NoReturn:"
}
```

> TOOL

tool_result
id: toolu_01UazvxDpaWgV556qbTKnePW
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/src/shared/scripts/skf-preapply.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now fix the uncaught `re.error`:

> TOOL

tool_use Edit
id: toolu_017ghYMrsCcgNKXjtqtiXNFz
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/shared/scripts/skf-preapply.py",
  "old_string": "        if use_regex:\n                pattern = re.compile(fp)\n                if pattern.search(content):",
  "new_string": "        if use_regex:\n                try:\n                    pattern = re.compile(fp)\n                except re.error as exc:\n                    _err(\n                        f\"Invalid regex in workaround fingerprint: {exc}\",\n                        \"INVALID_REGEX\",\n                    )\n                if pattern.search(content):"
}
```

> TOOL

tool_result
id: toolu_017ghYMrsCcgNKXjtqtiXNFz
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/src/shared/scripts/skf-preapply.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now remove the dead module import from the test file:

> TOOL

tool_use Edit
id: toolu_01AzUhM1nhg7zshv1KsoHRPH
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/test/test-skf-preapply.py",
  "old_string": "import importlib.util\nimport json\nimport pathlib\nimport subprocess\nimport sys\nimport textwrap\n\nimport pytest\nimport yaml\n\nREPO_ROOT = pathlib.Path(__file__).resolve().parent.parent\nSCRIPT_PATH = REPO_ROOT / \"src\" / \"shared\" / \"scripts\" / \"skf-preapply.py\"\nREGISTRY_PATH = REPO_ROOT / \"src\" / \"shared\" / \"_known-workarounds.yaml\"\n\nspec = importlib.util.spec_from_file_location(\"skf_preapply\", SCRIPT_PATH)\nmod = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(mod)",
  "new_string": "import json\nimport pathlib\nimport subprocess\nimport sys\n\nimport pytest\nimport yaml\n\nREPO_ROOT = pathlib.Path(__file__).resolve().parent.parent\nSCRIPT_PATH = REPO_ROOT / \"src\" / \"shared\" / \"scripts\" / \"skf-preapply.py\"\nREGISTRY_PATH = REPO_ROOT / \"src\" / \"shared\" / \"_known-workarounds.yaml\""
}
```

> TOOL

tool_result
id: toolu_01AzUhM1nhg7zshv1KsoHRPH
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/test/test-skf-preapply.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now add a test for the new `INVALID_REGEX` error path:

> TOOL

tool_use Edit
id: toolu_01EnVMhQG6EozPMjfn8qy378
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/test/test-skf-preapply.py",
  "old_string": "    def test_registry_not_found_code(self, tmp_path: pathlib.Path) -> None:",
  "new_string": "    def test_invalid_regex_code(self, tmp_path: pathlib.Path) -> None:\n        target = tmp_path / \"target\"\n        target.mkdir()\n        _write_md(target / \"doc.md\", \"some content\")\n        registry = tmp_path / \"reg.yaml\"\n        _write_registry(registry, {\n            \"version\": 1,\n            \"workarounds\": [{\n                \"fingerprint\": \"[invalid(regex\",\n                \"fix\": \"x\",\n                \"source\": \"test\",\n                \"severity\": \"low\",\n                \"description\": \"bad regex\",\n                \"regex\": True,\n            }],\n        })\n        proc = _run_cli(\"--target-dir\", str(target), \"--registry\", str(registry))\n        assert proc.returncode == 2\n        err = json.loads(proc.stderr.strip())\n        assert err[\"code\"] == \"INVALID_REGEX\"\n\n    def test_registry_not_found_code(self, tmp_path: pathlib.Path) -> None:"
}
```

> TOOL

tool_result
id: toolu_01EnVMhQG6EozPMjfn8qy378
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/test/test-skf-preapply.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now fix the completion notes in the story:

> TOOL

tool_use Edit
id: toolu_01X9xVRBKriLUC1xfvm2GdTj
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/_bmad-output/implementation-artifacts/3-5-pre-apply-workaround-registry.md",
  "old_string": "- Created 25 tests covering registry structure, script PEP 723 compliance, CLI args, output schema, exit codes (0 and 2), substring matching, regex matching, local-override merge, and no-match passthrough",
  "new_string": "- Created 39 tests covering registry structure, script PEP 723 compliance, CLI args, output schema, exit codes (0 and 2), substring matching, regex matching, local-override merge, no-match passthrough, log-dir writing, nested dir scanning, multi-file matching, and invalid regex handling"
}
```

> TOOL

tool_result
id: toolu_01X9xVRBKriLUC1xfvm2GdTj
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/_bmad-output/implementation-artifacts/3-5-pre-apply-workaround-registry.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now run the tests again to confirm all fixes pass:

> TOOL

tool_use Bash
id: toolu_018spXJFR37Fk8FvnoMTiwLx
```json
{
  "command": "uv run --with pytest --with pyyaml pytest test/test-skf-preapply.py -v 2>&1",
  "description": "Verify all tests pass after fixes",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_018spXJFR37Fk8FvnoMTiwLx
```
============================= test session starts ==============================
platform linux -- Python 3.11.14, pytest-9.0.3, pluggy-1.6.0 -- /home/armel/.cache/uv/builds-v0/.tmpHVUBJc/bin/python
cachedir: .pytest_cache
rootdir: /home/armel/Projects/OSS/bmad-module-skill-forge
collecting ... collected 39 items

test/test-skf-preapply.py::TestRegistryExists::test_registry_file_exists PASSED [  2%]
test/test-skf-preapply.py::TestRegistryVersion::test_version_is_1 PASSED [  5%]
test/test-skf-preapply.py::TestRegistryEntryCount::test_workarounds_is_list PASSED [  7%]
test/test-skf-preapply.py::TestRegistryEntryCount::test_at_least_25_entries PASSED [ 10%]
test/test-skf-preapply.py::TestRegistryEntrySchema::test_all_entries_have_required_fields PASSED [ 12%]
test/test-skf-preapply.py::TestRegistrySeverityValues::test_valid_severity_values PASSED [ 15%]
test/test-skf-preapply.py::TestRegistryRegexEntries::test_at_least_one_regex_entry PASSED [ 17%]
test/test-skf-preapply.py::TestScriptExists::test_script_file_exists PASSED [ 20%]
test/test-skf-preapply.py::TestScriptPEP723::test_has_pep723_header PASSED [ 23%]
test/test-skf-preapply.py::TestScriptPEP723::test_requires_python PASSED [ 25%]
test/test-skf-preapply.py::TestScriptPEP723::test_pyyaml_dependency PASSED [ 28%]
test/test-skf-preapply.py::TestCLIArgs::test_help_mentions_target_dir PASSED [ 30%]
test/test-skf-preapply.py::TestCLIArgs::test_help_mentions_registry PASSED [ 33%]
test/test-skf-preapply.py::TestCLIArgs::test_help_mentions_local_registry PASSED [ 35%]
test/test-skf-preapply.py::TestOutputSchema::test_output_has_required_keys PASSED [ 38%]
test/test-skf-preapply.py::TestExitCodeSuccess::test_exit_0_no_matches PASSED [ 41%]
test/test-skf-preapply.py::TestExitCodeSuccess::test_exit_0_with_matches PASSED [ 43%]
test/test-skf-preapply.py::TestExitCodeErrors::test_exit_2_missing_target_dir PASSED [ 46%]
test/test-skf-preapply.py::TestExitCodeErrors::test_exit_2_missing_registry PASSED [ 48%]
test/test-skf-preapply.py::TestExitCodeErrors::test_exit_2_invalid_yaml PASSED [ 51%]
test/test-skf-preapply.py::TestExitCodeErrors::test_stderr_json_on_error PASSED [ 53%]
test/test-skf-preapply.py::TestSubstringMatching::test_substring_fix_applied PASSED [ 56%]
test/test-skf-preapply.py::TestRegexMatching::test_regex_fix_applied PASSED [ 58%]
test/test-skf-preapply.py::TestLocalRegistryOverride::test_local_wins_on_collision PASSED [ 61%]
test/test-skf-preapply.py::TestNoMatchNoModification::test_no_changes_when_no_match PASSED [ 64%]
test/test-skf-preapply.py::TestLogDirWritesJson::test_log_file_created PASSED [ 66%]
test/test-skf-preapply.py::TestLogDirWritesJson::test_log_dir_created_if_missing PASSED [ 69%]
test/test-skf-preapply.py::TestNestedDirectoryScanning::test_finds_md_in_subdirectories PASSED [ 71%]
test/test-skf-preapply.py::TestNonMdFilesIgnored::test_txt_and_yaml_not_scanned PASSED [ 74%]
test/test-skf-preapply.py::TestMultipleWorkaroundsApplied::test_batch_apply PASSED [ 76%]
test/test-skf-preapply.py::TestAppliedEntryFields::test_applied_entry_structure PASSED [ 79%]
test/test-skf-preapply.py::TestEmptyTargetDirectory::test_no_md_files_exits_0 PASSED [ 82%]
test/test-skf-preapply.py::TestRegistryVersionOutput::test_version_value_propagated PASSED [ 84%]
test/test-skf-preapply.py::TestInvalidRegistryFormat::test_exit_2_missing_workarounds_key PASSED [ 87%]
test/test-skf-preapply.py::TestSpecificErrorCodes::test_target_not_found_code PASSED [ 89%]
test/test-skf-preapply.py::TestSpecificErrorCodes::test_invalid_regex_code PASSED [ 92%]
test/test-skf-preapply.py::TestSpecificErrorCodes::test_registry_not_found_code PASSED [ 94%]
test/test-skf-preapply.py::TestAdditiveMerge::test_local_adds_unique_entries PASSED [ 97%]
test/test-skf-preapply.py::TestMultiFileMatching::test_workaround_applied_to_all_matching_files PASSED [100%]

============================== 39 passed in 2.38s ==============================
```

> AGENT

All 39 tests pass. Now updating the story status and syncing sprint tracking (Step 5).

> TOOL

tool_use Edit
id: toolu_01SKZm96WAAuyE9rNjwFjqSo
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/_bmad-output/implementation-artifacts/3-5-pre-apply-workaround-registry.md",
  "old_string": "Status: review",
  "new_string": "Status: done"
}
```

> TOOL

tool_result
id: toolu_01SKZm96WAAuyE9rNjwFjqSo
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/_bmad-output/implementation-artifacts/3-5-pre-apply-workaround-registry.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01HRiPP7u5CkFE45x9jspS4k
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/_bmad-output/implementation-artifacts/3-5-pre-apply-workaround-registry.md",
  "old_string": "- 2026-05-27: Implemented pre-apply workaround registry — shared seed with 25 fingerprints, skf-preapply.py script, and 25 structural/functional tests",
  "new_string": "- 2026-05-27: Implemented pre-apply workaround registry — shared seed with 25 fingerprints, skf-preapply.py script, and 39 structural/functional tests\n- 2026-05-27: Review fixes — added NoReturn annotation to _err(), added re.error handling for invalid regex fingerprints, removed dead importlib import from tests, added invalid regex test"
}
```

> TOOL

tool_result
id: toolu_01HRiPP7u5CkFE45x9jspS4k
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/_bmad-output/implementation-artifacts/3-5-pre-apply-workaround-registry.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now check for sprint-status.yaml:

> TOOL

tool_use Bash
id: toolu_01Gsa2DHknJiqqtpBHmmbSoc
```json
{
  "command": "ls /home/armel/Projects/OSS/bmad-module-skill-forge/_bmad-output/implementation-artifacts/sprint-status.yaml 2>/dev/null && echo \"EXISTS\" || echo \"NOT_FOUND\"",
  "description": "Check if sprint-status.yaml exists"
}
```

> TOOL

tool_result
id: toolu_01Gsa2DHknJiqqtpBHmmbSoc
```
/home/armel/Projects/OSS/bmad-module-skill-forge/_bmad-output/implementation-artifacts/sprint-status.yaml
EXISTS
```

> TOOL

tool_use Read
id: toolu_01DmmNBSxyN6z3Vuf7goBoNs
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/_bmad-output/implementation-artifacts/sprint-status.yaml"
}
```

> TOOL

tool_result
id: toolu_01DmmNBSxyN6z3Vuf7goBoNs
```
1	# generated: 2026-05-26
2	# last_updated: 2026-05-26T22:26:00
3	# project: bmad-module-skill-forge
4	# project_key: NOKEY
5	# tracking_system: file-system
6	# story_location: _bmad-output/implementation-artifacts
7	#
8	# STATUS DEFINITIONS:
9	# ==================
10	# Epic Status:
11	#   - backlog: Epic not yet started
12	#   - in-progress: Epic actively being worked on
13	#   - done: All stories in epic completed
14	#
15	# Epic Status Transitions:
16	#   - backlog → in-progress: Automatically when first story is created (via create-story)
17	#   - in-progress → done: Manually when all stories reach 'done' status
18	#
19	# Story Status:
20	#   - backlog: Story only exists in epic file
21	#   - ready-for-dev: Story file created in stories folder
22	#   - in-progress: Developer actively working on implementation
23	#   - review: Ready for code review (via Dev's code-review workflow)
24	#   - done: Story completed
25	#
26	# Retrospective Status:
27	#   - optional: Can be completed but not required
28	#   - done: Retrospective has been completed
29	#
30	# WORKFLOW NOTES:
31	# ===============
32	# - Epic transitions to 'in-progress' automatically when first story is created
33	# - Stories can be worked in parallel if team capacity allows
34	# - Developer typically creates next story after previous one is 'done' to incorporate learnings
35	# - Dev moves story to 'review', then runs code-review (fresh context, different LLM recommended)
36	# - v1.9 = Epics 1-3 (deepwiki + core improvements)
37	# - v2.0 = Epic 4 (campaign orchestration)
38	
39	generated: 2026-05-26
40	last_updated: 2026-05-27T03:15:00
41	project: bmad-module-skill-forge
42	project_key: NOKEY
43	tracking_system: file-system
44	story_location: _bmad-output/implementation-artifacts
45	
46	development_status:
47	  # ── Epic 1: Source Intelligence Foundation (v1.9) ──
48	  epic-1: done
49	  1-1-skill-shape-detection-shared-module: done
50	  1-2-doc-detection-chain-shared-module: done
51	  1-3-doc-tracking-at-compile-time: done
52	  1-4-doc-drift-detection-in-audit: done
53	  1-5-ss-active-version-manifest-state-bugfix: done
54	  epic-1-retrospective: done
55	
56	  # ── Epic 2: deepwiki — Zero-Ceremony Skill Creation (v1.9) ──
57	  epic-2: done
58	  2-1-auto-scope-mode-for-an: done
59	  2-2-auto-brief-generation-for-bs: done
60	  2-3-auto-brief-validation-with-progressive-fallback: done
61	  2-4-auto-decomposition-for-massive-repos: done
62	  2-5-docs-only-deepwiki-path: done
63	  2-6-coexistence-detection: done
64	  2-7-version-pinning-for-deepwiki: done
65	  2-8-deepwiki-pipeline-alias-onboard-deprecation: done
66	  2-9-v1-9-documentation: done
67	  epic-2-retrospective: done
68	
69	  # ── Epic 3: Quality, Scale & Workaround Automation (v1.9) ──
70	  epic-3: in-progress
71	  3-1-tiered-quality-gate-hard-gate: done
72	  3-2-per-pipeline-quality-thresholds: done
73	  3-3-evidence-report-on-threshold-fallback: done
74	  3-4-auto-shard-at-400-line-ceiling: done
75	  3-5-pre-apply-workaround-registry: review
76	  3-6-doc-rot-correction-hooks: backlog
77	  epic-3-retrospective: optional
78	
79	  # ── Epic 4: Campaign Orchestration (v2.0) ──
80	  epic-4: backlog
81	  4-1-campaign-workflow-scaffolding-state-schema: backlog
82	  4-2-campaign-setup-campaign-brief-yaml: backlog
83	  4-3-strategy-generation-provenance: backlog
84	  4-4-pin-validation: backlog
85	  4-5-dependency-tracking-enforcement: backlog
86	  4-6-per-skill-loop-kickoff-emitter: backlog
87	  4-7-tier-b-batch-capstone: backlog
88	  4-8-verification-refinement: backlog
89	  4-9-export-maintenance-campaign-report: backlog
90	  4-10-campaign-resume: backlog
91	  4-11-standing-directive: backlog
92	  4-12-onboard-removal-v2-0-documentation: backlog
93	  epic-4-retrospective: optional
94	
```

> TOOL

tool_use Edit
id: toolu_01CYf1PnUGuyyFNrkubJCLBc
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/_bmad-output/implementation-artifacts/sprint-status.yaml",
  "old_string": "  3-5-pre-apply-workaround-registry: review",
  "new_string": "  3-5-pre-apply-workaround-registry: done"
}
```

> TOOL

tool_result
id: toolu_01CYf1PnUGuyyFNrkubJCLBc
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/_bmad-output/implementation-artifacts/sprint-status.yaml has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

---

**Review Complete!**

**Story Status:** done
**Issues Fixed:** 3 (all MEDIUM issues)
**Action Items Created:** 0

| # | Severity | Finding | Fix Applied |
|---|----------|---------|-------------|
| 1 | MEDIUM | `re.compile(fp)` uncaught `re.error` → raw traceback | Added try/except with `INVALID_REGEX` error code + test |
| 2 | MEDIUM | Dead `importlib` import — `mod` never used | Removed unused import and module loading |
| 3 | MEDIUM | `_err()` annotated `-> None` instead of `-> NoReturn` | Changed to `NoReturn` import + annotation |
| 4 | LOW | Completion notes said "25 tests" (actual: 39) | Corrected to 39 |

Sprint status synced: `3-5-pre-apply-workaround-registry` → **done**
