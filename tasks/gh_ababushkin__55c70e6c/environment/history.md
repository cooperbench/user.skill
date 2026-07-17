> DEVELOPER

i'm seeing lots of duplicate skills related to the shape pack, is it a caching issue?

> AGENT

Not a caching issue — it's real duplication from how the same skill is registered under multiple names. Let me confirm against the actual files.

> TOOL

tool_use Bash
id: toolu_01Bap5yG3mPKySJZfVpX2aiD
```json
{
  "command": "echo \"=== skills/ ===\" && ls skills/ && echo \"\" && echo \"=== .claude/commands/ ===\" && ls -R .claude/commands/ 2>/dev/null && echo \"\" && echo \"=== plugin.json ===\" && cat .claude-plugin/plugin.json",
  "description": "List skills, commands, and plugin manifest"
}
```

> TOOL

tool_result
id: toolu_01Bap5yG3mPKySJZfVpX2aiD
```
=== skills/ ===
delivery/
design/
exec-build/
exec-debug/
exec-finish/
exec-pickup/
exec-review/
exec-simplify/
exec-verify/
idea/
plan-review/
pr-prepare/
project/
render-html/
using-this-pack/
writing-refinement/

=== .claude/commands/ ===
exec/
delivery.md  359B
design.md  366B
idea.md  281B
plan-review.md  370B
pr-prepare.md  345B
project.md  289B
render-html.md  290B
stop-the-line.md  319B
ta[REDACTED_SK].md  400B
build.md  323B
debug.md  256B
finish.md  305B
pickup.md  318B
review.md  418B
simplify.md  283B
verify.md  327B

=== plugin.json ===
{
  "name": "shape",
  "description": "Workflow skills for the full product-engineering arc: idea intake and shaping, pre-build design (design-doc, product-spike, and backend-spike tracks), delivery planning, execution end-to-end. Utilities: plan review, implementation verification, PR preparation.",
  "version": "0.2.0",
  "author": {
    "name": "Anton Babushkin"
  },
  "homepage": "https://github.com/ababushkin/agent-skills-shaper",
  "repository": "https://github.com/ababushkin/agent-skills-shaper",
  "license": "MIT",
  "commands": "./.claude/commands",
  "hooks": "./hooks/hooks.json"
}
```

> TOOL

tool_use Bash
id: toolu_01Lx6vk4LDNeyaTG3QVBXjuU
```json
{
  "command": "echo \"=== skills/delivery/SKILL.md frontmatter ===\" && head -5 skills/delivery/SKILL.md && echo \"\" && echo \"=== .claude/commands/delivery.md ===\" && cat .claude/commands/delivery.md && echo \"\" && echo \"=== .claude/commands/exec/build.md ===\" && cat .claude/commands/exec/build.md",
  "description": "Inspect skill and command file contents"
}
```

> TOOL

tool_result
id: toolu_01Lx6vk4LDNeyaTG3QVBXjuU
```
=== skills/delivery/SKILL.md frontmatter ===
---
name: delivery
[281 more lines]
=== .claude/commands/delivery.md ===
---
description: "Run shape:delivery — decomposes committed work into an ordered, verifiable delivery hierarchy (deliverables → nodes → tasks) a human reads top-down and a reader walks into a tracker manifest."
argument-hint: "[initiative or goal + key results]"
---

@../../skills/delivery/SKILL.md

Run the delivery skill on the following: $ARGUMENTS

=== .claude/commands/exec/build.md ===
---
description: Run exec:build — gated RED/GREEN/commit loop for a single broken-down task. Every increment lands verified, smallest first, with a commit trail a reviewer can replay.
argument-hint: "[task description or path to task list]"
---

@../../../skills/exec-build/SKILL.md

Run the exec:build skill. $ARGUMENTS
```

> AGENT

No, it's not caching. It's real, structural duplication — every shape workflow is registered up to **three times** under different names because it exists as both a *skill* and a *command wrapper*, and plugin commands get double-registered. Here's the breakdown:

**Three name families, same 16 workflows:**

| Family | Example | Source | Count |
|--------|---------|--------|-------|
| `shape-<name>` | `shape-delivery`, `shape-exec-build` | Plugin **skills** auto-discovered from `skills/<name>/SKILL.md`, prefixed by plugin name `shape` | 16 |
| `<name>` (bare) | `delivery`, `exec:build` | **Command wrappers** in `.claude/commands/*.md` | 16 |
| `shape:<name>` | `shape:delivery`, `shape:exec:build` | Same command wrappers, **plugin-namespaced** copy | 16 |

So one workflow like delivery shows up as `shape-delivery` (the skill), `delivery` (bare command), and `shape:delivery` (namespaced command) — ~48 shape entries total for 16 actual workflows.

**Why it exists:** The `.claude/commands/*.md` files are thin wrappers that just `@import` the matching `SKILL.md` and invoke it — they were added to give slash-command UX (`/delivery`) on top of the auto-discovered skills. Claude Code then registers each plugin command under both its bare name and the `shape:`-prefixed name, which is the doubling you see on top of the skills.

```
.claude/commands/delivery.md  →  @../../skills/delivery/SKILL.md   (wrapper)
skills/delivery/SKILL.md       →  the actual skill […]

> DEVELOPER

option 1

> TOOL

tool_use Bash
id: toolu_01UsbLid59ChkKXnt12BJZ3x
```json
{
  "command": "echo \"=== stop-the-line.md ===\" && cat .claude/commands/stop-the-line.md && echo \"\" && echo \"=== ta[REDACTED_SK].md ===\" && cat .claude/commands/ta[REDACTED_SK].md && echo \"\" && echo \"=== grep refs to .claude/commands ===\" && grep -rn \"\\.claude/commands\" --include=\"*.md\" . | grep -v \"^\\./\\.claude/commands/\"",
  "description": "Inspect hook-pointing commands and find references"
}
```

> TOOL

tool_result
id: toolu_01UsbLid59ChkKXnt12BJZ3x
```
=== stop-the-line.md ===
---
description: Run stop-the-line — scans a diff for type suppressions, compiler directives, test skips, deleted assertions, and static-analysis suppressions.
argument-hint: "[diff or description]"
---

@../../hooks/stop-the-line/HOOK.md

Run the stop-the-line check on the current diff or the following: $ARGUMENTS

