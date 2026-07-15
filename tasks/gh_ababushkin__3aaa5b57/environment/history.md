> DEVELOPER

i'm seeing lots of duplicate skills related to the shape pack, is it a caching issue?

> AGENT

Not a caching issue — it's real duplication from how the same skill is registered under multiple names. Let me confirm against the actual files.

> AGENT

No, it's not caching. It's real, structural duplication — every shape workflow is registered up to **three times** under different names because it exists as both a *skill* and a *command wrapper*, and plugin commands get double-registered. Here's the breakdown: **Three name families, same 16 workflows:** | Family | Example | Source | Count | |--------|---------|--------|-------| | `shape-<name>` | `shape-delivery`, `shape-exec-build` | Plugin **skills** auto-discovered from `skills/<name>/SKILL.md`, prefixed by plugin name `shape` | 16 | | `<name>` (bare) | `delivery`, `exec:build` | **Command wrappers** in `.claude/commands/*.md` | 16 | | `shape:<name>` | `shape:delivery`, `shape:exec:build` | Same command wrappers, **plugin-namespaced** copy | 16 | So one workflow like delivery shows up as `shape-delivery` (the skill), `delivery` (bare command), and `shape:delivery` (namespaced command) — ~48 shape entries total for 16 actual workflows. **Why it exists:** The `.claude/commands/*.md` files are thin wrappers that just `@import` the matching `SKILL.md` and invoke it — they were added to give slash-command UX (`/delivery`) on top of the auto-discovered skills. Claude Code then registers each plugin command under both its bare name and the `shape:`-prefixed name, which is the doubling you see on top of the skills. ``` .claude/commands/delivery.md → @../../skills/delivery/SKILL.md (wrapper) skills/delivery/SKILL.md → the actual skill […]