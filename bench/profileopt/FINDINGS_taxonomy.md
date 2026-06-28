# Move-taxonomy optimization — raising inter-judge agreement

**Goal:** the move classifier underpinning CondAgree had only **κ≈0.65–0.69** inter-judge agreement
(Landis–Koch "substantial", below the 0.80 "reliable" bar) — and that ~0.04 label noise exceeded the
gains we'd chase. Optimize the taxonomy + classifier prompt to raise agreement.

## Result

A **4-way taxonomy replaces the 7-way**, raising mean pairwise κ from **0.647 → 0.779 (+0.13, ~+20%)**
on a fixed 120-item sample (real + osim-4b messages), judged by Haiku-4.5 / Sonnet-4.6 / Opus-4.8.
Agreement is now **balanced** (h-s 0.775, h-o 0.753, s-o 0.808) and the old disagreement *hub*
(`new_work~refine_redirect` + the `refine_redirect` cluster) is gone.

### Final taxonomy (v2)
| category | test |
|---|---|
| **approve** | pure acceptance / go-ahead — no instruction, no complaint |
| **critical** | explicitly states the work is defective (bug/error/failure/wrong/reject/revert) |
| **directive** | tells the agent to build/add/change/proceed-with-changes — no defect asserted |
| **inquiry** | asks for information/explanation/options — no defect asserted |

(`interrupt` stays regex-detected; its post-marker text is classified into the 4-way, bare → critical.)

The winning prompt's key move is **not merging alone** — naive merges just relocate disagreement
(e.g. `request~question`, `approve~request`). What worked is an **ordered decision rule with a sharp
"defect test"**: a message is `critical` only if it *explicitly asserts a defect*; merely changing
direction is `directive`. (An earlier variant that called every fix-request `critical` *lowered* κ.)

## How it was chosen
- κ-eval harness: `tax_eval.py` (3 judges, mean pairwise Cohen's κ, confusion) on `tax_sample.json`.
- Candidates authored by a workflow (6 strategies → critique → synthesis): `candidates.json`.
- Swept with Claude-family judges (`tax_eval_cli.py`); refined the winner (`run_refine.py`).

| taxonomy | #cats | mean κ |
|---|---|---|
| **axes4-defect-test (v2, FINAL)** | 4 | **0.779** |
| behavior-axes-4way | 4 | 0.786 (60-item; 0.77 balanced) |
| merge-4way-no-other | 4 | 0.778 |
| decision-tree-5way | 5 | 0.674 |
| merge-5way | 5 | 0.659 |
| baseline-7way | 7 | 0.647 |
| keep6-sharp-boundary | 6 | 0.571 |

5-way and 6-way variants did **not** beat the 7-way meaningfully — the reliable gain needs the 4-way
collapse of the two inherently-ambiguous distinctions (new vs refine work; pushback vs bug).

## Downstream continuity (site metrics preserved)
`OLD_TO_NEW` in `taxonomy.py`: approve_proceed→approve; pushback/bug_report/interrupt→critical;
new_work/refine_redirect→directive; question→inquiry; other→(none). So **approve% = approve** and
**critical% = critical** carry over directly; `directive`/`inquiry` replace the old active/question split.

## Caveats
- **Judges:** optimized with **Claude-family** judges (Haiku/Sonnet/Opus) because the OpenRouter
  account ran out of prepaid credits mid-sweep. The original κ≈0.69 was **cross-family**
  (Haiku/Opus/GPT-5). The relative +0.13 win is large and consistent across all three Claude judges
  and very likely holds cross-family (a 4-way is universally easier), but **cross-family confirmation
  with GPT-5 is pending an OpenRouter top-up** (`openrouter.ai/settings/credits`).
- Granularity tradeoff is intentional: the merged distinctions (new vs refine, pushback vs bug) were
  the unreliable ones and are not used by the headline metrics; the 4-way is exactly the
  approve/critical/directive/inquiry signal that matters.
- Residual confusions (now small, no hub): critical~inquiry, approve~directive, critical~directive.
