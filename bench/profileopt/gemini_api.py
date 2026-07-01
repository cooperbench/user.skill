"""Minimal Gemini API (generativelanguage.googleapis.com) client for the scaling experiment.

Key from env GEMINI_API_KEY (never committed). Retries on 429/5xx with backoff; returns the
concatenated non-thought text parts, or "Error: ..." after exhausting retries (mirrors orouter.chat's
contract so scaling_history can reuse the bench's error handling).
"""
import json
import os
import time
import urllib.error
import urllib.request

BASE = "https://generativelanguage.googleapis.com/v1beta/models"
RETRIES = 5


def chat(model, prompt, max_tokens=4000, temperature=0.7, seed=None, thinking="HIGH"):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return "Error: GEMINI_API_KEY not set"
    gen_cfg = {"temperature": temperature, "maxOutputTokens": max_tokens,
               "thinkingConfig": {"thinkingLevel": thinking}}
    if seed is not None:
        gen_cfg["seed"] = int(seed)
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}],
                       "generationConfig": gen_cfg}).encode()
    url = f"{BASE}/{model}:generateContent?key={key}"
    last = "Error: no attempt"
    for i in range(RETRIES):
        try:
            req = urllib.request.Request(url, data=body,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as r:
                d = json.loads(r.read())
            cand = (d.get("candidates") or [{}])[0]
            parts = cand.get("content", {}).get("parts", [])
            txt = "".join(p.get("text", "") for p in parts if not p.get("thought")).strip()
            if txt:
                return txt
            last = f"Error: empty ({cand.get('finishReason')})"
        except urllib.error.HTTPError as e:
            code = e.code
            try:
                msg = json.loads(e.read()).get("error", {}).get("message", "")[:120]
            except Exception:
                msg = ""
            last = f"Error: HTTP {code} {msg}"
            if code == 429 or code >= 500:
                time.sleep(min(60, 2 ** i * 4))
                continue
            return last  # 4xx other than 429: don't hammer
        except Exception as e:  # timeouts, conn resets
            last = f"Error: {type(e).__name__}"
        time.sleep(min(30, 2 ** i * 2))
    return last
