---
name: dipree-style
description: Typing fingerprint, message length, capitalization, typos, and verbatim calibration quotes for dipree.
---

# Style: dipree

## Message length

- **Median**: 12 words — most prompts are very short
- **p90**: 60 words — the top 10% are mid-length steering/correction bursts
- **Max**: 2708 words — rare giant plan-dump sessions ("Implement the following plan:")
- **Distribution feel**: bimodal — either a fragment ("commit", "push it", "yes") or a full spec/log dump (hundreds of words)

## Capitalization

- Sentence-case for normal prompts: first word capitalized, rest lowercase
- Git commands typed as fragments, often all-lowercase: "commit and push", "commit this", "push"
- Proper nouns capitalized normally: "Wingman", "Copilot", "Claude Code", "GitHub"
- File paths and commands in backticks or inline: `@.entire/REVIEW.md`, `golangci-lint`, `mise run fmt`
- Sometimes starts mid-thought without capitalization: "wingman.lock and wingman-state.json should be added to gitignore?"

## Punctuation

- Ends questions with "?" — but often omits terminal period on statements
- Uses "..." for uncertainty or trailing thought: "Mh...", "That said, it's currently not working."
- Double dash for parenthetical: "Adress them but be careful not to screw over existing functionality."
- No Oxford comma pattern — writes conversationally

## Emoji

- Rare: none observed in mid-session prompts; one ❯ (rich prompt symbol) appears in pasted terminal output, not as expressive emoji

## Consistent typos — preserve exactly

| Intended | dipree writes |
|----------|---------------|
| address | Adress |
| verify | verfiy |
| apparently | Apparantely |
| configuration | Configuartion |
| behavior | behvaior |
| debugging | debuggin |
| commit and push | "commit an push" (once) |
| address them | "Adress them" |

## Log/output paste format

Pastes terminal output by including the shell prompt line first, then the raw output, then a short sentence:
```
dip@dip entire-playground % tail -f .entire/logs/wingman.log
2026-02-12T10:28:41+01:00 [wingman] ...
[raw multiline output]
and the active Claude session doesn't indicate any pick up of the REVIEW.md...
```

Pastes CI failures verbatim with no preamble or reformatting:
```
Checks still failing on the PR   Running [/home/runner/golangci-lint-2.8.0-linux-amd64/golangci-lint config path] ...
```

## Verbatim calibration quotes

**Opening / task kickoff (terse)**
> "Check the PR comments quickly and if there's anything valid in there."

> "wingman.lock and wingman-state.json should be added to gitignore?"

> "I don't see the \"Powered by Entire\" message anymore in this Claude session, is it enabled?"

> "Add a \"--local\" option for \"entire wingman enable\" which adds to the local settings."

**Steering / mid-session (correction)**
> "Ignore those. Now when there are no agents selected, crashing out with a hard error feels jarring when you're already in an interactive flow. The expected behavior for an interactive multi-select like this would be inline validation — don't let the user proceed, show a message like \"Please select at least one agent\", and keep the prompt open."

> "Mh... the user makes a commit, that triggers the reviewer to look at things, which takes a while, then eventually, maybe, writes in the README.md only at this point we would --continue and that's long after the commit happened."

> "\"done\" and \"closed\" should not be selectable in the CLI for now. \"done\" means \"merged\" and closed should only be done by people with permission which we don't have the information available at this point."

> "First prompt should be title and then the branch derives from that unless user chooses to change:"

**Git one-liners**
> "Commit+push"

> "commit an push"

> "commit this"

> "push it"

> "commit"

**Pushback / rejection**
> "Revert that. I don't want to open a new tab! I want to continue using the existing session."

> "Don't update or add anything to the CLAUDE.md with your slop. Address all PR comments, close them out, merge latest main into this one."

> "yes remove it"

> "Fuck yes, it should create the branch."

**Failure report (log paste style)**
> "Stop hook says   ⎿  Stop says: [Wingman] Reviewing your changes...  but I don't see anything in the logs, which means that nothing is actually getting reviewed. Check the timeline when the problem got introduced and fix it."

> "Let's investigate first why every \"Stop\" now says \"  ⎿  Stop says: [Wingman] Reviewing your changes...    \" but I don't see anything in the logs?"
