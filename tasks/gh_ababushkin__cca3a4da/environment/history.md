> DEVELOPER

my last run of drain-cycle looks like it stalled, have a look at this log message:

16:42:58 ABA-394  turn 43 · 3.9M tok (peak 121k) · 8m
16:43:05 ABA-394  turn 44 · 4.1M tok (peak 121k) · 8m
16:43:10 ABA-394  not-Done with commits: spawning finishing sub-agent

however the watch output showed me that it exited:

*Stop-guard satisfied**
- `exec-state.json` now carries the `finish` section with `pr_urls: ["https://github.com/ababushkin/agent-skills-shaper/pull/56"]` (commit `0f2f6a8`).
- Branch `ABA-394` is up to date with `origin/ABA-394`; both commits (`a7ecf78` skill rebalance, `0f2f6a8` exec-state finish) are pushed.

**Linear status**
Left at **In Progress** with the review-summary comment posted (id `c6800e18…`). Per repo governance ("not Done until committed and pushed to main") the issue should transition to Done only after PR #56 merges. Flagging this rather than transitioning early.

=== done: 45 turns, $4.07 ===

> AGENT

I'll dig into the actual drain-cycle code to understand what happened here. Let me look at the orchestrator's completion/halt logic.

> TOOL

tool_use Bash
id: toolu_01MrZfHFMRP6yPgBmPtjHoWK
```json
{
  "command": "git log --oneline -8 && echo \"---\" && rg -l \"spawning finishing sub-agent|not-Done with commits|finishing sub-agent\" --type py",
  "description": "Find source of the log message"
}
```

> TOOL

tool_result ERROR
id: toolu_01MrZfHFMRP6yPgBmPtjHoWK
```
Exit code 2
a7e5f5a chore: untrack stray exec-state.json drain artefact
8c6b717 chore(ABA-334): record pr_urls, outcome_verdict, prep_verdict in exec-state.json
d2178b6 feat(ABA-334): grade reads confirmed grade files, exits nonzero on silent-Done violations
253ebfe feat(ABA-401): drop legacy .drain-handoff.json; exec-state.json is the only state file (#32)
0b4b2b7 Merge remote-tracking branch 'origin/main' into ABA-401
ff54ab0 fix(ABA-401): read the sectioned exec-state.json contract
4a1584e fix(worktree): trust mise config in created worktrees
ec3067c feat(ABA-401): drop legacy .drain-handoff.json; exec-state.json is the only state file
---
grep: unrecognized option `--type'
usage: grep [REDACTED] [-A num] [-B num] [-C[num]]
	[-e pattern] [-f file] [--binary-files=value] [--color=when]
	[--context[=num]] [--directories=action] [--label] [--line-buffered]
	[--null] [pattern] [file ...]
```

> TOOL

tool_use Bash
id: toolu_014KG6NoLDcHKcLyMrbBYZRC
```json
{
  "command": "rg -rn \"not-Done with commits|spawning finishing|finishing sub-agent|finishing subagent\" .",
  "description": "Locate the log string across repo"
}
```

> TOOL

tool_result ERROR
id: toolu_014KG6NoLDcHKcLyMrbBYZRC
```
Exit code 1
```

> TOOL

tool_use Bash
id: toolu_017rpCMiymV4t7Cc7otYgBYi
```json
{
  "command": "grep -rn \"spawning finishing\\|not-Done with commits\\|finishing sub-agent\\|finishing subagent\\|not-Done\" --include=*.py . | head -40",
  "description": "Search python files for log strings"
}
```

> TOOL

tool_result
id: toolu_017rpCMiymV4t7Cc7otYgBYi
```
(eval):1: no matches found: --include=*.py
```

> TOOL

tool_use Bash
id: toolu_01LEQQmz2UyjAMQmAjEK5ort
```json
{
  "command": "grep -rn \"spawning finishing\" . 2>/dev/null | head; echo \"===\"; grep -rn \"not-Done\" . 2>/dev/null | head; echo \"===\"; grep -rn \"finishing sub-agent\" . 2>/dev/null | head",
  "description": "Grep for the log strings"
}
```

> TOOL

tool_result
id: toolu_01LEQQmz2UyjAMQmAjEK5ort
```
<persisted-output>
Output too large (50.9KB). Full output saved to: /Users/anton/.claude/projects/-Users-anton-src-drain-cycle/75418cc5-ca2f-42e9-9cbf-74ba261dd2d7/tool-results/b54bipw77.txt

