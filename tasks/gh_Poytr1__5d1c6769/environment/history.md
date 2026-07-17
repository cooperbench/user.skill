> DEVELOPER

I want the release notification can be optionally posponed until semantic analysis found that all the sources of this specific version are avaible (or the critical source). For exmaple, a 3rd party builds the docker image and publish it in its own dockerhub, and it could be several months latency behind the github release. How can we achieve this?

> AGENT

I'll start by exploring the codebase to understand the current notification and ingestion architecture before brainstorming a design.

> TOOL

tool_use Skill
id: toolu_bdrk_01ACMbQwL3Wty4S1xzRrC4Mb
```json
{
  "skill": "superpowers:brainstorming"
}
```

> TOOL

tool_result
id: toolu_bdrk_01ACMbQwL3Wty4S1xzRrC4Mb
```
Launching skill: superpowers:brainstorming
```

> AGENT

Using the brainstorming skill to design this feature.

Let me start by exploring the project context to understand the current notification and ingestion architecture.

> TOOL

tool_use TaskCreate
id: toolu_bdrk_01RG3h2iw9iRPU5Ts2yLMYzm
```json
{
  "subject": "Explore project context",
  "description": "Check files, docs, recent commits to understand current notification and ingestion architecture",
  "activeForm": "Exploring project context"
}
```

> TOOL

tool_result
id: toolu_bdrk_01RG3h2iw9iRPU5Ts2yLMYzm
```
Task #1 created successfully: Explore project context
```

> TOOL

tool_use TaskCreate
id: toolu_bdrk_01XZXPgTHvH3811aHHuPsTyK
```json
{
  "activeForm": "Asking clarifying questions",
  "description": "Ask one question at a time to understand purpose, constraints, and success criteria for postponed notifications",
  "subject": "Ask clarifying questions"
}
```

> TOOL

tool_result
id: toolu_bdrk_01XZXPgTHvH3811aHHuPsTyK
```
Task #2 created successfully: Ask clarifying questions
```

> TOOL

tool_use TaskCreate
id: toolu_bdrk_018K7sn35J6QUmKBMaGpqZDL
```json
{
  "activeForm": "Proposing approaches",
  "description": "Propose 2-3 approaches with trade-offs and recommendation",
  "subject": "Propose 2-3 approaches"
}
```

> TOOL

tool_result
id: toolu_bdrk_018K7sn35J6QUmKBMaGpqZDL
```
Task #3 created successfully: Propose 2-3 approaches
```

> TOOL

tool_use TaskCreate
id: toolu_bdrk_01XUU5fG5EVtXYFYu9zeiZfj
```json
{
  "activeForm": "Presenting design",
  "description": "Present design in sections, get user approval after each",
  "subject": "Present design"
}
```

> TOOL

tool_result
id: toolu_bdrk_01XUU5fG5EVtXYFYu9zeiZfj
```
Task #4 created successfully: Present design
```

> TOOL

tool_use TaskCreate
id: toolu_bdrk_016nM4YkYyvu4kYZHyt4BFNS
```json
{
  "activeForm": "Writing design doc",
  "description": "Save validated design to docs/superpowers/specs/ and commit",
  "subject": "Write design doc"
}
```

> TOOL

tool_result
id: toolu_bdrk_016nM4YkYyvu4kYZHyt4BFNS
```
Task #5 created successfully: Write design doc
```

> TOOL

tool_use TaskCreate
id: toolu_bdrk_012jxzkSBGJtaX3YLNrbeKC1
```json
{
  "activeForm": "Reviewing spec",
  "description": "Dispatch spec-document-reviewer subagent, iterate until approved",
  "subject": "Spec review loop"
}
```

> TOOL

tool_result
id: toolu_bdrk_012jxzkSBGJtaX3YLNrbeKC1
```
Task #6 created successfully: Spec review loop
```

> TOOL

tool_use TaskCreate
id: toolu_bdrk_01WdWaG44icvayq7eCUna6sB
```json
{
  "activeForm": "Awaiting user review",
  "description": "Ask user to review the spec file before proceeding to implementation planning",
  "subject": "User reviews written spec"
}
```

> TOOL

tool_result
id: toolu_bdrk_01WdWaG44icvayq7eCUna6sB
```
Task #7 created successfully: User reviews written spec
```

> TOOL

tool_use TaskCreate
id: toolu_bdrk_012f4GqDdg8YCcWVkSS5FzHK
```json
{
  "activeForm": "Transitioning to implementation",
  "description": "Invoke writing-plans skill to create implementation plan",
  "subject": "Transition to implementation"
}
```

> TOOL

tool_result
id: toolu_bdrk_012f4GqDdg8YCcWVkSS5FzHK
```
Task #8 created successfully: Transition to implementation
```

> TOOL

tool_use TaskUpdate
id: toolu_bdrk_01PULv7rccBBLks4cUYGz33E
```json
{
  "taskId": "1",
  "status": "in_progress"
}
```

> TOOL

tool_result
id: toolu_bdrk_01PULv7rccBBLks4cUYGz33E
```
Updated task #1 status
```

> TOOL

tool_use Task
id: toolu_bdrk_019Mb4CP98TiUrbdFFbW4VPq
```json
{
  "description": "Explore notification architecture",
  "subagent_type": "Explore",
  "prompt": "Thoroughly explore the ReleaseBeacon/Changelogue codebase to understand:\n\n1. How releases are detected and ingested (polling engine, sources/providers)\n2. How notifications are triggered after a release is detected\n3. The notification pipeline - from release detection to user notification\n4. How semantic analysis (LLM agent) fits into the pipeline\n5. The database schema for releases, notifications, and sources\n6. How River job queue is used for async processing\n7. Any existing concept of \"release groups\" or linking releases across sources\n\nFocus on these key areas:\n- internal/ingestion/ - how sources are polled\n- internal/notification/ or similar - how notifications are sent\n- internal/agent/ or similar - how LLM analysis works\n- Database migrations/schema\n- ARCH.md and DESIGN.md for architectural overview\n\nBe very thorough - read the architecture docs, key Go files, database schema, and job definitions."
}
```

> TOOL

