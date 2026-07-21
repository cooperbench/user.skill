#!/usr/bin/env python3
"""Harbor verifier for UserBench multi-label act scoring.

Composer 2.5 classifies both the held-out developer message and the predicted
message into non-empty subsets of {approve, critical, steer, inquiry}. The
primary reward is Jaccard/IoU over those sets. Invalid or empty output scores 0.

The evaluator must provide CURSOR_API_KEY. No task contains credentials.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import time

VDIR = os.environ.get("SIMBENCH_VERIFIER_LOG_DIR", "/logs/verifier")
TESTS_DIR = os.environ.get("SIMBENCH_TESTS_DIR", "/tests")
SIM_DIR = os.environ.get("SIMBENCH_SIM_DIR", "/sim")
os.makedirs(VDIR, exist_ok=True)

JUDGE = os.environ.get("SIMBENCH_JUDGE", "composer-2.5")
AGENT_BIN = (
    os.environ.get("CURSOR_AGENT_BIN")
    or shutil.which("agent")
    or shutil.which("cursor-agent")
    or "/opt/cursor-agent/versions/current/cursor-agent"
)
if not os.path.isfile(AGENT_BIN) and not shutil.which(AGENT_BIN):
    versions = "/opt/cursor-agent/versions"
    if os.path.isdir(versions):
        candidates = sorted(
            (
                os.path.join(versions, version, "cursor-agent")
                for version in os.listdir(versions)
                if os.path.isfile(
                    os.path.join(versions, version, "cursor-agent")
                )
            ),
            reverse=True,
        )
        if candidates:
            AGENT_BIN = candidates[0]

ACTS = ["approve", "critical", "steer", "inquiry"]
ACT_SET = set(ACTS)
TAXONOMY_PROMPT = """\
Classify the developer's communicative ACTS by the observable function(s) of their message toward the agent's previous turn. Free multi-label: select EVERY act that applies (non-empty subset). Multiple acts are OK when a turn does several things (e.g. asks a question AND assigns a new task).

Acts:
- approve: greenlight the *current* proposal — proceed with what was already offered. Examples: go ahead; LGTM; "can you work on this/these?"; yes/ok/thanks as go-ahead; conditional "fine if X". No new task beyond that proposal.
- critical: asserts fault (something is WRONG) — not merely proposing an alternative. Examples: bug; wrong output; still failing; wrong approach; correcting a misunderstanding. Proposing a different plan without asserting fault → steer, not critical.
- steer: change *what to build/do* next — a NEW or DIFFERENT task from the current proposal (not mere go-ahead; not "go verify a fact"). May be phrased as a question ("can you…?"); still steer, not inquiry, when the ask is new/different work.
- inquiry: want information or confirmation (an answer), not a new build/do ask. Examples: status/why/what happened; "confirm after searching". "Go verify a fact" without changing what to build → inquiry, not steer.

Soft guidance (not hard exclusivity):
- Prefer including critical whenever fault/error/dissatisfaction is clearly asserted, even if the message also steers or asks.
- approve vs steer: go-ahead on the agent's plan (incl. "fine if X", "can you work on these?") → approve; new/changed ask → steer. Do not tag go-ahead as steer.
- Picking an option the agent already offered → approve, not steer. If the agent presents multiple options (e.g. A or B) and the user selects one (e.g. *"Yes it should be started automatically as part of the MCP fleet"*), that greenlights an already-offered option → approve.
- critical vs steer: assert fault → critical; propose alternative without asserting fault → steer.
- Decide steer vs inquiry by goal (new action vs answer/confirmation), not punctuation. "Confirm after searching" → inquiry; changing what to build/do → steer.
- Use both inquiry and steer only when both goals are genuinely present.
- approve+critical together is rare/contradictory; only use if both are genuinely present (e.g. the agent proposes a listed plan and the user approves parts of it but pushes back on other parts).
- Do NOT force a single winner via a first-match ladder.

