#!/usr/bin/env python3
"""Run deterministic baseline and train400 verifier smoke checks."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WORKSPACE = Path("/data/swesimbench-v2-harbor")
TASK = "yyovil__a5d654fb"
TASKS = {
    "baseline": REPO / "datasets" / "eval-620" / TASK,
    "train400": WORKSPACE / "datasets" / "eval-train400" / TASK,
}

FAKE_AGENT = """\
#!/usr/bin/env python3
import json
import sys

prompt = sys.argv[-1]
if "<message>fixture prediction message</message>" in prompt:
    acts = ["steer", "inquiry"]
else:
    acts = ["critical", "steer"]
print(json.dumps({"acts": acts}))
"""


def run_one(name: str, task: Path, root: Path) -> dict:
    tests_dir = root / "tests"
    sim_dir = root / "sim"
    logs_dir = root / "logs"
    tests_dir.mkdir(parents=True)
    sim_dir.mkdir(parents=True)
    logs_dir.mkdir(parents=True)
    (tests_dir / "gold.json").write_text(
        (task / "tests" / "gold.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (sim_dir / "answer.txt").write_text(
        "fixture prediction message", encoding="utf-8"
    )
    agent = root / "agent"
    agent.write_text(FAKE_AGENT, encoding="utf-8")
    agent.chmod(0o755)

    env = os.environ.copy()
    env.update(
        {
            "CURSOR_API_KEY": "fixture-not-a-real-key",
            "CURSOR_AGENT_BIN": str(agent),
            "SIMBENCH_TESTS_DIR": str(tests_dir),
            "SIMBENCH_SIM_DIR": str(sim_dir),
            "SIMBENCH_VERIFIER_LOG_DIR": str(logs_dir),
        }
    )
    subprocess.run(
        [sys.executable, str(task / "tests" / "verify.py")],
        check=True,
        env=env,
    )
    verdict = json.loads((logs_dir / "verdict.json").read_text())
    assert verdict["gold_acts"] == ["critical", "steer"], verdict
    assert verdict["pred_acts"] == ["steer", "inquiry"], verdict
    assert verdict["jaccard"] == 1 / 3, verdict
    assert verdict["reward"] == 1 / 3, verdict
    assert verdict["exact_match"] is False, verdict
    print(
        f"{name}: gold_acts={verdict['gold_acts']} "
        f"pred_acts={verdict['pred_acts']} "
        f"jaccard={verdict['jaccard']}"
    )
    return verdict


def main() -> None:
    template = (
        REPO
        / "data-pipelines"
        / "swesimbench-v2"
        / "verify_multilabel.py"
    ).read_bytes()
    for name, task in TASKS.items():
        if (task / "tests" / "verify.py").read_bytes() != template:
            raise RuntimeError(f"{name} task verifier differs from template")

    with tempfile.TemporaryDirectory(prefix="userbench-smoke-") as tmp:
        root = Path(tmp)
        results = {
            name: run_one(name, task, root / name)
            for name, task in TASKS.items()
        }
        summary = root / "smoke-summary.json"
        summary.write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
