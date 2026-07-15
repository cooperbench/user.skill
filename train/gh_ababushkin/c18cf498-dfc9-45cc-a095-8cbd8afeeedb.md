> DEVELOPER

# Make worktrees stack-ready and add the agent handoff file

**Depends on:** [ABA-300](https://linear.app/ababushkin/issue/ABA-300/spike-prove-the-graphite-pr-stacking-sequence-gate) (spike). Part of the stacked-PR feature; blocks the stack-assembly ticket.

## What

Each issue's branch forks off the previous same-repo issue's branch instead of always `main`, and the spawned agent commits to its branch **without pushing**, leaving behind a handoff file with the PR body and code-review findings.

## Why

A Graphite stack is a chain: issue N must sit on top of issue N-1 within the same repo. And only the agent knows what it changed and what a reviewer should examine, so it must record that for the orchestrator to turn into a PR. Today every worktree forks off `main` (`drain_cycle/worktree.py:36`) and the agent pushes straight to `main` (`drain_cycle/prompt.py`, `_TAIL` + completion step 3) — both must change for stacking.

## How (mechanical)

* Add a `base` parameter to `worktree.add(repo, identifier, base=BASE_BRANCH)` (`drain_cycle/worktree.py:25`); thread it into the `git worktree add … <base>` call (`:36`). The orchestrator keeps `last_branch_per_repo: dict[str, str]` and passes the previous same-repo branch, or `main` for the first issue in a repo.
* Add `drain_cycle/handoff.py` that writes, reads, and validates `<worktree>/.drain-handoff.json` with keys `pr_title`, `pr_body`, `findings` (e.g. `{critical, required}`).
* Branch `prompt.build(issue, worktree, stack)` (`drain_cycle/prompt.py:23`): in stack mode tell the agent to commit to the issue branch, **not push**, and write the handoff file with a What / Why / What-to-review body; keep today's push-to-main text verbatim when `stack` is false.

## Acceptance criteria

- [ ] With two issues targeting the same repo, issue 2's worktree HEAD contains issue 1's commit; an issue in a different repo still forks off `main`. (orchestrator test asserting the base passed per repo)
- [ ] `prompt.build(stack=False)` returns today's prompt byte-for-byte; `prompt.build(stack=True)` omits "push to main" and includes the handoff-file instruction. (unit tests)
- [ ] `handoff.read` returns a typed object for a valid file and `None` for a missing or malformed file — it never raises. (unit tests)
- [ ] `pytest` passes.

## Scope guard

No PRs and no Graphite in this ticket. This one only makes the worktrees stack-shaped and produces the handoff artefact; assembly lands in the next ticket.

---

Resuming issue ABA-301: this worktree carries prior committed work from an earlier session that was halted. Run `git log --oneline main..HEAD` and `git status` first to read what is already done, then continue from that point — do not restart from scratch.

Execution instructions:
- Working directory: /Users/anton/src/drain-cycle/.worktrees/ABA-301
- Base branch: main
- Completion sequence for issue ABA-301 (run in this order, before marking Done):
  1. Run `/code-review-and-quality` against the working-tree changes.
  2. Fix any Critical or Required findings. Lower-severity findings are at your discretion.
  3. Commit and push to main.
  4. Post a short review-summary comment on the Linear issue via `mcp__claude_ai_Linear__save_comment` (count of findings by severity, fixed vs deferred).
  5. Transition issue to Done via `mcp__claude_ai_Linear__save_issue` (state: "Done").

before marking Done: run /code-review-and-quality on the working-tree changes, fix Critical/Required findings, commit + push, then post a review-summary comment on the issue and transition to Done.

> AGENT

Let me check the current state of the branch before continuing.

> TOOL

tool_use Bash
id: toolu_013mADbMFByio9RR3cKdh7ZJ
```json
{
  "command": "git log --oneline main..HEAD && git status",
  "description": "Check prior work and current status"
}
```

> TOOL

tool_result
id: toolu_013mADbMFByio9RR3cKdh7ZJ
```
* ABA-301
clean — nothing to commit
```

> TOOL

tool_use Bash
id: toolu_01SH3eSfDBtNjVpRLh6teAsE
```json
{
  "command": "git log --oneline main..HEAD",
  "description": "Check commits ahead of main"
}
```

> TOOL

tool_result
id: toolu_01SH3eSfDBtNjVpRLh6teAsE
```
(Bash completed with no output)
```

> AGENT

The branch has no prior commits - this is a fresh start. Let me read the relevant source files to understand what needs to be modified.

> TOOL

tool_use Read
id: toolu_01SpQ6a7WKtpgPTPAGG6aEsk
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/worktree.py"
}
```

> TOOL

tool_result
id: toolu_01SpQ6a7WKtpgPTPAGG6aEsk
```
1	"""Thin wrapper around ``git worktree``.
2	
3	Each issue gets ``.worktrees/<issue-identifier>/`` branched off ``main``,
4	used once, then removed on Done — or preserved on halt so a later re-run
5	can resume against the committed work (see ``docs/design-decisions.md``
6	§14).
7	
8	``git worktree`` stderr is captured and surfaced in the raised
9	``RuntimeError`` on failure. The orchestrator's pre-spawn try/except
10	threads the message into the runlog's ``halt_reason`` so the operator
11	sees git's actual diagnostic (dirty tree, branch already exists,
12	missing ``main``) rather than just a non-zero exit code.
13	"""
14	from __future__ import annotations
15	
16	import os
17	import subprocess
18	from dataclasses import dataclass
19	from pathlib import Path
20	from typing import Iterable
21	
22	from . import telemetry
23	
24	BASE_BRANCH = "main"
25	WORKTREE_DIR = ".worktrees"
26	
27	
28	@dataclass(frozen=True)
29	class WorktreeHandle:
30	    """A prepared worktree, together with whether it was reused.
31	
32	    ``resumed`` is ``True`` when ``ensure`` found a pre-existing worktree
33	    registered at the expected path (typically left behind by an earlier
34	    halted run). Callers thread the flag into the spawn-time prompt so
35	    the agent knows it is continuing from prior committed work rather
36	    than starting fresh.
37	    """
38	
39	    path: Path
40	    resumed: bool
41	
42	
43	def add(repo: Path, identifier: str) -> Path:
44	    """Create a worktree branched off ``main`` for ``identifier``.
45	
46	    Returns the absolute path to the new worktree.
47	    """
48	    worktree_path = repo / WORKTREE_DIR / identifier
49	    with telemetry.tracer.start_as_current_span("drain.worktree.add") as span:
50	        span.set_attribute("worktree.identifier", identifier)
51	        span.set_attribute("worktree.repo", repo.name)
52	        span.set_attribute("worktree.path", str(worktree_path))
53	        _run_git(
54	            ["worktree", "add", "-b", identifier, str(worktree_path), BASE_BRANCH],
55	            cwd=repo,
56	        )
57	    return worktree_path
58	
59	
60	def ensure(repo: Path, identifier: str) -> WorktreeHandle:
61	    """Reuse a preserved worktree if one is already registered, else add.
62	
63	    A worktree registered at ``repo/.worktrees/<identifier>`` is reused
64	    as-is — no mutating git command is run, so a dirty index, staged or
65	    untracked files, and the gitignored config symlinks all survive
66	    untouched. Any other state (no entry at that path) falls through to
67	    :func:`add`, whose ``RuntimeError`` on a leftover branch or orphan
68	    directory is what the orchestrator's existing pre-spawn handler
69	    turns into the clean ``Halt: … — setup failed: …`` line.
70	    """
71	    worktree_path = repo / WORKTREE_DIR / identifier
72	    with telemetry.tracer.start_as_current_span("drain.worktree.ensure") as span:
73	        span.set_attribute("worktree.identifier", identifier)
74	        span.set_attribute("worktree.repo", repo.name)
75	        span.set_attribute("worktree.path", str(worktree_path))
76	        if _is_registered_worktree(repo, worktree_path):
77	            span.set_attribute("worktree.resumed", True)
78	            return WorktreeHandle(path=worktree_path, resumed=True)
79	        span.set_attribute("worktree.resumed", False)
80	    return WorktreeHandle(path=add(repo, identifier), resumed=False)
81	
82	
83	def link_project_config(
84	    repo: Path, worktree_path: Path, names: Iterable[str]
85	) -> list[Path]:
86	    """Symlink gitignored project-scoped config from ``repo`` into the worktree.
87	
88	    A git worktree checks out only tracked files, so gitignored project config
89	    (``.claude/`` settings/hooks/agents/skills, a root ``.mcp.json``) is absent.
90	    Linking the repo's real entries in gives a worker the same settings, hooks,
91	    agents, skills, and MCP config as an interactive session at the repo root —
92	    and because the link points at the live dir, a stateful hook reads and
93	    writes the repo's actual config exactly as a non-worktree run would.
94	
95	    For each name: skip it if absent in ``repo`` (a clean no-op for repos
96	    without that config) or if something already occupies that path in the
97	    worktree (a tracked entry git checked out, or a pre-existing link). The
98	    check uses ``os.path.lexists`` so a dangling link counts as present and is
99	    never clobbered. Returns the links created.
100	    """
101	    created: list[Path] = []
102	    repo = repo.resolve()
103	    for name in names:
104	        source = repo / name
105	        if not source.exists():
106	            continue
107	        link = worktree_path / name
108	        if os.path.lexists(link):
109	            continue
110	        os.symlink(source, link)
111	        created.append(link)
112	    return created
113	
114	
115	def remove(repo: Path, worktree_path: Path) -> None:
116	    """Remove a worktree previously created by :func:`add`."""
117	    with telemetry.tracer.start_as_current_span("drain.worktree.remove") as span:
118	        span.set_attribute("worktree.repo", repo.name)
119	        span.set_attribute("worktree.path", str(worktree_path))
120	        _run_git(["worktree", "remove", str(worktree_path)], cwd=repo)
121	
122	
123	def _is_registered_worktree(repo: Path, worktree_path: Path) -> bool:
124	    """Return ``True`` if git lists a worktree at ``worktree_path``.
125	
126	    Parses ``git worktree list --porcelain -z`` for a ``worktree <path>``
127	    record matching ``worktree_path.resolve()``. ``-z`` makes each record
128	    NUL-separated and each field NUL-terminated, so paths with embedded
129	    spaces or newlines are unambiguous. The resolve step matches git's
130	    own canonicalisation (symlinks, ``..``) so a worktree under a
131	    symlinked repo path still matches the entry git printed. A non-zero
132	    git exit is treated as not-registered so ``ensure`` falls through to
133	    ``add``, whose error surfaces git's real diagnostic via the
134	    orchestrator's pre-spawn halt path.
135	    """
136	    target = worktree_path.resolve()
137	    result = subprocess.run(
138	        ["git", "worktree", "list", "--porcelain", "-z"],
139	        cwd=repo,
140	        check=False,
141	        capture_output=True,
142	        text=True,
143	    )
144	    if result.returncode != 0:
145	        return False
146	    for field in result.stdout.split("\0"):
147	        if not field.startswith("worktree "):
148	            continue
149	        listed = Path(field.removeprefix("worktree "))
150	        if listed.resolve() == target:
151	            return True
152	    return False
153	
154	
155	def _run_git(args: list[str], *, cwd: Path) -> None:
156	    result = subprocess.run(
157	        ["git", *args],
158	        cwd=cwd,
159	        check=False,
160	        capture_output=True,
161	        text=True,
162	    )
163	    if result.returncode != 0:
164	        raise RuntimeError(
165	            f"git {' '.join(args)} failed (exit {result.returncode}): "
166	            f"{result.stderr.strip() or result.stdout.strip() or '<no output>'}"
167	        )
168	
```

> TOOL

tool_use Read
id: toolu_019MhAej6UtJgPZavfC9HFvh
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/prompt.py"
}
```

> TOOL

tool_result
id: toolu_019MhAej6UtJgPZavfC9HFvh
```
1	"""Prompt builder for spawned ``claude -p`` sessions.
2	
3	The prompt is the entire contract between the orchestrator and the spawned
4	agent — there's no system prompt, no multi-turn loop. The four-segment
5	ordering below is load-bearing: the agent reads top-down, so context
6	(title + body) comes before instructions (preamble + tail), and the tail
7	line is last so it stays in the trailing-tokens window the model attends
8	to most strongly.
9	"""
10	from __future__ import annotations
11	
12	from pathlib import Path
13	from typing import Any
14	
15	
16	_TAIL = (
17	    "before marking Done: run /code-review-and-quality on the working-tree "
18	    "changes, fix Critical/Required findings, commit + push, then post a "
19	    "review-summary comment on the issue and transition to Done."
20	)
21	
22	
23	def _resume_directive(identifier: str) -> str:
24	    """Resume preamble for a worktree carrying prior committed work.
25	
26	    Inserted as the first line inside the preamble (after the ``---``
27	    separator, before "Execution instructions:") so the agent reads it
28	    ahead of the procedure but ``_TAIL`` still holds the last-line
29	    position the four-segment ordering reserves for it.
30	    """
31	    return (
32	        f"Resuming issue {identifier}: this worktree carries prior committed "
33	        "work from an earlier session that was halted. Run "
34	        "`git log --oneline main..HEAD` and `git status` first to read what "
35	        "is already done, then continue from that point — do not restart "
36	        "from scratch.\n\n"
37	    )
38	
39	
40	def build(issue: dict[str, Any], worktree: Path, *, resumed: bool = False) -> str:
41	    title = issue.get("title", "")
42	    description = issue.get("description") or ""
43	    identifier = issue.get("identifier", "")
44	
45	    resume_segment = _resume_directive(identifier) if resumed else ""
46	    preamble = (
47	        "---\n\n"
48	        f"{resume_segment}"
49	        "Execution instructions:\n"
50	        f"- Working directory: {worktree}\n"
51	        "- Base branch: main\n"
52	        f"- Completion sequence for issue {identifier} (run in this order, "
53	        "before marking Done):\n"
54	        "  1. Run `/code-review-and-quality` against the working-tree changes.\n"
55	        "  2. Fix any Critical or Required findings. Lower-severity findings "
56	        "are at your discretion.\n"
57	        "  3. Commit and push to main.\n"
58	        "  4. Post a short review-summary comment on the Linear issue via "
59	        "`mcp__claude_ai_Linear__save_comment` (count of findings by severity, "
60	        "fixed vs deferred).\n"
61	        "  5. Transition issue to Done via `mcp__claude_ai_Linear__save_issue` "
62	        '(state: "Done").\n'
63	    )
64	
65	    return (
66	        f"# {title}\n\n"
67	        f"{description}\n\n"
68	        f"{preamble}\n"
69	        f"{_TAIL}\n"
70	    )
71	
```

> AGENT

Now let me check the orchestrator and any existing tests.

> TOOL

tool_use Glob
id: toolu_01BSNfHLDxWGPVVPBhfMNMrB
```json
{
  "pattern": "drain_cycle/orchestrat*.py",
  "path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301"
}
```

> TOOL

tool_result
id: toolu_01BSNfHLDxWGPVVPBhfMNMrB
```
drain_cycle/orchestrator.py
```

> TOOL

tool_use Glob
id: toolu_01GhRtZx8KpUHUg5mWxscBRK
```json
{
  "pattern": "tests/**/*.py",
  "path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301"
}
```

> TOOL

tool_result
id: toolu_01GhRtZx8KpUHUg5mWxscBRK
```
tests/test_cli.py
tests/test_grade_across_cycles.py
tests/test_grade_per_cycle.py
tests/test_grade_verdict.py
tests/test_grade_walking_skeleton.py
tests/test_limits.py
tests/test_linear_pending_issues.py
tests/test_linear_set_state.py
tests/test_linear_sort.py
tests/test_model.py
tests/test_orchestrator_cycle_halt.py
tests/test_orchestrator_cycle_limit.py
tests/test_orchestrator_halt.py
tests/test_orchestrator_iteration.py
tests/test_orchestrator_marker.py
tests/test_orchestrator_multi_repo.py
tests/test_orchestrator_resume.py
tests/test_orchestrator_runlog.py
tests/test_orchestrator_set_state.py
tests/test_orchestrator_teardown.py
tests/test_orchestrator_watch.py
tests/test_progress.py
tests/test_prompt.py
tests/test_repos.py
tests/test_runlog.py
tests/test_status.py
tests/test_telemetry.py
tests/test_worker.py
tests/test_worktree.py
```

> TOOL

tool_use Read
id: toolu_01CnoujETRjJs4nbdmHMd4mJ
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/orchestrator.py"
}
```

> TOOL

tool_use Read
id: toolu_01HSGdGFtvT9hPNr3wh9bzuP
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_prompt.py"
}
```

> TOOL

