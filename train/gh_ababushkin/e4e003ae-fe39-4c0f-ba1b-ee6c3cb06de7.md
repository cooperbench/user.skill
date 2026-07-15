> DEVELOPER

[Image #1] i'm re-thinking the architecture for this project and this is my rough idea that i'm going through at the moment. review it, critique it and lets collaboratively design something better

one idea i had was that this project effectively could have been a set of claude skills, eg: /execute-project or /execute-cycle and then it will create a precrafted prompt and go through a workflow to create a "team of agents" in claude. i don't think it has to be this way necessarily as this feature is not cross-portable between different agent paradigms but i still like this way of encapsulating the implementation. overall i need to have a clearer understanding of what the "orchestator" and all the code that's been written is for and what the control plane should look like

> AGENT

Let me ground myself in your current north-star docs before critiquing, since the new sketch has to be judged against the vision.

> TOOL

tool_use Read
id: toolu_01NnyhJkKeBWQbxuSy4S7P7w
```json
{
  "file_path": "/Users/anton/src/drain-cycle/docs/vision.md"
}
```

> TOOL

tool_use Read
id: toolu_01PMRdm8RZh32RacpiCkJYnZ
```json
{
  "file_path": "/Users/anton/src/drain-cycle/docs/architecture.md"
}
```

> TOOL

tool_result
id: toolu_01PMRdm8RZh32RacpiCkJYnZ
```
1	# Architecture
2	
3	How `drain-cycle` is built to serve the vision. The vision ([`docs/vision.md`](vision.md)) is the stable north-star — the *why*; this doc is the *how*, and it changes as the system does. The running decision log beneath it, with rationale and alternatives per change, is [`docs/design-decisions.md`](design-decisions.md).
4	
5	These section numbers are stable anchors — other docs cite them (e.g. `§8` for the autonomy horizon).
6	
7	## 1. Two layers, one product
8	
9	The work splits into two layers, and `drain-cycle` is only the top one.
10	
11	- **Layer 1 — supervision (`drain-cycle`).** Picks up a Linear cycle, spawns a worker per issue, holds the guardrails, halts/reverts/resumes/recovers, and records and grades the outcome. It is vendor-agnostic: the worker is a `claude -p` (or any equivalent) subprocess.
12	- **Layer 2 — workflow (the Shaper pack).** The intra-issue procedure, captured as composable skills: how a piece of work goes from picked-up to merged PR. This is the knowledge that used to live in the operator's head, written down once.
13	
14	The vision's three pieces map onto this split: "one place for state" is the state plane (§6), "the steps become skills" is Layer 2, and "the supervision becomes a supervisor" is Layer 1.
15	
16	## 2. The artifact boundary
17	
18	The two layers meet at an artifact, not at a function call. **Layer 2 writes signals; Layer 1 reads them.** The supervisor never reads the workflow's steps — only the artifacts the workflow leaves behind: Linear issue state, run-log fields, and `.drain-handoff.json` (e.g. `pr_urls`).
19	
20	The placement test for any new behaviour: does `drain-cycle` need to know *what a role does* (Layer 2), or only *whether an artifact exists* (Layer 1)? Submitting a PR is "what a role does" — it belongs in a skill. Reading back the submitted PR URLs to decide whether to advance is "whether an artifact exists" — it belongs in the supervisor (see design decision §19).
21	
22	Keeping the boundary at the artifact is what makes Layer 1 content-blind, and content-blindness is what lets the same Layer 2 run under any worker.
23	
24	## 3. Dual-mode: the same skills by hand or unattended
25	
26	Because the workflow is skills and the supervisor only reads artifacts, the same skills run two ways: the operator invokes them at the keyboard, or a spawned worker runs them unattended. There is one workflow, exercised two ways — not a manual path and a separate automated path that drift apart.
27	
28	Design decision §10 (config symlinked into each worktree) is what makes the headless worker's environment match an interactive session, so a skill behaves the same in both modes.
29	
30	## 4. Layer 2 — the workflow pack
31	
32	The pack carries two verb namespaces, one per half of the lifecycle:
33	
34	- **Planning — `shape:*`.** Four front-door skills: `shape:idea`, `shape:project`, `shape:design`, `shape:delivery`. (Consolidation tracked by the "Consolidate Shaper's Lifecycle into Four Phase Skills" project.)
35	- **Execution — `exec:*`.** The intra-issue graph, named delegations only, no inlined procedure:
36	
37	  ```
38	  exec:pickup → exec:breakdown → exec:build → (exec:debug | exec:simplify)
39	              → exec:review → exec:verify → exec:finish
40	  ```
41	
42	  `exec:pickup` is the front door; `exec:review` fans out reviewer personas; `exec:finish` is Graphite-first with a plain-git fallback and produces the trail artefacts (What/Why/Focus PR body, review-summary comment, Linear status move). The execution namespace is pinned by ADR 0004 / the Shaper `execution-workflow` design doc; that doc is authoritative for the graph and the handoff contract.
43	
44	Every step is also a standalone skill, so a human can run any one by hand. A **handoff envelope** carries the issue's acceptance criteria from pickup through to review, so the spec-compliance persona can grade *built-the-wrong-thing*, not just *built-it-badly*.
45	
46	## 5. Layer 1 — the supervisor
47	
48	`drain-cycle` owns process concerns only: spawn, guardrails, halt, revert, resume, recover, record, grade. It reads Linear state and the worker's artifacts to decide whether to advance to the next issue or stop. It does not contain workflow prose — the worker's prompt points at the entry skill and the procedure lives in Layer 2.
49	
50	The supervisor mechanics are the bulk of `docs/design-decisions.md`: worktree-per-issue (§3), resource guardrails (§9), group-kill on breach (§8), resume-on-rerun (§14), blocks-aware ordering (§12), and the watch overlay (§15).
51	
52	## 6. The state plane
53	
54	Everything works off one organized record of where the work stands. **Linear is authoritative** for issue status (design decision §1, §12). Beneath it sit the durable supervisor records: per-run logs (§4, §8), the atomic active-run marker (§11), and opt-in OpenTelemetry traces (§13).
55	
56	These records are the **delayed feedback loop** that replaces live watching. Automating supervision deliberately gives up the operator's real-time view of each worker; observability is how that trade is paid back. Better observability widens the set of work that is safe to hand off (§8).
57	
58	## 7. The keystone
59	
60	The move that realizes the whole split: **`prompt.py` becomes a thin pointer at `exec:pickup`** instead of inlining the workflow. The supervisor stops carrying procedure; the pack owns it; any vendor's worker follows the same prose. This is tracked by the "drain-cycle supervises; the pack owns the workflow" project and is the run-first step — everything else in this doc is a facet of it. Until it lands, the supervisor's prompt still names a few skills directly (e.g. the current `/code-review-and-quality` and `/shape:pr-finishing`); those references swap to `exec:*` at the keystone cutover.
61	
62	## 8. The supervisor's autonomy horizon
63	
64	How far the supervisor runs without the operator. Today it drains a cycle transactionally — one issue, one worker, one diff — and halts when it runs out of runnable work or hits a result it cannot get past. The horizon extends outward as observability earns more trust: building on unmerged work, auto-merging trusted classes, and eventually a resident process that watches its own PRs through the review-and-merge loop. That extension is shaped in [`ideas/drain-past-the-merge-gate.md`](ideas/drain-past-the-merge-gate.md).
65	
66	The horizon is a deliberate trade, not a default: autonomy is applied selectively where the delayed feedback loop (§6) makes the loss of live intervention acceptable.
67	
68	## Known open seam
69	
70	The one undecided boundary crossing: how Layer-2 verdicts (`outcome_verdict`, `prep_verdict`) travel from a skill into the run-log. Today `handoff.py` carries only `pr_urls`. The verdict-handoff schema is a one-way door for the correctness work (the "Multi-agent collaboration for correctness" Layer-1 project) and should be decided before that work starts.
71	
```

> TOOL

tool_result
id: toolu_01NnyhJkKeBWQbxuSy4S7P7w
```
1	# Vision
2	
3	## Problem
4	
5	Doing a piece of work is never a single action. It's a sequence of steps - prompt an agent to write the code, review it against the right standards, open a PR, rewrite the PR description so a person can read it, and on from there. My agent handles any one of these steps well, but only one at a time, and only after I've set it up. Each step is its own conversation: I prompt it, refine what I mean, check what comes back.
6	
7	This holds up fine for small work. But the more complex the work gets - the more thinking and planning it needs up front - the faster that workflow breaks down. And when it breaks, it's clear the thing holding the work together was me all along, doing three jobs I'd never thought to separate:
8	
9	1. **Holding the state** - where the work stands: what's done, what's next, what's blocked. Ideally this lives in one organized place. By default, in agentic development, it scatters into loose markdown files that are painful to keep straight.
10	2. **Knowing the steps** - what the steps are, what order they run in, and the standard each one has to meet. That knowledge lives in my head and comes out a little differently every time.
11	3. **Supervising the run** - moving each piece of work from one step to the next, pushing a worker from "coding" to "reviewing" to "open the PR," kicking off each step, watching what comes back, and carrying on to the next.
12	
13	The last two feel like a single job, because I do them in the same breath - I drive the work and carry the process in my head at the same time, and never notice they're two different things.
14	
15	Carrying all three myself leaves me with two problems I can't get out from under:
16	
17	1. **Execution is inconsistent.** Because the steps live in my head, the care they get depends on me. On a good day I break the work down and run every step methodically. On a worse one I get lazy, skip a step, or forget part of the process - so the same kind of work gets a different level of care depending on the day.
18	2. **I'm pinned to supervising.** Because the driving eats my attention, I can't do much else while my workers run. I can't step back to think about the next set of projects or to level myself up.
19	
20	So the problem isn't doing the work. It's that holding it all together - the state, the steps, the supervision - falls entirely on me, and the more demanding the work, the worse that gets.
21	
22	## Solution
23	
24	The way out is to stop *being* the thing that holds the work together and build that thing once instead. It rests on three pieces, and they line up with the three things the problem dumps on me - the state, the steps, and the supervision.
25	
26	**One place for state.** Everything starts from a single, organized record of where the work stands: what's done, what's next, what's blocked. Instead of each piece of work's status scattering across loose markdown files, there's one source of truth, and everything else works off it. This is the ground the rest stands on. Of the three, state was the one I already treated as its own job. The other two I carried fused - knowing the work and supervising it, done in the same breath. Pulled apart, each becomes something I can build.
27	
28	**The steps become skills.** Knowing the work is knowing what the steps are, what order they run in, and what standard each one has to meet. That knowledge used to live in my head and come out a little differently every time. I capture it as skills: one skill per step, plus a sequence that runs them in order. The process is written down once, out in the open, the same on every run.
29	
30	**The supervision becomes a supervisor.** The other half is the mechanical part - kick off each step, watch it, check it produced what it should, move to the next, stop and flag anything it can't get past. That's pure mechanics, the part of me that isn't thinking. It gets automated into a supervisor - I call it the drain-cycle - that drives the skills, verifies each result, updates the record, and carries each piece of work along on its own. I'm no longer the connector between steps. I built the connector, and my job moves up a level: I point it at a project and let it run.
31	
32	**Before - I am the connector**
33	
34	```
35	me     → "write the code for this"
36	agent  → writes it
37	me     → read it. "now review it against these standards"
38	agent  → reviews it
39	me     → "open a PR"
40	agent  → opens it
41	me     → "rewrite the PR description so it reads well"
42	agent  → rewrites it
43	me     → check it, mark it done
44	       → then start the whole chain over for the next piece of work
45	```
46	
47	I'm there at every arrow - for every piece of work in the project. And on a tired day, I skip one.
48	
49	**After - I built the connector**
50	
51	```
52	me         → "work through this project"
53	supervisor → picks up the first piece of work
54	           → runs build → review → PR → finish, checking each result
55	           → marks it done, moves to the next
56	           → ...
57	           → hits one it can't get past review, stops, tells me why
58	me         → review the finished work; step in only where it halted
59	```
60	
61	I'm there once at the start, and again only when something genuinely needs me.
62	
63	**What changes for me**
64	
65	Two things.
66	
67	First, the work gets *more consistent than I am.* Because the steps are captured once and the supervisor runs them the same way every time, execution stops depending on my discipline. It doesn't get tired, skip a step, or forget the process on a bad day, so every piece of work gets the same level of care, not whatever level I happened to have that afternoon.
68	
69	Second, my attention comes off the mechanical loop entirely. Instead of walking each piece of work through the same chain of steps, I move to the work that needs a person: scoping the next project, judging whether finished work is any good, and improving the system itself.
70	
71	And this pays off hardest exactly where the problem hurt most. The more complex the work (the more steps, the more planning) the more the old way leaned on me and the more it broke down. The new way leans on the same captured process and the same supervisor no matter how big the project gets.
72	
```

> AGENT

This is a good sketch to think against. Before I critique it, let me name the thing it's wrestling with, because your existing docs already solved half of it and the sketch quietly re-opens it.

## What your current architecture already nailed

Your `architecture.md` draws one clean line: **Layer 1 (supervisor) reads artifacts; Layer 2 (skills) owns the workflow**, and they meet at an artifact boundary, not a function call. That boundary is load-bearing — it's *the* reason the same skills run by hand or unattended, and the reason the worker can be any vendor.

Your sketch is mostly a **Layer 2 picture** (Code It / Review It / Merge It and the skills under each) with a **Layer 1 frame bolted on top** (process manager, control plane API, execution-coordinator). The trouble is the diagram doesn't respect the boundary — it draws coordinators as if Layer 1 reaches *into* each phase. Let me separate the three distinct ideas tangled in it.

## The three ideas tangled together

**1. The control plane (genuinely new — worth designing).**
`process manager → control plane API → execution-coordinator` is the only part that isn't already in your model. Today `drain-cycle` is a *one-shot CLI*: you point it at a cycle, it drains transactionally, it exits. A "control plane API + process manager" only earns its weight if you're moving to a **resident supervisor** — something you can query ("what's running?"), steer ("halt issue 3", "resume"), and that survives across cycles. That's exactly your §8 autonomy horizon ("a resident process that watches its own PRs through the review-and-merge loop"). So this isn't a redesign — it's *committing to the §8 horizon now* and giving it a shape. That's a real decision, not a diagram tweak.

**2. The per-phase "coordinators" (mostly a rename — be careful).**
`coding-agent-coordinator`, `review-agent-coordinator`, `git-agent-coordinator` map almost 1:1 onto your existing `exec:build`, `exec:review`, `exec:finish`. If they're just skills the worker invokes in sequence, you already have them — don't add a "coordinator" noun that implies a persistent process per phase. If instead you mean **a team of parallel sub-agents within one issue** (e.g. review fans out to 5 reviewer personas concurrently), note that `exec:review` *already* fans out personas. So the question is: are you introducing *new* intra-issue concurrency, or renaming the chain you have?

**3. "drain-cycle could have been a set of Claude skills" (/execute-cycle).**
You flagged the catch yourself: it's not portable. But it's sharper than that — making the *supervisor* a Claude skill **collapses the artifact boundary you deliberately built**. The supervisor's whole value is being content-blind and vendor-agnostic; a `/execute-cycle` skill runs *inside* a Claude session, so the supervisor becomes Claude-shaped and the "any vendor worker" property dies. The encapsulation you like (one entry command) you can keep *without* paying that price: a thin CLI front-door (`drain-cycle run <cycle>`) is the same ergonomics, and Layer 2 already *is* skills. So I'd keep Layer 1 as a process, not a skill.

## The critique in one line

The diagram's real flaw is that it draws **Layer 1 owning Layer 2's internals** — coordinators-with-skills-inside, under a control plane. Your strongest existing idea is that Layer 1 *never* sees inside a phase; it only reads the artifact a phase leaves behind. A better diagram keeps that: the control plane drives *issues through states*, and each state's procedure is a black box it can't see into.

Before I redraw it, three forks are genuinely yours to call — and they change the whole shape:

> TOOL

tool_use AskUserQuestion
id: toolu_01KKZiTJFTjnSfgEm4ro9iqe
```json
{
  "questions": [
    {
      "question": "Is this redesign meant to turn drain-cycle into a resident, live-controllable process (the §8 horizon), or keep it a one-shot transactional drain?",
      "header": "Control plane",
      "multiSelect": false,
      "options": [
        {
          "label": "Resident supervisor",
          "description": "A long-lived process you query/steer via an API: what's running, halt/resume an issue, survives across cycles, eventually watches its own PRs. This is what justifies a 'control plane API'."
        },
        {
          "label": "Stay one-shot",
          "description": "Point it at a cycle, it drains and exits. Then the 'control plane API + process manager' is overbuilt — drop it and the sketch collapses back to your current two layers."
        },
        {
          "label": "One-shot now, resident later",
          "description": "Design the state model so a resident process is a clean later addition, but ship the one-shot drainer first."
        }
      ]
    },
    {
      "question": "What do the per-phase 'coordinators' (coding/review/git) actually mean?",
      "header": "Coordinators",
      "multiSelect": false,
      "options": [
        {
          "label": "Just the exec:* skills renamed",
          "description": "A worker runs build → review → finish sequentially. You already have this; the 'coordinator' boxes are exec:build/review/finish. No new structure needed."
        },
        {
          "label": "New intra-issue agent teams",
          "description": "You want genuine parallel sub-agent teams within a single issue beyond the persona fan-out exec:review already does. This adds real concurrency to design."
        },
        {
          "label": "Not sure — help me decide",
          "description": "Walk through whether per-phase agent teams buy anything over the sequential single-worker model."
        }
      ]
    },
    {
      "question": "Should the supervisor stay a vendor-agnostic process, or become Claude skills (/execute-cycle)?",
      "header": "Supervisor form",
      "multiSelect": false,
      "options": [
        {
          "label": "Stay a process (CLI front-door)",
          "description": "Keep the artifact boundary and 'any vendor worker' property. Get the one-command ergonomics from a thin CLI, not a Claude skill."
        },
        {
          "label": "Become Claude skills",
          "description": "Encapsulate as /execute-cycle. Accept that the supervisor becomes Claude-shaped and the vendor-agnostic boundary is gone."
        },
        {
          "label": "Hybrid",
          "description": "Process supervisor, but a /execute-cycle skill is a thin convenience wrapper that shells out to it for interactive use."
        }
      ]
    }
  ]
}
```

> TOOL

tool_result
id: toolu_01KKZiTJFTjnSfgEm4ro9iqe
```
Your questions have been answered: "Is this redesign meant to turn drain-cycle into a resident, live-controllable process (the §8 horizon), or keep it a one-shot transactional drain?"="Resident supervisor", "What do the per-phase 'coordinators' (coding/review/git) actually mean?"="its a new agent, that is created and it's entire job is to execute various skills in sequence within that workflow to reach a certain goal. for example, the cording-agent-coordinator ensures that the coding artifacts are written in well defined, single slices. it's a fairly straight forward agent that will probably not spin off individual sub-agents. the review-agent-coordinator is also its own agent, and it's goal is to ensure all the quality criteria have been applied systematically (eg. adversarial code review, security review, reliability/resilience review and finally an outcome review). and the git-agent-coordinatr has the goal of ensuring that the work lands as a set of human-friendly ready to review PRs. double check if the "exec" skills we have meet this criteria or not", "Should the supervisor stay a vendor-agnostic process, or become Claude skills (/execute-cycle)?"="Stay a process (CLI front-door)". You can now continue with these answers in mind.
```

> AGENT

Good — answers are clear: resident supervisor, three phase-agents each owning a goal-shaped skill sequence, supervisor stays a process. Now let me verify your key question — do the existing `exec:*` skills actually deliver what your three coordinators require?

> TOOL

tool_use Bash
id: toolu_018pe3abiAfPpTuNmXssEiEd
```json
{
  "command": "find / -type d \\( -name \"shape*\" -o -name \"*exec*\" \\) 2>/dev/null | grep -iE \"skill|shape|exec\" | grep -v node_modules | head -50",
  "description": "Locate shape/exec skill directories"
}
```

> TOOL

tool_result
id: toolu_018pe3abiAfPpTuNmXssEiEd
```
/usr/libexec
/Users/anton/.executor
/opt/homebrew/Caskroom/executor
/Library/Apple/usr/libexec
/Library/Developer/CommandLineTools/usr/libexec
/opt/homebrew/Cellar/python@3.14/3.14.4_1/libexec
/opt/homebrew/Cellar/python@3.14/3.14.4/libexec
/opt/homebrew/Cellar/python@3.14/3.14.5/libexec
/opt/homebrew/Cellar/pipx/1.14.0/libexec
/opt/homebrew/Cellar/gettext/1.0/libexec
/opt/homebrew/Cellar/nss/3.123.1/libexec
/private/tmp/test-install/ABA-383/fixtures/execution-review
/private/tmp/test-install/ABA-383/skills/shape:design
/private/tmp/test-install/ABA-383/skills/exec-pickup
/private/tmp/test-install/ABA-383/skills/execution-review
/Users/anton/Library/Application Support/@executor-js
/private/var/folders/jd/9__6t9p9725glsmql48869lh0000gn/C/sh.executor.desktop.helper
/private/var/folders/jd/9__6t9p9725glsmql48869lh0000gn/C/sh.executor.desktop
/Users/anton/src/agent-skills-shaper/fixtures/execution-review
/Users/anton/src/agent-skills-shaper/skills/exec-pickup
/Users/anton/src/agent-skills-shaper/skills/execution-review
/Users/anton/src/agent-skills-shaper/docs/design-docs/execution-workflow
/Users/anton/src/agent-skills-shaper/docs/plan-reviews/execution-workflow
/Users/anton/src/agent-skills-shaper/.claude/commands/exec
/Users/anton/src/redbubble/lib/workers/executors
/Users/anton/src/agent-skills-shaper/examples/delivery-plans/issues-drain-end-to-end/D2-execution-workflow-drains-issues
/Users/anton/src/shop/app/server/lib/executeOrTimeout
/Users/anton/src/stock-screener/mcp/yf/.venv/lib/python3.14/site-packages/pandas/api/executors
/Users/anton/.codex/.tmp/plugins/plugins/superpowers/skills/executing-plans
/Users/anton/.codex/.tmp/plugins/plugins/deepnote/skills/deepnote-data-execution
/Users/anton/Library/Application Support/Cursor/logs/20260615T123201/window1/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260615T123201/window2/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260519T215251/window1_wb0/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260519T215251/window5_wb0/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260519T215251/window8/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260519T215251/window4_wb0/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260519T215251/window6/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260519T215251/window7/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260519T215251/window3/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260603T210849/window1/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260517T225955/window2_wb1/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260517T225955/window1/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260517T225955/window2_wb2/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260612T002722/window3/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260525T191947/window1/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260525T191947/window3/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260517T225955/window2_wb0/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260612T002722/window2/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260525T191947/window5/exthost/anysphere.cursor-agent-exec
/Users/anton/Library/Application Support/Cursor/logs/20260525T191947/window4/exthost/anysphere.cursor-agent-exec
```

> AGENT

The skills live in `/Users/anton/src/agent-skills-shaper`. Let me read the exec skill set and the workflow design doc to judge them against your three coordinator goals.

> TOOL

tool_use Bash
id: toolu_0114UHrbKKPgRy4SUwMS4hWL
```json
{
  "command": "cd /Users/anton/src/agent-skills-shaper && ls skills/ && echo \"---EXEC CMDS---\" && ls .claude/commands/exec/ 2>/dev/null && echo \"---DESIGN DOC---\" && ls docs/design-docs/execution-workflow/",
  "description": "List skills, exec commands, design doc"
}
```

> TOOL

tool_result
id: toolu_0114UHrbKKPgRy4SUwMS4hWL
```
debugging/
delivery/
design/
exec-pickup/
execution-review/
idea/
plan-review/
pr-finishing/
pr-prepare/
project/
render-html/
simplify/
using-this-pack/
verify-implementation/
writing-refinement/
---EXEC CMDS---
pickup.md  318B
review.md  428B
---DESIGN DOC---
design-doc.md  18.2K
Shell cwd was reset to /Users/anton/src/drain-cycle
```

> TOOL

tool_use Bash
id: toolu_01TRupfoZ4k1pMnEYQoEB52W
```json
{
  "command": "cd /Users/anton/src/agent-skills-shaper && for d in exec-pickup execution-review pr-finishing simplify debugging verify-implementation; do echo \"===== $d/SKILL.md =====\"; head -40 skills/$d/SKILL.md 2>/dev/null; done",
  "description": "Read heads of exec skill files"
}
```

> TOOL

tool_result
id: toolu_01TRupfoZ4k1pMnEYQoEB52W
```
===== exec-pickup/SKILL.md =====
---
name: exec:pickup
description: >
  Front door for draining a Linear issue end-to-end — pickup through breakdown,
  build, review, verify, and PR finishing. Every step is a named delegation to its
  owning skill; this is the supervisor pointer, not the procedure. Use when a
  drain-cycle worker or supervisor prompt picks up a Linear issue and needs a single
  entry point for the full execution workflow. Trigger phrases: "pick up this issue",
  "start working on this ticket", "drain this issue", "exec:pickup", "work on ABA-NNN".
---

# Exec: pickup

## Purpose

Take a freshly-picked Linear issue all the way to a finished PR with a full review trail. This skill reads the issue, writes a handoff envelope, and then delegates each step — breakdown, build, review, verify, finish — to its owning `exec:*` skill by name. It inlines no procedure; the named delegation is the whole of each step. The issue's acceptance criteria travel inside `pickup-envelope.json` from pickup to the spec-compliance persona in `exec:review`, re-typed by no one and lost by no one.

## When to use

- A Linear issue is assigned and a worktree is open.
{
}
[97 more lines]===== execution-review/SKILL.md =====
---
name: execution-review
description: >
  Multi-persona execution review — dispatches spec-compliance, security-auditor, and
  code-quality personas over a working-tree diff and aggregates a single deduped GO/NO-GO
  verdict. Spec compliance is reviewed first so built-the-wrong-thing is caught before
  built-it-badly. Use before any issue is transitioned to Done.
  Trigger phrases: "review this diff", "run execution review", "review before Done",
  "multi-persona review", "fan-out review", "check the diff against AC and security".
---

# Execution Review

## Purpose

A single lens misses defect classes it is not oriented to find. This skill dispatches three narrow personas in a fixed order — spec compliance, then security, then code quality — so the aggregate surfaces what any one reviewer would miss alone. Spec compliance runs first because built-the-wrong-thing must be caught before built-it-badly (the wrong sequence means the code-quality pass validates work that will be thrown away). The three personas emit structured finding triples; this skill deduplicates and aggregates them into one GO/NO-GO verdict.

## When to use

- Before any issue is transitioned to Done — the minimum review gate.
[105 more lines]===== pr-finishing/SKILL.md =====
---
name: pr-finishing
description: Finish an already-green, sliced development branch by submitting one small PR per commit slice. Use when work is complete, committed in reviewable slices, and ready for PR submission through Graphite or plain git.
---

## Purpose

`pr-finishing` turns an already-green feature branch into a stack of small PRs, one per commit slice. Prefer Graphite when available and configured; otherwise use plain git. Preserve the same PR body format on both paths.

## Use when

- Work is complete and tests pass.
- Changes are committed as independently reviewable slices, one logical change per commit.
- The operator asks to finish, submit, create stacked PRs, or submit the stack.
- Optional: a drain-cycle handoff file exists at `.drain-handoff.json`.
- Optional: a Linear issue ID is available for the final trail comment.

Do not use this skill to hide failing tests, submit a known-broken branch, or re-slice a squashed multi-change commit after the fact.

## Inputs
{
    {
    }
}
[142 more lines]===== simplify/SKILL.md =====
---
name: simplify
description: >
  Reduce complexity after code is green. Use after build passes but the implementation is
  heavier than it needs to be — simplify for clarity while preserving exact behaviour,
  leaving a reviewable before/after rationale. Trigger phrases: "clean this up", "simplify
  this", "this is over-engineered", "post-green pass", "make it readable".
---

# Simplify

## Purpose

The post-green pass that strips accidental complexity from working code while preserving exact behaviour. The one thing that must hold: every change carries a before/after rationale a reviewer can read to see why clarity improved without behaviour changing.

## When to use

- After `build` completes and all tests pass.
- The implementation feels heavier than it needs to be — unnecessary nesting, duplication, unclear names.
- A review flags readability or complexity in a working diff.
[94 more lines]===== debugging/SKILL.md =====
---
name: debugging
description: >
  Find root cause before proposing fixes. Use when stuck on a failing test, build, or
  system behaviour — hypothesis and evidence instead of guess-and-check. Trigger phrases:
  "why is this failing", "I can't figure out", "tried everything", "build keeps breaking",
  "escalate from build".
---

# Debugging

## Purpose

Diagnose broken builds and unexpected behaviour by root cause, not by guessing. The one thing that must hold: no fix is attempted before a written root-cause note names what is broken and why.

## When to use

- After three consecutive build failures without narrowing the error (escalation from `build`).
- A test fails and the cause is unclear, before attempting any fix.
- Production bugs, unexpected behaviour, performance problems, integration failures.
[89 more lines]===== verify-implementation/SKILL.md =====
---
name: verify-implementation
description: Outcome verifier — reads the ticket AC checklist and the working-tree diff, then produces a structured pass/fail verdict with one finding per unmet AC item. Use after an implementation is claimed complete and before an issue is transitioned to Done. Trigger phrases: "verify this is done", "check the implementation against AC", "is this ready to close", "did the diff satisfy the ticket", "run the outcome verifier", "verify implementation", "check AC before marking Done".
---

# Verify implementation

## Purpose

Map every AC item in a ticket against observable diff evidence — a named file, a changed block, a new function — and emit a binary verdict: pass (all AC met) or fail (at least one unmet, one finding per gap).

A fail verdict is a halt, not a suggestion: the issue does not transition to Done until each finding is resolved or explicitly accepted by the operator with a written reason. Err toward precision over recall — only call an item unmet when there is a specific, nameable gap. A false fail on AC that is actually met is the failure mode to avoid.

## When to use

- An implementation is claimed complete and the issue is about to transition to Done.
- A diff exists — working-tree, PR, or commit range — and the ticket has AC.
- You are walking a completion sequence that requires a verdict before Done.

## Do not use when
{
    {
    }
}
[99 more lines]
Shell cwd was reset to /Users/anton/src/drain-cycle
```

> TOOL

tool_use Bash
id: toolu_01FehyedyYRARfsdvF63NKZV
```json
{
  "command": "cd /Users/anton/src/agent-skills-shaper && echo \"===build SKILL (slicing)===\" && sed -n '1,40p' skills/*/SKILL.md 2>/dev/null | grep -iA3 -m1 \"slice\"; echo \"===personas in execution-review===\" && grep -iE \"persona|reliab|resil|adversar|security|spec|quality|outcome\" skills/execution-review/SKILL.md | head -30; echo \"===build skill location===\"; ls skills | grep -i build; grep -rl \"name: build\" skills/*/SKILL.md",
  "description": "Check slicing and review persona coverage"
}
```

> TOOL

tool_result
id: toolu_01FehyedyYRARfsdvF63NKZV
```
===build SKILL (slicing)===
  story", "work on this issue", "pick up this task", "start building", "implement the slice".
===personas in execution-review===
  Multi-persona execution review — dispatches spec-compliance, security-auditor, and
  code-quality personas over a working-tree diff and aggregates a single deduped GO/NO-GO
  verdict. Spec compliance is reviewed first so built-the-wrong-thing is caught before
  "multi-persona review", "fan-out review", "check the diff against AC and security".
A single lens misses defect classes it is not oriented to find. This skill dispatches three narrow personas in a fixed order — spec compliance, then security, then code quality — so the aggregate surfaces what any one reviewer would miss alone. Spec compliance runs first because built-the-wrong-thing must be caught before built-it-badly (the wrong sequence means the code-quality pass validates work that will be thrown away). The three personas emit structured finding triples; this skill deduplicates and aggregates them into one GO/NO-GO verdict.
- Any time you need a defensible review trail that separates spec, security, and quality concerns.
- **Threat modelling or full security audit** — execution-review's security-auditor persona catches structural patterns; it does not replace a dedicated security audit on high-risk surfaces.
- **Plan or spec review** — use `plan-review` or `verify-implementation` for AC verification outside a diff.
- The issue or task statement (for the spec-compliance lens)
- The acceptance criteria from the issue (spec-compliance reads these before the code; pass them explicitly if not embedded in the issue)
- **Findings** (deduped, ordered spec → security → quality): each on one line — `<file> <class> <severity>`
Before reading the diff: load `docs/adr/0003-persona-contract-and-dispatch-protocol.md` (dispatch rules), the issue statement, and the acceptance criteria.
**2. Dispatch personas — spec compliance first.**
Dispatch in this fixed order: `spec-compliance` → `security-auditor` → `code-quality`. On **Claude Code**, dispatch all three via the `Agent` tool in a single batched message (one `Agent` call per persona, parallel); the fixed order governs the *reporting* sequence, not the runtime sequence. On **non-Claude workers** (codex, kimi, or any worker without an Agent fan-out tool), run the personas inline-sequentially: load `personas/spec-compliance.md`, apply it to the diff, capture findings; then repeat for `personas/security-auditor.md`; then `personas/code-quality.md`.
Each persona receives:
- The issue statement and AC list (spec-compliance uses these; the other two may reference them for context)
Gather the raw finding triples from all three personas. Deduplicate on the match key `(file · defect_class · severity)` — if two personas surface the same triple, count it once. A finding that appears in two personas is not more severe; it is one finding with corroboration.
Use the template below. Report findings in order: spec-compliance findings first, then security-auditor, then code-quality. Within each group, Critical before Required before Suggested.
### Spec compliance
### Security
- `<file>` · `security-hole` · Critical — <one sentence>
### Code quality
| "Tests are passing so the spec compliance lens is unnecessary." | Tests verify what was tested, not what the AC required. The spec-compliance persona reads the AC directly against the diff — it cannot be substituted by a test run. |
| "I already did a code review — running three personas is overkill." | A single reviewer has a single orientation. The three lenses are narrow by design; overlap is deduped, not double-counted. The cost is one extra dispatch; the benefit is two defect classes the single reviewer wasn't looking for. |
| "Security is obvious — I'd have caught it manually." | Security findings have a strong availability bias: the obvious ones get caught; the structural ones (hardcoded secrets, string-concatenated queries) get normalised. The security-auditor persona's orientation is to find what the implementing agent normalised. |
| "The spec-compliance persona needs the full AC list, which I don't have." | If the AC is not in context, stop and retrieve it. A spec-compliance check run without the AC is a security theatre exercise: it will find nothing because it has nothing to check against. |
- Findings emitted by one persona and ignored because the other personas didn't flag them — deduplication merges, it does not suppress.
- NO-GO verdict issued without naming the specific finding that blocks merge — the implementing agent needs a file and a class to act on.
- GO verdict on a diff with non-trivial changes and zero findings — check that all three personas actually ran and received the diff.
- Spec-compliance persona run without the issue's AC list in context — it cannot check compliance against AC it has not loaded.
===build skill location===
skills/build/SKILL.md
Shell cwd was reset to /Users/anton/src/drain-cycle
```

> AGENT

Checked the skills against your three coordinator goals. Here's the honest mapping — two of the three are well covered, the review one is **not** what you described, and one capability is missing entirely.

## Do the `exec:*` skills meet your coordinator goals?

| Your coordinator | Goal you stated | Existing skill(s) | Verdict |
|---|---|---|---|
| **coding-agent-coordinator** | artifacts in well-defined single slices, loop | `build` (gated RED/GREEN/commit, smallest-first, sliced commits) + `debugging` (escalation) + `simplify` (post-green) | ✅ Covered. The slice loop is exactly `build`. |
| **review-agent-coordinator** | adversarial code + security + reliability/resilience + outcome review, applied systematically | `execution-review` (spec-compliance → security → code-quality) + `verify-implementation` (outcome, separate skill) | ⚠️ **Mismatch.** See below. |
| **git-agent-coordinator** | land as human-friendly ready-to-review PRs; respond to PR comments | `pr-finishing` (slices→stack) + `pr-prepare` (What/Why/Focus bodies, auto-merge routing) | ⚠️ PR creation ✅; **"respond to PR comments" has no skill.** |

### Where review diverges from your spec
Your review set is **{adversarial code, security, reliability/resilience, outcome}**. The shipped `execution-review` set is **{spec-compliance, security, code-quality}**, and outcome lives *outside* it in `verify-implementation`. So:

- **reliability/resilience review** — does not exist as a persona. Genuine gap.
- **outcome review** — exists but as a separate skill, not a review persona. Your model wants it *inside* the review coordinator's goal.
- **spec-compliance** — exists in the skill but wasn't in your list. You probably want it (built-the-wrong-thing is the cheapest defect to catch).
- **"adversarial"** — code-quality isn't framed adversarially today.

The fix is small: `execution-review`'s persona set is config, not architecture — adding a `reliability-resilience` persona and folding `verify-implementation` in as the outcome persona makes the skill match your coordinator's goal exactly. That's a Layer-2 edit, not a redesign.

### The one real new capability
**"respond to PR comments"** isn't a skill because it's a *resident-supervisor* behavior — it requires watching a PR after it's open, which a one-shot drain never does. It's literally your §8 horizon ("a resident process that watches its own PRs through the review-and-merge loop"). So it falls out of the "resident supervisor" answer you gave, not the current pack.

## The corrected architecture (given your three answers)

Your sketch's real contribution is the **three goal-shaped phase agents**. That's actually a refinement of today's model: right now `exec:pickup` is *one* worker running the whole chain. You're proposing *three* workers per issue, each with a tight goal and tight context, handing off **across the artifact boundary** — which is exactly the seam your architecture already trusts. That's a legitimately better factoring. Here's the redrawn version that keeps Layer 1 blind to Layer 2:

```
                      user
                        │ start / steer / query
                        ▼
        ┌───────────────────────────────────┐
        │  CONTROL PLANE  (resident process) │   ← Layer 1, vendor-agnostic
        │  - process mgr: lifecycle, daemon  │
        │  - API: status / halt / resume     │
        │  - drains a cycle, issue by issue  │
        └───────────────┬───────────────────┘
                        │ spawns per issue, reads only artifacts
        ┌───────────────▼───────────────────┐
        │  execution-coordinator (per issue) │   ← still Layer 1: sequences phases,
        │  advances on artifact, halts on    │     never reads inside a phase
        │  missing/failed artifact           │
        └──┬──────────────┬──────────────┬───┘
           │ artifact      │ artifact     │ artifact
           ▼               ▼              ▼
    ┌──────────┐    ┌────────────┐   ┌──────────┐
    │ CODE-IT  │    │ REVIEW-IT  │   │ MERGE-IT │     ← Layer 2: goal-shaped
    │ agent    │    │ agent      │   │ agent    │       worker per phase
    ├──────────┤    ├────────────┤   ├──────────┤
    │ build    │    │ spec       │   │ pr-finish│
    │ debug    │    │ security   │   │ pr-prepare│
    │ simplify │    │ reliability│   │ respond  │ ← NEW (resident)
    │ (loop,   │    │ outcome    │   │ to PR    │
    │  slices) │    │ (+adversar.)│   │ comments │
    └──────────┘    └────────────┘   └──────────┘
```

Three things this makes explicit that your sketch blurred:

1. **The control plane never touches the phase boxes.** It drives the *execution-coordinator*, which advances issues by reading artifacts (`pickup-envelope.json`, review verdict, `pr_urls`). The control plane sees *issue states*, not skills. This is the boundary that lets the worker be any vendor.

2. **The phase agents are Layer 2 — goal-shaped worker prompts, not processes.** "coding-agent-coordinator" = a `claude -p` worker whose prompt is "produce sliced artifacts" and whose body delegates to `build`/`debug`/`simplify`. No persistent coordinator daemon per phase. That keeps the resident-process count at one (the control plane), not four.

3. **The execution-coordinator vs control plane split.** In your sketch these were two stacked bars + a floating circle. Cleaner: the *control plane* is the resident daemon (one per machine, owns the API and the cycle queue); the *execution-coordinator* is the per-issue driver it spawns. Same Layer 1, two scopes (fleet vs issue).

## What I'd actually do next

The redesign is mostly **rename + one new persona + one new skill + commit to a daemon** — not a teardown. Concretely:

- **Layer 2 (cheap, do first):** add a `reliability-resilience` persona to `execution-review`; fold `verify-implementation` in as the outcome persona so Review-It's goal matches your spec.
- **Layer 1 horizon (the real work):** the resident process + control plane API + "respond to PR comments" — this is the §8 jump and the *Known open seam* in your architecture (how Layer-2 verdicts travel into the run-log) is the one-way door you must decide before building it.

One thing I'd push back on before we go further: **do you actually need three separate phase agents per issue, or one worker that runs the chain?** Three agents buys clean context isolation and lets each phase use a different model — but every phase boundary now pays a full spawn + artifact-rehydration cost, and your handoff schema has to carry *everything* the next phase needs (today one worker keeps it in context for free). That's the next decision worth making deliberately rather than inheriting from the diagram.

Want me to (a) write this up as a revision to `architecture.md` + a `design-decisions.md` entry, or (b) keep designing the control-plane API and the one-vs-three-agents question first?

> DEVELOPER

i'd still push on having 3 separate agents. an agent that coded and then subsequentely reviewing its own work is likely to lead to poor outcomes. also i will almost always anchor towards more expensive models for review even when a cheaper model was used to code it up.

having a new persona is fine as well as the fold you're suggesting

one minor tweak is that right now this project is framed as "drain a cycle", but it can also "execute a project", which is not in scope yet but will be later on. for archiecture/vision i'd rather keep it more generic (execute a planned cycle or an entire project).

the other thing is also envision that there will two additional "review it" phases:

- one at the deliverable/milestone stage: when a coordinator agent learns that an entire milestone has been completed it will launch a review phase against that milestone. i'll create some additional skills/extend existing ones later on but i currently envision: an integration/coherence review/acceptance review (similar to the task one but now at the milestone level) and a regression review (did landing this degrade anything outside its own boundary?)

- one at a whole project level: similarly but this will just do an architecture review and check against any stated goals that can be measured now (not all can be as some project goals take time to measure)

> AGENT

Both pushes make the design sharper. Let me fold them in, because together they change the shape more than they first look.

## 1. Phase separation is now a principle, not a preference

You've given the three-agent split two independent justifications, and they're stronger than "clean context":

- **Independence of verification.** The agent that wrote the code must not be the agent that judges it. A coder reviewing its own work rationalizes its own choices — separation makes the review *adversarial by construction*, not by prompt wording.
- **Per-phase model economics.** Review anchors to a stronger (more expensive) model regardless of what coded it. That's only expressible if the phase is its own spawn with its own model pin.

So the architecture should state it as a rule: **each phase is a distinct worker with its own model tier, and review is always run by an agent that did not produce the artifact.** That kills the "one worker runs the chain" alternative outright — good, it was the weaker option. The cost we accept in return: every phase boundary pays a spawn + artifact-rehydration, so the handoff envelope must carry everything the next phase needs. That's a known, bounded cost, and it's the price of independence.

## 2. Generalize the unit: "execute planned work," not "drain a cycle"

Agreed, and it's a clean generalization because the **atom doesn't change** — it's still one issue → one worker per phase. A cycle and a project are both just *containers of planned work with a hierarchy over them*. So vision/architecture language becomes: the supervisor **executes a planned unit** (a cycle now, a project later). "Drain a cycle" becomes one entry point, not the definition. `drain-cycle` stays the tool name; the concept widens.

## 3. The big one: review is multi-altitude — the dual of the delivery hierarchy

This is the most important thing you added. Your `shape:delivery` already decomposes committed work **downward**: project → deliverables/milestones → nodes → tasks. Your two new review phases say verification rolls **upward** along the same tree:

```
        DELIVERY (fans down)          REVIEW (rolls up)
   ┌─────────────────────────┐   ┌──────────────────────────────┐
   │ PROJECT                  │ ◄─┤ project review:               │
   │                          │   │  architecture + measurable    │
   │                          │   │  goals (partial; some deferred)│
   │  ├─ MILESTONE            │ ◄─┤ milestone review:             │
   │  │                       │   │  integration/coherence/accept │
   │  │                       │   │  + regression (cross-boundary)│
   │  │   ├─ TASK (issue)     │ ◄─┤ task review:                  │
   │  │   │                   │   │  spec/security/reliability/   │
   │  │   │                   │   │  quality/outcome (diff-bound)  │
   └──┴───┴───────────────────┘   └──────────────────────────────┘
```

Work fans down; verification rolls up. The review *altitude* matches the decomposition *altitude*. That symmetry is the architectural insight worth writing down, and it's elegant because the trigger is structural: a parent's review fires exactly when its last child completes.

This has **three consequences for the control plane** that I want to flag before we commit, because two of them are non-obvious one-way doors:

**(a) The execution-coordinator becomes a tree walker, not a queue drainer.** Today it's "next runnable issue." With altitude reviews it must model the hierarchy, detect "this milestone's last child just landed," and fire the milestone review. The hierarchy itself is authoritative in Linear (milestones, projects) — which fits your existing "Linear is authoritative for state" principle, so no new source of truth.

**(b) Higher-altitude review produces *new work*, not reverts.** A task review fails → you can halt before the PR merges. But a milestone review fails *after* its task PRs have merged — you can't cleanly revert a merged slice. So a failing milestone/project review must emit **new remediation issues** slotted back into the plan, not block an already-landed artifact. That's a genuinely different halt semantic from task-level, and it should be explicit in the design. (Regression review especially: "did this degrade something outside its boundary" presumes the boundary already shipped.)

**(c) Project review is partial + deferred.** You said some goals can't be measured yet. So project review isn't a single inline pass — it measures what it can *now* and **schedules** the rest. That's only possible with the resident process you committed to, and it pulls "scheduled/deferred verification" into the control-plane API as a first-class thing, not just "halt/resume/status."

## Two design unknowns these surface (candidates for a spike, not a decision now)

1. **Regression review scope.** Task review is diff-bounded (cheap, well-defined). "Did landing this milestone degrade anything outside its boundary" is *not* diff-bounded — it needs a blast-radius definition and probably a cross-repo test/check run. This is the hardest of the new pieces; I'd shape it as a `shape:design` spike before building.
2. **Remediation routing.** When an altitude review fails, what exactly gets created (new issue under the same milestone? a blocking flag on the project?) and does the supervisor pause the parent or keep draining siblings? This is the "open seam" (verdict-handoff schema) widened to higher altitudes.

---

I think the design is now coherent enough to commit to paper. I'd write it as:

- **`vision.md`** — minimal edits: generalize "drain a cycle" → "execute planned work"; the connector now also verifies at milestone and project boundaries.
- **`architecture.md`** — the substantive update: phase-separation principle (independence + model tiers), the resident control plane (process mgr + API + per-issue execution-coordinator), and the multi-altitude review hierarchy as the dual of the delivery hierarchy.
- **`design-decisions.md`** — three entries: (1) three-agent phase split over single-worker, with the independence + model-tier rationale and the rehydration cost accepted; (2) multi-altitude review + higher-altitude-review-yields-new-work-not-reverts; (3) generalize the execution unit.

Want me to draft those now, or keep pulling on the two unknowns (regression scope / remediation routing) first?

> DEVELOPER

that looks good go ahead

> TOOL

tool_use Read
id: toolu_018ZSbp1RifBioZToHrFZCXP
```json
{
  "file_path": "/Users/anton/src/drain-cycle/docs/design-decisions.md"
}
```

> TOOL

tool_result
id: toolu_018ZSbp1RifBioZToHrFZCXP
```
1	# Design decisions
2	
3	Design rationale for `drain-cycle`. Read this before making architectural changes — `AGENTS.md` points here.
4	
5	These decisions serve the project's guiding vision, [`docs/vision.md`](vision.md), and realize the architecture that serves it, [`docs/architecture.md`](architecture.md) — the two-layer supervisor/workflow split on an artifact boundary. Each decision below should hold the vision as its frame; a decision that no longer fits it is the signal to revisit the vision deliberately, not to drift from it silently.
6	
7	Nineteen decisions are recorded so a future reader doesn't have to reverse-engineer them from the code. ADRs would be heavier than this tool needs.
8	
9	## 1. The spawned agent updates Linear itself
10	
11	> **Superseded-by (pending).** The "Multi-agent collaboration for correctness" Layer-1 project replaces self-asserted Done with a **verifier-gated Done** contract: a ticket reaches Done only with a recorded `outcome_verdict` (its KR2). The supervisor records the verdict; the agent no longer asserts success unobserved. Until that lands, the decision below stands.
12	
13	The orchestrator does **not** poll Linear and write status. The spawned `claude -p` session is told, in its prompt, to move its issue to Done on completion. The orchestrator only reads Linear after the session exits, to decide whether to advance or halt.
14	
15	**Alternative considered.** Orchestrator-owned status: the parent polls Linear, transitions states, owns the lifecycle. This is more conventional and easier to reason about.
16	
17	**Why the agent-self-update path.** The orchestrator can only observe *process exit*, not *task success*. A Claude session may exit 0 having done nothing useful, or exit non-zero having actually shipped — exit code is a poor proxy for "the issue is Done." Letting the agent assert Done in Linear forces it to make an explicit, observable claim about its own outcome, which is exactly the artefact we need to grade KR1 and trigger the kill condition. If this pattern proves unreliable, that's the initiative's kill condition firing — not a bug to paper over.
18	
19	## 2. `--dangerously-skip-permissions` is accepted
20	
21	Every spawned session runs with `--dangerously-skip-permissions`. The agent can run any tool on any path inside its worktree, including shell commands, file writes, and network calls, with no operator approval.
22	
23	**Blast radius.** Bounded to the per-issue worktree under `.worktrees/<issue-identifier>/` inside the target repo, plus the operator's Linear account (the agent can transition issues), plus whatever the spawned shell can reach (env vars, secrets in `~/.config`, network egress). Not bounded to the worktree at the filesystem level — a determined or confused agent can `cd` out.
24	
25	**Why accepted.** The single-operator personal-product context: target repos are mine, the Linear workspace is mine, the machine is mine. The point of the tool is removing prompts; gating them defeats the purpose. The mitigation is **scope discipline at cycle planning** — don't drain a cycle whose issues touch credentials, production systems, or shared infrastructure. This is operator responsibility, not a tool guarantee.
26	
27	## 3. Fresh worktree per issue, not a shared workspace
28	
29	Each issue gets `.worktrees/<issue-identifier>/` branched off `main`, used once, then either removed (on Done) or preserved (on halt).
30	
31	**Alternative considered.** Shared workspace where all issues run in the target repo's main checkout in sequence. Simpler, faster, no worktree plumbing.
32	
33	**Why worktree-per-issue.** Issues drift. An agent that misunderstands its task can leave the workspace in a broken state — half-applied edits, uncommitted files, branch in the wrong place — that contaminates every subsequent issue's starting point. The worktree gives each issue a clean, identical starting point regardless of what the previous one did, and preservation-on-halt (US-B) means inspectable debug state. The cost is filesystem space and a few seconds of branch setup per issue. Cheap.
34	
35	## 4. Run-log is one file per invocation, not one file per cycle
36	
37	Each `drain-cycle` invocation writes its own run-log file at `~/.drain-cycle/runs/<cycle-id>-<run-timestamp>.json`. The per-file schema is unchanged — `{cycle_id, cycle_duration_seconds, entries: [...]}` — and `cycle_id` inside each file is how downstream readers group runs of the same cycle.
38	
39	**Alternatives considered.** (A) Multi-run schema in one file: `{cycle_id, runs: [...]}`. Faithful, but every reader has to learn the new shape and the on-disk backup file needs migrating. (B) Open-and-extend: load the existing file and append to a single flat `entries` list. Loses run boundaries, and `cycle_duration_seconds` (computed as `max(finished_at) - min(started_at)`) spans the inter-run gap and becomes misleading. (D) Refuse to clobber: fail-fast if the file exists. Breaks the unattended re-run flow the tool exists for (fix X, re-run, drain the rest) until a resume mode is built.
40	
41	**Why per-run files.** The bug being fixed (ABA-230) is that a second invocation against the same cycle silently overwrites the first run's data. Per-run files make the write path single-writer-write-once — no read-then-write race, no schema diff, no migration. US-D (ABA-197), which already plans to glob `runs/*.json` and merge across cycles, gets a one-line addition (group by `cycle_id`) instead of a new shape to read. Each file's `cycle_duration_seconds` represents one invocation's hands-off time; US-D sums them when reporting cycle-level KR2.
42	
43	**Cost.** A re-run cycle accumulates one file per invocation. At cycle scale (≤ 15 issues, rarely more than 2–3 invocations to drain) this is negligible. No retention policy is shipped; trim by hand if it ever matters.
44	
45	## 5. Each issue declares its target repo via a `repo:<name>` Linear label
46	
47	The orchestrator used to be single-repo by construction: `repo = Path.cwd()`, every worktree under `<cwd>/.worktrees/`. Cycles in this workspace span multiple repos by design — `linear-workflow.md` makes "Affected repos" part of the six initiative-readiness fields, and the Ops slot deliberately holds cross-repo maintenance issues. Each issue now carries a `repo:<name>` Linear label; `~/.drain-cycle/repos.yml` maps the name to an absolute path; the operator runs `drain-cycle` from anywhere.
48	
49	**Grouped labels are supported.** The Linear workspace uses label groups (`repo`, `model`, `wave`, …). A child label in the `repo` group — e.g. the leaf `drain-cycle` under the `repo` group — is indistinguishable from a flat `repo:drain-cycle` label to `repos.resolve`. The `pending_issues` query fetches `labels { nodes { name parent { name } } }` and renders each grouped node as `"<group>:<name>"` via `_label_name`; ungrouped nodes keep their bare name (backward-compatible with any literal `repo:<name>` labels already in use). The same rendering applies to `model` group children for `model.resolve` (§7).
50	
51	**Alternatives considered.**
52	
53	- *Description-body encoding* (e.g. a `Repo: drain-cycle` line in the markdown). The description is the most-edited surface, agents rewrite it routinely, and there's no schema enforcement. A label is one structured field with one value — Linear validates it, and a label rename triggers a clear "this label doesn't exist" error rather than silently drifting to a wrong repo.
54	- *Title prefix* (e.g. `[drain-cycle] Fix the foo`). Cleaner machine parse than the body, but every issue's title gains visual clutter for a parser-only concern. Labels don't pay that cost.
55	- *Inherit from the Linear project's "affected repos"*. Ambiguous for projects that legitimately touch multiple repos, and there is no obvious answer for the Ops container project, which is multi-repo by definition.
56	
57	**Missing-repo halt behaviour.** Same machinery as every other pre-spawn halt: write a run-log entry, print the `Halt:` line to stderr, exit 1, leave subsequent issues untouched. The new wrinkle is that resolution failures happen before any Linear state is moved, so they skip the post-spawn revert path (`_revert_to_pre_halt_state`). This is the difference from the existing setup-failure halt: that one happens after `worktree.add` or the initial `linear.set_state` attempt; the resolution halt happens before either. Either way, no revert is needed because no state was moved.
58	
59	**`repos.yml` config errors are even earlier.** A missing or malformed `repos.yml` halts the CLI at startup, before any Linear traffic and before the run-log file is created. There is no cycle yet to log against, so the failure surfaces only on stderr. This is enforced eagerly in `cli.main` so the orchestrator never sees a broken config.
60	
61	**Why labels over file conventions.** (e.g. requiring the operator to put the issue identifier in a branch comment, or use a remote-name convention). Labels are the only signal that's enforceable in Linear's UI: cycle planners can see at a glance which repo an issue targets, and the multi-repo distinction is visible at the right surface (Linear) rather than buried in a config file.
62	
63	**Out-of-v1 deliberately.** No env-var expansion inside `repos.yml`; no auto-clone if the path is missing; no parallelism across repos; no retroactive labelling of pre-cycle issues. All are operator-time concerns rather than tool-time concerns. Multi-team Linear support stays out of scope too — the tool is still hardcoded to the `Personal` team.
64	
65	## 6. Installed as a `uv tool`, with the secret read from `~/.drain-cycle/.env`
66	
67	`drain-cycle` is installed via `uv tool install`, which puts the executable on `$PATH` in an isolated environment. The Linear API key is read from `~/.drain-cycle/.env` (shell-exported vars still win), beside the `repos.yml` config and the `runs/` logs the tool already kept there.
68	
69	**Alternatives considered.**
70	
71	- *`pipx`*. Functionally equivalent for installing a Python CLI in isolation. Rejected because `uv` already anchors this repo's stack (`uv.lock`, the `mise.toml` Python pin) — adding `pipx` spends an innovation token on a second tool that does the same job.
72	- *Publish to PyPI*. Lets anyone `uv tool install drain-cycle` by name, but buys a release-and-versioning burden — tagging, changelogs, a name on the index — that a single-operator tool doesn't earn. `uv tool install git+https://…` already covers install-from-anywhere with no release step.
73	
74	**The secret-loading change this forced.** The CLI used to load `.env` only from the repo root (`Path(__file__).parent.parent`). Once installed, the package lives in the isolated tool env, where that path has no `.env` — so the key has to live somewhere stable. The load order is now shell env → `~/.drain-cycle/.env` → repo-root `.env`, first hit wins (`load_dotenv` defaults to `override=False`). The repo-root entry survives only as a dev-checkout fallback (it works under `--editable`, where `__file__` still points into the checkout); the installed tool reads the key from `~/.drain-cycle/.env`.
75	
76	**Out-of-v1 deliberately.** No PyPI release. No `drain-cycle init` command to scaffold `~/.drain-cycle/` — a missing `repos.yml` already halts with an actionable message that prints the expected shape, and `docs/repos.example.yml` is a copyable template, which is enough for a single operator.
77	
78	## 7. Workers default to Sonnet; a `model:` label overrides per issue
79	
80	A spawned `claude -p` worker inherits whatever model the operator has globally pinned. In the diagnosed quota-burn run all five workers ran on `claude-opus-4-7` (the operator's global pin), and Opus was the single largest cost multiplier of the ~108M-token spend. Workers now default to `claude-sonnet-4-6`, passed explicitly via `--model`; an individual issue opts up (or down) with a `model:<alias>` Linear label, mirroring the `repo:<name>` mechanism. Known aliases (`sonnet`/`opus`/`haiku`) map to full ids; an unrecognised value is passed to `claude --model` verbatim.
81	
82	**Why lenient, not strict.** Unlike `repo:` resolution — where a missing label is a hard halt because there is no safe default target — model resolution always has a safe fallback. So it never raises: no label, an unknown alias, or conflicting `model:` labels all fall back to the default rather than halting an unattended cycle over a label typo. The model actually used is recorded in the run log, so a mis-labelled issue surfaces after the fact instead of stalling the run.
83	
84	**Grouped model labels.** A child of the Linear `model` group — e.g. the leaf `sonnet` under `model` — renders as `model:sonnet` via the same `_label_name` projection described in §5. `model.resolve` sees it identically to a flat `model:sonnet` label.
85	
86	**Alternatives considered.** (A) Keep inheriting the global pin — rejected, it is exactly what caused the burn and gives the operator no per-issue control. (B) A single global `--model` flag with no per-issue override — simpler, but a cycle legitimately mixes cheap mechanical issues with a few that warrant Opus; per-issue is the right grain. (C) Raise on ambiguous labels like `repo:` does — rejected, halting a whole unattended cycle over a duplicate label is worse than silently taking the cheap, safe default.
87	
88	## 8. Workers use stream-json output; usage is parsed from the wire and the worker leads its own process group
89	
90	The worker launches with `claude -p --verbose --output-format stream-json` via `subprocess.Popen(..., stdout=PIPE, stderr=STDOUT, text=True, bufsize=1, start_new_session=True)`, reading output line by line in a reader thread. The per-issue run-log entry gains `model`, a `usage` block (the four token components + `cumulative` + `peak_context`), `cost_usd`, `num_turns`, `session_id`, `is_error`, and an explicit `duration_seconds`; the file gains top-level `cycle_cost_usd` and `cycle_tokens_cumulative`. All of this lives in `drain_cycle/worker.py`; the orchestrator calls `worker.run_issue(...)` and records the result.
91	
92	**The problem.** A run that burned ~108M tokens left the operator with no on-disk record of *which issue* spent what — usage had to be reconstructed from `~/.claude/projects/*.jsonl`. Spend is the metric the cost guardrail (a downstream slice) acts on, so it has to be captured at the source.
93	
94	**Why parse the stream rather than the JSONL transcript.** The transcript files are keyed by session and live outside the worktree; correlating them back to an issue after the fact is exactly the manual step this removes. The event stream is emitted by the process we already spawn, in real time, and carries everything we need.
95	
96	**Token accounting — dedup by `message.id`.** The same `assistant` message is emitted *once per content block* (thinking, text, tool_use), each copy repeating the identical `message.usage`. Summing per event double-counts a turn, so usage is keyed by `message.id` and counted once. `cumulative` sums all four token components across turns — the real billed total, dominated in long tool-use loops by cache reads re-paid every turn (this is what the 108M figure was). `result.usage` is deliberately *not* used for the totals: it is only the final turn's snapshot, and it is absent entirely when a session is killed before finishing. The terminal `result` event is authoritative only for `cost_usd` (`total_cost_usd`), `num_turns`, `session_id`, `is_error`; those are `null` on a killed session.
97	
98	**Why `start_new_session=True` + `os.killpg`.** The old `subprocess.run(timeout=)` killed only the direct child on timeout, orphaning grandchildren — MCP servers, sub-agents — that kept consuming. Making the worker a process-group leader and SIGKILLing the whole group on the time cap reaps them. SIGKILL with no SIGTERM grace is deliberate: a session past its deadline has no clean-shutdown work worth waiting for, and SIGKILL is the only signal a wedged grandchild cannot ignore. Killing the group also closes the stdout pipe those grandchildren inherited, which is what lets the reader thread reach EOF instead of blocking.
99	
100	**Additive schema.** `grade.py` reads only `cycle_id` and `entries[].final_linear_state` / `exit_code`, so the new fields don't touch grading and pre-existing run logs grade unchanged. Entries written before any session runs (resolution and setup-failure halts) carry `null` for the worker fields but keep the same key set.
101	
102	- **Parallelism.** Issues run one at a time. The Linear cycle is the unit; intra-cycle parallelism adds resource contention and serialises poorly with the agent-self-update pattern (two agents racing to mark different issues Done is fine, but two agents racing on overlapping files is not).
103	- **Retry.** Superseded by §14 — a halted issue is now resumed automatically on re-run by reusing its preserved worktree, bounded by ``max_resume_attempts``. The operator-owned manual path (inspect, fix, redo, descope) still applies; the change is that the default `drain-cycle` re-run no longer fails on a leftover worktree.
104	- **Cross-cycle scheduling.** One cycle per invocation. Chaining cycles is an operator concern.
105	
106	## 9. Resource guardrails: a native cost belt and orchestrator token/time suspenders
107	
108	Before this, the only ceiling on a worker was a 3600s wall-clock timeout, and the cycle as a whole had none. A single diagnosed run burned ~108M tokens across five issues with no circuit-breaker. `drain_cycle/limits.py` now defines per-issue and cycle-wide caps on tokens, wall-clock, and cost, enforced in two layers:
109	
110	- **Native belt.** The per-issue cost cap is passed to `claude` as `--max-budget-usd`, so the session self-terminates on spend without the orchestrator watching it.
111	- **Orchestrator suspenders.** The per-issue token and time caps are enforced by the worker against the live event stream: a poll loop compares the running cumulative-token tally and elapsed wall-clock against the caps and SIGKILLs the session's process group on the first breach (reusing the group-kill machinery from decision 8). The cycle-wide caps are enforced by the orchestrator between issues — after each Done issue it sums the run log's running totals and stops the run if any cycle cap is crossed.
112	
113	**Why both layers.** The cost belt is the cheapest possible enforcement — `claude` already meters its own spend — but it only knows about *this* session's dollars, and a subscription user cares about tokens, not dollars. The token cap is therefore the primary guardrail and has to be the orchestrator's job, since `claude` exposes no `--max-tokens` equivalent for a whole session. Time is enforced the same way because a session can wedge while emitting no usage at all (the old 3600s timeout's job), so wall-clock can't be inferred from the token stream.
114	
115	**Why the cycle caps live in the orchestrator, not the worker.** A worker only sees its own issue. The failure mode the cycle caps exist for is death-by-aggregate: every issue stays comfortably under its per-issue cap while their sum drains the quota (8M × 5 = 40M, past a 30M cycle cap, with no single issue ever breaching). Only the orchestrator, which holds the run log's running totals, can see that — so it checks after each Done issue and stops before spawning the next.
116	
117	**Defaults: per-issue 8M tokens · 20 min · $15; cycle 30M tokens · 90 min · $60.** These are deliberately generous starting points sized below the diagnosed bad run (one issue alone hit 43M tokens / 23 min), not tuned values. The intent is a circuit-breaker that trips on the pathological case, not a tight budget. They are meant to be recalibrated against real run-log spend.
118	
119	**Each guardrail is independently on/off-able.** Any cap can be `None` (off). The defaults are all live; an operator turns one off with `null` in the optional `~/.drain-cycle/limits.yml`. With both the per-issue token and time caps off, the worker simply waits for the session to exit on its own — there is no longer any implicit outer timeout, which is the operator's explicit choice when they disable both.
120	
121	**The time cap absorbed the old 3600s timeout.** Rather than keep a separate hardcoded outer timeout alongside the configurable time cap, the time cap *is* the timeout — `per_issue_seconds` (default 20 min, tighter than the old 3600s and below the diagnosed 23-min overrun). One time concept, configurable, instead of two.
122	
123	**Breach reporting.** A breach is a small `Breach(scope, metric, limit, observed)` value whose `describe()` renders the operator-facing line — used verbatim by the worker (per-issue kill) and the orchestrator (cycle stop) so the wording can't drift. A per-issue breach takes the existing exit-1 + revert + `halt_reason` contract, naming the cap and the value at kill time. A cycle breach lands in the run log's top-level `cycle_halt_reason`: the breaching issue's own entry is a normal Done, and the top-level field explains why the run stopped.
124	
125	**`limits.yml` semantics and validation.** Absent key → baked-in default; explicit `null` → guardrail off; positive number → override. A present-but-malformed file (unknown key, non-positive, non-numeric, bool, invalid YAML) raises `LimitsConfigError` and halts at CLI startup — mirroring the eager `repos.yml` validation (decision 5). The reasoning is sharper here: silently falling back to defaults on a typo would leave the operator believing a tighter cap was active when it wasn't, which is worse than a loud halt.
126	
127	**Alternatives considered.**
128	
129	- *CLI flags to override limits per invocation.* Deferred. The acceptance criteria require only defaults + `limits.yml`, and `cli.main` is a deliberately minimal exact-match dispatcher (decision in `cli.py`); adding an argument parser to thread per-run overrides is scope the single operator can cover by editing `limits.yml`. Revisit if a use case for one-off overrides appears.
130	- *Kill on the cycle cap mid-stream (pass cycle-so-far totals into the worker).* Rejected as unnecessary: the per-issue cap (8M) is below the cycle cap (30M), so a single issue can't cross the cycle cap before crossing its own; checking between issues catches the aggregate case without coupling the worker to cycle state.
131	- *A separate hardcoded outer timeout kept alongside the configurable caps.* Rejected — two time concepts where one suffices (see above).
132	
133	## 10. Headless workers inherit project-scoped config by symlink
134	
135	The operator noticed entire.io's checkpointing didn't take effect during a headless drain. The hypothesis was that the worker's worktree cwd (`.worktrees/<id>`) diverges from an interactive session at the repo root. A reproduction run confirmed the divergence and sharpened the cause (below); the resolution is to symlink the repo's project-scoped config into each worktree at spawn, restoring parity.
136	
137	**What was observed (claude 2.1.150).** Running `claude -p --debug-file <path>` from the repo root vs. from a fresh `git worktree` of the same repo, then diffing the debug logs:
138	
139	| | Repo root | Worktree |
140	|---|---|---|
141	| Settings files watched | user `~/.claude/settings.json` + **project** `.claude/settings.json` + `.claude/settings.local.json` | **user only** |
142	| Project `.claude/settings.json` | loaded | "Broken symlink or missing file encountered" |
143	| entire.io hooks | SessionStart + SessionEnd fire ("Entire CLI will link this conversation to your next commit") | **absent — zero references** |
144	| User-scoped plugins (crit, hookify, agent-skills, security-guidance) | "Registered 7 hooks from 15 plugins" | **identical: "Registered 7 hooks from 15 plugins"** |
145	
146	**The cause is project-scoped registration in a gitignored file — not cwd alone, and not plugins generally.** entire registers its hooks in the project-scoped `.claude/settings.json`. That file is gitignored (`.gitignore` ends with `.claude`). A `git worktree` is a fresh checkout of *tracked* files only, and git reports the worktree directory as its own `--show-toplevel`, so Claude Code resolves the project root to the worktree and finds no `.claude/` there. User-scoped plugins and MCP servers — registered under `~/.claude/` — are cwd-independent and load identically in both, which is why the symptom looked like "some plugins" rather than "all hooks": only the project-scoped ones drop out. The original hypothesis (worktree cwd) was right that cwd is involved, but the operative mechanism is the gitignored project-settings file, not cwd by itself; were `.claude/settings.json` tracked, the worktree checkout would carry it.
147	
148	**Reproduction step (one-shot).** From a target repo with project-scoped hooks registered in `.claude/settings.json`:
149	
150	```bash
151	# Repo root — interactive-equivalent project root
152	claude -p --debug-file /tmp/root.debug.log --model claude-sonnet-4-6 \
153	  --max-budget-usd 0.50 "Reply with exactly: ok"
154	
155	# Fresh worktree — the worker's actual cwd
156	git worktree add -b repro .worktrees/repro main
157	( cd .worktrees/repro && claude -p --debug-file /tmp/worktree.debug.log \
158	    --model claude-sonnet-4-6 --max-budget-usd 0.50 "Reply with exactly: ok" )
159	git worktree remove --force .worktrees/repro && git branch -D repro
160	
161	# Diff the loaded settings/hooks. The worktree run is missing the project
162	# settings file and any hook registered in it.
163	grep -iE 'settings.json|Registered .* hooks|<your-plugin-name>' /tmp/root.debug.log
164	grep -iE 'settings.json|Registered .* hooks|<your-plugin-name>' /tmp/worktree.debug.log
165	```
166	
167	The same capture is wired into the worker as an opt-in: `DRAIN_CYCLE_DEBUG=1 drain-cycle` passes `--debug-file` to every spawned session, landing one `<run-log-stem>-<issue>.debug.log` per issue beside the run log in `~/.drain-cycle/runs/`. It is off by default — the diagnostic is for one-shot investigation, not steady-state overhead, and debug output goes to the file rather than stderr so the usage parser's stream is unaffected.
168	
169	**Decision — symlink a configurable set of project config into each worktree.** The earlier hesitation was upstream of the mechanism: it wasn't obvious headless checkpointing was even *wanted*, since a `drain-cycle` worktree is a throwaway branch. That resolved in favour of wanting it — the checkpoint links a session to the commit it produces, and that commit is pushed to `main` before the worktree is removed, so the link outlives the branch. The operator wants the same project tooling headless as interactively.
170	
171	After `worktree.add`, the orchestrator calls `worktree.link_project_config`, which symlinks the repo's real project-config entries into the new worktree. Because each link points at the live dir, the worker reads *and writes* the repo's actual config exactly as a non-worktree run does — so a stateful hook like entire's checkpointing works and persists. Teardown needs no special handling: `git worktree remove` deletes the worktree directory and its symlinks but not the link targets, so the repo's real `.claude/` and `.entire/` survive.
172	
173	This depends on a precondition: every configured path must be gitignored in the target repo. The defaults (`.claude`, `.mcp.json`) and `.entire` are gitignored in a typical repo, so the symlink is invisible to git in the worktree (it shares the repo's tracked `.gitignore`) and the worker's `git add` never stages it. A non-ignored, untracked entry would be the opposite: the worker would stage the symlink into the commit it pushes, and `git worktree remove` would then refuse the dirty worktree. The link step doesn't enforce this — it skips a name only when it's absent in the repo or already present in the worktree — so the requirement is documented (`repos.yml` comment, README) rather than coded. The link step is also not transactional: if `os.symlink` fails partway through the set, the already-created links remain and the failure surfaces as a pre-spawn "setup failed" halt, leaving the worktree in place for inspection.
174	
175	The linked set is configurable. It defaults to `[.claude, .mcp.json]` — sensible for any repo — and is overridden by an optional `worktree_config_paths` list in `repos.yml`. `.entire` is not a default, because not every repo uses entire.io; an operator who does adds it there. Entries must be relative paths without `..`, since they are resolved inside the repo and linked into the worktree.
176	
177	Symlink beat the alternatives. Passing `--settings <repo>/.claude/settings.json` loads only one file and leaves four other surfaces broken: `settings.local.json`, project agents/skills/commands, hook scripts whose paths are relative to `$CLAUDE_PROJECT_DIR`, and `.mcp.json`. Copying the config (rather than linking) isolates the worker but discards entire's checkpoint writes when the worktree is removed. Tracking `.claude/` in git would commit machine-specific config. The accepted tradeoff: a worker runs `--dangerously-skip-permissions`, so it shares — and could mutate — the live config dirs, exactly as a non-worktree run would (decision 2).
178	
179	## 11. Active-run marker lives above `runs/` as `~/.drain-cycle/active.json`
180	
181	Without a live-run signal there is no way to distinguish a working run from a hung one: the run-log gains an entry only on issue completion, and the orchestrator emits only sparse stderr lines. The fix is an active-run marker — a small JSON file written before each spawn and removed in the worker's try/finally — that a second terminal can read with `drain-cycle status`.
182	
183	**Why `~/.drain-cycle/active.json`, not inside `runs/`.** The `grade` command globs `runs/*.json` and groups files by `cycle_id`. A marker placed in `runs/` would either corrupt a grading run (if it looks like a run log) or require `grade` to skip it by sentinel field (fragile coupling). Placing the marker at `~/.drain-cycle/active.json` — one level above `runs/` — means `grade`'s glob never sees it and the two concerns share no code path.
184	
185	**Why not `runs/active.json`.** Same issue: inside `runs/` it's in the glob's scope. A separate directory (`~/.drain-cycle/live/`) was considered but adds a layer without benefit; a single well-named file at the parent level is enough.
186	
187	**Why atomic write (temp-file rename).** `drain-cycle status` reads the marker from a different process, potentially mid-write. `Path.write_text` is not atomic: the file is truncated before the new content is written, so a reader arriving between those two steps sees an empty file. Rename is atomic on POSIX filesystems: the reader sees either the old complete content or the new complete content, never a partial write. The temp file uses a `.tmp` extension adjacent to the marker (`active.json.tmp → active.json`), not a different directory, so the rename is always within the same filesystem mount.
188	
189	**Why the progress block is updated on every new turn, not on every raw JSON line.** The worker's stream-json output emits one event per content block per turn (thinking, text, tool_use) — a single turn with a thinking + tool_use block produces two events carrying the identical usage. Firing the callback on every raw event would write the file multiple times per turn with the same data, wasting I/O and producing redundant stderr lines. The reader thread deduplicates by message id: the callback fires once per unique message id, which is once per turn. The first event in a turn records the turn; subsequent events with the same id are no-ops for the callback.
190	
191	**Stale marker detection.** A crash or SIGKILL leaves the marker on disk (the try/finally doesn't run on SIGKILL). `drain-cycle status` checks `os.kill(pid, 0)` — if the pid is gone it reports a stale marker rather than a live run. It does not delete the marker automatically; the operator removes it with `rm`, preserving forensic evidence of the interrupted run.
192	
193	## 12. Execution order: manual drag-order only, blocks-aware
194	
195	Before this change the orchestrator ordered issues by `(priority, sortOrder)` and ignored blocks/blocked-by entirely. Priority overrode the operator's manual drag-order, and a blocked issue could run before its blocker — wasting a worker on work that couldn't succeed.
196	
197	**Decision.** Order purely by manual `sortOrder` ascending; drop `priority` from sorting. Overlay a topological pass (Kahn's algorithm) using `(sortOrder, id)` as the tiebreak among ready issues: each issue is "ready" once all its intra-drain blockers have been scheduled. This preserves the operator's intended drag-order as far as dependencies allow.
198	
199	**External unresolved blocker → defer.** If a pending issue is blocked by an issue not in this drain's runnable set — including an In Progress issue in the same cycle, which the drain won't complete — the blocked issue is deferred: left Todo, not spawned, logged to stderr. Deferral cascades: if X is deferred and X intra-drain-blocks Y, Y defers too (falls out naturally from Kahn, since Y's in-degree never reaches zero while X is treated as permanently deferred). The exclusion rule is "defer unless the blocker is `completed` or `canceled`" — so `started`/`unstarted`/`backlog`/`triage` external blockers all defer. Deferred issues are not run-logged: they were never attempted, and counting them in `done/attempted` would corrupt `grade`'s completion signal.
200	
201	**Intra-drain cycle → halt.** If the blocks graph among the pending issues contains a cycle (self-loop included), `DependencyCycleError` is raised, the orchestrator sets `cycle_halt_reason`, prints a `Halt:` line naming the involved issues, and exits 1. Nothing runs.
202	
203	**`pending_issues` return type changed from `list[dict]` to `ExecutionPlan`.** The pure function `_plan(issues) -> ExecutionPlan` replaces `_sort_pending_issues`. `ExecutionPlan` is a frozen dataclass carrying `order: list[dict]` (runnable issues, topo-sorted) and `deferred: list[dict]` (each entry has `issue`, `blocker_identifier`, `blocker_state_type`). `DependencyCycleError(RuntimeError)` carries `identifiers: list[str]` for the cycle report. The `inverseRelations` GraphQL field is fetched in `pending_issues`, flattened to `issue["blockers"] = [{id, identifier, state_type}]`, and the raw key dropped — wire shape stays local to `pending_issues`, like `labels`.
204	
205	**All-deferred → exit 0.** If `plan.order` is empty but `plan.deferred` is not, the run emits the stderr deferral lines and returns 0: the cycle isn't broken, it's just blocked externally. An empty `plan.order` with an empty `plan.deferred` is also exit 0 ("nothing to do").
206	
207	**Alternatives considered.**
208	
209	- *Keep priority in the sort key.* Rejected: the operator has one predictable knob — the manual drag-order — and priority overriding it is surprising and undesirable.
210	- *Ignore blocks entirely.* Rejected: running a blocked issue wastes a worker on work that can't succeed by definition.
211	- *Best-effort run instead of defer/halt.* Rejected: silently violating a dependency the operator encoded is worse than a loud skip or stop.
212	- *Record deferrals in the run log.* Rejected: a deferred issue was never attempted; counting it as an entry corrupts `done/attempted` in `grade`.
213	
214	## 13. Opt-in OpenTelemetry tracing to Honeycomb
215	
216	A drain runs unattended and can take hours, spending real tokens across many spawned sessions. The run log records the outcome per issue, but it is one flat file per invocation — it can't show where time went inside a drain, how the Linear round-trips and worker sessions nest, or let an operator aggregate cost across drains. Tracing fills that gap.
217	
218	**Decision.** Each invocation emits one trace: a `drain.cycle` root span, a `drain.issue` span per attempted issue, and under those the `drain.worker.session`, `drain.worktree.add`/`.remove`, and per-operation `linear.*` spans. The `httpx` transport is auto-instrumented, so every Linear GraphQL POST appears as a child of its `linear.*` span. Worker token/cost/turn usage, the issue's repo/model/final-state, and the cycle outcome ride as span attributes; every halt site is tagged with a static `exception.slug` (greppable, low-cardinality, safe to `GROUP BY`). `service.name` is `drain-cycle`, which is also the Honeycomb dataset.
219	
220	**Opt-in via `HONEYCOMB_API_KEY`.** The key's presence in the environment is the on/off switch. Absent, `telemetry.setup()` is a no-op and the default no-op tracer stays installed — a drain with no telemetry configured behaves exactly as before, takes no new network dependency at runtime, and the `start_as_current_span` calls scattered through the code cost nothing. The OTel packages are unconditional install-time dependencies (lightweight, pure-Python); only *exporting* is gated.
221	
222	**Flush-on-exit is load-bearing.** `drain-cycle` is a short-lived CLI that exits through `sys.exit`. A `BatchSpanProcessor` buffers spans and exports on a timer, so without an explicit flush the queued spans die with the interpreter and the last issues of a drain never ship. `setup()` registers `shutdown()` (which flushes the processor) with `atexit`; `SystemExit` still runs `atexit` handlers, so every exit path drains the queue.
223	
224	**Alternatives considered.**
225	
226	- *`opentelemetry-instrument` zero-code agent.* Rejected: it wraps a `python` invocation, but the tool ships as a `uv tool` console-script entry point (`drain-cycle`), so there is no `python app.py` to wrap. Programmatic setup in `telemetry.setup()` is reliable regardless of how the entry point is launched.
227	- *Always-on tracing.* Rejected: it would force an exporter and an egress dependency on an operator who hasn't asked for it, and fail noisily (or silently retry) when Honeycomb is unreachable. Opt-in keeps the default path dependency-free.
228	- *Metrics and logs alongside traces.* Out of scope. The run log already covers durable per-issue accounting; traces add the causal/nesting view. A metrics layer can be added later if cost-rate alerting is wanted (see the otel-instrumentation layering guidance).
229	- *A span per private helper (e.g. `_plan`, `link_project_config`).* Rejected as over-instrumentation: those are fast, pure, and not independently aggregable. Interesting, failure-prone, or aggregable operations get spans; the rest stay as attributes on their parent.
230	
231	## 14. Halted issues resume on re-run by reusing the preserved worktree
232	
233	Before this, a halted issue's worktree was preserved on disk for the operator to inspect, but a re-run of `drain-cycle` against the same cycle would call `git worktree add` on the same path and fail opaquely — every halt required a manual `rm -rf .worktrees/<id>` plus `git worktree prune` plus `git branch -D <id>` before the next run could even reach the spawn. That friction punished the exact workflow the tool exists for: "halt, inspect, re-run, drain the rest."
234	
235	**Decision.** `worktree.ensure` replaces `worktree.add` in the orchestrator's pre-spawn path: if a worktree is already registered at `repo/.worktrees/<identifier>`, it is reused as-is (no mutating git command runs, so a dirty index, staged or untracked files, and the gitignored config symlinks all survive untouched); otherwise it falls through to `add` exactly as before. The handle returned carries a `resumed: bool` flag that the orchestrator threads into `prompt.build(..., resumed=…)`. When true, the spawned prompt prepends a "Resuming issue …" directive that tells the agent to run `git log --oneline main..HEAD` and `git status` first to read what is already done before continuing — so the agent does not restart from scratch and clobber the prior work.
236	
237	**Bounded by `limits.max_resume_attempts`.** A perma-stuck issue would otherwise consume an attempt on every re-run forever. The orchestrator counts prior halted attempts for the issue across the cycle's run-log files (entries with a non-Done `final_linear_state` matching the identifier) and refuses to spawn once that count *exceeds* the cap. The refusal is a no-spawn halt: no Linear `set_state`, no worktree manipulation, no worker invocation; a halt entry is still written so KR1 grading sees the refused attempt and the halt line names the cap so the operator knows how to clear it (raise the cap, clear prior runs, or finish by hand). The semantic follows the stdlib `urllib3` / `requests` convention for `max_retries`: `max_resume_attempts=N` allows up to N resumes *after* the initial attempt, for `N+1` total halts before refusal. The default is 3 (one fresh attempt + three resumes = four total halts before the fifth would be refused); `null` removes the cap entirely. `max_resume_attempts` is a *policy* cap, not a runtime guardrail in the §9 sense — no `Breach` is raised, the check is purely pre-spawn against the run-log history, and the field validation is integer-only (`1.5` would be incoherent on a count).
238	
239	**Why the cap-halt fires before `worktree.ensure` and `set_state`.** The point of refusing is to leave the issue exactly where it was so the operator can intervene without untangling a half-done re-run. Calling `worktree.ensure` first would be harmless (`ensure` is read-only on the worktree-already-registered branch), but `set_state(In Progress)` would not — a refused attempt that nevertheless flipped Linear to In Progress would silently exclude the issue from the next `pending_issues` query and the cycle would stall invisibly. The order is: resolve repo → resume-cap check → `worktree.ensure` → `link_project_config` → `set_state` → spawn. Each step is a pure no-op until the one before it succeeds.
240	
241	**Why "resumed" is a prompt directive, not a worker flag.** The worker is just a `claude -p` subprocess; the only contract surface between orchestrator and agent is the prompt string. Adding a CLI flag for "resumed" to the worker would still resolve to "include this paragraph in the system context," and the prompt is already that context. The four-segment ordering in `prompt.py` (title → body → preamble → tail) is load-bearing; the resume directive inserts as the first line of the preamble (after the `---` separator, before "Execution instructions:") so the agent reads it ahead of the procedure while `_TAIL` keeps the last-line position the ordering reserves for it.
242	
243	**Run-log entries treat resume halts the same as first-attempt halts.** A halt entry written on a resumed run has identical shape to one from a fresh attempt — same `final_linear_state`, same `worktree_path`, same `halt_reason` template via `_halt_message`. This is deliberate: KR1 grading and the cap-counting helper both read `final_linear_state` per entry, and giving resumed halts a different shape would split the schema into two cases for no benefit. The cap-halt entry uses `exit_code=-1` (the no-spawn sentinel, like the resolution and setup-failure halts in §8/§5) and carries the cap-specific message in `halt_reason` so the operator can grep for it.
244	
245	**This supersedes the `rerun-after-halt-detect-cleanly` plan (`docs/tasks/`).** That earlier doc proposed a `PriorArtefactsExist` exception that would convert the leftover worktree into a clean `Halt:` line — same friction, prettier error. The resume path eliminates the friction entirely: the operator's mental model is "re-run drains the rest," and `drain-cycle` now matches it. The task doc carries a supersession note pointing here.
246	
247	**Alternatives considered.**
248	
249	- *Auto-delete the preserved worktree on re-run.* Rejected. The worktree exists because §3 chose preservation-on-halt for inspectability (US-B). Deleting it on re-run means the operator's evidence is gone the moment they re-run, which is the worst-of-both: they cannot inspect (deleted) but also cannot resume (fresh worktree, no prior work). Preservation + resume is the only combination that lets the operator both inspect *and* re-run.
250	- *Refuse to re-run while a halted worktree exists, force `drain-cycle clean <id>` first.* Rejected as scope creep — a new subcommand plus a new gating rule, both to enforce the workflow `drain-cycle` already trains. The mental model "halt, inspect, re-run" is the one operators have; a forced clean step adds friction without adding safety (the operator could already have re-run after deletion in the old model).
251	- *Resume by replaying the agent's last few turns from the worker stream-json log.* Rejected. The transcript is keyed by session and lives outside the worktree (§8); reconstructing context from it duplicates what `git log main..HEAD` and `git status` already tell the agent at the start of a resume. Two sources of truth where one suffices.
252	- *Resume by passing `--continue` or `--resume <session-id>` to `claude -p` instead of changing the prompt.* Rejected because a halted worker may have died mid-turn with no clean session boundary; the next worker is a fresh `claude -p` against a worktree that already has commits. The prompt directive is the right level of abstraction: "this worktree carries prior committed work; read it before continuing." The mechanism is the same whether the prior session lived for one turn or one hour.
253	- *Cap-halt resets when the operator manually marks the issue Done in Linear.* Considered — the cap counts non-Done entries, so a manual Done in Linear does NOT directly reset the cap, because the prior halted entries in the run log still carry their non-Done `final_linear_state`. The operator clears the cap by raising it, deleting the relevant run-log files, or simply not re-running. This is fine: the cap exists to prevent infinite resume loops, not to track Linear state — Linear state can flip independently of the on-disk history.
254	
255	## 15. `--watch` runs claude *in* the tmux pane, not a formatter tailing a log
256	
257	In `--watch` mode the operator wants to see the agent working in real time. The pane therefore **is** the `claude` session: the orchestrator runs `claude … | tee <fifo>` in a `tmux split-window`, and the same stream-json bytes that scroll in the pane flow through a named pipe (FIFO) to drain-cycle's reader thread. The reader opens the FIFO instead of a `subprocess.PIPE`; usage accounting, cost, and breach detection are byte-for-byte identical to the spawned path — there is exactly one `claude` process, and both consumers (the operator's terminal and the parser) see its raw output.
258	
259	**What this replaces.** The first cut tailed a *secondhand* view: the worker spawned `claude` normally, an internal `_WatchWriter` formatted each event into a human-readable activity log, and the pane ran `tail -f` on that file. The operator saw a filtered summary produced by drain-cycle, not the live session — and the formatter was a second place for stream-json knowledge to rot. `tee`-into-a-FIFO deletes the formatter and the intermediate file entirely (`runlog.watch_path` and `_WatchWriter` are gone): the pane shows precisely what `claude` emits.
260	
261	**FIFO startup is non-blocking with a timeout.** drain-cycle opens the read end `O_RDONLY | O_NONBLOCK` and `select`s up to ten seconds for the pane's `tee` to produce its first bytes, then clears `O_NONBLOCK` so the reader thread blocks normally until EOF. A reader-only FIFO with no writer is *not* readable in `select` until a writer connects (verified on macOS/BSD and Linux), so a pane that never started can't wedge the drain — the `select` simply times out. On timeout (or any pane/FIFO setup failure, or no `$TMUX`), the pane is torn down and the issue runs through the **normal subprocess path** unchanged. Watch is a convenience overlay; it never gates whether the cycle drains.
262	
263	**Breach kills the pane, not a process group.** On the spawned path a per-issue breach SIGKILLs the worker's process group (§9). On the watch path there is no child process to signal — `claude` belongs to the pane — so the worker calls a `kill_fn` the orchestrator wires to `tmux kill-pane`. Killing the pane terminates `claude` and its `tee`, which closes the FIFO write end and lets the reader reach EOF. The pane command ends in `; exec ${SHELL}` so the pane survives `claude`'s *normal* exit (the final issue's scrollback is preserved, AC of the pane-lifecycle: prior pane killed when the next issue starts, last one left open); `tee` still closes the FIFO on claude's exit, so EOF fires regardless of the trailing shell.
264	
265	**`exit_code` is `0` on the watch path.** The pane owns `claude`, so its real return code isn't observable from drain-cycle. The run-log entry records `exit_code=0`; the breach field and the result event's `is_error` carry the real outcome, and KR1 grading keys on `final_linear_state`, not the exit code. This is the one fidelity gap versus the spawned path, and it is cosmetic.
266	
267	## 16. The Graphite PR-stacking sequence the orchestrator will run (ABA-300 spike)
268	
269	> **Superseded by §19.** The orchestrator no longer assembles or submits the stack. The `gt`/`gh` sequence below is now run by the worker's finishing skill, not the orchestrator; the verified commands stay accurate, but the actor is the skill. See §19.
270	
271	Decided empirically by ABA-300: the full `gt` + `gh` stacking sequence was driven by hand against this repo with two stacked branches (`spike/aba-300-step-a` off `main`, `spike/aba-300-step-b` off A), producing PRs [#5](https://github.com/ababushkin/drain-cycle/pull/5) and [#6](https://github.com/ababushkin/drain-cycle/pull/6). The four findings below are what the orchestrator (Ticket 2) wires against — verified commands, not guesses.
272	
273	**(a) `gt` works from a linked worktree; cwd = the per-issue worktree root.** `gt track` and `gt submit` were run from inside `.worktrees/spike-a` and `.worktrees/spike-b` (linked worktrees created with `git worktree add`), and both succeeded. The Graphite metadata DB lives in the shared `.git` dir (`.git/.graphite_metadata.db`), so every linked worktree sees the same stack state — `gt ls` from worktree B even annotates which worktree each branch is checked out in. **The orchestrator runs `gt` from the per-issue worktree root** (§3's "fresh worktree per issue"), the same cwd the worker already uses. No need to run from the primary checkout.
274	
275	**(b) Exact command sequence.** Per branch, in its worktree, adopting the already-created branch (don't recreate):
276	
277	```
278	gt track --parent <parent>     # parent = main for the base layer; the layer below for each step up
279	# ... commits land in the worktree as normal ...
280	gt submit --stack --no-interactive --publish
281	```
282	
283	`--no-interactive` is mandatory under automation: without it `gt submit` prompts for PR fields and would hang the headless run (it prints "Running in non-interactive mode. Inline prompts … will be skipped."). `--publish` makes the PRs ready-for-review; **omit it to leave them draft** (bare `gt submit --no-interactive` creates draft PRs). `--stack` submits every layer below the current branch in one call, so submitting from the top branch creates the whole stack with correct bases (verified: #5 base `main`, #6 base `spike/aba-300-step-a`).
284	
285	**(c) The PR body comes from the commit-message body; empty body → fall back to `gh pr edit --body-file`.** `gt` populates the PR title from the commit subject and the PR **body from the commit message body** (everything after the subject's blank line) — verified: PR #5's commit carried a `## What / ## Why / ## What to review` body and it appeared **verbatim** in the PR. A commit with only a subject and no body yields an **empty** PR body (verified: PR #6 came up blank). So the orchestrator's rule: **put the What/Why/What-to-review block in the commit message body**; if a layer's body is empty or needs editing after submit, set it with `gh pr edit <n> --body-file <f>` (verified fallback). Labels are applied the same way: `gh label create review:high --color B60205` (idempotent; create-if-absent) then `gh pr edit <n> --add-label review:high`.
286	
287	**(d) Per-repo preconditions: `gt auth` + `gt init --trunk main`, both one-time and manual.** `gt auth` is an interactive browser flow and **cannot run under `--dangerously-skip-permissions`** — treat it as one-time operator setup, not an automatable step. Likewise `gt init --trunk main` is run once per repo. The orchestrator must **not** attempt either: it assumes both are already done (token in `~/.config/graphite/auth`, trunk config in `.git/.graphite_repo_config`). If `gt auth` or `gt init` is missing, `gt submit` aborts before any push — that is a **stop-the-line**: surface it for the operator, do not work around it.
288	
289	**Restack conflict policy (stop-the-line, not auto-merge).** A branch forked off an older `main` shows "needs restack"; `gt restack` rebases it. A restack that hits a **semantic conflict is a stop-the-line**: abort with `git rebase --abort` (`gt abort` refuses in non-interactive mode — use the `git` form), leave the stack on its pre-restack history, and surface the conflict for a human. Never auto-resolve and `gt restack --continue`. (This is the rule the `graphite-stack-review.md` runbook §4 was reconciled to.)
290	
291	## 17. `/shape:task` runs inside the worker session; whole-project shaping stays at design-doc scope
292	
293	> **Forward-pointer.** Not stale today, but the target moved into the pack. Under the `exec:*` namespace (ADR 0004 / Shaper `execution-workflow` design doc), `/shape:task` folds into `exec:pickup`/`exec:breakdown` at the keystone cutover ([`architecture.md`](architecture.md) §7). The in/out contract below still describes what that step does.
294	
295	The M2 worker pipeline introduces a Task Shaper role — `/shape:task` — that runs before the implementer on verify-flow tickets. The initiative doc deferred the invocation interface to this ADR: whether whole-project shaping (via `/shape:planning-and-task-breakdown`) pre-computes per-ticket task lists that workers later read, or `/shape:task` runs inside each worker session on its own ticket.
296	
297	**Decision: `/shape:task` runs inside the worker session, invoked once per ticket before the implementer begins.** The skill takes a Linear issue identifier, fetches the live issue from Linear via MCP, and produces an enriched AC checklist + sizing decision + per-stack task list. The output is fed to the implementer in-session and written to the Linear issue body. The Linear write is the durable artefact — a worker resuming a halted issue (§14) reads the existing output from the issue body rather than re-invoking the skill.
298	
299	**Why the per-ticket, in-worker path.** The alternative (pre-computation) would require the operator to run `/shape:planning-and-task-breakdown` before any drain can begin, turning the whole-project skill into a planning gate every drain must pass through. `drain-cycle`'s autonomous-drain promise is a single `drain-cycle` invocation, unattended. Fracturing that into "run planning, then drain" creates ceremony the tool exists to remove. A worker that calls `/shape:task` itself is self-contained: the same invocation path works for a cycle drain, a single-ticket re-run, or a §14 resume — no prior planning artefact required.
300	
301	**Rejected alternative: `/shape:planning-and-task-breakdown` pre-computes per-ticket task lists.** The whole-project skill runs once before the drain, writes structured per-ticket task lists somewhere (a design doc, a Linear comment, an issue body block), and workers read those artefacts at session start. The appeal is operator review of decomposition before any code runs. The costs are: (a) a mandatory pre-drain gate that breaks the single-invocation promise; (b) a machine-readable output contract that `/shape:planning-and-task-breakdown` must emit and every worker must parse — a shared format across two skills and their update paths; (c) stale-data risk when the issue body changes between planning and execution; (d) the only way to know whether the pre-computed list still applies is to re-derive it, making pre-computation an expensive cache that must be manually invalidated. The two skills stay at distinct scopes: `/shape:planning-and-task-breakdown` operates on a whole design doc; `/shape:task` operates on a single Linear issue.
302	
303	**`/shape:task`'s input/output contract, as constrained by this decision.**
304	
305	*Input:* A Linear issue identifier. The skill fetches the current issue body, title, and AC from Linear at invocation time. It does not read any prior planning artefact.
306	
307	*Output:*
308	- **Enriched AC checklist** — AC items made concrete, implicit contracts surfaced, irresolvable gaps flagged (the skill notes gaps and continues; it does not hang waiting for operator input).
309	- **Sizing decision** — `single-stack` (all work on one branch) or `N-stacks` (N specified and justified), based on whether the implementation can reach Done in a single PR stack.
310	- **Per-stack task list** — one ordered task list per stack, intended as direct context for the implementer.
311	
312	*Dual-write:* Output is (a) returned to the calling worker for in-session context and (b) appended to the Linear issue body. The Linear write is authoritative: a resumed worker reads the block from the issue body instead of re-running the skill. The skill must emit the output in a stable, delimited format that a future invocation can detect (to avoid silently double-writing).
313	
314	## 18. PR links are recorded in the run-log and posted to Linear by the orchestrator
315	
316	> **Superseded by §19.** This decision assumes the orchestrator assembles the stack, so `graphite.submit` returns the URL and the orchestrator posts the Linear comment. Under §19 the worker's finishing skill submits and writes `pr_urls` into `.drain-handoff.json`; the orchestrator *reads them back* rather than producing them. The recording intent survives — memory lives in artefacts — but the actor and the source of the URL changed.
317	
318	After a stack-mode issue is confirmed Done and its branch is assembled into the per-repo Graphite stack (§16), the orchestrator needs to close the loop: the operator and any future session must be able to find the PR without reading source or re-running `gh`. Memory lives in artefacts.
319	
320	**Decision.** The orchestrator already holds the PR's URL and number — `graphite.submit` returns them (`gh pr view` runs as the final step of assembly). On a successful submit it:
321	
322	1. Records `pr_url`, `pr_number`, `review_high` (the flag computed from the Linear label and the handoff findings, the same one that drives the GitHub `review:high` label), and `parent_branch` (the stack parent the branch was tracked under) in the run-log entry alongside the existing usage fields.
323	2. Posts a comment on the Linear issue via `linear.add_comment` (GraphQL `commentCreate`) with the PR URL and, when flagged, a `review:high` note.
324	
325	All four run-log fields are additive and default to `null` (push-to-main repos, halted issues, pre-PR run-logs). `grade.py` reads only `cycle_id`, `final_linear_state`, and `exit_code`, so pre-existing run-logs grade unchanged. The Linear comment is non-fatal: any failure is logged to stderr and the drain continues. The PR link is informational, never load-bearing for the drain's control flow.
326	
327	**Why the submit result, not a post-hoc `gh pr list` lookup.** An earlier draft of this decision had the orchestrator re-query GitHub by head branch after the worker exited — necessary in a design where the *worker* ran `gt submit`. Under §16's orchestrator-assembles design the lookup is redundant: the assembly step that creates the PR returns its URL and number in the same call, with no second query, no race against GitHub's index, and no dependency on branch-name conventions.
328	
329	**Why the orchestrator, not the agent.** The agent commits without pushing and writes the handoff file; it never talks to GitHub. The orchestrator is also the only component that can write to the run-log — it owns the `RunLog` object and calls `append_entry`.
330	
331	**Alternatives considered.**
332	
333	- *Post-hoc `gh pr list --head <branch>` lookup.* Rejected as redundant once assembly moved into the orchestrator — see above.
334	- *Always post the PR comment unconditionally (even on halt).* Rejected: a halted issue has no submitted PR (a graphite failure halts before this step). The comment fires only on confirmed Done with a successful submit.
335	
336	## 19. The worker owns PR submission via the finishing skill; the orchestrator reads `pr_urls` back
337	
338	This reverses the actor in §16 and §18. There, the orchestrator assembled and submitted the per-repo Graphite stack and posted the Linear comment. Now the **worker** does it: in drain mode the worker commits reviewable slices, then runs the finishing skill (`/shape:pr-finishing` today; `exec:finish` after the keystone cutover, [`architecture.md`](architecture.md) §7), which owns submission — it drives `gt`/`gh`, writes the submitted PR URLs into `.drain-handoff.json` (`pr_urls`), and posts the review-summary comment on the Linear issue. The orchestrator no longer assembles or submits anything; it **reads `pr_urls` back** as confirmation that submission succeeded, and a Done stack-mode issue with no `pr_urls` halts the run rather than letting the next issue stack on an unpushed branch.
339	
340	**Why the reversal.** It is the artifact boundary applied ([`architecture.md`](architecture.md) §2). Submitting a stack is "what a role does" — Layer 2 — so it belongs in a skill that runs identically by hand or unattended. Reading back whether the PRs exist is "whether an artifact exists" — Layer 1 — so it stays in the supervisor. The §16/§18 design put a Layer-2 action inside Layer 1, which is exactly the coupling the two-layer split removes: an orchestrator that knows the `gt`/`gh` sequence cannot be the thin, vendor-agnostic supervisor the keystone (§7) requires.
341	
342	**The verified `gt`/`gh` sequence in §16 is still correct** — it is just run by the finishing skill, not the orchestrator. §16's per-repo preconditions (`gt auth`, `gt init --trunk main`) and its stop-the-line restack policy carry over unchanged.
343	
344	**Completion recovery preserves the boundary.** When a worker exits leaving committed slices but the issue is not properly closed (not Done, or Done-without-`pr_urls`), the orchestrator does not run `gt`/`gh` itself — it spawns a fresh finishing sub-agent that runs the skill, then re-checks the contract, and only halts if completion still fails. A worker that left no committed slices halts as untrusted. (Tracked by the "Orchestrator-enforced completion" delivery plan.)
345	
346	**Alternatives considered.**
347	
348	- *Keep the orchestrator assembling the stack (§16/§18 as written).* Rejected: it hard-codes the PR-tooling sequence into Layer 1, blocking the keystone and the vendor-agnostic worker.
349	- *Worker pushes by hand instead of via the skill.* Rejected: the skill is the single place the submission procedure lives, so it stays identical in interactive and drain modes; a hand-rolled push in the worker prompt would be a second, drifting copy.
350	
```

> AGENT

Approved — writing the three docs now. Starting with the vision (light touch), then the architecture (the substantive update), then three decision-log entries.

> TOOL

tool_use Edit
id: toolu_01TUzZ2hV5nRtep7o1PuYUzr
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/docs/vision.md",
  "old_string": "**The supervision becomes a supervisor.** The other half is the mechanical part - kick off each step, watch it, check it produced what it should, move to the next, stop and flag anything it can't get past. That's pure mechanics, the part of me that isn't thinking. It gets automated into a supervisor - I call it the drain-cycle - that drives the skills, verifies each result, updates the record, and carries each piece of work along on its own. I'm no longer the connector between steps. I built the connector, and my job moves up a level: I point it at a project and let it run.",
  "new_string": "**The supervision becomes a supervisor.** The other half is the mechanical part - kick off each step, watch it, check it produced what it should, move to the next, stop and flag anything it can't get past. That's pure mechanics, the part of me that isn't thinking. It gets automated into a supervisor - I call it the drain-cycle - that drives the skills, verifies each result, updates the record, and carries each piece of work along on its own. I'm no longer the connector between steps. I built the connector, and my job moves up a level: I point it at a body of planned work - a cycle now, a whole project later - and let it run.\n\nAnd because the work is planned as a hierarchy - a project holds milestones, a milestone holds tasks - the connector verifies at every altitude, not just the bottom. It checks each task as it lands, then checks each milestone once its tasks are in (did the pieces cohere, did landing them break anything outside their boundary), then checks the project against the goals that can be measured by the end. Verification rolls up the same hierarchy the work was broken down along."
}
```

> TOOL

tool_result
id: toolu_01TUzZ2hV5nRtep7o1PuYUzr
```
The file /Users/anton/src/drain-cycle/docs/vision.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now the architecture doc. First generalize §1's unit, then add three new sections (appended so the stable anchors §1–§8 don't shift).

> TOOL

tool_use Edit
id: toolu_01TRaTuBBKavasU6tWzSc7EZ
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/docs/architecture.md",
  "old_string": "- **Layer 1 — supervision (`drain-cycle`).** Picks up a Linear cycle, spawns a worker per issue, holds the guardrails, halts/reverts/resumes/recovers, and records and grades the outcome. It is vendor-agnostic: the worker is a `claude -p` (or any equivalent) subprocess.",
  "new_string": "- **Layer 1 — supervision (`drain-cycle`).** Picks up a body of planned work — a Linear cycle today, a whole project later (§12) — spawns a worker per phase per issue, holds the guardrails, halts/reverts/resumes/recovers, and records and grades the outcome. It is vendor-agnostic: each worker is a `claude -p` (or any equivalent) subprocess."
}
```

> TOOL

tool_result
id: toolu_01TRaTuBBKavasU6tWzSc7EZ
```
The file /Users/anton/src/drain-cycle/docs/architecture.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01THsunBRMsyMq8At5Tzibdo
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/docs/architecture.md",
  "old_string": "## Known open seam",
  "new_string": "## 9. Phase separation: a worker per phase, not a worker per issue\n\nA worker does not run the whole `exec:*` chain. Each phase — code, review, finish — is its own spawn, with its own model tier, and the agent that produced an artifact never judges it. Two independent reasons force this:\n\n- **Independent verification.** A coder reviewing its own work rationalises its own choices. Spawning review as a separate agent that did not write the code makes review adversarial by construction, not by prompt wording.\n- **Per-phase model economics.** Review anchors to a stronger (more expensive) model regardless of what coded the change. That asymmetry is only expressible if each phase is its own spawn with its own `--model` pin — a cheap model can build while an expensive one reviews.\n\nThe three phase agents map onto the existing pack: code = `exec:build` (+`exec:debug`, `exec:simplify`), review = `exec:review`, finish = `exec:finish`. Each is a goal-shaped worker prompt, not a resident process — the goal (\"produce sliced artifacts\", \"apply every quality lens\", \"land human-readable PRs\") drives a sequence of skill delegations inside one spawn.\n\nThe cost accepted in return: every phase boundary pays a spawn plus artifact rehydration, so the handoff envelope (§2) must carry everything the next phase needs — a single worker kept that context in memory for free. This is the deliberate price of independence; see design decision §20.\n\n## 10. The resident control plane\n\nThe supervisor is moving from a one-shot CLI to a resident process — the autonomy horizon of §8 made concrete. Two scopes, both Layer 1:\n\n- **Control plane (one per machine).** The long-lived daemon. Owns process lifecycle, the queue of planned units to execute, and an API the operator queries and steers: what is running, halt this issue, resume, and (the horizon behaviour) watch open PRs through the review-and-merge loop and respond to review comments.\n- **Execution-coordinator (one per unit in flight).** Spawned by the control plane to drive a single cycle or project. It advances work by reading artifacts (§2) — never by reading inside a phase — and halts on a missing or failed artifact.\n\nThe control plane stays a **process, not a Claude skill** (design decision §22). A `/execute-cycle` skill would run inside a Claude session and collapse the artifact boundary that makes the worker vendor-agnostic; the one-command ergonomics come instead from a thin CLI front-door (`drain-cycle run <unit>`). \"Respond to PR comments\" is a control-plane behaviour, not a pack skill, because it requires watching a PR after it is open — which only a resident process does.\n\n## 11. Multi-altitude review: the dual of the delivery hierarchy\n\n`shape:delivery` decomposes committed work *downward* — project → milestones → nodes → tasks. Verification rolls *upward* along the same tree, with the review altitude matching the decomposition altitude:\n\n| Altitude | Fires when | Lenses |\n|---|---|---|\n| **Task** (per issue) | a task's diff is ready, before its PR merges | spec-compliance · security · reliability/resilience · code-quality · outcome — diff-bounded |\n| **Milestone** | a milestone's last child task lands | integration/coherence/acceptance (the task lens raised a level) · regression (did landing degrade anything outside this boundary?) |\n| **Project** | a project's last milestone lands | architecture review · measurable stated goals (partial — some goals take time and are deferred) |\n\nWork fans down; verification rolls up. The trigger is structural — a parent's review fires exactly when its last child completes — and the hierarchy itself is authoritative in Linear (milestones, projects), so the state plane (§6) reads it rather than holding a second copy.\n\nThree consequences distinguish higher-altitude review from task review:\n\n1. **The execution-coordinator is a tree walker, not a queue drainer.** It models the hierarchy, detects \"this milestone's last child landed\", and fires the milestone review.\n2. **Higher-altitude review produces new work, not reverts.** A task review can halt before a PR merges. A milestone or project review runs *after* its child PRs have merged — a merged slice cannot be cleanly reverted — so a failing review emits new remediation issues slotted back into the plan. This is a different halt semantic from task-level, and it widens the open seam below.\n3. **Project review is partial and deferred.** Some goals cannot be measured at completion. Project review measures what it can now and *schedules* the rest, which is only possible with the resident control plane (§10).\n\nTwo unknowns here are not yet decided and are shaped as spikes, not committed: the **blast-radius definition** for regression review (it is not diff-bounded like task review), and **remediation routing** (what gets created on a failing altitude review, and whether the parent pauses or its siblings keep draining). See design decision §21.\n\n## 12. The execution unit: a cycle or a project\n\nThe supervisor executes a *planned unit*. The atom is unchanged — one issue, with a worker per phase (§9) — and a cycle and a project differ only as containers with a hierarchy over them. \"Drain a cycle\" is one entry point, not the definition; project execution is out of scope today but is a later container, not a redesign (design decision §22). The tool keeps the name `drain-cycle`; the concept it serves is wider.\n\n## Known open seam"
}
```

> TOOL

tool_result
id: toolu_01THsunBRMsyMq8At5Tzibdo
```
The file /Users/anton/src/drain-cycle/docs/architecture.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now extend the open-seam note to connect to the new altitude reviews, then write the three decision entries.

> TOOL

tool_use Edit
id: toolu_0119QQ5o7vQNRChtYSZpJyEg
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/docs/architecture.md",
  "old_string": "The one undecided boundary crossing: how Layer-2 verdicts (`outcome_verdict`, `prep_verdict`) travel from a skill into the run-log. Today `handoff.py` carries only `pr_urls`. The verdict-handoff schema is a one-way door for the correctness work (the \"Multi-agent collaboration for correctness\" Layer-1 project) and should be decided before that work starts.",
  "new_string": "The one undecided boundary crossing: how Layer-2 verdicts (`outcome_verdict`, `prep_verdict`) travel from a skill into the run-log. Today `handoff.py` carries only `pr_urls`. The verdict-handoff schema is a one-way door for the correctness work (the \"Multi-agent collaboration for correctness\" Layer-1 project) and should be decided before that work starts.\n\nThe multi-altitude reviews (§11) widen this same seam: a milestone or project verdict has to cross the boundary too, and a failing one routes *remediation work* back into the plan rather than recording a pass/fail on a single diff. Whatever schema resolves the task-level verdict handoff should be designed to carry the higher-altitude verdicts as well."
}
```

> TOOL

tool_result
id: toolu_0119QQ5o7vQNRChtYSZpJyEg
```
The file /Users/anton/src/drain-cycle/docs/architecture.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now the three decision-log entries and the count bump.

> TOOL

tool_use Edit
id: toolu_01RBBfzkWpfnioDiHAbvaBTG
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/docs/design-decisions.md",
  "old_string": "Nineteen decisions are recorded so a future reader doesn't have to reverse-engineer them from the code. ADRs would be heavier than this tool needs.",
  "new_string": "Twenty-two decisions are recorded so a future reader doesn't have to reverse-engineer them from the code. ADRs would be heavier than this tool needs."
}
```

> TOOL

tool_result
id: toolu_01RBBfzkWpfnioDiHAbvaBTG
```
The file /Users/anton/src/drain-cycle/docs/design-decisions.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_0161PHLG3eGwARNSrMUeG2be
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/docs/design-decisions.md",
  "old_string": "- *Worker pushes by hand instead of via the skill.* Rejected: the skill is the single place the submission procedure lives, so it stays identical in interactive and drain modes; a hand-rolled push in the worker prompt would be a second, drifting copy.",
  "new_string": "- *Worker pushes by hand instead of via the skill.* Rejected: the skill is the single place the submission procedure lives, so it stays identical in interactive and drain modes; a hand-rolled push in the worker prompt would be a second, drifting copy.\n\n## 20. A worker per phase, not a worker per issue\n\nToday one spawned worker runs the whole `exec:*` chain for an issue — pickup through finish — in a single session. The decision is to split it: each phase (code, review, finish) is its own spawn, with its own model tier, and the agent that produced an artifact never reviews it. See [`architecture.md`](architecture.md) §9.\n\n**Why split.** Two independent reasons, either sufficient on its own:\n\n- *Independent verification.* A coder reviewing its own work rationalises its own choices — the review inherits the blind spots of the build. A separate review agent that did not write the code is adversarial by construction, not by prompt wording. This is the same logic that made `exec:review` fan out to distinct personas (the persona contract); phase separation extends it across the build/review boundary, not just within review.\n- *Per-phase model economics.* The operator anchors review to a stronger, more expensive model regardless of what built the change — a cheap model codes, an expensive one reviews. That asymmetry is only expressible if each phase is its own `claude -p` spawn with its own `--model` pin. A single worker pins one model for the whole chain.\n\n**Cost accepted.** Every phase boundary now pays a spawn plus artifact rehydration: the next phase starts cold and reads its inputs from the handoff envelope (architecture §2) rather than inheriting them in context. A single worker kept that context for free. This makes the handoff envelope load-bearing for *all* cross-phase state, not just `pr_urls` — the envelope must carry what each phase needs the next to know. This is the deliberate price of independence and the asymmetric-model economics.\n\n**Alternatives considered.**\n\n- *One worker runs the whole chain (status quo).* Rejected: it forecloses both independent review and per-phase model pinning — the coder grades itself, on the model that built the change.\n- *One worker, but review re-spawned as a sub-agent within it.* Rejected as a half-measure: it buys independent review but not independent model economics at the phase grain, and it keeps the chain's lifecycle coupled to one outer session that the control plane cannot steer phase-by-phase (§10).\n\n## 21. Review is multi-altitude; higher-altitude review yields new work, not reverts\n\nReview fires at three altitudes matching the delivery hierarchy `shape:delivery` already produces — task, milestone, project — not only per task. The full model is in [`architecture.md`](architecture.md) §11.\n\n**Why multi-altitude.** A task review is diff-bounded: it grades one issue's change against its AC and the quality lenses. It cannot see whether the tasks of a milestone *cohere*, whether landing them degraded something *outside* their own boundary, or whether the project met its stated goals. Those are real defect classes that only exist at a higher altitude, so they need a review oriented to that altitude. Verification rolls up the same tree the work was decomposed down — the dual of the delivery hierarchy.\n\n**The load-bearing consequence: higher-altitude review produces new remediation work, not reverts.** Task review can halt before a PR merges, so its verdict can block a not-yet-merged artifact. A milestone or project review runs *after* its child PRs have merged; a merged slice cannot be cleanly reverted. So a failing milestone/project review emits new Linear issues slotted back into the plan — it does not roll back landed work. This is a genuinely different halt semantic from the task-level halt/revert contract (§3, §9-guardrails) and must be modelled as such: the supervisor's tree walker reacts to a failing altitude verdict by *scheduling*, not *reverting*.\n\n**Two unknowns deferred to spikes, not decided here.**\n\n- *Regression-review blast radius.* \"Did landing this milestone degrade anything outside its boundary\" is not diff-bounded the way task review is — it needs a definition of the boundary and probably a cross-cutting test/check run. Shape it with `shape:design` before building.\n- *Remediation routing.* When an altitude review fails, what exactly is created (a new issue under the same milestone? a blocking flag on the project?), and does the supervisor pause the parent or keep draining siblings? This is the verdict-handoff open seam (architecture \"Known open seam\") widened to higher altitudes.\n\n**Alternatives considered.**\n\n- *Task review only; trust that coherent tasks compose into a coherent milestone.* Rejected: integration and regression defects are exactly the ones that survive a green per-task review, because no task-level lens is oriented to find them.\n- *Run all altitude reviews inline at project end.* Rejected: a milestone defect found only at project end is far more expensive to remediate than one caught when the milestone closed, and project-end is too late to inform the next milestone's work.\n\n## 22. The supervisor stays a process executing a planned unit; it is not a Claude skill\n\nTwo coupled decisions about the supervisor's form and scope.\n\n**Scope — a planned unit, not specifically a cycle.** The supervisor executes a *planned unit of work*: a Linear cycle today, a whole project later. The execution atom is unchanged (one issue, a worker per phase, §20); a cycle and a project differ only as containers with a hierarchy over them (§21). \"Drain a cycle\" becomes one entry point rather than the definition. Project execution is out of scope now, but it is a later container on the same machinery, not a redesign — so vision and architecture are written in the generic terms ([`architecture.md`](architecture.md) §12). The tool keeps the name `drain-cycle`.\n\n**Form — a process with a CLI front-door, not a `/execute-cycle` skill.** It is tempting to encapsulate the supervisor itself as a Claude skill (`/execute-cycle`, `/execute-project`) for one-command ergonomics. Rejected: a skill runs *inside* a Claude session, which makes the supervisor Claude-shaped and collapses the artifact boundary (§2) that lets the worker be any vendor. The supervisor's whole value is being content-blind and vendor-agnostic; a skill cannot be that. The one-command ergonomics come instead from a thin CLI front-door (`drain-cycle run <unit>`), while Layer 2 stays skills.\n\n**Why this matters now.** The resident control plane (§10) is a long-lived process with an API — that only makes sense as a process, reinforcing the form decision. A control plane implemented as a Claude skill could not be the daemon that spawns and steers vendor-agnostic workers.\n\n**Alternatives considered.**\n\n- */execute-cycle as the primary entry point.* Rejected per above — collapses the vendor-agnostic boundary.\n- *Hybrid: a `/execute-cycle` skill that shells out to the process for interactive use.* Not adopted now, but not foreclosed — it is a thin convenience wrapper over `drain-cycle run`, addable later if the keyboard ergonomics warrant it, without moving any supervision logic into the skill."
}
```

> TOOL

tool_result
id: toolu_0161PHLG3eGwARNSrMUeG2be
```
The file /Users/anton/src/drain-cycle/docs/design-decisions.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Docs are written. Let me update the north-star memory entry since the architecture evolved materially in this session.

