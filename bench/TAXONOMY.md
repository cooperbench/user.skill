# Move taxonomy — canonical for ALL evals (v2)

The single source of truth is **`bench/profileopt/taxonomy.py`**. All move classification in this
repo uses it: `scripts/validate.py:speech_act` and the eval's labeler both delegate to
`taxonomy.classify` (single judge) or `taxonomy.majority_label` (3-judge).

## The 4 categories
| category | test |
|---|---|
| **approve** | acceptance/permission — no new content, no complaint (incl. thanks/greetings) |
| **critical** | asserts something is WRONG (bug/failure/wrong output/unwanted approach) |
| **directive** | tells the agent what to DO next, no fault asserted (new task / forward steer) |
| **inquiry** | asks for information/explanation, expecting an ANSWER |

`interrupt` is detected by regex (the `[INTERRUPT]` marker); its post-marker text is classified into
the 4-way, and a bare interrupt → `critical`.

## Why (chosen by κ-search)
Replaces the old 7-way (new_work, refine_redirect, pushback, bug_report, approve_proceed, question,
other), whose `new_work~refine_redirect` and `pushback~bug_report` boundaries were inherently
ambiguous. Mean pairwise inter-judge κ on a 120-item sample:

| panel | 7-way | **4-way (v2)** |
|---|---|---|
| cross-family (Haiku-4.5 / Opus-4.8 / GPT-5) | 0.681 | **0.805** |
| Claude-family (Haiku / Sonnet / Opus) | 0.647 | ~0.79 |

Full method + results: `bench/profileopt/FINDINGS_taxonomy.md`.

## Metric mapping (continuity)
`OLD_TO_NEW` (in `taxonomy.py`): approve_proceed→approve; pushback/bug_report/interrupt→critical;
new_work/refine_redirect→directive; question→inquiry; other→(none). So **approve% = approve** and
**critical% = critical** carry over unchanged.

## Usage
```python
import taxonomy
move = taxonomy.classify(text, prev_agent, backend="cli")          # single judge (CLI/subscription)
move = taxonomy.classify(text, prev_agent, model="anthropic/claude-haiku-4.5", backend="or")  # OpenRouter
move, per_judge = taxonomy.majority_label(text, prev_agent, backend="or")  # 3-judge majority (most robust)
```
Remap any legacy 7-way labels with `OLD_TO_NEW` if needed.
