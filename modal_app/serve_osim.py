"""Serve OdysSim OSim-4B and OSim-8B (cmu-lti) as OpenAI-compatible vLLM endpoints
on Modal, for the UserSimBench v0 coding move-fidelity eval.

Both are Qwen3 (MIT) post-trained to play the *human/user* side of a conversation.
Deploy:  modal deploy modal_app/serve_osim.py
URLs:    https://kevinli020508--osim-eval-serve-8b.modal.run/v1
         https://kevinli020508--osim-eval-serve-4b.modal.run/v1
API key: osim-eval-key
"""
import os
import subprocess

import modal

from common import serve_image, volume, VOL_MOUNT, HF_CACHE

app = modal.App("osim-eval")

API_KEY = "osim-eval-key"


def _launch(model_id: str, served_name: str):
    """Start a vLLM OpenAI server for one HF model id (chat_template.jinja in the
    repo is picked up by the tokenizer). Qwen3 thinking is left to the request
    (we pass enable_thinking=false from the client) and stripped client-side."""
    os.makedirs(HF_CACHE, exist_ok=True)
    cmd = [
        "python", "-m", "vllm.entrypoints.openai.api_server",
        "--model", model_id,
        "--served-model-name", served_name,
        "--download-dir", HF_CACHE,
        "--port", "8000", "--host", "0.0.0.0",
        "--api-key", API_KEY,
        "--max-model-len", "16384",
        "--gpu-memory-utilization", "0.90",
        "--dtype", "bfloat16",
        "--enable-prefix-caching",
    ]
    print("[serve] launching:", " ".join(cmd))
    subprocess.Popen(cmd)


@app.function(
    image=serve_image, gpu="L40S", volumes={VOL_MOUNT: volume},
    secrets=[modal.Secret.from_name("huggingface")],
    timeout=60 * 60 * 2, scaledown_window=60 * 5, max_containers=1,
)
@modal.concurrent(max_inputs=32)
@modal.web_server(port=8000, startup_timeout=60 * 12)
def serve_8b():
    _launch("cmu-lti/osim-8b", "osim-8b")


@app.function(
    image=serve_image, gpu="L40S", volumes={VOL_MOUNT: volume},
    secrets=[modal.Secret.from_name("huggingface")],
    timeout=60 * 60 * 2, scaledown_window=60 * 5, max_containers=1,
)
@modal.concurrent(max_inputs=32)
@modal.web_server(port=8000, startup_timeout=60 * 12)
def serve_4b():
    _launch("cmu-lti/osim-4b", "osim-4b")


@app.local_entrypoint()
def main():
    print("Deploy with: modal deploy modal_app/serve_osim.py")
