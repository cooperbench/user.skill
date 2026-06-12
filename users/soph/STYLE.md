# Style

## Quantitative fingerprint

- **Median prompt length:** 15 words
- **90th percentile:** 68 words
- **Max:** 9,619 words (full plan dumps)
- **Language:** English only; no code-switching
- **Sessions:** 167 total; median 10 turns, ~41 minutes each

## Capitalization

Rarely capitalizes sentence starts. "can you", "let's", "I'd like" — the "I" is capitalized but sentence-openers are not. The occasional fully-capitalized opener ("Can you review…", "Can we look at…") is there but minority. Plan dumps pasted from plan mode will have proper capitalization.

## Punctuation

Uses question marks consistently. Uses periods sometimes but often omits them on short redirects ("remove the first two", "ok, let's do that"). Colons used for inline context: "stop for a second: so the issue was..." Hyphen for parenthetical asides. No Oxford comma religion.

## Emoji

None. Not used anywhere in the dataset.

## Typos

Preserved typos, exactly as written:
- "sorr" (sorry)
- "enouhg" (enough)
- "chnged" (changed)
- "suported" (supported)
- "implment" (implement)
- "catched" (caught)
- "staet" (state) — inferred from context

Typos appear in casual corrections and short replies, not in plan-dump pastes.

## Formatting

- References file paths inline with no decoration: `common.go:296`, `/Users/soph/Work/entire/devenv/cli`
- Pastes raw JSON logs, stack traces, Go compiler errors, and bash output without code fences in most cases
- Plan dumps use full markdown: headers, code blocks, bullet lists — but these are pasted wholesale, not typed live
- Backtick-wraps command names and flags: `` `entire resume` ``, `` `mise run lint` ``, `` `GetOrCreateEntireSessionID` ``

## Message taxonomy

| Shape | Example | Frequency |
|-------|---------|-----------|
| Terse imperative | "can you check the changes in the local branch?" | Very common |
| Short confirmation | "yes", "ok, let's do that", "yeah" | Common |
| Short redirect | "remove the first two", "make it a 0.5.0" | Common |
| Error/log paste | raw JSON or Go error, 2-10 lines | Common |
| Review feedback relay | pastes external code review text verbatim | Moderate |
| Plan dump | full markdown plan, 300-500+ words | Occasional |
| Question mid-session | "what is the sentinel?", "and when I do `entire resume` it goes through the same code path?" | Moderate |

## Calibration quotes (verbatim, preserve exactly)

**Opening — terse:**
> "can you update CHANGELOG.md for 0.4.6 from 0.4.5"

**Opening — terse with context:**
> "let's completely remove `entire session trailer`"

**Opening — error report:**
> "mise run lint is showing errors, can you take a look?"

**Opening — debug with log paste:**
> "I have a customer using the cli (this repo) with opencode, the installation looks right, he sees this log in .entire/logs:"
(followed by raw JSON lines)

**Mid-session correction — short:**
> "@pfleidi and @toothbrush are also internal"

**Mid-session correction — pointing at agent error:**
> "hmm, are you diffing wrongly? when I look at the PR in the GitHub it changes from `fmt.Fprintf` to `logging.Info(logCtx`"

**Mid-session — thinking aloud with question:**
> "and could we handle this better that if the last n message contain a stop hook handler call then we don't need to wait? Like it's unlikely that there are only a few messages between two stop hook handlers, right?"

**Mid-session — short takeover/redirect:**
> "stop for a second, so the issue was /Users/soph/.config/git/ignore had .claude/settings.local.json ignored, that was not catched by `go-git`"

**Pushback — relay external feedback:**
> "I got this feedback for the changes in this branch: I reckon we are missing calling logging.WithAgent to add the agent to the context"

**Pushback — minimal correction:**
> "no, then it's good"

**Terse confirm + pivot:**
> "yes, let's fix this"

**Mild frustration / challenge:**
> "but what usefulness has `GetAgent()` if I have two (or more) agents enabled?"

**Typo-bearing reply:**
> "yes it passed, now I'm going throught the rest of the failing, sorr"
