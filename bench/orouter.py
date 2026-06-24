#!/usr/bin/env python3
"""Minimal OpenRouter chat client (dependency-free) for the v0 user-sim benchmark.

Key is read from $OPENROUTER_API_KEY or the repo-root .env (gitignored). One function:
`chat(model, prompt, ...) -> str`. Returns the assistant message text, or a string
starting with "Error:" on failure (callers filter these with validate.is_cli_failure).
"""

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

API = "https://openrouter.ai/api/v1/chat/completions"
_KEY_CACHE = None


def _key():
    global _KEY_CACHE
    if _KEY_CACHE:
        return _KEY_CACHE
    k = os.environ.get("OPENROUTER_API_KEY")
    if not k:
        envf = Path(__file__).resolve().parent.parent / ".env"
        if envf.exists():
            for line in envf.read_text().splitlines():
                if line.strip().startswith("OPENROUTER_API_KEY="):
                    k = line.split("=", 1)[1].strip()
                    break
    if not k:
        raise SystemExit("set OPENROUTER_API_KEY (env or .env)")
    _KEY_CACHE = k
    return k


def chat(model, prompt, system=None, max_tokens=1000, temperature=0.7,
         reasoning_effort="low", seed=None, retries=4, timeout=180):
    """One chat completion. reasoning_effort='low' keeps reasoning models from spending
    the whole budget before emitting the (short) user message; ignored by non-reasoning
    models. Retries transient errors / empty content with backoff."""
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": prompt})
    body = {"model": model, "messages": msgs, "max_tokens": max_tokens,
            "temperature": temperature}
    if reasoning_effort:
        body["reasoning"] = {"effort": reasoning_effort}
    if seed is not None:
        body["seed"] = seed
    data = json.dumps(body).encode()
    last = ""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                API, data=data,
                headers={"Authorization": f"Bearer {_key()}",
                         "Content-Type": "application/json",
                         "X-Title": "user.skill-v0-bench"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                d = json.loads(r.read())
            ch = d.get("choices") or []
            if ch:
                msg = ch[0].get("message", {}) or {}
                c = (msg.get("content") or "").strip()
                if c:
                    return c
                # empty content (e.g. reasoning ate the budget): retry with more room
                body["max_tokens"] = min(4000, int(body["max_tokens"] * 2))
                data = json.dumps(body).encode()
            last = json.dumps(d.get("error") or {"empty": True})[:200]
        except urllib.error.HTTPError as e:
            try:
                last = f"HTTP {e.code}: {e.read().decode()[:200]}"
            except Exception:
                last = f"HTTP {e.code}"
            if e.code in (400, 401, 403, 404):
                break  # not transient
        except Exception as e:  # noqa: BLE001
            last = f"{type(e).__name__}: {str(e)[:200]}"
        time.sleep(1.5 * (attempt + 1))
    return f"Error: {last}"
