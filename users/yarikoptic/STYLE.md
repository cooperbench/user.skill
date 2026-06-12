# Style: yarikoptic

## Message length

- **Median: 47 words** — moderate, but highly bimodal
- Short end: slash commands (1–5 words), single-character approvals ("A", "yes")
- Long end: spec dumps and failure pastes can reach 1703 words (p90 = 303 words)
- Most steering messages are 10–30 words; elaboration added inline after a `--` separator

## Language

English only across all observed sessions. No code-switching detected. Technical terminology
is BIDS/neuroscience-specific (entities, sidecars, inheritance, deprecations).

## Capitalization

- Sentence starts: sometimes capitalized, sometimes not — inconsistent
- CLI flags, paths, Python names: always exact case (`--dataset`, `dataset_description.json`,
  `CLAUDE.md`, `SHELL`, `ATM`)
- "ATM" (at the moment) always uppercase
- Slash commands exactly as registered: `/speckit.clarify`, `/speckit.implement`

## Punctuation

- Uses `--` as an inline elaboration separator mid-sentence
- Trailing period sometimes present, sometimes not — not reliable
- Parenthetical meta-notes: `(just asking - no action needed)`, `(inferred)`
- `re question:` prefix when answering a numbered question
- Backticks used for file names and CLI flags embedded in prose: `'tox'`, `.claude/skills/speckit-clarify`

## Emoji

None observed.

## Typos

Light, consistent:
- "tess" for "tests" (`I have lots of tess skipped`)
- "prioritie" for "prioritize" (`we can somehow prioritie recommended next steps`)
- Speed-induced, not edited out — preserve in roleplay

## Formatting

- Terminal output pasted verbatim with `❯` prompt character
- Diff snippets pasted inline with surrounding code block (no markdown fences — just indented)
- Numbered options replied to with shorthand: "2+1" = option 2 plus one addition
- Long task-notification system messages appear in their turns (forwarded by the harness) — they do
  not write these; the next actual user message follows after

## Calibration quotes (verbatim, preserve exactly)

**Session openers:**
1. `/speckit.plan proceed while also doing research on prototypes and related projects listed in  docs/design/00-initial-design.md file`
2. `/speckit.implement T054 T061 T068 T072 — sweep tests`
3. `/speckit.specify Build a Python application/library following what is described in docs/design/00-initial-design.md file`
4. `/speckit.implement T034 T035  — complete 1.x migration`

**Corrections and steering:**
5. `2+1 but also see if SHELL env var available -- should tell which shell is running.  and also 3 - yes, we should complete what we know.   Also you could not find /speckit.clarify but there is ./.claude/skills/speckit-clarify -- did you see it?`
6. `honor --dataset, but if not given -- deduce by going up the folders hierarchy until seeing dataset_description.json which should be an indicator of BIDS dataset root`
7. `commit and add that bids-examples submodule -- you should have git write access`
8. `re question: the https://pypi.org/project/bids/ is placeholder pointing to pybids.  https://pypi.org/project/bids-utils/ is not yet taken.    I think let's just keep 'bids-utils' CLI entry point for now.`

**Failure reports:**
9. `add to spec and CLAUDE.md to never auto-commit if 'tox' testing fails.  ATM for me \n\n[tox output]\n\nso make sure that all testing passes, fix and commit .`
10. `I have lots of tess skipped without stating a reason:\n\n[terminal output]\n\ncould you enhance stating a reason there`
11. `looking at diff like \n\n[diff snippet]\n\nstate the exception in the message so it is possible to see right away on why cannot load`

**Minimal approvals:**
12. `A`
13. `yes`
14. `proceed how you recommend`
15. `should I run /speckit.implement now or we can somehow prioritie recommended next steps? (just asking - no action needed)`
