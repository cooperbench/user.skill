# Preferences — vaayne

## Pushback distribution

| Type | Rate |
|---|---|
| Correction | 46.9% |
| Non-pushback (acceptance) | 42.0% |
| Takeover | 7.4% |
| Failure report | 2.5% |
| Rejection | 1.2% |

Corrections dominate — nearly half of all mid-session prompts redirect the agent.

## What triggers correction

- Agent omits something vaayne considers obvious ("agents.md is needed. so keep sync skills and sync agentsmd")
- Agent uses wrong flag or approach ("use `--append-system-prompt` not replace exist system prompt")
- Agent adds backward-compatibility work vaayne didn't ask for ("no backward compat")
- Agent leaves behind old sync tasks that are now superseded ("remove them, pi-delegate skill handles it now")
- Agent misreads a count ("implement the three improvements, i think there are 4")
- Agent adds hardcoded paths vaayne wants read from env ("do not hardcode `~/.anna/config.yaml` there is envs for this")
- Agent adds a comparison/marketing section vaayne didn't want ("remove comparison sestions")
- Agent doesn't commit when vaayne expects it to ("need commit too")

## What triggers a takeover (commit without explicit instruction to commit)

Takeovers happen when the agent summarizes a completed task without committing; vaayne responds with a single imperative: "commit this", "commit", "commit this and create a PR".

## What satisfies (non-pushback acceptance)

- "yes"
- "yes, go ahead"
- "go ahead."
- "ok, let's test the deligate with a review agent to review the new skill"
- "looks good, commit"

## Workflow habits

1. **Explore / plan first**: Frequently opens with "explore and make a plan", "what's your plan", "plan again", "give me a plan" before any implementation
2. **Approve the plan**: Approves with "yes, go ahead" or "go ahead." — rarely modifies the plan in the same message
3. **Iterate corrections**: Sends short corrections one at a time until the implementation matches intent
4. **Commit frequently**: Wants commits after every coherent chunk of work; issues "commit this" / "commit" / "commit and push" as separate messages
5. **Delegate to external models for review**: Uses `/pi-delegate use openai-codex gpt-5.4 thinking high to review again` to get a second opinion, then incorporates findings as corrections
6. **Interrupt rather than wait**: Hits interrupt when the agent is going the wrong direction, then restates the goal

## Tool and stack preferences

- **Go** for the core (anna is a Go binary)
- **Atlas** for database migrations (not hardcoded Go migrations)
- **QuickJS / Wazero** for embedded JS runtime (CGO-free)
- **Caddy-style blank-import pattern** for Go plugins
- **rsync** for syncing skill files across agent directories
- **gh CLI** for GitHub operations
- **mise.toml** as task runner
- **specs-dev** for writing implementation plans ("use specs-dev")
- **No backward compatibility**: explicitly rejects compat shims

## Testing attitude

- Tests are an afterthought — only 2.4% of prompts are test intent
- Coverage requested reactively ("Total coverage: 49.1% cause CI failed, can you add more uts?")
- Not test-driven; tests added after the fact

## Explanation preference

- Does not ask for explanations of what the agent did
- Does not acknowledge summaries; moves directly to the next task or correction
- When asking "what's the issue", expects a short answer followed by a fix, not a long diagnosis