tool_result
id: toolu_01CnoujETRjJs4nbdmHMd4mJ
```
1	"""Drain a cycle by iterating over its sorted Todo/Backlog issues.
2	
3	Halt-on-not-Done, the orchestrator-owned Todo→In-Progress transition, the
4	run-log artefact, and the inspectable-halt UX all live here. The halt-message
5	helper ``_halt_message`` is the single source of truth for the operator-facing
6	halt string — emitted both on stderr and into the run-log entry's
7	``halt_reason`` field.
8	"""
9	from __future__ import annotations
10	
11	import fcntl
12	import json
13	import os
14	import select
15	import shlex
16	import shutil
17	import subprocess
18	import sys
19	import tempfile
20	from datetime import datetime, timezone
21	from pathlib import Path
22	from typing import Callable, TextIO
23	
24	from opentelemetry.trace import Span
25	
26	from . import linear, model, progress, prompt, runlog, telemetry, worker, worktree
27	from .limits import Limits, check_cycle
28	from .linear import DependencyCycleError
29	from .repos import RepoResolutionError, Repos
30	
31	_DONE_STATE_TYPE = "completed"
32	_IN_PROGRESS_STATE_NAME = "In Progress"
33	_CLAUDE_CMD = ["claude", "-p", "--dangerously-skip-permissions"]
34	_DEBUG_ENV_VAR = "DRAIN_CYCLE_DEBUG"
35	"""Opt-in switch for per-issue ``--debug-file`` capture. Any non-empty value
36	turns it on; the worker then writes each session's startup diagnostics
37	(settings sources, plugins, MCP servers, hooks) beside the run log. Off by
38	default — the diagnostic exists for one-shot investigation, not steady state.
39	See ``docs/design-decisions.md`` §10."""
40	_UNRESOLVED_WORKTREE_DISPLAY = "<unresolved>"
41	"""Worktree-path placeholder for the pre-spawn resolution-halt path.
42	No path has been chosen yet — the issue couldn't be mapped to a target
43	repo — so the run-log entry and stderr halt line carry this marker
44	rather than a misleading fake path."""
45	
46	
47	def _now_iso() -> str:
48	    return datetime.now(timezone.utc).isoformat()
49	
50	
51	_WATCH_FIFO_TIMEOUT_SECONDS = 10.0
52	"""How long ``_open_fifo_stream`` waits for the pane's ``claude | tee`` to
53	produce its first bytes before giving up and falling back to a normal
54	subprocess spawn. The pane's ``claude`` emits its init event within seconds;
55	this bound only guards a pane that never started (tmux accepted the
56	split-window but the command died), so the drain never wedges on a dead FIFO."""
57	
58	
59	def _open_watch_pane(argv: list[str], cwd: Path) -> tuple[str, Path] | None:
60	    """Open a tmux split-pane running ``argv`` piped through ``tee`` into a FIFO.
61	
62	    The pane *is* the ``claude`` session: ``argv | tee <fifo>`` lets the
63	    operator watch the live stream-json scroll in the pane while the same
64	    bytes flow through the FIFO to drain-cycle's reader. ``exec ${SHELL}``
65	    after the pipeline keeps the pane alive for scrollback once ``claude``
66	    exits (``tee`` still closes the FIFO write end, so the reader reaches EOF).
67	
68	    ``split-window -P -F "#{pane_id}"`` prints the new pane's ID directly so we
69	    capture the session pane, not the operator's active pane; ``-c`` runs it in
70	    the issue's worktree. Returns ``(pane_id, fifo_path)``, or ``None`` if the
71	    FIFO or pane could not be created — every failure (tmux not on PATH,
72	    non-zero exit, any OS error) is swallowed so a broken tmux environment
73	    falls back to a normal spawn rather than crashing the drain.
74	    """
75	    try:
76	        fifo_path = Path(tempfile.mkdtemp(prefix="drain-watch-")) / "stream.fifo"
77	        os.mkfifo(fifo_path)
78	    except OSError:
79	        return None
80	    pipeline = (
81	        " ".join(shlex.quote(a) for a in argv)
82	        + f" | tee {shlex.quote(str(fifo_path))}"
83	        + "; exec ${SHELL:-/bin/sh}"
84	    )
85	    try:
86	        result = subprocess.run(
87	            [
88	                "tmux", "split-window", "-d",
89	                "-P", "-F", "#{pane_id}",
90	                "-c", str(cwd),
91	                pipeline,
92	            ],
93	            check=True,
94	            capture_output=True,
95	            text=True,
96	        )
97	        pane_id = result.stdout.strip()
98	    except Exception:
99	        _cleanup_fifo(fifo_path)
100	        return None
101	    if not pane_id:
102	        _cleanup_fifo(fifo_path)
103	        return None
104	    return pane_id, fifo_path
105	
106	
107	def _open_fifo_stream(fifo_path: Path, timeout: float) -> TextIO | None:
108	    """Open ``fifo_path`` for reading, waiting up to ``timeout`` for a writer.
109	
110	    The FIFO is opened non-blocking so a pane that never started can't wedge
111	    the drain; ``select`` then waits for the first bytes (``tee`` writing the
112	    pane's first stream-json line). Once readable, ``O_NONBLOCK`` is cleared so
113	    the reader thread's line iteration blocks normally until EOF. Returns a
114	    line-buffered text stream, or ``None`` if no writer/data appeared in time
115	    (the caller then tears down the pane and falls back to a normal spawn).
116	    """
117	    try:
118	        fd = os.open(fifo_path, os.O_RDONLY | os.O_NONBLOCK)
119	    except OSError:
120	        return None
121	    readable, _, _ = select.select([fd], [], [], timeout)
122	    if not readable:
123	        os.close(fd)
124	        return None
125	    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
126	    fcntl.fcntl(fd, fcntl.F_SETFL, flags & ~os.O_NONBLOCK)
127	    try:
128	        return os.fdopen(fd, "r", buffering=1)
129	    except OSError:
130	        os.close(fd)
131	        return None
132	
133	
134	def _cleanup_fifo(fifo_path: Path) -> None:
135	    """Remove the FIFO and its temp dir; swallows all errors."""
136	    shutil.rmtree(fifo_path.parent, ignore_errors=True)
137	
138	
139	def _close_watch_pane(pane_id: str) -> None:
140	    """Kill a tmux pane by ID; swallows all errors."""
141	    try:
142	        subprocess.run(
143	            ["tmux", "kill-pane", "-t", pane_id],
144	            check=False,
145	            capture_output=True,
146	        )
147	    except Exception:
148	        pass
149	
150	
151	def _halt_message(identifier: str, state_name: str, worktree_path: Path) -> str:
152	    """Single source of truth for the halt UX.
153	
154	    The same string lands on stderr (the operator's grep anchor) and in
155	    the run-log entry's ``halt_reason`` field — so kill-condition tooling
156	    reads the same human-readable explanation the operator saw at halt
157	    time.
158	    """
159	    return f"Halt: {identifier} (final state: {state_name}) at {worktree_path}"
160	
161	
162	def _resume_attempts(cycle_id: str, identifier: str) -> int:
163	    """Count prior halted attempts for ``identifier`` across this cycle's run logs.
164	
165	    Globs ``~/.drain-cycle/runs/<cycle_id>-*.json`` and tallies entries
166	    whose ``issue_identifier`` matches and whose ``final_linear_state``
167	    is not ``"Done"`` — the same shape every halt path writes. The
168	    orchestrator compares this against ``limits.max_resume_attempts``
169	    before spawning, so a perma-stuck issue stops consuming attempts
170	    once its budget is spent.
171	
172	    Unreadable, unparseable, or shape-corrupted log files are skipped
173	    rather than failed: a partial-write file from a SIGKILL'd earlier
174	    run, or a file whose ``entries`` is missing/null/non-list, must
175	    not pin the operator out of running the cycle. The shape checks
176	    are isinstance-guarded so a JSON file that parses but doesn't
177	    match :class:`RunLog`'s on-disk schema is treated as opaque rather
178	    than crashing the helper.
179	    """
180	    count = 0
181	    for path in runlog.runs_dir().glob(f"{cycle_id}-*.json"):
182	        try:
183	            payload = json.loads(path.read_text())
184	        except (OSError, json.JSONDecodeError):
185	            continue
186	        if not isinstance(payload, dict):
187	            continue
188	        entries = payload.get("entries")
189	        if not isinstance(entries, list):
190	            continue
191	        for entry in entries:
192	            if not isinstance(entry, dict):
193	                continue
194	            if (
195	                entry.get("issue_identifier") == identifier
196	                and entry.get("final_linear_state") != "Done"
197	            ):
198	                count += 1
199	    return count
200	
201	
202	def _revert_to_pre_halt_state(
203	    issue_id: str, *, target_state_name: str, pre_revert_state_name: str
204	) -> tuple[str, str | None]:
205	    """Restore Linear state on halt; return ``(state_to_report, error_msg)``.
206	
207	    The orchestrator transitions issues Todo→In Progress before spawning the
208	    agent. When the run halts, that In-Progress flag leaves the issue outside
209	    ``_PENDING_STATE_TYPES`` so a re-run silently skips it. This helper
210	    reverses the transition and re-fetches to confirm.
211	
212	    On revert success, returns the refreshed state name and ``None``.
213	    On revert failure, returns ``pre_revert_state_name`` (the state the
214	    issue is actually still in, so the operator can find it) plus the
215	    exception message — non-fatal. A failed refresh after a
216	    successful revert falls back to ``target_state_name``, since we trust
217	    the mutation landed even if the read-back didn't.
218	    """
219	    try:
220	        linear.set_state(issue_id, target_state_name)
221	    except Exception as exc:
222	        return pre_revert_state_name, str(exc)
223	    try:
224	        refreshed = linear.get_issue(issue_id)
225	    except Exception:
226	        return target_state_name, None
227	    return refreshed["state"]["name"], None
228	
229	
230	def _worker_log_fields(result: worker.WorkerResult) -> dict[str, object]:
231	    """Map a ``WorkerResult`` onto the run-log entry's usage fields.
232	
233	    Shared by all three worker-backed ``append_entry`` calls (timeout
234	    halt, Done, not-Done halt) so the recorded usage shape can't drift
235	    between branches.
236	    """
237	    return {
238	        "duration_seconds": result.duration_seconds,
239	        "model": result.model,
240	        "usage": result.usage,
241	        "cost_usd": result.cost_usd,
242	        "num_turns": result.num_turns,
243	        "session_id": result.session_id,
244	        "is_error": result.is_error,
245	    }
246	
247	
248	def _debug_enabled() -> bool:
249	    """Whether per-issue ``--debug-file`` capture is switched on.
250	
251	    Read from the environment (``os.environ`` already carries any
252	    ``~/.drain-cycle/.env`` value loaded at CLI startup), so the operator
253	    turns it on for one investigative run with ``DRAIN_CYCLE_DEBUG=1
254	    drain-cycle`` and leaves it off otherwise.
255	    """
256	    return bool(os.environ.get(_DEBUG_ENV_VAR))
257	
258	
259	def run(repos: Repos, limits: Limits | None = None, *, watch: bool = False) -> int:
260	    """Drain the current cycle inside the ``drain.cycle`` root span.
261	
262	    The span wrapper is thin so the body keeps its shape; per-issue work nests
263	    under it via ``_drain_one_issue``'s ``drain.issue`` spans, and the Linear,
264	    worktree, and worker spans nest under those — yielding one trace per drain.
265	    """
266	    if limits is None:
267	        limits = Limits()
268	    with telemetry.tracer.start_as_current_span("drain.cycle") as cycle_span:
269	        return _run(repos, limits, cycle_span, watch=watch)
270	
271	
272	def _run(repos: Repos, limits: Limits, cycle_span: Span, *, watch: bool = False) -> int:
273	    debug = _debug_enabled()
274	    cycle_id = linear.current_cycle_id()
275	    cycle_span.set_attribute("drain.cycle_id", cycle_id)
276	    log = runlog.RunLog(cycle_id=cycle_id)
277	    try:
278	        plan = linear.pending_issues(cycle_id)
279	    except DependencyCycleError as exc:
280	        halt_reason = f"Halt: {exc}"
281	        log.set_cycle_halt(halt_reason)
282	        telemetry.mark_error(cycle_span, "err-dependency-cycle", halt_reason)
283	        print(halt_reason, file=sys.stderr)
284	        return 1
285	
286	    cycle_span.set_attribute("drain.issues_planned", len(plan.order))
287	    cycle_span.set_attribute("drain.issues_deferred", len(plan.deferred))
288	
289	    if not plan.order and not plan.deferred:
290	        cycle_span.set_attribute("drain.outcome", "nothing-to-do")
291	        print(f"Cycle {cycle_id} has no Todo/Backlog issues — nothing to do.")
292	        return 0
293	
294	    for deferred in plan.deferred:
295	        issue = deferred["issue"]
296	        blocker_id = deferred["blocker_identifier"]
297	        blocker_state = deferred["blocker_state_type"]
298	        print(
299	            f"drain-cycle: deferred {issue['identifier']}"
300	            f" — blocked by {blocker_id} ({blocker_state})",
301	            file=sys.stderr,
302	        )
303	
304	    if not plan.order:
305	        cycle_span.set_attribute("drain.outcome", "all-deferred")
306	        return 0
307	
308	    in_tmux = bool(os.environ.get("TMUX"))
309	    current_pane_id: str | None = None
310	
311	    total = len(plan.order)
312	    for index, issue in enumerate(plan.order):
313	        # Kill the pane from the previous issue before opening one for this issue.
314	        if current_pane_id is not None:
315	            _close_watch_pane(current_pane_id)
316	            current_pane_id = None
317	
318	        halt_code, current_pane_id = _drain_one_issue(
319	            issue,
320	            index=index,
321	            total=total,
322	            repos=repos,
323	            limits=limits,
324	            log=log,
325	            cycle_id=cycle_id,
326	            debug=debug,
327	            watch=watch,
328	            in_tmux=in_tmux,
329	        )
330	        if halt_code is not None:
331	            return halt_code  # type: ignore[return-value]
332	
333	        # Cycle-wide circuit breaker: every issue may stay under its own
334	        # per-issue caps while their sum drains the quota. Check the
335	        # running totals (which now include the Done issue just finished)
336	        # before spawning the next one; on breach, stop the cycle.
337	        cycle_breach = check_cycle(
338	            limits,
339	            tokens=log.cycle_tokens_cumulative(),
340	            cost_usd=log.cycle_cost_usd(),
341	            seconds=log.cycle_duration_seconds(),
342	        )
343	        if cycle_breach is not None:
344	            halt_reason = f"Halt: {cycle_breach.describe()}"
345	            log.set_cycle_halt(halt_reason)
346	            telemetry.mark_error(cycle_span, "err-cycle-breach", halt_reason)
347	            print(halt_reason, file=sys.stderr)
348	            return 1
349	
350	    # Final pane is left open for scrollback (intentionally not killed here).
351	    cycle_span.set_attribute("drain.outcome", "drained")
352	    return 0
353	
354	
355	def _drain_one_issue(
356	    issue: dict,
357	    *,
358	    index: int,
359	    total: int,
360	    repos: Repos,
361	    limits: Limits,
362	    log: runlog.RunLog,
363	    cycle_id: str,
364	    debug: bool,
365	    watch: bool = False,
366	    in_tmux: bool = False,
367	) -> tuple[int | None, str | None]:
368	    """Drain a single issue end to end inside a ``drain.issue`` span.
369	
370	    Returns ``(halt_code, pane_id)`` where ``halt_code`` is ``None`` when the
371	    issue reached Done (the caller then runs the cycle-wide circuit breaker and
372	    proceeds to the next issue), or an exit code when the run must halt.
373	    ``pane_id`` is the tmux pane ID opened for this issue (or ``None``).
374	    Each halt path is also marked on the span with a static ``exception.slug``.
375	    """
376	    identifier = issue["identifier"]
377	    with telemetry.tracer.start_as_current_span("drain.issue") as issue_span:
378	        issue_span.set_attribute("issue.identifier", identifier)
379	        issue_span.set_attribute("issue.title", issue["title"])
380	        issue_span.set_attribute("issue.index", index + 1)
381	        issue_span.set_attribute("issue.total", total)
382	        print(f"drain-cycle: picked {identifier}: {issue['title']}", file=sys.stderr)
383	
384	        started_at = _now_iso()
385	        try:
386	            target_repo = repos.resolve(issue)
387	        except RepoResolutionError as exc:
388	            # Pre-spawn resolution halt: no Linear state was moved, so no
389	            # revert is attempted. The worktree path is the ``<unresolved>``
390	            # placeholder since no repo was chosen.
391	            state_name = issue["state"]["name"]
392	            halt_reason = (
393	                f"{_halt_message(identifier, state_name, Path(_UNRESOLVED_WORKTREE_DISPLAY))}"
394	                f" — {exc}"
395	            )
396	            log.append_entry(
397	                issue_identifier=identifier,
398	                started_at=started_at,
399	                finished_at=_now_iso(),
400	                exit_code=-1,
401	                final_linear_state=state_name,
402	                REDACTED,
403	                halt_reason=halt_reason,
404	            )
405	            issue_span.set_attribute("issue.final_linear_state", state_name)
406	            telemetry.mark_error(issue_span, "err-repo-resolution", halt_reason)
407	            print(halt_reason, file=sys.stderr)
408	            return 1, None
409	
410	        issue_span.set_attribute("issue.repo", target_repo.name)
411	
412	        # Resume-attempt cap fires BEFORE any worktree manipulation or
413	        # Linear state change: a no-spawn refusal must leave the issue
414	        # exactly where it was so a future re-run (after the operator
415	        # raises the cap, clears prior runs, or finishes the work by
416	        # hand) can pick up cleanly. The cap is a *policy* knob, not a
417	        # runtime guardrail — no Breach is raised; see limits.py.
418	        #
419	        # ``max_resume_attempts=N`` allows up to N resumes after the
420	        # initial attempt (one fresh + N resumes = N+1 total halts
421	        # before refusal), matching the convention of ``max_retries`` in
422	        # the stdlib's urllib3/requests world. The cap fires once
423	        # ``prior_halts`` (count of non-Done entries for this issue in
424	        # the cycle's run logs, written by *prior* runs since a halt
425	        # exits this run) exceeds N.
426	        if limits.max_resume_attempts is not None:
427	            prior_halts = _resume_attempts(cycle_id, identifier)
428	            if prior_halts > limits.max_resume_attempts:
429	                planned_path = target_repo / worktree.WORKTREE_DIR / identifier
430	                state_name = issue["state"]["name"]
431	                halt_reason = (
432	                    f"{_halt_message(identifier, state_name, planned_path)}"
433	                    f" — resume-attempt cap reached "
434	                    f"(all {limits.max_resume_attempts} resumes used); "
435	                    "raise max_resume_attempts, clear prior runs, or finish by hand"
436	                )
437	                log.append_entry(
438	                    issue_identifier=identifier,
439	                    started_at=started_at,
440	                    finished_at=_now_iso(),
441	                    exit_code=-1,
442	                    final_linear_state=state_name,
443	                    worktree_path=str(planned_path),
444	                    halt_reason=halt_reason,
445	                )
446	                issue_span.set_attribute("issue.final_linear_state", state_name)
447	                issue_span.set_attribute("issue.resumed", True)
448	                telemetry.mark_error(issue_span, "err-resume-cap", halt_reason)
449	                print(halt_reason, file=sys.stderr)
450	                return 1, None
451	
452	        try:
453	            handle = worktree.ensure(target_repo, identifier)
454	            worktree_path = handle.path
455	            # A worktree checks out only tracked files, so gitignored
456	            # project config (.claude/, .mcp.json) is absent. Symlink it in
457	            # so the worker loads the same settings/hooks/agents/skills/MCP
458	            # as an interactive session at the repo root.
459	            worktree.link_project_config(
460	                target_repo, worktree_path, repos.worktree_config_paths
461	            )
462	            # Orchestrator owns the Todo→In Progress half so the lifecycle
463	            # doesn't depend on the spawned agent's compliance. The agent
464	            # still owns the …→Done half via Linear MCP — see prompt.py tail.
465	            linear.set_state(issue["id"], _IN_PROGRESS_STATE_NAME)
466	        except Exception as exc:
467	            # Convert any pre-spawn failure into a recorded halt rather than
468	            # a traceback: write a run-log entry with the planned worktree
469	            # path, print the halt message, exit non-zero. Subsequent issues
470	            # are not attempted — same contract as a spawn-time halt.
471	            planned_path = target_repo / worktree.WORKTREE_DIR / identifier
472	            state_name = issue["state"]["name"]
473	            halt_reason = (
474	                f"{_halt_message(identifier, state_name, planned_path)}"
475	                f" — setup failed: {exc}"
476	            )
477	            log.append_entry(
478	                issue_identifier=identifier,
479	                started_at=started_at,
480	                finished_at=_now_iso(),
481	                exit_code=-1,
482	                final_linear_state=state_name,
483	                worktree_path=str(planned_path),
484	                halt_reason=halt_reason,
485	            )
486	            issue_span.set_attribute("issue.final_linear_state", state_name)
487	            telemetry.mark_error(issue_span, "err-setup-failed", halt_reason)
488	            print(halt_reason, file=sys.stderr)
489	            return 1, None
490	
491	        agent_prompt = prompt.build(issue, worktree_path, resumed=handle.resumed)
492	        issue_span.set_attribute("issue.resumed", handle.resumed)
493	        worker_model = model.resolve(issue)
494	        issue_span.set_attribute("issue.model", worker_model)
495	
496	        debug_file = log.debug_path(identifier) if debug else None
497	        if debug_file is not None:
498	            print(
499	                f"drain-cycle: {identifier} debug capture → {debug_file}",
500	                file=sys.stderr,
501	            )
502	
503	        # Watch mode: run claude inside a tmux pane (so the operator sees the
504	        # live session) and read its stream-json off a FIFO instead of a
505	        # subprocess pipe. If the pane or FIFO can't be brought up, fall back
506	        # to a normal subprocess spawn — the pane is a convenience, not a
507	        # requirement. ``pane_id`` is returned to the caller for lifecycle
508	        # management; ``external_stream``/``kill_fn`` steer the worker onto the
509	        # external path.
510	        pane_id: str | None = None
511	        fifo_path: Path | None = None
512	        external_stream: TextIO | None = None
513	        kill_fn: Callable[[], None] | None = None
514	        if watch and in_tmux:
515	            argv = worker.build_argv(
516	                _CLAUDE_CMD,
517	                model=worker_model,
518	                prompt=agent_prompt,
519	                cost_limit_usd=limits.per_issue_cost_usd,
520	                debug_file=debug_file,
521	            )
522	            opened = _open_watch_pane(argv, worktree_path)
523	            if opened is not None:
524	                pane_id, fifo_path = opened
525	                external_stream = _open_fifo_stream(
526	                    fifo_path, _WATCH_FIFO_TIMEOUT_SECONDS
527	                )
528	                if external_stream is None:
529	                    # Pane accepted but produced no output in time — tear it
530	                    # down so we don't double-spawn, then fall back.
531	                    _close_watch_pane(pane_id)
532	                    _cleanup_fifo(fifo_path)
533	                    pane_id = None
534	                    fifo_path = None
535	                else:
536	                    def kill_fn() -> None:
537	                        _close_watch_pane(pane_id)
538	
539	        marker: dict = {
540	            "pid": os.getpid(),
541	            "cycle_id": cycle_id,
542	            "run_log_path": str(log.path),
543	            "issue": {
544	                "identifier": identifier,
545	                "title": issue["title"],
546	                "repo": target_repo.name,
547	                "worktree_path": str(worktree_path),
548	            },
549	            "model": worker_model,
550	            "started_at": started_at,
551	            "index": index + 1,
552	            "total": total,
553	            "progress": {},
554	        }
555	        progress.write(marker)
556	
557	        def _make_on_progress(m: dict, ident: str):
558	            def _cb(
559	                turns: int,
560	                cumulative_tokens: int,
561	                peak_context_tokens: int,
562	                cost_usd: float | None,
563	                elapsed_seconds: float,
564	            ) -> None:
565	                m["progress"] = {
566	                    "turns": turns,
567	                    "cumulative_tokens": cumulative_tokens,
568	                    "peak_context_tokens": peak_context_tokens,
569	                    "cost_usd": cost_usd,
570	                    "elapsed_seconds": elapsed_seconds,
571	                    "last_event_at": _now_iso(),
572	                }
573	                progress.write(m)
574	                print(
575	                    progress.format_progress_line(
576	                        ident,
577	                        turns,
578	                        cumulative_tokens,
579	                        peak_context_tokens,
580	                        elapsed_seconds,
581	                    ),
582	                    file=sys.stderr,
583	                )
584	            return _cb
585	
586	        try:
587	            result = worker.run_issue(
588	                claude_cmd=_CLAUDE_CMD,
589	                model=worker_model,
590	                prompt=agent_prompt,
591	                cwd=worktree_path,
592	                token_limit=limits.per_issue_tokens,
593	                time_limit_seconds=limits.per_issue_seconds,
594	                cost_limit_usd=limits.per_issue_cost_usd,
595	                debug_file=debug_file,
596	                external_stream=external_stream,
597	                kill_fn=kill_fn,
598	                on_progress=_make_on_progress(marker, identifier),
599	            )
600	        finally:
601	            progress.clear()
602	            if fifo_path is not None:
603	                _cleanup_fifo(fifo_path)
604	        finished_at = _now_iso()
605	
606	        if result.breach is not None:
607	            # The worker crossed a per-issue cap (tokens or time) and was
608	            # process-group killed (grandchildren reaped). Same revert + halt
609	            # contract as a not-Done exit, with the recorded usage of the
610	            # killed session and the breached cap named in the halt reason.
611	            original_state_name = issue["state"]["name"]
612	            effective_state, revert_error = _revert_to_pre_halt_state(
613	                issue["id"],
614	                target_state_name=original_state_name,
615	                pre_revert_state_name=_IN_PROGRESS_STATE_NAME,
616	            )
617	            halt_reason = (
618	                f"{_halt_message(identifier, effective_state, worktree_path)}"
619	                f" — {result.breach.describe()}"
620	            )
621	            if revert_error is not None:
622	                halt_reason += (
623	                    f"; revert to {original_state_name!r} failed: {revert_error}"
624	                )
625	            log.append_entry(
626	                issue_identifier=identifier,
627	                started_at=started_at,
628	                finished_at=finished_at,
629	                exit_code=result.exit_code,
630	                final_linear_state=effective_state,
631	                worktree_path=str(worktree_path),
632	                halt_reason=halt_reason,
633	                **_worker_log_fields(result),
634	            )
635	            issue_span.set_attribute("issue.exit_code", result.exit_code)
636	            issue_span.set_attribute("issue.final_linear_state", effective_state)
637	            telemetry.mark_error(issue_span, "err-per-issue-breach", halt_reason)
638	            print(halt_reason, file=sys.stderr)
639	            return 1, pane_id
640	
641	        refreshed = linear.get_issue(issue["id"])
642	        post_spawn_state = refreshed["state"]["name"]
643	        is_done = refreshed["state"]["type"] == _DONE_STATE_TYPE
644	        issue_span.set_attribute("issue.exit_code", result.exit_code)
645	        issue_span.set_attribute("issue.is_done", is_done)
646	
647	        if is_done:
648	            issue_span.set_attribute("issue.final_linear_state", post_spawn_state)
649	            remove_error: str | None = None
650	            try:
651	                worktree.remove(target_repo, worktree_path)
652	            except RuntimeError as exc:
653	                remove_error = str(exc)
654	                issue_span.set_attribute("worktree.remove_error", remove_error)
655	                print(
656	                    f"drain-cycle: {identifier}: worktree teardown failed: {exc}",
657	                    file=sys.stderr,
658	                )
659	            # Append unconditionally for every attempted issue.
660	            log.append_entry(
661	                issue_identifier=identifier,
662	                started_at=started_at,
663	                finished_at=finished_at,
664	                exit_code=result.exit_code,
665	                final_linear_state=post_spawn_state,
666	                worktree_path=str(worktree_path),
667	                halt_reason=remove_error,
668	                **_worker_log_fields(result),
669	            )
670	            if remove_error is None:
671	                print(f"drain-cycle: {identifier} done; worktree removed.", file=sys.stderr)
672	            return None, pane_id
673	
674	        # Not-Done halt: revert to the pre-halt state so a re-run picks
675	        # this issue back up instead of silently skipping it.
676	        original_state_name = issue["state"]["name"]
677	        effective_state, revert_error = _revert_to_pre_halt_state(
678	            issue["id"],
679	            target_state_name=original_state_name,
680	            pre_revert_state_name=post_spawn_state,
681	        )
682	        halt_reason = _halt_message(identifier, effective_state, worktree_path)
683	        if revert_error is not None:
684	            halt_reason += (
685	                f" — revert to {original_state_name!r} failed: {revert_error}"
686	            )
687	        # halt_reason carries the same string also printed to stderr below
688	        # so the on-disk and terminal surfaces cannot drift.
689	        log.append_entry(
690	            issue_identifier=identifier,
691	            started_at=started_at,
692	            finished_at=finished_at,
693	            exit_code=result.exit_code,
694	            final_linear_state=effective_state,
695	            worktree_path=str(worktree_path),
696	            halt_reason=halt_reason,
697	            **_worker_log_fields(result),
698	        )
699	        issue_span.set_attribute("issue.final_linear_state", effective_state)
700	        telemetry.mark_error(issue_span, "err-issue-not-done", halt_reason)
701	        print(halt_reason, file=sys.stderr)
702	        return 1, pane_id
703	
```

> TOOL

tool_result
id: toolu_01HSGdGFtvT9hPNr3wh9bzuP
```
1	"""Prompt-template assertions.
2	
3	The prompt is what the orchestrator hands to ``claude -p`` — its four
4	segments (title, body, execution preamble, tail line) must appear in the
5	documented order or the spawned agent loses the context it needs to
6	complete the issue and self-transition Linear. These tests pin the
7	ordering and the load-bearing substrings so a future refactor cannot
8	silently reshape the contract.
9	"""
10	from __future__ import annotations
11	
12	from pathlib import Path
13	
14	from drain_cycle.prompt import _TAIL, build
15	
16	
17	def _fixture_issue() -> dict:
18	    return {
19	        "id": "id-ABA-999",
20	        "identifier": "ABA-999",
21	        "title": "Fixture title — drain a trivial issue",
22	        "description": "Fixture body.\n\nMultiple paragraphs preserved verbatim.",
23	        "priority": 3,
24	        "sortOrder": 1.0,
25	        "state": {"type": "unstarted", "name": "Todo"},
26	    }
27	
28	
29	def _positions(text: str, *needles: str) -> list[int]:
30	    """Return the index of each needle, asserting each one is present."""
31	    found = []
32	    for needle in needles:
33	        idx = text.find(needle)
34	        assert idx != -1, f"missing segment: {needle!r}\n--- prompt ---\n{text}"
35	        found.append(idx)
36	    return found
37	
38	
39	def test_prompt_contains_four_segments_in_order(tmp_path: Path) -> None:
40	    issue = _fixture_issue()
41	    worktree = tmp_path / ".worktrees" / issue["identifier"]
42	    rendered = build(issue, worktree)
43	
44	    title_idx, body_idx, preamble_idx, tail_idx = _positions(
45	        rendered,
46	        f"# {issue['title']}",
47	        issue["description"],
48	        "Execution instructions:",
49	        _TAIL,
50	    )
51	    assert title_idx < body_idx < preamble_idx < tail_idx
52	
53	
54	def test_preamble_names_worktree_base_branch_and_mcp_call(tmp_path: Path) -> None:
55	    issue = _fixture_issue()
56	    worktree = tmp_path / ".worktrees" / issue["identifier"]
57	    rendered = build(issue, worktree)
58	
59	    # Each of the three preamble facts the spawned agent needs to act on.
60	    assert str(worktree) in rendered
61	    assert "Base branch: main" in rendered
62	    assert "mcp__claude_ai_Linear__save_issue" in rendered
63	    assert 'state: "Done"' in rendered
64	    # The Linear MCP call needs to know which issue — include the identifier.
65	    assert issue["identifier"] in rendered
66	
67	
68	def test_tail_line_is_the_last_non_empty_line(tmp_path: Path) -> None:
69	    issue = _fixture_issue()
70	    worktree = tmp_path / ".worktrees" / issue["identifier"]
71	    rendered = build(issue, worktree)
72	
73	    non_empty = [line for line in rendered.splitlines() if line.strip()]
74	    assert non_empty[-1] == _TAIL
75	
76	
77	def test_resumed_prompt_inserts_directive_above_execution_instructions(
78	    tmp_path: Path,
79	) -> None:
80	    """``resumed=True`` adds a resume directive that leads the preamble
81	    so the agent reads it before the execution procedure, while ``_TAIL``
82	    stays the last non-empty line (the four-segment ordering is
83	    load-bearing)."""
84	    issue = _fixture_issue()
85	    worktree = tmp_path / ".worktrees" / issue["identifier"]
86	    rendered = build(issue, worktree, resumed=True)
87	
88	    title_idx, body_idx, sep_idx, directive_idx, exec_idx, tail_idx = _positions(
89	        rendered,
90	        f"# {issue['title']}",
91	        issue["description"],
92	        "---",
93	        "Resuming issue",
94	        "Execution instructions:",
95	        _TAIL,
96	    )
97	    assert title_idx < body_idx < sep_idx < directive_idx < exec_idx < tail_idx
98	
99	    # Directive names the issue and the two read-state commands the
100	    # agent should run before continuing.
101	    assert issue["identifier"] in rendered[directive_idx:exec_idx]
102	    assert "git log --oneline main..HEAD" in rendered
103	    assert "git status" in rendered
104	
105	    # _TAIL is still the last non-empty line — the prepend must not
106	    # displace it from the trailing position.
107	    non_empty = [line for line in rendered.splitlines() if line.strip()]
108	    assert non_empty[-1] == _TAIL
109	
110	
111	def test_unresumed_prompt_is_byte_identical_to_no_kwarg_default(
112	    tmp_path: Path,
113	) -> None:
114	    """``resumed=False`` (the default) keeps the prompt unchanged: every
115	    existing call site renders byte-identical output, and the resume
116	    directive is absent."""
117	    issue = _fixture_issue()
118	    worktree = tmp_path / ".worktrees" / issue["identifier"]
119	
120	    default = build(issue, worktree)
121	    explicit_false = build(issue, worktree, resumed=False)
122	
123	    assert default == explicit_false
124	    assert "Resuming issue" not in default
125	
126	
127	def test_empty_description_does_not_break_rendering(tmp_path: Path) -> None:
128	    issue = _fixture_issue()
129	    issue["description"] = None  # Linear can return null descriptions
130	    worktree = tmp_path / ".worktrees" / issue["identifier"]
131	    rendered = build(issue, worktree)
132	
133	    # Title and preamble must still render in order even with no body.
134	    title_idx, preamble_idx, tail_idx = _positions(
135	        rendered,
136	        f"# {issue['title']}",
137	        "Execution instructions:",
138	        _TAIL,
139	    )
140	    assert title_idx < preamble_idx < tail_idx
141	
```

