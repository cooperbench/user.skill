> DEVELOPER

reacquaint

> AGENT

Reacquainting — reading the todo intro and checking repo state.

> TOOL

tool_use Read
id: toolu_019LAngcMeZvixQKA9767SDW
```json
{
  "file_path": "/home/<USER>/data/prgs/rust/zc-ring-x1/notes/todo.md",
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

> DEVELOPER

In the linux kernel io_uring how does it's API handle a full queue?

> AGENT

Short answer: io_uring has two rings with two different answers — the submission side pushes back on the caller, and the completion side buffers kernel-side rather than drop.

**Submission queue (SQ) full — caller's problem, fail fast:**
- Userspace is the producer of SQEs. In liburing, `io_uring_get_sqe()` simply returns `NULL` when there's no free SQE slot — no blocking, no queuing. The application's remedy is to call `io_uring_submit()` (i.e. `io_uring_enter()`) so the kernel consumes entries, then retry.
- Since 5.4-ish the kernel consumes SQEs immediately at submit time (they're copied out of the ring inside `io_uring_enter`), so SQ-full is transient by construction: submit drains it fully. With `SQPOLL`, the kernel thread drains asynchronously and userspace just waits for `khead` to advance.

**Completion queue (CQ) full — kernel buffers, never drops (modern behavior):**
- The CQ is sized 2× the SQ by default (tunable via `IORING_SETUP_CQSIZE`) since the kernel can generate completions faster than the app reaps (e.g. multishot ops).
- Originally (5.1–5.4) an overflowing completion was **dropped**, with the CQ ring's `overflow` counter incremented so the app at least knew it lost events.
- Since 5.5 (advertised by the `IORING_FEAT_NODROP` feature flag): when the CQ ring is full, the kernel […]

> DEVELOPER

Let's do #1 but I don't like terminology  "Descriptor queue endpoints" DescSender/DescReceiver
I think just Send and Receive and two variants of Send one requires the Msg to have an intrusive
link list and it cannot fail the other returns a Full error. Thoughts only.

> AGENT

Let me ground this in the design notes before opining.

> TOOL

tool_use Bash
id: toolu_01SSqHmJT5XKLYtudp8AmNxU
```json
{
  "command": "grep -n '^#' notes/ring-buffer-design.md | head -40",
  "description": "List headings in ring-buffer-design.md"
}
```

> TOOL

tool_result
id: toolu_01SSqHmJT5XKLYtudp8AmNxU
```
1:# Ring buffer design
16:## Goal
61:## Terminology
90:## Requirements
122:## Constraints
160:### Execution contexts
204:## Memory layout
216:#[repr(C, align(64))]
219:#[repr(C)]
316:## API
392:## Blocking and user words
433:## Validation
450:## MPSC ring (sibling primitive)
463:### MPSC protocol
511:### MPSC API: closure send
554:### Overflow readiness
579:### MPSC trust
597:### Fan-in (composition, not a mode)
616:### MPSC measurement plan
637:### MPSC open questions
655:## Messaging layer: pools and descriptor queues
675:### System model (overview)
757:### Layer requirements
775:### Provenance and descriptors
780:#### Offsets only, everywhere
786:#### Message provenance
795:#### Descriptors
803:#### Pool self-description
809:#### Pool-id resolution
816:#### Trust
823:### Descriptor and registry design (0.7.0)
895:### Free path: intrusive LIFO free-stack
926:### Pool topology and phasing
951:### Usage model: roles and buffer lifecycle
963:### Overflow FIFO (future)
987:### Prior art: iceoryx2
1010:### Open questions
1017:#### Pool-id allocation
1024:#### Setup plane
1031:#### Message header shape
```

> TOOL

tool_use Bash
id: toolu_01AZXxMkL8wJTHZMsjdvpgK3
```json
{
  "command": "sed -n '963,1010p' notes/ring-buffer-design.md",
  "description": "Read Overflow FIFO section of design notes"
}
```

> TOOL

tool_result
id: toolu_01AZXxMkL8wJTHZMsjdvpgK3
```
### Overflow FIFO (future)

