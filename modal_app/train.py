"""SFT training: Qwen + LoRA on marcus-sa user simulator data.

Defaults are tuned for the Qwen3.5-9B run with seq 32K, no chunking, and proper
assistant-only loss. The Qwen2.5-7B-Instruct v1 run can still be reproduced by
flipping `base_model`, `seq_len`, `epochs`, and `out_subdir`.

Approach:
- standard SFT with TRL SFTTrainer
- assistant_only_loss=True (TRL >= 0.14): loss masked on system+user-role tokens
- chat template patched to wrap assistant content in {% generation %} so TRL's
  mask computation works; original template restored before save for serving
- enable_thinking=False at training (and serve) time so the model is trained to
  emit raw JSON with no <think>...</think> preamble
- peft LoRA r=64 on attention + MLP projections
- merge LoRA into bf16 weights before saving for vLLM
"""
import json
import os
import time
from pathlib import Path

import modal

from common import app, train_image, volume, VOL_MOUNT, DATA_DIR, CKPT_DIR


# Qwen-family chat template with TRL {% generation %} markers around assistant
# content. Identical token sequence to the standard Qwen3 template when
# enable_thinking=False (no <think>...</think> insertion).
QWEN_TEMPLATE_WITH_GENERATION = (
    "{%- for message in messages %}"
    "<|im_start|>{{ message['role'] }}\n"
    "{%- if message['role'] == 'assistant' %}"
    "{% generation %}{{ message['content'] }}{% endgeneration %}"
    "{%- else %}"
    "{{ message['content'] }}"
    "{%- endif %}"
    "<|im_end|>\n"
    "{%- endfor %}"
    "{%- if add_generation_prompt %}<|im_start|>assistant\n{%- endif %}"
)


