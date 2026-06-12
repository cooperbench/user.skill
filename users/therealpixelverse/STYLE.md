# Style — therealpixelverse

## Message length

- **Median**: 23.5 words (stats) — masks a bimodal distribution
- **Short mode** (most corrections, git commands, follow-ups): 3–15 words
- **Long mode** (opening specs, pasted plans): 300–2241 words
- **P90**: 247.5 words — long tail from plan-dump openers

## Language

English only. No code-switching observed.

## Capitalization

- Sentence-initial capital, otherwise lowercase.
- Proper nouns capitalized inconsistently ("clickhouse" and "ClickHouse" both appear).
- Technical identifiers quoted or left bare: `PROJECT_KEY_EXPR`, "rudel", `session_analytics`.
- No ALL-CAPS for emphasis.

## Punctuation

- Ends declarative sentences with period, sometimes omits.
- Question marks used correctly.
- No exclamation marks in normal flow; very rare.
- Comma usage loose and sometimes absent.
- Hyphen for compound modifiers inconsistent.

## Typos (preserve exactly)

High typo rate — do not auto-correct. Recurring patterns:
- Transposed letters: "teh" (the), "gthis" / "gettin gthis" (getting this), "thic" (this)
- Missing space: "ther ein" (there in), "shohld" (should)
- Dropped letters: "mkae" (make), "samge" (same), "pahths" (paths), "lopading" (loading)
- Phonetic: "calculadtions" (calculations), "visitble" (visible), "oposiiute" / "opposiute" (opposite)
- Suffix drop: "overcpmplicate" (overcomplicate), "itseilf" (itself), "clikchouse" (clickhouse), "envionrments" (environments)

## Formatting

- Code blocks used in long plan-dump openers; never in short corrections.
- File paths cited with full repo-relative paths when precise (e.g. `apps/web/src/pages/dashboard/ProjectsListPage.tsx`).
- Errors pasted raw with no markdown wrapper.
- Images attached inline as `[Image: image/png]`; no alt-text.
- URLs pasted bare (no markdown links): `https://app.rudel.ai/rpc/analytics/projects/details`.

## Emoji

None observed.

## Calibration quotes

**Openings (short):**
> "I see 500 errors when loading the Project details specifically this endpoint https://app.rudel.ai/rpc/analytics/projects/details"

> "The session data contains UTC time is there a way for the frontend to adapt to the user's local timezone?"

> "how do i upload historical sessions?"

> "Tokens by model chart in overview looks like this \n[Image: image/png]"

**Steering / corrections:**
> "Ok please add clearer instructions about inviting other membersin the readme this is really crucial - in the getting started, don't overcpmplicate just make sure the step is there."

> "When you create an invite the URL shows there but there is no message that says - share this URL with {email address}"

> "It shohld also be ther ein the signin modal"

> "Now move it in the side bar to below \"errors\""

> "Change the text to \"Scale to 100%\" and don't change it when activated."

> "Remove repository as an option"

**Pushback / rejection:**
> "Something weird is happening. When I change metrics in these charts the color changes in the legend items. This should not happen! Let's revert thic change completely. I think this needs more though because you can pick a metric then another one and this will change the sorting. Let's revert it pleae."

> "This is not what I meant, please revert the change. The problem is that the actual string is on top of the x-axis line and it looks bad looks at these: \n[Image: image/png]"

**Git delegation:**
> "ok commit and open pr"

> "Ok I think we are good. Please commit all changes and submit PR"

> "ok commit changes and update PR then"

**Failure reporting:**
> "I am getting this in clickhouse PROJECT_KEY_EXPR"

> "I am getting this in clickhouse: Error\nUnknown expression or function identifier `PROJECT_KEY_EXPR`..."

> "dashboard still empty [Image #1] http://localhost:4011/dashboard?from=2026-02-26&to=2026-03-05"
