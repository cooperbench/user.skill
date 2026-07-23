#!/usr/bin/env python3
"""Build a 100-item gold_acts annotation sample for the UserBench annotator.

Filters compaction/continuation summaries out of prediction targets.
Canonical copy for website regenerations; keep in sync with
`swesimbench-annotator/scripts/build_sample.py` when both are used.

Sources (priority):
  1. cooperbench/user.skill @kevin tasks with filled gold_move + history.md
  2. v2tasks/inline filled golds, with kevin history.md when matched else
     instruction.md <transcript> converted to history.md blockquote format

Writes:
  public/data/items.json
  public/data/meta.json
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "public" / "data"
KEVIN = Path("/data/user.skill-kevin/tasks")
V2_INLINE = Path("/data/swesimbench-v2-harbor/v2tasks/inline")
N_TARGET = 100
VALID = ("approve", "critical", "steer", "inquiry")
# Legacy gold_move "directive" accepted and rewritten to "steer".
LEGACY_MOVE = {"directive": "steer"}

# Compaction / continuation summaries are harness injects, not developer turns.
COMPACTION_PREFIXES = (
    "this session is being continued",
    "this conversation is being continued",
    "the conversation was compacted",
    "conversation continued from a previous",
)


def is_compaction_continuation(text: str) -> bool:
    """True for context-compaction summaries that must not be prediction targets."""
    t = (text or "").strip()
    if not t:
        return False
    head = t[:400].lower()
    if any(head.startswith(p) for p in COMPACTION_PREFIXES):
        return True
    # Long Claude Code form: prefix + "ran out of context" + summary blurb.
    if "ran out of context" in head and "summary below covers" in head:
        return True
    return False


def canonicalize_act(a: str) -> str:
    a = a.strip().lower()
    return LEGACY_MOVE.get(a, a)


def normalize_acts(raw) -> list[str] | None:
    if raw is None:
        return None
    if isinstance(raw, str):
        a = canonicalize_act(raw)
        return [a] if a in VALID else None
    if isinstance(raw, (list, tuple)):
        out = []
        for x in raw:
            if isinstance(x, str):
                a = canonicalize_act(x)
                if a in VALID and a not in out:
                    out.append(a)
        out = [c for c in VALID if c in out]
        return out or None
    return None
# Earlier context is kept in full (UI scrolls to the tail by the target turn).
# Set env CONTEXT_TRIM=1 to restore legacy size caps for local debugging.
CTX_MAX_CHARS = int(__import__("os").environ.get("CONTEXT_MAX_CHARS", "0"))
CTX_MAX_TURNS = int(__import__("os").environ.get("CONTEXT_MAX_TURNS", "0"))
TRIM_CONTEXT = __import__("os").environ.get("CONTEXT_TRIM", "").strip() in {
    "1",
    "true",
    "yes",
}

ROLE_MAP = {
    "DEVELOPER": "DEVELOPER",
    "AGENT": "AGENT",
    "TOOL": "TOOL",
    "SYSTEM": "SYSTEM",
    "METADATA": "METADATA",
    "user": "DEVELOPER",
    "assistant": "AGENT",
    "tool": "TOOL",
    "system": "SYSTEM",
}


def format_turn(label: str, body: str) -> str:
    body = (body or "").rstrip()
    return f"> {label}\n\n{body}"


def transcript_to_history(transcript: str) -> str:
    """Convert [DEVELOPER]/[AGENT]/... blocks to history.md blockquotes."""
    parts = re.split(r"\n(?=\[(?:DEVELOPER|AGENT|TOOL|SYSTEM|METADATA)\]:)", transcript.strip())
    turns = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        m = re.match(r"\[(DEVELOPER|AGENT|TOOL|SYSTEM|METADATA)\]:\s*(.*)", part, re.S)
        if not m:
            continue
        turns.append(format_turn(m.group(1), m.group(2).strip()))
    return "\n\n".join(turns) + ("\n" if turns else "")


def load_v2_instruction_history(tid: str) -> str | None:
    path = V2_INLINE / tid / "instruction.md"
    if not path.exists():
        return None
    text = path.read_text(errors="replace")
    m = re.search(r"<transcript>(.*?)</transcript>", text, re.S)
    if not m:
        return None
    return transcript_to_history(m.group(1))


def split_history_before_target(history: str, real: str, prev_agent: str) -> tuple[str, str]:
    """Return (context_md, target_md). Prefer splitting on the final DEVELOPER turn
    matching `real`; else append target after full history."""
    real = (real or "").strip()
    blocks = re.split(r"(?=\n> (?:DEVELOPER|AGENT|TOOL|SYSTEM|METADATA)\n)", "\n" + history.strip())
    blocks = [b.strip() for b in blocks if b.strip()]

    target_idx = None
    for i in range(len(blocks) - 1, -1, -1):
        b = blocks[i]
        if not b.startswith("> DEVELOPER"):
            continue
        body = re.sub(r"^> DEVELOPER\n\n?", "", b).strip()
        if body == real or body.startswith(real[:120]) or real.startswith(body[:120]):
            target_idx = i
            break

    if target_idx is None:
        # history is prefix-only (common for eval tasks): use all as context
        ctx_blocks = restore_prev_agent_block(blocks, prev_agent)
        ctx = "\n\n".join(ctx_blocks).strip()
        target = format_turn("DEVELOPER", real)
        return ctx, target

    ctx_blocks = blocks[:target_idx]
    # history.md often truncates long AGENT turns with […] while gold.json
    # keeps the full prev_agent (including question lists the user replies to).
    ctx_blocks = restore_prev_agent_block(ctx_blocks, prev_agent)
    ctx = "\n\n".join(ctx_blocks).strip()
    # Ensure target body is the gold `real` text (canonical)
    target = format_turn("DEVELOPER", real)
    return ctx, target


def restore_prev_agent_block(blocks: list[str], prev_agent: str) -> list[str]:
    """Replace the last AGENT block with full gold prev_agent when history truncated it."""
    prev = (prev_agent or "").strip()
    if not prev or not blocks:
        return blocks
    for i in range(len(blocks) - 1, -1, -1):
        if not blocks[i].startswith("> AGENT"):
            continue
        body = re.sub(r"^> AGENT\n\n?", "", blocks[i]).strip()
        truncated = (
            "[…]" in body
            or body.rstrip().endswith("…")
            or "…" in body[-80:]
            or len(prev) > len(body) + 200
        )
        if truncated and (len(prev) >= len(body) or prev.startswith(body[:80])):
            out = list(blocks)
            out[i] = format_turn("AGENT", prev)
            return out
        break
    return blocks


def trim_tail(md: str, max_chars: int = CTX_MAX_CHARS, max_turns: int = CTX_MAX_TURNS) -> str:
    """Optionally keep only the most recent prior turns (off by default)."""
    md = (md or "").strip()
    if not md or not TRIM_CONTEXT:
        return md
    if max_turns <= 0 and max_chars <= 0:
        return md
    blocks = re.split(r"(?=\n> (?:DEVELOPER|AGENT|TOOL|SYSTEM|METADATA)\n)", "\n" + md)
    blocks = [b.strip() for b in blocks if b.strip()]
    if max_turns > 0 and len(blocks) > max_turns:
        blocks = blocks[-max_turns:]
        md = "…\n\n" + "\n\n".join(blocks)
    else:
        md = "\n\n".join(blocks)
    if max_chars <= 0 or len(md) <= max_chars:
        return md
    cut = md[-max_chars:]
    m = re.search(r"\n> (?:DEVELOPER|AGENT|TOOL|SYSTEM|METADATA)\n", cut)
    if m:
        cut = cut[m.start() + 1 :]
    return "…\n\n" + cut.lstrip()


def load_kevin_by_real() -> dict[str, dict]:
    out: dict[str, dict] = {}
    if not KEVIN.exists():
        return out
    for gp in KEVIN.glob("*/tests/gold.json"):
        g = json.loads(gp.read_text())
        g = g[0] if isinstance(g, list) else g
        real = (g.get("real") or "").strip()
        if not real:
            continue
        task_dir = gp.parent.parent
        hist = task_dir / "environment" / "history.md"
        out.setdefault(real, {
            "gold": g,
            "task_id": task_dir.name,
            "history_path": hist if hist.exists() else None,
            "developer": g.get("developer"),
            "point_id": g.get("point_id"),
            "gold_move": g.get("gold_move"),
        })
    return out


def collect_candidates() -> list[dict]:
    kevin = load_kevin_by_real()
    seen_real: set[str] = set()
    items: list[dict] = []

    # Prefer kevin filled labels (full history.md)
    for real, meta in sorted(kevin.items(), key=lambda kv: kv[1]["task_id"]):
        if is_compaction_continuation(real):
            continue
        acts = normalize_acts(meta["gold"].get("gold_acts")) or normalize_acts(meta.get("gold_move"))
        if not acts:
            continue
        gm = acts[0]
        hist_path = meta["history_path"]
        history = hist_path.read_text(errors="replace") if hist_path else ""
        g = meta["gold"]
        ctx, target = split_history_before_target(history, real, g.get("prev_agent") or "")
        items.append({
            "id": f"kevin:{meta['task_id']}",
            "source": "kevin",
            "task_id": meta["task_id"],
            "point_id": meta.get("point_id") or meta["task_id"],
            "developer": meta.get("developer") or "",
            "gold_move": gm,
            "gold_acts": acts,
            "prev_agent": g.get("prev_agent") or "",
            "real": real,
            "context_md": trim_tail(ctx, CTX_MAX_CHARS),
            "target_md": target,
            "judge_model": "composer-2.5",
        })
        seen_real.add(real)

    # Fill from v2tasks/inline
    for gp in sorted(V2_INLINE.glob("t*/tests/gold.json")):
        tid = gp.parent.parent.name
        g = json.loads(gp.read_text())
        g = g[0] if isinstance(g, list) else g
        acts = normalize_acts(g.get("gold_acts")) or normalize_acts(g.get("gold_move"))
        real = (g.get("real") or "").strip()
        if not acts or not real or real in seen_real or is_compaction_continuation(real):
            continue
        gm = acts[0]

        history = ""
        source = "v2tasks"
        task_id = tid
        developer = g.get("dev") or ""
        point_id = g.get("point_id") or tid

        if real in kevin and kevin[real].get("history_path"):
            history = kevin[real]["history_path"].read_text(errors="replace")
            source = "v2tasks+kevin-history"
            task_id = kevin[real]["task_id"]
            developer = kevin[real].get("developer") or developer
            point_id = kevin[real].get("point_id") or point_id
        else:
            history = load_v2_instruction_history(tid) or ""

        ctx, target = split_history_before_target(history, real, g.get("prev_agent") or "")
        # If instruction transcript already ends with agent turn, context is good;
        # ensure prev_agent appears if context is empty.
        if not ctx.strip() and g.get("prev_agent"):
            ctx = format_turn("AGENT", g["prev_agent"])

        items.append({
            "id": f"v2:{tid}",
            "source": source,
            "task_id": task_id,
            "point_id": point_id,
            "developer": developer,
            "gold_move": gm,
            "gold_acts": acts,
            "prev_agent": g.get("prev_agent") or "",
            "real": real,
            "context_md": trim_tail(ctx, CTX_MAX_CHARS),
            "target_md": target,
            "judge_model": "composer-2.5",
        })
        seen_real.add(real)

    return items


def stratified_sample(items: list[dict], n: int) -> list[dict]:
    """Round-robin across labels for a balanced-ish MVP sample."""
    by = defaultdict(list)
    for it in items:
        # Stratify on primary act for balanced sample size.
        by[it["gold_move"]].append(it)
    for k in by:
        by[k].sort(key=lambda x: x["id"])

    labels = [l for l in VALID if by[l]]
    chosen: list[dict] = []
    cursors = {l: 0 for l in labels}
    while len(chosen) < n and labels:
        progressed = False
        for l in list(labels):
            i = cursors[l]
            if i < len(by[l]):
                chosen.append(by[l][i])
                cursors[l] = i + 1
                progressed = True
                if len(chosen) >= n:
                    break
            else:
                labels = [x for x in labels if cursors[x] < len(by[x])]
        if not progressed:
            break

    # stable order by id for the UI
    chosen.sort(key=lambda x: x["id"])
    for i, it in enumerate(chosen, 1):
        it["index"] = i
    return chosen


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    all_items = collect_candidates()
    sample = stratified_sample(all_items, N_TARGET)
    dist = Counter(a for x in sample for a in (x.get("gold_acts") or [x["gold_move"]]))
    src = Counter(x["source"] for x in sample)

    meta = {
        "title": "SWESimBench gold_acts annotator (MVP)",
        "n_items": len(sample),
        "n_candidates": len(all_items),
        "label_dist": dict(dist),
        "source_dist": dict(src),
        "labels": list(VALID),
        "judge_model": "composer-2.5",
        "multi_label": True,
        "gold_mode": "multi",
        "taxonomy": {
            "approve": "greenlight the agent's proposal — go ahead / LGTM; no new task",
            "critical": "asserts something is WRONG — bug/failure/wrong output, or approach mistaken",
            "steer": "assigns a NEW or DIFFERENT task from what the agent just proposed (not mere go-ahead)",
            "inquiry": "goal is an answer/explanation, not asking the agent to do work",
        },
        "notes": (
            "Blind free multi-label. Approve = proceed with agent's proposal; "
            "steer = new/different ask. Primary metrics: Jaccard + per-label κ."
        ),
    }

    (OUT_DIR / "items.json").write_text(json.dumps(sample, ensure_ascii=False))
    (OUT_DIR / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {len(sample)} items -> {OUT_DIR / 'items.json'}")
    print("label_dist", dict(dist))
    print("source_dist", dict(src))
    print("candidates", len(all_items))


if __name__ == "__main__":
    main()