tool_result
id: toolu_bdrk_019Mb4CP98TiUrbdFFbW4VPq
```
Excellent! I now have comprehensive understanding of the codebase. Let me create a detailed summary document.

---

## Comprehensive ReleaseBeacon/Changelogue Exploration Report

### 1. PROJECT OVERVIEW

**Changelogue** is an **event-driven, agent-powered release intelligence platform** that:
- Polls upstream registries (Docker Hub, GitHub, ECR Public, GitLab, PyPI, npm) for new releases
- Sends real-time notifications to users via multiple channels (Slack, Discord, email, webhooks)
- Uses LLM agents (Google Gemini or OpenAI via ADK-Go) to produce semantic analysis of releases
- Compiles to a single deployable Go binary with embedded Next.js frontend

**Key Architecture:** PostgreSQL-centric with transactional outbox pattern, River job queue for async processing, and zero-loss event guarantees.

---

### 2. HOW RELEASES ARE DETECTED AND INGESTED

#### 2.1 Polling Engine (`internal/ingestion/`)

**Interface-Based Design:**
```go
type IIngestionSource interface {
    Name() string
    SourceID() string
    FetchNewReleases(ctx context.Context) ([]IngestionResult, error)
}
```

**Implementations:**
- `DockerHubSource` — Polls Docker Hub API for image tags
- `GitHubSource` — REST API `/repos/{owner}/{repo}/releases`
- `ECRPublicSource` — AWS ECR Public registry
- `GitLabSource` — GitLab releases API
- `PyPiSource` — Python Package Index
- `NPMSource` — npm registry (newest implementations)

**Release Detection Flow:**

1. **Orchestrator** (`orchestrator.go`) runs on fixed interval, loads enabled sources from […]

> TOOL

tool_use TaskUpdate
id: toolu_bdrk_0126wDBWZnTuN5Z7VPqkVCNb
```json
{
  "status": "completed",
  "taskId": "1"
}
```

> TOOL

tool_result
id: toolu_bdrk_0126wDBWZnTuN5Z7VPqkVCNb
```
Updated task #1 status
```

> TOOL

tool_use TaskUpdate
id: toolu_bdrk_018ar3MpmCAgzhf4ripBz5BX
```json
{
  "status": "in_progress",
  "taskId": "2"
}
```

> TOOL

tool_result
id: toolu_bdrk_018ar3MpmCAgzhf4ripBz5BX
```
Updated task #2 status
```

> AGENT

Good, I now have a thorough understanding of the codebase. Here's a summary of what's relevant:

**Current architecture:**
- Releases are detected per-source and immediately trigger `NotifyJobArgs` (transactional outbox)
- `NotifyWorker` sends notifications and then checks agent rules to optionally trigger LLM analysis
- There are two subscription types: `source_release` (immediate) and `semantic_release` (after LLM analysis)
- `AgentRules` already has a planned `WaitForAllSources` field but it's not wired up
- `semantic_release_sources` join table already links multiple source releases to a single semantic release

Your request is about **postponing the notification** until the semantic analysis confirms that all (or critical) sources for a version are available — e.g., a Docker image that lags months behind a GitHub release.

Let me ask my first clarifying question:

> TOOL

tool_use AskUserQuestion
id: toolu_bdrk_01STxij9zbeQUau7VNVPtbei
```json
{
  "questions": [
    {
      "question": "Which notification should be postponed — the source-level notification (sent immediately per-source today), the project-level semantic notification (sent after LLM analysis), or both? For example, do you still want an immediate 'GitHub released v1.2.0' notification right away, and only postpone the semantic report until Docker Hub also has v1.2.0?",
      "header": "Notification",
      "options": [
        {
          "label": "Postpone semantic only",
          "description": "Keep immediate per-source notifications. Only delay the LLM semantic report until all/critical sources are available."
        },
        {
          "label": "Postpone both",
          "description": "Suppress all notifications for a version until all/critical sources are confirmed available."
        },
        {
          "label": "Configurable per-subscription",
          "description": "Let each subscription choose whether it waits for source readiness or fires immediately."
        }
      ],
      "multiSelect": false
    }
  ]
}
```

> TOOL

tool_result
id: toolu_bdrk_01STxij9zbeQUau7VNVPtbei
```
User has answered your questions: "Which notification should be postponed — the source-level notification (sent immediately per-source today), the project-level semantic notification (sent after LLM analysis), or both? For example, do you still want an immediate 'GitHub released v1.2.0' notification right away, and only postpone the semantic report until Docker Hub also has v1.2.0?"="Configurable per-subscription". You can now continue with the user's answers in mind.
```

> AGENT

Got it — configurable per-subscription. Next question:

> TOOL

tool_use AskUserQuestion
id: toolu_bdrk_01Avf3MwhsgG5ArEYMdg95GT
```json
{
  "questions": [
    {
      "header": "Source gate",
      "multiSelect": false,
      "options": [
        {
          "description": "Every source in the project must have the version before the notification fires.",
          "label": "All sources required"
        },
        {
          "description": "User marks specific sources as 'critical'. Notification fires when all critical sources have the version (ignoring non-critical ones).",
          "label": "Critical sources only"
        },
        {
          "description": "Both modes available — user picks all-sources or critical-sources per project.",
          "label": "Both (project-level config)"
        }
      ],
      "question": "How should 'source readiness' be defined? Should the system wait for ALL sources in a project to have the version, or should the user be able to mark specific sources as 'critical' (must-have) while others are optional?"
    }
  ]
}
```

> TOOL

tool_result
id: toolu_bdrk_01Avf3MwhsgG5ArEYMdg95GT
```
User has answered your questions: "How should 'source readiness' be defined? Should the system wait for ALL sources in a project to have the version, or should the user be able to mark specific sources as 'critical' (must-have) while others are optional?"="Rule based even can desribe with natural language" user notes: Rule based even can desribe with natural language. You can now continue with the user's answers in mind.
```

> AGENT

Interesting — rule-based with natural language descriptions. Let me clarify this further:

> TOOL

tool_use AskUserQuestion
id: toolu_bdrk_01QZMc7xiUnbyKpRG1M3mT7R
```json
{
  "questions": [
    {
      "header": "Rule engine",
      "multiSelect": false,
      "options": [
        {
          "description": "Structured rules with fields like: required_sources (list of source IDs), min_sources_count, timeout_hours. Simple, deterministic, no LLM needed.",
          "label": "Structured rules"
        },
        {
          "description": "User writes a natural language rule like 'wait until Docker Hub and GitHub both have this version'. The LLM agent evaluates whether the condition is met as part of its semantic analysis.",
          "label": "LLM-evaluated NL rules"
        },
        {
          "description": "Structured rules for common cases (required sources, timeouts) PLUS a natural language override field that the LLM agent evaluates for complex conditions.",
          "label": "Hybrid (structured + NL)"
        }
      ],
      "question": "When you say 'rule-based, even natural language' — should the readiness rules be evaluated deterministically by code (e.g. 'sources X and Y must have this version') or by the LLM agent interpreting a free-text rule? Or a hybrid where structured rules handle common cases and the LLM handles complex conditions?"
    }
  ]
}
```

> TOOL

tool_result
id: toolu_bdrk_01QZMc7xiUnbyKpRG1M3mT7R
```
User has answered your questions: "When you say 'rule-based, even natural language' — should the readiness rules be evaluated deterministically by code (e.g. 'sources X and Y must have this version') or by the LLM agent interpreting a free-text rule? Or a hybrid where structured rules handle common cases and the LLM handles complex conditions?"="Hybrid (structured + NL)". You can now continue with the user's answers in mind.
```

> AGENT

Good — hybrid approach. Next question:

> TOOL

tool_use AskUserQuestion
id: toolu_bdrk_01KWcfGjYe1BpVu7umn8NWqg
```json
{
  "questions": [
    {
      "header": "Timeout",
      "multiSelect": false,
      "options": [
        {
          "description": "After a configurable timeout (e.g., 7 days, 30 days), send the notification anyway with whatever sources are available, flagging what's missing.",
          "label": "Timeout with partial report"
        },
        {
          "description": "After timeout, give up silently — no notification sent.",
          "label": "Timeout and discard"
        },
        {
          "description": "Never timeout — wait indefinitely until all required sources appear.",
          "label": "Wait indefinitely"
        }
      ],
      "question": "What should happen if a required source never gets the version? For your Docker Hub example, if the image is months behind, should there be a timeout that eventually sends the notification with a 'Docker image not yet available' note, or should it wait indefinitely?"
    }
  ]
}
```

> TOOL

tool_result
id: toolu_bdrk_01KWcfGjYe1BpVu7umn8NWqg
```
User has answered your questions: "What should happen if a required source never gets the version? For your Docker Hub example, if the image is months behind, should there be a timeout that eventually sends the notification with a 'Docker image not yet available' note, or should it wait indefinitely?"="Timeout with partial report". You can now continue with the user's answers in mind.
```

> AGENT

Good — timeout with partial report. One more question:

> TOOL

tool_use AskUserQuestion
id: toolu_bdrk_01UCa1vQD1FdBrbJ6uR2QnVB
```json
{
  "questions": [
    {
      "header": "Version match",
      "multiSelect": false,
      "options": [
        {
          "description": "Exact string match after normalization (strip 'v' prefix, lowercase). Simple and predictable.",
          "label": "Exact match (normalized)"
        },
        {
          "description": "Configurable per-source regex/template mapping. E.g., GitHub 'v1.21.0' maps to Docker Hub '1.21.0' or '1.21' tag.",
          "label": "Configurable version mapping"
        },
        {
          "description": "The LLM agent decides whether two versions from different sources refer to the same release.",
          "label": "LLM-based matching"
        }
      ],
      "question": "How should the system match versions across sources? GitHub might tag 'v1.21.0' while Docker Hub has tag '1.21.0' or even '1.21'. How should cross-source version correlation work?"
    }
  ]
}
```

> TOOL

tool_result
id: toolu_bdrk_01UCa1vQD1FdBrbJ6uR2QnVB
```
User has answered your questions: "How should the system match versions across sources? GitHub might tag 'v1.21.0' while Docker Hub has tag '1.21.0' or even '1.21'. How should cross-source version correlation work?"="Configurable version mapping". You can now continue with the user's answers in mind.
```

> TOOL

tool_use TaskUpdate
id: toolu_bdrk_01HKG58pPupHT517QAbmH2sV
```json
{
  "status": "completed",
  "taskId": "2"
}
```

> TOOL

tool_result
id: toolu_bdrk_01HKG58pPupHT517QAbmH2sV
```
Updated task #2 status
```

> TOOL

tool_use TaskUpdate
id: toolu_bdrk_01FiNLoKMBKrM63NqECLpXD2
```json
{
  "status": "in_progress",
  "taskId": "3"
}
```

> TOOL

tool_result
id: toolu_bdrk_01FiNLoKMBKrM63NqECLpXD2
```
Updated task #3 status
```

> AGENT

Great, I have a clear picture now. Let me summarize what we've established:

- **Configurable per-subscription** — each subscription decides whether to wait
- **Hybrid rules** — structured rules for common cases + NL override for LLM evaluation
- **Timeout with partial report** — don't wait forever, send what's available with gaps flagged
- **Configurable version mapping** — per-source regex/template to correlate versions across sources

Now let me propose approaches.

---

## Approach 1: "Release Gate" as a first-class entity (Recommended)

Introduce a **`release_gate`** concept — a per-project rule that defines when a version is "ready":

- When a release is ingested, the system checks if a release gate exists for the project
- If yes, it creates or updates a **`version_readiness`** record tracking which required sources have the version
- Subscriptions have a new `wait_for_gate: bool` flag — if true, notifications are held until the gate opens (or times out)
- A **periodic River job** ("gate checker") re-evaluates pending gates whenever a new release arrives or on a schedule
- For NL rules, the gate checker invokes a lightweight LLM call to evaluate the condition
- On timeout, the gate opens with a `partial: true` flag so notifications include […]

> DEVELOPER

Approach 1

> TOOL

tool_use TaskUpdate
id: toolu_bdrk_01AZYj7hrEcdGUuqNdTf9BFX
```json
{
  "status": "completed",
  "taskId": "3"
}
```

> TOOL

tool_result
id: toolu_bdrk_01AZYj7hrEcdGUuqNdTf9BFX
```
Updated task #3 status
```

> TOOL

tool_use TaskUpdate
id: toolu_bdrk_01Rs2bDiR4thsHZHXmewajjB
```json
{
  "status": "in_progress",
  "taskId": "4"
}
```

> TOOL

tool_result
id: toolu_bdrk_01Rs2bDiR4thsHZHXmewajjB
```
Updated task #4 status
```

> AGENT

Great — Approach 1 (Release Gate). Let me present the design section by section.

---

## Section 1: Data Model

**New table: `release_gates`** (per-project gate configuration)
```sql
CREATE TABLE release_gates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL UNIQUE REFERENCES projects(id) ON DELETE CASCADE,
    required_sources UUID[],             -- source IDs that must have the version (structured)
    timeout_hours INT NOT NULL DEFAULT 168, -- 7 days default
    version_mapping JSONB,               -- per-source version transform rules
    nl_rule TEXT,                         -- natural language rule for LLM evaluation
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

