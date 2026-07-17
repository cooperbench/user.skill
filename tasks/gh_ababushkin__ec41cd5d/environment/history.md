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
Output too large (50.9KB). Full output saved to: /home/<USER>/.claude/projects/-Users-anton-src-drain-cycle/75418cc5-ca2f-42e9-9cbf-74ba261dd2d7/tool-results/b54bipw77.txt

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
  "file_path": "/home/<USER>/src/drain-cycle/drain_cycle/orchestrator.py",
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