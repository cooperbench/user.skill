> DEVELOPER

i'm seeing lots of duplicate skills related to the shape pack, is it a caching issue?

> AGENT

Not a caching issue — it's real duplication from how the same skill is registered under multiple names. Let me confirm against the actual files.

> AGENT

No, it's not caching. It's real, structural duplication — every shape workflow is registered up to **three times** under different names because it exists as both a *skill* and a *command wrapper*, and plugin commands get double-registered. Here's the breakdown: **Three name families, same 16 workflows:** | Family | Example | Source | Count | |--------|---------|--------|-------| | `shape-<name>` | `shape-delivery`, `shape-exec-build` | Plugin **skills** auto-discovered from `skills/<name>/SKILL.md`, prefixed by plugin name `shape` | 16 | | `<name>` (bare) | `delivery`, `exec:build` | **Command wrappers** in `.claude/commands/*.md` | 16 | | `shape:<name>` | `shape:delivery`, `shape:exec:build` | Same command wrappers, **plugin-namespaced** copy | 16 | So one workflow like delivery shows up as `shape-delivery` (the skill), `delivery` (bare command), and `shape:delivery` (namespaced command) — ~48 shape entries total for 16 actual workflows. **Why it exists:** The `.claude/commands/*.md` files are thin wrappers that just `@import` the matching `SKILL.md` and invoke it — they were added to give slash-command UX (`/delivery`) on top of the auto-discovered skills. Claude Code then registers each plugin command under both its bare name and the `shape:`-prefixed name, which is the doubling you see on top of the skills. ``` .claude/commands/delivery.md → @../../skills/delivery/SKILL.md (wrapper) skills/delivery/SKILL.md → the actual skill […]

> DEVELOPER

option 1

> AGENT

Good. One important nuance before I start deleting: two of those command files — `stop-the-line.md` and `ta[REDACTED_SK].md` — point at **hooks**, not skills, so they aren't duplicates of anything. They're the only manual entry point for those two hooks. Let me check the docs that reference the commands before I decide how much to remove.

> AGENT

There's an `install.sh` that generates wrappers/symlinks and an ADR that bakes in the wrapper convention — this is more wired-in than a simple folder delete. Let me read `install.sh` before touching anything.

> AGENT

Reading `install.sh` changes the picture — option 1 is bigger than just deleting a folder. The command wrappers are a **deliberate second install surface**, and they're generated/published by `install.sh`, declared in `plugin.json`, and locked in by an Accepted ADR. Full blast radius: - **`.claude/commands/*.md`** (16 files) — delete the wrappers - **`install.sh`** — remove step 1 (wrapper generation into `~/.claude/commands/shape/`) and the "Available commands" help block - **`plugin.json`** — drop the `"commands"` key - **`CLAUDE.md`, `CONTRIBUTING.md`** — remove the wrapper/`~/.claude/commands/shape/` references - **ADR 0005** — its decision table binds the wrapper convention; this change partially reverses it Two things genuinely need your call before I touch anything:

> AGENT

Both calls made. Plan: delete the 14 skill-duplicating wrappers, keep the 2 hook wrappers, update `install.sh`/docs, and write a superseding ADR. Let me set up a branch and gather the files I need to edit.

> AGENT

Now let me read ADR 0004 (the prefix split this partially reverses) so the superseding ADR cites it correctly.

> AGENT

Now I have the full context. Let me delete the 14 wrappers and scan for any other references to the dropped slash-command surface (README, using-this-pack, supervisor prompts).

> AGENT

The wrapper deletion is done (only the two hook commands remain). But the dropped slash-command surface is referenced across README, `references/`, `rules/`, and two skills — those become stale. Let me see the README section so I can reframe it accurately.

> AGENT

This touches the install/onboarding surface, so I'll fix it properly. Let me make the edits. Starting with README (the surface bullets and the walkthrough), then `install.sh`, `CLAUDE.md`, `CONTRIBUTING.md`, the prose cross-refs, and finally the ADR.

> AGENT

I need to Read the files before editing. Let me read the ones I'll edit.

> AGENT

