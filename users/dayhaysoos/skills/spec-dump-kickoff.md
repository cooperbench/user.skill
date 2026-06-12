---
name: spec-dump-kickoff
description: How dayhaysoos opens large new feature implementations — a long pre-structured spec block with non-negotiables, already-decided defaults, and explicit "your mission" framing. Triggers when starting a new phase or handing off a significant feature.
---

When starting a new implementation phase or large feature, dayhaysoos writes a dense spec block that frontloads all decisions so the agent doesn't ask. The structure is:

1. "You are taking over…" framing with project/branch context
2. "Non-negotiable goals:" numbered list
3. "Implementation defaults (already decided):" with file paths, URLs, schema fields, env var names
4. "Your mission:" numbered steps with explicit part ordering ("implement in part order: 1, 2, 3, 4")

He does NOT ask the agent what approach to take — choices are already made.

**Example 1** (Minimal Report UI V1):
> "You are taking over Nimbus "Minimal Report UI V1" implementation. Context: - Product direction: keep GitHub/CI-native workflow, but add a lightweight visual report viewer. - We do NOT want a full dashboard yet. [...] Non-negotiable goals: 1) Render a review by reviewId from existing worker API. 2) Make it easy to copy report content into coding agents. [...] Implementation defaults (already decided): - URL route: /reports/:reviewId - Data source: existing API GET /api/reviews/:id - V1 has no auth/SSO complexity (public-by-reviewId is acceptable for now)"

**Example 2** (CLI phase):
> "### Phase 5 — CLI: nimbus repo register command\n\nNew top-level command following the exact same pattern as existing commands:\n- Reads NIMBUS_WORKER_URL via getWorkerUrl()\n- Reads NIMBUS_API_KEY via process.env and injects as X-Nimbus-Api-Key\n[...]\nBehavior:\n- Auto-detect repo slug from git remote origin if not explicitly provided"

**Example 3** (OpenRouter direct call):
> "The endpoint contract mismatch means we should not route the intent summarization pre-pass through AGENT_ENDPOINT. Instead, call OpenRouter directly from the worker for this specific call. Implement the full plan from the previous prompt with this change to Part 2: [...] Endpoint: https://openrouter.ai/api/v1/chat/completions - Model: anthropic/claude-haiku-4-5 [...] Implement in part order: 1, 2, 3, 4. After all four parts are done..."
