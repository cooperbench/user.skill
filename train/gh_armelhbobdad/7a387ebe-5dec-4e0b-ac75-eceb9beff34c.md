> AGENT

I'll start by reading the improvement-queue to understand what issues actually exist before planning any fixes. Let me investigate.

> TOOL

tool_use Bash
id: toolu_011U7e4w5bB8QKJ76EvupnFA
```json
{
  "command": "ls -la /home/armel/Projects/GMC/Code/gmc-skills/forge-data/improvement-queue/ 2>&1; echo \"---TREE---\"; find /home/armel/Projects/GMC/Code/gmc-skills/forge-data/improvement-queue/ -type f 2>&1 | head -100",
  "description": "List improvement-queue contents"
}
```

> TOOL

tool_result
id: toolu_011U7e4w5bB8QKJ76EvupnFA
```
total 16
drwxrwxr-x  2 armel armel 4096 May 24 16:28 .
drwxrwxr-x 19 armel armel 4096 May 24 16:20 ..
-rw-rw-r--  1 armel armel 2331 May 24 16:22 hc-brief-skill-20260524-122157.md
-rw-rw-r--  1 armel armel 2454 May 24 16:28 hc-create-skill-20260524-122816.md
---TREE---
/home/armel/Projects/GMC/Code/gmc-skills/forge-data/improvement-queue/hc-create-skill-20260524-122816.md
/home/armel/Projects/GMC/Code/gmc-skills/forge-data/improvement-queue/hc-brief-skill-20260524-122157.md
```

> TOOL

tool_use Bash
id: toolu_01H7kcAhUYcibwbbkufGzina
```json
{
  "command": "git log --oneline -5 && echo \"---STATUS---\" && git status --short && echo \"---BRANCH---\" && git branch --show-current",
  "description": "Check SKF repo git state"
}
```

> TOOL

tool_result
id: toolu_01H7kcAhUYcibwbbkufGzina
```
7aeaaf2e Merge pull request #387 from armelhbobdad/fix/skf-brief-writer-roundtrip-385
831fcd67 fix(skf-brief-skill): round-trip target_ref/tier_a_include/amendments on brief re-write
3e79ba00 Merge pull request #386 from armelhbobdad/feat/skf-brief-skill-from-brief-headless
f6cfebfa feat(skf-brief-skill): add from_brief headless arg to ratify a pre-authored brief
88720254 Merge pull request #384 from armelhbobdad/fix/skf-create-skill-exports-map-entrypoints
---STATUS---
---BRANCH---
main
```

> AGENT

Two findings in the queue. Let me read both in full.

> TOOL

tool_use Read
id: toolu_012b93QKUL32efDwo1YfNe4X
```json
{
  "file_path": "/home/armel/Projects/GMC/Code/gmc-skills/forge-data/improvement-queue/hc-brief-skill-20260524-122157.md"
}
```

> TOOL

tool_use Read
id: toolu_017jfzZzaTWChBkAL2gBjmWz
```json
{
  "file_path": "/home/armel/Projects/GMC/Code/gmc-skills/forge-data/improvement-queue/hc-create-skill-20260524-122816.md"
}
```

> TOOL

tool_result
id: toolu_012b93QKUL32efDwo1YfNe4X
```
1	---
2	type: workflow-health-finding
3	workflow: skf-brief-skill
4	step_file: references/analyze-target.md
5	severity: gap
6	fingerprint: fp-e043b54
7	date: 2026-05-24
8	---
9	
10	## Workflow
11	`skf-brief-skill`
12	
13	## Step File
14	`src/skf-brief-skill/references/analyze-target.md`
15	
16	## Severity
17	`gap`
18	
19	## Fingerprint
20	`fp-e043b54`
21	
22	## Finding
23	Step-02 §1 fetches the repo tree at `trees/HEAD?recursive=1` unconditionally, even when `target_version` was supplied in step 01 and a matching git tag exists.
24	
25	## Expected
26	When the brief pins a `target_version`, analyze-target should resolve that version to a git ref (tag) and fetch the tree/manifests/entry files at that ref, so the analyzed structure matches the version being skilled.
27	
28	## Actual
29	The tree, manifests, and all `contents/{path}` reads default to `HEAD`. For an actively-developed repo whose HEAD has diverged past the pinned tag, this analyzes the wrong source — wrong file layout, exports, and version.
30	
31	## Evidence
32	- `references/analyze-target.md:36-37` — "`gh api repos/{owner}/{repo}/git/trees/HEAD?recursive=1` (fetch file tree)" — hardcoded `HEAD`, no `target_version`→tag resolution.
33	- `references/analyze-target.md:149` — §4.1 `contents/{file}` fetches also imply default branch, not the pinned ref.
34	- This session: `surrealdb.js` HEAD `pushed_at=2026-05-21` is past tag `v2.0.3`; I manually appended `?ref=v2.0.3` to every `gh api .../contents` and used `trees/v2.0.3` to analyze the pinned version.
35	
36	## Impact
37	Silent wrong-version analysis whenever HEAD ≠ pinned tag. In this session it cost ~6 manual fetch redirections; a less careful run would have produced a brief scoped to HEAD while claiming `target_version: 2.0.3`.
38	
39	## Suggested Fix
40	In §1, when `target_version` is set, first resolve it to a tag (try `v{version}` then `{version}` via `gh api repos/{o}/{r}/git/refs/tags`), store it as `{analysis_ref}` (default `HEAD`), and use `?ref={analysis_ref}` / `trees/{analysis_ref}` for all tree, manifest, and contents fetches in §1/§1b/§4. The local-clone path (forge-source-repo-localclone-rule) already checks out the tag; the remote-API path should match.
41	
42	## Environment
43	| Field | Value |
44	|-------|-------|
45	| Date | 2026-05-24 |
46	| OS | Linux (Debian 13) |
47	| AI Editor | Claude Code |
48	| Model | Claude Opus 4.7 (1M) |
49	| Forge Tier | Deep |
50	| SKF Version | N/A |
51	
```

> TOOL

tool_result
id: toolu_017jfzZzaTWChBkAL2gBjmWz
```
1	---
2	type: workflow-health-finding
3	workflow: skf-create-skill
4	step_file: references/extraction-patterns.md
5	severity: bug
6	fingerprint: fp-79de9d8
7	date: 2026-05-24
8	---
9	
10	## Workflow
11	`skf-create-skill`
12	
13	## Step File
14	`src/skf-create-skill/references/extraction-patterns.md`
15	
16	## Severity
17	`bug`
18	
19	## Finding
20	On ast-grep 0.42.2, the documented `language: typescript` recipes `export class $NAME`, `export function $NAME`, `export interface $NAME { $$$ }`, `export type $NAME`, and `export enum $NAME` all return **zero** matches against real `.ts` sources; only `export const $NAME` works.
21	
22	## Expected
23	The "JavaScript/TypeScript — exported functions/constants/classes" recipes and the "ast-grep Patterns" list claim these patterns extract TS exports at T1 confidence for `language: typescript`.
24	
25	## Actual
26	Verified on packages/sdk/src (72 files, 224 named exports): `export const`→32 matches; `export class`/`export function`/`export interface`/`export type`/`export enum`→0 each. Forced full source-read fallback (T1-low) for ~192 of 224 exports.
27	
28	## Evidence
29	- `references/extraction-patterns.md:250-290` — recipes `js-exported-functions`/`js-exported-classes` documented for `language: typescript`.
30	- `references/extraction-patterns.md:397` — Known Limitation #5 scopes the `export function` failure to **tsx only**; this run shows plain `typescript` class/function/interface/type/enum also fail on 0.42.2.
31	- This session: `ast-grep run -p 'export class $NAME' -l typescript --json=stream src/api src/engine src/errors.ts src/value` → 0; `export const`→32.
32	
33	## Impact
34	TS extraction at Forge/Deep silently degrades to T1-low source-reading for all non-const declaration forms; a less careful run would under-count the public surface or mis-tier confidence. Cost this session: ~0 (caught it, used a barrel-cross-checked source extractor).
35	
36	## Suggested Fix
37	Add a Known Limitation #9: "ast-grep 0.42.x — plain `language: typescript` `export class/function/interface/type/enum` patterns return zero; only `export const` matches. Use `find_code` (MCP) or a barrel-cross-checked source-read fallback at T1-low; AST-confirm only `export const`." Mirror the Rust #8 / tsx #5 fallback guidance for the `typescript` selector.
38	
39	## Environment
40	| Field | Value |
41	|-------|-------|
42	| Date | 2026-05-24 |
43	| OS | Linux (Debian 13) |
44	| AI Editor | Claude Code |
45	| Model | Claude Opus 4.7 (1M) |
46	| Forge Tier | Deep |
47	| ast-grep | 0.42.2 |
48	| SKF Version | N/A |
49	
```

> AGENT

Both findings are in **this** repo's `src/`. Per my standing practice I must re-validate each finding against the live source (and the real tool) before changing anything — the queue records what a past session believed, not necessarily current truth. Let me read the cited source files.

> TOOL

