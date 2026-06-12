# PROJECTS.md — ujuc

## ujuc/agent-stuff (50%) — DOMINANT

**Purpose**: Claude Code and multi-agent configuration repository. Deployed as a git submodule inside `ujuc/dotrc` at `agents/`, then symlinked to `~/.claude`. Contains skills, guides, specs, and documentation standards for Claude Code sessions.

**Tech stack**: Markdown/YAML (no build system), Zsh scripts for linting, git pre-commit hooks.

**Directory structure (as of sessions):**
```
agents/claude/
├── CLAUDE.md          # Claude-only settings
├── AGENTS.md          # agents.md-standard project guide
├── settings.json      # Model, permissions
├── mcp.json           # MCP servers (sequential-thinking)
├── skills/
│   └── generate-claude-md/SKILL.md  # 4-step CLAUDE.md generator
├── scripts/
│   ├── lint-docs.sh
│   └── pre-commit-lint
└── memory/MEMORY.md
spec-design/
├── common-template.md  # YAML frontmatter spec (CalVer, required fields)
└── writing-guide.md    # Korean-language writing rules for docs
docs/guides/            # AI-generated documents following spec-design rules
```

**Recurring themes:**
- Migrating XML-format guide documents to YAML frontmatter format
- Evolving the `generate-claude-md` skill (4-step: analyze → interview → generate → validate)
- Designing a 3-layer document hierarchy: `CLAUDE.md → AGENTS.md → contributing-docs/`
- Enforcing Karpathy-style CLAUDE.md philosophy: "이것 없이 Claude가 실수하는가?" as the inclusion test
- Adding nested CLAUDE.md support for monorepos and submodules

---

## ujuc/dotrc (50%)

**Purpose**: Personal macOS dotfiles repository. Manages shell environment via symlinks from `${DOTRCDIR}` (`~/.config/dotrc`) to standard locations. `agents/` is a git submodule pointing to `ujuc/agent-stuff`.

**Tech stack**: Zsh (single `zshrc` file, section-divided), TOML (starship), JSON (ghostty, zed, VSCode), zimfw, mise.

**Key patterns:**
- Eager loading for fast tools (starship, fzf); lazy-loading wrappers for slow ones (zoxide, mise)
- Symlink deployment: `agents/claude/ → ~/.claude`, `agents/pi/ → ~/.pi`, `agents/gemini/ → ~/.gemini`
- Korean Conventional Commits for all changes
- No CI/CD; uses `./scripts/benchmark.sh` for zsh startup benchmarking

**Recurring themes:**
- Writing/regenerating `CLAUDE.md` and `AGENTS.md` for the dotrc root using the `generate-claude-md` skill
- Restoring Agent Identity sections in `agents/claude/CLAUDE.md` from `SOUL.md` canonical source
- Adding nested CLAUDE.md support for `agents/` submodule
- Updating submodule commit references
