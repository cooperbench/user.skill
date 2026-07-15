> DEVELOPER

I want the release notification can be optionally posponed until semantic analysis found that all the sources of this specific version are avaible (or the critical source). For exmaple, a 3rd party builds the docker image and publish it in its own dockerhub, and it could be several months latency behind the github release. How can we achieve this?

> AGENT

I'll start by exploring the codebase to understand the current notification and ingestion architecture before brainstorming a design.

> AGENT

Using the brainstorming skill to design this feature. Let me start by exploring the project context to understand the current notification and ingestion architecture.

> AGENT

Good, I now have a thorough understanding of the codebase. Here's a summary of what's relevant: **Current architecture:** - Releases are detected per-source and immediately trigger `NotifyJobArgs` (transactional outbox) - `NotifyWorker` sends notifications and then checks agent rules to optionally trigger LLM analysis - There are two subscription types: `source_release` (immediate) and `semantic_release` (after LLM analysis) - `AgentRules` already has a planned `WaitForAllSources` field but it's not wired up - `semantic_release_sources` join table already links multiple source releases to a single semantic release Your request is about **postponing the notification** until the semantic analysis confirms that all (or critical) sources for a version are available — e.g., a Docker image that lags months behind a GitHub release. Let me ask my first clarifying question:

> AGENT

Got it — configurable per-subscription. Next question:

> AGENT

Interesting — rule-based with natural language descriptions. Let me clarify this further:

> AGENT

Good — hybrid approach. Next question:

> AGENT

Good — timeout with partial report. One more question:

> AGENT

Great, I have a clear picture now. Let me summarize what we've established: - **Configurable per-subscription** — each subscription decides whether to wait - **Hybrid rules** — structured rules for common cases + NL override for LLM evaluation - **Timeout with partial report** — don't wait forever, send what's available with gaps flagged - **Configurable version mapping** — per-source regex/template to correlate versions across sources Now let me propose approaches. --- ## Approach 1: "Release Gate" as a first-class entity (Recommended) Introduce a **`release_gate`** concept — a per-project rule that defines when a version is "ready": - When a release is ingested, the system checks if a release gate exists for the project - If yes, it creates or updates a **`version_readiness`** record tracking which required sources have the version - Subscriptions have a new `wait_for_gate: bool` flag — if true, notifications are held until the gate opens (or times out) - A **periodic River job** ("gate checker") re-evaluates pending gates whenever a new release arrives or on a schedule - For NL rules, the gate checker invokes a lightweight LLM call to evaluate the condition - On timeout, the gate opens with a `partial: true` flag so notifications include […]

> DEVELOPER

Approach 1

> AGENT

Great — Approach 1 (Release Gate). Let me present the design section by section. --- ## Section 1: Data Model **New table: `release_gates`** (per-project gate configuration) ```sql CREATE TABLE release_gates ( id UUID PRIMARY KEY DEFAULT gen_random_uuid(), project_id UUID NOT NULL UNIQUE REFERENCES projects(id) ON DELETE CASCADE, required_sources UUID[], -- source IDs that must have the version (structured) timeout_hours INT NOT NULL DEFAULT 168, -- 7 days default version_mapping JSONB, -- per-source version transform rules nl_rule TEXT, -- natural language rule for LLM evaluation enabled BOOLEAN NOT NULL DEFAULT true, created_at TIMESTAMPTZ NOT NULL DEFAULT now(), updated_at TIMESTAMPTZ NOT NULL DEFAULT now() ); ``` - `required_sources`: array of source UUIDs that must report the version. If empty/null, all project sources are required. - `version_mapping`: per-source transform config, e.g. `{"<source_id>": {"pattern": "^v?(.+)$", "template": "$1"}}` — extracts the version string each source uses. - `nl_rule`: optional free-text condition evaluated by LLM when structured rules pass (e.g., "wait until the Docker image has been pulled at least 1000 times"). - One gate per project (1:1 via UNIQUE on project_id). **New table: `version_readiness`** (tracks per-version gate state) ```sql CREATE TABLE version_readiness ( id UUID PRIMARY KEY DEFAULT gen_random_uuid(), project_id UUID NOT NULL REFERENCES projects(id) […]

> DEVELOPER

I'm thinking if this release gate should be applied to the semantic report generation as well

> AGENT

Good question. That makes a lot of sense — the semantic report would be much more useful if it can analyze all available sources rather than running with incomplete data.

> AGENT