=== ta[REDACTED_SK].md ===
---
description: Run ta[REDACTED_SK] — counts task headers vs valid Model: routing lines in docs/tasks/*.md and flags any task block missing its model-tier annotation.
argument-hint: "[task list path, or blank for committed docs/tasks/*.md]"
---

@../../hooks/ta[REDACTED_SK]/HOOK.md

Run the ta[REDACTED_SK] on the committed `docs/tasks/*.md` files, or the following: $ARGUMENTS

=== grep refs to .claude/commands ===
./docs/adr/0005-shaping-door-leaf-names.md:24:| `shape:idea` | `skills/idea/` | `.claude/commands/idea.md` | `~/.claude/skills/shape-idea` |
./docs/adr/0005-shaping-door-leaf-names.md:25:| `shape:project` | `skills/project/` | `.claude/commands/project.md` | `~/.claude/skills/shape-project` |
./docs/adr/0005-shaping-door-leaf-names.md:26:| `shape:design` | `skills/design/` | `.claude/commands/design.md` | `~/.claude/skills/shape-design` |
./docs/adr/0005-shaping-door-leaf-names.md:27:| `shape:delivery` | `skills/delivery/` | `.claude/commands/delivery.md` | `~/.claude/skills/shape-delivery` |
./CONTRIBUTING.md:87:1. Slash commands in `~/.claude/commands/shape/`
./.worktrees/ABA-374/docs/adr/0005-shaping-door-leaf-names.md:24:| `shape:idea` | `skills/idea/` | `.claude/commands/idea.md` | `~/.claude/skills/shape-idea` |
./.worktrees/ABA-374/docs/adr/0005-shaping-door-leaf-names.md:25:| `shape:project` | `skills/project/` | `.claude/commands/project.md` | `~/.claude/skills/shape-project` |
./.worktrees/ABA-374/docs/adr/0005-shaping-door-leaf-names.md:26:| `shape:design` | `skills/design/` | `.claude/commands/design.md` | `~/.claude/skills/shape-design` |
./.worktrees/ABA-374/docs/adr/0005-shaping-door-leaf-names.md:27:| `shape:delivery` | `skills/delivery/` | `.claude/commands/delivery.md` | `~/.claude/skills/shape-delivery` |
./.worktrees/ABA-374/CONTRIBUTING.md:87:1. Slash commands in `~/.claude/commands/shape/`
./.worktrees/ABA-374/CLAUDE.md:17:- Version-control all command/skill files in the repo (not `~/.claude/commands/`)
./.worktrees/ABA-374/CLAUDE.md:33:.claude/commands/   Slash-command wrappers
./.worktrees/ABA-406/docs/adr/0005-shaping-door-leaf-names.md:24:| `shape:idea` | `skills/idea/` […]

> AGENT

Good. One important nuance before I start deleting: two of those command files — `stop-the-line.md` and `ta[REDACTED_SK].md` — point at **hooks**, not skills, so they aren't duplicates of anything. They're the only manual entry point for those two hooks. Let me check the docs that reference the commands before I decide how much to remove.

> TOOL

tool_use Bash
id: toolu_01Y3NfURg8HpX7mwcCoF3jWU
```json
{
  "command": "echo \"=== CONTRIBUTING.md 75-100 ===\" && sed -n '75,100p' CONTRIBUTING.md && echo \"\" && echo \"=== ADR 0005 head ===\" && sed -n '1,40p' docs/adr/0005-shaping-door-leaf-names.md && echo \"\" && echo \"=== hooks.json ===\" && cat hooks/hooks.json 2>/dev/null",
  "description": "Inspect CONTRIBUTING, ADR 0005, hooks.json"
}
```

> TOOL

tool_result
id: toolu_01Y3NfURg8HpX7mwcCoF3jWU
```
=== CONTRIBUTING.md 75-100 ===
## Local development setup

To work on this pack with the symlinks pointing at your clone (so edits propagate without re-running the install):

```bash
git clone https://github.com/ababushkin/agent-skills-shaper.git
cd agent-skills-shaper
./install.sh
```

This wires up:

1. Slash commands in `~/.claude/commands/shape/`
2. Auto-invocable skill symlinks in `~/.claude/skills/shape-<name>`
3. `@`-refs to the rule files in `~/.claude/CLAUDE.md`

Re-run `./install.sh` after a `git pull` or after adding a new skill — it's idempotent and prunes stale symlinks.

---

## Commits and PRs

- Conventional-commit-ish prefixes: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`.
- Subject line ≤ 70 chars. Details in the body.
- One artefact per PR is the strong default. A PR that adds a skill, a hook, and three references is harder to review than three PRs.
- The PR description should name: which problem the artefact solves, which principle(s) it implements, which existing artefact it might overlap with (if any), and how you'd verify it works in practice.

=== ADR 0005 head ===
# ADR 0005 — Shaping door leaf names (`shape:idea` / `shape:project` / `shape:design` / `shape:delivery`)

- **Status:** Accepted
- **Date:** 2026-06-12
- **Serves:** Initiative B / KR1 — the shaping library consolidates to […]

> AGENT

There's an `install.sh` that generates wrappers/symlinks and an ADR that bakes in the wrapper convention — this is more wired-in than a simple folder delete. Let me read `install.sh` before touching anything.

> TOOL

tool_use Bash
id: toolu_01CzhWadPUw8AJf3S2stkAGK
```json
{
  "command": "cat install.sh",
  "description": "Read install.sh"
}
```

> TOOL

tool_result
id: toolu_01CzhWadPUw8AJf3S2stkAGK
```
#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="${HOME}/.claude"
COMMANDS_DIR="${CLAUDE_DIR}/commands"
CLAUDE_MD="${CLAUDE_DIR}/CLAUDE.md"

# Portable in-place sed: GNU sed wants `-i` with no arg, BSD/macOS sed wants
# `-i ''`. Detect once (GNU sed answers --version; BSD sed errors) and route
# accordingly so this script runs on both Linux and macOS.
if sed --version >/dev/null 2>&1; then
  sedi() { sed -i "$@"; }
else
  sedi() { sed -i '' "$@"; }
fi

echo "Installing Shaper from ${REPO_DIR}"

# 1. Generate wrapper command files in ~/.claude/commands/shape/
#    A directory symlink breaks @include resolution: Claude Code resolves @../../ against
#    the virtual path through the symlink (~/.claude/commands/shape/../../ = ~/.claude/),
#    not the real path. Generated wrappers use absolute @paths instead.
mkdir -p "${COMMANDS_DIR}"

if [ -L "${COMMANDS_DIR}/shape" ]; then
  echo "Removing existing symlink: ${COMMANDS_DIR}/shape"
  rm "${COMMANDS_DIR}/shape"
elif [ -d "${COMMANDS_DIR}/shape" ]; then
  echo "Refreshing: ${COMMANDS_DIR}/shape"
  rm -rf "${COMMANDS_DIR}/shape"
fi

mkdir -p "${COMMANDS_DIR}/shape"

# Process top-level and subdirectory command files
for src in "${REPO_DIR}/.claude/commands/"*.md "${REPO_DIR}/.claude/commands"/*/*.md; do
  [ -f "$src" ] || continue
  relpath="${src#${REPO_DIR}/.claude/commands/}"
  dest="${COMMANDS_DIR}/shape/${relpath}"
  mkdir -p "$(dirname "$dest")"
  sed "s|@../../../|@${REPO_DIR}/|g; s|@../../|@${REPO_DIR}/|g" "$src" > "$dest"
  echo "Generated: ${dest}"
done

# 2. Prune stale rule-file @-refs from ~/.claude/CLAUDE.md.
#    Rule […]

> AGENT

Reading `install.sh` changes the picture — option 1 is bigger than just deleting a folder. The command wrappers are a **deliberate second install surface**, and they're generated/published by `install.sh`, declared in `plugin.json`, and locked in by an Accepted ADR. Full blast radius:

- **`.claude/commands/*.md`** (16 files) — delete the wrappers
- **`install.sh`** — remove step 1 (wrapper generation into `~/.claude/commands/shape/`) and the "Available commands" help block
- **`plugin.json`** — drop the `"commands"` key
- **`CLAUDE.md`, `CONTRIBUTING.md`** — remove the wrapper/`~/.claude/commands/shape/` references
- **ADR 0005** — its decision table binds the wrapper convention; this change partially reverses it

Two things genuinely need your call before I touch anything:

> TOOL

