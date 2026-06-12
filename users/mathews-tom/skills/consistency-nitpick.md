---
name: consistency-nitpick
description: How Mathews-Tom raises consistency issues — he notices structural or naming inconsistencies after the agent declares completion, describes the problem clearly, and asks "how can and should we fix this?" Trigger after the agent reports task completion and there's a structural discrepancy the user might notice.
---

# Consistency Nitpick

After an agent reports task completion, Mathews-Tom audits the output for inconsistencies between directories, naming schemes, or structural conventions. When he finds one, he:

1. Describes the inconsistency concisely and specifically (which dirs are inconsistent, how)
2. Names the symptom ("The repo appears to lack consistency")
3. Frames the fix as an open question ("how can and should we fix this?") — inviting options rather than dictating

He is not asking idly. If the agent proposes something that doesn't feel right, he immediately counter-proposes (see `counter-proposal.md`). The question form leaves room for the agent to suggest, but he has strong opinions.

He also uses this pattern when the agent's response reveals it misunderstood his context — he corrects with specificity, naming the exact entities he meant.

## Examples

**Example 1** (after agent declared all 9 alignment/systems scripts complete):
```
We need to make some chnages. All the scripts in the `foundations` folder are numbered to be in order but the scripts in the `alignment` and `systems` folders don't have it. The repo appears to lack consistency. how can and should we fix this?
```

**Example 2** (correcting the agent's clarifying question — context was already there):
```
I was talking secitons like `foundational` (rename it to `foundations`), `alignment` and `systems`.
```

**Example 3** (after agent reported all 7 foundation scripts validated):
```
Why is the test run for `03-microgpt.py` only has a marginal pass. Wasn't this script we got from karpathy directly, https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95.
```

**Example 4** (after all changes committed, quality check before publishing):
```
Before we publish the repo, let us make sure we we have all documentation, comments in scripts and everything perfectly updated and aligned with the overall goal of the repo.
```
