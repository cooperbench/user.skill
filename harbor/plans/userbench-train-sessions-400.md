# UserBench — train-session context (400 human turns)

**Status:** design + prototype sampler (no eval rebuild)  
**Prototype:** [`scripts/prototype_train400_sampler.py`](../scripts/prototype_train400_sampler.py)  
**Example dump:** [`meta/train400_sampler_examples.json`](../meta/train400_sampler_examples.json)  
**Counts:** [`meta/eval62_train_session_turn_counts.json`](../meta/eval62_train_session_turn_counts.json)

---

## 1. Goal

Replace (or ablate against) the optional developer **style profile** skill with a **past training corpus** totaling **exactly 400 human user-turns**, sampled for both:

| Axis | Intent |
|------|--------|
| **Breadth** | Cover many distinct train sessions (repos, topics, time) |
| **Depth** | Keep **contiguous prefixes** within a session so dialogue context survives |

Eval tasks stay **noprofile** for the *held* conversation (`/sim/history.md`). The 400-turn pack is additional prior evidence of how this developer writes.

All 62 eval-eligible developers already have **≥400** train human-turns (median ~892; median ~84 train sessions; range 10–3347 sessions).

---

## 2. How train sessions / turns are stored

| Artifact | Role |
|----------|------|
| `clean_manifest.json` | Per-dev `train_sessions[]` / `held_sessions[]` with `{sid, ts, n, repo, …}` where **`n = human_turns`** (same units as `train_turns`) |
| `clean_sessions.jsonl` | Full scrubbed traces: `{session_id, user, turns:[{role,text,ts},…], …}` |
| `cohort.json` (via `prepare.py`) | Eval points + legacy `profile` = last `PROFILE_TURNS=40` predictable train turns (60-word trunc) |
| `export_train_markdown.py` → `train/<slug>/<sid>.md` | Train dumps in the same `> DEVELOPER` / `> AGENT` markdown as eval `history.md` (no word trunc) |
| Harbor `datasets/eval/*` | **noprofile** tasks: `environment/history.md` only; profiles optional via Harbor skills |

**Unit of budget:** one *human user-turn* = one counted unit of `n` / `train_turns` (not assistant/tool/system; not necessarily “predictable” — megapaste turns still count toward style corpus unless we filter later).

**Prefix rule (when packaging):** for allocation `take = a` on a session, emit all transcript turns from the start through the **a-th human user turn** (include intervening AGENT/TOOL/SYSTEM). Same formatter as `export_train_markdown.py` / `prepare.format_history_turn` (decide separately whether to word-truncate for token budget).

**Chronology:** train sessions satisfy `max(train_ts) < min(held_ts)` at **session-start** granularity. Sampling must stay within train sids only. For leakage-safe packs, also require `max(turn.ts) < eval_session.ts` per eval point (see [`userbench-train-leakage-audit.md`](userbench-train-leakage-audit.md)); do not assume a global per-dev train pool is safe for every held point.

---

## 3. Sampling options (ranked)

Budget `B = 400`. Let `S` = # train sessions with `n ≥ 1`, lengths `n_1…n_S`. Always emit **contiguous prefixes** of length `take_i ≤ n_i`, with `∑ take_i = B` (or all turns if total `< B`, which does not happen for the eval62 set).

### Rank 1 — **Recommended: sqrt two-stage** (`sqrt_two_stage`)

```text
if total_train_turns < B + 80:            # scarce-data escape
    selected ← all sessions
else:
    K ← min(S, max(round(√B), round(√S))) # √400=20; grows slowly with S
    selected ← stratify_pick(chrono, K)   # longest session in each of K time bins
    while ∑n(selected) < B and K < S:     # capacity repair
        K ← min(S, K + max(1, K//4))
        selected ← stratify_pick(chrono, K)
take[] ← waterfill_prefixes(selected, B)  # round-robin +1 until B or caps
```

**Waterfill:** repeatedly add one turn of depth to each selected session that still has capacity (`take_i < n_i`), in chronological order among the selected set, until `∑ take = B`.

**Why this wins**

- Single knob family (√) that auto-adapts light vs heavy session counts.
- Guarantees meaningful depth when `S` is large (unlike pure round-robin).
- Time-binned pick (longest session per bin) covers chronology without drowning in `n=1` fragments.
- Capacity repair + scarce-data escape handle short-session / tight-budget devs.
- Deterministic, cheap (manifest-only), easy to fingerprint in QC.

