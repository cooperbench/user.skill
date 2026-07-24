#!/usr/bin/env python3
"""Re-aggregate the 2026-07-18 judge IRR snapshot without the DataClaw donors.

Reads the trial outputs already on disk in the annotator repo and writes
`public/data/judge_trials/irr_cross_summary_20260718_no_dataclaw.json`, which
the annotator dashboard loads. No judge run and no labeling run is repeated;
the dated all-100 snapshot stays next to it, untouched.

Kevin's side comes from the frozen `kevin_labels.json` captured with the
trials, not from Redis, so the exclusion is the only thing that moves between
the two files. As a guard, the unfiltered recompute must reproduce the shipped
snapshot before the filtered one is written.

Exclusion list: see `lib/cohort.ts` and `COHORT_POLICY.md` in the harbor repo.

    python3 scripts/build_irr_no_dataclaw.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ANNOTATOR = Path("/data/swesimbench-annotator")
TRIALS = ANNOTATOR / "public" / "data" / "judge_trials"
COMPOSER_DIR = TRIALS / "composer_irr_3x_20260718T233043Z"
LUNA_DIR = TRIALS / "luna_max_irr_3x_20260718T233043Z"
SHIPPED = TRIALS / "irr_cross_summary_20260718.json"

WEB = Path(__file__).resolve().parents[1]
ITEMS = WEB / "public" / "data" / "items.json"
OUT = WEB / "public" / "data" / "judge_trials" / (
    "irr_cross_summary_20260718_no_dataclaw.json"
)

EXCLUDED_DEVELOPER_SLUGS = {"dc_000", "dc_001", "dc_004", "dc_010"}

# Same metric code the dated snapshot was built with, so the two files stay
# comparable line for line.
sys.path.insert(0, str(ANNOTATOR / "scripts"))
from compute_irr_and_cross import (  # noqa: E402
    irr_three,
    label_stats,
    load_trial_dir,
    set_agreement,
)

TRIAL_NAMES = ["trial_1", "trial_2", "trial_3"]


def excluded_item_ids() -> set[str]:
    items = json.loads(ITEMS.read_text())
    return {
        it["id"]
        for it in items
        if str(it.get("developer", "")).split(":")[-1] in EXCLUDED_DEVELOPER_SLUGS
    }


def build(composer, luna, kevin, drop: set[str]) -> dict:
    keep = lambda d: {k: v for k, v in d.items() if k not in drop}  # noqa: E731
    composer = [keep(t) for t in composer]
    luna = [keep(t) for t in luna]
    kevin = keep(kevin)

    composer_irr = irr_three(composer, TRIAL_NAMES)
    luna_irr = irr_three(luna, TRIAL_NAMES)

    c1, l1 = composer[0], luna[0]
    ids_lc = sorted(set(c1) & set(l1))
    ids_k = sorted(i for i in kevin if i in c1 and i in l1)

    cross = {
        "primary_trial": "trial_1",
        "primary_note": (
            "trial_1 Composer = production gold_acts (composer-2.5 rejudge "
            "2026-07-18). trial_1 Luna = first independent luna-max pass. "
            "Kevin = labels frozen with the trials."
        ),
        "pairs": {
            "luna_vs_composer": set_agreement(
                [l1[i] for i in ids_lc], [c1[i] for i in ids_lc]
            ),
            "luna_vs_kevin": set_agreement(
                [l1[i] for i in ids_k], [kevin[i] for i in ids_k]
            ),
            "composer_vs_kevin": set_agreement(
                [c1[i] for i in ids_k], [kevin[i] for i in ids_k]
            ),
        },
        "label_stats": {
            "luna_primary": label_stats([l1[i] for i in ids_lc]),
            "composer_primary": label_stats([c1[i] for i in ids_lc]),
            "kevin": label_stats([kevin[i] for i in ids_k]),
            "luna_on_kevin_subset": label_stats([l1[i] for i in ids_k]),
            "composer_on_kevin_subset": label_stats([c1[i] for i in ids_k]),
        },
        "within_composer_irr": composer_irr["pairwise_avg"],
        "within_luna_irr": luna_irr["pairwise_avg"],
        "within_composer_n_way": composer_irr["n_way"],
        "within_luna_n_way": luna_irr["n_way"],
    }
    return {"within_composer": composer_irr, "within_luna": luna_irr, "cross": cross}


def main() -> None:
    composer = [load_trial_dir(COMPOSER_DIR / n) for n in TRIAL_NAMES]
    luna = [load_trial_dir(LUNA_DIR / n) for n in TRIAL_NAMES]
    kevin = json.loads((LUNA_DIR / "kevin_labels.json").read_text())

    plain = build(composer, luna, kevin, set())
    shipped = json.loads(SHIPPED.read_text())
    for section in ("within_composer", "within_luna"):
        if plain[section]["pairwise_avg"] != shipped[section]["pairwise_avg"]:
            raise SystemExit(
                f"recompute does not reproduce {SHIPPED.name} ({section}); "
                "check the trial dirs before trusting the filtered output"
            )
    for pair, got in plain["cross"]["pairs"].items():
        want = shipped["cross"]["pairs"][pair]
        if (got["n"], got["jaccard"], got["exact_pct"]) != (
            want["n"],
            want["jaccard"],
            want["exact_pct"],
        ):
            raise SystemExit(f"recompute does not reproduce {SHIPPED.name} ({pair})")

    drop = excluded_item_ids()
    filtered = build(composer, luna, kevin, drop)
    filtered["exclusion"] = {
        "developers": sorted(f"dc:{s}" for s in EXCLUDED_DEVELOPER_SLUGS),
        "items": len(drop),
        "reason": (
            "DataClaw donors, excluded from published metrics per COHORT_POLICY.md"
        ),
        "unfiltered_source": str(SHIPPED),
    }
    filtered["composer_dir"] = str(COMPOSER_DIR)
    filtered["luna_dir"] = str(LUNA_DIR)
    OUT.write_text(json.dumps(filtered, indent=2, ensure_ascii=False) + "\n")

    print(f"dropped {len(drop)} DataClaw items")
    for section in ("within_composer", "within_luna"):
        print(
            section,
            shipped[section]["n_items"],
            shipped[section]["pairwise_avg"],
            "->",
            filtered[section]["n_items"],
            filtered[section]["pairwise_avg"],
        )
    for pair in filtered["cross"]["pairs"]:
        a = shipped["cross"]["pairs"][pair]
        b = filtered["cross"]["pairs"][pair]
        print(
            pair,
            f"n={a['n']} J={a['jaccard']} exact={a['exact_pct']}",
            "->",
            f"n={b['n']} J={b['jaccard']} exact={b['exact_pct']}",
        )
    print("wrote", OUT)


if __name__ == "__main__":
    main()
