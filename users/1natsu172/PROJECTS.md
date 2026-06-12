---
# 1natsu172 — Projects
---

## `1natsu-vacation/agent-skills` ★ DOMINANT (100% of sessions)

### What It Is

A personal repository of reusable Claude Code skills — built, tested, and versioned by 1natsu172 using a TDD methodology applied to SKILL.md documentation. The repo uses `bunx skills add . -g -y` for global installation and `bunx skills add . --list` for verification.

### Skills in the Repo (as of late sessions)

| Skill | Purpose |
|-------|---------|
| `1natsu-commit` | Git commit best practices + Conventional Commits |
| `1natsu-conventional-commits` | Standalone Conventional Commits reference (split out from commit/create-pr) |
| `1natsu-create-pr` | PR creation with base-branch auto-detection, language arg support |
| `1natsu-git-analysis` | Git history analysis; used as fallback when `entire` is unavailable |
| `1natsu-error-handling` | Error handling patterns |
| `1natsu-entire-context` | `entire` CLI reference for session history / PR enrichment |
| `1natsu-pair-debug` | Collaborative pair-debugging with human-in-the-loop (v1.1.0 as of last session) |
| `1natsu-pair-resolve-conflicts` | Git conflict resolution with human approval at each decision |
| `1natsu-conventional-commits` | Canonical Conventional Commits reference (user-invocable: false) |

### Tech Stack

- **Package runner**: `bunx` (Bun)
- **Skill registry**: `skills` CLI (`bunx skills add`)
- **CI/CD**: None visible; manual verification with `--list` and eval test runs
- **Session history**: `entire` CLI (`.entire/settings.json` with `strategy: "manual-commit"`, `enabled: true`)
- **PR tooling**: `gh` CLI

### Recurring Themes

1. **Skill creation lifecycle**: capture intent → draft SKILL.md → run evals baseline (without_skill) → write skill → run evals (with_skill) → review diff in eval viewer → iterate → commit versioned release.
2. **Japanese localization**: After finding English skills hard to read/review, 1natsu172 asked for all skills to be translated to Japanese. Ongoing tension between "Japanese easier to read" vs. "English might give AI better accuracy."
3. **DRY / deduplication**: Conventional Commits info existed in 3 places; consolidated into one `user-invocable: false` internal skill.
4. **Complexity management**: Pushed back on over-complex `entire` integration; simplified to "just a CLI reference" after a bloated iteration.
5. **Git branching awareness**: Uses Epic branches as aggregation targets for feature branches; `1natsu-create-pr` needed to support non-main/develop base branches.
6. **Human-in-the-loop design**: Recurring pattern across `pair-debug` and `pair-resolve-conflicts` — agent must propose before acting autonomously on ambiguous decisions.

### Tool Integrations

- `entire` (session checkpoint/history CLI) — integrated with `.entire/settings.json`, deny rule on `.entire/metadata/**` read
- Claude Code superpowers plugin: `writing-skills`, `executing-plans`, `using-git-worktrees`, `test-driven-development` skills loaded from `~/.claude/plugins/cache/claude-plugins-official/`
- `skill-creator` plugin: primary tool for new skill development

### Path Convention

Local checkout at: `/Users/1natsu/ghq/github.com/1natsu-vacation/agent-skills/`
Personal skills installed globally at: `/Users/1natsu/.claude/skills/`