tool_use AskUserQuestion
id: toolu_01Cz28ZFq3p6ADJZ3usaSGqk
```json
{
  "questions": [
    {
      "question": "stop-the-line and ta[REDACTED_SK] are command wrappers pointing at HOOKS, not skills — and they're NOT wired into hooks.json, so the wrapper is their only manual trigger. They aren't duplicates of any skill. Remove them too, or keep them?",
      "header": "Hook commands",
      "multiSelect": false,
      "options": [
        {
          "label": "Keep these two",
          "description": "Delete the 14 skill-duplicating wrappers, keep stop-the-line + ta[REDACTED_SK] as the sole manual entry for those hooks. Removes all real duplicates; leaves 4 legit non-duplicate entries."
        },
        {
          "label": "Remove everything",
          "description": "Delete all 16 wrappers and the whole .claude/commands/ surface. The two hooks lose their only manual invocation (they'd run only if added to hooks.json)."
        }
      ]
    },
    {
      "question": "This change reverses part of Accepted ADR 0005 (and the wrapper half of ADR 0004's prefix split). How should the decision record be handled?",
      "header": "ADR handling",
      "multiSelect": false,
      "options": [
        {
          "label": "Write superseding ADR",
          "description": "Author a new ADR recording the drop of the shape: command-wrapper surface and marking the relevant parts of 0004/0005 superseded. Matches this repo's ADR discipline."
        },
        {
          "label": "Just edit, note in commit",
          "description": "Make the change and explain it in […]

> TOOL

tool_result
id: toolu_01Cz28ZFq3p6ADJZ3usaSGqk
```
Your questions have been answered: "stop-the-line and ta[REDACTED_SK] are command wrappers pointing at HOOKS, not skills — and they're NOT wired into hooks.json, so the wrapper is their only manual trigger. They aren't duplicates of any skill. Remove them too, or keep them?"="Keep these two", "This change reverses part of Accepted ADR 0005 (and the wrapper half of ADR 0004's prefix split). How should the decision record be handled?"="Write superseding ADR". You can now continue with these answers in mind.
```

> AGENT

Both calls made. Plan: delete the 14 skill-duplicating wrappers, keep the 2 hook wrappers, update `install.sh`/docs, and write a superseding ADR. Let me set up a branch and gather the files I need to edit.

> TOOL

tool_use Bash
id: toolu_013nykBigxJLc2fqQvDXx4DB
```json
{
  "command": "git checkout -b chore/drop-command-wrapper-surface 2>&1 | head -2 && echo \"---ADR dir---\" && ls docs/adr/ && echo \"---CLAUDE.md---\" && cat -n CLAUDE.md | sed -n '14,40p'",
  "description": "Create branch, list ADRs, show CLAUDE.md structure"
}
```

> TOOL

tool_result
id: toolu_013nykBigxJLc2fqQvDXx4DB
```
Switched to a new branch 'chore/drop-command-wrapper-surface'
---ADR dir---
0001-delivery-shape-new-skill-vs-expand-planning-and-task-breakdown.md  7.6K
0002-delivery-shape-accepts-ideas-goal-optional.md  3.4K
0003-persona-contract-and-dispatch-protocol.md  4.7K
0004-execution-verb-namespace.md  3.7K
0005-shaping-door-leaf-names.md  3.7K
---CLAUDE.md---
14 │ 
15 │ ## Skill Development
16 │ 
17 │ - Version-control all command/skill files in the repo (not `~/.claude/commands/`)
18 │ - Always include proper frontmatter on new skill files on first pass
19 │ 
20 │ ---
21 │ 
22 │ ## Repo structure
23 │ 
24 │ ```
25 │ skills/             Flat layout — one dir per skill, each with SKILL.md
26 │                     (matches Claude Code plugin auto-discovery convention)
27 │ rules/              Persistently-loaded rule files (PRODUCT_RULES.md, eng-principles-*.md)
28 │ hooks/
29 │   stop-the-line/    HOOK.md
30 │ references/         Standalone reference files cited by skills
31 │ docs/               Anatomy specs and authoring guidance (skill-anatomy.md, hook-anatomy.md, …)
32 │ .claude-plugin/     plugin.json — manifest for marketplace install
33 │ .claude/commands/   Slash-command wrappers
34 │ ```
35 │ 
36 │ Skills live at `skills/<name>/SKILL.md`. Hooks at `hooks/<name>/HOOK.md`. References at `references/<name>.md`. Rule files (`PRODUCT_RULES.md`, `eng-principles-*.md`) live at `rules/<name>.md`.
37 │ 
38 │ The flat skills layout matches the convention used by every other Claude Code plugin (verified across `addyosmani/agent-skills`, `claude-plugins-official/skill-creator`, etc.) — the plugin loader scans `<plugin_root>/skills/<name>/SKILL.md` and does […]

> AGENT

Now let me read ADR 0004 (the prefix split this partially reverses) so the superseding ADR cites it correctly.

> TOOL

tool_use Bash
id: toolu_01Hh3TeGYn7x63vfnbEaAPWU
```json
{
  "command": "cat docs/adr/0004-execution-verb-namespace.md",
  "description": "Read ADR 0004"
}
```

> TOOL

tool_result
id: toolu_01Hh3TeGYn7x63vfnbEaAPWU
```
# ADR 0004 — Execution verb namespace (`exec:*`)

- **Status:** Accepted
- **Date:** 2026-06-10
- **Serves:** Initiative D2 / KR1 — drained issues reach Done with a merged PR and full review trail (N04–N08).
- **Premise for:** Initiative B (verb consolidation consumes this namespace table) and Initiative C (the drain-cycle supervisor binds the front-door verb literally).
- **Record of:** the namespace decision in `docs/design-docs/execution-workflow/design-doc.md` (N04). The design doc carries the full alternatives analysis and skill graph; this ADR is the durable decision downstream skills bind to.

## Context

D2 authors five execution-side skills (front door, build, debug/simplify, review fan-out, verify, PR finishing). Each must be reachable by name from the front-door skill, and the drain-cycle supervisor in initiative C will name the front-door verb literally in `drain_cycle/prompt.py`. The verb namespace is a one-way door: once the supervisor prompt and workers' muscle memory bind, a rename costs a coordinated migration across every drainer.

Shaping verbs (`shape:*`) are already established. The execution half was unnamed. Four candidates were weighed in the N04 design doc:

1. **Bare verbs** (`/pickup`, `/build`, `/review`) — rejected: `/review` collides with installed packs (`code-review`, `crit`, built-in `review`); no slash-command grouping.
2. **`exec:*` prefix** — […]

> AGENT

Now I have the full context. Let me delete the 14 wrappers and scan for any other references to the dropped slash-command surface (README, using-this-pack, supervisor prompts).

> TOOL

tool_use Bash
id: toolu_0163epm9r5j8w5JNLeWm48Ru
```json
{
  "command": "cd /home/<USER>/src/agent-skills-shaper\ngit rm .claude/commands/delivery.md .claude/commands/design.md .claude/commands/idea.md .claude/commands/plan-review.md .claude/commands/pr-prepare.md .claude/commands/project.md .claude/commands/render-html.md .claude/commands/exec/build.md .claude/commands/exec/debug.md .claude/commands/exec/finish.md .claude/commands/exec/pickup.md .claude/commands/exec/review.md .claude/commands/exec/simplify.md .claude/commands/exec/verify.md 2>&1 | tail -3\necho \"--- remaining commands ---\"\nls -R .claude/commands/\necho \"--- refs to dropped slash verbs (non-worktree) ---\"\ngrep -rEn \"/(shape|exec):(idea|project|design|delivery|plan-review|pr-prepare|render-html|pickup|build|debug|finish|review|simplify|verify)\" --include=\"*.md\" . | grep -v \"/.worktrees/\" | grep -v \"/docs/adr/\" | head -40",
  "description": "Delete wrappers, list remainder, scan for references"
}
```

> TOOL

tool_result
id: toolu_0163epm9r5j8w5JNLeWm48Ru
```
rm '.claude/commands/pr-prepare.md'
rm '.claude/commands/project.md'
rm '.claude/commands/render-html.md'
--- remaining commands ---
stop-the-line.md
ta[REDACTED_SK].md
--- refs to dropped slash verbs (non-worktree) ---
README.md:52:- **Slash commands** for the core skills, namespaced `/shape:` (e.g. `/shape:idea`, `/shape:design`).
README.md:63:1. **An idea arrives.** *"A customer asked for bulk export."* → `/shape:idea` scores it, classifies it, and routes it — to the idea bank if it's strong, to a design spike if the bet is unproven.
README.md:64:2. **It's worth doing.** → `/shape:project` turns it into a committed project with a well defined goal and clear measures of success that an agent can self-grade. Will automatically re-route to creating an individual task if a project is unnecessary.
README.md:65:3. **Time to design.** → `/shape:design` lays out the approach, the trade-offs, and the operability plan on the design-doc track. Unsure about a risky unknown first? The product-spike or backend-spike tracks answer the one question before you commit.
README.md:66:4. **Plan the build.** → `/shape:delivery` decomposes the initiative into an ordered, verifiable task list. `/plan-review` reads it adversarially and catches what's missing *before* a line of code is written.
README.md:67:5. **Build it.** → `/exec:build` runs a gated red/green/commit loop, one small increment at a time. Stuck? `/exec:debug` finds the […]

> AGENT

The wrapper deletion is done (only the two hook commands remain). But the dropped slash-command surface is referenced across README, `references/`, `rules/`, and two skills — those become stale. Let me see the README section so I can reframe it accurately.

