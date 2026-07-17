> DEVELOPER

I ran iiac-perf a bunch of times and the framing/sample time is moving quite a bit, but the loop/iter is steady. Your opinion

> DEVELOPER

I ran iiac-perf a bunch of times and the framing/sample time is moving quite a bit,
but the loop/iter is steady. I just grabbed those first few lines of each run. Your opinion

wink@3900x 26-07-08T15:16:18.605Z:~/data/prgs/rust/iiac-perf (main+1)
$ iiac-perf mpsc-1t
iiac-perf 0.20.0 — Rust latency microbenchmark harness

Calibration:
  framing/sample      11.12 ns  (timer pair, two-point fit)
  loop/iter            0.49 ns  (per inner-loop iteration)

wink@3900x 26-07-08T15:16:25.892Z:~/data/prgs/rust/iiac-perf (main+1)
$ iiac-perf mpsc-1t
iiac-perf 0.20.0 — Rust latency microbenchmark harness

Calibration:
  framing/sample      21.22 ns  (timer pair, two-point fit)
  loop/iter            0.49 ns  (per inner-loop iteration)

wink@3900x 26-07-08T15:16:32.318Z:~/data/prgs/rust/iiac-perf (main+1)
$ iiac-perf mpsc-1t
iiac-perf 0.20.0 — Rust latency microbenchmark harness

Calibration:
  framing/sample      21.22 ns  (timer pair, two-point fit)
  loop/iter            0.49 ns  (per inner-loop iteration)

wink@3900x 26-07-08T15:16:38.857Z:~/data/prgs/rust/iiac-perf (main+1)
$ iiac-perf mpsc-1t
iiac-perf 0.20.0 — Rust latency microbenchmark harness

Calibration:
  framing/sample      11.22 ns  (timer pair, two-point fit)
  loop/iter            0.49 ns  (per inner-loop iteration)

wink@3900x 26-07-08T15:16:45.466Z:~/data/prgs/rust/iiac-perf (main+1)
$ iiac-perf mpsc-1t -d 1
iiac-perf 0.20.0 — Rust latency microbenchmark harness

Calibration:
  framing/sample      11.22 ns  (timer pair, two-point fit)
  loop/iter            0.49 ns  (per inner-loop iteration)

wink@3900x 26-07-08T15:16:53.466Z:~/data/prgs/rust/iiac-perf (main+1)
$ iiac-perf mpsc-1t -d 1
iiac-perf 0.20.0 — Rust latency microbenchmark harness

Calibration:
  framing/sample       1.02 ns  (timer pair, two-point fit)
  loop/iter            0.49 ns  (per inner-loop iteration)

wink@3900x […]

> AGENT

The quantized values (1.02, 11.12, 11.22, 21.22 — steps of ~10 ns) are a strong clue. Let me look at how the framing calibration is computed.

> TOOL

tool_use Bash
id: toolu_01UfvX8Zd9Lso65djsthkGYH
```json
{
  "command": "grep -rn \"framing\" --include=\"*.rs\" -l /home/<USER>/data/prgs/rust/iiac-perf/src | head",
  "description": "Find files mentioning framing"
}
```

> TOOL

tool_result
id: toolu_01UfvX8Zd9Lso65djsthkGYH
```
/home/<USER>/data/prgs/rust/iiac-perf/src/overhead.rs
/home/<USER>/data/prgs/rust/iiac-perf/src/benches/tp_pc.rs
/home/<USER>/data/prgs/rust/iiac-perf/src/main.rs
/home/<USER>/data/prgs/rust/iiac-perf/src/harness.rs
```

> TOOL

tool_use Read
id: toolu_01PUGvmyUrrJ4F124y4F3U1U
```json
{
  "file_path": "/home/<USER>/data/prgs/rust/iiac-perf/src/overhead.rs"
}
```

> TOOL

