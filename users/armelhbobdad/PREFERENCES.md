# Preferences: armelhbobdad

## What triggers correction (29% of turns)

- **Agent ignores workflow command**: If the agent responds to a `/bmad-bmb-edit-module` invocation
  with a menu instead of loading and executing the full workflow file, Armel fires the ALL CAPS
  override.
- **Wrong factual claim in output**: Agent writes something stale or incorrect about the project
  ("you said X, it is not the case for the moment").
- **Missing scope**: Agent omits a file/doc that should have been updated ("yes update everywhere.
  Do not forget to align it with the astro documentation too.").
- **Untested UI state**: Agent reports done without testing light mode, dark mode, or a specific
  URL path.
- **Broken links**: Catches wrong base paths in generated URLs
  ("instead of `.../getting-started/` we get `.../bmad-module-skill-forge/getting-started/`").
- **Out-of-scope description**: Agent describes SKF as "Part of the BMad Method ecosystem" before
  that is true — corrects immediately.
- **Wrong tool recommended**: Agent suggests a flag that doesn't work (`ccc ---version`), Armel
  says "Try it yoursefl".

## What triggers failure reports (3%)

- UI bug reports with live URL: "The app is live at http://localhost:4321/architecture/. When I
  click on the diagram, it is shown too small."
- Version / display issues during live install testing — pastes full terminal session.

## What triggers rejection (1%)

- Outright "drop" — hard stop, no explanation.
- "yes" in response to an unwanted action prompt (once accepted an undesired path, corrected).

## What satisfies

- Pre-implementation plan presented as a table or structured list → "yes" or "Implement the
  following plan: ..." with the plan pasted back.
- Agent asks party-mode brainstorm → Armel gives numbered answers: "1. X 2. Y 3. Z".
- Deep review before push catches real issues → Armel gives "fix all N" or selects specific items.
- Clean commit confirmed → "perfect. please commit" or just "commit".

## Workflow habits

- **Plan-first when scope is large**: Pastes full implementation plans as opening prompt for
  big features; smaller tasks get direct one-liners.
- **Not test-driven**: No TDD references. Tests come as a CI/linting check, not driving design.
- **Commit cadence**: Commits frequently during development — "commit", "commit files from git
  status", "read all changes and commit". Sometimes commits before continuing next phase.
- **Party mode for architecture decisions**: Uses `/bmad-party-mode` when facing trade-offs
  (e.g., which deep-tier tool to use, brainstorming QMD alternatives).
- **Phase templates to control agent**: Pastes Feature Development Phase 1–6 templates mid-session
  to force a structured agent workflow.
- **References examples from peer repos**: `@temp/bmad-method-test-architecture-enterprise/` is
  the TEA reference module consulted frequently.
- **Explains rationale sparingly**: Usually omits why; occasionally gives one-sentence context
  ("It is need to run npx command where is needed.").
- **Does not ask for explanations**: Rarely wants the agent to explain what it did; wants action.
- **Memory plugin**: Explicitly asks agent to use memory plugin ("use the memory plugin to see
  what works in the past").

## Stack and tool preferences

- Claude Code as primary IDE
- npm / npx for distribution
- BMAD module framework (workflows, agents, step files)
- ast-grep for Forge tier, QMD for Deep tier, cocoindex-code (ccc) for Forge+ tier
- Astro + Starlight for documentation sites
- GitHub Issues for bug tracking (references issue URLs directly)
- Husky for git hooks
- `entire` CLI tool for commit hooks
