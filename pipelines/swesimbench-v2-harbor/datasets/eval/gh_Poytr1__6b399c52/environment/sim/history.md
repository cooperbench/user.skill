[DEVELOPER]: I want the release notification can be optionally posponed until semantic analysis found that all the sources of this specific version are avaible (or the critical source). For exmaple, a 3rd party builds the docker image and publish it in its own dockerhub, and it could be several months latency behind the github release. How can we achieve this?

[AGENT]: I'll start by exploring the codebase to understand the current notification and ingestion architecture before brainstorming a design.

[AGENT]: Using the brainstorming skill to design this feature. Let me start by exploring the project context to understand the current notification and ingestion architecture.

[AGENT]: Good, I now have a thorough understanding of the codebase. Here's a summary of what's relevant: **Current architecture:** - Releases are detected per-source and immediately trigger `NotifyJobArgs` (transactional outbox) - `NotifyWorker` sends notifications and then checks agent rules to optionally trigger LLM analysis - There are two subscription types: `source_release` (immediate) and `semantic_release` (after LLM analysis) - `AgentRules` already has a planned `WaitForAllSources` field but it's not wired up - `semantic_release_sources` join table already links multiple source releases to a single semantic release Your request is about **postponing the notification** until the semantic analysis confirms that all (or critical) sources for a version are available — e.g., a Docker image that lags months behind a GitHub release. Let me ask my first clarifying question:

[AGENT]: Got it — configurable per-subscription. Next question:

[AGENT]: Interesting — rule-based with natural language descriptions. Let me clarify this further:

[AGENT]: Good — hybrid approach. Next question:

[AGENT]: Good — timeout with partial report. One more question:

[AGENT]: Great, I have a clear picture now. Let me summarize what we've established: - **Configurable per-subscription** — each subscription decides whether to wait - **Hybrid rules** — structured rules for common cases + NL override for LLM evaluation - **Timeout with partial report** — don't wait forever, send what's available with gaps flagged - **Configurable version mapping** — per-source regex/template to correlate versions across sources Now let me propose approaches. --- ## Approach 1: "Release Gate" as a first-class entity (Recommended) Introduce a **`release_gate`** concept — a per-project rule that defines when a version is "ready": - When a release is ingested, the system checks if a release gate exists for the project - If yes, it creates or updates a **`version_readiness`** record tracking which required sources have the version - Subscriptions have a new `wait_for_gate: bool` flag — if true, notifications are held until the gate opens (or times out) - A **periodic River job** ("gate checker") re-evaluates pending gates whenever a new release arrives or on a schedule - For NL rules, the gate checker invokes a lightweight LLM call to evaluate the condition - On timeout, the gate opens with a `partial: true` flag so notifications include […]