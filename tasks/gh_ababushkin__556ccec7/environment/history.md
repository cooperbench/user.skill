> DEVELOPER

why do i see this error when i try to grade my drain-cycle runs? drain-cycle grade: warning: ABA-406 is a draft — excluded from rate

> AGENT

I'll find where that warning comes from in the grade code.

> TOOL

tool_use Bash
id: toolu_013bb8Pwp7FDePE8u5wyoiwQ
```json
{
  "command": "rg -n \"is a draft|excluded from rate|draft\" --type py",
  "description": "Search for draft warning string"
}
```

> TOOL

tool_result ERROR
id: toolu_013bb8Pwp7FDePE8u5wyoiwQ
```
Exit code 2
grep: unrecognized option `--type'
usage: grep [REDACTED] [-A num] [-B num] [-C[num]]
	[-e pattern] [-f file] [--binary-files=value] [--color=when]
	[--context[=num]] [--directories=action] [--label] [--line-buffered]
	[--null] [pattern] [file ...]
```

> TOOL

tool_use Bash
id: toolu_01HBiMcuP8rTfcusbxg1LoeP
```json
{
  "command": "grep -rn \"is a draft\\|excluded from rate\\|is a draft —\" --include=*.py .",
  "description": "Search for draft warning string"
}
```

> TOOL

tool_result ERROR
id: toolu_01HBiMcuP8rTfcusbxg1LoeP
```
Exit code 1
(eval):1: no matches found: --include=*.py
```

> TOOL

tool_use Bash
id: toolu_01NVVKxdU6JxJ5Pqbm5PvwmC
```json
{
  "command": "grep -rn \"excluded from rate\" . ; echo \"---\" ; grep -rn \"is a draft\" .",
  "description": "Search warning strings"
}
```

> TOOL

tool_result
id: toolu_01NVVKxdU6JxJ5Pqbm5PvwmC
```
<persisted-output>
Output too large (165.1KB). Full output saved to: /home/<USER>/.claude/projects/-Users-anton-src-drain-cycle/6d19145b-86d2-4b0d-9077-624706537065/tool-results/b42391o6k.txt