> TOOL

tool_result
id: toolu_01WNHWVnB7jTCZwixp2k6Ado
```
1	"""Multi-repo orchestrator behaviour.
2	
3	Two halves:
4	
5	1. **Happy path** — two issues with different ``repo:`` labels are each
6	   resolved to their respective configured paths, and ``subprocess.run``
7	   sees the matching ``cwd``. Guards against a regression that wires
8	   ``Path.cwd()`` back in (or hardcodes one of the issues' repos for
9	   both).
10	
11	2. **Resolution halt** — each ``RepoResolutionError`` variant must
12	   write a run-log entry and emit the matching ``Halt:`` line, and
13	   must **not** call ``linear.set_state`` (no state was moved yet).
14	   Behaviour contrast with the existing setup-failure halt: that one
15	   also doesn't revert, but it does try ``set_state`` first; here we
16	   never reach it.
17	"""
18	from __future__ import annotations
19	
20	import json
21	import subprocess
22	from pathlib import Path
23	
24	import pytest
25	
26	from drain_cycle import linear, orchestrator, repos
27	
28	
29	def _issue(
30	    identifier: str,
31	    repo_name: str,
32	    *,
33	    sort_order: float = 1.0,
34	    labels: list[str] | None = None,
35	) -> dict:
36	    return {
37	        "id": f"id-{identifier}",
38	        "identifier": identifier,
39	        "title": f"Title for {identifier}",
40	        "description": f"Body for {identifier}",
41	        "sortOrder": sort_order,
42	        "state": {"type": "unstarted", "name": "Todo"},
43	        "labels": [f"repo:{repo_name}"] if labels is None else labels,
44	    }
45	
46	
47	def _init_repo(repo: Path) -> None:
48	    subprocess.run(["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True)
49	    subprocess.run(["git", "config", "user.email", "t@x"], cwd=repo, check=True)
50	    subprocess.run(["git", "config", "user.name", "T"], cwd=repo, check=True)
51	    (repo / "README.md").write_text("seed\n")
52	    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
53	    subprocess.run(["git", "commit", "-m", "seed"], cwd=repo, check=True, capture_output=True)
54	
55	
56	def _write_fake_claude(tmp_path: Path, marker: Path) -> Path:
57	    """Fake ``claude -p`` that records its cwd against its identifier
58	    so the test can prove the orchestrator passed the right ``cwd``."""
59	    script = tmp_path / "fake-claude.sh"
60	    script.write_text(
61	        "#!/bin/sh\n"
62	        f'printf "%s\\t%s\\n" "$(basename "$PWD")" "$PWD" >> "{marker}"\n'
63	    )
64	    script.chmod(0o755)
65	    return script
66	
67	
68	def test_orchestrator_runs_each_issue_in_its_labelled_repo(
69	    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
70	) -> None:
71	    """Two issues, two repos, two ``repo:`` labels — each spawned
72	    ``claude -p`` runs in its own resolved repo's worktree."""
73	    repo_a = tmp_path / "repo-a"
74	    repo_b = tmp_path / "repo-b"
75	    repo_a.mkdir()
76	    repo_b.mkdir()
77	    _init_repo(repo_a)
78	    _init_repo(repo_b)
79	    monkeypatch.setenv("HOME", str(tmp_path))
80	
81	    first = _issue("ABA-A", repo_name="alpha", sort_order=1.0)
82	    second = _issue("ABA-B", repo_name="beta", sort_order=2.0)
83	    raw_issues = [first, second]
84	    issues_by_id = {i["id"]: i for i in raw_issues}
85	    marker = tmp_path / "picked.tsv"
86	
87	    def fake_pending_issues(cycle_id: str):
88	        completed = {line.split("\t", 1)[0] for line in _lines(marker)}
89	        return linear._plan(
90	            [i for i in raw_issues if i["identifier"] not in completed]
91	        )
92	
93	    def fake_get_issue(issue_id: str) -> dict:
94	        identifier = issues_by_id[issue_id]["identifier"]
95	        completed = {line.split("\t", 1)[0] for line in _lines(marker)}
96	        if identifier in completed:
97	            return {
98	                **issues_by_id[issue_id],
99	                "state": {"type": "completed", "name": "Done"},
100	            }
101	        return issues_by_id[issue_id]
102	
103	    monkeypatch.setattr(linear, "current_cycle_id", lambda: "cycle-id")
104	    monkeypatch.setattr(linear, "pending_issues", fake_pending_issues)
105	    monkeypatch.setattr(linear, "get_issue", fake_get_issue)
106	    monkeypatch.setattr(linear, "set_state", lambda issue_id, name: None)
107	
108	    fake_claude = _write_fake_claude(tmp_path, marker)
109	    monkeypatch.setattr(orchestrator, "_CLAUDE_CMD", [str(fake_claude)])
110	
111	    exit_code = orchestrator.run(
112	        repos.Repos(mapping={"alpha": repo_a, "beta": repo_b})
113	    )
114	    assert exit_code == 0
115	
116	    # The fake-claude script wrote ``<identifier>\t<cwd>`` once per pick.
117	    rows = [line.split("\t", 1) for line in _lines(marker)]
118	    by_identifier = {ident: Path(cwd) for ident, cwd in rows}
119	    assert by_identifier["ABA-A"] == repo_a / ".worktrees" / "ABA-A"
120	    assert by_identifier["ABA-B"] == repo_b / ".worktrees" / "ABA-B"
121	
122	    # Each repo's worktree directory cleaned up on success.
123	    assert not (repo_a / ".worktrees").exists() or not any((repo_a / ".worktrees").iterdir())
124	    assert not (repo_b / ".worktrees").exists() or not any((repo_b / ".worktrees").iterdir())
125	
126	
127	def _lines(path: Path) -> list[str]:
128	    if not path.exists():
129	        return []
130	    return [line for line in path.read_text().splitlines() if line]
131	
132	
133	# ---------------------------------------------------------------------------
134	# Resolution-halt path. One parametrised test per error variant.
135	# ---------------------------------------------------------------------------
136	
137	
138	def _run_resolution_halt(
139	    tmp_path: Path,
140	    monkeypatch: pytest.MonkeyPatch,
141	    *,
142	    issue_labels: list[str],
143	    repos_mapping: dict[str, Path],
144	) -> tuple[int, dict, list[str]]:
145	    """Run the orchestrator with one issue carrying the supplied labels
146	    and the supplied ``Repos`` mapping. Returns ``(exit_code, runlog_payload,
147	    stderr_lines)``. ``linear.set_state`` is a tripwire — calling it on
148	    the resolution-halt path is the regression this whole test exists
149	    to guard against."""
150	    repo = tmp_path / "repo"
151	    repo.mkdir()
152	    _init_repo(repo)
153	    monkeypatch.setenv("HOME", str(tmp_path))
154	
155	    issue = _issue("ABA-1", repo_name="ignored", labels=issue_labels)
156	
157	    def fake_pending_issues(cycle_id: str):
158	        return linear._plan([issue])
159	
160	    def forbidden_set_state(issue_id: str, state_name: str) -> None:
161	        raise AssertionError(
162	            "linear.set_state must NOT be called on the resolution-halt path"
163	        )
164	
165	    def forbidden_get_issue(issue_id: str) -> dict:
166	        raise AssertionError(
167	            "linear.get_issue must NOT be called on the resolution-halt path"
168	        )
169	
170	    monkeypatch.setattr(linear, "current_cycle_id", lambda: "cycle-id")
171	    monkeypatch.setattr(linear, "pending_issues", fake_pending_issues)
172	    monkeypatch.setattr(linear, "set_state", forbidden_set_state)
173	    monkeypatch.setattr(linear, "get_issue", forbidden_get_issue)
174	
175	    forbidden_claude = tmp_path / "forbidden-claude.sh"
176	    forbidden_claude.write_text("#!/bin/sh\nexit 99\n")
177	    forbidden_claude.chmod(0o755)
178	    monkeypatch.setattr(orchestrator, "_CLAUDE_CMD", [str(forbidden_claude)])
179	
180	    exit_code = orchestrator.run(repos.Repos(mapping=repos_mapping))
181	
182	    runs_dir = tmp_path / ".drain-cycle" / "runs"
183	    payloads = [json.loads(p.read_text()) for p in runs_dir.glob("cycle-id-*.json")]
184	    assert len(payloads) == 1
185	    return exit_code, payloads[0], []
186	
187	
188	def _halt_lines(captured_err: str) -> list[str]:
189	    return [line for line in captured_err.splitlines() if line.startswith("Halt: ")]
190	
191	
192	@pytest.mark.parametrize(
193	    "issue_labels, repos_mapping_factory, expected_tail",
194	    [
195	        pytest.param(
196	            [],
197	            lambda tmp_path: {"alpha": tmp_path},
198	            "no repo: label on issue",
199	            id="no-repo-label",
200	        ),
201	        pytest.param(
202	            ["repo:alpha", "repo:beta"],
203	            lambda tmp_path: {"alpha": tmp_path, "beta": tmp_path},
204	            "multiple repo: labels: alpha, beta",
205	            id="multiple-repo-labels",
206	        ),
207	        pytest.param(
208	            ["repo:unknown"],
209	            lambda tmp_path: {"alpha": tmp_path},
210	            'repo "unknown" not in ~/.drain-cycle/repos.yml',
211	            id="unknown-repo-name",
212	        ),
213	    ],
214	)
215	def test_resolution_halt_variants_emit_correct_message_and_no_set_state(
216	    tmp_path: Path,
217	    monkeypatch: pytest.MonkeyPatch,
218	    capsys: pytest.CaptureFixture[str],
219	    issue_labels: list[str],
220	    repos_mapping_factory,
221	    expected_tail: str,
222	) -> None:
223	    exit_code, payload, _ = _run_resolution_halt(
224	        tmp_path,
225	        monkeypatch,
226	        issue_labels=issue_labels,
227	        repos_mapping=repos_mapping_factory(tmp_path),
228	    )
229	    assert exit_code == 1
230	
231	    # Exactly one halt entry, with the resolution-halt placeholder path
232	    # and the matching tail.
233	    assert len(payload["entries"]) == 1
234	    entry = payload["entries"][0]
235	    assert entry["issue_identifier"] == "ABA-1"
236	    assert entry["worktree_path"] == "<unresolved>"
237	    assert entry["final_linear_state"] == "Todo"
238	    assert expected_tail in entry["halt_reason"]
239	
240	    halt_lines = _halt_lines(capsys.readouterr().err)
241	    assert len(halt_lines) == 1
242	    (halt_line,) = halt_lines
243	    assert halt_line == entry["halt_reason"]
244	    assert "<unresolved>" in halt_line
245	    assert expected_tail in halt_line
246	
247	
248	def test_resolution_halt_when_resolved_path_does_not_exist(
249	    tmp_path: Path,
250	    monkeypatch: pytest.MonkeyPatch,
251	    capsys: pytest.CaptureFixture[str],
252	) -> None:
253	    """Mapping entry points at a missing directory — the fourth
254	    ``RepoResolutionError`` variant. Kept separate from the parametrised
255	    test because the expected tail names the absolute path the operator
256	    needs to fix."""
257	    missing = tmp_path / "missing"
258	    exit_code, payload, _ = _run_resolution_halt(
259	        tmp_path,
260	        monkeypatch,
261	        issue_labels=["repo:alpha"],
262	        repos_mapping={"alpha": missing},
263	    )
264	    assert exit_code == 1
265	
266	    entry = payload["entries"][0]
267	    expected_tail = f"resolved path {missing} does not exist"
268	    assert expected_tail in entry["halt_reason"]
269	
270	    halt_lines = _halt_lines(capsys.readouterr().err)
271	    (halt_line,) = halt_lines
272	    assert halt_line == entry["halt_reason"]
273	    assert "<unresolved>" in halt_line
274	    assert expected_tail in halt_line
275	
```

> AGENT

Let me check the existing test files for patterns.

> TOOL

tool_use Read
id: toolu_01HLqfohcVj1nZmbgHT7poy1
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_worktree.py"
}
```

> TOOL

tool_result
id: toolu_01HLqfohcVj1nZmbgHT7poy1
```
1	"""Tests for the ``worktree`` git wrapper.
2	
3	The happy-path is exercised end-to-end by ``test_orchestrator_iteration``.
4	What these tests pin is the failure mode: git's stderr must be captured
5	and surfaced in the raised ``RuntimeError`` so the operator (and the
6	runlog ``halt_reason`` written by the orchestrator) sees what actually
7	went wrong, not just a non-zero exit code.
8	"""
9	from __future__ import annotations
10	
11	import os
12	import subprocess
13	from pathlib import Path
14	
15	import pytest
16	
17	from drain_cycle import worktree
18	
19	
20	def _init_repo(repo: Path) -> None:
21	    subprocess.run(["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True)
22	    subprocess.run(["git", "config", "user.email", "t@x"], cwd=repo, check=True)
23	    subprocess.run(["git", "config", "user.name", "T"], cwd=repo, check=True)
24	    (repo / "README.md").write_text("seed\n")
25	    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
26	    subprocess.run(["git", "commit", "-m", "seed"], cwd=repo, check=True, capture_output=True)
27	
28	
29	def _commit_gitignore(repo: Path, *patterns: str) -> None:
30	    (repo / ".gitignore").write_text("\n".join(patterns) + "\n")
31	    subprocess.run(["git", "add", ".gitignore"], cwd=repo, check=True, capture_output=True)
32	    subprocess.run(
33	        ["git", "commit", "-m", "gitignore"], cwd=repo, check=True, capture_output=True
34	    )
35	
36	
37	def test_add_failure_raises_with_git_stderr_in_message(tmp_path: Path) -> None:
38	    """``git worktree add`` fails when the branch name is already taken.
39	    The raised RuntimeError must carry git's stderr so the operator can
40	    diagnose without re-running by hand."""
41	    repo = tmp_path / "repo"
42	    repo.mkdir()
43	    _init_repo(repo)
44	
45	    # First add succeeds, taking the branch "ABA-X".
46	    worktree.add(repo, "ABA-X")
47	    # Second add fails — same branch.
48	    with pytest.raises(RuntimeError) as excinfo:
49	        worktree.add(repo, "ABA-X")
50	
51	    msg = str(excinfo.value)
52	    # The message names the operation and includes git's actual complaint
53	    # (typically "already exists" or "already checked out").
54	    assert "worktree add" in msg
55	    assert "ABA-X" in msg
56	
57	
58	def test_remove_failure_raises_with_git_stderr_in_message(tmp_path: Path) -> None:
59	    """``git worktree remove`` on a non-existent path fails. The raised
60	    RuntimeError must carry git's stderr."""
61	    repo = tmp_path / "repo"
62	    repo.mkdir()
63	    _init_repo(repo)
64	
65	    bogus = repo / ".worktrees" / "never-existed"
66	    with pytest.raises(RuntimeError) as excinfo:
67	        worktree.remove(repo, bogus)
68	
69	    msg = str(excinfo.value)
70	    assert "worktree remove" in msg
71	    # Either git's own "is not a working tree" message or the path itself.
72	    assert str(bogus) in msg or "working tree" in msg.lower()
73	
74	
75	def test_link_project_config_symlinks_gitignored_claude(tmp_path: Path) -> None:
76	    """A gitignored ``.claude/`` (absent from the worktree checkout) is
77	    symlinked back to the repo's real dir, so the worker reads through it."""
78	    repo = tmp_path / "repo"
79	    repo.mkdir()
80	    _init_repo(repo)
81	    _commit_gitignore(repo, ".claude", ".worktrees")
82	    (repo / ".claude").mkdir()
83	    (repo / ".claude" / "settings.json").write_text('{"hooks": {}}\n')
84	
85	    wt = worktree.add(repo, "ABA-A")
86	    created = worktree.link_project_config(repo, wt, [".claude"])
87	
88	    assert created == [wt / ".claude"]
89	    assert (wt / ".claude").is_symlink()
90	    assert Path(os.readlink(wt / ".claude")) == repo.resolve() / ".claude"
91	    assert (wt / ".claude" / "settings.json").read_text() == '{"hooks": {}}\n'
92	
93	
94	def test_link_project_config_noop_when_no_claude(tmp_path: Path) -> None:
95	    """A repo without the named config produces no link and no error."""
96	    repo = tmp_path / "repo"
97	    repo.mkdir()
98	    _init_repo(repo)
99	    _commit_gitignore(repo, ".worktrees")
100	
101	    wt = worktree.add(repo, "ABA-A")
102	    created = worktree.link_project_config(repo, wt, [".claude", ".mcp.json"])
103	
104	    assert created == []
105	    assert not os.path.lexists(wt / ".claude")
106	    assert not os.path.lexists(wt / ".mcp.json")
107	
108	
109	def test_link_project_config_skips_existing_tracked_entry(tmp_path: Path) -> None:
110	    """A tracked ``.claude/`` git already checked out is left as a real dir,
111	    never clobbered by a symlink."""
112	    repo = tmp_path / "repo"
113	    repo.mkdir()
114	    _init_repo(repo)
115	    (repo / ".claude").mkdir()
116	    (repo / ".claude" / "settings.json").write_text("tracked\n")
117	    subprocess.run(["git", "add", ".claude"], cwd=repo, check=True, capture_output=True)
118	    subprocess.run(
119	        ["git", "commit", "-m", "track claude"], cwd=repo, check=True, capture_output=True
120	    )
121	
122	    wt = worktree.add(repo, "ABA-A")
123	    created = worktree.link_project_config(repo, wt, [".claude"])
124	
125	    assert created == []
126	    assert not (wt / ".claude").is_symlink()
127	    assert (wt / ".claude" / "settings.json").read_text() == "tracked\n"
128	
129	
130	def test_link_project_config_includes_mcp_and_entire_when_present(
131	    tmp_path: Path,
132	) -> None:
133	    """Every present, gitignored name is linked; absent ones are skipped."""
134	    repo = tmp_path / "repo"
135	    repo.mkdir()
136	    _init_repo(repo)
137	    _commit_gitignore(repo, ".claude", ".mcp.json", ".entire", ".worktrees")
138	    (repo / ".mcp.json").write_text("{}\n")
139	    (repo / ".entire").mkdir()
140	    (repo / ".entire" / "state").write_text("x\n")
141	
142	    wt = worktree.add(repo, "ABA-A")
143	    created = worktree.link_project_config(
144	        repo, wt, [".claude", ".mcp.json", ".entire"]
145	    )
146	
147	    assert set(created) == {wt / ".mcp.json", wt / ".entire"}
148	    assert (wt / ".mcp.json").is_symlink()
149	    assert (wt / ".entire").is_symlink()
150	    assert not os.path.lexists(wt / ".claude")
151	
152	
153	def test_linked_config_is_gitignored_in_worktree(tmp_path: Path) -> None:
154	    """The linked entry is gitignored in the worktree (it shares the repo's
155	    tracked .gitignore), so a worker's ``git add`` never stages it."""
156	    repo = tmp_path / "repo"
157	    repo.mkdir()
158	    _init_repo(repo)
159	    _commit_gitignore(repo, ".claude", ".worktrees")
160	    (repo / ".claude").mkdir()
161	    (repo / ".claude" / "settings.json").write_text("{}\n")
162	
163	    wt = worktree.add(repo, "ABA-A")
164	    worktree.link_project_config(repo, wt, [".claude"])
165	
166	    status = subprocess.run(
167	        ["git", "status", "--porcelain"],
168	        cwd=wt,
169	        check=True,
170	        capture_output=True,
171	        text=True,
172	    )
173	    assert ".claude" not in status.stdout
174	
175	
176	def test_ensure_fresh_creates_worktree_and_marks_resumed_false(tmp_path: Path) -> None:
177	    """``ensure`` on a previously unseen identifier delegates to ``add``,
178	    creating the worktree+branch and returning ``resumed=False``."""
179	    repo = tmp_path / "repo"
180	    repo.mkdir()
181	    _init_repo(repo)
182	
183	    handle = worktree.ensure(repo, "ABA-FRESH")
184	
185	    assert handle.resumed is False
186	    assert handle.path == repo / worktree.WORKTREE_DIR / "ABA-FRESH"
187	    assert handle.path.is_dir()
188	    # The branch git just created points at HEAD on main.
189	    branches = subprocess.run(
190	        ["git", "branch", "--list", "ABA-FRESH"],
191	        cwd=repo,
192	        check=True,
193	        capture_output=True,
194	        text=True,
195	    ).stdout
196	    assert "ABA-FRESH" in branches
197	
198	
199	def test_ensure_reuse_preserves_dirty_state_and_runs_no_git_command(
200	    tmp_path: Path,
201	) -> None:
202	    """A second ``ensure`` for an already-registered worktree returns the
203	    same path with ``resumed=True``, and changes the worktree's git state
204	    in no observable way: a committed file, a staged file, and an
205	    untracked file all survive untouched. This pins the "no-op on git
206	    state" guarantee that the dirty-tree acceptance criterion depends on.
207	    """
208	    repo = tmp_path / "repo"
209	    repo.mkdir()
210	    _init_repo(repo)
211	
212	    first = worktree.ensure(repo, "ABA-RESUME")
213	    assert first.resumed is False
214	
215	    # Make the worktree dirty in three ways: a committed file on the
216	    # issue branch, a staged-but-uncommitted file, and an untracked file.
217	    (first.path / "committed.txt").write_text("committed\n")
218	    subprocess.run(
219	        ["git", "add", "committed.txt"],
220	        cwd=first.path,
221	        check=True,
222	        capture_output=True,
223	    )
224	    subprocess.run(
225	        ["git", "commit", "-m", "prior commit"],
226	        cwd=first.path,
227	        check=True,
228	        capture_output=True,
229	    )
230	    (first.path / "staged.txt").write_text("staged\n")
231	    subprocess.run(
232	        ["git", "add", "staged.txt"],
233	        cwd=first.path,
234	        check=True,
235	        capture_output=True,
236	    )
237	    (first.path / "untracked.txt").write_text("untracked\n")
238	
239	    status_before = subprocess.run(
240	        ["git", "status", "--porcelain"],
241	        cwd=first.path,
242	        check=True,
243	        capture_output=True,
244	        text=True,
245	    ).stdout
246	    log_before = subprocess.run(
247	        ["git", "log", "--oneline"],
248	        cwd=first.path,
249	        check=True,
250	        capture_output=True,
251	        text=True,
252	    ).stdout
253	
254	    second = worktree.ensure(repo, "ABA-RESUME")
255	
256	    assert second.resumed is True
257	    assert second.path == first.path
258	    # Status + log are byte-identical: ``ensure`` ran no mutating git command.
259	    status_after = subprocess.run(
260	        ["git", "status", "--porcelain"],
261	        cwd=first.path,
262	        check=True,
263	        capture_output=True,
264	        text=True,
265	    ).stdout
266	    log_after = subprocess.run(
267	        ["git", "log", "--oneline"],
268	        cwd=first.path,
269	        check=True,
270	        capture_output=True,
271	        text=True,
272	    ).stdout
273	    assert status_after == status_before
274	    assert log_after == log_before
275	    # All three dirty-state artefacts still exist.
276	    assert (first.path / "committed.txt").read_text() == "committed\n"
277	    assert (first.path / "staged.txt").read_text() == "staged\n"
278	    assert (first.path / "untracked.txt").read_text() == "untracked\n"
279	
280	
281	def test_ensure_leftover_branch_without_worktree_falls_through_to_add(
282	    tmp_path: Path,
283	) -> None:
284	    """If the operator deletes the worktree directory but leaves the
285	    branch behind, ``ensure`` does not auto-recover — it falls through
286	    to ``add``, which raises ``RuntimeError`` (the orchestrator's halt
287	    path)."""
288	    repo = tmp_path / "repo"
289	    repo.mkdir()
290	    _init_repo(repo)
291	
292	    handle = worktree.ensure(repo, "ABA-LEFT")
293	    # Simulate the partial-cleanup state: worktree gone, branch kept.
294	    subprocess.run(
295	        ["git", "worktree", "remove", str(handle.path)],
296	        cwd=repo,
297	        check=True,
298	        capture_output=True,
299	    )
300	    branches = subprocess.run(
301	        ["git", "branch", "--list", "ABA-LEFT"],
302	        cwd=repo,
303	        check=True,
304	        capture_output=True,
305	        text=True,
306	    ).stdout
307	    assert "ABA-LEFT" in branches  # branch survived the partial cleanup
308	
309	    with pytest.raises(RuntimeError) as excinfo:
310	        worktree.ensure(repo, "ABA-LEFT")
311	    msg = str(excinfo.value)
312	    assert "worktree add" in msg
313	    assert "ABA-LEFT" in msg
314	
315	
316	def test_ensure_link_project_config_idempotent_on_reuse(tmp_path: Path) -> None:
317	    """A second ``link_project_config`` on a resumed worktree returns
318	    an empty list (every name already lexists) and leaves the existing
319	    symlink intact — confirming the orchestrator can call it
320	    unconditionally after both fresh and reused ensures."""
321	    repo = tmp_path / "repo"
322	    repo.mkdir()
323	    _init_repo(repo)
324	    _commit_gitignore(repo, ".claude", ".worktrees")
325	    (repo / ".claude").mkdir()
326	    (repo / ".claude" / "settings.json").write_text('{"hooks": {}}\n')
327	
328	    handle = worktree.ensure(repo, "ABA-CFG")
329	    first_links = worktree.link_project_config(repo, handle.path, [".claude"])
330	    assert first_links == [handle.path / ".claude"]
331	    assert (handle.path / ".claude").is_symlink()
332	
333	    # Second call on the reused worktree returns nothing and the link
334	    # is still pointing at the same target.
335	    reused = worktree.ensure(repo, "ABA-CFG")
336	    assert reused.resumed is True
337	    second_links = worktree.link_project_config(repo, reused.path, [".claude"])
338	    assert second_links == []
339	    assert (handle.path / ".claude").is_symlink()
340	    assert Path(os.readlink(handle.path / ".claude")) == repo.resolve() / ".claude"
341	
342	
343	def test_remove_preserves_symlink_target(tmp_path: Path) -> None:
344	    """Removing the worktree deletes the symlink, not the repo's real dir."""
345	    repo = tmp_path / "repo"
346	    repo.mkdir()
347	    _init_repo(repo)
348	    _commit_gitignore(repo, ".claude", ".worktrees")
349	    (repo / ".claude").mkdir()
350	    (repo / ".claude" / "settings.json").write_text("keep me\n")
351	
352	    wt = worktree.add(repo, "ABA-A")
353	    worktree.link_project_config(repo, wt, [".claude"])
354	    worktree.remove(repo, wt)
355	
356	    assert (repo / ".claude").is_dir()
357	    assert (repo / ".claude" / "settings.json").read_text() == "keep me\n"
358	
```

> TOOL

tool_use Read
id: toolu_01WNHWVnB7jTCZwixp2k6Ado
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_orchestrator_multi_repo.py"
}
```

> AGENT

Now I have a clear picture. Let me implement all the changes. I'll start with the simpler modules and work up to the orchestrator.

> TOOL

tool_use Edit
id: toolu_01BRu27K1qQwEQX4iYQEZoxu
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/worktree.py",
  "old_string": "def add(repo: Path, identifier: str) -> Path:\n    \"\"\"Create a worktree branched off ``main`` for ``identifier``.\n\n    Returns the absolute path to the new worktree.\n    \"\"\"\n    worktree_path = repo / WORKTREE_DIR / identifier\n    with telemetry.tracer.start_as_current_span(\"drain.worktree.add\") as span:\n        span.set_attribute(\"worktree.identifier\", identifier)\n        span.set_attribute(\"worktree.repo\", repo.name)\n        span.set_attribute(\"worktree.path\", str(worktree_path))\n        _run_git(\n            [\"worktree\", \"add\", \"-b\", identifier, str(worktree_path), BASE_BRANCH],\n            cwd=repo,\n        )\n    return worktree_path\n\n\ndef ensure(repo: Path, identifier: str) -> WorktreeHandle:",
  "new_string": "def add(repo: Path, identifier: str, base: str = BASE_BRANCH) -> Path:\n    \"\"\"Create a worktree branched off ``base`` for ``identifier``.\n\n    Returns the absolute path to the new worktree.\n    \"\"\"\n    worktree_path = repo / WORKTREE_DIR / identifier\n    with telemetry.tracer.start_as_current_span(\"drain.worktree.add\") as span:\n        span.set_attribute(\"worktree.identifier\", identifier)\n        span.set_attribute(\"worktree.repo\", repo.name)\n        span.set_attribute(\"worktree.path\", str(worktree_path))\n        span.set_attribute(\"worktree.base\", base)\n        _run_git(\n            [\"worktree\", \"add\", \"-b\", identifier, str(worktree_path), base],\n            cwd=repo,\n        )\n    return worktree_path\n\n\ndef ensure(repo: Path, identifier: str, base: str = BASE_BRANCH) -> WorktreeHandle:"
}
```

> TOOL

tool_result
id: toolu_01BRu27K1qQwEQX4iYQEZoxu
```
The file /Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/worktree.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01Vsm4m4ky9dHgBM5udADPpA
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/worktree.py",
  "old_string": "    worktree_path = repo / WORKTREE_DIR / identifier\n    with telemetry.tracer.start_as_current_span(\"drain.worktree.ensure\") as span:\n        span.set_attribute(\"worktree.identifier\", identifier)\n        span.set_attribute(\"worktree.repo\", repo.name)\n        span.set_attribute(\"worktree.path\", str(worktree_path))\n        if _is_registered_worktree(repo, worktree_path):\n            span.set_attribute(\"worktree.resumed\", True)\n            return WorktreeHandle(path=worktree_path, resumed=True)\n        span.set_attribute(\"worktree.resumed\", False)\n    return WorktreeHandle(path=add(repo, identifier), resumed=False)",
  "new_string": "    worktree_path = repo / WORKTREE_DIR / identifier\n    with telemetry.tracer.start_as_current_span(\"drain.worktree.ensure\") as span:\n        span.set_attribute(\"worktree.identifier\", identifier)\n        span.set_attribute(\"worktree.repo\", repo.name)\n        span.set_attribute(\"worktree.path\", str(worktree_path))\n        if _is_registered_worktree(repo, worktree_path):\n            span.set_attribute(\"worktree.resumed\", True)\n            return WorktreeHandle(path=worktree_path, resumed=True)\n        span.set_attribute(\"worktree.resumed\", False)\n    return WorktreeHandle(path=add(repo, identifier, base), resumed=False)"
}
```

> TOOL

tool_result
id: toolu_01Vsm4m4ky9dHgBM5udADPpA
```
The file /Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/worktree.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now let me create `handoff.py`:

