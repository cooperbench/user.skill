# Preferences

## What triggers corrections (14% pushback rate)

- **Consistency failures**: Numbering, naming, or structural patterns applied in one directory but not another. Top trigger — he notices and surfaces these immediately after the agent claims completion.
- **Agent jumping ahead or declaring premature victory**: The agent says "all done" while Mathews-Tom still has concerns about quality or consistency.
- **Wrong branch name**: Using a branch name other than his specified convention (e.g., `feat/alignment-systems`).
- **Agent asking clarifying questions when the answer was in context**: Responding "Which sections?" when the user said "sections like `foundational`, `alignment` and `systems`" — context was available.
- **Marginal quality criteria**: Noticing a script "only has a marginal pass" on a success criterion rather than confidently passing.
- **Unsolicited insight blocks**: The agent adding "★ Insight ─────" boxes or opinions in responses — he interrupts and redirects to concrete execution steps.
- **Commit granularity**: Committing all changes in one big commit when logical groupings were obvious; he pushes back with "use sequential thinking and commit using multiple commits."

## What satisfies them

- Scripts completing within the 7-minute M-series Mac runtime budget
- Validation tables showing pass/fail for each success criterion per script
- Clean, logically grouped commits with conventional commit messages (`feat(scope): description`)
- Detailed PRs listing all commits, changed files, and implementation notes
- Consistent naming and file structure across all directories
- Comment density in the 30-40% range
- Zero external dependencies, stdlib only

## Workflow habits

- **Plan-first**: Enters plan mode, produces a full implementation spec (or has Claude Code produce one), then launches execution with "Implement the following plan:"
- **Multi-agent orchestration**: Directs parallel implementation waves by task-agent type and model tier. References "TeamCreate", parallel waves, "file ownership is sacred."
- **Validates before merge**: Always runs scripts individually and reviews output before merging PRs. "run all 7 scripts to validate before merging."
- **Multiple semantic commits**: Prefers 3–10 commits per PR with clear scopes over one big commit.
- **PRs for everything**: Always opens a PR rather than pushing directly to main; asks for "detailed PR."
- **Autonomous mid-session**: Does not babysit during implementation — "keep going, don't wait for me."
- **No code-level explanations needed**: Does not ask the agent to explain algorithm choices; questions are about quality, consistency, or structure.
- **Interrupts tool use**: Frequently interrupts when the agent is running tools mid-session to redirect; several sessions show `[Request interrupted by user for tool use]`.
- **Opinion-soliciting before pivots**: Occasionally asks "What do you think?" before committing to a direction, but then immediately acts on his own judgment.

## Stack / tool preferences

- Python 3 (stdlib only — `os`, `math`, `random`, `urllib.request`, `collections`)
- `random.seed(42)` convention everywhere
- Claude Code with task agents (Sonnet for implementation, Opus for coordination)
- Conventional commits format
- GitHub PRs
- M-series Mac as local dev environment
- `names.txt` from Karpathy's makemore as the canonical training dataset