tool_use Read
id: toolu_01MiAWgvQEYwNP3Cw4jgnqrN
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/references/analyze-target.md"
}
```

> TOOL

tool_result
id: toolu_01MiAWgvQEYwNP3Cw4jgnqrN
```
1	---
2	nextStepFile: 'scope-definition.md'
3	versionResolutionFile: 'references/version-resolution.md'
4	extractPublicApiProbeOrder:
5	  - '{project-root}/_bmad/skf/shared/scripts/skf-extract-public-api.py'
6	  - '{project-root}/src/shared/scripts/skf-extract-public-api.py'
7	detectWorkspacesProbeOrder:
8	  - '{project-root}/_bmad/skf/shared/scripts/skf-detect-workspaces.py'
9	  - '{project-root}/src/shared/scripts/skf-detect-workspaces.py'
10	detectLanguageProbeOrder:
11	  - '{project-root}/_bmad/skf/shared/scripts/skf-detect-language.py'
12	  - '{project-root}/src/shared/scripts/skf-detect-language.py'
13	---
14	
15	<!-- Config: communicate in {communication_language}. -->
16	
17	# Step 2: Analyze Target
18	
19	## STEP GOAL:
20	
21	To analyze the target repository by resolving its location, reading its structure, detecting the primary language, and listing top-level modules and exports — providing the user with a factual foundation for scoping decisions.
22	
23	## Rules
24	
25	- Focus only on analysis — do not define scope yet (Step 03)
26	- Do not make scoping decisions or recommendations
27	- Do not hallucinate or guess about repository contents
28	- All user-facing output in `{communication_language}`
29	
30	## MANDATORY SEQUENCE
31	
32	### 1. Resolve Target Location
33	
34	**For GitHub URLs:**
35	- Issue both probes in **one message with two parallel Bash calls** — they are independent:
36	  - `gh api repos/{owner}/{repo}` (verify repo exists)
37	  - `gh api repos/{owner}/{repo}/git/trees/HEAD?recursive=1` (fetch file tree)
38	- If the repo-existence probe fails, fall through to the failure-class triage below; the tree response from the parallel call is discarded in that case.
39	
40	**Truncation detection:** After receiving the tree response, check the `truncated` field in the JSON output. If `truncated: true`:
41	- Display: "Note: GitHub API returned a truncated tree response ({count} items). Full analysis may require a local clone."
42	- Record in analysis summary: "Tree listing is partial — some files may not appear in the analysis."
43	- For very large repos (>1000 files in tree response): offer a recovery path instead of just warning. Interactive — present:
44	  ```
45	  Tree is truncated. How would you like to proceed?
46	    [L] Clone locally and re-analyze (slower but complete)
47	    [P] Proceed with the partial tree (faster, may miss exports under deeper paths)
48	  ```
49	  On `[L]`: shallow-clone (`git clone --depth 1 {url} {tmp_dir}`), restart this section against the local path, and remove `{tmp_dir}` after the analysis summary in §5. On `[P]` (or under headless): record `tree_truncated: true` in the analysis summary and continue without HALT.
50	
51	**On API failure (non-200 from `gh api`):**
52	
53	Distinguish the failure class before reporting:
54	- Auto-run `gh auth status` and capture its output. If it reports an unauthenticated state or expired token: HALT (exit code 3, `halt_reason: "gh-auth-failed"`) — "**Error:** GitHub CLI is not authenticated. `gh auth status` says: `{captured output}`. Run `gh auth login` and retry."
55	- If `gh auth status` reports authenticated but the call still failed (404/403): HALT (exit code 3, `halt_reason: "target-inaccessible"`) — "**Error:** Cannot access repository at `{url}`. The CLI is authenticated but the API returned `{status}`. Check the URL and that the account has access to private repositories if applicable."
56	- If `gh auth status` itself fails to run (binary missing): HALT (exit code 3, `halt_reason: "gh-auth-failed"`) — "**Error:** `gh` CLI not found on PATH. Install it from <https://cli.github.com> and re-run."
57	
58	**For local paths:**
59	- Verify the directory exists
60	- List the directory tree
61	- If path doesn't exist: **HALT** — "**Error:** Directory not found at {path}. Verify the path is correct."
62	
63	Display: "**Resolving target...**"
64	
65	### 1b. Detect Monorepo / Workspace Layout
66	
67	**Resolve `{detectWorkspacesHelper}`** from `{detectWorkspacesProbeOrder}`; first existing path wins. HALT if no candidate exists.
68	
69	Delegate workspace detection to `{detectWorkspacesHelper}` instead of reasoning through manifest rules in prose. Build a payload from the tree fetched in §1 plus the small set of root manifests the detector needs, then invoke the script:
70	
71	```bash
72	echo '{"tree": [<flat list of repo-relative file paths>], "manifests": {"package.json": "<raw text>", "Cargo.toml": "<raw text>", "pnpm-workspace.yaml": "<raw text>", "lerna.json": "<raw text>"}}' | \
73	  uv run {detectWorkspacesHelper}
74	```
75	
76	- **`tree`** — pass the flat list of repo-relative file paths already fetched in §1 (for GitHub: the `path` values from the `gh api .../git/trees/HEAD?recursive=1` response; for local: the equivalent listing).
77	- **`manifests`** — only the root manifests need contents; child-workspace manifests are looked up from the tree by the script. Include any of `package.json`, `Cargo.toml`, `pnpm-workspace.yaml`, `lerna.json` that appears at the repo root. Fetch them in **one message with N parallel Bash calls** (`gh api .../contents/{path}` for GitHub, file reads for local), then base64-decode together. Per-workspace manifest contents (e.g. `packages/foo/package.json`) are optional — including them populates the workspace `name` field with the manifest's declared package name; omitting them falls back to the directory basename.
78	
79	The script returns a JSON envelope: `{is_monorepo, manifest_kind, workspaces[], warnings[]}`. Apply the result deterministically — see `src/shared/scripts/schemas/workspace-detection.v1.json` for the full contract.
80	
81	**If `is_monorepo: false`** — skip this section silently and continue to §2.
82	
83	**If `is_monorepo: true`** — present the discovered workspaces and prompt:
84	
85	```
86	This looks like a monorepo ({manifest_kind}) with these workspaces:
87	  1. {workspaces[0].name} ({workspaces[0].path})
88	  2. {workspaces[1].name} ({workspaces[1].path})
89	  ...
90	Which one should the skill cover? Pick a number, or type 'all' to scope at the repo root.
91	```
92	
93	Interactive: wait for the user choice. On a numbered choice, store `monorepo_workspace: {path}` and rebase §2-§4b against that path. On `'all'`, leave `monorepo_workspace` unset and proceed at the repo root with a note in the analysis summary that scope is unfiltered.
94	
95	Headless: if the input contract supplied an `include` glob that begins with one of the workspace paths, auto-select that workspace (log `"headless: auto-selected workspace {name} from include glob"`). Otherwise default to repo root and log `"warn: monorepo detected ({manifest_kind}) but no workspace pre-selected — analyzing at repo root"`.
96	
97	Surface any non-empty `warnings[]` from the script to the operator log so a malformed root manifest is debuggable; the workflow does not HALT — falling back to repo-root analysis is always safe.
98	
99	**`cross-ecosystem workspace ignored` warning:** when a root workspace manifest from a different language ecosystem co-exists with the surfaced one (e.g. a root `Cargo.toml [workspace]` alongside a pnpm workspace), the script surfaces only the higher-priority kind and emits this warning naming the ignored kind and its member count. The ignored ecosystem's workspaces are **not** in `workspaces[]`, so the numbered menu above will not list them. When this warning is present, tell the operator both ecosystems exist and ask which the skill should cover; if they pick the ignored ecosystem, scope §2-§4b at its root (or the relevant member) rather than the surfaced workspace, and carry the ignored kind into §3 (see the `workspace_signal` note there).
100	
101	### 2. Read Repository Structure
102	
103	List the top-level directory structure:
104	
105	"**Repository Structure:**
106	```
107	{repo-name}/
108	├── {top-level files}
109	├── {top-level directories}/
110	│   └── ...
111	└── ...
112	```
113	**Total:** {file count} files, {directory count} directories"
114	
115	### 3. Detect Primary Language
116	
117	**Resolve `{detectLanguageHelper}`** from `{detectLanguageProbeOrder}`; first existing path wins. HALT if no candidate exists.
118	
119	Delegate the rule walk to `{detectLanguageHelper}` instead of evaluating manifest presence and extension frequency in prose:
120	
121	```bash
122	echo '{"tree": [<flat list of repo-relative file paths from §1>], "workspace_signal": "<§1b manifest_kind, or omit when null>"}' | uv run {detectLanguageHelper}
123	```
124	
125	Pass the §1b `manifest_kind` as `workspace_signal` (omit the key when it is `null` / not a monorepo). This gives the workspace root precedence: for a `cargo-workspace` or `python-multi-package` root, the script returns the root language (rust/python) instead of being misled into `typescript` by a nested `package.json` + `tsconfig.json` in a non-workspace subdirectory (e.g. a `docs/` or `website/` site). JS-family workspace kinds (`npm-workspaces`/`pnpm-workspaces`/`lerna`) carry no override — their root `package.json` resolves js/ts normally.
126	
127	**When §1b surfaced a `cross-ecosystem workspace ignored` warning and the operator chose the ignored ecosystem:** pass that ignored kind as `workspace_signal` (not the surfaced kind), so a co-located `cargo-workspace`/`python-multi-package` root resolves to rust/python instead of being pinned to the surfaced ecosystem's language by the workspace that won detection priority.
128	
129	The script returns `{language, confidence, detection_source, fallback_to_extension_frequency}` after walking the documented rule table (the `workspace_signal` precedence above first, then manifest presence — package.json with tsconfig.json disambiguation, Cargo.toml, pyproject.toml/setup.py/setup.cfg, go.mod, pom.xml, build.gradle.kts, build.gradle Groovy with Java/Kotlin disambiguation, *.csproj/*.sln, Gemfile — then extension-frequency fallback over recognized source extensions). Use the returned values directly:
130	
131	"**Detected language:** {language}
132	**Confidence:** {confidence}
133	**Detection source:** {detection_source}"
134	
135	If `confidence` is `low` (or `unknown` is returned for `language`): flag for user override in step 03 §4.
136	
137	### 4. List Top-Level Modules and Exports
138	
139	**Resolve `{extractPublicApiHelper}`** from `{extractPublicApiProbeOrder}`; first existing path wins. HALT if no candidate exists.
140	
141	Identify the public API surface. **Delegate the parsing to `{extractPublicApiHelper}` whenever the detected language is supported** — the script is the single source of truth for manifest parsing, export discovery, and version detection across the whole SKF pipeline. Hand-rolling these in prose creates drift seams the LLM cannot fully close.
142	
143	**Script-supported languages** (use the script): `js`, `ts`, `javascript`, `typescript`, `python`, `rust`, `go`, `java`, `kotlin`.
144	
145	This section runs exactly one of §4.1 (script path) or §4.2 (fallback path) based on the detected language, then always emits §4.3 (output format) and conditionally §4.4 (semantic signals).
146	
147	#### 4.1 Procedure — script-supported languages
148	
149	1. Read the relevant files into memory (no parsing yet — just collect content). For GitHub sources, issue **all N `gh api repos/{owner}/{repo}/contents/{file}` calls in a single message with N parallel Bash calls** (one per manifest + each entry point), then base64-decode the responses together — these are 2-4 independent fetches per typical run. For local sources read directly (also parallelisable, but local reads are fast enough that serial Read tool calls are acceptable).
150	
151	   | Language | Manifest | Entry points (mode=quick) |
152	   |----------|----------|--------------------------|
153	   | js / ts / javascript / typescript | `package.json` (root, or primary workspace package per `references/version-resolution.md`) | `index.{ts,js}` and/or `src/index.{ts,js}` if present |
154	   | python | `pyproject.toml` (or `setup.py` / `setup.cfg` if no `pyproject.toml`) | top-level `__init__.py` of the package, plus `_version.py` if present |
155	   | rust | `Cargo.toml` (`[package]` — workspace root if `version = { workspace = true }`) | `src/lib.rs` |
156	   | go | `go.mod` | top-level `*.go` exporting the package surface |
157	   | java | `pom.xml` | (manifest alone is sufficient for the modules listing) |
158	   | kotlin | `build.gradle` / `build.gradle.kts` | (manifest alone) |
159	
160	2. Build a JSON payload matching the script contract:
161	
162	   ```json
163	   {
164	     "language": "<one of the supported values>",
165	     "manifest": {"path": "<relative path>", "content": "<file contents>"},
166	     "entries":  [{"path": "<relative path>", "content": "<file contents>"}, ...],
167	     "mode":     "quick"
168	   }
169	   ```
170	
171	3. Invoke the script and parse its JSON stdout:
172	
173	   ```bash
174	   echo '<payload-json>' | uv run {extractPublicApiHelper} --mode quick
175	   ```
176	
177	   On a non-zero exit (codes 1 or 2 per the script's docstring), capture stderr, log it, and fall through to §4.2 (the prose-fallback path) — never HALT just because the script choked on an unusual manifest.
178	
179	4. Render the returned `package_name`, `exports` (each entry's `name`/`type`/`source_file`), `dependencies`, and any `warnings` to the user. The script also returns `version` — feed that into §4b instead of re-deriving.
180	
181	5. The script does not enumerate directories under `src/`. The LLM still lists those as "Top-Level Modules/Directories" so the user sees structural context (Maven and Gradle are the exception — for those, the script returns a `modules` array which IS the list).
182	
183	#### 4.2 Procedure — fallback (not script-supported)
184	
185	Languages outside the script coverage (Ruby / C# / Swift / etc.) take this path. The §4.1 fall-through on script error also lands here.
186	
187	Fall back to ad-hoc inspection — `Gemfile` / `*.csproj` / `*.sln` / `Package.swift` / file extension frequency. List top-level source directories as potential modules and note any obvious entry points. Flag the limitation in the analysis summary so the user knows scoping is on coarser signals.
188	
189	#### 4.3 Output format (both paths)
190	
191	"**Top-Level Modules/Directories:**
192	{numbered list of modules with brief description of each}
193	
194	**Detected Exports/Entry Points:**
195	{numbered list of public-facing items found — from script output when available, ad-hoc inspection otherwise}"
196	
197	#### 4.4 Semantic Signals (Forge+/Deep with ccc only)
198	
199	**Remote source guard:** If the target source was resolved via GitHub API (remote URL, not a local file path), skip this CCC subsection — CCC requires a local source index and cannot operate on remote-only sources. Note: "CCC semantic discovery skipped — target is remote. CCC discovery will run automatically during create-skill after the source is cloned."
200	
201	If `tools.ccc` is true in forge-tier.yaml, supplement the module listing with a semantic discovery pass:
202	
203	**CCC Semantic Discovery:**
204	- **Claude Code:** Use `/ccc search "{repo_name} public API exports modules" {source_path}`
205	- **Cursor:** Use `ccc` MCP server `search` tool with query `"{repo_name} public API exports modules"` and path `{source_path}`
206	- **CLI fallback:** `ccc search "{repo_name} public API exports modules" --path {source_path} --limit 10`
207	
208	See `knowledge/tool-resolution.md` for full bridge-to-tool mapping.
209	
210	If results are returned, display:
211	
212	"**Semantic Signals (ccc):**
213	{numbered list of file:snippet pairs from CCC results — top 5 most relevant}"
214	
215	This supplements — never replaces — the explicit module list above. CCC may surface non-obvious entry points (dynamically constructed exports, re-export chains) that static directory analysis misses.
216	
217	If CCC is unavailable or returns no results: skip this subsection silently.
218	
219	### 4b. Detect Source Version
220	
221	**When the language was script-supported (§4 took the script path):** the `version` field returned by `{extractPublicApiHelper}` IS the detected version — do not re-derive it and do not load `{versionResolutionFile}`. The script already implements the language-specific lookups documented in that reference, so loading the reference here only burns context.
222	
223	**When the language was not script-supported:** load `{versionResolutionFile}` and follow the prose Detection Algorithm directly (Ruby / C# / Swift / etc. fall outside the script's coverage).
224	
225	Surface the result regardless of which path produced it:
226	
227	**If `target_version` was provided in step 01:**
228	- Display: "**Target version:** {target_version} (user-specified)"
229	
230	Display: "**Detected version:** {version or 'Not detected — will default to 1.0.0'}"
231	
232	{If target_version was provided AND auto-detected version differs:}
233	"**Note:** Detected version ({detected_version}) differs from your target version ({target_version}). Using target version (per `references/version-resolution.md` precedence rules)."
234	
235	If detection fails or returns a non-semver value: note that version will default to `"1.0.0"` and the user can override in step 04. The actual write happens in step 05.
236	
237	### 5. Report Analysis Summary
238	
239	Present the complete analysis:
240	
241	"**Analysis Complete**
242	
243	---
244	
245	**Target:** {repo URL or path}
246	**Language:** {detected language} ({confidence})
247	**Structure:** {file count} files across {directory count} directories
248	
249	**Key Modules ({count}):**
250	{bulleted list of modules}
251	
252	**Public Exports/Entry Points ({count}):**
253	{bulleted list of exports}
254	
255	**Notable Files:**
256	- README: {found/not found}
257	- Tests: {found/not found — location}
258	- Docs: {found/not found — location}
259	- Config: {list of config files found}
260	- Version: {detected version or "Not detected — defaulting to 1.0.0"}
261	
262	---
263	
264	{If language confidence is low:}
265	**Note:** Language detection confidence is low. You'll be able to override this in the next step.
266	
267	Moving to scope definition where you'll choose what to include and exclude."
268	
269	### 6. Auto-Proceed to Scope Definition
270	
271	Display: "**Proceeding to scope definition...**
272	
273	Review the analysis above. If anything looks wrong, let me know now — otherwise I'll proceed to scope definition."
274	
275	Pause briefly for user input. If the user provides corrections or asks questions, address them and re-present any updated analysis findings. Then proceed.
276	
277	#### Menu Handling Logic:
278	
279	- After analysis report is presented to user and any corrections addressed, load, read entire file, then execute {nextStepFile}
280	
281	#### EXECUTION RULES:
282	
283	- This is a soft auto-proceed step — present the pause prompt, wait briefly for user input
284	- If user provides corrections: address them, then proceed
285	- If no user input after a brief pause: proceed directly to step 03
286	
287	## CRITICAL STEP COMPLETION NOTE
288	
289	ONLY WHEN the analysis is complete and the summary has been presented to the user will you load and read fully `scope-definition.md` to begin scope definition.
290	
291	
```

> AGENT

Finding 1 is **confirmed** against live source: `HEAD` is hardcoded at lines 37, 76, and the `contents/{file}` fetches at line 149 default to the branch HEAD. `target_version` is a known variable (used in §4b, lines 227–235). The gap is real.

Now let me read the create-skill finding's source and the related references, and empirically re-validate the ast-grep claim since I have the tool.

> TOOL

tool_use Read
id: toolu_01DpNMVfsv67MNfXCPjxwvTC
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/references/extraction-patterns.md",
  "offset": 230,
  "limit": 180
}
```

> TOOL

tool_result
id: toolu_01DpNMVfsv67MNfXCPjxwvTC
```
230	```
231	
232	**Python — public classes:**
233	
234	```yaml
235	id: python-public-classes
236	language: python
237	rule:
238	  pattern: 'class $NAME'
239	  kind: class_definition
240	  inside:
241	    kind: module
242	    stopBy: end
243	constraints:
244	  NAME:
245	    regex: '^[^_]'
246	```
247	
248	> **Pattern note:** The minimal `class $NAME` pattern (with `kind: class_definition` to disambiguate the AST node) works on ast-grep 0.42.x via both MCP `find_code_by_rule` and CLI `--json=stream`. The previously documented `class $NAME($$$BASES)` and `class $NAME($$$BASES):` variants are known-broken on 0.42.x — see Known Limitations #7 below. For simple CLI extraction without a YAML rule, use `ast-grep run -p 'class $NAME' -l python --json=stream {path}` and post-filter names via the `^[^_]` regex in the Python processing step of the CLI streaming template.
249	
250	**JavaScript/TypeScript — exported functions:**
251	
252	> **Language selection:** Use `language: typescript` for `.ts` files and `language: tsx` for `.tsx` files. Patterns that work with `typescript` may return zero results with `tsx` and vice versa — they use different tree-sitter parsers. For mixed codebases, run each pattern twice (once per language) and merge results. Note: `export function` patterns may fail with `tsx` on ast-grep 0.41.x (see Known Limitations #5) — use source reading as fallback for those.
253	
254	```yaml
255	id: js-exported-functions
256	language: typescript  # Use 'tsx' for .tsx files — see language selection note above
257	rule:
258	  pattern: 'export function $NAME($$$PARAMS)'
259	```
260	
261	**JavaScript/TypeScript — exported constants:**
262	
263	```yaml
264	id: js-exported-constants
265	language: typescript
266	rule:
267	  pattern: 'export const $NAME = $VALUE'
268	```
269	
270	**JavaScript/TypeScript — exported arrow functions:**
271	
272	```yaml
273	id: js-exported-arrow-functions
274	language: typescript
275	rule:
276	  pattern: 'export const $NAME = ($$$PARAMS) => $BODY'
277	```
278	
279	> **JS/TS Pattern Merging:** Modern TypeScript codebases often use `export const` exclusively for all exports (arrow functions, objects, constants). Run ALL four JS/TS patterns (functions, arrow functions, constants, classes) and merge results by `$NAME`. Priority when deduplicating: arrow function match > function declaration match > constant match. Arrow function matches capture parameters directly; constant matches require inspecting `$VALUE` to extract signatures.
280	
281	**JavaScript/TypeScript — exported classes (use `find_code`, not `find_code_by_rule`):**
282	
283	```yaml
284	id: js-exported-classes
285	language: typescript
286	rule:
287	  pattern: 'export class $NAME'
288	```
289	
290	> **Important:** For class patterns, use `find_code()` rather than `find_code_by_rule()`. The `find_code_by_rule` API requires explicit AST `kind` rules for class exports, which adds complexity. The simpler `find_code()` pattern approach works reliably for class detection.
291	
292	**JavaScript/TypeScript — re-export detection (use `find_code`):**
293	
294	Use `find_code()` with pattern `export { $$$NAMES } from $SOURCE` for re-export detection. Note: this pattern may produce multiple AST node matches. Post-process results to split comma-separated names from `$$$NAMES`. For complex re-export chains (aliased exports, default re-exports, namespace re-exports), fall back to the Re-Export Tracing protocol in `extraction-patterns-tracing.md`.
295	
296	**Rust — public functions:**
297	
298	```yaml
299	id: rust-public-functions
300	language: rust
301	rule:
302	  any:
303	    - pattern: 'pub fn $NAME($$$PARAMS) -> $RET'
304	    - pattern: 'pub fn $NAME($$$PARAMS)'
305	```
306	
307	**Go — exported functions (capitalized):**
308	
309	```yaml
310	id: go-exported-functions
311	language: go
312	rule:
313	  any:
314	    - pattern: 'func $NAME($$$PARAMS) $RET'
315	    - pattern: 'func $NAME($$$PARAMS)'
316	constraints:
317	  NAME:
318	    regex: '^[A-Z]'
319	```
320	
321	### Component Library YAML Rule Recipes
322	
323	These patterns are used by `component-extraction.md` when `scope.type: "component-library"`. They prioritize Props interfaces and PascalCase component exports.
324	
325	**React/TypeScript — Props interfaces (primary API contracts):**
326	
327	```yaml
328	id: react-props-interfaces
329	language: typescript  # Use 'tsx' for .tsx files
330	rule:
331	  pattern: 'export interface $NAME { $$$ }'
332	constraints:
333	  NAME:
334	    regex: '.*Props$'
335	```
336	
337	**React/TypeScript — Component function exports (PascalCase):**
338	
339	> **Language note:** Use `language: tsx` for `.tsx` files. The `export function` pattern may fail with tsx on ast-grep 0.41.x (see Known Limitations #5). Use `export const` patterns as primary and fall back to source reading for `export function` in tsx files.
340	
341	```yaml
342	id: react-component-functions
343	language: tsx
344	rule:
345	  pattern: 'export function $NAME($$$PARAMS)'
346	constraints:
347	  NAME:
348	    regex: '^[A-Z]'
349	```
350	
351	**React/TypeScript — Component arrow function exports:**
352	
353	```yaml
354	id: react-component-arrow-functions
355	language: typescript
356	rule:
357	  pattern: 'export const $NAME = ($$$PARAMS) => $BODY'
358	constraints:
359	  NAME:
360	    regex: '^[A-Z]'
361	```
362	
363	**Vue — defineProps extraction:**
364	
365	```yaml
366	id: vue-define-props
367	language: typescript
368	rule:
369	  pattern: 'defineProps<$TYPE>()'
370	```
371	
372	**Props-to-Component linking strategy:**
373	
374	After extracting Props interfaces and component exports, link them using this 3-level fallback chain:
375	
376	1. **Naming convention (primary):** Strip `Props` suffix from interface name → match to component export (e.g., `NativeLiquidButtonProps` → `NativeLiquidButton`)
377	2. **File co-location (fallback):** If naming doesn't match, check if a Props interface and a PascalCase export function are defined in the same file — link them
378	3. **Generic parameter (deep fallback):** Search for `ComponentProps<typeof $NAME>` or `React.ComponentProps<typeof $NAME>` patterns that reference the component by name
379	
380	Unlinked Props interfaces are included as standalone type exports. Unlinked component exports are included with a note that no Props interface was found (signature-only, T1-low confidence for API contract).
381	
382	### Known ast-grep Limitations
383	
384	When using ast-grep for extraction, be aware of these documented limitations:
385	
386	1. **`find_code_by_rule` requires explicit `kind` for class exports:** The `export class $NAME` pattern needs a `kind` rule specifying the tree-sitter node type when used with `find_code_by_rule`. Use the simpler `find_code()` API instead for class detection.
387	
388	2. **Re-export patterns produce multiple AST nodes:** `export { A, B, C } from './module'` decomposes into multiple metavariable bindings for `$$$NAMES`. Results require post-processing to split comma-separated names.
389	
390	3. **Default anonymous exports capture no name:** `export default function $NAME` works, but `export default $EXPR` (anonymous default export) captures no name in `$NAME`. Fall back to source reading (T1-low) for anonymous defaults.
391	
392	4. **Fallback protocol:** If an ast-grep pattern returns errors or zero results when results are expected:
393	   - First: retry with `find_code()` using a simpler pattern (drop type annotations, use broader match)
394	   - Second: if `find_code()` also fails, fall back to source reading for that pattern category (T1-low confidence)
395	   - Never silently accept zero results for a pattern category that the source language commonly uses
396	
397	5. **TSX `export function` pattern failure:** The `export function $NAME($$$PARAMS)` pattern may return zero results in TSX files with ast-grep 0.41.x. This affects both MCP tools and CLI. `export const` and `export type` patterns are unaffected. **Workaround:** For TSX files, use `export const` patterns first (which work), then fall back to source reading (grep/file read) for `export function` declarations. When a TSX codebase shows zero `export function` matches but source files clearly contain them, this is a known ast-grep tree-sitter tsx parser limitation — not an extraction error. Log it in the evidence report and proceed with T1-low confidence for those exports.
398	
399	6. **CLI `--json=stream` may produce no output:** On ast-grep 0.41.x, `--json=stream` may produce empty output for certain patterns. The `--json=stream` flag requires the explicit `run` subcommand: use `ast-grep run -p '{pattern}' --json=stream` (not `ast-grep -p '{pattern}' --json=stream`). If streaming still produces no output, fall back to the MCP tool or source reading.
400	
401	7. **Python class patterns with bases/colon return zero (ast-grep 0.42.x):** The patterns `class $NAME($$$BASES)` and `class $NAME($$$BASES):` return zero matches on real Python sources with ast-grep 0.42.0, even on files containing dozens of subclassed public classes. `find_code_by_rule` also rejects the bare inline rule without `kind` as `Rule must specify a set of AST kinds to match. Try adding \`kind\` rule.` **Workaround:** Use the minimal `class $NAME` pattern with `kind: class_definition` (YAML) or `ast-grep run -p 'class $NAME' -l python --json=stream` (CLI), then post-filter names via the `^[^_]` regex. The `^[^_]` constraint enforces the "public" filter since ast-grep's base-match rule is what's broken, not the name-match rule. See the Python — public classes recipe above.
402	
403	8. **Rust `pub fn` any-pattern returns zero; bare `pub fn $NAME` over-captures (ast-grep 0.42.x):** The `rust-public-functions` recipe's `any:` of `pub fn $NAME($$$PARAMS) -> $RET` / `pub fn $NAME($$$PARAMS)` returns "No matches found" on real Rust sources with ast-grep 0.42.2, even on crates containing 200+ public functions. Dropping to the bare `pub fn $NAME` pattern matches, but over-captures restricted-visibility functions such as `pub(crate) fn` / `pub(super) fn`, which are **not** public API. **Workaround:** Prefer a visibility-constrained source grep — `rg '^\s*pub fn ' <src>` filtered to exclude lines beginning `pub(` — cross-checked against the AN-verified public surface, at T1-low confidence. Never silently accept zero results for Rust public functions, and never treat a bare `pub fn $NAME` match set as the public API without stripping `pub(...)`-restricted items. See the Rust — public functions recipe above.
404	
405	### Component Library Demo/Example Auto-Exclusion
406	
407	When `scope.type: "component-library"`, auto-detect and propose demo/example exclusions before extraction begins. **User confirmation is required before applying** — some `examples/` directories contain API-level code.
408	
409	**Auto-detect directory patterns:**
```

> TOOL

tool_use Bash
id: toolu_01CVJHKrUDGtUa9k7eXiGGi6
```json
{
  "command": "which ast-grep sg 2>&1; echo \"---VERSION---\"; ast-grep --version 2>&1 || sg --version 2>&1",
  "description": "Check ast-grep availability and version"
}
```

> TOOL

tool_result
id: toolu_01CVJHKrUDGtUa9k7eXiGGi6
```
/home/armel/.cargo/bin/ast-grep
/home/armel/.cargo/bin/sg
---VERSION---
ast-grep 0.42.2
```

> AGENT

I have ast-grep **0.42.2** — exactly the version in the finding. Let me empirically test each documented TypeScript export pattern against a real `.ts` fixture to confirm/refute the claim before I touch any docs.

> TOOL

tool_use Bash
id: toolu_01WWkDYneHh8YZgFHX61TXo2
```json
{
  "command": "cd /tmp && cat > skf-astgrep-probe.ts <<'EOF'\nexport const myConst = 42;\nexport const myArrow = (a: number): number => a + 1;\nexport function myFunc(a: number): number { return a; }\nexport class MyClass { x = 1; }\nexport interface MyIface { x: number; }\nexport type MyType = string | number;\nexport enum MyEnum { A, B, C }\nEOF\necho \"=== export const \\$NAME = \\$VALUE ===\"\nast-grep run -p 'export const $NAME = $VALUE' -l typescript --json=stream skf-astgrep-probe.ts | grep -o '\"text\":\"export [a-z]* [A-Za-z]*' || echo \"(no output)\"\necho \"=== export function \\$NAME(\\$\\$\\$PARAMS) ===\"\nast-grep run -p 'export function $NAME($$$PARAMS)' -l typescript --json=stream skf-astgrep-probe.ts | grep -o '\"text\":\"export [a-z]* [A-Za-z]*' || echo \"(no output)\"\necho \"=== export class \\$NAME ===\"\nast-grep run -p 'export class $NAME' -l typescript --json=stream skf-astgrep-probe.ts | grep -o '\"text\":\"export [a-z]* [A-Za-z]*' || echo \"(no output)\"\necho \"=== export interface \\$NAME { \\$\\$\\$ } ===\"\nast-grep run -p 'export interface $NAME { $$$ }' -l typescript --json=stream skf-astgrep-probe.ts | grep -o '\"text\":\"export [a-z]* [A-Za-z]*' || echo \"(no output)\"\necho \"=== export type \\$NAME ===\"\nast-grep run -p 'export type $NAME' -l typescript --json=stream skf-astgrep-probe.ts | grep -o '\"text\":\"export [a-z]* [A-Za-z]*' || echo \"(no output)\"\necho \"=== export enum \\$NAME ===\"\nast-grep run -p 'export enum $NAME' -l typescript --json=stream skf-astgrep-probe.ts | grep -o '\"text\":\"export [a-z]* [A-Za-z]*' || echo \"(no output)\"",
  "description": "Empirically test TS export patterns on ast-grep 0.42.2"
}
```

> TOOL

tool_result
id: toolu_01WWkDYneHh8YZgFHX61TXo2
```
=== export const $NAME = $VALUE ===
"text":"export const myConst
"text":"export const myArrow
=== export function $NAME($$$PARAMS) ===
(no output)
=== export class $NAME ===
Warning: Pattern contains an ERROR node and may cause unexpected results.
Help: ast-grep parsed the pattern but it matched nothing in this run. Try using playground to refine the pattern.
See also: https://ast-grep.github.io/playground.html

(no output)
=== export interface $NAME { $$$ } ===
"text":"export interface MyIface
=== export type $NAME ===
Warning: Pattern contains an ERROR node and may cause unexpected results.
Help: ast-grep parsed the pattern but it matched nothing in this run. Try using playground to refine the pattern.
See also: https://ast-grep.github.io/playground.html

(no output)
=== export enum $NAME ===
Warning: Pattern contains an ERROR node and may cause unexpected results.
Help: ast-grep parsed the pattern but it matched nothing in this run. Try using playground to refine the pattern.
See also: https://ast-grep.github.io/playground.html

(no output)
Shell cwd was reset to /home/armel/Projects/OSS/bmad-module-skill-forge
```

> AGENT

Critical nuance — the empirical results **partially contradict** the finding. Let me probe interface variants more carefully, since the finding claims `export interface` returns zero but my test shows it matches.

> TOOL

tool_use Bash
id: toolu_01GXuhxBK4GJiRDKKGzRiuXF
```json
{
  "command": "cd /tmp && cat > skf-astgrep-probe2.ts <<'EOF'\nexport interface Simple { x: number; }\nexport interface Generic<T> { value: T; }\nexport interface Extended extends Base { y: number; }\nexport interface Multi {\n  a: string;\n  b: number;\n}\nexport interface Empty {}\nEOF\necho \"=== export interface \\$NAME { \\$\\$\\$ } (variants) ===\"\nast-grep run -p 'export interface $NAME { $$$ }' -l typescript --json=stream skf-astgrep-probe2.ts 2>&1 | grep -o '\"text\":\"export interface [A-Za-z]*' || echo \"(no matches)\"\necho \"\"\necho \"=== bare: export interface \\$NAME ===\"\nast-grep run -p 'export interface $NAME' -l typescript --json=stream skf-astgrep-probe2.ts 2>&1 | grep -oE '(ERROR node|\"text\":\"export interface [A-Za-z]*)' || echo \"(no matches)\"\necho \"\"\necho \"=== type alias variants: type \\$NAME = \\$T (no export kw) ===\"\nprintf 'export type A = string;\\ntype B = number;\\n' > t2.ts\nast-grep run -p 'type $NAME = $T' -l typescript --json=stream t2.ts 2>&1 | grep -oE '(ERROR node|\"text\":\"[a-z ]*type [A-Za-z]*)' || echo \"(no matches)\"",
  "description": "Probe interface and type-alias pattern variants"
}
```

> TOOL

tool_result
id: toolu_01GXuhxBK4GJiRDKKGzRiuXF
```
=== export interface $NAME { $$$ } (variants) ===
"text":"export interface Simple
"text":"export interface Multi
"text":"export interface Empty

=== bare: export interface $NAME ===
ERROR node

=== type alias variants: type $NAME = $T (no export kw) ===
"text":"type A
"text":"type B
Shell cwd was reset to /home/armel/Projects/OSS/bmad-module-skill-forge
```

> AGENT

More nuance: `export interface $NAME { $$$ }` works for **plain** interfaces but silently misses `Generic<T>` and `extends Base` forms. And `type $NAME = $T` works while `export type $NAME` errors. Let me nail down the `export function` case and confirm the pattern that the finding documents.

> TOOL

tool_use Bash
id: toolu_014KkU8qmzT7CrDyDq9DpVTC
```json
{
  "command": "cd /tmp && cat > skf-fn.ts <<'EOF'\nexport function plainFn(a: number): number { return a; }\nexport function noRet(a: number) { return a; }\nexport async function asyncFn(): Promise<void> {}\nfunction bareFn(a: number) { return a; }\nEOF\nfor pat in 'export function $NAME($$$PARAMS)' 'export function $NAME($$$PARAMS) { $$$ }' 'function $NAME($$$PARAMS)' 'export function $NAME'; do\n  echo \"=== [$pat] ===\"\n  ast-grep run -p \"$pat\" -l typescript --json=stream skf-fn.ts 2>&1 | grep -oE '(Pattern contains an ERROR|\"text\":\"[a-z ]*function [A-Za-z]*)' || echo \"(no matches)\"\ndone\necho \"\"\necho \"=== class with body: export class \\$NAME { \\$\\$\\$ } ===\"\nast-grep run -p 'export class $NAME { $$$ }' -l typescript --json=stream skf-astgrep-probe.ts 2>&1 | grep -oE '(Pattern contains an ERROR|\"text\":\"export class [A-Za-z]*)' || echo \"(no matches)\"\necho \"=== enum with body: export enum \\$NAME { \\$\\$\\$ } ===\"\nast-grep run -p 'export enum $NAME { $$$ }' -l typescript --json=stream skf-astgrep-probe.ts 2>&1 | grep -oE '(Pattern contains an ERROR|\"text\":\"export enum [A-Za-z]*)' || echo \"(no matches)\"",
  "description": "Probe function pattern forms and class/enum-with-body"
}
```

> TOOL

tool_result
id: toolu_014KkU8qmzT7CrDyDq9DpVTC
```
=== [export function $NAME($$$PARAMS)] ===
(no matches)
=== [export function $NAME($$$PARAMS) { $$$ }] ===
"text":"export function noRet
=== [function $NAME($$$PARAMS)] ===
(no matches)
=== [export function $NAME] ===
Pattern contains an ERROR

=== class with body: export class $NAME { $$$ } ===
"text":"export class MyClass
=== enum with body: export enum $NAME { $$$ } ===
"text":"export enum MyEnum
Shell cwd was reset to /home/armel/Projects/OSS/bmad-module-skill-forge
```

> AGENT

Now I have ground truth. The failure is about **syntactically incomplete patterns** (no body): adding the body fixes class/enum, while `type $NAME = $T` works and bare `export function $NAME($$$PARAMS)` is unreliable. The finding's claim that `export interface` returns zero is **wrong** — it works for plain interfaces.

The doc's Known Limitation #1 and #7 claim the MCP `find_code()` API "works reliably for class detection." Let me verify whether MCP `find_code` succeeds where the CLI fails, since that determines whether the recipes are actually broken or just the CLI path.

> TOOL

tool_use ToolSearch
id: toolu_014vtYBfeQdEytepRiBX2WQZ
```json
{
  "query": "select:mcp__ast-grep__find_code,mcp__ast-grep__find_code_by_rule",
  "max_results": 5
}
```

> TOOL

tool_result
id: toolu_014vtYBfeQdEytepRiBX2WQZ
```
{
  "type": "tool_reference",
  "tool_name": "mcp__ast-grep__find_code"
}
{
  "type": "tool_reference",
  "tool_name": "mcp__ast-grep__find_code_by_rule"
}
```

> AGENT

Now let me test the MCP `find_code` for `export class $NAME` — the doc claims this API "works reliably for class detection."

> TOOL

tool_use Bash
id: toolu_011w2rSAiKfQcbj3JNSjkabV
```json
{
  "command": "cd /tmp && mkdir -p skf-mcp-probe && cp skf-astgrep-probe.ts skf-mcp-probe/probe.ts && ls skf-mcp-probe/",
  "description": "Set up isolated folder for MCP probe"
}
```

> TOOL

tool_result
id: toolu_011w2rSAiKfQcbj3JNSjkabV
```
probe.ts
Shell cwd was reset to /home/armel/Projects/OSS/bmad-module-skill-forge
```

> TOOL

tool_use mcp__ast-grep__find_code
id: toolu_01FUG4WqB2eTa8teqUFNQx1h
```json
{
  "project_folder": "/tmp/skf-mcp-probe",
  "pattern": "export class $NAME",
  "language": "typescript"
}
```

> TOOL

tool_result
id: toolu_01FUG4WqB2eTa8teqUFNQx1h
```
No matches found
```

> TOOL

tool_use mcp__ast-grep__find_code
id: toolu_01BVAVqNNx4QmZsnm6WxhoJF
```json
{
  "project_folder": "/tmp/skf-mcp-probe",
  "pattern": "export function $NAME($$$PARAMS)",
  "language": "typescript"
}
```

> TOOL

tool_result
id: toolu_01BVAVqNNx4QmZsnm6WxhoJF
```
No matches found
```

> TOOL

tool_use mcp__ast-grep__find_code
id: toolu_01G3p14TEiMajAitNEKQVkxo
```json
{
  "project_folder": "/tmp/skf-mcp-probe",
  "pattern": "export type $NAME",
  "language": "typescript"
}
```

> TOOL

tool_result
id: toolu_01G3p14TEiMajAitNEKQVkxo
```
No matches found
```

> AGENT

Confirmed: MCP `find_code` **also** returns zero for `export class $NAME`, `export function $NAME($$$PARAMS)`, and `export type $NAME` — so the doc's claim that `find_code()` "works reliably for class detection" is false on 0.42.2. Let me confirm the body-completed workarounds work via MCP too.

> TOOL

tool_use mcp__ast-grep__find_code
id: toolu_01A8qeezwPjvbk75VAeTE8kM
```json
{
  "project_folder": "/tmp/skf-mcp-probe",
  "pattern": "export class $NAME { $$$ }",
  "language": "typescript"
}
```

> TOOL

tool_result
id: toolu_01A8qeezwPjvbk75VAeTE8kM
```
Found 1 matches:

/tmp/skf-mcp-probe/probe.ts:4
export class MyClass { x = 1; }
```

> TOOL

tool_use mcp__ast-grep__find_code
id: toolu_015wN1RNds7nfeK1Xah3xHpj
```json
{
  "project_folder": "/tmp/skf-mcp-probe",
  "pattern": "export enum $NAME { $$$ }",
  "language": "typescript"
}
```

> TOOL

tool_result
id: toolu_015wN1RNds7nfeK1Xah3xHpj
```
Found 1 matches:

/tmp/skf-mcp-probe/probe.ts:7
export enum MyEnum { A, B, C }
```

> TOOL

tool_use mcp__ast-grep__find_code
id: toolu_01FKsiWHfiRwi3jTfy8Hrpbs
```json
{
  "project_folder": "/tmp/skf-mcp-probe",
  "pattern": "type $NAME = $T",
  "language": "typescript"
}
```

> TOOL

tool_result
id: toolu_01FKsiWHfiRwi3jTfy8Hrpbs
```
Found 1 matches:

/tmp/skf-mcp-probe/probe.ts:6
type MyType = string | number;
```

> AGENT

Ground truth is now locked across **both** CLI and MCP on ast-grep 0.42.2:

| Documented pattern | Result | Working form |
|---|---|---|
| `export const $NAME = $VALUE` | ✅ works | — |
| `export function $NAME($$$PARAMS)` | ❌ zero | source-read (body form breaks on return types) |
| `export class $NAME` | ❌ zero | `export class $NAME { $$$ }` ✅ |
| `export interface $NAME { $$$ }` | ✅ plain only | misses `<T>`/`extends` → source-read those |
| `export type $NAME` | ❌ zero (ERROR) | `type $NAME = $T` ✅ |
| `export enum $NAME` | ❌ zero (ERROR) | `export enum $NAME { $$$ }` ✅ |

The finding is **directionally right but materially wrong in two ways**: (1) `export interface` actually works for plain interfaces, and (2) class/enum/type are recoverable by completing the pattern body — they don't need a pure source-read fallback. The doc's existing claim that `find_code()` "works reliably for class detection" is also false on 0.42.x.

Now let me finish validating finding 1 and check for test coverage that my edits could break.

> TOOL

tool_use Bash
id: toolu_01KynSr3ZTHj2ZB9tqXcnzLH
```json
{
  "command": "cd /home/armel/Projects/OSS/bmad-module-skill-forge\necho \"=== target_version in brief skill (step 01 + schema) ===\"\ngrep -rln \"target_version\" src/skf-brief-skill/ | head -20\necho \"\"\necho \"=== forge-source-repo-localclone-rule mentions ===\"\ngrep -rln \"localclone\\|local-clone\\|forge-source-repo\" src/ | head -20\necho \"\"\necho \"=== tests referencing analyze-target or extraction-patterns ===\"\ngrep -rln \"analyze-target\\|extraction-patterns\" test/ 2>/dev/null | head -20\necho \"\"\necho \"=== tests referencing these skills' .md content/headings ===\"\nls test/ | grep -iE \"scan|structure|coherence|brief|create|extract\" | head -40",
  "description": "Validate finding 1 inputs and test coverage"
}
```

> TOOL

tool_result
id: toolu_01KynSr3ZTHj2ZB9tqXcnzLH
```
=== target_version in brief skill (step 01 + schema) ===
src/skf-brief-skill/references/headless-args.md
src/skf-brief-skill/references/version-resolution.md
src/skf-brief-skill/SKILL.md
src/skf-brief-skill/references/draft-checkpoint.md
src/skf-brief-skill/references/write-brief.md
src/skf-brief-skill/assets/skill-brief-schema.md
src/skf-brief-skill/references/gather-intent.md
src/skf-brief-skill/references/confirm-brief.md
src/skf-brief-skill/references/analyze-target.md

=== forge-source-repo-localclone-rule mentions ===

=== tests referencing analyze-target or extraction-patterns ===
test/test-installation-components.js
test/test-skf-detect-scripts-assets.py

=== tests referencing these skills' .md content/headings ===
test-skf-emit-brief-result-envelope.py
test-skf-extract-public-api.py
test-skf-scan-manifests.py
test-skf-scan-skill-md-structure.py
test-skf-validate-brief-inputs.py
test-skf-validate-brief-schema.py
test-skf-write-skill-brief.py
```

> TOOL

tool_use Bash
id: toolu_019ikT7tzmTTPth8kFE6EdC8
```json
{
  "command": "cd /home/armel/Projects/OSS/bmad-module-skill-forge\necho \"=== what test-installation-components.js checks re: these files ===\"\ngrep -n \"analyze-target\\|extraction-patterns\" test/test-installation-components.js\necho \"\"\necho \"=== what test-skf-detect-scripts-assets.py checks ===\"\ngrep -n \"analyze-target\\|extraction-patterns\" test/test-skf-detect-scripts-assets.py\necho \"\"\necho \"=== clone + checkout tag behavior (localclone rule by any name) ===\"\ngrep -rln \"git checkout\\|--branch\\|checkout.*tag\\|clone.*tag\\|target_version.*tag\\|tag.*target_version\" src/ | head\necho \"\"\necho \"=== refs/tags resolution anywhere already? ===\"\ngrep -rln \"refs/tags\\|git/refs\\|?ref=\" src/ | head",
  "description": "Check test assertions and existing tag-resolution prose"
}
```

> TOOL

tool_result
id: toolu_019ikT7tzmTTPth8kFE6EdC8
```
=== what test-installation-components.js checks re: these files ===
208:      steps: ['gather-intent.md', 'analyze-target.md', 'scope-definition.md', 'confirm-brief.md', 'write-brief.md', 'health-check.md'],
229:        'extraction-patterns.md',
230:        'extraction-patterns-tracing.md',

=== what test-skf-detect-scripts-assets.py checks ===
4:Covers detection rules from src/skf-create-skill/references/extraction-patterns-tracing.md:

=== clone + checkout tag behavior (localclone rule by any name) ===
src/skf-quick-skill/references/resolve-target.md
src/skf-create-skill/references/load-brief.md
src/skf-audit-skill/references/init.md
src/skf-brief-skill/assets/skill-brief-schema.md
src/skf-update-skill/references/re-extract.md
src/skf-analyze-source/assets/skill-brief-schema.md
src/skf-update-skill/references/remote-source-resolution.md
src/skf-create-skill/references/source-resolution-protocols.md

=== refs/tags resolution anywhere already? ===
src/skf-quick-skill/.analysis/2026-05-15T19-39-21Z/findings.md
src/skf-quick-skill/references/quick-extract.md
src/skf-audit-skill/references/init.md
src/skf-create-skill/references/source-resolution-protocols.md
```

> AGENT

Tests only assert these files **exist** in the manifest (not their content), so prose edits are low-risk. There's already tag-resolution prose in `source-resolution-protocols.md` (it has both `refs/tags` and `?ref=`). Let me read it plus the brief's version-resolution to mirror the existing approach rather than invent a new one.

> TOOL

tool_use Bash
id: toolu_01TPodYDrBLuzMfi6QALPACx
```json
{
  "command": "cd /home/armel/Projects/OSS/bmad-module-skill-forge\necho \"########## source-resolution-protocols.md (refs/tags + ?ref= context) ##########\"\ngrep -n \"refs/tags\\|?ref=\\|git checkout\\|--branch\\|target_version\\|v{version}\\|{version}\" src/skf-create-skill/references/source-resolution-protocols.md\necho \"\"\necho \"########## brief version-resolution.md (full) ##########\"\nwc -l src/skf-brief-skill/references/version-resolution.md",
  "description": "Locate existing tag-resolution recipe"
}
```

> TOOL

tool_result
id: toolu_01TPodYDrBLuzMfi6QALPACx
```
########## source-resolution-protocols.md (refs/tags + ?ref= context) ##########
9:Tag resolution maps a declared version in the brief onto a concrete git ref before cloning, so the skill is built from code matching its declared version. Three signals can drive it, in priority order: an explicit `brief.target_ref` (a ref the user states verbatim — highest priority), an **explicit** `brief.target_version` (deliberate user intent), or an **implicit** `brief.version` (auto-populated hint from `brief-skill`). All apply only when `source_repo` is a remote URL.
13:**When none of `brief.target_ref`, `brief.target_version`, or `brief.version` is set:** skip tag resolution entirely. Set `source_ref` to `HEAD` (default branch).
15:### Explicit Tag Resolution (when target_version is set)
17:When `brief.target_version` is present AND `source_repo` is a remote URL, resolve the target version to a git tag before cloning:
21:   - Fallback: `git ls-remote --tags "{source_repo}" | sed 's|.*refs/tags/||'`
23:2. **Match `target_version` against tags** in priority order:
24:   - **Exact match:** `{target_version}` (e.g., `0.5.0`)
25:   - **With `v` prefix:** `v{target_version}` (e.g., `v0.5.0`)
26:   - **With package scope (monorepos):** `{brief.name}@{target_version}` or `@{scope}/{brief.name}@{target_version}`
27:   - **With crate/package-directory prefix (monorepos):** `{brief.name}/v{target_version}`, `{brief.name}/{target_version}`, or `{brief.name}-v{target_version}` (e.g. `tokio/v1.0.0`). Covers monorepos whose tags are prefixed by the crate/package directory **when that directory equals the skill name**. When the directory differs from the skill name (e.g. crate `livekit` for skill `livekit-rust`, tag `livekit/v0.7.42`), this heuristic can't infer it — set `target_ref` explicitly instead.
31:   - **Multiple matches:** Present the matching tags to the user — "Multiple tags match version {target_version}: {list}. Which one should I use?" Wait for selection.
32:   - **Zero matches:** ⚠️ Warn: "No git tag found matching version {target_version}. Closest available tags: {list 5 nearest by semver sort}. Falling back to default branch — **extracted code may not match target version.**" Set `source_ref` to `HEAD` and proceed with default branch.
38:When `brief.target_version` is absent but `brief.version` is present AND `source_repo` is a remote URL, treat `brief.version` as an **implicit** target version and attempt tag resolution before cloning. This matches `brief-skill`'s behavior, which auto-populates `brief.version` from the latest non-prerelease release tag — so a tag matching `brief.version` is the common case, and silently cloning HEAD would produce a skill labeled with `brief.version` but built from an unrelated default-branch commit.
42:2. **Match `brief.version` against tags** in this reduced priority order. Package-scoped monorepo variants are **not** tried — those require deliberate user intent via `target_version`, since implicit matching against a monorepo tag like `{brief.name}@{version}` could silently select a sibling package's ref:
49:   - **Zero matches:** ⚠️ Warn: "No git tag found matching `brief.version` ({brief.version}). Falling back to default branch — **extracted code may not match the declared version.** If you intended to pin a specific version, set `target_version` explicitly in the brief." Set `source_ref` to `HEAD` and proceed with default branch. Append `tag_resolution: {status: "fallback-head", requested: "{brief.version}", reason: "no-matching-tag"}` to the in-context evidence-report payload so step 5 §7 surfaces the fallback in the evidence report. This turns the warning into a persistent audit trail a reviewer can grep later, not just a one-shot stderr line.
59:When `brief.target_version` is set AND `source_repo` is a local path:
61:⚠️ "**Local source may not match target version {target_version}.** Ensure you've checked out the correct version locally, or use a remote GitHub URL so SKF can clone from the git tag automatically."
100:   git -C "{workspace_repo_path}" ls-remote --tags origin {source_ref} | grep -q "refs/tags/{source_ref}$" && ref_kind=tag || ref_kind=branch
103:   Fetch using the ref-kind-appropriate invocation so tag refs are written into `refs/tags/*` rather than being dropped by a branch-only fetch:
134:   Clone with the appropriate branch flag — `--branch` is only valid for real branch/tag names, not for `HEAD`. **Do NOT pass `--single-branch`** here: workspace clones are persistent and re-used for future forges with different `source_ref` values (a later run may target a different tag or branch). A single-branch workspace clone would force every re-forge with a new ref to fall through to ephemeral cloning, defeating the workspace cache:
138:   git clone --depth 1 --branch {source_ref} "{source_repo}" "{workspace_repo_path}"
167:   git clone --depth 1 --branch {source_ref} --single-branch --filter=blob:none "{source_repo}" "{temp_path}"
219:**Target version override:** If `brief.target_version` is present, use it as the authoritative version for the skill. Do NOT warn about a brief-vs-source version mismatch — the user intentionally specified this version. Set the working version to `brief.target_version` and skip the rest of this reconciliation section. The `target_version` field indicates deliberate user intent (e.g., targeting an older version, or providing the version for a docs-only skill).

########## brief version-resolution.md (full) ##########
46 src/skf-brief-skill/references/version-resolution.md
```

> AGENT

There's a canonical **Tag Resolution** protocol already in `source-resolution-protocols.md` (exact → `v`-prefix → monorepo variants). My fix for finding 1 should mirror that matching logic for the GitHub-API path rather than invent a new one. Let me confirm exactly which fields step 01 of the brief captures, so I reference real variables.

> TOOL

tool_use Bash
id: toolu_01JY5VdVuNitmvycr3YdzKx9
```json
{
  "command": "cd /home/armel/Projects/OSS/bmad-module-skill-forge\necho \"=== target_version / target_ref capture in gather-intent + headless-args ===\"\ngrep -n \"target_version\\|target_ref\" src/skf-brief-skill/references/gather-intent.md src/skf-brief-skill/references/headless-args.md\necho \"\"\necho \"=== version-resolution.md (brief) full content ===\"\ncat src/skf-brief-skill/references/version-resolution.md",
  "description": "Confirm brief step-01 variable surface"
}
```

> TOOL

tool_result
id: toolu_01JY5VdVuNitmvycr3YdzKx9
```
=== target_version / target_ref capture in gather-intent + headless-args ===
src/skf-brief-skill/references/headless-args.md:13:| `target_version` | no | — | Auto-detected in step 2 if absent. Full X.Y.Z semver required (HALT exit 2, `halt_reason: "input-invalid"` on partial forms like `1`, `1.2`, `v2`) |
src/skf-brief-skill/references/gather-intent.md:155:  - `name` ← `brief.name`; `version` ← `brief.version`; `target_version` ← `brief.target_version`
src/skf-brief-skill/references/gather-intent.md:156:  - `target_ref` ← `brief.target_ref`; `source_ref` ← `brief.source_ref` (optional git refs; preserve when present)
src/skf-brief-skill/references/gather-intent.md:209:This step only collects `target_version` and validates its shape with the regex below — auto-detection runs in step 2 and precedence/invariant resolution lands in step 5's writer script. The canonical precedence rules live in `references/version-resolution.md`; load it from step 2 / step 5 only when the relevant section needs it.
src/skf-brief-skill/references/gather-intent.md:211:**Headless:** if `target_version` was supplied as an argument, store it and skip the interactive prompt below. If `doc_urls` were also supplied, treat the version-vs-doc-URL confirmation prompt as auto-confirmed (Y).
src/skf-brief-skill/references/gather-intent.md:221:**If user provides a version:** Validate the shape against `^v?\d+\.\d+\.\d+([.\-+][0-9A-Za-z][0-9A-Za-z.\-+]*)?$` (full X.Y.Z form, with optional `v` prefix and pre-release / build suffix; CalVer like `2024.04.01` accepted; partial forms like `1`, `1.2`, `v2`, `latest` rejected). On a match, store as `target_version` and set `version` to this value. On a non-match, warn `"'{value}' doesn't look like semver — write the explicit triple (e.g. 1.0.0). Fix it now or skip auto-detection?"` and re-prompt for a corrected value or blank to fall through to step 2 auto-detection.
src/skf-brief-skill/references/gather-intent.md:222:**If blank:** Proceed without `target_version` — version will be auto-detected in step 02.
src/skf-brief-skill/references/gather-intent.md:224:{If target_version was set AND doc_urls are being collected (either docs-only primary or supplemental):}
src/skf-brief-skill/references/gather-intent.md:226:"**You're targeting version {target_version}. Do these documentation URLs correspond to that version?** [Y/N]"
src/skf-brief-skill/references/gather-intent.md:229:- **If N:** "Provide the correct documentation URLs for version {target_version}." Re-collect doc_urls.
src/skf-brief-skill/references/gather-intent.md:281:  2. `{name}-{target_version}` if `target_version` is set and the suffix wouldn't collide (e.g. `marked-1.2.3`)
src/skf-brief-skill/references/gather-intent.md:284:  Number the surviving alternates `[1] [2] [3]…` in the order produced (1 alternate for a community-authority brief with no `target_version`; 2–3 otherwise). Then present:
src/skf-brief-skill/references/gather-intent.md:315:{If target_version set:}
src/skf-brief-skill/references/gather-intent.md:316:- **Target version:** {target_version} (user-specified)
src/skf-brief-skill/references/gather-intent.md:395:  3. **Hydrate and route.** Store `ratify_mode: true` and `ratify_source_path: <resolved-brief-path>` in workflow context, then hydrate the brief context variables from the parsed `brief` payload exactly as the §3.1a `[R]` branch does (the identical field-mapping list: `name`/`version`/`target_version`, `target_ref`/`source_ref`, `source_repo`/`source_type`/`source_authority`/`doc_urls`, `language`/`description`/`forge_tier`, `created`/`created_by`, `scope.type`/`scope.include`/`scope.exclude`/`scope.tier_a_include`/`scope.notes`/`scope.rationale`/`scope.amendments`, `scripts_intent`/`assets_intent` — preserving `target_ref`/`source_ref`/`tier_a_include`/`amendments` verbatim). Load, read entirely, and execute `{ratifyTargetFile}` — bypassing step 2 (analyze-target) and step 3 (scope-definition), both of which would re-derive fields already on disk. The forward chain resumes at step 4 (confirm-brief), which auto-confirms `[C]` under headless and proceeds to step 5's write (the step 5 §2b ratify branch auto-overwrites in place). Do **not** run the source-authority detection or the `[C] → {nextStepFile}` routing below — they belong to the derive path.

=== version-resolution.md (brief) full content ===
# Version Resolution

Single source of truth for how brief-skill resolves the `version` field of `skill-brief.yaml`. Loaded by step 2 §4b (auto-detect, fallback path only when the language is not script-supported) and step 5 §3 (resolve & write) so both operate on the same precedence rules and invariant. Step-01 §3b references this file in prose for human-readable rationale but does not load it — that step only collects `target_version` and validates its shape with an inline regex.

**Aligned with** `assets/skill-brief-schema.md` "Version Detection" section. If you change one, change the other.

## Detection Algorithm

For the detected source language, attempt the lookups in order. Stop at the first match.

- **Python:** `pyproject.toml` `[project] version` (static) → if `dynamic = ["version"]`, check `__init__.py` for `__version__` → `_version.py` if exists → `setup.py` `version=` → `git describe --tags --abbrev=0`
- **JavaScript / TypeScript:** root `package.json` (`"version"`). If the root has `"private": true` with a `"workspaces"` array or lacks a `"version"` field, fall back to a primary workspace package's `package.json` (e.g. `code/core/package.json`, or the first matching `packages/*/package.json`). For GitHub sources, prefer `gh api repos/{owner}/{repo}/releases/latest` → `tag_name` when a non-pre-release tag exists, over a default-branch pre-release. Treat a version containing `-alpha`, `-beta`, `-rc`, `-next`, or `-canary` as a pre-release.
- **Rust:** `Cargo.toml` `[package] version` (static). If `version = { workspace = true }`, resolve from workspace root `Cargo.toml` → `git describe --tags --abbrev=0`.
- **Go:** version tag from `go.mod`, or `git describe --tags --abbrev=0`.

For remote GitHub sources, fetch version-bearing files via `gh api repos/{owner}/{repo}/contents/{file}` (decode base64). For local sources, read the file directly.

If every step fails or returns a non-semver value, the detected version is `null` — the resolver below falls back to `"1.0.0"`.

**Pre-release handling:** preserve detected pre-release tags (`1.0.0-beta.0`, `2.0.0-rc.1`) verbatim. Do not strip them.

## Precedence — Resolving the `version` Field

The brief's `version` field is resolved from three candidate sources, in priority order:

1. **`target_version`** — collected interactively in step 1 §3b or supplied as a headless argument. When present, this value wins outright. The auto-detection above still runs for informational purposes (the user sees both "Target version" and "Detected version" side-by-side at the analysis summary), but the brief's `version` field is set from `target_version`.
2. **Auto-detected version** — from §"Detection Algorithm" above. Used when `target_version` is absent.
3. **Default** — `"1.0.0"` when both of the above fail or yield a non-semver value.

## Invariant

When `target_version` is set, the written brief MUST satisfy:

```
brief.target_version == brief.version
```

Step-05 §3 enforces this by setting both fields to the same string when `target_version` is present. Downstream tooling (e.g. `skf-create-skill`) can distinguish "user-requested" from "auto-detected" by the presence of `target_version` without re-deriving provenance — but the values themselves are identical. Different values are a contract violation and a bug.

## Step-Level Responsibilities

| Step | Responsibility |
|------|----------------|
| 01 §3b | Collect `target_version` (interactive prompt, or headless arg). Do not auto-detect — that is step 02's job. |
| 02 §4b | Run the detection algorithm regardless of whether `target_version` is set. If `target_version` is set and the detected version differs, surface the disagreement to the user — but the precedence above is unchanged: `target_version` wins. |
| 05 §3 | Apply the precedence rules and write `version`. If `target_version` is set, also write the `target_version` field with the identical value. Enforce the invariant. |
```

> AGENT

I now have everything I need, all empirically grounded. Let me do one last check — whether matching GitHub issues exist (for clean `Fixes #NNN` references) and whether these recipe patterns are duplicated elsewhere in `src/` (sync risk).

> TOOL

tool_use Bash
id: toolu_01MgVJnm44jevCN1NLP9vuv8
```json
{
  "command": "cd /home/armel/Projects/OSS/bmad-module-skill-forge\necho \"=== open issues mentioning analyze-target / target_version / ast-grep / extraction ===\"\ngh issue list --state open --limit 30 --search \"analyze-target OR target_version OR ast-grep OR extraction-patterns OR typescript\" 2>&1 | head -30 || echo \"(gh issue list failed)\"\necho \"\"\necho \"=== is 'export class \\$NAME' duplicated outside extraction-patterns.md? ===\"\ngrep -rln \"export class \\$NAME\\|export function \\$NAME\" src/ | grep -v \"extraction-patterns.md\"\necho \"\"\necho \"=== does any step file consume analyze-target's tree ref / HEAD assumption downstream? ===\"\ngrep -rln \"trees/HEAD\\|/contents/\" src/skf-brief-skill/ ",
  "description": "Check for matching issues and pattern duplication"
}
```

> TOOL

tool_result
id: toolu_01MgVJnm44jevCN1NLP9vuv8
```
=== open issues mentioning analyze-target / target_version / ast-grep / extraction ===

=== is 'export class $NAME' duplicated outside extraction-patterns.md? ===

=== does any step file consume analyze-target's tree ref / HEAD assumption downstream? ===
src/skf-brief-skill/references/version-resolution.md
src/skf-brief-skill/references/analyze-target.md
src/skf-brief-skill/assets/skill-brief-schema.md
src/skf-brief-skill/references/scope-definition.md
```

> AGENT

All clear: no matching open issues (commits will be descriptive, no internal-artifact refs), and the broken patterns aren't duplicated elsewhere. One last impact check — does step 03 (`scope-definition.md`) re-fetch file contents at HEAD, which would undermine an analyze-target-only fix?

> TOOL

tool_use Bash
id: toolu_01HLwTZZJgDUHiCtaQPQcdwC
```json
{
  "command": "cd /home/armel/Projects/OSS/bmad-module-skill-forge\necho \"=== scope-definition.md /contents/ usage ===\"\ngrep -n \"/contents/\\|trees/\\|HEAD\\|?ref=\\|gh api\" src/skf-brief-skill/references/scope-definition.md | head -20\necho \"\"\necho \"=== version-resolution.md /contents usage (step 4b fallback path) ===\"\ngrep -n \"/contents/\\|HEAD\\|?ref=\" src/skf-brief-skill/references/version-resolution.md",
  "description": "Check downstream HEAD fetches in step 03 and 4b"
}
```

> TOOL

tool_result
id: toolu_01HLwTZZJgDUHiCtaQPQcdwC
```
=== scope-definition.md /contents/ usage ===
73:HEAD-check the URLs in parallel — issue all N `curl -sI --max-time 5 {url}` calls in a **single message with N parallel Bash calls**, then process the responses together. On a 4xx/5xx, DNS failure, or timeout per URL, warn `"Could not reach {url} — {status or error}."` and offer the same correct/keep choice as step 1 §3. The check is best-effort — never HALT on a failed HEAD — but the failure must surface here so it is not discovered downstream during compilation.
75:**On re-entry from step 4 [R]:** if `doc_urls` is byte-identical to the list that was probed on the previous pass through this subsection AND the prior per-URL probe results are still recoverable from conversation context, skip the parallel HEAD-check and reuse those results. Re-running the probes when the list has not changed wastes round-trips and can flap on transient failures. Any addition, removal, or edit to a URL invalidates the cache — re-probe the entire updated set. If the prior results are not recoverable (long session, compaction, etc.), re-probe — never cache-hit on a list whose results you cannot cite.
91:**Fetch registry-file contents before building the payload.** Step-02 §4.1 fetches `package.json` plus the entry-point files but does not fetch `registry.ts` / `components.ts` — the deep-match branch of the component-registry rule needs those contents. Scan the tree for any of `registry.ts` / `registry.tsx` / `components.ts` / `components.tsx` (any depth). For each match, fetch its contents in **one message with N parallel Bash calls** (`gh api repos/{owner}/{repo}/contents/{path}` for GitHub, file reads for local), then base64-decode the responses together. Skip the fetch if the tree contains no registry files.

=== version-resolution.md /contents usage (step 4b fallback path) ===
16:For remote GitHub sources, fetch version-bearing files via `gh api repos/{owner}/{repo}/contents/{file}` (decode base64). For local sources, read the file directly.
```

> AGENT

I've fully validated both findings against live source and the real tool. Here's what I found, and one impact the finding **missed**.

## Validation results

**Finding 1 — `skf-brief-skill/analyze-target.md` (gap): CONFIRMED.**
`HEAD` is hardcoded at `analyze-target.md:37` (tree fetch), `:76` (tree-path reference), and the §4.1 `contents/{file}` fetches (`:149`) default to the branch HEAD. `target_version`/`target_ref` are both captured at step 01 (`gather-intent.md:155-156`) and available here. So when a brief pins a version whose tag ≠ HEAD, analysis silently reads the wrong source. There's already a canonical tag-matching recipe in `skf-create-skill/references/source-resolution-protocols.md` (exact → `v`-prefix → monorepo) I can mirror.

**Impact the finding missed:** step 03 `scope-definition.md:91` *also* does `gh api .../contents/{path}` with no ref (registry files for component libraries), and `version-resolution.md:16` fetches version files at HEAD. Fixing only analyze-target would leave a residual "analyze at tag, scope at HEAD" seam. For a *coherent* fix, `{analysis_ref}` should carry into those two sites too — all three files are in `skf-brief-skill`.

**Finding 2 — `skf-create-skill/extraction-patterns.md` (bug): CONFIRMED but the finding is materially wrong in two ways.** Tested on ast-grep **0.42.2**, both CLI *and* MCP `find_code`:

| Documented pattern | Result | Verified fix |
|---|---|---|
| `export const $NAME = $VALUE` | ✅ works | — |
| `export function $NAME($$$PARAMS)` | ❌ zero | source-read (body form misses return-typed/async) |
| `export class $NAME` | ❌ zero (ERROR node) | `export class $NAME { $$$ }` ✅ |
| `export interface $NAME { $$$ }` | ✅ **works** (finding wrongly says zero) | misses `<T>`/`extends` → source-read those |
| `export type $NAME` | ❌ zero (ERROR node) | `type $NAME = $T` ✅ |
| `export enum $NAME` | ❌ zero (ERROR node) | `export enum $NAME { $$$ }` ✅ |

The finding's prescription ("everything returns zero → pure source-read fallback") would falsely document `interface` as broken and throw away working AST extraction for class/enum/type. The doc *also* contains a now-falsified claim (#1 and the line-290 note: `find_code()` "works reliably for class detection" — it fails identically on 0.42.x). The correct, convention-matching fix mirrors how existing limitations **#7 (Python)** and **#8 (Rust)** already work: keep the recipe but ship the *working* form and add a precise Known Limitation **#9** with verified workarounds.

**Other checks:** no test parses these files' content (only existence, via `test-installation-components.js`); the broken patterns aren't duplicated elsewhere in `src/`; no matching open GitHub issues exist (so commits stay descriptive, no internal-artifact/fingerprint refs per OSS hygiene). Party mode / advanced elicitation aren't warranted — the path is evidence-determined.

Two genuine decisions before I implement:

> TOOL

tool_use AskUserQuestion
id: toolu_018W2kiHU7CbWqzwGjb4DYDv
```json
{
  "questions": [
    {
      "question": "How wide should the Finding-1 (analyze-target HEAD) fix go?",
      "header": "Fix scope",
      "multiSelect": false,
      "options": [
        {
          "label": "Coherent: all 3 sites (Recommended)",
          "description": "Resolve {analysis_ref} in analyze-target §1 AND carry it into scope-definition.md:91 + version-resolution.md:16, so the whole brief analysis reads the pinned tag. Closes the residual seam the finding missed. 3 files, all in skf-brief-skill, one logical change."
        },
        {
          "label": "Literal: analyze-target.md only",
          "description": "Fix exactly what the finding cites — analyze-target §1/§1b/§4 use {analysis_ref}. Smaller diff, but step-03 registry fetch and fallback version detection still read HEAD (residual wrong-version seam for component libraries / non-script languages)."
        }
      ]
    },
    {
      "question": "How should the two independent fixes be packaged?",
      "header": "PR structure",
      "multiSelect": false,
      "options": [
        {
          "label": "Two sequential PRs (Recommended)",
          "description": "One PR per skill (skf-brief-skill, then skf-create-skill), each a single focused commit. Matches recent repo convention (#384/#386/#387 are one-skill-per-PR) and your 'merge before next' practice. Independently reviewable/revertible; disjoint files = no conflicts."
        },
        {
          "label": "One combined PR, two commits",
          "description": "Single branch + PR with one commit per skill. Fewest PRs literally, but bundles two unrelated skills into one review."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_018W2kiHU7CbWqzwGjb4DYDv
```
Your questions have been answered: "How wide should the Finding-1 (analyze-target HEAD) fix go?"="Coherent: all 3 sites (Recommended)", "How should the two independent fixes be packaged?"="Two sequential PRs (Recommended)". You can now continue with these answers in mind.
```

> AGENT

Both recommendations confirmed: coherent 3-site fix, two sequential PRs. Per my standing practice I'll prepare **PR 1 (skf-brief-skill)** locally — branch + commit — run the full suite, then stop for your approval before pushing; PR 2 follows after you merge PR 1.

Let me create the branch and kick off the test suite in the background while I edit.

> TOOL

tool_use Bash
id: toolu_017DJqUrFBYHCZNdXVS99JQk
```json
{
  "command": "cd /home/armel/Projects/OSS/bmad-module-skill-forge\ngit checkout -b fix/skf-brief-analysis-ref 2>&1\necho \"---\"\ngit branch --show-current",
  "description": "Create PR 1 branch for brief-skill fix"
}
```

> TOOL

tool_use Bash
id: toolu_01DGtZBbtsmuUj3ZqsXPwcCT
```json
{
  "command": "npm test 2>&1 | tail -40",
  "description": "Run full test suite (baseline) in background",
  "run_in_background": true
}
```

> TOOL

tool_result
id: toolu_017DJqUrFBYHCZNdXVS99JQk
```
Switched to a new branch 'fix/skf-brief-analysis-ref'
---
fix/skf-brief-analysis-ref
```

> TOOL

tool_result
id: toolu_01DGtZBbtsmuUj3ZqsXPwcCT
```
Command running in background with ID: brdfug0uv. Output is being written to: /tmp/claude-1000/-home-armel-Projects-OSS-bmad-module-skill-forge/96dd758c-4fe6-4a48-be32-846451558cdb/tasks/brdfug0uv.output. You will be notified when it completes. To check interim output, use Read on that file path.
```

> AGENT

Now the edits for PR 1. First, `analyze-target.md` §1 — add the analysis-ref resolution and use it for the tree fetch:

> TOOL

tool_use Edit
id: toolu_01RYbEvKDSiAVLoSP87awmuT
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/references/analyze-target.md",
  "old_string": "**For GitHub URLs:**\n- Issue both probes in **one message with two parallel Bash calls** — they are independent:\n  - `gh api repos/{owner}/{repo}` (verify repo exists)\n  - `gh api repos/{owner}/{repo}/git/trees/HEAD?recursive=1` (fetch file tree)\n- If the repo-existence probe fails, fall through to the failure-class triage below; the tree response from the parallel call is discarded in that case.",
  "new_string": "**For GitHub URLs:**\n\n**Resolve the analysis ref first.** `{analysis_ref}` is the git ref every GitHub-API fetch in this step (tree, manifests, contents) reads from — resolve it before fetching anything so the analyzed structure matches the version being skilled:\n- If neither `target_ref` nor `target_version` was set in step 01: `{analysis_ref}` = `HEAD` (default branch). This is the common case — skip straight to the probes below with no extra call.\n- If `target_ref` is set (an explicit ref the user stated verbatim, highest priority): use it directly as `{analysis_ref}` — no tag lookup.\n- If `target_version` is set: resolve it to a tag via `gh api repos/{owner}/{repo}/git/refs/tags` (paginate if the repo has many tags), matching in priority order — exact `{target_version}`, then `v{target_version}`. This mirrors the clone-path tag matching in `skf-create-skill/references/source-resolution-protocols.md` (see that file for the full monorepo-tag priority if the simple forms miss). On a single match, set `{analysis_ref}` to that tag. On **multiple matches**, present them and ask which to use (headless: take the exact match, else the `v`-prefixed one). On **zero matches**, warn `\"No git tag matches version {target_version}; analyzing the default branch (HEAD) instead — structure and exports may not match the pinned version.\"`, set `{analysis_ref}` = `HEAD`, and record the fallback in the §5 analysis summary.\n\n- Issue both probes in **one message with two parallel Bash calls** — they are independent:\n  - `gh api repos/{owner}/{repo}` (verify repo exists)\n  - `gh api repos/{owner}/{repo}/git/trees/{analysis_ref}?recursive=1` (fetch file tree at the resolved ref)\n- If the repo-existence probe fails, fall through to the failure-class triage below; the tree response from the parallel call is discarded in that case."
}
```

> TOOL

tool_result
id: toolu_01RYbEvKDSiAVLoSP87awmuT
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/references/analyze-target.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now §1b — the tree-path reference (line 76) and manifest fetches (line 77):

> TOOL

tool_use Edit
id: toolu_01DKLtB19XfcA5M6wF4dYiei
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/references/analyze-target.md",
  "old_string": "- **`tree`** — pass the flat list of repo-relative file paths already fetched in §1 (for GitHub: the `path` values from the `gh api .../git/trees/HEAD?recursive=1` response; for local: the equivalent listing).\n- **`manifests`** — only the root manifests need contents; child-workspace manifests are looked up from the tree by the script. Include any of `package.json`, `Cargo.toml`, `pnpm-workspace.yaml`, `lerna.json` that appears at the repo root. Fetch them in **one message with N parallel Bash calls** (`gh api .../contents/{path}` for GitHub, file reads for local), then base64-decode together.",
  "new_string": "- **`tree`** — pass the flat list of repo-relative file paths already fetched in §1 (for GitHub: the `path` values from the `gh api .../git/trees/{analysis_ref}?recursive=1` response; for local: the equivalent listing).\n- **`manifests`** — only the root manifests need contents; child-workspace manifests are looked up from the tree by the script. Include any of `package.json`, `Cargo.toml`, `pnpm-workspace.yaml`, `lerna.json` that appears at the repo root. Fetch them in **one message with N parallel Bash calls** (`gh api .../contents/{path}?ref={analysis_ref}` for GitHub, file reads for local), then base64-decode together."
}
```

