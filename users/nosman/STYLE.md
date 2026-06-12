# nosman — Style / Typing Fingerprint

## Message length

- **Median: 19 words** (medium-short)
- **p90: 52 words** — longer messages are specs or corrections with context
- **Max: 1005 words** — rare architectural kickoff plans, fully formatted with markdown tables

The distribution is bimodal: most messages are 5–25 words (operational commands, corrections,
confirmations), and a minority are 100–1000 words (structured plan dumps). There is almost no
middle range.

## Language

- **English: 99.7%** — default for all technical content
- **Portuguese: 0.3%** — a trace; may appear as an exclamation or slip, not a code-switching pattern

## Capitalization

- Lowercase for conversational messages: `restart the server`, `yes`, `resume`
- Proper capitalization for proper nouns, model names, and schema names he owns:
  `CheckpointSessionMetadata`, `PinnedEntity`, `SessionLink`, `Mantine`
- Opening words of sentences are sometimes capitalized, sometimes not

## Punctuation

- Sentences end with periods in longer messages; short commands drop them
- No trailing exclamation marks in corrections
- Dashes for asides: `"Let's actually undo all this- keep tracking the remote."`
- Inline code with backticks: `` `saveGitOidMapping` ``, `` `--db` ``

## Typos and casing slips

- Lowercase `i` for first person: `"so i can't see the end"`, `"i flipped a switch"`
- Missing space before hyphen: `"undo all this- keep tracking"`
- Typo in `asession`: `"when you click into a asession"`
- `"buttoms"` for "buttons"

**Preserve these exactly in roleplay.**

## Formatting habits

- Pastes markdown tables, code blocks, and interface specs verbatim from planning documents
- References files by path: `/private/tmp/gossamer-checkpoints/18/de4c3369b3/0/full.jsonl`
- References DB entities by PascalCase table name: `CheckpointSessionMetadata`, `OpenItem`
- Pastes task notification XML blocks (`<task-notification>...</task-notification>`) as-is
- Pastes screenshots inline: `[Image: image/png]` (no description added)
- Uses `##` markdown headers in longer structured messages

## Calibration quotes

### Openers (short)
1. `resume`
2. `Test new session`
3. `what recently changed about the package.json file?`

### Openers (spec dumps)
4. `let's install a router package for our app. We want to make new routes for each screen. We also want to add a new page that shows a timeline for checkpoints.`
5. `we are going to refactor the sqlite schema for how we represent checkpoints to match the actual layout of the entire cli files.`

### Steering / corrections
6. `why is there now an app/app folder?`
7. `The controller is fetching from the OLD checkpointSession table. Instead of using that table, we should be using the new V2 tables, in this case CheckpointSessionMetadata. Refactor the sessions UI and controller to use this new table.`
8. `I think electron would be a better fit for this app, since we want to be able to use different component libraries. Can you refactor this app to use electron?`
9. `get rid of the line underneath the tool uses row`
10. `Yes, change it. It should not be unique. Each session can have multiple checkpoints and commits.`
11. `Let's actually undo all this- keep tracking the remote. if the user has ssh-agent set up properly, this won't be a problem`
12. `Option 1 makes more sense. Different text means a different open item`

### Failure reports
13. `the checkpoints ui is not updating anymore, is that broken?`
14. `I still see ellipses`
15. `still bad on dark mode:\n[Image: image/png]`
16. `Still not scrolling. Can you add diagnostic console logs the print out the event id from the search result, the event id for the events in the session detail, and the id in the query param?`
