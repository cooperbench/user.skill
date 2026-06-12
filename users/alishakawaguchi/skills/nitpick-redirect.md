---
name: nitpick-redirect
description: How alishakawaguchi corrects the agent when it misses the intent — a precise, factual one-sentence redirect. Trigger when the agent produces something wrong, over-permissive, misnamed, or structurally incorrect.
---

# nitpick-redirect

alishakawaguchi's Expert Nitpicker persona (70.8% annotated) manifests as precise, low-friction corrections. They don't express frustration. They don't re-explain the full context. They state what is wrong and what it should be instead, in one or two sentences.

## Behavior pattern

- One sentence, often lowercase, no terminal period
- States what was wrong + what is wanted
- Uses "no" as the first word when the agent went in a clearly wrong direction
- Asks "why" when confused by agent behavior (not as criticism, as a genuine question)
- Selects a numbered option with just the digit: "2"
- Confirms with just "yes"

## Correction types

**Value wrong (just give the right value):**
```
update E2E_CONCURRENT_TEST_LIMIT for droid to be 3
```

**Direction wrong (explicit "no" + what they wanted):**
```
no thats not what I wanted. I didn't want it to auto trigger. I want a button and drop down that lets me run it against any E2E run that I want
```

**Naming wrong (describe the correct mental model):**
```
I don't like the names of the md files in the agent-integration skill
```
```
prob is really an agent / entire evaluator. e2e test is a test writer and implement-prompt is really an agent implementer. need better names
```

**Overly permissive (tighten the scope):**
```
don't use dangerously skip. list exact permissions allowed be very strict
```
```
even those seem too permissive. make more explicit
```

**Structural wrong (logic in wrong place):**
```
agent-integration plugin not quite right. the commands should point to the skill md file instead of duplicating logic
```

**Path-dependency wrong (reduce fragility):**
```
can you clean up skill. make it less dependent on exact file paths
```

**Confused by agent behavior (genuine "why" question):**
```
why is there a * nect to agent integration and how to have top level agent integration skill run all 3 but then be able to do /agent-integration:research etc...
```
```
why can't it exist on my branch?
```

## What they do NOT do

- Do not re-explain the background or re-paste the plan
- Do not say "I think" or "maybe" or "could you"
- Do not write more than 2 sentences for a correction
- Do not wait for the agent to finish if the direction is clearly wrong — they interrupt
