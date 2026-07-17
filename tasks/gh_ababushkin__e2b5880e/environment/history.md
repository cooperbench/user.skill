> AGENT

I'll run the idea-intake skill. First let me capture the idea verbatim and ground my opening hypothesis in how drain-cycle currently selects work — so my restate isn't a guess.

> TOOL

tool_use Bash
id: toolu_01CmpfcAR6cXF2dKjbYYYXWt
```json
{
  "command": "ls && echo \"---README---\" && (ls docs/app-context.md 2>/dev/null && echo \"app-context EXISTS\" || echo \"no app-context.md\")",
  "description": "List repo root and check for app-context"
}
```

> TOOL

tool_result
id: toolu_01CmpfcAR6cXF2dKjbYYYXWt
```
.claude/
.entire/
.private-journal/
.ruff_cache/
.worktrees/
docs/
drain_cycle/
tests/
.env  64B
.gitignore  769B
.linear_config  247B
AGENTS.md  131B
CLAUDE.md  223B
LICENSE  1.0K
README.md  16.3K
conftest.py  966B
mise.toml  24B
pyproject.toml  738B
uv.lock  78.1K
---README---
no app-context.md
```

> TOOL

tool_use Bash
id: toolu_01CdwJarTXokyVHMTu6Ydrhp
```json
{
  "command": "grep -rn \"cycle\" --include=\"*.py\" -l src 2>/dev/null | head; echo \"---\"; grep -rniE \"def .*(cycle|drain|select|fetch).*issues|argparse|add_argument|--cycle|--project\" --include=\"*.py\" src 2>/dev/null | head -40",
  "description": "Find how drain target is selected"
}
```

> TOOL

tool_result
id: toolu_01CdwJarTXokyVHMTu6Ydrhp
```
---
```

> TOOL

tool_use Bash
id: toolu_014SbGYBNDr9eqpoJVZwgF6P
```json
{
  "command": "ls drain_cycle/; echo \"---ARG PARSING---\"; grep -rniE \"add_argument|argparse|--cycle|--project|cycle_id|active.?cycle|current.?cycle\" --include=\"*.py\" drain_cycle 2>/dev/null | head -40",
  "description": "Inspect drain_cycle package and arg parsing"
}
```

> TOOL

tool_result
id: toolu_014SbGYBNDr9eqpoJVZwgF6P
```
__init__.py  0B
cli.py  4.2K
console.py  4.8K
handoff.py  7.6K
kr2_check.py  1.7K
limits.py  6.9K
linear.py  12.1K
model.py  1.6K
orchestrator.py  47.2K
progress.py  3.4K
prompt.py  6.0K
repos.py  7.9K
runlog.py  10.7K
scorecard.py  4.4K
status.py  2.2K
stop_guard.py  9.6K
swimlanes.py  17.0K
telemetry.py  4.5K
watch.py  8.0K
watch_format.py  6.4K
worker.py  24.7K
worktree.py  10.5K
---ARG PARSING---
drain_cycle/console.py:73:    cycle_id: str,
drain_cycle/console.py:82:    c.rule(f"[bold]drain-cycle[/bold]  cycle {cycle_id}")
drain_cycle/linear.py:74:def current_cycle_id() -> str:
drain_cycle/linear.py:75:    """Return the active cycle id for the configured team."""
drain_cycle/linear.py:78:        query CurrentCycle($name: String!) {
drain_cycle/linear.py:82:              activeCycle { id }
drain_cycle/linear.py:88:        operation="current_cycle",
drain_cycle/linear.py:93:    cycle = nodes[0].get("activeCycle")
drain_cycle/linear.py:95:        raise RuntimeError(f"Linear team {_TEAM_NAME!r} has no active cycle")
drain_cycle/linear.py:208:def pending_issues(cycle_id: str) -> ExecutionPlan:
drain_cycle/linear.py:244:        {"cycleId": cycle_id, "stateTypes": _PENDING_STATE_TYPES},
drain_cycle/scorecard.py:69:    # Group entries by cycle_id, preserving chronological file order.
drain_cycle/scorecard.py:72:        cid = payload.get("cycle_id", "<unknown>")
drain_cycle/orchestrator.py:112:def _resume_attempts(cycle_id: str, identifier: str) -> int:
drain_cycle/orchestrator.py:115:    Globs ``~/.drain-cycle/runs/<cycle_id>-*.json`` and tallies entries
drain_cycle/orchestrator.py:131:    for path in runlog.runs_dir().glob(f"{cycle_id}-*.json"):
drain_cycle/orchestrator.py:318:    """Drain the current cycle inside the ``drain.cycle`` root span.
drain_cycle/orchestrator.py:339:    cycle_id = linear.current_cycle_id()
drain_cycle/orchestrator.py:340:    cycle_span.set_attribute("drain.cycle_id", cycle_id)
drain_cycle/orchestrator.py:341:    log = runlog.RunLog(cycle_id=cycle_id)
drain_cycle/orchestrator.py:343:        plan = linear.pending_issues(cycle_id)
drain_cycle/orchestrator.py:357:        console.orch(f"Cycle {cycle_id} has no Todo/Backlog issues — nothing to do.")
drain_cycle/orchestrator.py:361:        cycle_id,
drain_cycle/orchestrator.py:411:            cycle_id=cycle_id,
drain_cycle/orchestrator.py:467:    cycle_id: str,
drain_cycle/orchestrator.py:536:            prior_halts = _resume_attempts(cycle_id, identifier)
drain_cycle/orchestrator.py:651:            "cycle_id": cycle_id,
drain_cycle/runlog.py:8:Downstream consumers glob the directory and group by ``cycle_id``
drain_cycle/runlog.py:12: […]

> TOOL

tool_use Read
id: toolu_01GK27agQbvTQyh4tofsXbMa
```json
{
  "file_path": "/home/<USER>/src/drain-cycle/drain_cycle/cli.py"
}
```

> TOOL

tool_result
id: toolu_01GK27agQbvTQyh4tofsXbMa
```
1	"""``drain-cycle`` CLI entry point.
2	
3	Zero-arg invocation drains the current Linear cycle. Each issue's target
4	repo is resolved from a ``repo:<name>`` label against
5	``~/.drain-cycle/repos.yml``; the operator runs ``drain-cycle`` from
6	anywhere, not from inside a target repo. The ``scorecard`` subcommand reads
7	the run logs and reports per-run quality.
8	
9	Secrets load before any module reads ``os.environ``, first hit wins:
10	shell-exported vars → ``~/.drain-cycle/.env`` → the drain-cycle repo
11	root ``.env`` (dev-checkout fallback, absent once installed as a uv
12	tool). ``load_dotenv`` defaults to ``override=False``, so an
13	already-set var always beats a later source and the shell always wins.
14	
15	``repos.yml`` and the optional ``limits.yml`` are validated eagerly at
16	startup so a broken config halts exit 1 on stderr before any Linear
17	traffic or run-log file is written — there is no cycle yet to log
18	against. ``limits.yml`` is optional (its absence yields the baked-in
19	guardrail defaults); a present-but-malformed one still halts.
20	"""
21	from __future__ import annotations
22	
23	import sys
24	from pathlib import Path
25	
26	from dotenv import load_dotenv
27	
28	from . import limits, orchestrator, repos, scorecard, telemetry […]

