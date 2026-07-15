> AGENT

The CLAUDE.md is already very detailed. Let me ask a few targeted questions about gaps the code can't answer.

> AGENT

Now I'll make the changes. Let me read the end of CLAUDE.md to find the best insertion point.

> AGENT

Now I'll add the two sections and create the `/verify` skill in parallel.

> AGENT

Now create the `/verify` skill:

> AGENT

Done. Now Phase 7 — checking for additional optimizations.

> AGENT

## Summary

**Files written:**

**`CLAUDE.md`** — two sections added:
- `## Deployment` — GitHub Actions CI/CD + ktool migration timing note
- `## Workflow Skills` — table of all available skills with when-to-use descriptions

**`.claude/skills/verify/SKILL.md`** — new `/verify` skill: runs `code-quality-check` → unit tests → e2e tests in order, blocks claiming work done until all pass

**Kept as-is:**
- Pre-push hook (intentionally empty)
- Existing PostToolUse hook (`code-quality-check` on every edit)
- All 11 existing skills (unchanged)

---

**Suggested next steps:**

1. `/plugin install skill-creator@claude-plugins-official` → then `/skill-creator <name>` to refine any existing skill with evals
2. `/plugin` — browse official plugins (Playwright for browser testing, etc.)
3. Consider splitting the long CLAUDE.md into `.claude/rules/` files scoped by path — e.g., `testing.md` for the test section, `migrations.md` for the database migration rules. This keeps each file focused and Claude only loads what's relevant to the current files.

> DEVELOPER

/claude-automation-recommender`

> DEVELOPER

Unknown skill: claude-automation-recommender

> DEVELOPER

do you know `/claude-automation-recommender`

> AGENT

No. It's not in the available skills list and doesn't exist as a plugin I'm aware of.

Where did you see it referenced?

> DEVELOPER

check internet

> AGENT

It's part of the official `claude-code-setup` plugin. Install it with:

```
/plugin install claude-code-setup@claude-plugins-official
```

Then invoke with `/claude-automation-recommender` (or prompts like "recommend automations for this project"). It analyzes your codebase and suggests hooks, skills, MCP servers, and subagents tailored to your stack — read-only, no file changes.

Sources:
- [SKILL.md on GitHub](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-code-setup/skills/claude-automation-recommender/SKILL.md)
- [Claude Code Setup Plugin](https://claude.com/plugins/claude-code-setup)

> DEVELOPER

Unknown skill: claude-automation-recommender

> AGENT

No response requested.
