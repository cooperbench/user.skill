#!/usr/bin/env python3
"""Export full leak-safe train pools (all eligible sessions) for GitHub.

Per eval-620 developer:
  T* = min(held_sessions[].ts)
  include train session iff session.ts < T* AND max(turn.ts) < T*

Writes (default → user-simulator/train_pools/):
  train_pools/README.md
  train_pools/_registry.json
  train_pools/<slug>/
    _meta.json
    sessions.jsonl.gz   # one JSON object per session (turns included)

Hub variants (train400, train1000, …) subsample from this pool at publish time.
"""
from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
import tomllib
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path("/data/swesimbench-v2-harbor")
sys.path.insert(0, str(HERE / "scripts"))
sys.path.insert(0, "/data/claude-crawl")

from cohort_policy import is_human_target, scrub_text  # noqa: E402
from prototype_train400_sampler import (  # noqa: E402
    filter_sessions_before_cutoff,
    load_session_max_turn_ts,
    load_sessions,
    parse_ts,
)

MANIFEST = HERE / "clean_manifest.json"
SESSIONS_JSONL = HERE / "clean_sessions.jsonl"
SRC_EVAL = HERE / "datasets" / "eval-620"
DEFAULT_OUT = Path("/data/user-simulator/train_pools")


def slugify(dev: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", dev)


def task_developer(task_dir: Path) -> str:
    data = tomllib.loads((task_dir / "task.toml").read_text())
    return data["metadata"]["developer"]


def build_sid_offsets(path: Path, want: set[str]) -> dict[str, int]:
    sid_re = re.compile(rb'"session_id"\s*:\s*"((?:\\.|[^"\\])*)"')
    offsets: dict[str, int] = {}
    with open(path, "rb") as handle:
        while True:
            offset = handle.tell()
            line = handle.readline()
            if not line:
                break
            if b'"session_id"' not in line:
                continue
            match = sid_re.search(line)
            if not match:
                continue
            try:
                sid = json.loads(b'"' + match.group(1) + b'"')
            except Exception:
                continue
            if sid in want and sid not in offsets:
                offsets[sid] = offset
                if len(offsets) >= len(want):
                    break
    return offsets


def scrub_turns(turns: list) -> list[dict]:
    out = []
    for t in turns:
        out.append(
            {
                "role": t.get("role"),
                "text": scrub_text(t.get("text") or ""),
                "ts": t.get("ts"),
            }
        )
    return out


def max_turn_ts_str(turns: list) -> str | None:
    best = None
    for t in turns:
        dt = parse_ts(t.get("ts"))
        if dt is not None and (best is None or dt > best):
            best = dt
    if best is None:
        return None
    return best.isoformat().replace("+00:00", "Z")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--src-eval", type=Path, default=SRC_EVAL)
    ap.add_argument("--limit-devs", type=int, default=0)
    a = ap.parse_args()

    man = {u["user"]: u for u in json.load(open(MANIFEST))["users"]}
    task_dirs = sorted(
        p for p in a.src_eval.iterdir() if p.is_dir() and (p / "task.toml").exists()
    )
    by_dev: dict[str, list[Path]] = defaultdict(list)
    for td in task_dirs:
        by_dev[task_developer(td)].append(td)

    if a.limit_devs:
        keep = sorted(by_dev)[: a.limit_devs]
        by_dev = {k: by_dev[k] for k in keep}

    print(f"exporting full train pools for {len(by_dev)} developers → {a.out}", flush=True)

    needed: set[str] = set()
    tstar_by: dict[str, str] = {}
    eligible_meta: dict[str, list[dict]] = {}
    for dev in by_dev:
        u = man[dev]
        tstar = min(x["ts"] for x in u["held_sessions"])
        tstar_by[dev] = tstar
        needed.update(x["sid"] for x in u["train_sessions"] if int(x.get("n") or 0) >= 1)

    print(f"loading max(turn.ts) for {len(needed)} train sessions...", flush=True)
    max_turn_ts = load_session_max_turn_ts(needed, SESSIONS_JSONL)
    print(f"loaded ends for {len(max_turn_ts)}", flush=True)

    for dev in sorted(by_dev):
        u = man[dev]
        tstar = tstar_by[dev]
        pool = filter_sessions_before_cutoff(
            load_sessions(u), tstar, max_turn_ts=max_turn_ts
        )
        eligible_meta[dev] = pool
        print(
            f"  {dev}: {len(pool)} sessions / {sum(s['n'] for s in pool)} turns (T*={tstar})",
            flush=True,
        )

    want = {s["sid"] for pool in eligible_meta.values() for s in pool}
    print(f"indexing offsets for {len(want)} eligible sessions...", flush=True)
    offsets = build_sid_offsets(SESSIONS_JSONL, want)
    missing = sorted(want - set(offsets))
    if missing:
        raise SystemExit(f"missing offsets: {missing[:5]} ({len(missing)} total)")

    if a.out.exists():
        # only wipe pool subdirs / registry, keep if partial? full replace
        import shutil

        shutil.rmtree(a.out)
    a.out.mkdir(parents=True)

    registry = {
        "name": "UserBench leak-safe train pools",
        "exported_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "leak_rule": "T*=min(held.session.ts); include iff session.ts<T* AND max(turn.ts)<T*",
        "n_developers": len(by_dev),
        "hub_baseline": "userbench/UserBench@v2",
        "hub_variants_note": (
            "Harbor twins (UserBench-train400, future train1000, …) subsample "
            "from this pool at publish time via sqrt_two_stage; they do not "
            "ship the full pool."
        ),
        "developers": [],
    }

    total_sess = total_turns = 0
    for dev in sorted(by_dev):
        slug = slugify(dev)
        pool = eligible_meta[dev]
        tstar = tstar_by[dev]
        dev_dir = a.out / slug
        dev_dir.mkdir(parents=True)
        # Keep each gz under GitHub's 100 MiB hard limit.
        max_shard = 85 * 1000 * 1000  # keep each shard well under GitHub 100MB / 90MB soft cap
        written = []
        shard_files: list[str] = []
        shard_i = 0
        out_path = dev_dir / "sessions.jsonl.gz"
        out = gzip.open(out_path, "wt", encoding="utf-8")
        shard_files.append(out_path.name)
        n_since_check = 0

        with open(SESSIONS_JSONL, "rb") as src:
            for s in pool:
                src.seek(offsets[s["sid"]])
                rec = json.loads(src.readline())
                turns = scrub_turns(rec.get("turns") or [])
                n_human = sum(
                    1 for t in turns if t.get("role") == "user" and is_human_target(t)
                )
                end = max_turn_ts_str(turns)
                cut = parse_ts(tstar)
                st = parse_ts(s["ts"])
                et = parse_ts(end)
                if cut is None or (st is not None and st >= cut) or (
                    et is not None and et >= cut
                ):
                    out.close()
                    raise SystemExit(f"leakage while exporting {dev} {s['sid']}")
                row = {
                    "sid": s["sid"],
                    "ts": s["ts"],
                    "repo": s.get("repo") or "",
                    "n": n_human,
                    "max_turn_ts": end,
                    "turns": turns,
                }
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                written.append(
                    {
                        "sid": s["sid"],
                        "ts": s["ts"],
                        "repo": s.get("repo") or "",
                        "n": n_human,
                        "max_turn_ts": end,
                    }
                )
                n_since_check += 1
                if n_since_check >= 100:
                    out.flush()
                    if out_path.stat().st_size >= max_shard:
                        out.close()
                        # Rename first file into shard scheme once we overflow.
                        if shard_i == 0 and out_path.name == "sessions.jsonl.gz":
                            new0 = dev_dir / "sessions_000.jsonl.gz"
                            out_path.rename(new0)
                            shard_files[0] = new0.name
                        shard_i += 1
                        out_path = dev_dir / f"sessions_{shard_i:03d}.jsonl.gz"
                        out = gzip.open(out_path, "wt", encoding="utf-8")
                        shard_files.append(out_path.name)
                    n_since_check = 0
        out.close()

        turns_sum = sum(x["n"] for x in written)
        meta = {
            "developer": dev,
            "slug": slug,
            "Tstar": tstar,
            "leak_rule": "session.ts < T* AND max(turn.ts) < T*",
            "n_sessions": len(written),
            "n_human_turns": turns_sum,
            "sessions_file": shard_files[0] if len(shard_files) == 1 else None,
            "sessions_files": shard_files,
            "sessions": written,
            "n_eval_tasks": len(by_dev[dev]),
        }
        (dev_dir / "_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
        registry["developers"].append(
            {
                "developer": dev,
                "slug": slug,
                "Tstar": tstar,
                "n_sessions": len(written),
                "n_human_turns": turns_sum,
                "n_eval_tasks": len(by_dev[dev]),
                "path": slug,
            }
        )
        total_sess += len(written)
        total_turns += turns_sum
        gz_mb = sum((dev_dir / n).stat().st_size for n in shard_files) / 1e6
        print(
            f"wrote {slug}: {len(written)} sessions / {turns_sum} turns "
            f"({gz_mb:.1f} MB gz across {len(shard_files)} file(s))",
            flush=True,
        )

    registry["n_sessions"] = total_sess
    registry["n_human_turns"] = total_turns
    (a.out / "_registry.json").write_text(json.dumps(registry, indent=2) + "\n")

    readme = f"""# UserBench leak-safe train pools

Full per-developer **train** corpora for the public UserBench eval
([`userbench/UserBench@v2`](https://hub.harborframework.com/datasets/userbench/UserBench):
62 developers × 10 held tasks).

## Leakage invariant (always)

For each developer, let `T* = min(held_sessions[].ts)` (manifest session timestamp).

A train session is included **only if**:

1. `session.ts < T*`, **and**
2. `max(turn.ts) < T*`

Never include train sessions that wall-clock-overlap or follow the earliest held
session. This is stricter than the cohort’s session-start split alone.

## Layout

```text
train_pools/
  README.md
  _registry.json
    <slug>/                 # e.g. gh_winksaville, dc_dc_000
    _meta.json            # T*, session index, turn totals
    sessions.jsonl.gz     # one JSON object per eligible session
                          # (large developers may use sessions_XXX.jsonl.gz shards)
```

Each sessions JSONL line:

```json
{{"sid","ts","repo","n","max_turn_ts","turns":[{{"role","text","ts"}},...]}}
```

`n` is the human-target user-turn count (same units as the clean cohort
`train_sessions[].n`). Texts are policy-scrubbed.

## Harbor Hub variants

This directory is the **full pool**. Harbor twins **subsample** at publish time:

| Hub package | Budget | Sampler |
|-------------|-------:|---------|
| `userbench/UserBench-train400` | 400 human-turns | `sqrt_two_stage` |
| *(future)* `UserBench-train1000` etc. | 1000+ | same pool + sampler |

Packaging writes contiguous **prefixes** (through the *k*-th human turn,
including intervening AGENT/TOOL/SYSTEM) into each task’s `/sim/train/`.
The zero-train baseline `userbench/UserBench@v2` is unchanged and does **not**
ship this pool.

## Stats (this export)

| | |
|--|--:|
| Developers | {len(by_dev)} |
| Eligible sessions | {total_sess} |
| Eligible human-turns | {total_turns} |

See `_registry.json` for per-developer `T*` and sizes.
"""
    (a.out / "README.md").write_text(readme)
    print(
        f"\nDONE developers={len(by_dev)} sessions={total_sess} turns={total_turns} → {a.out}",
        flush=True,
    )


if __name__ == "__main__":
    main()
