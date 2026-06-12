# PROJECTS

## ronnnnn/cc ★ (dominant — 100% of sessions)

**What it is**: A personal Claude Code plugin and skill collection. ronnnnn uses this repo as his primary workspace for extending Claude Code with custom automation.

**Tech stack**:
- Python 3 for hook scripts (no external dependencies)
- Markdown for skill/agent/command definitions
- JSON for plugin manifests and marketplace registry
- Shell scripts (bash/zsh) for worktree setup and git operations
- commitlint + Conventional Commits for commit message enforcement

**Plugin structure** (inferred from prompts):
```
plugins/
  git/            # git automation: commit, pr-create, pr-watch, pr-ci, pr-fix, pr-explain, wt
  hookify/        # custom replacement for official hookify plugin
  claude/         # Claude Code configuration tools (claude:init, claude:update)
  catch-up/       # (referenced in bump-version targets)
.claude-plugin/
  marketplace.json  # plugin registry
```

**Recurring workflows**:
1. **Plugin creation**: large spec-dump → agent implements → nitpick format → verify → commit → PR
2. **PR automation loop**: `/git:pr-create` → `/git:pr-watch` (autonomous 30–120 min loop) → CI fixes → merge
3. **Version management**: `/bump-version` infers target from changed files; auto-increments semver
4. **Skill iteration**: short correction → agent fixes → re-verify in real directory

**Active themes across sessions**:
- Improving git plugin (pr-watch pagination, commit scope inference, wt worktree setup)
- Building hookify replacement with global + project rule search and regex tool_matcher
- Integrating external tools (entire CLI → changed to manual-commit strategy)
- Enforcing fact-checking on review comments with MCP-prioritized sources
- Migrating commands → skills and writing all markdown in Japanese