> TOOL

tool_use Read
id: toolu_01HTAb9gYNC8pGMnCqH1K3vY
```json
{
  "file_path": "/Users/anton/.claude/projects/-Users-anton-src-drain-cycle/memory/north-star-design.md"
}
```

> TOOL

tool_result
id: toolu_01HTAb9gYNC8pGMnCqH1K3vY
```
1	---
2	name: north-star-design
3	description: "drain-cycle direction: vision.md = stable WHY (north star); architecture.md = the HOW (two-layer supervision/workflow split on the artifact boundary, dual-mode, exec:* keystone)"
4	metadata: 
5	  node_type: memory
6	  type: project
7	  originSessionId: 1e976e2b-d1ef-4117-8571-ed46c0326009
8	---
9	
10	`drain-cycle/docs/vision.md` is the **guiding vision (stable WHY / north star)** for the whole
11	drain-cycle project — every decision/project/ticket aligns to it; all analytics/reviews are grounded
12	in it. Keep it stable: when a change conflicts with it, change the vision first, deliberately.
13	The **architecture that serves it** now lives in `drain-cycle/docs/architecture.md` (the HOW —
14	numbered §; the `(§8)` autonomy-horizon anchor and `(§7)` keystone anchor live there). Wired in from
15	AGENTS.md ("read first" → vision, architecture for the how), README, and design-decisions.md.
16	
17	**Core intent:** the orchestrator (Layer 1) is the *human supervisory role, automated* — it does
18	the mechanical supervision Anton does by hand, to free him for higher-order work. Deliberate
19	trade-off: automating supervision **gives up the live feedback loop** (early intervention, rapid
20	pivot), so autonomy is applied selectively where the trade pays. **Observability is first-class** —
21	run-log/traces/grade are the delayed feedback loop that replaces live watching and drives
22	incremental improvement; better observability widens the set of work safe to hand off.
23	
24	It supersedes the architecture content in `docs/initiative-multi-agent-collaboration.md` and
25	shaper's `docs/ideas/lifecycle-expansion.md` (both now carry a pointer to it).
26	
27	Core idea — **dual-mode, two layers split on an artifact boundary**:
28	- **Layer 2 (workflow)** = the Shaper pack: `exec:pickup` sequences breakdown→build→review→verify→finish; every step is also a standalone skill. Usable by hand OR driven.
29	- **Layer 1 (supervision)** = drain-cycle: spawn/guardrails/halt/revert/resume/recover/record/grade. Content-blind; reads artifacts only (Linear state, run-log fields, `.drain-handoff.json`), never the workflow's steps.
30	- **Boundary = the artifact.** Workflow writes signals; supervisor reads them. Placement test: does it need drain-cycle to know what a role DOES (L2) or only whether an artifact EXISTS (L1)?
31	
32	Project mapping: "drain-cycle supervises; the pack owns the workflow" is the **keystone (run first)** — strips `prompt.py` to a ≤15-line pointer at `exec:pickup`. "Multi-agent collaboration for correctness" is **reframed** as the L1 enforcement/recording/grading project (keep ABA-320/321/322/328/333/334/336/332 + [[orchestrator-enforced-completion]] ABA-393; close overtaken skill-build/wiring ABA-324/326/327/330). "Drain past the merge gate" = L1 autonomy horizon.
33	
34	**Unbuilt one-way-door seam:** how Layer-2 verdicts (`outcome_verdict`, `prep_verdict`) cross into the run-log — today `handoff.py` carries only `pr_urls`. Decide the handoff/run-log schema before the correctness work. See [[stack-pr-submission-regression]].
35	
```