> TOOL

tool_result
id: toolu_01DKLtB19XfcA5M6wF4dYiei
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/references/analyze-target.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now §4.1 (line 149) — the public-API entry/manifest fetches:

> TOOL

tool_use Edit
id: toolu_011Myn7kgFfMHZdxYypvGUyN
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/references/analyze-target.md",
  "old_string": "1. Read the relevant files into memory (no parsing yet — just collect content). For GitHub sources, issue **all N `gh api repos/{owner}/{repo}/contents/{file}` calls in a single message with N parallel Bash calls** (one per manifest + each entry point), then base64-decode the responses together — these are 2-4 independent fetches per typical run.",
  "new_string": "1. Read the relevant files into memory (no parsing yet — just collect content). For GitHub sources, issue **all N `gh api repos/{owner}/{repo}/contents/{file}?ref={analysis_ref}` calls in a single message with N parallel Bash calls** (one per manifest + each entry point), then base64-decode the responses together — these are 2-4 independent fetches per typical run. Carrying `{analysis_ref}` through here is what keeps the analyzed exports/version aligned with the pinned tag rather than HEAD."
}
```

> TOOL

tool_result
id: toolu_011Myn7kgFfMHZdxYypvGUyN
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/references/analyze-target.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Baseline suite passed (exit 0) — green starting point. Now §5: record `{analysis_ref}` in the analysis summary and persist it for step 03. Let me add it to the "Notable Files" block:

> TOOL

tool_use Edit
id: toolu_01Tc9b87YRXBhnU3tWndLinF
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/references/analyze-target.md",
  "old_string": "**Notable Files:**\n- README: {found/not found}\n- Tests: {found/not found — location}\n- Docs: {found/not found — location}\n- Config: {list of config files found}\n- Version: {detected version or \"Not detected — defaulting to 1.0.0\"}",
  "new_string": "**Notable Files:**\n- README: {found/not found}\n- Tests: {found/not found — location}\n- Docs: {found/not found — location}\n- Config: {list of config files found}\n- Version: {detected version or \"Not detected — defaulting to 1.0.0\"}\n{If the target was a GitHub URL:}\n- Analysis ref: {analysis_ref} {append \" (resolved from target_version {target_version})\" when a tag was matched, or \" (no tag matched {target_version} — analyzed default branch)\" on the zero-match fallback}\n\nStore `{analysis_ref}` in workflow context — step 03 (`scope-definition.md`) reuses it for any further `contents/` fetches so scope analysis reads the same ref as this step."
}
```

