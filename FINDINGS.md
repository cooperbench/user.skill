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
- **Metrics:** embedding cosine to the real message, LLM judge (content + style, 0–100), length
  ratio, and a 2-alternative forced-choice (2AFC) style-discrimination test (own vs. wrong folder,
  given a sample of the user's real messages; chance = 50%).

## Headline results

| Mode | 2AFC own-picked | users 2AFC>0.5 | own vs. wrong: style | own vs. wrong: content |
|---|---|---|---|---|
| **inline** | **80.4%** | **8/9** | **+9.2** | **+8.1** |
| folder | 53.6% | 5/9 | +4.3 | +3.0 |

## What we learned

1. **The distillation captures genuinely user-specific voice.** Given a sample of a user's real
   messages and two candidates — one from the user's own folder, one from a different user's folder
   — the judge picks the own-folder candidate **80.4%** of the time in inline mode, for **8 of 9
   users** (only `robouden` falls below chance). This is the cleanest test because own-vs-wrong
   holds "has a folder at all" constant; the only difference is *whose* folder.

2. **Inline beats folder-access for short-message role-play.** Pasting the whole folder into context
   discriminates much better (80.4%) than having the agent read the folder itself and decide what to
   use (53.6%). For a one-line reply, an agent reading 7 files tends to under-weight the terse style
   cues; full context keeps them present. (An earlier draft concluded the opposite — that was an
   artifact of corrupted inline data; see below.)

3. **The win is against the wrong user, not against a generic agent.** On style, the distilled
   folder (23.4) is close to the no-folder generic baseline (25.0) — a capable model already writes
   plausible developer messages. The folder's distinctive value is *specialization toward the right
   person*: it beats the **wrong** folder by +9.2 style / +8.1 content points. So the folder encodes
   *which* developer, more than it teaches the model to "sound like a developer" in general.

4. **Exact next-message prediction has a low ceiling.** Absolute judge scores are modest for every
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
