"""Smoke-test serve: runs vLLM with the BASE Qwen2.5-7B-Instruct so we can
validate the serving stack and with-user integration end-to-end before the
trained model is ready. Once training finishes, use `serve.py` instead
(which serves the merged LoRA checkpoint from the volume).
"""
import os
import subprocess

import modal

from common import app, serve_image, volume, VOL_MOUNT


SERVED_MODEL_NAME = "user-sim"
API_KEY = "user-sim-dev-key"


@app.function(
    image=serve_image,
    gpu="L40S",
    volumes={VOL_MOUNT: volume},
    secrets=[modal.Secret.from_name("huggingface")],
    timeout=60 * 60 * 2,
    scaledown_window=60 * 5,
    max_containers=1,
)
@modal.concurrent(max_inputs=32)
@modal.web_server(port=8000, startup_timeout=600)
def serve_base():
    cmd = [
        "python", "-m", "vllm.entrypoints.openai.api_server",
        "--model", "Qwen/Qwen2.5-7B-Instruct",
        "--served-model-name", SERVED_MODEL_NAME,
        "--port", "8000",
        "--host", "0.0.0.0",
        "--api-key", API_KEY,
        "--max-model-len", "16384",
        "--gpu-memory-utilization", "0.92",
        "--dtype", "bfloat16",
        "--enable-prefix-caching",
        "--download-dir", f"{VOL_MOUNT}/hf_cache/hub",
    ]
    print("[serve_base] cmd:", " ".join(cmd))
    subprocess.Popen(cmd)