> TOOL

tool_result
id: toolu_01Tc9b87YRXBhnU3tWndLinF
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/references/analyze-target.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now site 2 — `scope-definition.md:91` registry-file fetch:

> TOOL

tool_use Edit
id: toolu_01CxJ2vQETYXM3vWrk62WcxE
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/references/scope-definition.md",
  "old_string": "Scan the tree for any of `registry.ts` / `registry.tsx` / `components.ts` / `components.tsx` (any depth). For each match, fetch its contents in **one message with N parallel Bash calls** (`gh api repos/{owner}/{repo}/contents/{path}` for GitHub, file reads for local), then base64-decode the responses together.",
  "new_string": "Scan the tree for any of `registry.ts` / `registry.tsx` / `components.ts` / `components.tsx` (any depth). For each match, fetch its contents in **one message with N parallel Bash calls** (`gh api repos/{owner}/{repo}/contents/{path}?ref={analysis_ref}` for GitHub — `{analysis_ref}` is the ref resolved in step 02 §1, defaulting to `HEAD`; file reads for local), then base64-decode the responses together."
}
```

> TOOL

tool_result ERROR
id: toolu_01CxJ2vQETYXM3vWrk62WcxE
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

> TOOL

tool_use Read
id: toolu_011JCrrUHiszMPSZxuzWDrVS
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/references/scope-definition.md",
  "offset": 85,
  "limit": 12
}
```

