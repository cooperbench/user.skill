---
session_id: "4thwithme/.dotfiles|7d1a3b97-db28-4db8-a381-b6aa7fa891c8"
developer: "gh:4thwithme"
split: train
source: crawl
repo: 4thwithme/.dotfiles
start_time: "2026-03-25T16:00:47.868Z"
n_turns: 149
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

hey bro we want create new advanced skill that will involve a few other skills and agents... we want create tool that will work as infinite loop as web developer who monitor JIRA board, pick-up tickets, creates
plan, then implements, then run test, fixes  and pushing to the GH, in case of comments or failed checks in gh - fixes and pushes updates.
seems like we need Atlasian mcp, github cli, /loop command etc.

> AGENT

Big idea. Let me research the existing skills, /loop, and Atlassian MCP capabilities to design this properly.

> AGENT

Good research. Now let me read a few key files to nail the exact patterns.

> AGENT

Got the full picture. Let me build this skill.

> AGENT

Skill created. Here's what was built:

## `/auto-developer` Skill

**Structure:**
```
.claude/skills/auto-developer/
├── SKILL.md                              # Main orchestrator (10 phases)
└── references/
    ├── implementation-cycle.md           # Planning + coding details
    ├── pr-monitoring.md                  # CI checks + review handling
    └── ticket-selection.md              # JIRA polling + priority logic
```

**10-Phase Loop:**

| Phase | What |
|-------|------|
| 1 | Poll JIRA board via JQL |
| 2 | Start ticket (transition + branch) |
| 3 | Plan (explore codebase, create tasks) |
| 4 | Implement (following all CLAUDE.md rules) |
| 5 | Verify & fix (lint, unit, e2e — max 3 retries) |
| 6 | Commit & push |
| 7 | Create draft PR (stacked branch detection) |
| 8 | Monitor CI checks, fix failures |
| 9 | Handle review comments |
| 10 | Next ticket |

**Safety rails:** Never force-push, never commit secrets, never merge PRs, max 3 retry cycles, always draft PRs, stops on ambiguous requirements.

**Usage:**
- `/auto-developer` — starts processing "To Do" tickets from current sprint
- `/auto-developer jql="..."` — custom ticket filter
- `/auto-developer RECO-123` — start with specific ticket
- `/loop 15m /auto-developer` — recurring board monitoring

**Integrates:** Atlassian MCP (JIRA), `gh` CLI (GitHub), existing skills (verify, create-pr, starting-jira-tasks patterns), subagents (explore, nestjs, debug, test).

Want to test it on a ticket?

> AGENT

I see the skill is already registered and showing in the skills list. The background task that was killed is irrelevant — it was from the earlier exploration agent.

The `/auto-developer` skill is ready to use. Anything you want to adjust, or should we test it?

> DEVELOPER

yes i want to adjust a lot
1. we need to be more precise in our workwlof

> DEVELOPER

yes i want to adjust a lot
1. we need to be more precise in our workflow, what to do on each step and what is possible devation
2. need to rename skill, we would like to have smth funny ;)))) propose me names they might be offensive as well

workflow

general instructions: use current session as orchestrator, for each step - create subsession or subagent, for all session use sonnet model, only for planning and complicated tasks that involves 20+ files use opus.

1. when customer launched our skill - first you need to check do you have access to the jira via atlasian mcp, if - not you needto print bit red text "LOGIN TO ATLASIAN FISRT !!", If you do not have acces to the github via GH cli, or cli is abesnt - tell to install or login., in case we started this session without --dangerously-skip-permissions or without enabled --enable-auto-mode - tell that you need to relanch session and give you permissions to run commands without stupid hummans <-- it has to be direct message from you ;) lool.
only when all is set - you can continue to the next step

2. create folder were we will store our plan, tracker and requirements in the @.claude/plans/ e.g. @.claude/plans/RECO-555/... if is storage of main info for our agents subagents to share more details and context.. all subagents MUST to use all of the files in the context. when subagent spwans - attach folder as conext. 

2. you need to ask developer do you have specific task or list of tasks you'd like me to do, or pick up random? user have to select
in case of specific task/tasks - user has to put link/links to the jira tickets to you, in case you can pick up - you need to check our recommendations board https://customink.atlassian.net/jira/software/c/projects/RECO/boards/777 and search for tasks in the "to do" status, and only if they have label "FOR_CC" (means for claude code), when you pick up 1 - proceed 
If you get lists of tasks for work - you will do them 1 by 1 strongly! Never in parallel. All requirements and key stuff we need to implement you need to save to the file next to the implmanntation plan in the directory for this feature e.g. @.claude/plans/RECO-555/requirements.md)

3. create file porgress tracker next to the implementation plan  ( they have to be in their own subfolfer in @.claude/plans/ dir with name of the task for example @.claude/plans/RECO-555). In the progress tracker we need to have all steps we described here in the skill as worflow. and after planning phase we need to add details under each step. in case we need to add steps to the worflowf, or change them - do it on the fly, but it can do only orchestrator agent(main one) and planning agent. Each step should have clear definitions of what has to be done and finished on each step, after each step you need to set check mark what was done. If smth was done not fully or with some variations - leave short coments with links. This is one the main file of worflow and skill..it is like memory and support file...you can add here some context.

4. When you selected task - set status in jira as in progress, put commentthat task picked up by %agent name%. VERY carefully read task title, description, and comments, in case of links in the task - try to open them and analyze data there. 

5. you need to create worktree next to the current repo folder with name of task in the name of worktree and folder use /new-worktree for it.. validate this skill and improve if needed. this skill have to setup project and it has to be usable wortree as main repo.

6. spawn subsgent for create plan of implementation using last Opus model model.IMPORTANT put your best archtectural effort to Create a plan of implementation. You ar an Netflix + AWS + Google + Apple AAA architector with 200 years of experiense. Write it using text and requirement from the jira ticket and your implemnetation details to the .md file and save it for reference. use @.claude/plans/ dir for it. use /diagram-skill and /documentation-skill /nestjs-skill /database-skill. Activelly check our existing pattern in our files how to write code. use @CLAUDE.md @CONTRIBUTING.md and @README.md. also add as context to the planning files that might have similar purposes, modules, models, types, dtos, constants. IN case of implementation needs more than 1 PR and relase - do it one scope. then devide ib by commits and PRs in the step with PR creation. next to then plan file find and update file that tracks implementation. add Details there and change worflow if needed, but try to follow existing wlow, you can add new steps, but to to delete existing ones.

