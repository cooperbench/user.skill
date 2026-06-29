"""Smoke-test the deployed vLLM endpoint with two real with-user calls."""
import json
import os
import sys

import modal


def main(base_url: str, api_key: str, model_id: str = "user-sim"):
    try:
        from openai import OpenAI
    except ImportError:
        print("pip install openai", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(base_url=base_url, api_key=api_key)

    SYSTEM = """You are simulating a human user who has filed a bug report / feature request and is now
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

    INITIAL = """Below is the problem you (the user) want fixed. Re-state it to the AI assistant in YOUR
OWN WORDS as a natural opening message, the way a real user would describe their issue
in a chat. Do NOT copy it verbatim. Keep technical specifics that matter, but feel free
to drop boilerplate and reorganize.

Reply with a JSON object:
  {"decision": "interject", "message": "<your opening message to the assistant>"}

Problem:
---
The eval suite is failing on observer-llm-reasoning. beforeAll setup throws a
SurrealDB query error: "The query was not executed due to a failed transaction".
The failure originates in setupEvalRuntime in evals/eval-test-kit.ts.
---"""

    STEP = """The AI assistant just took step 1. Here is what they said and did, plus the
tool/observation that came back.

ASSISTANT (latest action):
---
[tool: Read] file: evals/eval-test-kit.ts {"limit": 100}
---

OBSERVATION:
---
1: import { surreal } from "../db/surreal";
2: export async function setupEvalRuntime() {
3:   const schemaStatements = splitSurqlStatements(schemaSql);
4:   for (const stmt of schemaStatements) {
5:     await surreal.query(stmt).catch(...);
6:   }
7:   // ...
---

Reminder of the original problem you want fixed:
---
The eval suite is failing on observer-llm-reasoning ...
---

Decide whether to stay silent or interject. Reply with JSON only."""

    # Opening turn
    print("=== OPENING ===")
    resp = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": INITIAL},
        ],
        temperature=0.7,
        max_tokens=400,
    )
    out1 = resp.choices[0].message.content
    print(out1)
    try:
        d1 = json.loads(out1)
        print(f"  parsed: decision={d1.get('decision')}, message_len={len(d1.get('message',''))}")
    except Exception as e:
        print(f"  PARSE ERROR: {e}")

    # Step turn (after opening)
    print("\n=== STEP 1 ===")
    resp = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": INITIAL},
            {"role": "assistant", "content": out1},
            {"role": "user", "content": STEP},
        ],
        temperature=0.7,
        max_tokens=400,
    )
    out2 = resp.choices[0].message.content
    print(out2)
    try:
        d2 = json.loads(out2)
        print(f"  parsed: decision={d2.get('decision')}, message_len={len(d2.get('message',''))}")
    except Exception as e:
        print(f"  PARSE ERROR: {e}")


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--base-url", required=True, help="https://...modal.run/v1")
    p.add_argument("--api-key", default="user-sim-dev-key")
    p.add_argument("--model-id", default="user-sim")
    args = p.parse_args()
    main(args.base_url, args.api_key, args.model_id)
