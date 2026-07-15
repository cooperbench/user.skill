[SYSTEM]: <system_instruction> You are working inside Conductor, a Mac app that lets the user run many coding agents in parallel. Your work should take place in the /Users/marcus/conductor/workspaces/brain-v1/los-angeles directory (unless otherwise directed), which has been set up for you to work in. Each workspace has a .context directory (gitignored) where you can save files to collaborate with other agents. The target branch for this workspace is main. Use this for actions like creating new PRs, bisecting, etc., unless you're told otherwise. By default, the user will only see the last message that you send before stopping. Include all essential information in the last message. The intermediate messages will be collapsed and accessible by the user but not displayed by default. If the user asks you to work on several unrelated tasks, you can suggest they start new workspaces. Sometimes the user might send you a message they meant to send in a different workspace or a different chat. If something doesn't make sense in the context of your work, just ask. If the user asks for help with Conductor, you can ask them to go to "Help -> Send Feedback" to get in touch with our team. </system_instruction> /nw-finalize

[AGENT]: Let me check the pre-dispatch gate first — verifying all steps are complete.

[AGENT]: Let me check the final COMMIT events to verify all steps are done.

[AGENT]: All 21 steps have COMMIT events with PASS status. Pre-dispatch gate passed. Now let me gather the remaining artifacts needed for finalization.

[AGENT]: Now let me read the key artifacts needed for the evolution document.

[AGENT]: Good, I have all the context. Let me now read the ADRs and check existing permanent directories.

[AGENT]: Good. All permanent directories exist. Let me also read the UX journey files to migrate.

[AGENT]: Now I have everything needed. Let me check existing docs directories and create the evolution document + migrate artifacts.

[AGENT]: Good. I can see the ADR naming continues from ADR-010. The skills ADRs should be numbered starting from the next available. Let me check the highest existing ADR number.

[AGENT]: ADRs go up to 083. Skills ADRs will be 084, 085, 086. Now let me proceed with all phases. **Phase A**: Create evolution document **Phase B**: Migrate lasting artifacts

[AGENT]: Now Phase B — migrate lasting artifacts. Let me create the destination directories and copy files.

[AGENT]: Now let me update the architecture doc status from "FUTURE DESIGN" references and verify all migrated files exist.

[AGENT]: All 9 artifacts migrated successfully. Now **Phase C** — show the cleanup list for your approval. Here are the files that will be **removed** with `docs/feature/skills/`: **Process scaffolding (no lasting value):** - `deliver/execution-log.json` — audit trail captured in evolution doc - `deliver/roadmap.json` — superseded by evolution doc + git history - `deliver/.develop-progress.json` — resume state - `deliver/CLAUDE.md` — wave-local instructions - `design/review-proof.md` — review findings - `design/wave-decisions.md` — extracted into evolution doc - `design/CLAUDE.md` — wave-local instructions - `discover/wave-decisions.md` — extracted into evolution doc - `discover/lean-canvas.md` — discovery scaffolding - `discover/opportunity-tree.md` — discovery scaffolding - `discover/problem-validation.md` — discovery scaffolding - `discover/solution-testing.md` — discovery scaffolding - `discover/CLAUDE.md` — wave-local instructions - `discuss/wave-decisions.md` — extracted into evolution doc - `discuss/dor-validation.md` — process gate - `discuss/shared-artifacts-registry.md` — process scaffolding - `discuss/prioritization.md` — superseded by roadmap execution - `discuss/outcome-kpis.md` — captured in evolution doc context - `discuss/story-map.md` — process artifact - `discuss/user-stories.md` — requirements captured in tests - `discuss/journey-agent-creation.feature` — Gherkin (YAML+visual migrated) - `discuss/journey-skill-library.feature` — Gherkin (YAML+visual migrated) - `discuss/CLAUDE.md` — wave-local instructions - `distill/wave-decisions.md` — extracted into evolution doc **Already migrated (copies in permanent locations):** - `design/architecture.md` → `docs/architecture/skills/` - `design/adr-001-*.md` → `docs/adrs/ADR-084-*` - `design/adr-002-*.md` → `docs/adrs/ADR-085-*` - `design/adr-003-*.md` → `docs/adrs/ADR-086-*` - […]