When a queue's ring is Full, the sender appends the message to
a pending FIFO instead of failing — "send" then always
succeeds while pool memory lasts.

- **Intrusive, zero-allocation** — the FIFO links through the
  same embedded next-link offset the free-stack uses. A
  buffer is on at most one list at a time (free stack,
  pending FIFO, in flight in a ring, held by an owner), so
  one link field serves every state.
- **Sender-private** — the pending list belongs to the
  producer endpoint: head + tail offsets for O(1) append, no
  shared mutation, no CAS. Order discipline: the producer
  drains the FIFO oldest-first before ring-sending anything
  new, or FIFO order breaks. Draining happens on subsequent
  send attempts and/or an explicit flush.
- **Validated traversal** — the links live in shared pool
  memory a peer can scribble; the drainer bounds- and
  alignment-checks each offset as the free-stack popper does.
- **Naturally bounded** — messages come from pools, so the
  FIFO cannot outgrow total pool capacity; backpressure
  reappears as allocation failure rather than queue Full.

### Prior art: iceoryx2

[iceoryx2](https://github.com/eclipse-iceoryx/iceoryx2) is a
Rust-native zero-copy IPC library implementing most of this
layer: publishers […]

> TOOL

tool_use Bash
id: toolu_01JV7SMmBzwwgmiCPm4u4mv6
```json
{
  "command": "sed -n '823,962p' notes/ring-buffer-design.md",
  "description": "Read descriptor/registry design and usage model sections"
}
```

> TOOL

tool_result
id: toolu_01JV7SMmBzwwgmiCPm4u4mv6
```
### Descriptor and registry design (0.7.0)

The in-process slice as designed for the 0.7.0 cycle;
cross-process setup (mapping exchange, pool-id
coordination) remains in [Open questions](#open-questions).

- **`Desc { pool_id: u32, buf_idx: u32 }`** — 8 bytes, POD
  (zerocopy derives), so it rides any queue as an ordinary
  message. A buffer *index*, not a byte offset: the
  offsets-only rule bars pointers (per-process mappings),
  and an index is equally position-independent while
  matching what the free-stack and guards already speak;
  validation is one bounds check where a byte offset would
  also need a buffer-boundary divisibility check.
- **`PoolRegistry`** — per-process, fixed capacity
  (const-generic array; no_std, zero allocation).
  `register(resolver) -> PoolId` assigns the next slot
  index; phase 1 has no unregister, so ids never dangle.
  Sequential assignment produces cross-process id agreement
  only when one process assigns all ids — the in-process
  slice's case; cross-process will need registration under
  an externally agreed id (e.g. `register_at(id, ...)`),
  pending [Pool-id allocation](#pool-id-allocation).
- **`Pool::resolver() -> PoolResolver`** — a non-allocating
  view (header ref, buffer base, geometry) derived from the
  existing handle, so no second region borrow and no
  Stacked Borrows retag hazard (`init` takes the region
  pointer exactly once). Send + Sync: resolving mints
  guards […]

> AGENT

Thoughts, grounded in the design notes:

**Naming — agree, with one nit.** "Desc" leaks the wire format into the user-facing name; users think "I send a message," and the descriptor is how it travels, not what they care about. `Sender`/`Receiver` also matches every Rust channel convention (std, crossbeam, tokio), which buys free intuition. The nit: `Send` can't be a *type* name — it collides with the `Send` auto trait and would be genuinely painful (`impl Send for Send`...). So: types `Sender`/`Receiver`, methods `send`/`recv`. I'd guess that's what you meant anyway.

**Two send variants — the split is right, and Rust already has names for it.** `try_send() -> Result<(), Full>` for the fallible one and `send()` for the infallible one is exactly the std/tokio idiom (`try_` = won't block/park/spill, plain = always succeeds one way or another). The infallible one has a genuinely nice property worth stating in its doc: since the message was already allocated and the pending append is just link writes into memory you own, `send` consuming a `BufSlot` *cannot* fail — backpressure doesn't disappear, it moves to `alloc`, which is where a pool system wants it.

**The intrusive-link requirement may already be free.** Per the free-stack design, […]

> DEVELOPER

I'm thinking we do 1 & 2 as one ladder. I was looking at our SPSC it's slower than our MPSC implemenation and as line 142 of ring-buffer-design we "forbid concurrent access" that effect "Execution contexts" in addition the notion of using both try_send/send on the same SPSC requires a Mutex. I'm thinking we drop SPSC, at least for now, thoughts?

> DEVELOPER

I'm thinking we do 1 & 2 as one ladder. Also, I was looking at our SPSC and as line 142 of ring-buffer-design says "SPC roles forbid concurrent access" that complicates "Execution contexts" and in addition the notion of using both try_send/send on the same SPSC requires a Mutex. I'm thinking we drop SPSC, thoughts?

> AGENT

Let me re-read the constraints and execution-contexts sections before weighing in.

> TOOL

tool_use Bash
id: toolu_01L8AzWPxN9zcVpkMkY4BWmK
```json
{
  "command": "sed -n '122,215p' notes/ring-buffer-design.md",
  "description": "Read Constraints and Execution contexts sections"
}
```

> TOOL

tool_result
id: toolu_01L8AzWPxN9zcVpkMkY4BWmK
```
## Constraints

- **Slot geometry: M slots × N bytes** — the ring holds M
  [slots](#terminology) of N bytes each.
  - M (capacity) is a power of two — index wrapping is a
    mask, no division; checked at construction.
  - N (slot size) is a multiple of the cache-line size, and
    each slot is cache-line aligned — adjacent slots never
    share a line, and any `T` with `align_of::<T>()` up to
    the line size fits without padding logic.
  - This trades space for isolation (a 16-byte message
    occupies a full 64-byte slot) — the right default for
    IPC; a packed-slot variant is a possible follow-on.
- **Monotonic indices** — producer/consumer indices are
  free-running unsigned counters (wrap via masking), so
  full/empty are distinguishable without a separate flag or
  a sacrificial slot.
- **Cache-line separation** — producer- and consumer-owned
  indices are padded/aligned to separate cache lines to avoid
  false sharing.
- **SPSC roles forbid concurrent access, not multiple
  owners** — the single-producer and single-consumer contract
  is "at most one accessor in an endpoint at a time," a
  *serialization* requirement via a serializer/mutex-type
  entity, not a fixed thread identity.
  How threads and ISRs each satisfy it is
  [Execution contexts](#execution-contexts).
- […]

> TOOL

tool_use Bash
id: toolu_019baPASTwLpCCX3HLAG6Y6k
```json
{
  "command": "ls src/ src/bin 2>/dev/null; grep -rln 'mpsc\\|Mpsc' src/ --include='*.rs' | head",
  "description": "List source files and find MPSC implementation files"
}
```

> TOOL

tool_result
id: toolu_019baPASTwLpCCX3HLAG6Y6k
```
src/:
bin
lib.rs
mpsc
policy.rs
pool
registry.rs
spsc

src/bin:
zc-ring-x1-demo.rs
src/lib.rs
src/mpsc/v0/consumer.rs
src/bin/zc-ring-x1-demo.rs
src/mpsc/mod.rs
src/pool/v0/mod.rs
src/mpsc/v0/mod.rs
src/mpsc/v0/producer.rs
```

> AGENT

Thoughts — I land close to you, with one hinge question you should decide explicitly.

**The case for dropping SPSC is stronger than the two reasons you gave.** Your measurements already made the third and biggest one: cross-core, SPSC moves ~10.0 cache lines per round trip vs MPSC's ~6.7 and loses by ~26–40% (that's what spawned todo #3, the seam-word variant). So SPSC's remaining justification is only (a) the SMT/same-core win where transfers ≈ 0, and (b) the load-store-only floor. It's not "simpler and faster with a concurrency restriction" — it's *slower* in the deployment shape that matters and restricted.

**Your execution-contexts point is real and generalizes.** With MPSC, the whole gnarly half of that section evaporates: "threads sharing an endpoint" (mutex) and "ISR sharing an endpoint" (irqsave + try-and-bail) both exist only because SPSC has exactly one producer slot. MPSC's answer is uniform: every context — each thread, each ISR — gets its *own* Sender, and the CAS claim serializes them lock-free. The section shrinks to "one endpoint per context; done."

**One correction on the mutex claim, which actually strengthens the MPSC case.** `try_send`/`send` on one SPSC sender doesn't itself need a mutex — a sole-owner thread can call […]

> DEVELOPER

M0 could work if we added an optional Mutex or DI/EI (as a brute force CAS fn/macro)

> AGENT

Agreed — that closes the hinge, and it's a well-trodden path in embedded Rust rather than an invention. Thoughts on the shape of it:

**The ecosystem already packaged this exact idea: `portable-atomic`.** It's a drop-in for `core::sync::atomic` that compiles to native atomics on targets that have them (zero cost on x86/ARMv7+) and, on thumbv6m, implements `compare_exchange` via exactly your DI/EI brute force — either `unsafe-assume-single-core` (raw cpsid/cpsie) or the `critical-section` crate for boards where DI alone isn't enough. That last case matters: the flagship no-CAS chip today is the RP2040, which is *dual-core* M0+, where DI/EI on one core doesn't serialize the other — critical-section there is backed by the chip's hardware spinlocks. A hand-rolled DI/EI macro gets single-core M0 right and dual-core M0 silently wrong; portable-atomic gets both. Its atomic types are documented same-size/same-align as the underlying integers, so the shared-memory `#[repr(C)]` header layout is unaffected.

**Correctness argument is sound for the single-core case:** on one core, only an interrupt can preempt, so a DI-bracketed load-compare-store *is* atomic against every observer that exists. The critical section is a handful of instructions, so the "no longer lock-free" cost is a bounded few-cycle IRQ latency bump — the embedded world's standard […]

> DEVELOPER

RP2040 is definitely a target in my mind, does the RISC-V CPUs have CAS?

> AGENT

Mostly yes, with an important asterisk: RISC-V atomics are an optional extension (the "A" in a name like RV32IMAC), and the base ISA has none.

- **How it works when present:** the A extension gives LR/SC (load-reserved/store-conditional) plus fetch-and-op AMOs. RISC-V historically has *no* native CAS instruction — `compare_exchange` is synthesized from an LR/SC loop by the compiler, which is fine and is exactly what Rust/LLVM emits. (A true `amocas` instruction only arrived with the Zacas extension, ratified 2023, rare in silicon so far.)
- **The chip you probably care about — RP2350 (Pico 2):** its Hazard3 cores are RV32IMAC — A extension present, so CAS works natively in both its RISC-V mode and its Cortex-M33 mode (ARMv8-M has ldrex/strex). So across the Pico line, the RP2040 is the *only* no-CAS part, and portable-atomic + the RP2040 critical-section impl (hardware spinlocks, dual-core-correct) covers it.
- **Where the asterisk bites elsewhere:** plenty of small RISC-V parts omit A. ESP32-C3 is RV32IMC (no atomics; the C6 added A); the ultra-cheap CH32V003 is RV32EC. portable-atomic handles those the same way it handles thumbv6m — critical-section fallback — so the story stays uniform: native atomics where the ISA has them, DI/EI-style emulation where it […]