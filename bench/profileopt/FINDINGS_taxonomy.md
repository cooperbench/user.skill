# Move-taxonomy optimization — raising inter-judge agreement

**Goal:** the move classifier underpinning accuracy had only **κ≈0.68 cross-family** inter-judge
agreement (Landis–Koch "substantial", below the 0.80 "reliable" bar) — and that label noise exceeded
the gains we'd chase. Optimize the taxonomy + classifier prompt to raise agreement.

## Result — confirmed cross-family

A **4-way taxonomy replaces the 7-way**, raising mean pairwise κ:

| judge panel | 7-way baseline | **4-way (v2, final)** | Δ |
|---|---|---|---|
| **cross-family** (Haiku-4.5 / Opus-4.8 / **GPT-5**) | 0.681 | **0.805** | **+0.12** |
| Claude-family (Haiku-4.5 / Sonnet-4.6 / Opus-4.8) | 0.647 | ~0.79 | +0.14 |

Cross-family the 4-way is **balanced and reliable-tier** (h-o 0.784, h-g 0.774, o-g 0.856), and the
old disagreement *hub* (`new_work~refine_redirect` + the `refine_redirect` cluster) is gone.

### Final taxonomy (v2)
| category | test |
|---|---|
| **approve** | acceptance/permission — no new content, no complaint (incl. thanks/greetings) |
| **critical** | asserts something is WRONG (bug/failure/wrong output/unwanted approach) |
| **directive** | tells the agent what to DO next, no fault asserted (new task / forward steer) |
| **inquiry** | asks for information/explanation, expecting an ANSWER |

(`interrupt` stays regex-detected; its post-marker text is classified into the 4-way, bare → critical.)

The winning prompt (`behavior-axes-4way`) frames each move by its **observable function** and applies
an **ordered decision rule whose first test is "is a fault asserted?"** — a neutral change of
approach ("use AST instead") is `directive`; only a stated defect ("regex misses nested cases") is
`critical`. **Merging alone did not help** (it relocates disagreement to `request~question` /
`approve~request`); the fault-first rule is what works.

## How it was chosen
- κ-eval harness: `tax_eval.py` (cross-family, OpenRouter) / `tax_eval_cli.py` (Claude-family, CLI),
  mean pairwise Cohen's κ + confusion on `tax_sample.json` (120 real+osim-4b items).
- Candidates authored by a workflow (6 strategies → critique → synthesis): `candidates.json`.
- Swept, then **confirmed cross-family** (the panel that motivated the work):

| taxonomy | #cats | cross-family κ |
|---|---|---|
| **behavior-axes-4way (FINAL)** | 4 | **0.805** |
| axes4-defect-test (a refinement) | 4 | 0.730 |
| merge-4way-no-other | 4 | 0.716 |
| baseline-7way | 7 | 0.681 |

Important: selection on the Claude-family panel preferred a "defect-test" refinement, but the
**cross-family panel (with GPT-5) preferred the original behavior-axes body** (0.805 vs 0.730) — so the
final lock is made on the cross-family panel. 5-/6-way variants did not beat the 7-way meaningfully;
the reliable gain needs the 4-way collapse of the two inherently-ambiguous distinctions (new vs
refine work; pushback vs bug).

## Downstream continuity (site metrics preserved)
`OLD_TO_NEW` in `taxonomy.py`: approve_proceed→approve; pushback/bug_report/interrupt→critical;
new_work/refine_redirect→directive; question→inquiry; other→(none). So **approve% = approve** and
**critical% = critical** carry over directly; `directive`/`inquiry` replace the old active/question split.

## Caveats
- The 4-way intentionally drops the new-vs-refine and pushback-vs-bug distinctions — these were the
  *unreliable* ones and are not used by the headline metrics; the 4-way is exactly the
  approve/critical/directive/inquiry signal that matters.
- Residual confusions (now small, no hub): critical~inquiry, approve~directive, critical~directive.
- κ ceiling: even two strong models only reach ~0.86 (opus–gpt5); ~0.80 cross-family is about as
  reliable as this move-labeling task gets without multi-label or human adjudication.
- Wired into the profile-opt labeler (`judges.py` → `taxonomy.py`). Switching the published
  benchmark/site to v2 requires re-labeling under the 4-way (follow-up).
