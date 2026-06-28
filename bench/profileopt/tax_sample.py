"""Persist a fixed, stratified sample of NON-INTERRUPT (prev_agent, message) items for the
taxonomy κ-search. Items = real held-out messages + osim-4b generations from the v0_1 cache.
Interrupts are excluded (they're regex-determined downstream; the taxonomy search is about the
LLM-classified categories, where the disagreement lives)."""
import json, sys, random
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "bench"))
import validate as V, v0_1

C = {}
for l in open(ROOT / "bench/results/v0_1_raw.jsonl"):
    if l.strip():
        r = json.loads(l); C[r["key"]] = r
pts = {p["point_id"]: p for p in v0_1.load_points(50)}

items = []  # {id, kind, text, prev_agent, base_move}
for pid, p in pts.items():
    pa = p["prev_agent"]
    rl = C.get(f"label|real|{pid}", {}).get("move")
    if rl and rl != "interrupt" and not V.is_interrupt(p["real"]):
        items.append({"id": f"real|{pid}", "kind": "real", "text": p["real"], "prev_agent": pa, "base_move": rl})
    g = C.get(f"gen|{pid}|osim-4b|distilled", {})
    sl = C.get(f"label|osim-4b|distilled|{pid}", {}).get("move")
    if g.get("text") and sl and sl != "interrupt" and not V.is_interrupt(g["text"]) and not V.is_cli_failure(g["text"]):
        items.append({"id": f"sim|{pid}", "kind": "sim", "text": g["text"], "prev_agent": pa, "base_move": sl})

# stratify by base_move (existing 7-way), ~equal per class, cap ~120
random.seed(11)
by = defaultdict(list)
for it in items:
    by[it["base_move"]].append(it)
sample = []
per = max(1, 120 // max(1, len(by)))
for mv, lst in by.items():
    random.shuffle(lst)
    sample += lst[:per + 6]   # a few extra for rarer classes
random.shuffle(sample)
sample = sample[:120]
Path(ROOT / "bench/profileopt/tax_sample.json").write_text(json.dumps(sample, indent=1, ensure_ascii=False))
from collections import Counter
print(f"sample: {len(sample)} non-interrupt items (real+sim)")
print("base-move strata:", dict(Counter(it["base_move"] for it in sample)))
print("kinds:", dict(Counter(it["kind"] for it in sample)))
