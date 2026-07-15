> DEVELOPER

reaquaint and let's do todo 3 Exp[lore why zcr-mpsc-2t is faster than zcr-with-2t for that I want to use TProbe & TProbe2 in ../iiac-perf/src/tprobe.rs and tprobe2.rs as appropriate if you think they'll help.

> AGENT

Now let me read the ring implementations.

> AGENT

The gap reproduces at 10s: SPSC adjusted mean 131.5 ns vs MPSC 93.9 ns. Now let me check perf counters availability and the CLI's pinning flags.

> AGENT

While the perf matrix runs, let me write the TProbe-instrumented bench variants in iiac-perf.

> AGENT

I've stopped — the write of the new bench file into `../iiac-perf/src/benches/` was rejected, so I haven't made any changes to either repo.

Where things stand so far (read-only exploration done):

- **Gap reproduces at 10s, unpinned**: `zcr-with-2t` adjusted mean 131.5 ns vs `zcr-mpsc-2t` 93.9 ns (core z..n2 means: 122.0 vs 87.1). Same sign and similar magnitude as the recorded 300s numbers.
- **perf counters are available**: Zen 2's `ls_refills_from_sys.ls_mabresp_lcl_cache` (demand fills from another core's cache) is a direct cross-core line-transfer counter. A 6-run matrix (both benches × pin 0,1 same-CCX / pin 0,3 cross-CCX / unpinned) just finished in the scratchpad; I haven't analyzed it yet.
- **My plan for TProbe/TProbe2**: add `tp-zcr-with-2t` / `tp-zcr-mpsc-2t` benches to iiac-perf, one `TProbe` per protocol phase (main send/recv, worker recv/send, worker probes returned via `JoinHandle`), mirroring the existing `probe-mpsc-2t` + `tp-pc` patterns. I was about to write the first of those files when you interrupted. My take on TProbe2: not a fit here — its record buffer grows unbounded (~70M round-trips × 24 B ≈ multi-GB over a 10s+ run) and its report currently merges all sites into one histogram, so it can't separate phases anyway.

How would you like me to […]

> DEVELOPER

I wanted to know the plan and I'm thinking I'd like the test here in zc-ring-x1 so we have
the reproducible information. Also, if you didn't think TProbe2 was suitable why would you
create a new bench that looked like you were going to use it?

> AGENT

Fair on both counts — let me answer the TProbe2 question directly, then re-plan for the test living here.

On TProbe2: I never intended a TProbe2 bench. The file I started, `tp_zcr_with_2t.rs`, uses only `TProbe` — the `tp-` prefix copied the existing `tp-pc` bench's naming (which is the TProbe variant; `tp2-pc` is the TProbe2 one). So the name signaled "TProbe", not "TProbe2" — but I should have led with that conclusion before writing code: **TProbe fits, TProbe2 doesn't**, because TProbe2's record buffer grows unbounded (tens of millions of round trips × 24 B = GBs in a 10s run) and its `report` currently drains all sites into a single histogram, so it can't separate phases anyway. Its strength (record-order preservation, interleaved scopes) isn't what this question needs.

Let me check whether iiac-perf exposes a library target so a test here can use TProbe directly.

> AGENT