| Developer shape | Behavior |
|-----------------|----------|
| Session-light (S≈10–20) | `K=S` (and/or scarce escape), deepen; short sessions saturate (`take=n`); leftover deepens long ones. |
| Median (S≈84, turns≫400) | `K≈20`, mean depth ≈20. |
| Median but tight turns (~493) | Scarce escape → all sessions, near-full corpus. |
| Session-heavy (S≈1000+) | `K≈√S` (e.g. ~58 for S=3347), mean depth ≈`B/K` (~7). Still multi-turn prefixes, not 400×1. |

### Rank 2 — Fixed-K two-stage (`fixed_k20` / `fixed_k_sqrtB`)

Same as Rank 1 but `K` is a constant (e.g. 20 ≈ √B). Simpler to explain in a paper; slightly worse for mega-session users (less breadth than √S).

### Rank 3 — Round-robin over **all** sessions (`round_robin`)

Lockstep deepen every session. Excellent when `S ≤ B` and you want max breadth; **degenerates** when `S ≥ B` to `take=1` on B sessions (no dialogue depth). Reject as default for this corpus (dc:dc_000 has S=3347).

### Rank 4 — Square-root weights over all sessions (`sqrt_weights`)

`take_i ∝ √n_i` with largest-remainder, then prefix. Good depth×length coupling, but when `S ≫ B` most sessions get 0 and the active set is implicit/fragile; less controllable breadth than explicit K.

### Rank 5 — Length-proportional with floor/cap (`proportional`)

`take_i ∝ n_i`, optional floor/cap. Tends to dump budget into a few mega-sessions (scottdensmore has one session with n=311). Needs an explicit session cap (e.g. 40) or it becomes a depth-only method.

---

## 4. Edge cases

| Case | Handling |
|------|----------|
| Session shorter than equal share | Waterfill skips capped sessions; leftover deepens others |
| Many `n=1` sessions | Stratify still picks them; they contribute 1 turn of breadth; depth concentrates on longer picks |
| `∑ n == B` (tight: ~411 turns) | Nearly the full train corpus; still apply K-selection *or* take almost everything — prefer taking all sessions with waterfill (K=S) so nothing arbitrary is dropped when every turn matters |
| Mega-session (`n ≫ B/K`) | Prefix only — never mid-session slices or random turns |
| Empty / missing sid in `clean_sessions.jsonl` | Skip + redistribute (exporter already warns in export) |
| Token blow-up | Cap chars/words per turn when packaging (eval uses 200 words; train export uses none). Recommend a packaging cap (e.g. 200–400 words/turn) independent of the 400-turn *count* budget |

**Tight-budget refinement (optional):** if `train_turns < B + margin` (e.g. `< 480`), set `K=S` and waterfill over all sessions so sampling does not discard scarce data.

---

## 5. Harbor packaging (vs current noprofile)

Current ship path ([`packages/UserBench/README.md`](../packages/UserBench/README.md)):

- Tasks are **noprofile**: only `/sim/history.md` (held context).
- Style profiles are **optional Harbor skills** at job time (`--skill` / `agents[].skills`), not baked into the task twin.

For **400 turns of real dialogue**, skills are the wrong vehicle (size, latency, agent-skills UX). Prefer baking into the task environment like `history.md`.

### Recommended package shape

```text
datasets/eval-train400/<task>/
  instruction.md          # noprofile text + pointer to past sessions
  environment/
    Dockerfile            # COPY history.md + train/
    history.md            # held context (unchanged)
    train/
      _index.json         # [{sid, ts, repo, human_turns_take, path}, …] sum take=400
      <sid>.md            # prefix transcript, history.md format
  tests/…                 # unchanged gold / verifier
```

**Instruction delta** (kept short): after the existing history.md paragraph, add that prior sessions for this developer live under `/sim/train/` (see `_index.json`); skim or search them the same way; still output one next message to `/sim/answer.txt`.

**Do not** concatenate 400 turns into the instruction prompt. **Do not** replace noprofile with a baked style bullet list unless running that ablation.

### Condition matrix (suggested)

