---
name: spec-dump-kickoff
description: Opens a complex task with a detailed, structured spec that includes categories, tables, and step-by-step instructions. Trigger when the user is starting a non-trivial new feature, a TDD session, or a multi-function refactor.
---

# Spec dump kickoff

When a task is complex — multi-function changes, TDD plans, or feature specs — adrientaudiere switches from terse commands to full structured specs. These are written in markdown with headers, tables, and code blocks. They are the exception to the 11-word median; they reach hundreds or thousands of words.

These specs typically appear as opening prompts for a session, or after the user has thought through a problem and wants to hand over a complete plan.

## Example structure (from TDD plan opening):

```
Implement the following plan: # Plan: Test & fix functions with `fact` param on single-level factor
## Context
Many MiscMetabar functions accept a `fact` parameter but crash with cryptic errors...
## Categories
### A. Functions that SHOULD WORK with 1 level
| Function | File | Expected output |
|---|---|---|
| `tax_bar_pq` | `R/plot_functions.R` | Single-bar ggplot |
...
### B. Functions that SHOULD GIVE INFORMATIVE ERROR with 1 level
...
```

## Example (feature spec opening):

```
I want to add a new parameter (logical, default FALSE) to biplot_pq. If true, each bar part (ie each sample sum total for the given taxa) is delimited by vertical bars. So using contour color (default white) of bar, I want to see the distribution of the number of sequences across samples using staked bar.
```

Note the typo "staked" for "stacked" and parenthetical clarifications. Spec dumps are detailed but not perfectly edited.
