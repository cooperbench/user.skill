---
name: at-file-kickoff
description: vaayne opens sessions by tagging one or more files/dirs with @ before stating the task, with no other preamble
---

vaayne uses `@path` syntax (Claude Code's file-reference shorthand) at the start of opening prompts to anchor the task to specific files or directories. They do not say "look at X" or "in the file Y" — they just prefix with `@`.

**Verbatim opening examples:**

Single file + terse task:
> `@mise.toml we need migrate to all skill base, only need to sync skills expect pi extensions`

Two files + task:
> `@memory/database.go @db/ current hardcode migration in code, it's better use altas generate migration and use altas to migration instead of hard code migrate in code. explore and make a plan`

Skill dir + detailed improvement spec:
> `@skills/pi-delegate/ I want to improve the skill, not hardcode the mode but add guide that which model is good model and which is fast model, then agent can run \`pi --list-models [search]\` to list all models.`

File + URL + task (with typo "Iwant"):
> `@cli-is-all-agents-need.md https://github.com/epiral/agent-clip Iwant to explore how this will help anna`

Handoff file reference:
> `read handoff.md and continue. @internal/skills/tool.go for skill, it should not have dependency of \`github.com/vaayne/anna/internal/ai\`.`

Mid-session vaayne also uses `@` to refer to files they want checked:
> `@mise.toml check if tasks need updated`
