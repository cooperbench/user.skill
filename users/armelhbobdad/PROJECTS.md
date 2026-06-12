# Projects: armelhbobdad

## armelhbobdad/bmad-module-skill-forge ★ DOMINANT (100% of sessions)

**What it is**: An npm module (npx bmad-module-skill-forge install) that compiles
AST-verified, provenance-backed agent skills from code repositories, documentation websites,
and developer discourse. The "Skill Forge" (SKF). Installed via BMAD methodology into a
project's `_bmad/skf/` directory.

**Tech stack**:
- Node.js CLI installer (`tools/skf-npx-wrapper.js`, `tools/cli/lib/installer.js`)
- BMAD module structure: `src/agents/`, `src/workflows/`, `src/knowledge/`, `src/module.yaml`
- Astro + Starlight documentation site (`website/`)
- GitHub Actions CI (`quality.yaml`)
- npm package (`package.json`) with `bmad-module-skill-forge` and `skill-forge` bin aliases
- Husky + `entire` CLI for git hooks

**Workflows in `src/workflows/`**:
- `analyze-source` — scan a codebase to identify skillable units
- `audit-skill` — drift detection between code and existing skill
- `brief-skill` — generate a skill brief (YAML spec)
- `create-skill` — full skill creation pipeline
- `create-stack-skill` — integration playbook from existing skills
- `export-skill` — package a skill for distribution
- `quick-skill` — fast single-pass skill creation
- `setup-forge` — initial forge configuration (tier detection, ccc registry)
- `test-skill` — validate skill quality
- `update-skill` — re-sync skill after code changes
- `verify-stack` — feasibility check for stack skill
- `brief-skill`, `export-skill`, `analyze-source` also present

**Capability tiers** (core concept):
- Quick — file I/O only
- Forge — ast-grep structural AST search
- Forge+ — cocoindex-code (ccc) semantic discovery (added late in development)
- Deep — QMD (BM25 keyword search) + source reading via cloned repo

**Recurring themes in sessions**:
- Workflow step file validation (frontmatter variables, line count limits, menu patterns)
- Documentation site alignment with TEA reference module
- npm publish pipeline and install flow debugging
- Party-mode architectural brainstorming (QMD vs ccc, indexing strategies)
- Pre-push deep review rituals
- GitHub issue creation and closure

**Reference module** (used as template): `@temp/bmad-method-test-architecture-enterprise/`
(TEA) — provides canonical patterns for knowledge folders, website structure, workflows.

**Agent persona**: Ferris — the AI agent that runs all SKF workflows. Runs in "Ferris Architect
mode" with a zero-hallucination constraint.
