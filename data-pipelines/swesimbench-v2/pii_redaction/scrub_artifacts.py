#!/usr/bin/env python3
"""Apply the full secrets+PII scrub to SWESimBench train + eval artifacts.

Targets (canonical paths used by site/datasets):
  * train: clean_sessions.jsonl (+ train/ markdown if present)
  * eval:  datasets/eval/**/environment/history.md, instruction.md, tests/gold*
  * v2tasks: v2tasks/inline/**/instruction.md, tests/gold.json
  * kevin: /tmp/user.skill-kevin/tasks/** (annotator source) when present

Backs up large files before in-place rewrite. Writes a redaction count report.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/data/swesimbench-v2-harbor")
sys.path.insert(0, str(ROOT))
sys.path.insert(0, "/data/claude-crawl")

from pii_redaction.pipeline import ScrubPipeline, ScrubStats  # noqa: E402
from pii_redaction.trufflehog import scan_paths, find_trufflehog_bin  # noqa: E402

HISTORY_ROLE_RE = re.compile(
    r"(?m)^> (DEVELOPER|AGENT|TOOL|SYSTEM|METADATA)\s*$"
)
TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def backup_file(path: Path, backup_dir: Path) -> Path | None:
    if not path.exists() or not path.is_file():
        return None
    backup_dir.mkdir(parents=True, exist_ok=True)
    dest = backup_dir / f"{path.name}.{TS}.bak"
    # Hardlink when possible (same filesystem) to avoid doubling 4GB.
    try:
        os.link(path, dest)
    except OSError:
        shutil.copy2(path, dest)
    return dest


def split_history_blocks(text: str) -> list[tuple[str | None, str]]:
    """Return list of (role_or_None, block_text) for history.md blockquotes."""
    if not text:
        return []
    parts = re.split(r"(?m)(?=^> (?:DEVELOPER|AGENT|TOOL|SYSTEM|METADATA)\s*$)", text)
    out: list[tuple[str | None, str]] = []
    for part in parts:
        if not part:
            continue
        m = HISTORY_ROLE_RE.match(part)
        if m:
            out.append((m.group(1), part))
        else:
            out.append((None, part))
    return out


def scrub_history_md(text: str, pipe: ScrubPipeline) -> str:
    blocks = split_history_blocks(text)
    if not blocks:
        return pipe.scrub_all_roles(text)
    out: list[str] = []
    for role, block in blocks:
        if role in ("DEVELOPER", "AGENT"):
            m = HISTORY_ROLE_RE.match(block)
            if m:
                body_start = m.end()
                if body_start < len(block) and block[body_start] == "\n":
                    body_start += 1
                header = block[:body_start]
                body = pipe.scrub(block[body_start:], role=role)
                out.append(header + body)
            else:
                out.append(pipe.scrub(block, role=role))
        else:
            # Tool/system/metadata: regex + trufflehog only (Joe skips Presidio).
            out.append(pipe.scrub_all_roles(block))
    return "".join(out)


def scrub_jsonl_sessions(
    src: Path,
    dst: Path,
    pipe: ScrubPipeline,
    progress_every: int = 100,
    presidio_roles: frozenset[str] | None = None,
):
    """Rewrite sessions JSONL.

    ``presidio_roles`` restricts which roles get NER (default: pipeline NL roles).
    Use ``frozenset({"user"})`` for a faster train pass — Joe-style PERSON
    validators almost never fire on long assistant code dumps anyway.
    """
    n = 0
    with src.open("r", encoding="utf-8", errors="replace") as fin, dst.open(
        "w", encoding="utf-8"
    ) as fout:
        for line in fin:
            if not line.strip():
                continue
            rec = json.loads(line)
            for turn in rec.get("turns") or []:
                role = turn.get("role") or ""
                text = turn.get("text")
                if not isinstance(text, str):
                    continue
                if presidio_roles is not None and role not in presidio_roles:
                    turn["text"] = pipe.scrub(text, role=role, apply_presidio=False)
                else:
                    turn["text"] = pipe.scrub(text, role=role)
            # Also scrub any top-level free-text fields if present.
            for key in ("prompt_text", "title", "summary"):
                if isinstance(rec.get(key), str):
                    rec[key] = pipe.scrub_all_roles(rec[key])
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
            if n % progress_every == 0:
                print(
                    f"  clean_sessions {n}  changed={pipe.stats.texts_changed} "
                    f"presidio={sum(pipe.stats.presidio.values())}",
                    flush=True,
                )
    return n


def scrub_text_file(path: Path, pipe: ScrubPipeline, *, history: bool = False) -> bool:
    original = path.read_text(encoding="utf-8", errors="replace")
    if history or path.name == "history.md":
        new = scrub_history_md(original, pipe)
    else:
        # instruction.md / gold-adjacent: treat as mixed; Presidio on whole text
        # is OK for short gold fields; for long instruction transcripts use history parser
        # when blockquotes are present.
        if "> DEVELOPER" in original or "> AGENT" in original:
            new = scrub_history_md(original, pipe)
        else:
            new = pipe.scrub(original, role="user")
    if new != original:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def scrub_json_file(path: Path, pipe: ScrubPipeline, text_keys: tuple[str, ...]) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        return False
    changed = False

    def walk(obj):
        nonlocal changed
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, str) and (k in text_keys or k.endswith("_md") or k.endswith("_text")):
                    nv = pipe.scrub(v, role="user")
                    if nv != v:
                        obj[k] = nv
                        changed = True
                else:
                    walk(v)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                if isinstance(v, str):
                    continue
                walk(v)

    walk(data)
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def collect_trufflehog_targets(targets: set[str]) -> list[Path]:
    paths: list[Path] = []
    if "train" in targets:
        p = ROOT / "clean_sessions.jsonl"
        if p.exists():
            paths.append(p)
        train_dir = ROOT / "train"
        if train_dir.is_dir():
            paths.append(train_dir)
    if "eval" in targets:
        eval_dir = ROOT / "datasets" / "eval"
        if eval_dir.is_dir():
            paths.append(eval_dir)
    if "v2tasks" in targets:
        v2 = ROOT / "v2tasks"
        if v2.is_dir():
            paths.append(v2)
    if "kevin" in targets:
        kevin = Path("/tmp/user.skill-kevin/tasks")
        if kevin.is_dir():
            paths.append(kevin)
    return paths


def run_global_trufflehog(targets: set[str], bin_path: str | None, results: str) -> dict[str, str]:
    paths = collect_trufflehog_targets(targets)
    print(f"[trufflehog] scanning {len(paths)} roots …", flush=True)
    try:
        find_trufflehog_bin(bin_path)
    except FileNotFoundError as exc:
        print(f"[trufflehog] SKIP: {exc}", flush=True)
        return {}
    t0 = time.time()
    findings = scan_paths(paths, bin_path=bin_path, results=results)
    print(
        f"[trufflehog] {len(findings)} unique secrets in {time.time()-t0:.1f}s",
        flush=True,
    )
    return findings


def process_train(
    pipe: ScrubPipeline,
    backup_dir: Path,
    enable_presidio_train: bool,
    presidio_train_roles: str = "user",
) -> dict:
    src = ROOT / "clean_sessions.jsonl"
    if not src.exists():
        return {"skipped": True, "reason": "missing clean_sessions.jsonl"}
    bak = backup_file(src, backup_dir)
    print(f"[train] backup -> {bak}", flush=True)

    old_presidio = pipe.enable_presidio
    role_set: frozenset[str] | None = None
    if not enable_presidio_train:
        pipe.enable_presidio = False
        print(
            "[train] Presidio disabled for clean_sessions (regex+trufflehog only)",
            flush=True,
        )
    else:
        roles = {r.strip() for r in presidio_train_roles.split(",") if r.strip()}
        role_set = frozenset(roles) if roles else None
        print(
            f"[train] Presidio on roles={sorted(role_set) if role_set else 'all-NL'} "
            f"in clean_sessions",
            flush=True,
        )

    tmp = src.with_suffix(".jsonl.scrubbing")
    n = scrub_jsonl_sessions(src, tmp, pipe, presidio_roles=role_set)
    os.replace(tmp, src)
    pipe.enable_presidio = old_presidio

    train_md = ROOT / "train"
    md_files = 0
    if train_md.is_dir():
        for path in train_md.rglob("*.md"):
            if scrub_text_file(path, pipe, history=True):
                md_files += 1
    return {
        "sessions": n,
        "train_md_changed": md_files,
        "backup": str(bak),
        "presidio": enable_presidio_train,
        "presidio_roles": sorted(role_set) if role_set else None,
    }


def process_eval(pipe: ScrubPipeline) -> dict:
    eval_dir = ROOT / "datasets" / "eval"
    if not eval_dir.is_dir():
        return {"skipped": True}
    hist_changed = 0
    instr_changed = 0
    gold_changed = 0
    n_hist = 0
    for hist in eval_dir.glob("*/environment/history.md"):
        n_hist += 1
        if scrub_text_file(hist, pipe, history=True):
            hist_changed += 1
        if n_hist % 100 == 0:
            print(f"  eval histories {n_hist}", flush=True)
        instr = hist.parent.parent / "instruction.md"
        if instr.exists() and scrub_text_file(instr, pipe):
            instr_changed += 1
        for gold in (hist.parent.parent / "tests").glob("gold*"):
            if gold.suffix == ".json" or gold.suffix == ".jsonl":
                if scrub_json_file(
                    gold,
                    pipe,
                    text_keys=("real", "prev_agent", "content", "text", "prompt"),
                ):
                    gold_changed += 1
            elif gold.suffix == ".md":
                if scrub_text_file(gold, pipe):
                    gold_changed += 1
    return {
        "histories": n_hist,
        "history_changed": hist_changed,
        "instruction_changed": instr_changed,
        "gold_changed": gold_changed,
    }


def process_v2tasks(pipe: ScrubPipeline) -> dict:
    inline = ROOT / "v2tasks" / "inline"
    if not inline.is_dir():
        return {"skipped": True}
    changed = Counter()
    n = 0
    for tid_dir in sorted(inline.glob("t*")):
        n += 1
        instr = tid_dir / "instruction.md"
        if instr.exists() and scrub_text_file(instr, pipe):
            changed["instruction"] += 1
        gold = tid_dir / "tests" / "gold.json"
        if gold.exists() and scrub_json_file(
            gold, pipe, text_keys=("real", "prev_agent", "content", "text")
        ):
            changed["gold"] += 1
    return {"tasks": n, "changed": dict(changed)}


def process_kevin(pipe: ScrubPipeline) -> dict:
    kevin = Path("/tmp/user.skill-kevin/tasks")
    if not kevin.is_dir():
        return {"skipped": True}
    hist_changed = 0
    gold_changed = 0
    n = 0
    for hist in kevin.glob("*/environment/history.md"):
        n += 1
        if scrub_text_file(hist, pipe, history=True):
            hist_changed += 1
        gold = hist.parent.parent / "tests" / "gold.json"
        if gold.exists() and scrub_json_file(
            gold, pipe, text_keys=("real", "prev_agent", "content", "text")
        ):
            gold_changed += 1
    return {"tasks": n, "history_changed": hist_changed, "gold_changed": gold_changed}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--targets",
        default="train,eval,v2tasks,kevin",
        help="Comma list: train,eval,v2tasks,kevin",
    )
    ap.add_argument("--report", type=Path, default=ROOT / "meta" / "pii_scrub_report.json")
    ap.add_argument("--backup-dir", type=Path, default=ROOT / "meta" / "pii_backups")
    ap.add_argument("--trufflehog-bin", default=None)
    ap.add_argument("--trufflehog-results", default="verified")
    ap.add_argument("--skip-trufflehog", action="store_true")
    ap.add_argument("--skip-presidio", action="store_true")
    ap.add_argument(
        "--presidio-train",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Run Presidio NER on clean_sessions (default: on; roles via --presidio-train-roles)",
    )
    ap.add_argument(
        "--presidio-train-roles",
        default="user",
        help="Comma roles for train Presidio (default: user). Use user,assistant for Joe-full.",
    )
    ap.add_argument("--model", default="en_core_web_sm")
    args = ap.parse_args()

    targets = {t.strip() for t in args.targets.split(",") if t.strip()}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.backup_dir.mkdir(parents=True, exist_ok=True)

    findings: dict[str, str] = {}
    if not args.skip_trufflehog:
        findings = run_global_trufflehog(targets, args.trufflehog_bin, args.trufflehog_results)
        # Persist detector names only (never secret values) for the report.
        finding_types = Counter(findings.values())
    else:
        finding_types = Counter()

    pipe = ScrubPipeline(
        enable_presidio=not args.skip_presidio,
        enable_trufflehog_findings=bool(findings),
        trufflehog_findings=findings,
        model_name=args.model,
    )

    results: dict = {
        "ts": TS,
        "targets": sorted(targets),
        "trufflehog_unique_secrets": len(findings),
        "trufflehog_by_detector": dict(finding_types.most_common()),
        "presidio_enabled": not args.skip_presidio,
        "presidio_train": args.presidio_train,
        "model": args.model,
    }

    t0 = time.time()
    if "train" in targets:
        print("[train] scrubbing clean_sessions.jsonl …", flush=True)
        results["train"] = process_train(
            pipe,
            args.backup_dir,
            enable_presidio_train=args.presidio_train,
            presidio_train_roles=args.presidio_train_roles,
        )
    if "eval" in targets:
        print("[eval] scrubbing datasets/eval …", flush=True)
        # Fresh stats slice: keep cumulative in pipe.stats
        results["eval"] = process_eval(pipe)
    if "v2tasks" in targets:
        print("[v2tasks] scrubbing …", flush=True)
        results["v2tasks"] = process_v2tasks(pipe)
    if "kevin" in targets:
        print("[kevin] scrubbing annotator source tasks …", flush=True)
        results["kevin"] = process_kevin(pipe)

    results["stats"] = pipe.stats.as_dict()
    results["elapsed_sec"] = round(time.time() - t0, 1)
    args.report.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))
    print(f"wrote report {args.report}", flush=True)


if __name__ == "__main__":
    main()
