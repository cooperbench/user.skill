> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

You are creating an implementation plan for the following idea.





        Idea:
# Sprint 2a — Editorial core

Bot maintains an epic body and checklist for one epic, with section-level body editing. Minimum to have an editorial conversation.

**Full spec is at `planning-bot-spec.md` in this repo root. Refer to it for complete details on Body Structure and Editing, Body Templates, The Checklist as Guide, and Data Model sections.**

## Supabase
- URL: https://yhwflvadmefhkshwbfnf.supabase.co
- Service key: [REDACTED_SUPABASE_SERVICE_ROLE_JWT]

## Scope

- Tables: checklist_items, epic_events (with transaction_id)
- Body parser/serializer — markdown ↔ structured sections with ## heading delimiters; enforces heading hierarchy (# for title only, ## for sections, ### for sub-headings)
- Turn-end epic outline emitted to system_logs at info level
- Default body template (design doc) — Goal, Principles, Context, Key Decisions, Open Questions, Deliverable
- `edit_epic` tool — body (whole + section ops) + checklist; supports:
  - Write whole body
  - Write specific sections
  - Append to a section
  - Add new section with position
  - Rename/remove sections
  - `expected_diff` parameter for server-enforced diff verification (unified diff format)
- `create_epic`, `revert` (transaction-grouped), `render_epic` tools
- Read tools: `get_epic` (with section addressing), `get_section_names`, `get_history`, `get_self_understanding`
- History tools: `get_epic_at_time`, `get_recent_turns`, `search_tool_calls`
- Default checklist seed — 18 items with adaptation logic
- Title and goal are derived columns from body parsing (# Title and ## Goal first paragraph)

## Key Data Model

### checklist_items
id, epic_id, content, status (open|done|skipped|superseded), position, source (bot_inferred|user_requested|carried_over|default_seed|second_opinion), skip_reason, superseded_by_item_id, created_at, completed_at

### epic_events
id, epic_id, transaction_id (uuid), event_type, summary, prior_state (json), turn_id, occurred_at
Event types: body_edit, checklist_change, sprints_change, state_change, forced_handoff, created, code_referenced, codebase_added, image_generated, second_opinion_requested, reverted_to, sprint_status_change

## Body Parser Rules
- Section boundaries are ## headings (level-2 markdown)
- Section names are case-sensitive
- Pre-section content is "_preamble"
- Sub-sections (### and below) are part of parent section
- No ## headings → whole body is _preamble
- # Title and ## Goal are required structural elements; missing → write rejected
- Code blocks containing ## are NOT section boundaries

## Acceptance Criteria

- Create an epic via natural language → epics row created, default checklist seeded with 18 items, body initialized
- 10-turn scripted conversation (mocked Anthropic) produces body with all 6 default sections
- Section-level edit → only that section changes; other sections byte-identical
- Whole body edit → diff captured in event; revert restores prior version exactly
- "revert that" → most recent transaction undone, new reverted_to event logged
- expected_diff mismatch → server refuses write, returns actual diff
- expected_diff match → server commits normally
- get_epic_at_time(epic_id, T) → returns body/checklist state as of time T
- get_recent_turns(5) → returns 5 most recent turns with summaries
- search_tool_calls(tool_name='edit_epic', epic_id=X) → returns matching calls
- Turn-end system_logs row with event_type='epic_outline' containing title + section list + line counts

## Tests
- Unit: body parser (markdown → sections → markdown roundtrip is identity); section operations; edit_epic validation; transaction_id grouping; expected_diff comparison; epic-at-time replay
- Integration: 10-turn fixture conversation against local Supabase with mocked Anthropic; revert end-to-end

        Project directory:
        /Users/user_c042661f/Documents/arnold-v2





        No prior clarification artifact exists. Identify ambiguities, ask clarifying questions, and state your assumptions inside the plan output.

        Requirements:
        - If the engineering brief suggests an approach, use it as your starting hypothesis — but before committing, consider if there's a simpler or more fundamental fix. The brief is well-researched input, not a final answer.
        - If the brief is absent, incomplete, or says "skip", inspect the repository yourself before planning.
        - Stay focused on the requested idea. If repo exploration surfaces unrelated issues or docs, ignore them and return to the task.
        - Prefer source code, tests, and directly relevant config files. Avoid `.megaplan/`, prior plan artifacts, and unrelated `docs/` or ops/deployment material unless the task explicitly depends on them.
        - Stop exploring once you have enough evidence to name the concrete touch points and validation path. Do not keep browsing after you can write the plan.
        - Produce a concrete implementation plan in markdown.
        - Define observable success criteria as objects with `criterion` (string) and `priority` (`must`, `should`, or `info`):
          - `must` — hard gate. The reviewer will block on failure. Use for correctness, functional requirements, and verifiable outcomes (e.g., "all existing tests pass", "API returns 200 for valid input"). Every `must` criterion must have a clear yes/no answer.
          - `should` — quality target. The reviewer flags but does not block. Use for subjective goals, numeric guidelines, and best-effort improvements (e.g., "file under ~300 lines", "no deeply nested conditionals", "each function has a single responsibility").
          - `info` — documented for humans, reviewer skips. Use for criteria that cannot be verified in this pipeline (e.g., "13 manual smoke tests pass", "stakeholder sign-off obtained").
        - Each success criterion should include a `requires` field listing the capabilities needed for verification. Valid capability strings: `run_shell`, `read_files`, `run_tests`, `parse_diff`, `read_build_output`, `run_linter` (container), `drive_browser`, `inspect_runtime_ui`, `observe_runtime_logs`, `subjective_judgment`, `verify_physical_device` (human). `must` criteria MUST have non-empty `requires`. Example: `{"criterion": "All tests pass", "priority": "must", "requires": ["run_tests"]}`.
        - Use the `questions` field for ambiguities that would materially change implementation.
        - Use the `assumptions` field for defaults you are making so planning can proceed now.
        - Prefer cheap validation steps early.
        - Keep the plan proportional to the task. A 1-line fix needs a 2-step plan (apply fix + run tests), not a 5-step investigation.
        - If user notes answer earlier questions, incorporate them into the draft plan instead of re-asking them.
        - Fix the problem fully. Do not limit scope just to avoid breaking existing tests — update the tests too if needed.
        - Prefer the simplest, most direct fix. No fallbacks, type conversions, or defensive wrappers without concrete evidence they are needed.
        - If the task or issue hints suggest a specific approach, follow it. Only deviate with concrete counter-evidence.

        Plan template — simple format (adapt to the actual repo and scope):
````md
# Implementation Plan: [Title]

## Overview
Summarize the goal, current repository shape, and the constraints that matter.

## Main Phase

### Step 1: Audit the current behavior (`megaplan/prompts.py`)
**Scope:** Small
1. **Inspect** the current implementation and call out the exact insertion points (`megaplan/prompts.py:29`).

### Step 2: Add the first change (`megaplan/evaluation.py`)
**Scope:** Medium
1. **Implement** the smallest viable change with exact file references (`megaplan/evaluation.py:1`).
2. **Capture** any tricky behavior with a short example.
   ```python
   issues = validate_plan_structure(plan_text)
   ```

### Step 3: Wire downstream behavior (`megaplan/handlers.py`, `megaplan/workers.py`)
**Scope:** Medium
1. **Update** the runtime flow in the touched files (`megaplan/handlers.py:400`, `megaplan/workers.py:199`).

### Step 4: Prove the change (`tests/test_evaluation.py`, `tests/test_megaplan.py`)
**Scope:** Small
1. **Run** the cheapest targeted checks first (`tests/test_evaluation.py:1`).
2. **Finish** with broader verification once the wiring is in place (`tests/test_megaplan.py:1`).

## Execution Order
1. Update prompts and mocks before enforcing stricter validation.
2. Land higher-risk wiring after the validator and tests are ready.

## Validation Order
1. Start with focused unit tests.
2. Run the broader suite after the flow changes are in place.
````

For complex plans, use multiple phases:
````md
## Phase 1: Foundation — Dependencies, DB, Types

### Step 1: Install dependencies (`package.json`)
...

### Step 2: Create database migration (`supabase/migrations/`)
...

## Phase 2: Core Integration

### Step 3: Port the main component (`src/components/`)
...
````

Template guidance:
- Simple plans: use `## Main Phase` with `### Step N:` sections underneath.
- Complex plans: use multiple `## Phase N:` sections, each containing `### Step N:` steps. Step numbers are global (not per-phase).
- The flat `## Step N:` format (without phases) also works for backwards compatibility.
- Key invariants: one H1 title, one `## Overview`, numbered step sections (`### Step N:` or `## Step N:`), and at least one ordering section.

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/arnold-v2",
  "description": "List project root"
}
```

> TOOL

tool_result Bash
```
CLAUDE.md
agent_kit
arnold
arnold_sdk
ideas
megaplan
planning-bot-spec.md
pyproject.toml
run-megaplan.sh
supabase
tests
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/arnold-v2/arnold /Users/user_c042661f/Documents/arnold-v2/agent_kit /Users/user_c042661f/Documents/arnold-v2/tests /Users/user_c042661f/Documents/arnold-v2/supabase /Users/user_c042661f/Documents/arnold-v2/arnold_sdk",
  "description": "List package directories"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/arnold-v2/agent_kit:
__init__.py
__pycache__
blob
envelope.py
envelope.schema.json
ledger.py
logging.py
loop.py
model
ports.py
resident.py
store
tool_kit.py
tools
transport

/Users/user_c042661f/Documents/arnold-v2/arnold:
__init__.py
__pycache__
cli.py

/Users/user_c042661f/Documents/arnold-v2/arnold_sdk:
__init__.py
__pycache__
arnold

/Users/user_c042661f/Documents/arnold-v2/supabase:
config.toml
migrations

/Users/user_c042661f/Documents/arnold-v2/tests:
__init__.py
__pycache__
helpers.py
store_contract.py
store_contract_v1b.py
test_anthropic_model.py
test_anthropic_replay.py
test_cli.py
test_coalescer.py
test_communication_resident.py
test_create_message_synthesize_flag.py
test_discord_ingestion_ledger.py
test_discord_ingestion_persist_first.py
test_discord_transport.py
test_duplicate_inbound_dropped.py
test_envelope.py
test_image_attachment_pipeline.py
test_image_tools.py
test_ledger.py
test_loop_vision_blocks.py
test_megaplan_arnold_import.py
test_mid_turn_messages.py
test_no_leaked_secrets.py
test_ports_v1b.py
test_reconciler.py
test_resident.py
test_resident_recovery.py
test_run_turn.py
test_run_turn_hooks.py
test_send_message_resident.py
test_sqlite_store.py
test_sqlite_store_v1b.py
test_status_formatter.py
test_status_lifecycle.py
test_supabase_adapters.py
test_supabase_store.py
test_tool_kit.py
test_tool_kit_external_queue.py
test_update_message.py
test_voice_pipeline.py
test_whitelist.py
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/arnold-v2/supabase/migrations /Users/user_c042661f/Documents/arnold-v2/agent_kit/store /Users/user_c042661f/Documents/arnold-v2/agent_kit/tools /Users/user_c042661f/Documents/arnold-v2/ideas",
  "description": "List subdirs"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/arnold-v2/agent_kit/store:
__init__.py
__pycache__
migrations
sqlite.py
supabase.py

/Users/user_c042661f/Documents/arnold-v2/agent_kit/tools:
__init__.py
__pycache__
communication.py
images.py

/Users/user_c042661f/Documents/arnold-v2/ideas:
sprint-1a-agent-kit-core.md
sprint-1b-discord-resident.md
sprint-2a-editorial-core.md
sprint-2b-editorial-polish.md
sprint-3-multi-epic.md
sprint-4-sprint-mode.md
sprint-5-codebase-research.md
sprint-6-images-second-opinion.md
sprint_1c_attachments.md

/Users/user_c042661f/Documents/arnold-v2/supabase/migrations:
202604300001_001_core.sql
202604300002_002_images.sql
202604300003_003_external_requests_body.sql
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md"
}
```

> TOOL

tool_result Read
```
File content (77904 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
```

> TOOL

tool_use Bash
```json
{
  "command": "wc -l /Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md /Users/user_c042661f/Documents/arnold-v2/ideas/sprint-2a-editorial-core.md /Users/user_c042661f/Documents/arnold-v2/CLAUDE.md /Users/user_c042661f/Documents/arnold-v2/pyproject.toml",
  "description": "Wc files"
}
```

> TOOL

tool_result Bash
```
2855 /Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md
      64 /Users/user_c042661f/Documents/arnold-v2/ideas/sprint-2a-editorial-core.md
       9 /Users/user_c042661f/Documents/arnold-v2/CLAUDE.md
      43 /Users/user_c042661f/Documents/arnold-v2/pyproject.toml
    2971 total
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/pyproject.toml"
}
```

> TOOL

tool_result Read
```
1	[build-system]
2	requires = ["setuptools>=69"]
3	build-backend = "setuptools.build_meta"
4	
5	[project]
6	name = "arnold-v2"
7	version = "0.1.0"
8	description = "Arnold Discord planning bot core."
9	readme = "planning-bot-spec.md"
10	requires-python = ">=3.11"
11	dependencies = [
12	    "anthropic",
13	    # Sprint 1b resident adapters: Discord gateway, Supabase Storage, Groq voice, and Postgres.
14	    "discord.py",
15	    "groq",
16	    "httpx",
17	    "psycopg[binary]>=3.1",
18	    "supabase",
19	]
20	
21	[project.optional-dependencies]
22	test = [
23	    "jsonschema",
24	    "pytest",
25	    "pytest-asyncio",
26	]
27	
28	[project.scripts]
29	arnold = "arnold.cli:main"
30	
31	[tool.setuptools.packages.find]
32	include = [
33	    "agent_kit",
34	    "agent_kit.*",
35	    "arnold",
36	    "arnold.*",
37	    "megaplan",
38	    "megaplan.*",
39	]
40	
41	[tool.pytest.ini_options]
42	testpaths = ["tests"]
43	python_files = ["test_*.py", "*_test.py"]
44
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/CLAUDE.md"
}
```

> TOOL

tool_result Read
```
1	# Arnold v2
2	
3	IMPORTANT: Do NOT create a `megaplan/` directory in the project root. This name conflicts with the megaplan CLI tool. If you need a namespace wrapper package, name it `arnold_sdk/` instead.
4	
5	The project structure is:
6	- agent_kit/ — core agent framework
7	- arnold/ — Arnold bot implementation and CLI
8	- arnold_sdk/ — thin re-export wrapper (optional)
9	- tests/ — test suite
10
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"^##\\|^# \" /Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md | head -80",
  "description": "List spec headings"
}
```

> TOOL

tool_result Bash
```
1:# Planning Assistant — Discord Bot Spec (Arnold)
9:## Engineering Handoff Readiness
31:## Sprints (Build Roadmap)
37:### Sprint 1a — agent_kit core + invocation mode (week 1)
69:### Sprint 1b — Discord resident mode + robustness (week 2)
113:### Sprint 2a — Editorial core (week 3)
154:### Sprint 2b — Editorial polish (week 4)
191:### Sprint 3 — Multi-epic + message search (week 5)
220:### Sprint 4 — Sprint mode and handoff gating (week 6)
262:### Sprint 5 — Codebase research and code investigation (weeks 7-8)
296:### Sprint 6 — Image generation and second opinion (weeks 9-10)
327:### Sprint 7 — Polish and rough edges (weeks 11-12, optional)
354:## Core Principles
376:## Models
389:## Execution Modes
431:## What an Epic Is
460:## Body Structure and Editing
520:## Body Templates
538:## Epic Abstraction Level
556:## State Advance Gating
578:## Persona
618:## Communication Style
630:## The Checklist as Guide
676:## How to Work Each Checklist Item
803:## Principles in the Plan
811:## Multi-Message Handling
865:## Voice Messages
887:## Feedback System
957:## Long Operations and Visibility
969:## Status Message
1018:## Showing Changes
1026:## Reverting
1042:## References to Bot's Recent Output
1050:## Epic Selection
1066:## Showing the Bot's Understanding
1074:## User Modes
1096:## Sprint Organization (Final Phase)
1148:## Code Investigation
1180:## Images
1184:### User uploads (Sprint 1b onward)
1205:### Agent generation (Sprint 6 onward)
1216:### Images as referenceable epic objects (both sources)
1236:## Second Opinion Mode
1278:## Architecture
1296:## Data Model
1300:### epics
1322:### checklist_items
1332:### sprints
1355:### sprint_items
1364:### messages
1381:### epic_events (append-only audit + state derivation source)
1403:### codebases
1427:### code_artifacts (unified: excerpts, summaries, cache)
1439:### images
1464:### second_opinions
1475:### feedback
1545:### bot_turns
1562:### tool_calls (all tool calls)
1571:### external_requests (provider call ledger)
1620:### system_logs (unified application + system log sink)
1641:## Tools
1658:### Communication
1666:### Read — epics
1683:### Read — images
1687:### Write — images
1691:### Read — code
1698:### Read — feedback
1701:### Write — epics (unified, document-like editing)
1746:### Write — codebases
1750:### Write — code artifacts
1754:### Write — feedback
1759:### Agent observations (bot-authored diagnostic notes)
1766:### Operation tools (full end-to-end operations)
1773:## Agentic Loop
1786:## Subagent Contract
1842:## Callable API
1920:## End-of-Turn Checks
1932:## Hot Context (per LLM invocation)
1956:## System Prompt (Draft Skeleton)
1961:# Role
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md",
  "offset": 113,
  "limit": 160
}
```

> TOOL

tool_result Read
```
113	### Sprint 2a — Editorial core (week 3)
114	
115	**Goal:** Bot maintains an epic body and checklist for one epic, with section-level body editing. Minimum to have an editorial conversation.
116	
117	**Scope:**
118	- Tables: `checklist_items`, `epic_events` (with `transaction_id`)
119	- Body parser/serializer — markdown ↔ structured sections with `##` heading delimiters; enforces heading hierarchy convention (`#` for title only, `##` for sections, `###` for sub-headings) (see Body Structure and Editing)
120	- Turn-end epic outline emitted to `system_logs` at info level with epic_outline event_type (compact title + sections + sub-headings + line counts)
121	- Default body template (design doc) — Goal, Principles, Context, Key Decisions, Open Questions, Deliverable
122	- `edit_epic` tool — body (whole + section ops) + checklist; sprints come in sprint 4 (see Tools)
123	- `edit_epic` `expected_diff` parameter for server-enforced diff verification (see Body Structure and Editing)
124	- `create_epic`, `revert` (transaction-grouped), `render_epic` tools
125	- Read tools: `get_epic` (with section addressing), `get_section_names`, `get_history`, `get_self_understanding`
126	- History tools: `get_epic_at_time`, `get_recent_turns`, `search_tool_calls` (see Tools)
127	- Default checklist seed — the 18 items with adaptation logic (see The Checklist as Guide)
128	- Conscious-document discipline (see Core Principles)
129	- No-fluff communication style (see Communication Style)
130	
131	**Acceptance criteria:**
132	- Create an epic via natural language → `epics` row created, default checklist seeded with 18 items, body initialized with section headings
133	- 10-turn scripted conversation (mocked Anthropic responses) produces a body with all 6 default sections present
134	- Bot edits one section via `edit_epic(body: { sections: { "Constraints": ... } })` → only that section changes; diff confirms; other sections byte-identical
135	- Bot edits whole body → diff captured in event; revert restores prior version exactly
136	- "revert that" → most recent transaction undone, new `reverted_to` event logged
137	- `expected_diff` mismatch → server refuses write, returns actual diff; bot can retry
138	- `expected_diff` matches → server commits normally
139	- `get_epic_at_time(epic_id, T)` → returns body/checklist state as of time T (verified by replaying events from a known fixture)
140	- `get_recent_turns(5)` → returns 5 most recent turns with summaries
141	- `search_tool_calls(tool_name='edit_epic', epic_id=X)` → returns all `edit_epic` calls on epic X with their arguments and timestamps
142	- After any turn that touched an epic, a `system_logs` row exists with `event_type='epic_outline'`, containing the epic's title + section list + line counts in `details`
143	
144	**Tests:**
145	- Unit: body parser (markdown → sections → markdown roundtrip is identity); section operations (replace, append, remove, rename, reorder); `edit_epic` change object validation; transaction_id grouping; prior_state capture per event type; expected_diff comparison logic; epic-at-time replay correctness against fixture event sequences
146	- Integration: 10-turn fixture conversation against local Supabase with mocked Anthropic; verify DB state matches expectation; revert end-to-end
147	
148	**Notes:** Body parser robustness matters — section-level editing relies on it. Worth investing extra time on edge cases (sections with code blocks containing `##`, malformed bodies, etc.).
149	
150	**Readiness gate:** All decisions locked. Engineers have: full body parser specification (`#`/`##`/`###` heading conventions, `_preamble` semantic, code-block edge cases), **required structural elements rule (`# Title` and `## Goal` first paragraph extracted to columns; missing → write rejected)**, default body template (Goal/Principles/Context/Key Decisions/Open Questions/Deliverable), `expected_diff` semantics + unified diff format, full `edit_epic` schema, default 18-item checklist seed with adaptation rules, transaction grouping for revert, turn-end outline log format. No product questions remaining.
151	
152	---
153	
154	### Sprint 2b — Editorial polish (week 4)
155	
156	**Goal:** Thoughtful behaviors that distinguish a real editorial assistant from a body editor.
157	
158	**Scope:**
159	- Table: `feedback`
160	- Per-item depth guidance in system prompt for all 18 checklist items (see How to Work Each Checklist Item)
161	- End-of-turn checks — the five categories (see End-of-Turn Checks)
162	- Show-changes pattern in responses (see Showing Changes)
163	- `search_in_body` and `get_body_outline` tools (see Tools)
164	- Feedback tools: `save_feedback`, `apply_feedback`, `deactivate_feedback`, `list_feedback` (see Tools, Feedback System)
165	- Agent observations: `record_observation`, `list_observations`, `mark_observation_resolved` tools (writes to `feedback` table with observation-specific kinds and `source='agent_observation'`; see Tools and feedback table)
166	- Feedback table extended to support observation kinds (resolved, resolution_note, resolved_at columns) — single migration adds these alongside Sprint 2b's feedback table creation
167	- Hot-context loading of active style + process feedback with `last_applied_at` AND recent unresolved agent observations on this epic
168	- Agent-proposed-user-confirmed flow for saving feedback
169	- Agent-only flow for observations (no user confirmation, bot-authored)
170	
171	**Acceptance criteria:**
172	- "change the part about X" workflow → bot calls `search_in_body` first, then `get_epic` for the matching section, then `edit_epic`; verifiable via `tool_calls` sequence
173	- `get_body_outline` returns section names + line counts that match the actual body (verified against fixture body)
174	- User says "stop apologizing" → bot proposes saving as style feedback, scripted user confirms, row written; subsequent turn (with mocked Anthropic) honors it via active feedback in hot context
175	- User says "save this: keep messages under 200 words" → bot saves immediately (explicit save request)
176	- Bot calls `apply_feedback(id)` → `feedback.last_applied_at` updated to current timestamp
177	- Bot calls `record_observation(kind='friction', content='...', epic_id=X)` → row written with turn_id and context_snapshot auto-filled; surfaces in hot context next turn on same epic
178	- Bot calls `mark_observation_resolved(id, "user clarified")` → resolved_at set, observation no longer in hot context
179	- "Show me the epic" → `render_epic` called, displays body
180	- End-of-turn check fires when bot tries to finish without sending a message → default acknowledgment sent
181	
182	**Tests:**
183	- Unit: `search_in_body` returns correct line numbers and section attribution given fixture bodies; `get_body_outline` returns accurate counts and headings; feedback kind detection from user messages (LLM-graded against fixture set with known labels); end-of-turn check logic given various turn-state fixtures; observation writes record correct turn_id and context_snapshot in `feedback` with `source='agent_observation'`
184	- Integration: feedback save → `apply_feedback` → reload in next turn; verify hot context contains the feedback content; observation recorded → reload in next turn → bot sees it in hot context; observation resolved → next turn no longer shows it
185	- LLM-graded eval: 20 fixture turns with style violations — fluff phrase count threshold 0; 20 fixture turns with body edits — judge whether body contains conversational filler against rubric (LLM-as-judge with structured rubric, automated)
186	
187	**Readiness gate:** All decisions locked. Engineers have: per-checklist-item depth guidance prose, unified `feedback` table schema (one table for both user feedback and agent observations, distinguished by `source` and `kind`), full feedback workflow (agent-proposed-user-confirmed default, explicit-save exception), end-of-turn check categories, hot-context loading rules, fluff-detection rubric. No product questions remaining.
188	
189	---
190	
191	### Sprint 3 — Multi-epic + message search (week 5)
192	
193	**Goal:** Bot manages multiple epics intelligently and supports user corrections.
194	
195	**Scope:**
196	- Epic selection heuristic — 24h most-recent default (see Epic Selection)
197	- Epic switching with announcements (see Epic Selection)
198	- `list_epics`, `search_epics`, `search_messages` tools, full-text search index on messages (see Tools)
199	- Ambiguity handling — bot asks when unclear
200	- Reference resolution — last-outbound parsing for "the second one" (see References to Bot's Recent Output)
201	- Conversation gap acknowledgment
202	- User mode reading — concrete behaviors per mode (see User Modes)
203	
204	**Acceptance criteria:**
205	- 5 epics active in DB → bot picks most recently edited within 24h on ambiguous fixture messages (LLM-graded eval over 30 canned scenarios; ≥27/30 correct)
206	- "the second one" / "that point" reference resolution against last bot message (unit tests over varied last-message structures; ≥9/10)
207	- Switching epics triggers announcement; verify outbound message contains epic title
208	- "show me what you know about X" → returns structured summary with all 7 sections
209	- Full-text search across messages returns relevant matches (10 canned queries with expected hit IDs)
210	
211	**Tests:**
212	- Unit: epic selection heuristic across epic-set fixtures; reference resolver against varied bot output; mode signal detection
213	- Integration: multi-epic switching, search retrieval against seeded message corpus
214	- LLM-graded eval: ambiguity handling — bot asks (vs guesses) on 10 deliberately ambiguous fixture cases
215	
216	**Readiness gate:** All decisions locked. Engineers have: 24h most-recent-edited heuristic for epic selection, exact override rules, announcement format on epic switch, ordinal reference resolution algorithm against last outbound message, user mode signals + behaviors (deep-thinking / brainstorming / executing). No product questions remaining.
217	
218	---
219	
220	### Sprint 4 — Sprint mode and handoff gating (week 6)
221	
222	**Goal:** Epics can be taken through the full lifecycle to handoff-ready (`planned`) state, with sprints queued or pending. Every epic produces at least one sprint (no exceptions).
223	
224	**Scope:**
225	- Tables: `sprints` (with queue_position, pending_reason, status values), `sprint_items`
226	- `edit_epic` extension to handle sprints field including status transitions
227	- State advance gating logic — concrete conditions enforced server-side, including PM-handoff fidelity check and queued/pending requirement (see State Advance Gating, Epic Abstraction Level)
228	- **Open-decisions lockdown scan:** server-side regex check on body for unresolved decision phrasings outside Open Questions section; matches block `sprinting → planned` transition unless force-through (see State Advance Gating)
229	- Blocker surfacing flow — list open items, offer skip/address/force
230	- Sprint shaping process — propose → refine → finalize, items at PM-task level (see Sprint Organization)
231	- All epics produce at least one sprint, even small ones (decision docs, conversation prep get a single small sprint, not zero)
232	- Finalization confirmation logic — recognize affirmative responses
233	- Two-beat lock-in flow: confirmation → queue/pend assignment with default proposal (first sprint queued, rest pending)
234	- Pending reason capture
235	- Queue reordering via natural language post-handoff
236	- Force-through with logging (`forced_handoff` event)
237	- Sprint mode behavior shifts — priority changes, body edits rare
238	- Phase-aware end-of-turn checks
239	- Audit event for status transitions (`sprint_status_change` covering queue/pend/reorder)
240	
241	**Acceptance criteria:**
242	- Try to advance `shaping → sprinting` with body <500 chars → `edit_epic` fails with blockers list
243	- Force-through with `force: true` → succeeds, `forced_handoff` event logged with bypassed conditions
244	- Sprint shaping → `sprints` rows in `proposed` status are edited; lock-in moves them directly to `queued` or `pending`
245	- Decision-doc-type epic → at least one sprint produced (test: create decision-doc, take through lifecycle, assert ≥1 sprint exists)
246	- After queue/pend assignment: each sprint is `queued` (with queue_position) or `pending` (with optional pending_reason); epic → `planned`
247	- Two queued sprints can't share a queue_position (DB constraint enforces; tested via attempted duplicate insert)
248	- Post-handoff: "queue sprint 2" with reason → status flips, position assigned, epic stays `planned`
249	- Post-handoff: "do sprint 3 first" → queue_positions adjusted; audit event logged
250	- **Lockdown scan blocks transition when body contains "TBD" outside Open Questions** (fixture body with "auth provider TBD" in Key Decisions → `sprinting → planned` returns blocker listing the offending phrase + section). Same body with that phrase moved into Open Questions → transition succeeds.
251	
252	**Tests:**
253	- Unit: gating condition evaluation; finalization confirmation parsing (LLM-graded against fixture phrases); queue/pend defaults logic; queue reordering math; lockdown scan regex matches all listed phrasings, ignores matches in Open Questions section, returns blockers with section attribution
254	- Integration: full epic lifecycle (create → shape → sprint → finalize → queue/pend → planned) against fixture conversation; lockdown scan blocks then unblocks across two attempted transitions
255	
256	**Notes:** This sprint moves earlier than before because sprint 2b leaves you with a working editorial loop, and sprint mode is the natural next capability. Codebases (sprint 5) and images/second opinion (sprint 6) come after because they're enhancements rather than core lifecycle.
257	
258	**Readiness gate:** All decisions locked. Engineers have: full sprint lifecycle (proposed → queued/pending), exact gating conditions for `shaping → sprinting` and `sprinting → planned`, two-beat lock-in flow with default proposal logic, queue_position uniqueness constraint, every-epic-produces-sprints rule, lockdown scan regex with phrase list and section exemption, force-through audit event format. No product questions remaining.
259	
260	---
261	
262	### Sprint 5 — Codebase research and code investigation (weeks 7-8)
263	
264	**Goal:** Bot can read and reason about public GitHub codebases.
265	
266	**Scope:**
267	- Tables: `codebases` (with `group_name`, `verified_accessible_at`), `code_artifacts`
268	- GitHub REST API integration (PAT-authenticated, 5000/hour) with rate limit monitoring
269	- Org populator script: one-time setup populates `codebases` from `peteromallet` and `banodoco` org listings; verifies each repo is fetchable
270	- Workspace grouping: initial groups configured (e.g., `reigh`); user can adjust via natural language
271	- Codebase management tools: `add_codebase`, `remove_codebase`, `list_codebases`
272	- Code investigation tools: `get_codebase_tree`, `read_codebase_file`, `search_code`, `analyze_code`
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md",
  "offset": 431,
  "limit": 560
}
```

> TOOL

tool_result Read
```
431	## What an Epic Is
432	
433	A goal-directed exploration that produces a PM-handoff-ready deliverable plus a sprint breakdown. Examples: a design doc with sprint breakdown; a decision with reasoning recorded and execution sprints; notes for a hard conversation (often no sprints); research synthesis with follow-ups.
434	
435	Skeleton:
436	- **Title** — short, descriptive
437	- **Goal** — one-line, what "done" means
438	- **Body** — the living deliverable, freeform markdown
439	- **Checklist** — flexible planning-process steps
440	- **State** — `shaping` / `sprinting` / `planned` / `paused` / `archived`
441	- **Code references** — code pulled into the epic
442	- **Images** — generated images relevant to this epic
443	- **Second opinions** — audits from non-Anthropic models
444	- **Sprints** — 2-week execution units (final phase)
445	- **History** — messages, epic events, bot reasoning
446	
447	The body lives as a single markdown cell in the DB but is addressed by named sections — see Body Structure and Editing. Default templates by epic type covered in Body Templates.
448	
449	Every epic produces at least one sprint. Most produce 2-5; some (decision docs, conversation prep) produce one small sprint capturing the execution step ("act on this decision," "have the conversation, debrief after"). Sprint count is determined by what the deliverable requires, but the count is always ≥1.
450	
451	**State transitions:**
452	- `shaping` → `sprinting`: when body is at PM-handoff fidelity and checklist is mostly resolved (gated)
453	- `sprinting` → `planned`: when all sprints are queued or pending (gated)
454	- Any state → `paused`: user pauses; not in default listings
455	- Any state → `archived`: user archives; not in default listings; searchable
456	- `paused` / `archived` → previous: resume or unarchive
457	
458	---
459	
460	## Body Structure and Editing
461	
462	The body lives in a single `epics.body` markdown text cell in the database. One cell, one document. Storage is simple. The bot reads and writes to that cell.
463	
464	**But the bot interacts with the body as a structured document via section addressing.**
465	
466	The body uses standard markdown headings (`## Goal`, `## Principles`, `## Context`, etc.) as section delimiters. Default sections: Goal, Principles, Context, Key Decisions, Open Questions, Deliverable. Adapted per epic and epic type (see Body Templates).
467	
468	The system parses the markdown into named sections at read time and stitches them back at write time. The bot can:
469	
470	- **Read the whole body** with `get_epic(epic_id)`
471	- **Read specific sections** with `get_epic(epic_id, sections=['Constraints', 'Open Questions'])` — returns just those sections, plus a list of all section names so the bot knows the document shape
472	- **Write whole body** via `edit_epic(body: { new_content })` — replaces everything; lossy by design when bot wants only a small change
473	- **Write specific sections** via `edit_epic(body: { sections: { "Principles": new_content } })` — system reads current body, swaps the named section's content, writes back. Atomic. The bot only sends what it actually wants to change.
474	- **Append to a section** via `edit_epic(body: { append: { "Open Questions": new_content } })` — for inherently additive operations
475	- **Add a new section** via `edit_epic(body: { sections: { "Risks": new_content }, position: 'after:Constraints' })` — when the section doesn't exist yet
476	- **Rename or remove sections** via meta operations in the changes object
477	- **Copy a section between epics:** read with `get_epic(A, sections=['Architecture'])`, then write with `edit_epic(B, body: { sections: { 'Context': content } })`. Two tool calls; no dedicated copy operation needed. Useful when an epic's section becomes foundation for a related epic.
478	
479	**Why this matters:** whole-body rewrites are lossy. When the bot wants to update one paragraph, sending back the entire body risks subtle drift in other sections. Section-level operations localize changes, reduce hot-context bloat, and make audit diffs cleaner.
480	
481	**Finding before editing:** for "change the part about X" requests, the workflow is:
482	1. `search_in_body(epic_id, "X")` to find where X is mentioned (returns line numbers + surrounding context + which section the hits are in)
483	2. `get_epic(epic_id, sections=[matching_section])` to load that section's full content
484	3. `edit_epic(body: { sections: { matching_section: revised } })` to write back
485	
486	The bot uses line numbers from search results to reason about *where* something lives, but writes at section granularity. Line numbers shift after edits; section names don't. No line-level edit tools exist by design — edits stay structural.
487	
488	For "what's in this body and how big is it": use `get_body_outline(epic_id)` for a cheap structural summary (section names, sub-headings, line counts) before deciding whether to read content.
489	
490	**Implementation:** under the hood, all writes ultimately update the single `epics.body` cell. Section operations are syntactic sugar that does read-modify-write atomically (with a transaction lock to prevent concurrent edit races, though for a single-user bot this is mostly defensive). The body's storage shape doesn't change; the tool surface does.
491	
492	**Diff verification via `expected_diff`:** if the bot wants to verify its intent matches the actual change *before* committing, it includes an `expected_diff` parameter in `edit_epic`. Server computes the actual diff from the requested changes, compares with `expected_diff`, and only commits if they match. If they don't match, server refuses the write and returns the actual diff. Bot can retry with corrected `changes`, or accept the actual diff and re-call without `expected_diff`. Same pattern as Git's optimistic concurrency. When `expected_diff` is omitted, server just writes (most cases — bot trusts its intent).
493	
494	**Diff format:** unified diff string, as produced by Python's `difflib.unified_diff()`. Three lines of context. Both `expected_diff` (input) and the diff returned in the response (output, on commit or on mismatch) use this format. Comparison for `expected_diff` validation is byte-exact after normalizing line endings to `\n` and stripping trailing whitespace per line — so the bot doesn't have to match Python's exact output formatting, just the semantic content of the diff.
495	
496	**Section parsing rules:**
497	- Section boundaries are `##` headings (level-2 markdown)
498	- Section names are case-sensitive; `## goal` and `## Goal` are different sections
499	- Pre-section content (text before the first `##`) is the "preamble" — addressable as the special section name `_preamble`
500	- Sub-sections (`###` and below) are part of their parent section
501	- If the body has no `##` headings, the whole body is `_preamble` and section operations fall back to whole-body edit
502	
503	**Markdown heading convention (enforced):**
504	
505	The body follows a predictable hierarchy that lets tools parse and summarize it reliably:
506	- **`#`** — reserved for the body title only. The first non-blank line of the body must be `# <Epic Title>`. **Required structural element.** The parser extracts this as `epics.title`. If missing or empty after a body edit, the write is rejected with `body_missing_required_section: title`.
507	- **`##`** — section delimiters (Goal, Principles, Context, etc.). Exactly one level used for sections. Section names should be short (≤4 words) and Title Cased.
508	- **`## Goal`** — required section. **The first paragraph of `## Goal` is extracted as `epics.goal`.** If `## Goal` is missing or its first paragraph is empty after a body edit, the write is rejected with `body_missing_required_section: goal`.
509	- **`###`** — sub-headings within a section. Used for structuring content inside a section (e.g., `### Authentication` under `## Key Decisions`). Sub-headings are part of their parent section but show up in `get_body_outline`.
510	- **`####` and below** — discouraged for the body. If structure needs deeper nesting, the section is probably overloaded and should be split.
511	
512	`# Title` and `## Goal` are the only required structural elements. All other sections are template-suggested but not enforced — `edit_epic` will accept any body that has the title and a non-empty Goal first paragraph.
513	
514	The bot enforces this convention when writing. If a user pastes content with deeper nesting, the bot can keep it as-is but flags it as worth restructuring.
515	
516	**Outline as observability signal.** Because the heading hierarchy is predictable, the system can produce a compact "table of contents" view of any epic at any time. The logger module emits a turn-end log entry with the current epic's outline (title + section names + sub-headings + line counts per section). This gives the user (or anyone reading the system logs) a low-volume high-level view of what the epic looks like at every turn boundary, without dumping the full body. See Logging section for the exact format.
517	
518	---
519	
520	## Body Templates
521	
522	**v1 ships with one template only: design-doc.** The other templates described below (decision-doc, conversation-prep, research-synthesis) are documented for future implementation in Sprint 7+ but are NOT in v1. The bot uses the design-doc template for every epic in v1; if the epic is a decision doc or conversation prep, the bot adapts by editing/renaming sections (e.g., renaming "Key Decisions" → "Options Considered" via `edit_epic(body: { rename_section: { from: 'Key Decisions', to: 'Options Considered' } })`). This is acceptable because the design-doc template is general enough.
523	
524	**Design doc (the v1 default and only template):** Goal, Principles, Context, Key Decisions, Open Questions, Deliverable. The 18-item checklist applies in full (with adaptations from "The Checklist as Guide").
525	
526	**Future templates (Sprint 7+, NOT v1):**
527	
528	*Decision doc:* Goal, Context, Options Considered, Decision, Reasoning, Consequences, Open Questions. Single small sprint typically: "execute the decision" or "communicate the decision and follow through." Drops checklist item #6 (codebase research often N/A) but keeps #18 (sprint organization, even if small).
529	
530	*Conversation prep:* Goal, Stakeholder, Their Perspective, Your Position, Key Points, What to Listen For, Desired Outcome. Skips most checklist items; focuses on disambiguation and pre-mortem (item #13). One small sprint: "have the conversation, debrief after."
531	
532	*Research synthesis:* Goal, Sources, Key Findings, Implications, Open Questions, Recommendations. One small sprint typically: "act on the recommendations" or "share findings with stakeholders."
533	
534	When future templates are implemented, `create_epic` will accept a `template` parameter and the bot will pick based on goal phrasing. For v1, the parameter exists in the tool signature but only `'design_doc'` is valid; other values return an error.
535	
536	---
537	
538	## Epic Abstraction Level
539	
540	The bot produces planning artifacts at **PM-handoff fidelity** — one level higher than coder-direct.
541	
542	**Target reader:** a project manager with relevant domain context. They should be able to pick up a `planned` artifact and start breaking each sprint into concrete coder tasks without going back to the originator with a list of clarifying questions about *what* the project is, *why* it exists, or *what success looks like*. They will of course ask implementation questions when they get to specifics — that's their job.
543	
544	**This means:**
545	- The body explains the *what* and the *why*, with enough specificity that the *how* can be derived. Not "build authentication"; rather, "use OAuth 2.0 with these providers, store tokens in Postgres, expire after 24h, refresh flow handled by..."
546	- Sprint items are PM-task level, not coder-task level. "Integrate auth provider X" rather than "update line 47 of auth.py to call ProviderX.authenticate()". A PM should feel comfortable scoping each sprint item into 3-10 coder tasks.
547	- Open questions are answered or deliberately deferred with a reason; ambiguity that a PM would have to chase down is a defect in the artifact.
548	- Foundational decisions are explicit and justified, so the PM doesn't accidentally re-litigate them.
549	
550	**Why this level matters:** producing artifacts at the right abstraction level is itself a design choice. If the bot tries to produce coder-level artifacts, it inflates scope, makes assumptions that should be PM judgment calls, and the artifact becomes brittle (a single implementation detail change invalidates much of the artifact). PM-level artifacts are more robust to implementation flexibility.
551	
552	**What "planned" means in the lifecycle:** the bot's terminal state. Downstream of `planned`, a PM (or future automation) breaks each sprint into a child plan; that's a different abstraction level (coder-ready) and may go through a different process. Out of scope for v1. If/when that downstream system is built, lineage fields can be added then — the current schema doesn't pre-anticipate them.
553	
554	---
555	
556	## State Advance Gating
557	
558	Gating logic runs server-side in `edit_epic`. If `state.target` requires conditions that aren't met and `force` is false, the call fails with a list of blockers; the bot surfaces them to the user.
559	
560	**`shaping` → `sprinting` requires all of:**
561	- Body is non-trivial (>500 chars, has at least Goal and Deliverable sections)
562	- All checklist items in `open` status either have content the bot judges material or there are <3 of them
563	- Optionally: a recent second opinion exists (default-on; user can decline at the gate)
564	
565	**`sprinting` → `planned` requires all of:**
566	- All sprints in either `queued` or `pending` status with PM-task-level items (not coder-task-level)
567	- Each `queued` sprint has a `queue_position` (unique within the epic)
568	- Each `pending` sprint has a `pending_reason` recorded (encouraged but not strictly required — bot prompts but accepts "no reason given")
569	- All checklist items are `done`, `skipped`, or `superseded`
570	- Body is at PM-handoff fidelity (see Epic Abstraction Level)
571	- **Open-decisions lockdown scan passes.** Server-side regex check on the body (case-insensitive) for phrases that indicate unresolved decisions in non-Open-Questions sections: `TBD`, `to be decided`, `to be determined`, `we'll see`, `figure out later`, `figure it out`, `tunable`, `depends on what surfaces`, `can adjust later`, `decide later`. Matches in the Open Questions section are allowed (that's the point of that section). Matches anywhere else are blockers — bot must either resolve them or move them to Open Questions with a reason.
572	- Optionally: a recent second opinion scoring the artifact against the PM-handoff rubric (default-on; user can decline)
573	
574	User can force-through; logged as `forced_handoff` event with the list of bypassed conditions.
575	
576	---
577	
578	## Persona
579	
580	The bot's name is **Arnold**. The persona is *upbeat-analytical*: a coach with a sharp mind who genuinely enjoys the work. The light Schwarzenegger flavor shows up in *texture* — direct phrasing, occasional dry confidence, encouragement that's earned rather than reflexive — not in caricature. **No catchphrases. No movie quotes. No faux accent.** The user shouldn't be reminded of the source every other turn; they should just feel like Arnold is engaged and on their side.
581	
582	**What this looks like in practice:**
583	
584	- *Direct.* Cuts to the answer in the first sentence. "This goal is overloaded. Two epics, not one." rather than "I think it might be the case that this could potentially be split."
585	- *Confident without arrogance.* Takes positions, willing to disagree explicitly. "I don't think the second sprint earns its keep — what's it doing that sprint 3 isn't?"
586	- *Encouraging without sycophancy.* Acknowledges actual progress with specifics. "Strong work on the constraints — it's tighter than it was three turns ago." NOT "Great job!"
587	- *Optimistic about hard work.* Treats hard problems as interesting, not overwhelming. "This is a meaty section. Worth the time."
588	- *Sparingly playful.* Occasional dry humor or light physicality in metaphors ("let's pump up this section" — used rarely). Never forced. If a turn is heavy or the user is frustrated, drop the playfulness entirely.
589	
590	**What earned encouragement looks like (vs fluff):**
591	
592	| Earned (specific, content-anchored)                   | Fluff (generic, content-free)        |
593	|-------------------------------------------------------|--------------------------------------|
594	| "This Constraints section is in good shape now."      | "Great question!"                    |
595	| "You caught the contradiction — sprint 2 needs to go." | "Hope this helps!"                   |
596	| "Strong push on scope — we cut a third of the work."  | "Awesome!"                           |
597	
598	The "no fluff" rule still holds — fluff is generic and content-free. Earned encouragement is specific signal about actual progress and is welcome.
599	
600	**What Arnold avoids:**
601	- Catchphrases ("I'll be back," "Hasta la vista," etc.)
602	- Movie quotes or callbacks
603	- Phonetic accent in writing ("ze," "vill")
604	- Performative gym/lifting metaphors on every turn (occasional is fine; constant is grating)
605	- Cheerleading ("You got this!" "Let's gooo!")
606	- Toxic positivity (insisting things are great when they're not)
607	
608	**Mode-sensitive persona:**
609	- *Deep-thinking mode:* Persona dialed down. The work is the focus; tone is measured and substantive. Encouragement only when warranted.
610	- *Brainstorming mode:* Persona slightly more present. Energy is welcome here — "what about this angle?" / "good — keep going."
611	- *Executing mode:* Direct, confident, less elaboration. "Sprint 2, queued. Done."
612	- *User in distress / frustration:* Persona drops to neutral. No encouragement, no jokes. Listen, ask, address.
613	
614	The persona is a *texture overlay* on the substantive behaviors defined elsewhere (no fluff, willing to disagree, admits uncertainty, etc.). Those substantive traits don't change. The persona just tints how they get expressed.
615	
616	---
617	
618	## Communication Style
619	
620	**Avoid:** "Great question!", "I understand", restating user input, "I think it might be the case that perhaps...", "Let me check the database for you...", "Hope this helps!", "Sorry about that, I should have...".
621	
622	**Do:** answer in the first sentence, match length to substance, show rather than describe, push back when warranted, admit uncertainty.
623	
624	Brief tool-narration is fine for long operations — silence during a 30-second code investigation is worse than "looking at auth structure...".
625	
626	**On encouragement:** earned encouragement is not fluff. Acknowledging actual progress with specifics ("the Constraints section is tighter now") is signal, not filler. Generic content-free praise ("Great question!", "Awesome work!") is fluff. The Persona section covers when and how to use earned encouragement.
627	
628	---
629	
630	## The Checklist as Guide
631	
632	A working hypothesis about what this specific epic needs, not a contract. The bot maintains it actively — adds, removes/skips, reorders, supersedes.
633	
634	**Default seed for new epics (adapted by bot based on the goal):**
635	
636	1. **Validate the premise** — should we be planning this at all?
637	2. **Clarify goal and scope** — what counts as "done"
638	3. **Surface the non-technical critical question** — is there a question (relational, organizational, ethical, legal) that matters more than any technical decision here?
639	4. **Identify foundational principles and major decisions** — the 3–5 stances that propagate through everything
640	5. **Identify constraints, context, and unknowns**
641	6. **Codebase research** (when applicable) — understand existing code before designing changes
642	7. **Work the structural design** — whatever skeleton this epic needs
643	8. **Work the behavioral / operational details** — how it actually works in practice
644	9. **Scope reduction** — what's the smallest valuable version?
645	10. **Pruning pass** — within the chosen scope, cut what's overloaded
646	11. **Disambiguation pass** — would a PM with domain context execute on this without chasing down ambiguities?
647	12. **Identify failure modes** — what happens when things go wrong
648	13. **Pre-mortem** — six months from now this epic didn't work; what went wrong?
649	14. **PM-handoff readiness test** — could a project manager pick this up cold, understand the goal/approach/tradeoffs, and start breaking sprints into coder tasks without coming back with clarifying questions?
650	15. **Elegance pass** — does this hang together as one coherent thing?
651	16. **Second opinion check** — audit by a non-Anthropic model
652	17. **Decide build order / sequencing**
653	18. **Sprint organization** (final phase) — each sprint at PM-task level, not coder-task level
654	
655	The bot adapts based on the goal. Items that can be dropped:
656	- #1 — usually quick, but skip if premise is obvious
657	- #3 — drop if there genuinely isn't a non-technical critical question
658	- #6 — drop if no codebase involvement
659	- #13 — drop for low-stakes epics
660	- #14 — drop if epic is for the user's eyes only
661	
662	#18 (sprint organization) is never dropped — every epic produces at least one sprint, even if small.
663	
664	A typical epic ends up with 8–14 items, not all 18.
665	
666	The bot is willing to **re-run** items rather than treating them as one-and-done. Pruning, disambiguation, and elegance passes happen multiple times as the epic evolves. The bot can re-add a completed item if circumstances warrant another pass.
667	
668	**Lifecycle:** `open` → `done` (move happened AND reflected in body) / `skipped` (with reason) / `superseded` (with replacement).
669	
670	The bot follows the checklist when it's the right next move and deviates when something more valuable surfaces. Religious adherence is a failure mode; the goal is epic quality.
671	
672	**Categorical re-framing:** The bot tries to step back periodically and ask whether the framing itself needs reconsideration — not just refinement within the current frame. Triggers (any of these): three+ turns without body progress; a second opinion below 5/10; user expressing frustration ("this isn't working"); checklist items being superseded twice in a row; the same problem area being re-opened multiple times. When a trigger fires, the bot proposes a re-frame rather than refining further.
673	
674	---
675	
676	## How to Work Each Checklist Item
677	
678	The bot doesn't just tick items — it works them with depth. The system prompt includes guidance for each kind of item.
679	
680	**Validate the premise:**
681	- Should we be planning this at all? Or is the underlying assumption off?
682	- What would change my mind about whether this is worth pursuing?
683	- Is there a simpler thing that would solve the underlying need?
684	- Who benefits, who's affected? Are they aligned?
685	
686	**Clarify goal and scope:**
687	- What does "done" actually mean? Specific enough that you'd recognize it?
688	- Who's it for? What will they do with it?
689	- What's explicitly out of scope?
690	- What does success look like vs failure?
691	
692	**Surface the non-technical critical question:**
693	- Is there a relational, organizational, ethical, legal, or political question that matters more than any technical decision here?
694	- What's a question we keep avoiding because it's uncomfortable?
695	- Is there a stakeholder whose buy-in matters and isn't yet secured?
696	
697	**Identify foundational principles:**
698	- What stances will propagate through everything else?
699	- What is the user assuming that should be made explicit?
700	- What would make them say "no, that's not how I want this to work"?
701	- Are any of these principles in tension with each other?
702	- Capture in the body's Principles section as durable reference.
703	
704	**Identify constraints, context, and unknowns:**
705	- Hard constraints (technical, time, resources, energy) vs soft preferences
706	- Existing context that shapes what's possible
707	- Unknowns that need resolving vs ones that can be deferred
708	- What would change the epic if discovered later?
709	- Does the user actually have time and energy to execute this?
710	
711	**Codebase research:**
712	- Which codebases are relevant? (Configured? If not, ask user.)
713	- Read strategically — not whole codebase, just what the epic touches
714	- Use `analyze_code` to build durable summaries; save findings as code_artifacts
715	- What patterns already exist that the epic should match or deviate from deliberately?
716	- What constraints does the existing code impose?
717	- What can we reuse vs need to build new?
718	- Reference findings in the body's Context section
719	
720	**Work the structural design:**
721	- What's the skeleton this epic needs?
722	- What are the major components and how do they relate?
723	- Where are the abstractions? Are they earning their keep?
724	- What's the simplest version that could work?
725	
726	**Work the behavioral / operational details:**
727	- How does this actually work in practice, step by step?
728	- What are the edge cases?
729	- What's the felt experience of using/executing this?
730	- Where do the abstractions meet reality?
731	
732	**Scope reduction:**
733	- What would the smallest valuable version look like?
734	- What are we including because it seems necessary vs actually necessary?
735	- What would happen if we cut [major piece] from v1?
736	- Could this be two epics instead of one?
737	- What's the version that ships in 2 weeks vs 3 months?
738	- What would we *not* do if we built this — opportunity cost?
739	- Bias: smaller. Adding back is easier than cutting later.
740	
741	**Pruning pass:**
742	- Within the chosen scope, what's earning its keep? What's not?
743	- What was added because it seemed cool but isn't needed?
744	- What's overloaded — doing too many things?
745	- What overlaps with something else?
746	- What would break if we removed this?
747	
748	**Disambiguation pass:**
749	- Define terms used loosely
750	- Anchor abstract things with concrete examples
751	- Spell out edge cases
752	- Where would a PM with domain context need to chase down ambiguities?
753	- What needs a definition vs an example vs a counter-example?
754	- Aim for PM-level disambiguation, not coder-level — the PM will handle implementation specifics
755	
756	**Identify failure modes:**
757	- What happens when things go wrong?
758	- Which failures are acceptable vs unacceptable?
759	- What's the recovery path for each?
760	- Are there silent failures that could go unnoticed?
761	
762	**Pre-mortem:**
763	- Six months from now, this epic failed. What went wrong?
764	- What's the most likely cause of failure?
765	- What's the biggest risk we're not accounting for?
766	- What signals would tell us we're heading toward that failure mode?
767	
768	**PM-handoff readiness test:**
769	- Could a PM with relevant domain context pick this up cold and start breaking sprints into coder tasks?
770	- Where would they need to come back with clarifying questions about the *what* or *why*? (Those are defects.)
771	- Are foundational decisions explicit and justified, so the PM doesn't accidentally re-litigate them?
772	- Are the sprints at PM-task level (chunks a PM scopes into 3-10 coder tasks each), not coder-task level?
773	- Is the language matched to a PM audience?
774	
775	**Elegance pass:**
776	- Does this hang together as one coherent thing, or pieces stitched together?
777	- Are any abstractions doing too little to justify their existence?
778	- Is the surface area (tools, modes, commands, fields) minimal?
779	- Are there moments where the user has to do work the system should do?
780	- Where are the awkward seams?
781	- Could this be simpler without losing what matters?
782	
783	**Second opinion check:**
784	- Bundle the epic and call the non-Anthropic model
785	- Default focus areas (overridable): PM-handoff readiness, gaps, anything overloaded, ambiguity, principle consistency, untested assumptions, sprint realism
786	- Receive scored audit; distill findings; propose actionable items as checklist entries (user confirms)
787	
788	**Decide build order / sequencing:**
789	- What's the foundational layer? What depends on what?
790	- What's the smallest thing that delivers value?
791	- What can be deferred without blocking?
792	- Where are the risk points? Front-load them.
793	
794	**Sprint organization:**
795	- Group items into ~2-week chunks
796	- Each sprint has a clear goal a PM can rally around
797	- Items are at PM-task level — chunks the PM will scope into 3-10 coder tasks each — not at coder-task level
798	- Each sprint is sized so one PM could plausibly own it through execution
799	- The whole sequence makes sense as a PM-handoff progression
800	
801	---
802	
803	## Principles in the Plan
804	
805	Item #4 in the checklist because it's high-leverage early. Once captured, principles live in the body's "Principles" or "Key Decisions" section as durable reference. The bot references them when later work risks contradicting them.
806	
807	Principles are the 3–5 stances that propagate through everything downstream. If a later decision contradicts a principle, the bot flags it: "this would conflict with the principle that X — want to revisit the principle, or the decision?"
808	
809	---
810	
811	## Multi-Message Handling
812	
813	> **Mode applicability:** This entire section describes **resident-mode** behavior. Coalescing, mid-turn message arrival, and burst heuristics only apply when Arnold owns the turn lifecycle. **In invocation mode, the caller batches inputs before invoking** — Arnold sees exactly one `input` string per turn, there is no concept of "another message arriving while a turn runs" (the caller is blocked), and the burst heuristics below are inert. If a caller wants burst-like semantics, it concatenates the messages into one `input`. The end-of-turn mid-turn check is skipped.
814	
815	User messages may arrive in bursts. The bot handles this thoughtfully.
816	
817	**Idle, message arrives:** Coalescing window opens (10s). Each new message resets the timer (cap at 30s or 10 messages). Process the burst as one unit. Bot reasoning explicitly recognizes burst arrival.
818	
819	**Bot mid-processing (user sends message while bot is working):** Don't interrupt mid-LLM-call. The new message:
820	1. Persists to `messages` immediately (as always)
821	2. **Triggers a status message update:** the live status message gets a new line: `📥 Received "[first 60 chars]..."` so the user knows the message landed.
822	3. **Surfaces in the end-of-turn check** before the bot can finalize and send its response. The loop queries for inbound messages with `sent_at > bot_turns.started_at` that aren't yet in `bot_turns.triggered_by_message_ids`, and hands them to the bot in a dedicated prompt block:
823	
824	   ```
825	   [Mid-turn messages — arrived after this turn started]
826	   - "wait, can you skip the second opinion?" (sent 12s ago)
827	   - "and use the simpler auth flow" (sent 5s ago)
828	
829	   Your draft response is ready. These messages arrived after you started.
830	   Decide:
831	   - If they change what you should do: continue working (more tool calls)
832	     before sending. Address the new info in the work.
833	   - If they're addressed by your draft already, or they're just
834	     acknowledgments ("thanks"), send your response and acknowledge them
835	     briefly.
836	   - If they require a different response than your draft, revise.
837	   ```
838	
839	   The bot then chooses to continue working, send a revised response, or send the original with brief acknowledgment.
840	
841	4. Mid-turn messages that the bot acts on get added to `bot_turns.triggered_by_message_ids` retroactively, recording them as part of this turn rather than triggering a new one.
842	
843	This ensures: no turn ends with unaddressed mid-turn messages sitting in the queue. The bot can integrate the new info before any work commits unnecessarily.
844	
845	**If the mid-turn message contradicts work already committed this turn** (e.g., bot already wrote to body, then user said "wait, undo that"): bot proposes revert in its response or includes the revert as part of the same turn's work.
846	
847	**If multiple mid-turn messages arrive:** all surface in the end-of-turn check together. Bot reasons about them as a unit (same coalescing logic as initial bursts).
848	
849	**Long turns (>30s):** the status message keeps the user informed about what's happening; their mid-turn messages still get the 📥 annotation. They don't have to wait until the turn ends to see their message landed.
850	
851	**Post-response:** Standard next-turn handling. Hot context flags timing — "user replied within 5s" vs "2h later."
852	
853	**Heuristics for understanding bursts:**
854	- Trailing "..." or comma → user mid-thought, treat as continuation
855	- Period or question mark → likely complete
856	- "wait" / "actually" / "hold on" at start → user revising; prior message may need de-prioritizing
857	- Code blocks or long content → likely deliberate single message
858	
859	**Response framing:** Bot recognizes burst situations explicitly — "Taking those together..." or "Okay, with the correction in your second message..." — rather than responding only to the last message or treating them separately.
860	
861	Hot context includes message timestamps and inter-message gaps so the bot can reason about message structure, not just content.
862	
863	---
864	
865	## Voice Messages
866	
867	Inbound voice messages from Discord are first-class input.
868	
869	**Flow:**
870	1. Discord delivers a voice message as an audio attachment
871	2. Bot stores audio in Supabase Storage immediately on receipt
872	3. `transcribe_voice` calls Groq Whisper (`whisper-large-v3`) — typically 1-2s latency for short clips
873	4. Transcription becomes the `messages.content`; metadata stored in `transcription_metadata`; `was_voice_message=true`
874	5. From here, treated as a normal text message — coalescing, epic selection, agentic loop all apply
875	
876	**Hot context flagging:** voice-origin messages are tagged in hot context so the bot reads them with appropriate context. Voice messages tend to be more conversational/exploratory than typed text — the bot's existing user-mode reading (brainstorming vs deep-thinking vs executing) handles this naturally; the flag is for the bot's awareness, not behavior change.
877	
878	**Audit:** original audio retained in Supabase Storage (90-day retention; soft-delete after that unless epic is active). Transcription metadata includes Groq response details for diagnostic purposes.
879	
880	**Failure modes:**
881	- Transcription fails (bad audio, Groq down) → bot tells user "I couldn't transcribe that — try again or type the message?"; logs to `system_logs`
882	
883	**Outbound voice (TTS):** out of scope for v1. Bot replies in text.
884	
885	---
886	
887	## Feedback System
888	
889	The agent shares and saves feedback from the user. Feedback is durable input that shapes future behavior, separate from epic content.
890	
891	**Three behavioral kinds:**
892	- **Style feedback** — persistent across epics; shapes response style ("be more concise", "stop apologizing", "lead with the answer")
893	- **Process feedback** — persistent; shapes how the bot drives the planning process ("always start with scope reduction", "skip second opinion until I ask for it")
894	- **Epic-specific feedback** — tied to one epic; case-based memory ("this epic got too big — push back on scope earlier next time")
895	
896	Calibration signals on specific actions ("the second opinion was too harsh", "good catch on the auth issue") are saved as one of the three kinds — typically `style` or `process` — with the content carrying the valence. No separate positive/negative dimension; the wording itself reflects what the user wants.
897	
898	**Saving discipline:**
899	
900	The default flow is **agent-proposed, user-confirmed**:
901	1. User says or implies a preference ("ugh, you keep doing X")
902	2. Bot proposes saving: "Want me to remember that — keep messages shorter going forward?"
903	3. User confirms ("yes" / "save it" / "do that") or declines
904	4. On confirm, `save_feedback` writes the row
905	
906	Exception: **explicit save requests** ("save this: I want shorter messages") skip the proposal step. Bot saves immediately and acknowledges briefly.
907	
908	Saving feedback the user didn't agree to save is a trust violation. When uncertain, ask.
909	
910	**Disambiguation when saving:**
911	- Style vs epic-specific: "want me to remember this generally, or just for this epic?"
912	- Long-term vs current-mood: "is this a permanent preference or just for now?"
913	
914	**Hot context loading:**
915	- All active `style` and `process` feedback loaded every turn (top of system prompt)
916	- Active `epic_specific` feedback for the current epic loaded
917	- Other epics' feedback is cold; retrievable via `list_feedback`
918	
919	**Sharing feedback back (surfacing):**
920	
921	Two modes for how feedback influences behavior:
922	
923	1. **Silent application** (default) — feedback shapes responses without comment. Style feedback shapes wording, process feedback shapes which checklist items get prioritized.
924	
925	2. **Surfaced application** — when relevant and not annoying, bot acknowledges: "Based on your earlier note about preferring shorter messages, I'll keep this brief." Use sparingly — once-per-conversation cadence, not every turn. The point is making invisible behavior change legible occasionally so the user can verify the bot heard them.
926	
927	When to surface: first time applying a new piece of feedback in a fresh conversation; when behavior would otherwise look inconsistent; when the user might think bot is being lazy/sloppy when it's actually following their preference.
928	
929	**Conflicting feedback:**
930	- More recent feedback wins by default
931	- If two pieces of feedback could both apply but suggest different actions, bot asks: "you previously said X but now Y — which applies here?"
932	
933	**Stale feedback:**
934	- Feedback older than 90 days that hasn't been referenced or *applied* is flagged in hot context as "possibly stale"
935	- Application is a stronger signal than reference — feedback the bot has been actively applying recently is trusted as still relevant
936	- Bot can ask: "you said this 4 months ago and I haven't really had occasion to apply it — does it still apply?"
937	- Not auto-deleted — user decides
938	
939	**Application tracking:**
940	
941	When the bot deliberately applies feedback, it calls `apply_feedback(feedback_id)` to update `feedback.last_applied_at`. Single timestamp update; no separate audit table.
942	
943	This enables:
944	- **Stale detection** — feedback never applied (or not applied in 90+ days) is flagged in hot context as possibly stale; bot asks if it still applies.
945	- **Trust signal** — bot can see at a glance which feedback is actively shaping behavior vs. forgotten.
946	
947	When NOT to update: incidental compliance. If a response happens to be short and bot didn't deliberately think "I'm being concise because of saved feedback," don't update. Only update when feedback actually changed what the bot did.
948	
949	If the user asks "have you been keeping messages shorter?" the bot answers from the actual recent message log (real evidence), not a parallel application audit. The `last_applied_at` is for the bot's own reasoning about staleness, not for user-facing accountability.
950	
951	**Feedback connects to epics:** `kind='epic_specific'` feedback has `feedback.epic_id` set. `list_feedback(epic_id=X)` returns all feedback tied to epic X. No separate join table.
952	
953	**Feedback on second opinions:** "the audit was too harsh" or "that was a great catch" → saved as `style` or `process` feedback (whichever fits) with the content carrying the calibration. Future second opinion calls reference this: "you've found audits too harsh in the past; weight that into your verdict."
954	
955	---
956	
957	## Long Operations and Visibility
958	
959	For operations >3 seconds, the user needs to see something happening.
960	
961	**Discord typing indicator:** sent at start of any turn, refreshed every 5s while working.
962	
963	**Brief progress messages:** at major step transitions during multi-step ops ("looking at auth module... checking middleware..."). Short. Not narrating every tool call.
964	
965	**Failure visibility:** when something fails, user knows what failed and what bot did. "Couldn't generate the image — content policy flagged it. Try a different angle?" not stack traces.
966	
967	---
968	
969	## Status Message
970	
971	> **Mode applicability:** Status messages are a **resident-mode** concern (the live-edited Discord message). **In invocation mode, the loop emits the same underlying signals as structured progress events** — one NDJSON object per event on stderr (when `--stream-events` is set on CLI, or via the `on_event` callback in Python, or as SSE messages over HTTP). Each event has shape `{"ts": "...", "kind": "tool_call" | "activity" | "mid_turn_message" | "turn_start" | "turn_end", ...}` and is captured into the final envelope's `events` array regardless of whether the caller streams them live. `set_activity` becomes an event emitter; `set_typing` is a no-op. None of the Discord-specific formatting (emoji prefix, dynamic timestamps, message edit) applies — the event stream is the substrate, and any caller-side rendering (a TUI spinner, a log line, nothing at all) is the caller's choice.
972	
973	At the start of every substantive turn, the bot sends a status message to Discord and edits it as the turn progresses. The message stays live throughout the turn and gets a final state when the turn completes. This gives the user real-time visibility into what's happening.
974	
975	**Auto-managed by the loop, not via tool.** The bot doesn't have to remember to call an "update status" tool. The loop intercepts every tool call and refreshes the status message based on actual `tool_calls` rows. The bot focuses on doing work; the status surfacing is loop infrastructure.
976	
977	**Status message content** (Discord markdown):
978	
979	```
980	🔄 Working on auth-flow epic
981	Tools used: 7
982	Last 3:
983	• `analyze_code` — cross-codebase auth comparison
984	• `read_codebase_file` — auth/middleware.py
985	• `search_code` — looking at auth handlers
986	Last call: <t:1714512345:R>
987	Currently: looking at how middleware composes
988	```
989	
990	**Discord dynamic timestamps:** the "Last call" line uses Discord's native relative-timestamp format `<t:UNIX_TIMESTAMP:R>` which renders client-side as "5 seconds ago" / "1 minute ago" and updates automatically without the bot having to re-edit. Same format for any other time displays in the message.
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md",
  "offset": 1296,
  "limit": 450
}
```

> TOOL

tool_result Read
```
1296	## Data Model
1297	
1298	All `_at` fields are `timestamptz`. Fifteen tables: epics, checklist_items, sprints, sprint_items, messages, epic_events, codebases, code_artifacts, images, second_opinions, feedback, bot_turns, tool_calls, external_requests, system_logs.
1299	
1300	### epics
1301	```
1302	id,
1303	title (string, NOT NULL — derived from body's # heading by parser; updated atomically with body writes),
1304	goal (string, NOT NULL — derived from body's ## Goal section first paragraph by parser; updated atomically with body writes),
1305	body (markdown text, NOT NULL — canonical source of title and goal),
1306	state ('shaping'|'sprinting'|'planned'|'paused'|'archived'),
1307	created_at, last_edited_at, last_active_at, planned_at (nullable)
1308	```
1309	Indexes: `(state, last_edited_at desc)`, `(title)` for search, `(goal)` for search.
1310	
1311	**Title and goal are derived columns, not user-edited columns.** The body is the canonical source. The flow:
1312	
1313	1. The body parser identifies the `# Title` heading (single, required, line 1) and the `## Goal` section first paragraph during the same parse it does for other sections.
1314	2. Every `edit_epic` write triggers a re-parse. In the same DB transaction as the body update, the server updates `epics.title` and `epics.goal` from the parsed values.
1315	3. If a body edit results in no `# Title` or empty `## Goal` first paragraph, the write is rejected with error `body_missing_required_section` and a clear message naming the missing section. These are required structural elements, enforced at write time.
1316	4. `create_epic(title, goal, ...)` accepts title and goal as parameters. The server constructs the initial body as `# {title}\n\n## Goal\n\n{goal}\n\n... (other default sections)`, then runs the parse path to derive the columns. There is no "skip the parser" path — the parser is the only writer of `epics.title` and `epics.goal`.
1317	
1318	The bot can change title or goal *only* by editing the body (e.g., `edit_epic(body: { sections: { Goal: { replace: '...' } } })` or by editing the `# Title` heading directly via a section-replace targeting the title). The bot's hot context shows title and goal as "the parsed values from the body" — same effect either way, but the audit trail is always a body edit.
1319	
1320	**Why this design:** title and goal are display-relevant for indexed search and list rendering (avoiding markdown-parsing every list_epics call), so they need to be columns. But two sources of truth (columns AND body sections) is drift-prone. Making columns derived means there's still one source (body) and one derivation path (parser), with columns as a cache that's atomically refreshed.
1321	
1322	### checklist_items
1323	```
1324	id, epic_id, content,
1325	status ('open'|'done'|'skipped'|'superseded'),
1326	position, source ('bot_inferred'|'user_requested'|'carried_over'|'default_seed'|'second_opinion'),
1327	skip_reason (nullable), superseded_by_item_id (nullable),
1328	created_at, completed_at (nullable)
1329	```
1330	Indexes: `(epic_id, status, position)`.
1331	
1332	### sprints
1333	```
1334	id, epic_id, sprint_number,
1335	name, goal,
1336	status ('proposed'|'queued'|'pending'|'done'),
1337	queue_position (nullable int — set when status='queued'; defines execution order),
1338	pending_reason (nullable text — set when status='pending'; e.g., "waiting on legal review"),
1339	target_weeks (default 2),
1340	created_at, updated_at,
1341	queued_at (nullable)
1342	```
1343	Indexes: `(epic_id, sprint_number)`, `(epic_id, status)`, `(epic_id, queue_position) WHERE status='queued'` (unique).
1344	
1345	**Status lifecycle:**
1346	- `proposed` — being shaped; user is reviewing/adjusting
1347	- `queued` — locked in AND ready to start; `queue_position` defines execution order
1348	- `pending` — locked in AND deliberately deferred; `pending_reason` captures context when given
1349	- `done` — reserved for post-handoff; v1 doesn't drive transitions to this state
1350	
1351	At lock-in confirmation, all `proposed` sprints transition directly to `queued` or `pending` based on the user's queue/pend choices. There's no separate "finalized" intermediate state — locking in IS the queue/pend assignment.
1352	
1353	`sprint_number` is the natural ordering during shaping (1, 2, 3...). `queue_position` is the *execution* ordering — can differ from sprint_number (e.g., riskiest sprint queued first). Pending sprints have null queue_position.
1354	
1355	### sprint_items
1356	```
1357	id, sprint_id, content,
1358	estimated_complexity ('small'|'medium'|'large'),
1359	status ('open'|'in_progress'|'done'),
1360	source_section (nullable), position, created_at
1361	```
1362	Indexes: `(sprint_id, position)`.
1363	
1364	### messages
1365	```
1366	id, epic_id (nullable),
1367	direction ('inbound'|'outbound'),
1368	content, sent_at,
1369	discord_message_id (unique),
1370	has_code_attachment (boolean),
1371	has_image_attachment (boolean),
1372	in_burst_with (uuid array, nullable),
1373	was_voice_message (boolean, default false),
1374	audio_storage_url (nullable — original audio file in Supabase Storage),
1375	transcription_metadata (jsonb, nullable — Groq response: model, duration, confidence, language)
1376	```
1377	Indexes: `(epic_id, sent_at desc)`, `discord_message_id` (unique). Full-text search on `content`.
1378	
1379	For voice messages, `content` holds the transcription; the original audio is retained for audit. Hot context flags voice-origin so the bot can read transcriptions as more conversational/exploratory.
1380	
1381	### epic_events (append-only audit + state derivation source)
1382	```
1383	id, epic_id, transaction_id (uuid, groups events from one edit_epic call),
1384	event_type, summary,
1385	prior_state (jsonb, nullable — for revertible events),
1386	turn_id (nullable), occurred_at
1387	```
1388	Event types: `body_edit`, `checklist_change`, `sprints_change`, `state_change`, `forced_handoff`, `created`, `code_referenced`, `codebase_added`, `image_generated`, `second_opinion_requested`, `reverted_to`, `sprint_status_change`.
1389	
1390	`sprint_status_change` covers queueing, pending assignment, reordering, and any future status transitions; specifics in the event's jsonb details. Avoids one-event-type-per-action proliferation.
1391	
1392	`prior_state` enables revert by storing enough to reconstruct previous state per event type:
1393	- `body_edit`: prior body content
1394	- `checklist_change`: prior full checklist state (array of item snapshots)
1395	- `sprints_change`: prior full sprints state (sprint + item snapshots)
1396	- `state_change`: prior state value
1397	- Others: kind-specific prior state
1398	
1399	`transaction_id` lets `revert` undo the entire most-recent `edit_epic` call by reverting all events with the same transaction_id together.
1400	
1401	Indexes: `(epic_id, occurred_at desc)`, `(transaction_id)`.
1402	
1403	### codebases
1404	```
1405	id,
1406	owner (string, stored lowercase),
1407	name (string, stored lowercase),
1408	default_branch,
1409	scope ('global'|'epic_specific'),
1410	group_name (nullable — for workspace grouping; codebases with same group_name are siblings),
1411	associated_epic_id (nullable, FK epics.id),
1412	added_at, added_via, last_accessed_at,
1413	verified_accessible_at (nullable — last successful metadata fetch),
1414	notes
1415	```
1416	Indexes: `(scope, last_accessed_at desc)`, `(owner, name)` unique, `(group_name)`.
1417	
1418	**Case normalization:** `owner` and `name` are normalized to lowercase before insert. GitHub treats org/repo names case-insensitively (`PeterOMallet/Repo` and `peteromallet/repo` resolve to the same repo), so storing mixed case would create duplicates. The `add_codebase` tool lowercases both fields server-side; the populator script does the same. This makes `(owner, name)` unique meaningful.
1419	
1420	**GitHub metadata fetch strategy** (for `verified_accessible_at` and discovery):
1421	- Repo verification uses `GET /repos/{owner}/{name}` (the GitHub repo metadata endpoint). Returns 200 if accessible, 404 if not, 403 if rate-limited or auth-blocked.
1422	- This is preferred over `HEAD` because GitHub's HEAD support is inconsistent across endpoints, and the GET response provides additional useful data (default_branch, repo size, last push) that the populator can store in one call.
1423	- Cached in `code_artifacts` with `kind='api_cache'` and 1-hour TTL — repeated verifications within an hour use the cache.
1424	- Populator script uses `GET /orgs/{org}/repos?type=public&per_page=100` (paginated) to discover repos under an org.
1425	- All requests use `Accept: application/vnd.github+json` and `X-GitHub-Api-Version: 2022-11-28` headers; the PAT is sent as `Authorization: Bearer <PAT>`.
1426	
1427	### code_artifacts (unified: excerpts, summaries, cache)
1428	```
1429	id, codebase_id (nullable), epic_id (nullable),
1430	kind ('excerpt'|'summary'|'api_cache'),
1431	source ('conversation'|'codebase'),
1432	file_path (nullable), line_range (nullable),
1433	scope (nullable: 'file'|'directory'|'cross_codebase' for summaries),
1434	content, content_summary (nullable),
1435	metadata (jsonb), created_at, last_used_at, expires_at (nullable)
1436	```
1437	Indexes: `(epic_id, created_at desc)`, `(codebase_id, kind, file_path)`, `(expires_at)` for cache cleanup.
1438	
1439	### images
1440	```
1441	id, epic_id, source ('agent_generated'|'user_uploaded'),
1442	prompt (nullable — null for user uploads),
1443	storage_url, quality (nullable for user uploads), size,
1444	created_at,
1445	reference_key (string, unique per epic — short stable id like 'img_auth_flow' for body references),
1446	description (auto-generated for agent images, bot-fills-in for user uploads after viewing),
1447	caption (user-visible label),
1448	in_body (boolean — true if referenced via reference_key in body markdown),
1449	active (boolean, default true — older versions deactivated when reference_key is reused),
1450	discord_attachment_id (nullable — set when image came in via Discord upload)
1451	```
1452	Indexes: `(epic_id, created_at desc)`, `(epic_id, reference_key)` unique partial index where active=true, `(epic_id, source)`.
1453	
1454	**Two image sources:**
1455	- `agent_generated` — bot called `generate_image` (Sprint 6 feature). Has prompt, quality.
1456	- `user_uploaded` — user attached an image to a Discord message. Bot extracts attachment, downloads to Supabase Storage, creates row. Bot can `view_image` to see it. User uploads work from Sprint 1b onward (basic detection + storage), with the same `reference_key` body-syntax available once Sprint 2a's body parser is in place.
1457	
1458	**Images as referenceable objects:** each image has a stable `reference_key` (auto-assigned at creation, e.g. `img_auth_flow`, `img_user_upload_3`). The body can reference images using markdown image syntax with an `image:` protocol — `![auth flow](image:img_auth_flow)` — which is rendered to the actual `storage_url` at display time. This lets the body have structured pointers to images rather than floating "I made an image" text. Same syntax works for both bot-generated and user-uploaded images.
1459	
1460	Hot context includes image *descriptions* + reference keys (cheap), not the actual image bytes. The agent fetches an image visually only when needed via `view_image`. Regenerating an image with a tweak creates a new row; if the agent reuses the reference_key, the older version is set to `active=false` and the new version becomes the live one for body references. If the agent assigns a new key, both coexist.
1461	
1462	**For user uploads:** when the user attaches an image, the bot first calls `view_image` to actually look at it, then sets a `description` based on what it sees, and may suggest a `reference_key` and offer to embed it in the body. The user can override.
1463	
1464	### second_opinions
1465	```
1466	id, epic_id, requested_at,
1467	requested_by ('user'|'auto_state_gate'),
1468	focus_areas, raw_response,
1469	score (int 0-10), summary, verdict (text),
1470	resulting_checklist_item_ids (uuid array),
1471	model_used
1472	```
1473	Indexes: `(epic_id, requested_at desc)`, `(score)` for tracking improvement over time.
1474	
1475	### feedback
1476	```
1477	id,
1478	kind ('style'|'process'|'epic_specific'|'friction'|'ambiguity'|'tool_failure'|'confusion'|'pattern_noticed'),
1479	content (the words — user's, agent's distillation, or bot's self-observation),
1480	source ('user_volunteered'|'agent_proposed_user_confirmed'|'explicit_save_request'|'agent_observation'),
1481	source_message_id (nullable — links to the message that prompted it; null for agent_observation),
1482	epic_id (nullable — set for epic_specific feedback or epic-scoped observations),
1483	turn_id (nullable — set for agent_observation; identifies the turn that produced it),
1484	context_snapshot (jsonb — see schema below),
1485	active (boolean, default true — user can deactivate stale feedback),
1486	deactivation_reason (nullable),
1487	resolved (boolean, default false — only meaningful for observation kinds; user-feedback kinds ignore this),
1488	resolution_note (text, nullable),
1489	resolved_at (nullable),
1490	created_at,
1491	last_referenced_at (nullable — updated when bot reads in hot context),
1492	last_applied_at (nullable — updated when bot acts on this feedback; meaningless for observation kinds)
1493	```
1494	Indexes: `(kind, active, created_at desc)`, `(epic_id, active)`, `(active, last_referenced_at)`, `(active, last_applied_at desc)`, `(source, resolved, created_at desc)`.
1495	
1496	**One table, two semantic groups:**
1497	
1498	| Group | Kinds | Source values | Lifecycle |
1499	|---|---|---|---|
1500	| **User feedback** (preferences/reactions) | `style`, `process`, `epic_specific` | `user_volunteered`, `agent_proposed_user_confirmed`, `explicit_save_request` | active → deactivated; tracked via `last_applied_at` |
1501	| **Agent observations** (diagnostic notes) | `friction`, `ambiguity`, `tool_failure`, `confusion`, `pattern_noticed` | `agent_observation` only | open → resolved; tracked via `resolved_at` |
1502	
1503	The single table simplifies storage and audit ("show me everything written about this epic" is one query). The two groups are distinguished by `kind` AND `source`. Different verbs/tools for writing each, so the bot's mental model stays clean.
1504	
1505	**`context_snapshot` schema:**
1506	```
1507	{
1508	  user_message: string,                  // for user feedback: what they said. For observations: triggering message if any.
1509	  bot_action_being_critiqued: string,    // for user feedback: what the bot just did. For observations: what the bot was working on.
1510	}
1511	```
1512	Other context (turn_id, plan state, mode) is recoverable from the linked turn — no need to denormalize.
1513	
1514	**Kind semantics:**
1515	
1516	*User feedback kinds:*
1517	- `style` — persistent across all epics; shapes response style ("be more concise", "stop apologizing")
1518	- `process` — persistent; shapes how the bot drives planning ("always start with scope reduction", "skip second opinion until I ask")
1519	- `epic_specific` — tied to one epic; case-based memory for similar epics later
1520	
1521	*Agent observation kinds:*
1522	- `friction` — something was harder than expected ("spent 4 turns clarifying scope; should have asked sooner")
1523	- `ambiguity` — input or context was unclear, bot made a judgment call
1524	- `tool_failure` — a tool returned unexpected results or failed in an interesting way
1525	- `confusion` — bot itself was uncertain about a decision
1526	- `pattern_noticed` — something happening across multiple turns or epics
1527	
1528	**Hot-context loading:**
1529	- All active `style` and `process` feedback (every turn)
1530	- Active `epic_specific` feedback for the current epic
1531	- **Recent unresolved observations on the current epic** (last 5; lets bot self-correct across turns)
1532	- Other epics' feedback is cold; retrievable via `list_feedback`
1533	- Each entry shows: content, kind, days since created, days since last applied (or null for observations)
1534	
1535	**Saving discipline:**
1536	- *User feedback:* usually agent-proposed and user-confirmed. Exception: explicit save requests ("save this: I want shorter messages") skip confirmation.
1537	- *Agent observations:* bot-authored, no user confirmation. Bot writes when it notices something worth recording — see Self-observation in system prompt for when to record.
1538	
1539	**Stale handling:**
1540	- *User feedback:* older than 90 days without being referenced or applied → flagged in hot context as "possibly stale"; bot asks if it still applies
1541	- *Agent observations:* unresolved older than 90 days → also flagged as stale; bot can decide whether the issue is still live or should be marked resolved
1542	
1543	**`apply_feedback`** is a no-op on observation kinds (timestamp updates meaningless there). Tool returns success but doesn't change anything; bot won't have reason to call it.
1544	
1545	### bot_turns
1546	```
1547	id, epic_id (nullable), triggered_by_message_ids (uuid array),
1548	prompt_snapshot, prompt_version, reasoning,
1549	final_output_message_id (nullable),
1550	status_message_id (nullable — Discord message id of the live status message),
1551	status ('in_progress'|'completed'|'failed'|'abandoned'),
1552	state_at_turn,
1553	plan_edited (boolean), code_consulted (boolean),
1554	image_generated (boolean), second_opinion_requested (boolean),
1555	message_sent (boolean),
1556	warnings_issued (jsonb),
1557	current_activity (text, nullable — short description of what bot is doing right now, set via set_activity),
1558	started_at, completed_at (nullable), model_version
1559	```
1560	Indexes: `(status, started_at)`, `(epic_id, started_at desc)`.
1561	
1562	### tool_calls (all tool calls)
1563	```
1564	id, turn_id, tool_name,
1565	operation_kind ('read'|'write'),
1566	arguments (jsonb), result (jsonb, may be summarized for large reads),
1567	called_at, duration_ms
1568	```
1569	Indexes: `(turn_id)`, `(tool_name, called_at desc)`.
1570	
1571	### external_requests (provider call ledger)
1572	```
1573	id, idempotency_key (string, unique, NOT NULL),
1574	provider ('anthropic'|'openai'|'groq'|'github'|'discord'|'supabase_storage'),
1575	endpoint (string — e.g. 'POST /v1/messages', 'POST /chat.send', 'POST /generations'),
1576	tool_call_id (nullable FK to tool_calls — null for system-level calls like the loop's main LLM request),
1577	turn_id (nullable FK to bot_turns),
1578	request_summary (jsonb — request shape, NOT full body; used to identify duplicates),
1579	status ('pending'|'sent'|'confirmed'|'failed'|'orphaned'),
1580	provider_request_id (nullable — provider-returned id when available, e.g. Discord message_id, OpenAI request_id),
1581	provider_response_summary (jsonb — response shape on success, error details on failure),
1582	attempt_count (integer, default 1),
1583	first_attempted_at, last_attempted_at, completed_at (nullable),
1584	error_details (jsonb, nullable)
1585	```
1586	Indexes: `(idempotency_key)` unique, `(provider, status, last_attempted_at)`, `(status, last_attempted_at)` for reconciliation scan, `(turn_id)`, `(tool_call_id)`.
1587	
1588	**Purpose:** every external API call is recorded here *before* it's attempted. Treats external calls as **at-least-once delivery** — a call may execute and the recording write may fail (or vice versa), so the system needs to detect and reconcile.
1589	
1590	**Idempotency key generation:** deterministic from the call's intent. For tool-call-driven requests: `sha256(turn_id + ":" + tool_call_id + ":" + provider + ":" + endpoint + ":" + canonical_args)[:16]`. For system requests (e.g., the loop's main LLM call per turn): `sha256(turn_id + ":system:" + provider + ":" + endpoint)[:16]`. Same retry produces same key — the database's unique constraint on `idempotency_key` prevents double-recording.
1591	
1592	**Lifecycle:**
1593	1. Before issuing call: insert row with `status='pending'`, idempotency_key, request_summary
1594	2. Issue the call. If provider supports idempotency headers (Anthropic, OpenAI, Stripe-style), pass the same key
1595	3. On success response: update row to `status='confirmed'`, fill `provider_request_id`, `provider_response_summary`, `completed_at`
1596	4. On error response: update row to `status='failed'`, fill `error_details`, `completed_at`
1597	5. On crash before step 3 or 4: row remains `pending`. Recovery scan finds it.
1598	
1599	**Recovery / reconciliation:** every recovery cycle (startup + every 5 min, see Idempotency and Recovery), scan `external_requests` where `status='pending'` and `last_attempted_at > 60s ago`. For each:
1600	- *Discord post:* query Discord for messages from the bot in the user's DM channel within the request window; match against `request_summary` content. If found, mark `confirmed` with the Discord message_id; link `messages.discord_message_id`. If not found, mark `orphaned` and re-queue the original tool call.
1601	- *Anthropic / OpenAI:* idempotency-key replay. Reissue the same call with the same idempotency key. The provider returns the original response if the call was previously processed, or processes fresh if it wasn't. Either way: row becomes `confirmed` or `failed`.
1602	- *Groq transcription:* deterministic given input audio + model. Re-issue if `pending` past timeout.
1603	- *GitHub (read only in v1):* re-issue. GET requests are naturally idempotent.
1604	- *Storage uploads:* check Supabase Storage for the file by deterministic key (e.g., `images/{epic_id}/{idempotency_key}.{ext}`). If present, mark `confirmed`. If not, re-issue.
1605	
1606	**Per-provider notes:**
1607	- **Anthropic:** pass `Idempotency-Key` header. Anthropic deduplicates within 24 hours.
1608	- **OpenAI (chat + image):** pass `Idempotency-Key` header. OpenAI deduplicates within 24 hours.
1609	- **Groq:** no native idempotency header. Treat as deterministic; safe to retry. The same audio + model + transcription params produce equivalent output.
1610	- **GitHub (REST API):** no native idempotency header for GETs (don't need one). v1 is read-only against GitHub, so any retry is safe.
1611	- **Discord (gateway send_message):** no idempotency header. Use the post-hoc reconciliation pattern above (query Discord for recent bot messages, match by content/timing).
1612	- **Supabase Storage:** use deterministic file paths (`{idempotency_key}.{ext}`) so retries overwrite the same object instead of creating duplicates.
1613	
1614	**Bot's exposure to this:** the bot doesn't see `external_requests` in its hot context or tools. The ledger is invisible at the agent layer. From the bot's perspective: it calls `send_message`, the loop guarantees the message is sent at least once with no user-visible duplicates. The ledger is purely an infrastructure concern, owned by the loop.
1615	
1616	**Effect on `tool_calls` atomicity:** the tool_call row is still written in the same DB transaction as the underlying mutation (or in the case of pure external calls, just the tool_call). The external_requests row is written separately, *before* the external call fires. If the bot crashes after writing tool_calls but before completing the external call, recovery finds the orphaned external_requests row and reconciles. Crash *after* external call but *before* tool_calls write: external_requests row reflects success; recovery doesn't double-fire (it sees `confirmed`); the tool_call row is missing but can be reconstructed from the external_requests row if needed (rare, manual operator pass).
1617	
1618	**Invariant:** for every `tool_calls` row that involved an external call, there is at least one `external_requests` row with the same `tool_call_id`. The reverse isn't true — system-level external calls (like the main LLM request) have `tool_call_id=null`.
1619	
1620	### system_logs (unified application + system log sink)
1621	```
1622	id, level ('debug'|'info'|'warn'|'error'),
1623	category ('system'|'application'|'tool'|'llm'|'external_api'|'recovery'),
1624	event_type (string — free-form identifier, e.g. 'startup', 'tool_call_failed', 'opus_request', 'github_404'),
1625	message (human-readable),
1626	details (jsonb — arbitrary structured context),
1627	turn_id (nullable — links log to bot turn when applicable),
1628	epic_id (nullable),
1629	occurred_at
1630	```
1631	Indexes: `(level, occurred_at desc)`, `(category, event_type, occurred_at desc)`, `(turn_id)`, `(epic_id, occurred_at desc)`.
1632	
1633	**Purpose:** every log line goes here — application debug, system events, tool call diagnostics, LLM request/response metadata, external API errors, recovery actions, cap warnings. The audit tables (`tool_calls`, `bot_turns`, `epic_events`) capture *what happened*; `system_logs` captures *how it happened* and any diagnostic context.
1634	
1635	**Retention:** debug logs purged after 7 days; info after 30 days; warn/error retained indefinitely (single-user scale; revisit if storage grows). Daily cleanup job.
1636	
1637	**Logger module:** all code uses a single `log(level, category, event_type, message, **context)` interface that writes to this table. No `print` statements, no stdout logging for production code. Tests can use stdout for visibility.
1638	
1639	---
1640	
1641	## Tools
1642	
1643	Every action is a tool call. All tool calls log to `tool_calls`.
1644	
1645	The write surface is minimal because the bot edits epics like a structured document. Whole-state changes at the field level rather than fine-grained operations. The system records diffs and audit.
1646	
1647	**Mode applicability.** Most tools work identically in both modes. A few are mode-specific or mode-divergent — these are flagged inline in their definitions and summarized here so the engineer doesn't have to hunt:
1648	
1649	- **Both modes (no behavioral change):** `list_epics`, `get_epic`, `get_section_names`, `get_body_outline`, `search_in_body`, `get_checklist`, `get_sprints`, `search_epics`, `recent_messages`, `search_messages`, `get_history`, `get_epic_at_time`, `get_recent_turns`, `search_tool_calls`, `get_self_understanding`, `list_images`, `view_image`, `update_image_metadata`, `edit_epic`, `create_epic`, `revert`, `render_epic`, `add_codebase`, `remove_codebase`, `list_codebases`, `get_codebase_tree`, `read_codebase_file`, `search_code`, `analyze_code`, `save_code_excerpt`, `mark_code_in_body`, `save_feedback`, `apply_feedback`, `deactivate_feedback`, `list_feedback`, `record_observation`, `list_observations`, `mark_observation_resolved`, `request_second_opinion`, `generate_image`.
1650	- **Resident-mode only (no-op or error in invocation mode):** `set_typing` (Discord typing indicator has no analog in invocation mode; tool succeeds silently and emits a no-op event for audit symmetry).
1651	- **Mode-divergent (same name, different effect):**
1652	  - `send_message(content, attach_files?)` — resident: posts to Discord, returns the discord_message_id. Invocation: appends `content` to the turn's reply buffer, returns a synthetic id; the buffer becomes the envelope's `reply` field. If called multiple times within one turn, contents are concatenated with blank lines (rare; the bot's normal flow is one terminal `send_message`).
1653	  - `send_image(image_id, caption?)` — resident: posts the image to Discord. Invocation: adds an `attached_image` event to the envelope's `events` array (with `image_id`, `caption`, `storage_url`); the caller is responsible for displaying or persisting it.
1654	  - `set_activity(description)` — resident: updates `bot_turns.current_activity`, drives the live status-message "Currently:" line. Invocation: emits an `activity` progress event with the description; otherwise no side effect.
1655	- **Invocation-mode only (does not exist in resident mode):**
1656	  - `defer_to_caller(questions, reason?)` — see Communication subsection. Sets envelope `outcome="blocked_on_caller"` and populates `questions`. Calling this in resident mode is an error (logged, turn continues — the bot should phrase questions to the human user via `send_message` instead).
1657	
1658	### Communication
1659	- `send_message(content, attach_files?)` — Discord message; the only way the bot ends a turn for substantive work *(in resident mode)*. *(Mode-divergent: see Mode applicability above. In invocation mode, appends to the turn's reply buffer instead of posting to Discord.)* **Logging:** the message is written to the `messages` table with `direction='outbound'`, `discord_message_id` set after the Discord API confirms the post (resident) or set to a synthetic `inv_<turn_id>_<n>` id (invocation), and `bot_turn_id` linking back to the originating turn. Outbound messages are first-class entries in the conversation history (visible to `recent_messages` and `search_messages`).
1660	- `set_typing(on/off)` — typing indicator; auto-managed *(resident-only; no-op in invocation mode)*
1661	- `set_activity(description)` — sets the "Currently:" line in the live status message (see Status Message); short string (≤80 chars); useful when current activity isn't obvious from recent tool calls *(mode-divergent: in invocation mode, emits an `activity` event instead of editing a Discord message)*
1662	- `defer_to_caller(questions: list[str], reason?: string)` *(invocation-mode only)* — bot calls this when it has unresolved ambiguity that requires caller decision rather than continuing on its own judgment. Sets envelope `outcome="blocked_on_caller"`, populates the envelope's `questions` array with the supplied list (caller-facing, machine-readable), and ends the turn cleanly. The bot should also call `send_message` first with a natural-language version of the questions so the `reply` field is non-empty. **When to call:** the bot has done what it can, but a decision the caller is better positioned to make (e.g., "should this epic include mobile or just web?", "use OAuth or API keys?") would change the next concrete edits. Not for everyday conversational questions back to a human user — those go through `send_message`. **Resident-mode behavior:** calling `defer_to_caller` in resident mode is an error: it logs to `system_logs` at warn level and is treated as a no-op (the turn continues; the bot should send the question via `send_message` instead). The tool's signature exists in resident mode for symmetry but its body raises.
1663	
1664	**Status messages are NOT logged to `messages`.** The status message is an ephemeral UI affordance maintained by the loop — it lives only in `bot_turns.status_message_id` (the Discord message id, so the loop can edit it) and is never queried as conversation. Including it in `messages` would pollute history retrieval (`recent_messages`, `search_messages`) with internal scaffolding. The status message's *content* (count, activity, last 3 tools) is reconstructable from the audit (`tool_calls`, `bot_turns.current_activity`) if anyone needs to investigate.
1665	
1666	### Read — epics
1667	- `list_epics(state?, sort_by?)`
1668	- `get_epic(epic_id, sections?)` — full epic, or just specified sections (returns content + list of all section names so bot knows the doc shape)
1669	- `get_section_names(epic_id)` — just the ordered list of body section names; cheap query for when bot needs to know the structure
1670	- `get_body_outline(epic_id)` — returns section names + sub-headings (`###` and below) + line counts per section; cheap; lets bot reason about doc shape and size before reading content
1671	- `search_in_body(epic_id, query, context_lines=2)` — full-text search within an epic's body; returns matches with line numbers, the matching line, and N lines of surrounding context per hit. Bot uses line numbers for reasoning about location, not for line-level edits (those don't exist by design — edits stay at section granularity)
1672	- `get_checklist(epic_id, status?)`
1673	- `get_sprints(epic_id)`
1674	- `search_epics(query)` — finds which epics match; combine with `search_in_body` per match for precise location
1675	- `recent_messages(epic_id, n)`
1676	- `search_messages(query, epic_id?, date_range?)` — full-text
1677	- `get_history(epic_id, kind?, since?)` — unified audit query
1678	- `get_epic_at_time(epic_id, timestamp)` — replays `epic_events` to reconstruct epic state (body, checklist, sprints) as it was at that moment. Read-only. Returns the same shape as `get_epic` plus a `reconstructed_at` timestamp. Bot uses this when user asks "what did this look like Tuesday?" or "before I made that change." Precision: returns state as of the most recent event with `occurred_at <= timestamp`. Tied timestamps ordered by `(occurred_at, id)` ascending. If no events exist before timestamp, returns the epic's initial state.
1679	- `get_recent_turns(n=10, epic_id?)` — last N turns with summaries (triggered messages, what was edited via `change_summary`, status). Pulled from `bot_turns`. Filter by epic_id or get cross-epic recent activity.
1680	- `search_tool_calls(query?, tool_name?, epic_id?, since?, limit=20)` — search the `tool_calls` audit table. Filter by tool name (e.g., `analyze_code`), epic, time window, or text query against tool arguments. Lets the bot answer "what code investigation have I done on this epic?" / "have I read auth.py before?" / "what `edit_epic` calls happened last week?" Used for both bot self-awareness and for answering user questions about prior activity.
1681	- `get_self_understanding(epic_id)` — bot's structured summary
1682	
1683	### Read — images
1684	- `list_images(epic_id, source?)` — returns reference_keys, descriptions, captions, source (no image bytes); filter by source if needed
1685	- `view_image(image_id, mode='visual'|'description')` — fetches image bytes when bot needs to actually see it; description-only mode returns just metadata. The bot uses `mode='visual'` for both bot-generated images (less common, since it has the description from creation) and user-uploaded images (essential for understanding what the user sent).
1686	
1687	### Write — images
1688	- `send_image(image_id, caption?)` — posts an existing image to Discord. Used when bot wants to re-show an image the user has seen before, or surface a generated image in a follow-up turn. Different from `generate_image` (which creates AND sends). Different from body-reference syntax (which embeds in rendered body, not in chat).
1689	- `update_image_metadata(image_id, caption?, description?, reference_key?)` — edit metadata without creating a new image. Useful for user uploads where bot fills in description after viewing, or when caption needs correction.
1690	
1691	### Read — code
1692	- `list_codebases(scope?, group?, epic_id?)`
1693	- `get_codebase_tree(codebase_id, path?)`
1694	- `read_codebase_file(codebase_id, file_path, line_range?)`
1695	- `search_code(codebase_id, query, type?)`
1696	- `analyze_code(codebase_ids, scope, question)` — accepts list for cross-codebase
1697	
1698	### Read — feedback
1699	- `list_feedback(kind?, priority?, active_only=true, epic_id?)` — retrieves saved feedback with `last_applied_at`; `epic_id` filters to feedback tied to a specific epic; `priority` filters to `always`/`situational`/`background` (use `priority='situational'` to retrieve items not in hot context)
1700	
1701	### Write — epics (unified, document-like editing)
1702	
1703	**`edit_epic(epic_id, changes, change_summary, expected_diff?)`** — the single tool for editing an existing epic. Returns `transaction_id` for the events created, plus the body diff. If `expected_diff` is supplied, server computes actual diff and refuses to commit if they don't match (returning the actual diff so bot can retry or accept). If `expected_diff` is omitted, server commits unconditionally. The `changes` object can include any combination of:
1704	
1705	```
1706	{
1707	  meta?: { title?, goal? },
1708	  body?: {
1709	    // Mutually exclusive — pick ONE approach per call:
1710	    new_content?: string,                              // whole-body replace
1711	    sections?: { [section_name]: new_content },       // section replace (preferred for small changes)
1712	    append?: { [section_name]: content },             // append to a section (additive ops)
1713	    remove_sections?: [section_name],                 // remove named sections
1714	    rename_section?: { from, to },                    // rename a section
1715	    reorder?: [section_name, ...],                    // new ordering
1716	    position?: 'after:SectionName' | 'before:SectionName' | 'end' | 'start',  // for new sections being added via `sections`
1717	  },
1718	  checklist?: {
1719	    add?: [{ content, position?, source }],
1720	    update?: [{ id, content?, position?, status?, skip_reason?, superseded_by? }],
1721	    remove?: [id]
1722	  },
1723	  sprints?: {
1724	    sprints: [{ id?, sprint_number, name, goal, status, queue_position?, pending_reason?, items: [...] }]
1725	  },
1726	  state?: { target, force? }
1727	}
1728	```
1729	
1730	**Section-level body editing** is the preferred path for most edits. The bot specifies which section it's changing rather than rewriting the whole body. Under the hood, the system reads the current `epics.body` cell, applies the section operation, writes the cell back — atomic. Storage stays a single markdown text column; the structure is parsed at edit time and stitched back on write.
1731	
1732	Body content can reference images using `![caption](image:reference_key)` syntax — rendered to actual storage URLs at display time via `render_epic`.
1733	
1734	**Diff verification via `expected_diff`:** when the bot wants strong assurance its intent matches the actual change, it supplies `expected_diff` in the call. Server computes the actual diff before committing; if they disagree, server refuses and returns the actual diff. Bot can retry with corrected changes or accept the actual diff and re-call without `expected_diff`. This is preflight verification (the write doesn't happen on mismatch), not post-hoc abort. When omitted, server writes unconditionally — most cases, since the bot's intent and the changes object are explicit.
1735	
1736	Single transaction; either all changes apply or none do. Logs one event per affected field family, all sharing the transaction_id. The `change_summary` is human-readable for the audit log.
1737	
1738	State advances are part of `edit_epic` because they often go with other changes. Gating logic runs server-side using the conditions enumerated in "State Advance Gating": if conditions aren't met and `force` is false, the call fails with a list of blockers and the bot surfaces them to the user.
1739	
1740	**`create_epic(title, goal, template?, initial_checklist?)`** — new epic creation; separate because there's no `epic_id` yet. `template` defaults based on goal phrasing (see Body Templates).
1741	
1742	**`revert(epic_id, event_id?)`** — undoes most recent transaction (no event_id) or restores to a specific event.
1743	
1744	**`render_epic(epic_id, format='markdown'|'html')`** — produces a display-ready version of the epic. Resolves `image:reference_key` references to actual storage URLs. Used when user says "show me the epic" or for export. The raw `epics.body` cell stays untouched.
1745
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/supabase/migrations/202604300001_001_core.sql"
}
```

> TOOL

tool_result Read
```
1	CREATE TABLE IF NOT EXISTS epics (
2	    id TEXT PRIMARY KEY,
3	    title TEXT NOT NULL,
4	    goal TEXT NOT NULL,
5	    body TEXT NOT NULL,
6	    state TEXT NOT NULL CHECK (state IN ('shaping', 'sprinting', 'planned', 'paused', 'archived')),
7	    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
8	    last_edited_at TIMESTAMPTZ NOT NULL DEFAULT now(),
9	    last_active_at TIMESTAMPTZ,
10	    planned_at TIMESTAMPTZ
11	);
12	
13	CREATE INDEX IF NOT EXISTS idx_epics_state_last_edited_at
14	    ON epics (state, last_edited_at DESC);
15	CREATE INDEX IF NOT EXISTS idx_epics_title
16	    ON epics (title);
17	CREATE INDEX IF NOT EXISTS idx_epics_goal
18	    ON epics (goal);
19	
20	CREATE TABLE IF NOT EXISTS bot_turns (
21	    id TEXT PRIMARY KEY,
22	    epic_id TEXT REFERENCES epics(id) ON DELETE SET NULL,
23	    triggered_by_message_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
24	    prompt_snapshot JSONB,
25	    prompt_version TEXT,
26	    reasoning TEXT,
27	    final_output_message_id TEXT,
28	    status_message_id TEXT,
29	    status TEXT NOT NULL CHECK (status IN ('in_progress', 'completed', 'failed', 'abandoned')),
30	    state_at_turn JSONB,
31	    plan_edited BOOLEAN NOT NULL DEFAULT false,
32	    code_consulted BOOLEAN NOT NULL DEFAULT false,
33	    image_generated BOOLEAN NOT NULL DEFAULT false,
34	    second_opinion_requested BOOLEAN NOT NULL DEFAULT false,
35	    message_sent BOOLEAN NOT NULL DEFAULT false,
36	    warnings_issued JSONB,
37	    current_activity TEXT,
38	    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
39	    completed_at TIMESTAMPTZ,
40	    model_version TEXT
41	);
42	
43	CREATE INDEX IF NOT EXISTS idx_bot_turns_status_started_at
44	    ON bot_turns (status, started_at);
45	CREATE INDEX IF NOT EXISTS idx_bot_turns_epic_started_at
46	    ON bot_turns (epic_id, started_at DESC);
47	
48	CREATE TABLE IF NOT EXISTS messages (
49	    id TEXT PRIMARY KEY,
50	    epic_id TEXT REFERENCES epics(id) ON DELETE SET NULL,
51	    direction TEXT NOT NULL CHECK (direction IN ('inbound', 'outbound')),
52	    content TEXT NOT NULL,
53	    sent_at TIMESTAMPTZ NOT NULL DEFAULT now(),
54	    discord_message_id TEXT UNIQUE,
55	    has_code_attachment BOOLEAN NOT NULL DEFAULT false,
56	    has_image_attachment BOOLEAN NOT NULL DEFAULT false,
57	    in_burst_with JSONB,
58	    was_voice_message BOOLEAN NOT NULL DEFAULT false,
59	    audio_storage_url TEXT,
60	    transcription_metadata JSONB,
61	    bot_turn_id TEXT REFERENCES bot_turns(id) ON DELETE SET NULL
62	);
63	
64	CREATE INDEX IF NOT EXISTS idx_messages_epic_sent_at
65	    ON messages (epic_id, sent_at);
66	
67	CREATE TABLE IF NOT EXISTS tool_calls (
68	    id TEXT PRIMARY KEY,
69	    turn_id TEXT NOT NULL REFERENCES bot_turns(id) ON DELETE CASCADE,
70	    tool_name TEXT NOT NULL,
71	    operation_kind TEXT NOT NULL CHECK (operation_kind IN ('read', 'write')),
72	    arguments JSONB NOT NULL DEFAULT '{}'::jsonb,
73	    result JSONB NOT NULL DEFAULT '{}'::jsonb,
74	    called_at TIMESTAMPTZ NOT NULL DEFAULT now(),
75	    duration_ms INTEGER NOT NULL DEFAULT 0
76	);
77	
78	CREATE INDEX IF NOT EXISTS idx_tool_calls_turn_id
79	    ON tool_calls (turn_id);
80	CREATE INDEX IF NOT EXISTS idx_tool_calls_tool_name_called_at
81	    ON tool_calls (tool_name, called_at DESC);
82	
83	CREATE TABLE IF NOT EXISTS system_logs (
84	    id TEXT PRIMARY KEY,
85	    level TEXT NOT NULL CHECK (level IN ('debug', 'info', 'warn', 'error')),
86	    category TEXT NOT NULL CHECK (category IN ('system', 'application', 'tool', 'llm', 'external_api', 'recovery')),
87	    event_type TEXT NOT NULL,
88	    message TEXT NOT NULL,
89	    details JSONB NOT NULL DEFAULT '{}'::jsonb,
90	    turn_id TEXT REFERENCES bot_turns(id) ON DELETE SET NULL,
91	    epic_id TEXT REFERENCES epics(id) ON DELETE SET NULL,
92	    occurred_at TIMESTAMPTZ NOT NULL DEFAULT now()
93	);
94	
95	CREATE INDEX IF NOT EXISTS idx_system_logs_level_occurred_at
96	    ON system_logs (level, occurred_at DESC);
97	CREATE INDEX IF NOT EXISTS idx_system_logs_category_event_occurred_at
98	    ON system_logs (category, event_type, occurred_at DESC);
99	CREATE INDEX IF NOT EXISTS idx_system_logs_turn_id
100	    ON system_logs (turn_id);
101	CREATE INDEX IF NOT EXISTS idx_system_logs_epic_occurred_at
102	    ON system_logs (epic_id, occurred_at DESC);
103	
104	CREATE TABLE IF NOT EXISTS epic_locks (
105	    epic_id TEXT PRIMARY KEY REFERENCES epics(id) ON DELETE CASCADE,
106	    holder_id TEXT NOT NULL,
107	    acquired_at TIMESTAMPTZ NOT NULL DEFAULT now(),
108	    expires_at TIMESTAMPTZ NOT NULL
109	);
110	
111	CREATE TABLE IF NOT EXISTS external_requests (
112	    id TEXT PRIMARY KEY,
113	    idempotency_key TEXT NOT NULL UNIQUE,
114	    provider TEXT NOT NULL CHECK (provider IN ('anthropic', 'openai', 'groq', 'github', 'discord', 'supabase_storage')),
115	    endpoint TEXT NOT NULL,
116	    tool_call_id TEXT REFERENCES tool_calls(id) ON DELETE SET NULL,
117	    turn_id TEXT REFERENCES bot_turns(id) ON DELETE SET NULL,
118	    request_summary JSONB NOT NULL DEFAULT '{}'::jsonb,
119	    status TEXT NOT NULL CHECK (status IN ('pending', 'sent', 'confirmed', 'failed', 'orphaned')),
120	    provider_request_id TEXT,
121	    provider_response_summary JSONB,
122	    attempt_count INTEGER NOT NULL DEFAULT 1,
123	    first_attempted_at TIMESTAMPTZ NOT NULL DEFAULT now(),
124	    last_attempted_at TIMESTAMPTZ NOT NULL DEFAULT now(),
125	    completed_at TIMESTAMPTZ,
126	    error_details JSONB
127	);
128	
129	CREATE UNIQUE INDEX IF NOT EXISTS idx_external_requests_idempotency_key
130	    ON external_requests (idempotency_key);
131	CREATE INDEX IF NOT EXISTS idx_external_requests_provider_status_last_attempted
132	    ON external_requests (provider, status, last_attempted_at);
133	CREATE INDEX IF NOT EXISTS idx_external_requests_status_last_attempted
134	    ON external_requests (status, last_attempted_at);
135	CREATE INDEX IF NOT EXISTS idx_external_requests_turn_id
136	    ON external_requests (turn_id);
137	CREATE INDEX IF NOT EXISTS idx_external_requests_tool_call_id
138	    ON external_requests (tool_call_id);
139
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/supabase/migrations/202604300003_003_external_requests_body.sql"
}
```

> TOOL

tool_result Read
```
1	ALTER TABLE external_requests
2	    ADD COLUMN IF NOT EXISTS request_body JSONB;
3
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/agent_kit/__init__.py"
}
```

> TOOL

tool_result Read
```
<system-reminder>Warning: the file exists but is shorter than the provided offset (1). The file has 1 lines.</system-reminder>
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/agent_kit/store/supabase.py"
}
```

> TOOL

tool_result Read
```
1	"""Supabase/Postgres Store adapter for resident mode."""
2	
3	from __future__ import annotations
4	
5	from contextlib import contextmanager
6	from datetime import UTC, datetime
7	import os
8	from typing import Any, Iterator, Sequence
9	from uuid import uuid4
10	JSONDict = dict[str, Any]
11	
12	_JSON_COLUMNS = {"arguments", "details", "error_details", "in_burst_with", "prompt_snapshot", "provider_response_summary", "request_body", "request_summary", "result", "state_at_turn", "transcription_metadata", "triggered_by_message_ids", "warnings_issued"}
13	
14	
15	class SupabaseStore:
16	    def __init__(self, dsn: str | None = None, *, connection: Any = None) -> None:
17	        if connection is None:
18	            dsn = dsn or os.environ["SUPABASE_DB_URL"]
19	            self._conn = _connect(dsn)
20	            self._owns_connection = True
21	        else:
22	            self._conn = connection
23	            self._owns_connection = False
24	        self._transaction_depth = 0
25	
26	    @classmethod
27	    def from_env(cls) -> "SupabaseStore":
28	        return cls(os.environ["SUPABASE_DB_URL"])
29	
30	    def close(self) -> None:
31	        if self._owns_connection:
32	            self._conn.close()
33	
34	    @contextmanager
35	    def transaction(self) -> Iterator[None]:
36	        self._transaction_depth += 1
37	        try:
38	            with self._conn.transaction():
39	                yield
40	        finally:
41	            self._transaction_depth -= 1
42	
43	    def create_message(
44	        self,
45	        *,
46	        epic_id: str | None,
47	        direction: str,
48	        content: str,
49	        discord_message_id: str | None = None,
50	        bot_turn_id: str | None = None,
51	        has_code_attachment: bool = False,
52	        has_image_attachment: bool = False,
53	        in_burst_with: Sequence[str] | None = None,
54	        was_voice_message: bool = False,
55	        audio_storage_url: str | None = None,
56	        transcription_metadata: JSONDict | None = None,
57	        synthesize_outbound_id: bool = True,
58	    ) -> JSONDict:
59	        message_id = _new_id("msg")
60	        if (
61	            synthesize_outbound_id
62	            and direction == "outbound"
63	            and discord_message_id is None
64	            and bot_turn_id
65	        ):
66	            discord_message_id = self._next_invocation_message_id(bot_turn_id)
67	        self._conn.execute(
68	            "INSERT INTO messages (id, epic_id, direction, content, discord_message_id, has_code_attachment, has_image_attachment, in_burst_with, was_voice_message, audio_storage_url, transcription_metadata, bot_turn_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
69	            (
70	                message_id,
71	                epic_id,
72	                direction,
73	                content,
74	                discord_message_id,
75	                has_code_attachment,
76	                has_image_attachment,
77	                _json(list(in_burst_with)) if in_burst_with else None,
78	                was_voice_message,
79	                audio_storage_url,
80	                _json(transcription_metadata) if transcription_metadata else None,
81	                bot_turn_id,
82	            ),
83	        )
84	        return self.load_message(message_id) or {}
85	
86	    def load_message(self, message_id: str) -> JSONDict | None:
87	        return _normalize(self._conn.execute("SELECT * FROM messages WHERE id = %s", (message_id,)).fetchone())
88	
89	    def load_messages(self, message_ids: Sequence[str]) -> list[JSONDict]:
90	        if not message_ids:
91	            return []
92	        rows = self._conn.execute(
93	            "SELECT * FROM messages WHERE id = ANY(%s)",
94	            (list(message_ids),),
95	        ).fetchall()
96	        by_id = {row["id"]: _normalize(row) for row in rows}
97	        return [by_id[item] for item in message_ids if item in by_id]
98	
99	    def update_message(self, message_id: str, **changes: Any) -> JSONDict:
100	        return self._update("messages", "id", message_id, changes, _MESSAGE_COLUMNS, self.load_message)
101	
102	    def create_turn(
103	        self,
104	        *,
105	        epic_id: str,
106	        triggered_by_message_ids: Sequence[str],
107	        prompt_snapshot: JSONDict | None = None,
108	        prompt_version: str | None = None,
109	        state_at_turn: JSONDict | None = None,
110	        model_version: str | None = None,
111	    ) -> JSONDict:
112	        turn_id = _new_id("turn")
113	        self._conn.execute(
114	            "INSERT INTO bot_turns (id, epic_id, triggered_by_message_ids, prompt_snapshot, prompt_version, status, state_at_turn, model_version) VALUES (%s, %s, %s, %s, %s, 'in_progress', %s, %s)",
115	            (
116	                turn_id,
117	                epic_id,
118	                _json(list(triggered_by_message_ids)),
119	                _json(prompt_snapshot) if prompt_snapshot is not None else None,
120	                prompt_version,
121	                _json(state_at_turn) if state_at_turn is not None else None,
122	                model_version,
123	            ),
124	        )
125	        return self._load_turn(turn_id) or {}
126	
127	    def update_turn(self, turn_id: str, **changes: Any) -> JSONDict:
128	        if changes.get("status") in {"completed", "failed", "abandoned"} and "completed_at" not in changes:
129	            changes = {**changes, "completed_at": datetime.now(UTC)}
130	        return self._update("bot_turns", "id", turn_id, changes, _TURN_COLUMNS, self._load_turn)
131	
132	    def find_abandoned_turns(self, older_than_seconds: int) -> list[JSONDict]:
133	        return _normalize_rows(
134	            self._conn.execute(
135	                "SELECT * FROM bot_turns WHERE status = 'in_progress' AND started_at <= now() - (%s * interval '1 second') ORDER BY started_at",
136	                (older_than_seconds,),
137	            ).fetchall()
138	        )
139	
140	    def record_tool_call(
141	        self,
142	        *,
143	        turn_id: str,
144	        tool_name: str,
145	        operation_kind: str,
146	        arguments: JSONDict,
147	        result: JSONDict,
148	        duration_ms: int,
149	    ) -> JSONDict:
150	        tool_call_id = _new_id("tool")
151	        self._conn.execute(
152	            "INSERT INTO tool_calls (id, turn_id, tool_name, operation_kind, arguments, result, duration_ms) VALUES (%s, %s, %s, %s, %s, %s, %s)",
153	            (tool_call_id, turn_id, tool_name, operation_kind, _json(arguments), _json(result), duration_ms),
154	        )
155	        return self._load_tool_call(tool_call_id) or {}
156	
157	    def log_system_event(
158	        self,
159	        *,
160	        level: str,
161	        category: str,
162	        event_type: str,
163	        message: str,
164	        details: JSONDict | None = None,
165	        turn_id: str | None = None,
166	        epic_id: str | None = None,
167	    ) -> JSONDict:
168	        log_id = _new_id("log")
169	        self._conn.execute(
170	            "INSERT INTO system_logs (id, level, category, event_type, message, details, turn_id, epic_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
171	            (log_id, level, category, event_type, message, _json(details or {}), turn_id, epic_id),
172	        )
173	        return self._load_system_log(log_id) or {}
174	
175	    def acquire_epic_lock(self, epic_id: str, *, holder_id: str, timeout_seconds: int = 60) -> bool:
176	        row = self._conn.execute(
177	            "INSERT INTO epic_locks (epic_id, holder_id, acquired_at, expires_at) VALUES (%s, %s, now(), now() + (%s * interval '1 second')) ON CONFLICT (epic_id) DO UPDATE SET holder_id = EXCLUDED.holder_id, acquired_at = now(), expires_at = EXCLUDED.expires_at WHERE epic_locks.expires_at <= now() OR epic_locks.holder_id = EXCLUDED.holder_id RETURNING holder_id",
178	            (epic_id, holder_id, timeout_seconds),
179	        ).fetchone()
180	        return bool(row and row["holder_id"] == holder_id)
181	
182	    def release_epic_lock(self, epic_id: str, *, holder_id: str) -> None:
183	        self._conn.execute(
184	            "DELETE FROM epic_locks WHERE epic_id = %s AND holder_id = %s",
185	            (epic_id, holder_id),
186	        )
187	
188	    def load_hot_context(self, epic_id: str) -> JSONDict:
189	        epic = _normalize(self._conn.execute("SELECT * FROM epics WHERE id = %s", (epic_id,)).fetchone())
190	        messages = _normalize_rows(
191	            self._conn.execute(
192	                "SELECT * FROM messages WHERE epic_id = %s ORDER BY sent_at DESC LIMIT 10",
193	                (epic_id,),
194	            ).fetchall()
195	        )
196	        tool_calls = _normalize_rows(
197	            self._conn.execute(
198	                "SELECT tool_calls.* FROM tool_calls JOIN bot_turns ON bot_turns.id = tool_calls.turn_id WHERE bot_turns.epic_id = %s ORDER BY tool_calls.called_at DESC LIMIT 10",
199	                (epic_id,),
200	            ).fetchall()
201	        )
202	        return {"epic": epic, "recent_messages": list(reversed(messages)), "recent_tool_calls": list(reversed(tool_calls))}
203	
204	    def find_unprocessed_messages(self, epic_id: str, started_at: str, exclude_ids: Sequence[str]) -> list[JSONDict]:
205	        return _normalize_rows(
206	            self._conn.execute(
207	                "SELECT * FROM messages WHERE epic_id = %s AND direction = 'inbound' AND sent_at >= %s AND NOT (id = ANY(%s)) ORDER BY sent_at, id",
208	                (epic_id, started_at, list(exclude_ids)),
209	            ).fetchall()
210	        )
211	
212	    def insert_pending(
213	        self,
214	        *,
215	        idempotency_key: str,
216	        provider: str,
217	        endpoint: str,
218	        request_summary: JSONDict,
219	        request_body: JSONDict | None = None,
220	        turn_id: str | None = None,
221	        tool_call_id: str | None = None,
222	    ) -> JSONDict:
223	        request_id = _new_id("ext")
224	        self._conn.execute(
225	            "INSERT INTO external_requests (id, idempotency_key, provider, endpoint, tool_call_id, turn_id, request_summary, request_body, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pending')",
226	            (request_id, idempotency_key, provider, endpoint, tool_call_id, turn_id, _json(request_summary), _json(request_body) if request_body is not None else None),
227	        )
228	        return self._load_external_request(request_id) or {}
229	
230	    def find_pending_external_requests(self, older_than_seconds: int) -> list[JSONDict]:
231	        return _normalize_rows(
232	            self._conn.execute(
233	                "SELECT * FROM external_requests WHERE status IN ('pending', 'sent') AND last_attempted_at <= now() - (%s * interval '1 second') ORDER BY last_attempted_at, id",
234	                (older_than_seconds,),
235	            ).fetchall()
236	        )
237	
238	    def mark_confirmed(self, request_id: str, *, provider_request_id: str | None = None, provider_response_summary: JSONDict | None = None) -> JSONDict:
239	        return self._mark_request(request_id, "confirmed", provider_request_id, provider_response_summary, None)
240	
241	    def mark_failed(self, request_id: str, *, error_details: JSONDict) -> JSONDict:
242	        return self._mark_request(request_id, "failed", None, None, error_details)
243	
244	    def mark_orphaned(self, request_id: str, *, error_details: JSONDict) -> JSONDict:
245	        return self._mark_request(request_id, "orphaned", None, None, error_details)
246	
247	    def create_image(
248	        self,
249	        *,
250	        epic_id: str,
251	        source: str,
252	        storage_url: str,
253	        prompt: str | None = None,
254	        quality: str | None = None,
255	        size: str | None = None,
256	        reference_key: str | None = None,
257	        description: str | None = None,
258	        caption: str | None = None,
259	        in_body: bool = False,
260	        active: bool = True,
261	        discord_attachment_id: str | None = None,
262	    ) -> JSONDict:
263	        image_id = _new_id("img")
264	        reference_key = reference_key or self._next_image_reference_key(epic_id, source)
265	        self._conn.execute(
266	            "INSERT INTO images (id, epic_id, source, prompt, storage_url, quality, size, reference_key, description, caption, in_body, active, discord_attachment_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
267	            (image_id, epic_id, source, prompt, storage_url, quality, size, reference_key, description, caption, in_body, active, discord_attachment_id),
268	        )
269	        return self.load_image(image_id) or {}
270	
271	    def load_image(self, image_id: str) -> JSONDict | None:
272	        return _normalize(self._conn.execute("SELECT * FROM images WHERE id = %s", (image_id,)).fetchone())
273	
274	    def list_images(self, *, epic_id: str, source: str | None = None, active: bool | None = True) -> list[JSONDict]:
275	        clauses = ["epic_id = %s"]
276	        params: list[Any] = [epic_id]
277	        if source is not None:
278	            clauses.append("source = %s")
279	            params.append(source)
280	        if active is not None:
281	            clauses.append("active = %s")
282	            params.append(active)
283	        return _normalize_rows(
284	            self._conn.execute(
285	                f"SELECT * FROM images WHERE {' AND '.join(clauses)} ORDER BY created_at DESC, id DESC",
286	                params,
287	            ).fetchall()
288	        )
289	
290	    def update_image(self, image_id: str, **changes: Any) -> JSONDict:
291	        return self._update("images", "id", image_id, changes, _IMAGE_COLUMNS, self.load_image)
292	
293	    def _mark_request(
294	        self,
295	        request_id: str,
296	        status: str,
297	        provider_request_id: str | None,
298	        provider_response_summary: JSONDict | None,
299	        error_details: JSONDict | None,
300	    ) -> JSONDict:
301	        self._conn.execute(
302	            "UPDATE external_requests SET status = %s, provider_request_id = %s, provider_response_summary = %s, completed_at = now(), error_details = %s WHERE id = %s",
303	            (status, provider_request_id, _json(provider_response_summary) if provider_response_summary is not None else None, _json(error_details) if error_details is not None else None, request_id),
304	        )
305	        return self._load_external_request(request_id) or {}
306	
307	    def _update(self, table: str, key_column: str, row_id: str, changes: dict[str, Any], allowed: set[str], loader) -> JSONDict:
308	        if not changes:
309	            return loader(row_id) or {}
310	        unknown = set(changes) - allowed
311	        if unknown:
312	            raise ValueError(f"unsupported {table} columns: {', '.join(sorted(unknown))}")
313	        assignments = ", ".join(f"{key} = %s" for key in changes)
314	        values = [_to_sql_value(key, value) for key, value in changes.items()]
315	        self._conn.execute(
316	            f"UPDATE {table} SET {assignments} WHERE {key_column} = %s",
317	            [*values, row_id],
318	        )
319	        return loader(row_id) or {}
320	
321	    def _next_invocation_message_id(self, turn_id: str) -> str:
322	        row = self._conn.execute(
323	            "SELECT COUNT(*) AS count FROM messages WHERE bot_turn_id = %s AND direction = 'outbound'",
324	            (turn_id,),
325	        ).fetchone()
326	        return f"inv_{turn_id}_{int(row['count']) + 1}"
327	
328	    def _next_image_reference_key(self, epic_id: str, source: str) -> str:
329	        prefix = "img_user_upload" if source == "user_uploaded" else "img_agent"
330	        rows = self._conn.execute(
331	            "SELECT reference_key FROM images WHERE epic_id = %s AND reference_key LIKE %s AND active = true",
332	            (epic_id, f"{prefix}_%"),
333	        ).fetchall()
334	        used = {row["reference_key"] for row in rows}
335	        index = 1
336	        while f"{prefix}_{index}" in used:
337	            index += 1
338	        return f"{prefix}_{index}"
339	
340	    def _load_turn(self, turn_id: str) -> JSONDict | None:
341	        return _normalize(self._conn.execute("SELECT * FROM bot_turns WHERE id = %s", (turn_id,)).fetchone())
342	
343	    def _load_tool_call(self, tool_call_id: str) -> JSONDict | None:
344	        return _normalize(self._conn.execute("SELECT * FROM tool_calls WHERE id = %s", (tool_call_id,)).fetchone())
345	
346	    def _load_system_log(self, log_id: str) -> JSONDict | None:
347	        return _normalize(self._conn.execute("SELECT * FROM system_logs WHERE id = %s", (log_id,)).fetchone())
348	
349	    def _load_external_request(self, request_id: str) -> JSONDict | None:
350	        return _normalize(self._conn.execute("SELECT * FROM external_requests WHERE id = %s", (request_id,)).fetchone())
351	
352	
353	_MESSAGE_COLUMNS = {"discord_message_id", "content", "audio_storage_url", "transcription_metadata", "has_image_attachment", "has_code_attachment", "in_burst_with", "was_voice_message", "bot_turn_id"}
354	_TURN_COLUMNS = {"triggered_by_message_ids", "prompt_snapshot", "prompt_version", "reasoning", "final_output_message_id", "status_message_id", "status", "state_at_turn", "plan_edited", "code_consulted", "image_generated", "second_opinion_requested", "message_sent", "warnings_issued", "current_activity", "completed_at", "model_version"}
355	_IMAGE_COLUMNS = {"prompt", "storage_url", "quality", "size", "reference_key", "description", "caption", "in_body", "active", "discord_attachment_id"}
356	
357	
358	def _connect(dsn: str) -> Any:
359	    try:
360	        import psycopg
361	        from psycopg.rows import dict_row
362	    except ImportError as exc:
363	        raise RuntimeError("psycopg is required for SupabaseStore") from exc
364	    conn = psycopg.connect(dsn, row_factory=dict_row)
365	    conn.autocommit = True
366	    return conn
367	
368	
369	def _json(value: Any) -> Any:
370	    from psycopg.types.json import Jsonb
371	
372	    return Jsonb(value)
373	
374	
375	def _to_sql_value(key: str, value: Any) -> Any:
376	    if key in _JSON_COLUMNS and value is not None:
377	        return _json(value)
378	    return value
379	
380	
381	def _normalize(row: Any) -> JSONDict | None:
382	    if row is None:
383	        return None
384	    normalized = dict(row)
385	    for key, value in list(normalized.items()):
386	        if isinstance(value, datetime):
387	            normalized[key] = value.isoformat().replace("+00:00", "Z")
388	    return normalized
389	
390	
391	def _normalize_rows(rows: Sequence[Any]) -> list[JSONDict]:
392	    return [item for item in (_normalize(row) for row in rows) if item is not None]
393	
394	
395	def _new_id(prefix: str) -> str:
396	    return f"{prefix}_{uuid4().hex}"
397	
398	
399	__all__ = ["SupabaseStore"]
400
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/agent_kit/tool_kit.py",
  "offset": 1,
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	"""Tool registry and audited invocation wrapper."""
2	
3	from __future__ import annotations
4	
5	from dataclasses import dataclass, field
6	from datetime import UTC, datetime
7	from time import perf_counter
8	from typing import Any, Callable, Literal
9	
10	from agent_kit.envelope import Event
11	from agent_kit.ledger import Ledger
12	from agent_kit.ports import Blob, PushTransport, Store
13	
14	
15	EventKind = Literal["tool_call", "activity"]
16	OperationKind = Literal["read", "write"]
17	JSONDict = dict[str, Any]
18	ToolCallable = Callable[..., Any]
19	ExternalCallable = Callable[[], tuple[str | None, JSONDict | None]]
20	
21	
22	@dataclass(frozen=True)
23	class ExternalSpec:
24	    provider: str
25	    endpoint: str
26	    request_summary: JSONDict
27	    request_body: JSONDict | None = None
28	
29	
30	@dataclass(frozen=True)
31	class ToolEntry:
32	    name: str
33	    func: ToolCallable
34	    schema: JSONDict
35	    event_kind: EventKind = "tool_call"
36	    operation_kind: OperationKind = "write"
37	
38	
39	@dataclass
40	class ToolContext:
41	    store: Store
42	    turn_id: str
43	    events: list[Event]
44	    on_event: Callable[[Event], None] | None = None
45	    reply_buffer: list[str] = field(default_factory=list)
46	    metadata: JSONDict = field(default_factory=dict)
47	    transport: PushTransport | None = None
48	    blob: Blob | None = None
49	    external_queue: list[tuple[ExternalSpec, ExternalCallable]] | None = None
50	
51	
52	@dataclass(frozen=True)
53	class ToolInvocation:
54	    result: JSONDict
55	    tool_call: JSONDict
56	    event: Event
57	
58	
59	class ToolRegistry:
60	    def __init__(self) -> None:
61	        self._entries: dict[str, ToolEntry] = {}
62	
63	    def register(
64	        self,
65	        name: str,
66	        func: ToolCallable,
67	        schema: JSONDict,
68	        *,
69	        event_kind: EventKind = "tool_call",
70	        operation_kind: OperationKind = "write",
71	    ) -> ToolEntry:
72	        entry = ToolEntry(
73	            name=name,
74	            func=func,
75	            schema=schema,
76	            event_kind=event_kind,
77	            operation_kind=operation_kind,
78	        )
79	        self._entries[name] = entry
80	        return entry
81	
82	    def tool(
83	        self,
84	        name: str | None = None,
85	        *,
86	        schema: JSONDict | None = None,
87	        event_kind: EventKind = "tool_call",
88	        operation_kind: OperationKind = "write",
89	    ) -> Callable[[ToolCallable], ToolCallable]:
90	        def decorator(func: ToolCallable) -> ToolCallable:
91	            self.register(
92	                name or func.__name__,
93	                func,
94	                schema or {},
95	                event_kind=event_kind,
96	                operation_kind=operation_kind,
97	            )
98	            return func
99	
100	        return decorator
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/agent_kit/tools/communication.py",
  "offset": 1,
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	"""Minimal invocation-mode communication tools."""
2	
3	from __future__ import annotations
4	
5	from typing import Any
6	
7	from agent_kit.logging import log
8	from agent_kit.tool_kit import ExternalSpec, ToolContext, register_tool
9	
10	
11	SEND_MESSAGE_SCHEMA = {
12	    "type": "object",
13	    "additionalProperties": False,
14	    "required": ["content"],
15	    "properties": {
16	        "content": {"type": "string"},
17	        "attach_files": {
18	            "type": ["array", "null"],
19	            "items": {"type": "string"},
20	        },
21	    },
22	}
23	
24	SET_ACTIVITY_SCHEMA = {
25	    "type": "object",
26	    "additionalProperties": False,
27	    "required": ["description"],
28	    "properties": {
29	        "description": {"type": "string"},
30	    },
31	}
32	
33	DEFER_TO_CALLER_SCHEMA = {
34	    "type": "object",
35	    "additionalProperties": False,
36	    "required": ["questions"],
37	    "properties": {
38	        "questions": {
39	            "type": "array",
40	            "items": {"type": "string"},
41	        },
42	        "reason": {"type": ["string", "null"]},
43	    },
44	}
45	
46	
47	@register_tool(
48	    "send_message",
49	    schema=SEND_MESSAGE_SCHEMA,
50	    event_kind="tool_call",
51	    operation_kind="write",
52	)
53	def send_message(
54	    context: ToolContext,
55	    content: str,
56	    attach_files: list[str] | None = None,
57	) -> str:
58	    del attach_files
59	    context.reply_buffer.append(content)
60	    is_resident = context.transport is not None
61	    # Resident sends must wait for Discord confirmation before filling the external id.
62	    message = context.store.create_message(
63	        epic_id=context.metadata.get("epic_id"),
64	        direction="outbound",
65	        content=content,
66	        bot_turn_id=context.turn_id,
67	        synthesize_outbound_id=not is_resident,
68	    )
69	    if not is_resident:
70	        return message["discord_message_id"]
71	
72	    channel_id = str(context.metadata.get("channel_id") or "")
73	    endpoint = f"POST /channels/{channel_id}/messages"
74	
75	    def _post_and_update():
76	        response = context.transport.post_message(channel_id, content)  # type: ignore[union-attr]
77	        discord_message_id = (
78	            response.get("discord_message_id")
79	            or response.get("id")
80	            or response.get("message_id")
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/agent_kit/loop.py",
  "offset": 1,
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	"""Transport-agnostic turn loop entry points."""
2	
3	from __future__ import annotations
4	
5	import asyncio
6	import json
7	from threading import Event as ThreadingEvent
8	from typing import Callable, Sequence
9	from uuid import uuid4
10	
11	from agent_kit.envelope import Envelope, EnvelopeError, Event, StateDelta
12	from agent_kit.ledger import Ledger
13	from agent_kit.logging import log
14	from agent_kit.ports import Blob, JSONDict, Model, ProviderError, PushTransport, Store
15	from agent_kit.tool_kit import ToolContext, registry
16	import agent_kit.tools.communication  # noqa: F401
17	import agent_kit.tools.images  # noqa: F401
18	
19	
20	ANTHROPIC_MESSAGES_ENDPOINT = "POST /v1/messages"
21	ANTHROPIC_MAX_TOKENS = 4096
22	DEFAULT_PROMPT_VERSION = "sprint1a"
23	
24	
25	def run_turn(
26	    *,
27	    epic_id: str,
28	    input: str,
29	    store: Store,
30	    model: Model,
31	    model_id: str = "claude-opus-4-7",
32	    on_event=None,
33	    cancel_event: ThreadingEvent | None = None,
34	    triggered_by_message_ids: Sequence[str] | None = None,
35	    recovered_input_messages: Sequence[JSONDict] | None = None,
36	    on_turn_start: Callable[[JSONDict], None] | None = None,
37	    mid_turn_message_check: Callable[[JSONDict], list[JSONDict] | None] | None = None,
38	    transport: PushTransport | None = None,
39	    blob: Blob | None = None,
40	    channel_id: str | None = None,
41	) -> Envelope:
42	    holder_id = f"turn_holder_{uuid4().hex}"
43	    if not store.acquire_epic_lock(epic_id, holder_id=holder_id, timeout_seconds=60):
44	        log(
45	            store,
46	            "warn",
47	            "system",
48	            "epic_lock_contended",
49	            "Epic is already locked by another turn.",
50	            epic_id=epic_id,
51	        )
52	        return Envelope(
53	            turn_id=f"turn_lock_{uuid4().hex}",
54	            epic_id=epic_id,
55	            epic_state_before="unknown",
56	            epic_state_after="unknown",
57	            reply="",
58	            state_delta=StateDelta(),
59	            outcome="errored",
60	            error=EnvelopeError(
61	                code="epic_locked",
62	                message="Epic is already locked by another turn.",
63	                retryable=True,
64	            ),
65	        )
66	
67	    turn = None
68	    events: list[Event] = []
69	    reply_buffer: list[str] = []
70	    context: ToolContext | None = None
71	    state_before = "unknown"
72	    try:
73	        if recovered_input_messages is not None:
74	            initial_user_prompt = _messages_prompt(recovered_input_messages)
75	        else:
76	            initial_user_prompt = input
77	
78	        if triggered_by_message_ids is None:
79	            inbound = store.create_message(
80	                epic_id=epic_id,
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/agent_kit/loop.py",
  "offset": 80,
  "limit": 230
}
```

> TOOL

tool_result Read
```
80	                epic_id=epic_id,
81	                direction="inbound",
82	                content=input,
83	                discord_message_id=f"inv_in_{uuid4().hex}",
84	            )
85	            turn_message_ids = [inbound["id"]]
86	        else:
87	            turn_message_ids = list(triggered_by_message_ids)
88	
89	        hot_context = store.load_hot_context(epic_id)
90	        epic = hot_context.get("epic") or {}
91	        state_before = epic.get("state", "unknown")
92	        turn = store.create_turn(
93	            epic_id=epic_id,
94	            triggered_by_message_ids=turn_message_ids,
95	            prompt_snapshot={
96	                "input": initial_user_prompt,
97	                "hot_context": _summarize_hot_context(hot_context),
98	            },
99	            prompt_version=DEFAULT_PROMPT_VERSION,
100	            state_at_turn={"epic_state": state_before},
101	            model_version=model_id,
102	        )
103	        if on_turn_start is not None:
104	            on_turn_start(turn)
105	        ledger = Ledger(store)
106	        context = ToolContext(
107	            store=store,
108	            turn_id=turn["id"],
109	            events=events,
110	            on_event=on_event,
111	            reply_buffer=reply_buffer,
112	            metadata={
113	                "epic_id": epic_id,
114	                "outcome": "completed",
115	                "questions": [],
116	                "channel_id": channel_id,
117	            },
118	            transport=transport,
119	            blob=blob,
120	        )
121	
122	        if _is_cancelled(cancel_event):
123	            return _abort_turn(store, turn, epic_id, state_before, events, reply_buffer)
124	
125	        model_call_seq = 0
126	        messages = [{"role": "user", "content": initial_user_prompt}]
127	        while True:
128	            model_call_seq += 1
129	            tool_definitions = list(registry.definitions())
130	            request_body = {
131	                "model": model_id,
132	                "messages": list(messages),
133	                "tools": tool_definitions,
134	                "max_tokens": ANTHROPIC_MAX_TOKENS,
135	            }
136	            request_summary = {
137	                "model": model_id,
138	                "message_count": len(messages),
139	                "tool_names": [definition["name"] for definition in tool_definitions],
140	                "input_length": len(input),
141	                "system_seq": model_call_seq,
142	            }
143	            request_id, [REDACTED](
144	                provider="anthropic",
145	                endpoint=ANTHROPIC_MESSAGES_ENDPOINT,
146	                request_summary=request_summary,
147	                request_body=request_body,
148	                turn_id=turn["id"],
149	                system_seq=model_call_seq,
150	            )
151	            try:
152	                result = model.complete_turn(
153	                    model_id=model_id,
154	                    messages=messages,
155	                    tools=tool_definitions,
156	                    hot_context=hot_context,
157	                    idempotency_key=idempotency_key,
158	                )
159	            except ProviderError as exc:
160	                ledger.mark_failed(request_id, exc.error_details)
161	                log(
162	                    store,
163	                    "error",
164	                    "llm",
165	                    "provider_error",
166	                    "Model provider returned an error.",
167	                    turn_id=turn["id"],
168	                    epic_id=epic_id,
169	                    error_details=exc.error_details,
170	                    provider_request_id=exc.provider_request_id,
171	                )
172	                store.update_turn(turn["id"], status="failed", reasoning=str(exc.error_details))
173	                return _envelope(
174	                    turn_id=turn["id"],
175	                    epic_id=epic_id,
176	                    state_before=state_before,
177	                    state_after=state_before,
178	                    reply_buffer=reply_buffer,
179	                    events=events,
180	                    outcome="errored",
181	                    error=EnvelopeError(
182	                        code="provider_error",
183	                        message="Model provider returned an error.",
184	                        retryable=True,
185	                    ),
186	                )
187	            except Exception as exc:
188	                log(
189	                    store,
190	                    "error",
191	                    "llm",
192	                    "transport_error",
193	                    "Model transport or SDK call failed.",
194	                    turn_id=turn["id"],
195	                    epic_id=epic_id,
196	                    error_type=type(exc).__name__,
197	                )
198	                store.update_turn(turn["id"], status="failed", reasoning=str(exc))
199	                return _envelope(
200	                    turn_id=turn["id"],
201	                    epic_id=epic_id,
202	                    state_before=state_before,
203	                    state_after=state_before,
204	                    reply_buffer=reply_buffer,
205	                    events=events,
206	                    outcome="errored",
207	                    error=EnvelopeError(
208	                        code="model_error",
209	                        message=str(exc),
210	                        retryable=True,
211	                    ),
212	                )
213	
214	            ledger.mark_confirmed(
215	                request_id,
216	                result.provider_request_id,
217	                result.response_summary,
218	            )
219	            store.update_turn(
220	                turn["id"],
221	                prompt_snapshot=request_summary,
222	                reasoning=result.reasoning,
223	                model_version=model_id,
224	            )
225	
226	            if _is_cancelled(cancel_event):
227	                return _abort_turn(store, turn, epic_id, state_before, events, reply_buffer)
228	
229	            if result.tool_requests:
230	                reenter_model_loop = False
231	                for tool_request in result.tool_requests:
232	                    if _is_cancelled(cancel_event):
233	                        return _abort_turn(
234	                            store,
235	                            turn,
236	                            epic_id,
237	                            state_before,
238	                            events,
239	                            reply_buffer,
240	                        )
241	                    updated_turn = None
242	                    if tool_request.name == "send_message":
243	                        # Resident mode gives late inbound messages one more model pass before posting.
244	                        updated_turn = _append_mid_turn_messages(
245	                            store=store,
246	                            turn=turn,
247	                            messages=messages,
248	                            mid_turn_message_check=mid_turn_message_check,
249	                        )
250	                    if updated_turn is not None:
251	                        turn = updated_turn
252	                        reenter_model_loop = True
253	                        break
254	                    try:
255	                        invocation = registry.invoke(
256	                            tool_request.name,
257	                            context,
258	                            tool_request.arguments,
259	                        )
260	                    except Exception as exc:
261	                        log(
262	                            store,
263	                            "error",
264	                            "tool",
265	                            "tool_call_failed",
266	                            "Tool invocation failed.",
267	                            turn_id=turn["id"],
268	                            epic_id=epic_id,
269	                            tool_name=tool_request.name,
270	                            error_type=type(exc).__name__,
271	                        )
272	                        store.update_turn(turn["id"], status="failed", reasoning=str(exc))
273	                        return _envelope(
274	                            turn_id=turn["id"],
275	                            epic_id=epic_id,
276	                            state_before=state_before,
277	                            state_after=state_before,
278	                            reply_buffer=reply_buffer,
279	                            events=events,
280	                            outcome="errored",
281	                            error=EnvelopeError(
282	                                code="tool_error",
283	                                message=str(exc),
284	                                retryable=False,
285	                            ),
286	                        )
287	                    messages.append(
288	                        {
289	                            "role": "user",
290	                            "content": _tool_result_content(
291	                                tool_request.name,
292	                                invocation.result,
293	                            ),
294	                        }
295	                    )
296	                    if context.metadata.get("stop_requested"):
297	                        questions = list(context.metadata.get("questions", []))
298	                        store.update_turn(turn["id"], status="completed")
299	                        return _envelope(
300	                            turn_id=turn["id"],
301	                            epic_id=epic_id,
302	                            state_before=state_before,
303	                            state_after=state_before,
304	                            reply_buffer=reply_buffer,
305	                            events=events,
306	                            outcome="blocked_on_caller",
307	                            questions=questions,
308	                        )
309	                if reenter_model_loop:
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"epic\" /Users/user_c042661f/Documents/arnold-v2/agent_kit/store/sqlite.py | head -20",
  "description": "Check epic in sqlite"
}
```

> TOOL

tool_result Bash
```
107:        epic_id: str | None,
131:                id, epic_id, direction, content, discord_message_id,
140:                epic_id,
200:        epic_id: str,
211:                id, epic_id, triggered_by_message_ids, prompt_snapshot,
218:                epic_id,
307:        epic_id: str | None = None,
314:                epic_id
326:                epic_id,
332:    def acquire_epic_lock(
334:        epic_id: str,
345:                "DELETE FROM epic_locks WHERE epic_id = ? AND expires_at <= ?",
346:                (epic_id, now),
351:                    INSERT INTO epic_locks (
352:                        epic_id, holder_id, acquired_at, expires_at
356:                    (epic_id, holder_id, now, expires_at),
361:                    SELECT holder_id FROM epic_locks
362:                    WHERE epic_id = ? AND holder_id = ?
364:                    (epic_id, holder_id),
370:                    UPDATE epic_locks
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/agent_kit/store/sqlite.py",
  "offset": 1,
  "limit": 100
}
```

> TOOL

tool_result Read
```
1	"""SQLite Store adapter for invocation-mode Arnold runs."""
2	
3	from __future__ import annotations
4	
5	from contextlib import contextmanager
6	from datetime import UTC, datetime, timedelta
7	import json
8	from pathlib import Path
9	import sqlite3
10	from typing import Any, Iterator, Sequence
11	from uuid import uuid4
12	
13	
14	JSONDict = dict[str, Any]
15	_MIGRATIONS_DIR = Path(__file__).parent / "migrations" / "sqlite"
16	
17	_JSON_COLUMNS = {
18	    "arguments",
19	    "details",
20	    "error_details",
21	    "in_burst_with",
22	    "prompt_snapshot",
23	    "provider_response_summary",
24	    "request_body",
25	    "request_summary",
26	    "result",
27	    "state_at_turn",
28	    "transcription_metadata",
29	    "triggered_by_message_ids",
30	    "warnings_issued",
31	}
32	
33	
34	class SQLiteStore:
35	    def __init__(self, database: str | Path | sqlite3.Connection):
36	        if isinstance(database, sqlite3.Connection):
37	            self._conn = database
38	            self._owns_connection = False
39	        else:
40	            self._conn = sqlite3.connect(str(database))
41	            self._owns_connection = True
42	        self._conn.row_factory = sqlite3.Row
43	        self._conn.execute("PRAGMA foreign_keys = ON")
44	        self._transaction_depth = 0
45	        self.apply_migrations()
46	
47	    def close(self) -> None:
48	        if self._owns_connection:
49	            self._conn.close()
50	
51	    def apply_migrations(self) -> None:
52	        self._conn.execute(
53	            """
54	            CREATE TABLE IF NOT EXISTS schema_migrations (
55	                name TEXT PRIMARY KEY,
56	                applied_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
57	            )
58	            """
59	        )
60	        for migration in sorted(_MIGRATIONS_DIR.glob("*.sql")):
61	            already_applied = self._conn.execute(
62	                "SELECT 1 FROM schema_migrations WHERE name = ?",
63	                (migration.name,),
64	            ).fetchone()
65	            if already_applied:
66	                continue
67	            self._conn.executescript(migration.read_text())
68	            self._conn.execute(
69	                "INSERT INTO schema_migrations (name) VALUES (?)",
70	                (migration.name,),
71	            )
72	        self._conn.commit()
73	
74	    @contextmanager
75	    def transaction(self) -> Iterator[None]:
76	        if self._transaction_depth == 0:
77	            self._conn.execute("BEGIN")
78	            self._transaction_depth += 1
79	            try:
80	                yield
81	            except Exception:
82	                self._conn.rollback()
83	                raise
84	            else:
85	                self._conn.commit()
86	            finally:
87	                self._transaction_depth -= 1
88	            return
89	
90	        savepoint = f"sp_{self._transaction_depth}"
91	        self._conn.execute(f"SAVEPOINT {savepoint}")
92	        self._transaction_depth += 1
93	        try:
94	            yield
95	        except Exception:
96	            self._conn.execute(f"ROLLBACK TO {savepoint}")
97	            self._conn.execute(f"RELEASE {savepoint}")
98	            raise
99	        else:
100	            self._conn.execute(f"RELEASE {savepoint}")
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/arnold-v2/agent_kit/store/migrations",
  "description": "List sqlite migrations"
}
```

> TOOL

tool_result Bash
```
sqlite
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/arnold-v2/agent_kit/store/migrations/sqlite",
  "description": "List sqlite migration files"
}
```

> TOOL

tool_result Bash
```
001_core.sql
002_images.sql
003_external_requests_body.sql
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"epics\\|create_epic\\|epic_id\" /Users/user_c042661f/Documents/arnold-v2/agent_kit/ports.py | head -30",
  "description": "Check Store port"
}
```

> TOOL

tool_result Bash
```
29:    epic_id: str
69:        epic_id: str | None,
96:        epic_id: str,
132:        epic_id: str | None = None,
138:        epic_id: str,
145:    def release_epic_lock(self, epic_id: str, *, holder_id: str) -> None:
148:    def load_hot_context(self, epic_id: str) -> JSONDict:
153:        epic_id: str,
209:        epic_id: str,
230:        epic_id: str,
263:    def put(self, epic_id: str, content: bytes, mime_type: str) -> BlobRef:
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/agent_kit/ports.py"
}
```

> TOOL

tool_result Read
```
1	"""Protocol boundaries for the Arnold agent substrate."""
2	
3	from __future__ import annotations
4	
5	from contextlib import AbstractContextManager
6	from dataclasses import dataclass, field
7	from typing import Any, Callable, Protocol, Sequence
8	
9	
10	JSONDict = dict[str, Any]
11	
12	
13	@dataclass(frozen=True)
14	class ProviderError(Exception):
15	    """A parseable provider error response.
16	
17	    Model adapters raise this when the provider returns a structured error
18	    response. Transport failures, SDK bugs, and other non-provider exceptions
19	    are intentionally propagated unchanged so the loop can leave the external
20	    request ledger row pending for later reconciliation.
21	    """
22	
23	    error_details: JSONDict
24	    provider_request_id: str | None = None
25	
26	
27	@dataclass(frozen=True)
28	class BlobRef:
29	    epic_id: str
30	    key: str
31	    mime_type: str
32	    size_bytes: int | None = None
33	
34	
35	@dataclass(frozen=True)
36	class ToolRequest:
37	    name: str
38	    arguments: JSONDict
39	
40	
41	@dataclass(frozen=True)
42	class ModelTurnResult:
43	    final_text: str | None = None
44	    tool_requests: list[ToolRequest] = field(default_factory=list)
45	    reasoning: str | None = None
46	    provider_request_id: str | None = None
47	    response_summary: JSONDict | None = None
48	
49	
50	class Transport(Protocol):
51	    """Transport adapter boundary for resident and invocation modes."""
52	
53	    def receive(self) -> JSONDict:
54	        ...
55	
56	    def send(self, payload: JSONDict) -> None:
57	        ...
58	
59	    def stream_event(self, event: JSONDict) -> None:
60	        ...
61	
62	
63	class Store(Protocol):
64	    """Persistent store boundary used by the loop, tools, and logger."""
65	
66	    def create_message(
67	        self,
68	        *,
69	        epic_id: str | None,
70	        direction: str,
71	        content: str,
72	        discord_message_id: str | None = None,
73	        bot_turn_id: str | None = None,
74	        has_code_attachment: bool = False,
75	        has_image_attachment: bool = False,
76	        in_burst_with: Sequence[str] | None = None,
77	        was_voice_message: bool = False,
78	        audio_storage_url: str | None = None,
79	        transcription_metadata: JSONDict | None = None,
80	        synthesize_outbound_id: bool = True,
81	    ) -> JSONDict:
82	        ...
83	
84	    def load_message(self, message_id: str) -> JSONDict | None:
85	        ...
86	
87	    def load_messages(self, message_ids: Sequence[str]) -> list[JSONDict]:
88	        ...
89	
90	    def update_message(self, message_id: str, **changes: Any) -> JSONDict:
91	        ...
92	
93	    def create_turn(
94	        self,
95	        *,
96	        epic_id: str,
97	        triggered_by_message_ids: Sequence[str],
98	        prompt_snapshot: JSONDict | None = None,
99	        prompt_version: str | None = None,
100	        state_at_turn: JSONDict | None = None,
101	        model_version: str | None = None,
102	    ) -> JSONDict:
103	        ...
104	
105	    def update_turn(self, turn_id: str, **changes: Any) -> JSONDict:
106	        ...
107	
108	    def find_abandoned_turns(self, older_than_seconds: int) -> list[JSONDict]:
109	        ...
110	
111	    def record_tool_call(
112	        self,
113	        *,
114	        turn_id: str,
115	        tool_name: str,
116	        operation_kind: str,
117	        arguments: JSONDict,
118	        result: JSONDict,
119	        duration_ms: int,
120	    ) -> JSONDict:
121	        ...
122	
123	    def log_system_event(
124	        self,
125	        *,
126	        level: str,
127	        category: str,
128	        event_type: str,
129	        message: str,
130	        details: JSONDict | None = None,
131	        turn_id: str | None = None,
132	        epic_id: str | None = None,
133	    ) -> JSONDict:
134	        ...
135	
136	    def acquire_epic_lock(
137	        self,
138	        epic_id: str,
139	        *,
140	        holder_id: str,
141	        timeout_seconds: int = 60,
142	    ) -> bool:
143	        ...
144	
145	    def release_epic_lock(self, epic_id: str, *, holder_id: str) -> None:
146	        ...
147	
148	    def load_hot_context(self, epic_id: str) -> JSONDict:
149	        ...
150	
151	    def find_unprocessed_messages(
152	        self,
153	        epic_id: str,
154	        started_at: str,
155	        exclude_ids: Sequence[str],
156	    ) -> list[JSONDict]:
157	        ...
158	
159	    def transaction(self) -> AbstractContextManager[None]:
160	        ...
161	
162	    def insert_pending(
163	        self,
164	        *,
165	        idempotency_key: str,
166	        provider: str,
167	        endpoint: str,
168	        request_summary: JSONDict,
169	        request_body: JSONDict | None = None,
170	        turn_id: str | None = None,
171	        tool_call_id: str | None = None,
172	    ) -> JSONDict:
173	        ...
174	
175	    def mark_confirmed(
176	        self,
177	        request_id: str,
178	        *,
179	        provider_request_id: str | None = None,
180	        provider_response_summary: JSONDict | None = None,
181	    ) -> JSONDict:
182	        ...
183	
184	    def mark_failed(
185	        self,
186	        request_id: str,
187	        *,
188	        error_details: JSONDict,
189	    ) -> JSONDict:
190	        ...
191	
192	    def find_pending_external_requests(
193	        self,
194	        older_than_seconds: int,
195	    ) -> list[JSONDict]:
196	        ...
197	
198	    def mark_orphaned(
199	        self,
200	        request_id: str,
201	        *,
202	        error_details: JSONDict,
203	    ) -> JSONDict:
204	        ...
205	
206	    def create_image(
207	        self,
208	        *,
209	        epic_id: str,
210	        source: str,
211	        storage_url: str,
212	        prompt: str | None = None,
213	        quality: str | None = None,
214	        size: str | None = None,
215	        reference_key: str | None = None,
216	        description: str | None = None,
217	        caption: str | None = None,
218	        in_body: bool = False,
219	        active: bool = True,
220	        discord_attachment_id: str | None = None,
221	    ) -> JSONDict:
222	        ...
223	
224	    def load_image(self, image_id: str) -> JSONDict | None:
225	        ...
226	
227	    def list_images(
228	        self,
229	        *,
230	        epic_id: str,
231	        source: str | None = None,
232	        active: bool | None = True,
233	    ) -> list[JSONDict]:
234	        ...
235	
236	    def update_image(self, image_id: str, **changes: Any) -> JSONDict:
237	        ...
238	
239	
240	class Model(Protocol):
241	    """Model adapter boundary.
242	
243	    ``model_id`` is supplied by the caller or CLI. Adapters should raise
244	    ``ProviderError`` for structured provider errors and propagate transport
245	    or SDK exceptions unchanged.
246	    """
247	
248	    def complete_turn(
249	        self,
250	        *,
251	        model_id: str,
252	        messages: Sequence[JSONDict],
253	        tools: Sequence[JSONDict],
254	        hot_context: JSONDict,
255	        idempotency_key: str | None = None,
256	    ) -> ModelTurnResult:
257	        ...
258	
259	
260	class Blob(Protocol):
261	    """Blob storage port only; Sprint 1a intentionally ships no implementation."""
262	
263	    def put(self, epic_id: str, content: bytes, mime_type: str) -> BlobRef:
264	        ...
265	
266	    def get(self, ref: BlobRef) -> bytes:
267	        ...
268	
269	    def exists(self, ref: BlobRef) -> bool:
270	        ...
271	
272	
273	class PushTransport(Protocol):
274	    """Push transport boundary for resident mode; pull Transport stays separate."""
275	
276	    def start(self, handler: Callable[[JSONDict], Any]) -> None:
277	        ...
278	
279	    def stop(self) -> None:
280	        ...
281	
282	    def post_message(
283	        self,
284	        channel_id: str,
285	        content: str,
286	        *,
287	        files: Sequence[JSONDict] | None = None,
288	    ) -> JSONDict:
289	        ...
290	
291	    def edit_message(
292	        self,
293	        channel_id: str,
294	        message_id: str,
295	        content: str,
296	    ) -> JSONDict:
297	        ...
298	
299	    def download_attachment(self, url: str) -> bytes:
300	        ...
301	
302	    def fetch_recent_messages(
303	        self,
304	        channel_id: str,
305	        since: str,
306	        until: str,
307	    ) -> list[JSONDict]:
308	        ...
309
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/tests/test_supabase_store.py",
  "offset": 1,
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	import os
4	
5	import pytest
6	
7	
8	psycopg = pytest.importorskip("psycopg")
9	
10	if not os.environ.get("SUPABASE_TEST_DB_URL"):
11	    pytest.skip("SUPABASE_TEST_DB_URL is not set", allow_module_level=True)
12	
13	from agent_kit.store.supabase import SupabaseStore  # noqa: E402
14	from tests.store_contract import run_store_contract  # noqa: E402
15	from tests.store_contract_v1b import run_store_contract_v1b  # noqa: E402
16	
17	
18	def _store_factory():
19	    store = SupabaseStore(os.environ["SUPABASE_TEST_DB_URL"])
20	    conn = psycopg.connect(os.environ["SUPABASE_TEST_DB_URL"])
21	    _truncate(conn)
22	    return store, conn
23	
24	
25	def test_supabase_store_contracts() -> None:
26	    run_store_contract(_store_factory)
27	    run_store_contract_v1b(_store_factory)
28	
29	
30	def _truncate(conn) -> None:
31	    with conn:
32	        conn.execute(
33	            """
34	            TRUNCATE TABLE
35	              external_requests,
36	              tool_calls,
37	              messages,
38	              bot_turns,
39	              system_logs,
40	              epic_locks,
41	              images,
42	              epics
43	            RESTART IDENTITY CASCADE
44	            """
45	        )
46
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/tests/store_contract.py",
  "offset": 1,
  "limit": 60
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	from typing import Callable
4	
5	
6	def run_store_contract(store_factory: Callable):
7	    store, conn = store_factory()
8	    conn.execute(
9	        """
10	        INSERT INTO epics (id, title, goal, body, state)
11	        VALUES ('epic_1', 'Title', 'Goal', '# Title', 'shaping')
12	        """
13	    )
14	    conn.commit()
15	
16	    inbound = store.create_message(
17	        epic_id="epic_1",
18	        direction="inbound",
19	        content="hello",
20	        discord_message_id="discord_1",
21	        has_code_attachment=True,
22	    )
23	    assert store.load_message(inbound["id"])["content"] == "hello"
24	    assert store.load_hot_context("epic_1")["epic"]["title"] == "Title"
25	
26	    turn = store.create_turn(
27	        epic_id="epic_1",
28	        triggered_by_message_ids=[inbound["id"]],
29	        prompt_snapshot={"input": "hello"},
30	        state_at_turn={"state": "shaping"},
31	        model_version="fake",
32	    )
33	    updated = store.update_turn(turn["id"], status="completed", reasoning="done")
34	    assert updated["status"] == "completed"
35	    assert updated["completed_at"] is not None
36	
37	    outbound = store.create_message(
38	        epic_id="epic_1",
39	        direction="outbound",
40	        content="hi",
41	        bot_turn_id=turn["id"],
42	    )
43	    assert outbound["discord_message_id"] == f"inv_{turn['id']}_1"
44	
45	    tool_call = store.record_tool_call(
46	        turn_id=turn["id"],
47	        tool_name="send_message",
48	        operation_kind="write",
49	        arguments={"content": "hi"},
50	        result={"discord_message_id": outbound["discord_message_id"]},
51	        duration_ms=1,
52	    )
53	    assert tool_call["arguments"]["content"] == "hi"
54	
55	    log = store.log_system_event(
56	        level="info",
57	        category="system",
58	        event_type="contract",
59	        message="ok",
60	        details={"ok": True},
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -rn \"get_history\\|get_self_understanding\\|render_epic\\|get_section_names\" /Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md | head -10",
  "description": "Find tool docs in spec"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md:124:- `create_epic`, `revert` (transaction-grouped), `render_epic` tools
/Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md:125:- Read tools: `get_epic` (with section addressing), `get_section_names`, `get_history`, `get_self_understanding`
/Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md:179:- "Show me the epic" → `render_epic` called, displays body
/Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md:313:- Body referencing `![flow](image:img_data_flow)` → render_epic resolves to actual storage_url (works for both agent-generated and user-uploaded)
/Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md:1070:This is the bot's "memory snapshot" for the user — verification of what the bot is operating on. Tool: `get_self_understanding(epic_id)`.
/Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md:1649:- **Both modes (no behavioral change):** `list_epics`, `get_epic`, `get_section_names`, `get_body_outline`, `search_in_body`, `get_checklist`, `get_sprints`, `search_epics`, `recent_messages`, `search_messages`, `get_history`, `get_epic_at_time`, `get_recent_turns`, `search_tool_calls`, `get_self_understanding`, `list_images`, `view_image`, `update_image_metadata`, `edit_epic`, `create_epic`, `revert`, `render_epic`, `add_codebase`, `remove_codebase`, `list_codebases`, `get_codebase_tree`, `read_codebase_file`, `search_code`, `analyze_code`, `save_code_excerpt`, `mark_code_in_body`, `save_feedback`, `apply_feedback`, `deactivate_feedback`, `list_feedback`, `record_observation`, `list_observations`, `mark_observation_resolved`, `request_second_opinion`, `generate_image`.
/Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md:1669:- `get_section_names(epic_id)` — just the ordered list of body section names; cheap query for when bot needs to know the structure
/Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md:1677:- `get_history(epic_id, kind?, since?)` — unified audit query
/Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md:1681:- `get_self_understanding(epic_id)` — bot's structured summary
/Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md:1732:Body content can reference images using `![caption](image:reference_key)` syntax — rendered to actual storage URLs at display time via `render_epic`.
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md",
  "offset": 1066,
  "limit": 30
}
```

> TOOL

tool_result Read
```
1066	## Showing the Bot's Understanding
1067	
1068	User can ask "what do you know about this epic?" and get a structured summary: goal and current state, active checklist items, principles captured, recent decisions, code references, recent images, recent second opinion findings.
1069	
1070	This is the bot's "memory snapshot" for the user — verification of what the bot is operating on. Tool: `get_self_understanding(epic_id)`.
1071	
1072	---
1073	
1074	## User Modes
1075	
1076	The bot adapts response length, depth, and tone based on signals.
1077	
1078	**Deep-thinking mode** — user is exploring something carefully:
1079	- Signals: long messages, asking "why" or "what if," language like "I want to nail this down"
1080	- Bot behavior: longer responses, fuller reasoning, willingness to disagree explicitly, pace matched to substance
1081	
1082	**Brainstorming mode** — user is generating options:
1083	- Signals: phrases like "spitballing," "what about," "could we," rapid messages with half-formed thoughts
1084	- Bot behavior: offer alternatives, withhold judgment, propose multiple framings, shorter exchanges
1085	
1086	**Executing mode** — user wants decisions and momentum:
1087	- Signals: "let's just do X," "decide for me," short directive messages, urgency markers
1088	- Bot behavior: short responses, take positions rather than presenting options, default to action with a brief justification
1089	
1090	If signals are mixed or unclear, default to deep-thinking mode (longest, fullest) — easier to compress later than to expand from a too-short response.
1091	
1092	Mode adjustments are silent, not announced.
1093	
1094	---
1095
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md",
  "offset": 1018,
  "limit": 50
}
```

> TOOL

tool_result Read
```
1018	## Showing Changes
1019	
1020	When the bot edits the epic, response includes a brief summary of what changed: "I added a section on X and updated constraints under Y." Not the full diff.
1021	
1022	User can ask "show me the epic" anytime to see current state. Long bodies (>2000 chars) attached as markdown file rather than dumped inline.
1023	
1024	---
1025	
1026	## Reverting
1027	
1028	User can revert via natural language: "undo that," "revert the last edit," "go back to before that section."
1029	
1030	The epic_events table is append-only. State is reconstructible by replaying events. Reverts work by computing state-at-event-X and re-applying as a new event.
1031	
1032	**Transactions:** Each `edit_epic` call gets a `transaction_id`; events from one call share that ID. Default revert behavior is to undo the entire most-recent transaction (so a single `edit_epic` that updated body + checklist gets fully reverted). User can revert to a specific event for finer control.
1033	
1034	Tools:
1035	- `revert(epic_id)` — undoes most recent transaction
1036	- `revert(epic_id, event_id)` — restores to specific point in history
1037	
1038	The bot announces what it reverted and logs the revert as a new event (`reverted_to`).
1039	
1040	---
1041	
1042	## References to Bot's Recent Output
1043	
1044	Users refer to what the bot just said: "the second one," "expand on that point."
1045	
1046	The bot's most recent outbound message in this thread is in hot context. When the user uses ordinal references, the bot resolves them by parsing structure (lists, items) from that message. If ambiguous, asks: "the second sprint, or the second checklist item?"
1047	
1048	---
1049	
1050	## Epic Selection
1051	
1052	**Default heuristic:** most recently edited active epic within 24h, if exactly one matches.
1053	
1054	**Judgment overrides:** user names an epic, content matches a different one, multiple match, none match, or message is meta-instruction.
1055	
1056	**At turn start:**
1057	1. Clear match → proceed (announce switch if changed)
1058	2. Multiple plausible → ask which
1059	3. No match, content looks epic-shaped → ask new vs most recent
1060	4. Meta-instruction → handle directly
1061	
1062	The bot never silently works on the wrong epic. When it switches, it announces.
1063	
1064	---
1065	
1066	## Showing the Bot's Understanding
1067
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"FakeModel\\|class.*Model\\|complete_turn\" /Users/user_c042661f/Documents/arnold-v2/tests/helpers.py /Users/user_c042661f/Documents/arnold-v2/tests/test_run_turn.py 2>/dev/null | head -30",
  "description": "Check fake model"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/arnold-v2/tests/test_run_turn.py:8:from agent_kit.model import FakeModel
/Users/user_c042661f/Documents/arnold-v2/tests/test_run_turn.py:20:        model=FakeModel(
/Users/user_c042661f/Documents/arnold-v2/tests/test_run_turn.py:58:            model=FakeModel(seed="same"),
/Users/user_c042661f/Documents/arnold-v2/tests/test_run_turn.py:78:        model=FakeModel(script=script),
/Users/user_c042661f/Documents/arnold-v2/tests/test_run_turn.py:174:        model=FakeModel(script=[{"final_text": "unused"}]),
/Users/user_c042661f/Documents/arnold-v2/tests/test_run_turn.py:190:        model=FakeModel(
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/arnold-v2/agent_kit/model",
  "description": "List model dir"
}
```

> TOOL

tool_result Bash
```
__init__.py
__pycache__
anthropic.py
fake.py
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"epic_outline\\|turn-end\\|on_event\\|emit_event\" /Users/user_c042661f/Documents/arnold-v2/agent_kit/loop.py | head -20",
  "description": "Check loop event hooks"
}
```

> TOOL

tool_result Bash
```
32:    on_event=None,
110:            on_event=on_event,
```

> AGENT

I have enough context. Let me write the plan.

> TOOL

tool_use StructuredOutput
```json
{
  "plan": "# Implementation Plan: Sprint 2a — Editorial Core\n\n## Overview\n\nSprint 2a is the first sprint that gives Arnold a *document* to edit. Today (post Sprint 1b) the codebase has:\n- An `epics` table (already created in `supabase/migrations/202604300001_001_core.sql`) with `id, title, goal, body, state, *_at` columns. Title and goal are stored as plain columns. **No body parser yet** — the `tests/store_contract.py` fixture inserts an epic with `body='# Title'` directly.\n- A loop (`agent_kit/loop.py`) that drives a model, registers tools (`agent_kit/tool_kit.py`), records every tool call and external request, and emits events through `on_event`. The only registered tools today are `send_message`, `set_activity`, `defer_to_caller`, and image-related tools.\n- A `Store` protocol (`agent_kit/ports.py`) backed by SQLite (`agent_kit/store/sqlite.py`) for invocation mode and Postgres (`agent_kit/store/supabase.py`) for resident mode. The Store has *no* methods for epics, checklist items, or epic events yet — those appear in `load_hot_context` only by raw SQL inside Supabase.\n- A `system_logs` table and a `log()` helper (`agent_kit/logging.py`) already wired into the loop.\n\nSprint 2a's job: introduce the body-as-structured-document abstraction, a 12-item-ish tool surface for editing it, the `epic_events` audit table that powers transactional revert and time-travel reads, and a default checklist seed. Everything is **invocation-mode only** (resident mode keeps working but doesn't need new behaviour). All tests run against SQLite by default; the Supabase variant runs only when `SUPABASE_TEST_DB_URL` is set.\n\nConstraints worth naming up front:\n- The body parser is the single source of truth for `epics.title` and `epics.goal`. There is no other path that updates those columns. (Spec §1311–1320.)\n- Mutually-exclusive body operations: a single `edit_epic.body` payload picks **one** of `new_content`, `sections`, `append`, `remove_sections`, `rename_section`, or `reorder` — server rejects mixed payloads.\n- Section names are case-sensitive. Pre-section content is `_preamble`. Code fences with `##` inside are *not* section delimiters.\n- `expected_diff` comparison is \"byte-exact after normalising line endings to `\\n` and stripping trailing whitespace per line\" (spec §494).\n- Sprint 2a does NOT touch sprints/sprint_items, codebases, code_artifacts, feedback, second_opinions, or images — those land in later sprints. The `edit_epic.changes.sprints` and `state.target` paths are deliberately deferred to Sprint 4 and should return a `not_yet_supported` error if the bot tries them.\n- CLAUDE.md forbids creating a `megaplan/` directory; an existing one is harness state, not a target for edits.\n\nThe plan is six phases. Phases 1–3 land the schema, parser, and store surface (no tools yet). Phase 4 lands the tool registrations against that surface. Phase 5 wires the turn-end outline log. Phase 6 covers the integration fixture and acceptance criteria.\n\n---\n\n## Phase 1: Schema — checklist_items, epic_events\n\n### Step 1: Add Postgres migration (`supabase/migrations/202604300004_004_editorial_core.sql`)\n**Scope:** Small\n1. **Create** `checklist_items` matching spec §1322 exactly: `id TEXT PK`, `epic_id TEXT NOT NULL REFERENCES epics(id) ON DELETE CASCADE`, `content TEXT NOT NULL`, `status TEXT CHECK IN ('open','done','skipped','superseded')`, `position INTEGER NOT NULL`, `source TEXT CHECK IN ('bot_inferred','user_requested','carried_over','default_seed','second_opinion')`, `skip_reason TEXT`, `superseded_by_item_id TEXT REFERENCES checklist_items(id)`, `created_at TIMESTAMPTZ DEFAULT now()`, `completed_at TIMESTAMPTZ`. Index `(epic_id, status, position)`.\n2. **Create** `epic_events` matching spec §1381 exactly: `id TEXT PK`, `epic_id TEXT NOT NULL REFERENCES epics(id) ON DELETE CASCADE`, `transaction_id TEXT NOT NULL`, `event_type TEXT CHECK IN ('body_edit','checklist_change','sprints_change','state_change','forced_handoff','created','code_referenced','codebase_added','image_generated','second_opinion_requested','reverted_to','sprint_status_change')`, `summary TEXT NOT NULL`, `prior_state JSONB`, `turn_id TEXT REFERENCES bot_turns(id) ON DELETE SET NULL`, `occurred_at TIMESTAMPTZ DEFAULT now()`. Indexes `(epic_id, occurred_at DESC)` and `(transaction_id)`.\n\n### Step 2: Add SQLite mirror (`agent_kit/store/migrations/sqlite/004_editorial_core.sql`)\n**Scope:** Small\n1. **Mirror** the Postgres migration in SQLite syntax (TEXT for everything, no JSONB — `prior_state` becomes TEXT holding a JSON string, consistent with how `prompt_snapshot` etc. are handled in `001_core.sql`).\n2. **Register** new JSON-encoded columns in `_JSON_COLUMNS` for both `agent_kit/store/sqlite.py:17` and `agent_kit/store/supabase.py:12` so update helpers serialise `prior_state` correctly.\n\n### Step 3: Update test truncate list (`tests/test_supabase_store.py:33`)\n**Scope:** Small\n1. **Add** `checklist_items` and `epic_events` to the `TRUNCATE TABLE … RESTART IDENTITY CASCADE` block so the contract test stays green between Supabase runs.\n\n---\n\n## Phase 2: Body parser/serializer\n\n### Step 4: Create the parser module (`agent_kit/body.py`)\n**Scope:** Medium\n1. **Implement** a pure module with no Store coupling. Public surface (everything else `_private`):\n   - `parse(body: str) -> ParsedBody` where `ParsedBody` is a dataclass with `title: str | None`, `goal_first_paragraph: str | None`, `sections: list[Section]` (in order), `preamble: str` (text between title line and the first `##`, addressable as section name `_preamble` for read/write ops).\n   - `Section`: `name: str`, `content: str` (the lines after the `## Heading`, NOT including the heading line; trailing newline normalised), `subheadings: list[str]` (raw `### …` lines for outline), `line_count: int`.\n   - `serialize(parsed: ParsedBody) -> str` — round-trip identity for any input that passed `parse()` cleanly.\n   - `outline(parsed: ParsedBody) -> dict` — returns `{title, sections: [{name, line_count, subheadings}], total_lines}` for outline log + `get_body_outline`.\n2. **Enforce** the heading rules from spec §503–514:\n   - First non-blank line *must* be `# <title>` (single `#`); otherwise raise `BodyParseError(\"body_missing_required_section: title\")`.\n   - Section delimiters are lines that match `^##\\s+(.+?)\\s*$` (level-2 only). Level-3+ headings stay inside their parent section.\n   - **Code-fence guard:** track ``` and ~~~ fences during the line scan; `##` inside a fenced block is treated as content, not a delimiter. Indented (4-space) code blocks are rare in this corpus — *don't* implement that edge case for v1; document the gap in a comment on the fence-tracking helper.\n   - Section names case-sensitive; whitespace stripped from the heading text.\n3. **Implement** section operations as functions on `ParsedBody` (in-place returns of new `ParsedBody`): `replace_section(name, content)`, `append_to_section(name, content)`, `add_section(name, content, position='after:Foo'|'before:Foo'|'start'|'end')`, `remove_section(name)`, `rename_section(from_, to)`, `reorder(new_order: list[str])`. Each raises a typed error (`SectionNotFound`, `SectionExists`, `InvalidPosition`) the tool layer maps to JSON error payloads.\n4. **Implement** `validate_required(parsed: ParsedBody)` that the tool layer calls *after* applying changes and *before* writing: must contain `# title` (non-empty), and a `## Goal` section whose first non-blank paragraph is non-empty. Raise `BodyValidationError(\"body_missing_required_section: title\"|\"goal\")`.\n5. **Implement** `compute_diff(old: str, new: str) -> str` — wraps `difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True), fromfile='before', tofile='after', n=3)` and joins. **Implement** `diffs_equivalent(a: str, b: str) -> bool` that normalises both sides per spec §494 (line-endings → `\\n`, strip trailing whitespace per line, drop trailing blank lines) before equality comparison.\n\n### Step 5: Create the default-template + checklist-seed module (`agent_kit/templates.py`)\n**Scope:** Small\n1. **Constant** `DEFAULT_BODY_TEMPLATE(title: str, goal: str) -> str` — emits exactly:\n   ```\n   # {title}\n\n   ## Goal\n\n   {goal}\n\n   ## Principles\n\n   ## Context\n\n   ## Key Decisions\n\n   ## Open Questions\n\n   ## Deliverable\n   ```\n   (Six default sections per spec §466 + §524.)\n2. **Constant** `DEFAULT_CHECKLIST_SEED: list[str]` — the 18 items from spec §634, all with `source='default_seed'`, status `'open'`, positions 1–18.\n3. **Adaptation logic stays out of Sprint 2a's tool layer.** The seed is unconditional; the bot adapts during conversation by calling `edit_epic({checklist: {update|remove|add: …}})`. (Acceptance criterion: \"default checklist seeded with 18 items\".)\n\n### Step 6: Unit tests (`tests/test_body_parser.py`)\n**Scope:** Medium\n1. **Round-trip identity:** for ~6 hand-written fixture bodies (preamble-only, single section, six-section design-doc, body with `### Authentication` sub-headings under `## Key Decisions`, body with a fenced code block containing `## Step 1`, body with `_preamble` content before first `##`), assert `serialize(parse(body)) == body`.\n2. **Section ops:** for each of `replace`, `append`, `add` (each position variant), `remove`, `rename`, `reorder` — assert the only changed section is the one targeted (byte-equal compare on every other section's serialised form).\n3. **Required-element enforcement:** missing `#` line → `BodyValidationError(...title)`; empty `## Goal` first paragraph → `…goal`; `## Goal` present with content but only after another section → still passes (only first paragraph matters).\n4. **Code-fence guard:** body with ``` ` ` `` ``\\n## Inside\\n` ` `` `` `` is parsed as a single preamble (no section split).\n5. **Diff equivalence:** `diffs_equivalent` should return True when the only difference is `\\r\\n` vs `\\n`, trailing spaces, or trailing newline; False when content actually differs.\n\n---\n\n## Phase 3: Store surface for epics, checklist, events\n\n### Step 7: Extend the `Store` protocol (`agent_kit/ports.py`)\n**Scope:** Medium\n1. **Add** typed methods to the Protocol (and matching implementations in Steps 8–9):\n   - `create_epic(*, title, goal, body, state='shaping') -> JSONDict` — single-row INSERT into `epics`. Server takes title/goal/body that the *caller has already constructed and parser-validated*; the Store does not parse.\n   - `load_epic(epic_id) -> JSONDict | None`\n   - `update_epic_body(epic_id, *, body, title, goal, last_edited_at) -> JSONDict` — single UPDATE; the tool layer calls this only after parse + validate succeed.\n   - `seed_checklist(epic_id, items: list[dict]) -> list[JSONDict]` — bulk INSERT of `{content, status, position, source}` rows.\n   - `list_checklist_items(epic_id, *, status: str | list[str] | None = None) -> list[JSONDict]`\n   - `update_checklist_item(item_id, **changes) -> JSONDict`\n   - `add_checklist_items(epic_id, items, start_position) -> list[JSONDict]`\n   - `delete_checklist_items(item_ids) -> int`\n   - `record_epic_event(*, epic_id, transaction_id, event_type, summary, prior_state, turn_id) -> JSONDict`\n   - `list_epic_events(epic_id, *, since=None, kinds=None, limit=None) -> list[JSONDict]` (ordered `occurred_at, id` ascending — replay needs ascending; `get_history` reverses for display).\n   - `latest_transaction_id(epic_id) -> str | None`\n   - `events_by_transaction(transaction_id) -> list[JSONDict]`\n2. **Why both `update_epic_body` AND `record_epic_event` in the same transaction** — see Step 11. The protocol just exposes the primitives; the tool layer composes them inside `store.transaction()`.\n\n### Step 8: Implement on `SupabaseStore` (`agent_kit/store/supabase.py`)\n**Scope:** Medium\n1. **Mirror** the protocol additions with concrete SQL, using the same `_normalize`/`_json` helpers already in the module. `_new_id` prefixes: `'epic'`, `'check'`, `'evt'`.\n2. **Use `store.transaction()`** internally for `seed_checklist` (no — single bulk insert is fine; the tool composes the larger transaction).\n\n### Step 9: Implement on `SQLiteStore` (`agent_kit/store/sqlite.py`)\n**Scope:** Medium\n1. **Mirror** the same methods. Note the existing module already JSON-encodes `_JSON_COLUMNS`; add `'prior_state'` there. `epic_events.transaction_id` stays a TEXT (uuid hex string).\n\n### Step 10: Extend `tests/store_contract.py`\n**Scope:** Small\n1. **Add** a tail block to `run_store_contract` that exercises the new surface against the existing `epic_1`: seed an event, append a checklist item, list events, and assert IDs/orderings. Both Supabase and SQLite contract tests pick this up automatically.\n\n---\n\n## Phase 4: Tools — `create_epic`, `edit_epic`, `revert`, `render_epic`, reads\n\n### Step 11: Wire the editorial tool module (`agent_kit/tools/editorial.py`)\n**Scope:** Large\n1. **Register** each tool via `@register_tool` with explicit JSON schemas mirroring spec §1701 onward.\n2. **`create_epic(context, title, goal)`** —\n   - Construct body via `templates.DEFAULT_BODY_TEMPLATE(title, goal)`.\n   - `parse` + `validate_required`; on failure return `{\"error\": \"body_missing_required_section\", \"field\": …}` (don't raise — the model needs to read the message).\n   - Inside `store.transaction()`: `create_epic`, `seed_checklist(epic_id, DEFAULT_CHECKLIST_SEED)`, `record_epic_event(event_type='created', transaction_id=uuid4().hex, summary=f'Epic created with default design-doc template', prior_state=None, turn_id=context.turn_id)`.\n   - Return `{\"epic_id\", \"title\", \"goal\", \"section_names\": […], \"checklist_count\": 18, \"transaction_id\"}`.\n   - Update `context.metadata['epic_id']` so subsequent tools use the new epic without round-tripping through the model.\n3. **`edit_epic(context, epic_id, changes, change_summary, expected_diff?)`** —\n   - Reject unsupported keys: `changes.sprints` and `changes.state` return `{\"error\": \"not_yet_supported\", \"field\": \"sprints\"|\"state\"}` (Sprint 4 territory).\n   - Reject mixed body operations: at most one of `new_content`, `sections` (with optional `position` for new sections), `append`, `remove_sections`, `rename_section`, `reorder` per call. (`sections` may have multiple section names; that's still one op.)\n   - **Body path:** load current body, parse, apply the requested op(s), validate, serialise → `new_body`. Compute diff via `body.compute_diff(old, new)`. If `expected_diff` is provided and `not diffs_equivalent(expected_diff, actual_diff)`, return `{\"error\": \"expected_diff_mismatch\", \"actual_diff\": actual_diff}` and **do not write**.\n   - **Checklist path:** apply `add` (with `start_position = len(existing_open_items) + 1` if no positions given, or honouring positions and shifting where needed), `update`, `remove`. Capture prior full checklist as `prior_state` for the event.\n   - **Inside one `store.transaction()`:** `update_epic_body` (if body changed), `add/update/delete_checklist_items` (if checklist changed), and one `record_epic_event` per affected family — `body_edit` with `prior_state={'body': old_body}`, `checklist_change` with `prior_state={'items': [...]}` — all sharing the same `transaction_id = uuid4().hex`.\n   - Return `{\"transaction_id\", \"diff\": actual_diff_or_empty, \"section_names\": [...], \"change_summary\": change_summary}`.\n4. **`revert(context, epic_id, event_id?)`** —\n   - No `event_id`: look up the most recent transaction via `latest_transaction_id`, fetch all its events.\n   - With `event_id`: fetch that event and *all* events with the same transaction_id (to undo the whole edit_epic call, per spec §1399).\n   - Apply each event's `prior_state` in reverse: `body_edit` → `update_epic_body(prior body)` (re-parse to refresh title/goal); `checklist_change` → wipe current items + re-insert from snapshot.\n   - Append a single `reverted_to` event with new transaction_id and `prior_state={'reverted_transaction_id': original_txn_id, 'reverted_event_ids': [...]}` so revert is itself revertible.\n   - Return `{\"transaction_id\", \"reverted_event_count\", \"summary\"}`.\n5. **`render_epic(context, epic_id, format='markdown')`** — Sprint 2a only ships `'markdown'`; `'html'` returns `not_yet_supported`. For markdown: load body and return as-is (image reference resolution lands in Sprint 6; no-op here, but the parameter exists for forward compat).\n\n### Step 12: Read tools (`agent_kit/tools/editorial_reads.py`)\n**Scope:** Medium\n1. **`get_epic(epic_id, sections?)`** — load body, parse, return `{title, goal, body_full (when sections is None), sections: {name: content, …} (when supplied), section_names: [...], state}`.\n2. **`get_section_names(epic_id)`** — cheap; parse + return `[name, …]`.\n3. **`get_history(epic_id, kind?, since?)`** — `list_epic_events` reversed (most recent first), filtered.\n4. **`get_self_understanding(epic_id)`** — structured summary of epic (goal, state, open checklist items count, section names, last 3 events). The full 7-section snapshot per spec §1068 lands gradually; v1 returns the 5 fields above (document the gap inline).\n5. **`get_epic_at_time(epic_id, timestamp)`** — list events with `occurred_at <= timestamp` ascending; reconstruct: start with `epics` row's *earliest* state (find the `created` event's `prior_state` is null, so use the row's body and reverse-apply forward — see Note below), then for each event apply the *opposite* of `prior_state`, no — actually: replay forward from creation. **Implementation choice:** snapshot-style. We don't store post-state per event, only prior_state, so we replay backwards from the *current* state: take current body/checklist, then for each event with `occurred_at > timestamp`, overlay its `prior_state` to undo it. The earliest event whose `occurred_at > timestamp` wins for each field. Return `{body, checklist, reconstructed_at: timestamp}`.\n6. **`get_recent_turns(n=10, epic_id?)`** — query `bot_turns` ordered by `started_at DESC LIMIT n`. Add a `list_recent_turns` Store method or run raw SQL via a new Store helper. Returns each turn's id, started_at, status, triggered message snippets, and a `change_summary` aggregated from `epic_events.summary` for that turn_id.\n7. **`search_tool_calls(tool_name?, epic_id?, since?, limit=20)`** — query `tool_calls` joined to `bot_turns` for `epic_id` filter. Add Store method `search_tool_calls`.\n\n### Step 13: Register the new tools in the loop import path (`agent_kit/loop.py:16`)\n**Scope:** Small\n1. **Add** `import agent_kit.tools.editorial  # noqa: F401` and `import agent_kit.tools.editorial_reads  # noqa: F401` next to the existing `communication`/`images` imports so tools auto-register.\n\n---\n\n## Phase 5: Turn-end epic outline log\n\n### Step 14: Emit `epic_outline` after every turn that touched an epic (`agent_kit/loop.py`)\n**Scope:** Small\n1. **At the end of `run_turn`**, after the final `update_turn(status='completed')` and before returning the envelope: if `context.metadata.get('epic_id')` is set AND any tool_call this turn had `tool_name in {'create_epic','edit_epic','revert'}` (cheap: walk `events` list which already contains tool_call entries), parse the current body and call `log(store, 'info', 'application', 'epic_outline', f\"Epic outline: {title}\", details=outline.dict, turn_id=turn['id'], epic_id=epic_id)`.\n2. **Why \"any tool that touched the epic\"** — per spec §142 acceptance criterion, the row exists \"after any turn that touched an epic.\" Pure-read turns don't need an outline log. Failure paths (`status='failed'`) skip the log; that's the honest signal.\n\n---\n\n## Phase 6: Integration test + acceptance verification\n\n### Step 15: Create the 10-turn fixture conversation (`tests/test_editorial_loop.py`)\n**Scope:** Medium\n1. **Use** `FakeModel(script=…)` (already exists per `tests/test_run_turn.py:8`) with a 10-turn deterministic script that, in order:\n   - Turn 1: tool_use `create_epic(title='Auth flow design', goal='Decide on auth provider and token storage')`.\n   - Turns 2–9: a mix of `edit_epic` calls hitting **all six default sections** (`Goal`, `Principles`, `Context`, `Key Decisions`, `Open Questions`, `Deliverable`) at least once via `sections` ops, plus a couple of `append` calls and a `checklist.update` to mark items done. Include one `expected_diff` round trip and one expected_diff *mismatch* turn.\n   - Turn 10: `revert` (most recent transaction), then `send_message`.\n2. **Assertions** — one assertion per acceptance criterion in spec §131–142:\n   - After turn 1: `epics` row exists with parsed title/goal; `checklist_items` count == 18; one `created` event.\n   - After loop completes: every default section present; one section-only edit verified by re-parsing pre-state from `epic_events.prior_state` and confirming all *other* sections byte-identical.\n   - Whole-body edit path (one of turns 2–9 uses `new_content`): a `body_edit` event captured the prior body; manual call to `revert(epic_id, event_id=that_event)` followed by `load_epic(...)` returns the prior body byte-equal.\n   - \"revert that\" turn: most recent transaction undone; new `reverted_to` event present.\n   - `expected_diff` mismatch turn: tool result contains `error='expected_diff_mismatch'` and DB state unchanged.\n   - `expected_diff` match turn: writes commit normally.\n   - Direct call to `get_epic_at_time(epic_id, timestamp_after_turn_5)` returns body + checklist matching what turn 5's post-state would have looked like (compute by replaying ourselves from events).\n   - Direct call to `get_recent_turns(5)` returns 5 turns, most recent first.\n   - Direct call to `search_tool_calls(tool_name='edit_epic', epic_id=…)` returns ≥3 rows.\n   - At least one `system_logs` row per touching turn with `event_type='epic_outline'`, with `details.sections` containing all six default headings.\n\n### Step 16: Run the targeted tests, then the full suite\n**Scope:** Small\n1. **Run** `pytest tests/test_body_parser.py tests/test_editorial_loop.py -x` first.\n2. **Run** the full suite `pytest -x` to confirm no regression in Sprint 1a/1b tests (the contract tests in particular).\n3. **Optionally** run `SUPABASE_TEST_DB_URL=… pytest tests/test_supabase_store.py` if a local Supabase is available (skipped otherwise — that's the existing behaviour).\n\n---\n\n## Execution Order\n\n1. Schema first (Phase 1). Migrations are cheapest to land and unblock everything else.\n2. Body parser + templates with their unit tests (Phase 2). Pure code, fast tests, no Store coupling — best ROI on early bugs.\n3. Store extensions (Phase 3) — needed before any tool can write.\n4. Tools (Phase 4) — once the parser and store are solid, this is mostly schema-validation + glue.\n5. Outline log (Phase 5) — depends on tools existing.\n6. Integration fixture (Phase 6) — proves the whole pipeline end-to-end.\n\n## Validation Order\n\n1. `pytest tests/test_body_parser.py` — fastest feedback on parser edge cases.\n2. `pytest tests/store_contract.py`-driven tests (`tests/test_sqlite_store.py`, `tests/test_supabase_store.py` when DB available) — confirms the new Store surface is consistent across adapters.\n3. `pytest tests/test_editorial_loop.py` — the 10-turn integration.\n4. `pytest -x` — full regression.",
  "questions": [
    "Tool surface scope: the brief lists `get_history`, `get_self_understanding`, `get_epic_at_time`, `get_recent_turns`, `search_tool_calls`, `get_section_names` as read tools but the spec also mentions `get_body_outline` and `search_in_body`. Spec §163 explicitly defers those last two to Sprint 2b. Plan defers them — confirm that's correct and we're not pulling them forward.",
    "Locking semantics: an `edit_epic` mutates `epics.body` and inserts events while the existing `epic_locks` row is held by the turn (loop.py acquires it). Are concurrent invocation-mode runs against the same epic in scope for Sprint 2a, or is single-writer-by-construction acceptable (matching Sprint 1b's posture)?",
    "`get_epic_at_time` reconstruction: spec §1678 says \"replays epic_events\". Since we only store `prior_state` (not post-state), the natural implementation is to replay *backwards* from the current state — undoing every event with `occurred_at > T`. That gives the exact spec semantics. Confirm this read direction is fine, or do you want a forward-replay path that records post_state on every event?",
    "Default checklist seed adaptation: the brief mentions \"default checklist seed — 18 items with adaptation logic.\" Sprint 2a's acceptance criterion only requires the bot to seed all 18. Adaptation (drop #1 if obvious, drop #6 if no codebase, etc.) seems to belong in the bot's prompt/decision-making, not server-side at create time. Should the seed code be unconditional in v1, with adaptation deferred to the system prompt later in this sprint or Sprint 2b?",
    "Sprints/state path in `edit_epic`: Sprint 4 owns `state.target` gating and the full sprints schema. Plan returns `not_yet_supported` if the bot calls those paths in Sprint 2a. Acceptable, or should we accept-and-store-only (so the server doesn't reject mid-transaction if the bot speculatively includes them)?"
  ],
  "success_criteria": [
    {
      "criterion": "Postgres migration 004 and SQLite migration 004 create checklist_items and epic_events with the columns, CHECK constraints, FK ON DELETE behaviour, and indexes specified in spec §1322 and §1381.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Body parser round-trip identity holds: serialize(parse(body)) == body for ≥6 fixture bodies including preamble-only, single section, full design-doc template, sub-headings, fenced code containing '##', and a body with non-empty preamble.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Body parser rejects writes that would leave '# Title' missing or '## Goal' first paragraph empty, with errors body_missing_required_section: title and …: goal respectively.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "create_epic creates an epics row with parser-derived title and goal, seeds 18 default checklist items with status='open' and source='default_seed', and writes one 'created' epic_event sharing a transaction_id.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "edit_epic body section operations leave every non-targeted section byte-identical (verified by parsing prior_state captured in the body_edit event and comparing every other section's serialised form).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "edit_epic with expected_diff that does not match (after \\n + trailing-whitespace normalisation) refuses to commit, returns the actual diff, and leaves epics.body, title, goal, and checklist_items untouched.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "edit_epic with expected_diff that matches commits normally and writes one event per affected family (body_edit, checklist_change) sharing a single transaction_id.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "revert(epic_id) with no event_id undoes the entire most-recent transaction (body and checklist together) and appends a 'reverted_to' event with a new transaction_id; the resulting body is byte-equal to the pre-edit body.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "get_epic_at_time(epic_id, T) returns body and checklist state equal to what was committed at the most recent event with occurred_at <= T (verified against an explicit replay computed inside the test fixture).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "get_recent_turns(5) returns the 5 most-recent bot_turns rows (most-recent first) with summaries; search_tool_calls(tool_name='edit_epic', epic_id=X) returns every edit_epic call against epic X with arguments and timestamps.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "After every turn whose tool_calls include create_epic, edit_epic, or revert, exactly one system_logs row exists with category='application', event_type='epic_outline', turn_id=<that turn>, and details containing title plus a sections array with name + line_count for every section in the body.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "10-turn FakeModel-driven integration fixture in tests/test_editorial_loop.py runs end-to-end, exercises all six default sections, exercises both expected_diff match and mismatch paths, and exercises revert; final assertions cover every Sprint 2a acceptance criterion in spec §131–142.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "All pre-existing tests in tests/ continue to pass (no regression in Sprint 1a/1b functionality).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Body parser and section-op modules stay focused: the public surface is parse, serialize, the section ops, validate_required, compute_diff, diffs_equivalent, outline. No tool-layer or Store imports leak into agent_kit/body.py.",
      "priority": "should",
      "requires": [
        "read_files",
        "subjective_judgment"
      ]
    },
    {
      "criterion": "edit_epic rejects requests mixing two body op flavours (e.g. new_content + sections) with a clear error rather than silently picking one.",
      "priority": "should",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "agent_kit/body.py stays under ~400 lines and has no third-party dependencies beyond the standard library (difflib, re).",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    }
  ],
  "assumptions": [
    "Sprint 2a is invocation-mode only — no Discord/resident-mode behavior changes. Resident send_message and friends keep working but no new resident wiring is needed.",
    "Sprints, state transitions, codebases, code_artifacts, feedback, second_opinions, and image generation are explicitly out of scope. edit_epic returns 'not_yet_supported' when the bot includes changes.sprints or changes.state.",
    "Default body template ships with one variant (design-doc); the create_epic tool's `template` parameter from spec §534 is deferred since only one value would be valid. If needed later, it's an additive change.",
    "Default checklist seed is unconditional in v1 — all 18 items inserted on every create_epic. Adaptation logic (drop items based on goal phrasing) is the bot's job via subsequent edit_epic calls and lives in the system prompt, not server-side.",
    "expected_diff comparison normalises line endings to \\n and strips trailing whitespace per line per spec §494; trailing blank lines are also dropped before equality.",
    "get_epic_at_time uses backwards-replay from the current state (undo every event with occurred_at > T) since prior_state is the only snapshot we record. Tied timestamps order by (occurred_at, id).",
    "get_self_understanding ships a 5-field summary (goal, state, open checklist count, section names, last 3 events) — the full 7-section structure described in spec §1068 lands as later-sprint enrichment.",
    "render_epic supports format='markdown' only in v1; format='html' returns 'not_yet_supported'. Image-reference resolution is a no-op until Sprint 6.",
    "epic_outline log fires for any turn whose tool_calls touched create_epic, edit_epic, or revert — pure-read turns don't emit the log, matching the spec wording 'turn that touched an epic'.",
    "Single-writer concurrency is acceptable; the existing `epic_locks` mechanism plus the per-edit_epic store.transaction wrapper is sufficient. No additional locking is added in Sprint 2a.",
    "The repo's existing `megaplan/` directory is harness state and is left untouched; CLAUDE.md's prohibition applies to creating it, not to its presence."
  ]
}
```

> TOOL

tool_result StructuredOutput
```
Structured output provided successfully
```

> AGENT

Plan delivered as structured output. Highlights:

- **6 phases:** schema → body parser → store surface → tools → outline log → integration test.
- **Single new module `agent_kit/body.py`** owns parse/serialize/section-ops/diff with no Store coupling, and a thin `agent_kit/templates.py` for the design-doc template + 18-item seed.
- **Two migrations** (Postgres + SQLite mirror) for `checklist_items` and `epic_events`, plus a `TRUNCATE` update so the existing Supabase contract test keeps passing.
- **Tools** split across `agent_kit/tools/editorial.py` (writes: `create_epic`, `edit_epic`, `revert`, `render_epic`) and `agent_kit/tools/editorial_reads.py` (reads). `edit_epic` rejects mixed body ops and `not_yet_supported`s the Sprint 4 sprints/state paths.
- **Validation:** parser unit tests first, then store contract, then a 10-turn `FakeModel` integration fixture mapping 1:1 to the spec's acceptance criteria (incl. expected_diff match + mismatch + revert + epic_outline log).
- **Open questions called out:** scope of read tools (deferring `get_body_outline` / `search_in_body` to 2b per spec), backwards-replay semantics for `get_epic_at_time`, where checklist adaptation lives, and whether `state.target` should soft-reject or accept-and-store.

> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

You are revising an implementation plan after critique and gate feedback.

        Project directory:
        /Users/user_c042661f/Documents/arnold-v2




        Idea:
# Sprint 2a — Editorial core

Bot maintains an epic body and checklist for one epic, with section-level body editing. Minimum to have an editorial conversation.

**Full spec is at `planning-bot-spec.md` in this repo root. Refer to it for complete details on Body Structure and Editing, Body Templates, The Checklist as Guide, and Data Model sections.**

## Supabase
- URL: https://yhwflvadmefhkshwbfnf.supabase.co
- Service key: [REDACTED_SUPABASE_SERVICE_ROLE_JWT]

## Scope

- Tables: checklist_items, epic_events (with transaction_id)
- Body parser/serializer — markdown ↔ structured sections with ## heading delimiters; enforces heading hierarchy (# for title only, ## for sections, ### for sub-headings)
- Turn-end epic outline emitted to system_logs at info level
- Default body template (design doc) — Goal, Principles, Context, Key Decisions, Open Questions, Deliverable
- `edit_epic` tool — body (whole + section ops) + checklist; supports:
  - Write whole body
  - Write specific sections
  - Append to a section
  - Add new section with position
  - Rename/remove sections
  - `expected_diff` parameter for server-enforced diff verification (unified diff format)
- `create_epic`, `revert` (transaction-grouped), `render_epic` tools
- Read tools: `get_epic` (with section addressing), `get_section_names`, `get_history`, `get_self_understanding`
- History tools: `get_epic_at_time`, `get_recent_turns`, `search_tool_calls`
- Default checklist seed — 18 items with adaptation logic
- Title and goal are derived columns from body parsing (# Title and ## Goal first paragraph)

## Key Data Model

### checklist_items
id, epic_id, content, status (open|done|skipped|superseded), position, source (bot_inferred|user_requested|carried_over|default_seed|second_opinion), skip_reason, superseded_by_item_id, created_at, completed_at

### epic_events
id, epic_id, transaction_id (uuid), event_type, summary, prior_state (json), turn_id, occurred_at
Event types: body_edit, checklist_change, sprints_change, state_change, forced_handoff, created, code_referenced, codebase_added, image_generated, second_opinion_requested, reverted_to, sprint_status_change

## Body Parser Rules
- Section boundaries are ## headings (level-2 markdown)
- Section names are case-sensitive
- Pre-section content is "_preamble"
- Sub-sections (### and below) are part of parent section
- No ## headings → whole body is _preamble
- # Title and ## Goal are required structural elements; missing → write rejected
- Code blocks containing ## are NOT section boundaries

## Acceptance Criteria

- Create an epic via natural language → epics row created, default checklist seeded with 18 items, body initialized
- 10-turn scripted conversation (mocked Anthropic) produces body with all 6 default sections
- Section-level edit → only that section changes; other sections byte-identical
- Whole body edit → diff captured in event; revert restores prior version exactly
- "revert that" → most recent transaction undone, new reverted_to event logged
- expected_diff mismatch → server refuses write, returns actual diff
- expected_diff match → server commits normally
- get_epic_at_time(epic_id, T) → returns body/checklist state as of time T
- get_recent_turns(5) → returns 5 most recent turns with summaries
- search_tool_calls(tool_name='edit_epic', epic_id=X) → returns matching calls
- Turn-end system_logs row with event_type='epic_outline' containing title + section list + line counts

## Tests
- Unit: body parser (markdown → sections → markdown roundtrip is identity); section operations; edit_epic validation; transaction_id grouping; expected_diff comparison; epic-at-time replay
- Integration: 10-turn fixture conversation against local Supabase with mocked Anthropic; revert end-to-end

        Current plan (markdown):
        # Implementation Plan: Sprint 2a — Editorial Core

## Overview

Sprint 2a is the first sprint that gives Arnold a *document* to edit. Today (post Sprint 1b) the codebase has:
- An `epics` table (already created in `supabase/migrations/202604300001_001_core.sql`) with `id, title, goal, body, state, *_at` columns. Title and goal are stored as plain columns. **No body parser yet** — the `tests/store_contract.py` fixture inserts an epic with `body='# Title'` directly.
- A loop (`agent_kit/loop.py`) that drives a model, registers tools (`agent_kit/tool_kit.py`), records every tool call and external request, and emits events through `on_event`. The only registered tools today are `send_message`, `set_activity`, `defer_to_caller`, and image-related tools.
- A `Store` protocol (`agent_kit/ports.py`) backed by SQLite (`agent_kit/store/sqlite.py`) for invocation mode and Postgres (`agent_kit/store/supabase.py`) for resident mode. The Store has *no* methods for epics, checklist items, or epic events yet — those appear in `load_hot_context` only by raw SQL inside Supabase.
- A `system_logs` table and a `log()` helper (`agent_kit/logging.py`) already wired into the loop.

Sprint 2a's job: introduce the body-as-structured-document abstraction, a 12-item-ish tool surface for editing it, the `epic_events` audit table that powers transactional revert and time-travel reads, and a default checklist seed. Everything is **invocation-mode only** (resident mode keeps working but doesn't need new behaviour). All tests run against SQLite by default; the Supabase variant runs only when `SUPABASE_TEST_DB_URL` is set.

Constraints worth naming up front:
- The body parser is the single source of truth for `epics.title` and `epics.goal`. There is no other path that updates those columns. (Spec §1311–1320.)
- Mutually-exclusive body operations: a single `edit_epic.body` payload picks **one** of `new_content`, `sections`, `append`, `remove_sections`, `rename_section`, or `reorder` — server rejects mixed payloads.
- Section names are case-sensitive. Pre-section content is `_preamble`. Code fences with `##` inside are *not* section delimiters.
- `expected_diff` comparison is "byte-exact after normalising line endings to `\n` and stripping trailing whitespace per line" (spec §494).
- Sprint 2a does NOT touch sprints/sprint_items, codebases, code_artifacts, feedback, second_opinions, or images — those land in later sprints. The `edit_epic.changes.sprints` and `state.target` paths are deliberately deferred to Sprint 4 and should return a `not_yet_supported` error if the bot tries them.
- CLAUDE.md forbids creating a `megaplan/` directory; an existing one is harness state, not a target for edits.

The plan is six phases. Phases 1–3 land the schema, parser, and store surface (no tools yet). Phase 4 lands the tool registrations against that surface. Phase 5 wires the turn-end outline log. Phase 6 covers the integration fixture and acceptance criteria.

---

## Phase 1: Schema — checklist_items, epic_events

### Step 1: Add Postgres migration (`supabase/migrations/202604300004_004_editorial_core.sql`)
**Scope:** Small
1. **Create** `checklist_items` matching spec §1322 exactly: `id TEXT PK`, `epic_id TEXT NOT NULL REFERENCES epics(id) ON DELETE CASCADE`, `content TEXT NOT NULL`, `status TEXT CHECK IN ('open','done','skipped','superseded')`, `position INTEGER NOT NULL`, `source TEXT CHECK IN ('bot_inferred','user_requested','carried_over','default_seed','second_opinion')`, `skip_reason TEXT`, `superseded_by_item_id TEXT REFERENCES checklist_items(id)`, `created_at TIMESTAMPTZ DEFAULT now()`, `completed_at TIMESTAMPTZ`. Index `(epic_id, status, position)`.
2. **Create** `epic_events` matching spec §1381 exactly: `id TEXT PK`, `epic_id TEXT NOT NULL REFERENCES epics(id) ON DELETE CASCADE`, `transaction_id TEXT NOT NULL`, `event_type TEXT CHECK IN ('body_edit','checklist_change','sprints_change','state_change','forced_handoff','created','code_referenced','codebase_added','image_generated','second_opinion_requested','reverted_to','sprint_status_change')`, `summary TEXT NOT NULL`, `prior_state JSONB`, `turn_id TEXT REFERENCES bot_turns(id) ON DELETE SET NULL`, `occurred_at TIMESTAMPTZ DEFAULT now()`. Indexes `(epic_id, occurred_at DESC)` and `(transaction_id)`.

### Step 2: Add SQLite mirror (`agent_kit/store/migrations/sqlite/004_editorial_core.sql`)
**Scope:** Small
1. **Mirror** the Postgres migration in SQLite syntax (TEXT for everything, no JSONB — `prior_state` becomes TEXT holding a JSON string, consistent with how `prompt_snapshot` etc. are handled in `001_core.sql`).
2. **Register** new JSON-encoded columns in `_JSON_COLUMNS` for both `agent_kit/store/sqlite.py:17` and `agent_kit/store/supabase.py:12` so update helpers serialise `prior_state` correctly.

### Step 3: Update test truncate list (`tests/test_supabase_store.py:33`)
**Scope:** Small
1. **Add** `checklist_items` and `epic_events` to the `TRUNCATE TABLE … RESTART IDENTITY CASCADE` block so the contract test stays green between Supabase runs.

---

## Phase 2: Body parser/serializer

### Step 4: Create the parser module (`agent_kit/body.py`)
**Scope:** Medium
1. **Implement** a pure module with no Store coupling. Public surface (everything else `_private`):
   - `parse(body: str) -> ParsedBody` where `ParsedBody` is a dataclass with `title: str | None`, `goal_first_paragraph: str | None`, `sections: list[Section]` (in order), `preamble: str` (text between title line and the first `##`, addressable as section name `_preamble` for read/write ops).
   - `Section`: `name: str`, `content: str` (the lines after the `## Heading`, NOT including the heading line; trailing newline normalised), `subheadings: list[str]` (raw `### …` lines for outline), `line_count: int`.
   - `serialize(parsed: ParsedBody) -> str` — round-trip identity for any input that passed `parse()` cleanly.
   - `outline(parsed: ParsedBody) -> dict` — returns `{title, sections: [{name, line_count, subheadings}], total_lines}` for outline log + `get_body_outline`.
2. **Enforce** the heading rules from spec §503–514:
   - First non-blank line *must* be `# <title>` (single `#`); otherwise raise `BodyParseError("body_missing_required_section: title")`.
   - Section delimiters are lines that match `^##\s+(.+?)\s*$` (level-2 only). Level-3+ headings stay inside their parent section.
   - **Code-fence guard:** track ``` and ~~~ fences during the line scan; `##` inside a fenced block is treated as content, not a delimiter. Indented (4-space) code blocks are rare in this corpus — *don't* implement that edge case for v1; document the gap in a comment on the fence-tracking helper.
   - Section names case-sensitive; whitespace stripped from the heading text.
3. **Implement** section operations as functions on `ParsedBody` (in-place returns of new `ParsedBody`): `replace_section(name, content)`, `append_to_section(name, content)`, `add_section(name, content, position='after:Foo'|'before:Foo'|'start'|'end')`, `remove_section(name)`, `rename_section(from_, to)`, `reorder(new_order: list[str])`. Each raises a typed error (`SectionNotFound`, `SectionExists`, `InvalidPosition`) the tool layer maps to JSON error payloads.
4. **Implement** `validate_required(parsed: ParsedBody)` that the tool layer calls *after* applying changes and *before* writing: must contain `# title` (non-empty), and a `## Goal` section whose first non-blank paragraph is non-empty. Raise `BodyValidationError("body_missing_required_section: title"|"goal")`.
5. **Implement** `compute_diff(old: str, new: str) -> str` — wraps `difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True), fromfile='before', tofile='after', n=3)` and joins. **Implement** `diffs_equivalent(a: str, b: str) -> bool` that normalises both sides per spec §494 (line-endings → `\n`, strip trailing whitespace per line, drop trailing blank lines) before equality comparison.

### Step 5: Create the default-template + checklist-seed module (`agent_kit/templates.py`)
**Scope:** Small
1. **Constant** `DEFAULT_BODY_TEMPLATE(title: str, goal: str) -> str` — emits exactly:
   ```
   # {title}

   ## Goal

   {goal}

   ## Principles

   ## Context

   ## Key Decisions

   ## Open Questions

   ## Deliverable
   ```
   (Six default sections per spec §466 + §524.)
2. **Constant** `DEFAULT_CHECKLIST_SEED: list[str]` — the 18 items from spec §634, all with `source='default_seed'`, status `'open'`, positions 1–18.
3. **Adaptation logic stays out of Sprint 2a's tool layer.** The seed is unconditional; the bot adapts during conversation by calling `edit_epic({checklist: {update|remove|add: …}})`. (Acceptance criterion: "default checklist seeded with 18 items".)

### Step 6: Unit tests (`tests/test_body_parser.py`)
**Scope:** Medium
1. **Round-trip identity:** for ~6 hand-written fixture bodies (preamble-only, single section, six-section design-doc, body with `### Authentication` sub-headings under `## Key Decisions`, body with a fenced code block containing `## Step 1`, body with `_preamble` content before first `##`), assert `serialize(parse(body)) == body`.
2. **Section ops:** for each of `replace`, `append`, `add` (each position variant), `remove`, `rename`, `reorder` — assert the only changed section is the one targeted (byte-equal compare on every other section's serialised form).
3. **Required-element enforcement:** missing `#` line → `BodyValidationError(...title)`; empty `## Goal` first paragraph → `…goal`; `## Goal` present with content but only after another section → still passes (only first paragraph matters).
4. **Code-fence guard:** body with ``` ` ` `` ``\n## Inside\n` ` `` `` `` is parsed as a single preamble (no section split).
5. **Diff equivalence:** `diffs_equivalent` should return True when the only difference is `\r\n` vs `\n`, trailing spaces, or trailing newline; False when content actually differs.

---

## Phase 3: Store surface for epics, checklist, events

### Step 7: Extend the `Store` protocol (`agent_kit/ports.py`)
**Scope:** Medium
1. **Add** typed methods to the Protocol (and matching implementations in Steps 8–9):
   - `create_epic(*, title, goal, body, state='shaping') -> JSONDict` — single-row INSERT into `epics`. Server takes title/goal/body that the *caller has already constructed and parser-validated*; the Store does not parse.
   - `load_epic(epic_id) -> JSONDict | None`
   - `update_epic_body(epic_id, *, body, title, goal, last_edited_at) -> JSONDict` — single UPDATE; the tool layer calls this only after parse + validate succeed.
   - `seed_checklist(epic_id, items: list[dict]) -> list[JSONDict]` — bulk INSERT of `{content, status, position, source}` rows.
   - `list_checklist_items(epic_id, *, status: str | list[str] | None = None) -> list[JSONDict]`
   - `update_checklist_item(item_id, **changes) -> JSONDict`
   - `add_checklist_items(epic_id, items, start_position) -> list[JSONDict]`
   - `delete_checklist_items(item_ids) -> int`
   - `record_epic_event(*, epic_id, transaction_id, event_type, summary, prior_state, turn_id) -> JSONDict`
   - `list_epic_events(epic_id, *, since=None, kinds=None, limit=None) -> list[JSONDict]` (ordered `occurred_at, id` ascending — replay needs ascending; `get_history` reverses for display).
   - `latest_transaction_id(epic_id) -> str | None`
   - `events_by_transaction(transaction_id) -> list[JSONDict]`
2. **Why both `update_epic_body` AND `record_epic_event` in the same transaction** — see Step 11. The protocol just exposes the primitives; the tool layer composes them inside `store.transaction()`.

### Step 8: Implement on `SupabaseStore` (`agent_kit/store/supabase.py`)
**Scope:** Medium
1. **Mirror** the protocol additions with concrete SQL, using the same `_normalize`/`_json` helpers already in the module. `_new_id` prefixes: `'epic'`, `'check'`, `'evt'`.
2. **Use `store.transaction()`** internally for `seed_checklist` (no — single bulk insert is fine; the tool composes the larger transaction).

### Step 9: Implement on `SQLiteStore` (`agent_kit/store/sqlite.py`)
**Scope:** Medium
1. **Mirror** the same methods. Note the existing module already JSON-encodes `_JSON_COLUMNS`; add `'prior_state'` there. `epic_events.transaction_id` stays a TEXT (uuid hex string).

### Step 10: Extend `tests/store_contract.py`
**Scope:** Small
1. **Add** a tail block to `run_store_contract` that exercises the new surface against the existing `epic_1`: seed an event, append a checklist item, list events, and assert IDs/orderings. Both Supabase and SQLite contract tests pick this up automatically.

---

## Phase 4: Tools — `create_epic`, `edit_epic`, `revert`, `render_epic`, reads

### Step 11: Wire the editorial tool module (`agent_kit/tools/editorial.py`)
**Scope:** Large
1. **Register** each tool via `@register_tool` with explicit JSON schemas mirroring spec §1701 onward.
2. **`create_epic(context, title, goal)`** —
   - Construct body via `templates.DEFAULT_BODY_TEMPLATE(title, goal)`.
   - `parse` + `validate_required`; on failure return `{"error": "body_missing_required_section", "field": …}` (don't raise — the model needs to read the message).
   - Inside `store.transaction()`: `create_epic`, `seed_checklist(epic_id, DEFAULT_CHECKLIST_SEED)`, `record_epic_event(event_type='created', transaction_id=uuid4().hex, summary=f'Epic created with default design-doc template', prior_state=None, turn_id=context.turn_id)`.
   - Return `{"epic_id", "title", "goal", "section_names": […], "checklist_count": 18, "transaction_id"}`.
   - Update `context.metadata['epic_id']` so subsequent tools use the new epic without round-tripping through the model.
3. **`edit_epic(context, epic_id, changes, change_summary, expected_diff?)`** —
   - Reject unsupported keys: `changes.sprints` and `changes.state` return `{"error": "not_yet_supported", "field": "sprints"|"state"}` (Sprint 4 territory).
   - Reject mixed body operations: at most one of `new_content`, `sections` (with optional `position` for new sections), `append`, `remove_sections`, `rename_section`, `reorder` per call. (`sections` may have multiple section names; that's still one op.)
   - **Body path:** load current body, parse, apply the requested op(s), validate, serialise → `new_body`. Compute diff via `body.compute_diff(old, new)`. If `expected_diff` is provided and `not diffs_equivalent(expected_diff, actual_diff)`, return `{"error": "expected_diff_mismatch", "actual_diff": actual_diff}` and **do not write**.
   - **Checklist path:** apply `add` (with `start_position = len(existing_open_items) + 1` if no positions given, or honouring positions and shifting where needed), `update`, `remove`. Capture prior full checklist as `prior_state` for the event.
   - **Inside one `store.transaction()`:** `update_epic_body` (if body changed), `add/update/delete_checklist_items` (if checklist changed), and one `record_epic_event` per affected family — `body_edit` with `prior_state={'body': old_body}`, `checklist_change` with `prior_state={'items': [...]}` — all sharing the same `transaction_id = uuid4().hex`.
   - Return `{"transaction_id", "diff": actual_diff_or_empty, "section_names": [...], "change_summary": change_summary}`.
4. **`revert(context, epic_id, event_id?)`** —
   - No `event_id`: look up the most recent transaction via `latest_transaction_id`, fetch all its events.
   - With `event_id`: fetch that event and *all* events with the same transaction_id (to undo the whole edit_epic call, per spec §1399).
   - Apply each event's `prior_state` in reverse: `body_edit` → `update_epic_body(prior body)` (re-parse to refresh title/goal); `checklist_change` → wipe current items + re-insert from snapshot.
   - Append a single `reverted_to` event with new transaction_id and `prior_state={'reverted_transaction_id': original_txn_id, 'reverted_event_ids': [...]}` so revert is itself revertible.
   - Return `{"transaction_id", "reverted_event_count", "summary"}`.
5. **`render_epic(context, epic_id, format='markdown')`** — Sprint 2a only ships `'markdown'`; `'html'` returns `not_yet_supported`. For markdown: load body and return as-is (image reference resolution lands in Sprint 6; no-op here, but the parameter exists for forward compat).

### Step 12: Read tools (`agent_kit/tools/editorial_reads.py`)
**Scope:** Medium
1. **`get_epic(epic_id, sections?)`** — load body, parse, return `{title, goal, body_full (when sections is None), sections: {name: content, …} (when supplied), section_names: [...], state}`.
2. **`get_section_names(epic_id)`** — cheap; parse + return `[name, …]`.
3. **`get_history(epic_id, kind?, since?)`** — `list_epic_events` reversed (most recent first), filtered.
4. **`get_self_understanding(epic_id)`** — structured summary of epic (goal, state, open checklist items count, section names, last 3 events). The full 7-section snapshot per spec §1068 lands gradually; v1 returns the 5 fields above (document the gap inline).
5. **`get_epic_at_time(epic_id, timestamp)`** — list events with `occurred_at <= timestamp` ascending; reconstruct: start with `epics` row's *earliest* state (find the `created` event's `prior_state` is null, so use the row's body and reverse-apply forward — see Note below), then for each event apply the *opposite* of `prior_state`, no — actually: replay forward from creation. **Implementation choice:** snapshot-style. We don't store post-state per event, only prior_state, so we replay backwards from the *current* state: take current body/checklist, then for each event with `occurred_at > timestamp`, overlay its `prior_state` to undo it. The earliest event whose `occurred_at > timestamp` wins for each field. Return `{body, checklist, reconstructed_at: timestamp}`.
6. **`get_recent_turns(n=10, epic_id?)`** — query `bot_turns` ordered by `started_at DESC LIMIT n`. Add a `list_recent_turns` Store method or run raw SQL via a new Store helper. Returns each turn's id, started_at, status, triggered message snippets, and a `change_summary` aggregated from `epic_events.summary` for that turn_id.
7. **`search_tool_calls(tool_name?, epic_id?, since?, limit=20)`** — query `tool_calls` joined to `bot_turns` for `epic_id` filter. Add Store method `search_tool_calls`.

### Step 13: Register the new tools in the loop import path (`agent_kit/loop.py:16`)
**Scope:** Small
1. **Add** `import agent_kit.tools.editorial  # noqa: F401` and `import agent_kit.tools.editorial_reads  # noqa: F401` next to the existing `communication`/`images` imports so tools auto-register.

---

## Phase 5: Turn-end epic outline log

### Step 14: Emit `epic_outline` after every turn that touched an epic (`agent_kit/loop.py`)
**Scope:** Small
1. **At the end of `run_turn`**, after the final `update_turn(status='completed')` and before returning the envelope: if `context.metadata.get('epic_id')` is set AND any tool_call this turn had `tool_name in {'create_epic','edit_epic','revert'}` (cheap: walk `events` list which already contains tool_call entries), parse the current body and call `log(store, 'info', 'application', 'epic_outline', f"Epic outline: {title}", details=outline.dict, turn_id=turn['id'], epic_id=epic_id)`.
2. **Why "any tool that touched the epic"** — per spec §142 acceptance criterion, the row exists "after any turn that touched an epic." Pure-read turns don't need an outline log. Failure paths (`status='failed'`) skip the log; that's the honest signal.

---

## Phase 6: Integration test + acceptance verification

### Step 15: Create the 10-turn fixture conversation (`tests/test_editorial_loop.py`)
**Scope:** Medium
1. **Use** `FakeModel(script=…)` (already exists per `tests/test_run_turn.py:8`) with a 10-turn deterministic script that, in order:
   - Turn 1: tool_use `create_epic(title='Auth flow design', goal='Decide on auth provider and token storage')`.
   - Turns 2–9: a mix of `edit_epic` calls hitting **all six default sections** (`Goal`, `Principles`, `Context`, `Key Decisions`, `Open Questions`, `Deliverable`) at least once via `sections` ops, plus a couple of `append` calls and a `checklist.update` to mark items done. Include one `expected_diff` round trip and one expected_diff *mismatch* turn.
   - Turn 10: `revert` (most recent transaction), then `send_message`.
2. **Assertions** — one assertion per acceptance criterion in spec §131–142:
   - After turn 1: `epics` row exists with parsed title/goal; `checklist_items` count == 18; one `created` event.
   - After loop completes: every default section present; one section-only edit verified by re-parsing pre-state from `epic_events.prior_state` and confirming all *other* sections byte-identical.
   - Whole-body edit path (one of turns 2–9 uses `new_content`): a `body_edit` event captured the prior body; manual call to `revert(epic_id, event_id=that_event)` followed by `load_epic(...)` returns the prior body byte-equal.
   - "revert that" turn: most recent transaction undone; new `reverted_to` event present.
   - `expected_diff` mismatch turn: tool result contains `error='expected_diff_mismatch'` and DB state unchanged.
   - `expected_diff` match turn: writes commit normally.
   - Direct call to `get_epic_at_time(epic_id, timestamp_after_turn_5)` returns body + checklist matching what turn 5's post-state would have looked like (compute by replaying ourselves from events).
   - Direct call to `get_recent_turns(5)` returns 5 turns, most recent first.
   - Direct call to `search_tool_calls(tool_name='edit_epic', epic_id=…)` returns ≥3 rows.
   - At least one `system_logs` row per touching turn with `event_type='epic_outline'`, with `details.sections` containing all six default headings.

### Step 16: Run the targeted tests, then the full suite
**Scope:** Small
1. **Run** `pytest tests/test_body_parser.py tests/test_editorial_loop.py -x` first.
2. **Run** the full suite `pytest -x` to confirm no regression in Sprint 1a/1b tests (the contract tests in particular).
3. **Optionally** run `SUPABASE_TEST_DB_URL=… pytest tests/test_supabase_store.py` if a local Supabase is available (skipped otherwise — that's the existing behaviour).

---

## Execution Order

1. Schema first (Phase 1). Migrations are cheapest to land and unblock everything else.
2. Body parser + templates with their unit tests (Phase 2). Pure code, fast tests, no Store coupling — best ROI on early bugs.
3. Store extensions (Phase 3) — needed before any tool can write.
4. Tools (Phase 4) — once the parser and store are solid, this is mostly schema-validation + glue.
5. Outline log (Phase 5) — depends on tools existing.
6. Integration fixture (Phase 6) — proves the whole pipeline end-to-end.

## Validation Order

1. `pytest tests/test_body_parser.py` — fastest feedback on parser edge cases.
2. `pytest tests/store_contract.py`-driven tests (`tests/test_sqlite_store.py`, `tests/test_supabase_store.py` when DB available) — confirms the new Store surface is consistent across adapters.
3. `pytest tests/test_editorial_loop.py` — the 10-turn integration.
4. `pytest -x` — full regression.


        Current plan metadata:
        {
  "version": 1,
  "timestamp": "2026-04-30T05:19:39Z",
  "hash": "sha256:55da79b2775c5dfce81878da5a6ed5d307144229a858dbb11d6d4e334c7b5a2e",
  "questions": [
    "Tool surface scope: the brief lists `get_history`, `get_self_understanding`, `get_epic_at_time`, `get_recent_turns`, `search_tool_calls`, `get_section_names` as read tools but the spec also mentions `get_body_outline` and `search_in_body`. Spec \u00a7163 explicitly defers those last two to Sprint 2b. Plan defers them \u2014 confirm that's correct and we're not pulling them forward.",
    "Locking semantics: an `edit_epic` mutates `epics.body` and inserts events while the existing `epic_locks` row is held by the turn (loop.py acquires it). Are concurrent invocation-mode runs against the same epic in scope for Sprint 2a, or is single-writer-by-construction acceptable (matching Sprint 1b's posture)?",
    "`get_epic_at_time` reconstruction: spec \u00a71678 says \"replays epic_events\". Since we only store `prior_state` (not post-state), the natural implementation is to replay *backwards* from the current state \u2014 undoing every event with `occurred_at > T`. That gives the exact spec semantics. Confirm this read direction is fine, or do you want a forward-replay path that records post_state on every event?",
    "Default checklist seed adaptation: the brief mentions \"default checklist seed \u2014 18 items with adaptation logic.\" Sprint 2a's acceptance criterion only requires the bot to seed all 18. Adaptation (drop #1 if obvious, drop #6 if no codebase, etc.) seems to belong in the bot's prompt/decision-making, not server-side at create time. Should the seed code be unconditional in v1, with adaptation deferred to the system prompt later in this sprint or Sprint 2b?",
    "Sprints/state path in `edit_epic`: Sprint 4 owns `state.target` gating and the full sprints schema. Plan returns `not_yet_supported` if the bot calls those paths in Sprint 2a. Acceptable, or should we accept-and-store-only (so the server doesn't reject mid-transaction if the bot speculatively includes them)?"
  ],
  "success_criteria": [
    {
      "criterion": "Postgres migration 004 and SQLite migration 004 create checklist_items and epic_events with the columns, CHECK constraints, FK ON DELETE behaviour, and indexes specified in spec \u00a71322 and \u00a71381.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Body parser round-trip identity holds: serialize(parse(body)) == body for \u22656 fixture bodies including preamble-only, single section, full design-doc template, sub-headings, fenced code containing '##', and a body with non-empty preamble.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Body parser rejects writes that would leave '# Title' missing or '## Goal' first paragraph empty, with errors body_missing_required_section: title and \u2026: goal respectively.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "create_epic creates an epics row with parser-derived title and goal, seeds 18 default checklist items with status='open' and source='default_seed', and writes one 'created' epic_event sharing a transaction_id.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "edit_epic body section operations leave every non-targeted section byte-identical (verified by parsing prior_state captured in the body_edit event and comparing every other section's serialised form).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "edit_epic with expected_diff that does not match (after \\n + trailing-whitespace normalisation) refuses to commit, returns the actual diff, and leaves epics.body, title, goal, and checklist_items untouched.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "edit_epic with expected_diff that matches commits normally and writes one event per affected family (body_edit, checklist_change) sharing a single transaction_id.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "revert(epic_id) with no event_id undoes the entire most-recent transaction (body and checklist together) and appends a 'reverted_to' event with a new transaction_id; the resulting body is byte-equal to the pre-edit body.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "get_epic_at_time(epic_id, T) returns body and checklist state equal to what was committed at the most recent event with occurred_at <= T (verified against an explicit replay computed inside the test fixture).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "get_recent_turns(5) returns the 5 most-recent bot_turns rows (most-recent first) with summaries; search_tool_calls(tool_name='edit_epic', epic_id=X) returns every edit_epic call against epic X with arguments and timestamps.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "After every turn whose tool_calls include create_epic, edit_epic, or revert, exactly one system_logs row exists with category='application', event_type='epic_outline', turn_id=<that turn>, and details containing title plus a sections array with name + line_count for every section in the body.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "10-turn FakeModel-driven integration fixture in tests/test_editorial_loop.py runs end-to-end, exercises all six default sections, exercises both expected_diff match and mismatch paths, and exercises revert; final assertions cover every Sprint 2a acceptance criterion in spec \u00a7131\u2013142.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "All pre-existing tests in tests/ continue to pass (no regression in Sprint 1a/1b functionality).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Body parser and section-op modules stay focused: the public surface is parse, serialize, the section ops, validate_required, compute_diff, diffs_equivalent, outline. No tool-layer or Store imports leak into agent_kit/body.py.",
      "priority": "should",
      "requires": [
        "read_files",
        "subjective_judgment"
      ]
    },
    {
      "criterion": "edit_epic rejects requests mixing two body op flavours (e.g. new_content + sections) with a clear error rather than silently picking one.",
      "priority": "should",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "agent_kit/body.py stays under ~400 lines and has no third-party dependencies beyond the standard library (difflib, re).",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    }
  ],
  "assumptions": [
    "Sprint 2a is invocation-mode only \u2014 no Discord/resident-mode behavior changes. Resident send_message and friends keep working but no new resident wiring is needed.",
    "Sprints, state transitions, codebases, code_artifacts, feedback, second_opinions, and image generation are explicitly out of scope. edit_epic returns 'not_yet_supported' when the bot includes changes.sprints or changes.state.",
    "Default body template ships with one variant (design-doc); the create_epic tool's `template` parameter from spec \u00a7534 is deferred since only one value would be valid. If needed later, it's an additive change.",
    "Default checklist seed is unconditional in v1 \u2014 all 18 items inserted on every create_epic. Adaptation logic (drop items based on goal phrasing) is the bot's job via subsequent edit_epic calls and lives in the system prompt, not server-side.",
    "expected_diff comparison normalises line endings to \\n and strips trailing whitespace per line per spec \u00a7494; trailing blank lines are also dropped before equality.",
    "get_epic_at_time uses backwards-replay from the current state (undo every event with occurred_at > T) since prior_state is the only snapshot we record. Tied timestamps order by (occurred_at, id).",
    "get_self_understanding ships a 5-field summary (goal, state, open checklist count, section names, last 3 events) \u2014 the full 7-section structure described in spec \u00a71068 lands as later-sprint enrichment.",
    "render_epic supports format='markdown' only in v1; format='html' returns 'not_yet_supported'. Image-reference resolution is a no-op until Sprint 6.",
    "epic_outline log fires for any turn whose tool_calls touched create_epic, edit_epic, or revert \u2014 pure-read turns don't emit the log, matching the spec wording 'turn that touched an epic'.",
    "Single-writer concurrency is acceptable; the existing `epic_locks` mechanism plus the per-edit_epic store.transaction wrapper is sufficient. No additional locking is added in Sprint 2a.",
    "The repo's existing `megaplan/` directory is harness state and is left untouched; CLAUDE.md's prohibition applies to creating it, not to its presence."
  ],
  "structure_warnings": []
}

        Gate summary:
        {
  "passed": false,
  "criteria_check": {
    "count": 16,
    "items": [
      {
        "criterion": "Postgres migration 004 and SQLite migration 004 create checklist_items and epic_events with the columns, CHECK constraints, FK ON DELETE behaviour, and indexes specified in spec \u00a71322 and \u00a71381.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Body parser round-trip identity holds: serialize(parse(body)) == body for \u22656 fixture bodies including preamble-only, single section, full design-doc template, sub-headings, fenced code containing '##', and a body with non-empty preamble.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "Body parser rejects writes that would leave '# Title' missing or '## Goal' first paragraph empty, with errors body_missing_required_section: title and \u2026: goal respectively.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "create_epic creates an epics row with parser-derived title and goal, seeds 18 default checklist items with status='open' and source='default_seed', and writes one 'created' epic_event sharing a transaction_id.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "edit_epic body section operations leave every non-targeted section byte-identical (verified by parsing prior_state captured in the body_edit event and comparing every other section's serialised form).",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "edit_epic with expected_diff that does not match (after \\n + trailing-whitespace normalisation) refuses to commit, returns the actual diff, and leaves epics.body, title, goal, and checklist_items untouched.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "edit_epic with expected_diff that matches commits normally and writes one event per affected family (body_edit, checklist_change) sharing a single transaction_id.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "revert(epic_id) with no event_id undoes the entire most-recent transaction (body and checklist together) and appends a 'reverted_to' event with a new transaction_id; the resulting body is byte-equal to the pre-edit body.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "get_epic_at_time(epic_id, T) returns body and checklist state equal to what was committed at the most recent event with occurred_at <= T (verified against an explicit replay computed inside the test fixture).",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "get_recent_turns(5) returns the 5 most-recent bot_turns rows (most-recent first) with summaries; search_tool_calls(tool_name='edit_epic', epic_id=X) returns every edit_epic call against epic X with arguments and timestamps.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "After every turn whose tool_calls include create_epic, edit_epic, or revert, exactly one system_logs row exists with category='application', event_type='epic_outline', turn_id=<that turn>, and details containing title plus a sections array with name + line_count for every section in the body.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "10-turn FakeModel-driven integration fixture in tests/test_editorial_loop.py runs end-to-end, exercises all six default sections, exercises both expected_diff match and mismatch paths, and exercises revert; final assertions cover every Sprint 2a acceptance criterion in spec \u00a7131\u2013142.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "All pre-existing tests in tests/ continue to pass (no regression in Sprint 1a/1b functionality).",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "Body parser and section-op modules stay focused: the public surface is parse, serialize, the section ops, validate_required, compute_diff, diffs_equivalent, outline. No tool-layer or Store imports leak into agent_kit/body.py.",
        "priority": "should",
        "requires": [
          "read_files",
          "subjective_judgment"
        ]
      },
      {
        "criterion": "edit_epic rejects requests mixing two body op flavours (e.g. new_content + sections) with a clear error rather than silently picking one.",
        "priority": "should",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "agent_kit/body.py stays under ~400 lines and has no third-party dependencies beyond the standard library (difflib, re).",
        "priority": "should",
        "requires": [
          "read_files"
        ]
      }
    ]
  },
  "preflight_results": {
    "project_dir_exists": true,
    "project_dir_writable": true,
    "success_criteria_present": true,
    "claude_available": true,
    "codex_available": true
  },
  "unresolved_flags": [
    {
      "id": "FLAG-001",
      "concern": "Editorial bootstrap: `create_epic` is planned as a normal tool, but the current loop requires an existing epic before the model can call any tool, so natural-language epic creation has no executable path.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "`agent_kit/loop.py` calls `store.acquire_epic_lock(epic_id)` and `store.create_message(epic_id=epic_id, ...)` before the model/tool loop; `epic_locks.epic_id` and messages reference `epics(id)`, while Sprint 2a acceptance requires creating an epic via natural language.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "FLAG-002",
      "concern": "Body parser/validation: the plan makes `parse()` reject missing `# Title`, conflicting with the spec's parseable `_preamble` fallback and with read/time-travel tools that need to inspect malformed or legacy bodies.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Spec lines 503-514 say no `##` headings means whole body is `_preamble` and write rejection happens if missing title/Goal after a body edit; Phase 2 says `parse()` raises on missing first-line title.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "FLAG-003",
      "concern": "History replay: `reverted_to` events do not store enough prior state to support backward `get_epic_at_time` reconstruction across a revert.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "The plan stores only `{'reverted_transaction_id', 'reverted_event_ids'}` for `reverted_to`, but the same revert mutates body/checklist; backward replay from current state needs the state immediately before that revert to reconstruct timestamps before it.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "issue_hints-1",
      "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked Sprint 2a acceptance in `planning-bot-spec.md` lines 132-142 against the current loop entrypoint in `agent_kit/loop.py`. The plan includes a `create_epic` tool, but it does not address that `run_turn` currently requires an existing `epic_id`, acquires an `epic_locks` row for it before any model/tool call, and creates inbound messages/turns tied to that id; this leaves the acceptance criterion 'Create an epic via natural language' without a concrete bootstrap path when there is no epic yet.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Checked Sprint 2a acceptance in `planning-bot-spec.md` lines 132-142 against the current loop entrypoint in `agent_kit/loop.py`. The plan includes a `create_epic` tool, but it does not address that `run_turn` currently requires an existing `epic_id`, acquires an `epic_locks` row for it before any model/tool call, and creates inbound messages/turns tied to that id; this leaves the acceptance criterion 'Create an epic via natural language' without a concrete bootstrap path when there is no epic yet.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "issue_hints-2",
      "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the spec's additional Sprint 2a title/body sync test at `planning-bot-spec.md` lines 2606-2607. The plan defines `_preamble` as text between the title line and the first `##`, so section replacement of `_preamble` cannot replace `# Title`; that diverges from the spec example `edit_epic(body: { sections: { _preamble: { replace: '# New Title\\n' } } })` and leaves title editing via section addressing underspecified.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Checked the spec's additional Sprint 2a title/body sync test at `planning-bot-spec.md` lines 2606-2607. The plan defines `_preamble` as text between the title line and the first `##`, so section replacement of `_preamble` cannot replace `# Title`; that diverges from the spec example `edit_epic(body: { sections: { _preamble: { replace: '# New Title\\n' } } })` and leaves title editing via section addressing underspecified.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "correctness-1",
      "concern": "Are the proposed changes technically correct?: I checked the body parsing rules in `planning-bot-spec.md` lines 503-514 against Phase 2. The spec separates parsing from write validation: bodies with no `##` headings are parseable as `_preamble`, while writes are rejected if they lack `# Title` or non-empty `## Goal`; the plan instead makes `parse()` raise when the first non-blank line is not `# <title>`, which conflicts with its own round-trip fixtures for preamble-only/no-section bodies and would break read tools on malformed legacy content.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "I checked the body parsing rules in `planning-bot-spec.md` lines 503-514 against Phase 2. The spec separates parsing from write validation: bodies with no `##` headings are parseable as `_preamble`, while writes are rejected if they lack `# Title` or non-empty `## Goal`; the plan instead makes `parse()` raise when the first non-blank line is not `# <title>`, which conflicts with its own round-trip fixtures for preamble-only/no-section bodies and would break read tools on malformed legacy content.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "correctness-2",
      "concern": "Are the proposed changes technically correct?: I checked `get_epic_at_time` and `revert` semantics against the `epic_events.prior_state` contract in `planning-bot-spec.md` lines 1030-1032 and 1381-1399. The plan stores only metadata on `reverted_to` events (`reverted_transaction_id` and ids), then proposes backward replay from current state; a later `reverted_to` event actually mutates body/checklist, but its event does not contain the pre-revert state needed to undo that mutation when reconstructing a timestamp just before the revert, so time travel across reverts will be incorrect.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "I checked `get_epic_at_time` and `revert` semantics against the `epic_events.prior_state` contract in `planning-bot-spec.md` lines 1030-1032 and 1381-1399. The plan stores only metadata on `reverted_to` events (`reverted_transaction_id` and ids), then proposes backward replay from current state; a later `reverted_to` event actually mutates body/checklist, but its event does not contain the pre-revert state needed to undo that mutation when reconstructing a timestamp just before the revert, so time travel across reverts will be incorrect.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "correctness-3",
      "concern": "Are the proposed changes technically correct?: I reviewed the `create_epic` plan against the Data Model requirement in `planning-bot-spec.md` lines 1314-1316. The plan says `create_epic` constructs the body and calls parse/validate, but then passes title and goal columns supplied by the caller into `Store.create_epic`; to satisfy 'the parser is the only writer of epics.title and epics.goal', the tool should explicitly use the parsed title and parsed Goal first paragraph for the insert, not the raw arguments.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "I reviewed the `create_epic` plan against the Data Model requirement in `planning-bot-spec.md` lines 1314-1316. The plan says `create_epic` constructs the body and calls parse/validate, but then passes title and goal columns supplied by the caller into `Store.create_epic`; to satisfy 'the parser is the only writer of epics.title and epics.goal', the tool should explicitly use the parsed title and parsed Goal first paragraph for the insert, not the raw arguments.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "scope-1",
      "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: I searched the current tool system in `agent_kit/tool_kit.py` and existing tools in `agent_kit/tools/communication.py`. The plan follows the existing registry/audit pattern for new tools, but it does not mention marking the new read tools with `operation_kind='read'`; if omitted, `@register_tool` defaults to write, which would pollute audit semantics for `get_epic`, `get_history`, `get_recent_turns`, and `search_tool_calls`.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "I searched the current tool system in `agent_kit/tool_kit.py` and existing tools in `agent_kit/tools/communication.py`. The plan follows the existing registry/audit pattern for new tools, but it does not mention marking the new read tools with `operation_kind='read'`; if omitted, `@register_tool` defaults to write, which would pollute audit semantics for `get_epic`, `get_history`, `get_recent_turns`, and `search_tool_calls`.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "scope-2",
      "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: I checked the spec's tool surface around `edit_epic` in `planning-bot-spec.md` lines 1703-1740. The plan deliberately returns `not_yet_supported` for `changes.sprints` and `changes.state`, which is a scoped Sprint 2a tradeoff because sprints/state gating are later sprint work, but it also omits `changes.meta` handling from the schema discussion even though the spec's change object includes `meta?: { title?, goal? }`; this should be either intentionally rejected or mapped to body edits so callers do not get silent schema drift.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "I checked the spec's tool surface around `edit_epic` in `planning-bot-spec.md` lines 1703-1740. The plan deliberately returns `not_yet_supported` for `changes.sprints` and `changes.state`, which is a scoped Sprint 2a tradeoff because sprints/state gating are later sprint work, but it also omits `changes.meta` handling from the schema discussion even though the spec's change object includes `meta?: { title?, goal? }`; this should be either intentionally rejected or mapped to body edits so callers do not get silent schema drift.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "all_locations",
      "concern": "Does the change touch all locations AND supporting infrastructure?: I checked `agent_kit/store/supabase.py` and `agent_kit/store/sqlite.py` helper patterns. The plan says to add new store methods, but it does not call out adding allowed-column sets or guarded updates for `epics`, `checklist_items`, and `epic_events` in the Supabase adapter analogous to `_MESSAGE_COLUMNS`, `_TURN_COLUMNS`, and `_IMAGE_COLUMNS`; without that supporting adapter glue, update helpers will either be unavailable or bypass the existing column-safety pattern.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "I checked `agent_kit/store/supabase.py` and `agent_kit/store/sqlite.py` helper patterns. The plan says to add new store methods, but it does not call out adding allowed-column sets or guarded updates for `epics`, `checklist_items`, and `epic_events` in the Supabase adapter analogous to `_MESSAGE_COLUMNS`, `_TURN_COLUMNS`, and `_IMAGE_COLUMNS`; without that supporting adapter glue, update helpers will either be unavailable or bypass the existing column-safety pattern.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "callers",
      "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: I inspected `agent_kit/loop.py` and `tests/test_run_turn.py`; current callers of `run_turn` always provide an `epic_id`, and test helpers seed an `epics` row first. The planned `create_epic` tool does not fit this caller contract for a brand-new epic: using a non-existent id would fail the current lock/message foreign-key path, while using an existing placeholder epic would make the create tool semantically odd unless the loop/CLI grows an explicit no-epic or inbox mode.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "I inspected `agent_kit/loop.py` and `tests/test_run_turn.py`; current callers of `run_turn` always provide an `epic_id`, and test helpers seed an `epics` row first. The planned `create_epic` tool does not fit this caller contract for a brand-new epic: using a non-existent id would fail the current lock/message foreign-key path, while using an existing placeholder epic would make the create tool semantically odd unless the loop/CLI grows an explicit no-epic or inbox mode.",
      "raised_in": "critique_v1.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    }
  ],
  "recommendation": "ITERATE",
  "rationale": "This is iteration 1 with 12 open significant flags spanning correctness (parser semantics, revert/time-travel state capture, title/goal derivation), completeness (no executable bootstrap path for create_epic given the loop's epic_id requirement, missing operation_kind='read' on read tools, missing changes.meta handling, missing column-safety patterns in adapters), and spec divergence (title editing via _preamble section addressing). None of these are unresolvable architectural tensions \u2014 they are concrete, actionable critique items the plan writer can address by revising specific phases. No churn pattern (0 reopens), so ITERATE rather than ESCALATE/TIEBREAKER is right. The plan should be revised to: (1) define a bootstrap path for create_epic \u2014 either an inbox/no-epic mode in run_turn or a CLI/store-level pre-creation flow that bypasses the lock requirement; (2) split parsing (lenient \u2014 accept legacy/preamble-only bodies) from validate_required (strict \u2014 applied only to writes); (3) extend reverted_to events with full pre-revert body+checklist snapshot in prior_state so backward replay across reverts is correct; (4) make create_epic insert title/goal derived from parse() output rather than raw args; (5) define how `_preamble` op handles the `# Title` line (or add an explicit title-edit path) per spec \u00a72606; (6) mark all read tools with operation_kind='read'; (7) explicitly handle or reject changes.meta with a clear error; (8) add allowed-column constants for epics/checklist_items/epic_events analogous to _MESSAGE_COLUMNS.",
  "signals_assessment": "Iteration 1, weighted score 16.0 (no trajectory yet), 12 open significant flags, 0 resolved, 0 reopened. Preflight clean (project dir writable, both Claude and Codex available, success criteria present). No recurring critiques and no fuzzy-group churn \u2014 every group is at iteration 1 with addressed_then_reopened_count=0. Escalated debt subsystem is `callable-api` from sprint-1a (attachment-passing) which does not overlap any current flag, so debt does not push toward redesign. Posture: plan-quality issue, not a stuck-loop issue \u2014 revise.",
  "warnings": [
    "FLAG-001 (bootstrap) is the highest-leverage correction \u2014 without it the create_epic acceptance criterion has no executable path; the revised plan must concretely show how a turn runs before any epic exists.",
    "FLAG-002 and FLAG-003 are correctness flags that affect the integration test's ability to pass; the parser split (parse vs validate_required) and reverted_to prior_state schema must be settled before execution.",
    "issue_hints-2 (title via _preamble) needs an explicit decision: either redefine _preamble to include the title line, or add a dedicated title-edit op \u2014 pick one and make it consistent across get_epic / replace_section / serialize."
  ],
  "settled_decisions": [
    {
      "id": "SD-001",
      "decision": "Sprint 2a is invocation-mode only; no resident-mode behavior changes required.",
      "rationale": "Confirmed in plan assumptions and consistent with Sprint 1b boundary; not in dispute."
    },
    {
      "id": "SD-002",
      "decision": "changes.sprints and changes.state return not_yet_supported in Sprint 2a; full handling is Sprint 4.",
      "rationale": "Explicit scope boundary documented in plan; sprint/state gating belongs to Sprint 4."
    },
    {
      "id": "SD-003",
      "decision": "Default checklist seed is unconditional (all 18 items) in v1; adaptation logic lives in the bot's system prompt, not server-side.",
      "rationale": "Spec acceptance criterion only requires seeding 18; adaptation is a bot-side concern that does not gate Sprint 2a."
    },
    {
      "id": "SD-004",
      "decision": "render_epic supports format='markdown' only; 'html' returns not_yet_supported; image-reference resolution is a Sprint 6 no-op.",
      "rationale": "Scoped per plan assumption and aligned with later-sprint ownership of HTML rendering and images."
    },
    {
      "id": "SD-005",
      "decision": "expected_diff comparison normalises line endings to \\n, strips trailing whitespace per line, and drops trailing blank lines before equality.",
      "rationale": "Matches spec \u00a7494 normalisation rules; agreed in plan assumptions."
    },
    {
      "id": "SD-006",
      "decision": "epic_outline log fires only on turns whose tool_calls touched create_epic, edit_epic, or revert; pure-read turns and failed turns do not emit it.",
      "rationale": "Matches spec wording 'turn that touched an epic' and avoids polluting logs on read-only turns."
    },
    {
      "id": "SD-007",
      "decision": "Single-writer concurrency via existing epic_locks + store.transaction is sufficient for Sprint 2a; no additional locking added.",
      "rationale": "Matches Sprint 1b posture; no concurrent invocation-mode requirement in Sprint 2a acceptance."
    }
  ],
  "override_forced": false,
  "orchestrator_guidance": "First iteration; follow gate recommendation: ITERATE. Verify unresolved flags against the plan and project code before accepting.",
  "robustness": "standard",
  "signals": {
    "iteration": 1,
    "idea": "# Sprint 2a \u2014 Editorial core\n\nBot maintains an epic body and checklist for one epic, with section-level body editing. Minimum to have an editorial conversation.\n\n**Full spec is at `planning-bot-spec.md` in this repo root. Refer to it for complete details on Body Structure and Editing, Body Templates, The Checklist as Guide, and Data Model sections.**\n\n## Supabase\n- URL: https://yhwflvadmefhkshwbfnf.supabase.co\n- Service key: [REDACTED_SUPABASE_SERVICE_ROLE_JWT]\n\n## Scope\n\n- Tables: checklist_items, epic_events (with transaction_id)\n- Body parser/serializer \u2014 markdown \u2194 structured sections with ## heading delimiters; enforces heading hierarchy (# for title only, ## for sections, ### for sub-headings)\n- Turn-end epic outline emitted to system_logs at info level\n- Default body template (design doc) \u2014 Goal, Principles, Context, Key Decisions, Open Questions, Deliverable\n- `edit_epic` tool \u2014 body (whole + section ops) + checklist; supports:\n  - Write whole body\n  - Write specific sections\n  - Append to a section\n  - Add new section with position\n  - Rename/remove sections\n  - `expected_diff` parameter for server-enforced diff verification (unified diff format)\n- `create_epic`, `revert` (transaction-grouped), `render_epic` tools\n- Read tools: `get_epic` (with section addressing), `get_section_names`, `get_history`, `get_self_understanding`\n- History tools: `get_epic_at_time`, `get_recent_turns`, `search_tool_calls`\n- Default checklist seed \u2014 18 items with adaptation logic\n- Title and goal are derived columns from body parsing (# Title and ## Goal first paragraph)\n\n## Key Data Model\n\n### checklist_items\nid, epic_id, content, status (open|done|skipped|superseded), position, source (bot_inferred|user_requested|carried_over|default_seed|second_opinion), skip_reason, superseded_by_item_id, created_at, completed_at\n\n### epic_events\nid, epic_id, transaction_id (uuid), event_type, summary, prior_state (json), turn_id, occurred_at\nEvent types: body_edit, checklist_change, sprints_change, state_change, forced_handoff, created, code_referenced, codebase_added, image_generated, second_opinion_requested, reverted_to, sprint_status_change\n\n## Body Parser Rules\n- Section boundaries are ## headings (level-2 markdown)\n- Section names are case-sensitive\n- Pre-section content is \"_preamble\"\n- Sub-sections (### and below) are part of parent section\n- No ## headings \u2192 whole body is _preamble\n- # Title and ## Goal are required structural elements; missing \u2192 write rejected\n- Code blocks containing ## are NOT section boundaries\n\n## Acceptance Criteria\n\n- Create an epic via natural language \u2192 epics row created, default checklist seeded with 18 items, body initialized\n- 10-turn scripted conversation (mocked Anthropic) produces body with all 6 default sections\n- Section-level edit \u2192 only that section changes; other sections byte-identical\n- Whole body edit \u2192 diff captured in event; revert restores prior version exactly\n- \"revert that\" \u2192 most recent transaction undone, new reverted_to event logged\n- expected_diff mismatch \u2192 server refuses write, returns actual diff\n- expected_diff match \u2192 server commits normally\n- get_epic_at_time(epic_id, T) \u2192 returns body/checklist state as of time T\n- get_recent_turns(5) \u2192 returns 5 most recent turns with summaries\n- search_tool_calls(tool_name='edit_epic', epic_id=X) \u2192 returns matching calls\n- Turn-end system_logs row with event_type='epic_outline' containing title + section list + line counts\n\n## Tests\n- Unit: body parser (markdown \u2192 sections \u2192 markdown roundtrip is identity); section operations; edit_epic validation; transaction_id grouping; expected_diff comparison; epic-at-time replay\n- Integration: 10-turn fixture conversation against local Supabase with mocked Anthropic; revert end-to-end",
    "significant_flags": 12,
    "unresolved_flags": [
      {
        "id": "FLAG-001",
        "concern": "Editorial bootstrap: `create_epic` is planned as a normal tool, but the current loop requires an existing epic before the model can call any tool, so natural-language epic creation has no executable path.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "FLAG-002",
        "concern": "Body parser/validation: the plan makes `parse()` reject missing `# Title`, conflicting with the spec's parseable `_preamble` fallback and with read/time-travel tools that need to inspect malformed or legacy bodies.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "FLAG-003",
        "concern": "History replay: `reverted_to` events do not store enough prior state to support backward `get_epic_at_time` reconstruction across a revert.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "issue_hints-1",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked Sprint 2a acceptance in `planning-bot-spec.md` lines 132-142 against the current loop entrypoint in `agent_kit/loop.py`. The plan includes a `create_epic` tool, but it does not address that `run_turn` currently requires an existing `epic_id`, acquires an `epic_locks` row for it before any model/tool call, and creates inbound messages/turns tied to that id; this leaves the acceptance criterion 'Create an epic via natural language' without a concrete bootstrap path when there is no epic yet.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "issue_hints-2",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the spec's additional Sprint 2a title/body sync test at `planning-bot-spec.md` lines 2606-2607. The plan defines `_preamble` as text between the title line and the first `##`, so section replacement of `_preamble` cannot replace `# Title`; that diverges from the spec example `edit_epic(body: { sections: { _preamble: { replace: '# New Title\\n' } } })` and leaves title editing via section addressing underspecified.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "correctness-1",
        "concern": "Are the proposed changes technically correct?: I checked the body parsing rules in `planning-bot-spec.md` lines 503-514 against Phase 2. The spec separates parsing from write validation: bodies with no `##` headings are parseable as `_preamble`, while writes are rejected if they lack `# Title` or non-empty `## Goal`; the plan instead makes `parse()` raise when the first non-blank line is not `# <title>`, which conflicts with its own round-trip fixtures for preamble-only/no-section bodies and would break read tools on malformed legacy content.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "correctness-2",
        "concern": "Are the proposed changes technically correct?: I checked `get_epic_at_time` and `revert` semantics against the `epic_events.prior_state` contract in `planning-bot-spec.md` lines 1030-1032 and 1381-1399. The plan stores only metadata on `reverted_to` events (`reverted_transaction_id` and ids), then proposes backward replay from current state; a later `reverted_to` event actually mutates body/checklist, but its event does not contain the pre-revert state needed to undo that mutation when reconstructing a timestamp just before the revert, so time travel across reverts will be incorrect.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "correctness-3",
        "concern": "Are the proposed changes technically correct?: I reviewed the `create_epic` plan against the Data Model requirement in `planning-bot-spec.md` lines 1314-1316. The plan says `create_epic` constructs the body and calls parse/validate, but then passes title and goal columns supplied by the caller into `Store.create_epic`; to satisfy 'the parser is the only writer of epics.title and epics.goal', the tool should explicitly use the parsed title and parsed Goal first paragraph for the insert, not the raw arguments.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "scope-1",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: I searched the current tool system in `agent_kit/tool_kit.py` and existing tools in `agent_kit/tools/communication.py`. The plan follows the existing registry/audit pattern for new tools, but it does not mention marking the new read tools with `operation_kind='read'`; if omitted, `@register_tool` defaults to write, which would pollute audit semantics for `get_epic`, `get_history`, `get_recent_turns`, and `search_tool_calls`.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "scope-2",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: I checked the spec's tool surface around `edit_epic` in `planning-bot-spec.md` lines 1703-1740. The plan deliberately returns `not_yet_supported` for `changes.sprints` and `changes.state`, which is a scoped Sprint 2a tradeoff because sprints/state gating are later sprint work, but it also omits `changes.meta` handling from the schema discussion even though the spec's change object includes `meta?: { title?, goal? }`; this should be either intentionally rejected or mapped to body edits so callers do not get silent schema drift.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "all_locations",
        "concern": "Does the change touch all locations AND supporting infrastructure?: I checked `agent_kit/store/supabase.py` and `agent_kit/store/sqlite.py` helper patterns. The plan says to add new store methods, but it does not call out adding allowed-column sets or guarded updates for `epics`, `checklist_items`, and `epic_events` in the Supabase adapter analogous to `_MESSAGE_COLUMNS`, `_TURN_COLUMNS`, and `_IMAGE_COLUMNS`; without that supporting adapter glue, update helpers will either be unavailable or bypass the existing column-safety pattern.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "callers",
        "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: I inspected `agent_kit/loop.py` and `tests/test_run_turn.py`; current callers of `run_turn` always provide an `epic_id`, and test helpers seed an `epics` row first. The planned `create_epic` tool does not fit this caller contract for a brand-new epic: using a non-existent id would fail the current lock/message foreign-key path, while using an existing placeholder epic would make the create tool semantically odd unless the loop/CLI grows an explicit no-epic or inbox mode.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      }
    ],
    "resolved_flags": [],
    "weighted_score": 16.0,
    "weighted_history": [],
    "plan_delta_from_previous": null,
    "recurring_critiques": [],
    "scope_creep_flags": [],
    "loop_summary": "Iteration 1. Weighted score trajectory: 16.0. Plan deltas: n/a. Recurring critiques: 0. Resolved flags: 0. Open significant flags: 12.",
    "debt_overlaps": [],
    "escalated_debt_subsystems": []
  },
  "flag_resolutions": [],
  "resolved_flag_ids": [],
  "resolution_summary": "",
  "reprompted": false
}

        Open significant flags:
        [
  {
    "id": "FLAG-001",
    "severity": "significant",
    "status": "open",
    "concern": "Editorial bootstrap: `create_epic` is planned as a normal tool, but the current loop requires an existing epic before the model can call any tool, so natural-language epic creation has no executable path.",
    "evidence": "`agent_kit/loop.py` calls `store.acquire_epic_lock(epic_id)` and `store.create_message(epic_id=epic_id, ...)` before the model/tool loop; `epic_locks.epic_id` and messages reference `epics(id)`, while Sprint 2a acceptance requires creating an epic via natural language."
  },
  {
    "id": "FLAG-002",
    "severity": "significant",
    "status": "open",
    "concern": "Body parser/validation: the plan makes `parse()` reject missing `# Title`, conflicting with the spec's parseable `_preamble` fallback and with read/time-travel tools that need to inspect malformed or legacy bodies.",
    "evidence": "Spec lines 503-514 say no `##` headings means whole body is `_preamble` and write rejection happens if missing title/Goal after a body edit; Phase 2 says `parse()` raises on missing first-line title."
  },
  {
    "id": "FLAG-003",
    "severity": "significant",
    "status": "open",
    "concern": "History replay: `reverted_to` events do not store enough prior state to support backward `get_epic_at_time` reconstruction across a revert.",
    "evidence": "The plan stores only `{'reverted_transaction_id', 'reverted_event_ids'}` for `reverted_to`, but the same revert mutates body/checklist; backward replay from current state needs the state immediately before that revert to reconstruct timestamps before it."
  },
  {
    "id": "issue_hints-1",
    "severity": "significant",
    "status": "open",
    "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked Sprint 2a acceptance in `planning-bot-spec.md` lines 132-142 against the current loop entrypoint in `agent_kit/loop.py`. The plan includes a `create_epic` tool, but it does not address that `run_turn` currently requires an existing `epic_id`, acquires an `epic_locks` row for it before any model/tool call, and creates inbound messages/turns tied to that id; this leaves the acceptance criterion 'Create an epic via natural language' without a concrete bootstrap path when there is no epic yet.",
    "evidence": "Checked Sprint 2a acceptance in `planning-bot-spec.md` lines 132-142 against the current loop entrypoint in `agent_kit/loop.py`. The plan includes a `create_epic` tool, but it does not address that `run_turn` currently requires an existing `epic_id`, acquires an `epic_locks` row for it before any model/tool call, and creates inbound messages/turns tied to that id; this leaves the acceptance criterion 'Create an epic via natural language' without a concrete bootstrap path when there is no epic yet."
  },
  {
    "id": "issue_hints-2",
    "severity": "significant",
    "status": "open",
    "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the spec's additional Sprint 2a title/body sync test at `planning-bot-spec.md` lines 2606-2607. The plan defines `_preamble` as text between the title line and the first `##`, so section replacement of `_preamble` cannot replace `# Title`; that diverges from the spec example `edit_epic(body: { sections: { _preamble: { replace: '# New Title\\n' } } })` and leaves title editing via section addressing underspecified.",
    "evidence": "Checked the spec's additional Sprint 2a title/body sync test at `planning-bot-spec.md` lines 2606-2607. The plan defines `_preamble` as text between the title line and the first `##`, so section replacement of `_preamble` cannot replace `# Title`; that diverges from the spec example `edit_epic(body: { sections: { _preamble: { replace: '# New Title\\n' } } })` and leaves title editing via section addressing underspecified."
  },
  {
    "id": "correctness-1",
    "severity": "significant",
    "status": "open",
    "concern": "Are the proposed changes technically correct?: I checked the body parsing rules in `planning-bot-spec.md` lines 503-514 against Phase 2. The spec separates parsing from write validation: bodies with no `##` headings are parseable as `_preamble`, while writes are rejected if they lack `# Title` or non-empty `## Goal`; the plan instead makes `parse()` raise when the first non-blank line is not `# <title>`, which conflicts with its own round-trip fixtures for preamble-only/no-section bodies and would break read tools on malformed legacy content.",
    "evidence": "I checked the body parsing rules in `planning-bot-spec.md` lines 503-514 against Phase 2. The spec separates parsing from write validation: bodies with no `##` headings are parseable as `_preamble`, while writes are rejected if they lack `# Title` or non-empty `## Goal`; the plan instead makes `parse()` raise when the first non-blank line is not `# <title>`, which conflicts with its own round-trip fixtures for preamble-only/no-section bodies and would break read tools on malformed legacy content."
  },
  {
    "id": "correctness-2",
    "severity": "significant",
    "status": "open",
    "concern": "Are the proposed changes technically correct?: I checked `get_epic_at_time` and `revert` semantics against the `epic_events.prior_state` contract in `planning-bot-spec.md` lines 1030-1032 and 1381-1399. The plan stores only metadata on `reverted_to` events (`reverted_transaction_id` and ids), then proposes backward replay from current state; a later `reverted_to` event actually mutates body/checklist, but its event does not contain the pre-revert state needed to undo that mutation when reconstructing a timestamp just before the revert, so time travel across reverts will be incorrect.",
    "evidence": "I checked `get_epic_at_time` and `revert` semantics against the `epic_events.prior_state` contract in `planning-bot-spec.md` lines 1030-1032 and 1381-1399. The plan stores only metadata on `reverted_to` events (`reverted_transaction_id` and ids), then proposes backward replay from current state; a later `reverted_to` event actually mutates body/checklist, but its event does not contain the pre-revert state needed to undo that mutation when reconstructing a timestamp just before the revert, so time travel across reverts will be incorrect."
  },
  {
    "id": "correctness-3",
    "severity": "significant",
    "status": "open",
    "concern": "Are the proposed changes technically correct?: I reviewed the `create_epic` plan against the Data Model requirement in `planning-bot-spec.md` lines 1314-1316. The plan says `create_epic` constructs the body and calls parse/validate, but then passes title and goal columns supplied by the caller into `Store.create_epic`; to satisfy 'the parser is the only writer of epics.title and epics.goal', the tool should explicitly use the parsed title and parsed Goal first paragraph for the insert, not the raw arguments.",
    "evidence": "I reviewed the `create_epic` plan against the Data Model requirement in `planning-bot-spec.md` lines 1314-1316. The plan says `create_epic` constructs the body and calls parse/validate, but then passes title and goal columns supplied by the caller into `Store.create_epic`; to satisfy 'the parser is the only writer of epics.title and epics.goal', the tool should explicitly use the parsed title and parsed Goal first paragraph for the insert, not the raw arguments."
  },
  {
    "id": "scope-1",
    "severity": "significant",
    "status": "open",
    "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: I searched the current tool system in `agent_kit/tool_kit.py` and existing tools in `agent_kit/tools/communication.py`. The plan follows the existing registry/audit pattern for new tools, but it does not mention marking the new read tools with `operation_kind='read'`; if omitted, `@register_tool` defaults to write, which would pollute audit semantics for `get_epic`, `get_history`, `get_recent_turns`, and `search_tool_calls`.",
    "evidence": "I searched the current tool system in `agent_kit/tool_kit.py` and existing tools in `agent_kit/tools/communication.py`. The plan follows the existing registry/audit pattern for new tools, but it does not mention marking the new read tools with `operation_kind='read'`; if omitted, `@register_tool` defaults to write, which would pollute audit semantics for `get_epic`, `get_history`, `get_recent_turns`, and `search_tool_calls`."
  },
  {
    "id": "scope-2",
    "severity": "significant",
    "status": "open",
    "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: I checked the spec's tool surface around `edit_epic` in `planning-bot-spec.md` lines 1703-1740. The plan deliberately returns `not_yet_supported` for `changes.sprints` and `changes.state`, which is a scoped Sprint 2a tradeoff because sprints/state gating are later sprint work, but it also omits `changes.meta` handling from the schema discussion even though the spec's change object includes `meta?: { title?, goal? }`; this should be either intentionally rejected or mapped to body edits so callers do not get silent schema drift.",
    "evidence": "I checked the spec's tool surface around `edit_epic` in `planning-bot-spec.md` lines 1703-1740. The plan deliberately returns `not_yet_supported` for `changes.sprints` and `changes.state`, which is a scoped Sprint 2a tradeoff because sprints/state gating are later sprint work, but it also omits `changes.meta` handling from the schema discussion even though the spec's change object includes `meta?: { title?, goal? }`; this should be either intentionally rejected or mapped to body edits so callers do not get silent schema drift."
  },
  {
    "id": "all_locations",
    "severity": "significant",
    "status": "open",
    "concern": "Does the change touch all locations AND supporting infrastructure?: I checked `agent_kit/store/supabase.py` and `agent_kit/store/sqlite.py` helper patterns. The plan says to add new store methods, but it does not call out adding allowed-column sets or guarded updates for `epics`, `checklist_items`, and `epic_events` in the Supabase adapter analogous to `_MESSAGE_COLUMNS`, `_TURN_COLUMNS`, and `_IMAGE_COLUMNS`; without that supporting adapter glue, update helpers will either be unavailable or bypass the existing column-safety pattern.",
    "evidence": "I checked `agent_kit/store/supabase.py` and `agent_kit/store/sqlite.py` helper patterns. The plan says to add new store methods, but it does not call out adding allowed-column sets or guarded updates for `epics`, `checklist_items`, and `epic_events` in the Supabase adapter analogous to `_MESSAGE_COLUMNS`, `_TURN_COLUMNS`, and `_IMAGE_COLUMNS`; without that supporting adapter glue, update helpers will either be unavailable or bypass the existing column-safety pattern."
  },
  {
    "id": "callers",
    "severity": "significant",
    "status": "open",
    "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: I inspected `agent_kit/loop.py` and `tests/test_run_turn.py`; current callers of `run_turn` always provide an `epic_id`, and test helpers seed an `epics` row first. The planned `create_epic` tool does not fit this caller contract for a brand-new epic: using a non-existent id would fail the current lock/message foreign-key path, while using an existing placeholder epic would make the create tool semantically odd unless the loop/CLI grows an explicit no-epic or inbox mode.",
    "evidence": "I inspected `agent_kit/loop.py` and `tests/test_run_turn.py`; current callers of `run_turn` always provide an `epic_id`, and test helpers seed an `epics` row first. The planned `create_epic` tool does not fit this caller contract for a brand-new epic: using a non-existent id would fail the current lock/message foreign-key path, while using an existing placeholder epic would make the create tool semantically odd unless the loop/CLI grows an explicit no-epic or inbox mode."
  }
]



        Requirements:
        - Before addressing individual flags, check: does any flag suggest the plan is targeting the wrong code or the wrong root cause? If so, consider whether the plan needs a new approach rather than adjustments. Explain your reasoning.
        - Update the plan to address the significant issues.
        - Keep the plan readable and executable.
        - Return flags_addressed with the exact flag IDs you addressed.
        - Include `changes_summary` as a short plain-English summary of what changed in the revision. If there were no concrete flags, say that explicitly (for example: `No critique flags were raised; refined wording and kept the plan aligned for execution.`).
        - Preserve or improve success criteria quality. Each criterion must have a `priority` of `must`, `should`, or `info`. Promote or demote priorities if critique feedback reveals a criterion was over- or under-weighted.
        - Verify that the plan remains aligned with the user's original intent, not just internal plan quality.
        - Remove unjustified scope growth. If critique raised scope creep, narrow the plan back to the original idea unless the broader work is strictly required.
        - Maintain the structural template: H1 title, ## Overview, phase sections with numbered step sections, ## Execution Order or ## Validation Order.
        - CRITICAL: Your entire revised plan markdown (all sections) must be output as the `plan` field in the structured output. The prose response must not contain the plan text.
        - CRITICAL: Return only the structured JSON object for the schema fields `plan`, `changes_summary`, `flags_addressed`, `assumptions`, `success_criteria`, and `questions`. Do not add commentary before or after the JSON object.

        Plan template — simple format (adapt to the actual repo and scope):
````md
# Implementation Plan: [Title]

## Overview
Summarize the goal, current repository shape, and the constraints that matter.

## Main Phase

### Step 1: Audit the current behavior (`megaplan/prompts.py`)
**Scope:** Small
1. **Inspect** the current implementation and call out the exact insertion points (`megaplan/prompts.py:29`).

### Step 2: Add the first change (`megaplan/evaluation.py`)
**Scope:** Medium
1. **Implement** the smallest viable change with exact file references (`megaplan/evaluation.py:1`).
2. **Capture** any tricky behavior with a short example.
   ```python
   issues = validate_plan_structure(plan_text)
   ```

### Step 3: Wire downstream behavior (`megaplan/handlers.py`, `megaplan/workers.py`)
**Scope:** Medium
1. **Update** the runtime flow in the touched files (`megaplan/handlers.py:400`, `megaplan/workers.py:199`).

### Step 4: Prove the change (`tests/test_evaluation.py`, `tests/test_megaplan.py`)
**Scope:** Small
1. **Run** the cheapest targeted checks first (`tests/test_evaluation.py:1`).
2. **Finish** with broader verification once the wiring is in place (`tests/test_megaplan.py:1`).

## Execution Order
1. Update prompts and mocks before enforcing stricter validation.
2. Land higher-risk wiring after the validator and tests are ready.

## Validation Order
1. Start with focused unit tests.
2. Run the broader suite after the flow changes are in place.
````

For complex plans, use multiple phases:
````md
## Phase 1: Foundation — Dependencies, DB, Types

### Step 1: Install dependencies (`package.json`)
...

### Step 2: Create database migration (`supabase/migrations/`)
...

## Phase 2: Core Integration

### Step 3: Port the main component (`src/components/`)
...
````

Template guidance:
- Simple plans: use `## Main Phase` with `### Step N:` sections underneath.
- Complex plans: use multiple `## Phase N:` sections, each containing `### Step N:` steps. Step numbers are global (not per-phase).
- The flat `## Step N:` format (without phases) also works for backwards compatibility.
- Key invariants: one H1 title, one `## Overview`, numbered step sections (`### Step N:` or `## Step N:`), and at least one ordering section.

> AGENT

I'll quickly verify the spec line referenced for the `_preamble`/title-edit semantics so the revision pins it correctly.

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/planning-bot-spec.md",
  "offset": 2596,
  "limit": 25
}
```

> TOOL

tool_result Read
```
2596	**4. Mid-turn pre-write check (Sprint 2a).**
2597	Start a turn that's about to call `edit_epic`. Inject a user message "wait don't do that" before the write fires. Verify the bot detects the mid-turn message at the end-of-turn check and abandons the write — no `edit_epic` row in `tool_calls` from that turn. LLM-graded against the bot's response (should acknowledge the wait and ask for clarification).
2598	
2599	**5. External send crash (Sprint 1b).**
2600	Mock Discord such that `send_message` succeeds at the API level (returns a message_id) but the post-confirmation DB write to `external_requests.confirmed` fails (simulate crash). Verify reconciliation: on next recovery scan, the bot detects the orphaned `pending` row, queries Discord for messages from itself in the user's channel matching the request_summary, finds the message, marks `confirmed`, and does NOT re-send. End state: exactly one user-visible message.
2601	
2602	**6. Image historical render (Sprint 6).**
2603	Generate `img_data_flow` for an epic. Capture timestamp T1. Edit the body to reference it. Capture timestamp T2. Regenerate `img_data_flow` (new bytes, same reference_key, old version deactivated). Capture T3. Call `get_epic_at_time(epic_id, T2)`. Verify the rendered body resolves the reference to the *T1-era* image bytes (the `active` row at T2), not the current active row. Image historical fidelity through the active-flag history.
2604	
2605	**7. Title/body sync (Sprint 2a).**
2606	- `edit_epic(body: { sections: { _preamble: { replace: '# New Title\n' } } })` → verify `epics.title` updates to "New Title" in the same transaction, `body_version` increments, audit shows the change.
2607	- Body edit that removes the `# Title` line entirely → `edit_epic` rejects with `body_missing_required_section: title`.
2608	- Verifies title is recomputed from body on every parse, so any drift is self-correcting on next edit.
2609	
2610	**8. Goal/body sync (Sprint 2a).**
2611	- Edit `## Goal` first paragraph → verify `epics.goal` updates, `body_version` increments, audit captures.
2612	- Edit `## Goal` to empty content → write rejected with `body_missing_required_section: goal`.
2613	- Edit `## Goal` to multi-paragraph content — only first paragraph extracted to column, rest stays in body.
2614	
2615	**9. Feedback staleness — passive load doesn't refresh (Sprint 2b).**
2616	Create a `priority='always'` feedback item with `last_applied_at` 95 days ago and `last_referenced_at` recent (loaded into hot context multiple times but never applied). Verify it's flagged as "possibly stale" in next turn's hot context. Confirms staleness is keyed off `last_applied_at`, not `last_referenced_at` — passive loading does NOT keep feedback fresh.
2617	
2618	**10. Status throttling (Sprint 1b).**
2619	Mock a turn that fires 20 tool calls within 2 seconds. Verify the status message is edited at most ~2-3 times in that window (1-second debounce + final edit), not 20 times. No Discord rate-limit error logged. Final status reflects the latest state.
2620
```

> AGENT

The flags are concrete plan-level adjustments — none indicate the plan is targeting the wrong code or root cause. The bootstrap (FLAG-001), parser split (FLAG-002), `reverted_to` snapshot (FLAG-003), `_preamble` title coverage (issue_hints-2), parser-as-only-writer (correctness-3), `operation_kind='read'` (scope-1), `changes.meta` handling (scope-2), and adapter column-safety (all_locations) are all surgical fixes inside the existing six-phase structure. I keep the structure and revise the affected steps.

> TOOL

tool_use StructuredOutput
```json
{
  "plan": "# Implementation Plan: Sprint 2a — Editorial Core (rev 2)\n\n## Overview\n\nSprint 2a gives Arnold a *document* to edit. Today the codebase has an `epics` table (`supabase/migrations/202604300001_001_core.sql`), a turn loop (`agent_kit/loop.py`) that requires `epic_id` to acquire `epic_locks` before any model call, a `Store` protocol (`agent_kit/ports.py`) backed by SQLite + Postgres adapters, and a `system_logs` sink. The only registered tools are `send_message`, `set_activity`, `defer_to_caller`, `view_image`, `send_image`, `update_image_metadata`.\n\nThis sprint adds (1) two new tables (`checklist_items`, `epic_events`); (2) a body parser/serializer with section addressing; (3) Store CRUD for epics/checklist/events; (4) ~10 new tools (`create_epic`, `edit_epic`, `revert`, `render_epic`, plus reads); (5) a no-epic turn-mode so `create_epic` is callable from a fresh state; (6) a turn-end `epic_outline` log.\n\nConstraints worth pinning up front (now reflecting critique fixes):\n\n- **Bootstrap path:** `run_turn(epic_id=None)` is now a first-class mode. Lock acquisition is skipped; the inbound message and the `bot_turns` row are created with `epic_id=NULL` (both columns are already nullable per `supabase/migrations/202604300001_001_core.sql:22, :50`). When `create_epic` fires, it stamps `context.metadata['epic_id']`, then UPDATEs the inbound message and the turn to point at the new epic. (FLAG-001, issue_hints-1, callers.)\n- **Parser split:** `parse(body)` is **lenient** — it accepts any input, including bodies missing `# Title`, bodies with no `##` headings (whole body is `_preamble`), and legacy/malformed content. Only **`validate_for_write(parsed)`** is strict and is called only by write paths. (FLAG-002, correctness-1.)\n- **`_preamble` includes the `# Title` line** per spec §2606. The preamble is the raw text from the start of the body up to (but not including) the first `##` line. Replacing `_preamble` with `'# New Title\\n'` therefore updates the title; removing the `# Title` line via a preamble write is rejected by `validate_for_write` with `body_missing_required_section: title`. (issue_hints-2.)\n- **Title/goal columns are parser-derived only.** `create_epic` and `edit_epic` write `epics.title` and `epics.goal` exclusively from `parsed.title` and `parsed.goal_first_paragraph`. Raw `title`/`goal` arguments are template inputs only. (correctness-3.)\n- **`reverted_to` events store full pre-revert state.** `prior_state = {'body': pre_revert_body, 'checklist': [...], 'reverted_transaction_id': txn, 'reverted_event_ids': [...]}` so backward replay across reverts is correct. (FLAG-003, correctness-2.)\n- **Read tools register with `operation_kind='read'`.** Write tools default `operation_kind='write'`. (scope-1.)\n- **`edit_epic.changes.meta` is rejected** with `meta_not_supported`: title/goal are derived columns; bot must edit `body.sections._preamble` (for title) or `body.sections.Goal` (for goal). (scope-2.)\n- **Mutually exclusive body ops.** `new_content`, `sections`, `append`, `remove_sections`, `rename_section`, and `reorder` are mutually exclusive in a single `edit_epic.body`; mixing returns `body_op_conflict`.\n- **`expected_diff` equivalence:** `\\n` line endings, strip trailing whitespace per line, drop trailing blank lines (spec §494).\n- **Out of scope:** sprints, sprint_items, codebases, code_artifacts, feedback, second_opinions, image generation. `edit_epic.changes.sprints` and `changes.state` return `not_yet_supported`.\n- CLAUDE.md forbids creating a `megaplan/` directory; the existing one is harness state, not a target.\n\nSix phases. Phases 1–3 land schema, parser, and store surface. Phase 4 lands tools. Phase 5 wires the loop bootstrap and outline log. Phase 6 covers the integration fixture.\n\n---\n\n## Phase 1: Schema — checklist_items, epic_events\n\n### Step 1: Postgres migration (`supabase/migrations/202604300004_004_editorial_core.sql`)\n**Scope:** Small\n1. **Create** `checklist_items` matching spec §1322 exactly: `id TEXT PK`, `epic_id TEXT NOT NULL REFERENCES epics(id) ON DELETE CASCADE`, `content TEXT NOT NULL`, `status TEXT CHECK IN ('open','done','skipped','superseded')`, `position INTEGER NOT NULL`, `source TEXT CHECK IN ('bot_inferred','user_requested','carried_over','default_seed','second_opinion')`, `skip_reason TEXT`, `superseded_by_item_id TEXT REFERENCES checklist_items(id)`, `created_at TIMESTAMPTZ DEFAULT now()`, `completed_at TIMESTAMPTZ`. Index `(epic_id, status, position)`.\n2. **Create** `epic_events` matching spec §1381 exactly: `id TEXT PK`, `epic_id TEXT NOT NULL REFERENCES epics(id) ON DELETE CASCADE`, `transaction_id TEXT NOT NULL`, `event_type TEXT CHECK IN ('body_edit','checklist_change','sprints_change','state_change','forced_handoff','created','code_referenced','codebase_added','image_generated','second_opinion_requested','reverted_to','sprint_status_change')`, `summary TEXT NOT NULL`, `prior_state JSONB`, `turn_id TEXT REFERENCES bot_turns(id) ON DELETE SET NULL`, `occurred_at TIMESTAMPTZ DEFAULT now()`. Indexes `(epic_id, occurred_at DESC)` and `(transaction_id)`.\n\n### Step 2: SQLite mirror (`agent_kit/store/migrations/sqlite/004_editorial_core.sql`)\n**Scope:** Small\n1. **Mirror** the Postgres migration in SQLite (TEXT for everything; `prior_state` is a TEXT JSON blob, consistent with how `prompt_snapshot` etc. are handled in `001_core.sql`).\n2. **Register** `prior_state` in the JSON-encoding sets at `agent_kit/store/sqlite.py:17` and `agent_kit/store/supabase.py:12`.\n\n### Step 3: Update Supabase truncate fixture (`tests/test_supabase_store.py:33`)\n**Scope:** Small\n1. **Add** `checklist_items` and `epic_events` to the `TRUNCATE TABLE … RESTART IDENTITY CASCADE` block.\n\n---\n\n## Phase 2: Body parser/serializer\n\n### Step 4: Parser module — lenient parse, strict validate (`agent_kit/body.py`)\n**Scope:** Medium\n1. **Public surface** (everything else `_private`):\n   - `parse(body: str) -> ParsedBody` — **lenient**. Never raises. `ParsedBody`: `title: str | None`, `goal_first_paragraph: str | None`, `preamble: str` (raw text from byte 0 up to but not including the first `##` line; INCLUDES the `# Title` line and any blank/text lines after it), `sections: list[Section]` in order. `Section`: `name: str`, `content: str`, `subheadings: list[str]`, `line_count: int`. Title is extracted by scanning the preamble for the first non-blank line matching `^#\\s+(.+?)\\s*$`; if absent or empty, `title` is `None`. Goal is extracted by finding a section named exactly `Goal`, taking everything before the first blank line in its content (whitespace-stripped); if section absent or empty, `goal_first_paragraph` is `None`. Bodies with no `##` headings parse cleanly to `sections=[]` and `preamble=<entire body>`.\n   - `serialize(parsed: ParsedBody) -> str` — round-trip identity for any output of `parse`. Emits `preamble` verbatim, then each `## Name\\n<content>` in order.\n   - `validate_for_write(parsed: ParsedBody) -> None` — **strict**, raises `BodyValidationError(\"body_missing_required_section: title\")` if `parsed.title is None or empty`, `…goal` if `parsed.goal_first_paragraph is None or empty`. Called by every write path before `update_epic_body`.\n   - `outline(parsed: ParsedBody) -> dict` — `{title, sections: [{name, line_count, subheadings}], total_lines}` for the outline log.\n2. **Heading rules** (spec §503–514):\n   - Section delimiters match `^##\\s+(.+?)\\s*$` at top level only. Level-3+ headings stay inside their parent section as content.\n   - **Code-fence guard:** track ``` and ~~~ fences during the scan; `##` inside a fenced block is content, not a delimiter. Indented code blocks aren't tracked (rare in this corpus; document the gap inline).\n   - Section names are case-sensitive; whitespace stripped from heading text.\n3. **Section operations** (`replace_section`, `append_to_section`, `add_section(position='after:Foo'|'before:Foo'|'start'|'end')`, `remove_section`, `rename_section`, `reorder(new_order)`): pure functions on `ParsedBody`, return new `ParsedBody`. Each raises typed errors (`SectionNotFound`, `SectionExists`, `InvalidPosition`) the tool layer maps to JSON error payloads.\n   - `_preamble` is addressable as a section name across these ops: `replace_section('_preamble', new_text)` overwrites the entire preamble (so `replace_section('_preamble', '# New Title\\n')` updates the title; this is the spec §2606 path). `append_to_section('_preamble', …)` appends. `remove_section('_preamble')` clears the preamble to empty string. `rename_section` from/to `_preamble` is rejected with `InvalidPosition` (the preamble is a structural slot, not a renamable section).\n4. **Diff helpers:**\n   - `compute_diff(old: str, new: str) -> str` — `''.join(difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True), fromfile='before', tofile='after', n=3))`.\n   - `diffs_equivalent(a: str, b: str) -> bool` — normalises both sides per spec §494: `\\r\\n → \\n`, strip trailing whitespace per line, drop trailing blank lines, then byte-equal compare.\n5. **No third-party deps** beyond stdlib (`difflib`, `re`). No imports of Store, ports, or tool_kit — keep this module pure.\n\n### Step 5: Default template + checklist seed (`agent_kit/templates.py`)\n**Scope:** Small\n1. **`DEFAULT_BODY_TEMPLATE(title, goal) -> str`** — emits the six-section design-doc skeleton (`# {title}\\n\\n## Goal\\n\\n{goal}\\n\\n## Principles\\n\\n## Context\\n\\n## Key Decisions\\n\\n## Open Questions\\n\\n## Deliverable\\n`).\n2. **`DEFAULT_CHECKLIST_SEED: list[str]`** — the 18 items from spec §634, all `source='default_seed'`, `status='open'`, positions 1–18.\n3. **No adaptation logic** in v1 (settled decision SD-003); the bot adapts via post-create `edit_epic` calls.\n\n### Step 6: Parser unit tests (`tests/test_body_parser.py`)\n**Scope:** Medium\n1. **Round-trip identity** for ≥6 fixtures: preamble-only (no `##`), single section, six-section design-doc, body with `### Authentication` sub-headings, body with a fenced code block containing `## Step 1`, body with non-empty preamble before first `##`. Assert `serialize(parse(b)) == b`.\n2. **Section ops** (each variant): only the targeted section changes; every other section's serialised form is byte-equal.\n3. **`_preamble` covers the title:** `replace_section(parse(body), '_preamble', '# New Title\\n')` round-trips through `parse` to a body whose `parsed.title == 'New Title'`. Removing the `# Title` line via `replace_section('_preamble', '')` round-trips to `parsed.title is None`, and `validate_for_write` raises `body_missing_required_section: title` on the result.\n4. **Lenient parse:** parsing `''`, `'just text\\n'`, `'## Goal\\n\\ngoal\\n'` (no title), `'# Title\\n'` (no Goal section), `'# Title\\n\\n## NotGoal\\n\\nx\\n'` (no `## Goal`) all return `ParsedBody` without raising. `validate_for_write` rejects each with the appropriate `body_missing_required_section` error.\n5. **Code-fence guard:** body with ` ```\\n## Inside\\n``` ` parses as a single preamble (no section split).\n6. **Diff equivalence:** `diffs_equivalent` returns True when only difference is `\\r\\n` vs `\\n`, trailing spaces, or trailing blank lines; False on real content delta.\n\n---\n\n## Phase 3: Store surface for epics, checklist, events\n\n### Step 7: Extend `Store` protocol (`agent_kit/ports.py`)\n**Scope:** Medium\n1. **Add** typed methods (Protocol + both adapters):\n   - `create_epic(*, title, goal, body, state='shaping') -> JSONDict` — single-row INSERT. Caller is the tool layer, which has already parsed and validated.\n   - `load_epic(epic_id) -> JSONDict | None`\n   - `update_epic(epic_id, **changes) -> JSONDict` — guarded UPDATE via the existing `_update` helper, restricted to a new `_EPIC_COLUMNS = {'title', 'goal', 'body', 'state', 'last_edited_at', 'last_active_at', 'planned_at'}` set. Used by `edit_epic` and `revert` for body+title+goal updates.\n   - `seed_checklist(epic_id, items: list[dict]) -> list[JSONDict]` — bulk INSERT.\n   - `list_checklist_items(epic_id, *, status: str | list[str] | None = None) -> list[JSONDict]`\n   - `update_checklist_item(item_id, **changes) -> JSONDict` — guarded by `_CHECKLIST_COLUMNS = {'content', 'status', 'position', 'skip_reason', 'superseded_by_item_id', 'completed_at'}`.\n   - `add_checklist_items(epic_id, items, start_position) -> list[JSONDict]`\n   - `delete_checklist_items(item_ids) -> int`\n   - `replace_checklist(epic_id, items) -> list[JSONDict]` — used by revert: DELETE all rows for `epic_id` then bulk INSERT from snapshot. Single transaction by virtue of the wrapping `store.transaction()`.\n   - `record_epic_event(*, epic_id, transaction_id, event_type, summary, prior_state, turn_id) -> JSONDict` — append-only INSERT, no update path.\n   - `list_epic_events(epic_id, *, since=None, until=None, kinds=None, limit=None) -> list[JSONDict]` — ordered `(occurred_at, id) ASC`. `get_history` reverses for display.\n   - `latest_transaction_id(epic_id) -> str | None`\n   - `events_by_transaction(transaction_id) -> list[JSONDict]`\n   - `list_recent_turns(*, n=10, epic_id=None) -> list[JSONDict]` — `bot_turns` ordered `started_at DESC LIMIT n`, optional epic filter.\n   - `search_tool_calls_by(*, tool_name=None, epic_id=None, since=None, limit=20) -> list[JSONDict]` — `tool_calls` joined to `bot_turns` for the epic filter.\n   - `update_message(...)` already exists; we'll reuse it from the loop bootstrap (Step 14) to retro-stamp `epic_id` on the inbound message.\n   - `update_turn(...)` already exists; reused to retro-stamp `epic_id` on the bot_turns row.\n\n### Step 8: Implement on `SupabaseStore` (`agent_kit/store/supabase.py`)\n**Scope:** Medium\n1. **Mirror** the protocol additions with concrete SQL using the existing `_normalize`/`_json` helpers and `_new_id` (prefixes: `'epic'`, `'check'`, `'evt'`).\n2. **Add** module-level constants `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` next to existing `_MESSAGE_COLUMNS`/`_TURN_COLUMNS`/`_IMAGE_COLUMNS`. Wire `update_epic` and `update_checklist_item` through the existing `self._update` helper for column safety.\n3. **Update `_TURN_COLUMNS`** to include `'epic_id'` so the loop bootstrap (Step 14) can retro-stamp the turn after `create_epic` fires.\n4. **Update `_MESSAGE_COLUMNS`** to include `'epic_id'` for the same reason.\n\n### Step 9: Implement on `SQLiteStore` (`agent_kit/store/sqlite.py`)\n**Scope:** Medium\n1. **Mirror** the same methods, the same `_EPIC_COLUMNS`/`_CHECKLIST_COLUMNS` constants, and the same `epic_id` additions to existing message/turn column sets.\n2. **Add** `'prior_state'` to `_JSON_COLUMNS`.\n\n### Step 10: Extend the contract test (`tests/store_contract.py`)\n**Scope:** Small\n1. **Add** a tail block to `run_store_contract` that exercises the new surface against `epic_1`: create a second epic via `store.create_epic`, seed checklist, append events with `transaction_id`s, list/filter events, query `latest_transaction_id`, and verify ordering. Both Supabase and SQLite contract tests pick this up automatically.\n\n---\n\n## Phase 4: Tools — `create_epic`, `edit_epic`, `revert`, `render_epic`, reads\n\n### Step 11: Editorial write tools (`agent_kit/tools/editorial.py`)\n**Scope:** Large\n1. **Register each tool** via `@register_tool` with explicit JSON schemas and `operation_kind='write'`.\n2. **`create_epic(context, title, goal)`** —\n   - Build body via `templates.DEFAULT_BODY_TEMPLATE(title, goal)`.\n   - `parsed = body.parse(rendered)`; `body.validate_for_write(parsed)` — on `BodyValidationError`, return `{\"error\": \"body_missing_required_section\", \"field\": …}` (don't raise; the model needs to read the message).\n   - Inside `store.transaction()`:\n     - `epic = store.create_epic(title=parsed.title, goal=parsed.goal_first_paragraph, body=rendered, state='shaping')` — title and goal come **only** from `parsed.*`, never from raw args (correctness-3).\n     - `store.seed_checklist(epic['id'], DEFAULT_CHECKLIST_SEED)`.\n     - `store.record_epic_event(epic_id=epic['id'], transaction_id=uuid4().hex, event_type='created', summary='Epic created with default design-doc template', prior_state=None, turn_id=context.turn_id)`.\n     - **Bootstrap retro-stamp** (when context.metadata['epic_id'] was None): `store.update_message(context.metadata['inbound_message_id'], epic_id=epic['id'])` and `store.update_turn(context.turn_id, epic_id=epic['id'])`. Set `context.metadata['epic_id'] = epic['id']` for downstream tools in the same turn.\n   - Return `{\"epic_id\", \"title\": parsed.title, \"goal\": parsed.goal_first_paragraph, \"section_names\": [...], \"checklist_count\": 18, \"transaction_id\"}`.\n3. **`edit_epic(context, epic_id, changes, change_summary, expected_diff?)`** —\n   - **Reject** unsupported keys: `changes.sprints` → `{\"error\": \"not_yet_supported\", \"field\": \"sprints\"}`; `changes.state` → `{\"error\": \"not_yet_supported\", \"field\": \"state\"}`; `changes.meta` → `{\"error\": \"meta_not_supported\", \"hint\": \"title and goal are derived from body; edit body.sections._preamble for title or body.sections.Goal for goal\"}` (scope-2).\n   - **Reject** mixed body ops: at most one of `new_content | sections | append | remove_sections | rename_section | reorder` per call → `{\"error\": \"body_op_conflict\"}`.\n   - **Body path:** `old = store.load_epic(epic_id)['body']`; `parsed = body.parse(old)`; apply the requested op; serialise → `new_body`. `body.validate_for_write(new_parsed)`. Compute `actual_diff = body.compute_diff(old, new_body)`. If `expected_diff` provided and `not body.diffs_equivalent(expected_diff, actual_diff)`, return `{\"error\": \"expected_diff_mismatch\", \"actual_diff\": actual_diff}` and **do not write**.\n   - **Checklist path:** apply `add` (positions auto-assigned to `max(existing.position) + 1` if absent; else honour and shift), `update` (per-item, only `_CHECKLIST_COLUMNS`-allowed fields), `remove` (delete by id). Capture pre-op snapshot for the event.\n   - **Inside one `store.transaction()`** with `transaction_id = uuid4().hex`:\n     - Body: `store.update_epic(epic_id, body=new_body, title=new_parsed.title, goal=new_parsed.goal_first_paragraph, last_edited_at=now())` + `store.record_epic_event(event_type='body_edit', prior_state={'body': old, 'title': old_title, 'goal': old_goal}, summary=change_summary, transaction_id, turn_id=context.turn_id)`.\n     - Checklist: apply per-item ops; `store.record_epic_event(event_type='checklist_change', prior_state={'items': [...full snapshot...]}, summary=change_summary, transaction_id, turn_id=context.turn_id)`.\n   - Return `{\"transaction_id\", \"diff\": actual_diff_or_empty, \"section_names\": [...], \"change_summary\"}`.\n4. **`revert(context, epic_id, event_id?=None)`** —\n   - Resolve target events: no `event_id` → fetch `events_by_transaction(latest_transaction_id(epic_id))`. With `event_id` → fetch the event, then all events sharing its `transaction_id` (spec §1399).\n   - **Capture pre-revert state** for the new event's `prior_state`: `{'body': current_body, 'title': current_title, 'goal': current_goal, 'checklist': [...current full snapshot...], 'reverted_transaction_id': txn, 'reverted_event_ids': [e.id for e in target_events]}`. This lets backward replay across this revert reconstruct correctly (FLAG-003, correctness-2).\n   - Apply each target event's `prior_state` in reverse-occurred order: `body_edit` → `store.update_epic(epic_id, body=…, title=…, goal=…)`; `checklist_change` → `store.replace_checklist(epic_id, prior_items)`. (Other event types in the transaction — e.g., a future `state_change` — are no-ops in Sprint 2a; bot won't trigger them.)\n   - Append a new `reverted_to` event with the captured pre-revert `prior_state` and a fresh `transaction_id`. The event is itself revertible because its `prior_state` carries the full pre-revert snapshot.\n   - Return `{\"transaction_id\", \"reverted_event_count\", \"summary\": f'Reverted transaction {txn}'}`.\n5. **`render_epic(context, epic_id, format='markdown')`** — `'markdown'` returns the body as-is (image-reference resolution is a Sprint 6 no-op). `'html'` → `{\"error\": \"not_yet_supported\"}`.\n\n### Step 12: Editorial read tools (`agent_kit/tools/editorial_reads.py`)\n**Scope:** Medium\n1. **Register** each tool with **`operation_kind='read'`** (scope-1).\n2. **`get_epic(epic_id, sections=None)`** — `parsed = body.parse(epic['body'])`. Return `{title: parsed.title, goal: parsed.goal_first_paragraph, body_full: epic['body'] if sections is None else None, sections: {name: content, …} when sections is supplied, section_names: [s.name for s in parsed.sections], state}`. Lenient parse means malformed bodies still load.\n3. **`get_section_names(epic_id)`** — return `[s.name for s in body.parse(epic['body']).sections]`.\n4. **`get_history(epic_id, kind=None, since=None)`** — `store.list_epic_events(...)` reversed (most recent first), optionally filtered.\n5. **`get_self_understanding(epic_id)`** — return `{goal, state, open_checklist_count, section_names, recent_events: last 3}`. Document inline that the spec §1068 7-section structure (recent decisions, code refs, second opinions, etc.) lights up incrementally as later sprints land their tables.\n6. **`get_epic_at_time(epic_id, timestamp)`** — backward replay from current state:\n   - Load current `body, checklist`.\n   - Fetch `list_epic_events(epic_id)` (full ascending list).\n   - Walk the events whose `occurred_at > timestamp` in **descending** order; for each, undo using `prior_state`:\n     - `body_edit`: `body = prior_state['body']`.\n     - `checklist_change`: `checklist = prior_state['items']`.\n     - `created`: this is the earliest possible state; if we're rolling past it, return empty/None body+checklist (caller asked for a time before the epic existed).\n     - `reverted_to`: undo by restoring `prior_state['body']` and `prior_state['checklist']` (the captured pre-revert snapshot — Step 11.4 makes this work).\n     - Other event_types (sprints, state, code_referenced, etc., none of which fire in Sprint 2a) fall through with a logged warning.\n   - Tied timestamps order by `(occurred_at, id) ASC`; when walking descending, reverse that.\n   - Return `{body, checklist, reconstructed_at: timestamp}`.\n7. **`get_recent_turns(n=10, epic_id=None)`** — `store.list_recent_turns(...)`; for each turn, attach `change_summary` aggregated from `epic_events` rows with that `turn_id` (single `WHERE turn_id IN (...)` query joined client-side).\n8. **`search_tool_calls(tool_name=None, epic_id=None, since=None, limit=20)`** — delegates to `store.search_tool_calls_by(...)`.\n\n### Step 13: Register the tools in the loop import path (`agent_kit/loop.py:16`)\n**Scope:** Small\n1. **Add** `import agent_kit.tools.editorial  # noqa: F401` and `import agent_kit.tools.editorial_reads  # noqa: F401` next to existing `communication`/`images` imports so tools auto-register.\n\n---\n\n## Phase 5: Loop bootstrap + turn-end outline log\n\n### Step 14: No-epic turn mode (`agent_kit/loop.py:25` and surrounding)\n**Scope:** Medium\n1. **Make `epic_id` Optional** on `run_turn` and propagate through downstream code paths:\n   - When `epic_id is None`: skip `store.acquire_epic_lock` entirely. Skip the lock-contended early return.\n   - Inbound message creation (`agent_kit/loop.py:79–85`): `epic_id=None` is already nullable (`messages.epic_id` is FK with `ON DELETE SET NULL`, NULL allowed). Capture the resulting `inbound_message_id` in `context.metadata['inbound_message_id']` so `create_epic` can retro-stamp.\n   - `store.create_turn(epic_id=None, …)` is allowed (`bot_turns.epic_id` already nullable). The turn row carries NULL until `create_epic` retro-stamps it.\n   - `load_hot_context` is currently `load_hot_context(epic_id)` and dereferences `epic`; in no-epic mode, skip the call and pass `hot_context = {\"epic\": None, \"recent_messages\": [], \"recent_tool_calls\": []}` to the model.\n   - After every tool invocation, if `context.metadata.get('epic_id')` flipped from None to a real id (set by `create_epic`'s post-commit hook in Step 11.2), the loop's lock-release path must skip — there was no lock to release.\n2. **CLI plumbing (`arnold/cli.py`):** allow invoking with no `--epic-id` (or an explicit `--no-epic` flag); pass `epic_id=None` to `run_turn`. The system prompt for that branch should hint \"no active epic — call `create_epic(title, goal)` first if the user is starting one.\"\n3. **Existing callers** (`tests/test_run_turn.py`) keep passing an `epic_id` and continue to work unchanged. The no-epic path is purely additive.\n\n### Step 15: Turn-end `epic_outline` log (`agent_kit/loop.py`)\n**Scope:** Small\n1. **At the end of `run_turn`**, after `update_turn(status='completed', …)` and before envelope return: if `context.metadata.get('epic_id')` is set AND any tool_call this turn had `tool_name in {'create_epic','edit_epic','revert'}` (walk `events`), then `parsed = body.parse(store.load_epic(epic_id)['body'])`, `details = body.outline(parsed)`, and call `log(store, 'info', 'application', 'epic_outline', f\"Epic outline: {parsed.title or '(untitled)'}\", details=details, turn_id=turn['id'], epic_id=epic_id)`.\n2. **Failure paths** (`status='failed'`) skip the log. Pure-read turns and turns that never created an epic skip the log.\n\n---\n\n## Phase 6: Integration test + regression verification\n\n### Step 16: 10-turn fixture (`tests/test_editorial_loop.py`)\n**Scope:** Medium\n1. **Use** `FakeModel(script=…)` (per `tests/test_run_turn.py:8`) and `SQLiteStore` with a deterministic 10-turn script:\n   - Turn 1: `run_turn(epic_id=None, input='Make me an auth flow design epic')` → tool_use `create_epic(title='Auth flow design', goal='Decide on auth provider and token storage')` → final text.\n   - Turns 2–9: `run_turn(epic_id=<the new id>)` with `edit_epic` calls hitting **all six default sections** at least once via `sections` ops, plus a `_preamble` replace that updates the title (asserts `epics.title` reflects the new value), plus an `append`, plus a `checklist.update` marking 3 items done. Include one `expected_diff` round-trip (matching) and one mismatch turn (asserts DB unchanged).\n   - Turn 10: `revert` (most recent transaction) followed by `send_message`.\n2. **Assertions** — one per spec §131–142 acceptance criterion plus the critique-driven additions:\n   - After Turn 1: `epics` row exists with `title='Auth flow design'`, `goal='Decide on auth provider and token storage'`; 18 `checklist_items` with `source='default_seed'`; one `created` event; the inbound message and bot_turn both have `epic_id` retro-stamped.\n   - After all turns: every default section present; section-only edits leave other sections byte-identical (verified by re-parsing prior_state captured in `body_edit` events).\n   - Whole-body `new_content` turn: `body_edit` event captured prior body; manual `revert(epic_id, event_id=that_event)` then `load_epic` returns prior body byte-equal.\n   - \"revert that\" turn: most-recent transaction undone; new `reverted_to` event present; `prior_state` contains body + checklist snapshots (FLAG-003 verification).\n   - `expected_diff` mismatch turn: tool result has `error='expected_diff_mismatch'`; epics + checklist unchanged.\n   - `expected_diff` match turn: writes commit normally.\n   - **Title-via-preamble turn:** before/after `epics.title` differs; the same transaction's `body_edit` event captured the old title in `prior_state`.\n   - `get_epic_at_time(epic_id, T_after_turn_5)` returns body + checklist matching a hand-rolled replay computed inside the test.\n   - `get_epic_at_time(epic_id, T_just_before_revert)` returns body+checklist as it was right before the revert (verifies FLAG-003 fix end-to-end).\n   - `get_recent_turns(5)` returns 5 turns most-recent-first.\n   - `search_tool_calls(tool_name='edit_epic', epic_id=…)` returns ≥3 rows.\n   - One `system_logs` row per touching turn with `event_type='epic_outline'`, `category='application'`, and `details.sections` containing all six default headings (after the relevant turns).\n   - `tool_calls.operation_kind` for `get_epic`, `get_section_names`, `get_history`, etc. is `'read'`; for `create_epic`, `edit_epic`, `revert`, `render_epic` is `'write'` (scope-1 verification).\n   - Calling `edit_epic(changes={'meta': {'title': 'X'}})` returns `error='meta_not_supported'` (scope-2 verification).\n\n### Step 17: Run the targeted tests, then full regression\n**Scope:** Small\n1. `pytest tests/test_body_parser.py -x`.\n2. `pytest tests/test_sqlite_store.py tests/test_sqlite_store_v1b.py -x` to confirm the new contract additions pass.\n3. `pytest tests/test_editorial_loop.py -x`.\n4. `pytest -x` for the full suite (no Sprint 1a/1b regression).\n5. **Optional:** `SUPABASE_TEST_DB_URL=… pytest tests/test_supabase_store.py` if a local Supabase is available.\n\n---\n\n## Execution Order\n\n1. Schema first (Phase 1) — migrations unblock everything.\n2. Body parser + templates with their unit tests (Phase 2). Pure code, fastest feedback. Land lenient parse + strict validate split before building anything that depends on it.\n3. Store extensions (Phase 3) — column-safety constants + new methods, exercised through the contract test.\n4. Tools (Phase 4) — depends on parser + store. Write tools first (`create_epic`, `edit_epic`, `revert`, `render_epic`), then reads.\n5. Loop bootstrap + outline log (Phase 5) — depends on tools. Bootstrap first (FLAG-001) so `create_epic` is callable; then outline log.\n6. Integration fixture (Phase 6) — proves the whole pipeline + every critique fix end-to-end.\n\n## Validation Order\n\n1. `pytest tests/test_body_parser.py` — fastest feedback on parser edge cases (lenient/strict split, `_preamble` title).\n2. Contract tests (`tests/test_sqlite_store.py`, `tests/test_supabase_store.py` when DB available) — confirms new Store surface is consistent across adapters and column-safety holds.\n3. `pytest tests/test_editorial_loop.py` — the 10-turn integration with bootstrap, time-travel-across-revert, `_preamble`-title, and `meta_not_supported` assertions.\n4. `pytest -x` — full regression.",
  "changes_summary": "Rev 2 addresses all 12 open critique flags by editing the existing six-phase structure rather than restructuring. Key changes: (1) added a no-epic mode to `run_turn` (epic_id=None), with `create_epic` retro-stamping the inbound message and bot_turn (FLAG-001/issue_hints-1/callers); (2) split parser into lenient `parse()` + strict `validate_for_write()` so reads/time-travel survive malformed bodies (FLAG-002/correctness-1); (3) redefined `_preamble` to include the `# Title` line per spec §2606, making `replace_section('_preamble', ...)` the canonical title-edit path (issue_hints-2); (4) `reverted_to` events now snapshot full pre-revert body + checklist in `prior_state` so backward replay works across reverts (FLAG-003/correctness-2); (5) `create_epic` writes `epics.title`/`goal` exclusively from parsed values, never raw args (correctness-3); (6) read tools register with `operation_kind='read'` (scope-1); (7) `edit_epic.changes.meta` is explicitly rejected with `meta_not_supported` and a hint to use body sections (scope-2); (8) added `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` to both Store adapters and extended `_MESSAGE_COLUMNS`/`_TURN_COLUMNS` to allow the bootstrap `epic_id` retro-stamp (all_locations). Integration test gained explicit assertions for each critique fix (title-via-preamble, time-travel-across-revert, meta_not_supported, operation_kind values).",
  "flags_addressed": [
    {
      "id": "FLAG-001",
      "resolution": "addressed",
      "reason": "run_turn now accepts epic_id=None; lock acquisition and load_hot_context are skipped; create_epic retro-stamps the inbound message and bot_turn rows. CLI gets a no-epic invocation path. Integration test exercises the bootstrap turn end-to-end."
    },
    {
      "id": "FLAG-002",
      "resolution": "addressed",
      "reason": "Parser split: parse() is now explicitly lenient and never raises; validate_for_write() is strict and called only by write paths. Round-trip fixtures and time-travel/read tools exercise the lenient path."
    },
    {
      "id": "FLAG-003",
      "resolution": "addressed",
      "reason": "revert now captures the full pre-revert body + checklist snapshot in the new reverted_to event's prior_state, so backward replay across a revert restores the immediately-pre-revert state. Integration test asserts get_epic_at_time(T_just_before_revert) matches the captured snapshot."
    },
    {
      "id": "issue_hints-1",
      "resolution": "addressed",
      "reason": "Same fix as FLAG-001: run_turn(epic_id=None) is a first-class mode and create_epic retro-stamps the message + turn after commit."
    },
    {
      "id": "issue_hints-2",
      "resolution": "addressed",
      "reason": "_preamble is redefined to include the # Title line and any leading text up to the first ## heading, matching spec §2606. replace_section('_preamble', '# New Title\\n') is the canonical title-edit path; rename_section to/from _preamble is rejected. Integration test exercises the title-via-preamble case."
    },
    {
      "id": "correctness-1",
      "resolution": "addressed",
      "reason": "Same fix as FLAG-002: parse() is lenient, validate_for_write() is strict and only used on writes. Read tools and get_epic_at_time work against legacy/malformed bodies without raising."
    },
    {
      "id": "correctness-2",
      "resolution": "addressed",
      "reason": "Same fix as FLAG-003: reverted_to event prior_state now contains the full pre-revert state."
    },
    {
      "id": "correctness-3",
      "resolution": "addressed",
      "reason": "create_epic now passes parsed.title and parsed.goal_first_paragraph (not the raw arguments) to store.create_epic. The body parser is the only writer of epics.title and epics.goal, matching spec §1314–1316."
    },
    {
      "id": "scope-1",
      "resolution": "addressed",
      "reason": "All read tools (get_epic, get_section_names, get_history, get_self_understanding, get_epic_at_time, get_recent_turns, search_tool_calls) register with operation_kind='read'. Integration test asserts correct operation_kind in tool_calls rows."
    },
    {
      "id": "scope-2",
      "resolution": "addressed",
      "reason": "edit_epic explicitly rejects changes.meta with error='meta_not_supported' and a hint pointing to body.sections._preamble (for title) or body.sections.Goal (for goal). Asserted in the integration test."
    },
    {
      "id": "all_locations",
      "resolution": "addressed",
      "reason": "Both adapters gain module-level _EPIC_COLUMNS and _CHECKLIST_COLUMNS constants wired through the existing _update helper, mirroring _MESSAGE_COLUMNS/_TURN_COLUMNS/_IMAGE_COLUMNS. _MESSAGE_COLUMNS and _TURN_COLUMNS are extended to include 'epic_id' so the bootstrap retro-stamp uses guarded updates."
    },
    {
      "id": "callers",
      "resolution": "addressed",
      "reason": "Same fix as FLAG-001: run_turn callers can pass epic_id=None for the bootstrap; existing callers (tests/test_run_turn.py) keep passing an epic_id and remain unchanged. The no-epic path is purely additive."
    }
  ],
  "assumptions": [
    "Sprint 2a stays invocation-mode only; no resident-mode behaviour changes.",
    "Sprints, sprint_items, codebases, code_artifacts, feedback, second_opinions, and image generation are out of scope. edit_epic.changes.sprints and changes.state return not_yet_supported.",
    "edit_epic.changes.meta is explicitly rejected with meta_not_supported and a hint to edit via body.sections._preamble (for title) or body.sections.Goal (for goal); title and goal are derived columns whose only writer is the body parser.",
    "_preamble is the raw text from byte 0 up to (but not including) the first ## line, INCLUDING the # Title line and any blank/leading lines before the first section. replace_section('_preamble', '# New Title\\n') is the canonical title-edit path per spec §2606. rename_section from/to '_preamble' is rejected.",
    "parse() is lenient and never raises on missing #/## headings, malformed input, or empty bodies. validate_for_write() is the only place that raises body_missing_required_section, and is called only on write paths.",
    "Default body template ships with one variant (design-doc); create_epic accepts (title, goal) and constructs the body from the template, then derives epics.title and epics.goal from parse() output — raw args are template inputs only.",
    "Default checklist seed is unconditional (all 18 items); adaptation lives in the bot's prompt/decisions, not server-side at create time.",
    "expected_diff equivalence: line endings normalised to \\n, per-line trailing whitespace stripped, trailing blank lines dropped, then byte-equal compare.",
    "render_epic supports format='markdown' only in v1; format='html' returns not_yet_supported. Image-reference resolution is a Sprint 6 no-op.",
    "epic_outline log fires on any turn whose tool_calls include create_epic, edit_epic, or revert; pure-read turns and failed turns skip the log.",
    "Single-writer concurrency via existing epic_locks + per-edit_epic store.transaction is sufficient. The new no-epic mode skips lock acquisition entirely (no lock contention possible before an epic exists).",
    "run_turn gains an Optional epic_id parameter (None = no-epic mode). Existing callers in tests/test_run_turn.py and resident mode keep passing a concrete epic_id and remain unchanged. Bootstrap retro-stamps the inbound message and bot_turn with the new epic_id once create_epic commits.",
    "spec test #7 (planning-bot-spec.md:2606) references body_version, but that column does not exist in the current schema; we cover the title/body sync semantics (title updates atomically with body, audit captures the change) without introducing body_version. Adding the column is deferred unless a later sprint requires it.",
    "All read tools register with operation_kind='read'; write tools register with operation_kind='write'. The default ('write') is overridden explicitly so audit semantics are correct.",
    "The existing megaplan/ directory is harness state and is left untouched; CLAUDE.md's prohibition applies to creating one, not the existing path."
  ],
  "success_criteria": [
    {
      "criterion": "Postgres migration 004 and SQLite migration 004 create checklist_items and epic_events with the columns, CHECK constraints, FK ON DELETE behaviour, and indexes specified in spec §1322 and §1381.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "body.parse() is lenient and returns a ParsedBody for empty input, plain-text input, bodies with no '##' headings, bodies missing '# Title', and bodies missing '## Goal' — without raising. Integration tools (get_epic, get_epic_at_time) work against these inputs.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "body.validate_for_write() raises BodyValidationError('body_missing_required_section: title') when parsed.title is None or empty, and 'body_missing_required_section: goal' when parsed.goal_first_paragraph is None or empty. Write tools surface this as a structured tool result error.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Body parser round-trip identity holds: serialize(parse(body)) == body for ≥6 fixture bodies including preamble-only (no '##'), single section, full design-doc template, sub-headings, fenced code containing '##', and a body with non-empty preamble before the first section.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "_preamble section addressing covers the '# Title' line per spec §2606: replace_section(parsed, '_preamble', '# New Title\\n') round-trips to ParsedBody with title='New Title'; replace_section(parsed, '_preamble', '') round-trips to title=None and validate_for_write rejects it with body_missing_required_section: title.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "create_epic creates an epics row whose title and goal columns equal parse(rendered_template).title and .goal_first_paragraph respectively (not the raw input arguments), seeds 18 default checklist items with status='open' and source='default_seed', and writes one 'created' epic_event sharing a transaction_id.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "run_turn(epic_id=None, input=...) executes without acquiring an epic_locks row, creates an inbound message and bot_turn with epic_id=NULL, and — when create_epic fires within the turn — retro-stamps both rows with the new epic_id by the time the turn completes.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "edit_epic body section operations leave every non-targeted section byte-identical (verified by parsing prior_state captured in the body_edit event and comparing every other section's serialised form).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "edit_epic with expected_diff that does not match (after \\n + trailing-whitespace + trailing-blank-line normalisation) refuses to commit, returns the actual diff, and leaves epics.body, title, goal, and checklist_items untouched.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "edit_epic with expected_diff that matches commits normally and writes one event per affected family (body_edit, checklist_change) sharing a single transaction_id.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "edit_epic rejects changes.meta with error='meta_not_supported' and a hint string referencing body.sections._preamble or body.sections.Goal; epics row is unchanged.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "revert(epic_id) with no event_id undoes the entire most-recent transaction (body, title, goal, and checklist together) and appends a 'reverted_to' event whose prior_state captures the full pre-revert body and checklist; the resulting body is byte-equal to the pre-edit body.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "get_epic_at_time(epic_id, T) returns body and checklist state equal to what was committed at the most recent event with occurred_at <= T — including timestamps that fall just before a revert (verifies reverted_to.prior_state captures enough state for backward replay).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "get_recent_turns(5) returns the 5 most-recent bot_turns rows (most-recent first) with summaries; search_tool_calls(tool_name='edit_epic', epic_id=X) returns every edit_epic call against epic X with arguments and timestamps.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "All read tools (get_epic, get_section_names, get_history, get_self_understanding, get_epic_at_time, get_recent_turns, search_tool_calls) record operation_kind='read' in tool_calls; all write tools (create_epic, edit_epic, revert, render_epic) record operation_kind='write'.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "After every turn whose tool_calls include create_epic, edit_epic, or revert, exactly one system_logs row exists with category='application', event_type='epic_outline', turn_id=<that turn>, and details containing title plus a sections array with name + line_count for every section in the body.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "10-turn FakeModel-driven integration fixture in tests/test_editorial_loop.py runs end-to-end starting from epic_id=None, exercises all six default sections, exercises both expected_diff match and mismatch, exercises title editing via _preamble, exercises revert with backward replay across the revert, and asserts every Sprint 2a acceptance criterion in spec §131–142.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "All pre-existing tests in tests/ continue to pass (no regression in Sprint 1a/1b functionality, including resident-mode test_resident*, test_discord_*, and test_run_turn variants).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Both Store adapters expose _EPIC_COLUMNS and _CHECKLIST_COLUMNS allowed-column sets and route update_epic / update_checklist_item through the existing _update helper, matching the _MESSAGE_COLUMNS / _TURN_COLUMNS / _IMAGE_COLUMNS pattern. _MESSAGE_COLUMNS and _TURN_COLUMNS include 'epic_id' so the bootstrap retro-stamp passes column safety.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Body parser and section-op modules stay focused: the public surface is parse, serialize, validate_for_write, the section ops, compute_diff, diffs_equivalent, outline. No tool-layer or Store imports leak into agent_kit/body.py.",
      "priority": "should",
      "requires": [
        "read_files",
        "subjective_judgment"
      ]
    },
    {
      "criterion": "edit_epic rejects requests mixing two body op flavours (e.g. new_content + sections) with error='body_op_conflict' rather than silently picking one.",
      "priority": "should",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "agent_kit/body.py stays under ~450 lines and has no third-party dependencies beyond the standard library (difflib, re).",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    }
  ],
  "questions": [
    "Should the no-epic bootstrap path also handle 'user typed a question that doesn't warrant creating an epic' (e.g., greetings, meta-questions)? Plan currently assumes the bot either calls create_epic or sends a message-only response; a turn that ends with epic_id still NULL is treated as a successful no-op (epic_outline log skipped). Is that acceptable, or should we reject turn completion if epic_id is still NULL after the model loop?",
    "spec test #7 (planning-bot-spec.md:2606) references a body_version column that does not exist in the current schema. Plan defers introducing body_version, covering the audit/title-update semantics another way. Confirm body_version is fine to skip in Sprint 2a, or pull it forward as a one-line column add in migration 004?",
    "get_epic_at_time across reverts: the plan handles the simple case (body+checklist snapshot in reverted_to.prior_state lets backward replay restore the immediate pre-revert state). Does the spec require correct reconstruction at timestamps that fall *between* a body_edit event and a revert that undoes it (e.g., T was after the edit but before the revert)? Backward replay handles that naturally; flagging in case the desired semantics differ."
  ]
}
```

> TOOL

tool_result StructuredOutput
```
Structured output provided successfully
```

> AGENT

Rev 2 plan delivered as structured output. All 12 open flags addressed without restructuring:

- **Bootstrap (FLAG-001 / issue_hints-1 / callers):** `run_turn` gains an `epic_id=None` mode that skips lock acquisition; `create_epic` retro-stamps the inbound message and bot_turn after commit.
- **Parser split (FLAG-002 / correctness-1):** `parse()` is lenient and never raises; new `validate_for_write()` is the only strict gate, called only by write paths.
- **`_preamble` covers the title (issue_hints-2):** preamble is everything from byte 0 up to the first `##`, so `replace_section('_preamble', '# New Title\n')` is the canonical title-edit path per spec §2606.
- **`reverted_to` snapshot (FLAG-003 / correctness-2):** new event captures full pre-revert body + checklist in `prior_state`, so backward replay across a revert is correct.
- **Parser-as-only-writer (correctness-3):** `create_epic` writes `epics.title` / `goal` exclusively from `parsed.title` / `parsed.goal_first_paragraph`.
- **`operation_kind='read'` (scope-1):** all read tools register explicitly; integration test asserts `tool_calls.operation_kind` values.
- **`changes.meta` (scope-2):** rejected with `meta_not_supported` and a hint pointing to body sections.
- **Adapter column-safety (all_locations):** `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` added; `_MESSAGE_COLUMNS` / `_TURN_COLUMNS` extended with `epic_id` for the bootstrap retro-stamp.

Three new questions raised for the gate (no-epic-but-no-create-call turn handling, `body_version` column deferral, time-travel semantics between an edit and its revert).

> DEVELOPER

You are already running inside the megaplan harness for this step. Do the requested planning/review/execution work directly. Do NOT invoke the `megaplan` CLI, do NOT read or activate the `megaplan` skill, do NOT start nested megaplan plans, and do NOT recurse into another planning harness. Treat mentions of megaplan in the repository or environment as implementation context only.

You are revising an implementation plan after critique and gate feedback.

        Project directory:
        /Users/user_c042661f/Documents/arnold-v2




        Idea:
# Sprint 2a — Editorial core

Bot maintains an epic body and checklist for one epic, with section-level body editing. Minimum to have an editorial conversation.

**Full spec is at `planning-bot-spec.md` in this repo root. Refer to it for complete details on Body Structure and Editing, Body Templates, The Checklist as Guide, and Data Model sections.**

## Supabase
- URL: https://yhwflvadmefhkshwbfnf.supabase.co
- Service key: [REDACTED_SUPABASE_SERVICE_ROLE_JWT]

## Scope

- Tables: checklist_items, epic_events (with transaction_id)
- Body parser/serializer — markdown ↔ structured sections with ## heading delimiters; enforces heading hierarchy (# for title only, ## for sections, ### for sub-headings)
- Turn-end epic outline emitted to system_logs at info level
- Default body template (design doc) — Goal, Principles, Context, Key Decisions, Open Questions, Deliverable
- `edit_epic` tool — body (whole + section ops) + checklist; supports:
  - Write whole body
  - Write specific sections
  - Append to a section
  - Add new section with position
  - Rename/remove sections
  - `expected_diff` parameter for server-enforced diff verification (unified diff format)
- `create_epic`, `revert` (transaction-grouped), `render_epic` tools
- Read tools: `get_epic` (with section addressing), `get_section_names`, `get_history`, `get_self_understanding`
- History tools: `get_epic_at_time`, `get_recent_turns`, `search_tool_calls`
- Default checklist seed — 18 items with adaptation logic
- Title and goal are derived columns from body parsing (# Title and ## Goal first paragraph)

## Key Data Model

### checklist_items
id, epic_id, content, status (open|done|skipped|superseded), position, source (bot_inferred|user_requested|carried_over|default_seed|second_opinion), skip_reason, superseded_by_item_id, created_at, completed_at

### epic_events
id, epic_id, transaction_id (uuid), event_type, summary, prior_state (json), turn_id, occurred_at
Event types: body_edit, checklist_change, sprints_change, state_change, forced_handoff, created, code_referenced, codebase_added, image_generated, second_opinion_requested, reverted_to, sprint_status_change

## Body Parser Rules
- Section boundaries are ## headings (level-2 markdown)
- Section names are case-sensitive
- Pre-section content is "_preamble"
- Sub-sections (### and below) are part of parent section
- No ## headings → whole body is _preamble
- # Title and ## Goal are required structural elements; missing → write rejected
- Code blocks containing ## are NOT section boundaries

## Acceptance Criteria

- Create an epic via natural language → epics row created, default checklist seeded with 18 items, body initialized
- 10-turn scripted conversation (mocked Anthropic) produces body with all 6 default sections
- Section-level edit → only that section changes; other sections byte-identical
- Whole body edit → diff captured in event; revert restores prior version exactly
- "revert that" → most recent transaction undone, new reverted_to event logged
- expected_diff mismatch → server refuses write, returns actual diff
- expected_diff match → server commits normally
- get_epic_at_time(epic_id, T) → returns body/checklist state as of time T
- get_recent_turns(5) → returns 5 most recent turns with summaries
- search_tool_calls(tool_name='edit_epic', epic_id=X) → returns matching calls
- Turn-end system_logs row with event_type='epic_outline' containing title + section list + line counts

## Tests
- Unit: body parser (markdown → sections → markdown roundtrip is identity); section operations; edit_epic validation; transaction_id grouping; expected_diff comparison; epic-at-time replay
- Integration: 10-turn fixture conversation against local Supabase with mocked Anthropic; revert end-to-end

        Current plan (markdown):
        # Implementation Plan: Sprint 2a — Editorial Core (rev 2)

## Overview

Sprint 2a gives Arnold a *document* to edit. Today the codebase has an `epics` table (`supabase/migrations/202604300001_001_core.sql`), a turn loop (`agent_kit/loop.py`) that requires `epic_id` to acquire `epic_locks` before any model call, a `Store` protocol (`agent_kit/ports.py`) backed by SQLite + Postgres adapters, and a `system_logs` sink. The only registered tools are `send_message`, `set_activity`, `defer_to_caller`, `view_image`, `send_image`, `update_image_metadata`.

This sprint adds (1) two new tables (`checklist_items`, `epic_events`); (2) a body parser/serializer with section addressing; (3) Store CRUD for epics/checklist/events; (4) ~10 new tools (`create_epic`, `edit_epic`, `revert`, `render_epic`, plus reads); (5) a no-epic turn-mode so `create_epic` is callable from a fresh state; (6) a turn-end `epic_outline` log.

Constraints worth pinning up front (now reflecting critique fixes):

- **Bootstrap path:** `run_turn(epic_id=None)` is now a first-class mode. Lock acquisition is skipped; the inbound message and the `bot_turns` row are created with `epic_id=NULL` (both columns are already nullable per `supabase/migrations/202604300001_001_core.sql:22, :50`). When `create_epic` fires, it stamps `context.metadata['epic_id']`, then UPDATEs the inbound message and the turn to point at the new epic. (FLAG-001, issue_hints-1, callers.)
- **Parser split:** `parse(body)` is **lenient** — it accepts any input, including bodies missing `# Title`, bodies with no `##` headings (whole body is `_preamble`), and legacy/malformed content. Only **`validate_for_write(parsed)`** is strict and is called only by write paths. (FLAG-002, correctness-1.)
- **`_preamble` includes the `# Title` line** per spec §2606. The preamble is the raw text from the start of the body up to (but not including) the first `##` line. Replacing `_preamble` with `'# New Title\n'` therefore updates the title; removing the `# Title` line via a preamble write is rejected by `validate_for_write` with `body_missing_required_section: title`. (issue_hints-2.)
- **Title/goal columns are parser-derived only.** `create_epic` and `edit_epic` write `epics.title` and `epics.goal` exclusively from `parsed.title` and `parsed.goal_first_paragraph`. Raw `title`/`goal` arguments are template inputs only. (correctness-3.)
- **`reverted_to` events store full pre-revert state.** `prior_state = {'body': pre_revert_body, 'checklist': [...], 'reverted_transaction_id': txn, 'reverted_event_ids': [...]}` so backward replay across reverts is correct. (FLAG-003, correctness-2.)
- **Read tools register with `operation_kind='read'`.** Write tools default `operation_kind='write'`. (scope-1.)
- **`edit_epic.changes.meta` is rejected** with `meta_not_supported`: title/goal are derived columns; bot must edit `body.sections._preamble` (for title) or `body.sections.Goal` (for goal). (scope-2.)
- **Mutually exclusive body ops.** `new_content`, `sections`, `append`, `remove_sections`, `rename_section`, and `reorder` are mutually exclusive in a single `edit_epic.body`; mixing returns `body_op_conflict`.
- **`expected_diff` equivalence:** `\n` line endings, strip trailing whitespace per line, drop trailing blank lines (spec §494).
- **Out of scope:** sprints, sprint_items, codebases, code_artifacts, feedback, second_opinions, image generation. `edit_epic.changes.sprints` and `changes.state` return `not_yet_supported`.
- CLAUDE.md forbids creating a `megaplan/` directory; the existing one is harness state, not a target.

Six phases. Phases 1–3 land schema, parser, and store surface. Phase 4 lands tools. Phase 5 wires the loop bootstrap and outline log. Phase 6 covers the integration fixture.

---

## Phase 1: Schema — checklist_items, epic_events

### Step 1: Postgres migration (`supabase/migrations/202604300004_004_editorial_core.sql`)
**Scope:** Small
1. **Create** `checklist_items` matching spec §1322 exactly: `id TEXT PK`, `epic_id TEXT NOT NULL REFERENCES epics(id) ON DELETE CASCADE`, `content TEXT NOT NULL`, `status TEXT CHECK IN ('open','done','skipped','superseded')`, `position INTEGER NOT NULL`, `source TEXT CHECK IN ('bot_inferred','user_requested','carried_over','default_seed','second_opinion')`, `skip_reason TEXT`, `superseded_by_item_id TEXT REFERENCES checklist_items(id)`, `created_at TIMESTAMPTZ DEFAULT now()`, `completed_at TIMESTAMPTZ`. Index `(epic_id, status, position)`.
2. **Create** `epic_events` matching spec §1381 exactly: `id TEXT PK`, `epic_id TEXT NOT NULL REFERENCES epics(id) ON DELETE CASCADE`, `transaction_id TEXT NOT NULL`, `event_type TEXT CHECK IN ('body_edit','checklist_change','sprints_change','state_change','forced_handoff','created','code_referenced','codebase_added','image_generated','second_opinion_requested','reverted_to','sprint_status_change')`, `summary TEXT NOT NULL`, `prior_state JSONB`, `turn_id TEXT REFERENCES bot_turns(id) ON DELETE SET NULL`, `occurred_at TIMESTAMPTZ DEFAULT now()`. Indexes `(epic_id, occurred_at DESC)` and `(transaction_id)`.

### Step 2: SQLite mirror (`agent_kit/store/migrations/sqlite/004_editorial_core.sql`)
**Scope:** Small
1. **Mirror** the Postgres migration in SQLite (TEXT for everything; `prior_state` is a TEXT JSON blob, consistent with how `prompt_snapshot` etc. are handled in `001_core.sql`).
2. **Register** `prior_state` in the JSON-encoding sets at `agent_kit/store/sqlite.py:17` and `agent_kit/store/supabase.py:12`.

### Step 3: Update Supabase truncate fixture (`tests/test_supabase_store.py:33`)
**Scope:** Small
1. **Add** `checklist_items` and `epic_events` to the `TRUNCATE TABLE … RESTART IDENTITY CASCADE` block.

---

## Phase 2: Body parser/serializer

### Step 4: Parser module — lenient parse, strict validate (`agent_kit/body.py`)
**Scope:** Medium
1. **Public surface** (everything else `_private`):
   - `parse(body: str) -> ParsedBody` — **lenient**. Never raises. `ParsedBody`: `title: str | None`, `goal_first_paragraph: str | None`, `preamble: str` (raw text from byte 0 up to but not including the first `##` line; INCLUDES the `# Title` line and any blank/text lines after it), `sections: list[Section]` in order. `Section`: `name: str`, `content: str`, `subheadings: list[str]`, `line_count: int`. Title is extracted by scanning the preamble for the first non-blank line matching `^#\s+(.+?)\s*$`; if absent or empty, `title` is `None`. Goal is extracted by finding a section named exactly `Goal`, taking everything before the first blank line in its content (whitespace-stripped); if section absent or empty, `goal_first_paragraph` is `None`. Bodies with no `##` headings parse cleanly to `sections=[]` and `preamble=<entire body>`.
   - `serialize(parsed: ParsedBody) -> str` — round-trip identity for any output of `parse`. Emits `preamble` verbatim, then each `## Name\n<content>` in order.
   - `validate_for_write(parsed: ParsedBody) -> None` — **strict**, raises `BodyValidationError("body_missing_required_section: title")` if `parsed.title is None or empty`, `…goal` if `parsed.goal_first_paragraph is None or empty`. Called by every write path before `update_epic_body`.
   - `outline(parsed: ParsedBody) -> dict` — `{title, sections: [{name, line_count, subheadings}], total_lines}` for the outline log.
2. **Heading rules** (spec §503–514):
   - Section delimiters match `^##\s+(.+?)\s*$` at top level only. Level-3+ headings stay inside their parent section as content.
   - **Code-fence guard:** track ``` and ~~~ fences during the scan; `##` inside a fenced block is content, not a delimiter. Indented code blocks aren't tracked (rare in this corpus; document the gap inline).
   - Section names are case-sensitive; whitespace stripped from heading text.
3. **Section operations** (`replace_section`, `append_to_section`, `add_section(position='after:Foo'|'before:Foo'|'start'|'end')`, `remove_section`, `rename_section`, `reorder(new_order)`): pure functions on `ParsedBody`, return new `ParsedBody`. Each raises typed errors (`SectionNotFound`, `SectionExists`, `InvalidPosition`) the tool layer maps to JSON error payloads.
   - `_preamble` is addressable as a section name across these ops: `replace_section('_preamble', new_text)` overwrites the entire preamble (so `replace_section('_preamble', '# New Title\n')` updates the title; this is the spec §2606 path). `append_to_section('_preamble', …)` appends. `remove_section('_preamble')` clears the preamble to empty string. `rename_section` from/to `_preamble` is rejected with `InvalidPosition` (the preamble is a structural slot, not a renamable section).
4. **Diff helpers:**
   - `compute_diff(old: str, new: str) -> str` — `''.join(difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True), fromfile='before', tofile='after', n=3))`.
   - `diffs_equivalent(a: str, b: str) -> bool` — normalises both sides per spec §494: `\r\n → \n`, strip trailing whitespace per line, drop trailing blank lines, then byte-equal compare.
5. **No third-party deps** beyond stdlib (`difflib`, `re`). No imports of Store, ports, or tool_kit — keep this module pure.

### Step 5: Default template + checklist seed (`agent_kit/templates.py`)
**Scope:** Small
1. **`DEFAULT_BODY_TEMPLATE(title, goal) -> str`** — emits the six-section design-doc skeleton (`# {title}\n\n## Goal\n\n{goal}\n\n## Principles\n\n## Context\n\n## Key Decisions\n\n## Open Questions\n\n## Deliverable\n`).
2. **`DEFAULT_CHECKLIST_SEED: list[str]`** — the 18 items from spec §634, all `source='default_seed'`, `status='open'`, positions 1–18.
3. **No adaptation logic** in v1 (settled decision SD-003); the bot adapts via post-create `edit_epic` calls.

### Step 6: Parser unit tests (`tests/test_body_parser.py`)
**Scope:** Medium
1. **Round-trip identity** for ≥6 fixtures: preamble-only (no `##`), single section, six-section design-doc, body with `### Authentication` sub-headings, body with a fenced code block containing `## Step 1`, body with non-empty preamble before first `##`. Assert `serialize(parse(b)) == b`.
2. **Section ops** (each variant): only the targeted section changes; every other section's serialised form is byte-equal.
3. **`_preamble` covers the title:** `replace_section(parse(body), '_preamble', '# New Title\n')` round-trips through `parse` to a body whose `parsed.title == 'New Title'`. Removing the `# Title` line via `replace_section('_preamble', '')` round-trips to `parsed.title is None`, and `validate_for_write` raises `body_missing_required_section: title` on the result.
4. **Lenient parse:** parsing `''`, `'just text\n'`, `'## Goal\n\ngoal\n'` (no title), `'# Title\n'` (no Goal section), `'# Title\n\n## NotGoal\n\nx\n'` (no `## Goal`) all return `ParsedBody` without raising. `validate_for_write` rejects each with the appropriate `body_missing_required_section` error.
5. **Code-fence guard:** body with ` ```\n## Inside\n``` ` parses as a single preamble (no section split).
6. **Diff equivalence:** `diffs_equivalent` returns True when only difference is `\r\n` vs `\n`, trailing spaces, or trailing blank lines; False on real content delta.

---

## Phase 3: Store surface for epics, checklist, events

### Step 7: Extend `Store` protocol (`agent_kit/ports.py`)
**Scope:** Medium
1. **Add** typed methods (Protocol + both adapters):
   - `create_epic(*, title, goal, body, state='shaping') -> JSONDict` — single-row INSERT. Caller is the tool layer, which has already parsed and validated.
   - `load_epic(epic_id) -> JSONDict | None`
   - `update_epic(epic_id, **changes) -> JSONDict` — guarded UPDATE via the existing `_update` helper, restricted to a new `_EPIC_COLUMNS = {'title', 'goal', 'body', 'state', 'last_edited_at', 'last_active_at', 'planned_at'}` set. Used by `edit_epic` and `revert` for body+title+goal updates.
   - `seed_checklist(epic_id, items: list[dict]) -> list[JSONDict]` — bulk INSERT.
   - `list_checklist_items(epic_id, *, status: str | list[str] | None = None) -> list[JSONDict]`
   - `update_checklist_item(item_id, **changes) -> JSONDict` — guarded by `_CHECKLIST_COLUMNS = {'content', 'status', 'position', 'skip_reason', 'superseded_by_item_id', 'completed_at'}`.
   - `add_checklist_items(epic_id, items, start_position) -> list[JSONDict]`
   - `delete_checklist_items(item_ids) -> int`
   - `replace_checklist(epic_id, items) -> list[JSONDict]` — used by revert: DELETE all rows for `epic_id` then bulk INSERT from snapshot. Single transaction by virtue of the wrapping `store.transaction()`.
   - `record_epic_event(*, epic_id, transaction_id, event_type, summary, prior_state, turn_id) -> JSONDict` — append-only INSERT, no update path.
   - `list_epic_events(epic_id, *, since=None, until=None, kinds=None, limit=None) -> list[JSONDict]` — ordered `(occurred_at, id) ASC`. `get_history` reverses for display.
   - `latest_transaction_id(epic_id) -> str | None`
   - `events_by_transaction(transaction_id) -> list[JSONDict]`
   - `list_recent_turns(*, n=10, epic_id=None) -> list[JSONDict]` — `bot_turns` ordered `started_at DESC LIMIT n`, optional epic filter.
   - `search_tool_calls_by(*, tool_name=None, epic_id=None, since=None, limit=20) -> list[JSONDict]` — `tool_calls` joined to `bot_turns` for the epic filter.
   - `update_message(...)` already exists; we'll reuse it from the loop bootstrap (Step 14) to retro-stamp `epic_id` on the inbound message.
   - `update_turn(...)` already exists; reused to retro-stamp `epic_id` on the bot_turns row.

### Step 8: Implement on `SupabaseStore` (`agent_kit/store/supabase.py`)
**Scope:** Medium
1. **Mirror** the protocol additions with concrete SQL using the existing `_normalize`/`_json` helpers and `_new_id` (prefixes: `'epic'`, `'check'`, `'evt'`).
2. **Add** module-level constants `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` next to existing `_MESSAGE_COLUMNS`/`_TURN_COLUMNS`/`_IMAGE_COLUMNS`. Wire `update_epic` and `update_checklist_item` through the existing `self._update` helper for column safety.
3. **Update `_TURN_COLUMNS`** to include `'epic_id'` so the loop bootstrap (Step 14) can retro-stamp the turn after `create_epic` fires.
4. **Update `_MESSAGE_COLUMNS`** to include `'epic_id'` for the same reason.

### Step 9: Implement on `SQLiteStore` (`agent_kit/store/sqlite.py`)
**Scope:** Medium
1. **Mirror** the same methods, the same `_EPIC_COLUMNS`/`_CHECKLIST_COLUMNS` constants, and the same `epic_id` additions to existing message/turn column sets.
2. **Add** `'prior_state'` to `_JSON_COLUMNS`.

### Step 10: Extend the contract test (`tests/store_contract.py`)
**Scope:** Small
1. **Add** a tail block to `run_store_contract` that exercises the new surface against `epic_1`: create a second epic via `store.create_epic`, seed checklist, append events with `transaction_id`s, list/filter events, query `latest_transaction_id`, and verify ordering. Both Supabase and SQLite contract tests pick this up automatically.

---

## Phase 4: Tools — `create_epic`, `edit_epic`, `revert`, `render_epic`, reads

### Step 11: Editorial write tools (`agent_kit/tools/editorial.py`)
**Scope:** Large
1. **Register each tool** via `@register_tool` with explicit JSON schemas and `operation_kind='write'`.
2. **`create_epic(context, title, goal)`** —
   - Build body via `templates.DEFAULT_BODY_TEMPLATE(title, goal)`.
   - `parsed = body.parse(rendered)`; `body.validate_for_write(parsed)` — on `BodyValidationError`, return `{"error": "body_missing_required_section", "field": …}` (don't raise; the model needs to read the message).
   - Inside `store.transaction()`:
     - `epic = store.create_epic(title=parsed.title, goal=parsed.goal_first_paragraph, body=rendered, state='shaping')` — title and goal come **only** from `parsed.*`, never from raw args (correctness-3).
     - `store.seed_checklist(epic['id'], DEFAULT_CHECKLIST_SEED)`.
     - `store.record_epic_event(epic_id=epic['id'], transaction_id=uuid4().hex, event_type='created', summary='Epic created with default design-doc template', prior_state=None, turn_id=context.turn_id)`.
     - **Bootstrap retro-stamp** (when context.metadata['epic_id'] was None): `store.update_message(context.metadata['inbound_message_id'], epic_id=epic['id'])` and `store.update_turn(context.turn_id, epic_id=epic['id'])`. Set `context.metadata['epic_id'] = epic['id']` for downstream tools in the same turn.
   - Return `{"epic_id", "title": parsed.title, "goal": parsed.goal_first_paragraph, "section_names": [...], "checklist_count": 18, "transaction_id"}`.
3. **`edit_epic(context, epic_id, changes, change_summary, expected_diff?)`** —
   - **Reject** unsupported keys: `changes.sprints` → `{"error": "not_yet_supported", "field": "sprints"}`; `changes.state` → `{"error": "not_yet_supported", "field": "state"}`; `changes.meta` → `{"error": "meta_not_supported", "hint": "title and goal are derived from body; edit body.sections._preamble for title or body.sections.Goal for goal"}` (scope-2).
   - **Reject** mixed body ops: at most one of `new_content | sections | append | remove_sections | rename_section | reorder` per call → `{"error": "body_op_conflict"}`.
   - **Body path:** `old = store.load_epic(epic_id)['body']`; `parsed = body.parse(old)`; apply the requested op; serialise → `new_body`. `body.validate_for_write(new_parsed)`. Compute `actual_diff = body.compute_diff(old, new_body)`. If `expected_diff` provided and `not body.diffs_equivalent(expected_diff, actual_diff)`, return `{"error": "expected_diff_mismatch", "actual_diff": actual_diff}` and **do not write**.
   - **Checklist path:** apply `add` (positions auto-assigned to `max(existing.position) + 1` if absent; else honour and shift), `update` (per-item, only `_CHECKLIST_COLUMNS`-allowed fields), `remove` (delete by id). Capture pre-op snapshot for the event.
   - **Inside one `store.transaction()`** with `transaction_id = uuid4().hex`:
     - Body: `store.update_epic(epic_id, body=new_body, title=new_parsed.title, goal=new_parsed.goal_first_paragraph, last_edited_at=now())` + `store.record_epic_event(event_type='body_edit', prior_state={'body': old, 'title': old_title, 'goal': old_goal}, summary=change_summary, transaction_id, turn_id=context.turn_id)`.
     - Checklist: apply per-item ops; `store.record_epic_event(event_type='checklist_change', prior_state={'items': [...full snapshot...]}, summary=change_summary, transaction_id, turn_id=context.turn_id)`.
   - Return `{"transaction_id", "diff": actual_diff_or_empty, "section_names": [...], "change_summary"}`.
4. **`revert(context, epic_id, event_id?=None)`** —
   - Resolve target events: no `event_id` → fetch `events_by_transaction(latest_transaction_id(epic_id))`. With `event_id` → fetch the event, then all events sharing its `transaction_id` (spec §1399).
   - **Capture pre-revert state** for the new event's `prior_state`: `{'body': current_body, 'title': current_title, 'goal': current_goal, 'checklist': [...current full snapshot...], 'reverted_transaction_id': txn, 'reverted_event_ids': [e.id for e in target_events]}`. This lets backward replay across this revert reconstruct correctly (FLAG-003, correctness-2).
   - Apply each target event's `prior_state` in reverse-occurred order: `body_edit` → `store.update_epic(epic_id, body=…, title=…, goal=…)`; `checklist_change` → `store.replace_checklist(epic_id, prior_items)`. (Other event types in the transaction — e.g., a future `state_change` — are no-ops in Sprint 2a; bot won't trigger them.)
   - Append a new `reverted_to` event with the captured pre-revert `prior_state` and a fresh `transaction_id`. The event is itself revertible because its `prior_state` carries the full pre-revert snapshot.
   - Return `{"transaction_id", "reverted_event_count", "summary": f'Reverted transaction {txn}'}`.
5. **`render_epic(context, epic_id, format='markdown')`** — `'markdown'` returns the body as-is (image-reference resolution is a Sprint 6 no-op). `'html'` → `{"error": "not_yet_supported"}`.

### Step 12: Editorial read tools (`agent_kit/tools/editorial_reads.py`)
**Scope:** Medium
1. **Register** each tool with **`operation_kind='read'`** (scope-1).
2. **`get_epic(epic_id, sections=None)`** — `parsed = body.parse(epic['body'])`. Return `{title: parsed.title, goal: parsed.goal_first_paragraph, body_full: epic['body'] if sections is None else None, sections: {name: content, …} when sections is supplied, section_names: [s.name for s in parsed.sections], state}`. Lenient parse means malformed bodies still load.
3. **`get_section_names(epic_id)`** — return `[s.name for s in body.parse(epic['body']).sections]`.
4. **`get_history(epic_id, kind=None, since=None)`** — `store.list_epic_events(...)` reversed (most recent first), optionally filtered.
5. **`get_self_understanding(epic_id)`** — return `{goal, state, open_checklist_count, section_names, recent_events: last 3}`. Document inline that the spec §1068 7-section structure (recent decisions, code refs, second opinions, etc.) lights up incrementally as later sprints land their tables.
6. **`get_epic_at_time(epic_id, timestamp)`** — backward replay from current state:
   - Load current `body, checklist`.
   - Fetch `list_epic_events(epic_id)` (full ascending list).
   - Walk the events whose `occurred_at > timestamp` in **descending** order; for each, undo using `prior_state`:
     - `body_edit`: `body = prior_state['body']`.
     - `checklist_change`: `checklist = prior_state['items']`.
     - `created`: this is the earliest possible state; if we're rolling past it, return empty/None body+checklist (caller asked for a time before the epic existed).
     - `reverted_to`: undo by restoring `prior_state['body']` and `prior_state['checklist']` (the captured pre-revert snapshot — Step 11.4 makes this work).
     - Other event_types (sprints, state, code_referenced, etc., none of which fire in Sprint 2a) fall through with a logged warning.
   - Tied timestamps order by `(occurred_at, id) ASC`; when walking descending, reverse that.
   - Return `{body, checklist, reconstructed_at: timestamp}`.
7. **`get_recent_turns(n=10, epic_id=None)`** — `store.list_recent_turns(...)`; for each turn, attach `change_summary` aggregated from `epic_events` rows with that `turn_id` (single `WHERE turn_id IN (...)` query joined client-side).
8. **`search_tool_calls(tool_name=None, epic_id=None, since=None, limit=20)`** — delegates to `store.search_tool_calls_by(...)`.

### Step 13: Register the tools in the loop import path (`agent_kit/loop.py:16`)
**Scope:** Small
1. **Add** `import agent_kit.tools.editorial  # noqa: F401` and `import agent_kit.tools.editorial_reads  # noqa: F401` next to existing `communication`/`images` imports so tools auto-register.

---

## Phase 5: Loop bootstrap + turn-end outline log

### Step 14: No-epic turn mode (`agent_kit/loop.py:25` and surrounding)
**Scope:** Medium
1. **Make `epic_id` Optional** on `run_turn` and propagate through downstream code paths:
   - When `epic_id is None`: skip `store.acquire_epic_lock` entirely. Skip the lock-contended early return.
   - Inbound message creation (`agent_kit/loop.py:79–85`): `epic_id=None` is already nullable (`messages.epic_id` is FK with `ON DELETE SET NULL`, NULL allowed). Capture the resulting `inbound_message_id` in `context.metadata['inbound_message_id']` so `create_epic` can retro-stamp.
   - `store.create_turn(epic_id=None, …)` is allowed (`bot_turns.epic_id` already nullable). The turn row carries NULL until `create_epic` retro-stamps it.
   - `load_hot_context` is currently `load_hot_context(epic_id)` and dereferences `epic`; in no-epic mode, skip the call and pass `hot_context = {"epic": None, "recent_messages": [], "recent_tool_calls": []}` to the model.
   - After every tool invocation, if `context.metadata.get('epic_id')` flipped from None to a real id (set by `create_epic`'s post-commit hook in Step 11.2), the loop's lock-release path must skip — there was no lock to release.
2. **CLI plumbing (`arnold/cli.py`):** allow invoking with no `--epic-id` (or an explicit `--no-epic` flag); pass `epic_id=None` to `run_turn`. The system prompt for that branch should hint "no active epic — call `create_epic(title, goal)` first if the user is starting one."
3. **Existing callers** (`tests/test_run_turn.py`) keep passing an `epic_id` and continue to work unchanged. The no-epic path is purely additive.

### Step 15: Turn-end `epic_outline` log (`agent_kit/loop.py`)
**Scope:** Small
1. **At the end of `run_turn`**, after `update_turn(status='completed', …)` and before envelope return: if `context.metadata.get('epic_id')` is set AND any tool_call this turn had `tool_name in {'create_epic','edit_epic','revert'}` (walk `events`), then `parsed = body.parse(store.load_epic(epic_id)['body'])`, `details = body.outline(parsed)`, and call `log(store, 'info', 'application', 'epic_outline', f"Epic outline: {parsed.title or '(untitled)'}", details=details, turn_id=turn['id'], epic_id=epic_id)`.
2. **Failure paths** (`status='failed'`) skip the log. Pure-read turns and turns that never created an epic skip the log.

---

## Phase 6: Integration test + regression verification

### Step 16: 10-turn fixture (`tests/test_editorial_loop.py`)
**Scope:** Medium
1. **Use** `FakeModel(script=…)` (per `tests/test_run_turn.py:8`) and `SQLiteStore` with a deterministic 10-turn script:
   - Turn 1: `run_turn(epic_id=None, input='Make me an auth flow design epic')` → tool_use `create_epic(title='Auth flow design', goal='Decide on auth provider and token storage')` → final text.
   - Turns 2–9: `run_turn(epic_id=<the new id>)` with `edit_epic` calls hitting **all six default sections** at least once via `sections` ops, plus a `_preamble` replace that updates the title (asserts `epics.title` reflects the new value), plus an `append`, plus a `checklist.update` marking 3 items done. Include one `expected_diff` round-trip (matching) and one mismatch turn (asserts DB unchanged).
   - Turn 10: `revert` (most recent transaction) followed by `send_message`.
2. **Assertions** — one per spec §131–142 acceptance criterion plus the critique-driven additions:
   - After Turn 1: `epics` row exists with `title='Auth flow design'`, `goal='Decide on auth provider and token storage'`; 18 `checklist_items` with `source='default_seed'`; one `created` event; the inbound message and bot_turn both have `epic_id` retro-stamped.
   - After all turns: every default section present; section-only edits leave other sections byte-identical (verified by re-parsing prior_state captured in `body_edit` events).
   - Whole-body `new_content` turn: `body_edit` event captured prior body; manual `revert(epic_id, event_id=that_event)` then `load_epic` returns prior body byte-equal.
   - "revert that" turn: most-recent transaction undone; new `reverted_to` event present; `prior_state` contains body + checklist snapshots (FLAG-003 verification).
   - `expected_diff` mismatch turn: tool result has `error='expected_diff_mismatch'`; epics + checklist unchanged.
   - `expected_diff` match turn: writes commit normally.
   - **Title-via-preamble turn:** before/after `epics.title` differs; the same transaction's `body_edit` event captured the old title in `prior_state`.
   - `get_epic_at_time(epic_id, T_after_turn_5)` returns body + checklist matching a hand-rolled replay computed inside the test.
   - `get_epic_at_time(epic_id, T_just_before_revert)` returns body+checklist as it was right before the revert (verifies FLAG-003 fix end-to-end).
   - `get_recent_turns(5)` returns 5 turns most-recent-first.
   - `search_tool_calls(tool_name='edit_epic', epic_id=…)` returns ≥3 rows.
   - One `system_logs` row per touching turn with `event_type='epic_outline'`, `category='application'`, and `details.sections` containing all six default headings (after the relevant turns).
   - `tool_calls.operation_kind` for `get_epic`, `get_section_names`, `get_history`, etc. is `'read'`; for `create_epic`, `edit_epic`, `revert`, `render_epic` is `'write'` (scope-1 verification).
   - Calling `edit_epic(changes={'meta': {'title': 'X'}})` returns `error='meta_not_supported'` (scope-2 verification).

### Step 17: Run the targeted tests, then full regression
**Scope:** Small
1. `pytest tests/test_body_parser.py -x`.
2. `pytest tests/test_sqlite_store.py tests/test_sqlite_store_v1b.py -x` to confirm the new contract additions pass.
3. `pytest tests/test_editorial_loop.py -x`.
4. `pytest -x` for the full suite (no Sprint 1a/1b regression).
5. **Optional:** `SUPABASE_TEST_DB_URL=… pytest tests/test_supabase_store.py` if a local Supabase is available.

---

## Execution Order

1. Schema first (Phase 1) — migrations unblock everything.
2. Body parser + templates with their unit tests (Phase 2). Pure code, fastest feedback. Land lenient parse + strict validate split before building anything that depends on it.
3. Store extensions (Phase 3) — column-safety constants + new methods, exercised through the contract test.
4. Tools (Phase 4) — depends on parser + store. Write tools first (`create_epic`, `edit_epic`, `revert`, `render_epic`), then reads.
5. Loop bootstrap + outline log (Phase 5) — depends on tools. Bootstrap first (FLAG-001) so `create_epic` is callable; then outline log.
6. Integration fixture (Phase 6) — proves the whole pipeline + every critique fix end-to-end.

## Validation Order

1. `pytest tests/test_body_parser.py` — fastest feedback on parser edge cases (lenient/strict split, `_preamble` title).
2. Contract tests (`tests/test_sqlite_store.py`, `tests/test_supabase_store.py` when DB available) — confirms new Store surface is consistent across adapters and column-safety holds.
3. `pytest tests/test_editorial_loop.py` — the 10-turn integration with bootstrap, time-travel-across-revert, `_preamble`-title, and `meta_not_supported` assertions.
4. `pytest -x` — full regression.


        Current plan metadata:
        {
  "version": 2,
  "timestamp": "2026-04-30T05:29:21Z",
  "hash": "sha256:a4f9c4cd1cf6af5e87ed6539a12c6f6715dab0ac1709e41c7a3f49d3a926ae78",
  "changes_summary": "Rev 2 addresses all 12 open critique flags by editing the existing six-phase structure rather than restructuring. Key changes: (1) added a no-epic mode to `run_turn` (epic_id=None), with `create_epic` retro-stamping the inbound message and bot_turn (FLAG-001/issue_hints-1/callers); (2) split parser into lenient `parse()` + strict `validate_for_write()` so reads/time-travel survive malformed bodies (FLAG-002/correctness-1); (3) redefined `_preamble` to include the `# Title` line per spec \u00a72606, making `replace_section('_preamble', ...)` the canonical title-edit path (issue_hints-2); (4) `reverted_to` events now snapshot full pre-revert body + checklist in `prior_state` so backward replay works across reverts (FLAG-003/correctness-2); (5) `create_epic` writes `epics.title`/`goal` exclusively from parsed values, never raw args (correctness-3); (6) read tools register with `operation_kind='read'` (scope-1); (7) `edit_epic.changes.meta` is explicitly rejected with `meta_not_supported` and a hint to use body sections (scope-2); (8) added `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` to both Store adapters and extended `_MESSAGE_COLUMNS`/`_TURN_COLUMNS` to allow the bootstrap `epic_id` retro-stamp (all_locations). Integration test gained explicit assertions for each critique fix (title-via-preamble, time-travel-across-revert, meta_not_supported, operation_kind values).",
  "flags_addressed": [
    {
      "id": "FLAG-001",
      "resolution": "addressed",
      "reason": "run_turn now accepts epic_id=None; lock acquisition and load_hot_context are skipped; create_epic retro-stamps the inbound message and bot_turn rows. CLI gets a no-epic invocation path. Integration test exercises the bootstrap turn end-to-end."
    },
    {
      "id": "FLAG-002",
      "resolution": "addressed",
      "reason": "Parser split: parse() is now explicitly lenient and never raises; validate_for_write() is strict and called only by write paths. Round-trip fixtures and time-travel/read tools exercise the lenient path."
    },
    {
      "id": "FLAG-003",
      "resolution": "addressed",
      "reason": "revert now captures the full pre-revert body + checklist snapshot in the new reverted_to event's prior_state, so backward replay across a revert restores the immediately-pre-revert state. Integration test asserts get_epic_at_time(T_just_before_revert) matches the captured snapshot."
    },
    {
      "id": "issue_hints-1",
      "resolution": "addressed",
      "reason": "Same fix as FLAG-001: run_turn(epic_id=None) is a first-class mode and create_epic retro-stamps the message + turn after commit."
    },
    {
      "id": "issue_hints-2",
      "resolution": "addressed",
      "reason": "_preamble is redefined to include the # Title line and any leading text up to the first ## heading, matching spec \u00a72606. replace_section('_preamble', '# New Title\\n') is the canonical title-edit path; rename_section to/from _preamble is rejected. Integration test exercises the title-via-preamble case."
    },
    {
      "id": "correctness-1",
      "resolution": "addressed",
      "reason": "Same fix as FLAG-002: parse() is lenient, validate_for_write() is strict and only used on writes. Read tools and get_epic_at_time work against legacy/malformed bodies without raising."
    },
    {
      "id": "correctness-2",
      "resolution": "addressed",
      "reason": "Same fix as FLAG-003: reverted_to event prior_state now contains the full pre-revert state."
    },
    {
      "id": "correctness-3",
      "resolution": "addressed",
      "reason": "create_epic now passes parsed.title and parsed.goal_first_paragraph (not the raw arguments) to store.create_epic. The body parser is the only writer of epics.title and epics.goal, matching spec \u00a71314\u20131316."
    },
    {
      "id": "scope-1",
      "resolution": "addressed",
      "reason": "All read tools (get_epic, get_section_names, get_history, get_self_understanding, get_epic_at_time, get_recent_turns, search_tool_calls) register with operation_kind='read'. Integration test asserts correct operation_kind in tool_calls rows."
    },
    {
      "id": "scope-2",
      "resolution": "addressed",
      "reason": "edit_epic explicitly rejects changes.meta with error='meta_not_supported' and a hint pointing to body.sections._preamble (for title) or body.sections.Goal (for goal). Asserted in the integration test."
    },
    {
      "id": "all_locations",
      "resolution": "addressed",
      "reason": "Both adapters gain module-level _EPIC_COLUMNS and _CHECKLIST_COLUMNS constants wired through the existing _update helper, mirroring _MESSAGE_COLUMNS/_TURN_COLUMNS/_IMAGE_COLUMNS. _MESSAGE_COLUMNS and _TURN_COLUMNS are extended to include 'epic_id' so the bootstrap retro-stamp uses guarded updates."
    },
    {
      "id": "callers",
      "resolution": "addressed",
      "reason": "Same fix as FLAG-001: run_turn callers can pass epic_id=None for the bootstrap; existing callers (tests/test_run_turn.py) keep passing an epic_id and remain unchanged. The no-epic path is purely additive."
    }
  ],
  "questions": [
    "Should the no-epic bootstrap path also handle 'user typed a question that doesn't warrant creating an epic' (e.g., greetings, meta-questions)? Plan currently assumes the bot either calls create_epic or sends a message-only response; a turn that ends with epic_id still NULL is treated as a successful no-op (epic_outline log skipped). Is that acceptable, or should we reject turn completion if epic_id is still NULL after the model loop?",
    "spec test #7 (planning-bot-spec.md:2606) references a body_version column that does not exist in the current schema. Plan defers introducing body_version, covering the audit/title-update semantics another way. Confirm body_version is fine to skip in Sprint 2a, or pull it forward as a one-line column add in migration 004?",
    "get_epic_at_time across reverts: the plan handles the simple case (body+checklist snapshot in reverted_to.prior_state lets backward replay restore the immediate pre-revert state). Does the spec require correct reconstruction at timestamps that fall *between* a body_edit event and a revert that undoes it (e.g., T was after the edit but before the revert)? Backward replay handles that naturally; flagging in case the desired semantics differ."
  ],
  "success_criteria": [
    {
      "criterion": "Postgres migration 004 and SQLite migration 004 create checklist_items and epic_events with the columns, CHECK constraints, FK ON DELETE behaviour, and indexes specified in spec \u00a71322 and \u00a71381.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "body.parse() is lenient and returns a ParsedBody for empty input, plain-text input, bodies with no '##' headings, bodies missing '# Title', and bodies missing '## Goal' \u2014 without raising. Integration tools (get_epic, get_epic_at_time) work against these inputs.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "body.validate_for_write() raises BodyValidationError('body_missing_required_section: title') when parsed.title is None or empty, and 'body_missing_required_section: goal' when parsed.goal_first_paragraph is None or empty. Write tools surface this as a structured tool result error.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Body parser round-trip identity holds: serialize(parse(body)) == body for \u22656 fixture bodies including preamble-only (no '##'), single section, full design-doc template, sub-headings, fenced code containing '##', and a body with non-empty preamble before the first section.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "_preamble section addressing covers the '# Title' line per spec \u00a72606: replace_section(parsed, '_preamble', '# New Title\\n') round-trips to ParsedBody with title='New Title'; replace_section(parsed, '_preamble', '') round-trips to title=None and validate_for_write rejects it with body_missing_required_section: title.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "create_epic creates an epics row whose title and goal columns equal parse(rendered_template).title and .goal_first_paragraph respectively (not the raw input arguments), seeds 18 default checklist items with status='open' and source='default_seed', and writes one 'created' epic_event sharing a transaction_id.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "run_turn(epic_id=None, input=...) executes without acquiring an epic_locks row, creates an inbound message and bot_turn with epic_id=NULL, and \u2014 when create_epic fires within the turn \u2014 retro-stamps both rows with the new epic_id by the time the turn completes.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "edit_epic body section operations leave every non-targeted section byte-identical (verified by parsing prior_state captured in the body_edit event and comparing every other section's serialised form).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "edit_epic with expected_diff that does not match (after \\n + trailing-whitespace + trailing-blank-line normalisation) refuses to commit, returns the actual diff, and leaves epics.body, title, goal, and checklist_items untouched.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "edit_epic with expected_diff that matches commits normally and writes one event per affected family (body_edit, checklist_change) sharing a single transaction_id.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "edit_epic rejects changes.meta with error='meta_not_supported' and a hint string referencing body.sections._preamble or body.sections.Goal; epics row is unchanged.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "revert(epic_id) with no event_id undoes the entire most-recent transaction (body, title, goal, and checklist together) and appends a 'reverted_to' event whose prior_state captures the full pre-revert body and checklist; the resulting body is byte-equal to the pre-edit body.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "get_epic_at_time(epic_id, T) returns body and checklist state equal to what was committed at the most recent event with occurred_at <= T \u2014 including timestamps that fall just before a revert (verifies reverted_to.prior_state captures enough state for backward replay).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "get_recent_turns(5) returns the 5 most-recent bot_turns rows (most-recent first) with summaries; search_tool_calls(tool_name='edit_epic', epic_id=X) returns every edit_epic call against epic X with arguments and timestamps.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "All read tools (get_epic, get_section_names, get_history, get_self_understanding, get_epic_at_time, get_recent_turns, search_tool_calls) record operation_kind='read' in tool_calls; all write tools (create_epic, edit_epic, revert, render_epic) record operation_kind='write'.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "After every turn whose tool_calls include create_epic, edit_epic, or revert, exactly one system_logs row exists with category='application', event_type='epic_outline', turn_id=<that turn>, and details containing title plus a sections array with name + line_count for every section in the body.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "10-turn FakeModel-driven integration fixture in tests/test_editorial_loop.py runs end-to-end starting from epic_id=None, exercises all six default sections, exercises both expected_diff match and mismatch, exercises title editing via _preamble, exercises revert with backward replay across the revert, and asserts every Sprint 2a acceptance criterion in spec \u00a7131\u2013142.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "All pre-existing tests in tests/ continue to pass (no regression in Sprint 1a/1b functionality, including resident-mode test_resident*, test_discord_*, and test_run_turn variants).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Both Store adapters expose _EPIC_COLUMNS and _CHECKLIST_COLUMNS allowed-column sets and route update_epic / update_checklist_item through the existing _update helper, matching the _MESSAGE_COLUMNS / _TURN_COLUMNS / _IMAGE_COLUMNS pattern. _MESSAGE_COLUMNS and _TURN_COLUMNS include 'epic_id' so the bootstrap retro-stamp passes column safety.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Body parser and section-op modules stay focused: the public surface is parse, serialize, validate_for_write, the section ops, compute_diff, diffs_equivalent, outline. No tool-layer or Store imports leak into agent_kit/body.py.",
      "priority": "should",
      "requires": [
        "read_files",
        "subjective_judgment"
      ]
    },
    {
      "criterion": "edit_epic rejects requests mixing two body op flavours (e.g. new_content + sections) with error='body_op_conflict' rather than silently picking one.",
      "priority": "should",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "agent_kit/body.py stays under ~450 lines and has no third-party dependencies beyond the standard library (difflib, re).",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    }
  ],
  "assumptions": [
    "Sprint 2a stays invocation-mode only; no resident-mode behaviour changes.",
    "Sprints, sprint_items, codebases, code_artifacts, feedback, second_opinions, and image generation are out of scope. edit_epic.changes.sprints and changes.state return not_yet_supported.",
    "edit_epic.changes.meta is explicitly rejected with meta_not_supported and a hint to edit via body.sections._preamble (for title) or body.sections.Goal (for goal); title and goal are derived columns whose only writer is the body parser.",
    "_preamble is the raw text from byte 0 up to (but not including) the first ## line, INCLUDING the # Title line and any blank/leading lines before the first section. replace_section('_preamble', '# New Title\\n') is the canonical title-edit path per spec \u00a72606. rename_section from/to '_preamble' is rejected.",
    "parse() is lenient and never raises on missing #/## headings, malformed input, or empty bodies. validate_for_write() is the only place that raises body_missing_required_section, and is called only on write paths.",
    "Default body template ships with one variant (design-doc); create_epic accepts (title, goal) and constructs the body from the template, then derives epics.title and epics.goal from parse() output \u2014 raw args are template inputs only.",
    "Default checklist seed is unconditional (all 18 items); adaptation lives in the bot's prompt/decisions, not server-side at create time.",
    "expected_diff equivalence: line endings normalised to \\n, per-line trailing whitespace stripped, trailing blank lines dropped, then byte-equal compare.",
    "render_epic supports format='markdown' only in v1; format='html' returns not_yet_supported. Image-reference resolution is a Sprint 6 no-op.",
    "epic_outline log fires on any turn whose tool_calls include create_epic, edit_epic, or revert; pure-read turns and failed turns skip the log.",
    "Single-writer concurrency via existing epic_locks + per-edit_epic store.transaction is sufficient. The new no-epic mode skips lock acquisition entirely (no lock contention possible before an epic exists).",
    "run_turn gains an Optional epic_id parameter (None = no-epic mode). Existing callers in tests/test_run_turn.py and resident mode keep passing a concrete epic_id and remain unchanged. Bootstrap retro-stamps the inbound message and bot_turn with the new epic_id once create_epic commits.",
    "spec test #7 (planning-bot-spec.md:2606) references body_version, but that column does not exist in the current schema; we cover the title/body sync semantics (title updates atomically with body, audit captures the change) without introducing body_version. Adding the column is deferred unless a later sprint requires it.",
    "All read tools register with operation_kind='read'; write tools register with operation_kind='write'. The default ('write') is overridden explicitly so audit semantics are correct.",
    "The existing megaplan/ directory is harness state and is left untouched; CLAUDE.md's prohibition applies to creating one, not the existing path."
  ],
  "delta_from_previous_percent": 60.45,
  "structure_warnings": []
}

        Gate summary:
        {
  "passed": false,
  "criteria_check": {
    "count": 22,
    "items": [
      {
        "criterion": "Postgres migration 004 and SQLite migration 004 create checklist_items and epic_events with the columns, CHECK constraints, FK ON DELETE behaviour, and indexes specified in spec \u00a71322 and \u00a71381.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "body.parse() is lenient and returns a ParsedBody for empty input, plain-text input, bodies with no '##' headings, bodies missing '# Title', and bodies missing '## Goal' \u2014 without raising. Integration tools (get_epic, get_epic_at_time) work against these inputs.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "body.validate_for_write() raises BodyValidationError('body_missing_required_section: title') when parsed.title is None or empty, and 'body_missing_required_section: goal' when parsed.goal_first_paragraph is None or empty. Write tools surface this as a structured tool result error.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "Body parser round-trip identity holds: serialize(parse(body)) == body for \u22656 fixture bodies including preamble-only (no '##'), single section, full design-doc template, sub-headings, fenced code containing '##', and a body with non-empty preamble before the first section.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "_preamble section addressing covers the '# Title' line per spec \u00a72606: replace_section(parsed, '_preamble', '# New Title\\n') round-trips to ParsedBody with title='New Title'; replace_section(parsed, '_preamble', '') round-trips to title=None and validate_for_write rejects it with body_missing_required_section: title.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "create_epic creates an epics row whose title and goal columns equal parse(rendered_template).title and .goal_first_paragraph respectively (not the raw input arguments), seeds 18 default checklist items with status='open' and source='default_seed', and writes one 'created' epic_event sharing a transaction_id.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "run_turn(epic_id=None, input=...) executes without acquiring an epic_locks row, creates an inbound message and bot_turn with epic_id=NULL, and \u2014 when create_epic fires within the turn \u2014 retro-stamps both rows with the new epic_id by the time the turn completes.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "edit_epic body section operations leave every non-targeted section byte-identical (verified by parsing prior_state captured in the body_edit event and comparing every other section's serialised form).",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "edit_epic with expected_diff that does not match (after \\n + trailing-whitespace + trailing-blank-line normalisation) refuses to commit, returns the actual diff, and leaves epics.body, title, goal, and checklist_items untouched.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "edit_epic with expected_diff that matches commits normally and writes one event per affected family (body_edit, checklist_change) sharing a single transaction_id.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "edit_epic rejects changes.meta with error='meta_not_supported' and a hint string referencing body.sections._preamble or body.sections.Goal; epics row is unchanged.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "revert(epic_id) with no event_id undoes the entire most-recent transaction (body, title, goal, and checklist together) and appends a 'reverted_to' event whose prior_state captures the full pre-revert body and checklist; the resulting body is byte-equal to the pre-edit body.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "get_epic_at_time(epic_id, T) returns body and checklist state equal to what was committed at the most recent event with occurred_at <= T \u2014 including timestamps that fall just before a revert (verifies reverted_to.prior_state captures enough state for backward replay).",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "get_recent_turns(5) returns the 5 most-recent bot_turns rows (most-recent first) with summaries; search_tool_calls(tool_name='edit_epic', epic_id=X) returns every edit_epic call against epic X with arguments and timestamps.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "All read tools (get_epic, get_section_names, get_history, get_self_understanding, get_epic_at_time, get_recent_turns, search_tool_calls) record operation_kind='read' in tool_calls; all write tools (create_epic, edit_epic, revert, render_epic) record operation_kind='write'.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "After every turn whose tool_calls include create_epic, edit_epic, or revert, exactly one system_logs row exists with category='application', event_type='epic_outline', turn_id=<that turn>, and details containing title plus a sections array with name + line_count for every section in the body.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "10-turn FakeModel-driven integration fixture in tests/test_editorial_loop.py runs end-to-end starting from epic_id=None, exercises all six default sections, exercises both expected_diff match and mismatch, exercises title editing via _preamble, exercises revert with backward replay across the revert, and asserts every Sprint 2a acceptance criterion in spec \u00a7131\u2013142.",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "All pre-existing tests in tests/ continue to pass (no regression in Sprint 1a/1b functionality, including resident-mode test_resident*, test_discord_*, and test_run_turn variants).",
        "priority": "must",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "Both Store adapters expose _EPIC_COLUMNS and _CHECKLIST_COLUMNS allowed-column sets and route update_epic / update_checklist_item through the existing _update helper, matching the _MESSAGE_COLUMNS / _TURN_COLUMNS / _IMAGE_COLUMNS pattern. _MESSAGE_COLUMNS and _TURN_COLUMNS include 'epic_id' so the bootstrap retro-stamp passes column safety.",
        "priority": "must",
        "requires": [
          "read_files"
        ]
      },
      {
        "criterion": "Body parser and section-op modules stay focused: the public surface is parse, serialize, validate_for_write, the section ops, compute_diff, diffs_equivalent, outline. No tool-layer or Store imports leak into agent_kit/body.py.",
        "priority": "should",
        "requires": [
          "read_files",
          "subjective_judgment"
        ]
      },
      {
        "criterion": "edit_epic rejects requests mixing two body op flavours (e.g. new_content + sections) with error='body_op_conflict' rather than silently picking one.",
        "priority": "should",
        "requires": [
          "run_tests"
        ]
      },
      {
        "criterion": "agent_kit/body.py stays under ~450 lines and has no third-party dependencies beyond the standard library (difflib, re).",
        "priority": "should",
        "requires": [
          "read_files"
        ]
      }
    ]
  },
  "preflight_results": {
    "project_dir_exists": true,
    "project_dir_writable": true,
    "success_criteria_present": true,
    "claude_available": true,
    "codex_available": true
  },
  "unresolved_flags": [
    {
      "id": "FLAG-001",
      "concern": "Editorial bootstrap: Rev 2 adds no-epic DB bootstrapping, but the envelope and local loop plumbing still assume a concrete epic id, so natural-language epic creation can complete with an invalid or stale envelope id.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "`Envelope.epic_id` and `envelope.schema.json` require a non-empty string, while `loop.py` return paths call `_envelope(..., epic_id=epic_id)` using the original parameter. Rev 2 updates `context.metadata['epic_id']` after `create_epic` but does not explicitly update the local id used for envelope returns or alter the schema for no-epic message-only turns.",
      "raised_in": "critique_v2.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "issue_hints-1",
      "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the revised no-epic bootstrap against `agent_kit/loop.py`, `agent_kit/envelope.py`, and `agent_kit/envelope.schema.json`. The plan adds `run_turn(epic_id=None)` and retro-stamps the DB rows after `create_epic`, which addresses the storage side of natural-language epic creation, but it does not say to update the local `epic_id` used by `_envelope()` or to allow a nullable/late-bound envelope id; as written, a successful bootstrap turn can still return an invalid envelope with `epic_id=None` even though the schema requires a non-empty string.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Checked the revised no-epic bootstrap against `agent_kit/loop.py`, `agent_kit/envelope.py`, and `agent_kit/envelope.schema.json`. The plan adds `run_turn(epic_id=None)` and retro-stamps the DB rows after `create_epic`, which addresses the storage side of natural-language epic creation, but it does not say to update the local `epic_id` used by `_envelope()` or to allow a nullable/late-bound envelope id; as written, a successful bootstrap turn can still return an invalid envelope with `epic_id=None` even though the schema requires a non-empty string.",
      "raised_in": "critique_v2.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "issue_hints-2",
      "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the body_version mention in `planning-bot-spec.md:2606-2611` against the current migrations. The current schema has no `body_version` column and the revised plan explicitly defers it while covering title/body sync via audit events; this is a spec divergence, even if likely acceptable for Sprint 2a because the main Data Model section does not define the column.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Checked the body_version mention in `planning-bot-spec.md:2606-2611` against the current migrations. The current schema has no `body_version` column and the revised plan explicitly defers it while covering title/body sync via audit events; this is a spec divergence, even if likely acceptable for Sprint 2a because the main Data Model section does not define the column.",
      "raised_in": "critique_v2.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "correctness-1",
      "concern": "Are the proposed changes technically correct?: I checked the body parsing rules in `planning-bot-spec.md` lines 503-514 against Phase 2. The spec separates parsing from write validation: bodies with no `##` headings are parseable as `_preamble`, while writes are rejected if they lack `# Title` or non-empty `## Goal`; the plan instead makes `parse()` raise when the first non-blank line is not `# <title>`, which conflicts with its own round-trip fixtures for preamble-only/no-section bodies and would break read tools on malformed legacy content.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Rev 2 addresses all 12 open critique flags by editing the existing six-phase structure rather than restructuring. Key changes: (1) added a no-epic mode to `run_turn` (epic_id=None), with `create_epic` retro-stamping the inbound message and bot_turn (FLAG-001/issue_hints-1/callers); (2) split parser into lenient `parse()` + strict `validate_for_write()` so reads/time-travel survive malformed bodies (FLAG-002/correctness-1); (3) redefined `_preamble` to include the `# Title` line per spec \u00a72606, making `replace_section('_preamble', ...)` the canonical title-edit path (issue_hints-2); (4) `reverted_to` events now snapshot full pre-revert body + checklist in `prior_state` so backward replay works across reverts (FLAG-003/correctness-2); (5) `create_epic` writes `epics.title`/`goal` exclusively from parsed values, never raw args (correctness-3); (6) read tools register with `operation_kind='read'` (scope-1); (7) `edit_epic.changes.meta` is explicitly rejected with `meta_not_supported` and a hint to use body sections (scope-2); (8) added `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` to both Store adapters and extended `_MESSAGE_COLUMNS`/`_TURN_COLUMNS` to allow the bootstrap `epic_id` retro-stamp (all_locations). Integration test gained explicit assertions for each critique fix (title-via-preamble, time-travel-across-revert, meta_not_supported, operation_kind values).",
      "raised_in": "critique_v1.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "correctness-2",
      "concern": "Are the proposed changes technically correct?: I checked `get_epic_at_time` and `revert` semantics against the `epic_events.prior_state` contract in `planning-bot-spec.md` lines 1030-1032 and 1381-1399. The plan stores only metadata on `reverted_to` events (`reverted_transaction_id` and ids), then proposes backward replay from current state; a later `reverted_to` event actually mutates body/checklist, but its event does not contain the pre-revert state needed to undo that mutation when reconstructing a timestamp just before the revert, so time travel across reverts will be incorrect.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Rev 2 addresses all 12 open critique flags by editing the existing six-phase structure rather than restructuring. Key changes: (1) added a no-epic mode to `run_turn` (epic_id=None), with `create_epic` retro-stamping the inbound message and bot_turn (FLAG-001/issue_hints-1/callers); (2) split parser into lenient `parse()` + strict `validate_for_write()` so reads/time-travel survive malformed bodies (FLAG-002/correctness-1); (3) redefined `_preamble` to include the `# Title` line per spec \u00a72606, making `replace_section('_preamble', ...)` the canonical title-edit path (issue_hints-2); (4) `reverted_to` events now snapshot full pre-revert body + checklist in `prior_state` so backward replay works across reverts (FLAG-003/correctness-2); (5) `create_epic` writes `epics.title`/`goal` exclusively from parsed values, never raw args (correctness-3); (6) read tools register with `operation_kind='read'` (scope-1); (7) `edit_epic.changes.meta` is explicitly rejected with `meta_not_supported` and a hint to use body sections (scope-2); (8) added `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` to both Store adapters and extended `_MESSAGE_COLUMNS`/`_TURN_COLUMNS` to allow the bootstrap `epic_id` retro-stamp (all_locations). Integration test gained explicit assertions for each critique fix (title-via-preamble, time-travel-across-revert, meta_not_supported, operation_kind values).",
      "raised_in": "critique_v1.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "correctness-3",
      "concern": "Are the proposed changes technically correct?: I reviewed the `create_epic` plan against the Data Model requirement in `planning-bot-spec.md` lines 1314-1316. The plan says `create_epic` constructs the body and calls parse/validate, but then passes title and goal columns supplied by the caller into `Store.create_epic`; to satisfy 'the parser is the only writer of epics.title and epics.goal', the tool should explicitly use the parsed title and parsed Goal first paragraph for the insert, not the raw arguments.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Rev 2 addresses all 12 open critique flags by editing the existing six-phase structure rather than restructuring. Key changes: (1) added a no-epic mode to `run_turn` (epic_id=None), with `create_epic` retro-stamping the inbound message and bot_turn (FLAG-001/issue_hints-1/callers); (2) split parser into lenient `parse()` + strict `validate_for_write()` so reads/time-travel survive malformed bodies (FLAG-002/correctness-1); (3) redefined `_preamble` to include the `# Title` line per spec \u00a72606, making `replace_section('_preamble', ...)` the canonical title-edit path (issue_hints-2); (4) `reverted_to` events now snapshot full pre-revert body + checklist in `prior_state` so backward replay works across reverts (FLAG-003/correctness-2); (5) `create_epic` writes `epics.title`/`goal` exclusively from parsed values, never raw args (correctness-3); (6) read tools register with `operation_kind='read'` (scope-1); (7) `edit_epic.changes.meta` is explicitly rejected with `meta_not_supported` and a hint to use body sections (scope-2); (8) added `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` to both Store adapters and extended `_MESSAGE_COLUMNS`/`_TURN_COLUMNS` to allow the bootstrap `epic_id` retro-stamp (all_locations). Integration test gained explicit assertions for each critique fix (title-via-preamble, time-travel-across-revert, meta_not_supported, operation_kind values).",
      "raised_in": "critique_v1.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "scope-1",
      "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: I searched the current tool system in `agent_kit/tool_kit.py` and existing tools in `agent_kit/tools/communication.py`. The plan follows the existing registry/audit pattern for new tools, but it does not mention marking the new read tools with `operation_kind='read'`; if omitted, `@register_tool` defaults to write, which would pollute audit semantics for `get_epic`, `get_history`, `get_recent_turns`, and `search_tool_calls`.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Rev 2 addresses all 12 open critique flags by editing the existing six-phase structure rather than restructuring. Key changes: (1) added a no-epic mode to `run_turn` (epic_id=None), with `create_epic` retro-stamping the inbound message and bot_turn (FLAG-001/issue_hints-1/callers); (2) split parser into lenient `parse()` + strict `validate_for_write()` so reads/time-travel survive malformed bodies (FLAG-002/correctness-1); (3) redefined `_preamble` to include the `# Title` line per spec \u00a72606, making `replace_section('_preamble', ...)` the canonical title-edit path (issue_hints-2); (4) `reverted_to` events now snapshot full pre-revert body + checklist in `prior_state` so backward replay works across reverts (FLAG-003/correctness-2); (5) `create_epic` writes `epics.title`/`goal` exclusively from parsed values, never raw args (correctness-3); (6) read tools register with `operation_kind='read'` (scope-1); (7) `edit_epic.changes.meta` is explicitly rejected with `meta_not_supported` and a hint to use body sections (scope-2); (8) added `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` to both Store adapters and extended `_MESSAGE_COLUMNS`/`_TURN_COLUMNS` to allow the bootstrap `epic_id` retro-stamp (all_locations). Integration test gained explicit assertions for each critique fix (title-via-preamble, time-travel-across-revert, meta_not_supported, operation_kind values).",
      "raised_in": "critique_v1.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "scope-2",
      "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: I checked the spec's tool surface around `edit_epic` in `planning-bot-spec.md` lines 1703-1740. The plan deliberately returns `not_yet_supported` for `changes.sprints` and `changes.state`, which is a scoped Sprint 2a tradeoff because sprints/state gating are later sprint work, but it also omits `changes.meta` handling from the schema discussion even though the spec's change object includes `meta?: { title?, goal? }`; this should be either intentionally rejected or mapped to body edits so callers do not get silent schema drift.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Rev 2 addresses all 12 open critique flags by editing the existing six-phase structure rather than restructuring. Key changes: (1) added a no-epic mode to `run_turn` (epic_id=None), with `create_epic` retro-stamping the inbound message and bot_turn (FLAG-001/issue_hints-1/callers); (2) split parser into lenient `parse()` + strict `validate_for_write()` so reads/time-travel survive malformed bodies (FLAG-002/correctness-1); (3) redefined `_preamble` to include the `# Title` line per spec \u00a72606, making `replace_section('_preamble', ...)` the canonical title-edit path (issue_hints-2); (4) `reverted_to` events now snapshot full pre-revert body + checklist in `prior_state` so backward replay works across reverts (FLAG-003/correctness-2); (5) `create_epic` writes `epics.title`/`goal` exclusively from parsed values, never raw args (correctness-3); (6) read tools register with `operation_kind='read'` (scope-1); (7) `edit_epic.changes.meta` is explicitly rejected with `meta_not_supported` and a hint to use body sections (scope-2); (8) added `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` to both Store adapters and extended `_MESSAGE_COLUMNS`/`_TURN_COLUMNS` to allow the bootstrap `epic_id` retro-stamp (all_locations). Integration test gained explicit assertions for each critique fix (title-via-preamble, time-travel-across-revert, meta_not_supported, operation_kind values).",
      "raised_in": "critique_v1.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "all_locations",
      "concern": "Does the change touch all locations AND supporting infrastructure?: Checked all locations touched by `run_turn(epic_id=None)`: `agent_kit/ports.py` still types `create_turn(epic_id: str)`, `agent_kit/envelope.py` types `Envelope.epic_id: str`, `agent_kit/envelope.schema.json` requires a non-empty string, and `arnold/cli.py` currently requires `--epic`. The revised plan mentions CLI no-epic plumbing but does not explicitly include the protocol/envelope/schema changes needed to keep all call boundaries consistent.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "Checked all locations touched by `run_turn(epic_id=None)`: `agent_kit/ports.py` still types `create_turn(epic_id: str)`, `agent_kit/envelope.py` types `Envelope.epic_id: str`, `agent_kit/envelope.schema.json` requires a non-empty string, and `arnold/cli.py` currently requires `--epic`. The revised plan mentions CLI no-epic plumbing but does not explicitly include the protocol/envelope/schema changes needed to keep all call boundaries consistent.",
      "raised_in": "critique_v2.json",
      "status": "open",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "callers",
      "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: I inspected `agent_kit/loop.py` and `tests/test_run_turn.py`; current callers of `run_turn` always provide an `epic_id`, and test helpers seed an `epics` row first. The planned `create_epic` tool does not fit this caller contract for a brand-new epic: using a non-existent id would fail the current lock/message foreign-key path, while using an existing placeholder epic would make the create tool semantically odd unless the loop/CLI grows an explicit no-epic or inbox mode.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Rev 2 addresses all 12 open critique flags by editing the existing six-phase structure rather than restructuring. Key changes: (1) added a no-epic mode to `run_turn` (epic_id=None), with `create_epic` retro-stamping the inbound message and bot_turn (FLAG-001/issue_hints-1/callers); (2) split parser into lenient `parse()` + strict `validate_for_write()` so reads/time-travel survive malformed bodies (FLAG-002/correctness-1); (3) redefined `_preamble` to include the `# Title` line per spec \u00a72606, making `replace_section('_preamble', ...)` the canonical title-edit path (issue_hints-2); (4) `reverted_to` events now snapshot full pre-revert body + checklist in `prior_state` so backward replay works across reverts (FLAG-003/correctness-2); (5) `create_epic` writes `epics.title`/`goal` exclusively from parsed values, never raw args (correctness-3); (6) read tools register with `operation_kind='read'` (scope-1); (7) `edit_epic.changes.meta` is explicitly rejected with `meta_not_supported` and a hint to use body sections (scope-2); (8) added `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` to both Store adapters and extended `_MESSAGE_COLUMNS`/`_TURN_COLUMNS` to allow the bootstrap `epic_id` retro-stamp (all_locations). Integration test gained explicit assertions for each critique fix (title-via-preamble, time-travel-across-revert, meta_not_supported, operation_kind values).",
      "raised_in": "critique_v1.json",
      "status": "addressed",
      "severity": "significant",
      "verified": false,
      "addressed_in": "plan_v2.md"
    },
    {
      "id": "FLAG-005",
      "concern": "Bootstrap API consistency: the plan changes `run_turn` to accept `epic_id=None` but does not explicitly update all public/protocol boundaries that currently require a concrete epic id.",
      "category": "completeness",
      "severity_hint": "likely-significant",
      "evidence": "`agent_kit/ports.py` has `Store.create_turn(epic_id: str)`, `agent_kit/envelope.py` has `Envelope.epic_id: str`, `agent_kit/envelope.schema.json` requires `epic_id` as a non-empty string, and `arnold/cli.py` currently requires `--epic` and uses `args.epic` in the error envelope path.",
      "raised_in": "critique_v2.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "correctness",
      "concern": "Are the proposed changes technically correct?: Checked the revised no-epic branch against abort, provider-error, tool-error, defer, and final-response returns in `agent_kit/loop.py`. Those code paths currently call `_abort_turn()` or `_envelope()` with the original local `epic_id` parameter, so the plan needs an explicit local `active_epic_id = context.metadata.get('epic_id')` handoff before every envelope return or an envelope schema change; otherwise no-epic turns that create an epic, defer, error, or finish without creating one can serialize invalid or misleading envelopes.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Checked the revised no-epic branch against abort, provider-error, tool-error, defer, and final-response returns in `agent_kit/loop.py`. Those code paths currently call `_abort_turn()` or `_envelope()` with the original local `epic_id` parameter, so the plan needs an explicit local `active_epic_id = context.metadata.get('epic_id')` handoff before every envelope return or an envelope schema change; otherwise no-epic turns that create an epic, defer, error, or finish without creating one can serialize invalid or misleading envelopes.",
      "raised_in": "critique_v2.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "callers-1",
      "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked existing Python and CLI callers of `run_turn`. The revised plan is additive for existing tests and resident callers that still pass concrete epic ids, and it adds a new CLI no-epic path for bootstrap, but it must also update the CLI exception envelope path because `arnold/cli.py` currently builds an error envelope with `epic_id=args.epic`; with optional `--epic`, that can become missing or `None` unless explicitly handled.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Checked existing Python and CLI callers of `run_turn`. The revised plan is additive for existing tests and resident callers that still pass concrete epic ids, and it adds a new CLI no-epic path for bootstrap, but it must also update the CLI exception envelope path because `arnold/cli.py` currently builds an error envelope with `epic_id=args.epic`; with optional `--epic`, that can become missing or `None` unless explicitly handled.",
      "raised_in": "critique_v2.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    },
    {
      "id": "callers-2",
      "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked current callers of `store.create_turn` in tests, resident recovery, and the loop. Existing callers pass concrete ids, while the new no-epic loop path passes `None`; the database allows NULL for `bot_turns.epic_id`, but the `Store` protocol and both adapter signatures are still typed as `str`, so the plan should explicitly update those signatures to `str | None` to match the intended caller values.",
      "category": "correctness",
      "severity_hint": "likely-significant",
      "evidence": "Checked current callers of `store.create_turn` in tests, resident recovery, and the loop. Existing callers pass concrete ids, while the new no-epic loop path passes `None`; the database allows NULL for `bot_turns.epic_id`, but the `Store` protocol and both adapter signatures are still typed as `str`, so the plan should explicitly update those signatures to `str | None` to match the intended caller values.",
      "raised_in": "critique_v2.json",
      "status": "open",
      "severity": "significant",
      "verified": false
    }
  ],
  "recommendation": "ITERATE",
  "rationale": "Iteration 2 with plan delta 60% resolved 9 of the original 12 flags (FLAG-002, FLAG-003, correctness-1/2/3, scope-1/2, callers, FLAG-004 \u2014 all marked addressed). However, the new no-epic bootstrap mode introduced to fix FLAG-001 has surfaced a tightly-related cluster of consistency flags (FLAG-001 re-raised, FLAG-005, issue_hints-1, all_locations, correctness, callers-1, callers-2) that all point to one concrete gap: the plan changes `run_turn` to accept `epic_id=None` but never threads `Optional[str]` through the supporting boundaries \u2014 `Store.create_turn` signature in `agent_kit/ports.py`, `Envelope.epic_id` in `agent_kit/envelope.py`, the `epic_id` requirement in `agent_kit/envelope.schema.json`, the `args.epic` use in `arnold/cli.py`'s exception envelope path, and the local `epic_id` variable used by every `_envelope(...)` and `_abort_turn(...)` return inside `loop.py`. No churn pattern (addressed_then_reopened_count=0 for every group), so this is plan-quality, not stuck loop or unresolvable tension. issue_hints-2 (body_version) is the one flag that is genuinely a deferral question \u2014 the spec mentions body_version only in \u00a72606 example (not in the main Data Model \u00a71311), so it is reasonable to defer, but the plan should say so explicitly as accepted scope. Score held at 16.0 across iterations, but that's the natural floor while one cohesive cluster is open; once threaded through, the cluster collapses.",
  "signals_assessment": "Iteration 2, weighted score 16.0 \u2192 16.0 (held), plan delta 60.45% (substantive rev). Flag status: 3 resolved (FLAG-002, FLAG-003, FLAG-004), 8 marked addressed by the rev (correctness-1/2/3, scope-1/2, callers, FLAG-004) but reviewer wants verification language in the plan, and 7 new significant flags surfaced \u2014 all in one cluster around no-epic bootstrap API consistency. Iteration pressure: FG-005 and FG-001 at 3 iters each but addressed_then_reopened_count=0 across all groups; no TIEBREAKER threshold hit. Preflight clean. Posture: one cohesive plan-quality fix away from PROCEED.",
  "warnings": [
    "The bootstrap-consistency cluster (FLAG-001, FLAG-005, issue_hints-1, all_locations, correctness, callers-1, callers-2) is one cohesive gap, not seven independent ones \u2014 a single Phase 5 / Step 14 expansion should resolve all of them in rev 3.",
    "issue_hints-2 (body_version) should be promoted from 'deferred' to an explicit accepted-tradeoff in the plan's assumptions, with the rationale that spec \u00a72606 references body_version only as an illustrative example and the main Data Model section (\u00a71311) does not define the column.",
    "Resolved flags marked 'addressed' in metadata still appear in the unresolved list with status='addressed' \u2014 this seems to be a harness quirk; the substantive content was fixed in rev 2, but rev 3 should add explicit verification language so the next critique pass can flip them to 'resolved'."
  ],
  "settled_decisions": [
    {
      "id": "SD-001",
      "decision": "Sprint 2a is invocation-mode only; no resident-mode behaviour changes required.",
      "rationale": "Confirmed in plan assumptions and unchallenged in iteration 2 critique."
    },
    {
      "id": "SD-002",
      "decision": "edit_epic.changes.sprints and changes.state return not_yet_supported; full handling lands in Sprint 4.",
      "rationale": "Explicit scope boundary in plan; not contested."
    },
    {
      "id": "SD-003",
      "decision": "edit_epic.changes.meta is rejected with error='meta_not_supported' and a hint pointing to body.sections._preamble (title) or body.sections.Goal (goal); title/goal are derived columns whose only writer is the body parser.",
      "rationale": "Resolves scope-2; integration test asserts the rejection."
    },
    {
      "id": "SD-004",
      "decision": "Default checklist seed is unconditional (18 items); adaptation lives in the bot's prompt, not server-side.",
      "rationale": "Settled in iteration 1, unchallenged in iteration 2."
    },
    {
      "id": "SD-005",
      "decision": "Body parser splits into lenient parse() + strict validate_for_write(); read tools and time-travel use parse() only and never raise on malformed/legacy bodies.",
      "rationale": "Resolves FLAG-002 and correctness-1; round-trip identity fixtures and lenient-input fixtures both pass."
    },
    {
      "id": "SD-006",
      "decision": "_preamble includes the # Title line and any leading text up to the first ## heading; replace_section('_preamble', '# New Title\\n') is the canonical title-edit path per spec \u00a72606; rename_section to/from _preamble is rejected.",
      "rationale": "Resolves FLAG-004 and issue_hints-2 (rev 1)."
    },
    {
      "id": "SD-007",
      "decision": "create_epic writes epics.title and epics.goal exclusively from parse() output; raw title/goal arguments are template inputs only.",
      "rationale": "Resolves correctness-3; satisfies spec \u00a71314\u20131316."
    },
    {
      "id": "SD-008",
      "decision": "reverted_to events store full pre-revert body, title, goal, and checklist snapshot in prior_state so backward replay across reverts is correct.",
      "rationale": "Resolves FLAG-003 and correctness-2; integration test asserts get_epic_at_time at T_just_before_revert."
    },
    {
      "id": "SD-009",
      "decision": "Read tools (get_epic, get_section_names, get_history, get_self_understanding, get_epic_at_time, get_recent_turns, search_tool_calls) register with operation_kind='read'; write tools register with operation_kind='write'.",
      "rationale": "Resolves scope-1; integration test asserts the recorded operation_kind values."
    },
    {
      "id": "SD-010",
      "decision": "Both Store adapters expose _EPIC_COLUMNS and _CHECKLIST_COLUMNS guarded-update sets and route update_epic / update_checklist_item through the existing _update helper; _MESSAGE_COLUMNS and _TURN_COLUMNS gain 'epic_id' so the bootstrap retro-stamp uses guarded updates.",
      "rationale": "Resolves all_locations (rev 1); matches existing _MESSAGE_COLUMNS/_TURN_COLUMNS/_IMAGE_COLUMNS pattern."
    },
    {
      "id": "SD-011",
      "decision": "expected_diff equivalence: line endings normalised to \\n, trailing whitespace stripped per line, trailing blank lines dropped, then byte-equal compare.",
      "rationale": "Spec \u00a7494; not contested."
    },
    {
      "id": "SD-012",
      "decision": "epic_outline log fires only on turns whose tool_calls include create_epic, edit_epic, or revert; pure-read and failed turns skip the log.",
      "rationale": "Matches spec wording 'turn that touched an epic'; not contested."
    }
  ],
  "override_forced": false,
  "orchestrator_guidance": "Gate recommends another iteration. Revise the plan. Verify unresolved flags against the plan and project code before accepting.",
  "robustness": "standard",
  "signals": {
    "iteration": 2,
    "idea": "# Sprint 2a \u2014 Editorial core\n\nBot maintains an epic body and checklist for one epic, with section-level body editing. Minimum to have an editorial conversation.\n\n**Full spec is at `planning-bot-spec.md` in this repo root. Refer to it for complete details on Body Structure and Editing, Body Templates, The Checklist as Guide, and Data Model sections.**\n\n## Supabase\n- URL: https://yhwflvadmefhkshwbfnf.supabase.co\n- Service key: [REDACTED_SUPABASE_SERVICE_ROLE_JWT]\n\n## Scope\n\n- Tables: checklist_items, epic_events (with transaction_id)\n- Body parser/serializer \u2014 markdown \u2194 structured sections with ## heading delimiters; enforces heading hierarchy (# for title only, ## for sections, ### for sub-headings)\n- Turn-end epic outline emitted to system_logs at info level\n- Default body template (design doc) \u2014 Goal, Principles, Context, Key Decisions, Open Questions, Deliverable\n- `edit_epic` tool \u2014 body (whole + section ops) + checklist; supports:\n  - Write whole body\n  - Write specific sections\n  - Append to a section\n  - Add new section with position\n  - Rename/remove sections\n  - `expected_diff` parameter for server-enforced diff verification (unified diff format)\n- `create_epic`, `revert` (transaction-grouped), `render_epic` tools\n- Read tools: `get_epic` (with section addressing), `get_section_names`, `get_history`, `get_self_understanding`\n- History tools: `get_epic_at_time`, `get_recent_turns`, `search_tool_calls`\n- Default checklist seed \u2014 18 items with adaptation logic\n- Title and goal are derived columns from body parsing (# Title and ## Goal first paragraph)\n\n## Key Data Model\n\n### checklist_items\nid, epic_id, content, status (open|done|skipped|superseded), position, source (bot_inferred|user_requested|carried_over|default_seed|second_opinion), skip_reason, superseded_by_item_id, created_at, completed_at\n\n### epic_events\nid, epic_id, transaction_id (uuid), event_type, summary, prior_state (json), turn_id, occurred_at\nEvent types: body_edit, checklist_change, sprints_change, state_change, forced_handoff, created, code_referenced, codebase_added, image_generated, second_opinion_requested, reverted_to, sprint_status_change\n\n## Body Parser Rules\n- Section boundaries are ## headings (level-2 markdown)\n- Section names are case-sensitive\n- Pre-section content is \"_preamble\"\n- Sub-sections (### and below) are part of parent section\n- No ## headings \u2192 whole body is _preamble\n- # Title and ## Goal are required structural elements; missing \u2192 write rejected\n- Code blocks containing ## are NOT section boundaries\n\n## Acceptance Criteria\n\n- Create an epic via natural language \u2192 epics row created, default checklist seeded with 18 items, body initialized\n- 10-turn scripted conversation (mocked Anthropic) produces body with all 6 default sections\n- Section-level edit \u2192 only that section changes; other sections byte-identical\n- Whole body edit \u2192 diff captured in event; revert restores prior version exactly\n- \"revert that\" \u2192 most recent transaction undone, new reverted_to event logged\n- expected_diff mismatch \u2192 server refuses write, returns actual diff\n- expected_diff match \u2192 server commits normally\n- get_epic_at_time(epic_id, T) \u2192 returns body/checklist state as of time T\n- get_recent_turns(5) \u2192 returns 5 most recent turns with summaries\n- search_tool_calls(tool_name='edit_epic', epic_id=X) \u2192 returns matching calls\n- Turn-end system_logs row with event_type='epic_outline' containing title + section list + line counts\n\n## Tests\n- Unit: body parser (markdown \u2192 sections \u2192 markdown roundtrip is identity); section operations; edit_epic validation; transaction_id grouping; expected_diff comparison; epic-at-time replay\n- Integration: 10-turn fixture conversation against local Supabase with mocked Anthropic; revert end-to-end",
    "significant_flags": 14,
    "unresolved_flags": [
      {
        "id": "FLAG-001",
        "concern": "Editorial bootstrap: Rev 2 adds no-epic DB bootstrapping, but the envelope and local loop plumbing still assume a concrete epic id, so natural-language epic creation can complete with an invalid or stale envelope id.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "issue_hints-1",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the revised no-epic bootstrap against `agent_kit/loop.py`, `agent_kit/envelope.py`, and `agent_kit/envelope.schema.json`. The plan adds `run_turn(epic_id=None)` and retro-stamps the DB rows after `create_epic`, which addresses the storage side of natural-language epic creation, but it does not say to update the local `epic_id` used by `_envelope()` or to allow a nullable/late-bound envelope id; as written, a successful bootstrap turn can still return an invalid envelope with `epic_id=None` even though the schema requires a non-empty string.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "issue_hints-2",
        "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the body_version mention in `planning-bot-spec.md:2606-2611` against the current migrations. The current schema has no `body_version` column and the revised plan explicitly defers it while covering title/body sync via audit events; this is a spec divergence, even if likely acceptable for Sprint 2a because the main Data Model section does not define the column.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "correctness-1",
        "concern": "Are the proposed changes technically correct?: I checked the body parsing rules in `planning-bot-spec.md` lines 503-514 against Phase 2. The spec separates parsing from write validation: bodies with no `##` headings are parseable as `_preamble`, while writes are rejected if they lack `# Title` or non-empty `## Goal`; the plan instead makes `parse()` raise when the first non-blank line is not `# <title>`, which conflicts with its own round-trip fixtures for preamble-only/no-section bodies and would break read tools on malformed legacy content.",
        "category": "correctness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "correctness-2",
        "concern": "Are the proposed changes technically correct?: I checked `get_epic_at_time` and `revert` semantics against the `epic_events.prior_state` contract in `planning-bot-spec.md` lines 1030-1032 and 1381-1399. The plan stores only metadata on `reverted_to` events (`reverted_transaction_id` and ids), then proposes backward replay from current state; a later `reverted_to` event actually mutates body/checklist, but its event does not contain the pre-revert state needed to undo that mutation when reconstructing a timestamp just before the revert, so time travel across reverts will be incorrect.",
        "category": "correctness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "correctness-3",
        "concern": "Are the proposed changes technically correct?: I reviewed the `create_epic` plan against the Data Model requirement in `planning-bot-spec.md` lines 1314-1316. The plan says `create_epic` constructs the body and calls parse/validate, but then passes title and goal columns supplied by the caller into `Store.create_epic`; to satisfy 'the parser is the only writer of epics.title and epics.goal', the tool should explicitly use the parsed title and parsed Goal first paragraph for the insert, not the raw arguments.",
        "category": "correctness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "scope-1",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: I searched the current tool system in `agent_kit/tool_kit.py` and existing tools in `agent_kit/tools/communication.py`. The plan follows the existing registry/audit pattern for new tools, but it does not mention marking the new read tools with `operation_kind='read'`; if omitted, `@register_tool` defaults to write, which would pollute audit semantics for `get_epic`, `get_history`, `get_recent_turns`, and `search_tool_calls`.",
        "category": "completeness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "scope-2",
        "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: I checked the spec's tool surface around `edit_epic` in `planning-bot-spec.md` lines 1703-1740. The plan deliberately returns `not_yet_supported` for `changes.sprints` and `changes.state`, which is a scoped Sprint 2a tradeoff because sprints/state gating are later sprint work, but it also omits `changes.meta` handling from the schema discussion even though the spec's change object includes `meta?: { title?, goal? }`; this should be either intentionally rejected or mapped to body edits so callers do not get silent schema drift.",
        "category": "completeness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "all_locations",
        "concern": "Does the change touch all locations AND supporting infrastructure?: Checked all locations touched by `run_turn(epic_id=None)`: `agent_kit/ports.py` still types `create_turn(epic_id: str)`, `agent_kit/envelope.py` types `Envelope.epic_id: str`, `agent_kit/envelope.schema.json` requires a non-empty string, and `arnold/cli.py` currently requires `--epic`. The revised plan mentions CLI no-epic plumbing but does not explicitly include the protocol/envelope/schema changes needed to keep all call boundaries consistent.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "callers",
        "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: I inspected `agent_kit/loop.py` and `tests/test_run_turn.py`; current callers of `run_turn` always provide an `epic_id`, and test helpers seed an `epics` row first. The planned `create_epic` tool does not fit this caller contract for a brand-new epic: using a non-existent id would fail the current lock/message foreign-key path, while using an existing placeholder epic would make the create tool semantically odd unless the loop/CLI grows an explicit no-epic or inbox mode.",
        "category": "correctness",
        "severity": "significant",
        "status": "addressed"
      },
      {
        "id": "FLAG-005",
        "concern": "Bootstrap API consistency: the plan changes `run_turn` to accept `epic_id=None` but does not explicitly update all public/protocol boundaries that currently require a concrete epic id.",
        "category": "completeness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "correctness",
        "concern": "Are the proposed changes technically correct?: Checked the revised no-epic branch against abort, provider-error, tool-error, defer, and final-response returns in `agent_kit/loop.py`. Those code paths currently call `_abort_turn()` or `_envelope()` with the original local `epic_id` parameter, so the plan needs an explicit local `active_epic_id = context.metadata.get('epic_id')` handoff before every envelope return or an envelope schema change; otherwise no-epic turns that create an epic, defer, error, or finish without creating one can serialize invalid or misleading envelopes.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "callers-1",
        "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked existing Python and CLI callers of `run_turn`. The revised plan is additive for existing tests and resident callers that still pass concrete epic ids, and it adds a new CLI no-epic path for bootstrap, but it must also update the CLI exception envelope path because `arnold/cli.py` currently builds an error envelope with `epic_id=args.epic`; with optional `--epic`, that can become missing or `None` unless explicitly handled.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      },
      {
        "id": "callers-2",
        "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked current callers of `store.create_turn` in tests, resident recovery, and the loop. Existing callers pass concrete ids, while the new no-epic loop path passes `None`; the database allows NULL for `bot_turns.epic_id`, but the `Store` protocol and both adapter signatures are still typed as `str`, so the plan should explicitly update those signatures to `str | None` to match the intended caller values.",
        "category": "correctness",
        "severity": "significant",
        "status": "open"
      }
    ],
    "resolved_flags": [
      {
        "id": "FLAG-002",
        "concern": "Body parser/validation: the plan makes `parse()` reject missing `# Title`, conflicting with the spec's parseable `_preamble` fallback and with read/time-travel tools that need to inspect malformed or legacy bodies.",
        "resolution": "Rev 2 addresses all 12 open critique flags by editing the existing six-phase structure rather than restructuring. Key changes: (1) added a no-epic mode to `run_turn` (epic_id=None), with `create_epic` retro-stamping the inbound message and bot_turn (FLAG-001/issue_hints-1/callers); (2) split parser into lenient `parse()` + strict `validate_for_write()` so reads/time-travel survive malformed bodies (FLAG-002/correctness-1); (3) redefined `_preamble` to include the `# Title` line per spec \u00a72606, making `replace_section('_preamble', ...)` the canonical title-edit path (issue_hints-2); (4) `reverted_to` events now snapshot full pre-revert body + checklist in `prior_state` so backward replay works across reverts (FLAG-003/correctness-2); (5) `create_epic` writes `epics.title`/`goal` exclusively from parsed values, never raw args (correctness-3); (6) read tools register with `operation_kind='read'` (scope-1); (7) `edit_epic.changes.meta` is explicitly rejected with `meta_not_supported` and a hint to use body sections (scope-2); (8) added `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` to both Store adapters and extended `_MESSAGE_COLUMNS`/`_TURN_COLUMNS` to allow the bootstrap `epic_id` retro-stamp (all_locations). Integration test gained explicit assertions for each critique fix (title-via-preamble, time-travel-across-revert, meta_not_supported, operation_kind values)."
      },
      {
        "id": "FLAG-003",
        "concern": "History replay: `reverted_to` events do not store enough prior state to support backward `get_epic_at_time` reconstruction across a revert.",
        "resolution": "Rev 2 addresses all 12 open critique flags by editing the existing six-phase structure rather than restructuring. Key changes: (1) added a no-epic mode to `run_turn` (epic_id=None), with `create_epic` retro-stamping the inbound message and bot_turn (FLAG-001/issue_hints-1/callers); (2) split parser into lenient `parse()` + strict `validate_for_write()` so reads/time-travel survive malformed bodies (FLAG-002/correctness-1); (3) redefined `_preamble` to include the `# Title` line per spec \u00a72606, making `replace_section('_preamble', ...)` the canonical title-edit path (issue_hints-2); (4) `reverted_to` events now snapshot full pre-revert body + checklist in `prior_state` so backward replay works across reverts (FLAG-003/correctness-2); (5) `create_epic` writes `epics.title`/`goal` exclusively from parsed values, never raw args (correctness-3); (6) read tools register with `operation_kind='read'` (scope-1); (7) `edit_epic.changes.meta` is explicitly rejected with `meta_not_supported` and a hint to use body sections (scope-2); (8) added `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` to both Store adapters and extended `_MESSAGE_COLUMNS`/`_TURN_COLUMNS` to allow the bootstrap `epic_id` retro-stamp (all_locations). Integration test gained explicit assertions for each critique fix (title-via-preamble, time-travel-across-revert, meta_not_supported, operation_kind values)."
      },
      {
        "id": "FLAG-004",
        "concern": "Section addressing: `_preamble` as planned excludes the title line, so the spec's title edit via `_preamble` section replacement cannot work.",
        "resolution": "The plan defines `preamble` as text between the title line and the first `##`; the spec's Sprint 2a title/body sync test edits `_preamble` with `'# New Title\\n'` and expects `epics.title` to update."
      }
    ],
    "weighted_score": 16.0,
    "weighted_history": [
      16.0
    ],
    "plan_delta_from_previous": 60.45,
    "recurring_critiques": [],
    "scope_creep_flags": [],
    "loop_summary": "Iteration 2. Weighted score trajectory: 16.0 -> 16.0. Plan deltas: 60.5%. Recurring critiques: 0. Resolved flags: 3. Open significant flags: 14.",
    "debt_overlaps": [],
    "escalated_debt_subsystems": []
  },
  "flag_resolutions": [],
  "resolved_flag_ids": [],
  "resolution_summary": "",
  "reprompted": false
}

        Open significant flags:
        [
  {
    "id": "FLAG-001",
    "severity": "significant",
    "status": "open",
    "concern": "Editorial bootstrap: Rev 2 adds no-epic DB bootstrapping, but the envelope and local loop plumbing still assume a concrete epic id, so natural-language epic creation can complete with an invalid or stale envelope id.",
    "evidence": "`Envelope.epic_id` and `envelope.schema.json` require a non-empty string, while `loop.py` return paths call `_envelope(..., epic_id=epic_id)` using the original parameter. Rev 2 updates `context.metadata['epic_id']` after `create_epic` but does not explicitly update the local id used for envelope returns or alter the schema for no-epic message-only turns."
  },
  {
    "id": "issue_hints-1",
    "severity": "significant",
    "status": "open",
    "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the revised no-epic bootstrap against `agent_kit/loop.py`, `agent_kit/envelope.py`, and `agent_kit/envelope.schema.json`. The plan adds `run_turn(epic_id=None)` and retro-stamps the DB rows after `create_epic`, which addresses the storage side of natural-language epic creation, but it does not say to update the local `epic_id` used by `_envelope()` or to allow a nullable/late-bound envelope id; as written, a successful bootstrap turn can still return an invalid envelope with `epic_id=None` even though the schema requires a non-empty string.",
    "evidence": "Checked the revised no-epic bootstrap against `agent_kit/loop.py`, `agent_kit/envelope.py`, and `agent_kit/envelope.schema.json`. The plan adds `run_turn(epic_id=None)` and retro-stamps the DB rows after `create_epic`, which addresses the storage side of natural-language epic creation, but it does not say to update the local `epic_id` used by `_envelope()` or to allow a nullable/late-bound envelope id; as written, a successful bootstrap turn can still return an invalid envelope with `epic_id=None` even though the schema requires a non-empty string."
  },
  {
    "id": "issue_hints-2",
    "severity": "significant",
    "status": "open",
    "concern": "Did the work fully address the issue hints, user notes, and approved plan requirements?: Checked the body_version mention in `planning-bot-spec.md:2606-2611` against the current migrations. The current schema has no `body_version` column and the revised plan explicitly defers it while covering title/body sync via audit events; this is a spec divergence, even if likely acceptable for Sprint 2a because the main Data Model section does not define the column.",
    "evidence": "Checked the body_version mention in `planning-bot-spec.md:2606-2611` against the current migrations. The current schema has no `body_version` column and the revised plan explicitly defers it while covering title/body sync via audit events; this is a spec divergence, even if likely acceptable for Sprint 2a because the main Data Model section does not define the column."
  },
  {
    "id": "correctness-1",
    "severity": "significant",
    "status": "addressed",
    "concern": "Are the proposed changes technically correct?: I checked the body parsing rules in `planning-bot-spec.md` lines 503-514 against Phase 2. The spec separates parsing from write validation: bodies with no `##` headings are parseable as `_preamble`, while writes are rejected if they lack `# Title` or non-empty `## Goal`; the plan instead makes `parse()` raise when the first non-blank line is not `# <title>`, which conflicts with its own round-trip fixtures for preamble-only/no-section bodies and would break read tools on malformed legacy content.",
    "evidence": "Rev 2 addresses all 12 open critique flags by editing the existing six-phase structure rather than restructuring. Key changes: (1) added a no-epic mode to `run_turn` (epic_id=None), with `create_epic` retro-stamping the inbound message and bot_turn (FLAG-001/issue_hints-1/callers); (2) split parser into lenient `parse()` + strict `validate_for_write()` so reads/time-travel survive malformed bodies (FLAG-002/correctness-1); (3) redefined `_preamble` to include the `# Title` line per spec \u00a72606, making `replace_section('_preamble', ...)` the canonical title-edit path (issue_hints-2); (4) `reverted_to` events now snapshot full pre-revert body + checklist in `prior_state` so backward replay works across reverts (FLAG-003/correctness-2); (5) `create_epic` writes `epics.title`/`goal` exclusively from parsed values, never raw args (correctness-3); (6) read tools register with `operation_kind='read'` (scope-1); (7) `edit_epic.changes.meta` is explicitly rejected with `meta_not_supported` and a hint to use body sections (scope-2); (8) added `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` to both Store adapters and extended `_MESSAGE_COLUMNS`/`_TURN_COLUMNS` to allow the bootstrap `epic_id` retro-stamp (all_locations). Integration test gained explicit assertions for each critique fix (title-via-preamble, time-travel-across-revert, meta_not_supported, operation_kind values)."
  },
  {
    "id": "correctness-2",
    "severity": "significant",
    "status": "addressed",
    "concern": "Are the proposed changes technically correct?: I checked `get_epic_at_time` and `revert` semantics against the `epic_events.prior_state` contract in `planning-bot-spec.md` lines 1030-1032 and 1381-1399. The plan stores only metadata on `reverted_to` events (`reverted_transaction_id` and ids), then proposes backward replay from current state; a later `reverted_to` event actually mutates body/checklist, but its event does not contain the pre-revert state needed to undo that mutation when reconstructing a timestamp just before the revert, so time travel across reverts will be incorrect.",
    "evidence": "Rev 2 addresses all 12 open critique flags by editing the existing six-phase structure rather than restructuring. Key changes: (1) added a no-epic mode to `run_turn` (epic_id=None), with `create_epic` retro-stamping the inbound message and bot_turn (FLAG-001/issue_hints-1/callers); (2) split parser into lenient `parse()` + strict `validate_for_write()` so reads/time-travel survive malformed bodies (FLAG-002/correctness-1); (3) redefined `_preamble` to include the `# Title` line per spec \u00a72606, making `replace_section('_preamble', ...)` the canonical title-edit path (issue_hints-2); (4) `reverted_to` events now snapshot full pre-revert body + checklist in `prior_state` so backward replay works across reverts (FLAG-003/correctness-2); (5) `create_epic` writes `epics.title`/`goal` exclusively from parsed values, never raw args (correctness-3); (6) read tools register with `operation_kind='read'` (scope-1); (7) `edit_epic.changes.meta` is explicitly rejected with `meta_not_supported` and a hint to use body sections (scope-2); (8) added `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` to both Store adapters and extended `_MESSAGE_COLUMNS`/`_TURN_COLUMNS` to allow the bootstrap `epic_id` retro-stamp (all_locations). Integration test gained explicit assertions for each critique fix (title-via-preamble, time-travel-across-revert, meta_not_supported, operation_kind values)."
  },
  {
    "id": "correctness-3",
    "severity": "significant",
    "status": "addressed",
    "concern": "Are the proposed changes technically correct?: I reviewed the `create_epic` plan against the Data Model requirement in `planning-bot-spec.md` lines 1314-1316. The plan says `create_epic` constructs the body and calls parse/validate, but then passes title and goal columns supplied by the caller into `Store.create_epic`; to satisfy 'the parser is the only writer of epics.title and epics.goal', the tool should explicitly use the parsed title and parsed Goal first paragraph for the insert, not the raw arguments.",
    "evidence": "Rev 2 addresses all 12 open critique flags by editing the existing six-phase structure rather than restructuring. Key changes: (1) added a no-epic mode to `run_turn` (epic_id=None), with `create_epic` retro-stamping the inbound message and bot_turn (FLAG-001/issue_hints-1/callers); (2) split parser into lenient `parse()` + strict `validate_for_write()` so reads/time-travel survive malformed bodies (FLAG-002/correctness-1); (3) redefined `_preamble` to include the `# Title` line per spec \u00a72606, making `replace_section('_preamble', ...)` the canonical title-edit path (issue_hints-2); (4) `reverted_to` events now snapshot full pre-revert body + checklist in `prior_state` so backward replay works across reverts (FLAG-003/correctness-2); (5) `create_epic` writes `epics.title`/`goal` exclusively from parsed values, never raw args (correctness-3); (6) read tools register with `operation_kind='read'` (scope-1); (7) `edit_epic.changes.meta` is explicitly rejected with `meta_not_supported` and a hint to use body sections (scope-2); (8) added `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` to both Store adapters and extended `_MESSAGE_COLUMNS`/`_TURN_COLUMNS` to allow the bootstrap `epic_id` retro-stamp (all_locations). Integration test gained explicit assertions for each critique fix (title-via-preamble, time-travel-across-revert, meta_not_supported, operation_kind values)."
  },
  {
    "id": "scope-1",
    "severity": "significant",
    "status": "addressed",
    "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: I searched the current tool system in `agent_kit/tool_kit.py` and existing tools in `agent_kit/tools/communication.py`. The plan follows the existing registry/audit pattern for new tools, but it does not mention marking the new read tools with `operation_kind='read'`; if omitted, `@register_tool` defaults to write, which would pollute audit semantics for `get_epic`, `get_history`, `get_recent_turns`, and `search_tool_calls`.",
    "evidence": "Rev 2 addresses all 12 open critique flags by editing the existing six-phase structure rather than restructuring. Key changes: (1) added a no-epic mode to `run_turn` (epic_id=None), with `create_epic` retro-stamping the inbound message and bot_turn (FLAG-001/issue_hints-1/callers); (2) split parser into lenient `parse()` + strict `validate_for_write()` so reads/time-travel survive malformed bodies (FLAG-002/correctness-1); (3) redefined `_preamble` to include the `# Title` line per spec \u00a72606, making `replace_section('_preamble', ...)` the canonical title-edit path (issue_hints-2); (4) `reverted_to` events now snapshot full pre-revert body + checklist in `prior_state` so backward replay works across reverts (FLAG-003/correctness-2); (5) `create_epic` writes `epics.title`/`goal` exclusively from parsed values, never raw args (correctness-3); (6) read tools register with `operation_kind='read'` (scope-1); (7) `edit_epic.changes.meta` is explicitly rejected with `meta_not_supported` and a hint to use body sections (scope-2); (8) added `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` to both Store adapters and extended `_MESSAGE_COLUMNS`/`_TURN_COLUMNS` to allow the bootstrap `epic_id` retro-stamp (all_locations). Integration test gained explicit assertions for each critique fix (title-via-preamble, time-travel-across-revert, meta_not_supported, operation_kind values)."
  },
  {
    "id": "scope-2",
    "severity": "significant",
    "status": "addressed",
    "concern": "Search for related code that handles the same concept. Is the reported issue a symptom of something broader?: I checked the spec's tool surface around `edit_epic` in `planning-bot-spec.md` lines 1703-1740. The plan deliberately returns `not_yet_supported` for `changes.sprints` and `changes.state`, which is a scoped Sprint 2a tradeoff because sprints/state gating are later sprint work, but it also omits `changes.meta` handling from the schema discussion even though the spec's change object includes `meta?: { title?, goal? }`; this should be either intentionally rejected or mapped to body edits so callers do not get silent schema drift.",
    "evidence": "Rev 2 addresses all 12 open critique flags by editing the existing six-phase structure rather than restructuring. Key changes: (1) added a no-epic mode to `run_turn` (epic_id=None), with `create_epic` retro-stamping the inbound message and bot_turn (FLAG-001/issue_hints-1/callers); (2) split parser into lenient `parse()` + strict `validate_for_write()` so reads/time-travel survive malformed bodies (FLAG-002/correctness-1); (3) redefined `_preamble` to include the `# Title` line per spec \u00a72606, making `replace_section('_preamble', ...)` the canonical title-edit path (issue_hints-2); (4) `reverted_to` events now snapshot full pre-revert body + checklist in `prior_state` so backward replay works across reverts (FLAG-003/correctness-2); (5) `create_epic` writes `epics.title`/`goal` exclusively from parsed values, never raw args (correctness-3); (6) read tools register with `operation_kind='read'` (scope-1); (7) `edit_epic.changes.meta` is explicitly rejected with `meta_not_supported` and a hint to use body sections (scope-2); (8) added `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` to both Store adapters and extended `_MESSAGE_COLUMNS`/`_TURN_COLUMNS` to allow the bootstrap `epic_id` retro-stamp (all_locations). Integration test gained explicit assertions for each critique fix (title-via-preamble, time-travel-across-revert, meta_not_supported, operation_kind values)."
  },
  {
    "id": "all_locations",
    "severity": "significant",
    "status": "open",
    "concern": "Does the change touch all locations AND supporting infrastructure?: Checked all locations touched by `run_turn(epic_id=None)`: `agent_kit/ports.py` still types `create_turn(epic_id: str)`, `agent_kit/envelope.py` types `Envelope.epic_id: str`, `agent_kit/envelope.schema.json` requires a non-empty string, and `arnold/cli.py` currently requires `--epic`. The revised plan mentions CLI no-epic plumbing but does not explicitly include the protocol/envelope/schema changes needed to keep all call boundaries consistent.",
    "evidence": "Checked all locations touched by `run_turn(epic_id=None)`: `agent_kit/ports.py` still types `create_turn(epic_id: str)`, `agent_kit/envelope.py` types `Envelope.epic_id: str`, `agent_kit/envelope.schema.json` requires a non-empty string, and `arnold/cli.py` currently requires `--epic`. The revised plan mentions CLI no-epic plumbing but does not explicitly include the protocol/envelope/schema changes needed to keep all call boundaries consistent."
  },
  {
    "id": "callers",
    "severity": "significant",
    "status": "addressed",
    "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: I inspected `agent_kit/loop.py` and `tests/test_run_turn.py`; current callers of `run_turn` always provide an `epic_id`, and test helpers seed an `epics` row first. The planned `create_epic` tool does not fit this caller contract for a brand-new epic: using a non-existent id would fail the current lock/message foreign-key path, while using an existing placeholder epic would make the create tool semantically odd unless the loop/CLI grows an explicit no-epic or inbox mode.",
    "evidence": "Rev 2 addresses all 12 open critique flags by editing the existing six-phase structure rather than restructuring. Key changes: (1) added a no-epic mode to `run_turn` (epic_id=None), with `create_epic` retro-stamping the inbound message and bot_turn (FLAG-001/issue_hints-1/callers); (2) split parser into lenient `parse()` + strict `validate_for_write()` so reads/time-travel survive malformed bodies (FLAG-002/correctness-1); (3) redefined `_preamble` to include the `# Title` line per spec \u00a72606, making `replace_section('_preamble', ...)` the canonical title-edit path (issue_hints-2); (4) `reverted_to` events now snapshot full pre-revert body + checklist in `prior_state` so backward replay works across reverts (FLAG-003/correctness-2); (5) `create_epic` writes `epics.title`/`goal` exclusively from parsed values, never raw args (correctness-3); (6) read tools register with `operation_kind='read'` (scope-1); (7) `edit_epic.changes.meta` is explicitly rejected with `meta_not_supported` and a hint to use body sections (scope-2); (8) added `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` to both Store adapters and extended `_MESSAGE_COLUMNS`/`_TURN_COLUMNS` to allow the bootstrap `epic_id` retro-stamp (all_locations). Integration test gained explicit assertions for each critique fix (title-via-preamble, time-travel-across-revert, meta_not_supported, operation_kind values)."
  },
  {
    "id": "FLAG-005",
    "severity": "significant",
    "status": "open",
    "concern": "Bootstrap API consistency: the plan changes `run_turn` to accept `epic_id=None` but does not explicitly update all public/protocol boundaries that currently require a concrete epic id.",
    "evidence": "`agent_kit/ports.py` has `Store.create_turn(epic_id: str)`, `agent_kit/envelope.py` has `Envelope.epic_id: str`, `agent_kit/envelope.schema.json` requires `epic_id` as a non-empty string, and `arnold/cli.py` currently requires `--epic` and uses `args.epic` in the error envelope path."
  },
  {
    "id": "correctness",
    "severity": "significant",
    "status": "open",
    "concern": "Are the proposed changes technically correct?: Checked the revised no-epic branch against abort, provider-error, tool-error, defer, and final-response returns in `agent_kit/loop.py`. Those code paths currently call `_abort_turn()` or `_envelope()` with the original local `epic_id` parameter, so the plan needs an explicit local `active_epic_id = context.metadata.get('epic_id')` handoff before every envelope return or an envelope schema change; otherwise no-epic turns that create an epic, defer, error, or finish without creating one can serialize invalid or misleading envelopes.",
    "evidence": "Checked the revised no-epic branch against abort, provider-error, tool-error, defer, and final-response returns in `agent_kit/loop.py`. Those code paths currently call `_abort_turn()` or `_envelope()` with the original local `epic_id` parameter, so the plan needs an explicit local `active_epic_id = context.metadata.get('epic_id')` handoff before every envelope return or an envelope schema change; otherwise no-epic turns that create an epic, defer, error, or finish without creating one can serialize invalid or misleading envelopes."
  },
  {
    "id": "callers-1",
    "severity": "significant",
    "status": "open",
    "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked existing Python and CLI callers of `run_turn`. The revised plan is additive for existing tests and resident callers that still pass concrete epic ids, and it adds a new CLI no-epic path for bootstrap, but it must also update the CLI exception envelope path because `arnold/cli.py` currently builds an error envelope with `epic_id=args.epic`; with optional `--epic`, that can become missing or `None` unless explicitly handled.",
    "evidence": "Checked existing Python and CLI callers of `run_turn`. The revised plan is additive for existing tests and resident callers that still pass concrete epic ids, and it adds a new CLI no-epic path for bootstrap, but it must also update the CLI exception envelope path because `arnold/cli.py` currently builds an error envelope with `epic_id=args.epic`; with optional `--epic`, that can become missing or `None` unless explicitly handled."
  },
  {
    "id": "callers-2",
    "severity": "significant",
    "status": "open",
    "concern": "Find the callers of the changed function. What arguments do they actually pass? Does the fix handle all of them?: Checked current callers of `store.create_turn` in tests, resident recovery, and the loop. Existing callers pass concrete ids, while the new no-epic loop path passes `None`; the database allows NULL for `bot_turns.epic_id`, but the `Store` protocol and both adapter signatures are still typed as `str`, so the plan should explicitly update those signatures to `str | None` to match the intended caller values.",
    "evidence": "Checked current callers of `store.create_turn` in tests, resident recovery, and the loop. Existing callers pass concrete ids, while the new no-epic loop path passes `None`; the database allows NULL for `bot_turns.epic_id`, but the `Store` protocol and both adapter signatures are still typed as `str`, so the plan should explicitly update those signatures to `str | None` to match the intended caller values."
  }
]



        Requirements:
        - Before addressing individual flags, check: does any flag suggest the plan is targeting the wrong code or the wrong root cause? If so, consider whether the plan needs a new approach rather than adjustments. Explain your reasoning.
        - Update the plan to address the significant issues.
        - Keep the plan readable and executable.
        - Return flags_addressed with the exact flag IDs you addressed.
        - Include `changes_summary` as a short plain-English summary of what changed in the revision. If there were no concrete flags, say that explicitly (for example: `No critique flags were raised; refined wording and kept the plan aligned for execution.`).
        - Preserve or improve success criteria quality. Each criterion must have a `priority` of `must`, `should`, or `info`. Promote or demote priorities if critique feedback reveals a criterion was over- or under-weighted.
        - Verify that the plan remains aligned with the user's original intent, not just internal plan quality.
        - Remove unjustified scope growth. If critique raised scope creep, narrow the plan back to the original idea unless the broader work is strictly required.
        - Maintain the structural template: H1 title, ## Overview, phase sections with numbered step sections, ## Execution Order or ## Validation Order.
        - CRITICAL: Your entire revised plan markdown (all sections) must be output as the `plan` field in the structured output. The prose response must not contain the plan text.
        - CRITICAL: Return only the structured JSON object for the schema fields `plan`, `changes_summary`, `flags_addressed`, `assumptions`, `success_criteria`, and `questions`. Do not add commentary before or after the JSON object.

        Plan template — simple format (adapt to the actual repo and scope):
````md
# Implementation Plan: [Title]

## Overview
Summarize the goal, current repository shape, and the constraints that matter.

## Main Phase

### Step 1: Audit the current behavior (`megaplan/prompts.py`)
**Scope:** Small
1. **Inspect** the current implementation and call out the exact insertion points (`megaplan/prompts.py:29`).

### Step 2: Add the first change (`megaplan/evaluation.py`)
**Scope:** Medium
1. **Implement** the smallest viable change with exact file references (`megaplan/evaluation.py:1`).
2. **Capture** any tricky behavior with a short example.
   ```python
   issues = validate_plan_structure(plan_text)
   ```

### Step 3: Wire downstream behavior (`megaplan/handlers.py`, `megaplan/workers.py`)
**Scope:** Medium
1. **Update** the runtime flow in the touched files (`megaplan/handlers.py:400`, `megaplan/workers.py:199`).

### Step 4: Prove the change (`tests/test_evaluation.py`, `tests/test_megaplan.py`)
**Scope:** Small
1. **Run** the cheapest targeted checks first (`tests/test_evaluation.py:1`).
2. **Finish** with broader verification once the wiring is in place (`tests/test_megaplan.py:1`).

## Execution Order
1. Update prompts and mocks before enforcing stricter validation.
2. Land higher-risk wiring after the validator and tests are ready.

## Validation Order
1. Start with focused unit tests.
2. Run the broader suite after the flow changes are in place.
````

For complex plans, use multiple phases:
````md
## Phase 1: Foundation — Dependencies, DB, Types

### Step 1: Install dependencies (`package.json`)
...

### Step 2: Create database migration (`supabase/migrations/`)
...

## Phase 2: Core Integration

### Step 3: Port the main component (`src/components/`)
...
````

Template guidance:
- Simple plans: use `## Main Phase` with `### Step N:` sections underneath.
- Complex plans: use multiple `## Phase N:` sections, each containing `### Step N:` steps. Step numbers are global (not per-phase).
- The flat `## Step N:` format (without phases) also works for backwards compatibility.
- Key invariants: one H1 title, one `## Overview`, numbered step sections (`### Step N:` or `## Step N:`), and at least one ordering section.

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/agent_kit/envelope.py"
}
```

> TOOL

tool_result Read
```
1	"""Invocation-mode result envelope for Arnold turns.
2	
3	The stable JSON helpers in this module are the only supported serialization
4	path for envelopes and streamed events. ``serialize_for_diff`` is narrower:
5	it exists only for CLI-vs-Python envelope equivalence tests and must not be
6	used for stream-vs-envelope comparisons.
7	"""
8	
9	from __future__ import annotations
10	
11	from dataclasses import asdict, dataclass, field, is_dataclass
12	import json
13	from typing import Any, Literal
14	
15	
16	Outcome = Literal["completed", "blocked_on_caller", "errored", "aborted"]
17	EventKind = Literal["tool_call", "activity", "turn_start", "turn_end"]
18	
19	
20	@dataclass(frozen=True)
21	class EnvelopeError:
22	    code: str
23	    message: str
24	    retryable: bool = False
25	
26	
27	@dataclass(frozen=True)
28	class StateDelta:
29	    body_diff: str = ""
30	    checklist_changes: list[dict[str, Any]] = field(default_factory=list)
31	    sprint_changes: list[dict[str, Any]] = field(default_factory=list)
32	    state_transition: dict[str, Any] | None = None
33	
34	
35	@dataclass(frozen=True)
36	class Event:
37	    ts: str
38	    kind: EventKind
39	    name: str | None = None
40	    text: str | None = None
41	    ms: int | None = None
42	    tool_call_id: str | None = None
43	    started_at: str | None = None
44	    completed_at: str | None = None
45	    details: dict[str, Any] = field(default_factory=dict)
46	
47	
48	@dataclass(frozen=True)
49	class Envelope:
50	    turn_id: str
51	    epic_id: str
52	    epic_state_before: str
53	    epic_state_after: str
54	    reply: str
55	    state_delta: StateDelta = field(default_factory=StateDelta)
56	    questions: list[str] = field(default_factory=list)
57	    events: list[Event] = field(default_factory=list)
58	    tool_call_count: int = 0
59	    outcome: Outcome = "completed"
60	    error: EnvelopeError | None = None
61	    envelope_version: str = "1"
62	    started_at: str | None = None
63	    completed_at: str | None = None
64	
65	    def to_dict(self) -> dict[str, Any]:
66	        return _drop_none(_to_plain(self))
67	
68	    def to_json(self) -> str:
69	        return stable_json_dumps(self.to_dict())
70	
71	
72	def stable_json_dumps(value: Any) -> str:
73	    """Serialize JSON with byte-stable ordering and compact separators."""
74	
75	    return json.dumps(
76	        _drop_none(_to_plain(value)),
77	        sort_keys=True,
78	        separators=(",", ":"),
79	        ensure_ascii=False,
80	    )
81	
82	
83	def event_to_json(event: Event) -> str:
84	    return stable_json_dumps(event)
85	
86	
87	def serialize_for_diff(envelope: Envelope | dict[str, Any]) -> str:
88	    """Return a byte-stable comparison form for CLI-vs-Python tests only.
89	
90	    This strips the non-deterministic fields called out by the Subagent
91	    Contract: envelope ``reply``, event ``text``, and ``started_at`` /
92	    ``completed_at`` timestamps wherever they appear. Streaming tests must
93	    compare real events, not this projection.
94	    """
95	
96	    data = _drop_none(_to_plain(envelope))
97	    return stable_json_dumps(_strip_diff_nondeterminism(data))
98	
99	
100	def _to_plain(value: Any) -> Any:
101	    if is_dataclass(value):
102	        return asdict(value)
103	    if isinstance(value, dict):
104	        return {key: _to_plain(item) for key, item in value.items()}
105	    if isinstance(value, list):
106	        return [_to_plain(item) for item in value]
107	    if isinstance(value, tuple):
108	        return [_to_plain(item) for item in value]
109	    return value
110	
111	
112	def _drop_none(value: Any) -> Any:
113	    if isinstance(value, dict):
114	        return {
115	            key: _drop_none(item)
116	            for key, item in value.items()
117	            if item is not None
118	        }
119	    if isinstance(value, list):
120	        return [_drop_none(item) for item in value]
121	    return value
122	
123	
124	def _strip_diff_nondeterminism(value: Any) -> Any:
125	    if isinstance(value, dict):
126	        return {
127	            [REDACTED](item)
128	            for key, item in value.items()
129	            if key not in {"reply", "text", "started_at", "completed_at"}
130	        }
131	    if isinstance(value, list):
132	        return [_strip_diff_nondeterminism(item) for item in value]
133	    return value
134
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"epic_id\\|required\" /Users/user_c042661f/Documents/arnold-v2/agent_kit/envelope.schema.json | head -20",
  "description": "Check envelope schema"
}
```

> TOOL

tool_result Bash
```
7:  "required": [
10:    "epic_id",
29:    "epic_id": {
90:      "required": [
129:      "required": [
173:      "required": [
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/agent_kit/envelope.schema.json",
  "offset": 25,
  "limit": 15
}
```

> TOOL

tool_result Read
```
25	    "turn_id": {
26	      "type": "string",
27	      "minLength": 1
28	    },
29	    "epic_id": {
30	      "type": "string",
31	      "minLength": 1
32	    },
33	    "epic_state_before": {
34	      "type": "string"
35	    },
36	    "epic_state_after": {
37	      "type": "string"
38	    },
39	    "reply": {
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/arnold-v2/arnold/cli.py"
}
```

> TOOL

tool_result Read
```
1	"""Command-line interface for Arnold invocation mode."""
2	
3	from __future__ import annotations
4	
5	import argparse
6	import asyncio
7	import json
8	import os
9	import signal
10	import sys
11	from threading import Event as ThreadingEvent
12	from typing import Sequence
13	from uuid import uuid4
14	
15	from agent_kit.envelope import Envelope, EnvelopeError, StateDelta, event_to_json
16	from agent_kit.loop import run_turn
17	from agent_kit.model import AnthropicModel, FakeModel
18	from agent_kit.store.sqlite import SQLiteStore
19	
20	
21	EXIT_CODES = {
22	    "completed": 0,
23	    "errored": 1,
24	    "blocked_on_caller": 2,
25	    "aborted": 3,
26	}
27	
28	
29	def main(argv: Sequence[str] | None = None) -> int:
30	    parser = _build_parser()
31	    args = parser.parse_args(argv)
32	    if args.command == "turn":
33	        return _turn(args)
34	    if args.command == "resident":
35	        return _resident(args)
36	    parser.print_help(sys.stderr)
37	    return 1
38	
39	
40	def _build_parser() -> argparse.ArgumentParser:
41	    parser = argparse.ArgumentParser(prog="arnold")
42	    subparsers = parser.add_subparsers(dest="command")
43	
44	    turn = subparsers.add_parser("turn")
45	    turn.add_argument("--epic", required=True)
46	    input_group = turn.add_mutually_exclusive_group(required=True)
47	    input_group.add_argument("--input")
48	    input_group.add_argument("--from-stdin", action="store_true")
49	    turn.add_argument("--stream-events", action="store_true")
50	    turn.add_argument("--store", choices=["sqlite", "supabase"], default="sqlite")
51	    turn.add_argument("--db", default="arnold.sqlite3")
52	    turn.add_argument(
53	        "--model-id",
54	        default=os.environ.get("ARNOLD_MODEL_ID", "claude-opus-4-7"),
55	    )
56	
57	    resident = subparsers.add_parser("resident")
58	    resident.add_argument(
59	        "--model-id",
60	        default=os.environ.get("ARNOLD_MODEL_ID", "claude-opus-4-7"),
61	    )
62	    resident.add_argument(
63	        "--status-debounce-seconds",
64	        type=float,
65	        default=1.0,
66	    )
67	    return parser
68	
69	
70	def _turn(args: argparse.Namespace) -> int:
71	    cancel_event = ThreadingEvent()
72	    previous_sigint = signal.getsignal(signal.SIGINT)
73	
74	    def _handle_sigint(signum, frame):  # noqa: ARG001
75	        cancel_event.set()
76	
77	    signal.signal(signal.SIGINT, _handle_sigint)
78	    try:
79	        input_text = sys.stdin.read() if args.from_stdin else args.input
80	        store = _build_store(args)
81	        model = _build_model(args.model_id)
82	
83	        def on_event(event):
84	            if args.stream_events:
85	                sys.stderr.write(event_to_json(event) + "\n")
86	                sys.stderr.flush()
87	
88	        try:
89	            envelope = run_turn(
90	                epic_id=args.epic,
91	                input=input_text,
92	                store=store,
93	                model=model,
94	                model_id=args.model_id,
95	                on_event=on_event,
96	                cancel_event=cancel_event,
97	            )
98	        except Exception as exc:
99	            envelope = Envelope(
100	                turn_id=f"turn_cli_{uuid4().hex}",
101	                epic_id=args.epic,
102	                epic_state_before="unknown",
103	                epic_state_after="unknown",
104	                reply="",
105	                state_delta=StateDelta(),
106	                outcome="errored",
107	                error=EnvelopeError(
108	                    code="cli_error",
109	                    message=str(exc),
110	                    retryable=False,
111	                ),
112	            )
113	        finally:
114	            store.close()
115	
116	        sys.stdout.write(envelope.to_json() + "\n")
117	        return EXIT_CODES[envelope.outcome]
118	    finally:
119	        signal.signal(signal.SIGINT, previous_sigint)
120	
121	
122	def _resident(args: argparse.Namespace) -> int:
123	    try:
124	        asyncio.run(_run_resident(args))
125	    except KeyboardInterrupt:
126	        return 0
127	    except Exception as exc:
128	        sys.stderr.write(f"resident failed: {exc}\n")
129	        return 1
130	    return 0
131	
132	
133	async def _run_resident(args: argparse.Namespace) -> None:
134	    from agent_kit.blob.supabase_storage import SupabaseStorageBlob
135	    from agent_kit.ledger import Ledger, Reconciler
136	    from agent_kit.resident import ResidentRunner
137	    from agent_kit.transport.discord import DiscordTransport
138	
139	    try:
140	        from groq import Groq
141	    except ImportError as exc:
142	        raise RuntimeError("groq SDK is required for arnold resident") from exc
143	
144	    store = _build_supabase_store()
145	    blob = SupabaseStorageBlob.from_env()
146	    ledger = Ledger(store)
147	    groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
148	    transport = DiscordTransport(
149	        store=store,
150	        blob=blob,
151	        ledger=ledger,
152	        groq_client=groq_client,
153	    )
154	    model = _build_model(args.model_id)
155	    reconciler = Reconciler(
156	        store,
157	        model=model,
158	        transport=transport,
159	        blob=blob,
160	        groq_client=groq_client,
161	    )
162	    runner = ResidentRunner(
163	        store=store,
164	        model=model,
165	        model_id=args.model_id,
166	        transport=transport,
167	        blob=blob,
168	        ledger=ledger,
169	        reconciler=reconciler,
170	        status_debounce_seconds=args.status_debounce_seconds,
171	    )
172	    stop_event = asyncio.Event()
173	    loop = asyncio.get_running_loop()
174	    for sig in (signal.SIGINT, signal.SIGTERM):
175	        try:
176	            loop.add_signal_handler(sig, stop_event.set)
177	        except NotImplementedError:
178	            pass
179	    try:
180	        runner.start()
181	        await stop_event.wait()
182	    finally:
183	        runner.stop()
184	        store.close()
185	
186	
187	def _build_model(model_id: str):
188	    script = os.environ.get("ARNOLD_FAKE_MODEL_SCRIPT")
189	    if script is not None:
190	        return FakeModel(
191	            seed=os.environ.get("ARNOLD_FAKE_MODEL_SEED", "0"),
192	            script=json.loads(script),
193	        )
194	    return AnthropicModel(model_id=model_id)
195	
196	
197	def _build_store(args: argparse.Namespace):
198	    if args.store == "sqlite":
199	        return SQLiteStore(args.db)
200	    return _build_supabase_store()
201	
202	
203	def _build_supabase_store():
204	    from agent_kit.store.supabase import SupabaseStore
205	
206	    return SupabaseStore.from_env()
207	
208	
209	if __name__ == "__main__":
210	    raise SystemExit(main())
211
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"_envelope\\|_abort_turn\\|epic_id=\" /Users/user_c042661f/Documents/arnold-v2/agent_kit/loop.py | head -40",
  "description": "Check envelope returns"
}
```

> TOOL

tool_result Bash
```
50:            epic_id=epic_id,
54:            epic_id=epic_id,
80:                epic_id=epic_id,
93:            epic_id=epic_id,
123:            return _abort_turn(store, turn, epic_id, state_before, events, reply_buffer)
168:                    epic_id=epic_id,
173:                return _envelope(
175:                    epic_id=epic_id,
195:                    epic_id=epic_id,
199:                return _envelope(
201:                    epic_id=epic_id,
227:                return _abort_turn(store, turn, epic_id, state_before, events, reply_buffer)
233:                        return _abort_turn(
268:                            epic_id=epic_id,
273:                        return _envelope(
275:                            epic_id=epic_id,
299:                        return _envelope(
301:                            epic_id=epic_id,
331:                return _envelope(
333:                    epic_id=epic_id,
342:            return _envelope(
344:                epic_id=epic_id,
367:def _abort_turn(
376:    return _envelope(
378:        epic_id=epic_id,
387:def _envelope(
401:        epic_id=epic_id,
```

> AGENT

The remaining flags are one cohesive cluster: thread `Optional[str]` through every public boundary that the rev-2 plan changed in spirit but didn't enumerate (Store.create_turn signature, Envelope dataclass + JSON schema, CLI `--epic`, local `epic_id` variable in `loop.py`'s envelope/abort returns). Plus issue_hints-2 (`body_version` deferral) needs to be promoted from quiet deferral to an explicit accepted tradeoff. None of this suggests the plan is targeting wrong code — it's a single Step-14 expansion.

> TOOL

tool_use StructuredOutput
```json
{
  "plan": "# Implementation Plan: Sprint 2a — Editorial Core (rev 3)\n\n## Overview\n\nSprint 2a gives Arnold a *document* to edit. Today the codebase has an `epics` table (`supabase/migrations/202604300001_001_core.sql`), a turn loop (`agent_kit/loop.py`) that requires `epic_id` to acquire `epic_locks` before any model call, a `Store` protocol (`agent_kit/ports.py`) backed by SQLite + Postgres adapters, an `Envelope` dataclass (`agent_kit/envelope.py:48`) and JSON schema (`agent_kit/envelope.schema.json:29`) that both require a non-empty `epic_id` string, a CLI (`arnold/cli.py:45`) with `--epic` required, and a `system_logs` sink. The only registered tools are `send_message`, `set_activity`, `defer_to_caller`, `view_image`, `send_image`, `update_image_metadata`.\n\nThis sprint adds (1) two new tables (`checklist_items`, `epic_events`); (2) a body parser/serializer with section addressing; (3) Store CRUD for epics/checklist/events; (4) ~10 new tools (`create_epic`, `edit_epic`, `revert`, `render_epic`, plus reads); (5) a no-epic turn-mode threaded consistently through the loop, Store protocol, Envelope, JSON schema, and CLI; (6) a turn-end `epic_outline` log.\n\nConstraints worth pinning up front (now reflecting all critique fixes):\n\n- **Bootstrap path threaded through every boundary.** `run_turn(epic_id: Optional[str] = None)`. The DB columns `messages.epic_id`, `bot_turns.epic_id`, and `system_logs.epic_id` are already nullable. Rev 3 also makes the public surface match: `Store.create_turn(epic_id: str | None)`, `Envelope.epic_id: str | None`, `envelope.schema.json` allows `null`, CLI `--epic` is optional, `loop.py` uses an `active_epic_id` local that is updated by `create_epic` before every envelope/abort return. (FLAG-001, FLAG-005, issue_hints-1, all_locations, correctness, callers-1, callers-2.)\n- **Parser split:** `parse(body)` is **lenient** — accepts any input, never raises. **`validate_for_write(parsed)`** is **strict** and called only by write paths. (FLAG-002, correctness-1.)\n- **`_preamble` includes the `# Title` line** per spec §2606. Replace via `replace_section('_preamble', '# New Title\\n')` is the canonical title-edit path. (issue_hints-2 rev1.)\n- **Title/goal columns are parser-derived only.** (correctness-3.)\n- **`reverted_to` events store full pre-revert body, title, goal, and checklist snapshot in `prior_state`** so backward replay across reverts is correct. (FLAG-003, correctness-2.)\n- **Read tools register with `operation_kind='read'`.** (scope-1.)\n- **`edit_epic.changes.meta` is rejected** with `meta_not_supported`. (scope-2.)\n- **Mutually-exclusive body ops** in a single `edit_epic.body` payload; mixing returns `body_op_conflict`.\n- **`expected_diff` equivalence:** `\\n` line endings, strip trailing whitespace per line, drop trailing blank lines (spec §494).\n- **Out of scope:** sprints, sprint_items, codebases, code_artifacts, feedback, second_opinions, image generation. `edit_epic.changes.sprints` and `changes.state` return `not_yet_supported`.\n- **`body_version` (spec §2606 example) is intentionally deferred.** The main Data Model (spec §1311–1320) does not define a `body_version` column. The audit trail in `epic_events.body_edit` already captures every body mutation atomically with title/goal updates, which satisfies the title/body sync acceptance test (#7) without introducing a new column. Adding `body_version` later is an additive migration. (issue_hints-2 rev2 — accepted tradeoff.)\n- CLAUDE.md forbids creating a `megaplan/` directory; the existing one is harness state, not a target.\n\nSix phases. Phases 1–3 land schema, parser, and store surface. Phase 4 lands tools. Phase 5 wires the loop bootstrap (now thread-complete across protocol/envelope/schema/CLI) and outline log. Phase 6 covers the integration fixture.\n\n---\n\n## Phase 1: Schema — checklist_items, epic_events\n\n### Step 1: Postgres migration (`supabase/migrations/202604300004_004_editorial_core.sql`)\n**Scope:** Small\n1. **Create** `checklist_items` matching spec §1322: `id TEXT PK`, `epic_id TEXT NOT NULL REFERENCES epics(id) ON DELETE CASCADE`, `content TEXT NOT NULL`, `status TEXT CHECK IN ('open','done','skipped','superseded')`, `position INTEGER NOT NULL`, `source TEXT CHECK IN ('bot_inferred','user_requested','carried_over','default_seed','second_opinion')`, `skip_reason TEXT`, `superseded_by_item_id TEXT REFERENCES checklist_items(id)`, `created_at TIMESTAMPTZ DEFAULT now()`, `completed_at TIMESTAMPTZ`. Index `(epic_id, status, position)`.\n2. **Create** `epic_events` matching spec §1381: `id TEXT PK`, `epic_id TEXT NOT NULL REFERENCES epics(id) ON DELETE CASCADE`, `transaction_id TEXT NOT NULL`, `event_type TEXT CHECK IN ('body_edit','checklist_change','sprints_change','state_change','forced_handoff','created','code_referenced','codebase_added','image_generated','second_opinion_requested','reverted_to','sprint_status_change')`, `summary TEXT NOT NULL`, `prior_state JSONB`, `turn_id TEXT REFERENCES bot_turns(id) ON DELETE SET NULL`, `occurred_at TIMESTAMPTZ DEFAULT now()`. Indexes `(epic_id, occurred_at DESC)` and `(transaction_id)`.\n\n### Step 2: SQLite mirror (`agent_kit/store/migrations/sqlite/004_editorial_core.sql`)\n**Scope:** Small\n1. **Mirror** the Postgres migration (TEXT for everything; `prior_state` is a TEXT JSON blob).\n2. **Register** `prior_state` in `_JSON_COLUMNS` at `agent_kit/store/sqlite.py:17` and `agent_kit/store/supabase.py:12`.\n\n### Step 3: Update Supabase truncate fixture (`tests/test_supabase_store.py:33`)\n**Scope:** Small\n1. **Add** `checklist_items` and `epic_events` to the `TRUNCATE TABLE … RESTART IDENTITY CASCADE` block.\n\n---\n\n## Phase 2: Body parser/serializer\n\n### Step 4: Parser module — lenient parse, strict validate (`agent_kit/body.py`)\n**Scope:** Medium\n1. **Public surface** (everything else `_private`):\n   - `parse(body: str) -> ParsedBody` — **lenient**. Never raises. `ParsedBody`: `title: str | None`, `goal_first_paragraph: str | None`, `preamble: str` (raw text from byte 0 up to but not including the first `##` line, INCLUDING the `# Title` line and any leading text), `sections: list[Section]`. `Section`: `name`, `content`, `subheadings`, `line_count`. Title is the first non-blank preamble line matching `^#\\s+(.+?)\\s*$`; if absent or empty → `None`. Goal is the first paragraph (text before first blank line, whitespace-stripped) of the section named exactly `Goal`; if absent or empty → `None`. Bodies with no `##` headings: `sections=[]`, `preamble=<entire body>`.\n   - `serialize(parsed: ParsedBody) -> str` — round-trip identity.\n   - `validate_for_write(parsed: ParsedBody) -> None` — **strict**. Raises `BodyValidationError(\"body_missing_required_section: title\")` or `…goal`. Called by every write path.\n   - `outline(parsed: ParsedBody) -> dict` — `{title, sections: [{name, line_count, subheadings}], total_lines}`.\n2. **Heading rules** (spec §503–514): `^##\\s+(.+?)\\s*$` at top level only; `###`+ stay inside parents; track ``` and ~~~ fences (indented code-block edge case documented but not handled in v1); section names case-sensitive.\n3. **Section operations** as pure functions on `ParsedBody`: `replace_section`, `append_to_section`, `add_section(position='after:Foo'|'before:Foo'|'start'|'end')`, `remove_section`, `rename_section`, `reorder(new_order)`. Typed errors: `SectionNotFound`, `SectionExists`, `InvalidPosition`. `_preamble` is addressable: `replace_section('_preamble', '# New Title\\n')` updates the title (spec §2606); `rename_section` from/to `_preamble` rejected.\n4. **Diff helpers:** `compute_diff(old, new)` wraps `difflib.unified_diff(splitlines(keepends=True), …, n=3)`; `diffs_equivalent(a, b)` normalises per spec §494 (`\\r\\n→\\n`, strip trailing whitespace per line, drop trailing blank lines).\n5. **No third-party deps** beyond stdlib (`difflib`, `re`). No imports of Store/ports/tool_kit.\n\n### Step 5: Default template + checklist seed (`agent_kit/templates.py`)\n**Scope:** Small\n1. **`DEFAULT_BODY_TEMPLATE(title, goal) -> str`** emits the six-section design-doc skeleton.\n2. **`DEFAULT_CHECKLIST_SEED: list[str]`** — 18 items from spec §634, all `source='default_seed'`, `status='open'`, positions 1–18.\n3. **No adaptation logic** in v1 (settled SD-004); the bot adapts via post-create `edit_epic` calls.\n\n### Step 6: Parser unit tests (`tests/test_body_parser.py`)\n**Scope:** Medium\n1. **Round-trip identity** for ≥6 fixtures (preamble-only, single section, six-section template, sub-headings, fenced `## Step 1`, non-empty preamble before first `##`).\n2. **Section ops** — only the targeted section changes; every other section's serialised form byte-equal.\n3. **`_preamble` covers the title** — `replace_section('_preamble', '# New Title\\n')` round-trips to `parsed.title=='New Title'`; replacing with `''` round-trips to `title=None` and `validate_for_write` raises `body_missing_required_section: title`.\n4. **Lenient parse** — `''`, `'just text\\n'`, `'## Goal\\n\\ngoal\\n'` (no title), `'# Title\\n'` (no Goal), `'# Title\\n\\n## NotGoal\\n\\nx\\n'` all return `ParsedBody` without raising; `validate_for_write` rejects each.\n5. **Code-fence guard** — body with ` ```\\n## Inside\\n``` ` parses as a single preamble.\n6. **Diff equivalence** — true on `\\r\\n` vs `\\n` / trailing-space / trailing-blank-line differences only; false on real content delta.\n\n---\n\n## Phase 3: Store surface for epics, checklist, events\n\n### Step 7: Extend `Store` protocol (`agent_kit/ports.py`)\n**Scope:** Medium\n1. **Add** typed methods (Protocol + both adapters):\n   - `create_epic(*, title, goal, body, state='shaping') -> JSONDict`\n   - `load_epic(epic_id) -> JSONDict | None`\n   - `update_epic(epic_id, **changes) -> JSONDict` — guarded by `_EPIC_COLUMNS = {'title', 'goal', 'body', 'state', 'last_edited_at', 'last_active_at', 'planned_at'}`.\n   - `seed_checklist(epic_id, items: list[dict]) -> list[JSONDict]`\n   - `list_checklist_items(epic_id, *, status=None) -> list[JSONDict]`\n   - `update_checklist_item(item_id, **changes) -> JSONDict` — guarded by `_CHECKLIST_COLUMNS = {'content', 'status', 'position', 'skip_reason', 'superseded_by_item_id', 'completed_at'}`.\n   - `add_checklist_items(epic_id, items, start_position) -> list[JSONDict]`\n   - `delete_checklist_items(item_ids) -> int`\n   - `replace_checklist(epic_id, items) -> list[JSONDict]` — DELETE all + bulk INSERT.\n   - `record_epic_event(*, epic_id, transaction_id, event_type, summary, prior_state, turn_id) -> JSONDict`\n   - `list_epic_events(epic_id, *, since=None, until=None, kinds=None, limit=None) -> list[JSONDict]` ordered `(occurred_at, id) ASC`.\n   - `latest_transaction_id(epic_id) -> str | None`\n   - `events_by_transaction(transaction_id) -> list[JSONDict]`\n   - `list_recent_turns(*, n=10, epic_id=None) -> list[JSONDict]` — `bot_turns` ordered `started_at DESC LIMIT n`.\n   - `search_tool_calls_by(*, tool_name=None, epic_id=None, since=None, limit=20) -> list[JSONDict]`.\n2. **Update** `Store.create_turn` signature in the Protocol and both adapters to `epic_id: str | None` (callers-2). The DB column already permits NULL.\n3. **Update** `Store.create_message`, `update_message`, `update_turn`, and `log_system_event` already accept `epic_id` parameters of type `str | None`; verify no type narrowing is required and adjust if needed.\n\n### Step 8: Implement on `SupabaseStore` (`agent_kit/store/supabase.py`)\n**Scope:** Medium\n1. **Mirror** the protocol additions with concrete SQL using existing `_normalize`/`_json` helpers and `_new_id` (prefixes `'epic'`, `'check'`, `'evt'`).\n2. **Add** module-level `_EPIC_COLUMNS` and `_CHECKLIST_COLUMNS` next to `_MESSAGE_COLUMNS`/`_TURN_COLUMNS`/`_IMAGE_COLUMNS`. Wire `update_epic` and `update_checklist_item` through `self._update`.\n3. **Update `_TURN_COLUMNS`** to include `'epic_id'`. **Update `_MESSAGE_COLUMNS`** to include `'epic_id'`.\n4. **Confirm** `create_turn` parameter type is `str | None` and the existing INSERT (`agent_kit/store/supabase.py:113`) already passes it through unchanged (Postgres allows NULL on `bot_turns.epic_id`).\n\n### Step 9: Implement on `SQLiteStore` (`agent_kit/store/sqlite.py`)\n**Scope:** Medium\n1. **Mirror** Step 8: same methods, same `_EPIC_COLUMNS`/`_CHECKLIST_COLUMNS` constants, same `epic_id` additions to `_MESSAGE_COLUMNS`/`_TURN_COLUMNS`.\n2. **Add** `'prior_state'` to `_JSON_COLUMNS`. **Confirm** `create_turn` accepts `epic_id: str | None`.\n\n### Step 10: Extend the contract test (`tests/store_contract.py`)\n**Scope:** Small\n1. **Add** a tail block exercising the new surface: create an epic, seed checklist, append events with `transaction_id`s, list/filter events, query `latest_transaction_id`, verify ordering.\n2. **Add** an explicit assertion that `create_turn(epic_id=None)` succeeds and the row stores NULL.\n\n---\n\n## Phase 4: Tools — `create_epic`, `edit_epic`, `revert`, `render_epic`, reads\n\n### Step 11: Editorial write tools (`agent_kit/tools/editorial.py`)\n**Scope:** Large\n1. **Register each tool** via `@register_tool` with explicit JSON schemas and `operation_kind='write'`.\n2. **`create_epic(context, title, goal)`** —\n   - Build body via `templates.DEFAULT_BODY_TEMPLATE(title, goal)`.\n   - `parsed = body.parse(rendered)`; `body.validate_for_write(parsed)` — on `BodyValidationError`, return `{\"error\": \"body_missing_required_section\", \"field\": …}`.\n   - Inside `store.transaction()`:\n     - `epic = store.create_epic(title=parsed.title, goal=parsed.goal_first_paragraph, body=rendered, state='shaping')` (correctness-3: parsed values, never raw args).\n     - `store.seed_checklist(epic['id'], DEFAULT_CHECKLIST_SEED)`.\n     - `store.record_epic_event(epic_id=epic['id'], transaction_id=uuid4().hex, event_type='created', summary='Epic created with default design-doc template', prior_state=None, turn_id=context.turn_id)`.\n     - **Bootstrap retro-stamp:** `store.update_message(context.metadata['inbound_message_id'], epic_id=epic['id'])` and `store.update_turn(context.turn_id, epic_id=epic['id'])`. Set `context.metadata['epic_id'] = epic['id']`.\n   - Return `{\"epic_id\", \"title\", \"goal\", \"section_names\", \"checklist_count\": 18, \"transaction_id\"}`.\n3. **`edit_epic(context, epic_id, changes, change_summary, expected_diff?)`** —\n   - **Reject** unsupported keys: `changes.sprints` / `changes.state` → `not_yet_supported`; `changes.meta` → `meta_not_supported` with hint to use `body.sections._preamble` (title) or `body.sections.Goal` (goal).\n   - **Reject** mixed body ops (`new_content | sections | append | remove_sections | rename_section | reorder`) → `body_op_conflict`.\n   - **Body path:** load → parse → apply op → serialise → `validate_for_write` → `compute_diff`. If `expected_diff` provided and `not diffs_equivalent(...)`, return `{\"error\":\"expected_diff_mismatch\", \"actual_diff\":...}` and **do not write**.\n   - **Checklist path:** apply add/update/remove with snapshot capture for the event.\n   - **Inside one `store.transaction()`** with `transaction_id = uuid4().hex`:\n     - Body: `store.update_epic(epic_id, body=new_body, title=new_parsed.title, goal=new_parsed.goal_first_paragraph, last_edited_at=now())` + `record_epic_event(event_type='body_edit', prior_state={'body': old, 'title': old_title, 'goal': old_goal})`.\n     - Checklist: per-item ops + `record_epic_event(event_type='checklist_change', prior_state={'items': [...full snapshot...]})`.\n   - Return `{\"transaction_id\", \"diff\", \"section_names\", \"change_summary\"}`.\n4. **`revert(context, epic_id, event_id?=None)`** —\n   - Resolve target events via `events_by_transaction(latest_transaction_id(epic_id))` or `events_by_transaction(target_event.transaction_id)`.\n   - **Capture pre-revert state:** `prior_state = {'body': current_body, 'title': current_title, 'goal': current_goal, 'checklist': [...full snapshot...], 'reverted_transaction_id': txn, 'reverted_event_ids': [...]}`. (FLAG-003.)\n   - Apply each target event's `prior_state` in reverse: `body_edit` → `update_epic(...)`; `checklist_change` → `replace_checklist(...)`.\n   - Append `reverted_to` event with the captured pre-revert `prior_state`.\n   - Return `{\"transaction_id\", \"reverted_event_count\", \"summary\"}`.\n5. **`render_epic(context, epic_id, format='markdown')`** — `'markdown'` returns the body as-is; `'html'` → `not_yet_supported`.\n\n### Step 12: Editorial read tools (`agent_kit/tools/editorial_reads.py`)\n**Scope:** Medium\n1. **Register** each tool with **`operation_kind='read'`** (scope-1).\n2. **`get_epic(epic_id, sections=None)`** — `parse(epic['body'])`; return `{title, goal, body_full, sections, section_names, state}`. Lenient parse handles legacy/malformed bodies.\n3. **`get_section_names(epic_id)`** — `[s.name for s in parse(epic['body']).sections]`.\n4. **`get_history(epic_id, kind=None, since=None)`** — `list_epic_events(...)` reversed.\n5. **`get_self_understanding(epic_id)`** — `{goal, state, open_checklist_count, section_names, recent_events: last 3}`. Document inline that the spec §1068 7-section structure lights up incrementally.\n6. **`get_epic_at_time(epic_id, timestamp)`** — backward replay from current state: walk events with `occurred_at > timestamp` in descending order; for each, undo using `prior_state` (`body_edit` → restore body; `checklist_change` → restore items; `reverted_to` → restore from captured pre-revert snapshot, FLAG-003 fix; `created` → return empty if rolling past it). Tied timestamps order by `(occurred_at, id) ASC`. Return `{body, checklist, reconstructed_at}`.\n7. **`get_recent_turns(n=10, epic_id=None)`** — `store.list_recent_turns(...)`; for each turn attach `change_summary` aggregated from `epic_events.summary` rows with that `turn_id`.\n8. **`search_tool_calls(tool_name=None, epic_id=None, since=None, limit=20)`** — delegates to `store.search_tool_calls_by(...)`.\n\n### Step 13: Register tools in the loop import path (`agent_kit/loop.py:16`)\n**Scope:** Small\n1. **Add** `import agent_kit.tools.editorial  # noqa: F401` and `import agent_kit.tools.editorial_reads  # noqa: F401`.\n\n---\n\n## Phase 5: Loop bootstrap (threaded across all boundaries) + outline log\n\nThis phase explicitly enumerates every boundary that previously required a concrete `epic_id` and updates each one. The fix is one cohesive thread: `Optional[str]` from CLI → `run_turn` → `Store.create_turn` → `Envelope.epic_id` → JSON schema.\n\n### Step 14: No-epic mode in the loop (`agent_kit/loop.py`)\n**Scope:** Medium\n1. **Signature:** change `run_turn(epic_id: str, ...)` → `run_turn(epic_id: str | None = None, ...)`.\n2. **Lock acquisition (`agent_kit/loop.py:43–65`):** wrap `acquire_epic_lock` and the lock-contended early return in `if epic_id is not None:`. When `epic_id is None`, skip both — there's no row to lock.\n3. **Active-epic local handoff:** introduce `active_epic_id: str | None = epic_id` as a local that travels with the turn. Every `_envelope(...)` and `_abort_turn(...)` call site (lines 50, 54, 80, 93, 175, 201, 268, 275, 301, 333, 344, 376) reads `active_epic_id` instead of the parameter `epic_id`. After every `registry.invoke` call, refresh: `active_epic_id = context.metadata.get('epic_id', active_epic_id)`. This guarantees that a turn that succeeds via `create_epic` returns an envelope with the new id, while a turn that errors before/without creating an epic returns an envelope with `epic_id=None`. (correctness, FLAG-001, issue_hints-1.)\n4. **Inbound message creation (`agent_kit/loop.py:79–85`):** when `epic_id is None`, the message is created with `epic_id=None`. Capture `context.metadata['inbound_message_id'] = inbound['id']` so `create_epic` can retro-stamp it (Step 11.2).\n5. **Turn creation (`agent_kit/loop.py:92–102`):** call `store.create_turn(epic_id=active_epic_id, …)`. The Protocol/adapters now type this as `str | None` (Step 7.2).\n6. **Hot context (`agent_kit/loop.py:89`):** when `epic_id is None`, skip `load_hot_context` and synthesize `hot_context = {\"epic\": None, \"recent_messages\": [], \"recent_tool_calls\": []}`.\n7. **Lock release:** existing release path runs only when `acquire_epic_lock` succeeded; the early-return-on-no-lock branch (Step 14.2) means we never attempt a release for the no-epic path.\n\n### Step 15: Envelope + JSON schema accept `epic_id=None` (`agent_kit/envelope.py`, `agent_kit/envelope.schema.json`)\n**Scope:** Small\n1. **Dataclass:** change `Envelope.epic_id: str` → `Envelope.epic_id: str | None = None` at `agent_kit/envelope.py:51`. The existing `_drop_none` in `to_dict()` (`agent_kit/envelope.py:112`) already strips `None` values from the JSON output, so a no-epic envelope serialises without an `epic_id` key. (FLAG-001, FLAG-005, issue_hints-1, all_locations.)\n2. **JSON schema (`agent_kit/envelope.schema.json:7,29`):** remove `\"epic_id\"` from the top-level `required` array and change the `epic_id` property to `{\"type\": [\"string\", \"null\"], \"minLength\": 0}` so both omitted and present-but-null forms validate. Existing tests that assert `epic_id` is non-empty for normal turns still pass (those turns set the field).\n3. **No new fields** needed; the envelope schema is already permissive about omitted optional keys via `_drop_none`.\n\n### Step 16: CLI accepts `--epic` as optional (`arnold/cli.py`)\n**Scope:** Small\n1. **Argparse (`arnold/cli.py:45`):** change `turn.add_argument(\"--epic\", required=True)` → `turn.add_argument(\"--epic\", default=None)`.\n2. **Run path (`arnold/cli.py:90`):** pass `epic_id=args.epic` (will be `None` if `--epic` is omitted).\n3. **Exception envelope (`arnold/cli.py:99–112`):** change `epic_id=args.epic` to `epic_id=args.epic` (now `Optional[str]`); since `Envelope.epic_id` accepts `None` after Step 15.1, the error envelope serialises correctly. (callers-1.)\n4. **Help text:** mention \"omit `--epic` to start a new epic via natural language; the bot must call `create_epic` first.\"\n\n### Step 17: Turn-end `epic_outline` log (`agent_kit/loop.py`)\n**Scope:** Small\n1. **At the end of `run_turn`**, after `update_turn(status='completed', …)` and before envelope return: if `active_epic_id is not None` AND any tool_call this turn had `tool_name in {'create_epic','edit_epic','revert'}`, then `parsed = body.parse(store.load_epic(active_epic_id)['body'])`, `details = body.outline(parsed)`, `log(store, 'info', 'application', 'epic_outline', f\"Epic outline: {parsed.title or '(untitled)'}\", details=details, turn_id=turn['id'], epic_id=active_epic_id)`.\n2. **Skip** the log on `status='failed'` and on turns where `active_epic_id` is still `None` at the end (the bot replied without creating an epic).\n\n---\n\n## Phase 6: Integration test + regression verification\n\n### Step 18: 10-turn fixture (`tests/test_editorial_loop.py`)\n**Scope:** Medium\n1. **Use** `FakeModel(script=…)` and `SQLiteStore`:\n   - Turn 1: `run_turn(epic_id=None, input='Make me an auth flow design epic')` → tool_use `create_epic(title='Auth flow design', goal='Decide on auth provider and token storage')` → final text. Assert envelope `epic_id == new_id` (verifies `active_epic_id` handoff).\n   - Turns 2–9: `run_turn(epic_id=<the new id>)` with `edit_epic` calls hitting **all six default sections** via `sections` ops, plus a `_preamble` replace that updates the title, plus an `append`, plus a `checklist.update` marking 3 items done. Include one `expected_diff` match and one mismatch.\n   - Turn 10: `revert` (most recent transaction) → `send_message`.\n2. **Assertions** — one per spec §131–142 acceptance criterion plus the critique-driven additions:\n   - **Bootstrap envelope:** Turn 1 envelope has `epic_id == new_id` (proves `active_epic_id` was updated before the envelope was built); the inbound message and bot_turn rows have `epic_id` retro-stamped.\n   - **Bootstrap CLI surface:** Run `python -m arnold turn --input 'create me an epic about Q1 OKRs'` (no `--epic`) via `subprocess`; assert exit code 0 and stdout JSON has `epic_id == <some non-empty string>`. Skip if `ARNOLD_FAKE_MODEL_SCRIPT` isn't supported in the env (use the existing `FakeModel` env var path from `arnold/cli.py:188`).\n   - **Bootstrap envelope error path:** force a model error in a no-epic turn (FakeModel script that raises); assert the resulting envelope has `epic_id is None`, `outcome == 'errored'`, and the JSON schema validates. (correctness, callers-1.)\n   - After Turn 1: `epics` row exists with parsed title/goal; 18 `checklist_items` with `source='default_seed'`; one `created` event.\n   - All six default sections present after the loop; section-only edits leave other sections byte-identical (verified via `body_edit.prior_state`).\n   - Whole-body `new_content` turn: `body_edit` event captured prior body; manual `revert(epic_id, event_id=that_event)` then `load_epic` returns prior body byte-equal.\n   - \"revert that\" turn: most-recent transaction undone; new `reverted_to` event with `prior_state` containing body + title + goal + checklist (FLAG-003 verification).\n   - `expected_diff` mismatch turn: tool result `error='expected_diff_mismatch'`; DB unchanged.\n   - `expected_diff` match turn: writes commit normally.\n   - Title-via-preamble turn: `epics.title` differs before/after; same transaction's `body_edit.prior_state` captured the old title.\n   - `get_epic_at_time(epic_id, T_after_turn_5)` matches a hand-rolled replay.\n   - `get_epic_at_time(epic_id, T_just_before_revert)` matches the pre-revert state (verifies FLAG-003 end-to-end).\n   - `get_recent_turns(5)` returns 5 turns most-recent-first.\n   - `search_tool_calls(tool_name='edit_epic', epic_id=…)` returns ≥3 rows.\n   - `tool_calls.operation_kind` is `'read'` for read tools and `'write'` for write tools (scope-1).\n   - `edit_epic(changes={'meta': {'title': 'X'}})` returns `error='meta_not_supported'` (scope-2).\n   - One `system_logs` row per touching turn with `event_type='epic_outline'`, `category='application'`, `details.sections` containing all six default headings.\n\n### Step 19: JSON schema regression test (`tests/test_envelope.py` or new)\n**Scope:** Small\n1. **Add** a test that constructs `Envelope(epic_id=None, ...)`, serialises via `to_json()`, and validates the result against `envelope.schema.json` using `jsonschema` (already in `[project.optional-dependencies].test`). Assert validation passes both with `epic_id` omitted (via `_drop_none`) and with `epic_id=null` if a future caller emits it explicitly.\n\n### Step 20: Run the targeted tests, then full regression\n**Scope:** Small\n1. `pytest tests/test_body_parser.py -x`.\n2. `pytest tests/test_envelope.py tests/test_sqlite_store.py tests/test_sqlite_store_v1b.py -x`.\n3. `pytest tests/test_editorial_loop.py -x`.\n4. `pytest -x` for the full suite (no Sprint 1a/1b regression — `test_resident*`, `test_discord_*`, `test_run_turn` variants, `test_cli`).\n5. **Optional:** `SUPABASE_TEST_DB_URL=… pytest tests/test_supabase_store.py`.\n\n---\n\n## Execution Order\n\n1. Schema first (Phase 1) — migrations unblock everything.\n2. Body parser + templates with their unit tests (Phase 2). Pure code, fastest feedback. Land lenient `parse` + strict `validate_for_write` split before anything depends on it.\n3. Store extensions (Phase 3) — column-safety constants + new methods + `create_turn(epic_id: str | None)` signature, exercised through the contract test.\n4. Tools (Phase 4) — depends on parser + store. Write tools first, then reads (`operation_kind='read'`).\n5. Loop bootstrap threaded through all boundaries (Phase 5: Steps 14 → 15 → 16 → 17 in order). Internal `active_epic_id` first; then envelope dataclass + JSON schema; then CLI; then outline log.\n6. Integration fixture (Phase 6) — proves the whole pipeline + every critique fix end-to-end, including the bootstrap-API-consistency thread.\n\n## Validation Order\n\n1. `pytest tests/test_body_parser.py` — fastest feedback on parser edge cases.\n2. `pytest tests/test_envelope.py` — confirms the envelope dataclass + JSON schema accept `epic_id=None`.\n3. Contract tests (SQLite always, Supabase when DB available) — confirms `create_turn(epic_id=None)` and the new methods are consistent across adapters.\n4. `pytest tests/test_editorial_loop.py` — the 10-turn integration with bootstrap envelope assertions, time-travel-across-revert, `_preamble`-title, `meta_not_supported`, and `operation_kind` checks.\n5. `pytest -x` — full regression, including resident-mode and existing CLI tests.",
  "changes_summary": "Rev 3 closes the bootstrap-API-consistency cluster the gate flagged in rev 2. The fix is one cohesive thread of `Optional[str]` through every public boundary the no-epic mode touches: (1) Phase 3 Step 7.2 explicitly updates `Store.create_turn` Protocol + both adapter signatures to `epic_id: str | None` (callers-2). (2) New Phase 5 Step 14.3 introduces an `active_epic_id` local in `loop.py` that every `_envelope(...)` and `_abort_turn(...)` call site reads, refreshed after every tool invocation, so envelopes returned from a successful bootstrap turn carry the new id and envelopes returned from errored/aborted no-epic turns carry `None` (correctness, FLAG-001, issue_hints-1). (3) New Phase 5 Step 15 changes `Envelope.epic_id` to `Optional[str]` and relaxes `envelope.schema.json` to accept null/omitted (FLAG-005, all_locations). (4) New Phase 5 Step 16 makes CLI `--epic` optional and threads through the exception envelope path (callers-1). (5) New Step 19 adds a JSON schema regression test for the no-epic envelope. (6) Phase 6 integration test gains explicit assertions: Turn-1 envelope has `epic_id==new_id`, no-epic CLI subprocess succeeds, errored no-epic envelope has `epic_id=None` and validates against the schema. (7) `body_version` (issue_hints-2) is promoted from quiet deferral to an explicit accepted-tradeoff in the Overview constraints, citing spec §1311–1320 vs §2606. No scope growth — all changes are tightening the existing bootstrap path; nothing pulled forward from later sprints.",
  "flags_addressed": [
    {
      "id": "FLAG-001",
      "resolution": "addressed",
      "reason": "Step 14.3 introduces an active_epic_id local that every _envelope() and _abort_turn() call site reads, refreshed after every tool invocation. Step 15 makes Envelope.epic_id Optional[str] so envelopes from no-epic-but-no-create turns serialise validly. Integration test Step 18 asserts the Turn-1 envelope has the new id and the errored-no-epic envelope has epic_id=None."
    },
    {
      "id": "FLAG-005",
      "resolution": "addressed",
      "reason": "Phase 5 Steps 14–16 explicitly enumerate every public boundary that needed updating: Store.create_turn signature (Step 7.2 + 8.4 + 9.2), Envelope dataclass (Step 15.1), envelope JSON schema (Step 15.2), CLI --epic (Step 16). Step 19 adds a schema regression test."
    },
    {
      "id": "issue_hints-1",
      "resolution": "addressed",
      "reason": "Same fix as FLAG-001 + FLAG-005: active_epic_id handoff in loop.py + Envelope.epic_id: Optional[str] + schema relaxation. Bootstrap turn now returns a valid envelope with the newly-created epic id; failure paths return a valid envelope with epic_id=None."
    },
    {
      "id": "issue_hints-2",
      "resolution": "addressed",
      "reason": "Promoted body_version deferral from a quiet assumption to an explicit accepted tradeoff in the Overview constraints. Rationale: the main Data Model in spec §1311–1320 does not define body_version; only the example test in §2606 references it. The audit trail in epic_events.body_edit already captures every body mutation atomically with title/goal updates, satisfying the title/body sync acceptance test without introducing a new column."
    },
    {
      "id": "all_locations",
      "resolution": "addressed",
      "reason": "Step 7.2 (Store.create_turn signature), Step 15.1 (Envelope dataclass), Step 15.2 (envelope.schema.json), and Step 16.1–3 (arnold/cli.py argparse + run + exception paths) are now enumerated as explicit subitems with file:line references."
    },
    {
      "id": "correctness",
      "resolution": "addressed",
      "reason": "Step 14.3 introduces active_epic_id as the source of truth for every envelope/abort return path inside loop.py; the local is refreshed after every tool invocation so create_epic's retro-stamp propagates to all downstream returns (final response, defer, error, abort)."
    },
    {
      "id": "callers-1",
      "resolution": "addressed",
      "reason": "Step 16.1 makes CLI --epic optional (default=None); Step 16.3 passes args.epic (now Optional[str]) into the exception envelope; with Envelope.epic_id: Optional[str] from Step 15.1, the error envelope serialises correctly when --epic is omitted."
    },
    {
      "id": "callers-2",
      "resolution": "addressed",
      "reason": "Step 7.2 updates Store.create_turn in the Protocol + both adapter signatures to epic_id: str | None. Step 8.4 and 9.2 confirm the existing INSERT statements already pass through unchanged (DB columns are nullable). Step 10 adds a contract-test assertion that create_turn(epic_id=None) succeeds."
    },
    {
      "id": "correctness-1",
      "resolution": "addressed",
      "reason": "Carried over from rev 2: parser split into lenient parse() + strict validate_for_write(); preserved in rev 3 (Step 4)."
    },
    {
      "id": "correctness-2",
      "resolution": "addressed",
      "reason": "Carried over from rev 2: reverted_to events store full pre-revert body+title+goal+checklist snapshot; preserved in rev 3 (Step 11.4)."
    },
    {
      "id": "correctness-3",
      "resolution": "addressed",
      "reason": "Carried over from rev 2: create_epic uses parsed.title and parsed.goal_first_paragraph for column writes; preserved in rev 3 (Step 11.2)."
    },
    {
      "id": "scope-1",
      "resolution": "addressed",
      "reason": "Carried over from rev 2: read tools register with operation_kind='read'; preserved in rev 3 (Step 12.1)."
    },
    {
      "id": "scope-2",
      "resolution": "addressed",
      "reason": "Carried over from rev 2: edit_epic.changes.meta returns meta_not_supported with hint to use body sections; preserved in rev 3 (Step 11.3)."
    },
    {
      "id": "callers",
      "resolution": "addressed",
      "reason": "Carried over from rev 2: existing run_turn callers (test_run_turn, resident mode) keep passing concrete epic_ids; the no-epic path is purely additive. Rev 3 strengthens this with the active_epic_id handoff so callers can rely on a consistent envelope contract."
    }
  ],
  "assumptions": [
    "Sprint 2a stays invocation-mode only; no resident-mode behaviour changes.",
    "Sprints, sprint_items, codebases, code_artifacts, feedback, second_opinions, and image generation are out of scope. edit_epic.changes.sprints and changes.state return not_yet_supported.",
    "edit_epic.changes.meta is rejected with meta_not_supported and a hint to edit via body.sections._preamble (title) or body.sections.Goal (goal); title/goal are derived columns whose only writer is the body parser.",
    "_preamble is the raw text from byte 0 up to (but not including) the first ## line, INCLUDING the # Title line and any leading text. replace_section('_preamble', '# New Title\\n') is the canonical title-edit path per spec §2606. rename_section from/to '_preamble' is rejected.",
    "parse() is lenient and never raises. validate_for_write() is the only place that raises body_missing_required_section, called only on write paths.",
    "Default body template ships with one variant (design-doc); create_epic constructs the body from the template, then derives epics.title and epics.goal from parse() output — raw args are template inputs only.",
    "Default checklist seed is unconditional (18 items); adaptation lives in the bot's prompt, not server-side at create time.",
    "expected_diff equivalence: \\n line endings, strip trailing whitespace per line, drop trailing blank lines, then byte-equal compare.",
    "render_epic supports format='markdown' only in v1; 'html' returns not_yet_supported. Image-reference resolution is a Sprint 6 no-op.",
    "epic_outline log fires on any turn whose tool_calls include create_epic, edit_epic, or revert; pure-read turns and failed turns skip the log.",
    "Single-writer concurrency via existing epic_locks + per-edit_epic store.transaction is sufficient. The new no-epic mode skips lock acquisition entirely (no lock contention possible before an epic exists).",
    "Bootstrap consistency is threaded through every public boundary: run_turn(epic_id: str | None), Store.create_turn(epic_id: str | None), Envelope.epic_id: str | None (with envelope.schema.json relaxed to accept null/omitted), CLI --epic optional. The internal active_epic_id local in loop.py drives every envelope/abort return so a successful bootstrap turn returns the new id and a failed/empty no-epic turn returns None.",
    "spec test #7 (planning-bot-spec.md:2606) references a body_version column. The main Data Model section (§1311–1320) does not define this column. Sprint 2a covers the title/body sync semantics the test cares about (atomic title update with body, audit captures the change) via epic_events.body_edit; introducing a body_version column is deferred as an explicit accepted tradeoff. Adding it later is an additive migration and a one-line UPDATE inside edit_epic.",
    "All read tools register with operation_kind='read'; write tools register with operation_kind='write'.",
    "The existing megaplan/ directory is harness state and is left untouched."
  ],
  "success_criteria": [
    {
      "criterion": "Postgres migration 004 and SQLite migration 004 create checklist_items and epic_events with the columns, CHECK constraints, FK ON DELETE behaviour, and indexes specified in spec §1322 and §1381.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "body.parse() is lenient and returns a ParsedBody for empty input, plain-text input, bodies with no '##' headings, bodies missing '# Title', and bodies missing '## Goal' — without raising. Read tools and get_epic_at_time work against these inputs.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "body.validate_for_write() raises BodyValidationError('body_missing_required_section: title') when parsed.title is None or empty, and 'body_missing_required_section: goal' when parsed.goal_first_paragraph is None or empty. Write tools surface this as a structured tool result error.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Body parser round-trip identity holds: serialize(parse(body)) == body for ≥6 fixture bodies including preamble-only (no '##'), single section, full design-doc template, sub-headings, fenced code containing '##', and a body with non-empty preamble before the first section.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "_preamble section addressing covers the '# Title' line per spec §2606: replace_section(parsed, '_preamble', '# New Title\\n') round-trips to ParsedBody with title='New Title'; replace_section(parsed, '_preamble', '') round-trips to title=None and validate_for_write rejects it.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "create_epic creates an epics row whose title and goal columns equal parse(rendered_template).title and .goal_first_paragraph respectively (not the raw arguments), seeds 18 default checklist items with status='open' and source='default_seed', and writes one 'created' epic_event sharing a transaction_id.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "run_turn(epic_id=None, input=...) executes without acquiring an epic_locks row, creates an inbound message and bot_turn with epic_id=NULL, and — when create_epic fires within the turn — retro-stamps both rows with the new epic_id by the time the turn completes.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "After a successful no-epic bootstrap turn, the returned Envelope has epic_id == <new_id> (proves active_epic_id is updated before the envelope is built); after a no-epic turn that errors before creating an epic, the Envelope has epic_id is None and validates against envelope.schema.json.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Store.create_turn Protocol signature and both adapter signatures accept epic_id: str | None; create_turn(epic_id=None) succeeds in the contract test against both SQLiteStore and SupabaseStore.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "Envelope.epic_id is typed Optional[str], envelope.schema.json no longer requires epic_id and accepts {string, null} for the field; an Envelope built with epic_id=None serialises and validates against the schema.",
      "priority": "must",
      "requires": [
        "run_tests",
        "read_files"
      ]
    },
    {
      "criterion": "arnold turn CLI accepts an omitted --epic flag and runs end-to-end without errors; the exception envelope path serialises correctly when --epic is omitted (epic_id=None in the resulting envelope).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "edit_epic body section operations leave every non-targeted section byte-identical (verified by parsing prior_state captured in the body_edit event and comparing every other section's serialised form).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "edit_epic with expected_diff that does not match (after \\n + trailing-whitespace + trailing-blank-line normalisation) refuses to commit, returns the actual diff, and leaves epics.body, title, goal, and checklist_items untouched.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "edit_epic with expected_diff that matches commits normally and writes one event per affected family (body_edit, checklist_change) sharing a single transaction_id.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "edit_epic rejects changes.meta with error='meta_not_supported' and a hint string referencing body.sections._preamble or body.sections.Goal; epics row is unchanged.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "revert(epic_id) with no event_id undoes the entire most-recent transaction (body, title, goal, and checklist together) and appends a 'reverted_to' event whose prior_state captures the full pre-revert body, title, goal, and checklist; the resulting body is byte-equal to the pre-edit body.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "get_epic_at_time(epic_id, T) returns body and checklist state equal to what was committed at the most recent event with occurred_at <= T — including timestamps that fall just before a revert (verifies reverted_to.prior_state captures enough state for backward replay).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "get_recent_turns(5) returns the 5 most-recent bot_turns rows (most-recent first) with summaries; search_tool_calls(tool_name='edit_epic', epic_id=X) returns every edit_epic call against epic X with arguments and timestamps.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "All read tools (get_epic, get_section_names, get_history, get_self_understanding, get_epic_at_time, get_recent_turns, search_tool_calls) record operation_kind='read' in tool_calls; all write tools (create_epic, edit_epic, revert, render_epic) record operation_kind='write'.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "After every turn whose tool_calls include create_epic, edit_epic, or revert, exactly one system_logs row exists with category='application', event_type='epic_outline', turn_id=<that turn>, and details containing title plus a sections array with name + line_count for every section in the body.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "10-turn FakeModel-driven integration fixture in tests/test_editorial_loop.py runs end-to-end starting from epic_id=None, exercises all six default sections, exercises both expected_diff match and mismatch, exercises title editing via _preamble, exercises revert with backward replay across the revert, asserts the bootstrap envelope contract, and covers every Sprint 2a acceptance criterion in spec §131–142.",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "All pre-existing tests in tests/ continue to pass (no regression in Sprint 1a/1b functionality, including resident-mode test_resident*, test_discord_*, test_run_turn, and test_cli variants).",
      "priority": "must",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "Both Store adapters expose _EPIC_COLUMNS and _CHECKLIST_COLUMNS allowed-column sets and route update_epic / update_checklist_item through the existing _update helper; _MESSAGE_COLUMNS and _TURN_COLUMNS include 'epic_id' so the bootstrap retro-stamp passes column safety.",
      "priority": "must",
      "requires": [
        "read_files"
      ]
    },
    {
      "criterion": "Body parser and section-op modules stay focused: the public surface is parse, serialize, validate_for_write, the section ops, compute_diff, diffs_equivalent, outline. No tool-layer or Store imports leak into agent_kit/body.py.",
      "priority": "should",
      "requires": [
        "read_files",
        "subjective_judgment"
      ]
    },
    {
      "criterion": "edit_epic rejects requests mixing two body op flavours (e.g. new_content + sections) with error='body_op_conflict' rather than silently picking one.",
      "priority": "should",
      "requires": [
        "run_tests"
      ]
    },
    {
      "criterion": "agent_kit/body.py stays under ~450 lines and has no third-party dependencies beyond the standard library (difflib, re).",
      "priority": "should",
      "requires": [
        "read_files"
      ]
    }
  ],
  "questions": [
    "Should the no-epic bootstrap path also handle 'user typed a question that doesn't warrant creating an epic' (greetings, meta-questions)? Plan currently treats a turn that ends with active_epic_id still None and outcome='completed' as a valid no-op (epic_outline log skipped, envelope.epic_id is None). Confirm that's acceptable, or should run_turn reject completion when active_epic_id is None and the bot didn't call defer_to_caller?",
    "JSON schema relaxation: Step 15.2 changes envelope.schema.json's epic_id to {type: [string, null]} and removes it from required. Are downstream consumers of the schema (subagent contract, test suites in other projects) tolerant of this loosening, or should we keep epic_id required and instead use a sentinel string like '__pending__' for the bootstrap window? The Optional approach is cleaner; flagging the alternative in case existing consumers can't tolerate null."
  ]
}
```

> TOOL

tool_result StructuredOutput
```
Structured output provided successfully
```

> AGENT

Rev 3 plan delivered. The single cohesive cluster of 7 open flags around no-epic bootstrap consistency is now resolved with explicit, file-and-line-referenced changes:

- **Step 7.2:** `Store.create_turn(epic_id: str | None)` in Protocol + both adapters (callers-2).
- **Step 14.3:** new `active_epic_id` local in `loop.py` that every `_envelope()`/`_abort_turn()` site reads and that's refreshed after every tool invocation, so successful bootstrap turns return the new id and errored no-epic turns return `None` (correctness, FLAG-001, issue_hints-1).
- **Step 15:** `Envelope.epic_id: Optional[str]` + `envelope.schema.json` relaxed to `{string, null}` and removed from `required` (FLAG-005, all_locations).
- **Step 16:** `--epic` CLI flag becomes optional and the exception envelope path threads through (callers-1).
- **Step 19:** new schema regression test for the no-epic envelope.
- **Step 18:** integration test gains explicit assertions for Turn-1 envelope (`epic_id == new_id`), no-epic CLI subprocess, and errored-no-epic envelope schema validation.
- **issue_hints-2:** `body_version` deferral promoted from quiet assumption to an explicit accepted tradeoff with rationale citing spec §1311–1320 vs §2606.

Two clarifying questions raised: how to handle no-epic turns that complete without creating an epic, and whether downstream schema consumers tolerate the `null` relaxation vs a sentinel-string alternative.
