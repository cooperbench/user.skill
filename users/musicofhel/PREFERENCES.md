# Preferences: musicofhel

## What they correct or reject

Nothing — ever. `pushback_distribution: {non_pushback: 1.0}`. The pipeline does not loop back to the agent for corrections. It consumes the first response unconditionally.

## What satisfies them

Output that conforms to the specified JSON schema. The pipeline downstream parses the JSON, checks whether any finding has `severity: "critical"`, and uses that as the gate signal. A response that contains valid JSON with the correct keys is a successful response, regardless of the content of the findings.

## Workflow habits

- **No planning step.** The pipeline emits a fully-formed instruction; there is no "let's think about how to approach this" phase.
- **No explanation requested.** The instructions explicitly forbid explanation: `no explanation outside the JSON`. The user never asks "why" — they ask for structured data.
- **No iteration.** Session turns median = 1. One prompt, one response, done. The `dev-loop` handles looping at the infrastructure level, not the conversation level.
- **Test-aware but not test-driven interactively.** Intent distribution is 57% `understand` and 43% `test` — both map to the same review-gate use case; the classification reflects whether the reviewed change is a test or production code.
- **Batch operation.** Multiple sessions exist for the same diff (e.g., the README typo fix appears in at least 3 separate sessions). This indicates the pipeline reruns on the same issue context, possibly for regression testing the reviewer itself.

## Tool and stack preferences

- **Claude Code** as the LLM engine (100% of sessions)
- **Python** as the primary reviewed language (calculator.py, scoring.py, test files, uv.lock)
- **uv** as the Python package manager (uv.lock files appear in diffs)
- **pytest** as the test framework (uv.lock includes pytest, iniconfig, pluggy)
- **Markdown** for structured prompts (not plain text, not XML)
- **JSON** as the output format — never asks for prose summaries that aren't also JSON

## What the pipeline is testing

The reviewed code samples reveal the pipeline is used to test the reviewer against known-good and known-bad diffs:

- `factorial()` — correct implementation with proper error handling (expected: no critical findings)
- README typo fix — trivial change (expected: no findings at all)
- SQL search endpoint — almost certainly contains SQL injection vulnerability (`q` parameter concatenated into raw SQL) (expected: `critical` finding for `logic_errors` or `missing_error_handling_at_boundaries`)
- `round_score()` helper — thin wrapper around `round()` (expected: suggestion-level findings at most)

This is a benchmark/eval loop: the user is evaluating the LLM reviewer's recall and precision against a set of labeled diffs.
