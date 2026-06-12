# Persona — yorrick

## Background (inferred)

- **GitHub handle**: `yorrick` (real name likely Yorrick Jansen, inferred from path `/Users/yorrickjansen/`)
- **Role**: Independent developer / plugin author, possibly a technical founder or senior IC (inferred from building tooling for his own workflow rather than shipping a product)
- **Seniority**: Senior-to-staff level (inferred). Designs async state-graph engines from scratch, reasons fluently about plugin distribution, knows when to avoid LangGraph, reaches for uv, pyproject.toml, and pytest without friction.
- **Operating system**: macOS (evidenced by `/Users/yorrickjansen/`, `/Applications/Google Chrome.app/`, `platform darwin`)
- **Python toolchain**: `uv`, `pyproject.toml`, `pytest`, Python 3.14 beta — early-adopter profile.

## Domains

- **AI coding tooling**: building Claude Code plugins that automate the dev loop (brainstorm → branch → implement → test → PR → review).
- **Workflow orchestration**: designing a lightweight Python `StateGraph` engine that can call Claude, Codex, and Gemini CLI as nodes.
- **Plugin distribution**: thinking about how to package and publish Claude Code plugins; aware of distribution constraints (no shared PyPI packages across plugins).
- **Quality engineering**: lint/format/typecheck gates are non-negotiable; docs-as-code (CLAUDE.md, Mermaid diagrams).

## Attitude toward the agent

**Trusting but directive**. Lets the agent do 89% of the code; rarely writes code himself. However, corrects frequently (34% of prompts are corrections) when the agent uses the wrong tool, adds scope it wasn't asked for, or skips a required quality step. Interrupts mid-run without ceremony. Does not explain his frustration — just redirects.

- Trusts the agent to implement once direction is set.
- Does NOT trust the agent to choose the right slash command or tool; polices this actively.
- Comfortable giving very short answers ("yes", "ok", "2") when the agent presents clear options.
- Will brainstorm verbosely when exploring design space, then switches back to one-liners once a path is chosen.

## Tone

Casual, typo-rich, no pleasantries. Speaks in fragments and imperative sentences. Never says "please" or "thanks". Occasionally conversational when thinking out loud ("I mean, as long as we don't push and publish, no one is going to be impacted right"). Uses "we" to refer to himself + agent as a pair.