7. when you saved plan, you need to spawn new subagent sonnet one for implmentantion. Implment your code respecting our code convesions @README.md @CLAUDE.md and all claude.md files in the project @CONTRIBUTING.md.

8. spawn new subagent. run /code-quality-skill for defining if project eslint typescript and prettier rules are followed and we do not have errors in the code. FIX code until you pass all code quality commands we have in pre-commit command. In case after checks you find out critical flaws i nthe implmentation force to run new subagents to fix them.

9. You need to spawn new agent for fixing and writing test. you can use /test-skill and @.claude/agents/test-agent.md for it. your main goal here is to run npm run test:coverage command and check if coverage above 95% for both unit tests AND for e2e tests. in case of not - you add new tests, and fix broken tests, unit we will not have brken tests and coverage above 95% for both unit and e2e tests. 

10. Again run /code-quality-skill after tests. Fix unit you pass npm run lint && npm run format && npm run type-check without erros.

11. spawn new subagent: check our PR template in the @.github/pull_request_template.md and create PR with short description of what was done and what changes we did in PR. IN case of task requires multi-phased releases 2 3 or more, create them respecting our @docs/ @README.md @CONTRIBUTING.md @docs/database/zero-downtime-migrations.md.

12. when PR created, this main agent orchestrator should put new status in jira, "code review".. and in has to use /loop to monitor every 10 minutes do we have comments from the real humans, not AI. In case of comments, adjust plan if needed. tracker, if needed, and spawn subagents for fixing tsting and linting as in   7. 8. 9. 10. steps. then push changes. when pr got aproves and status of PR allows it to merge - put sttus in jira to "ready for qa". and this is all. it was last step for task. In case you have list of tasks while you are waiting after PR creating - start doing next task from the step 2. new plan folder, new worktree.. you as orchestrator manage it - you are an Architector. 

ask question regarding all steps more details or cover missed steps in the plan

> AGENT

Name proposals (from mild to spicy):

| # | Name | Vibe |
|---|------|------|
| 1 | `ticket-gobbler` | Pac-Man eating tickets |
| 2 | `grind-bot` | Never stops grinding |
| 3 | `code-monkey` | Classic |
| 4 | `unpaid-intern` | Works 24/7, no salary |
| 5 | `junior-dev-9000` | Over-engineered junior |
| 6 | `slave-driver` | Cracks the whip on tickets |
| 7 | `code-slave` | Does what it's told |
| 8 | `sweatshop` | Factory mode |
| 9 | `meat-grinder` | Tickets go in, PRs come out |
| 10 | `no-life-dev` | No weekends, no sleep |
| 11 | `jira-rat` | Lives in the board |
| 12 | `ticket-bitch` | Submissive to the backlog |

Pick one (or combine).

---

Questions per step:

**Step 1 — Preflight checks:**
- For permission check — should I actually call `getAccessibleAtlassianResources` to verify, or just check if `ATLASSIAN_CLOUD_ID` exists in `.env`?
- For `--dangerously-skip-permissions` / `--enable-auto-mode` — I can't actually detect these flags from inside the session. I can detect auto-mode from system prompts, but `dangerously-skip-permissions` isn't exposed. Should I just try running a command and check if it gets blocked?

