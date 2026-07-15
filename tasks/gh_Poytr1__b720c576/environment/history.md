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