> TOOL

tool_use Edit
id: toolu_01UNtcnksHoTNYishoF9cF5Q
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/.claude/projects/-Users-anton-src-drain-cycle/memory/north-star-design.md",
  "old_string": "**Unbuilt one-way-door seam:** how Layer-2 verdicts (`outcome_verdict`, `prep_verdict`) cross into the run-log — today `handoff.py` carries only `pr_urls`. Decide the handoff/run-log schema before the correctness work. See [[stack-pr-submission-regression]].",
  "new_string": "**Unbuilt one-way-door seam:** how Layer-2 verdicts (`outcome_verdict`, `prep_verdict`) cross into the run-log — today `handoff.py` carries only `pr_urls`. Decide the handoff/run-log schema before the correctness work. See [[stack-pr-submission-regression]].\n\n**2026-06-15 architecture redesign (added §9–§12 + decisions §20–§22; vision generalized):**\n- **§20 worker-per-phase, not per-issue:** each phase (code/review/finish) is its own `claude -p` spawn with its own `--model`; the agent that built an artifact never reviews it. Two reasons: independent verification (no self-review) + per-phase model economics (cheap codes, expensive reviews). Cost: handoff envelope must carry ALL cross-phase state (rehydration), not just `pr_urls`.\n- **§10 resident control plane:** supervisor moving from one-shot CLI → resident daemon. Two scopes both L1: control-plane (per machine: lifecycle, queue, API steer/halt/resume, watch-PRs/respond-to-comments) + execution-coordinator (per unit in flight; tree walker). \"Respond to PR comments\" = control-plane behaviour, not a pack skill.\n- **§11/§21 multi-altitude review = dual of delivery hierarchy:** review fires at task (diff-bound) / milestone (integration+coherence+acceptance + regression) / project (architecture + measurable goals, partial/deferred). Fires when a parent's last child lands. KEY: higher-altitude review yields NEW remediation issues, not reverts (merged slices can't be reverted). Two spikes deferred: regression blast-radius def + remediation routing.\n- **§12/§22 generic unit + stays a process:** supervisor executes a \"planned unit\" (cycle now, project later — same machinery); stays a vendor-agnostic process w/ thin CLI front-door (`drain-cycle run <unit>`), NOT a `/execute-cycle` skill (would collapse the artifact boundary). Tool keeps name `drain-cycle`.\n- Review-pack gap found: `execution-review` ships spec/security/code-quality; Anton's target adds reliability/resilience persona + folds `verify-implementation` (outcome) in as a persona. Cheap L2 edit."
}
```

> TOOL

tool_result
id: toolu_01UNtcnksHoTNYishoF9cF5Q
```
The file /Users/anton/.claude/projects/-Users-anton-src-drain-cycle/memory/north-star-design.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Done. Here's what landed across the three docs:

**`vision.md`** (light) — the supervisor now points at "a body of planned work — a cycle now, a whole project later," and a new paragraph states that verification rolls up the hierarchy: task as it lands → milestone once its tasks are in → project against measurable goals.

**`architecture.md`** (substantive, anchors §1–§8 untouched) — generalized §1's unit, then appended four sections:
- **§9 Phase separation** — worker per phase, not per issue; independence + per-phase model tiers; rehydration cost accepted.
- **§10 Resident control plane** — daemon (lifecycle/queue/API/watch-PRs) + per-unit execution-coordinator; stays a process, not a skill.
- **§11 Multi-altitude review** — the dual of the delivery hierarchy, with the table, the tree-walker consequence, and *higher-altitude review yields new work, not reverts*.
- **§12 Execution unit** — cycle or project, same machinery.
- Extended the open-seam note: the milestone/project verdicts widen the verdict-handoff one-way door.

**`design-decisions.md`** — three new entries (§20 phase split, §21 multi-altitude review + remediation-not-revert, §22 process-not-skill + generic unit), each with rationale and rejected alternatives; count bumped to twenty-two.

Two things I deliberately recorded as *unknowns, not decisions* — regression-review blast radius and remediation routing — both flagged as `shape:design` spikes and tied to the existing open seam.