The perf-counter matrix already gives strong evidence for the hypothesis. Cross-core cache-line fills (`ls_mabresp_lcl_cache`, demand fills served from another core's cache) per round trip:

| placement | zcr-with-2t | zcr-mpsc-2t |
|---|---|---|
| pin 0,1 (same CCX) | 10.3 | 7.2 |
| pin 0,3 (cross CCX) | 10.2 | 7.0 |
| unpinned | 10.2 | 7.1 |

SPSC pays ~3 more cross-core line transfers per round trip (~1.5 per handoff), rock-steady across placements — consistent with the chores hypothesis that SPSC bounces both index lines per handoff while MPSC's only bouncing hot word is the seq line. (The absolute counts are higher than the naive 2-vs-1 accounting because each spin-poll after an invalidation refetches the line; the *ratio* ~10:7 ≈ the ~26% latency gap.)

**Revised plan — the probe test lives in zc-ring-x1:**

TProbe is the right instrument (TProbe2 ruled out as explained above). But TProbe lives in iiac-perf, which is binary-only, so step 1 enables reuse:

1. **iiac-perf cycle (small)**: add a `[lib]` target — `src/lib.rs` exposing `tprobe`, `tprobe2`, `ticks`, `band_table` (and their module deps); `main.rs` consumes the lib. No behavior change to the CLI.
2. **zc-ring-x1 cycle (todo 3, 0.13.0)**:
   - `[dev-dependencies] iiac-perf = { path […]

> DEVELOPER

How hard would it be to create a "trivial" bench and tprobe mod/lib here such that
it would be "easy" to refactor them into reusable entities in the future?

> AGENT

Let me size up what a minimal local version would actually need from iiac-perf.

> AGENT

Very tractable — the dependency closure of `TProbe` is small and nearly self-contained.

**What a local copy needs** (from iiac-perf, mostly verbatim):

- `tprobe.rs` — 64 lines (`TProbe2` is another 130 if we want it along for completeness, though it's not needed for this exploration).
- `ticks.rs` + `ticks/x86_64.rs` (+ `aarch64.rs` if kept) — ~130–190 lines (rdtsc read, calibration, `require_ok`).
- `band_table.rs` + `bands.rs` — ~390 lines (the report renderer), plus two tiny `fmt_commas` helpers it pulls from `harness.rs`.
- One external dep: `hdrhistogram`.

So ~650 lines, almost all copy-paste, no entanglement with iiac-perf's harness/calibration machinery.

**The "trivial" bench** is genuinely trivial: a fixed-duration loop around the round-trip (no adaptive inner-sizing, no overhead calibration — we're comparing phases A/B under identical framing, so absolute framing subtraction doesn't matter), four TProbes, `--duration`/`--pin`-style args. ~200 lines as an example or bin here.

**Structure for easy future extraction** — my recommendation: a small local crate in this repo, e.g. `tprobe/` (own `Cargo.toml`, depends only on `hdrhistogram`), with zc-ring-x1 taking it as a **path dev-dependency**. Two properties make the future refactor easy:

- It's already a crate with a clean boundary — "reusable entity" later means moving the directory out (or publishing it) and […]

> DEVELOPER

Yes, proceed with the local tprobe crate plan

> AGENT

Here's the proposed cycle plan and ladder before I touch anything.

**Cycle: `0.13.0` — pick up Todo #3** (explore why zcr-mpsc-2t measures faster than zcr-with-2t)

**Chores / close-out title** (anticipated): `perf: explore spsc vs mpsc 2t gap`

**Problem statement** (for `## In Progress`): At 1p/1c cross-thread, the MPSC ring measures ~26% faster than SPSC (73.9 vs 100.1 ns adjusted at 300s). We think SPSC bounces two index cache lines per handoff while MPSC's only shared hot word is the slot seq. Verify with cross-core cache-fill counters and a phase-probed round trip, from this repo so the measurement is reproducible here.

**Ladder** (stem: `2t gap`):

1. `0.13.0-0` — `docs: 2t gap exploration plan` — Preparation: bump version-of-record, move Todo #3 into `## In Progress`, open the chores section.
2. `0.13.0-1` — `feat: 2t gap tprobe dev crate` — local `tprobe/` crate (verbatim-as-possible copies of iiac-perf 0.20.0's `tprobe.rs`, `tprobe2.rs`, `ticks/`, `band_table.rs`, `bands.rs` + the two `fmt_commas` helpers; dep: `hdrhistogram` only; provenance noted in module docs). Root `Cargo.toml` gains `[workspace] members = ["tprobe"]` and the path dev-dependency.
3. `0.13.0-2` — `feat: 2t gap probed roundtrip example` — `examples/tp_roundtrip.rs`: the same 1p/1c round trip as the iiac-perf benches, SPSC and MPSC flavors, four TProbes […]

> DEVELOPER

Add that to todo as the In Progess item with detils in chores

> AGENT

Now making the Preparation edits: version bump, todo.md, chores section.

> AGENT

Now the chores section with the details.

> AGENT

Preparation work for `0.13.0-0` is complete:

- `Cargo.toml` / `Cargo.lock`: version-of-record → `0.13.0-0`.
- `notes/todo.md`: Todo #3 moved into `## In Progress` (bold title, problem statement, 5-step ladder, `-0` marked `(current)`); remaining entries renumbered via `vc-x1 fix-todo`.
- `notes/chores/chores-02.md`: opened `## perf: explore spsc vs mpsc 2t gap` with empty `Commits:`, the full plan details (local tprobe crate rationale, TProbe2 exclusion, example shape, measurement matrix), and a `### Preliminary evidence` subsection recording today's exploratory counter table (10.2–10.3 vs 7.0–7.2 fills/round-trip) and the 10 s repro; new ref `[6]` → chores-01's 2t-surprise outcome.

Ready to commit. Please review.

> DEVELOPER

commit using `vc-x1 push ..`

> AGENT

Running the validation (cargo cycle) before the description review.

> AGENT

Validation clean — fmt, clippy (no warnings), 40 tests pass.

Proposed commit description for the `0.13.0-0` push:

**Title**

```
docs: 2t gap exploration plan
```

**Body**

```
Open the 0.13.0 cycle: pick up the "explore why zcr-mpsc-2t
measures faster than zcr-with-2t" Todo.

- Cargo.toml: version-of-record 0.12.0 -> 0.13.0-0
- Cargo.lock: version sync
- notes/todo.md: Todo #3 -> ## In Progress (problem statement
  + 0.13.0 ladder, -0 current); remaining entries renumbered
- notes/chores/chores-02.md: open "perf: explore spsc vs mpsc
  2t gap" — plan details (local tprobe dev crate, phase-probed
  roundtrip example, measurement matrix) + preliminary
  cross-core fill-counter evidence (spsc ~10.2 vs mpsc ~7.1
  fills/round-trip)
```

(`ochid:` trailer injected by `vc-x1 push` itself.)

Since the diff review happened here in conversation, I'll invoke it as `vc-x1 push main --from message --title ... --body ...` (skips the interactive gate; preflight already run by hand above). OK to push?

> DEVELOPER

go

> AGENT

landed

> DEVELOPER

Continue with 0.13.0-1, the tprobe dev crate

> AGENT

Starting `0.13.0-1`. First, read the iiac-perf sources to copy.

> AGENT

Now building the crate. First, ladder bookkeeping and remaining file reads.

> DEVELOPER

I want to be sure you were going to stop and get approval before committing (vc-x1 push) but
also, I'd like to rename TProbe2 so maybe TProbeSpan or ... thoughts, no actions.

> AGENT

Yes — I was stopping: the ladder flip + chores correction were the last edits of the `0.13.0-1` work, and the next thing out of me was going to be "ready to commit, please review." No `vc-x1 push` without your go.

On renaming `TProbe2` — thoughts only:

**The "2" is worth killing.** It names the order of invention, not the semantics, and every reader has to go find out what "2" means. Now is the cheapest moment ever to rename: the crate is one uncommitted commit old and nothing depends on it (the `-2` example only uses `TProbe`).

**Candidates:**

- **`TProbeSpan`** — my pick. "Span" is exactly the right word: the start/end interval vocabulary from tracing, and non-stack interleaving (which this supports by construction) is span-like, not scope-like. Keeping the `TProbe` prefix groups the two types in autocomplete/greps and reads as "the span-recording flavor of TProbe". The handle type falls out nicely: `TProbe2RecId` → `TProbeSpanId`, and `let span = p.start(site); … p.end(span);` reads naturally.
- **`TSpanProbe`** — grammatically more precise (the object *is* a probe that collects spans; a `TProbeSpan` arguably names the span, not the probe). Costs the shared prefix. If you value strict noun accuracy over grouping, this […]

> DEVELOPER

Rename to TProbeSpan and fold it into -1

> AGENT

Rename folded in and validation is green (fmt, clippy, 4 + 40 tests). The `0.13.0-1` work is complete:

- **`tprobe/` crate** (new): `lib.rs` (provenance + documented deltas), `fmt.rs`, `ticks.rs` + `ticks/{x86_64,aarch64}.rs`, `band_table.rs`, `tprobe.rs`, `tprobe_span.rs` — copied from iiac-perf 0.20.0. Deltas, all recorded in `lib.rs`: fmt helpers into their own module, "iiac-perf" strings → "tprobe", broken cross-repo doc links → plain text, `// OK:` + missing `///` per repo conventions, and **`TProbe2` → `TProbeSpan`** (`TProbe2RecId` → `TProbeSpanId`, file → `tprobe_span.rs`, report label → `"tprobe-span"`).
- **Root `Cargo.toml`**: version → `0.13.0-1`, `[workspace] members = ["tprobe"]`, `tprobe` path dev-dependency (+ `Cargo.lock`).
- **`notes/todo.md`**: `-0` → done, `-1` → current→done at commit.
- **`notes/chores/chores-02.md`**: plan bullet corrected (dependency closure: `minstant` in, `bands.rs` out) and the rename + rationale recorded.

Ready to commit. Please review.

> DEVELOPER

I see you're following the convention that was in tprobe of documenting the history in the doc comments,
let's not do that, that belongs in chores. Also, the goal of "verbatim as possible" from iiac-perf isn't
the goal. This is a new crate and the goal is to make it "trivial/simple" but adequate leveraging
iiac-perf where appropriate. Update as needed.

> AGENT

Reworking to the new goal: no history in doc comments (chores carries provenance), and simplify where it helps — which also lets me drop the `minstant` dependency (its only uses were the 10 ms calibration anchor, replaceable by `std::time::Instant`, and a kernel-clocksource check that's a one-line sysfs read).

> AGENT

Now rewriting the chores bullet — provenance and deltas belong there:

> AGENT

Reworked per your direction — all history/provenance is out of the code and in chores:

- **Doc comments**: `lib.rs` now just describes what the crate is; `fmt.rs`, `tprobe.rs`, `tprobe_span.rs` docs describe the primitives on their own terms (no iiac-perf references, no delta lists). "Scope" wording → "span" throughout `tprobe_span.rs`.
- **Simplification win**: `minstant` dependency dropped entirely — calibration anchors on `std::time::Instant` (negligible overhead over the 10 ms window), and the kernel-clocksource check is a direct sysfs read (`current_clocksource == "tsc"`, same thing minstant checked). Sole dep is now `hdrhistogram`; `Cargo.lock` no longer contains minstant.
- **Chores** (`chores-02.md`): the tprobe bullet rewritten — new-crate framing ("trivial/simple but adequate, leveraging iiac-perf"), with the full delta list (rename, minstant drop, bands.rs exclusion, doc rewording, conventions) recorded there.

Validation green: fmt, clippy `-D warnings`, 4 + 40 tests pass.

Ready to commit `0.13.0-1`. Please review.

> DEVELOPER

commit using `vc-x1 push ..`

> AGENT

Proposed commit description for `0.13.0-1`:

**Title**

```
feat: 2t gap tprobe dev crate
```

**Body**

```
New local dev crate with hardware tick-counter probes (TProbe /
TProbeSpan), derived from iiac-perf 0.20.0 but simplified — a
new crate, not a copy; provenance and deltas recorded in
chores-02.

- tprobe/Cargo.toml: new crate manifest; sole dep hdrhistogram
- tprobe/src/lib.rs: crate doc, module decls, re-exports
- tprobe/src/fmt.rs: thousands-separator formatting helpers
- tprobe/src/ticks.rs: per-arch tick-counter abstraction
- tprobe/src/ticks/x86_64.rs: rdtsc + invariant-TSC check;
  calibration anchored on std::time::Instant and kernel
  clocksource checked via sysfs (no minstant dep)
- tprobe/src/ticks/aarch64.rs: CNTVCT_EL0 / CNTFRQ_EL0
- tprobe/src/band_table.rs: percentile band-table renderer
- tprobe/src/tprobe.rs: TProbe direct-record histogram probe
- tprobe/src/tprobe_span.rs: TProbeSpan start/end span probe
  (renamed from iiac-perf's TProbe2) + unit tests
- Cargo.toml: version 0.13.0-1; [workspace] members; tprobe
  path dev-dependency
- Cargo.lock: sync
- notes/todo.md: ladder -0 -> done, -1 -> done
- notes/chores/chores-02.md: tprobe plan bullet rewritten to
  the new-crate goal with the delta list (TProbeSpan rename,
  minstant drop, bands.rs exclusion, doc/convention deltas)
```

OK to push?

> DEVELOPER

go

> AGENT

landed

> DEVELOPER

Actually where is the local repo for the new code, I don't see it?

> AGENT

There's no separate repo — `tprobe/` is a subdirectory crate *inside* the zc-ring-x1 repo, at `/home/wink/data/prgs/rust/zc-ring-x1/tprobe/`. It's a Cargo **workspace member** (root `Cargo.toml` has `[workspace] members = ["tprobe"]` plus the path dev-dependency), not a new git/jj repo.

It was committed and pushed as part of `0.13.0-1` — the diff stat above shows all 9 `tprobe/` files in that commit on `main`.

That matches the plan we discussed: a *crate* boundary (own `Cargo.toml`, own `src/`) so a future extraction into its own repo is a directory move, but living in this repo for now so the measurement tooling is reproducible from here. If you'd rather it be its own repo already, that's a different setup — say the word.

> DEVELOPER

Got it, I was gone and I looked and thought you hadn't pushed and then didn't see any changes and was confused. So continue -2

> AGENT

It runs. Let me see the full output for both flavors:

> AGENT

The decomposition already localizes the gap — SPSC's send phases cost ~45 ns each vs MPSC's ~12 ns. Validating now:

> AGENT

`0.13.0-2` work is complete:

- **`examples/tp_roundtrip.rs`** (new): phase-probed 1p/1c round trip, SPSC and MPSC flavors over two rings each. Four `TProbe`s per flavor (main send, worker recv, worker send, main recv — reported in trip order), worker probes returned through the scoped-thread join. CLI: `[spsc|mpsc|both] [-d secs] [--pin main,worker] [-t]`. The two flavors share a generic `drive` loop (wall-clock checked every 4096 iterations to keep `Instant::now` off the hot path); shutdown via a `STOP` sentinel. Uses scoped threads over stack regions — no leaking needed, unlike the iiac-perf benches.
- **`Cargo.toml`**: version → `0.13.0-2`.
- **`notes/todo.md`**: `-2` marked done.

Validation: fmt, clippy `-D warnings`, all 5 test targets ok, `cargo install` replaced the demo at `0.13.0-2`.

And the 2 s smoke run already answers the "where" question cleanly, unpinned: **SPSC's send phases cost ~45 ns each; MPSC's ~12 ns** (recv waits: ~100 vs ~66 ns, mostly just absorbing the other side's half-trip). Both SPSC sends together are ~66 ns/round-trip more expensive than MPSC's — matching the SPSC producer having to read the peer-written index line (and commit to a line the peer is polling) where the MPSC producer's claim is core-local. The full measurement matrix + written findings are `-3`. […]