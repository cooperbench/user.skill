# Findings

Validation of the user-distillation pipeline on 9 stratified users (56 held-out prediction
points × 3 conditions × 2 generation modes). Full numbers in `results/report.html`.

## Setup

- **Task:** held-out next-message prediction. The role-play agent sees a real conversation prefix
  and writes the user's next message.
- **Conditions:** `distilled` (the user's own folder), `generic` (no folder), `wrong` (a different
  user's folder).
- **Modes:** `inline` (folder text pasted into the prompt; a controlled experiment) and `folder`
  (the agent is pointed at `users/<slug>/` and reads it via the `roleplay-user` skill — the actual
  product flow).
- **Metrics:** embedding cosine to the real message, LLM judge (content + style, 0–100), length
  ratio, and a 2-alternative forced-choice (2AFC) style-discrimination test (own vs. wrong folder,
  given a sample of the user's real messages; chance = 50%).

## Headline results

| Mode | own vs. wrong: style | own vs. wrong: content | 2AFC own-picked | users 2AFC>0.5 |
|---|---|---|---|---|
| inline | +0.2 | +1.1 | 51.8% | 4/9 |
| folder | **+4.3** | **+3.0** | **53.6%** | 5/9 |

## What we learned

1. **The folder carries real user-specific signal.** In both modes the agent given the user's own
   folder matches the real user better than when given a *different* user's folder — clearest in
   folder-access mode (style +4.3, content +3.0 on the 0–100 judge). This is the clean test, because
   own-vs-wrong holds the "has a folder at all" variable constant.

2. **Reading the folder beats pasting it in.** Folder-access mode (the real product flow) produced
   a larger own-vs-wrong gap *and* zero generation errors, versus a negligible gap and 5/168 errors
   for inline. Letting the agent actively read and internalize the folder works better than dumping
   8k words of persona into one prompt.

3. **The effect is strongly bimodal.** Stylistically distinctive users are captured near-perfectly
   (marcus-sa, ujuc, dipree, roo-oliv reach 1.0 in at least one mode); users with a generic terse
   "coder" voice sit at or below chance. Aggregate numbers average these two populations.

4. **A generic agent is a strong baseline.** "No folder" scores high — a capable model is already a
   decent generic next-message predictor, and in folder mode it can even edge out the distilled
   folder on raw content-match. Authentic terse style (e.g. answering "commit") often scores *lower*
   against a specific real message than a fluent generic guess does. The distillation's measurable
   value is **specialization toward the right person**, not beating a generic agent at guessing the
   exact next message.

5. **Exact next-message prediction has a low ceiling.** Absolute judge scores are low for every
   condition because many different messages are plausible at any point. Comparisons between
   conditions — not absolute scores — are where the signal lives.

## Limitations & next steps

- **Noisy wrong-pairing.** Each user is compared against a single rotated "wrong" user. Averaging
  over several wrong users per point would stabilize per-user 2AFC.
- **Judge model.** Scoring uses Haiku; a stronger judge would sharpen fine style discrimination.
- **Subset.** 9 users validated; the distillation itself ran for all 99. A full-cohort validation
  is a `validate.py --users 99` run away.
- **Response-side validation not done.** We validated the *requests* the simulated user produces.
  Validating that the coding agent *responds the same way* to a simulated vs. real user requires
  re-running the agent from each checkpoint's repo state — feasible with SWE-chat's
  `checkpoints`/`commits` tables, left as future work.
- **Style over content.** The distillation captures *voice* better than it predicts *what* the user
  will ask next — expected, since the next ask depends on project state the folder doesn't encode.
