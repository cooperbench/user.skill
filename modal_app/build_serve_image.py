"""Trigger the serve image build by running a noop on it.

Run this in parallel with training so the vLLM image is cached and
`modal deploy serve.py` is fast when training finishes.
"""
import modal

from common import app, serve_image


@app.function(image=serve_image, timeout=60 * 30, cpu=2, memory=4096)
def warm():
    import vllm  # noqa
    print(f"[warm] vllm available")
    return "ok"


@app.local_entrypoint()
def main():
    print(warm.remote())
