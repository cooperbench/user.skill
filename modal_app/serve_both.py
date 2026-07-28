"""Deploy BOTH endpoints (base + trained) in one Modal app so they coexist.

URLs after `modal deploy serve_both.py`:
  - https://<workspace>--user-sim-marcus-sa-serve-base.modal.run/v1   (Qwen2.5-7B-Instruct, untrained)
  - https://<workspace>--user-sim-marcus-sa-serve-trained.modal.run/v1 (LoRA-merged user simulator)

Both expose OpenAI-compatible /v1/chat/completions, both serve the model under
the name `user-sim`, both use the same API key `user-sim-dev-key`.
"""
import os
import subprocess

import modal

from common import app, serve_image, volume, VOL_MOUNT, CKPT_DIR


SERVED_MODEL_NAME = "user-sim"  # avoid claude/anthropic/sonnet/opus/haiku substrings
API_KEY = "user-sim-dev-key"


def _vllm_cmd(model_path: str) -> list[str]:
    return [
        "python", "-m", "vllm.entrypoints.openai.api_server",
        "--model", model_path,
        "--served-model-name", SERVED_MODEL_NAME,
        "--port", "8000",
        "--host", "0.0.0.0",
        "--api-key", API_KEY,
        "--max-model-len", "32768",
        "--gpu-memory-utilization", "0.92",
        "--dtype", "bfloat16",
        "--enable-prefix-caching",
        "--download-dir", f"{VOL_MOUNT}/hf_cache/hub",
    ]


# ------------ BASE MODEL ENDPOINT ------------
@app.function(
    image=serve_image,
    gpu="L40S",
    volumes={VOL_MOUNT: volume},
    secrets=[modal.Secret.from_name("huggingface")],
    timeout=60 * 60 * 4,
    scaledown_window=60 * 5,
    max_containers=1,
)
@modal.concurrent(max_inputs=32)
@modal.web_server(port=8000, startup_timeout=600)
def serve_base():
    cmd = _vllm_cmd("Qwen/Qwen2.5-7B-Instruct")
    print("[serve_base] cmd:", " ".join(cmd))
    subprocess.Popen(cmd)


# ------------ TRAINED MODEL ENDPOINT ------------
@app.function(
    image=serve_image,
    gpu="L40S",
    volumes={VOL_MOUNT: volume},
    secrets=[modal.Secret.from_name("huggingface")],
    timeout=60 * 60 * 4,
    scaledown_window=60 * 5,
    max_containers=1,
)
@modal.concurrent(max_inputs=32)
@modal.web_server(port=8000, startup_timeout=600)
def serve_trained():
    run_name = os.environ.get("USER_SIM_RUN_NAME", "qwen25-7b-marcus-sa-v1")
    model_dir = f"{CKPT_DIR}/{run_name}/merged"
    print(f"[serve_trained] model_dir={model_dir}")
    cmd = _vllm_cmd(model_dir)
    print("[serve_trained] cmd:", " ".join(cmd))
    subprocess.Popen(cmd)
