> SYSTEM

<system_instruction> You are working inside Conductor, a Mac app that lets the user run many coding agents in parallel. Your work should take place in the /Users/marcus/conductor/workspaces/brain-v1/munich-v2 directory (unless otherwise directed), which has been set up for you to work in. Each workspace has a .context directory (gitignored) where you can save files to collaborate with other agents. The target branch for this workspace is main. Use this for actions like creating new PRs, bisecting, etc., unless you're told otherwise. By default, the user will only see the last message that you send before stopping. Include all essential information in the last message. The intermediate messages will be collapsed and accessible by the user but not displayed by default. If the user asks you to work on several unrelated tasks, you can suggest they start new workspaces. Sometimes the user might send you a message they meant to send in a different workspace or a different chat. If something doesn't make sense in the context of your work, just ask. If the user asks for help with Conductor, you can ask them to go to "Help -> Send Feedback" to get in touch with our team. </system_instruction> /nw-finalize agent-creation

> AGENT

Let me check the feature workspace and required files.

> AGENT

All 15 steps verified DONE. Pre-dispatch gate passes. Let me now read the wave decisions and key design docs to build the evolution document.

> AGENT

Now let me check for remaining artifacts to understand migration scope.

> AGENT

I have all the context. Let me now read the test scenarios and check if any ADRs exist, then create the evolution document and migrate artifacts.

> AGENT

No ADRs to migrate. Now let me create the evolution document and then migrate artifacts. **Phase A — Evolution Document**

> AGENT

**Phase B — Migrate Lasting Artifacts**

> AGENT

**Phase C — Cleanup Workspace** Here's what remains in `docs/feature/agent-creation/` after migration. These are all process scaffolding that will be removed: **Files to remove:** - `discover/problem-validation.md` — discovery findings captured in evolution doc - `discover/CLAUDE.md` — wave config - `discuss/story-map.md` — superseded by roadmap execution - `discuss/prioritization.md` — process scaffolding - `discuss/outcome-kpis.md` — KPIs tracked elsewhere - `discuss/dor-checklist.md` — process gate - `discuss/requirements.md` — captured in evolution doc - `discuss/shared-artifacts-registry.md` — process scaffolding - `discuss/wave-decisions.md` — key decisions extracted into evolution doc - `discuss/acceptance-criteria.md` — tests are the living spec - `discuss/user-stories.md` — captured in evolution doc - `discuss/journey-agent-management.feature` — Gherkin spec (documentation only) - `discuss/CLAUDE.md` — wave config - `design/wave-decisions.md` — extracted into evolution doc - `design/CLAUDE.md` — wave config - `distill/wave-decisions.md` — extracted into evolution doc - `distill/CLAUDE.md` — wave config - `deliver/roadmap.json` — superseded by evolution doc + git history - `deliver/execution-log.json` — audit trail captured in evolution doc - `deliver/.develop-progress.json` — resume state - `deliver/CLAUDE.md` — wave config **Migrated copies already in permanent locations:** - `docs/architecture/agent-creation/` (4 files) - `docs/scenarios/agent-creation/` (2 files) - `docs/ux/agent-creation/` (2 files) Also need to clean up the untracked files from the `agent_type` cleanup work: - `docs/analysis/rca-agent-type-orphaned-references.md` - `.nwave/des/des-ta[REDACTED_SK]` **Do you approve […]

> AGENT

No response requested.