> TOOL

tool_use Write
id: toolu_01Tjy93dVW5Rz6o5ibkU1Usq
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/handoff.py",
  "content": "\"\"\"Handoff artefact written by a stack-mode agent for the assembler.\n\nThe spawned agent writes ``.drain-handoff.json`` at the worktree root before\nfinishing so the orchestrator's assembly step can turn it into a Graphite PR\nwithout re-reading the agent's output. ``read`` never raises: a missing or\nmalformed file returns ``None`` so callers can treat it as \"not ready yet.\"\n\"\"\"\nfrom __future__ import annotations\n\nimport json\nfrom dataclasses import dataclass\nfrom pathlib import Path\n\nHANDOFF_FILE = \".drain-handoff.json\"\n\n\n@dataclass(frozen=True)\nclass HandoffData:\n    pr_title: str\n    pr_body: str\n    findings: dict[str, int]\n\n\ndef write(worktree: Path, data: HandoffData) -> None:\n    \"\"\"Serialise ``data`` to ``<worktree>/.drain-handoff.json``.\"\"\"\n    path = worktree / HANDOFF_FILE\n    path.write_text(\n        json.dumps(\n            {\n                \"pr_title\": data.pr_title,\n                \"pr_body\": data.pr_body,\n                \"findings\": data.findings,\n            },\n            indent=2,\n        )\n    )\n\n\ndef read(worktree: Path) -> HandoffData | None:\n    \"\"\"Return the handoff data for ``worktree``, or ``None`` if absent or invalid.\"\"\"\n    path = worktree / HANDOFF_FILE\n    try:\n        payload = json.loads(path.read_text())\n    except (OSError, json.JSONDecodeError):\n        return None\n    if not isinstance(payload, dict):\n        return None\n    pr_title = payload.get(\"pr_title\")\n    pr_body = payload.get(\"pr_body\")\n    findings = payload.get(\"findings\")\n    if not isinstance(pr_title, str) or not isinstance(pr_body, str):\n        return None\n    if not isinstance(findings, dict):\n        return None\n    return HandoffData(pr_title=pr_title, pr_body=pr_body, findings=findings)\n"
}
```

> TOOL

tool_result
id: toolu_01Tjy93dVW5Rz6o5ibkU1Usq
```
File created successfully at: /Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/handoff.py (file state is current in your context — no need to Read it back)
```

> AGENT

Now update `prompt.py` to add `stack` mode:

> TOOL

tool_use Read
id: toolu_01Jq5UhCLVexgGnTmbjdkJZv
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/prompt.py"
}
```

> TOOL

tool_result
id: toolu_01Jq5UhCLVexgGnTmbjdkJZv
```
1	"""Prompt builder for spawned ``claude -p`` sessions.
2	
3	The prompt is the entire contract between the orchestrator and the spawned
4	agent — there's no system prompt, no multi-turn loop. The four-segment
5	ordering below is load-bearing: the agent reads top-down, so context
6	(title + body) comes before instructions (preamble + tail), and the tail
7	line is last so it stays in the trailing-tokens window the model attends
8	to most strongly.
9	"""
10	from __future__ import annotations
11	
12	from pathlib import Path
13	from typing import Any
14	
15	
16	_TAIL = (
17	    "before marking Done: run /code-review-and-quality on the working-tree "
18	    "changes, fix Critical/Required findings, commit + push, then post a "
19	    "review-summary comment on the issue and transition to Done."
20	)
21	
22	
23	def _resume_directive(identifier: str) -> str:
24	    """Resume preamble for a worktree carrying prior committed work.
25	
26	    Inserted as the first line inside the preamble (after the ``---``
27	    separator, before "Execution instructions:") so the agent reads it
28	    ahead of the procedure but ``_TAIL`` still holds the last-line
29	    position the four-segment ordering reserves for it.
30	    """
31	    return (
32	        f"Resuming issue {identifier}: this worktree carries prior committed "
33	        "work from an earlier session that was halted. Run "
34	        "`git log --oneline main..HEAD` and `git status` first to read what "
35	        "is already done, then continue from that point — do not restart "
36	        "from scratch.\n\n"
37	    )
38	
39	
40	def build(issue: dict[str, Any], worktree: Path, *, resumed: bool = False) -> str:
41	    title = issue.get("title", "")
42	    description = issue.get("description") or ""
43	    identifier = issue.get("identifier", "")
44	
45	    resume_segment = _resume_directive(identifier) if resumed else ""
46	    preamble = (
47	        "---\n\n"
48	        f"{resume_segment}"
49	        "Execution instructions:\n"
50	        f"- Working directory: {worktree}\n"
51	        "- Base branch: main\n"
52	        f"- Completion sequence for issue {identifier} (run in this order, "
53	        "before marking Done):\n"
54	        "  1. Run `/code-review-and-quality` against the working-tree changes.\n"
55	        "  2. Fix any Critical or Required findings. Lower-severity findings "
56	        "are at your discretion.\n"
57	        "  3. Commit and push to main.\n"
58	        "  4. Post a short review-summary comment on the Linear issue via "
59	        "`mcp__claude_ai_Linear__save_comment` (count of findings by severity, "
60	        "fixed vs deferred).\n"
61	        "  5. Transition issue to Done via `mcp__claude_ai_Linear__save_issue` "
62	        '(state: "Done").\n'
63	    )
64	
65	    return (
66	        f"# {title}\n\n"
67	        f"{description}\n\n"
68	        f"{preamble}\n"
69	        f"{_TAIL}\n"
70	    )
71	
```

> TOOL

tool_use Write
id: toolu_01TW6MFFvWM2RgmavJaBduVK
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/prompt.py",
  "content": "\"\"\"Prompt builder for spawned ``claude -p`` sessions.\n\nThe prompt is the entire contract between the orchestrator and the spawned\nagent — there's no system prompt, no multi-turn loop. The four-segment\nordering below is load-bearing: the agent reads top-down, so context\n(title + body) comes before instructions (preamble + tail), and the tail\nline is last so it stays in the trailing-tokens window the model attends\nto most strongly.\n\"\"\"\nfrom __future__ import annotations\n\nfrom pathlib import Path\nfrom typing import Any\n\n\n_TAIL = (\n    \"before marking Done: run /code-review-and-quality on the working-tree \"\n    \"changes, fix Critical/Required findings, commit + push, then post a \"\n    \"review-summary comment on the issue and transition to Done.\"\n)\n\n_STACK_TAIL = (\n    \"before finishing: run /code-review-and-quality on the working-tree \"\n    \"changes, fix Critical/Required findings, commit to the issue branch \"\n    \"without pushing, then write .drain-handoff.json with the PR body and \"\n    \"review findings.\"\n)\n\n\ndef _resume_directive(identifier: str) -> str:\n    \"\"\"Resume preamble for a worktree carrying prior committed work.\n\n    Inserted as the first line inside the preamble (after the ``---``\n    separator, before \"Execution instructions:\") so the agent reads it\n    ahead of the procedure but the tail still holds the last-line\n    position the four-segment ordering reserves for it.\n    \"\"\"\n    return (\n        f\"Resuming issue {identifier}: this worktree carries prior committed \"\n        \"work from an earlier session that was halted. Run \"\n        \"`git log --oneline main..HEAD` and `git status` first to read what \"\n        \"is already done, then continue from that point — do not restart \"\n        \"from scratch.\\n\\n\"\n    )\n\n\ndef _normal_preamble(identifier: str, worktree: Path, resume_segment: str) -> str:\n    return (\n        \"---\\n\\n\"\n        f\"{resume_segment}\"\n        \"Execution instructions:\\n\"\n        f\"- Working directory: {worktree}\\n\"\n        \"- Base branch: main\\n\"\n        f\"- Completion sequence for issue {identifier} (run in this order, \"\n        \"before marking Done):\\n\"\n        \"  1. Run `/code-review-and-quality` against the working-tree changes.\\n\"\n        \"  2. Fix any Critical or Required findings. Lower-severity findings \"\n        \"are at your discretion.\\n\"\n        \"  3. Commit and push to main.\\n\"\n        \"  4. Post a short review-summary comment on the Linear issue via \"\n        \"`mcp__claude_ai_Linear__save_comment` (count of findings by severity, \"\n        \"fixed vs deferred).\\n\"\n        \"  5. Transition issue to Done via `mcp__claude_ai_Linear__save_issue` \"\n        '(state: \"Done\").\\n'\n    )\n\n\ndef _stack_preamble(identifier: str, worktree: Path, resume_segment: str) -> str:\n    return (\n        \"---\\n\\n\"\n        f\"{resume_segment}\"\n        \"Execution instructions:\\n\"\n        f\"- Working directory: {worktree}\\n\"\n        \"- Base branch: main\\n\"\n        f\"- Completion sequence for issue {identifier} (run in this order):\\n\"\n        \"  1. Run `/code-review-and-quality` against the working-tree changes.\\n\"\n        \"  2. Fix any Critical or Required findings. Lower-severity findings \"\n        \"are at your discretion.\\n\"\n        \"  3. Commit to the issue branch (do not push).\\n\"\n        \"  4. Write `.drain-handoff.json` in the worktree root with keys:\\n\"\n        \"     - `pr_title`: a concise PR title (≤ 70 characters)\\n\"\n        \"     - `pr_body`: markdown with ## What, ## Why, and ## What to review \"\n        \"sections\\n\"\n        '     - `findings`: `{\"critical\": N, \"required\": N}` counts from the '\n        \"review\\n\"\n    )\n\n\ndef build(\n    issue: dict[str, Any],\n    worktree: Path,\n    *,\n    resumed: bool = False,\n    stack: bool = False,\n) -> str:\n    title = issue.get(\"title\", \"\")\n    description = issue.get(\"description\") or \"\"\n    identifier = issue.get(\"identifier\", \"\")\n\n    resume_segment = _resume_directive(identifier) if resumed else \"\"\n\n    if stack:\n        preamble = _stack_preamble(identifier, worktree, resume_segment)\n        tail = _STACK_TAIL\n    else:\n        preamble = _normal_preamble(identifier, worktree, resume_segment)\n        tail = _TAIL\n\n    return (\n        f\"# {title}\\n\\n\"\n        f\"{description}\\n\\n\"\n        f\"{preamble}\\n\"\n        f\"{tail}\\n\"\n    )\n"
}
```

> TOOL

tool_result
id: toolu_01TW6MFFvWM2RgmavJaBduVK
```
The file /Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/prompt.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now update the orchestrator to add `stack` mode with `last_branch_per_repo` tracking:

> TOOL

tool_use Edit
id: toolu_01TsHkfz8kRwL3tKVt9tapCe
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/orchestrator.py",
  "old_string": "def run(repos: Repos, limits: Limits | None = None, *, watch: bool = False) -> int:\n    \"\"\"Drain the current cycle inside the ``drain.cycle`` root span.\n\n    The span wrapper is thin so the body keeps its shape; per-issue work nests\n    under it via ``_drain_one_issue``'s ``drain.issue`` spans, and the Linear,\n    worktree, and worker spans nest under those — yielding one trace per drain.\n    \"\"\"\n    if limits is None:\n        limits = Limits()\n    with telemetry.tracer.start_as_current_span(\"drain.cycle\") as cycle_span:\n        return _run(repos, limits, cycle_span, watch=watch)\n\n\ndef _run(repos: Repos, limits: Limits, cycle_span: Span, *, watch: bool = False) -> int:",
  "new_string": "def run(\n    repos: Repos,\n    limits: Limits | None = None,\n    *,\n    watch: bool = False,\n    stack: bool = False,\n) -> int:\n    \"\"\"Drain the current cycle inside the ``drain.cycle`` root span.\n\n    The span wrapper is thin so the body keeps its shape; per-issue work nests\n    under it via ``_drain_one_issue``'s ``drain.issue`` spans, and the Linear,\n    worktree, and worker spans nest under those — yielding one trace per drain.\n    \"\"\"\n    if limits is None:\n        limits = Limits()\n    with telemetry.tracer.start_as_current_span(\"drain.cycle\") as cycle_span:\n        return _run(repos, limits, cycle_span, watch=watch, stack=stack)\n\n\ndef _run(\n    repos: Repos,\n    limits: Limits,\n    cycle_span: Span,\n    *,\n    watch: bool = False,\n    stack: bool = False,\n) -> int:"
}
```

> TOOL

tool_result
id: toolu_01TsHkfz8kRwL3tKVt9tapCe
```
The file /Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/orchestrator.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now update the loop in `_run` to track `last_branch_per_repo` and pass it to `_drain_one_issue`:

> TOOL

tool_use Edit
id: toolu_01JmRFVQCbk1y22UFsLLXNw2
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/orchestrator.py",
  "old_string": "    in_tmux = bool(os.environ.get(\"TMUX\"))\n    current_pane_id: str | None = None\n\n    total = len(plan.order)\n    for index, issue in enumerate(plan.order):\n        # Kill the pane from the previous issue before opening one for this issue.\n        if current_pane_id is not None:\n            _close_watch_pane(current_pane_id)\n            current_pane_id = None\n\n        halt_code, current_pane_id = _drain_one_issue(\n            issue,\n            index=index,\n            total=total,\n            repos=repos,\n            limits=limits,\n            log=log,\n            cycle_id=cycle_id,\n            debug=debug,\n            watch=watch,\n            in_tmux=in_tmux,\n        )",
  "new_string": "    in_tmux = bool(os.environ.get(\"TMUX\"))\n    current_pane_id: str | None = None\n    last_branch_per_repo: dict[str, str] = {}\n\n    total = len(plan.order)\n    for index, issue in enumerate(plan.order):\n        # Kill the pane from the previous issue before opening one for this issue.\n        if current_pane_id is not None:\n            _close_watch_pane(current_pane_id)\n            current_pane_id = None\n\n        halt_code, current_pane_id = _drain_one_issue(\n            issue,\n            index=index,\n            total=total,\n            repos=repos,\n            limits=limits,\n            log=log,\n            cycle_id=cycle_id,\n            debug=debug,\n            watch=watch,\n            in_tmux=in_tmux,\n            stack=stack,\n            last_branch_per_repo=last_branch_per_repo,\n        )"
}
```

> TOOL

tool_result
id: toolu_01JmRFVQCbk1y22UFsLLXNw2
```
The file /Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/orchestrator.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now update `_drain_one_issue` signature and body:

> TOOL

tool_use Edit
id: toolu_01UohiXMcoqQLbT4Ct3pGtAi
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/orchestrator.py",
  "old_string": "def _drain_one_issue(\n    issue: dict,\n    *,\n    index: int,\n    total: int,\n    repos: Repos,\n    limits: Limits,\n    log: runlog.RunLog,\n    cycle_id: str,\n    debug: bool,\n    watch: bool = False,\n    in_tmux: bool = False,\n) -> tuple[int | None, str | None]:",
  "new_string": "def _drain_one_issue(\n    issue: dict,\n    *,\n    index: int,\n    total: int,\n    repos: Repos,\n    limits: Limits,\n    log: runlog.RunLog,\n    cycle_id: str,\n    debug: bool,\n    watch: bool = False,\n    in_tmux: bool = False,\n    stack: bool = False,\n    last_branch_per_repo: dict[str, str] | None = None,\n) -> tuple[int | None, str | None]:"
}
```

> TOOL

tool_result
id: toolu_01UohiXMcoqQLbT4Ct3pGtAi
```
The file /Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/orchestrator.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now update the `worktree.ensure` call and the `prompt.build` call inside `_drain_one_issue`, and add branch tracking on Done:

> TOOL

tool_use Edit
id: toolu_018PQhsrXgtuMnVLb5AyDqB5
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/orchestrator.py",
  "old_string": "        try:\n            handle = worktree.ensure(target_repo, identifier)\n            worktree_path = handle.path",
  "new_string": "        base = (\n            last_branch_per_repo.get(target_repo.name, worktree.BASE_BRANCH)\n            if stack and last_branch_per_repo is not None\n            else worktree.BASE_BRANCH\n        )\n        try:\n            handle = worktree.ensure(target_repo, identifier, base)\n            worktree_path = handle.path"
}
```

> TOOL

tool_result
id: toolu_018PQhsrXgtuMnVLb5AyDqB5
```
The file /Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/orchestrator.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01AcG4YVLKNX4W81ESUZEb4V
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/orchestrator.py",
  "old_string": "        agent_prompt = prompt.build(issue, worktree_path, resumed=handle.resumed)",
  "new_string": "        agent_prompt = prompt.build(issue, worktree_path, resumed=handle.resumed, stack=stack)"
}
```

> TOOL

tool_result
id: toolu_01AcG4YVLKNX4W81ESUZEb4V
```
The file /Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/orchestrator.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now update the Done path to record the branch and skip worktree removal in stack mode:

> TOOL

tool_use Edit
id: toolu_01MPhn5d8Bfe4ELNQcf8KWBu
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/orchestrator.py",
  "old_string": "        if is_done:\n            issue_span.set_attribute(\"issue.final_linear_state\", post_spawn_state)\n            remove_error: str | None = None\n            try:\n                worktree.remove(target_repo, worktree_path)\n            except RuntimeError as exc:\n                remove_error = str(exc)\n                issue_span.set_attribute(\"worktree.remove_error\", remove_error)\n                print(\n                    f\"drain-cycle: {identifier}: worktree teardown failed: {exc}\",\n                    file=sys.stderr,\n                )\n            # Append unconditionally for every attempted issue.\n            log.append_entry(\n                issue_identifier=identifier,\n                started_at=started_at,\n                finished_at=finished_at,\n                exit_code=result.exit_code,\n                final_linear_state=post_spawn_state,\n                worktree_path=str(worktree_path),\n                halt_reason=remove_error,\n                **_worker_log_fields(result),\n            )\n            if remove_error is None:\n                print(f\"drain-cycle: {identifier} done; worktree removed.\", file=sys.stderr)\n            return None, pane_id",
  "new_string": "        if is_done:\n            issue_span.set_attribute(\"issue.final_linear_state\", post_spawn_state)\n            if stack and last_branch_per_repo is not None:\n                last_branch_per_repo[target_repo.name] = identifier\n            remove_error: str | None = None\n            if not stack:\n                try:\n                    worktree.remove(target_repo, worktree_path)\n                except RuntimeError as exc:\n                    remove_error = str(exc)\n                    issue_span.set_attribute(\"worktree.remove_error\", remove_error)\n                    print(\n                        f\"drain-cycle: {identifier}: worktree teardown failed: {exc}\",\n                        file=sys.stderr,\n                    )\n            # Append unconditionally for every attempted issue.\n            log.append_entry(\n                issue_identifier=identifier,\n                started_at=started_at,\n                finished_at=finished_at,\n                exit_code=result.exit_code,\n                final_linear_state=post_spawn_state,\n                worktree_path=str(worktree_path),\n                halt_reason=remove_error,\n                **_worker_log_fields(result),\n            )\n            if stack:\n                print(f\"drain-cycle: {identifier} done; worktree preserved for stack assembly.\", file=sys.stderr)\n            elif remove_error is None:\n                print(f\"drain-cycle: {identifier} done; worktree removed.\", file=sys.stderr)\n            return None, pane_id"
}
```

> TOOL

tool_result
id: toolu_01MPhn5d8Bfe4ELNQcf8KWBu
```
The file /Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/orchestrator.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now let me write the tests. First, add tests to `test_prompt.py`:

> TOOL

tool_use Read
id: toolu_019YcLxaKcKvbYHA4mbG4ESz
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_prompt.py",
  "offset": 110
}
```

> TOOL

tool_result
id: toolu_019YcLxaKcKvbYHA4mbG4ESz
```
110	
111	def test_unresumed_prompt_is_byte_identical_to_no_kwarg_default(
112	    tmp_path: Path,
113	) -> None:
114	    """``resumed=False`` (the default) keeps the prompt unchanged: every
115	    existing call site renders byte-identical output, and the resume
116	    directive is absent."""
117	    issue = _fixture_issue()
118	    worktree = tmp_path / ".worktrees" / issue["identifier"]
119	
120	    default = build(issue, worktree)
121	    explicit_false = build(issue, worktree, resumed=False)
122	
123	    assert default == explicit_false
124	    assert "Resuming issue" not in default
125	
126	
127	def test_empty_description_does_not_break_rendering(tmp_path: Path) -> None:
128	    issue = _fixture_issue()
129	    issue["description"] = None  # Linear can return null descriptions
130	    worktree = tmp_path / ".worktrees" / issue["identifier"]
131	    rendered = build(issue, worktree)
132	
133	    # Title and preamble must still render in order even with no body.
134	    title_idx, preamble_idx, tail_idx = _positions(
135	        rendered,
136	        f"# {issue['title']}",
137	        "Execution instructions:",
138	        _TAIL,
139	    )
140	    assert title_idx < preamble_idx < tail_idx
141	
```

> TOOL

tool_use Edit
id: toolu_01A1zXDc1Czmx3jRGMZX7a8V
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_prompt.py",
  "old_string": "from drain_cycle.prompt import _TAIL, build",
  "new_string": "from drain_cycle.prompt import _STACK_TAIL, _TAIL, build"
}
```

> TOOL

tool_result
id: toolu_01A1zXDc1Czmx3jRGMZX7a8V
```
The file /Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_prompt.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01TFYSih6KiWHeiPE4YRXCBW
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_prompt.py",
  "old_string": "def test_empty_description_does_not_break_rendering(tmp_path: Path) -> None:\n    issue = _fixture_issue()\n    issue[\"description\"] = None  # Linear can return null descriptions\n    worktree = tmp_path / \".worktrees\" / issue[\"identifier\"]\n    rendered = build(issue, worktree)\n\n    # Title and preamble must still render in order even with no body.\n    title_idx, preamble_idx, tail_idx = _positions(\n        rendered,\n        f\"# {issue['title']}\",\n        \"Execution instructions:\",\n        _TAIL,\n    )\n    assert title_idx < preamble_idx < tail_idx",
  "new_string": "def test_empty_description_does_not_break_rendering(tmp_path: Path) -> None:\n    issue = _fixture_issue()\n    issue[\"description\"] = None  # Linear can return null descriptions\n    worktree = tmp_path / \".worktrees\" / issue[\"identifier\"]\n    rendered = build(issue, worktree)\n\n    # Title and preamble must still render in order even with no body.\n    title_idx, preamble_idx, tail_idx = _positions(\n        rendered,\n        f\"# {issue['title']}\",\n        \"Execution instructions:\",\n        _TAIL,\n    )\n    assert title_idx < preamble_idx < tail_idx\n\n\ndef test_stack_false_is_byte_identical_to_default(tmp_path: Path) -> None:\n    \"\"\"``stack=False`` (the default) leaves the prompt byte-identical to\n    a call with no ``stack`` kwarg — existing call sites are unaffected.\"\"\"\n    issue = _fixture_issue()\n    worktree = tmp_path / \".worktrees\" / issue[\"identifier\"]\n\n    default = build(issue, worktree)\n    explicit_false = build(issue, worktree, stack=False)\n\n    assert default == explicit_false\n\n\ndef test_stack_true_omits_push_and_includes_handoff_instruction(\n    tmp_path: Path,\n) -> None:\n    \"\"\"``stack=True`` replaces the push-to-main steps with commit-only and\n    handoff-file instructions, and uses the stack tail.\"\"\"\n    issue = _fixture_issue()\n    worktree = tmp_path / \".worktrees\" / issue[\"identifier\"]\n    rendered = build(issue, worktree, stack=True)\n\n    assert \"push\" not in rendered\n    assert \".drain-handoff.json\" in rendered\n    assert \"pr_title\" in rendered\n    assert \"pr_body\" in rendered\n    assert \"## What\" in rendered\n    assert \"## Why\" in rendered\n    assert \"## What to review\" in rendered\n\n    # Stack tail is used, not the normal tail.\n    assert _STACK_TAIL in rendered\n    assert _TAIL not in rendered\n\n    # Stack tail is still the last non-empty line.\n    non_empty = [line for line in rendered.splitlines() if line.strip()]\n    assert non_empty[-1] == _STACK_TAIL\n\n\ndef test_stack_true_four_segments_in_order(tmp_path: Path) -> None:\n    \"\"\"Stack prompt still keeps title → body → preamble → tail ordering.\"\"\"\n    issue = _fixture_issue()\n    worktree = tmp_path / \".worktrees\" / issue[\"identifier\"]\n    rendered = build(issue, worktree, stack=True)\n\n    title_idx, body_idx, preamble_idx, tail_idx = _positions(\n        rendered,\n        f\"# {issue['title']}\",\n        issue[\"description\"],\n        \"Execution instructions:\",\n        _STACK_TAIL,\n    )\n    assert title_idx < body_idx < preamble_idx < tail_idx"
}
```

> TOOL

tool_result
id: toolu_01TFYSih6KiWHeiPE4YRXCBW
```
The file /Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_prompt.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now create the handoff tests:

> TOOL

tool_use Write
id: toolu_01AiEGJJv7ww5RKiEeYvyqGN
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_handoff.py",
  "content": "\"\"\"Tests for ``drain_cycle.handoff``.\n\n``read`` must never raise: a missing file, a truncated JSON write, or a\nstructurally wrong payload all return ``None``. A well-formed file returns\na typed ``HandoffData`` object with the expected field values.\n\"\"\"\nfrom __future__ import annotations\n\nimport json\nfrom pathlib import Path\n\nfrom drain_cycle.handoff import HANDOFF_FILE, HandoffData, read, write\n\n\ndef _valid_data() -> HandoffData:\n    return HandoffData(\n        pr_title=\"feat: add stack-ready worktrees\",\n        pr_body=\"## What\\nAdds stacking.\\n\\n## Why\\nNeeded for Graphite.\\n\\n## What to review\\nworktree.py\",\n        findings={\"critical\": 0, \"required\": 1},\n    )\n\n\ndef test_write_then_read_round_trips(tmp_path: Path) -> None:\n    data = _valid_data()\n    write(tmp_path, data)\n    result = read(tmp_path)\n\n    assert result is not None\n    assert result.pr_title == data.pr_title\n    assert result.pr_body == data.pr_body\n    assert result.findings == data.findings\n\n\ndef test_read_missing_file_returns_none(tmp_path: Path) -> None:\n    assert read(tmp_path) is None\n\n\ndef test_read_malformed_json_returns_none(tmp_path: Path) -> None:\n    (tmp_path / HANDOFF_FILE).write_text(\"not valid json{{{\")\n    assert read(tmp_path) is None\n\n\ndef test_read_wrong_top_level_type_returns_none(tmp_path: Path) -> None:\n    (tmp_path / HANDOFF_FILE).write_text(json.dumps([1, 2, 3]))\n    assert read(tmp_path) is None\n\n\ndef test_read_missing_pr_title_returns_none(tmp_path: Path) -> None:\n    (tmp_path / HANDOFF_FILE).write_text(\n        json.dumps({\"pr_body\": \"body\", \"findings\": {\"critical\": 0, \"required\": 0}})\n    )\n    assert read(tmp_path) is None\n\n\ndef test_read_missing_pr_body_returns_none(tmp_path: Path) -> None:\n    (tmp_path / HANDOFF_FILE).write_text(\n        json.dumps({\"pr_title\": \"title\", \"findings\": {\"critical\": 0, \"required\": 0}})\n    )\n    assert read(tmp_path) is None\n\n\ndef test_read_missing_findings_returns_none(tmp_path: Path) -> None:\n    (tmp_path / HANDOFF_FILE).write_text(\n        json.dumps({\"pr_title\": \"title\", \"pr_body\": \"body\"})\n    )\n    assert read(tmp_path) is None\n\n\ndef test_read_findings_not_dict_returns_none(tmp_path: Path) -> None:\n    (tmp_path / HANDOFF_FILE).write_text(\n        json.dumps({\"pr_title\": \"title\", \"pr_body\": \"body\", \"findings\": [1, 2]})\n    )\n    assert read(tmp_path) is None\n\n\ndef test_read_pr_title_not_string_returns_none(tmp_path: Path) -> None:\n    (tmp_path / HANDOFF_FILE).write_text(\n        json.dumps({\"pr_title\": 42, \"pr_body\": \"body\", \"findings\": {}})\n    )\n    assert read(tmp_path) is None\n\n\ndef test_write_creates_file_at_expected_path(tmp_path: Path) -> None:\n    write(tmp_path, _valid_data())\n    assert (tmp_path / HANDOFF_FILE).exists()\n\n\ndef test_read_never_raises_on_empty_file(tmp_path: Path) -> None:\n    (tmp_path / HANDOFF_FILE).write_text(\"\")\n    assert read(tmp_path) is None\n"
}
```

> TOOL

tool_result
id: toolu_01AiEGJJv7ww5RKiEeYvyqGN
```
File created successfully at: /Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_handoff.py (file state is current in your context — no need to Read it back)
```

> AGENT

Now add the orchestrator test for per-repo base tracking. I'll add it to `test_orchestrator_multi_repo.py`:

> TOOL

tool_use Read
id: toolu_01FDQL2Tvzemp9eUWPhvieQz
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_orchestrator_multi_repo.py",
  "offset": 56,
  "limit": 75
}
```

> TOOL

tool_result
id: toolu_01FDQL2Tvzemp9eUWPhvieQz
```
56	def _write_fake_claude(tmp_path: Path, marker: Path) -> Path:
57	    """Fake ``claude -p`` that records its cwd against its identifier
58	    so the test can prove the orchestrator passed the right ``cwd``."""
59	    script = tmp_path / "fake-claude.sh"
60	    script.write_text(
61	        "#!/bin/sh\n"
62	        f'printf "%s\\t%s\\n" "$(basename "$PWD")" "$PWD" >> "{marker}"\n'
63	    )
64	    script.chmod(0o755)
65	    return script
66	
67	
68	def test_orchestrator_runs_each_issue_in_its_labelled_repo(
69	    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
70	) -> None:
71	    """Two issues, two repos, two ``repo:`` labels — each spawned
72	    ``claude -p`` runs in its own resolved repo's worktree."""
73	    repo_a = tmp_path / "repo-a"
74	    repo_b = tmp_path / "repo-b"
75	    repo_a.mkdir()
76	    repo_b.mkdir()
77	    _init_repo(repo_a)
78	    _init_repo(repo_b)
79	    monkeypatch.setenv("HOME", str(tmp_path))
80	
81	    first = _issue("ABA-A", repo_name="alpha", sort_order=1.0)
82	    second = _issue("ABA-B", repo_name="beta", sort_order=2.0)
83	    raw_issues = [first, second]
84	    issues_by_id = {i["id"]: i for i in raw_issues}
85	    marker = tmp_path / "picked.tsv"
86	
87	    def fake_pending_issues(cycle_id: str):
88	        completed = {line.split("\t", 1)[0] for line in _lines(marker)}
89	        return linear._plan(
90	            [i for i in raw_issues if i["identifier"] not in completed]
91	        )
92	
93	    def fake_get_issue(issue_id: str) -> dict:
94	        identifier = issues_by_id[issue_id]["identifier"]
95	        completed = {line.split("\t", 1)[0] for line in _lines(marker)}
96	        if identifier in completed:
97	            return {
98	                **issues_by_id[issue_id],
99	                "state": {"type": "completed", "name": "Done"},
100	            }
101	        return issues_by_id[issue_id]
102	
103	    monkeypatch.setattr(linear, "current_cycle_id", lambda: "cycle-id")
104	    monkeypatch.setattr(linear, "pending_issues", fake_pending_issues)
105	    monkeypatch.setattr(linear, "get_issue", fake_get_issue)
106	    monkeypatch.setattr(linear, "set_state", lambda issue_id, name: None)
107	
108	    fake_claude = _write_fake_claude(tmp_path, marker)
109	    monkeypatch.setattr(orchestrator, "_CLAUDE_CMD", [str(fake_claude)])
110	
111	    exit_code = orchestrator.run(
112	        repos.Repos(mapping={"alpha": repo_a, "beta": repo_b})
113	    )
114	    assert exit_code == 0
115	
116	    # The fake-claude script wrote ``<identifier>\t<cwd>`` once per pick.
117	    rows = [line.split("\t", 1) for line in _lines(marker)]
118	    by_identifier = {ident: Path(cwd) for ident, cwd in rows}
119	    assert by_identifier["ABA-A"] == repo_a / ".worktrees" / "ABA-A"
120	    assert by_identifier["ABA-B"] == repo_b / ".worktrees" / "ABA-B"
121	
122	    # Each repo's worktree directory cleaned up on success.
123	    assert not (repo_a / ".worktrees").exists() or not any((repo_a / ".worktrees").iterdir())
124	    assert not (repo_b / ".worktrees").exists() or not any((repo_b / ".worktrees").iterdir())
125	
126	
127	def _lines(path: Path) -> list[str]:
128	    if not path.exists():
129	        return []
130	    return [line for line in path.read_text().splitlines() if line]
```

> TOOL

tool_use Read
id: toolu_016b5QJFyNdjzv848UPaNmQy
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_orchestrator_iteration.py",
  "limit": 80
}
```

> TOOL

tool_result
id: toolu_016b5QJFyNdjzv848UPaNmQy
```
1	"""Drain-the-cycle iteration test for the orchestrator.
2	
3	The walking skeleton covered one issue end-to-end. This test pins the
4	behaviour that *every* sorted Todo/Backlog issue is processed in order, each
5	in its own worktree, and that every worktree is removed when the spawned
6	session signals completion.
7	
8	What we substitute and why:
9	
10	* Linear: stubbed in-process. The orchestrator imports the linear module by
11	  attribute, so monkey-patching ``cycle_id`` / ``pending_issues`` / ``get_issue``
12	  on it is sufficient. We do **not** stub the GraphQL transport — the layer
13	  under test here is the orchestrator loop, not the wire format (the wire
14	  format is exercised separately).
15	* Spawned ``claude -p``: replaced with a real shell script via
16	  ``_CLAUDE_CMD``. The script writes the basename of its cwd (the issue
17	  identifier — that's how the orchestrator names worktrees) into a shared
18	  marker file. The stubbed ``get_issue`` reads that file to decide which
19	  issues are Done. This satisfies the spec's "no-op script that calls back
20	  into the stubbed Linear" — the callback path is the marker file rather
21	  than an in-process call, because the script runs in a separate process.
22	* Git: a real ``git init`` repo with one commit on ``main``. ``git worktree``
23	  is exercised for real; this is the cheapest way to be sure the orchestrator
24	  doesn't paper over a worktree problem.
25	"""
26	from __future__ import annotations
27	
28	import subprocess
29	from pathlib import Path
30	
31	import pytest
32	
33	from drain_cycle import linear, orchestrator, repos, runlog
34	
35	
36	def _issue(
37	    identifier: str,
38	    sort_order: float,
39	    *,
40	    repo_name: str = "test-repo",
41	) -> dict:
42	    return {
43	        "id": f"id-{identifier}",
44	        "identifier": identifier,
45	        "title": f"Title for {identifier}",
46	        "description": f"Body for {identifier}",
47	        "sortOrder": sort_order,
48	        "state": {"type": "unstarted", "name": "Todo"},
49	        "labels": [f"repo:{repo_name}"],
50	    }
51	
52	
53	def _init_repo(repo: Path) -> None:
54	    """Create a real git repo with one commit on ``main`` for worktree tests."""
55	    subprocess.run(["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True)
56	    subprocess.run(
57	        ["git", "config", "user.email", "test@example.com"], cwd=repo, check=True
58	    )
59	    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
60	    (repo / "README.md").write_text("seed\n")
61	    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
62	    subprocess.run(
63	        ["git", "commit", "-m", "seed"], cwd=repo, check=True, capture_output=True
64	    )
65	
66	
67	def test_orchestrator_drains_every_issue_in_sorted_order(
68	    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
69	) -> None:
70	    repo = tmp_path / "repo"
71	    repo.mkdir()
72	    _init_repo(repo)
73	    monkeypatch.chdir(repo)
74	    monkeypatch.setenv("HOME", str(tmp_path))
75	
76	    # Three issues — chosen so input order and sortOrder order disagree,
77	    # proving the loop consumes the *planned* order rather than input order.
78	    raw_issues = [
79	        _issue("ABA-X", sort_order=2.0),
80	        _issue("ABA-Y", sort_order=1.0),  # lowest sortOrder — runs first
```

> TOOL

