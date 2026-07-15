[DEVELOPER]: Edit cpp_benchmarks/*.cpp , besides avg_ms , report std_ms (standard deviation of the time in ms).

[AGENT]: I’m checking the benchmark sources under `cpp_benchmarks/` to see how timing is computed now, then I’ll patch the reporting to include `std_ms` alongside `avg_ms`.

[AGENT]: The sandbox blocked basic file inspection in this workspace, so I’m rerunning the reads with elevated access and then I’ll make the timing change directly in the benchmark sources.

[AGENT]: I found four benchmark sources with the same timing pattern. I’m reading the timing blocks and headers now so I can make one consistent change across all of them without touching unrelated code.

[AGENT]: I’ve confirmed the four `.cpp` benchmarks share the same reporting shape. Before editing, I’m checking whether any local tooling parses the current timing labels so I can preserve compatibility while adding `std_ms`.

[AGENT]: I’m patching the four benchmark sources now. The change is narrow: compute `std_ms` from the per-iteration timings after `avg_ms`, then print it as an extra summary line without changing the existing `avg ms` output that local scripts already parse.

[AGENT]: The code is patched. I’m doing a quick verification pass on the edited sources to confirm the new `std_ms` calculation and output landed in each benchmark cleanly.

[AGENT]: The source diffs look clean. I’m attempting a build verification next; if the local ROCm/libtorch setup blocks any target, I’ll stop at the exact failure rather than guess.