One concrete follow-up that fell out of the skill audit and isn't yet ticketed: the **`execution-review` persona set** needs a `reliability-resilience` persona added and `verify-implementation` folded in as the outcome persona to match your Review-It goal. That's a cheap Layer-2 edit in `agent-skills-shaper` — want me to open a Linear issue for it, or make the edit now?

Nothing is committed — the doc changes are in the working tree on `main`. Say the word if you want them committed and pushed.

> DEVELOPER

review everything you've written carefully with /writing-refinement

> TOOL

tool_use Skill
id: toolu_012fDTiSZYceVpoHh9cLNevA
```json
{
  "skill": "writing-refinement",
  "args": "review docs/vision.md, docs/architecture.md, docs/design-decisions.md changes"
}
```

> TOOL

tool_result
id: toolu_012fDTiSZYceVpoHh9cLNevA
```
Launching skill: writing-refinement
```

> AGENT

I'm in **review mode**. Let me load the standard first, then test the drafts against it.

> TOOL

tool_use Read
id: toolu_01ScdYMQEReKNXnJbLBky1Vy
```json
{
  "file_path": "/Users/anton/.claude/skills/shape-writing-refinement/references/style-rules.md"
}
```

> TOOL

tool_result
id: toolu_01ScdYMQEReKNXnJbLBky1Vy
```
1	# Style Rules (all document types)
2	
3	Apply these during Phase 4. The goal is the shortest path to the reader's mind without losing operational facts.
4	
5	## Sentence mechanics
6	
7	**Characters as subjects, actions as verbs.** Find the doer; make it the subject; make its activity a specific verb.
8	
9	| Bad | Good |
10	|---|---|
11	| "There was a failure in the deployment process due to configuration drift." | "The deploy failed because the staging config drifted from prod." |
12	| "Request dropping occurs at high utilization." | "The load balancer drops requests above 1k RPS." |
13	| "It was decided that caching should be utilized." | "We will cache session tokens in Redis." |
14	
15	**Old before new.** Start with what the reader knows; end with the new term. The end of a sentence is the stress position — the reader emphasizes whatever sits there.
16	
17	| Bad | Good |
18	|---|---|
19	| "Edge Workers, which intercept requests at the CDN layer, will reduce load time." | "To cut load time, we will intercept requests at the CDN layer using Edge Workers." |
20	
21	**Hand-product test.** Every task, goal, or milestone must imply a tangible end product the reader can visualize. "Investigate latency" fails; "a report naming the three slowest queries in /orders" passes.
22	
23	## Nominalizations — reverse them
24	
25	Abstract nouns derived from verbs freeze action. Turn them back into verbs.
26	
27	| Frozen | Active |
28	|---|---|
29	| utilization | use |
30	| implementation | implement |
31	| optimization | optimize |
32	| investigation | investigate |
33	| facilitation | help / enable |
34	| determination | decide |
35	| reduction | reduce / cut |
36	
37	## Vocabulary watchlist
38	
39	Sweep the document for these and replace:
40	
41	| Avoid | Prefer | Why |
42	|---|---|---|
43	| load-bearing / vital | essential / required | Overworked metaphor distracts from the technical reality |
44	| bottleneck | shortage / delay / hold-up | Cliché that hides the specific cause of constriction |
45	| target | objective / goal / aim | Often "attained" without being "hit" |
46	| blueprint | plan / scheme / spec | Implies a final design; usually misused for early ideas |
47	| ceiling | limit / maximum | "Raise the limit" is clearer than "raise the ceiling" |
48	| interface with | talk to | Jargon for a plain act |
49	| impact (as verb) | affect | "Impact" blunts a painful truth |
50	| leverage (as verb) | use | Same |
51	| basically / actually / quite / virtually / a bit | *(delete)* | Little qualifiers dilute authority |
52	| "at this point in time" | now | Shortest path to the mind |
53	| "in order to" | to | Same |
54	| "It should be noted that…" / "It is important to…" | *(start directly)* | Throat-clearing adds nothing |
55	| full and complete / each and every | full / each | Redundant pairs |
56	
57	## Keep the exact term; cut only the hiding metaphor
58	
59	Use the precise technical term whenever it is accurate — `mutex`, `P99`, `idempotent` earn their place. Replace a metaphor only when it hides the cause the reader needs. A figure of speech that names no mechanism leaves the reader guessing; the concrete noun states it.
60	
61	| Hides the cause | States it |
62	|---|---|
63	| "The seam lives in the orchestrator." | "The recovery points are in the orchestrator." |
64	| "The missing move is the status check." | "The orchestrator checks the status." |
65	| "This keeps reviewable work from being stranded." | "This prevents stranded branches." |
66	
67	## The pruning safety rule
68	
69	Concision serves clarity, never the reverse. Before deleting a sentence, ask: does it carry a dependency, risk, assumption, or constraint? If yes, compress it into fewer words — do not remove it. A short document that omits the rollback plan is worse than a longer one that keeps it.
70	
```

> TOOL

tool_use Read
id: toolu_011v71ncytumxuP7eFNCCrcn
```json
{
  "file_path": "/Users/anton/.claude/skills/shape-writing-refinement/references/design-docs.md"
}
```

> TOOL

tool_result
id: toolu_011v71ncytumxuP7eFNCCrcn
```
1	# Engineering Design Docs / RFCs
2	
3	This file governs **how each section reads**, not which sections exist or their order. Inside the Shaper shape:design skill (design-doc track), that skill owns the section set, the gates, and the NFR taxonomy (`references/nfr-categories.md`); this file only refines the prose within whatever structure it mandates. Used standalone, treat the sections below as the conventional shape, not a gate.
4	
5	Map the five-phase workflow onto the design-doc sections. The reader should experience a story — where we are, what broke, what we will do — never a framework.
6	
7	## Section-by-section guidance
8	
9	**## Problem**
10	Open with the stable, accepted fact (the situation), then the disturbance and its cost. The undesired current state must be concrete: a number, an incident, a failing metric. End the section with the one-sentence answer — the recommended move — so the reader holds the conclusion before the detail.
11	
12	> Bad: "Latency has been a concern for some time and various stakeholders have expressed interest in improvements."
13	> Good: "Checkout completes in 1.2s today. Since the loyalty service launched in March, P95 has climbed to 4.1s, and conversion is down 6%. We will move loyalty lookups to an async path, restoring sub-1.5s checkout."
14	
15	**## Context**
16	Anchor the reader in stable, known facts before introducing anything new. Old before new applies at the section level: architecture the reader knows first, the recent change last.
17	
18	**## Constraints / NFRs**
19	Order by degree (most binding first) or by structure (latency / cost / compliance). Each constraint gets a number where one exists.
20	
21	**## Alternatives**
22	The set of alternatives must be MECE — no two options that partially overlap, no obvious option missing. Open each alternative with its summary effect ("Buys 5x headroom at 2x infra cost"), then the detail. State why each loses to the recommendation.
23	
24	**## Recommended Approach**
25	Old before new: start from the system as it is, walk to the proposed change. The newest component lands at the ends of sentences, where the stress position emphasizes it. Headings within this section are achievements ("Route loyalty calls through the event bus"), not labels ("Architecture").
26	
27	**## Operability / Rollout Plan**
28	Every gate gets a verifiable "Done when": "Done when canary error rate holds under 0.1% for 24h", not "monitor and proceed if healthy". Rollback criteria are operational facts — never prune them.
29	
30	## Design-doc review additions
31	
32	Beyond the universal Phase 5 gate, check:
33	
34	- Does the Problem section state the cost of the status quo in numbers?
35	- Is the recommendation stated in one sentence before the detail begins?
36	- Are alternatives genuinely exclusive and exhaustive?
37	- Do rollout gates have visualizable, verifiable end states?
38	- Did assumptions, risks, and dependencies survive pruning?
39	
```

> TOOL

tool_use Read
id: toolu_017i1NwaFT5uTKzpvMqJHrMm
```json
{
  "file_path": "/Users/anton/src/drain-cycle/docs/design-decisions.md"
}
```

> TOOL

