[DEVELOPER]: can you updaet the single select in the enable agent selection window to be a multi-select?

[AGENT]: Let me find the relevant code for the enable command's agent selection.

[AGENT]: Now I can see the code. The `detectOrSelectAgent` function at line 515 uses `huh.NewSelect[string]()` for single agent selection. I need to change it to `huh.NewMultiSelect[string]()` and update the callers to handle multiple agents. Let me check the tests and how `huh.NewMultiSelect` works.

[AGENT]: Let me check the agent detection and list APIs.

[AGENT]: Now I have a clear picture. I need to: 1. Change `detectOrSelectAgent` to return `[]agent.Agent` 2. Change the `huh.NewSelect` to `huh.NewMultiSelect` in the interactive path 3. Update both callers to iterate over the returned agents 4. Update tests

[AGENT]: Now update the `runEnableWithStrategy` caller to handle the slice:

[AGENT]: Now update the `runEnableInteractive` caller:

[AGENT]: Now update the tests to handle the new `[]agent.Agent` return type:

[AGENT]: Now let me run the tests to make sure everything compiles and passes:

[AGENT]: All tests pass. Let me also check if there are any integration tests that reference `detectOrSelectAgent`:

[AGENT]: Only in the files we already updated. Let me run the full test suite to confirm nothing is broken:

[AGENT]: All tests pass including integration tests. Here's a summary of the changes: **`cmd/entire/cli/setup.go`:** - Changed `detectOrSelectAgent` return type from `(agent.Agent, error)` to `([]agent.Agent, error)` - Replaced `huh.NewSelect[string]()` with `huh.NewMultiSelect[string]()` and updated the title to "Which agents are you using?" - The value binding now uses `[]string` instead of `string` - Added validation that at least one agent is selected - Updated the "Selected agents:" output to join multiple agent names with commas - Auto-detect and no-TTY fallback paths return single-element slices for backwards compatibility - Updated both callers (`runEnableInteractive`, `runEnableWithStrategy`) to iterate over the returned agents slice when setting up hooks **`cmd/entire/cli/setup_test.go`:** - Updated all `TestDetectOrSelectAgent_*` tests to handle the `[]agent.Agent` return type, checking `len(agents)` and accessing `agents[0]` instead of a single `ag`

[DEVELOPER]: hwo do i select the agents in the multi select when im in the terminal? i would epect it's with the enter button>?

[AGENT]: With `huh`'s multi-select in the terminal: - **Space** — toggles an item on/off (checks/unchecks it) - **Enter** — confirms your selection and moves on - **Arrow keys** (or j/k) — navigate between items So the flow is: navigate to an agent, press Space to select it, navigate to another if you want, press Space again, then press Enter to confirm.

[DEVELOPER]: add some text to tell the user to use space to select it.

[AGENT]: Done. Added a `.Description("Use space to select, enter to confirm.")` to the multi-select prompt so users know the controls.