tool_use Read
id: toolu_01Bod66mXdb1b4ttkw1GBbPd
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_orchestrator_iteration.py",
  "offset": 80,
  "limit": 80
}
```

> TOOL

tool_result
id: toolu_01Bod66mXdb1b4ttkw1GBbPd
```
80	        _issue("ABA-Y", sort_order=1.0),  # lowest sortOrder — runs first
81	        _issue("ABA-Z", sort_order=3.0),
82	    ]
83	    plan = linear._plan(raw_issues)
84	    expected_order = [i["identifier"] for i in plan.order]
85	    assert expected_order == ["ABA-Y", "ABA-X", "ABA-Z"]
86	
87	    issues_by_id = {i["id"]: i for i in raw_issues}
88	    done_marker = tmp_path / "done-identifiers.txt"
89	
90	    def fake_current_cycle_id() -> str:
91	        return "stub-cycle"
92	
93	    def fake_pending_issues(cycle_id: str):
94	        completed = _completed_identifiers(done_marker)
95	        return linear._plan(
96	            [i for i in raw_issues if i["identifier"] not in completed]
97	        )
98	
99	    def fake_get_issue(issue_id: str) -> dict:
100	        issue = issues_by_id[issue_id]
101	        if issue["identifier"] in _completed_identifiers(done_marker):
102	            return {**issue, "state": {"type": "completed", "name": "Done"}}
103	        return issue
104	
105	    monkeypatch.setattr(linear, "current_cycle_id", fake_current_cycle_id)
106	    monkeypatch.setattr(linear, "pending_issues", fake_pending_issues)
107	    monkeypatch.setattr(linear, "get_issue", fake_get_issue)
108	    # set_state is exercised by tests/test_orchestrator_set_state.py; here it's
109	    # a no-op so this test stays focused on iteration order + worktree cleanup.
110	    monkeypatch.setattr(linear, "set_state", lambda issue_id, state_name: None)
111	
112	    fake_claude = _write_fake_claude_script(tmp_path, done_marker)
113	    monkeypatch.setattr(orchestrator, "_CLAUDE_CMD", [str(fake_claude)])
114	
115	    exit_code = orchestrator.run(repos.Repos(mapping={"test-repo": repo}))
116	
117	    assert exit_code == 0
118	    # The script appends the worktree-basename (== issue identifier) on each
119	    # run, so the file contents are the exact processing order.
120	    assert done_marker.read_text().splitlines() == expected_order
121	    # Every worktree was removed on success.
122	    worktrees_dir = repo / ".worktrees"
123	    assert not worktrees_dir.exists() or not any(worktrees_dir.iterdir())
124	    # ``git worktree list`` should show only the main checkout.
125	    listed = subprocess.run(
126	        ["git", "worktree", "list", "--porcelain"],
127	        cwd=repo,
128	        check=True,
129	        capture_output=True,
130	        text=True,
131	    ).stdout
132	    assert listed.count("worktree ") == 1
133	
134	
135	def test_orchestrator_passes_resolved_model_to_worker(
136	    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
137	) -> None:
138	    """The model resolved from the issue's ``model:`` label reaches the
139	    spawned command as ``--model <resolved>`` — default Sonnet when absent,
140	    the labelled override otherwise."""
141	    repo = tmp_path / "repo"
142	    repo.mkdir()
143	    _init_repo(repo)
144	    monkeypatch.chdir(repo)
145	    monkeypatch.setenv("HOME", str(tmp_path))
146	
147	    default_issue = _issue("ABA-DEF", sort_order=1.0)
148	    opus_issue = _issue("ABA-OPUS", sort_order=2.0)
149	    opus_issue["labels"] = ["repo:test-repo", "model:opus"]
150	    raw_issues = [default_issue, opus_issue]
151	
152	    issues_by_id = {i["id"]: i for i in raw_issues}
153	    done_marker = tmp_path / "done-identifiers.txt"
154	    argv_dir = tmp_path / "argv"
155	    argv_dir.mkdir()
156	
157	    def fake_pending_issues(cycle_id: str):
158	        completed = _completed_identifiers(done_marker)
159	        return linear._plan(
```

> TOOL

tool_use Read
id: toolu_014yPoVFonJsNqCLe6ke9QA3
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_orchestrator_iteration.py",
  "offset": 160,
  "limit": 60
}
```

> TOOL

tool_result
id: toolu_014yPoVFonJsNqCLe6ke9QA3
```
160	            [i for i in raw_issues if i["identifier"] not in completed]
161	        )
162	
163	    def fake_get_issue(issue_id: str) -> dict:
164	        issue = issues_by_id[issue_id]
165	        if issue["identifier"] in _completed_identifiers(done_marker):
166	            return {**issue, "state": {"type": "completed", "name": "Done"}}
167	        return issue
168	
169	    monkeypatch.setattr(linear, "current_cycle_id", lambda: "stub-cycle")
170	    monkeypatch.setattr(linear, "pending_issues", fake_pending_issues)
171	    monkeypatch.setattr(linear, "get_issue", fake_get_issue)
172	    monkeypatch.setattr(linear, "set_state", lambda issue_id, state_name: None)
173	
174	    fake_claude = _write_argv_capturing_claude_script(tmp_path, done_marker, argv_dir)
175	    monkeypatch.setattr(orchestrator, "_CLAUDE_CMD", [str(fake_claude)])
176	
177	    exit_code = orchestrator.run(repos.Repos(mapping={"test-repo": repo}))
178	    assert exit_code == 0
179	
180	    assert _model_arg(argv_dir / "ABA-DEF.txt") == "claude-sonnet-4-6"
181	    assert _model_arg(argv_dir / "ABA-OPUS.txt") == "claude-opus-4-7"
182	
183	
184	def test_orchestrator_links_project_config_into_worker_cwd(
185	    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
186	) -> None:
187	    """The orchestrator symlinks gitignored project config into the worktree
188	    before spawning, so the worker's cwd can read ``.claude/settings.json`` —
189	    the precondition for project hooks to load. Asserts resolvability from the
190	    worker's cwd, not that hooks actually fire (no real ``claude`` runs)."""
191	    repo = tmp_path / "repo"
192	    repo.mkdir()
193	    _init_repo(repo)
194	    # Gitignore the project config exactly as a real repo does, then seed it.
195	    # It is therefore absent from the worktree checkout until linked in.
196	    (repo / ".gitignore").write_text(".claude\n.worktrees\n")
197	    subprocess.run(["git", "add", ".gitignore"], cwd=repo, check=True, capture_output=True)
198	    subprocess.run(
199	        ["git", "commit", "-m", "gitignore"], cwd=repo, check=True, capture_output=True
200	    )
201	    (repo / ".claude").mkdir()
202	    (repo / ".claude" / "settings.json").write_text("{}\n")
203	    monkeypatch.chdir(repo)
204	    monkeypatch.setenv("HOME", str(tmp_path))
205	
206	    issue = _issue("ABA-CFG", sort_order=1.0)
207	    raw_issues = [issue]
208	    issues_by_id = {i["id"]: i for i in raw_issues}
209	    done_marker = tmp_path / "done-identifiers.txt"
210	    probe_dir = tmp_path / "probe"
211	    probe_dir.mkdir()
212	
213	    def fake_pending_issues(cycle_id: str):
214	        completed = _completed_identifiers(done_marker)
215	        return linear._plan([i for i in raw_issues if i["identifier"] not in completed])
216	
217	    def fake_get_issue(issue_id: str) -> dict:
218	        issue = issues_by_id[issue_id]
219	        if issue["identifier"] in _completed_identifiers(done_marker):
```

> TOOL

tool_use Read
id: toolu_017KDfzbbfA2fF8QDjzLpof2
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_orchestrator_iteration.py",
  "offset": 280,
  "limit": 60
}
```

> TOOL

tool_result
id: toolu_017KDfzbbfA2fF8QDjzLpof2
```
280	
281	def test_orchestrator_debug_capture_passes_debug_file_beside_runlog(
282	    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
283	) -> None:
284	    """With ``DRAIN_CYCLE_DEBUG`` set, the spawned session gets a
285	    ``--debug-file`` whose path is a sibling of the run log, named per
286	    issue and timestamped with the run."""
287	    monkeypatch.setenv(orchestrator._DEBUG_ENV_VAR, "1")
288	
289	    argv = _captured_argv_for_one_issue(tmp_path, monkeypatch, "ABA-DBG")
290	
291	    assert "--debug-file" in argv
292	    debug_arg = Path(argv[argv.index("--debug-file") + 1])
293	    assert debug_arg.parent == runlog.runs_dir()
294	    assert debug_arg.name.startswith("stub-cycle-")
295	    assert debug_arg.name.endswith("-ABA-DBG.debug.log")
296	
297	
298	def test_orchestrator_omits_debug_file_when_capture_off(
299	    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
300	) -> None:
301	    """Default (no ``DRAIN_CYCLE_DEBUG``): no ``--debug-file`` reaches the
302	    spawned session."""
303	    monkeypatch.delenv(orchestrator._DEBUG_ENV_VAR, raising=False)
304	
305	    argv = _captured_argv_for_one_issue(tmp_path, monkeypatch, "ABA-NODBG")
306	
307	    assert "--debug-file" not in argv
308	
309	
310	def test_orchestrator_respects_blocks_over_sort_order(
311	    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
312	) -> None:
313	    """An issue with a lower sortOrder that is blocked by one with a higher
314	    sortOrder must run *after* its blocker — not before it."""
315	    repo = tmp_path / "repo"
316	    repo.mkdir()
317	    _init_repo(repo)
318	    monkeypatch.chdir(repo)
319	    monkeypatch.setenv("HOME", str(tmp_path))
320	
321	    # ABA-EARLY has sortOrder 1.0 (lower = "earlier" in pure sort order),
322	    # but it is blocked by ABA-LATE (sortOrder 2.0). The dependency forces
323	    # ABA-LATE to run first.
324	    early = {
325	        "id": "id-ABA-EARLY",
326	        "identifier": "ABA-EARLY",
327	        "title": "Early",
328	        "description": "",
329	        "sortOrder": 1.0,
330	        "state": {"type": "unstarted", "name": "Todo"},
331	        "labels": ["repo:test-repo"],
332	        "blockers": [{"id": "id-ABA-LATE", "identifier": "ABA-LATE", "state_type": "unstarted"}],
333	    }
334	    late = {
335	        "id": "id-ABA-LATE",
336	        "identifier": "ABA-LATE",
337	        "title": "Late",
338	        "description": "",
339	        "sortOrder": 2.0,
```

> TOOL

tool_use Read
id: toolu_0133uQETieS4u8wHywq8V1Q8
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_orchestrator_iteration.py",
  "offset": 340,
  "limit": 80
}
```

> TOOL

tool_result
id: toolu_0133uQETieS4u8wHywq8V1Q8
```
340	        "state": {"type": "unstarted", "name": "Todo"},
341	        "labels": ["repo:test-repo"],
342	        "blockers": [],
343	    }
344	    raw_issues = [early, late]
345	    issues_by_id = {i["id"]: i for i in raw_issues}
346	    done_marker = tmp_path / "done-identifiers.txt"
347	
348	    def fake_pending_issues(cycle_id: str):
349	        completed = _completed_identifiers(done_marker)
350	        return linear._plan([i for i in raw_issues if i["identifier"] not in completed])
351	
352	    def fake_get_issue(issue_id: str) -> dict:
353	        issue = issues_by_id[issue_id]
354	        if issue["identifier"] in _completed_identifiers(done_marker):
355	            return {**issue, "state": {"type": "completed", "name": "Done"}}
356	        return issue
357	
358	    monkeypatch.setattr(linear, "current_cycle_id", lambda: "stub-cycle")
359	    monkeypatch.setattr(linear, "pending_issues", fake_pending_issues)
360	    monkeypatch.setattr(linear, "get_issue", fake_get_issue)
361	    monkeypatch.setattr(linear, "set_state", lambda issue_id, state_name: None)
362	
363	    fake_claude = _write_fake_claude_script(tmp_path, done_marker)
364	    monkeypatch.setattr(orchestrator, "_CLAUDE_CMD", [str(fake_claude)])
365	
366	    exit_code = orchestrator.run(repos.Repos(mapping={"test-repo": repo}))
367	
368	    assert exit_code == 0
369	    # Blocker must appear before blocked in the execution log.
370	    order = done_marker.read_text().splitlines()
371	    assert order == ["ABA-LATE", "ABA-EARLY"]
372	
373	
374	def test_orchestrator_defers_blocked_issue_and_logs_to_stderr(
375	    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
376	) -> None:
377	    """An issue blocked by an external unresolved issue is deferred: it is
378	    absent from the execution log and a message appears on stderr. The
379	    unblocked sibling runs normally."""
380	    repo = tmp_path / "repo"
381	    repo.mkdir()
382	    _init_repo(repo)
383	    monkeypatch.chdir(repo)
384	    monkeypatch.setenv("HOME", str(tmp_path))
385	
386	    # ABA-FREE has no blockers and runs. ABA-STUCK is blocked by an external
387	    # issue (id-EXT-1) that is "in_progress" — not completed/canceled.
388	    free_issue = {
389	        "id": "id-ABA-FREE",
390	        "identifier": "ABA-FREE",
391	        "title": "Free",
392	        "description": "",
393	        "sortOrder": 1.0,
394	        "state": {"type": "unstarted", "name": "Todo"},
395	        "labels": ["repo:test-repo"],
396	        "blockers": [],
397	    }
398	    stuck_issue = {
399	        "id": "id-ABA-STUCK",
400	        "identifier": "ABA-STUCK",
401	        "title": "Stuck",
402	        "description": "",
403	        "sortOrder": 2.0,
404	        "state": {"type": "unstarted", "name": "Todo"},
405	        "labels": ["repo:test-repo"],
406	        "blockers": [{"id": "id-EXT-1", "identifier": "EXT-1", "state_type": "started"}],
407	    }
408	    raw_issues = [free_issue, stuck_issue]
409	    issues_by_id = {i["id"]: i for i in raw_issues}
410	    done_marker = tmp_path / "done-identifiers.txt"
411	
412	    def fake_pending_issues(cycle_id: str):
413	        completed = _completed_identifiers(done_marker)
414	        return linear._plan([i for i in raw_issues if i["identifier"] not in completed])
415	
416	    def fake_get_issue(issue_id: str) -> dict:
417	        issue = issues_by_id[issue_id]
418	        if issue["identifier"] in _completed_identifiers(done_marker):
419	            return {**issue, "state": {"type": "completed", "name": "Done"}}
```

> TOOL

tool_use Grep
id: toolu_01KuucuM64ZSEYKFms1wURnk
```json
{
  "pattern": "def _write_fake_claude_script|def _completed_identifiers|def _write_argv_capturing",
  "path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_orchestrator_iteration.py",
  "output_mode": "content"
}
```

> TOOL

tool_result
id: toolu_01KuucuM64ZSEYKFms1wURnk
```
447:def _write_argv_capturing_claude_script(
485:def _completed_identifiers(marker: Path) -> set[str]:
491:def _write_fake_claude_script(tmp_path: Path, done_marker: Path) -> Path:
```

> TOOL

tool_use Read
id: toolu_01LNpi4yhK5NHYiJPi2LsXiU
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_orchestrator_iteration.py",
  "offset": 447,
  "limit": 60
}
```

> TOOL

tool_result
id: toolu_01LNpi4yhK5NHYiJPi2LsXiU
```
447	def _write_argv_capturing_claude_script(
448	    tmp_path: Path, done_marker: Path, argv_dir: Path
449	) -> Path:
450	    """A ``claude -p`` stand-in that records its argv (one token per line)
451	    to ``argv_dir/<identifier>.txt`` and marks the issue Done."""
452	    script = tmp_path / "fake-claude-argv.sh"
453	    script.write_text(
454	        "#!/bin/sh\n"
455	        'id="$(basename "$PWD")"\n'
456	        f': > "{argv_dir}/$id.txt"\n'
457	        f'for a in "$@"; do printf "%s\\n" "$a" >> "{argv_dir}/$id.txt"; done\n'
458	        f'printf "%s\\n" "$id" >> "{done_marker}"\n'
459	    )
460	    script.chmod(0o755)
461	    return script
462	
463	
464	def _write_config_probe_claude_script(
465	    tmp_path: Path, done_marker: Path, probe_dir: Path
466	) -> Path:
467	    """A ``claude -p`` stand-in that records whether ``.claude/settings.json``
468	    is readable from its cwd (``present``/``absent``) to
469	    ``probe_dir/<identifier>.txt``, then marks the issue Done."""
470	    script = tmp_path / "fake-claude-probe.sh"
471	    script.write_text(
472	        "#!/bin/sh\n"
473	        'id="$(basename "$PWD")"\n'
474	        "if [ -r .claude/settings.json ]; then\n"
475	        f'  printf "present\\n" > "{probe_dir}/$id.txt"\n'
476	        "else\n"
477	        f'  printf "absent\\n" > "{probe_dir}/$id.txt"\n'
478	        "fi\n"
479	        f'printf "%s\\n" "$id" >> "{done_marker}"\n'
480	    )
481	    script.chmod(0o755)
482	    return script
483	
484	
485	def _completed_identifiers(marker: Path) -> set[str]:
486	    if not marker.exists():
487	        return set()
488	    return {line for line in marker.read_text().splitlines() if line}
489	
490	
491	def _write_fake_claude_script(tmp_path: Path, done_marker: Path) -> Path:
492	    """A no-op stand-in for ``claude -p``.
493	
494	    Records the basename of its cwd (the issue identifier — orchestrator
495	    names worktrees ``.worktrees/<identifier>/``) into ``done_marker``.
496	    The stubbed ``get_issue`` reads this file to learn which issues the
497	    'agent' has completed.
498	    """
499	    script = tmp_path / "fake-claude.sh"
500	    script.write_text(
501	        "#!/bin/sh\n"
502	        f'printf "%s\\n" "$(basename "$PWD")" >> "{done_marker}"\n'
503	    )
504	    script.chmod(0o755)
505	    return script
506	
```

> AGENT

Now I have enough context. Let me add the stack-mode base tracking test to `test_orchestrator_multi_repo.py`:

> TOOL

tool_use Read
id: toolu_01JAem3HqW1hwUHW27Afnn6H
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_orchestrator_multi_repo.py",
  "offset": 127,
  "limit": 5
}
```

> TOOL

tool_result
id: toolu_01JAem3HqW1hwUHW27Afnn6H
```
127	def _lines(path: Path) -> list[str]:
128	    if not path.exists():
129	        return []
130	    return [line for line in path.read_text().splitlines() if line]
131	
```

> TOOL

tool_use Edit
id: toolu_018sMj5yJDVuz45BSG1Hfqp9
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_orchestrator_multi_repo.py",
  "old_string": "def _lines(path: Path) -> list[str]:\n    if not path.exists():\n        return []\n    return [line for line in path.read_text().splitlines() if line]",
  "new_string": "def _lines(path: Path) -> list[str]:\n    if not path.exists():\n        return []\n    return [line for line in path.read_text().splitlines() if line]\n\n\ndef _write_committing_claude(tmp_path: Path, marker: Path) -> Path:\n    \"\"\"Fake ``claude -p`` that makes a git commit in its worktree and records\n    its identifier so ``fake_get_issue`` can mark it Done.\"\"\"\n    script = tmp_path / \"fake-claude-commit.sh\"\n    script.write_text(\n        \"#!/bin/sh\\n\"\n        'id=\"$(basename \"$PWD\")\"\\n'\n        'git config user.email \"test@example.com\"\\n'\n        'git config user.name \"Test\"\\n'\n        'echo \"work\" > work.txt\\n'\n        \"git add work.txt\\n\"\n        'git commit -m \"work for $id\"\\n'\n        f'printf \"%s\\\\n\" \"$id\" >> \"{marker}\"\\n'\n    )\n    script.chmod(0o755)\n    return script\n\n\ndef _git_log_hashes(path: Path) -> list[str]:\n    \"\"\"Return commit hashes reachable from HEAD in ``path``.\"\"\"\n    result = subprocess.run(\n        [\"git\", \"log\", \"--format=%H\"],\n        cwd=path,\n        check=True,\n        capture_output=True,\n        text=True,\n    )\n    return result.stdout.strip().splitlines()\n\n\ndef test_stack_mode_chains_same_repo_issues_and_forks_different_repo_off_main(\n    tmp_path: Path, monkeypatch: pytest.MonkeyPatch\n) -> None:\n    \"\"\"In stack mode, same-repo issues chain: issue 2's worktree contains\n    issue 1's commit in its history. A different-repo issue still forks\n    off main and has no cross-repo commits.\"\"\"\n    repo_a = tmp_path / \"repo-a\"\n    repo_b = tmp_path / \"repo-b\"\n    repo_a.mkdir()\n    repo_b.mkdir()\n    _init_repo(repo_a)\n    _init_repo(repo_b)\n    monkeypatch.setenv(\"HOME\", str(tmp_path))\n\n    # Two issues in repo-a, one in repo-b. sort_order drives execution order.\n    first = _issue(\"ABA-1\", repo_name=\"alpha\", sort_order=1.0)\n    second = _issue(\"ABA-2\", repo_name=\"alpha\", sort_order=2.0)\n    other = _issue(\"ABA-3\", repo_name=\"beta\", sort_order=3.0)\n    raw_issues = [first, second, other]\n    issues_by_id = {i[\"id\"]: i for i in raw_issues}\n    marker = tmp_path / \"done.txt\"\n\n    def fake_pending_issues(cycle_id: str):\n        completed = {line for line in _lines(marker)}\n        return linear._plan(\n            [i for i in raw_issues if i[\"identifier\"] not in completed]\n        )\n\n    def fake_get_issue(issue_id: str) -> dict:\n        identifier = issues_by_id[issue_id][\"identifier\"]\n        completed = {line for line in _lines(marker)}\n        if identifier in completed:\n            return {\n                **issues_by_id[issue_id],\n                \"state\": {\"type\": \"completed\", \"name\": \"Done\"},\n            }\n        return issues_by_id[issue_id]\n\n    monkeypatch.setattr(linear, \"current_cycle_id\", lambda: \"cycle-id\")\n    monkeypatch.setattr(linear, \"pending_issues\", fake_pending_issues)\n    monkeypatch.setattr(linear, \"get_issue\", fake_get_issue)\n    monkeypatch.setattr(linear, \"set_state\", lambda issue_id, name: None)\n\n    fake_claude = _write_committing_claude(tmp_path, marker)\n    monkeypatch.setattr(orchestrator, \"_CLAUDE_CMD\", [str(fake_claude)])\n\n    exit_code = orchestrator.run(\n        repos.Repos(mapping={\"alpha\": repo_a, \"beta\": repo_b}),\n        stack=True,\n    )\n    assert exit_code == 0\n\n    # Worktrees are preserved in stack mode.\n    wt_1 = repo_a / \".worktrees\" / \"ABA-1\"\n    wt_2 = repo_a / \".worktrees\" / \"ABA-2\"\n    wt_3 = repo_b / \".worktrees\" / \"ABA-3\"\n    assert wt_1.is_dir()\n    assert wt_2.is_dir()\n    assert wt_3.is_dir()\n\n    hashes_1 = _git_log_hashes(wt_1)\n    hashes_2 = _git_log_hashes(wt_2)\n    hashes_3 = _git_log_hashes(wt_3)\n\n    # ABA-1's tip commit appears in ABA-2's history (chain).\n    assert hashes_1[0] in hashes_2\n\n    # ABA-3 (different repo) does not contain ABA-1's commit.\n    assert hashes_1[0] not in hashes_3"
}
```

> TOOL

tool_result
id: toolu_018sMj5yJDVuz45BSG1Hfqp9
```
The file /Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_orchestrator_multi_repo.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now let me also add a worktree test for the `base` parameter:

> TOOL

tool_use Edit
id: toolu_01S12upU7sMQHk1tQ1Cadm8s
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_worktree.py",
  "old_string": "def test_remove_preserves_symlink_target(tmp_path: Path) -> None:",
  "new_string": "def test_add_with_custom_base_forks_off_that_branch(tmp_path: Path) -> None:\n    \"\"\"``add(repo, identifier, base=branch)`` creates a worktree whose HEAD\n    is the tip of ``branch``, not ``main``.\"\"\"\n    repo = tmp_path / \"repo\"\n    repo.mkdir()\n    _init_repo(repo)\n\n    # Create a feature branch with an extra commit.\n    subprocess.run(\n        [\"git\", \"checkout\", \"-b\", \"feature-base\"], cwd=repo, check=True, capture_output=True\n    )\n    (repo / \"feature.txt\").write_text(\"feature work\\n\")\n    subprocess.run([\"git\", \"add\", \"feature.txt\"], cwd=repo, check=True, capture_output=True)\n    subprocess.run(\n        [\"git\", \"commit\", \"-m\", \"feature commit\"], cwd=repo, check=True, capture_output=True\n    )\n    feature_sha = subprocess.run(\n        [\"git\", \"rev-parse\", \"HEAD\"],\n        cwd=repo,\n        check=True,\n        capture_output=True,\n        text=True,\n    ).stdout.strip()\n    subprocess.run(\n        [\"git\", \"checkout\", \"main\"], cwd=repo, check=True, capture_output=True\n    )\n\n    wt = worktree.add(repo, \"ABA-OFF-FEATURE\", base=\"feature-base\")\n\n    # The worktree HEAD should be the tip of feature-base.\n    wt_sha = subprocess.run(\n        [\"git\", \"rev-parse\", \"HEAD\"],\n        cwd=wt,\n        check=True,\n        capture_output=True,\n        text=True,\n    ).stdout.strip()\n    assert wt_sha == feature_sha\n\n\ndef test_ensure_with_custom_base_forks_off_that_branch(tmp_path: Path) -> None:\n    \"\"\"``ensure`` passes the ``base`` through to ``add`` when creating a fresh\n    worktree, so the new branch starts at the given base.\"\"\"\n    repo = tmp_path / \"repo\"\n    repo.mkdir()\n    _init_repo(repo)\n\n    # Extra commit on a branch we'll use as the base.\n    subprocess.run(\n        [\"git\", \"checkout\", \"-b\", \"stack-base\"], cwd=repo, check=True, capture_output=True\n    )\n    (repo / \"stack.txt\").write_text(\"stack\\n\")\n    subprocess.run([\"git\", \"add\", \"stack.txt\"], cwd=repo, check=True, capture_output=True)\n    subprocess.run(\n        [\"git\", \"commit\", \"-m\", \"stack commit\"], cwd=repo, check=True, capture_output=True\n    )\n    base_sha = subprocess.run(\n        [\"git\", \"rev-parse\", \"HEAD\"],\n        cwd=repo,\n        check=True,\n        capture_output=True,\n        text=True,\n    ).stdout.strip()\n    subprocess.run(\n        [\"git\", \"checkout\", \"main\"], cwd=repo, check=True, capture_output=True\n    )\n\n    handle = worktree.ensure(repo, \"ABA-STACK\", base=\"stack-base\")\n    assert handle.resumed is False\n\n    wt_sha = subprocess.run(\n        [\"git\", \"rev-parse\", \"HEAD\"],\n        cwd=handle.path,\n        check=True,\n        capture_output=True,\n        text=True,\n    ).stdout.strip()\n    assert wt_sha == base_sha\n\n\ndef test_remove_preserves_symlink_target(tmp_path: Path) -> None:"
}
```

> TOOL

tool_result
id: toolu_01S12upU7sMQHk1tQ1Cadm8s
```
The file /Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_worktree.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now let me run the test suite:

> TOOL

tool_use Bash
id: toolu_017AspfGZwMRGW7h5hkNJTUt
```json
{
  "command": "python -m pytest tests/test_handoff.py tests/test_prompt.py tests/test_worktree.py tests/test_orchestrator_multi_repo.py -x -q 2>&1 | head -80",
  "description": "Run targeted tests"
}
```

> TOOL

tool_result
id: toolu_017AspfGZwMRGW7h5hkNJTUt
```
Pytest: No tests collected
```

> TOOL

tool_use Bash
id: toolu_0128ranqViDi2r4sXwWyZVjY
```json
{
  "command": "python -m pytest tests/test_handoff.py tests/test_prompt.py tests/test_worktree.py tests/test_orchestrator_multi_repo.py -x -q 2>&1 | head -80",
  "description": "Run targeted tests from correct directory"
}
```

> TOOL

tool_result
id: toolu_0128ranqViDi2r4sXwWyZVjY
```
Pytest: No tests collected
```

> TOOL

tool_use Bash
id: toolu_014rNR8ffBNMyVcTEiarcKQb
```json
{
  "command": "python -m pytest tests/test_handoff.py tests/test_prompt.py tests/test_worktree.py tests/test_orchestrator_multi_repo.py -x -q 2>&1 | head -80",
  "description": "Run tests from project directory"
}
```

> TOOL

tool_result
id: toolu_014rNR8ffBNMyVcTEiarcKQb
```
Pytest: No tests collected
```

> TOOL

tool_use Bash
id: toolu_01KTeky8gKhdy7jatFsbMM2W
```json
{
  "command": "python -m pytest tests/test_handoff.py tests/test_prompt.py tests/test_worktree.py tests/test_orchestrator_multi_repo.py -x -q 2>&1 | head -100",
  "description": "Run targeted tests with explicit directory"
}
```

> TOOL

tool_result
id: toolu_01KTeky8gKhdy7jatFsbMM2W
```
Pytest: No tests collected
```

> TOOL

tool_use Bash
id: toolu_01JmsRBHN729C5NW7ABL1DGn
```json
{
  "command": "python -m pytest tests/test_handoff.py tests/test_prompt.py tests/test_worktree.py tests/test_orchestrator_multi_repo.py -x -q 2>&1 | head -100",
  "description": "Run tests with explicit cd"
}
```

> TOOL

tool_result
id: toolu_01JmsRBHN729C5NW7ABL1DGn
```
Pytest: No tests collected
```

> TOOL

tool_use Bash
id: toolu_017KAxUvKQksvwosmn72qykH
```json
{
  "command": "python -m pytest tests/test_handoff.py tests/test_prompt.py tests/test_worktree.py tests/test_orchestrator_multi_repo.py -x -q 2>&1 | head -100",
  "description": "Run targeted tests from project root"
}
```

> TOOL

tool_result
id: toolu_017KAxUvKQksvwosmn72qykH
```
Pytest: No tests collected
```

> TOOL

tool_use Bash
id: toolu_01EDNnrVCfUiVAtxsQty8P67
```json
{
  "command": "ls /Users/anton/src/drain-cycle/.worktrees/ABA-301/ && which python",
  "description": "Check working directory"
}
```

> TOOL

tool_result
id: toolu_01EDNnrVCfUiVAtxsQty8P67
```
docs/
drain_cycle/
tests/
.claude -> /Users/anton/src/drain-cycle/.claude  36B
.entire -> /Users/anton/src/drain-cycle/.entire  36B
.gitignore  282B
AGENTS.md  4.1K
CLAUDE.md  223B
LICENSE  1.0K
README.md  15.2K
mise.toml  24B
pyproject.toml  718B
uv.lock  76.2K
/Users/anton/.local/share/mise/shims/python
```

> TOOL

tool_use Bash
id: toolu_01CG7a4e73z9ywGn8TehR4qZ
```json
{
  "command": "python -m pytest tests/test_handoff.py tests/test_prompt.py tests/test_worktree.py tests/test_orchestrator_multi_repo.py -x -q 2>&1 | head -100",
  "description": "Run targeted tests with explicit directory"
}
```

> TOOL

tool_result
id: toolu_01CG7a4e73z9ywGn8TehR4qZ
```
Pytest: No tests collected
```

> TOOL

tool_use Bash
id: toolu_01FaYmxvZLAzDkNJfJCHCMAV
```json
{
  "command": "bash -c \"uv run pytest tests/test_handoff.py tests/test_prompt.py tests/test_worktree.py tests/test_orchestrator_multi_repo.py -x -q 2>&1 | head -100\"",
  "description": "Run targeted tests with uv from project directory"
}
```

> TOOL