tool_result
id: toolu_017i1NwaFT5uTKzpvMqJHrMm
```
1	# Design decisions
2	
3	Design rationale for `drain-cycle`. Read this before making architectural changes — `AGENTS.md` points here.
4	
5	These decisions serve the project's guiding vision, [`docs/vision.md`](vision.md), and realize the architecture that serves it, [`docs/architecture.md`](architecture.md) — the two-layer supervisor/workflow split on an artifact boundary. Each decision below should hold the vision as its frame; a decision that no longer fits it is the signal to revisit the vision deliberately, not to drift from it silently.
6	
7	Twenty-two decisions are recorded so a future reader doesn't have to reverse-engineer them from the code. ADRs would be heavier than this tool needs.
8	
9	## 1. The spawned agent updates Linear itself
10	
11	> **Superseded-by (pending).** The "Multi-agent collaboration for correctness" Layer-1 project replaces self-asserted Done with a **verifier-gated Done** contract: a ticket reaches Done only with a recorded `outcome_verdict` (its KR2). The supervisor records the verdict; the agent no longer asserts success unobserved. Until that lands, the decision below stands.
12	
13	The orchestrator does **not** poll Linear and write status. The spawned `claude -p` session is told, in its prompt, to move its issue to Done on completion. The orchestrator only reads Linear after the session exits, to decide whether to advance or halt.
14	
15	**Alternative considered.** Orchestrator-owned status: the parent polls Linear, transitions states, owns the lifecycle. This is more conventional and easier to reason about.
16	
17	**Why the agent-self-update path.** The orchestrator can only observe *process exit*, not *task success*. A Claude session may exit 0 having done nothing useful, or exit non-zero having actually shipped — exit code is a poor proxy for "the issue is Done." Letting the agent assert Done in Linear forces it to make an explicit, observable claim about its own outcome, which is exactly the artefact we need to grade KR1 and trigger the kill condition. If this pattern proves unreliable, that's the initiative's kill condition firing — not a bug to paper over.
18	
19	## 2. `--dangerously-skip-permissions` is accepted
20	
21	Every spawned session runs with `--dangerously-skip-permissions`. The agent can run any tool on any path inside its worktree, including shell commands, file writes, and network calls, with no operator approval.
22	
23	**Blast radius.** Bounded to the per-issue worktree under `.worktrees/<issue-identifier>/` inside the target repo, plus the operator's Linear account (the agent can transition issues), plus whatever the spawned shell can reach (env vars, secrets in `~/.config`, network egress). Not bounded to the worktree at the filesystem level — a determined or confused agent can `cd` out.
24	
25	**Why accepted.** The single-operator personal-product context: target repos are mine, the Linear workspace is mine, the machine is mine. The point of the tool is removing prompts; gating them defeats the purpose. The mitigation is **scope discipline at cycle planning** — don't drain a cycle whose issues touch credentials, production systems, or shared infrastructure. This is operator responsibility, not a tool guarantee.
26	
27	## 3. Fresh worktree per issue, not a shared workspace
28	
29	Each issue gets `.worktrees/<issue-identifier>/` branched off `main`, used once, then either removed (on Done) or preserved (on halt).
30	
31	**Alternative considered.** Shared workspace where all issues run in the target repo's main checkout in sequence. Simpler, faster, no worktree plumbing.
32	
33	**Why worktree-per-issue.** Issues drift. An agent that misunderstands its task can leave the workspace in a broken state — half-applied edits, uncommitted files, branch in the wrong place — that contaminates every subsequent issue's starting point. The worktree gives each issue a clean, identical starting point regardless of what the previous one did, and preservation-on-halt (US-B) means inspectable debug state. The cost is filesystem space and a few seconds of branch setup per issue. Cheap.
34	
35	## 4. Run-log is one file per invocation, not one file per cycle
36	
37	Each `drain-cycle` invocation writes its own run-log file at `~/.drain-cycle/runs/<cycle-id>-<run-timestamp>.json`. The per-file schema is unchanged — `{cycle_id, cycle_duration_seconds, entries: [...]}` — and `cycle_id` inside each file is how downstream readers group runs of the same cycle.
38	
39	**Alternatives considered.** (A) Multi-run schema in one file: `{cycle_id, runs: [...]}`. Faithful, but every reader has to learn the new shape and the on-disk backup file needs migrating. (B) Open-and-extend: load the existing file and append to a single flat `entries` list. Loses run boundaries, and `cycle_duration_seconds` (computed as `max(finished_at) - min(started_at)`) spans the inter-run gap and becomes misleading. (D) Refuse to clobber: fail-fast if the file exists. Breaks the unattended re-run flow the tool exists for (fix X, re-run, drain the rest) until a resume mode is built.
40	
41	**Why per-run files.** The bug being fixed (ABA-230) is that a second invocation against the same cycle silently overwrites the first run's data. Per-run files make the write path single-writer-write-once — no read-then-write race, no schema diff, no migration. US-D (ABA-197), which already plans to glob `runs/*.json` and merge across cycles, gets a one-line addition (group by `cycle_id`) instead of a new shape to read. Each file's `cycle_duration_seconds` represents one invocation's hands-off time; US-D sums them when reporting cycle-level KR2.
42	
43	**Cost.** A re-run cycle accumulates one file per invocation. At cycle scale (≤ 15 issues, rarely more than 2–3 invocations to drain) this is negligible. No retention policy is shipped; trim by hand if it ever matters.
44	
45	## 5. Each issue declares its target repo via a `repo:<name>` Linear label
46	
47	The orchestrator used to be single-repo by construction: `repo = Path.cwd()`, every worktree under `<cwd>/.worktrees/`. Cycles in this workspace span multiple repos by design — `linear-workflow.md` makes "Affected repos" part of the six initiative-readiness fields, and the Ops slot deliberately holds cross-repo maintenance issues. Each issue now carries a `repo:<name>` Linear label; `~/.drain-cycle/repos.yml` maps the name to an absolute path; the operator runs `drain-cycle` from anywhere.
48	
49	**Grouped labels are supported.** The Linear workspace uses label groups (`repo`, `model`, `wave`, …). A child label in the `repo` group — e.g. the leaf `drain-cycle` under the `repo` group — is indistinguishable from a flat `repo:drain-cycle` label to `repos.resolve`. The `pending_issues` query fetches `labels { nodes { name parent { name } } }` and renders each grouped node as `"<group>:<name>"` via `_label_name`; ungrouped nodes keep their bare name (backward-compatible with any literal `repo:<name>` labels already in use). The same rendering applies to `model` group children for `model.resolve` (§7).
50	
51	**Alternatives considered.**
52	
53	- *Description-body encoding* (e.g. a `Repo: drain-cycle` line in the markdown). The description is the most-edited surface, agents rewrite it routinely, and there's no schema enforcement. A label is one structured field with one value — Linear validates it, and a label rename triggers a clear "this label doesn't exist" error rather than silently drifting to a wrong repo.
54	- *Title prefix* (e.g. `[drain-cycle] Fix the foo`). Cleaner machine parse than the body, but every issue's title gains visual clutter for a parser-only concern. Labels don't pay that cost.
55	- *Inherit from the Linear project's "affected repos"*. Ambiguous for projects that legitimately touch multiple repos, and there is no obvious answer for the Ops container project, which is multi-repo by definition.
56	
57	**Missing-repo halt behaviour.** Same machinery as every other pre-spawn halt: write a run-log entry, print the `Halt:` line to stderr, exit 1, leave subsequent issues untouched. The new wrinkle is that resolution failures happen before any Linear state is moved, so they skip the post-spawn revert path (`_revert_to_pre_halt_state`). This is the difference from the existing setup-failure halt: that one happens after `worktree.add` or the initial `linear.set_state` attempt; the resolution halt happens before either. Either way, no revert is needed because no state was moved.
58	
59	**`repos.yml` config errors are even earlier.** A missing or malformed `repos.yml` halts the CLI at startup, before any Linear traffic and before the run-log file is created. There is no cycle yet to log against, so the failure surfaces only on stderr. This is enforced eagerly in `cli.main` so the orchestrator never sees a broken config.
60	
61	**Why labels over file conventions.** (e.g. requiring the operator to put the issue identifier in a branch comment, or use a remote-name convention). Labels are the only signal that's enforceable in Linear's UI: cycle planners can see at a glance which repo an issue targets, and the multi-repo distinction is visible at the right surface (Linear) rather than buried in a config file.
62	
63	**Out-of-v1 deliberately.** No env-var expansion inside `repos.yml`; no auto-clone if the path is missing; no parallelism across repos; no retroactive labelling of pre-cycle issues. All are operator-time concerns rather than tool-time concerns. Multi-team Linear support stays out of scope too — the tool is still hardcoded to the `Personal` team.
64	
65	## 6. Installed as a `uv tool`, with the secret read from `~/.drain-cycle/.env`
66	
67	`drain-cycle` is installed via `uv tool install`, which puts the executable on `$PATH` in an isolated environment. The Linear API key is read from `~/.drain-cycle/.env` (shell-exported vars still win), beside the `repos.yml` config and the `runs/` logs the tool already kept there.
68	
69	**Alternatives considered.**
70	
71	- *`pipx`*. Functionally equivalent for installing a Python CLI in isolation. Rejected because `uv` already anchors this repo's stack (`uv.lock`, the `mise.toml` Python pin) — adding `pipx` spends an innovation token on a second tool that does the same job.
72	- *Publish to PyPI*. Lets anyone `uv tool install drain-cycle` by name, but buys a release-and-versioning burden — tagging, changelogs, a name on the index — that a single-operator tool doesn't earn. `uv tool install git+https://…` already covers install-from-anywhere with no release step.
73	
74	**The secret-loading change this forced.** The CLI used to load `.env` only from the repo root (`Path(__file__).parent.parent`). Once installed, the package lives in the isolated tool env, where that path has no `.env` — so the key has to live somewhere stable. The load order is now shell env → `~/.drain-cycle/.env` → repo-root `.env`, first hit wins (`load_dotenv` defaults to `override=False`). The repo-root entry survives only as a dev-checkout fallback (it works under `--editable`, where `__file__` still points into the checkout); the installed tool reads the key from `~/.drain-cycle/.env`.
75	
76	**Out-of-v1 deliberately.** No PyPI release. No `drain-cycle init` command to scaffold `~/.drain-cycle/` — a missing `repos.yml` already halts with an actionable message that prints the expected shape, and `docs/repos.example.yml` is a copyable template, which is enough for a single operator.
77	
78	## 7. Workers default to Sonnet; a `model:` label overrides per issue
79	
80	A spawned `claude -p` worker inherits whatever model the operator has globally pinned. In the diagnosed quota-burn run all five workers ran on `claude-opus-4-7` (the operator's global pin), and Opus was the single largest cost multiplier of the ~108M-token spend. Workers now default to `claude-sonnet-4-6`, passed explicitly via `--model`; an individual issue opts up (or down) with a `model:<alias>` Linear label, mirroring the `repo:<name>` mechanism. Known aliases (`sonnet`/`opus`/`haiku`) map to full ids; an unrecognised value is passed to `claude --model` verbatim.
81	
82	**Why lenient, not strict.** Unlike `repo:` resolution — where a missing label is a hard halt because there is no safe default target — model resolution always has a safe fallback. So it never raises: no label, an unknown alias, or conflicting `model:` labels all fall back to the default rather than halting an unattended cycle over a label typo. The model actually used is recorded in the run log, so a mis-labelled issue surfaces after the fact instead of stalling the run.
83	
84	**Grouped model labels.** A child of the Linear `model` group — e.g. the leaf `sonnet` under `model` — renders as `model:sonnet` via the same `_label_name` projection described in §5. `model.resolve` sees it identically to a flat `model:sonnet` label.
85	
86	**Alternatives considered.** (A) Keep inheriting the global pin — rejected, it is exactly what caused the burn and gives the operator no per-issue control. (B) A single global `--model` flag with no per-issue override — simpler, but a cycle legitimately mixes cheap mechanical issues with a few that warrant Opus; per-issue is the right grain. (C) Raise on ambiguous labels like `repo:` does — rejected, halting a whole unattended cycle over a duplicate label is worse than silently taking the cheap, safe default.
87	
88	## 8. Workers use stream-json output; usage is parsed from the wire and the worker leads its own process group
89	
90	The worker launches with `claude -p --verbose --output-format stream-json` via `subprocess.Popen(..., stdout=PIPE, stderr=STDOUT, text=True, bufsize=1, start_new_session=True)`, reading output line by line in a reader thread. The per-issue run-log entry gains `model`, a `usage` block (the four token components + `cumulative` + `peak_context`), `cost_usd`, `num_turns`, `session_id`, `is_error`, and an explicit `duration_seconds`; the file gains top-level `cycle_cost_usd` and `cycle_tokens_cumulative`. All of this lives in `drain_cycle/worker.py`; the orchestrator calls `worker.run_issue(...)` and records the result.
91	
92	**The problem.** A run that burned ~108M tokens left the operator with no on-disk record of *which issue* spent what — usage had to be reconstructed from `~/.claude/projects/*.jsonl`. Spend is the metric the cost guardrail (a downstream slice) acts on, so it has to be captured at the source.
93	
94	**Why parse the stream rather than the JSONL transcript.** The transcript files are keyed by session and live outside the worktree; correlating them back to an issue after the fact is exactly the manual step this removes. The event stream is emitted by the process we already spawn, in real time, and carries everything we need.
95	
96	**Token accounting — dedup by `message.id`.** The same `assistant` message is emitted *once per content block* (thinking, text, tool_use), each copy repeating the identical `message.usage`. Summing per event double-counts a turn, so usage is keyed by `message.id` and counted once. `cumulative` sums all four token components across turns — the real billed total, dominated in long tool-use loops by cache reads re-paid every turn (this is what the 108M figure was). `result.usage` is deliberately *not* used for the totals: it is only the final turn's snapshot, and it is absent entirely when a session is killed before finishing. The terminal `result` event is authoritative only for `cost_usd` (`total_cost_usd`), `num_turns`, `session_id`, `is_error`; those are `null` on a killed session.
97	
98	**Why `start_new_session=True` + `os.killpg`.** The old `subprocess.run(timeout=)` killed only the direct child on timeout, orphaning grandchildren — MCP servers, sub-agents — that kept consuming. Making the worker a process-group leader and SIGKILLing the whole group on the time cap reaps them. SIGKILL with no SIGTERM grace is deliberate: a session past its deadline has no clean-shutdown work worth waiting for, and SIGKILL is the only signal a wedged grandchild cannot ignore. Killing the group also closes the stdout pipe those grandchildren inherited, which is what lets the reader thread reach EOF instead of blocking.
99	
100	**Additive schema.** `grade.py` reads only `cycle_id` and `entries[].final_linear_state` / `exit_code`, so the new fields don't touch grading and pre-existing run logs grade unchanged. Entries written before any session runs (resolution and setup-failure halts) carry `null` for the worker fields but keep the same key set.
101	
102	- **Parallelism.** Issues run one at a time. The Linear cycle is the unit; intra-cycle parallelism adds resource contention and serialises poorly with the agent-self-update pattern (two agents racing to mark different issues Done is fine, but two agents racing on overlapping files is not).
103	- **Retry.** Superseded by §14 — a halted issue is now resumed automatically on re-run by reusing its preserved worktree, bounded by ``max_resume_attempts``. The operator-owned manual path (inspect, fix, redo, descope) still applies; the change is that the default `drain-cycle` re-run no longer fails on a leftover worktree.
104	- **Cross-cycle scheduling.** One cycle per invocation. Chaining cycles is an operator concern.
105	
106	## 9. Resource guardrails: a native cost belt and orchestrator token/time suspenders
107	
108	Before this, the only ceiling on a worker was a 3600s wall-clock timeout, and the cycle as a whole had none. A single diagnosed run burned ~108M tokens across five issues with no circuit-breaker. `drain_cycle/limits.py` now defines per-issue and cycle-wide caps on tokens, wall-clock, and cost, enforced in two layers:
109	
110	- **Native belt.** The per-issue cost cap is passed to `claude` as `--max-budget-usd`, so the session self-terminates on spend without the orchestrator watching it.
111	- **Orchestrator suspenders.** The per-issue token and time caps are enforced by the worker against the live event stream: a poll loop compares the running cumulative-token tally and elapsed wall-clock against the caps and SIGKILLs the session's process group on the first breach (reusing the group-kill machinery from decision 8). The cycle-wide caps are enforced by the orchestrator between issues — after each Done issue it sums the run log's running totals and stops the run if any cycle cap is crossed.
112	
113	**Why both layers.** The cost belt is the cheapest possible enforcement — `claude` already meters its own spend — but it only knows about *this* session's dollars, and a subscription user cares about tokens, not dollars. The token cap is therefore the primary guardrail and has to be the orchestrator's job, since `claude` exposes no `--max-tokens` equivalent for a whole session. Time is enforced the same way because a session can wedge while emitting no usage at all (the old 3600s timeout's job), so wall-clock can't be inferred from the token stream.
114	
115	**Why the cycle caps live in the orchestrator, not the worker.** A worker only sees its own issue. The failure mode the cycle caps exist for is death-by-aggregate: every issue stays comfortably under its per-issue cap while their sum drains the quota (8M × 5 = 40M, past a 30M cycle cap, with no single issue ever breaching). Only the orchestrator, which holds the run log's running totals, can see that — so it checks after each Done issue and stops before spawning the next.
116	
117	**Defaults: per-issue 8M tokens · 20 min · $15; cycle 30M tokens · 90 min · $60.** These are deliberately generous starting points sized below the diagnosed bad run (one issue alone hit 43M tokens / 23 min), not tuned values. The intent is a circuit-breaker that trips on the pathological case, not a tight budget. They are meant to be recalibrated against real run-log spend.
118	
119	**Each guardrail is independently on/off-able.** Any cap can be `None` (off). The defaults are all live; an operator turns one off with `null` in the optional `~/.drain-cycle/limits.yml`. With both the per-issue token and time caps off, the worker simply waits for the session to exit on its own — there is no longer any implicit outer timeout, which is the operator's explicit choice when they disable both.
120	
121	**The time cap absorbed the old 3600s timeout.** Rather than keep a separate hardcoded outer timeout alongside the configurable time cap, the time cap *is* the timeout — `per_issue_seconds` (default 20 min, tighter than the old 3600s and below the diagnosed 23-min overrun). One time concept, configurable, instead of two.
122	
123	**Breach reporting.** A breach is a small `Breach(scope, metric, limit, observed)` value whose `describe()` renders the operator-facing line — used verbatim by the worker (per-issue kill) and the orchestrator (cycle stop) so the wording can't drift. A per-issue breach takes the existing exit-1 + revert + `halt_reason` contract, naming the cap and the value at kill time. A cycle breach lands in the run log's top-level `cycle_halt_reason`: the breaching issue's own entry is a normal Done, and the top-level field explains why the run stopped.
124	
125	**`limits.yml` semantics and validation.** Absent key → baked-in default; explicit `null` → guardrail off; positive number → override. A present-but-malformed file (unknown key, non-positive, non-numeric, bool, invalid YAML) raises `LimitsConfigError` and halts at CLI startup — mirroring the eager `repos.yml` validation (decision 5). The reasoning is sharper here: silently falling back to defaults on a typo would leave the operator believing a tighter cap was active when it wasn't, which is worse than a loud halt.
126	
127	**Alternatives considered.**
128	
129	- *CLI flags to override limits per invocation.* Deferred. The acceptance criteria require only defaults + `limits.yml`, and `cli.main` is a deliberately minimal exact-match dispatcher (decision in `cli.py`); adding an argument parser to thread per-run overrides is scope the single operator can cover by editing `limits.yml`. Revisit if a use case for one-off overrides appears.
130	- *Kill on the cycle cap mid-stream (pass cycle-so-far totals into the worker).* Rejected as unnecessary: the per-issue cap (8M) is below the cycle cap (30M), so a single issue can't cross the cycle cap before crossing its own; checking between issues catches the aggregate case without coupling the worker to cycle state.
131	- *A separate hardcoded outer timeout kept alongside the configurable caps.* Rejected — two time concepts where one suffices (see above).
132	
133	## 10. Headless workers inherit project-scoped config by symlink
134	
135	The operator noticed entire.io's checkpointing didn't take effect during a headless drain. The hypothesis was that the worker's worktree cwd (`.worktrees/<id>`) diverges from an interactive session at the repo root. A reproduction run confirmed the divergence and sharpened the cause (below); the resolution is to symlink the repo's project-scoped config into each worktree at spawn, restoring parity.
136	
137	**What was observed (claude 2.1.150).** Running `claude -p --debug-file <path>` from the repo root vs. from a fresh `git worktree` of the same repo, then diffing the debug logs:
138	
139	| | Repo root | Worktree |
140	|---|---|---|
141	| Settings files watched | user `~/.claude/settings.json` + **project** `.claude/settings.json` + `.claude/settings.local.json` | **user only** |
142	| Project `.claude/settings.json` | loaded | "Broken symlink or missing file encountered" |
143	| entire.io hooks | SessionStart + SessionEnd fire ("Entire CLI will link this conversation to your next commit") | **absent — zero references** |
144	| User-scoped plugins (crit, hookify, agent-skills, security-guidance) | "Registered 7 hooks from 15 plugins" | **identical: "Registered 7 hooks from 15 plugins"** |
145	
146	**The cause is project-scoped registration in a gitignored file — not cwd alone, and not plugins generally.** entire registers its hooks in the project-scoped `.claude/settings.json`. That file is gitignored (`.gitignore` ends with `.claude`). A `git worktree` is a fresh checkout of *tracked* files only, and git reports the worktree directory as its own `--show-toplevel`, so Claude Code resolves the project root to the worktree and finds no `.claude/` there. User-scoped plugins and MCP servers — registered under `~/.claude/` — are cwd-independent and load identically in both, which is why the symptom looked like "some plugins" rather than "all hooks": only the project-scoped ones drop out. The original hypothesis (worktree cwd) was right that cwd is involved, but the operative mechanism is the gitignored project-settings file, not cwd by itself; were `.claude/settings.json` tracked, the worktree checkout would carry it.
147	
148	**Reproduction step (one-shot).** From a target repo with project-scoped hooks registered in `.claude/settings.json`:
149	
150	```bash
151	# Repo root — interactive-equivalent project root
152	claude -p --debug-file /tmp/root.debug.log --model claude-sonnet-4-6 \
153	  --max-budget-usd 0.50 "Reply with exactly: ok"
154	
155	# Fresh worktree — the worker's actual cwd
156	git worktree add -b repro .worktrees/repro main
157	( cd .worktrees/repro && claude -p --debug-file /tmp/worktree.debug.log \
158	    --model claude-sonnet-4-6 --max-budget-usd 0.50 "Reply with exactly: ok" )
159	git worktree remove --force .worktrees/repro && git branch -D repro
160	
161	# Diff the loaded settings/hooks. The worktree run is missing the project
162	# settings file and any hook registered in it.
163	grep -iE 'settings.json|Registered .* hooks|<your-plugin-name>' /tmp/root.debug.log
164	grep -iE 'settings.json|Registered .* hooks|<your-plugin-name>' /tmp/worktree.debug.log
165	```
166	
167	The same capture is wired into the worker as an opt-in: `DRAIN_CYCLE_DEBUG=1 drain-cycle` passes `--debug-file` to every spawned session, landing one `<run-log-stem>-<issue>.debug.log` per issue beside the run log in `~/.drain-cycle/runs/`. It is off by default — the diagnostic is for one-shot investigation, not steady-state overhead, and debug output goes to the file rather than stderr so the usage parser's stream is unaffected.
168	
169	**Decision — symlink a configurable set of project config into each worktree.** The earlier hesitation was upstream of the mechanism: it wasn't obvious headless checkpointing was even *wanted*, since a `drain-cycle` worktree is a throwaway branch. That resolved in favour of wanting it — the checkpoint links a session to the commit it produces, and that commit is pushed to `main` before the worktree is removed, so the link outlives the branch. The operator wants the same project tooling headless as interactively.
170	
171	After `worktree.add`, the orchestrator calls `worktree.link_project_config`, which symlinks the repo's real project-config entries into the new worktree. Because each link points at the live dir, the worker reads *and writes* the repo's actual config exactly as a non-worktree run does — so a stateful hook like entire's checkpointing works and persists. Teardown needs no special handling: `git worktree remove` deletes the worktree directory and its symlinks but not the link targets, so the repo's real `.claude/` and `.entire/` survive.
172	
173	This depends on a precondition: every configured path must be gitignored in the target repo. The defaults (`.claude`, `.mcp.json`) and `.entire` are gitignored in a typical repo, so the symlink is invisible to git in the worktree (it shares the repo's tracked `.gitignore`) and the worker's `git add` never stages it. A non-ignored, untracked entry would be the opposite: the worker would stage the symlink into the commit it pushes, and `git worktree remove` would then refuse the dirty worktree. The link step doesn't enforce this — it skips a name only when it's absent in the repo or already present in the worktree — so the requirement is documented (`repos.yml` comment, README) rather than coded. The link step is also not transactional: if `os.symlink` fails partway through the set, the already-created links remain and the failure surfaces as a pre-spawn "setup failed" halt, leaving the worktree in place for inspection.
174	
175	The linked set is configurable. It defaults to `[.claude, .mcp.json]` — sensible for any repo — and is overridden by an optional `worktree_config_paths` list in `repos.yml`. `.entire` is not a default, because not every repo uses entire.io; an operator who does adds it there. Entries must be relative paths without `..`, since they are resolved inside the repo and linked into the worktree.
176	
177	Symlink beat the alternatives. Passing `--settings <repo>/.claude/settings.json` loads only one file and leaves four other surfaces broken: `settings.local.json`, project agents/skills/commands, hook scripts whose paths are relative to `$CLAUDE_PROJECT_DIR`, and `.mcp.json`. Copying the config (rather than linking) isolates the worker but discards entire's checkpoint writes when the worktree is removed. Tracking `.claude/` in git would commit machine-specific config. The accepted tradeoff: a worker runs `--dangerously-skip-permissions`, so it shares — and could mutate — the live config dirs, exactly as a non-worktree run would (decision 2).
178	
179	## 11. Active-run marker lives above `runs/` as `~/.drain-cycle/active.json`
180	
181	Without a live-run signal there is no way to distinguish a working run from a hung one: the run-log gains an entry only on issue completion, and the orchestrator emits only sparse stderr lines. The fix is an active-run marker — a small JSON file written before each spawn and removed in the worker's try/finally — that a second terminal can read with `drain-cycle status`.
182	
183	**Why `~/.drain-cycle/active.json`, not inside `runs/`.** The `grade` command globs `runs/*.json` and groups files by `cycle_id`. A marker placed in `runs/` would either corrupt a grading run (if it looks like a run log) or require `grade` to skip it by sentinel field (fragile coupling). Placing the marker at `~/.drain-cycle/active.json` — one level above `runs/` — means `grade`'s glob never sees it and the two concerns share no code path.
184	
185	**Why not `runs/active.json`.** Same issue: inside `runs/` it's in the glob's scope. A separate directory (`~/.drain-cycle/live/`) was considered but adds a layer without benefit; a single well-named file at the parent level is enough.
186	
187	**Why atomic write (temp-file rename).** `drain-cycle status` reads the marker from a different process, potentially mid-write. `Path.write_text` is not atomic: the file is truncated before the new content is written, so a reader arriving between those two steps sees an empty file. Rename is atomic on POSIX filesystems: the reader sees either the old complete content or the new complete content, never a partial write. The temp file uses a `.tmp` extension adjacent to the marker (`active.json.tmp → active.json`), not a different directory, so the rename is always within the same filesystem mount.
188	
189	**Why the progress block is updated on every new turn, not on every raw JSON line.** The worker's stream-json output emits one event per content block per turn (thinking, text, tool_use) — a single turn with a thinking + tool_use block produces two events carrying the identical usage. Firing the callback on every raw event would write the file multiple times per turn with the same data, wasting I/O and producing redundant stderr lines. The reader thread deduplicates by message id: the callback fires once per unique message id, which is once per turn. The first event in a turn records the turn; subsequent events with the same id are no-ops for the callback.
190	
191	**Stale marker detection.** A crash or SIGKILL leaves the marker on disk (the try/finally doesn't run on SIGKILL). `drain-cycle status` checks `os.kill(pid, 0)` — if the pid is gone it reports a stale marker rather than a live run. It does not delete the marker automatically; the operator removes it with `rm`, preserving forensic evidence of the interrupted run.
192	
193	## 12. Execution order: manual drag-order only, blocks-aware
194	
195	Before this change the orchestrator ordered issues by `(priority, sortOrder)` and ignored blocks/blocked-by entirely. Priority overrode the operator's manual drag-order, and a blocked issue could run before its blocker — wasting a worker on work that couldn't succeed.
196	
197	**Decision.** Order purely by manual `sortOrder` ascending; drop `priority` from sorting. Overlay a topological pass (Kahn's algorithm) using `(sortOrder, id)` as the tiebreak among ready issues: each issue is "ready" once all its intra-drain blockers have been scheduled. This preserves the operator's intended drag-order as far as dependencies allow.
198	
199	**External unresolved blocker → defer.** If a pending issue is blocked by an issue not in this drain's runnable set — including an In Progress issue in the same cycle, which the drain won't complete — the blocked issue is deferred: left Todo, not spawned, logged to stderr. Deferral cascades: if X is deferred and X intra-drain-blocks Y, Y defers too (falls out naturally from Kahn, since Y's in-degree never reaches zero while X is treated as permanently deferred). The exclusion rule is "defer unless the blocker is `completed` or `canceled`" — so `started`/`unstarted`/`backlog`/`triage` external blockers all defer. Deferred issues are not run-logged: they were never attempted, and counting them in `done/attempted` would corrupt `grade`'s completion signal.
200	
201	**Intra-drain cycle → halt.** If the blocks graph among the pending issues contains a cycle (self-loop included), `DependencyCycleError` is raised, the orchestrator sets `cycle_halt_reason`, prints a `Halt:` line naming the involved issues, and exits 1. Nothing runs.
202	
203	**`pending_issues` return type changed from `list[dict]` to `ExecutionPlan`.** The pure function `_plan(issues) -> ExecutionPlan` replaces `_sort_pending_issues`. `ExecutionPlan` is a frozen dataclass carrying `order: list[dict]` (runnable issues, topo-sorted) and `deferred: list[dict]` (each entry has `issue`, `blocker_identifier`, `blocker_state_type`). `DependencyCycleError(RuntimeError)` carries `identifiers: list[str]` for the cycle report. The `inverseRelations` GraphQL field is fetched in `pending_issues`, flattened to `issue["blockers"] = [{id, identifier, state_type}]`, and the raw key dropped — wire shape stays local to `pending_issues`, like `labels`.
204	
205	**All-deferred → exit 0.** If `plan.order` is empty but `plan.deferred` is not, the run emits the stderr deferral lines and returns 0: the cycle isn't broken, it's just blocked externally. An empty `plan.order` with an empty `plan.deferred` is also exit 0 ("nothing to do").
206	
207	**Alternatives considered.**
208	
209	- *Keep priority in the sort key.* Rejected: the operator has one predictable knob — the manual drag-order — and priority overriding it is surprising and undesirable.
210	- *Ignore blocks entirely.* Rejected: running a blocked issue wastes a worker on work that can't succeed by definition.
211	- *Best-effort run instead of defer/halt.* Rejected: silently violating a dependency the operator encoded is worse than a loud skip or stop.
212	- *Record deferrals in the run log.* Rejected: a deferred issue was never attempted; counting it as an entry corrupts `done/attempted` in `grade`.
213	
214	## 13. Opt-in OpenTelemetry tracing to Honeycomb
215	
216	A drain runs unattended and can take hours, spending real tokens across many spawned sessions. The run log records the outcome per issue, but it is one flat file per invocation — it can't show where time went inside a drain, how the Linear round-trips and worker sessions nest, or let an operator aggregate cost across drains. Tracing fills that gap.
217	
218	**Decision.** Each invocation emits one trace: a `drain.cycle` root span, a `drain.issue` span per attempted issue, and under those the `drain.worker.session`, `drain.worktree.add`/`.remove`, and per-operation `linear.*` spans. The `httpx` transport is auto-instrumented, so every Linear GraphQL POST appears as a child of its `linear.*` span. Worker token/cost/turn usage, the issue's repo/model/final-state, and the cycle outcome ride as span attributes; every halt site is tagged with a static `exception.slug` (greppable, low-cardinality, safe to `GROUP BY`). `service.name` is `drain-cycle`, which is also the Honeycomb dataset.
219	
220	**Opt-in via `HONEYCOMB_API_KEY`.** The key's presence in the environment is the on/off switch. Absent, `telemetry.setup()` is a no-op and the default no-op tracer stays installed — a drain with no telemetry configured behaves exactly as before, takes no new network dependency at runtime, and the `start_as_current_span` calls scattered through the code cost nothing. The OTel packages are unconditional install-time dependencies (lightweight, pure-Python); only *exporting* is gated.
221	
222	**Flush-on-exit is load-bearing.** `drain-cycle` is a short-lived CLI that exits through `sys.exit`. A `BatchSpanProcessor` buffers spans and exports on a timer, so without an explicit flush the queued spans die with the interpreter and the last issues of a drain never ship. `setup()` registers `shutdown()` (which flushes the processor) with `atexit`; `SystemExit` still runs `atexit` handlers, so every exit path drains the queue.
223	
224	**Alternatives considered.**
225	
226	- *`opentelemetry-instrument` zero-code agent.* Rejected: it wraps a `python` invocation, but the tool ships as a `uv tool` console-script entry point (`drain-cycle`), so there is no `python app.py` to wrap. Programmatic setup in `telemetry.setup()` is reliable regardless of how the entry point is launched.
227	- *Always-on tracing.* Rejected: it would force an exporter and an egress dependency on an operator who hasn't asked for it, and fail noisily (or silently retry) when Honeycomb is unreachable. Opt-in keeps the default path dependency-free.
228	- *Metrics and logs alongside traces.* Out of scope. The run log already covers durable per-issue accounting; traces add the causal/nesting view. A metrics layer can be added later if cost-rate alerting is wanted (see the otel-instrumentation layering guidance).
229	- *A span per private helper (e.g. `_plan`, `link_project_config`).* Rejected as over-instrumentation: those are fast, pure, and not independently aggregable. Interesting, failure-prone, or aggregable operations get spans; the rest stay as attributes on their parent.
230	
231	## 14. Halted issues resume on re-run by reusing the preserved worktree
232	
233	Before this, a halted issue's worktree was preserved on disk for the operator to inspect, but a re-run of `drain-cycle` against the same cycle would call `git worktree add` on the same path and fail opaquely — every halt required a manual `rm -rf .worktrees/<id>` plus `git worktree prune` plus `git branch -D <id>` before the next run could even reach the spawn. That friction punished the exact workflow the tool exists for: "halt, inspect, re-run, drain the rest."
234	
235	**Decision.** `worktree.ensure` replaces `worktree.add` in the orchestrator's pre-spawn path: if a worktree is already registered at `repo/.worktrees/<identifier>`, it is reused as-is (no mutating git command runs, so a dirty index, staged or untracked files, and the gitignored config symlinks all survive untouched); otherwise it falls through to `add` exactly as before. The handle returned carries a `resumed: bool` flag that the orchestrator threads into `prompt.build(..., resumed=…)`. When true, the spawned prompt prepends a "Resuming issue …" directive that tells the agent to run `git log --oneline main..HEAD` and `git status` first to read what is already done before continuing — so the agent does not restart from scratch and clobber the prior work.
236	
237	**Bounded by `limits.max_resume_attempts`.** A perma-stuck issue would otherwise consume an attempt on every re-run forever. The orchestrator counts prior halted attempts for the issue across the cycle's run-log files (entries with a non-Done `final_linear_state` matching the identifier) and refuses to spawn once that count *exceeds* the cap. The refusal is a no-spawn halt: no Linear `set_state`, no worktree manipulation, no worker invocation; a halt entry is still written so KR1 grading sees the refused attempt and the halt line names the cap so the operator knows how to clear it (raise the cap, clear prior runs, or finish by hand). The semantic follows the stdlib `urllib3` / `requests` convention for `max_retries`: `max_resume_attempts=N` allows up to N resumes *after* the initial attempt, for `N+1` total halts before refusal. The default is 3 (one fresh attempt + three resumes = four total halts before the fifth would be refused); `null` removes the cap entirely. `max_resume_attempts` is a *policy* cap, not a runtime guardrail in the §9 sense — no `Breach` is raised, the check is purely pre-spawn against the run-log history, and the field validation is integer-only (`1.5` would be incoherent on a count).
238	
239	**Why the cap-halt fires before `worktree.ensure` and `set_state`.** The point of refusing is to leave the issue exactly where it was so the operator can intervene without untangling a half-done re-run. Calling `worktree.ensure` first would be harmless (`ensure` is read-only on the worktree-already-registered branch), but `set_state(In Progress)` would not — a refused attempt that nevertheless flipped Linear to In Progress would silently exclude the issue from the next `pending_issues` query and the cycle would stall invisibly. The order is: resolve repo → resume-cap check → `worktree.ensure` → `link_project_config` → `set_state` → spawn. Each step is a pure no-op until the one before it succeeds.
240	
241	**Why "resumed" is a prompt directive, not a worker flag.** The worker is just a `claude -p` subprocess; the only contract surface between orchestrator and agent is the prompt string. Adding a CLI flag for "resumed" to the worker would still resolve to "include this paragraph in the system context," and the prompt is already that context. The four-segment ordering in `prompt.py` (title → body → preamble → tail) is load-bearing; the resume directive inserts as the first line of the preamble (after the `---` separator, before "Execution instructions:") so the agent reads it ahead of the procedure while `_TAIL` keeps the last-line position the ordering reserves for it.
242	
243	**Run-log entries treat resume halts the same as first-attempt halts.** A halt entry written on a resumed run has identical shape to one from a fresh attempt — same `final_linear_state`, same `worktree_path`, same `halt_reason` template via `_halt_message`. This is deliberate: KR1 grading and the cap-counting helper both read `final_linear_state` per entry, and giving resumed halts a different shape would split the schema into two cases for no benefit. The cap-halt entry uses `exit_code=-1` (the no-spawn sentinel, like the resolution and setup-failure halts in §8/§5) and carries the cap-specific message in `halt_reason` so the operator can grep for it.
244	
245	**This supersedes the `rerun-after-halt-detect-cleanly` plan (`docs/tasks/`).** That earlier doc proposed a `PriorArtefactsExist` exception that would convert the leftover worktree into a clean `Halt:` line — same friction, prettier error. The resume path eliminates the friction entirely: the operator's mental model is "re-run drains the rest," and `drain-cycle` now matches it. The task doc carries a supersession note pointing here.
246	
247	**Alternatives considered.**
248	
249	- *Auto-delete the preserved worktree on re-run.* Rejected. The worktree exists because §3 chose preservation-on-halt for inspectability (US-B). Deleting it on re-run means the operator's evidence is gone the moment they re-run, which is the worst-of-both: they cannot inspect (deleted) but also cannot resume (fresh worktree, no prior work). Preservation + resume is the only combination that lets the operator both inspect *and* re-run.
250	- *Refuse to re-run while a halted worktree exists, force `drain-cycle clean <id>` first.* Rejected as scope creep — a new subcommand plus a new gating rule, both to enforce the workflow `drain-cycle` already trains. The mental model "halt, inspect, re-run" is the one operators have; a forced clean step adds friction without adding safety (the operator could already have re-run after deletion in the old model).
251	- *Resume by replaying the agent's last few turns from the worker stream-json log.* Rejected. The transcript is keyed by session and lives outside the worktree (§8); reconstructing context from it duplicates what `git log main..HEAD` and `git status` already tell the agent at the start of a resume. Two sources of truth where one suffices.
252	- *Resume by passing `--continue` or `--resume <session-id>` to `claude -p` instead of changing the prompt.* Rejected because a halted worker may have died mid-turn with no clean session boundary; the next worker is a fresh `claude -p` against a worktree that already has commits. The prompt directive is the right level of abstraction: "this worktree carries prior committed work; read it before continuing." The mechanism is the same whether the prior session lived for one turn or one hour.
253	- *Cap-halt resets when the operator manually marks the issue Done in Linear.* Considered — the cap counts non-Done entries, so a manual Done in Linear does NOT directly reset the cap, because the prior halted entries in the run log still carry their non-Done `final_linear_state`. The operator clears the cap by raising it, deleting the relevant run-log files, or simply not re-running. This is fine: the cap exists to prevent infinite resume loops, not to track Linear state — Linear state can flip independently of the on-disk history.
254	
255	## 15. `--watch` runs claude *in* the tmux pane, not a formatter tailing a log
256	
257	In `--watch` mode the operator wants to see the agent working in real time. The pane therefore **is** the `claude` session: the orchestrator runs `claude … | tee <fifo>` in a `tmux split-window`, and the same stream-json bytes that scroll in the pane flow through a named pipe (FIFO) to drain-cycle's reader thread. The reader opens the FIFO instead of a `subprocess.PIPE`; usage accounting, cost, and breach detection are byte-for-byte identical to the spawned path — there is exactly one `claude` process, and both consumers (the operator's terminal and the parser) see its raw output.
258	
259	**What this replaces.** The first cut tailed a *secondhand* view: the worker spawned `claude` normally, an internal `_WatchWriter` formatted each event into a human-readable activity log, and the pane ran `tail -f` on that file. The operator saw a filtered summary produced by drain-cycle, not the live session — and the formatter was a second place for stream-json knowledge to rot. `tee`-into-a-FIFO deletes the formatter and the intermediate file entirely (`runlog.watch_path` and `_WatchWriter` are gone): the pane shows precisely what `claude` emits.
260	
261	**FIFO startup is non-blocking with a timeout.** drain-cycle opens the read end `O_RDONLY | O_NONBLOCK` and `select`s up to ten seconds for the pane's `tee` to produce its first bytes, then clears `O_NONBLOCK` so the reader thread blocks normally until EOF. A reader-only FIFO with no writer is *not* readable in `select` until a writer connects (verified on macOS/BSD and Linux), so a pane that never started can't wedge the drain — the `select` simply times out. On timeout (or any pane/FIFO setup failure, or no `$TMUX`), the pane is torn down and the issue runs through the **normal subprocess path** unchanged. Watch is a convenience overlay; it never gates whether the cycle drains.
262	
263	**Breach kills the pane, not a process group.** On the spawned path a per-issue breach SIGKILLs the worker's process group (§9). On the watch path there is no child process to signal — `claude` belongs to the pane — so the worker calls a `kill_fn` the orchestrator wires to `tmux kill-pane`. Killing the pane terminates `claude` and its `tee`, which closes the FIFO write end and lets the reader reach EOF. The pane command ends in `; exec ${SHELL}` so the pane survives `claude`'s *normal* exit (the final issue's scrollback is preserved, AC of the pane-lifecycle: prior pane killed when the next issue starts, last one left open); `tee` still closes the FIFO on claude's exit, so EOF fires regardless of the trailing shell.
264	
265	**`exit_code` is `0` on the watch path.** The pane owns `claude`, so its real return code isn't observable from drain-cycle. The run-log entry records `exit_code=0`; the breach field and the result event's `is_error` carry the real outcome, and KR1 grading keys on `final_linear_state`, not the exit code. This is the one fidelity gap versus the spawned path, and it is cosmetic.
266	
267	## 16. The Graphite PR-stacking sequence the orchestrator will run (ABA-300 spike)
268	
269	> **Superseded by §19.** The orchestrator no longer assembles or submits the stack. The `gt`/`gh` sequence below is now run by the worker's finishing skill, not the orchestrator; the verified commands stay accurate, but the actor is the skill. See §19.
270	
271	Decided empirically by ABA-300: the full `gt` + `gh` stacking sequence was driven by hand against this repo with two stacked branches (`spike/aba-300-step-a` off `main`, `spike/aba-300-step-b` off A), producing PRs [#5](https://github.com/ababushkin/drain-cycle/pull/5) and [#6](https://github.com/ababushkin/drain-cycle/pull/6). The four findings below are what the orchestrator (Ticket 2) wires against — verified commands, not guesses.
272	
273	**(a) `gt` works from a linked worktree; cwd = the per-issue worktree root.** `gt track` and `gt submit` were run from inside `.worktrees/spike-a` and `.worktrees/spike-b` (linked worktrees created with `git worktree add`), and both succeeded. The Graphite metadata DB lives in the shared `.git` dir (`.git/.graphite_metadata.db`), so every linked worktree sees the same stack state — `gt ls` from worktree B even annotates which worktree each branch is checked out in. **The orchestrator runs `gt` from the per-issue worktree root** (§3's "fresh worktree per issue"), the same cwd the worker already uses. No need to run from the primary checkout.
274	
275	**(b) Exact command sequence.** Per branch, in its worktree, adopting the already-created branch (don't recreate):
276	
277	```
278	gt track --parent <parent>     # parent = main for the base layer; the layer below for each step up
279	# ... commits land in the worktree as normal ...
280	gt submit --stack --no-interactive --publish
281	```
282	
283	`--no-interactive` is mandatory under automation: without it `gt submit` prompts for PR fields and would hang the headless run (it prints "Running in non-interactive mode. Inline prompts … will be skipped."). `--publish` makes the PRs ready-for-review; **omit it to leave them draft** (bare `gt submit --no-interactive` creates draft PRs). `--stack` submits every layer below the current branch in one call, so submitting from the top branch creates the whole stack with correct bases (verified: #5 base `main`, #6 base `spike/aba-300-step-a`).
284	
285	**(c) The PR body comes from the commit-message body; empty body → fall back to `gh pr edit --body-file`.** `gt` populates the PR title from the commit subject and the PR **body from the commit message body** (everything after the subject's blank line) — verified: PR #5's commit carried a `## What / ## Why / ## What to review` body and it appeared **verbatim** in the PR. A commit with only a subject and no body yields an **empty** PR body (verified: PR #6 came up blank). So the orchestrator's rule: **put the What/Why/What-to-review block in the commit message body**; if a layer's body is empty or needs editing after submit, set it with `gh pr edit <n> --body-file <f>` (verified fallback). Labels are applied the same way: `gh label create review:high --color B60205` (idempotent; create-if-absent) then `gh pr edit <n> --add-label review:high`.
286	
287	**(d) Per-repo preconditions: `gt auth` + `gt init --trunk main`, both one-time and manual.** `gt auth` is an interactive browser flow and **cannot run under `--dangerously-skip-permissions`** — treat it as one-time operator setup, not an automatable step. Likewise `gt init --trunk main` is run once per repo. The orchestrator must **not** attempt either: it assumes both are already done (token in `~/.config/graphite/auth`, trunk config in `.git/.graphite_repo_config`). If `gt auth` or `gt init` is missing, `gt submit` aborts before any push — that is a **stop-the-line**: surface it for the operator, do not work around it.
288	
289	**Restack conflict policy (stop-the-line, not auto-merge).** A branch forked off an older `main` shows "needs restack"; `gt restack` rebases it. A restack that hits a **semantic conflict is a stop-the-line**: abort with `git rebase --abort` (`gt abort` refuses in non-interactive mode — use the `git` form), leave the stack on its pre-restack history, and surface the conflict for a human. Never auto-resolve and `gt restack --continue`. (This is the rule the `graphite-stack-review.md` runbook §4 was reconciled to.)
290	
291	## 17. `/shape:task` runs inside the worker session; whole-project shaping stays at design-doc scope
292	
293	> **Forward-pointer.** Not stale today, but the target moved into the pack. Under the `exec:*` namespace (ADR 0004 / Shaper `execution-workflow` design doc), `/shape:task` folds into `exec:pickup`/`exec:breakdown` at the keystone cutover ([`architecture.md`](architecture.md) §7). The in/out contract below still describes what that step does.
294	
295	The M2 worker pipeline introduces a Task Shaper role — `/shape:task` — that runs before the implementer on verify-flow tickets. The initiative doc deferred the invocation interface to this ADR: whether whole-project shaping (via `/shape:planning-and-task-breakdown`) pre-computes per-ticket task lists that workers later read, or `/shape:task` runs inside each worker session on its own ticket.
296	
297	**Decision: `/shape:task` runs inside the worker session, invoked once per ticket before the implementer begins.** The skill takes a Linear issue identifier, fetches the live issue from Linear via MCP, and produces an enriched AC checklist + sizing decision + per-stack task list. The output is fed to the implementer in-session and written to the Linear issue body. The Linear write is the durable artefact — a worker resuming a halted issue (§14) reads the existing output from the issue body rather than re-invoking the skill.
298	
299	**Why the per-ticket, in-worker path.** The alternative (pre-computation) would require the operator to run `/shape:planning-and-task-breakdown` before any drain can begin, turning the whole-project skill into a planning gate every drain must pass through. `drain-cycle`'s autonomous-drain promise is a single `drain-cycle` invocation, unattended. Fracturing that into "run planning, then drain" creates ceremony the tool exists to remove. A worker that calls `/shape:task` itself is self-contained: the same invocation path works for a cycle drain, a single-ticket re-run, or a §14 resume — no prior planning artefact required.
300	
301	**Rejected alternative: `/shape:planning-and-task-breakdown` pre-computes per-ticket task lists.** The whole-project skill runs once before the drain, writes structured per-ticket task lists somewhere (a design doc, a Linear comment, an issue body block), and workers read those artefacts at session start. The appeal is operator review of decomposition before any code runs. The costs are: (a) a mandatory pre-drain gate that breaks the single-invocation promise; (b) a machine-readable output contract that `/shape:planning-and-task-breakdown` must emit and every worker must parse — a shared format across two skills and their update paths; (c) stale-data risk when the issue body changes between planning and execution; (d) the only way to know whether the pre-computed list still applies is to re-derive it, making pre-computation an expensive cache that must be manually invalidated. The two skills stay at distinct scopes: `/shape:planning-and-task-breakdown` operates on a whole design doc; `/shape:task` operates on a single Linear issue.
302	
303	**`/shape:task`'s input/output contract, as constrained by this decision.**
304	
305	*Input:* A Linear issue identifier. The skill fetches the current issue body, title, and AC from Linear at invocation time. It does not read any prior planning artefact.
306	
307	*Output:*
308	- **Enriched AC checklist** — AC items made concrete, implicit contracts surfaced, irresolvable gaps flagged (the skill notes gaps and continues; it does not hang waiting for operator input).
309	- **Sizing decision** — `single-stack` (all work on one branch) or `N-stacks` (N specified and justified), based on whether the implementation can reach Done in a single PR stack.
310	- **Per-stack task list** — one ordered task list per stack, intended as direct context for the implementer.
311	
312	*Dual-write:* Output is (a) returned to the calling worker for in-session context and (b) appended to the Linear issue body. The Linear write is authoritative: a resumed worker reads the block from the issue body instead of re-running the skill. The skill must emit the output in a stable, delimited format that a future invocation can detect (to avoid silently double-writing).
313	
314	## 18. PR links are recorded in the run-log and posted to Linear by the orchestrator
315	
316	> **Superseded by §19.** This decision assumes the orchestrator assembles the stack, so `graphite.submit` returns the URL and the orchestrator posts the Linear comment. Under §19 the worker's finishing skill submits and writes `pr_urls` into `.drain-handoff.json`; the orchestrator *reads them back* rather than producing them. The recording intent survives — memory lives in artefacts — but the actor and the source of the URL changed.
317	
318	After a stack-mode issue is confirmed Done and its branch is assembled into the per-repo Graphite stack (§16), the orchestrator needs to close the loop: the operator and any future session must be able to find the PR without reading source or re-running `gh`. Memory lives in artefacts.
319	
320	**Decision.** The orchestrator already holds the PR's URL and number — `graphite.submit` returns them (`gh pr view` runs as the final step of assembly). On a successful submit it:
321	
322	1. Records `pr_url`, `pr_number`, `review_high` (the flag computed from the Linear label and the handoff findings, the same one that drives the GitHub `review:high` label), and `parent_branch` (the stack parent the branch was tracked under) in the run-log entry alongside the existing usage fields.
323	2. Posts a comment on the Linear issue via `linear.add_comment` (GraphQL `commentCreate`) with the PR URL and, when flagged, a `review:high` note.
324	
325	All four run-log fields are additive and default to `null` (push-to-main repos, halted issues, pre-PR run-logs). `grade.py` reads only `cycle_id`, `final_linear_state`, and `exit_code`, so pre-existing run-logs grade unchanged. The Linear comment is non-fatal: any failure is logged to stderr and the drain continues. The PR link is informational, never load-bearing for the drain's control flow.
326	
327	**Why the submit result, not a post-hoc `gh pr list` lookup.** An earlier draft of this decision had the orchestrator re-query GitHub by head branch after the worker exited — necessary in a design where the *worker* ran `gt submit`. Under §16's orchestrator-assembles design the lookup is redundant: the assembly step that creates the PR returns its URL and number in the same call, with no second query, no race against GitHub's index, and no dependency on branch-name conventions.
328	
329	**Why the orchestrator, not the agent.** The agent commits without pushing and writes the handoff file; it never talks to GitHub. The orchestrator is also the only component that can write to the run-log — it owns the `RunLog` object and calls `append_entry`.
330	
331	**Alternatives considered.**
332	
333	- *Post-hoc `gh pr list --head <branch>` lookup.* Rejected as redundant once assembly moved into the orchestrator — see above.
334	- *Always post the PR comment unconditionally (even on halt).* Rejected: a halted issue has no submitted PR (a graphite failure halts before this step). The comment fires only on confirmed Done with a successful submit.
335	
336	## 19. The worker owns PR submission via the finishing skill; the orchestrator reads `pr_urls` back
337	
338	This reverses the actor in §16 and §18. There, the orchestrator assembled and submitted the per-repo Graphite stack and posted the Linear comment. Now the **worker** does it: in drain mode the worker commits reviewable slices, then runs the finishing skill (`/shape:pr-finishing` today; `exec:finish` after the keystone cutover, [`architecture.md`](architecture.md) §7), which owns submission — it drives `gt`/`gh`, writes the submitted PR URLs into `.drain-handoff.json` (`pr_urls`), and posts the review-summary comment on the Linear issue. The orchestrator no longer assembles or submits anything; it **reads `pr_urls` back** as confirmation that submission succeeded, and a Done stack-mode issue with no `pr_urls` halts the run rather than letting the next issue stack on an unpushed branch.
339	
340	**Why the reversal.** It is the artifact boundary applied ([`architecture.md`](architecture.md) §2). Submitting a stack is "what a role does" — Layer 2 — so it belongs in a skill that runs identically by hand or unattended. Reading back whether the PRs exist is "whether an artifact exists" — Layer 1 — so it stays in the supervisor. The §16/§18 design put a Layer-2 action inside Layer 1, which is exactly the coupling the two-layer split removes: an orchestrator that knows the `gt`/`gh` sequence cannot be the thin, vendor-agnostic supervisor the keystone (§7) requires.
341	
342	**The verified `gt`/`gh` sequence in §16 is still correct** — it is just run by the finishing skill, not the orchestrator. §16's per-repo preconditions (`gt auth`, `gt init --trunk main`) and its stop-the-line restack policy carry over unchanged.
343	
344	**Completion recovery preserves the boundary.** When a worker exits leaving committed slices but the issue is not properly closed (not Done, or Done-without-`pr_urls`), the orchestrator does not run `gt`/`gh` itself — it spawns a fresh finishing sub-agent that runs the skill, then re-checks the contract, and only halts if completion still fails. A worker that left no committed slices halts as untrusted. (Tracked by the "Orchestrator-enforced completion" delivery plan.)
345	
346	**Alternatives considered.**
347	
348	- *Keep the orchestrator assembling the stack (§16/§18 as written).* Rejected: it hard-codes the PR-tooling sequence into Layer 1, blocking the keystone and the vendor-agnostic worker.
349	- *Worker pushes by hand instead of via the skill.* Rejected: the skill is the single place the submission procedure lives, so it stays identical in interactive and drain modes; a hand-rolled push in the worker prompt would be a second, drifting copy.
350	
351	## 20. A worker per phase, not a worker per issue
352	
353	Today one spawned worker runs the whole `exec:*` chain for an issue — pickup through finish — in a single session. The decision is to split it: each phase (code, review, finish) is its own spawn, with its own model tier, and the agent that produced an artifact never reviews it. See [`architecture.md`](architecture.md) §9.
354	
355	**Why split.** Two independent reasons, either sufficient on its own:
356	
357	- *Independent verification.* A coder reviewing its own work rationalises its own choices — the review inherits the blind spots of the build. A separate review agent that did not write the code is adversarial by construction, not by prompt wording. This is the same logic that made `exec:review` fan out to distinct personas (the persona contract); phase separation extends it across the build/review boundary, not just within review.
358	- *Per-phase model economics.* The operator anchors review to a stronger, more expensive model regardless of what built the change — a cheap model codes, an expensive one reviews. That asymmetry is only expressible if each phase is its own `claude -p` spawn with its own `--model` pin. A single worker pins one model for the whole chain.
359	
360	**Cost accepted.** Every phase boundary now pays a spawn plus artifact rehydration: the next phase starts cold and reads its inputs from the handoff envelope (architecture §2) rather than inheriting them in context. A single worker kept that context for free. This makes the handoff envelope load-bearing for *all* cross-phase state, not just `pr_urls` — the envelope must carry what each phase needs the next to know. This is the deliberate price of independence and the asymmetric-model economics.
361	
362	**Alternatives considered.**
363	
364	- *One worker runs the whole chain (status quo).* Rejected: it forecloses both independent review and per-phase model pinning — the coder grades itself, on the model that built the change.
365	- *One worker, but review re-spawned as a sub-agent within it.* Rejected as a half-measure: it buys independent review but not independent model economics at the phase grain, and it keeps the chain's lifecycle coupled to one outer session that the control plane cannot steer phase-by-phase (§10).
366	
367	## 21. Review is multi-altitude; higher-altitude review yields new work, not reverts
368	
369	Review fires at three altitudes matching the delivery hierarchy `shape:delivery` already produces — task, milestone, project — not only per task. The full model is in [`architecture.md`](architecture.md) §11.
370	
371	**Why multi-altitude.** A task review is diff-bounded: it grades one issue's change against its AC and the quality lenses. It cannot see whether the tasks of a milestone *cohere*, whether landing them degraded something *outside* their own boundary, or whether the project met its stated goals. Those are real defect classes that only exist at a higher altitude, so they need a review oriented to that altitude. Verification rolls up the same tree the work was decomposed down — the dual of the delivery hierarchy.
372	
373	**The load-bearing consequence: higher-altitude review produces new remediation work, not reverts.** Task review can halt before a PR merges, so its verdict can block a not-yet-merged artifact. A milestone or project review runs *after* its child PRs have merged; a merged slice cannot be cleanly reverted. So a failing milestone/project review emits new Linear issues slotted back into the plan — it does not roll back landed work. This is a genuinely different halt semantic from the task-level halt/revert contract (§3, §9-guardrails) and must be modelled as such: the supervisor's tree walker reacts to a failing altitude verdict by *scheduling*, not *reverting*.
374	
375	**Two unknowns deferred to spikes, not decided here.**
376	
377	- *Regression-review blast radius.* "Did landing this milestone degrade anything outside its boundary" is not diff-bounded the way task review is — it needs a definition of the boundary and probably a cross-cutting test/check run. Shape it with `shape:design` before building.
378	- *Remediation routing.* When an altitude review fails, what exactly is created (a new issue under the same milestone? a blocking flag on the project?), and does the supervisor pause the parent or keep draining siblings? This is the verdict-handoff open seam (architecture "Known open seam") widened to higher altitudes.
379	
380	**Alternatives considered.**
381	
382	- *Task review only; trust that coherent tasks compose into a coherent milestone.* Rejected: integration and regression defects are exactly the ones that survive a green per-task review, because no task-level lens is oriented to find them.
383	- *Run all altitude reviews inline at project end.* Rejected: a milestone defect found only at project end is far more expensive to remediate than one caught when the milestone closed, and project-end is too late to inform the next milestone's work.
384	
385	## 22. The supervisor stays a process executing a planned unit; it is not a Claude skill
386	
387	Two coupled decisions about the supervisor's form and scope.
388	
389	**Scope — a planned unit, not specifically a cycle.** The supervisor executes a *planned unit of work*: a Linear cycle today, a whole project later. The execution atom is unchanged (one issue, a worker per phase, §20); a cycle and a project differ only as containers with a hierarchy over them (§21). "Drain a cycle" becomes one entry point rather than the definition. Project execution is out of scope now, but it is a later container on the same machinery, not a redesign — so vision and architecture are written in the generic terms ([`architecture.md`](architecture.md) §12). The tool keeps the name `drain-cycle`.
390	
391	**Form — a process with a CLI front-door, not a `/execute-cycle` skill.** It is tempting to encapsulate the supervisor itself as a Claude skill (`/execute-cycle`, `/execute-project`) for one-command ergonomics. Rejected: a skill runs *inside* a Claude session, which makes the supervisor Claude-shaped and collapses the artifact boundary (§2) that lets the worker be any vendor. The supervisor's whole value is being content-blind and vendor-agnostic; a skill cannot be that. The one-command ergonomics come instead from a thin CLI front-door (`drain-cycle run <unit>`), while Layer 2 stays skills.
392	
393	**Why this matters now.** The resident control plane (§10) is a long-lived process with an API — that only makes sense as a process, reinforcing the form decision. A control plane implemented as a Claude skill could not be the daemon that spawns and steers vendor-agnostic workers.
394	
395	**Alternatives considered.**
396	
397	- */execute-cycle as the primary entry point.* Rejected per above — collapses the vendor-agnostic boundary.
398	- *Hybrid: a `/execute-cycle` skill that shells out to the process for interactive use.* Not adopted now, but not foreclosed — it is a thin convenience wrapper over `drain-cycle run`, addable later if the keyboard ergonomics warrant it, without moving any supervision logic into the skill.
399	
```

> AGENT

I've checked the standard (`style-rules.md` + `design-docs.md`) against the prose I added. Reading the drafts against it rather than from memory:

## Verdict: accept with notes

No load-bearing span fails a Phase 1–3 rule — the SCQA spine holds, the multi-altitude table is MECE, headings carry results, and the two spike unknowns survived pruning (risks intact). Only Phase-4 vocabulary/character findings remain.

## Findings

**1. `vision.md:32` — nominalization + dropped actor (the one real fix).**
> "Verification rolls up the same hierarchy the work was broken down along."

The whole paragraph names *the connector* as the doer ("the connector verifies at every altitude… It checks each task…"), then this closing sentence switches to an abstract noun + passive and loses the actor. Rule: *characters as subjects, reverse nominalizations.*
Rewrite: **"The connector verifies up the same hierarchy it broke the work down along."**

**2. `vision.md:32` — `altitude` is borrowed jargon in the plainspoken doc.**
> "the connector verifies at every altitude, not just the bottom"

`altitude` is `architecture.md` §11's *defined* term. The vision is deliberately plainspoken (talking to yourself). Rule: *no jargon where a plainer word works.*
Rewrite: **"at every level, not just the bottom"** — optional; keep `altitude` if you want the two docs to echo each other.

**3. `design-decisions.md:372` and `:360` — `load-bearing` is on the watchlist.**
> "The load-bearing consequence: higher-altitude review produces new remediation work…"
> "This makes the handoff envelope load-bearing for *all* cross-phase state…"

The watchlist flags `load-bearing → essential/required` (overworked metaphor). Caveat worth weighing: this is **established house style** — §13 ("Flush-on-exit is load-bearing"), §14 ("the four-segment ordering… is load-bearing") predate my changes, so my new usages are *consistent*, not novel. The strict rule says replace; consistency says keep. Your call.
If replacing: **"The decisive consequence:"** and **"…makes the handoff envelope carry *all* cross-phase state."**

Everything else — §9/§10/§12, the architecture §1 edit, the open-seam extension, §20/§22, the count bump — passes clean. "Work fans down; verification rolls up" is the strongest line in the set.

Want me to apply #1 (clear fix), and #2/#3 per your preference?

> DEVELOPER

also make a linear issue for the changes you've identified in layer 2 (reliability-resilience persona and a verification-implementation fold)

> AGENT

I'll apply finding #1 (the unambiguous fix), then create the Linear issue. Let me also pull the current cycle so I can slot it correctly.

> TOOL

tool_use Edit
id: toolu_012XoQJYFwmufQ3M79LZxQCu
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/src/drain-cycle/docs/vision.md",
  "old_string": "Verification rolls up the same hierarchy the work was broken down along.",
  "new_string": "The connector verifies up the same hierarchy it broke the work down along."
}
```