Good — the release gate becomes the single control point. The flow becomes: ``` Release ingested → Non-gated subscriptions fire immediately (as today) → Gate checks: version_readiness created/updated → Gate opens (all required sources met OR timeout) → Agent runs with full source data → Semantic report generated → Gated notifications fire (with report context) ``` This means the existing `agent_rules` trigger logic gets subordinated to the gate — agent rules still decide *whether* to run the agent, but the gate decides *when*. The agent only runs after the gate opens. Let me revise the data model to reflect this. The `release_gates` table stays the same. The key change is that `version_readiness` now directly drives agent triggering: ```sql CREATE TABLE version_readiness ( id UUID PRIMARY KEY DEFAULT gen_random_uuid(), project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE, version VARCHAR(100) NOT NULL, status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'ready', 'timed_out')), sources_met UUID[] NOT NULL DEFAULT '{}', sources_missing UUID[] NOT NULL DEFAULT '{}', nl_rule_passed BOOLEAN, timeout_at TIMESTAMPTZ NOT NULL, opened_at TIMESTAMPTZ, agent_triggered BOOLEAN NOT NULL DEFAULT false, -- tracks if agent was enqueued created_at TIMESTAMPTZ NOT NULL DEFAULT now(), updated_at TIMESTAMPTZ NOT NULL DEFAULT now(), UNIQUE(project_id, version) ); […]

> DEVELOPER

Looks good, there's another requirment that in the most cases, one project one source, one semantic release report per source release, so we want to get the notification only when the semantic report generated for the specific version, so the notification can be merged on one (now two sperated). Like source v1 released (urgency high) ...

> AGENT

That's a great simplification for the common case. So today users get two separate notifications: 1. **Source notification**: "GitHub released v1.21.0" 2. **Semantic notification**: "Semantic report for v1.21.0 — High Urgency" And you want a single unified notification like: **"v1.21.0 released — High Urgency: security patch, upgrade recommended"** — combining the release event with the semantic analysis in one message.

> AGENT

What would you like to clarify about the unified notification approach?

> DEVELOPER

there should be no release gate for single source subscription right?

> AGENT

Right, of course. Let me make sure I have the model straight: - **Single-source project (common case):** No gate needed. Release detected → agent runs → single unified notification with semantic report. The user just wants to wait for the semantic report before notifying, not for other sources. - **Multi-source project:** Release gate kicks in. Wait for required sources → gate opens → agent runs → unified notification with full semantic report. So the core need is really: **"don't notify me until the semantic report is ready for this version"** — and the release gate is an additional layer on top for multi-source projects that controls *when the agent even starts*. This means `wait_for_gate` on subscriptions is the wrong framing. The real subscription option is more like **"wait for semantic report"** — which naturally handles both cases: - Single source: release → agent runs immediately (no gate) → semantic report ready → notification fires - Multi source with gate: release → gate accumulates sources → gate opens → agent runs → semantic report ready → notification fires The subscription just says "I want to be notified when the semantic report exists for this version" rather than caring about the gate […]

> DEVELOPER

Yes

> AGENT

Good. Let me revise the design with this clearer model. --- ## Section 1 (Revised): Data Model **Subscription types** become: | Type | Behavior | |------|----------| | `source_release` | Fires immediately when a source detects a release (unchanged) | | `semantic_release` | Fires when the semantic report is completed for the version (unchanged, but now the primary choice for most users) | No new subscription type needed. The existing `semantic_release` type already does what we want — users just subscribe to `semantic_release` instead of `source_release` to get the unified notification. The notification message template for `semantic_release` gets enriched to include release info + urgency + summary in one message. **Release gate** is purely project-level config for multi-source agent timing: ```sql CREATE TABLE release_gates ( id UUID PRIMARY KEY DEFAULT gen_random_uuid(), project_id UUID NOT NULL UNIQUE REFERENCES projects(id) ON DELETE CASCADE, required_sources UUID[], -- null/empty = all sources required timeout_hours INT NOT NULL DEFAULT 168, version_mapping JSONB, -- per-source version transform nl_rule TEXT, -- optional LLM-evaluated condition enabled BOOLEAN NOT NULL DEFAULT true, created_at TIMESTAMPTZ NOT NULL DEFAULT now(), updated_at TIMESTAMPTZ NOT NULL DEFAULT now() ); ``` ```sql CREATE TABLE version_readiness ( id UUID PRIMARY KEY DEFAULT gen_random_uuid(), project_id UUID NOT […]

> DEVELOPER

For the Single-source project, users can still choose source release only notification right?

> AGENT

Yes, absolutely. Both subscription types remain available. Users choose what they want: - **`source_release`** — immediate notification when the source detects a release, no waiting for agent analysis - **`semantic_release`** — notification after the agent produces the semantic report A user can even subscribe to both on the same source/project if they want an immediate heads-up followed by the detailed report later. The only change is that `semantic_release` notifications get enriched to be the "unified" message (release info + urgency + summary), making it the better default for most users. `source_release` stays as-is for users who want raw speed. OK, moving on. --- ## Section 2: Gate Evaluation Logic **When a release is ingested**, the `NotifyWorker` (after sending `source_release` notifications as today) does this: 1. **Check if project has a release gate** (`release_gates` where `project_id` and `enabled = true`) 2. **No gate?** → Check agent rules as today → trigger agent immediately if rules match 3. **Gate exists?** → - Normalize the version using the gate's `version_mapping` for this source - Upsert `version_readiness` row for `(project_id, normalized_version)`: - Add this source ID to `sources_met` - Recalculate `sources_missing` (required sources minus met sources) - Set `timeout_at = now() + gate.timeout_hours` on […]

> DEVELOPER

Yes

> AGENT

## Section 3: Version Mapping The `version_mapping` JSONB on `release_gates` defines how to normalize versions across sources. Format: ```json { "<source_id>": { "pattern": "^v?(.+)$", "template": "$1" }, "<docker_source_id>": { "pattern": "^(\\d+\\.\\d+\\.\\d+).*$", "template": "$1" } } ``` **How it works:** - When a release arrives from a source, apply that source's `pattern` regex to extract groups - Apply `template` with `$1`, `$2` substitution to produce the **normalized version** - If no mapping exists for a source, default to stripping the `v` prefix and lowercasing - The normalized version is the key used in `version_readiness(project_id, version)` **Example:** Project tracks Go releases via GitHub (`v1.21.0`) and Docker Hub (`1.21.0`): - GitHub mapping: `pattern: "^v?(.+)$"` → normalized: `1.21.0` - Docker Hub mapping: `pattern: "^(.+)$"` → normalized: `1.21.0` - Both map to the same `version_readiness` row Does this version mapping approach work?

> DEVELOPER

Yes

> AGENT

## Section 4: Enriched Semantic Notification Today `semantic_release` notifications send the report content. We enrich the `Notification` struct to include release context so the message is self-contained: **Notification content for `semantic_release` subscribers:** ``` 📦 Go v1.21.0 — High Urgency Security patch addressing CVE-2024-XXXX in net/http. Sources: GitHub ✓, Docker Hub ✓ Recommendation: Upgrade immediately Changelog summary: ... Download: docker pull golang:1.21.0 ``` **When gate timed out (partial):** ``` 📦 Go v1.21.0 — High Urgency (⚠ partial) Security patch addressing CVE-2024-XXXX in net/http. Sources: GitHub ✓, Docker Hub ✗ (not yet available) Recommendation: Upgrade when Docker image is available Changelog summary: ... ``` The data for this already exists — `SemanticReport` has `Urgency`, `ChangelogSummary`, `StatusChecks`, `DownloadCommands`. The `version_readiness` row provides `sources_met` / `sources_missing`. We just need to merge them into the notification template. **No changes to the Sender interface** — the `Notification` struct's `Body` field gets the enriched content. Each sender (Slack, Discord, etc.) formats it using their existing rich-formatting logic. Does this look good?

> DEVELOPER

Yes

> AGENT

## Section 5: API & UI Surface **New API endpoints:** | Method | Path | Description | |--------|------|-------------| | `GET` | `/api/v1/projects/{id}/release-gate` | Get gate config for project | | `PUT` | `/api/v1/projects/{id}/release-gate` | Create/update gate config | | `DELETE` | `/api/v1/projects/{id}/release-gate` | Remove gate (disables gating) | | `GET` | `/api/v1/projects/{id}/version-readiness` | List version readiness records (paginated) | | `GET` | `/api/v1/projects/{id}/version-readiness/{version}` | Get specific version's gate status | **PUT request body example:** ```json { "required_sources": ["uuid-github", "uuid-dockerhub"], "timeout_hours": 720, "version_mapping": { "uuid-github": {"pattern": "^v?(.+)$", "template": "$1"}, "uuid-dockerhub": {"pattern": "^(.+)$", "template": "$1"} }, "nl_rule": "Wait until the Docker image has at least 100 pulls", "enabled": true } ``` **Dashboard additions (web/):** - Project settings page: gate configuration form (required sources picker, timeout, version mapping, NL rule textarea) - Project overview: version readiness status table showing pending/ready/timed_out versions with source checklist **No changes to existing endpoints.** Subscription creation stays the same — users just pick `semantic_release` type to get the unified gated notification. Does this cover the API surface you'd expect?

> DEVELOPER

Yes

> AGENT

## Section 6: New River Jobs **1. `GateCheckJobArgs`** — triggered when a release is ingested for a gated project ```go type GateCheckJobArgs struct { ProjectID string SourceID string ReleaseID string Version string // raw version from source } // Kind() = "gate_check" ``` Enqueued transactionally alongside `NotifyJobArgs` in `IngestRelease()`. The `GateCheckWorker`: 1. Loads gate config 2. Normalizes version via mapping 3. Upserts `version_readiness` 4. Evaluates structured rules 5. If all structured rules pass and NL rule exists → enqueue `GateNLEvalJobArgs` 6. If all rules pass (no NL rule) → open gate, enqueue agent **2. `GateNLEvalJobArgs`** — lightweight LLM call to evaluate natural language rule ```go type GateNLEvalJobArgs struct { VersionReadinessID string ProjectID string Version string } // Kind() = "gate_nl_eval" ``` The `GateNLEvalWorker`: 1. Loads gate's `nl_rule` text and version readiness context 2. Makes a single LLM call: "Given these sources and this rule, is the condition met? Answer true/false with reason." 3. Updates `nl_rule_passed` on `version_readiness` 4. If passed → open gate, enqueue agent **3. `GateTimeoutJobArgs`** — periodic sweep (no per-version args) ```go type GateTimeoutJobArgs struct{} // Kind() = "gate_timeout" ``` Runs on a fixed schedule (every 15 minutes via River periodic jobs). Queries for expired pending gates, marks […]

> DEVELOPER

Yes

> AGENT

That covers the full design. Let me summarize the complete picture: --- ## Design Summary: Release Gate **Problem:** Users want notifications delayed until all relevant sources for a version are available, with the semantic report included in a single unified notification. **Solution:** A project-level "release gate" that controls when the LLM agent runs, combined with existing `semantic_release` subscriptions for unified notifications. **Key components:** 1. **`release_gates` table** — per-project config: required sources, timeout, version mapping, optional NL rule 2. **`version_readiness` table** — per-version tracking: which sources have reported in, gate status 3. **`GateCheckWorker`** — evaluates structured rules on each release ingestion 4. **`GateNLEvalWorker`** — lightweight LLM call for NL rules (only when structured rules pass) 5. **`GateTimeoutWorker`** — periodic sweep to force-open expired gates with partial flag 6. **Enriched semantic notifications** — single message with release + urgency + source status 7. **Version mapping** — per-source regex/template to normalize versions across providers 8. **API endpoints** — CRUD for gate config + version readiness status 9. **No changes to subscription model** — `source_release` for immediate, `semantic_release` for gated+unified **Flows:** - Single-source (no gate): release → agent → semantic report → notify (as today, no change) - Multi-source (with gate): release → gate […]

> AGENT

Good point — let me add observability before committing. I'll add a section for gate event history.

> AGENT

Now let me commit and move to the spec review.

> AGENT

Now dispatching the spec review.

> AGENT

The spec review found 3 critical and 5 important issues. Let me fix them all.

> AGENT

Now I'll address all the review findings in one edit pass.

> AGENT

Spec written and committed to `docs/superpowers/specs/2026-03-23-release-gate-design.md`. Here's a summary of what was addressed from the review: **Fixes applied:** 1. **JSONB instead of `UUID[]`** — all array fields use JSONB for codebase consistency 2. **Unconditional job enqueue** — `GateCheckJobArgs` always enqueued; worker short-circuits for non-gated projects 3. **Concurrency control** — `INSERT ... ON CONFLICT` + `WHERE status = 'pending'` guard prevents duplicate gate opens 4. **Partial index** — added for timeout sweep queries 5. **Timeout sweep mechanics** — `SELECT ... FOR UPDATE SKIP LOCKED`, 100-row batch limit, periodic registration pattern 6. **Multi-variant tags** — handled by existing source-level version filters before gate check 7. **NL rule failure** — stays pending, re-evaluated on next source report, timeout always opens gate 8. **`WaitForAllSources` migration** — auto-create gates for existing projects, keep snooze logic as fallback 9. **Denormalization rationale** — documented for `gate_events` table 10. **DESIGN.md naming** — noted discrepancy, flagged for update Please review the spec and let me know if you want any changes before we move to writing the implementation plan.