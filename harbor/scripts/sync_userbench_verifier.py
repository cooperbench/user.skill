#!/usr/bin/env python3
"""Sync the canonical UserBench verifier without changing task selection.

This updates only tests/verify.py in the baseline and train400 task trees, plus
the workspace verifier copy used by local smoke jobs. It refuses partial or
mismatched 620-task trees.
"""
from __future__ import annotations

import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WORKSPACE = Path("/data/swesimbench-v2-harbor")
TEMPLATE = (
    REPO / "data-pipelines" / "swesimbench-v2" / "verify_multilabel.py"
)
TREES = [
    REPO / "datasets" / "eval-620",
    WORKSPACE / "datasets" / "eval-620",
    WORKSPACE / "datasets" / "eval-train400",
]


def task_dirs(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.iterdir()
        if path.is_dir() and (path / "task.toml").exists()
    )


def main() -> None:
    verifier = TEMPLATE.read_text(encoding="utf-8")
    if '"scoring": "multilabel_jaccard_v1"' not in verifier:
        raise RuntimeError("canonical verifier lacks multi-label scoring")

    by_tree = {root: task_dirs(root) for root in TREES}
    for root, tasks in by_tree.items():
        if len(tasks) != 620:
            raise RuntimeError(f"{root}: expected 620 tasks, found {len(tasks)}")

    expected = {path.name for path in by_tree[TREES[0]]}
    for root, tasks in by_tree.items():
        names = {path.name for path in tasks}
        if names != expected:
            raise RuntimeError(
                f"{root}: task selection differs from canonical eval-620"
            )

    for root, tasks in by_tree.items():
        for task in tasks:
            destination = task / "tests" / "verify.py"
            destination.write_text(verifier, encoding="utf-8")
        print(f"synced {len(tasks)} verifiers under {root}")

    workspace_copy = WORKSPACE / "scripts" / "verify_composer.py"
    shutil.copyfile(TEMPLATE, workspace_copy)
    print(f"synced workspace verifier {workspace_copy}")


if __name__ == "__main__":
    main()
