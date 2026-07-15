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
  "command": "grep -rn \"framing\" --include=\"*.rs\" -l /home/wink/data/prgs/rust/iiac-perf/src | head",
  "description": "Find files mentioning framing"
}
```

> TOOL

tool_result
id: toolu_01UfvX8Zd9Lso65djsthkGYH
```
/home/wink/data/prgs/rust/iiac-perf/src/overhead.rs
/home/wink/data/prgs/rust/iiac-perf/src/benches/tp_pc.rs
/home/wink/data/prgs/rust/iiac-perf/src/main.rs
/home/wink/data/prgs/rust/iiac-perf/src/harness.rs
```

> TOOL

tool_use Read
id: toolu_01PUGvmyUrrJ4F124y4F3U1U
```json
{
  "file_path": "/home/wink/data/prgs/rust/iiac-perf/src/overhead.rs"
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