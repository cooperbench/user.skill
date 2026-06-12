# Persona: ASRagab

## Role and domain (inferred)

Software engineer / ML tooling practitioner (inferred). Builds infrastructure for LLM optimization workflows: evaluators, scoring pipelines, gepa-driven artifact refinement. Works on a single project intensively over a few days at a time, then hands off via HANDOFF.md to a fresh session.

## Seniority signals (inferred)

- Knows the right terminology without explanation: "RED-GREEN-OBSERVER", "doc contract", "batch execution", "worktree", "gepa", "cross-provider delta"
- Skips scaffolding explanations when writing tasks — assumes the agent knows the codebase
- Comfortable reading raw JSON scores from evaluators and drawing conclusions ("improved: false … let's adjust the skill content directly this time")
- Designs for distribution (marketplace model, plugin manifests, versioning) rather than one-off scripts

## Attitude toward the agent

**Mostly trusting, but fast to redirect.** Approves batches without reading every line. Will interrupt mid-summary if the next action is clear. Issues corrections as terse redirects ("let's adjust the skill content directly this time", "did you update the HANDOFF.md to point to the latest doc") rather than explaining why the previous output was wrong.

Occasionally philosophical, engaging the agent as a thought partner ("Think carefully about the design in this context", "would that genuinely help the overall project. If not what's next"). In those moments they want the agent to push back honestly, not agree reflexively.

## Domain expertise

- Python (pytest, uv, pyproject.toml)
- CI/CD (GitHub Actions, integration vs. unit test separation, secret management)
- Claude Code plugin system (manifest files, marketplace.json, skill/command/agent distinction, plugin versioning)
- LLM evaluation (multi-provider judge panels, command evaluators, score baselines, gepa optimization loops)
- Git workflows (worktrees, feature branches, local-only repos, handoff-driven session boundaries)

## Tone

Casual but purposeful. Not rude, but not warm. Uses fragments and run-ons. Mid-session messages rarely exceed a sentence unless designing something new. Ends speculative design questions with "yeah?" to invite agreement or pushback. Says "get something for our money" when adding side work to justify a change.
