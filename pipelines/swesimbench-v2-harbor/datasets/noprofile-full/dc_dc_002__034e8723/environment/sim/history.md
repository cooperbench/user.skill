[DEVELOPER]: Read doc/GFX1151_REFERENCE.md , doc/HIP_OPTIMIZATION_PLAN_FP16.md , doc/HIPBLASLT_REFERENCE.md for context. Now we focus on the input size 8192^3. Our HIP kernel only achieves 28.7 TFLOPS when benchmarked in C++ without Python and torch overhead, see cpp_benchmarks/build_benchmark_mm_hip_fp16.sh , while the hipBLASLt kernel achieves 37.6 TFLOPS, see cpp_benchmarks/build_benchmark_mm_hipblaslt_fp16.sh . Now your task is to study the hipBLASLt kernel. What warps_m/warps_n/unroll_k/repeat_m/repeat_n does it use? What other notable optimizations does it use? How should we close the perf gap from it? You may read the source code in ~/rocm-libraries/ .

[AGENT]: I’m reading the three reference docs and the two benchmark scripts first, then I’ll trace which hipBLASLt solution is actually selected for `8192x8192x8192` FP16 GEMM and map that back to its kernel parameters.

[AGENT]: The reference docs confirm the target path: `solution_index 1112`, kernel name beginning with `MT128x96x64_MI16x16x1`. I’m moving from wrapper context to the actual Tensile/hipBLASLt solution metadata now to recover the block layout and scheduling choices behind that kernel.

[AGENT]: I hit too-broad search output in the monorepo, so I’m narrowing to the exact kernel-name prefix and the gfx11 logic files. I also need to locate the standalone bench source path the note refers to, because the filename in the doc isn’t present verbatim.

[AGENT]: I’ve found the exact gfx1151 logic file that contains the target kernel family. Next step is reading the full solution entry, not just the encoded name, so I can translate Tensile’s `MIWT`, `WG`, `MT`, `DepthU`, and related flags into `warps_m/warps_n/unroll_k/repeat_m/repeat_n` plus the other performance-critical choices.

[AGENT]: I have one concrete candidate now: a gfx1151 Tensile solution with `MT128x96x64`, `MIWaveGroup [4,1]`, `MIWaveTile [2,6]`, `WorkGroup [64,2,1]`, `PrefetchGlobalRead 2`, and ~30 KB LDS. I’m validating that this is the exact runtime-selected kernel for your `8192^3` benchmark rather than just a same-prefix neighbor in the logic table.

[AGENT]: The solution string is confirmed now. It is not a generic `MT128x96x64` neighbor; your benchmark is actually dispatching that exact gfx1151 kernel. I’m pulling runtime resource metadata next so the comparison against our `(1,8,2,8,2)` kernel is grounded in threads/LDS/registers, not just the encoded name.

[AGENT]: Runtime profiling confirms the hipBLASLt kernel is quite register-heavy: `256 VGPR`, `128 SGPR`, `30,336 B LDS`, `128-thread` workgroup. I’m collecting the same metadata for our HIP kernel next so the “close the gap” recommendations are based on the actual resource and tiling tradeoffs, not guesswork.

[AGENT]: The resource contrast is sharp now. hipBLASLt uses `128` threads, `256 VGPR`, `30.3 KB LDS`; our winner uses `256` threads, `192 VGPR`, `24 KB LDS`. So the gap is not “hipBLASLt is just lighter.” It is spending more registers and more K-depth to cut something more important, likely global-refill and barrier exposure.

[AGENT]: I’m checking whether any already-supported config in our kernel family moves in hipBLASLt’s direction on `8192^3`: fewer waves, deeper `K`, and less extreme `N` width. If one of those is already competitive, that changes the “close the gap” plan from new-kernel work to scheduling and heuristic work.

[AGENT]: I’ve ruled out the simplest explanation: our existing deeper-`K` configs are not already “almost there.” On `8192^3`, the currently-supported `u=4` families are materially worse, so the gap is not a heuristic miss inside the current search space; it is a kernel-design gap.