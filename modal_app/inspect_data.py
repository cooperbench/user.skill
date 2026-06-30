"""Spot-check one prepared training example from the volume."""
import json

import modal

from common import app, data_image, volume, VOL_MOUNT, DATA_DIR


@app.function(image=data_image, volumes={VOL_MOUNT: volume}, timeout=120)
def show(user_id: str = "marcus-sa"):
    from pathlib import Path

    p = Path(DATA_DIR) / user_id / "train.jsonl"
    with open(p) as f:
        first = json.loads(f.readline())
    msgs = first["messages"]
    print(f"session_id: {first['session_id']}")
    print(f"n messages: {len(msgs)}")
    print("=" * 60)
    for i, m in enumerate(msgs[:7]):
        print(f"--- [{i}] role={m['role']} ---")
        c = m["content"]
        if len(c) > 800:
            c = c[:800] + "...[trunc]"
        print(c)
        print()
    asst = [m["content"] for m in msgs if m["role"] == "assistant"]
    by_decision = {"interject": 0, "continue": 0, "other": 0}
    for a in asst:
        try:
            d = json.loads(a)
            by_decision[d.get("decision", "other")] = by_decision.get(d.get("decision", "other"), 0) + 1
        except Exception:
            by_decision["other"] += 1
    print(f"session asst breakdown: {by_decision}")


@app.local_entrypoint()
def main(user_id: str = "marcus-sa"):
    show.remote(user_id=user_id)