> TOOL

tool_use Bash
id: toolu_011oLxryx6wRFNDWWheUF2Mp
```json
{
  "command": "cat -n README.md | sed -n '44,72p'",
  "description": "Show README how-it-works section"
}
```

> TOOL

tool_result
id: toolu_011oLxryx6wRFNDWWheUF2Mp
```
 44 │ 
 45 │ ```
 46 │ /plugin install github@ababushkin/agent-skills-shaper
 47 │ ```
 48 │ 
 49 │ Restart Claude Code. That's it — you now have:
 50 │ 
 51 │ - **16 skills**, auto-invoked when the task matches (e.g. say *"how should we build this?"* and shape:design fires).
 52 │ - **Slash commands** for the core skills, namespaced `/shape:` (e.g. `/shape:idea`, `/shape:design`).
 53 │ - A **SessionStart hook** that loads the navigator skill so the agent always knows which step it's on.
 54 │ 
 55 │ Prefer to drive it yourself? Type the slash command. Prefer the agent to choose? Just describe what you're doing — the skills trigger on natural phrases.
 56 │ 
 57 │ ---
 58 │ 
 59 │ ## How to use it
 60 │ 
 61 │ Start anywhere in the arc and follow the chain. A typical run looks like this:
 62 │ 
 63 │ 1. **An idea arrives.** *"A customer asked for bulk export."* → `/shape:idea` scores it, classifies it, and routes it — to the idea bank if it's strong, to a design spike if the bet is unproven.
 64 │ 2. **It's worth doing.** → `/shape:project` turns it into […]

> AGENT

This touches the install/onboarding surface, so I'll fix it properly. Let me make the edits. Starting with README (the surface bullets and the walkthrough), then `install.sh`, `CLAUDE.md`, `CONTRIBUTING.md`, the prose cross-refs, and finally the ADR.

> TOOL

tool_use Edit
id: toolu_01VZrkVuCoraRMgwCunxP1NV
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/README.md",
  "old_string": "- **16 skills**, auto-invoked when the task matches (e.g. say *\"how should we build this?\"* and shape:design fires).\n- **Slash commands** for the core skills, namespaced `/shape:` (e.g. `/shape:idea`, `/shape:design`).\n- A **SessionStart hook** that loads the navigator skill so the agent always knows which step it's on.\n\nPrefer to drive it yourself? Type the slash command. Prefer the agent to choose? Just describe what you're doing — the skills trigger on natural phrases.",
  "new_string": "- **16 skills**, auto-invoked when the task matches (e.g. say *\"how should we build this?\"* and shape:design fires). Each also invokes by name when you want to drive a step yourself.\n- A **SessionStart hook** that loads the navigator skill so the agent always knows which step it's on.\n- **Two utility slash commands** — `/shape:stop-the-line` and `/shape:ta[REDACTED_SK]` — that run the diff-scan and task-annotation hooks on demand.\n\nPrefer the agent to choose? Just describe what you're doing — the skills trigger on natural phrases. Prefer to drive a step yourself? Name the skill (e.g. *\"run shape:delivery\"*)."
}
```

> TOOL

tool_result ERROR
id: toolu_01VZrkVuCoraRMgwCunxP1NV
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

> AGENT

I need to Read the files before editing. Let me read the ones I'll edit.

> TOOL

tool_use Read
id: toolu_01SskKCofvo9m6N3jXMNQiQn
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/README.md",
  "offset": 49,
  "limit": 22
}
```

> TOOL

tool_result
id: toolu_01SskKCofvo9m6N3jXMNQiQn
```
49	Restart Claude Code. That's it — you now have:
50	
51	- **16 skills**, auto-invoked when the task matches (e.g. say *"how should we build this?"* and shape:design fires).
52	- **Slash commands** for the core skills, namespaced `/shape:` (e.g. `/shape:idea`, `/shape:design`).
53	- A **SessionStart hook** that loads the navigator skill so the agent always knows which step it's on.
54	
55	Prefer to drive it yourself? Type the slash command. Prefer the agent to choose? Just describe what you're doing — the skills trigger on natural phrases.
56	
57	---
58	
59	## How to use it
60	
61	Start anywhere in the arc and follow the chain. A typical run looks like this:
62	
63	1. **An idea arrives.** *"A customer asked for bulk export."* → `/shape:idea` scores it, classifies it, and routes it — to the idea bank if it's strong, to a design spike if the bet is unproven.
64	2. **It's worth doing.** → `/shape:project` turns it into a committed project with a well defined goal and clear measures of success that an agent can self-grade. Will automatically re-route to creating an individual task if a project is unnecessary. […]

> TOOL

tool_use Edit
id: toolu_01C3uDke443CSLhazAe8TCNH
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/README.md",
  "old_string": "- **16 skills**, auto-invoked when the task matches (e.g. say *\"how should we build this?\"* and shape:design fires).\n- **Slash commands** for the core skills, namespaced `/shape:` (e.g. `/shape:idea`, `/shape:design`).\n- A **SessionStart hook** that loads the navigator skill so the agent always knows which step it's on.\n\nPrefer to drive it yourself? Type the slash command. Prefer the agent to choose? Just describe what you're doing — the skills trigger on natural phrases.",
  "new_string": "- **16 skills**, auto-invoked when the task matches (e.g. say *\"how should we build this?\"* and shape:design fires). Each also invokes by name when you want to drive a step yourself.\n- A **SessionStart hook** that loads the navigator skill so the agent always knows which step it's on.\n- **Two utility slash commands** — `/shape:stop-the-line` and `/shape:ta[REDACTED_SK]` — that run the diff-scan and task-annotation hooks on demand.\n\nPrefer the agent to choose? Just describe what you're doing — the skills trigger on natural phrases. Prefer to drive a step yourself? Name the skill (e.g. *\"run shape:delivery\"*)."
}
```

> TOOL

tool_result
id: toolu_01C3uDke443CSLhazAe8TCNH
```
The file /home/<USER>/src/agent-skills-shaper/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01PFYBJn5U1fw69uEEw6hgob
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/README.md",
  "old_string": "1. **An idea arrives.** *\"A customer asked for bulk export.\"* → `/shape:idea` scores it, classifies it, and routes it — to the idea bank if it's strong, to a design spike if the bet is unproven.\n2. **It's worth doing.** → `/shape:project` turns it into a committed project with a well defined goal and clear measures of success that an agent can self-grade. Will automatically re-route to creating an individual task if a project is unnecessary.\n3. **Time to design.** → `/shape:design` lays out the approach, the trade-offs, and the operability plan on the design-doc track. Unsure about a risky unknown first? The product-spike or backend-spike tracks answer the one question before you commit.\n4. **Plan the build.** → `/shape:delivery` decomposes the initiative into an ordered, verifiable task list. `/plan-review` reads it adversarially and catches what's missing *before* a line of code is written.\n5. **Build it.** → `/exec:build` runs a gated red/green/commit loop, one small increment at a time. Stuck? `/exec:debug` finds the root cause. Heavy? `/exec:simplify` trims it once it's green.\n6. **Prove it's done.** → `/exec:verify` checks the diff against the ticket's acceptance criteria; `/exec:review` runs spec, security, and quality passes. […]

> TOOL

