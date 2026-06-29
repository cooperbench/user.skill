"""Offline evaluation on the val set: load merged model, generate one
assistant turn per held-out conversation prefix, report JSON validity and
decision accuracy.
"""
import json
import os
import re
from pathlib import Path

import modal

from common import app, train_image, volume, VOL_MOUNT, DATA_DIR, CKPT_DIR


@app.function(
    image=train_image,
    volumes={VOL_MOUNT: volume},
    secrets=[modal.Secret.from_name("huggingface")],
    gpu="A100-40GB",
    timeout=60 * 30,
    cpu=4,
    memory=32 * 1024,
)
def evaluate(
    user_id: str = "marcus-sa",
    run_name: str = "qwen25-7b-marcus-sa-v1",
    max_examples: int = 12,
    max_new_tokens: int = 300,
):
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM

    model_dir = f"{CKPT_DIR}/{run_name}/merged"
    val_path = f"{DATA_DIR}/{user_id}/val.jsonl"

    print(f"[eval] loading model from {model_dir}")
    tok = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForCausalLM.from_pretrained(
        model_dir, torch_dtype=torch.bfloat16, device_map="cuda:0"
    )
    model.eval()

    examples = []
    with open(val_path) as f:
        for line in f:
            examples.append(json.loads(line))
    examples = examples[:max_examples]

    # For each example, sample a decision point: pick a random assistant turn
    # (index >= 2 since [0]=system, [1]=user-initial), use messages up to but
    # NOT including that assistant turn as context, generate.
    import random
    rng = random.Random(0)

    stats = {"parse_ok": 0, "schema_ok": 0, "decision_match": 0, "total": 0}
    samples_to_show = 4
    shown = 0

    for ex in examples:
        msgs = ex["messages"]
        # find all assistant turn indices
        asst_idxs = [i for i, m in enumerate(msgs) if m["role"] == "assistant"]
        if not asst_idxs:
            continue
        # pick a random assistant turn, but not too early (to test multi-turn context)
        idx = rng.choice(asst_idxs)
        context = msgs[:idx]
        target = json.loads(msgs[idx]["content"])

        prompt = tok.apply_chat_template(context, tokenize=False, add_generation_prompt=True)
        ids = tok(prompt, return_tensors="pt", truncation=True, max_length=12000).to(model.device)
        with torch.no_grad():
            out = model.generate(
                **ids,
                max_new_tokens=max_new_tokens,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tok.eos_token_id,
            )
        gen = tok.decode(out[0][ids["input_ids"].shape[1]:], skip_special_tokens=True)
        stats["total"] += 1

        m = re.search(r"\{.*\}", gen, re.DOTALL)
        parsed = None
        if m:
            try:
                parsed = json.loads(m.group(0))
                stats["parse_ok"] += 1
                if (
                    isinstance(parsed, dict)
                    and "decision" in parsed
                    and "message" in parsed
                    and parsed["decision"] in ("continue", "interject")
                ):
                    stats["schema_ok"] += 1
                    if parsed["decision"] == target["decision"]:
                        stats["decision_match"] += 1
            except Exception:
                pass

        if shown < samples_to_show:
            print(f"\n--- SAMPLE {shown+1} ---")
            print(f"  context_turns: {len(context)}")
            print(f"  TARGET: {msgs[idx]['content'][:200]}")
            print(f"  PRED:   {gen[:300]}")
            print(f"  parse_ok={parsed is not None} | target_decision={target.get('decision')}"
                  f" | pred_decision={(parsed or {}).get('decision','?')}")
            shown += 1

    print("\n=== summary ===")
    n = max(stats["total"], 1)
    print(f"total={stats['total']}")
    print(f"parse_ok        {stats['parse_ok']}/{n}  ({stats['parse_ok']/n:.1%})")
    print(f"schema_ok       {stats['schema_ok']}/{n}  ({stats['schema_ok']/n:.1%})")
    print(f"decision_match  {stats['decision_match']}/{n}  ({stats['decision_match']/n:.1%})")
    return stats


@app.local_entrypoint()
def main(
    user_id: str = "marcus-sa",
    run_name: str = "qwen25-7b-marcus-sa-v1",
):
    print(evaluate.remote(user_id=user_id, run_name=run_name))
