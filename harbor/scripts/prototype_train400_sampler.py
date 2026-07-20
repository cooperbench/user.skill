#!/usr/bin/env python3
"""Prototype: allocate exactly B train human-user-turns across sessions.

Uses clean_manifest.json session lengths by default (no transcript I/O).
Optional ``--cutoff`` / ``--enforce-turn-end`` filters the train pool so
selected sessions are strictly earlier than an eval-session boundary
(leakage-safe packing). Recommended default strategy: ``sqrt_two_stage``.

Usage:
  python3 scripts/prototype_train400_sampler.py
  python3 scripts/prototype_train400_sampler.py --devs gh:scottdensmore,gh:ET-NoahDolev,dc:dc_000
  python3 scripts/prototype_train400_sampler.py --devs dc:dc_000 \\
      --cutoff 2026-05-14T21:39:36.728Z --enforce-turn-end
"""
from __future__ import annotations

import argparse
import json
import math
import statistics as st
from datetime import datetime, timezone
from pathlib import Path

HERE = Path("/data/swesimbench-v2-harbor")
MANIFEST = HERE / "clean_manifest.json"
SESSIONS_JSONL = HERE / "clean_sessions.jsonl"
EVAL62 = HERE / "meta" / "eval62_train_session_turn_counts.json"
B_DEFAULT = 400


def parse_ts(ts: str | None) -> datetime | None:
    if not ts:
        return None
    s = str(ts).replace("Z", "+00:00")
    if "." in s:
        head, rest = s.split(".", 1)
        frac = ""
        tz = ""
        for i, ch in enumerate(rest):
            if ch.isdigit():
                frac += ch
            else:
                tz = rest[i:]
                break
        s = f"{head}.{(frac + '000000')[:6]}{tz or '+00:00'}"
    try:
        dt = datetime.fromisoformat(s)
    except Exception:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def load_sessions(user_rec: dict) -> list[dict]:
    """Chronological train sessions with ≥1 human turn."""
    sess = [
        {"sid": x["sid"], "ts": x["ts"], "n": int(x["n"]), "repo": x.get("repo") or ""}
        for x in user_rec["train_sessions"]
        if int(x.get("n") or 0) >= 1
    ]
    sess.sort(key=lambda x: (x["ts"], x["sid"]))
    return sess


def load_session_max_turn_ts(sids: set[str], path: Path = SESSIONS_JSONL) -> dict[str, datetime]:
    """Map session_id -> max(turn.ts) for the requested sids (one JSONL scan)."""
    if not sids:
        return {}
    out: dict[str, datetime] = {}
    with open(path, "rb") as handle:
        for line in handle:
            if b'"session_id"' not in line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            sid = rec.get("session_id")
            if sid not in sids or sid in out:
                continue
            best = None
            for turn in rec.get("turns") or []:
                dt = parse_ts(turn.get("ts"))
                if dt is not None and (best is None or dt > best):
                    best = dt
            if best is not None:
                out[sid] = best
            if len(out) >= len(sids):
                break
    return out


def filter_sessions_before_cutoff(
    sessions: list[dict],
    cutoff: str,
    *,
    max_turn_ts: dict[str, datetime] | None = None,
) -> list[dict]:
    """Keep sessions strictly earlier than an eval-session cutoff.

    Always requires ``session.ts < cutoff`` (ISO strings / parsed datetimes).
    When ``max_turn_ts`` is provided, also requires ``max(turn.ts) < cutoff``
    so long-running train sessions cannot wall-clock-overlap the eval session.
    """
    cut = parse_ts(cutoff)
    if cut is None:
        raise ValueError(f"invalid cutoff timestamp: {cutoff!r}")
    kept = []
    for sess in sessions:
        st_dt = parse_ts(sess["ts"])
        if st_dt is not None and st_dt >= cut:
            continue
        if st_dt is None and str(sess["ts"]) >= cutoff:
            # string fallback for odd timestamps
            continue
        if max_turn_ts is not None:
            end = max_turn_ts.get(sess["sid"])
            if end is not None and end >= cut:
                continue
        kept.append(sess)
    return kept


