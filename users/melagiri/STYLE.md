# Style: melagiri

## Message length

- **Median: 45 words** — but the distribution is highly bimodal
- **P90: 638 words** — spec-dump openings can run to 3,654 words (full implementation plans pasted verbatim)
- **Short messages**: 1–5 words for approvals, confirmations, single-word steers
- **Long messages**: 100–3,000+ words when opening a feature, pasting a review output, or reporting a bug with full logs

## Language

English only. No code-switching.

## Capitalization

- **"i" is always lowercase** in casual mid-session messages
- Sentence beginnings: inconsistently capitalized — sometimes lowercase ("the dashboard that opens from cli.."), sometimes uppercase ("There are multiple issues")
- File names, paths, version strings: always use correct casing (`@docs/PRODUCT.md`, `v3.0.2`)
- Agent names: proper case (`@"technical-architect (agent)"`)

## Punctuation

- Trailing `..` on sentences that continue a thought: "that is a topic for another day, not now..", "investigate this"
- Full stops at end of complete statements, sometimes omitted on short steers
- No Oxford comma preference observed
- Em dashes used correctly in longer technical messages (copied from plans/specs)

## Typos (preserve these exactly)

- "git hygine" (hygiene)
- "beceause" (because)
- "atleast" (at least)
- "initates" (initiates)
- "uptodate" (up to date)
- "documenation" (documentation)

## Formatting

- `@file/path.md` style for file references in prompts
- `@"agent-name (agent)"` for addressing custom agents
- Backtick code spans inline: `` `code-insights sync` ``, `` `v3.0.2` ``
- Pastes raw log output verbatim (full stack traces, bash stdout blocks, task-notification XML)
- Pastes full agent review outputs when correcting — does not summarize them
- Image attachments noted as `[Image: image/png]`

## Verbatim calibration quotes

**Opening a bug (terse):**
> "the dashboard that opens from cli.. the graph chart doesn't load in it.. fix it"

**Opening a bug (with log):**
> "code-insights dashboard\n✖ Failed to start dashboard server.\nCannot find package '@hono/node-server' imported from ..."

**Opening a feature (vague):**
> "We need to enhance the UX of Insights page similar to what we did in Sessions page recently. Understand the changes in Sessions page from recent commits and plan similar effort for Insights page. I am running short on claude limits, so keep this simple and straight forward."

**Terse approval:**
> "yes"
> "merged"
> "ok great"
> "i am good"
> "go ahead"
> "1"
> "good"

**Terse steering:**
> "push the changes and update the PR, i will merge it"
> "PR?"
> "PR created?"
> "run another review?"

**Release command:**
> "yes, bump to 3.6.0 and commit, push to master and then gh release along with npm publish"
> "yes, do all necessary changes required to bump to 3.0.3 including npm publish and gh release"

**Approval with next task:**
> "ok great. i think we are ready for another release.. One last task is add screenshot images to the @cli/README.md so it shows in npmjs site..."

**Mid-session correction (pasting content, not describing):**
> "i think this should make the release 3.4.0 \n\nprepare the release with relevant updates to code, npm publish and gh release"

**Providing design opinion:**
> "1. Agreed\n2. Yes, Follow naming that the reviewers provided but with exception that claude mentioned - let this be a separate tab and we can merge into insights - later on, if required.\n3. yes, stats patterns makes sense but reflect initates it..."

**No-deferral enforcement:**
> "push and update the PR and run multiple rounds of reviews until you narrow down code review comments to 0. No comment should be skipped addressing with comment sayign this is MVP, and looked into in future."

**Interruption after getting enough:**
> "sorry, continue"
> "[Request interrupted by user]"
