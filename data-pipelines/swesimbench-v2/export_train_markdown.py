#!/usr/bin/env python3
"""Export train-split sessions as markdown (same turn format as history.md).

Layout (NOT Harbor tasks):
  <out>/
    README.md
    _manifest.json
    <dev_slug>/
      <session_id>.md

Each session file has YAML frontmatter + full scrubbed turns as:

  > DEVELOPER

  ...

  > AGENT

  ...

No per-turn word truncation (unlike eval history.md context windows).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, "/data/claude-crawl")
from cohort_policy import POLICY_VERSION, policy_fingerprint, scrub_text

HERE = "/data/swesimbench-v2-harbor"
ROLE_LABELS = {
    "user": "DEVELOPER",
    "assistant": "AGENT",
    "system": "SYSTEM",
    "tool": "TOOL",
    "metadata": "METADATA",
}


def slug(s: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", s)


def safe_sid(sid: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", sid)


def format_turn(role: str, text: str) -> str:
    label = ROLE_LABELS.get(role, "METADATA")
    body = scrub_text(text or "").rstrip()
    return f"> {label}\n\n{body}"


def yaml_escape(s: str) -> str:
    s = s or ""
    if re.search(r'[:#{}[\],&*?|>!%@`]|^\s|\s$|\n|"', s):
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s or '""'


def render_session(meta: dict, turns: list) -> str:
    lines = [
        "---",
        f"session_id: {yaml_escape(meta['session_id'])}",
        f"developer: {yaml_escape(meta['user'])}",
        f"split: train",
        f"source: {yaml_escape(meta.get('source') or '')}",
        f"repo: {yaml_escape(meta.get('repo') or '')}",
        f"start_time: {yaml_escape(meta.get('start_time') or '')}",
        f"n_turns: {len(turns)}",
        f"policy_version: {yaml_escape(POLICY_VERSION)}",
        "---",
        "",
    ]
    body = "\n\n".join(format_turn(t.get("role"), t.get("text")) for t in turns)
    lines.append(body)
    if not body.endswith("\n"):
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default=os.path.join(HERE, "train"),
        help="output directory (default: /data/swesimbench-v2-harbor/train)",
    )
    a = ap.parse_args()
    out = a.out

    clean_manifest = json.load(open(os.path.join(HERE, "clean_manifest.json")))
    assert clean_manifest["policy_version"] == POLICY_VERSION
    assert clean_manifest["policy_fingerprint"] == policy_fingerprint()

    train_meta = {}  # sid -> {user, repo, ts, ... from manifest}
    per_user = {}
    for u in clean_manifest["users"]:
        per_user[u["user"]] = {
            "developer": u["user"],
            "slug": slug(u["user"]),
            "train_sessions": len(u["train_sessions"]),
            "train_turns": u.get("train_turns", 0),
            "sources": u.get("sources", []),
        }
        for x in u["train_sessions"]:
            train_meta[x["sid"]] = {
                "user": u["user"],
                "repo": x.get("repo") or "",
                "start_time": x.get("ts") or "",
            }

    # wipe + recreate
    if os.path.isdir(out):
        for root, dirs, files in os.walk(out, topdown=False):
            for f in files:
                os.remove(os.path.join(root, f))
            for d in dirs:
                os.rmdir(os.path.join(root, d))
    os.makedirs(out, exist_ok=True)

    written = 0
    missing = 0
    by_dev_files = defaultdict(list)
    seen = set()

    for line in open(os.path.join(HERE, "clean_sessions.jsonl")):
        s = json.loads(line)
        sid = s["session_id"]
        if sid not in train_meta:
            continue
        seen.add(sid)
        m = train_meta[sid]
        meta = {
            "session_id": sid,
            "user": m["user"],
            "source": s.get("source") or "",
            "repo": s.get("repo") or m.get("repo") or "",
            "start_time": s.get("start_time") or m.get("start_time") or "",
        }
        dev_dir = os.path.join(out, slug(m["user"]))
        os.makedirs(dev_dir, exist_ok=True)
        path = os.path.join(dev_dir, f"{safe_sid(sid)}.md")
        with open(path, "w") as f:
            f.write(render_session(meta, s.get("turns") or []))
        by_dev_files[m["user"]].append(os.path.relpath(path, out))
        written += 1
        if written % 1000 == 0:
            print(f"wrote {written}/{len(train_meta)}", flush=True)

    missing = len(train_meta) - len(seen)
    if missing:
        print(f"WARNING: {missing} train sids missing from clean_sessions.jsonl", flush=True)

    manifest = {
        "policy_version": POLICY_VERSION,
        "policy_fingerprint": policy_fingerprint(),
        "cohort_fingerprint": clean_manifest.get("cohort_fingerprint"),
        "split": "train",
        "developers": len(per_user),
        "sessions": written,
        "format": "markdown-blockquote-turns",
        "layout": "train/<developer_slug>/<session_id>.md",
        "users": sorted(
            [
                {
                    **per_user[u],
                    "files": len(by_dev_files[u]),
                }
                for u in per_user
            ],
            key=lambda r: r["slug"],
        ),
    }
    json.dump(manifest, open(os.path.join(out, "_manifest.json"), "w"), indent=2)
    open(os.path.join(out, "README.md"), "w").write(
        f"""# SWESimBench v2 — train sessions

Scrubbed **train-split** coding-agent sessions for the Opus-era clean cohort
({manifest['developers']} developers, {manifest['sessions']} sessions).

Not Harbor tasks. Held-out prediction points live under `../tasks/`.

## Layout

```text
train/
  _manifest.json
  <developer_slug>/
    <session_id>.md
```

## File format

YAML frontmatter (`session_id`, `developer`, `source`, `repo`, `start_time`, …)
then the full conversation in the same markdown turn format as eval `history.md`:

```markdown
> DEVELOPER

…

> AGENT

…
```

Turns are **not** word-truncated (eval histories are, for context-window sizing).
Secrets are already scrubbed by the clean-cohort pipeline.

Policy: `{POLICY_VERSION}`.
"""
    )
    print(f"exported {written} train sessions -> {out} ({missing} missing)")


if __name__ == "__main__":
    main()
