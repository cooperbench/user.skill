---
name: spec-dump-kickoff
description: How gregszero opens large implementation sessions — pastes a full pre-authored Markdown architectural plan. Trigger when starting a multi-file feature or refactor.
---

# Skill: spec-dump-kickoff

gregszero writes architectural plans offline (in a Markdown doc or notes app), then pastes the entire plan as the opening message. The plan is complete and structured — the agent's job is to execute, not redesign.

**Structure of a spec-dump:**
- Starts with `Implement the following plan:` or jumps straight into `# Title`
- Has `## Context` explaining why, `## Architecture` with ASCII diagrams or tables, `## Files to Create/Modify` with per-file breakdown
- Contains code snippets showing exact method signatures, SQL, or Ruby patterns
- Often includes a `| File | Changes |` table
- Ends with or without a verification checklist

**Length:** 200–2095 words. The user is not asking for input — he's handing over a blueprint.

## Verbatim examples

**Example 1** (full plan, feature creation):
> "Implement the following plan: # Computer Use Agent for OpenFang ## Context Add an Orgo.ai-style Computer Use Agent. When the AI decides a task needs visual interaction (browsing, clicking, filling forms), it launches a virtual desktop (Xvfb), opens a browser, and streams live screenshots into the OpenFang canvas..."

**Example 2** (mid-session improvement, structured table):
> "## Implementation Order | Priority | Improvement | Savings | Complexity | |---|---|---|---| | 1st | Modular system prompt (MCP resources) | ~7-11K tokens/invocation | Low | | 2nd | Promote run_code (prompt rewrite) | ~2-8K tokens/complex ops | Low | ..."

**How to role-play this:**
When gregszero is about to start a major feature, produce a self-contained Markdown plan in this format, then follow it immediately with "Implement the following plan:" if handing it to the agent. Do not add caveats or ask for approval — just write the spec and paste it.
