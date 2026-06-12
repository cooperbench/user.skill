# Preferences: oddessentials

## Pushback distribution

- **Correction (48%):** Most common pushback. He rewrites the agent's direction with a structured markdown list, usually bullet points mapping to specific requirements, file paths, and line numbers.
- **Non-pushback (39.8%):** Includes brief approvals ("Got it. Proceed", "yes please") and neutral continuations (pasting task output).
- **Failure report (6.4%):** Pastes raw CLI output, CI run URLs, or task-notification XML and says what failed. Minimal commentary — the error speaks for itself.
- **Rejection (5.7%):** Refuses the agent's output and reverts or benches: "Stop", "Revert what ever you just did", "you're on the bench now bro."

## What triggers correction

- Agent makes **unverified claims** ("Is this something you read somewhere or are these verified findings?")
- Agent **commits without permission** ("answer me before committing")
- Agent **scopes beyond what was requested** ("You changed this file scripts/run_repo_hook.py")
- Agent delivers **broad/generic analysis instead of specific findings** ("Now focus on what I'm asking you. Why isn't gitleak running properly? DOn't tell me about the history of it")
- Agent introduces a **silent failure mode** ("I do not want some shit where the user doesn't have python installed so all checks silently fails or something insane like that")
- Agent uses **broad exception catches** ("Critical: do not silently swallow Exception in __init__.py.")
- Agent **does not enforce invariants** — e.g., zero suppressions, no `any` types, CI parity
- Agent **rushes to implementation** before plan is approved

## What satisfies him

- Agent says "I'm ready" or summarizes the repo state accurately before beginning work
- Clean CI + local gate parity confirmed
- "Devil's Advocate" multi-agent sign-off on plan/branch
- Ratchet baselines actually decremented (not just claims)
- Tests covering every success criteria item, not approximations ("~10 tests" is unacceptable)
- Commits that are small, focused, and pause before pushing

## Workflow habits

1. **Orientation first.** Every session starts with the agent reading the branch, invariants, and issue before any action.
2. **Plan before code.** He often uses `/plan`, `/speckit.specify`, `/speckit.plan` before any implementation.
3. **Multi-agent review.** Deploys TeamCreate specialist panels (devops, qa, fullstack, architect, devex, Devil's Advocate) to review specs and branches.
4. **Phased implementation.** Large tasks broken into numbered phases (Phase 1–7, tasks T001–T065, etc.); he tracks progress by task number.
5. **Commit cadence:** Small, targeted commits. "Commit first and pause" is a recurring pattern. He never wants to push without explicit sign-off.
6. **Local testing before push.** Smoke tests via CLI: `ado-insights stage-artifacts --org ... --serve --open`. He runs `python scripts/run_pytest.py` and pastes output when reporting failures.
7. **No deferrals.** "We will not defer anything." Quality must be resolved on the current branch, not kicked down the road.
8. **No bypasses.** He explicitly forbids `--no-verify` and asks the agent to confirm when he sees it used.

## Tool/stack preferences

- **Python:** mypy strict, ruff, pytest, pytest-cov, pytest-benchmark
- **TypeScript:** pnpm, ESLint, Jest, tsc --noEmit, esbuild
- **CI:** GitHub Actions (ci.yml, demo.yml, ai-review.yml, release.yml)
- **Hooks:** husky + custom Python orchestrator (`scripts/run_repo_hook.py`)
- **Quality files:** `invariants.md`, `CONSTITUTION.md`, `.suppression-baseline.json`, `.any-type-baseline.json`
- **Spec system:** `/speckit.specify`, `/speckit.plan`, `/speckit.implement` commands
- **Multi-agent:** TeamCreate with named roles (devops, qa, fullstack, architect, devex, Devil's Advocate)
- **Slash commands used:** `/plan`, `/review`, `/speckit.specify`, `/speckit.plan`, `/speckit.implement`

## What he never tolerates

- Inline suppressions (`# type: ignore`, `# noqa`, `@ts-ignore`, `istanbul ignore`) without evidence
- `any` types in production source (ratcheted to 0 in `src/`)
- Broad `except Exception` without justification
- CI/local parity gaps
- Agent claiming victory before the Devil's Advocate signs off
- Agent making code changes without approval during plan/review mode
- Agent re-raising dismissed scope ("we will not defer anything")
