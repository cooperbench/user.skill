> DEVELOPER

reacquaint

> AGENT

Reacquainting — reading the todo intro and checking repo state.

> TOOL

tool_use Read
id: toolu_019LAngcMeZvixQKA9767SDW
```json
{
  "file_path": "/home/wink/data/prgs/rust/zc-ring-x1/notes/todo.md",
  "offset": 0,
  "limit": 60
}
```

> TOOL

tool_result
id: toolu_019LAngcMeZvixQKA9767SDW
```
0	# Todo
1	
2	This file uses [Prose form](../AGENTS.md#prose-form). It
3	contains near term tasks with a short description and
4	uses links or reference links for more details.
5	
6	## In Progress
7	
8	_No cycle currently in progress._
9	
10	## Todo
11	
12	 Entries are in **strict priority rank** — #1 highest,
13	 descending. Reprioritize by moving an entry, then
14	 `vc-x1 fix-todo --no-dry-run notes/todo.md` to renumber.
15	 The numbers are positional rank, not stable IDs — to refer
16	 to a Todo, name it by its **title** (a greppable mention;
17	 a numbered list item has no anchor to link to), not its
18	 number. Long-tail entries
19	 live in [todo-backlog.md](todo-backlog.md). Use the
20	 [Prose Form in AGENTS.md](../AGENTS.md#prose-form); deeper
21	 detail goes in `notes/chores/chores-NN.md` design
22	 subsections (link via `[N]` ref).
23	
24	1. Descriptor queue endpoints: paired DescSender (loan +
25	   send) / DescReceiver (recv) [[11]]:
26	   - own ring endpoint + registry access;
27	   - the demo's ~20-line send path becomes ~3 lines;
28	   - `resolve`'s unsafe is audited once inside the crate
29	     (recv safe by construction);
30	   - guard handed back on Full;
31	   - design […]

> TOOL

tool_use Bash
id: toolu_01Tp2RDPyzqTZYewCrg2d3Aj
```json
{
  "command": "jj st -R .",
  "description": "Show app repo working copy status"
}
```

> TOOL

tool_result
id: toolu_01Tp2RDPyzqTZYewCrg2d3Aj
```
The working copy has no changes.
Working copy  (@) : tpqrqsuk 655069ca (empty) (no description set)
Parent commit (@-): vnnyltum 6964dd17 main | feat: tp-matrix perf counters + tables
```

> AGENT

Reacquainted. Here's where things stand:

**Repo state:** Clean working copy, `@` empty on top of `main` at `6964dd17 feat: tp-matrix perf counters + tables`. No cycle in progress (`## In Progress` is empty).

**Recent work** (from git log): the tp-matrix series just landed — perf counter module, cells bin + tables, README + verification, clap help + banner, and finally perf counters + tables.

**Top of the ranked Todo:**
1. **Descriptor queue endpoints** — paired DescSender (loan + send) / DescReceiver (recv); collapses the demo's ~20-line send path to ~3 lines, audits `resolve`'s unsafe once inside the crate, designed against both SPSC + MPSC; also the future home of per-sender overflow pending lists.
2. **Overflow FIFO** — on ring Full, append to a sender-private intrusive pending list (zero-alloc, bounded by pool capacity).
3. **Seam-word SPSC variant** — per-slot seq words so neither side reads the other's index line (load/store only, no CAS); must keep the SMT/1t win; needs A/B measurement with tp_roundtrip before adopting.
4. **Batch alloc/free demo** — alloc X then free all, pool vs global allocator.

Ready to pick something up — #1 (descriptor queue endpoints) is the top-ranked item if you want to start a cycle there.