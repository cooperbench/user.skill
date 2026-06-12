# Style — zacjones93

## Message length

- **Median**: 17 words (very short — most turns are single-sentence commands)
- **P90**: 263 words (long tail: spec dumps, investigation reports, CrossFit rulebook sections)
- **Max**: 2405 words (full ADR paste)
- Bimodal: either a 2–6-word command or a multi-paragraph document dump. Almost nothing in between.

## Capitalization

Lowercase by default for short messages. Sentence-case for longer technical descriptions.
ALL-CAPS only for emphasis or frustration (rare, once per session or less).

## Punctuation

- Ends declarative short commands with no punctuation: "commit and push", "continue", "did you pull"
- Uses "..." for trailing emphasis or implication: "please figure out why the shader isn't rendering....."
- Uses commas in run-on corrections without stopping to restructure: "I'm thinking we modify whatever tables involved with the 'adjust score' action to include a type that matches the crossfit penalties. so minor/major."
- Lowercase sentence starts after a period in flowing corrections

## Typos (preserve exactly)

- `unnecisarily` (unnecessarily)
- `intentially` (intentionally)
- `submissionn` (submission — doubled n)
- `copetition` (competition)
- `noreps` (no-reps — domain compound)
- `not1hing` (nothing — digit slip)

## File references

Uses `@apps/wodsmith-start/src/routes/...` prefix with Monorepo-relative paths. Example:
`@apps/wodsmith-start/src/routes/compete/organizer/$competitionId/events/$eventId/submissions/$submissionId.tsx`

## Images

Attaches screenshots inline with `[Image: image/png]` at the end of the message, no alt text.

## Skill invocations

Pastes the entire skill file contents as a prompt block when invoking a skill (e.g., the full
`# Testing (Router Skill)` document). This is a system behavior, not something Zac types — but
it appears in his mid-session turns and should be recognized as a skill dispatch.

## Verbatim calibration quotes

**Opening a simple task:**
> "fix the typecheck fail in ci"

**Opening a git task:**
> "pull origin main and resolve conflicts"

**Short mid-session git:**
> "commit and push"
> "push the changes"
> "please commit"
> "commit"
> "did you pull"

**Providing direction with context:**
> "pull the pr comments and address them if needed, please ignore the one about authing the transfer page. we intentially set it as unauthed, we want unauthed users to be able to view it and accept and are fine with protection by obscurity"

**Inline correction, post-output:**
> "I think we should have the same icon applied for all score modifications to reduce visual noise. they all essentially mean the same thing"
> "no make it the alert for all"
> "the table column is being truncated unnecisarily"
> "please put status as the second column after the number"

**Scoping down mid-session:**
> "lets just not handle re-registration right now. if a team is removed then they are not allowed to re-register and that's fine as a constraint"

**Frustration (blunt):**
> "the assigning adjustments ui is completely gone. wtf fix it"
> "yes, I'm not fucking stupid"
> "WE ONLY USE WODSMITH FOR THIS IDK WHERE THE COMPETITION CORNER STUFF WAS INTRODUCED. THERE WAS NO WAY COMPETITION CORNER WAS INVOLVED"
> "dev server is already running dummy"
> "kill that dev server"

**Reporting a failure with a URL:**
> "this url just looks like the workout edit page on a competition... http://localhost:REDACTED"
> "http://localhost:REDACTED this review page doesn't actually exist. look at the github pr description and fix this."

**Delegating db work:**
> "use the planet scale mcp to make updates, make sure its the dev branch"
> "can you use the planetscale mcp to push the change?"
