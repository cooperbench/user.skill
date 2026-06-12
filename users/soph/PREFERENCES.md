# Preferences

## Pushback distribution

| Type | Rate |
|------|------|
| correction | 52.4% |
| non_pushback | 37.9% |
| failure_report | 9.0% |
| rejection | 0.5% |
| takeover | 0.2% |

Over half of follow-ups are corrections. Soph reads agent output carefully and points out errors specifically.

## What triggers corrections

- Agent uses wrong contributor names or misses codeowners (corrects with specific names)
- Agent reviews the wrong diff or reads the wrong state ("ok, I had a wrong state")
- Agent over-engineers or adds unnecessary code ("no wait, we should not use ENTIRE_TEST_TTY=0 but...")
- Agent leaves a mismatched naming convention ("yeah I feel the prefix is redundant")
- Agent references the wrong branch or file ("can you check the changes in the local branch again?")
- Agent's analysis contradicts what Soph sees in the code ("not sure your analysis is correct, because the old code did not get to askConfirmTTY, right?")

## What satisfies them

- Clean execution of the stated plan with all steps completed
- Agent that checks its own work before reporting done
- Grouped, meaningful commits ("can we group the changes into meaningful commits?")
- Lint and test passing (`mise run fmt && mise run lint && mise run test:ci`)
- Concise answers to "what does X do?" style questions — not essays

## Workflow habits

- **Planning first for big tasks**: often enters plan mode, writes a structured plan, then pastes "Implement the following plan: …" as a session opener.
- **Test-driven mindset**: frequently asks "are there tests for this?" or "can we add tests for this?" especially after changes to critical paths.
- **Verification via test repo**: uses a local test repo skill (`/Users/soph/Work/entire/test/…`) to validate end-to-end behavior.
- **Lint-gated**: runs `mise run lint` after changes; if it fails, pastes the error and asks the agent to fix.
- **Commit cadence**: prefers meaningful grouped commits, not one giant commit; delegates commit creation to the agent.
- **PR reviews**: often asks agent to review a PR by URL or local branch; uses `/workflows:review` slash command.
- **Prefers results over explanations**: asks "what does X do?" but follows up with actions, not more discussion. Doesn't want long summaries.

## Stack and tool preferences visible in prompts

- Go (the codebase), `mise` as task runner (`mise run lint`, `mise run test:ci`, `mise run fmt`)
- `go-git` for git operations (prefers it over shell `git` in library code)
- Structured logging via `logging.Info(logCtx, ...)` not `fmt.Fprintf(os.Stderr, ...)`
- GitHub Actions for CI; `gh` CLI for PR interactions
- Claude Code as primary agent; Gemini CLI and OpenCode as secondary agents
- Neovim (LazyVim) — visible in a request to add `sindrets/diffview.nvim`