| Condition | Prior evidence | Task payload |
|-----------|----------------|--------------|
| `noprofile` (default today) | none | `/sim/history.md` |
| `profile-skill` | last-40 truncated turns | skill at job time |
| `train400` (new) | 400 human-turns, sqrt two-stage | `/sim/train/*` + instruction pointer |

Same task IDs / gold; only environment + instruction differ. Parallel GitHub eval work can keep shipping noprofile; `train400` can be a dataset twin built later.

### Alternatives rejected as default

| Idea | Why not default |
|------|-----------------|
| Harbor skill containing full 400-turn markdown | Too large; fights skill format |
| Single concatenated `past.md` | Harder to skim by session; OK as optional extra |
| Dev-level shared volume outside the task | Harbor tasks should be self-contained |

---

## 6. Pseudocode (recommended)

```python
def allocate_train400(train_sessions, B=400, tight_margin=80):
    # train_sessions: [{sid, ts, n}] with n = human_turns >= 1, sorted by (ts, sid)
    S = len(train_sessions)
    total = sum(s["n"] for s in train_sessions)
    B = min(B, total)

    if total < B + tight_margin:
        selected = list(train_sessions)
    else:
        K = min(S, max(round(sqrt(B)), round(sqrt(S))))
        while True:
            selected = stratify_pick(train_sessions, K)  # longest per time bin
            if sum(s["n"] for s in selected) >= B or K >= S:
                break
            K = min(S, K + max(1, K // 4))

    take = {s["sid"]: 0 for s in selected}
    caps = {s["sid"]: s["n"] for s in selected}
    left = B
    while left:
        progressed = False
        for s in selected:       # chronological among selected
            sid = s["sid"]
            if left and take[sid] < caps[sid]:
                take[sid] += 1
                left -= 1
                progressed = True
        if not progressed:
            break
    return [(sid, t) for sid, t in take.items() if t > 0]


def render_prefix(turns, human_take):
    """Include transcript through the human_take-th human user turn."""
    seen = 0
    out = []
    for t in turns:
        out.append(t)
        if is_human_user_turn(t):  # same predicate as clean human_turns
            seen += 1
            if seen >= human_take:
                break
    return format_history_md(out)  # > DEVELOPER / > AGENT / …
```

QC asserts: `sum(take)==min(B, eligible)`, all sids ⊆ train, `take_i ≤ n_i`, prefixes only, `session.ts` and `max(turn.ts)` strictly before the eval session cutoff, policy fingerprints unchanged.

---

## 7. Example allocations (prototype)

Command:

```bash
python3 scripts/prototype_train400_sampler.py \
  --devs gh:scottdensmore,gh:ET-NoahDolev,dc:dc_000 \
  --json-out meta/train400_sampler_examples.json
```

Measured under `sqrt_two_stage` (B=400); full sid tables in the JSON dump:

| Developer | Train S | Train turns | Sessions used | Depth min/med/mean/max |
|-----------|--------:|------------:|--------------:|------------------------|
| `gh:scottdensmore` (light) | 10 | 427 | 10 | 1 / 3.5 / 40 / 284 |
| `gh:ET-NoahDolev` (≈median S, tight turns) | 87 | 493 | 58 | 1 / 5 / 6.9 / 39 |
| `dc:dc_000` (heavy) | 3347 | 16584 | 58 | 3 / 7 / 6.9 / 7 |

Contrast: `round_robin` on `dc:dc_000` uses **400 sessions at depth 1** — breadth-only, poor dialogue context.

---

## 8. Implementation sketch (when building — not now)

1. Libraryize allocator from the prototype (seed/fingerprint fields).
2. `prepare.py` or a sibling: for each eval62 dev, compute allocation; optionally attach to `cohort.json` as `train400: [{sid, take},…]`.
3. `build_agentic.py --cond train400`: COPY `train/` into image; extend `INSTRUCTION`.
4. Token audit (cl100k) on packaged train packs — may need per-turn truncation.
5. Pilot N developers × both `noprofile` and `train400` before full twin publish.

**Out of scope for this note:** GitHub eval-set edits, full dataset rebuild, commits/publish.

---

## 9. Recommendation

Ship **`sqrt_two_stage`** as the train400 sampler: stratified session pick with `K = min(S, max(√B, √S))`, then contiguous-prefix waterfill to exactly 400 human turns. Package as **`/sim/train/`** beside noprofile `history.md`, not as a Harbor skill. Keep today’s style-profile skill as a separate ablation.
