> DEVELOPER

What do we have open/pending in .agents/backlog.md ?

> AGENT

Open/pending items in `.agents/backlog.md` (5 of 7 entries are `pending`): | Date | Failure | Roles | Description | |------|---------|-------|-------------| | 06-22 | tool-error | specifier, integrator | Auto-mode classifier blocks in-role autonomous actions (`git reset --hard`, `gh pr merge`) without per-invocation direction — consider permission pre-authorization or prompt phrasing | | 06-22 | convention-gap | architect, hardender, ux-engineer, QA | 4 roles used 7-char git hash instead of required 10-char — add `git rev-parse --short=10 HEAD` to handoff template/constitution | | 06-22 | convention-gap | cleaner, QA | CRAP bootstrap invocation unclear: `python -m crap4py` should be `uv run python -m crap4py`; note rtk prefix breaks it | | 06-22 | tool-error | cleaner, hardender, architect | mutmut targeted/incremental run semantics misunderstood — no scan/count mode; targeted reruns reset cache; always analyze ALL survivors upfront | The other two are closed: one `applied` (stale `entire session current`) and two `wontfix` (GPG signing, f-string escaping).

> DEVELOPER

first item, do we need to update git settings.json for that? Check in ../swarm-forge, if needed create a PR there and here manually modify the settings.json

> DEVELOPER

Do not check example in swarmforge, if we will modify the settings there must be in the swarmfortge engine itself

> AGENT

Checked both. Here's the state: **swarm-forge engine — no change/PR needed.** The engine (`swarmforge.sh:522`) launches Claude with `--permission-mode acceptEdits` and does **not** ship or distribute any project `.claude/settings.json` permission allowlist. Its own `.claude/settings.local.json` only covers the swarm-forge repo itself (rtk git, cmux, notify-agent). There's no engine-level seam where per-project git permissions belong — permission pre-authorization is inherently per-target-project. **crap4py settings.json — already done.** `.claude/settings.json` already contains both rules the backlog item names: ```json "allow": [ "Bash(gh pr merge*)", "Bash(git reset --hard origin/*)" ] ``` It's gitignored (`.claude/*`), so it's local-only — nothing to commit. So: nothing to PR in swarm-forge, and the manual settings.json edit is already in place. One gap worth noting: `git reset --hard origin/*` only matches resets to a remote ref. If a role runs `git reset --hard HEAD` or `git reset --hard <sha>` it'd still prompt. Want me to broaden it to `Bash(git reset --hard*)`?

> DEVELOPER

swarm-forge, check that we update the settings file, we need to include this too. And update status here of this tasks/ledger as needed

> AGENT

swarm-forge's `.claude/` is gitignored — so this is a local-only edit, no

> DEVELOPER

again, do not check the settings in swarm-forge project, check that the swarm forge engine modifies the settings

> AGENT

The engine does **not** touch any project `.claude/settings.json` — it writes `.gitignore`, git excludes, `notify-agent.sh`, and prompt files, then launches with `--permission-mode acceptEdits`. So permission allow-rules are never provisioned by the engine. That's the gap. Let me read the relevant setup section to add it correctly.

> AGENT

Now I'll create the branch and implement the engine change.

> AGENT

Understood — pivot to the setup skill. Let me locate the setup-swarm skill (it already "writes permission allow-rules").

> DEVELOPER

ok, in that case include in setup skill or as needed

> DEVELOPER

Wwhich was yours previous plan?

> AGENT

