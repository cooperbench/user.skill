#!/usr/bin/env python3
"""Audit fresh anonymous UserBench downloads and public task pages."""
from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

import httpx

from harbor.db.client import RegistryDB

PACKAGES = {
    "UserBench": (7, "5ae6956f943da5d0781cf835cd8025a0411160321bb048f12c77bde7aac46bda"),
    "UserBench-train400": (
        4,
        "ed4a2f13efe35bec348b5da764c9ccb290443a9d42d622f055eb701dc5c0d2ab",
    ),
}
HUB = "https://hub.harborframework.com"


async def resolve_refs() -> dict:
    db = RegistryDB()
    result = {}
    for name, (expected_revision, expected_hash) in PACKAGES.items():
        refs = {}
        for ref in ("latest", "v2"):
            _, version = await db.resolve_dataset_version(
                "userbench", name, ref
            )
            tasks = await db.get_dataset_version_tasks(version["id"])
            refs[ref] = {
                "revision": version["revision"],
                "content_hash": version["content_hash"],
                "id": version["id"],
                "tasks": len(tasks),
            }
        assert refs["latest"] == refs["v2"], refs
        assert refs["latest"]["revision"] == expected_revision, refs
        assert refs["latest"]["content_hash"] == expected_hash, refs
        assert refs["latest"]["tasks"] == 620, refs
        result[name] = refs
    return result


async def check_pages(task_names: list[str]) -> dict:
    semaphore = asyncio.Semaphore(32)
    failures: list[str] = []

    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=30,
        headers={"User-Agent": "UserBench-public-audit/1.0"},
    ) as client:
        async def check(url: str) -> None:
            async with semaphore:
                response = await client.get(url)
                if response.status_code != 200:
                    failures.append(f"{response.status_code} {url}")

        urls = [
            f"{HUB}/tasks/userbench/{name}" for name in sorted(task_names)
        ]
        urls.extend(
            f"{HUB}/datasets/userbench/{name}" for name in PACKAGES
        )
        await asyncio.gather(*(check(url) for url in urls))

    if failures:
        raise RuntimeError(
            f"{len(failures)} public page failures: {failures[:10]}"
        )
    return {"task_pages_200": len(task_names), "dataset_pages_200": 2}


def verify_download(root: Path, package: str) -> tuple[dict, list[str]]:
    package_root = root / package
    task_dirs = sorted(
        path
        for path in package_root.iterdir()
        if path.is_dir() and (path / "task.toml").exists()
    )
    assert len(task_dirs) == 620, (package, len(task_dirs))
    verifiers = [
        (task / "tests" / "verify.py").read_text(encoding="utf-8")
        for task in task_dirs
    ]
    assert len(set(verifiers)) == 1, package
    assert all(
        '"scoring": "multilabel_jaccard_v1"' in verifier
        and '"pred_acts": pred_acts' in verifier
        and '"gold_acts": gold_acts' in verifier
        and '"jaccard": reward' in verifier
        and "Choose exactly one" not in verifier
        for verifier in verifiers
    )
    return {
        "tasks": len(task_dirs),
        "unique_verifiers": len(set(verifiers)),
        "all_multilabel_jaccard": True,
    }, [task.name for task in task_dirs]


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("audit_root", type=Path)
    args = parser.parse_args()

    downloads = {}
    task_names: list[str] | None = None
    for package, subdir in (
        ("UserBench", "baseline"),
        ("UserBench-train400", "train400"),
    ):
        summary, names = verify_download(
            args.audit_root / subdir, package
        )
        downloads[package] = summary
        if task_names is None:
            task_names = names
        else:
            assert names == task_names, "package task selections differ"

    report = {
        "refs": await resolve_refs(),
        "anonymous_downloads": downloads,
        "public_pages": await check_pages(task_names or []),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    asyncio.run(main())
