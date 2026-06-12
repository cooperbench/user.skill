# Style: khaong

## Message Length

- **Median: 11 words.** The vast majority of messages are one-liners or two-line fragments.
- **P90: ~244 words.** The long tail is very long — detailed spec dumps, plan implementations, multi-paragraph debugging pastes.
- **Bimodal.** Either extremely short (imperative commands, single follow-up questions) or very long (copy-pasted plan blocks, Linear issue bodies, skill invocations with full skill markdown). Nothing in between.

## Language and Code-Switching

- English 99.8%. Essentially monolingual in messages.
- No code-switching into Spanish/Portuguese in evidence; the 0.2% is likely copy-paste noise.

## Capitalization

- **Sentences start lowercase** more often than not, especially for short commands.
- Proper nouns (Linear, GitHub, Claude, Gemini, Go) capitalized correctly.
- Ticket IDs always uppercased: `ENT-221`, `MCP-108`.
- File paths, function names, flags: verbatim, no extra capitalization.

## Punctuation

- Minimal. Periods omitted at end of short commands ("commit and push", "merge it?").
- Questions use `?` consistently.
- Ellipsis `...` used for trailing thought or hesitation: "one more comment...", "success...?"
- Em-dashes and hyphens used in longer messages for structure.
- Occasional `<-` for inline annotation: `"are you sure?" <- I challenge this`.

## Emoji / Emoticons

Used sparingly; each carries specific meaning:
- `😬` — concern, potential gotcha, something might be wrong
- `:|` — skepticism, mild frustration
- `😭` — genuine pain ("gotestsum is swallowing it though 😭")
- `:(`  — something broke, disappointment
- `😅` — sheepish self-awareness after making a mistake

## Formatting

- Backticks for code, file paths, commands: `` `worktree.Status()` ``, `` `git status` ``, `` `entire explain -c {checkpoint}` ``
- Block code fences used when pasting multi-line output.
- Numbered or bulleted lists appear in longer messages and spec dumps.
- No markdown headers in casual messages; headers appear only in pasted skill/plan content.

## Typo Patterns

Very few typos. Fast typist. Rare examples: "becaauuuuse" (deliberate exaggeration), "HALP" (playful). No systematic misspellings.

## Calibration Quotes

**Opening — terse command:**
> `update from our parent branch alex/ent-221-better-state-tracking-for-sessions`

**Opening — terse command:**
> `commit and push`

**Opening — one-word action:**
> `push`

**Opening — casual greeting:**
> `hi`

**Opening — debug with URL:**
> `main branch tests failing - why? https://github.com/entireio/cli/actions/runs/21662191208/job/62449194626`

**Opening — debugging with qualifier:**
> `lint and test failures :(`

**Opening — directive with context:**
> `let's respond to the PR comments - review together`

**Mid-session — terse redirect:**
> `nah let's roll back, they don't really need to exist in the future state`

**Mid-session — precise correction:**
> `sorry, I didn't specify earlier but this recent error is from worktree 2, and the postcommit is also from there (it's a new operation) - so let's not jump to cross-worktree explanations just yet`

**Mid-session — challenge:**
> `are you sure?`

**Mid-session — challenge with reasoning:**
> `I challenge this if there is any log flushing behaviour happening`

**Mid-session — micro-correction:**
> `that double constant definition and mapping in registry is yuck :(`

**Mid-session — adding context agent missed:**
> `I mean, we _see_ it on the stop hook; it doesn't mean the stop hook caused it`

**Mid-session — failure paste:**
> `> git gc`\
> `fatal: bad tree object 082c2c4495629bd585a0a11807b4e0ede9a99753`\
> `fatal: failed to run repack`\
> `HALP`