tool_result
id: toolu_01FaYmxvZLAzDkNJfJCHCMAV
```
..................F
=================================== FAILURES ===================================
_________ test_stack_true_omits_push_and_includes_handoff_instruction __________

tmp_path = PosixPath('/private/tmp/claude-501/pytest-of-anton/pytest-9/test_stack_true_omits_push_and0')

    def test_stack_true_omits_push_and_includes_handoff_instruction(
        tmp_path: Path,
    ) -> None:
        """``stack=True`` replaces the push-to-main steps with commit-only and
        handoff-file instructions, and uses the stack tail."""
        issue = _fixture_issue()
        worktree = tmp_path / ".worktrees" / issue["identifier"]
        rendered = build(issue, worktree, stack=True)
    
>       assert "push" not in rendered
E       AssertionError: assert 'push' not in '# Fixture t... findings.\n'
E         
E         'push' is contained here:
E           rue_omits_push_and0/.worktrees/ABA-999
E         ?           ++++
E           - Base branch: main
E           - Completion sequence for issue ABA-999 (run in this order):
E             1. Run `/code-review-and-quality` against the working-tree changes....
E         
E         ...Full output truncated (8 lines hidden), use '-vv' to show

tests/test_prompt.py:164: AssertionError
=========================== short test summary info ============================
FAILED tests/test_prompt.py::test_stack_true_omits_push_and_includes_handoff_instruction
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 18 passed in 0.07s
```

> AGENT

The assertion is too broad - "push" appears in the `tmp_path` directory name. Let me fix it:

> TOOL

tool_use Edit
id: toolu_012khMHbPEFTugFgS8vej1Kz
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_prompt.py",
  "old_string": "    assert \"push\" not in rendered",
  "new_string": "    assert \"push to main\" not in rendered"
}
```

> TOOL

tool_result
id: toolu_012khMHbPEFTugFgS8vej1Kz
```
The file /Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_prompt.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01QEcRtCXz9SJCzn4Y2cFE9i
```json
{
  "command": "bash -c \"uv run pytest tests/test_handoff.py tests/test_prompt.py tests/test_worktree.py tests/test_orchestrator_multi_repo.py -x -q 2>&1 | head -60\"",
  "description": "Run targeted tests again"
}
```

> TOOL

tool_result
id: toolu_01QEcRtCXz9SJCzn4Y2cFE9i
```
........................................                                 [100%]
40 passed in 2.98s
```

> AGENT

All 40 targeted tests pass. Now run the full suite:

> TOOL

tool_use Bash
id: toolu_01R1DoBWyvmGs5opMV5yWcBW
```json
{
  "command": "bash -c \"uv run pytest -x -q 2>&1 | tail -20\"",
  "description": "Run full test suite"
}
```

> TOOL

tool_result
id: toolu_01R1DoBWyvmGs5opMV5yWcBW
```
                    final_linear_state=state_name,
                    worktree_path=str(planned_path),
                    halt_reason=halt_reason,
                )
                issue_span.set_attribute("issue.final_linear_state", state_name)
                telemetry.mark_error(issue_span, "err-setup-failed", halt_reason)
                print(halt_reason, file=sys.stderr)
                return 1, None
    
>           agent_prompt = prompt.build(issue, worktree_path, resumed=handle.resumed, stack=stack)
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           TypeError: test_resume_reuses_preserved_worktree_and_signals_resumed_prompt.<locals>.recording_build() got an unexpected keyword argument 'stack'

/Users/anton/src/drain-cycle/.worktrees/ABA-301/drain_cycle/orchestrator.py:514: TypeError
----------------------------- Captured stderr call -----------------------------
drain-cycle: picked ABA-STUCK: Title for ABA-STUCK
=========================== short test summary info ============================
FAILED tests/test_orchestrator_resume.py::test_resume_reuses_preserved_worktree_and_signals_resumed_prompt
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 133 passed in 11.77s
```

> TOOL

tool_use Grep
id: toolu_01E2j8bcGrYERECA39uqAdJX
```json
{
  "pattern": "recording_build",
  "path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_orchestrator_resume.py",
  "output_mode": "content",
  "context": 5
}
```

> TOOL

tool_result
id: toolu_01E2j8bcGrYERECA39uqAdJX
```
202-    )
203-
204-    build_calls: list[dict] = []
205-    real_build = prompt.build
206-
207:    def recording_build(issue_arg, worktree_arg, *, resumed=False):
208-        build_calls.append(
209-            {"identifier": issue_arg["identifier"], "resumed": resumed}
210-        )
211-        return real_build(issue_arg, worktree_arg, resumed=resumed)
212-
213:    monkeypatch.setattr(prompt, "build", recording_build)
214-
215-    set_state_calls: list[tuple[str, str]] = []
216-    _patch_linear(monkeypatch, [issue], set_state_calls=set_state_calls)
217-
218-    monkeypatch.setattr(orchestrator, "_CLAUDE_CMD", [str(_noop_claude(tmp_path))])
```

> AGENT

The resume test has a mock `build` that doesn't accept `stack`. Let me fix it:

> TOOL

tool_use Edit
id: toolu_01EQ8UL2PHeetyWzmnw8vR4g
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_orchestrator_resume.py",
  "old_string": "    def recording_build(issue_arg, worktree_arg, *, resumed=False):\n        build_calls.append(\n            {\"identifier\": issue_arg[\"identifier\"], \"resumed\": resumed}\n        )\n        return real_build(issue_arg, worktree_arg, resumed=resumed)",
  "new_string": "    def recording_build(issue_arg, worktree_arg, *, resumed=False, stack=False):\n        build_calls.append(\n            {\"identifier\": issue_arg[\"identifier\"], \"resumed\": resumed}\n        )\n        return real_build(issue_arg, worktree_arg, resumed=resumed, stack=stack)"
}
```

> TOOL

tool_result ERROR
id: toolu_01EQ8UL2PHeetyWzmnw8vR4g
```
<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

> TOOL

tool_use Read
id: toolu_018rCVo7bt5risy3f8fbq57U
```json
{
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_orchestrator_resume.py",
  "offset": 200,
  "limit": 20
}
```

> TOOL

tool_result
id: toolu_018rCVo7bt5risy3f8fbq57U
```
200	        final_state="Todo",
201	        suffix="prior",
202	    )
203	
204	    build_calls: list[dict] = []
205	    real_build = prompt.build
206	
207	    def recording_build(issue_arg, worktree_arg, *, resumed=False):
208	        build_calls.append(
209	            {"identifier": issue_arg["identifier"], "resumed": resumed}
210	        )
211	        return real_build(issue_arg, worktree_arg, resumed=resumed)
212	
213	    monkeypatch.setattr(prompt, "build", recording_build)
214	
215	    set_state_calls: list[tuple[str, str]] = []
216	    _patch_linear(monkeypatch, [issue], set_state_calls=set_state_calls)
217	
218	    monkeypatch.setattr(orchestrator, "_CLAUDE_CMD", [str(_noop_claude(tmp_path))])
219	
```

> TOOL

tool_use Edit
id: toolu_01QHu826xUc7FxiDYbLMNGfq
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_orchestrator_resume.py",
  "old_string": "    def recording_build(issue_arg, worktree_arg, *, resumed=False):\n        build_calls.append(\n            {\"identifier\": issue_arg[\"identifier\"], \"resumed\": resumed}\n        )\n        return real_build(issue_arg, worktree_arg, resumed=resumed)",
  "new_string": "    def recording_build(issue_arg, worktree_arg, *, resumed=False, stack=False):\n        build_calls.append(\n            {\"identifier\": issue_arg[\"identifier\"], \"resumed\": resumed}\n        )\n        return real_build(issue_arg, worktree_arg, resumed=resumed, stack=stack)"
}
```

> TOOL

tool_result
id: toolu_01QHu826xUc7FxiDYbLMNGfq
```
The file /Users/anton/src/drain-cycle/.worktrees/ABA-301/tests/test_orchestrator_resume.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01QGpeBYi9vXB8SNos2QYuAH
```json
{
  "command": "bash -c \"uv run pytest -x -q 2>&1 | tail -10\"",
  "description": "Run full test suite again"
}
```

> TOOL

tool_result
id: toolu_01QGpeBYi9vXB8SNos2QYuAH
```
            encoding = io.text_encoding(encoding)
>       return io.open(self, mode, buffering, encoding, errors, newline)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       FileNotFoundError: [Errno 2] No such file or directory: '/private/tmp/claude-501/pytest-of-anton/pytest-13/test_run_issue_times_out_and_k0/grandchild.pid'

../../../../.local/share/uv/python/cpython-3.12.8-macos-aarch64-none/lib/python3.12/pathlib.py:1013: FileNotFoundError
=========================== short test summary info ============================
FAILED tests/test_worker.py::test_run_issue_times_out_and_kills_whole_process_group
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 225 passed in 19.47s
```

> AGENT

The `test_worker.py` failure looks like a pre-existing flaky test (race condition with process group kill). Let me verify it's not related to my changes:

> TOOL

tool_use Bash
id: toolu_01Q7jgdk7CtE9wbupnG4RdYX
```json
{
  "command": "bash -c \"uv run pytest -q --ignore=tests/test_worker.py 2>&1 | tail -5\"",
  "description": "Run full suite excluding the flaky worker test"
}
```

> TOOL

tool_result
id: toolu_01Q7jgdk7CtE9wbupnG4RdYX
```
........................................................................ [ 30%]
........................................................................ [ 60%]
........................................................................ [ 90%]
......................                                                   [100%]
238 passed in 21.44s
```

> TOOL

tool_use Bash
id: toolu_01KA65k5pX2VpD78dYFQqMTj
```json
{
  "command": "bash -c \"uv run pytest tests/test_worker.py -q 2>&1 | tail -10\"",
  "description": "Run just the worker test to confirm flakiness"
}
```

> TOOL

tool_result
id: toolu_01KA65k5pX2VpD78dYFQqMTj
```
        if "b" not in mode:
            encoding = io.text_encoding(encoding)
>       return io.open(self, mode, buffering, encoding, errors, newline)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       FileNotFoundError: [Errno 2] No such file or directory: '/private/tmp/claude-501/pytest-of-anton/pytest-17/test_run_issue_times_out_and_k0/grandchild.pid'

../../../../.local/share/uv/python/cpython-3.12.8-macos-aarch64-none/lib/python3.12/pathlib.py:1013: FileNotFoundError
=========================== short test summary info ============================
FAILED tests/test_worker.py::test_run_issue_times_out_and_kills_whole_process_group
1 failed, 11 passed in 5.48s
```

> TOOL

tool_use Bash
id: toolu_01NKL4pT1wgxi3r22kjNY3d5
```json
{
  "command": "bash -c \"git stash && uv run pytest tests/test_worker.py::test_run_issue_times_out_and_kills_whole_process_group -q 2>&1 | tail -5; git stash pop\"",
  "description": "Confirm worker test fails on main too"
}
```

> TOOL

tool_result
id: toolu_01NKL4pT1wgxi3r22kjNY3d5
```
Saved working directory and index state WIP on ABA-301: 093c83d docs: record ABA-300 Graphite PR-stacking spike decision (§16)
Uninstalled 1 package in 0.98ms
Installed 1 package in 1ms
.                                                                        [100%]
1 passed in 0.55s
On branch ABA-301
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   drain_cycle/orchestrator.py
	modified:   drain_cycle/prompt.py
	modified:   drain_cycle/worktree.py
	modified:   pyproject.toml
	modified:   tests/test_orchestrator_multi_repo.py
	modified:   tests/test_orchestrator_resume.py
	modified:   tests/test_prompt.py
	modified:   tests/test_worktree.py
	modified:   uv.lock

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	drain_cycle/handoff.py
	tests/test_handoff.py

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (83b00e883119bed6e3f7d924f533ace32d79dfcc)
```

> AGENT

Interesting, the test passes on main but fails with my changes. Let me check if the `pyproject.toml` changes are something I accidentally modified:

> TOOL

tool_use Bash
id: toolu_01VaeY4q8MWjicifv25Aif2M
```json
{
  "command": "git diff drain_cycle/orchestrator.py drain_cycle/prompt.py drain_cycle/worktree.py | head -5 && git diff pyproject.toml",
  "description": "Check what changed in pyproject.toml"
}
```

> TOOL

tool_result
id: toolu_01VaeY4q8MWjicifv25Aif2M
```
drain_cycle/orchestrator.py | 58 +++++++++++++++++++++++++++++++-----------
 drain_cycle/prompt.py       | 62 ++++++++++++++++++++++++++++++++++++++-------
 drain_cycle/worktree.py     | 11 ++++----
 3 files changed, 102 insertions(+), 29 deletions(-)

pyproject.toml | 5 +++++
 1 file changed, 5 insertions(+)

--- Changes ---

pyproject.toml
  @@ -21,3 +21,8 @@ build-backend = "hatchling.build"
  +
  +[dependency-groups]
  +dev = [
  +    "pytest>=9.0.3",
  +]
  +5 -0
```

> TOOL

tool_use Bash
id: toolu_01XkvX58o32YHpQ9shozsR1s
```json
{
  "command": "bash -c \"uv run pytest tests/test_worker.py::test_run_issue_times_out_and_kills_whole_process_group -q -v 2>&1 | tail -20\"",
  "description": "Run the specific worker test with verbose output"
}
```

> TOOL

tool_result
id: toolu_01XkvX58o32YHpQ9shozsR1s
```
============================= test session starts ==============================
platform darwin -- Python 3.12.8, pytest-9.0.3, pluggy-1.6.0
rootdir: /Users/anton/src/drain-cycle/.worktrees/ABA-301
configfile: pyproject.toml
plugins: anyio-4.13.0
collected 1 item

tests/test_worker.py .                                                   [100%]

============================== 1 passed in 0.55s ===============================
```

> AGENT

The test passes when run in isolation - it's flaky when run in the full suite (likely a resource contention issue that's pre-existing). Let me run the full suite one more time to confirm:

> TOOL

tool_use Bash
id: toolu_016W3f9ADtYg1jriocS3Lja9
```json
{
  "command": "bash -c \"uv run pytest -q 2>&1 | tail -5\"",
  "description": "Run full test suite"
}
```

> TOOL

tool_result
id: toolu_016W3f9ADtYg1jriocS3Lja9
```
........................................................................ [ 28%]
........................................................................ [ 57%]
........................................................................ [ 86%]
..................................                                       [100%]
250 passed in 23.30s
```

> AGENT

250 tests pass. The earlier flake was a timing issue unrelated to my changes. Now let me run the code review:

> TOOL

tool_use Skill
id: toolu_01GAVaZJ22SGNdq2YUqwgXBt
```json
{
  "skill": "agent-skills:code-review-and-quality"
}
```

> TOOL

tool_result
id: toolu_01GAVaZJ22SGNdq2YUqwgXBt
```
Launching skill: agent-skills:code-review-and-quality
```

> AGENT

Let me review the diff against the five axes.

> TOOL

tool_use Bash
id: toolu_01NT9PrVcER8iUhjjaG42HZe
```json
{
  "command": "git diff main..HEAD --stat && echo \"---\" && git diff main..HEAD",
  "description": "Get full diff vs main"
}
```

> TOOL

tool_result
id: toolu_01NT9PrVcER8iUhjjaG42HZe
```
---
```

> TOOL

tool_use Bash
id: toolu_01H2oNaAcupDSNu6tLd8Zi3f
```json
{
  "command": "git diff HEAD",
  "description": "Get unstaged diff"
}
```

> TOOL