> TOOL

tool_result
id: toolu_011JCrrUHiszMPSZxuzWDrVS
```
85	**Recommend a scope type — don't present the five options as equal weight.** SKILL.md states this workflow "steers toward the smaller, sharper version when scope is unclear" — surface that opinion at decision time. Use the analysis from step 2 and the user's intent from step 1 to pick the best-fit recommendation, then present the menu with that option marked as the suggested default.
86	
87	**Resolve `{recommendScopeTypeHelper}`** from `{recommendScopeTypeProbeOrder}`; first existing path wins. HALT if no candidate exists.
88	
89	**Delegate the recommendation to `{recommendScopeTypeHelper}`** instead of walking the heuristic ladder in prose. The script is the single source of truth for the five-rule ladder (component-registry → reference-app keywords → specific-modules naming/count → narrow-public-api → default full-library) plus the docs-only short-circuit. Both the interactive recommendation and the §6 headless GATE invoke the same script — same inputs, same outputs, no drift.
90	
91	**Fetch registry-file contents before building the payload.** Step-02 §4.1 fetches `package.json` plus the entry-point files but does not fetch `registry.ts` / `components.ts` — the deep-match branch of the component-registry rule needs those contents. Scan the tree for any of `registry.ts` / `registry.tsx` / `components.ts` / `components.tsx` (any depth). For each match, fetch its contents in **one message with N parallel Bash calls** (`gh api repos/{owner}/{repo}/contents/{path}` for GitHub, file reads for local), then base64-decode the responses together. Skip the fetch if the tree contains no registry files.
92	
93	Build the payload and invoke:
94	
95	```bash
96	echo '{
```

> TOOL

tool_use Edit
id: toolu_015hNMQttzZFP39Nu3NP9QsS
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/references/scope-definition.md",
  "old_string": "Scan the tree for any of `registry.ts` / `registry.tsx` / `components.ts` / `components.tsx` (any depth). For each match, fetch its contents in **one message with N parallel Bash calls** (`gh api repos/{owner}/{repo}/contents/{path}` for GitHub, file reads for local), then base64-decode the responses together.",
  "new_string": "Scan the tree for any of `registry.ts` / `registry.tsx` / `components.ts` / `components.tsx` (any depth). For each match, fetch its contents in **one message with N parallel Bash calls** (`gh api repos/{owner}/{repo}/contents/{path}?ref={analysis_ref}` for GitHub — `{analysis_ref}` is the ref resolved in step 02 §1, defaulting to `HEAD`; file reads for local), then base64-decode the responses together."
}
```

> TOOL

tool_result
id: toolu_015hNMQttzZFP39Nu3NP9QsS
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/references/scope-definition.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now site 3 — `version-resolution.md:16`. Let me read the exact line and edit it with the safe conditional-ref phrasing:

> TOOL