tool_result
id: toolu_01PFYBJn5U1fw69uEEw6hgob
```
The file /home/<USER>/src/agent-skills-shaper/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

I used the wrong verb form for the exec steps — the canonical verbs (per ADR 0004) are `exec:build`, not `shape:exec:build`. Let me fix.

> TOOL

tool_use Edit
id: toolu_01LvmrebnY59C8JGimNQUQKd
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/README.md",
  "old_string": "5. **Build it.** → **shape:exec:build** runs a gated red/green/commit loop, one small increment at a time. Stuck? **shape:exec:debug** finds the root cause. Heavy? **shape:exec:simplify** trims it once it's green.\n6. **Prove it's done.** → **shape:exec:verify** checks the diff against the ticket's acceptance criteria; **shape:exec:review** runs spec, security, and quality passes. A fail is a halt, not a suggestion.\n7. **Ship it.** → **shape:exec:finish** submits the stack, one small PR per slice, and delegates to **shape:pr-prepare** to write each PR's reviewer body and route it for merge or human review.",
  "new_string": "5. **Build it.** → **exec:build** runs a gated red/green/commit loop, one small increment at a time. Stuck? **exec:debug** finds the root cause. Heavy? **exec:simplify** trims it once it's green.\n6. **Prove it's done.** → **exec:verify** checks the diff against the ticket's acceptance criteria; **exec:review** runs spec, security, and quality passes. A fail is a halt, not a suggestion.\n7. **Ship it.** → **exec:finish** submits the stack, one small PR per slice, and delegates to **shape:pr-prepare** to write each PR's reviewer body and route it for merge or human review."
}
```

> TOOL

tool_result
id: toolu_01LvmrebnY59C8JGimNQUQKd
```
The file /home/<USER>/src/agent-skills-shaper/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now `install.sh` — update the "Available commands" help block to list only the two remaining commands.

> TOOL

tool_use Read
id: toolu_01XkVFuJVxPzfL19YCoj1y82
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/install.sh",
  "offset": 160,
  "limit": 25
}
```

> TOOL

tool_result
id: toolu_01XkVFuJVxPzfL19YCoj1y82
```
160	
161	echo ""
162	echo "Done. Restart Claude Code to pick up changes."
163	echo ""
164	echo "Available commands:"
165	echo "  /shape:idea                         Triage an incoming idea"
166	echo "  /shape:design                       Work through a technical or product unknown before building (design doc, backend spike, or product spike)"
167	echo "  /shape:delivery                     Decompose an initiative into a delivery plan"
168	echo "  /shape:project                      Shape a vague idea into a goal-driven initiative"
169	echo "  /shape:plan-review                  Review a plan/spec/design before approval"
170	echo "  /shape:exec:pickup                  Drain a Linear issue end-to-end"
171	echo "  /shape:exec:review                  Multi-persona execution review of a diff"
172	echo "  /shape:verify-implementation        Check a diff against ticket AC before Done"
173	echo "  /shape:pr-prepare                   Write PR bodies and route the stack to merge or review"
174	echo "  /shape:render-html                  Render a markdown doc as a reviewable HTML file"
175	echo "  /shape:stop-the-line                Scan a diff for quality red flags"
176	echo "  /shape:ta[REDACTED_SK]        Check docs/tasks/*.md for model-tier annotations"
177	echo ""
178	echo "Auto-invocable skills (model-triggered, namespaced as shape-<name>):"
179	for link in "${SKILLS_DIR}"/shape-*; do
180	  [ -L "${link}" ] || continue
181	  echo "  $(basename "${link}")"
182	done
183	echo ""
184	echo […]

> TOOL

tool_use Edit
id: toolu_01XbBoJK8s61uJxfqVqkw1a2
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/install.sh",
  "old_string": "echo \"Available commands:\"\necho \"  /shape:idea                         Triage an incoming idea\"\necho \"  /shape:design                       Work through a technical or product unknown before building (design doc, backend spike, or product spike)\"\necho \"  /shape:delivery                     Decompose an initiative into a delivery plan\"\necho \"  /shape:project                      Shape a vague idea into a goal-driven initiative\"\necho \"  /shape:plan-review                  Review a plan/spec/design before approval\"\necho \"  /shape:exec:pickup                  Drain a Linear issue end-to-end\"\necho \"  /shape:exec:review                  Multi-persona execution review of a diff\"\necho \"  /shape:verify-implementation        Check a diff against ticket AC before Done\"\necho \"  /shape:pr-prepare                   Write PR bodies and route the stack to merge or review\"\necho \"  /shape:render-html                  Render a markdown doc as a reviewable HTML file\"\necho \"  /shape:stop-the-line                Scan a diff for quality red flags\"\necho \"  /shape:ta[REDACTED_SK]        Check docs/tasks/*.md for model-tier annotations\"\necho \"\"\necho \"Auto-invocable skills (model-triggered, namespaced as shape-<name>):\"",
  "new_string": "echo \"Utility slash commands (on-demand hook runs):\"\necho \"  /shape:stop-the-line                Scan a diff for quality red flags\"\necho \"  /shape:ta[REDACTED_SK]        Check docs/tasks/*.md for model-tier annotations\"\necho \"\"\necho \"Every workflow ships as an auto-invocable skill (model-triggered, or invoke by name).\"\necho \"Skills installed, namespaced as shape-<name>:\""
}
```

> TOOL

tool_result
id: toolu_01XbBoJK8s61uJxfqVqkw1a2
```
The file /home/<USER>/src/agent-skills-shaper/install.sh has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now `CLAUDE.md` — the repo-structure line and the hooks listing (stop-the-line is shown but ta[REDACTED_SK] hook isn't).

> TOOL

tool_use Edit
id: toolu_01AYsfxXqVx9RWWcY6d6P5DG
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/CLAUDE.md",
  "old_string": ".claude-plugin/     plugin.json — manifest for marketplace install\n.claude/commands/   Slash-command wrappers",
  "new_string": ".claude-plugin/     plugin.json — manifest for marketplace install\n.claude/commands/   Slash-command wrappers — utility hooks only (stop-the-line,\n                    ta[REDACTED_SK]). Workflow skills are invoked by name,\n                    not via wrappers."
}
```

> TOOL

tool_result
id: toolu_01AYsfxXqVx9RWWcY6d6P5DG
```
The file /home/<USER>/src/agent-skills-shaper/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now CONTRIBUTING.md — the local-dev "what this wires up" list.

> TOOL

tool_use Read
id: toolu_01Dvb719UjPggipiXLFP2TWJ
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/CONTRIBUTING.md",
  "offset": 85,
  "limit": 8
}
```

> TOOL

tool_result
id: toolu_01Dvb719UjPggipiXLFP2TWJ
```
85	This wires up:
86	
87	1. Slash commands in `~/.claude/commands/shape/`
88	2. Auto-invocable skill symlinks in `~/.claude/skills/shape-<name>`
89	3. `@`-refs to the rule files in `~/.claude/CLAUDE.md`
90	
91	Re-run `./install.sh` after a `git pull` or after adding a new skill — it's idempotent and prunes stale symlinks.
92	
```

> TOOL

tool_use Edit
id: toolu_017RskJKQS148roCqR7ZDiwK
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/CONTRIBUTING.md",
  "old_string": "1. Slash commands in `~/.claude/commands/shape/`\n2. Auto-invocable skill symlinks in `~/.claude/skills/shape-<name>`\n3. `@`-refs to the rule files in `~/.claude/CLAUDE.md`",
  "new_string": "1. Auto-invocable skill symlinks in `~/.claude/skills/shape-<name>` — the primary invocation surface for every workflow\n2. Utility slash commands in `~/.claude/commands/shape/` — only the two hook runners (`stop-the-line`, `ta[REDACTED_SK]`)\n3. `@`-refs to the rule files in `~/.claude/CLAUDE.md`"
}
```

> TOOL

tool_result
id: toolu_017RskJKQS148roCqR7ZDiwK
```
The file /home/<USER>/src/agent-skills-shaper/CONTRIBUTING.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now the prose cross-refs that still say you can type `/shape:X`. Let me read and fix them.

> TOOL

tool_use Bash
id: toolu_011mqd3m91eWBg5mDoheyJSK
```json
{
  "command": "cd /home/<USER>/src/agent-skills-shaper\necho \"=== design:28 ===\" && sed -n '28p' skills/design/SKILL.md\necho \"=== plan-review:38 ===\" && sed -n '38p' skills/plan-review/SKILL.md\necho \"=== PRODUCT_RULES:3 ===\" && sed -n '3p' rules/PRODUCT_RULES.md\necho \"=== project-types 5,15,21,39,362,363 ===\" && sed -n '5p;15p;21p;39p;362p;363p' references/project-types.md",
  "description": "Read exact cross-ref lines"
}
```

> TOOL