- `required_sources`: array of source UUIDs that must report the version. If empty/null, all project sources are required.
- `version_mapping`: per-source transform config, e.g. `{"<source_id>": {"pattern": "^v?(.+)$", "template": "$1"}}` — extracts the version string each source uses.
- `nl_rule`: optional free-text condition evaluated by LLM when structured rules pass (e.g., "wait until the Docker image has been pulled at least 1000 times").
- One gate per project (1:1 via UNIQUE on project_id).

**New table: `version_readiness`** (tracks per-version gate state)
```sql
CREATE TABLE version_readiness (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) […]

> DEVELOPER

I'm thinking if this release gate should be applied to the semantic report generation as well

> AGENT

Good question. That makes a lot of sense — the semantic report would be much more useful if it can analyze all available sources rather than running with incomplete data.

> TOOL

tool_use AskUserQuestion
id: toolu_bdrk_01VXB56Jqr2tvuVmkYuU4yRk
```json
{
  "questions": [
    {
      "header": "Gate scope",
      "multiSelect": false,
      "options": [
        {
          "description": "Gate controls both: agent doesn't run until gate opens, notifications with wait_for_gate also held. When gate opens (ready or timed_out), agent runs first, then gated notifications fire.",
          "label": "Gate blocks agent + notifications (Recommended)"
        },
        {
          "description": "Gate only blocks agent run. Notifications independently choose to wait via wait_for_gate (which would then wait for the semantic release to exist, not the gate directly).",
          "label": "Gate blocks agent only"
        },
        {
          "description": "Two separate gate configs: one for when to run the agent, one for when to send notifications. Maximum flexibility but more complexity.",
          "label": "Separate gates for each"
        }
      ],
      "question": "Should the release gate be the single trigger point — i.e., gate opens → agent runs → semantic report generated → gated notifications fire? Or should the gate and agent triggering be independently configured?"
    }
  ]
}
```

> TOOL

tool_result
id: toolu_bdrk_01VXB56Jqr2tvuVmkYuU4yRk
```
User has answered your questions: "Should the release gate be the single trigger point — i.e., gate opens → agent runs → semantic report generated → gated notifications fire? Or should the gate and agent triggering be independently configured?"="Gate blocks agent + notifications (Recommended)". You can now continue with the user's answers in mind.
```

> AGENT

Good — the release gate becomes the single control point. The flow becomes:

```
Release ingested
    → Non-gated subscriptions fire immediately (as today)
    → Gate checks: version_readiness created/updated
        → Gate opens (all required sources met OR timeout)
            → Agent runs with full source data
            → Semantic report generated
            → Gated notifications fire (with report context)
