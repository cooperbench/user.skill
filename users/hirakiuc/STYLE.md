# Style: hirakiuc

## Message length

- **Median**: 13 words. **p90**: 39 words. **Max**: 451 words (single large spec dump).
- Typical messages are 8–20 words. Multi-sentence messages are rare and only appear for
  corrections or encouragements.
- The 451-word max is a one-off structured spec paste (AGENTS.md content via @-file
  expansion), not representative of composed prose.

## Capitalization

- Mixed, sentence-level. Sentences starting with "I", "Wait", "Hey", "Yes", "OK" are
  capitalized. Messages starting with "got", "please", "what" are often lowercase.
- File paths and @-references follow their literal casing.

## Punctuation

- Ends most sentences with a period. No trailing ellipses.
- Comma after "Wait" and "Hey" as openers.
- No exclamation marks except rare encouragement: "Let's complete this hard work!"
- No em-dashes, no markdown formatting in prose messages.

## Emoji

- None.

## Typos / non-standard phrasing

- "clearify" instead of "clarify" (verbatim: "I just clearify if you need some more
  knowledge")
- Slightly non-native phrasing: "address those feedback" (not "that feedback"),
  "research related knowledge online at first"
- Otherwise grammatically clean.

## @-file references (Gemini CLI syntax)

- References files with `@path`: `@AGENTS.md`, `@.agent/feedback.md`,
  `@~/.gemini/GEMINI.md`
- Never pastes file contents directly — uses @-reference and lets the agent expand it.

## Error / failure reporting

- Does NOT paste logs, stack traces, or diffs inline.
- Reports failures with minimal words: "CI status shows failure. please check and fix it."
  or "what happened?"

## Calibration quotes (verbatim)

**Session openers:**
> "check the @AGENTS.md , @GEMINI.md and @~/.gemini/GEMINI.md files to understand this project development workflow."

**Feedback delegation:**
> "got some feedback on the current code base. please check the @.agent/feedback.md file."
> "got some feedback. please check the @.agent/feedback.md file."

**Steering / mid-session:**
> "I have merged the pull request on GitHub. switch to the main branch and pull the latest commits."
> "OK, let's proceed this refactoring task"
> "Yes, please create the pull request with this topic branch."
> "Please switch back to the topic branch. Then the reviewer will review the topic branch."

**"Wait," corrections:**
> "Wait, please make a proposal to address those feedback."
> "Wait, could you analyze the current situation? I'm really curious why this topic branch needs to be changed with so much diffs."

**Git workflow reminder:**
> "Hey, do you forget about this project development workflow? Before making code change, you should create a topic branch. and after changing codes, the change should be committed to the topic branch. And then you should create a pull request."

**Failure reports:**
> "CI status shows failure. please check and fix it."
> "what happened?"
> "What happened?"

**Research nudge:**
> "I think, you should research related knowledge online at first. Then you might have enough understanding how to fix them. Please research anything actively as you need."

**Encouragement:**
> "OK, I had already same understanding. I just clearify if you need some more knowledge (like, latest specific module information or howto...) to solve this situation. Then, please proceed this. Let's complete this hard work!"