tool_result
id: toolu_011mqd3m91eWBg5mDoheyJSK
```
=== design:28 ===
If the problem itself is not yet framed, run `/shape:idea` first. A design or spike on an undefined problem produces an answer to the wrong question.
=== plan-review:38 ===
- **The plan itself doesn't exist yet.** Use `/shape:design` or `/shape:idea` to produce a plan first.
=== PRODUCT_RULES:3 ===
These are the product principles and operational rules for the Shaper pack. They cover roadmap structure, prioritisation, commitment, and learning. The `/shape:idea` skill handles problem-framing and roadmap mechanics at the point of intake.
=== project-types 5,15,21,39,362,363 ===
  Used by /shape:project to set the Objective shape and the rubric the KRs are judged
The `/shape:project` skill probes the project type before shaping KRs. The type determines what "success" means for the initiative: a methodology skill pack and a personal product can both pass cycle close, but they pass on different KRs, because their theories of success are different. Naming the type up front lets the skill load the right Objective shape and verification rubric — and lets a downstream agent reading the Linear project description apply the right rubric without re-deriving the taxonomy.
**Worked-example convention.** Each example below uses the PM-readable KR shape `/shape:project` emits — […]

> TOOL

tool_use Read
id: toolu_014Az1PhdLLk93Aya7itBRDk
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/skills/design/SKILL.md",
  "offset": 28,
  "limit": 1
}
```

> TOOL

tool_result
id: toolu_014Az1PhdLLk93Aya7itBRDk
```
28	If the problem itself is not yet framed, run `/shape:idea` first. A design or spike on an undefined problem produces an answer to the wrong question.
```

> TOOL

tool_use Read
id: toolu_018zrnShhLkAhuAU3QAj3jon
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/skills/plan-review/SKILL.md",
  "offset": 38,
  "limit": 1
}
```

> TOOL

tool_result
id: toolu_018zrnShhLkAhuAU3QAj3jon
```
38	- **The plan itself doesn't exist yet.** Use `/shape:design` or `/shape:idea` to produce a plan first.
```

> TOOL

tool_use Read
id: toolu_01J7sCn9HjMSrrJ8yrD5ewqS
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/rules/PRODUCT_RULES.md",
  "offset": 3,
  "limit": 1
}
```

> TOOL

tool_result
id: toolu_01J7sCn9HjMSrrJ8yrD5ewqS
```
3	These are the product principles and operational rules for the Shaper pack. They cover roadmap structure, prioritisation, commitment, and learning. The `/shape:idea` skill handles problem-framing and roadmap mechanics at the point of intake.
```

> TOOL

tool_use Read
id: toolu_01SFANGjcNHAWvwABtT9gMRN
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/references/project-types.md",
  "offset": 3,
  "limit": 40
}
```

> TOOL

tool_result
id: toolu_01SFANGjcNHAWvwABtT9gMRN
```
3	description: >
4	  Six-type taxonomy for classifying a Linear initiative by what success means for it.
5	  Used by /shape:project to set the Objective shape and the rubric the KRs are judged
6	  against. Per-type playbooks (default KR mix, anti-patterns, verification rubric) are
7	  filled in below the corresponding type entry as the skill matures.
8	type: reference
9	cited_by:
10	  - skills/project/SKILL.md
11	---
12	
13	# Initiative types (6)
14	
15	The `/shape:project` skill probes the project type before shaping KRs. The type determines what "success" means for the initiative: a methodology skill pack and a personal product can both pass cycle close, but they pass on different KRs, because their theories of success are different. Naming the type up front lets the skill load the right Objective shape and verification rubric — and lets a downstream agent reading the Linear project description apply the right rubric without re-deriving the taxonomy.
16	
17	The six types below are the ones actually observed across this portfolio (`agent-skills-shaper`, `nestl`, `agent-skills`, paused `em-os`, `stock-review`) plus one anticipated type (production / customer-facing). If a new initiative doesn't fit any of the six, the taxonomy needs updating — […]

> AGENT

Now the edits:

> TOOL

tool_use Edit
id: toolu_015be3ZXgPr1CDwVdZW9VyGN
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/skills/design/SKILL.md",
  "old_string": "If the problem itself is not yet framed, run `/shape:idea` first.",
  "new_string": "If the problem itself is not yet framed, run **shape:idea** first."
}
```

> TOOL

tool_result
id: toolu_015be3ZXgPr1CDwVdZW9VyGN
```
The file /home/<USER>/src/agent-skills-shaper/skills/design/SKILL.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01MBNFFNUMZy44dLCW4osKuH
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/skills/plan-review/SKILL.md",
  "old_string": "- **The plan itself doesn't exist yet.** Use `/shape:design` or `/shape:idea` to produce a plan first.",
  "new_string": "- **The plan itself doesn't exist yet.** Use **shape:design** or **shape:idea** to produce a plan first."
}
```

> TOOL

tool_result
id: toolu_01MBNFFNUMZy44dLCW4osKuH
```
The file /home/<USER>/src/agent-skills-shaper/skills/plan-review/SKILL.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_012F4uxuwJK7hF6vqbdNs4rK
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/rules/PRODUCT_RULES.md",
  "old_string": "The `/shape:idea` skill handles problem-framing and roadmap mechanics at the point of intake.",
  "new_string": "The **shape:idea** skill handles problem-framing and roadmap mechanics at the point of intake."
}
```

> TOOL

tool_result
id: toolu_012F4uxuwJK7hF6vqbdNs4rK
```
The file /home/<USER>/src/agent-skills-shaper/rules/PRODUCT_RULES.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now `references/project-types.md` — the `/shape:project` verb refs (lines 5, 15, 21, 39) and the two buggy `skills/shape:project/` paths (362–363, which should be `skills/project/`).

> TOOL

tool_use Edit
id: toolu_01AX2Ms8kf6BxDontC9GuysL
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/references/project-types.md",
  "old_string": "  Used by /shape:project to set the Objective shape and the rubric the KRs are judged",
  "new_string": "  Used by shape:project to set the Objective shape and the rubric the KRs are judged"
}
```

> TOOL

tool_result
id: toolu_01AX2Ms8kf6BxDontC9GuysL
```
The file /home/<USER>/src/agent-skills-shaper/references/project-types.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01QR41PNfAD6dTTBZLoLk9Sg
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/references/project-types.md",
  "old_string": "The `/shape:project` skill probes the project type before shaping KRs.",
  "new_string": "The **shape:project** skill probes the project type before shaping KRs."
}
```

> TOOL

tool_result
id: toolu_01QR41PNfAD6dTTBZLoLk9Sg
```
The file /home/<USER>/src/agent-skills-shaper/references/project-types.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01RYR1RryfTXUpu3USRr3Zh9
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/references/project-types.md",
  "old_string": "Each example below uses the PM-readable KR shape `/shape:project` emits",
  "new_string": "Each example below uses the PM-readable KR shape **shape:project** emits"
}
```

> TOOL

tool_result
id: toolu_01RYR1RryfTXUpu3USRr3Zh9
```
The file /home/<USER>/src/agent-skills-shaper/references/project-types.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01JBwHyBBHp3WgeEpmhVCGTB
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/references/project-types.md",
  "old_string": "**Worked example — `/shape:project` itself.**",
  "new_string": "**Worked example — `shape:project` itself.**"
}
```

> TOOL

tool_result
id: toolu_01JBwHyBBHp3WgeEpmhVCGTB
```
The file /home/<USER>/src/agent-skills-shaper/references/project-types.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Read
id: toolu_01F8V26VAzwFp9CAB8qG8aaU
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/references/project-types.md",
  "offset": 360,
  "limit": 5
}
```

> TOOL

tool_result
id: toolu_01F8V26VAzwFp9CAB8qG8aaU
```
360	
361	- Internal research: Linear document "Research and implementation plan — OKR shapes by project type" (Section 1.1, project `Initiative quality — type-aware OKRs with KRs`)
362	- `skills/shape:project/SKILL.md` — the six-field initiative format the type field is added to (defined inline in the skill); tracker capture is owned by the Workflow pack when installed
363	- `skills/shape:project/SKILL.md` — invokes the type probe at Step 2.5
364	
```

> TOOL

tool_use Edit
id: toolu_01R7y2xJPhhwhmRsnkB141A6
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/references/project-types.md",
  "old_string": "- `skills/shape:project/SKILL.md` — the six-field initiative format the type field is added to (defined inline in the skill); tracker capture is owned by the Workflow pack when installed\n- `skills/shape:project/SKILL.md` — invokes the type probe at Step 2.5",
  "new_string": "- `skills/project/SKILL.md` — the six-field initiative format the type field is added to (defined inline in the skill); tracker capture is owned by the Workflow pack when installed\n- `skills/project/SKILL.md` — invokes the type probe at Step 2.5"
}
```

