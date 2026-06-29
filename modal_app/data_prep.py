"""Prepare SFT data from SWE-chat for user `marcus-sa`.

Each training example is a multi-turn chat session:
  system  -> with-user system_template (verbatim)
  user    -> initial_template with the session's first user_prompt as {{problem_statement}}
  assist  -> JSON {"decision":"interject","message":"<that first user prompt>"}
  user    -> step_template for assistant turn 1
  assist  -> JSON decision (continue if user was silent, interject otherwise)
  ...

Loss masked on assistant turns only (standard for SFT). Saved as jsonl of
{"messages": [...]} to the Modal volume.
"""
import json
import os
import re
from pathlib import Path

import modal

from common import app, data_image, volume, VOL_MOUNT, DATA_DIR


# === with-user templates (verbatim from src/withuser/configs/swebench__mini_swe_agent.yaml) ===
SYSTEM_TEMPLATE = """You are simulating a human user who has filed a bug report / feature request and is now
working with an AI coding assistant to fix it. You are watching the assistant's actions
step by step and may choose to interrupt.

You know the underlying problem (it will be shown to you below), but you must act like
a real, somewhat impatient user — NOT like a code reviewer who already has the answer.
Specifically:
  - Do NOT dictate file paths, function names, or the exact fix.
  - Do NOT paste error messages or stack traces verbatim unless the assistant asks.
  - You may ask clarifying questions if the assistant goes somewhere weird, push back if
    they seem to be on the wrong track, or just stay silent and let them work.
  - Prefer staying silent. Most steps you should choose `continue`.

You ALWAYS reply with a single JSON object and nothing else:

  {"decision": "continue" | "interject", "message": "<text or empty>"}

Meaning:
  - "continue": stay silent. `message` is ignored.
  - "interject": send `message` to the assistant as a user-role message.

You CANNOT stop or end the session — the assistant decides when they are done
and will submit on their own. Your only choice is to stay silent or speak up.
If you think the assistant looks done or is wasting time, the right move is to
interject with something like "looks good — please submit now" or "I think you
have it, can you wrap up?", NOT to try to end the session.

Keep `message` short (1-3 sentences), conversational, first-person."""

INITIAL_TEMPLATE = """Below is the problem you (the user) want fixed. Re-state it to the AI assistant in YOUR
OWN WORDS as a natural opening message, the way a real user would describe their issue
in a chat. Do NOT copy it verbatim. Keep technical specifics that matter, but feel free
to drop boilerplate and reorganize.

Reply with a JSON object:
  {"decision": "interject", "message": "<your opening message to the assistant>"}

Problem:
---
__PROBLEM_STATEMENT__
---"""

STEP_TEMPLATE = """The AI assistant just took step __STEP__. Here is what they said and did, plus the
tool/observation that came back.

ASSISTANT (latest action):
---
__ASSISTANT_TEXT__
---

OBSERVATION:
---
__OBSERVATION__
---

Reminder of the original problem you want fixed:
---
__TASK__
---

Decide whether to stay silent or interject. Reply with JSON only."""


def render_initial(problem_statement: str) -> str:
    return INITIAL_TEMPLATE.replace("__PROBLEM_STATEMENT__", problem_statement)


def render_step(step: int, assistant_text: str, observation: str, task: str) -> str:
    return (
        STEP_TEMPLATE.replace("__STEP__", str(step))
        .replace("__ASSISTANT_TEXT__", assistant_text)
        .replace("__OBSERVATION__", observation)
        .replace("__TASK__", task)
    )


# --- text cleaning ---
CONDUCTOR_PAT = re.compile(
    r"<system_instruction>.*?</system_instruction>\s*", re.DOTALL | re.IGNORECASE
)
SYSTEM_REMINDER_PAT = re.compile(
    r"<system-reminder>.*?</system-reminder>\s*", re.DOTALL | re.IGNORECASE
)
COMMAND_BLOCK_PAT = re.compile(
    r"<(?:command-name|command-message|command-args|local-command-stdout|"
    r"local-command-stderr)>.*?</(?:command-name|command-message|command-args|"
    r"local-command-stdout|local-command-stderr)>\s*",
    re.DOTALL | re.IGNORECASE,
)


def clean_user_prompt(text: str) -> str:
    if not text:
        return ""
    text = CONDUCTOR_PAT.sub("", text)
    text = SYSTEM_REMINDER_PAT.sub("", text)
    text = COMMAND_BLOCK_PAT.sub("", text)
    text = text.strip()
    return text


def truncate(s: str, n: int = 4000) -> str:
    if s is None:
        return ""
    s = str(s)
    if len(s) <= n:
        return s
    return s[: n - 50] + "\n...[truncated]"


