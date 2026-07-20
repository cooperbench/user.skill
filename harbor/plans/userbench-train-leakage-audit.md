# UserBench train-context leakage audit

**Status:** complete (no Hub publish)  
**Date:** 2026-07-20  
**Artifacts:** [`meta/train_leakage_audit.json`](../meta/train_leakage_audit.json), [`meta/train_leakage_audit_cutoffs.json`](../meta/train_leakage_audit_cutoffs.json)  
**Sampler:** [`scripts/prototype_train400_sampler.py`](../scripts/prototype_train400_sampler.py) (`--cutoff`, `--enforce-turn-end`)

---

## Verdict

| Check | Result |
|-------|--------|
| Official train/held **session-start** split intact | **PASS** (68/68 developers) |
| Eval sessions ⊆ held, ∉ train (620 + 1520) | **PASS** |
| Train `session_id` never equals eval `session_id` | **PASS** |
| Train pack from **global** per-dev train pool cannot wall-clock-overlap some held sessions | **FAIL** (naive packing risk) |
| Train pack **conditioned on eval session** with `session.ts < cutoff` **and** `max(turn.ts) < cutoff` | **PASS** (prototype verified on 620) |
| Gold next-message text uniquely leaked via train transcripts | **PASS** (exact-string hits are generic phrases, not held-session copies) |

**Bottom line:** The clean cohort’s train/held **split labels** are chronologically sound at session-start granularity, and every current eval point’s session is held-only. A **naive** train400 pack that uses the developer’s full `train_sessions` list can still include train sessions whose **last turn timestamp** is at/after an earlier held session’s start — a real leakage risk for early held eval points. The train-context build must allocate **per eval point** (or per-dev with a global end-time floor of `min(held.session_ts)`).

---

## 1. Official train / held split rule

**Source of truth:** `/data/claude-crawl/census_cc.py::split`, re-checked in `build_clean_cohort.py`.

1. Per developer, collect sessions with ≥1 human target turn; sort by **session timestamp** ascending (`created_at` / `start_time` / equivalent → manifest `ts`).
2. Walk a boundary `b` from the end: `held = sessions[b:]`, `train = sessions[:b]`, choosing the latest `b` such that **held human-turns ≥ 100**, without placing equal-timestamp sessions on opposite sides of the cut.
3. Qualify developer if **train human-turns ≥ 400** and **held ≥ 100**.
4. Clean cohort asserts:
   - `max(train_ts) < min(held_ts)`
   - disjoint `session_id`s
   - no exact `trace_hash` crossing train/held

**Eval points** (`prepare.py`): carved only from **held** sessions; `point_id = "{session_id}#{turn_index}"` with gold = that human turn’s text; history = prior turns in the **same** held session.

**What “strictly earlier” means in the data model**

| Layer | Field | Meaning |
|-------|-------|---------|
| Split / manifest | `train_sessions[].ts`, `held_sessions[].ts` | Session-level timestamp used for the chronological cut (= `clean_sessions.start_time`) |
| Turn stream | `turns[].ts` | Per-message timestamps; **can start before or end after** `start_time` |
| Eval cutoff (recommended) | eval session’s manifest `ts` | Primary cutoff for packing |
| Eval cutoff (stricter) | `min(manifest_ts, min(turn.ts))` | Conservative when clocks / start_time disagree |

The shipped split **does not** enforce `max(train.turn.ts) < min(held.session_ts)`. That gap is the leakage surface for train-context packs.

---

## 2. Dataset coverage

| Set | Path | Tasks | Notes |
|-----|------|------:|-------|
| Current ship | `datasets/eval` (= `datasets/eval-620`) | 620 | Checked exhaustively |
| Full cohort slice | `datasets/eval-1520-full` | 1520 | Checked exhaustively |
| Developers in `clean_manifest.json` | — | 68 | All have train+held |

---

## 3. Per-eval-point checks

### 3.1 Structural (session identity / split membership)

| Check | 620 | 1520 |
|-------|----:|-----:|
| Eval developer missing from manifest | 0 | 0 |
| Eval `session_id` ∉ `held_sessions` | 0 | 0 |
| Eval `session_id` ∈ `train_sessions` | 0 | 0 |
| Train session with `session.ts ≥ eval.session.ts` | 0 | 0 |

**PASS** — global train-split membership is sufficient for *session-id* and *session-start* non-overlap with every eval point.

### 3.2 Wall-clock turn-end overlap (naive global train pool)

Count of eval points where **some** train-split session has `max(turn.ts) ≥ cutoff`:

| Cutoff definition | 620 | 1520 | Devs with any risk vs earliest held |
|-------------------|----:|-----:|------------------------------------:|
| Eval **manifest** `session.ts` | **53** | **121** | **13** |
| Conservative `min(manifest_ts, min(turn.ts))` | **143** | **369** | **47** |

Many “conservative” hits are inflated by held sessions whose earliest `turn.ts` precedes manifest `start_time` (39/47 turn-overlap developers show this quirk). The **manifest-cutoff** numbers are the actionable leakage signal under the official split field.