> TOOL

tool_result
id: toolu_01R7y2xJPhhwhmRsnkB141A6
```
The file /home/<USER>/src/agent-skills-shaper/references/project-types.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now the superseding ADR. Let me write ADR 0006.

> TOOL

tool_use Write
id: toolu_01RBEjSan7BDtqEWVzauT6cc
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/docs/adr/0006-drop-command-wrapper-surface.md",
  "content": "# ADR 0006 — Drop the command-wrapper surface for workflow skills\n\n- **Status:** Accepted\n- **Date:** 2026-06-18\n- **Supersedes (in part):** ADR 0004 (`exec:*` verb namespace) and ADR 0005 (shaping door leaf names) — specifically the part of each that realised the reserved verbs as generated `/shape:*` and `/exec:*` slash-command wrappers. The reserved verb *names* stand; only the wrapper *invocation surface* is withdrawn.\n- **Serves:** Pack ergonomics — one invocation surface per workflow, so the skill picker lists each workflow once instead of three times.\n\n## Context\n\nEvery workflow shipped on two installed surfaces:\n\n1. **Auto-invocable skill** — `skills/<name>/SKILL.md`, installed as `~/.claude/skills/shape-<name>`, model-triggered or invoked by name via the Skill tool.\n2. **Slash-command wrapper** — `.claude/commands/<name>.md`, a thin file that `@`-imports the same `SKILL.md` and invokes it, installed as `/shape:<name>` (and `/exec:<name>`).\n\nBecause the pack is loaded as a Claude Code plugin, each wrapper is also registered twice — once bare (`delivery`) and once plugin-namespaced (`shape:delivery`). The net effect in the skill picker: one workflow (e.g. delivery) appears three times — `shape-delivery` (the skill), `delivery` (bare command), and `shape:delivery` (namespaced command). Across 14 workflows that is ~42 entries for 14 capabilities. Operators read this as duplication or a caching fault.\n\nThe […]

> TOOL

tool_result
id: toolu_01RBEjSan7BDtqEWVzauT6cc
```
File created successfully at: /home/<USER>/src/agent-skills-shaper/docs/adr/0006-drop-command-wrapper-surface.md (file state is current in your context — no need to Read it back)
```

> AGENT

Let me add back-pointers in ADR 0004 and 0005 so the record is navigable.

> TOOL

tool_use Edit
id: toolu_012jWBQqVTGdz8KPnaDbMMWv
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/docs/adr/0004-execution-verb-namespace.md",
  "old_string": "- **Status:** Accepted\n- **Date:** 2026-06-10",
  "new_string": "- **Status:** Accepted (wrapper surface superseded in part by ADR 0006 — the `exec:*` verb names stand; they are no longer published as typed slash commands)\n- **Date:** 2026-06-10"
}
```

> TOOL

tool_result ERROR
id: toolu_012jWBQqVTGdz8KPnaDbMMWv
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

> TOOL

tool_use Edit
id: toolu_01KdfMFSMv55Q5B5tt9nkmhZ
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/docs/adr/0005-shaping-door-leaf-names.md",
  "old_string": "- **Status:** Accepted\n- **Date:** 2026-06-12",
  "new_string": "- **Status:** Accepted (wrapper surface superseded in part by ADR 0006 — the leaf names stand; the `.claude/commands/*.md` wrappers are withdrawn for core skills)\n- **Date:** 2026-06-12"
}
```

> TOOL

tool_result ERROR
id: toolu_01KdfMFSMv55Q5B5tt9nkmhZ
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

> TOOL

tool_use Read
id: toolu_01NgJg1ReyoxSiVQisi8CJ7x
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/docs/adr/0004-execution-verb-namespace.md",
  "limit": 4
}
```

> TOOL

tool_result
id: toolu_01NgJg1ReyoxSiVQisi8CJ7x
```
1	# ADR 0004 — Execution verb namespace (`exec:*`)
2	
3	- **Status:** Accepted
4	- **Date:** 2026-06-10
```

> TOOL

tool_use Read
id: toolu_019sudPNi61zJxU1wgYxKjcn
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/docs/adr/0005-shaping-door-leaf-names.md",
  "limit": 4
}
```

> TOOL

tool_result
id: toolu_019sudPNi61zJxU1wgYxKjcn
```
1	# ADR 0005 — Shaping door leaf names (`shape:idea` / `shape:project` / `shape:design` / `shape:delivery`)
2	
3	- **Status:** Accepted
4	- **Date:** 2026-06-12
```

> TOOL

tool_use Edit
id: toolu_01SNLysC4wcnwNTwhzWtf1U2
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/docs/adr/0004-execution-verb-namespace.md",
  "old_string": "- **Status:** Accepted\n- **Date:** 2026-06-10",
  "new_string": "- **Status:** Accepted (wrapper surface superseded in part by ADR 0006 — the `exec:*` verb names stand; they are no longer published as typed slash commands)\n- **Date:** 2026-06-10"
}
```

> TOOL