def stratify_pick(sessions: list[dict], k: int) -> list[dict]:
    """Pick k sessions across time: longest session in each of k chrono bins.

    Breadth via time coverage; depth bias via max-n within bin (ties → earlier).
    """
    s = len(sessions)
    if k >= s:
        return list(sessions)
    if k <= 1:
        return [max(sessions, key=lambda x: (x["n"], x["ts"]))]
    bins: list[list[dict]] = [[] for _ in range(k)]
    for i, sess in enumerate(sessions):
        # map index into [0, k-1]
        b = min(k - 1, (i * k) // s)
        bins[b].append(sess)
    picked = []
    seen = set()
    for bucket in bins:
        if not bucket:
            continue
        best = max(bucket, key=lambda x: (x["n"], x["ts"], x["sid"]))
        if best["sid"] not in seen:
            seen.add(best["sid"])
            picked.append(best)
    # top up if empty bins / collisions
    if len(picked) < k:
        rest = sorted(
            (x for x in sessions if x["sid"] not in seen),
            key=lambda x: (-x["n"], x["ts"], x["sid"]),
        )
        for x in rest:
            picked.append(x)
            seen.add(x["sid"])
            if len(picked) >= k:
                break
    picked.sort(key=lambda x: (x["ts"], x["sid"]))
    return picked[:k]


def waterfill_prefixes(selected: list[dict], budget: int) -> list[dict]:
    """Equal base + remainder; short sessions capped; leftover redistributed.

    Returns list of {sid, ts, n, take, repo} with sum(take) == min(budget, total_n).
    """
    if not selected:
        return []
    caps = [s["n"] for s in selected]
    total_cap = sum(caps)
    target = min(budget, total_cap)
    k = len(selected)
    take = [0] * k

    # Round-robin deepen one turn at a time (contiguous prefix lengths).
    # Prefer sessions that still have capacity; stable order = chrono among selected.
    remaining = target
    while remaining > 0:
        progressed = False
        for i in range(k):
            if remaining <= 0:
                break
            if take[i] < caps[i]:
                take[i] += 1
                remaining -= 1
                progressed = True
        if not progressed:
            break

    return [
        {
            "sid": s["sid"],
            "ts": s["ts"],
            "n": s["n"],
            "take": take[i],
            "repo": s["repo"],
        }
        for i, s in enumerate(selected)
        if take[i] > 0
    ]


def alloc_round_robin(sessions: list[dict], budget: int) -> list[dict]:
    """Breadth-first: deepen all sessions in lockstep until budget met."""
    return waterfill_prefixes(sessions, budget)


def alloc_proportional(sessions: list[dict], budget: int, floor: int = 0, cap: int | None = None) -> list[dict]:
    """Allocate ∝ n_i with optional per-session floor/cap; then waterfill adjust."""
    s = len(sessions)
    if s == 0:
        return []
    total = sum(x["n"] for x in sessions)
    target = min(budget, total)
    raw = [target * x["n"] / total for x in sessions]
    # largest-remainder to integers
    base = [int(math.floor(r)) for r in raw]
    frac = sorted(range(s), key=lambda i: raw[i] - base[i], reverse=True)
    need = target - sum(base)
    for i in frac[:need]:
        base[i] += 1
    if floor:
        for i in range(s):
            if base[i] > 0 or sessions[i]["n"] >= floor:
                base[i] = max(base[i], min(floor, sessions[i]["n"])) if base[i] > 0 else base[i]
        # Re-normalize by clamping and waterfill on the support where base>0;
        # simpler: clamp to [0, cap] then waterfill among all with positive desire.
    takes = []
    for i, x in enumerate(sessions):
        t = base[i]
        if cap is not None:
            t = min(t, cap)
        t = min(t, x["n"])
        takes.append(t)
    # Fix sum via waterfill on selected (those with take>0, else top by n)
    selected = []
    for i, x in enumerate(sessions):
        if takes[i] > 0:
            selected.append({**x, "_soft": takes[i]})
    if sum(takes) < target:
        # include more sessions by n descending until capacity enough
        have = {s["sid"] for s in selected}
        for x in sorted(sessions, key=lambda z: (-z["n"], z["ts"])):
            if sum(s["n"] for s in selected) >= target:
                break
            if x["sid"] not in have:
                selected.append({**x, "_soft": 0})
                have.add(x["sid"])
    # Use soft targets as initial, then waterfill to exact budget
    selected.sort(key=lambda z: (z["ts"], z["sid"]))
    # seed with soft caps as max(take_soft, ...) via custom waterfill:
    # just waterfill with session caps — proportional only chose the *set* + soft preference
    # Prefer deepening sessions with higher soft first: order by -soft then chrono
    selected.sort(key=lambda z: (-z.get("_soft", 0), z["ts"], z["sid"]))
    out = waterfill_prefixes(selected, target)
    out.sort(key=lambda z: (z["ts"], z["sid"]))
    return out


def expand_until_capacity(sessions: list[dict], k: int, budget: int) -> list[dict]:
    """Stratify-pick K, then grow K until selected capacity ≥ budget (or K=S)."""
    s = len(sessions)
    k = max(1, min(k, s))
    target = min(budget, sum(x["n"] for x in sessions))
    while True:
        selected = stratify_pick(sessions, k)
        if sum(x["n"] for x in selected) >= target or k >= s:
            return selected
        k = min(s, k + max(1, k // 4))


def alloc_fixed_k(sessions: list[dict], budget: int, k: int) -> list[dict]:
    """Two-stage: stratify-pick K sessions, then equal-prefix waterfill to budget."""
    selected = expand_until_capacity(sessions, k, budget)
    return waterfill_prefixes(selected, budget)


def alloc_sqrt_two_stage(
    sessions: list[dict], budget: int, tight_margin: int = 80
) -> list[dict]:
    """Recommended: K = min(S, max(√B, √S)), stratify pick, prefix waterfill.

    Balances breadth and depth:
      - session-light (S ≤ √B): use all sessions, deepen
      - session-heavy: ~√S sessions (floored by √B), depth ≈ B/K
      - if stratified pick lacks capacity, grow K until ∑n ≥ B
      - if total train turns < B + tight_margin, use all sessions (scarce data)
    """
    s = len(sessions)
    if s == 0:
        return []
    total = sum(x["n"] for x in sessions)
    if total < budget + tight_margin:
        return waterfill_prefixes(sessions, budget)
    k_ideal = max(1, round(math.sqrt(budget)))
    k_breadth = max(1, round(math.sqrt(s)))
    k = min(s, max(k_ideal, k_breadth))
    return alloc_fixed_k(sessions, budget, k)


def alloc_sqrt_weights(sessions: list[dict], budget: int) -> list[dict]:
    """Allocate ∝ √n_i over all sessions (many zeros when S ≫ B); prefixes."""
    s = len(sessions)
    if s == 0:
        return []
    total = sum(x["n"] for x in sessions)
    target = min(budget, total)
    w = [math.sqrt(x["n"]) for x in sessions]
    sw = sum(w)
    raw = [target * wi / sw for wi in w]
    base = [int(math.floor(r)) for r in raw]
    frac = sorted(range(s), key=lambda i: raw[i] - base[i], reverse=True)
    need = target - sum(base)
    for i in frac:
        if need <= 0:
            break
        if base[i] < sessions[i]["n"]:
            base[i] += 1
            need -= 1
    # If still short (caps), waterfill among positive
    selected = [
        {**sessions[i], "_soft": base[i]}
        for i in range(s)
        if base[i] > 0
    ]
    if sum(base) < target:
        have = {x["sid"] for x in selected}
        for x in sorted(sessions, key=lambda z: (-math.sqrt(z["n"]), z["ts"])):
            if sum(s["n"] for s in selected) >= target:
                break
            if x["sid"] not in have:
                selected.append({**x, "_soft": 0})
                have.add(x["sid"])
    selected.sort(key=lambda z: (-z.get("_soft", 0), z["ts"], z["sid"]))
    out = waterfill_prefixes(selected, target)
    out.sort(key=lambda z: (z["ts"], z["sid"]))
    return out


STRATEGIES = {
    "round_robin": alloc_round_robin,
    "proportional": lambda sess, b: alloc_proportional(sess, b),
    "fixed_k20": lambda sess, b: alloc_fixed_k(sess, b, 20),
    "fixed_k_sqrtB": lambda sess, b: alloc_fixed_k(sess, b, max(1, round(math.sqrt(b)))),
    "sqrt_weights": alloc_sqrt_weights,
    "sqrt_two_stage": alloc_sqrt_two_stage,
}


def summarize(alloc: list[dict], budget: int, n_sessions_available: int) -> dict:
    takes = [a["take"] for a in alloc]
    return {
        "sessions_used": len(alloc),
        "sessions_available": n_sessions_available,
        "turns": sum(takes),
        "budget": budget,
        "mean_depth": round(st.mean(takes), 2) if takes else 0,
        "median_depth": st.median(takes) if takes else 0,
        "min_depth": min(takes) if takes else 0,
        "max_depth": max(takes) if takes else 0,
        "frac_full_session": round(
            sum(1 for a in alloc if a["take"] == a["n"]) / len(alloc), 3
        )
        if alloc
        else 0,
    }


def default_example_devs() -> list[str]:
    """Session-light, near-median, session-heavy from eval62 stats."""
    per = json.load(open(EVAL62))["per_dev"]
    by = sorted(per, key=lambda r: r["train_sessions_ge1"])
    return [by[0]["dev"], by[len(by) // 2]["dev"], by[-1]["dev"]]


def print_alloc(dev: str, strategy: str, sessions: list[dict], alloc: list[dict], budget: int):
    summ = summarize(alloc, budget, len(sessions))
    print(f"\n{'=' * 72}")
    print(f"{dev}  strategy={strategy}")
    print(
        f"  available: {summ['sessions_available']} sessions, "
        f"{sum(s['n'] for s in sessions)} human-turns"
    )
    print(
        f"  allocated: {summ['turns']}/{budget} turns across "
        f"{summ['sessions_used']} sessions | "
        f"depth min/med/mean/max = "
        f"{summ['min_depth']}/{summ['median_depth']}/{summ['mean_depth']}/{summ['max_depth']} | "
        f"full-session frac={summ['frac_full_session']}"
    )
    # show up to 25 rows; collapse middle if longer
    rows = alloc
    print(f"  {'take':>4}  {'n':>4}  {'ts':<24}  sid")
    if len(rows) <= 25:
        show_idxs = list(range(len(rows)))
    else:
        print(f"  (showing first 12 + last 8 of {len(rows)} sessions)")
        show_idxs = list(range(12)) + list(range(len(rows) - 8, len(rows)))
    prev = -1
    for i in show_idxs:
        if prev >= 0 and i > prev + 1:
            print("  ...")
        a = rows[i]
        marker = " *" if a["take"] == a["n"] else ""
        print(
            f"  {a['take']:>4}  {a['n']:>4}  {a['ts']:<24}  {a['sid'][:8]}…{marker}"
        )
        prev = i


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=int, default=B_DEFAULT)
    ap.add_argument(
        "--devs",
        default="",
        help="comma-separated developer ids (default: light/median/heavy from eval62)",
    )
    ap.add_argument(
        "--strategies",
        default="sqrt_two_stage,round_robin,fixed_k20,proportional,sqrt_weights",
        help="comma-separated strategy names",
    )
    ap.add_argument(
        "--json-out",
        default="",
        help="optional path to write full allocation JSON",
    )
    ap.add_argument(
        "--cutoff",
        default="",
        help=(
            "ISO timestamp: only sample train sessions with session.ts < cutoff. "
            "Use the eval held-session manifest ts (or a stricter eval-session start)."
        ),
    )
    ap.add_argument(
        "--enforce-turn-end",
        action="store_true",
        help=(
            "With --cutoff: also drop train sessions whose max(turn.ts) >= cutoff "
            "(scans clean_sessions.jsonl). Recommended for leakage-safe packs."
        ),
    )
    ap.add_argument(
        "--sessions-jsonl",
        default=str(SESSIONS_JSONL),
        help="path to clean_sessions.jsonl (for --enforce-turn-end)",
    )
    a = ap.parse_args()

    man = {u["user"]: u for u in json.load(open(MANIFEST))["users"]}
    devs = [d.strip() for d in a.devs.split(",") if d.strip()] or default_example_devs()
    strategies = [s.strip() for s in a.strategies.split(",") if s.strip()]

    max_turn_ts: dict[str, datetime] | None = None
    if a.enforce_turn_end:
        if not a.cutoff:
            raise SystemExit("--enforce-turn-end requires --cutoff")
        needed = set()
        for dev in devs:
            u = man.get(dev)
            if u:
                needed.update(x["sid"] for x in u["train_sessions"] if int(x.get("n") or 0) >= 1)
        print(f"loading max(turn.ts) for {len(needed)} train sessions...", flush=True)
        max_turn_ts = load_session_max_turn_ts(needed, Path(a.sessions_jsonl))
        print(f"loaded ends for {len(max_turn_ts)} sessions", flush=True)

    report = {
        "budget": a.budget,
        "cutoff": a.cutoff or None,
        "enforce_turn_end": bool(a.enforce_turn_end),
        "developers": {},
    }
    for dev in devs:
        u = man.get(dev)
        if not u:
            print(f"WARNING: {dev} not in clean_manifest", flush=True)
            continue
        sessions = load_sessions(u)
        n_before = len(sessions)
        turns_before = sum(s["n"] for s in sessions)
        if a.cutoff:
            sessions = filter_sessions_before_cutoff(
                sessions, a.cutoff, max_turn_ts=max_turn_ts
            )
            print(
                f"{dev}: cutoff pool {len(sessions)}/{n_before} sessions, "
                f"{sum(s['n'] for s in sessions)}/{turns_before} turns "
                f"(cutoff={a.cutoff}, turn_end={a.enforce_turn_end})",
                flush=True,
            )
        report["developers"][dev] = {
            "pool_sessions": len(sessions),
            "pool_turns": sum(s["n"] for s in sessions),
            "strategies": {},
        }
        for name in strategies:
            fn = STRATEGIES[name]
            alloc = fn(sessions, a.budget)
            assert sum(x["take"] for x in alloc) == min(
                a.budget, sum(s["n"] for s in sessions)
            ), (dev, name)
            print_alloc(dev, name, sessions, alloc, a.budget)
            report["developers"][dev]["strategies"][name] = {
                "summary": summarize(alloc, a.budget, len(sessions)),
                "alloc": alloc,
            }

    if a.json_out:
        Path(a.json_out).parent.mkdir(parents=True, exist_ok=True)
        json.dump(report, open(a.json_out, "w"), indent=2)
        print(f"\nwrote {a.json_out}", flush=True)


if __name__ == "__main__":
    main()
