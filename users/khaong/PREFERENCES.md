# Preferences: khaong

## What khaong Corrects (39.9% of turns)

Corrections are the dominant pushback type. Patterns:

**Scope creep / wrong frame.** Agent jumps to a cross-worktree explanation when the issue is local to worktree 2: "so let's not jump to cross-worktree explanations just yet." Agent assumes a hook *caused* a bug when it only *revealed* it: "I mean, we _see_ it on the stop hook; it doesn't mean the stop hook caused it."

**Factual assumptions stated as certain.** Agent says "X writes to the index" without verifying: "are you sure?" Agent's explanation is internally consistent but khaong has contradicting live evidence: "I challenge this if there is any log flushing behaviour happening."

**Missing specification that khaong thought was obvious.** "sorry, I didn't specify earlier but..." — khaong will catch this and supply the missing detail mid-session rather than up front.

**Design disagreements expressed bluntly.** "that double constant definition and mapping in registry is yuck :(", "can we remove these magic numbers?", "move the message up just before the file list?"

**Workflow deviations.** Agent attached a document to the project instead of the issue directly: "not as a comment, but as a document attached to the issue directly. you've attached it to the project..."

**Agent got ahead of itself.** Agent starts implementing before the plan is agreed: "let's go with A" (forcing a choice before proceeding).

## What khaong Rejects (1.2% of turns)

Rare but decisive. Examples:
- "nah let's roll back, they don't really need to exist in the future state"
- "no don't set it, let's see if it keeps happening"
- "push" (terse rejection of agent stopping short after a rebase, just wants the action done)

## What khaong Rewards (non-pushback = 51.6%)

- Agent executes precisely, no over-explanation, just results.
- Agent takes initiative on follow-through (commits, pushes, creates PRs) without being asked for every step.
- Agent follows a skill/plan invocation exactly as written.
- Agent surfaces the right question rather than guessing.

## Workflow Habits

**Plan-first for big features.** Large implementation sessions start with a written plan in `docs/plans/`. khaong references these by path: "have a look at docs/plans/2026-02-06-session-phase-state-machine.md".

**TDD when explicitly directed.** "Write tests first (TDD). Run mise run fmt && mise run lint && mise run test:ci before considering complete." This appears in spec dumps but not in casual sessions.

**Preflight before shipping.** "run our preflight fmt, lint, test:ci please" — consistent CI gate before committing.

**Stacked PR workflow.** Works on feature branches off parent branches (e.g., `alex/ent-221-phase-aware-git-hooks`), regularly rebases, creates stacked PRs against parent branches rather than main.

**Linear-driven.** Starts sessions by referencing a Linear ticket. Logs new issues to Linear mid-session ("log a linear issue in Project:Troy with this observation").

**Lets agent drive commits.** "commit and push", "commit, push, create draft PR" — rarely commits manually except for takeover situations.

**Asks questions rather than specifying:** Frequently asks "is there a reason X?" or "are there any tests that do Y?" to get the agent's read before deciding.

**Subagent workflow.** Invokes Task-based subagent reviewers: "can we fire off an explore agent before starting work to look for related things?" Monitors background task output.

## Tool/Stack Preferences

- Go (primary language)
- `mise` for task running (`mise run fmt`, `mise run lint`, `mise run test:ci`)
- GitHub CLI (`gh`) for PR management
- Linear for issue tracking (Project: Troy)
- `gotestsum` for test output
- tmux for E2E interactive test sessions
- Slash commands / plugin skills for structured workflows (`/superpowers:brainstorm`, `/review`, `/debug-e2e`)
- Claude Code (93%), occasionally Agent mode (7%)
