# Style: musicofhel

## Message length

- **Median**: 340 words  
- **p90**: 880 words  
- **Max**: 882 words  

Messages are long because they are instruction payloads, not because the user is verbose. Every word serves a structural purpose. There is no filler, no preamble, no sign-off.

## Format anatomy

Every prompt follows this exact skeleton, in this order:

```
You are a senior code reviewer performing an automated quality gate check.

## Issue Context
**Title:** <issue title>
**Description:** <one or two sentences>

## Review Criteria
Check the diff for the following issues:
  - race_conditions
  - memory_leaks
  - logic_errors
  - missing_error_handling_at_boundaries
  - performance_antipatterns

## Severity Levels
  - critical: fail
  - warning: pass
  - suggestion: pass

## Instructions
1. Review the diff below carefully.
2. For each finding, classify it as: critical, warning, or suggestion.
3. Respond with ONLY valid JSON — no markdown fences, no explanation outside the JSON.
4. Use this exact schema:
   { "findings": [...], "summary": "..." }

If there are no findings, return: {"findings": [], "summary": "No issues found."}

## Diff to Review
```<diff>```
```

Some prompts are collapsed (all `##` sections run together with no blank lines between); others use blank lines between sections. Both are valid — the pipeline has minor whitespace inconsistency.

## Capitalization and punctuation

- Section headers always use `##` markdown, title-cased: `## Issue Context`, `## Review Criteria`
- Bold for field labels: `**Title:**`, `**Description:**`
- Criteria and severity items use lowercase kebab-case with leading `  - ` (two-space indent)
- JSON keys are lowercase snake_case
- The output-constraint sentence uses ALL CAPS for the key word: `ONLY valid JSON`
- No trailing punctuation on bullet items
- No emoji, no exclamation marks

## Language

English only. No code-switching detected across any of the 7 prompts.

## What is never present

- Conversational openers ("Hey", "Can you", "Please", "Hi")
- Hedging ("maybe", "I think", "if possible")
- Follow-up or correction messages
- Apologies or thanks
- Inline commentary on why criteria were chosen

## Verbatim calibration quotes

**Role assignment (opening line — always identical):**
> `You are a senior code reviewer performing an automated quality gate check.`

**Output contract (always present, always this wording):**
> `Respond with ONLY valid JSON — no markdown fences, no explanation outside the JSON.`

**Null-findings fallback (always present):**
> `If there are no findings, return: {"findings": [], "summary": "No issues found."}`

**Severity mapping (always these three lines):**
> `  - critical: fail`  
> `  - warning: pass`  
> `  - suggestion: pass`

**Review criteria block (always these five, always in this order):**
> `  - race_conditions`  
> `  - memory_leaks`  
> `  - logic_errors`  
> `  - missing_error_handling_at_boundaries`  
> `  - performance_antipatterns`

**Issue context — example 1:**
> `**Title:** Add factorial function with edge case handling`  
> `**Description:** Add factorial() to src/oo_test_project/calculator.py. Must handle negative (ValueError) and float (TypeError) inputs. Tests exist in tests/test_calculator.py.`

**Issue context — example 2:**
> `**Title:** Fix typo in README.md installation section`  
> `**Description:** The README.md has a typo: 'pip instal' should be 'pip install'`

**Issue context — example 3:**
> `**Title:** Add user search with database query`  
> `**Description:** Add GET /api/users/search endpoint. Accept a q parameter and search users by name using SQL.`

**Issue context — example 4:**
> `**Title:** v4: add rounding helper to scoring`  
> `**Description:** ` *(empty — description field left blank)*

**JSON schema block (always this exact schema):**
> `{ "findings": [ { "severity": "critical|warning|suggestion", "message": "description of the issue", "file": "path/to/file or null", "line": line_number_or_null, "rule": "which criteria this violates" } ], "summary": "one-line overall assessment" }`
