#!/usr/bin/env python3
"""OpenAI-compatible client for the OSim (OdysSim) vLLM endpoints on Modal, plus
the model's NATIVE role-swapped prompt format.

OSim plays the human/user side: it is conditioned on a social-context system prompt
(who the developer is) and the *other party's* (coding agent's) turns, and generates
the next human (developer) turn. In a chat template the generated role is "assistant",
so we swap: agent turns -> role "user", the developer's own prior turns -> "assistant".
"""
import json
import re
import time
import urllib.error
import urllib.request

# filled in by the runner once `modal deploy` prints the URLs
ENDPOINTS = {
    "osim-8b": "https://kevinli020508--osim-eval-serve-8b.modal.run/v1",
    "osim-4b": "https://kevinli020508--osim-eval-serve-4b.modal.run/v1",
}
API_KEY = "osim-eval-key"

_THINK = re.compile(r"<think>.*?</think>", re.S)


def _clean(t: str) -> str:
    s = _THINK.sub("", t or "").strip()
    for tag in ("DEVELOPER:", "USER:", "Developer:", "User:", "Message:"):
        if s.startswith(tag):
            s = s[len(tag):].strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        s = s[1:-1].strip()
    return s


def build_osim_messages(point, folder_text, truncate_words, context_turn_words=200):
    """Role-swapped messages: system = social context (the developer persona),
    then the conversation with agent='user' and developer='assistant'. Consecutive
    same-role turns are merged so the chat template stays well-formed."""
    if folder_text:
        system = (
            "You are role-playing a specific real software developer who is using an AI "
            "coding agent. The profile below is who you are — your background, voice, "
            "preferences and how you drive a coding session.\n\n"
            f"{folder_text}\n\n"
            "Continue as this developer: read what the agent just did and write your next "
            "message to it, exactly as this developer would type it (their length, casing, "
            "typos and idiom). Output only the message."
        )
    else:
        system = (
            "You are role-playing a software developer using an AI coding agent. Read what "
            "the agent just did and write your next message to it — the move you would "
            "actually make (often new work, a redirect, a question, or a problem you "
            "noticed, not just approval). Output only the message."
        )
    # swap roles: SWE-chat user(=developer) -> assistant ; assistant(=agent) -> user
    swapped = []
    for t in point["context"]:
        role = "assistant" if t["role"] == "user" else "user"
        swapped.append({"role": role, "content": truncate_words(t["text"], context_turn_words)})
    # merge consecutive same-role
    merged = []
    for m in swapped:
        if merged and merged[-1]["role"] == m["role"]:
            merged[-1]["content"] += "\n\n" + m["content"]
        else:
            merged.append(dict(m))
    # the model must generate an "assistant" (developer) turn next, so the last
    # message should be a "user" (agent) turn; if not, append a nudge.
    if not merged or merged[-1]["role"] != "user":
        merged.append({"role": "user", "content": "[the agent is waiting for your next message]"})
    return [{"role": "system", "content": system}] + merged


def chat(model, messages, base_url=None, max_tokens=400, temperature=0.7, retries=4, timeout=180):
    base_url = base_url or ENDPOINTS[model]
    body = {
        "model": model, "messages": messages,
        "max_tokens": max_tokens, "temperature": temperature,
        # Qwen3: turn off thinking so we get just the user message
        "chat_template_kwargs": {"enable_thinking": False},
    }
    data = json.dumps(body).encode()
    last = ""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                base_url.rstrip("/") + "/chat/completions", data=data,
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                d = json.loads(r.read())
            ch = d.get("choices") or []
            if ch:
                c = _clean(ch[0].get("message", {}).get("content") or "")
                if c:
                    return c
            last = json.dumps(d.get("error") or {"empty": True})[:200]
        except urllib.error.HTTPError as e:
            try:
                last = f"HTTP {e.code}: {e.read().decode()[:200]}"
            except Exception:
                last = f"HTTP {e.code}"
        except Exception as e:  # noqa: BLE001
            last = f"{type(e).__name__}: {str(e)[:200]}"
        time.sleep(3 * (attempt + 1))  # cold start / warmup tolerance
    return f"Error: {last}"
