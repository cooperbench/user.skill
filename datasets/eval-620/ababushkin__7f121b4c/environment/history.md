> DEVELOPER

i'm reviewing the prs open in this repo
specifically the stacks from pr 22 up to 28

lets review the handoff process and its verdicts as that's the focus

explain to me the handoff API with an example of how to use it and give me human friendly version of the happy path and failure mode tests that have been written

> AGENT

I'll dig into the handoff process across PRs 22-28. Let me start by looking at the open PRs and finding the handoff code.

> TOOL

tool_use Bash
id: toolu_01V5wPdztzEeLkAJ111ZMjnz
```json
{
  "command": "gh pr list --state open --limit 30 2>/dev/null | head -40",
  "description": "List open PRs"
}
```

> TOOL

tool_use Bash
id: toolu_01Nz5yeZvC4JZHeCF7xXt8jt
```json
{
  "command": "git log --oneline -15 && echo \"---BRANCHES---\" && git branch -a | head -40",
  "description": "Show recent log and branches"
}
```

> TOOL

tool_result
id: toolu_01V5wPdztzEeLkAJ111ZMjnz
```
Pull Requests
  [open] #29 ABA-371: collapse prompt to skill pointer, delete verify-... (ababushkin)
  [open] #28 fix: harden finishing-sub-agent recovery (timeouts, state... (ababushkin)
  [open] #27 test: cover finishing sub-agent recovery at both halt sites (ababushkin)
  [open] #26 feat: orchestrator spawns finishing sub-agent to recover ... (ababushkin)
  [open] #25 feat: add prompt.build_finishing for finishing-only sub-a... (ababushkin)
  [open] #24 feat: halt cycle on outcome verifier fail, leave worktree... (ababushkin)
  [open] #23 feat: add KR2 schema check for run-log verdict completeness (ababushkin)
  [open] #22 feat: extend handoff schema with verdict fields, wire int... (ababushkin)
```

> TOOL

tool_result
id: toolu_01Nz5yeZvC4JZHeCF7xXt8jt
```
c7addcf chore: add .linear_config tracker binding (team, ops_project)
2d7da43 Revise AGENTS.md with updated guidelines
d80f750 docs: move generic workflow rules to workflow-hooks pack
db0372d Update README with companion plugins information
e2ae465 docs: repoint architecture.html decision refs to ADRs
9ad90a1 docs: split design-decisions.md into one ADR per decision
a5264e3 Remove redundant text in README.md
a64b669 Update README to emphasize project risks
529f32c Update guiding vision and architecture references
b6e0058 Update README with improved project description
1c2c41c Update README with project details and future plans
376b9e3 docs: add ADR §26 on execution-state file ownership
6b34392 docs: merge restated facts in ADR 0002, replace live metaphors
637654c fix: wire stop-guard Stop hook into spawned workers via --settings
bfc9f23 docs: tighten ADR 0002 Context from 8 paragraphs to 6
---BRANCHES---
* main
  ABA-328
  ABA-371
  ABA-373
  ABA-373-handoff-schema
  ABA-393
  ABA-393-01-prompt
  ABA-393-02-orchestrator
  ABA-393-03-tests
  anton/aba-370-n01-thin-supervisor-contract-design-doc-before-build
  docs/adr-0002-merge-restated-facts
  entire/03cf48f-e3b0c4
  entire/05a0d0a-3c86ec
  entire/0712bb4-6bac32
  entire/1bcbcdd-e3b0c4
  entire/2ca0b09-092813
  entire/2d4c277-e3b0c4
  entire/3eae2f5-e3b0c4
  entire/40d44cd-e3b0c4
  entire/506211f-fd34fa
  entire/528d5b0-868b51
  entire/633d422-b584ff
  entire/637654c-e3b0c4
  entire/66b57fb-9d3af8
  entire/6b34392-e3b0c4
  entire/6bc03b1-e3b0c4
  entire/80f400b-e3b0c4
  entire/8ab8766-e3b0c4
  entire/a89c4c8-e3b0c4
  entire/ba6a427-e3b0c4
  entire/c7addcf-e3b0c4
  entire/c888784-91b342
  entire/cf45f9e-e3b0c4
  entire/checkpoints/v1
  entire/de85ea3-9a7bba
  entire/e40e511-e59961
  entire/e7ff918-4b9c7f
  entire/e8f291c-4e06c9
  entire/f52f140-342abd
```