tool_result
id: toolu_01PUGvmyUrrJ4F124y4F3U1U
```
1	//! Apparatus-overhead calibration. Fits a two-point line through an
2	//! empty bench at two `inner` sizes (`N_LOW`, `N_HIGH`) to separate
3	//! per-sample timer-pair framing from per-iteration loop cost.
4	
5	use std::hint::black_box;
6	use std::time::{Duration, Instant};
7	
8	use crate::harness::Bench;
9	
10	/// Calibration warmup iterations — long enough for CPU frequency
11	/// boost to ramp before the first `min_low` measurement.
12	pub const CAL_WARMUP: u64 = 100_000;
13	
14	/// Samples per `measure()` call; the reported minimum approaches
15	/// the hardware floor as samples grow.
16	pub const CAL_SAMPLES: u64 = 100_000;
17	
18	/// Inner-loop count for the low-N calibration point.
19	pub const N_LOW: u64 = 100;
20	
21	/// Inner-loop count for the high-N calibration point. A wide spread
22	/// (`N_HIGH / (N_HIGH - N_LOW) ≈ 1.01`) keeps noise amplification on
23	/// the fitted framing small — the 0.6.0 fix for framing instability.
24	pub const N_HIGH: u64 = 10_000;
25	
26	/// Apparatus-overhead model fitted by [`calibrate`]. Bench code uses
27	/// [`Overhead::per_call_ns`] to subtract per-call overhead from
28	/// reported latencies.
29	#[derive(Debug)]
30	pub struct Overhead {
31	    /// Fixed per-sample timer-pair […]

> AGENT

This is timer quantization, not real drift — and the math in `overhead.rs` explains both halves of what you're seeing.

Look at the framing values you got: **1.02, 11.12, 11.22, 21.22 ns**. They're not wandering continuously — they sit on a lattice with ~10.1 ns spacing (one, sometimes two steps apart). That's the signature of the TSC's effective granularity on your 3900X: `minstant` reads the TSC, and on Zen 2 the TSC is derived from the 100 MHz reference clock, so elapsed-time readings effectively quantize to ~10 ns steps. (We think that's the mechanism; the 10.1 ns lattice in your data is the observation.)

Now trace it through the fit in `src/overhead.rs:85-90`:

- `min_low` is the minimum elapsed time for `inner = 100` empty iterations — a true duration of ~50-60 ns, which the timer can only report as a multiple of the ~10 ns quantum. Which quantum you land on depends on the phase alignment between the loop and the tick boundary, and that differs run to run even across 100k samples. So `min_low` jumps by exactly one or two quanta between runs.
- **framing** is essentially `min_low − 49`, so it inherits that jump one-for-one (the noise-amplification comment […]

> DEVELOPER

Just so you know and the default time is 5secs and I'm meauring some stuff that's pretty fast:
wink@3900x 26-07-08T15:16:18.605Z:~/data/prgs/rust/iiac-perf (main+1)
$ iiac-perf mpsc-1t
iiac-perf 0.20.0 — Rust latency microbenchmark harness

Calibration:
  framing/sample      11.12 ns  (timer pair, two-point fit)

wink@3900x 26-07-08T15:16:25.892Z:~/data/prgs/rust/iiac-perf (main+1)
$ iiac-perf mpsc-1t
iiac-perf 0.20.0 — Rust latency microbenchmark harness

Calibration:
  framing/sample      21.22 ns  (timer pair, two-point fit)
  loop/iter            0.49 ns  (per inner-loop iteration)

wink@3900x 26-07-08T15:16:32.318Z:~/data/prgs/rust/iiac-perf (main+1)
$ iiac-perf mpsc-1t
iiac-perf 0.20.0 — Rust latency microbenchmark harness

Calibration:
  framing/sample      21.22 ns  (timer pair, two-point fit)
  loop/iter            0.49 ns  (per inner-loop iteration)

wink@3900x 26-07-08T15:16:38.857Z:~/data/prgs/rust/iiac-perf (main+1)
$ iiac-perf mpsc-1t
iiac-perf 0.20.0 — Rust latency microbenchmark harness

Calibration:
  framing/sample      11.22 ns  (timer pair, two-point fit)
  loop/iter            0.49 ns  (per inner-loop iteration)

wink@3900x 26-07-08T15:16:45.466Z:~/data/prgs/rust/iiac-perf (main+1)
$ iiac-perf mpsc-1t -d 1
iiac-perf 0.20.0 — Rust latency microbenchmark harness

Calibration:
  framing/sample      11.22 ns  (timer pair, two-point fit)
  loop/iter            0.49 ns  (per inner-loop iteration)

wink@3900x 26-07-08T15:16:53.466Z:~/data/prgs/rust/iiac-perf (main+1)
$ iiac-perf mpsc-1t -d 1
iiac-perf 0.20.0 — Rust latency microbenchmark harness

Calibration:
  framing/sample       1.02 ns  (timer pair, two-point fit)
  loop/iter            0.49 ns  (per inner-loop iteration)

wink@3900x 26-07-08T15:16:57.020Z:~/data/prgs/rust/iiac-perf (main+1)
$ iiac-perf mpsc-1t -d 1
iiac-perf 0.20.0 — Rust latency microbenchmark harness

Calibration:
  framing/sample      11.12 ns  (timer pair, two-point […]

> DEVELOPER

I ran iiac-perf a bunch of times and the framing/sample time is moving quite a bit,
but the loop/iter is steady. I just grabbed those first few lines of each run. Your opinion

wink@3900x 26-07-08T15:28:00.588Z:~/data/prgs/rust/iiac-perf (main+1)
$ iiac-perf zcr-with-1t
iiac-perf 0.20.0 — Rust latency microbenchmark harness

Calibration:
  framing/sample      11.22 ns  (timer pair, two-point fit)
  loop/iter            0.49 ns  (per inner-loop iteration)
  cal pin           core 0 (unpinned after cal; --no-pin-cal to skip)
  bench pin         none (unpinned)
  sleep inhibit     active (systemd-inhibit --what=sleep)
  config            none (built-in defaults)

zcr-with-1t: zc-ring-x1 reserve_slot_with round-trip (1 thread) [duration=5.0s outer=28,103,644 inner=43 calls=1,208,456,692 adj/call=0.75ns labels=both]:
                        first           last         range        count          mean      adjusted
  z4  0.000_1          2.6 ns         2.6 ns        0.0 ns            4        2.6 ns        1.8 ns
  p10 0.10             2.8 ns         2.8 ns        0.0 ns    3,702,968        2.8 ns        2.0 ns
  p20 0.20             3.0 ns         3.0 ns        0.0 ns    1,779,782        3.0 ns        2.3 ns
  p40 0.40             3.0 ns         3.0 ns        0.0 ns    9,081,958        3.0 ns        2.3 ns
  p60 0.60             3.2 ns         3.2 ns        0.0 ns    1,319,800        3.2 ns        2.5 ns
  p80 0.80             3.3 ns         3.3 ns        0.0 ns    9,780,917        3.3 ns        2.5 ns
  n2  0.99             3.5 ns         4.0 ns        0.5 ns    2,152,683        3.6 ns        2.9 ns
  n3  0.999            4.2 ns         4.9 ns        0.7 ns […]

> AGENT

Same story as before on the calibration — 11.22 ns is the middle quantum on the ~10 ns lattice, so nothing new there. But this fuller output actually shows where the framing wobble *does* matter, and it's worth flagging.

**The framing slop leaks into your adjusted numbers here.** This bench ran at `inner=43`, and `adj/call = 0.75 ns` checks out as `11.22/43 + 0.49 ≈ 0.75`. But if the next run's calibration lands on the 1.02 or 21.22 quantum instead, the adjustment becomes 0.51 or 0.98 ns — a ±0.23 ns swing on adjusted values that sit around 2.0-2.9 ns. That's ~10% of your measurement moving run-to-run purely from which timer quantum the calibration happened to land on. At `inner=100`+ this was negligible; at `inner=43` it isn't. That strengthens the case for the min-of-mins calibration repeat I mentioned — it would make the calibration reliably land on the lowest quantum instead of a random one.

On the bench results themselves, they look healthy:

- The core distribution is tight: z4 through n2 spans 2.6-4.0 ns with a 0.2 ns stdev — that's a clean, well-behaved fast path for a reserve/round-trip at ~2.4 ns adjusted.
- The tail structure is classic […]

> DEVELOPER

One thing I was thinking is maybe the calibration should be longer
and maybe it should be a percentage of the duration (10%/100%/1000%?
Also maybe it should be in a config file and only calculated on demand
or and if there is no config file?

> DEVELOPER

One thing I was thinking is maybe the calibration should be longer
and maybe it should be a percentage of the duration (10%/100%/1000%)?
Or maybe it should be in a config file and only calculated on demand
or and if there is no config file?

> AGENT

Good instincts on the config file; I'd push back on the duration-scaling. Let me take them in turn.

**Longer / percentage-of-duration calibration: I'd skip this.** The run-to-run wobble isn't a sampling-depth problem — you're already taking the min over 100k samples, and within a single run that min sits stably on one quantum. The error is which ~10 ns quantum the run's timing phase happens to align with, and more time in one continuous measurement doesn't re-roll that alignment. Also, conceptually, calibration measures a property of the *machine* (timer cost, loop cost), not of the *bench* — tying its length to `-d` couples an apparatus constant to workload length for no accuracy gain. What does re-roll the alignment is re-entering the measurement: repeat the `min_low`/`min_high` pair K times (say 5-9) and take min-of-mins. That reliably lands on the lowest quantum for tens of milliseconds, not seconds.

**Config-file caching: yes, and for a better reason than saving time.** The strongest argument isn't startup cost — it's *comparability*. Right now two otherwise-identical runs can differ by ~0.23 ns adjusted at `inner=43` purely because each run drew a different calibration quantum. If the adjustment constants are pinned in a config, run-to-run deltas in […]

> DEVELOPER

SG, what is the "floor" in our 1 to 21ns?

> AGENT

Good question — "floor" is doing two different jobs there, and it's worth separating them.

**The floor the min-of-mins estimator finds is a lattice point, not the true cost.** With a ~10 ns quantum, an interval of true length T measures as either ⌊T/10⌋ or ⌈T/10⌉ quanta depending on phase alignment. The min over enough phase re-rolls converges to the *lower* reading — which can under-read the true duration by up to one full quantum. Your observed `min_low` values decode to 50, 60, and 70 ns; the 1.02 ns framing run is the one that hit 50.

**So the true framing is somewhere in roughly [1, 11] ns — the timer can't resolve it tighter than that with this method.** The two-point fit fundamentally can't see inside one quantum, because its input (`min_low`) only exists on the lattice. Min-of-mins buys you *consistency* (every run reports 1.02, so adjusted numbers are comparable) but not *accuracy* — you'd be systematically adjusting by the optimistic edge of the interval.

If you want to actually resolve the true value, there's a method that beats the quantum: time a batch of timer pairs *inside one window* — one `Instant::now()` at the start, then a loop […]

> DEVELOPER

But the value of inner is adjusted based on the time a "step" takes and the user can adjust outer and inner on the command line.

> AGENT

Right — let me look at how the harness picks `inner` so I can reason about the actual worst case rather than the one run I saw.

> TOOL

tool_use Bash
id: toolu_01BmaRCdq7Bf3LqRCGTbcqpD
```json
{
  "command": "grep -n \"inner\" /home/<USER>/data/prgs/rust/iiac-perf/src/harness.rs | head -40",
  "description": "Find inner-tuning logic in harness.rs"
}
```

> TOOL

tool_result
id: toolu_01BmaRCdq7Bf3LqRCGTbcqpD
```
1://! Generic bench driver: the [`Bench`] trait, adaptive outer/inner
19:/// but dividing a sample by `inner` in ps keeps the true sub-ns
62:    /// Force a fixed inner-loop count, bypassing the
64:    pub inner_override: Option<u64>,
96:/// `(histogram, outer, inner, duration_s, suspended_s)`.
98:/// After a fixed warmup, `inner` is auto-sized so apparatus framing
99:/// doesn't dominate (skipped when `cfg.inner_override` is set). The
112:    let inner = cfg
113:        .inner_override
114:        .unwrap_or_else(|| pick_inner(step_cost_ns, framing_ns));
119:            let (hist, duration_s) = run_counted(bench, outer, inner);
123:            let (hist, duration_s) = run_timed(bench, cfg.target_seconds, inner);
128:    (hist, outer, inner, duration_s, clocks.suspended_s())
146:fn pick_inner(step_cost_ns: f64, framing_ns: f64) -> u64 {
151:fn run_counted<B: Bench>(bench: &mut B, outer: u64, inner: u64) -> (Histogram<u64>, f64) {
155:        record_sample(bench, inner, &mut hist);
161:fn run_timed<B: Bench>(bench: &mut B, target_seconds: f64, inner: u64) -> (Histogram<u64>, f64) {
166:        record_sample(bench, inner, &mut hist);
182:/// Time one sample (`inner` back-to-back calls), divide down to a
186:fn record_sample<B: Bench>(bench: &mut B, inner: u64, hist: &mut Histogram<u64>) {
188:    for _ in 0..inner {
192:    hist.saturating_record(round_elapsed_ps(elapsed_ps, inner));
195:/// Per-call value: `elapsed_ps / inner`, rounded to nearest, in
199:fn round_elapsed_ps(elapsed_ps: u128, inner: u64) -> u64 {
200:    let inner = inner as u128;
201:    ((elapsed_ps […]

> TOOL

tool_use Read
id: toolu_01QRfLhQr5SPBGQR6pCRCtLN
```json
{
  "file_path": "/home/<USER>/data/prgs/rust/iiac-perf/src/harness.rs",
  "offset": 130,
  "limit": 22
}
```

> TOOL

tool_result
id: toolu_01QRfLhQr5SPBGQR6pCRCtLN
```
130	
131	fn estimate_step_cost<B: Bench>(bench: &mut B) -> f64 {
132	    let mut samples: Vec<f64> = (0..ESTIMATE_SAMPLES)
133	        .map(|_| {
134	            let start = minstant::Instant::now();
135	            for _ in 0..ESTIMATE_STEPS {
136	                black_box(bench.step());
137	            }
138	            let total = start.elapsed().as_nanos() as u64;
139	            total as f64 / ESTIMATE_STEPS as f64
140	        })
141	        .collect();
142	    samples.sort_by(|a, b| a.partial_cmp(b).unwrap());
143	    samples[ESTIMATE_SAMPLES / 2]
144	}
145	
146	fn pick_inner(step_cost_ns: f64, framing_ns: f64) -> u64 {
147	    let target = (FRAMING_DOMINATION_RATIO * framing_ns / step_cost_ns).ceil() as u64;
148	    target.clamp(1, MAX_INNER)
149	}
150	
151	fn run_counted<B: Bench>(bench: &mut B, outer: u64, inner: u64) -> (Histogram<u64>, f64) {
```

> TOOL

tool_use Bash
id: toolu_016UNTuKvgoV9TKSCaKVUy9K
```json
{
  "command": "grep -n \"FRAMING_DOMINATION_RATIO\\|MAX_INNER\\|ESTIMATE_STEPS\\|ESTIMATE_SAMPLES\" /home/<USER>/data/prgs/rust/iiac-perf/src/harness.rs | head",
  "description": "Find tuning constants"
}
```

> TOOL

tool_result
id: toolu_016UNTuKvgoV9TKSCaKVUy9K
```
12:const ESTIMATE_STEPS: u64 = 1_000;
13:const ESTIMATE_SAMPLES: usize = 5;
14:const FRAMING_DOMINATION_RATIO: f64 = 10.0;
15:const MAX_INNER: u64 = 1_000;
132:    let mut samples: Vec<f64> = (0..ESTIMATE_SAMPLES)
135:            for _ in 0..ESTIMATE_STEPS {
139:            total as f64 / ESTIMATE_STEPS as f64
143:    samples[ESTIMATE_SAMPLES / 2]
147:    let target = (FRAMING_DOMINATION_RATIO * framing_ns / step_cost_ns).ceil() as u64;
148:    target.clamp(1, MAX_INNER)
```

> AGENT

I checked `pick_inner` (`src/harness.rs:146-149`), and you're right to push on this — the adaptivity makes the framing error matter *more* than my "±0.23 ns at inner=43" framing, in two ways.

**The auto-sizing turns framing uncertainty into a roughly constant ~9% relative error.** `pick_inner` sizes `inner ≈ 10 × framing / step_cost`, i.e. the sample window is ten framings long regardless of step cost. The per-call adjustment error is `δ/inner` where δ is the framing estimation error, and substituting the sizing rule: `δ/inner ≈ δ × step / (10 × framing)` — so relative to the step cost it's `δ/(10 × framing)`, independent of how fast or slow the bench is. With framing ≈ 11 ns and δ up to a full ~10 ns quantum, that's up to ~9% error on *every* auto-sized bench, fast or slow. The adaptivity doesn't dilute the error; it holds it at a fixed fraction.

**Worse: the framing estimate feeds the sizing itself, so a low-quantum calibration under-sizes `inner`.** If a run draws the 1.02 ns calibration, `pick_inner` computes `ceil(10 × 1.02 / 2.9) ≈ 4` instead of ~43 for your zcr bench. Then the *true* ~11 ns framing is amortized over only 4 calls — […]

> DEVELOPER

so using the config file is the "best" most solution, so is the framming error a constant because the timer is a constant even whent he machine is throttled or in "turbo" mode?

> AGENT

Two different constants there, and they behave differently under frequency changes:

**The timer's quantum and rate: yes, constant.** Modern x86 TSCs are "invariant" — they tick at a fixed rate regardless of turbo, throttle, or idle states (that's precisely what makes them usable as a wall-clock source, and why `minstant` can use them). The ~10 ns granularity lattice is derived from the fixed reference clock, so it doesn't move with core frequency.

**The framing *cost*: no, not constant.** The framing number is the wall-clock time to *execute* the timer-pair reads — some ~tens of cycles of `rdtsc` plus `minstant` arithmetic, run by the core at whatever frequency it currently holds. The same ~40 cycles is ~8.7 ns at 4.6 GHz boost and ~18 ns at a 2.2 GHz throttle. Same for loop/iter. So a cached calibration is implicitly "framing cost at the frequency the calibration ran at."

In practice this is less scary than it sounds, for two reasons:

- The calibration warmup (`CAL_WARMUP` at `src/overhead.rs:12`) exists to ramp boost before measuring, and your benches are also hot loops that hold boost — so calibration and bench typically run at the *same* (boosted) frequency, and the cached constant matches. The […]

> DEVELOPER

Good, capture this information in chores. But I also think we should create notes/design.md so information like this doesn't get buried.

> TOOL

tool_use Bash
id: toolu_01G5z97TRs96n3SjzGBVxaa4
```json
{
  "command": "ls /home/<USER>/data/prgs/rust/iiac-perf/notes/ /home/<USER>/data/prgs/rust/iiac-perf/notes/chores/",
  "description": "List notes directory"
}
```

> TOOL

tool_result
id: toolu_01G5z97TRs96n3SjzGBVxaa4
```
/home/<USER>/data/prgs/rust/iiac-perf/notes/:
bot-convo.txt
chores
chores-01.md
chores-02.md
chores-03.md
cycle-protocol.md
done.md
ideas.md
jj-tips.md
README.md
todo.md
vc-notes.md
versioning.md

/home/<USER>/data/prgs/rust/iiac-perf/notes/chores/:
chores-04.md
```

> TOOL

tool_use Bash
id: toolu_01MjsCSTDoneoqWPa2PGP78K
```json
{
  "command": "grep -n '^## \\|^# ' /home/<USER>/data/prgs/rust/iiac-perf/notes/chores/chores-04.md",
  "description": "Scan chores-04 headings"
}
```

> TOOL

tool_result
id: toolu_01MjsCSTDoneoqWPa2PGP78K
```
1:# Chores 04
7:## feat: zcr bench family (raw/with/spin, 1t/2t)
80:## fix: saturate hist records, flag suspended runs
113:## fix: report column alignment
138:## feat: finer report tail bands
157:## feat: inhibit sleep during bench runs
181:## feat: nines/zeros tail bands (z4..n10)
207:## fix: number todo entries per AGENTS todo format
229:## feat: report options + ps recording
266:## feat: config file + pin profiles
307:## refactor: drop zcr raw/spin bench tiers
333:## fix: trim label spans populated bands
387:## fix: upper-closed band intervals
424:## docs: add "Reading a report" to README
450:## feat: zcr-mpsc-1t/2t benches
476:# References
```

> TOOL

tool_use Read
id: toolu_011DGr9esUJ4z5bEPuCirh7U
```json
{
  "file_path": "/home/<USER>/data/prgs/rust/iiac-perf/notes/chores/chores-04.md",
  "offset": 440,
  "limit": 80
}
```

> TOOL

tool_result
id: toolu_011DGr9esUJ4z5bEPuCirh7U
```
440	  worked 10-value and single-sample tables, the interval-convention
441	  citations as inline links (Hazen 1914, pandas.cut, numpy.histogram,
442	  Dijkstra EWD831), and the `-d` investigation technique with real
443	  few-sample / single-sample output.
444	- The `### Band membership` note is trimmed to a pointer at that
445	  README section (SSOT); its four interval refs move to README inline
446	  links and are pruned here.
447	- A machine-dependence caveat on the `-d` reproducer rounds it out —
448	  the value that lands N samples is timing-specific.
449	
450	## feat: zcr-mpsc-1t/2t benches
451	
452	Commits:
453	
454	zc-ring-x1 0.11.0 grew an MPSC sibling ring (CAS-claimed
455	producer index + per-slot seq array, closure `send_with`);
456	these benches are the A/B its design's measurement plan calls
457	for, mirroring the zcr-with pair.
458	
459	- `zcr-mpsc-1t` — same-thread round-trip: the uncontended
460	  claim CAS + seq publish, against `zcr-with-1t`'s
461	  load/store-only SPSC pair.
462	- `zcr-mpsc-2t` — main → echo worker → main over two MPSC
463	  rings (one producer each), the same shape as `zcr-with-2t`:
464	  the "MPSC when you don't need it" number.
465	- `zcr_common` gained `leak_mpsc_ring()`; the `zcr` CLI
466	  prefix now resolves […]

> TOOL

tool_use Read
id: toolu_01FtPaNkKGr2FH64ZdFWWx5B
```json
{
  "file_path": "/home/<USER>/data/prgs/rust/iiac-perf/notes/todo.md",
  "offset": 0,
  "limit": 60
}
```

> TOOL

tool_result
id: toolu_01FtPaNkKGr2FH64ZdFWWx5B
```
0	# Todo
1	
2	This file uses [Prose form](../AGENTS.md#prose-form). It
3	contains near term tasks with a short description and
4	uses links or reference links for more details.
5	
6	## In Progress
7	
8	When a `## Todo` item is picked up, its text moves here: the
9	problem overview and its list of things to do. That is followed
10	by the "plan" — a bulleted list of the development "ladder":
11	   - 0.xx.y-0 blah (done)
12	   - 0.xx.y-1 blah blah (current)
13	   - 0.xx.y-2 blah blah blah
14	   - 0.xx.y close-out and validation
15	
16	_No cycle currently in progress._
17	
18	## Todo
19	
20	Entries are in **strict priority rank** — #1 highest,
21	descending. Reprioritize by moving an entry, then
22	`vc-x1 fix-todo --no-dry-run notes/todo.md` to renumber.
23	The numbers are positional rank, not stable IDs — to refer
24	to a Todo, name it by its **title** (a greppable mention;
25	a numbered list item has no anchor to link to), not its
26	number. Use the
27	[Prose Form in AGENTS.md](../AGENTS.md#prose-form); deeper
28	detail goes in `notes/chores/chores-NN.md` design
29	subsections (link via `[N]` ref).
30	
31 […]

> TOOL

tool_use Bash
id: toolu_017vDZb2fMyrKDnmMjjqmz73
```json
{
  "command": "grep -n \"design\\|README\" /home/<USER>/data/prgs/rust/iiac-perf/notes/README.md | head -20",
  "description": "Peek at notes/README.md structure"
}
```

> TOOL

tool_result
id: toolu_017vDZb2fMyrKDnmMjjqmz73
```
(Bash completed with no output)
```

> TOOL

tool_use Read
id: toolu_01LKD2RfvkJeEnYzYzUJGetS
```json
{
  "file_path": "/home/<USER>/data/prgs/rust/iiac-perf/notes/README.md"
}
```

> TOOL

tool_result
id: toolu_01LKD2RfvkJeEnYzYzUJGetS
```
1	# Notes
2	
3	This directory contains various notes and documentation related to the project.
4	Each file is organized by topic for easy reference.
5	
6	By default there are chores-*.md and todo.md. Chores are general notes
7	about tasks and todo.md contains short term tasks and their status.
8	
9	In the future we I expect we may want to create a "notes"
10	database to better manage the information, TBD.
11	
12	Examples chore file:
13	```
14	# Chores-01.md
15	
16	General maintenance tasks and considerations for the project see other files for
17	more specific topics. A chore in a chores file provides quick information on the
18	how and why of a particular chore. The section header is short and sweet
19	and the title is appended with the version number of the app when the chore
20	is completed.
21	
22	## Create an app that does something interesting (0.1.0)
23	
24	The app counts from 1 to 100, not to interesting.
25	```
26	
27	## Commit Workflow
28	
29	This project uses a per-step commit / push / finalize flow against
30	two paired repos (app […]

> TOOL

tool_use Bash
id: toolu_01HVNHKB92hxsH8RjwpMUNSw
```json
{
  "command": "grep -rn \"config\" /home/<USER>/data/prgs/rust/iiac-perf/src/main.rs | head; ls /home/<USER>/data/prgs/rust/iiac-perf/src/",
  "description": "Check config-file implementation surface"
}
```

> TOOL

tool_result
id: toolu_01HVNHKB92hxsH8RjwpMUNSw
```
/home/<USER>/data/prgs/rust/iiac-perf/src/main.rs:4:mod config;
/home/<USER>/data/prgs/rust/iiac-perf/src/main.rs:35:    /// config `duration`). Auto-sizes outer and inner loop counts.
/home/<USER>/data/prgs/rust/iiac-perf/src/main.rs:63:    /// the config file expands to that profile's core spec (e.g.
/home/<USER>/data/prgs/rust/iiac-perf/src/main.rs:100:    /// config `band_labels`; both absent defaults to 'both'.
/home/<USER>/data/prgs/rust/iiac-perf/src/main.rs:108:    /// config `decimals`; both absent defaults to 1.
/home/<USER>/data/prgs/rust/iiac-perf/src/main.rs:127:/// Banner text listing which config files were loaded, or
/home/<USER>/data/prgs/rust/iiac-perf/src/main.rs:129:fn config_summary(files: &[std::path::PathBuf]) -> String {
/home/<USER>/data/prgs/rust/iiac-perf/src/main.rs:169:    // CLI). A malformed config is fatal so a typo surfaces.
/home/<USER>/data/prgs/rust/iiac-perf/src/main.rs:170:    let (config, config_files) = match config::load() {
/home/<USER>/data/prgs/rust/iiac-perf/src/main.rs:173:            eprintln!("error: config: {e}");
bands.rs
band_table.rs
benches
config.rs
harness.rs
inhibit.rs
main.rs
overhead.rs
pin.rs
probe.rs
ticks
ticks.rs
tprobe2.rs
tprobe.rs
```

> AGENT

Now I'll write `notes/design.md` and the chores section.

> TOOL

tool_use Write
id: toolu_01G8hHRQ18mEeDvnXTmeXudQ
```json
{
  "file_path": "/home/<USER>/data/prgs/rust/iiac-perf/notes/design.md",
  "content": "# Design\n\nDurable design analyses for iiac-perf. Chores sections record\nwhat landed per commit; this file holds the analysis and\nreasoning that should outlive any one cycle — measurement\ntheory, error models, and the design decisions they drive.\nChores and todo entries link here rather than restating.\n\n## Calibration accuracy: framing quantization\n\nAnalysis from a 2026-07-08 session on the 3900X, prompted by\nthe framing/sample header value jumping between ~1 ns and\n~21 ns across runs while loop/iter held steady at 0.49 ns.\n\n### Observation: framing sits on a ~10 ns lattice\n\nRepeated runs reported framing/sample of 1.02, 11.12, 11.22,\nand 21.22 ns — not a continuous drift but discrete steps of\n~10.1 ns. Decoding through the two-point fit\n(`src/overhead.rs`), the underlying `min_low` measurements\nwere 50, 60, and 70 ns.\n\nWe think the mechanism is TSC granularity: `minstant` reads\nthe TSC, and on Zen 2 the TSC is derived from the 100 MHz\nreference clock, so elapsed-time readings quantize to ~10 ns\nsteps.\n\n### Why framing wobbles but loop/iter is steady\n\nBoth constants come from the same two measurements; they\ndiffer in amortization:\n\n- `framing = min_low - N_LOW * loop_per_iter` — inherits\n  `min_low`'s quantization one-for-one (noise amplification\n  ~1.01, per the comment in `src/overhead.rs`).\n- `loop_per_iter = (min_high - min_low) / 9_900` — the same\n  ±1-2 […]

> TOOL

tool_result
id: toolu_01G8hHRQ18mEeDvnXTmeXudQ
```
File created successfully at: /home/<USER>/data/prgs/rust/iiac-perf/notes/design.md (file state is current in your context — no need to Read it back)
```

> AGENT

Now the chores section, inserted before `# References`:

> TOOL

tool_use Edit
id: toolu_01BH2wdhFqhkNk3DfXwJBman
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/data/prgs/rust/iiac-perf/notes/chores/chores-04.md",
  "old_string": "- Cargo.lock: the zc-ring-x1 git dep advances to 0.11.1 (the\n  MPSC release + backfill tip).\n\n# References",
  "new_string": "- Cargo.lock: the zc-ring-x1 git dep advances to 0.11.1 (the\n  MPSC release + backfill tip).\n\n## docs: add notes/design.md (calibration accuracy)\n\nCommits:\n\nRepeated runs showed framing/sample jumping 1-21 ns while\nloop/iter held steady — traced to ~10 ns TSC quantization of\nthe un-amortized `min_low` measurement, not sampling noise.\nThe analysis and the resulting design (amortized framing\nmeasurement + cached calibration in the config file) are too\ndurable for a chores section, so this cycle opens\n[notes/design.md](../design.md) as the home for\nmeasurement-theory / error-model analyses, with this as its\nfirst entry\n([Calibration accuracy](../design.md#calibration-accuracy-framing-quantization)).\n\n- Key findings recorded there: the min estimator can't\n  resolve inside a quantum (true framing ∈ ~[1, 11] ns); the\n  framing estimate sizes `inner` via `pick_inner`, so an\n  under-read under-sizes the experiment (worst case ~50%\n  apparatus contamination, invisible in the report); the TSC\n  quantum is frequency-invariant but the framing *cost* is\n  core-clocked.\n- Design direction: amortized framing measurement (M timer\n  pairs in one window, error q/M), constants cached in the\n  config file with provenance and a cheap live validity\n  check each run; duration-scaled calibration rejected.\n- notes/README.md gains a pointer to design.md.\n\n# References"
}
```

> TOOL

tool_result
id: toolu_01BH2wdhFqhkNk3DfXwJBman
```
The file /home/<USER>/data/prgs/rust/iiac-perf/notes/chores/chores-04.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_013tAtFmKoVjfURQDUbaLjje
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/data/prgs/rust/iiac-perf/notes/README.md",
  "old_string": "By default there are chores-*.md and todo.md. Chores are general notes\nabout tasks and todo.md contains short term tasks and their status.",
  "new_string": "By default there are chores-*.md and todo.md. Chores are general notes\nabout tasks and todo.md contains short term tasks and their status.\nDurable design analyses (measurement theory, error models, decisions\nthat outlive a cycle) live in [design.md](design.md)."
}
```

> TOOL

tool_result
id: toolu_013tAtFmKoVjfURQDUbaLjje
```
The file /home/<USER>/data/prgs/rust/iiac-perf/notes/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Adding a todo entry so the implementation work is tracked, then renumbering:

> TOOL

tool_use Edit
id: toolu_018X2M53hMwKdUNnQjdkwi2s
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/data/prgs/rust/iiac-perf/notes/todo.md",
  "old_string": "1. Unit scaling in report columns (`us`/`ms`) — per-row",
  "new_string": "1. Amortized framing calibration + cached constants in config\n   — framing is quantized to the ~10 ns TSC lattice and the\n   estimate sizes `inner`, so a low draw under-sizes the\n   experiment (up to ~9% relative error, worst case ~50%\n   apparatus contamination); measure M timer pairs in one\n   window (error q/M), cache in config with provenance +\n   live validity check, header says cached vs live\n   [analysis](design.md#calibration-accuracy-framing-quantization)\n1. Unit scaling in report columns (`us`/`ms`) — per-row"
}
```

> TOOL

tool_result
id: toolu_018X2M53hMwKdUNnQjdkwi2s
```
The file /home/<USER>/data/prgs/rust/iiac-perf/notes/todo.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_0126KAM9p5n9YKHED9FxY8wB
```json
{
  "command": "vc-x1 fix-todo --no-dry-run notes/todo.md",
  "description": "Renumber todo entries"
}
```

> TOOL

tool_result
id: toolu_0126KAM9p5n9YKHED9FxY8wB
```
fix-todo: notes/todo.md

## Todo
  2. Unit scaling in report columns (`us`/`ms`) — per-row  [40: was 1]
  3. Investigate: suspend gap missing from samples. A 0.13.5  [46: was 2]
  4. CLAUDE.md governance model (design cogitation) [20]  [54: was 3]
  5. Add framing adjustment to `Probe::report` (subtract  [55: was 4]
  6. Convert `harness` / `Bench` to probe-based measurement. Will  [58: was 5]
  7. Rename app  [63: was 6]
  8. Design an app to measure IIAC perforanace written in Rust[1]  [64: was 7]
  9. `ice-ps-2t-wait` — iceoryx2 pub/sub with blocking waits via  [65: was 8]
  10. Switch ice benches to the loan-based zero-copy send path  [68: was 9, indent 3 → 4]
  11. Payload-size sweep for the round-trip benches (8 B / 8 KiB /  [71: was 10]
  12. `crossbeam-1t` / `crossbeam-2t` — `crossbeam-channel` directly  [74: was 11]
  13. `tokio-mpsc-1t` / `tokio-mpsc-2t` — `tokio::sync::mpsc` round-trip  [76: was 12]
  14. `flume-1t` / `flume-2t` — `flume` MPMC channel  [78: was 13]
  15. Function-call baselines: direct call vs `Box<dyn Trait>` vs  [79: was 14]
  16. When the second channel impl lands, extract shared message types  [82: was 15]
  17. Additional thread control (count, per-thread pin lists, NUMA) —  [84: was 16]
  18. […]

> TOOL

tool_use Bash
id: toolu_01GMFcFoQpk2sx129rDCgJ6a
```json
{
  "command": "vc-x1 validate-todo notes/todo.md",
  "description": "Validate todo numbering"
}
```

> TOOL

tool_result
id: toolu_01GMFcFoQpk2sx129rDCgJ6a
```
validate-todo: notes/todo.md

18 entries checked (18 Todo, 0 Bugs) — all sequential
```

> AGENT

Done — the analysis is captured in three places, each doing a different job:

- **`notes/design.md`** (new) — the durable home. Opens with a short statement of purpose (measurement theory, error models, decisions that outlive a cycle), then the full calibration analysis as its first entry: the ~10 ns TSC lattice observation, why framing wobbles while loop/iter is steady (amortization asymmetry), why the min estimator can't resolve inside a quantum, the error propagation through `pick_inner` (including why min-of-mins would have been the wrong fix), the frequency-dependence answer from your last question (invariant TSC quantum vs core-clocked framing cost), and the resulting design: amortized framing measurement + cached constants in the config file with provenance and a live validity check. The rejected duration-scaling alternative is recorded too, with the reason.

- **`notes/chores/chores-04.md`** — a new section `## docs: add notes/design.md (calibration accuracy)` with an empty `Commits:` line per convention, conceptual bullets, and links pointing at design.md as the source of truth rather than restating it.

- **`notes/todo.md`** — I added the implementation work as a new entry, "Amortized framing calibration + cached constants in config", linking to the design.md analysis. I ranked it #1 since it affects measurement correctness (up to […]

> DEVELOPER

In the design doc add and `## Architecure Overview` section giving a high level view of the app architecture.

> AGENT

Let me survey the module docstrings to write an accurate overview.

> TOOL

tool_use Bash
id: toolu_01QxVHU4uGPXdeiMB4whLfeW
```json
{
  "command": "for f in /home/<USER>/data/prgs/rust/iiac-perf/src/*.rs /home/<USER>/data/prgs/rust/iiac-perf/src/benches/*.rs; do echo \"=== $f\"; sed -n '1,8p' \"$f\" | grep '^//!'; done",
  "description": "Show module docstrings for all source files"
}
```

> TOOL

tool_result
id: toolu_01QxVHU4uGPXdeiMB4whLfeW
```
=== /home/<USER>/data/prgs/rust/iiac-perf/src/bands.rs
//! Report band boundaries and label styles: the single source of
//! truth for the min/z/p/n/max ladder that
//! [`crate::harness::print_report`] renders, documented by the
//! README's boundary-ladder table (pinned by this module's tests).
//!
//! - Familiar deciles in the body; nines/zeros tails generated
//!   from [`Z_DEPTH`]/[`N_DEPTH`]. Fractions and names come from
//!   one structural description, so the label styles can never
=== /home/<USER>/data/prgs/rust/iiac-perf/src/band_table.rs
//! Shared band-table renderer for tick-valued histograms.
//!
//! Both `TProbe` (fast path, direct-histogram) and `TProbe2`
//! (scope API, records → drain) store hardware tick deltas and
//! want the same band-table output shape — min/p1/…/p99/max
//! rows with first/last/range/count/mean columns, plus summary
//! lines for mean, stdev, mean min-p99, stdev min-p99. This
//! module provides a single implementation both can call into.
=== /home/<USER>/data/prgs/rust/iiac-perf/src/config.rs
//! Layered configuration for defaults: built-in < XDG config file <
//! project-local file < CLI flags.
//!
//! - **XDG file** — `$XDG_CONFIG_HOME/iiac-perf/config.toml`, or
//!   `$HOME/.config/iiac-perf/config.toml` when `XDG_CONFIG_HOME`
//!   is unset. The per-user home for defaults and pin profiles.
//! - **Project-local file** — [`LOCAL_FILE`] in the current
//!   directory (no upward walk). Overrides the XDG file
=== /home/<USER>/data/prgs/rust/iiac-perf/src/harness.rs
//! Generic bench driver: the […]

> TOOL

tool_use Read
id: toolu_01NQNaEahDe9hiffpLNyj7NF
```json
{
  "file_path": "/home/<USER>/data/prgs/rust/iiac-perf/src/main.rs",
  "offset": 1,
  "limit": 30
}
```

> TOOL

tool_result
id: toolu_01NQNaEahDe9hiffpLNyj7NF
```
1	mod band_table;
2	mod bands;
3	mod benches;
4	mod config;
5	mod harness;
6	mod inhibit;
7	mod overhead;
8	mod pin;
9	mod probe;
10	mod ticks;
11	mod tprobe;
12	mod tprobe2;
13	
14	use clap::Parser;
15	use log::{debug, info};
16	
17	#[derive(Parser)]
18	#[command(
19	    version,
20	    about = concat!(
21	        "iiac-perf ",
22	        env!("CARGO_PKG_VERSION"),
23	        " — Rust latency microbenchmark harness",
24	    ),
25	    max_term_width = 80,
26	)]
27	struct Cli {
28	    /// Benches to run. Pass 'all' for every registered bench, or
29	    /// one or more names; a name matching no bench exactly runs
30	    /// every bench it is a prefix of (e.g. 'ice', 'mpsc').
```

> TOOL

tool_use Read
id: toolu_0164WoinQsWDH7ynkNEcwuXT
```json
{
  "file_path": "/home/<USER>/data/prgs/rust/iiac-perf/src/main.rs",
  "offset": 150,
  "limit": 110
}
```

> TOOL

tool_result
id: toolu_0164WoinQsWDH7ynkNEcwuXT
```
150	            log::LevelFilter::Debug
151	        } else {
152	            log::LevelFilter::Warn
153	        });
154	    }
155	    builder.format_timestamp(None).init();
156	
157	    if cli.benches.is_empty() {
158	        println!("no benches specified. use -h or --help for more info.");
159	        println!("available: all, {}", benches::names().join(", "));
160	        return;
161	    }
162	
163	    // Re-exec under systemd-inhibit (unless --no-inhibit or
164	    // already inhibited) before any output, so the banner prints
165	    // once, from the inhibited child.
166	    let inhibit_status = inhibit::ensure(cli.no_inhibit);
167	
168	    // Layered defaults (built-in < XDG file < project-local file <
169	    // CLI). A malformed config is fatal so a typo surfaces.
170	    let (config, config_files) = match config::load() {
171	        Ok(c) => c,
172	        Err(e) => {
173	            eprintln!("error: config: {e}");
174	            std::process::exit(2);
175	        }
176	    };
177	
178	    println!(
179	        "iiac-perf {} — Rust latency microbenchmark harness\n",
180	        env!("CARGO_PKG_VERSION")
181	    );
182	
183	    if let Some(mask) = pin::current_affinity() {
184	        info!("startup affinity: {}", pin::affinity_summary(&mask));
185	    }
186	
187	    let pin_cores: Vec<usize> = match cli.pin.as_deref() {
188	        None => Vec::new(),
189	        // A spec naming a config profile expands to its core list;
190	        // anything else parses as a raw core spec.
191	        Some(spec) => match pin::parse_cores(config.resolve_pin(spec)) {
192 […]

> TOOL

tool_use Edit
id: toolu_01Hq8oTU3maDpyVZ9VZjaex2
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/data/prgs/rust/iiac-perf/notes/design.md",
  "old_string": "Durable design analyses for iiac-perf. Chores sections record\nwhat landed per commit; this file holds the analysis and\nreasoning that should outlive any one cycle — measurement\ntheory, error models, and the design decisions they drive.\nChores and todo entries link here rather than restating.\n\n## Calibration accuracy: framing quantization",
  "new_string": "Durable design analyses for iiac-perf. Chores sections record\nwhat landed per commit; this file holds the analysis and\nreasoning that should outlive any one cycle — measurement\ntheory, error models, and the design decisions they drive.\nChores and todo entries link here rather than restating.\n\n## Architecture Overview\n\niiac-perf is a latency microbenchmark harness: a single binary\nthat runs named benches (mostly inter-thread communication\nround-trips) and renders each as a band-table latency\nhistogram. The architecture has four layers — startup /\nenvironment control, measurement, benches, and reporting.\n\n### Startup and environment control\n\n`main.rs` runs a fixed pipeline before any bench executes:\n\n- **CLI** (clap) — bench selection by exact name or prefix\n  (`zcr` runs every `zcr-*` bench), plus duration, outer/inner\n  overrides, pinning, and report options.\n- **Sleep inhibition** (`inhibit.rs`) — re-exec the process\n  under `systemd-inhibit` so an idle suspend can't poison a\n  long run; harness suspend detection remains the backstop.\n- **Layered config** (`config.rs`) — built-in < XDG […]

> TOOL

tool_result
id: toolu_01Hq8oTU3maDpyVZ9VZjaex2
```
The file /home/<USER>/data/prgs/rust/iiac-perf/notes/design.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Let me verify the bench CLI names I cited match the registry:

> TOOL

tool_use Bash
id: toolu_01GvwhHU7GoKh3NsDPHhFV6C
```json
{
  "command": "grep -rn 'NAME: &str\\|pub const NAME' /home/<USER>/data/prgs/rust/iiac-perf/src/benches/*.rs",
  "description": "List registered bench names"
}
```

> TOOL

tool_result
id: toolu_01GvwhHU7GoKh3NsDPHhFV6C
```
/home/<USER>/data/prgs/rust/iiac-perf/src/benches/zcr_with_1t.rs:12:pub const NAME: &str = "zcr-with-1t";
/home/<USER>/data/prgs/rust/iiac-perf/src/benches/min_now.rs:8:pub const NAME: &str = "min-now";
/home/<USER>/data/prgs/rust/iiac-perf/src/benches/zcr_mpsc_2t.rs:14:pub const NAME: &str = "zcr-mpsc-2t";
/home/<USER>/data/prgs/rust/iiac-perf/src/benches/ice_rr_1t.rs:12:pub const NAME: &str = "ice-rr-1t";
/home/<USER>/data/prgs/rust/iiac-perf/src/benches/ice_ps_1t.rs:12:pub const NAME: &str = "ice-ps-1t";
/home/<USER>/data/prgs/rust/iiac-perf/src/benches/tp2_pc.rs:22:pub const NAME: &str = "tp2-pc";
/home/<USER>/data/prgs/rust/iiac-perf/src/benches/probe_mpsc_2t.rs:18:pub const NAME: &str = "probe-mpsc-2t";
/home/<USER>/data/prgs/rust/iiac-perf/src/benches/std_now.rs:8:pub const NAME: &str = "std-now";
/home/<USER>/data/prgs/rust/iiac-perf/src/benches/mpsc_1t.rs:9:pub const NAME: &str = "mpsc-1t";
/home/<USER>/data/prgs/rust/iiac-perf/src/benches/mpsc_2t.rs:11:pub const NAME: &str = "mpsc-2t";
/home/<USER>/data/prgs/rust/iiac-perf/src/benches/ice_ps_2t.rs:16:pub const NAME: &str = "ice-ps-2t";
/home/<USER>/data/prgs/rust/iiac-perf/src/benches/zcr_with_2t.rs:14:pub const NAME: &str = "zcr-with-2t";
/home/<USER>/data/prgs/rust/iiac-perf/src/benches/producer_consumer.rs:24:pub const NAME: &str = "producer-consumer";
/home/<USER>/data/prgs/rust/iiac-perf/src/benches/ice_rr_2t.rs:15:pub const NAME: &str = "ice-rr-2t";
/home/<USER>/data/prgs/rust/iiac-perf/src/benches/mpsc_2t_spin.rs:11:pub const NAME: &str = "mpsc-2t-spin";
/home/<USER>/data/prgs/rust/iiac-perf/src/benches/tp_pc.rs:23:pub const NAME: &str = "tp-pc";
/home/<USER>/data/prgs/rust/iiac-perf/src/benches/zcr_mpsc_1t.rs:12:pub const NAME: &str = "zcr-mpsc-1t";
```

> TOOL

tool_use Edit
id: toolu_01K9VZPbvWAb1bu6iwdgwfUW
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/data/prgs/rust/iiac-perf/notes/design.md",
  "old_string": "(`ice-*`), and probe-instrumented producer/consumer variants\n(`pc`, `tp-pc`, `tp2-pc`) used to measure the probes\nthemselves.",
  "new_string": "(`ice-*`), and probe-instrumented variants (`probe-mpsc-2t`,\n`producer-consumer`, `tp-pc`, `tp2-pc`) used to measure the\nprobes themselves."
}
```

> TOOL

tool_result
id: toolu_01K9VZPbvWAb1bu6iwdgwfUW
```
The file /home/<USER>/data/prgs/rust/iiac-perf/notes/design.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

The chores section should reflect that the file now also carries the overview:

> TOOL

tool_use Edit
id: toolu_01Xb5MyDoMeeYH9Aja1hWwyK
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/data/prgs/rust/iiac-perf/notes/chores/chores-04.md",
  "old_string": "- notes/README.md gains a pointer to design.md.",
  "new_string": "- design.md also opens with an `## Architecture Overview` —\n  the four layers (startup / environment control,\n  measurement, benches, reporting), the two measurement\n  styles (harness-driven `Bench` vs self-driven probes), and\n  the bench-family map — so the error-model sections have a\n  structural map to hang off.\n- notes/README.md gains a pointer to design.md."
}
```

> TOOL

tool_result
id: toolu_01Xb5MyDoMeeYH9Aja1hWwyK
```
The file /home/<USER>/data/prgs/rust/iiac-perf/notes/chores/chores-04.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Done — `notes/design.md` now opens with an `## Architecture Overview` section, placed ahead of the calibration analysis so the file reads top-down from structure to specifics. I verified every module and bench name it cites against the source (one fix along the way: the probe-instrumented benches are `probe-mpsc-2t`, `producer-consumer`, `tp-pc`, `tp2-pc` — there's no bench named `pc`).

The overview describes the app in four layers:

- **Startup / environment control** — the fixed `main.rs` pipeline: clap CLI with prefix bench matching, `systemd-inhibit` re-exec, layered config (built-in < XDG < project-local < CLI), cal pinning with affinity save/restore, then the two-point calibration. The calibration bullet links down to the quantization analysis.
- **Measurement** — the two coexisting styles: harness-driven (`Bench` trait, adaptive `inner` via `pick_inner`, ps-recorded HDR histogram, overhead subtraction) and self-driven probes (`Probe` in ns, `TProbe` in raw ticks, `TProbe2` scope API with lazy drain), over the arch-neutral `ticks` facade.
- **Benches** — the flat registry in `benches/mod.rs` and the family map (timer baselines, mpsc, zcr, ice, probe-instrumented), plus the 1t/2t naming convention and what it's for.
- **Reporting** — `bands.rs` as the band-ladder SSOT, `harness::print_report` for the main table, `band_table.rs` as the shared renderer that keeps probe output visually […]

> DEVELOPER

Great, I still need to read it thoroughly, but more than good enough for now.
So where are we now?

> TOOL

tool_use Bash
id: toolu_01JVsdYM6RwUDYru44z6C1pB
```json
{
  "command": "jj st -R .",
  "description": "Show app repo working-copy status"
}
```

> TOOL

tool_result
id: toolu_01JVsdYM6RwUDYru44z6C1pB
```
Working copy changes:
M Cargo.lock
M notes/README.md
M notes/chores/chores-04.md
A notes/design.md
M notes/todo.md
Working copy  (@) : xmspulvo b0c1f096 (no description set)
Parent commit (@-): tuqqmuml 49260af2 main | feat: zcr-mpsc-1t/2t benches
```

> TOOL

tool_use Bash
id: toolu_01MPPHmEJoEpe7i963yUyfyw
```json
{
  "command": "jj diff -R . Cargo.lock --stat",
  "description": "Check Cargo.lock change size"
}
```

> TOOL

tool_result
id: toolu_01MPPHmEJoEpe7i963yUyfyw
```
Cargo.lock | 299 +++++++++++++++++++++++++++++++++++++++------------------------
1 file changed, 187 insertions(+), 112 deletions(-)
```

> AGENT

Here's the state of play:

**Working copy (uncommitted, on top of `main` = `feat: zcr-mpsc-1t/2t benches`):**

- `notes/design.md` (new) — Architecture Overview + the full calibration/framing-quantization analysis and the fix design (amortized framing measurement, cached constants in config with provenance + live validity check).
- `notes/chores/chores-04.md` — new section `## docs: add notes/design.md (calibration accuracy)` with empty `Commits:`, awaiting backfill after it lands.
- `notes/todo.md` — new #1: "Amortized framing calibration + cached constants in config", linked to the design.md analysis; renumbered and validated.
- `notes/README.md` — one-line pointer to design.md.
- `Cargo.lock` — a large change (187+/112−) that predates this session's work; it was already modified when we started. It's unrelated to the docs and shouldn't ride along in a docs commit — worth a look at what drove it (a `cargo update`?) before deciding its fate.

**No cycle is in progress** — this is a notes-only change, so it can land as a single `docs:` commit without a ladder, and the cargo validation cycle is skippable per protocol.

**Natural next steps, in order:**

1. You read design.md thoroughly (you said you still want to).
2. Decide what to do with Cargo.lock — split it out or land it […]

> DEVELOPER

So each version should/could have it's own Cargo.toml/lock files?

> TOOL

tool_use Bash
id: toolu_01PooWTfLuyHJwVxHwg4vyJJ
```json
{
  "command": "jj diff -R . Cargo.lock | grep '^[+-]name\\|^[+-]version\\|^[+-]source' | head -40",
  "description": "Summarize what changed in Cargo.lock"
}
```

> TOOL

tool_result
id: toolu_01PooWTfLuyHJwVxHwg4vyJJ
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01R8arSW9sc2nYuviKVsUuqA
```json
{
  "command": "jj diff -R . Cargo.lock --git | grep '^[+-]' | grep -v '^[+-][+-]' | grep 'name = \\|version = \\|source = ' | head -60",
  "description": "List package-level changes in Cargo.lock diff"
}
```

> TOOL

tool_result
id: toolu_01R8arSW9sc2nYuviKVsUuqA
```
-version = "1.5.0"
+version = "1.5.1"
-version = "2.11.1"
-source = "registry+https://github.com/rust-lang/crates.io-index"
+version = "1.3.2"
+source = "registry+https://github.com/rust-lang/crates.io-index"
+name = "bitflags"
+version = "2.13.0"
+source = "registry+https://github.com/rust-lang/crates.io-index"
-version = "3.20.2"
+version = "3.20.3"
-version = "1.2.65"
+version = "1.2.66"
-version = "4.6.0"
+version = "4.6.1"
-version = "4.6.0"
+version = "4.6.1"
-version = "0.5.15"
+version = "0.5.16"
-version = "0.8.21"
+version = "0.8.22"
+name = "defmt"
+version = "1.1.1"
+source = "registry+https://github.com/rust-lang/crates.io-index"
+name = "defmt-macros"
+version = "1.1.1"
+source = "registry+https://github.com/rust-lang/crates.io-index"
+name = "defmt-parser"
+version = "1.0.0"
+source = "registry+https://github.com/rust-lang/crates.io-index"
-version = "1.0.1"
+version = "2.0.0"
-version = "0.11.10"
+version = "0.11.11"
+name = "futures-core"
+version = "0.3.32"
+source = "registry+https://github.com/rust-lang/crates.io-index"
+name = "futures-task"
+version = "0.3.32"
+source = "registry+https://github.com/rust-lang/crates.io-index"
+name = "futures-util"
+version = "0.3.32"
+source = "registry+https://github.com/rust-lang/crates.io-index"
-version = "0.9.2"
+version = "0.9.3"
-version = "0.9.2"
+version = "0.9.3"
-version = "0.9.2"
+version = "0.9.3"
-version = "0.9.2"
+version = "0.9.3"
-version = "0.9.2"
+version = "0.9.3"
-version = "0.9.2"
+version = "0.9.3"
-version = "0.9.2"
+version = "0.9.3"
-version = "0.9.2"
+version = "0.9.3"
-version = "0.9.2"
```

> AGENT

Yes — and git already does that for you; the practice to adopt is making it *deliberate*.

Every commit snapshots the whole tree, so each released version X.Y.Z inherently carries the exact `Cargo.toml` (with `version = "X.Y.Z"`) and the exact `Cargo.lock` it was built from. That's the main reason a binary crate commits its lockfile at all: check out any version's commit, `cargo build`, and you get the same dependency graph it shipped with. You don't create per-version files; history is the per-version file.

What follows from that is a discipline about *when* the lockfile changes:

- **The routine case** — a cycle's `-0` version bump edits `Cargo.toml`, and `Cargo.lock` updates its own one-line entry for the `iiac-perf` package. That rides along with the bump commit; it's tiny and self-explanatory.
- **The deliberate case** — dependency changes (adding a dep, bumping `zc-ring-x1`, a `cargo update`) should be their own commit so history attributes them. Your pending diff is this kind: I looked, and it's a broad `cargo update` — many patch bumps plus what looks like iceoryx2 0.9.2 → 0.9.3, which pulled in new transitive crates (`defmt`, `futures-*`, `bitflags 2.13`).

And for this project specifically the stakes are higher than […]

> DEVELOPER

Could/Should we make each of the benchs standalone package, i.e. change iipc-perf to a workspace, with it's own set of dependencies that override the not now just thinking

> AGENT

Worth thinking through — but there's a Cargo fact that undercuts the specific mechanism: **a workspace shares one `Cargo.lock` across all members.** Workspace members don't get their own lockfiles; resolution is unified for the whole graph (semver-compatible requirements collapse to one version). So "workspace with per-bench dependency sets" doesn't exist as such — a `cargo update` would still move every bench's deps in one shot, in one shared lock.

What a workspace *does* buy you:

- **Dep scoping per package** — only the ice benches would declare `iceoryx2`, so the mpsc/zcr benches stop paying its build cost, and `cargo build -p bench-mpsc` gets fast.
- **Structural clarity** — the harness, probes, bands, and report code would become a library crate with a real public API, which is pressure in a healthy direction anyway (todo already has "extract shared message types + round-trip helpers").
- **Blast-radius control for builds** — a broken/heavy dep (iceoryx2 is the obvious one) can't take down building everything else.

What it costs: one binary becomes many (or a dispatcher), so `iiac-perf all` and prefix matching need rethinking; N `Cargo.toml`s to maintain; and each binary calibrates independently — fine, but cross-bench tables stop coming from one process. […]