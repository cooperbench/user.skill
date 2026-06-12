# Preferences — squishykid

## What triggers correction (41% of responses)

- **Missing a file that needs the same change.** After the agent pushes, squishykid asks: "can you check hooks_geminicli_handers.go. perhaps this needs a change too". Expects the agent to proactively cover all affected files.
- **Structural choice the agent made without asking.** The agent modifies two session files; squishykid redirects to a single shared location ("could we call IsEmptyRepository inside OpenRepository()?").
- **Exported symbol that should be unexported.** Asks "why is HookManager exported?" then follows with "let make HookManager and DetectHookManagers local (not captialised)".
- **Duplicate code/test helpers.** Points it out explicitly with file names and a description of what's duplicated, then expects the agent to consolidate.
- **PR description that's wrong.** "fix the description on pr#392" — no elaboration on what's wrong.
- **Agent commits on the wrong branch.** "move to another branch before committing".
- **Incomplete spec implementation.** Pastes the missing config file patterns verbatim from an external source (DeepWiki) when the agent's detection is incomplete.

## What satisfies them (no pushback, 53% of responses)

- Clean "commit and push" sequences with no surprises.
- PRs created with the right issue references.
- Agent answers a "is X used anywhere?" question accurately.
- Tests pass after a "fix the tests" command.
- "lets run the manual tests" → manual tests pass.

## Workflow habits

- **Plan then delegate, but retain oversight.** Opens sessions with either a full markdown plan or a one-liner. Doesn't micromanage execution steps — but corrects structural decisions.
- **Commits constantly.** After almost every meaningful change: "commit and push", "commit as 'agent: remove HookHandler'", "commit and create a pr referencing issue 424". PR creation is part of the normal flow, not a ceremony.
- **Branch hygiene.** Uses `rwr/` prefix for feature branches. Stacks PRs ("create a PR on top of 427"). Asks agent to handle branch creation.
- **Does not ask for explanations.** When the agent gives a bullet-list "Here's what changed" summary, squishykid ignores it. Only reads explanations when asking an explicit question ("what is the difference between HookSupport.GetSupportedHooks and Agent.HookNames").
- **No planning docs.** Brings pre-written plans from elsewhere; does not ask the agent to design an approach.
- **Interrupts freely.** If the agent is doing something wrong mid-execution, kills the tool call and reissues.
- **Test-aware, not test-driven.** Delegates test writing and fixing ("fix the tests please", "add a test to exercise..."). Does pause to verify test coverage before deleting code ("lets double check that we haven't lost any valuable test scenarios").
- **Stack preference:** Go, `go-git`, CLI tooling, GitHub Actions for CI. No frontend, no scripting.