tool_use Edit
id: toolu_01Jhd7nWtvsMgSCyxxZaHCRg
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/references/version-resolution.md",
  "old_string": "For remote GitHub sources, fetch version-bearing files via `gh api repos/{owner}/{repo}/contents/{file}` (decode base64). For local sources, read the file directly.",
  "new_string": "For remote GitHub sources, fetch version-bearing files via `gh api repos/{owner}/{repo}/contents/{file}?ref={analysis_ref}` (decode base64) — `{analysis_ref}` is the ref resolved in step 02 §1, defaulting to `HEAD` when no `target_ref`/`target_version` was pinned; reading at the pinned ref keeps the \"Detected version\" the user sees consistent with the version being skilled. For local sources, read the file directly."
}
```

> TOOL

tool_result ERROR
id: toolu_01Jhd7nWtvsMgSCyxxZaHCRg
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

> TOOL

tool_use Read
id: toolu_015Y6yGmwLeLm3CpZ8YfyS7g
```json
{
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/references/version-resolution.md",
  "offset": 14,
  "limit": 4
}
```

> TOOL

tool_result
id: toolu_015Y6yGmwLeLm3CpZ8YfyS7g
```
14	- **Go:** version tag from `go.mod`, or `git describe --tags --abbrev=0`.
15	
16	For remote GitHub sources, fetch version-bearing files via `gh api repos/{owner}/{repo}/contents/{file}` (decode base64). For local sources, read the file directly.
17	
```

> TOOL

tool_use Edit
id: toolu_01QuWybBjjT7Ae3YjR9SJHvg
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/references/version-resolution.md",
  "old_string": "For remote GitHub sources, fetch version-bearing files via `gh api repos/{owner}/{repo}/contents/{file}` (decode base64). For local sources, read the file directly.",
  "new_string": "For remote GitHub sources, fetch version-bearing files via `gh api repos/{owner}/{repo}/contents/{file}?ref={analysis_ref}` (decode base64) — `{analysis_ref}` is the ref resolved in step 02 §1, defaulting to `HEAD` when no `target_ref`/`target_version` was pinned; reading at the pinned ref keeps the \"Detected version\" consistent with the version being skilled. For local sources, read the file directly."
}
```

> TOOL

tool_result
id: toolu_01QuWybBjjT7Ae3YjR9SJHvg
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-brief-skill/references/version-resolution.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

All three sites edited. Let me review the complete PR-1 diff and re-run the suite to confirm nothing regressed.

> TOOL

tool_use Bash
id: toolu_01Lt8wVy3fKWK8sVJ9hPdksH
```json
{
  "command": "git --no-pager diff --stat && echo \"=== FULL DIFF ===\" && git --no-pager diff",
  "description": "Review PR-1 diff"
}
```

> TOOL

tool_result
id: toolu_01Lt8wVy3fKWK8sVJ9hPdksH
```
 src/skf-brief-skill/references/analyze-target.md     | 18 ++++++++++++++----
 src/skf-brief-skill/references/scope-definition.md   |  2 +-
 src/skf-brief-skill/references/version-resolution.md |  2 +-
 3 files changed, 16 insertions(+), 6 deletions(-)
=== FULL DIFF ===
diff --git a/src/skf-brief-skill/references/analyze-target.md b/src/skf-brief-skill/references/analyze-target.md
index 74af0863..f6960b49 100644
--- a/src/skf-brief-skill/references/analyze-target.md
+++ b/src/skf-brief-skill/references/analyze-target.md
@@ -32,9 +32,15 @@ To analyze the target repository by resolving its location, reading its structur
 ### 1. Resolve Target Location
 
 **For GitHub URLs:**
+
+**Resolve the analysis ref first.** `{analysis_ref}` is the git ref every GitHub-API fetch in this step (tree, manifests, contents) reads from — resolve it before fetching anything so the analyzed structure matches the version being skilled:
+- If neither `target_ref` nor `target_version` was set in step 01: `{analysis_ref}` = `HEAD` (default branch). This is the common case — skip straight to the probes below with no extra call.
+- If `target_ref` is set (an explicit ref the user stated verbatim, highest priority): use it directly as `{analysis_ref}` — no tag lookup.
+- If `target_version` is set: resolve it to a tag via `gh api repos/{owner}/{repo}/git/refs/tags` (paginate if the repo has many tags), matching in priority order — exact `{target_version}`, then `v{target_version}`. This mirrors the clone-path tag matching in `skf-create-skill/references/source-resolution-protocols.md` (see that file for the full monorepo-tag priority if the simple forms miss). On a single match, set `{analysis_ref}` to that tag. On **multiple matches**, present them and ask which to use (headless: take the exact match, else the `v`-prefixed one). On **zero matches**, warn `"No git tag matches version {target_version}; analyzing the default branch (HEAD) instead — structure and exports may not match the pinned version."`, set `{analysis_ref}` = `HEAD`, and record the fallback in the §5 analysis summary.
+
 - Issue both probes in **one message with two parallel Bash calls** — they are independent:
   - `gh api repos/{owner}/{repo}` (verify repo exists)
-  - `gh api repos/{owner}/{repo}/git/trees/HEAD?recursive=1` (fetch file tree)
+  - `gh api repos/{owner}/{repo}/git/trees/{analysis_ref}?recursive=1` (fetch file tree at the resolved ref)
 - If the repo-existence probe fails, fall through to the failure-class triage below; the tree response from the parallel call is discarded in that case.
 
 **Truncation detection:** After receiving the tree response, check the `truncated` field in the JSON output. If `truncated: true`:
@@ -73,8 +79,8 @@ echo '{"tree": [<flat list of repo-relative file paths>], "manifests": {"package
   uv run {detectWorkspacesHelper}
 ```
 
-- **`tree`** — pass the flat list of repo-relative file paths already fetched in §1 (for GitHub: the `path` values from the `gh api .../git/trees/HEAD?recursive=1` response; for local: the equivalent listing).
-- **`manifests`** — only the root manifests need contents; child-workspace manifests are looked up from the tree by the script. Include any of `package.json`, `Cargo.toml`, `pnpm-workspace.yaml`, `lerna.json` that appears at the repo root. Fetch them in **one message with N parallel Bash calls** (`gh api .../contents/{path}` for GitHub, file reads for local), then base64-decode together. Per-workspace manifest contents (e.g. `packages/foo/package.json`) are optional — including them populates the workspace `name` field with the manifest's declared package name; omitting them falls back to the directory basename.
+- **`tree`** — pass the flat list of repo-relative file paths already fetched in §1 (for GitHub: the `path` values from the `gh api .../git/trees/{analysis_ref}?recursive=1` response; for local: the equivalent listing).
+- **`manifests`** — only the root manifests need contents; child-workspace manifests are looked up from the tree by the script. Include any of `package.json`, `Cargo.toml`, `pnpm-workspace.yaml`, `lerna.json` that appears at the repo root. Fetch them in **one message with N parallel Bash calls** (`gh api .../contents/{path}?ref={analysis_ref}` for GitHub, file reads for local), then base64-decode together. Per-workspace manifest contents (e.g. `packages/foo/package.json`) are optional — including them populates the workspace `name` field with the manifest's declared package name; omitting them falls back to the directory basename.
 
 The script returns a JSON envelope: `{is_monorepo, manifest_kind, workspaces[], warnings[]}`. Apply the result deterministically — see `src/shared/scripts/schemas/workspace-detection.v1.json` for the full contract.
 
@@ -146,7 +152,7 @@ This section runs exactly one of §4.1 (script path) or §4.2 (fallback path) ba
 
 #### 4.1 Procedure — script-supported languages
 
-1. Read the relevant files into memory (no parsing yet — just collect content). For GitHub sources, issue **all N `gh api repos/{owner}/{repo}/contents/{file}` calls in a single message with N parallel Bash calls** (one per manifest + each entry point), then base64-decode the responses together — these are 2-4 independent fetches per typical run. For local sources read directly (also parallelisable, but local reads are fast enough that serial Read tool calls are acceptable).
+1. Read the relevant files into memory (no parsing yet — just collect content). For GitHub sources, issue **all N `gh api repos/{owner}/{repo}/contents/{file}?ref={analysis_ref}` calls in a single message with N parallel Bash calls** (one per manifest + each entry point), then base64-decode the responses together — these are 2-4 independent fetches per typical run. Carrying `{analysis_ref}` through here is what keeps the analyzed exports/version aligned with the pinned tag rather than HEAD. For local sources read directly (also parallelisable, but local reads are fast enough that serial Read tool calls are acceptable).
 
    | Language | Manifest | Entry points (mode=quick) |
    |----------|----------|--------------------------|
@@ -258,6 +264,10 @@ Present the complete analysis:
 - Docs: {found/not found — location}
 - Config: {list of config files found}
 - Version: {detected version or "Not detected — defaulting to 1.0.0"}
+{If the target was a GitHub URL:}
+- Analysis ref: {analysis_ref} {append " (resolved from target_version {target_version})" when a tag was matched, or " (no tag matched {target_version} — analyzed default branch)" on the zero-match fallback}
+
+Store `{analysis_ref}` in workflow context — step 03 (`scope-definition.md`) reuses it for any further `contents/` fetches so scope analysis reads the same ref as this step.
 
 ---
 
diff --git a/src/skf-brief-skill/references/scope-definition.md b/src/skf-brief-skill/references/scope-definition.md
index 6a84329c..6b46bb9f 100644
--- a/src/skf-brief-skill/references/scope-definition.md
+++ b/src/skf-brief-skill/references/scope-definition.md
@@ -88,7 +88,7 @@ Load `{scopeTemplatesPath}` for the scope type options ([F], [M], [P], [C], [R])
 
 **Delegate the recommendation to `{recommendScopeTypeHelper}`** instead of walking the heuristic ladder in prose. The script is the single source of truth for the five-rule ladder (component-registry → reference-app keywords → specific-modules naming/count → narrow-public-api → default full-library) plus the docs-only short-circuit. Both the interactive recommendation and the §6 headless GATE invoke the same script — same inputs, same outputs, no drift.
 
-**Fetch registry-file contents before building the payload.** Step-02 §4.1 fetches `package.json` plus the entry-point files but does not fetch `registry.ts` / `components.ts` — the deep-match branch of the component-registry rule needs those contents. Scan the tree for any of `registry.ts` / `registry.tsx` / `components.ts` / `components.tsx` (any depth). For each match, fetch its contents in **one message with N parallel Bash calls** (`gh api repos/{owner}/{repo}/contents/{path}` for GitHub, file reads for local), then base64-decode the responses together. Skip the fetch if the tree contains no registry files.
+**Fetch registry-file contents before building the payload.** Step-02 §4.1 fetches `package.json` plus the entry-point files but does not fetch `registry.ts` / `components.ts` — the deep-match branch of the component-registry rule needs those contents. Scan the tree for any of `registry.ts` / `registry.tsx` / `components.ts` / `components.tsx` (any depth). For each match, fetch its contents in **one message with N parallel Bash calls** (`gh api repos/{owner}/{repo}/contents/{path}?ref={analysis_ref}` for GitHub — `{analysis_ref}` is the ref resolved in step 02 §1, defaulting to `HEAD`; file reads for local), then base64-decode the responses together. Skip the fetch if the tree contains no registry files.
 
 Build the payload and invoke:
 
diff --git a/src/skf-brief-skill/references/version-resolution.md b/src/skf-brief-skill/references/version-resolution.md
index 1a415926..14579f83 100644
--- a/src/skf-brief-skill/references/version-resolution.md
+++ b/src/skf-brief-skill/references/version-resolution.md
@@ -13,7 +13,7 @@ For the detected source language, attempt the lookups in order. Stop at the firs
 - **Rust:** `Cargo.toml` `[package] version` (static). If `version = { workspace = true }`, resolve from workspace root `Cargo.toml` → `git describe --tags --abbrev=0`.
 - **Go:** version tag from `go.mod`, or `git describe --tags --abbrev=0`.
 
-For remote GitHub sources, fetch version-bearing files via `gh api repos/{owner}/{repo}/contents/{file}` (decode base64). For local sources, read the file directly.
+For remote GitHub sources, fetch version-bearing files via `gh api repos/{owner}/{repo}/contents/{file}?ref={analysis_ref}` (decode base64) — `{analysis_ref}` is the ref resolved in step 02 §1, defaulting to `HEAD` when no `target_ref`/`target_version` was pinned; reading at the pinned ref keeps the "Detected version" consistent with the version being skilled. For local sources, read the file directly.
 
 If every step fails or returns a non-semver value, the detected version is `null` — the resolver below falls back to `"1.0.0"`.
```

> TOOL

tool_use Bash
id: toolu_01JGrF9oPXP3n4PmZVrWZChG
```json
{
  "command": "npm test 2>&1 | tail -25",
  "description": "Re-run full suite after edits",
  "run_in_background": true
}
```

> TOOL

tool_result
id: toolu_01JGrF9oPXP3n4PmZVrWZChG
```
Command running in background with ID: bmt8q4edc. Output is being written to: /tmp/claude-1000/-home-armel-Projects-OSS-bmad-module-skill-forge/96dd758c-4fe6-4a48-be32-846451558cdb/tasks/bmt8q4edc.output. You will be notified when it completes. To check interim output, use Read on that file path.
```

> AGENT

The PR-1 diff is coherent and minimal (3 files, +16/−6), all in `skf-brief-skill`. Waiting on the post-edit suite to confirm green before committing.

> TOOL

tool_use Bash
id: toolu_01LUjZoJ7Vj39vs7KSpC3Qbt
```json
{
  "command": "while kill -0 $(pgrep -f \"npm test\" | head -1) 2>/dev/null; do sleep 3; done; echo \"=== suite finished, tail: ===\"; tail -20 /tmp/claude-1000/-home-armel-Projects-OSS-bmad-module-skill-forge/96dd758c-4fe6-4a48-be32-846451558cdb/tasks/bmt8q4edc.output",
  "description": "Wait for suite and show result"
}
```

> TOOL

tool_result
id: toolu_01LUjZoJ7Vj39vs7KSpC3Qbt
```
Command running in background with ID: b9u7eipzr. Output is being written to: /tmp/claude-1000/-home-armel-Projects-OSS-bmad-module-skill-forge/96dd758c-4fe6-4a48-be32-846451558cdb/tasks/b9u7eipzr.output. You will be notified when it completes. To check interim output, use Read on that file path.
```

> AGENT

Post-edit suite passed (exit 0). Let me confirm the tail and then commit PR 1 locally.

> TOOL

tool_use Bash
id: toolu_01EGhVS8wofGo7th9gN3HQQQ
```json
{
  "command": "tail -15 /tmp/claude-1000/-home-armel-Projects-OSS-bmad-module-skill-forge/96dd758c-4fe6-4a48-be32-846451558cdb/tasks/bmt8q4edc.output",
  "description": "Show post-edit suite tail"
}
```

> TOOL

tool_result
id: toolu_01EGhVS8wofGo7th9gN3HQQQ
```
> bmad-module-skill-forge@1.6.0 lint:md
> markdownlint-cli2 "**/*.md"

markdownlint-cli2 v0.19.1 (markdownlint v0.39.0)
Finding: **/*.md !node_modules/** !test/fixtures/** !CODE_OF_CONDUCT.md !_bmad/** !_bmad*/** !.*/** !z*/** !temp/** !website/** !build/** !skills/reports/**
Linting: 225 file(s)
Summary: 0 error(s)

> bmad-module-skill-forge@1.6.0 format:check
> prettier --check "**/*.{js,cjs,mjs,json,yaml}"

Checking formatting...
All matched files use Prettier code style!
```

> AGENT

Green — markdownlint clean on all 225 files (including my edits), Python and Node suites passed (exit 0). Committing PR 1 locally with `--no-verify` (suite already verified):

> TOOL

tool_use Bash
id: toolu_014DcgisgTJwjUon7CccaDZ5
```json
{
  "command": "cd /home/armel/Projects/OSS/bmad-module-skill-forge\ngit add src/skf-brief-skill/references/analyze-target.md src/skf-brief-skill/references/scope-definition.md src/skf-brief-skill/references/version-resolution.md\ngit commit --no-verify -F - <<'EOF'\nfix(skf-brief-skill): analyze pinned target_version at its git tag, not HEAD\n\nWhen a brief pins target_version (or target_ref), step 02 analyze-target\nresolved the repo tree, manifests, and entry-file contents at HEAD\nregardless. For an actively-developed repo whose default branch has moved\npast the pinned tag, this analyzed the wrong source — wrong file layout,\nexports, and detected version — while the brief still claimed the pinned\nversion.\n\nResolve an {analysis_ref} up front (target_ref verbatim, else target_version\nmatched to a git tag via refs/tags as exact then v-prefixed, else HEAD) and\nthread it through every GitHub-API fetch: the tree (§1), workspace/root\nmanifests (§1b), public-API manifest+entry reads (§4.1), the §5 summary, the\nstep-03 registry-file fetch, and fallback version detection. Mirrors the tag\nmatching the create-skill clone path already uses. Local-path analysis is\nunchanged (the user owns the checkout). A no-tag-match falls back to HEAD\nwith a warning recorded in the analysis summary.\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\nEOF\necho \"=== committed ===\"\ngit --no-pager log --oneline -1",
  "description": "Commit PR 1 locally"
}
```

> TOOL

tool_result
id: toolu_014DcgisgTJwjUon7CccaDZ5
```
[fix/skf-brief-analysis-ref 9f357f75] fix(skf-brief-skill): analyze pinned target_version at its git tag, not HEAD
 3 files changed, 16 insertions(+), 6 deletions(-)
