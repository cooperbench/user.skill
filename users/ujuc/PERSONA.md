# PERSONA.md — ujuc

## Background (inferred)

Korean software developer, likely based in Korea given consistent Korean-language commit messages, Korean UI preferences, and macOS tooling. Maintains a personal development environment as a first-class engineering artifact — dotfiles are versioned, symlink-deployed, and submodule-linked to an AI agent configuration repository. This level of systematic environment management signals seniority and a long programming career.

## Role (inferred)

Individual contributor or independent developer. No references to team PRs, code reviews from others, or org-level tooling. Projects are personal repos: `ujuc/agent-stuff`, `ujuc/dotrc`. He may be a staff or senior engineer at a company but uses Claude Code entirely for his personal tooling work.

## Domain expertise

- **AI agent configuration**: Designs and iterates CLAUDE.md/AGENTS.md document hierarchies, Claude Code skills, and documentation specification systems with deep understanding of how LLM context works (e.g., knows that style rules belong in linters not CLAUDE.md; knows the system prompt is ~50 instructions already; knows CLAUDE.md errors amplify downstream).
- **Zsh/macOS environment**: Expert-level zsh config (zimfw, starship, fzf, zoxide, mise); understands eager vs. lazy loading patterns.
- **Documentation systems**: Designed a custom YAML frontmatter spec (CalVer versioning, required fields), a writing guide, and a multi-layer doc hierarchy (CLAUDE.md → AGENTS.md → contributing-docs/).
- **Git workflow**: Consistent Conventional Commits in Korean, submodule management, symlink deployment patterns.

## Seniority signals

- Opens tasks with complete implementation plans including file-level diffs — he has already thought through the change before asking Claude.
- Injects Karpathy-referenced principles ("LLM은 인컨텍스트 학습자다") and cites performance optimization literature (Jeff Dean, Abseil).
- Pushes back on agent over-engineering with principled arguments, not just preferences.
- Annotated 87.5% as "Expert Nitpicker" — spots exact field-level issues (YAML bracket syntax, wrong metadata field scope, wrong layer in document hierarchy).

## Attitude toward the agent

**Trusting for execution, skeptical of scope.** He delegates well-defined tasks without micromanaging steps, but corrects immediately when the agent adds unrequested content, uses wrong philosophy, or produces verbose summaries he didn't ask for. The most common correction pattern is pasting the actual guideline document — he expects the agent to read and apply it, not be told in plain language. He uses the agent as a fast executor of plans he already designed.

## Tone

Casual and economical in Korean; technical and structured in English. Rarely uses formal politeness levels (존댓말). Uses "어" as a soft affirmation. No explicit praise — acceptance is silence or moving directly to the next item.
