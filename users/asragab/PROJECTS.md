# Projects: ASRagab

## ASRagab/optimize-anything ★ dominant repo

**All 14 sessions (100% of activity) are in this single repository.**

### What it is

A Python CLI tool (`optimize-anything` / `gepa`) that runs LLM-driven optimization loops on text artifacts — prompts, skills, configs. The user is simultaneously the author, primary user, and dogfooder.

### Tech stack

- Python 3.12, uv, pytest, pyproject.toml
- CLI entry point with subcommands: `optimize`, `score`, `analyze`
- LLM judge integration: OpenAI (gpt-4o-mini), Anthropic (claude-sonnet), Google (Gemini)
- Bash evaluator scripts (`evaluators/skill_clarity.sh`) alongside LLM judges
- GitHub Actions CI: unit tests on PRs, integration tests on push to main
- Claude Code plugin system integration: plugin.json, marketplace.json, skills/

### Key directories (inferred from prompts)

- `docs/` — HANDOFF.md, plans/YYYY-MM-DD-*.md, design docs
- `skills/generate-evaluator/SKILL.md` — skill for generating evaluator scripts
- `skills/optimization-guide/SKILL.md` — skill for running gepa workflows
- `evaluators/skill_clarity.sh` — bash heuristic scorer
- `tests/test_cli.py`, `tests/test_doc_contract.py`, `tests/test_llm_judge.py`
- `integration_runs/` — run artifacts from RED-GREEN-OBSERVER cycles

### Recurring themes

1. **Skill quality**: obsessive about evaluator/skill clarity scores; runs RED-GREEN-OBSERVER cycles to push scores above baselines
2. **Plugin system integration**: building and maintaining Claude Code plugin manifests and marketplaces so `optimize-anything` is installable as a plugin
3. **CI hygiene**: separation of unit vs. integration tests, secret management per provider, doc contract tests catching missing files
4. **Handoff discipline**: every batch of work produces a HANDOFF.md; sessions are designed to be resumable by a fresh agent with zero carry-over context
5. **Multi-provider evaluation**: OpenAI + Anthropic + Google judges; cross-provider delta as a stability metric (target ≤ 0.03)
