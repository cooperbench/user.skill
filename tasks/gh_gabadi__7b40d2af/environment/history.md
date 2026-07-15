> DEVELOPER

What do we have open/pending in .agents/backlog.md ?

> TOOL

tool_use Read
id: toolu_01MKsdzsLq8jSe6YTG76SSpd
```json
{
  "file_path": "/Users/gabadi/workspace/addi/crap4py/.agents/backlog.md"
}
```

> TOOL

tool_result
id: toolu_01MKsdzsLq8jSe6YTG76SSpd
```
1	# Enforcement-Gate Backlog
2	
3	Append-only proposals for mechanical gates, config guards, or CI checks.
4	
5	Format: `<date> | <source> | <failure-class> | <roles-affected> | <status> | <description>`
6	
7	--- 
8	
9	## Entries
10	
11	2026-06-22 | swarmforge-pattern | tool-error | architect,cleaner | wontfix | 1Password GPG signing fails silently in agent worktrees — add --no-gpg-sign to all commit invocations in agent role prompts or local-engineering constitution; affects at least architect and cleaner
12	2026-06-22 | swarmforge-pattern | tool-error | curator,specifier,cleaner | applied | `entire session current` returns wrong/stale session across 3 roles — agent-retro must verify returned worktree_path matches $PWD before trusting; add sanity-check to SKILL.md
13	2026-06-22 | swarmforge-pattern | convention-gap | coder,hardender | wontfix | f-string escaping confusion when generating code that contains f-strings — document two-level escaping rule in APS generation guidance; affects acceptance generator authoring by both roles
14	2026-06-22 | swarmforge-pattern | tool-error | specifier,integrator | pending | Auto-mode classifier blocks in-role autonomous actions (git reset --hard, gh pr merge) when no explicit per-invocation user direction — both roles blocked in same pipeline run; consider permission pre-authorization or role prompt phrasing adjustment
15	2026-06-22 | swarmforge-pattern […]

> AGENT

Open/pending items in `.agents/backlog.md` (5 of 7 entries are `pending`):

| Date | Failure | Roles | Description |
|------|---------|-------|-------------|
| 06-22 | tool-error | specifier, integrator | Auto-mode classifier blocks in-role autonomous actions (`git reset --hard`, `gh pr merge`) without per-invocation direction — consider permission pre-authorization or prompt phrasing |
| 06-22 | convention-gap | architect, hardender, ux-engineer, QA | 4 roles used 7-char git hash instead of required 10-char — add `git rev-parse --short=10 HEAD` to handoff template/constitution |
| 06-22 | convention-gap | cleaner, QA | CRAP bootstrap invocation unclear: `python -m crap4py` should be `uv run python -m crap4py`; note rtk prefix breaks it |
| 06-22 | tool-error | cleaner, hardender, architect | mutmut targeted/incremental run semantics misunderstood — no scan/count mode; targeted reruns reset cache; always analyze ALL survivors upfront |

The other two are closed: one `applied` (stale `entire session current`) and two `wontfix` (GPG signing, f-string escaping).