> DEVELOPER

Implement the following plan: # Plan: Add Commit Steps to Agent Integration Skill ## Context The agent-integration skill runs three phases (research, write-tests, implement) but never commits code. All changes pile up uncommitted, making it harder to review, revert, or understand progress. Adding commits at each phase boundary and after each E2E tier creates clean, reviewable checkpoints. ## Changes ### 1. `.claude/skills/agent-integration/SKILL.md` Add commit instructions after each phase section: - After **Phase 1** output: commit AGENT.md + test script - After **Phase 2** output: commit E2E runner - After **Phase 3** output: no additional commit needed (implementer already commits at each milestone) Use `/commit` skill for the commits (follows project conventions). ### 2. `.claude/skills/agent-integration/researcher.md` Add a new section **"Phase 6: Commit"** at the end of the procedure, after Phase 5 (Implementation One-Pager). Stage and commit `cmd/entire/cli/agent/$AGENT_PACKAGE/AGENT.md` and `scripts/test-$AGENT_SLUG-agent-integration.sh`. ### 3. `.claude/skills/agent-integration/test-writer.md` Add a **"Step 7: Commit"** section after Step 6 (Verify). Stage and commit the E2E runner file `e2e/agents/$AGENT_SLUG.go` and any `e2e/testutil/repo.go` changes from Step 5. ### 4. `.claude/skills/agent-integration/implementer.md` Add a commit instruction block after each milestone step. The pattern is: after `mise run fmt && mise run lint` passes, stage and commit all modified agent files. Specific commit points: | After Step | Commit message pattern | What's staged | |---|---|---| | Step 3 (stubs compile) | `$AGENT_NAME: scaffold agent package` | `cmd/entire/cli/agent/$AGENT_PACKAGE/`, `cmd/entire/cli/hooks_cmd.go`, `cmd/entire/cli/agent/registry.go` | | Step 4 (Tier 1 passes) | `$AGENT_NAME: implement hook installation and basic event parsing` | `cmd/entire/cli/agent/$AGENT_PACKAGE/` | | Step 5 (Tier 2 passes) | `$AGENT_NAME: implement full lifecycle and transcript support` | `cmd/entire/cli/agent/$AGENT_PACKAGE/` | | Step 6 (Tier 2b passes) | `$AGENT_NAME: fix transcript metadata validation` | `cmd/entire/cli/agent/$AGENT_PACKAGE/` | | Step 7 (Tier 3 passes) | `$AGENT_NAME: support agent commit-in-turn` | `cmd/entire/cli/agent/$AGENT_PACKAGE/` | | Step 8 (Tier 4 passes) | `$AGENT_NAME: support …

> AGENT

`★ Insight ─────────────────────────────────────` This plan adds commit checkpoints to a multi-phase skill workflow. The key design choice is using `/commit` (the project's commit skill) rather than raw `git commit` commands — this ensures commit messages follow project conventions and hooks run properly. Staging specific files rather than `git add -A` prevents accidentally committing unrelated changes. `─────────────────────────────────────────────────` Let me start by reading the four files that need modification.

> AGENT

Now I have all four files. Let me implement the changes across all four files. `★ Insight ─────────────────────────────────────` The skill files use a phase/step numbering system. Adding commits as explicit steps (rather than inline notes) makes them first-class operations that won't be skipped. Using `/commit` skill ensures project conventions are followed — the skill handles message formatting, hooks, and signing automatically. `─────────────────────────────────────────────────` Let me make all four edits in parallel since they're independent:

> DEVELOPER

can be more generic. just say commit all files

> AGENT

Got it — I'll keep the commit instructions simple and generic. Let me fix the first edit that already landed and continue with the rest.

> AGENT

Now let me apply the remaining three SKILL.md and the other file edits:

> AGENT

Now the researcher.md and test-writer.md edits:

> AGENT

Now the implementer.md — I need to add commit blocks after each step's `mise run fmt && mise run lint`. Let me add them all:

> AGENT

Now I need to add commit blocks after Step 14 (unit tests) and Step 16 (final validation) in the implementer:

> AGENT

All edits are done. Let me verify the changes by quickly grepping for the commit instructions across all four files:

> AGENT

All commit instructions are in place across all four files. Here's the summary: | File | Commit points added | |---|---| | `SKILL.md` | 2 — after Phase 1 (research) and Phase 2 (write-tests) | | `researcher.md` | 1 — Phase 6: Commit (after the one-pager) | | `test-writer.md` | 1 — Step 7: Commit (after verification) | | `implementer.md` | 12 — after Steps 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16 | Every commit block uses the same pattern: `**Commit:** Use `/commit` to commit all files. Skip if no files changed.` — keeping it generic and consistent. The `/commit` skill handles message formatting and project conventions automatically. `★ Insight ─────────────────────────────────────` - Using `/commit` (a skill) rather than raw git commands delegates commit message conventions and hook execution to the skill — the instructions stay simple while the behavior stays consistent. - The "Skip if no files changed" guard prevents empty commits when a step requires no new code (common in later E2E tiers that exercise the strategy layer rather than agent-specific code). `─────────────────────────────────────────────────`