tool_result
id: toolu_01SNLysC4wcnwNTwhzWtf1U2
```
The file /home/<USER>/src/agent-skills-shaper/docs/adr/0004-execution-verb-namespace.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01NV7xoaLBSTcfJES3hNyDUk
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/docs/adr/0005-shaping-door-leaf-names.md",
  "old_string": "- **Status:** Accepted\n- **Date:** 2026-06-12",
  "new_string": "- **Status:** Accepted (wrapper surface superseded in part by ADR 0006 — the leaf names stand; the `.claude/commands/*.md` wrappers are withdrawn for core skills)\n- **Date:** 2026-06-12"
}
```

> TOOL

tool_result
id: toolu_01NV7xoaLBSTcfJES3hNyDUk
```
The file /home/<USER>/src/agent-skills-shaper/docs/adr/0005-shaping-door-leaf-names.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Let me sweep for any remaining stale slash-command references and sanity-check the install script still parses.

> TOOL

tool_use Bash
id: toolu_018jYayXBXYpTKG25CtesW9Z
```json
{
  "command": "cd /home/<USER>/src/agent-skills-shaper\necho \"=== remaining /shape: or /exec: refs (excl worktrees & ADRs) ===\"\ngrep -rEn \"/(shape|exec):\" --include=\"*.md\" . | grep -v \"/.worktrees/\" | grep -v \"/docs/adr/\" | grep -vE \"/shape:(stop-the-line|ta[REDACTED_SK])\" || echo \"(none)\"\necho \"\"\necho \"=== bash syntax check install.sh ===\"\nbash -n install.sh && echo \"OK\"\necho \"\"\necho \"=== git status ===\"\ngit status --short",
  "description": "Sweep stale refs, lint install.sh, show status"
}
```

> TOOL

tool_result
id: toolu_018jYayXBXYpTKG25CtesW9Z
```
=== remaining /shape: or /exec: refs (excl worktrees & ADRs) ===
README.md:73:Not sure which skill applies? Ask, or run `/shape:using-this-pack` — the navigator maps your task to the right step.
docs/adr/0006-drop-command-wrapper-surface.md:5:- **Supersedes (in part):** ADR 0004 (`exec:*` verb namespace) and ADR 0005 (shaping door leaf names) — specifically the part of each that realised the reserved verbs as generated `/shape:*` and `/exec:*` slash-command wrappers. The reserved verb *names* stand; only the wrapper *invocation surface* is withdrawn.
docs/adr/0006-drop-command-wrapper-surface.md:13:2. **Slash-command wrapper** — `.claude/commands/<name>.md`, a thin file that `@`-imports the same `SKILL.md` and invokes it, installed as `/shape:<name>` (and `/exec:<name>`).
docs/adr/0006-drop-command-wrapper-surface.md:37:- No typed `/shape:idea`-style slash command for the core workflows. Operators who preferred typing a command now name the skill ("run shape:delivery") or let it auto-trigger. Accepted — the convenience did not justify a 3× picker.
docs/adr/0004-execution-verb-namespace.md:20:**Supervisor-binding audit (performed before pinning).** A read of current `drain_cycle/prompt.py` confirmed the migration surface is bounded: the supervisor emits `/code-review-and-quality` (4 string locations) and `/shape:task` (verify-flow directive only); the rest of the completion sequence is inlined prose. Adopting `exec:*` is a bounded string swap plus an additive replacement, not a coordinated cross-drainer migration. The audit also corrected a stale assumption — `/shape:verify-implementation`, `/shape:pr-prepare`, […]

> AGENT

One live ref left — `README.md:73` points at `/shape:using-this-pack`, which never had a wrapper (it's the navigator skill). Let me fix it.

> TOOL

tool_use Read
id: toolu_01F9NRXJJjPZNxaHmUT3bUoH
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/README.md",
  "offset": 73,
  "limit": 1
}
```

> TOOL

tool_result
id: toolu_01F9NRXJJjPZNxaHmUT3bUoH
```
73	Not sure which skill applies? Ask, or run `/shape:using-this-pack` — the navigator maps your task to the right step.
```

> TOOL

tool_use Edit
id: toolu_01GWBVzhijpTWpFnDW558CeZ
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/README.md",
  "old_string": "Not sure which skill applies? Ask, or run `/shape:using-this-pack` — the navigator maps your task to the right step.",
  "new_string": "Not sure which skill applies? Ask, or invoke **shape:using-this-pack** — the navigator maps your task to the right step."
}
```

> TOOL

tool_result
id: toolu_01GWBVzhijpTWpFnDW558CeZ
```
The file /home/<USER>/src/agent-skills-shaper/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01Bsr8qn3NYGLH7J3W9uye4E
```json
{
  "command": "cd /home/<USER>/src/agent-skills-shaper\necho \"=== README 'command'/'slash' mentions ===\" && grep -niE \"slash|command\" README.md || echo \"(none)\"\necho \"\" && echo \"=== .claude/commands tree ===\" && find .claude/commands -type f -o -type d | sort\necho \"\" && echo \"=== exec dir on disk? ===\" && ls .claude/commands/exec 2>&1 || true",
  "description": "Check README mentions and commands dir state"
}
```

> TOOL

tool_result
id: toolu_01Bsr8qn3NYGLH7J3W9uye4E
```
=== README 'command'/'slash' mentions ===
53:- **Two utility slash commands** — `/shape:stop-the-line` and `/shape:ta[REDACTED_SK]` — that run the diff-scan and task-annotation hooks on demand.
147:The script writes slash-command wrappers, symlinks each skill into `~/.claude/skills/shape-<name>`, and installs the SessionStart hook. Re-run after a `git pull` — it's idempotent and prunes stale symlinks.

=== .claude/commands tree ===
.claude/commands
.claude/commands/stop-the-line.md
.claude/commands/ta[REDACTED_SK].md

=== exec dir on disk? ===
ls: .claude/commands/exec: No such file or directory
```

> AGENT

`README.md:147` describes install.sh as writing "slash-command wrappers" broadly. Let me tighten it.

> TOOL

tool_use Read
id: toolu_01T1ozGnwTe7ULHcHMBWYXeP
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/README.md",
  "offset": 145,
  "limit": 4
}
```

> TOOL

tool_result
id: toolu_01T1ozGnwTe7ULHcHMBWYXeP
```
145	```
146	
147	The script writes slash-command wrappers, symlinks each skill into `~/.claude/skills/shape-<name>`, and installs the SessionStart hook. Re-run after a `git pull` — it's idempotent and prunes stale symlinks.
148	
```

> TOOL

tool_use Edit
id: toolu_01XtSbScBvaMQkiMZbxBYK3x
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/src/agent-skills-shaper/README.md",
  "old_string": "The script writes slash-command wrappers, symlinks each skill into `~/.claude/skills/shape-<name>`, and installs the SessionStart hook. Re-run after a `git pull` — it's idempotent and prunes stale symlinks.",
  "new_string": "The script symlinks each skill into `~/.claude/skills/shape-<name>`, writes the two utility hook wrappers, and installs the SessionStart hook. Re-run after a `git pull` — it's idempotent and prunes stale symlinks."
}
```

> TOOL

tool_result
id: toolu_01XtSbScBvaMQkiMZbxBYK3x
```
The file /home/<USER>/src/agent-skills-shaper/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Let me get a final diffstat to summarize.

> TOOL

tool_use Bash
id: toolu_01PrQcGBNktprE8Q5oh1VGAY
```json
{
  "command": "git add -A && git diff --cached --stat",
  "description": "Stage all and show diffstat"
}
```

> TOOL

tool_result
id: toolu_01PrQcGBNktprE8Q5oh1VGAY
```
ok 25 files changed, 73 insertions(+), 150 deletions(-)
.claude/commands/delivery.md                  |  8 -----
 .claude/commands/design.md                    |  8 -----
 .claude/commands/exec/build.md                |  8 -----
 .claude/commands/exec/debug.md                |  8 -----
 .claude/commands/exec/finish.md               |  8 -----
 .claude/commands/exec/pickup.md               |  8 -----
 .claude/commands/exec/review.md               |  8 -----
 .claude/commands/exec/simplify.md             |  8 -----
 .claude/commands/exec/verify.md               |  8 -----
 .claude/commands/idea.md                      |  8 -----
 .claude/commands/plan-review.md               |  8 -----
 .claude/commands/pr-prepare.md                |  8 -----
 .claude/commands/project.md                   |  8 -----
 .claude/commands/render-html.md               |  8 -----
 CLAUDE.md                                     |  4 ++-
 CONTRIBUTING.md                               |  4 +--
 README.md                                     | 24 +++++++--------
 docs/adr/0004-execution-verb-namespace.md     |  2 +-
 docs/adr/0005-shaping-door-leaf-names.md      |  2 +-
 docs/adr/0006-drop-command-wrapper-surface.md | 42 +++++++++++++++++++++++++++
 install.sh                                    | 15 ++--------
 references/project-types.md                   | 12 ++++----
 rules/PRODUCT_RULES.md                        |  2 +-
 skills/design/SKILL.md                        |  2 +-
 skills/plan-review/SKILL.md                   |  2 +-
 25 files changed, 73 insertions(+), 150 deletions(-)
```

> AGENT

Done. Here's what changed and why it fixes the "duplicate skills" you saw.

## Root cause (recap)
Not caching. Each workflow shipped on **two install surfaces** — an auto-invocable skill (`shape-<name>`) *and* a slash-command wrapper that just re-imported the same `SKILL.md`. As a plugin, each wrapper was then registered twice (bare `delivery` + namespaced `shape:delivery`), so one workflow showed up three times in the picker.

## What I did (option 1)
**Deleted the 14 skill-duplicating wrappers**, keeping only the two that aren't duplicates — `stop-the-line` and `ta[REDACTED_SK]`, which point at hooks and have no backing skill (their wrapper is the only manual trigger). Each workflow now appears once, as `shape-<name>`.

Beyond the deletes, the wrapper surface was wired into several places, so I updated all of them:

- **`install.sh`** — the "Available commands" help block now lists only the two utility commands; still generates wrappers, just for those two.
- **`plugin.json`** — unchanged (the `commands` key is still valid for the two remaining wrappers).
- **`README.md`** — rewrote the install bullets and the 7-step walkthrough to present workflows as skills (`shape:idea`, `exec:build`, …) invoked by name/auto-trigger, not typed `/`-commands; fixed `/shape:using-this-pack` (never a real command) and the install-script description.
- […]