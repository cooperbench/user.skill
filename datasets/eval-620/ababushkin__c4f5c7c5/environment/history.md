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