> TOOL

tool_result
id: toolu_012XoQJYFwmufQ3M79LZxQCu
```
The file /Users/anton/src/drain-cycle/docs/vision.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use ToolSearch
id: toolu_01Q3yBPRnYhxYxbEztD3Jau4
```json
{
  "query": "select:mcp__claude_ai_Linear__list_cycles,mcp__claude_ai_Linear__save_issue,mcp__claude_ai_Linear__list_projects",
  "max_results": 5
}
```

> TOOL

tool_result
id: toolu_01Q3yBPRnYhxYxbEztD3Jau4
```
{
  "type": "tool_reference",
  "tool_name": "mcp__claude_ai_Linear__list_cycles"
}
{
  "type": "tool_reference",
  "tool_name": "mcp__claude_ai_Linear__save_issue"
}
{
  "type": "tool_reference",
  "tool_name": "mcp__claude_ai_Linear__list_projects"
}
```

> TOOL

tool_use mcp__claude_ai_Linear__list_cycles
id: toolu_017gfrjDXecvuj4SjhHXghvL
```json
{
  "teamId": "Personal",
  "type": "current"
}
```

> TOOL

tool_use mcp__claude_ai_Linear__list_projects
id: toolu_0145JAa2UvGS6fivPATJragD
```json
{
  "team": "Personal",
  "query": "lifecycle phase skills"
}
```

> TOOL

tool_result ERROR
id: toolu_017gfrjDXecvuj4SjhHXghvL
```
Argument Validation Error
```

> TOOL

tool_result
id: toolu_0145JAa2UvGS6fivPATJragD
```
{"projects":[],"hasNextPage":false}
```

> TOOL

tool_use ToolSearch
id: toolu_018Bk4JbgDwEratKrJqTLbrN
```json
{
  "query": "select:mcp__claude_ai_Linear__list_teams",
  "max_results": 3
}
```

> TOOL

tool_result
id: toolu_018Bk4JbgDwEratKrJqTLbrN
```
{
  "type": "tool_reference",
  "tool_name": "mcp__claude_ai_Linear__list_teams"
}
```

> TOOL

tool_use mcp__claude_ai_Linear__list_projects
id: toolu_01SqDpvBLs9bcGCZ6bKQB9tt
```json
{
  "team": "Personal"
}
```

> TOOL

tool_result
id: toolu_01SqDpvBLs9bcGCZ6bKQB9tt
```
{"projects":[{"id":"b1835e7e-4034-4f3f-921f-3bf3554531e2","icon":null,"color":"#bec2c8","name":"Watch pane: Claude-Code-style rendering","summary":"drain-cycle -w pane renders worker sessions as a Claude-Code-style transcript — display-side only, zero observability impact. One 5-PR Graphite stack.","description":"**Goal:** An operator watching `drain-cycle -w` reads each worker session as a Claude-Code-style transcript instead of raw stream-json or terse `===` headers — with zero impact on parse fidelity, usage accounting, or run logs.\n\n+++ **Delivery plan**: `drain-cycle docs/delivery-plans/watch-pane-rich-rendering/`\n\n+++","url":"https://linear.app/ababushkin/project/watch-pane-claude-code-style-rendering-80c86f79c7ee","createdAt":"2026-06-11T07:31:14.247Z","updatedAt":"2026-06-11T14:01:01.187Z","startedAt":"2026-06-11T12:02:36.226Z","completedAt":"2026-06-11T14:01:01.187Z","canceledAt":null,"startDate":"2026-06-11","startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":0,"name":"No priority"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"8703bdf7-c7c4-4c03-bb77-90f6d4163c6b","name":"Completed","type":"completed"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"b313da89-8ac3-43fb-ad5b-e9f76a6050f2","icon":null,"color":"#bec2c8","name":"drain-cycle supervises; the pack owns the workflow","summary":"Re-scope drain-cycle to a thin vendor-agnostic supervisor (spawn, guardrails, halt, resume, grade); the intra-issue workflow moves into the Shaper pack. Third of three in the lifecycle expansion.","description":"**Goal:** For Anton (single user), make unattended cycle drains run with the supervisor owning only process concerns — spawn, guardrails, halt, resume, grade — so any vendor's worker can follow the pack's workflow prose unchanged.\n\n**Key results:**\n\n**KR1 (stretch)** — a full cycle drains to completion with the worker prompt reduced to issue context + a single skill pointer (zero inlined workflow steps), at the execution initiative's quality b… (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/drain-cycle-supervises-the-pack-owns-the-workflow-0f0222d99392","createdAt":"2026-06-10T03:09:57.953Z","updatedAt":"2026-06-10T03:09:57.953Z","startedAt":null,"completedAt":null,"canceledAt":null,"startDate":null,"startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":0,"name":"No priority"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"397ab5c0-7cdf-47ad-b862-02acfd85c92f","name":"Planned","type":"planned"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"962be170-d2f2-4b4e-99e5-19f01140c3b4","icon":null,"color":"#bec2c8","name":"Consolidate Shaper’s Lifecycle into Four Phase Skills","summary":"Collapse the shaping half of Shaper into four phase skills (shape:idea/project/design/delivery), each under the length cap, every pruned skill absorbed or deleted. Second of three lifecycle-expansion projects.","description":"The current Shaper library is spread across 11 skills, totaling 2,357 lines. Because several components exceed our 300-line limit and the fragmented structure slows down both humans and agents, we will consolidate the shaping process into four core phase skills: `shape:idea`, `shape:project`, `shape:design`, and `shape:delivery`.\n\nOur goal is to ensure every new skill is gate-complete and fits within our technical constraints without losing th… (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/consolidate-shapers-lifecycle-into-four-phase-skills-9c8a65552b93","createdAt":"2026-06-10T03:09:46.260Z","updatedAt":"2026-06-11T23:58:57.566Z","startedAt":"2026-06-11T23:58:57.565Z","completedAt":null,"canceledAt":null,"startDate":"2026-06-11","startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":0,"name":"No priority"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"9ef516a2-cb23-4981-a57d-34c060daa524","name":"In Progress","type":"started"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"f9399232-74f6-45fe-977c-dde359f2c035","icon":null,"color":"#bec2c8","name":"Issues drain end-to-end on first-party skills","summary":"Execution-half of the Shaper lifecycle expansion: workers complete Linear issues end-to-end on first-party skills so superpowers and agent-skills can be uninstalled.","description":"**Goal:** For drain-cycle workers (and Anton driving interactively), make every picked-up Linear issue flow from pickup to a merged, reviewable PR on Shaper skills alone — review trail attached, no rescue by a human and no reliance on third-party packs.\n\n**Key results:**\n\n**KR1 (stretch)** — ≥4 of the next 5 drained issues reach Done with a merged PR and zero manual fix commits after the worker's final push, with the full review trail present … (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/issues-drain-end-to-end-on-first-party-skills-be562671c8d8","createdAt":"2026-06-10T03:07:34.303Z","updatedAt":"2026-06-11T14:01:15.756Z","startedAt":"2026-06-10T05:13:17.145Z","completedAt":"2026-06-11T14:01:15.756Z","canceledAt":null,"startDate":"2026-06-10","startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":0,"name":"No priority"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"8703bdf7-c7c4-4c03-bb77-90f6d4163c6b","name":"Completed","type":"completed"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"97265a3e-9dd7-4719-91ad-420cca11c3b3","icon":null,"color":"#bec2c8","name":"Fold execution-breakdown into delivery-shape","summary":"Collapse delivery-shape + execution-breakdown into one skill that emits execution-ready plans with AC and model routing on every task.","description":"Collapse the two-skill delivery planning pipeline into one. delivery-shape will produce execution-ready nodes — full task lists with acceptance criteria, dependency ordering, and model routing via task-sizing.md — eliminating the separate at-pickup breakdown step. execution-breakdown is hard-deleted.\n\n**Why:** Having two skills (delivery-shape → execution-breakdown) with a deferred delegation step adds friction without value. The \"tasks decay … (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/fold-execution-breakdown-into-delivery-shape-228626f3ec95","createdAt":"2026-06-09T01:18:35.865Z","updatedAt":"2026-06-10T01:48:59.760Z","startedAt":"2026-06-09T01:19:59.958Z","completedAt":"2026-06-10T01:48:59.759Z","canceledAt":null,"startDate":"2026-06-09","startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":0,"name":"No priority"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"8703bdf7-c7c4-4c03-bb77-90f6d4163c6b","name":"Completed","type":"completed"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"f630d813-2f10-4691-baac-64858ef1e2b3","icon":"Rocket","color":"#bec2c8","name":"Knowledge Retrieval for Agent Cognitive Augmentation","summary":"Local hybrid retrieval system giving LLM agents access to 43 curated books via MCP","description":"**Goal:** For Anton building LLM-based cognitive augmentation tools, agents reliably draw on curated domain knowledge at query time instead of answering from training data alone.\n\n**Key results:**\n\n**KR1 (stretch/bet)** — ≥ 3 of 4 manual test prompts against the middle-management domain return a clearly relevant passage in top-3 results at walking skeleton completion\n\n* baseline: 0/4 — no retrieval system exists\n* target: ≥ 3/4\n* measured over… (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/knowledge-retrieval-for-agent-cognitive-augmentation-2f5b6f5a313c","createdAt":"2026-06-07T23:30:38.200Z","updatedAt":"2026-06-07T23:30:38.200Z","startedAt":null,"completedAt":null,"canceledAt":null,"startDate":null,"startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":0,"name":"No priority"},"labels":[],"initiatives":[],"lead":{},"status":{"id":"2941e5ab-173a-4b38-8032-c21209bb8883","name":"Backlog","type":"backlog"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"0d5d19a0-2683-4b3e-8681-754c5d24f6aa","icon":":ticket:","color":"#bec2c8","name":"Idea-to-ticket shaping — any idea, right-sized, review-ready","summary":"Generalize delivery-shape into the product-facing ticket shaper: any idea (single/bulk, goal optional) → consistent, right-sized, review-ready tickets, size-gated so agents never pick up oversized work. Shape-and-park for a future cycle.","description":"> **Status: parked.** Shaped and ready, not yet in a cycle. Pull into cycle planning when ready to build. Amends ADR 0001's input clause (see `docs/adr/0002-delivery-shape-accepts-ideas-goal-optional.md`); full brief in `docs/designs/shaping-pipeline.md`.\n\n**Goal:** For the operator shaping product work, we want turning a raw idea — one or many, with or without a goal attached — into consistent, right-sized, review-ready tickets to take minute… (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/idea-to-ticket-shaping-any-idea-right-sized-review-ready-b639a7bf24ac","createdAt":"2026-06-03T10:40:28.059Z","updatedAt":"2026-06-11T07:29:36.817Z","startedAt":"2026-06-03T11:12:42.394Z","completedAt":null,"canceledAt":"2026-06-11T07:29:36.817Z","startDate":"2026-06-03","startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":3,"name":"Medium"},"labels":[],"initiatives":[{"id":"d06c222a-5de9-4d47-8423-f294a4dacfd8","name":"Planning overhaul with linear decoupling"}],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"c00893f6-f280-41b4-a1a1-c29abf16dc3a","name":"Canceled","type":"canceled"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"bc9ad068-270a-4f29-82e2-ffb8c8d2dc99","icon":null,"color":"#bec2c8","name":"Verify-flow agent skills","summary":"Four SKILL.md files encoding the agent roles in the verify flow — task shaping, outcome verification, PR preparation, and PR feedback response.","description":"**Goal:** For operators running agent drain-cycles on outcome-focused tickets, make task shaping, outcome verification, PR preparation, and PR feedback response happen through codified skill-encoded roles — so these checkpoints don't rely on ad-hoc agent judgement or get silently skipped.\n\n**Key results:**\n\n**KR1 (commit)** — Each of the four skills fires correctly when invoked manually against a real ticket or PR, producing structured output … (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/verify-flow-agent-skills-88838dbc61e0","createdAt":"2026-06-01T06:34:32.143Z","updatedAt":"2026-06-10T01:48:51.637Z","startedAt":"2026-06-01T06:36:04.718Z","completedAt":null,"canceledAt":"2026-06-10T01:48:51.636Z","startDate":"2026-06-01","startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":2,"name":"High"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"c00893f6-f280-41b4-a1a1-c29abf16dc3a","name":"Canceled","type":"canceled"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"812bc9b5-1618-48b8-8041-6d6223dc6d4c","icon":null,"color":"#bec2c8","name":"Multi-agent collaboration for correctness","summary":"Layer-1 enforcement/recording/grading in drain-cycle: verifier-gated Done + run-log verdicts + grading, around the pack's already-shipped exec:* skills. So hard tickets don't silently land with missing AC.","description":"**Re-scoped (2026-06-15) to Layer-1 only.** This project originally proposed six agent-driven roles plus the skills behind them. Those skills now exist: the \"Issues drain end-to-end on first-party skills\" project shipped them in the Shaper pack as the `exec:*` execution flow (`exec:pickup`/`exec:breakdown`, `exec:build`, `exec:debug`/`exec:simplify`, `exec:review`/`exec:pr-prepare`, `exec:verify`, `exec:pr-respond`). Under the two-layer archit… (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/multi-agent-collaboration-for-correctness-5a36114c586c","createdAt":"2026-05-28T10:17:39.942Z","updatedAt":"2026-06-15T09:22:13.600Z","startedAt":"2026-06-01T06:52:26.789Z","completedAt":null,"canceledAt":null,"startDate":"2026-06-01","startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":0,"name":"No priority"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"2941e5ab-173a-4b38-8032-c21209bb8883","name":"Backlog","type":"backlog"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"21b16b54-4f87-46e0-8566-257a17c402e8","icon":null,"color":"#bec2c8","name":"Test drain-cycle failure modes and resume without a real Linear cycle","summary":"","description":"**Goal:** For the drain-cycle operator (single-user, personal product), make failure modes and resume behaviour cheap to test, so that adding a test for a new scenario no longer needs a real Linear cycle and the existing failure paths gain a trusted safety net.\n\n**Key results:**\n\n**KR1 (commit)** — Adding a test for a new drain-cycle failure mode no longer needs a real Linear cycle. A new scenario plugs into the harness, runs against the in-pr… (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/test-drain-cycle-failure-modes-and-resume-without-a-real-linear-cycle-910b954af13f","createdAt":"2026-05-28T08:30:31.900Z","updatedAt":"2026-06-10T14:25:58.567Z","startedAt":null,"completedAt":null,"canceledAt":null,"startDate":null,"startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":0,"name":"No priority"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"2941e5ab-173a-4b38-8032-c21209bb8883","name":"Backlog","type":"backlog"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"8b6ce9b1-6b87-4d3b-97fc-2b1ffe17a608","icon":":building_construction:","color":"#bec2c8","name":"Top-down delivery planning — framing baked in, foundational work never silent","summary":"Standalone delivery-planning skill: turn a committed initiative into a hierarchical markdown delivery plan (deliverables→capabilities/stories→tasks) with framing + foundational work baked in. Parked behind the initiative-shape Linear-decouple.","description":"**Goal:** For Anton and any agent invoking Shaper, make a committed initiative produce its full delivery plan top-down — deliverables → capabilities/stories → verifiable tasks — with framing baked in and foundational work never silently dropped.\n\n**Key results:**\n\n**KR1 (commit)** — A documented plan-artefact contract and a worked file-set for one real already-shaped initiative exist, and a walk-script converts that file-set into the expected … (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/top-down-delivery-planning-framing-baked-in-foundational-work-never-352e1fe0c3b8","createdAt":"2026-05-25T08:14:25.141Z","updatedAt":"2026-06-03T11:12:52.930Z","startedAt":"2026-05-25T10:13:43.887Z","completedAt":"2026-06-03T11:12:52.929Z","canceledAt":null,"startDate":"2026-05-25","startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":2,"name":"High"},"labels":[],"initiatives":[{"id":"d06c222a-5de9-4d47-8423-f294a4dacfd8","name":"Planning overhaul with linear decoupling"}],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"8703bdf7-c7c4-4c03-bb77-90f6d4163c6b","name":"Completed","type":"completed"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"8b7d20a8-eb98-45ce-998e-537ad6cff93b","icon":":compass:","color":"#bec2c8","name":"Per-task model routing — deliberate, not ad-hoc","summary":"A planning-time routing layer: every task gets a model tier + risk profile from a 5-axis rubric. Parked until ready to pull into a cycle.","description":"> **Status: parked.** Shaped and ready, not yet in a cycle. Pull into cycle planning when ready to build. The issue breakdown below is captured up front so the work is thorough on day one.\n\n**Goal:** For Anton and any agent breaking work into tasks in Shaper, assign every task a model tier and a risk profile at breakdown time without prompting — so model choice and review attention are deliberate and reproducible rather than ad-hoc.\n\n**Key res… (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/per-ta[REDACTED_SK]","createdAt":"2026-05-25T08:04:37.546Z","updatedAt":"2026-06-03T11:12:59.187Z","startedAt":"2026-05-28T13:20:55.689Z","completedAt":"2026-06-03T11:12:59.187Z","canceledAt":null,"startDate":"2026-05-28","startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":2,"name":"High"},"labels":[],"initiatives":[{"id":"d06c222a-5de9-4d47-8423-f294a4dacfd8","name":"Planning overhaul with linear decoupling"}],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"8703bdf7-c7c4-4c03-bb77-90f6d4163c6b","name":"Completed","type":"completed"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"fdbb920e-a39c-4b83-83a4-348d2bf06df5","icon":":gear:","color":"#bec2c8","name":"Workflow governance — single source, installable on any machine","summary":"Package workflow governance as a separately-installable pack (repo agent-skills-workflow, plugin workflow) with Linear as one module — distinct from Shaper, so it travels to any machine and adopting Shaper never forces a tracker.","description":"# Initiative — workflow governance, single-sourced and installable anywhere\n\n**Goal:** For anyone who wants to work the way I do — me included, on a new machine — we want our workflow governance to be adoptable on its own, separate from the Shaper methodology, so adopting Shaper never forces a tracker and the patterns travel to any machine unchanged.\n\n## Key results\n\n**KR1 (commit)** — Governance installs and loads on a clean machine with zero… (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/workflow-governance-single-source-installable-on-any-machine-6b861e6c3769","createdAt":"2026-05-25T06:09:08.731Z","updatedAt":"2026-06-03T10:12:44.517Z","startedAt":"2026-05-28T13:20:17.897Z","completedAt":"2026-06-03T10:12:44.516Z","canceledAt":null,"startDate":"2026-05-28","startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":2,"name":"High"},"labels":[],"initiatives":[{"id":"d06c222a-5de9-4d47-8423-f294a4dacfd8","name":"Planning overhaul with linear decoupling"}],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"8703bdf7-c7c4-4c03-bb77-90f6d4163c6b","name":"Completed","type":"completed"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"404fb55b-1efc-4a7e-a1a9-9a3a3ce038e0","icon":null,"color":"#bec2c8","name":"Shaper — shape skills fire at the right decision moment, no /command required","summary":"","description":"**Goal:** For Anton using the Shaper pack, make shape skills fire at the right decision moment — so Claude invokes the correct skill proactively without requiring a typed /skill-name command.\n\n**Key results:**\n\n**KR1 (commit)** — Running `bash hooks/session-start.sh` produces valid JSON whose `message` field contains the name and trigger phrases for ≥8 of 10 shape skills *(foundation)*\n\n* baseline: hook does not exist; no shape skill descripti… (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/shaper-shape-skills-fire-at-the-right-decision-moment-no-command-d51ca28c5098","createdAt":"2026-05-25T06:04:31.461Z","updatedAt":"2026-05-25T06:17:16.940Z","startedAt":"2026-05-25T06:09:53.775Z","completedAt":"2026-05-25T06:17:16.940Z","canceledAt":null,"startDate":"2026-05-25","startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":0,"name":"No priority"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"8703bdf7-c7c4-4c03-bb77-90f6d4163c6b","name":"Completed","type":"completed"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"f6e4dffc-f8a1-4d9d-ae8f-3d09be443418","icon":"Chart","color":"#bec2c8","name":"cc-metrics — Claude Code session cost → Linear","summary":"","description":"Goal: For any Claude Code user, automatically record AI compute cost and time against the active Linear issue — so session governance requires zero manual steps.\n\nKey results:\n\n1. cc-metrics install completes without error on macOS\n   baseline: not implemented\n   target: [install.sh](<http://install.sh>) exits 0, SessionEnd hook appears in settings.json\n   window: by end of initiative\n   source: [install.sh](<http://install.sh>) exit code + se… (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/cc-metrics-claude-code-session-cost-linear-c37b14980615","createdAt":"2026-05-25T06:01:46.776Z","updatedAt":"2026-06-11T07:29:21.203Z","startedAt":null,"completedAt":null,"canceledAt":"2026-06-11T07:29:21.203Z","startDate":null,"startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":3,"name":"Medium"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"c00893f6-f280-41b4-a1a1-c29abf16dc3a","name":"Canceled","type":"canceled"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"fde36e75-91b0-4256-ac99-91f0de18ca8c","icon":":camera:","color":"#bec2c8","name":"AU passport/visa photo — pre-submission compliance","summary":"Local, offline tool to verify and auto-fix a photo against AU passport/visa specs before printing or uploading — no face data sent to any online service.","description":"For myself, preparing an AU immigration document set: know whether a photo will be accepted before I print or upload it — without sending my face to the online photo services the Australian Passport Office warns against (identity-fraud risk).\n\n```\nGoal:           For myself (preparing an AU immigration document set), verify and auto-fix\n                a photo against AU passport/visa specs entirely locally — no face data sent\n                … (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/au-passportvisa-photo-pre-submission-compliance-5e0d442d05d0","createdAt":"2026-05-25T02:01:13.129Z","updatedAt":"2026-05-25T06:33:40.705Z","startedAt":"2026-05-25T02:10:27.813Z","completedAt":"2026-05-25T06:33:38.172Z","canceledAt":null,"startDate":"2026-05-25","startDateResolution":null,"targetDate":"2026-05-25","targetDateResolution":null,"priority":{"value":2,"name":"High"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"8703bdf7-c7c4-4c03-bb77-90f6d4163c6b","name":"Completed","type":"completed"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"31524abe-5b32-4b9f-ad5e-648d78436fa2","icon":null,"color":"#bec2c8","name":"Faster FB Marketplace listings via /resell-au","summary":"Make /resell-au meaningfully faster end-to-end without regressing the reliability that works today (Type 3 utility skill pack)","description":"**Objective:** Make `/resell-au` meaningfully faster end-to-end - without losing the quality or coverage that work today.\n\n---\n\n### Key results\n\n**KR1 (stretch) - Faster end-to-end** *(the bet)*\n\nMedian time from \"item in front of me\" to \"posted\" drops by 40%.\n\n* baseline: TBD — first 3 listings of the cycle set it\n* target: −40% on median elapsed time\n* measured over:  next 10 listings (after baseline)\n* how we'll know:  `elapsed_seconds` fie… (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/faster-fb-marketplace-listings-via-resell-au-00423ec1108c","createdAt":"2026-05-21T13:37:36.666Z","updatedAt":"2026-06-11T07:29:47.390Z","startedAt":null,"completedAt":null,"canceledAt":"2026-06-11T07:29:47.390Z","startDate":null,"startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":3,"name":"Medium"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"c00893f6-f280-41b4-a1a1-c29abf16dc3a","name":"Canceled","type":"canceled"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"3b5c5e13-355a-4e70-b943-6251d7f14baf","icon":null,"color":"#bec2c8","name":"Autonomous cycle drain - eliminate manual shepherding","summary":"A CLI that drains a Linear cycle by spawning fresh Claude Code sessions per issue — frees operator time for scoping and validation.","description":"**Goal:**\nI want to drain a well-scoped Linear cycle without shepherding each issue, so my attention shifts from execution to scoping the next cycle and validating delivered work.\n\n(*Well-scoped* = every issue has acceptance criteria explicit enough for a Claude session to verify its own work against.)\n\n**Key results:**\n\n**KR1 \\[aspirational\\]** — A well-scoped cycle drains to \"all issues Done\" in a single uninterrupted run.\n\n* baseline: 0% — … (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/autonomous-cycle-drain-eliminate-manual-shepherding-75daa8863063","createdAt":"2026-05-21T12:31:22.306Z","updatedAt":"2026-06-03T10:13:33.544Z","startedAt":"2026-05-21T13:16:45.647Z","completedAt":"2026-06-03T10:13:33.543Z","canceledAt":null,"startDate":"2026-05-21","startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":2,"name":"High"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"8703bdf7-c7c4-4c03-bb77-90f6d4163c6b","name":"Completed","type":"completed"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"6dcb88bc-b0e9-45ed-b0d1-68690b024dbe","icon":"Chart","color":"#bec2c8","name":"Personal observability for Claude Code skill packs + nestl","summary":"","description":"**Goal.** For Anton (sole developer): a single free-tier dashboard showing Claude Code skill usage, token cost, and nestl pipeline reliability. No recurring cost, no servers to maintain, no on-call alerts. Skill-description drift surfaces weekly as evidence, not guesswork.\n\n**Key results**\n\n**KR1:** Claude Code sessions produce complete traces in Honeycomb.\n\n* baseline: zero traces ingested; no LLM telemetry backend wired up\n* target: each of … (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/personal-observability-for-claude-code-skill-packs-nestl-ffe9ee99d973","createdAt":"2026-05-21T11:05:52.258Z","updatedAt":"2026-06-10T14:26:01.927Z","startedAt":null,"completedAt":null,"canceledAt":null,"startDate":null,"startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":2,"name":"High"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"2941e5ab-173a-4b38-8032-c21209bb8883","name":"Backlog","type":"backlog"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"13b58566-a84a-4c79-9eef-ab294a911e90","icon":null,"color":"#bec2c8","name":"Pipeline recovery without the database console","summary":"","description":"**Goal:** For the Nestl operator, we want the operator to trigger and recover all pipeline jobs from the admin dashboard, on a laptop that regularly sleeps.\n\n**Key results:**\n\n**KR1 \\[committed\\] — Recovery path** — Any stuck PipelineRun state clears from the admin dashboard in one action.\n\n* baseline: stuck `\"running\"` rows require direct DB access to clear; the admin UI has no escape hatch\n* target: any operator-visible stuck state clearable… (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/pipeline-recovery-without-the-database-console-628d938363fa","createdAt":"2026-05-21T11:02:02.030Z","updatedAt":"2026-05-25T06:04:45.569Z","startedAt":null,"completedAt":null,"canceledAt":null,"startDate":null,"startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":3,"name":"Medium"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"2941e5ab-173a-4b38-8032-c21209bb8883","name":"Backlog","type":"backlog"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"eb473805-5029-47eb-b0e6-3e06e3e42a04","icon":null,"color":"#bec2c8","name":"Workspace docs","summary":"Home for workspace-level docs that span multiple initiatives — period goals, planning references, governance notes.","description":"Home for workspace-level documents that don't belong to any single initiative — period goals, planning references, governance notes. Not an initiative; no Goal or Key Results.","url":"https://linear.app/ababushkin/project/workspace-docs-2d8b127436c8","createdAt":"2026-05-20T14:10:03.506Z","updatedAt":"2026-05-20T14:10:38.948Z","startedAt":"2026-05-20T14:10:35.668Z","completedAt":null,"canceledAt":null,"startDate":"2026-05-20","startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":2,"name":"High"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"9ef516a2-cb23-4981-a57d-34c060daa524","name":"In Progress","type":"started"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"172c8fce-10cf-45a1-bc7c-ddd4d05083aa","icon":null,"color":"#bec2c8","name":"Initiative quality - type-aware OKRs with KRs","summary":"Improve /initiative-shape so it produces type-aware OKR-shaped Linear initiatives with 3 KRs each (baseline+target+window+source), a kill condition, and a project type tag — verifiable by system inspection.","description":"## Goal\n\nFor Anton (and any agent invoking pde-skills), make `/initiative-shape` produce OKR-shaped Linear initiatives that are type-aware, carry 3 KRs each (not 1 success criterion), and are verifiable by system inspection — so cycle planning operates on well-shaped goals instead of repo-aliased backlogs.\n\n## Key results\n\n**KR1 \\[committed\\]** — `/initiative-shape` produces ≥3 KRs (not 1 success criterion) for every initiative created across … (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/initiative-quality-type-aware-okrs-with-krs-8087dfe76e88","createdAt":"2026-05-20T13:07:06.295Z","updatedAt":"2026-05-25T08:02:19.939Z","startedAt":"2026-05-20T14:14:06.357Z","completedAt":"2026-05-25T08:02:19.938Z","canceledAt":null,"startDate":"2026-05-20","startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":2,"name":"High"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"8703bdf7-c7c4-4c03-bb77-90f6d4163c6b","name":"Completed","type":"completed"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"012923d7-25b5-475b-a1a7-5832a54ed389","icon":null,"color":"#bec2c8","name":"Ops - bugs, maintenance, emergent","summary":"Container for non-initiative work. Not an initiative; no Goal or Key Results. Bugs, KTLO, compliance, one-offs. Pulled into each cycle's ops slot at planning.","description":"**Role:** Container for non-initiative work — bugs, KTLO, compliance, one-offs, anything that doesn't have a sustained goal behind it.\n\n**What belongs here:**\n\n* Bugs (any size)\n* Maintenance / KTLO\n* Compliance + legal items\n* Single-issue emergent work\n* Anything under \\~5 issues with no clear unifying outcome\n\n**What does NOT belong here:**\n\n* Anything with 5+ issues and a goal — that's an initiative; run `/initiative-shape` instead. Don't … (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/ops-bugs-maintenance-emergent-d6cc8ff6679c","createdAt":"2026-05-20T09:41:27.461Z","updatedAt":"2026-05-20T14:39:22.020Z","startedAt":"2026-05-20T14:39:22.019Z","completedAt":null,"canceledAt":null,"startDate":"2026-05-20","startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":3,"name":"Medium"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"9ef516a2-cb23-4981-a57d-34c060daa524","name":"In Progress","type":"started"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"afbe8146-8e15-4415-9978-2bdd2eb69a26","icon":null,"color":"#bec2c8","name":"Equity - valuation reacts to fresh earnings, not stale Wall Street consensus","summary":"","description":"**Goal:** For the investor, the moment a company reports earnings, our valuation reflects what the company actually just said — not stale Wall Street consensus that hasn't caught up yet. We get there by reading the small set of company-specific numbers that actually drive the forecast (segment revenue for multi-segment businesses, backlog/bookings for infrastructure companies).\n\n**Key results:**\n\n1. Two new KPI families ship — segment revenue … (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/equity-valuation-reacts-to-fresh-earnings-not-stale-wall-street-10465d705ca7","createdAt":"2026-05-20T09:13:54.331Z","updatedAt":"2026-05-25T06:04:37.386Z","startedAt":"2026-05-20T14:12:38.644Z","completedAt":null,"canceledAt":null,"startDate":"2026-05-20","startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":3,"name":"Medium"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"2941e5ab-173a-4b38-8032-c21209bb8883","name":"Backlog","type":"backlog"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"483d7387-8f39-4918-b359-7512b11fb92e","icon":null,"color":"#bec2c8","name":"FB Listing - refresh stale listings","summary":"","description":"**Goal:** For the seller, refresh stale Facebook Marketplace listings automatically — drop the price, re-list, keep selling — instead of manually deleting and re-creating each one.\n\n**Key results:**\n\n1. Running the refresh command on a folder of listings completes the whole loop for every eligible stale item — find it, delete the old listing, post a new one at a lower price, record the result — with no need for the seller to step in mid-run.\n2… (truncated, use `get_project` for full description)","url":"https://linear.app/ababushkin/project/fb-listing-refresh-stale-listings-a65e6498defc","createdAt":"2026-05-20T09:13:33.614Z","updatedAt":"2026-06-03T10:11:57.283Z","startedAt":"2026-05-20T14:12:02.847Z","completedAt":"2026-06-03T10:11:57.282Z","canceledAt":null,"startDate":"2026-05-20","startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":3,"name":"Medium"},"labels":[],"initiatives":[],"lead":{"id":"720d0535-dfc6-465f-8111-d1a3e6eab786","name":"Anton Babushkin"},"status":{"id":"8703bdf7-c7c4-4c03-bb77-90f6d4163c6b","name":"Completed","type":"completed"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]},{"id":"640e383c-4722-447f-9216-acedefdbdf21","icon":null,"color":"#bec2c8","name":"PDE skill pack","summary":"Closed 2026-05-20: 3 issues shipped in Cycle 1 (backend-spike, product-spike rename, render-html registration). Superseded by initiative-based model.","description":"","url":"https://linear.app/ababushkin/project/pde-skill-pack-7616052be5d2","createdAt":"2026-05-12T03:42:00.198Z","updatedAt":"2026-06-15T09:18:05.748Z","startedAt":null,"completedAt":"2026-05-20T09:22:20.455Z","canceledAt":null,"startDate":"2026-04-27","startDateResolution":null,"targetDate":null,"targetDateResolution":null,"priority":{"value":4,"name":"Low"},"labels":[],"initiatives":[],"lead":{},"status":{"id":"8703bdf7-c7c4-4c03-bb77-90f6d4163c6b","name":"Completed","type":"completed"},"teams":[{"id":"c20f56da-f121-4653-bf6c-dc1c8aac21c1","name":"Personal","key":"ABA"}]}],"hasNextPage":false}
```

> AGENT

This Layer-2 work lives in the Shaper pack (`agent-skills-shaper`), not drain-cycle. None of the open projects is a clean home — the execution skills shipped under the now-completed "Issues drain end-to-end" project, and the correctness project is Layer-1 only. I'll create it as an unscheduled Todo issue so you can slot it into a cycle deliberately rather than silently expanding scope.

> TOOL

tool_use mcp__claude_ai_Linear__save_issue
id: toolu_01DtKAhRfvkHhzMW26PJJ1Lp
```json
{
  "team": "Personal",
  "title": "exec:review — add reliability/resilience persona and fold in the outcome lens",
  "state": "Todo",
  "labels": [
    "repo:agent-skills-shaper"
  ],
  "priority": 3,
  "description": "## Context\n\nThe drain-cycle architecture redesign (vision/architecture §9–§11, design-decisions §20–§21) defines a Review-It phase whose goal is \"apply every quality lens systematically.\" Auditing `execution-review` against that goal surfaced two gaps in the persona set.\n\nToday `execution-review` ships three reviewer personas — spec-compliance, security-auditor, code-quality — dispatched in parallel on Claude Code workers, inline-sequential on non-Claude workers. The outcome check lives in a *separate* skill, `verify-implementation`.\n\n## What's missing\n\n1. **No reliability/resilience persona.** Nothing in the current set is oriented to failure modes, error handling, retries/idempotency, resource exhaustion, or degradation under load. These defects survive a green spec/security/quality review.\n2. **The outcome lens is a separate skill.** `verify-implementation` runs apart from the review fan-out, so the \"did it actually achieve the intended outcome\" check isn't part of the systematic lens sweep the Review-It goal calls for.\n\n## Scope\n\n- Add a `reliability-resilience` reviewer persona to `execution-review`, matching the existing persona contract (Claude-Code parallel dispatch / non-Claude inline-sequential).\n- Fold `verify-implementation`'s outcome check into `execution-review` as an outcome persona, so all lenses run under one fan-out and one verdict surface.\n- Keep the dual-dispatch behaviour and the handoff/verdict shape intact.\n\n## Done when\n\n- `execution-review` runs five lenses: spec-compliance, security, reliability/resilience, code-quality, outcome.\n- The outcome lens is reachable through `execution-review` rather than only as a standalone `verify-implementation` invocation.\n- Both dispatch paths (parallel on Claude Code, sequential elsewhere) carry the two new lenses.\n- Manual run against a real changeset emits findings from each of the five lenses.\n\n## Notes\n\n- Repo: `agent-skills-shaper`. Layer-2 (workflow pack) change — no drain-cycle code touched.\n- Relates to the phase-separation / multi-altitude-review design recorded in `drain-cycle/docs/design-decisions.md` §20–§21 and `architecture.md` §9, §11. The task-altitude lens list in §11 already names reliability/resilience and outcome as expected lenses."
}
```

> TOOL

tool_result
id: toolu_01DtKAhRfvkHhzMW26PJJ1Lp
```
{"id":"ABA-395","title":"exec:review — add reliability/resilience persona and fold in the outcome lens","description":"## Context\n\nThe drain-cycle architecture redesign (vision/architecture §9–§11, design-decisions §20–§21) defines a Review-It phase whose goal is \"apply every quality lens systematically.\" Auditing `execution-review` against that goal surfaced two gaps in the persona set.\n\nToday `execution-review` ships three reviewer personas — spec-compliance, security-auditor, code-quality — dispatched in parallel on Claude Code workers, inline-sequential on non-Claude workers. The outcome check lives in a *separate* skill, `verify-implementation`.\n\n## What's missing\n\n1. **No reliability/resilience persona.** Nothing in the current set is oriented to failure modes, error handling, retries/idempotency, resource exhaustion, or degradation under load. These defects survive a green spec/security/quality review.\n2. **The outcome lens is a separate skill.** `verify-implementation` runs apart from the review fan-out, so the \"did it actually achieve the intended outcome\" check isn't part of the systematic lens sweep the Review-It goal calls for.\n\n## Scope\n\n* Add a `reliability-resilience` reviewer persona to `execution-review`, matching the existing persona contract (Claude-Code parallel dispatch / non-Claude inline-sequential).\n* Fold `verify-implementation`'s outcome check into `execution-review` as an outcome persona, so all lenses run under one fan-out and one verdict surface.\n* Keep the dual-dispatch behaviour and the handoff/verdict shape intact.\n\n## Done when\n\n* `execution-review` runs five lenses: spec-compliance, security, reliability/resilience, code-quality, outcome.\n* The outcome lens is reachable through `execution-review` rather than only as a standalone `verify-implementation` invocation.\n* Both dispatch paths (parallel on Claude Code, sequential elsewhere) carry the two new lenses.\n* Manual run against a real changeset emits findings from each of the five lenses.\n\n## Notes\n\n* Repo: `agent-skills-shaper`. Layer-2 (workflow pack) change — no drain-cycle code touched.\n* Relates to the phase-separation / multi-altitude-review design recorded in `drain-cycle/docs/design-decisions.md` §20–§21 and `architecture.md` §9, §11. The task-altitude lens list in §11 already names reliability/resilience and outcome as expected lenses.","priority":{"value":3,"name":"Medium"},"url":"https://linear.app/ababushkin/issue/ABA-395/execreview-add-reliabilityresilience-persona-and-fold-in-the-outcome","gitBranchName":"anton/aba-395-execreview-add-reliabilityresilience-persona-and-fold-in-the","createdAt":"2026-06-15T11:57:59.522Z","updatedAt":"2026-06-15T11:57:59.522Z","archivedAt":null,"completedAt":null,"startedAt":null,"canceledAt":null,"dueDate":null,"slaStartedAt":null,"slaMediumRiskAt":null,"slaHighRiskAt":null,"slaBreachesAt":null,"slaType":"all","status":"Todo","statusType":"unstarted","labels":[],"attachments":[],"documents":[],"createdBy":"Anton Babushkin","createdById":"720d0535-dfc6-465f-8111-d1a3e6eab786","team":"Personal","teamId":"c20f56da-f121-4653-bf6c-dc1c8aac21c1"}
```

> AGENT

Created **[ABA-395](https://linear.app/ababushkin/issue/ababushkin/aba-395)** — *"exec:review — add reliability/resilience persona and fold in the outcome lens"* — Todo, Medium, unscheduled.

One thing to flag: the `repo:agent-skills-shaper` label didn't stick (it came back with no labels — that label probably doesn't exist in the workspace yet). Worth adding by hand, or I can retry with the right label name if you tell me what it is.

Let me record the issue in memory so it's not re-derived later.

> TOOL

tool_use Edit
id: toolu_01Rodq5ZMbdZ62FSH3c2yK5S
```json
{
  "replace_all": false,
  "file_path": "/Users/anton/.claude/projects/-Users-anton-src-drain-cycle/memory/north-star-design.md",
  "old_string": "- Review-pack gap found: `execution-review` ships spec/security/code-quality; Anton's target adds reliability/resilience persona + folds `verify-implementation` (outcome) in as a persona. Cheap L2 edit.",
  "new_string": "- Review-pack gap found: `execution-review` ships spec/security/code-quality; Anton's target adds reliability/resilience persona + folds `verify-implementation` (outcome) in as a persona. Cheap L2 edit in agent-skills-shaper. Ticketed as ABA-395 (Todo, unscheduled — slot into a cycle deliberately)."
}
```

> TOOL

tool_result
id: toolu_01Rodq5ZMbdZ62FSH3c2yK5S
```
The file /Users/anton/.claude/projects/-Users-anton-src-drain-cycle/memory/north-star-design.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Done. Summary:

- **Writing fix applied** — `vision.md` finding #1: the closing line now reads *"The connector verifies up the same hierarchy it broke the work down along"* (actor restored, nominalization gone). Findings #2 (`altitude` in vision) and #3 (`load-bearing` watchlist) are left for your call — #3 in particular matches existing house style across §13/§14, so I'd lean toward keeping it.
- **Linear issue** — [ABA-395](https://linear.app/ababushkin/issue/ababushkin/aba-395) created (Todo, unscheduled), capturing both Layer-2 changes: add the `reliability-resilience` persona to `execution-review` and fold `verify-implementation` in as the outcome lens. Left out of a cycle so you can slot it deliberately. The `repo:agent-skills-shaper` label didn't apply — add it by hand or give me the exact label name.
- **Memory** updated to point at ABA-395.

Doc changes remain uncommitted in the working tree. Want me to commit them?

> TOOL

tool_use Bash
id: toolu_01Mfz4NcKfM5GznrRbCYaXuP
```json
{
  "command": "git add docs/architecture.md docs/design-decisions.md docs/vision.md && git commit -m \"docs: add phase separation, control plane, and multi-altitude review\n\nGeneralize the execution unit from a cycle to any planned unit (cycle now,\nproject later), and record the redesign across the three north-star docs:\n\n- architecture: new §9 phase-per-worker separation, §10 resident control\n  plane, §11 multi-altitude review (task/milestone/project), §12 generic\n  execution unit; widen the known open seam to higher-altitude verdicts.\n- design-decisions: new §20-§22 with rationale and rejected alternatives.\n- vision: generalize the supervised unit and add verification that rolls\n  up the delivery hierarchy.\"",
  "description": "Stage the three docs and commit"
}
```

> TOOL

tool_result
id: toolu_01Mfz4NcKfM5GznrRbCYaXuP
```
ok 3 files changed, 105 insertions(+), 9 deletions(-)
ok 8dcfc46
```

> AGENT

Committed as `8dcfc46`.

One thing I noticed while staging that I want to flag rather than leave buried: the diff included a change at the top of `docs/architecture.md` that wasn't mine and looks like an accidental truncation —

```
-How `drain-cycle` is built to serve the vision. … [intro + design-decisions link]
-These section numbers are stable anchors — other docs cite them (e.g. `§8` …).
+Pre-read:[`docs/vision.md`](vision.md)).
```

That replacement dropped the doc's intro, the link to `design-decisions.md`, and the stable-anchors note (which the new §9–§12 rely on, since they cite `§2`/`§8`/etc.), and left a stray `)`. It's now committed as-is per your `/commit`. Want me to restore that header in a follow-up commit?