**Naive packing risk:** building one train pack from the full per-developer `train_sessions` list (as the prototype did before cutoffs) can include sessions that are train-labeled but still **active after** an early held session starts. Measured: **29/68** developers have at least one session in a global `sqrt_two_stage(B=400)` allocation whose `max(turn.ts)` is ≥ that developer’s earliest held `session.ts`.

### 3.3 Gold / later-turn content

| Check | 620 | 1520 | Interpretation |
|-------|----:|-----:|----------------|
| Exact normalized gold string appears as a train human turn | 13 | 35 | **Not session leakage** — all inspected hits are short repeated style phrases (`Commit and push all changes`, `Continue from where you left off.`, etc.) |
| Train turn shares eval `session_id` | 0 | 0 | **PASS** |
| Train pack includes later turns of the eval session | 0 | 0 | Impossible if sid-disjoint + prefix-from-other-sessions |

Dedup already forbids exact full-transcript hash copies across the split; repeated short commands are expected style evidence, not held-session spoilers.

### 3.4 Capacity under safe filters

| Pool rule | Points with &lt; 400 eligible train human-turns (620) |
|-----------|-----------------------------------------------------:|
| Train split only (global) | 0 |
| `session.ts < eval.manifest_ts` **and** `max(turn.ts) < eval.manifest_ts` | **0** |
| Same with conservative eval start | 38 (timestamp-quirk exclusions) |

So the safer **manifest** cutoff does **not** create a budget shortfall on the current 620 set. If total eligible turns ever fall below `B`, take all eligible turns (same scarce-data escape as the sampler).

---

## 4. Sampler: per-eval-point allocation

Extended prototype:

```bash
python3 scripts/prototype_train400_sampler.py \
  --devs dc:dc_000 \
  --cutoff 2026-05-14T21:39:36.728Z \
  --enforce-turn-end \
  --budget 400
```

- `--cutoff`: keep `train.session.ts < cutoff` (use that eval point’s held-session manifest `ts`).
- `--enforce-turn-end`: also drop sessions with `max(turn.ts) ≥ cutoff` (scans `clean_sessions.jsonl`).

Re-ran allocations for all **620** eval points with both filters: **0** allocations contained a late session-start or late turn-end relative to the point’s cutoff.

**Global per-dev pool vs per-point pool**

| Approach | Safe? | Notes |
|----------|-------|-------|
| One pack per developer from full `train_sessions` | **No** | Can include train sessions that wall-clock-overlap early held sessions |
| One pack per developer from sessions with `max(turn.ts) < min_held.session_ts` | **Yes** (for all that dev’s held points) | Smaller pool; same pack reused |
| **Pack per eval point** with `session.ts < eval.session.ts` and `max(turn.ts) < eval.session.ts` | **Yes (preferred)** | Maximally tight; more train data for later held points |

---

## 5. Required invariant for the train-context build

For each eval point with developer `D`, held session `S_eval`, manifest timestamp `T_eval = S_eval.ts`:

1. **Split membership:** every packed session `S` satisfies `S ∈ D.train_sessions` and `S.id ≠ S_eval.id`.
2. **Session-start earlier:** `S.ts < T_eval`.
3. **Turn-end earlier:** `max(S.turns[].ts) < T_eval` (skip session if turn timestamps missing only after failing closed, or treat missing as ineligible).
4. **Prefix-only packaging:** for allocation `take = k`, emit transcript from the start through the `k`-th human user turn — never mid-session slices, never turns from `S_eval`.
5. **Budget:** `sum(take) = min(B, eligible_turns)`; if eligible &lt; `B`, pack all eligible (do not dip into post-cutoff sessions).
6. **QC asserts** on every built task: (1)–(5), plus fingerprint that the eval gold human turn text is not present as a turn inside packed train files *from session `S_eval`* (sid check is enough).

Optional stricter cutoff: replace `T_eval` with `min(T_eval, min(S_eval.turns[].ts))` when start_time / turn clocks disagree.

**Do not** ship a developer-global train pack without the `max(turn.ts) < min(held.ts)` floor.

---

## 6. Count-agnostic naming

Agent-facing instructions should describe “earlier sessions under `/sim/train/`” without hardcoding the turn budget. The budget `B` (e.g. 400) remains a build-time sampler parameter, not prompt text. See [`userbench-train400-instruction.md`](userbench-train400-instruction.md).

---

## 7. Pass/fail summary

| Item | Pass/Fail |
|------|-----------|
| Manifest chronology `max(train_ts) < min(held_ts)` | **PASS** (0 violators) |
| Sid / hash train∩held empty | **PASS** |
| All eval points’ sessions held-only (620, 1520) | **PASS** |
| Naive global train400 pack leakage-safe for all held points | **FAIL** (53/620 points have train `max(turn.ts) ≥ eval.manifest_ts`; 29/68 devs affected in example global allocations) |
| Per-eval-point cutoff pack (`ts` + `max(turn.ts)`) | **PASS** |
| Recommended build invariant (§5) | **Required** |
