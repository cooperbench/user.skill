"""Move labeler for the profile-optimization scorer — now delegates to the v2 4-way taxonomy
(taxonomy.py), which raised inter-judge agreement from κ≈0.65 to κ≈0.78. See FINDINGS_taxonomy.md.

API (unchanged): label(text, prev_agent) -> (majority_move, {judge: move}).
Backend defaults to the local `claude` CLI judges (Haiku/Sonnet/Opus) since OpenRouter credits are
out; pass backend="or" to use Haiku/Opus/GPT-5 once the OpenRouter account is topped up."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import taxonomy as TAX

CATEGORIES = TAX.CATEGORIES
OLD_TO_NEW = TAX.OLD_TO_NEW


def label(text, prev_agent, backend="cli"):
    return TAX.majority_label(text, prev_agent, backend=backend)


def classify(text, prev_agent, model=None, backend="cli"):
    kw = {"backend": backend}
    if model:
        kw["model"] = model
    return TAX.classify(text, prev_agent, **kw)