@app.function(
    image=train_image,
    volumes={VOL_MOUNT: volume},
    secrets=[modal.Secret.from_name("huggingface")],
    gpu="H100",  # 80GB; needed for 9B + seq 32K. A100-80GB tries to fit but margin is thin.
    timeout=60 * 60 * 6,
    cpu=8,
    memory=96 * 1024,
)
def train(
    user_id: str = "marcus-sa",
    data_subdir: str = "no-chunk",
    base_model: str = "Qwen/Qwen3.5-9B",
    run_name: str = "qwen35-9b-marcus-sa-v1",
    # 1 epoch keeps total wall-clock under $50 budget. Empirically ~850s/step
    # at seq 32K with FA2 + packing on H100. Packing reduces to ~23 steps total.
    epochs: float = 1.0,
    lr: float = 2e-4,
    seq_len: int = 32768,
    micro_batch: int = 1,
    grad_accum: int = 2,
    lora_r: int = 64,
    lora_alpha: int = 32,
    warmup_ratio: float = 0.03,
    grad_ckpt: bool = True,  # set False to try the no-checkpoint path (2x faster if VRAM fits)
):
    import torch
    from datasets import load_dataset
    from transformers import (
        AutoTokenizer,
        AutoModelForCausalLM,
    )
    from peft import LoraConfig, get_peft_model, TaskType, PeftModel
    from trl import SFTTrainer, SFTConfig

    print(f"[train] torch={torch.__version__} | cuda_avail={torch.cuda.is_available()}")
    print(f"[train] gpu={torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'cpu'}")

    out_dir = Path(CKPT_DIR) / run_name
    out_dir.mkdir(parents=True, exist_ok=True)
    log_dir = out_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    # --- data ---
    data_dir = Path(DATA_DIR) / user_id / data_subdir if data_subdir else Path(DATA_DIR) / user_id
    train_path = str(data_dir / "train.jsonl")
    val_path = str(data_dir / "val.jsonl")
    print(f"[train] loading data: {train_path}")
    train_ds = load_dataset("json", data_files=train_path, split="train")
    val_ds = load_dataset("json", data_files=val_path, split="train")
    print(f"[train] train={len(train_ds)} val={len(val_ds)}")

    # --- tokenizer / model ---
    print(f"[train] loading tokenizer + model: {base_model}")
    tok = AutoTokenizer.from_pretrained(base_model, token=os.environ["HF_TOKEN"], trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    # Patch chat template for assistant-only loss; keep original for serving restore.
    original_chat_template = tok.chat_template
    tok.chat_template = QWEN_TEMPLATE_WITH_GENERATION

    # Try FlashAttention 2 first; fall back to SDPA if Qwen3.5 doesn't have an FA2
    # path. SDPA at seq 32K on a 9B with the Qwen3.5 attention variant lands at
    # ~87s per fwd+bwd vs ~10-20s expected with FA2.
    attn_impl = "flash_attention_2"
    try:
        model = AutoModelForCausalLM.from_pretrained(
            base_model,
            torch_dtype=torch.bfloat16,
            attn_implementation=attn_impl,
            token=os.environ["HF_TOKEN"],
            trust_remote_code=True,
        )
    except (ValueError, ImportError) as e:
        print(f"[train] FA2 unavailable for this model ({e}); falling back to sdpa")
        attn_impl = "sdpa"
        model = AutoModelForCausalLM.from_pretrained(
            base_model,
            torch_dtype=torch.bfloat16,
            attn_implementation=attn_impl,
            token=os.environ["HF_TOKEN"],
            trust_remote_code=True,
        )
    actual_impl = getattr(model.config, "_attn_implementation", "unknown")
    print(f"[train] attn_implementation requested={attn_impl} actual={actual_impl}")
    model.config.use_cache = False
    if grad_ckpt:
        model.gradient_checkpointing_enable()
    model.enable_input_require_grads()

    # --- LoRA ---
    target_modules = [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ]
    lora_cfg = LoraConfig(
        r=lora_r,
        lora_alpha=lora_alpha,
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
        target_modules=target_modules,
    )
    model = get_peft_model(model, lora_cfg)
    model.print_trainable_parameters()

    # --- SFT config (TRL >= 0.14 supports assistant_only_loss) ---
    sft_cfg = SFTConfig(
        output_dir=str(out_dir / "adapter"),
        run_name=run_name,
        num_train_epochs=epochs,
        per_device_train_batch_size=micro_batch,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=grad_accum,
        learning_rate=lr,
        lr_scheduler_type="cosine",
        warmup_ratio=warmup_ratio,
        max_length=seq_len,
        bf16=True,
        logging_steps=1,
        eval_strategy="steps",
        eval_steps=20,
        save_strategy="epoch",
        save_total_limit=1,
        report_to=["tensorboard"],
        logging_dir=str(log_dir),
        gradient_checkpointing=grad_ckpt,
        gradient_checkpointing_kwargs={"use_reentrant": False} if grad_ckpt else None,
        dataset_num_proc=4,
        dataloader_num_workers=2,
        # Packing concatenates multiple short sessions into one max_length window
        # with proper attention masking, eliminating pad-token compute. With our
        # avg session ~14k tokens, packing roughly doubles throughput at seq 32K.
        packing=True,
        remove_unused_columns=True,
        assistant_only_loss=True,  # mask loss on system+user-role tokens
        use_liger_kernel=True,     # chunked CE + fused RMSNorm; required so the
                                   # [1, 32K, 152K] logit tensor doesn't OOM the H100
        max_grad_norm=1.0,
        weight_decay=0.0,
        optim="adamw_torch",
        seed=42,
    )

    trainer = SFTTrainer(
        model=model,
        args=sft_cfg,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        processing_class=tok,
    )

    # Sanity-check the assistant-only mask on example 0
    try:
        s = trainer.train_dataset[0]
        if "labels" in s:
            import numpy as np
            labels = np.array(s["labels"])
            n_pred = int((labels != -100).sum())
            n_tot = int(len(labels))
            print(f"[train] mask sample0: {n_pred}/{n_tot} pred tokens ({n_pred/max(n_tot,1):.1%})")
    except Exception as e:
        print(f"[train] mask check skipped: {e}")

    t0 = time.time()
    trainer.train()
    dt = time.time() - t0
    print(f"[train] training done in {dt/60:.1f} min")

    # Restore the standard chat template so vLLM serves a parseable Jinja
    # template (the {% generation %} extension isn't available at inference).
    tok.chat_template = original_chat_template

    adapter_dir = out_dir / "adapter"
    trainer.save_model(str(adapter_dir))
    tok.save_pretrained(str(adapter_dir))
    print(f"[train] adapter saved to {adapter_dir}")

    print("[train] merging LoRA into base model for serving...")
    del model, trainer
    torch.cuda.empty_cache()

    base = AutoModelForCausalLM.from_pretrained(
        base_model,
        torch_dtype=torch.bfloat16,
        attn_implementation="sdpa",
        token=os.environ["HF_TOKEN"],
        trust_remote_code=True,
    )
    merged = PeftModel.from_pretrained(base, str(adapter_dir)).merge_and_unload()
    merged_dir = out_dir / "merged"
    merged.save_pretrained(str(merged_dir), safe_serialization=True)
    tok.save_pretrained(str(merged_dir))
    print(f"[train] merged model saved to {merged_dir}")

    with open(out_dir / "meta.json", "w") as f:
        json.dump(
            {
                "run_name": run_name,
                "base_model": base_model,
                "user_id": user_id,
                "data_subdir": data_subdir,
                "epochs": epochs,
                "lr": lr,
                "seq_len": seq_len,
                "micro_batch": micro_batch,
                "grad_accum": grad_accum,
                "lora_r": lora_r,
                "lora_alpha": lora_alpha,
                "assistant_only_loss": True,
                "enable_thinking_at_serve": False,
                "train_examples": len(train_ds),
                "val_examples": len(val_ds),
                "training_seconds": dt,
            },
            f,
            indent=2,
        )

    volume.commit()
    print("[train] volume committed. done.")
    return {"run_name": run_name, "merged_dir": str(merged_dir)}


@app.local_entrypoint()
def main(
    user_id: str = "marcus-sa",
    data_subdir: str = "no-chunk",
    base_model: str = "Qwen/Qwen3.5-9B",
    run_name: str = "qwen35-9b-marcus-sa-v1",
    epochs: float = 1.0,
    seq_len: int = 32768,
    grad_ckpt: bool = False,
):
    print(
        train.remote(
            user_id=user_id,
            data_subdir=data_subdir,
            base_model=base_model,
            run_name=run_name,
            epochs=epochs,
            seq_len=seq_len,
            grad_ckpt=grad_ckpt,
        )
    )
