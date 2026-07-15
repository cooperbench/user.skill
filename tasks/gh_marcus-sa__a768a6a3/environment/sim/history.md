> SYSTEM

<system_instruction> You are working inside Conductor, a Mac app that lets the user run many coding agents in parallel. Your work should take place in the /Users/marcus/conductor/workspaces/brain-v1/los-angeles directory (unless otherwise directed), which has been set up for you to work in. Each workspace has a .context directory (gitignored) where you can save files to collaborate with other agents. The target branch for this workspace is main. Use this for actions like creating new PRs, bisecting, etc., unless you're told otherwise. By default, the user will only see the last message that you send before stopping. Include all essential information in the last message. The intermediate messages will be collapsed and accessible by the user but not displayed by default. If the user asks you to work on several unrelated tasks, you can suggest they start new workspaces. Sometimes the user might send you a message they meant to send in a different workspace or a different chat. If something doesn't make sense in the context of your work, just ask. If the user asks for help with Conductor, you can ask them to go to "Help -> Send Feedback" to get in touch with our team. </system_instruction> /nw-discover gh issue […]

> AGENT

Let me gather context on the GitHub issue and the existing agent creation flow before starting discovery.

> AGENT

Let me also check the existing research documents referenced in the issue.

> AGENT

I have full context on: - **Issue #177**: Detailed Skills spec with schema, activation model, governance, import path - **Research doc**: `skills-sandbox-agent-integration.md` — resolved decisions on hybrid strategy, source references, no file storage - **Current agent creation UI**: 2-step wizard (runtime selection → form with name/description/model/authority scopes) - **User's ask**: Expand to 3-step wizard (agent config → skills setup → tools setup) Let me launch the product discovery agent to validate the feature scope and UX decisions.

> AGENT

Discovery complete. Let me read the key artifacts to give you a summary.

> AGENT

Now let me also write the wave-decisions summary to complete the DISCOVER wave.

> AGENT

## DISCOVER Wave Complete — Skills Feature (#177) All 4 gates passed. Here's the summary: ### 3-Step Agent Creation Wizard | Step | What | Key UX | |------|------|--------| | **1. Agent Config** | Runtime (radio group), name, description, model, authority scopes, sandbox config | Consolidates current 2 steps into 1 | | **2. Skills Setup** | Checklist of active workspace skills to assign (`possesses` edges) | Skippable, shows name + description + source icon | | **3. Tools Setup** | Skill-derived tools (read-only, "via skill X") + manual tool selection (`can_use`) | Skippable, shows effective toolset union | ### Top Risks | Risk | Mitigation | |------|-----------| | **H3: Implicit tool grants confusing** (primary usability risk) | "via skill X" labels on derived tools in Step 3 | | **H1: 3-step flow feels heavy** | Steps 2+3 are skippable; external agents pass through quickly | | **H4: External agents annoyed by extra steps** | Skip buttons + note that skills apply to sandbox agents only | ### MVP Scope 1. Skill CRUD API (draft/active/deprecated lifecycle) 2. Schema migration (skill table + 5 relation tables) 3. 3-step wizard frontend 4. `possesses` edges created in agent creation transaction 5. `setSkillsConfig` adapter […]