@app.function(
    image=data_image,
    volumes={VOL_MOUNT: volume},
    secrets=[modal.Secret.from_name("huggingface")],
    timeout=60 * 60,
    cpu=4,
    memory=16384,
)
def prepare(
    user_id: str = "marcus-sa",
    min_user_prompts: int = 2,
    max_steps_per_example: int = 10,
    text_trunc_chars: int = 800,
    task_trunc_chars: int = 600,
    out_subdir: str = "",
):
    import pandas as pd
    from datasets import load_dataset

    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

    print(f"[prep] loading conversations parquet for user_id={user_id}")
    ds = load_dataset(
        "SALT-NLP/SWE-chat",
        data_files="conversations.parquet",
        split="train",
        token=os.environ["HF_TOKEN"],
    )
    df = ds.to_pandas()
    print(f"[prep] total rows: {len(df):,}")

    # Filter to user, sort
    df = df[df["user_id"] == user_id].copy()
    print(f"[prep] rows for {user_id}: {len(df):,}")
    # Keep is_conversational=True for user/assistant text, but ALWAYS keep
    # tool_use / tool_result rows (which are mostly is_conversational=False).
    mask = df["is_conversational"].fillna(False) | df["role"].isin(["tool_use", "tool_result"])
    df = df[mask].copy()
    print(f"[prep] after role/conv filter: {len(df):,}")

    # Sort by session, turn_number
    df = df.sort_values(["session_id", "turn_number"]).reset_index(drop=True)

    def render_tool_call(row) -> str:
        name = row.get("tool_name") or ""
        cmd = row.get("command") or ""
        fp = row.get("file_path") or ""
        pat = row.get("pattern") or ""
        content = row.get("content") or ""
        parts = []
        if name:
            parts.append(f"[tool: {name}]")
        if fp:
            parts.append(f"file: {fp}")
        if pat:
            parts.append(f"pattern: {pat}")
        if cmd:
            parts.append(f"command: {cmd}")
        if content and content not in {"No response requested.", ""}:
            parts.append(content)
        return " ".join(parts).strip()

    def is_slash_command_only(text: str) -> bool:
        t = (text or "").strip()
        if not t:
            return True
        # short slash-command stubs like "/nw-deliver foo", "Tool loaded."
        if len(t) < 15:
            return True
        if t.startswith("/") and "\n" not in t and len(t) < 80:
            return True
        if t in {"Tool loaded.", "tool loaded", "continue", "go on", "ok"}:
            return True
        return False

    sessions = []
    skipped = {"too_short": 0, "no_user_prompt": 0, "no_assistant": 0, "stub_first_prompt": 0}

    for sid, g in df.groupby("session_id", sort=False):
        events = []
        for _, row in g.iterrows():
            role = row["role"]
            ttype = row["turn_type"]
            content = row.get("content") or ""
            if role == "user" and ttype == "user_prompt":
                cleaned = clean_user_prompt(content)
                if not cleaned or len(cleaned) < 3:
                    continue
                events.append(("user_prompt", cleaned))
            elif role == "assistant" and ttype == "assistant_response":
                txt = str(content).strip()
                if txt and txt != "No response requested.":
                    events.append(("assistant_action", txt))
            elif role == "assistant" and ttype == "assistant_thinking":
                # treat thinking as part of the assistant's "step"
                txt = str(content).strip()
                if txt:
                    events.append(("assistant_action", f"[thinking] {txt}"))
            elif role == "tool_use":
                txt = render_tool_call(row)
                if txt:
                    events.append(("assistant_action", txt))
            elif role == "tool_result":
                txt = str(content).strip()
                if txt:
                    events.append(("tool_result", txt))
            # ignore: system_injected, metadata/progress

        user_prompts = [e for e in events if e[0] == "user_prompt"]
        asst_actions = [e for e in events if e[0] == "assistant_action"]
        if len(user_prompts) < min_user_prompts:
            skipped["no_user_prompt"] += 1
            continue
        if len(asst_actions) < 1:
            skipped["no_assistant"] += 1
            continue
        first_up = user_prompts[0][1]
        if is_slash_command_only(first_up):
            skipped["stub_first_prompt"] += 1
            continue
        sessions.append((sid, events))

    print(f"[prep] usable sessions: {len(sessions)} | skipped: {skipped}")

    # Build SFT examples: one or more per session, multi-turn chat with assistant-only loss.
    # Long sessions are split into non-overlapping chunks of `max_steps_per_example` steps;
    # every chunk starts fresh from system + initial + opening message so the model
    # always sees the same context shape it will see at inference time.
    examples = []
    for sid, events in sessions:
        # First user prompt = problem statement and target opening message.
        first_up = next(e[1] for e in events if e[0] == "user_prompt")
        problem_statement = first_up
        task = truncate(first_up, task_trunc_chars)

        # Walk forward from the first user_prompt, collecting (assistant_text,
        # observation, target_decision_json) step-tuples for the whole session.
        first_up_idx = next(i for i, e in enumerate(events) if e[0] == "user_prompt")
        rest = events[first_up_idx + 1 :]
        steps = []  # list of (assistant_text, observation, target_json)
        i = 0
        while i < len(rest):
            kind, content = rest[i]
            if kind == "tool_result":
                i += 1
                continue
            if kind == "assistant_action":
                assistant_text = content
                observation_parts = []
                j = i + 1
                while j < len(rest) and rest[j][0] == "tool_result":
                    observation_parts.append(rest[j][1])
                    j += 1
                observation = "\n".join(observation_parts) if observation_parts else ""
                k = j
                pending_user_prompts = []
                while k < len(rest) and rest[k][0] != "assistant_action":
                    if rest[k][0] == "user_prompt":
                        pending_user_prompts.append(rest[k][1])
                    k += 1
                if pending_user_prompts:
                    target = json.dumps(
                        {"decision": "interject", "message": pending_user_prompts[0]},
                        ensure_ascii=False,
                    )
                else:
                    target = json.dumps(
                        {"decision": "continue", "message": ""}, ensure_ascii=False
                    )
                steps.append((assistant_text, observation, target))
                i = k
                continue
            i += 1

        if not steps:
            continue

        # Chunk the steps into non-overlapping windows of max_steps_per_example.
        for chunk_start in range(0, len(steps), max_steps_per_example):
            chunk = steps[chunk_start : chunk_start + max_steps_per_example]
            messages = [
                {"role": "system", "content": SYSTEM_TEMPLATE},
                {"role": "user", "content": render_initial(truncate(problem_statement, task_trunc_chars))},
                {
                    "role": "assistant",
                    "content": json.dumps(
                        {"decision": "interject", "message": truncate(first_up, 1200)},
                        ensure_ascii=False,
                    ),
                },
            ]
            for offset, (asst, obs, target) in enumerate(chunk):
                global_step = chunk_start + offset + 1
                messages.append(
                    {
                        "role": "user",
                        "content": render_step(
                            step=global_step,
                            assistant_text=truncate(asst, text_trunc_chars),
                            observation=truncate(obs, text_trunc_chars),
                            task=task,
                        ),
                    }
                )
                messages.append({"role": "assistant", "content": target})
            examples.append(
                {
                    "session_id": sid,
                    "chunk": chunk_start // max_steps_per_example,
                    "messages": messages,
                }
            )

    # Stats
    interject_cnt = 0
    continue_cnt = 0
    for ex in examples:
        for m in ex["messages"]:
            if m["role"] == "assistant":
                try:
                    d = json.loads(m["content"])
                    if d.get("decision") == "interject":
                        interject_cnt += 1
                    elif d.get("decision") == "continue":
                        continue_cnt += 1
                except Exception:
                    pass
    total = interject_cnt + continue_cnt
    print(
        f"[prep] examples={len(examples)} | assistant turns: {total} "
        f"(interject={interject_cnt} {interject_cnt/total:.1%} | "
        f"continue={continue_cnt} {continue_cnt/total:.1%})"
    )

    # Train/val split: 95/5
    import random
    random.seed(0)
    random.shuffle(examples)
    val_n = max(5, len(examples) // 20)
    val = examples[:val_n]
    train = examples[val_n:]
    print(f"[prep] train={len(train)} | val={len(val)}")

    out_dir = Path(DATA_DIR) / user_id / out_subdir if out_subdir else Path(DATA_DIR) / user_id
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "train.jsonl", "w") as f:
        for ex in train:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    with open(out_dir / "val.jsonl", "w") as f:
        for ex in val:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    with open(out_dir / "stats.json", "w") as f:
        json.dump(
            {
                "user_id": user_id,
                "n_sessions_processed": len(sessions),
                "n_examples_train": len(train),
                "n_examples_val": len(val),
                "interject_pct": interject_cnt / max(total, 1),
                "continue_pct": continue_cnt / max(total, 1),
                "skipped": skipped,
            },
            f,
            indent=2,
        )
    print(f"[prep] wrote to {out_dir}")
    volume.commit()
    return {"n_train": len(train), "n_val": len(val)}


@app.local_entrypoint()
def main(
    user_id: str = "marcus-sa",
    max_steps_per_example: int = 10,
    text_trunc_chars: int = 800,
    task_trunc_chars: int = 600,
    out_subdir: str = "",
):
    print(prepare.remote(
        user_id=user_id,
        max_steps_per_example=max_steps_per_example,
        text_trunc_chars=text_trunc_chars,
        task_trunc_chars=task_trunc_chars,
        out_subdir=out_subdir,
    ))
