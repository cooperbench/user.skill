# Findings

Validation of the user-distillation pipeline on 9 stratified users (56 held-out prediction
points × 3 conditions × 2 generation modes). All 168×2 generations are clean. Full numbers in
`results/report.html`.

## Setup

- **Task:** held-out next-message prediction. The role-play agent sees a real conversation prefix
  and writes the user's next message.
- **Conditions:** `distilled` (the user's own folder), `generic` (no folder), `wrong` (a different
  user's folder).
- **Modes:** `inline` (folder text pasted into the prompt) and `folder` (the agent is pointed at
  `users/<slug>/` and reads it via the `roleplay-user` skill — the product flow).
- **Metrics:** embedding cosine to the real message; an LLM judge on three axes (content, style,
  realism — 0–100), where *style* = surface recognizability and *realism* = a plausible in-character
  message judged by intent/substance, explicitly **not** rewarding catchphrase mimicry; length
  ratio; and a 2-alternative forced-choice (2AFC) own-vs-wrong-folder test run under **both** a
  style and a realism criterion (chance = 50%).

## Headline results

The judge scores three axes — content, **style** (surface recognizability) and **realism**
(plausible in-character message, judged by intent/substance, *not* catchphrase mimicry) — and the
own-vs-wrong 2AFC is run under both a style and a realism criterion (9-user subset, rescored):

| Mode | 2AFC style | 2AFC realism | realism: own | realism: wrong |
|---|---|---|---|---|
| **inline** | **83.9%** | **76.8%** | 28.8 | 24.3 |
| folder | 62.5% | 58.9% | **30.4** | 29.5 |

(Earlier single-criterion style-2AFC numbers were inline 80.4% / folder 53.6%; the rescore with the
updated judge is consistent.)

## What we learned

1. **The distillation captures genuinely user-specific voice.** Given a sample of a user's real
   messages and two candidates — one from the user's own folder, one from a different user's folder
   — the judge picks the own-folder candidate **80.4%** of the time in inline mode, for **8 of 9
   users** (only `robouden` falls below chance). This is the cleanest test because own-vs-wrong
   holds "has a folder at all" constant; the only difference is *whose* folder.

2. **Inline beats folder-access on discrimination — but that is mostly *recognizability*.**
   Inline discriminates better under both criteria (style 83.9% vs 62.5%; realism 76.8% vs 58.9%).
   The reason is concrete: inline reproduces the user's **signature catchphrases** verbatim — e.g.
   asragab's `"looks good whats next"` appears identically across unrelated turns (44% of inline
   distilled generations are exact repeats, vs 36% in folder mode). A discrimination judge rewards
   that caricature.

3. **On realism, folder-access is actually better.** The per-record realism axis (plausible
   in-character message, ignoring phrase-parroting) *reverses* the mode ordering: folder-access
   distilled scores **30.4** vs inline **28.8**. The flexible folder-reading agent writes more
   natural, situationally-appropriate messages. So "inline is better" is specific to recognizability,
   not fidelity — inline is better at being *recognizable as* the user, folder-access at being
   *realistic for* the user.

4. **Realism is real but not user-discriminative.** Switching the 2AFC from a style to a realism
   criterion only narrows the inline–folder gap (style +21.4pts → realism +17.9pts); it does not flip
   it. Any 2AFC structurally rewards distinctiveness, and realism is *shared*: in folder mode even the
   wrong folder scores realistic (29.5, near the right folder's 30.4) because the agent grounds in the
   live conversation, and the no-folder generic baseline scores **highest of all** on realism (~34).
   To measure fidelity you must read the per-record realism/content scores, not a discrimination test.

5. **The win is against the wrong user, not against a generic agent.** A capable model already writes
   plausible developer messages, so the distilled folder barely beats the no-folder baseline on style
   or realism. Its distinctive value is *specialization toward the right person*: it beats the
   **wrong** folder under every criterion. The folder encodes *which* developer, more than it teaches
   the model to "sound like a developer" in general.

6. **Exact next-message prediction has a low ceiling.** Absolute judge scores are modest for every
   condition because many messages are plausible at any point; comparisons between conditions, not
   absolute scores, carry the signal.

## A bug worth recording

The first inline validation run was silently corrupted: it coincided with an API session-usage
limit, and 122/168 generations were the literal string *"You've hit your session limit…"* saved as
if they were predictions. The original error filter only caught outputs starting with `Error:` and
empty strings, so these polluted the scores (and made inline look no better than chance). The fix:
`is_cli_failure()` now detects session-limit / rate-limit / overload / max-turns markers anywhere in
the output; such generations are retried, never persisted as predictions, and excluded from scoring.
A gentle low-concurrency top-up driver (`scripts/topup_and_score.sh`) refilled all 168 cleanly. The
folder-mode run was unaffected (0 bad). **Lesson:** when an LLM is the data source, validate that
outputs are model text, not harness/CLI error strings — silent failures masquerade as weak results.

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