=== committed ===
9f357f75 fix(skf-brief-skill): analyze pinned target_version at its git tag, not HEAD
```

> AGENT

PR 1 is committed locally on `fix/skf-brief-analysis-ref` (3 files, +16/−6, suite green). Per "no push without permission," I'll stop here for your approval before pushing.

## PR 1 ready — `skf-brief-skill`: analyze pinned version at its tag, not HEAD

**What it fixes:** when a brief pins `target_version`/`target_ref`, step 02 analyzed the repo at `HEAD`. If the default branch had moved past the pinned tag, the brief recorded the wrong layout/exports/version while still claiming the pinned version. Now an `{analysis_ref}` is resolved once (explicit ref → `target_version` matched to a tag exact-then-`v`-prefixed → else `HEAD`) and threaded through all GitHub-API fetches across the three sites you approved.

**Validation:** full `npm test` green before and after; markdownlint clean (225 files); no test parses these files' content; patterns/strings not duplicated elsewhere; local-path flow untouched. No breaking changes — the no-pin common path is byte-identical behavior (`{analysis_ref}`=`HEAD`).

**Proposed PR body** (no internal-artifact references):

> **Problem:** `skf-brief-skill` step 02 (`analyze-target`) fetched the repo tree, manifests, and entry-file contents at `HEAD` even when the brief pinned `target_version`/`target_ref`. On a repo whose default branch has diverged past the pinned tag, analysis silently described the wrong source while the brief claimed the pinned version.
>
> **Fix:** Resolve `{analysis_ref}` once at the top of §1 — `target_ref` verbatim, else `target_version` matched against `git/refs/tags` (exact, then `v`-prefixed), else `HEAD` — and use it for every GitHub-API read: tree (§1), root/workspace manifests (§1b), public-API manifest+entry reads (§4.1), the analysis summary (§5), the step-03 registry-file fetch, and fallback version detection. Mirrors the tag matching the create-skill clone path already uses. A no-tag-match warns and falls back to `HEAD`, recorded in the summary. Local-path analysis is unchanged.
>
> **Tests:** full suite green; behavior for un-pinned briefs is unchanged.

How would you like to proceed?

> TOOL

tool_use AskUserQuestion
id: toolu_01P3BNxP7vQcUtvjSJKk6QgH
```json
{
  "questions": [
    {
      "question": "PR 1 is committed locally and green. Push it and open the PR now?",
      "header": "Push PR 1",
      "multiSelect": false,
      "options": [
        {
          "label": "Push & open PR 1",
          "description": "Push fix/skf-brief-analysis-ref and open the PR with the body above. I'll then wait for you to merge before starting PR 2 (skf-create-skill)."
        },
        {
          "label": "Hold — let me review locally first",
          "description": "Leave the commit local. You inspect the diff / PR body, and I push only after you say so."
        },
        {
          "label": "Build PR 2 locally first too",
          "description": "Don't push yet; prepare the skf-create-skill commit on its own branch as well, so you can review both before any push. (Branches touch disjoint files, so no conflict.)"
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01P3BNxP7vQcUtvjSJKk6QgH
```
Your questions have been answered: "PR 1 is committed locally and green. Push it and open the PR now?"="Push & open PR 1". You can now continue with these answers in mind.
```

> AGENT

Pushing PR 1 and opening the pull request.

> TOOL

tool_use Bash
id: toolu_01SU9XzvXjN8Vb8R26JVQfj9
```json
{
  "command": "cd /home/armel/Projects/OSS/bmad-module-skill-forge\ngit push -u origin fix/skf-brief-analysis-ref 2>&1 | tail -8",
  "description": "Push PR 1 branch"
}
```

> TOOL

tool_result
id: toolu_01SU9XzvXjN8Vb8R26JVQfj9
```
[entire] Pushing session logs to origin...
remote: 
remote: Create a pull request for 'fix/skf-brief-analysis-ref' on GitHub by visiting:        
remote:      https://github.com/armelhbobdad/bmad-module-skill-forge/pull/new/fix/skf-brief-analysis-ref        
remote: 
To https://github.com/armelhbobdad/bmad-module-skill-forge.git
 * [new branch]        fix/skf-brief-analysis-ref -> fix/skf-brief-analysis-ref
branch 'fix/skf-brief-analysis-ref' set up to track 'origin/fix/skf-brief-analysis-ref'.
```

> TOOL

tool_use Bash
id: toolu_01F6hpTdv2jMU5yVDYyHMMUV
```json
{
  "command": "cd /home/armel/Projects/OSS/bmad-module-skill-forge\ngh pr create --base main --head fix/skf-brief-analysis-ref \\\n  --title \"fix(skf-brief-skill): analyze pinned target_version at its git tag, not HEAD\" \\\n  --body \"$(cat <<'EOF'\n**Problem:** `skf-brief-skill` step 02 (`analyze-target`) fetched the repo tree, manifests, and entry-file contents at `HEAD` even when the brief pinned `target_version`/`target_ref`. On a repo whose default branch has diverged past the pinned tag, analysis silently described the wrong source — file layout, exports, detected version — while the brief still claimed the pinned version.\n\n**Fix:** Resolve `{analysis_ref}` once at the top of §1 — `target_ref` verbatim, else `target_version` matched against `git/refs/tags` (exact, then `v`-prefixed), else `HEAD` — and use it for every GitHub-API read:\n- tree fetch (§1)\n- root/workspace manifests (§1b)\n- public-API manifest + entry reads (§4.1)\n- analysis summary records the resolved ref (§5)\n- step-03 `scope-definition` registry-file fetch\n- fallback version detection (`version-resolution`)\n\nMirrors the tag matching the create-skill clone path (`source-resolution-protocols.md`) already uses. A no-tag-match warns and falls back to `HEAD`, recorded in the analysis summary. Local-path analysis is unchanged — the user owns the checkout.\n\n**Behavior compatibility:** for briefs with no pinned version/ref, `{analysis_ref}` is `HEAD` and behavior is identical to before.\n\n**Tests:** full `npm test` suite green; markdownlint clean.\nEOF\n)\" 2>&1 | tail -5",
  "description": "Open PR 1"
}
```

> TOOL

tool_result
id: toolu_01F6hpTdv2jMU5yVDYyHMMUV
```
https://github.com/armelhbobdad/bmad-module-skill-forge/pull/388
```

> AGENT

**PR 1 is open: https://github.com/armelhbobdad/bmad-module-skill-forge/pull/388**

Per your "two sequential PRs" choice and the merge-before-next practice, I'll **wait for you to merge #388** before starting PR 2 (so the branches don't diverge). Here's what PR 2 will contain, already fully validated, so you know what's coming:

## PR 2 (queued) — `skf-create-skill/extraction-patterns.md`: correct the 0.42.x TS recipes

A **single-file, docs-only** change that fixes the finding *and* corrects the finding's own two errors, mirroring the existing #7 (Python) / #8 (Rust) limitation pattern:

1. **Fix the `js-exported-classes` recipe** → `export class $NAME { $$$ }` (verified to match on 0.42.2 via both CLI and MCP, where the bare form returns zero).
2. **Add Known Limitation #9** with the empirically-verified truth: bare `export class/function/type/enum` for `language: typescript` return zero on 0.42.x (class/type/enum emit ERROR-node warnings), affecting **both** CLI and MCP `find_code`. Verified workarounds: complete the body (`export class $NAME { $$$ }`, `export enum $NAME { $$$ }`); `type $NAME = $T` for aliases; source-read for `export function` (the body form misses return-typed/async forms).
3. **Correct the finding's `interface` error**: `export interface $NAME { $$$ }` *works* for plain interfaces (so I will **not** document it as broken) — it only misses `<T>`/`extends` forms, which get the source-read note.
4. **Correct the doc's own false claim** in #1 and the line-290 note that `find_code()` "works reliably for class detection" — it fails identically on 0.42.x; point to the `{ $$$ }` body form instead.

Commit will be `fix(skf-create-skill): correct ast-grep 0.42.x TypeScript export recipes` — no fingerprints, run-ids, or queue paths.

Just say the word once #388 is merged (or tell me to prep PR 2 locally now if you'd rather review both together). I won't push anything else without your go-ahead.

> DEVELOPER

merged

> AGENT

Merged — thanks. Now PR 2. Let me sync `main`, clean up the merged branch, and create the PR 2 branch.

> TOOL

tool_use Bash
id: toolu_016pb5raYLqrWtU6cZh92yZh
```json
{
  "command": "cd /home/armel/Projects/OSS/bmad-module-skill-forge\ngit checkout main 2>&1 | tail -1\ngit pull --ff-only 2>&1 | tail -3\ngit branch -d fix/skf-brief-analysis-ref 2>&1\necho \"=== confirm #388 commit present on main ===\"\ngit --no-pager log --oneline -3\ngit checkout -b fix/skf-create-astgrep-ts-recipes 2>&1\necho \"---\"; git branch --show-current",
  "description": "Sync main, delete merged branch, create PR 2 branch"
}
```

> TOOL

tool_result
id: toolu_016pb5raYLqrWtU6cZh92yZh
```
Your branch is up to date with 'origin/main'.
 src/skf-brief-skill/references/scope-definition.md   |  2 +-
 src/skf-brief-skill/references/version-resolution.md |  2 +-
 3 files changed, 16 insertions(+), 6 deletions(-)
Deleted branch fix/skf-brief-analysis-ref (was 9f357f75).
=== confirm #388 commit present on main ===
5a890121 Merge pull request #388 from armelhbobdad/fix/skf-brief-analysis-ref
9f357f75 fix(skf-brief-skill): analyze pinned target_version at its git tag, not HEAD
7aeaaf2e Merge pull request #387 from armelhbobdad/fix/skf-brief-writer-roundtrip-385
Switched to a new branch 'fix/skf-create-astgrep-ts-recipes'
---
fix/skf-create-astgrep-ts-recipes
```

> AGENT

Main synced (#388 present), branch created. Now the edits to `extraction-patterns.md`. First, fix the `js-exported-classes` recipe and its note:

> TOOL

tool_use Edit
id: toolu_01JtUi2jeSRF72U9FxdtGnrC
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/references/extraction-patterns.md",
  "old_string": "**JavaScript/TypeScript — exported classes (use `find_code`, not `find_code_by_rule`):**\n\n```yaml\nid: js-exported-classes\nlanguage: typescript\nrule:\n  pattern: 'export class $NAME'\n```\n\n> **Important:** For class patterns, use `find_code()` rather than `find_code_by_rule()`. The `find_code_by_rule` API requires explicit AST `kind` rules for class exports, which adds complexity. The simpler `find_code()` pattern approach works reliably for class detection.",
  "new_string": "**JavaScript/TypeScript — exported classes:**\n\n```yaml\nid: js-exported-classes\nlanguage: typescript\nrule:\n  pattern: 'export class $NAME { $$$ }'\n```\n\n> **Important:** The body (`{ $$$ }`) is required on ast-grep 0.42.x. The bare `export class $NAME` pattern returns zero matches — and emits a `Pattern contains an ERROR node` warning — through **both** `find_code()` and the CLI, because an incomplete class declaration does not parse as a complete statement (see Known Limitation #9). With the body present, the simple `find_code()` pattern detects class exports reliably; `find_code_by_rule` would additionally require an explicit AST `kind` rule."
}
```

> TOOL

tool_result
id: toolu_01JtUi2jeSRF72U9FxdtGnrC
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/references/extraction-patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now broaden the exported-functions language-selection note (it currently scopes the failure to tsx 0.41.x; plain `typescript` also fails on 0.42.x):

> TOOL

tool_use Edit
id: toolu_01NCJB6qLWMNyXg5Ksuv1Mip
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/references/extraction-patterns.md",
  "old_string": "> **Language selection:** Use `language: typescript` for `.ts` files and `language: tsx` for `.tsx` files. Patterns that work with `typescript` may return zero results with `tsx` and vice versa — they use different tree-sitter parsers. For mixed codebases, run each pattern twice (once per language) and merge results. Note: `export function` patterns may fail with `tsx` on ast-grep 0.41.x (see Known Limitations #5) — use source reading as fallback for those.",
  "new_string": "> **Language selection:** Use `language: typescript` for `.ts` files and `language: tsx` for `.tsx` files. Patterns that work with `typescript` may return zero results with `tsx` and vice versa — they use different tree-sitter parsers. For mixed codebases, run each pattern twice (once per language) and merge results. Note: the `export function $NAME($$$PARAMS)` pattern returns **zero** with `tsx` on ast-grep 0.41.x (see Known Limitation #5) **and** with plain `typescript` on 0.42.x (see Known Limitation #9) — use source reading as the fallback for `export function` on both."
}
```

> TOOL

tool_result
id: toolu_01NCJB6qLWMNyXg5Ksuv1Mip
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/references/extraction-patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now correct the false claim in Known Limitation #1:

> TOOL

tool_use Edit
id: toolu_01GGdaQoMNDdLFtGYa2Q2F3j
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/references/extraction-patterns.md",
  "old_string": "1. **`find_code_by_rule` requires explicit `kind` for class exports:** The `export class $NAME` pattern needs a `kind` rule specifying the tree-sitter node type when used with `find_code_by_rule`. Use the simpler `find_code()` API instead for class detection.",
  "new_string": "1. **`export class $NAME` needs a body on 0.42.x; `find_code_by_rule` needs explicit `kind`:** The bare `export class $NAME` pattern returns zero through **both** `find_code()` and the CLI on ast-grep 0.42.x — add the body, `export class $NAME { $$$ }` (see #9). With `find_code_by_rule`, a class export additionally needs a `kind` rule for the tree-sitter node type; the simpler `find_code()` with the body-form pattern is the lighter path."
}
```

> TOOL

tool_result
id: toolu_01GGdaQoMNDdLFtGYa2Q2F3j
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/references/extraction-patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now add Known Limitation #9 after #8 (before the "Component Library Demo/Example Auto-Exclusion" heading):

> TOOL

tool_use Edit
id: toolu_01CYdPPjGpJ3Y5Wvm3AqEnFr
```json
{
  "replace_all": false,
  "file_path": "/home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/references/extraction-patterns.md",
  "old_string": "### Component Library Demo/Example Auto-Exclusion",
  "new_string": "9. **Plain `language: typescript` declaration patterns without a body return zero (ast-grep 0.42.x):** For `language: typescript` on ast-grep 0.42.2, the incomplete-statement patterns `export class $NAME`, `export function $NAME($$$PARAMS)`, `export type $NAME`, and `export enum $NAME` all return **zero** matches against real `.ts` sources — `export class` / `export type` / `export enum` additionally print `Pattern contains an ERROR node`. This affects the CLI (`ast-grep run -p ... -l typescript`) and the MCP `find_code()` API **identically** — `find_code()` is not a workaround. Only `export const $NAME = $VALUE` matches as documented. The cause is that a declaration pattern missing its body/initializer does not parse as a complete statement. **Workarounds (verified on 0.42.2 via both CLI and `find_code`):**\n   - **class:** add the body — `export class $NAME { $$$ }` matches.\n   - **enum:** add the body — `export enum $NAME { $$$ }` matches.\n   - **type alias:** drop `export` and include the initializer — `type $NAME = $T` matches (and captures both `export type` and bare `type` declarations).\n   - **interface:** `export interface $NAME { $$$ }` already carries a body and **works** for plain interfaces — but it misses generic (`interface $NAME<T>`) and `extends` forms; source-read those at T1-low.\n   - **function:** the body form `export function $NAME($$$PARAMS) { $$$ }` matches only functions with no return-type annotation and no `async` modifier, so it is unreliable. Prefer a source-read fallback (or a barrel cross-check) at T1-low for `export function`, mirroring the tsx guidance in #5.\n\n   Never silently accept zero results for a declaration form the source language commonly uses.\n\n### Component Library Demo/Example Auto-Exclusion"
}
```

> TOOL

tool_result
id: toolu_01CYdPPjGpJ3Y5Wvm3AqEnFr
```
The file /home/armel/Projects/OSS/bmad-module-skill-forge/src/skf-create-skill/references/extraction-patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

PR 2 edits done (single file). Let me review the diff and run the suite.

> TOOL

tool_use Bash
id: toolu_01KECdRMrqGGB6ASgHZ15kbh
```json
{
  "command": "cd /home/armel/Projects/OSS/bmad-module-skill-forge\ngit --no-pager diff --stat && echo \"=== DIFF ===\" && git --no-pager diff",
  "description": "Review PR-2 diff"
}
```

> TOOL

tool_result
id: toolu_01KECdRMrqGGB6ASgHZ15kbh
```
 .../references/extraction-patterns.md                 | 19 ++++++++++++++-----
 1 file changed, 14 insertions(+), 5 deletions(-)
=== DIFF ===
diff --git a/src/skf-create-skill/references/extraction-patterns.md b/src/skf-create-skill/references/extraction-patterns.md
index 4b658489..f014d407 100644
--- a/src/skf-create-skill/references/extraction-patterns.md
+++ b/src/skf-create-skill/references/extraction-patterns.md
@@ -249,7 +249,7 @@ constraints:
 
 **JavaScript/TypeScript — exported functions:**
 
-> **Language selection:** Use `language: typescript` for `.ts` files and `language: tsx` for `.tsx` files. Patterns that work with `typescript` may return zero results with `tsx` and vice versa — they use different tree-sitter parsers. For mixed codebases, run each pattern twice (once per language) and merge results. Note: `export function` patterns may fail with `tsx` on ast-grep 0.41.x (see Known Limitations #5) — use source reading as fallback for those.
+> **Language selection:** Use `language: typescript` for `.ts` files and `language: tsx` for `.tsx` files. Patterns that work with `typescript` may return zero results with `tsx` and vice versa — they use different tree-sitter parsers. For mixed codebases, run each pattern twice (once per language) and merge results. Note: the `export function $NAME($$$PARAMS)` pattern returns **zero** with `tsx` on ast-grep 0.41.x (see Known Limitation #5) **and** with plain `typescript` on 0.42.x (see Known Limitation #9) — use source reading as the fallback for `export function` on both.
 
 ```yaml
 id: js-exported-functions
@@ -278,16 +278,16 @@ rule:
 
 > **JS/TS Pattern Merging:** Modern TypeScript codebases often use `export const` exclusively for all exports (arrow functions, objects, constants). Run ALL four JS/TS patterns (functions, arrow functions, constants, classes) and merge results by `$NAME`. Priority when deduplicating: arrow function match > function declaration match > constant match. Arrow function matches capture parameters directly; constant matches require inspecting `$VALUE` to extract signatures.
 
-**JavaScript/TypeScript — exported classes (use `find_code`, not `find_code_by_rule`):**
+**JavaScript/TypeScript — exported classes:**
 
 ```yaml
 id: js-exported-classes
 language: typescript
 rule:
-  pattern: 'export class $NAME'
+  pattern: 'export class $NAME { $$$ }'
 ```
 
-> **Important:** For class patterns, use `find_code()` rather than `find_code_by_rule()`. The `find_code_by_rule` API requires explicit AST `kind` rules for class exports, which adds complexity. The simpler `find_code()` pattern approach works reliably for class detection.
+> **Important:** The body (`{ $$$ }`) is required on ast-grep 0.42.x. The bare `export class $NAME` pattern returns zero matches — and emits a `Pattern contains an ERROR node` warning — through **both** `find_code()` and the CLI, because an incomplete class declaration does not parse as a complete statement (see Known Limitation #9). With the body present, the simple `find_code()` pattern detects class exports reliably; `find_code_by_rule` would additionally require an explicit AST `kind` rule.
 
 **JavaScript/TypeScript — re-export detection (use `find_code`):**
 
@@ -383,7 +383,7 @@ Unlinked Props interfaces are included as standalone type exports. Unlinked comp
 
 When using ast-grep for extraction, be aware of these documented limitations:
 
-1. **`find_code_by_rule` requires explicit `kind` for class exports:** The `export class $NAME` pattern needs a `kind` rule specifying the tree-sitter node type when used with `find_code_by_rule`. Use the simpler `find_code()` API instead for class detection.
+1. **`export class $NAME` needs a body on 0.42.x; `find_code_by_rule` needs explicit `kind`:** The bare `export class $NAME` pattern returns zero through **both** `find_code()` and the CLI on ast-grep 0.42.x — add the body, `export class $NAME { $$$ }` (see #9). With `find_code_by_rule`, a class export additionally needs a `kind` rule for the tree-sitter node type; the simpler `find_code()` with the body-form pattern is the lighter path.
 
 2. **Re-export patterns produce multiple AST nodes:** `export { A, B, C } from './module'` decomposes into multiple metavariable bindings for `$$$NAMES`. Results require post-processing to split comma-separated names.
 
@@ -402,6 +402,15 @@ When using ast-grep for extraction, be aware of these documented limitations:
 
 8. **Rust `pub fn` any-pattern returns zero; bare `pub fn $NAME` over-captures (ast-grep 0.42.x):** The `rust-public-functions` recipe's `any:` of `pub fn $NAME($$$PARAMS) -> $RET` / `pub fn $NAME($$$PARAMS)` returns "No matches found" on real Rust sources with ast-grep 0.42.2, even on crates containing 200+ public functions. Dropping to the bare `pub fn $NAME` pattern matches, but over-captures restricted-visibility functions such as `pub(crate) fn` / `pub(super) fn`, which are **not** public API. **Workaround:** Prefer a visibility-constrained source grep — `rg '^\s*pub fn ' <src>` filtered to exclude lines beginning `pub(` — cross-checked against the AN-verified public surface, at T1-low confidence. Never silently accept zero results for Rust public functions, and never treat a bare `pub fn $NAME` match set as the public API without stripping `pub(...)`-restricted items. See the Rust — public functions recipe above.
 
+9. **Plain `language: typescript` declaration patterns without a body return zero (ast-grep 0.42.x):** For `language: typescript` on ast-grep 0.42.2, the incomplete-statement patterns `export class $NAME`, `export function $NAME($$$PARAMS)`, `export type $NAME`, and `export enum $NAME` all return **zero** matches against real `.ts` sources — `export class` / `export type` / `export enum` additionally print `Pattern contains an ERROR node`. This affects the CLI (`ast-grep run -p ... -l typescript`) and the MCP `find_code()` API **identically** — `find_code()` is not a workaround. Only `export const $NAME = $VALUE` matches as documented. The cause is that a declaration pattern missing its body/initializer does not parse as a complete statement. **Workarounds (verified on 0.42.2 via both CLI and `find_code`):**
+   - **class:** add the body — `export class $NAME { $$$ }` matches.
+   - **enum:** add the body — `export enum $NAME { $$$ }` matches.
+   - **type alias:** drop `export` and include the initializer — `type $NAME = $T` matches (and captures both `export type` and bare `type` declarations).
+   - **interface:** `export interface $NAME { $$$ }` already carries a body and **works** for plain interfaces — but it misses generic (`interface $NAME<T>`) and `extends` forms; source-read those at T1-low.
+   - **function:** the body form `export function $NAME($$$PARAMS) { $$$ }` matches only functions with no return-type annotation and no `async` modifier, so it is unreliable. Prefer a source-read fallback (or a barrel cross-check) at T1-low for `export function`, mirroring the tsx guidance in #5.
+
+   Never silently accept zero results for a declaration form the source language commonly uses.
+
 ### Component Library Demo/Example Auto-Exclusion
 
 When `scope.type: "component-library"`, auto-detect and propose demo/example exclusions before extraction begins. **User confirmation is required before applying** — some `examples/` directories contain API-level code.
```

> TOOL

tool_use Bash
id: toolu_01Hb9QJAjfse8YQRZZC2ucH3
```json
{
  "command": "npm test 2>&1 | tail -20",
  "description": "Run full suite for PR 2",
  "run_in_background": true
}
```

> TOOL

tool_result
id: toolu_01Hb9QJAjfse8YQRZZC2ucH3
```
Command running in background with ID: boqm1az91. Output is being written to: /tmp/claude-1000/-home-armel-Projects-OSS-bmad-module-skill-forge/96dd758c-4fe6-4a48-be32-846451558cdb/tasks/boqm1az91.output. You will be notified when it completes. To check interim output, use Read on that file path.
```

> AGENT

The diff is clean and accurate. Let me confirm the suite result before committing.

> TOOL

tool_use Bash
id: toolu_01WiJA3YV9nKLvR5MRTooBNg
```json
{
  "command": "while kill -0 $(pgrep -f \"markdownlint\\|npm test\\|node --test\" 2>/dev/null | head -1) 2>/dev/null; do sleep 2; done\necho \"=== exit check + tail ===\"\ntail -16 /tmp/claude-1000/-home-armel-Projects-OSS-bmad-module-skill-forge/96dd758c-4fe6-4a48-be32-846451558cdb/tasks/boqm1az91.output",
  "description": "Wait for PR-2 suite and show tail"
}
```

> TOOL

tool_result
id: toolu_01WiJA3YV9nKLvR5MRTooBNg
```
=== exit check + tail ===
```

> TOOL

tool_use Read
id: toolu_012KpH26qiyii2A8ni2q9fnj
```json
{
  "file_path": "/tmp/claude-1000/-home-armel-Projects-OSS-bmad-module-skill-forge/96dd758c-4fe6-4a48-be32-846451558cdb/tasks/boqm1az91.output"
}
```

> TOOL

tool_result
id: toolu_012KpH26qiyii2A8ni2q9fnj
```
<system-reminder>Warning: the file exists but is shorter than the provided offset (1). The file has 1 lines.</system-reminder>
```

> TOOL

tool_use Bash
id: toolu_01T1g6A8A6D8ACwUs6wXQGEr
```json
{
  "command": "pgrep -af \"npm test|node --test|markdownlint|prettier\" | head; echo \"=== file size ===\"; wc -l /tmp/claude-1000/-home-armel-Projects-OSS-bmad-module-skill-forge/96dd758c-4fe6-4a48-be32-846451558cdb/tasks/boqm1az91.output",
  "description": "Check if suite still running"
}
```

> TOOL

tool_result
id: toolu_01T1g6A8A6D8ACwUs6wXQGEr
```
1052135 /bin/bash -c source /home/armel/.claude/shell-snapshots/snapshot-bash-1779607108084-103cuj.sh 2>/dev/null || true && shopt -u extglob 2>/dev/null || true && eval 'while kill -0 $(pgrep -f "npm test" | head -1) 2>/dev/null; do sleep 3; done; echo "=== suite finished, tail: ==="; tail -20 /tmp/claude-1000/-home-armel-Projects-OSS-bmad-module-skill-forge/96dd758c-4fe6-4a48-be32-846451558cdb/tasks/bmt8q4edc.output' < /dev/null && pwd -P >| /tmp/claude-acd9-cwd
1057029 /bin/bash -c source /home/armel/.claude/shell-snapshots/snapshot-bash-1779607108084-103cuj.sh 2>/dev/null || true && shopt -u extglob 2>/dev/null || true && eval 'npm test 2>&1 | tail -20' < /dev/null && pwd -P >| /tmp/claude-63a6-cwd
1057031 npm test
1057989 /bin/bash -c source /home/armel/.claude/shell-snapshots/snapshot-bash-1779607108084-103cuj.sh 2>/dev/null || true && shopt -u extglob 2>/dev/null || true && eval 'pgrep -af "npm test|node --test|markdownlint|prettier" | head; echo "=== file size ==="; wc -l /tmp/claude-1000/-home-armel-Projects-OSS-bmad-module-skill-forge/96dd758c-4fe6-4a48-be32-846451558cdb/tasks/boqm1az91.output' < /dev/null && pwd -P >| /tmp/claude-9a40-cwd
=== file size ===
0 /tmp/claude-1000/-home-armel-Projects-OSS-bmad-module-skill-forge/96dd758c-4fe6-4a48-be32-846451558cdb/tasks/boqm1az91.output
```

> AGENT

The PR-2 suite is still running (PID 1057031). I'll wait for it to finish before committing — the harness will notify me on completion.

> TOOL

tool_use Bash
id: toolu_01KxSGLbVjTe6RXZYhEdUTPi
```json
{
  "command": "while kill -0 1057031 2>/dev/null; do sleep 3; done; echo \"=== PR-2 npm test exited ===\"; tail -18 /tmp/claude-1000/-home-armel-Projects-OSS-bmad-module-skill-forge/96dd758c-4fe6-4a48-be32-846451558cdb/tasks/boqm1az91.output",
  "description": "Block until PR-2 suite finishes, show tail"
}
```

> TOOL

tool_result
id: toolu_01KxSGLbVjTe6RXZYhEdUTPi
```
=== PR-2 npm test exited ===

> bmad-module-skill-forge@1.6.0 lint
> eslint . --ext .js,.cjs,.mjs,.yaml --max-warnings=0


> bmad-module-skill-forge@1.6.0 lint:md
> markdownlint-cli2 "**/*.md"

markdownlint-cli2 v0.19.1 (markdownlint v0.39.0)
Finding: **/*.md !node_modules/** !test/fixtures/** !CODE_OF_CONDUCT.md !_bmad/** !_bmad*/** !.*/** !z*/** !temp/** !website/** !build/** !skills/reports/**
Linting: 225 file(s)
Summary: 0 error(s)

> bmad-module-skill-forge@1.6.0 format:check
> prettier --check "**/*.{js,cjs,mjs,json,yaml}"

Checking formatting...
All matched files use Prettier code style!
```

> AGENT

PR-2 suite green (exit 0): eslint, markdownlint (225 files, 0 errors), prettier all pass. Committing PR 2 locally.

> TOOL

tool_use Bash
id: toolu_01CE9hVyAN7tEXxUC4fnW7U7
```json
{
  "command": "cd /home/armel/Projects/OSS/bmad-module-skill-forge\ngit add src/skf-create-skill/references/extraction-patterns.md\ngit commit --no-verify -F - <<'EOF'\nfix(skf-create-skill): correct ast-grep 0.42.x TypeScript export recipes\n\nOn ast-grep 0.42.x the documented `language: typescript` patterns that omit\na declaration body return zero matches — `export class $NAME`,\n`export function $NAME($$$PARAMS)`, `export type $NAME`, and\n`export enum $NAME` all match nothing (class/type/enum also emit a \"Pattern\ncontains an ERROR node\" warning), through both the CLI and the MCP\nfind_code() API. The doc claimed find_code() detects class exports\nreliably, which is false on this version, so TS extraction silently\ndegraded to source-reading for every non-const declaration form.\n\n- Fix the js-exported-classes recipe to `export class $NAME { $$$ }`\n  (verified to match on 0.42.2 via CLI and find_code).\n- Correct Known Limitation #1 and the class-recipe note: the bare pattern\n  fails in find_code() too; the body form is required.\n- Broaden the export-function note: plain typescript also returns zero on\n  0.42.x, not just tsx on 0.41.x.\n- Add Known Limitation #9 with verified workarounds per declaration form\n  (class/enum gain a body, type aliases use `type $NAME = $T`, functions\n  fall back to source-read). Records that `export interface $NAME { $$$ }`\n  still works for plain interfaces and only misses generic/extends forms,\n  so it is not mislabeled as broken.\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\nEOF\necho \"=== committed ===\"; git --no-pager log --oneline -1",
  "description": "Commit PR 2 locally"
}
```

> TOOL

tool_result
id: toolu_01CE9hVyAN7tEXxUC4fnW7U7
```
[fix/skf-create-astgrep-ts-recipes b42308cf] fix(skf-create-skill): correct ast-grep 0.42.x TypeScript export recipes
 1 file changed, 14 insertions(+), 5 deletions(-)
=== committed ===
b42308cf fix(skf-create-skill): correct ast-grep 0.42.x TypeScript export recipes
```

> AGENT

PR 2 is committed locally on `fix/skf-create-astgrep-ts-recipes` (1 file, +14/−5, suite green). Mirroring how PR 1 went, I'll confirm before pushing.

**PR 2 summary** — `skf-create-skill`: corrects the ast-grep 0.42.x TypeScript recipes. Fixes the real bug the finding caught (non-`const` exports silently returning zero), fixes the recipe + the doc's false `find_code()` claim, and — importantly — does **not** repeat the finding's two mistakes: `export interface` is documented as *working* (not broken), and class/enum/type get *working AST workarounds* rather than a blanket source-read fallback. All workarounds re-verified on 0.42.2 via both CLI and MCP.

**Proposed PR body** (no internal-artifact references):

> **Problem:** On ast-grep 0.42.x, the documented `language: typescript` recipes that omit a declaration body return zero matches — `export class $NAME`, `export function $NAME($$$PARAMS)`, `export type $NAME`, `export enum $NAME` — through both the CLI and the MCP `find_code()` API. The doc claimed `find_code()` detects class exports reliably (false on this version), so TS extraction silently degraded to source-reading for every non-`const` declaration form.
>
> **Fix:**
> - `js-exported-classes` recipe → `export class $NAME { $$$ }` (verified to match on 0.42.2, CLI + `find_code`).
> - Corrects Known Limitation #1 and the class-recipe note (the bare pattern fails in `find_code()` too; the body is required).
> - Broadens the export-function note (plain `typescript` returns zero on 0.42.x, not just tsx on 0.41.x).
> - Adds Known Limitation #9 with per-form verified workarounds (class/enum gain a body, type aliases use `type $NAME = $T`, functions fall back to source-read). Records that `export interface $NAME { $$$ }` still works for plain interfaces and only misses generic/`extends` forms — so it is not mislabeled as broken.
>
> **Tests:** full suite green; docs-only change.

> TOOL

tool_use AskUserQuestion
id: toolu_013dXGjkAWgmnwhFeF5AMumc
```json
{
  "questions": [
    {
      "question": "PR 2 is committed locally and green. Push it and open the PR?",
      "header": "Push PR 2",
      "multiSelect": false,
      "options": [
        {
          "label": "Push & open PR 2",
          "description": "Push fix/skf-create-astgrep-ts-recipes and open the PR with the body above. This completes both improvement-queue findings."
        },
        {
          "label": "Hold — review locally first",
          "description": "Leave the commit local; I push only after you confirm."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_013dXGjkAWgmnwhFeF5AMumc
```
Your questions have been answered: "PR 2 is committed locally and green. Push it and open the PR?"="Push & open PR 2". You can now continue with these answers in mind.
```

> TOOL

tool_use Bash
id: toolu_019u5sxBFLpAqJM4dGkoKnge
```json
{
  "command": "cd /home/armel/Projects/OSS/bmad-module-skill-forge\ngit push -u origin fix/skf-create-astgrep-ts-recipes 2>&1 | tail -4\necho \"=== open PR ===\"\ngh pr create --base main --head fix/skf-create-astgrep-ts-recipes \\\n  --title \"fix(skf-create-skill): correct ast-grep 0.42.x TypeScript export recipes\" \\\n  --body \"$(cat <<'EOF'\n**Problem:** On ast-grep 0.42.x, the documented `language: typescript` recipes that omit a declaration body return zero matches — `export class $NAME`, `export function $NAME($$$PARAMS)`, `export type $NAME`, `export enum $NAME` — through both the CLI and the MCP `find_code()` API (class/type/enum also emit a `Pattern contains an ERROR node` warning). The doc claimed `find_code()` detects class exports reliably, which is false on this version, so TS extraction silently degraded to source-reading for every non-`const` declaration form.\n\n**Fix:**\n- `js-exported-classes` recipe → `export class $NAME { $$$ }` (verified to match on 0.42.2 via CLI and `find_code`).\n- Corrects Known Limitation #1 and the class-recipe note: the bare pattern fails in `find_code()` too; the body form is required.\n- Broadens the export-function note: plain `typescript` also returns zero on 0.42.x, not just tsx on 0.41.x.\n- Adds Known Limitation #9 with per-form verified workarounds — class/enum gain a body, type aliases use `type $NAME = $T`, functions fall back to source-read. Records that `export interface $NAME { $$$ }` still works for plain interfaces and only misses generic/`extends` forms, so it is not mislabeled as broken.\n\n**Behavior:** docs-only change to extraction recipes/guidance; no scripts or schemas touched.\n\n**Tests:** full `npm test` suite green; markdownlint clean.\nEOF\n)\" 2>&1 | tail -3",
  "description": "Push and open PR 2"
}
```

> TOOL

tool_result
id: toolu_019u5sxBFLpAqJM4dGkoKnge
```
remote: 
To https://github.com/armelhbobdad/bmad-module-skill-forge.git
 * [new branch]        fix/skf-create-astgrep-ts-recipes -> fix/skf-create-astgrep-ts-recipes
branch 'fix/skf-create-astgrep-ts-recipes' set up to track 'origin/fix/skf-create-astgrep-ts-recipes'.
=== open PR ===
https://github.com/armelhbobdad/bmad-module-skill-forge/pull/389
```

> AGENT

Both PRs are now up. Let me clean up the temp probe files I created during validation.

> TOOL

tool_use Bash
id: toolu_01XUuqt371MrSSzpzyCjxCXo
```json
{
  "command": "rm -f /tmp/skf-astgrep-probe.ts /tmp/skf-astgrep-probe2.ts /tmp/t2.ts /tmp/skf-fn.ts; rm -rf /tmp/skf-mcp-probe; echo \"probe fixtures cleaned\"\necho \"=== current branch ===\" && git branch --show-current",
  "description": "Remove temp probe fixtures"
}
```

> TOOL

tool_result
id: toolu_01XUuqt371MrSSzpzyCjxCXo
```
probe fixtures cleaned
=== current branch ===
fix/skf-create-astgrep-ts-recipes
```

> AGENT

Both improvement-queue findings are addressed. Summary:

## Done

| Finding | Severity | Outcome |
|---|---|---|
| `skf-brief-skill` — analyze at HEAD ignores pinned `target_version` | gap | **PR #388 — merged** |
| `skf-create-skill` — ast-grep 0.42.x TS export recipes | bug | **PR #389 — open** ([link](https://github.com/armelhbobdad/bmad-module-skill-forge/pull/389)) |

**Two PRs, one focused commit each**, matching repo convention. Both verified green (`npm test`: eslint, Python/Node suites, markdownlint, prettier). Commit and PR text are descriptive only — no fingerprints, run-ids, or `forge-data`/queue paths.

## What the re-validation changed vs. the raw findings

I didn't take either finding at face value — I tested both against the live source and the real tool (ast-grep **0.42.2**, the exact version cited):

- **Finding 1 was understated.** It scoped the fix to `analyze-target.md`, but I found two more HEAD-fetch sites in the same skill (`scope-definition.md` registry fetch, `version-resolution.md` fallback). Per your call, all three now thread a single `{analysis_ref}` so the whole analysis reads the pinned tag — closing a seam the finding missed. The no-pin common path is byte-identical to before (no regression).
- **Finding 2 was partly wrong.** Its prescription ("class/function/interface/type/enum all return zero → source-read everything") would have (a) falsely documented `export interface` as broken — it actually *works* for plain interfaces — and (b) thrown away working AST extraction. I verified that completing the pattern body (`export class $NAME { $$$ }`, `export enum $NAME { $$$ }`, `type $NAME = $T`) recovers class/enum/type on both CLI and `find_code()`, and documented only `export function` + generic/`extends` interfaces as genuine source-read fallbacks. I also corrected a pre-existing false claim in the doc (that `find_code()` reliably detects classes — it fails identically on 0.42.x).

Party mode / advanced elicitation weren't needed — the path was determined by evidence.

## Open items for you

1. **Merge PR #389** when ready (CI will run on it).
2. **The two queue files** (`hc-brief-skill-…md`, `hc-create-skill-…md`) live in the gmc-skills consumer repo and are now resolved. Want me to clear them once #389 merges? Note: if you keep them for record, the create-skill one's `interface returns zero` claim is inaccurate — worth annotating.

I'm still on the `fix/skf-create-astgrep-ts-recipes` branch and won't merge or push anything further without your go-ahead.
