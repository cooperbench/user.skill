---
name: automated-review-kickoff
description: How musicofhel opens every session — a machine-generated structured instruction block that assigns a role, provides issue context, states review criteria, and demands JSON output. Triggered on every single interaction; there are no other opening patterns.
---

Every prompt begins by assigning the agent a role and framing the task as an automated quality gate. There is no variation in this opener — it is emitted identically by the pipeline on every run.

The opening line is always:

> `You are a senior code reviewer performing an automated quality gate check.`

This is followed immediately by `## Issue Context` with bold-labeled `**Title:**` and `**Description:**` fields populated from the issue/PR metadata.

**Example 1** (feature addition):
```
You are a senior code reviewer performing an automated quality gate check.

## Issue Context
**Title:** Add factorial function with edge case handling
**Description:** Add factorial() to src/oo_test_project/calculator.py. Must handle negative (ValueError) and float (TypeError) inputs. Tests exist in tests/test_calculator.py.
```

**Example 2** (trivial doc fix):
```
You are a senior code reviewer performing an automated quality gate check.

## Issue Context
**Title:** Fix typo in README.md installation section
**Description:** The README.md has a typo: 'pip instal' should be 'pip install'
```

**Example 3** (empty description — the pipeline does not guard against blank fields):
```
You are a senior code reviewer performing an automated quality gate check.

## Issue Context
**Title:** v4: add rounding helper to scoring
**Description:** 
```

The opener is never modified based on the nature of the diff. A security-sensitive change (SQL injection) and a documentation typo fix receive the exact same role assignment and framing.
