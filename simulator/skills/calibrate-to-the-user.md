---
name: calibrate-to-the-user
description: Pick each move at the rate THIS user actually makes it, using their stats.json and folder. Use on every turn to avoid collapsing into generic "approve" and to match the user's move-distribution.
---

# Calibrate to the user (applies to every move choice)

The single biggest fidelity lever is making the *right kind of move at the right rate* for this
specific person. Generic simulators over-approve; real users are diverse and individual.

## Read the user's propensities

From `users/<slug>/stats.json`:
- `intent_distribution` — their mix of `create new code` / `refactor` / `debug` / `understand` /
  `connect` / `git` / `test` / `other`. High `create new code` → they drive with `new_work`.
  High `debug` → they `bug_report` and `pushback` a lot. High `git` → frequent `approve_proceed`
  ("commit and push") beats.
- `pushback_distribution` — how often and which way they push back (`correction`, `rejection`,
  `failure_report`, `pacing_complaint`, `takeover`, `requirement_change`, `non_pushback`).
  A high non-`non_pushback` share → push back / interrupt more.

From `PREFERENCES.md` and `skills/` — concrete habits (do they plan first? interrupt? nitpick
naming? paste errors?).

## Apply it

- Don't pick `approve_proceed` by default. Pick it only when the user genuinely would *and* at about
  their rate. If their history is full of corrections and new specs, most turns should be those.
- Let the move distribution over a session approximate the user's: e.g. a heavy debugger produces
  many `bug_report`/`pushback` turns; a feature-driven founder produces many `new_work` turns; a
  hands-off user produces more `approve_proceed`.
- When unsure between two plausible moves, choose the one more characteristic of THIS user.

This skill governs *which* move; the other skills govern *how* to execute each move; `STYLE.md`
governs the *voice*.
