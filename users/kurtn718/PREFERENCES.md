# Preferences — kurtn718

## What triggers correction (35% of prompts)

1. **Agent proposes work that already exists**: The single most common correction trigger. When an agent plans to implement something already in the codebase, kurtn718 cuts in immediately.
   - "We did implement something already"
   - "audiocapturekit is our repo - we have it locally we can make a change to it"

2. **Agent gives too much process instead of just doing it**: When the agent explains options or asks which approach rather than acting.
   - "ok can you do that for me" (after agent listed two options)
   - "that seams like a lot - could you read what we have and then use new bd commands to populate the issues"

3. **Pre-existing bugs dismissed by agent**: Kurtn718 insists on fixing issues even if the agent says they're pre-existing.
   - "even if it's preexisting we need to fix"

4. **Linting/build not verified before commit**: Agent declares success without running lint or tests.
   - "Commit and pr but does lint and tests pass" (after agent said "ready to commit")
   - "ummm...we need to fix now" (on lint failure the agent missed)

5. **Wrong explanation when he knows the code**: When the agent misidentifies what's possible in their own repos.
   - "ok i thought the api had an option where we could request the PCM files"
   - "we do have 104.2 it's just that you have to request it with the PCM format"

6. **Renaming/branding missed**: When Xcode target still says "PabloCompanion" after a branding pass.
   - "for whatever reason the menubar still says PabloCompanion"

## What triggers failure reports (8.3% of prompts)

Raw error output dropped with minimal commentary:
- "codeql fails"
- "build error"
- "more progress i guess - Failed to load patients: Pablo.PabloError.JsonParse(message: \"error decoding response body\")"
- "it's still failing on main CI - take a close look at all of the erros - reason if you have to"
- Pastes full cmake/Xcode/Rust build output verbatim

## What satisfies kurtn718

- Agent delivers working code and says "ready to commit" → kurtn718 types "push on main" or "Let's commit and close out any related beads issue and then push a Pr"
- Agent explains something clearly → "yes please" or "yes let's do it"
- Partial progress with something still broken → "progress :-) [paste error]"

## Workflow habits

- **Planning before execution**: for big epics, uses `/epic` or `/work` commands to spin up multi-agent teams. For small tasks, types directly.
- **Beads (bd) for issue tracking**: keeps PABLO-D-xxx tickets updated; expects agents to close tickets when work is done.
- **Worktrees**: uses git worktrees per ticket; expects agents to create them with `bd`-aware names.
- **Commits frequently**: asks to commit and push after each meaningful chunk of work. Doesn't batch across multiple sessions.
- **Force push when needed**: comfortable with force-push on feature branches, not precious about git history cleanliness mid-sprint.
- **Tests are a checkpoint, not a driver**: doesn't ask for tests upfront but checks "does everything build?" and "Did you lint the code" before merge.
- **Doesn't ask for explanations by default**: wants results. When asking for explanation, uses "whats" / "how does this" style questions.
- **No planning docs**: doesn't want design docs written out; wants agents to read existing code and act.

## Tool/stack preferences

- **Agent orchestration**: runs named agent teams (coder-swift-models, coder-rust, reviewer, hipaa-reviewer, planner, code-explorer).
- **Custom skills**: uses `/work`, `/continue`, `/epic` slash commands.
- **CI**: GitHub Actions; tracks CodeQL, SwiftLint strict, xcodebuild.
- **Issue tracker**: Beads (`bd`), with PABLO-D-xxx IDs.
- **Firebase**: used for auth; aware of token refresh, Keychain storage, API key security.
- **11labs**: used for e2e test audio generation.
