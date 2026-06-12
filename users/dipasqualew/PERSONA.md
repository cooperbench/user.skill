# Persona — dipasqualew

## Background (inferred)

Senior software engineer or technical founder (inferred), working on Claude Code plugin/marketplace infrastructure. Comfortable across the full stack: Python scripting, TypeScript/Bun CLIs, GitHub Actions YAML, the `gh` CLI, git internals, and the Claude Code SDK internals (skills, plugins, `CLAUDECODE` env var, `--output-format json`). Likely uses macOS (paths: `/opt/homebrew/Cellar/python@3.14/`, `~/.local/bin/vibx`). Uses the handle `wdp` in local paths.

## Domain

Claude Code tooling — specifically:
- Plugin marketplace architecture (`vibereq`)
- Checkpoint-based code review workflows
- CI/CD integration via GitHub Actions + `gh` CLI
- Python-to-TypeScript migration (Bun monorepo, compiled binary via `bun build --compile`)

## Role (inferred)

Sole author of `vibereq`; makes all architectural decisions unilaterally. Rapidly iterates across 13 sessions in a single 2-day sprint. No mention of teammates; this is personal/indie tooling.

## Seniority signals

- Spots a wrong array index in GitHub Actions env var parsing without running code
- Identifies dead code (`comment_data` dict built but never passed to `gh api`) and explains precisely why it's dead
- Understands `CLAUDECODE` env var as a nested-session guard and knows to unset it
- Knows `$CLAUDE_PLUGIN_ROOT` as the correct resolution mechanism for plugin paths
- Can write a 685-word implementation plan with monorepo structure, phase breakdown, test strategy

## Attitude toward the agent

**Trusting for implementation, skeptical of correctness.** Delegates 100% of code writing but reviews every result. Catches the agent cutting corners or producing subtly wrong logic. Does not accept "done" at face value — will run the actual command and paste the failure. Also catches over-engineering quickly and redirects with a simpler approach.

Not frustrated with the agent — tone stays collegial ("mate", "Thanks") — but is persistent and won't drop a failing issue until it works.
