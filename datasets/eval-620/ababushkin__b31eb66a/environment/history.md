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