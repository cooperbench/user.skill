"""Evaluate a candidate move taxonomy by INTER-JUDGE agreement.

A candidate = {"name","categories":[...],"body": "<category defs + rules + examples>"}.
We run Haiku-4.5 + Opus-4.8 + GPT-5 with the same agent/message framing and the candidate's
body, then compute mean pairwise Cohen's κ over the fixed sample (bench/profileopt/tax_sample.json).

Reports: mean pairwise κ, per-pair κ, raw agreement, #categories, and top confusions.
Content-addressed cache (tax_eval_cache.jsonl) keyed by (judge, full-prompt hash, item id)."""
import hashlib, itertools, json, re, sys, threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "bench"))
import validate as V, orouter

JUDGES = {"haiku": "anthropic/claude-haiku-4.5", "opus": "anthropic/claude-opus-4.8", "gpt5": "openai/gpt-5"}
SAMPLE = json.loads((Path(__file__).resolve().parent / "tax_sample.json").read_text())
CACHE = Path(__file__).resolve().parent / "tax_eval_cache.jsonl"
_LOCK = threading.Lock()
_C = None


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


def _full_prompt(body, agent, msg):
    return ("A developer is using an AI coding agent. The agent just said:\n"
            f"<agent>{V.truncate_words(agent, 120)}</agent>\n\n"
            "The developer's next message was:\n"
            f"<message>{V.truncate_words(msg, 150)}</message>\n\n"
            f"{body}\n\n"
            'Respond with ONLY JSON: {"act": "<one label from the list>"}')


def _classify(judge, body, cats, item):
    fp = _full_prompt(body, item["prev_agent"], item["text"])
    k = f"{judge}:" + hashlib.sha256((fp).encode()).hexdigest()[:24]
    c = _cache()
    if k in c:
        return c[k]
    eff = None if judge == "haiku" else "low"
    out = orouter.chat(JUDGES[judge], fp, max_tokens=900, temperature=0, reasoning_effort=eff)
    m = re.search(r'"act"\s*:\s*"([\w\-]+)"', out)
    a = m.group(1) if m else None
    lab = a if a in cats else ("other" if (a and "other" in cats) else None)
    if lab is not None:
        _put(k, lab)
    return lab


def kappa(a, b):
    pairs = [(x, y) for x, y in zip(a, b) if x and y]
    if not pairs:
        return None, None, 0
    n = len(pairs); po = sum(1 for x, y in pairs if x == y) / n
    labs = set(x for x, _ in pairs) | set(y for _, y in pairs)
    ca, cb = Counter(x for x, _ in pairs), Counter(y for _, y in pairs)
    pe = sum((ca[l] / n) * (cb[l] / n) for l in labs)
    k = (po - pe) / (1 - pe) if pe < 1 else 1.0
    return round(k, 3), round(po, 3), n


def evaluate(cand, workers=12, verbose=True):
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
        k, po, n = kappa(labels[a], labels[b]); ks[f"{a}-{b}"] = (k, po, n)
    valid_ks = [v[0] for v in ks.values() if v[0] is not None]
    mean_k = round(sum(valid_ks) / len(valid_ks), 3) if valid_ks else None
    # top confusions across all judge pairs
    conf = Counter()
    for a, b in pairs:
        for x, y in zip(labels[a], labels[b]):
            if x and y and x != y:
                conf[tuple(sorted((x, y)))] += 1
    out = {"name": cand["name"], "n_categories": len(cats), "mean_kappa": mean_k,
           "pairwise": {k: {"kappa": v[0], "raw": v[1], "n": v[2]} for k, v in ks.items()},
           "label_dist": {j: dict(Counter(l for l in labels[j] if l)) for j in JUDGES},
           "top_confusions": [{"pair": list(p), "n": c} for p, c in conf.most_common(8)],
           "n_items": len(SAMPLE)}
    if verbose:
        print(f"\n=== {cand['name']}  ({len(cats)} cats)  mean κ = {mean_k} ===")
        for k, v in ks.items():
            print(f"  {k:12s} κ={v[0]}  raw={v[1]}  n={v[2]}")
        print("  top confusions:", ", ".join(f"{p['pair'][0]}~{p['pair'][1]}({p['n']})" for p in out["top_confusions"][:6]))
    return out


if __name__ == "__main__":
    # baseline: current 7-way (+other) definitions, NON-interrupt (interrupt handled by regex elsewhere)
    BASELINE = {
        "name": "baseline-7way", "categories": ["new_work", "refine_redirect", "pushback", "bug_report", "approve_proceed", "question", "other"],
        "body": (
            "Classify the developer's conversational MOVE (speech act), ignoring the specific "
            "details/topic. Choose exactly one:\n"
            "- new_work: introduces a NEW feature/task/requirement to build or document\n"
            "- refine_redirect: steers or adjusts the CURRENT task; changes requirements\n"
            "- pushback: corrects, rejects, or complains about the agent's output/approach\n"
            "- bug_report: reports something broken or not behaving as expected\n"
            "- approve_proceed: approves, says continue, commit/push, or moves on\n"
            "- question: asks for information or clarification\n"
            "- other"),
    }
    r = evaluate(BASELINE)
    Path(Path(__file__).resolve().parent / "tax_results.jsonl").open("a").write(json.dumps(r) + "\n")
