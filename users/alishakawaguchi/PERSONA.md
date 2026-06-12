# Persona: alishakawaguchi

## Role and domain (inferred)

Software engineer at Entire (inferred from repo `entireio/cli` and path `/Users/alisha/Projects/`). Works on developer tooling — a CLI that integrates with AI coding agents (Claude Code, Gemini CLI, Factory AI Droid, OpenCode). The work spans Go backend, GitHub Actions CI, E2E test infrastructure, and Claude Code skill/plugin authoring.

## Seniority signals

- Writes multi-page implementation plans before delegating: root cause analysis, rejected alternatives, exact file/line references, verification steps. This is the planning output of someone who has already debugged the problem mentally.
- Critiques the agent's code at the interface level: "agent-integration plugin not quite right. the commands should point to the skill md file instead of duplicating logic."
- Knows when tests are trivial: audits an entire test file and classifies tests as "trivial / nearly useless (candidates for removal)" vs. "genuinely useful."
- Catches type-system errors by pasting `golangci-lint` output directly — doesn't explain what's wrong, just pastes the evidence.
- Understands GitHub Actions expression language, Go package boundaries, tmux PTY behavior, and git hook mechanics.

**Seniority estimate**: Senior IC or tech lead (inferred). Operates like someone who designs the architecture and then has an AI execute it.

## Agent relationship

- **Highly delegating** — agent code percentage median is 100%; they write almost no code themselves during sessions.
- **Architecturally in control** — they pre-design in plan mode and hand a finished spec to the agent. The agent is an executor, not a collaborator on design.
- **Skeptical of agent autonomy** — interrupts tool use frequently, enforces strict permission lists, pushes back on anything that seems too permissive.
- **Impatient with verbosity** — annotated persona distribution shows "Expert Nitpicker" at 70.8%. They cut off over-explained responses by immediately issuing the next command.

## Tone

- Direct, minimal. No filler phrases, no "please", no "thanks."
- Corrections are factual statements, not complaints: "update E2E_CONCURRENT_TEST_LIMIT for droid to be 3."
- Occasional wry question when confused by agent behavior: "why is there a * nect to agent integration and how to have top level agent integration skill run all 3"
- Short affirmatives: "yes", "2" (when given numbered options).

## Locale

English only (1.0 in language distribution). macOS (paths reference `/Users/alisha/`, `/var/folders/`, `/private/var/folders/`). Uses `mise` as the task runner.
