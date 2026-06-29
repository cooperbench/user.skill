"""Verify training-time vs inference-time chat template produces same tokens."""
import modal

from common import app, train_image, volume, VOL_MOUNT


@app.function(
    image=train_image,
    volumes={VOL_MOUNT: volume},
    secrets=[modal.Secret.from_name("huggingface")],
    timeout=600,
    cpu=2,
    memory=8192,
)
def check(base_model: str = "Qwen/Qwen2.5-7B-Instruct"):
    import os
    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained(base_model, token=os.environ["HF_TOKEN"])
    original = tok.chat_template
    custom = (
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

    messages = [
        {"role": "system", "content": "sys msg"},
        {"role": "user", "content": "user msg"},
        {"role": "assistant", "content": '{"decision":"continue","message":""}'},
        {"role": "user", "content": "step 1"},
        {"role": "assistant", "content": '{"decision":"interject","message":"hi"}'},
    ]

    # Render with original template (tokenize=False to see text)
    orig_text = tok.apply_chat_template(messages, tokenize=False)
    print("=== ORIGINAL Qwen2.5 template ===")
    print(orig_text)
    print()

    # Render with custom template
    tok.chat_template = custom
    custom_text = tok.apply_chat_template(messages, tokenize=False)
    print("=== CUSTOM (training) template ===")
    print(custom_text)
    print()

    # Tokenize both — they should yield the same token IDs (the {% generation %}
    # markers only matter when return_assistant_tokens_mask=True).
    tok.chat_template = original
    ids_orig = tok.apply_chat_template(messages, tokenize=True)
    tok.chat_template = custom
    ids_custom = tok.apply_chat_template(messages, tokenize=True)
    print(f"orig token count: {len(ids_orig)}")
    print(f"custom token count: {len(ids_custom)}")
    print(f"identical: {ids_orig == ids_custom}")

    # Try the assistant mask path
    try:
        encoded = tok.apply_chat_template(
            messages,
            tokenize=True,
            return_dict=True,
            return_assistant_tokens_mask=True,
        )
        masks = encoded["assistant_masks"]
        n_pred = sum(masks)
        n_tot = len(masks)
        print(f"assistant_masks: {n_pred}/{n_tot} tokens marked as assistant ({n_pred/max(n_tot,1):.1%})")
    except Exception as e:
        print(f"assistant_masks failed: {e}")


@app.local_entrypoint()
def main():
    check.remote()
