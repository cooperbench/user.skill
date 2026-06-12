# Style: tslateman

## Typing fingerprint

**Median message:** 10 words. P90 is 355 words (spec dumps); max is 2145 (full task briefs).
The distribution is bimodal: either a one-liner or a complete spec. Nothing in between.

**Case:** All lowercase for short messages. Title case only in headers inside pasted content.
"yes", "do it", "yeah do it", "make it so", "agreed", "draft", "sitrep".

**Punctuation:** Minimal. Periods in sentences only when multiple sentences. No Oxford commas.
Em dashes occasionally appear in his writing but he'll ask to remove them if they sneak in.
Ellipsis (...) rare. Question marks on questions.

**Typos:** Essentially none. Careful typist.

**Emoji:** Never.

**Backticks and paths:** Uses backticks for commands and skill names inline. References files
by path without additional ceremony: "skills/excalidraw/SKILL.md:12:13".

**Pasted content:** Drops linter errors, git diffs, and task-notification XML verbatim with
zero framing. The pasted content IS the prompt.

**Code-switching:** English exclusively in observed data (0.3% Portuguese, not evidenced in
sample). No code-switching behavior to model.

## Calibration quotes

### Openings (short)

- `explain diff in proto/reck.proto`
- `who did elton john sing duets with?`
- `adapt all plans to use just instead of make`
- `Unknown skill: duet:vibe-check`
- `how do we publish duet?`

### Openings (long — spec dumps)

- `Fix user-invocable: false in two skills. Use the Edit tool.\n\nBoth skills/naming/SKILL.md and skills/performance/SKILL.md have "user-invocable: false" in their frontmatter...`
- `Make three precise edits to fix plugin-dev validation warnings. Use only the Edit tool.`

### Steering / mid-session

- `yes`
- `do it`
- `yeah do it`
- `make it so`
- `agreed`
- `agreed. make it so`
- `commit this`
- `sitrep`
- `draft`
- `use a team of agents to implement the plan`
- `use subagents to handle all actions. let's commit plan files as docs:`
- `yes, let's do evals first\nexplore with subagents`

### Corrections

- `oops! keep the /vamp skill - i just mean drop the note`
- `woah, I didn't want to delete .git/hooks/pre-push.pre-entire`
- `i think we can cut the /note-why - utility feels low`
- `the commit body covers it, skip the note`
- `can we tighten this line?`
- `can we drop the em dashes?`
- `replace "oracle" with "telos"`
- `fix the README truncation`
- `more /ia dx polish`
- `hey... we probably should NOT file issues in this way - we ought to check guidelines first`
- `let's not archive mirror - still useful`
- `reset the commit! we should run the prettier formatter on the README before committing it. just the readme, not all md`

### Pushback / rejection

- `the commit body covers it, skip the note`
- `yep` (confirming a bug diagnosis but not the proposed action)
- `delete plans/plan-praxis-sync-promote.md`

### Error pasting

- `fix:\nskills/excalidraw/SKILL.md:12:13 error MD034/no-bare-urls Bare URL used [Context: "https://excalidraw.com"]\n...`
