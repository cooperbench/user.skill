#!/usr/bin/env python3
"""Reads /sim/answer.txt (agent output) + /tests/gold.json (hidden).
Classifies the predicted message's move with the PINNED JUDGE (4-way taxonomy).
If gold_move is null, classifies `real` with the same judge. Reward = 1.0 if match else 0.0.
Judge model is configurable via SIMBENCH_JUDGE (default: the pinned gemini-3.1-pro-preview)."""
import json, os, re, time, urllib.request, urllib.error

KEY = os.environ.get("GEMINI_API_KEY", "")
JUDGE = os.environ.get("SIMBENCH_JUDGE", "gemini-3.1-pro-preview")
CATS = ["approve", "critical", "directive", "inquiry"]
BODY = ("Classify the developer's MOVE by the observable function of their message toward the agent's previous turn. Choose exactly one:\n"
"- approve: acceptance/permission, no new content, no complaint (yes/ok/lgtm/go ahead/thanks).\n"
"- critical: asserts something is WRONG — a bug/failure/wrong output, or the approach is mistaken/unwanted.\n"
"- directive: tells the agent what to DO next with no fault stated — a new task/addition/forward steer.\n"
"- inquiry: primarily asks for information/explanation, expecting an ANSWER.\n"
"DECISION RULE (first match): 1 fault/error/dissatisfaction -> critical; 2 asks for info -> inquiry; 3 requests action/change -> directive; 4 else -> approve.")

def tw(t, n):
    w = (t or "").split()
    return " ".join(w[:n])

def gemini(prompt, retries=6):
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}],
                       "generationConfig": {"temperature": 0, "maxOutputTokens": 2048}}).encode()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{JUDGE}:generateContent?key={KEY}"
    for a in range(retries):
        try:
            d = json.load(urllib.request.urlopen(
                urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}), timeout=90))
            return "".join(p.get("text", "") for p in d.get("candidates", [{}])[0].get("content", {}).get("parts", []))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503) and a < retries - 1:
                time.sleep(4 * (a + 1)); continue
            return ""
        except Exception:
            if a < retries - 1:
                time.sleep(3); continue
            return ""
    return ""

def classify(text, prev):
    if not (text or "").strip():
        return None
    out = gemini(f"A developer is using an AI coding agent. The agent just said:\n<agent>{tw(prev,120)}</agent>\n\n"
                 f"The developer's next message was:\n<message>{tw(text,150)}</message>\n\n{BODY}\n\n"
                 'Respond with ONLY JSON: {"act":"<one label>"}')
    m = re.search(r'"act"\s*:\s*"(\w+)"', out)
    a = m.group(1) if m else None
    return a if a in CATS else None

gold = json.load(open("/tests/gold.json"))
prev = gold.get("prev_agent", "")
gold_move = gold.get("gold_move") or classify(gold.get("real", ""), prev)

pred_text = ""
try:
    pred_text = open("/sim/answer.txt").read().strip()
except Exception:
    pass
pred_move = classify(pred_text, prev) if pred_text else None

match = bool(pred_move and gold_move and pred_move == gold_move)
reward = 1.0 if match else 0.0

verdict = {
    "point_id": gold.get("point_id"),
    "developer": gold.get("developer"),
    "condition": gold.get("condition"),
    "judge": JUDGE,
    "predicted_msg": pred_text,
    "pred_move": pred_move,
    "gold_move": gold_move,
    "real_msg": gold.get("real", ""),
    "match": match,
    "reward": reward,
}
os.makedirs("/logs/verifier", exist_ok=True)
json.dump(verdict, open("/logs/verifier/verdict.json", "w"), indent=1)
open("/logs/verifier/reward.txt", "w").write(str(reward))
print(f"pred_move={pred_move} gold_move={gold_move} match={match} reward={reward}")
print(f"predicted: {pred_text[:200]!r}")
