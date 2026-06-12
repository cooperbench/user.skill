# Projects — dipasqualew

## dipasqualew/vibereq ★ dominant (100% of sessions)

A Claude Code plugin marketplace that packages AI-assisted checkpoint-based code review workflows as installable plugins.

### What the user does here

All 13 sessions, all 2 days. This is the active project. The user is the sole author.

### Tech stack

- **Plugin layer**: Claude Code plugin manifest (`plugin.json`), skills (`SKILL.md`), marketplace (`marketplace.json`)
- **Scripts (legacy)**: Python 3 — `get-checkpoint-folders.py`, `intent.py`, `get-intents.py`, `run-review.py`
- **CLI (migration target)**: TypeScript/Bun monorepo → `vibx` compiled binary
  - `apps/cli/src/` with yargs, vitest
  - Commands: `get-checkpoint-folders`, `get-intents`, `intent`, `review`
- **CI**: GitHub Actions, `gh` CLI, `GITHUB_REF_NAME` / `GITHUB_EVENT_PATH`
- **Git conventions**: `Entire-Checkpoint:` commit trailers, `entire/checkpoints/v1:` git refs

### Recurring themes

1. **Plugin path resolution**: `$CLAUDE_PLUGIN_ROOT` is the env var that points to the installed plugin root; early bugs involved using `{VIBEREQ_ROOT}` as a literal string instead of expanding it
2. **Nested session blocking**: `CLAUDECODE` env var blocks Claude Code from launching inside another Claude Code session; scripts must unset it before spawning `claude -p`
3. **CI JSON output cleanliness**: Claude Code skills called in CI mode (`/skill ci`) must output raw JSON only — no fenced blocks, no commentary — or the wrapping script breaks
4. **`create-reviewer` meta-skill**: a skill that generates other skills (specialized reviewers) by asking the user questions and producing a `SKILL.md`
5. **`vibx review` UX**: GitHub PR review flow — start a review, attach diff comments, resolve fulfilled ones immediately, post general findings to the review summary comment

### Related path

`~/git/dipasqualew/vibe-writing/.claude/` — a sibling repo that contains the original skills that were migrated into the plugin. Referenced when fixing the installed skill in place.
