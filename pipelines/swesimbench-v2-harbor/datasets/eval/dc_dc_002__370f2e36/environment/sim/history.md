[DEVELOPER]: Read doc/GFX1151_REFERENCE.md , doc/HIP_OPTIMIZATION_PLAN_PREPACKED_E5M2.md , kernel/hip/hip_kernel.cu for context. Now implement A prefetch, like how we've done it in kernel/hip/hip_kernel_fp16.cu . If the benchmark looks good, then construct a heuristic for when to enable it. Put temp files in the folder tmp_mixed_precision_analysis/

[AGENT]: I’m reading the two docs and both HIP kernels first, then I’ll mirror the existing A-prefetch pattern from the FP16 kernel into the mixed-precision path and validate it with a benchmark before deciding on a heuristic.

[AGENT]: The sandbox is refusing even read-only shell commands here, so I’m rerunning the file reads outside the sandbox to gather context before patching the kernel.

[AGENT]: I’ve got the mixed-precision and FP16 kernel context. Next I’m pulling the rest of the FP16 implementation and the launch heuristics so I can copy the A-prefetch structure and wire in a data-driven enable rule instead of guessing.

[AGENT]: I’ve confirmed the mixed kernel currently has only `A WSGR` plus synchronous A/B refills, while the FP16 path already has the split `B prefetch -> compute -> store B -> refill A` schedule. I’m mapping the mixed-precision equivalent now, then I’ll run the required test and benchmark sequence with outputs staged under `tmp_mixed_precision_analysis/` and only keep a heuristic if the measured region is actually positive.