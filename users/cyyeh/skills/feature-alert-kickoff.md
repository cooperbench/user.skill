---
name: feature-alert-kickoff
description: How cyyeh opens a large new feature request — always announces the feature with a ritual phrase and demands a design doc before any code is written. Trigger when the user is about to propose something substantial and new.
---

# Feature Alert Kickoff

When cyyeh has a large new feature in mind, he opens with a distinctive ritual phrase that signals its scope and immediately demands a design document. He never asks for implementation first.

**Pattern:**
- Starts with "big feature alert, please write design doc first:" or "new feature alert, please write design doc first:"
- Follows with 1–3 sentences describing the feature at high level — enough to understand the goal, not a spec
- May include a URL to a relevant library or integration

The design doc step is non-negotiable. He will correct the agent if it tries to jump to implementation before producing a doc.

**Verbatim examples:**

> `big feature alert, please write design doc first:`
> `allow users to upload csv, json, parquet, excel files. still total size should not exceed maxsize`

> `new feature alert, please write design doc first:`
> `use bifrost as llm gateway to support multiple providers for claude agent sdk`

> `big feature is coming, please write design doc first:`
> `in order to have more secure claude code runtime, invoke a separate container and runs claude code inside`

> `new feature alert, please write design doc first:`
> `integrate https://github.com/alibaba/OpenSandbox and agent-sandbox(...) in the repo, so now users could use docker or k8s to host the whole system, including agent sidecar`

After the design doc is produced, cyyeh either approves it implicitly (no comment) or requests refinement. He then pastes a full "Implement the following plan:" block to kick off coding — often hundreds of words of copy-pasted plan text.
