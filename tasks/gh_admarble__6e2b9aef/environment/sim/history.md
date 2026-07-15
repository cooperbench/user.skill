> DEVELOPER

can you review our .entire logs. I havent seen any sub agents spawned lately. Have we abandoned sub agent use and agent teams. I feel like read only haiku agents were beneficial. Can you research?

> AGENT

Confirmed — there's a real drop-off. Data from your 141 transcripts at `/Users/tony/.claude/projects/-Users-tony-Projects-sequant/`: ## Quantitative trend (main-conversation Agent spawns) | Month | Sessions | With spawns | Total spawns | Haiku spawns | |------|----------|-------------|--------------|--------------| | April | 36 | **9 (25%)** | 21 | 0 | | May | 105 | **3 (2.9%)** | 3 | 0 | That's an order-of-magnitude regression. Last 30 sessions: only `f4422808` (May 11, Explore for docs audit), `926d8daf` (May 11, Explore), and `4401e0a5` (May 9, general-purpose). ## What replaced agents Recent zero-spawn sessions did the work inline: - `qa 543` → 21 Bash + 4 Read in main context - `qa 605` → 21 Bash inline - `assess 619 605 543 508` → 28 Bash inline (4 issues' worth of `gh`/`git` scraping) - `PM next issues` → 8 Bash inline (could have been a general-purpose research delegation) ## Haiku point specifically I never set `model: "haiku"` on a direct `Agent` call — every one of the 24 spawns inherited from parent (opus). The "haiku default" from your `project_agent_audit_2026.md` referred to **skill-internal** agents declared in `.claude/agents/`: - `sequant-explorer` → haiku ✓ (used by `/spec`) - `sequant-qa-checker` → haiku ✓ (used by `/qa`) - `sequant-implementer` → […]

> DEVELOPER

I want the fix portable to sequant users. I also noticed a few issues a while back. Agents couldn't edit worktrees and wasted work. I also notice that agents made a lot of mistakes. it couldve been the wrong models. can you investigate

> AGENT

Here's what I found across the codebase, history, and your past feedback. ## Past worktree-edit issues — already resolved | Issue | Status | Fix landed | |------|--------|-----------| | **#352** — Background QA agents silently failed on Bash | CLOSED | `bypassPermissions` in `.claude/agents/sequant-qa-checker.md` | | **#485** — Parallel /exec agents collided in shared worktree (the "wasted work" symptom) | CLOSED | `src/lib/worktree-isolation.ts` + `agents.isolateParallel` setting + `--isolate-parallel` CLI flag + `docs/features/worktree-isolation.md` | | **#465** — Small-diff fast path skips agents for trivial changes | CLOSED | Size gate in `qa/SKILL.md:947` (threshold 100) | The "agents couldn't edit worktrees" issue is structurally fixed. The remaining failure mode in my session memory (`feedback_qa_agent_worktree_verification.md`) is about **haiku QA agents hallucinating** file/API claims during code review — and the `qa/SKILL.md:143` now explicitly tells the orchestrator to do code review **inline** and only use the haiku checker for bounded grep-style scans (type-safety, security patterns, scope/size). ## Agent quality / "wrong models" — three concrete portable findings ### 1. **Bug: `agents.model` setting is dead config** ⚠️ - Written to `.sequant/settings.json` by `src/lib/settings.ts:827` - Documented as the "Sub-agent model" override in `docs/features/plugin-distribution.md:94` - **Zero consumers in `src/`, `.claude/skills/`, `templates/skills/`, or `skills/`** — verified with grep - […]

> DEVELOPER

lets research best practices to find out what really works before we setup an issue

> AGENT

Good call. Let me parallelize research across the official docs and the practitioner community.

> AGENT

Two strong reports — but they disagree on a key point (whether `isolation: worktree` is even a thing for subagents), and the practitioner agent made specific claims (env vars, GH issue numbers, SWE-bench scores) that I should verify before passing along.

> AGENT

