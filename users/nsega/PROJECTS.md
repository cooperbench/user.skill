# nsega — Projects

## nsega/mcp-obsidian ★ DOMINANT (50% of sessions)

**What nsega does here**: Builds and maintains a Go-based MCP server that exposes Obsidian vault operations (note search, frontmatter manipulation, slug generation, deletion) to AI agents via JSON-RPC. Refactors monolithic `main.go` toward idiomatic Go package structure. Monitors CI (lint + build/test matrix on Go 1.25+). Writes no tests directly but verifies tool registration and end-to-end MCP handshake.

**Tech stack**: Go, `modelcontextprotocol/go-sdk`, slog, staticcheck, GitHub Actions, Makefile, JSON-RPC.

**Recurring themes**:
- Logging best practice (slog migration)
- Package structure refactoring ("meaningful size of logic")
- MCP protocol compliance (handshake, tool schema, protocol version)
- CI green-lighting (lint + test matrix)
- PR-first, step-by-step commit workflow

---

## nsega/.emacs.d (33% of sessions)

**What nsega does here**: Configures and debugs a personal Emacs setup. Primary concern during observed sessions: high CPU usage from overactive hooks (`buffer-list-update-hook`, `window-configuration-change-hook`). Also manages gitignore for generated files (tree-sitter parsers) and Claude Code config files.

**Tech stack**: Emacs Lisp, tree-sitter, vterm, git, `.claude/settings.json` / `settings.local.json`.

**Recurring themes**:
- CPU/performance issues from hook frequency
- git hygiene (.gitignore for build artifacts)
- Claude Code integration (`.claude/` directory management)

---

## nsega/mcp-todoist (17% of sessions)

**What nsega does here**: Maintains another MCP server, this one integrating with Todoist. Minimal direct evidence in the digest — only presence in repo stats.

**Tech stack**: Likely Go (consistent with other MCP repos). (inferred)

**Recurring themes**: (insufficient data to characterize)