I used the wrong verb form for the exec steps — the canonical verbs (per ADR 0004) are `exec:build`, not `shape:exec:build`. Let me fix.

> AGENT

Now `install.sh` — update the "Available commands" help block to list only the two remaining commands.

> AGENT

Now `CLAUDE.md` — the repo-structure line and the hooks listing (stop-the-line is shown but ta[REDACTED_SK] hook isn't).

> AGENT

Now CONTRIBUTING.md — the local-dev "what this wires up" list.

> AGENT

Now the prose cross-refs that still say you can type `/shape:X`. Let me read and fix them.

> AGENT

Now the edits:

> AGENT

Now `references/project-types.md` — the `/shape:project` verb refs (lines 5, 15, 21, 39) and the two buggy `skills/shape:project/` paths (362–363, which should be `skills/project/`).

> AGENT

Now the superseding ADR. Let me write ADR 0006.

> AGENT

Let me add back-pointers in ADR 0004 and 0005 so the record is navigable.

> AGENT

Let me sweep for any remaining stale slash-command references and sanity-check the install script still parses.

> AGENT

One live ref left — `README.md:73` points at `/shape:using-this-pack`, which never had a wrapper (it's the navigator skill). Let me fix it.

> AGENT

`README.md:147` describes install.sh as writing "slash-command wrappers" broadly. Let me tighten it.

> AGENT

Let me get a final diffstat to summarize.

> AGENT

Done. Here's what changed and why it fixes the "duplicate skills" you saw. ## Root cause (recap) Not caching. Each workflow shipped on **two install surfaces** — an auto-invocable skill (`shape-<name>`) *and* a slash-command wrapper that just re-imported the same `SKILL.md`. As a plugin, each wrapper was then registered twice (bare `delivery` + namespaced `shape:delivery`), so one workflow showed up three times in the picker. ## What I did (option 1) **Deleted the 14 skill-duplicating wrappers**, keeping only the two that aren't duplicates — `stop-the-line` and `ta[REDACTED_SK]`, which point at hooks and have no backing skill (their wrapper is the only manual trigger). Each workflow now appears once, as `shape-<name>`. Beyond the deletes, the wrapper surface was wired into several places, so I updated all of them: - **`install.sh`** — the "Available commands" help block now lists only the two utility commands; still generates wrappers, just for those two. - **`plugin.json`** — unchanged (the `commands` key is still valid for the two remaining wrappers). - **`README.md`** — rewrote the install bullets and the 7-step walkthrough to present workflows as skills (`shape:idea`, `exec:build`, …) invoked by name/auto-trigger, not typed `/`-commands; fixed `/shape:using-this-pack` (never a real command) and the install-script description. - […]

> SYSTEM

This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation. Summary: 1. Primary Request and Intent: - **Initial diagnostic:** User saw "lots of duplicate skills related to the shape pack" and asked whether it was a caching issue. Intent: understand why the skill picker shows triplicate entries. - **Remediation (option 1):** User chose to **drop the command-wrapper surface entirely** to eliminate the duplication, accepting loss of the typed `/shape:X` slash-command UX. - **Two refinements via AskUserQuestion:** - Keep the two hook-pointing wrappers (`stop-the-line`, `ta[REDACTED_SK]`) since they are the only manual trigger for those hooks and aren't duplicates — delete only the 14 skill-duplicating wrappers. - Write a superseding ADR to record the decision (matching the repo's ADR discipline), rather than just editing silently. 2. Key Technical Concepts: - Claude Code plugin skill auto-discovery: `skills/<name>/SKILL.md` → installed as `shape-<name>` - Slash-command wrappers: `.claude/commands/<name>.md` thin files that `@`-import a SKILL.md or HOOK.md; plugin-registered under both bare and `shape:`-namespaced names (the source of triple-registration) - `install.sh` dual install path (vs `.claude-plugin/plugin.json` marketplace path): generates wrappers into `~/.claude/commands/shape/`, symlinks skills to `~/.claude/skills/shape-<name>`, installs SessionStart hook - ADR (Architecture Decision Record) […]