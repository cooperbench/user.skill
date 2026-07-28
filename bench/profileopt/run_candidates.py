"""Evaluate inter-judge κ for all candidate taxonomies + the baseline, print a ranked table."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tax_eval as TE

cands = json.loads((HERE / "candidates.json").read_text())
cands = [TE.__dict__.get("BASELINE")] if False else cands
# include baseline
import importlib
baseline = {
    "name": "baseline-7way",
    "categories": ["new_work", "refine_redirect", "pushback", "bug_report", "approve_proceed", "question", "other"],
    "body": ("Classify the developer's conversational MOVE (speech act), ignoring the specific "
             "details/topic. Choose exactly one:\n"
             "- new_work: introduces a NEW feature/task/requirement to build or document\n"
             "- refine_redirect: steers or adjusts the CURRENT task; changes requirements\n"
             "- pushback: corrects, rejects, or complains about the agent's output/approach\n"
             "- bug_report: reports something broken or not behaving as expected\n"
             "- approve_proceed: approves, says continue, commit/push, or moves on\n"
             "- question: asks for information or clarification\n"
             "- other"),
}
allc = [baseline] + cands
results = []
for c in allc:
    results.append(TE.evaluate(c))
(HERE / "tax_results.jsonl").write_text("\n".join(json.dumps(r) for r in results) + "\n")

print("\n\n================ RANKED (mean inter-judge κ) ================")
print(f"{'taxonomy':26s} {'#cats':>5} {'meanκ':>7} {'h-o':>6} {'h-g':>6} {'o-g':>6}")
for r in sorted(results, key=lambda r: -(r['mean_kappa'] or 0)):
    pw = r['pairwise']
    print(f"{r['name']:26s} {r['n_categories']:>5} {str(r['mean_kappa']):>7} "
          f"{str(pw['haiku-opus']['kappa']):>6} {str(pw['haiku-gpt5']['kappa']):>6} {str(pw['opus-gpt5']['kappa']):>6}")