Preview (first 2KB):
Binary file ./drain_cycle/__pycache__/grade.cpython-314.pyc matches
./drain_cycle/grade.py:108:                f"drain-cycle grade: warning: {issue} is a draft — excluded from rate",
Binary file ./.worktrees/ABA-334/drain_cycle/__pycache__/grade.cpython-312.pyc matches
./.worktrees/ABA-334/drain_cycle/grade.py:108:                f"drain-cycle grade: warning: {issue} is a draft — excluded from rate",
./.worktrees/ABA-334/.entire/metadata/51c362f7-1d19-487b-a57d-f83ee5dd1961/full.jsonl:182:{"parentUuid":"88225320-3cfe-4ab1-bb6f-db2839314ea3","isSidechain":false,"message":{"model":"claude-sonnet-4-6","id":"msg_01AgYS8KAfuXvaKEFhWKhmPQ","type":"message","role":"assistant","content":[{"type":"tool_use","id":"toolu_013bi4uDppPLWK7kuLnBFQuQ","name":"Write","input":{"file_path":"/home/<USER>/src/drain-cycle/.worktrees/ABA-334/drain_cycle/grade.py","content":"\"\"\"``drain-cycle grade``: initiative health from confirmed grade files.\n\nReads every grade file at ``~/.drain-cycle/grades/*.md``, separates\nconfirmed from draft, and reports:\n\n1. Total tickets graded (confirmed count).\n2. Pass-rate: confirmed entries without a silent-Done violation,\n   expressed as ``N/D (P%)``.\n3. Silent-Done violations: confirmed Done entries where the outcome\n   verifier never ran (``outcome_verdict == null`` in the run log).\n4. Draft files are warned about on stderr and excluded from the count.\n\nA *silent-Done violation* is the condition the halt-on-fail gate (ABA-328)\nis supposed to prevent: a ticket reaches Done in Linear without the outcome\nverifier running. Only ``outcome_verdict == null`` counts — a verdict of any\nkind (pass or fail) clears the violation.\n\nExit code: 0 if no violations; 1 if any silent-Done violation is found.\n\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport sys\nfrom pathlib import Path\nfrom typing import Any\n\nfrom . import grade_draft, runlog\n\n\ndef default_grades_dir() -> Path:\n    return grade_draft.grades_dir()\n\n\ndef default
...
</persisted-output>
```

> AGENT

The warning lives in `drain_cycle/grade.py:108`. Let me read the surrounding logic.

> TOOL

tool_use Read
id: toolu_01Q2E3MHusYMwuA4TLnZgep6
```json
{
  "file_path": "/home/<USER>/src/drain-cycle/drain_cycle/grade.py",
  "offset": 80,
  "limit": 50
}
```

> TOOL

tool_result
id: toolu_01Q2E3MHusYMwuA4TLnZgep6
```
80	def run(grades_dir: Path, runs_dir: Path) -> int:
81	    """Read grade files, report pass-rate and silent-Done violations.
82	
83	    Returns exit code: 0 (clean) or 1 (violations found).
84	    """
85	    confirmed: list[str] = []
86	    drafts: list[str] = []
87	
88	    if grades_dir.is_dir():
89	        for path in sorted(grades_dir.glob("*.md")):
90	            try:
91	                fm = _parse_frontmatter(path.read_text())
92	            except OSError as exc:
93	                print(
94	                    f"drain-cycle grade: skipping unreadable grade file {path}: {exc}",
95	                    file=sys.stderr,
96	                )
97	                continue
98	            issue = fm.get("issue", path.stem)
99	            status = fm.get("status", "draft")
100	            if status == "confirmed":
101	                confirmed.append(issue)
102	            else:
103	                drafts.append(issue)
104	
105	    if drafts:
106	        for issue in drafts:
107	            print(
108	                f"drain-cycle grade: warning: {issue} is a draft — excluded from rate",
109	                file=sys.stderr,
110	            )
111	
112	    total = len(confirmed)
113	
114	    violations: list[str] = []
115	    no_runlog: list[str] = []
116	
117	    for issue in confirmed:
118	        entry = _find_run_entry(issue, runs_dir)
119	        if entry is None:
120	            no_runlog.append(issue)
121	            continue
122	        if _is_silent_done(entry):
123	            violations.append(issue)
124	
125	    for issue in no_runlog:
126	        print(
127	            f"drain-cycle grade: warning: {issue} confirmed but no run-log entry found",
128	            file=sys.stderr,
129	        )
```

> AGENT

This is a benign warning, not an error. Here's what's happening.

`grade` reads every grade file in `~/.drain-cycle/grades/*.md`. Each file has a frontmatter `status:` field that is either `confirmed` or `draft`. Only `confirmed` files count toward the pass-rate. For any file that is *not* `confirmed`, it prints this warning to stderr and excludes it (`grade.py:98-110`).

So you're seeing this because the grade file for **ABA-406** has `status: draft` (or no `status` field — the default is `draft` per line 99). Let me confirm by looking at the actual file:

> TOOL

tool_use Bash
id: toolu_013CA93yFNnYrbjHdvGN4Aj3
```json
{
  "command": "f=~/.drain-cycle/grades/ABA-406.md; ls -la \"$f\" 2>/dev/null && echo \"--- head ---\" && head -20 \"$f\" 2>/dev/null; echo \"=== all grade files ===\"; ls -la ~/.drain-cycle/grades/ 2>/dev/null",
  "description": "Inspect ABA-406 grade file frontmatter"
}
```

> TOOL

tool_result
id: toolu_013CA93yFNnYrbjHdvGN4Aj3
```
644  /home/<USER>/.drain-cycle/grades/ABA-406.md  432B
--- head ---
---
issue: ABA-406
status: draft
---

## Run summary

- outcome: Done
- started_at: 2026-06-18T11:29:25.408934+00:00
- finished_at: 2026-06-18T11:49:14.390246+00:00
[13 more lines]=== all grade files ===
644  ABA-328.md  434B
644  ABA-358.md  442B
644  ABA-359.md  434B
644  ABA-360.md  431B
644  ABA-362.md  434B
644  ABA-363.md  434B
644  ABA-364.md  434B
644  ABA-365.md  442B
644  ABA-366.md  434B
644  ABA-367.md  442B
644  ABA-370.md  432B
644  ABA-371.md  437B
644  ABA-373.md  434B
644  ABA-377.md  434B
644  ABA-378.md  434B
644  ABA-379.md  434B
644  ABA-380.md  434B
644  ABA-381.md  434B
644  ABA-382.md  434B
644  ABA-384.md  434B
644  ABA-385.md  432B
644  ABA-386.md  431B
644  ABA-388.md  432B
644  ABA-389.md  432B
644  ABA-390.md  432B
644  ABA-392.md  432B
644  ABA-393.md  432B
644  ABA-394.md  432B
644  ABA-398.md  432B
644  ABA-399.md  434B
644  ABA-400.md  434B
644  ABA-401.md  437B
644  ABA-404.md  446B
644  ABA-405.md  433B
644  ABA-406.md  432B
```

> AGENT

Confirmed. It's exactly as expected — not an error.

`~/.drain-cycle/grades/ABA-406.md` has `status: draft` in its frontmatter. The `grade` command splits files into `confirmed` vs everything-else, and warns + excludes anything not yet confirmed so it doesn't pollute the pass-rate (`grade.py:100-110`).

Let me check what flips a grade from `draft` → `confirmed`, so you know how to clear the warning:

> TOOL

tool_use Bash
id: toolu_01DrEop2J9vQB2nPUtYzipQ4
```json
{
  "command": "grep -n \"confirmed\\|status\\|def \" drain_cycle/grade_draft.py | head -40",
  "description": "Inspect grade_draft confirmation flow"
}
```

> TOOL

tool_result
id: toolu_01DrEop2J9vQB2nPUtYzipQ4
```
8 matches in 1 files:

drain_cycle/grade_draft.py:5:``~/.drain-cycle/grades/<issue>.md`` with ``status: draft`` and a populated
drain_cycle/grade_draft.py:25:def grades_dir() -> Path:
drain_cycle/grade_draft.py:34:def grade_path(issue_identifier: str) -> Path:
drain_cycle/grade_draft.py:38:def _find_most_recent_entry(
drain_cycle/grade_draft.py:58:def _render(issue_identifier: str, entry: dict[str, Any]) -> str:
drain_cycle/grade_draft.py:77:"status: draft",
drain_cycle/grade_draft.py:103:def write_draft_from_entry(
drain_cycle/grade_draft.py:116:def run(issue_identifier: str) -> int:
```

> TOOL

tool_use Read
id: toolu_01E7r97wWCoDeeHDKf8k5AM9
```json
{
  "file_path": "/home/<USER>/src/drain-cycle/drain_cycle/grade_draft.py",
  "offset": 58,
  "limit": 40
}
```

> TOOL

tool_result
id: toolu_01E7r97wWCoDeeHDKf8k5AM9
```
58	def _render(issue_identifier: str, entry: dict[str, Any]) -> str:
59	    outcome = entry.get("final_linear_state", "unknown")
60	    duration = entry.get("duration_seconds")
61	    duration_str = f"{duration:.1f}s" if duration is not None else "—"
62	    exit_code = entry.get("exit_code", "—")
63	    model = entry.get("model") or "—"
64	    num_turns = entry.get("num_turns")
65	    num_turns_str = str(num_turns) if num_turns is not None else "—"
66	    cost_usd = entry.get("cost_usd")
67	    cost_str = f"${cost_usd:.4f}" if cost_usd is not None else "—"
68	    usage = entry.get("usage") or {}
69	    tokens_str = str(usage["cumulative"]) if "cumulative" in usage else "—"
70	    halt_reason = entry.get("halt_reason") or "—"
71	    started_at = entry.get("started_at", "—")
72	    finished_at = entry.get("finished_at", "—")
73	
74	    lines = [
75	        "---",
76	        f"issue: {issue_identifier}",
77	        "status: draft",
78	        "---",
79	        "",
80	        "## Run summary",
81	        "",
82	        f"- outcome: {outcome}",
83	        f"- started_at: {started_at}",
84	        f"- finished_at: {finished_at}",
85	        f"- duration: {duration_str}",
86	        f"- exit_code: {exit_code}",
87	        f"- model: {model}",
88	        f"- num_turns: {num_turns_str}",
89	        f"- cost_usd: {cost_str}",
90	        f"- tokens_cumulative: {tokens_str}",
91	        f"- halt_reason: {halt_reason}",
92	        "",
93	        "## KR check",
94	        "",
95	        f"- [ ] KR1: outcome is Done (recorded: {outcome})",
96	        f"- [ ] KR2: duration is acceptable (recorded: {duration_str})",
97	        "- [ […]

> AGENT

That's the full picture. Here's the answer.

## Why you see the warning

It's **not an error** — it's `grade` telling you ABA-406's grade hasn't been reviewed yet, so it's left out of the pass-rate math.

The flow:
1. After a drain run, drain-cycle auto-writes a grade file at `~/.drain-cycle/grades/ABA-406.md` with `status: draft` and unchecked KR checkboxes (`grade_draft.py:77`, `_render`).
2. `grade` reads every file in that dir. Only files with `status: confirmed` count toward the rate; anything else is a draft, gets the stderr warning, and is excluded (`grade.py:100-110`).
3. ABA-406's file currently reads:
   ```
   ---
   issue: ABA-406
   status: draft
   ---
   ```
   It was just generated today (run finished `2026-06-18T11:49`), so it hasn't been confirmed yet.

## How to clear it

Review the draft and promote it. Open `~/.drain-cycle/grades/ABA-406.md`, fill in the `## KR check` checkboxes, and change `status: draft` → `status: confirmed`. On the next `grade` run the warning disappears and ABA-406 counts toward the rate.

This is by design — the draft/confirmed split is the human-in-the-loop gate so an unreviewed run can't silently inflate (or deflate) your initiative pass-rate. It's the same mechanism the silent-Done violation check is built on (`grade.py` module docstring).

> DEVELOPER

i need to make the grading automated - also grading is a bad choice of words
i'm trying to figure out a way to automate how to measure the quality of each run - duration,cost,correctness

> AGENT

Let me understand what signals already exist per run before proposing a design.

> TOOL

tool_use Bash
id: toolu_01SJgPEqy1zgsUK2huy56TLj
```json
{
  "command": "cd /home/<USER>/src/drain-cycle; echo \"=== runlog.py ===\"; cat drain_cycle/runlog.py 2>/dev/null | head -120",
  "description": "Read runlog module"
}
```

> TOOL

tool_result
id: toolu_01SJgPEqy1zgsUK2huy56TLj
```
=== runlog.py ===
"""Per-cycle run-log artefact.

Each ``drain-cycle`` invocation produces a single JSON file at
``~/.drain-cycle/runs/<cycle-id>-<run-timestamp>.json`` capturing one
entry per attempted issue. The filename embeds the run-start timestamp
(UTC, ``%Y%m%dT%H%M%S%fZ``) so re-running ``drain-cycle`` against the
same cycle writes a new file instead of clobbering the prior one.
Downstream consumers glob the directory and group by ``cycle_id``
(carried inside each file).

* KR1 (completion %) is computed from ``entries[].final_linear_state``
  merged across every file sharing the same ``cycle_id``.
* Cycle-drain self-grading reads every file across cycles.
* The kill condition (KR1 < 50%) merges per-cycle then thresholds.

Schema:

::

    {
      "cycle_id":               "<linear-cycle-uuid>",
      "cycle_duration_seconds": <float>,
      "cycle_cost_usd":         <float>,
      "cycle_tokens_cumulative": <int>,
      "cycle_halt_reason":      null | "<cycle-budget halt line>",
      "entries":                [
        {
          "issue_identifier":   "ABA-NNN",
          "started_at":         "<iso-8601 UTC>",
          "finished_at":        "<iso-8601 UTC>",
          "exit_code":          <int>,
          "final_linear_state": "Done" | "Todo" | ...,
          "worktree_path":      "<absolute path>",
          "halt_reason":        null | "<orchestrator stderr halt line>",
          "duration_seconds":   <float>,
          "model":              null | "<resolved model id>",
          "usage":              null | {
            "input_tokens":               <int>,
            "output_tokens":              <int>,
            "cache_creation_input_tokens": <int>,
            "cache_read_input_tokens":    <int>,
            "cumulative":                 <int>,
            "peak_context":               <int>,
          },
          "cost_usd":           null | <float>,
          "num_turns":          null | <int>,
          "session_id":         null | "<uuid>",
          "is_error":           null | <bool>,
          "outcome_verdict":    null | {"result": "pass"|"fail", "findings": [...], "invoked_at": "<iso-8601>"},
          "prep_verdict":       null | {"result": "<str>", […]

> AGENT

The run log already gives you most of this. Let me check the metrics framing in the docs before I lay out a design.

> TOOL

tool_use Bash
id: toolu_01X81mrC6xsms5W4vgWHR2ds
```json
{
  "command": "cd /home/<USER>/src/drain-cycle; grep -rln \"outcome_verdict\\|correctness\\|pass-rate\\|pass_rate\\|quality\\|scorecard\\|KR1\\|KR2\" docs/ drain_cycle/ 2>/dev/null | head -30",
  "description": "Find quality/KR references"
}
```

> TOOL

tool_result
id: toolu_01X81mrC6xsms5W4vgWHR2ds
```
docs/images/architecture-overview.svg
docs/images/README.md
docs/architecture.html
docs/delivery-plans/exec-state-file-rename/D1-one-pack-owned-execution-state-file/N01-amend-thin-supervisor-contract.md
docs/delivery-plans/exec-state-file-rename/README.md
docs/spikes/live-execution-swimlanes-observability/recommendation.md
docs/integration-test-architecture.md
docs/prototypes/live-execution-swimlanes/__pycache__/demo.cpython-314.pyc
docs/prototypes/live-execution-swimlanes/demo.py
docs/integration-test-architecture.html
docs/adrs/0018-resume-on-rerun.md
docs/adrs/references/drain-handoff-schema-v2.md
docs/adrs/0008-run-log-per-invocation.md
docs/adrs/0019-watch-in-tmux-pane.md
docs/adrs/0002-thin-supervisor-contract.md
docs/adrs/0025-multi-altitude-review.md
docs/adrs/0028-keystone-cutover.md
docs/adrs/0005-agent-self-updates-linear.md
docs/ideas/drain-past-the-merge-gate.md
docs/ideas/live-execution-swimlanes.md
drain_cycle/grade_draft.py
drain_cycle/handoff.py
drain_cycle/__pycache__/orchestrator.cpython-312.pyc
drain_cycle/__pycache__/orchestrator.cpython-314.pyc
drain_cycle/__pycache__/prompt.cpython-314.pyc
drain_cycle/__pycache__/runlog.cpython-314.pyc
drain_cycle/__pycache__/prompt.cpython-312.pyc
drain_cycle/__pycache__/runlog.cpython-312.pyc
drain_cycle/__pycache__/grade.cpython-314.pyc
drain_cycle/__pycache__/grade.cpython-312.pyc
```

> AGENT

I dug into the schema. Here's the key realization before we name anything or build anything:

**You're already capturing all three signals per run.** Look at the run-log entry schema (`runlog.py`):

- **duration** → `duration_seconds` (auto-computed every persist)
- **cost** → `cost_usd` + `usage.cumulative` (tokens) — populated from the worker's stream-json
- **correctness** → `outcome_verdict: {result: "pass"|"fail", findings, invoked_at}` — written by the exec:verify outcome verifier

So duration and cost are *already* fully automatic. And correctness is already captured as a machine-readable verdict — `grade.py` even reads it today for the silent-Done check.

**The only thing that's manual is the part you'd delete.** `grade_draft.py` writes a file with `status: draft` and a `## KR check` list of empty checkboxes, and a human ticks the boxes and flips `status` to `confirmed`. "Automating grading" basically means: stop requiring that hand-confirmation and instead compute a per-run verdict directly from the run-log entry, which already has every field.

That reduces to **one real design decision: what do you trust as the automatic correctness signal?** Right now a human confirms precisely because `outcome_verdict` is the agent assessing its own work. To remove the human you have to pick what counts as "correct" without one. That's […]

> TOOL

tool_use AskUserQuestion
id: toolu_01DiUajYFxoaW56ySjE6MA28
```json
{
  "questions": [
    {
      "question": "What should count as the automatic 'correctness' signal for a run, now that no human confirms it?",
      "header": "Correctness",
      "multiSelect": false,
      "options": [
        {
          "label": "Composite of run-log verdicts",
          "description": "Correct = outcome_verdict pass AND review GO AND prep route present. All already in the run log, no external lookups. Multi-signal so one over-optimistic verifier can't pass it alone. Recommended.",
          "preview": "correct = (outcome_verdict.result == 'pass')\n         and (review verdict == 'GO')\n         and (prep_verdict.route in {auto-merge, human-review})\n\n# all fields already in the run-log entry\n# zero git/GitHub calls"
        },
        {
          "label": "Outcome verdict alone",
          "description": "Correct = outcome_verdict.result == 'pass'. Cheapest, zero new plumbing, but it's the agent grading its own homework.",
          "preview": "correct = outcome_verdict.result == 'pass'\n\n# already captured\n# weakness: self-assessment, no corroboration"
        },
        {
          "label": "Ground-truth merge status",
          "description": "Correct = the run's PR(s) actually merged into origin/main. Most objective, but lags (PRs merge later) and needs git/GitHub lookups via the recorded pr_urls.",
          "preview": "correct = all(pr merged into origin/main\n              for pr in entry.pr_urls)\n\n# objective ground truth\n# but: lags real-time, needs GitHub API\n# conflates 'correct' with 'merged'"
        }
      ]
    },
    {
      "question": "'Grading' is the wrong word. What should the […]

> TOOL

tool_result
id: toolu_01DiUajYFxoaW56ySjE6MA28
```
Your questions have been answered: "What should count as the automatic 'correctness' signal for a run, now that no human confirms it?"="Composite of run-log verdicts" selected preview:
correct = (outcome_verdict.result == 'pass')
         and (review verdict == 'GO')
         and (prep_verdict.route in {auto-merge, human-review})

# all fields already in the run-log entry
# zero git/GitHub calls, "'Grading' is the wrong word. What should the command and concept be called?"="scorecard" selected preview:
drain-cycle scorecard

ABA-406  pass  19m50s  $0.42  142k tok
ABA-405  pass   8m12s  $0.18   61k tok
...
cycle: 12/13 correct (92%). You can now continue with these answers in mind.
```

> AGENT

Good — composite correctness + `scorecard`. One thing I need to verify before designing: the composite references a **review GO** verdict, but the run-log schema only lists `outcome_verdict` and `prep_verdict`. Let me check whether the review verdict is actually persisted anywhere.

> TOOL

tool_use Bash
id: toolu_01KCzuBgEPTMA6P4cvL9GzRY
```json
{
  "command": "cd /home/<USER>/src/drain-cycle; echo \"=== run-log/exec-state writers ===\"; grep -rn \"outcome_verdict\\|prep_verdict\\|review_verdict\\|review_verdict\\|exec-state\\|exec_state\" drain_cycle/*.py | grep -iv \"def test\" | head -40",
  "description": "Find verdict writers in source"
}
```

> TOOL

tool_result
id: toolu_01KCzuBgEPTMA6P4cvL9GzRY
```
=== run-log/exec-state writers ===
drain_cycle/grade.py:10:   verifier never ran (``outcome_verdict == null`` in the run log).
drain_cycle/grade.py:15:verifier running. Only ``outcome_verdict == null`` counts — a verdict of any
drain_cycle/grade.py:73:    """True when the entry is Done in Linear but outcome_verdict was never set."""
drain_cycle/grade.py:76:        and entry.get("outcome_verdict") is None
drain_cycle/handoff.py:5:review-summary comment, and records the submitted PRs in ``exec-state.json``
drain_cycle/handoff.py:12:and the ``verify`` section, which it maps to its ``outcome_verdict`` for the
drain_cycle/handoff.py:15:``read`` reads the sectioned ``exec-state.json`` — the only state file. The
drain_cycle/handoff.py:19:``outcome_verdict`` is derived from the pack's ``verify`` section: a ``FAIL``
drain_cycle/handoff.py:22:halt paths can carry whatever the worker managed to write. ``prep_verdict`` has
drain_cycle/handoff.py:35:EXEC_STATE_FILE = "exec-state.json"
drain_cycle/handoff.py:47:    outcome_verdict: dict[str, Any] | None = None
drain_cycle/handoff.py:48:    prep_verdict: dict[str, Any] | None = None
drain_cycle/handoff.py:123:def _read_exec_state(path: Path) -> HandoffData | None:
drain_cycle/handoff.py:124:    """Parse the sectioned ``exec-state.json``, returning HandoffData or None.
drain_cycle/handoff.py:126:    ``pr_urls`` comes from the ``finish`` section; ``outcome_verdict`` from the
drain_cycle/handoff.py:140:        outcome_verdict=_verify_to_outcome(payload.get("verify")),
drain_cycle/handoff.py:141:        prep_verdict=None,
drain_cycle/handoff.py:148:    Reads the sectioned ``exec-state.json`` (the pack-named file). Returns
drain_cycle/handoff.py:151:    ``outcome_verdict`` and ``prep_verdict`` are optional: missing sections/keys
drain_cycle/handoff.py:154:    return _read_exec_state(worktree / EXEC_STATE_FILE)
drain_cycle/handoff.py:160:    """Return ``(outcome_verdict, prep_verdict)`` without the ``pr_urls`` gate.
drain_cycle/handoff.py:164:    Reads the ``verify`` section of ``exec-state.json`` for the outcome verdict;
drain_cycle/handoff.py:165:    there is no ``prep_verdict`` producer […]

> AGENT

Plan mode is on — I'll research and write a plan rather than edit. That last grep surfaced a critical gap: `handoff.py:165` says **"there is no prep_verdict producer in the exec:* workflow today,"** and there's no `review_verdict` field at all. So the composite you chose (outcome pass AND review GO AND prep route) references two signals that aren't fully plumbed yet. I need to map exactly what's produced vs. missing before planning.

Let me launch focused exploration in parallel.

> TOOL

tool_use Agent
id: toolu_0191rpnaDJMhtaZA6Lnu6ZUd
```json
{
  "description": "Map verdict production pipeline",
  "subagent_type": "Explore",
  "prompt": "I'm planning to automate a per-run \"scorecard\" in the drain-cycle repo (/home/<USER>/src/drain-cycle) that derives a correctness verdict from three signals already meant to be captured per run: the outcome verifier verdict, the multi-persona review GO/NO-GO verdict, and the PR-prep routing verdict.\n\nI need a precise map of WHERE each of these verdicts is produced and whether it actually gets persisted into the run-log / exec-state.json pipeline. Be thorough and quote file:line.\n\nSpecifically investigate:\n\n1. `drain_cycle/handoff.py` — full read. How does it parse exec-state.json? What sections exist (verify, finish, prep, review)? It maps the `verify` section to `outcome_verdict`. Does it produce a `prep_verdict`? Does it read any `review` section? Quote the relevant code.\n\n2. The exec-state.json schema/producers. Search for where exec-state.json is WRITTEN (not just read) — which skill or which part of the exec:* workflow writes the `verify` / `finish` / `prep` / `review` sections. Look in the skills under any `shape-exec-*` / `pr-prepare` / `pr-finishing` skill directories (search the repo and ~/.claude for skill markdown that writes exec-state.json sections). \n\n3. The exec:review skill (shape-exec-review / shape:exec:review) — does it emit a GO/NO-GO verdict to exec-state.json or anywhere machine-readable, or […]

> TOOL

tool_use Agent
id: toolu_01CNFze7bhNAjihWDWiKNrsx
```json
{
  "description": "Map grade command surface",
  "subagent_type": "Explore",
  "prompt": "In the drain-cycle repo (/home/<USER>/src/drain-cycle), I'm planning to (a) automate away a manual draft→confirmed gate and (b) rename the `grade` command/concept to `scorecard`. I need a complete map of the current \"grade\" surface so nothing is missed in the rename/rework.\n\nInvestigate and report with file:line:\n\n1. `drain_cycle/grade.py` — full read. What does `run()` do end to end? How does it consume confirmed vs draft files? What does it print? Exit codes?\n\n2. `drain_cycle/grade_draft.py` — full read. When/where is `write_draft_from_entry` and `run()` called from? Who triggers draft creation? What is the `## KR check` manual checkbox block and `status: draft` for?\n\n3. `drain_cycle/kr2_check.py` — full read. What does it check and where is it invoked?\n\n4. CLI wiring: find the argparse/click/typer dispatch (likely `drain_cycle/cli.py` or `__main__.py`). Where is the `grade` subcommand registered? Are `grade-draft` / `kr2-check` also subcommands? List every subcommand name and the function it dispatches to.\n\n5. Search the whole repo (docs/, tests/, README, AGENTS.md) for references to the word \"grade\"/\"grading\"/\"grade-draft\"/\"self-grading\" so I know everything that a rename to \"scorecard\" would touch. Distinguish code references from doc/prose references.\n\n6. Tests: which test files cover grade.py / grade_draft.py / kr2_check.py? List paths and […]

> TOOL

tool_result
id: toolu_0191rpnaDJMhtaZA6Lnu6ZUd
```
Perfect! Now I have all the information I need to provide a comprehensive report. Let me compile the findings:

## Report: Verdict Signals in drain-cycle

Based on thorough investigation of the codebase, here's the precise map of the three verdict signals:

### 1. **OUTCOME_VERDICT** (exec:verify verdict)

**Produced by:** `exec:verify` skill → writes to exec-state.json `verify` section  
**Structure in exec-state.json:**
```json
"verify": {
  "verdict": "PASS|FAIL",
  "ac_results": [
    {"item": "<AC text>", "result": "PASS|FAIL"},
    ...
  ]
}
```

**Persisted:** YES  
**Evidence:** `/home/<USER>/src/drain-cycle/tests/fixtures/exec-state.json:34-39`

**Read by orchestrator:** YES  
**Mapping code:** `/home/<USER>/src/drain-cycle/drain_cycle/handoff.py:95-120` (_verify_to_outcome)
- Maps `verify.verdict` to `outcome_verdict.result` ("pass" or "fail")
- Extracts failing AC items to `outcome_verdict.findings`

**Reaches run-log:** YES  
**Evidence:**
- `/home/<USER>/src/drain-cycle/drain_cycle/orchestrator.py:688` (read from handoff)
- `/home/<USER>/src/drain-cycle/drain_cycle/orchestrator.py:691-692` (fallback to handoff if M2+ didn't populate)
- `/home/<USER>/src/drain-cycle/drain_cycle/orchestrator.py:973-974` (appended to run-log entry)
- `/home/<USER>/src/drain-cycle/drain_cycle/runlog.py:49` (schema: `outcome_verdict: null | {"result": "pass"|"fail", "findings": [...], "invoked_at": "<iso-8601>"}`)

**Status:** COMPLETE — fully produced, persisted, and reaches run-log

---

### 2. **REVIEW_VERDICT** (exec:review GO/NO-GO verdict)

**Produced by:** `exec:review` skill → writes to exec-state.json `review` section  
**Structure in exec-state.json:**
```json
"review": {
  "verdict": "GO|NO-GO",
  "findings": [
    {"file": "...", "defect_class": "...", "severity": "..."},
    ...
  ]
}
```

**Persisted:** YES (in fixture)  
**Evidence:** `/home/<USER>/src/drain-cycle/tests/fixtures/exec-state.json:30-33`

**Read by orchestrator:** CURRENT STATUS IS […]

> TOOL

tool_result
id: toolu_01CNFze7bhNAjihWDWiKNrsx
```
Excellent! Now I have all the information. Let me compile the complete map:

## Complete Grade Surface Mapping

### 1. **drain_cycle/grade.py** — Full Analysis

**File:** `/home/<USER>/src/drain-cycle/drain_cycle/grade.py`

**Purpose:** Reads every grade file at `~/.drain-cycle/grades/*.md`, separates confirmed from draft, and reports health metrics including pass-rate and silent-Done violations (a core safety guarantee: Done entries with `outcome_verdict == null`).

**Key Functions:**

- `run(grades_dir: Path, runs_dir: Path) -> int` (lines 80-150): Main entry point
  - **End-to-end flow:**
    1. Glob `grades_dir/*.md` files and parse YAML frontmatter
    2. Extract `issue` field (fallback to filename stem) and `status` field (default: "draft")
    3. Separate into `confirmed` (status: "confirmed") and `drafts` (anything else)
    4. **Drafts handling:** Print stderr warning for each draft, exclude from count
    5. For each confirmed issue, call `_find_run_entry()` to load most-recent run-log entry
    6. Track `no_runlog` issues and `violations` (confirmed Done entries where `outcome_verdict == null`)
    7. **Output:** Prints to stdout:
       - `graded: {total}` (confirmed count only)
       - `pass-rate: {passes}/{denominator} ({pct}%)` or `pass-rate: n/a`
       - `silent-Done violations: none` or list by issue ID
    8. **Exit codes:** 0 (no violations) or 1 (violations found)

- `_parse_frontmatter(text: str) -> dict[str, str]` (lines 38-54): Parses YAML `---` blocks for simple `key: value` pairs

- […]

> AGENT

Thorough. There's one discrepancy to resolve and a few critical files to confirm myself. Let me read the actual source.

> TOOL

tool_use Read
id: toolu_01GrQPcZ445Z93fiy5tTpVYJ
```json
{
  "file_path": "/home/<USER>/src/drain-cycle/drain_cycle/handoff.py"
}
```

> TOOL

tool_result
id: toolu_01GrQPcZ445Z93fiy5tTpVYJ
```
1	"""Handoff artefact a stack-mode worker leaves behind after submitting PRs.
2	
3	In stack mode the worker drives PR submission itself via the ``pr-finishing``
4	skill, which runs ``gt``/``gh`` inside the worktree, posts the Linear
5	review-summary comment, and records the submitted PRs in ``exec-state.json``
6	(the pack-named file). The pack writes that file as a set of phase-keyed
7	sections — ``pickup``, ``breakdown``, ``build``, ``review``, ``verify``,
8	``finish`` — each skill owning its own section (ADR 0030). The orchestrator
9	reads two of those sections back: ``finish.pr_urls`` as its submission-confirmation
10	signal — a present, non-empty list means the skill submitted at least one PR;
11	its absence means submission never completed and the per-repo chain must halt —
12	and the ``verify`` section, which it maps to its ``outcome_verdict`` for the
13	run-log and the verifier-fail gate.
14	
15	``read`` reads the sectioned ``exec-state.json`` — the only state file. The
16	legacy flat ``.drain-handoff.json`` has been dropped. A missing or structurally
17	invalid file returns ``None``.
18	
19	``outcome_verdict`` is derived from the pack's ``verify`` section: a ``FAIL``
20	verdict maps to ``result == "fail"`` with the failed AC items as ``findings``.
21 […]

> TOOL

tool_use Read
id: toolu_01PYjVPTLjGpACkavy2bVBNz
```json
{
  "file_path": "/home/<USER>/src/drain-cycle/tests/fixtures/exec-state.json"
}
```

> TOOL

tool_result
id: toolu_01PYjVPTLjGpACkavy2bVBNz
```
1	{
2	  "pickup": {
3	    "issue_id": "ABA-000",
4	    "branch": "ABA-000",
5	    "parent_branch": "main",
6	    "worktree_path": "/tmp/worktrees/ABA-000",
7	    "ac_checklist": [
8	      "The feature does X when Y.",
9	      "The skill writes exec-state.json with a finish.pr_urls section."
10	    ],
11	    "body_md": "Example issue body for fixture use.",
12	    "labels": ["sonnet", "agent-skills-shaper"],
13	    "blocked_by": []
14	  },
15	  "breakdown": {
16	    "tasks": [
17	      {
18	        "id": "t1",
19	        "title": "Update pr-finishing skill",
20	        "done_when": "SKILL.md step 7 writes exec-state.json finish section with pr_urls.",
21	        "model_tier": "sonnet",
22	        "axes": { "RC": 1, "SC": 0, "HS": 0, "SR": 1, "OR": 0 }
23	      }
24	    ]
25	  },
26	  "build": {
27	    "completed_tasks": ["t1"],
28	    "commits": ["abc1234"]
29	  },
30	  "review": {
31	    "verdict": "GO",
32	    "findings": []
33	  },
34	  "verify": {
35	    "verdict": "PASS",
36	    "ac_results": [
37	      { "item": "The feature does X when Y.", "result": "PASS" },
38	      { "item": "The skill writes exec-state.json with a finish.pr_urls section.", "result": "PASS" }
39	    ]
40	  },
41	  "finish": {
42	    "pr_urls": [
43	      { "title": "feat: update pr-finishing to dual-write exec-state.json", "url": "https://github.com/example/repo/pull/1" }
44	    ]
45	  }
46	}
47	
```

> AGENT

Let me confirm the current pass-rate semantics and the orchestrator's draft-write hook — these determine how much I can delete.

> TOOL

tool_use Read
id: toolu_01P6Su9sf8fCaXsx2R3F4REs
```json
{
  "file_path": "/home/<USER>/src/drain-cycle/drain_cycle/grade.py",
  "offset": 129,
  "limit": 40
}
```

> TOOL

tool_result
id: toolu_01P6Su9sf8fCaXsx2R3F4REs
```
129	        )
130	
131	    passes = total - len(violations) - len(no_runlog)
132	    pass_rate_denom = total - len(no_runlog)
133	
134	    if pass_rate_denom > 0:
135	        pct = round(passes * 100 / pass_rate_denom)
136	        pass_rate_str = f"{passes}/{pass_rate_denom} ({pct}%)"
137	    else:
138	        pass_rate_str = "n/a"
139	
140	    print(f"graded: {total}")
141	    print(f"pass-rate: {pass_rate_str}")
142	
143	    if violations:
144	        print("silent-Done violations:")
145	        for issue in violations:
146	            print(f"  {issue}")
147	    else:
148	        print("silent-Done violations: none")
149	
150	    return 1 if violations else 0
151	
```

> TOOL

tool_use Read
id: toolu_01KqHBjvsissrjedZ1A7CfCE
```json
{
  "file_path": "/home/<USER>/src/drain-cycle/drain_cycle/orchestrator.py",
  "offset": 960,
  "limit": 35
}
```

> TOOL

tool_result
id: toolu_01KqHBjvsissrjedZ1A7CfCE
```
960	            except RuntimeError as exc:
961	                remove_error = str(exc)
962	                issue_span.set_attribute("worktree.remove_error", remove_error)
963	                console.orch(f"{identifier}: worktree teardown failed: {exc}")
964	            # Append unconditionally for every attempted issue.
965	            log.append_entry(
966	                issue_identifier=identifier,
967	                started_at=started_at,
968	                finished_at=finished_at,
969	                exit_code=result.exit_code,
970	                final_linear_state=post_spawn_state,
971	                worktree_path=str(worktree_path),
972	                halt_reason=remove_error,
973	                outcome_verdict=outcome.outcome_verdict,
974	                prep_verdict=outcome.prep_verdict,
975	                responder_runs=outcome.responder_runs,
976	                finishing_runs=finishing_runs,
977	                **_worker_log_fields(outcome.result),
978	            )
979	            _set_verdict_span_attrs(issue_span, outcome)
980	            try:
981	                draft_path = grade_draft.write_draft_from_entry(
982	                    identifier, log.entries[-1]
983	                )
984	                console.worker_event(identifier, f"grade draft → {draft_path}")
985	            except Exception as exc:
986	                console.orch(
987	                    f"{identifier}: grade-draft write failed (non-fatal): {exc}"
988	                )
989	            if remove_error is None:
990	                console.worker_event(identifier, "done; worktree removed")
991	            return None, pane_id
992	
993	        # Not-Done halt: revert to the pre-halt state so a re-run picks
994	        # this issue back up instead of silently skipping it.
```

> AGENT

I now have the full picture. Two findings that shape the plan:

1. **Today's "pass-rate" doesn't actually check correctness.** `grade.py:131` counts a run as a "pass" if it's confirmed, has a run-log entry, and isn't silent-Done — it never reads `outcome_verdict.result`. So a **FAIL** verdict counts as a pass today. The composite you picked fixes that.

2. **The three signals have very different readiness:**
   - `outcome_verdict` (pass/fail) — ✅ fully flows to the run log today.
   - `review` GO/NO-GO — ⚠️ exec:review **already writes** it to `exec-state.json` (I confirmed the `review` section in the fixture), but `handoff.py` never reads it, so it never reaches the run log. In-repo plumbing only.
   - `prep_verdict.route` — ❌ **no producer exists anywhere.** Wiring it up means changing the `pr-prepare` skill in a *separate* repo (`agent-skills-shaper`) to write a `prep` section. If the scorecard hard-requires "route present," every run fails correctness until that cross-repo change lands.

That last point is a real scoping fork for the plan:

> TOOL

tool_use AskUserQuestion
id: toolu_01MxpMA3H1QKd2qaWMm6CPYw
```json
{
  "questions": [
    {
      "question": "The prep-route signal has no producer yet (needs a skill change in the separate agent-skills-shaper repo). How should the scorecard treat signals that aren't produced yet, and what's in scope for this plan?",
      "header": "Scope",
      "multiSelect": false,
      "options": [
        {
          "label": "Phase it — in-repo now",
          "description": "Build the composite engine reading all three signals, wire review GO→run-log (in-repo), gate correctness on outcome AND review. Treat prep-route as advisory (shown but not blocking) until its producer exists. Keeps this a single-repo change. Recommended.",
          "preview": "correct = outcome pass AND review GO\nprep route: shown as advisory column\n              (not yet blocking)\n\nscope: drain-cycle repo only\n  - read review section in handoff.py\n  - add review_verdict to run log\n  - new scorecard command\n  - delete draft/confirmed flow"
        },
        {
          "label": "Full composite now",
          "description": "Also change the pr-prepare skill in agent-skills-shaper to emit prep_verdict, read all three, gate on all three. Cross-repo, bigger, but the full gate is live immediately.",
          "preview": "correct = outcome pass\n        AND review GO\n        AND prep route present\n\nscope: drain-cycle + agent-skills-shaper\n  - pr-prepare writes prep section\n  - handoff reads review + prep\n  - all three gate correctness"
        },
        {
          "label": "Outcome-only […]

> TOOL

tool_result
id: toolu_01MxpMA3H1QKd2qaWMm6CPYw
```
Your questions have been answered: "The prep-route signal has no producer yet (needs a skill change in the separate agent-skills-shaper repo). How should the scorecard treat signals that aren't produced yet, and what's in scope for this plan?"="Phase it — in-repo now" selected preview:
correct = outcome pass AND review GO
prep route: shown as advisory column
              (not yet blocking)

scope: drain-cycle repo only
  - read review section in handoff.py
  - add review_verdict to run log
  - new scorecard command
  - delete draft/confirmed flow. You can now continue with these answers in mind.
```

> AGENT

Decision captured: **outcome pass AND review GO**, prep advisory, drain-cycle repo only. I have everything I need — I've read all the critical source directly. Writing the plan.

> TOOL

tool_use Write
id: toolu_01NBpvurcUrrqKYeWVnZFKJz
```json
{
  "file_path": "/home/<USER>/.claude/plans/composed-watching-cerf.md",
  "content": "# Automate run-quality measurement: replace manual \"grade\" with `scorecard`\n\n## Context\n\nToday, measuring the quality of a drain-cycle run is half-manual and the wrong\nshape:\n\n- After each issue completes, the orchestrator auto-writes a markdown draft to\n  `~/.drain-cycle/grades/<issue>.md` with `status: draft` and an empty\n  `## KR check` checkbox list (`grade_draft.py`).\n- A human must tick the boxes and flip `status: draft` → `status: confirmed`.\n- `drain-cycle grade` only counts `confirmed` files, warns on drafts\n  (`warning: ABA-406 is a draft — excluded from rate`), and reports a\n  \"pass-rate\".\n\nTwo problems:\n\n1. **It isn't automated.** The draft/confirmed step is manual, so the warning\n   the user hit is just \"you haven't hand-confirmed ABA-406 yet.\"\n2. **The \"pass-rate\" doesn't measure correctness.** `grade.py:131` counts a run\n   as a pass if it's confirmed, has a run-log entry, and isn't silent-Done — it\n   never reads `outcome_verdict.result`. A **FAIL** verdict counts as a pass.\n\nWe want each run measured automatically on three dimensions —\n**duration, cost, correctness** — with no human gate. Duration and cost are\nalready captured per run-log entry (`duration_seconds`, `cost_usd`,\n`usage.cumulative`). Correctness should be derived from verdicts already (mostly)\ncaptured. \"Grade\" is also the wrong word; the concept is renamed **scorecard**.\n\n**Decided scope (phased, in-repo only):**\n- Correctness = `outcome_verdict.result == \"pass\"` […]

> TOOL

tool_result
id: toolu_01NBpvurcUrrqKYeWVnZFKJz
```
File created successfully at: /home/<USER>/.claude/plans/composed-watching-cerf.md (file state is current in your context — no need to Read it back)
```

> AGENT

The plan is written. Here's the shape of it:

**The core insight:** you're already capturing duration and cost per run, and `outcome_verdict` correctness already flows to the run log. The only manual thing is the markdown draft→confirmed gate — that's what the warning was about, and it's what we delete. Today's "pass-rate" doesn't even read the verdict result (a FAIL counts as a pass); the new scorecard fixes that.

**What the plan does:**
1. Wires the **review GO/NO-GO** verdict (already written to `exec-state.json` by exec:review, just never read) through the same path `outcome_verdict` takes → run log.
2. New `drain-cycle scorecard` command reads run-log JSON directly: per-run duration / cost / tokens / correctness, with a per-cycle and overall correctness rate. Correctness = `outcome pass AND review GO`; prep-route shown as advisory.
3. Deletes the whole manual flow — `grade_draft.py`, the orchestrator auto-draft write, `~/.drain-cycle/grades/`, the `grade-draft` subcommand.
4. Preserves the one hard guarantee: silent-Done (Done with null verdict) still exits nonzero.

**Deferred:** `prep_verdict.route` gating, since its producer needs a cross-repo skill change in `agent-skills-shaper`.

> TOOL

tool_use ToolSearch
id: toolu_016puzZ4zgxQWFqMNe2ixtSC
```json
{
  "query": "select:ExitPlanMode",
  "max_results": 1
}
```

> TOOL

tool_result
id: toolu_016puzZ4zgxQWFqMNe2ixtSC
```
{
  "type": "tool_reference",
  "tool_name": "ExitPlanMode"
}
```

> TOOL

tool_use ExitPlanMode
id: toolu_011HjfQ3NKCPiuLeRncSM9iB
```json
{
  "allowedPrompts": [
    {
      "tool": "Bash",
      "prompt": "run the python test suite (uv run pytest)"
    },
    {
      "tool": "Bash",
      "prompt": "run drain-cycle CLI commands to verify scorecard output"
    }
  ],
  "plan": "# Automate run-quality measurement: replace manual \"grade\" with `scorecard`\n\n## Context\n\nToday, measuring the quality of a drain-cycle run is half-manual and the wrong\nshape:\n\n- After each issue completes, the orchestrator auto-writes a markdown draft to\n  `~/.drain-cycle/grades/<issue>.md` with `status: draft` and an empty\n  `## KR check` checkbox list (`grade_draft.py`).\n- A human must tick the boxes and flip `status: draft` → `status: confirmed`.\n- `drain-cycle grade` only counts `confirmed` files, warns on drafts\n  (`warning: ABA-406 is a draft — excluded from rate`), and reports a\n  \"pass-rate\".\n\nTwo problems:\n\n1. **It isn't automated.** The draft/confirmed step is manual, so the warning\n   the user hit is just \"you haven't hand-confirmed ABA-406 yet.\"\n2. **The \"pass-rate\" doesn't measure correctness.** `grade.py:131` counts a run\n   as a pass if it's confirmed, has a run-log entry, and isn't silent-Done — it\n   never reads `outcome_verdict.result`. A **FAIL** verdict counts as a pass.\n\nWe want each run measured automatically on three dimensions —\n**duration, cost, correctness** — with no human gate. Duration and cost are\nalready captured per run-log entry (`duration_seconds`, `cost_usd`,\n`usage.cumulative`). Correctness […]

> TOOL

tool_result ERROR
id: toolu_011HjfQ3NKCPiuLeRncSM9iB
```
Plan review feedback — revise the plan to address the review comments. Comments are in /home/<USER>/.crit/plans/automate-run-quality-measurement-replace-manual-grade-with-scorecard-2026-06-18/.crit/review.json — grouped per file with start_line/end_line referencing the source. Each comment has a scope field: "line" for inline comments, "file" for file-level, or "review" for review-level comments. Read the file, revise the plan to address each comment. If you are running under Codex, re-emit the revised plan inside <proposed_plan>...</proposed_plan> so Crit can review the new version. To reply to comments, use `crit comment --plan automate-run-quality-measurement-replace-manual-grade-with-scorecard-2026-06-18 --reply-to <id> --author <your-name> "<explanation>"`.
```

> TOOL

tool_use Read
id: toolu_01LdBi16KzZmkbtohmYqL25D
```json
{
  "file_path": "/home/<USER>/.crit/plans/automate-run-quality-measurement-replace-manual-grade-with-scorecard-2026-06-18/.crit/review.json"
}
```

> TOOL

tool_result
id: toolu_01LdBi16KzZmkbtohmYqL25D
```
1	{
2	  "branch": "ABA-409-live-execution-swimlanes",
3	  "base_ref": "03e19af351f7b6223ad08ea5b2709aac27b78305",
4	  "updated_at": "2026-06-18T12:17:42Z",
5	  "review_round": 1,
6	  "review_comments": [
7	    {
8	      "id": "r_18e925",
9	      "start_line": 0,
10	      "end_line": 0,
11	      "body": "this plan should be about creating a delivery plan in linear (project or just issues depending on how many tasks there are)",
12	      "author": "Anton Babushkin",
13	      "user_id": "4684d894-240a-4567-8e2d-ee5b222c7158",
14	      "scope": "review",
15	      "created_at": "2026-06-18T12:17:41Z",
16	      "updated_at": "2026-06-18T12:17:41Z",
17	      "review_round": 1
18	    }
19	  ],
20	  "cli_args": [
21	    "/home/<USER>/.crit/plans/automate-run-quality-measurement-replace-manual-grade-with-scorecard-2026-06-18/current.md"
22	  ],
23	  "files": {}
24	}
```

> AGENT

The reviewer wants this shaped as a **Linear delivery plan** (project or issues), not an implementation plan I execute myself. That fits this repo's ticket-driven approach. Let me check the existing correctness project in Linear to mirror its conventions before I rewrite the plan.

> TOOL

tool_use ToolSearch
id: toolu_01U76GvkeBjfxyXrqNLVxe2j
```json
{
  "query": "select:mcp__claude_ai_Linear__list_projects,mcp__claude_ai_Linear__list_issues,mcp__claude_ai_Linear__get_project",
  "max_results": 3
}
```

> TOOL

tool_result
id: toolu_01U76GvkeBjfxyXrqNLVxe2j
```
{
  "type": "tool_reference",
  "tool_name": "mcp__claude_ai_Linear__list_projects"
}
{
  "type": "tool_reference",
  "tool_name": "mcp__claude_ai_Linear__list_issues"
}
{
  "type": "tool_reference",
  "tool_name": "mcp__claude_ai_Linear__get_project"
}
```

> TOOL

tool_use mcp__claude_ai_Linear__list_projects
id: toolu_01MqL1H7tDhFFSreZtacZSUJ
```json
{
  "query": "correctness collaboration",
  "includeMilestones": true,
  "limit": 10
}
```

> TOOL

tool_result
id: toolu_01MqL1H7tDhFFSreZtacZSUJ
```
{"projects":[],"hasNextPage":false}
```

> TOOL

tool_use mcp__claude_ai_Linear__list_projects
id: toolu_017xMxuVcPwCJ7ikgGAVq1LK
```json
{
  "includeMilestones": true,
  "limit": 30
}
```

> TOOL

tool_result
id: toolu_017xMxuVcPwCJ7ikgGAVq1LK
```
<persisted-output>
Output too large (54.3KB). Full output saved to: /home/<USER>/.claude/projects/-Users-anton-src-drain-cycle/6d19145b-86d2-4b0d-9077-624706537065/tool-results/REDACTED.json

Preview (first 2KB):
[
  {
    "type": "text",
    "text": "{\"projects\":[{\"id\":\"b1835e7e-4034-4f3f-921f-3bf3554531e2\",\"icon\":null,\"color\":\"#bec2c8\",\"name\":\"Watch pane: Claude-Code-style rendering\",\"summary\":\"drain-cycle -w pane renders worker sessions as a Claude-Code-style transcript — display-side only, zero observability impact. One 5-PR Graphite stack.\",\"description\":\"**Goal:** An operator watching `drain-cycle -w` reads each worker session as a Claude-Code-style transcript instead of raw stream-json or terse `===` headers — with zero impact on parse fidelity, usage accounting, or run logs.\\n\\n+++ **Delivery plan**: `drain-cycle docs/delivery-plans/watch-pane-rich-rendering/`\\n\\n+++\",\"url\":\"https://linear.app/ababushkin/project/watch-pane-claude-code-style-rendering-80c86f79c7ee\",\"createdAt\":\"2026-06-11T07:31:14.247Z\",\"updatedAt\":\"2026-06-11T14:01:01.187Z\",\"startedAt\":\"2026-06-11T12:02:36.226Z\",\"completedAt\":\"2026-06-11T14:01:01.187Z\",\"canceledAt\":null,\"startDate\":\"2026-06-11\",\"startDateResolution\":null,\"targetDate\":null,\"targetDateResolution\":null,\"priority\":{\"value\":0,\"name\":\"No priority\"},\"labels\":[],\"initiatives\":[],\"lead\":{\"id\":\"720d0535-dfc6-465f-8111-d1a3e6eab786\",\"name\":\"Anton Babushkin\"},\"status\":{\"id\":\"8703bdf7-c7c4-4c03-bb77-90f6d4163c6b\",\"name\":\"Completed\",\"type\":\"completed\"},\"teams\":[{\"id\":\"c20f56da-f121-4653-bf6c-dc1c8aac21c1\",\"name\":\"Personal\",\"key\":\"ABA\"}],\"milestones\":[]},{\"id\":\"b313da89-8ac3-43fb-ad5b-e9f76a6050f2\",\"icon\":null,\"color\":\"#bec2c8\",\"name\":\"drain-cycle supervises; the pack owns the workflow\",\"summary\":\"Merged into \\\"Multi-agent collaboration for correctness\\\" — issues N01–N05 (ABA-370–374) moved there. Closed to keep one owner for the run-log verdict schema.\",\"description\":\"> **Merged 2026-06-15 into [Multi-agent collaboration for correctness](<https://linear.app/ababushkin/project/multi-agent-collaboration-for-correct
...
</persisted-output>
```

> TOOL

tool_use Bash
id: toolu_01VFhPbBgpjycPjx3U38Lsr3
```json
{
  "command": "cd /home/<USER>/.claude/projects/-Users-anton-src-drain-cycle/6d19145b-86d2-4b0d-9077-624706537065/tool-results/; python3 -c \"\nimport json\ndata=json.load(open('REDACTED.json'))\nprojs=json.loads(data[0]['text'])['projects']\nfor p in projs:\n    print(p['status']['name'].ljust(11), p['id'], p['name'])\n    for m in p.get('milestones',[]):\n        print('      milestone:', m.get('name'))\n\"",
  "description": "List projects with status and milestones"
}
```

> TOOL

tool_result
id: toolu_01VFhPbBgpjycPjx3U38Lsr3
```
Completed   b1835e7e-4034-4f3f-921f-3bf3554531e2 Watch pane: Claude-Code-style rendering
Canceled    b313da89-8ac3-43fb-ad5b-e9f76a6050f2 drain-cycle supervises; the pack owns the workflow
      milestone: D1 — Supervisor sheds workflow prose
      milestone: D2 — Every drain inspectable
      milestone: D3 — Full cycle drains on the pointer prompt
Completed   962be170-d2f2-4b4e-99e5-19f01140c3b4 Consolidate Shaper’s Lifecycle into Four Phase Skills
      milestone: D1 : Architecture
      milestone: D2: Verification
      milestone: D3: Final Polish
Completed   f9399232-74f6-45fe-977c-dde359f2c035 Issues drain end-to-end on first-party skills
      milestone: D1 — Review gate proven on seeded defects
      milestone: D2 — Execution workflow drains issues end-to-end
      milestone: D3 — Cutover off third-party packs
Completed   97265a3e-9dd7-4719-91ad-420cca11c3b3 Fold execution-breakdown into delivery-shape
Backlog     f630d813-2f10-4691-baac-64858ef1e2b3 Knowledge Retrieval for Agent Cognitive Augmentation
      milestone: D1 — Walking Skeleton
      milestone: D2 — Full Corpus Ingest
      milestone: D3 — Reliability Layer
      milestone: D4 — Incremental Ingest Operability
Canceled    0d5d19a0-2683-4b3e-8681-754c5d24f6aa Idea-to-ticket shaping — any idea, right-sized, review-ready
Canceled    bc9ad068-270a-4f29-82e2-ffb8c8d2dc99 Verify-flow agent skills
Completed   812bc9b5-1618-48b8-8041-6d6223dc6d4c Multi-agent collaboration for correctness
      milestone: 1 - Record the pack's verdicts in the run log
      milestone: 2 - Gate Done on the outcome verdict
      milestone: 3 - Thin the supervisor (pointer-only prompt)
      milestone: 4 - Grade the outcome
Backlog     21b16b54-4f87-46e0-8566-257a17c402e8 Test drain-cycle failure modes and resume without a real Linear cycle
      milestone: M1 — […]

> AGENT

The "Multi-agent collaboration for correctness" project (which had a **"4 — Grade the outcome"** milestone) is already Completed — so this scorecard work is a fresh effort. My breakdown is ~5 dependent slices (stacked-PR friendly):

1. Plumb the `review` verdict into the run log (foundation)
2. New `scorecard` module + composite correctness logic (rename grade→scorecard)
3. CLI rename + usage/help
4. Delete the manual draft/confirmed flow + update `kr2_check`
5. ADR + doc touch-ups

That's right at your project-vs-issues boundary. You raised it, so let me get your call:

> TOOL

tool_use AskUserQuestion
id: toolu_01RDR8gshFf8ztTb2TydGjJa
```json
{
  "questions": [
    {
      "question": "How should the scorecard work be structured in Linear? (~5 dependent, stacked-PR-friendly slices.)",
      "header": "Linear shape",
      "multiSelect": false,
      "options": [
        {
          "label": "Standalone stacked issues",
          "description": "~5 standalone ABA issues, ordered/blocking like the exec-state rename (ABA-398–401). No new project. Lighter; fits a focused in-repo refactor. Recommended.",
          "preview": "ABA-AAA  Plumb review verdict → run log\nABA-BBB  scorecard module + correctness   (blocked by AAA)\nABA-CCC  CLI rename grade→scorecard       (blocked by BBB)\nABA-DDD  Delete draft/confirmed + kr2_check (blocked by BBB)\nABA-EEE  ADR + doc touch-ups\n\nno project; issues blocked-by ordered"
        },
        {
          "label": "New project + milestone",
          "description": "A new Linear project 'Automated run scorecard' with one milestone and the 5 issues, plus a delivery-plan doc under docs/delivery-plans/. Heavier; matches the watch-pane project precedent.",
          "preview": "Project: Automated run scorecard\n  Milestone D1 — scorecard replaces manual grade\n    ABA-AAA … ABA-EEE (5 issues)\n  + docs/delivery-plans/scorecard/README.md"
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01RDR8gshFf8ztTb2TydGjJa
```
Your questions have been answered: "How should the scorecard work be structured in Linear? (~5 dependent, stacked-PR-friendly slices.)"="New project + milestone" selected preview:
Project: Automated run scorecard
  Milestone D1 — scorecard replaces manual grade
    ABA-AAA … ABA-EEE (5 issues)
  + docs/delivery-plans/scorecard/README.md. You can now continue with these answers in mind.
```

> AGENT

New project + milestone it is. Rewriting the plan as a Linear delivery plan.

> TOOL

tool_use Write
id: toolu_0192xwdgNrt2xDH11mqCJNpW
```json
{
  "file_path": "/home/<USER>/.claude/plans/composed-watching-cerf.md",
  "content": "# Delivery plan: Automated run scorecard (replace manual \"grade\")\n\n## Context\n\nMeasuring the quality of a drain-cycle run is currently half-manual and the wrong\nshape. After each issue the orchestrator writes a markdown draft to\n`~/.drain-cycle/grades/<issue>.md` with `status: draft` and an empty `## KR check`\nchecklist; a human must tick the boxes and flip `status` to `confirmed` before\n`drain-cycle grade` counts it. That manual gate is why the user hits\n`warning: ABA-406 is a draft — excluded from rate`. Worse, the reported\n\"pass-rate\" never reads `outcome_verdict.result` (`grade.py:131`), so a **FAIL**\nverdict counts as a pass.\n\nWe want each run measured **automatically** on duration, cost, and correctness,\nwith no human gate, and the concept renamed from \"grade\" to **scorecard**.\nDuration and cost are already in every run-log entry (`duration_seconds`,\n`cost_usd`, `usage.cumulative`). Correctness will be derived from verdicts already\n(mostly) captured.\n\n**Decided scope (phased, in-repo only):** correctness = `outcome_verdict.result\n== \"pass\"` AND `review_verdict == \"GO\"`. `prep_verdict.route` is shown as an\nadvisory column but does **not** gate correctness (no producer yet — would need a\ncross-repo change to the `pr-prepare` skill in `agent-skills-shaper`). The manual\nmarkdown draft/confirmed flow is deleted; the scorecard reads run-log JSON\ndirectly.\n\nThis plan **creates the Linear delivery plan** for that work — a project, one\nmilestone, five ordered issues, and a […]

> TOOL

tool_result
id: toolu_0192xwdgNrt2xDH11mqCJNpW
```
The file /home/<USER>/.claude/plans/composed-watching-cerf.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

The plan is now a Linear delivery plan: a new **"Automated run scorecard"** project, one milestone (**D1 — scorecard replaces manual grade**), and five ordered, stacked-PR-friendly issues (I1 plumb review verdict → I2 scorecard module → I3 CLI rename, I4 delete draft flow → I5 ADR/docs), each with an AC checklist, model-tier label, and `blocked_by` ordering. On approval I'll create the project, milestone, and issues in Linear.

> TOOL

tool_use ExitPlanMode
id: toolu_01C3148zZcWrhrVQX9iXLXuH
```json
{
  "allowedPrompts": [],
  "plan": "# Delivery plan: Automated run scorecard (replace manual \"grade\")\n\n## Context\n\nMeasuring the quality of a drain-cycle run is currently half-manual and the wrong\nshape. After each issue the orchestrator writes a markdown draft to\n`~/.drain-cycle/grades/<issue>.md` with `status: draft` and an empty `## KR check`\nchecklist; a human must tick the boxes and flip `status` to `confirmed` before\n`drain-cycle grade` counts it. That manual gate is why the user hits\n`warning: ABA-406 is a draft — excluded from rate`. Worse, the reported\n\"pass-rate\" never reads `outcome_verdict.result` (`grade.py:131`), so a **FAIL**\nverdict counts as a pass.\n\nWe want each run measured **automatically** on duration, cost, and correctness,\nwith no human gate, and the concept renamed from \"grade\" to **scorecard**.\nDuration and cost are already in every run-log entry (`duration_seconds`,\n`cost_usd`, `usage.cumulative`). Correctness will be derived from verdicts already\n(mostly) captured.\n\n**Decided scope (phased, in-repo only):** correctness = `outcome_verdict.result\n== \"pass\"` AND `review_verdict == \"GO\"`. `prep_verdict.route` is shown as an\nadvisory column but does **not** gate correctness (no producer yet — would need a\ncross-repo change to the `pr-prepare` skill in `agent-skills-shaper`). The manual\nmarkdown draft/confirmed flow is deleted; the scorecard reads run-log JSON\ndirectly.\n\nThis plan **creates the Linear delivery plan** for that work — a project, one\nmilestone, five ordered issues, and a […]

> TOOL

tool_result ERROR
id: toolu_01C3148zZcWrhrVQX9iXLXuH
```
Plan review feedback — revise the plan to address the review comments. Comments are in /home/<USER>/.crit/plans/automate-run-quality-measurement-replace-manual-grade-with-scorecard-2026-06-18/.crit/review.json — grouped per file with start_line/end_line referencing the source. Each comment has a scope field: "line" for inline comments, "file" for file-level, or "review" for review-level comments. Read the file, revise the plan to address each comment. If you are running under Codex, re-emit the revised plan inside <proposed_plan>...</proposed_plan> so Crit can review the new version. To reply to comments, use `crit comment --plan automate-run-quality-measurement-replace-manual-grade-with-scorecard-2026-06-18 --reply-to <id> --author <your-name> "<explanation>"`.
```

> TOOL

tool_use Bash
id: toolu_01FwqLyvM93tMDTS72v3ZX5x
```json
{
  "command": "cd /home/<USER>/.crit/plans/automate-run-quality-measurement-replace-manual-grade-with-scorecard-2026-06-18/.crit/; python3 -c \"\nimport json\nd=json.load(open('review.json'))\nprint('round', d.get('review_round'))\nfor c in d['review_comments']:\n    print('---', c['id'], 'scope=', c['scope'], 'lines', c['start_line'],'-',c['end_line'])\n    print(c['body'])\n\"",
  "description": "Read latest review comments"
}
```

> TOOL

tool_result
id: toolu_01FwqLyvM93tMDTS72v3ZX5x
```
round 2
--- r_18e925 scope= review lines 0 - 0
this plan should be about creating a delivery plan in linear (project or just issues depending on how many tasks there are)
--- r_d9b3de scope= review lines 0 - 0
use /shape:delivery to check if you've followed all the right conventions
Shell cwd was reset to /home/<USER>/src/drain-cycle
```

> AGENT

The reviewer wants me to run `shape:delivery` to validate against the repo's delivery-plan conventions. Let me invoke it.

> TOOL

tool_use Skill
id: toolu_0157GkDGDFPMDW2F1LNrXbmj
```json
{
  "skill": "shape:delivery",
  "args": "Automated run scorecard — replace the manual \"grade\" draft/confirmed flow with an automatic per-run scorecard measuring duration, cost, and correctness (correctness = outcome_verdict pass AND review GO; prep-route advisory). In-repo (drain-cycle) only. Plan draft at /home/<USER>/.claude/plans/composed-watching-cerf.md"
}
```

> TOOL

tool_result ERROR
id: toolu_0157GkDGDFPMDW2F1LNrXbmj
```
<tool_use_error>Unknown skill: shape:delivery</tool_use_error>
```

> TOOL

tool_use Skill
id: toolu_01DN5dWVwZta2XvzhbZvYYvU
```json
{
  "skill": "shape-delivery",
  "args": "Automated run scorecard — replace the manual \"grade\" draft/confirmed flow with an automatic per-run scorecard measuring duration, cost, and correctness (correctness = outcome_verdict pass AND review GO; prep-route advisory). In-repo (drain-cycle) only. Plan draft at /home/<USER>/.claude/plans/composed-watching-cerf.md"
}
```

> TOOL

tool_result
id: toolu_01DN5dWVwZta2XvzhbZvYYvU
```
Launching skill: shape-delivery
```

> AGENT

I need the delivery-shape conventions to restructure the plan correctly. Let me read the contract, the model-routing rubric, and an existing in-repo delivery plan as a reference.

> TOOL

tool_use Bash
id: toolu_01KfsrBT5MAGB2Bn7TPsGkgi
```json
{
  "command": "cd /home/<USER>/.claude/skills/shape-delivery; echo \"=== contract ===\"; cat docs/delivery-shape-contract.md 2>/dev/null; echo; echo \"=== task-sizing ===\"; cat references/task-sizing.md 2>/dev/null",
  "description": "Read delivery contract and sizing rubric"
}
```

> TOOL

tool_result ERROR
id: toolu_01KfsrBT5MAGB2Bn7TPsGkgi
```
Exit code 1
=== contract ===

=== task-sizing ===
```

> TOOL

tool_use Bash
id: toolu_019pViJ7MJHu8jx4J8Go3eFx
```json
{
  "command": "cd /home/<USER>/.claude/skills/shape-delivery; find . -maxdepth 2 -type f | head -50",
  "description": "List skill files"
}
```

> TOOL

tool_result
id: toolu_019pViJ7MJHu8jx4J8Go3eFx
```
./SKILL.md
Shell cwd was reset to /home/<USER>/src/drain-cycle
```

> TOOL

tool_use Bash
id: toolu_01NMt5ALBz5jumy856Bb17fb
```json
{
  "command": "find /home/<USER>/src/agent-skills-shaper /home/<USER>/.claude -name \"delivery-shape-contract.md\" -o -name \"task-sizing.md\" -o -name \"walk-delivery-plan\" 2>/dev/null | head; echo \"=== drain-cycle existing delivery plans ===\"; ls -R /home/<USER>/src/drain-cycle/docs/delivery-plans/ 2>/dev/null | head -40",
  "description": "Locate contract and example plans"
}
```

> TOOL

tool_result
id: toolu_01NMt5ALBz5jumy856Bb17fb
```
/home/<USER>/src/agent-skills-shaper/bin/walk-delivery-plan
/home/<USER>/src/agent-skills-shaper/references/task-sizing.md
/home/<USER>/src/agent-skills-shaper/docs/delivery-shape-contract.md
/home/<USER>/src/agent-skills-shaper/.worktrees/ABA-374/bin/walk-delivery-plan
/home/<USER>/src/agent-skills-shaper/.worktrees/ABA-374/references/task-sizing.md
/home/<USER>/src/agent-skills-shaper/.worktrees/ABA-374/docs/delivery-shape-contract.md
=== drain-cycle existing delivery plans ===
exec-state-file-rename/
live-execution-swimlanes/
D1-one-pack-owned-execution-state-file/
D1-live-execution-swimlanes/
README.md  3.2K
N01-amend-thin-supervisor-contract.md  4.9K
N02-pack-dual-writes-exec-state.md  3.6K
N03-supervisor-reads-exec-state.md  4.0K
N04-drop-legacy-handoff.md  2.9K
_deliverable.md  2.0K
README.md  4.3K
```

> TOOL

tool_use Read
id: toolu_01PiDudJBQnLvP6kUsscYRXY
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/docs/delivery-shape-contract.md"
}
```

> TOOL

tool_result
id: toolu_01PiDudJBQnLvP6kUsscYRXY
```
1	# delivery-shape — plan-artefact contract
2	
3	The schema for a **delivery plan**: the set of cross-referenced markdown files that turn one
4	committed initiative into an ordered, verifiable delivery hierarchy — deliverable → node → task —
5	that a human reads top-down and a deterministic reader walks bottom-up into a tracker manifest.
6	
7	This contract was **read off a worked example**, not designed in the abstract:
8	[`examples/delivery-plans/top-down-delivery-planning/`](../examples/delivery-plans/top-down-delivery-planning/).
9	Read that example alongside this spec — every rule here points at a node that demonstrates it.
10	
11	> **Tool-agnostic by rule.** This contract names no tracker, language, or runtime. It describes
12	> *file-set structure* and *tracker-artefact classes* (milestone-class / issue-class /
13	> sub-issue-class). Binding those classes to a concrete tracker is the **adapter's** job and lives
14	> in another repo. Emitted plans (the example) may name concrete tools; this contract may not.
15	
16	---
17	
18	## The three layers
19	
20	| Layer | Lives as | Tracker-artefact class | Completion criterion |
21	|-------|----------|------------------------|----------------------|
22	| **Deliverable** | a directory `D*/` with `_deliverable.md` | milestone-class | its served KR is observed |
23	| **Node** […]

> AGENT

Plan mode is exited. I have the contract. Now let me read the in-repo example plan and the two gate scripts so my emitted file-set matches conventions exactly.

> TOOL

tool_use Bash
id: toolu_013uFM9nPAAEyFNms8Yq2fRP
```json
{
  "command": "cd /home/<USER>/src/drain-cycle/docs/delivery-plans/exec-state-file-rename; echo \"=== README.md ===\"; cat README.md; echo; echo \"=== _deliverable.md ===\"; cat D1-one-pack-owned-execution-state-file/_deliverable.md; echo; echo \"=== N01 ===\"; cat D1-one-pack-owned-execution-state-file/N01-amend-thin-supervisor-contract.md",
  "description": "Read example delivery plan"
}
```

> TOOL

tool_result
id: toolu_013uFM9nPAAEyFNms8Yq2fRP
```
=== README.md ===
# Delivery plan — one pack-owned execution-state file (design decision §26)

Shaped from an **accepted design doc**: `docs/design-decisions.md` §26, "The supervisor guarantees
the execution state; each skill writes its own section." The full sizing and the two sequencing
paths live in the approved plan at `~/.claude/plans/refactored-booping-crayon.md`; this file-set
carries the recommended path (ship the rename standalone) as a deliverable → node → task hierarchy.

> **§-references may move.** A parallel effort splits `design-decisions.md` into separate ADR files.
> Treat §19/§24/§26 and ADR 0002 as pointers that could be re-homed.

## The decision being delivered

§26 names one pack-owned execution-state file per task (illustratively `exec-state.json`), written
section-per-phase by the skills, and drops the consumer-named `.drain-handoff.json`. The supervisor
authors none of it and reads only the fields it gates on (`pr_urls` today). The rename closes the
last consumer-coupling the two-layer split set out to remove.

The work is smaller than §26 implies: the supervisor reads one field (`pr_urls`) from one file
today, and the schema-v2 the decision treats as built was never written — so collapsing schemas is
documentation work, and the code change is a tolerant rename behind a dual-write/dual-read window.

## Traceability — […]

> AGENT

I'm back in plan mode with the full contract and a worked example (`exec-state-file-rename`) to mirror. I need the model-routing rubric to annotate tasks correctly, then I'll rewrite the plan as a proper delivery-shape blueprint.

> TOOL

tool_use Read
id: toolu_01VRErSaeMqN5ojxbu9Lrpe8
```json
{
  "file_path": "/home/<USER>/src/agent-skills-shaper/references/task-sizing.md"
}
```

> TOOL

tool_result
id: toolu_01VRErSaeMqN5ojxbu9Lrpe8
```
1	---
2	name: task-sizing
3	description: >
4	  Risk-weighted model-routing rubric — five axes scored Low/Med/High that route a
5	  single task to a model tier and a review-attention flag at planning time. Not effort
6	  estimation; a second lens on the verification-granularity Size check.
7	type: reference
8	cited_by:
9	  - skills/project/SKILL.md
10	---
11	
12	# Task sizing — the 5-axis routing rubric
13	
14	This rubric routes a single task to a **model tier** and a **review-attention flag** at planning time. It is risk-weighted *routing*, not effort estimation: the output is "which model should run this, and how much review does it warrant," never "how long will this take." You score five axes Low/Med/High, the stakes axis sets a default direction, the other axes adjust it, and a tier and a flag fall out.
15	
16	Routing is not cascading. **Routing** is planning-time pre-classification — one model is chosen per task *before* it runs. **Cascading** is runtime escalation — start on a cheap model and retry on a bigger one mid-execution when the cheap one fails. This rubric only does routing; cascading is a named, separate, out-of-scope layer (see *What this is […]

> AGENT

I now have the contract, the worked example, and the routing rubric. Rewriting the plan as a proper delivery-shape blueprint — deliverable → nodes → tasks with completion forms and `Model:` routing — plus the Linear mapping and the two verification gates.

> TOOL

tool_use Write
id: toolu_01MmAy4nESG9PXDD6fa22Eah
```json
{
  "file_path": "/home/<USER>/.claude/plans/composed-watching-cerf.md",
  "content": "# Delivery plan — Automated run scorecard\n\n## Context\n\nMeasuring the quality of a drain-cycle run is half-manual and the wrong shape. After each issue the\norchestrator writes a markdown draft to `~/.drain-cycle/grades/<issue>.md` with `status: draft` and\nan empty `## KR check` checklist (`grade_draft.py`); a human ticks the boxes and flips `status` to\n`confirmed` before `drain-cycle grade` counts it. That manual gate is why the user hits\n`warning: ABA-406 is a draft — excluded from rate`. Worse, the \"pass-rate\" never reads\n`outcome_verdict.result` (`grade.py:131`), so a **FAIL** verdict counts as a pass.\n\nWe want each run measured **automatically** on duration, cost, and correctness, with no human gate,\nand the concept renamed from \"grade\" to **scorecard**. Duration and cost already live in every\nrun-log entry (`duration_seconds`, `cost_usd`, `usage.cumulative`). Correctness is derived from\nverdicts already (mostly) captured.\n\n**Decided scope (confirmed with the user):**\n- Correctness = `outcome_verdict.result == \"pass\"` AND `review_verdict == \"GO\"`.\n- `prep_verdict.route` is shown advisory-only; it does not gate correctness (no producer yet — needs\n  a cross-repo `pr-prepare` change in `agent-skills-shaper`).\n- The manual markdown draft/confirmed flow is deleted; the scorecard reads run-log JSON directly.\n- Shaped as a **new Linear project + one milestone**, structured via `shape:delivery` conventions\n  (`docs/delivery-shape-contract.md`).\n\nThis plan defines the delivery-plan file-set to emit […]

> TOOL

tool_result
id: toolu_01MmAy4nESG9PXDD6fa22Eah
```
The file /home/<USER>/.claude/plans/composed-watching-cerf.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

The plan is now a delivery-shape blueprint following the repo's `docs/delivery-shape-contract.md` conventions, mirroring the existing `exec-state-file-rename` plan:

- **One deliverable D1** serving a single KR1, with a hand-count manifest (1 milestone / 5 issues / 16 sub-issues).
- **Five typed nodes**: `adr` (correctness contract, blocks the rest) → `story·skeleton` (review verdict → run log, the real integration seam) → `story` (scorecard module) → `story` (CLI + delete manual flow) → `ktlo` (doc hygiene).
- Every task carries a `Done when:` clause and a `Model:` routing line scored on the 5-axis rubric.
- Execution emits the file-set under `docs/delivery-plans/scorecard/`, runs both gates (`bin/walk-delivery-plan`, `bin/check-plan-framing`), then creates the Linear project + milestone + 5 blocked-ordered issues.

> TOOL

tool_use ExitPlanMode
id: toolu_011BLDsJrmpevbCwVtHaQ4Bp
```json
{
  "allowedPrompts": [
    {
      "tool": "Bash",
      "prompt": "run the delivery-plan gate scripts (bin/walk-delivery-plan, bin/check-plan-framing)"
    }
  ],
  "plan": "# Delivery plan — Automated run scorecard\n\n## Context\n\nMeasuring the quality of a drain-cycle run is half-manual and the wrong shape. After each issue the\norchestrator writes a markdown draft to `~/.drain-cycle/grades/<issue>.md` with `status: draft` and\nan empty `## KR check` checklist (`grade_draft.py`); a human ticks the boxes and flips `status` to\n`confirmed` before `drain-cycle grade` counts it. That manual gate is why the user hits\n`warning: ABA-406 is a draft — excluded from rate`. Worse, the \"pass-rate\" never reads\n`outcome_verdict.result` (`grade.py:131`), so a **FAIL** verdict counts as a pass.\n\nWe want each run measured **automatically** on duration, cost, and correctness, with no human gate,\nand the concept renamed from \"grade\" to **scorecard**. Duration and cost already live in every\nrun-log entry (`duration_seconds`, `cost_usd`, `usage.cumulative`). Correctness is derived from\nverdicts already (mostly) captured.\n\n**Decided scope (confirmed with the user):**\n- Correctness = `outcome_verdict.result == \"pass\"` AND `review_verdict == \"GO\"`.\n- `prep_verdict.route` is shown advisory-only; it does not gate correctness (no producer yet — needs\n  a cross-repo `pr-prepare` change in `agent-skills-shaper`).\n- The manual markdown draft/confirmed flow is deleted; the scorecard reads run-log JSON directly.\n- Shaped as a **new Linear project + one […]

> TOOL

tool_result ERROR
id: toolu_011BLDsJrmpevbCwVtHaQ4Bp
```
Plan review feedback — revise the plan to address the review comments. Comments are in /home/<USER>/.crit/plans/automate-run-quality-measurement-replace-manual-grade-with-scorecard-2026-06-18/.crit/review.json — grouped per file with start_line/end_line referencing the source. Each comment has a scope field: "line" for inline comments, "file" for file-level, or "review" for review-level comments. Read the file, revise the plan to address each comment. If you are running under Codex, re-emit the revised plan inside <proposed_plan>...</proposed_plan> so Crit can review the new version. To reply to comments, use `crit comment --plan automate-run-quality-measurement-replace-manual-grade-with-scorecard-2026-06-18 --reply-to <id> --author <your-name> "<explanation>"`.
```

> TOOL

tool_use Bash
id: toolu_01DbtB5LndMx9tPAbnuojwTY
```json
{
  "command": "cd /home/<USER>/.crit/plans/automate-run-quality-measurement-replace-manual-grade-with-scorecard-2026-06-18/.crit/; python3 -c \"\nimport json\nd=json.load(open('review.json'))\nprint('round', d.get('review_round'))\nfor c in d['review_comments']:\n    print('---', c['id'], 'scope=', c['scope'], 'lines', c['start_line'],'-',c['end_line'], 'author=', c.get('author'))\n    print(c['body'])\n\"",
  "description": "Read latest review comments"
}
```

> TOOL

tool_result
id: toolu_01DbtB5LndMx9tPAbnuojwTY
```
round 2
--- r_18e925 scope= review lines 0 - 0 author= Anton Babushkin
this plan should be about creating a delivery plan in linear (project or just issues depending on how many tasks there are)
--- r_d9b3de scope= review lines 0 - 0 author= Anton Babushkin
use /shape:delivery to check if you've followed all the right conventions
--- r_483cea scope= review lines 0 - 0 author= Anton Babushkin
review the plan using the /writing-refinement skill

delete anything unnecessary or what would clash with the exec:breakdown skill
Shell cwd was reset to /home/<USER>/src/drain-cycle
```

> AGENT

Two new asks: run `writing-refinement` over the plan, and **delete anything that clashes with `exec:breakdown`**. That's the key insight — my per-node task tables (Done-when + `Model:` + 5-axis scores) are exactly what `exec:breakdown` produces at issue pickup, so pre-authoring them in the delivery plan duplicates its job. Let me load writing-refinement to apply its rules faithfully.

> TOOL

tool_use Skill
id: toolu_01V77iPE4qnzCgbTaVqE12uw
```json
{
  "skill": "shape-writing-refinement",
  "args": "Tighten the delivery plan at /home/<USER>/.claude/plans/composed-watching-cerf.md; remove pre-authored task/Model breakdowns that belong to exec:breakdown at pickup."
}
```

> TOOL

tool_result
id: toolu_01V77iPE4qnzCgbTaVqE12uw
```
Launching skill: shape-writing-refinement
```

> AGENT

I'll apply writing-refinement and cut the clash with `exec:breakdown`. The core fix: my per-node task tables (Done-when + `Model:` + 5-axis scores) are precisely what `exec:breakdown` generates when an issue is picked up — so the delivery plan should stop at the **issue (node) level** with node-level completion criteria, and let `exec:breakdown` expand tasks at pickup. I'll also merge the facts repeated across sections (the "review never read", "prep deferred", and correctness-definition statements each had several homes).

> TOOL

tool_use Write
id: toolu_01FsH4NWu3JW9JYXYZELd1cK
```json
{
  "file_path": "/home/<USER>/.claude/plans/composed-watching-cerf.md",
  "content": "# Delivery plan — Automated run scorecard\n\nCreate a Linear project that replaces the manual `grade` draft/confirmed gate with an automatic\n`scorecard` scoring every run on duration, cost, and correctness — where correctness =\n`outcome_verdict pass AND review GO`. One deliverable, five issues; `exec:breakdown` expands each\nissue into tasks at pickup.\n\n## Why\n\nAfter each issue the orchestrator writes a markdown draft to `~/.drain-cycle/grades/<issue>.md` with\n`status: draft`; a human ticks `## KR check` boxes and flips it to `confirmed` before\n`drain-cycle grade` counts it. That manual gate is why the user hits\n`warning: ABA-406 is a draft — excluded from rate`. And the \"pass-rate\" never reads\n`outcome_verdict.result` (`grade.py:131`), so a **FAIL** verdict counts as a pass.\n\nDuration and cost already live in every run-log entry (`duration_seconds`, `cost_usd`,\n`usage.cumulative`); correctness comes from verdicts the pipeline already (mostly) records. The fix\nis to score each run straight from the run-log JSON and delete the markdown gate.\n\n### Signal readiness (verified against source)\n\n| Signal | Produced | Reaches run log | Action |\n|---|---|---|---|\n| `outcome_verdict` (exec:verify) | yes | yes | none |\n| `review` GO/NO-GO (exec:review) | yes — `review` section, `tests/fixtures/exec-state.json:30` | no — `handoff.py` never reads it | wire it (N02) |\n| `prep_verdict.route` (pr-prepare) | no producer […]

> TOOL

tool_result
id: toolu_01FsH4NWu3JW9JYXYZELd1cK
```
The file /home/<USER>/.claude/plans/composed-watching-cerf.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Revised. Changes made this round:

- **Cut the exec:breakdown clash** — removed every per-node task table with `Done when:` / `Model:` / 5-axis scores. The plan now stops at the issue level with a node-level completion criterion each; the manifest counts milestones + issues only, with an explicit note that `exec:breakdown` produces the per-task `done_when` + routing scores at pickup.
- **Applied writing-refinement** — added a 30-second main-point sentence up top; merged repeated facts to one home each (the "review never read", "prep deferred", and correctness-definition statements were each restated 3–4 times → now stated once and referenced); collapsed the duplicated signal-readiness content; tightened headings to results.
- Kept the load-bearing structure: one deliverable serving KR1, five typed nodes (adr → story·skeleton → story → story → ktlo), the gates, and the Linear creation steps.

> TOOL

tool_use ExitPlanMode
id: toolu_01239RuJV6fm5rVw7Q2vCUnJ
```json
{
  "allowedPrompts": [
    {
      "tool": "Bash",
      "prompt": "run the delivery-plan gate scripts (bin/walk-delivery-plan, bin/check-plan-framing)"
    }
  ],
  "plan": "# Delivery plan — Automated run scorecard\n\nCreate a Linear project that replaces the manual `grade` draft/confirmed gate with an automatic\n`scorecard` scoring every run on duration, cost, and correctness — where correctness =\n`outcome_verdict pass AND review GO`. One deliverable, five issues; `exec:breakdown` expands each\nissue into tasks at pickup.\n\n## Why\n\nAfter each issue the orchestrator writes a markdown draft to `~/.drain-cycle/grades/<issue>.md` with\n`status: draft`; a human ticks `## KR check` boxes and flips it to `confirmed` before\n`drain-cycle grade` counts it. That manual gate is why the user hits\n`warning: ABA-406 is a draft — excluded from rate`. And the \"pass-rate\" never reads\n`outcome_verdict.result` (`grade.py:131`), so a **FAIL** verdict counts as a pass.\n\nDuration and cost already live in every run-log entry (`duration_seconds`, `cost_usd`,\n`usage.cumulative`); correctness comes from verdicts the pipeline already (mostly) records. The fix\nis to score each run straight from the run-log JSON and delete the markdown gate.\n\n### Signal readiness (verified against source)\n\n| Signal | Produced | Reaches run log | Action |\n|---|---|---|---|\n| `outcome_verdict` (exec:verify) | yes | yes | none |\n| `review` GO/NO-GO (exec:review) | yes — `review` section, `tests/fixtures/exec-state.json:30` | no — `handoff.py` […]

> TOOL

tool_result
id: toolu_01239RuJV6fm5rVw7Q2vCUnJ
```
User has approved your plan. You can now start coding. Start with updating your todo list if applicable

Your plan has been saved to: /home/<USER>/.claude/plans/composed-watching-cerf.md
You can refer back to it if needed during implementation.

## Approved Plan (edited by user):
# Delivery plan — Automated run scorecard

Create a Linear project that replaces the manual `grade` draft/confirmed gate with an automatic
`scorecard` scoring every run on duration, cost, and correctness — where correctness =
`outcome_verdict pass AND review GO`. One deliverable, five issues; `exec:breakdown` expands each
issue into tasks at pickup.

## Why

After each issue the orchestrator writes a markdown draft to `~/.drain-cycle/grades/<issue>.md` with
`status: draft`; a human ticks `## KR check` boxes and flips it to `confirmed` before
`drain-cycle grade` counts it. That manual gate is why the user hits
`warning: ABA-406 is a draft — excluded from rate`. And the "pass-rate" never reads
`outcome_verdict.result` (`grade.py:131`), so a **FAIL** verdict counts as a pass.

Duration and cost already live in every run-log entry (`duration_seconds`, `cost_usd`,
`usage.cumulative`); correctness comes from verdicts the pipeline already (mostly) records. The fix
is to score each run straight from the run-log JSON and delete the markdown gate.

### […]

> AGENT

Plan approved. Let me set up task tracking and read the two gate scripts so the emitted file-set passes on the first try.

> TOOL

tool_use ToolSearch
id: toolu_01RPH7WtzdNRBVXHM9QX9QdH
```json
{
  "query": "select:TaskCreate",
  "max_results": 1
}
```

> TOOL

tool_result
id: toolu_01RPH7WtzdNRBVXHM9QX9QdH
```
{
  "type": "tool_reference",
  "tool_name": "TaskCreate"
}
```

> TOOL

tool_use Bash
id: toolu_01H3jZ6k5M9He7cAaUMmP5vZ
```json
{
  "command": "cd /home/<USER>/src/agent-skills-shaper; echo \"=== walk-delivery-plan ===\"; cat bin/walk-delivery-plan; echo; echo \"=== check-plan-framing ===\"; cat bin/check-plan-framing",
  "description": "Read delivery-plan gate scripts"
}
```

> TOOL

tool_result
id: toolu_01H3jZ6k5M9He7cAaUMmP5vZ
```
<persisted-output>
Output too large (36.8KB). Full output saved to: /home/<USER>/.claude/projects/-Users-anton-src-drain-cycle/6d19145b-86d2-4b0d-9077-624706537065/tool-results/by9iihlmp.txt

Preview (first 2KB):
=== walk-delivery-plan ===
#!/usr/bin/env python3
"""walk-delivery-plan — walk a delivery-plan file-set into a tracker manifest.

Reads a delivery plan laid out per `docs/delivery-shape-contract.md`
(deliverable directories → node files → task checklist lines) and emits a
tracker-shaped manifest: milestone-class ← deliverables, issue-class ← nodes,
sub-issue-class ← tasks. The manifest is *derived* from directory structure +
front-matter, never authored.

The script is the mechanical-conversion half of the delivery-shape spike's kill
gate. It is deliberately dependency-free (stdlib only, no YAML library): the
front-matter the contract pins down is a small fixed set of keys, and a targeted
reader for those keys is more boring — and more honest about what it relies on —
than pulling in a parser. If a plan's front-matter ever outgrows this reader,
that is itself signal the seam needs re-shaping.

Usage:
    bin/walk-delivery-plan <plan-dir> [--json]

Two tier shapes are accepted:

  - Full tier — root has `D<n>-*/` deliverable directories; manifest oracle
    in README is required.
  - Lite tier — root has flat `N<nn>-*.md` node files (no `D*/`); for the
    small-scale delivery-shape path. No manifest oracle is required; the
    walker emits a flat […]

> TOOL

tool_use Read
id: toolu_019FPmXvV71NyEUn39i5JD8A
```json
{
  "file_path": "/home/<USER>/.claude/projects/-Users-anton-src-drain-cycle/6d19145b-86d2-4b0d-9077-624706537065/tool-results/by9iihlmp.txt"
}
```

> TOOL

tool_result
id: toolu_019FPmXvV71NyEUn39i5JD8A
```
1	=== walk-delivery-plan ===
2	#!/usr/bin/env python3
3	"""walk-delivery-plan — walk a delivery-plan file-set into a tracker manifest.
4	
5	Reads a delivery plan laid out per `docs/delivery-shape-contract.md`
6	(deliverable directories → node files → task checklist lines) and emits a
7	tracker-shaped manifest: milestone-class ← deliverables, issue-class ← nodes,
8	sub-issue-class ← tasks. The manifest is *derived* from directory structure +
9	front-matter, never authored.
10	
11	The script is the mechanical-conversion half of the delivery-shape spike's kill
12	gate. It is deliberately dependency-free (stdlib only, no YAML library): the
13	front-matter the contract pins down is a small fixed set of keys, and a targeted
14	reader for those keys is more boring — and more honest about what it relies on —
15	than pulling in a parser. If a plan's front-matter ever outgrows this reader,
16	that is itself signal the seam needs re-shaping.
17	
18	Usage:
19	    bin/walk-delivery-plan <plan-dir> [--json]
20	
21	Two tier shapes are accepted:
22	
23	  - Full tier — root has `D<n>-*/` deliverable directories; manifest oracle
24	    in README is required.
25	  - Lite tier — root has flat `N<nn>-*.md` node files (no `D*/`); for the
26 […]

> AGENT

I now understand the gates precisely. The clean reconciliation: emit a **full-tier** plan (D1/ with N01–N05) carrying **zero `- [ ]` task lines** — the framing gate only requires a skeleton task and `Model:` annotations *when tasks exist*, so deferring all tasks to `exec:breakdown` passes both gates, with the README oracle at 1 milestone / 5 issues / 0 sub-issues. Let me set up tracking and emit the file-set.

> TOOL

tool_use TaskCreate
id: toolu_01W1BKqUKdGtC9SHziiVDvqB
```json
{
  "subject": "Emit scorecard delivery-plan file-set",
  "description": "Write docs/delivery-plans/scorecard/ — README, D1 _deliverable.md, and N01–N05 nodes with five-section bodies, no pre-authored tasks.",
  "activeForm": "Emitting delivery-plan file-set"
}
```

> TOOL

tool_result
id: toolu_01W1BKqUKdGtC9SHziiVDvqB
```
Task #1 created successfully: Emit scorecard delivery-plan file-set
```

> TOOL

tool_use TaskCreate
id: toolu_01Pf5RqCGHS1sGCXzQoFjz7V
```json
{
  "subject": "Pass both delivery-plan gates",
  "description": "Run bin/walk-delivery-plan and bin/check-plan-framing from agent-skills-shaper against the emitted plan; fix until both exit 0.",
  "activeForm": "Running delivery-plan gates"
}
```

> TOOL

tool_result
id: toolu_01Pf5RqCGHS1sGCXzQoFjz7V
```
Task #2 created successfully: Pass both delivery-plan gates
```

> TOOL

tool_use TaskCreate
id: toolu_01T2LmCoGaKJgkkMqqh5MZ7w
```json
{
  "subject": "Create Linear project + milestone + 5 issues",
  "description": "Create the \"Automated run scorecard\" project (ABA), milestone \"D1 — Scorecard replaces manual grade\", and issues N01–N05 with model-tier labels and blocked-by ordering.",
  "activeForm": "Creating Linear artefacts"
}
```

> TOOL

tool_result
id: toolu_01T2LmCoGaKJgkkMqqh5MZ7w
```
Task #3 created successfully: Create Linear project + milestone + 5 issues
```

> AGENT

Now writing the file-set.

> TOOL

tool_use Write
id: toolu_0149nmYw9ySnuYfh8PxsDYWL
```json
{
  "file_path": "/home/<USER>/src/drain-cycle/docs/delivery-plans/scorecard/README.md",
  "content": "# Delivery plan — Automated run scorecard\n\nReplace the manual `grade` draft/confirmed gate with an automatic `scorecard` that scores every\ndrain-cycle run on duration, cost, and correctness — where correctness is `outcome_verdict` pass\nAND review GO.\n\n## Goal\n\nEvery drain-cycle run is scored automatically on duration, cost, and correctness, with no manual\nconfirmation step.\n\n## KR1\n\n`drain-cycle scorecard` derives correctness from verdicts (outcome pass AND review GO); a FAIL\nverdict is never counted correct; the draft-confirmation warning is gone; silent-Done (a Done entry\nwith a null outcome verdict) still exits nonzero.\n\n## Why now\n\nAfter each issue the orchestrator writes a markdown draft to `~/.drain-cycle/grades/<issue>.md` with\n`status: draft`; a human ticks `## KR check` boxes and flips it to `confirmed` before\n`drain-cycle grade` counts it — the gate behind the `… is a draft — excluded from rate` warning. The\nreported pass-rate never reads `outcome_verdict.result` (`grade.py:131`), so a FAIL verdict counts as\na pass. Duration and cost already live in every run-log entry; correctness comes from verdicts the\npipeline already records, except the review GO/NO-GO verdict, which `handoff.py` writes nowhere the\nrun log can see. The fix scores each run from the run-log JSON and deletes the markdown gate.\n\n## How to read\n\nStart here, then read `D1-scorecard-replaces-manual-grade/_deliverable.md` for the milestone, […]

> TOOL

tool_result
id: toolu_0149nmYw9ySnuYfh8PxsDYWL
```
File created successfully at: /home/<USER>/src/drain-cycle/docs/delivery-plans/scorecard/README.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_01FM1bodjwWAPBpFWPZZbBPi
```json
{
  "file_path": "/home/<USER>/src/drain-cycle/docs/delivery-plans/scorecard/D1-scorecard-replaces-manual-grade/_deliverable.md",
  "content": "---\nlayer: deliverable\nid: D1\ntitle: Scorecard replaces manual grade\nparent: ..\nserves_kr: KR1\nmaps_to: linear-milestone\ncompletion:\n  form: kr-observed\n  criterion: >\n    KR1 holds — drain-cycle scorecard scores each run on duration, cost, and\n    correctness (outcome pass AND review GO) straight from the run log, no\n    markdown confirmation flow exists, and silent-Done still exits nonzero.\n---\n\n# D1 — Scorecard replaces manual grade\n\n**Serves:** KR1 — automatic per-run scoring on duration, cost, and correctness (see the README,\n\"Goal\" and \"KR1\", for the full claim).\n\nThis deliverable maps onto a new Linear milestone. Rule A1 (`design-doc` trigger) does not fire — the\nchange is reversible, single-repo, and additive to the run-log schema — so there is no `design-doc`\nnode. The one architectural decision (remove the human gate; define automated correctness) lands in\nan `adr` node placed first and blocking the build nodes.\n\n## Nodes\n\n- [N01 — Record the scorecard correctness contract](N01-record-the-scorecard-correctness-contract.md) · `adr`\n- [N02 — Review verdict reaches the run log](N02-review-verdict-reaches-the-run-log.md) · `story` · `skeleton`\n- [N03 — Scorecard computes and reports per-run quality](N03-scorecard-computes-and-reports-per-run-quality.md) · `story`\n- [N04 — CLI exposes scorecard; manual draft flow removed](N04-cli-exposes-scorecard-manual-draft-flow-removed.md) · `story`\n- [N05 — Retire stale grade references](N05-retire-stale-grade-references.md) · `ktlo`\n\n## Done when\n\nKR1 is observed: `drain-cycle scorecard` scores each run on duration, cost, and correctness derived\nfrom […]

> TOOL

tool_result
id: toolu_01FM1bodjwWAPBpFWPZZbBPi
```
File created successfully at: /home/<USER>/src/drain-cycle/docs/delivery-plans/scorecard/D1-scorecard-replaces-manual-grade/_deliverable.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_01HsxhdDBT6rzy8XghLFVGFR
```json
{
  "file_path": "/home/<USER>/src/drain-cycle/docs/delivery-plans/scorecard/D1-scorecard-replaces-manual-grade/N01-record-the-scorecard-correctness-contract.md",
  "content": "---\nlayer: node\nid: N01\ntype: adr\ntitle: Record the scorecard correctness contract\nparent: D1\nserves_kr: KR1\nmaps_to: linear-issue\nexternal_window: none\ncompletion:\n  form: decision-record\ndelegates_to: ADR discipline (Rule A3 + D3 living ADRs) — plan-review gate fires on the gate-removal and correctness-definition decision\n---\n\n# N01 — Record the scorecard correctness contract\n\n**Type:** `adr`. The build nodes encode this contract, so it is decided before they are picked up.\n\n> **▶ On pickup — before N02–N05:** record the decision through the ADR discipline and run the\n> plan-review gate.\n> **Blocks:** N02, N03, N04, N05 — their task breakdown waits until this is accepted.\n\n## What\n\nRecord an ADR for the automated-quality contract: remove the manual draft/confirmed gate; define run\ncorrectness as `outcome_verdict` pass AND review GO; keep silent-Done as the hard violation; add\n`review_verdict` to the run log as an additive field; treat `prep_verdict.route` as advisory until a\nproducer exists.\n\n## Why\n\nBuilding the correctness rule before its semantics are fixed risks re-encoding today's bug, where a\nFAIL verdict counts as a pass. The bet is that two already-recorded verdicts (outcome and review) are\na strong enough correctness signal to retire the human gate. Rejected alternatives: outcome-only\ncorrectness, where the agent grades its own work with no second signal; and a full prep-gated\ncomposite now, which blocks […]

> TOOL

tool_result
id: toolu_01HsxhdDBT6rzy8XghLFVGFR
```
File created successfully at: /home/<USER>/src/drain-cycle/docs/delivery-plans/scorecard/D1-scorecard-replaces-manual-grade/N01-record-the-scorecard-correctness-contract.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_01QQSCWeAyFKPk2zhw5UPnoT
```json
{
  "file_path": "/home/<USER>/src/drain-cycle/docs/delivery-plans/scorecard/D1-scorecard-replaces-manual-grade/N02-review-verdict-reaches-the-run-log.md",
  "content": "---\nlayer: node\nid: N02\ntype: story\ntitle: Review verdict reaches the run log\nparent: D1\nserves_kr: KR1\nmaps_to: linear-issue\nskeleton: true\nexternal_window: none\ncompletion:\n  form: acceptance-criteria\ndelegates_to: at-pickup task breakdown (exec:breakdown)\n---\n\n# N02 — Review verdict reaches the run log\n\n**Type:** `story`. This is the deliverable's walking skeleton — the thinnest end-to-end slice through\nthe real seam.\n\n> **Blocked by:** N01 — task breakdown waits until the correctness contract is accepted.\n\n## What\n\nAs the supervisor, I want each worker's review GO/NO-GO verdict recorded in the run log, so that the\nscorecard can gate correctness on the review outcome.\n\n## Why\n\nexec:review already writes a `review` section to `exec-state.json`, but `handoff.py` never reads it,\nso the verdict never reaches the run log. This is the real integration seam — `exec-state.json` →\n`handoff.py` → `orchestrator.py` → `runlog.py` — and the thinnest end-to-end slice of the\ndeliverable, which is why it is the skeleton. The change mirrors the existing `outcome_verdict` path\n(`_verify_to_outcome`, handoff.py:95). Rejected alternative: re-deriving review state from PR status,\nwhich lags real time and needs external lookups.\n\n## Completion\n\n- **Done when:** `handoff.read` maps the `exec-state.json` `review` section to a `review_verdict`\n  (`{\"result\": \"go\"|\"no-go\", \"findings\": [...]}`); an unrecognised verdict drops to null.\n- **Done when:** a run-log entry written from `tests/fixtures/exec-state.json` carries\n  `review_verdict {\"result\": \"go\", \"findings\": []}`.\n- **Done when:** […]

> TOOL

tool_result
id: toolu_01QQSCWeAyFKPk2zhw5UPnoT
```
File created successfully at: /home/<USER>/src/drain-cycle/docs/delivery-plans/scorecard/D1-scorecard-replaces-manual-grade/N02-review-verdict-reaches-the-run-log.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_012CVSxQYCSyjiyMYEqBGWTk
```json
{
  "file_path": "/home/<USER>/src/drain-cycle/docs/delivery-plans/scorecard/D1-scorecard-replaces-manual-grade/N03-scorecard-computes-and-reports-per-run-quality.md",
  "content": "---\nlayer: node\nid: N03\ntype: story\ntitle: Scorecard computes and reports per-run quality\nparent: D1\nserves_kr: KR1\nmaps_to: linear-issue\nexternal_window: none\ncompletion:\n  form: acceptance-criteria\ndelegates_to: at-pickup task breakdown (exec:breakdown)\n---\n\n# N03 — Scorecard computes and reports per-run quality\n\n**Type:** `story`.\n\n> **Blocked by:** N01 (the correctness contract) and N02 (`review_verdict` in the run log).\n\n## What\n\nAs an operator, I want `drain-cycle scorecard` to read the run log and report each run's duration,\ncost, and correctness, so that I can measure run quality without confirming anything by hand.\n\n## Why\n\nThis replaces the markdown draft/confirmed flow and fixes the bug where a FAIL verdict counts as a\npass — `grade.py:131` never reads `outcome_verdict.result`. It reuses `_find_run_entry`\n(grade.py:57) and reads run-log JSON directly. Rejected alternative: keep the markdown files and\nauto-confirm drafts, which leaves a second source of truth that drifts from the run log.\n\n## Completion\n\n- **Done when:** `scorecard` prints one row per run grouped by `cycle_id`, each with duration, cost,\n  and tokens.\n- **Done when:** correctness = outcome pass AND review GO; a FAIL outcome and a NO-GO review each\n  yield not-correct; a missing review verdict yields not-correct but is not a violation.\n- **Done when:** a Done entry with a null `outcome_verdict` exits 1 and is listed; a clean run exits 0\n […]

> TOOL

tool_result
id: toolu_012CVSxQYCSyjiyMYEqBGWTk
```
File created successfully at: /home/<USER>/src/drain-cycle/docs/delivery-plans/scorecard/D1-scorecard-replaces-manual-grade/N03-scorecard-computes-and-reports-per-run-quality.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_01D7Xs9PdERtoY1xgxdiwQhb
```json
{
  "file_path": "/home/<USER>/src/drain-cycle/docs/delivery-plans/scorecard/D1-scorecard-replaces-manual-grade/N04-cli-exposes-scorecard-manual-draft-flow-removed.md",
  "content": "---\nlayer: node\nid: N04\ntype: story\ntitle: CLI exposes scorecard; manual draft flow removed\nparent: D1\nserves_kr: KR1\nmaps_to: linear-issue\nexternal_window: none\ncompletion:\n  form: acceptance-criteria\ndelegates_to: at-pickup task breakdown (exec:breakdown)\n---\n\n# N04 — CLI exposes scorecard; manual draft flow removed\n\n**Type:** `story`.\n\n> **Blocked by:** N03 — the scorecard module must exist before the CLI exposes it.\n\n## What\n\nAs an operator, I want `drain-cycle scorecard` to be the only quality command, with no markdown\ndrafts to confirm, so that run quality is measured automatically end to end.\n\n## Why\n\nThis retires the manual gate entirely: the markdown draft writer, the orchestrator's auto-draft\nwrite, and the `grade-draft` subcommand all go. `kr2_check`'s `prep_verdict` requirement\n(kr2_check.py:35) can never hold — no producer writes it — so it is dropped. Rejected alternative:\nkeep `grade-draft` as an alias, which preserves the dead flow.\n\n## Completion\n\n- **Done when:** `drain-cycle scorecard` dispatches, and `grade` / `grade-draft` are unknown\n  invocations (exit 2).\n- **Done when:** `grade_draft.py` and the orchestrator auto-draft write (orchestrator.py:980-988) are\n  gone, and no code references `grade_draft`.\n- **Done when:** `kr2_check` requires only `outcome_verdict` on Done entries; its tests pass an entry\n  with `outcome_verdict` and no `prep_verdict`.\n- **Done when:** the test suite is green and renamed `test_scorecard_*`, including a regression test\n  that a FAIL verdict is not counted correct.\n\n## […]

> TOOL

tool_result
id: toolu_01D7Xs9PdERtoY1xgxdiwQhb
```
File created successfully at: /home/<USER>/src/drain-cycle/docs/delivery-plans/scorecard/D1-scorecard-replaces-manual-grade/N04-cli-exposes-scorecard-manual-draft-flow-removed.md (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Write
id: toolu_012AoHxZZ4F4ck3sYujQ8pJq
```json
{
  "file_path": "/home/<USER>/src/drain-cycle/docs/delivery-plans/scorecard/D1-scorecard-replaces-manual-grade/N05-retire-stale-grade-references.md",
  "content": "---\nlayer: node\nid: N05\ntype: ktlo\ntitle: Retire stale grade references\nparent: D1\nserves_kr: KR1\nmaps_to: linear-issue\nexternal_window: none\ncompletion:\n  form: none\ndelegates_to: ops slot — KTLO carve-out, no outcome framing\n---\n\n# N05 — Retire stale `grade` references\n\n**Type:** `ktlo`.\n\n> **Blocked by:** N04 — rename the surface before retiring references to the old name.\n\n## What\n\nReplace stale `grade` / `grade-draft` mentions in code comments and current docs with `scorecard`,\npreserving behaviour. Historical ADRs keep their original language.\n\n## Why\n\nA renamed command surface drifts from comments that still say `grade`, misleading the next reader.\nThis is housekeeping with no behaviour change — a KTLO carve-out, so it carries no outcome framing.\n\n## Completion\n\nNone — KTLO carve-out. Behaviour is unchanged; the node is done when grepping `grade` under\n`drain_cycle/` and `docs/` returns only historical ADRs (e.g. comments at `runlog.py:74-76` and\n`progress.py:6` now read `scorecard`).\n\n## Assumptions\n\n- Historical ADRs are intentionally left untouched. *(verified)*\n\n## Key Risks\n\n- **Risk:** a doc reference is missed and keeps pointing at the old command.\n  *Mitigation:* the completion grep is the falsifier — it must return only historical ADRs.\n"
}
```

> TOOL

tool_result
id: toolu_012AoHxZZ4F4ck3sYujQ8pJq
```
File created successfully at: /home/<USER>/src/drain-cycle/docs/delivery-plans/scorecard/D1-scorecard-replaces-manual-grade/N05-retire-stale-grade-references.md (file state is current in your context — no need to Read it back)
```

> AGENT

File-set emitted. Now run both gates.

> TOOL

tool_use Bash
id: toolu_01Cae5Zc2zQSJcef6MRQQVQH
```json
{
  "command": "cd /home/<USER>/src/drain-cycle; PLAN=docs/delivery-plans/scorecard; echo \"=== walk-delivery-plan ===\"; python3 /home/<USER>/src/agent-skills-shaper/bin/walk-delivery-plan \"$PLAN\"; echo \"exit: $?\"; echo; echo \"=== check-plan-framing ===\"; python3 /home/<USER>/src/agent-skills-shaper/bin/check-plan-framing \"$PLAN\"; echo \"exit: $?\"",
  "description": "Run both delivery-plan gates"
}
```

> TOOL

tool_result
id: toolu_01Cae5Zc2zQSJcef6MRQQVQH
```
=== walk-delivery-plan ===
Delivery-plan manifest — scorecard
source: docs/delivery-plans/scorecard

MILESTONE  D1  Scorecard replaces manual grade
           [linear-milestone · serves KR1]
  ISSUE  N01  Record the scorecard correctness contract
         [linear-issue · adr · KR1]
         completion: decision-record
  ISSUE  N02  Review verdict reaches the run log
         [linear-issue · story · KR1 · skeleton]
         completion: acceptance-criteria
  ISSUE  N03  Scorecard computes and reports per-run quality
         [linear-issue · story · KR1]
         completion: acceptance-criteria
  ISSUE  N04  CLI exposes scorecard; manual draft flow removed
         [linear-issue · story · KR1]
         completion: acceptance-criteria
  ISSUE  N05  Retire stale grade references
         [linear-issue · ktlo · KR1]
         completion: none

Summary: 1 milestones / 5 issues / 0 sub-issues
Oracle (README hand-count): 1 / 5 / 0  -> MATCH
exit: 0

=== check-plan-framing ===

FRAMING DROPPED:
  Assumptions list items without a (verified) or (to-verify) tag — every assumption must be explicitly verified or marked for verification:
    - D1-scorecard-replaces-manual-grade/N03-scorecard-computes-and-reports-per-run-quality.md:
        - The silent-Done check (Done with a null `outcome_verdict`) stays the only nonzero-exit condition.
check-plan-framing — scorecard
source: docs/delivery-plans/scorecard  (tier: full)
nodes checked: 5
  [ok ] N01  D1-scorecard-replaces-manual-grade/N01-record-the-scorecard-correctness-contract.md  (adr)
  [ok ] N02  D1-scorecard-replaces-manual-grade/N02-review-verdict-reaches-the-run-log.md  (story)
  [UNTAGGED ASSUMPTION] N03  D1-scorecard-replaces-manual-grade/N03-scorecard-computes-and-reports-per-run-quality.md  (story)
  [ok ] N04  D1-scorecard-replaces-manual-grade/N04-cli-exposes-scorecard-manual-draft-flow-removed.md  (story)
  [ok ] N05  D1-scorecard-replaces-manual-grade/N05-retire-stale-grade-references.md  (ktlo)
skeleton tasks in plan: 0 […]