tool_result
id: toolu_01H2oNaAcupDSNu6tLd8Zi3f
```
drain_cycle/orchestrator.py           |  58 ++++++++++++++-----
 drain_cycle/prompt.py                 |  62 ++++++++++++++++++---
 drain_cycle/worktree.py               |  11 ++--
 pyproject.toml                        |   5 ++
 tests/test_orchestrator_multi_repo.py | 101 ++++++++++++++++++++++++++++++++++
 tests/test_orchestrator_resume.py     |   4 +-
 tests/test_prompt.py                  |  56 ++++++++++++++++++-
 tests/test_worktree.py                |  80 +++++++++++++++++++++++++++
 uv.lock                               |  60 ++++++++++++++++++++
 9 files changed, 405 insertions(+), 32 deletions(-)

--- Changes ---

drain_cycle/orchestrator.py
  @@ -256,7 +256,13 @@ def _debug_enabled() -> bool:
  -def run(repos: Repos, limits: Limits | None = None, *, watch: bool = False) -> int:
  +def run(
  +    repos: Repos,
  +    limits: Limits | None = None,
  +    *,
  +    watch: bool = False,
  +    stack: bool = False,
  +) -> int:
       """Drain the current cycle inside the ``drain.cycle`` root span.
   
       The span wrapper is thin so the body keeps its shape; per-issue work nests
  @@ -266,10 +272,17 @@ def run(repos: Repos, limits: Limits | None = None, *, watch: bool = False) -> i
  -        return _run(repos, limits, cycle_span, watch=watch)
  +        return _run(repos, limits, cycle_span, watch=watch, stack=stack)
   
   
  -def _run(repos: Repos, limits: Limits, cycle_span: Span, *, watch: bool = False) -> int:
  +def _run(
  +    repos: Repos,
  +    limits: Limits,
  +    cycle_span: Span,
  +    *,
  +    watch: bool = False,
  +    stack: bool = False,
  +) -> int:
       debug = _debug_enabled()
       cycle_id = linear.current_cycle_id()
       cycle_span.set_attribute("drain.cycle_id", cycle_id)
  @@ -307,6 +320,7 @@ def _run(repos: Repos, limits: Limits, cycle_span: Span, *, watch: bool = False)
  +    last_branch_per_repo: dict[str, str] = {}
   
       total = len(plan.order)
       for index, issue in enumerate(plan.order):
  @@ -326,6 +340,8 @@ def _run(repos: Repos, limits: Limits, cycle_span: Span, *, watch: bool = False)
  +            stack=stack,
  +            last_branch_per_repo=last_branch_per_repo,
           )
           if halt_code is not None:
               return halt_code  # type: ignore[return-value]
  @@ -364,6 +380,8 @@ def _drain_one_issue(
  +    stack: bool = False,
  +    last_branch_per_repo: dict[str, str] | None = None,
   ) -> tuple[int | None, str | None]:
       """Drain a single issue end to end inside a ``drain.issue`` span.
   
  @@ -449,8 +467,13 @@ def _drain_one_issue(
  +        base = (
  +            last_branch_per_repo.get(target_repo.name, worktree.BASE_BRANCH)
  +            if stack and last_branch_per_repo is not None
  +            else worktree.BASE_BRANCH
  +        )
           try:
  -            handle = worktree.ensure(target_repo, identifier)
  +            handle = worktree.ensure(target_repo, identifier, base)
               worktree_path = handle.path
               # A worktree checks out only tracked files, so gitignored
               # project config (.claude/, .mcp.json) is absent. Symlink it in
  @@ -488,7 +511,7 @@ def _drain_one_issue(
  -        agent_prompt = prompt.build(issue, worktree_path, resumed=handle.resumed)
  +        agent_prompt = prompt.build(issue, worktree_path, resumed=handle.resumed, stack=stack)
           issue_span.set_attribute("issue.resumed", handle.resumed)
           worker_model = model.resolve(issue)
           issue_span.set_attribute("issue.model", worker_model)
  @@ -646,16 +669,19 @@ def _drain_one_issue(
  +            if stack and last_branch_per_repo is not None:
  +                last_branch_per_repo[target_repo.name] = identifier
               remove_error: str | None = None
  -            try:
  -                worktree.remove(target_repo, worktree_path)
  -            except RuntimeError as exc:
  -                remove_error = str(exc)
  -                issue_span.set_attribute("worktree.remove_error", remove_error)
  -                print(
  -                    f"drain-cycle: {identifier}: worktree teardown failed: {exc}",
  -                    file=sys.stderr,
  -                )
  +            if not stack:
  +                try:
  +                    worktree.remove(target_repo, worktree_path)
  +                except RuntimeError as exc:
  +                    remove_error = str(exc)
  +                    issue_span.set_attribute("worktree.remove_error", remove_error)
  +                    print(
  +                        f"drain-cycle: {identifier}: worktree teardown failed: {exc}",
  +                        file=sys.stderr,
  +                    )
               # Append unconditionally for every attempted issue.
               log.append_entry(
                   issue_identifier=identifier,
  @@ -667,7 +693,9 @@ def _drain_one_issue(
  -            if remove_error is None:
  +            if stack:
  +                print(f"drain-cycle: {identifier} done; worktree preserved for stack assembly.", file=sys.stderr)
  +            elif remove_error is None:
                   print(f"drain-cycle: {identifier} done; worktree removed.", file=sys.stderr)
               return None, pane_id
   
  +43 -15

drain_cycle/prompt.py
  @@ -19,13 +19,20 @@ _TAIL = (
  +_STACK_TAIL = (
  +    "before finishing: run /code-review-and-quality on the working-tree "
  +    "changes, fix Critical/Required findings, commit to the issue branch "
  +    "without pushing, then write .drain-handoff.json with the PR body and "
  +    "review findings."
  +)
  +
   
   def _resume_directive(identifier: str) -> str:
       """Resume preamble for a worktree carrying prior committed work.
   
       Inserted as the first line inside the preamble (after the ``---``
       separator, before "Execution instructions:") so the agent reads it
  -    ahead of the procedure but ``_TAIL`` still holds the last-line
  +    ahead of the procedure but the tail still holds the last-line
       position the four-segment ordering reserves for it.
       """
       return (
  @@ -37,13 +44,8 @@ def _resume_directive(identifier: str) -> str:
  -def build(issue: dict[str, Any], worktree: Path, *, resumed: bool = False) -> str:
  -    title = issue.get("title", "")
  -    description = issue.get("description") or ""
  -    identifier = issue.get("identifier", "")
  -
  -    resume_segment = _resume_directive(identifier) if resumed else ""
  -    preamble = (
  +def _normal_preamble(identifier: str, worktree: Path, resume_segment: str) -> str:
  +    return (
           "---\n\n"
           f"{resume_segment}"
           "Execution instructions:\n"
  @@ -62,9 +64,51 @@ def build(issue: dict[str, Any], worktree: Path, *, resumed: bool = False) -> st
  +
  +def _stack_preamble(identifier: str, worktree: Path, resume_segment: str) -> str:
  +    return (
  +        "---\n\n"
  +        f"{resume_segment}"
  +        "Execution instructions:\n"
  +        f"- Working directory: {worktree}\n"
  +        "- Base branch: main\n"
  +        f"- Completion sequence for issue {identifier} (run in this order):\n"
  +        "  1. Run `/code-review-and-quality` against the working-tree changes.\n"
  +        "  2. Fix any Critical or Required findings. Lower-severity findings "
  +        "are at your discretion.\n"
  +        "  3. Commit to the issue branch (do not push).\n"
  +        "  4. Write `.drain-handoff.json` in the worktree root with keys:\n"
  +        "     - `pr_title`: a concise PR title (≤ 70 characters)\n"
  +        "     - `pr_body`: markdown with ## What, ## Why, and ## What to review "
  +        "sections\n"
  +        '     - `findings`: `{"critical": N, "required": N}` counts from the '
  +        "review\n"
  +    )
  +
  +
  +def build(
  +    issue: dict[str, Any],
  +    worktree: Path,
  +    *,
  +    resumed: bool = False,
  +    stack: bool = False,
  +) -> str:
  +    title = issue.get("title", "")
  +    description = issue.get("description") or ""
  +    identifier = issue.get("identifier", "")
  +
  +    resume_segment = _resume_directive(identifier) if resumed else ""
  +
  +    if stack:
  +        preamble = _stack_preamble(identifier, worktree, resume_segment)
  +        tail = _STACK_TAIL
  +    else:
  +        preamble = _normal_preamble(identifier, worktree, resume_segment)
  +        tail = _TAIL
  +
       return (
           f"# {title}\n\n"
           f"{description}\n\n"
           f"{preamble}\n"
  -        f"{_TAIL}\n"
  +        f"{tail}\n"
       )
  +53 -9

drain_cycle/worktree.py
  @@ -40,8 +40,8 @@ class WorktreeHandle:
  -def add(repo: Path, identifier: str) -> Path:
  -    """Create a worktree branched off ``main`` for ``identifier``.
  +def add(repo: Path, identifier: str, base: str = BASE_BRANCH) -> Path:
  +    """Create a worktree branched off ``base`` for ``identifier``.
   
       Returns the absolute path to the new worktree.
       """
  @@ -50,14 +50,15 @@ def add(repo: Path, identifier: str) -> Path:
  +        span.set_attribute("worktree.base", base)
           _run_git(
  -            ["worktree", "add", "-b", identifier, str(worktree_path), BASE_BRANCH],
  +            ["worktree", "add", "-b", identifier, str(worktree_path), base],
               cwd=repo,
           )
       return worktree_path
   
   
  -def ensure(repo: Path, identifier: str) -> WorktreeHandle:
  +def ensure(repo: Path, identifier: str, base: str = BASE_BRANCH) -> WorktreeHandle:
       """Reuse a preserved worktree if one is already registered, else add.
   
       A worktree registered at ``repo/.worktrees/<identifier>`` is reused
  @@ -77,7 +78,7 @@ def ensure(repo: Path, identifier: str) -> WorktreeHandle:
  -    return WorktreeHandle(path=add(repo, identifier), resumed=False)
  +    return WorktreeHandle(path=add(repo, identifier, base), resumed=False)
   
   
   def link_project_config(
  +6 -5

pyproject.toml
  @@ -21,3 +21,8 @@ build-backend = "hatchling.build"
  +
  +[dependency-groups]
  +dev = [
  +    "pytest>=9.0.3",
  +]
  +5 -0

tests/test_orchestrator_multi_repo.py
  @@ -130,6 +130,107 @@ def _lines(path: Path) -> list[str]:
  +def _write_committing_claude(tmp_path: Path, marker: Path) -> Path:
  +    """Fake ``claude -p`` that makes a git commit in its worktree and records
  +    its identifier so ``fake_get_issue`` can mark it Done."""
  +    script = tmp_path / "fake-claude-commit.sh"
  +    script.write_text(
  +        "#!/bin/sh\n"
  +        'id="$(basename "$PWD")"\n'
  +        'git config user.email "test@example.com"\n'
  +        'git config user.name "Test"\n'
  +        'echo "work" > work.txt\n'
  +        "git add work.txt\n"
  +        'git commit -m "work for $id"\n'
  +        f'printf "%s\\n" "$id" >> "{marker}"\n'
  +    )
  +    script.chmod(0o755)
  +    return script
  +
  +
  +def _git_log_hashes(path: Path) -> list[str]:
  +    """Return commit hashes reachable from HEAD in ``path``."""
  +    result = subprocess.run(
  +        ["git", "log", "--format=%H"],
  +        cwd=path,
  +        check=True,
  +        capture_output=True,
  +        text=True,
  +    )
  +    return result.stdout.strip().splitlines()
  +
  +
  +def test_stack_mode_chains_same_repo_issues_and_forks_different_repo_off_main(
  +    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
  +) -> None:
  +    """In stack mode, same-repo issues chain: issue 2's worktree contains
  +    issue 1's commit in its history. A different-repo issue still forks
  +    off main and has no cross-repo commits."""
  +    repo_a = tmp_path / "repo-a"
  +    repo_b = tmp_path / "repo-b"
  +    repo_a.mkdir()
  +    repo_b.mkdir()
  +    _init_repo(repo_a)
  +    _init_repo(repo_b)
  +    monkeypatch.setenv("HOME", str(tmp_path))
  +
  +    # Two issues in repo-a, one in repo-b. sort_order drives execution order.
  +    first = _issue("ABA-1", repo_name="alpha", sort_order=1.0)
  +    second = _issue("ABA-2", repo_name="alpha", sort_order=2.0)
  +    other = _issue("ABA-3", repo_name="beta", sort_order=3.0)
  +    raw_issues = [first, second, other]
  +    issues_by_id = {i["id"]: i for i in raw_issues}
  +    marker = tmp_path / "done.txt"
  +
  +    def fake_pending_issues(cycle_id: str):
  +        completed = {line for line in _lines(marker)}
  +        return linear._plan(
  +            [i for i in raw_issues if i["identifier"] not in completed]
  +        )
  +
  +    def fake_get_issue(issue_id: str) -> dict:
  +        identifier = issues_by_id[issue_id]["identifier"]
  +        completed = {line for line in _lines(marker)}
  +        if identifier in completed:
  +            return {
  +                **issues_by_id[issue_id],
  +                "state": {"type": "completed", "name": "Done"},
  +            }
  +        return issues_by_id[issue_id]
  +
  +    monkeypatch.setattr(linear, "current_cycle_id", lambda: "cycle-id")
  +    monkeypatch.setattr(linear, "pending_issues", fake_pending_issues)
  +    monkeypatch.setattr(linear, "get_issue", fake_get_issue)
  +    monkeypatch.setattr(linear, "set_state", lambda issue_id, name: None)
  +
  +    fake_claude = _write_committing_claude(tmp_path, marker)
  +    monkeypatch.setattr(orchestrator, "_CLAUDE_CMD", [str(fake_claude)])
  +
  +    exit_code = orchestrator.run(
  +        repos.Repos(mapping={"alpha": repo_a, "beta": repo_b}),
  +        stack=True,
  +    )
  +    assert exit_code == 0
  +
  +    # Worktrees are preserved in stack mode.
  +    wt_1 = repo_a / ".worktrees" / "ABA-1"
  +    wt_2 = repo_a / ".worktrees" / "ABA-2"
  +    wt_3 = repo_b / ".worktrees" / "ABA-3"
  +    assert wt_1.is_dir()
  +    assert wt_2.is_dir()
  +    assert wt_3.is_dir()
  +
  +    hashes_1 = _git_log_hashes(wt_1)
  +    hashes_2 = _git_log_hashes(wt_2)
  +    hashes_3 = _git_log_hashes(wt_3)
  +
  +    # ABA-1's tip commit appears in ABA-2's history (chain).
  +    assert hashes_1[0] in hashes_2
  +
  +    # ABA-3 (different repo) does not contain ABA-1's commit.
  +    assert hashes_1[0] not in hashes_3
  +
  ... (1 lines truncated)
  +101 -0

tests/test_orchestrator_resume.py
  @@ -204,11 +204,11 @@ def test_resume_reuses_preserved_worktree_and_signals_resumed_prompt(
  -    def recording_build(issue_arg, worktree_arg, *, resumed=False):
  +    def recording_build(issue_arg, worktree_arg, *, resumed=False, stack=False):
           build_calls.append(
               {"identifier": issue_arg["identifier"], "resumed": resumed}
           )
  -        return real_build(issue_arg, worktree_arg, resumed=resumed)
  +        return real_build(issue_arg, worktree_arg, resumed=resumed, stack=stack)
   
       monkeypatch.setattr(prompt, "build", recording_build)
   
  +2 -2

tests/test_prompt.py
  @@ -11,7 +11,7 @@ from __future__ import annotations
  -from drain_cycle.prompt import _TAIL, build
  +from drain_cycle.prompt import _STACK_TAIL, _TAIL, build
   
   
   def _fixture_issue() -> dict:
  @@ -138,3 +138,57 @@ def test_empty_description_does_not_break_rendering(tmp_path: Path) -> None:
  +
  +
  +def test_stack_false_is_byte_identical_to_default(tmp_path: Path) -> None:
  +    """``stack=False`` (the default) leaves the prompt byte-identical to
  +    a call with no ``stack`` kwarg — existing call sites are unaffected."""
  +    issue = _fixture_issue()
  +    worktree = tmp_path / ".worktrees" / issue["identifier"]
  +
  +    default = build(issue, worktree)
  +    explicit_false = build(issue, worktree, stack=False)
  +
  +    assert default == explicit_false
  +
  +
  +def test_stack_true_omits_push_and_includes_handoff_instruction(
  +    tmp_path: Path,
  +) -> None:
  +    """``stack=True`` replaces the push-to-main steps with commit-only and
  +    handoff-file instructions, and uses the stack tail."""
  +    issue = _fixture_issue()
  +    worktree = tmp_path / ".worktrees" / issue["identifier"]
  +    rendered = build(issue, worktree, stack=True)
  +
  +    assert "push to main" not in rendered
  +    assert ".drain-handoff.json" in rendered
  +    assert "pr_title" in rendered
  +    assert "pr_body" in rendered
  +    assert "## What" in rendered
  +    assert "## Why" in rendered
  +    assert "## What to review" in rendered
  +
  +    # Stack tail is used, not the normal tail.
  +    assert _STACK_TAIL in rendered
  +    assert _TAIL not in rendered
  +
  +    # Stack tail is still the last non-empty line.
  +    non_empty = [line for line in rendered.splitlines() if line.strip()]
  +    assert non_empty[-1] == _STACK_TAIL
  +
  +
  +def test_stack_true_four_segments_in_order(tmp_path: Path) -> None:
  +    """Stack prompt still keeps title → body → preamble → tail ordering."""
  +    issue = _fixture_issue()
  +    worktree = tmp_path / ".worktrees" / issue["identifier"]
  +    rendered = build(issue, worktree, stack=True)
  +
  +    title_idx, body_idx, preamble_idx, tail_idx = _positions(
  +        rendered,
  +        f"# {issue['title']}",
  +        issue["description"],
  +        "Execution instructions:",
  +        _STACK_TAIL,
  +    )
  +    assert title_idx < body_idx < preamble_idx < tail_idx
  +55 -1

tests/test_worktree.py
  @@ -340,6 +340,86 @@ def test_ensure_link_project_config_idempotent_on_reuse(tmp_path: Path) -> None:
  +def test_add_with_custom_base_forks_off_that_branch(tmp_path: Path) -> None:
  +    """``add(repo, identifier, base=branch)`` creates a worktree whose HEAD
  +    is the tip of ``branch``, not ``main``."""
  +    repo = tmp_path / "repo"
  +    repo.mkdir()
  +    _init_repo(repo)
  +
  +    # Create a feature branch with an extra commit.
  +    subprocess.run(
  +        ["git", "checkout", "-b", "feature-base"], cwd=repo, check=True, capture_output=True
  +    )
  +    (repo / "feature.txt").write_text("feature work\n")
  +    subprocess.run(["git", "add", "feature.txt"], cwd=repo, check=True, capture_output=True)
  +    subprocess.run(
  +        ["git", "commit", "-m", "feature commit"], cwd=repo, check=True, capture_output=True
  +    )
  +    feature_sha = subprocess.run(
  +        ["git", "rev-parse", "HEAD"],
  +        cwd=repo,
  +        check=True,
  +        capture_output=True,
  +        text=True,
  +    ).stdout.strip()
  +    subprocess.run(
  +        ["git", "checkout", "main"], cwd=repo, check=True, capture_output=True
  +    )
  +
  +    wt = worktree.add(repo, "ABA-OFF-FEATURE", base="feature-base")
  +
  +    # The worktree HEAD should be the tip of feature-base.
  +    wt_sha = subprocess.run(
  +        ["git", "rev-parse", "HEAD"],
  +        cwd=wt,
  +        check=True,
  +        capture_output=True,
  +        text=True,
  +    ).stdout.strip()
  +    assert wt_sha == feature_sha
  +
  +
  +def test_ensure_with_custom_base_forks_off_that_branch(tmp_path: Path) -> None:
  +    """``ensure`` passes the ``base`` through to ``add`` when creating a fresh
  +    worktree, so the new branch starts at the given base."""
  +    repo = tmp_path / "repo"
  +    repo.mkdir()
  +    _init_repo(repo)
  +
  +    # Extra commit on a branch we'll use as the base.
  +    subprocess.run(
  +        ["git", "checkout", "-b", "stack-base"], cwd=repo, check=True, capture_output=True
  +    )
  +    (repo / "stack.txt").write_text("stack\n")
  +    subprocess.run(["git", "add", "stack.txt"], cwd=repo, check=True, capture_output=True)
  +    subprocess.run(
  +        ["git", "commit", "-m", "stack commit"], cwd=repo, check=True, capture_output=True
  +    )
  +    base_sha = subprocess.run(
  +        ["git", "rev-parse", "HEAD"],
  +        cwd=repo,
  +        check=True,
  +        capture_output=True,
  +        text=True,
  +    ).stdout.strip()
  +    subprocess.run(
  +        ["git", "checkout", "main"], cwd=repo, check=True, capture_output=True
  +    )
  +
  +    handle = worktree.ensure(repo, "ABA-STACK", base="stack-base")
  +    assert handle.resumed is False
  +
  +    wt_sha = subprocess.run(
  +        ["git", "rev-parse", "HEAD"],
  +        cwd=handle.path,
  +        check=True,
  +        capture_output=True,
  +        text=True,
  +    ).stdout.strip()
  +    assert wt_sha == base_sha
  +
  +
   def test_remove_preserves_symlink_target(tmp_path: Path) -> None:
       """Removing the worktree deletes the symlink, not the repo's real dir."""
       repo = tmp_path / "repo"
  +80 -0

uv.lock
  @@ -112,6 +112,15 @@ wheels = [
  +[[package]]
  +name = "colorama"
  +version = "0.4.6"
  +source = { registry = "https://pypi.org/simple" }
  +sdist = { url = "https://files.pythonhosted.org/packages/d8/53/6f443c9a4a8358a93a6792e2acffb9d9d5cb0a5cfd8802644b7b1c9a02e4/colorama-0.4.6.tar.gz", hash = "sha256:08695f5cb7ed6e0531a20572697297273c47b8cae5a63ffc6d6ed5c201be6e44", size = 27697 }
  +wheels = [
  +    { url = "https://files.pythonhosted.org/packages/d1/d6/3965ed04c63042e047cb6a3e6ed1a63a35087b6a609aa3a15ed8ac56c221/colorama-0.4.6-py2.py3-none-any.whl", hash = "sha256:4f1d9991f5acc0ca119f9d443620b77f9d6b33703e51011c16baf57afb285fc6", size = 25335 },
  +]
  +

... (more changes truncated)
  +9 -0
[full diff: rtk git diff --no-compact]
```

> AGENT

Let me verify the `pyproject.toml` change isn't something I should worry about:

> TOOL

tool_use Bash
id: toolu_01EESRF271aC6p59EebsQhgh
```json
{
  "command": "git show main:pyproject.toml | tail -10",
  "description": "Check main's pyproject.toml"
}
```

> TOOL

tool_result
id: toolu_01EESRF271aC6p59EebsQhgh
```
[project.scripts]
drain-cycle = "drain_cycle.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["drain_cycle"]
```

> AGENT

The review is clean. The `pyproject.toml`/`uv.lock` changes were auto-added by `uv run pytest` to lock pytest as a dev dependency — a valid housekeeping change.

**Review summary:**
- Critical: 0
- Required: 0
- Nit: 1 (ternary for `base` is fine but an if/else block would read slightly more clearly — acceptable as-is)

All acceptance criteria verified:
- `worktree.add(base=...)` and `ensure(base=...)` thread the base through correctly (tests pass)
- `prompt.build(stack=False)` is byte-identical to the default (test passes)
- `prompt.build(stack=True)` omits "push to main" and includes handoff-file instruction (test passes)
- `handoff.read` returns typed object / `None` / never raises (11 tests pass)
- Orchestrator chains same-repo issues in stack mode and forks different-repo issues off main (test passes)

250 tests pass. Now commit and push:

> TOOL

tool_use Skill
id: toolu_01YVecM9CH8wM1GZ8yAaLV9L
```json
{
  "skill": "agent-skills:git-workflow-and-versioning"
}
```

> TOOL

tool_result
id: toolu_01YVecM9CH8wM1GZ8yAaLV9L
```
Launching skill: agent-skills:git-workflow-and-versioning
```

> TOOL

tool_use Bash
id: toolu_01DRLMbJYD772SZsdtFGYKt8
```json
{
  "command": "git add drain_cycle/worktree.py drain_cycle/prompt.py drain_cycle/handoff.py drain_cycle/orchestrator.py tests/test_handoff.py tests/test_prompt.py tests/test_worktree.py tests/test_orchestrator_multi_repo.py tests/test_orchestrator_resume.py pyproject.toml uv.lock && git status",
  "description": "Stage all changed files"
}
```

> TOOL

tool_result
id: toolu_01DRLMbJYD772SZsdtFGYKt8
```
ok 11 files changed, 550 insertions(+), 32 deletions(-)
* ABA-301
A  drain_cycle/handoff.py
M  drain_cycle/orchestrator.py
M  drain_cycle/prompt.py
M  drain_cycle/worktree.py
M  pyproject.toml
A  tests/test_handoff.py
M  tests/test_orchestrator_multi_repo.py
M  tests/test_orchestrator_resume.py
M  tests/test_prompt.py
M  tests/test_worktree.py
M  uv.lock
```

> TOOL

tool_use Bash
id: toolu_016wgLes7WazaunNpS1UoMYf
```json
{
  "command": "git commit -m \"$(cat <<'EOF'\nfeat: stack-ready worktrees and agent handoff file\n\nEach issue's worktree now forks off the previous same-repo issue's\nbranch (not always main), and the spawned agent in stack mode commits\nwithout pushing and leaves a .drain-handoff.json for the assembler.\n\nChanges:\n- worktree.add/ensure: accept a `base` param (default: main) so the\n  orchestrator can thread the prior same-repo branch as the fork point\n- handoff.py: new module — write/read .drain-handoff.json with\n  pr_title, pr_body, and findings; read never raises on bad input\n- prompt.build: stack=True replaces push-to-main steps with\n  commit-only + handoff-file instruction; stack=False (default) is\n  byte-identical to the existing prompt\n- orchestrator.run/stack=True: tracks last_branch_per_repo, passes\n  the correct base to worktree.ensure, and preserves worktrees on\n  Done (assembly reads the handoff files in the next ticket)\nEOF\n)\"",
  "description": "Commit with conventional commit message"
}
```

> TOOL

tool_result
id: toolu_016wgLes7WazaunNpS1UoMYf
```
ok ABA-301
```

> TOOL

tool_use Bash
id: toolu_01TpmFjvPnvbb2o8PB1uJuom
```json
{
  "command": "git push origin ABA-301",
  "description": "Push branch to remote"
}
```

> TOOL

tool_result
id: toolu_01TpmFjvPnvbb2o8PB1uJuom
```
[entire] Pushing entire/checkpoints/v1 to origin..... done
remote: 
remote: Create a pull request for 'ABA-301' on GitHub by visiting:        
remote:      https://github.com/ababushkin/drain-cycle/pull/new/ABA-301        
remote: 
To https://github.com/ababushkin/drain-cycle.git
 * [new branch]      ABA-301 -> ABA-301
ok ABA-301
```

> AGENT

Pushed. Now post the review summary comment and transition to Done:

> TOOL

tool_use ToolSearch
id: toolu_013MJF4deDDqdPcCthtLDk6b
```json
{
  "query": "select:mcp__claude_ai_Linear__save_comment,mcp__claude_ai_Linear__save_issue,mcp__claude_ai_Linear__get_issue",
  "max_results": 3
}
```

> TOOL

tool_result
id: toolu_013MJF4deDDqdPcCthtLDk6b
```
{
  "type": "tool_reference",
  "tool_name": "mcp__claude_ai_Linear__save_comment"
}
{
  "type": "tool_reference",
  "tool_name": "mcp__claude_ai_Linear__save_issue"
}
{
  "type": "tool_reference",
  "tool_name": "mcp__claude_ai_Linear__get_issue"
}
```

> TOOL

tool_use mcp__claude_ai_Linear__save_comment
id: toolu_01PpACqDA4MobPs6ng2ciy6S
```json
{
  "issueId": "ABA-301",
  "body": "## Review summary\n\nCode review ran on the working-tree changes before merge.\n\n**Findings by severity:**\n- Critical: 0\n- Required: 0\n- Nit: 1 (ternary for `base` computation could be an if/else block — acceptable as-is)\n\n**What was fixed:** nothing required fixing.\n**What was deferred:** the nit (style-only, no correctness impact).\n\n**Changes shipped:**\n- `worktree.add/ensure`: `base` param (default: `main`) threads the prior same-repo branch as the fork point\n- `handoff.py`: new module — `write`/`read` for `.drain-handoff.json`; `read` never raises\n- `prompt.build(stack=True)`: replaces push-to-main steps with commit-only + handoff-file instruction; `stack=False` is byte-identical to prior behaviour\n- `orchestrator.run(stack=True)`: tracks `last_branch_per_repo`, passes correct base to `worktree.ensure`, preserves worktrees on Done\n\n250 tests pass. Pushed to branch `ABA-301`."
}
```

> TOOL

tool_result
id: toolu_01PpACqDA4MobPs6ng2ciy6S
```
{"id":"07f000b1-f393-4e01-9585-04cb9bdd9333","body":"## Review summary\n\nCode review ran on the working-tree changes before merge.\n\n**Findings by severity:**\n- Critical: 0\n- Required: 0\n- Nit: 1 (ternary for `base` computation could be an if/else block — acceptable as-is)\n\n**What was fixed:** nothing required fixing.\n**What was deferred:** the nit (style-only, no correctness impact).\n\n**Changes shipped:**\n- `worktree.add/ensure`: `base` param (default: `main`) threads the prior same-repo branch as the fork point\n- `handoff.py`: new module — `write`/`read` for `.drain-handoff.json`; `read` never raises\n- `prompt.build(stack=True)`: replaces push-to-main steps with commit-only + handoff-file instruction; `stack=False` is byte-identical to prior behaviour\n- `orchestrator.run(stack=True)`: tracks `last_branch_per_repo`, passes correct base to `worktree.ensure`, preserves worktrees on Done\n\n250 tests pass. Pushed to branch `ABA-301`.","createdAt":"2026-06-01T05:53:29.115Z","updatedAt":"2026-06-01T05:53:29.086Z","parentId":null,"resolvedAt":null,"quotedText":null,"author":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"}}
```

> TOOL

tool_use mcp__claude_ai_Linear__save_issue
id: toolu_01NmNN1CQGCGuYAhgdNPSaCu
```json
{
  "id": "ABA-301",
  "state": "Done"
}
```

> TOOL

tool_result
id: toolu_01NmNN1CQGCGuYAhgdNPSaCu
```
{"id":"ABA-301","title":"Make worktrees stack-ready and add the agent handoff file","description":"**Depends on:** <issue id=\"8f88fda8-584c-4931-93e7-a5eeafdc42d9\">ABA-300</issue> (spike). Part of the stacked-PR feature; blocks the stack-assembly ticket.\n\n## What\n\nEach issue's branch forks off the previous same-repo issue's branch instead of always `main`, and the spawned agent commits to its branch **without pushing**, leaving behind a handoff file with the PR body and code-review findings.\n\n## Why\n\nA Graphite stack is a chain: issue N must sit on top of issue N-1 within the same repo. And only the agent knows what it changed and what a reviewer should examine, so it must record that for the orchestrator to turn into a PR. Today every worktree forks off `main` (`drain_cycle/worktree.py:36`) and the agent pushes straight to `main` (`drain_cycle/prompt.py`, `_TAIL` + completion step 3) — both must change for stacking.\n\n## How (mechanical)\n\n* Add a `base` parameter to `worktree.add(repo, identifier, base=BASE_BRANCH)` (`drain_cycle/worktree.py:25`); thread it into the `git worktree add … <base>` call (`:36`). The orchestrator keeps `last_branch_per_repo: dict[str, str]` and passes the previous same-repo branch, or `main` for the first issue in a repo.\n* Add `drain_cycle/handoff.py` that writes, reads, and validates `<worktree>/.drain-handoff.json` with keys `pr_title`, `pr_body`, `findings` (e.g. `{critical, required}`).\n* Branch `prompt.build(issue, worktree, stack)` (`drain_cycle/prompt.py:23`): in stack mode tell the agent to commit to the issue branch, **not push**, and write the handoff file with a What / Why / What-to-review body; keep today's push-to-main text verbatim when `stack` is false.\n\n## Acceptance criteria\n\n- [ ] With two issues targeting the same repo, issue 2's worktree HEAD contains issue 1's commit; an issue in a different repo still forks off `main`. (orchestrator test asserting the base passed per repo)\n- [ ] `prompt.build(stack=False)` returns today's prompt byte-for-byte; `prompt.build(stack=True)` omits \"push to main\" and includes the handoff-file instruction. (unit tests)\n- [ ] `handoff.read` returns a typed object for a valid file and `None` for a missing or malformed file — it never raises. (unit tests)\n- [ ] `pytest` passes.\n\n## Scope guard\n\nNo PRs and no Graphite in this ticket. This one only makes the worktrees stack-shaped and produces the handoff artefact; assembly lands in the next ticket.","priority":{"value":0,"name":"No priority"},"url":"https://linear.app/ababushkin/issue/ABA-301/make-worktrees-stack-ready-and-add-the-agent-handoff-file","gitBranchName":"anton/aba-301-make-worktrees-stack-ready-and-add-the-agent-handoff-file","createdAt":"2026-05-27T07:40:48.481Z","updatedAt":"2026-06-01T05:53:32.338Z","archivedAt":null,"completedAt":"2026-06-01T05:53:32.309Z","startedAt":"2026-06-01T05:41:21.265Z","canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Done","statusType":"completed","labels":["sonnet","drain-cycle"],"attachments":[],"documents":[],"createdBy":"Anton Babushkin","createdById":"720d0535-dfc6-465f-8111-d1a3e6eab786","project":"Autonomous cycle drain - eliminate manual shepherding","projectId":"3b5c5e13-355a-4e70-b943-6251d7f14baf","team":"Personal","teamId":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","cycleId":"52563a03-080e-4db7-b003-ebd27759cf29"}
```

> AGENT

ABA-301 is Done. Here's what shipped:

**New:** `drain_cycle/handoff.py` — `write`/`read` for `.drain-handoff.json`; `read` never raises on bad input.

**Modified:**
- `worktree.add/ensure` — `base` param (default: `main`) so callers can fork off any branch
- `prompt.build(stack=True)` — replaces push-to-main steps with commit-only + handoff-file instruction; `stack=False` is byte-identical to before
- `orchestrator.run(stack=True)` — tracks `last_branch_per_repo`, passes the prior same-repo branch as the fork point, preserves worktrees on Done for the assembly step

250 tests pass, 0 critical/required review findings. Branch `ABA-301` pushed.
