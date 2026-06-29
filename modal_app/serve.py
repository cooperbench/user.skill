"""vLLM OpenAI-compatible inference server on Modal.

Serves the merged user-sim model behind a public URL. Drop-in for `with-user`:
  export OPENAI_API_BASE="https://<your-url>/v1"
  export OPENAI_API_KEY="<token>"
  --user-model openai/user-sim
"""
import os
import subprocess
import time

import modal

from common import app, serve_image, volume, VOL_MOUNT, CKPT_DIR


SERVED_MODEL_NAME = "user-sim"  # MUST NOT contain anthropic/claude/sonnet/opus/haiku
API_KEY_PLACEHOLDER = "user-sim-dev-key"  # for prod, mount as Secret


@app.function(
    image=serve_image,
    # L40S has 48GB which fits Qwen3-8B bf16 + KV cache easily, at ~$1.95/h
    # (vs A100-80GB at $2.50/h). For higher throughput swap to "A100-80GB".
    gpu="L40S",
    volumes={VOL_MOUNT: volume},
    secrets=[modal.Secret.from_name("huggingface")],
    timeout=60 * 60 * 4,
    scaledown_window=60 * 5,
    max_containers=1,
)
@modal.concurrent(max_inputs=64)
@modal.web_server(port=8000, startup_timeout=600)
def serve():
    run_name = os.environ.get("USER_SIM_RUN_NAME", "qwen25-7b-marcus-sa-v1")
    model_dir = f"{CKPT_DIR}/{run_name}/merged"
    print(f"[serve] starting vLLM with model_dir={model_dir} served_name={SERVED_MODEL_NAME}")

    cmd = [
        "python", "-m", "vllm.entrypoints.openai.api_server",
        "--model", model_dir,
        "--served-model-name", SERVED_MODEL_NAME,
        "--port", "8000",
        "--host", "0.0.0.0",
        "--api-key", os.environ.get("USER_SIM_API_KEY", API_KEY_PLACEHOLDER),
        "--max-model-len", "16384",
        "--gpu-memory-utilization", "0.92",
        "--dtype", "bfloat16",
        "--enable-prefix-caching",
    ]
    print("[serve] cmd:", " ".join(cmd))
    subprocess.Popen(cmd)


@app.local_entrypoint()
def main():
    """Deploy via `modal deploy serve.py` instead of running this.

    `modal run serve.py` would invoke `main` synchronously rather than
    starting the web server."""
    print(
        "Run `modal deploy serve.py` to publish the web endpoint. "
        "URL pattern: https://<workspace>--user-sim-marcus-sa-serve.modal.run"
    )
