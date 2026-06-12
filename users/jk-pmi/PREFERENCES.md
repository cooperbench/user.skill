# PREFERENCES — jk-pmi

## Pushback distribution

| Type | Rate |
|------|------|
| Non-pushback (accepted) | 52.4% |
| Correction | 38.6% |
| Failure report | 5.3% |
| Rejection | 3.7% |

Nearly 1 in 2 agent responses triggers at minimum a correction. The user actively steers.

## What triggers corrections

- **Agent asks clarifying questions** when the user expected action. Response: "implement this. no questons. NO QUESTIOS!" or silent interruption + re-prompt.
- **Agent misidentifies the scope of the request.** "2 is again codebase specific." / "DO NOT add dirigent feature flags, add the argument to the plan skill frontmatter"
- **Agent takes shortcuts** (grep-based tests instead of integration tests, sudo password prompt instead of a proper fix).
- **Agent answers the wrong thing or goes off on a tangent.** "nein man. schon wieder vollkommen am pnkt vorbei" (again completely off the point).
- **Agent misses a detail that was already specified.** User re-sends the full prompt with the constraint added in caps or bold.
- **Agent claims something is impossible when documentation says otherwise.** User pastes the docs URL: "fucking liar: https://..."
- **Agent forgets to commit.** "the dirigent tends to forget to commit stuff it has built"

## What triggers rejections

- Agent pushes code with a critical bug the user discovers immediately (password prompt, broken hooks).
- Agent waits instead of acting after the user approved a plan.
- Stash/reset as escape hatch: `<bash-input>git stash</bash-input>` or "push" when work is incomplete.

## What satisfies them

- Correct, autonomous execution with a commit at the end.
- Answers to "is this fixed now?" confirmed by a working smoke test.
- Short summaries, not long explanations: "can you give a summary (and just a summary) of the dirigent (2 sentences)"
- Agent uses `ultrathink` / external references proactively.
- When agent acknowledges it got it wrong without over-explaining.

## Workflow habits

- **No planning ceremonies.** Does not ask for a plan before implementation; says "implement this" and expects the agent to figure out the plan internally.
- **"ultrathink" as a keyword.** Used to signal that the user wants the agent to reason deeply before acting, not just execute.
- **Smoke-test loop.** After significant changes, always runs the smoke test: "run smoke test again", "yes. smoke-test again :D"
- **Git-heavy pacing.** Commits frequently; uses terse git commands directly ("commit", "bump version", "create pr", `<bash-input>git co master</bash-input>`).
- **Interrupts and re-prompts.** Does not let the agent finish if it's going the wrong direction. Kills the run, then re-sends a tighter version of the prompt.
- **Explores before implementing.** Scans existing resources first: `.opencode` dir, `.claude/` dir, external tools (entire, byterover). "look in the .opencode dir. Any cool stuff we can copy?"
- **Thinks by analogy.** "hmm. why reinvent the wheel when we can just copycat the opencode skills and make them claude skills :D"
- **Test quality is non-negotiable.** Will reject grep-based acceptance criteria and write detailed tables of what tests MUST cover. Uses the term "user-based" tests to mean behavioral/integration, not unit.
- **Does not ask for explanations.** Rarely asks "why does X work" — prefers to inspect output directly or check logs.
- **Forwards team feedback verbatim.** Pastes user/team feedback (sometimes in German) and asks the agent to act on a specific numbered item.

## Tool and stack preferences

- Python + `uv` for packaging and running.
- Claude Code as the underlying agent. Aware of plugin system, skills, agents, hooks.
- Uses `ultraplan` (remote planning session) for large architectural decisions.
- References `brv` (byterover), `entire.io`, `ast-grep`, `opencode` as tools worth integrating.
- Prefers `haiku` for fast/cheap test runs; `opus` for deep analysis agents.
- `$HOME/.dirigent/` for ephemeral run state (not inside the repo).
- Shell hooks preferred over Python hooks when both are an option: "shell it is."