> TOOL

tool_use Bash
id: toolu_019mKdfJf2xkpBtTW24ePaDs
```json
{
  "command": "find . -path ./.git -prune -o -type f -name '*.py' -print | grep -iE 'handoff|verdict|exec' | head -40; echo \"---\"; ls",
  "description": "Find handoff-related files and list root"
}
```

> TOOL

tool_result
id: toolu_019mKdfJf2xkpBtTW24ePaDs
```
./tests/test_grade_verdict.py
./tests/test_handoff.py
./drain_cycle/handoff.py
---
.claude/
.entire/
.private-journal/
.ruff_cache/
.worktrees/
docs/
drain_cycle/
tests/
.drain-guard-tripped  85B
.env  64B
.gitignore  504B
.linear_config  247B
AGENTS.md  13B
CLAUDE.md  223B
LICENSE  1.0K
README.md  16.3K
conftest.py  512B
mise.toml  24B
pyproject.toml  738B
uv.lock  78.1K
```

> TOOL

tool_use Bash
id: toolu_013N96FVk8NC4C9sZhw4Gbvc
```json
{
  "command": "for n in 22 23 24 25 26 27 28; do echo \"=== PR #$n ===\"; gh pr view $n --json title,headRefName,baseRefName -q '.title + \"  [\" + .headRefName + \" -> \" + .baseRefName + \"]\"'; done",
  "description": "Show PR head/base refs for stack 22-28"
}
```

> TOOL

tool_result
id: toolu_013N96FVk8NC4C9sZhw4Gbvc
```
=== PR #22 ===
feat: extend handoff schema with verdict fields, wire into run log  [ABA-373-handoff-schema -> main]
=== PR #23 ===
feat: add KR2 schema check for run-log verdict completeness  [ABA-373 -> ABA-373-handoff-schema]
=== PR #24 ===
feat: halt cycle on outcome verifier fail, leave worktree intact  [ABA-328 -> ABA-373]
=== PR #25 ===
feat: add prompt.build_finishing for finishing-only sub-agent sessions  [ABA-393-01-prompt -> ABA-328]
=== PR #26 ===
feat: orchestrator spawns finishing sub-agent to recover committed-but-unfinished issues  [ABA-393-02-orchestrator -> ABA-393-01-prompt]
=== PR #27 ===
test: cover finishing sub-agent recovery at both halt sites  [ABA-393-03-tests -> ABA-393-02-orchestrator]
=== PR #28 ===
fix: harden finishing-sub-agent recovery (timeouts, state refresh, run log)  [ABA-393 -> ABA-393-03-tests]
```

> AGENT

