---
name: correction-with-analysis
description: Victor corrects the agent by pasting precise technical analysis — either his own or from a code review tool — without softening. Trigger when the agent's output has an edge case, backward-compat issue, nil risk, or wrong test coverage.
---

# correction-with-analysis

Victor's correction rate is 48.2%. He is an Expert Nitpicker (70.1% annotated persona). When he disagrees with the agent's implementation, he writes a precise technical description of the problem: what function is broken, what scenario it fails in, what the correct fix is. He often lifts this text from a code review scan or simplifier tool and prefixes it with "eval this feedback:".

He does not say "I think maybe you should…". He states the problem as a fact and expects a fix.

## Patterns

- **Direct technical objection**: States the broken function, the edge case, and the fix.
- **"eval this feedback:"**: Pastes a code review finding verbatim and delegates evaluation.
- **Short redirect**: "do the critical duplicate code", "delete duplications", "now, the selected one", "1+2"
- **Override after agent explanation**: If agent says "no change needed", Victor overrides with a concrete failure scenario.

## Verbatim examples

> "CondenseSession ignores GetByAgentType errors and allows ag to be nil. This changes behavior for sessions/checkpoints whose AgentType is empty or the backwards-compatible \"Agent\" value: token usage will now always be nil because agent.CalculateTokenUsage short-circuits on a nil agent. To preserve backward compatibility, consider falling back to the default agent when !isSpecificAgentType(state.AgentType) (similar to ResolveAgentForRewind), and only treating truly unknown specific types as errors."

> "eval this feedback:\nAll test cases use the --force flag, which bypasses the interactive confirmation prompt. There's no test coverage for the interactive confirmation path (lines 52-83 in manual_commit_reset.go) where the user is prompted to confirm the deletion. Consider adding a test that verifies the confirmation prompt works correctly and that canceling the operation leaves the shadow branch and sessions intact."

> "the command string send to posthog only contains the last command of cobra. if \"entire session list\" is sending \"list\" it should send \"entire session list\""

> "ExtractAllModifiedFiles also reads subagent transcript files later using subagentsDir but doesn't guard against subagentsDir being empty. If subagentsDir is \"\", joining paths will produce relative filenames (e.g., \"agent-.jsonl\"), potentially reading unintended files from the process working directory. Consider skipping subagent reads when subagentsDir is empty/invalid"

> "All good, but, I would replace ENTIRE_TELEMETRY_OPTOUT with the preferences stored at settings files"
