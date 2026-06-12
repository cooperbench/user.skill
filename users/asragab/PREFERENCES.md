# Preferences: ASRagab

## Pushback distribution

| Type | Rate |
|------|------|
| non_pushback | 78.5% |
| correction | 11.8% |
| failure_report | 6.5% |
| takeover | 2.2% |
| rejection | 1.1% |

Most interactions are accepted without comment. When the user does push back, it's almost always a correction (redirect) or a pasted failure, not a rejection.

## What triggers corrections

- **Agent wraps up instead of acting**: a results-summary response triggers "commit changes, merge locally back to main, create handoff document for next batch" — they want the next directive issued, not a recap
- **Agent misses a scope edge**: "did you update the HANDOFF.md to point to the latest doc" — notices a missed detail in an otherwise accepted result
- **Silent regression in a config file**: "hmmm the trigger wasn't changed" — agent said it fixed CI but didn't; user pastes no evidence, just a short hmm + description
- **Redundant naming**: "it seems the generate-evaluator is both a skill and a slash command, confirm this is true and offer proposals for consildation" — duplicates in the plugin surface
- **Scope creep into the wrong direction**: "let's adjust the skill content directly this time" after agent ran an optimizer instead of editing the file

## What triggers failure reports

Pasted raw CI output with a short trailing label. No analysis, no formatting — just the stdout block. Examples:
- Full pytest traceback → "test failures"
- Empty pytest collection → "workflow integration tests not running"
- Evaluator JSON output → (passed inline, no label, treated as context for next turn)

## What triggers takeovers

Agent is in a "presenting options / summarizing what was done" mode when the next action is already obvious to the user. User cuts in: "commit changes, merge locally back to main, create handoff document for next batch" / "use the skill finish the branch". No interest in the summary — wants execution.

## What triggers rejection

Rare (1.1%). Only observed as a bare `"clear"` — likely dismissing an agent response entirely to start fresh.

## What satisfies

- Batch execution completing without errors: user responds with "looks good whats next", "next", "batch 2", "yes"
- GREEN optimization improving score: user reads the JSON and moves on without comment
- Agent proactively catching a doc/README gap: accepted silently (non_pushback)

## Workflow habits

1. **Skill-first**: Sessions begin with a skill invocation (`/superpowers:executing-plans`, `/worktrunk:worktrunk`). Rarely starts with ad-hoc instructions alone.
2. **Batch execution with checkpoints**: Tasks are divided into named batches. After each batch the agent must commit, create a HANDOFF.md, and stop. User reviews between batches.
3. **Handoff-driven context**: Every new session loads `docs/HANDOFF.md` as the primary context source. Plans are stored in `docs/plans/YYYY-MM-DD-<feature>.md`.
4. **TDD / RED-GREEN-OBSERVER**: Tests come first; the eval loop is RED (baseline score) → GREEN (optimization) → OBSERVER (validate). Cares that CI is green before merging.
5. **Worktrees for feature work**: Uses `.worktrees/` or worktrunk for branch isolation; merges locally back to main after completion.
6. **Private repo, local merge**: No PR workflow observed — commits directly to main in local-only repos.
7. **Numbered option selection**: When agent presents choices, responds with "1", "Option A", or a prioritized list ("3, 1, 2, 4") without explanation.
8. **Background agents**: Launches background agents via `/superpowers:executing-plans @docs/HANDOFF.md … spare your context use agents and observe and monitor`; checks in with "just checking are background aagents still alive."

## Stack preferences (observed)

- Python + uv + pytest + pyproject.toml
- GitHub Actions (CI), integration tests separated by pytest mark
- Claude Code plugin/skill system (plugin.json manifest, marketplace.json)
- gepa / optimize-anything CLI
- trufflehog pre-commit hooks for secret scanning
