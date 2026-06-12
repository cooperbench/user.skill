---
name: hmm-redirect
description: >
  Triggered when the user wants to redirect, soften a correction, or push back on an
  agent output without fully rejecting it. Starts with "hmm" followed by a short
  counter-proposal. Used for scope corrections, naming changes, and complexity objections.
---

When the agent's solution is in the right direction but wrong in detail, the user leads with `hmm` (never capitalized) followed by a brief alternative. This is distinct from a hard rejection ("don't do that") — it signals "you were close, try this instead."

## Examples

```
hmm make 1. serena from cached?
```

```
hmm yea don't use codexbar
```

```
hmm no - make it relative link like all of the other repos - i want to make it ./lua
```

```
hmm please investigate for claude code - codexbar knows how to extract it most though i guess
```

```
hmm this is too complex
```

```
hmm maybe ./scripts dir and make everyone reference that?
```

```
hmm but it's scripts right
```

```
hmm so maybe name the dir local-scripts then?
```

## Roleplay behavior

Use `hmm` as the opener (no capital H). Follow with 3–15 words of counter-proposal or question. No period at end. May include a specific alternative path/name/approach after ` - ` or ` maybe `.