Respond with ONLY JSON: {"acts":["<label>",...]} with labels from {approve,critical,steer,inquiry}, deduplicated."""


def truncate_words(text: str, limit: int) -> str:
    return " ".join((text or "").split()[:limit])


def canonicalize_act(value: str) -> str:
    value = (value or "").strip().lower()
    return "steer" if value == "directive" else value


def normalize_acts(raw: object) -> list[str] | None:
    if isinstance(raw, str):
        raw = [raw]
    if not isinstance(raw, (list, tuple)) or not raw:
        return None

    found: set[str] = set()
    for value in raw:
        if not isinstance(value, str):
            return None
        act = canonicalize_act(value)
        if act not in ACT_SET:
            return None
        found.add(act)
    return [act for act in ACTS if act in found] or None


def jaccard(predicted: list[str] | None, gold: list[str] | None) -> float:
    if not predicted or not gold:
        return 0.0
    predicted_set = set(predicted)
    gold_set = set(gold)
    union = predicted_set | gold_set
    return len(predicted_set & gold_set) / len(union) if union else 0.0


def run_composer(prompt: str, retries: int = 4) -> str:
    if not os.environ.get("CURSOR_API_KEY", "").strip():
        print("ERROR: CURSOR_API_KEY unset", flush=True)
        return ""

    binary = AGENT_BIN if os.path.isfile(AGENT_BIN) else shutil.which(AGENT_BIN)
    if not binary:
        print(f"ERROR: Cursor agent binary not found: {AGENT_BIN}", flush=True)
        return ""

    command = [
        binary,
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
    env["PATH"] = os.path.dirname(os.path.realpath(binary)) + ":" + env.get(
        "PATH", ""
    )
    for attempt in range(retries):
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=240,
                env=env,
            )
            output = (result.stdout or "").strip()
            if result.returncode == 0 and output:
                return output
            error = (result.stderr or "")[:400]
            print(
                f"composer attempt {attempt + 1}: "
                f"rc={result.returncode} err={error!r}",
                flush=True,
            )
        except Exception as exc:
            print(f"composer attempt {attempt + 1}: {exc}", flush=True)
        if attempt < retries - 1:
            time.sleep(3 * (attempt + 1))
    return ""


def parse_acts(output: str) -> list[str] | None:
    if not output:
        return None
    cleaned = re.sub(r"^```(?:json)?\s*", "", output.strip())
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r'\{[^{}]*"acts"\s*:\s*\[[^\]]*\][^{}]*\}', cleaned, re.S)
        if not match:
            return None
        try:
            value = json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    if not isinstance(value, dict) or set(value) != {"acts"}:
        return None
    return normalize_acts(value.get("acts"))


def classify(text: str, previous_agent: str) -> list[str] | None:
    if not (text or "").strip():
        return None
    prompt = (
        "A developer is using an AI coding agent. The agent just said:\n"
        f"<agent>{truncate_words(previous_agent, 120)}</agent>\n\n"
        "The developer's next message was:\n"
        f"<message>{truncate_words(text, 150)}</message>\n\n"
        f"{TAXONOMY_PROMPT}\n\n"
        'Respond with ONLY JSON: {"acts":["<label>",...]}'
    )
    return parse_acts(run_composer(prompt))


def read_prediction() -> str:
    for path in (
        os.path.join(SIM_DIR, "answer.txt"),
        "/workspace/prediction.txt",
        "/logs/artifacts/prediction.txt",
    ):
        if os.path.exists(path):
            with open(path, encoding="utf-8", errors="replace") as handle:
                return handle.read().strip()
    return ""


def main() -> None:
    with open(
        os.path.join(TESTS_DIR, "gold.json"), encoding="utf-8"
    ) as handle:
        gold = json.load(handle)
    previous_agent = gold.get("prev_agent", "")

    gold_acts = normalize_acts(gold.get("gold_acts"))
    if not gold_acts:
        gold_acts = classify(gold.get("real", ""), previous_agent)

    predicted_text = read_prediction()
    pred_acts = (
        classify(predicted_text, previous_agent) if predicted_text else None
    )

    reward = jaccard(pred_acts, gold_acts)
    exact = bool(
        pred_acts and gold_acts and set(pred_acts) == set(gold_acts)
    )
    per_label = {
        act: {
            "pred": int(bool(pred_acts and act in pred_acts)),
            "gold": int(bool(gold_acts and act in gold_acts)),
        }
        for act in ACTS
    }
    verdict = {
        "point_id": gold.get("point_id"),
        "developer": gold.get("developer") or gold.get("dev"),
        "condition": gold.get("condition") or gold.get("variant"),
        "judge": JUDGE,
        "judge_backend": "cursor-agent",
        "scoring": "multilabel_jaccard_v1",
        "taxonomy": ACTS,
        "taxonomy_map": {"directive": "steer"},
        "predicted_msg": predicted_text,
        "pred_acts": pred_acts,
        "gold_acts": gold_acts,
        "pred_move": pred_acts[0] if pred_acts else None,
        "gold_move": gold_acts[0] if gold_acts else None,
        "real_msg": gold.get("real", ""),
        "match": exact,
        "exact_match": exact,
        "per_label": per_label,
        "jaccard": reward,
        "reward": reward,
    }
    with open(f"{VDIR}/verdict.json", "w", encoding="utf-8") as handle:
        json.dump(verdict, handle, indent=1, ensure_ascii=False)
        handle.write("\n")
    with open(f"{VDIR}/reward.txt", "w", encoding="utf-8") as handle:
        handle.write(str(reward))
    print(
        f"pred_acts={pred_acts} gold_acts={gold_acts} "
        f"jaccard={reward:.4f} exact={exact}",
        flush=True,
    )


if __name__ == "__main__":
    main()