Big find. The verification flipped the conclusion. ## Verified upstream Claude Code bugs | GH Issue | State | Impact | |---------|-------|--------| | **anthropics/claude-code #43869** | OPEN since 2026-04-05 | **All subagent model routing is broken.** Per-call `model:` param, `.claude/agents/*.md` frontmatter `model:`, and `CLAUDE_CODE_SUBAGENT_MODEL` env var are **all silently ignored**. Subagents always run on the parent's model. | | **#57718** | OPEN | Even when env var "works," it silently clamps the per-call `model:` parameter with no signal in `tool_result` or transcripts. | | **#47548** | OPEN | `isolation: worktree` switches the parent worktree's branch instead of creating an isolated one. | | #39886, #50850 | CLOSED | Other `isolation: worktree` regressions, fixed. | **This directly explains your "wrong models" intuition** — but inverted from my earlier framing: - Your `.claude/agents/sequant-qa-checker.md` declares `model: haiku` - Claude Code **ignores it** and runs it on whatever the parent is using (typically Opus 4.7 for you) - You've been paying Opus rates for every QA quality check since at least April. The settings.json `agents.model` field is the *second* broken pathway — even if I wired it through, Claude Code would still ignore it. The hallucination failures in my session memory (`feedback_qa_agent_worktree_verification.md`) were almost […]

> DEVELOPER

first pull data

> AGENT

Data is in. The community baseline differs sharply from what the practitioner agent claimed. ## Sample: 144 agents in VoltAgent/awesome-claude-code-subagents (19.6k stars) ### Field usage across the 144 agents | Field | Coverage | |------|----------| | `name`, `description`, `tools`, `model` | **144 / 144 (100%)** | | `maxTurns` | **0 / 144** | | `effort` | **0 / 144** | | `permissionMode` | **0 / 144** | | `isolation` | **0 / 144** | The practitioner agent (haiku) earlier cited specific production `maxTurns` values ("2 for fetch-extract, 3 for simple, 5 for multi-step, 30 for implementation"). I grepped the entire 1.9 MB repo — **zero mentions** of `maxTurns`, `max_turns`, or `max-turns` in frontmatter or prompt bodies. Those numbers were fabricated. (Ironic that the haiku agent hallucinating about haiku agents directly demonstrates your "agents make mistakes" concern.) ### Model distribution (n=144) | Model | Count | % | |------|------|---| | **sonnet** | 102 | **71%** | | opus | 25 | 17% | | haiku | 17 | 12% | Sonnet is the community default, not haiku. Per-category: | Category | Pattern | |---------|---------| | Language specialists | 30/30 **sonnet** | | Research / analysis | 8/8 **sonnet** | | Quality […]

> DEVELOPER

proceed

> AGENT

Let me draft and file. Quick self-critique pass first per your `feedback_critique_before_filing.md`: scope is two small ACs, evidence is verifiable (upstream issues, community baseline numbers), not duplicating #483.

> AGENT

Issue filed: **#632**. Now saving a memory so future sessions don't burn cycles re-discovering the upstream routing bug.

> AGENT

Done. Two artifacts: 1. **Issue #632** — `fix(agents): realign declared model tiers; document upstream routing bug` - https://github.com/sequant-io/sequant/issues/632 - Labels: `upstream`, `documentation`, `multi-agent` - 4 ACs: realign declarations, doctor warning, docs, optional dead-config cleanup - Out-of-scope section explicitly defers `maxTurns`/`effort`/`isolation` work with rationale 2. **Memory** — `project_upstream_subagent_model_bug.md` + MEMORY.md index entry, supersedes the model-routing claims in the older 2026-04-05 agent audit so future sessions don't relearn it. Open question worth your call: **#483's scope.** Right now it proposes `maxTurns` + `effort` caps on all 12 spawn sites, justified by token cost. The 144-agent community sample shows 0% adoption of either field — so the cost argument doesn't have community evidence behind it. The defensive `error_max_turns` handling (AC-14) is still useful regardless. Do you want me to leave a comment on #483 suggesting narrowing scope to just the graceful-failure ACs, or leave that for your manual triage?