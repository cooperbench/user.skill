"""Export a small sample of training traces as a single JSON file so the web
viewer can ship them statically."""
import json
import modal

from common import app, data_image, volume, VOL_MOUNT, DATA_DIR


@app.function(image=data_image, volumes={VOL_MOUNT: volume}, timeout=120)
def export(user_id: str = "marcus-sa", subdir: str = "no-chunk", n: int = 20) -> str:
    from pathlib import Path
    p = Path(DATA_DIR) / user_id / subdir / "train.jsonl"
    out = []
    with open(p) as f:
        for i, line in enumerate(f):
            if i >= n:
                break
            ex = json.loads(line)
            out.append(ex)
    return json.dumps(out, ensure_ascii=False)


@app.local_entrypoint()
def main(user_id: str = "marcus-sa", subdir: str = "no-chunk", n: int = 20, out: str = "/data/with-user/web/public/traces.json"):
    from pathlib import Path
    data = export.remote(user_id=user_id, subdir=subdir, n=n)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(data)
    parsed = json.loads(data)
    print(f"wrote {len(parsed)} traces to {out}")
    print(f"  total messages: {sum(len(t['messages']) for t in parsed)}")
