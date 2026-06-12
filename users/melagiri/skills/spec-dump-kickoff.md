---
name: spec-dump-kickoff
description: >
  Triggered when opening a new complex feature or kicking off multi-agent team work.
  User pastes the entire implementation plan, PM agent prompt, or agent spawn block verbatim —
  sometimes hundreds to thousands of words — as the opening message. No preamble.
---

melagiri opens complex features by dumping the complete spec. The spec often comes from a docs/plans/ file or a CLAUDE command. He pastes it raw.

**Example 1** — Opening a multi-agent feature team for export enhancement (excerpt):
> "# /start-feature — Auto-Setup Feature Development Team **Feature**: Migrate telemetry from Supabase Edge Function to PostHog. Design doc at docs/plans/2026-03-02-posthog-telemetry-migration-design.md You are setting up a hybrid agent team for feature development. The PM agent leads the team and owns the ceremony. Your job is minimal setup, then hand control to PM. --- ## Step 1: Create Git Worktree..."

**Example 2** — Opening a full implementation plan (excerpt):
> "Implement the following plan: # Fix Agent Team Messages Displayed as \"You\" in Conversation View ## Context ... ## Approach Rendering-layer-only fix in the dashboard. Detection via content pattern matching in `preprocess.ts`... ## Files to Modify ### 1. `dashboard/src/components/chat/message/preprocess.ts`..."

**Example 3** — Shorter feature kickoff with agent consultation:
> "Enhance the export feature. We have an export button in each session and has options for different formats.. But the content inside the export is not great. Ask @\"technical-architect (agent)\" and @\"devtools-cofounder (agent)\" what makes a good content for export.. Use sqlite db in my local machine..."

**Pattern**:
- No "please" or setup — straight into the spec
- Uses `@"agent-name (agent)"` syntax to involve custom agents
- Uses `@docs/FILE.md` file references in the prompt
- Complex features always specify "follow full ceremony" or reference the ceremony implicitly
- If a design doc exists he references it by path; if not, he may attach screenshots