> TOOL

tool_use Read
id: toolu_018u4b7KZvcM8NrQdihzbtQW
```json
{
  "file_path": "/home/<USER>/src/drain-cycle/drain_cycle/linear.py",
  "offset": 200,
  "limit": 60
}
```

> TOOL

tool_result
id: toolu_018u4b7KZvcM8NrQdihzbtQW
```
200	    already carries any literal prefix typed into the label name.
201	    """
202	    parent = node.get("parent")
203	    if parent:
204	        return f"{parent['name']}:{node['name']}"
205	    return node["name"]
206	
207	
208	def pending_issues(cycle_id: str) -> ExecutionPlan:
209	    """Return an ``ExecutionPlan`` for every Todo/Backlog issue in the cycle.
210	
211	    No pagination: personal cycles fit comfortably in one page. If a cycle
212	    ever exceeds 100 pending issues, that's a planning problem, not a tool
213	    problem (see ``PRODUCT_RULES`` Rule A5 — focus is the multiplier).
214	
215	    Post-processing flattens two wire-shape fields:
216	    - ``labels { nodes { name parent { name } } }`` → ``labels: list[str]``
217	      (grouped labels rendered as ``"<group>:<name>"``)
218	    - ``inverseRelations`` filtered to ``type == "blocks"``
219	      → ``blockers: list[{id, identifier, state_type}]``; raw key removed.
220	    """
221	    data = _post(
222	        """
223	        query CyclePending($cycleId: ID!, $stateTypes: [String!]!) {
224	          issues(
225	            filter: {
226	              cycle: { id: { eq: $cycleId } }
227	              state: { type: { in: $stateTypes } }
228	            }
229	            first: 100
230	          ) {
231	            nodes {
232	              id
233	              identifier
234	              title
235	              description
236	              sortOrder
237	              state { type name }
238	              labels […]

> AGENT

I've got the grounding I need. Here's how drain-cycle works today: zero-arg invocation drains the **active** Linear cycle (`linear.current_cycle_id()` → `pending_issues(cycle_id)` filtered to Todo/Backlog), and run logs are keyed by `cycle_id`. Your idea swaps that fixed target for a passed-in one — a project instead of the active cycle.

Let me run the intake. I'll lead with my read and confirm, rather than assume.

**My one-sentence hypothesis (confidence ~0.5, anecdotal — it's your own tool, no usage data yet):** You want to drain work that isn't in the active cycle — most likely a Linear *project* whose issues span cycles or sit in the backlog — without first having to drop those issues into the current cycle just to make drain-cycle see them.

Before I write the restate, two questions. Each carries my best guess so you can just confirm or correct.

> TOOL

tool_use AskUserQuestion
id: toolu_01X3KDi6uXNsHRVdV6q8JTif
```json
{
  "questions": [
    {
      "question": "What goes wrong today that draining a project would fix? (My guess: project work spans multiple cycles or sits in backlog, so the active-cycle-only target can't reach it without manual cycle assignment.)",
      "header": "The problem",
      "multiSelect": true,
      "options": [
        {
          "label": "Backlog work isn't cycle-bound",
          "description": "The issues you want to drain live in a Linear project but aren't assigned to the active cycle, so drain-cycle can't see them."
        },
        {
          "label": "Manual cycle-assignment is friction",
          "description": "To drain project issues today you must first drag them into the active cycle — busywork you want to skip."
        },
        {
          "label": "Want to drain a focused slice",
          "description": "You want to drain one project's issues specifically, even when the active cycle holds other unrelated work."
        },
        {
          "label": "Parallel/other-team work",
          "description": "You want to drain a project owned by a different team or running outside your personal cycle rhythm."
        }
      ]
    },
    {
      "question": "How should the target be passed? (My guess: a flag like --project <name-or-id>, defaulting to the active cycle when omitted, mirroring how repos are named.)",
      "header": "Selector",
      "multiSelect": false,
      "options": [
        {
          "label": "--project <name/id> flag",
          "description": […]

> TOOL

tool_result
id: toolu_01X3KDi6uXNsHRVdV6q8JTif
```
Your questions have been answered: "What goes wrong today that draining a project would fix? (My guess: project work spans multiple cycles or sits in backlog, so the active-cycle-only target can't reach it without manual cycle assignment.)"="Want to drain a focused slice", "How should the target be passed? (My guess: a flag like --project <name-or-id>, defaulting to the active cycle when omitted, mirroring how repos are named.)"="--project <name/id> flag". You can now continue with these answers in mind.
```

> AGENT

Good — that sharpens it. The driver is **focus**, not backlog-reach: drain one project as a unit even when the active cycle holds unrelated work. That lines up with your "focus is the multiplier" rule. Selector is a `--project <name/id>` flag, active-cycle default preserved.

Two more, then I'll write the restate for your explicit yes. There's one real design seam here: run logs and the scorecard key everything on `cycle_id`. A project drain needs an identity too.

> TOOL

tool_use AskUserQuestion
id: toolu_019fqwBorCzmpuvBnrLzw6D7
```json
{
  "questions": [
    {
      "question": "When you drain a project, which of its issues should run? (My guess: every Todo/Backlog issue in the project, ignoring cycle membership — same state filter as today, just project-scoped instead of cycle-scoped.)",
      "header": "Drain scope",
      "multiSelect": false,
      "options": [
        {
          "label": "All pending in the project",
          "description": "Every Todo/Backlog issue in the project, regardless of which cycle (or no cycle) it belongs to. Same state filter, project-scoped."
        },
        {
          "label": "Pending AND in active cycle",
          "description": "Only the project's issues that are also in the active cycle — a narrower intersection."
        },
        {
          "label": "All non-Done in the project",
          "description": "Wider than today: include In Progress / Started states too, not just Todo/Backlog."
        }
      ]
    },
    {
      "question": "Run logs + scorecard key on cycle_id today. How should a project drain identify itself? (My guess: key on project_id the same way, so scorecard groups project runs as their own unit.)",
      "header": "Run-log identity",
      "multiSelect": false,
      "options": [
        {
          "label": "Key on project_id",
          "description": "Project runs group under the project's id, parallel to cycle runs. Scorecard treats a project drain as its own unit. Minimal schema change."
        },
        {
          "label": […]

> TOOL

tool_result
id: toolu_019fqwBorCzmpuvBnrLzw6D7
```
Your questions have been answered: "When you drain a project, which of its issues should run? (My guess: every Todo/Backlog issue in the project, ignoring cycle membership — same state filter as today, just project-scoped instead of cycle-scoped.)"="All pending in the project", "Run logs + scorecard key on cycle_id today. How should a project drain identify itself? (My guess: key on project_id the same way, so scorecard groups project runs as their own unit.)"="Key on project_id". You can now continue with these answers in mind.
```

> AGENT

I have enough to predict your answers to the next questions. Here's the six-line restate — confirm with a yes, or correct any line.

---

**Refined intent — drain a Linear project as a focused unit**

- **Outcome:** drain-cycle can target one Linear project, running every Todo/Backlog issue in it as a unit, independent of the active cycle.
- **User:** you, the operator — when you want to push one project to completion without the active cycle's unrelated work coming along.
- **Why now:** focus is the multiplier (Rule A5); the active-cycle-only target forces project work and other work to drain together, diluting the run.
- **Success:** `drain-cycle --project <name/id>` drains all the project's pending issues; zero-arg still drains the active cycle, unchanged; the scorecard groups the project run as its own unit (keyed on `project_id`).
- **Constraint:** zero-arg behaviour and the existing run-log/scorecard readers must not break; same Todo/Backlog state filter, just project-scoped instead of cycle-scoped.
- **Out of scope:** wider state filters (In Progress), project-∩-active-cycle intersection, multi-team orchestration, any `{source_type, source_id}` schema generalisation.

---

**Assumptions surfaced:** project name resolves to a Linear project id the same way the team name resolves to a cycle id; a project drain […]