My previous plan (engine-script approach, before you pivoted to the setup skill): **Branch:** `feat/provision-claude-permission-allowlist` in swarm-forge (already created). **Change:** Add a new `ensure_claude_settings()` function to `swarmforge/scripts/swarmforge.sh`, mirroring the existing `ensure_initial_gitignore` / `ensure_runtime_git_excludes` setup functions, and call it alongside them (after line 561, `ensure_runtime_git_excludes`). The function would, for the target `$WORKING_DIR`: - Ensure `.claude/settings.json` exists. - Merge these allow-rules into `.permissions.allow` (idempotent — append only if missing, order-preserving): - `Bash(gh pr merge*)` - `Bash(git reset --hard*)` (broader than crap4py's current `git reset --hard origin/*`) - Use `jq` when available; create the file fresh if absent; warn and skip if `jq` missing (never corrupt JSON). Then: open a PR on swarm-forge, and update the backlog/ledger status in crap4py to `applied`. You've now redirected this to the **setup-swarm skill** instead (which already "writes permission allow-rules"), which is the more natural home since it's the one-time provisioning step. Do you want me to drop the engine-script change and the branch, and implement it in the setup skill instead?

> DEVELOPER

no, modify the setup, and go on

> AGENT

The skill isn't in the `swarm-forge` engine repo — it lives in `gabadi-swarm-forge` (canonical) and is installed into projects like crap4py. Let me check which is source-of-truth and read the relevant section.

> DEVELOPER

ok, so check there we can modify the settings file maybe

> AGENT

The skill's Step 4 already writes both rules — the only gap is `git reset --hard origin/*` is narrower than the backlog item needs (`git reset --hard` without a remote ref still prompts). I'll broaden it to `git reset --hard*` in the canonical skill.

> AGENT

Now commit and open the PR on the canonical repo:

> AGENT

PR #25 created. Now clean up the abandoned engine branch and apply the same changes locally in crap4py (installed skill copies + settings.json + backlog/ledger).

> AGENT

Now broaden crap4py's own active `.claude/settings.json` rule:

> AGENT

Now update the backlog status and check the ledger. Let me look at the ledger files referenced in git status:

> AGENT

The same classifier-blocking issue appears three times in the swarmforge ledger (lines 35, 54, 83) — all resolved by this pre-authorization fix. Marking them applied:

> AGENT

I over-matched — multiple ledger rows share each session-id, so I wrongly flagged unrelated entries (convention-gap/missing-artifact rows). Reverting those, keeping only the three genuine permission/reset tool-errors (35, 54, 83):

> AGENT

Reverts clean — only the three genuine permission/reset rows (35, 54, 83) stay `applied`. Done. Summary: **swarm-forge engine** — confirmed it never provisions `.claude/settings.json` (only writes `.gitignore`, git excludes, `notify-agent.sh`, prompts; launches with `--permission-mode acceptEdits`). Permission allow-rules are the **setup-swarm skill's** job (Step 4), which is the right home. **Canonical fix** — gabadi/swarm-forge PR **#25**: broadened Step 4's reset rule `git reset --hard origin/*` → `git reset --hard*` (the narrow form still tripped the classifier on `HEAD`/sha resets). `gh pr merge*` was already covered. **Applied locally in crap4py:** - Both installed skill copies (`swarmforge/skills/...` + `.claude/skills/...`) broadened to match. - Active `.claude/settings.json` rule broadened (gitignored, local-only). - `.agents/backlog.md`: item → **applied** with resolution note. - `.agents/ledger-swarmforge.md`: the 3 matching tool-error rows → **applied**; reverted 6 unrelated rows I initially over-matched. Abandoned the earlier engine-script branch (deleted). Note: PR #25 only changes the skill instructions — existing swarm projects keep their old narrow rule until setup-swarm is re-run (or edited manually, as I did here for crap4py).

> DEVELOPER

Whats next?

> AGENT

Three `pending` items remain in `.agents/backlog.md`, all from 2026-06-22: 1. **10-char git hash** (architect, hardender, ux-engineer, QA) — 4 roles used 7-char hashes in handoff drafts. Fix: add `git rev-parse --short=10 HEAD` as a mandatory line in the handoff-draft template / constitution handoffs article. 2. **CRAP bootstrap invocation** (cleaner, QA) — `local-engineering.prompt` says `python -m crap4py` but correct form is `uv run python -m crap4py`; note `rtk` prefix breaks it. 3. **mutmut run semantics** (cleaner, hardender, architect) — no scan/count mode exists; targeted reruns reset cache. Fix: document "analyze ALL survivors upfront, never mix targeted+full runs." \#2 is the quickest and most mechanical (one-line prompt fix, same canonical-skill + local-copy pattern we just used). #1 is also low-effort. #3 is doc-only but needs careful wording. Want me to take #2 next?

> DEVELOPER

1. Apply

> DEVELOPER

1 and 2. Apply

> AGENT

The handoff template already uses `$(git rev-parse --short=10 HEAD)` (line 30) — the problem is roles paste a literal 7-char hash from `git log` instead of running the command. So the fix is an explicit mandate, not adding the token. Let me check if this article is canonical and apply there + locally.

> AGENT

Item 1 = canonical (`handoffs.prompt` identical); Item 2 = crap4py-only (`local-engineering.prompt` doesn't exist in canonical). **Item 1** — new canonical branch + explicit mandate:

> DEVELOPER

forget about cannonical now

> AGENT

Understood — leaving canonical alone. Cleaning up the empty branch I just made there, then applying both items to crap4py local files only.

> DEVELOPER

No, keep the prev change in cannonical, do not apply THIS change in cannonical

> AGENT

Good — PR #25 stays (it's on its own branch, untouched). This change stays crap4py-local only. **Item 1** — add the explicit mandate to crap4py's `handoffs.prompt`:

> AGENT

**Item 2** — fix the CRAP invocation in `local-engineering.prompt`:

> AGENT

Now mark both backlog items applied:

> AGENT

Now check the swarmforge ledger for related entries to these two items:

> AGENT

Let me finish the ledger updates for items 1 & 2, then restore the canonical change. First, current canonical state:

> AGENT

PR #25's branch still carries the broaden change intact (`main` is clean — the change correctly lives in the open PR). I'll confirm that after finishing the ledger. First, the related ledger entries. Items 1 & 2 each recur several times:

> DEVELOPER

i've restored already, anything missing here?

> AGENT

Let me confirm the full crap4py change set is coherent:

> AGENT

Canonical is restored (`main` has `git reset --hard*`; PR #25 still open — now somewhat redundant since you applied it to main directly, your call whether to close it). For items 1 & 2, everything is in place. What's still worth your attention: 1. **Real conflict I introduced** — my `handoffs.prompt` mandate says run `git rev-parse --short=10 HEAD`, but ledger rows **50 & 72** (left pending) say the **integrator** must hash `origin/main`, *not* `HEAD`, post-merge (HEAD stays on the integrator branch). So the blanket "HEAD" wording is wrong for that one role. Should I soften the mandate to "...`HEAD` (or the correct ref for your case, e.g. `origin/main` post-merge)" so it doesn't mislead the integrator? 2. **Backlog item 3 (mutmut semantics)** — still `pending`; you scoped this round to 1 & 2. 3. **My crap4py edits are uncommitted** — `handoffs.prompt`, `local-engineering.prompt`, `.agents/backlog.md`, `.agents/ledger-swarmforge.md` are tracked and modified but not committed. (`.claude/settings.json` and the skill copies are gitignored — local-only.) Want me to commit the tracked ones? Note: the other dirty files (`curator.md`, `curator.prompt`, `agent-retro/SKILL.md`, deleted fallback skills, `ledger-project.md`) predate this session — not mine, left untouched. Want me to fix #1, then handle #2 and/or #3?

> DEVELOPER

1. What do we need to do? we are making a lot of changes, you can see other changes,be aware

> AGENT

For #1 the fix is small and contained — just reword the one bullet I added so it's ref-aware instead of hard-coding `HEAD`. No new files, nothing else touched. That single edit also genuinely covers ledger rows 50 & 72 (the integrator `origin/main` case), so they can move to applied too. Here's the edit:

> AGENT

Now mark ledger rows 50 & 72 applied (now genuinely covered by the ref-aware wording):

> AGENT

Done. To answer your question directly — **#1 needed exactly one reworded bullet**, nothing more. The mandate now reads `git rev-parse --short=10 <ref>` with `HEAD` for the normal case and `origin/main` post-merge, so it no longer misleads the integrator. That closed the last two pending hash rows (50 & 72) too. State now, scoped to *only* what I touched this session: - `swarmforge/constitution/articles/handoffs.prompt` — ref-aware commit-hash mandate - `swarmforge/constitution/articles/local-engineering.prompt` — CRAP `uv run python -m crap4py` + rtk warning - `.agents/backlog.md` — items 14, 15, 16 → applied - `.agents/ledger-swarmforge.md` — all matching hash + CRAP + permission rows → applied - `.claude/settings.json` + both `setup-swarm` skill copies — broadened reset rule (gitignored / local) - Canonical: PR #25 open; you restored the change on `main` I have **not** touched the pre-existing dirty files (`curator.md`, `curator.prompt`, `agent-retro/SKILL.md`, the two deleted fallback skills, `ledger-project.md`) — those predate this session. Remaining backlog: **item 3 (mutmut semantics)**, still pending. Want me to take it, or commit the tracked edits first?

> DEVELOPER

Ok, what else is in backlog?

> AGENT

Backlog now — only **one item left**, everything else resolved: **Pending (1):** - **mutmut run semantics** (cleaner, hardender, architect) — no scan/count mode exists; targeted/incremental reruns reset the cache and report 0 files mutated. Rule to document: *analyze ALL survivors upfront, never mix targeted + full runs.* **Closed (6):** - ✅ applied — `entire session current` stale session (12) - ✅ applied — permission pre-auth / git reset + gh pr merge (14) - ✅ applied — 10-char commit hash mandate (15) - ✅ applied — CRAP `uv run python -m crap4py` (16) - ⛔ wontfix — 1Password GPG signing in worktrees (11) - ⛔ wontfix — f-string two-level escaping (13) The mutmut item is doc-only and lands in the same `local-engineering.prompt` CRAP/mutation section I already edited. Want me to take it?

> DEVELOPER

Explain, donnt understand. And its ok that all of them runs mutmut? check each prompt

> AGENT

Good catch to question this — the backlog item is actually **conflating two different problems across roles that don't all run mutmut the same way**. Here's what each prompt actually says: | Role | Runs language mutation (mutmut)? | What its prompt says | |------|------|------| | **hardender** | ✅ **Yes — owns it** | "Run the mutation tool **one file at a time**", "differential mutation **against the manifest**" (`hardender.prompt:14-15`) | | **cleaner** | ⚠️ Uses a **"scan/count mode"** | "Use the mutation tool's **scan/count mode**… to count mutation sites without running tests" (`cleaner.prompt:20,23`); but "**Do not run mutation tests**" (`:27`) | | **architect** | ❌ No mention in prompt | (constitution says architect must *fix* surviving mutants, but prompt never tells it to run anything) | | **QA** | ❌ No (unless asked) | "hardender owns mutation" (`QA.prompt:22`) | | **coder** | ❌ No | "cleaner, architect, hardender own those checks" (`coder.prompt:26`) | | **specifier** | ❌ Only *Gherkin* mutation, not mutmut | — | So **no, not all of them run mutmut** — only the hardender truly runs it. The cleaner only *counts* sites. **What the backlog item is reporting (two real bugs):** 1. **`cleaner.prompt` assumes a "scan/count mode" […]

> AGENT

Entire Recall: I'll ground the "why is this broken" explanation in the actual sessions where these roles hit the mutmut problem. Running preflight + searches.

> DEVELOPER

search will be empty, use @.entire/ search

> AGENT

## Closest precedent The mutmut behavior was learned the hard way and **already promoted into role knowledge docs** — but the **role prompts still contain the wrong instructions**. That gap is the whole story. - architect c531c23f → `.agents/roles/architect.md:3` - hardender d8370093 → `.agents/roles/hardender.md:11` - hardender 773c8e94 → ledger (worker-flag finding) ## Why it's actually broken — the mechanism mutmut keeps a cache in `mutants/` keyed on **which source functions changed**. That one fact causes every symptom: 1. **It only re-tests mutants in *changed source functions*.** Adding or editing a **test** file does *not* mark a source function as changed → mutmut **does not re-run** your new kill-test against the survivor. You "fix" it, re-run, and it still shows surviving — not because the test is bad, but because mutmut never executed it. (`architect.md:3`, c531c23f) 2. **After a source merge, everything shows `not checked`** until you re-run coverage *then* `mutmut run`. (`hardender.md:11`, d8370093) 3. **There is no "count/scan" mode.** You cannot enumerate mutation-site counts without actually generating/running mutants. 4. The worker flag is **`--max-children N`**, not `--max-workers N`. (773c8e94) ## So which prompts are broken, and why | Prompt | Line | Why it's broken | |--------|------|------| | **cleaner.prompt** | […]

> DEVELOPER

be more clear and direct

> AGENT

**Why the mutmut backlog item exists: the team learned how mutmut really works, wrote it into `.agents/roles/*.md`, but never fixed the role *prompts*. The prompts still tell roles to do impossible or wrong things.** mutmut's cache only re-tests mutants in **source functions that changed**. From that, three prompts are wrong: 1. **cleaner.prompt:20,23** — tells the cleaner to use a "scan/count mode" to count mutation sites. **That mode does not exist.** The cleaner can't do it. 2. **hardender.prompt:14** — "run one file at a time." Targeted runs fight the cache and print misleading `0 files mutated`. **Should be: one full run, fix all survivors.** 3. **hardender.prompt:18** — says `--max-workers 8`. **Wrong flag; it's `--max-children`.** 4. **local-engineering.prompt:10** — calls the cache "incremental" like it's safe. It hides two traps: adding a test does NOT re-test the mutant, and a merge wipes all results. Fix = 4 edits in 3 files to match what's already in `.agents/roles/`. Apply them?

> DEVELOPER

ok, a couple of things here. 1. .agents/role/ must automatically be loaded by swarmforge engine. 2. The mutmut incompatibilities are because its not the correct mutation engine, check for example unclebob mutate4go and mutate4clj, there you will find the mutation tool that we need to implement in the uture and we will not have this issue. Refrme based on this context

> AGENT

Let me verify point 1 — whether the engine actually auto-loads `.agents/roles/`:

> AGENT

Confirmed point 1 — and it changes the picture. Here's the reframe. ## Point 1: `.agents/roles/` is NOT auto-loaded by the engine today The engine's bootstrap (`write_agent_instruction_file`, swarmforge.sh:483) injects exactly two reads: ``` Read swarmforge/constitution.prompt … recursively Read swarmforge/roles/${role}.prompt … recursively ``` `.agents/roles/<role>.md` is **not** in that chain. It only reaches an agent indirectly — via `AGENTS.md` pointers ("See `.agents/roles/hardender.md`…"), which is **claude-only** (codex/grok/copilot don't read AGENTS.md the same way) and requires the agent to actively go read it. So your requirement "must automatically be loaded" is **not met**. The fix is one line in the engine's `write_agent_instruction_file`: ``` If .agents/roles/${role}.md exists, read it and obey it. ``` That makes the curator's promoted knowledge reach every agent deterministically, agent-agnostic — which is the whole point of promoting it. ## Point 2: the mutmut "bugs" aren't prompt bugs — it's the wrong tool mutmut's two footguns — **changed-function-only cache** and **no scan/count mode** — are fundamental mismatches with what the pipeline needs: - the **cleaner** needs to *cheaply count mutation sites* to gate file splits → mutmut structurally can't. - the **hardender** needs *deterministic full survivor analysis* → mutmut's incremental cache fights it. The real solution is **`mutate4py`**, modeled on unclebob's […]

> DEVELOPER

1. .agents/roles/<role>.md <- ensure that the curator uses this pattern, and this file its optioal . The file load must be dynamical, can be added new data while running in next iteration. this fix goes in the current branch in ../gabadi-swarm-forge (we already have some changes). And we can delete the AGENTS.md mappings now. Point 2: We will not create it now, we can update the .agents/roles/<role>.md now maybe, but we must keep the same idea, we don't run the full mutation, or from where are you taking this idea? reframe

> AGENT

Let me ground the reframe in the actual state before I assert anything (I clearly got the "full run" idea wrong — let me check where it came from too).

> AGENT

This is a more advanced fork — it already has **ADR 0013 (curator-knowledge-promotion)**, **ADR 0014 (agents-knowledge-injection)**, and **docs/tool-analysis-crap-dry-mutation.md**. Let me read the directly relevant ones before reframing.

> AGENT

ADR 0014 is **accepted but its `main` implementation is still pending** — that's exactly point 1. Let me find where the bundle is actually built in this fork (the `.sh` here lacks `write_agent_instruction_file`) and read the mutation tool-analysis doc for point 2.

> AGENT

This reframes both points correctly — and I was wrong about "full run." Let me read the exact bundle function and the crap4py AGENTS.md mappings before reframing + acting.

> AGENT

Now I have the full picture from the fork's own design docs. Here's the corrected reframe, then I'll execute point 1. ## Reframe ### Point 1 — this is ADR 0014, accepted but not yet implemented The fork already decided this: **ADR 0014 (`.agents/` knowledge contract injected into every bundle)**. Its `main` task is literally still pending — "extend the bundle generator to append `AGENTS.md` and `.agents/roles/<role>.md` when present." The real engine is `write-agent-instruction-file!` in **`swarmforge.bb:311`** (the ADR says `.sh`, but `.bb` is the live one). Today it injects only constitution + role prompt. Your refinements on top of the ADR: - **optional** → "if it exists" (silently skipped) ✓ matches ADR - **dynamic / next-iteration** → inject *by reference* (like the existing "Read …" lines) with "re-read at the start of every task," **not** inlined content — so curator updates land next iteration without relaunch - **curator owns the pattern** → already true (ADR 0013; curator.prompt creates `.agents/roles/<role>.md` lazily) - **delete AGENTS.md per-role mappings** → correct: once the engine injects each role's file role-scoped, the "See `.agents/roles/X.md`" pointers are redundant ### Point 2 — I was wrong about "full run," and here's where my error came from I took […]

> AGENT

Checking whether the `.sh` wrapper also needs the change or just delegates to `.bb`:

> AGENT

`.sh` just `exec bb` — single source, and the `.bb` parsed cleanly (failure was runtime config, not syntax). Now mark ADR 0014 implemented and delete the crap4py AGENTS.md mappings:

> AGENT

Now delete the redundant per-role mappings from crap4py's AGENTS.md:

> AGENT

Now verifying two dependencies of this deletion in crap4py: (a) does crap4py vendor the updated engine yet, and (b) do the actual `.agents/roles/*.md` files exist (so the deleted pointers lose nothing)?

> AGENT

Done with point 1. All five `.agents/roles/*.md` files exist, so deleting the AGENTS.md pointers lost **zero content** — the knowledge lives in those files, which the engine now injects. ## What I changed **gabadi-swarm-forge (current branch `main`, uncommitted alongside your SKILL.md change):** - `swarmforge.bb` — `write-agent-instruction-file!` now also injects, **by reference + "if it exists"**: root `AGENTS.md` (all roles) and `.agents/roles/<role>.md` (role-scoped). By-path, not inlined → optional + dynamic; re-read each task so mid-run curator updates land next iteration. (`.sh` just `exec bb`s it — single source; parsed clean.) - `docs/adr/0014-...md` — marked the pending `main` item **Done**, corrected `.sh`→`.bb`, noted the by-reference/dynamic choice. **crap4py:** - `AGENTS.md` — deleted the five redundant "### X role knowledge → See `.agents/roles/X.md`" pointer blocks. ## ⚠️ One sequencing risk you should know crap4py does **not** vendor the engine (`swarmforge.bb` isn't in its tree — it runs from the pinned install). So the injection only reaches crap4py **once its engine pin is upgraded** (ADR 0018). Until then, crap4py has *neither* the AGENTS.md pointers (just deleted) *nor* engine injection → role agents won't see `.agents/roles/*.md` during that window. You'll want to bump crap4py's engine pin before the next run, or hold the AGENTS.md deletion until […]

> DEVELOPER

~/workspace/addi/gabadi-swarm-forge/swarmforge/scripts/swarmforge.bb, but the role must be set, do not let the agent decide the role

> AGENT

You're right — let me make the role an explicit, engine-set fact rather than anything the agent infers. Reading the current state:

> AGENT

Confirmed — `role` interpolates to the concrete name (e.g. `hardender`), and the bundle now opens with an explicit, launcher-set role declaration: > `Your role is hardender. This is assigned by the launcher — do not infer, change, or adopt any other role.` So the role is fixed by the engine, the `.agents/roles/<role>.md` path is baked concretely (no agent guessing), and the file stays optional + dynamically re-read each task. Open threads from before, unchanged: - **Engine-pin gap in crap4py** — its pinned engine doesn't have this injection yet, and the AGENTS.md pointers are already deleted. Bump the pin before the next run, or I can check it. - **Point 2** — re-scope backlog item 17 (mutmut lacks `--scan` + stateful cache → structural fix is `mutate4py`, keep differential model) and optionally a one-line `.agents/roles/cleaner.md` note. Want me to take either now?

> DEVELOPER

engine pin forget, i'll apply later. Explain point 2

> AGENT

## Point 2 — what it is and what I propose **The backlog item (item 17)** says: "mutmut targeted/incremental run semantics misunderstood by 3 roles — no scan/count mode exists; targeted reruns reset cache and show 0 files mutated; **always analyze ALL survivors upfront, never mix targeted+full runs**." **Why it's misframed:** that bolded remedy ("analyze all survivors upfront, never mix targeted+full") points toward *full runs*. But your own `docs/tool-analysis-crap-dry-mutation.md` shows the intended model is the **opposite — differential by default**: - `--since-last-run` → skip functions whose hash matches the manifest (the normal path) - `--mutate-all` → force a full run (the exception) - `--scan` → count mutation sites, no tests So the "problems" aren't roles misusing mutmut, and the fix isn't "run full." They're **capability gaps in mutmut vs. the tool you actually designed**: - the **cleaner** wants `--scan` to count sites cheaply → mutmut has no such mode - the **hardender** wants clean differential-against-manifest → mutmut's incremental cache has footguns (adding a test doesn't re-test; a merge marks everything `not checked`) Those gaps disappear structurally when `mutate4py` is built (todo). Until then they're inherent to the workaround — not

> DEVELOPER

engine pin forget, i'll apply later. Explain point 2, do not give details, give me exactly what is missing

> AGENT

Point 2 — what's missing, exactly: 1. **Backlog item 17 is mis-scoped.** It blames the roles ("misunderstood") when the real cause is mutmut being the wrong tool. Needs re-scoping to: mutmut lacks `--scan` and has a stateful cache → structural fix is `mutate4py` (todo). 2. **`cleaner.prompt` tells the cleaner to use a "scan/count mode" that mutmut doesn't have.** Nothing records that this instruction is currently impossible. Missing: a note that the site-count gate can't run until `mutate4py` exists. 3. **No `.agents/roles/cleaner.md` mutmut entry.** The architect and hardender have their mutmut realities captured; the cleaner doesn't. 4. **`hardender.prompt:18` has a wrong flag** (`--max-workers`, should be `--max-children`) — already known in the ledger, never fixed in the prompt.

> DEVELOPER

ok, what do we need?

> AGENT

What we need for point 2 — four edits: 1. **Re-scope backlog item 17** — change its text from "roles misunderstood mutmut" to "mutmut lacks `--scan` + stateful cache; structural fix = `mutate4py` (todo); keep differential model." 2. **`cleaner.prompt`** — note the "scan/count mode" can't run on mutmut; the site-count split gate is deferred until `mutate4py`. 3. **`.agents/roles/cleaner.md`** — add the cleaner's mutmut reality (no `--scan`), matching what architect/hardender already have. 4. **`hardender.prompt:18`** — fix `--max-workers` → `--max-children`. All four are in crap4py (local prompts + backlog + role doc). None touch the engine. Want me to apply them?

> DEVELOPER

apply