"""κ-evaluation using THREE Claude-family judges via the local `claude` CLI (no OpenRouter).
Judges: Haiku-4.5, Sonnet-4.6, Opus-4.8. Re-baselines absolute κ (same-family agrees more) but
gives a fully-valid RELATIVE ranking of taxonomies. Reuses tax_eval's SAMPLE, kappa, _full_prompt."""
import hashlib, itertools, json, re, sys, threading, random
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(HERE))
import validate as V
import tax_eval as TE

JUDGES = {"haiku": "claude-haiku-4-5-20251001", "sonnet": "claude-sonnet-4-6", "opus": "claude-opus-4-8"}
CACHE = HERE / "tax_cli_cache.jsonl"
_LOCK = threading.Lock()
_C = None
# fixed 60-item subsample (CLI is slow); deterministic
random.seed(5)
_IDX = sorted(random.sample(range(len(TE.SAMPLE)), min(60, len(TE.SAMPLE))))
SAMPLE = [TE.SAMPLE[i] for i in _IDX]


def _cache():
    global _C
    if _C is None:
        _C = {}
        if CACHE.exists():
            for ln in CACHE.read_text().splitlines():
                if ln.strip():
                    r = json.loads(ln); _C[r["k"]] = r["v"]
    return _C


def _put(k, v):
    with _LOCK:
        _cache()[k] = v
        with CACHE.open("a") as f:
            f.write(json.dumps({"k": k, "v": v}) + "\n")


def _classify(judge, body, cats, item):
    fp = TE._full_prompt(body, item["prev_agent"], item["text"])
    k = f"{judge}:" + hashlib.sha256(fp.encode()).hexdigest()[:24]
    c = _cache()
    if k in c:
        return c[k]
    out = V.run_claude(fp, JUDGES[judge], timeout=90)
    if V.is_cli_failure(out):
        return None
    m = re.search(r'"act"\s*:\s*"([\w\-]+)"', out)
    a = m.group(1) if m else None
    lab = a if a in cats else ("other" if (a and "other" in cats) else None)
    if lab is not None:
        _put(k, lab)
    return lab


def evaluate(cand, workers=6):
    body, cats = cand["body"], cand["categories"]
    labels = {j: [None] * len(SAMPLE) for j in JUDGES}
    jobs = [(j, i) for j in JUDGES for i in range(len(SAMPLE))]

    def run(job):
        j, i = job
        return j, i, _classify(j, body, cats, SAMPLE[i])
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for fut in as_completed([ex.submit(run, jb) for jb in jobs]):
            j, i, lab = fut.result(); labels[j][i] = lab
    pairs = list(itertools.combinations(JUDGES, 2))
    ks = {}
    for a, b in pairs:
        k, po, n = TE.kappa(labels[a], labels[b]); ks[f"{a}-{b}"] = (k, po, n)
    valid = [v[0] for v in ks.values() if v[0] is not None]
    mean_k = round(sum(valid) / len(valid), 3) if valid else None
    conf = Counter()
    for a, b in pairs:
        for x, y in zip(labels[a], labels[b]):
            if x and y and x != y:
                conf[tuple(sorted((x, y)))] += 1
    cov = {j: sum(1 for l in labels[j] if l) for j in JUDGES}
    return {"name": cand["name"], "n_categories": len(cats), "mean_kappa": mean_k,
            "pairwise": {k: {"kappa": v[0], "raw": v[1], "n": v[2]} for k, v in ks.items()},
            "coverage": cov, "n_items": len(SAMPLE),
            "label_dist": {j: dict(Counter(l for l in labels[j] if l)) for j in JUDGES},
            "top_confusions": [{"pair": list(p), "n": c} for p, c in conf.most_common(8)]}


def main():
    baseline = {"name": "baseline-7way",
                "categories": ["new_work", "refine_redirect", "pushback", "bug_report", "approve_proceed", "question", "other"],
                "body": ("Classify the developer's conversational MOVE (speech act), ignoring the specific details/topic. Choose exactly one:\n"
                         "- new_work: introduces a NEW feature/task/requirement to build or document\n"
                         "- refine_redirect: steers or adjusts the CURRENT task; changes requirements\n"
                         "- pushback: corrects, rejects, or complains about the agent's output/approach\n"
                         "- bug_report: reports something broken or not behaving as expected\n"
                         "- approve_proceed: approves, says continue, commit/push, or moves on\n"
                         "- question: asks for information or clarification\n- other")}
    cands = [baseline] + json.loads((HERE / "candidates.json").read_text())
    results = [evaluate(c) for c in cands]
    (HERE / "tax_results_cli.jsonl").write_text("\n".join(json.dumps(r) for r in results) + "\n")
    print(f"\n===== RANKED (3 Claude-family judges, {len(SAMPLE)} items) =====")
    print(f"{'taxonomy':24s} {'#c':>3} {'meanκ':>7} {'h-s':>6} {'h-o':>6} {'s-o':>6}  coverage")
    for r in sorted(results, key=lambda r: -(r['mean_kappa'] or 0)):
        pw = r['pairwise']
        cov = "/".join(str(r['coverage'][j]) for j in JUDGES)
        print(f"{r['name']:24s} {r['n_categories']:>3} {str(r['mean_kappa']):>7} "
              f"{str(pw['haiku-sonnet']['kappa']):>6} {str(pw['haiku-opus']['kappa']):>6} {str(pw['sonnet-opus']['kappa']):>6}  {cov}")


if __name__ == "__main__":
    main()
