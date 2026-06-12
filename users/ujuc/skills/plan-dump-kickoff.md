---
name: plan-dump-kickoff
description: "ujuc opens big implementation sessions by pasting a fully-formed plan document (500–1500 words) with the prefix 'Implement the following plan:'. Trigger: opening prompt for any non-trivial creation or refactor task."
---

# Plan-dump kickoff

When starting a substantive session, ujuc pastes a complete implementation plan he already wrote (typically from Claude Code's plan mode). The plan is:

- Prefixed with `Implement the following plan:` or `Implement the following plan:\n\n`
- Written in markdown with `# Title`, `## Context`, `## Changes`, numbered steps, and `## Verification`
- Includes exact file paths, before/after code blocks, rationale for each change
- Often ends with a note: `If you need specific details from before exiting plan mode [...], read the full transcript at: /Users/ujuc/...`
- Sometimes 1000+ words with code snippets and table summaries

He does NOT ask the agent to design the approach. The plan is the specification; the agent executes it.

## Examples

**Opening a git file move task:**
> "Implement the following plan:\n\n# Plan: Move template/guide files from docs/ to spec-design/\n\n## Context\n\nThe files in `docs/` (`common-template.md`, `writing-guide.md`) are user-authored design specifications [...] These specification files need a new home: `spec-design/`.\n\n## Changes\n\n### 1. Create `spec-design/` directory and move files\n\n- `docs/common-template.md` → `spec-design/common-template.md`\n- `docs/writing-guide.md` → `spec-design/writing-guide.md`\n\nUse `git mv` to preserve history. [...]"

**Opening a documentation migration task:**
> "Implement the following plan: # Guidelines.md Migration Plan ## Context The user maintains comprehensive development guidelines in a global `~/.claude/` configuration. [...] **Goal**: Migrate the global `guidelines.md` into the `agent-stuff` project under `docs/guides/guidelines.md`, transforming its format to comply with the project's documentation specifications. [1000+ more words]"
