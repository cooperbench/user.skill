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

> AGENT

I checked `pick_inner` (`src/harness.rs:146-149`), and you're right to push on this — the adaptivity makes the framing error matter *more* than my "±0.23 ns at inner=43" framing, in two ways.

**The auto-sizing turns framing uncertainty into a roughly constant ~9% relative error.** `pick_inner` sizes `inner ≈ 10 × framing / step_cost`, i.e. the sample window is ten framings long regardless of step cost. The per-call adjustment error is `δ/inner` where δ is the framing estimation error, and substituting the sizing rule: `δ/inner ≈ δ × step / (10 × framing)` — so relative to the step cost it's `δ/(10 × framing)`, independent of how fast or slow the bench is. With framing ≈ 11 ns and δ up to a full ~10 ns quantum, that's up to ~9% error on *every* auto-sized bench, fast or slow. The adaptivity doesn't dilute the error; it holds it at a fixed fraction.

**Worse: the framing estimate feeds the sizing itself, so a low-quantum calibration under-sizes `inner`.** If a run draws the 1.02 ns calibration, `pick_inner` computes `ceil(10 × 1.02 / 2.9) ≈ 4` instead of ~43 for your zcr bench. Then the *true* ~11 ns framing is amortized over only 4 calls — […]