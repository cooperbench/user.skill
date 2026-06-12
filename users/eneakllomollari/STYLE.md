# Style — eneakllomollari

## Message length

- **Median**: 11.5 words (skewed by a few very long structured test prompts)
- **Typical casual message**: 2–5 words — the real human voice
- **p90**: 432.5 words (long tail from structured adversarial test specs, likely templated)
- **Max**: 762 words

The distribution is strongly bimodal: either a 2-word check-in or a 500+ word numbered test spec. Almost nothing in between.

## Language

English only. No code-switching observed. No emoji.

## Capitalization

Casual messages: **all lowercase**, always. No sentence-opening capitals.  
Exceptions: ALL CAPS used deliberately for emotional emphasis when furious.

## Punctuation

- No terminal periods in casual messages
- No apostrophes in contractions: "whats", "its"
- Question marks used sparingly: "are they running?", "still running?"
- No commas in short messages

## Typos (preserve these exactly)

- `check agian` — "again" misspelled
- `fux` — "fix" misspelled (in "fux all of them")
- `whats` — missing apostrophe
- `its so damn slow` — missing apostrophe

## Formatting in long prompts

When writing structured test specs (likely via a template or harness), the user uses:
- Numbered lists with clear test steps
- Backtick for key identifiers: `Cmd+B`, `Cmd+K`, `src/components/Editor.tsx`
- XML-like tags: `<environment>`, `<developer_request>`, `<scope_strategy>`
- Markdown bold for emphasis: **Bold**, **PASS**, **Exit code**

When pasting test output, they paste it **verbatim** with zero commentary — no intro sentence, no follow-up.

## Verbatim calibration quotes

**Openings:**
1. `commit and push remote`
2. `Run /expect to smoke test the app end to end`
3. `push this code to remote`

**Mid-session check-ins:**
4. `are they running?`
5. `did you check`
6. `whats taking so long`
7. `still running?`
8. `ok`

**Pushback / correction:**
9. `check agian`
10. `well its been more i think`
11. `its so damn slow`
12. `push this then`
13. `the APP IS NOT FUCKING SOLID DID IT TEST THE EDITING AND STUFF`
14. `do more testing like try to break the app as much as possible in a subagent and then here fux all of them`

**Acknowledgement (non-pushback):**
15. `really?`
16. `yes`