The stack is linear: `main → #22 → #23 → #24 → #25 → #26 → #27 → #28`. The focus (handoff + verdicts) lives in `drain_cycle/handoff.py` and `tests/test_handoff.py`. Let me read the cumulative tip (PR #28 / branch `ABA-393`).

> TOOL

tool_use Bash
id: toolu_014ku8AxLnTsCjZDQHX3A8ja
```json
{
  "command": "git show ABA-393:drain_cycle/handoff.py",
  "description": "Show handoff.py at stack tip"
}
```

> TOOL

tool_result
id: toolu_014ku8AxLnTsCjZDQHX3A8ja
```
"""Handoff artefact a stack-mode worker leaves behind after submitting PRs.

In stack mode the worker drives PR submission itself via the ``pr-finishing``
skill, which runs ``gt``/``gh`` inside the worktree, posts the Linear
review-summary comment, and records the submitted PRs in
``.drain-handoff.json`` as a ``pr_urls`` list. The orchestrator reads that
list back as its confirmation signal — a present, non-empty ``pr_urls`` means
the skill submitted at least one PR; its absence means submission never
completed and the per-repo chain must halt rather than march on.

Schema v2 adds ``outcome_verdict`` and ``prep_verdict`` fields so the worker
can record its self-assessment. The orchestrator reads these on every exit
path — Done, halted, or errored — and lands them in the run-log entry.
``read_partial`` extracts those fields without the ``pr_urls`` validity gate,
so halt paths can carry whatever verdicts the worker managed to write.

``read`` never raises: a missing or malformed file returns ``None`` so callers
can treat it as "not submitted yet."
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

HANDOFF_FILE = ".drain-handoff.json"


@dataclass(frozen=True)
class PullRequest:
    title: str
    url: str


@dataclass(frozen=True)
class HandoffData:
    pr_urls: tuple[PullRequest, ...]
    outcome_verdict: dict[str, […]

> TOOL

tool_use Bash
id: toolu_01QtkNVctmynbN25edCzpF6o
```json
{
  "command": "git show ABA-393:tests/test_handoff.py",
  "description": "Show test_handoff.py at stack tip"
}
```

> TOOL

tool_result
id: toolu_01QtkNVctmynbN25edCzpF6o
```
"""Tests for ``drain_cycle.handoff``.

``read`` must never raise: a missing file, a truncated JSON write, or a
structurally wrong payload all return ``None``. A well-formed file returns
a typed ``HandoffData`` object listing the submitted PRs. An empty
``pr_urls`` list reads as ``None`` — the skill writes URLs only after a PR
is actually created, so "present but empty" means submission never happened.
"""
from __future__ import annotations

import json
from pathlib import Path

from drain_cycle.handoff import HANDOFF_FILE, HandoffData, PullRequest, read, read_partial, write


def _valid_data() -> HandoffData:
    return HandoffData(
        pr_urls=(
            PullRequest(title="feat: crash-proof filter", url="https://github.com/o/r/pull/1"),
            PullRequest(title="feat: transcript core", url="https://github.com/o/r/pull/2"),
        )
    )


def test_write_then_read_round_trips(tmp_path: Path) -> None:
    data = _valid_data()
    write(tmp_path, data)
    result = read(tmp_path)

    assert result is not None
    assert result.pr_urls == data.pr_urls


def test_read_missing_file_returns_none(tmp_path: Path) -> None:
    assert read(tmp_path) is None


def test_read_malformed_json_returns_none(tmp_path: Path) -> None:
    (tmp_path / HANDOFF_FILE).write_text("not valid json{{{")
    assert read(tmp_path) is None


def test_read_wrong_top_level_type_returns_none(tmp_path: Path) -> None:
    (tmp_path / HANDOFF_FILE).write_text(json.dumps([1, 2, 3]))
    assert read(tmp_path) is None


def test_read_missing_pr_urls_returns_none(tmp_path: Path) -> None:
    (tmp_path / HANDOFF_FILE).write_text(json.dumps({"other": "key"}))
    assert read(tmp_path) is None


def test_read_empty_pr_urls_returns_none(tmp_path: Path) -> None:
    (tmp_path / HANDOFF_FILE).write_text(json.dumps({"pr_urls": []}))
    assert read(tmp_path) is None


def test_read_pr_urls_not_list_returns_none(tmp_path: Path) -> None:
    (tmp_path / HANDOFF_FILE).write_text(json.dumps({"pr_urls": {"title": "x", "url": "y"}}))
    assert […]

> AGENT

Now let me see how the orchestrator consumes these verdicts and lands them in the run log (PR #22–24), plus the KR2 schema check (PR #23).

> TOOL

tool_use Bash
id: toolu_01QpYw4katW3Z8EV215fBegu
```json
{
  "command": "git grep -l -e 'handoff' -e 'read_partial' -e 'outcome_verdict' ABA-393 -- 'drain_cycle/*.py' | sort -u",
  "description": "Find files referencing handoff/verdicts in source"
}
```

> TOOL

tool_result
id: toolu_01QpYw4katW3Z8EV215fBegu
```
ABA-393:drain_cycle/handoff.py
ABA-393:drain_cycle/kr2_check.py
ABA-393:drain_cycle/orchestrator.py
ABA-393:drain_cycle/prompt.py
ABA-393:drain_cycle/runlog.py
ABA-393:drain_cycle/stop_guard.py
```

> TOOL

tool_use Bash
id: toolu_01LyK9MDjYjurXgc6Q93hyYR
```json
{
  "command": "ls drain_cycle && echo \"---runlog?---\" && git grep -l -e 'verdict' -e 'run_log' -e 'run-log' ABA-393 -- 'drain_cycle/*.py'",
  "description": "List source modules and run-log references"
}
```

> TOOL

tool_result
id: toolu_01LyK9MDjYjurXgc6Q93hyYR
```
__init__.py  0B
cli.py  4.4K
console.py  4.8K
flow.py  658B
grade.py  7.0K
grade_draft.py  4.5K
handoff.py  2.5K
limits.py  6.9K
linear.py  12.1K
model.py  1.6K
orchestrator.py  33.3K
progress.py  3.4K
prompt.py  6.9K
repos.py  7.9K
runlog.py  10.7K
status.py  2.2K
stop_guard.py  9.5K
telemetry.py  4.5K
watch.py  8.0K
watch_format.py  6.4K
worker.py  24.3K
worktree.py  9.4K
---runlog?---
ABA-393:drain_cycle/cli.py
ABA-393:drain_cycle/console.py
ABA-393:drain_cycle/grade.py
ABA-393:drain_cycle/grade_draft.py
ABA-393:drain_cycle/handoff.py
ABA-393:drain_cycle/kr2_check.py
ABA-393:drain_cycle/limits.py
ABA-393:drain_cycle/orchestrator.py
ABA-393:drain_cycle/progress.py
ABA-393:drain_cycle/repos.py
ABA-393:drain_cycle/runlog.py
ABA-393:drain_cycle/worker.py
```

> TOOL

tool_use Bash
id: toolu_01WpjpViAw8wG8ZZWVbAnhte
```json
{
  "command": "git show ABA-393:drain_cycle/kr2_check.py",
  "description": "Show KR2 schema check (PR 23)"
}
```

> TOOL

tool_result
id: toolu_01WpjpViAw8wG8ZZWVbAnhte
```
"""KR2 schema check: every Done run-log entry must carry non-null verdicts.

A Done entry without ``outcome_verdict`` or ``prep_verdict`` is uninspectable
— the operator cannot grade the cycle. Null verdicts on non-Done entries are
fine: a halt or error explains the missing assessment via ``halt_reason``.

Usage::

    python -m drain_cycle.kr2_check <run-log.json> [...]

Exits 0 when all Done entries in every file carry both verdicts.
Exits 1 when any Done entry lacks either verdict.
Exits 2 on bad invocation.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def check_file(path: Path) -> list[str]:
    """Return a violation message for each Done entry missing a verdict."""
    try:
        payload = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: unreadable — {exc}"]
    violations: list[str] = []
    for entry in payload.get("entries", []):
        if entry.get("final_linear_state") != "Done":
            continue
        ident = entry.get("issue_identifier", "<unknown>")
        if entry.get("outcome_verdict") is None:
            violations.append(f"{path}: Done entry {ident} missing outcome_verdict")
        if entry.get("prep_verdict") is None:
            violations.append(f"{path}: Done entry {ident} missing prep_verdict")
    return violations


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("usage: kr2_check <run-log.json> [...]", file=sys.stderr)
        return 2
    violations: list[str] = []
    for arg in argv:
        violations.extend(check_file(Path(arg)))
    for v […]

> TOOL

tool_use Bash
id: toolu_013KJpkmDsCiJt6dKZ3ZpkQ8
```json
{
  "command": "git show ABA-393:drain_cycle/orchestrator.py | grep -nE 'handoff\\.|read_partial|outcome_verdict|prep_verdict|finishing|def ' | head -80",
  "description": "Grep orchestrator for handoff/verdict/finishing usage"
}
```

> TOOL

tool_result
id: toolu_013KJpkmDsCiJt6dKZ3ZpkQ8
```
43:"""Model for the finishing sub-agent spawned to recover a committed-but-unfinished
45:mechanical protocol (review → fix → pr-finishing → Done) runs reliably."""
48:def _now_iso() -> str:
52:def _commits_beyond_base(worktree_path: Path, base: str) -> bool:
82:def _emit_summary(log: runlog.RunLog, *, total: int, halted_on: str | None) -> None:
100:def _halt_message(identifier: str, state_name: str, worktree_path: Path) -> str:
111:def _resume_attempts(cycle_id: str, identifier: str) -> int:
151:def _revert_to_pre_halt_state(
179:def _worker_log_fields(result: worker.WorkerResult) -> dict[str, object]:
205:    outcome_verdict: dict | None = None
206:    prep_verdict: dict | None = None
210:def _set_verdict_span_attrs(
218:    if outcome.outcome_verdict is not None:
220:            "issue.outcome_verdict", outcome.outcome_verdict["result"]
222:    if outcome.prep_verdict is not None:
223:        issue_span.set_attribute("issue.prep_verdict", outcome.prep_verdict["result"])
249:    def record(
259:        finishing_runs: list[dict] | None = None,
264:                "outcome_verdict": outcome.outcome_verdict,
265:                "prep_verdict": outcome.prep_verdict,
279:            finishing_runs=finishing_runs,
287:def _debug_enabled() -> bool:
298:def run(
317:def _run(
423:def _drain_one_issue(
639:        def _make_on_progress(m: dict, ident: str):
640:            def _cb(
665:        outcome_verdict: dict | None = None
666:        prep_verdict: dict | None = None
689:        # Read any verdicts the worker recorded in the handoff. M2+-populated
691:        _hov, _hpv = handoff.read_partial(worktree_path)
694:            outcome_verdict=outcome_verdict if outcome_verdict is not None else _hov,
695:            prep_verdict=prep_verdict if prep_verdict is not None else _hpv,
737:        finishing_runs: list[dict] = []
738:        finishing_attempted = […]

> AGENT

I have the core picture. Let me confirm who actually writes the file and check the verdict shapes used downstream.

> TOOL

tool_use Bash
id: toolu_01HbnZ64Pha1ZVzwoCE4msdA
```json
{
  "command": "git grep -nE 'handoff\\.write|handoff\\.read|\\.drain-handoff' ABA-393 -- 'drain_cycle/*.py' 'docs/*' '.claude/*' 2>/dev/null | grep -v test | head; echo \"=== build_finishing ===\"; git show ABA-393:drain_cycle/prompt.py | sed -n '/def build_finishing/,/^def /p' | head -60",
  "description": "Find writers of handoff and show build_finishing"
}
```

> TOOL

tool_result
id: toolu_01HbnZ64Pha1ZVzwoCE4msdA
```
ABA-393:docs/adrs/0002-thin-supervisor-contract.md:8:This ADR pins that split: the 15-line worker prompt template and how its lines are allocated, the `.drain-handoff.json` schema (v2), and where the line between process and workflow falls across every `drain_cycle/` concern. It extends the pack's execution-workflow design doc (`agent-skills-shaper/docs/design-docs/execution-workflow/design-doc.md`) — which owns the `exec:*` skill graph — with the supervisor's half of the contract: what it hands the worker, and what the worker leaves behind. It does not re-open that skill graph.
ABA-393:docs/adrs/0002-thin-supervisor-contract.md:30:- `.drain-handoff.json` must carry the verdict fields the supervisor reads at run-end to (a) grade the run, (b) build the run-log entry, and (c) name the halt reason on any non-Done exit. Every field has a named writer and a named reader.
ABA-393:docs/adrs/0002-thin-supervisor-contract.md:31:- The schema must extend `pickup-envelope.json` rather than duplicate it. `pickup-envelope.json` is the carrier that moves *between skills* during a run; `.drain-handoff.json` is the exit record handed *from the worker back to the supervisor*.
ABA-393:docs/adrs/0002-thin-supervisor-contract.md:40:| Schema-v2 fitness | `.drain-handoff.json` produced by any worker exit parses against the JSON Schema in `docs/adrs/references/drain-handoff-schema-v2.md` and every required field is present per its writer's exit gate | Extract the fenced JSON Schema, validate every `~/.drain-cycle/runs/*.json` against it; exit 0 on every fixture and every […]

> AGENT

I've got the full picture across the stack. Here's the review of the handoff process and its verdicts.

## What the handoff is

`.drain-handoff.json` is the **exit record a stack-mode worker leaves behind** for the orchestrator to read after the worker finishes an issue. It's the one file the supervisor reads to answer three questions on every exit path (Done, halted, or errored):

1. Did the worker actually submit PRs? (`pr_urls`)
2. How did the work self-assess? (`outcome_verdict`, `prep_verdict`) — schema v2
3. If it didn't reach Done, what verdicts did it manage to record before stopping?

The module is `drain_cycle/handoff.py`. Note a division of labour: the **`/shape:pr-finishing` skill writes the JSON** (it owns `gt`/`gh` and the file); the Python `write()` is the canonical serializer/test helper. The **orchestrator only reads** — it's the sole reader of `pr_urls`.

## The API

Three functions and two dataclasses:

```python
@dataclass(frozen=True)
class PullRequest:
    title: str
    url: str

@dataclass(frozen=True)
class HandoffData:
    pr_urls: tuple[PullRequest, ...]
    outcome_verdict: dict | None = None   # the outcome verifier's self-assessment
    prep_verdict: dict | None = None      # the PR-prep routing decision

write(worktree: Path, data: HandoffData) -> None
read(worktree: Path) -> HandoffData | None                       # strict: gated on valid pr_urls
read_partial(worktree: […]