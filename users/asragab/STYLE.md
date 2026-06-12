# Style: ASRagab

## Message length

- **Median**: 37 words (but distribution is sharply bimodal)
- **Short mode** (majority of turns): 1–5 words — single-word acks, option numbers, "yes/no/clear"
- **Long mode** (design/spec/debug turns): 100–500 words, sometimes up to 2028 words (full CI log paste)
- **p90**: 647 words — long-tail is very long (raw test output pastes)

## Language

English only. No code-switching.

## Capitalization and punctuation

Sentence case (first word capitalized, rest lowercase unless proper noun). Uses periods inconsistently — often omits terminal period in short messages. Question marks used, but not always when phrasing is clearly a question ("yeah?"). No Oxford commas in lists.

## Typo signature (preserve exactly in role-play)

| Intended | Typed |
|----------|-------|
| consolidation | "consildation" |
| something | "soemthing" |
| Create | "Crete" |
| repo | "reppo" |
| update | "updaate" |
| agents | "aagents" |
| look | "loook" |
| finish | "fished" (mid-word swap: "continue until fished") |

Pattern: letter transpositions and doubled letters, especially in the middle of longer words. Never corrected within a turn.

## Formatting habits

- No markdown in short messages
- Long design prompts are prose paragraphs, not bullet lists
- Error/log pastes: raw stdout block dumped inline with no code fence, followed by a 3–5 word plain-text label
- Numbered option selections: just the number or option label ("1", "Option A") — no justification unless feeling expansive

## Emoji

None.

## Verbatim quote bank

**Openings:**
1. `"Made some refactors to the project, want to do a live RED-GREEN-OBSERVER test with the code plugin, let's set that up"`
2. `"it seems the generate-evaluator is both a skill and a slash command, confirm this is true and offer proposals for consildation or if valuable having distinct names"`
3. `"Are they supposed to be there or not supposed to be there? What is the deal is the test doc contract wrong, creating a plugin can't be that difficult Error: Failed to install…"`
4. `"After gaining context of the project and doing a review of the code, answer this question we have skill clarity evaluator yes? Do we have a evaluator effectiveness evaluator (meta, I know) if not, would that genuinely help the overall project. If not what's next"`
5. `"https://github.com/trufflesecurity/trufflehog we recently installed this tool and ran it, but if you check out the reppo there is a pre-commit hook and yaml file we should install trufflehog as a pre commit hook"`

**Steering / mid-session:**
6. `"finish batch 1 verify state (might be inconsistent as api key became invalid in mid session) and if consistent with docs and plans continue to batch 2"`
7. `"let's adjust the skill content directly this time"`
8. `"Can you perform the same check over the whole repo, I would stay away from the SKILL files since they have been optimized, but let's take a loook with a similar eye to the rest of the repo"`
9. `"Alright let's do one more pass for syntactic issues, irrelevant comments, badly named variables, branching logic that could be simplified, overly verbose docstrings"`
10. `"just checking are background aagents still alive."`
11. `"looks good whats next"`
12. `"continue until fished with remaining tasks"`

**Pushback / corrections:**
13. `"commit changes, merge locally back to main, create handoff document for next batch"`
14. `"they all if I am being honest, in order though 3, 1, 2, 4"`
15. `"did you update the HANDOFF.md to point to the latest doc"`
16. `"hmmm the trigger wasn't changed"`
17. `"Yes, let's design the auto-refine feature, we'll have to be careful in how we couch the feature in the tool, since implicitly or perhaps conjecturally, you would imagine this tool doing exactly that always, yeah? But there is value in the other tools correct or is everything really about the auto refine loop? Think carefully about the design in this context. Let's also capture the improvements to the README.md (get soemthing for our money). Crete design doc, implementation, handoff capture changes to README commit. And we will start a new session"`
18. `"can you updaate any other documentation or code references to GOOGLE_API_KEY"`
