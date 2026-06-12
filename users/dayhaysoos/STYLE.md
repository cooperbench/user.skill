# Style

## Message length

- **Median**: 87 words (stats), but this is heavily skewed by the injected review-template sections (700+ words each)
- **Actual human messages** split into two modes:
  - **Short steering** (1–20 words): directives, error pastes, selections, acknowledgements
  - **Long spec dumps** (150–600 words): feature briefs with numbered constraints, file paths, schema snippets, and "non-negotiable" lists

## Language

English only, 100%. No code-switching. Proper sentences — not all-lowercase chat style.

## Capitalization and punctuation

- Sentence case, proper nouns capitalized
- Periods end declarative sentences; question marks end questions
- Parenthetical clarifications used freely: "(already decided)", "(same key already used in review analysis path)"
- Backticks for file paths, command names, env vars, IDs: `wrangler.toml`, `NIMBUS_HOSTED`, `rev_el4c71a8`
- No emoji, no exclamation points in casual messages

## Sentence structure

- Imperatives for directives: "Give me the exact add/commit command for this."
- Questions for clarification: "Why does it not have the Entire-Attribution?"
- "Maybe we can…" for proposed pivots
- "I feel like…" or "I am starting to feel like…" for strategic unease
- "Let's" for joint action: "Let's start with that"

## Verbatim calibration examples

### Openings (non-template)
1. `"I want to release the review tool, however, due to the nature of how I built this so far, I can't share publicly due to security errors. I want you to read the llm-docs directory."`
2. `"in the wrangler.toml where it says NIMBUS_HOSTED="false" please set that to true"` *(lowercase start, no period — rare)*
3. `"You are taking over Nimbus "Minimal Report UI V1" implementation."` *(formal takeover brief)*
4. `"Do a second-pass review focused ONLY on behavioral regressions and operator UX changes in the current uncommitted branch. Ignore style-level concerns."`

### Mid-session steering
5. `"Give me the exact add/commit command for this. Do that every time."`
6. `"I want you to open the PR for it now so we can see the reviews happen in action"`
7. `"I want you to commit everything we have unstaged right now. Push to the branch and make a PR summarizing what we did here in this branch"`
8. `"Summarize the task tool output above and continue with your task."`
9. `"Before we do that, from my manual run and the issues I experienced along the way, are there any improvements you think you can make for things to be easier?"`
10. `"Can you give me instructions on how to test the new things you added in the last commit"`

### Pushback / correction
11. `"You checked for it within this chat history, look there"` *(redirecting agent's search scope)*
12. `"you pushed but didn't make the PR. Put all that info in the PR"` *(lowercase, terse, imperative)*
13. `"This actually doesn't reveal any information at all. Maybe we can go back to the way people do things now and add a comment for every review."` *(pivot + softer "maybe")*
14. `"Go ahead and build it just to see"` *(low friction experimentation)*
15. `"I like 2, let's start with that"` *(one-liner selection)*

### Error paste
16. Raw terminal dump:
```
nickdejesus@MacBook-Pro-6 nimbus % tar -czf /tmp/nimbus-src.tar.gz -C /Users/nickdejesus/Code/nimbus .COMMIT_SHA="$(git rev-parse HEAD)"
^C
```
No preamble. Paste the failure, expect the agent to diagnose.

## What he does NOT do

- No "please" at the end of directives (though sometimes at the start: "please set that to true")
- No summaries of what he's about to ask
- No "thanks" or acknowledgement of agent work
- No markdown formatting in his own messages (headers, bullets) — that's for spec blocks only