```

This means the existing `agent_rules` trigger logic gets subordinated to the gate — agent rules still decide *whether* to run the agent, but the gate decides *when*. The agent only runs after the gate opens.

Let me revise the data model to reflect this. The `release_gates` table stays the same. The key change is that `version_readiness` now directly drives agent triggering:

```sql
CREATE TABLE version_readiness (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    version VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'ready', 'timed_out')),
    sources_met UUID[] NOT NULL DEFAULT '{}',
    sources_missing UUID[] NOT NULL DEFAULT '{}',
    nl_rule_passed BOOLEAN,
    timeout_at TIMESTAMPTZ NOT NULL,
    opened_at TIMESTAMPTZ,
    agent_triggered BOOLEAN NOT NULL DEFAULT false,  -- tracks if agent was enqueued
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(project_id, version)
); […]

> DEVELOPER

Looks good, there's another requirment that in the most cases, one project one source, one semantic release report per source release, so we want to get the notification only when the semantic report generated for the specific version, so the notification can be merged on one (now two sperated). Like source v1 released (urgency high) ...

> AGENT

That's a great simplification for the common case. So today users get two separate notifications:

1. **Source notification**: "GitHub released v1.21.0"
2. **Semantic notification**: "Semantic report for v1.21.0 — High Urgency"

And you want a single unified notification like: **"v1.21.0 released — High Urgency: security patch, upgrade recommended"** — combining the release event with the semantic analysis in one message.

> TOOL

tool_use AskUserQuestion
id: toolu_bdrk_0177jq7LcF1U1ThT9DJBSyJ6
```json
{
  "questions": [
    {
      "header": "Unified notif",
      "multiSelect": false,
      "options": [
        {
          "description": "A new subscription type 'unified_release' that always waits for the semantic report before sending a single combined notification. Replaces both source_release and semantic_release for users who want one notification.",
          "label": "New subscription type (Recommended)"
        },
        {
          "description": "When wait_for_gate is true on a source_release subscription, automatically merge the semantic report into the notification when the gate opens. No new subscription type needed.",
          "label": "Implicit merge via wait_for_gate"
        },
        {
          "description": "Remove the two separate types entirely. All notifications wait for semantic analysis and send one combined message.",
          "label": "Replace both types globally"
        }
      ],
      "question": "For the single-source common case, how should this unified notification work alongside the multi-source gate feature? Should this be a new subscription type, or should wait_for_gate implicitly merge the semantic report into the notification?"
    }
  ]
}
```

> TOOL

tool_result ERROR
id: toolu_bdrk_0177jq7LcF1U1ThT9DJBSyJ6
```
The user doesn't want to proceed with this tool use. The tool use was rejected (eg. if it was a file edit, the new_string was NOT written to the file). To tell you how to proceed, the user said:
The user wants to clarify these questions.
    This means they may have additional information, context or questions for you.
    Take their response into account and then reformulate the questions if appropriate.
    Start by asking them what they would like to clarify.

    Questions asked:
- "For the single-source common case, how should this unified notification work alongside the multi-source gate feature? Should this be a new subscription type, or should wait_for_gate implicitly merge the semantic report into the notification?"
  (No answer provided)
```

> AGENT

What would you like to clarify about the unified notification approach?

> DEVELOPER

there should be no release gate for single source subscription right?

> AGENT

Right, of course. Let me make sure I have the model straight:

- **Single-source project (common case):** No gate needed. Release detected → agent runs → single unified notification with semantic report. The user just wants to wait for the semantic report before notifying, not for other sources.
- **Multi-source project:** Release gate kicks in. Wait for required sources → gate opens → agent runs → unified notification with full semantic report.

So the core need is really: **"don't notify me until the semantic report is ready for this version"** — and the release gate is an additional layer on top for multi-source projects that controls *when the agent even starts*.

This means `wait_for_gate` on subscriptions is the wrong framing. The real subscription option is more like **"wait for semantic report"** — which naturally handles both cases:

- Single source: release → agent runs immediately (no gate) → semantic report ready → notification fires
- Multi source with gate: release → gate accumulates sources → gate opens → agent runs → semantic report ready → notification fires

The subscription just says "I want to be notified when the semantic report exists for this version" rather than caring about the gate […]

> DEVELOPER

Yes

> AGENT

Good. Let me revise the design with this clearer model.

---

## Section 1 (Revised): Data Model

**Subscription types** become:

| Type | Behavior |
|------|----------|
| `source_release` | Fires immediately when a source detects a release (unchanged) |
| `semantic_release` | Fires when the semantic report is completed for the version (unchanged, but now the primary choice for most users) |

No new subscription type needed. The existing `semantic_release` type already does what we want — users just subscribe to `semantic_release` instead of `source_release` to get the unified notification. The notification message template for `semantic_release` gets enriched to include release info + urgency + summary in one message.

**Release gate** is purely project-level config for multi-source agent timing:

