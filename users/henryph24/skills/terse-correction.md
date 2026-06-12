---
name: terse-correction
description: >
  Trigger: agent output is incomplete, wrong, or overengineered relative to what he asked.
  He corrects with a 1-8 word directive, no explanation, no softening. Fires when agent stops
  short of writing results into the paper, repeats old numbers, adds unnecessary steps, or
  fails to reach the RACE VM repeatedly.
---

# terse-correction

henryph24 corrects without preamble. He does not explain why the agent was wrong unless the
error is domain-specific and requires technical context. His corrections are imperative, present
tense, lowercase, and assume the agent already knows what went wrong.

## Pattern

- 1-8 words
- No punctuation or minimal
- No explanation of the problem
- Sometimes just "try AGAIN" or a restatement of what he originally wanted

## Verbatim examples

**When agent stops short of writing results to paper:**
> `yes, make sure that all results that are relevant and sthenghenting our paper are wrriten`

**When agent blocks on VM access:**
> `just whitelist, try again reaching the vm`
> `try AGAIN`
> `VM just restarted, try again`

**When agent misattributes experiment scope:**
> `I thought we had 29 experiments`

**When agent writes partial table and defers the rest:**
> `are any of these should be written into the paper (aware of length limit of 9 pages)`

**When agent underestimates and he wants more queued:**
> `plan changes and further experiments needed to reach 9`
> `let design that and run that in race vm now`

**When agent finishes experiments but paper isn't updated:**
> `did we factor in new relevant results into the paper ?`
> `did we fill in newly arrived results into the main paper`

**When direction needs to change:**
> `should we replan our approach ?`
> `I want the boldest path to NeuralIPS 2026`

## What he does NOT do

He does not write "I think the issue is X, can you please Y instead." He just gives the
corrected instruction and expects the agent to pick up immediately.
