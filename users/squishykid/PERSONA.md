# Persona — squishykid

## Background (inferred)

- **Role:** Founder or core maintainer of `entireio/cli`, a CLI tool that wraps AI coding agents (Claude Code, Gemini CLI, Cursor) with git session tracking. (inferred from deep familiarity with every subsystem and the pattern of PR-driven work)
- **Seniority:** Senior / principal-level. Understands Go interfaces, exported vs. unexported symbols, test helper sharing, and strategic dead-code removal without being told. (inferred)
- **Domain expertise:** Git internals (`go-git`, plumbing layer, `core.hooksPath`), hook manager ecosystems (Husky, Lefthook, pre-commit, Overcommit), AI agent hook protocols. Clearly the architect of this system.

## Attitude toward the agent

- **Trusting but vigilant.** Accepts code output without re-reading it line by line — but catches structural mistakes: a symbol that should be unexported, a duplicate test helper, a file that was missed. Corrections are immediate and short.
- **Not interested in summaries.** When the agent delivers a bulleted "Here's what I changed" recap, squishykid ignores it and sends the next command. Never rewards summaries with acknowledgment.
- **Delegates execution, retains design authority.** Will hand the agent a 600-word plan and say "implement this" — but will redirect mid-execution if the agent makes a structural choice squishykid disagrees with ("rather than modifying initializeSession for both files, could we call IsEmptyRepository inside OpenRepository()?").
- **Comfortable interrupting.** Kills tool use mid-flight and reissues the prompt if things go sideways.

## Tone

- All lowercase. No punctuation on short messages. No greetings or closings.
- Minimal hedging. "lets remove it", not "maybe we should consider removing it".
- Questions are a soft correction: "why is HookManager exported?" means "make it unexported".
- Pastes raw reference data (spec tables, config file lists) without wrapping text when correcting the agent's incomplete implementation.
