#!/usr/bin/env python3
"""Harbor verifier: classify predicted + gold move with Composer 2.5 (Cursor Agent CLI).

Env:
  CURSOR_API_KEY   required
  CURSOR_AGENT_BIN optional path to `agent` / cursor-agent binary
  SIMBENCH_JUDGE   model slug (default composer-2.5)

Writes /logs/verifier/{verdict.json,reward.txt}.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import time

VDIR = "/logs/verifier"
os.makedirs(VDIR, exist_ok=True)

JUDGE = os.environ.get("SIMBENCH_JUDGE", "composer-2.5")
AGENT_BIN = (
    os.environ.get("CURSOR_AGENT_BIN")
    or shutil.which("agent")
    or "/opt/cursor-agent/versions/current/cursor-agent"
)
if not os.path.isfile(AGENT_BIN) and not shutil.which(AGENT_BIN):
    versions = "/opt/cursor-agent/versions"
    if os.path.isdir(versions):
        cands = sorted(
            (
                os.path.join(versions, d, "cursor-agent")
                for d in os.listdir(versions)
                if os.path.isfile(os.path.join(versions, d, "cursor-agent"))
            ),
            reverse=True,
        )
        if cands:
            AGENT_BIN = cands[0]

CATS = ["approve", "critical", "directive", "inquiry"]
BODY = (
    "Classify the developer's MOVE by the observable function of their message "
    "toward the agent's previous turn. Choose exactly one:\n"
    "- approve: acceptance/permission, no new content, no complaint "
    "(yes/ok/lgtm/go ahead/thanks).\n"
    "- critical: asserts something is WRONG — a bug/failure/wrong output, "
    "or the approach is mistaken/unwanted.\n"
    "- directive: tells the agent what to DO next with no fault stated — "
    "a new task/addition/forward steer.\n"
    "- inquiry: primarily asks for information/explanation, expecting an ANSWER.\n"
    "DECISION RULE (first match): 1 fault/error/dissatisfaction -> critical; "
    "2 asks for info -> inquiry; 3 requests action/change -> directive; 4 else -> approve."
)


def tw(t, n):
    return " ".join((t or "").split()[:n])


def composer(prompt: str, retries: int = 4) -> str:
    if not os.environ.get("CURSOR_API_KEY", "").strip():
        print("ERROR: CURSOR_API_KEY unset", flush=True)
        return ""
    bin_path = AGENT_BIN if os.path.isfile(AGENT_BIN) else shutil.which(AGENT_BIN)
    if not bin_path:
        print(f"ERROR: agent binary not found: {AGENT_BIN}", flush=True)
        return ""
    cmd = [
        bin_path,
        "-p",
        "--mode",
        "ask",
        "--model",
        JUDGE,
        "--trust",
        "--workspace",
        "/tmp",
        "--output-format",
        "text",
        prompt,
    ]
    env = os.environ.copy()
    # cursor-agent often needs its install dir on PATH/LD path
    agent_dir = os.path.dirname(os.path.realpath(bin_path))
    env["PATH"] = agent_dir + ":" + env.get("PATH", "")
    for a in range(retries):
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=240, env=env
            )
            text = (proc.stdout or "").strip()
            if proc.returncode == 0 and text:
                return text
            err = (proc.stderr or "")[:400]
            print(f"composer attempt {a}: rc={proc.returncode} err={err!r}", flush=True)
            if a < retries - 1:
                time.sleep(3 * (a + 1))
        except Exception as e:
            print(f"composer attempt {a}: {e}", flush=True)
            if a < retries - 1:
                time.sleep(3)
    return ""


def parse_act(out: str):
    if not out:
        return None
    out = out.strip()
    out = re.sub(r"^```(?:json)?\s*", "", out)
    out = re.sub(r"\s*```$", "", out)
    m = re.search(r'"act"\s*:\s*"(\w+)"', out)
    if m:
        a = m.group(1).lower()
        if a == "steer":
            a = "directive"
        return a if a in CATS else None
    found = re.findall(r'"(\w+)"', out)
    for a in found:
        a = a.lower()
        if a == "steer":
            a = "directive"
        if a in CATS:
            return a
    return None


def classify(text: str, prev: str):
    if not (text or "").strip():
        return None
    out = composer(
        "A developer is using an AI coding agent. The agent just said:\n"
        f"<agent>{tw(prev, 120)}</agent>\n\n"
        "The developer's next message was:\n"
        f"<message>{tw(text, 150)}</message>\n\n"
        f"{BODY}\n\n"
        'Respond with ONLY JSON: {"act":"<one label>"}'
    )
    return parse_act(out)


def main() -> None:
    gold = json.load(open("/tests/gold.json"))
    prev = gold.get("prev_agent", "")
    gold_move = gold.get("gold_move") or classify(gold.get("real", ""), prev)

    pred_text = ""
    for p in (
        "/sim/answer.txt",
        "/workspace/prediction.txt",
        "/logs/artifacts/prediction.txt",
    ):
        if os.path.exists(p):
            pred_text = open(p, encoding="utf-8", errors="replace").read().strip()
            break
    pred_move = classify(pred_text, prev) if pred_text else None

    match = bool(pred_move and gold_move and pred_move == gold_move)
    reward = 1.0 if match else 0.0
    verdict = {
        "point_id": gold.get("point_id"),
        "developer": gold.get("developer") or gold.get("dev"),
        "condition": gold.get("condition") or gold.get("variant"),
        "judge": JUDGE,
        "judge_backend": "cursor-agent",
        "agent_bin": AGENT_BIN,
        "predicted_msg": pred_text,
        "pred_move": pred_move,
        "gold_move": gold_move,
        "real_msg": gold.get("real", ""),
        "match": match,
        "reward": reward,
    }
    json.dump(verdict, open(f"{VDIR}/verdict.json", "w"), indent=1)
    open(f"{VDIR}/reward.txt", "w").write(str(reward))
    print(
        f"pred_move={pred_move} gold_move={gold_move} match={match} reward={reward}",
        flush=True,
    )
    print(f"predicted: {pred_text[:200]!r}", flush=True)


if __name__ == "__main__":
    main()
