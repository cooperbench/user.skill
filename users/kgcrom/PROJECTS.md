# Projects

## kgcrom/cluefin ★ dominant (58% of sessions)

**What kgcrom does here**: Builds a Bloomberg Terminal-style TUI dashboard for Korean stock market data. The main app is `cluefin-desk` (a Textual TUI), backed by `cluefin-openapi` (Python SDK wrapping Kiwoom, KIS, DART APIs).

**Tech stack**:
- Python, uv, Textual (TUI framework), Pydantic, loguru, plotext, rich
- Kiwoom Open API (domestic stock data, sector indices, ETF, rankings, investor flows)
- KIS WebSocket API (real-time bond prices)
- DART API + XBRL (corporate disclosures, financial statements)
- Monorepo: `apps/cluefin-desk/` and `packages/cluefin-openapi/`

**Recurring themes**:
- Implementing 5-screen navigation: MKT, RANK, THEME, ETF, INV (Bloomberg-style numbered keys `1`–`5`)
- Debugging invisible/blank panels — API field name mismatches (e.g., `all_inds_index` → `all_inds_idex`), wrong parameter values, ANSI rendering artifacts
- Adding Literal type validation to Kiwoom API method signatures
- Creating PR/issue templates for the open-source repo
- Publishing `cluefin-openapi` to PyPI via `uv publish`

**Style of work here**: Plan-heavy. kgcrom writes full Korean design specs with ASCII mockups before any implementation session.

---

## kgcrom/agent-foundry (42% of sessions)

**What kgcrom does here**: Builds a universal AI skills/agents repository for use across Claude Code, Codex, Gemini, GitHub Copilot. Includes CLI tooling (Bun/TypeScript) for validating, listing, and testing skill definitions. GitHub Actions integration.

**Tech stack**:
- TypeScript, Bun (`bun run validate`, `bun test`, `bun run check`, `bun run typecheck`)
- YAML skill definitions with frontmatter (name, description, allowed-tools, license, metadata)
- GitHub issue/PR templates (YAML form format)
- GitHub CLI (`gh`) for repo management

**Recurring themes**:
- Creating new skill files (commit, create-pr, create-issue) with 8-step Korean workflow docs
- Writing eval YAML files for each skill (`evals/skills/<name>.eval.yaml`)
- Maintaining `evals/manifest.json` as skill registry
- Wording repo description for GitHub (English, "universal collection" framing)
- Commit message formatting: English type prefix + Korean summary/body

**Style of work here**: Mix of spec dumps (for skill creation) and short operational messages (commit resets, description changes). Less debugging, more scaffolding.
