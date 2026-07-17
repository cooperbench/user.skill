"""TruffleHog verified-secret scan + redact (Joe steps 5 + 7)."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path


def sanitize_detector_name(name: str) -> str:
    tag = re.sub(r"[^A-Z0-9]+", "_", (name or "SECRET").upper()).strip("_")
    return tag[:64]


def find_trufflehog_bin(explicit: str | None = None) -> str:
    if explicit and Path(explicit).exists():
        return explicit
    for candidate in (
        shutil.which("trufflehog"),
        "/data/swesimbench-v2-harbor/.local/bin/trufflehog",
        str(Path.home() / "go/bin/trufflehog"),
        "/usr/local/bin/trufflehog",
    ):
        if candidate and Path(candidate).exists():
            return candidate
    raise FileNotFoundError(
        "trufflehog binary not found; install to "
        "/data/swesimbench-v2-harbor/.local/bin/trufflehog"
    )


_USERINFO_RE = re.compile(r"^[a-z][a-z0-9+.-]*://([^/@\s:]+:[^/@\s]+)@")


def _userinfo_from_url(raw: str | None) -> str | None:
    if not raw:
        return None
    m = _USERINFO_RE.match(raw)
    return m.group(1) if m else None


def run_trufflehog(
    paths: list[Path],
    bin_path: str | None = None,
    results: str = "verified",
) -> dict[str, str]:
    """Return {secret_string -> detector_name} for verified findings."""
    bin_path = find_trufflehog_bin(bin_path)
    existing = [str(p) for p in paths if p.exists()]
    if not existing:
        return {}
    cmd = [bin_path, "filesystem", "--json", f"--results={results}", *existing]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    findings: dict[str, str] = {}

    def _record(secret: str | None, det: str) -> None:
        if secret and secret not in findings and len(secret) >= 6:
            findings[secret] = det

    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        det = obj.get("DetectorName") or "SECRET"
        _record(obj.get("Raw"), det)
        _record(obj.get("RawV2"), det)
        _record(_userinfo_from_url(obj.get("Raw")), det)
        _record(_userinfo_from_url(obj.get("RawV2")), det)
    if proc.returncode not in (0, 1) and proc.stderr:
        # trufflehog may exit 1 when findings exist depending on version.
        print(f"[trufflehog] exit={proc.returncode} stderr_tail={proc.stderr[-500:]}", flush=True)
    return findings


def redact_with_findings(text: str, findings: dict[str, str]):
    """Replace secret strings with <TRUFFLEHOG_REDACTED_*> placeholders."""
    if not text or not findings:
        return text, Counter()
    hits: Counter[str] = Counter()
    # Longest-first to avoid prefix collisions.
    repl = sorted(
        (
            (raw, f"<TRUFFLEHOG_REDACTED_{sanitize_detector_name(det)}>")
            for raw, det in findings.items()
        ),
        key=lambda kv: len(kv[0]),
        reverse=True,
    )
    out = text
    for raw, placeholder in repl:
        if raw in out:
            n = out.count(raw)
            out = out.replace(raw, placeholder)
            hits[placeholder.strip("<>")] += n
    return out, hits


def scan_text_blob(text: str, bin_path: str | None = None, results: str = "verified"):
    """Write text to a temp file, scan, return findings map."""
    if not text:
        return {}
    tmp_dir = Path(tempfile.mkdtemp(prefix="thog_"))
    try:
        path = tmp_dir / "blob.txt"
        path.write_text(text, encoding="utf-8", errors="replace")
        return run_trufflehog([path], bin_path=bin_path, results=results)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def scan_paths(paths: list[Path], bin_path: str | None = None, results: str = "verified"):
    return run_trufflehog(paths, bin_path=bin_path, results=results)
