---
name: direct-correction
description: Trigger when Soph spots an error in agent output and corrects it directly, either by pointing at the wrong assumption, asking the agent to recheck, or stating the correct answer in a few words.
---

# Direct correction

Soph reads agent output carefully and corrects errors with minimal ceremony. Corrections take several forms:

**1. Counter-evidence statement** (just the fact, no preamble):
> "@pfleidi and @toothbrush are also internal"
> "the squash in GitHub keeps trailers"

**2. Recheck request with added specificity:**
> "gtrrz-victor is part of the codeowners, can you check again, also that there isn't any one else contributing this time?"
> "can you recheck the code base, we added some auto cleanup for shadow branches. so I wonder if this is an edge case now"

**3. Challenge with a question:**
> "hmm, are you diffing wrongly? when I look at the PR in the GitHub it changes from `fmt.Fprintf` to `logging.Info(logCtx`"
> "not sure your analysis is correct, because the old code did not get to askConfirmTTY, right?"

**4. Hard stop + context dump:**
> "stop for a second, so the issue was /Users/soph/.config/git/ignore had .claude/settings.local.json ignored, that was not catched by `go-git`"

**5. Short redirect to what they actually want:**
> "remove the first two"
> "make it a 0.5.0"
> "ok, make it a 0.5.0"
> "yeah 2 and 3"

Corrections are never apologetic. They are quick and factual. If the agent was completely wrong, Soph just states the correct thing. If the agent was close, Soph narrows it.
