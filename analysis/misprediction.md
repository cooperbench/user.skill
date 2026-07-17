# Misprediction Analysis

I want to understand the biggest misprediction on the user actions.
Basically for each turn, can you analyze the difference between
the prediction and the user action, and tell me whether the prediction
itself is a reasonable guess.

My core hypothesis is that:

**LLMs are trained to complete tasks, instead of imitating human behaviors
so they are systematically homogenous instead of making decisions
based on the individual differences.**

Could you design experiments to test it.

<You can update this document to include plans>

---

## Plan (drafted 2026-07-16)

### Framing the hypothesis in our taxonomy

Every held-out user turn is labeled with one of four moves (`bench/profileopt/taxonomy.py`):
**approve** (accept/permit, no new content), **critical** (asserts something is wrong — old
pushback+bug_report+interrupt), **directive** (tells the agent what to do next — old
new_work+refine_redirect), **inquiry** (asks for an answer). "Task-completion homogeneity"
becomes three *falsifiable* claims about the simulator's predicted moves:

- **H1 — Central attractor (secondary; prompt-sensitive).** The model's *unprompted* default is
  task-completion: approve/directive over-produced, critical/inquiry under-produced. **Caveat
  found in the data:** our product simulator is heavily prompted *away* from approving ("do NOT
  default to approving"), and in the v5 `generic` records it actually *over*-produces
  critical/inquiry (pushback 13, question 13 of 56). So the *direction* of the marginal skew is an
  artifact of prompt engineering, not a clean read on the base model. H1 is therefore only
  testable on a **low-/no-prompt baseline** (see E7); on the product simulator, treat the marginal
  as descriptive, not as the hypothesis test.
- **H2 — Between-user variance collapse (primary).** Predicted per-user move-mixes are more
  similar to *each other* than real per-user mixes are. The model doesn't spread across
  individuals. Robust to prompting: even a simulator prompted to be assertive can still give
  *everyone* the same assertive mix.
- **H3 — Regression to the median developer (primary).** Each user's predicted mix sits closer to
  the population-average mix than their real mix does (shrinkage toward the average human). Also
  prompt-robust — it is about *spread around* the center, not *where* the center is.

H2/H3 are the load-bearing tests (prompt-invariant); H1 is descriptive unless run on E7's
low-prompt control. Labels in the records are the 7-way speech acts; the analysis folds them to
the 4 categories via `taxonomy.OLD_TO_NEW` (`other` → dropped).

If the model captured individual differences, the **distilled** condition (and context alone)
would reproduce each user's real mix and preserve the spread; homogeneity predicts the
**generic** condition ≈ one population mean for everyone.

### Data

Post-hoc analysis of the full-cohort validation records
(`results/validation_results.json` inline + `results/validation_results_folder.json` folder;
the ~57-user run prepped on the `kevin` branch). Each point carries: real text, a generation
per condition (**distilled / generic / wrong**), `real_act`, `pred_act`, `judge_{content,style,
realism}`, `cosine`. The three conditions are the lever: generic = no individual info (pure
task prior), distilled = individualized (product flow), wrong = a different individual.

### Experiments

**E1 — Per-turn misprediction audit (the direct ask).** For each point form `real_act →
pred_act`; severity = act mismatch weighted by low content/realism. Take the worst K per
condition. A stronger adjudicator (Sonnet/Opus judge, not Haiku) answers two things per point:
(a) **reasonableness** — is the prediction a plausible message *some* competent developer could
send here? (0/1 + reason); (b) **error type** ∈ {task-completion substitution (predicted
approve/keep-going where the real move was critical/interrupt/redirect), generic-not-specific
(right move, wrong *this user's* flavor), hallucinated content, underdetermined (both fine),
other}. **Headline:** among genuine misses, the share that are *task-completion substitution* +
*generic-not-specific*. The hypothesis predicts mispredictions are mostly **reasonable-in-general
but wrong-for-this-person** — failure of individuation, not competence.

**E2 — Marginal skew & confusion (H1, descriptive on the product simulator).** Aggregate the
`real_cat → pred_cat` confusion over the cohort. Report the net off-diagonal flow between
{approve,directive} and {critical,inquiry} with a two-sided sign test, and the predicted−real
marginal per category. Because the simulator is prompted away from approve (see H1 caveat), report
this as a *direction-of-skew description*; the clean approve-collapse test is E7's low-prompt arm.

**E3 — Between-user variance collapse (H2).** Per user, the 4-way mix for real vs predicted.
Metric: mean pairwise TVD across users. Compare spread(pred) vs spread(real) via a permutation
test. Report **generic** (no individuation) and **distilled** (attempted individuation)
separately — does the folder restore spread, or not?

**E4 — Regression to the median (H3).** Population-median mix p̄ from all real turns. Paired over
users: TVD(real_u, p̄) vs TVD(pred_u, p̄), Wilcoxon signed-rank. Prediction: predictions are
closer to p̄.

**E5 — Decision vs surface: does the folder change WHAT they do or only HOW it reads?** Across
distilled/generic/wrong, measure move-level distance to the user's real mix. If distilled shifts
`pred_act` toward real_u (and beats wrong), individuation is real. If move-agreement is flat
across conditions while `judge_style` differs, the folder personalizes only the *surface*
(catchphrases) and leaves the *decision* homogeneous — the exact signature the hypothesis
predicts, and consistent with FINDINGS points 2–3 (inline wins on recognizability, not fidelity).

**E6 — Confound control: underdetermination.** Alternative story: misses come from a low ceiling
(many messages plausible), not homogeneity. (a) Self-consistency — sample generic k times per
point; drop high move-entropy (underdetermined) points and re-run E2–E4; the distribution-level
claims should survive on the determined subset. (b) Note E3/E4 are distribution-level and robust
to per-point noise: pure underdetermination would still leave predicted and real *distributions*
matched, whereas homogeneity predicts a systematically *narrower* predicted distribution.

**E7 — Causal probe (optional, strongest).** Test the stated mechanism ("trained to complete
tasks, not imitate humans") by manipulation, reusing existing flags: compare generic default vs
an explicit "imitate THIS human, do not optimize the task" instruction vs move-conditioned
sampling from the user's real prior (`validate.py --move-conditioned --move-source sample`). If
(ii)/(iii) recover critical% and between-user variance, the homogeneity is an objective/prompt
artifact, not a capability ceiling.

### Falsifiable predictions (one-line scoreboard)

| # | Prediction if hypothesis TRUE |
|---|---|
| E2 | approve% pred > real; critical% pred < real |
| E3 | pairwise-TVD(pred) < pairwise-TVD(real) |
| E4 | TVD(pred, median) < TVD(real, median) |
| E5 | move-dist(distilled→real) ≈ move-dist(generic→real) while style differs |
| E6 | E2–E4 hold on the determined subset |

### Deliverables & dependencies

- **`scripts/misprediction.py` — built.** Reads any `validation_results*.json` (folds 7-way labels
  to 4 via `taxonomy.OLD_TO_NEW`), computes E2 (marginal/confusion), E3 (variance collapse, paired
  permutation test), E4 (median regression, Wilcoxon), E5 (decision-vs-surface verdict), and E1
  (worst-K audit). E2–E5 are pure offline stats (no scipy); E1's LLM adjudication is gated behind
  `--adjudicate --judge-model claude-sonnet-5`. Writes `analysis/misprediction_report.json` + a
  console verdict. Verified against `results/folder_v5samp_9users.json` (9-user smoke): E5 already
  reads `surface_only` there — folder lifts style but not move-fidelity.
- **Follow-ups:** an `.md`/`.html` render of the JSON (per-user mix, variance, shrinkage plots);
  E6 (self-consistency resampling) and E7 (low-prompt / move-conditioned control), which need new
  generation, not just the records.
- **Dependency:** E1–E5 are offline over the validation records — land the ~57-user cohort run
  first (prepped on `kevin`) for a powered result; the 9-user files only smoke-test the pipeline.
