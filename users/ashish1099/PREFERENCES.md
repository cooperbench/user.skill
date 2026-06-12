# Preferences: ashish1099

## Pushback distribution

- **non_pushback: 70%** — most of the time the agent's output is accepted without comment.
- **takeover: 20%** — agent summary triggers a direct override instruction.
- **failure_report: 10%** — agent claims success but runtime error surfaces.

## What triggers corrections

### Takeover
Both observed takeovers happen at the same moment: the agent finishes a task and produces a
summary. ashish1099 does not engage with the summary; they respond with a git command, taking
back control of the workflow. The correction is not about code quality — it is about the agent
assuming it should decide what happens next.

Pattern: *agent produces summary → ashish1099 issues terse git override*
> agent: "All tests pass. Here's a summary of the changes: …"
> user: "commit this and its already in staged"

The "its already in staged" clause signals the agent was about to run `git add` — ashish1099
pre-empts it.

### Failure report
When the agent declares success but the runtime disagrees, ashish1099 pastes the exact error
string with no preamble or diagnosis. No "I got this error" — just the error. The expectation
is that the agent will read it and fix the root cause.
> "tag sync v1.4.4: checkout tag v1.4.4: reset v1.4.4: invalid reset option: object not found"

### Interrupt
When a tool call diverges from intent mid-execution, they cancel it immediately rather than
letting it complete and correcting afterward.

## What satisfies them

- Agent executes the pre-written plan without adding unrequested features or abstractions.
- Tests pass, build passes — that is the stated acceptance criterion in every spec.
- No unsolicited design changes to the plan.

## Workflow habits

- **Plan-before-session**: architectural decisions are made before the conversation starts.
  The spec arrives fully formed; the agent is an executor, not a designer.
- **No explanation requests**: zero prompts asking "how does X work" (except one casual
  doc/location question). They already know; they are confirming or fixing.
- **Commit-driven**: git commits are a recurring concern (33% git intent). They dictate commit
  timing precisely and correct staging state when the agent would get it wrong.
- **Short sessions**: median 4 turns, ~13 minutes. Get in, execute, commit, done.
- **Minimal back-and-forth**: sessions do not involve iterative refinement through conversation;
  the spec is the contract.

## Stack/tool preferences

- Go (all sessions)
- go-git library (referenced by specific method names in specs)
- GitHub issues for bug tracking (drops issue URL mid-session)
- Claude Code as the agent (100% of sessions)
- Directory-based YAML config, Puppet/OpenVox environment management