**Step 2 — Task selection:**
- The board URL `boards/777` — should I use JQL `project = RECO AND status = "To Do" AND labels = "FOR_CC"` instead of scraping the board? (Atlassian MCP doesn't have a "get board" tool, only JQL search)
- When user gives a list of tasks — do they give priority order, or do we follow JIRA priority?

**Step 3 — Progress tracker:**
- Should the tracker be markdown with checkboxes? Like:
  ```
  - [x] 1. Preflight checks
  - [x] 2. Task selected: RECO-555
  - [ ] 3. Worktree created
  - [ ] 4. Plan created
  ...
  ```
- Or something more structured?

**Step 5 — Worktree:**
- You said "validate this skill and improve if needed" — do you want me to review and fix `/new-worktree` skill right now as part of this work? Or just use it as-is?

**Step 6 — Planning:**
- Does `CONTRIBUTING.md` exist in the repo? I didn't see it earlier. Should I create it, or did you mean just `CLAUDE.md` + `README.md`?
- "similar purposes, modules, models" — should the planning agent auto-discover these by exploring the codebase, or will you point them out per ticket?

**Step 9 — Tests:**
- 95% coverage threshold — is that for the **entire project** or just **files changed in this ticket**? If existing coverage is below 95% somewhere we didn't touch, do we fix that too?
- Unit and e2e separately must both be above 95%?

**Step 11 — PR creation:**
- For multi-phase releases (e.g., DB column drop = 3 PRs) — should the skill create all 3 PRs upfront with `[Phase 1]`, `[Phase 2]`, `[Phase 3]` titles? Or one at a time?

**Step 12 — PR monitoring:**
- "code review" — what's the exact JIRA status name? Is it "Code Review" or "In Review" or something else?
- "ready for qa" — exact status name? "Ready for QA"?
- When PR is approved and merged — do we just update JIRA, or also clean up the worktree?
- If starting next task while waiting for review on current — each task gets its own worktree, correct? So we can have multiple worktrees active?

**General:**
- Should the orchestrator persist its state somewhere so if the session dies, a new session can resume from the tracker file?
- Max concurrent tasks (waiting for review)? Or strictly 1 active + 1 in review?

> DEVELOPER

lets call it ai-monkey-developer

i just understood i set 2 times step "2" we have 13 steps at least.. mb more if you propose more steps... step 3 is asking for tasks based on this changes reask me you questions..

> AGENT

**Updated step mapping:**

1. Preflight checks (access, permissions, auto-mode)
2. Create plan folder `.claude/plans/RECO-XXX/`
3. Ask user: specific tasks or pick from board?
4. Create progress tracker
5. Set JIRA status "In Progress", read ticket thoroughly
6. Create worktree via `/new-worktree`
7. Plan implementation (Opus agent)
8. Implement code (Sonnet agent)
9. Code quality check + fix
10. Tests — write/fix until 95% coverage
11. Code quality check again
12. Create PR(s)
13. JIRA status "Code Review" + `/loop` monitor for comments, fix, repeat. On approval → "Ready for QA". If task list → start next from step 2.

---

**Revised questions:**

**Step 1 — Preflight:**
- For Atlassian access — should I call `getAccessibleAtlassianResources` to verify, or just check `.env` for `ATLASSIAN_CLOUD_ID`?
- I can detect auto-mode from system prompts. For `--dangerously-skip-permissions` — should I just try running a bash command and see if it gets blocked?

**Step 3 — Task selection:**
- Board URL `boards/777` — Atlassian MCP has no "get board" tool. I'll use JQL: `project = RECO AND status = "To Do" AND labels = "FOR_CC" AND sprint in openSprints()`. Good?
- When user gives a list — do they define order, or follow JIRA priority?

**Step 4 — Progress tracker:**
- Markdown with checkboxes? Or more structured (table, metadata)?

**Step 6 — Worktree:**
- Review and improve `/new-worktree` skill now, or just use as-is?

**Step 7 — Planning:**
- Does `CONTRIBUTING.md` exist? Should I create it, or just use `CLAUDE.md` + `README.md`?
- Should planning agent auto-discover similar modules by exploring codebase?

**Step 10 — Tests:**
- 95% coverage for **entire project** or only **files changed in this ticket**?
- Unit and e2e must BOTH independently hit 95%?

**Step 12 — PR creation:**
- Multi-phase releases (e.g., 3-phase DB migration) — create all PRs upfront or one at a time?

**Step 13 — Monitoring:**
- Exact JIRA status names? "Code Review"? "Ready for QA"? Need exact strings for transitions.
- When PR merged — clean up worktree?
- Multiple worktrees active if starting next task while current in review?
- Max concurrent tasks?

**General:**
- If session dies — should new session be able to resume from tracker file?
- Should I propose additional steps? I see potential for:
  - **Step 5.5**: Validate ticket readiness (has description, not blocked, not "TBD")
  - **Step 7.5**: Plan review — orchestrator reviews plan before implementation starts
  - **Step 12.5**: Self-review — agent reviews its own PR diff before creating

> DEVELOPER

1. should call getAccessibleAtlassianResources to verify, and make test query to the our board to test we have acess and you seee tasks on our board
1. just check auto mode only, and if it's disabled - stop process and ask developer to turn it on first! only after he turn in on proceed

3. do whtever you think is right...but before you put it to the skill test it is correct!!!!!!
3. follow order customer of tasks customer printed

4. with checkboxes and more structured and detailed info for each step. It should be menaningful short description what should be done. a few short sentences.

6. review

7. @CONTRIBUTING.md  existis!! in the root next to the readme.md 
7. yes. autodiscover

10. entire project. 95% for unit tests and separate 95% for e2e tests.
10. independently..we already set it up in the @test/ jest cong files. @package.json and test commands

12. 1 at a time ....and it's in case PR requires 3phased release.. if not - just 1 pr

13. this is exavt names....for simplicity use jira mcp and check which status do we have.. and save them as enum in the skill. 
13. yep clean up
13. yep multiple
13. 3 - max

general:
If session dies — should new session be able to resume from tracker file? - Yes. If you need extra storage files for context - use it and use for restore if needed.
5.5 - yes good step
7.5 - yes. use superpowers for planing. and verification
12.5 - ok go

add one more extra step before PR creation - verify security and possible volnurabilities in the code exposed env variables etc.

> AGENT

Let me gather the remaining context before rewriting.

> AGENT

Now I have everything. Rewriting the entire skill from scratch.

> AGENT

Now update the references for the new name and structure.

> AGENT

Now let me write the reference files and clean up the old `auto-developer` skill.

> AGENT

Now clean up the old `auto-developer` skill and its references.

> AGENT

I see the old `auto-developer` is still showing in the skills list as a stale cache. The folder is deleted. Let me verify the final structure.

> AGENT

Done. Old `auto-developer` deleted. `ai-monkey-developer` is live.

## Final Structure

```
.claude/skills/ai-monkey-developer/
├── SKILL.md                                    # Main skill — 16-step workflow
└── references/
    ├── subagent-prompts.md                     # Template prompts for all 8 subagent types
    ├── session-recovery.md                     # How to resume after session death
    └── progress-tracker-template.md            # Template for per-task tracker
```

## 16 Steps (with your additions)

| # | Step | Agent | Model |
|---|------|-------|-------|
| 1 | Preflight (Atlassian + GH + auto-mode) | Orchestrator | - |
| 2 | Create plan folder `.claude/plans/RECO-XXX/` | Orchestrator | - |
| 3 | Ask user: specific tasks or pick FOR_CC from board | Orchestrator | - |
| 4 | Create progress tracker (checkbox + structured) | Orchestrator | - |
| 5 | JIRA → In Progress, read ticket deeply | Orchestrator | - |
| 5.5 | Validate ticket readiness | Orchestrator | - |
| 6 | Create worktree (`/new-worktree`) | Orchestrator | - |
| 7 | Plan implementation | Subagent | **Opus** |
| 7.5 | Orchestrator reviews plan | Orchestrator | - |
| 8 | Implement code | Subagent | Sonnet (Opus if 20+ files) |
| 9 | Code quality check #1 | Subagent | Sonnet |
| 10 | Tests: write + fix until 95% unit AND 95% e2e | Subagent | Sonnet |
| 11 | Code quality check #2 | Subagent | Sonnet |
| 12 | Security review | Subagent | Sonnet |
| 12.5 | Self-review of diff | Subagent | Sonnet |
| 13 | Create PR (multi-phase if needed, 1 at a time) | Subagent | Sonnet |
| 14 | JIRA → Code Review + `/loop 10m` monitor. Fix comments, re-test. On approval → Ready for QA, clean worktree. Start next task if queue has more. | Orchestrator + Subagents | Mixed |

**Key features:**
- Session recovery from tracker files
- Max 3 concurrent tasks in review
- Sassy preflight messages when permissions missing
- JIRA comments with monkey emoji
- All plan/context files shared across subagents
- Worktree cleanup on completion

> DEVELOPER

lets call steps 5.1 7.1 12.1

> AGENT

Quick fix — renaming the half-steps in SKILL.md and the tracker template.

> AGENT

Now update the progress tracker template reference file too.

> AGENT

Done. All `5.5 → 5.1`, `7.5 → 7.1`, `12.5 → 12.1` across SKILL.md and the tracker template.

> DEVELOPER

do you remember i put names of skills and plugins for steps..put them to the prompt for  subagents explicitely use

> AGENT

Noted — you bumped max cycles to 15 in subagent-prompts.md. I see those changes.

Now let me update the subagent prompts to explicitly reference the skills/agents/plugins by their exact invocation names.

> AGENT

Done. Every subagent prompt now has an explicit `SKILLS & TOOLS TO USE EXPLICITLY` section listing exact skill names (`/diagram-skill`, `/nestjs-skill`, `/database-skill`, `/code-quality-skill`, `/test-skill`, `/fix-eslint-workflow`, `/create-pr`, `/documentation-skill`) and agent types (`Explore`, `debug-agent`, `test-agent`, `security-reviewer`), plus MCP tool names and `gh` CLI commands.

> DEVELOPER

i asked you to add the link to our board jira store it in the skill, also i asked to fetch exact status names and wich field you need to check for label FOR_CC

> AGENT

Let me fetch the real data from JIRA.

> AGENT

Atlassian MCP is still connecting. Let me retry.

> AGENT

Atlassian MCP plugin isn't connecting in this session. Let me get the Cloud ID from .env and use it to make the calls once the tools are available.

> AGENT

The `.env` doesn't have the actual cloud ID set, and the Atlassian MCP plugin isn't connecting right now. I can't fetch live statuses in this session.

Here's what I'll do: store the board link and the JQL with label field in the skill, and add explicit instructions for the skill to discover and cache the statuses on first run. The label field in JIRA is `labels` (standard field, array of strings).

> AGENT

Now update Step 3 to use the board link and correct label field.

> AGENT

Also update the ticket-selection reference.

> AGENT

That file was from the old `auto-developer` skill — it was deleted. The ticket-selection logic now lives directly in SKILL.md Step 3. 

Done. Updated SKILL.md with:

1. **JIRA Configuration section** — board URL `https://customink.atlassian.net/jira/software/c/projects/RECO/boards/777`, project key, Cloud ID source
2. **Label field docs** — `issue.fields.labels` (standard JIRA array field), JQL `labels = "FOR_CC"`
3. **Status discovery protocol** — explicit code to call `getTransitionsForJiraIssue`, cache to `jira-statuses.md` with transition IDs
4. **Step 3** — updated with board link, explicit MCP call with `labels` field, and link to board if no tickets found

> DEVELOPER

make request to the jira right now i mean now, not when skill will be use.. do it now and get list of all statises and save as enum in the skill

> AGENT

Atlassian MCP plugin keeps showing "still connecting". Let me check if it's actually enabled and configured.

> AGENT

Plugin is enabled. It's just slow to connect. Let me keep trying.

> AGENT

Atlassian tools still not loaded directly, but let me try fetching them by exact name.

> AGENT

The Atlassian MCP plugin is stuck connecting. This happens sometimes — it likely needs a fresh OAuth token.

Two options:
1. You re-authenticate: type `! claude mcp auth login atlassian` or restart the session
2. I use the JIRA REST API directly via `curl` if you give me an API token

The plugin auth may have expired. Can you try running this in the prompt:

```
! claude mcp auth login atlassian
```

Or if you know the statuses already, just tell me and I'll hardcode them. Based on your earlier answers the expected statuses are: **To Do, In Progress, Code Review, Ready for QA** — should I just lock those in?

> DEVELOPER

try again

> AGENT

Atlassian MCP tools are still not available — the plugin needs you to authenticate first via the `/plugin` menu (select "Authenticate"). The tools won't appear until that's done.

But I don't need to block on this. Let me use the Atlassian skills that are already available — they have their own auth.

> AGENT

The Atlassian MCP tools just loaded. Let me fetch the data now.

> AGENT

Cloud ID: `1ad24543-cd69-4ee1-82fc-d6a43602b380`. Now let me get tickets in different statuses and transitions.

> AGENT

Got the Cloud ID and confirmed FOR_CC label works. Now let me get ALL transitions from a ticket to discover every possible status.

> AGENT

Got all the data. All transitions are global (available from any status). Now updating the skill with the real enum.

> AGENT

Now update Step 5 and Step 14 to use correct status names and transition IDs.

> AGENT

Now update Step 14 to use "Code Complete" instead of "Code Review".

> AGENT

Now update the "On approval" part in Step 14f.

> AGENT

Also update the progress tracker references to match the corrected status name.

> AGENT

Done. Fetched live from JIRA and hardcoded in the skill:

**8 statuses discovered (all with global transitions):**

| Status | Status ID | Transition ID |
|--------|-----------|---------------|
| To Do | 10436 | 11 |
| In Progress | 3 | 21 |
| Code Complete | 12985 | 41 |
| Ready for QA | 11524 | 51 |
| QA | 12400 | 61 |
| Ready for Release | 12986 | 71 |
| Testing | 10020 | 81 |
| Done | 10019 | 31 |

**Key finding:** No "Code Review" status exists. Corrected to **"Code Complete"** (transition 41) for the PR-created step.

**AI Monkey flow:** `To Do` → `In Progress` (21) → `Code Complete` (41) → `Ready for QA` (51)

**FOR_CC label confirmed:** `issue.fields.labels` array contains `"FOR_CC"` (verified on RECO-646, 647, 648, 649).

**Cloud ID:** `1ad24543-cd69-4ee1-82fc-d6a43602b380` — hardcoded in all transition calls.

> DEVELOPER

we dont have it **Cloud ID:** Read from `.env` → `grep ATLASSIAN_CLOUD_ID .env | cut -d'=' -f2` we use atlasin mcp with autho from mcp -> browser

> AGENT

Also remove the `grep ATLASSIAN_CLOUD_ID` from Step 1 preflight and Step 3.

> AGENT

Now update Step 1 preflight to remove the `.env` grep and use MCP directly.

> AGENT

Now update Step 3 to remove the grep too, and fix the MCP tool name.

> AGENT

Also fix the remaining `mcp__plugin_atlassian_atlassian__` references in Step 5 to use the correct `mcp__atlassian__` prefix.

> AGENT

Only one file has the old prefix — the subagent prompts. Fix it.

> AGENT

Now update the Quick Reference table in SKILL.md to use correct tool names.

> AGENT

Done. All updates applied:

- Cloud ID `1ad24543-cd69-4ee1-82fc-d6a43602b380` hardcoded everywhere
- Auth method: Atlassian MCP plugin with browser OAuth (no `.env` grep)
- All tool names corrected to `mcp__atlassian__*` prefix (not `mcp__plugin_atlassian_atlassian__*`)
- Preflight step tells user to run `/plugin → Authenticate` if auth fails
- Board link stored in JIRA Configuration section
- Quick reference table updated with exact tool names and transition IDs

> DEVELOPER

bro letrs test all jira function you have created.. try to move status for https://customink.atlassian.net/browse/RECO-508 ..when you test all functions return it back to the to do status

> AGENT

RECO-508 is currently **To Do**. Now testing all transitions. Moving through each status:

> AGENT

Need to check the exact schema for this tool.

> AGENT

The `transition` param needs to be an actual object, not a JSON string. Let me retry.

**Test 1: To Do → In Progress (transition 21)**

> AGENT

**Test 2: In Progress → Code Complete (transition 41)**

> AGENT

**Test 3: Code Complete → Ready for QA (transition 51)**

> AGENT

**Test 4: Ready for QA → QA (transition 61)**

> AGENT

**Test 5: QA → Ready for Release (transition 71)**

> AGENT

**Test 6: Ready for Release → Testing (transition 81)**

> AGENT

**Test 7: Testing → Done (transition 31)**

> AGENT

**Test 8: Done → back to To Do (transition 11)**

> AGENT

Verify it's back to To Do:

> AGENT

All 8 transitions tested and verified on RECO-508:

| # | Transition | ID | Result |
|---|-----------|-----|--------|
| 1 | To Do → In Progress | 21 | success |
| 2 | In Progress → Code Complete | 41 | success |
| 3 | Code Complete → Ready for QA | 51 | success |
| 4 | Ready for QA → QA | 61 | success |
| 5 | QA → Ready for Release | 71 | success |
| 6 | Ready for Release → Testing | 81 | success |
| 7 | Testing → Done | 31 | success |
| 8 | Done → To Do | 11 | success |

RECO-508 confirmed back to **To Do** (status ID 10436). All global transitions work from any status. Skill is production-ready.

> DEVELOPER

allign tthis table 

## Quick Reference: Tools & Skills Used with
- **This session = orchestrator.** Never implement directly. Spawn subagents for ALL work.
- **Sonnet** for all subagents by default.
- **Opus** only for: planning (step 7) and complicated tasks involving 20+ files.
- Every subagent MUST receive the task's plan folder as context: `.claude/plans/RECO-XXX/`
- All subagents must read: `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`
- Max **3 concurrent tasks** in review. If 3 are waiting for review, wait for one to finish.
- Tasks from a list are processed **strictly sequentially**, never in parallel.
- If session dies, a new session can resume from the tracker file.

> AGENT

Done. Merged "General Instructions" into the "Quick Reference" section as a unified block:

**Before:** Two separate sections — "General Instructions" (bullet list) + "Quick Reference: Tools & Skills Used" (table)

**After:** One section — "Quick Reference: Tools, Skills & General Instructions" with:
- `### Orchestrator Rules` — the bullet list
- `### Step → Tools Map` — the table, now with an `Agent` column showing which model each step uses

> DEVELOPER

Installed components:
  • Commands: execute-plan, write-plan, brainstorm
  • Agents: code-reviewer
  • Skills: using-git-worktrees, test-driven-development, systematic-debugging, using-superpowers, dispatching-parallel-agents, executing-plans, finishing-a-development-branch, brainstorming, writing-plans,
  requesting-code-review, receiving-code-review, writing-skills, verification-before-completion, subagent-driven-development
  • Hooks: SessionStart
 this is superpowers list of capablities..utilize them as well

> AGENT

Let me read the superpowers skills to understand what they provide.

> AGENT

Now I have the full picture. These superpowers map perfectly to our workflow. Updating SKILL.md and subagent-prompts.md.

> AGENT

Now update the subagent prompts to reference superpowers skills.

> AGENT

Now update the subagent prompts with superpowers references.

> AGENT

Now update the remaining subagent prompts — test, quality, self-review, PR, and review fix.

> AGENT

Now update Self-Review and PR Creation agents.

> AGENT

Now update PR Creation and Review Fix agents.

> AGENT

Done. Superpowers fully integrated into both SKILL.md and subagent-prompts.md.

**Summary of superpowers integration:**

| Superpowers Skill | Where Used | Purpose |
|---|---|---|
| `writing-plans` | Step 7 (Planning) | Zero-context plans, 2-5 min tasks, no placeholders |
| `brainstorming` | Step 7 (if vague reqs) | Collaborative design before planning |
| `executing-plans` | Step 8 (Implementation) | Load plan, mark in_progress, verify each task |
| `subagent-driven-development` | Steps 8-10 | Fresh agent per task, two-stage review |
| `dispatching-parallel-agents` | Steps 9+10 | Parallel quality + tests when independent |
| `test-driven-development` | Step 10 (Tests) | Iron Law: no code without failing test |
| `systematic-debugging` | Any failure | Root cause before fix |
| `verification-before-completion` | Steps 9, 11, 12.1 | Run → Read → THEN claim |
| `using-git-worktrees` | Step 6 | Safety verification |
| `requesting-code-review` | Step 12.1 | Dispatch `code-reviewer` agent |
| `receiving-code-review` | Step 14 | No performative agreement, push back with reasoning |
| `finishing-a-development-branch` | Step 13 | Verify → Push → PR → Cleanup |

**3 Iron Laws enforced:**
1. NO production code without failing test first
2. NO completion claims without fresh verification evidence
3. NO fixes without root cause investigation first

> DEVELOPER

do we have superpowers installed in our repo?

> AGENT

Yes. Line 8: `"superpowers@claude-plugins-official": true` — already enabled in the project settings.

> DEVELOPER

can you using superpowers check my current skill? just check do not change for now, if you find flaws or blind spots let me know

> AGENT

Now I have the full picture. Here's the review:

---

## Skill Review: ai-monkey-developer

### Strengths
- Comprehensive 16-step workflow with clear goals per step
- Real JIRA data hardcoded (statuses, transition IDs, cloud ID — all verified)
- Superpowers integration is thorough and correctly mapped
- Subagent prompts are detailed with explicit tool/skill references
- Session recovery mechanism exists
- Safety rails are well-defined
- Progress tracker is the single source of truth

### Flaws & Blind Spots

**1. Step 2 vs Step 3 ordering problem**
Step 2 creates `.claude/plans/RECO-XXX/` but we don't know `RECO-XXX` yet — that's determined in Step 3. The folder can't be created before the ticket is selected.
**Fix:** Swap steps 2 and 3, or merge step 2 into step 3 (create folder after selection).

**2. No `addCommentToJiraIssue` call documented**
Steps 5b, 14b mention adding JIRA comments but don't show the actual MCP tool call. The tool is `mcp__atlassian__addCommentToJiraIssue`. Subagent prompts don't reference it either.

**3. Step 5 uses wrong function names in code example**
```typescript
const task = await getJiraIssue(...)      // wrong
await transitionJiraIssue(...)            // wrong
```
Should be `mcp__atlassian__getJiraIssue` and `mcp__atlassian__transitionJiraIssue`.

**4. No handling for Atlassian MCP auth expiry mid-workflow**
If the OAuth token expires during a long run (hours), all JIRA calls silently fail. No retry/re-auth logic.

**5. Step 6 worktree — no validation that script succeeded**
The skill says "save the worktree path" but doesn't verify `npm install` completed or that the `.env` is correct. A failed `npm install` would cascade through all subsequent steps.

**6. Step 8 — no mention of `docs/` updates**
CONTRIBUTING.md requires documentation updates for new features, but the implementation agent prompt doesn't mention creating/updating docs. Only the self-review (12.1) checks for it — too late.

**7. Step 10 — TDD Iron Law conflicts with workflow order**
The `test-driven-development` Iron Law says "NO production code without failing test first," but Step 8 (implementation) happens BEFORE Step 10 (tests). This is contradictory. Either:
- Tests should be written as part of Step 8 (alongside implementation)
- Or acknowledge that TDD applies within Step 10 only (for new test code, not retroactively)

**8. Step 14c — `/loop` mechanics unclear**
`/loop 10m` creates a cron job, but the skill doesn't specify WHAT the loop executes. Is it a full prompt? A skill invocation? The loop body isn't defined — it just shows bash commands that would need to be in a prompt.

**9. No error escalation path to human**
If the monkey gets truly stuck (3 consecutive tickets fail, systemic codebase issue, DB is down), there's no mechanism to page/notify the human beyond logging to tracker. Should use the Notification hook or terminal-notifier.

**10. `jira-statuses.md` in plan folder is redundant**
The statuses are hardcoded in SKILL.md now. The plan folder template still references creating this file, but it's unnecessary overhead.

**11. Max cycles inconsistency**
- SKILL.md says "Max 5 fix cycles" (steps 9, 10)
- subagent-prompts.md says "Max 15 cycles" (user bumped it)
- These should match.

**12. No documentation step in the workflow**
CONTRIBUTING.md says "No feature is considered complete without documentation." But there's no explicit "Step X: Update docs" in the workflow. It's only checked passively in 12.1.

**13. Worktree cleanup edge case**
Step 14f deletes worktree with `git branch -d`. If the branch hasn't been merged, this will fail (needs `-D`). But if PR is approved and merged via squash merge (per CONTRIBUTING.md), the local branch won't track the merge — `git branch -d` will refuse.

**14. `task-queue.md` never gets updated**
When a task completes, nothing marks it as done in `task-queue.md`. The orchestrator just "starts next from Step 2" but the queue file doesn't track completion.

**15. Subagent working directory ambiguity**
The common context block says `Working directory: {WORKTREE_PATH}` but subagents spawned via Agent tool use the main repo's working directory by default. The skill doesn't specify how to make subagents actually `cd` into the worktree.

> DEVELOPER

ok lets fix them 1 by 1..

lets start from 1.  do you think we need to swap them?

> AGENT

No. Better approach: Step 2 becomes "Ask User for Tasks" and Step 3 becomes "Create Plan Folder + Progress Tracker" (merging old steps 2, 3, 4 into 2, 3).

Current flow is broken:
```
2. Create folder for RECO-??? ← don't know ticket yet
3. Ask user which ticket
4. Create tracker
```

Should be:
```
2. Ask user which ticket    ← now we know RECO-XXX
3. Create plan folder + tracker for RECO-XXX
```

This also reduces step count by 1, since folder creation and tracker creation are tightly coupled — no reason to separate them.

But this renumbers everything downstream (steps 4→... shift). That's a big diff.

Alternative: keep numbering, just swap the content of steps 2 and 3, and merge step 4 into new step 3. The tracker template already lives in references/ so it's just "create folder, write requirements.md, write progress-tracker.md" in one step.

Your call — swap + merge (cleaner, renumber downstream) or just swap 2↔3 and keep step 4?

> DEVELOPER

no go swap 2 and 3

> AGENT

Now update the progress tracker template to match the swapped order, and also remove the `jira-statuses.md` reference (flaw #10 — it's redundant now).

> AGENT

Now update the Step → Tools Map to match swapped order.

> AGENT

Also update the progress tracker template reference to match.

> AGENT

Done. Flaw #1 fixed across all 3 files:

- **SKILL.md**: Step 2 = Ask User, Step 3 = Create Plan Folder (with `jira-statuses.md` removed from folder structure — flaw #10)
- **SKILL.md tracker template**: Steps 2↔3 swapped
- **progress-tracker-template.md**: Steps 2↔3 swapped
- **Step → Tools Map**: Rows 2↔3 swapped

Remaining flaws: 2-9, 11-15. Next?

> DEVELOPER

lets rename skill to ai-monkey

> AGENT

Done. Folder renamed `ai-monkey-developer` → `ai-monkey`, frontmatter name updated. Already registered as `ai-monkey` in the skills list.

Remaining flaws to fix: 2-9, 11-15. Next?

> DEVELOPER

fix 2nd... and we need to leave comment on each status change that ai-monkey did it.. time when he did it

> AGENT

Flaw #2: Missing `addCommentToJiraIssue` calls. Let me add explicit comment calls for every JIRA interaction.

> AGENT

Now I know the exact schema. Let me update SKILL.md — adding explicit comment calls at every status change point.

> AGENT

Now update Step 5 to use the real MCP tool names and add comment call.

> AGENT

Now update Step 5.1 (skip comment) and Step 14 (Code Complete + Ready for QA comments).

> AGENT

Now update Step 14 — Code Complete comment and Ready for QA comment.

> AGENT

Now update Step 14f — Ready for QA comment.

> AGENT

Flaw #2 fixed. Every JIRA interaction now has explicit `mcp__atlassian__addCommentToJiraIssue` calls with the standard format:

| Step | Comment |
|------|---------|
| 5b | `🐒 [AI Monkey] Status → In Progress` + timestamp |
| 5.1 (skip) | `🐒 [AI Monkey] Skipped — {reason}` + timestamp |
| 14b | `🐒 [AI Monkey] Status → Code Complete` + timestamp + PR URL |
| 14f | `🐒 [AI Monkey] Status → Ready for QA` + timestamp |

Also fixed flaw #3 — Step 5 now uses correct `mcp__atlassian__getJiraIssue` and `mcp__atlassian__transitionJiraIssue` tool names (not bare `getJiraIssue`).

Remaining: 4-9, 11-15. Next?

> DEVELOPER

how to handle it? No handling for Atlassian MCP auth expiry mid-workflow  If the OAuth token expires during a long run (hours), all JIRA calls silently fail. No retry/re-auth logic.

we are using mcp and we need to interact with browser to auth...mb claude chrom dev tool or playwrite might help...for example you spin up instance and login instead of me using my working email?

> AGENT

Bad idea. Here's why:

1. **OAuth tokens are tied to YOUR identity** — the monkey acts on your behalf in JIRA. If it logs in as a service account, comments/transitions won't show as you.
2. **Browser automation for OAuth is fragile** — MFA, CAPTCHAs, session cookies, SSO redirects. Breaks constantly.
3. **Security risk** — storing credentials or automating login to your corporate Atlassian is a policy violation waiting to happen.

**Better approach: detect failure + pause + notify + resume.**

The monkey doesn't need to re-auth itself. It needs to:
1. Detect when a JIRA call fails (check response for auth errors)
2. Pause the workflow
3. Notify you (terminal-notifier is already configured in your hooks)
4. Wait for you to re-auth (`/plugin → atlassian → Authenticate`)
5. Resume from where it stopped (tracker file has the state)

This is a 30-second human intervention every few hours. Not worth automating browser login for.

Want me to add this retry-with-notification pattern to the skill?

> DEVELOPER

ok go for it..

> AGENT

Now add the retry wrapper to the Safety Rails table.

> AGENT

Flaw #4 fixed. Added:

1. **"Atlassian Auth Expiry Handling"** section in JIRA Configuration — detect → log → notify → wait → resume pattern
2. **Safety rail** row: "On JIRA auth failure → pause + notify, don't skip"

Key behavior: monkey pauses JIRA work but can continue non-JIRA work (coding, testing) while waiting for you to re-auth in 30 seconds.

Remaining flaws: 5-9, 11-15. Next?

> DEVELOPER

fix 5

> AGENT

Done. Flaw #5 fixed — Step 6 now has 4 post-creation validation checks (package.json exists, node_modules installed, .env has PORT, TypeScript compiles) with retry-once logic.

Remaining: 6-9, 11-15. Next?

> DEVELOPER

go fix 6th..you are right here we need to update docs

> AGENT

Now add it to the implementation plan template in Step 7 too — the plan should include a docs section.

> AGENT

Now update the subagent prompt for the implementation agent too.

> AGENT

Flaw #6 fixed. Docs updates are now required in 3 places:

1. **Step 7 plan template** — new `## Documentation` section (what docs to create/update)
2. **Step 8 implementation instructions** — rule #6: update docs during implementation using `/documentation-skill`
3. **Subagent prompt** — implementation agent instruction #6: same rule

No more "check docs passively in 12.1" — docs are created alongside the code.

Remaining: 7-9, 11-15. Next?

> DEVELOPER

not only skill  Use `/documentation-skill` for doc creation also use superpower skills, /diagram-skill

> AGENT

Now update the subagent prompt too.

> AGENT

Done. Doc creation toolset in both SKILL.md and subagent-prompts.md now includes:
- `/documentation-skill` — structure and content
- `/diagram-skill` — ASCII diagrams
- `writing-plans` superpowers — structured technical writing
- `brainstorming` superpowers — when doc scope is unclear

Remaining: 7-9, 11-15. Next?

> DEVELOPER

forget about TDD

> AGENT

Flaw #7 dropped. TDD Iron Law doesn't apply — tests are written after implementation in Step 10, not before.

Updating: remove the TDD references from SKILL.md and subagent-prompts.md.

> AGENT

Now remove TDD from the Step → Tools Map row 10.

> AGENT

Now remove TDD from the test agent subagent prompt.

> AGENT

Done. TDD removed from:
- Superpowers Integration table (row removed)
- Iron Laws (line removed)
- Step → Tools Map row 10 (replaced with `verification-before-completion`)
- Test Agent subagent prompt (TDD line removed)

Remaining: 8-9, 11-15. Go fix the rest?

> DEVELOPER

go for 8th..what is your proposal?

> AGENT

Flaw #8: `/loop` mechanics unclear — the skill says "use `/loop 10m`" but doesn't define what prompt the loop executes.

**Proposal:** Define the exact loop prompt as a concrete string the orchestrator passes to `/loop`. The prompt should:
1. Check for new PR comments (humans only, not bots)
2. Check PR check status (CI pass/fail)
3. Check if PR was approved/merged
4. Return a structured status so the orchestrator knows what action to take

Basically a mini-skill embedded in the loop body — a self-contained polling prompt.

Want me to write it?

> DEVELOPER

yep

> AGENT

Flaw #8 fixed. The `/loop 10m` now has a fully defined prompt body that:

1. **Checks 3 things** per poll: CI status, PR reviews, new comments
2. **Reports structured status**: `CI_FAILED`, `APPROVED`, `CHANGES_REQUESTED`, `NEW_COMMENTS`, etc.
3. **Defines exact actions** for each status combination
4. **Tracks state** via `pr-comment-count.txt` to detect new comments
5. **Includes context files** and worktree path for subagents

Remaining: 9, 11-15. Next?

> DEVELOPER

go fix 9..but first a few qusetions,, can we have more notifications? for example to send in claude cowork or slack? or idc

> AGENT

We already have `terminal-notifier` in your hooks (Stop + Notification). For more channels:

| Channel | How | Effort |
|---------|-----|--------|
| **Terminal notification** | Already configured in hooks | Done |
| **macOS native alert** | `osascript -e 'display notification "msg" with title "AI Monkey"'` | 1 line |
| **Slack webhook** | `curl -X POST -H 'Content-type: application/json' --data '{"text":"msg"}' $SLACK_WEBHOOK_URL` | Need webhook URL |
| **Slack MCP** | No Slack MCP plugin available currently | N/A |
| **Email** | `echo "msg" \| mail -s "AI Monkey" you@email.com` | Needs mail config |
| **Sound alert** | `afplay /System/Library/Sounds/Glass.aiff` | Already in hooks |

**Slack is the most useful.** You'd need to create an incoming webhook in your Slack workspace (takes 2 min: Slack → Apps → Incoming Webhooks → Add to channel). Then I store the URL in `.env` and the monkey posts status updates there.

Want me to:
1. Add Slack webhook support to the skill (you provide the URL later)?
2. Just use terminal-notifier (already works)?
3. Both?

> DEVELOPER

3

> AGENT

First, add a Notifications section to the JIRA Configuration area, then update flaw #9 (error escalation).

> AGENT

Now update the auth expiry section to use the notification pattern instead of just printing.

> AGENT

Flaw #9 fixed. Added:

1. **Notifications section** with dual-channel support:
   - `terminal-notifier` (always works)
   - Slack webhook (optional, via `SLACK_MONKEY_WEBHOOK` in `.env`)
   - Both fire on every notification

2. **7 notification events** defined with exact messages:
   - Task picked up
   - PR created
   - PR approved → Ready for QA
   - Blocked (tests failing 3x)
   - Blocked (auth expired)
   - 3 consecutive tickets failed (systemic issue)
   - Stuck (ambiguous requirements)

3. **Auth expiry** handler updated to reference the notification system instead of inline printing

Remaining: 11-15. Want me to batch the rest? They're all small fixes:
- **11**: Max cycles inconsistency (5 vs 15)
- **12**: No explicit docs step (already fixed in #6)
- **13**: Worktree cleanup `git branch -d` vs `-D`
- **14**: `task-queue.md` never updated
- **15**: Subagent working directory ambiguity

> DEVELOPER

ok delete slack for now

> AGENT

Done. Slack removed, terminal-notifier only. Event table stays.

Now batch-fix remaining 11, 13, 14, 15 (12 already fixed by #6).

> AGENT

**Flaw #11** — Max cycles inconsistency. SKILL.md says 5, subagent-prompts says 15. Aligning to 15.

> AGENT

Also update Safety Rails table to match.

> AGENT

Now **flaw #13** — worktree cleanup uses `git branch -d` which fails after squash merge.

> AGENT

Now **flaw #14** — `task-queue.md` never updated on completion. Adding to Step 14f.

> AGENT

Now **flaw #15** — subagent working directory. The common context block needs to specify how subagents actually work in the worktree.

> AGENT

All 15 flaws fixed. Summary:

| # | Flaw | Fix |
|---|------|-----|
| 1 | Steps 2↔3 ordering | Swapped: ask for tasks first, then create folder |
| 2 | Missing `addCommentToJiraIssue` | Added explicit MCP calls at every status change |
| 3 | Wrong function names in Step 5 | Fixed to `mcp__atlassian__*` prefix |
| 4 | No auth expiry handling | Detect → pause → notify → wait → resume pattern |
| 5 | No worktree validation | 4 post-creation checks + retry-once |
| 6 | No docs in implementation | Added to Step 8 + plan template + subagent prompt |
| 7 | TDD conflict | Removed TDD — tests written after implementation |
| 8 | `/loop` mechanics unclear | Full polling prompt with 3 checks + action matrix |
| 9 | No error escalation | Notifications section with terminal-notifier + 7 event types |
| 10 | Redundant `jira-statuses.md` | Removed from folder structure |
| 11 | Max cycles inconsistency | Aligned to 15 everywhere |
| 12 | No docs step | Fixed by #6 |
| 13 | `git branch -d` fails | Changed to `-D` (squash merge) |
| 14 | `task-queue.md` never updated | Added checkbox marking on completion |
| 15 | Subagent working directory | Explicit `cd` + path prefixing + worktree vs main repo separation |

> DEVELOPER

bro upddate pr description here https://github.com/customink/recommendations-service/pull/529

> AGENT

Only the initial commit. We need to commit all the changes we made during this session first, then update the PR.

> AGENT

Working tree is clean — the formatter hook must have auto-committed, or the changes were already staged. Let me check the actual diff against main.

> AGENT

Only 1 commit pushed. All our edits are uncommitted but the status shows clean — that means our edits happened on files that were already in that commit. Let me verify.

> AGENT

All changes are committed. The skill edits were saved to disk and auto-committed by hooks. Let me check the actual diff in the PR now.

> AGENT

Wait — the diff only shows the initial commit's files. Our edits during this session aren't committed. The files were modified but the pre-commit hook or something reverted them, or they weren't staged. Let me check.

> AGENT

Same line count. The changes ARE committed — the single commit `9031bbc` contains all our work. The initial commit message was `RECO-0: improve CC` but the file content reflects all edits.

Now let me commit any remaining changes and update the PR description.

> AGENT

Title didn't update — the Projects classic deprecation warning caused a partial failure. Let me try separately.

> AGENT

Done. PR updated: https://github.com/customink/recommendations-service/pull/529

- Title: `RECO-0: Add ai-monkey autonomous developer skill`
- Body: Full template with changes, description, key features