Preview (first 2KB):
Binary file ./drain_cycle/__pycache__/orchestrator.cpython-312.pyc matches
Binary file ./drain_cycle/__pycache__/orchestrator.cpython-314.pyc matches
./drain_cycle/orchestrator.py:734:                    identifier, "not-Done with commits: spawning finishing sub-agent"
./drain_cycle/orchestrator.py:786:                        identifier, "Done but no pr_urls: spawning finishing sub-agent"
Binary file ./.worktrees/ABA-334/drain_cycle/__pycache__/orchestrator.cpython-312.pyc matches
./.worktrees/ABA-334/drain_cycle/orchestrator.py:734:                    identifier, "not-Done with commits: spawning finishing sub-agent"
./.worktrees/ABA-334/drain_cycle/orchestrator.py:786:                        identifier, "Done but no pr_urls: spawning finishing sub-agent"
./.entire/metadata/df5bb8bc-fa36-4eb3-aa39-d909ccadf357/full.jsonl:194:{"parentUuid":"91561060-e59f-49e8-9fbd-a37a8151981f","isSidechain":false,"promptId":"b446cf24-17fc-44e9-acce-a807f537a148","type":"user","message":{"role":"user","content":[{"tool_use_id":"toolu_013uvq15eQuKQCoYrmRSFmmx","type":"tool_result","content":"drain_cycle/orchestrator.py | 224 +++++++++++++++++++++++++++++++++++++++++---\n 1 file changed, 210 insertions(+), 14 deletions(-)\n\n--- Changes ---\n\ndrain_cycle/orchestrator.py\n  @@ -10,7 +10,8 @@ from __future__ import annotations\n  -from dataclasses import dataclass, field\n  +import subprocess\n  +from dataclasses import dataclass, field, replace as dataclass_replace\n   from datetime import datetime, timezone\n   from pathlib import Path\n   from typing import Callable, TextIO\n  @@ -31,18 +32,53 @@ _DEBUG_ENV_VAR = \"DRAIN_CYCLE_DEBUG\"\n  -See ``docs/design-decisions.md`` §10.\"\"\"\n  +See ``docs/adrs/0014-worktree-config-symlink.md``.\"\"\"\n   _UNRESOLVED_WORKTREE_DISPLAY = \"<unresolved>\"\n   \"\"\"Worktree-path placeholder for the pre-spawn resolution-halt path.\n   No path has been chosen yet — the issue couldn't be mapped to a target\n   repo — so the run-log entry and stderr 
...
</persisted-output>
```

> AGENT

Let me read the relevant orchestrator logic around the finishing sub-agent spawn.

> TOOL

tool_use Read
id: toolu_01DVBt3KZbbzzaLntYenKqgT
```json
{
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/orchestrator.py",
  "offset": 680,
  "limit": 160
}
```

> TOOL

tool_result
id: toolu_01DVBt3KZbbzzaLntYenKqgT
```
680	            # The worker crossed a per-issue cap (tokens or time) and was
681	            # process-group killed (grandchildren reaped). Same revert + halt
682	            # contract as a not-Done exit, with the recorded usage of the
683	            # killed session and the breached cap named in the halt reason.
684	            original_state_name = issue["state"]["name"]
685	            effective_state, revert_error = _revert_to_pre_halt_state(
686	                issue["id"],
687	                target_state_name=original_state_name,
688	                pre_revert_state_name=_IN_PROGRESS_STATE_NAME,
689	            )
690	            halt_reason = (
691	                f"{_halt_message(identifier, effective_state, worktree_path)}"
692	                f" — {result.breach.describe()}"
693	            )
694	            if revert_error is not None:
695	                halt_reason += (
696	                    f"; revert to {original_state_name!r} failed: {revert_error}"
697	                )
698	            issue_span.set_attribute("issue.exit_code", result.exit_code)
699	            _set_verdict_span_attrs(issue_span, outcome)
700	            halt_ctx.record(
701	                slug="err-per-issue-breach",
702	                halt_reason=halt_reason,
703	                final_linear_state=effective_state,
704	                worktree_path=str(worktree_path),
705	                finished_at=finished_at,
706	                exit_code=result.exit_code,
707	                outcome=outcome,
708	            )
709	            return 1, pane_id
710	
711	        refreshed = linear.get_issue(issue["id"])
712	        post_spawn_state = refreshed["state"]["name"]
713	        is_done = refreshed["state"]["type"] == _DONE_STATE_TYPE
714	        issue_span.set_attribute("issue.exit_code", result.exit_code)
715	        issue_span.set_attribute("issue.is_done", is_done)
716	
717	        finishing_runs: list[dict] = []
718	        finishing_attempted = False
719	
720	        # Recovery: committed-but-unfinished → spawn a sonnet finishing sub-agent
721	        # before halting. Fires only when the branch has commits beyond base (an
722	        # empty or uncommitted-only branch is a genuine failure), the verifier did […]

> AGENT

Let me check the `handoff.read` contract and whether the not-Done path ever consults existing `pr_urls`.

> TOOL

tool_use Bash
id: toolu_01DhCvab99QK1bxpvWGFQdJS
```json
{
  "command": "grep -rn \"def read\\b\\|def read_partial\\|def read(\" drain_cycle/handoff.py 2>/dev/null | head; echo \"===\"; sed -n '1,60p' drain_cycle/handoff.py 2>/dev/null",
  "description": "Inspect handoff module read functions"
}
```

> TOOL

tool_result
id: toolu_01DhCvab99QK1bxpvWGFQdJS
```
drain_cycle/handoff.py:145:def read(worktree: Path) -> HandoffData | None:
drain_cycle/handoff.py:157:def read_partial(
===
"""Handoff artefact a stack-mode worker leaves behind after submitting PRs.

In stack mode the worker drives PR submission itself via the ``pr-finishing``
skill, which runs ``gt``/``gh`` inside the worktree, posts the Linear
review-summary comment, and records the submitted PRs in ``exec-state.json``
(the pack-named file). The pack writes that file as a set of phase-keyed
sections — ``pickup``, ``breakdown``, ``build``, ``review``, ``verify``,
``finish`` — each skill owning its own section (ADR 0030). The orchestrator
reads two of those sections back: ``finish.pr_urls`` as its submission-confirmation
signal — a present, non-empty list means the skill submitted at least one PR;
its absence means submission never completed and the per-repo chain must halt —
and the ``verify`` section, which it maps to its ``outcome_verdict`` for the
run-log and the verifier-fail gate.

``read`` reads the sectioned ``exec-state.json`` — the only state file. The
legacy flat ``.drain-handoff.json`` has been dropped. A missing or structurally
invalid file returns ``None``.

``outcome_verdict`` is derived from the pack's ``verify`` section: a ``FAIL``
verdict maps to ``result == "fail"`` with the failed AC items as ``findings``.
``read_partial`` extracts that verdict without the ``pr_urls`` validity gate, so
halt […]

> AGENT

Confirmed the root cause. Here's what happened — it's not really a stall, it's a **redundant finishing sub-agent spawn** caused by a collision between worker governance and the orchestrator's completion heuristic.

## What happened

Your worker finished **correctly and completely**:
- Ran `/shape:pr-finishing`, opened PR #56, pushed both commits
- Wrote `exec-state.json` with `finish.pr_urls: [...PR#56]`
- Posted the Linear review-summary comment
- **Deliberately left the issue at "In Progress"** — per repo governance ("not Done until committed and pushed to *main*"), it correctly refused to transition to Done before PR #56 merges. That's the `=== done: 45 turns, $4.07 ===` clean exit you saw in the watch pane.

Then the orchestrator re-read Linear (orchestrator.py:711) and hit this gate:

```python
# orchestrator.py:726
if not is_done and _commits_beyond_base(worktree_path, base):
    ...
    console.worker_event(identifier, "not-Done with commits: spawning finishing sub-agent")
```

The check is only **(Linear state ≠ Done) AND (branch has commits)**. Both are true — because the worker *correctly* left it In Progress and *correctly* has commits. So the orchestrator concludes "committed but unfinished" and spawns a sonnet finishing sub-agent (orchestrator.py:737) to redo work that was already done. That redundant agent re-running `pr-finishing` against an already-submitted branch is the "stall" you're seeing.

## […]

> DEVELOPER

also the linear ticket was marked as done, where as it should have been left in progress - i can't tell if thats an issue with linear or something else - i also see this file in the repo: .drain-guard-tripped

> AGENT

Let me investigate both — the `.drain-guard-tripped` file and what marked the ticket Done.

> TOOL

tool_use Bash
id: toolu_01EiHuXwazaJHRgDiEDLX7Bk
```json
{
  "command": "ls -la .drain-guard-tripped 2>/dev/null && echo \"=== CONTENT ===\" && cat .drain-guard-tripped 2>/dev/null; echo; echo \"=== writers ===\"; grep -rn \"drain-guard-tripped\\|guard-tripped\\|guard_tripped\" . 2>/dev/null | grep -v \"Binary\\|.pyc\\|.entire\\|.worktrees\" | head -20",
  "description": "Inspect guard-tripped file and its writers"
}
```

> TOOL

tool_result
id: toolu_01EiHuXwazaJHRgDiEDLX7Bk
```
644  .drain-guard-tripped  85B
=== CONTENT ===
uncommitted changes in worktree, no valid .drain-handoff.json after 1 re-injection(s)
=== writers ===
./.pytest_cache/v/cache/nodeids:223:  "tests/test_orchestrator_halt.py::test_orchestrator_halt_reason_includes_stop_guard_tripped_marker",
./tests/test_stop_guard.py:60:        f"{stop_guard.MARKER_FILE}\n.drain-guard-tripped\n"
./tests/test_stop_guard.py:89:        f"{stop_guard.MARKER_FILE}\n.drain-guard-tripped\n"
./tests/test_stop_guard.py:105:        f"{stop_guard.MARKER_FILE}\n.drain-guard-tripped\n"
./tests/test_orchestrator_halt.py:142:def test_orchestrator_halt_reason_includes_stop_guard_tripped_marker(
./tests/test_orchestrator_halt.py:148:    ``.drain-guard-tripped`` in the worktree on its way out. The
./tests/test_orchestrator_halt.py:169:    tripped_file = worktree_path / ".drain-guard-tripped"
./docs/adrs/0029-stop-guard-via-settings.md:7:The orchestrator plants `.drain-guard.json` before each spawn and reads `.drain-guard-tripped` after (the stop-guard mechanism), but the Stop hook that increments the marker and writes the tripped file — `drain-cycle _stop-guard` — only ran when the target repo's own tracked `.claude/settings.json` happened to register it. In a repo that didn't (the common case), nothing invoked `stop_guard.run()`: the marker stayed at `count: 0`, no tripped file appeared, and a worker that stopped mid-completion exited cleanly with the work uncommitted. The guard designed to catch a premature stop was inert, so the run halted with the generic not-Done line and no signal that the work had been finished but not captured.
./.gitignore:7:.drain-guard-tripped
./drain_cycle/stop_guard.py:16:gives up, writes ``.drain-guard-tripped`` with the observed state, and
./drain_cycle/stop_guard.py:34:TRIPPED_FILE = ".drain-guard-tripped"
./drain_cycle/stop_guard.py:121:    ``.drain-guard.json``, ``.drain-guard-tripped``, ``exec-state.json``
```

> TOOL

tool_use Read
id: toolu_01Vox4sZywnbGiNQtDRYVFif
```json
{
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/stop_guard.py"
}
```

> TOOL

tool_result
id: toolu_01Vox4sZywnbGiNQtDRYVFif
```
1	"""Stop-hook guard for spawned drain workers.
2	
3	A ``claude -p`` session that loads a "report findings / await input" skill
4	can end its turn before the completion sequence (commit + handoff + Linear
5	comment + Done) runs. The session exits cleanly with the implementation
6	green but uncommitted, and the orchestrator only sees a generic not-Done
7	halt with no signal that the work was finished.
8	
9	This module is the Stop hook the worker session runs at end-of-turn. It
10	fires only when the orchestrator has planted ``.drain-guard.json`` in the
11	worktree root, so interactive sessions and non-drain runs are a silent
12	no-op. When the marker is present and the session is trying to stop with
13	work still uncaptured (dirty tree or, in stack mode, no valid
14	``exec-state.json``), it returns ``decision: block`` to push the agent
15	through the completion sequence. After ``max_blocks`` re-injections it
16	gives up, writes ``.drain-guard-tripped`` with the observed state, and
17	lets the session exit — the orchestrator reads that marker and tags the
18	halt as ``worker_stopped_incomplete`` rather than the generic not-Done
19	line.
20	"""
21	from __future__ import annotations […]

> AGENT

Let me check the finishing sub-agent's prompt — that's likely what marked the ticket Done.

> TOOL

tool_use Bash
id: toolu_019BTzUWPTzEBd8kdRjzwwS5
```json
{
  "command": "grep -rn \"def build_finishing\" drain_cycle/prompt.py; echo \"===\"; awk '/def build_finishing/,/^def [a-z]/' drain_cycle/prompt.py | head -80",
  "description": "Read build_finishing prompt"
}
```

> TOOL

tool_result
id: toolu_019BTzUWPTzEBd8kdRjzwwS5
```
drain_cycle/prompt.py:76:def build_finishing(identifier: str, worktree: Path, base: str) -> str:
===
def build_finishing(identifier: str, worktree: Path, base: str) -> str:
```

> TOOL

tool_use Read
id: toolu_01Q5FgBeDU9zFbJdA22c1jkW
```json
{
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/prompt.py",
  "offset": 76,
  "limit": 70
}
```

> TOOL

tool_result
id: toolu_01Q5FgBeDU9zFbJdA22c1jkW
```
76	def build_finishing(identifier: str, worktree: Path, base: str) -> str:
77	    """Build a finishing-only prompt for a committed-but-unfinished issue.
78	
79	    The implementation is already committed. The agent runs review → fix →
80	    pr-finishing → Done. It must not re-implement or add commits beyond those
81	    needed to fix Critical/Required review findings.
82	    Critical/Required fixes are delegated to ``_FINISHING_OPUS_MODEL`` sub-agents.
83	    """
84	    if base == "main":
85	        base_clause = ""
86	    else:
87	        base_clause = (
88	            f" These commits are stacked on `{base}`, not `main`, so pass "
89	            f"`{base}` to the skill as its base branch (it slices `{base}..HEAD`)."
90	        )
91	    return (
92	        f"# Finishing incomplete issue {identifier}\n\n"
93	        f"The implementation for this issue is already committed on this branch. "
94	        f"Run `git log --oneline {base}..HEAD` to see the committed work.\n\n"
95	        "Your only task is to run the finishing protocol below. Do not "
96	        "re-implement, redesign, or add commits beyond those needed to fix "
97	        "Critical/Required review findings.\n\n"
98	        "---\n\n"
99	        f"Finishing instructions for issue {identifier}:\n"
100	        f"- Working directory: {worktree}\n"
101	        f"- Base branch: {base}\n"
102	        "- Steps (run in order, before marking Done):\n"
103 […]

> AGENT

Both questions answered — and they're the **same bug** as before, plus an unrelated stale file.

## The Linear ticket marked Done — not a Linear issue, drain-cycle did it

It was the redundant finishing sub-agent. The `build_finishing` prompt (prompt.py:117) hard-codes:

```
6. Transition issue to Done via mcp__claude_ai_Linear__save_issue (state: "Done").
```

Its only escape hatch (prompt.py:114) is "if the skill *could not submit*, leave In Progress." But PR #56 was already submitted and `pr_urls` was already in `exec-state.json` — so step 5 passed and step 6 dutifully marked it **Done**.

So the full chain is:

1. **Original worker** ran `exec:pickup` with governance awareness ("not Done until merged to *main*"), opened PR #56, recorded `pr_urls`, and **deliberately left the issue In Progress**, posting "should transition to Done only after PR #56 merges."
2. **Orchestrator misfired** (orchestrator.py:726, the missing `pr_urls` guard from my first answer) → spawned the finishing sub-agent.
3. **Finishing sub-agent** saw `pr_urls` present and, per its prompt, **flipped the issue to Done** — overriding the exact governance decision the original worker got right.

This is a **governance contradiction baked into two prompts:**
- Worker / `exec:pickup`: *not Done until merged to main* → leave In Progress
- `build_finishing` […]

> DEVELOPER

the watcher also never showed me the sub-agent and the drain-cycle process is still "stuck" as if its in progress

> AGENT

Let me check whether the process is actually still alive and how the sub-agent output is (not) being routed to the watch pane.

> TOOL

tool_use Bash
id: toolu_01WjiEHWE6n1KASGsW3YbrYD
```json
{
  "command": "ps aux | grep -i \"drain\\|claude -p\\|run_issue\" | grep -v grep | head -20",
  "description": "Check for live drain-cycle / worker processes"
}
```

> TOOL

tool_result
id: toolu_01WjiEHWE6n1KASGsW3YbrYD
```
anton             6785   0.7  0.8 508564512 561664   ??  Ss    4:43PM   0:03.76 claude -p --dangerously-skip-permissi...
```

> TOOL

tool_use Bash
id: toolu_01WiP6F5kJUs6Aa5FTp9rSEQ
```json
{
  "command": "grep -n \"class AgentSink\\|class.*Sink\\|def worker_event\\|AgentSink\\|def passthrough\\|watch\\|pane\" drain_cycle/console.py 2>/dev/null | head -40",
  "description": "Inspect console sinks and watch-pane routing"
}
```

> TOOL

tool_result
id: toolu_01WiP6F5kJUs6Aa5FTp9rSEQ
```
3 matches in 1 files:

drain_cycle/console.py:15::class:`AgentSink` so it is visually distinct from orchestrator lines.
drain_cycle/console.py:51:def worker_event(identifier: str, message: str) -> None:
drain_cycle/console.py:123:class AgentSink:
```

> AGENT

Live process confirmed: **PID 6785, a `claude -p` started at 4:43PM with only 3.76s CPU** — that's the finishing sub-agent, spawned at 16:43:10 and still alive, idle/hung (not spinning). The orchestrator is blocked in `worker.run_issue` waiting on it. Let me see why the time cap didn't kill it and why the watch pane never showed it.

> TOOL

tool_use Read
id: toolu_01M4ashdAjCa9urfkXwGwJqy
```json
{
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/console.py",
  "offset": 110,
  "limit": 60
}
```

> TOOL

tool_result
id: toolu_01M4ashdAjCa9urfkXwGwJqy
```
110	    table.add_row("Issues done", f"{issues_done}/{issues_total}")
111	    if halted_on is not None:
112	        table.add_row("Halted on", halted_on)
113	    table.add_row("Cost", "n/a" if cost_usd is None else f"${cost_usd:.2f}")
114	    table.add_row("Tokens", fmt_tokens(tokens))
115	    table.add_row("Elapsed", fmt_elapsed(elapsed_seconds))
116	    table.add_row("Run log", run_log_path)
117	    c.rule()
118	    c.print(table)
119	    for step in next_steps:
120	        c.print(f"  [dim]→[/dim] {step}")
121	
122	
123	class AgentSink:
124	    """File-like wrapper that routes ``print``/``write`` output through
125	    :func:`agent_line`, line-buffered.
126	
127	    The orchestrator hands an instance to ``worker.run_issue`` via its
128	    ``passthrough`` parameter so agent non-JSON output flows through the same
129	    Rich console as orchestrator events, with the ``│`` indent prefix. Tests
130	    that need to assert on raw agent output continue to pass an ``io.StringIO``
131	    instead.
132	    """
133	
134	    def __init__(self) -> None:
135	        self._buf = ""
136	
137	    def write(self, s: str) -> int:
138	        if not s:
139	            return 0
140	        self._buf += s
141	        while "\n" in self._buf:
142	            line, self._buf = self._buf.split("\n", 1)
143	            if line:
144	                agent_line(line)
145	        return len(s)
146	
147	    def flush(self) -> None:
148	        if self._buf:
149	            agent_line(self._buf)
150	            self._buf = ""
151	
```

> TOOL

tool_use Bash
id: toolu_015q7w52pM3nDVGcxPBgaknN
```json
{
  "command": "grep -n \"def run_issue\\|time_limit\\|token_limit\\|cost_limit\\|kill\\|terminate\\|poll\\|wait\\|TimeoutExpired\\|signal\\|killpg\\|monotonic\\|deadline\\|passthrough\\|watch\\|fifo\\|tee\" drain_cycle/worker.py 2>/dev/null | head -50",
  "description": "Inspect worker.run_issue cap enforcement"
}
```

> TOOL

tool_result
id: toolu_015q7w52pM3nDVGcxPBgaknN
```
81 matches in 1 files:

drain_cycle/worker.py:5:wire, and how it is force-terminated when it overruns the per-issue time cap.
drain_cycle/worker.py:6:Normally the session is a subprocess this module spawns. In watch mode the
drain_cycle/worker.py:9:the parser and breach monitor are identical, only the launch and kill
drain_cycle/worker.py:33:from the accumulated per-turn stream, which is also what survives a kill
drain_cycle/worker.py:37:``claude`` as ``--max-budget-usd`` so the session self-terminates on cost
drain_cycle/worker.py:39:suspenders: a poll loop watches the live cumulative-token tally and the
drain_cycle/worker.py:42:off the worker simply waits for the session to exit on its own. A crossed
drain_cycle/worker.py:46:**Process-group kill.** The worker is launched with
drain_cycle/worker.py:48:the whole group is SIGKILLed via ``os.killpg``, reaping grandchildren —
drain_cycle/worker.py:49:MCP servers, sub-agents — that a kill of the direct child alone would
drain_cycle/worker.py:51:deliberately: a session being force-terminated past a guardrail has no
drain_cycle/worker.py:52:clean-shutdown work worth waiting for, and SIGKILL is the only signal a
drain_cycle/worker.py:61:import signal
drain_cycle/worker.py:96:"""Bound on waiting for the stdout-reader thread to drain to EOF after the
drain_cycle/worker.py:99:pathological case of a group member that somehow escaped the kill, so the
drain_cycle/worker.py:105:most one interval before the kill lands; one second is responsive enough for
drain_cycle/worker.py:106:a session measured in minutes and cheap enough to poll."""
drain_cycle/worker.py:120:``exit_code`` is the […]

> TOOL

tool_use Read
id: toolu_01Drn7DeTEmB6brhrECHWJjb
```json
{
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/worker.py",
  "offset": 200,
  "limit": 140
}
```

> TOOL

tool_result
id: toolu_01Drn7DeTEmB6brhrECHWJjb
```
200	
201	def run_issue(
202	    *,
203	    claude_cmd: list[str],
204	    model: str,
205	    prompt: str,
206	    cwd: Path,
207	    token_limit: int | None,
208	    time_limit_seconds: float | None,
209	    cost_limit_usd: float | None,
210	    passthrough: TextIO | None = None,
211	    debug_file: Path | None = None,
212	    poll_interval_seconds: float = _POLL_INTERVAL_SECONDS,
213	    on_progress: Callable[[int, int, int, float | None, float], None] | None = None,
214	    external_stream: TextIO | None = None,
215	    kill_fn: Callable[[], None] | None = None,
216	) -> WorkerResult:
217	    """Run one streaming ``claude -p`` session and return its usage.
218	
219	    Two execution paths share the same usage parser, breach monitor, and
220	    result shape:
221	
222	    * **Spawned (default).** ``external_stream is None``: the worker builds
223	      the argv (see :func:`build_argv`) and launches ``claude`` in its own
224	      process group, reading the merged stdout/stderr pipe. On a token/time
225	      breach the whole group is SIGKILLed.
226	    * **External (watch mode).** ``external_stream`` is an already-open stream
227	      of the session's stream-json — drain-cycle reads it while the *same*
228	      bytes scroll in a tmux pane that owns the ``claude`` process. No
229	      subprocess is spawned here; on a breach ``kill_fn`` […]

> TOOL

tool_use Bash
id: toolu_01ShbiKbbgKuzMZC2VLSj4he
```json
{
  "command": "grep -n \"def _monitor\" drain_cycle/worker.py; sed -n '/def _monitor/,/return None/p' drain_cycle/worker.py | head -70",
  "description": "Read _monitor cap loop"
}
```

> TOOL

tool_use Bash
id: toolu_01K44pSsYtts217enWPWBnJT
```json
{
  "command": "grep -rn \"per_issue_seconds\\|per_issue_tokens\\|per_issue_cost\\|time_limit\\|PerIssue\\|class Limits\\|per-issue\" drain_cycle/*.py | grep -iv \"def run_issue\" | head -40",
  "description": "Find per-issue limit defaults"
}
```

> TOOL

tool_result
id: toolu_01ShbiKbbgKuzMZC2VLSj4he
```
1 matches in 1 files:

drain_cycle/worker.py:377:def _monitor(
def _monitor(
    wait: Callable[[float | None], bool],
    accumulator: _UsageAccumulator,
    *,
    started: float,
    token_limit: int | None,
    time_limit_seconds: float | None,
    poll_interval_seconds: float,
) -> Breach | None:
    """Wait for the session, returning the per-issue cap it breaches (if any).

    ``wait(timeout)`` blocks up to ``timeout`` seconds (``None`` = until
    completion) and returns ``True`` once the session has finished — a thin
    seam over ``proc.wait`` (spawned path) or the reader thread reaching EOF
    (external path). With both caps off there is nothing to watch for, so we
    block until completion. Otherwise we wake every ``poll_interval_seconds``
    to compare the live cumulative-token tally and elapsed wall-clock against
    the caps; the first crossed cap is returned for the caller to kill on.
    Returns ``None`` when the session finishes on its own first.
    """
    if token_limit is None and time_limit_seconds is None:
        wait(None)
        return None
```

> TOOL

tool_result
id: toolu_01K44pSsYtts217enWPWBnJT
```
drain_cycle/console.py:11:* ``ABA-NNN``  — per-issue outcomes (picked, done, progress).
drain_cycle/console.py:52:    """Emit a per-issue event tagged with ``identifier``."""
drain_cycle/grade_draft.py:26:    """Return the directory where per-issue grade files are written.
drain_cycle/limits.py:4:and quota with no ceiling but the outer per-issue timeout. This module
drain_cycle/limits.py:10:* *Native belt* — ``per_issue_cost_usd`` is handed to ``claude`` as
drain_cycle/limits.py:13:* *Orchestrator suspenders* — ``per_issue_tokens`` and ``per_issue_seconds``
drain_cycle/limits.py:19:  what the per-issue caps cannot catch.
drain_cycle/limits.py:47:class LimitsConfigError(RuntimeError):
drain_cycle/limits.py:55:    ``scope`` is ``"per-issue"`` or ``"cycle"``; ``metric`` is ``"token"``,
drain_cycle/limits.py:58:    the operator-facing line — the worker uses it for a per-issue kill and
drain_cycle/limits.py:80:class Limits:
drain_cycle/limits.py:83:    Defaults: per-issue 8M tokens · 20 min · $15; cycle 30M tokens ·
drain_cycle/limits.py:94:    per_issue_tokens: int | None = 8_000_000
drain_cycle/limits.py:95:    per_issue_seconds: float | None = 20 * 60
drain_cycle/limits.py:96:    per_issue_cost_usd: float | None = 15.0
drain_cycle/limits.py:154:    # ``bool`` is a subclass of ``int``; ``per_issue_tokens: true`` would
drain_cycle/orchestrator.py:31:"""Opt-in switch for per-issue ``--debug-file`` capture. Any non-empty value
drain_cycle/orchestrator.py:278:    """Whether per-issue ``--debug-file`` capture is switched on.
drain_cycle/orchestrator.py:297:    The span wrapper is thin so the body keeps its shape; per-issue work nests
drain_cycle/orchestrator.py:390:        # per-issue caps while their sum drains the quota. Check the
drain_cycle/orchestrator.py:593:                cost_limit_usd=limits.per_issue_cost_usd,
drain_cycle/orchestrator.py:655:                token_limit=limits.per_issue_tokens,
drain_cycle/orchestrator.py:656:                time_limit_seconds=limits.per_issue_seconds,
drain_cycle/orchestrator.py:657:                cost_limit_usd=limits.per_issue_cost_usd,
drain_cycle/orchestrator.py:680:            # The worker crossed a per-issue […]

> TOOL

tool_use Read
id: toolu_013X8MXGjUzRahqrfXjP8QQu
```json
{
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/worker.py",
  "offset": 395,
  "limit": 60
}
```

> TOOL

tool_result
id: toolu_013X8MXGjUzRahqrfXjP8QQu
```
395	    Returns ``None`` when the session finishes on its own first.
396	    """
397	    if token_limit is None and time_limit_seconds is None:
398	        wait(None)
399	        return None
400	    while True:
401	        if wait(poll_interval_seconds):
402	            return None
403	        if token_limit is not None:
404	            observed = accumulator.cumulative()
405	            if observed >= token_limit:
406	                return Breach("per-issue", "token", token_limit, observed)
407	        if time_limit_seconds is not None:
408	            elapsed = time.monotonic() - started
409	            if elapsed >= time_limit_seconds:
410	                return Breach("per-issue", "time", time_limit_seconds, elapsed)
411	
412	
413	def _kill_process_group(proc: subprocess.Popen[str]) -> None:
414	    """SIGKILL the worker's whole process group, reaping grandchildren.
415	
416	    No-ops if the leader has already exited (its pid — and thus the group
417	    id — is gone). SIGKILL is sent before the caller reaps the leader, so
418	    the group still exists and its id cannot have been reused.
419	    """
420	    try:
421	        pgid = os.getpgid(proc.pid)
422	    except ProcessLookupError:
423	        return
424	    try:
425	        os.killpg(pgid, signal.SIGKILL)
426	    except ProcessLookupError:
427	        pass
428	
429	
430	def _drain_stream(
431	    stream: TextIO | None,
432	    accumulator: _UsageAccumulator,
433	    sink: TextIO,
434	    on_progress: Callable[[int, int, int, float | None], None] | None = None,
435	) -> None: […]

> AGENT

Let me check the run-log and active limits config to confirm whether a time cap was even in play.

> TOOL

tool_use Bash
id: toolu_01SgSrmDMD9i4NVxUDyLDDtt
```json
{
  "command": "find . -name \"*.jsonl\" -path \"*runlog*\" -o -name \"run-log*\" 2>/dev/null | grep -v entire | head; echo \"=== recent run logs ===\"; ls -lat ~/.drain-cycle/ 2>/dev/null | head; find ~/.drain-cycle -name \"*.json*\" 2>/dev/null | head; echo \"=== limits config ===\"; cat ~/.drain-cycle/limits.* 2>/dev/null; cat ~/.drain-cycle/config.* 2>/dev/null; find . -maxdepth 2 -name \"*.toml\" -o -maxdepth 2 -name \"limits*\" 2>/dev/null | grep -v entire | head",
  "description": "Locate run-log and limits config"
}
```

> TOOL

tool_result
id: toolu_01SgSrmDMD9i4NVxUDyLDDtt
```
=== recent run logs ===
755  runs/
755  grades/
644  repos.yml  377B
644  limits.yml  135B
644  .env  268B
/Users/anton/.drain-cycle/runs/52563a03-080e-4db7-b003-ebd27759cf29-20260601T054139473320Z.json
/Users/anton/.drain-cycle/runs/52563a03-080e-4db7-b003-ebd27759cf29-20260526T100729016200Z.json
/Users/anton/.drain-cycle/runs/793fc9ea-08c7-40c1-8c1b-417efb20adbf-20260610T140220454364Z.json
/Users/anton/.drain-cycle/runs/52563a03-080e-4db7-b003-ebd27759cf29-20260526T100700541279Z.json
/Users/anton/.drain-cycle/runs/52563a03-080e-4db7-b003-ebd27759cf29-20260528T130032809057Z.json
/Users/anton/.drain-cycle/runs/793fc9ea-08c7-40c1-8c1b-417efb20adbf-20260614T081115904202Z.json
/Users/anton/.drain-cycle/runs/9e17380f-9527-40ef-8523-4e4358f12809-20260615T141442258554Z.json
/Users/anton/.drain-cycle/runs/793fc9ea-08c7-40c1-8c1b-417efb20adbf-20260611T111842249473Z.json
/Users/anton/.drain-cycle/runs/52563a03-080e-4db7-b003-ebd27759cf29-20260526T094355176586Z.json
/Users/anton/.drain-cycle/runs/52563a03-080e-4db7-b003-ebd27759cf29-20260526T111721271333Z.json
=== limits config ===
per_issue_tokens: 16000000 # 16 million, double the default
per_issue_seconds: 1800 # 30 minutes, complex tasks can take 20-25 minutes
(eval):1: no matches found: /Users/anton/.drain-cycle/config.*
./pyproject.toml
./mise.toml
./docs/limits.example.yml
./drain_cycle/limits.py
```

> AGENT

Limits config shows `per_issue_seconds: 1800` (30 min) — so a wall-clock cap **is** set. PID 6785 should have been killed at ~17:13. The fact that it survived hours means the monitor isn't watching it. Let me check the process tree — is the parent orchestrator even still alive?

> TOOL

tool_use Bash
id: toolu_011qrkWe6J7GviXHUHKKXzAF
```json
{
  "command": "echo \"=== PID 6785 detail (ppid, pgid, start, cpu) ===\"; ps -o pid,ppid,pgid,sess,stat,lstart,time,command -p 6785 2>/dev/null; echo; echo \"=== parent chain ===\"; PPID=$(ps -o ppid= -p 6785 2>/dev/null | tr -d ' '); echo \"parent pid: $PPID\"; ps -o pid,ppid,stat,lstart,command -p \"$PPID\" 2>/dev/null; echo; echo \"=== any python drain/orchestrator alive? ===\"; ps aux | grep -iE \"python.*drain|drain[-_]cycle|orchestrat\" | grep -v grep; echo; echo \"=== any tmux watch sessions ===\"; tmux ls 2>/dev/null | grep -i drain",
  "description": "Inspect process tree and parentage of the stuck claude process"
}
```

> TOOL

tool_result
id: toolu_011qrkWe6J7GviXHUHKKXzAF
```
=== PID 6785 detail (ppid, pgid, start, cpu) ===
  PID  PPID  PGID   SESS STAT STARTED                           TIME COMMAND

=== parent chain ===
(eval):1: read-only variable: PPID
```

> AGENT

PID 6785's detail came back empty — it may have just exited. Let me re-scan for live processes.

> TOOL

tool_use Bash
id: toolu_016MwfWMkn9n6zDPQVwyx4ZX
```json
{
  "command": "echo \"=== claude -p processes ===\"; ps -o pid,ppid,pgid,stat,lstart,time,command -ax 2>/dev/null | grep \"claude -p\" | grep -v grep; echo; echo \"=== python drain ===\"; ps -o pid,ppid,stat,lstart,command -ax 2>/dev/null | grep -iE \"drain|orchestrat\" | grep -v grep; echo; echo \"=== was 6785 alive? ===\"; ps -p 6785 >/dev/null 2>&1 && echo \"ALIVE\" || echo \"GONE\"; echo; echo \"=== tmux ===\"; tmux ls 2>/dev/null",
  "description": "Re-scan for live worker/orchestrator processes"
}
```

> TOOL

tool_result
id: toolu_016MwfWMkn9n6zDPQVwyx4ZX
```
=== claude -p processes ===

=== python drain ===

=== was 6785 alive? ===
GONE

=== tmux ===
0: 1 windows (created Sat Jun 13 12:44:13 2026)
7: 1 windows (created Thu Jun 18 16:34:06 2026) (attached)
```

> AGENT

PID 6785 is now **GONE** — and there's no live orchestrator or worker process at all. So nothing is actually running anymore; the finishing sub-agent exited sometime in the last few minutes. Let me read today's run-log to see how the orchestrator actually ended.

> TOOL

tool_use Bash
id: toolu_012yP94i2bVdmTkX4d5Es3Q8
```json
{
  "command": "cd ~/.drain-cycle/runs && ls -lat *.json | head -5; echo \"=== latest (today 2026-06-18) ===\"; LATEST=$(ls -t *.json | head -1); echo \"file: $LATEST\"; python3 -c \"\nimport json,sys\nd=json.load(open('$LATEST'))\nprint('keys:', list(d.keys()))\nprint('started:', d.get('started_at'), 'finished:', d.get('finished_at'))\nprint('outcome/verdict:', d.get('outcome_verdict') or d.get('verdict') or d.get('grade'))\nfor k in ('issues','results','entries'):\n    if k in d:\n        print('--', k, '--')\n        for it in (d[k] if isinstance(d[k],list) else [d[k]]):\n            if isinstance(it,dict):\n                print(' ', {kk:it.get(kk) for kk in ('identifier','id','final_linear_state','halt_reason','exit_code','is_done','finishing_runs','pr_urls') if kk in it})\n\"",
  "description": "Read latest run-log summary"
}
```

> TOOL

tool_result
id: toolu_012yP94i2bVdmTkX4d5Es3Q8
```
-rw-r--r--@ 1 anton  staff  1813 18 Jun 16:50 9e17380f-9527-40ef-8523-4e4358f12809-20260618T063410869643Z.json
-rw-r--r--@ 1 anton  staff  2111 18 Jun 13:26 9e17380f-9527-40ef-8523-4e4358f12809-20260618T030710785395Z.json
-rw-r--r--@ 1 anton  staff  6657 17 Jun 17:04 9e17380f-9527-40ef-8523-4e4358f12809-20260617T051541788266Z.json
-rw-r--r--@ 1 anton  staff  3089 16 Jun 22:39 9e17380f-9527-40ef-8523-4e4358f12809-20260616T115934707744Z.json
-rw-r--r--@ 1 anton  staff  3079 16 Jun 21:54 9e17380f-9527-40ef-8523-4e4358f12809-20260616T105539655472Z.json
=== latest (today 2026-06-18) ===
file: 9e17380f-9527-40ef-8523-4e4358f12809-20260618T063410869643Z.json
keys: ['cycle_id', 'cycle_duration_seconds', 'cycle_cost_usd', 'cycle_tokens_cumulative', 'cycle_halt_reason', 'entries']
started: None finished: None
outcome/verdict: None
-- entries --
  {'final_linear_state': 'Done', 'halt_reason': None, 'exit_code': 0, 'finishing_runs': [{'trigger': 'err-issue-not-done', 'started_at': '2026-06-18T06:43:10.245774+00:00', 'finished_at': '2026-06-18T06:50:35.392445+00:00', 'duration_seconds': 445.14038400002755, 'model': 'claude-sonnet-4-6', 'usage': {'input_tokens': 390, 'output_tokens': 1319, 'cache_creation_input_tokens': 64480, 'cache_read_input_tokens': 2644532, 'cumulative': 2710721, 'peak_context': 81343}, 'cost_usd': 1.4781996, 'num_turns': 57, 'session_id': '1ba3bb9a-30ae-4ddb-89a5-da1c748c70f7', 'is_error': False}]}
Shell cwd was reset to /Users/anton/src/drain-cycle
```

> AGENT

Now I have the full, corrected picture from the run-log. Let me verify the timeline with the current time.

> TOOL

tool_use Bash
id: toolu_015sC7THHxdYCAq9nyvYy6iK
```json
{
  "command": "date \"+now: %H:%M:%S %Z (%z)\"; echo \"run-log written:\"; ls -l --time-style=+%H:%M:%S ~/.drain-cycle/runs/9e17380f-9527-40ef-8523-4e4358f12809-20260618T063410869643Z.json 2>/dev/null || stat -f \"%Sm\" -t \"%H:%M:%S\" ~/.drain-cycle/runs/9e17380f-9527-40ef-8523-4e4358f12809-20260618T063410869643Z.json",
  "description": "Confirm current time vs run completion"
}
```

> TOOL

tool_result
id: toolu_015sC7THHxdYCAq9nyvYy6iK
```
now: 16:51:58 AEST (+1000)
run-log written:
16:50:35
```

> AGENT

Correction to my earlier "hung process" guess — the run-log tells the real story. It wasn't stuck; it was **invisibly working and has now finished** (16:50:35, ~90 seconds before now). Here's what actually happened on both points.

## Why the watcher never showed the sub-agent — a real blind spot

The main worker and the finishing sub-agent run on **two different execution paths in `worker.run_issue`**:

- **Main worker (watch mode):** the *external* path (worker.py:226). Its `claude` runs inside a **tmux pane under `tee`**, and drain-cycle reads the teed stream. That's the only thing the `-w` pane mirrors.
- **Finishing sub-agent:** the *spawned* path. The orchestrator calls `run_issue(..., passthrough=console.AgentSink())` (orchestrator.py:737) with **no `external_stream` and no `kill_fn`**, so it's a plain `subprocess.Popen` (worker.py:272). Its output flows through `AgentSink → agent_line` to the orchestrator's Rich console (main stdout) — **never into the tmux watch pane.**

So in watch mode the **entire recovery/finishing phase is invisible**. The pane froze on the worker's `=== done: 45 turns ===` frame and showed nothing for the next 7 minutes while real work happened off-screen. That blackout is what made it look stalled.

## It wasn't stuck — it was a legitimate 7-minute finishing pass

The run-log entry: […]

> DEVELOPER

i've fixed the linear state, lets just fix the defects

> AGENT

Let me read the orchestrator and handoff modules to make precise edits.

> TOOL

tool_use Read
id: toolu_01Xb1YimpYbDCqcCKZfs3gro
```json
{
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/orchestrator.py",
  "offset": 660,
  "limit": 220
}
```

> TOOL

tool_result
id: toolu_01Xb1YimpYbDCqcCKZfs3gro
```
660	                kill_fn=kill_fn,
661	                on_progress=_make_on_progress(marker, identifier),
662	                passthrough=console.AgentSink(),
663	            )
664	        finally:
665	            progress.clear()
666	            if session is not None:
667	                session.cleanup()
668	        finished_at = _now_iso()
669	        # Read any verdicts the worker recorded in the handoff. M2+-populated
670	        # locals take precedence; handoff fills the gap when they are None.
671	        _hov, _hpv = handoff.read_partial(worktree_path)
672	        outcome = _WorkerOutcome(
673	            result=result,
674	            outcome_verdict=outcome_verdict if outcome_verdict is not None else _hov,
675	            prep_verdict=prep_verdict if prep_verdict is not None else _hpv,
676	            responder_runs=responder_runs,
677	        )
678	
679	        if result.breach is not None:
680	            # The worker crossed a per-issue cap (tokens or time) and was
681	            # process-group killed (grandchildren reaped). Same revert + halt
682	            # contract as a not-Done exit, with the recorded usage of the
683	            # killed session and the breached cap named in the halt reason.
684	            original_state_name = issue["state"]["name"]
685	            effective_state, revert_error = _revert_to_pre_halt_state(
686	                issue["id"],
687	                target_state_name=original_state_name,
688	                pre_revert_state_name=_IN_PROGRESS_STATE_NAME,
689	            )
690	            halt_reason = (
691	                f"{_halt_message(identifier, effective_state, worktree_path)}"
692	                f" — {result.breach.describe()}"
693	            )
694	            if revert_error is not None:
695	                halt_reason += (
696	                    f"; revert to {original_state_name!r} failed: {revert_error}"
697	                )
698	            issue_span.set_attribute("issue.exit_code", result.exit_code)
699	            _set_verdict_span_attrs(issue_span, outcome)
700 […]

> TOOL

tool_use Read
id: toolu_01ARg1kMprrRvTuTXuK2qaN7
```json
{
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/handoff.py"
}
```

> TOOL

tool_result
id: toolu_01ARg1kMprrRvTuTXuK2qaN7
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

> AGENT

Let me read the rest of the post-finishing logic to understand the not-Done path.

> TOOL

tool_use Read
id: toolu_0111bpaMCzqeuhiwvLGyFLbM
```json
{
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/orchestrator.py",
  "offset": 880,
  "limit": 160
}
```

> TOOL

tool_result
id: toolu_0111bpaMCzqeuhiwvLGyFLbM
```
880	                        f"; revert to {original_state_name!r} failed: {revert_error}"
881	                    )
882	                _set_verdict_span_attrs(issue_span, outcome)
883	                halt_ctx.record(
884	                    slug="err-outcome-verifier-fail",
885	                    halt_reason=halt_reason,
886	                    final_linear_state=effective_state,
887	                    worktree_path=str(worktree_path),
888	                    finished_at=finished_at,
889	                    exit_code=result.exit_code,
890	                    outcome=outcome,
891	                    finishing_runs=finishing_runs,
892	                )
893	                # set_cycle_halt is called here (not via the _run() cycle-cap
894	                # path) because the spec requires cycle_halt_reason to name the
895	                # verifier findings so downstream tooling can distinguish this
896	                # halt type from a cap breach or a worker not-Done.
897	                halt_ctx.log.set_cycle_halt(halt_reason)
898	                return 1, pane_id
899	
900	            if submitted is not None:
901	                # Hand the baton to the next same-repo issue and record the
902	                # submitted PRs as the orchestrator's confirmation line.
903	                baton[target_repo.name] = identifier
904	                issue_span.set_attribute("issue.submitted_pr_count", len(submitted.pr_urls))
905	                pr_list = ", ".join(pr.url for pr in submitted.pr_urls)
906	                console.worker_event(identifier, f"submitted {pr_list}")
907	
908	            issue_span.set_attribute("issue.final_linear_state", post_spawn_state)
909	
910	            remove_error: str | None = None
911	            try:
912	                worktree.merge_entire_sessions(worktree_path, target_repo)
913	                worktree.remove(target_repo, worktree_path)
914	            except RuntimeError as exc:
915	                remove_error = str(exc)
916	                issue_span.set_attribute("worktree.remove_error", remove_error)
917	                console.orch(f"{identifier}: worktree teardown failed: {exc}")
918	            # Append unconditionally for every attempted issue.
919	            log.append_entry(
920	                issue_identifier=identifier,
921	                started_at=started_at,
922	                finished_at=finished_at,
923	                exit_code=result.exit_code,
924	                final_linear_state=post_spawn_state,
925	                worktree_path=str(worktree_path),
926	                halt_reason=remove_error,
927	                outcome_verdict=outcome.outcome_verdict,
928 […]

> AGENT

This is more than a missing guard — it's an architectural mismatch, and I want to get the direction right before editing core control flow. Let me map the current behavior precisely.

The orchestrator's success machinery (baton handoff, worktree teardown, log entry) all lives **inside** `if is_done:` (orchestrator.py:770–945). So the success signal is the Linear *Done* state. But the `exec:*` skill your main worker runs has already adopted the opposite governance — it submitted PR #56, recorded `pr_urls`, and deliberately **left the issue In Progress** ("Left at In Progress…"). That's the collision: the worker's contract is "In Progress until the PR merges," the orchestrator's contract is "Done = success." The finishing sub-agent exists to force the issue Done so the orchestrator's gate passes.

So a minimal guard alone won't work: if I just skip the redundant finishing pass, the correctly-finished (In Progress + `pr_urls`) issue falls straight through to the not-Done **halt** at line 947 — reverting it and stopping the whole drain. The real fix is to make the orchestrator key success on **submission (`pr_urls` present)**, not on the Linear Done state.

Before I restructure that gate, let me scope the blast radius in the tests.

> TOOL

tool_use Bash
id: toolu_01MKRQMXcNxJExaJTy7HEBJu
```json
{
  "command": "ls tests/ 2>/dev/null && echo \"---FINISHING/DONE refs---\" && grep -rln \"is_done\\|finishing\\|pr_urls\\|err-issue-not-done\\|err-stack-no-prs\\|build_finishing\" tests/ 2>/dev/null",
  "description": "List tests and find finishing/done references"
}
```

> TOOL

tool_result
id: toolu_01MKRQMXcNxJExaJTy7HEBJu
```
fixtures/
test_cli.py  11.0K
test_console.py  3.7K
test_grade_across_cycles.py  4.0K
test_grade_draft.py  8.4K
test_grade_per_cycle.py  4.0K
test_grade_verdict.py  5.9K
test_grade_walking_skeleton.py  3.5K
test_handoff.py  10.8K
test_kr2_check.py  3.0K
test_limits.py  6.4K
test_linear_api_url.py  1.5K
test_linear_pending_issues.py  8.8K
test_linear_set_state.py  2.5K
test_linear_sort.py  5.1K
test_model.py  1.5K
test_orchestrator_cycle_halt.py  3.3K
test_orchestrator_cycle_limit.py  6.0K
test_orchestrator_finishing.py  38.0K
test_orchestrator_halt.py  31.5K
test_orchestrator_handoff_verdicts.py  10.4K
test_orchestrator_iteration.py  19.8K
test_orchestrator_marker.py  9.8K
test_orchestrator_multi_repo.py  17.5K
test_orchestrator_resume.py  21.2K
test_orchestrator_runlog.py  10.4K
test_orchestrator_set_state.py  5.6K
test_orchestrator_teardown.py  4.8K
test_orchestrator_watch.py  15.1K
test_progress.py  3.8K
test_prompt.py  8.6K
test_repos.py  11.2K
test_runlog.py  8.6K
test_status.py  4.7K
test_stop_guard.py  8.6K
test_telemetry.py  2.1K
test_watch.py  3.5K
test_watch_format.py  8.9K
test_worker.py  18.4K
test_worktree.py  18.5K
---FINISHING/DONE refs---
tests/test_orchestrator_runlog.py
tests/test_orchestrator_finishing.py
tests/test_stop_guard.py
tests/test_orchestrator_halt.py
tests/test_runlog.py
tests/test_prompt.py
tests/test_handoff.py
tests/__pycache__/test_stop_guard.cpython-314-pytest-9.0.3.pyc
tests/__pycache__/test_handoff.cpython-312-pytest-9.0.3.pyc
tests/__pycache__/test_orchestrator_finishing.cpython-314-pytest-9.0.3.pyc
tests/__pycache__/test_runlog.cpython-314-pytest-9.0.3.pyc
tests/__pycache__/test_runlog.cpython-312.pyc
tests/__pycache__/test_orchestrator_multi_repo.cpython-314-pytest-9.0.3.pyc
tests/__pycache__/test_prompt.cpython-312.pyc
tests/__pycache__/test_orchestrator_runlog.cpython-312-pytest-9.0.3.pyc
tests/__pycache__/test_handoff.cpython-312.pyc
tests/__pycache__/test_orchestrator_halt.cpython-314-pytest-9.0.3.pyc
tests/__pycache__/test_prompt.cpython-312-pytest-9.0.3.pyc
tests/__pycache__/test_orchestrator_finishing.cpython-312.pyc
tests/__pycache__/test_orchestrator_runlog.cpython-312.pyc
tests/__pycache__/test_stop_guard.cpython-312.pyc
tests/__pycache__/test_orchestrator_handoff_verdicts.cpython-312.pyc
tests/__pycache__/test_orchestrator_multi_repo.cpython-312-pytest-9.0.3.pyc
tests/__pycache__/test_orchestrator_runlog.cpython-314-pytest-9.0.3.pyc
tests/__pycache__/test_orchestrator_finishing.cpython-312-pytest-9.0.3.pyc
tests/__pycache__/test_handoff.cpython-314-pytest-9.0.3.pyc
tests/__pycache__/test_stop_guard.cpython-312-pytest-9.0.3.pyc
tests/__pycache__/test_runlog.cpython-312-pytest-9.0.3.pyc
tests/__pycache__/test_orchestrator_multi_repo.cpython-312.pyc
tests/__pycache__/test_orchestrator_handoff_verdicts.cpython-312-pytest-9.0.3.pyc
tests/__pycache__/test_orchestrator_halt.cpython-312-pytest-9.0.3.pyc
tests/__pycache__/test_prompt.cpython-314-pytest-9.0.3.pyc
tests/__pycache__/test_orchestrator_halt.cpython-312.pyc
tests/test_orchestrator_handoff_verdicts.py
tests/fixtures/exec-state.json
tests/test_orchestrator_multi_repo.py
```

> AGENT

`test_orchestrator_finishing.py` is 38K — the core behavior I'm about to change is heavily covered. Let me read it and the finishing-success scenarios to understand exactly what's asserted.

> TOOL

tool_use Read
id: toolu_014nMGg9uQYbjnWeAZzRgtKA
```json
{
  "file_path": "/Users/anton/src/drain-cycle/tests/test_orchestrator_finishing.py"
}
```

> TOOL

tool_result
id: toolu_014nMGg9uQYbjnWeAZzRgtKA
```
1	"""Tests for orchestrator-enforced completion via finishing sub-agent.
2	
3	The orchestrator spawns a sonnet finishing sub-agent when a worker exits
4	without completing the protocol but has committed work beyond the base branch.
5	Two recovery sites are covered:
6	  * not-Done halt: worker exits without marking the issue Done
7	  * stack-no-PRs halt: worker marks Done but leaves no pr_urls in the handoff
8	
9	Both use the same sub-agent (``_FINISHING_MODEL``), a one-attempt-per-issue-per-run
10	guard, and write a ``finishing_runs`` entry in the run log.
11	
12	Substitution pattern mirrors ``test_orchestrator_halt.py``: real git repo,
13	in-process Linear stubs, fake ``claude`` shell script as ``_CLAUDE_CMD``.
14	
15	Scripts use an invocation counter file (``<tmp_path>/invocation_count.txt``)
16	to distinguish the main worker (first invocation) from the finishing sub-agent
17	(second invocation). First invocation makes a commit in the worktree so
18	``_commits_beyond_base`` returns True; second invocation runs the finishing
19	protocol (marks Done, writes handoff when in stack mode).
20	"""
21	from __future__ import annotations
22	
23	import json
24	import subprocess
25	from pathlib import Path
26	
27	import pytest
28	
29	from drain_cycle import linear, orchestrator, repos
30	
31	
32	_TEST_REPO_NAME = "test-repo"
33	
34 […]

> AGENT

The test suite makes the design intent explicit: drain-cycle's current contract is **"Done = complete,"** and the finishing sub-agent exists to *force* Done. But the `exec:*` skill the worker runs has moved to **"leave In Progress until the PR merges"** — which is the governance you endorsed by reverting ABA-394. So the real defect is that the orchestrator keys success on the Linear *Done* state instead of on the *submission signal* (`pr_urls`).

The clean fix is **additive**: accept a stack-mode worker that wrote `pr_urls` and stayed In Progress as *complete* (no finishing pass, no halt), while leaving the genuine "committed-but-unsubmitted" recovery untouched. Let me confirm no existing test already exercises the "stack + pr_urls + not-Done" combination, and check the prompt/stop-guard text assertions.

> TOOL

tool_use Bash
id: toolu_01Lbw1cvh6jZtaRKf1gtSY3N
```json
{
  "command": "echo \"=== halt: stack+notdone+pr_urls combos ===\" && grep -n \"pr_urls\\|In Progress\\|is_done\\|final_linear_state\" tests/test_orchestrator_halt.py | head -40 && echo \"=== handoff_verdicts ===\" && grep -n \"pr_urls\\|In Progress\\|final_linear_state\\|no_stack\" tests/test_orchestrator_handoff_verdicts.py | head -40",
  "description": "Scan halt/verdict tests for stack+pr_urls+not-done cases"
}
```

> TOOL

tool_use Read
id: toolu_01PjpH7Vo1vnKouURfA9WABM
```json
{
  "file_path": "/Users/anton/src/drain-cycle/tests/test_prompt.py"
}
```

> TOOL

tool_result
id: toolu_01Lbw1cvh6jZtaRKf1gtSY3N
```
=== halt: stack+notdone+pr_urls combos ===
25 matches in 1 files:

tests/test_orchestrator_halt.py:11:`final_linear_state` reflecting the non-Done state the agent left it in
tests/test_orchestrator_halt.py:211:issue — with `final_linear_state` matching the non-Done state name
tests/test_orchestrator_halt.py:274:"final_linear_state",
tests/test_orchestrator_halt.py:293:assert entry["final_linear_state"] == first["state"]["name"]
tests/test_orchestrator_halt.py:294:assert entry["final_linear_state"] != "Done"
tests/test_orchestrator_halt.py:378:assert entry["final_linear_state"] == first["state"]["name"]
tests/test_orchestrator_halt.py:447:assert entry["final_linear_state"] == first["state"]["name"]
tests/test_orchestrator_halt.py:489:"type": "started" if state_name == "In Progress" else "unstarted",
tests/test_orchestrator_halt.py:513:# Two set_state calls in pick order: In Progress (pre-spawn), then
tests/test_orchestrator_halt.py:516:(first["id"], "In Progress"),
tests/test_orchestrator_halt.py:522:# The halt entry's final_linear_state reflects the post-revert state
tests/test_orchestrator_halt.py:523:# observed via refresh, not the in-flight "In Progress".
tests/test_orchestrator_halt.py:527:assert entry["final_linear_state"] == first["state"]["name"]
tests/test_orchestrator_halt.py:540:"In Progress" — the orchestrator must revert to the original
tests/test_orchestrator_halt.py:560:"type": "started" if state_name == "In Progress" else "unstarted",
tests/test_orchestrator_halt.py:583:(first["id"], "In Progress"),
tests/test_orchestrator_halt.py:591:assert entry["final_linear_state"] == first["state"]["name"]
tests/test_orchestrator_halt.py:620:# First call (Todo → In Progress) succeeds; second call (revert)
tests/test_orchestrator_halt.py:626:# Agent left the issue in In Progress. Revert will be attempted
tests/test_orchestrator_halt.py:630:"state": {"type": "started", "name": "In Progress"},
tests/test_orchestrator_halt.py:646:# Revert was attempted: In Progress (pre-spawn) and then the failing
tests/test_orchestrator_halt.py:649:(first["id"], "In Progress"),
tests/test_orchestrator_halt.py:710:# Exactly one set_state call — the failed pre-spawn In Progress
tests/test_orchestrator_halt.py:712:assert set_state_calls == [(first["id"], "In Progress")]
tests/test_orchestrator_halt.py:741:"type": "started" if state_name == "In Progress" else "unstarted",
=== handoff_verdicts ===
8 matches in 1 files:

tests/test_orchestrator_handoff_verdicts.py:39:# Sectioned […]

> TOOL

tool_result
id: toolu_01PjpH7Vo1vnKouURfA9WABM
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
14	from drain_cycle.prompt import _TAIL, build, build_finishing
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
40 […]

> AGENT

The test landscape confirms the additive fix is safe: every existing not-Done/halt test runs with no `pr_urls` (or `no_stack=True`), so none exercises the "stack + `pr_urls` + In Progress" combination I'm about to treat as success. And `test_prompt.py:208` pins `"Done"` in `build_finishing`'s tail — so I'll make that prompt mode-aware (Done for push, In Progress for stack).

Let me make the orchestrator edits first.

> TOOL

tool_use Edit
id: toolu_017y7cB4jMwS7DqqAp9Y7xFp
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/orchestrator.py",
  "old_string": "        finishing_runs: list[dict] = []\n        finishing_attempted = False\n\n        # Recovery: committed-but-unfinished → spawn a sonnet finishing sub-agent\n        # before halting. Fires only when the branch has commits beyond base (an\n        # empty or uncommitted-only branch is a genuine failure), the verifier did\n        # not explicitly reject the work (a FAIL verdict must stay halted to\n        # satisfy KR2), and a cap breach did not already stop the session (that\n        # path returned above). At most one finishing attempt per issue per run.\n        if not is_done and _commits_beyond_base(worktree_path, base):",
  "new_string": "        finishing_runs: list[dict] = []\n        finishing_attempted = False\n\n        # The submission signal is ``pr_urls`` in exec-state.json, not the Linear\n        # Done state. A stack worker that submitted its PR(s) and deliberately\n        # left the issue In Progress (governance: stay In Progress until the PR\n        # merges) is complete — read that signal up front so both the recovery\n        # condition and the success gate below key on submission rather than on\n        # Done. Push mode has no handoff, so this is always ``None`` there.\n        submitted = handoff.read(worktree_path) if stack else None\n\n        # Recovery: committed-but-unsubmitted → spawn a sonnet finishing sub-agent\n […]

> TOOL

tool_result
id: toolu_017y7cB4jMwS7DqqAp9Y7xFp
```
The file /Users/anton/src/drain-cycle/drain_cycle/orchestrator.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_019PZy33C6uMV7VNe4ypWoDp
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/orchestrator.py",
  "old_string": "                _finishing_result = worker.run_issue(\n                    claude_cmd=_CLAUDE_CMD,\n                    model=_FINISHING_MODEL,\n                    prompt=prompt.build_finishing(identifier, worktree_path, base),\n                    cwd=worktree_path,\n                    token_limit=limits.per_issue_tokens,\n                    time_limit_seconds=limits.per_issue_seconds,\n                    cost_limit_usd=limits.per_issue_cost_usd,\n                    passthrough=console.AgentSink(),\n                )\n                _finishing_finished = _now_iso()\n                finishing_runs.append({\n                    \"trigger\": \"err-issue-not-done\",",
  "new_string": "                _finishing_result = worker.run_issue(\n                    claude_cmd=_CLAUDE_CMD,\n                    model=_FINISHING_MODEL,\n                    prompt=prompt.build_finishing(\n                        identifier, worktree_path, base, stack=stack\n                    ),\n                    cwd=worktree_path,\n                    token_limit=limits.per_issue_tokens,\n                    time_limit_seconds=limits.per_issue_seconds,\n                    cost_limit_usd=limits.per_issue_cost_usd,\n                    passthrough=console.AgentSink(),\n                )\n                _finishing_finished = _now_iso()\n                finishing_runs.append({\n                    \"trigger\": \"err-issue-not-done\","
}
```

> TOOL

tool_result
id: toolu_019PZy33C6uMV7VNe4ypWoDp
```
The file /Users/anton/src/drain-cycle/drain_cycle/orchestrator.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01QcDvJ2kJuhZr1sUvETQA8K
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/orchestrator.py",
  "old_string": "                # Re-read to see whether finishing succeeded\n                refreshed = linear.get_issue(issue[\"id\"])\n                post_spawn_state = refreshed[\"state\"][\"name\"]\n                is_done = refreshed[\"state\"][\"type\"] == _DONE_STATE_TYPE\n                issue_span.set_attribute(\"issue.is_done\", is_done)",
  "new_string": "                # Re-read to see whether finishing succeeded. In stack mode the\n                # finishing agent records ``pr_urls`` and (per governance) leaves\n                # the issue In Progress, so re-read the submission signal too —\n                # the success gate below accepts it whether or not Done was set.\n                refreshed = linear.get_issue(issue[\"id\"])\n                post_spawn_state = refreshed[\"state\"][\"name\"]\n                is_done = refreshed[\"state\"][\"type\"] == _DONE_STATE_TYPE\n                issue_span.set_attribute(\"issue.is_done\", is_done)\n                submitted = handoff.read(worktree_path) if stack else None"
}
```

> TOOL

tool_result
id: toolu_01QcDvJ2kJuhZr1sUvETQA8K
```
The file /Users/anton/src/drain-cycle/drain_cycle/orchestrator.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now the success gate and the redundant inner re-read:

> TOOL

tool_use Edit
id: toolu_016sUMdV76nDUjQ1gM8Mb6PE
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/orchestrator.py",
  "old_string": "        if is_done:\n            # Stack-mode confirmation gate, read before teardown removes the\n            # worktree. A Done issue in stack mode must have left a non-empty\n            # ``pr_urls`` — that is the orchestrator's proof submission ran.\n            # If it's missing, the worker marked Done without opening a PR:\n            # revert + halt, preserve the worktree for inspection, and do NOT\n            # extend the baton — the next same-repo issue must not stack onto a\n            # branch that was never pushed. Push-mode issues have no stack to\n            # extend and no handoff, so they bypass the gate entirely.\n            submitted = handoff.read(worktree_path) if stack else None\n            if stack and submitted is None:",
  "new_string": "        if is_done or submitted is not None:\n            # Success gate. The cycle completes when the worker either marked the\n            # issue Done (push mode: the push to main is the completion proof) or\n            # left a non-empty ``pr_urls`` (stack mode: the submitted PR is the\n            # proof, and the issue stays In Progress until that PR merges).\n            #\n            # Stack-mode confirmation, read before teardown removes the worktree:\n            # a stack issue that reached here on Done alone but […]

> TOOL

tool_result
id: toolu_016sUMdV76nDUjQ1gM8Mb6PE
```
The file /Users/anton/src/drain-cycle/drain_cycle/orchestrator.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now update the stack-no-PRs recovery's `build_finishing` call to pass `stack`:

> TOOL

tool_use Edit
id: toolu_01DfNmVAGPYwj7v3iQpkWsN1
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/orchestrator.py",
  "old_string": "                    _finishing_result = worker.run_issue(\n                        claude_cmd=_CLAUDE_CMD,\n                        model=_FINISHING_MODEL,\n                        prompt=prompt.build_finishing(identifier, worktree_path, base),\n                        cwd=worktree_path,\n                        token_limit=limits.per_issue_tokens,\n                        time_limit_seconds=limits.per_issue_seconds,\n                        cost_limit_usd=limits.per_issue_cost_usd,\n                        passthrough=console.AgentSink(),\n                    )\n                    _finishing_finished = _now_iso()\n                    finishing_runs.append({\n                        \"trigger\": \"err-stack-no-prs\",",
  "new_string": "                    _finishing_result = worker.run_issue(\n                        claude_cmd=_CLAUDE_CMD,\n                        model=_FINISHING_MODEL,\n                        prompt=prompt.build_finishing(\n                            identifier, worktree_path, base, stack=stack\n                        ),\n                        cwd=worktree_path,\n                        token_limit=limits.per_issue_tokens,\n                        time_limit_seconds=limits.per_issue_seconds,\n                        cost_limit_usd=limits.per_issue_cost_usd,\n                        passthrough=console.AgentSink(),\n                    )\n                    _finishing_finished = _now_iso()\n                    finishing_runs.append({\n                        \"trigger\": \"err-stack-no-prs\","
}
```

> TOOL

tool_result
id: toolu_01DfNmVAGPYwj7v3iQpkWsN1
```
The file /Users/anton/src/drain-cycle/drain_cycle/orchestrator.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now make `build_finishing` mode-aware — leave In Progress in stack mode (PR not merged yet), mark Done in push mode:

> TOOL

tool_use Edit
id: toolu_01MF4HNUg4XQyxiRVgYeQNMU
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/prompt.py",
  "old_string": "def build_finishing(identifier: str, worktree: Path, base: str) -> str:\n    \"\"\"Build a finishing-only prompt for a committed-but-unfinished issue.\n\n    The implementation is already committed. The agent runs review → fix →\n    pr-finishing → Done. It must not re-implement or add commits beyond those\n    needed to fix Critical/Required review findings.\n    Critical/Required fixes are delegated to ``_FINISHING_OPUS_MODEL`` sub-agents.\n    \"\"\"\n    if base == \"main\":\n        base_clause = \"\"\n    else:\n        base_clause = (\n            f\" These commits are stacked on `{base}`, not `main`, so pass \"\n            f\"`{base}` to the skill as its base branch (it slices `{base}..HEAD`).\"\n        )\n    return (\n        f\"# Finishing incomplete issue {identifier}\\n\\n\"\n        f\"The implementation for this issue is already committed on this branch. \"\n        f\"Run `git log --oneline {base}..HEAD` to see the committed work.\\n\\n\"\n        \"Your only task is to run the finishing protocol below. Do not \"\n        \"re-implement, redesign, or add commits beyond those needed to fix \"\n        \"Critical/Required review findings.\\n\\n\"\n        \"---\\n\\n\"\n        f\"Finishing instructions for issue {identifier}:\\n\"\n        f\"- Working directory: {worktree}\\n\"\n        f\"- Base branch: {base}\\n\"\n        \"- Steps (run in order, before marking Done):\\n\"\n        \"  1. Review the committed changes for correctness and quality.\\n\"\n        \"  2. Fix any Critical or Required findings. For each fix […]

> TOOL

tool_result
id: toolu_01MF4HNUg4XQyxiRVgYeQNMU
```
The file /Users/anton/src/drain-cycle/drain_cycle/prompt.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now the stop-guard stack block prompt — it also tells the agent to "transition the issue to Done":

> TOOL

tool_use Edit
id: toolu_015xuWW8ruu5CrYr5cPCfKdz
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/stop_guard.py",
  "old_string": "_BLOCK_PROMPT_STACK = (\n    \"drain-cycle stop-guard: the issue is not finished — the worktree has \"\n    \"uncommitted changes or no submitted PRs in exec-state.json yet. \"\n    \"Complete the remaining steps now: commit any pending changes to the \"\n    \"issue branch as reviewable slices (do not push by hand), run \"\n    \"`/shape:pr-finishing` to submit the stacked PR(s) — it writes the \"\n    \"pr_urls into exec-state.json and posts the review-summary comment \"\n    \"— then transition the issue to Done. If you are genuinely blocked, \"\n    \"leave the issue In Progress and post a comment naming the blocker — \"\n    \"do not stop silently.\"\n)",
  "new_string": "_BLOCK_PROMPT_STACK = (\n    \"drain-cycle stop-guard: the issue is not finished — the worktree has \"\n    \"uncommitted changes or no submitted PRs in exec-state.json yet. \"\n    \"Complete the remaining steps now: commit any pending changes to the \"\n    \"issue branch as reviewable slices (do not push by hand), run \"\n    \"`/shape:pr-finishing` to submit the stacked PR(s) — it writes the \"\n    \"pr_urls into exec-state.json and posts the review-summary comment. \"\n    \"Leave the issue In Progress: the submitted PR is the completion signal \"\n    \"and the issue stays In Progress […]

> TOOL

tool_result
id: toolu_015xuWW8ruu5CrYr5cPCfKdz
```
The file /Users/anton/src/drain-cycle/drain_cycle/stop_guard.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now update the prompt tests for the mode-aware tail:

> TOOL

tool_use Edit
id: toolu_01XaQV3AesYnQZU53Lp3M3Yz
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/tests/test_prompt.py",
  "old_string": "def test_build_finishing_contains_identifier_base_and_worktree(tmp_path: Path) -> None:\n    \"\"\"build_finishing names the identifier, worktree, and base in the output.\"\"\"\n    worktree = tmp_path / \".worktrees\" / \"ABA-383\"\n    rendered = build_finishing(\"ABA-383\", worktree, \"main\")\n\n    assert \"ABA-383\" in rendered\n    assert str(worktree) in rendered\n    assert \"main..HEAD\" in rendered\n    assert \"/shape:pr-finishing\" in rendered\n    assert \"exec-state.json\" in rendered\n    assert \".drain-handoff.json\" not in rendered\n    # Tail line last\n    non_empty = [line for line in rendered.splitlines() if line.strip()]\n    assert \"Done\" in non_empty[-1]",
  "new_string": "def test_build_finishing_contains_identifier_base_and_worktree(tmp_path: Path) -> None:\n    \"\"\"build_finishing names the identifier, worktree, and base in the output.\"\"\"\n    worktree = tmp_path / \".worktrees\" / \"ABA-383\"\n    rendered = build_finishing(\"ABA-383\", worktree, \"main\")\n\n    assert \"ABA-383\" in rendered\n    assert str(worktree) in rendered\n    assert \"main..HEAD\" in rendered\n    assert \"/shape:pr-finishing\" in rendered\n    assert \"exec-state.json\" in rendered\n    assert \".drain-handoff.json\" not in rendered\n\n\ndef test_build_finishing_stack_leaves_in_progress(tmp_path: Path) -> None:\n    \"\"\"Stack mode (the default): the submitted PR is the completion signal, so\n    the agent leaves the issue In Progress and must not transition to Done.\"\"\"\n    worktree = tmp_path / \".worktrees\" / \"ABA-383\"\n    rendered = build_finishing(\"ABA-383\", worktree, \"main\", stack=True)\n\n    non_empty = [line for line in rendered.splitlines() if line.strip()]\n    assert \"In Progress\" in non_empty[-1]\n    assert \"do not transition it to Done\" in rendered\n    # No […]

> TOOL

tool_result
id: toolu_01XaQV3AesYnQZU53Lp3M3Yz
```
The file /Users/anton/src/drain-cycle/tests/test_prompt.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now check test_stop_guard.py for assertions on the changed prompt text:

> TOOL

tool_use Bash
id: toolu_01Uy9hKz8QYLSDezbf5ZycFL
```json
{
  "command": "grep -n \"Done\\|transition\\|In Progress\\|_BLOCK_PROMPT\\|block_reason\\|review-summary\\|pr_urls\" tests/test_stop_guard.py",
  "description": "Find stop-guard test assertions on prompt text"
}
```

> TOOL

tool_result
id: toolu_01Uy9hKz8QYLSDezbf5ZycFL
```
19 matches in 1 files:

tests/test_stop_guard.py:38:# pr_urls live under the finish section (ADR 0030) — the sectioned shape the
tests/test_stop_guard.py:41:json.dumps({"finish": {"pr_urls": [{"title": "feat: x", "url": "https://githu...
tests/test_stop_guard.py:48:assert decision.block_reason is None
tests/test_stop_guard.py:66:assert decision.block_reason is None
tests/test_stop_guard.py:77:assert decision.block_reason is not None
tests/test_stop_guard.py:78:assert "commit" in decision.block_reason.lower()
tests/test_stop_guard.py:79:assert "exec-state.json" in decision.block_reason
tests/test_stop_guard.py:97:assert decision.block_reason is not None
tests/test_stop_guard.py:98:assert "exec-state.json" in decision.block_reason
tests/test_stop_guard.py:112:assert decision.block_reason is None
tests/test_stop_guard.py:126:assert d1.block_reason is not None
tests/test_stop_guard.py:127:assert d2.block_reason is not None
tests/test_stop_guard.py:128:assert d3.block_reason is None
tests/test_stop_guard.py:141:assert d1.block_reason is not None
tests/test_stop_guard.py:144:assert d2.block_reason is None
tests/test_stop_guard.py:208:assert decision.block_reason is None
tests/test_stop_guard.py:220:# sectioned shape the pack writes: pr_urls live under the finish section.
tests/test_stop_guard.py:222:_json.dumps({"finish": {"pr_urls": [{"title": "feat", "url": "https://github....
tests/test_stop_guard.py:225:assert decision.block_reason is None
```

> AGENT

`test_stop_guard.py` only asserts on `"commit"` and `"exec-state.json"` — both still present. Now add the key orchestrator test: a stack worker that submits `pr_urls` and leaves the issue In Progress is accepted as complete, with no finishing pass.

> TOOL

tool_use Edit
id: toolu_01SsVLnW7Qwa6aktfxRqWYeA
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/tests/test_orchestrator_finishing.py",
  "old_string": "# ---------------------------------------------------------------------------\n# not-Done recovery: finishing sub-agent fails to mark Done\n# ---------------------------------------------------------------------------",
  "new_string": "# ---------------------------------------------------------------------------\n# not-Done but submitted: pr_urls present + In Progress → complete, no finishing\n# ---------------------------------------------------------------------------\n\n\ndef test_stack_worker_in_progress_with_pr_urls_is_complete(\n    tmp_path: Path, monkeypatch: pytest.MonkeyPatch\n) -> None:\n    \"\"\"Stack worker that submits its PR(s) and leaves the issue In Progress is\n    complete: no finishing sub-agent spawns, the run continues, and the\n    submission — not a Done transition — is the completion signal.\"\"\"\n    repo = tmp_path / \"repo\"\n    repo.mkdir()\n    _init_repo(repo)\n    monkeypatch.chdir(repo)\n    monkeypatch.setenv(\"HOME\", str(tmp_path))\n\n    issue = _issue(\"ABA-INPROG\")\n    issues_by_id = {issue[\"id\"]: issue}\n    counter_file = tmp_path / \"invocation_count.txt\"\n\n    def fake_get_issue(issue_id: str) -> dict:\n        # The worker leaves the issue In Progress (started) — never Done.\n        base = issues_by_id[issue_id]\n        return {**base, \"state\": {\"type\": \"started\", \"name\": \"In Progress\"}}\n\n    monkeypatch.setattr(linear, \"current_cycle_id\", lambda: \"stub-cycle\")\n    monkeypatch.setattr(linear, \"pending_issues\", lambda c: linear._plan([issue]))\n    monkeypatch.setattr(linear, \"get_issue\", fake_get_issue)\n    monkeypatch.setattr(linear, \"set_state\", lambda iid, s: None)\n\n    # Single invocation: commit, write finish.pr_urls, leave In Progress (no Done).\n    script = tmp_path / \"fake-claude.sh\"\n    script.write_text(\n        \"#!/bin/sh\\n\"\n        f'count=$(cat \"{counter_file}\" 2>/dev/null || echo 0)\\n'\n        'count=$((count + 1))\\n'\n        f'printf \"%s\" \"$count\" > \"{counter_file}\"\\n'\n        'git config user.email \"test@test.com\" 2>/dev/null\\n'\n        'git config user.name \"Test\" 2>/dev/null\\n'\n        'touch work.txt\\n'\n        \"git add work.txt 2>/dev/null\\n\"\n        'git commit -m \"work\" 2>/dev/null\\n'\n […]

> TOOL

tool_result
id: toolu_01SsVLnW7Qwa6aktfxRqWYeA
```
The file /Users/anton/src/drain-cycle/tests/test_orchestrator_finishing.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now let me run the affected test suites to validate the orchestrator, prompt, and stop-guard changes:

> TOOL

tool_use Bash
id: toolu_01QXyxRyxfyFAzoYrTyYDB5H
```json
{
  "command": "python -m pytest tests/test_orchestrator_finishing.py tests/test_prompt.py tests/test_stop_guard.py tests/test_orchestrator_handoff_verdicts.py tests/test_orchestrator_halt.py -q 2>&1 | tail -30",
  "description": "Run finishing, prompt, stop-guard, halt, verdict tests"
}
```

> TOOL

tool_result
id: toolu_01QXyxRyxfyFAzoYrTyYDB5H
```
Pytest: No tests collected
[full output: ~/Library/Application Support/rtk/tee/1781766160_pytest.log]
```

> TOOL

tool_use Bash
id: toolu_017ReekUynZkQ6X8HZsiG1dQ
```json
{
  "command": "cat ~/Library/Application\\ Support/rtk/tee/1781766160_pytest.log 2>/dev/null | tail -30 || true; echo \"=== retry via proxy ===\"; rtk proxy python -m pytest tests/test_orchestrator_finishing.py tests/test_prompt.py tests/test_stop_guard.py -q 2>&1 | tail -30",
  "description": "Inspect pytest log and retry"
}
```

> TOOL

tool_result
id: toolu_017ReekUynZkQ6X8HZsiG1dQ
```
    from . import telemetry
drain_cycle/telemetry.py:32: in <module>
    from opentelemetry import trace
E   ModuleNotFoundError: No module named 'opentelemetry'
_________ ERROR collecting tests/test_orchestrator_handoff_verdicts.py _________
ImportError while importing test module '/Users/anton/src/drain-cycle/tests/test_orchestrator_handoff_verdicts.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../.local/share/mise/installs/python/3.12.13/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_orchestrator_handoff_verdicts.py:25: in <module>
    from drain_cycle import linear, orchestrator, repos
drain_cycle/linear.py:14: in <module>
    import httpx
E   ModuleNotFoundError: No module named 'httpx'
_______________ ERROR collecting tests/test_orchestrator_halt.py _______________
ImportError while importing test module '/Users/anton/src/drain-cycle/tests/test_orchestrator_halt.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../.local/share/mise/installs/python/3.12.13/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_orchestrator_halt.py:30: in <module>
    from drain_cycle import limits, linear, orchestrator, repos
drain_cycle/limits.py:42: in <module>
    import yaml
E   ModuleNotFoundError: No module named 'yaml'
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
4 errors in 0.16s
=== retry via proxy ===
Traceback:
../../.local/share/mise/installs/python/3.12.13/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_orchestrator_finishing.py:29: in <module>
    from drain_cycle import linear, orchestrator, repos
drain_cycle/linear.py:14: in <module>
    import httpx
E   ModuleNotFoundError: No module named 'httpx'
__________________ ERROR collecting tests/test_stop_guard.py ___________________
ImportError while importing test module '/Users/anton/src/drain-cycle/tests/test_stop_guard.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../.local/share/mise/installs/python/3.12.13/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_stop_guard.py:21: in <module> […]

> AGENT

Wrong interpreter — this is a uv-tool project. Let me use its environment.

> TOOL

tool_use Bash
id: toolu_01LmACN4sQof4iQrmxGUYkbk
```json
{
  "command": "ls .venv/bin/python 2>/dev/null && echo \"has venv\"; head -5 pyproject.toml 2>/dev/null; echo \"---try uv run---\"; uv run --quiet pytest tests/test_orchestrator_finishing.py tests/test_prompt.py tests/test_stop_guard.py -q 2>&1 | tail -25",
  "description": "Run tests via uv environment"
}
```

> TOOL

tool_result
id: toolu_01LmACN4sQof4iQrmxGUYkbk
```
.venv/bin/python -> python3.14  10B
has venv
[project]
name = "drain-cycle"
[27 more lines]---try uv run---
..............................................                           [100%]
46 passed in 8.68s
```

> AGENT

All 46 pass. Now run the full suite to confirm nothing else regressed:

> TOOL

tool_use Bash
id: toolu_01KfNYCfay3fm7R3fuHLYYD3
```json
{
  "command": "uv run --quiet pytest -q 2>&1 | tail -20",
  "description": "Run full test suite"
}
```

> TOOL

tool_result
id: toolu_01KfNYCfay3fm7R3fuHLYYD3
```
........................................................................ [ 19%]
........................................................................ [ 38%]
........................................................................ [ 57%]
........................................................................ [ 77%]
........................................................................ [ 96%]
.............                                                            [100%]
373 passed in 45.32s
```

> AGENT

Full suite green (373 passed). Defect #1 done. Now defect #3 — the stale `.drain-guard-tripped`:

> TOOL

tool_use Bash
id: toolu_01DRJptmeJpC2ngfgnaKJwCZ
```json
{
  "command": "cat .drain-guard-tripped 2>/dev/null; echo \"--- gitignored? ---\"; git check-ignore .drain-guard-tripped; echo \"--- tracked? ---\"; git ls-files .drain-guard-tripped | head; rm -f .drain-guard-tripped && echo \"removed\"; ls .drain-guard-tripped 2>&1 | head -1",
  "description": "Inspect and remove stale guard-tripped file"
}
```

> TOOL

tool_result
id: toolu_01DRJptmeJpC2ngfgnaKJwCZ
```
uncommitted changes in worktree, no valid .drain-handoff.json after 1 re-injection(s)--- gitignored? ---
.drain-guard-tripped
--- tracked? ---
removed
ls: .drain-guard-tripped: No such file or directory
```

> AGENT

Defect #3 done (stale file referenced legacy `.drain-handoff.json`, gitignored, removed). Now defect #2 — the watch-pane blackout. Let me understand the console/watch architecture to scope the fix.

> TOOL

tool_use Read
id: toolu_01DznZSPpyj8owtvUkAPK97X
```json
{
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/console.py"
}
```

> TOOL

tool_result
id: toolu_01DznZSPpyj8owtvUkAPK97X
```
1	"""Structured Rich event log for the drain-cycle orchestrator.
2	
3	Replaces the scattered ``print(..., file=sys.stderr)`` calls with a small set of
4	labeled, timestamped event functions plus startup and completion tables. Every
5	function writes to ``sys.stderr`` so stdout stays free for piping.
6	
7	The three event labels are:
8	
9	* ``orch``     — orchestrator-side activity (worktree setup, spawn, PR posts,
10	  non-fatal errors).
11	* ``ABA-NNN``  — per-issue outcomes (picked, done, progress).
12	* ``HALT``     — halt conditions; rendered red.
13	
14	Agent output (the worker's ``passthrough`` stream) is indented with ``│`` via
15	:class:`AgentSink` so it is visually distinct from orchestrator lines.
16	
17	The Rich ``Console`` is built lazily on each call against the live
18	``sys.stderr`` reference. That keeps pytest's ``capsys`` capture working — it
19	swaps ``sys.stderr`` after this module is imported, and a cached Console
20	would otherwise still hold the original.
21	"""
22	from __future__ import annotations
23	
24	import sys
25	from datetime import datetime
26	from typing import Iterable, Sequence
27	
28	from rich.console import Console
29	from rich.table import Table
30	
31	
32	def _console() -> Console:
33	    return Console(file=sys.stderr, highlight=False, soft_wrap=True)
34 […]

> AGENT

Output all goes to stderr via Rich. Now let me understand how watch mode sets up the pane vs. the spawned path, to see how feasible routing the finishing agent into the pane is.

> TOOL

tool_use Bash
id: toolu_01L7onYCYhznUHemxRBwwd4k
```json
{
  "command": "echo \"=== orchestrator: watch/pane/external_stream/kill_fn setup ===\"; grep -n \"external_stream\\|kill_fn\\|pane\\|watch\\|run_issue\\|_make_on_progress\\|session\" drain_cycle/orchestrator.py | head -50",
  "description": "Find watch/pane wiring in orchestrator"
}
```

> TOOL

tool_result
id: toolu_01L7onYCYhznUHemxRBwwd4k
```
=== orchestrator: watch/pane/external_stream/kill_fn setup ===
52 matches in 1 files:

drain_cycle/orchestrator.py:22:from . import watch as watch_pane
drain_cycle/orchestrator.py:32:turns it on; the worker then writes each session's startup diagnostics
drain_cycle/orchestrator.py:192:"session_id": result.session_id,
drain_cycle/orchestrator.py:292:watch: bool = False,
drain_cycle/orchestrator.py:304:return _run(repos, limits, cycle_span, watch=watch, no_stack=no_stack)
drain_cycle/orchestrator.py:312:watch: bool = False,
drain_cycle/orchestrator.py:356:current_pane_id: str | None = None
drain_cycle/orchestrator.py:366:# Kill the pane from the previous issue before opening one for this issue.
drain_cycle/orchestrator.py:367:if current_pane_id is not None:
drain_cycle/orchestrator.py:368:watch_pane.close_pane(current_pane_id)
drain_cycle/orchestrator.py:369:current_pane_id = None
drain_cycle/orchestrator.py:371:halt_code, current_pane_id = _drain_one_issue(
drain_cycle/orchestrator.py:380:watch=watch,
drain_cycle/orchestrator.py:407:# Final pane is left open for scrollback (intentionally not killed here).
drain_cycle/orchestrator.py:423:watch: bool = False,
drain_cycle/orchestrator.py:430:Returns ``(halt_code, pane_id)`` where ``halt_code`` is ``None`` when the
drain_cycle/orchestrator.py:433:``pane_id`` is the tmux pane ID opened for this issue (or ``None``).
drain_cycle/orchestrator.py:531:# as an interactive session at the repo root.
drain_cycle/orchestrator.py:561:# for drain sessions and knows which completion sequence to enforce.
drain_cycle/orchestrator.py:576:# Watch mode: run claude inside a tmux pane (so the operator sees the
drain_cycle/orchestrator.py:577:# live session) and read its stream-json off a FIFO instead of a
drain_cycle/orchestrator.py:578:# subprocess pipe. ``watch_pane.open_session`` returns ``None`` if the pane
drain_cycle/orchestrator.py:580:# and we fall back to a normal subprocess spawn — the pane is a
drain_cycle/orchestrator.py:581:# convenience, not a requirement. ``pane_id`` is returned to the caller […]

> TOOL

tool_use Read
id: toolu_01JaxnWMswz4xtZTNn6WQncd
```json
{
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/orchestrator.py",
  "offset": 570,
  "limit": 95
}
```

> TOOL

tool_result
id: toolu_01JaxnWMswz4xtZTNn6WQncd
```
570	        issue_span.set_attribute("issue.model", worker_model)
571	
572	        debug_file = log.debug_path(identifier) if debug else None
573	        if debug_file is not None:
574	            console.worker_event(identifier, f"debug capture → {debug_file}")
575	
576	        # Watch mode: run claude inside a tmux pane (so the operator sees the
577	        # live session) and read its stream-json off a FIFO instead of a
578	        # subprocess pipe. ``watch_pane.open_session`` returns ``None`` if the pane
579	        # or FIFO can't be brought up (having torn down its own partial state),
580	        # and we fall back to a normal subprocess spawn — the pane is a
581	        # convenience, not a requirement. ``pane_id`` is returned to the caller
582	        # for lifecycle management; ``external_stream``/``kill_fn`` steer the
583	        # worker onto the external path.
584	        session: watch_pane.WatchSession | None = None
585	        pane_id: str | None = None
586	        external_stream: TextIO | None = None
587	        kill_fn: Callable[[], None] | None = None
588	        if watch and in_tmux:
589	            argv = worker.build_argv(
590	                _CLAUDE_CMD,
591	                model=worker_model,
592	                prompt=agent_prompt,
593	                cost_limit_usd=limits.per_issue_cost_usd,
594	                debug_file=debug_file,
595	            )
596	            session = watch_pane.open_session(argv, worktree_path)
597	            if session is not None:
598	                pane_id = session.pane_id
599	                external_stream = session.stream
600	                kill_fn = session.kill
601 […]

> AGENT

Now I understand the wiring: the main worker gets a tmux pane (`watch_pane.open_session` → `external_stream`/`kill_fn`), but both finishing-recovery `run_issue` calls omit those **and** omit `on_progress` — so during finishing there's zero per-turn feedback. Let me check how the watch pane is laid out relative to the orchestrator's stderr, to know whether a stderr heartbeat is even visible in watch mode.

> TOOL

tool_use Bash
id: toolu_01DTCLktcLFepXuwK16jYFeg
```json
{
  "command": "grep -n \"split\\|select-pane\\|tmux\\|def open_session\\|def close_pane\\|def kill\\|class WatchSession\\|def cleanup\\|window\" drain_cycle/watch.py | head -40",
  "description": "Inspect tmux pane layout in watch module"
}
```

> TOOL

tool_result
id: toolu_01DTCLktcLFepXuwK16jYFeg
```
18 matches in 1 files:

drain_cycle/watch.py:1:"""Watch-mode tmux pane + FIFO plumbing for a spawned ``claude`` session.
drain_cycle/watch.py:4:``claude ... | tee <fifo> | <formatter>`` in a tmux split-pane and reads the
drain_cycle/watch.py:34:(tmux accepted the split-window but the command died), so the drain never
drain_cycle/watch.py:39:class WatchSession:
drain_cycle/watch.py:55:def kill(self) -> None:
drain_cycle/watch.py:58:def cleanup(self) -> None:
drain_cycle/watch.py:62:def open_session(
drain_cycle/watch.py:67:Runs ``argv | tee <fifo> | <formatter>`` in a tmux split-pane (in ``cwd``,
drain_cycle/watch.py:70:*any* failure — no tmux, non-zero split-window exit, a pane that never
drain_cycle/watch.py:88:def close_pane(pane_id: str) -> None:
drain_cycle/watch.py:89:"""Kill a tmux pane by ID; swallows all errors.
drain_cycle/watch.py:96:["tmux", "kill-pane", "-t", pane_id],
drain_cycle/watch.py:126:"""Open a tmux split-pane running ``argv`` piped through ``tee`` into a FIFO.
drain_cycle/watch.py:129:splits the stream — the FIFO branch carries byte-for-byte stream-json to
drain_cycle/watch.py:136:``split-window -P -F "#{pane_id}"`` prints the new pane's ID directly so we
drain_cycle/watch.py:139:FIFO or pane could not be created — every failure (tmux not on PATH,
drain_cycle/watch.py:140:non-zero exit, any OS error) is swallowed so a broken tmux environment
drain_cycle/watch.py:157:"tmux", "split-window", "-d",
```

> AGENT

The watch pane is a tmux **split** (`split-window`), so the orchestrator's stderr stays visible in the original pane alongside the worker's split. That means the operator *would* see a heartbeat from the orchestrator — but the finishing `run_issue` calls pass **no `on_progress`** (and emit no completion line), so for 7 minutes both panes went silent. Let me check `_worker_log_fields` so I can emit a meaningful completion line.

> TOOL

tool_use Bash
id: toolu_01EFcTxLUj1GhTfuRzvkR7TT
```json
{
  "command": "grep -n \"_worker_log_fields\\|def _worker_log_fields\\|num_turns\\|cost_usd\" drain_cycle/orchestrator.py | head; echo \"---\"; sed -n '/def _worker_log_fields/,/^def /p' drain_cycle/orchestrator.py | head -30",
  "description": "Read _worker_log_fields helper"
}
```

> TOOL

tool_result
id: toolu_01EFcTxLUj1GhTfuRzvkR7TT
```
15 matches in 1 files:

drain_cycle/orchestrator.py:92:cost_usd=log.cycle_cost_usd() or None,
drain_cycle/orchestrator.py:179:def _worker_log_fields(result: worker.WorkerResult) -> dict[str, object]:
drain_cycle/orchestrator.py:190:"cost_usd": result.cost_usd,
drain_cycle/orchestrator.py:191:"num_turns": result.num_turns,
drain_cycle/orchestrator.py:259:**_worker_log_fields(outcome.result),
drain_cycle/orchestrator.py:396:cost_usd=log.cycle_cost_usd(),
drain_cycle/orchestrator.py:593:cost_limit_usd=limits.per_issue_cost_usd,
drain_cycle/orchestrator.py:625:cost_usd: float | None,
---
def _worker_log_fields(result: worker.WorkerResult) -> dict[str, object]:
    """Map a ``WorkerResult`` onto the run-log entry's usage fields.

    Shared by all three worker-backed ``append_entry`` calls (timeout
    halt, Done, not-Done halt) so the recorded usage shape can't drift
    between branches.
    """
    return {
        "duration_seconds": result.duration_seconds,
        "model": result.model,
        "usage": result.usage,
        "cost_usd": result.cost_usd,
        "num_turns": result.num_turns,
        "session_id": result.session_id,
        "is_error": result.is_error,
    }


@dataclass(frozen=True)
class _WorkerOutcome:
    """The post-spawn verdict/responder trio plus the worker result, gathered
    once after the worker exits and passed as a unit to the halt epilogue and
    the span-attribute writer so the recorded shape can't drift across branches.
    """

    result: worker.WorkerResult
    outcome_verdict: dict | None = None
    prep_verdict: dict | None = None
    responder_runs: list[dict] = field(default_factory=list)
```

> AGENT

Now I'll add live progress feedback (`on_progress`) and a completion line to both finishing-recovery spawns. Let me view the current not-Done block precisely:

> TOOL

tool_use Read
id: toolu_01BM2UQ8MQi8TfPukiK3HLaN
```json
{
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/orchestrator.py",
  "offset": 740,
  "limit": 40
}
```

> TOOL

tool_result
id: toolu_01BM2UQ8MQi8TfPukiK3HLaN
```
740	            )
741	            if not _prior_verifier_failed:
742	                finishing_attempted = True
743	                console.worker_event(
744	                    identifier, "not-Done with commits: spawning finishing sub-agent"
745	                )
746	                _finishing_started = _now_iso()
747	                _finishing_result = worker.run_issue(
748	                    claude_cmd=_CLAUDE_CMD,
749	                    model=_FINISHING_MODEL,
750	                    prompt=prompt.build_finishing(
751	                        identifier, worktree_path, base, stack=stack
752	                    ),
753	                    cwd=worktree_path,
754	                    token_limit=limits.per_issue_tokens,
755	                    time_limit_seconds=limits.per_issue_seconds,
756	                    cost_limit_usd=limits.per_issue_cost_usd,
757	                    passthrough=console.AgentSink(),
758	                )
759	                _finishing_finished = _now_iso()
760	                finishing_runs.append({
761	                    "trigger": "err-issue-not-done",
762	                    "started_at": _finishing_started,
763	                    "finished_at": _finishing_finished,
764	                    **_worker_log_fields(_finishing_result),
765	                })
766	                finished_at = _finishing_finished
767	                # Re-read to see whether finishing succeeded. In stack mode the
768	                # finishing agent records ``pr_urls`` and (per governance) leaves
769	                # the issue In Progress, so re-read the submission signal too —
770	                # the success gate below accepts it whether or not Done was set.
771	                refreshed = linear.get_issue(issue["id"])
772	                post_spawn_state = refreshed["state"]["name"]
773	                is_done = refreshed["state"]["type"] == _DONE_STATE_TYPE
774	                issue_span.set_attribute("issue.is_done", is_done)
775	                submitted = handoff.read(worktree_path) if stack else None
776	                # Pull any verdicts the finishing agent wrote to the handoff so
777	                # the verifier gate below uses the freshest available signal.
778	                _fhov, _fhpv = handoff.read_partial(worktree_path)
779	                if _fhov is not None or _fhpv is not None:
```

> TOOL

tool_use Edit
id: toolu_01UuWduQr5HemURVr3Dr28vz
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/orchestrator.py",
  "old_string": "                _finishing_started = _now_iso()\n                _finishing_result = worker.run_issue(\n                    claude_cmd=_CLAUDE_CMD,\n                    model=_FINISHING_MODEL,\n                    prompt=prompt.build_finishing(\n                        identifier, worktree_path, base, stack=stack\n                    ),\n                    cwd=worktree_path,\n                    token_limit=limits.per_issue_tokens,\n                    time_limit_seconds=limits.per_issue_seconds,\n                    cost_limit_usd=limits.per_issue_cost_usd,\n                    passthrough=console.AgentSink(),\n                )\n                _finishing_finished = _now_iso()\n                finishing_runs.append({\n                    \"trigger\": \"err-issue-not-done\",\n                    \"started_at\": _finishing_started,\n                    \"finished_at\": _finishing_finished,\n                    **_worker_log_fields(_finishing_result),\n                })\n                finished_at = _finishing_finished",
  "new_string": "                _finishing_started = _now_iso()\n                # The finishing agent runs on the spawned (non-pane) path, so the\n                # watch split-pane can't mirror it. Route its per-turn progress\n                # through ``on_progress`` so the orchestrator pane keeps ticking —\n                # otherwise a normal multi-minute finishing run reads as a hang.\n                _finishing_result = worker.run_issue(\n                    claude_cmd=_CLAUDE_CMD,\n                    model=_FINISHING_MODEL,\n                    prompt=prompt.build_finishing(\n                        identifier, worktree_path, base, stack=stack\n                    ),\n                    cwd=worktree_path,\n                    token_limit=limits.per_issue_tokens,\n                    time_limit_seconds=limits.per_issue_seconds,\n                    cost_limit_usd=limits.per_issue_cost_usd,\n                    on_progress=_make_on_progress(marker, identifier),\n                    passthrough=console.AgentSink(),\n                )\n                _finishing_finished = _now_iso()\n                _log_finishing_done(identifier, _finishing_result)\n                finishing_runs.append({\n                    \"trigger\": \"err-issue-not-done\",\n                    \"started_at\": _finishing_started,\n                    \"finished_at\": _finishing_finished,\n                    **_worker_log_fields(_finishing_result),\n                })\n                finished_at = _finishing_finished"
}
```

> TOOL

tool_result
id: toolu_01UuWduQr5HemURVr3Dr28vz
```
The file /Users/anton/src/drain-cycle/drain_cycle/orchestrator.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now the stack-no-PRs site:

> TOOL

tool_use Edit
id: toolu_014LEgeYwWjRyiZJqNJVFie3
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/orchestrator.py",
  "old_string": "                    _finishing_started = _now_iso()\n                    _finishing_result = worker.run_issue(\n                        claude_cmd=_CLAUDE_CMD,\n                        model=_FINISHING_MODEL,\n                        prompt=prompt.build_finishing(\n                            identifier, worktree_path, base, stack=stack\n                        ),\n                        cwd=worktree_path,\n                        token_limit=limits.per_issue_tokens,\n                        time_limit_seconds=limits.per_issue_seconds,\n                        cost_limit_usd=limits.per_issue_cost_usd,\n                        passthrough=console.AgentSink(),\n                    )\n                    _finishing_finished = _now_iso()\n                    finishing_runs.append({\n                        \"trigger\": \"err-stack-no-prs\",\n                        \"started_at\": _finishing_started,\n                        \"finished_at\": _finishing_finished,\n                        **_worker_log_fields(_finishing_result),\n                    })\n                    finished_at = _finishing_finished",
  "new_string": "                    _finishing_started = _now_iso()\n                    _finishing_result = worker.run_issue(\n                        claude_cmd=_CLAUDE_CMD,\n                        model=_FINISHING_MODEL,\n                        prompt=prompt.build_finishing(\n                            identifier, worktree_path, base, stack=stack\n                        ),\n                        cwd=worktree_path,\n                        token_limit=limits.per_issue_tokens,\n                        time_limit_seconds=limits.per_issue_seconds,\n                        cost_limit_usd=limits.per_issue_cost_usd,\n                        on_progress=_make_on_progress(marker, identifier),\n                        passthrough=console.AgentSink(),\n                    )\n                    _finishing_finished = _now_iso()\n                    _log_finishing_done(identifier, _finishing_result)\n                    finishing_runs.append({\n                        \"trigger\": \"err-stack-no-prs\",\n                        \"started_at\": _finishing_started,\n                        \"finished_at\": _finishing_finished,\n                        **_worker_log_fields(_finishing_result),\n                    })\n                    finished_at = _finishing_finished"
}
```

> TOOL

tool_result
id: toolu_014LEgeYwWjRyiZJqNJVFie3
```
The file /Users/anton/src/drain-cycle/drain_cycle/orchestrator.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now add the `_log_finishing_done` helper next to `_worker_log_fields`:

> TOOL

tool_use Edit
id: toolu_01T9gpMMZGnroRBZAWJzy5eL
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/drain_cycle/orchestrator.py",
  "old_string": "@dataclass(frozen=True)\nclass _WorkerOutcome:",
  "new_string": "def _log_finishing_done(identifier: str, result: worker.WorkerResult) -> None:\n    \"\"\"Emit a completion line for a finishing sub-agent.\n\n    The finishing agent runs off the watch pane, so without an explicit\n    end-of-run line the orchestrator pane would fall silent when it exits —\n    the same blind spot that makes an in-flight finishing run look hung. The\n    line mirrors the worker's ``=== done ===`` frame: turns and cost, flagged\n    if the session errored.\n    \"\"\"\n    cost = \"n/a\" if result.cost_usd is None else f\"${result.cost_usd:.2f}\"\n    suffix = \" (error)\" if result.is_error else \"\"\n    console.worker_event(\n        identifier,\n        f\"finishing sub-agent done: {result.num_turns} turns, {cost}{suffix}\",\n    )\n\n\n@dataclass(frozen=True)\nclass _WorkerOutcome:"
}
```

> TOOL

tool_result
id: toolu_01T9gpMMZGnroRBZAWJzy5eL
```
The file /Users/anton/src/drain-cycle/drain_cycle/orchestrator.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01VDRxz2pWHKyrHih2QH6r8Z
```json
{
  "command": "uv run --quiet pytest tests/test_orchestrator_finishing.py tests/test_orchestrator_runlog.py tests/test_orchestrator_watch.py -q 2>&1 | tail -15",
  "description": "Run finishing, runlog, watch tests"
}
```

> TOOL

tool_result
id: toolu_01VDRxz2pWHKyrHih2QH6r8Z
```
......................                                                   [100%]
22 passed in 21.01s
```

> AGENT

Let me add a regression assertion that the finishing completion line is emitted (the visibility fix):

> TOOL

tool_use Edit
id: toolu_01WjgJuth2xMi1c9RCzhCaoQ
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/tests/test_orchestrator_finishing.py",
  "old_string": "def test_finishing_sub_agent_recovers_not_done_with_commits(\n    tmp_path: Path, monkeypatch: pytest.MonkeyPatch\n) -> None:\n    \"\"\"Not-Done + commits → finishing sub-agent runs and marks Done → run continues.\"\"\"",
  "new_string": "def test_finishing_sub_agent_recovers_not_done_with_commits(\n    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]\n) -> None:\n    \"\"\"Not-Done + commits → finishing sub-agent runs and marks Done → run continues.\"\"\""
}
```

> TOOL

tool_result
id: toolu_01WjgJuth2xMi1c9RCzhCaoQ
```
The file /Users/anton/src/drain-cycle/tests/test_orchestrator_finishing.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01AK97sDTjvzda6zm2QfwsPe
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/tests/test_orchestrator_finishing.py",
  "old_string": "    # finishing_runs records the sub-agent spawn\n    assert len(entry[\"finishing_runs\"]) == 1\n    assert entry[\"finishing_runs\"][0][\"trigger\"] == \"err-issue-not-done\"",
  "new_string": "    # finishing_runs records the sub-agent spawn\n    assert len(entry[\"finishing_runs\"]) == 1\n    assert entry[\"finishing_runs\"][0][\"trigger\"] == \"err-issue-not-done\"\n    # The finishing run emits a completion line so its exit is visible off the\n    # watch pane (the blind spot that makes an in-flight finishing run look hung).\n    stderr = capsys.readouterr().err\n    assert \"finishing sub-agent done\" in stderr"
}
```

> TOOL

tool_result
id: toolu_01AK97sDTjvzda6zm2QfwsPe
```
The file /Users/anton/src/drain-cycle/tests/test_orchestrator_finishing.py has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01BRy2mZbQ7UPW2v1ZZpqX81
```json
{
  "command": "uv run --quiet pytest -q 2>&1 | tail -8",
  "description": "Run full suite after all changes"
}
```

> TOOL

tool_result
id: toolu_01BRy2mZbQ7UPW2v1ZZpqX81
```
........................................................................ [ 19%]
........................................................................ [ 38%]
........................................................................ [ 57%]
........................................................................ [ 77%]
........................................................................ [ 96%]
.............                                                            [100%]
373 passed in 45.56s
```

> AGENT

All 373 pass. Let me review the complete diff for correctness, especially the orchestrator control-flow changes:

> TOOL

tool_use Bash
id: toolu_0187W2HDdhbgHyjUgUbXUkck
```json
{
  "command": "git --no-pager diff --stat; echo \"=== orchestrator gate region ===\"; git --no-pager diff drain_cycle/orchestrator.py | sed -n '1,200p'",
  "description": "Show diff stat and orchestrator diff"
}
```

> TOOL

tool_result
id: toolu_0187W2HDdhbgHyjUgUbXUkck
```
drain_cycle/orchestrator.py          | 78 ++++++++++++++++++++++++++++--------
 drain_cycle/prompt.py                | 46 ++++++++++++++++-----
 drain_cycle/stop_guard.py            |  9 +++--
 tests/test_orchestrator_finishing.py | 70 +++++++++++++++++++++++++++++++-
 tests/test_prompt.py                 | 23 ++++++++++-
 5 files changed, 193 insertions(+), 33 deletions(-)
=== orchestrator gate region ===
drain_cycle/orchestrator.py | 78 +++++++++++++++++++++++++++++++++++----------
 1 file changed, 62 insertions(+), 16 deletions(-)

--- Changes ---

drain_cycle/orchestrator.py
  @@ -194,6 +194,23 @@ def _worker_log_fields(result: worker.WorkerResult) -> dict[str, object]:
  +def _log_finishing_done(identifier: str, result: worker.WorkerResult) -> None:
  +    """Emit a completion line for a finishing sub-agent.
  +
  +    The finishing agent runs off the watch pane, so without an explicit
  +    end-of-run line the orchestrator pane would fall silent when it exits —
  +    the same blind spot that makes an in-flight finishing run look hung. The
  +    line mirrors the worker's ``=== done ===`` frame: turns and cost, flagged
  +    if the session errored.
  +    """
  +    cost = "n/a" if result.cost_usd is None else f"${result.cost_usd:.2f}"
  +    suffix = " (error)" if result.is_error else ""
  +    console.worker_event(
  +        identifier,
  +        f"finishing sub-agent done: {result.num_turns} turns, {cost}{suffix}",
  +    )
  +
  +
   @dataclass(frozen=True)
   class _WorkerOutcome:
       """The post-spawn verdict/responder trio plus the worker result, gathered
  @@ -717,13 +734,23 @@ def _drain_one_issue(
  -        # Recovery: committed-but-unfinished → spawn a sonnet finishing sub-agent […]

> AGENT

The control flow is sound: `post_spawn_state` is set unconditionally at the initial refresh, push-mode behavior is unchanged (`submitted` always `None` → gate reduces to `is_done`), and the In-Progress-submitted path correctly records `final_linear_state="In Progress"` and extends the baton. Let me run the linter if the project has one, and a final import check:

> TOOL

tool_use Bash
id: toolu_018qsdtPPMgXzLX1Cpr2TazK
```json
{
  "command": "uv run --quiet ruff check drain_cycle/orchestrator.py drain_cycle/prompt.py drain_cycle/stop_guard.py 2>&1 | tail -20 || echo \"(ruff not configured)\"; echo \"=== import check ===\"; uv run --quiet python -c \"import drain_cycle.orchestrator, drain_cycle.prompt, drain_cycle.stop_guard; print('imports OK')\"",
  "description": "Lint changed modules and verify imports"
}
```

> TOOL

tool_result
id: toolu_018qsdtPPMgXzLX1Cpr2TazK
```
error: Failed to spawn: `ruff`
  Caused by: No such file or directory (os error 2)
=== import check ===
imports OK
```

> AGENT

No linter configured; imports clean; all 373 tests pass. The `orchestrator-enforced-completion` memory now describes superseded behavior (finishing agent forcing Done), so let me update it to avoid stale guidance.

> TOOL

tool_use Read
id: toolu_01NDyrZPuai14kfZDfV5sHPV
```json
{
  "file_path": "/Users/anton/.claude/projects/-Users-anton-src-drain-cycle/memory/orchestrator-enforced-completion.md"
}
```

> TOOL

tool_result
id: toolu_01NDyrZPuai14kfZDfV5sHPV
```
<system-reminder>This memory is 3 days old. Memories are point-in-time observations, not live state — claims about code behavior or file:line citations may be outdated. Verify against current code before asserting as fact.</system-reminder>
1	---
2	name: orchestrator-enforced-completion
3	description: Weak-model workers commit but skip finishing; orchestrator should recover via a finishing sub-agent (ABA-393)
4	metadata: 
5	  node_type: memory
6	  type: project
7	  originSessionId: 1e976e2b-d1ef-4117-8571-ed46c0326009
8	---
9	
10	In cycle 793fc9ea (2026-06-14), ABA-383 ran on a `model:haiku` worker that committed 4 reviewable
11	slices but exited (exit 0, clean Stop) without running the drain-mode finishing protocol (review →
12	`/shape:pr-finishing` → `.drain-handoff.json` pr_urls → Linear Done). The orchestrator's not-Done
13	halt (`orchestrator.py:781`, slug `err-issue-not-done`) reverted it to Todo and halted the run.
14	Root cause: the orchestrator delegates completeness entirely to the worker, and a weak model
15	treats "code committed" as done. Model routing itself works as designed — "haiku" is a grouped
16	Linear label rendered `model:haiku` by linear.py.
17	
18	Fix shaped into **ABA-393** (Autonomous cycle drain project): orchestrator post-check at both halt
19	sites (not-Done `:781` and stack-no-PRs `:706`) — if there are commits beyond base and the issue
20	isn't properly […]

> TOOL

tool_use Edit
id: toolu_016jK6ujkAc6BWXgMvRCUTHq
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/.claude/projects/-Users-anton-src-drain-cycle/memory/orchestrator-enforced-completion.md",
  "old_string": "Fix shaped into **ABA-393** (Autonomous cycle drain project): orchestrator post-check at both halt\nsites (not-Done `:781` and stack-no-PRs `:706`) — if there are commits beyond base and the issue\nisn't properly closed, spawn a **sonnet** finishing sub-agent (reusing `worker.run_issue` + new\n`prompt.build_finishing`) that delegates any Critical/Required **fix to opus**, then re-check and\nrecover or fall through to halt. Uncommitted-only / empty branch = genuine failure, never trusted.\nDelivery plan: `docs/delivery-plans/orchestrator-enforced-completion/`. Relates to\n[[stack-pr-submission-regression]] Inc2.",
  "new_string": "Fix shaped into **ABA-393** (Autonomous cycle drain project): orchestrator post-check at both halt\nsites (not-Done and stack-no-PRs) — if there are commits beyond base and the issue\nisn't properly closed, spawn a **sonnet** finishing sub-agent (reusing `worker.run_issue` + new\n`prompt.build_finishing`) that delegates any Critical/Required **fix to opus**, then re-check and\nrecover or fall through to halt. Uncommitted-only / empty branch = genuine failure, never trusted.\nDelivery plan: `docs/delivery-plans/orchestrator-enforced-completion/`. Relates to\n[[stack-pr-submission-regression]] Inc2.\n\n**SUPERSEDED governance (2026-06-18, ABA-394 post-mortem):** the orchestrator success gate no\nlonger keys on the Linear **Done** state — it keys on the **submission signal** (`pr_urls` in\nexec-state.json). In **stack mode**, a worker (or finishing sub-agent) that submits its PR and\nleaves the issue **In Progress** is complete; the issue stays In Progress until the PR *merges* —\nnothing transitions […]

> TOOL

tool_result
id: toolu_016jK6ujkAc6BWXgMvRCUTHq
```
The file /Users/anton/.claude/projects/-Users-anton-src-drain-cycle/memory/orchestrator-enforced-completion.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

All three defects are fixed and the full suite (373 tests) is green. Nothing is committed yet.

## What changed

**Defect #1 — governance collision (the real bug)**

The orchestrator keyed "complete" on the Linear **Done** state, but the `exec:*` skill now leaves issues **In Progress** until the PR merges. That mismatch is what spawned the redundant finishing pass on ABA-394 and flipped it to Done. Fixed by making the orchestrator key on the **submission signal** (`pr_urls`) instead:

- `orchestrator.py` — read `submitted = handoff.read(...)` up front; the not-Done recovery now fires only when `submitted is None`; the success gate is `if is_done or submitted is not None:`. A stack worker that submitted its PR and stayed In Progress is now accepted as complete (baton extended, `final_linear_state="In Progress"`), with no finishing pass. Push mode is unchanged (`submitted` is always `None` there → gate reduces to `is_done`).
- `prompt.py` — `build_finishing` is now mode-aware (`stack=` param): stack mode tells the agent to **leave In Progress** (PR is the completion signal); push mode still marks Done.
- `stop_guard.py` — the stack block-prompt no longer says "transition to Done."

**Defect #2 — watch-pane blackout**

The finishing sub-agent runs off the tmux split-pane, and […]