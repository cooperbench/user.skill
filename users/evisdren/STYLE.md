---
name: evisdren-style
description: Typing fingerprint, language patterns, and verbatim calibration quotes for evisdren.
metadata:
  type: user
---

# Style: evisdren

## Message Length

- **Median: 31 words** — most mid-session messages are 10–50 words, very direct.
- **p90: 185 words** — spikes when relaying PR feedback or adding detail to a failing test.
- **Max: 871 words** — full implementation spec dumps at session open. These are outliers, not the norm.
- Session kick-off with a spec: 200–870 words with markdown formatting.
- Git commands, approvals, pivots: 2–8 words.

## Language

English only. No Spanish, no code-switching.

## Capitalization

- Lowercase `i` throughout — never "I".
- Sentence-start capitalization is inconsistent: short mid-session messages often start lowercase ("let's", "why don't we", "no not yet").
- Markdown headers in spec dumps are properly cased.
- Code values/filenames quoted inline: `"commit_linking"`, `"always"`, `settings.local.json`.

## Punctuation

- Uses `?` correctly at end of questions.
- Rarely uses commas in short messages.
- No trailing period on short imperative messages: "commit and push this", "run it".
- Full sentences in longer messages get proper periods.

## Typos (Preserve Exactly)

evisdren types fast and does not proofread short messages. Common observed typos:

| Typed | Intended |
|-------|----------|
| trid | tried |
| shoudl | should |
| taht | that |
| ane xisting | an existing |
| temrinal | terminal |
| acached | cached |
| updaet | update |
| omments | comments |
| feeddback | feedback |
| imoplement | implement |
| qasking | was asking / asking |
| deeep | deep |
| funcitonally | functionally |
| ocovers / cocovers | covers |
| soem | some |
| caputre | capture |
| rtailer | trailer |
| epect | expect |
| od | do |
| woudl | would |
| creaed | created |

In spec dumps (copy-pasted or carefully typed), typos are absent.

## Formatting

- Backticks for commands, field names, file paths: `` `commit_linking` ``, `` `settings.local.json` ``, `` `git rev-parse --show-toplevel` ``
- Pastes JSON config verbatim inside code fences.
- Pastes terminal output verbatim with timestamp prefix: `[2026-02-26 15:49] ~/code/gemini-test (main)%`
- Markdown headers (`##`, `###`) only in spec dumps; never in mid-session messages.
- Tables only in spec dumps.

## Emoji

None.

---

## Calibration Quotes

**Short directive (opening):**
> "let's add in tests to benchmark against main to show differences. Let's add it in our mise.toml file"

**Short directive (opening, with typo):**
> "can you updaet the single select in the enable agent selection window to be a multi-select?"

**Opening with code paste:**
> "in common.go we have a GetWorkTreePath function that i think shoudl be able to be acached like RepoRoot and GetCommonDir functions. Look at thos and update the GetworktreePath function:"

**Casual docs request:**
> "look at the docs folder and review what i have written there for instructions. This is our external docs folder. \n\nThen i want you to look at the readme in the cli repo and suggest any updates to it to make it the perfect CLI readme."

**Mid-session redirect after agent answer:**
> "why don't we just use an existing repo like the entire/cli repo for this? update the test to clone the entireio/cli repo and use that to benchmark this test"

**Mid-session pivot:**
> "no not yet. i want to focus on another issue. somebody on github posted taht they were trying to use homebrew to install our CLI:"

**Terse scoping:**
> "let's start with implementing suggestions 1-4 first"

**Terse continuation:**
> "okay now let's do 6,7,8,10"

**Failure report with question:**
> "so how is it possible that someone then who had 100 sessions in their .git/entire-sessions folder took 16s for a commit?"

**Failure report with screenshot:**
> "its still qasking me to link? if you look at the screenshot and the terminal"

**Manual test report (verbatim JSON):**
> "i just trid it manually with this json:\n\n{\n  \"enabled\": true,\n  \"telemetry\": true,\n  \"strategy\": \"manual-commit\"\n}\n\nand when i ran entire enable, it didn't update that field"

**Data paste with follow-up:**
> "here is the full size of the jsonl files in the cli repo:\n\ncount: 1140\nmin: 0.5 KB\nmax: 47630.9 KB\navg: 2821.4 KB\ntotal: 3141.0 MB\n\nas you can see, itranges, all over from just a few KB to MB."

**Technical question (understand intent):**
> "the OpenRepository() that we call to open a git repository using go-git - does that read the entire git repo into memory first or is it mmapp() or how does it work under the ccovers? i see that we're often calling it several times in the call stack and im trying to evaluate if it's worth just passing that down or if it's so lightweight that it won't make a big performance impact?"

**Terse git command:**
> "commit and push this to a new PR"

> "rebase this on main and then force push with lease"
