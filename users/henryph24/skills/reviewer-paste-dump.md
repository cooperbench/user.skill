---
name: reviewer-paste-dump
description: >
  Trigger: user pastes a large block of formatted reviewer/critic text (800-1800 words,
  with bold headers, LaTeX math, numbered points) without any framing or explicit instruction.
  Sometimes prefixed with a short phrase like "What do you think of this another reviewer
  feedback:" or "A new reviewer flags this:" or nothing at all. The agent is expected to
  extract action items, audit validity, and respond or act.
---

# reviewer-paste-dump

henryph24 feeds reviewer critiques — from LLM reviewers, simulated NeurIPS ACs, or
`paperreview.ai` — directly into the session as raw prompts. He provides no instruction about
what to do with them. In ~30% of cases, the paste is the entire message with zero framing.
In the remaining cases, a 3-10 word lead-in precedes the paste.

He always uses triple-quote delimiters `"""..."""` when there is any framing at all.

After pasting, he expects the agent to: audit which claims are real vs hallucinated,
prioritize must-fix items, implement the non-experiment fixes immediately, and queue
experiments for the ones that need GPU time.

## Pattern

Option A (no framing — just the paste):
```
**[Senior Area Chair (Reviewer 4) has entered the chat...]**

Take a deep breath...
[800-1800 words of formatted reviewer text]
```

Option B (minimal framing):
```
What do you think of this another reviewer feedback: """Must-fix items: Resolve the Table 2
vs. Table 8 diagonal inconsistency — that's the one legitimate issue...

Ultrathink"""
```

Option C (paste + single modifier):
```
[paste of 1100 words]

Ultrathink
```

## Verbatim examples

> `What do you think of this another reviewer feedback: "Must-fix items: Resolve the Table 2 vs. Table 8 diagonal inconsistency — that's the one legitimate issue that could genuinely erode reviewer trust...`
> [400 more words]
> `Ultrathink`

> `did we fully address the review of: """Get detailed AI feedback on your research paper...`
> [1816 words]

> `A new reviewer flag this: """`
> [998 words of reviewer text]

> `address this feedback: """`
> [909 words]

## After the paste

He follows up with short steering once the agent responds:
- "let handle them carefully item by item"
- "let do what does not need new experiments now, then recite the next steps"
- "are any of these should be written into the paper"
