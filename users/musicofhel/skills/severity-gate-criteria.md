---
name: severity-gate-criteria
description: How musicofhel encodes the pass/fail gate logic — five fixed review criteria, three severity levels mapped to binary gate outcomes, always stated in the same order and format. This is the core decision framework of the dev-loop pipeline.
---

Every prompt includes two sibling sections that together define the gate: the criteria to check, and the severity-to-outcome mapping.

**## Review Criteria** (always these five, always this order, always lowercase kebab-case):
```
## Review Criteria
Check the diff for the following issues:
  - race_conditions
  - memory_leaks
  - logic_errors
  - missing_error_handling_at_boundaries
  - performance_antipatterns
```

**## Severity Levels** (always these three lines, always this mapping):
```
## Severity Levels
  - critical: fail
  - warning: pass
  - suggestion: pass
```

The gate logic: only `critical` findings cause a pipeline failure. `warning` and `suggestion` findings are surfaced but do not block. This means the pipeline is tuned for precision on blockers — it prefers false negatives over false positives at the `critical` level.

The five criteria represent the user's threat model for their codebase:
- `race_conditions` — concurrent access bugs
- `memory_leaks` — resource management failures  
- `logic_errors` — incorrect algorithm or control flow (this is the bucket that catches SQL injection)
- `missing_error_handling_at_boundaries` — unguarded I/O, type mismatches at API surfaces
- `performance_antipatterns` — O(n²) loops, unnecessary allocations, etc.

These criteria never change between sessions — they are hardcoded in the pipeline template, not parameterized per-issue.