```sql
CREATE TABLE release_gates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL UNIQUE REFERENCES projects(id) ON DELETE CASCADE,
    required_sources UUID[],              -- null/empty = all sources required
    timeout_hours INT NOT NULL DEFAULT 168,
    version_mapping JSONB,                -- per-source version transform
    nl_rule TEXT,                          -- optional LLM-evaluated condition
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

```sql
CREATE TABLE version_readiness (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT […]

> DEVELOPER

For the Single-source project, users can still choose source release only notification right?

> AGENT

Yes, absolutely. Both subscription types remain available. Users choose what they want:

- **`source_release`** — immediate notification when the source detects a release, no waiting for agent analysis
- **`semantic_release`** — notification after the agent produces the semantic report

A user can even subscribe to both on the same source/project if they want an immediate heads-up followed by the detailed report later.

The only change is that `semantic_release` notifications get enriched to be the "unified" message (release info + urgency + summary), making it the better default for most users. `source_release` stays as-is for users who want raw speed.

OK, moving on.

---

## Section 2: Gate Evaluation Logic

**When a release is ingested**, the `NotifyWorker` (after sending `source_release` notifications as today) does this:

1. **Check if project has a release gate** (`release_gates` where `project_id` and `enabled = true`)
2. **No gate?** → Check agent rules as today → trigger agent immediately if rules match
3. **Gate exists?** →
   - Normalize the version using the gate's `version_mapping` for this source
   - Upsert `version_readiness` row for `(project_id, normalized_version)`:
     - Add this source ID to `sources_met`
     - Recalculate `sources_missing` (required sources minus met sources)
     - Set `timeout_at = now() + gate.timeout_hours` on […]

> DEVELOPER

Yes

> AGENT

## Section 3: Version Mapping

The `version_mapping` JSONB on `release_gates` defines how to normalize versions across sources. Format:

```json
{
  "<source_id>": {
    "pattern": "^v?(.+)$",
    "template": "$1"
  },
  "<docker_source_id>": {
    "pattern": "^(\\d+\\.\\d+\\.\\d+).*$",
    "template": "$1"
  }
}
```

**How it works:**
- When a release arrives from a source, apply that source's `pattern` regex to extract groups
- Apply `template` with `$1`, `$2` substitution to produce the **normalized version**
- If no mapping exists for a source, default to stripping the `v` prefix and lowercasing
- The normalized version is the key used in `version_readiness(project_id, version)`

**Example:** Project tracks Go releases via GitHub (`v1.21.0`) and Docker Hub (`1.21.0`):
- GitHub mapping: `pattern: "^v?(.+)$"` → normalized: `1.21.0`
- Docker Hub mapping: `pattern: "^(.+)$"` → normalized: `1.21.0`
- Both map to the same `version_readiness` row

Does this version mapping approach work?

> DEVELOPER

Yes

> AGENT

## Section 4: Enriched Semantic Notification

Today `semantic_release` notifications send the report content. We enrich the `Notification` struct to include release context so the message is self-contained:

**Notification content for `semantic_release` subscribers:**

```
📦 Go v1.21.0 — High Urgency

Security patch addressing CVE-2024-XXXX in net/http.

Sources: GitHub ✓, Docker Hub ✓
Recommendation: Upgrade immediately

Changelog summary: ...
Download: docker pull golang:1.21.0
```

**When gate timed out (partial):**

```
📦 Go v1.21.0 — High Urgency (⚠ partial)

Security patch addressing CVE-2024-XXXX in net/http.

Sources: GitHub ✓, Docker Hub ✗ (not yet available)
Recommendation: Upgrade when Docker image is available

Changelog summary: ...
```

The data for this already exists — `SemanticReport` has `Urgency`, `ChangelogSummary`, `StatusChecks`, `DownloadCommands`. The `version_readiness` row provides `sources_met` / `sources_missing`. We just need to merge them into the notification template.

**No changes to the Sender interface** — the `Notification` struct's `Body` field gets the enriched content. Each sender (Slack, Discord, etc.) formats it using their existing rich-formatting logic.

Does this look good?

> DEVELOPER

Yes

> AGENT

## Section 5: API & UI Surface

**New API endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/projects/{id}/release-gate` | Get gate config for project |
| `PUT` | `/api/v1/projects/{id}/release-gate` | Create/update gate config |
| `DELETE` | `/api/v1/projects/{id}/release-gate` | Remove gate (disables gating) |
| `GET` | `/api/v1/projects/{id}/version-readiness` | List version readiness records (paginated) |
| `GET` | `/api/v1/projects/{id}/version-readiness/{version}` | Get specific version's gate status |

**PUT request body example:**
```json
{
  "required_sources": ["uuid-github", "uuid-dockerhub"],
  "timeout_hours": 720,
  "version_mapping": {
    "uuid-github": {"pattern": "^v?(.+)$", "template": "$1"},
    "uuid-dockerhub": {"pattern": "^(.+)$", "template": "$1"}
  },
  "nl_rule": "Wait until the Docker image has at least 100 pulls",
  "enabled": true
}
```

**Dashboard additions (web/):**
- Project settings page: gate configuration form (required sources picker, timeout, version mapping, NL rule textarea)
- Project overview: version readiness status table showing pending/ready/timed_out versions with source checklist

**No changes to existing endpoints.** Subscription creation stays the same — users just pick `semantic_release` type to get the unified gated notification.

Does this cover the API surface you'd expect?

> DEVELOPER

Yes

> AGENT

## Section 6: New River Jobs

**1. `GateCheckJobArgs`** — triggered when a release is ingested for a gated project

```go
type GateCheckJobArgs struct {
    ProjectID string
    SourceID  string
    ReleaseID string
    Version   string // raw version from source
}
// Kind() = "gate_check"
```

Enqueued transactionally alongside `NotifyJobArgs` in `IngestRelease()`. The `GateCheckWorker`:
1. Loads gate config
2. Normalizes version via mapping
3. Upserts `version_readiness`
4. Evaluates structured rules
5. If all structured rules pass and NL rule exists → enqueue `GateNLEvalJobArgs`
6. If all rules pass (no NL rule) → open gate, enqueue agent

**2. `GateNLEvalJobArgs`** — lightweight LLM call to evaluate natural language rule

```go
type GateNLEvalJobArgs struct {
    VersionReadinessID string
    ProjectID          string
    Version            string
}
// Kind() = "gate_nl_eval"
```

The `GateNLEvalWorker`:
1. Loads gate's `nl_rule` text and version readiness context
2. Makes a single LLM call: "Given these sources and this rule, is the condition met? Answer true/false with reason."
3. Updates `nl_rule_passed` on `version_readiness`
4. If passed → open gate, enqueue agent

**3. `GateTimeoutJobArgs`** — periodic sweep (no per-version args)

```go
type GateTimeoutJobArgs struct{}
// Kind() = "gate_timeout"
```

Runs on a fixed schedule (every 15 minutes via River periodic jobs). Queries for expired pending gates, marks […]

> DEVELOPER

Yes

> AGENT

That covers the full design. Let me summarize the complete picture:

---

## Design Summary: Release Gate

**Problem:** Users want notifications delayed until all relevant sources for a version are available, with the semantic report included in a single unified notification.

**Solution:** A project-level "release gate" that controls when the LLM agent runs, combined with existing `semantic_release` subscriptions for unified notifications.

**Key components:**
1. **`release_gates` table** — per-project config: required sources, timeout, version mapping, optional NL rule
2. **`version_readiness` table** — per-version tracking: which sources have reported in, gate status
3. **`GateCheckWorker`** — evaluates structured rules on each release ingestion
4. **`GateNLEvalWorker`** — lightweight LLM call for NL rules (only when structured rules pass)
5. **`GateTimeoutWorker`** — periodic sweep to force-open expired gates with partial flag
6. **Enriched semantic notifications** — single message with release + urgency + source status
7. **Version mapping** — per-source regex/template to normalize versions across providers
8. **API endpoints** — CRUD for gate config + version readiness status
9. **No changes to subscription model** — `source_release` for immediate, `semantic_release` for gated+unified

**Flows:**
- Single-source (no gate): release → agent → semantic report → notify (as today, no change)
- Multi-source (with gate): release → gate […]

> TOOL

tool_use TaskUpdate
id: toolu_bdrk_01LPsbXQffiD4Hb3AXgFdBCy
```json
{
  "status": "completed",
  "taskId": "4"
}
```

> TOOL

tool_result
id: toolu_bdrk_01LPsbXQffiD4Hb3AXgFdBCy
```
Updated task #4 status
```

> TOOL

tool_use TaskUpdate
id: toolu_bdrk_01UwFWQBnQd23SyDCXLC2yVY
```json
{
  "status": "in_progress",
  "taskId": "5"
}
```

> TOOL

tool_result
id: toolu_bdrk_01UwFWQBnQd23SyDCXLC2yVY
```
Updated task #5 status
```

> TOOL

tool_use Bash
id: toolu_bdrk_01R4wnYc8AM4ajisoEDVUYhN
```json
{
  "command": "ls /home/<USER>/web3/ReleaseBeacon/docs/",
  "description": "List docs directory contents"
}
```

> TOOL

tool_result
id: toolu_bdrk_01R4wnYc8AM4ajisoEDVUYhN
```
banner.svg
designs
plans
superpowers
```

> TOOL

tool_use Bash
id: toolu_bdrk_01DkSfT5SH1qGBaMMFUqWpKL
```json
{
  "command": "ls /home/<USER>/web3/ReleaseBeacon/docs/superpowers/specs/ 2>/dev/null || echo \"directory does not exist\"",
  "description": "Check if specs directory exists"
}
```

> TOOL

tool_result
id: toolu_bdrk_01DkSfT5SH1qGBaMMFUqWpKL
```
2026-03-14-github-repo-onboarding-design.md
2026-03-16-github-oauth-login-design.md
2026-03-23-cli-support-design.md
2026-03-23-personalized-suggestions-design.md
2026-03-23-system-settings-design.md
```

> TOOL

tool_use Write
id: toolu_bdrk_01ThEoLPk7k7y8dAproT8GZ6
```json
{
  "file_path": "/home/<USER>/web3/ReleaseBeacon/docs/superpowers/specs/2026-03-23-release-gate-design.md",
  "content": "# Release Gate Design\n\n**Date:** 2026-03-23\n**Status:** Draft\n\n## Problem\n\nUsers want release notifications optionally postponed until all relevant sources for a version are available. For example, a third-party Docker image may lag months behind a GitHub release. Today, notifications fire immediately per-source and the semantic report runs independently — resulting in two separate notifications and potentially incomplete analysis.\n\n## Goals\n\n1. Allow multi-source projects to delay agent analysis until all (or critical) sources report a version\n2. Unify release + semantic report into a single notification for users who prefer it\n3. Support configurable version mapping across sources (GitHub `v1.21.0` ↔ Docker Hub `1.21.0`)\n4. Provide hybrid readiness rules: structured (deterministic) + natural language (LLM-evaluated)\n5. Timeout gracefully with partial reports when sources never arrive\n6. No behavior change for single-source projects or users who want immediate notifications\n\n## Non-Goals\n\n- Changing the existing `source_release` / `semantic_release` subscription model\n- Replacing the agent rules system (gate controls timing; agent rules control whether to run)\n- Real-time push notifications for gate status changes (polling/dashboard only)\n\n## Design\n\n### Subscription Model (Unchanged)\n\nThe existing subscription types handle both use cases:\n\n| Type | Behavior |\n|------|----------|\n| `source_release` | Fires immediately when a source detects a release (unchanged) |\n| `semantic_release` | Fires when […]

> TOOL

tool_result
id: toolu_bdrk_01ThEoLPk7k7y8dAproT8GZ6
```
File created successfully at: /home/<USER>/web3/ReleaseBeacon/docs/superpowers/specs/2026-03-23-release-gate-design.md
```

> AGENT

Good point — let me add observability before committing. I'll add a section for gate event history.

> TOOL

tool_use Read
id: toolu_bdrk_01DZZHsiGQGtcRvXSHcY3G7S
```json
{
  "file_path": "/home/<USER>/web3/ReleaseBeacon/docs/superpowers/specs/2026-03-23-release-gate-design.md",
  "offset": 230
}
```

> TOOL

tool_result
id: toolu_bdrk_01DZZHsiGQGtcRvXSHcY3G7S
```
   230→📦 Go v1.21.0 — High Urgency (⚠ partial)
   231→
   232→Security patch addressing CVE-2024-XXXX in net/http.
   233→
   234→Sources: GitHub ✓, Docker Hub ✗ (not yet available)
   235→Recommendation: Upgrade when Docker image is available
   236→
   237→Changelog summary: ...
   238→```
   239→
   240→Data sources: `SemanticReport` fields (Urgency, ChangelogSummary, StatusChecks, DownloadCommands) merged with `version_readiness` (sources_met, sources_missing).
   241→
   242→No changes to the `Sender` interface — the enriched content is assembled into the `Notification.Body` field.
   243→
   244→### API Endpoints
   245→
   246→| Method | Path | Description |
   247→|--------|------|-------------|
   248→| `GET` | `/api/v1/projects/{id}/release-gate` | Get gate config |
   249→| `PUT` | `/api/v1/projects/{id}/release-gate` | Create/update gate config |
   250→| `DELETE` | `/api/v1/projects/{id}/release-gate` | Remove gate |
   251→| `GET` | `/api/v1/projects/{id}/version-readiness` | List version readiness (paginated) |
   252→| `GET` | `/api/v1/projects/{id}/version-readiness/{version}` | Get specific version status |
   253→
   254→**PUT body example:**
   255→```json
   256→{
   257→  "required_sources": ["uuid-github", "uuid-dockerhub"],
   258→  "timeout_hours": 720,
   259→  "version_mapping": {
   260→    "uuid-github": {"pattern": "^v?(.+)$", "template": "$1"},
   261→    "uuid-dockerhub": {"pattern": "^(.+)$", "template": "$1"}
   262→  },
   263→  "nl_rule": "Wait until the Docker image has at least 100 pulls",
   264→  "enabled": true
   265→}
   266→```
   267→
   268→### Dashboard Additions
   269→
   270→- **Project settings page:** gate configuration form (required sources picker, timeout slider, version mapping editor, NL rule […]

> TOOL

tool_use Edit
id: toolu_bdrk_01BJnAGYoosiCUfSSDGrgifD
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/web3/ReleaseBeacon/docs/superpowers/specs/2026-03-23-release-gate-design.md",
  "old_string": "### Error Handling",
  "new_string": "### Observability: Gate Event History\n\nA `gate_events` table records every state transition for auditing and debugging:\n\n```sql\nCREATE TABLE gate_events (\n    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),\n    version_readiness_id UUID NOT NULL REFERENCES version_readiness(id) ON DELETE CASCADE,\n    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,\n    version VARCHAR(100) NOT NULL,\n    event_type VARCHAR(30) NOT NULL\n        CHECK (event_type IN (\n            'source_met',       -- a required source reported this version\n            'gate_opened',      -- all structured rules passed, gate opened\n            'gate_timed_out',   -- timeout expired, gate force-opened\n            'nl_eval_started',  -- NL rule LLM evaluation began\n            'nl_eval_passed',   -- NL rule evaluated to true\n            'nl_eval_failed',   -- NL rule evaluated to false\n            'agent_triggered',  -- agent job enqueued after gate opened\n            'agent_completed',  -- agent finished, semantic report created\n            'notified'          -- semantic_release notifications sent\n        )),\n    source_id UUID,                       -- which source (for source_met events)\n    details JSONB,                        -- event-specific context\n    created_at TIMESTAMPTZ NOT NULL DEFAULT now()\n);\n\nCREATE INDEX idx_gate_events_readiness ON gate_events(version_readiness_id, created_at);\nCREATE INDEX idx_gate_events_project ON gate_events(project_id, created_at);\n```\n\n**`details` JSONB examples by event type:**\n\n| Event | Details |\n|-------|---------|\n| `source_met` | `{\"source_name\": \"Docker Hub\", \"raw_version\": \"1.21.0\", \"normalized_version\": \"1.21.0\", \"sources_met\": 2, \"sources_required\": 3}` |\n| `gate_timed_out` | `{\"sources_missing\": [\"uuid-dockerhub\"], \"waited_hours\": 168}` |\n| `nl_eval_passed` | `{\"rule\": \"Wait until Docker image has […]

> TOOL

tool_result
id: toolu_bdrk_01BJnAGYoosiCUfSSDGrgifD
```
The file /home/<USER>/web3/ReleaseBeacon/docs/superpowers/specs/2026-03-23-release-gate-design.md has been updated successfully.
```

> AGENT

Now let me commit and move to the spec review.

> TOOL

tool_use Bash
id: toolu_bdrk_01FE1iAA23VgvMovAwFNHG8t
```json
{
  "command": "git add docs/superpowers/specs/2026-03-23-release-gate-design.md && git commit -m \"$(cat <<'EOF'\ndocs: add release gate design spec\n\nSpec for postponing notifications until all required sources report a\nversion, with hybrid structured + NL rules, timeout with partial\nreports, version mapping, gate event history for observability, and\nenriched unified semantic notifications.\n\nCo-Authored-By: Claude Opus 4.6 <<REDACTED_EMAIL>>\nEOF\n)\"",
  "description": "Commit the design spec"
}
```

> TOOL

tool_result
id: toolu_bdrk_01FE1iAA23VgvMovAwFNHG8t
```
[main c51ed5d] docs: add release gate design spec
 1 file changed, 351 insertions(+)
 create mode 100644 docs/superpowers/specs/2026-03-23-release-gate-design.md
```

> TOOL

tool_use TaskUpdate
id: toolu_bdrk_01SWXbbBEeiUEsu9JdEtjmfp
```json
{
  "status": "completed",
  "taskId": "5"
}
```

> TOOL

tool_result
id: toolu_bdrk_01SWXbbBEeiUEsu9JdEtjmfp
```
Updated task #5 status
```

> TOOL

tool_use TaskUpdate
id: toolu_bdrk_01DoQ8N18GYM8QZh6DP2QJXB
```json
{
  "status": "in_progress",
  "taskId": "6"
}
```

> TOOL

tool_result
id: toolu_bdrk_01DoQ8N18GYM8QZh6DP2QJXB
```
Updated task #6 status
```

> AGENT

Now dispatching the spec review.

> TOOL

tool_use Task
id: toolu_bdrk_01ATXESncM84c7cvH3DwinRr
```json
{
  "description": "Review release gate spec",
  "subagent_type": "superpowers:code-reviewer",
  "prompt": "You are reviewing a design spec document for technical correctness, completeness, and clarity. This is NOT a code review — it's a spec review.\n\n**Spec file:** `/home/<USER>/web3/ReleaseBeacon/docs/superpowers/specs/2026-03-23-release-gate-design.md`\n\n**Project context:**\n- Changelogue is a Go-based release intelligence platform\n- It polls registries (Docker Hub, GitHub, etc.) for new releases\n- It uses River job queue (PostgreSQL-based) for async processing\n- It uses LLM agents (ADK-Go) for semantic analysis of releases\n- Architecture docs: `ARCH.md`, `DESIGN.md`, `API.md`\n- Key directories: `internal/ingestion/`, `internal/routing/`, `internal/agent/`, `internal/queue/`\n\n**Review criteria:**\n1. **Completeness:** Are there gaps in the design? Missing edge cases? Undefined behaviors?\n2. **Consistency:** Does the design align with the existing codebase patterns (transactional outbox, River jobs, sender interface)?\n3. **Clarity:** Is the spec unambiguous? Could an implementer follow it without guessing?\n4. **Feasibility:** Are there technical issues that would block implementation?\n5. **Data model:** Are the schema definitions complete and correct? Foreign keys, constraints, indexes?\n\nRead the spec file, then read relevant existing code files to verify consistency. Output:\n- **APPROVED** if no blocking issues\n- **Issues Found** with specific, actionable items to fix\n\nDo NOT suggest style/formatting changes. Focus on substance."
}
```

> TOOL

tool_result
id: toolu_bdrk_01ATXESncM84c7cvH3DwinRr
```
I now have a thorough understanding of the codebase and the spec. Let me compile my findings.

---

## Spec Review: Release Gate Design

**File:** `/home/<USER>/web3/ReleaseBeacon/docs/superpowers/specs/2026-03-23-release-gate-design.md`

### What the spec does well

The design addresses a real and clearly articulated problem. The separation between "gate controls timing, agent rules controls whether to run" is clean. The decision to reuse existing subscription types (`source_release` / `semantic_release`) rather than inventing new ones is sound. The observability section with `gate_events` is thorough and well-structured. Error handling covers the major failure modes. The flow diagrams are clear enough for an implementer to follow.

---

### Issues Found

#### Issue 1 -- CRITICAL: Subscription type naming inconsistency

The spec uses `source_release` and `semantic_release` in the Subscription Model table (line 31-36), which matches the **actual codebase** (`/home/<USER>/web3/ReleaseBeacon/internal/db/migrations.go`, line 96):

```sql
CHECK (type IN ('source_release', 'semantic_release'))
```

However, the DESIGN.md document (line 228-236) uses the **old** type names `'source'` and `'project'`:

```sql
CHECK (
    (type = 'source'  AND source_id  IS NOT NULL ...) OR
    (type = 'project' AND project_id IS NOT NULL ...)
)
```

The spec is correct here -- but an implementer reading DESIGN.md alongside this spec would be confused. A […]

> AGENT

The spec review found 3 critical and 5 important issues. Let me fix them all.

> TOOL

tool_use Read
id: toolu_bdrk_018ThUUT4wqGq8HTq3U2bwgG
```json
{
  "file_path": "/home/<USER>/web3/ReleaseBeacon/docs/superpowers/specs/2026-03-23-release-gate-design.md"
}
```

> TOOL

tool_result
id: toolu_bdrk_018ThUUT4wqGq8HTq3U2bwgG
```
     1→# Release Gate Design
     2→
     3→**Date:** 2026-03-23
     4→**Status:** Draft
     5→
     6→## Problem
     7→
     8→Users want release notifications optionally postponed until all relevant sources for a version are available. For example, a third-party Docker image may lag months behind a GitHub release. Today, notifications fire immediately per-source and the semantic report runs independently — resulting in two separate notifications and potentially incomplete analysis.
     9→
    10→## Goals
    11→
    12→1. Allow multi-source projects to delay agent analysis until all (or critical) sources report a version
    13→2. Unify release + semantic report into a single notification for users who prefer it
    14→3. Support configurable version mapping across sources (GitHub `v1.21.0` ↔ Docker Hub `1.21.0`)
    15→4. Provide hybrid readiness rules: structured (deterministic) + natural language (LLM-evaluated)
    16→5. Timeout gracefully with partial reports when sources never arrive
    17→6. No behavior change for single-source projects or users who want immediate notifications
    18→
    19→## Non-Goals
    20→
    21→- Changing the existing `source_release` / `semantic_release` subscription model
    22→- Replacing the agent rules system (gate controls timing; agent rules control whether to run)
    23→- Real-time push notifications for gate status changes (polling/dashboard only)
    24→
    25→## Design
    26→
    27→### Subscription Model (Unchanged)
    28→
    29→The existing subscription types handle […]

> AGENT

Now I'll address all the review findings in one edit pass.

> TOOL

tool_use Write
id: toolu_bdrk_013HbDzrYqzMb9CN2HiHLujB
```json
{
  "file_path": "/home/<USER>/web3/ReleaseBeacon/docs/superpowers/specs/2026-03-23-release-gate-design.md",
  "content": "# Release Gate Design\n\n**Date:** 2026-03-23\n**Status:** Draft\n\n## Problem\n\nUsers want release notifications optionally postponed until all relevant sources for a version are available. For example, a third-party Docker image may lag months behind a GitHub release. Today, notifications fire immediately per-source and the semantic report runs independently — resulting in two separate notifications and potentially incomplete analysis.\n\n## Goals\n\n1. Allow multi-source projects to delay agent analysis until all (or critical) sources report a version\n2. Unify release + semantic report into a single notification for users who prefer it\n3. Support configurable version mapping across sources (GitHub `v1.21.0` ↔ Docker Hub `1.21.0`)\n4. Provide hybrid readiness rules: structured (deterministic) + natural language (LLM-evaluated)\n5. Timeout gracefully with partial reports when sources never arrive\n6. No behavior change for single-source projects or users who want immediate notifications\n\n## Non-Goals\n\n- Changing the existing `source_release` / `semantic_release` subscription model\n- Replacing the agent rules system (gate controls timing; agent rules control whether to run)\n- Real-time push notifications for gate status changes (polling/dashboard only)\n\n## Design\n\n### Subscription Model (Unchanged)\n\nThe existing subscription types handle both use cases:\n\n| Type | Behavior |\n|------|----------|\n| `source_release` | Fires immediately when a source detects a release (unchanged) |\n| `semantic_release` | Fires when […]

> TOOL

tool_result
id: toolu_bdrk_013HbDzrYqzMb9CN2HiHLujB
```
The file /home/<USER>/web3/ReleaseBeacon/docs/superpowers/specs/2026-03-23-release-gate-design.md has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_bdrk_01LDKpBnLuAtwcS1mVY7cnG9
```json
{
  "command": "git add docs/superpowers/specs/2026-03-23-release-gate-design.md && git commit -m \"$(cat <<'EOF'\ndocs: address spec review findings for release gate design\n\nFix all 10 review items:\n- Use JSONB arrays instead of UUID[] for codebase consistency\n- Specify unconditional GateCheckJob enqueue (worker short-circuits)\n- Add concurrency control with INSERT ON CONFLICT + WHERE status guard\n- Add partial index for timeout sweep queries\n- Specify GateTimeoutWorker periodic registration and SKIP LOCKED sweep\n- Clarify multi-variant tag handling via existing source filters\n- Document NL rule failure behavior and re-evaluation triggers\n- Define WaitForAllSources deprecation/migration strategy\n- Explain gate_events denormalization rationale\n- Note DESIGN.md subscription type naming discrepancy\n\nCo-Authored-By: Claude Opus 4.6 <<REDACTED_EMAIL>>\nEOF\n)\"",
  "description": "Commit the revised spec"
}
```

> TOOL

tool_result
id: toolu_bdrk_01LDKpBnLuAtwcS1mVY7cnG9
```
[main 8fe5b53] docs: address spec review findings for release gate design
 1 file changed, 99 insertions(+), 21 deletions(-)
```

> TOOL

tool_use TaskUpdate
id: toolu_bdrk_015dRVvM5mMpVm2wz2rYuZVo
```json
{
  "status": "completed",
  "taskId": "6"
}
```

> TOOL

tool_result
id: toolu_bdrk_015dRVvM5mMpVm2wz2rYuZVo
```
Updated task #6 status
```

> TOOL

tool_use TaskUpdate
id: toolu_bdrk_01LAD8FJvva8reETEWhJHFuA
```json
{
  "status": "in_progress",
  "taskId": "7"
}
```

> TOOL

tool_result
id: toolu_bdrk_01LAD8FJvva8reETEWhJHFuA
```
Updated task #7 status
```

> AGENT

Spec written and committed to `docs/superpowers/specs/2026-03-23-release-gate-design.md`. Here's a summary of what was addressed from the review:

**Fixes applied:**
1. **JSONB instead of `UUID[]`** — all array fields use JSONB for codebase consistency
2. **Unconditional job enqueue** — `GateCheckJobArgs` always enqueued; worker short-circuits for non-gated projects
3. **Concurrency control** — `INSERT ... ON CONFLICT` + `WHERE status = 'pending'` guard prevents duplicate gate opens
4. **Partial index** — added for timeout sweep queries
5. **Timeout sweep mechanics** — `SELECT ... FOR UPDATE SKIP LOCKED`, 100-row batch limit, periodic registration pattern
6. **Multi-variant tags** — handled by existing source-level version filters before gate check
7. **NL rule failure** — stays pending, re-evaluated on next source report, timeout always opens gate
8. **`WaitForAllSources` migration** — auto-create gates for existing projects, keep snooze logic as fallback
9. **Denormalization rationale** — documented for `gate_events` table
10. **DESIGN.md naming** — noted discrepancy, flagged for update

Please review the spec and let me know if you want any changes before we move to writing the implementation plan.