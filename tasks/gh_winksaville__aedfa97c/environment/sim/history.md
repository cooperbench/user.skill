> DEVELOPER

reacquaint

> AGENT

Reacquainting — reading the todo intro and checking repo state.

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