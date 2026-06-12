---
name: terse-correction
description: One-phrase correction when the agent gets a factual detail wrong (wrong provider, wrong auth type, wrong service). No apology, no explanation — just the correct fact. Trigger when agent_said contains a wrong assumption and user corrects with a short clause.
---

# terse-correction

When the agent gets something wrong — wrong LLM provider, wrong credential type, wrong service —
correct with the shortest possible phrase that states what IS right. Do not explain why, do not
say "actually", do not hedge.

**Pattern:** `<correct thing> not <wrong thing>` or just `<correct thing>`

## Examples

```
with auth token not api key
```

```
even telegram isnt starting and this was supposed to work with claude code and codex not gemini
```

(The second is longer because multiple things are wrong simultaneously. Still no punctuation,
all lowercase, typos intact: "isnt" not "isn't".)

```
i wanna autheticate with codex cli
```

(Redirects by stating the desired action; implicit correction that the agent's suggestion was wrong.)
